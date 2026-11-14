"""Five physical BE16 parameter allocations with original-width read projections."""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from tools.direct_code import direct_code as d

f = d.f
ROOT = d.ROOT
FORMAL_ROOT = ROOT / 'analysis/diplomacy_parameter_word_fields/generated'
DEFAULT_FIELDS = FORMAL_ROOT / 'fields.json'
OUTPUT_ROOT = ROOT / 'build/diplomacy_parameter_word_fields'
FORMAT = 'g5510-diplomacy-arithmetic-parameter-WORD-fields-v1'
START, END, EDITABLE_BYTES = 0xDF08, 0xDF6E, 102
TABLES = (
    (0xDF08, 0xDF0E, 1, 'DIVU_divisor_WORDs', (0xEEC6,)),
    (0xDF0E, 0xDF1A, 2, 'MULU_span_ADD_WORD_pairs', (0xF806, 0xF80C)),
    (0xDF1A, 0xDF3E, 2, 'MULU_span_ADD_WORD_pairs', (0xF280, 0xF286)),
    (0xDF3E, 0xDF62, 2, 'MULU_span_ADD_WORD_pairs', (0xF76A, 0xF770)),
    (0xDF62, 0xDF6E, 2, 'overwritten_preload_multiplier_WORD_pairs', (0xE922, 0xE92C)),
)
GUARDS = (
    (0xEEBC, 0xEECA, reference_value(__name__, 'GUARDS')),
    (0xF232, 0xF28E, reference_value(__name__, 'GUARDS_2')),
    (0xF71C, 0xF778, reference_value(__name__, 'GUARDS_3')),
    (0xF7F6, 0xF810, reference_value(__name__, 'GUARDS_4')),
    (0xE90E, 0xE932, reference_value(__name__, 'GUARDS_5')),
    (0xDF6E, 0xDF72, reference_value(__name__, 'GUARDS_6')),
    (0x83D4, 0x83FA, reference_value(__name__, 'GUARDS_7')),
)
CALLERS = ((0xF0CA, 0xF232, '61000166'), (0xF6CC, 0xF71C, '6100004e'),
           (0xF778, 0xF7DA, '61000060'), (0x32BE2, 0xF7DA, '4eb90000f7da'))
LEAS = ((0xEEBC, 0xDF08, '43faf04a'), (0xF7FC, 0xDF0E, '41fae710'),
        (0xF27C, 0xDF1A, '41faec9c'), (0xF766, 0xDF3E, '41fae7d6'),
        (0xE91E, 0xDF62, '41faf642'))
sha, dump, load_fields = f.sha, f.dump, f.load_json


def metadata():
    return dict(format=FORMAT, canonical_source=dict(size=f.ROM_SIZE, sha256=f.ROM_SHA),
                confidence='confirmed_original_WORD_reads_probable_diplomacy_parameter_role',
                owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0)


def topology(spec):
    a, z, width, role, pcs = spec
    return dict(id=f'rom_{a:06X}_arithmetic_WORD_source', start=a, end=z,
                physical_rows=(z-a)//(2*width), WORDs_per_row=width, WORD_order='big',
                role=role, original_read_PCs=list(pcs), editor_count_is_CPU_clamp=False)


def verify_rom(rom):
    if type(rom) is not bytes:
        raise ValueError('immutable original ROM bytes required')
    f.verify_rom(rom)
    for a, z, digest in GUARDS:
        if sha(rom[a:z]) != digest:
            raise ValueError('original reader/producer/RNG/boundary source differs')
    for pc, target, raw in LEAS:
        if rom[pc:pc+4] != bytes.fromhex(raw) or pc+2+int.from_bytes(rom[pc+2:pc+4], 'big', signed=True) != target:
            raise ValueError('original PC-relative allocation reference differs')
    for pc, target, raw in CALLERS:
        if rom[pc:pc+len(raw)//2] != bytes.fromhex(raw):
            raise ValueError('original compiled caller differs')
        decoded = int.from_bytes(rom[pc+2:pc+6], 'big') if raw.startswith('4eb9') else pc+2+int.from_bytes(rom[pc+2:pc+4], 'big', signed=True)
        if decoded != target:
            raise ValueError('original caller target differs')


def extract(rom):
    verify_rom(rom)
    tables = []
    for spec in TABLES:
        a, z, width, _, _ = spec
        rows = [[int.from_bytes(rom[p+2*j:p+2*j+2], 'big') for j in range(width)]
                for p in range(a, z, 2*width)]
        tables.append(dict(**topology(spec), row_WORDs=rows))
    return dict(**metadata(), tables=tables)


def fixed(value, expected, mutable, label):
    f.keys(value, set(expected) | set(mutable), label)
    for key, item in expected.items():
        f.same(value[key], item, label + '.' + key)


def exact_list(value, count, label):
    if type(value) is not list or len(value) != count:
        raise ValueError(label + ': physical allocation differs')
    return value


def blocks(rom, fields):
    verify_rom(rom)
    fixed(fields, metadata(), {'tables'}, 'diplomacy parameter package')
    result = []
    for table, spec in zip(exact_list(fields['tables'], 5, 'tables'), TABLES):
        expected = topology(spec)
        fixed(table, expected, {'row_WORDs'}, 'physical table')
        data = bytearray()
        for row in exact_list(table['row_WORDs'], expected['physical_rows'], 'physical rows'):
            for word in exact_list(row, expected['WORDs_per_row'], 'row WORDs'):
                data.extend(f.uint(word, 65535, 'full parameter WORD').to_bytes(2, 'big'))
        result.append(dict(id=expected['id'], start=spec[0], end=spec[1], data=bytes(data), role=spec[3]))
    if sum(len(row['data']) for row in result) != EDITABLE_BYTES:
        raise ValueError('102-byte allocation differs')
    return result


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row['start']:row['end']] = row['data']
    return bytes(image)


