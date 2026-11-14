"""Battle loss proportions, paired live casualties and award settlement.

No CPU addresses/registers appear in these policies. MemberRemoved is a
nonlocal completion handled by the settlement operation, not ordinary return.
"""
from .domain import BattleState, Word, Long, Table, MemberRemoved, u16, u32, low16, high16, zero_extend_word, add_low_word, divu_retained, random_sample, signed_divmod, complete_removal, uint
from .contexts_settlement import RatioInputs
from .business_members import remove_member, transfer_attacker, transfer_defender

def settle_battle(state: BattleState) -> None:
    quotient, remainder = loss_ratio(state)
    ratio = low16(quotient)
    if defender_needs_scaled_settlement(ratio):
        defender_scaled_loss(state, ratio)
        try:
            attacker_heavy_loss(state, ratio)
        except MemberRemoved:
            pass
        settle_awards(state)
        transfer_attacker(state)
    else:
        try:
            defender_heavy_loss(state, ratio)
        except MemberRemoved:
            pass
        attacker_light_loss(state)
        settle_awards(state)
        transfer_defender(state)

def loss_ratio(state: BattleState) -> tuple[Long, Long]:
    inputs = read_battle_loss_inputs(state)
    return signed_divmod(inputs.numerator, inputs.denominator)

def defender_scaled_loss(state: BattleState, ratio: Word) -> None:
    settle_defender_scaled_loss_capacity(state, ratio)
    settle_defender_scaled_loss_troops(state)

def attacker_heavy_loss(state: BattleState, count_hint: Word) -> None:
    settle_attacker_heavy_loss_capacity(state)
    troops, troop_offset, remaining_troops = settle_attacker_heavy_loss_troops(state)
    if casualty_requires_member_removal(remaining_troops):
        complete_attacker_casualty_removal(state, troops, troop_offset, remaining_troops, count_hint)

def settle_awards(state: BattleState) -> None:
    awards = state.capacity_parameters
    commit_attacker_loss_award(state, awards)
    commit_defender_loss_award(state, awards)

def defender_heavy_loss(state: BattleState, count_hint: Word) -> None:
    settle_defender_heavy_loss_capacity(state)
    troops, troop_offset, remaining_troops = settle_defender_heavy_loss_troops(state)
    if casualty_requires_member_removal(remaining_troops):
        complete_defender_casualty_removal(state, troops, troop_offset, remaining_troops, count_hint)

def attacker_light_loss(state: BattleState) -> None:
    settle_attacker_light_loss_capacity(state)
    settle_attacker_light_loss_troops(state)

def read_attacker_loss_numerator(state: BattleState, parameters: Table, attributes: Table) -> Long:
    selected = state.attacker_officer()
    offset = u16(selected << 1)
    first = attributes.word(offset)
    first_product = u32(first * 10)
    offset = u16(offset << 1)
    numerator = u32(low16(first_product) * parameters.word(offset, 2))
    return numerator

def read_defender_loss_denominator(state: BattleState, parameters: Table, attributes: Table) -> Long:
    selected = state.defender_officer()
    offset = u16(selected << 1)
    denominator_attribute = attributes.word(offset)
    denominator_attribute = u16(denominator_attribute + 1)
    offset = u16(offset << 1)
    index_product = u32(low16(offset) * parameters.word(offset, 2))
    index_product = add_low_word(index_product, 1)
    denominator = u32(low16(denominator_attribute) * low16(index_product))
    return denominator

def read_battle_loss_inputs(state: BattleState) -> RatioInputs:
    parameters = state.capacity_fields
    attributes = state.ratio_attributes
    numerator = read_attacker_loss_numerator(state, parameters, attributes)
    denominator = read_defender_loss_denominator(state, parameters, attributes)
    return RatioInputs(numerator, denominator)

def defender_needs_scaled_settlement(ratio: Word) -> bool:
    uint(ratio, 16)
    return ratio <= 10

def casualty_requires_member_removal(remaining_troops: Word) -> bool:
    uint(remaining_troops, 16)
    return remaining_troops <= 10

def settle_defender_scaled_loss_capacity(state: BattleState, ratio: Word) -> None:
    sample = zero_extend_word(random_sample(state))
    rate = u16(high16(u32(sample * 31)) + 50)
    rate = low16(u32(rate * ratio))
    parameters = state.capacity_fields
    parameter_selector = state.defender_officer()
    parameter_offset = u16(parameter_selector << 2)
    capacity = parameters.word(parameter_offset, 2)
    product = u32(low16(rate) * low16(capacity))
    loss = low16(divu_retained(product, 1000))
    remaining_capacity = u16(capacity - loss)
    parameters.set_word(parameter_offset, remaining_capacity, 2)
    award = low16(divu_retained(zero_extend_word(loss), 100))
    state.set_first_loss_award(award)

def settle_defender_scaled_loss_troops(state: BattleState) -> None:
    sample = zero_extend_word(random_sample(state))
    rate = high16(u32(sample * 31))
    troops = state.troops
    troop_selector = state.defender_officer()
    troop_offset = u16(troop_selector << 1)
    previous_troops = troops.word(troop_offset)
    loss = low16(divu_retained(u32(low16(rate) * low16(previous_troops)), 100))
    remaining_troops = u16(previous_troops - loss)
    if remaining_troops == 0:
        remaining_troops = u16(1)
    troops.set_word(troop_offset, remaining_troops)

