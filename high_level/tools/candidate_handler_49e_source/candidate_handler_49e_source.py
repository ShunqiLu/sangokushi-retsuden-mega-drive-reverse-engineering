"""Sealed 01A49E handler/helper allocation and sole editable mnemonic source.

Normal builds read the sealed ledger and edited source without decoding or a
canonical-ROM fallback. Explicit exports alone decode canonical bytes. The
existing RNG source is excluded, not emitted again by this package.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import csv
import io
from pathlib import Path

from tools.graphics_build import graphics_build as gb

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT/'src/m68k/candidate_handler_49e.s'
GENERATED = ROOT/'analysis/candidate_handler_49e_source/generated'
LEDGER = GENERATED/'instructions.csv'
ENHANCED = ROOT/'analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv'
ENHANCED_SHA = reference_value(__name__, 'ENHANCED_SHA')
LEDGER_SHA = reference_value(__name__, 'LEDGER_SHA')
sha, dump = gb.sha, gb.dump

# Independent fixed half-open extents. Never derive selection from the mutable
# model, graph, a supplied source or the global build allocation.
SPANS = (
    (0x01A438,0x01A44E,7,reference_value(__name__, 'SPANS')),
    (0x01A49E,0x01A706,176,reference_value(__name__, 'SPANS_2')),
)
EXCLUDED_TABLES = ((0x1A1DC,0x1A200),(0x1A492,0x1A49E),(0x1A808,0x1A818))
REUSED_CODE = ((0x1A44E,0x1A47A,15,44,'src/m68k/candidate_filter.s'),
               (0x1A706,0x1A808,83,258,'src/m68k/candidate_handler_818.s'),
               (0x83D4,0x83FA,15,38,'src/m68k/candidate_action.s'))
REUSED_RNG = (0x83D4,0x83FA)
PRIOR_LEDGERS = (
    ('analysis/m68k_build/generated/instructions.csv',
     reference_value(__name__, 'PRIOR_LEDGERS'),11671,42752),
    ('analysis/candidate_source/generated/instructions.csv',
     reference_value(__name__, 'PRIOR_LEDGERS_2'),184,624),
    ('analysis/candidate_action_source/generated/instructions.csv',
     reference_value(__name__, 'PRIOR_LEDGERS_3'),241,910),
    ('analysis/candidate_handler_source/generated/instructions.csv',
     reference_value(__name__, 'PRIOR_LEDGERS_4'),196,660),
)
# Baseline canonical identities, not a ban on editing those existing sources.
# Normal build paths validate their immutable ledgers without reading or resetting
# old editable mnemonics. Export metadata and audit tests retain these seals.
PRIOR_SOURCE_SEALS = (
    ('src/m68k/recovered_code.s',reference_value(__name__, 'PRIOR_SOURCE_SEALS')),
    ('src/m68k/candidate_filter.s',reference_value(__name__, 'PRIOR_SOURCE_SEALS_2')),
    ('src/m68k/candidate_action.s',reference_value(__name__, 'PRIOR_SOURCE_SEALS_3')),
    ('src/m68k/candidate_handler_818.s',reference_value(__name__, 'PRIOR_SOURCE_SEALS_4')),
)
PRIOR_SOURCES = tuple(path for path,_ in PRIOR_SOURCE_SEALS)
FIELDS = ('address','size','bytes','original_mnemonic','original_operand',
          'discovery_confidence','decoder_origin','source_confidence','evidence_id')
EVIDENCE = 'phase27-fixed-handler-49e-source-v1'


def read(path):
    return gb.af._read(gb.af.safe_path(path,regular_input=True),16*1024*1024)


def verify_rom(rom):
    gb.af.verify_rom(rom)
    for first,last,_,identity in SPANS:
        if sha(rom[first:last]) != identity:
            raise ValueError('handler original-code identity changed')


def _rows(raw):
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))


def legacy_map():
    raw = read(ENHANCED)
    if sha(raw) != ENHANCED_SHA:
        raise ValueError('legacy enhanced map changed')
    return {int(row['address']):row for row in _rows(raw)}


def csv_bytes(records):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream,fieldnames=FIELDS,lineterminator='\n')
    writer.writeheader(); writer.writerows(records)
    return stream.getvalue().encode()


def excluded_coverage():
    """Pin all four older ledgers without importing the global allocator."""
    positions = set(); old_records = []
    for name,identity,count,width in PRIOR_LEDGERS:
        raw = read(ROOT/name)
        if sha(raw) != identity:
            raise ValueError('prior compiled instruction ledger changed')
        rows = _rows(raw); old_records.extend(rows)
        covered = [p for row in rows for p in range(int(row['address']),int(row['address'])+int(row['size']))]
        if len(rows)!=count or len(covered)!=len(set(covered)) or len(covered)!=width:
            raise ValueError('prior compiled instruction allocation changed')
        if positions.intersection(covered):
            raise ValueError('prior compiled instruction ledgers overlap')
        positions.update(covered)
    for first,last,count,width,_ in REUSED_CODE:
        rows = [row for row in old_records if first<=int(row['address'])<last]
        if (not set(range(first,last))<=positions or len(rows)!=count or
            sum(int(row['size']) for row in rows)!=width or last-first!=width):
            raise ValueError('reused shared code is missing from prior physical sources')
    for first,last in (*EXCLUDED_TABLES,REUSED_RNG):
        positions.update(range(first,last))
    return positions


def validate_records(rom,records):
    verify_rom(rom)
    if type(records) is not list or len(records)!=183:
        raise ValueError('handler instruction count changed')
    previous = legacy_map(); positions = []
    for row in records:
        if type(row) is not dict or set(row)!=set(FIELDS):
            raise ValueError('handler provenance fields changed')
        first,size = row['address'],row['size']
        if (type(first) is not int or type(size) is not int or first & 1 or
            size not in (2,4,6,8,10) or first<0 or first+size>len(rom)):
            raise ValueError('invalid handler instruction extent')
        if row['bytes'] != rom[first:first+size].hex():
            raise ValueError('handler bytes do not match original ROM')
        if row['source_confidence']!='probable' or row['evidence_id']!=EVIDENCE:
            raise ValueError('handler source evidence changed')
        old = previous.get(first)
        if old is None or (int(old['size']),old['bytes'],old['mnemonic'],old['operand'],old['confidence']) != (
            size,row['bytes'],row['original_mnemonic'],row['original_operand'],row['discovery_confidence']):
            raise ValueError('legacy decoder provenance changed')
        if row['decoder_origin']!='phase3-enhanced':
            raise ValueError('legacy provenance origin changed')
        if not any(a<=first and first+size<=z for a,z,_,_ in SPANS):
            raise ValueError('instruction outside fixed handler allocation')
        positions.extend(range(first,first+size))
    expected = [p for first,last,_,_ in SPANS for p in range(first,last)]
    if positions!=expected or len(positions)!=638:
        raise ValueError('handler instruction order or coverage changed')
    if set(positions)&excluded_coverage():
        raise ValueError('handler instructions overlap prior source or table authority')
    for first,last,count,_ in SPANS:
        if sum(first<=row['address']<last for row in records)!=count:
            raise ValueError('per-span instruction boundaries changed')
    return {'selected_instructions':183,'selected_code_bytes':638,
        'legacy_decoder_rows':183,'new_decoder_rows':0,'source_confidence':'probable',
        'ownership_bytes_added':0,'complete_indirect_domains_added':0,
        'reused_RNG_bytes_not_emitted':38,'reused_shared_instructions_not_emitted':113,
        'reused_shared_code_bytes_not_emitted':340,'natural_runtime_observations_added':0}


def inventory(rom):
    raw = read(LEDGER)
    if sha(raw)!=LEDGER_SHA:
        raise ValueError('handler instruction ledger changed; independent re-audit required')
    records = _rows(raw)
    for row in records:
        row['address']=int(row['address']);row['size']=int(row['size'])
    return records,validate_records(rom,records)


def verify_source(rom,source):
    """Instruction-only syntax guard; actual widths require the compiled ELF."""
    from tools.m68k_build.m68k_build import validate_source
    records,info=inventory(rom)
    return {**info,**validate_source(source,records)}


def load_source(rom,source_path=None):
    """Read the single editable source, never decode or regenerate a fallback."""
    from tools.m68k_build.m68k_build import validate_source
    records,info=inventory(rom)
    data=read(SOURCE if source_path is None else source_path)
    return data,records,{**info,**validate_source(data,records)}


def decode(rom):
    """Explicit canonical evidence/source export only; pinned Capstone 5.0.6."""
    from tools.code_analysis.m68k_code_map import load_capstone
    verify_rom(rom); previous=legacy_map(); capstone=load_capstone()
    if capstone.__version__!='5.0.6':
        raise ValueError('explicit handler export requires pinned Capstone 5.0.6')
    decoder=capstone.Cs(capstone.CS_ARCH_M68K,capstone.CS_MODE_BIG_ENDIAN|capstone.CS_MODE_M68K_000)
    decoder.detail=True;records,instructions=[],[]
    for first,last,count,_ in SPANS:
        decoded=list(decoder.disasm(rom[first:last],first))
        if len(decoded)!=count or sum(item.size for item in decoded)!=last-first:
            raise ValueError('independent decoder disagrees with fixed handler span')
        for item in decoded:
            # Explicit raw length check prevents the known truncated absolute
            # JSR/JMP placeholder behavior from entering canonical evidence.
            if item.bytes[:2] in (b'\x4e\xb9',b'\x4e\xf9') and item.size!=6:
                raise ValueError('truncated absolute control-transfer instruction')
            old=previous.get(item.address)
            if old is None:
                raise ValueError('handler instruction lacks sealed old decoder provenance')
            records.append(dict(zip(FIELDS,(item.address,item.size,item.bytes.hex(),item.mnemonic,
                item.op_str,old['confidence'],'phase3-enhanced','probable',EVIDENCE))))
            instructions.append(item)
    validate_records(rom,records)
    return records,instructions


def assembly(rom):
    from tools.m68k_build.source import format_instruction
    from tools.m68k_build.m68k_build import validate_source
    records,instructions=decode(rom)
    lines=['| Probable fixed 01A49E handler/helpers; zero new confirmed ownership.',
           '| Shared terrain/helpers/RNG retain prior physical sources; data tables excluded.',
           '.cpu 68000','.section .text','_start:']
    for item in instructions:
        lines.extend([f'.org 0x{item.address:X}',f'| {item.bytes.hex()} {item.op_str}'.rstrip(),
            f'm68k_{item.address:06x}:','        '+format_instruction(item),f'm68k_{item.address:06x}_end:'])
    result=('\n'.join(lines)+'\n').encode()
    validate_source(result,records)
    return result


def verify_image(rom,object_data,image):
    """Verify actual labels/extents and zero gaps; preserve allowed edited bytes.

    The returned sparse image must never be imported wholesale into a ROM.
    Consumers may splice only inventory record extents, after this verification.
    """
    from tools.m68k_build.elf_verify import verify_object
    records,info=inventory(rom)
    if type(image) is not bytes or len(image)!=0x1A706:
        raise ValueError('handler sparse image extent changed')
    if verify_object(object_data,records)!=image:
        raise ValueError('handler objcopy image differs from ELF text')
    selected={p for first,last,_,_ in SPANS for p in range(first,last)}
    if any(value for position,value in enumerate(image) if position not in selected):
        raise ValueError('handler padding contains bytes outside authorized extents')
    return info


def render_bundle(rom):
    records,_=decode(rom);raw=csv_bytes(records);source=assembly(rom)
    if sha(raw)!=LEDGER_SHA:
        raise ValueError('exported instruction ledger disagrees with fixed seal')
    info=validate_records(rom,records)
    info.update(format='g5510-candidate-handler-49e-source-v1',canonical_rom_sha256=gb.af.ROM_SHA256,
        enhanced_sha256=ENHANCED_SHA,instructions_sha256=sha(raw),canonical_source_sha256=sha(source),
        evidence_id=EVIDENCE,source_authority='src/m68k/candidate_handler_49e.s',
        entry=0x1A49E,sparse_extent=0x1A706,
        spans=[{'start':a,'end':z,'instructions':n,'sha256':h} for a,z,n,h in SPANS],
        excluded_prior_ledgers=[{'path':p,'sha256':h,'instructions':n,'bytes':b} for p,h,n,b in PRIOR_LEDGERS],
        excluded_table_ranges=[list(pair) for pair in EXCLUDED_TABLES],excluded_table_bytes=64,
        existing_dispatch_authority='analysis/candidate_tables/generated/assets.json:action_dispatch_offsets',
        newly_emitted_table_bytes=0,
        baseline_prior_canonical_sources=[{'path':p,'sha256':h} for p,h in PRIOR_SOURCE_SEALS],
        reused_shared_code=[{'start':a,'end':z,'instructions':n,'bytes':b,'sole_existing_physical_source':p,
            'new_emitted_bytes':0} for a,z,n,b,p in REUSED_CODE],
        reused_rng={'range':list(REUSED_RNG),'bytes':38,'instructions':15,
            'sole_existing_physical_source':'src/m68k/candidate_action.s','new_emitted_bytes':0},
        confirmed_natural_entry=False,
        scope='conditional source identity only; global build and runtime evidence are separate')
    return {'instructions.csv':raw,'manifest.json':dump(info),'README.md':(
        '# Fixed 01A49E handler mnemonic source\n\n'
        'probable: 183 instructions / 638B in two fixed source extents.\n'
        'confirmed: all183 old enhanced-map spellings and heuristic discovery grades are retained.\n'
        'confirmed: old11671/42752B, Phase24184/624B, Phase25241/910B and Phase26196/660B ledgers are disjoint.\n'
        'confirmed: three nearby data tables64B are excluded from this instruction source.\n'
        'confirmed: dispatch1A492..1A49E12B already belongs to candidate_tables action_dispatch_offsets; zero new table bytes.\n'
        'confirmed: terrain15/44B, Cshared83/258B and RNG15/38B retain their prior physical sources.\n'
        'confirmed: this inventory is not a GNU run or whole-ROM integration result.\n'
        'confirmed: no new primary owner, complete indirect domain or natural runtime observation.\n'
        'unknown: natural entry/actor/bank/state domains and complete game action effects.\n').encode()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    for command in ('export','export-source','verify-source','verify-object','verify-image'):
        item=sub.add_parser(command)
        item.add_argument('--rom',type=Path,default=gb.DEFAULT_ROM)
        if command.startswith('export'):
            item.add_argument('--output',type=Path,required=True)
        elif command=='verify-source':
            item.add_argument('--source',type=Path,default=SOURCE)
        else:
            item.add_argument('--object',type=Path,required=True)
            item.add_argument('--image',type=Path,required=True)
    args=parser.parse_args();rom=read(args.rom);verify_rom(rom)
    if args.command in ('verify-object','verify-image'):
        print(dump(verify_image(rom,read(args.object),read(args.image))).decode(),end='');return
    if args.command=='verify-source':
        _,_,info=load_source(rom,args.source)
        print(dump(info).decode(),end='');return
    inputs=[args.rom,ENHANCED,*(ROOT/p for p in PRIOR_SOURCES),*(ROOT/p for p,_,_,_ in PRIOR_LEDGERS)]
    if args.command=='export':
        print(gb.publish(render_bundle(rom),args.output,[*inputs,SOURCE]));return
    target=gb.af.safe_path(args.output)
    gb.af._separate(target,[gb.af.safe_path(path,regular_input=True) for path in inputs])
    if target.exists() or not target.parent.is_dir():
        raise ValueError('fresh source file with existing parent required')
    result=assembly(rom)
    with target.open('xb') as stream:
        stream.write(result)
    print(target)


if __name__=='__main__':
    main()