def read_WORD(image, base, index, displacement, pc):
    # Brief indexed EA sign-extends the index once; +2 is an EA displacement,
    # not a new ADDQ.W index operation (including index7FFE/8000 boundaries).
    signed = index-65536 if index & 32768 else index
    logical = (base + signed + displacement) & 0xFFFFFFFF
    address = logical & 0xFFFFFF
    if address & 1 or address+2 > len(image):
        raise ValueError('source WORD read boundary')
    return dict(kind='source_WORD_read_projection', pc=pc, logical_address=logical,
                address=address, size=2, value=int.from_bytes(image[address:address+2], 'big'),
                index_WORD=index, inside_editor_catalog=START <= address and address+2 <= END)


def projection_flags():
    return dict(CPU_executed=False, true_call_RTS_executed=False, independent_CPU_comparison=False,
                complete_entry=False, natural_selector_domain_complete=False)


def pair_preview(rom, fields, reader, selector_first_WORD, rng_WORD, failed_comparisons=0, *, selector_add_WORD=None):
    """MULU/SWAP/ADD projection, supplied RNG result; never host randomness.

    F232/F71C read EFD2 twice. Callers can supply different values at those
    reads; omitting the second explicitly requests a stable-selector example.
    The comparison count models the original two equality branches, not a CPU
    upper-bound check on EFD2. F7DA has a single selector read and no such chain.
    """
    f.uint(selector_first_WORD, 65535, 'selector at first original read')
    f.uint(rng_WORD, 65535, 'supplied original RNG low WORD')
    f.uint(failed_comparisons, 2, 'original failed equality comparisons')
    if type(reader) is not str or reader not in ('rom_00F232', 'rom_00F71C', 'rom_00F7DA'):
        raise ValueError('explicit original reader required')
    if reader == 'rom_00F7DA':
        if selector_add_WORD is not None or failed_comparisons:
            raise ValueError('F7DA has one selector read and no comparison increments')
        base, pcs = 0xDF0E, (0xF806, 0xF80C)
        index = (selector_first_WORD << 2) & 65535
        second = None
    else:
        second = selector_first_WORD if selector_add_WORD is None else f.uint(selector_add_WORD, 65535, 'selector at second live original read')
        base, pcs, shift = (0xDF1A, (0xF280, 0xF286), 4) if reader == 'rom_00F232' else (0xDF3E, (0xF76A, 0xF770), 3)
        index = ((((selector_first_WORD << 1) & 65535) + second) & 65535)
        index = (index << shift) & 65535
        for _ in range(failed_comparisons):
            index = (index + 4) & 65535
    image = rebuild(rom, fields)
    reads = [read_WORD(image, base, index, displacement, pc) for displacement, pc in zip((0, 2), pcs)]
    product = rng_WORD * reads[0]['value']
    swapped = ((product & 65535) << 16) | (product >> 16)
    value = ((product >> 16) + reads[1]['value']) & 65535
    return dict(**projection_flags(), status='MULU_SWAP_ADD_projected', reader=reader,
                selector_first_WORD=selector_first_WORD, selector_add_WORD=second,
                stable_selector_example=second is None or second == selector_first_WORD,
                failed_comparisons=failed_comparisons, index_WORD=index, events=reads,
                product_LONG=product, D0_LONG_after_SWAP=swapped,
                result_WORD=value, D0_LONG_after_ADD=(swapped & 0xFFFF0000) | value,
                D2_saved_restored_bytes=2 if reader != 'rom_00F7DA' else 0,
                RNG_helper_reused=0x83D4, RNG_helper_executed=False)


def divisor_preview(rom, fields, selector_WORD, numerator_LONG):
    f.uint(selector_WORD, 65535, 'selector WORD at EEC0')
    f.uint(numerator_LONG, 0xFFFFFFFF, 'unsigned dividend LONG at EEC6')
    read = read_WORD(rebuild(rom, fields), 0xDF08, (selector_WORD << 1) & 65535, 0, 0xEEC6)
    result = dict(**projection_flags(), selector_WORD=selector_WORD, events=[read], numerator_LONG=numerator_LONG)
    if read['value'] == 0:
        return dict(**result, status='DIVU_divide_by_zero_boundary')
    quotient, remainder = divmod(numerator_LONG, read['value'])
    if quotient > 65535:
        return dict(**result, status='DIVU_overflow_boundary', quotient=quotient)
    return dict(**result, status='DIVU_projected', quotient=quotient, remainder=remainder,
                packed_result_LONG=(remainder << 16) | quotient)


