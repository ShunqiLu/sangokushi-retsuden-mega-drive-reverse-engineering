"""Live economy, recruitment and equipment policy with fixed-width behavior.

Original mistakes are deliberately preserved. Explicit retained contexts are
conditional inputs, not evidence that gameplay callers zeroed those values.
"""
from .domain import (
    GameState, Word, Long, Table, uint, u16, u32, low8, low16, high16,
    replace_byte, swap_words, s16, negative_byte, negative_word,
    descending_inclusive, divu_retained,
)
from .contexts_training import (
    TrainingCandidate, TrainingOrder, checked_training_candidate,
    checked_training_order,
)
from .contexts_equipment import (
    EquipmentPurchaseViews, OfficerEquipmentCategories, EquipmentQuote,
    EquipmentBudgetDecision, checked_equipment_quote, checked_equipment_views,
)
from .contexts_recruitment import (
    RecruitmentBest, RecruitmentCandidate, RecruitmentNeighborViews,
    RecruitmentOrder, RecruitmentPredicate, checked_recruitment_best, checked_recruitment_candidate,
    checked_recruitment_submission_order,
)
from .contexts_domestic import (
    DomesticOfficer, CityBudgetBalance, ResourceSupportViews,
    CitySupplyRequirement, ResourceSupportCandidate, CityResourceOrder,
    DomesticPredicate, checked_city_resource_order,
)


def select_welfare_officer(state: GameState) -> tuple[Word, Word]:
    """Keep the original two-WORD ABI while exposing a named officer query."""
    candidate = query_welfare_officer(state)
    return candidate.score, candidate.officer


def query_welfare_officer(state: GameState) -> DomesticOfficer:
    """Select from live eligible members, masking identity only in this query."""
    roster = state.economy_roster.cursor()
    intelligence = state.officer_intelligence
    education = state.officer_education
    best_score = u16(0)
    best_officer = u16(65535)
    while True:
        officer = roster.next_word()
        if negative_word(officer):
            break
        if officer & 16384 != 0:
            continue
        officer = u16(officer & 255)
        score = u16(education.byte(officer))
        index = u16(officer << 1)
        score = u16(score + intelligence.word(index))
        if domestic_officer_score_is_better(score, best_score):
            best_score = score
            best_officer = officer
    return DomesticOfficer(best_score, best_officer)


def plan_welfare_budget(state: GameState) -> None:
    """Consume the real sample, read the city balance, decide and submit amount."""
    factor = sample_domestic_budget_factor(state, 20)
    funding = read_domestic_budget_balance(state)
    budget = calculate_domestic_budget(state, funding.balance, factor)
    submit_domestic_order_amount(state, budget)


def select_development_officer(state: GameState) -> tuple[Word, Word]:
    """Preserve the public two-WORD return, including full-WORD member aliases."""
    candidate = query_development_officer(state)
    return candidate.score, candidate.officer


def query_development_officer(state: GameState) -> DomesticOfficer:
    roster = state.economy_roster.cursor()
    intelligence = state.officer_intelligence
    best_score = u16(0)
    best_officer = u16(65535)
    while True:
        officer = roster.next_word()
        if negative_word(officer):
            break
        if officer & 16384 != 0:
            continue
        index = u16(officer << 1)
        score = intelligence.word(index)
        if domestic_officer_score_is_better(score, best_score):
            best_score = score
            best_officer = officer
    return DomesticOfficer(best_score, best_officer)


def domestic_officer_score_is_better(score: Word, best_score: Word) -> DomesticPredicate:
    """Strict unsigned WORD improvement keeps the first eligible tie."""
    score = uint(score, 16)
    best_score = uint(best_score, 16)
    return score > best_score


def plan_development_budget(state: GameState) -> None:
    """Preserve the original overwritten random factor rather than correcting it."""
    discarded_factor = sample_domestic_budget_factor(state, 30)
    funding = read_domestic_budget_balance(state)
    factor = funding.city_offset
    budget = calculate_domestic_budget(state, funding.balance, factor)
    submit_domestic_order_amount(state, budget)


