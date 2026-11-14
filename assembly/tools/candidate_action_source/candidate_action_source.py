"""Pinned probable action-bridge instruction ledger and editable mnemonic source.

Only explicit export decodes the original ROM. Normal inventory/source/object
paths read the sealed additive ledger and the sole editable assembly source.
The shared RNG bytes remain an existing multi-consumer owner and are emitted
physically once; a Z80 payload copy is a derived view, not a second authority.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import csv
import io
from pathlib import Path

from tools.graphics_build import graphics_build as gb

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT/'src/m68k/candidate_action.s'
GENERATED = ROOT/'analysis/candidate_action_source/generated'
LEDGER = GENERATED/'instructions.csv'
ENHANCED = ROOT/'analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv'
ENHANCED_SHA = reference_value(__name__, 'ENHANCED_SHA')
LEDGER_SHA = reference_value(__name__, 'LEDGER_SHA')
sha, dump = gb.sha, gb.dump

# Independent fixed allocation, not inferred from any mutable execution model,
# primary region, or later global source selection. All bounds are half-open.
SPANS = (
    (0x0083D4, 0x0083FA, 15, reference_value(__name__, 'SPANS')),
    (0x019B2C, 0x019B42, 6, reference_value(__name__, 'SPANS_2')),
    (0x019C9E, 0x019E0E, 92, reference_value(__name__, 'SPANS_3')),
    (0x019E16, 0x019EC2, 38, reference_value(__name__, 'SPANS_4')),
    (0x019ECE, 0x019EF0, 7, reference_value(__name__, 'SPANS_5')),
    (0x01A47A, 0x01A492, 6, reference_value(__name__, 'SPANS_6')),
    (0x01AF80, 0x01AFA0, 10, reference_value(__name__, 'SPANS_7')),
    (0x01AFBC, 0x01B098, 67, reference_value(__name__, 'SPANS_8')),
)
EXCLUDED_TABLES = ((0x19B42,0x19B5E), (0x19C96,0x19C9E),
    (0x19E0E,0x19E16), (0x19EC2,0x19ECE), (0x1AFA0,0x1AFAC), (0x1AFAC,0x1AFBC))
EXISTING_ACTION_TABLE = (0x1A492,0x1A49E)
PRIOR_LEDGERS = (
    ('analysis/m68k_build/generated/instructions.csv',
     reference_value(__name__, 'PRIOR_LEDGERS'),11671,42752),
    ('analysis/candidate_source/generated/instructions.csv',
     reference_value(__name__, 'PRIOR_LEDGERS_2'),184,624),
)
FIELDS = ('address','size','bytes','original_mnemonic','original_operand',
          'discovery_confidence','decoder_origin','source_confidence','evidence_id')
EVIDENCE = 'phase25-fixed-action-source-v1'


def read(path):
    return gb.af._read(gb.af.safe_path(path, regular_input=True), 16*1024*1024)


def verify_rom(rom):
    gb.af.verify_rom(rom)
    for first,last,_,identity in SPANS:
        if sha(rom[first:last]) != identity:
            raise ValueError('action original-code identity changed')


def _rows(raw):
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))


def legacy_map():
    raw = read(ENHANCED)
    if sha(raw) != ENHANCED_SHA:
        raise ValueError('legacy enhanced map changed')
    return {int(row['address']):row for row in _rows(raw)}


def csv_bytes(records):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator='\n')
    writer.writeheader(); writer.writerows(records)
    return stream.getvalue().encode()


def excluded_coverage():
    """Pin prior ledgers without importing a mutable global build allocator."""
    positions = set()
    for name,identity,count,width in PRIOR_LEDGERS:
        raw = read(ROOT/name)
        if sha(raw) != identity:
            raise ValueError('prior compiled instruction ledger changed')
        rows = _rows(raw)
        covered = [p for row in rows for p in range(int(row['address']),int(row['address'])+int(row['size']))]
        if len(rows) != count or len(covered) != len(set(covered)) or len(covered) != width:
            raise ValueError('prior compiled instruction allocation changed')
        if positions.intersection(covered):
            raise ValueError('prior compiled instruction ledgers overlap')
        positions.update(covered)
    for first,last in (*EXCLUDED_TABLES,EXISTING_ACTION_TABLE):
        positions.update(range(first,last))
    return positions


def validate_records(rom, records):
    verify_rom(rom)
    if type(records) is not list or len(records) != 241:
        raise ValueError('action instruction count changed')
    previous = legacy_map(); positions = []
    for row in records:
        if type(row) is not dict or set(row) != set(FIELDS):
            raise ValueError('action provenance fields changed')
        first,size = row['address'],row['size']
        if (type(first) is not int or type(size) is not int or first & 1 or
            size not in (2,4,6,8,10) or first < 0 or first+size > len(rom)):
            raise ValueError('invalid action instruction extent')
        if row['bytes'] != rom[first:first+size].hex():
            raise ValueError('action bytes do not match original ROM')
        if row['source_confidence'] != 'probable' or row['evidence_id'] != EVIDENCE:
            raise ValueError('action source evidence changed')
        old = previous.get(first)
        if old is None or (int(old['size']),old['bytes'],old['mnemonic'],old['operand'],old['confidence']) != (
            size,row['bytes'],row['original_mnemonic'],row['original_operand'],row['discovery_confidence']):
            raise ValueError('legacy decoder provenance changed')
        if row['decoder_origin'] != 'phase3-enhanced':
            raise ValueError('legacy provenance origin changed')
        if not any(a <= first and first+size <= z for a,z,_,_ in SPANS):
            raise ValueError('instruction outside fixed action allocation')
        positions.extend(range(first,first+size))
    expected = [p for first,last,_,_ in SPANS for p in range(first,last)]
    if positions != expected or len(positions) != 910:
        raise ValueError('action instruction order or coverage changed')
    if set(positions) & excluded_coverage():
        raise ValueError('action instructions overlap previous source or data authority')
    for first,last,count,_ in SPANS:
        if sum(first <= row['address'] < last for row in records) != count:
            raise ValueError('per-span instruction boundaries changed')
    return {'selected_instructions':241,'selected_code_bytes':910,
        'legacy_decoder_rows':241,'new_decoder_rows':0,'source_confidence':'probable',
        'ownership_bytes_added':0,'existing_multi_consumer_bytes':38,
        'complete_indirect_domains_added':0}


def inventory(rom):
    raw = read(LEDGER)
    if sha(raw) != LEDGER_SHA:
        raise ValueError('action instruction ledger changed; independent re-audit required')
    records = _rows(raw)
    for row in records:
        row['address'] = int(row['address']); row['size'] = int(row['size'])
    return records, validate_records(rom,records)


def load_source(rom, source_path=None):
    """Normal editable-source path. No decoding, regeneration or ROM fallback."""
    from tools.m68k_build.m68k_build import validate_source
    records,info = inventory(rom)
    data = read(SOURCE if source_path is None else source_path)
    return data, records, {**info,**validate_source(data,records)}


def decode(rom):
    """Explicit canonical evidence/source export only."""
    from tools.code_analysis.m68k_code_map import load_capstone
    verify_rom(rom); previous = legacy_map(); capstone = load_capstone()
    if capstone.__version__ != '5.0.6':
        raise ValueError('explicit action export requires pinned Capstone 5.0.6')
    decoder = capstone.Cs(capstone.CS_ARCH_M68K,capstone.CS_MODE_BIG_ENDIAN|capstone.CS_MODE_M68K_000)
    decoder.detail = True; records,instructions = [],[]
    for first,last,count,_ in SPANS:
        decoded = list(decoder.disasm(rom[first:last],first))
        if len(decoded) != count or sum(item.size for item in decoded) != last-first:
            raise ValueError('independent decoder disagrees with fixed action span')
        for item in decoded:
            old = previous.get(item.address)
            if old is None:
                raise ValueError('action instruction lacks sealed old decoder provenance')
            records.append(dict(zip(FIELDS,(item.address,item.size,item.bytes.hex(),
                item.mnemonic,item.op_str,old['confidence'],'phase3-enhanced','probable',EVIDENCE))))
            instructions.append(item)
    validate_records(rom,records)
    return records,instructions


def assembly(rom):
    from tools.m68k_build.source import format_instruction
    from tools.m68k_build.m68k_build import validate_source
    records,instructions = decode(rom)
    lines = ['| Probable fixed action-bridge source; no new confirmed ownership.',
        '| RNG has one physical emitter; its Z80 payload copy is a derived view.',
        '.cpu 68000','.section .text','_start:']
    for item in instructions:
        lines.extend([f'.org 0x{item.address:X}',f'| {item.bytes.hex()} {item.op_str}'.rstrip(),
            f'm68k_{item.address:06x}:','        '+format_instruction(item),f'm68k_{item.address:06x}_end:'])
    result = ('\n'.join(lines)+'\n').encode()
    validate_source(result,records)
    return result


def verify_image(rom, object_data, image):
    from tools.m68k_build.elf_verify import verify_object
    records,info = inventory(rom)
    if type(image) is not bytes or len(image) != 0x1B098:
        raise ValueError('action sparse image extent changed')
    if verify_object(object_data,records) != image:
        raise ValueError('action objcopy image differs from ELF text')
    selected = {p for first,last,_,_ in SPANS for p in range(first,last)}
    if any(value for position,value in enumerate(image) if position not in selected):
        raise ValueError('action padding contains bytes outside authorized extents')
    return info


def alias_contract():
    return {'rom_start':0x83D4,'rom_end':0x83FA,'bytes':38,
        'existing_primary_region':[0x83C8,0x879C], 'classification':'multi_consumer',
        'roles':['m68k_code','z80_payload'],'primary_confidence':'confirmed',
        'secondary_copy':{'rom_start':0x799C,'rom_end':0x879C,'z80_destination':0x1000},
        'z80_alias_start':0x1A38,'z80_alias_end':0x1A5E,
        'z80_classification':'foreign_m68k_source_copy',
        'known_reachable_z80_instruction_overlap':False,
        'baseline_raw_interval':[0x8089,0x879C], 'baseline_typed_audio_overlap':0,
        'physical_emitter':'src/m68k/candidate_action.s',
        'derived_view':'Z80 payload bytes extracted from composed ROM, never a second editable copy',
        'edited_rom_gameplay_or_audio_safety_proven':False,'new_owner_bytes':0}


def render_bundle(rom):
    records,_ = decode(rom); raw = csv_bytes(records); source = assembly(rom)
    info = validate_records(rom,records)
    info.update(format='g5510-candidate-action-source-v1',canonical_rom_sha256=gb.af.ROM_SHA256,
        enhanced_sha256=ENHANCED_SHA,instructions_sha256=sha(raw),canonical_source_sha256=sha(source),
        evidence_id=EVIDENCE,source_authority='src/m68k/candidate_action.s',
        spans=[{'start':a,'end':z,'instructions':n,'sha256':h} for a,z,n,h in SPANS],
        excluded_prior_ledgers=[{'path':p,'sha256':h,'instructions':n,'bytes':b} for p,h,n,b in PRIOR_LEDGERS],
        excluded_new_table_ranges=[list(pair) for pair in EXCLUDED_TABLES],excluded_new_table_bytes=84,
        existing_action_table={'range':list(EXISTING_ACTION_TABLE),'bytes':12,
            'authority':'analysis/candidate_tables/generated/assets.json'},
        rng_physical_alias=alias_contract(),confirmed_natural_entry=False,
        scope='conditional source identity only; whole-ROM integration and runtime evidence are separate')
    return {'instructions.csv':raw,'manifest.json':dump(info),'README.md':(
        '# Fixed action-bridge mnemonic source\n\n'
        'probable: 241 instructions / 910B in eight fixed source extents.\n'
        'confirmed: all241 old enhanced-map spellings and original discovery grades are retained.\n'
        'confirmed: old11671/42752B and Phase24184/624B compiled sources do not overlap this allocation.\n'
        'confirmed: six new tables84B and the existing action table12B are excluded.\n'
        'confirmed: RNG38B retain their existing multi_consumer owner; one physical source emits them.\n'
        'confirmed: the Z80 payload alias is derived from composed ROM, never separately editable.\n'
        'unknown: natural state domains, whole action effects and edited-ROM gameplay/audio safety.\n'
        'confirmed: this inventory is not a GNU run or whole-ROM integration result.\n'
        'confirmed: this package adds zero owner bytes and zero complete indirect domains.\n').encode()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','export-source','verify-source','verify-object'))
    parser.add_argument('--rom',type=Path,default=gb.DEFAULT_ROM)
    parser.add_argument('--output',type=Path);parser.add_argument('--source',type=Path,default=SOURCE)
    parser.add_argument('--object',type=Path);parser.add_argument('--image',type=Path)
    args = parser.parse_args(); rom = read(args.rom); verify_rom(rom)
    if args.command == 'verify-object':
        if args.object is None or args.image is None:
            raise ValueError('--object and --image required')
        print(dump(verify_image(rom,read(args.object),read(args.image))).decode(),end=''); return
    if args.command == 'verify-source':
        _,_,info = load_source(rom,args.source)
        print(dump(info).decode(),end=''); return
    if args.command == 'export':
        if args.output is None:
            raise ValueError('--output required')
        print(gb.publish(render_bundle(rom),args.output,[args.rom,ENHANCED,SOURCE])); return
    target = gb.af.safe_path(args.source)
    gb.af._separate(target,[gb.af.safe_path(args.rom,regular_input=True),ENHANCED])
    if target.exists() or not target.parent.is_dir():
        raise ValueError('fresh source file with existing parent required')
    result = assembly(rom)
    with target.open('xb') as stream:
        stream.write(result)
    print(target)


if __name__ == '__main__':
    main()
