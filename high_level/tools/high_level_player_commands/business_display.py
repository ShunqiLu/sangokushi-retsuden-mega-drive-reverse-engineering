"""Player route editing, group selection and RAM-only UI packet construction.

Tile constants are original tile IDs/control attributes, not embedded artwork.
The sprite helper's provisional historical name is retained for this draft API;
its actual role is clipping six-byte sprite descriptors into eight-byte slots.
"""
from .business_budget import _six_place_decimal_fields
from .contexts_numeric import DecimalMemory
from .domain import (
    GameState, Word, Long, Table, Cursor, CarryOutcome, checked_state,
    checked_table, checked_cursor, uint, u8, u16, u32, low8, low16,
    replace_word, negative_byte, negative_word, s16, divu_retained,
    descending_inclusive, read_packed_long, store_packed_long_reverse,
)
from .contexts_display import SpriteAppendResult, TileRun, RouteCost, MarkerResult, WorldSelection
from .business_budget import append_six_place_decimal_value
from .business_reuse import terrain_cell_query, collect_blocked_cargo


from .contexts_display import SpritePacketMemory, SpritePacketFields, FirstDeploymentFrame, first_replace, _first_word, _first_byte, _first_long, _first_add_word, _first_sub_word, _first_shift_word, _first_memory_word

from .domain import swap_words

def append_live_command_string_words(state: GameState, source: Table, x: Word, y: Word, attributes: Word = 0, reset_scroll: bool = True) -> SpriteAppendResult:
    """Historical player sprite API projects the same sole descriptor algorithm."""
    checked_state(state)
    checked_table(source,state)
    result = append_live_command_sprite_packet_fields(SpritePacketMemory(state),
        first_replace(FirstDeploymentFrame.unobserved(),roster=source.cursor()),
        x,y,attributes,reset_scroll=reset_scroll,initialize_clip=True)
    return SpriteAppendResult(result.frame.roster,result.attributes)


def append_route_selection_pair(state: GameState) -> None:
    checked_state(state)
    destination = state.route_candidate_list.cursor()
    while not negative_word(destination.next_word()):
        pass
    destination.set_word(0, state.scalar('route_first_member'), -2)
    destination.put_word(state.scalar('route_second_member'))
    destination.set_word(0, 65535, 2)


def append_route_cursor_sprite(state: GameState) -> None:
    checked_state(state)
    if state.scalar('ui_gate_flags') & 4:
        return
    x = state.scalar('route_row_coordinate')
    y = state.scalar('route_column_coordinate')
    state.set_scalar('scroll_x', state.scalar('map_scroll_x'))
    state.set_scalar('scroll_y', state.scalar('map_scroll_y'))
    append_live_command_string_words(state, state.route_cursor_shape, x, y, 0, False)


def step_world_route_cursor(state: GameState) -> None:
    """Directional priority and per-step terrain budget follow the original order."""
    checked_state(state)
    controls = state.scalar('held_controls_WORD')
    direction = 0
    if controls & 1:
        row = state.scalar('route_row_coordinate')
        if row == 0:
            return
        row = u16(row - 16)
        column = state.scalar('route_column_coordinate')
        direction = 1
    elif controls & 8:
        if state.scalar('route_column_coordinate') >= 0x450:
            return
        row = state.scalar('route_row_coordinate')
        column = u16(state.scalar('route_column_coordinate') + 16)
        direction = 2
    elif controls & 2:
        if state.scalar('route_row_coordinate') >= 0x470:
            return
        row = u16(state.scalar('route_row_coordinate') + 16)
        column = state.scalar('route_column_coordinate')
        direction = 3
    elif controls & 4:
        column = state.scalar('route_column_coordinate')
        if column == 0:
            return
        column = u16(column - 16)
        row = state.scalar('route_row_coordinate')
        direction = 4
    else:
        return
    result = query_route_move_cost(state, row, column)
    if negative_word(result.cost):
        return
    budget = state.scalar('remaining_move_budget')
    if budget < result.cost:
        return
    state.set_scalar('remaining_move_budget', u16(budget - result.cost))
    if direction == 1 or direction == 3:
        state.set_scalar('route_row_coordinate', result.row)
    else:
        state.set_scalar('route_column_coordinate', result.column)
    state.route_direction_bytes.set_byte(state.scalar('route_step_count'), direction)
    state.set_scalar('route_step_count', u16(state.scalar('route_step_count') + 1))


def query_scaled_route_terrain(state: GameState, row: Word, column: Word) -> RouteCost:
    checked_state(state)
    uint(row, 16)
    uint(column, 16)
    terrain, cost = terrain_cell_query(state, row >> 4, column >> 4)
    return RouteCost(u16((row >> 4) << 4), u16((column >> 4) << 4), cost)


def query_route_move_cost(state: GameState, row: Word, column: Word) -> RouteCost:
    checked_state(state)
    uint(row, 16)
    uint(column, 16)
    return query_scaled_route_terrain(state, row, column)


def append_candidate_member_panel(state: GameState) -> Cursor:
    checked_state(state)
    output = state.command_queue.cursor(state.scalar('command_queue_offset'))
    for tile in (6, 0xC322, 0xC380, 0xC381, 0xC381, 0xC381, 0xC381, 0xCB80):
        output.append_word(tile)
    members = state.selection_members.cursor()
    row_tile = 0xC3A2
    while True:
        output.set_word(0, 6, 16)
        output.append_word(6)
        output.put_word(row_tile)
        row_tile = u16(row_tile + 128)
        output.set_word(0, row_tile, 16)
        row_tile = u16(row_tile + 128)
        output = output.advance(2)
        output.set_word(0, 0xC382, 16)
        output.append_word(0xC382)
        tile = u16((members.next_byte() << 3) + 0xC019)
        output = append_short_paired_tiles(state, output, tile, 3).destination
        output.set_word(0, 0xCB82, 16)
        output.append_word(0xCB82)
        output = output.advance(16)
        state.set_scalar('command_queue_offset', u16(state.scalar('command_queue_offset') + 16))
        if negative_byte(members.byte()):
            break
        output.append_word(6)
        output.append_word(row_tile)
        row_tile = u16(row_tile + 128)
        output.append_word(0xC382)
        for index in range(4):
            output.append_word(0xC001)
        output.append_word(0xCB82)
        state.set_scalar('command_queue_offset', u16(state.scalar('command_queue_offset') + 16))
    for tile in (6, row_tile, 0xD380, 0xD381, 0xD381, 0xD381, 0xD381, 0xDB80):
        output.append_word(tile)
    output.put_word(0)
    state.set_scalar('command_queue_offset', u16(state.scalar('command_queue_offset') + 32))
    return output


def append_short_paired_tiles(state: GameState, destination: Cursor, tile: Long, counter: Long) -> TileRun:
    checked_state(state)
    checked_cursor(destination, state)
    uint(tile, 32)
    uint(counter, 32)
    for index in descending_inclusive(low16(counter)):
        destination.put_word(low16(tile))
        tile = replace_word(tile, u16(tile + 1))
        destination.set_word(0, low16(tile), 16)
        tile = replace_word(tile, u16(tile + 1))
        destination = destination.advance(2)
    return TileRun(destination, tile, replace_word(counter, 65535))


