"""Neighbour queries and command policies with explicit live-data semantics."""
from .domain import (AiState, CarryOutcome, Long, Table, Word,
                     descending_inclusive, low8, negative_byte, negative_word,
                     replace_byte, u16, u32)


def choose_attribute_neighbor_action(state: AiState) -> None:
    best, selected = select_foreign_neighbor_attribute_max(state)
    if not negative_word(selected):
        threshold = u16(5)
        if best < 80:
            threshold = u16(3)
        sample = state.sample_random()
        scaled = u16(u32(sample << 3) >> 16)
        if scaled < threshold:
            state.set_command(5)
            return
    state.set_command(3)


def select_foreign_neighbor_attribute_max(state: AiState) -> tuple[Word, Word]:
    neighbors = state.neighbors.at(u16(state.current_city() << 3)).cursor()
    best = u16(0)
    selected = u16(65535)
    force = state.force_selector()
    owners = state.city_owners
    first = state.b600
    second = state.b400
    status = state.c300
    processed = state.city_processed
    while True:
        city = u16(neighbors.next_byte())
        if negative_byte(city):
            break
        if owners.byte(city) == low8(force):
            continue
        if negative_byte(owners.byte(city)):
            continue
        if processed.byte(city) != 0:
            continue
        score = city_officer_attribute_max(state, city, first, second, status)
        if score > best:
            best = score
            selected = city
    return best, selected


def city_officer_attribute_max(state: AiState, city: Word, first: Table,
                               second: Table, status: Table) -> Word:
    city = u16(city)
    membership = state.city_assignments
    maximum = u16(0)
    for officer in descending_inclusive(255):
        if membership.previous_byte() != low8(city):
            continue
        if status.byte(officer) > 95:
            continue
        index = u16(officer << 1)
        if first.word(index) > maximum:
            maximum = first.word(index)
        if second.word(index) > maximum:
            maximum = second.word(index)
    return maximum


def choose_player_neighbor_action(state: AiState) -> None:
    gate = neighbor_has_player_owner(state)
    if gate.carry == 1:
        state.set_command(4)
    else:
        state.set_command(8)


def neighbor_has_player_owner(state: AiState) -> CarryOutcome:
    neighbors = state.neighbors.at(u16(state.current_city() << 3)).cursor()
    owners = state.city_owners
    while True:
        city = u16(neighbors.next_byte())
        if negative_byte(city):
            break
        owner = u16(owners.byte(city))
        if negative_byte(owner):
            continue
        if owner == state.player_first():
            return state.carry_result(1)
        if owner == state.player_second():
            return state.carry_result(1)
        if owner == state.player_third():
            return state.carry_result(1)
    return state.carry_result(0)


def choose_resource_neighbor_action(state: AiState) -> None:
    state.sample_random()
    total, selected = select_player_neighbor_resource_sum(state)
    state.set_chosen_city(selected)
    if total >= 100000:
        command = u16(6)
    elif total >= 50000:
        if u16(state.seed_word() & 7) < 5:
            command = u16(6)
        else:
            command = u16(8)
    elif total >= 10000:
        if state.seed_low_byte() & 1:
            command = u16(6)
        else:
            command = u16(8)
    else:
        if u16(state.seed_word() & 7) < 2:
            command = u16(6)
        else:
            command = u16(8)
    state.set_command(command)


def select_player_neighbor_resource_sum(state: AiState) -> tuple[Long, Word]:
    neighbors = state.neighbors.at(u16(state.current_city() << 3)).cursor()
    best = u32(0)
    selected = u16(65535)
    city = u16(0)
    owners = state.city_owners
    balances = state.city_balances
    rice = state.city_rice
    while True:
        city = u16(replace_byte(city, neighbors.next_byte()))
        if negative_byte(low8(city)):
            break
        owner = u16(owners.byte(city))
        if negative_byte(owner):
            continue
        if owner != state.player_first():
            if owner != state.player_second():
                if low8(selected) != state.player_third():
                    continue
        city = u16(city << 2)
        total = u32(balances.long(city) + rice.long(city))
        if total > best:
            best = total
            city = u16(city >> 2)
            selected = city
    return best, selected
