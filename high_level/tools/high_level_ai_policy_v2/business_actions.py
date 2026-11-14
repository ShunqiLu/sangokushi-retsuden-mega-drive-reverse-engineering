"""Live campaign action selection and packet/contact resource policy.

These rules retain original partial-width calculations and unusual ordering.
Named context values disclose the preserved portions of incoming operands;
they do not assert a natural selector domain or a complete CPU/dispatcher.
"""
from .domain import (GameState, Table, Word, Long, CarryOutcome, checked_state, uint, u8, u16,
                     u32, low8, low16, high16, replace_byte, replace_word,
                     negative_byte, negative_word, descending_inclusive,
                     divu_retained, ContactMaskContext, RankingContext,
                     CoordinateScratchContext, PackedCountContext,
                     CandidateSelectionContext, RosterStrengthContext)


def locate_packet_contact_city(state: GameState) -> CarryOutcome:
    state = checked_state(state)
    x = u16(state.ai_grid_x() << 4)
    left = u16(x - 8)
    right = u16(x + 24)
    y = u16(state.ai_grid_y() << 4)
    top = u16(y - 16)
    bottom = u16(y + 32)
    coordinates = state.contact_city_coordinates
    city = 65535
    for city in descending_inclusive(39):
        if left <= coordinates.word(0, 2):
            if right >= coordinates.word(0, 2):
                if top <= coordinates.word():
                    if bottom >= coordinates.word():
                        break
        coordinates = coordinates.advance(-4)
    else:
        city = 65535
    if state.following_city_owners.byte(city) == state.current_force_low():
        return state.carry_result(1)
    state.set_chosen_city(u16((city & 255) + 1))
    return state.carry_result(0)


def choose_city_assault_action(state: GameState) -> None:
    state = checked_state(state)
    measure_packet_ready_strength(state)
    strength, ready = measure_chosen_city_strength(state)
    if strength >= state.ai_strength():
        state.set_command(13)
    elif ready > state.ai_ready_count():
        state.set_command(13)
    else:
        state.set_command(12)
    return None


def measure_packet_ready_strength(state: GameState) -> tuple[Long, Word]:
    state = checked_state(state)
    packet = state.group_packets.at(state.ai_group_index())
    members = packet.byte() & 15
    strength = 0
    ready = 0
    for index in descending_inclusive(u16(members - 1)):
        officer = packet.byte(index, 13)
        offset = u16(officer << 2)
        strength = u32(strength + state.officer_strengths.long(offset))
        item = state.officer_strengths.long(offset)
        if item < 5000:
            continue
        offset = u16(officer << 1)
        troops = state.combat_troops.word(offset)
        if troops >= state.officer_capacities.word(offset):
            ready = u16(ready + 1)
    state.set_ai_strength(strength)
    state.set_ai_ready_count(ready)
    return strength, ready


def measure_chosen_city_strength(state: GameState) -> tuple[Long, Word]:
    state = checked_state(state)
    assignments = state.officer_assignments_end.cursor()
    city = state.chosen_city()
    strength = 0
    ready = 0
    for officer in descending_inclusive(255):
        if assignments.previous_byte() != low8(city):
            continue
        offset = u16(officer << 2)
        strength = u32(strength + state.officer_strengths.long(offset))
        item = state.officer_strengths.long(offset)
        if item >= 5000:
            ready = u16(ready + 1)
    return strength, ready


def choose_city_mask_action(state: GameState, mask_context: ContactMaskContext) -> None:
    state = checked_state(state)
    mask_context = state.checked_contact_mask(mask_context)
    owner = state.city_owners.byte(state.chosen_city())
    if not negative_byte(owner):
        mask = u32(mask_context.mask_high_word << 16 | state.force_masks.word(u16(owner << 1)))
        force_bit = u16(state.current_force() - 1) & 31
        if mask & (1 << force_bit):
            sample = state.sample_random()
            scaled = u16(low16(sample) << 2)
            scaled = high16(scaled)
            if scaled != 0:
                state.set_command(16)
                return None
    state.set_command(9)
    return None


def choose_processed_city_action(state: GameState) -> None:
    state = checked_state(state)
    if state.city_processed.byte(state.chosen_city()) != 0:
        state.set_command(10)
    else:
        state.set_command(7)
    return None


