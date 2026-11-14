"""Four original PC-indexed RNG predicate tables, preserving every source bit."""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from tools.direct_code import direct_code as d

f = d.f
ROOT = d.ROOT
FORMAL_ROOT = ROOT / 'analysis/battle_probability_word_fields/generated'
DEFAULT_FIELDS = FORMAL_ROOT / 'fields.json'
OUTPUT_ROOT = ROOT / 'build/battle_probability_word_fields'
FORMAT = 'g5510-battle-predicate-source-WORD-fields-v1'
EDITABLE_BYTES = 300
# Physical order: EFD2=0 / EFD2!=0,2 / EFD2=2; first then second stage.
TABLES = (
    (0x2A78A, 0x2A7D2, 0x2A72C, ((0x2A734, 0x2A762), (0x2A746, 0x2A774), (0x2A74E, 0x2A77C))),
    (0x2A834, 0x2A87C, 0x2A7D8, ((0x2A7E0, 0x2A80E), (0x2A7F2, 0x2A820), (0x2A7FA, 0x2A828))),
    (0x2A8DA, 0x2A922, 0x2A87C, ((0x2A884, 0x2A8B2), (0x2A896, 0x2A8C4), (0x2A89E, 0x2A8CC))),
    (0x2A980, 0x2A9C8, 0x2A922, ((0x2A92A, 0x2A958), (0x2A93C, 0x2A96A), (0x2A944, 0x2A972))),
)
GUARDS = (
    (0x2A2D8, 0x2A2EC, reference_value(__name__, 'GUARDS')),
    (0x28F90, 0x28F9C, reference_value(__name__, 'GUARDS_2')),
    (0x2A70C, 0x2A78A, reference_value(__name__, 'GUARDS_3')),
    (0x2A7D2, 0x2A834, reference_value(__name__, 'GUARDS_4')),
    (0x2A87C, 0x2A8DA, reference_value(__name__, 'GUARDS_5')),
    (0x2A922, 0x2A980, reference_value(__name__, 'GUARDS_6')),
    (0x2AA00, 0x2AA14, reference_value(__name__, 'GUARDS_7')),
)
THRESHOLDS = (40, 60, 80, 100, 120, 65535)
THRESHOLD_START = 0x2A308
sha, dump, load_fields = f.sha, f.dump, f.load_json


def metadata():
    return dict(format=FORMAT, canonical_source=dict(size=f.ROM_SIZE, sha256=f.ROM_SHA),
                confidence='confirmed_WORD_encoding_probable_battle_predicate_role',
                owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0)


def topology(spec):
    start, end, branch, pcs = spec
    return dict(id=f'rom_{start:06X}_predicate_WORDs', start=start, end=end,
                original_branch_entry=branch, source_WORDs=36, WORD_order='big',
                editor_count_is_CPU_clamp=False)


def threshold_topology():
    return dict(id='rom_02A308_counter_threshold_WORDs', start=THRESHOLD_START,
                end=THRESHOLD_START + 12, source_WORDs=6, WORD_order='big',
                original_read_PC=0x28F96, editor_count_is_CPU_clamp=False,
                last_WORD_is_CPU_terminator=False)


def group_topology(spec, group):
    start = spec[0] + 24 * group
    return dict(group_index=group, flag_case=('EFD2_WORD_zero', 'EFD2_WORD_other', 'EFD2_WORD_two')[group],
                start=start, end=start + 24, read_PCs=list(spec[3][group]),
                stage_bases=[start, start + 12], stage_editor_WORDs=6)


def verify_rom(rom):
    if type(rom) is not bytes:
        raise ValueError('immutable canonical ROM bytes required')
    f.verify_rom(rom)
    for start, end, digest in GUARDS:
        if sha(rom[start:end]) != digest:
            raise ValueError('original producer/consumer/helper source differs')
    # These are original short-index extension words, D6.W without a scale.
    for spec in TABLES:
        for group in range(3):
            for stage, pc in enumerate(spec[3][group]):
                if rom[pc:pc + 3] != bytes.fromhex('343b60'):
                    raise ValueError('original MOVE.W PC-indexed D6.W differs')
                base = pc + 2 + int.from_bytes(rom[pc + 3:pc + 4], 'big', signed=True)
                if base != spec[0] + 24 * group + 12 * stage:
                    raise ValueError('original signed8 PC displacement differs')
    # Caller enters this real chain through BSR2A5F4; table regions are skipped.
    if rom[0x2A2E8:0x2A2EC] != bytes.fromhex('6100030a'):
        raise ValueError('original outer BSR source differs')
    for end, raw in ((0x2A7D2, '3e3c0042'), (0x2A87C, '4a78efd2'),
                     (0x2A922, '4a78efd2'), (0x2A9C8, '343b6018'), (0x2A314, '6000015a')):
        if rom[end:end + 4] != bytes.fromhex(raw):
            raise ValueError('following original instruction boundary differs')