def gift_pair_preview(rom, fields, selector_WORD, seed_WORD):
    f.uint(selector_WORD, 65535, 'selector at E918')
    f.uint(seed_WORD, 65535, 'live seed WORD at E926')
    image = rebuild(rom, fields)
    index = (selector_WORD << 2) & 65535
    reads = [read_WORD(image, 0xDF62, index, displacement, pc) for displacement, pc in ((0, 0xE922), (2, 0xE92C))]
    return dict(**projection_flags(), status='gift_preload_SWAP_ADD_projected', events=reads,
                overwritten_preload_WORD=reads[0]['value'], effective_multiplier_WORD=reads[1]['value'],
                D1_LONG_after_ADD=(seed_WORD << 16) | reads[1]['value'])


def raw_guard(base):
    raw = d.raw_positions(base)
    if not set(range(START, END)) <= raw:
        raise ValueError('all102 bytes must remain sole raw source authority')
    return dict(guarded_raw_bytes=102, layout_remaining_raw=len(raw))


def render_bundle(rom):
    fields = extract(rom)
    if rebuild(rom, load_fields(dump(fields))) != rom:
        raise ValueError('serialized whole-ROM roundtrip differs')
    views = [divisor_preview(rom, fields, i, 300) for i in range(3)]
    # Conditional full-WORD read coverage, deliberately not natural fixtures:
    # solve24*s+4*b=EA mod65536 for each physical pair via original F71C.
    constructs = []
    for address in range(0xDF0E, END, 4):
        index = (address - 0xDF3E) & 65535
        branch = 0 if index % 8 == 0 else 1
        adjusted = (index - 4*branch) & 65535
        selector = ((adjusted // 8) * 2731) % 8192  # inverse3 modulo8192
        view = pair_preview(rom, fields, 'rom_00F71C', selector, 65535, branch)
        if view['events'][0]['address'] != address:
            raise ValueError('constructed source read arithmetic differs')
        constructs.append(dict(selector_WORD=selector, failed_comparisons=branch, address=address))
        views.append(view)
    union = {p for view in views for event in view['events'] for p in range(event['address'], event['address']+2)}
    if union != set(range(START, END)):
        raise ValueError('physical conditional source read projection union differs')
    report = dict(**metadata(), editable_bytes=102, full_WORD_fields=51, physical_blocks=5,
        whole_ROM_exact=True, whole_ROM_sha256=sha(rebuild(rom, fields)),
        constructed_read_projections=len(views), conditional_source_read_union_bytes=len(union),
        conditional_constructs_not_natural=constructs,
        original_PC_relative_references=[dict(pc=p, target=t, bytes=b) for p,t,b in LEAS],
        original_callers=[dict(pc=p, target=t, bytes=b, CPU_executed=False) for p,t,b in CALLERS],
        source_guards=[dict(start=a, end=z, sha256=h, physical_emit=False) for a,z,h in GUARDS],
        original_pair_stride=dict(F232_stable_selector=48, F71C_stable_selector=24,
                                  first_read_shift=1, final_shifts=[4, 3], comparison_increments=[0, 4, 8]),
        original_RNG_reused=True, new_RNG_physical_emit_bytes=0,
        gift_preload_existing_semantic_author='tools/diplomacy_flow/diplomacy_flow.py:GiftDifficultyPairs',
        **projection_flags(),
        limitations=['51 full WORDs are fixed physical fields, not a natural EFD2 domain or CPU row clamp.',
            'Two live selector reads are independent; same-value examples do not establish alias/IRQ lifetime.',
            'Original48/24 stride crosses parameter roles and can read compiledDF6E code; no normalization.',
            'EA +2 remains displacement after sign extension, not a second wrapped index.',
            'Read/arithmetic projections are not full CPU, RNG/stack execution or complete diplomacy functions.',
            'High-selector constructed catalog coverage is conditional only; no new natural/owner/domain claims.',
            'Old gift semantic authority remains unchanged; this package alone emits these new source fields.'])
    members = {'fields.json': dump(fields), 'validation.json': dump(report)}
    members['manifest.json'] = dump(dict(**metadata(), editable_bytes=102,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value):
    path = f.safe_path(value)
    if path != FORMAL_ROOT and (path == OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):
        raise ValueError('fresh formal directory or dedicated build/diplomacy_parameter_word_fields required')
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
        for name,data in members.items():
            f.put(target / name, data)
        result = dict(path=str(target), editable_bytes=102, members={name:sha(data) for name,data in members.items()})
    else:
        image = rebuild(rom, load_fields(f.read_bounded(args.fields, f.MAX_JSON)))
        if target is not None:
            f.put(target, image)
        result = dict(path=None if target is None else str(target), exact_canonical=image == rom, sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
