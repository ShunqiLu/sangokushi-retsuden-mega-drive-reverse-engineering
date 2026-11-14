"""Editable movement source fields; the intervening72 bytes remain unknown."""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from tools.direct_code import direct_code as d

f = d.f
ROOT = d.ROOT
FORMAL_ROOT = ROOT / 'analysis/troop_movement_source_fields/generated'
DEFAULT_FIELDS = FORMAL_ROOT / 'fields.json'
OUTPUT_ROOT = ROOT / 'build/troop_movement_source_fields'
FORMAT = 'g5510-movement-offset-and-list-source-fields-v1'
EDITABLE_BYTES = 24
GUARDS = (
    (0x1DBAC, 0x1DC00, reference_value(__name__, 'GUARDS')),
    (0x1DE36, 0x1DEAC, reference_value(__name__, 'GUARDS_2')),
    (0x1DAF6, 0x1DAFA, reference_value(__name__, 'GUARDS_3')),
    (0x1DC60, 0x1DC94, reference_value(__name__, 'GUARDS_4')),
)
sha, dump, load_fields = f.sha, f.dump, f.load_json


def metadata():
    return dict(format=FORMAT, canonical_source=dict(size=f.ROM_SIZE, sha256=f.ROM_SHA),
                confidence='confirmed_encoding_probable_movement_role', owner_bytes_added=0,
                natural_domains_added=0, complete_domains_added=0)


def offset_topology():
    return dict(id='rom_01DC00_movement_offset_WORD_pairs', start=0x1DC00, end=0x1DC10,
                entries=4, entry_bytes=4, WORD_order='big', read_PCs=[0x1DBF6, 0x1DBFA, 0x1DE9A, 0x1DEA2],
                editor_count_is_CPU_clamp=False)


def pointer_topology():
    return dict(id='rom_01DC58_list_address_LONGs', start=0x1DC58, end=0x1DC60,
                entries=2, entry_bytes=4, LONG_order='big', read_PC=0x1DC6E,
                target_bus_bits=24, editor_count_is_CPU_clamp=False)


def verify_rom(rom):
    if type(rom) is not bytes:
        raise ValueError('immutable canonical ROM bytes required')
    f.verify_rom(rom)
    for start, end, digest in GUARDS:
        if sha(rom[start:end]) != digest:
            raise ValueError('original complete producer/caller/reader slice differs')
    # Exact opcode windows, including true calls and original selector producers.
    for start, raw in (
        (0x1DBAC, '610000044e75'),
        (0x1DBF0, 'e54841fa000cda700000dc7000024e75'),
        (0x1DE94, 'e5494bfafd68da75100033850000dc751002338600026084'),
        (0x1DAF6, '61000168'),
        (0x1DC60, '3038f3a63238f6d602410002e3492c7b10e8'),
    ):
        if rom[start:start + len(raw) // 2] != bytes.fromhex(raw):
            raise ValueError('original caller/read/index instruction differs')
    if 0x1DBF4 + int.from_bytes(rom[0x1DBF4:0x1DBF6], 'big', signed=True) != 0x1DC00:
        raise ValueError('original A0 PC source differs')
    if 0x1DE98 + int.from_bytes(rom[0x1DE98:0x1DE9A], 'big', signed=True) != 0x1DC00:
        raise ValueError('original A5 PC source differs')
    if 0x1DC70 + int.from_bytes(rom[0x1DC71:0x1DC72], 'big', signed=True) != 0x1DC58:
        raise ValueError('original PC-indexed pointer source differs')


def extract(rom):
    verify_rom(rom)
    pairs = [dict(X_WORD=int.from_bytes(rom[p:p + 2], 'big'), Y_WORD=int.from_bytes(rom[p + 2:p + 4], 'big'))
             for p in range(0x1DC00, 0x1DC10, 4)]
    addresses = [int.from_bytes(rom[p:p + 4], 'big') for p in range(0x1DC58, 0x1DC60, 4)]
    return dict(**metadata(), offsets=dict(**offset_topology(), pairs=pairs),
                list_pointers=dict(**pointer_topology(), addresses_LONG=addresses))


def fixed(value, expected, mutable, label):
    f.keys(value, set(expected) | set(mutable), label)
    for key, item in expected.items():
        f.same(value[key], item, label + '.' + key)


def blocks(rom, fields):
    verify_rom(rom)
    fixed(fields, metadata(), {'offsets', 'list_pointers'}, 'movement package')
    offsets = fields['offsets']
    fixed(offsets, offset_topology(), {'pairs'}, 'offset table')
    pairs = offsets['pairs']
    if type(pairs) is not list or len(pairs) != 4:
        raise ValueError('four physical offset pairs required')
    data = bytearray()
    for pair in pairs:
        f.keys(pair, {'X_WORD', 'Y_WORD'}, 'offset pair')
        for name in ('X_WORD', 'Y_WORD'):
            data.extend(f.uint(pair[name], 65535, 'complete signed-interpretation WORD').to_bytes(2, 'big'))
    pointers = fields['list_pointers']
    fixed(pointers, pointer_topology(), {'addresses_LONG'}, 'pointer table')
    values = pointers['addresses_LONG']
    if type(values) is not list or len(values) != 2:
        raise ValueError('two physical source LONGs required')
    pointer_data = b''.join(f.uint(x, 0xFFFFFFFF, 'complete source LONG').to_bytes(4, 'big') for x in values)
    return [dict(id=offsets['id'], start=0x1DC00, end=0x1DC10, data=bytes(data), role='signed_WORD_movement_offset_pairs'),
            dict(id=pointers['id'], start=0x1DC58, end=0x1DC60, data=pointer_data, role='full_LONG_list_address_sources')]


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row['start']:row['end']] = row['data']
    return bytes(image)