def append_selected_group_panel(state: GameState) -> Cursor:
    checked_state(state)
    selected = state.table(state.scalar('active_descriptor'))
    amount = read_packed_long(selected, 5)
    append_six_place_decimal_value(state, amount, 0xC386, 0xC001, state.decimal_scratch.cursor())
    amount = read_packed_long(selected, 9)
    append_six_place_decimal_value(state, amount, 0xC386, 0xC001, state.decimal_scratch.cursor(12))
    output = state.command_queue.cursor(state.scalar('command_queue_offset'))
    for tile in (15, 0xC382, 0xC380):
        output.append_word(tile)
    for index in range(13):
        output.append_word(0xC381)
    output.append_word(0xCB80)
    output.set_word(0, 15, 34)
    output.append_word(15)
    output.set_word(0, 0xC482, 34)
    output.append_word(0xC402)
    output.set_word(0, 0xC382, 34)
    output.append_word(0xC382)
    output = append_wide_paired_tiles(state, output, 0xC049, 5).destination
    output.set_word(0, 0xC001, 34)
    output.append_word(0xC001)
    digits = state.decimal_scratch.cursor()
    for index in range(6):
        output.set_word(0, digits.next_word(), 34)
        output.append_word(0xC001)
    output.set_word(0, 0xCB82, 34)
    output.append_word(0xCB82)
    output = output.advance(34)
    output.set_word(0, 15, 34)
    output.append_word(15)
    output.set_word(0, 0xC602, 34)
    output.append_word(0xC582)
    output.set_word(0, 0xC382, 34)
    output.append_word(0xC382)
    output = append_wide_paired_tiles(state, output, 0xC055, 3).destination
    for index in range(3):
        output.set_word(0, 0xC001, 34)
        output.append_word(0xC001)
    for index in range(6):
        output.set_word(0, digits.next_word(), 34)
        output.append_word(0xC001)
    output.set_word(0, 0xCB82, 34)
    output.append_word(0xCB82)
    output = output.advance(34)
    output.set_word(0, 15, 34)
    output.append_word(15)
    output.set_word(0, 0xC782, 34)
    output.append_word(0xC702)
    output.set_word(0, 0xC382, 34)
    output.append_word(0xC382)
    output = append_wide_paired_tiles(state, output, 0xC05D, 5).destination
    for index in range(5):
        output.set_word(0, 0xC001, 34)
        output.append_word(0xC001)
    selected = state.table(state.scalar('active_descriptor'))
    count = selected.byte() & 15
    tens_tile = 0xC001
    if count >= 10:
        tens_tile = 0xC387
        count = u16(count - 10)
    output.set_word(0, tens_tile, 34)
    output.append_word(0xC001)
    output.set_word(0, u16(count + 0xC386), 34)
    output.append_word(0xC001)
    output.set_word(0, 0xCB82, 34)
    output.append_word(0xCB82)
    output = output.advance(34)
    output.set_word(0, 15, 68)
    output.set_word(0, 15, 34)
    output.append_word(15)
    output.set_word(0, 0xC802, 68)
    output.set_word(0, 0xC682, 34)
    output.append_word(0xC502)
    output.set_word(0, 0xD380, 68)
    output.set_word(0, 0xC382, 34)
    output.append_word(0xC382)
    for index in range(13):
        output.set_word(0, 0xD381, 68)
        output.set_word(0, 0xC001, 34)
        output.append_word(0xC001)
    output.set_word(0, 0xDB80, 68)
    output.set_word(0, 0xCB82, 34)
    output.append_word(0xCB82)
    output.set_word(0, 0, 68)
    state.set_scalar('command_queue_offset', u16(state.scalar('command_queue_offset') + 0x154))
    return output


def append_wide_paired_tiles(state: GameState, destination: Cursor, tile: Long, counter: Long) -> TileRun:
    checked_state(state)
    checked_cursor(destination, state)
    uint(tile, 32)
    uint(counter, 32)
    for index in descending_inclusive(low16(counter)):
        destination.put_word(low16(tile))
        tile = replace_word(tile, u16(tile + 1))
        destination.set_word(0, low16(tile), 34)
        tile = replace_word(tile, u16(tile + 1))
        destination = destination.advance(2)
    return TileRun(destination, tile, replace_word(counter, 65535))


def step_candidate_selection_cursor(state: GameState) -> None:
    checked_state(state)
    controls = state.scalar('held_controls_BYTE') & 3
    if controls == 0:
        state.set_scalar('repeat_timer', 1)
        return
    delay = u16(state.scalar('repeat_timer') - 1)
    state.set_scalar('repeat_timer', delay)
    if delay != 0:
        return
    state.set_scalar('repeat_timer', 12)
    if controls & 2:
        index = u16(state.scalar('selected_candidate_index') + 1)
        if negative_byte(state.selection_members.byte(index)):
            index = 0
        state.set_scalar('selected_candidate_index', index)
    elif state.scalar('selected_candidate_index') != 0:
        state.set_scalar('selected_candidate_index', u16(state.scalar('selected_candidate_index') - 1))
    else:
        index = 0
        while not negative_byte(state.selection_members.byte(index, 1)):
            index = u16(index + 1)
        state.set_scalar('selected_candidate_index', index)


def append_candidate_selection_sprite(state: GameState) -> None:
    checked_state(state)
    if state.scalar('pressed_controls_BYTE') & 32:
        return
    controls = state.scalar('held_controls_BYTE') & 3
    if controls == 0 and state.scalar('ui_gate_flags') & 8:
        return
    x = u16(state.scalar('selected_candidate_index') * 24 + 48)
    append_live_command_string_words(state, state.candidate_cursor_shape, x, 136)


def collect_group_members_below_capacity(state: GameState) -> Word:
    checked_state(state)
    selected = state.table(state.scalar('active_descriptor'))
    count = u16((selected.byte() & 15) - 1)
    members = selected.cursor(13)
    output = state.candidate_roster.cursor()
    found = 0
    for index in descending_inclusive(count):
        member_offset = u16(members.next_byte() << 1)
        capacity = state.officer_capacity.word(member_offset)
        if capacity != state.officer_readiness.word(member_offset):
            output.append_word(member_offset >> 1)
            found = u16(found + 1)
    output.put_word(65535)
    state.set_scalar('candidate_member_count', found)
    return found


def clear_world_group_selection_marks(state: GameState) -> None:
    checked_state(state)
    state.set_scalar('saved_scroll_x', state.scalar('map_scroll_x'))
    state.set_scalar('saved_scroll_y', state.scalar('map_scroll_y'))
    group = state.group_records
    while True:
        header = group.byte() & 239
        group.set_byte(0, header)
        count = header & 15
        if count == 0:
            return
        group = group.at(count, 13)


def select_world_group_or_city_at_marker(state: GameState, marker: Word) -> WorldSelection:
    checked_state(state)
    uint(marker, 16)
    result = find_world_marker_record(state, marker)
    if result.outcome.carry:
        state.set_scalar('world_aux_flag', 0)
        scene = result.record.byte()
        state.set_scalar('selected_scene', scene)
        if scene != 50:
            offset = u16(scene * 4)
            y = state.city_world_positions.word(offset)
            x = state.city_world_positions.word(offset, 2)
            x = 0 if x < 104 else u16(x - 104)
            y = 0 if y < 152 else u16(y - 152)
            state.set_scalar('active_descriptor', 0)
            return WorldSelection(x, y, None)
    group = state.group_records
    while group.byte(0, 13) != low8(marker):
        group = group.at(group.byte() & 15, 13)
    state.set_scalar('active_descriptor', group.base)
    x = u16(group.byte(0, 1) << 4)
    state.set_scalar('selected_world_x', x)
    x = 0 if x < 104 else u16(x - 104)
    y = u16(group.byte(0, 2) << 4)
    state.set_scalar('selected_world_y', y)
    y = 0 if y < 152 else u16(y - 152)
    return WorldSelection(x, y, group)


def find_world_marker_record(state: GameState, marker: Word) -> MarkerResult:
    checked_state(state)
    uint(marker, 16)
    records = state.world_command_records.cursor(1)
    while records.next_byte() != low8(marker):
        while records.next_byte() != 0:
            pass
        # Original14D46 branches to14D3A: each packet skips its leading BYTE.
        records = records.advance(1)
    records = records.advance(1)
    if negative_byte(records.next_byte()):
        return MarkerResult(records, state.carry_result(1))
    state.set_scalar('selected_scene', 65535)
    return MarkerResult(records, state.carry_result(0))


def test_selected_group_enemy_contacts(state: GameState, stride_carrier: Word) -> CarryOutcome:
    checked_state(state)
    uint(stride_carrier, 16)
    if state.scalar('selected_scene') != 50:
        return state.carry_result(0)
    selected = state.table(state.scalar('active_descriptor'))
    count = encode_live_group_coordinate_packet(state, stride_carrier)
    if count != 0:
        return state.carry_result(0)
    state.set_scalar('adjacent_count_tick', u16(state.scalar('adjacent_count_tick') + 2))
    return state.carry_result(1)


def set_pending_group_move_position(state: GameState, direction: Word) -> WorldSelection:
    checked_state(state)
    uint(direction, 16)
    x = state.scalar('selected_world_x')
    y = state.scalar('selected_world_y')
    if direction == 1:
        x = u16(x - 16)
    elif direction == 2:
        y = u16(y + 16)
        group = state.table(state.scalar('active_descriptor'))
        group.set_byte(0, group.byte() | 128)
    elif direction == 3:
        x = u16(x + 16)
    else:
        y = u16(y - 16)
        group = state.table(state.scalar('active_descriptor'))
        group.set_byte(0, group.byte() & 127)
    state.set_scalar('pending_world_x', x)
    state.set_scalar('pending_world_y', y)
    return WorldSelection(x, y, None)


