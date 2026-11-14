"""Finite, fully consumed route Python flows -> ordinary 68000 target choices.

The expected flows below are business semantics, not original assembly strings.
March queries, policies, costs and commits are consumed as complete helper ASTs.
Only the declared unsigned comparisons and bounded thresholds are editable;
other valid Python edits are rejected rather than silently omitted.
"""
import ast
from copy import deepcopy
from .compiler_common import CompileError, semantic_functions, lower_declared
from .target import ROUTES_BINDINGS, BY_NAME, TABLE_BINDINGS, SCALAR_BINDINGS

DECLARATIONS = {
  "choose_neighbor_relation_phase": {
    "flow": "checked_state(state)\noutcome = hostile_neighbor_exists_carry(state)\nstate.set_action_phase(4 if outcome.carry else 2)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "hostile_neighbor_exists_carry": {
    "flow": "checked_state(state)\nviews = read_neighbor_query_views(state)\nforce = state.current_force()\nfound = query_foreign_neighbor(views, force)\nreturn state.carry_result(1 if found else 0)",
    "returns": "CarryOutcome",
    "signature": "state: GameState"
  },
  "read_neighbor_query_views": {
    "flow": "checked_state(state)\nneighbors = state.city_neighbors.cursor(u16(state.current_city() << 3))\nowners = state.city_owner\nreturn NeighborQueryViews(neighbors, owners)",
    "returns": "NeighborQueryViews",
    "signature": "state: GameState"
  },
  "query_foreign_neighbor": {
    "flow": "force = uint(force, 16)\nwhile True:\n    neighbor = views.neighbors.next_byte()\n    if negative_byte(neighbor):\n        return False\n    owner = views.owners.byte(neighbor)\n    if negative_byte(owner):\n        continue\n    if not neighbor_owner_is_foreign(owner, u8(force)):\n        continue\n    return True",
    "returns": "RoutePredicate",
    "signature": "views: NeighborQueryViews, force: Word"
  },
  "neighbor_owner_is_foreign": {
    "flow": "owner = uint(owner, 8)\nforce = uint(force, 8)\nreturn owner != force",
    "returns": "RoutePredicate",
    "signature": "owner: Word, force: Word"
  },
  "choose_unowned_neighbor_phase": {
    "flow": "checked_state(state)\noutcome = unowned_neighbor_exists_carry(state)\nstate.set_action_phase(3 if outcome.carry else 9)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "unowned_neighbor_exists_carry": {
    "flow": "checked_state(state)\nfound = query_unowned_neighbor(read_neighbor_query_views(state))\nreturn state.carry_result(1 if found else 0)",
    "returns": "CarryOutcome",
    "signature": "state: GameState"
  },
  "query_unowned_neighbor": {
    "flow": "while True:\n    neighbor = views.neighbors.next_byte()\n    if negative_byte(neighbor):\n        return False\n    if not negative_byte(views.owners.byte(neighbor)):\n        continue\n    return True",
    "returns": "RoutePredicate",
    "signature": "views: NeighborQueryViews"
  },
  "choose_roster_troop_phase": {
    "flow": "checked_state(state)\ncount = count_roster_large_troops(state)\nstate.set_action_phase(7 if roster_troop_threshold_met(count, 3) else 9)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "roster_troop_threshold_met": {
    "flow": "count = uint(count, 16)\nthreshold = uint(threshold, 16)\nreturn count >= threshold",
    "returns": "RoutePredicate",
    "signature": "count: Word, threshold: Word"
  },
  "count_roster_large_troops": {
    "flow": "checked_state(state)\nroster = state.route_roster.cursor()\ntroops = state.officer_troops\ncount = 0\nwhile True:\n    officer = roster.next_word()\n    if negative_word(officer):\n        return count\n    offset = u16(u8(officer) << 2)\n    if not roster_officer_has_large_troops(troops.long(offset)):\n        continue\n    count = u16(count + 1)",
    "returns": "Word",
    "signature": "state: GameState"
  },
  "roster_officer_has_large_troops": {
    "flow": "quantity = uint(quantity, 32)\nreturn quantity >= 5000",
    "returns": "RoutePredicate",
    "signature": "quantity: Long"
  },
  "choose_random_neighbor_phase": {
    "flow": "checked_state(state)\nstate.set_action_phase(decide_random_neighbor_phase(state))",
    "returns": "None",
    "signature": "state: GameState"
  },
  "decide_random_neighbor_phase": {
    "flow": "sample = state.sample_random()\nif sample & 4:\n    if unowned_neighbor_exists_carry(state).carry:\n        return 5\nreturn 6",
    "returns": "Word",
    "signature": "state: GameState"
  },
  "choose_roster_troop_phase_five": {
    "flow": "checked_state(state)\ncount = count_roster_large_troops(state)\nstate.set_action_phase(7 if roster_troop_threshold_met(count, 5) else 9)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "evaluate_neighbor_march_phase": {
    "flow": "checked_state(state)\nbaseline = sum_city_officer_troops(state, state.current_city())\noutcome = choose_weaker_enemy_neighbor(state, baseline)\nstate.set_action_phase(8 if outcome.carry else 9)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "sum_city_officer_troops": {
    "flow": "checked_state(state)\ncity = uint(city, 16)\nassignments = state.officer_city\ntroops = state.officer_troops\ntotal = 0\ncount = 0\nfor officer in descending_inclusive(255):\n    if assignments.byte(officer) != u8(city):\n        continue\n    quantity = troops.long(u16(officer << 2))\n    total = u32(total + quantity)\n    if city_troop_word_qualifies(u16(quantity)):\n        count = u16(count + 1)\nreturn CityTroopSummary(total, count)",
    "returns": "CityTroopSummary",
    "signature": "state: GameState, city: Word"
  },
  "city_troop_word_qualifies": {
    "flow": "quantity = uint(quantity, 16)\nreturn quantity >= 5000",
    "returns": "RoutePredicate",
    "signature": "quantity: Word"
  },
  "choose_weaker_enemy_neighbor": {
    "flow": "checked_state(state)\nchecked_city_troop_summary(baseline)\nviews = read_neighbor_query_views(state)\nreturn query_weaker_enemy_neighbor(state, views, baseline)",
    "returns": "CarryOutcome",
    "signature": "state: GameState, baseline: CityTroopSummary"
  },
  "query_weaker_enemy_neighbor": {
    "flow": "while True:\n    neighbor = views.neighbors.next_byte()\n    if negative_byte(neighbor):\n        return state.carry_result(0)\n    owner = views.owners.byte(neighbor)\n    if negative_byte(owner):\n        continue\n    if not neighbor_owner_is_foreign(owner, state.current_force_byte()):\n        continue\n    summary = sum_city_officer_troops(state, neighbor)\n    if not enemy_total_is_weaker(summary.total, baseline.total):\n        continue\n    if not enemy_roster_is_eligible(summary.qualifying_count, baseline.qualifying_count):\n        continue\n    return commit_enemy_neighbor_choice(state, neighbor, summary)",
    "returns": "CarryOutcome",
    "signature": "state: GameState, views: NeighborQueryViews, baseline: CityTroopSummary"
  },
  "enemy_total_is_weaker": {
    "flow": "candidate = uint(candidate, 32)\nbaseline = uint(baseline, 32)\nreturn candidate < baseline",
    "returns": "RoutePredicate",
    "signature": "candidate: Long, baseline: Long"
  },
  "enemy_roster_is_eligible": {
    "flow": "candidate = uint(candidate, 16)\nbaseline = uint(baseline, 16)\nreturn candidate <= baseline",
    "returns": "RoutePredicate",
    "signature": "candidate: Word, baseline: Word"
  },
  "commit_enemy_neighbor_choice": {
    "flow": "state.set_target_city(neighbor)\nstate.set_phase_argument(summary.qualifying_count)\nreturn state.carry_result(1)",
    "returns": "CarryOutcome",
    "signature": "state: GameState, neighbor: Word, summary: CityTroopSummary"
  },
  "commit_unowned_neighbor_march": {
    "flow": "checked_state(state)\nroute = shortest_unowned_neighbor(state)\nstate.set_path_length(route.length)\nstate.set_target_city(route.city)\nsort_equipment_roster(state)\ntroops = state.officer_troops\nif two_officer_roster_is_ready(state, troops):\n    commit_two_officer_departure(state)\nassignments = state.officer_city\nif departing_head_is_marked(state, assignments):\n    restore_departing_city_head(state)\nstate.set_action_phase(9)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "two_officer_roster_is_ready": {
    "flow": "troops = state.checked_table(troops)\nfirst = u16(state.first_candidate_officer() << 2)\nif not march_officer_has_troops(troops.long(first)):\n    return False\nsecond = u16(state.second_candidate_officer() << 2)\nreturn march_officer_has_troops(troops.long(second))",
    "returns": "MarchPredicate",
    "signature": "state: GameState, troops: Table"
  },
  "march_officer_has_troops": {
    "flow": "quantity = uint(quantity, 32)\nreturn quantity >= 5000",
    "returns": "MarchPredicate",
    "signature": "quantity: Long"
  },
  "read_march_funds": {
    "flow": "checked_state(state)\nfood = state.city_food\ncity_offset = u16(state.current_city() << 2)\navailable = food.long(city_offset)\nreturn MarchFunds(food, city_offset, available)",
    "returns": "MarchFunds",
    "signature": "state: GameState"
  },
  "two_officer_supply_is_affordable": {
    "flow": "available = uint(available, 32)\nbudget = uint(budget, 32)\nreturn available >= budget",
    "returns": "MarchPredicate",
    "signature": "available: Long, budget: Long"
  },
  "commit_two_officer_departure": {
    "flow": "state.set_march_supply_budget(u16(price_two_officer_march(state)))\nfunds = read_march_funds(state)\nif two_officer_supply_is_affordable(funds.available, state.march_supply_budget()):\n    debit = state.march_supply_budget()\n    funds.food.set_long(funds.city_offset, u32(funds.food.long(funds.city_offset) - debit))\n    append_two_officer_march(state)\n    state.build_ai_movement_packet()\n    mark_two_officers_departing(state)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "mark_two_officers_departing": {
    "flow": "assignments = state.officer_city\nofficer = u8(state.first_candidate_officer())\nassignments.set_byte(officer, assignments.byte(officer) | 64)\nofficer = u8(state.second_candidate_officer())\nassignments.set_byte(officer, assignments.byte(officer) | 64)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "departing_head_is_marked": {
    "flow": "assignments = state.checked_table(assignments)\nheads = state.city_heads\nhead = heads.word(u16(state.current_city() << 1))\nreturn assignments.byte(head) & 64 != 0",
    "returns": "MarchPredicate",
    "signature": "state: GameState, assignments: Table"
  },
  "shortest_unowned_neighbor": {
    "flow": "return query_shortest_unowned_route(state, read_unowned_neighbor_views(state))",
    "returns": "NeighborRoute",
    "signature": "state: GameState"
  },
  "read_unowned_neighbor_views": {
    "flow": "checked_state(state)\ncity_offset = u16(state.current_city() << 3)\nneighbors = state.city_neighbors.cursor(city_offset)\ncoordinates = state.city_coordinates\ncoordinate_offset = city_offset >> 1\nstate.set_path_start_first(coordinates.word(coordinate_offset, displacement=2) >> 4)\nstate.set_path_start_second(coordinates.word(coordinate_offset) >> 4)\nowners = state.city_owner\nreturn UnownedNeighborViews(neighbors, coordinates, owners)",
    "returns": "UnownedNeighborViews",
    "signature": "state: GameState"
  },
  "query_shortest_unowned_route": {
    "flow": "checked_cursor(views.neighbors, state)\nbest_length = 65535\nbest_city = 65535\nwhile True:\n    neighbor = views.neighbors.next_byte()\n    if negative_byte(neighbor):\n        return NeighborRoute(best_length, best_city)\n    if not negative_byte(views.owners.byte(neighbor)):\n        continue\n    offset = u16(neighbor << 2)\n    state.set_path_goal_first(views.coordinates.word(offset, displacement=2) >> 4)\n    state.set_path_goal_second(views.coordinates.word(offset) >> 4)\n    state.build_path_from_cells()\n    if not march_route_improves(best_length, state.path_length()):\n        continue\n    best_length = state.path_length()\n    best_city = neighbor",
    "returns": "NeighborRoute",
    "signature": "state: GameState, views: UnownedNeighborViews"
  },
  "march_route_improves": {
    "flow": "best_length = uint(best_length, 16)\ncandidate_length = uint(candidate_length, 16)\nreturn best_length > candidate_length",
    "returns": "MarchPredicate",
    "signature": "best_length: Word, candidate_length: Word"
  },
  "price_two_officer_march": {
    "flow": "load = read_two_officer_troop_load(state)\nbase_price = calculate_march_base_charge(load.total)\nspeed = read_two_officer_average_speed(state, load)\nstate.set_phase_argument(speed)\ndistance = state.path_length()\nduration = calculate_two_officer_duration(distance, speed)\nquote = MarchQuote(speed, duration, u32(u16(base_price) * duration))\nreturn quote.supply",
    "returns": "Long",
    "signature": "state: GameState"
  },
  "read_two_officer_troop_load": {
    "flow": "checked_state(state)\ntroops = state.officer_troops\nfirst = u16(state.first_candidate_officer() << 2)\ntotal = troops.long(first)\nsecond = u16(state.second_candidate_officer() << 2)\ntotal = u32(total + troops.long(second))\ntotal = u32(total + 200)\nreturn TwoOfficerTroopLoad(first, second, total)",
    "returns": "TwoOfficerTroopLoad",
    "signature": "state: GameState"
  },
  "calculate_march_base_charge": {
    "flow": "total = uint(total, 32)\nencoded_price = divu_retained(total, 10)\nbase_price = u32(u16(encoded_price) * 3)\nreturn base_price",
    "returns": "Long",
    "signature": "total: Long"
  },
  "read_two_officer_average_speed": {
    "flow": "speeds = state.officer_march_speed\nspeed = u8(speeds.byte(load.first_offset >> 2) + speeds.byte(load.second_offset >> 2)) >> 1\nreturn speed",
    "returns": "Word",
    "signature": "state: GameState, load: TwoOfficerTroopLoad"
  },
  "calculate_two_officer_duration": {
    "flow": "distance = uint(distance, 16)\nspeed = uint(speed, 16)\nrounded_distance = u16(u16(distance + speed) - 1)\nduration = divu_retained(rounded_distance, speed)\nduration = u16(u16(duration) + 3)\nreturn duration",
    "returns": "Word",
    "signature": "distance: Word, speed: Word"
  },
  "append_two_officer_march": {
    "flow": "checked_state(state)\npacket = find_march_queue_tail(state)\npacket.set_byte(0, 34)\nwrite_march_origin(state, packet)\npacket.set_byte(3, state.phase_argument_byte())\npacket.set_byte(4, state.current_force_byte())\npacket.set_byte(5, 0)\npacket.set_byte(6, 0)\npacket.set_byte(7, 0)\npacket.set_byte(8, 0)\nwrite_march_budget_bytes(packet, 12, state.march_supply_budget())\npacket.set_byte(13, state.first_candidate_officer_byte())\nstate.set_packed_head(state.first_candidate_officer())\npacket.set_byte(14, state.second_candidate_officer_byte())\npacket.set_byte(15, 0)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "find_march_queue_tail": {
    "flow": "packet = state.packed_groups.cursor()\nwhile True:\n    count = packet.byte() & 15\n    if count == 0:\n        break\n    packet = packet.advance(13 + count)\nreturn packet",
    "returns": "PackedGroupCursor",
    "signature": "state: GameState"
  },
  "write_march_origin": {
    "flow": "checked_cursor(packet, state)\ncoordinates = state.city_coordinates\noffset = u16(state.current_city() << 2)\nfirst = coordinates.word(offset, displacement=2)\nstate.set_packed_first(first)\npacket.set_byte(1, u8(first >> 4))\nsecond = coordinates.word(offset)\nstate.set_packed_second(second)\npacket.set_byte(2, u8(second >> 4))",
    "returns": "None",
    "signature": "state: GameState, packet: PackedGroupCursor"
  },
  "write_march_budget_bytes": {
    "flow": "checked_cursor(packet)\nlast_slot = uint(last_slot, 16)\nbudget = uint(budget, 32)\npacket.set_byte(last_slot, u8(budget))\nbudget >>= 8\npacket.set_byte(u16(last_slot - 1), u8(budget))\nbudget >>= 8\npacket.set_byte(u16(last_slot - 2), u8(budget))\nbudget = u16(budget) >> 8\npacket.set_byte(u16(last_slot - 3), u8(budget))",
    "returns": "None",
    "signature": "packet: PackedGroupCursor, last_slot: Word, budget: Long"
  },
  "restore_departing_city_head": {
    "flow": "checked_state(state)\ndestination = state.support_roster.cursor()\nsource = state.remaining_roster.cursor()\ncopy_remaining_city_roster(source, destination)\nstate.choose_city_head(state.current_city())",
    "returns": "None",
    "signature": "state: GameState"
  },
  "copy_remaining_city_roster": {
    "flow": "checked_cursor(source)\nchecked_cursor(destination, source.state)\nwhile True:\n    officer = source.next_word()\n    destination.append_word(officer)\n    if negative_word(officer):\n        break",
    "returns": "None",
    "signature": "source: Cursor, destination: Cursor"
  },
  "commit_support_march": {
    "flow": "checked_state(state)\ncount = state.roster_count()\nif support_city_has_roster(count):\n    balances = state.city_gold\n    city_offset = u16(state.current_city() << 2)\n    gold = balances.long(city_offset)\n    if support_city_has_gold(gold):\n        state.set_selected_gold_budget(gold >> 1)\n        if not collect_support_officers(state).carry:\n            choose_support_roster(state)\n            if not negative_word(state.scratch_roster.word()):\n                price_support_march(state)\n                funds = read_march_funds(state)\n                if support_supply_is_affordable(funds.available, state.march_supply_budget()):\n                    settle_support_march_funds(state, funds)\n                    append_support_march(state)\n                    state.build_ai_movement_packet()\n                    assignments = mark_selected_support_departing(state)\n                    if departing_head_is_marked(state, assignments):\n                        rebuild_departing_city_head(state)\nstate.set_action_phase(65535)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "support_city_has_roster": {
    "flow": "count = uint(count, 16)\nreturn count >= 3",
    "returns": "MarchPredicate",
    "signature": "count: Word"
  },
  "support_city_has_gold": {
    "flow": "gold = uint(gold, 32)\nreturn gold >= 2000",
    "returns": "MarchPredicate",
    "signature": "gold: Long"
  },
  "support_supply_is_affordable": {
    "flow": "available = uint(available, 32)\nbudget = uint(budget, 32)\nreturn available > budget",
    "returns": "MarchPredicate",
    "signature": "available: Long, budget: Long"
  },
  "settle_support_march_funds": {
    "flow": "available = u32(funds.available - state.march_supply_budget())\nfunds.food.set_long(funds.city_offset, available)\nbalances = state.city_gold\ngold = balances.long(funds.city_offset)\ngold = u32(gold - state.selected_gold_budget())\nbalances.set_long(funds.city_offset, gold)",
    "returns": "None",
    "signature": "state: GameState, funds: MarchFunds"
  },
  "mark_selected_support_departing": {
    "flow": "selected = state.scratch_roster.cursor()\nassignments = state.officer_city\nwhile True:\n    officer = selected.next_word()\n    if negative_word(officer):\n        break\n    assignments.set_byte(officer, assignments.byte(officer) | 64)\nreturn assignments",
    "returns": "Table",
    "signature": "state: GameState"
  },
  "collect_support_officers": {
    "flow": "views = read_support_officer_views(state)\ncount_bytes = collect_eligible_support_officers(views)\nviews.roster.put_word(65535)\nif negative_word(state.support_roster.word()):\n    return state.carry_result(1)\nif negative_word(state.support_roster.word(displacement=2)):\n    return state.carry_result(1)\norder_support_candidates(state, count_bytes)\nreturn state.carry_result(0)",
    "returns": "CarryOutcome",
    "signature": "state: GameState"
  },
  "read_support_officer_views": {
    "flow": "checked_state(state)\nsource = state.route_roster.cursor()\nroster = state.support_roster.cursor()\ntroops = state.officer_troops\nstrengths = state.officer_strength\nscratch = state.scratch_roster.cursor()\nlimits = state.officer_loyalty_limit\nloyalty = state.officer_loyalty\nreturn SupportOfficerViews(source, roster, troops, strengths, scratch, limits, loyalty)",
    "returns": "SupportOfficerViews",
    "signature": "state: GameState"
  },
  "collect_eligible_support_officers": {
    "flow": "count_bytes = 0\nwhile True:\n    officer = views.source.next_word()\n    if negative_word(officer):\n        break\n    officer = u8(officer)\n    offset = u16(officer << 2)\n    if not march_officer_has_troops(views.troops.long(offset)):\n        continue\n    offset >>= 1\n    limit = views.limits.long(offset)\n    if not support_loyalty_allows_departure(limit, views.loyalty.long(offset)):\n        continue\n    views.roster.append_word(officer)\n    views.scratch.append_word(views.strengths.word(offset))\n    count_bytes = u16(count_bytes + 2)\nreturn count_bytes",
    "returns": "Word",
    "signature": "views: SupportOfficerViews"
  },
  "support_loyalty_allows_departure": {
    "flow": "limit = uint(limit, 32)\ncurrent = uint(current, 32)\nreturn limit >= current",
    "returns": "MarchPredicate",
    "signature": "limit: Long, current: Long"
  },
  "order_support_candidates": {
    "flow": "count_bytes = uint(count_bytes, 16)\nroster = state.support_roster\nscratch = state.scratch_roster\nwhile True:\n    offset = 2\n    while True:\n        previous = scratch.word(offset, displacement=-2)\n        if support_strength_requires_swap(previous, scratch.word(offset)):\n            scratch.set_word(u16(offset - 2), scratch.word(offset))\n            scratch.set_word(offset, previous)\n            officer = roster.word(offset, displacement=-2)\n            roster.set_word(u16(offset - 2), roster.word(offset))\n            roster.set_word(offset, officer)\n        offset = u16(offset + 2)\n        if offset >= count_bytes:\n            break\n    count_bytes = u16(count_bytes - 2)\n    if count_bytes >= 2:\n        break",
    "returns": "None",
    "signature": "state: GameState, count_bytes: Word"
  },
  "support_strength_requires_swap": {
    "flow": "previous = uint(previous, 16)\ncurrent = uint(current, 16)\nreturn previous < current",
    "returns": "MarchPredicate",
    "signature": "previous: Word, current: Word"
  },
  "choose_support_roster": {
    "flow": "checked_state(state)\nsource = state.support_roster.cursor()\noutput = state.scratch_roster.cursor()\ndecision = resolve_support_roster_size(state)\nif not decision.accepted:\n    state.scratch_roster.set_word(0, 65535)\n    return\nchosen_count = decision.count\ncopy_selected_support_officers(source, output, chosen_count)\nflags = state.officer_flags\nselected = state.scratch_roster.cursor()\nif selected_support_has_required_flag(selected, flags):\n    if chosen_count <= state.phase_argument():\n        state.scratch_roster.set_word(0, 65535)\n    return\nchosen_count = append_required_support_officer(state, selected, flags, chosen_count)\nif chosen_count <= state.phase_argument():\n    state.scratch_roster.set_word(0, 65535)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "resolve_support_roster_size": {
    "flow": "size = state.phase_argument()\nif size < 2:\n    size = 2\nsize = u16(size + 1)\nif size >= state.roster_count():\n    size = u16(state.roster_count() - 1)\nif size < 2 or size < state.phase_argument():\n    return SupportRosterSize(size, False)\nif size == 0:\n    return SupportRosterSize(size, False)\nreturn SupportRosterSize(size, True)",
    "returns": "SupportRosterSize",
    "signature": "state: GameState"
  },
  "copy_selected_support_officers": {
    "flow": "checked_cursor(source)\nchecked_cursor(output, source.state)\nsize = uint(size, 16)\ncounter = u16(size - 1)\nfor unused in descending_inclusive(counter):\n    output.append_word(source.next_word())\noutput.put_word(65535)",
    "returns": "None",
    "signature": "source: Cursor, output: Cursor, size: Word"
  },
  "selected_support_has_required_flag": {
    "flow": "checked_cursor(selected)\nflags = selected.state.checked_table(flags)\nwhile True:\n    officer = selected.next_word()\n    if negative_word(officer):\n        return False\n    if flags.byte(officer) & 16:\n        return True",
    "returns": "MarchPredicate",
    "signature": "selected: Cursor, flags: Table"
  },
  "append_required_support_officer": {
    "flow": "checked_cursor(selected, state)\nflags = state.checked_table(flags)\nchosen_count = uint(chosen_count, 16)\nlimit = u16(state.roster_count() - 1)\nif chosen_count < limit:\n    source = state.route_roster.cursor()\n    while True:\n        officer = source.next_word()\n        if negative_word(officer):\n            break\n        if not flags.byte(officer) & 16:\n            continue\n        selected.put_word(officer)\n        selected.set_word(0, 65535, displacement=2)\n        chosen_count = u16(chosen_count + 1)\n        break\nreturn chosen_count",
    "returns": "Word",
    "signature": "state: GameState, selected: Cursor, flags: Table, chosen_count: Word"
  },
  "price_support_march": {
    "flow": "initialize_support_march_path(state)\nload = read_support_troop_load(state)\nencoded_average = divu_retained(load.speed_sum, load.count)\naverage = u16(encoded_average)\nstate.set_packed_first(average)\nstate.set_packed_second(load.count)\ndistance = state.path_length()\nduration = calculate_support_duration(distance, average)\nprice = calculate_march_base_charge(load.total)\nquote = MarchQuote(average, duration, u32(u16(price) * duration))\nstate.set_march_supply_budget(quote.supply)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "initialize_support_march_path": {
    "flow": "checked_state(state)\ncoordinates = state.city_coordinates\noffset = u16(state.current_city() << 2)\nstate.set_path_start_first(coordinates.word(offset, displacement=2))\nstate.set_path_start_second(coordinates.word(offset))\noffset = u16(state.target_city() << 2)\nstate.set_path_goal_first(coordinates.word(offset, displacement=2))\nstate.set_path_goal_second(coordinates.word(offset))\nstate.build_path()",
    "returns": "None",
    "signature": "state: GameState"
  },
  "read_support_troop_load": {
    "flow": "roster = state.scratch_roster.cursor()\nspeeds = state.officer_march_speed\ntroops = state.officer_troops\nspeed_sum = 0\ntotal = 0\ncount = 0\nwhile True:\n    officer = roster.next_word()\n    if negative_word(officer):\n        break\n    count = u16(count + 1)\n    speed_sum = u8(speed_sum + speeds.byte(officer))\n    total = u32(total + troops.long(u16(officer << 2)))\n    total = u32(total + 100)\nreturn SupportTroopLoad(speed_sum, total, count)",
    "returns": "SupportTroopLoad",
    "signature": "state: GameState"
  },
  "calculate_support_duration": {
    "flow": "distance = uint(distance, 16)\naverage = uint(average, 16)\nrounded = u16(u16(distance + average) - 1)\nsigned_distance = rounded - 65536 if negative_word(rounded) else rounded\nencoded_duration = divu_retained(u32(signed_distance), average)\nduration = u16(u16(encoded_duration) + 2)\nreturn duration",
    "returns": "Word",
    "signature": "distance: Word, average: Word"
  },
  "append_support_march": {
    "flow": "checked_state(state)\npacket = find_march_queue_tail(state)\nsize = state.packed_second()\npacket.set_byte(0, u8(size | 32))\npacket.set_byte(3, state.packed_first_byte())\npacket.set_byte(4, state.current_force_byte())\nstate.set_phase_argument(state.packed_first())\nwrite_march_origin(state, packet)\nwrite_march_budget_bytes(packet, 8, state.selected_gold_budget())\nwrite_march_budget_bytes(packet, 12, state.march_supply_budget())\noutput = packet.advance(13)\nsource = state.scratch_roster.cursor()\nwrite_support_packet_members(source, output)\nstate.set_packed_head(state.scratch_roster.word())",
    "returns": "None",
    "signature": "state: GameState"
  },
  "write_support_packet_members": {
    "flow": "checked_cursor(source)\nchecked_cursor(output, source.state)\nwhile True:\n    officer = source.next_word()\n    if negative_word(officer):\n        break\n    output.append_byte(u8(officer))\noutput.set_byte(0, 0)",
    "returns": "None",
    "signature": "source: Cursor, output: Cursor"
  },
  "rebuild_departing_city_head": {
    "flow": "checked_state(state)\ncity = state.current_city()\nstate.set_roster_head(65535)\nstate.build_roster(city)\nstate.choose_city_head(city)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "finish_support_phase": {
    "flow": "checked_state(state)\nstate.set_action_phase(65535)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "evaluate_packed_group_supply_phase": {
    "flow": "decision = read_packed_supply_decision(state)\nstate.set_action_phase(2 if packed_supply_is_insufficient(decision.cash, decision.price) else 6)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "read_packed_supply_decision": {
    "flow": "checked_state(state)\ngroup = state.packed_groups.cursor(state.packed_group_offset())\nprice = price_packed_group(state, group)\ncash = read_packed_long_bytes(group, 9)\nreturn PackedSupplyDecision(group, price, cash)",
    "returns": "PackedSupplyDecision",
    "signature": "state: GameState"
  },
  "read_packed_long_bytes": {
    "flow": "checked_cursor(record)\nfirst_slot = uint(first_slot, 16)\ncash = record.byte(first_slot)\ncash = u16(cash << 8)\ncash = cash & 65280 | record.byte(u16(first_slot + 1))\ncash = u32(cash << 8)\ncash = cash & 4294967040 | record.byte(u16(first_slot + 2))\ncash = u32(cash << 8)\ncash = cash & 4294967040 | record.byte(u16(first_slot + 3))\nreturn cash",
    "returns": "Long",
    "signature": "record: Cursor, first_slot: Word"
  },
  "packed_supply_is_insufficient": {
    "flow": "cash = uint(cash, 32)\nprice = uint(price, 32)\nreturn cash < price",
    "returns": "RoutePredicate",
    "signature": "cash: Long, price: Long"
  },
  "price_packed_group": {
    "flow": "return calculate_packed_supply_cost(read_packed_troop_load(state, group))",
    "returns": "Long",
    "signature": "state: GameState, group: PackedGroupCursor"
  },
  "read_packed_troop_load": {
    "flow": "checked_state(state)\nchecked_cursor(group, state)\ncount = u16((group.byte() & 15) - 1)\ntroops = state.officer_troops\ntotal = 0\nfor member in descending_inclusive(count):\n    officer = group.byte(member, displacement=13)\n    total = u32(total + troops.long(u16(officer << 2)))\n    total = u32(total + 100)\nreturn total",
    "returns": "Long",
    "signature": "state: GameState, group: PackedGroupCursor"
  },
  "calculate_packed_supply_cost": {
    "flow": "total = uint(total, 32)\nencoded = divu_retained(total, 10)\nprice = u16(u16(encoded) << 1)\nprice = u16(price + u16(encoded))\nreturn price",
    "returns": "Long",
    "signature": "total: Long"
  },
  "choose_group_destination_phase": {
    "flow": "checked_state(state)\nstate.choose_ai_destination()\nstate.set_action_phase(3 if negative_word(state.target_city()) else 4)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "evaluate_transport_supply_phase": {
    "flow": "supply = read_transport_supply(state)\nif transport_supply_allows_route(supply):\n    if not reachable_transport_coordinate_carry(state).carry:\n        state.set_action_phase(5)\n        return\nstate.set_action_phase(4)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "read_transport_supply": {
    "flow": "checked_state(state)\nrecord = state.officer_packet_data.at(state.packed_group_offset())\nreturn read_packed_long_bytes(record.cursor(), 5)",
    "returns": "Long",
    "signature": "state: GameState"
  },
  "transport_supply_allows_route": {
    "flow": "supply = uint(supply, 32)\nreturn supply >= 500",
    "returns": "RoutePredicate",
    "signature": "supply: Long"
  },
  "reachable_transport_coordinate_carry": {
    "flow": "return query_transport_coordinate(state, read_transport_route_views(state))",
    "returns": "CarryOutcome",
    "signature": "state: GameState"
  },
  "read_transport_route_views": {
    "flow": "checked_state(state)\norigin_first = state.transport_first()\nstate.set_path_start_first(origin_first)\norigin_second = state.transport_second()\nstate.set_path_start_second(origin_second)\nbudget = state.transport_route_budget()\ncandidates = state.coordinate_candidates.cursor()\nreturn TransportRouteViews(origin_first, origin_second, budget, candidates)",
    "returns": "TransportRouteViews",
    "signature": "state: GameState"
  },
  "query_transport_coordinate": {
    "flow": "candidates = views.candidates\nwhile True:\n    first = candidates.byte()\n    if negative_byte(first):\n        return state.carry_result(1)\n    state.set_path_goal_first(first)\n    delta_first = transport_first_delta(first, u8(views.first))\n    if transport_component_within_budget(delta_first, u8(views.budget)):\n        second = candidates.byte(1)\n        state.set_path_goal_second(second)\n        delta_second = transport_second_delta(second, u8(views.second))\n        distance = u8(delta_first + u8(delta_second))\n        if transport_component_within_budget(distance, u8(views.budget)):\n            state.build_path_from_cells()\n            if transport_route_accepts_length(views.budget, state.path_length()):\n                return state.carry_result(0)\n    candidates = candidates.advance(2)",
    "returns": "CarryOutcome",
    "signature": "state: GameState, views: TransportRouteViews"
  },
  "transport_first_delta": {
    "flow": "destination = uint(destination, 8)\norigin = uint(origin, 8)\ndelta = u8(destination - origin)\nif destination < origin:\n    delta = u8(-delta)\nreturn delta",
    "returns": "Word",
    "signature": "destination: Word, origin: Word"
  },
  "transport_second_delta": {
    "flow": "destination = uint(destination, 8)\norigin = uint(origin, 8)\ndelta = u8(destination - origin)\nif destination < origin:\n    delta = u16(-delta)\nreturn delta",
    "returns": "Word",
    "signature": "destination: Word, origin: Word"
  },
  "transport_component_within_budget": {
    "flow": "distance = uint(distance, 8)\nbudget = uint(budget, 8)\nreturn distance <= budget",
    "returns": "RoutePredicate",
    "signature": "distance: Word, budget: Word"
  },
  "transport_route_accepts_length": {
    "flow": "budget = uint(budget, 16)\nlength = uint(length, 16)\nreturn budget <= length",
    "returns": "RoutePredicate",
    "signature": "budget: Word, length: Word"
  },
  "commit_staging_city_phase": {
    "flow": "checked_state(state)\ngroup = choose_nearest_staging_city(state)\nif not negative_word(state.target_city()):\n    commit_staging_departure(state, group)\nstate.set_action_phase(22)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "commit_staging_departure": {
    "flow": "checked_cursor(group, state)\nstate.set_target_city(u16(state.target_city() + 1))\nstate.set_phase_argument(group.byte(3))\nstate.set_packed_head(group.byte(13))\nstate.build_ai_movement_packet()",
    "returns": "None",
    "signature": "state: GameState, group: PackedGroupCursor"
  },
  "choose_nearest_staging_city": {
    "flow": "views = read_staging_search_views(state)\nquery_nearest_staging_city(state, views)\nreturn views.group",
    "returns": "PackedGroupCursor",
    "signature": "state: GameState"
  },
  "read_staging_search_views": {
    "flow": "checked_state(state)\ngroup = state.packed_groups.cursor(state.packed_group_offset())\nfirst = group.byte(1) << 4\nstate.set_path_start_first(first)\nstate.set_packed_first(first)\nfirst >>= 4\nsecond = group.byte(2) << 4\nstate.set_path_start_second(second)\nstate.set_packed_second(second)\nsecond >>= 4\nstate.set_target_city(65535)\ncoordinates = state.city_coordinates_zero_based\nowners = state.city_owner_zero_based\nreturn StagingSearchViews(group, first, second, coordinates, owners)",
    "returns": "StagingSearchViews",
    "signature": "state: GameState"
  },
  "query_nearest_staging_city": {
    "flow": "best_distance = 65535\nfor city in descending_inclusive(39):\n    if views.owners.byte(city) != state.current_force_byte():\n        continue\n    if state.city_roster_full_carry(city).carry:\n        continue\n    offset = u16(city << 2)\n    destination_first = views.coordinates.word(offset, displacement=2) >> 4\n    delta_first = staging_axis_distance(destination_first, views.first)\n    destination_second = views.coordinates.word(offset) >> 4\n    delta_second = staging_axis_distance(destination_second, views.second)\n    distance = u16(delta_second + delta_first)\n    if not staging_distance_improves(distance, best_distance):\n        continue\n    best_distance = distance\n    state.set_target_city(city)",
    "returns": "None",
    "signature": "state: GameState, views: StagingSearchViews"
  },
  "staging_axis_distance": {
    "flow": "destination = uint(destination, 16)\norigin = uint(origin, 16)\ndelta = u16(destination - origin)\nif destination < origin:\n    delta = u16(-delta)\nreturn delta",
    "returns": "Word",
    "signature": "destination: Word, origin: Word"
  },
  "staging_distance_improves": {
    "flow": "candidate = uint(candidate, 16)\nbest = uint(best, 16)\nreturn candidate < best",
    "returns": "RoutePredicate",
    "signature": "candidate: Word, best: Word"
  },
  "choose_destination_progress_phase": {
    "flow": "checked_state(state)\nstate.set_action_phase(21 if destination_has_been_reached(state) else 20)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "destination_has_been_reached": {
    "flow": "first = state.path_goal_first()\nif destination_axis_matches(first, state.path_start_first()):\n    second = state.path_goal_second()\n    if destination_axis_matches(second, state.path_start_second()):\n        return True\nreturn False",
    "returns": "RoutePredicate",
    "signature": "state: GameState"
  },
  "destination_axis_matches": {
    "flow": "goal = uint(goal, 16)\nstart = uint(start, 16)\nreturn goal == start",
    "returns": "RoutePredicate",
    "signature": "goal: Word, start: Word"
  },
  "choose_terrain_exit_phase": {
    "flow": "checked_state(state)\nif query_adjacent_terrain_exit(state):\n    located = locate_packet_contact_city(state)\n    state.set_action_phase(13 if located.carry else 24)\nelse:\n    state.set_action_phase(13)",
    "returns": "None",
    "signature": "state: GameState"
  },
  "query_adjacent_terrain_exit": {
    "flow": "row = state.transport_first()\noffset = u16(u16(u16(row << 3) + state.transport_first()) << 3)\noffset = u16(offset + state.transport_second())\nterrain = state.terrain_types\nif terrain_kind_is_exit(terrain.byte(offset, displacement=-72)):\n    return True\nif terrain_kind_is_exit(terrain.byte(offset, displacement=-1)):\n    return True\nif terrain_kind_is_exit(terrain.byte(offset, displacement=1)):\n    return True\nif terrain_kind_is_exit(terrain.byte(offset, displacement=72)):\n    return True\nreturn False",
    "returns": "RoutePredicate",
    "signature": "state: GameState"
  },
  "terrain_kind_is_exit": {
    "flow": "kind = uint(kind, 8)\nreturn kind == 1",
    "returns": "RoutePredicate",
    "signature": "kind: Word"
  }
}
MARCH_SOURCE_FUNCTIONS = ('commit_unowned_neighbor_march', 'two_officer_roster_is_ready', 'march_officer_has_troops', 'read_march_funds', 'two_officer_supply_is_affordable', 'commit_two_officer_departure', 'mark_two_officers_departing', 'departing_head_is_marked', 'shortest_unowned_neighbor', 'read_unowned_neighbor_views', 'query_shortest_unowned_route', 'march_route_improves', 'price_two_officer_march', 'read_two_officer_troop_load', 'calculate_march_base_charge', 'read_two_officer_average_speed', 'calculate_two_officer_duration', 'append_two_officer_march', 'find_march_queue_tail', 'write_march_origin', 'write_march_budget_bytes', 'restore_departing_city_head', 'copy_remaining_city_roster', 'commit_support_march', 'support_city_has_roster', 'support_city_has_gold', 'support_supply_is_affordable', 'settle_support_march_funds', 'mark_selected_support_departing', 'collect_support_officers', 'read_support_officer_views', 'collect_eligible_support_officers', 'support_loyalty_allows_departure', 'order_support_candidates', 'support_strength_requires_swap', 'choose_support_roster', 'resolve_support_roster_size', 'copy_selected_support_officers', 'selected_support_has_required_flag', 'append_required_support_officer', 'price_support_march', 'initialize_support_march_path', 'read_support_troop_load', 'calculate_support_duration', 'append_support_march', 'write_support_packet_members', 'rebuild_departing_city_head', 'finish_support_phase')
TRANSPORT_SOURCE_FUNCTIONS = ('choose_neighbor_relation_phase', 'hostile_neighbor_exists_carry', 'read_neighbor_query_views', 'query_foreign_neighbor', 'neighbor_owner_is_foreign', 'choose_unowned_neighbor_phase', 'unowned_neighbor_exists_carry', 'query_unowned_neighbor', 'choose_roster_troop_phase', 'roster_troop_threshold_met', 'count_roster_large_troops', 'roster_officer_has_large_troops', 'choose_random_neighbor_phase', 'decide_random_neighbor_phase', 'choose_roster_troop_phase_five', 'evaluate_neighbor_march_phase', 'sum_city_officer_troops', 'city_troop_word_qualifies', 'choose_weaker_enemy_neighbor', 'query_weaker_enemy_neighbor', 'enemy_total_is_weaker', 'enemy_roster_is_eligible', 'commit_enemy_neighbor_choice', 'evaluate_packed_group_supply_phase', 'read_packed_supply_decision', 'read_packed_long_bytes', 'packed_supply_is_insufficient', 'price_packed_group', 'read_packed_troop_load', 'calculate_packed_supply_cost', 'choose_group_destination_phase', 'evaluate_transport_supply_phase', 'read_transport_supply', 'transport_supply_allows_route', 'reachable_transport_coordinate_carry', 'read_transport_route_views', 'query_transport_coordinate', 'transport_first_delta', 'transport_second_delta', 'transport_component_within_budget', 'transport_route_accepts_length', 'commit_staging_city_phase', 'commit_staging_departure', 'choose_nearest_staging_city', 'read_staging_search_views', 'query_nearest_staging_city', 'staging_axis_distance', 'staging_distance_improves', 'choose_destination_progress_phase', 'destination_has_been_reached', 'destination_axis_matches', 'choose_terrain_exit_phase', 'query_adjacent_terrain_exit', 'terrain_kind_is_exit')
DECLARATIONS['march_officer_has_troops']['slots'] = {5000:('march_troop_threshold',0,4294967295)}
DECLARATIONS['support_city_has_roster']['slots'] = {3:('support_roster_threshold',0,65535)}
DECLARATIONS['support_city_has_gold']['slots'] = {2000:('support_gold_threshold',0,4294967295)}
DECLARATIONS['roster_officer_has_large_troops']['slots'] = {5000:('large_troop_threshold',0,65535)}
DECLARATIONS['city_troop_word_qualifies']['slots'] = {5000:('city_troop_threshold',0,65535)}
DECLARATIONS['transport_supply_allows_route']['slots'] = {500:('transport_supply_threshold',0,4294967295)}