def signed_WORD(value):
    return value - 65536 if value & 32768 else value


def direction_slot(first_WORD, second_WORD):
    """Original1DBB2/1DE3A WORD-sign/unsigned-compare selection, not a CPU."""
    f.uint(first_WORD, 65535, 'first source WORD')
    f.uint(second_WORD, 65535, 'second source WORD')
    if not first_WORD & 32768:
        if not second_WORD & 32768:
            return 1 if first_WORD < second_WORD else 2
        return 2 if first_WORD >= (-second_WORD & 65535) else 3
    if not second_WORD & 32768:
        return 0 if (-first_WORD & 65535) >= second_WORD else 1
    return 0 if first_WORD <= second_WORD else 3


def offset_read(rom, fields, index_WORD):
    """Low WORD index AT original ADD read; arbitrary offsets are not clamped."""
    f.uint(index_WORD, 65535, 'original shifted index WORD')
    image = rebuild(rom, fields)
    logical = (0x1DC00 + signed_WORD(index_WORD)) & 0xFFFFFFFF
    address = logical & 0xFFFFFF
    if address & 1:
        return dict(status='odd_WORD_address_boundary', logical_address=logical, address=address, reads=[], complete_CPU_entry=False)
    if address + 4 > len(image):
        return dict(status='ROM_read_boundary', logical_address=logical, address=address, reads=[], complete_CPU_entry=False)
    words = [int.from_bytes(image[p:p + 2], 'big') for p in (address, address + 2)]
    return dict(status='WORD_pair_read', logical_address=logical, address=address, reads=[dict(address=address + i * 2, size=2, value=x) for i, x in enumerate(words)],
                X_WORD=words[0], Y_WORD=words[1], signed_X=signed_WORD(words[0]), signed_Y=signed_WORD(words[1]),
                inside_editor_catalog=0x1DC00 <= address and address + 4 <= 0x1DC10, complete_CPU_entry=False)


def offset_adjustment(rom, fields, first_WORD, second_WORD, X_WORD, Y_WORD):
    f.uint(X_WORD, 65535, 'original D5 WORD')
    f.uint(Y_WORD, 65535, 'original D6 WORD')
    slot = direction_slot(first_WORD, second_WORD)
    view = offset_read(rom, fields, (slot << 2) & 65535)
    return dict(**view, selected_slot=slot, shifted_index_WORD=slot << 2,
                adjusted_X_WORD=(X_WORD + view['X_WORD']) & 65535,
                adjusted_Y_WORD=(Y_WORD + view['Y_WORD']) & 65535)


