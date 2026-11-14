"""Live campaign arrival, ranked merging and adjacent hostile blocking.

Compatibility includes unusual original field aliases and the asymmetric rice
ceiling. Names describe probable roles, not a closed natural gameplay domain.
"""
from .domain import (GameState, Table, Word, CarryOutcome, uint, u8, u16, u32,
                     low8, low16, high16, replace_byte, negative_byte,
                     negative_word, descending_inclusive, divu_retained)
from .domain import s16
from ..high_level_scene_flows.domain import SceneState
from ..high_level_main_flows.services import FirstDeploymentFrame
from ..high_level_main_flows.business_movement_support import (first_replace,
    MovementContinuationBoundary, _movement_frame, _movement_move,
    _movement_test, _movement_test_long, _movement_move_long,
    _movement_compare, _movement_compare_address, _movement_binary_flags,
    _movement_fixed_shift_word, _movement_shift_long, _movement_adjust_word,
    _movement_arithmetic_long, _movement_multiply_word, _movement_divu_word,
    _movement_save_longs, _movement_restore_longs, _movement_mutation_flags)
from ..high_level_main_flows.business_gameplay import _order_full_sr_carry
from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
from ..high_level_gameplay_flow.business_battle import build_roster_fields, choose_city_head_fields
from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
from ..high_level_battle_ai.business_formation import first_deployment_random_fields


def hostile_adjacent_block(state: GameState) -> CarryOutcome:
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


