"""Compose GNU-compiled CPU, typed audio/sprites/dialogue/fonts and raw gaps."""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from tools.audio_formats import audio_formats as af
from tools.audio_build import audio_build as audio
from tools.dialogue_text import dialogue_text as dialogue
from tools.font_build import font_build as font
from tools.graphics_build import graphics_build as graphics
from tools.scaled_bitmaps import scaled_bitmaps as scaled
from tools.world_resources import world_resources as world
from tools.battle_graphics import battle_graphics as battle_graphics
from tools.scenario_build import scenario_build as scenario
from tools.portrait_graphics import portrait_graphics as portrait
from tools.terrain_maps import terrain_maps as terrain
from tools.battlefield_resources import battlefield_resources as battlefield
from tools.ui_layouts import ui_layouts as ui
from tools.personnel_build import personnel_build as personnel
from tools.candidate_tables import candidate_tables as candidate_tables
from tools.candidate_source import candidate_source as candidate_source
from tools.candidate_action_tables import candidate_action_tables as action_tables
from tools.candidate_action_source import candidate_action_source as action_source
from tools.candidate_handler_tables import candidate_handler_tables as handler_tables
from tools.candidate_handler_source import candidate_handler_source as handler_source
from tools.candidate_handler_49e_source import candidate_handler_49e_source as handler49e_source
from tools.candidate_handler_9b0_source import candidate_handler_9b0_source as handler9b0_source
from tools.candidate_handler_c26_source import candidate_handler_c26_source as handlerc26_source

SOURCE = ROOT / 'src/m68k/recovered_code.s'
PRIMARY = ROOT / 'analysis/integration/semantic_primary_regions.csv'
INSTRUCTIONS = ROOT / 'analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv'
PRIMARY_HASH = reference_value(__name__, 'PRIMARY_HASH')
INSTRUCTIONS_HASH = reference_value(__name__, 'INSTRUCTIONS_HASH')
# The base mnemonics actually present in the audited 68000 source. GNU also
# accepts dotless data directives (e.g. dc.w); a lexical shape alone is unsafe.
MNEMONICS = frozenset(('add adda addi addq and andi asl asr bcc bchg bclr bcs beq '
    'bhi bls bmi bne bpl bra bset bsr btst clr cmp cmpa cmpi dbra divu eor eori '
    'exg ext jmp jsr lea lsl lsr move movea movem moveq muls mulu neg nop not '
    'or ori ror roxl roxr rte rts sub subi subq swap tst').split())


def sha(data): return hashlib.sha256(data).hexdigest()
def dump(value): return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)+'\n').encode('utf-8')
def read(path, limit=16*1024*1024): return af._read(af.safe_path(path, regular_input=True), limit)


def inventory(rom):
    af.verify_rom(rom)
    primary_raw, instruction_raw = read(PRIMARY), read(INSTRUCTIONS)
    if sha(primary_raw) != PRIMARY_HASH: raise ValueError('primary partition changed; re-audit build scope')
    if sha(instruction_raw) != INSTRUCTIONS_HASH: raise ValueError('instruction map changed; re-audit build scope')
    primary = list(csv.DictReader(io.StringIO(primary_raw.decode('utf-8-sig'))))
    owners = {address for region in primary if region['classification'] == 'm68k_code'
              for address in range(int(region['start']), int(region['end']))}
    records, observed = [], set()
    partial, touched = [], set()
    for row in csv.DictReader(io.StringIO(instruction_raw.decode('utf-8-sig'))):
        start, size = int(row['address']), int(row['size'])
        raw = bytes.fromhex(row['bytes'])
        if size < 2 or size > 10 or start & 1 or len(raw) != size or raw != rom[start:start+size]:
            raise ValueError('instruction identity or width mismatch')
        span = set(range(start, start+size))
        if observed & span: raise ValueError('overlapping source instruction rows')
        observed.update(span)
        if not span & owners: continue
        touched.update(span & owners)
        if not span <= owners:
            partial.append({'address': start, 'size': size, 'owned_bytes': len(span & owners), 'bytes': raw.hex()})
            continue
        records.append({'address': start, 'size': size, 'bytes': raw.hex(),
                        'original_mnemonic': row['mnemonic'], 'original_operand': row['operand'],
                        'discovery_confidence': row['confidence']})
    records.sort(key=lambda row: row['address'])
    if len(records) != 11671 or sum(row['size'] for row in records) != 42752:
        raise ValueError('confirmed instruction selection changed; re-audit before widening')
    return records, {'canonical_rom_sha256': af.ROM_SHA256, 'primary_sha256': sha(primary_raw),
        'instructions_sha256': sha(instruction_raw), 'selected_instructions': len(records),
        'selected_code_bytes': sum(row['size'] for row in records), 'primary_code_bytes': len(owners),
        'straddling_instructions': partial, 'owned_bytes_without_instruction_rows': sorted(owners-touched),
        'ownership_bytes_added': 0, 'complete_indirect_domains_added': 0}