def sample_domestic_budget_factor(state: GameState, base: Word) -> Word:
    """One actual RNG call and the original partial-width sample arithmetic."""
    base = uint(base, 16)
    sample = u32(low16(state.sample_random()))
    original_sample = sample
    sample = u32(sample << 2)
    sample = u32(sample + original_sample)
    sample = u32(sample << 2)
    sample = u32(sample + original_sample)
    sample = swap_words(sample)
    return u16(low16(sample) + base)


def read_domestic_budget_balance(state: GameState) -> CityBudgetBalance:
    """Read after RNG; keep the gold view live and city offset exactly WORD-wide."""
    gold = state.city_gold
    city = u16(state.current_city() << 2)
    balance = gold.long(city)
    return CityBudgetBalance(gold, city, balance)


def calculate_domestic_budget(state: GameState, balance: Long, factor: Word) -> Long:
    """Original stitched WORD products and signed division, not a new money formula."""
    balance = uint(balance, 32)
    factor = uint(factor, 16)
    lower_product = u32(low16(balance) * factor)
    balance = swap_words(balance)
    balance = u32(low16(balance) * factor)
    balance = swap_words(balance)
    balance = u32(balance + lower_product)
    budget, remainder = state.divide_signed(balance, 100)
    return cap_domestic_order_amount(budget)


def cap_domestic_order_amount(budget: Long) -> Long:
    """The returned LONG bit pattern is compared unsigned, including negative quotients."""
    budget = uint(budget, 32)
    if budget > 9999:
        budget = u32(9999)
    return budget


def submit_domestic_order_amount(state: GameState, amount: Long) -> None:
    amount = uint(amount, 32)
    state.set_order_amount(amount)


def select_resource_support_city(state: GameState) -> tuple[Long, Word]:
    """Preserve the resource total/city compatibility interface."""
    candidate = query_resource_support_city(state)
    return candidate.total, candidate.city


def read_resource_support_views(state: GameState) -> ResourceSupportViews:
    """Capture live starting views, including the original predecrement owners."""
    force = state.current_force()
    current_city = state.current_city()
    troops = state.officer_troops
    gold = state.city_gold
    rice = state.city_rice
    processed = state.city_processed
    owners = state.city_owners_predecrement.cursor()
    return ResourceSupportViews(force, current_city, troops, gold, rice, processed, owners)


def query_resource_support_city(state: GameState) -> ResourceSupportCandidate:
    """Select the actual deficient city's minimum wrapped gold-plus-rice total.

    After the first requirement call, filtering genuinely uses its rebound
    assignment-table view. Later cities are not filtered using a cached flag.
    """
    views = read_resource_support_views(state)
    minimum = u32(4294967295)
    selected = u16(65535)
    processed = views.processed
    for city in descending_inclusive(40):
        if city == 0:
            break
        owner = views.owners.previous_byte()
        if low8(views.force) != owner:
            continue
        if processed.byte(city) != 0:
            continue
        if city == views.current_city:
            continue
        need = estimate_resource_support_need(state, city, views.troops)
        processed = need.next_filter
        index = u16(city << 2)
        if city_supply_is_sufficient(need.required, views.rice.long(index)):
            continue
        total = read_resource_support_total(views.gold, views.rice, index)
        if resource_support_total_is_better(total, minimum):
            minimum = total
            selected = city
    return ResourceSupportCandidate(minimum, selected)


def estimate_resource_support_need(state: GameState, city: Word, troops: Table) -> CitySupplyRequirement:
    """Return the real requirement and the callee's live A4-rebind compatibility."""
    requirement = estimate_city_troop_requirement(state, city, troops)
    return CitySupplyRequirement(requirement, state.officer_assignments)


