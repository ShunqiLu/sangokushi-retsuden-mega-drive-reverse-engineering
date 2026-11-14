"""Two-side postbattle roster disposition and live packed resource allocation."""
from .domain import (GameState,Table,Word,CarryOutcome,u8,u16,u32,low8,low16,
                     replace_byte,negative_byte,negative_word,descending_inclusive,divu_retained)
from .business_arrival import append_group_from_survivor_roster,apply_returning_officer_loyalty


def collect_city_attached_officers(state:GameState)->Word:
    output=state.candidate_roster.cursor()
    city=state.city()
    count=0
    for officer in descending_inclusive(255):
        if state.officer_assignments.byte(officer)==low8(city):
            output.append_word(officer)
            count=u16(count+1)
    output.set_word(0,65535)
    return count


def collect_unassigned_city_officers(state:GameState)->Word:
    output=state.candidate_roster.cursor()
    city=state.city()
    count=0
    for officer in descending_inclusive(255):
        if state.alternate_assignments.byte(officer)==low8(city):
            if not negative_byte(state.officer_assignments.byte(officer)):
                output.append_word(officer)
                count=u16(count+1)
    output.set_word(0,65535)
    return count


def rebuild_primary_after_battle(state:GameState)->None:
    collect_city_attached_officers(state)
    partition_city_survivors(state)
    incoming=collect_unassigned_city_officers(state)
    total=u16(incoming+state.remaining_count())
    if total>10:
        sort_returning_officer_status(state,u16(total-10))
    roster=state.survivor_roster.cursor()
    while True:
        officer=roster.word()
        if negative_word(officer):
            break
        roster.append_word(u16(officer|16384))
    if not negative_word(state.survivor_roster.word()):
        state.set_working_owner(state.secondary_owner_byte())
        outcome=owner_has_other_city_carry(state)
        if outcome.carry==0:
            state.set_resource_side(2)
            packet=append_group_from_survivor_roster(state)
            allocate_packed_group_resources(state,packet)
        else:
            city=u16(state.city()|128)
            roster=state.survivor_roster.cursor()
            while True:
                officer=roster.next_word()
                if negative_word(officer):
                    break
                officer=u16(officer&255)
                state.officer_assignments.set_byte(officer,low8(city))
    force=u16(state.primary_force()<<1)
    state.set_loyalty_source(state.force_heads.word(force))
    restore_returning_officer_assignments(state)


def sort_returning_officer_status(state:GameState,surplus:Word)->Word:
    surplus=u16(surplus)
    state.set_returning_count(u16(state.returning_count()+surplus))
    roster=state.remaining_roster.cursor()
    candidates=state.candidate_roster
    statuses=state.status_roster
    candidates.set_word(0,65535)
    retained_status=0
    while True:
        offset=0
        officer=roster.next_word()
        if negative_word(officer):
            break
        retained_status=u16(replace_byte(retained_status,state.status.byte(officer)))
        while not negative_word(candidates.word(offset)):
            if low8(retained_status)>statuses.byte(offset,1):
                break
            offset=u16(offset+2)
        while True:
            displaced=candidates.word(offset)
            candidates.set_word(offset,officer)
            if negative_word(officer):
                break
            displaced_status=statuses.word(offset)
            statuses.set_word(offset,retained_status)
            offset=u16(offset+2)
            officer=displaced
            retained_status=displaced_status
    returning=state.survivor_roster.cursor()
    while not negative_word(returning.next_word()):
        pass
    returning=returning.advance(-2)
    source=candidates.cursor()
    for member in descending_inclusive(u16(surplus-1)):
        returning.append_word(source.next_word())
    returning.set_word(0,65535)
    remaining=state.remaining_roster.cursor()
    count=0
    while True:
        officer=source.next_word()
        remaining.append_word(officer)
        if negative_word(officer):
            break
        count=u16(count+1)
    state.set_remaining_count(count)
    return count