def choose_linked_city_action(state: GameState) -> None:
    state = checked_state(state)
    links = state.officer_city_links_end.cursor()
    city = state.chosen_city()
    found = False
    officer = 65535
    for officer in descending_inclusive(255):
        if links.previous_byte() == low8(city):
            found = True
            break
    if not found:
        state.nonreturning_loop('linked officer search exhausted')
    assignment = state.officer_assignments.byte(officer) & 63
    owner = state.city_owners.byte(assignment)
    if owner == state.current_force_low():
        state.set_command(11)
    else:
        state.set_command(13)
    return None


def choose_packet_resource_action(state: GameState) -> None:
    state = checked_state(state)
    outcome = packet_resource_shortfall(state)
    if outcome.carry == 0:
        state.set_command(12)
    state.set_command(13)
    return None


def packet_resource_shortfall(state: GameState) -> CarryOutcome:
    state = checked_state(state)
    packet = state.group_packets.at(state.ai_group_index())
    count = u8((packet.byte() & 15) - 1)
    strength = 0
    for index in descending_inclusive(count):
        officer = packet.byte(index, 13)
        strength = u32(strength + state.officer_strengths.long(u16(officer << 2)))
        offset = u16(officer << 1)
        capacity = state.officer_capacities.word(offset)
        if state.combat_troops.word(offset) < capacity:
            return state.carry_result(1)
    if strength < 10000:
        return state.carry_result(1)
    return state.carry_result(0)


def count_linked_force_officers(state: GameState) -> Word:
    state = checked_state(state)
    city = state.chosen_city()
    force = state.current_force()
    count = 0
    for officer in descending_inclusive(255):
        if state.officer_city_links.byte(officer) & 63 != low8(city):
            continue
        assignment = state.officer_assignments.byte(officer) & 63
        if state.city_owners.byte(assignment) == low8(force):
            count = u16(count + 1)
    return count


def build_limited_packet_roster(state: GameState, limit: Word) -> None:
    state = checked_state(state)
    limit = uint(limit, 16)
    packet = state.group_packets.at(state.ai_group_index())
    count = packet.byte() & 15
    candidates = state.action_candidates.cursor()
    for index in descending_inclusive(u16(count - 1)):
        candidates.append_word(packet.byte(index, 13))
    candidates.set_word(0, 65535)
    candidates.set_word(0, 65535, 2)
    if count > limit:
        rank_packet_roster(state, RankingContext(65535, candidates))
        partition_ranked_packet_roster(state, limit)
    output = state.candidate_roster.cursor()
    source = state.action_candidates.cursor()
    total = 0
    while True:
        member = source.next_word()
        if negative_word(member):
            break
        output.append_word(member | 16384)
        total = u16(total + 1)
    while True:
        member = source.next_word()
        output.append_word(member)
        if negative_word(member):
            break
        total = u16(total + 1)
    state.set_selected_count(total)
    return None


def rank_packet_roster(state: GameState, ranking: RankingContext) -> None:
    state = checked_state(state)
    ranking = state.checked_ranking(ranking)
    ranking.tail.set_word(0, 65535)
    strength_offset = ranking.strength_offset
    while True:
        member = state.action_candidates.word()
        if negative_word(member):
            return None
        offset = u16(member << 2)
        strength = state.officer_strengths.word(strength_offset, 2)
        if strength > 10000:
            strength = 10000
        offset >>= 1
        attribute = state.officer_attributes.word(offset)
        member = offset >> 1
        members = state.ranked_members.cursor()
        strengths = state.ranked_strengths.cursor()
        attributes = state.ranked_attributes.cursor()
        while True:
            if not negative_word(members.word()):
                if strength < strengths.word():
                    members = members.advance(2)
                    strengths = strengths.advance(2)
                    attributes = attributes.advance(2)
                    continue
                if attribute < attributes.word():
                    members = members.advance(2)
                    strengths = strengths.advance(2)
                    attributes = attributes.advance(2)
                    continue
            break
        while True:
            displaced = members.word()
            strength_offset = displaced
            members.append_word(member)
            if negative_word(member):
                break
            displaced_strength = strengths.word()
            strengths.append_word(strength)
            displaced_attribute = attributes.next_word()
            attributes.append_word(attribute)
            member = displaced
            strength = displaced_strength
            attribute = displaced_attribute


def partition_ranked_packet_roster(state: GameState, limit: Word) -> None:
    state = checked_state(state)
    limit = uint(limit, 16)
    output = state.action_candidates.cursor()
    source = state.ranked_members.cursor()
    for remaining in descending_inclusive(u16(limit - 1)):
        output.append_word(source.next_word())
    output.append_word(65535)
    while True:
        member = source.next_word()
        output.append_word(member)
        if negative_word(member):
            break
    return None