def read_resource_support_total(gold: Table, rice: Table, index: Word) -> Long:
    gold = gold.state.checked_table(gold)
    rice = gold.state.checked_table(rice)
    index = uint(index, 16)
    total = gold.long(index)
    return u32(total + rice.long(index))


def city_supply_is_sufficient(required: Long, available: Long) -> DomesticPredicate:
    required = uint(required, 32)
    available = uint(available, 32)
    return required <= available


def resource_support_total_is_better(total: Long, minimum: Long) -> DomesticPredicate:
    total = uint(total, 32)
    minimum = uint(minimum, 32)
    return total < minimum


def estimate_city_troop_requirement(state: GameState, city: Word, troops: Table) -> Long:
    city = uint(city, 16)
    troops = state.checked_table(troops)
    total = read_city_assigned_troop_load(state, city, troops)
    return convert_city_troop_load_to_requirement(total)


def read_city_assigned_troop_load(state: GameState, city: Word, troops: Table) -> Long:
    """Predecrement through all 256 assignments and add the original per-member margin."""
    city = uint(city, 16)
    troops = state.checked_table(troops)
    assignments = state.officer_action_predecrement.cursor()
    total = u32(0)
    for officer in descending_inclusive(255):
        assignment = u16(assignments.previous_byte() & 63)
        if assignment == city:
            index = u16(officer << 2)
            total = u32(total + troops.long(index))
            total = u32(total + 100)
    return total


def convert_city_troop_load_to_requirement(total: Long) -> Long:
    """Preserve DIVU overflow retention and the following low-WORD projection."""
    total = uint(total, 32)
    total = divu_retained(total, 10)
    total = u32(low16(total))
    saved_total = total
    total = u32(total << 3)
    total = u32(total + saved_total)
    return total


def plan_city_defense_target(state: GameState) -> None:
    state.sample_random()
    summary = state.force_summary
    index = u16(state.current_force() << 2)
    tier = u16(summary.word(index) - 5)
    if tier > 3:
        tier = u16(3)
    saved_tier = tier
    tier = u16(tier << 2)
    tier = u16(tier + saved_tier)
    target = u16(55 - tier)
    sample = u32(state.seed_word())
    saved_sample = sample
    sample = u32(sample << 2)
    sample = u32(sample + saved_sample)
    sample = u32(sample << 1)
    sample = swap_words(sample)
    target = u16(target + low16(sample))
    defense = state.city_defense_targets
    welfare = state.city_welfare
    city = u16(state.current_city() << 2)
    if welfare.long(city) < 40:
        target = u16(target - 10)
    defense.set_long(city, u32(s16(target)))


def plan_force_support_action(state: GameState) -> None:
    state.sample_random()
    owned = state.count_force_cities(state.current_force())
    cities, rival = state.select_force_by_city_count()
    if negative_word(rival):
        state.set_command(2)
        return
    threshold = u16(2)
    if cities <= owned:
        threshold = u16(1)
    sample = u32(state.seed_word())
    sample = u32(sample << 3)
    sample = swap_words(sample)
    if low16(sample) >= threshold:
        state.set_command(2)
    else:
        state.set_support_city(rival)
        state.set_support_amount(0)
        state.set_command(7)


def clear_economy_command(state: GameState) -> None:
    state.set_command(65535)


def count_economy_roster(state: GameState) -> Word:
    roster = state.economy_roster.cursor()
    count = u16(0)
    while True:
        if negative_word(roster.next_word()):
            break
        count = u16(count + 1)
    return count


def select_roster_intelligence_max(state: GameState) -> tuple[Word, Word]:
    roster = state.economy_roster.cursor()
    intelligence = state.officer_intelligence
    best_score = u16(0)
    best_officer = u16(65535)
    while True:
        officer = roster.next_word()
        if negative_word(officer):
            break
        score = intelligence.word(u16(officer << 1))
        if score > best_score:
            best_score = score
            best_officer = officer
    return best_score, best_officer


