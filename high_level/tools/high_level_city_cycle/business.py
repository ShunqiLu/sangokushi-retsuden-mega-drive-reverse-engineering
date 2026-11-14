"""City income, expense, roster and shortage policies with live fixed-width data.

Neutral ledger/table names deliberately do not guess money versus food ownership.
These rules contain no target registers, PCs, instructions or original bytes.
"""
from .domain import *

def credit_primary(state: CityState, city: Word):
    modifiers: Table = state.city_modifiers
    offset: Word = shl16(city, 2)
    factor: Word = sub16(word(100), modifiers.word(offset, 2))
    ledger: Table = state.primary_ledger
    commit_income(state, city, offset, factor, ledger)

def credit_secondary(state: CityState, city: Word):
    modifiers: Table = state.city_modifiers
    offset: Word = shl16(city, 2)
    factor: Long = modifiers.long(offset)
    ledger: Table = state.secondary_ledger
    commit_income(state, city, offset, low_word(factor), ledger)

def commit_income(state: CityState, city: Word, offset: Word, factor: Word, ledger: Table):
    gain: Long = scaled_income(state, offset, factor)
    gain = saturating_add32(gain, ledger.long(offset))
    ledger.set_long(offset, gain)
    deplete_income(state, city, state.depletion_modifiers)

def scaled_income(state: CityState, offset: Word, factor: Word):
    rates: Table = state.secondary_rates
    thresholds: Table = state.depletion_modifiers
    bases: Table = state.income_bases
    factor = mulu16(factor, thresholds.word(offset, 2))
    factor = mulu16(factor, rates.word(offset, 2))
    factor = divu16(factor, 15000)
    gain: Long = bases.long(offset)
    gain = mask32(gain, 65535)
    gain = mulu16(gain, factor)
    return gain

def deplete_income(state: CityState, city: Word, thresholds: Table):
    """Decide the depletion tier, evolve the real seed, then apply live reserve loss."""
    offset: Word = shl16(city, 2)
    threshold: Long = thresholds.long(offset)
    tier: Word = word(0)
    if low_word(threshold) <= 45:
        return
    tier = advance_income_depletion_tier(threshold, tier)
    saved_city: Word = city
    step_random(state)
    city = saved_city
    reduction_factor = read_income_depletion_factor(state, tier)
    apply_income_reserve_depletion(state, city, reduction_factor)

def debit_primary(state: CityState, city: Word):
    modifiers: Table = state.city_modifiers
    factor: Word = word(100)
    offset: Word = shl16(city, 2)
    factor = sub16(factor, modifiers.word(offset, 2))
    ledger: Table = state.primary_ledger
    settle_expense(state, city, factor, ledger)

def debit_secondary(state: CityState, city: Word):
    modifiers: Table = state.city_modifiers
    offset: Word = shl16(city, 2)
    factor: Word = modifiers.word(offset, 2)
    ledger: Table = state.secondary_ledger
    settle_expense(state, city, factor, ledger)

def settle_expense(state: CityState, city: Word, factor: Word, ledger: Table):
    """Build the live roster, price both expense components, settle and commit."""
    categories: Table = state.officer_categories
    city = prepare_city_expense_roster(state, city)
    fees = calculate_city_expense(state, factor, categories)
    offset: Word = shl16(city, 2)
    remaining: Long = ledger.long(offset)
    remaining, borrowed = subtract_borrow32(remaining, fees)
    if borrowed:
        settle_shortage(state, remaining, factor)
        remaining = long(0)
    else:
        remaining = minimum32(remaining, 999999)
    offset = shl16(city, 2)
    ledger.set_long(offset, remaining)

def prepare_city_expense_roster(state: CityState, city: Word) -> Word:
    """Use the original one-based assignment query and freshly write its count."""
    city = add16(city, 1)
    state.set_head(word(-1))
    count: Word = build_roster(state, city)
    state.set_roster_count(count)
    city = sub16(city, 1)
    return city

def sum_roster_expense_amounts(state: CityState) -> Long:
    """Consume the live WORD roster; add each complete amount with LONG wrapping."""
    amounts: Table = state.officer_amounts
    roster: Table = state.roster
    total: Long = long(0)
    while True:
        member: Word = roster.next_word()
        if signed_word(member) < 0:
            break
        member = shl16(member, 2)
        total = add32(total, amounts.long(member))
    return total

def sum_roster_category_fees(state: CityState, categories: Table) -> Word:
    """Re-read the roster and retain the original &5 category/table alias rule."""
    roster = state.roster
    fees_table: Table = state.expense_parameters
    fees: Word = word(0)
    while True:
        member = roster.next_word()
        if signed_word(member) < 0:
            break
        category: Byte = categories.byte(member)
        category = mask16(category, 5)
        category = shl16(category, 1)
        fees = add16(fees, fees_table.word(category))
    return fees

def calculate_city_expense(state: CityState, factor: Word, categories: Table) -> Long:
    """Price amount and category passes without caching their live source reads."""
    total = sum_roster_expense_amounts(state)
    total = stitched_product(total, factor)
    total = divu16(total, 5000)
    fees = sum_roster_category_fees(state, categories)
    fees = mulu16(fees, factor)
    fees = divu16(fees, 100)
    total = mask32(total, 65535)
    fees = mask32(fees, 65535)
    fees = add32(fees, total)
    return fees

def build_roster(state: CityState, city: Word):
    assignments: Table = state.officer_assignments
    roster: Table = state.roster
    officer: Word = word(0)
    count: Word = word(0)
    head: Word = state.head()
    if signed_word(head) >= 0:
        roster.append_word(head)
        count = add16(count, 1)
    while True:
        assigned: Byte = assignments.next_byte()
        if assigned == low_byte(city) and officer != state.head():
            roster.append_word(officer)
            count = add16(count, 1)
        officer = add16(officer, 1)
        if officer >= 256:
            break
    roster.put_word(word(-1))
    return count

