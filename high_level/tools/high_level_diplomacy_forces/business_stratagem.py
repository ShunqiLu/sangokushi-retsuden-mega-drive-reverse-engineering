"""Method-byte 61 assessment, penalties and live leader/assignment commits.

The localized command name is unknown. These policies preserve actual data
effects, including unusual cursor aliases, without pretending they are fixes.
"""
from .domain import (GameState,Word,uint,u8,u16,u32,s8,low8,low16,high16,negative_byte,
                     negative_word,divu_retained,descending_inclusive)
from .business_shared import choose_city_head,prepare_message


def replace_removed_force_head(state:GameState, force:Word)->None:
    force=uint(force,16)
    state.owner_change_count.set_byte(force,u8(state.owner_change_count.byte(force)+1))
    if state.owner_change_count.byte(force)>4:
        state.force_heads.set_word(u16(force<<1),65535)
        state.set_working_force(force)
        mark_removed_force_assignments(state)
        clear_removed_force_roster_alias(state)
        return None
    head=state.force_heads.word(u16(force<<1))
    old_city=state.officer_assignments.byte(head)
    state.officer_assignments.set_byte(head,255)
    old_city=u16(s8(old_city))
    state.set_head(65535)
    state.build_roster(old_city)
    choose_city_head(state,old_city)
    cities=state.force_city_roster.cursor()
    for city in descending_inclusive(39):
        if state.other_city_owners.byte(city)==low8(force):
            cities.append_byte(low8(city))
    cities.set_byte(0,255)
    best_score=0
    replacement=65535
    for officer in descending_inclusive(255):
        assignment=state.officer_assignments.byte(officer)
        if assignment==0 or negative_byte(assignment):
            continue
        assignment=u8(assignment-1)
        cities=state.force_city_roster.cursor()
        while True:
            city=cities.next_byte()
            if negative_byte(city) or city<assignment:
                break
            if city==assignment:
                offset=u16(officer<<1)
                first=state.progress_c.word(offset)
                score=first+state.progress_be.word(offset)
                if score>best_score:
                    best_score=score
                    replacement=officer
                break
    state.force_heads.set_word(u16(force<<1),replacement)
    city=u16(s8(state.officer_assignments.byte(replacement)))
    state.city_heads.set_word(u16(city<<1),replacement)
    state.officer_status.set_byte(replacement,0)


def mark_removed_force_assignments(state:GameState)->None:
    force=state.working_force()
    cities=state.force_city_roster.cursor()
    for city in descending_inclusive(39):
        if state.other_city_owners.byte(city)==low8(force):
            cities.append_byte(low8(city))
    cities.set_byte(0,255)
    assignments=state.officer_assignments.cursor()
    for officer in descending_inclusive(255):
        cities=state.force_city_roster.cursor()
        assignment=assignments.next_byte()
        if assignment!=0 and not negative_byte(assignment):
            assignment=u8(assignment-1)
            while True:
                city=cities.next_byte()
                if negative_byte(city) or city<assignment:
                    break
                if city==assignment:
                    assignments.set_byte(0,u8(assignments.byte()|128))
                    break
        assignments=assignments.advance(1)


def clear_removed_force_roster_alias(state:GameState)->None:
    cities=state.force_city_roster.cursor()
    while True:
        city=u16(cities.next_byte())
        if negative_byte(city):
            return None
        cities.set_byte(city,0)


def settle_method61_stratagem(state:GameState)->None:
    if assess_method61_side(state)==0:
        settle_method61_resource_attempt(state)
    else:
        settle_method61_direct_attempt(state)


def assess_method61_side(state:GameState)->Word:
    city=state.selected_city()
    state.set_head(state.city_heads.word(u16(city<<1)))
    count=state.build_roster(city)
    result=0
    if count!=1:
        sample=low16(state.sample_random())
        score=u16(state.intelligence.word(u16(state.selected_officer()<<1))+high16(u32(sample*200)))
        if score>180:
            result=1
    state.set_mode_side(result)
    return result