def plan_foreign_officer_recruitment(state: GameState) -> None:
    """Query eligible foreign members, decide an order, then commit its fields.

    The shared roster builder really runs before the capacity decision. RNG is
    called exactly once only after an eligible candidate passes both gates.
    """
    count = read_recruitment_city_roster_count(state)
    if not recruitment_city_has_capacity(count):
        state.set_command(3)
        return
    candidate = query_foreign_recruitment_candidate(state)
    order = decide_foreign_recruitment_candidate(candidate)
    if order is RecruitmentOrder.FALLBACK:
        submit_foreign_recruitment_order(state, order, candidate)
        return
    sample = state.sample_random()
    order = decide_foreign_recruitment_lottery(sample)
    submit_foreign_recruitment_order(state, order, candidate)


def read_recruitment_city_roster_count(state: GameState) -> Word:
    """Preserve the real builder's live DATA and exclusion write, not a count cache."""
    city = state.current_city()
    state.set_roster_exclusion(65535)
    return state.build_roster(city)


def recruitment_city_has_capacity(count: Word) -> RecruitmentPredicate:
    count = uint(count, 16)
    return count < 10


def decide_foreign_recruitment_candidate(candidate: RecruitmentCandidate) -> RecruitmentOrder:
    """Reject absent or jointly low-scoring candidates without consuming RNG."""
    candidate = checked_recruitment_candidate(candidate)
    if negative_word(candidate.officer):
        return RecruitmentOrder.FALLBACK
    if candidate.primary_score < 75 and candidate.secondary_score < 75:
        return RecruitmentOrder.FALLBACK
    return RecruitmentOrder.ATTEMPT


def decide_foreign_recruitment_lottery(sample: Long) -> RecruitmentOrder:
    """Resolve the real sample's bit4; no random call or seed reread occurs here."""
    sample = uint(sample, 32)
    if sample & 16 != 0:
        return RecruitmentOrder.FALLBACK
    return RecruitmentOrder.RECRUIT


def submit_foreign_recruitment_order(state: GameState, order: RecruitmentOrder, candidate: RecruitmentCandidate) -> None:
    """Encode the resolved order, retaining the original three-write sequence."""
    order = checked_recruitment_submission_order(order)
    candidate = checked_recruitment_candidate(candidate)
    if order is RecruitmentOrder.FALLBACK:
        state.set_command(3)
    else:
        state.set_candidate_officer(candidate.officer)
        state.set_selected_city(candidate.city)
        state.set_command(6)


def select_foreign_neighbor_officer(state: GameState) -> tuple[Word, Word, Word, Word, Word]:
    """Keep the five-WORD public ABI for callers outside this domain chain."""
    candidate = query_foreign_recruitment_candidate(state)
    return candidate.score, candidate.officer, candidate.city, candidate.primary_score, candidate.secondary_score


def read_foreign_recruitment_views(state: GameState) -> RecruitmentNeighborViews:
    """Capture the original live view bindings and current city/force read order."""
    neighbors = state.neighbors.at(u16(state.current_city() << 3)).cursor()
    force = state.current_force()
    primary = state.officer_primary_attribute
    secondary = state.officer_intelligence
    status = state.officer_status
    owners = state.city_owners
    processed = state.city_processed
    return RecruitmentNeighborViews(neighbors, force, primary, secondary, status, owners, processed)


