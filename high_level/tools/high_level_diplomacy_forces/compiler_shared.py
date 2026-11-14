"""Complete typed shared flows lowered to ordinary original-ABI operations."""
from .compiler_common import semantic_functions,lower_declared
from .target import SHARED_BINDINGS


DECLARATIONS={
 'choose_city_head':dict(signature='state:GameState, city:Word',returns='Word',flow='''city=uint(city,16)
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
return head'''),
 'roster_contains_force_head_carry':dict(signature='state:GameState, city:Word, head:Word',returns='HeadMatch',flow='''city=uint(city,16)
head=uint(head,16)
owner=u16(state.city_owners.byte(city))
force_head=state.force_heads.word(u16(owner<<1))
roster=state.candidate_roster.cursor()
while not negative_word(roster.word()):
    if roster.next_word()==force_head:
        outcome=state.carry_result(1)
        return HeadMatch(force_head,outcome.carry,outcome.conditional_sr)
outcome=state.carry_result(0)
return HeadMatch(head,outcome.carry,outcome.conditional_sr)'''),
 'prepare_message':dict(signature='state:GameState, message:Word',returns='None',flow='''message=uint(message,16)
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
state.set_message_pending(1)''',slots={40:('message_mode',0,65535)}),
 'select_message_layout':dict(signature='state:GameState',returns='None',flow='''offset=u16(state.message_layout_index()<<2)
state.set_scene(state.message_layout.word(offset))
state.set_stage(state.message_layout.word(offset,2))'''),
 'resolve_message_pointer':dict(signature='state:GameState, message:Word',returns='Table',flow='''message=uint(message,16)
bank=state.message_directory.long()
bank_offset=u16(u16(message>>8)<<1)
bank=u32(bank+s16(state.message_bank_offsets.word(bank_offset)))
descriptor=state.table(bank)
pointer=descriptor.long()
item=u16(u16(message&255)<<1)
pointer=u32(pointer+s16(descriptor.word(item,4)))
return state.table(pointer)'''),
}
APPROVED={'domain':{'GameState','Word','Table','HeadMatch','uint','u16','u32','s16','low8','negative_word'}}


def _head(e,r):
    empty,done,scan=e.fresh('empty'),e.fresh('done'),e.fresh('scan')
    e.ins('movem.l','%d1-%d5/%a0-%a2,-(%sp)',4)
    e.ins('lea','0xf500:w,%a0',4);e.ins('move.w','(%a0)+,%d4');e.ins('bmi.w',empty,4)
    e.ins('bsr.w','roster_contains_force_head_carry',4);e.ins('bcs.w',done,4)
    e.ins('andi.w','#0xff,%d4',4);e.ins('lea','0xc300:w,%a1',4)
    e.ins('move.w','%d4,%d3');e.ins('move.b','(%a1,%d3.w),%d1',4);e.ins('move.b','%d1,%d2')
    e.label(scan);e.ins('move.w','(%a0)+,%d3');e.ins('bmi.b',done)
    e.ins('andi.w','#0xff,%d3',4);e.ins('move.b','(%a1,%d3.w),%d1',4);e.ins('cmp.b','%d2,%d1');e.ins('bls.b',scan)
    e.ins('move.w','%d3,%d4');e.ins('move.b','%d1,%d2');e.ins('bra.b',scan)
    e.label(empty);e.ins('lea','0xf427:w,%a0',4);e.ins('move.b','#0xff,(%a0,%d0.w)',6)
    e.ins('lea','0xe80c:w,%a0',4);e.ins('move.w','%d0,%d1');e.ins('lsl.w','#1,%d1');e.ins('add.w','%d0,%d1');e.ins('lsl.w','#2,%d1')
    for displacement in ('','4','8'):
        operand='(%a0,%d1.w)' if not displacement else displacement+'(%a0,%d1.w)'
        e.ins('move.w','#0xffff,'+operand,6)
    e.label(done);e.ins('lsl.w','#1,%d0');e.ins('lea','0xf45e:w,%a0',4)
    e.ins('move.w','%d4,(%a0,%d0.w)',4);e.ins('move.w','%d4,%d0')
    e.ins('movem.l','(%sp)+,%d1-%d5/%a0-%a2',4)


def _match(e,r):
    scan,missing,done=e.fresh('scan'),e.fresh('missing'),e.fresh('done')
    e.ins('lea','0xf427:w,%a2',4);e.ins('clr.w','%d5');e.ins('move.b','(%a2,%d0.w),%d5',4)
    e.ins('lsl.w','#1,%d5');e.ins('lea','0xe640:w,%a2',4);e.ins('move.w','(%a2,%d5.w),%d5',4)
    e.ins('lea','0xf500:w,%a2',4);e.label(scan);e.ins('tst.w','(%a2)');e.ins('bmi.w',missing,4)
    e.ins('cmp.w','(%a2)+,%d5');e.ins('bne.b',scan);e.ins('move.w','%d5,%d4')
    e.ins('ori.w','#1,%sr',4);e.ins('bra.w',done,4);e.label(missing);e.ins('andi.w','#0xfffe,%sr',4);e.label(done)


def _message(e,r):
    done=e.fresh('done');e.ins('tst.w','%d0');e.ins('bmi.b',done)
    e.ins('clr.w','0xf652:w',4);e.ins('bsr.w','resolve_message_pointer',4);e.ins('move.l','%a0,0xf3be:w',4)
    e.ins('move.w','0xf612:w,0xf3c2:w',6);e.ins('move.w','0xf362:w,0xf3c4:w',6)
    e.ins('clr.w','0xf36a:w',4);e.ins('clr.w','0xf3c6:w',4);e.ins('move.w',f"#{r['message_mode']},0xf600:w",6)
    e.ins('bsr.w','select_message_layout',4);e.ins('move.w','#1,0xefda:w',6);e.label(done)


def _layout(e,r):
    e.ins('move.w','0xf6c4:w,%d0',4);e.ins('lsl.w','#2,%d0')
    for address,dest in ((0x6773C,'0xf612:w'),(0x6773E,'0xf362:w')):
        disp=address-(e.pc+2)
        e.ins('move.w',f'{disp}(%pc,%d0.w),{dest}',6)


def _pointer(e,r):
    e.ins('movea.l','0x92c4a:l,%a1',6);e.ins('move.w','%d0,%d1');e.ins('lsr.w','#8,%d1');e.ins('lsl.w','#1,%d1')
    e.ins('lea','0x92c4e:l,%a0',6);e.ins('move.w','(%a0,%d1.w),%d1',4);e.ins('adda.w','%d1,%a1')
    e.ins('movea.l','(%a1),%a0');e.ins('move.w','%d0,%d1');e.ins('andi.w','#0xff,%d1',4)
    e.ins('lsl.w','#1,%d1');e.ins('move.w','4(%a1,%d1.w),%d1',4);e.ins('adda.w','%d1,%a0')


LOWERERS={'choose_city_head':_head,'roster_contains_force_head_carry':_match,'prepare_message':_message,
          'select_message_layout':_layout,'resolve_message_pointer':_pointer}


def compile_shared(source):
    return lower_declared(semantic_functions(source,DECLARATIONS,APPROVED),SHARED_BINDINGS,LOWERERS)
