"""Live weighted frontier search and reverse direction reconstruction.

Coordinate roles are neutral first/second. WORD wrapping and signed indexed
views are explicit compatibility, not a 72-cell API clamp. Unreachable targets
can exhaust the caller's DATA budget; no fabricated successful path is returned.
"""
from .domain import (
    GameState, Word, Table, Cursor, PathCoordinates, PathResult, FrontierResult,
    CarryOutcome, NeighborResult, uint, u8, u16, low8, s8, negative_byte,
    descending_inclusive, checked_state, checked_cursor,
)


def build_path(state: GameState) -> PathResult:
    checked_state(state)
    normalize_path_coordinates(state)
    return build_path_from_cells(state)


def build_path_from_cells(state: GameState) -> PathResult:
    checked_state(state)
    initialize_path_grid(state)
    first_buffer = state.path_frontier
    second_buffer = state.alternate_frontier
    source = first_buffer.cursor()
    source.append_byte(state.path_source_first_tail())
    source.append_byte(state.path_source_second_tail())
    source.append_byte(1)
    source.append_byte(255)
    length = u16(0)
    retained_direction = u16(0)
    while True:
        source = first_buffer.cursor()
        output = second_buffer.cursor()
        outcome = expand_path_frontier(state, source, output, retained_direction)
        retained_direction = outcome.retained_direction
        if outcome.carry == 1:
            break
        first_buffer, second_buffer = second_buffer, first_buffer
        length = u16(length + 1)
    length = u16(length + 1)
    state.set_path_length(length)
    coordinates = reconstruct_path(state)
    return PathResult(length, retained_direction, coordinates, output, state.path_grid)


def initialize_path_grid(state: GameState) -> None:
    checked_state(state)
    grid = state.path_grid.cursor()
    terrain = state.terrain_sources.cursor()
    costs = state.terrain_costs
    for remaining in descending_inclusive(u16(5183)):
        terrain_kind = u16(terrain.next_byte())
        cost = u16(costs.byte(terrain_kind))
        grid.append_word(cost)
    grid = state.path_grid
    objects = state.transport_records
    for remaining in descending_inclusive(u16(39)):
        if objects.byte() != 0:
            if objects.byte() & 16 == 0:
                first = u16(objects.byte(0, 1))
                offset = u16(u16(u16(first << 3) + first) << 3)
                second = u16(objects.byte(0, 2))
                offset = u16(u16(offset + second) << 1)
                grid.set_word(offset, 127)
        objects = objects.advance(4)
    objects = state.group_packets
    while True:
        size = u16(objects.byte() & 15)
        if size == 0:
            break
        first = u16(objects.byte(0, 1))
        offset = u16(u16(u16(first << 3) + first) << 3)
        second = u16(objects.byte(0, 2))
        offset = u16(u16(offset + second) << 1)
        grid.set_word(offset, 127)
        objects = objects.at(size, 13)
    coordinates = state.following_city_coordinates.cursor()
    for remaining in descending_inclusive(u16(39)):
        first = u16(coordinates.next_word() >> 4)
        second = u16(coordinates.next_word() >> 4)
        offset = u16(u16(u16(second << 3) + second) << 3)
        offset = u16(u16(offset + first) << 1)
        grid.set_word(offset, 255, -2)
        grid.set_word(offset, 255)


def normalize_path_coordinates(state: GameState) -> None:
    checked_state(state)
    state.set_path_destination_first(u16(state.path_destination_first() >> 4))
    state.set_path_destination_second(u16(state.path_destination_second() >> 4))
    state.set_path_source_first(u16(state.path_source_first() >> 4))
    state.set_path_source_second(u16(state.path_source_second() >> 4))


