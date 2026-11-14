"""Joining decisions and their live, fixed-width compatibility state changes.

The three-word trait bands are conditional source reads, not a natural-domain
clamp.  A failed bribe has already debited the requested resources.  Progress
and affinity changes deliberately read their destination again when required.
"""
from .domain import (
    GameState, Word, Long, uint, u8, u16, u32, s16, low8, low16, high16,
    replace_byte, swap_words, divu_retained, negative_word,
)
from .business_shared import choose_city_head, prepare_message


def settle_personnel_joining(state: GameState) -> None:
    if state.method() == 74:
        settle_bribe_joining(state)
    else:
        settle_persuasion_joining(state)


def settle_bribe_joining(state: GameState) -> None:
    if state.response() == 119:
        state.set_route(520)
        state.set_step(32)
        prepare_message(state, 85)
        state.set_message_gate(1)
        return None
    city_index = u16(state.current_city() << 2)
    amount = state.request_gold()
    previous = state.city_gold.long(city_index)
    state.city_gold.set_long(city_index, u32(previous - amount))
    amount = state.request_rice()
    previous = state.city_rice.long(city_index)
    state.city_rice.set_long(city_index, u32(previous - amount))
    city = state.selected_city()
    owner = u16(state.city_owners.byte(city))
    head = state.force_leaders.word(u16(owner << 1))
    if head == state.selected_officer():
        accepted = False
    else:
        offered = u32(state.request_gold() + state.request_rice())
        city = state.current_city()
        owner = u16(replace_byte(city, state.city_owners.byte(city)))
        head = state.force_leaders.word(u16(owner << 1))
        affinity = u16(state.officer_affinity.byte(head))
        lower = u32(low16(offered) * affinity)
        upper = u32(high16(offered) * affinity)
        offered_score = u32(swap_words(upper) + lower)
        actor = state.selected_officer()
        status = u16(state.officer_status.byte(actor))
        required = u32(status * status)
        affinity = u16(state.officer_affinity.byte(actor))
        required = u32(low16(required) * affinity)
        factor = bribe_acceptance_factor(state)
        lower = u32(low16(required) * factor)
        upper = u32(high16(required) * factor)
        required_score = u32(swap_words(upper) + lower)
        accepted = offered_score >= required_score
    if not accepted:
        penalize_force_head_affinity(state)
        reward_force_head_small_progress(state)
        state.set_route(520)
        state.set_step(32)
        state.set_message_actor(state.selected_officer())
        prepare_message(state, 91)
        return None
    reward_force_head_large_progress(state)
    transfer_joining_officer(state, state.selected_officer())
    state.set_route(520)
    state.set_step(40)
    state.set_message(90)
    state.set_message_target(state.selected_officer())
    saved_target = state.target_officer()
    state.set_target_officer(state.force_leaders.word(u16(state.current_force() << 1)))
    state.apply_returning_officer_loyalty()
    state.set_target_officer(saved_target)
    state.set_scene_queue(14)
    state.set_ui_first(0)
    state.set_ui_second(0)
    state.set_joining_refresh(0)


def bribe_acceptance_factor(state: GameState) -> Word:
    state.sample_random()
    actor = state.selected_officer()
    status = state.officer_status.byte(actor)
    band = u16(0)
    if status > 30:
        band = u16(band + 1)
        if status > 50:
            band = u16(band + 1)
            if status > 70:
                band = u16(band + 1)
                if status > 80:
                    band = u16(band + 1)
                    if status > 90:
                        band = u16(band + 1)
    index = u16(band + u16(band << 2))
    trait = u16(state.officer_traits.byte(actor) & 7)
    index = u16(u16(trait + index) << 1)
    weight = u16(state.bribe_factors.byte(index))
    weighted = u32(weight * state.seed_word())
    bias = u16(state.bribe_factors.byte(index, 1))
    return u16(high16(weighted) + bias)