def validate_source(source, records, *, allowed_mnemonics=None):
    try: text = source.decode('utf-8')
    except (UnicodeError, AttributeError) as error: raise ValueError('source must be UTF-8 bytes') from error
    if len(source) > 4*1024*1024: raise ValueError('oversize instruction source')
    lines = [line.split('|', 1)[0].strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    if lines[:3] != ['.cpu 68000', '.section .text', '_start:']:
        raise ValueError('fixed source header changed')
    if len(lines) != 3 + 4*len(records): raise ValueError('instruction source topology changed')
    for index, row in enumerate(records):
        group = lines[3+4*index:7+4*index]
        address = row['address']
        if group[0] != f'.org 0x{address:X}' or group[1] != f'm68k_{address:06x}:' or group[3] != f'm68k_{address:06x}_end:':
            raise ValueError('source fixed address/extent labels changed')
        if len(group[2]) > 256 or not re.fullmatch(r'[A-Za-z][A-Za-z0-9.]*([ \t]+[A-Za-z0-9_.$%#():,+*/ <>\-]+)?', group[2]):
            raise ValueError('expected exactly one mnemonic, no directives or additional statements')
        if group[2].split()[0].split('.')[0].lower() not in (MNEMONICS if allowed_mnemonics is None else allowed_mnemonics):
            raise ValueError('unapproved mnemonic or dotless assembler directive')
        # GAS permits whitespace before a label colon: `nop : dc.w ...` is
        # a label plus a directive, not an instruction. Only numeric absolute
        # address width suffixes may contain a colon in this source dialect.
        without_widths = re.sub(r'\b0x[0-9a-fA-F]+:[wWlL]\b', '', group[2])
        if ':' in without_widths or '/*' in group[2] or '*/' in group[2]:
            raise ValueError('labels or block comments inside an instruction are forbidden')
    return {'source_sha256': sha(source), 'source_instruction_count': len(records)}


def coalesce(records):
    result = []
    for row in records:
        start, end = row['address'], row['address']+row['size']
        if result and start == result[-1][1]: result[-1][1] = end
        else: result.append([start, end])
    return result


def gap(bank, offset, size, ranges, consumed, image_sources=None):
    start, end = bank*65536+offset, bank*65536+offset+size
    cursor, lines = start, []
    for first, last in ranges:
        if last <= start or first >= end: continue
        if first < start or last > end: raise ValueError('code range crosses typed asset or bank boundary')
        if cursor < first:
            lines.append(f'        .incbin "segments/bank{bank:02x}.bin", 0x{cursor-bank*65536:X}, 0x{first-cursor:X}')
        image_name = (image_sources or {}).get(first, 'm68k_code.bin')
        if image_name not in ('m68k_code.bin', 'm68k_candidate_code.bin', 'm68k_action_code.bin', 'm68k_handler_code.bin', 'm68k_handler49e_code.bin', 'm68k_handler9b0_code.bin', 'm68k_handlerc26_code.bin'):
            raise ValueError('unexpected compiled source image')
        lines.append(f'        .incbin "{image_name}", 0x{first:X}, 0x{last-first:X}')
        consumed.extend(range(first, last)); cursor = last
    if cursor < end:
        lines.append(f'        .incbin "segments/bank{bank:02x}.bin", 0x{cursor-bank*65536:X}, 0x{end-cursor:X}')
    return lines


def combined_bank08_source(font_rows, dialogue_rows):
    """Jointly emit font and name fields, leaving other bank08 bytes explicit."""
    font.bank_source(8,font_rows)  # Validate the complete fixed 1290-glyph topology.
    names=[row for row in dialogue_rows if 0x80000<=row['start']<0x90000]
    if len(names)!=296 or sum(row['end']-row['start'] for row in names)!=1696:
        raise ValueError('bank08 dialogue field scope changed')
    for row in names:
        if row['role'] not in ('officer_name','city_name') or row['start']&1 or row['end']&1:
            raise ValueError('unsupported bank08 dialogue field')
        if type(row['data']) is not bytes or len(row['data'])!=row['end']-row['start']:
            raise ValueError('bank08 dialogue width mismatch')
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',row['id']): raise ValueError('invalid dialogue label')
    rows=sorted([*font_rows,*names],key=lambda row:row['start'])
    label='dialogue_bank_08'; lines=[label+':']; cursor=0x80000
    for row in rows:
        if row['start']<cursor or not row['start']<row['end']<=0x90000:
            raise ValueError('overlapping or crossing bank08 typed fields')
        if cursor<row['start']:
            lines.append(f'        .incbin "segments/bank08.bin", 0x{cursor-0x80000:X}, 0x{row["start"]-cursor:X}')
        if row['role'] in ('font16_1bpp_rows','font8_1bpp_rows'):
            lines.extend(font.block_lines(row,label))
        else:
            lines.extend([f'        .if (. - {label}) != 0x{row["start"]-0x80000:X}',
                '        .error "dialogue field offset changed"','        .endif',
                f'        | {row["id"]}: {row["role"]}',
                '        .word '+','.join(f'0x{int.from_bytes(row["data"][p:p+2],"big"):04X}' for p in range(0,len(row['data']),2))])
        cursor=row['end']
    if cursor<0x90000:
        lines.append(f'        .incbin "segments/bank08.bin", 0x{cursor-0x80000:X}, 0x{0x90000-cursor:X}')
    lines.extend([f'        .if (. - {label}) != 0x10000','        .error "combined font/dialogue bank size changed"','        .endif'])
    return ('\n'.join(lines)+'\n').encode()


def typed_gap(bank,offset,size,ranges,consumed,rows,typed_consumed,image_sources=None):
    """Split derived field bytes at bank/gap boundaries without new authority.

    Odd RLE words and tiles crossing a 64KiB bank stay one source field; only
    their generated assembly representation is split. Every emitted byte is
    accounted for globally below, so a hidden overlap cannot be omitted.
    """
    first=bank*65536+offset; end=first+size; cursor=first; lines=[]
    for row in rows:
        start=max(first,row['start']); stop=min(end,row['end'])
        if start>=stop: continue
        if start<cursor: raise ValueError('overlapping typed graphics fields')
        if any(a<stop and start<b for a,b in ranges): raise ValueError('typed fields overlap compiled CPU')
        lines.extend(gap(bank,cursor-bank*65536,start-cursor,ranges,consumed,image_sources))
        data=row['data'][start-row['start']:stop-row['start']]
        lines.extend([f'        | {row["id"]}: {row["role"]}; derived byte offset {start-row["start"]}',
            f'        .if (. - m68k_bank_{bank:02x}_origin) != 0x{start-bank*65536:X}',
            '        .error "typed graphics offset changed"','        .endif'])
        for p in range(0,len(data),16):
            lines.append('        .byte '+','.join(f'0x{v:02X}' for v in data[p:p+16]))
        typed_consumed.extend(range(start,stop)); cursor=stop
    lines.extend(gap(bank,cursor-bank*65536,end-cursor,ranges,consumed,image_sources))
    return lines


def phase23_source_scope(rows, label):
    """Fixed editor allocations, not bounds imposed on original CPU readers."""
    expected=(set(range(0xAB8C4,0xABDCA)) if label=='UI' else
              set(range(0x11080,0x1108C))|set(range(0xAADE2,0xAB8C4)))
    positions=[]
    for row in rows:
        if (type(row['start']) is not int or type(row['end']) is not int or
            not 0<=row['start']<row['end']<=af.ROM_SIZE):
            raise ValueError(label+' source scope contains invalid bounds')
        positions.extend(range(row['start'],row['end']))
    if len(positions)!=len(expected) or set(positions)!=expected:
        raise ValueError(label+' source scope changed, omitted, duplicated or relocated')


def phase24_source_scope(rows):
    expected = set(range(0x17BB2,0x17BBE)) | set(range(0x1A492,0x1A49E)) | set(range(0x30876,0x30960))
    positions = []
    for row in rows:
        if (type(row['start']) is not int or type(row['end']) is not int or
                not 0 <= row['start'] < row['end'] <= af.ROM_SIZE):
            raise ValueError('candidate table source scope invalid')
        positions.extend(range(row['start'],row['end']))
    if len(positions) != 258 or set(positions) != expected:
        raise ValueError('candidate table source scope changed, omitted or duplicated')


def supplemental_selection(rom, legacy_records):
    extra_records, extra_info = candidate_source.inventory(rom)
    # Independent integration approval; package output cannot widen itself.
    expected = [(0x468,0x46C),(0xCE4,0xCEC),(0x17A9E,0x17BB2),
                (0x17BBE,0x17C7A),(0x1A44E,0x1A47A),(0x3080E,0x30876)]
    if len(extra_records) != 184 or coalesce(extra_records) != [list(r) for r in expected]:
        raise ValueError('candidate CPU source scope changed')
    if sha(candidate_source.csv_bytes(extra_records)) != reference_value(__name__, 'supplemental_selection'):
        raise ValueError('candidate CPU independently approved records changed')
    legacy = {p for r in legacy_records for p in range(r['address'],r['address']+r['size'])}
    additional = [p for r in extra_records for p in range(r['address'],r['address']+r['size'])]
    if len(additional) != 624 or len(set(additional)) != 624 or legacy.intersection(additional):
        raise ValueError('candidate CPU source overlaps or changes scope')
    return extra_records,extra_info


def phase25_source_scope(rows):
    expected = ((0x19B42,0x19B5E),(0x19C96,0x19C9E),(0x19E0E,0x19E16),
                (0x19EC2,0x19ECE),(0x1AFA0,0x1AFAC),(0x1AFAC,0x1AFBC))
    actual=[]
    for row in rows:
        if (type(row['start']) is not int or type(row['end']) is not int or
                not 0 <= row['start'] < row['end'] <= af.ROM_SIZE):
            raise ValueError('action table source scope invalid')
        actual.append((row['start'],row['end']))
    if tuple(actual) != expected:
        raise ValueError('action table source scope changed, omitted, duplicated or reordered')


def action_selection(rom, legacy_records, phase24_records):
    records,info = action_source.inventory(rom)
    expected = ((0x83D4,0x83FA),(0x19B2C,0x19B42),(0x19C9E,0x19E0E),(0x19E16,0x19EC2),
                (0x19ECE,0x19EF0),(0x1A47A,0x1A492),(0x1AF80,0x1AFA0),(0x1AFBC,0x1B098))
    if len(records) != 241 or coalesce(records) != [list(pair) for pair in expected]:
        raise ValueError('action CPU source scope changed')
    if sha(action_source.csv_bytes(records)) != reference_value(__name__, 'action_selection'):
        raise ValueError('action CPU independently approved records changed')
    old = {p for row in [*legacy_records,*phase24_records] for p in range(row['address'],row['address']+row['size'])}
    positions = [p for row in records for p in range(row['address'],row['address']+row['size'])]
    if len(positions) != 910 or len(set(positions)) != 910 or old.intersection(positions):
        raise ValueError('action CPU overlaps a previous compiled source')
    # Existing semantic ownership is not the same as an existing build emitter.
    # This shared RNG was raw before Phase25 and remains multi_consumer-owned.
    if info.get('existing_multi_consumer_bytes') != 38 or info.get('ownership_bytes_added') != 0:
        raise ValueError('action RNG existing-owner qualification changed')
    return records,info


def phase26_source_scope(rows):
    expected=((0x1A1DC,0x1A200),(0x1A808,0x1A818))
    actual=[]
    for row in rows:
        if (type(row['start']) is not int or type(row['end']) is not int or
                not 0<=row['start']<row['end']<=af.ROM_SIZE):
            raise ValueError('handler table source scope invalid')
        actual.append((row['start'],row['end']))
    if tuple(actual)!=expected:
        raise ValueError('handler table source scope changed, omitted, duplicated or reordered')


def handler_selection(rom,legacy_records,phase24_records,phase25_records):
    records,info=handler_source.inventory(rom)
    if len(records)!=196 or coalesce(records)!=[[0x1A706,0x1A808],[0x1A818,0x1A9AA]]:
        raise ValueError('handler CPU source scope changed')
    if sha(handler_source.csv_bytes(records))!=reference_value(__name__, 'handler_selection'):
        raise ValueError('handler CPU independently approved records changed')
    old={p for row in [*legacy_records,*phase24_records,*phase25_records]
         for p in range(row['address'],row['address']+row['size'])}
    positions=[p for row in records for p in range(row['address'],row['address']+row['size'])]
    if len(positions)!=660 or len(set(positions))!=660 or old.intersection(positions):
        raise ValueError('handler CPU overlaps a previous compiled source')
    if info.get('ownership_bytes_added')!=0 or info.get('source_confidence')!='probable':
        raise ValueError('handler source qualification changed')
    if set(range(0x83D4,0x83FA))&set(positions):
        raise ValueError('handler source must reuse, not duplicate RNG')
    return records,info


def handler49e_selection(rom,legacy_records,phase24_records,phase25_records,phase26_records):
    records,info=handler49e_source.inventory(rom)
    if len(records)!=183 or coalesce(records)!=[[0x1A438,0x1A44E],[0x1A49E,0x1A706]]:
        raise ValueError('handler49e CPU source scope changed')
    if sha(handler49e_source.csv_bytes(records))!=reference_value(__name__, 'handler49e_selection'):
        raise ValueError('handler49e CPU independently approved records changed')
    old={p for row in [*legacy_records,*phase24_records,*phase25_records,*phase26_records]
         for p in range(row['address'],row['address']+row['size'])}
    positions=[p for row in records for p in range(row['address'],row['address']+row['size'])]
    if len(positions)!=638 or len(set(positions))!=638 or old.intersection(positions):
        raise ValueError('handler49e CPU overlaps a previous compiled source')
    if (info.get('ownership_bytes_added')!=0 or info.get('source_confidence')!='probable' or
        info.get('complete_indirect_domains_added')!=0 or info.get('natural_runtime_observations_added')!=0):
        raise ValueError('handler49e source qualification changed')
    reused=set(range(0x83D4,0x83FA))|set(range(0x1A44E,0x1A47A))|set(range(0x1A706,0x1A808))
    if not reused<=old or reused.intersection(positions):
        raise ValueError('handler49e shared code must retain its previous physical emitters')
    if set(range(0x1A492,0x1A49E)).intersection(positions):
        raise ValueError('handler49e dispatch already belongs to candidate_tables')
    return records,info



def handler9b0_selection(rom,legacy_records,phase24_records,phase25_records,phase26_records,phase27_records):
    records,info=handler9b0_source.inventory(rom)
    if len(records)!=182 or coalesce(records)!=[[0x1A9B0,0x1AC1E]]:
        raise ValueError('handler9b0 CPU source scope changed')
    if sha(handler9b0_source.csv_bytes(records))!=reference_value(__name__, 'handler9b0_selection'):
        raise ValueError('handler9b0 CPU independently approved records changed')
    old={p for row in [*legacy_records,*phase24_records,*phase25_records,*phase26_records,*phase27_records]
         for p in range(row['address'],row['address']+row['size'])}
    positions=[p for row in records for p in range(row['address'],row['address']+row['size'])]
    if len(positions)!=622 or len(set(positions))!=622 or old.intersection(positions):
        raise ValueError('handler9b0 CPU overlaps a previous compiled source')
    if (info.get('ownership_bytes_added')!=0 or info.get('source_confidence')!='probable' or
        info.get('complete_indirect_domains_added')!=0 or info.get('natural_runtime_observations_added')!=0):
        raise ValueError('handler9b0 source qualification changed')
    reused=set(range(0x83D4,0x83FA))|set(range(0x1A438,0x1A47A))|set(range(0x1A706,0x1A808))
    if len(reused)!=362 or not reused<=old or reused.intersection(positions):
        raise ValueError('handler9b0 shared code must retain its previous physical emitters')
    if any(set(range(a,z)).intersection(positions) for a,z in ((0x1A1DC,0x1A200),(0x1A492,0x1A49E),(0x1A808,0x1A818),(0x1A9AA,0x1A9B0),(0x1AC1E,0x1AC26))):
        raise ValueError('handler9b0 old tables and unknown neighbours are excluded')
    return records,info


def handlerc26_selection(rom,legacy_records,phase24_records,phase25_records,phase26_records,phase27_records,phase28_records):
    records,info=handlerc26_source.inventory(rom)
    if len(records)!=264 or coalesce(records)!=[[0x1AC26,0x1AE6E],[0x1AEA0,0x1AF4C],[0x1AF5C,0x1AF78],[0x208CE,0x20930]]:
        raise ValueError('handlerc26 CPU source scope changed')
    if sha(handlerc26_source.csv_bytes(records))!=reference_value(__name__, 'handlerc26_selection'):
        raise ValueError('handlerc26 CPU independently approved records changed')
    old={p for row in [*legacy_records,*phase24_records,*phase25_records,*phase26_records,*phase27_records,*phase28_records]
         for p in range(row['address'],row['address']+row['size'])}
    positions=[p for row in records for p in range(row['address'],row['address']+row['size'])]
    if len(positions)!=882 or len(set(positions))!=882 or old.intersection(positions):
        raise ValueError('handlerc26 CPU overlaps a previous compiled source')
    if (info.get('ownership_bytes_added')!=0 or info.get('source_confidence')!='probable' or
        info.get('complete_indirect_domains_added')!=0 or info.get('natural_runtime_observations_added')!=0):
        raise ValueError('handlerc26 source qualification changed')
    reused=set(range(0x83D4,0x83FA))|set(range(0x1A7F4,0x1A808))
    if len(reused)!=58 or not reused<=old or reused.intersection(positions):
        raise ValueError('handlerc26 shared code must retain its previous physical emitters')
    if any(set(range(a,z)).intersection(positions) for a,z in ((0x1A1DC,0x1A200),(0x1A492,0x1A49E),(0x1A808,0x1A818),(0x1AC1E,0x1AC26),(0x1AE6E,0x1AEA0),(0x1AF4C,0x1AF54),(0x1AF54,0x1AF5C),(0x1AF78,0x1AF80))):
        raise ValueError('handlerc26 old tables and unknown neighbours are excluded')
    return records,info


def render_layout(rom, source, audio_assets, dialogue_assets=None, font_assets=None, graphics_assets=None,
                  scaled_assets=None, world_assets=None, battle_graphics_assets=None, scenario_assets=None, portrait_assets=None,
                  terrain_assets=None, battlefield_assets=None, ui_assets=None, personnel_assets=None,
                  candidate_tables_assets=None, candidate_code_source=None,
                  action_tables_assets=None, action_code_source=None,
                  handler_tables_assets=None, handler_code_source=None, handler49e_code_source=None, handler9b0_code_source=None, handlerc26_code_source=None):
    records, info = inventory(rom)
    info.update(validate_source(source, records))
    additional_records, additional_info = supplemental_selection(rom, records)
    if candidate_code_source is None: candidate_code_source = read(candidate_source.SOURCE)
    additional_info.update(validate_source(candidate_code_source, additional_records))
    action_records,action_info = action_selection(rom,records,additional_records)
    if action_code_source is None: action_code_source = read(action_source.SOURCE)
    action_info.update(validate_source(action_code_source,action_records))
    handler_records,handler_info=handler_selection(rom,records,additional_records,action_records)
    if handler_code_source is None:handler_code_source=read(handler_source.SOURCE)
    handler_info.update(validate_source(handler_code_source,handler_records))
    handler49e_records,handler49e_info=handler49e_selection(rom,records,additional_records,action_records,handler_records)
    if handler49e_code_source is None:handler49e_code_source=read(handler49e_source.SOURCE)
    handler49e_info.update(validate_source(handler49e_code_source,handler49e_records))
    handler9b0_records,handler9b0_info=handler9b0_selection(rom,records,additional_records,action_records,handler_records,handler49e_records)
    if handler9b0_code_source is None:handler9b0_code_source=read(handler9b0_source.SOURCE)
    handler9b0_info.update(validate_source(handler9b0_code_source,handler9b0_records))
    handlerc26_records,handlerc26_info=handlerc26_selection(rom,records,additional_records,action_records,handler_records,handler49e_records,handler9b0_records)
    if handlerc26_code_source is None:handlerc26_code_source=read(handlerc26_source.SOURCE)
    handlerc26_info.update(validate_source(handlerc26_code_source,handlerc26_records))
    audio_bundle = audio.render(rom, audio_assets)
    if dialogue_assets is None:
        dialogue_assets = af.load_assets(read(dialogue.DEFAULT_ASSETS))
    dialogue_rows = dialogue.blocks(rom, dialogue_assets)
    dialogue_bytes = sum(row['end']-row['start'] for row in dialogue_rows)
    if dialogue_bytes != 8570 or {row['start']//65536 for row in dialogue_rows} != {8,9}:
        raise ValueError('dialogue build scope changed; re-audit before widening')
    if font_assets is None:
        font_assets = af.load_assets(read(font.DEFAULT_ASSETS))
    font_rows = font.blocks(rom,font_assets)
    font_bytes = sum(row['end']-row['start'] for row in font_rows)
    if font_bytes != 35136: raise ValueError('font build scope changed; re-audit before widening')
    if graphics_assets is None: graphics_assets=af.load_assets(read(graphics.DEFAULT_ASSETS))
    graphics_rows=graphics.blocks(rom,graphics_assets)
    graphics_bytes=sum(row['end']-row['start'] for row in graphics_rows)
    if graphics_bytes!=90418: raise ValueError('graphics build scope changed; re-audit before widening')
    if scaled_assets is None: scaled_assets=af.load_assets(read(scaled.DEFAULT_ASSETS))
    if world_assets is None: world_assets=af.load_assets(read(world.DEFAULT_ASSETS))
    scaled_rows=scaled.blocks(rom,scaled_assets); world_rows=world.blocks(rom,world_assets)
    if sum(r['end']-r['start'] for r in scaled_rows)!=924: raise ValueError('scaled build scope changed')
    if sum(r['end']-r['start'] for r in world_rows)!=5821: raise ValueError('world build scope changed')
    if battle_graphics_assets is None: battle_graphics_assets=af.load_assets(read(battle_graphics.DEFAULT_ASSETS))
    if scenario_assets is None: scenario_assets=af.load_assets(read(scenario.DEFAULT_ASSETS))
    if portrait_assets is None: portrait_assets=af.load_assets(read(portrait.DEFAULT_ASSETS))
    if terrain_assets is None: terrain_assets=af.load_assets(read(terrain.DEFAULT_ASSETS))
    battle_rows=battle_graphics.blocks(rom,battle_graphics_assets)
    scenario_rows=scenario.blocks(rom,scenario_assets); portrait_rows=portrait.blocks(rom,portrait_assets)
    if sum(r['end']-r['start'] for r in battle_rows)!=45719: raise ValueError('battle graphics build scope changed')
    if sum(r['end']-r['start'] for r in scenario_rows)!=31872: raise ValueError('scenario build scope changed')
    if sum(r['end']-r['start'] for r in portrait_rows)!=126400: raise ValueError('portrait build scope changed')
    terrain_rows=terrain.blocks(rom,terrain_assets)
    if sum(r['end']-r['start'] for r in terrain_rows)!=90112: raise ValueError('terrain build scope changed')
    if battlefield_assets is None: battlefield_assets=af.load_assets(read(battlefield.DEFAULT_ASSETS))
    battlefield_rows=battlefield.blocks(rom,battlefield_assets)
    if sum(r['end']-r['start'] for r in battlefield_rows)!=9680: raise ValueError('battlefield build scope changed')
    if ui_assets is None: ui_assets=af.load_assets(read(ui.DEFAULT_ASSETS))
    if personnel_assets is None: personnel_assets=af.load_assets(read(personnel.DEFAULT_ASSETS))
    ui_rows=ui.blocks(rom,ui_assets); personnel_rows=personnel.blocks(rom,personnel_assets)
    if sum(r['end']-r['start'] for r in ui_rows)!=1286: raise ValueError('UI build scope changed')
    if sum(r['end']-r['start'] for r in personnel_rows)!=2798: raise ValueError('personnel build scope changed')
    phase23_source_scope(ui_rows,'UI'); phase23_source_scope(personnel_rows,'personnel')
    if candidate_tables_assets is None: candidate_tables_assets=af.load_assets(read(candidate_tables.DEFAULT_ASSETS))
    candidate_rows=candidate_tables.blocks(rom,candidate_tables_assets)
    phase24_source_scope(candidate_rows)
    if action_tables_assets is None: action_tables_assets=af.load_assets(read(action_tables.DEFAULT_ASSETS))
    action_rows=action_tables.blocks(rom,action_tables_assets)
    phase25_source_scope(action_rows)
    if handler_tables_assets is None:handler_tables_assets=af.load_assets(read(handler_tables.DEFAULT_ASSETS))
    handler_rows=handler_tables.blocks(rom,handler_tables_assets)
    phase26_source_scope(handler_rows)
    extra_rows=sorted(graphics_rows+scaled_rows+world_rows+battle_rows+scenario_rows+portrait_rows+terrain_rows+battlefield_rows+ui_rows+personnel_rows+candidate_rows+action_rows+handler_rows,key=lambda r:r['start'])
    for row in extra_rows:
        if (type(row['start']) is not int or type(row['end']) is not int or
            not 0<=row['start']<row['end']<=len(rom) or type(row['data']) is not bytes or
            len(row['data'])!=row['end']-row['start'] or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',row['id']) or
            not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',row['role'])):
            raise ValueError('invalid derived typed block')
    if any(a['end']>b['start'] for a,b in zip(extra_rows,extra_rows[1:])):
        raise ValueError('overlapping typed resource sources')
    extra_bytes=graphics_bytes+924+5821+45719+31872+126400+90112+9680+1286+2798+258+84+52
    typed_consumed=[]
    legacy_ranges, additional_ranges = coalesce(records), coalesce(additional_records)
    action_ranges=coalesce(action_records)
    handler_ranges=coalesce(handler_records)
    handler49e_ranges=coalesce(handler49e_records)
    handler9b0_ranges=coalesce(handler9b0_records)
    handlerc26_ranges=coalesce(handlerc26_records)
    ranges, consumed, bundle = sorted(legacy_ranges+additional_ranges+action_ranges+handler_ranges+handler49e_ranges+handler9b0_ranges+handlerc26_ranges), [], {}
    image_sources = {first:'m68k_candidate_code.bin' for first,_ in additional_ranges}
    image_sources.update({first:'m68k_action_code.bin' for first,_ in action_ranges})
    image_sources.update({first:'m68k_handler_code.bin' for first,_ in handler_ranges})
    image_sources.update({first:'m68k_handler49e_code.bin' for first,_ in handler49e_ranges})
    image_sources.update({first:'m68k_handler9b0_code.bin' for first,_ in handler9b0_ranges})
    image_sources.update({first:'m68k_handlerc26_code.bin' for first,_ in handlerc26_ranges})
    for bank in range(16):
        bank_rows=[row for row in extra_rows if row['start']<(bank+1)*65536 and row['end']>bank*65536]
        if bank in (0, 15):
            original = audio_bundle[f'bank{bank:02x}.s'].decode('utf-8').splitlines()
        elif bank == 8:
            original = combined_bank08_source(font_rows,dialogue_rows).decode('utf-8').splitlines()
        elif bank == 9:
            original = dialogue.bank_source(bank, dialogue_rows).decode('utf-8').splitlines()
        elif bank == 2:
            original = ['        .incbin "segments/bank02.bin", 0x0, 0x9038',
                        '        .include "../analysis/sprite_records/generated/sprite_records.s"',
                        '        .incbin "segments/bank02.bin", 0xA22E, 0x5DD2']
        else:
            original = [f'        .incbin "segments/bank{bank:02x}.bin", 0x0, 0x10000']
        output = [f'm68k_bank_{bank:02x}_origin:']
        for line in original:
            match = re.fullmatch(r'\s*\.incbin "segments/bank([0-9a-f]{2})\.bin", 0x([0-9A-F]+), 0x([0-9A-F]+)', line)
            if match:
                if int(match[1],16) != bank: raise ValueError('wrong source bank')
                output.extend(typed_gap(bank,int(match[2],16),int(match[3],16),ranges,consumed,bank_rows,typed_consumed,image_sources))
            else: output.append(line)
        bundle[f'm68k_bank{bank:02x}.s'] = ('\n'.join(output)+'\n').encode('utf-8')
    selected = {p for first,last in ranges for p in range(first,last)}
    if len(consumed) != len(selected) or set(consumed) != selected:
        raise ValueError('compiled code omitted or emitted more than once')
    typed_selected={p for row in extra_rows for p in range(row['start'],row['end'])}
    if len(typed_consumed)!=extra_bytes or set(typed_consumed)!=typed_selected:
        raise ValueError('typed graphics omitted, duplicated or overlapping another source')
    info.update(typed_audio_bytes=27258, typed_sprite_bytes=4598, typed_dialogue_bytes=dialogue_bytes,
                dialogue_assets_sha256=sha(dialogue.dump(dialogue_assets)),
                typed_font_bytes=font_bytes,font_assets_sha256=sha(font.dump(font_assets)),
                typed_graphics_bytes=graphics_bytes,graphics_assets_sha256=sha(graphics.dump(graphics_assets)),
                graphics_candidate_purpose_transfer_bytes=320,
                typed_scaled_bitmap_bytes=924,scaled_assets_sha256=sha(scaled.dump(scaled_assets)),
                typed_world_resource_bytes=5821,world_assets_sha256=sha(world.dump(world_assets)),
                typed_battle_graphics_bytes=45719,battle_graphics_assets_sha256=sha(battle_graphics.g.dump(battle_graphics_assets)),
                typed_scenario_bytes=31872,scenario_assets_sha256=sha(scenario.dump(scenario_assets)),
                typed_portrait_bytes=126400,portrait_assets_sha256=sha(portrait.dump(portrait_assets)),
                portrait_allocation_confidence='probable',
                typed_terrain_bytes=90112,terrain_assets_sha256=sha(terrain.dump(terrain_assets)),
                terrain_confirmed_field_bytes=89994,terrain_probable_type_bytes=118,
                typed_battlefield_bytes=9680,battlefield_assets_sha256=sha(battlefield.dump(battlefield_assets)),
                battlefield_editor_slots_are_cpu_domain=False,
                typed_ui_layout_bytes=1286,ui_assets_sha256=sha(ui.dump(ui_assets)),
                ui_caller_unproven_candidate_bytes=156,ui_editor_bounds_are_cpu_domain=False,
                typed_personnel_candidate_bytes=2798,personnel_assets_sha256=sha(personnel.dump(personnel_assets)),
                personnel_source_authority='analysis/personnel_flow/generated/scenario_candidates.json',
                typed_candidate_table_bytes=258,candidate_tables_assets_sha256=sha(candidate_tables.dump(candidate_tables_assets)),
                candidate_table_conditional_reference_bytes=256,candidate_table_probable_tail_bytes=2,
                supplemental_code=additional_info,supplemental_code_ranges=additional_ranges,
                typed_action_table_bytes=84,action_tables_assets_sha256=sha(action_tables.dump(action_tables_assets)),
                action_code=action_info,action_code_ranges=action_ranges,
                action_rng_existing_owner_bytes=38,action_rng_physical_emitters=1,
                typed_handler_table_bytes=52,handler_tables_assets_sha256=sha(handler_tables.dump(handler_tables_assets)),
                handler_code=handler_info,handler_code_ranges=handler_ranges,
                handler_reused_rng_bytes=38,handler_new_rng_emitters=0,
                handler49e_code=handler49e_info,handler49e_code_ranges=handler49e_ranges,
                handler49e_reused_code_bytes=340,handler49e_reused_dispatch_bytes=12,
                handler49e_new_table_bytes=0,handler49e_new_rng_emitters=0,
                handler9b0_code=handler9b0_info,handler9b0_code_ranges=handler9b0_ranges,
                handler9b0_reused_code_bytes=362,handler9b0_reused_table_bytes=64,
                handler9b0_new_table_bytes=0,handler9b0_new_rng_emitters=0,
                handlerc26_code=handlerc26_info,handlerc26_code_ranges=handlerc26_ranges,
                handlerc26_reused_code_bytes=58,handlerc26_reused_table_bytes=64,
                handlerc26_candidate_table_bytes_excluded=74,handlerc26_unknown_neighbour_bytes_excluded=8,
                handlerc26_new_table_bytes=0,handlerc26_new_rng_emitters=0,
                compiled_instruction_union=12921,compiled_code_union_bytes=47088,
                compiled_or_typed_bytes=74608+624+910+660+638+622+882+dialogue_bytes+font_bytes+extra_bytes,
                remaining_raw_slice_bytes=973968-624-910-660-638-622-882-dialogue_bytes-font_bytes-extra_bytes, code_ranges=legacy_ranges)
    bundle['m68k_layout.s'] = ('\n'.join(f'        .include "m68k_bank{bank:02x}.s"' for bank in range(16))+'\n').encode()
    bundle['manifest.json'] = dump(info)
    return bundle


def publish_content_addressed(bundle, output_root, inputs):
    names = {f'm68k_bank{bank:02x}.s' for bank in range(16)} | {'m68k_layout.s', 'manifest.json'}
    if set(bundle) != names or any(type(data) is not bytes for data in bundle.values()):
        raise ValueError('expected complete derived layout bundle')
    root = af.safe_path(output_root)
    af._separate(root, [af.safe_path(item, regular_input=True) for item in inputs])
    if not root.parent.is_dir(): raise ValueError('output root parent must exist')
    if not root.exists(): root.mkdir()
    if not root.is_dir(): raise ValueError('output root must be a directory')
    identity = sha(dump({name: sha(data) for name,data in sorted(bundle.items())}))
    target = af.safe_path(root / identity)
    if target.exists():
        if not target.is_dir() or {p.name for p in target.iterdir()} != set(bundle):
            raise ValueError('content-addressed output was modified')
        if any(read(target/name) != data for name,data in bundle.items()):
            raise ValueError('content-addressed output was modified')
        return target
    staging = Path(tempfile.mkdtemp(prefix='.m68k-build-', dir=root))
    state, produced = staging.stat(), {}
    try:
        for name, data in bundle.items():
            if re.fullmatch(r'm68k_(bank[0-9a-f]{2}|layout)\.s|manifest\.json', name) is None:
                raise ValueError('unexpected generated output name')
            with (staging/name).open('xb') as stream: stream.write(data)
            produced[name] = data
        af.safe_path(target)
        if target.exists(): raise ValueError('output appeared during publication')
        os.rename(staging, target)
    finally:
        af._cleanup_stage(staging, produced, state)
    return target


def verify_compiled(rom, object_data, image):
    from tools.m68k_build.elf_verify import verify_object
    records, info = inventory(rom)
    text = verify_object(object_data, records)
    if text != image: raise ValueError('objcopy image differs from ELF text')
    positions = {p for row in records for p in range(row['address'],row['address']+row['size'])}
    if any(value for index,value in enumerate(image) if index not in positions):
        raise ValueError('compiled bytes outside the allowed code extents')
    return info


def compose_expected_image(rom, code_image, audio_assets, dialogue_assets=None, font_assets=None, graphics_assets=None,
                           scaled_assets=None, world_assets=None, battle_graphics_assets=None, scenario_assets=None, portrait_assets=None,
                           terrain_assets=None, battlefield_assets=None, ui_assets=None, personnel_assets=None,
                           candidate_tables_assets=None, candidate_code_image=None,
                           action_tables_assets=None, action_code_image=None,
                           handler_tables_assets=None, handler_code_image=None, handler49e_code_image=None, handler9b0_code_image=None, handlerc26_code_image=None):
    """Independent field-codec composition; callers separately verify the ELF.

    Every codec receives the canonical ROM, never another codec's edited image.
    Only their disjoint typed spans and selected CPU spans are combined.
    """
    records, _ = inventory(rom)
    if type(code_image) is not bytes or len(code_image) != records[-1]['address']+records[-1]['size']:
        raise ValueError('compiled image extent changed')
    additional_records,_ = supplemental_selection(rom,records)
    if type(candidate_code_image) is not bytes or len(candidate_code_image) != 0x30876:
        raise ValueError('explicit supplemental compiled image required with fixed extent')
    action_records,_ = action_selection(rom,records,additional_records)
    if type(action_code_image) is not bytes or len(action_code_image) != 0x1B098:
        raise ValueError('explicit action compiled image required with fixed extent')
    handler_records,_=handler_selection(rom,records,additional_records,action_records)
    if type(handler_code_image) is not bytes or len(handler_code_image)!=0x1A9AA:
        raise ValueError('explicit handler compiled image required with fixed extent')
    handler49e_records,_=handler49e_selection(rom,records,additional_records,action_records,handler_records)
    if type(handler49e_code_image) is not bytes or len(handler49e_code_image)!=0x1A706:
        raise ValueError('explicit handler49e compiled image required with fixed extent')
    handler9b0_records,_=handler9b0_selection(rom,records,additional_records,action_records,handler_records,handler49e_records)
    if type(handler9b0_code_image) is not bytes or len(handler9b0_code_image)!=0x1AC1E:
        raise ValueError('explicit handler9b0 compiled image required with fixed extent')
    handlerc26_records,_=handlerc26_selection(rom,records,additional_records,action_records,handler_records,handler49e_records,handler9b0_records)
    if type(handlerc26_code_image) is not bytes or len(handlerc26_code_image)!=0x20930:
        raise ValueError('explicit handlerc26 compiled image required with fixed extent')
    if dialogue_assets is None:
        dialogue_assets = af.load_assets(read(dialogue.DEFAULT_ASSETS))
    if font_assets is None:
        font_assets = af.load_assets(read(font.DEFAULT_ASSETS))
    if graphics_assets is None: graphics_assets=af.load_assets(read(graphics.DEFAULT_ASSETS))
    if scaled_assets is None: scaled_assets=af.load_assets(read(scaled.DEFAULT_ASSETS))
    if world_assets is None: world_assets=af.load_assets(read(world.DEFAULT_ASSETS))
    if battle_graphics_assets is None: battle_graphics_assets=af.load_assets(read(battle_graphics.DEFAULT_ASSETS))
    if scenario_assets is None: scenario_assets=af.load_assets(read(scenario.DEFAULT_ASSETS))
    if portrait_assets is None: portrait_assets=af.load_assets(read(portrait.DEFAULT_ASSETS))
    if terrain_assets is None: terrain_assets=af.load_assets(read(terrain.DEFAULT_ASSETS))
    if battlefield_assets is None: battlefield_assets=af.load_assets(read(battlefield.DEFAULT_ASSETS))
    if ui_assets is None: ui_assets=af.load_assets(read(ui.DEFAULT_ASSETS))
    if personnel_assets is None: personnel_assets=af.load_assets(read(personnel.DEFAULT_ASSETS))
    ui_rows=ui.blocks(rom,ui_assets); personnel_rows=personnel.blocks(rom,personnel_assets)
    phase23_source_scope(ui_rows,'UI'); phase23_source_scope(personnel_rows,'personnel')
    if candidate_tables_assets is None: candidate_tables_assets=af.load_assets(read(candidate_tables.DEFAULT_ASSETS))
    candidate_rows=candidate_tables.blocks(rom,candidate_tables_assets)
    phase24_source_scope(candidate_rows)
    if action_tables_assets is None: action_tables_assets=af.load_assets(read(action_tables.DEFAULT_ASSETS))
    action_rows=action_tables.blocks(rom,action_tables_assets)
    phase25_source_scope(action_rows)
    if handler_tables_assets is None:handler_tables_assets=af.load_assets(read(handler_tables.DEFAULT_ASSETS))
    handler_rows=handler_tables.blocks(rom,handler_tables_assets)
    phase26_source_scope(handler_rows)
    expected, occupied = bytearray(rom), set()
    def claim(first,last,label):
        if type(first) is not int or type(last) is not int or not 0<=first<last<=len(rom):
            raise ValueError('invalid composed field extent')
        positions = set(range(first,last))
        if occupied & positions: raise ValueError(label+' overlaps another typed source')
        occupied.update(positions)
    sources=(
        ('audio',audio.rebuild(rom,audio_assets),[(r.start,r.end) for r in audio.blocks(rom,audio_assets)]),
        ('sprites',rom,[(0x29038,0x2A22E)]),  # Canonical sprite source is unchanged here.
        ('dialogue',dialogue.rebuild(rom,dialogue_assets),[(r['start'],r['end']) for r in dialogue.blocks(rom,dialogue_assets)]),
        ('font',font.rebuild(rom,font_assets),[(r['start'],r['end']) for r in font.blocks(rom,font_assets)]),
        ('graphics',graphics.rebuild(rom,graphics_assets),[(r['start'],r['end']) for r in graphics.blocks(rom,graphics_assets)]),
        ('scaled',scaled.rebuild(rom,scaled_assets),[(r['start'],r['end']) for r in scaled.blocks(rom,scaled_assets)]),
        ('world',world.rebuild(rom,world_assets),[(r['start'],r['end']) for r in world.blocks(rom,world_assets)]),
        ('battle_graphics',battle_graphics.rebuild(rom,battle_graphics_assets),[(r['start'],r['end']) for r in battle_graphics.blocks(rom,battle_graphics_assets)]),
        ('scenario',scenario.rebuild(rom,scenario_assets),[(r['start'],r['end']) for r in scenario.blocks(rom,scenario_assets)]),
        ('portrait',portrait.rebuild(rom,portrait_assets),[(r['start'],r['end']) for r in portrait.blocks(rom,portrait_assets)]),
        ('terrain',terrain.rebuild(rom,terrain_assets),[(r['start'],r['end']) for r in terrain.blocks(rom,terrain_assets)]),
        ('battlefield',battlefield.rebuild(rom,battlefield_assets),[(r['start'],r['end']) for r in battlefield.blocks(rom,battlefield_assets)]),
        ('ui',ui.rebuild(rom,ui_assets),[(r['start'],r['end']) for r in ui_rows]),
        ('personnel',personnel.rebuild(rom,personnel_assets),[(r['start'],r['end']) for r in personnel_rows]),
        ('candidate_tables',candidate_tables.rebuild(rom,candidate_tables_assets),[(r['start'],r['end']) for r in candidate_rows]),
        ('action_tables',action_tables.rebuild(rom,action_tables_assets),[(r['start'],r['end']) for r in action_rows]),
        ('handler_tables',handler_tables.rebuild(rom,handler_tables_assets),[(r['start'],r['end']) for r in handler_rows]))
    for label,image,ranges in sources:
        if type(image) is not bytes or len(image)!=len(rom): raise ValueError('codec image extent changed')
        for first,last in ranges:
            claim(first,last,label)
            expected[first:last]=image[first:last]
    for row in records:
        first, last = row['address'], row['address']+row['size']
        claim(first,last,'CPU')
        expected[first:last] = code_image[first:last]
    for row in additional_records:
        first,last=row['address'],row['address']+row['size']
        claim(first,last,'supplemental CPU')
        expected[first:last]=candidate_code_image[first:last]
    for row in action_records:
        first,last=row['address'],row['address']+row['size']
        claim(first,last,'action CPU')
        expected[first:last]=action_code_image[first:last]
    for row in handler_records:
        first,last=row['address'],row['address']+row['size']
        claim(first,last,'handler CPU')
        expected[first:last]=handler_code_image[first:last]
    for row in handler49e_records:
        first,last=row['address'],row['address']+row['size']
        claim(first,last,'handler49e CPU')
        expected[first:last]=handler49e_code_image[first:last]
    for row in handler9b0_records:
        first,last=row['address'],row['address']+row['size']
        claim(first,last,'handler9b0 CPU')
        expected[first:last]=handler9b0_code_image[first:last]
    for row in handlerc26_records:
        first,last=row['address'],row['address']+row['size']
        claim(first,last,'handlerc26 CPU')
        expected[first:last]=handlerc26_code_image[first:last]
    return bytes(expected)


def render_evidence(rom, source, assets, dialogue_assets=None, font_assets=None, graphics_assets=None,
                    scaled_assets=None, world_assets=None, battle_graphics_assets=None, scenario_assets=None, portrait_assets=None,
                    terrain_assets=None, battlefield_assets=None, ui_assets=None, personnel_assets=None,
                    candidate_tables_assets=None, candidate_code_source=None,
                    action_tables_assets=None, action_code_source=None,
                    handler_tables_assets=None, handler_code_source=None, handler49e_code_source=None, handler9b0_code_source=None, handlerc26_code_source=None):
    records, _ = inventory(rom)
    info = json.loads(render_layout(rom,source,assets,dialogue_assets,font_assets,graphics_assets,scaled_assets,world_assets,
                                    battle_graphics_assets,scenario_assets,portrait_assets,terrain_assets,battlefield_assets,ui_assets,personnel_assets,candidate_tables_assets,candidate_code_source,action_tables_assets,action_code_source,handler_tables_assets,handler_code_source,handler49e_code_source,handler9b0_code_source,handlerc26_code_source)['manifest.json'])
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=list(records[0]), lineterminator='\n')
    writer.writeheader(); writer.writerows(records)
    report = ('# Fixed-layout 68000 mnemonic build evidence\n\n'
        'Status: confirmed encoding/layout evidence, not whole-program semantics.\n\n'
        f"- Selected instructions: {info['selected_instructions']}; bytes: {info['selected_code_bytes']}.\n"
        f"- Primary-code role bytes: {info['primary_code_bytes']}; excluded role bytes: 84.\n"
        '- Exclusions: 10 bytes within 5 straddling instructions, plus 74 bytes without rows.\n'
        '- The 74 include 58 consumer-backed data bytes and 16 candidate helper bytes; see SCOUT.md.\n'
        f"- Typed main dialogue/names: {info['typed_dialogue_bytes']} bytes in banks08/09.\n"
        f"- Typed physical font rows: {info['typed_font_bytes']} bytes in bank08 (font16 end remains probable).\n"
        f"- Typed graphics: {info['typed_graphics_bytes']} bytes; 320 candidate-purpose transfer bytes remain explicitly qualified.\n"
        f"- Typed scaled bitmaps/directory: {info['typed_scaled_bitmap_bytes']} bytes; typed world resources: {info['typed_world_resource_bytes']} bytes.\n"
        f"- Typed battle-mode graphics: {info['typed_battle_graphics_bytes']} bytes, including16 map physical tail bytes NOT read at the row limit.\n"
        f"- Typed scenario source: {info['typed_scenario_bytes']} bytes, preserving full fields before lossy runtime transforms.\n"
        f"- Typed indexed-image source: {info['typed_portrait_bytes']} bytes; ALL allocations remain probable, not new confirmed ownership.\n"
        f"- Typed terrain maps/types: {info['typed_terrain_bytes']} bytes; 118 unselected type bytes remain probable. Full u16/u8 source fields are preserved, not clamped to natural domains.\n"
        f"- Typed battlefield coordinates/selection/geometry: {info['typed_battlefield_bytes']} bytes; full source WORDs and cross-record aliases retained. Forty editor slots are not a CPU-domain bound.\n"
        f"- Typed UI layouts/transfer/descriptors: {info['typed_ui_layout_bytes']} bytes; 156 caller-unproven candidate bytes remain qualified; full control words and physical aliases stay editable.\n"
        f"- Typed personnel candidate tables/directory: {info['typed_personnel_candidate_bytes']} bytes; the existing personnel_flow JSON is the sole editable authority, with fixed topology and no new ownership.\n"
        f"- Compiled CPU plus typed data: {info['compiled_or_typed_bytes']} bytes.\n"
        '- Supplemental probable source:184 instructions/624B; separate ledger/assembly, no new confirmed code ownership.\n'
        '- Candidate dispatch/numerical source fields:258B, including2B probable unconsumed tail seed; no full selector-domain claim.\n'
        '- Action probable source:241 instructions/910B in a third independent ledger; includes38B already-owned RNG with one physical emitter and a derived Z80 copy.\n'
        '- Action state/message/budget fields:84B in six distinct physical blocks; no natural selector-domain claim.\n'
        '- Handler01A818 probable source:196 instructions/660B in a fourth ledger; reused RNG stays in the third source, not emitted twice.\n'
        '- Handler coefficient/debit fields:52B/22 scalars in two separate blocks; editor extents are not CPU index bounds.\n'
        '- Handler01A49E probable source:183 instructions/638B in a fifth ledger;340B shared code keeps its existing physical sources.\n'
        '- Handler01A49E adds no table bytes:12B dispatch remains candidate_tables authority, and terrain/coefficient/debit sources are reused.\n'
        '- Handler01A9B0 probable source:182 instructions/622B in a sixth ledger;120/362B reused code and64B already editable tables retain sole old emitters.\n'
        '- Handler01A9B0 unknown6B/8B neighbours are excluded; no new table bytes or natural entry/domain proof.\n'
        '- Handler01AC26 probable source:264 instructions/882B in a seventh ledger;22/58B RNG/debit retains old sole sources.\n'
        '- Handler01AC26 excludes74B candidate tables,64B old tables and8B unknown neighbour; no new table/natural/domain proof.\n'
        f"- Explicit original bank slices: {info['remaining_raw_slice_bytes']} bytes.\n"
        '- New ownership: 0; newly complete indirect domains: 0.\n\n'
        '`instructions.csv` retains original decoder spellings as provenance, not the GNU dialect.\n'
        'The editable authority is `src/m68k/recovered_code.s`; its SHA-256 is in manifest.json.\n'
        'Canonical export is reproducible; the normal build never regenerates or overwrites it.\n'
        'The manifest is an inventory, not proof that GNU ran: execute the documented rebuild/tests.\n'
        'Only complete selected extents are spliced from the verified ELF text; .org padding is excluded.\n')
    return {'manifest.json':dump(info), 'instructions.csv':stream.getvalue().encode(), 'README.md':report.encode()}


def export_evidence(bundle, output, inputs):
    if set(bundle) != {'manifest.json','instructions.csv','README.md'} or any(type(x) is not bytes for x in bundle.values()):
        raise ValueError('expected complete evidence bundle')
    target = af.safe_path(output)
    af._separate(target,[af.safe_path(x,regular_input=True) for x in inputs])
    if target.exists() or not target.parent.is_dir(): raise ValueError('fresh evidence directory with existing parent required')
    staging = Path(tempfile.mkdtemp(prefix='.m68k-evidence-',dir=target.parent))
    state, produced = staging.stat(), {}
    try:
        for name,data in bundle.items():
            with (staging/name).open('xb') as stream: stream.write(data)
            produced[name] = data
        af.safe_path(target)
        if target.exists(): raise ValueError('evidence output appeared during publication')
        os.rename(staging,target)
    finally: af._cleanup_stage(staging,produced,state)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('prepare', 'verify-object', 'verify-image', 'export-source', 'evidence'))
    parser.add_argument('--rom', type=Path, default=af.DEFAULT_ROM)
    parser.add_argument('--source', type=Path, default=SOURCE)
    parser.add_argument('--audio-assets', type=Path, default=audio.DEFAULT_ASSETS)
    parser.add_argument('--dialogue-assets', type=Path, default=dialogue.DEFAULT_ASSETS)
    parser.add_argument('--font-assets', type=Path, default=font.DEFAULT_ASSETS)
    parser.add_argument('--graphics-assets', type=Path, default=graphics.DEFAULT_ASSETS)
    parser.add_argument('--scaled-assets', type=Path, default=scaled.DEFAULT_ASSETS)
    parser.add_argument('--world-assets', type=Path, default=world.DEFAULT_ASSETS)
    parser.add_argument('--battle-graphics-assets', type=Path, default=battle_graphics.DEFAULT_ASSETS)
    parser.add_argument('--scenario-assets', type=Path, default=scenario.DEFAULT_ASSETS)
    parser.add_argument('--portrait-assets', type=Path, default=portrait.DEFAULT_ASSETS)
    parser.add_argument('--terrain-assets', type=Path, default=terrain.DEFAULT_ASSETS)
    parser.add_argument('--battlefield-assets', type=Path, default=battlefield.DEFAULT_ASSETS)
    parser.add_argument('--ui-assets', type=Path, default=ui.DEFAULT_ASSETS)
    parser.add_argument('--personnel-assets', type=Path, default=personnel.DEFAULT_ASSETS)
    parser.add_argument('--candidate-tables-assets', type=Path, default=candidate_tables.DEFAULT_ASSETS)
    parser.add_argument('--candidate-code-source', type=Path, default=candidate_source.SOURCE)
    parser.add_argument('--candidate-object', type=Path)
    parser.add_argument('--candidate-image', type=Path)
    parser.add_argument('--action-tables-assets', type=Path, default=action_tables.DEFAULT_ASSETS)
    parser.add_argument('--action-code-source', type=Path, default=action_source.SOURCE)
    parser.add_argument('--action-object', type=Path)
    parser.add_argument('--action-image', type=Path)
    parser.add_argument('--handler-tables-assets', type=Path, default=handler_tables.DEFAULT_ASSETS)
    parser.add_argument('--handler-code-source', type=Path, default=handler_source.SOURCE)
    parser.add_argument('--handler-object', type=Path)
    parser.add_argument('--handler-image', type=Path)
    parser.add_argument('--handler49e-code-source', type=Path, default=handler49e_source.SOURCE)
    parser.add_argument('--handler49e-object', type=Path)
    parser.add_argument('--handler49e-image', type=Path)
    parser.add_argument('--handler9b0-code-source', type=Path, default=handler9b0_source.SOURCE)
    parser.add_argument('--handler9b0-object', type=Path)
    parser.add_argument('--handler9b0-image', type=Path)
    parser.add_argument('--handlerc26-code-source', type=Path, default=handlerc26_source.SOURCE)
    parser.add_argument('--handlerc26-object', type=Path)
    parser.add_argument('--handlerc26-image', type=Path)
    parser.add_argument('--output-root', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--object', type=Path)
    parser.add_argument('--image', type=Path)
    parser.add_argument('--rom-image', type=Path)
    args = parser.parse_args()
    rom = read(args.rom, af.ROM_SIZE); af.verify_rom(rom)
    if args.command == 'export-source':
        from tools.m68k_build.source import assembly
        target = af.safe_path(args.source)
        af._separate(target, [af.safe_path(args.rom, regular_input=True)])
        if target.exists() or not target.parent.is_dir(): raise ValueError('fresh source file with existing parent required')
        output = assembly(rom)
        validate_source(output, inventory(rom)[0])
        with target.open('xb') as stream: stream.write(output)
        print(target)
    elif args.command == 'evidence':
        if args.output is None: raise ValueError('--output required')
        bundle = render_evidence(rom,read(args.source),af.load_assets(read(args.audio_assets)),
                                 af.load_assets(read(args.dialogue_assets)),af.load_assets(read(args.font_assets)),af.load_assets(read(args.graphics_assets)),
                                 af.load_assets(read(args.scaled_assets)),af.load_assets(read(args.world_assets)),
                                 af.load_assets(read(args.battle_graphics_assets)),af.load_assets(read(args.scenario_assets)),af.load_assets(read(args.portrait_assets)),af.load_assets(read(args.terrain_assets)),af.load_assets(read(args.battlefield_assets)),af.load_assets(read(args.ui_assets)),af.load_assets(read(args.personnel_assets)),af.load_assets(read(args.candidate_tables_assets)),read(args.candidate_code_source),af.load_assets(read(args.action_tables_assets)),read(args.action_code_source),af.load_assets(read(args.handler_tables_assets)),read(args.handler_code_source),read(args.handler49e_code_source),read(args.handler9b0_code_source),read(args.handlerc26_code_source))
        print(export_evidence(bundle,args.output,[args.rom,args.source,args.audio_assets,args.dialogue_assets,args.font_assets,args.graphics_assets,args.scaled_assets,args.world_assets,args.battle_graphics_assets,args.scenario_assets,args.portrait_assets,args.terrain_assets,args.battlefield_assets,args.ui_assets,args.personnel_assets,args.candidate_tables_assets,args.candidate_code_source,candidate_source.LEDGER,args.action_tables_assets,args.action_code_source,action_source.LEDGER,args.handler_tables_assets,args.handler_code_source,handler_source.LEDGER,args.handler49e_code_source,handler49e_source.LEDGER,args.handler9b0_code_source,handler9b0_source.LEDGER,args.handlerc26_code_source,handlerc26_source.LEDGER,PRIMARY,INSTRUCTIONS]))
    elif args.command == 'prepare':
        if args.output_root is None: raise ValueError('--output-root required')
        bundle = render_layout(rom, read(args.source), af.load_assets(read(args.audio_assets)),
                               af.load_assets(read(args.dialogue_assets)),af.load_assets(read(args.font_assets)),af.load_assets(read(args.graphics_assets)),
                               af.load_assets(read(args.scaled_assets)),af.load_assets(read(args.world_assets)),
                               af.load_assets(read(args.battle_graphics_assets)),af.load_assets(read(args.scenario_assets)),af.load_assets(read(args.portrait_assets)),af.load_assets(read(args.terrain_assets)),af.load_assets(read(args.battlefield_assets)),af.load_assets(read(args.ui_assets)),af.load_assets(read(args.personnel_assets)),af.load_assets(read(args.candidate_tables_assets)),read(args.candidate_code_source),af.load_assets(read(args.action_tables_assets)),read(args.action_code_source),af.load_assets(read(args.handler_tables_assets)),read(args.handler_code_source),read(args.handler49e_code_source),read(args.handler9b0_code_source),read(args.handlerc26_code_source))
        print(publish_content_addressed(bundle, args.output_root, [args.rom,args.source,args.audio_assets,args.dialogue_assets,args.font_assets,args.graphics_assets,args.scaled_assets,args.world_assets,args.battle_graphics_assets,args.scenario_assets,args.portrait_assets,args.terrain_assets,args.battlefield_assets,args.ui_assets,args.personnel_assets,args.candidate_tables_assets,args.candidate_code_source,candidate_source.LEDGER,args.action_tables_assets,args.action_code_source,action_source.LEDGER,args.handler_tables_assets,args.handler_code_source,handler_source.LEDGER,args.handler49e_code_source,handler49e_source.LEDGER,args.handler9b0_code_source,handler9b0_source.LEDGER,args.handlerc26_code_source,handlerc26_source.LEDGER]))
    else:
        if args.object is None or args.image is None: raise ValueError('--object and --image required')
        object_data, image = read(args.object), read(args.image)
        info = verify_compiled(rom, object_data, image)
        if args.command == 'verify-image':
            if args.rom_image is None: raise ValueError('--rom-image required')
            if args.candidate_object is None or args.candidate_image is None:
                raise ValueError('--candidate-object and --candidate-image required')
            candidate_image = read(args.candidate_image)
            candidate_source.verify_image(rom,read(args.candidate_object),candidate_image)
            if args.action_object is None or args.action_image is None:
                raise ValueError('--action-object and --action-image required')
            action_image = read(args.action_image)
            action_source.verify_image(rom,read(args.action_object),action_image)
            if args.handler_object is None or args.handler_image is None:
                raise ValueError('--handler-object and --handler-image required')
            handler_image=read(args.handler_image)
            handler_source.verify_image(rom,read(args.handler_object),handler_image)
            if args.handler49e_object is None or args.handler49e_image is None:
                raise ValueError('--handler49e-object and --handler49e-image required')
            handler49e_image=read(args.handler49e_image)
            handler49e_source.verify_image(rom,read(args.handler49e_object),handler49e_image)
            if args.handler9b0_object is None or args.handler9b0_image is None:
                raise ValueError('--handler9b0-object and --handler9b0-image required')
            handler9b0_image=read(args.handler9b0_image)
            handler9b0_source.verify_image(rom,read(args.handler9b0_object),handler9b0_image)
            if args.handlerc26_object is None or args.handlerc26_image is None:
                raise ValueError('--handlerc26-object and --handlerc26-image required')
            handlerc26_image=read(args.handlerc26_image)
            handlerc26_source.verify_image(rom,read(args.handlerc26_object),handlerc26_image)
            expected = compose_expected_image(rom, image, af.load_assets(read(args.audio_assets)),
                                              af.load_assets(read(args.dialogue_assets)),af.load_assets(read(args.font_assets)),af.load_assets(read(args.graphics_assets)),
                                              af.load_assets(read(args.scaled_assets)),af.load_assets(read(args.world_assets)),
                                              af.load_assets(read(args.battle_graphics_assets)),af.load_assets(read(args.scenario_assets)),af.load_assets(read(args.portrait_assets)),af.load_assets(read(args.terrain_assets)),af.load_assets(read(args.battlefield_assets)),af.load_assets(read(args.ui_assets)),af.load_assets(read(args.personnel_assets)),af.load_assets(read(args.candidate_tables_assets)),candidate_image,af.load_assets(read(args.action_tables_assets)),action_image,af.load_assets(read(args.handler_tables_assets)),handler_image,handler49e_image,handler9b0_image,handlerc26_image)
            if read(args.rom_image, af.ROM_SIZE) != expected: raise ValueError('whole ROM differs from composed sources')
        print(json.dumps({'compiled_code_bytes': info['selected_code_bytes'], 'verified': True}))

if __name__ == '__main__': main()