APPROVED = {
    'domain': {'GameState','Word','Long','Table','Cursor','PackedGroupCursor','CityTroopSummary',
        'NeighborRoute','CarryOutcome','checked_state','checked_city_troop_summary',
        'checked_cursor','uint','u8','u16','u32','negative_byte','negative_word',
        'descending_inclusive','divu_retained'},
    'business_economy': {'sort_equipment_roster'},
    'business_actions': {'locate_packet_contact_city'},
    'contexts_march': {'MarchPredicate','UnownedNeighborViews','MarchFunds',
        'TwoOfficerTroopLoad','SupportOfficerViews','SupportRosterSize',
        'SupportTroopLoad','MarchQuote'},
    'contexts_transport': {'RoutePredicate','NeighborQueryViews',
        'PackedSupplyDecision','TransportRouteViews','StagingSearchViews'},
}


def _address(binding):
    address = binding['address']
    return f"0x{address & 65535:x}:w" if binding['suffix'] == 'w' else f'0x{address:x}:l'


def _scalar(name):
    return _address(SCALAR_BINDINGS[name])


def _table(name):
    return _address(TABLE_BINDINGS[name])


def _lea(e, name, register):
    b = TABLE_BINDINGS[name]
    e.ins('lea.l', _address(b) + ',' + register, 4 if b['suffix'] == 'w' else 6)


