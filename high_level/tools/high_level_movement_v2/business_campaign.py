"""Live campaign movement packets, destinations and neighbor capacity.

Rules keep the original fixed widths and live source aliases. No asset loader,
CPU state dictionary or implicit natural-domain bounds are part of this layer.
"""
from .domain import (GameState, Table, Cursor, Word, Byte, CarryOutcome,
                     uint, u8, u16, low8, replace_byte, s8, negative_word,
                     descending_inclusive, checked_state, checked_cursor)
from .business_path import build_path


def prepare_transport_path(state: GameState) -> None:
    """Set transport endpoints/budget, find the path, and enter transport mode."""
    state = checked_state(state)
    offset = u16(state.transport_index() << 2)
    records = state.transport_records
    budget = 15
    kind = records.byte(offset) & 3
    if kind == 3:
        budget = 10
    state.set_transport_budget(budget)
    state.set_path_origin_x(u16(records.byte(offset, 1) << 4))
    state.set_path_origin_y(u16(records.byte(offset, 2) << 4))
    destination = u16(records.byte(offset, 3) << 2)
    coordinates = state.city_coordinates
    state.set_path_target_x(coordinates.word(destination, 2))
    state.set_path_target_y(coordinates.word(destination))
    build_path(state)
    state.set_route(522)
    state.set_stage(1)
    state.set_transport_progress(0)
    return None


def ensure_neighbor_capacity(state: GameState) -> None:
    """Keep or choose a packed-coordinate neighbor whose group has capacity."""
    state = checked_state(state)
    capacity = selected_roster_capacity(state)
    mode_offset = u16((state.neighbor_mode() & 3) << 1)
    selected = state.neighbor_selected_slots.at(mode_offset)
    pointer = state.neighbor_source_pointers.long(u16(mode_offset << 1))
    source_head = state.table(pointer).word()
    if not negative_word(selected.word()):
        group = find_group_at_coordinate(state, selected.word())
        combined = u8((group.byte() & 15) + low8(capacity))
        if combined <= 10:
            return None
    count = collect_six_neighbor_candidates(state)
    count = filter_neighbor_candidates(state, count, source_head)
    if count == 0:
        return None
    candidates = state.neighbor_candidates.cursor()
    for remaining in descending_inclusive(u16(count - 1)):
        coordinate = candidates.next_word()
        if not negative_word(coordinate):
            selected.set_word(0, coordinate)
            return None
    candidates = state.neighbor_candidates.cursor()
    for remaining in descending_inclusive(u16(count - 1)):
        coordinate = candidates.next_word() & 32767
        group = find_group_at_coordinate(state, coordinate)
        combined = u8((group.byte() & 15) + low8(capacity))
        if combined <= 10:
            selected.set_word(0, coordinate)
            return None
    selected.set_word(0, 65535)
    return None


def find_group_at_coordinate(state: GameState, coordinate: Word) -> Table:
    """Return a live packed-group view, or the true zero-header sentinel view."""
    state = checked_state(state)
    coordinate = uint(coordinate, 16)
    x = coordinate >> 8
    y = low8(coordinate)
    group = state.group_packets
    while True:
        members = group.byte() & 15
        if members == 0:
            return group
        if group.byte(0, 1) == x:
            if group.byte(0, 2) == y:
                return group
        group = group.advance(13 + members)


def collect_six_neighbor_candidates(state: GameState) -> Word:
    """Append six source-valid neighbors in the original incremental order."""
    state = checked_state(state)
    output = state.neighbor_candidates.cursor()
    count = 0
    city_offset = u16(state.neighbor_city() << 2)
    coordinates = state.city_coordinates
    x = coordinates.word(city_offset, 2) >> 4
    y = coordinates.word(city_offset) >> 4
    x = u16(x - 1)
    y = u16(y - 1)
    for dx, dy in ((0, 0), (0, 1), (1, 1), (1, -1), (0, -1), (-1, -1)):
        x = u16(x + dx)
        y = u16(y + dy)
        cost = read_neighbor_source_cost(state, x, y)
        if s8(cost) >= 0:
            coordinate = u16((low8(x) << 8) | low8(y))
            output.append_word(coordinate)
            count = u16(count + 1)
    return count


def filter_neighbor_candidates(state: GameState, count: Word, source_head: Word) -> Word:
    """Mark matching groups and shift out foreign-head candidates, live in place."""
    state = checked_state(state)
    count = uint(count, 16)
    source_head = uint(source_head, 16)
    group = state.group_packets
    candidates = state.neighbor_candidates_prefix
    while True:
        members = group.byte() & 15
        if members == 0:
            return count
        coordinate = u16((group.byte(0, 1) << 8) | group.byte(0, 2))
        position = u16(count << 1)
        matched = False
        while True:
            if candidates.word(position) == coordinate:
                matched = True
                break
            position = u16(position - 2)
            if position == 0:
                break
        if matched:
            if group.byte(0, 4) == low8(source_head):
                candidates.set_word(position, candidates.word(position) | 32768)
            else:
                count = u16(count - 1)
                if count == 0:
                    return count
                limit = u16(count << 1)
                while True:
                    candidates.set_word(position, candidates.word(position, 2))
                    position = u16(position + 2)
                    if position >= limit:
                        break
        group = group.advance(13 + members)