def settle_method61_resource_attempt(state:GameState)->None:
    sample=low16(state.sample_random())
    factor=u16(high16(u32(sample*21))+20)
    cost=u32(state.intelligence.word(u16(state.selected_officer()<<1))*factor)
    city=u16(state.current_city()<<2)
    available=state.city_gold.long(city)
    success=False
    if available>=cost:
        state.city_gold.set_long(city,u32(available-cost))
        factor=method61_scenario_factor(state)
        target=u16(state.target_officer()<<1)
        factor=u16(factor+state.base_attribute.word(target))
        factor=u16(factor+state.progress_c.word(target))
        factor=u16(factor+state.intelligence.word(target))
        quotient=divu_retained(cost,factor)
        if low16(quotient)>=100:
            success=True
        else:
            state.sample_random()
            comparison=high16(u32(state.seed_word()*100))
            if comparison<=low16(quotient):
                success=True
    if not success:
        penalize_actor_small_affinity(state)
        penalize_force_small_affinity(state)
        reward_actor_small_c_progress(state)
        state.set_message_code(67)
        state.set_stage(31)
        state.set_message_delay(120)
    else:
        remove_stratagem_target(state)
        reward_actor_large_c_progress(state)
        state.set_message_code(68)
        state.set_scene_queue(2)
        state.set_stage(40)
    force=state.current_force()
    if force==state.player_force_1() or force==state.player_force_2() or force==state.player_force_3():
        state.set_scene(520)
        state.set_display_target(state.target_officer())
        state.set_display_actor(state.selected_officer())
        prepare_message(state,65)
        state.set_message_delay(120)


def settle_method61_direct_attempt(state:GameState)->None:
    if choose_secondary_stratagem_target(state)!=0:
        penalize_actor_large_affinity(state)
        penalize_force_large_affinity(state)
        reward_actor_small_c_progress(state)
        state.set_stage(31)
        state.set_message_code(67)
    else:
        if method61_direct_probability(state)==0:
            state.set_message_delay(120)
            state.set_stage(31)
            state.set_message_code(67)
            try_remove_secondary_target(state)
            penalize_actor_small_affinity(state)
            penalize_force_small_affinity(state)
            reward_actor_small_c_progress(state)
        else:
            remove_stratagem_target(state)
            reward_actor_large_c_progress(state)
            state.set_message_code(68)
            state.set_stage(40)
            state.set_scene_queue(2)
    state.set_scene(520)
    if state.message_code()==206:
        state.set_display_target(state.secondary_target())
    else:
        state.set_display_target(state.target_officer())
    state.set_display_actor(state.selected_officer())
    prepare_message(state,66)
    state.set_message_delay(120)


def method61_scenario_factor(state:GameState)->Word:
    offset=u16(u16(u16(state.difficulty()<<1)+state.difficulty())<<4)
    owner=u16(s8(state.city_owners.byte(state.current_city())))
    head=state.force_heads.word(u16(owner<<1))
    if head!=state.selected_officer():
        offset=u16(offset+4)
        city=state.current_city()
        if state.city_heads.word(u16(city<<1))!=state.selected_officer():
            offset=u16(offset+4)
    sample=low16(state.sample_random())
    factor=high16(u32(sample*state.scenario_factors.word(offset)))
    return u16(factor+state.scenario_factors.word(offset,2))


def penalize_actor_small_affinity(state:GameState)->None:
    sample=low16(state.sample_random())
    factor=u16(high16(u32(sample*11))+10)
    officer=state.selected_officer()
    previous=state.affinity.byte(officer)
    if previous!=0:
        deduction=low16(divu_retained(u32(u16(s8(previous))*factor),100))
        live=state.affinity.byte(officer)
        state.affinity.set_byte(officer,u8(live-low8(deduction)))
        if live<low8(deduction):
            state.affinity.set_byte(officer,0)


