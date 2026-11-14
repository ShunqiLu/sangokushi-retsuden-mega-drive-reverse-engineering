"""Lower the admitted complete battle-descriptor Frame rules to M68000.

The descriptor frontend supplies effects only after admitting the current
remaining_flows.business_city whole Frame owners. This backend preserves their
live register/partial-write, ordered memory and physical CALL allocation. It
never reads a ROM, assembly snapshot, old generated unit or opcode payload.
"""
from .compiler_common import CompileError, Emitter
from .target import REGISTERS, SCALAR_BINDINGS, TABLE_BINDINGS


FRAME_DESCRIPTOR_BINDINGS = {
    'prepare_both_battle_sides': (0x1B6C2, 0x1B7A2),
    'prepare_battle_mode_header': (0x1B7A2, 0x1B832),
    'prepare_battle_terrain': (0x1B850, 0x1B890),
    'choose_battle_order': (0x1B896, 0x1B8AC),
}


def _table(field):
    binding = TABLE_BINDINGS[field]
    suffix, address = binding['suffix'], binding['address']
    return f'0x{address & 0xffff if suffix == "w" else address:x}:{suffix}', 4 if suffix == 'w' else 6


def _scalar(field):
    binding = SCALAR_BINDINGS[field]
    suffix, address = binding['suffix'], binding['address']
    return f'0x{address & 0xffff if suffix == "w" else address:x}:{suffix}', 2 if suffix == 'w' else 4


def _lea(emitter, field, register):
    operand, width = _table(field)
    emitter.ins('lea', operand + ',%' + register, width)


def _load_scalar(emitter, field, register, size):
    operand, extension = _scalar(field)
    emitter.ins('move.' + size, operand + ',%' + register, 2 + extension)


def _store_scalar(emitter, field, operand, size, source_extension=0):
    destination, extension = _scalar(field)
    emitter.ins('move.' + size, operand + ',' + destination,
        2 + source_extension + extension)


def _mode_header(emitter, registers):
    """Two owner lookups, two three-way mode indices, distinct PC BYTE bases."""
    assignments, owners = registers['assignments'], registers['owners']
    first, second, index = registers['first_force'], registers['second_force'], registers['mode_index']
    selected, unused = registers['selected'], registers['unused_count']
    _lea(emitter, 'city_assignments', assignments)
    _lea(emitter, 'city_owners', owners)
    emitter.ins('clr.w', '%' + unused)
    for source, selected_field, force, force_field in (
            ('defender_officer', 'first_officer', first, 'first_force'),
            ('attacker_officer', 'second_officer', second, 'second_force')):
        _load_scalar(emitter, source, selected, 'w')
        _store_scalar(emitter, selected_field, '%' + selected, 'w')
        emitter.ins('move.b', f'(%{assignments},%{selected}.w),%{force}', 4)
        emitter.ins('andi.w', '#63,%' + force, 4)
        emitter.ins('move.b', f'(%{owners},%{force}.w),%{force}', 4)
        _store_scalar(emitter, force_field, '%' + force, 'w')
    emitter.ins('clr.w', '%' + index)
    for force, increment in ((first, 8), (second, 2)):
        complete = emitter.fresh('force_mode_complete')
        for field in ('active_force_1', 'active_force_2', 'active_force_3'):
            source, extension = _scalar(field)
            emitter.ins('cmp.b', source + ',%' + force, 2 + extension)
            emitter.ins('beq.w', complete, 4)
            emitter.ins('addq.w', f'#{increment},%{index}')
        emitter.label(complete)
    base = 'prep_data_battle_mode_parameters'
    _store_scalar(emitter, 'battle_mode', f'({base}-.-2)(%pc,%{index}.w)', 'b', 2)
    clear, extension = _scalar('mode_clear')
    emitter.ins('clr.b', clear, 2 + extension)
    # The second original PC-relative EA is 1B833, not a second 1B832 read.
    _store_scalar(emitter, 'swap_sides', f'({base}+1-.-2)(%pc,%{index}.w)', 'b', 2)
    return ('battle_mode_parameters',)


def _terrain(emitter, registers):
    """Inline the actual packet-view acquisition before row*72+column."""
    objects, offsets = registers['objects'], registers['offsets']
    row, column = registers['row'], registers['column']
    _lea(emitter, 'packed_entities', objects)
    _lea(emitter, 'packed_offsets', offsets)
    _load_scalar(emitter, 'object_index', row, 'w')
    emitter.ins('adda.w', f'(%{offsets},%{row}.w),%{objects}', 4)
    emitter.ins('clr.w', '%' + row)
    emitter.ins('move.b', f'1(%{objects}),%{row}', 4)
    emitter.ins('move.w', f'%{row},%{column}')
    emitter.ins('lsl.w', '#3,%' + row)
    emitter.ins('add.w', f'%{column},%{row}')
    emitter.ins('lsl.w', '#3,%' + row)
    emitter.ins('clr.w', '%' + column)
    emitter.ins('move.b', f'2(%{objects}),%{column}', 4)
    emitter.ins('add.w', f'%{column},%{row}')
    _lea(emitter, 'terrain_cells', objects)
    emitter.ins('clr.w', '%' + column)
    emitter.ins('move.b', f'(%{objects},%{row}.w),%{column}', 4)
    emitter.ins('lea', '(prep_data_terrain_parameters-.-2)(%pc),%' + objects, 4)
    _store_scalar(emitter, 'battle_terrain', f'(%{objects},%{column}.w)', 'b', 2)
    return ('terrain_parameters',)


