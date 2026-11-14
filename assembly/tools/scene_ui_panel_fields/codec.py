"""Two counted scene panels read by original 26BFA; not a CPU emulator."""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from tools.direct_code import direct_code as d
from tools.ui_layouts import ui_layouts as grammar

f = d.f
ROOT = d.ROOT
FORMAL_ROOT = ROOT / 'analysis/scene_ui_panel_fields/generated'
DEFAULT_FIELDS = FORMAL_ROOT / 'fields.json'
OUTPUT_ROOT = ROOT / 'build/scene_ui_panel_fields'
FORMAT = 'g5510-scene-counted-panel-source-fields-v1'
EDITABLE_BYTES = 160
# start, exact consumer end, columns, rows, original LEA and JSR pairs
STREAMS = (
    (0x313E0, 0x31430, 6, 10, ((0x313BC, 0x313CE),)),
    (0x3171A, 0x3176A, 8, 7, ((0x316F2, 0x31704), (0x31964, 0x31976))),
)
GUARDS = (
    (0x313BC, 0x313E0, reference_value(__name__, 'GUARDS')),
    (0x316F2, 0x3171A, reference_value(__name__, 'GUARDS_2')),
    (0x31964, 0x31990, reference_value(__name__, 'GUARDS_3')),
    (0x26BFA, 0x26C8E, reference_value(__name__, 'GUARDS_4')),
)
sha, dump, load_fields = f.sha, f.dump, f.load_json


def metadata():
    return dict(format=FORMAT, canonical_source=dict(size=f.ROM_SIZE, sha256=f.ROM_SHA),
                confidence='confirmed_counted_source_probable_scene_panel_role',
                owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0)


def verify_rom(rom):
    if type(rom) is not bytes:
        raise ValueError('immutable canonical ROM required')
    f.verify_rom(rom)
    for start, end, digest in GUARDS:
        if sha(rom[start:end]) != digest:
            raise ValueError('original panel consumer/renderer differs')
    for start, end, width, rows, readers in STREAMS:
        for pc, call in readers:
            target = pc + 2 + int.from_bytes(rom[pc + 2:pc + 4], 'big', signed=True)
            registers = (bytes.fromhex('203c') + (0xC0000000 | width).to_bytes(4, 'big')
                         + bytes.fromhex('323c') + rows.to_bytes(2, 'big'))
            if rom[pc:pc + 2] != bytes.fromhex('41fa') or target != start:
                raise ValueError('original signed PC-relative source LEA differs')
            if rom[pc + 4:pc + 14] != registers or rom[call:call + 6] != bytes.fromhex('4eb900026bfa'):
                raise ValueError('original fixed row/column setup and true JSR differ')


def parse_stream(image, spec):
    start, end, width, row_count, readers = spec
    view = grammar.walk_rows(image, start, width, row_count, command_budget=160)
    if view['status'] != 'complete' or view['end'] != end or view['output_words'] != width * row_count:
        raise ValueError('counted panel does not close at original source boundary')
    commands = []
    for command in view['commands']:
        op = dict(start=command['start'], end=command['end'], row=command['row'],
                  emitted_cells=command['output_words'])
        if command['kind'] == 'literal':
            op.update(kind='direct_WORD', WORD=command['word'])
        elif command['kind'] == 'word_command' and command['operation'] in ('repeat', 'increment_by_two'):
            op.update(kind=command['operation'], control_WORD=command['control_word'],
                      payload_WORD=command['operand_word'])
        else:
            raise ValueError('unsupported original panel command')
        commands.append(op)
    return dict(id=f'rom_{start:06X}_scene_panel', start=start, end=end, columns=width,
                rows=row_count, reader=0x26BFA, original_readers=[list(pair) for pair in readers],
                commands=commands)


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(), streams=[parse_stream(rom, spec) for spec in STREAMS])


def exact_list(value, count, label):
    if type(value) is not list or len(value) != count:
        raise ValueError(label + ': fixed physical count differs')
    return value


def pinned(value, original, mutable, label):
    f.keys(value, set(original), label)
    for key, expected in original.items():
        if key not in mutable:
            f.same(value[key], expected, label + '.' + key)