def query_foreign_recruitment_candidate(state: GameState) -> RecruitmentCandidate:
    """Scan live foreign neighbors, then reread the winner's actual attributes.

    Owner is checked both before and inside each city scan, in original order.
    Returned score lanes retain caller-supplied WORDs if no officer wins.
    """
    views = read_foreign_recruitment_views(state)
    best = RecruitmentBest(0, 65535, 65535)
    first = state.neighbor_selection_context.retained_first_score
    second = state.neighbor_selection_context.retained_second_score
    while True:
        city = u16(views.neighbors.next_byte())
        if negative_byte(low8(city)):
            break
        if views.processed.byte(city) != 0:
            continue
        if views.owners.byte(city) == low8(views.force):
            continue
        best = query_recruitment_city_candidate(state, city, best, views.primary, views.secondary, views.status)
    if not negative_word(best.officer):
        index = u16(best.officer << 1)
        first = views.primary.word(index)
        second = views.secondary.word(index)
    return RecruitmentCandidate(best.score, best.officer, best.city, first, second)


def scan_city_officer_candidate(state: GameState, city: Word, best_score: Word,
                                best_officer: Word, best_city: Word,
                                primary: Table, secondary: Table, status: Table) -> tuple[Word, Word, Word]:
    """Original three-WORD scan ABI; supplied tables remain actual live aliases."""
    city = uint(city, 16)
    best_score = uint(best_score, 16)
    best_officer = uint(best_officer, 16)
    best_city = uint(best_city, 16)
    primary = state.checked_table(primary)
    secondary = state.checked_table(secondary)
    status = state.checked_table(status)
    best = query_recruitment_city_candidate(state, city, RecruitmentBest(best_score, best_officer, best_city), primary, secondary, status)
    return best.score, best.officer, best.city


def query_recruitment_city_candidate(state: GameState, city: Word, best: RecruitmentBest, primary: Table, secondary: Table, status: Table) -> RecruitmentBest:
    """Filter and score actual members in descending inclusive 255..0 order."""
    city = uint(city, 16)
    best = checked_recruitment_best(best)
    primary = state.checked_table(primary)
    secondary = state.checked_table(secondary)
    status = state.checked_table(status)
    owner = u16(state.city_owners.byte(city))
    if negative_byte(low8(owner)):
        return best
    leader = state.force_heads.word(u16(owner << 1))
    assignments = state.officer_assignments
    for officer in descending_inclusive(255):
        if assignments.byte(officer) != low8(city):
            continue
        if low8(officer) == low8(leader):
            continue
        if status.byte(officer) > 65:
            continue
        score = read_recruitment_officer_score(primary, secondary, officer)
        if recruitment_score_is_better(score, best.score):
            best = RecruitmentBest(score, officer, city)
    return best


def read_recruitment_officer_score(primary: Table, secondary: Table, officer: Word) -> Word:
    """Read both components in order and retain the original WORD sum wrap."""
    primary = primary.state.checked_table(primary)
    secondary = primary.state.checked_table(secondary)
    officer = uint(officer, 16)
    index = u16(officer << 1)
    score = primary.word(index)
    return u16(score + secondary.word(index))


def recruitment_score_is_better(score: Word, best_score: Word) -> RecruitmentPredicate:
    """Strictly better WORD scores win; ties retain the first scanned member."""
    score = uint(score, 16)
    best_score = uint(best_score, 16)
    return score > best_score


def choose_resource_action(state: GameState) -> None:
    """Read the actual balance, choose a named order, encode its original command."""
    balance = read_current_resource_balance(state)
    order = decide_city_resource_order(balance)
    submit_city_resource_order(state, order)


def read_current_resource_balance(state: GameState) -> Long:
    gold = state.city_gold
    city = u16(state.current_city() << 2)
    return gold.long(city)


def decide_city_resource_order(balance: Long) -> CityResourceOrder:
    balance = uint(balance, 32)
    if balance >= 10000:
        return CityResourceOrder.FUNDED
    return CityResourceOrder.LIMITED


def submit_city_resource_order(state: GameState, order: CityResourceOrder) -> None:
    """Only compatibility command codes live here; no extra selection/RNG is invented."""
    order = checked_city_resource_order(order)
    if order is CityResourceOrder.FUNDED:
        state.set_command(7)
    else:
        state.set_command(4)