def merge_compatible_world_groups(state: GameState) -> Table:
    checked_state(state)
    selected = state.table(state.scalar('active_descriptor'))
    x = selected.byte(0, 1)
    y = selected.byte(0, 2)
    owner = selected.byte(0, 4)
    group = state.group_records
    while True:
        header = group.byte()
        if not header & 64:
            if header & 15 == 0:
                break
            if group.base != selected.base and group.byte(0, 1) == x and group.byte(0, 2) == y and group.byte(0, 4) == owner:
                if group.base < selected.base:
                    selected, group = group, selected
                merge_world_group_records(state, selected, group)
                break
        group = group.at(header & 15, 13)
    state.set_scalar('active_descriptor', selected.base)
    return selected


def merge_world_group_records(state: GameState, destination: Table, source: Table) -> Table:
    """Original live relocation, caps and do-first copies; not Python list merge."""
    checked_state(state)
    checked_table(destination, state)
    checked_table(source, state)
    source_count = source.byte() & 15
    destination_count = destination.byte() & 15
    destination.set_byte(0, u8(destination_count + source_count))
    append_at = destination.cursor(u16(destination_count + 13))
    total = u32(read_packed_long(destination, 5) + read_packed_long(source, 5))
    if total > 999999:
        total = 999999
    store_packed_long_reverse(destination, 5, total)
    total = u32(read_packed_long(destination, 9) + read_packed_long(source, 9))
    if total > 999999:
        total = 999999
    store_packed_long_reverse(destination, 9, total)
    scratch = state.group_member_scratch.cursor()
    index = 0
    while True:
        scratch.append_byte(source.byte(index, 13))
        index = u16(index + 1)
        if index >= source_count:
            break
    following = source.cursor(u16(source_count + 13))
    shifted = source.cursor(source_count)
    moving = source.cursor()
    if append_at.base != moving.base:
        while True:
            value = moving.previous_byte()
            shifted = shifted.advance(-1)
            shifted.set_byte(0, value)
            if append_at.base >= moving.base:
                break
    scratch = state.group_member_scratch.cursor()
    for index in descending_inclusive(u16(source_count - 1)):
        append_at.append_byte(scratch.next_byte())
    while True:
        count = following.byte() & 15
        if count == 0:
            break
        for index in descending_inclusive(u16(count + 12)):
            shifted.append_byte(following.next_byte())
    shifted.set_byte(0, 0)
    members = destination.cursor(13)
    count = destination.byte() & 15
    speed_sum = 0
    for index in descending_inclusive(u16(count - 1)):
        member = members.next_byte()
        speed_sum = u16(speed_sum + state.officer_march_speed.byte(member))
    average = divu_retained(speed_sum, count)
    destination.set_byte(0, low8(average), 3)
    return destination


def test_pending_group_destination(state: GameState, owner_carrier: Word = 0) -> CarryOutcome:
    checked_state(state)
    uint(owner_carrier, 16)
    x = state.scalar('pending_world_x') >> 4
    y = state.scalar('pending_world_y') >> 4
    selected = state.table(state.scalar('active_descriptor'))
    selected_count = selected.byte() & 15
    owner = (owner_carrier & 0xFF00) | selected.byte(0, 4)
    group = state.group_records
    while True:
        count = group.byte() & 15
        if count == 0:
            break
        if group.byte(0, 1) == low8(x) and group.byte(0, 2) == low8(y):
            if group.byte(0, 4) != low8(owner):
                return state.carry_result(1)
            command = state.world_command_records.at(state.scalar('world_command_offset'))
            # Original1530E BNE reaches15378, the clear-C tail.
            if command.byte(0, 1) != 0:
                return state.carry_result(0)
            if u16(count + selected_count) > 10:
                return state.carry_result(1)
            return state.carry_result(0)
        group = group.at(u16(count + 13))
    cities = state.city_locations
    for city in descending_inclusive(39):
        if cities.byte() != 0 and cities.byte(0, 1) == low8(x) and cities.byte(0, 2) == low8(y):
            relationship = state.force_relationship_bits.word(u16(owner * 2))
            city_owner = state.city_owner_bytes.byte(city)
            if low8(owner) == city_owner or relationship & (1 << (s16(city_owner if city_owner < 128 else city_owner | 0xFF00) & 31)):
                return state.carry_result(1)
            collect_blocked_cargo(state, cities)
            # Original15374 BRA reaches1537E, the set-C tail.
            return state.carry_result(1)
        cities = cities.advance(-4)
    return state.carry_result(0)


def encode_live_group_coordinate_packet(state: GameState, stride_carrier: Word) -> Word:
    """Collect adjacent opponents, preserving the original partial-byte stride.

    The incoming carrier's high BYTE survives the header's BYTE mask and is
    included in the next record's WORD stride. Do not assume it is zero: doing
    so would silently repair an original compatibility quirk.
    """
    checked_state(state)
    uint(stride_carrier, 16)
    selected = state.table(state.scalar('active_descriptor'))
    coordinate = u16((selected.byte(0, 1) << 8) | selected.byte(0, 2))
    owner = selected.byte(0, 4)
    neighbours = (u16(coordinate - 256), u16(coordinate + 1), u16(coordinate + 256), u16(coordinate - 1))
    state.adjacent_group_offsets.set_long(0, 0xFFFFFFFF)
    state.adjacent_group_offsets.set_long(0, 0xFFFFFFFF, 4)
    offset = 0
    while True:
        header = state.group_records.byte(offset)
        count = header & 15
        if count == 0:
            break
        if not state.group_records.byte(offset) & 32:
            if state.group_records.byte(offset, 4) != owner:
                other_coordinate = u16((state.group_records.byte(offset, 1) << 8) | state.group_records.byte(offset, 2))
                if other_coordinate == neighbours[0]:
                    state.adjacent_group_offsets.set_word(0, offset)
                elif other_coordinate == neighbours[1]:
                    state.adjacent_group_offsets.set_word(0, offset, 2)
                elif other_coordinate == neighbours[2]:
                    state.adjacent_group_offsets.set_word(0, offset, 4)
                elif other_coordinate == neighbours[3]:
                    state.adjacent_group_offsets.set_word(0, offset, 6)
        offset = u16(offset + 13 + ((stride_carrier & 0xFF00) | count))
    entries = state.adjacent_group_offsets.cursor()
    found = 0
    for index in range(4):
        if not negative_word(entries.next_word()):
            found = u16(found + 1)
    return found

def _sprite_compare(frame: FirstDeploymentFrame, observed, threshold, bits) -> FirstDeploymentFrame:
    """Captured AC32/AC64/ACFC CMP operands; missing legacy X stays unknown."""
    uint(observed,bits)
    uint(threshold,bits)
    if bits not in (8,16):
        raise ValueError('original sprite comparison width required')
    mask,sign = (1 << bits)-1,1 << (bits-1)
    difference = (observed-threshold) & mask
    status = None if frame.status is None else ((frame.status & 16) |
        (1 if observed<threshold else 0) | (4 if difference==0 else 0) |
        (8 if difference & sign else 0) |
        (2 if (observed ^ threshold) & (observed ^ difference) & sign else 0))
    return first_replace(frame,status=status)

def _sprite_bit(frame: FirstDeploymentFrame, attributes: Word, mask: Word) -> FirstDeploymentFrame:
    if mask not in (0x1000,0x800):
        raise ValueError('actual sprite flip bit required')
    return first_replace(frame,status=None if frame.status is None else
        ((frame.status & 27) | (0 if attributes & mask else 4)))

def _sprite_swap(frame: FirstDeploymentFrame, name: str) -> FirstDeploymentFrame:
    value = swap_words(frame.carrier(name))
    return _first_long(frame,name,value)

def _sprite_left_long_four(frame: FirstDeploymentFrame, value: Long) -> FirstDeploymentFrame:
    """ACA0 uses true LSL.L #4, before the WORD-only signed vertical shift."""
    uint(value,32)
    shifted = u32(value << 4)
    carry = bool(value & 0x10000000)
    return first_replace(frame,offset_x=shifted,status=(17 if carry else 0) |
        (8 if shifted & 0x80000000 else 0) | (4 if shifted==0 else 0))