def penalize_force_head_affinity(state: GameState) -> None:
    sample = low16(state.sample_random())
    scale = high16(u32(sample * 4))
    head = state.force_leaders.word(u16(state.current_force() << 1))
    affinity = u16(state.officer_affinity.byte(head))
    penalty = divu_retained(u32(affinity * scale), 100)
    previous = state.officer_affinity.byte(head)
    state.officer_affinity.set_byte(head, u8(previous - low8(penalty)))


def reward_force_head_small_progress(state: GameState) -> None:
    state.sample_random()
    seed = u32(state.seed_word())
    gain = u16(high16(u32(seed * 3)) + 1)
    head = state.force_leaders.word(u16(state.current_force() << 1))
    index = u16(head << 1)
    previous = state.progress_be.word(index)
    total = previous + gain
    state.progress_be.set_word(index, u16(total))
    if total > 65535:
        state.progress_be.set_word(index, 65535)


def reward_force_head_large_progress(state: GameState) -> None:
    sample = low16(state.sample_random())
    gain = u16(high16(u32(sample * 5)) + 1)
    head = state.force_leaders.word(u16(state.current_force() << 1))
    index = u16(head << 1)
    previous = state.progress_be.word(index)
    total = previous + gain
    state.progress_be.set_word(index, u16(total))
    if total > 65535:
        state.progress_be.set_word(index, 65535)


def transfer_joining_officer(state: GameState, officer: Word) -> None:
    officer = uint(officer, 16)
    index = u16(state.selected_city() << 1)
    index = u16(index + state.selected_city())
    index = u16(index << 2)
    if officer == state.city_orders.word(index):
        state.city_orders.set_word(index, 65535)
    elif officer == state.city_orders.word(index, 4):
        state.city_orders.set_word(index, 65535, 4)
    elif officer == state.city_orders.word(index, 8):
        state.city_orders.set_word(index, 65535, 8)
    head = state.city_heads.word(u16(state.selected_city() << 1))
    if head != officer:
        state.officer_assignments.set_byte(officer, state.city_tail())
        return None
    state.set_roster_exclusion(officer)
    count = state.build_roster(state.selected_city())
    if count != 1:
        roster = state.candidate_roster.cursor()
        attribute = u16(0)
        total = u16(0)
        while True:
            member = roster.next_word()
            if negative_word(member):
                break
            attribute = u16(replace_byte(attribute, state.officer_status.byte(member)))
            total = u16(total + attribute)
        average = divu_retained(u32(s16(total)), count)
        if low16(average) > 35:
            state.officer_assignments.set_byte(officer, state.city_tail())
            city = state.selected_city()
            state.set_roster_exclusion(65535)
            state.build_roster(city)
            choose_city_head(state, city)
            return None
    city = state.selected_city()
    old_owner = u16(state.city_owners.byte(city))
    state.city_owners.set_byte(city, state.current_force_tail())
    state.replace_city_assignments(old_owner)
    state.mark_c300_list()
    state.clear_city_orders()
    state.clear_selected_links()


def settle_persuasion_joining(state: GameState) -> None:
    if state.response() == 121:
        state.set_route(520)
        state.set_step(32)
        prepare_message(state, 85)
        state.set_message_gate(1)
        return None
    state.officer_actions.set_byte(state.selected_officer(), 1)
    city = state.selected_city()
    owner = u16(state.city_owners.byte(city))
    head = state.force_leaders.word(u16(owner << 1))
    if head == state.target_officer():
        accepted = False
    else:
        offered_score, required_score = persuasion_scores(state)
        accepted = offered_score >= required_score
    if not accepted:
        reward_actor_small_progress(state)
        penalize_actor_affinity(state)
        penalize_force_head_affinity(state)
        force = state.current_force()
        if force != state.player_force_1():
            if force != state.player_force_2():
                if force != state.player_force_3():
                    return None
        state.set_route(520)
        state.set_step(32)
        state.set_message_actor(state.selected_officer())
        prepare_message(state, 83)
        return None
    reward_actor_large_progress(state)
    transfer_joining_officer(state, state.target_officer())
    force = state.current_force()
    if force != state.player_force_1():
        if force != state.player_force_2():
            if force != state.player_force_3():
                return None
    state.set_route(520)
    state.set_step(40)
    state.set_message(92)
    state.set_message_target(state.target_officer())
    state.set_message_actor(state.selected_officer())
    state.set_scene_queue(12)
    state.set_ui_first(0)
    state.set_ui_second(0)
    state.set_selected_officer(state.target_officer())
    state.set_joining_refresh(0)
    state.set_target_officer(state.force_leaders.word(u16(state.current_force() << 1)))
    state.apply_returning_officer_loyalty()


