"""Live recruitment pools, roster movement and battle assignment settlement.

The public inputs are typed game state, complete WORD identifiers and live
views. List tails, wrapped offsets and unusual moving-cursor reads are kept
intentionally; a host DATA projection does not simulate the caller's stack.
"""
from .domain import (
    GameState, Table, Word, Long, CarryOutcome, descending_inclusive,
    u8, u16, u32, s16, low8, low16, replace_word, negative_word, divu_retained,
)


def initialize_recruitment_pool(state: GameState) -> None:
    state.set_next_state(27)
    state.set_allocation_pool(state.working_pool())


def commit_recruitment(state: GameState) -> None:
    index = u16(state.chosen_city() << 2)
    balances = state.balances
    balance = u32(balances.long(index) - state.cost())
    balances.set_long(index, balance)
    state.recruitment_pools.set_long(index, state.working_pool())


def settlement_progress(
    state: GameState, target_offset: Word, source_officer: Word, progress: Table,
) -> tuple[Word, Word]:
    target_offset = u16(target_offset)
    source_officer = u16(source_officer)
    doubled = u16(source_officer << 1)
    raw = progress.word(doubled)
    packed = divu_retained(u32(s16(raw)), 40)
    gain = u16(packed)
    officer = u16(doubled >> 1)
    city_index = u16(state.battle_city() << 1)
    if officer == state.city_heads.word(city_index):
        gain = u16(gain + 30)
    elif officer == state.alternate_heads.word(city_index):
        gain = u16(gain + 30)
    if state.action_flags.byte(officer) & 16:
        gain = u16(gain + 20)
    value = u16(progress.word(target_offset) + gain)
    if value > 999:
        value = u16(999)
    progress.set_word(target_offset, value)
    return value, gain


def remove_battle_roster(state: GameState, officer: Word) -> None:
    officer = u16(officer)
    if state.active_battle() == 0:
        return
    state.officer_assignments.set_byte(officer, 255)
    roster = state.battle_primary_roster.cursor()
    if officer != state.primary_officer():
        roster = state.defender_roster.cursor()
    while True:
        member = roster.next_word()
        if negative_word(member):
            return
        if u16(member & 255) == officer:
            break
    while True:
        member = roster.next_word()
        roster.set_word(65532, member)
        if negative_word(member):
            break


def apply_battle_roster_outcome(state: GameState) -> None:
    if state.active_battle() == 0:
        return
    outcome = state.outcome()
    if outcome < 6:
        return
    if outcome == 6:
        transfer_battle_roster(state, state.winning_officer())
    else:
        transfer_battle_roster(state, state.losing_officer())


def transfer_battle_roster(state: GameState, officer: Word) -> None:
    officer = u16(officer)
    source = state.defender_roster.cursor()
    target = state.secondary_transfer_roster.cursor()
    if officer == state.primary_officer():
        source = state.battle_primary_roster.cursor()
        target = state.primary_transfer_roster.cursor()
    while True:
        member = source.next_word()
        if negative_word(member):
            return
        if u16(member & 255) == officer:
            break
    while True:
        member = source.next_word()
        source.set_word(65532, member)
        if negative_word(member):
            break
    while True:
        member = target.next_word()
        if negative_word(member):
            break
    target.set_word(65534, officer)
    target.set_word(0, 65535)


def remove_original_selected_roster(state: GameState, officer: Word) -> None:
    officer = u16(officer)
    state.officer_assignments.set_byte(officer, 255)
    roster = state.battle_primary_roster.cursor()
    if officer != state.primary_officer():
        roster = state.defender_roster.cursor()
    # This older search deliberately has no negative-terminator guard.
    while True:
        member = roster.next_word()
        if u16(member & 255) == officer:
            break
    while True:
        member = roster.next_word()
        roster.set_word(65532, member)
        if negative_word(member):
            break


def assemble_defender_city_roster(state: GameState) -> Word:
    members = state.officer_flags.cursor()
    roster = state.defender_roster.cursor()
    city = state.battle_city()
    owner = u16(state.city_owners.byte(city))
    state.set_battle_owner(owner)
    doubled = u16(city << 1)
    head = state.city_heads.word(doubled)
    roster.append_word(head)
    city = u16(doubled >> 1)
    count = u16(0)
    for officer in descending_inclusive(u16(255)):
        membership = members.previous_byte()
        if membership != low8(city):
            continue
        if officer == head:
            continue
        roster.append_word(officer)
        count = u16(count + 1)
    roster.set_word(0, 65535)
    state.set_defender_count(count)
    return count


