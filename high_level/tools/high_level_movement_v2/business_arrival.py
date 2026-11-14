"""Live campaign arrival, ranked merging and adjacent hostile blocking.

Compatibility includes unusual original field aliases and the asymmetric rice
ceiling. Names describe probable roles, not a closed natural gameplay domain.
"""
from .domain import (GameState, Table, Word, CarryOutcome, uint, u8, u16, u32,
                     low8, low16, high16, replace_byte, negative_byte,
                     negative_word, descending_inclusive, divu_retained)


def hostile_adjacent_block(state: GameState) -> CarryOutcome:
    """Combine live low mask bits with the explicit retained upper-mask context.

    Original partial WORD operations leave the upper half available to dynamic
    LONG bit tests. The context is a conditional input, not an owner clamp or a
    claim that every original caller clears those bits.
    """
    if state.position_x() & 15 != 0:
        return state.carry_result(0)
    if state.position_y() & 15 != 0:
        return state.carry_result(0)
    center_x = u16(state.position_x() >> 4)
    left_x = u16(center_x - 1)
    right_x = u16(center_x + 1)
    center_y = u16(state.position_y() >> 4)
    upper_y = u16(center_y - 1)
    lower_y = u16(center_y + 1)
    packet = state.table(state.active_packet())
    owner = u16(packet.byte(0, 4))
    state.set_blocking_owner(owner)
    mask = state.force_masks.word(u16(owner << 1))
    state.set_blocking_mask(mask)
    groups = state.packed_groups
    while True:
        count = u16(groups.byte() & 15)
        if count == 0:
            break
        if groups.byte() & 32 == 0:
            other_owner = u16(groups.byte(0, 4))
            if low8(other_owner) != state.blocking_owner_tail():
                mask = state.blocking_mask()
                mask = state.effective_blocking_mask(mask)
                if mask & (1 << (other_owner & 31)) == 0:
                    if low8(left_x) == groups.byte(0, 1) and low8(center_y) == groups.byte(0, 2):
                        return state.carry_result(1)
                    if low8(center_x) == groups.byte(0, 1):
                        if low8(upper_y) == groups.byte(0, 2):
                            return state.carry_result(1)
                        if low8(lower_y) == groups.byte(0, 2):
                            return state.carry_result(1)
                    if low8(right_x) == groups.byte(0, 1) and low8(center_y) == groups.byte(0, 2):
                        return state.carry_result(1)
        count = u16(groups.byte() & 15)
        groups = groups.advance(u32(count + 13))
    grid = state.city_grid
    for city in descending_inclusive(39):
        if grid.byte() != 0:
            other_owner = u16(state.city_owners_reverse.byte(city))
            if low8(other_owner) != state.blocking_owner_tail():
                mask = state.blocking_mask()
                mask = state.effective_blocking_mask(mask)
                if mask & (1 << (other_owner & 31)) == 0:
                    if low8(left_x) == grid.byte(0, 1) and low8(center_y) == grid.byte(0, 2):
                        collect_blocked_cargo(state, grid)
                        return state.carry_result(1)
                    if low8(center_x) == grid.byte(0, 1):
                        if low8(lower_y) == grid.byte(0, 2):
                            collect_blocked_cargo(state, grid)
                            return state.carry_result(1)
                        if low8(upper_y) == grid.byte(0, 2):
                            collect_blocked_cargo(state, grid)
                            return state.carry_result(1)
                    if low8(right_x) == grid.byte(0, 1) and low8(center_y) == grid.byte(0, 2):
                        collect_blocked_cargo(state, grid)
                        return state.carry_result(1)
        grid = grid.advance(-4)
    return state.carry_result(0)