def extract(rom):
    verify_rom(rom)
    result = metadata()
    result['threshold_source'] = dict(**threshold_topology(), WORDs=[
        int.from_bytes(rom[p:p + 2], 'big') for p in range(THRESHOLD_START, THRESHOLD_START + 12, 2)])
    tables = []
    for spec in TABLES:
        groups = []
        for group in range(3):
            fixed = group_topology(spec, group)
            values = [[int.from_bytes(rom[base + 2 * i:base + 2 * i + 2], 'big')
                       for i in range(6)] for base in fixed['stage_bases']]
            groups.append(dict(**fixed, stage_WORDs=values))
        tables.append(dict(**topology(spec), groups=groups))
    result['tables'] = tables
    return result


def exact_list(value, count, label):
    if type(value) is not list or len(value) != count:
        raise ValueError(label + ': fixed physical count differs')
    return value


def fixed_fields(value, fixed, mutable, label):
    f.keys(value, set(fixed) | set(mutable), label)
    for key, expected in fixed.items():
        f.same(value[key], expected, label + '.' + key)


def blocks(rom, fields):
    verify_rom(rom)
    fixed_fields(fields, metadata(), {'tables', 'threshold_source'}, 'predicate package')
    threshold = fields['threshold_source']
    fixed_fields(threshold, threshold_topology(), {'WORDs'}, 'threshold source')
    threshold_data = b''.join(f.uint(x, 65535, 'complete threshold WORD').to_bytes(2, 'big')
                              for x in exact_list(threshold['WORDs'], 6, 'threshold WORDs'))
    rows = [dict(id=threshold['id'], start=THRESHOLD_START, end=THRESHOLD_START + 12,
                 data=threshold_data, role='original_unsigned_counter_BE16_threshold_fields')]
    for table, spec in zip(exact_list(fields['tables'], 4, 'tables'), TABLES):
        fixed_fields(table, topology(spec), {'groups'}, 'table')
        data = bytearray()
        for group, item in enumerate(exact_list(table['groups'], 3, 'groups')):
            fixed_fields(item, group_topology(spec, group), {'stage_WORDs'}, 'group')
            for stage in exact_list(item['stage_WORDs'], 2, 'stages'):
                for value in exact_list(stage, 6, 'source WORDs'):
                    data.extend(f.uint(value, 65535, 'complete source WORD').to_bytes(2, 'big'))
        if len(data) != 72:
            raise ValueError('fixed physical WORD table cost differs')
        rows.append(dict(id=table['id'], start=spec[0], end=spec[1], data=bytes(data),
                         role='original_PCindexed_RNG_predicate_BE16_fields'))
    if sum(len(row['data']) for row in rows) != EDITABLE_BYTES:
        raise ValueError('300-byte allocation differs')
    return rows


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row['start']:row['end']] = row['data']
    return bytes(image)


def signed_WORD(value):
    return value - 65536 if value & 32768 else value


def counter_index(rom, fields, counter_WORD, read_budget=8):
    """28F90 bounded data/counter projection, not a replacement CPU entry.

    The budget is an explicit diagnostic limit. FFFF does NOT stop on the
    physical FFFF threshold: the original unsigned BCC continues reading.
    """
    image = rebuild(rom, fields)
    f.uint(counter_WORD, 65535, 'counter low WORD')
    f.uint(read_budget, 65536, 'diagnostic read budget')
    if read_budget == 0:
        raise ValueError('positive diagnostic read budget required')
    index = 0xFFFE
    address = THRESHOLD_START
    reads = []
    for _ in range(read_budget):
        index = (index + 2) & 65535
        if address + 2 > len(image):
            return dict(status='ROM_read_boundary', D1_WORD=index, A2=address, reads=reads,
                        true_RTS_executed=False, complete_CPU_entry=False)
        threshold = int.from_bytes(image[address:address + 2], 'big')
        reads.append(dict(pc=0x28F96, address=address, size=2, value=threshold,
                          BCC_taken=counter_WORD >= threshold))
        address += 2
        if counter_WORD < threshold:
            return dict(status='original_unsigned_compare_return', D1_WORD=index, A2=address,
                        reads=reads, true_RTS_executed=False, complete_CPU_entry=False)
    return dict(status='diagnostic_budget_boundary', D1_WORD=index, A2=address, reads=reads,
                true_RTS_executed=False, complete_CPU_entry=False)