def list_pointer(rom, fields, F6D6_WORD):
    f.uint(F6D6_WORD, 65535, 'F6D6 low WORD at original read')
    image = rebuild(rom, fields)
    index = ((F6D6_WORD & 2) << 1) & 65535
    address = 0x1DC58 + signed_WORD(index)
    value = int.from_bytes(image[address:address + 4], 'big')
    return dict(original_read_PC=0x1DC6E, shifted_index_WORD=index, source_address=address, source_LONG=value,
                logical_target=value, bus_target=value & 0xFFFFFF,
                status='odd_WORD_target_boundary' if value & 1 else 'target_following_not_executed',
                target_followed=False, complete_CPU_entry=False)


def raw_guard(base):
    raw = d.raw_positions(base)
    positions = set(range(0x1DC00, 0x1DC10)) | set(range(0x1DC58, 0x1DC60))
    if not positions <= raw:
        raise ValueError('all24 bytes must remain sole raw source authority')
    return dict(guarded_raw_bytes=24, layout_remaining_raw=len(raw),
                excluded_middle_bytes=72, excluded_middle_raw_bytes=len(set(range(0x1DC10, 0x1DC58)) & raw))


def render_bundle(rom):
    fields = extract(rom)
    image = rebuild(rom, load_fields(dump(fields)))
    if image != rom:
        raise ValueError('serialized whole-ROM roundtrip differs')
    source_union = {p for slot in range(4) for p in range(0x1DC00 + 4 * slot, 0x1DC04 + 4 * slot)}
    source_union.update(p for flag in (0, 2) for p in range(list_pointer(rom, fields, flag)['source_address'], list_pointer(rom, fields, flag)['source_address'] + 4))
    if len(source_union) != 24:
        raise ValueError('original source union differs')
    report = dict(**metadata(), editable_bytes=24, full_WORD_fields=8, full_LONG_fields=2,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image), constructed_source_union_bytes=24,
        true_original_calls=[dict(pc=0x1DBAC, target=0x1DBB2, kind='BSR'), dict(pc=0x1DAF6, target=0x1DC60, kind='BSR')],
        source_LEAs=[dict(pc=0x1DBF2, target=0x1DC00), dict(pc=0x1DE96, target=0x1DC00)],
        guarded_original_code=[dict(start=a, end=z, sha256=h, physical_emit=False) for a, z, h in GUARDS],
        original_pointer_LONGs=fields['list_pointers']['addresses_LONG'],
        unknown_middle=dict(start=0x1DC10, end=0x1DC58, bytes=72, physical_emit=False,
            reason='Original instruction shape without an admitted entry witness; not classified as data or recovered code.'),
        natural_input_domains='unknown', independent_CPU_comparison=False, complete_CPU_entry=False,
        limitations=['Original selector producers choose four slots; this does not prove a global natural domain.',
            'Offset WORDs retain allbits with signed display and original modulo16 ADD results.',
            'Pointer LONGs retain all32bits; CPU uses24bit bus target; odd/all-ones edits are preview boundaries, not rejected target-domain guesses.',
            'Live RAM/list scans, SR/CCR, stacks and true function execution are not modeled.'])
    members = {'fields.json': dump(fields), 'validation.json': dump(report)}
    members['manifest.json'] = dump(dict(**metadata(), editable_bytes=24,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value):
    path = f.safe_path(value)
    if path != FORMAL_ROOT and (path == OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):
        raise ValueError('fresh formal directory or dedicated build/troop_movement_source_fields required')
    if path.exists() or not path.parent.is_dir():
        raise ValueError('fresh output with existing parent required')
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
        result = dict(path=str(target), editable_bytes=24, members={name: sha(data) for name, data in members.items()})
    else:
        image = rebuild(rom, load_fields(f.read_bounded(args.fields, f.MAX_JSON)))
        if target is not None:
            f.put(target, image)
        result = dict(path=None if target is None else str(target), exact_canonical=image == rom, sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