def choose_adjacent_group_action(state: GameState, scratch: CoordinateScratchContext) -> None:
    state = checked_state(state)
    scratch = state.checked_coordinate_scratch(scratch)
    collect_adjacent_hostile_groups(state, scratch)
    if negative_word(state.action_candidates.word()):
        state.set_command(16)
    else:
        state.set_command(14)
    return None


def collect_adjacent_hostile_groups(state: GameState, scratch: CoordinateScratchContext) -> None:
    state = checked_state(state)
    scratch = state.checked_coordinate_scratch(scratch)
    offset = state.ai_group_index()
    packet = state.group_packets.at(offset)
    coordinate = u32(scratch.coordinate_high_word << 16 | offset)
    y = packet.byte(0, 2)
    coordinate = replace_byte(coordinate, packet.byte(0, 1))
    right = u8(low8(coordinate) + 1)
    left = u8(low8(coordinate) - 1)
    below = u8(y + 1)
    above = u8(y - 1)
    offset = 0
    output = state.action_candidates.cursor()
    packet = state.group_packets
    while True:
        members = packet.byte() & 15
        if members == 0:
            break
        coordinate = u32(low16(coordinate) << 16 | high16(coordinate))
        coordinate = replace_byte(coordinate, packet.byte(0, 4))
        if low8(coordinate) != state.current_force_low():
            matched = False
            if packet.byte(0, 1) == left:
                if packet.byte(0, 2) == y:
                    matched = True
            if not matched and packet.byte(0, 1) == low8(coordinate):
                if packet.byte(0, 2) == above:
                    matched = True
                elif packet.byte(0, 2) == below:
                    matched = True
            if not matched and packet.byte(0, 1) == right:
                if packet.byte(0, 2) == y:
                    matched = True
            if matched:
                output.append_word(offset)
        packet = packet.advance(members + 13)
        offset = u16(offset + members + 13)
    output.set_word(0, 65535)
    return None


def choose_adjacent_strength_action(state: GameState, mask_context: ContactMaskContext) -> None:
    state = checked_state(state)
    mask_context = state.checked_contact_mask(mask_context)
    store_packet_strength(state)
    candidate, strength = select_largest_hostile_candidate(state, mask_context)
    if negative_word(candidate) or strength >= state.ai_strength():
        state.set_command(16)
    else:
        state.set_ai_budget(candidate)
        state.set_command(15)
    return None


def store_packet_strength(state: GameState) -> None:
    state = checked_state(state)
    packet = state.group_packets.at(state.ai_group_index())
    count = packet.byte() & 15
    strength = 0
    for index in descending_inclusive(u16(count - 1)):
        officer = packet.byte(index, 13)
        strength = u32(strength + state.officer_strengths.long(u16(officer << 2)))
    state.set_ai_strength(strength)
    return None


def select_largest_hostile_candidate(state: GameState, mask_context: ContactMaskContext) -> tuple[Word, Long]:
    state = checked_state(state)
    mask_context = state.checked_contact_mask(mask_context)
    candidates = state.action_candidates.cursor()
    mask = u32(mask_context.mask_high_word << 16 | state.force_masks.word(u16(state.current_force() << 1)))
    largest = 4294967295
    selected = 65535
    while True:
        candidate = candidates.next_word()
        if negative_word(candidate):
            break
        outcome, strength = measure_unmasked_candidate_strength(state, candidate, state.officer_strengths,
                                                                 mask)
        if outcome.carry != 0:
            continue
        if strength <= largest:
            continue
        largest = strength
        selected = candidate
    return selected, largest


def measure_unmasked_candidate_strength(state: GameState, candidate: Word, strengths: Table,
                                       mask: Long) -> tuple[CarryOutcome, Long | None]:
    state = checked_state(state)
    candidate = uint(candidate, 16)
    mask = uint(mask, 32)
    strengths = state.checked_table(strengths)
    packet = state.group_packets.at(candidate)
    owner = packet.byte(0, 4)
    if mask & (1 << (owner & 31)):
        return state.carry_result(1), None
    count = packet.byte() & 15
    strength = 0
    for index in descending_inclusive(u16(count - 1)):
        officer = packet.byte(index, 13)
        strength = u32(strength + strengths.long(u16(officer << 2)))
    return state.carry_result(0), strength


def queue_packet_stationary_command(state: GameState) -> None:
    state = checked_state(state)
    packet = state.group_packets.at(state.ai_group_index())
    queue = state.movement_queue.cursor(state.movement_queue_offset())
    queue.append_byte(0)
    queue.append_byte(packet.byte(0, 13))
    queue.append_byte(packet.byte(0, 3))
    queue.append_byte(144)
    queue.append_byte(50)
    queue.append_byte(0)
    queue.set_byte(0, 255)
    state.set_movement_queue_offset(u16(state.movement_queue_offset() + 6))
    state.set_command(65535)
    return None


