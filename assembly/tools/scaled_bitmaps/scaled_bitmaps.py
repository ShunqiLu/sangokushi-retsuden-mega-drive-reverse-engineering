"""Editable seven-source LSB-first bitmaps, 003A5A conversion and trace evidence."""
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
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools.audio_formats import audio_formats as af

DEFAULT_ROM = ROOT.parent / 'work/original_g5510.bin'
DEFAULT_ASSETS = ROOT / 'analysis/scaled_bitmaps/generated/assets.json'
DEFAULT_TRACE = ROOT / 'analysis/graphics_vdp/traces/boot_title/events.csv'
FORMAT = 'g5510-seven-scaled-lsb-bitmaps-v1'
DIRECTORY = 0x003A3E
DIRECTORY_END = 0x003A5A
BASE = 0x0D474A
END = 0x0D4ACA
SOURCES = tuple(BASE + i * 128 for i in range(7))
IDS = tuple(f'scaled_bitmap_{i}' for i in range(7))
TRACE_SHA256 = reference_value(__name__, 'TRACE_SHA256')
TRACE_GIT_LF_SHA256 = reference_value(__name__, 'TRACE_GIT_LF_SHA256')
ANCHORS = (
    (0x00393E, '31fc0003f32c3438f32c610000b6', 'initial parameter3 and call003A00'),
    (0x0041B6, '31fc0020f32c3438f32c6100f83e', 'explicit parameter32 and call003A00'),
    (0x00472E, '31fc0020f32c3438f32c6100f2c6', 'second explicit parameter32 caller'),
    (0x00480A, '31fc0020f32c3438f32c6100f1ea', 'third explicit parameter32 caller'),
    (0x003A04, '41fa00384e71363c03003a3c0006225845f8d100303c0020323c0020',
     'seven long pointers, tile0300, dimensions32x32, RAM D100 destination'),
    (0x003A20, '4eba00384e7145f8d1004eba00d64e710643001051cdffdc',
     'convert, upload512 bytes, tile increment16, seven-slot DBRA'),
    (0x003A5E, '76003601e14b86c202830000ffffe18b340078003a017c00264a',
     'zeroed D3, DIVU quotient floor((32<<8)/D2), shift8, row/pixel accumulators'),
    (0x003A78, '6100002848e7a0006100003e5145630647eb008060f2',
     'one source row; four groups of eight pixels separated by128 output bytes'),
    (0x003A8E, '4cdf0005d88353426704584a60d6', 'row accumulator and four-byte output-row stride'),
    (0x003AA2, '3e01e64f4844b840' '640acec4484449f170004e75',
     'source row guard, four source bytes per row, signed-word row index'),
    (0x003AB6, '287cffffffff48444e75', 'out-of-range row uses negative sentinel, no source read'),
    (0x003AC0, '200c6a047e0060362f05303c0007e98f4846bc4165044205601a',
     'negative row fills zero; bounded source x with long output nibble shift'),
    (0x003ADA, '3f003a06e64d1a345000300602400007010567040047000f',
     'byte index=x>>3, BTST bit=x&7: LSB-first within each byte'),
    (0x003AF2, '301f4846dc8351c8ffd42a1f26874e75', 'fixed-point column update and big-endian output long'),
    (0x003B06, 'ef8b02830003ff80e44b00434000484323c300c00004', 'tile-index-to-VDP command conversion'),
    (0x003B1C, '3e3c00ff33da00c0000051cffff84278d100', '256-word direct VDP upload and scratch terminator'),
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')


def verify_rom(rom):
    if type(rom) is not bytes:
        raise ValueError('canonical ROM must be bytes')
    af.verify_rom(rom)
    for address, encoded, _ in ANCHORS:
        raw = bytes.fromhex(encoded)
        if rom[address:address + len(raw)] != raw:
            raise ValueError(f'consumer bytes changed at {address:06X}')
    if tuple(int.from_bytes(rom[a:a + 4], 'big') for a in range(DIRECTORY, DIRECTORY_END, 4)) != SOURCES:
        raise ValueError('canonical seven-pointer directory changed')


def encode_rows(rows):
    if type(rows) is not list or len(rows) != 32:
        raise ValueError('exactly32 bitmap rows required')
    # Bit x is pixel x, including LSB-first bytes; each 32-pixel row is LE32.
    return b''.join(af._integer(row, 0xFFFFFFFF, 'row bitfield').to_bytes(4, 'little') for row in rows)


def decode_rows(raw):
    if type(raw) is not bytes or len(raw) != 128:
        raise ValueError('one fixed128-byte bitmap required')
    return [int.from_bytes(raw[i:i + 4], 'little') for i in range(0, 128, 4)]


def extract(rom):
    verify_rom(rom)
    return {'schema_version': 1, 'format': FORMAT,
            'directory': {'address': DIRECTORY, 'targets': list(IDS)},
            'bitmaps': [{'id': ident, 'start': start, 'rows': decode_rows(rom[start:start + 128])}
                        for ident, start in zip(IDS, SOURCES)]}


def blocks(rom, assets):
    verify_rom(rom)
    af._keys(assets, {'schema_version', 'format', 'directory', 'bitmaps'}, 'assets')
    af._same(assets['schema_version'], 1, 'schema_version')
    af._same(assets['format'], FORMAT, 'format')
    directory = assets['directory']
    af._keys(directory, {'address', 'targets'}, 'directory')
    af._same(directory['address'], DIRECTORY, 'directory address')
    targets = directory['targets']
    if type(targets) is not list or len(targets) != 7:
        raise ValueError('seven directory entries required')
    if any(type(target) is not str or target not in IDS for target in targets):
        raise ValueError('directory target must be an existing physical bitmap id')
    values = assets['bitmaps']
    if type(values) is not list or len(values) != 7:
        raise ValueError('seven physical bitmap definitions required')
    result = [{'id': 'scaled_bitmap_directory', 'start': DIRECTORY, 'end': DIRECTORY_END,
               'role': 'absolute_long_bitmap_directory',
               'data': b''.join(SOURCES[IDS.index(target)].to_bytes(4, 'big') for target in targets)}]
    for value, ident, start in zip(values, IDS, SOURCES):
        af._keys(value, {'id', 'start', 'rows'}, 'bitmap')
        af._same(value['id'], ident, 'bitmap id/order')
        af._same(value['start'], start, 'bitmap start')
        result.append({'id': ident, 'start': start, 'end': start + 128,
                       'role': 'bitmap_32x32_1bpp_lsb_rows', 'data': encode_rows(value['rows'])})
    return result


def rebuild(rom, assets):
    result = bytearray(rom)
    for block in blocks(rom, assets):
        result[block['start']:block['end']] = block['data']
    return bytes(result)


def convert(raw, scale_word):
    """003A5A at its reviewed fixed32x32 callers, not a global parameter proof.

    D2.w=0 traps at DIVU before conversion. All other unsigned word values
    produce a bounded512-byte buffer. Integer quotient truncation is retained.
    Output is four column strips, each32 rows of one BE32 eight-pixel word.
    """
    decode_rows(raw)
    scale = af._integer(scale_word, 0xFFFF, 'D2 word')
    if scale == 0:
        return {'status': 'divide_by_zero', 'scale_word': 0, 'step': None,
                'output': None, 'source_offsets': [], 'sample_read_count': 0}
    step = ((32 << 8) // scale) << 8
    output = bytearray(512)
    read_offsets = set()
    read_count = 0
    for y in range(32):
        source_y = (y * step) >> 16
        for x in range(32):
            source_x = (x * step) >> 16
            pixel = 0
            if source_y < 32 and source_x < 32:
                offset = 4 * source_y + (source_x >> 3)
                read_offsets.add(offset)
                read_count += 1
                pixel = (raw[offset] >> (source_x & 7)) & 1
            address = y * 4 + (x // 8) * 128 + (x % 8) // 2
            output[address] |= (15 * pixel) << (4 if x % 2 == 0 else 0)
    return {'status': 'rendered', 'scale_word': scale, 'step': step,
            'output': bytes(output), 'source_offsets': sorted(read_offsets),
            'sample_read_count': read_count}


def _check_runtime_group(rom, index, events):
    if len(events) != 256:
        raise ValueError('runtime upload must contain exactly256 word events')
    source = SOURCES[index]
    actual = bytearray()
    for lane, row in enumerate(events):
        expected = {'kind': 'vdp_write', 'pc': '003B24', 'address': 'C00000', 'mask': 'FFFF',
                    'a0': f'{DIRECTORY + 4 * (index + 1):08X}',
                    'a1': f'{source:08X}', 'a2': f'{0xFFFFD102 + 2 * lane:08X}',
                    'd0': '00000020', 'd1': '00000020', 'd2': '00000003',
                    'd3': f'{0x60000001 + index * 0x02000000:08X}', 'd7': f'{255 - lane:08X}'}
        if any(row.get(key) != value for key, value in expected.items()):
            raise ValueError('runtime register, source, ordering or lane mismatch')
        if not re.fullmatch('[0-9A-F]{4}', row.get('data', '')):
            raise ValueError('malformed runtime word')
        actual.extend(int(row['data'], 16).to_bytes(2, 'big'))
    converted = convert(rom[source:source + 128], 3)
    if bytes(actual) != converted['output']:
        raise ValueError('runtime upload differs from original fixed-point conversion')
    return {'id': IDS[index], 'source_start': source, 'source_end': source + 128,
            'scale_word': 3, 'step': converted['step'],
            'frames': sorted({int(row['frame']) for row in events}),
            'first_event': int(events[0]['event_id']), 'last_event': int(events[-1]['event_id']),
            'word_events': 256, 'output_bytes': 512, 'output_sha256': sha(bytes(actual)),
            'vram_start': 0x6000 + index * 512, 'vram_end': 0x6200 + index * 512,
            'model_source_offsets': converted['source_offsets'],
            'model_sample_read_count': converted['sample_read_count'],
            'source_read_events_captured': False, 'payload_equal': True}


def runtime_report(rom, trace):
    verify_rom(rom)
    if type(trace) is not bytes:
        raise ValueError('retained original boot trace identity changed')
    # The original capture used CRLF; repository *.csv text eol=lf yields the
    # other exact known byte identity in clean git archives. Reconstruct only
    # that sealed LF transport before validating the original capture identity.
    # This does NOT accept arbitrary newline/whitespace-normalized input.
    if sha(trace)==TRACE_GIT_LF_SHA256: trace=trace.replace(b'\n',b'\r\n')
    if sha(trace)!=TRACE_SHA256:
        raise ValueError('retained original boot trace identity changed')
    reader = csv.DictReader(io.StringIO(trace.decode('utf-8-sig'), newline=''))
    selected = [row for row in reader if row.get('kind') == 'vdp_write' and row.get('pc') == '003B24']
    if len(selected) != 1792:
        raise ValueError('seven exact runtime uploads required')
    groups = [_check_runtime_group(rom, i, selected[i * 256:(i + 1) * 256]) for i in range(7)]
    return {'schema_version': 1, 'trace_sha256': TRACE_SHA256,
            'trace_source': 'analysis/graphics_vdp/traces/boot_title/events.csv',
            'reader_instruction': 0x003B20, 'callback_pc': 0x003B24,
            'groups': groups, 'total_output_bytes': 3584, 'all_payloads_equal': True,
            'scope': 'retained cold-boot uploads at parameter3 only; modeled reads are not captured reads',
            'global_scale_domain_closed': False, 'all_source_bytes_runtime_read': False}


def asset_schema():
    def obj(fields):
        return {'type': 'object', 'additionalProperties': False, 'required': list(fields), 'properties': fields}
    definitions = [obj({'id': {'const': ident}, 'start': {'const': start},
                        'rows': {'type': 'array', 'minItems': 32, 'maxItems': 32,
                                 'items': {'type': 'integer', 'minimum': 0, 'maximum': 0xFFFFFFFF}}})
                   for ident, start in zip(IDS, SOURCES)]
    return {'$schema': 'https://json-schema.org/draft/2020-12/schema', **obj({
        'schema_version': {'const': 1}, 'format': {'const': FORMAT},
        'directory': obj({'address': {'const': DIRECTORY}, 'targets': {'type': 'array',
            'minItems': 7, 'maxItems': 7, 'items': {'enum': list(IDS)}}}),
        'bitmaps': {'type': 'array', 'minItems': 7, 'maxItems': 7, 'prefixItems': definitions, 'items': False}})}


MACROS = ('.macro scaled_bitmap_row row\n'
          '        .byte (\\row) & 255, ((\\row) >> 8) & 255, ((\\row) >> 16) & 255, ((\\row) >> 24) & 255\n'
          '.endm\n').encode('ascii')


def block_lines(block, origin, bank_base):
    """Validated typed fields for inclusion in a caller's fixed-bank layout."""
    af._keys(block, {'id', 'start', 'end', 'role', 'data'}, 'derived block')
    if type(origin) is not str or not re.fullmatch('[A-Za-z_][A-Za-z0-9_]*', origin):
        raise ValueError('invalid assembly origin')
    if type(bank_base) is not int or bank_base not in (0, 0xD0000):
        raise ValueError('unsupported bitmap bank')
    start, end, raw = block['start'], block['end'], block['data']
    if type(start) is not int or type(end) is not int or type(raw) is not bytes:
        raise ValueError('derived block types changed')
    if block['id'] == 'scaled_bitmap_directory':
        if (start, end, block['role'], bank_base, len(raw)) != (DIRECTORY, DIRECTORY_END, 'absolute_long_bitmap_directory', 0, 28):
            raise ValueError('directory block topology changed')
        values = [int.from_bytes(raw[i:i + 4], 'big') for i in range(0, 28, 4)]
        if any(value not in SOURCES for value in values):
            raise ValueError('derived directory target outside physical records')
        body = ['        .long ' + ', '.join(f'0x{value:06X}' for value in values)]
    else:
        if type(block['id']) is not str or block['id'] not in IDS:
            raise ValueError('unknown physical bitmap')
        expected = SOURCES[IDS.index(block['id'])]
        if (start, end, block['role'], bank_base) != (expected, expected + 128, 'bitmap_32x32_1bpp_lsb_rows', 0xD0000):
            raise ValueError('bitmap block topology changed')
        body = [f'        scaled_bitmap_row 0x{value:08X}' for value in decode_rows(raw)]
    return [f'        .if (. - {origin}) != 0x{start - bank_base:X}',
            '        .error "scaled bitmap offset changed"', '        .endif', f"{block['id']}:", *body]


def manifest(rom, runtime):
    values = blocks(rom, extract(rom))
    owners = [{'id': value['id'], 'start': value['start'], 'end': value['end'],
               'size': len(value['data']), 'role': value['role'], 'confidence': 'confirmed',
               'sha256': sha(value['data']), 'ownership': True,
               'evidence': 'original consumer bounds and typed canonical roundtrip; fullscale32 explicit callers'}
              for value in values]
    return {'schema_version': 1, 'format': FORMAT,
            'canonical_source': {'size': af.ROM_SIZE, 'sha256': af.ROM_SHA256},
            'canonical_asset_source_sha256': sha(dump(extract(rom))),
            'owners': owners, 'ownership_bytes_added': 924, 'directory_bytes': 28, 'bitmap_bytes': 896,
            'physical_records': 7, 'row_bitfields': 224, 'row_endianness': 'little',
            'pixel_bit_order': 'LSB_first_in_ascending_bytes', 'source_dimensions': [32, 32],
            'consumer_anchors': [{'address': a, 'bytes': raw, 'role': role, 'confidence': 'confirmed'}
                                 for a, raw, role in ANCHORS],
            'runtime_validation_sha256': sha(dump(runtime)), 'complete_indirect_domains_added': 0,
            'runtime_parameter_values': [3], 'explicit_fullscale_static_parameter': 32,
            'global_scale_domain_closed': False, 'business_role': 'unknown',
            'remaining_boundaries': [
                'No portrait/city/battle/name identity is assigned to these seven bitmaps.',
                'Only parameter3 is present in the retained upload capture; fullscale32 is static evidence.',
                'Model source-read offsets are not observed source-read events.',
                'The converter specializes the reviewed32x32 callers, not arbitrary dimensions.',
                'No natural global parameter lifetime or edited-gameplay correctness is claimed.',
                'Directory aliases are editable; physical bitmap definitions remain unique.']}


def render_bundle(rom, trace):
    assets = extract(rom)
    runtime = runtime_report(rom, trace)
    mapping = manifest(rom, runtime)
    values = blocks(rom, assets)
    directory = '\n'.join(block_lines(values[0], 'scaled_bank_00', 0)) + '\n'
    bitmaps = '\n'.join(line for value in values[1:] for line in block_lines(value, 'scaled_bank_0d', 0xD0000)) + '\n'
    report = ('# Seven scaled LSB-first bitmaps\n\n'
        'Confirmed typed fields and original-consumer bounds; business identities remain unknown.\n\n'
        '- Directory003A3E..003A5A:7 BE32 pointers,28 bytes.\n'
        '- Sources0D474A..0D4ACA:7 fixed32x32 1bpp records,896 bytes.\n'
        '- Sole editable authority: assets.json; each row is LE32, bit x means pixel x.\n'
        '- Fixed-point step: floor(8192 / D2.w) <<8; zero traps at DIVU.\n'
        '- Parameter3 samples coordinates0,10,21,31, not an ideal3x3 rescale.\n'
        '- Retained boot capture:7 uploads x512 bytes at parameter3, all byte-exact.\n'
        '- These modeled samples cover16 source bytes per bitmap, not the complete128 bytes.\n'
        '- Explicit static parameter32 callers consume all128 bytes in each fixed record.\n'
        '- No global parameter, natural fullscale use, portrait label or complete indirect domain claim.\n'
        '- Generated assembly requires macros.inc and caller-defined bank origins at ROM000000/0D0000.\n')
    return {'assets.json': dump(assets), 'assets.schema.json': dump(asset_schema()),
            'manifest.json': dump(mapping), 'runtime_validation.json': dump(runtime),
            'macros.inc': MACROS, 'directory.s': directory.encode(), 'bitmaps.s': bitmaps.encode(),
            'README.md': report.encode()}


def export_files(rom_path, trace_path, output):
    source = af.safe_path(rom_path, regular_input=True)
    trace = af.safe_path(trace_path, regular_input=True)
    target = af.safe_path(output)
    af._separate(target, [source, trace])
    if target.exists() or not target.parent.is_dir():
        raise ValueError('fresh output directory with existing parent required')
    bundle = render_bundle(af._read(source, af.ROM_SIZE), af._read(trace, 10 * 1024 * 1024))
    staging = Path(tempfile.mkdtemp(prefix='.scaled-bitmaps-', dir=target.parent))
    identity = staging.stat()
    produced = {}
    target_identity = None
    linked = {}
    published = False
    try:
        for name, data in bundle.items():
            with (staging / name).open('xb') as stream:
                stream.write(data)
            produced[name] = data
        af.safe_path(output)
        # Exclusive creation refuses even an empty concurrently created target;
        # POSIX rename could replace it. The prepared files are linked without
        # clobbering. The directory is visible during publication; only a
        # successful return promises the complete bundle.
        target.mkdir()
        target_identity = target.stat()
        for name, data in bundle.items():
            af.safe_path(target)
            current = target.stat()
            if (current.st_dev, current.st_ino) != (target_identity.st_dev, target_identity.st_ino):
                raise ValueError('output directory identity changed during publication')
            os.link(staging / name, target / name)
            linked[name] = data
        published = True
    finally:
        try:
            if target_identity is not None and not published:
                af._cleanup_stage(target, linked, target_identity)
        finally:
            af._cleanup_stage(staging, produced, identity)
    return {'output': str(target), 'files': sorted(bundle), 'ownership_bytes_added': 924}


def import_files(rom_path, asset_path, output):
    source = af.safe_path(rom_path, regular_input=True)
    asset = af.safe_path(asset_path, regular_input=True)
    target = af.safe_path(output)
    af._separate(target, [source, asset])
    if target.exists() or not target.parent.is_dir():
        raise ValueError('fresh output file with existing parent required')
    rom = af._read(source, af.ROM_SIZE)
    result = rebuild(rom, af.load_assets(af._read(asset, 1024 * 1024)))
    descriptor, name = tempfile.mkstemp(prefix='.scaled-bitmaps-', dir=target.parent)
    temporary = Path(name)
    identity = temporary.stat()
    complete = False
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(result)
            stream.flush()
            os.fsync(stream.fileno())
        complete = True
        af.safe_path(output)
        os.link(temporary, target)  # atomic no-clobber publication
    finally:
        if temporary.exists():
            af.safe_path(temporary, regular_input=True)
            current = temporary.stat()
            if complete and (current.st_dev, current.st_ino) == (identity.st_dev, identity.st_ino) and af._read(temporary, len(result)) == result:
                temporary.unlink()
            else:
                raise ValueError('incomplete or modified temporary image retained')
    return {'output': str(target), 'sha256': sha(result), 'canonical_exact': result == rom,
            'changed_bytes': sum(a != b for a, b in zip(rom, result))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('export', 'verify', 'import'))
    parser.add_argument('--rom', type=Path, default=DEFAULT_ROM)
    parser.add_argument('--assets', type=Path, default=DEFAULT_ASSETS)
    parser.add_argument('--trace', type=Path, default=DEFAULT_TRACE)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.command == 'export':
        if args.output is None:
            raise ValueError('--output required')
        result = export_files(args.rom, args.trace, args.output)
    elif args.command == 'import':
        if args.output is None:
            raise ValueError('--output required')
        result = import_files(args.rom, args.assets, args.output)
    else:
        rom = af._read(af.safe_path(args.rom, regular_input=True), af.ROM_SIZE)
        assets = af.load_assets(af._read(af.safe_path(args.assets, regular_input=True), 1024 * 1024))
        image = rebuild(rom, assets)
        result = {'sha256': sha(image), 'canonical_exact': image == rom, 'editable_bytes': 924}
    print(json.dumps(result))


if __name__ == '__main__':
    main()