def _sprite_signed_vertical_word(frame: FirstDeploymentFrame, value: Word) -> FirstDeploymentFrame:
    """ACA2 ASR.W #4 keeps the size bits in D5's observed upper WORD."""
    uint(value,16)
    shifted = u16(s16(value) >> 4)
    carry = bool(value & 8)
    return first_replace(frame,offset_x=replace_word(frame.offset_x,shifted),
        status=(17 if carry else 0) | (8 if shifted & 32768 else 0) | (4 if shifted==0 else 0))

def _sprite_increment_count(frame: FirstDeploymentFrame, value) -> FirstDeploymentFrame:
    uint(value,8)
    result = u8(value+1)
    return first_replace(frame,status=(17 if value==255 else 0) |
        (8 if result & 128 else 0) | (4 if result==0 else 0) | (2 if value==127 else 0))

def _sprite_finish(memory: SpritePacketMemory, frame: FirstDeploymentFrame,
        x: Word, y: Word, attributes: Word, observed, threshold, bits) -> SpritePacketFields:
    """One actual final CMP then AD00 MOVEM, never a second live read."""
    frame = memory.sync_status(_sprite_compare(frame,observed,threshold,bits))
    difference = (observed-threshold) & ((1 << bits)-1)
    sign = 1 << (bits-1)
    frame = memory.restore_scratch(frame)
    return SpritePacketFields(frame,x,y,attributes,observed<threshold,
        difference==0,bool(difference & sign),
        bool((observed ^ threshold) & (observed ^ difference) & sign)).validate(memory)

def append_live_command_sprite_packet_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame,
        x: Word, y: Word, attributes: Word, *, reset_scroll: bool, initialize_clip: bool) -> SpritePacketFields:
    """Sole AC08/AC10/AC28 clipping loop with actual fields and optional MOVEM.

    Descriptor positions, packed size, tile IDs and all clipping/count ports
    remain live DATA. The original horizontal WORD-shift loss is preserved.
    A legacy facade never invents missing high halves or a physical stack.
    """
    if type(memory) is not SpritePacketMemory:
        raise ValueError('actual sprite memory required')
    memory.frame(frame,frame.stack_cursor is not None)
    for value in (x,y,attributes):
        uint(value,16)
    if type(reset_scroll) is not bool or type(initialize_clip) is not bool:
        raise ValueError('explicit original sprite prefix choices required')
    if reset_scroll and not initialize_clip:
        raise ValueError('AC08 reset includes clipping prefix')
    state = memory.state
    if reset_scroll:
        for address in (0xFFFFF60A,0xFFFFF60E):
            state.read(address,2)
            state.write(address,2,0)
            frame = memory.sync_status(_first_memory_word(frame,0))
    if initialize_clip:
        for address,value in ((0xFFFFF302,112),(0xFFFFF304,352),(0xFFFFF306,112),(0xFFFFF308,448)):
            state.write(address,2,value)
            frame = memory.sync_status(_first_memory_word(frame,value))
    frame = memory.save_scratch(frame)
    count = state.read(0xFFFFF300,1)
    frame = memory.sync_status(_sprite_compare(frame,count,80,8))
    if count >= 80:
        return _sprite_finish(memory,frame,x,y,attributes,count,80,8)
    attributes &= 0xF800
    frame = memory.sync_status(_first_word(frame,'unit',attributes))
    frame = _first_word(frame,'count',x)
    scroll_x = state.read(0xFFFFF60A,2)
    frame = _first_sub_word(frame,'count',x,scroll_x)
    origin_x = u16(x-scroll_x)
    frame = memory.sync_status(_first_add_word(frame,'count',origin_x,128))
    origin_x = u16(origin_x+128)
    frame = _first_word(frame,'distance',y)
    scroll_y = state.read(0xFFFFF60E,2)
    frame = _first_sub_word(frame,'distance',y,scroll_y)
    origin_y = u16(y-scroll_y)
    frame = memory.sync_status(_first_add_word(frame,'distance',origin_y,128))
    origin_y = u16(origin_y+128)
    frame = _first_word(frame,'offset_x',0)
    count = state.read(0xFFFFF300,1)
    frame = _first_byte(frame,'offset_x',count)
    frame = memory.sync_status(_first_shift_word(frame,'offset_x',count,3))
    output = memory.cursor_at(0xFFFFF800,u16(count << 3))
    frame = first_replace(frame,candidates=output)
    while True:
        records = frame.roster
        coordinate_x = records.word()
        frame = _first_word(frame,'offset_x',coordinate_x)
        frame = memory.sync_status(_sprite_compare(frame,coordinate_x,32768,16))
        if coordinate_x == 32768:
            return _sprite_finish(memory,frame,x,y,attributes,coordinate_x,32768,16)
        frame = memory.sync_status(_sprite_bit(frame,attributes,0x1000))
        if attributes & 0x1000:
            packed_size = records.word(0,4)
            frame = _first_word(frame,'choice',packed_size)
            # Actual AND.L defines the upper bits; LSL.W then SWAP loses them.
            frame = _first_long(frame,'choice',packed_size)
            frame = _first_shift_word(frame,'choice',packed_size,4)
            frame = _sprite_swap(frame,'choice')
            correction = low16(frame.choice) & 3
            frame = _first_word(frame,'choice',correction)
            frame = _first_shift_word(frame,'choice',correction,3)
            correction = u16(correction << 3)
            frame = _first_add_word(frame,'choice',correction,8)
            correction = u16(correction+8)
            frame = _first_add_word(frame,'offset_x',coordinate_x,correction)
            coordinate_x = u16(coordinate_x+correction)
            frame = _first_sub_word(frame,'offset_x',0,coordinate_x)
            coordinate_x = u16(-coordinate_x)
        frame = memory.sync_status(_first_add_word(frame,'offset_x',coordinate_x,origin_x))
        coordinate_x = u16(coordinate_x+origin_x)
        minimum = state.read(0xFFFFF302,2)
        frame = memory.sync_status(_sprite_compare(frame,coordinate_x,minimum,16))
        visible_x = coordinate_x >= minimum
        if visible_x:
            maximum = state.read(0xFFFFF304,2)
            frame = memory.sync_status(_sprite_compare(frame,coordinate_x,maximum,16))
            visible_x = coordinate_x < maximum
        if visible_x:
            output.set_word(0,coordinate_x)
            frame = _first_memory_word(frame,coordinate_x)
            frame = _first_long(frame,'offset_x',0)
            packed_size = records.word(0,4)
            frame = _first_word(frame,'offset_x',packed_size)
            frame = _sprite_left_long_four(frame,packed_size)
            frame = _sprite_signed_vertical_word(frame,low16(frame.offset_x))
            packed = frame.offset_x
            coordinate_y = low16(packed)
            frame = _first_long(frame,'offset_y',packed)
            frame = memory.sync_status(_sprite_bit(frame,attributes,0x800))
            if attributes & 0x800:
                frame = _first_long(frame,'choice',packed)
                frame = _sprite_swap(frame,'choice')
                correction = low16(frame.choice) & 12
                frame = _first_word(frame,'choice',correction)
                frame = _first_shift_word(frame,'choice',correction,1)
                correction = u16(correction << 1)
                frame = _first_add_word(frame,'choice',correction,8)
                correction = u16(correction+8)
                frame = _first_add_word(frame,'offset_x',coordinate_y,correction)
                coordinate_y = u16(coordinate_y+correction)
                frame = _first_sub_word(frame,'offset_x',0,coordinate_y)
                coordinate_y = u16(-coordinate_y)
            frame = memory.sync_status(_first_add_word(frame,'offset_x',coordinate_y,origin_y))
            coordinate_y = u16(coordinate_y+origin_y)
            minimum = state.read(0xFFFFF306,2)
            frame = memory.sync_status(_sprite_compare(frame,coordinate_y,minimum,16))
            visible_y = coordinate_y >= minimum
            if visible_y:
                maximum = state.read(0xFFFFF308,2)
                frame = memory.sync_status(_sprite_compare(frame,coordinate_y,maximum,16))
                visible_y = coordinate_y < maximum
            if visible_y:
                output.set_word(0,coordinate_y,6)
                frame = _first_memory_word(frame,coordinate_y)
                frame = _sprite_swap(frame,'offset_y')
                size = low16(frame.offset_y)
                frame = _first_shift_word(frame,'offset_y',size,8)
                size = u16(size << 8)
                output.set_word(0,size,2)
                frame = _first_memory_word(frame,size)
                count = state.read(0xFFFFF300,1)
                frame = memory.sync_status(_sprite_compare(frame,count,0,8))
                if count != 0:
                    count = state.read(0xFFFFF300,1)
                    output.set_byte(0,count,-5)
                    # MOVE.B preserves X; BYTE comparison with zero has same NZVC.
                    frame = memory.sync_status(_sprite_compare(frame,count,0,8))
                count = state.read(0xFFFFF300,1)
                state.write(0xFFFFF300,1,u8(count+1))
                frame = memory.sync_status(_sprite_increment_count(frame,count))
                tile = records.word(0,2)
                frame = _first_word(frame,'offset_x',tile)
                tile = u16(tile ^ attributes)
                frame = _first_word(frame,'offset_x',tile)
                output.set_word(0,tile,4)
                frame = memory.sync_status(_first_memory_word(frame,tile))
                output = output.advance(8)
                frame = first_replace(frame,candidates=output)
        frame = first_replace(frame,roster=records.advance(6))
        count = state.read(0xFFFFF300,1)
        frame = memory.sync_status(_sprite_compare(frame,count,80,8))
        if count >= 80:
            return _sprite_finish(memory,frame,x,y,attributes,count,80,8)