def choose_reachable_city_action(state: GameState) -> None:
    state = checked_state(state)
    range_limit = packet_resource_range(state)
    collect_reachable_hostile_cities(state, low16(range_limit))
    if not negative_word(state.action_candidates.word()):
        strength, ready = measure_packet_ready_strength(state)
        if ready != 0:
            select_lightest_reachable_city(state, ready)
            if not negative_word(state.chosen_city()):
                state.set_command(17)
                return None
    state.set_command(18)
    return None


def packet_resource_range(state: GameState) -> Long:
    state = checked_state(state)
    packet = state.group_packets.at(state.ai_group_index())
    count = packet.byte() & 15
    strength = 0
    for index in descending_inclusive(u16(count - 1)):
        officer = packet.byte(index, 13)
        strength = u32(strength + state.officer_strengths.long(u16(officer << 2)))
        strength = u32(strength + 100)
    quotient = divu_retained(strength, 10)
    denominator = u16(low16(quotient) + u16(low16(quotient) << 1))
    food = packet.byte(0, 9)
    food = u32(food << 8 | packet.byte(0, 10))
    food = u32(food << 8 | packet.byte(0, 11))
    food = u32(food << 8 | packet.byte(0, 12))
    quotient = divu_retained(food, denominator)
    result = low16(quotient)
    if result == 0:
        return quotient
    result = u16(result - 1)
    if result > 2:
        result = 2
    return result * packet.byte(0, 3)


def collect_reachable_hostile_cities(state: GameState, range_limit: Word) -> None:
    state = checked_state(state)
    range_limit = uint(range_limit, 16)
    output = state.action_candidates.cursor()
    distances = state.candidate_distances.cursor()
    x = state.ai_grid_x()
    state.set_path_origin_x(x)
    y = state.ai_grid_y()
    state.set_path_origin_y(y)
    coordinates = state.contact_city_coordinates
    owners = state.city_owners_end.cursor()
    for city in descending_inclusive(39):
        if owners.previous_byte() == state.current_force_low():
            coordinates = coordinates.advance(-4)
            continue
        target_x = coordinates.word(0, 2) >> 4
        state.set_path_target_x(target_x)
        dx = u16(target_x - x)
        if target_x < x:
            dx = u16(-dx)
        if dx > range_limit:
            coordinates = coordinates.advance(-4)
            continue
        target_y = coordinates.word() >> 4
        state.set_path_target_y(target_y)
        dy = u16(target_y - y)
        if target_y < y:
            dy = u16(-dy)
        distance = u16(dx + dy)
        if distance <= range_limit:
            state.build_path_from_cells()
            if state.path_length() < range_limit:
                output.append_word(city)
                distances.append_word(state.path_length())
        coordinates = coordinates.advance(-4)
    output.set_word(0, 65535)
    return None


def select_lightest_reachable_city(state: GameState, own_ready_count: Word) -> None:
    state = checked_state(state)
    own_ready_count = uint(own_ready_count, 16)
    candidates = state.action_candidates.cursor()
    distances = state.candidate_distances_prefix.cursor()
    lightest = 4294967295
    shortest = 65535
    state.set_chosen_city(65535)
    while True:
        distances = distances.advance(2)
        index = candidates.next_word()
        if negative_word(index):
            break
        city, strength, ready = measure_indexed_city_strength(state, index)
        if ready > own_ready_count:
            continue
        if strength > lightest:
            continue
        if strength == lightest and distances.word() >= shortest:
            continue
        lightest = strength
        shortest = distances.word()
        state.set_chosen_city(city)
    return None


def measure_indexed_city_strength(state: GameState, city_index: Word) -> tuple[Word, Long, Word]:
    state = checked_state(state)
    city_index = uint(city_index, 16)
    city = u16(city_index + 1)
    assignments = state.officer_assignments_end.cursor()
    strength = 0
    ready = 0
    for officer in descending_inclusive(255):
        if assignments.previous_byte() == low8(city):
            item = state.officer_strengths.long(u16(officer << 2))
            strength = u32(strength + item)
            if item >= 5000:
                ready = u16(ready + 1)
    return city, strength, ready