def collect_blocked_cargo(state: GameState, obstacle: Table) -> None:
    obstacle = state.checked_table(obstacle)
    cargo = state.table(state.active_packet())
    kind = u16(obstacle.byte() & 3)
    if kind != 2:
        amount = u32(cargo.byte(0, 5) << 24)
        amount = u32(amount | (cargo.byte(0, 6) << 16))
        amount = u32(amount | (cargo.byte(0, 7) << 8))
        amount = u32(amount | cargo.byte(0, 8))
        amount = u32(amount + 10000)
        if amount > 999999:
            amount = u32(999999)
        cargo.set_byte(0, low8(amount), 8)
        amount = u32(amount >> 8)
        cargo.set_byte(0, low8(amount), 7)
        amount = u32(amount >> 8)
        cargo.set_byte(0, low8(amount), 6)
        amount = u16(low16(amount) >> 8)
        cargo.set_byte(0, low8(amount), 5)
        if kind != 3:
            obstacle.set_byte(0, 0)
        else:
            obstacle.set_byte(0, obstacle.byte() & 128)
            obstacle.set_byte(0, obstacle.byte() | 2)
    else:
        amount = u32(cargo.byte(0, 9) << 24)
        amount = u32(amount | (cargo.byte(0, 10) << 16))
        amount = u32(amount | (cargo.byte(0, 11) << 8))
        amount = u32(amount | cargo.byte(0, 12))
        amount = u32(amount + 10000)
        if amount > 999999:
            amount = u32(99999)
        cargo.set_byte(0, low8(amount), 12)
        amount = u32(amount >> 8)
        cargo.set_byte(0, low8(amount), 11)
        amount = u32(amount >> 8)
        cargo.set_byte(0, low8(amount), 10)
        amount = u16(low16(amount) >> 8)
        cargo.set_byte(0, low8(amount), 9)
        obstacle.set_byte(0, 0)


def settle_arriving_group(state: GameState, cargo_source: Table) -> CarryOutcome:
    cargo_source = state.checked_table(cargo_source)
    packet = state.table(state.active_packet())
    owner, city_index = locate_arrival_city(state, packet)
    if negative_byte(owner):
        owner = u16(replace_byte(owner, packet.byte(0, 4)))
        cargo_source = state.city_owners_reverse
        cargo_source.set_byte(city_index, low8(owner))
        initialize_arrival_loyalty(state, owner, city_index)
        clear_arrival_city_order(state)
    elif low8(owner) != packet.byte(0, 4):
        if owner == 16:
            return state.carry_observed(0)
        state.set_current_force(0)
        state.set_current_force_tail(packet.byte(0, 4))
        force = state.current_force()
        if force != state.player_force_word_1():
            if force != state.player_force_word_2():
                if force != state.player_force_word_3():
                    return state.carry_result(0)
        if state.city_processed.byte(state.selected_city()) & 2 != 0:
            return state.carry_result(0)
        state.set_command_step(12)
        return state.carry_result(1)
    city = u16(city_index + 1)
    state.set_current_city(city)
    state.set_roster_exclusion(65535)
    total_count = state.build_roster(city)
    if total_count >= 10:
        return state.carry_result(0)
    packet = state.table(state.active_packet())
    state.set_current_force_tail(packet.byte(0, 4))
    member_count = u16(packet.byte() & 15)
    total_count = u16(total_count + member_count)
    if total_count <= 10:
        state.credit_packet(city, packet)
        assign_packet_members(state, packet, city, member_count)
        compact_after_packet(state, packet, member_count)
        city = state.current_city()
        if negative_word(state.city_heads.word(u16(city << 1))):
            city = state.current_city()
            state.set_roster_exclusion(65535)
            state.build_roster(city)
            state.choose_city_head(city)
        return state.carry_result(0)
    owner = packet.byte(0, 4)
    if owner == state.player_force_1():
        total_count = detach_packet_force_head(state, packet, city_index, total_count)
    elif owner == state.player_force_2():
        total_count = detach_packet_force_head(state, packet, city_index, total_count)
    elif owner == state.player_force_3():
        total_count = detach_packet_force_head(state, packet, city_index, total_count)
    else:
        total_count = merge_overcapacity_arrival(state, packet, city_index, total_count)
        return state.carry_result(0)
    state.set_current_city(owner)
    excess = u16(total_count - 10)
    remaining = u16(member_count - excess)
    if remaining == 0:
        return state.carry_result(0)
    state.set_remaining_members(remaining)
    state.set_command_step(u16(state.command_step() + 1))
    return state.carry_result(1)


