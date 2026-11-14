"""668 physical bytes consumed by original 0080F4 / 008112 LONG copy loops.

Seven BE32/WORD/WORD transfer records and seven exact source banks. The catalog
is an editor allocation, not a natural CPU selector limit or renderer claim.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from tools.vdp_word_streams import format as shared
from tools.scene_tile_resources.codec import colour, colour_word

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = shared.DEFAULT_ROM
FORMAL_ROOT = ROOT / 'analysis/palette_copy_fields/generated'
DEFAULT_FIELDS = FORMAL_ROOT / 'fields.json'
OUTPUT_ROOT = ROOT / 'build/palette_copy_fields'
FORMAT = 'candidate-seven-palette-copy-fields-v1'
EDITABLE_BYTES = 668
DIRECTORY_START, DIRECTORY_END = 0x812C, 0x8164
BANKS = ((0x8164, 0x81E4), (0x81E4, 0x8264), (0x8264, 0x82E4),
         (0x82E4, 0x8324), (0x8324, 0x8328), (0x8328, 0x8348), (0x8348, 0x83C8))
CONSUMER = bytes.fromhex('43fa0036e748d2c024593659d6fc00803e1926da51cffffc5278f31e4e75'
                         '43fa0018e748d2c0245936593e1926da51cffffc5278f31e4e75')
# Address, exact immediate selector instruction, original actual call bytes.
CALLERS = ((0x5FA, bytes.fromhex('303c0001'), bytes.fromhex('4eb9000080f4')),
           (0x3BAE, bytes.fromhex('7004'), bytes.fromhex('4eb900008112')),
           (0x947E, bytes.fromhex('7000'), bytes.fromhex('4eb900008112')),
           (0xA23A, bytes.fromhex('7001'), bytes.fromhex('4eb900008112')),
           (0xA646, bytes.fromhex('7005'), bytes.fromhex('4eb900008112')),
           (0x1776A, bytes.fromhex('303c0006'), bytes.fromhex('4eb900008112')))
sha, dump, load_fields = shared.sha, shared.dump, shared.load_json


def ident(start):
    return f'rom_{start:06X}_palette_source'


def metadata():
    return dict(format=FORMAT, canonical_source=dict(size=shared.ROM_SIZE, sha256=shared.ROM_SHA),
                confidence='confirmed_copy_encoding_candidate_palette_role',
                owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0)


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != shared.ROM_SIZE or sha(rom) != shared.ROM_SHA:
        raise ValueError('canonical ROM identity required')
    if rom[0x80F4:0x812C] != CONSUMER:
        raise ValueError('original seven-record consumers differ')
    for pc, selector, call in CALLERS:
        if rom[pc:pc + len(selector) + len(call)] != selector + call:
            raise ValueError(f'original selector/call differs at {pc:06X}')
    for p, (start, end) in zip(range(DIRECTORY_START, DIRECTORY_END, 8), BANKS):
        if int.from_bytes(rom[p:p + 4], 'big') != start or 4 * (int.from_bytes(rom[p + 6:p + 8], 'big') + 1) != end - start:
            raise ValueError('original directory source/count does not exactly cover physical bank')


def exact(value, count, label):
    if type(value) is not list or len(value) != count:
        raise ValueError(label + ': fixed allocation differs')
    return value


def extract(rom):
    verify_rom(rom)
    result = metadata()
    result['transfers'] = [dict(id=f'rom_{p:06X}_transfer', source=ident(int.from_bytes(rom[p:p + 4], 'big')),
        destination_WORD=int.from_bytes(rom[p + 4:p + 6], 'big'),
        LONG_count_minus_one=int.from_bytes(rom[p + 6:p + 8], 'big')) for p in range(DIRECTORY_START, DIRECTORY_END, 8)]
    result['palettes'] = [dict(id=ident(start), start=start, end=end,
        colours=[colour(int.from_bytes(rom[p:p + 2], 'big')) for p in range(start, end, 2)]) for start, end in BANKS]
    blocks(rom, result)
    return result


def blocks(rom, fields):
    verify_rom(rom)
    shared.keys(fields, set(metadata()) | {'transfers', 'palettes'}, 'package')
    for key, value in metadata().items():
        shared.same(fields[key], value, 'package.' + key)
    catalog = {ident(start): (start, end) for start, end in BANKS}
    data = bytearray()
    for row, p in zip(exact(fields['transfers'], 7, 'transfer records'), range(DIRECTORY_START, DIRECTORY_END, 8)):
        shared.keys(row, {'id', 'source', 'destination_WORD', 'LONG_count_minus_one'}, 'transfer')
        shared.same(row['id'], f'rom_{p:06X}_transfer', 'transfer id')
        if type(row['source']) is not str or row['source'] not in catalog:
            raise ValueError('transfer source must use existing physical bank')
        start, end = catalog[row['source']]
        dest = shared.uint(row['destination_WORD'], 65535, 'MOVEA.W destination')
        count = shared.uint(row['LONG_count_minus_one'], 65535, 'DBRA count WORD')
        if 4 * (count + 1) > end - start:
            raise ValueError('editor copy exceeds existing source; not a CPU count clamp')
        data.extend(start.to_bytes(4, 'big') + dest.to_bytes(2, 'big') + count.to_bytes(2, 'big'))
    rows = [dict(id='rom_00812C_transfer_directory', start=DIRECTORY_START, end=DIRECTORY_END,
                 data=bytes(data), role='candidate_BE32_MOVEAWORD_DBRALONG_records')]
    for row, (start, end) in zip(exact(fields['palettes'], 7, 'palette banks'), BANKS):
        shared.keys(row, {'id', 'start', 'end', 'colours'}, 'palette bank')
        for key, value in dict(id=ident(start), start=start, end=end).items():
            shared.same(row[key], value, 'palette.' + key)
        data = b''.join(colour_word(item).to_bytes(2, 'big') for item in exact(row['colours'], (end - start) // 2, 'colour WORDs'))
        rows.append(dict(id=ident(start), start=start, end=end, data=data, role='candidate_palette_staging_colour_WORDs'))
    if sum(len(row['data']) for row in rows) != EDITABLE_BYTES:
        raise ValueError('fixed668 physical field cost differs')
    return rows


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row['start']:row['end']] = row['data']
    return bytes(image)


def original_plan(rom, selector_WORD, *, upper_buffer=False):
    """Exact original descriptor read footprint, not execution or editor clamp."""
    verify_rom(rom)
    selector = shared.uint(selector_WORD, 65535, 'selector WORD')
    if type(upper_buffer) is not bool:
        raise ValueError('upper-buffer variant must be a bool')
    offset = selector << 3 & 65535
    if offset & 32768:
        offset -= 65536
    p = DIRECTORY_START + offset
    if p < 0 or p + 8 > len(rom):
        raise ValueError('descriptor leaves mapped ROM; not a seven-record clamp')
    source = int.from_bytes(rom[p:p + 4], 'big')
    dest = int.from_bytes(rom[p + 4:p + 6], 'big')
    count = int.from_bytes(rom[p + 6:p + 8], 'big') + 1
    dest = (dest - 65536 if dest & 32768 else dest) + (128 if upper_buffer else 0)
    return dict(descriptor_address=p, source_LONG=source, destination_LONG=dest & 0xFFFFFFFF,
                LONG_copies=count, source_bytes=4 * count, increment_WORD_address=0xFFFFF31E)


def render_bundle(rom):
    fields = extract(rom)
    image = rebuild(rom, load_fields(dump(fields)))
    if image != rom:
        raise ValueError('serialized whole-ROM roundtrip differs')
    report = dict(**metadata(), editable_bytes=668, directory_bytes=56, palette_source_bytes=612,
        physical_banks=7, complete_colour_WORDs=306, whole_ROM_exact=True, whole_ROM_sha256=sha(image),
        consumers=dict(start=0x80F4, end=0x812C, bytes=CONSUMER.hex(),
                       indexed_read='LSL.W3; ADDA.W signed lowWORD', destination='MOVEA.W signextends then optional ADDA.W80',
                       copy='DBRA LONG_count_minus_one+1 LONGs; increment F31E WORD'),
        callers=[dict(selector_PC=pc, selector_bytes=selector.hex(), call_PC=pc + len(selector), call_bytes=call.hex()) for pc, selector, call in CALLERS],
        immediate_caller_selectors=[0, 1, 4, 5, 6], natural_selector_domain='unknown', selectors2_and3_natural_usage='unknown',
        palette_reserved_bits_preserved=True, independent_CPU_comparison=False, complete_renderer_reimplemented=False,
        edited_gameplay_safety='unknown', physical_catalog_is_not_CPU_selector_clamp=True)
    members = {'fields.json': dump(fields), 'validation.json': dump(report)}
    members['manifest.json'] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value):
    path = shared.safe_path(value)
    if path != FORMAL_ROOT and (path == OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):
        raise ValueError('output must be fresh formal directory or beneath build/palette_copy_fields')
    if path.exists() or not path.parent.is_dir():
        raise ValueError('fresh output with existing parent required')
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('export', 'import', 'verify'))
    parser.add_argument('--rom', default=str(DEFAULT_ROM))
    parser.add_argument('--fields', default=str(DEFAULT_FIELDS))
    parser.add_argument('--output')
    args = parser.parse_args(argv)
    target = None
    if args.command != 'verify':
        if args.output is None:
            raise ValueError('fresh output required')
        target = fresh_output(args.output)
        if args.command == 'import' and target.suffix.lower() != '.bin':
            raise ValueError('fresh .bin required')
    elif args.output is not None:
        raise ValueError('verify does not write')
    rom = shared.read_bounded(args.rom, shared.ROM_SIZE)
    if args.command == 'export':
        members = render_bundle(rom)
        target.mkdir()
        for name, data in members.items():
            shared.put(target / name, data)
        result = dict(path=str(target), editable_bytes=EDITABLE_BYTES, members={name: sha(data) for name, data in members.items()})
    else:
        image = rebuild(rom, load_fields(shared.read_bounded(args.fields, shared.MAX_JSON)))
        if target is not None:
            shared.put(target, image)
        result = dict(path=None if target is None else str(target), sha256=sha(image), exact_canonical=image == rom)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