def queue_packet_march_action(state: GameState) -> None:
    state = checked_state(state)
    packet = state.group_packets.at(state.ai_group_index())
    budget = packet.byte(0, 3)
    state.set_ai_budget(budget)
    state.set_ai_origin_x(u16(state.ai_grid_x() << 4))
    marker = u16(state.ai_grid_y() << 4)
    state.set_ai_origin_y(marker)
    marker = u16(replace_byte(marker, packet.byte(0, 13)))
    state.set_ai_packet_marker_word(marker)
    state.build_ai_movement_packet()
    state.set_command(22)
    return None


def choose_reachable_group_action(state: GameState) -> None:
    state = checked_state(state)
    packet, strength = store_packet_comparison_strength(state)
    mask_context = ContactMaskContext(high16(strength))
    fallback = collect_reachable_hostile_groups(state, packet.byte(0, 3), mask_context)
    if not negative_word(state.action_candidates.word()):
        lightest = select_lightest_group_candidate(state, fallback, PackedCountContext(0))
        if lightest <= state.ai_strength():
            state.set_command(19)
            return None
    state.set_command(4)
    return None


def store_packet_comparison_strength(state: GameState) -> tuple[Table, Long]:
    state = checked_state(state)
    packet = state.group_packets.at(state.ai_group_index())
    count = packet.byte() & 15
    strength = 0
    for index in descending_inclusive(u16(count - 1)):
        officer = packet.byte(index, 13)
        strength = u32(strength + state.officer_strengths.long(u16(officer << 2)))
    state.set_ai_strength(strength)
    return packet, strength


def collect_reachable_hostile_groups(state: GameState, range_limit: Word,
                                     mask_context: ContactMaskContext) -> CandidateSelectionContext:
    state = checked_state(state)
    range_limit = uint(range_limit, 16)
    mask_context = state.checked_contact_mask(mask_context)
    mask = u32(mask_context.mask_high_word << 16 | state.force_masks.word(u16(state.current_force() << 1)))
    output = state.action_candidates.cursor()
    x = state.ai_grid_x()
    state.set_path_origin_x(x)
    y = state.ai_grid_y()
    state.set_path_origin_y(y)
    offset = 0
    packet = state.group_packets
    while True:
        count = packet.byte() & 15
        if count == 0:
            break
        owner = packet.byte(0, 4)
        if owner != state.current_force():
            if mask & (1 << (owner & 31)) == 0:
                target_x = packet.byte(0, 1)
                state.set_path_target_x(target_x)
                dx = u8(target_x - low8(x))
                if target_x < low8(x):
                    dx = u16(-dx)
                if dx <= range_limit:
                    target_y = packet.byte(0, 2)
                    state.set_path_target_y(target_y)
                    dy = u16(target_y - y)
                    if target_y < y:
                        dy = u16(-dy)
                    if u16(dx + dy) <= range_limit:
                        state.build_path_from_cells()
                        if state.path_length() <= range_limit:
                            output.append_word(offset)
        packet = packet.advance(count + 13)
        offset = u16(offset + count + 13)
    output.set_word(0, 65535)
    return CandidateSelectionContext(x)


def select_lightest_group_candidate(state: GameState, fallback: CandidateSelectionContext,
                                     count_context: PackedCountContext) -> Long:
    state = checked_state(state)
    fallback = state.checked_candidate_selection(fallback)
    count_context = state.checked_packed_count(count_context)
    selected = fallback.fallback_offset
    lightest = 4294967295
    candidates = state.action_candidates.cursor()
    while True:
        candidate = candidates.next_word()
        if negative_word(candidate):
            break
        strength = measure_group_candidate_strength(state, candidate, state.officer_strengths, count_context)
        count_context = PackedCountContext(255)
        if strength < lightest:
            lightest = strength
            selected = candidate
    state.set_ai_selected_offset(selected)
    return lightest


def measure_group_candidate_strength(state: GameState, candidate: Word, strengths: Table,
                                      count_context: PackedCountContext) -> Long:
    state = checked_state(state)
    candidate = uint(candidate, 16)
    strengths = state.checked_table(strengths)
    count_context = state.checked_packed_count(count_context)
    packet = state.group_packets.at(candidate)
    count = u16(count_context.count_high_byte << 8 | (packet.byte() & 15))
    strength = 0
    for index in descending_inclusive(u16(count - 1)):
        officer = packet.byte(index, 13)
        strength = u32(strength + strengths.long(u16(officer << 2)))
    return strength


