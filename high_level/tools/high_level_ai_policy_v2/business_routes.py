"""Live AI city/army route decisions and original packed march commits.

These are executable data rules, not a CPU state interface. Lists, partial-width
arithmetic and original anomalous branches are intentionally not normalized.
"""
from .domain import (GameState, Word, Long, Table, Cursor, PackedGroupCursor,
    CityTroopSummary, NeighborRoute, CarryOutcome, checked_state,
    checked_city_troop_summary, checked_cursor, uint, u8, u16, u32,
    negative_byte, negative_word, descending_inclusive, divu_retained)
from .business_economy import sort_equipment_roster
from .business_actions import locate_packet_contact_city
from .contexts_march import (MarchPredicate, UnownedNeighborViews, MarchFunds,
    TwoOfficerTroopLoad, SupportOfficerViews, SupportRosterSize,
    SupportTroopLoad, MarchQuote)
from .contexts_transport import (RoutePredicate, NeighborQueryViews,
    PackedSupplyDecision, TransportRouteViews, StagingSearchViews)


def choose_neighbor_relation_phase(state: GameState) -> None:
    checked_state(state)
    outcome = hostile_neighbor_exists_carry(state)
    state.set_action_phase(4 if outcome.carry else 2)


def hostile_neighbor_exists_carry(state: GameState) -> CarryOutcome:
    """Capture the force once, scan live neighbors, then commit full-SR carry."""
    checked_state(state)
    views = read_neighbor_query_views(state)
    force = state.current_force()
    found = query_foreign_neighbor(views, force)
    return state.carry_result(1 if found else 0)


def read_neighbor_query_views(state: GameState) -> NeighborQueryViews:
    checked_state(state)
    neighbors = state.city_neighbors.cursor(u16(state.current_city() << 3))
    owners = state.city_owner
    return NeighborQueryViews(neighbors, owners)


def query_foreign_neighbor(views: NeighborQueryViews, force: Word) -> RoutePredicate:
    force = uint(force, 16)
    while True:
        neighbor = views.neighbors.next_byte()
        if negative_byte(neighbor):
            return False
        owner = views.owners.byte(neighbor)
        if negative_byte(owner):
            continue
        if not neighbor_owner_is_foreign(owner, u8(force)):
            continue
        return True


def neighbor_owner_is_foreign(owner: Word, force: Word) -> RoutePredicate:
    owner = uint(owner, 8)
    force = uint(force, 8)
    return owner != force


def choose_unowned_neighbor_phase(state: GameState) -> None:
    checked_state(state)
    outcome = unowned_neighbor_exists_carry(state)
    state.set_action_phase(3 if outcome.carry else 9)


def unowned_neighbor_exists_carry(state: GameState) -> CarryOutcome:
    checked_state(state)
    found = query_unowned_neighbor(read_neighbor_query_views(state))
    return state.carry_result(1 if found else 0)


def query_unowned_neighbor(views: NeighborQueryViews) -> RoutePredicate:
    while True:
        neighbor = views.neighbors.next_byte()
        if negative_byte(neighbor):
            return False
        if not negative_byte(views.owners.byte(neighbor)):
            continue
        return True


def choose_roster_troop_phase(state: GameState) -> None:
    checked_state(state)
    count = count_roster_large_troops(state)
    state.set_action_phase(7 if roster_troop_threshold_met(count, 3) else 9)


def roster_troop_threshold_met(count: Word, threshold: Word) -> RoutePredicate:
    count = uint(count, 16)
    threshold = uint(threshold, 16)
    return count >= threshold


def count_roster_large_troops(state: GameState) -> Word:
    checked_state(state)
    roster = state.route_roster.cursor()
    troops = state.officer_troops
    count = 0
    while True:
        officer = roster.next_word()
        if negative_word(officer):
            return count
        offset = u16(u8(officer) << 2)
        if not roster_officer_has_large_troops(troops.long(offset)):
            continue
        count = u16(count + 1)


def roster_officer_has_large_troops(quantity: Long) -> RoutePredicate:
    quantity = uint(quantity, 32)
    return quantity >= 5000


def choose_random_neighbor_phase(state: GameState) -> None:
    checked_state(state)
    state.set_action_phase(decide_random_neighbor_phase(state))


def decide_random_neighbor_phase(state: GameState) -> Word:
    """One real sample; the neighbor query occurs only when bit 2 is set."""
    sample = state.sample_random()
    if sample & 4:
        if unowned_neighbor_exists_carry(state).carry:
            return 5
    return 6


def choose_roster_troop_phase_five(state: GameState) -> None:
    checked_state(state)
    count = count_roster_large_troops(state)
    state.set_action_phase(7 if roster_troop_threshold_met(count, 5) else 9)


