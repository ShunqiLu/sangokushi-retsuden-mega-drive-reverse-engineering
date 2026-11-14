"""Fixed supplemental mnemonic source and independently sealed ROM provenance.

Normal builds read a pinned instruction ledger and editable assembly. Explicit
export alone invokes the decoder; it never replaces either legacy source/map.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import csv
import io
from pathlib import Path

from tools.graphics_build import graphics_build as gb

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'src/m68k/candidate_filter.s'
GENERATED = ROOT / 'analysis/candidate_source/generated'
LEDGER = GENERATED / 'instructions.csv'
ENHANCED = ROOT / 'analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv'
ENHANCED_SHA = reference_value(__name__, 'ENHANCED_SHA')
LEDGER_SHA = reference_value(__name__, 'LEDGER_SHA')
sha, dump = gb.sha, gb.dump

# Explicit root-reviewed selection, not inferred from a mutable consumer or
# from all future primary-code classifications. AF48's 34B remain legacy-only.
SPANS = (
    (0x000468, 0x00046C, 1, reference_value(__name__, 'SPANS')),
    (0x000CE4, 0x000CEC, 2, reference_value(__name__, 'SPANS_2')),
    (0x017A9E, 0x017BB2, 84, reference_value(__name__, 'SPANS_3')),
    (0x017BBE, 0x017C7A, 49, reference_value(__name__, 'SPANS_4')),
    (0x01A44E, 0x01A47A, 15, reference_value(__name__, 'SPANS_5')),
    (0x03080E, 0x030876, 33, reference_value(__name__, 'SPANS_6')),
)
FIELDS = ('address', 'size', 'bytes', 'original_mnemonic', 'original_operand',
          'discovery_confidence', 'decoder_origin', 'source_confidence', 'evidence_id')
EVIDENCE = 'phase24-fixed-conditional-source-v1'


def read(path):
    return gb.af._read(gb.af.safe_path(path, regular_input=True), 16*1024*1024)


def verify_rom(rom):
    gb.af.verify_rom(rom)
    for first, last, _, identity in SPANS:
        if sha(rom[first:last]) != identity:
            raise ValueError('supplemental original-code identity changed')


def legacy_map():
    raw = read(ENHANCED)
    if sha(raw) != ENHANCED_SHA:
        raise ValueError('legacy enhanced map changed')
    return {int(row['address']): row for row in csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))}


def csv_bytes(records):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator='\n')
    writer.writeheader(); writer.writerows(records)
    return stream.getvalue().encode()


def validate_records(rom, records):
    """Validate fixed coverage plus exact old spelling/confidence where present."""
    verify_rom(rom)
    if type(records) is not list or len(records) != 184:
        raise ValueError('supplemental instruction count changed')
    old = legacy_map(); positions = []; absent = 0
    for row in records:
        if type(row) is not dict or set(row) != set(FIELDS):
            raise ValueError('supplemental provenance fields changed')
        first, size = row['address'], row['size']
        if (type(first) is not int or type(size) is not int or first & 1 or
                size not in (2,4,6,8,10) or first < 0 or first+size > len(rom)):
            raise ValueError('invalid supplemental instruction extent')
        if row['bytes'] != rom[first:first+size].hex():
            raise ValueError('supplemental bytes do not match original ROM')
        if row['source_confidence'] != 'probable' or row['evidence_id'] != EVIDENCE:
            raise ValueError('supplemental source evidence changed')
        previous = old.get(first)
        if previous is not None:
            if (int(previous['size']), previous['bytes'], previous['mnemonic'], previous['operand'], previous['confidence']) != (
                    size, row['bytes'], row['original_mnemonic'], row['original_operand'], row['discovery_confidence']):
                raise ValueError('legacy decoder provenance changed')
            if row['decoder_origin'] != 'phase3-enhanced':
                raise ValueError('legacy provenance origin changed')
        else:
            absent += 1
            if row['decoder_origin'] != 'phase24-capstone-5.0.6' or row['discovery_confidence'] != 'probable':
                raise ValueError('new decoder provenance changed')
        if not any(a <= first and first+size <= b for a,b,_,_ in SPANS):
            raise ValueError('instruction outside supplemental allocation')
        positions.extend(range(first, first+size))
    expected = [p for first,last,_,_ in SPANS for p in range(first,last)]
    if positions != expected or absent != 29:
        raise ValueError('supplemental order/coverage/provenance changed')
    for first,last,count,_ in SPANS:
        if sum(first <= r['address'] < last for r in records) != count:
            raise ValueError('per-span instruction boundaries changed')
    return {'selected_instructions':184, 'selected_code_bytes':624,
        'legacy_decoder_rows':155, 'new_decoder_rows':29,
        'source_confidence':'probable', 'ownership_bytes_added':0,
        'complete_indirect_domains_added':0}


def inventory(rom):
    raw = read(LEDGER)
    if sha(raw) != LEDGER_SHA:
        raise ValueError('supplemental instruction ledger changed; independent re-audit required')
    records = list(csv.DictReader(io.StringIO(raw.decode('utf-8'))))
    for row in records:
        row['address'] = int(row['address']); row['size'] = int(row['size'])
    return records, validate_records(rom, records)


def decode(rom):
    """Explicit reproducible export, never a normal-build fallback."""
    from tools.code_analysis.m68k_code_map import load_capstone
    verify_rom(rom); old = legacy_map(); c = load_capstone()
    if c.__version__ != '5.0.6':
        raise ValueError('explicit source export requires pinned Capstone 5.0.6')
    decoder = c.Cs(c.CS_ARCH_M68K, c.CS_MODE_BIG_ENDIAN | c.CS_MODE_M68K_000)
    decoder.detail = True; records = []; instructions = []
    for first,last,count,_ in SPANS:
        decoded = list(decoder.disasm(rom[first:last], first))
        if len(decoded) != count or sum(i.size for i in decoded) != last-first:
            raise ValueError('independent decoder disagrees with fixed span')
        for instruction in decoded:
            previous = old.get(instruction.address)
            records.append(dict(zip(FIELDS, (instruction.address,instruction.size,instruction.bytes.hex(),
                instruction.mnemonic,instruction.op_str,previous['confidence'] if previous else 'probable',
                'phase3-enhanced' if previous else 'phase24-capstone-5.0.6','probable',EVIDENCE))))
            instructions.append(instruction)
    validate_records(rom,records)
    return records,instructions


def assembly(rom):
    from tools.m68k_build.source import format_instruction
    from tools.m68k_build.m68k_build import validate_source
    records,instructions = decode(rom)
    lines = ['| Probable conditional candidate-filter source; not new confirmed ownership.',
             '| Fixed independently reviewed extents; AF48 remains in recovered_code.s.',
             '.cpu 68000', '.section .text', '_start:']
    for instruction in instructions:
        lines.extend([f'.org 0x{instruction.address:X}',
            f'| {instruction.bytes.hex()} {instruction.op_str}'.rstrip(),
            f'm68k_{instruction.address:06x}:', '        '+format_instruction(instruction),
            f'm68k_{instruction.address:06x}_end:'])
    source = ('\n'.join(lines)+'\n').encode()
    validate_source(source,records)
    return source


def verify_image(rom, object_data, image):
    from tools.m68k_build.elf_verify import verify_object
    records,info = inventory(rom)
    if type(image) is not bytes or len(image) != 0x030876:
        raise ValueError('supplemental sparse image extent changed')
    if verify_object(object_data,records) != image:
        raise ValueError('supplemental objcopy image differs from ELF text')
    owned = {p for first,last,_,_ in SPANS for p in range(first,last)}
    if any(value for p,value in enumerate(image) if p not in owned):
        raise ValueError('supplemental padding contains bytes outside authorized extents')
    return info


def render_bundle(rom):
    records,_ = decode(rom); raw = csv_bytes(records); source = assembly(rom)
    info = validate_records(rom,records)
    info.update(format='g5510-candidate-source-v1', canonical_rom_sha256=gb.af.ROM_SHA256,
        enhanced_sha256=ENHANCED_SHA,instructions_sha256=sha(raw),
        canonical_source_sha256=sha(source), evidence_id=EVIDENCE,
        spans=[{'start':a,'end':b,'instructions':n,'sha256':h} for a,b,n,h in SPANS],
        source_authority='src/m68k/candidate_filter.s',
        excluded_legacy_dependency={'start':0xAF48,'end':0xAF6A,'bytes':34},
        confirmed_natural_entry=False,scope='conditional code identity; GNU results are separate evidence')
    return {'instructions.csv':raw,'manifest.json':dump(info),'README.md':(
        '# Supplemental candidate-filter mnemonic source\n\n'
        'probable: 184 instructions /624B in six fixed source extents.\n'
        'confirmed: original decoder provenance is retained for155 rows;29 new rows use pinned Capstone5.0.6.\n'
        'confirmed: legacy11671/42752B source and enhanced map are not replaced or relabelled.\n'
        'confirmed: real instructions use mnemonic source, never raw instruction directives.\n'
        'unknown: complete natural reachability, full input domains and whole-game behavior.\n'
        'confirmed: this generated inventory is not proof that GNU ran; verify object extents and whole-ROM builds separately.\n'
        'confirmed: ownership0 and complete-domain0 added by this package.\n').encode()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','export-source','verify-object'))
    parser.add_argument('--rom',type=Path,default=gb.DEFAULT_ROM)
    parser.add_argument('--output',type=Path); parser.add_argument('--source',type=Path,default=SOURCE)
    parser.add_argument('--object',type=Path);parser.add_argument('--image',type=Path)
    args=parser.parse_args(); rom=read(args.rom);verify_rom(rom)
    if args.command=='verify-object':
        if args.object is None or args.image is None:raise ValueError('--object and --image required')
        print(dump(verify_image(rom,read(args.object),read(args.image))).decode(),end='');return
    if args.command=='export':
        if args.output is None:raise ValueError('--output required')
        print(gb.publish(render_bundle(rom),args.output,[args.rom,ENHANCED]));return
    target=gb.af.safe_path(args.source)
    gb.af._separate(target,[gb.af.safe_path(args.rom,regular_input=True),ENHANCED])
    if target.exists() or not target.parent.is_dir():raise ValueError('fresh source file with existing parent required')
    output=assembly(rom)
    with target.open('xb') as stream:stream.write(output)
    print(target)


if __name__=='__main__':main()