def append_live_command_sprite_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame,
        *, reset_scroll: bool = True, initialize_clip: bool = True) -> FirstDeploymentFrame:
    """Complete current Scene bridge; the caller alone owns its outer JSR LONG."""
    memory.frame(frame,True)
    result = append_live_command_sprite_packet_fields(memory,frame,
        low16(frame.target_x),low16(frame.target_y),low16(frame.unit),
        reset_scroll=reset_scroll,initialize_clip=initialize_clip)
    return memory.frame(result.frame,True)


def _selected_group_panel_store_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame,
        value: Word, offset: Word = 0, *, advance: bool = False, clear: bool = False) -> FirstDeploymentFrame:
    """One layout WORD at the live A0 cursor; CLR retains its original read."""
    uint(value,16)
    uint(offset,16)
    if type(advance) is not bool or type(clear) is not bool:
        raise ValueError('explicit selected-panel write shape required')
    if clear:
        frame.roster.word(0,offset)
    frame.roster.set_word(0,value,offset)
    frame=memory.sync_status(_first_memory_word(frame,value))
    if advance:
        frame=first_replace(frame,roster=frame.roster.advance(2))
    return frame


def _selected_group_panel_cell_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame,
        far_tile: Word, near_tile: Word) -> FirstDeploymentFrame:
    """A paired row cell: lower-row WORD first, current-row WORD second."""
    frame=_selected_group_panel_store_fields(memory,frame,far_tile,34)
    return _selected_group_panel_store_fields(memory,frame,near_tile,advance=True)


def _selected_group_panel_amount_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame,
        offset: Word) -> FirstDeploymentFrame:
    """The four packed gold/rice bytes retain their ordered live reads and shifts."""
    frame=memory.sync_status(_first_byte(frame,'target_x',frame.candidates.byte(0,offset)))
    frame=memory.sync_status(_first_shift_word(frame,'target_x',low16(frame.target_x),8))
    frame=memory.sync_status(_first_byte(frame,'target_x',frame.candidates.byte(0,offset+1)))
    for displacement in (2,3):
        previous=frame.target_x
        value=u32(previous<<8)
        carry=bool(previous&(1<<24))
        status=(17 if carry else 0)|(8 if value&2147483648 else 0)|(4 if value==0 else 0)
        frame=memory.sync_status(first_replace(frame,target_x=value,status=status))
        frame=memory.sync_status(_first_byte(frame,'target_x',frame.candidates.byte(0,offset+displacement)))
    return frame


def _selected_group_panel_decimal_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Real1270A kernel result fields, not a Cursor passed off as a full frame."""
    memory.frame(frame,True)
    numeric=DecimalMemory(memory.state,frame.stack_cursor)
    digit_tile=low16(frame.target_y)
    fields=_six_place_decimal_fields(numeric,frame.target_x,digit_tile,
        low16(frame.unit),memory.cursor_at(frame.auxiliary.base))
    frame=first_replace(frame,target_x=fields.remainder,
        count=replace_word(frame.count,fields.divisor),distance=replace_word(frame.distance,fields.started),
        offset_x=replace_word(frame.offset_x,fields.glyph),auxiliary=fields.destination,
        stack_cursor=numeric.stack_cursor,status=16 if fields.glyph<digit_tile else 0)
    return memory.sync_status(_first_memory_word(frame,fields.glyph))


def append_wide_paired_tiles_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Whole14778 paired-label loop: actual D0 tile, D1 DBRA and A0 writes."""
    memory.frame(frame,True)
    for index in descending_inclusive(low16(frame.target_y)):
        frame=_selected_group_panel_store_fields(memory,frame,low16(frame.target_x))
        frame=memory.sync_status(_first_add_word(frame,'target_x',low16(frame.target_x),1))
        frame=_selected_group_panel_store_fields(memory,frame,low16(frame.target_x),34)
        frame=memory.sync_status(_first_add_word(frame,'target_x',low16(frame.target_x),1))
        frame=first_replace(frame,roster=frame.roster.advance(2),
            target_y=replace_word(frame.target_y,u16(low16(frame.target_y)-1)))
    return memory.frame(frame,True)


from ..high_level_main_flows.business_movement_support import (
    _movement_move, _movement_test, _movement_compare, _movement_fixed_shift_word,
    _movement_add_word, _movement_adjust_word, _movement_binary_flags)
from ..high_level_main_flows.contexts_gameplay import FirstDeploymentReturnBoundary


def _route_command_emit_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame, address: Long, value: Long, width: int=2, clear: bool=False) -> FirstDeploymentFrame:
    """One actual BYTE/WORD MOVE or CLR; no invented post-store arithmetic."""
    if width not in (1, 2) or type(clear) is not bool:
        raise ValueError('original route command BYTE/WORD store required')
    value &= (1 << width * 8) - 1
    if clear:
        memory.state.read(u32(address), width)
    memory.state.write(u32(address), width, value)
    return _movement_test(memory.state, frame, value, width * 8)

def _route_command_memory_delta_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame, address: Long, amount: Word, subtract: bool=False) -> FirstDeploymentFrame:
    """Original RAM-WORD RMW supplies arithmetic flags, not MOVE flags."""
    frame, value = _movement_binary_flags(memory.state, frame, memory.state.read(address, 2), amount, 16, subtract)
    memory.state.write(address, 2, value)
    return frame

def _route_command_call_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long) -> FirstDeploymentFrame:
    """Only this group's actual child calls; one physical LONG/RTS each."""
    uint(target, 32)
    uint(continuation, 32)
    allowed = ((44048, 82254), (44040, 84308), (83298, 83196), (82634, 82316), (82634, 82388), (82634, 82460), (82634, 82526), (82580, 82636), (82594, 82588))
    if (target, continuation) not in allowed:
        raise ValueError('original route/menu child and physical continuation required')
    memory.frame(frame, True)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    if target in (44040, 44048):
        returned = append_live_command_sprite_fields(memory, entered, reset_scroll=target == 44040, initialize_clip=True)
    elif target == 83298:
        returned = append_short_paired_tiles_fields(memory, entered)
    elif target == 82634:
        returned = query_route_move_cost_fields(memory, entered)
    elif target == 82580:
        returned = query_scaled_route_terrain_fields(memory, entered)
    else:
        from ..high_level_remaining_flows.business_city import terrain_cell_query_fields
        returned = terrain_cell_query_fields(memory.state, entered)
    memory.frame(returned, True)
    actual = returned.stack_cursor.long()
    if actual != continuation:
        raise FirstDeploymentReturnBoundary(actual, returned, continuation)
    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))

def append_route_selection_pair_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """14106: replace the actual sentinel with two live route coordinates."""
    memory.frame(frame, True)
    frame = first_replace(frame, roster=memory.cursor_at(4294942464))
    while True:
        value = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_test(memory.state, frame, value, 16)
        if frame.status & 8:
            break
    frame = _route_command_emit_fields(memory, frame, u32(frame.roster.base - 2), memory.state.read(4294964062, 2))
    frame = _route_command_emit_fields(memory, frame, frame.roster.base, memory.state.read(4294964064, 2))
    return _route_command_emit_fields(memory, frame, u32(frame.roster.base + 2), 65535)