def _arrival_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Require the actual live bus and every physical carrier, including A7."""
    frame = _movement_frame(state, frame)
    state.sr = state.sr & 65504 | frame.status
    return frame


def _arrival_store_fields(state, frame, address, value, width=2, clear=False) -> FirstDeploymentFrame:
    if clear:
        state.read(address, width)
    state.write(address, width, value)
    if width == 4:
        return _movement_test_long(state, frame, value)
    return _movement_test(state, frame, value, width * 8)


def _arrival_add_fields(state, frame, carrier, value, subtract=False) -> FirstDeploymentFrame:
    frame, result = _movement_binary_flags(state, frame, low16(frame.carrier(carrier)), value, 16, subtract)
    return first_replace(frame, **{carrier: frame.carrier(carrier) & 4294901760 | result})


def _arrival_db_fields(frame, carrier) -> tuple:
    remaining = u16(low16(frame.carrier(carrier)) - 1)
    return (first_replace(frame, **{carrier: frame.carrier(carrier) & 4294901760 | remaining}), remaining != 65535)


def _arrival_bit_fields(state, frame, value, bit) -> FirstDeploymentFrame:
    status = frame.status & 27 | (4 if not value & 1 << (bit & 31) else 0)
    state.sr = state.sr & 65504 | status
    return first_replace(frame, status=status)


def _arrival_carry_fields(state, frame, carry) -> FirstDeploymentFrame:
    _order_full_sr_carry(state, carry)
    return first_replace(frame, status=state.sr & 31)


def _arrival_memory_increment_fields(state, frame, address) -> FirstDeploymentFrame:
    prior = state.read(address, 2)
    frame, value = _movement_mutation_flags(state, frame, prior, 1, 16)
    state.write(address, 2, value)
    return frame


def _arrival_swap_fields(state, frame, carrier) -> FirstDeploymentFrame:
    value = frame.carrier(carrier)
    return _movement_move_long(state, frame, carrier, u32(value << 16 | value >> 16))


def _arrival_call_fields(state, frame, target, continuation) -> FirstDeploymentFrame:
    """One original callee-entry LONG; no synthesized return or detached RAM."""
    frame = _arrival_frame_fields(state, frame)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, uint(continuation, 32))
    entered = first_replace(frame, stack_cursor=stack)
    children = {87240: collect_blocked_cargo_fields, 87410: settle_arriving_group_fields, 87728: add_packet_city_resources_fields, 87836: assign_packet_members_fields, 87896: compact_after_packet_fields, 87930: initialize_arrival_loyalty_fields, 88000: clear_arrival_city_order_fields, 88024: merge_overcapacity_arrival_fields, 88052: build_packet_member_roster_fields, 88084: extract_force_head_from_roster_fields, 88152: sort_packet_roster_by_status_fields, 88224: assign_ranked_packet_members_fields, 88276: add_packet_city_resources_wrapped_fields, 88386: compact_arrival_packet_fields, 88428: detach_packet_force_head_fields, 91348: locate_arrival_city_fields}
    if target in children:
        returned = children[target](state, entered)
    elif target == 24392:
        returned = build_roster_fields(BattlePresentationMemory(state), entered)
    elif target == 57846:
        returned = choose_city_head_fields(BattlePresentationMemory(state), entered)
    elif target == 33748:
        returned = first_deployment_random_fields(BattlePolicyMemory(state), entered)
    else:
        raise MovementContinuationBoundary(target, entered, 'arrival child full algorithm not owned')
    returned = _arrival_frame_fields(state, returned)
    actual = returned.stack_cursor.long()
    if actual != continuation:
        raise MovementContinuationBoundary(actual, returned, 'original arrival return LONG changed')
    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))


def _arrival_adjacent_position_fields(state, frame, city_order) -> tuple:
    """Four cardinal neighbors; retain the different original city test order."""
    frame = _movement_compare(state, frame, low8(frame.target_y), frame.roster.byte(0, 1), 8)
    if frame.status & 4:
        frame = _movement_compare(state, frame, low8(frame.count), frame.roster.byte(0, 2), 8)
        if frame.status & 4:
            return (frame, True)
    frame = _movement_compare(state, frame, low8(frame.target_x), frame.roster.byte(0, 1), 8)
    if frame.status & 4:
        for carrier in ('offset_x', 'distance') if city_order else ('distance', 'offset_x'):
            frame = _movement_compare(state, frame, low8(frame.carrier(carrier)), frame.roster.byte(0, 2), 8)
            if frame.status & 4:
                return (frame, True)
    frame = _movement_compare(state, frame, low8(frame.unit), frame.roster.byte(0, 1), 8)
    if frame.status & 4:
        frame = _movement_compare(state, frame, low8(frame.count), frame.roster.byte(0, 2), 8)
        if frame.status & 4:
            return (frame, True)
    return (frame, False)


def hostile_adjacent_block_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """15384..154C8: moving armies and reverse city-grid hostile adjacency.

    The city loop's SWAP/DBRA carrier, repeated header reads and directional
    comparison order are retained.  This callee does not pop its outer LONG.
    """
    frame = _arrival_frame_fields(state, frame)
    frame = _movement_move(state, frame, 'target_x', state.read(16726966, 2), 16)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
    if not frame.status & 4:
        return _arrival_carry_fields(state, frame, False)
    frame = _movement_move(state, frame, 'target_y', state.read(16726968, 2), 16)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 15, 16)
    if not frame.status & 4:
        return _arrival_carry_fields(state, frame, False)
    frame = _movement_move(state, frame, 'target_x', state.read(16726966, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 4, True)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)
    frame = _movement_adjust_word(state, frame, 'target_y', -1)
    frame = _movement_move(state, frame, 'unit', low16(frame.target_x), 16)
    frame = _movement_adjust_word(state, frame, 'unit', 1)
    frame = _movement_move(state, frame, 'count', state.read(16726968, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'count', 4, True)
    frame = _movement_move(state, frame, 'distance', low16(frame.count), 16)
    frame = _movement_adjust_word(state, frame, 'distance', -1)
    frame = _movement_move(state, frame, 'offset_x', low16(frame.count), 16)
    frame = _movement_adjust_word(state, frame, 'offset_x', 1)
    frame = first_replace(frame, roster=state.table_at(4294960912).cursor(), controller=state.table_at(state.read(16726060, 4)).cursor())
    frame = _movement_move(state, frame, 'offset_y', 0, 16)
    frame = _movement_move(state, frame, 'offset_y', frame.controller.byte(0, 4), 8)
    frame = _arrival_store_fields(state, frame, 16726974, low16(frame.offset_y))
    frame = _movement_fixed_shift_word(state, frame, 'offset_y', 1)
    frame = _movement_move(state, frame, 'offset_y', frame.roster.word(low16(frame.offset_y)), 16)
    frame = _arrival_store_fields(state, frame, 16726976, low16(frame.offset_y))
    frame = first_replace(frame, roster=state.table_at(4294938624).cursor())
    while True:
        frame = _movement_move(state, frame, 'choice', frame.roster.byte(), 8)
        frame = _movement_move(state, frame, 'choice', low16(frame.choice) & 15, 16)
        if frame.status & 4:
            break
        frame = _arrival_bit_fields(state, frame, frame.roster.byte(), 5)
        if frame.status & 4:
            frame = _movement_move(state, frame, 'choice', 0, 16)
            frame = _movement_move(state, frame, 'choice', frame.roster.byte(0, 4), 8)
            frame = _movement_compare(state, frame, low8(frame.choice), state.read(16726975, 1), 8)
            if not frame.status & 4:
                frame = _movement_move(state, frame, 'offset_y', state.read(16726976, 2), 16)
                frame = _arrival_bit_fields(state, frame, frame.offset_y, frame.choice)
                if frame.status & 4:
                    frame, adjacent = _arrival_adjacent_position_fields(state, frame, False)
                    if adjacent:
                        return _arrival_carry_fields(state, frame, True)
        frame = _movement_move(state, frame, 'choice', frame.roster.byte(), 8)
        frame = _movement_move(state, frame, 'choice', low16(frame.choice) & 15, 16)
        frame = first_replace(frame, roster=frame.roster.advance(s16(low16(frame.choice)) + 13))
    frame = first_replace(frame, roster=state.table_at(4294954652).cursor(), candidates=state.table_at(4294964264).cursor())
    frame = _arrival_swap_fields(state, frame, 'target_x')
    frame = _movement_move(state, frame, 'target_x', 39, 16)
    while True:
        frame = _movement_test(state, frame, frame.roster.byte(), 8)
        if not frame.status & 4:
            frame = _movement_move(state, frame, 'choice', 0, 16)
            frame = _movement_move(state, frame, 'choice', frame.candidates.byte(low16(frame.target_x)), 8)
            frame = _movement_compare(state, frame, low8(frame.choice), state.read(16726975, 1), 8)
            if not frame.status & 4:
                frame = _movement_move(state, frame, 'offset_y', state.read(16726976, 2), 16)
                frame = _arrival_bit_fields(state, frame, frame.offset_y, frame.choice)
                if frame.status & 4:
                    frame = _arrival_swap_fields(state, frame, 'target_x')
                    frame, adjacent = _arrival_adjacent_position_fields(state, frame, True)
                    if adjacent:
                        frame = _arrival_call_fields(state, frame, 87240, 87228)
                        return _arrival_carry_fields(state, frame, True)
                    frame = _arrival_swap_fields(state, frame, 'target_x')
        frame = first_replace(frame, roster=frame.roster.advance(-4))
        frame, again = _arrival_db_fields(frame, 'target_x')
        if not again:
            return _arrival_carry_fields(state, frame, False)


def collect_blocked_cargo_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """154C8..15572: collect obstacle cargo, including the original rice cap."""
    frame = _arrival_frame_fields(state, frame)
    frame = first_replace(frame, candidates=state.table_at(state.read(16726060, 4)).cursor())
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 3, 16)
    frame = _movement_compare(state, frame, low8(frame.target_x), 2, 8)
    rice = frame.status & 4 != 0
    first = 9 if rice else 5
    frame = _movement_move(state, frame, 'target_y', frame.candidates.byte(0, first), 8)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 8)
    frame = _movement_move(state, frame, 'target_y', frame.candidates.byte(0, first + 1), 8)
    frame = _movement_shift_long(state, frame, 'target_y')
    frame = _movement_move(state, frame, 'target_y', frame.candidates.byte(0, first + 2), 8)
    frame = _movement_shift_long(state, frame, 'target_y')
    frame = _movement_move(state, frame, 'target_y', frame.candidates.byte(0, first + 3), 8)
    frame = _movement_arithmetic_long(state, frame, 'target_y', 10000)
    frame = _movement_compare_address(state, frame, frame.target_y, 999999)
    if not frame.status & 5:
        frame = _movement_move_long(state, frame, 'target_y', 99999 if rice else 999999)
    for displacement, long_shift in ((first + 3, True), (first + 2, True), (first + 1, False)):
        frame = _arrival_store_fields(state, frame, frame.candidates.address(0, displacement), low8(frame.target_y), 1)
        if long_shift:
            frame = _movement_shift_long(state, frame, 'target_y', True)
        else:
            frame = _movement_fixed_shift_word(state, frame, 'target_y', 8, True)
    frame = _arrival_store_fields(state, frame, frame.candidates.address(0, first), low8(frame.target_y), 1)
    if not rice:
        frame = _movement_compare(state, frame, low8(frame.target_x), 3, 8)
        if frame.status & 4:
            value = frame.roster.byte() & 128
            frame = _arrival_store_fields(state, frame, frame.roster.base, value, 1)
            value = frame.roster.byte() | 2
            return _arrival_store_fields(state, frame, frame.roster.base, value, 1)
    return _arrival_store_fields(state, frame, frame.roster.base, 0, 1, True)


def settle_arriving_group_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """15572..156B0: settle ownership, roster capacity and actual packet tails."""
    frame = _arrival_frame_fields(state, frame)
    frame = first_replace(frame, candidates=state.table_at(state.read(16726060, 4)).cursor())
    frame = _arrival_call_fields(state, frame, 91348, 87420)
    frame = _movement_test(state, frame, low8(frame.target_x), 8)
    if frame.status & 8:
        frame = _movement_move(state, frame, 'target_x', frame.candidates.byte(0, 4), 8)
        frame = first_replace(frame, roster=state.table_at(4294964264).cursor())
        frame = _arrival_store_fields(state, frame, frame.roster.address(low16(frame.distance)), low8(frame.target_x), 1)
        frame = _arrival_call_fields(state, frame, 87930, 87442)
        frame = _arrival_call_fields(state, frame, 88000, 87446)
    else:
        frame = _movement_compare(state, frame, low8(frame.target_x), frame.candidates.byte(0, 4), 8)
        if not frame.status & 4:
            frame = _movement_compare(state, frame, low16(frame.target_x), 16, 16)
            if frame.status & 4:
                return frame
            frame = _arrival_store_fields(state, frame, 4294964086, 0, 2, True)
            frame = _arrival_store_fields(state, frame, 4294964087, frame.candidates.byte(0, 4), 1)
            frame = _movement_move(state, frame, 'target_x', state.read(4294964086, 2), 16)
            for address in (4294964858, 4294964860, 4294964862):
                frame = _movement_compare(state, frame, low16(frame.target_x), state.read(address, 2), 16)
                if frame.status & 4:
                    break
            if not frame.status & 4:
                return _arrival_carry_fields(state, frame, False)
            frame = first_replace(frame, candidates=state.table_at(4294961719).cursor())
            frame = _movement_move(state, frame, 'target_x', state.read(4294964114, 2), 16)
            frame = _arrival_bit_fields(state, frame, frame.candidates.byte(low16(frame.target_x)), 1)
            if not frame.status & 4:
                return _arrival_carry_fields(state, frame, False)
            frame = _arrival_store_fields(state, frame, 4294964066, 12)
            return _arrival_carry_fields(state, frame, True)
    frame = _movement_move(state, frame, 'target_x', low16(frame.distance), 16)
    stack = frame.stack_cursor.advance(-2)
    stack.set_word(0, low16(frame.distance))
    frame = _movement_test(state, first_replace(frame, stack_cursor=stack), low16(frame.distance), 16)
    frame = _movement_adjust_word(state, frame, 'target_x', 1)
    frame = _arrival_store_fields(state, frame, 4294964068, low16(frame.target_x))
    frame = _arrival_store_fields(state, frame, 4294964784, 65535)
    frame = _arrival_call_fields(state, frame, 24392, 87480)
    restored = frame.stack_cursor.word()
    frame = _movement_move(state, first_replace(frame, stack_cursor=frame.stack_cursor.advance(2)), 'distance', restored, 16)
    frame = _movement_compare(state, frame, low16(frame.count), 10, 16)
    if not frame.status & 1:
        return _arrival_carry_fields(state, frame, False)
    frame = first_replace(frame, roster=state.table_at(state.read(16726060, 4)).cursor())
    frame = _arrival_store_fields(state, frame, 4294964087, frame.roster.byte(0, 4), 1)
    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(), 8)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 15, 16)
    frame = _arrival_add_fields(state, frame, 'count', low16(frame.target_y))
    frame = _movement_compare(state, frame, low16(frame.count), 10, 16)
    if not frame.status & 5:
        frame = _movement_move(state, frame, 'target_x', frame.roster.byte(0, 4), 8)
        for address in (4294964859, 4294964861, 4294964863):
            frame = _movement_compare(state, frame, low8(frame.target_x), state.read(address, 1), 8)
            if frame.status & 4:
                break
        if not frame.status & 4:
            frame = _arrival_call_fields(state, frame, 88024, 87648)
            return _arrival_carry_fields(state, frame, False)
        frame = _arrival_call_fields(state, frame, 88428, 87606)
        frame = _arrival_store_fields(state, frame, 4294964068, low16(frame.target_x))
        frame = _arrival_add_fields(state, frame, 'count', 10, True)
        frame = _arrival_add_fields(state, frame, 'target_y', low16(frame.count), True)
        if frame.status & 4:
            return _arrival_carry_fields(state, frame, False)
        frame = _arrival_store_fields(state, frame, 4294964870, low16(frame.target_y))
        frame = _arrival_memory_increment_fields(state, frame, 4294964066)
        return _arrival_carry_fields(state, frame, True)
    frame = _arrival_call_fields(state, frame, 87728, 87522)
    frame = _arrival_call_fields(state, frame, 87836, 87526)
    frame = _arrival_call_fields(state, frame, 87896, 87530)
    frame = first_replace(frame, roster=state.table_at(4294964318).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(4294964068, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
    frame = _movement_test(state, frame, frame.roster.word(low16(frame.target_x)), 16)
    if frame.status & 8:
        frame = _movement_move(state, frame, 'target_x', state.read(4294964068, 2), 16)
        frame = _arrival_store_fields(state, frame, 4294964784, 65535)
        frame = _arrival_call_fields(state, frame, 24392, 87564)
        frame = _arrival_call_fields(state, frame, 57846, 87570)
    return _arrival_carry_fields(state, frame, False)


def _arrival_credit_resources_fields(state, frame, wrapped) -> FirstDeploymentFrame:
    """Two original credit ABIs share byte decoding, not overflow policy."""
    carrier = 'target_x' if wrapped else 'offset_x'
    accumulator = 'unit' if wrapped else 'offset_x'
    index = 'target_y' if wrapped else 'distance'
    city = low16(frame.distance) if wrapped else low16(frame.target_x)
    frame = _movement_move(state, frame, index, city, 16)
    frame = _movement_fixed_shift_word(state, frame, index, 2)
    for first, address in ((5, 4294959100), (9, 4294959260)):
        if not wrapped:
            frame = first_replace(frame, opponent=state.table_at(address).cursor())
        frame = _movement_move(state, frame, carrier, frame.roster.byte(0, first), 8)
        frame = _movement_fixed_shift_word(state, frame, carrier, 8)
        frame = _movement_move(state, frame, carrier, frame.roster.byte(0, first + 1), 8)
        frame = _movement_shift_long(state, frame, carrier)
        frame = _movement_move(state, frame, carrier, frame.roster.byte(0, first + 2), 8)
        frame = _movement_shift_long(state, frame, carrier)
        frame = _movement_move(state, frame, carrier, frame.roster.byte(0, first + 3), 8)
        if wrapped:
            frame = first_replace(frame, candidates=state.table_at(address).cursor())
            frame = _movement_move_long(state, frame, accumulator, frame.candidates.long(low16(frame.carrier(index))))
            frame = _movement_arithmetic_long(state, frame, accumulator, frame.carrier(carrier))
            frame = _movement_compare_address(state, frame, frame.carrier(accumulator), 999999)
            cap = not frame.status & 5
        else:
            frame = _movement_arithmetic_long(state, frame, accumulator, frame.opponent.long(low16(frame.carrier(index))))
            cap = frame.status & 1 != 0
            if not cap:
                frame = _movement_compare_address(state, frame, frame.carrier(accumulator), 999999)
                cap = not frame.status & 5
        if cap:
            frame = _movement_move_long(state, frame, accumulator, 999999)
        destination = frame.candidates if wrapped else frame.opponent
        frame = _arrival_store_fields(state, frame, destination.address(low16(frame.carrier(index))), frame.carrier(accumulator), 4)
    return frame


def add_packet_city_resources_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """156B0..1571C: city credits retain carry-overflow saturation."""
    return _arrival_credit_resources_fields(state, _arrival_frame_fields(state, frame), False)


def add_packet_city_resources_wrapped_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """158D4..15942: ranked-arrival credit compares the wrapped LONG only."""
    return _arrival_credit_resources_fields(state, _arrival_frame_fields(state, frame), True)


def assign_packet_members_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1571C..15758: live member BYTEs, current city and force-head linkage."""
    frame = _arrival_frame_fields(state, frame)
    frame = first_replace(frame, candidates=state.table_at(4294953984).cursor(), scan=frame.roster.advance(13))
    frame = _movement_move(state, frame, 'count', low16(frame.target_y), 16)
    frame = _movement_adjust_word(state, frame, 'count', -1)
    frame = _movement_move(state, frame, 'unit', 0, 16)
    frame = _movement_move(state, frame, 'distance', 0, 16)
    frame = _movement_move(state, frame, 'distance', frame.roster.byte(0, 4), 8)
    frame = _movement_fixed_shift_word(state, frame, 'distance', 1)
    frame = first_replace(frame, controller=state.table_at(4294960704).cursor())
    frame = _movement_move(state, frame, 'distance', frame.controller.word(low16(frame.distance)), 16)
    frame = first_replace(frame, controller=state.table_at(4294964318).cursor())
    while True:
        value = frame.scan.byte()
        frame = _movement_move(state, first_replace(frame, scan=frame.scan.advance(1)), 'unit', value, 8)
        frame = _arrival_store_fields(state, frame, frame.candidates.address(low16(frame.unit)), low8(frame.target_x), 1)
        frame = _movement_compare(state, frame, low8(frame.distance), low8(frame.unit), 8)
        if frame.status & 4:
            frame = _movement_move(state, frame, 'unit', low16(frame.target_x), 16)
            frame = _movement_fixed_shift_word(state, frame, 'unit', 1)
            frame = _arrival_store_fields(state, frame, frame.controller.address(low16(frame.unit)), low16(frame.distance))
        frame, again = _arrival_db_fields(frame, 'count')
        if not again:
            return frame


