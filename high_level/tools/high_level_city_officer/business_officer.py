"""Officer actions/progress and live city-source queries, with width compatibility."""
from .domain import (GameState,Table,Cursor,Byte,Word,Long,u8,u16,u32,s8,low8,low16,
                     replace_byte,negative_byte,negative_word,divu_retained,descending_inclusive)


def scan_city_officers(state:GameState, city:Word, output:Cursor, count:Word)->Word:
    city=u16(city)
    count=u16(count)
    for officer in descending_inclusive(255):
        assignment=state.officer_assignments.byte(officer)
        if negative_byte(assignment):
            if assignment&127==city:
                output.append_word(officer)
                count=u16(count+1)
    return count


def mark_c300_list(state:GameState)->None:
    roster=state.action_roster.cursor()
    while True:
        officer=roster.next_word()
        if negative_word(officer):
            return None
        if state.officer_status.byte(officer)>=40:
            live=state.officer_status.byte(officer)
            state.officer_status.set_byte(officer,u8(live|128))


def replace_city_assignments(state:GameState, replacement:Word)->None:
    replacement=u16(replacement)
    replacement=u16(replacement+41)
    selected=u8(state.selected_city()|64)
    for officer in descending_inclusive(255):
        if state.officer_assignments.byte(officer)==selected:
            state.officer_assignments.set_byte(officer,low8(replacement))


def defense_progress(state:GameState, officer:Word, gain:Word)->None:
    officer=u16(officer)
    gain=u16(gain)
    index=u16(officer<<1)
    gain=u16(gain<<1)
    updated=u16(state.progress_be.word(index)+gain)
    if updated>999:
        updated=999
    state.progress_be.set_word(index,updated)
    updated=u16(state.progress_c.word(index)+gain)
    if updated>999:
        updated=999
    state.progress_c.set_word(index,updated)


def battle_progress_award(state:GameState, officer:Word, quantity:Long, progress:Table)->Word:
    officer=u16(officer)
    quantity=u32(quantity)
    divided=divu_retained(low16(quantity),100)
    index=u16(officer<<1)
    updated=u16(progress.word(index)+low16(divided))
    if updated>999:
        updated=999
    progress.set_word(index,updated)
    return updated


def replenish_b200_troops(state:GameState, retained_city:Word)->Word:
    retained_city=u16(retained_city)
    for officer in descending_inclusive(255):
        retained_city=u16(replace_byte(retained_city,state.officer_assignments.byte(officer)))
        if retained_city>40:
            continue
        if state.city_processed.byte(retained_city)!=0:
            continue
        retained_city=u16(officer<<1)
        capacity=state.capacities_b000.word(retained_city)
        divided=divu_retained(u32(capacity*15),100)
        updated=u16(state.troops_b200.word(retained_city)+low16(divided))
        if updated>capacity:
            updated=capacity
        state.troops_b200.set_word(retained_city,updated)
    return retained_city


def grow_original_long_field(state:GameState, target:Table)->Long:
    previous=target.long()
    divided=divu_retained(previous,100)
    updated=u32(previous+low16(divided))
    if updated>1000:
        updated=1000
    target.set_long(0,updated)
    return updated


def education_factor(state:GameState, teacher:Word, target:Word)->Word:
    teacher=u16(teacher)
    target=u16(target)
    index=0
    if target>=20:
        index=5
        if target>=40:
            index=10
            if target>=60:
                index=15
                if target>=80:
                    index=20
    if teacher>=20:
        index=u16(index+1)
        if teacher>=40:
            index=u16(index+1)
            if teacher>=60:
                index=u16(index+1)
                if teacher>=80:
                    index=u16(index+1)
    return u16(s8(state.education_factors.byte(index)))