def selected_roster_capacity(state: GameState) -> Word:
    """Count selected live rosters, cap ten, or return the single-slot fallback."""
    state = checked_state(state)
    if state.neighbor_mode_low() & 1:
        return 1
    if state.neighbor_mode_low() & 2:
        offset = u16(state.neighbor_city() << 1)
        if state.city_heads.word(offset) != state.selected_officer():
            return 1
        primary = state.city_primary_roster.cursor()
        secondary = state.city_secondary_roster.cursor()
    else:
        city = state.neighbor_city()
        if state.neighbor_city_flags.byte(city) != state.selected_officer():
            return 1
        primary = state.primary_roster.cursor()
        secondary = state.secondary_roster.cursor()
    count = 0
    while not negative_word(primary.next_word()):
        count = u16(count + 1)
    while not negative_word(secondary.next_word()):
        count = u16(count + 1)
    if count > 10:
        count = 10
    return count


def read_neighbor_source_cost(state: GameState, x: Word, y: Word) -> Byte:
    """Read both live sources at the same signed grid index; return the second."""
    state = checked_state(state)
    x = uint(x, 16)
    y = uint(y, 16)
    index = u16(u16(u16(x << 3) + x) << 3)
    index = u16(index + y)
    state.terrain_sources.byte(index)
    return state.terrain_costs.byte(index)


def build_ai_movement_packet(state: GameState) -> None:
    """Search the chosen destination and append an original queue command."""
    state = checked_state(state)
    state.set_path_origin_x(state.ai_origin_x())
    state.set_path_origin_y(state.ai_origin_y())
    coordinates = state.city_coordinates
    city_offset = u16(state.chosen_city() << 2)
    state.set_path_target_x(coordinates.word(city_offset, 2))
    state.set_path_target_y(coordinates.word(city_offset))
    path = build_path(state)
    output = state.movement_queue.cursor(state.movement_queue_offset())
    output.append_byte(0)
    output.append_byte(state.ai_packet_marker())
    output.append_byte(state.ai_budget_low())
    append_ai_path_steps(state, output, path.retained_direction)
    return None


def append_ai_path_steps(state: GameState, output: Cursor, retained_direction: Word) -> None:
    """Charge path steps from the low budget BYTE, preserving direction WORD bits."""
    state = checked_state(state)
    retained_direction = uint(retained_direction, 16)
    output = checked_cursor(output, state)
    budget = state.ai_budget()
    x = state.ai_origin_x() >> 4
    y = state.ai_origin_y() >> 4
    packet_bytes = 4
    sources = state.terrain_sources
    costs = state.terrain_costs
    path = state.world_path_steps.cursor()
    direction = retained_direction
    while True:
        step = path.next_byte()
        direction = u16(replace_byte(direction, step))
        if s8(step) < 0:
            break
        vector_offset = u16(direction << 2)
        vectors = state.group_step_vectors
        x = u16(x + vectors.word(vector_offset))
        y = u16(y + vectors.word(vector_offset, 2))
        direction = vector_offset >> 2
        cost = read_path_step_cost(state, x, y, sources, costs)
        old_budget = low8(budget)
        budget = u16(replace_byte(budget, u8(old_budget - cost)))
        if old_budget < cost:
            break
        packet_bytes = u16(packet_bytes + 1)
        output.append_byte(low8(direction))
        if low8(budget) == 0:
            break
    output.set_byte(0, 0)
    output.set_byte(0, 255, 1)
    state.set_movement_queue_offset(u16(state.movement_queue_offset() + packet_bytes))
    return None


def read_path_step_cost(state: GameState, x: Word, y: Word,
                        sources: Table, costs: Table) -> Byte:
    """Read terrain at the wrapped signed grid index, then cost by its full BYTE."""
    state = checked_state(state)
    x = uint(x, 16)
    y = uint(y, 16)
    sources = state.checked_table(sources)
    costs = state.checked_table(costs)
    index = u16(u16(u16(x << 3) + x) << 3)
    index = u16(index + y)
    terrain = sources.byte(index)
    return costs.byte(terrain)


def choose_ai_destination(state: GameState) -> None:
    """Choose a strictly shorter eligible friendly-city path, visiting cities backwards."""
    state = checked_state(state)
    group = state.group_packets.at(state.ai_group_index())
    budget = group.byte(0, 3)
    x = group.byte(0, 1)
    state.set_path_origin_x(u16(x << 4))
    y = group.byte(0, 2)
    state.set_path_origin_y(u16(y << 4))
    owners = state.city_owner_slots
    coordinates = state.following_city_coordinates
    best = 65535
    state.set_chosen_city(65535)
    for city in descending_inclusive(39):
        if owners.byte(city) != state.current_force():
            continue
        if city_roster_full_carry(state, city).carry:
            continue
        offset = u16(city << 2)
        target_x = coordinates.word(offset, 2)
        state.set_path_target_x(target_x)
        target_x = target_x >> 4
        dx = u16(target_x - x)
        if target_x < x:
            dx = u16(-dx)
        if dx > budget:
            continue
        target_y = coordinates.word(offset)
        state.set_path_target_y(target_y)
        target_y = target_y >> 4
        dy = u16(target_y - y)
        if target_y < y:
            dy = u16(-dy)
        distance = u16(dx + dy)
        if distance > budget:
            continue
        path = build_path(state)
        owners = path.final_frontier_cursor
        coordinates = path.final_grid
        if best > state.path_length():
            best = state.path_length()
            state.set_chosen_city(city)
    return None


def city_roster_full_carry(state: GameState, city: Word) -> CarryOutcome:
    """Return the original privileged carry outcome after the full BYTE roster scan."""
    state = checked_state(state)
    city = uint(city, 16)
    assignment = u16(city + 1)
    count = 0
    for officer in descending_inclusive(255):
        if state.officer_assignments.byte(officer) == low8(assignment):
            count = u16(count + 1)
    if count >= 10:
        return state.carry_result(1)
    return state.carry_result(0)

