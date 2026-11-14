"""462 structured bytes: original three-pointer directory and six tile rows.

Original03009A reads command WORDs, then tile WORDs until FFFF, with another
FFFF ending the stream. Tile output masks lowBYTE and ORs8300, not font text.
"""
import argparse
import json
from pathlib import Path
from tools.vdp_word_streams import format as shared

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = shared.DEFAULT_ROM
FORMAL_ROOT = ROOT / 'analysis/menu_tile_streams/generated'
DEFAULT_FIELDS = FORMAL_ROOT / 'fields.json'
OUTPUT_ROOT = ROOT / 'build/menu_tile_streams'
EDITABLE_BYTES = 462
FORMAT = 'candidate-menu-two-row-tile-streams-v1'
START, DIR_END, END = 0x300DE, 0x300EA, 0x302AC
STREAMS = ((0x300EA, 0x30180), (0x30180, 0x30216), (0x30216, 0x302AC))
CONSUMER = bytes.fromhex('41fa00424e71e5412070100030100c40ffff670000244ebab39470003a18428530180c40ffff67e4024000ff0040830033c000c0000060e833f900ff702600ff70324e75')
COMMAND = bytes.fromhex('48e7400002800000ffff220002403fff004040004840e049ec49808123c000c000044cdf00024e75')
sha, dump, load_fields = shared.sha, shared.dump, shared.load_json


def ident(start):
    return f'rom_{start:06X}_tile_stream'


def metadata():
    return dict(format=FORMAT, canonical_source=dict(size=shared.ROM_SIZE, sha256=shared.ROM_SHA),
                confidence='confirmed_read_encoding_candidate_menu_role', owner_bytes_added=0,
                natural_domains_added=0, complete_domains_added=0)


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != shared.ROM_SIZE or sha(rom) != shared.ROM_SHA:
        raise ValueError('canonical ROM identity required')
    if rom[0x3009A:START] != CONSUMER or rom[0x2B446:0x2B46E] != COMMAND:
        raise ValueError('original tile/VDP command consumers differ')


def exact(value, count, label):
    if type(value) is not list or len(value) != count:
        raise ValueError(label + ': fixed source allocation differs')
    return value


def extract(rom):
    verify_rom(rom)
    result = metadata()
    result['directory'] = [ident(int.from_bytes(rom[p:p + 4], 'big')) for p in range(START, DIR_END, 4)]
    result['streams'] = []
    for first, end in STREAMS:
        cursor, rows = first, []
        while True:
            if cursor + 2 > end:
                raise ValueError('original stream lacks complete end marker')
            command = int.from_bytes(rom[cursor:cursor + 2], 'big'); cursor += 2
            if command == 65535:
                break
            words = []
            while True:
                if cursor + 2 > end:
                    raise ValueError('original tile row lacks end marker')
                word = int.from_bytes(rom[cursor:cursor + 2], 'big'); cursor += 2
                if word == 65535:
                    break
                words.append(word)
            rows.append(dict(command_WORD=command, tile_WORDs=words, row_terminator_WORD=65535))
        if cursor != end or len(rows) != 2 or any(len(row['tile_WORDs']) != 35 for row in rows):
            raise ValueError('original two-row/35-tile allocation differs')
        result['streams'].append(dict(id=ident(first), start=first, end=end, rows=rows, stream_terminator_WORD=65535))
    blocks(rom, result)
    return result


def blocks(rom, fields):
    verify_rom(rom)
    shared.keys(fields, set(metadata()) | {'directory', 'streams'}, 'package')
    for key, value in metadata().items(): shared.same(fields[key], value, 'package.' + key)
    catalog = {ident(first): first for first, _ in STREAMS}
    raw = bytearray()
    for target in exact(fields['directory'], 3, 'directory'):
        if type(target) is not str or target not in catalog:
            raise ValueError('directory must alias complete existing stream')
        raw.extend(catalog[target].to_bytes(4, 'big'))
    result = [dict(id='rom_0300DE_directory', start=START, end=DIR_END, data=bytes(raw), role='candidate_BE32_tile_stream_directory')]
    for stream, (first, end) in zip(exact(fields['streams'], 3, 'streams'), STREAMS):
        shared.keys(stream, {'id', 'start', 'end', 'rows', 'stream_terminator_WORD'}, 'stream')
        for key, value in dict(id=ident(first), start=first, end=end, stream_terminator_WORD=65535).items():
            shared.same(stream[key], value, 'stream.' + key)
        raw = bytearray()
        for row in exact(stream['rows'], 2, 'rows'):
            shared.keys(row, {'command_WORD', 'tile_WORDs', 'row_terminator_WORD'}, 'row')
            command = shared.uint(row['command_WORD'], 65534, 'VDP source command WORD')
            shared.same(row['row_terminator_WORD'], 65535, 'row terminator')
            raw.extend(command.to_bytes(2, 'big'))
            for word in exact(row['tile_WORDs'], 35, 'tile WORDs'):
                raw.extend(shared.uint(word, 65534, 'tile WORD; FFFF reserved terminator').to_bytes(2, 'big'))
            raw.extend(b'\xff\xff')
        raw.extend(b'\xff\xff')
        if len(raw) != end - first: raise ValueError('source stream cost differs')
        result.append(dict(id=ident(first), start=first, end=end, data=bytes(raw), role='candidate_two_row_VDP_tile_WORD_stream'))
    if sum(len(row['data']) for row in result) != EDITABLE_BYTES:
        raise ValueError('fixed462 source cost differs')
    return result


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields): image[row['start']:row['end']] = row['data']
    return bytes(image)