def _load(e, name, register, size='w'):
    b = SCALAR_BINDINGS[name]
    e.ins('move.' + size, _address(b) + ',' + register, 4 if b['suffix'] == 'w' else 6)


def _store(e, register, name, size='w'):
    b = SCALAR_BINDINGS[name]
    e.ins('move.' + size, register + ',' + _address(b), 4 if b['suffix'] == 'w' else 6)


def _literal(e, value, name, size='w'):
    b = SCALAR_BINDINGS[name]
    extension = 4 if size == 'l' else 2
    e.ins('move.' + size, f'#{value},' + _address(b), extension + (4 if b['suffix'] == 'w' else 6))


def _call(e, name, size='w', *, absolute=False, offset=0):
    if name not in BY_NAME:
        raise CompileError('declared target callee required')
    symbol = name if not offset else '(' + name + f'+{offset})'
    if absolute:
        e.ins('jsr', symbol + ':l', 6)
    else:
        e.ins('bsr.' + size, symbol, 2 if size == 'b' else 4)


def _branch(e, condition, label, size='w'):
    e.ins('b' + condition + '.' + size, label, 2 if size == 'b' else 4)


def _carry(e, enabled):
    e.ins('ori.w' if enabled else 'andi.w', '#1,%sr' if enabled else '#65534,%sr', 4)