def choose_training_action(state: GameState) -> None:
    """Query live candidates, decide a named order, then commit its encoding."""
    candidate = query_training_candidate(state)
    order = decide_training_order(candidate)
    submit_training_order(state, order)


def select_roster_training_min(state: GameState) -> tuple[Word, Word]:
    """Preserve the original two-WORD public ABI for existing logical callers."""
    candidate = query_training_candidate(state)
    return candidate.minimum_score, candidate.officer_id


def query_training_candidate(state: GameState) -> TrainingCandidate:
    """Scan live RAM without snapshotting, masking member IDs or altering ties.

    The lowest score wins; equal scores retain the first eligible member.
    A negative WORD terminates, bit14 excludes, and the full member WORD is
    the signed effective-address offset of the BYTE training read. The score
    lane starts at zero and each read replaces only its low BYTE, just as the
    original entry does. No eligible member leaves the original 0xFFFF pair.
    """
    roster = state.economy_roster.cursor()
    training = state.officer_training
    best_score = u16(65535)
    best_officer = u16(65535)
    score = u16(0)
    while True:
        officer = roster.next_word()
        if negative_word(officer):
            break
        if officer & 16384 != 0:
            continue
        score = u16(replace_byte(score, training.byte(officer)))
        if score < best_score:
            best_score = score
            best_officer = officer
    return TrainingCandidate(best_score, best_officer)


def decide_training_order(candidate: TrainingCandidate) -> TrainingOrder:
    """Pure training policy: this comparison is a source-driven native rule.

    No state read, command encoding or 'no candidate' special case occurs here.
    The finite backend admits one unsigned WORD comparison (<, <=, >, >=, ==,
    !=) against a literal WORD and either named order on each branch.
    """
    candidate = checked_training_candidate(candidate)
    if candidate.minimum_score < 80:
        return TrainingOrder.TRAIN
    return TrainingOrder.ALTERNATE


def submit_training_order(state: GameState, order: TrainingOrder) -> None:
    """Compatibility writeback: keep machine command IDs out of the policy.

    Command 9 remains the alternate branch; its wider meaning is not guessed.
    Exactly one original WORD command write is performed after the live scan.
    """
    order = checked_training_order(order)
    if order is TrainingOrder.TRAIN:
        state.set_command(8)
    else:
        state.set_command(9)


def commit_recruitment_candidate(state: GameState) -> None:
    """Recheck capacity, assign the live candidate and reward the selected officer.

    These are intentionally different identities. The current city is reread
    after the builder and before the assignment; no plan-time snapshot is used.
    """
    count = read_recruitment_city_roster_count(state)
    if recruitment_city_has_capacity(count):
        assign_live_recruitment_candidate(state)
        reward_selected_recruitment_officer(state)
    state.set_command(8)


def assign_live_recruitment_candidate(state: GameState) -> None:
    """Commit only the original candidate's city assignment BYTE."""
    city = state.current_city()
    assignments = state.officer_assignments
    candidate = state.candidate_officer()
    assignments.set_byte(candidate, low8(city))


def reward_selected_recruitment_officer(state: GameState) -> None:
    """Read the independently selected officer, then write progress/action/mark."""
    progress = state.officer_progress
    officer = u16(state.selected_officer() << 1)
    gain = compute_recruitment_progress_gain(progress.word(officer))
    progress.set_word(officer, gain)
    officer = u16(officer >> 1)
    action = state.officer_action
    action.set_byte(officer, 1)
    state.mark_selected_roster_bit14(officer)


def compute_recruitment_progress_gain(current: Word) -> Word:
    """Add before capping, preserving WORD overflow rather than saturating first."""
    current = uint(current, 16)
    gain = u16(current + 10)
    if gain > 999:
        gain = u16(999)
    return gain


