"""City-head choice and message-state preparation, with live data order."""
from .domain import GameState,Word,Table,HeadMatch,uint,u16,u32,s16,low8,negative_word


def choose_city_head(state:GameState, city:Word)->Word:
    city=uint(city,16)
    roster=state.candidate_roster.cursor()
    head=roster.next_word()
    if negative_word(head):
        state.city_owners.set_byte(city,255)
        orders=u16(u16(u16(city<<1)+city)<<2)
        state.city_orders.set_word(orders,65535)
        state.city_orders.set_word(orders,65535,4)
        state.city_orders.set_word(orders,65535,8)
    else:
        outcome=roster_contains_force_head_carry(state,city,head)
        head=outcome.head
        if outcome.carry==0:
            head=u16(head&255)
            highest=state.officer_status.byte(head)
            while True:
                candidate=roster.next_word()
                if negative_word(candidate):
                    break
                candidate=u16(candidate&255)
                status=state.officer_status.byte(candidate)
                if status>highest:
                    head=candidate
                    highest=status
    state.city_heads.set_word(u16(city<<1),head)
    return head


def roster_contains_force_head_carry(state:GameState, city:Word, head:Word)->HeadMatch:
    city=uint(city,16)
    head=uint(head,16)
    owner=u16(state.city_owners.byte(city))
    force_head=state.force_heads.word(u16(owner<<1))
    roster=state.candidate_roster.cursor()
    while not negative_word(roster.word()):
        if roster.next_word()==force_head:
            outcome=state.carry_result(1)
            return HeadMatch(force_head,outcome.carry,outcome.conditional_sr)
    outcome=state.carry_result(0)
    return HeadMatch(head,outcome.carry,outcome.conditional_sr)


def prepare_message(state:GameState, message:Word)->None:
    message=uint(message,16)
    if negative_word(message):
        return None
    state.set_message_flag(0)
    pointer=resolve_message_pointer(state,message)
    state.set_message_pointer(pointer.base)
    state.set_message_scene(state.scene())
    state.set_message_stage(state.stage())
    state.set_message_kind(0)
    state.set_message_parameter(0)
    state.set_message_mode(40)
    select_message_layout(state)
    state.set_message_pending(1)


def select_message_layout(state:GameState)->None:
    offset=u16(state.message_layout_index()<<2)
    state.set_scene(state.message_layout.word(offset))
    state.set_stage(state.message_layout.word(offset,2))


def resolve_message_pointer(state:GameState, message:Word)->Table:
    message=uint(message,16)
    bank=state.message_directory.long()
    bank_offset=u16(u16(message>>8)<<1)
    bank=u32(bank+s16(state.message_bank_offsets.word(bank_offset)))
    descriptor=state.table(bank)
    pointer=descriptor.long()
    item=u16(u16(message&255)<<1)
    pointer=u32(pointer+s16(descriptor.word(item,4)))
    return state.table(pointer)
