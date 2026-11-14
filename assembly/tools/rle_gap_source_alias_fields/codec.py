"""542 physical BYTE sources reached by original conditional RLE readers.

The normal tile allocations do not read these BYTEs. Supplied full RAM WORD
selectors in two genuine original prefixes do. This is a bounded source-read
projection, not a CPU, VDP, natural-selector or unused-padding classification.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared

ROOT = Path(__file__).resolve().parents[2]
ROM_SIZE = 1048576
ROM_SHA256 = reference_value(__name__, 'ROM_SHA256')
DEFAULT_ROM = ROOT.parent / 'work/original_g5510.bin'
OUTPUT_ROOT = ROOT / 'build/rle_gap_source_alias_fields'
FORMAL_ROOT = ROOT / 'analysis/rle_gap_source_alias_fields/generated'
DEFAULT_FIELDS = FORMAL_ROOT / 'fields.json'
FORMAT = 'g5510-conditional-word-RLE-physical-BYTE-alias-fields-v1'
EDITABLE_BYTES = 542
MAX_JSON = 4 * 1048576
MEMBERS = frozenset(('fields.json', 'fields.schema.json', 'validation.json', 'manifest.json'))
BASELINE_LAYOUT = reference_value(__name__, 'BASELINE_LAYOUT')
BASELINE_MANIFEST_SHA = reference_value(__name__, 'BASELINE_MANIFEST_SHA')
PINS = (
    (0x3DB78, 0x3DB90, reference_value(__name__, 'PINS')),
    (0x3DBDC, 0x3DBFC, reference_value(__name__, 'PINS_2')),
    (0x3AACE, 0x3AB94, reference_value(__name__, 'PINS_3')),
    (0x3B2B0, 0x3B2D8, reference_value(__name__, 'PINS_4')),
)
# Canonical witnesses are immutable evidence, never an alternate data source.
# BYTE, reader kind, supplied 80DA.W, pointer EA, source start/end, actual stop.
GAP_PROFILES = (
    (0x04A9A1, 'tile', 0x09E2, 0x0403DC, 0x04814E, 0x04A9B7, 'marker_zero'),
    (0x04C5AB, 'tile', 0x101C, 0x041CC4, 0x04812A, 0x051F11, 'marker_zero'),
    (0x04E08F, 'tile', 0x101C, 0x041CC4, 0x04812A, 0x051F11, 'marker_zero'),
    (0x04FBE3, 'tile', 0x101C, 0x041CC4, 0x04812A, 0x051F11, 'marker_zero'),
    (0x051BBB, 'map', 0x2365, 0x036A24, 0x0518E0, 0x051BC1, 'marker_zero'),
    (0x053421, 'map', 0x2211, 0x0364D4, 0x0530C0, 0x0537F5, 'row_limit'),
    (0x05415F, 'map', 0x2609, 0x0374B4, 0x053CD0, 0x0541B3, 'row_limit'),
    (0x0546DF, 'map', 0x2542, 0x037198, 0x054430, 0x054C31, 'row_limit'),
    (0x055FA5, 'tile', 0x3911, 0x03C098, 0x054020, 0x056525, 'marker_zero'),
    (0x057579, 'tile', 0x214B, 0x036180, 0x0558D0, 0x058BC1, 'marker_zero'),
    (0x058A5F, 'map', 0x22A0, 0x036710, 0x058430, 0x058C31, 'row_limit'),
    (0x059E03, 'map', 0x2137, 0x03616C, 0x059C00, 0x059F01, 'row_limit'),
    (0x05A2B3, 'map', 0x2712, 0x0378D8, 0x05A000, 0x05A33D, 'row_limit'),
    (0x05B99B, 'map', 0x2168, 0x036230, 0x05B830, 0x05B9B5, 'row_limit'),
    (0x05CA95, 'map', 0x261F, 0x03750C, 0x05C8E0, 0x05CD45, 'row_limit'),
    (0x05CDE1, 'tile', 0x26CD, 0x037788, 0x05B8F0, 0x05D611, 'marker_zero'),
)
# The already closed final tile witness also reads the 526-B unknown tail
# prefix. The adjacent 1,460 B have their own independent editing authority.
PREFIX_START, PREFIX_END = 0x5CE22, 0x5D030
PROFILES = GAP_PROFILES + tuple((a, 'tile', 0x26CD, 0x37788, 0x5B8F0, 0x5D611, 'marker_zero')
                              for a in range(PREFIX_START, PREFIX_END))
ADDRESSES = frozenset(row[0] for row in PROFILES)
READERS = {
    'tile': (0x3DC54, 0x3DB84, 0x3DB8C, 0x3AB52),
    'map': (0x3DC90, 0x3DBE8, 0x3DBF8, 0x3AACE),
}
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError('canonical original ROM bytes/size/SHA required')


def pointer_address(supplied_WORD, kind):
    """Original ASL.W2 wrapping, then sign extension in the indexed EA."""
    value = uint(supplied_WORD, 65535, 'complete supplied RAM WORD')
    if type(kind) is not str or kind not in READERS:
        raise ValueError('original tile or map reader required')
    shifted = (value << 2) & 65535
    return READERS[kind][0] + (shifted - 65536 if shifted & 32768 else shifted)


def source_view(image, supplied_WORD, kind, output_budget=65536):
    """Actual sequential BYTE grammar and native map-row/marker stops.