def select_unmarked_roster_intelligence_max(state: GameState) -> tuple[Word, Word]:
    roster = state.economy_roster.cursor()
    intelligence = state.officer_intelligence
    best_score = u16(0)
    best_officer = u16(65535)
    while True:
        officer = roster.next_word()
        if negative_word(officer):
            break
        if officer & 16384 != 0:
            continue
        score = intelligence.word(u16(officer << 1))
        if score > best_score:
            best_score = score
            best_officer = officer
    return best_score, best_officer


def clear_candidate_city_order(state: GameState) -> None:
    orders = state.city_orders
    city = u16(state.selected_city() << 1)
    city = u16(city + state.selected_city())
    city = u16(city << 2)
    candidate = state.candidate_officer()
    if candidate == orders.word(city):
        orders.set_word(city, 65535)
    elif candidate == orders.word(city, 4):
        orders.set_word(city, 65535, 4)
    elif candidate == orders.word(city, 8):
        orders.set_word(city, 65535, 8)


def plan_equipment_action(state: GameState) -> None:
    city = u16(state.current_city() << 1)
    head = state.city_heads.word(city)
    action = state.officer_action
    if action.byte(head) == 0:
        sort_equipment_roster(state)
        purchase_roster_equipment(state)
    state.set_command(10)


def sort_equipment_roster(state: GameState) -> None:
    roster = state.economy_roster.cursor()
    attributes = state.officer_primary_attribute
    work = state.equipment_work.cursor()
    count = u16(0)
    while True:
        officer = roster.next_word()
        if negative_word(officer):
            break
        officer = u16(officer & 255)
        index = u16(officer << 1)
        work.append_word(attributes.word(index))
        count = u16(count + 1)
    if count == 1:
        return
    limit = u16(count << 1)
    work = state.equipment_work
    roster = state.economy_roster
    while True:
        index = u16(2)
        while True:
            previous = work.word(index, -2)
            if previous < work.word(index):
                previous = work.word(index)
                work.set_word(index, work.word(index, -2))
                work.set_word(index, previous, -2)
                previous = roster.word(index)
                roster.set_word(index, roster.word(index, -2))
                roster.set_word(index, previous, -2)
            index = u16(index + 2)
            if index >= limit:
                break
        limit = u16(limit - 2)
        if limit <= 2:
            break


def purchase_roster_equipment(state: GameState) -> None:
    """Run the complete live batch, separating quotes, policy and writeback.

    Each member still stops after the first purchase or rejected quote. Rejected
    prices do not try a later category. The level WORD persists between category
    and member iterations, and the final gold write occurs even for an empty
    roster. Compatibility anomalies are preserved by the named write helpers.
    """
    views = read_equipment_purchase_views(state)
    remaining = views.initial_balance
    level = views.retained_level
    while True:
        officer = views.roster.next_word()
        if negative_word(officer):
            break
        selection = read_officer_equipment_categories(state, views.attributes, officer)
        while True:
            category = u16(selection.categories.next_byte())
            if negative_byte(low8(category)):
                break
            level = read_equipment_level(views.equipment, category, selection.equipment_row, level)
            if level >= 3:
                continue
            quote = read_equipment_quote(state, category, level)
            level = quote.next_level
            decision = decide_equipment_budget(quote, remaining)
            if decision is EquipmentBudgetDecision.REJECT:
                break
            remaining = commit_equipment_purchase(views.equipment, remaining, quote)
            break
    settle_equipment_balance(views, remaining)


def read_equipment_purchase_views(state: GameState) -> EquipmentPurchaseViews:
    """Capture the original entry DATA sequence and retain live table aliases."""
    roster = state.economy_roster.cursor()
    attributes = state.officer_primary_attribute
    gold = state.city_gold
    city = u16(state.current_city() << 2)
    remaining = gold.long(city)
    equipment = state.officer_equipment
    level = u16(state.equipment_scan_context.retained_level_high_byte << 8)
    return EquipmentPurchaseViews(roster, attributes, gold, equipment, city, remaining, level)