def _arrival_compact_packet_tail_fields(state, frame) -> FirstDeploymentFrame:
    """Retain header scanning, BYTE copy order, and the sentinel CLR reads."""
    while True:
        frame = _movement_move(state, frame, 'target_x', frame.candidates.byte(), 8)
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
        if frame.status & 4:
            break
        frame = _arrival_add_fields(state, frame, 'target_x', 12)
        while True:
            value = frame.candidates.byte()
            frame = _arrival_store_fields(state, frame, frame.roster.base, value, 1)
            frame = first_replace(frame, candidates=frame.candidates.advance(1), roster=frame.roster.advance(1))
            frame, again = _arrival_db_fields(frame, 'target_x')
            if not again:
                break
    frame = _arrival_store_fields(state, frame, frame.roster.base, 0, 1, True)
    return _arrival_store_fields(state, frame, 16726060, 0, 4, True)


def compact_after_packet_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """15758..1577A: caller's actual D1 member count selects the next packet."""
    frame = _arrival_frame_fields(state, frame)
    frame = first_replace(frame, candidates=frame.roster.advance(s16(low16(frame.target_y)) + 13))
    return _arrival_compact_packet_tail_fields(state, frame)


def initialize_arrival_loyalty_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1577A..157C0: true five-LONG save, RNG slot and city reserve fraction."""
    frame = _arrival_frame_fields(state, frame)
    saved = ('target_x', 'target_y', 'unit', 'distance', 'roster')
    frame = _movement_save_longs(state, frame, saved)
    frame = first_replace(frame, roster=state.table_at(4294960704).cursor())
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
    frame = _movement_move(state, frame, 'target_x', frame.roster.word(low16(frame.target_x)), 16)
    frame = first_replace(frame, roster=state.table_at(4294951424).cursor())
    frame = _movement_move(state, frame, 'unit', 0, 16)
    frame = _movement_move(state, frame, 'unit', frame.roster.byte(low16(frame.target_x)), 8)
    frame = _arrival_call_fields(state, frame, 33748, 87960)
    frame = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)
    frame = _movement_move_long(state, frame, 'target_y', frame.target_x)
    value = frame.target_x
    shifted = u32(value << 1)
    status = (17 if value & 2147483648 else 0) | (8 if shifted & 2147483648 else 0) | (4 if shifted == 0 else 0)
    state.sr = state.sr & 65504 | status
    frame = first_replace(frame, target_x=shifted, status=status)
    frame = _movement_arithmetic_long(state, frame, 'target_x', frame.target_y)
    frame = _arrival_swap_fields(state, frame, 'target_x')
    frame = _arrival_add_fields(state, frame, 'target_x', 6)
    frame = _movement_multiply_word(state, frame, 'unit', low16(frame.target_x))
    frame = _movement_divu_word(state, frame, 'unit', 10, 87980)
    frame = first_replace(frame, roster=state.table_at(4294959904).cursor())
    frame = _movement_fixed_shift_word(state, frame, 'distance', 2)
    frame = _arrival_store_fields(state, frame, frame.roster.address(low16(frame.distance), 2), low16(frame.unit))
    return _movement_restore_longs(state, frame, saved)


def clear_arrival_city_order_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _arrival_frame_fields(state, frame)
    saved = ('target_x', 'roster')
    frame = _movement_save_longs(state, frame, saved)
    frame = first_replace(frame, roster=state.table_at(4294961012).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(4294964114, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    frame = _arrival_store_fields(state, frame, frame.roster.address(low16(frame.target_x)), 0, 4, True)
    return _movement_restore_longs(state, frame, saved)


def merge_overcapacity_arrival_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """157D8..157F4: rank the actual roster, credit cargo, compact its packet."""
    frame = _arrival_frame_fields(state, frame)
    frame = _movement_adjust_word(state, frame, 'distance', 1)
    for target, continuation in ((88052, 88030), (88084, 88034), (88152, 88038), (88224, 88042), (88276, 88046), (88386, 88050)):
        frame = _arrival_call_fields(state, frame, target, continuation)
    return frame


def build_packet_member_roster_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _arrival_frame_fields(state, frame)
    frame = first_replace(frame, candidates=state.table_at(4294955776).cursor())
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)
    frame = _movement_adjust_word(state, frame, 'target_y', -1)
    frame = _movement_move(state, frame, 'unit', 0, 16)
    while True:
        frame = _movement_move(state, frame, 'unit', frame.roster.byte(low16(frame.target_y), 13), 8)
        frame = _arrival_store_fields(state, frame, frame.candidates.base, low16(frame.unit))
        frame = first_replace(frame, candidates=frame.candidates.advance(2))
        frame, again = _arrival_db_fields(frame, 'target_y')
        if not again:
            return _arrival_store_fields(state, frame, frame.candidates.base, 65535)


def extract_force_head_from_roster_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _arrival_frame_fields(state, frame)
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(0, 4), 8)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
    frame = first_replace(frame, candidates=state.table_at(4294960704).cursor())
    frame = _movement_move(state, frame, 'target_y', frame.candidates.word(low16(frame.target_y)), 16)
    frame = first_replace(frame, candidates=state.table_at(4294955776).cursor(), controller=state.table_at(4294955798).cursor(), scan=state.table_at(4294955820).cursor())
    while True:
        value = frame.candidates.word()
        frame = _movement_move(state, first_replace(frame, candidates=frame.candidates.advance(2)), 'unit', value, 16)
        if frame.status & 8:
            break
        frame = _movement_compare(state, frame, low16(frame.unit), low16(frame.target_y), 16)
        if not frame.status & 4:
            continue
        frame = _arrival_store_fields(state, frame, frame.controller.base, low16(frame.target_y))
        frame = first_replace(frame, controller=frame.controller.advance(2))
        frame = _arrival_store_fields(state, frame, frame.scan.base, 100)
        frame = first_replace(frame, scan=frame.scan.advance(2))
        while True:
            value = frame.candidates.word()
            frame = first_replace(frame, candidates=frame.candidates.advance(2))
            frame = _arrival_store_fields(state, frame, frame.candidates.address(0, -4), value)
            if frame.status & 8:
                break
        frame = _movement_move(state, frame, 'unit', low16(frame.distance), 16)
        frame = _movement_fixed_shift_word(state, frame, 'unit', 1)
        frame = first_replace(frame, candidates=state.table_at(4294964318).cursor())
        frame = _arrival_store_fields(state, frame, frame.candidates.address(low16(frame.unit)), low16(frame.target_y))
        break
    return _arrival_store_fields(state, frame, frame.controller.base, 65535)


def sort_packet_roster_by_status_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """15858..158A0: stable insertion into paired member/rating WORD rosters."""
    frame = _arrival_frame_fields(state, frame)
    frame = first_replace(frame, candidates=state.table_at(4294955776).cursor(), opponent=state.table_at(4294951680).cursor())
    frame = _movement_move(state, frame, 'unit', 0, 16)
    while True:
        value = frame.candidates.word()
        frame = _movement_move(state, first_replace(frame, candidates=frame.candidates.advance(2)), 'target_y', value, 16)
        if frame.status & 8:
            return frame
        frame = _movement_move(state, frame, 'unit', frame.opponent.byte(low16(frame.target_y)), 8)
        frame = first_replace(frame, controller=state.table_at(4294955798).cursor(), scan=state.table_at(4294955820).cursor())
        while True:
            frame = _movement_test(state, frame, frame.controller.word(), 16)
            if frame.status & 8:
                break
            frame = _movement_compare(state, frame, low16(frame.unit), frame.scan.word(), 16)
            if not frame.status & 5:
                break
            frame = first_replace(frame, controller=frame.controller.advance(2), scan=frame.scan.advance(2))
        while True:
            frame = _movement_move(state, frame, 'offset_x', frame.controller.word(), 16)
            frame = _movement_move(state, frame, 'offset_y', frame.scan.word(), 16)
            frame = _arrival_store_fields(state, frame, frame.controller.base, low16(frame.target_y))
            frame = first_replace(frame, controller=frame.controller.advance(2))
            frame = _arrival_store_fields(state, frame, frame.scan.base, low16(frame.unit))
            frame = first_replace(frame, scan=frame.scan.advance(2))
            frame = _movement_move(state, frame, 'target_y', low16(frame.offset_x), 16)
            if frame.status & 8:
                break
            frame = _movement_move(state, frame, 'unit', low16(frame.offset_y), 16)
        frame = _arrival_store_fields(state, frame, frame.controller.base, 65535)


def assign_ranked_packet_members_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """158A0..158D4: native DBRA count and BYTE city-flag edits, not a clamp."""
    frame = _arrival_frame_fields(state, frame)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
    frame = _arrival_add_fields(state, frame, 'count', 9, True)
    frame = _arrival_add_fields(state, frame, 'target_x', low16(frame.count), True)
    frame = first_replace(frame, candidates=state.table_at(4294955798).cursor(), controller=state.table_at(4294953984).cursor())
    while True:
        value = frame.candidates.word()
        frame = _movement_move(state, first_replace(frame, candidates=frame.candidates.advance(2)), 'target_y', value, 16)
        frame = _arrival_store_fields(state, frame, frame.controller.address(low16(frame.target_y)), low8(frame.distance), 1)
        frame, again = _arrival_db_fields(frame, 'target_x')
        if not again:
            break
    frame = _arrival_bit_fields(state, frame, low8(frame.distance), 7)
    frame = first_replace(frame, distance=replace_byte(frame.distance, low8(frame.distance) | 128))
    while True:
        value = frame.candidates.word()
        frame = _movement_move(state, first_replace(frame, candidates=frame.candidates.advance(2)), 'target_y', value, 16)
        if frame.status & 8:
            break
        frame = _arrival_store_fields(state, frame, frame.controller.address(low16(frame.target_y)), low8(frame.distance), 1)
    frame = _arrival_bit_fields(state, frame, low8(frame.distance), 7)
    return first_replace(frame, distance=replace_byte(frame.distance, low8(frame.distance) & 127))


def compact_arrival_packet_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _arrival_frame_fields(state, frame)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
    frame = first_replace(frame, candidates=frame.roster.advance(s16(low16(frame.target_x)) + 13))
    return _arrival_compact_packet_tail_fields(state, frame)


def detach_packet_force_head_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1596C..159EA: native search/tail shifts and true four-LONG restoration.

    Preserve the original last-member cutoff and BYTE-only city-index merge;
    these are compatibility behaviors, not repaired limits or guessed values.
    """
    frame = _arrival_frame_fields(state, frame)
    saved = ('target_x', 'target_y', 'unit', 'candidates')
    frame = _movement_save_longs(state, frame, saved)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
    frame = _movement_adjust_word(state, frame, 'target_x', -1)
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(0, 4), 8)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
    frame = first_replace(frame, candidates=state.table_at(4294960704).cursor())
    frame = _movement_move(state, frame, 'target_y', frame.candidates.word(low16(frame.target_y)), 16)
    frame = _movement_move(state, frame, 'unit', 0, 16)
    while True:
        frame = _movement_compare(state, frame, low8(frame.target_y), frame.roster.byte(low16(frame.unit), 13), 8)
        if frame.status & 4:
            break
        frame = _movement_adjust_word(state, frame, 'unit', 1)
        frame = _movement_compare(state, frame, low16(frame.unit), low16(frame.target_x), 16)
        if not frame.status & 1:
            return _movement_restore_longs(state, frame, saved)
    while True:
        frame = _movement_adjust_word(state, frame, 'unit', 1)
        frame = _movement_compare(state, frame, low16(frame.unit), low16(frame.target_x), 16)
        if not frame.status & 1:
            break
        value = frame.roster.byte(low16(frame.unit), 13)
        frame = _arrival_store_fields(state, frame, frame.roster.address(low16(frame.unit), 12), value, 1)
    while True:
        frame = _movement_move(state, frame, 'target_x', frame.roster.byte(low16(frame.unit), 13), 8)
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
        if frame.status & 4:
            break
        frame = _arrival_add_fields(state, frame, 'target_x', 12)
        while True:
            value = frame.roster.byte(low16(frame.unit), 13)
            frame = _arrival_store_fields(state, frame, frame.roster.address(low16(frame.unit), 12), value, 1)
            frame = _movement_adjust_word(state, frame, 'unit', 1)
            frame, again = _arrival_db_fields(frame, 'target_x')
            if not again:
                break
    frame = _arrival_store_fields(state, frame, frame.roster.address(low16(frame.unit), 12), 0, 1, True)
    original = frame.roster.byte()
    frame, reduced = _movement_mutation_flags(state, frame, original, -1, 8)
    frame.roster.set_byte(0, reduced)
    frame = first_replace(frame, candidates=state.table_at(4294953984).cursor())
    frame = _movement_move(state, frame, 'unit', low8(frame.distance), 8)
    frame = _movement_adjust_word(state, frame, 'unit', 1)
    frame = _arrival_store_fields(state, frame, frame.candidates.address(low16(frame.target_y)), low8(frame.unit), 1)
    frame = _movement_fixed_shift_word(state, frame, 'unit', 1)
    frame = first_replace(frame, candidates=state.table_at(4294964318).cursor())
    frame = _arrival_store_fields(state, frame, frame.candidates.address(low16(frame.unit)), low16(frame.target_y))
    frame = _movement_adjust_word(state, frame, 'count', 1)
    return _movement_restore_longs(state, frame, saved)