def _phase_pair(e, callee, plain, carried, *, call_size='w'):
    yes, done = e.fresh('selected'), e.fresh('done')
    _call(e, callee, call_size)
    _branch(e, 'cs', yes)
    _literal(e, plain, 'action_phase')
    _branch(e, 'ra', done)
    e.label(yes)
    _literal(e, carried, 'action_phase')
    e.label(done)


def _choose_neighbor_relation_phase(e, rules):
    _phase_pair(e, 'hostile_neighbor_exists_carry', 2, 4)


def _hostile_neighbor_exists_carry(e, rules):
    scan, absent, done = e.fresh('scan'), e.fresh('absent'), e.fresh('done')
    _lea(e, 'city_neighbors', '%a0')
    _load(e, 'current_city', '%d0')
    e.ins('lsl.w', '#3,%d0')
    e.ins('adda.w', '%d0,%a0')
    _lea(e, 'city_owner', '%a1')
    _load(e, 'current_force', '%d1')
    e.label(scan)
    e.ins('move.b', '(%a0)+,%d0')
    _branch(e, 'mi', absent)
    e.ins('andi.w', '#255,%d0', 4)
    e.ins('move.b', '(%a1,%d0.w),%d2', 4)
    _branch(e, 'mi', scan, 'b')
    e.ins('cmp.b', '%d1,%d2')
    _branch(e, rules['foreign_owner_false_branch'], scan, 'b')
    _carry(e, True)
    _branch(e, 'ra', done)
    e.label(absent)
    _carry(e, False)
    e.label(done)