def purchase_packet_supplies(state: GameState) -> None:
    state = checked_state(state)
    packet, cash = load_packet_cash(state)
    cash = fill_packet_troop_deficits(state, packet, cash)
    cash = buy_packet_food(state, packet, cash)
    cash = buy_packet_equipment(state, packet, cash)
    packet.set_byte(0, low8(cash), 8)
    cash >>= 8
    packet.set_byte(0, low8(cash), 7)
    cash >>= 8
    packet.set_byte(0, low8(cash), 6)
    cash >>= 8
    packet.set_byte(0, low8(cash), 5)
    state.set_command(65535)
    return None


def load_packet_cash(state: GameState) -> tuple[Table, Long]:
    state = checked_state(state)
    packet = state.group_packets.at(state.ai_group_index())
    cash = packet.byte(0, 5)
    cash = u32(cash << 8 | packet.byte(0, 6))
    cash = u32(cash << 8 | packet.byte(0, 7))
    cash = u32(cash << 8 | packet.byte(0, 8))
    return packet, cash


def fill_packet_troop_deficits(state: GameState, packet: Table, cash: Long) -> Long:
    state = checked_state(state)
    cash = uint(cash, 32)
    packet = state.checked_table(packet)
    count = packet.byte() & 15
    for index in descending_inclusive(u16(count - 1)):
        officer = packet.byte(index, 13)
        offset = u16(officer << 1)
        difference = u16(state.officer_capacities.word(offset) - state.combat_troops.word(offset))
        if difference == 0:
            continue
        cost = difference * 50
        if cash < cost:
            cash = u32(cash - cost)
            cash = u32(cash + cost)
            break
        cash = u32(cash - cost)
        state.combat_troops.set_word(offset, u16(state.combat_troops.word(offset) + difference))
    return cash


def buy_packet_food(state: GameState, packet: Table, cash: Long) -> Long:
    state = checked_state(state)
    cash = uint(cash, 32)
    packet = state.checked_table(packet)
    count = state.force_troop_count(packet.cursor())
    coefficient = u32(count * 20)
    numerator = u32(cash * 8)
    quotient, remainder = state.divide_signed(numerator, 10)
    retained = divu_retained(quotient, low16(coefficient))
    amount = low16(retained)
    if amount == 0:
        return cash
    food = packet.byte(0, 9)
    food = u32(food << 8 | packet.byte(0, 10))
    food = u32(food << 8 | packet.byte(0, 11))
    food = u32(food << 8 | packet.byte(0, 12))
    food = u32(food + amount * low16(count))
    packet.set_byte(0, low8(food), 12)
    food >>= 8
    packet.set_byte(0, low8(food), 11)
    food >>= 8
    packet.set_byte(0, low8(food), 10)
    food >>= 8
    packet.set_byte(0, low8(food), 9)
    cash = u32(cash - amount * low16(coefficient))
    return cash


def buy_packet_equipment(state: GameState, packet: Table, cash: Long) -> Long:
    state = checked_state(state)
    cash = uint(cash, 32)
    packet = state.checked_table(packet)
    if cash < state.equipment_cost.long():
        return cash
    count = packet.byte() & 15
    for index in descending_inclusive(u16(count - 1)):
        officer = packet.byte(index, 13)
        attribute = state.officer_attributes.word(u16(officer << 1))
        if attribute >= 100:
            state.officer_attributes.set_byte(u16(u16(officer << 1) + officer), 4)
            cash = u32(cash - state.equipment_cost.long())
            if cash < state.equipment_cost.long():
                break
    return cash


def clear_packet_supply_command(state: GameState) -> None:
    state = checked_state(state)
    state.set_command(65535)
    return None


def choose_packet_readiness_action(state: GameState) -> None:
    state = checked_state(state)
    strength, ready = measure_packet_ready_strength(state)
    if ready != 0:
        state.set_command(8)
    else:
        state.set_command(4)
    return None


def load_active_packet_roster(state: GameState) -> None:
    state = checked_state(state)
    packet = state.table(state.active_packet())
    state.set_current_force(packet.byte(0, 4))
    count = packet.byte() & 15
    output = state.selected_roster.cursor()
    for index in descending_inclusive(u16(count - 1)):
        output.append_word(packet.byte(index, 13))
    output.set_word(0, 65535)
    return None


def choose_active_packet_contact_action(state: GameState) -> None:
    state = checked_state(state)
    outcome = active_packet_terrain_contact(state)
    if outcome.carry == 0:
        state.set_command(8)
    else:
        state.set_command(3)
    return None