def assign_packet_members(state: GameState, packet: Table, city: Word, count: Word) -> None:
    packet = state.checked_table(packet)
    city = uint(city, 16)
    count = uint(count, 16)
    roster = packet.at(0, 13).cursor()
    member = u16(0)
    force = u16(packet.byte(0, 4))
    head = state.force_heads.word(u16(force << 1))
    for position in descending_inclusive(u16(count - 1)):
        member = u16(replace_byte(member, roster.next_byte()))
        state.officer_assignments.set_byte(member, low8(city))
        if low8(member) == low8(head):
            member = u16(city << 1)
            state.city_heads.set_word(member, head)


def compact_after_packet(state: GameState, packet: Table, count: Word) -> None:
    packet = state.checked_table(packet)
    count = uint(count, 16)
    source = packet.at(count, 13).cursor()
    destination = packet.cursor()
    while True:
        size = u16(source.byte() & 15)
        if size == 0:
            break
        for position in descending_inclusive(u16(size + 12)):
            value = source.next_byte()
            destination.append_byte(value)
    destination.set_byte(0, 0)
    state.set_active_packet(0)


def initialize_arrival_loyalty(state: GameState, force: Word, city_index: Word) -> None:
    force = uint(force, 16)
    city_index = uint(city_index, 16)
    head = state.force_heads.word(u16(force << 1))
    affinity = u16(state.loyalty.byte(head))
    sample = u32(state.sample_random())
    multiplier = u16(high16(u32(sample * 3)) + 6)
    result = divu_retained(u32(affinity * multiplier), 10)
    state.city_reserves.set_word(u16(city_index << 2), low16(result), 2)


def clear_arrival_city_order(state: GameState) -> None:
    city = u16(state.selected_city() << 2)
    state.selected_orders.set_long(city, 0)


def merge_overcapacity_arrival(state: GameState, packet: Table, city_index: Word, total_count: Word) -> Word:
    packet = state.checked_table(packet)
    city_index = uint(city_index, 16)
    total_count = uint(total_count, 16)
    city = u16(city_index + 1)
    build_packet_member_roster(state, packet)
    extract_force_head_from_roster(state, packet, city)
    sort_packet_roster_by_status(state)
    excess = assign_ranked_packet_members(state, packet, city, total_count)
    state.credit_packet_wrapped(city, packet)
    compact_arrival_packet(state, packet)
    return excess


def build_packet_member_roster(state: GameState, packet: Table) -> None:
    packet = state.checked_table(packet)
    roster = state.member_roster.cursor()
    count = u16(packet.byte() & 15)
    member = u16(0)
    for position in descending_inclusive(u16(count - 1)):
        member = u16(replace_byte(member, packet.byte(position, 13)))
        roster.append_word(member)
    roster.set_word(0, 65535)


def extract_force_head_from_roster(state: GameState, packet: Table, city: Word) -> None:
    packet = state.checked_table(packet)
    city = uint(city, 16)
    force = u16(packet.byte(0, 4))
    head = state.force_heads.word(u16(force << 1))
    source = state.member_roster.cursor()
    ranked = state.ranked_roster.cursor()
    weights = state.ranked_status.cursor()
    while True:
        member = source.next_word()
        if negative_word(member):
            break
        if member == head:
            ranked.append_word(head)
            weights.append_word(100)
            while True:
                shifted = source.next_word()
                source.set_word(u16(65532), shifted)
                if negative_word(shifted):
                    break
            state.city_heads.set_word(u16(city << 1), head)
            break
    ranked.set_word(0, 65535)


def sort_packet_roster_by_status(state: GameState) -> None:
    source = state.member_roster.cursor()
    attribute = u16(0)
    while True:
        member = source.next_word()
        if negative_word(member):
            break
        attribute = u16(replace_byte(attribute, state.officer_status.byte(member)))
        ranked = state.ranked_roster.cursor()
        weights = state.ranked_status.cursor()
        while not negative_word(ranked.word()):
            if attribute > weights.word():
                break
            ranked = ranked.advance(2)
            weights = weights.advance(2)
        while True:
            old_member = ranked.word()
            old_attribute = weights.word()
            ranked.append_word(member)
            weights.append_word(attribute)
            member = old_member
            if negative_word(member):
                break
            attribute = old_attribute
        ranked.set_word(0, 65535)