def evaluate_neighbor_march_phase(state: GameState) -> None:
    checked_state(state)
    baseline = sum_city_officer_troops(state, state.current_city())
    outcome = choose_weaker_enemy_neighbor(state, baseline)
    state.set_action_phase(8 if outcome.carry else 9)


def sum_city_officer_troops(state: GameState, city: Word) -> CityTroopSummary:
    checked_state(state)
    city = uint(city, 16)
    assignments = state.officer_city
    troops = state.officer_troops
    total = 0
    count = 0
    for officer in descending_inclusive(255):
        if assignments.byte(officer) != u8(city):
            continue
        quantity = troops.long(u16(officer << 2))
        total = u32(total + quantity)
        if city_troop_word_qualifies(u16(quantity)):
            count = u16(count + 1)
    return CityTroopSummary(total, count)


def city_troop_word_qualifies(quantity: Word) -> RoutePredicate:
    """Compatibility: qualification uses the low WORD, not the total LONG."""
    quantity = uint(quantity, 16)
    return quantity >= 5000


def choose_weaker_enemy_neighbor(state: GameState, baseline: CityTroopSummary) -> CarryOutcome:
    checked_state(state)
    checked_city_troop_summary(baseline)
    views = read_neighbor_query_views(state)
    return query_weaker_enemy_neighbor(state, views, baseline)


def query_weaker_enemy_neighbor(state: GameState, views: NeighborQueryViews, baseline: CityTroopSummary) -> CarryOutcome:
    """Force remains a live BYTE read for each eligible neighbor."""
    while True:
        neighbor = views.neighbors.next_byte()
        if negative_byte(neighbor):
            return state.carry_result(0)
        owner = views.owners.byte(neighbor)
        if negative_byte(owner):
            continue
        if not neighbor_owner_is_foreign(owner, state.current_force_byte()):
            continue
        summary = sum_city_officer_troops(state, neighbor)
        if not enemy_total_is_weaker(summary.total, baseline.total):
            continue
        if not enemy_roster_is_eligible(summary.qualifying_count, baseline.qualifying_count):
            continue
        return commit_enemy_neighbor_choice(state, neighbor, summary)


def enemy_total_is_weaker(candidate: Long, baseline: Long) -> RoutePredicate:
    candidate = uint(candidate, 32)
    baseline = uint(baseline, 32)
    return candidate < baseline


def enemy_roster_is_eligible(candidate: Word, baseline: Word) -> RoutePredicate:
    candidate = uint(candidate, 16)
    baseline = uint(baseline, 16)
    return candidate <= baseline


def commit_enemy_neighbor_choice(state: GameState, neighbor: Word, summary: CityTroopSummary) -> CarryOutcome:
    state.set_target_city(neighbor)
    state.set_phase_argument(summary.qualifying_count)
    return state.carry_result(1)


def commit_unowned_neighbor_march(state: GameState) -> None:
    """Plan an unowned destination, qualify the live pair, then commit departure.

    The head check runs even when no march was funded. Route sentinels are not
    clamped, and both candidate words are reread after the real packet builder.
    """
    checked_state(state)
    route = shortest_unowned_neighbor(state)
    state.set_path_length(route.length)
    state.set_target_city(route.city)
    sort_equipment_roster(state)
    troops = state.officer_troops
    if two_officer_roster_is_ready(state, troops):
        commit_two_officer_departure(state)
    assignments = state.officer_city
    if departing_head_is_marked(state, assignments):
        restore_departing_city_head(state)
    state.set_action_phase(9)


def two_officer_roster_is_ready(state: GameState, troops: Table) -> MarchPredicate:
    """Short-circuit the second WORD read when the first officer fails policy."""
    troops = state.checked_table(troops)
    first = u16(state.first_candidate_officer() << 2)
    if not march_officer_has_troops(troops.long(first)):
        return False
    second = u16(state.second_candidate_officer() << 2)
    return march_officer_has_troops(troops.long(second))


def march_officer_has_troops(quantity: Long) -> MarchPredicate:
    quantity = uint(quantity, 32)
    return quantity >= 5000


def read_march_funds(state: GameState) -> MarchFunds:
    """Capture the actual food view and city slot, not a detached balance map."""
    checked_state(state)
    food = state.city_food
    city_offset = u16(state.current_city() << 2)
    available = food.long(city_offset)
    return MarchFunds(food, city_offset, available)


def two_officer_supply_is_affordable(available: Long, budget: Long) -> MarchPredicate:
    available = uint(available, 32)
    budget = uint(budget, 32)
    return available >= budget


