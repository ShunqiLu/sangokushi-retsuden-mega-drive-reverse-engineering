"""Four physical selections of two eight-WORD rows, preserving all tile bits."""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from tools.direct_code import direct_code as d

f = d.f
ROOT = d.ROOT
FORMAL_ROOT = ROOT / 'analysis/selected_tile_row_word_fields/generated'
DEFAULT_FIELDS = FORMAL_ROOT / 'fields.json'
OUTPUT_ROOT = ROOT / 'build/selected_tile_row_word_fields'
FORMAT = 'g5510-selected-VDP-row-source-WORD-fields-v1'
START, END = 0xA79E, 0xA81E
EDITABLE_BYTES = 128
CONTROL_LONGS = (0x41200003, 0x41A00003)
GUARDS = (
    (0xA760, 0xA79E, reference_value(__name__, 'GUARDS')),
    (0x153C, 0x1546, reference_value(__name__, 'GUARDS_2')),
    (0x1546, 0x154C, reference_value(__name__, 'GUARDS_3')),
    (0x9C66, 0x9C6A, reference_value(__name__, 'GUARDS_4')),
)
sha, dump, load_fields = f.sha, f.dump, f.load_json


def metadata():
    return dict(format=FORMAT, canonical_source=dict(size=f.ROM_SIZE, sha256=f.ROM_SHA),
                confidence='confirmed_WORD_transfer_probable_selected_tile_role',
                owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0)


def table_topology():
    return dict(id='rom_00A79E_selected_tile_row_WORDs', start=START, end=END,
                physical_selections=4, rows_per_selection=2, WORDs_per_row=8, WORD_order='big',
                original_LEA=0xA768, original_read_PC=0xA792, editor_count_is_CPU_clamp=False)


def selection_topology(i):
    return dict(editor_index=i, start=START + 32 * i, end=START + 32 * (i + 1))


def verify_rom(rom):
    if type(rom) is not bytes:
        raise ValueError('immutable canonical ROM bytes required')
    f.verify_rom(rom)
    for start, end, digest in GUARDS:
        if sha(rom[start:end]) != digest:
            raise ValueError('original entry/consumer/producer/caller differs')
    if rom[0xA768:0xA772] != bytes.fromhex('41fa00343438f350eb4a'):
        raise ValueError('original source and low-WORD LSL5 differ')
    if 0xA76A + int.from_bytes(rom[0xA76A:0xA76C], 'big', signed=True) != START:
        raise ValueError('original PC-relative source differs')
    if rom[0xA77C:0xA77E] != bytes.fromhex('6110') or rom[0xA788:0xA78A] != bytes.fromhex('6104'):
        raise ValueError('two true original short BSRs differ')
    if rom[0xA78E:0xA79E] != bytes.fromhex('323c00073cb02000544251c9fff84e75'):
        raise ValueError('original eight-WORD reader/ADDQ/DBRA differs')


def extract(rom):
    verify_rom(rom)
    selections = []
    for i in range(4):
        base = START + 32 * i
        rows = [[int.from_bytes(rom[base + 16 * row + 2 * cell:base + 16 * row + 2 * cell + 2], 'big')
                 for cell in range(8)] for row in range(2)]
        selections.append(dict(**selection_topology(i), row_WORDs=rows))
    return dict(**metadata(), table=dict(**table_topology(), selections=selections))


def fixed(value, expected, mutable, label):
    f.keys(value, set(expected) | set(mutable), label)
    for key, item in expected.items():
        f.same(value[key], item, label + '.' + key)


def exact_list(value, count, label):
    if type(value) is not list or len(value) != count:
        raise ValueError(label + ': fixed physical count differs')
    return value


def blocks(rom, fields):
    verify_rom(rom)
    fixed(fields, metadata(), {'table'}, 'selected row package')
    table = fields['table']
    fixed(table, table_topology(), {'selections'}, 'table')
    data = bytearray()
    for i, selection in enumerate(exact_list(table['selections'], 4, 'physical selections')):
        fixed(selection, selection_topology(i), {'row_WORDs'}, 'selection')
        for row in exact_list(selection['row_WORDs'], 2, 'rows'):
            for word in exact_list(row, 8, 'row WORDs'):
                data.extend(f.uint(word, 65535, 'complete tile source WORD').to_bytes(2, 'big'))
    if len(data) != EDITABLE_BYTES:
        raise ValueError('128-byte physical allocation differs')
    return [dict(id=table['id'], start=START, end=END, data=bytes(data), role='selected_VDP_tile_row_BE16_source_fields')]


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row['start']:row['end']] = row['data']
    return bytes(image)


def next_selector(current_WORD):
    """153C ADDQ.W1 then1540 ANDI.W3, arithmetic only, no RAM/CPU execute."""
    f.uint(current_WORD, 65535, 'F350 low WORD')
    return ((current_WORD + 1) & 65535) & 3