def active_packet_terrain_contact(state: GameState) -> CarryOutcome:
    state = checked_state(state)
    packet = state.table(state.active_packet())
    x = packet.byte(0, 1)
    y = packet.byte(0, 2)
    index = u16(u16(u16(x << 3) + x) << 3)
    index = u16(index + y)
    near_water = state.terrain_sources.byte(index, -72) == 1
    if not near_water:
        near_water = state.terrain_sources.byte(index, -1) == 1
    if not near_water:
        near_water = state.terrain_sources.byte(index, 1) == 1
    if not near_water:
        near_water = state.terrain_sources.byte(index, 72) == 1
    if not near_water:
        return state.carry_result(0)
    left = u16(u16(x - 1) << 4)
    left = u16(left + 8)
    right = u16(u16(x + 1) << 4)
    right = u16(right + 8)
    top = u16(u16(y - 1) << 4)
    bottom = u16(u16(y + 2) << 4)
    coordinates = state.contact_city_coordinates
    city = 65535
    for city in descending_inclusive(39):
        cell_x = coordinates.word(0, 2)
        if cell_x >= left and cell_x <= right:
            cell_y = coordinates.word()
            if cell_y >= top and cell_y <= bottom:
                break
        coordinates = coordinates.advance(-4)
    else:
        city = 65535
    owner = state.following_city_owners.byte(city)
    if owner == packet.byte(0, 4):
        return state.carry_result(0)
    state.set_chosen_city(u16(city + 1))
    return state.carry_result(1)


def choose_active_city_assault_action(state: GameState, projection: RosterStrengthContext) -> None:
    state = checked_state(state)
    projection = state.checked_roster_strength(projection)
    projected, capable, last = project_selected_roster_strength(state, projection)
    enemy_strength, enemy_capable = measure_self_assigned_officers(state)
    if enemy_strength > projected or enemy_capable > capable:
        state.set_command(8)
    else:
        state.set_command(7)
    return None


def project_selected_roster_strength(state: GameState, projection: RosterStrengthContext) -> tuple[Long, Word, Long]:
    state = checked_state(state)
    projection = state.checked_roster_strength(projection)
    source = state.selected_roster.cursor()
    projected = 0
    capable = 0
    last = projection.last_strength
    while True:
        member = source.next_word()
        projected = replace_word(projected, member)
        if negative_word(member):
            break
        projected = replace_word(projected, u16(member << 2))
        last = state.officer_strengths.long(low16(projected))
        projected = u32(projected + last)
        if last >= 5000:
            capable = u16(capable + 1)
    return projected, capable, last


def measure_self_assigned_officers(state: GameState) -> tuple[Long, Word]:
    state = checked_state(state)
    ignored_city = state.chosen_city()
    assignments = state.officer_assignments_end.cursor()
    strength = 0
    capable = 0
    for officer in descending_inclusive(255):
        if assignments.previous_byte() == low8(officer):
            item = state.officer_strengths.long(u16(officer << 2))
            strength = u32(strength + item)
            if item >= 5000:
                capable = u16(capable + 1)
    return strength, capable


def choose_active_city_mask_action(state: GameState, mask_context: ContactMaskContext) -> None:
    state = checked_state(state)
    mask_context = state.checked_contact_mask(mask_context)
    mask = u32(mask_context.mask_high_word << 16 | state.force_masks.word(u16(state.current_force() << 1)))
    owner = state.city_owners.byte(state.chosen_city())
    if mask & (1 << (owner & 31)):
        sample = state.sample_random()
        scaled = high16(u16(low16(sample) << 2))
        if scaled != 0:
            state.set_command(8)
            return None
    state.set_command(4)
    return None


def choose_active_processed_city_action(state: GameState) -> None:
    state = checked_state(state)
    if state.city_processed.byte(state.chosen_city()) != 0:
        state.set_command(5)
    else:
        state.set_command(2)
    return None


def choose_active_linked_city_action(state: GameState) -> None:
    state = checked_state(state)
    force = linked_city_force(state)
    if force == state.current_force():
        state.set_command(6)
    else:
        state.set_command(8)
    return None


def linked_city_force(state: GameState) -> Word:
    state = checked_state(state)
    city = state.chosen_city()
    officer = 65535
    for officer in descending_inclusive(255):
        if state.officer_city_links.byte(officer) == city:
            break
    else:
        officer = 65535
    assignment = state.officer_assignments.byte(officer)
    return state.city_owners.byte(assignment)


def choose_selected_roster_resource_action(state: GameState) -> None:
    state = checked_state(state)
    strength = selected_roster_strength(state)
    if strength < 8000:
        state.set_command(8)
    elif selected_roster_troop_shortfall(state).carry != 0:
        state.set_command(8)
    else:
        state.set_command(7)
    return None