def _choose_unowned_neighbor_phase(e, rules):
    _phase_pair(e, 'unowned_neighbor_exists_carry', 9, 3)


def _unowned_neighbor_exists_carry(e, rules):
    scan, absent, done = e.fresh('scan'), e.fresh('absent'), e.fresh('done')
    _lea(e, 'city_neighbors', '%a0')
    _load(e, 'current_city', '%d0')
    e.ins('lsl.w', '#3,%d0')
    e.ins('adda.w', '%d0,%a0')
    _lea(e, 'city_owner', '%a1')
    e.label(scan)
    e.ins('move.b', '(%a0)+,%d0')
    _branch(e, 'mi', absent)
    e.ins('andi.w', '#255,%d0', 4)
    e.ins('tst.b', '(%a1,%d0.w)', 4)
    _branch(e, 'pl', scan, 'b')
    _carry(e, True)
    _branch(e, 'ra', done)
    e.label(absent)
    _carry(e, False)
    e.label(done)


def _count_phase(e, count, call_size='w', false_branch='cs'):
    insufficient, done = e.fresh('insufficient'), e.fresh('done')
    _call(e, 'count_roster_large_troops', call_size)
    e.ins('cmpi.w', f'#{count},%d0', 4)
    _branch(e, false_branch, insufficient)
    _literal(e, 7, 'action_phase')
    _branch(e, 'ra', done)
    e.label(insufficient)
    _literal(e, 9, 'action_phase')
    e.label(done)


def _choose_roster_troop_phase(e, rules):
    _count_phase(e, 3, false_branch=rules['roster_count_false_branch'])


def _count_roster_large_troops(e, rules):
    scan, done = e.fresh('scan'), e.fresh('done')
    _lea(e, 'route_roster', '%a0')
    e.ins('clr.w', '%d0')
    _lea(e, 'officer_troops', '%a1')
    e.label(scan)
    e.ins('move.w', '(%a0)+,%d1')
    _branch(e, 'mi', done)
    e.ins('andi.w', '#255,%d1', 4)
    e.ins('lsl.w', '#2,%d1')
    e.ins('cmpi.l', f"#{rules['large_troop_threshold']},(%a1,%d1.w)", 8)
    _branch(e, rules['large_troop_false_branch'], scan, 'b')
    e.ins('addq.w', '#1,%d0')
    _branch(e, 'ra', scan, 'b')
    e.label(done)


def _choose_random_neighbor_phase(e, rules):
    plain, carried, done = e.fresh('plain'), e.fresh('carried'), e.fresh('done')
    _call(e, 'step_random', absolute=True)
    e.ins('btst.l', '#2,%d0', 4)
    _branch(e, 'eq', plain)
    _call(e, 'unowned_neighbor_exists_carry')
    _branch(e, 'cs', carried)
    e.label(plain)
    _literal(e, 6, 'action_phase')
    _branch(e, 'ra', done)
    e.label(carried)
    _literal(e, 5, 'action_phase')
    e.label(done)


def _choose_roster_troop_phase_five(e, rules):
    _count_phase(e, 5, 'b', rules['roster_count_false_branch'])


def _evaluate_neighbor_march_phase(e, rules):
    carried, done = e.fresh('carried'), e.fresh('done')
    _load(e, 'current_city', '%d0')
    _call(e, 'sum_city_officer_troops')
    e.ins('move.l', '%d1,%d6')
    e.ins('move.w', '%d2,%d7')
    _call(e, 'choose_weaker_enemy_neighbor')
    _branch(e, 'cs', carried)
    _literal(e, 9, 'action_phase')
    _branch(e, 'ra', done)
    e.label(carried)
    _literal(e, 8, 'action_phase')
    e.label(done)


def _sum_city_officer_troops(e, rules):
    scan, next_officer = e.fresh('scan'), e.fresh('next_officer')
    e.ins('movem.l', '%d3-%d4/%a0-%a1,-(%a7)', 4)
    _lea(e, 'officer_city', '%a0')
    e.ins('clr.l', '%d1')
    e.ins('clr.w', '%d2')
    _lea(e, 'officer_troops', '%a1')
    e.ins('move.w', '#255,%d3', 4)
    e.label(scan)
    e.ins('cmp.b', '(%a0,%d3.w),%d0', 4)
    _branch(e, 'ne', next_officer)
    e.ins('move.w', '%d3,%d4')
    e.ins('lsl.w', '#2,%d4')
    e.ins('move.l', '(%a1,%d4.w),%d4', 4)
    e.ins('add.l', '%d4,%d1')
    e.ins('cmpi.w', f"#{rules['city_troop_threshold']},%d4", 4)
    _branch(e, rules['city_troop_false_branch'], next_officer)
    e.ins('addq.w', '#1,%d2')
    e.label(next_officer)
    e.ins('dbra', '%d3,' + scan, 4)
    e.ins('movem.l', '(%a7)+,%d3-%d4/%a0-%a1', 4)


def _choose_weaker_enemy_neighbor(e, rules):
    scan, absent, done = e.fresh('scan'), e.fresh('absent'), e.fresh('done')
    _lea(e, 'city_neighbors', '%a2')
    _load(e, 'current_city', '%d0')
    e.ins('lsl.w', '#3,%d0')
    e.ins('adda.w', '%d0,%a2')
    _lea(e, 'city_owner', '%a3')
    e.label(scan)
    e.ins('move.b', '(%a2)+,%d0')
    _branch(e, 'mi', absent)
    e.ins('andi.w', '#255,%d0', 4)
    e.ins('move.b', '(%a3,%d0.w),%d5', 4)
    _branch(e, 'mi', scan, 'b')
    e.ins('cmp.b', _scalar('current_force_byte') + ',%d5', 4)
    _branch(e, rules['foreign_owner_false_branch'], scan, 'b')
    _call(e, 'sum_city_officer_troops', 'b')
    e.ins('cmp.l', '%d6,%d1')
    _branch(e, rules['enemy_total_false_branch'], scan, 'b')
    e.ins('cmp.w', '%d7,%d2')
    _branch(e, rules['enemy_roster_false_branch'], scan, 'b')
    _store(e, '%d0', 'target_city')
    _store(e, '%d2', 'phase_argument')
    _carry(e, True)
    _branch(e, 'ra', done)
    e.label(absent)
    _carry(e, False)
    e.label(done)


def _commit_unowned_neighbor_march(e, rules):
    head_check, done = e.fresh('head_check'), e.fresh('done')
    _call(e, 'shortest_unowned_neighbor')
    _store(e, '%d0', 'path_length')
    _store(e, '%d1', 'target_city')
    _call(e, 'sort_equipment_roster')
    _lea(e, 'officer_troops', '%a0')
    for name in ('first_candidate_officer', 'second_candidate_officer'):
        _load(e, name, '%d0')
        e.ins('lsl.w', '#2,%d0')
        e.ins('cmpi.l', f"#{rules['march_troop_threshold']},(%a0,%d0.w)", 8)
        _branch(e, rules['troop_false_branch'], head_check)
    _call(e, 'price_two_officer_march')
    e.ins('andi.l', '#65535,%d0', 6)
    _store(e, '%d0', 'march_supply_budget', 'l')
    _lea(e, 'city_food', '%a0')
    _load(e, 'current_city', '%d0')
    e.ins('lsl.w', '#2,%d0')
    e.ins('move.l', '(%a0,%d0.w),%d1', 4)
    e.ins('cmp.l', _scalar('march_supply_budget') + ',%d1', 4)
    _branch(e, rules['pair_food_false_branch'], head_check)
    _load(e, 'march_supply_budget', '%d1', 'l')
    e.ins('sub.l', '%d1,(%a0,%d0.w)', 4)
    _call(e, 'append_two_officer_march')
    _call(e, 'build_ai_movement_packet')
    _lea(e, 'officer_city', '%a0')
    for name in ('first_candidate_officer', 'second_candidate_officer'):
        _load(e, name, '%d0')
        e.ins('andi.w', '#255,%d0', 4)
        e.ins('bset.b', '#6,(%a0,%d0.w)', 6)
    e.label(head_check)
    _lea(e, 'officer_city', '%a0')
    _lea(e, 'city_heads', '%a1')
    _load(e, 'current_city', '%d0')
    e.ins('lsl.w', '#1,%d0')
    e.ins('move.w', '(%a1,%d0.w),%d0', 4)
    e.ins('btst.b', '#6,(%a0,%d0.w)', 6)
    _branch(e, 'eq', done)
    _call(e, 'restore_departing_city_head')
    e.label(done)
    _literal(e, 9, 'action_phase')


def _shortest_unowned_neighbor(e, rules):
    scan, done = e.fresh('scan'), e.fresh('done')
    _lea(e, 'city_neighbors', '%a0')
    _load(e, 'current_city', '%d0')
    e.ins('lsl.w', '#3,%d0')
    e.ins('adda.w', '%d0,%a0')
    _lea(e, 'city_coordinates', '%a1')
    e.ins('lsr.w', '#1,%d0')
    for displacement, destination in ((2,'path_start_first'),(0,'path_start_second')):
        prefix='2' if displacement else ''
        e.ins('move.w', prefix + '(%a1,%d0.w),%d1', 4)
        e.ins('lsr.w', '#4,%d1')
        _store(e, '%d1', destination)
    e.ins('move.w', '#65535,%d0', 4)
    e.ins('move.w', '#65535,%d1', 4)
    _lea(e, 'city_owner', '%a2')
    e.label(scan)
    e.ins('move.b', '(%a0)+,%d2')
    _branch(e, 'mi', done)
    e.ins('andi.w', '#255,%d2', 4)
    e.ins('tst.b', '(%a2,%d2.w)', 4)
    _branch(e, 'pl', scan, 'b')
    e.ins('lsl.w', '#2,%d2')
    for displacement, destination in ((2,'path_goal_first'),(0,'path_goal_second')):
        prefix='2' if displacement else ''
        e.ins('move.w', prefix + '(%a1,%d2.w),%d3', 4)
        e.ins('lsr.w', '#4,%d3')
        _store(e, '%d3', destination)
    e.ins('movem.l', '%d0-%d2/%a0-%a2,-(%a7)', 4)
    _call(e, 'build_path', absolute=True, offset=4)
    e.ins('movem.l', '(%a7)+,%d0-%d2/%a0-%a2', 4)
    e.ins('cmp.w', _scalar('path_length') + ',%d0', 4)
    _branch(e, rules['route_false_branch'], scan, 'b')
    _load(e, 'path_length', '%d0')
    e.ins('lsr.w', '#2,%d2')
    e.ins('move.w', '%d2,%d1')
    _branch(e, 'ra', scan, 'b')
    e.label(done)


def _price_two_officer_march(e, rules):
    _lea(e, 'officer_troops', '%a0')
    _load(e, 'first_candidate_officer', '%d1')
    e.ins('lsl.w', '#2,%d1')
    e.ins('move.l', '(%a0,%d1.w),%d0', 4)
    _load(e, 'second_candidate_officer', '%d2')
    e.ins('lsl.w', '#2,%d2')
    e.ins('add.l', '(%a0,%d2.w),%d0', 4)
    e.ins('addi.l', '#200,%d0', 6)
    e.ins('divu.w', '#10,%d0', 4)
    e.ins('mulu.w', '#3,%d0', 4)
    e.ins('lsr.w', '#2,%d1')
    e.ins('lsr.w', '#2,%d2')
    _lea(e, 'officer_march_speed', '%a0')
    e.ins('move.b', '(%a0,%d1.w),%d3', 4)
    e.ins('add.b', '(%a0,%d2.w),%d3', 4)
    e.ins('andi.w', '#255,%d3', 4)
    e.ins('lsr.w', '#1,%d3')
    _store(e, '%d3', 'phase_argument')
    e.ins('moveq', '#0,%d4')
    _load(e, 'path_length', '%d4')
    e.ins('add.w', '%d3,%d4')
    e.ins('subq.w', '#1,%d4')
    e.ins('divu.w', '%d3,%d4')
    e.ins('addq.w', '#3,%d4')
    e.ins('mulu.w', '%d4,%d0')