def persuasion_scores(state: GameState) -> tuple[Long, Long]:
    target = state.target_officer()
    status = u16(state.officer_status.byte(target))
    offered = u16(100 - status)
    head = state.force_leaders.word(u16(state.current_force() << 1))
    affinity = u16(state.officer_affinity.byte(head))
    offered = u32(low16(offered) * affinity)
    actor = state.selected_officer()
    affinity = u16(state.officer_affinity.byte(actor))
    offered = u32(low16(offered) * affinity)
    ability = state.officer_ability.word(u16(actor << 1))
    lower = u32(low16(offered) * ability)
    upper = u32(high16(offered) * ability)
    offered = u32(swap_words(upper) + lower)
    factor = persuasion_factor(state)
    lower = u32(low16(offered) * factor)
    upper = u32(high16(offered) * factor)
    offered_score = u32(swap_words(upper) + lower)
    target = state.target_officer()
    affinity = u16(state.officer_affinity.byte(target))
    city = state.selected_city()
    owner = u16(state.city_owners.byte(city))
    head = state.force_leaders.word(u16(owner << 1))
    head_affinity = u16(state.officer_affinity.byte(head))
    required = u32(affinity * head_affinity)
    ability = state.officer_ability.word(u16(target << 1))
    required = u32(low16(required) * ability)
    index = u16(state.difficulty() << 1)
    weight = state.persuasion_weights.word(index)
    lower = u32(low16(required) * weight)
    upper = u32(high16(required) * weight)
    required_score = u32(lower + swap_words(upper))
    return offered_score, required_score


def persuasion_factor(state: GameState) -> Word:
    state.sample_random()
    actor = state.selected_officer()
    actor_trait = u16(state.officer_traits.byte(actor) & 7)
    actor_deficit = u16(4 - actor_trait)
    index = u16(u16(actor_deficit << 2) + actor_deficit)
    target = state.target_officer()
    target_trait = u16(state.officer_traits.byte(target) & 7)
    target_deficit = u16(replace_byte(4, u8(4 - target_trait)))
    index = u16(u16(index + target_deficit) << 1)
    weight = u16(state.persuasion_factors.byte(index))
    weighted = u32(weight * state.seed_word())
    bias = u16(state.persuasion_factors.byte(index, 1))
    return u16(high16(weighted) + bias)


def reward_actor_small_progress(state: GameState) -> None:
    state.sample_random()
    seed = u32(state.seed_word())
    gain = u16(high16(u32(seed * 3)) + 1)
    index = u16(state.selected_officer() << 1)
    previous = state.progress_be.word(index)
    total = previous + gain
    state.progress_be.set_word(index, u16(total))
    if total > 65535:
        state.progress_be.set_word(index, 65535)


def reward_actor_large_progress(state: GameState) -> None:
    sample = low16(state.sample_random())
    gain = u16(high16(u32(sample * 6)) + 5)
    index = u16(state.selected_officer() << 1)
    previous = state.progress_be.word(index)
    total = previous + gain
    state.progress_be.set_word(index, u16(total))
    if total > 65535:
        state.progress_be.set_word(index, 65535)


def penalize_actor_affinity(state: GameState) -> None:
    sample = low16(state.sample_random())
    scale = high16(u32(sample * 11))
    actor = state.selected_officer()
    affinity = u16(state.officer_affinity.byte(actor))
    penalty = divu_retained(u32(affinity * scale), 100)
    previous = state.officer_affinity.byte(actor)
    amount = low8(penalty)
    state.officer_affinity.set_byte(actor, u8(previous - amount))
    if previous < amount:
        state.officer_affinity.set_byte(actor, 0)