def append_route_cursor_sprite_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """14120: real map-scroll cursor and the AC10 inner sprite entry."""
    from ..high_level_main_flows.business_gameplay import _map_presentation_bit_fields
    memory.frame(frame, True)
    frame = _map_presentation_bit_fields(memory.state, frame, memory.state.read(4294964001, 1), 4)
    if not frame.status & 4:
        return frame
    frame = first_replace(frame, roster=memory.cursor_at(82256))
    frame = _movement_move(memory.state, frame, 'target_x', memory.state.read(16726050, 2), 16)
    frame = _movement_move(memory.state, frame, 'target_y', memory.state.read(16726052, 2), 16)
    frame = _movement_move(memory.state, frame, 'unit', 0, 16)
    frame = _route_command_emit_fields(memory, frame, 4294964746, memory.state.read(4294963988, 2))
    frame = _route_command_emit_fields(memory, frame, 4294964750, memory.state.read(4294963992, 2))
    return _route_command_call_fields(memory, frame, 44048, 82254)

def query_scaled_route_terrain_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """14294: pixel/cell conversion around the sole actual terrain core."""
    memory.frame(frame, True)
    frame = _movement_fixed_shift_word(memory.state, frame, 'target_x', 4, True)
    frame = _movement_fixed_shift_word(memory.state, frame, 'target_y', 4, True)
    frame = _route_command_call_fields(memory, frame, 82594, 82588)
    frame = _movement_fixed_shift_word(memory.state, frame, 'target_x', 4)
    return _movement_fixed_shift_word(memory.state, frame, 'target_y', 4)

def query_route_move_cost_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """142CA: original short BSR then TST.W D3; do not substitute host cost."""
    memory.frame(frame, True)
    frame = _route_command_call_fields(memory, frame, 82580, 82636)
    return _movement_test(memory.state, frame, low16(frame.count), 16)