def read_parameter(rom, fields, read_PC, D6_WORD):
    """One original read at a supported PC, including signed-WORD overreads."""
    f.uint(read_PC, 0xFFFFFFFF, 'read PC')
    f.uint(D6_WORD, 65535, 'D6 low WORD')
    matches = [(spec, group, stage) for spec in TABLES for group in range(3)
               for stage, pc in enumerate(spec[3][group]) if pc == read_PC]
    if len(matches) != 1:
        raise ValueError('unsupported original parameter read PC')
    image = rebuild(rom, fields)
    spec, group, stage = matches[0]
    base = read_PC + 2 + int.from_bytes(image[read_PC + 3:read_PC + 4], 'big', signed=True)
    logical = (base + signed_WORD(D6_WORD)) & 0xFFFFFFFF
    bus = logical & 0xFFFFFF
    result = dict(pc=read_PC, source_base=base, D6_WORD=D6_WORD, signed_D6=signed_WORD(D6_WORD),
                  logical_address=logical, address=bus, size=2,
                  inside_stage_editor=base <= bus and bus + 2 <= base + 12,
                  inside_table_editor=spec[0] <= bus and bus + 2 <= spec[1],
                  complete_CPU_entry=False)
    if bus & 1:
        return dict(**result, status='odd_WORD_address_boundary', value=None, read_performed=False)
    if bus + 2 > len(image):
        return dict(**result, status='ROM_read_boundary', value=None, read_performed=False)
    return dict(**result, status='WORD_read', value=int.from_bytes(image[bus:bus + 2], 'big'), read_performed=True)


def selected_read(rom, fields, class_WORD, flag_WORD, D6_WORD, stage):
    """Values AT original reads: no snapshot of live EFD2 or complete function."""
    f.uint(class_WORD, 65535, 'D1 class WORD at2A718')
    f.uint(flag_WORD, 65535, 'EFD2 WORD at the selected stage')
    f.uint(stage, 1, 'stage')
    table = 3 if class_WORD < 4 else 2 if class_WORD < 8 else 1 if class_WORD == 8 else 0
    group = 0 if flag_WORD == 0 else 2 if flag_WORD == 2 else 1
    return read_parameter(rom, fields, TABLES[table][3][group][stage], D6_WORD)


def predicate_value(parameter_WORD, rng_WORD):
    """Pure low-WORD result of2AA00, supplied RNG value, no host randomness."""
    f.uint(parameter_WORD, 65535, 'complete source WORD')
    f.uint(rng_WORD, 65535, 'original RNG low WORD')
    mask = parameter_WORD & 7
    threshold = parameter_WORD >> 4
    masked = rng_WORD & mask
    return dict(parameter_WORD=parameter_WORD, mask_WORD=mask, ignored_bit3=(parameter_WORD >> 3) & 1,
                threshold_WORD=threshold, masked_RNG_WORD=masked, CMP_carry=masked < threshold,
                CMP_zero=masked == threshold, RNG_executed=False, complete_CPU_entry=False)


def schema():
    def fixed(value):
        if type(value) is dict:
            return dict(type='object', required=list(value), additionalProperties=False,
                        properties={key: fixed(item) for key, item in value.items()})
        if type(value) is list:
            return dict(type='array', minItems=len(value), maxItems=len(value), items=False,
                        prefixItems=[fixed(item) for item in value])
        return dict(type={str: 'string', int: 'integer', bool: 'boolean'}[type(value)], const=value)
    props = {key: fixed(value) for key, value in metadata().items()}
    threshold = fixed(threshold_topology())
    threshold['required'].append('WORDs')
    threshold['properties']['WORDs'] = dict(type='array', minItems=6, maxItems=6,
        items=dict(type='integer', minimum=0, maximum=65535))
    props['threshold_source'] = threshold
    tables = []
    for spec in TABLES:
        table = fixed(topology(spec))
        groups = []
        for i in range(3):
            group = fixed(group_topology(spec, i))
            group['required'].append('stage_WORDs')
            group['properties']['stage_WORDs'] = dict(type='array', minItems=2, maxItems=2,
                items=dict(type='array', minItems=6, maxItems=6, items=dict(type='integer', minimum=0, maximum=65535)))
            groups.append(group)
        table['required'].append('groups')
        table['properties']['groups'] = dict(type='array', minItems=3, maxItems=3, items=False, prefixItems=groups)
        tables.append(table)
    props['tables'] = dict(type='array', minItems=4, maxItems=4, items=False, prefixItems=tables)
    return dict(type='object', required=list(props), additionalProperties=False, properties=props,
                **{'$schema': 'https://json-schema.org/draft/2020-12/schema'})