def display_plan(rom, fields, selector_WORD):
    """Data-derived output for editor catalog, not a CPU or natural scene run."""
    blocks(rom, fields)
    selector = shared.uint(selector_WORD, 65535, 'selector WORD')
    if selector >= 3: raise ValueError('display helper uses editor catalog; original CPU index is unclamped')
    name = fields['directory'][selector]
    stream = next(item for item in fields['streams'] if item['id'] == name)
    return [dict(VDP_command_LONG=((row['command_WORD'] & 0x3FFF | 0x4000) << 16) | row['command_WORD'] >> 14,
                 tile_output_WORDs=[(word & 255) | 0x8300 for word in row['tile_WORDs']]) for row in stream['rows']]


def render_bundle(rom):
    fields = extract(rom); image = rebuild(rom, load_fields(dump(fields)))
    if image != rom: raise ValueError('serialized whole-ROM roundtrip differs')
    report = dict(**metadata(), editable_bytes=462, directory_bytes=12, stream_bytes=450,
        physical_streams=3, rows=6, tile_WORDs=210, whole_ROM_exact=True, whole_ROM_sha256=sha(image),
        original_consumer=dict(start=0x3009A, end=START, bytes=CONSUMER.hex()),
        original_VDP_command_helper=dict(start=0x2B446, end=0x2B46E, bytes=COMMAND.hex()),
        original_index='ASL.W2 followed by signed WORD index; no physical3-clamp',
        row_and_stream_terminator_WORD=65535, lowBYTE_FE_is_tile_not_terminator=True,
        ignored_tile_highBYTE_retained=True, Unicode_labels_added=0, independent_CPU_comparison=False,
        complete_renderer_reimplemented=False, edited_gameplay_safety='unknown')
    members = {'fields.json': dump(fields), 'validation.json': dump(report),
               'display_plan.json': dump([display_plan(rom, fields, i) for i in range(3)])}
    members['manifest.json'] = dump(dict(**metadata(), editable_bytes=462,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value):
    path = shared.safe_path(value)
    if path != FORMAL_ROOT and (path == OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):
        raise ValueError('output must be fresh formal directory or beneath build/menu_tile_streams')
    if path.exists() or not path.parent.is_dir(): raise ValueError('fresh output with existing parent required')
    return path


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=('export', 'import', 'verify')); p.add_argument('--rom', default=str(DEFAULT_ROM))
    p.add_argument('--fields', default=str(DEFAULT_FIELDS)); p.add_argument('--output'); args = p.parse_args(argv)
    target = None
    if args.command != 'verify':
        if args.output is None: raise ValueError('fresh output required')
        target = fresh_output(args.output)
        if args.command == 'import' and target.suffix.lower() != '.bin': raise ValueError('fresh .bin required')
    elif args.output is not None: raise ValueError('verify does not write')
    rom = shared.read_bounded(args.rom, shared.ROM_SIZE)
    if args.command == 'export':
        members = render_bundle(rom); target.mkdir()
        for name, data in members.items(): shared.put(target / name, data)
        result = dict(path=str(target), editable_bytes=462, members={name: sha(data) for name, data in members.items()})
    else:
        image = rebuild(rom, load_fields(shared.read_bounded(args.fields, shared.MAX_JSON)))
        if target is not None: shared.put(target, image)
        result = dict(path=None if target is None else str(target), exact_canonical=image == rom, sha256=sha(image))
    print(json.dumps(result, sort_keys=True)); return 0


if __name__ == '__main__': raise SystemExit(main())
