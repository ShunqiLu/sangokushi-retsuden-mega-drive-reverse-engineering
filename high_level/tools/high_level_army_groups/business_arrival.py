"""Packed-army construction, city arrival and loyalty rules.

Names are probable gameplay roles. Operations retain the original live fixed-
width order; unbounded searches and explicit source/budget boundaries are not
replaced by catalog limits. This module contains no target addresses or code.
"""
from .domain import (
    ArmyState, Table, Word, u8, u16, u32, low8, low16, high16,
    replace_byte, divu_retained, negative_byte, negative_word,
    descending_inclusive,
)


def settle_group_at_city(state: ArmyState) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    project_army_arrival_fields(state, 0x1D3BC)


def locate_group_city(state: ArmyState, packet: Table) -> Word:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    frame = project_army_arrival_fields(state, 0x1D40C, packet)
    return low16(frame.count)


def credit_packed_group_resources(state: ArmyState, packet: Table, city: Word) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    project_army_arrival_fields(state, 0x1D44C, packet, city)


def erase_group_packet(state: ArmyState, packet: Table) -> Table:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    frame = project_army_arrival_fields(state, 0x1D4B8, packet)
    return state.table(frame.roster.base)


def adjust_battle_losing_loyalty(state: ArmyState) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    project_army_arrival_fields(state, 0x1D4DA)


def apply_returning_officer_loyalty(state: ArmyState) -> None:
    sample = u32(state.sample_random() & 65535)
    factor = u16(high16(u32(sample * 5)) + 6)
    status = state.status
    value = u16(104)
    officer = u16(state.selected_officer() & 255)
    value = u16(replace_byte(value, low8(value - status.byte(officer))))
    value = u16(value >> 1)
    affinity = state.affinity
    source = u16(state.loyalty_source() & 255)
    influence = u16(affinity.byte(source))
    value = u32(low16(value) * low16(influence))
    value = u32(low16(value) * low16(factor))
    value = divu_retained(value, 500)
    if low16(value) > 100:
        value = u32((value & 4294901760) | 100)
    status.set_byte(officer, low8(value))


def append_group_from_survivor_roster(state: ArmyState) -> Table:
    packet = state.packed_groups
    assignments = state.city_assignments
    while True:
        count = u16(packet.byte() & 15)
        if count == 0:
            break
        packet = packet.at(count, 13)
    count = u16(0)
    roster = state.survivor_roster.cursor()
    while True:
        selected = roster.next_word()
        if negative_word(selected):
            break
        if not selected & 16384:
            continue
        packet.set_byte(count, low8(selected), 13)
        count = u16(count + 1)
        selected = u16(selected & 255)
        assignments.set_byte(selected, assignments.byte(selected) | 64)
    packet.set_byte(count, 0, 13)
    packet.set_byte(0, low8(count))
    if state.side_flags() & 2:
        force = state.secondary_force()
    else:
        force = state.primary_force()
    packet.set_byte(0, low8(force), 4)
    attributes = state.attributes
    remaining = u16(count - 1)
    total = u32(0)
    attribute = u16(0)
    for member_index in descending_inclusive(remaining):
        attribute = u16(replace_byte(attribute, packet.byte(member_index, 13)))
        attribute = u16(replace_byte(attribute, attributes.byte(attribute)))
        total = u32((total & 4294901760) | u16(low16(total) + attribute))
    total = divu_retained(total, count)
    packet.set_byte(0, low8(total), 3)
    row, column = choose_empty_neighbor_position(state)
    packet.set_byte(0, low8(row), 1)
    packet.set_byte(0, low8(column), 2)
    return packet


def choose_empty_neighbor_position(state: ArmyState) -> tuple[Word, Word]:
    neighbors = state.neighbor_offsets
    costs = state.terrain_cost
    terrain = state.terrain_cells
    selected = u16(state.city() << 2)
    coordinates = state.city_coordinates
    center_row = u16(coordinates.word(selected, 2) >> 4)
    center_column = u16(coordinates.word(selected) >> 4)
    while True:
        row = u16(center_row + neighbors.word())
        if row >= 72:
            neighbors = neighbors.advance(4)
            continue
        column = u16(center_column + neighbors.word(0, 2))
        if column >= 72:
            neighbors = neighbors.advance(4)
            continue
        cell = u16(row << 3)
        cell = u16(cell + row)
        cell = u16(cell << 3)
        cell = u16(cell + column)
        kind = u16(terrain.byte(cell))
        if negative_byte(costs.byte(kind)):
            neighbors = neighbors.advance(4)
            continue
        groups = state.packed_groups
        while True:
            count = u16(groups.byte() & 15)
            if count == 0:
                return row, column
            if low8(row) == groups.byte(0, 1):
                if low8(column) == groups.byte(0, 2):
                    break
            groups = groups.at(count, 13)
        neighbors = neighbors.advance(4)

from .domain import project_army_arrival_fields
