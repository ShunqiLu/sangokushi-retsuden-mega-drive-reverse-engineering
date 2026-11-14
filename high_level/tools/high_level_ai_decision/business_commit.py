"""Live roster decisions, city orders and officer training commitments.

The compatibility rules deliberately retain wrapped WORD offsets, the moving
roster look-up, DIVU overflow retention and the reversed growth-cap correction.
Tables are live views: repeated scalar and table reads are not snapshots.
This module contains business operations, not a CPU or a gameplay-domain claim.
"""
from .domain import AiState, Word, low8, negative_word, s16, u8, u16, u32


def mark_selected_roster_bit14(state: AiState, officer: Word) -> None:
    officer = u16(officer)
    roster = state.roster.cursor()
    while True:
        member = roster.next_word()
        if negative_word(member):
            break
        if member == officer:
            member = u16(member | 16384)
            roster.set_word(65534, member)
            break


def commit_roster_city_assignments(state: AiState) -> None:
    choose_city_head_from_roster(state)
    flag_roster_b600_candidate(state)
    update_roster_c700_status(state)
    state.set_command(5)


def choose_city_head_from_roster(state: AiState) -> None:
    heads = state.city_heads
    city_index = u16(state.current_city() << 1)
    head = heads.word(city_index)
    rulers = state.force_heads
    ruler_index = u16(state.force_selector() << 1)
    if head == rulers.word(ruler_index):
        return
    roster = state.roster.cursor()
    first = state.b600
    second = state.b400
    status = state.c300
    best = u16(0)
    selected = u16(65535)
    while True:
        member = roster.next_word()
        if negative_word(member):
            break
        officer = u16(member & 255)
        if status.byte(officer) < 90:
            continue
        index = u16(officer << 1)
        score = u16(first.word(index) + second.word(index))
        if score > best:
            best = score
            selected = officer
    if not negative_word(selected):
        heads.set_word(city_index, selected)


def flag_roster_b600_candidate(state: AiState) -> None:
    roster = state.roster.cursor()
    attributes = state.b600
    development = state.c000
    best = u16(0)
    selected = u16(65535)
    while True:
        member = roster.next_word()
        if negative_word(member):
            break
        officer = u16(member & 255)
        index = u16(officer << 1)
        score = attributes.word(index)
        if score < 100:
            if score < 95:
                continue
            if development.word(index) < 150:
                continue
        if score >= best:
            best = score
            selected = officer
    if not negative_word(selected):
        flags = state.c700
        flags.set_byte(selected, u8(flags.byte(selected) | 16))


def update_roster_c700_status(state: AiState) -> None:
    roster = state.roster.cursor()
    flags = state.c700
    categories = state.c600
    development = state.c000
    comparison = state.be00
    while True:
        member = roster.next_word()
        if negative_word(member):
            break
        officer = u16(member & 255)
        category = u16(0)
        parameter = categories.byte(officer)
        if parameter >= 5:
            category = u16(category + 1)
            if parameter >= 10:
                category = u16(category + 1)
                if parameter >= 15:
                    category = u16(category + 1)
                    if parameter >= 20:
                        category = u16(category + 1)
        moving_flag = u16(roster.byte(officer) & 7)
        if low8(moving_flag) >= low8(category):
            continue
        index = u16(officer << 1)
        if development.word(index) < comparison.word(index):
            category = u16(category | 8)
        previous = flags.byte(officer)
        flags.set_byte(officer, u8((previous & 16) | low8(category)))


def commit_city_field_order(state: AiState) -> None:
    gates = state.order_gates
    gate_index = u16(state.current_city() << 2)
    if gates.word(gate_index) < 100:
        best, selected = select_order_officer_b600(state)
        state.set_selected_officer(selected)
        if not negative_word(selected):
            prepare_city_order_amount(state)
            orders = state.city_orders
            index = u16(state.current_city() << 1)
            index = u16(index + state.current_city())
            index = u16(index << 2)
            orders.set_word(index, state.selected_officer(), 8)
            amount = state.divide_unsigned(state.order_amount(), 100)
            orders.set_word(index, u16(amount), 10)
            officer = state.selected_officer()
            state.officer_flags.set_byte(officer, 1)
            mark_selected_roster_bit14(state, officer)
    state.set_command(4)


def select_order_officer_b600(state: AiState) -> tuple[Word, Word]:
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
    return best, selected


def prepare_city_order_amount(state: AiState) -> None:
    balances = state.city_balances
    index = u16(state.current_city() << 2)
    amount, remainder = state.divide_signed(balances.long(index), 3)
    if amount > 99999:
        amount = u32(99999)
    state.set_order_amount(amount)


def commit_officer_training(state: AiState) -> None:
    best, selected = select_training_officer_c500(state)
    state.set_selected_officer(selected)
    if not negative_word(selected):
        prepare_officer_training_cost(state)
        balances = state.city_balances
        index = u16(state.current_city() << 2)
        balance = balances.long(index)
        if u32(balance >> 1) >= state.order_amount():
            balance = u32(balance - state.order_amount())
            balances.set_long(index, balance)
            apply_officer_training_growth(state)
            officer = state.selected_officer()
            state.officer_flags.set_byte(officer, 1)
            mark_selected_roster_bit14(state, officer)
    state.set_command(9)


def select_training_officer_c500(state: AiState) -> tuple[Word, Word]:
    roster = state.roster.cursor()
    training = state.c500
    troops = state.c800
    best = u16(65535)
    selected = u16(65535)
    while True:
        member = roster.next_word()
        if negative_word(member):
            break
        if member & 16384:
            continue
        index = u16(member << 2)
        if troops.long(index) == 0:
            continue
        score = training.byte(member)
        if score < low8(best):
            best = u16((best & 65280) | score)
            selected = member
    return best, selected


def prepare_officer_training_cost(state: AiState) -> None:
    troops = state.c800
    index = u16(state.selected_officer() << 2)
    packed = state.divide_unsigned(troops.long(index), 10)
    cost = u32(s16(u16(packed)))
    state.set_order_amount(cost)


def apply_officer_training_growth(state: AiState) -> None:
    state.sample_random()
    index = u16(state.selected_officer() << 1)
    attribute = state.b400.word(index)
    weighted = u16(u16(attribute << 2) + attribute)
    development = state.c000
    weighted = u16(weighted + development.word(index))
    factor = u16((u32(state.seed_word() << 3) >> 16) + 8)
    gain = u16(state.divide_unsigned(u32(weighted * factor), 1000))
    officer = u16(index >> 1)
    training = state.c500
    total = u16(training.byte(officer) + gain)
    if total > 100:
        deficit = u16(100 - total)
        gain = u16(gain - deficit)
        total = u16(100)
    training.set_byte(officer, low8(total))
    index = u16(officer << 1)
    development.set_word(index, u16(development.word(index) + gain))
    if development.word(index) > 999:
        development.set_word(index, 999)