def assign_ranked_packet_members(state: GameState, packet: Table, city: Word, total_count: Word) -> Word:
    packet = state.checked_table(packet)
    city = uint(city, 16)
    total_count = uint(total_count, 16)
    count = u16(packet.byte() & 15)
    excess = u16(total_count - 9)
    available = u16(count - excess)
    roster = state.ranked_roster.cursor()
    for position in descending_inclusive(available):
        member = roster.next_word()
        state.officer_assignments.set_byte(member, low8(city))
    city = u16(city | 128)
    while True:
        member = roster.next_word()
        if negative_word(member):
            break
        state.officer_assignments.set_byte(member, low8(city))
    city = u16(city & 65407)
    return excess


def compact_arrival_packet(state: GameState, packet: Table) -> None:
    packet = state.checked_table(packet)
    count = u16(packet.byte() & 15)
    source = packet.at(count, 13).cursor()
    destination = packet.cursor()
    while True:
        size = u16(source.byte() & 15)
        if size == 0:
            break
        for position in descending_inclusive(u16(size + 12)):
            value = source.next_byte()
            destination.append_byte(value)
    destination.set_byte(0, 0)
    state.set_active_packet(0)


def detach_packet_force_head(state: GameState, packet: Table, city_index: Word, total_count: Word) -> Word:
    packet = state.checked_table(packet)
    city_index = uint(city_index, 16)
    total_count = uint(total_count, 16)
    last = u16((packet.byte() & 15) - 1)
    force = u16(packet.byte(0, 4))
    head = state.force_heads.word(u16(force << 1))
    index = u16(0)
    while True:
        if low8(head) == packet.byte(index, 13):
            break
        index = u16(index + 1)
        if index >= last:
            return total_count
    index = u16(index + 1)
    while index < last:
        value = packet.byte(index, 13)
        packet.set_byte(index, value, 12)
        index = u16(index + 1)
    while True:
        size = u16(packet.byte(index, 13) & 15)
        if size == 0:
            break
        for position in descending_inclusive(u16(size + 12)):
            value = packet.byte(index, 13)
            packet.set_byte(index, value, 12)
            index = u16(index + 1)
    packet.set_byte(index, 0, 12)
    packet.set_byte(0, u8(packet.byte() - 1))
    city = u16(replace_byte(index, low8(city_index)))
    city = u16(city + 1)
    state.officer_assignments.set_byte(head, low8(city))
    state.city_heads.set_word(u16(city << 1), head)
    return u16(total_count + 1)


def locate_arrival_city(state: GameState, packet: Table) -> tuple[Word, Word]:
    packet = state.checked_table(packet)
    vertical = u16(packet.byte(0, 2) << 4)
    horizontal = u16(packet.byte(0, 1) << 4)
    coordinates = state.following_city_coordinates.cursor()
    city = u16(0)
    state.set_selected_city(1)
    for remaining in descending_inclusive(39):
        first = coordinates.next_word()
        second = coordinates.next_word()
        if horizontal == u16(second - 24):
            if vertical == first or vertical == u16(first - 16):
                return u16(state.city_owners_reverse.byte(city)), city
        if horizontal == u16(second - 8):
            if vertical == u16(first + 16) or vertical == first:
                return u16(state.city_owners_reverse.byte(city)), city
            if u16(first - 16) == first:
                return u16(state.city_owners_reverse.byte(city)), city
            if vertical == u16(first - 32):
                return u16(state.city_owners_reverse.byte(city)), city
        if horizontal == u16(second + 8):
            if vertical == first or vertical == u16(first - 16):
                return u16(state.city_owners_reverse.byte(city)), city
        city = u16(city + 1)
        state.set_selected_city(u16(state.selected_city() + 1))
    return u16(16), city