def blocks(rom, fields):
    original = extract(rom)
    pinned(fields, original, {'streams'}, 'panel package')
    result = []
    for stream, old in zip(exact_list(fields['streams'], 2, 'streams'), original['streams']):
        pinned(stream, old, {'commands'}, 'stream')
        data = bytearray()
        for command, source in zip(exact_list(stream['commands'], len(old['commands']), 'commands'), old['commands']):
            mutable = 'WORD' if source['kind'] == 'direct_WORD' else 'payload_WORD'
            pinned(command, source, {mutable}, 'command')
            value = f.uint(command[mutable], 65535, 'full source WORD')
            if mutable == 'WORD':
                if value & 0x8000:
                    raise ValueError('direct WORD must preserve original sign branch')
            else:
                data.extend(command['control_WORD'].to_bytes(2, 'big'))
            data.extend(value.to_bytes(2, 'big'))
        if len(data) != old['end'] - old['start']:
            raise ValueError('fixed source cost differs')
        result.append(dict(id=old['id'], start=old['start'], end=old['end'], data=bytes(data),
                           role='original_counted_scene_panel_WORD_stream'))
    if sum(len(block['data']) for block in result) != EDITABLE_BYTES:
        raise ValueError('160-byte source union differs')
    return result


def rebuild(rom, fields):
    image = bytearray(rom)
    for block in blocks(rom, fields):
        image[block['start']:block['end']] = block['data']
    return bytes(image)


def source_views(rom, fields):
    image = rebuild(rom, fields)
    return [parse_stream(image, spec) for spec in STREAMS]


def schema(rom):
    def fixed(value):
        if type(value) is dict:
            return dict(type='object', required=list(value), additionalProperties=False,
                        properties={key: fixed(item) for key, item in value.items()})
        if type(value) is list:
            return dict(type='array', minItems=len(value), maxItems=len(value), items=False,
                        prefixItems=[fixed(item) for item in value])
        return dict(type={int: 'integer', str: 'string', bool: 'boolean'}[type(value)], const=value)
    result = fixed(extract(rom))
    result['$schema'] = 'https://json-schema.org/draft/2020-12/schema'
    for stream in result['properties']['streams']['prefixItems']:
        for command in stream['properties']['commands']['prefixItems']:
            for key, maximum in (('WORD', 32767), ('payload_WORD', 65535)):
                if key in command['properties']:
                    command['properties'][key] = dict(type='integer', minimum=0, maximum=maximum)
    return result


def render_bundle(rom):
    fields = extract(rom)
    image = rebuild(rom, load_fields(dump(fields)))
    if image != rom:
        raise ValueError('serialized entire-ROM roundtrip differs')
    report = dict(**metadata(), editable_bytes=160, source_WORDs=80,
                  emitted_cells=116, streams=2, original_calls=3,
                  whole_ROM_exact=True, whole_ROM_sha256=sha(image),
                  source_consumption=[dict(start=s['start'], end=s['end'], columns=s['columns'],
                                           rows=s['rows']) for s in source_views(rom, fields)],
                  guarded_code=[dict(start=a, end=z, sha256=h, physical_emit=False) for a, z, h in GUARDS],
                  complete_CPU_entry=False, independent_CPU_comparison=False,
                  natural_input_domains='unknown', limitations=[
                      'Only original literal/repeat/increment source commands, not queue/device/RAM/CCR execution.',
                      'Control topology is pinned; payload WORD retains all bits, direct WORD retains the positive branch.',
                      'No complete scene business function, natural caller-domain or gameplay-safety claim.'])
    members = {'fields.json': dump(fields), 'fields.schema.json': dump(schema(rom)),
               'validation.json': dump(report)}
    members['manifest.json'] = dump(dict(**metadata(), editable_bytes=160,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value):
    path = f.safe_path(value)
    if path != FORMAL_ROOT and (path == OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):
        raise ValueError('fresh formal directory or dedicated scene_ui_panel_fields build output required')
    if path.exists() or not path.parent.is_dir():
        raise ValueError('fresh output and existing parent required')
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('export', 'import', 'verify'))
    parser.add_argument('--rom', default=str(f.DEFAULT_ROM))
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
    rom = f.read_bounded(args.rom, f.ROM_SIZE)
    if args.command == 'export':
        members = render_bundle(rom)
        target.mkdir()
        for name, data in members.items():
            f.put(target / name, data)
        result = dict(path=str(target), editable_bytes=160, members={name: sha(data) for name, data in members.items()})
    else:
        image = rebuild(rom, load_fields(f.read_bounded(args.fields, f.MAX_JSON)))
        if target is not None:
            f.put(target, image)
        result = dict(exact_canonical=image == rom, sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