def _find_packed_tail(e):
    scan, found = e.fresh('scan'), e.fresh('found')
    _lea(e, 'packed_groups', '%a0')
    e.label(scan)
    e.ins('move.b', '(%a0),%d0')
    e.ins('andi.w', '#15,%d0', 4)
    _branch(e, 'eq', found)
    e.ins('lea.l', '13(%a0,%d0.w),%a0', 4)
    _branch(e, 'ra', scan, 'b')
    e.label(found)


def _write_origin(e):
    _lea(e, 'city_coordinates', '%a1')
    _load(e, 'current_city', '%d0')
    e.ins('lsl.w', '#2,%d0')
    for displacement, destination, slot in ((2,'packed_first',1),(0,'packed_second',2)):
        prefix='2' if displacement else ''
        e.ins('move.w', prefix + '(%a1,%d0.w),%d1', 4)
        _store(e, '%d1', destination)
        e.ins('lsr.w', '#4,%d1')
        e.ins('move.b', f'%d1,{slot}(%a0)', 4)


def _write_reversed_long(e, scalar, high_slot):
    _load(e, scalar, '%d1', 'l')
    for ordinal, slot in enumerate(range(high_slot, high_slot-4, -1)):
        e.ins('move.b', f'%d1,{slot}(%a0)', 4)
        if ordinal < 3:
            e.ins('lsr.w' if ordinal == 2 else 'lsr.l', '#8,%d1')


def _append_two_officer_march(e, rules):
    _find_packed_tail(e)
    e.ins('move.b', '#34,(%a0)', 4)
    _write_origin(e)
    e.ins('move.b', _scalar('phase_argument_byte') + ',3(%a0)', 6)
    e.ins('move.b', _scalar('current_force_byte') + ',4(%a0)', 6)
    for slot in range(5, 9):
        e.ins('clr.b', f'{slot}(%a0)', 4)
    _write_reversed_long(e, 'march_supply_budget', 12)
    e.ins('move.b', _scalar('first_candidate_officer_byte') + ',13(%a0)', 6)
    e.ins('move.w', _scalar('first_candidate_officer') + ',' + _scalar('packed_head'), 6)
    e.ins('move.b', _scalar('second_candidate_officer_byte') + ',14(%a0)', 6)
    e.ins('clr.b', '15(%a0)', 4)


def _restore_departing_city_head(e, rules):
    scan = e.fresh('scan')
    _lea(e, 'support_roster', '%a0')
    _lea(e, 'remaining_roster', '%a1')
    e.label(scan)
    e.ins('move.w', '(%a1)+,(%a0)+')
    _branch(e, 'pl', scan, 'b')
    _load(e, 'current_city', '%d0')
    _call(e, 'choose_city_head', absolute=True)


def _commit_support_march(e, rules):
    finish, mark, heads = e.fresh('finish'), e.fresh('mark'), e.fresh('heads')
    _load(e, 'roster_count', '%d0')
    e.ins('cmpi.w', f"#{rules['support_roster_threshold']},%d0", 4)
    _branch(e, rules['support_roster_false_branch'], finish)
    _lea(e, 'city_gold', '%a0')
    _load(e, 'current_city', '%d0')
    e.ins('lsl.w', '#2,%d0')
    e.ins('move.l', '(%a0,%d0.w),%d0', 4)
    e.ins('cmpi.l', f"#{rules['support_gold_threshold']},%d0", 6)
    _branch(e, rules['support_gold_false_branch'], finish)
    e.ins('lsr.l', '#1,%d0')
    _store(e, '%d0', 'selected_gold_budget', 'l')
    _call(e, 'collect_support_officers')
    _branch(e, 'cs', finish)
    _call(e, 'choose_support_roster')
    e.ins('tst.w', _table('scratch_roster'), 4)
    _branch(e, 'mi', finish)
    _call(e, 'price_support_march')
    _lea(e, 'city_food', '%a0')
    _load(e, 'current_city', '%d0')
    e.ins('lsl.w', '#2,%d0')
    e.ins('move.l', '(%a0,%d0.w),%d1', 4)
    e.ins('cmp.l', _scalar('march_supply_budget') + ',%d1', 4)
    _branch(e, rules['support_food_false_branch'], finish)
    e.ins('sub.l', _scalar('march_supply_budget') + ',%d1', 4)
    e.ins('move.l', '%d1,(%a0,%d0.w)', 4)
    _lea(e, 'city_gold', '%a0')
    e.ins('move.l', '(%a0,%d0.w),%d1', 4)
    e.ins('sub.l', _scalar('selected_gold_budget') + ',%d1', 4)
    e.ins('move.l', '%d1,(%a0,%d0.w)', 4)
    _call(e, 'append_support_march')
    _call(e, 'build_ai_movement_packet')
    _lea(e, 'scratch_roster', '%a0')
    _lea(e, 'officer_city', '%a1')
    e.label(mark)
    e.ins('move.w', '(%a0)+,%d0')
    _branch(e, 'mi', heads)
    e.ins('bset.b', '#6,(%a1,%d0.w)', 6)
    _branch(e, 'ra', mark, 'b')
    e.label(heads)
    _lea(e, 'city_heads', '%a0')
    _load(e, 'current_city', '%d0')
    e.ins('move.w', '%d0,%d1')
    e.ins('lsl.w', '#1,%d1')
    e.ins('move.w', '(%a0,%d1.w),%d1', 4)
    e.ins('btst.b', '#6,(%a1,%d1.w)', 6)
    _branch(e, 'eq', finish)
    _call(e, 'rebuild_departing_city_head')
    e.label(finish)
    _literal(e, 65535, 'action_phase')


def _collect_support_officers(e, rules):
    scan, collected = e.fresh('scan'), e.fresh('collected')
    outer, inner, next_item = e.fresh('outer'), e.fresh('inner'), e.fresh('next_item')
    absent, done = e.fresh('absent'), e.fresh('done')
    for name, register in (('route_roster','%a0'),('support_roster','%a1'),
        ('officer_troops','%a2'),('officer_strength','%a3'),('scratch_roster','%a4'),
        ('officer_loyalty_limit','%a5'),('officer_loyalty','%a6')):
        _lea(e, name, register)
    e.ins('clr.w', '%d0')
    e.label(scan)
    e.ins('move.w', '(%a0)+,%d1')
    _branch(e, 'mi', collected)
    e.ins('andi.w', '#255,%d1', 4)
    e.ins('move.w', '%d1,%d2')
    e.ins('lsl.w', '#2,%d2')
    e.ins('cmpi.l', f"#{rules['march_troop_threshold']},(%a2,%d2.w)", 8)
    _branch(e, rules['troop_false_branch'], scan, 'b')
    e.ins('lsr.w', '#1,%d2')
    e.ins('move.l', '(%a5,%d2.w),%d3', 4)
    e.ins('cmp.l', '(%a6,%d2.w),%d3', 4)
    _branch(e, rules['loyalty_false_branch'], scan, 'b')
    e.ins('move.w', '%d1,(%a1)+')
    e.ins('move.w', '(%a3,%d2.w),(%a4)+', 4)
    e.ins('addq.w', '#2,%d0')
    _branch(e, 'ra', scan, 'b')
    e.label(collected)
    e.ins('move.w', '#65535,(%a1)', 4)
    e.ins('tst.w', _table('support_roster'), 4)
    _branch(e, 'mi', absent)
    e.ins('tst.w', '0xf502:w', 4)
    _branch(e, 'mi', absent)
    _lea(e, 'support_roster', '%a1')
    _lea(e, 'scratch_roster', '%a2')
    e.label(outer)
    e.ins('move.w', '#2,%d1', 4)
    e.label(inner)
    e.ins('move.w', '-2(%a2,%d1.w),%d2', 4)
    e.ins('cmp.w', '(%a2,%d1.w),%d2', 4)
    _branch(e, rules['strength_false_branch'], next_item)
    e.ins('move.w', '(%a2,%d1.w),-2(%a2,%d1.w)', 6)
    e.ins('move.w', '%d2,(%a2,%d1.w)', 4)
    e.ins('move.w', '-2(%a1,%d1.w),%d2', 4)
    e.ins('move.w', '(%a1,%d1.w),-2(%a1,%d1.w)', 6)
    e.ins('move.w', '%d2,(%a1,%d1.w)', 4)
    e.label(next_item)
    e.ins('addq.w', '#2,%d1')
    e.ins('cmp.w', '%d0,%d1')
    _branch(e, 'cs', inner, 'b')
    e.ins('subq.w', '#2,%d0')
    e.ins('cmpi.w', '#2,%d0', 4)
    _branch(e, 'cs', outer, 'b')
    _carry(e, False)
    _branch(e, 'ra', done)
    e.label(absent)
    _carry(e, True)
    e.label(done)


def _choose_support_roster(e, rules):
    minimum, limited, failed, done = (e.fresh(s) for s in ('minimum','limited','failed','done'))
    copy, scan, extra, search, compare = (e.fresh(s) for s in ('copy','scan','extra','search','compare'))
    _lea(e, 'support_roster', '%a0')
    _lea(e, 'scratch_roster', '%a1')
    _load(e, 'phase_argument', '%d0')
    e.ins('cmpi.w', '#2,%d0', 4)
    _branch(e, 'cc', minimum)
    e.ins('move.w', '#2,%d0', 4)
    e.label(minimum)
    e.ins('addq.w', '#1,%d0')
    e.ins('cmp.w', _scalar('roster_count') + ',%d0', 4)
    _branch(e, 'cs', limited)
    _load(e, 'roster_count', '%d0')
    e.ins('subq.w', '#1,%d0')
    e.label(limited)
    e.ins('cmpi.w', '#2,%d0', 4)
    _branch(e, 'cs', failed)
    e.ins('cmp.w', _scalar('phase_argument') + ',%d0', 4)
    _branch(e, 'cs', failed)
    e.ins('move.w', '%d0,%d1')
    e.ins('subq.w', '#1,%d0')
    _branch(e, 'cs', failed)
    e.label(copy)
    e.ins('move.w', '(%a0)+,(%a1)+')
    e.ins('dbra', '%d0,' + copy, 4)
    e.ins('move.w', '#65535,(%a1)', 4)
    _lea(e, 'officer_flags', '%a0')
    _lea(e, 'scratch_roster', '%a1')
    e.label(scan)
    e.ins('move.w', '(%a1)+,%d0')
    _branch(e, 'mi', extra)
    e.ins('btst.b', '#4,(%a0,%d0.w)', 6)
    _branch(e, 'ne', compare)
    _branch(e, 'ra', scan, 'b')
    e.label(extra)
    _load(e, 'roster_count', '%d0')
    e.ins('subq.w', '#1,%d0')
    e.ins('cmp.w', '%d0,%d1')
    _branch(e, 'cc', compare)
    _lea(e, 'route_roster', '%a2')
    e.label(search)
    e.ins('move.w', '(%a2)+,%d0')
    _branch(e, 'mi', compare)
    e.ins('btst.b', '#4,(%a0,%d0.w)', 6)
    _branch(e, 'eq', search, 'b')
    e.ins('move.w', '%d0,(%a1)')
    e.ins('move.w', '#65535,2(%a1)', 6)
    e.ins('addq.w', '#1,%d1')
    e.label(compare)
    e.ins('cmp.w', _scalar('phase_argument') + ',%d1', 4)
    _branch(e, 'ls', failed)
    _branch(e, 'ra', done)
    e.label(failed)
    e.ins('move.w', '#65535,' + _table('scratch_roster'), 6)
    e.label(done)


