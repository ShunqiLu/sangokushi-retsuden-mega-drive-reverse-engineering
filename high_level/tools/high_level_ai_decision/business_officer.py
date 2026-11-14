"""Ordered officer queries and candidate marking for the original AI decisions.

Tables are live views, not snapshots.  Wrapped WORD offsets and the skipped
membership predecrement are intentional compatibility rules.  Tuple results
expose the best value, selected identity, and last scan item where applicable.
The state boundary owns memory limits and conditional privileged carry writes.
"""
from .domain import (
    AiState, CarryOutcome, Table, Word, descending_inclusive,
    low8, negative_byte, negative_word, u16,
)


def select_roster_attribute_max(state: AiState) -> tuple[Word, Word, Word]:
    roster = state.roster.cursor()
    attributes = state.b600
    best = u16(0)
    selected = u16(65535)
    while True:
        member = roster.next_word()
        if negative_word(member):
            break
        if member & 16384:
            continue
        index = u16(member << 1)
        score = attributes.word(index)
        if score > best:
            best = score
            selected = u16(index >> 1)
    return best, selected, member


def select_foreign_nonruler_attribute_sum(state: AiState) -> tuple[Word, Word, Word]:
    neighbors = state.neighbors.at(u16(state.current_city() << 3)).cursor()
    first = state.b600
    second = state.b400
    owners = state.city_owners
    processed = state.city_processed
    status = state.c300
    best = u16(0)
    selected = u16(65535)
    selected_city = u16(65535)
    while True:
        city = u16(neighbors.next_byte())
        if negative_byte(city):
            break
        owner = u16(owners.byte(city))
        if negative_byte(owner):
            continue
        if owner == state.force_selector():
            continue
        if processed.byte(city) != 0:
            continue
        best, selected, selected_city = scan_nonruler_city_attribute_sum(
            state, city, best, selected, selected_city, first, second, status,
        )
    return best, selected, selected_city


def scan_nonruler_city_attribute_sum(
    state: AiState, city: Word, best: Word, selected: Word,
    selected_city: Word, first: Table, second: Table, status: Table,
) -> tuple[Word, Word, Word]:
    city = u16(city)
    best = u16(best)
    selected = u16(selected)
    selected_city = u16(selected_city)
    owner = u16(state.city_owners.byte(city))
    head = state.force_heads.word(u16(owner << 1))
    membership = state.officer_flags.cursor()
    for officer in descending_inclusive(u16(255)):
        # Skipping the ruler before this read shifts all subsequent memberships.
        if officer == head:
            continue
        if low8(city) != membership.previous_byte():
            continue
        if status.byte(officer) >= 95:
            continue
        index = u16(officer << 1)
        score = u16(first.word(index) + second.word(index))
        if score > best:
            best = score
            selected = officer
            selected_city = city
    return best, selected, selected_city


def selected_city_has_player_owner(state: AiState) -> CarryOutcome:
    owners = state.city_owners
    city = state.selected_city()
    owner = owners.byte(city)
    if owner == state.player_first():
        return state.carry_result(1)
    if owner == state.player_second():
        return state.carry_result(1)
    if owner == state.player_third():
        return state.carry_result(1)
    return state.carry_result(0)


def selected_player_officer_removed_gate(state: AiState) -> CarryOutcome:
    owners = state.city_owners
    city = state.selected_city()
    owner = owners.byte(city)
    if (owner == state.player_first() or owner == state.player_second()
            or owner == state.player_third()):
        officer = state.selected_officer()
        membership = state.officer_assignments.byte(officer)
        if membership == 255:
            return state.carry_result(1)
    return state.carry_result(0)


def select_player_neighbor_head_attribute_min(state: AiState) -> tuple[Word, Word, Word]:
    neighbors = state.neighbors.at(u16(state.current_city() << 3)).cursor()
    owners = state.city_owners
    attributes = state.b600
    heads = state.city_heads
    processed = state.city_processed
    best = u16(65535)
    selected = u16(65535)
    while True:
        city = u16(neighbors.next_byte())
        if negative_byte(city):
            break
        if processed.byte(city) != 0:
            continue
        owner = owners.byte(city)
        if (owner != state.player_first() and owner != state.player_second()
                and owner != state.player_third()):
            continue
        index = u16(city << 1)
        head = heads.word(index)
        head_index = u16(head << 1)
        score = attributes.word(head_index)
        if score < best:
            best = score
            selected = city
    return best, selected, city


def select_and_mark_roster_attribute_max(
    state: AiState, last_member: Word,
) -> tuple[Word, Word, Word]:
    last_member = u16(last_member)
    roster = state.roster.cursor()
    attributes = state.b600
    best = u16(0)
    selected = u16(65535)
    if negative_word(state.roster.word(u16(2))):
        return best, selected, last_member
    while True:
        last_member = roster.next_word()
        if negative_word(last_member):
            break
        if last_member & 16384:
            continue
        index = u16(last_member << 1)
        score = attributes.word(index)
        if score > best:
            best = score
            selected = last_member
    if negative_word(selected):
        return best, selected, last_member
    state.officer_flags.set_byte(selected, 1)
    roster = state.roster.cursor()
    while True:
        last_member = roster.next_word()
        if negative_word(last_member):
            break
        if last_member == selected:
            last_member = u16(last_member | 16384)
            roster.set_word(u16(65534), last_member)
            break
    return best, selected, last_member


def select_roster_attribute_max_preserving_id(state: AiState) -> tuple[Word, Word, Word]:
    roster = state.roster.cursor()
    attributes = state.b600
    best = u16(0)
    selected = u16(65535)
    while True:
        member = roster.next_word()
        if negative_word(member):
            break
        if member & 16384:
            continue
        index = u16(member << 1)
        score = attributes.word(index)
        if score > best:
            best = score
            selected = member
    return best, selected, member