def _order(emitter, registers):
    first, second = registers['first'], registers['second']
    _load_scalar(emitter, 'attacker_officer', first, 'w')
    _load_scalar(emitter, 'defender_officer', second, 'w')
    source, extension = _scalar('swap_sides')
    emitter.ins('tst.b', source, 2 + extension)
    complete = emitter.fresh('order_complete')
    emitter.ins('beq.w', complete, 4)
    # The loads retain high WORDs, and EXG swaps the complete LONG carriers.
    emitter.ins('exg', f'%{first},%{second}')
    emitter.label(complete)
    return ()


def _both_sides(emitter, registers):
    """All six real CALLs and two ordered, live side-descriptor iterations."""
    for name in ('prepare_battle_mode_header', 'prepare_battle_terrain', 'choose_battle_order'):
        emitter.ins('bsr.w', name, 4)
    assignments, owners, leaders = registers['assignments'], registers['owners'], registers['leaders']
    selected, second, force = registers['first'], registers['second'], registers['owner']
    _lea(emitter, 'city_assignments', assignments)
    _lea(emitter, 'city_owners', owners)
    _lea(emitter, 'force_leaders', leaders)
    for member, destination in ((selected, 'first_leader'), (second, 'second_leader')):
        emitter.ins('clr.w', '%' + force)
        emitter.ins('move.b', f'(%{assignments},%{member}.w),%{force}', 4)
        emitter.ins('andi.w', '#63,%' + force, 4)
        emitter.ins('move.b', f'(%{owners},%{force}.w),%{force}', 4)
        emitter.ins('lsl.w', '#1,%' + force)
        _store_scalar(emitter, destination, f'(%{leaders},%{force}.w)', 'w', 2)
    for field, local in (('capacity_fields', 'capacities'), ('side_attributes', 'side_attributes'),
            ('ratio_attributes', 'ratio_attributes'), ('troops', 'troops'),
            ('awards', 'awards'), ('attribute_selectors', 'attributes')):
        _lea(emitter, field, registers[local])
    for side in ('first', 'second'):
        if side == 'second':
            emitter.ins('move.w', f'%{second},%{selected}')
        _store_scalar(emitter, side + '_selected', '%' + selected, 'w')
        _store_scalar(emitter, side + '_side_attribute',
            f'(%{registers["side_attributes"]},%{selected}.w)', 'b', 2)
        emitter.ins('bsr.w', 'maximum_three_live_lookup_attributes', 4)
        _store_scalar(emitter, side + '_maximum', '%d3', 'w')
        emitter.ins('lsl.w', '#1,%' + selected)
        for source, destination in (('ratio_attributes', 'ratio_attribute'),
                ('troops', 'troops'), ('awards', 'awards')):
            _store_scalar(emitter, side + '_' + destination,
                f'(%{registers[source]},%{selected}.w)', 'w', 2)
        emitter.ins('lsl.w', '#1,%' + selected)
        _store_scalar(emitter, side + '_capacity',
            f'2(%{registers["capacities"]},%{selected}.w)', 'w', 2)
    emitter.ins('bsr.w', 'compact_active_deployment_queue', 4)
    return ()


def lower_frame_descriptor(binding, effects):
    """Return one unit for an already-admitted current whole Frame owner.

    Admission belongs to compiler_descriptor's current semantic_functions
    path. It must supply the effects from ``binding.name + '_fields'``; a
    historical scalar projection or old semantic snapshot is not this input.
    """
    expected = FRAME_DESCRIPTOR_BINDINGS.get(binding.name)
    if expected is None or (binding.entry, binding.end) != expected:
        raise CompileError('complete current Frame descriptor binding required')
    emitter = Emitter(binding)
    emitter.begin()
    lower = {'prepare_both_battle_sides': _both_sides,
        'prepare_battle_mode_header': _mode_header,
        'prepare_battle_terrain': _terrain, 'choose_battle_order': _order}[binding.name]
    definitions = lower(emitter, REGISTERS[binding.name])
    emitter.end()
    if sum(row['encoding_bytes'] for row in emitter.mapping) != binding.end - binding.entry:
        raise CompileError('complete Frame descriptor does not fit its exact original allocation')
    unit = emitter.unit(effects)
    unit['assembly'] = ''.join(f'.set prep_data_{name},0x{TABLE_BINDINGS[name]["address"]:x}\n'
        for name in definitions) + unit['assembly']
    return unit