def _price_support_march(e, rules):
    _lea(e, 'city_coordinates', '%a0')
    for source, first, second in (('current_city','path_start_first','path_start_second'),
        ('target_city','path_goal_first','path_goal_second')):
        _load(e, source, '%d0')
        e.ins('lsl.w', '#2,%d0')
        e.ins('move.w', '2(%a0,%d0.w),' + _scalar(first), 6)
        e.ins('move.w', '(%a0,%d0.w),' + _scalar(second), 6)
    _call(e, 'build_path', absolute=True)
    _lea(e, 'scratch_roster', '%a0')
    _lea(e, 'officer_march_speed', '%a1')
    _lea(e, 'officer_troops', '%a2')
    e.ins('clr.w', '%d0')
    e.ins('moveq', '#0,%d1')
    e.ins('clr.w', '%d3')
    scan, priced = e.fresh('scan'), e.fresh('priced')
    e.label(scan)
    e.ins('move.w', '(%a0)+,%d2')
    _branch(e, 'mi', priced, 'b')
    e.ins('addq.w', '#1,%d3')
    e.ins('add.b', '(%a1,%d2.w),%d0', 4)
    e.ins('lsl.w', '#2,%d2')
    e.ins('add.l', '(%a2,%d2.w),%d1', 4)
    e.ins('addi.l', '#100,%d1', 6)
    _branch(e, 'ra', scan, 'b')
    e.label(priced)
    e.ins('ext.l', '%d0')
    e.ins('divu.w', '%d3,%d0')
    _store(e, '%d0', 'packed_first')
    _store(e, '%d3', 'packed_second')
    _load(e, 'path_length', '%d2')
    e.ins('add.w', '%d0,%d2')
    e.ins('subq.w', '#1,%d2')
    e.ins('ext.l', '%d2')
    e.ins('divu.w', '%d0,%d2')
    e.ins('addi.w', '#2,%d2', 4)
    e.ins('divu.w', '#10,%d1', 4)
    e.ins('mulu.w', '#3,%d1', 4)
    e.ins('mulu.w', '%d2,%d1')
    _store(e, '%d1', 'march_supply_budget', 'l')


def _append_support_march(e, rules):
    _find_packed_tail(e)
    _load(e, 'packed_second', '%d0')
    e.ins('bset.l', '#5,%d0', 4)
    e.ins('move.b', '%d0,(%a0)')
    e.ins('move.b', _scalar('packed_first_byte') + ',3(%a0)', 6)
    e.ins('move.b', _scalar('current_force_byte') + ',4(%a0)', 6)
    e.ins('move.w', _scalar('packed_first') + ',' + _scalar('phase_argument'), 6)
    _write_origin(e)
    _write_reversed_long(e, 'selected_gold_budget', 8)
    _write_reversed_long(e, 'march_supply_budget', 12)
    e.ins('lea.l', '13(%a0),%a0', 4)
    _lea(e, 'scratch_roster', '%a1')
    scan, done = e.fresh('scan'), e.fresh('done')
    e.label(scan)
    e.ins('move.w', '(%a1)+,%d0')
    _branch(e, 'mi', done)
    e.ins('move.b', '%d0,(%a0)+')
    _branch(e, 'ra', scan, 'b')
    e.label(done)
    e.ins('clr.b', '(%a0)')
    e.ins('move.w', _table('scratch_roster') + ',' + _scalar('packed_head'), 6)


def _rebuild_departing_city_head(e, rules):
    _load(e, 'current_city', '%d0')
    _literal(e, 65535, 'roster_head')
    _call(e, 'build_roster', absolute=True)
    _call(e, 'choose_city_head', absolute=True)


def _finish_support_phase(e, rules):
    _literal(e, 65535, 'action_phase')


def _evaluate_packed_group_supply_phase(e, rules):
    low, done = e.fresh('low'), e.fresh('done')
    _lea(e, 'packed_groups', '%a0')
    e.ins('adda.w', _scalar('packed_group_offset') + ',%a0', 4)
    _call(e, 'price_packed_group')
    e.ins('move.b', '9(%a0),%d0', 4)
    e.ins('lsl.w', '#8,%d0')
    e.ins('move.b', '10(%a0),%d0', 4)
    e.ins('lsl.l', '#8,%d0')
    e.ins('move.b', '11(%a0),%d0', 4)
    e.ins('lsl.l', '#8,%d0')
    e.ins('move.b', '12(%a0),%d0', 4)
    e.ins('cmp.l', '%d2,%d0')
    _branch(e, rules['packed_supply_true_branch'], low)
    _literal(e, 6, 'action_phase')
    _branch(e, 'ra', done)
    e.label(low)
    _literal(e, 2, 'action_phase')
    e.label(done)


def _price_packed_group(e, rules):
    scan = e.fresh('scan')
    e.ins('move.b', '(%a0),%d0')
    e.ins('andi.w', '#15,%d0', 4)
    e.ins('subq.w', '#1,%d0')
    _lea(e, 'officer_troops', '%a1')
    e.ins('moveq', '#0,%d2')
    e.label(scan)
    e.ins('clr.w', '%d1')
    e.ins('move.b', '13(%a0,%d0.w),%d1', 4)
    e.ins('lsl.w', '#2,%d1')
    e.ins('add.l', '(%a1,%d1.w),%d2', 4)
    e.ins('addi.l', '#100,%d2', 6)
    e.ins('dbra', '%d0,' + scan, 4)
    e.ins('divu.w', '#10,%d2', 4)
    e.ins('move.w', '%d2,%d1')
    e.ins('lsl.w', '#1,%d2')
    e.ins('add.w', '%d1,%d2')
    e.ins('andi.l', '#65535,%d2', 6)


def _choose_group_destination_phase(e, rules):
    negative, done = e.fresh('negative'), e.fresh('done')
    _call(e, 'choose_ai_destination')
    e.ins('tst.w', _scalar('target_city'), 4)
    _branch(e, 'mi', negative)
    _literal(e, 4, 'action_phase')
    _branch(e, 'ra', done)
    e.label(negative)
    _literal(e, 3, 'action_phase')
    e.label(done)


def _evaluate_transport_supply_phase(e, rules):
    low, done = e.fresh('low'), e.fresh('done')
    _lea(e, 'officer_packet_data', '%a0')
    e.ins('adda.w', _scalar('packed_group_offset') + ',%a0', 4)
    e.ins('move.b', '5(%a0),%d0', 4)
    e.ins('lsl.w', '#8,%d0')
    e.ins('move.b', '6(%a0),%d0', 4)
    e.ins('lsl.l', '#8,%d0')
    e.ins('move.b', '7(%a0),%d0', 4)
    e.ins('lsl.l', '#8,%d0')
    e.ins('move.b', '8(%a0),%d0', 4)
    e.ins('cmpi.l', f"#{rules['transport_supply_threshold']},%d0", 6)
    _branch(e, rules['transport_supply_false_branch'], low)
    _call(e, 'reachable_transport_coordinate_carry')
    _branch(e, 'cs', low)
    _literal(e, 5, 'action_phase')
    _branch(e, 'ra', done)
    e.label(low)
    _literal(e, 4, 'action_phase')
    e.label(done)


def _reachable_transport_coordinate_carry(e, rules):
    scan, next_candidate, first_ok, second_ok = (e.fresh(s) for s in ('scan','next_candidate','first_ok','second_ok'))
    yes, no, done = e.fresh('yes'), e.fresh('no'), e.fresh('done')
    _load(e, 'transport_first', '%d0')
    _store(e, '%d0', 'path_start_first')
    _load(e, 'transport_second', '%d1')
    _store(e, '%d1', 'path_start_second')
    _load(e, 'transport_route_budget', '%d2')
    _lea(e, 'coordinate_candidates', '%a0')
    e.label(scan)
    e.ins('clr.w', '%d4')
    e.ins('move.b', '(%a0),%d4')
    _branch(e, 'mi', no)
    _store(e, '%d4', 'path_goal_first')
    e.ins('sub.b', '%d0,%d4')
    _branch(e, 'cc', first_ok)
    e.ins('neg.b', '%d4')
    e.label(first_ok)
    e.ins('cmp.b', '%d2,%d4')
    _branch(e, rules['transport_component_false_branch'], next_candidate)
    e.ins('clr.w', '%d5')
    e.ins('move.b', '1(%a0),%d5', 4)
    _store(e, '%d5', 'path_goal_second')
    e.ins('sub.b', '%d1,%d5')
    _branch(e, 'cc', second_ok)
    e.ins('neg.w', '%d5')
    e.label(second_ok)
    e.ins('add.b', '%d5,%d4')
    e.ins('cmp.b', '%d2,%d4')
    _branch(e, rules['transport_component_false_branch'], next_candidate)
    e.ins('movem.l', '%d0-%d2/%a0,-(%a7)', 4)
    _call(e, 'build_path', absolute=True, offset=4)
    e.ins('movem.l', '(%a7)+,%d0-%d2/%a0', 4)
    e.ins('cmp.w', _scalar('path_length') + ',%d2', 4)
    _branch(e, rules['transport_length_true_branch'], yes)
    e.label(next_candidate)
    e.ins('addq.l', '#2,%a0')
    _branch(e, 'ra', scan, 'b')
    e.label(yes)
    _carry(e, False)
    _branch(e, 'ra', done)
    e.label(no)
    _carry(e, True)
    e.label(done)


def _commit_staging_city_phase(e, rules):
    failed, done = e.fresh('failed'), e.fresh('done')
    _call(e, 'choose_nearest_staging_city')
    e.ins('tst.w', _scalar('target_city'), 4)
    _branch(e, 'mi', failed)
    e.ins('addq.w', '#1,' + _scalar('target_city'), 4)
    e.ins('clr.w', '%d0')
    e.ins('move.b', '3(%a0),%d0', 4)
    _store(e, '%d0', 'phase_argument')
    e.ins('clr.w', '%d0')
    e.ins('move.b', '13(%a0),%d0', 4)
    _store(e, '%d0', 'packed_head')
    _call(e, 'build_ai_movement_packet')
    _literal(e, 22, 'action_phase')
    _branch(e, 'ra', done)
    e.label(failed)
    _literal(e, 22, 'action_phase')
    e.label(done)


def _choose_nearest_staging_city(e, rules):
    scan, next_city, first_ok, second_ok = (e.fresh(s) for s in ('scan','next_city','first_ok','second_ok'))
    _lea(e, 'packed_groups', '%a0')
    e.ins('adda.w', _scalar('packed_group_offset') + ',%a0', 4)
    for slot, reg, start, packed in ((1,'%d0','path_start_first','packed_first'),
        (2,'%d1','path_start_second','packed_second')):
        e.ins('clr.w', reg)
        e.ins('move.b', f'{slot}(%a0),{reg}', 4)
        e.ins('lsl.w', '#4,' + reg)
        _store(e, reg, start)
        _store(e, reg, packed)
        e.ins('lsr.w', '#4,' + reg)
    e.ins('move.w', '#65535,%d2', 4)
    _literal(e, 65535, 'target_city')
    _lea(e, 'city_coordinates_zero_based', '%a1')
    _lea(e, 'city_owner_zero_based', '%a2')
    e.ins('move.w', '#39,%d3', 4)
    e.label(scan)
    e.ins('clr.w', '%d4')
    e.ins('move.b', '(%a2,%d3.w),%d4', 4)
    e.ins('cmp.b', _scalar('current_force_byte') + ',%d4', 4)
    _branch(e, 'ne', next_city)
    _call(e, 'city_roster_full_carry')
    _branch(e, 'cs', next_city)
    e.ins('move.w', '%d3,%d5')
    e.ins('lsl.w', '#2,%d5')
    e.ins('move.w', '2(%a1,%d5.w),%d6', 4)
    e.ins('lsr.w', '#4,%d6')
    e.ins('sub.w', '%d0,%d6')
    _branch(e, 'cc', first_ok)
    e.ins('neg.w', '%d6')
    e.label(first_ok)
    e.ins('move.w', '(%a1,%d5.w),%d7', 4)
    e.ins('lsr.w', '#4,%d7')
    e.ins('sub.w', '%d1,%d7')
    _branch(e, 'cc', second_ok)
    e.ins('neg.w', '%d7')
    e.label(second_ok)
    e.ins('add.w', '%d6,%d7')
    e.ins('cmp.w', '%d2,%d7')
    _branch(e, rules['staging_distance_false_branch'], next_city)
    e.ins('move.w', '%d7,%d2')
    _store(e, '%d3', 'target_city')
    e.label(next_city)
    e.ins('dbra', '%d3,' + scan, 4)