def expand_path_frontier(state: GameState, source: Cursor, output: Cursor, retained_direction: Word) -> FrontierResult:
    checked_state(state)
    checked_cursor(source, state)
    checked_cursor(output, state)
    retained_direction = uint(retained_direction, 16)
    while True:
        first = u16(source.next_byte())
        second = u16(source.next_byte())
        countdown = u8(source.next_byte() - 1)
        if countdown != 0:
            output.append_byte(low8(first))
            output.append_byte(low8(second))
            output.append_byte(countdown)
        else:
            borrowed = first == 0
            first = u16(first - 1)
            if not borrowed:
                retained_direction = u16(3)
                outcome = visit_path_neighbor(state, first, second, retained_direction, output)
                first, second = outcome.coordinates.first, outcome.coordinates.second
                if outcome.carry == 1:
                    return FrontierResult(1, retained_direction, PathCoordinates(first, second))
            first = u16(first + 1)
            borrowed = second == 0
            second = u16(second - 1)
            if not borrowed:
                retained_direction = u16(2)
                outcome = visit_path_neighbor(state, first, second, retained_direction, output)
                first, second = outcome.coordinates.first, outcome.coordinates.second
                if outcome.carry == 1:
                    return FrontierResult(1, retained_direction, PathCoordinates(first, second))
            second = u16(second + 2)
            if second < 72:
                retained_direction = u16(4)
                outcome = visit_path_neighbor(state, first, second, retained_direction, output)
                first, second = outcome.coordinates.first, outcome.coordinates.second
                if outcome.carry == 1:
                    return FrontierResult(1, retained_direction, PathCoordinates(first, second))
            first = u16(first + 1)
            if first < 72:
                second = u16(second - 1)
                retained_direction = u16(1)
                outcome = visit_path_neighbor(state, first, second, retained_direction, output)
                first, second = outcome.coordinates.first, outcome.coordinates.second
                if outcome.carry == 1:
                    return FrontierResult(1, retained_direction, PathCoordinates(first, second))
        if negative_byte(source.byte()):
            break
    output.set_byte(0, 255)
    outcome = state.carry_result(0)
    return FrontierResult(outcome.carry, retained_direction, PathCoordinates(first, second))


def visit_path_neighbor(state: GameState, first: Word, second: Word, direction: Word, output: Cursor) -> NeighborResult:
    checked_state(state)
    first = uint(first, 16)
    second = uint(second, 16)
    direction = uint(direction, 16)
    checked_cursor(output, state)
    outcome = path_neighbor_is_goal(state, first, second, direction)
    if outcome.carry == 1:
        return NeighborResult(outcome.carry, outcome.conditional_sr, PathCoordinates(first, second))
    stored_direction = read_path_direction(state, first, second)
    if low8(stored_direction) == 0:
        cost = read_path_cost(state, first, second)
        if not negative_byte(low8(cost)):
            output.append_byte(low8(first))
            first = u16(s8(low8(first)))
            output.append_byte(low8(second))
            second = u16(s8(low8(second)))
            output.append_byte(low8(cost))
            mark_path_direction(state, first, second, direction)
    outcome = state.carry_result(0)
    return NeighborResult(outcome.carry, outcome.conditional_sr, PathCoordinates(first, second))


def path_neighbor_is_goal(state: GameState, first: Word, second: Word, direction: Word) -> CarryOutcome:
    checked_state(state)
    first = uint(first, 16)
    second = uint(second, 16)
    direction = uint(direction, 16)
    if first == state.path_destination_first():
        if second == state.path_destination_second():
            mark_path_direction(state, first, second, direction)
            return state.carry_result(1)
    return state.carry_result(0)


def mark_path_direction(state: GameState, first: Word, second: Word, direction: Word) -> None:
    checked_state(state)
    first = uint(first, 16)
    second = uint(second, 16)
    direction = uint(direction, 16)
    offset = u16(u16(u16(first << 3) + first) << 3)
    offset = u16(u16(offset + second) << 1)
    state.path_grid.set_byte(offset, low8(direction))


def read_path_direction(state: GameState, first: Word, second: Word) -> Word:
    checked_state(state)
    first = uint(first, 16)
    second = uint(second, 16)
    retained = u16(first << 3)
    offset = u16(u16(retained + first) << 3)
    offset = u16(u16(offset + second) << 1)
    return u16((retained & 65280) | state.path_grid.byte(offset))


def read_path_cost(state: GameState, first: Word, second: Word) -> Word:
    checked_state(state)
    first = uint(first, 16)
    second = uint(second, 16)
    offset = u16(u16(u16(first << 3) + first) << 3)
    offset = u16(u16(offset + second) << 1)
    return u16(state.path_grid.byte(offset, 1))


def reconstruct_path(state: GameState) -> PathCoordinates:
    checked_state(state)
    result = state.path_frontier.cursor()
    first = state.path_destination_first()
    second = state.path_destination_second()
    while True:
        direction = read_path_direction(state, first, second)
        result.append_byte(low8(direction))
        coordinates = step_back_path(first, second, direction)
        first, second = coordinates.first, coordinates.second
        if first == state.path_source_first():
            if second == state.path_source_second():
                break
    result.set_byte(0, 255)
    return PathCoordinates(first, second)


def step_back_path(first: Word, second: Word, direction: Word) -> PathCoordinates:
    first = uint(first, 16)
    second = uint(second, 16)
    direction = uint(direction, 16)
    remaining = u8(low8(direction) - 1)
    if remaining == 0:
        first = u16(first - 1)
    else:
        remaining = u8(remaining - 1)
        if remaining == 0:
            second = u16(second + 1)
        else:
            remaining = u8(remaining - 1)
            if remaining == 0:
                first = u16(first + 1)
            else:
                second = u16(second - 1)
    return PathCoordinates(first, second)