def commit_two_officer_departure(state: GameState) -> None:
    """Keep low-WORD quotation storage and the later live food RMW distinct."""
    state.set_march_supply_budget(u16(price_two_officer_march(state)))
    funds = read_march_funds(state)
    if two_officer_supply_is_affordable(funds.available, state.march_supply_budget()):
        debit = state.march_supply_budget()
        funds.food.set_long(funds.city_offset, u32(funds.food.long(funds.city_offset) - debit))
        append_two_officer_march(state)
        state.build_ai_movement_packet()
        mark_two_officers_departing(state)


def mark_two_officers_departing(state: GameState) -> None:
    assignments = state.officer_city
    officer = u8(state.first_candidate_officer())
    assignments.set_byte(officer, assignments.byte(officer) | 64)
    officer = u8(state.second_candidate_officer())
    assignments.set_byte(officer, assignments.byte(officer) | 64)


def departing_head_is_marked(state: GameState, assignments: Table) -> MarchPredicate:
    assignments = state.checked_table(assignments)
    heads = state.city_heads
    head = heads.word(u16(state.current_city() << 1))
    return (assignments.byte(head) & 64) != 0


def shortest_unowned_neighbor(state: GameState) -> NeighborRoute:
    return query_shortest_unowned_route(state, read_unowned_neighbor_views(state))


def read_unowned_neighbor_views(state: GameState) -> UnownedNeighborViews:
    checked_state(state)
    city_offset = u16(state.current_city() << 3)
    neighbors = state.city_neighbors.cursor(city_offset)
    coordinates = state.city_coordinates
    coordinate_offset = city_offset >> 1
    state.set_path_start_first(coordinates.word(coordinate_offset, displacement=2) >> 4)
    state.set_path_start_second(coordinates.word(coordinate_offset) >> 4)
    owners = state.city_owner
    return UnownedNeighborViews(neighbors, coordinates, owners)


def query_shortest_unowned_route(state: GameState, views: UnownedNeighborViews) -> NeighborRoute:
    """Evaluate each live unowned neighbor through the actual path service.

    Equal lengths keep the earlier candidate. The path length is read twice on
    improvement; do not snapshot it across the original comparison/write point.
    """
    checked_cursor(views.neighbors, state)
    best_length = 65535
    best_city = 65535
    while True:
        neighbor = views.neighbors.next_byte()
        if negative_byte(neighbor):
            return NeighborRoute(best_length, best_city)
        if not negative_byte(views.owners.byte(neighbor)):
            continue
        offset = u16(neighbor << 2)
        state.set_path_goal_first(views.coordinates.word(offset, displacement=2) >> 4)
        state.set_path_goal_second(views.coordinates.word(offset) >> 4)
        state.build_path_from_cells()
        if not march_route_improves(best_length, state.path_length()):
            continue
        best_length = state.path_length()
        best_city = neighbor


def march_route_improves(best_length: Word, candidate_length: Word) -> MarchPredicate:
    best_length = uint(best_length, 16)
    candidate_length = uint(candidate_length, 16)
    return best_length > candidate_length


def price_two_officer_march(state: GameState) -> Long:
    """Separate live load/speed queries from retained-DIVU cost arithmetic."""
    load = read_two_officer_troop_load(state)
    base_price = calculate_march_base_charge(load.total)
    speed = read_two_officer_average_speed(state, load)
    state.set_phase_argument(speed)
    distance = state.path_length()
    duration = calculate_two_officer_duration(distance, speed)
    quote = MarchQuote(speed, duration, u32(u16(base_price) * duration))
    return quote.supply


def read_two_officer_troop_load(state: GameState) -> TwoOfficerTroopLoad:
    checked_state(state)
    troops = state.officer_troops
    first = u16(state.first_candidate_officer() << 2)
    total = troops.long(first)
    second = u16(state.second_candidate_officer() << 2)
    total = u32(total + troops.long(second))
    total = u32(total + 200)
    return TwoOfficerTroopLoad(first, second, total)


def calculate_march_base_charge(total: Long) -> Long:
    total = uint(total, 32)
    encoded_price = divu_retained(total, 10)
    base_price = u32(u16(encoded_price) * 3)
    return base_price


def read_two_officer_average_speed(state: GameState, load: TwoOfficerTroopLoad) -> Word:
    speeds = state.officer_march_speed
    speed = u8(speeds.byte(load.first_offset >> 2) + speeds.byte(load.second_offset >> 2)) >> 1
    return speed


def calculate_two_officer_duration(distance: Word, speed: Word) -> Word:
    distance = uint(distance, 16)
    speed = uint(speed, 16)
    rounded_distance = u16(u16(distance + speed) - 1)
    duration = divu_retained(rounded_distance, speed)
    duration = u16(u16(duration) + 3)
    return duration