def penalize_force_small_affinity(state:GameState)->None:
    sample=low16(state.sample_random())
    factor=u16(high16(u32(sample*6))+5)
    officer=state.force_heads.word(u16(state.current_force()<<1))
    previous=state.affinity.byte(officer)
    if previous!=0:
        deduction=low16(divu_retained(u32(u16(s8(previous))*factor),100))
        live=state.affinity.byte(officer)
        state.affinity.set_byte(officer,u8(live-low8(deduction)))
        if live<low8(deduction):
            state.affinity.set_byte(officer,0)


def reward_actor_small_c_progress(state:GameState)->None:
    sample=low16(state.sample_random())
    gain=u16(high16(u32(sample*3))+1)
    offset=u16(state.selected_officer()<<1)
    value=u16(state.progress_c.word(offset)+gain)
    if value>999:
        value=999
    state.progress_c.set_word(offset,value)


def remove_stratagem_target(state:GameState)->None:
    head=state.owner_head(state.selected_city())
    if head==state.target_officer():
        settle_removed_force_head(state)
    else:
        city=state.selected_city()
        if state.city_heads.word(u16(city<<1))==state.target_officer():
            remove_city_head_target(state)
    state.officer_assignments.set_byte(state.target_officer(),255)


def penalize_actor_large_affinity(state:GameState)->None:
    sample=low16(state.sample_random())
    factor=u16(high16(u32(sample*6))+5)
    officer=state.selected_officer()
    previous=state.affinity.byte(officer)
    if previous!=0:
        deduction=low16(divu_retained(u32(u16(s8(previous))*factor),100))
        live=state.affinity.byte(officer)
        state.affinity.set_byte(officer,u8(live-low8(deduction)))
        if live<low8(deduction):
            state.affinity.set_byte(officer,0)


def penalize_force_large_affinity(state:GameState)->None:
    sample=low16(state.sample_random())
    factor=high16(u32(sample*6))
    officer=state.force_heads.word(u16(state.current_force()<<1))
    previous=state.affinity.byte(officer)
    if previous!=0:
        deduction=low16(divu_retained(u32(u16(s8(previous))*factor),100))
        live=state.affinity.byte(officer)
        state.affinity.set_byte(officer,u8(live-low8(deduction)))
        if live<low8(deduction):
            state.affinity.set_byte(officer,0)


def settle_removed_force_head(state:GameState)->None:
    if state.mode_side()==0:
        force=u16(s8(state.city_owners.byte(state.selected_city())))
        replace_removed_force_head(state,force)
        return None
    trait=state.traits.byte(state.secondary_target())&15
    if trait>2:
        city=state.selected_city()
        force=u16(s8(state.city_owners.byte(city)))
        state.force_heads.set_word(u16(force<<1),state.secondary_target())
        state.city_heads.set_word(u16(city<<1),state.secondary_target())
        force=u16(force<<1)>>1
        alias=state.city_heads
        alias.set_byte(force,u8(alias.byte(force)+1))
        if alias.word(force)==4:
            state.force_heads.set_word(u16(force<<1),65535)
            state.set_working_force(force)
            mark_removed_force_assignments(state)
            return None
        else:
            return None
    else:
        state.sample_random()
        comparison=high16(u32(state.seed_word()*100))
        if trait==0:
            remove=comparison<=70
        else:
            remove=comparison<=30
        if remove:
            state.officer_assignments.set_byte(state.secondary_target(),255)
        else:
            reassign_or_mark_target(state)
    force=u16(s8(state.city_owners.byte(state.selected_city())))
    replace_removed_force_head(state,force)


def remove_city_head_target(state:GameState)->None:
    officer=state.target_officer()
    city=state.officer_assignments.byte(officer)
    state.officer_assignments.set_byte(officer,255)
    city=u16(s8(city))
    state.set_head(65535)
    state.build_roster(city)
    choose_city_head(state,city)