def settle_attacker_heavy_loss_capacity(state: BattleState) -> None:
    sample = zero_extend_word(random_sample(state))
    rate = u16(high16(u32(sample * 51)) + 50)
    parameters = state.capacity_fields
    parameter_selector = state.attacker_officer()
    parameter_offset = u16(parameter_selector << 2)
    capacity = parameters.word(parameter_offset, 2)
    product = u32(low16(rate) * low16(capacity))
    loss = low16(divu_retained(product, 100))
    remaining_capacity = u16(capacity - loss)
    parameters.set_word(parameter_offset, remaining_capacity, 2)
    award = low16(divu_retained(zero_extend_word(loss), 100))
    state.set_second_loss_award(award)

def settle_attacker_heavy_loss_troops(state: BattleState) -> tuple[Table, Word, Word]:
    sample = zero_extend_word(random_sample(state))
    rate = high16(u32(sample * 60))
    troops = state.troops
    troop_selector = state.attacker_officer()
    troop_offset = u16(troop_selector << 1)
    previous_troops = troops.word(troop_offset)
    loss = low16(divu_retained(u32(low16(rate) * low16(previous_troops)), 100))
    remaining_troops = u16(previous_troops - loss)
    troops.set_word(troop_offset, remaining_troops)
    return (troops, troop_offset, remaining_troops)

def complete_attacker_casualty_removal(state: BattleState, troops: Table, troop_offset: Word, remaining_troops: Word, count_hint: Word) -> None:
    troops.set_word(troop_offset, 0)
    object_view = state.packed_entities
    offsets = state.packed_offsets
    object_index = state.object_index()
    object_view = object_view.at(offsets.word(object_index))
    officer = state.attacker_officer()
    owner_hint = remaining_troops
    outcome = remove_member(state, officer, object_view, owner_hint, count_hint)
    complete_removal(outcome)
    state.add_second_loss_award(outcome.award_word)

def settle_defender_heavy_loss_capacity(state: BattleState) -> None:
    sample = zero_extend_word(random_sample(state))
    rate = u16(high16(u32(sample * 51)) + 50)
    parameters = state.capacity_fields
    parameter_selector = state.defender_officer()
    parameter_offset = u16(parameter_selector << 2)
    capacity = parameters.word(parameter_offset, 2)
    product = u32(low16(rate) * low16(capacity))
    loss = low16(divu_retained(product, 100))
    remaining_capacity = u16(capacity - loss)
    parameters.set_word(parameter_offset, remaining_capacity, 2)
    award = low16(divu_retained(zero_extend_word(loss), 100))
    state.set_first_loss_award(award)

def settle_defender_heavy_loss_troops(state: BattleState) -> tuple[Table, Word, Word]:
    sample = zero_extend_word(random_sample(state))
    rate = high16(u32(sample * 61))
    troops = state.troops
    troop_selector = state.defender_officer()
    troop_offset = u16(troop_selector << 1)
    previous_troops = troops.word(troop_offset)
    loss = low16(divu_retained(u32(low16(rate) * low16(previous_troops)), 100))
    remaining_troops = u16(previous_troops - loss)
    troops.set_word(troop_offset, remaining_troops)
    return (troops, troop_offset, remaining_troops)

def complete_defender_casualty_removal(state: BattleState, troops: Table, troop_offset: Word, remaining_troops: Word, count_hint: Word) -> None:
    troops.set_word(troop_offset, 0)
    object_view = Table(state, state.opposing_object())
    officer = state.defender_officer()
    owner_hint = troop_offset
    outcome = remove_member(state, officer, object_view, owner_hint, count_hint)
    complete_removal(outcome)
    state.add_first_loss_award(outcome.award_word)

def settle_attacker_light_loss_capacity(state: BattleState) -> None:
    sample = zero_extend_word(random_sample(state))
    rate = u16(high16(u32(sample * 31)) + 30)
    parameters = state.capacity_fields
    parameter_selector = state.attacker_officer()
    parameter_offset = u16(parameter_selector << 2)
    capacity = parameters.word(parameter_offset, 2)
    product = u32(low16(rate) * low16(capacity))
    loss = low16(divu_retained(product, 100))
    remaining_capacity = u16(capacity - loss)
    parameters.set_word(parameter_offset, remaining_capacity, 2)
    award = low16(divu_retained(zero_extend_word(loss), 100))
    state.set_second_loss_award(award)

def settle_attacker_light_loss_troops(state: BattleState) -> None:
    sample = zero_extend_word(random_sample(state))
    rate = high16(u32(sample * 31))
    troops = state.troops
    troop_selector = state.attacker_officer()
    troop_offset = u16(troop_selector << 1)
    previous_troops = troops.word(troop_offset)
    loss = low16(divu_retained(u32(low16(rate) * low16(previous_troops)), 100))
    remaining_troops = u16(previous_troops - loss)
    if remaining_troops == 0:
        remaining_troops = u16(1)
    troops.set_word(troop_offset, remaining_troops)

def commit_attacker_loss_award(state: BattleState, awards: Table) -> None:
    selected = state.attacker_officer()
    offset = u16(selected << 1)
    previous = awards.word(offset)
    updated = u16(previous + state.first_loss_award())
    if updated > 999:
        updated = u16(999)
    awards.set_word(offset, updated)

def commit_defender_loss_award(state: BattleState, awards: Table) -> None:
    selected = state.defender_officer()
    offset = u16(selected << 1)
    previous = awards.word(offset)
    updated = u16(previous + state.second_loss_award())
    if updated > 999:
        updated = u16(999)
    awards.set_word(offset, updated)