def _arrival_match_coordinate_fields(state, frame) -> tuple:
    """Original six geometric arms, including the retained self-offset CMP."""
    frame = _movement_move(state, frame, 'choice', low16(frame.offset_y), 16)
    frame = _arrival_add_fields(state, frame, 'choice', 24, True)
    frame = _movement_compare(state, frame, low16(frame.target_y), low16(frame.choice), 16)
    if frame.status & 4:
        frame = _movement_move(state, frame, 'choice', low16(frame.offset_x), 16)
        frame = _movement_compare(state, frame, low16(frame.target_x), low16(frame.choice), 16)
        if frame.status & 4:
            return (frame, True)
        frame = _arrival_add_fields(state, frame, 'choice', 16, True)
        frame = _movement_compare(state, frame, low16(frame.target_x), low16(frame.choice), 16)
        if frame.status & 4:
            return (frame, True)
    frame = _movement_move(state, frame, 'choice', low16(frame.offset_y), 16)
    frame = _arrival_add_fields(state, frame, 'choice', 8, True)
    frame = _movement_compare(state, frame, low16(frame.target_y), low16(frame.choice), 16)
    if frame.status & 4:
        frame = _movement_move(state, frame, 'choice', low16(frame.offset_x), 16)
        frame = _arrival_add_fields(state, frame, 'choice', 16)
        frame = _movement_compare(state, frame, low16(frame.target_x), low16(frame.choice), 16)
        if frame.status & 4:
            return (frame, True)
        frame = _movement_compare(state, frame, low16(frame.target_x), low16(frame.offset_x), 16)
        if frame.status & 4:
            return (frame, True)
        frame = _movement_move(state, frame, 'choice', low16(frame.offset_x), 16)
        frame = _arrival_add_fields(state, frame, 'choice', 16, True)
        frame = _movement_compare(state, frame, low16(frame.choice), low16(frame.offset_x), 16)
        if frame.status & 4:
            return (frame, True)
        frame = _movement_move(state, frame, 'choice', low16(frame.offset_x), 16)
        frame = _arrival_add_fields(state, frame, 'choice', 32, True)
        frame = _movement_compare(state, frame, low16(frame.target_x), low16(frame.choice), 16)
        if frame.status & 4:
            return (frame, True)
    frame = _movement_move(state, frame, 'choice', low16(frame.offset_y), 16)
    frame = _arrival_add_fields(state, frame, 'choice', 8, False)
    frame = _movement_compare(state, frame, low16(frame.target_y), low16(frame.choice), 16)
    if frame.status & 4:
        frame = _movement_move(state, frame, 'choice', low16(frame.offset_x), 16)
        frame = _movement_compare(state, frame, low16(frame.target_x), low16(frame.choice), 16)
        if frame.status & 4:
            return (frame, True)
        frame = _arrival_add_fields(state, frame, 'choice', 16, True)
        frame = _movement_compare(state, frame, low16(frame.target_x), low16(frame.choice), 16)
        if frame.status & 4:
            return (frame, True)
    return (frame, False)