def reassign_or_mark_target(state:GameState)->None:
    city=u16(s8(state.officer_assignments.byte(state.selected_officer())))
    state.set_head(state.head_alias.word(u16(city<<1)))
    count=state.build_roster(city)
    mark=True
    if count<10:
        state.sample_random()
        if high16(u32(state.seed_word()*100))<=30:
            state.officer_assignments.set_byte(state.secondary_target(),state.current_city_high())
            mark=False
    if mark:
        officer=state.secondary_target()
        state.officer_assignments.set_byte(officer,u8(state.officer_assignments.byte(officer)|128))


def try_remove_secondary_target(state:GameState)->None:
    trait=state.traits.byte(state.secondary_target())&7
    if trait>=3:
        return None
    sample=low16(state.sample_random())
    if high16(u32(sample*100))>50:
        remove_secondary_city_head(state)
        state.set_message_code(206)


def remove_secondary_city_head(state:GameState)->None:
    officer=state.secondary_target()
    city=state.officer_assignments.byte(officer)
    state.officer_assignments.set_byte(officer,255)
    city=u16(city&63)
    if state.city_heads.word(u16(city<<1))==officer:
        city=state.selected_city()
        state.set_head(65535)
        state.build_roster(city)
        choose_city_head(state,city)


def reward_actor_large_c_progress(state:GameState)->None:
    state.sample_random()
    gain=u16(high16(u32(state.seed_word()*10))+10)
    offset=u16(state.selected_officer()<<1)
    value=u16(state.progress_c.word(offset)+gain)
    if value>999:
        value=999
    state.progress_c.set_word(offset,value)


def choose_secondary_stratagem_target(state:GameState)->Word:
    owner=u16(s8(state.city_owners.byte(state.selected_city())))
    state.set_protected_head(state.force_heads.word(u16(owner<<1)))
    roster=state.candidate_roster.cursor()
    candidate=65535
    status=255
    while True:
        officer=roster.next_word()
        if negative_word(officer):
            break
        if officer==state.target_officer() or officer==state.protected_head():
            continue
        if status>state.officer_status.byte(officer):
            status=state.officer_status.byte(officer)
            candidate=officer
    if negative_word(candidate):
        return 1
    threshold=u16(status+30)
    sample=low16(state.sample_random())
    if high16(u32(sample*100))>threshold:
        state.set_secondary_target(candidate)
        return 0
    return 1


def method61_direct_probability(state:GameState)->Word:
    source=u16(state.secondary_target()<<1)
    numerator=state.base_attribute.word(source)
    numerator=u16(numerator+state.progress_c.word(source))
    numerator=u16(numerator+state.intelligence.word(source))
    denominator=method61_direct_factor(state)
    target=u16(state.target_officer()<<1)
    denominator=u16(denominator+state.base_attribute.word(target))
    denominator=u16(denominator+state.progress_c.word(target))
    denominator=u16(denominator+state.intelligence.word(target))
    quotient=divu_retained(u32(numerator*100),denominator)
    state.sample_random()
    if high16(u32(state.seed_word()*100))<=low16(quotient):
        return 1
    return 0


def method61_direct_factor(state:GameState)->Word:
    offset=u16(u16(u16(state.difficulty()<<1)+state.difficulty())<<3)
    owner=u16(s8(state.city_owners.byte(state.selected_city())))
    head=state.force_heads.word(u16(owner<<1))
    if head!=state.target_officer():
        offset=u16(offset+4)
        city=state.selected_city()
        if state.city_heads.word(u16(city<<1))!=state.target_officer():
            offset=u16(offset+4)
    sample=low16(state.sample_random())
    factor=high16(u32(sample*state.direct_factors.word(offset)))
    return u16(factor+state.direct_factors.word(offset,2))