def append_two_officer_march(state: GameState) -> None:
    checked_state(state)
    packet = find_march_queue_tail(state)
    packet.set_byte(0, 34)
    write_march_origin(state, packet)
    packet.set_byte(3, state.phase_argument_byte())
    packet.set_byte(4, state.current_force_byte())
    packet.set_byte(5, 0)
    packet.set_byte(6, 0)
    packet.set_byte(7, 0)
    packet.set_byte(8, 0)
    write_march_budget_bytes(packet, 12, state.march_supply_budget())
    packet.set_byte(13, state.first_candidate_officer_byte())
    state.set_packed_head(state.first_candidate_officer())
    packet.set_byte(14, state.second_candidate_officer_byte())
    packet.set_byte(15, 0)


def find_march_queue_tail(state: GameState) -> PackedGroupCursor:
    """Scan physical packed records using only their low-nibble member count."""
    packet = state.packed_groups.cursor()
    while True:
        count = packet.byte() & 15
        if count == 0:
            break
        packet = packet.advance(13 + count)
    return packet


def write_march_origin(state: GameState, packet: PackedGroupCursor) -> None:
    checked_cursor(packet, state)
    coordinates = state.city_coordinates
    offset = u16(state.current_city() << 2)
    first = coordinates.word(offset, displacement=2)
    state.set_packed_first(first)
    packet.set_byte(1, u8(first >> 4))
    second = coordinates.word(offset)
    state.set_packed_second(second)
    packet.set_byte(2, u8(second >> 4))


def write_march_budget_bytes(packet: PackedGroupCursor, last_slot: Word, budget: Long) -> None:
    """Write low-to-high BYTEs; retain the final WORD shift's visible low BYTE."""
    checked_cursor(packet)
    last_slot = uint(last_slot, 16)
    budget = uint(budget, 32)
    packet.set_byte(last_slot, u8(budget))
    budget >>= 8
    packet.set_byte(u16(last_slot - 1), u8(budget))
    budget >>= 8
    packet.set_byte(u16(last_slot - 2), u8(budget))
    budget = u16(budget) >> 8
    packet.set_byte(u16(last_slot - 3), u8(budget))


def restore_departing_city_head(state: GameState) -> None:
    checked_state(state)
    destination = state.support_roster.cursor()
    source = state.remaining_roster.cursor()
    copy_remaining_city_roster(source, destination)
    state.choose_city_head(state.current_city())


def copy_remaining_city_roster(source: Cursor, destination: Cursor) -> None:
    checked_cursor(source)
    checked_cursor(destination, source.state)
    while True:
        officer = source.next_word()
        destination.append_word(officer)
        if negative_word(officer):
            break


def commit_support_march(state: GameState) -> None:
    """Gate live roster/gold, select members, price, then commit the funded order."""
    checked_state(state)
    count = state.roster_count()
    if support_city_has_roster(count):
        balances = state.city_gold
        city_offset = u16(state.current_city() << 2)
        gold = balances.long(city_offset)
        if support_city_has_gold(gold):
            state.set_selected_gold_budget(gold >> 1)
            if not collect_support_officers(state).carry:
                choose_support_roster(state)
                if not negative_word(state.scratch_roster.word()):
                    price_support_march(state)
                    funds = read_march_funds(state)
                    if support_supply_is_affordable(funds.available, state.march_supply_budget()):
                        settle_support_march_funds(state, funds)
                        append_support_march(state)
                        state.build_ai_movement_packet()
                        assignments = mark_selected_support_departing(state)
                        if departing_head_is_marked(state, assignments):
                            rebuild_departing_city_head(state)
    state.set_action_phase(65535)


def support_city_has_roster(count: Word) -> MarchPredicate:
    count = uint(count, 16)
    return count >= 3


def support_city_has_gold(gold: Long) -> MarchPredicate:
    gold = uint(gold, 32)
    return gold >= 2000


def support_supply_is_affordable(available: Long, budget: Long) -> MarchPredicate:
    """Default support admission is strict; equal supply does not depart."""
    available = uint(available, 32)
    budget = uint(budget, 32)
    return available > budget


def settle_support_march_funds(state: GameState, funds: MarchFunds) -> None:
    """Settle captured food first, then reread live gold at the same city slot."""
    available = u32(funds.available - state.march_supply_budget())
    funds.food.set_long(funds.city_offset, available)
    balances = state.city_gold
    gold = balances.long(funds.city_offset)
    gold = u32(gold - state.selected_gold_budget())
    balances.set_long(funds.city_offset, gold)


def mark_selected_support_departing(state: GameState) -> Table:
    """Selected WORD identities stay full-width, unlike the two-person mask."""
    selected = state.scratch_roster.cursor()
    assignments = state.officer_city
    while True:
        officer = selected.next_word()
        if negative_word(officer):
            break
        assignments.set_byte(officer, assignments.byte(officer) | 64)
    return assignments