def step_world_route_cursor_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1416A: ordered up/right/down/left editing and original terrain budget.

    Each direction owns its actual cost BSR and retains its distinct early
    return flags. Coordinates and remaining budget are reread at the same
    stages; no preloaded host route, clipped index or fabricated cost is used.
    """
    from ..high_level_main_flows.business_gameplay import _map_presentation_bit_fields
    memory.frame(frame, True)
    state = memory.state
    frame = _movement_move(state, frame, 'distance', state.read(4294964738, 2), 16)
    selected = 0
    for mask, direction in ((1, 1), (8, 2), (2, 3), (4, 4)):
        frame = _map_presentation_bit_fields(state, frame, frame.distance, mask)
        if not frame.status & 4:
            selected = direction
            break
    if selected == 0:
        return frame
    if selected == 1:
        frame = _movement_move(state, frame, 'target_x', state.read(16726050, 2), 16)
        if frame.status & 4:
            return frame
        frame, coordinate = _movement_binary_flags(state, frame, low16(frame.target_x), 16, 16, True)
        frame = first_replace(frame, target_x=replace_word(frame.target_x, coordinate))
        frame = _movement_move(state, frame, 'target_y', state.read(16726052, 2), 16)
        continuation = 82316
    elif selected == 2:
        frame = _movement_compare(state, frame, state.read(16726052, 2), 1104, 16)
        if not frame.status & 1:
            return frame
        frame = _movement_move(state, frame, 'target_x', state.read(16726050, 2), 16)
        frame = _movement_move(state, frame, 'target_y', state.read(16726052, 2), 16)
        frame = _movement_add_word(state, frame, 'target_y', 16)
        continuation = 82388
    elif selected == 3:
        frame = _movement_compare(state, frame, state.read(16726050, 2), 1136, 16)
        if not frame.status & 1:
            return frame
        frame = _movement_move(state, frame, 'target_x', state.read(16726050, 2), 16)
        frame = _movement_add_word(state, frame, 'target_x', 16)
        frame = _movement_move(state, frame, 'target_y', state.read(16726052, 2), 16)
        continuation = 82460
    else:
        frame = _movement_move(state, frame, 'target_y', state.read(16726052, 2), 16)
        if frame.status & 4:
            return frame
        frame, coordinate = _movement_binary_flags(state, frame, low16(frame.target_y), 16, 16, True)
        frame = first_replace(frame, target_y=replace_word(frame.target_y, coordinate))
        frame = _movement_move(state, frame, 'target_x', state.read(16726050, 2), 16)
        continuation = 82526
    frame = _route_command_call_fields(memory, frame, 82634, continuation)
    frame = _movement_test(state, frame, low16(frame.count), 16)
    if frame.status & 8:
        return frame
    frame = _movement_move(state, frame, 'distance', state.read(4294964852, 2), 16)
    frame, budget = _movement_binary_flags(state, frame, low16(frame.distance), low16(frame.count), 16, True)
    frame = first_replace(frame, distance=replace_word(frame.distance, budget))
    if frame.status & 1:
        return frame
    frame = _route_command_emit_fields(memory, frame, 4294964852, low16(frame.distance))
    coordinate_address = 16726050 if selected in (1, 3) else 16726052
    coordinate_value = low16(frame.target_x) if selected in (1, 3) else low16(frame.target_y)
    frame = _route_command_emit_fields(memory, frame, coordinate_address, coordinate_value)
    frame = _movement_move(state, frame, 'target_y', selected, 16)
    frame = first_replace(frame, roster=memory.cursor_at(16726016))
    frame = _movement_move(state, frame, 'target_x', state.read(16726048, 2), 16)
    frame = _route_command_emit_fields(memory, frame, frame.roster.address(low16(frame.target_x)), low8(frame.target_y), 1)
    return _route_command_memory_delta_fields(memory, frame, 16726048, 1)

def append_short_paired_tiles_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """14562: D0 tile/D1 DBRA pair cells at the original sixteen-byte stride."""
    from ..high_level_main_flows.business_gameplay import _map_presentation_db_fields
    memory.frame(frame, True)
    while True:
        frame = _selected_group_panel_store_fields(memory, frame, low16(frame.target_x))
        frame = _movement_adjust_word(memory.state, frame, 'target_x', 1)
        frame = _selected_group_panel_store_fields(memory, frame, low16(frame.target_x), 16)
        frame = _movement_adjust_word(memory.state, frame, 'target_x', 1)
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame, more = _map_presentation_db_fields(frame, 'target_y')
        if not more:
            return frame

def append_candidate_member_panel_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """14494: complete live candidate rows, paired glyphs, blanks and borders.

    A1 is the real member stream; all queue-offset RMWs and the final CLR bus
    read remain ordered. The glyph helper owns only its original14562 BSR slot.
    Artwork stays in external assets; these constants are original tile IDs.
    """
    from ..high_level_main_flows.business_gameplay import _map_presentation_db_fields
    memory.frame(frame, True)
    state = memory.state
    frame = first_replace(frame, roster=memory.cursor_at(4294955264))
    frame = first_replace(frame, roster=frame.roster.advance(s16(state.read(4294963994, 2))))
    for tile in (6, 49954, 50048, 50049, 50049, 50049, 50049, 52096):
        frame = _selected_group_panel_store_fields(memory, frame, tile, advance=True)
    frame = first_replace(frame, candidates=memory.cursor_at(16726320))
    frame = _movement_move(state, frame, 'unit', 50082, 16)
    while True:
        frame = _selected_group_panel_store_fields(memory, frame, 6, 16)
        frame = _selected_group_panel_store_fields(memory, frame, 6, advance=True)
        frame = _selected_group_panel_store_fields(memory, frame, low16(frame.unit))
        frame = _movement_add_word(state, frame, 'unit', 128)
        frame = _selected_group_panel_store_fields(memory, frame, low16(frame.unit), 16)
        frame = _movement_add_word(state, frame, 'unit', 128)
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _selected_group_panel_store_fields(memory, frame, 50050, 16)
        frame = _selected_group_panel_store_fields(memory, frame, 50050, advance=True)
        frame = _movement_move(state, frame, 'target_x', 0, 16)
        frame = _movement_move(state, frame, 'target_x', frame.candidates.byte(), 8)
        frame = first_replace(frame, candidates=frame.candidates.advance(1))
        frame = _movement_fixed_shift_word(state, frame, 'target_x', 3)
        frame = _movement_add_word(state, frame, 'target_x', 49177)
        frame = _movement_move(state, frame, 'target_y', 3, 16)
        frame = _route_command_call_fields(memory, frame, 83298, 83196)
        frame = _selected_group_panel_store_fields(memory, frame, 52098, 16)
        frame = _selected_group_panel_store_fields(memory, frame, 52098, advance=True)
        frame = first_replace(frame, roster=frame.roster.advance(16))
        frame = _route_command_memory_delta_fields(memory, frame, 4294963994, 16)
        frame = _movement_test(state, frame, frame.candidates.byte(), 8)
        if frame.status & 8:
            break
        frame = _selected_group_panel_store_fields(memory, frame, 6, advance=True)
        frame = _selected_group_panel_store_fields(memory, frame, low16(frame.unit), advance=True)
        frame = _movement_add_word(state, frame, 'unit', 128)
        frame = _selected_group_panel_store_fields(memory, frame, 50050, advance=True)
        frame = _movement_move(state, frame, 'target_x', 3, 16)
        while True:
            frame = _selected_group_panel_store_fields(memory, frame, 49153, advance=True)
            frame, more = _map_presentation_db_fields(frame, 'target_x')
            if not more:
                break
        frame = _selected_group_panel_store_fields(memory, frame, 52098, advance=True)
        frame = _route_command_memory_delta_fields(memory, frame, 4294963994, 16)
    for tile in (6, low16(frame.unit), 54144, 54145, 54145, 54145, 54145, 56192):
        frame = _selected_group_panel_store_fields(memory, frame, tile, advance=True)
    frame = _selected_group_panel_store_fields(memory, frame, 0, clear=True)
    return _route_command_memory_delta_fields(memory, frame, 4294963994, 32)

def step_candidate_selection_cursor_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """148A4: original repeat timer and sentinel-defined cyclic member selection."""
    from ..high_level_main_flows.business_gameplay import _map_presentation_bit_fields
    memory.frame(frame, True)
    state = memory.state
    frame = _movement_move(state, frame, 'target_x', state.read(4294964738, 1), 8)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 3, 16)
    if frame.status & 4:
        return _route_command_emit_fields(memory, frame, 4294964744, 1)
    frame = _route_command_memory_delta_fields(memory, frame, 4294964744, 1, True)
    if not frame.status & 4:
        return frame
    frame = _route_command_emit_fields(memory, frame, 4294964744, 12)
    frame = _map_presentation_bit_fields(state, frame, frame.target_x, 2)
    if not frame.status & 4:
        frame = _movement_move(state, frame, 'target_x', state.read(4294964854, 2), 16)
        frame = _movement_adjust_word(state, frame, 'target_x', 1)
        frame = first_replace(frame, roster=memory.cursor_at(16726320))
        frame = _movement_test(state, frame, frame.roster.byte(low16(frame.target_x)), 8)
        if frame.status & 8:
            return _route_command_emit_fields(memory, frame, 4294964854, 0, clear=True)
        return _route_command_emit_fields(memory, frame, 4294964854, low16(frame.target_x))
    frame = _movement_test(state, frame, state.read(4294964854, 2), 16)
    if not frame.status & 4:
        return _route_command_memory_delta_fields(memory, frame, 4294964854, 1, True)
    frame = first_replace(frame, roster=memory.cursor_at(16726320))
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    while True:
        frame = _movement_test(state, frame, frame.roster.byte(low16(frame.target_x), 1), 8)
        if frame.status & 8:
            return _route_command_emit_fields(memory, frame, 4294964854, low16(frame.target_x))
        frame = _movement_adjust_word(state, frame, 'target_x', 1)

def append_candidate_selection_sprite_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """14914: actual selection/held flags, WORD position arithmetic and AC08."""
    from ..high_level_main_flows.business_gameplay import _map_presentation_bit_fields
    memory.frame(frame, True)
    state = memory.state
    frame = _map_presentation_bit_fields(state, frame, state.read(4294964739, 1), 32)
    if not frame.status & 4:
        return frame
    frame = _movement_move(state, frame, 'target_x', state.read(4294964738, 1), 8)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 3, 16)
    if frame.status & 4:
        frame = _map_presentation_bit_fields(state, frame, state.read(4294964001, 1), 8)
        if not frame.status & 4:
            return frame
    frame = first_replace(frame, roster=memory.cursor_at(84310))
    frame = _movement_move(state, frame, 'target_x', state.read(4294964854, 2), 16)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
    frame = _movement_add_word(state, frame, 'target_x', low16(frame.target_y))
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 3)
    frame = _movement_add_word(state, frame, 'target_x', 48)
    frame = _movement_move(state, frame, 'target_y', 136, 16)
    frame = _movement_move(state, frame, 'unit', 0, 16)
    return _route_command_call_fields(memory, frame, 44040, 84308)

def collect_group_members_below_capacity_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """149A0: compare each actual member's capacity/readiness and emit a roster.

    Zero member nibble keeps the original65536-iteration DBRA expansion; no
    Python empty-list replacement is introduced. All D high WORDs, A4..A7
    and final MOVE count flags survive exactly through the shared real helpers.
    """
    from ..high_level_main_flows.business_gameplay import _map_presentation_db_fields
    memory.frame(frame, True)
    state = memory.state
    frame = first_replace(frame, roster=memory.cursor_at(4294946816), candidates=memory.cursor_at(4294947328), controller=memory.cursor_at(state.read(16726060, 4)))
    frame = _movement_move(state, frame, 'unit', frame.controller.byte(), 8)
    frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 15, 16)
    frame = _movement_adjust_word(state, frame, 'unit', -1)
    frame = first_replace(frame, controller=frame.controller.advance(13), scan=memory.cursor_at(4294964480))
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    while True:
        frame = _movement_move(state, frame, 'target_y', 0, 16)
        frame = _movement_move(state, frame, 'target_y', frame.controller.byte(), 8)
        frame = first_replace(frame, controller=frame.controller.advance(1))
        frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
        frame = _movement_move(state, frame, 'count', frame.roster.word(low16(frame.target_y)), 16)
        frame = _movement_compare(state, frame, low16(frame.count), frame.candidates.word(low16(frame.target_y)), 16)
        if not frame.status & 4:
            frame = _movement_fixed_shift_word(state, frame, 'target_y', 1, True)
            frame = _route_command_emit_fields(memory, frame, frame.scan.base, low16(frame.target_y))
            frame = first_replace(frame, scan=frame.scan.advance(2))
            frame = _movement_adjust_word(state, frame, 'target_x', 1)
        frame, more = _map_presentation_db_fields(frame, 'unit')
        if not more:
            break
    frame = _route_command_emit_fields(memory, frame, frame.scan.base, 65535)
    return _route_command_emit_fields(memory, frame, 4294964790, low16(frame.target_x))

def clear_world_group_selection_marks_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """14C7C: save scroll and remove bit4 from every actual packed header."""
    from ..high_level_main_flows.business_gameplay import _map_presentation_bit_fields
    memory.frame(frame, True)
    state = memory.state
    frame = _route_command_emit_fields(memory, frame, 4294964054, state.read(4294963988, 2))
    frame = _route_command_emit_fields(memory, frame, 4294964052, state.read(4294963992, 2))
    frame = first_replace(frame, roster=memory.cursor_at(4294938624))
    while True:
        frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)
        frame = _map_presentation_bit_fields(state, frame, frame.target_x, 16)
        frame = first_replace(frame, target_x=frame.target_x & ~16)
        frame = _route_command_emit_fields(memory, frame, frame.roster.base, low8(frame.target_x), 1)
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
        if frame.status & 4:
            return frame
        frame = first_replace(frame, roster=frame.roster.advance(s16(low16(frame.target_x)) + 13))

def execute_city_group_display_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame, target: Long) -> FirstDeploymentFrame:
    """Closed complete group-command entries; the actual caller owns its LONG."""
    uint(target, 32)
    memory.frame(frame, True)
    children = {82182: append_route_selection_pair_fields, 82208: append_route_cursor_sprite_fields, 82282: step_world_route_cursor_fields, 82580: query_scaled_route_terrain_fields, 82634: query_route_move_cost_fields, 83092: append_candidate_member_panel_fields, 83298: append_short_paired_tiles_fields, 84132: step_candidate_selection_cursor_fields, 84244: append_candidate_selection_sprite_fields, 84384: collect_group_members_below_capacity_fields, 85116: clear_world_group_selection_marks_fields}
    if target not in children:
        raise ValueError('closed full-frame route/candidate software entry required')
    return children[target](memory, frame)


def _selected_group_panel_call_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame,
        target: Long, continuation: Long) -> FirstDeploymentFrame:
    """Two real inner callees only; physical LONG enters and actual RTS reads."""
    memory.frame(frame,True)
    call=DecimalMemory(memory.state,frame.stack_cursor)
    call.enter_call(continuation)
    entered=first_replace(frame,stack_cursor=call.stack_cursor)
    if target==75530:
        result=_selected_group_panel_decimal_fields(memory,entered)
    elif target==83832:
        result=append_wide_paired_tiles_fields(memory,entered)
    else:
        raise ValueError('selected panel has no other declared child target')
    call.stack_cursor=result.stack_cursor
    call.leave_call(continuation)
    return first_replace(result,stack_cursor=call.stack_cursor)


def _selected_group_panel_blank_cells_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame,
        counter: Word) -> FirstDeploymentFrame:
    """Fixed blank cells, preserving the genuine D0 low-WORD DBRA residue."""
    frame=memory.sync_status(_first_word(frame,'target_x',counter))
    for index in descending_inclusive(low16(frame.target_x)):
        frame=_selected_group_panel_cell_fields(memory,frame,0xC001,0xC001)
        frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
    return frame


def _selected_group_panel_digits_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Six live scratch glyphs; A1 advances rather than copying a guessed result."""
    frame=memory.sync_status(_first_word(frame,'target_x',5))
    for index in descending_inclusive(low16(frame.target_x)):
        glyph=frame.candidates.word()
        frame=first_replace(frame,candidates=frame.candidates.advance(2))
        frame=_selected_group_panel_cell_fields(memory,frame,glyph,0xC001)
        frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
    return frame