def read_officer_equipment_categories(state: GameState, attributes: Table, officer: Word) -> OfficerEquipmentCategories:
    """Read the member's live attribute, then select the original category row."""
    attributes = state.checked_table(attributes)
    officer = u16(uint(officer, 16) & 255)
    index = u16(officer << 1)
    score = attributes.word(index)
    category_row = u16(0)
    if score < 100:
        category_row = u16(category_row + 4)
        if score < 60:
            category_row = u16(category_row + 4)
    categories = state.equipment_categories.at(category_row).cursor()
    officer_row = u16(index >> 1)
    officer_row = u16(officer_row + index)
    return OfficerEquipmentCategories(categories, officer_row)


def read_equipment_level(equipment: Table, category: Word, officer_row: Word, retained_level: Word) -> Word:
    """Replace only the low BYTE; do not zero or normalize the retained prefix."""
    equipment = equipment.state.checked_table(equipment)
    category = uint(category, 16)
    officer_row = uint(officer_row, 16)
    retained_level = uint(retained_level, 16)
    equipment_slot = u16(category + officer_row)
    return u16(replace_byte(retained_level, equipment.byte(equipment_slot)))


def read_equipment_quote(state: GameState, category: Word, level: Word) -> EquipmentQuote:
    """Read price through the original full WORD index and signed effective EA.

    The index uses the current level, while the quote retains its next level.
    Width truncations and the external price source are compatibility, not an
    editor clamp or a new category/level validity rule.
    """
    category = uint(category, 16)
    level = uint(level, 16)
    price_slot = u16(category << 1)
    price_slot = u16(price_slot + category)
    price_slot = u16(price_slot + level)
    next_level = u16(level + 1)
    price_slot = u16(price_slot << 2)
    price = state.equipment_prices.long(price_slot)
    return EquipmentQuote(category, next_level, price)


def decide_equipment_budget(quote: EquipmentQuote, remaining_gold: Long) -> EquipmentBudgetDecision:
    """Pure budget admission: compare unsigned price to one quarter of balance.

    A single source relation (> >= < <= == !=) is lowered to the corresponding
    unsigned CMP.L rejection branch. Equality is affordable in the default.
    This helper has no RAM, category write or RNG effects.
    """
    quote = checked_equipment_quote(quote)
    remaining_gold = uint(remaining_gold, 32)
    available = u32(remaining_gold >> 2)
    if quote.price > available:
        return EquipmentBudgetDecision.REJECT
    return EquipmentBudgetDecision.PURCHASE


def commit_equipment_purchase(equipment: Table, remaining_gold: Long, quote: EquipmentQuote) -> Long:
    """Subtract with LONG wrap, then keep the original category-only BYTE write.

    The evaluated member's slot must not replace quote.category as destination:
    that would fix original behavior. Gold RAM is settled only at batch end.
    """
    equipment = equipment.state.checked_table(equipment)
    remaining_gold = uint(remaining_gold, 32)
    quote = checked_equipment_quote(quote)
    remaining_gold = u32(remaining_gold - quote.price)
    equipment.set_byte(quote.category, low8(quote.next_level))
    return remaining_gold


def settle_equipment_balance(views: EquipmentPurchaseViews, remaining_gold: Long) -> None:
    """Write once to the captured city slot, without rereading the city selector."""
    views = checked_equipment_views(views)
    remaining_gold = uint(remaining_gold, 32)
    views.gold.set_long(views.city_offset, remaining_gold)


def plan_troop_purchase_action(state: GameState) -> None:
    if state.ai_recruitment_capacity_gate().carry == 0:
        sort_equipment_roster(state)
        distribution = state.distribute_existing_troop_pool()
        if distribution.carry == 0:
            state.buy_and_distribute_troops(state.troop_purchase_context.retained_budget)
    state.set_command(11)


def clear_equipment_command(state: GameState) -> None:
    state.set_command(65535)