def collect_support_officers(state: GameState) -> CarryOutcome:
    """Collect live eligible members and preserve the original partial sort."""
    views = read_support_officer_views(state)
    count_bytes = collect_eligible_support_officers(views)
    views.roster.put_word(65535)
    if negative_word(state.support_roster.word()):
        return state.carry_result(1)
    if negative_word(state.support_roster.word(displacement=2)):
        return state.carry_result(1)
    order_support_candidates(state, count_bytes)
    return state.carry_result(0)


def read_support_officer_views(state: GameState) -> SupportOfficerViews:
    checked_state(state)
    source = state.route_roster.cursor()
    roster = state.support_roster.cursor()
    troops = state.officer_troops
    strengths = state.officer_strength
    scratch = state.scratch_roster.cursor()
    limits = state.officer_loyalty_limit
    loyalty = state.officer_loyalty
    return SupportOfficerViews(source, roster, troops, strengths, scratch, limits, loyalty)


def collect_eligible_support_officers(views: SupportOfficerViews) -> Word:
    count_bytes = 0
    while True:
        officer = views.source.next_word()
        if negative_word(officer):
            break
        officer = u8(officer)
        offset = u16(officer << 2)
        if not march_officer_has_troops(views.troops.long(offset)):
            continue
        offset >>= 1
        limit = views.limits.long(offset)
        if not support_loyalty_allows_departure(limit, views.loyalty.long(offset)):
            continue
        views.roster.append_word(officer)
        views.scratch.append_word(views.strengths.word(offset))
        count_bytes = u16(count_bytes + 2)
    return count_bytes


def support_loyalty_allows_departure(limit: Long, current: Long) -> MarchPredicate:
    limit = uint(limit, 32)
    current = uint(current, 32)
    return limit >= current


def order_support_candidates(state: GameState, count_bytes: Word) -> None:
    """Keep the original inverted outer-exit condition and repeated live reads.

    This is not replaced by Python sorted(): wrapped counts and the single-pass
    behavior are compatibility. Scratch and roster may overlap other live data.
    """
    count_bytes = uint(count_bytes, 16)
    roster = state.support_roster
    scratch = state.scratch_roster
    while True:
        offset = 2
        while True:
            previous = scratch.word(offset, displacement=-2)
            if support_strength_requires_swap(previous, scratch.word(offset)):
                scratch.set_word(u16(offset - 2), scratch.word(offset))
                scratch.set_word(offset, previous)
                officer = roster.word(offset, displacement=-2)
                roster.set_word(u16(offset - 2), roster.word(offset))
                roster.set_word(offset, officer)
            offset = u16(offset + 2)
            if offset >= count_bytes:
                break
        count_bytes = u16(count_bytes - 2)
        if count_bytes >= 2:
            break


def support_strength_requires_swap(previous: Word, current: Word) -> MarchPredicate:
    previous = uint(previous, 16)
    current = uint(current, 16)
    return previous < current


def choose_support_roster(state: GameState) -> None:
    checked_state(state)
    source = state.support_roster.cursor()
    output = state.scratch_roster.cursor()
    decision = resolve_support_roster_size(state)
    if not decision.accepted:
        state.scratch_roster.set_word(0, 65535)
        return
    chosen_count = decision.count
    copy_selected_support_officers(source, output, chosen_count)
    flags = state.officer_flags
    selected = state.scratch_roster.cursor()
    if selected_support_has_required_flag(selected, flags):
        if chosen_count <= state.phase_argument():
            state.scratch_roster.set_word(0, 65535)
        return
    chosen_count = append_required_support_officer(state, selected, flags, chosen_count)
    if chosen_count <= state.phase_argument():
        state.scratch_roster.set_word(0, 65535)


def resolve_support_roster_size(state: GameState) -> SupportRosterSize:
    """Retain the original repeated count/phase reads and WORD size wrap."""
    size = state.phase_argument()
    if size < 2:
        size = 2
    size = u16(size + 1)
    if size >= state.roster_count():
        size = u16(state.roster_count() - 1)
    if size < 2 or size < state.phase_argument():
        return SupportRosterSize(size, False)
    if size == 0:
        return SupportRosterSize(size, False)
    return SupportRosterSize(size, True)


def copy_selected_support_officers(source: Cursor, output: Cursor, size: Word) -> None:
    checked_cursor(source)
    checked_cursor(output, source.state)
    size = uint(size, 16)
    counter = u16(size - 1)
    for unused in descending_inclusive(counter):
        output.append_word(source.next_word())
    output.put_word(65535)