def recover_unacted_officer_b200(state:GameState)->None:
    actor=low8(state.current_force())
    for officer in descending_inclusive(255):
        city=state.officer_assignments.byte(officer)
        if city>40:
            continue
        if state.city_action_gates.byte(city)!=0:
            continue
        if state.city_owners.byte(city)!=actor:
            continue
        if state.officer_actions.byte(officer)!=0:
            continue
        index=u16(officer<<1)
        capacity=state.capacities_b000.word(index)
        divided=divu_retained(u32(capacity*15),100)
        updated=u16(state.troops_b200.word(index)+low16(divided))
        if updated>state.capacities_b000.word(index):
            updated=state.capacities_b000.word(index)
        state.troops_b200.set_word(index,updated)


def add_progress_be(state:GameState, gain:Word)->None:
    gain=u16(gain)
    index=u16(state.selected_officer()<<1)
    previous=state.progress_be.word(index)
    state.progress_be.set_word(index,u16(previous+gain))
    if state.progress_be.word(index)>999:
        state.progress_be.set_word(index,999)


def split_progress(state:GameState, gain:Long)->Word:
    gain=u32(gain)
    index=u16(state.selected_officer()<<1)
    divided=divu_retained(low16(gain),10)
    amount=low16(divided)
    previous=state.progress_be.word(index)
    state.progress_be.set_word(index,u16(previous+amount))
    if state.progress_be.word(index)>999:
        state.progress_be.set_word(index,999)
    amount=u16(amount>>1)
    previous=state.progress_c.word(index)
    state.progress_c.set_word(index,u16(previous+amount))
    if state.progress_c.word(index)>999:
        state.progress_c.set_word(index,999)
    return amount


def add_progress_c000(state:GameState, officer:Word, gain:Word)->None:
    officer=u16(officer)
    gain=u16(gain)
    index=u16(officer<<1)
    previous=state.progress_c.word(index)
    state.progress_c.set_word(index,u16(previous+gain))
    if state.progress_c.word(index)>999:
        state.progress_c.set_word(index,999)


def owner_head_lookup(state:GameState, city:Word)->Word:
    city=u16(city)
    owner=state.city_owners.byte(city)
    index=u16(s8(owner)<<1)
    head=state.force_heads.word(index)
    state.set_scene(513)
    return head


def clear_city_orders(state:GameState)->None:
    city=state.selected_city()
    index=u16((u16(city<<1)+city)<<2)
    state.city_orders.set_word(index,65535)
    state.city_orders.set_word(index,65535,4)
    state.city_orders.set_word(index,65535,8)


def clear_monthly_actions(state:GameState)->None:
    actions=state.officer_actions.cursor()
    for officer in descending_inclusive(255):
        if actions.byte()==1:
            actions.set_byte(0,0)
        actions=actions.advance(1)
    gates=state.city_action_gates.cursor()
    for city in descending_inclusive(39):
        flags=gates.byte()
        gates.append_byte(u8(flags&253))


def terrain_cell_query(state: GameState, row: Word, column: Word) -> tuple[Byte, Byte]:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    frame = project_officer_arrival_fields(state, 0x142A2, row, column)
    return low8(frame.unit), low8(frame.count)


def queue_development_order(state:GameState)->None:
    city=state.current_city()
    index=u16((u16(city<<1)+state.current_city())<<2)
    record=state.city_orders.at(index)
    previous=record.word()
    if not negative_word(previous):
        state.officer_actions.set_byte(previous,0)
        record.set_word(0,65535)
        if previous==state.selected_officer():
            return None
    record.set_word(0,state.selected_officer())
    record.set_word(2,state.development_amount())
    officer=state.selected_officer()
    state.officer_actions.set_byte(officer,2)


def queue_welfare_order(state:GameState)->None:
    city=state.current_city()
    index=u16((u16(city<<1)+state.current_city())<<2)
    record=state.city_orders.at(index,4)
    previous=record.word()
    if not negative_word(previous):
        state.officer_actions.set_byte(previous,0)
        record.set_word(0,65535)
        if previous==state.selected_officer():
            return None
    record.set_word(0,state.selected_officer())
    record.set_word(2,state.development_amount())
    officer=state.selected_officer()
    state.officer_actions.set_byte(officer,3)

from .domain import project_officer_arrival_fields