def initialize_prebattle_head_bytes(state: GameState) -> None:
    heads = state.force_heads.cursor()
    statuses = state.officer_status
    for slot in descending_inclusive(u16(15)):
        head = heads.next_word()
        if negative_word(head):
            continue
        statuses.set_byte(head, 100)


def clear_battle_assignment_state(state: GameState) -> None:
    first = state.assignment_a654.cursor()
    second = state.assignment_a754.cursor()
    third = state.assignment_ae28.cursor()
    fourth = state.assignment_ceae.cursor()
    for slot in descending_inclusive(u16(63)):
        first.append_long(0)
        second.append_long(0)
        third.append_long(0)
        fourth.append_long(0)
    state.set_clear_f6e8(65535)
    state.set_clear_f6ea(65535)
    state.set_clear_f6ec(65535)
    state.set_clear_f6ee(65535)
    state.set_clear_f6c8(0)
    state.set_clear_f6f8(0)


def copy_defender_roster_without_head(state: GameState) -> Word:
    target = state.working_roster.cursor()
    source = state.defender_tail.cursor()
    count = u16(0)
    while True:
        member = source.next_word()
        if negative_word(member):
            break
        target.append_word(member)
        count = u16(count + 1)
    target.append_word(65535)
    state.set_working_count(count)
    state.set_battle_count(count)
    return count


def ai_recruitment_capacity_gate(state: GameState) -> CarryOutcome:
    roster = state.ai_roster.cursor()
    capacities = state.capacities
    while True:
        member = roster.next_word()
        if negative_word(member):
            return state.set_carry(True)
        officer = u16(member & 255)
        offset = u16(officer << 1)
        capacity = u32(capacities.word(offset) * 100)
        moving_offset = u16(offset << 1)
        if capacity > roster.long(moving_offset):
            return state.set_carry(False)


def distribute_existing_troop_pool(state: GameState) -> CarryOutcome:
    pools = state.recruitment_pools
    index = u16(state.current_city() << 2)
    remaining = pools.long(index)
    carry = u16(0)
    if remaining != 0:
        roster = state.ai_roster.cursor()
        troops = state.troops
        capacities = state.capacities
        while True:
            member = roster.next_word()
            if negative_word(member):
                carry = u16(1)
                break
            officer = u16(member & 255)
            offset = u16(officer << 1)
            capacity = u32(capacities.word(offset) * 100)
            offset = u16(offset << 1)
            previous = troops.long(offset)
            gain = u32(capacity - previous)
            if capacity < previous:
                gain = u32(0)
            if gain > remaining:
                gain = remaining
            troops.set_long(offset, u32(troops.long(offset) + gain))
            remaining = u32(remaining - gain)
            if remaining == 0:
                break
    pools.set_long(index, remaining)
    return state.set_carry(carry != 0)


def buy_and_distribute_troops(state: GameState, retained_budget: Long) -> None:
    retained_budget = u32(retained_budget)
    roster = state.ai_roster.cursor()
    capacities = state.capacities
    balances = state.balances
    index = u16(state.current_city() << 2)
    balance = balances.long(index)
    if balance < 3000:
        return
    packed = divu_retained(balance, 200)
    quantity = low16(packed)
    remaining = replace_word(retained_budget, quantity)
    if quantity != 0:
        remaining = u32(quantity * 100)
        if remaining > 100000:
            remaining = u32(100000)
            quantity = u16(1000)
        charge = u32(quantity * 100)
        balance = u32(balance - charge)
        balances.set_long(index, balance)
        troops = state.troops
        while True:
            member = roster.next_word()
            if negative_word(member):
                break
            officer = u16(member & 255)
            offset = u16(officer << 1)
            capacity = u32(capacities.word(offset) * 100)
            offset = u16(offset << 1)
            gain = u32(capacity - troops.long(offset))
            if gain > remaining:
                gain = remaining
            troops.set_long(offset, u32(troops.long(offset) + gain))
            remaining = u32(remaining - gain)
            if remaining == 0:
                break
    index = u16(state.current_city() << 2)
    state.recruitment_pools.set_long(index, remaining)