def selected_support_has_required_flag(selected: Cursor, flags: Table) -> MarchPredicate:
    checked_cursor(selected)
    flags = selected.state.checked_table(flags)
    while True:
        officer = selected.next_word()
        if negative_word(officer):
            return False
        if flags.byte(officer) & 16:
            return True


def append_required_support_officer(state: GameState, selected: Cursor, flags: Table, chosen_count: Word) -> Word:
    """BUG024: selected already advanced over FFFF; append after, not over it."""
    checked_cursor(selected, state)
    flags = state.checked_table(flags)
    chosen_count = uint(chosen_count, 16)
    limit = u16(state.roster_count() - 1)
    if chosen_count < limit:
        source = state.route_roster.cursor()
        while True:
            officer = source.next_word()
            if negative_word(officer):
                break
            if not flags.byte(officer) & 16:
                continue
            selected.put_word(officer)
            selected.set_word(0, 65535, displacement=2)
            chosen_count = u16(chosen_count + 1)
            break
    return chosen_count


def price_support_march(state: GameState) -> None:
    """Use the real route first, then query load and commit average/count/price."""
    initialize_support_march_path(state)
    load = read_support_troop_load(state)
    encoded_average = divu_retained(load.speed_sum, load.count)
    average = u16(encoded_average)
    state.set_packed_first(average)
    state.set_packed_second(load.count)
    distance = state.path_length()
    duration = calculate_support_duration(distance, average)
    price = calculate_march_base_charge(load.total)
    quote = MarchQuote(average, duration, u32(u16(price) * duration))
    state.set_march_supply_budget(quote.supply)


def initialize_support_march_path(state: GameState) -> None:
    checked_state(state)
    coordinates = state.city_coordinates
    offset = u16(state.current_city() << 2)
    state.set_path_start_first(coordinates.word(offset, displacement=2))
    state.set_path_start_second(coordinates.word(offset))
    offset = u16(state.target_city() << 2)
    state.set_path_goal_first(coordinates.word(offset, displacement=2))
    state.set_path_goal_second(coordinates.word(offset))
    state.build_path()


def read_support_troop_load(state: GameState) -> SupportTroopLoad:
    roster = state.scratch_roster.cursor()
    speeds = state.officer_march_speed
    troops = state.officer_troops
    speed_sum = 0
    total = 0
    count = 0
    while True:
        officer = roster.next_word()
        if negative_word(officer):
            break
        count = u16(count + 1)
        speed_sum = u8(speed_sum + speeds.byte(officer))
        total = u32(total + troops.long(u16(officer << 2)))
        total = u32(total + 100)
    return SupportTroopLoad(speed_sum, total, count)


def calculate_support_duration(distance: Word, average: Word) -> Word:
    """Unlike the pair price, sign-extend the rounded WORD before DIVU."""
    distance = uint(distance, 16)
    average = uint(average, 16)
    rounded = u16(u16(distance + average) - 1)
    signed_distance = rounded - 65536 if negative_word(rounded) else rounded
    encoded_duration = divu_retained(u32(signed_distance), average)
    duration = u16(u16(encoded_duration) + 2)
    return duration


def append_support_march(state: GameState) -> None:
    checked_state(state)
    packet = find_march_queue_tail(state)
    size = state.packed_second()
    packet.set_byte(0, u8(size | 32))
    packet.set_byte(3, state.packed_first_byte())
    packet.set_byte(4, state.current_force_byte())
    state.set_phase_argument(state.packed_first())
    write_march_origin(state, packet)
    write_march_budget_bytes(packet, 8, state.selected_gold_budget())
    write_march_budget_bytes(packet, 12, state.march_supply_budget())
    output = packet.advance(13)
    source = state.scratch_roster.cursor()
    write_support_packet_members(source, output)
    state.set_packed_head(state.scratch_roster.word())


def write_support_packet_members(source: Cursor, output: Cursor) -> None:
    checked_cursor(source)
    checked_cursor(output, source.state)
    while True:
        officer = source.next_word()
        if negative_word(officer):
            break
        output.append_byte(u8(officer))
    output.set_byte(0, 0)


def rebuild_departing_city_head(state: GameState) -> None:
    checked_state(state)
    city = state.current_city()
    state.set_roster_head(65535)
    state.build_roster(city)
    state.choose_city_head(city)


def finish_support_phase(state: GameState) -> None:
    checked_state(state)
    state.set_action_phase(65535)


def evaluate_packed_group_supply_phase(state: GameState) -> None:
    decision = read_packed_supply_decision(state)
    state.set_action_phase(2 if packed_supply_is_insufficient(decision.cash, decision.price) else 6)