def locate_arrival_city_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """164D4..16588: actual external forty-city coordinates, never copied ROM."""
    frame = _arrival_frame_fields(state, frame)
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move(state, frame, 'target_x', frame.candidates.byte(0, 2), 8)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 4)
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    frame = _movement_move(state, frame, 'target_y', frame.candidates.byte(0, 1), 8)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 4)
    frame = first_replace(frame, controller=state.table_at(871114).cursor(), scan=state.table_at(4294964264).cursor())
    frame = _movement_move(state, frame, 'count', 39, 16)
    frame = _movement_move(state, frame, 'distance', 0, 16)
    frame = _arrival_store_fields(state, frame, 4294964114, 1)
    while True:
        value = frame.controller.word()
        frame = _movement_move(state, first_replace(frame, controller=frame.controller.advance(2)), 'offset_x', value, 16)
        value = frame.controller.word()
        frame = _movement_move(state, first_replace(frame, controller=frame.controller.advance(2)), 'offset_y', value, 16)
        frame, matched = _arrival_match_coordinate_fields(state, frame)
        if matched:
            frame = first_replace(frame, controller=state.table_at(4294964264).cursor())
            frame = _movement_move(state, frame, 'target_x', 0, 16)
            return _movement_move(state, frame, 'target_x', frame.controller.byte(low16(frame.distance)), 8)
        frame = _movement_adjust_word(state, frame, 'distance', 1)
        frame = _arrival_memory_increment_fields(state, frame, 4294964114)
        frame, again = _arrival_db_fields(frame, 'count')
        if not again:
            return _movement_move(state, frame, 'target_x', 16, 16)