def settle_shortage(state: CityState, outstanding: Long, factor: Word):
    """Rank the live roster, deplete quantities, then apply remaining penalties."""
    outstanding = negate32(outstanding)
    outstanding = stitched_product(outstanding, factor)
    build_shortage_priority_scores(state)
    sort_shortage_priority_roster(state)
    outstanding = deplete_shortage_amounts(state, outstanding)
    if outstanding != 0:
        apply_shortage_penalties(state)

def build_shortage_priority_scores(state: CityState) -> None:
    """Read both score components per live member in their original order."""
    roster: Table = state.roster
    scores: Table = state.scores
    first: Table = state.first_score_components
    second: Table = state.second_score_components
    while True:
        member: Word = roster.next_word()
        if signed_word(member) < 0:
            break
        first_score: Long = long(0)
        member = shl16(member, 1)
        first_score = first.word(member)
        score: Long = long(0)
        score = second.word(member)
        score = add32(score, first_score)
        scores.append_long(score)

def sort_shortage_priority_roster(state: CityState) -> None:
    """Swap live score/roster slots together; equal scores keep original ordering."""
    scores = state.scores
    roster = state.roster
    passes: Word = state.roster_count()
    if passes > 1:
        passes = sub16(passes, 1)
        while True:
            compared: Word = word(0)
            member_offset: Word = word(0)
            score_offset: Word = word(0)
            while True:
                left: Long = scores.long(score_offset)
                if left > scores.long(score_offset, 4):
                    scores.set_long(score_offset, scores.long(score_offset, 4))
                    scores.set_long(score_offset, left, 4)
                    left = roster.word(member_offset)
                    roster.set_word(member_offset, roster.word(member_offset, 2))
                    roster.set_word(member_offset, left, 2)
                compared = add16(compared, 1)
                member_offset = add16(member_offset, 2)
                score_offset = add16(score_offset, 4)
                if compared >= passes:
                    break
            passes = sub16(passes, 1)
            if passes == 0:
                break

def deplete_shortage_amounts(state: CityState, outstanding: Long) -> Long:
    """Keep original partial outstanding clear and low-BYTE modifier arithmetic."""
    roster = state.roster
    amounts: Table = state.officer_amounts
    modifiers: Table = state.officer_modifiers
    while True:
        member = roster.next_word()
        if signed_word(member) < 0:
            break
        offset: Word = shl16(member, 2)
        amount: Long = amounts.long(offset)
        if amount > outstanding:
            quantity: Long = outstanding
            outstanding = clear_low_word(outstanding)
        else:
            outstanding = sub32(outstanding, amount)
            quantity = amount
        modifier: Word = word(100)
        modifier = sub8(modifier, modifiers.byte(member))
        quantity = mulu16(quantity, modifier)
        quantity = divu16(quantity, 100)
        quantity = mask32(quantity, 65535)
        amount = sub32(amount, quantity)
        amounts.set_long(offset, amount)
        if outstanding == 0:
            break
    return outstanding

def apply_shortage_penalties(state: CityState) -> None:
    """Freshly scan remaining penalty fields; clamp only actual BYTE underflow."""
    roster = state.roster
    modifiers = state.officer_modifiers
    penalties: Table = state.officer_penalties
    while True:
        member = roster.next_word()
        if signed_word(member) < 0:
            break
        deduction: Long = long(100)
        deduction = sub8(deduction, modifiers.byte(member))
        deduction = divu16(deduction, 10)
        borrowed = penalties.subtract_byte(member, deduction)
        if borrowed:
            penalties.set_byte(member, byte(0))

def advance_income_depletion_tier(threshold: Long, tier: Word) -> Word:
    """Advance the original WORD parameter offset through four ordered bands."""
    if low_word(threshold) > 55:
        tier = add16(tier, 4)
        if low_word(threshold) > 65:
            tier = add16(tier, 4)
            if low_word(threshold) > 75:
                tier = add16(tier, 4)
                if low_word(threshold) > 85:
                    tier = add16(tier, 4)
    return tier

def read_income_depletion_factor(state: CityState, tier: Word) -> Word:
    """Read the live parameter pair around the freshly evolved seed high WORD."""
    parameters: Table = state.depletion_parameters
    reduction_factor: Word = parameters.word(tier)
    reduction_factor = mulu16(reduction_factor, state.seed_high())
    reduction_factor = swap_words(reduction_factor)
    reduction_factor = add16(reduction_factor, parameters.word(tier, 2))
    return reduction_factor

def apply_income_reserve_depletion(state: CityState, city: Word, reduction_factor: Word) -> None:
    """Read then subtract the original scaled WORD reserve loss, without a clamp."""
    reserve: Table = state.depletion_reserve
    offset = shl16(city, 2)
    loss: Word = reserve.word(offset, 2)
    loss = mulu16(loss, reduction_factor)
    loss = divu16(loss, 100)
    reserve.subtract_word(offset, loss, 2)

def step_random(state: CityState):
    seed: Long = state.seed()
    if seed == 0:
        seed = long(0x2A6D365A)
    previous: Long = seed
    seed = shl32(seed, 2)
    seed = add32(seed, previous)
    seed = shl32(seed, 3)
    seed = add32(seed, previous)
    sample: Word = low_word(seed)
    seed = swap_words(seed)
    sample = add16(sample, seed)
    seed = replace_low_word(seed, sample)
    seed = swap_words(seed)
    state.set_seed(seed)
    return sample