def read_packed_supply_decision(state: GameState) -> PackedSupplyDecision:
    """Price first, then read four live cash BYTEs from the retained group."""
    checked_state(state)
    group = state.packed_groups.cursor(state.packed_group_offset())
    price = price_packed_group(state, group)
    cash = read_packed_long_bytes(group, 9)
    return PackedSupplyDecision(group, price, cash)


def read_packed_long_bytes(record: Cursor, first_slot: Word) -> Long:
    """Preserve the first WORD shift followed by two LONG shifts and BYTE loads."""
    checked_cursor(record)
    first_slot = uint(first_slot, 16)
    cash = record.byte(first_slot)
    cash = u16(cash << 8)
    cash = (cash & 65280) | record.byte(u16(first_slot + 1))
    cash = u32(cash << 8)
    cash = (cash & 4294967040) | record.byte(u16(first_slot + 2))
    cash = u32(cash << 8)
    cash = (cash & 4294967040) | record.byte(u16(first_slot + 3))
    return cash


def packed_supply_is_insufficient(cash: Long, price: Long) -> RoutePredicate:
    cash = uint(cash, 32)
    price = uint(price, 32)
    return cash < price


def price_packed_group(state: GameState, group: PackedGroupCursor) -> Long:
    return calculate_packed_supply_cost(read_packed_troop_load(state, group))


def read_packed_troop_load(state: GameState, group: PackedGroupCursor) -> Long:
    """Low-nibble zero underflows to FFFF: retain the inclusive 65536 scan."""
    checked_state(state)
    checked_cursor(group, state)
    count = u16((group.byte() & 15) - 1)
    troops = state.officer_troops
    total = 0
    for member in descending_inclusive(count):
        officer = group.byte(member, displacement=13)
        total = u32(total + troops.long(u16(officer << 2)))
        total = u32(total + 100)
    return total


def calculate_packed_supply_cost(total: Long) -> Long:
    """This quote truncates the triple product to WORD, unlike march pricing."""
    total = uint(total, 32)
    encoded = divu_retained(total, 10)
    price = u16(u16(encoded) << 1)
    price = u16(price + u16(encoded))
    return price


def choose_group_destination_phase(state: GameState) -> None:
    checked_state(state)
    state.choose_ai_destination()
    state.set_action_phase(3 if negative_word(state.target_city()) else 4)


def evaluate_transport_supply_phase(state: GameState) -> None:
    supply = read_transport_supply(state)
    if transport_supply_allows_route(supply):
        if not reachable_transport_coordinate_carry(state).carry:
            state.set_action_phase(5)
            return
    state.set_action_phase(4)


def read_transport_supply(state: GameState) -> Long:
    checked_state(state)
    record = state.officer_packet_data.at(state.packed_group_offset())
    return read_packed_long_bytes(record.cursor(), 5)


def transport_supply_allows_route(supply: Long) -> RoutePredicate:
    supply = uint(supply, 32)
    return supply >= 500


def reachable_transport_coordinate_carry(state: GameState) -> CarryOutcome:
    return query_transport_coordinate(state, read_transport_route_views(state))


def read_transport_route_views(state: GameState) -> TransportRouteViews:
    checked_state(state)
    origin_first = state.transport_first()
    state.set_path_start_first(origin_first)
    origin_second = state.transport_second()
    state.set_path_start_second(origin_second)
    budget = state.transport_route_budget()
    candidates = state.coordinate_candidates.cursor()
    return TransportRouteViews(origin_first, origin_second, budget, candidates)


def query_transport_coordinate(state: GameState, views: TransportRouteViews) -> CarryOutcome:
    """Retain the original coarse BYTE budget and reversed full-WORD BLS gate."""
    candidates = views.candidates
    while True:
        first = candidates.byte()
        if negative_byte(first):
            return state.carry_result(1)
        state.set_path_goal_first(first)
        delta_first = transport_first_delta(first, u8(views.first))
        if transport_component_within_budget(delta_first, u8(views.budget)):
            second = candidates.byte(1)
            state.set_path_goal_second(second)
            delta_second = transport_second_delta(second, u8(views.second))
            distance = u8(delta_first + u8(delta_second))
            if transport_component_within_budget(distance, u8(views.budget)):
                state.build_path_from_cells()
                if transport_route_accepts_length(views.budget, state.path_length()):
                    return state.carry_result(0)
        candidates = candidates.advance(2)


def transport_first_delta(destination: Word, origin: Word) -> Word:
    destination = uint(destination, 8)
    origin = uint(origin, 8)
    delta = u8(destination - origin)
    if destination < origin:
        delta = u8(-delta)
    return delta


def transport_second_delta(destination: Word, origin: Word) -> Word:
    """Second-axis underflow is NEG.W, not the first-axis NEG.B."""
    destination = uint(destination, 8)
    origin = uint(origin, 8)
    delta = u8(destination - origin)
    if destination < origin:
        delta = u16(-delta)
    return delta