Edited pointers and source bytes are read from the supplied complete image.
Hardware writes, upper-level selector production and stack are not executed.
External budgets are explicit boundaries, not native source terminators.
"""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError('complete bytes image required; edited images allowed')
    uint(output_budget, 65536, 'external output WORD budget')
    if output_budget == 0:
        raise ValueError('positive external budget required')
    address = pointer_address(supplied_WORD, kind)
    table, pointer_pc, call_pc, entry = READERS[kind]
    result = dict(supplied_RAM_WORD=supplied_WORD, RAM_address=0xFFFF80DA,
        kind=kind, table=table, pointer_read_PC=pointer_pc,
        pointer_address=address, true_call_PC=call_pc, reader_entry=entry,
        natural_selection_domain_complete=False, independent_CPU_comparison=False)
    for start, end, expected in PINS:
        if sha(image[start:end]) != expected:
            return result | dict(status='changed_original_control_boundary', pin_start=start,
                                 editable_reads=[], source_BYTES=0, output_WORDs=0)
    target = int.from_bytes(image[address:address+4], 'big')
    result.update(pointer_LONG=target, pointer_BYTEs=list(image[address:address+4]))
    if not 0 <= (target & 0xFFFFFF) < ROM_SIZE:
        return result | dict(status='source_outside_ROM', editable_reads=[],
                             source_BYTES=0, output_WORDs=0)
    cursor, emitted, consumed = target, 0, 0
    reads, output = [], bytearray()
    map_entry = kind == 'map'

    def take(pc, role):
        nonlocal cursor, consumed
        bus = cursor & 0xFFFFFF
        if bus >= ROM_SIZE:
            raise IndexError('source outside supplied ROM')
        value = image[bus]
        if bus in ADDRESSES:
            reads.append(dict(address=bus, CPU_address=cursor, PC=pc, bytes=1, BYTE=value, role=role))
        cursor = (cursor + 1) & 0xFFFFFFFF
        consumed += 1
        return value

    status = 'external_output_budget'
    try:
        marker = take(0x3AAF0 if map_entry else 0x3AB5E, 'marker')
        while emitted < output_budget:
            first = take(0x3AAF2 if map_entry else 0x3AB60, 'first_command_BYTE')
            if first != marker:
                second = take(0x3AB02 if map_entry else 0x3AB68, 'literal_second_BYTE')
                count = 1
            else:
                count = take(0x3AB14 if map_entry else 0x3AB78, 'repeat_count_BYTE')
                if count == 0:
                    status = 'marker_zero'
                    break
                first = take(0x3AB1A if map_entry else 0x3AB7E, 'repeat_first_BYTE')
                second = take(0x3AB1E if map_entry else 0x3AB80, 'repeat_second_BYTE')
                count += 1  # Original DBRA starts at zero-extended count.
            word = first*256+second if map_entry else second*256+first
            for _ in range(count):
                output.extend(word.to_bytes(2, 'big'))
                emitted += 1
                if map_entry and emitted == 1024:
                    status = 'row_limit'
                    break
                if emitted == output_budget:
                    break
            if status == 'row_limit':
                break
    except IndexError:
        status = 'source_outside_ROM'
    return result | dict(status=status, source_start=target & 0xFFFFFF, source_end=cursor & 0xFFFFFF,
        CPU_source_start=target, CPU_source_end=cursor,
        source_BYTES=consumed, output_WORDs=emitted,
        decoded_WORDs_sha256=sha(bytes(output)), editable_reads=reads,
        source_sha256=sha(image[target & 0xFFFFFF:cursor & 0xFFFFFF]), hardware_writes_executed=False)


def target_view(image, address):
    uint(address, ROM_SIZE-1, 'physical BYTE address')
    profile = next((row for row in PROFILES if row[0] == address), None)
    if profile is None:
        raise ValueError('BYTE outside fixed unique source allocation')
    _, kind, supplied, _, _, _, _ = profile
    view = source_view(image, supplied, kind)
    read = next((row for row in view['editable_reads'] if row['address'] == address), None)
    return dict(address=address, target_reached=read is not None, actual_read=read,
                source_projection=view)


def metadata():
    return dict(format=FORMAT, confidence='confirmed_conditional_source_unknown_purpose',
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        padding_or_reserve_classification=False, natural_selector_domain='unknown',
        source_CPU_address_BITS=32, source_bus_address_BITS=24,
        original_business_or_graphical_purpose='unknown',
        physical_scope=dict(single_BYTE_gaps=16, tail_prefix_BYTES=526,
                            tail_start=PREFIX_START, tail_end=PREFIX_END),
        old_typed_source_and_pointer_neighbours_emitted_again=False,
        unique_physical_BYTE_authority=True, complete_CPU_or_VDP_algorithm=False,
        baseline=dict(layout=BASELINE_LAYOUT, manifest_sha256=BASELINE_MANIFEST_SHA,
                      resources=93, raw_BYTES=24594),
        pins=[dict(start=s, end=e, sha256=h) for s, e, h in PINS],
        profiles=[dict(address=a, kind=k, supplied_WORD=w, pointer_address=p,
                       canonical_source_start=s, canonical_source_end=e,
                       canonical_stop=t, constructed_selection_not_natural=True)
                  for a, k, w, p, s, e, t in PROFILES])


def extract(rom):
    verify_rom(rom)
    projections = {}
    for address, kind, word, pointer, start, end, stop in PROFILES:
        if (kind, word) not in projections:
            projections[kind, word] = source_view(rom, word, kind)
        actual = projections[kind, word]
        if not any(row['address'] == address for row in actual['editable_reads']) or (actual['pointer_address'], actual['source_start'],
                actual['source_end'], actual['status']) != (pointer, start, end, stop):
            raise ValueError('canonical complete original source witness differs')
    return metadata() | dict(source_BYTEs=[dict(address=a, BYTE=rom[a]) for a in sorted(ADDRESSES)])


def blocks(rom, fields):
    verify_rom(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {'source_BYTEs'}, 'conditional source fields')
    for key, expected in fixed.items():
        same(fields[key], expected, 'fields.'+key)
    result = []
    prefix = bytearray()
    for row, address in zip(exact_list(fields['source_BYTEs'], EDITABLE_BYTES, 'fixed BYTE count'), sorted(ADDRESSES)):
        keys(row, {'address', 'BYTE'}, 'physical source BYTE')
        same(row['address'], address, 'fixed physical address')
        value = uint(row['BYTE'], 255, 'full editable BYTE')
        if PREFIX_START <= address < PREFIX_END:
            prefix.append(value)
        else:
            result.append(dict(id=f'rom_{address:06X}_RLE_source_alias_BYTE', start=address,
                end=address+1, data=bytes([value]), role='conditional_original_WORD_RLE_source_BYTE_alias'))
    if len(prefix) != 526:
        raise ValueError('fixed prefix physical extent differs')
    result.append(dict(id='rom_05CE22_RLE_source_alias_BYTEs', start=PREFIX_START,
        end=PREFIX_END, data=bytes(prefix), role='conditional_original_WORD_RLE_source_BYTE_alias'))
    result.sort(key=lambda row: row['start'])
    return result


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row['start']:row['end']] = row['data']
    return bytes(image)


def schema():
    def obj(properties):
        return dict(type='object', properties=properties, required=list(properties), additionalProperties=False)
    def fixed(value):
        if type(value) is dict:
            return obj({k: fixed(v) for k, v in value.items()})
        if type(value) is list:
            return dict(type='array', prefixItems=[fixed(v) for v in value], items=False,
                        minItems=len(value), maxItems=len(value))
        return dict(type={str:'string', int:'integer', bool:'boolean'}[type(value)], const=value)
    rows = [obj(dict(address=fixed(a), BYTE=dict(type='integer', minimum=0, maximum=255)))
            for a in sorted(ADDRESSES)]
    return obj({**{k:fixed(v) for k,v in metadata().items()},
        'source_BYTEs':dict(type='array', prefixItems=rows, items=False,
                           minItems=EDITABLE_BYTES, maxItems=EDITABLE_BYTES)}) | {
        '$schema':'https://json-schema.org/draft/2020-12/schema'}


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError('serialized whole-ROM roundtrip differs')
    projections = {(kind, word):source_view(rom, word, kind)
                   for kind, word in sorted({(row[1], row[2]) for row in PROFILES})}
    report = metadata() | dict(editable_bytes=EDITABLE_BYTES, physical_blocks=17,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image),
        canonical_source_projections=list(projections.values()),
        canonical_witnesses=[dict(address=a, kind=kind, supplied_WORD=word,
            actual_read=next(r for r in projections[kind, word]['editable_reads'] if r['address'] == a))
            for a, kind, word, _, _, _, _ in PROFILES])
    members = {'fields.json':serialized, 'fields.schema.json':dump(schema()), 'validation.json':dump(report)}
    members['manifest.json'] = dump(metadata() | dict(editable_bytes=EDITABLE_BYTES, physical_blocks=17,
        members={name:dict(bytes=len(data), sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError('fresh output must stay in package build scope or exact formal bundle')
    if path.exists() or not path.parent.is_dir():
        raise ValueError('fresh output with existing parent required')
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('export', 'verify', 'import'))
    parser.add_argument('--rom', default=str(DEFAULT_ROM))
    parser.add_argument('--fields')
    parser.add_argument('--bundle')
    parser.add_argument('--output')
    args = parser.parse_args(argv)
    target = None
    if args.command == 'export':
        if args.output is None or args.fields is not None or args.bundle is not None:
            raise ValueError('export requires fresh output only')
        target = fresh_output(args.output, bundle=True)
    elif args.command == 'import':
        if args.output is None or args.bundle is not None:
            raise ValueError('import requires fields and fresh output')
        target = fresh_output(args.output)
        if target.suffix.lower() != '.bin':
            raise ValueError('fresh .bin output required')
    elif args.output is not None or (args.fields is not None and args.bundle is not None):
        raise ValueError('verify accepts fields or bundle and does not write')
    rom = read_bounded(args.rom, ROM_SIZE)
    if args.command == 'export':
        members = render_bundle(rom)
        target.mkdir()
        for name, data in members.items():
            put(target/name, data)
        result = dict(path=str(target), editable_bytes=EDITABLE_BYTES,
                      members={name:sha(data) for name,data in members.items()})
    elif args.command == 'verify' and args.bundle is not None:
        bundle = safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()} != MEMBERS:
            raise ValueError('exact four-member bundle required')
        for name, data in render_bundle(rom).items():
            if read_bounded(bundle/name, MAX_JSON) != data:
                raise ValueError('canonical bundle drift: '+name)
        result = dict(path=str(bundle), verified=True, editable_bytes=EDITABLE_BYTES,
                      whole_ROM_exact=True, whole_ROM_sha256=ROM_SHA256)
    else:
        image = rebuild(rom, load_fields(read_bounded(args.fields or DEFAULT_FIELDS, MAX_JSON)))
        if target is not None:
            put(target, image)
        result = dict(path=None if target is None else str(target), editable_bytes=EDITABLE_BYTES,
                      bytes=len(image), exact_canonical=image == rom, sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