def append_selected_group_panel_fields(memory: SpritePacketMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Whole14574: gold/rice six-digit rows, member count and complete panel border.

    SpritePacketMemory is only the existing true Scene/live-cursor ABI bridge;
    no sprite clipping or legacy GameState/TileRun facade is called. Incoming
    upper halves and untouched A/D fields survive each original-width operation.
    """
    memory.frame(frame,True)
    state=memory.state
    frame=first_replace(frame,candidates=memory.cursor_at(state.read(0xFF382C,4)))
    frame=_selected_group_panel_amount_fields(memory,frame,5)
    frame=memory.sync_status(_first_word(frame,'target_y',0xC386))
    frame=memory.sync_status(_first_word(frame,'unit',0xC001))
    frame=first_replace(frame,auxiliary=memory.cursor_at(0xFFFFD300))
    frame=_selected_group_panel_call_fields(memory,frame,75530,83362)
    frame=_selected_group_panel_amount_fields(memory,frame,9)
    frame=first_replace(frame,auxiliary=memory.cursor_at(0xFFFFD30C))
    frame=_selected_group_panel_call_fields(memory,frame,75530,83394)
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFFD100))
    queue_offset=state.read(0xFFFFF31A,2)
    frame=first_replace(frame,roster=frame.roster.advance(s16(queue_offset)))
    for tile in (15,0xC382,0xC380):
        frame=_selected_group_panel_store_fields(memory,frame,tile,advance=True)
    frame=memory.sync_status(_first_word(frame,'target_x',12))
    for index in descending_inclusive(low16(frame.target_x)):
        frame=_selected_group_panel_store_fields(memory,frame,0xC381,advance=True)
        frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
    frame=_selected_group_panel_store_fields(memory,frame,0xCB80,advance=True)
    for far_tile,near_tile in ((15,15),(0xC482,0xC402),(0xC382,0xC382)):
        frame=_selected_group_panel_cell_fields(memory,frame,far_tile,near_tile)
    frame=memory.sync_status(_first_word(frame,'target_x',0xC049))
    frame=memory.sync_status(_first_word(frame,'target_y',5))
    frame=_selected_group_panel_call_fields(memory,frame,83832,83472)
    frame=_selected_group_panel_cell_fields(memory,frame,0xC001,0xC001)
    frame=first_replace(frame,candidates=memory.cursor_at(0xFFFFD300))
    frame=_selected_group_panel_digits_fields(memory,frame)
    frame=_selected_group_panel_cell_fields(memory,frame,0xCB82,0xCB82)
    frame=first_replace(frame,roster=frame.roster.advance(34))
    for far_tile,near_tile in ((15,15),(0xC602,0xC582),(0xC382,0xC382)):
        frame=_selected_group_panel_cell_fields(memory,frame,far_tile,near_tile)
    frame=memory.sync_status(_first_word(frame,'target_x',0xC055))
    frame=memory.sync_status(_first_word(frame,'target_y',3))
    frame=_selected_group_panel_call_fields(memory,frame,83832,83558)
    frame=_selected_group_panel_blank_cells_fields(memory,frame,2)
    frame=_selected_group_panel_digits_fields(memory,frame)
    frame=_selected_group_panel_cell_fields(memory,frame,0xCB82,0xCB82)
    frame=first_replace(frame,roster=frame.roster.advance(34))
    for far_tile,near_tile in ((15,15),(0xC782,0xC702),(0xC382,0xC382)):
        frame=_selected_group_panel_cell_fields(memory,frame,far_tile,near_tile)
    frame=memory.sync_status(_first_word(frame,'target_x',0xC05D))
    frame=memory.sync_status(_first_word(frame,'target_y',5))
    frame=_selected_group_panel_call_fields(memory,frame,83832,83648)
    frame=_selected_group_panel_blank_cells_fields(memory,frame,4)
    frame=memory.sync_status(_first_word(frame,'target_x',0xC001))
    frame=first_replace(frame,controller=memory.cursor_at(state.read(0xFF382C,4)))
    frame=memory.sync_status(_first_word(frame,'unit',0))
    frame=memory.sync_status(_first_byte(frame,'unit',frame.controller.byte()))
    frame=memory.sync_status(_first_word(frame,'unit',low16(frame.unit)&15))
    frame=memory.sync_status(_sprite_compare(frame,low16(frame.unit),10,16))
    if not frame.status&1:
        frame=memory.sync_status(_first_word(frame,'target_x',0xC387))
        frame=memory.sync_status(_first_sub_word(frame,'unit',low16(frame.unit),10))
    frame=_selected_group_panel_cell_fields(memory,frame,low16(frame.target_x),0xC001)
    frame=memory.sync_status(_first_add_word(frame,'unit',low16(frame.unit),0xC386))
    frame=_selected_group_panel_cell_fields(memory,frame,low16(frame.unit),0xC001)
    frame=_selected_group_panel_cell_fields(memory,frame,0xCB82,0xCB82)
    frame=first_replace(frame,roster=frame.roster.advance(34))
    for bottom,middle,top in ((15,15,15),(0xC802,0xC682,0xC502),(0xD380,0xC382,0xC382)):
        frame=_selected_group_panel_store_fields(memory,frame,bottom,68)
        frame=_selected_group_panel_store_fields(memory,frame,middle,34)
        frame=_selected_group_panel_store_fields(memory,frame,top,advance=True)
    frame=memory.sync_status(_first_word(frame,'target_x',12))
    for index in descending_inclusive(low16(frame.target_x)):
        frame=_selected_group_panel_store_fields(memory,frame,0xD381,68)
        frame=_selected_group_panel_store_fields(memory,frame,0xC001,34)
        frame=_selected_group_panel_store_fields(memory,frame,0xC001,advance=True)
        frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
    frame=_selected_group_panel_store_fields(memory,frame,0xDB80,68)
    frame=_selected_group_panel_store_fields(memory,frame,0xCB82,34)
    frame=_selected_group_panel_store_fields(memory,frame,0xCB82,advance=True)
    frame=_selected_group_panel_store_fields(memory,frame,0,68,clear=True)
    previous=state.read(0xFFFFF31A,2)
    state.write(0xFFFFF31A,2,u16(previous+0x154))
    # Reuse arithmetic CCR without modifying any D carrier for memory ADDI.
    changed=_first_add_word(frame,'target_x',previous,0x154)
    frame=memory.sync_status(first_replace(changed,target_x=frame.target_x))
    return memory.frame(frame,True)