def _choose_destination_progress_phase(e, rules):
    different, done = e.fresh('different'), e.fresh('done')
    _load(e, 'path_goal_first', '%d0')
    e.ins('cmp.w', _scalar('path_start_first') + ',%d0', 4)
    _branch(e, rules['destination_axis_false_branch'], different)
    _load(e, 'path_goal_second', '%d0')
    e.ins('cmp.w', _scalar('path_start_second') + ',%d0', 4)
    _branch(e, rules['destination_axis_false_branch'], different)
    _literal(e, 21, 'action_phase')
    _branch(e, 'ra', done)
    e.label(different)
    _literal(e, 20, 'action_phase')
    e.label(done)


def _choose_terrain_exit_phase(e, rules):
    located, plain, done = e.fresh('located'), e.fresh('plain'), e.fresh('done')
    _load(e, 'transport_first', '%d0')
    e.ins('lsl.w', '#3,%d0')
    e.ins('add.w', _scalar('transport_first') + ',%d0', 4)
    e.ins('lsl.w', '#3,%d0')
    e.ins('add.w', _scalar('transport_second') + ',%d0', 4)
    _lea(e, 'terrain_types', '%a0')
    for displacement in (-72, -1, 1, 72):
        e.ins('move.b', f'{displacement}(%a0,%d0.w),%d1', 4)
        e.ins('cmpi.b', '#1,%d1', 4)
        _branch(e, rules['terrain_exit_true_branch'], located)
    e.label(plain)
    _literal(e, 13, 'action_phase')
    _branch(e, 'ra', done)
    e.label(located)
    _call(e, 'locate_packet_contact_city')
    _branch(e, 'cs', plain, 'b')
    _literal(e, 24, 'action_phase')
    e.label(done)


LOWERERS = {binding.name: globals()['_' + binding.name] for binding in ROUTES_BINDINGS}


MARCH_NATIVE_FUNCTIONS = (
    'commit_unowned_neighbor_march','shortest_unowned_neighbor',
    'price_two_officer_march','append_two_officer_march',
    'restore_departing_city_head','commit_support_march',
    'collect_support_officers','choose_support_roster','price_support_march',
    'append_support_march','rebuild_departing_city_head','finish_support_phase',
)


def _march_body(function):
    body = list(function.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and type(body[0].value.value) is str:
        body = body[1:]
    return body


def _march_source(source):
    """Read actual domain policy relations, then admit all helper AST bodies.

    Operators are normalized solely for topology checking. Their real relation
    and literals feed CMP/branch selection, with unchanged native operand order.
    No prior source body, assembly or encoded instruction is read or executed.
    """
    if type(source) is not str or len(source) > 300000:
        raise CompileError('bounded explicit march Python text required')
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError) as error:
        raise CompileError('invalid march business Python') from error
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    if any(name not in functions for name in MARCH_SOURCE_FUNCTIONS):
        raise CompileError('complete march query/policy/cost/commit helper family required')
    inverse = {ast.Lt:'cc', ast.LtE:'hi', ast.Gt:'ls', ast.GtE:'cs', ast.Eq:'ne', ast.NotEq:'eq'}
    policies = (
        ('march_officer_has_troops', 1, ast.GtE, 'troop_false_branch', 'march_troop_threshold', 32),
        ('two_officer_supply_is_affordable', 2, ast.GtE, 'pair_food_false_branch', None, 32),
        ('march_route_improves', 2, ast.Gt, 'route_false_branch', None, 16),
        ('support_city_has_roster', 1, ast.GtE, 'support_roster_false_branch', 'support_roster_threshold', 16),
        ('support_city_has_gold', 1, ast.GtE, 'support_gold_false_branch', 'support_gold_threshold', 32),
        ('support_supply_is_affordable', 2, ast.Gt, 'support_food_false_branch', None, 32),
        ('support_loyalty_allows_departure', 2, ast.GtE, 'loyalty_false_branch', None, 32),
        ('support_strength_requires_swap', 2, ast.Lt, 'strength_false_branch', None, 16),
    )
    normalized = deepcopy(tree)
    copied = {node.name: node for node in normalized.body if isinstance(node, ast.FunctionDef)}
    rules, relations = {}, {}
    for name, index, canonical, role, threshold, width in policies:
        try:
            test = _march_body(functions[name])[index].value
        except (AttributeError, IndexError) as error:
            raise CompileError('complete march comparison clause required') from error
        if (not isinstance(test, ast.Compare) or len(test.ops) != 1 or
                len(test.comparators) != 1 or type(test.ops[0]) not in inverse):
            raise CompileError('one declared unsigned march comparison required')
        rules[role] = inverse[type(test.ops[0])]
        relations[name] = dict(relation=type(test.ops[0]).__name__, width=width)
        _march_body(copied[name])[index].value.ops[0] = canonical()
        if threshold is not None:
            value = getattr(test.comparators[0], 'value', None)
            if type(value) is not int or not 0 <= value < 1 << width:
                raise CompileError('strict declared march threshold width required')
            rules[threshold] = value
    effects = {name: ast.dump(functions[name], include_attributes=False) for name in MARCH_SOURCE_FUNCTIONS}
    return ast.unparse(normalized), effects, dict(
        rules=rules, policies=relations, source_functions=MARCH_SOURCE_FUNCTIONS,
        unsigned_comparisons=True, helpers_inlined=True, extra_native_bytes=0,
        general_Python=False,
    )


TRANSPORT_NATIVE_FUNCTIONS = (
    'choose_neighbor_relation_phase','hostile_neighbor_exists_carry',
    'choose_unowned_neighbor_phase','unowned_neighbor_exists_carry',
    'choose_roster_troop_phase','count_roster_large_troops',
    'choose_random_neighbor_phase','choose_roster_troop_phase_five',
    'evaluate_neighbor_march_phase','sum_city_officer_troops',
    'choose_weaker_enemy_neighbor','evaluate_packed_group_supply_phase',
    'price_packed_group','choose_group_destination_phase',
    'evaluate_transport_supply_phase','reachable_transport_coordinate_carry',
    'commit_staging_city_phase','choose_nearest_staging_city',
    'choose_destination_progress_phase','choose_terrain_exit_phase',
)


def _transport_source(source):
    """Consume the complete live-query/policy/cost/commit family.

    Only a single declared unsigned relation or bounded threshold is variable.
    All other helper expressions, DATA order, calls and returns must match the
    admitted semantic topology. Actual relations, not normalized ones, select
    native branches; missing or changed compatibility effects are rejected.
    """
    if type(source) is not str or len(source) > 300000:
        raise CompileError('bounded explicit transport Python text required')
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError) as error:
        raise CompileError('invalid transport business Python') from error
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    if any(name not in functions for name in TRANSPORT_SOURCE_FUNCTIONS):
        raise CompileError('complete transport query/policy/cost/commit family required')
    inverse = {ast.Lt:'cc', ast.LtE:'hi', ast.Gt:'ls', ast.GtE:'cs', ast.Eq:'ne', ast.NotEq:'eq'}
    direct = {ast.Lt:'cs', ast.LtE:'ls', ast.Gt:'hi', ast.GtE:'cc', ast.Eq:'eq', ast.NotEq:'ne'}
    policies = (
        ('neighbor_owner_is_foreign', 2, ast.NotEq, 'foreign_owner_false_branch', None, 8, False),
        ('roster_troop_threshold_met', 2, ast.GtE, 'roster_count_false_branch', None, 16, False),
        ('roster_officer_has_large_troops', 1, ast.GtE, 'large_troop_false_branch', 'large_troop_threshold', 32, False),
        ('city_troop_word_qualifies', 1, ast.GtE, 'city_troop_false_branch', 'city_troop_threshold', 16, False),
        ('enemy_total_is_weaker', 2, ast.Lt, 'enemy_total_false_branch', None, 32, False),
        ('enemy_roster_is_eligible', 2, ast.LtE, 'enemy_roster_false_branch', None, 16, False),
        ('packed_supply_is_insufficient', 2, ast.Lt, 'packed_supply_true_branch', None, 32, True),
        ('transport_supply_allows_route', 1, ast.GtE, 'transport_supply_false_branch', 'transport_supply_threshold', 32, False),
        ('transport_component_within_budget', 2, ast.LtE, 'transport_component_false_branch', None, 8, False),
        ('transport_route_accepts_length', 2, ast.LtE, 'transport_length_true_branch', None, 16, True),
        ('staging_distance_improves', 2, ast.Lt, 'staging_distance_false_branch', None, 16, False),
        ('destination_axis_matches', 2, ast.Eq, 'destination_axis_false_branch', None, 16, False),
        ('terrain_kind_is_exit', 1, ast.Eq, 'terrain_exit_true_branch', None, 8, True),
    )
    normalized = deepcopy(tree)
    copied = {node.name: node for node in normalized.body if isinstance(node, ast.FunctionDef)}
    rules, relations = {}, {}
    for name, index, canonical, role, threshold, width, true_branch in policies:
        try:
            test = _march_body(functions[name])[index].value
        except (AttributeError, IndexError) as error:
            raise CompileError('complete transport comparison clause required') from error
        if (not isinstance(test, ast.Compare) or len(test.ops) != 1 or
                len(test.comparators) != 1 or type(test.ops[0]) not in inverse):
            raise CompileError('one declared unsigned transport comparison required')
        rules[role] = (direct if true_branch else inverse)[type(test.ops[0])]
        relations[name] = dict(relation=type(test.ops[0]).__name__, width=width)
        _march_body(copied[name])[index].value.ops[0] = canonical()
        if threshold is not None:
            value = getattr(test.comparators[0], 'value', None)
            maximum = 65535 if threshold == 'large_troop_threshold' else (1 << width)-1
            if type(value) is not int or not 0 <= value <= maximum:
                raise CompileError('strict declared transport threshold width required')
            rules[threshold] = value
    effects = {name: ast.dump(functions[name], include_attributes=False) for name in TRANSPORT_SOURCE_FUNCTIONS}
    return ast.unparse(normalized), effects, dict(
        rules=rules, policies=relations, source_functions=TRANSPORT_SOURCE_FUNCTIONS,
        unsigned_comparisons=True, helpers_inlined=True, extra_native_bytes=0,
        general_Python=False,
    )


def compile_routes(source):
    """Consume complete typed route flows, then select the fixed target ABI.

    All helpers are admitted before selecting native entries. Genuine policy
    operators determine branches; helpers are inlined in the fixed target ABI.
    No original program, old body or generated object is a generation input.
    """
    transport_normalized, transport_effects, transport_contract = _transport_source(source)
    normalized, effects, contract = _march_source(transport_normalized)
    complete = semantic_functions(normalized, DECLARATIONS, APPROVED)
    records = {binding.name: complete[binding.name] for binding in ROUTES_BINDINGS}
    for name in MARCH_NATIVE_FUNCTIONS:
        records[name]['rules'].update(contract['rules'])
        records[name]['effects'] = repr(effects)
    for name in TRANSPORT_NATIVE_FUNCTIONS:
        records[name]['rules'].update(transport_contract['rules'])
        records[name]['effects'] = repr(transport_effects)
    result = lower_declared(records, ROUTES_BINDINGS, LOWERERS)
    result['march_domain_contract'] = contract
    result['transport_domain_contract'] = transport_contract
    return result