def raw_guard(base):
    """Explicit existing layout input; no hidden build directory dependency."""
    raw = d.raw_positions(base)
    positions = {p for spec in TABLES for p in range(spec[0], spec[1])}
    positions.update(range(THRESHOLD_START, THRESHOLD_START + 12))
    if len(positions) != EDITABLE_BYTES or not positions <= raw:
        raise ValueError('all300 positions must remain sole current raw authority')
    return dict(guarded_raw_bytes=len(positions), layout_remaining_raw=len(raw),
                threshold_source_raw_bytes=len(set(range(THRESHOLD_START, THRESHOLD_START + 12)) & raw))


def render_bundle(rom):
    fields = extract(rom)
    image = rebuild(rom, load_fields(dump(fields)))
    if image != rom:
        raise ValueError('serialized entire-ROM roundtrip differs')
    coverage = {read_parameter(rom, fields, pc, index)['address']
                for spec in TABLES for pair in spec[3] for pc in pair for index in range(0, 12, 2)}
    if coverage != {p for spec in TABLES for p in range(spec[0], spec[1], 2)}:
        raise ValueError('24 original reader PCs do not cover exact144 physical WORDs')
    threshold_union = {event['address'] for value in (0, 40, 60, 80, 100, 120)
                       for event in counter_index(rom, fields, value)['reads']}
    if threshold_union != set(range(THRESHOLD_START, THRESHOLD_START + 12, 2)):
        raise ValueError('original counter reader does not cover exact6 threshold WORDs')
    report = dict(**metadata(), editable_bytes=300, tables=4, source_WORDs=150, original_read_PCs=25,
        parameter_source_WORDs=144, threshold_source_WORDs=6,
        conditioned_editor_read_union_bytes=300, whole_ROM_exact=True, whole_ROM_sha256=sha(image),
        guarded_original_code=[dict(start=a, end=z, sha256=digest, physical_emit=False) for a, z, digest in GUARDS],
        counter_threshold_source=dict(start=THRESHOLD_START, end=THRESHOLD_START + 12, WORDs=fields['threshold_source']['WORDs'],
            physical_emit=True, original_read_PC=0x28F96, next_original_PC=0x2A314, last_WORD_is_CPU_terminator=False),
        boundaries=[dict(start=spec[0], end=spec[1], last_WORD=int.from_bytes(rom[spec[1]-2:spec[1]], 'big'),
            next_original_PC=spec[1], next_instruction_prefix=rom[spec[1]:spec[1]+4].hex()) for spec in TABLES],
        counter_FFFF_diagnostic=counter_index(rom, fields, 65535, 6), natural_input_domains='unknown',
        independent_CPU_comparison=False, complete_CPU_entry=False,
        limitations=['Predicate source scope is144 WORDs plus6 counter WORDs; full D6.W uses signed offset, not a36/6-element clamp.',
            'Counter FFFF continues through the original FFFF threshold; diagnostic budget is not hardware behavior.',
            'EFD2 and class arguments are values at their original reads, not a live-RAM function snapshot.',
            'Source bit3 is preserved even though2AA00 ignores it; upper12 bits remain full unsigned threshold.',
            'RNG83D4 code/state and original consumer instructions are reused, never emitted by this package.',
            'No full caller/stack/CCR/RNG execution or natural-domain claim.'])
    members = {'fields.json': dump(fields), 'fields.schema.json': dump(schema()), 'validation.json': dump(report)}
    members['manifest.json'] = dump(dict(**metadata(), editable_bytes=300,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value):
    path = f.safe_path(value)
    if path != FORMAL_ROOT and (path == OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):
        raise ValueError('fresh formal directory or dedicated build/battle_probability_word_fields required')
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
        result = dict(path=str(target), editable_bytes=300, members={name: sha(data) for name, data in members.items()})
    else:
        image = rebuild(rom, load_fields(f.read_bounded(args.fields, f.MAX_JSON)))
        if target is not None:
            f.put(target, image)
        result = dict(path=None if target is None else str(target), exact_canonical=image == rom, sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