def transfer_preview(rom, fields, selector_WORD):
    """Value AT A76C. Source read/port-write descriptors, no hardware execution.

    The original D2 WORD increments after every read, so sign extension is
    recomputed per WORD, including wrap at FFFE->0000 between iterations.
    """
    f.uint(selector_WORD, 65535, 'original F350 WORD at read')
    image = rebuild(rom, fields)
    index = (selector_WORD << 5) & 65535
    initial_index = index
    events = []
    rows = []
    for row, control in enumerate(CONTROL_LONGS):
        events.append(dict(kind='VDP_control_write_projection', pc=(0xA772, 0xA77E)[row], address=0xC00004, size=4, value=control))
        values = []
        for cell in range(8):
            signed_index = index - 65536 if index & 32768 else index
            logical = (START + signed_index) & 0xFFFFFFFF
            address = logical & 0xFFFFFF
            if address & 1 or address + 2 > len(image):
                return dict(status='source_WORD_read_boundary', selector_WORD=selector_WORD,
                    initial_D2_WORD=initial_index, final_D2_WORD=index, rows=rows, events=events,
                    hardware_executed=False, true_call_RTS_executed=False, complete_CPU_entry=False)
            word = int.from_bytes(image[address:address + 2], 'big')
            events.append(dict(kind='source_WORD_read_projection', pc=0xA792, row=row, cell=cell,
                logical_address=logical, address=address, size=2, value=word, D2_WORD=index,
                inside_editor_catalog=START <= address and address + 2 <= END))
            events.append(dict(kind='VDP_data_write_projection', pc=0xA792, row=row, cell=cell,
                address=0xC00000, size=2, value=word))
            values.append(word)
            index = (index + 2) & 65535
        rows.append(dict(row=row, control_LONG=control, WORDs=values))
    return dict(status='two_eight_WORD_rows_projected', selector_WORD=selector_WORD,
        initial_D2_WORD=initial_index, final_D2_WORD=index, rows=rows, events=events,
        hardware_executed=False, true_call_RTS_executed=False, complete_CPU_entry=False)


def raw_guard(base):
    raw = d.raw_positions(base)
    if not set(range(START, END)) <= raw:
        raise ValueError('all128 bytes must remain sole raw source authority')
    return dict(guarded_raw_bytes=128, layout_remaining_raw=len(raw), excluded_tail_bytes=16,
                excluded_tail_raw_bytes=len(set(range(END, 0xA82E)) & raw))


def render_bundle(rom):
    fields = extract(rom)
    image = rebuild(rom, load_fields(dump(fields)))
    if image != rom:
        raise ValueError('serialized whole-ROM roundtrip differs')
    views = [transfer_preview(rom, fields, i) for i in range(4)]
    reads = [event for view in views for event in view['events'] if event['kind'] == 'source_WORD_read_projection']
    union = {p for event in reads for p in range(event['address'], event['address'] + event['size'])}
    if union != set(range(START, END)):
        raise ValueError('constructed original read union differs from128-byte fields')
    report = dict(**metadata(), editable_bytes=128, full_WORD_fields=64, constructed_selections=4,
        source_reads=len(reads), constructed_source_union_bytes=len(union),
        VDP_control_write_projections=8, VDP_WORD_write_projections=64,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image), source_table_sha256=sha(rom[START:END]),
        guarded_original_code=[dict(start=a, end=z, sha256=h, physical_emit=False) for a, z, h in GUARDS],
        true_original_BSRs=[dict(pc=0xA77C, target=0xA78E), dict(pc=0xA788, target=0xA78E)],
        excluded_tail=dict(start=END, end=0xA82E, bytes=16, confidence='unknown', physical_emit=False),
        natural_input_domains='unknown', independent_CPU_comparison=False, complete_CPU_entry=False,
        limitations=['Four editor selections are not a global CPU clamp; full selector WORD shift wraps then sign-extends each read.',
            'The writer transfers full WORDs to VDP data port, not color-palette normalization.',
            'Events are ordered read/write projections, not actual VDP/stack/CPU executions.',
            'The following16 bytes have no admitted independent consumer in this scope and are untouched.',
            'Selector arguments are values at A76C; whole live-RAM/IRQ alias lifetime is not proved.'])
    members = {'fields.json': dump(fields), 'validation.json': dump(report)}
    members['manifest.json'] = dump(dict(**metadata(), editable_bytes=128,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value):
    path = f.safe_path(value)
    if path != FORMAL_ROOT and (path == OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):
        raise ValueError('fresh formal directory or dedicated build/selected_tile_row_word_fields required')
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
        result = dict(path=str(target), editable_bytes=128, members={name: sha(data) for name, data in members.items()})
    else:
        image = rebuild(rom, load_fields(f.read_bounded(args.fields, f.MAX_JSON)))
        if target is not None:
            f.put(target, image)
        result = dict(path=None if target is None else str(target), exact_canonical=image == rom, sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