def selected_roster_strength(state: GameState) -> Long:
    state = checked_state(state)
    source = state.selected_roster.cursor()
    strength = 0
    while True:
        officer = source.next_word()
        if negative_word(officer):
            break
        strength = u32(strength + state.officer_strengths.long(u16(officer << 2)))
    return strength


def selected_roster_troop_shortfall(state: GameState) -> CarryOutcome:
    state = checked_state(state)
    source = state.selected_roster.cursor()
    while True:
        officer = source.next_word()
        if negative_word(officer):
            return state.carry_result(0)
        offset = u16(officer << 1)
        capacity = state.officer_capacities.word(offset)
        if capacity > state.combat_troops.word(offset):
            return state.carry_result(1)


def choose_active_adjacent_group_action(state: GameState, mask_context: ContactMaskContext) -> None:
    state = checked_state(state)
    mask_context = state.checked_contact_mask(mask_context)
    collect_active_adjacent_groups(state, mask_context)
    if negative_word(state.action_candidates.word()):
        state.set_command(11)
    else:
        state.set_command(9)
    return None


def collect_active_adjacent_groups(state: GameState, mask_context: ContactMaskContext) -> None:
    state = checked_state(state)
    mask_context = state.checked_contact_mask(mask_context)
    packet = state.table(state.active_packet())
    x = packet.byte(0, 1)
    y = packet.byte(0, 2)
    lower = u16(u16(x << 8) | y)
    below = u16(u16(x << 8) | u8(y + 1))
    above = u16(u16(x << 8) | u8(y - 1))
    right = u16(u16(u8(x + 1) << 8) | y)
    left = u16(u16(u8(x - 1) << 8) | y)
    mask = u32(mask_context.mask_high_word << 16 | state.force_masks.word(u16(state.current_force() << 1)))
    offset = 0
    output = state.action_candidates.cursor()
    packet = state.group_packets
    while True:
        count = packet.byte() & 15
        if count == 0:
            break
        owner = packet.byte(0, 4)
        if owner != state.current_force_low():
            if mask & (1 << (owner & 31)) == 0:
                coordinate = u16(packet.byte(0, 1) << 8 | packet.byte(0, 2))
                if coordinate == below or coordinate == above or coordinate == right or coordinate == left:
                    output.append_word(offset)
        packet = packet.advance(count + 13)
        offset = u16(offset + count + 13)
    output.set_word(0, 65535)
    return None


def choose_active_strength_action(state: GameState, fallback: CandidateSelectionContext) -> None:
    state = checked_state(state)
    fallback = state.checked_candidate_selection(fallback)
    own_strength = selected_roster_comparison_strength(state)
    lightest, selected = measure_lightest_active_candidate(state, fallback)
    if lightest > own_strength:
        state.set_command(11)
    else:
        state.set_ai_budget(selected)
        state.set_command(10)
    return None


def selected_roster_comparison_strength(state: GameState) -> Long:
    state = checked_state(state)
    source = state.selected_roster.cursor()
    strength = 0
    while True:
        officer = source.next_word()
        if negative_word(officer):
            break
        strength = u32(strength + state.officer_strengths.long(u16(officer << 2)))
    return strength


def measure_lightest_active_candidate(state: GameState, fallback: CandidateSelectionContext) -> tuple[Long, Word]:
    state = checked_state(state)
    fallback = state.checked_candidate_selection(fallback)
    candidates = state.action_candidates.cursor()
    lightest = 4294967295
    selected = fallback.fallback_offset
    while True:
        offset = candidates.next_word()
        if negative_word(offset):
            break
        packet = state.group_packets.at(offset)
        count = packet.byte() & 15
        strength = 0
        for index in descending_inclusive(u16(count - 1)):
            officer = packet.byte(index, 13)
            strength = u32(strength + state.officer_strengths.long(u16(officer << 2)))
        if strength < lightest:
            lightest = strength
            selected = offset
    return lightest, selected


def schedule_active_comparison_dialogue(state: GameState) -> None:
    state = checked_state(state)
    state.set_dialogue_selection(state.ai_budget())
    state.set_dialogue_auxiliary(0)
    state.set_dialogue_kind(20)
    state.set_menu_record(181)
    state.set_route(520)
    state.set_stage(4)
    state.set_dialogue_pending(1)
    state.set_command(65535)
    return None


def clear_active_contact_command(state: GameState) -> None:
    state = checked_state(state)
    state.set_command(65535)
    return None


def clear_active_idle_command(state: GameState) -> None:
    state = checked_state(state)
    state.set_command(65535)
    return None