def transport_component_within_budget(distance: Word, budget: Word) -> RoutePredicate:
    distance = uint(distance, 8)
    budget = uint(budget, 8)
    return distance <= budget


def transport_route_accepts_length(budget: Word, length: Word) -> RoutePredicate:
    budget = uint(budget, 16)
    length = uint(length, 16)
    return budget <= length


def commit_staging_city_phase(state: GameState) -> None:
    checked_state(state)
    group = choose_nearest_staging_city(state)
    if not negative_word(state.target_city()):
        commit_staging_departure(state, group)
    state.set_action_phase(22)


def commit_staging_departure(state: GameState, group: PackedGroupCursor) -> None:
    """Reuse search's live group; never reacquire a possibly rebound offset."""
    checked_cursor(group, state)
    state.set_target_city(u16(state.target_city() + 1))
    state.set_phase_argument(group.byte(3))
    state.set_packed_head(group.byte(13))
    state.build_ai_movement_packet()


def choose_nearest_staging_city(state: GameState) -> PackedGroupCursor:
    views = read_staging_search_views(state)
    query_nearest_staging_city(state, views)
    return views.group


def read_staging_search_views(state: GameState) -> StagingSearchViews:
    checked_state(state)
    group = state.packed_groups.cursor(state.packed_group_offset())
    first = group.byte(1) << 4
    state.set_path_start_first(first)
    state.set_packed_first(first)
    first >>= 4
    second = group.byte(2) << 4
    state.set_path_start_second(second)
    state.set_packed_second(second)
    second >>= 4
    state.set_target_city(65535)
    coordinates = state.city_coordinates_zero_based
    owners = state.city_owner_zero_based
    return StagingSearchViews(group, first, second, coordinates, owners)


def query_nearest_staging_city(state: GameState, views: StagingSearchViews) -> None:
    best_distance = 65535
    for city in descending_inclusive(39):
        if views.owners.byte(city) != state.current_force_byte():
            continue
        if state.city_roster_full_carry(city).carry:
            continue
        offset = u16(city << 2)
        destination_first = views.coordinates.word(offset, displacement=2) >> 4
        delta_first = staging_axis_distance(destination_first, views.first)
        destination_second = views.coordinates.word(offset) >> 4
        delta_second = staging_axis_distance(destination_second, views.second)
        distance = u16(delta_second + delta_first)
        if not staging_distance_improves(distance, best_distance):
            continue
        best_distance = distance
        state.set_target_city(city)


def staging_axis_distance(destination: Word, origin: Word) -> Word:
    destination = uint(destination, 16)
    origin = uint(origin, 16)
    delta = u16(destination - origin)
    if destination < origin:
        delta = u16(-delta)
    return delta


def staging_distance_improves(candidate: Word, best: Word) -> RoutePredicate:
    candidate = uint(candidate, 16)
    best = uint(best, 16)
    return candidate < best


def choose_destination_progress_phase(state: GameState) -> None:
    checked_state(state)
    state.set_action_phase(21 if destination_has_been_reached(state) else 20)


def destination_has_been_reached(state: GameState) -> RoutePredicate:
    """Second-axis goal/start remain unread when the first axis differs."""
    first = state.path_goal_first()
    if destination_axis_matches(first, state.path_start_first()):
        second = state.path_goal_second()
        if destination_axis_matches(second, state.path_start_second()):
            return True
    return False


def destination_axis_matches(goal: Word, start: Word) -> RoutePredicate:
    goal = uint(goal, 16)
    start = uint(start, 16)
    return goal == start


def choose_terrain_exit_phase(state: GameState) -> None:
    checked_state(state)
    if query_adjacent_terrain_exit(state):
        located = locate_packet_contact_city(state)
        state.set_action_phase(13 if located.carry else 24)
    else:
        state.set_action_phase(13)


def query_adjacent_terrain_exit(state: GameState) -> RoutePredicate:
    """Ordered north/west/east/south reads; row is deliberately read twice."""
    row = state.transport_first()
    offset = u16(u16(u16(row << 3) + state.transport_first()) << 3)
    offset = u16(offset + state.transport_second())
    terrain = state.terrain_types
    if terrain_kind_is_exit(terrain.byte(offset, displacement=-72)):
        return True
    if terrain_kind_is_exit(terrain.byte(offset, displacement=-1)):
        return True
    if terrain_kind_is_exit(terrain.byte(offset, displacement=1)):
        return True
    if terrain_kind_is_exit(terrain.byte(offset, displacement=72)):
        return True
    return False


def terrain_kind_is_exit(kind: Word) -> RoutePredicate:
    kind = uint(kind, 8)
    return kind == 1