def partition_city_survivors(state:GameState)->None:
    first=state.candidate_roster.word()
    city=u16(state.officer_assignments.byte(first)&63)
    owner=state.city_owners.byte(city)
    state.set_working_owner(owner)
    ruler=state.force_heads.word(u16(owner<<1))
    roster=state.candidate_roster.cursor()
    remaining=state.remaining_roster.cursor()
    returning=state.survivor_roster.cursor()
    return_count=0
    keep_count=0
    while True:
        officer=roster.next_word()
        if negative_word(officer):
            break
        if officer==ruler:
            outcome=owner_has_other_city_carry(state)
            if outcome.carry==0:
                returning.append_word(officer)
                return_count=u16(return_count+1)
            else:
                state.officer_assignments.set_byte(officer,255)
            continue
        strength_index=u16(officer<<2)
        if state.troop_strengths.long(strength_index)>500:
            if state.troop_strengths.long(strength_index)>1000:
                remaining.append_word(officer)
                keep_count=u16(keep_count+1)
                continue
            resource_index=u16(strength_index>>1)
            if state.officer_resources.word(resource_index)>30:
                remaining.append_word(officer)
                keep_count=u16(keep_count+1)
                continue
        sample=u16(state.sample_random()&3)
        if sample==0:
            returning.append_word(officer)
            return_count=u16(return_count+1)
        else:
            remaining.append_word(officer)
            keep_count=u16(keep_count+1)
    remaining.set_word(0,65535)
    returning.set_word(0,65535)
    state.set_returning_count(return_count)
    state.set_remaining_count(keep_count)


def owner_has_other_city_carry(state:GameState)->CarryOutcome:
    city=u16(state.city()-1)
    owner=state.working_owner()
    for candidate in descending_inclusive(39):
        if state.other_city_owners.byte(candidate)==owner:
            if candidate!=city:
                return state.carry_result(0)
    return state.carry_result(1)


def restore_returning_officer_assignments(state:GameState)->None:
    roster=state.remaining_roster.cursor()
    city=state.city()
    while True:
        officer=roster.next_word()
        if negative_word(officer):
            return None
        state.officer_assignments.set_byte(officer,low8(city))
        state.set_selected_officer(officer)
        apply_returning_officer_loyalty(state)


def allocate_packed_group_resources(state:GameState,packet:Table)->None:
    packet=state.checked_table(packet)
    members=u16(packet.byte()-1)
    total=0
    for member in descending_inclusive(members):
        officer=packet.byte(member,13)
        index=u16(officer<<2)
        total=u32(total+state.troop_strengths.long(index))
        total=u32(total+100)
    multiplied=u32(u32(total<<1)+total)
    gold_cost=u32(divu_retained(multiplied,5)&65535)
    rice_cost=gold_cost
    gold=state.city_ed84
    rice=state.city_ee24
    if state.side_flags()&2!=0:
        gold=state.city_gold
        rice=state.city_rice
    city=u16(state.city()<<2)
    available=gold.long(city)
    if available<gold_cost:
        gold_cost=available
    gold.set_long(city,u32(available-gold_cost))
    available=rice.long(city)
    if available<rice_cost:
        rice_cost=available
    rice.set_long(city,u32(available-rice_cost))
    packet.set_byte(8,low8(gold_cost))
    gold_cost=u32(gold_cost>>8)
    packet.set_byte(7,low8(gold_cost))
    gold_cost=u32(gold_cost>>8)
    packet.set_byte(6,low8(gold_cost))
    gold_cost=u32((gold_cost&4294901760)|u16(gold_cost<<8))
    packet.set_byte(5,low8(gold_cost))
    packet.set_byte(12,low8(rice_cost))
    rice_cost=u32(rice_cost>>8)
    packet.set_byte(11,low8(rice_cost))
    rice_cost=u32(rice_cost>>8)
    packet.set_byte(10,low8(rice_cost))
    rice_cost=u32((rice_cost&4294901760)|u16(low16(rice_cost)>>8))
    packet.set_byte(9,low8(rice_cost))


def rebuild_secondary_after_battle(state:GameState)->None:
    collect_unassigned_city_officers(state)
    partition_city_survivors(state)
    incoming=collect_city_attached_officers(state)
    total=u16(incoming+state.remaining_count())
    if total>10:
        sort_returning_officer_status(state,u16(total-10))
    roster=state.survivor_roster.cursor()
    while True:
        officer=roster.word()
        if negative_word(officer):
            break
        roster.append_word(u16(officer|16384))
    if not negative_word(state.survivor_roster.word()):
        state.set_working_owner(state.primary_owner_byte())
        outcome=owner_has_other_city_carry(state)
        if outcome.carry==0:
            state.set_resource_side(0)
            packet=append_group_from_survivor_roster(state)
            allocate_packed_group_resources(state,packet)
        else:
            city=u16(state.city()|128)
            roster=state.survivor_roster.cursor()
            while True:
                officer=roster.next_word()
                if negative_word(officer):
                    break
                officer=u16(officer&255)
                state.officer_assignments.set_byte(officer,low8(city))
    force=u16(state.secondary_force()<<1)
    state.set_loyalty_source(state.force_heads.word(force))
    restore_returning_officer_assignments(state)
