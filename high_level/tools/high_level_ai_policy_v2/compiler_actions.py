"""Restricted complete semantic AST admission and ordinary action lowering.

The compatibility backend selects typed arithmetic, live addressing, branches,
and ABI preservation. It does not open ROM, assembly, IR, objects or a cache.
"""
import ast
from .compiler_common import semantic_functions, lower_declared, CompileError
from .target import ACTIONS_BINDINGS


def _ins(e, operation, operands='', width=None):
    """Encoding extent from the admitted target operand family, not bytes."""
    if width is None:
        width = 2
        if operation.endswith('.w') and operation.startswith(('b','db')):
            width = 4
        elif operation in ('movem.l','movem.w'):
            width = 4
        elif operation in ('jsr','jmp'):
            width = 6 if ':l' in operands else 4
        elif ':l' in operands:
            width = 6
        elif ':w' in operands or '.w)' in operands or '(%a' in operands and operands.split(',')[0].lstrip().startswith(('0x','-0x')):
            width = 4
        if '#' in operands and operation not in ('moveq','lsl.w','lsl.l','lsr.w','lsr.l','addq.w','addq.l','addq.b','subq.w','subq.l','subq.b'):
            immediate = 4 if operation.endswith('.l') and operation not in ('btst.l','bset.l') else 2
            width += immediate
    e.ins(operation, operands, width)


def _label(e, role):
    return e.binding.name+'_'+role


def _mark(e, role):
    e.label(_label(e,role))


def _branch(e, operation, role):
    _ins(e,operation,_label(e,role))


def _call(e, name, absolute=False):
    _ins(e,'jsr' if absolute else 'bsr.w',name+(':l' if absolute else ''))


def _command(e, value):
    _ins(e,'move.w',f'#{value},0xf728:w')


def _carry(e, value):
    _ins(e,'ori.w' if value else 'andi.w','#1,%sr' if value else '#65534,%sr',4)


def _packet_base(e, register='%a0'):
    _ins(e,'lea.l','0x9000:w,'+register)
    _ins(e,'adda.w','0xf75a:w,'+register)


def _packet_sum(e, count, total, member, *, store=False, clear_first=False):
    _packet_base(e)
    if clear_first:
        _ins(e,'moveq','#0,'+total)
    _ins(e,'move.b','(%a0),'+count)
    _ins(e,'andi.w','#15,'+count)
    _ins(e,'subq.w','#1,'+count)
    if not clear_first:
        _ins(e,'moveq','#0,'+total)
    _ins(e,'lea.l','0xc800:w,%a1')
    _mark(e,'member')
    _ins(e,'clr.w',member)
    _ins(e,'move.b','0xd(%a0, '+count+'.w),'+member,4)
    _ins(e,'lsl.w','#2,'+member)
    _ins(e,'add.l','(%a1, '+member+'.w),'+total,4)
    _ins(e,'dbra',count+','+_label(e,'member'),4)
    if store:
        _ins(e,'move.l',total+',0xf744:w')


def _l_locate_packet_contact_city(e, r):
    for op,args in (('move.w','0xf75c:w,%d0'),('lsl.w','#4,%d0'),('move.w','%d0,%d1'),
                    ('subi.w','#8,%d0'),('addi.w','#24,%d1'),('move.w','0xf75e:w,%d2'),
                    ('lsl.w','#4,%d2'),('move.w','%d2,%d3'),('subi.w','#16,%d2'),('addi.w','#32,%d3'),
                    ('lea.l','0xd4b66:l,%a0'),('move.w','#39,%d4')): _ins(e,op,args)
    _mark(e,'city')
    _ins(e,'cmp.w','2(%a0),%d0',4);_branch(e,'bhi.w','next')
    _ins(e,'cmp.w','2(%a0),%d1',4);_branch(e,'bcs.w','next')
    _ins(e,'cmp.w','(%a0),%d2');_branch(e,'bhi.w','next')
    _ins(e,'cmp.w','(%a0),%d3');_branch(e,'bcc.w','owner')
    _mark(e,'next');_ins(e,'subq.l','#4,%a0');_ins(e,'dbra','%d4,'+_label(e,'city'),4)
    _mark(e,'owner');_ins(e,'lea.l','0xf428:w,%a0');_ins(e,'move.b','(%a0, %d4.w),%d5',4)
    _ins(e,'cmp.b','0xf377:w,%d5');_branch(e,'bne.w','hostile')
    _carry(e,1);_branch(e,'bra.w','return');_mark(e,'hostile');_carry(e,0)
    _ins(e,'andi.w','#255,%d4');_ins(e,'addq.w','#1,%d4');_ins(e,'move.w','%d4,0xf392:w')


def _l_choose_city_assault_action(e,r):
    _call(e,'measure_packet_ready_strength');_call(e,'measure_chosen_city_strength')
    _ins(e,'cmp.l','0xf744:w,%d1');_branch(e,'bcc.w','decline')
    _ins(e,'cmp.w','0xf748:w,%d2');_branch(e,'bhi.w','decline')
    _command(e,12);_branch(e,'bra.w','return');_mark(e,'decline');_command(e,13)


def _l_measure_packet_ready_strength(e,r):
    _ins(e,'movem.l','%d4/%a2-%a3,-(%a7)');_packet_base(e)
    _ins(e,'move.b','(%a0),%d2');_ins(e,'andi.w','#15,%d2');_ins(e,'subq.w','#1,%d2')
    _ins(e,'moveq','#0,%d0');_ins(e,'clr.w','%d1')
    for address,reg in (('0xc800','%a1'),('0xb200','%a2'),('0xb000','%a3')): _ins(e,'lea.l',address+':w,'+reg)
    _mark(e,'member');_ins(e,'clr.w','%d3')
    _ins(e,'move.b','13(%a0, %d2.w),%d3',4);_ins(e,'lsl.w','#2,%d3')
    _ins(e,'add.l','(%a1, %d3.w),%d0',4)
    _ins(e,'cmpi.l',f'#{r["ready_strength"]},(%a1, %d3.w)',8);_branch(e,'bcs.w','next')
    _ins(e,'lsr.w','#1,%d3');_ins(e,'move.w','(%a2, %d3.w),%d4',4)
    _ins(e,'cmp.w','(%a3, %d3.w),%d4',4);_branch(e,'bcs.w','next');_ins(e,'addq.w','#1,%d1')
    _mark(e,'next');_ins(e,'dbra','%d2,'+_label(e,'member'),4)
    _ins(e,'move.l','%d0,0xf744:w');_ins(e,'move.w','%d1,0xf748:w')
    _ins(e,'movem.l','(%a7)+,%d4/%a2-%a3')


def _l_measure_chosen_city_strength(e,r):
    _ins(e,'move.w','0xf392:w,%d0');_ins(e,'lea.l','0xc800:w,%a0');_ins(e,'lea.l','0xcd00:w,%a1')
    _ins(e,'moveq','#0,%d1');_ins(e,'clr.w','%d2');_ins(e,'move.w','#255,%d3');_mark(e,'officer')
    _ins(e,'cmp.b','-(%a1),%d0');_branch(e,'bne.w','next');_ins(e,'move.w','%d3,%d4');_ins(e,'lsl.w','#2,%d4')
    _ins(e,'add.l','(%a0, %d4.w),%d1',4);_ins(e,'cmpi.l','#5000,(%a0, %d4.w)',8)
    _branch(e,'bcs.w','next');_ins(e,'addq.w','#1,%d2');_mark(e,'next');_ins(e,'dbra','%d3,'+_label(e,'officer'),4)


def _sample_word_projection(e):
    _call(e,'step_random',True);_ins(e,'andi.l','#65535,%d0');_ins(e,'lsl.w','#2,%d0');_ins(e,'swap','%d0');_ins(e,'tst.w','%d0')


def _l_choose_city_mask_action(e,r):
    _ins(e,'lea.l','0xf427:w,%a0');_ins(e,'move.w','0xf392:w,%d0');_ins(e,'clr.w','%d1')
    _ins(e,'move.b','(%a0, %d0.w),%d1',4);_branch(e,'bmi.w','decline');_ins(e,'lsl.w','#1,%d1')
    _ins(e,'lea.l','0xe710:w,%a0');_ins(e,'move.w','(%a0, %d1.w),%d1',4)
    _ins(e,'move.w','0xf376:w,%d0');_ins(e,'subq.w','#1,%d0');_ins(e,'btst.l','%d0,%d1');_branch(e,'beq.w','decline')
    _sample_word_projection(e);_branch(e,'beq.w','decline');_command(e,16);_branch(e,'bra.w','return');_mark(e,'decline');_command(e,9)


def _processed_action(e, yes, no):
    _ins(e,'move.w','0xf392:w,%d0');_ins(e,'lea.l','0xea37:w,%a0');_ins(e,'tst.b','(%a0, %d0.w)',4)
    _branch(e,'bne.w','processed');_command(e,no);_branch(e,'bra.w','return');_mark(e,'processed');_command(e,yes)


def _l_choose_processed_city_action(e,r): _processed_action(e,10,7)


def _l_choose_linked_city_action(e,r):
    _ins(e,'lea.l','0xa150:w,%a0');_ins(e,'move.w','0xf392:w,%d0');_ins(e,'move.w','#255,%d1');_mark(e,'search')
    _ins(e,'cmp.b','-(%a0),%d0');_branch(e,'beq.w','found');_ins(e,'dbra','%d1,'+_label(e,'search'),4)
    _mark(e,'nonreturn');_branch(e,'bra.b','nonreturn');_mark(e,'found')
    _ins(e,'lea.l','0xcc00:w,%a0');_ins(e,'move.b','(%a0, %d1.w),%d2',4);_ins(e,'andi.w','#63,%d2')
    _ins(e,'lea.l','0xf427:w,%a0');_ins(e,'move.b','(%a0, %d2.w),%d2',4)
    _ins(e,'cmp.b','0xf377:w,%d2');_branch(e,'bne.w','other');_command(e,11);_branch(e,'bra.w','return');_mark(e,'other');_command(e,13)


def _l_choose_packet_resource_action(e,r):
    _call(e,'packet_resource_shortfall');_branch(e,'bcs.w','overwrite');_command(e,12);_mark(e,'overwrite');_command(e,13)


def _l_packet_resource_shortfall(e,r):
    _packet_base(e);_ins(e,'move.b','(%a0),%d0');_ins(e,'andi.w','#15,%d0');_ins(e,'subq.b','#1,%d0');_ins(e,'moveq','#0,%d1')
    for address,reg in (('0xb000','%a1'),('0xb200','%a2'),('0xc800','%a3')): _ins(e,'lea.l',address+':w,'+reg)
    _mark(e,'member');_ins(e,'clr.w','%d2');_ins(e,'move.b','13(%a0, %d0.w),%d2',4)
    _ins(e,'lsl.w','#2,%d2');_ins(e,'add.l','(%a3, %d2.w),%d1',4);_ins(e,'lsr.w','#1,%d2')
    _ins(e,'move.w','(%a1, %d2.w),%d3',4);_ins(e,'cmp.w','(%a2, %d2.w),%d3',4);_branch(e,'bhi.w','shortfall')
    _ins(e,'dbra','%d0,'+_label(e,'member'),4);_ins(e,'cmpi.l','#10000,%d1');_branch(e,'bcs.w','shortfall')
    _carry(e,0);_branch(e,'bra.w','return');_mark(e,'shortfall');_carry(e,1)


def _l_count_linked_force_officers(e,r):
    for address,reg in (('0xa050','%a0'),('0xf427','%a1'),('0xcc00','%a2')): _ins(e,'lea.l',address+':w,'+reg)
    _ins(e,'clr.w','%d0');_ins(e,'move.w','0xf392:w,%d1');_ins(e,'move.w','0xf376:w,%d3');_ins(e,'move.w','#255,%d2');_mark(e,'officer')
    _ins(e,'move.b','(%a0, %d2.w),%d4',4);_ins(e,'andi.w','#63,%d4');_ins(e,'cmp.b','%d1,%d4');_branch(e,'bne.w','next')
    _ins(e,'move.b','(%a2, %d2.w),%d4',4);_ins(e,'andi.w','#63,%d4');_ins(e,'cmp.b','(%a1, %d4.w),%d3',4);_branch(e,'bne.w','next')
    _ins(e,'addq.w','#1,%d0');_mark(e,'next');_ins(e,'dbra','%d2,'+_label(e,'officer'),4)


def _l_build_limited_packet_roster(e,r):
    _packet_base(e);_ins(e,'move.b','(%a0),%d0');_ins(e,'andi.w','#15,%d0');_ins(e,'move.w','%d0,%d3');_ins(e,'subq.w','#1,%d3')
    _ins(e,'lea.l','0xd300:w,%a1');_ins(e,'clr.w','%d2');_mark(e,'reverse')
    _ins(e,'move.b','13(%a0, %d3.w),%d2',4);_ins(e,'move.w','%d2,(%a1)+');_ins(e,'dbra','%d3,'+_label(e,'reverse'),4)
    _ins(e,'move.w','#65535,(%a1)');_ins(e,'move.w','#65535,2(%a1)',6)
    _ins(e,'cmp.w','%d1,%d0');_branch(e,'bls.w','copy');_call(e,'rank_packet_roster');_call(e,'partition_ranked_packet_roster')
    _mark(e,'copy');_ins(e,'lea.l','0xf500:w,%a0');_ins(e,'lea.l','0xd300:w,%a1');_ins(e,'clr.w','%d2');_mark(e,'marked')
    _ins(e,'move.w','(%a1)+,%d3');_branch(e,'bmi.w','unmarked');_ins(e,'bset.l','#14,%d3');_ins(e,'move.w','%d3,(%a0)+')
    _ins(e,'addq.w','#1,%d2');_branch(e,'bra.b','marked');_mark(e,'unmarked');_ins(e,'move.w','(%a1)+,(%a0)+')
    _branch(e,'bmi.w','counted');_ins(e,'addq.w','#1,%d2');_branch(e,'bra.b','unmarked');_mark(e,'counted');_ins(e,'move.w','%d2,0xf636:w')


def _l_rank_packet_roster(e,r):
    _ins(e,'movem.l','%d0-%d5/%a0-%a1,-(%a7)');_ins(e,'lea.l','0xd300:w,%a0');_ins(e,'lea.l','0xc800:w,%a4');_ins(e,'lea.l','0xb400:w,%a5')
    _ins(e,'move.w','#65535,(%a1)');_mark(e,'head');_ins(e,'move.w','(%a0),%d0');_branch(e,'bmi.w','restore')
    _ins(e,'lsl.w','#2,%d0');_ins(e,'move.w','2(%a4, %d3.w),%d1',4);_ins(e,'cmpi.w','#10000,%d1');_branch(e,'bls.w','capped');_ins(e,'move.w','#10000,%d1')
    _mark(e,'capped');_ins(e,'lsr.w','#1,%d0');_ins(e,'move.w','(%a5, %d0.w),%d2',4);_ins(e,'lsr.w','#1,%d0')
    for address,reg in (('0xd320','%a1'),('0xd340','%a2'),('0xd360','%a3')): _ins(e,'lea.l',address+':w,'+reg)
    _mark(e,'rank');_ins(e,'tst.w','(%a1)');_branch(e,'bmi.w','insert');_ins(e,'cmp.w','(%a2),%d1');_branch(e,'bcs.w','advance')
    _ins(e,'cmp.w','(%a3),%d2');_branch(e,'bcs.w','advance');_mark(e,'insert')
    _ins(e,'move.w','(%a1),%d3');_ins(e,'move.w','%d0,(%a1)+');_branch(e,'bmi.b','head')
    _ins(e,'move.w','(%a2),%d4');_ins(e,'move.w','%d1,(%a2)+');_ins(e,'move.w','(%a3)+,%d5');_ins(e,'move.w','%d2,(%a3)+')
    _ins(e,'move.w','%d3,%d0');_ins(e,'move.w','%d4,%d1');_ins(e,'move.w','%d5,%d2');_branch(e,'bra.b','insert')
    _mark(e,'advance');_ins(e,'addq.w','#2,%a1');_ins(e,'addq.w','#2,%a2');_ins(e,'addq.w','#2,%a3');_branch(e,'bra.b','rank')
    _mark(e,'restore');_ins(e,'movem.l','(%a7)+,%d0-%d5/%a0-%a1')


def _l_partition_ranked_packet_roster(e,r):
    _ins(e,'lea.l','0xd300:w,%a0');_ins(e,'lea.l','0xd320:w,%a1');_ins(e,'move.w','%d1,%d2');_ins(e,'subq.w','#1,%d2');_mark(e,'limited')
    _ins(e,'move.w','(%a1)+,(%a0)+');_ins(e,'dbra','%d2,'+_label(e,'limited'),4);_ins(e,'move.w','#65535,(%a0)+');_mark(e,'tail')
    _ins(e,'move.w','(%a1)+,(%a0)+');_branch(e,'bpl.b','tail')


def _candidate_action(e,call, yes, no):
    _call(e,call);_ins(e,'tst.w','0xd300:w');_branch(e,'bmi.w','empty');_command(e,yes);_branch(e,'bra.w','return');_mark(e,'empty');_command(e,no)


def _l_choose_adjacent_group_action(e,r): _candidate_action(e,'collect_adjacent_hostile_groups',14,16)


def _l_collect_adjacent_hostile_groups(e,r):
    _ins(e,'lea.l','0x9000:w,%a0');_ins(e,'move.w','0xf75a:w,%d0');_ins(e,'move.b','2(%a0, %d0.w),%d3',4)
    _ins(e,'move.b','%d3,%d4');_ins(e,'subi.b','#1,%d4');_ins(e,'move.b','%d3,%d5');_ins(e,'addi.b','#1,%d5')
    _ins(e,'move.b','1(%a0, %d0.w),%d0',4);_ins(e,'move.b','%d0,%d1');_ins(e,'subi.b','#1,%d1');_ins(e,'move.b','%d0,%d2');_ins(e,'addi.b','#1,%d2')
    _ins(e,'lea.l','0xd300:w,%a1');_ins(e,'clr.w','%d7');_mark(e,'packet');_ins(e,'move.b','(%a0),%d6');_ins(e,'andi.w','#15,%d6');_branch(e,'beq.w','terminator')
    _ins(e,'swap','%d0');_ins(e,'move.b','4(%a0),%d0',4);_ins(e,'cmp.b','0xf377:w,%d0');_branch(e,'beq.w','next')
    _ins(e,'cmp.b','1(%a0),%d1',4);_branch(e,'bne.w','center');_ins(e,'cmp.b','2(%a0),%d3',4);_branch(e,'beq.w','append')
    _mark(e,'center');_ins(e,'cmp.b','1(%a0),%d0',4);_branch(e,'bne.w','right');_ins(e,'cmp.b','2(%a0),%d4',4);_branch(e,'beq.w','append')
    _ins(e,'cmp.b','2(%a0),%d5',4);_branch(e,'beq.w','append');_mark(e,'right');_ins(e,'cmp.b','1(%a0),%d2',4);_branch(e,'bne.w','next')
    _ins(e,'cmp.b','2(%a0),%d3',4);_branch(e,'bne.w','next');_mark(e,'append');_ins(e,'move.w','%d7,(%a1)+')
    _mark(e,'next');_ins(e,'lea.l','13(%a0, %d6.w),%a0',4);_ins(e,'addi.w','#13,%d6');_ins(e,'add.w','%d6,%d7');_branch(e,'bra.b','packet')
    _mark(e,'terminator');_ins(e,'move.w','#65535,(%a1)')


def _l_choose_adjacent_strength_action(e,r):
    _call(e,'store_packet_strength');_call(e,'select_largest_hostile_candidate');_ins(e,'tst.w','%d0');_branch(e,'bmi.w','decline')
    _ins(e,'cmp.l','0xf744:w,%d1');_branch(e,'bcc.w','decline');_ins(e,'move.w','%d0,0xf744:w');_command(e,15)
    _branch(e,'bra.w','return');_mark(e,'decline');_command(e,16)


def _l_store_packet_strength(e,r): _packet_sum(e,'%d1','%d0','%d2',store=True,clear_first=True)


def _l_select_largest_hostile_candidate(e,r):
    _ins(e,'lea.l','0xd300:w,%a0');_ins(e,'move.w','#65535,%d0');_ins(e,'moveq','#-1,%d1')
    _ins(e,'lea.l','0xc800:w,%a1');_ins(e,'lea.l','0xe710:w,%a2');_ins(e,'move.w','0xf376:w,%d7');_ins(e,'lsl.w','#1,%d7')
    _ins(e,'move.w','(%a2, %d7.w),%d7',4);_mark(e,'candidate');_ins(e,'move.w','(%a0)+,%d2');_branch(e,'bmi.w','return')
    _call(e,'measure_unmasked_candidate_strength');_branch(e,'bcs.b','candidate');_ins(e,'cmp.l','%d1,%d4');_branch(e,'bls.b','candidate')
    _ins(e,'move.l','%d4,%d1');_ins(e,'move.w','%d2,%d0');_branch(e,'bra.b','candidate')


def _l_measure_unmasked_candidate_strength(e,r):
    _ins(e,'lea.l','0x9000:w,%a3');_ins(e,'adda.w','%d2,%a3');_ins(e,'move.b','4(%a3),%d3',4);_ins(e,'btst.l','%d3,%d7');_branch(e,'bne.w','masked')
    _ins(e,'move.b','(%a3),%d3');_ins(e,'andi.w','#15,%d3');_ins(e,'subq.w','#1,%d3');_ins(e,'moveq','#0,%d4')
    _mark(e,'member');_ins(e,'clr.w','%d5');_ins(e,'move.b','13(%a3, %d3.w),%d5',4);_ins(e,'lsl.w','#2,%d5');_ins(e,'add.l','(%a1, %d5.w),%d4',4)
    _ins(e,'dbra','%d3,'+_label(e,'member'),4);_carry(e,0);_branch(e,'bra.w','return');_mark(e,'masked');_carry(e,1)


def _l_queue_packet_stationary_command(e,r):
    _packet_base(e);_ins(e,'lea.l','0xff3000:l,%a1');_ins(e,'adda.w','0xff3826:l,%a1');_ins(e,'clr.b','(%a1)+')
    _ins(e,'move.b','13(%a0),(%a1)+',4);_ins(e,'move.b','3(%a0),(%a1)+',4)
    _ins(e,'move.b','#144,(%a1)+');_ins(e,'move.b','#50,(%a1)+');_ins(e,'clr.b','(%a1)+');_ins(e,'move.b','#255,(%a1)')
    _ins(e,'addq.w','#6,0xff3826:l');_command(e,65535)


def _l_choose_reachable_city_action(e,r):
    _call(e,'packet_resource_range');_call(e,'collect_reachable_hostile_cities');_ins(e,'tst.w','0xd300:w');_branch(e,'bmi.w','decline')
    _call(e,'measure_packet_ready_strength');_ins(e,'tst.w','%d1');_branch(e,'beq.w','decline');_call(e,'select_lightest_reachable_city')
    _ins(e,'tst.w','0xf392:w');_branch(e,'bmi.w','decline');_command(e,17);_branch(e,'bra.w','return');_mark(e,'decline');_command(e,18)


def _l_packet_resource_range(e,r):
    _packet_base(e);_ins(e,'move.b','(%a0),%d0');_ins(e,'andi.w','#15,%d0');_ins(e,'subq.w','#1,%d0');_ins(e,'moveq','#0,%d1')
    _ins(e,'lea.l','0xc800:w,%a1');_mark(e,'member');_ins(e,'clr.w','%d2');_ins(e,'move.b','13(%a0, %d0.w),%d2',4)
    _ins(e,'lsl.w','#2,%d2');_ins(e,'add.l','(%a1, %d2.w),%d1',4);_ins(e,'addi.l','#100,%d1');_ins(e,'dbra','%d0,'+_label(e,'member'),4)
    _ins(e,'divu.w','#10,%d1');_ins(e,'move.w','%d1,%d2');_ins(e,'lsl.w','#1,%d1');_ins(e,'add.w','%d2,%d1')
    _ins(e,'move.b','9(%a0),%d0',4);_ins(e,'lsl.w','#8,%d0');_ins(e,'move.b','10(%a0),%d0',4);_ins(e,'lsl.l','#8,%d0')
    _ins(e,'move.b','11(%a0),%d0',4);_ins(e,'lsl.l','#8,%d0');_ins(e,'move.b','12(%a0),%d0',4);_ins(e,'divu.w','%d1,%d0')
    _ins(e,'tst.w','%d0');_branch(e,'beq.w','return');_ins(e,'subq.w','#1,%d0');_ins(e,'cmpi.w','#2,%d0');_branch(e,'bls.w','capped')
    _ins(e,'move.w','#2,%d0');_mark(e,'capped');_ins(e,'clr.w','%d1');_ins(e,'move.b','3(%a0),%d1',4);_ins(e,'mulu.w','%d1,%d0')


def _l_collect_reachable_hostile_cities(e,r):
    _ins(e,'lea.l','0xd4b66:l,%a0');_ins(e,'move.w','0xf75c:w,%d1');_ins(e,'move.w','%d1,0xf63c:w');_ins(e,'move.w','0xf75e:w,%d2');_ins(e,'move.w','%d2,0xf63e:w')
    for address,reg in (('0xf450','%a1'),('0xd300','%a2'),('0xd400','%a3')): _ins(e,'lea.l',address+':w,'+reg)
    _ins(e,'move.w','#39,%d3');_mark(e,'city');_ins(e,'move.b','-(%a1),%d4');_ins(e,'cmp.b','0xf377:w,%d4');_branch(e,'beq.w','next')
    _ins(e,'move.w','2(%a0),%d4',4);_ins(e,'lsr.w','#4,%d4');_ins(e,'move.w','%d4,0xf640:w');_ins(e,'sub.w','%d1,%d4');_branch(e,'bcc.w','x_distance')
    _ins(e,'neg.w','%d4');_mark(e,'x_distance');_ins(e,'cmp.w','%d0,%d4');_branch(e,'bhi.w','next')
    _ins(e,'move.w','(%a0),%d5');_ins(e,'lsr.w','#4,%d5');_ins(e,'move.w','%d5,0xf642:w');_ins(e,'sub.w','%d2,%d5');_branch(e,'bcc.w','y_distance')
    _ins(e,'neg.w','%d5');_mark(e,'y_distance');_ins(e,'add.w','%d5,%d4');_ins(e,'cmp.w','%d0,%d4');_branch(e,'bhi.w','next')
    _ins(e,'movem.l','%d0-%d3/%a0-%a3,-(%a7)');_call(e,'build_path_from_cells',True);_ins(e,'movem.l','(%a7)+,%d0-%d3/%a0-%a3')
    _ins(e,'cmp.w','0xf644:w,%d0');_branch(e,'bls.w','next');_ins(e,'move.w','%d3,(%a2)+');_ins(e,'move.w','0xf644:w,(%a3)+')
    _mark(e,'next');_ins(e,'subq.w','#4,%a0');_ins(e,'dbra','%d3,'+_label(e,'city'),4);_ins(e,'move.w','#65535,(%a2)')


def _l_select_lightest_reachable_city(e,r):
    for address,reg in (('0xd300','%a0'),('0xc800','%a1'),('0xd3fe','%a4')): _ins(e,'lea.l',address+':w,'+reg)
    _ins(e,'moveq','#-1,%d7');_ins(e,'move.w','#65535,0xf392:w');_ins(e,'move.w','#65535,%d6');_mark(e,'candidate')
    _ins(e,'addq.w','#2,%a4');_ins(e,'move.w','(%a0)+,%d2');_branch(e,'bmi.w','return');_call(e,'measure_indexed_city_strength')
    _ins(e,'cmp.w','%d1,%d4');_branch(e,'bhi.b','candidate');_ins(e,'cmp.l','%d7,%d3');_branch(e,'bhi.b','candidate');_branch(e,'bne.w','select')
    _ins(e,'cmp.w','(%a4),%d6');_branch(e,'bls.b','candidate');_mark(e,'select');_ins(e,'move.w','(%a4),%d6');_ins(e,'move.l','%d3,%d7')
    _ins(e,'move.w','%d2,0xf392:w');_branch(e,'bra.b','candidate')


def _l_measure_indexed_city_strength(e,r):
    _ins(e,'move.w','%d6,-(%a7)');_ins(e,'lea.l','0xc800:w,%a2');_ins(e,'moveq','#0,%d3');_ins(e,'clr.w','%d4');_ins(e,'lea.l','0xcd00:w,%a3')
    _ins(e,'move.w','#255,%d5');_ins(e,'addq.w','#1,%d2');_mark(e,'officer');_ins(e,'cmp.b','-(%a3),%d2');_branch(e,'bne.w','next')
    _ins(e,'move.w','%d5,%d6');_ins(e,'lsl.w','#2,%d6');_ins(e,'move.l','(%a2, %d6.w),%d6',4);_ins(e,'add.l','%d6,%d3');_ins(e,'cmpi.l','#5000,%d6')
    _branch(e,'bcs.w','next');_ins(e,'addq.w','#1,%d4');_mark(e,'next');_ins(e,'dbra','%d5,'+_label(e,'officer'),4);_ins(e,'move.w','(%a7)+,%d6')


def _l_queue_packet_march_action(e,r):
    _packet_base(e);_ins(e,'clr.w','%d0');_ins(e,'move.b','3(%a0),%d0',4);_ins(e,'move.w','%d0,0xf744:w')
    _ins(e,'move.w','0xf75c:w,%d0');_ins(e,'lsl.w','#4,%d0');_ins(e,'move.w','%d0,0xf746:w');_ins(e,'move.w','0xf75e:w,%d0')
    _ins(e,'lsl.w','#4,%d0');_ins(e,'move.w','%d0,0xf748:w');_ins(e,'move.b','13(%a0),%d0',4);_ins(e,'move.w','%d0,0xf74a:w')
    _call(e,'build_ai_movement_packet');_command(e,22)


def _l_choose_reachable_group_action(e,r):
    _call(e,'store_packet_comparison_strength');_ins(e,'clr.w','%d0');_ins(e,'move.b','3(%a0),%d0',4);_call(e,'collect_reachable_hostile_groups')
    _ins(e,'tst.w','0xd300:w');_branch(e,'bmi.w','decline');_call(e,'select_lightest_group_candidate');_ins(e,'cmp.l','0xf744:w,%d0');_branch(e,'bhi.w','decline')
    _command(e,19);_branch(e,'bra.w','return');_mark(e,'decline');_command(e,4)


def _l_store_packet_comparison_strength(e,r): _packet_sum(e,'%d0','%d1','%d2',store=True)


def _l_collect_reachable_hostile_groups(e,r):
    _ins(e,'lea.l','0x9000:w,%a0');_ins(e,'lea.l','0xe710:w,%a1');_ins(e,'move.w','0xf376:w,%d1');_ins(e,'lsl.w','#1,%d1');_ins(e,'move.w','(%a1, %d1.w),%d1',4)
    _ins(e,'move.w','0xf75c:w,%d5');_ins(e,'move.w','%d5,0xf63c:w');_ins(e,'move.w','0xf75e:w,%d6');_ins(e,'move.w','%d6,0xf63e:w')
    _ins(e,'clr.w','%d7');_ins(e,'lea.l','0xd300:w,%a1');_mark(e,'packet');_ins(e,'move.b','(%a0),%d2');_ins(e,'andi.w','#15,%d2');_branch(e,'beq.w','terminator')
    _ins(e,'clr.w','%d3');_ins(e,'move.b','4(%a0),%d3',4);_ins(e,'cmp.w','0xf376:w,%d3');_branch(e,'beq.w','next');_ins(e,'btst.l','%d3,%d1');_branch(e,'bne.w','next')
    _ins(e,'clr.w','%d3');_ins(e,'move.b','1(%a0),%d3',4);_ins(e,'move.w','%d3,0xf640:w');_ins(e,'sub.b','%d5,%d3');_branch(e,'bcc.w','x_distance')
    _ins(e,'neg.w','%d3');_mark(e,'x_distance');_ins(e,'cmp.w','%d0,%d3');_branch(e,'bhi.w','next')
    _ins(e,'clr.w','%d4');_ins(e,'move.b','2(%a0),%d4',4);_ins(e,'move.w','%d4,0xf642:w');_ins(e,'sub.w','%d6,%d4');_branch(e,'bcc.w','y_distance')
    _ins(e,'neg.w','%d4');_mark(e,'y_distance');_ins(e,'add.w','%d4,%d3');_ins(e,'cmp.w','%d0,%d3');_branch(e,'bhi.w','next')
    _ins(e,'movem.l','%d0-%d7/%a0-%a1,-(%a7)');_call(e,'build_path_from_cells',True);_ins(e,'movem.l','(%a7)+,%d0-%d7/%a0-%a1')
    _ins(e,'cmp.w','0xf644:w,%d0');_branch(e,'bcs.w','next');_ins(e,'move.w','%d7,(%a1)+')
    _mark(e,'next');_ins(e,'lea.l','13(%a0, %d2.w),%a0',4);_ins(e,'addi.w','#13,%d2');_ins(e,'add.w','%d2,%d7');_branch(e,'bra.b','packet')
    _mark(e,'terminator');_ins(e,'move.w','#65535,(%a1)')


def _l_select_lightest_group_candidate(e,r):
    _ins(e,'lea.l','0xd300:w,%a0');_ins(e,'moveq','#-1,%d0');_ins(e,'lea.l','0xc800:w,%a1');_mark(e,'candidate')
    _ins(e,'move.w','(%a0)+,%d1');_branch(e,'bmi.w','selected');_call(e,'measure_group_candidate_strength');_ins(e,'cmp.l','%d0,%d4');_branch(e,'bcc.b','candidate')
    _ins(e,'move.l','%d4,%d0');_ins(e,'move.w','%d1,%d5');_branch(e,'bra.b','candidate');_mark(e,'selected');_ins(e,'move.w','%d5,0xf748:w')


def _l_measure_group_candidate_strength(e,r):
    _ins(e,'lea.l','0x9000:w,%a2');_ins(e,'adda.w','%d1,%a2');_ins(e,'move.b','(%a2),%d2');_ins(e,'andi.b','#15,%d2');_ins(e,'subq.w','#1,%d2')
    _ins(e,'moveq','#0,%d4');_mark(e,'member');_ins(e,'clr.w','%d3');_ins(e,'move.b','13(%a2, %d2.w),%d3',4);_ins(e,'lsl.w','#2,%d3')
    _ins(e,'add.l','(%a1, %d3.w),%d4',4);_ins(e,'dbra','%d2,'+_label(e,'member'),4)


def _l_purchase_packet_supplies(e,r):
    for name in ('load_packet_cash','fill_packet_troop_deficits','buy_packet_food','buy_packet_equipment'): _call(e,name)
    _ins(e,'move.b','%d7,8(%a0)',4);_ins(e,'lsr.l','#8,%d7');_ins(e,'move.b','%d7,7(%a0)',4)
    _ins(e,'lsr.l','#8,%d7');_ins(e,'move.b','%d7,6(%a0)',4);_ins(e,'lsr.w','#8,%d7');_ins(e,'move.b','%d7,5(%a0)',4);_command(e,65535)


def _load_packed_long(e,first,destination):
    for index in range(4):
        if index: _ins(e,'lsl.w' if index==1 else 'lsl.l','#8,'+destination)
        _ins(e,'move.b',str(first+index)+'(%a0),'+destination,4)


def _l_load_packet_cash(e,r):
    _packet_base(e);_load_packed_long(e,5,'%d7')


def _l_fill_packet_troop_deficits(e,r):
    _ins(e,'lea.l','0xb000:w,%a1');_ins(e,'lea.l','0xb200:w,%a2');_ins(e,'move.b','(%a0),%d1');_ins(e,'andi.w','#15,%d1');_ins(e,'subq.w','#1,%d1')
    _mark(e,'member');_ins(e,'clr.w','%d2');_ins(e,'move.b','13(%a0, %d1.w),%d2',4);_ins(e,'lsl.w','#1,%d2');_ins(e,'move.w','(%a1, %d2.w),%d3',4)
    _ins(e,'sub.w','(%a2, %d2.w),%d3',4);_branch(e,'beq.w','next');_ins(e,'move.w','%d3,%d4');_ins(e,'mulu.w','#50,%d4')
    _ins(e,'sub.l','%d4,%d7');_branch(e,'bcs.w','restore');_ins(e,'add.w','%d3,(%a2, %d2.w)',4)
    _mark(e,'next');_ins(e,'dbra','%d1,'+_label(e,'member'),4);_branch(e,'bra.w','return');_mark(e,'restore');_ins(e,'add.l','%d4,%d7')


def _l_buy_packet_food(e,r):
    _call(e,'price_packed_group');_ins(e,'move.l','%d2,%d3');_ins(e,'move.l','%d2,%d4');_ins(e,'lsl.l','#2,%d3');_ins(e,'add.l','%d2,%d3');_ins(e,'lsl.l','#2,%d3')
    _ins(e,'move.l','%d7,%d1');_ins(e,'lsl.l','#3,%d1');_ins(e,'moveq','#10,%d2');_call(e,'signed_divmod',True);_ins(e,'divu.w','%d3,%d1')
    _ins(e,'tst.w','%d1');_branch(e,'beq.w','return');_ins(e,'move.w','%d1,%d0');_ins(e,'mulu.w','%d4,%d1');_load_packed_long(e,9,'%d2')
    _ins(e,'add.l','%d1,%d2');_ins(e,'move.b','%d2,12(%a0)',4);_ins(e,'lsr.l','#8,%d2');_ins(e,'move.b','%d2,11(%a0)',4)
    _ins(e,'lsr.l','#8,%d2');_ins(e,'move.b','%d2,10(%a0)',4);_ins(e,'lsr.w','#8,%d2');_ins(e,'move.b','%d2,9(%a0)',4)
    _ins(e,'mulu.w','%d3,%d0');_ins(e,'sub.l','%d0,%d7')


def _l_buy_packet_equipment(e,r):
    _ins(e,'cmp.l','0xd2ea:l,%d7');_branch(e,'bcs.w','return');_ins(e,'move.b','(%a0),%d0');_ins(e,'andi.w','#15,%d0');_ins(e,'subq.w','#1,%d0')
    _ins(e,'lea.l','0xea88:w,%a1');_ins(e,'lea.l','0xb400:w,%a2');_mark(e,'member');_ins(e,'clr.w','%d1')
    _ins(e,'move.b','13(%a0, %d0.w),%d1',4);_ins(e,'move.w','%d1,%d2');_ins(e,'lsl.w','#1,%d1');_ins(e,'cmpi.w','#100,(%a2, %d1.w)',6)
    _branch(e,'bcs.w','next');_ins(e,'add.w','%d2,%d1');_ins(e,'move.b','#4,(%a2, %d1.w)',6)
    _ins(e,'sub.l','0xd2ea:l,%d7');_ins(e,'cmp.l','0xd2ea:l,%d7');_branch(e,'bcs.w','return')
    _mark(e,'next');_ins(e,'dbra','%d0,'+_label(e,'member'),4)


def _l_clear_packet_supply_command(e,r): _command(e,65535)


def _l_choose_packet_readiness_action(e,r):
    _call(e,'measure_packet_ready_strength');_ins(e,'tst.w','%d1');_branch(e,'beq.w','decline');_command(e,8);_branch(e,'bra.w','return');_mark(e,'decline');_command(e,4)


def _l_load_active_packet_roster(e,r):
    _ins(e,'movea.l','0xff382c:l,%a0');_ins(e,'lea.l','0xf72a:w,%a1');_ins(e,'clr.w','%d1');_ins(e,'move.b','4(%a0),%d1',4);_ins(e,'move.w','%d1,0xf376:w')
    _ins(e,'move.b','(%a0),%d0');_ins(e,'andi.w','#15,%d0');_ins(e,'subq.w','#1,%d0');_mark(e,'member');_ins(e,'clr.w','%d1')
    _ins(e,'move.b','13(%a0, %d0.w),%d1',4);_ins(e,'move.w','%d1,(%a1)+');_ins(e,'dbra','%d0,'+_label(e,'member'),4);_ins(e,'move.w','#65535,(%a1)')


def _l_choose_active_packet_contact_action(e,r):
    _call(e,'active_packet_terrain_contact');_branch(e,'bcs.w','contact');_command(e,8);_branch(e,'bra.w','return');_mark(e,'contact');_command(e,3)


def _l_active_packet_terrain_contact(e,r):
    _ins(e,'movea.l','0xff382c:l,%a0');_ins(e,'clr.w','%d0');_ins(e,'move.b','1(%a0),%d0',4);_ins(e,'clr.w','%d1');_ins(e,'move.b','2(%a0),%d1',4)
    _ins(e,'move.w','%d0,%d2');_ins(e,'lsl.w','#3,%d2');_ins(e,'add.w','%d0,%d2');_ins(e,'lsl.w','#3,%d2');_ins(e,'add.w','%d1,%d2')
    _ins(e,'lea.l','0xee5f0:l,%a1');_ins(e,'adda.w','%d2,%a1')
    for displacement in (-72,-1,1):
        _ins(e,'cmpi.b',f'#1,{displacement}(%a1)',6);_branch(e,'beq.w','water')
    _ins(e,'cmpi.b','#1,72(%a1)',6);_branch(e,'bne.w','clear');_mark(e,'water')
    _ins(e,'move.w','%d0,%d2');_ins(e,'subq.w','#1,%d0');_ins(e,'addq.w','#1,%d2');_ins(e,'lsl.w','#4,%d0');_ins(e,'lsl.w','#4,%d2')
    _ins(e,'addq.w','#8,%d0');_ins(e,'addq.w','#8,%d2');_ins(e,'move.w','%d1,%d3');_ins(e,'subq.w','#1,%d1');_ins(e,'addq.w','#2,%d3')
    _ins(e,'lsl.w','#4,%d1');_ins(e,'lsl.w','#4,%d3');_ins(e,'lea.l','0xd4b66:l,%a1');_ins(e,'move.w','#39,%d6');_mark(e,'city')
    _ins(e,'move.w','2(%a1),%d7',4);_ins(e,'cmp.w','%d0,%d7');_branch(e,'bcs.w','next');_ins(e,'cmp.w','%d2,%d7');_branch(e,'bhi.w','next')
    _ins(e,'move.w','(%a1),%d7');_ins(e,'cmp.w','%d1,%d7');_branch(e,'bcs.w','next');_ins(e,'cmp.w','%d3,%d7');_branch(e,'bls.w','owner')
    _mark(e,'next');_ins(e,'subq.w','#4,%a1');_ins(e,'dbra','%d6,'+_label(e,'city'),4);_mark(e,'owner')
    _ins(e,'lea.l','0xf428:w,%a1');_ins(e,'move.b','(%a1, %d6.w),%d0',4);_ins(e,'cmp.b','4(%a0),%d0',4);_branch(e,'beq.w','clear')
    _ins(e,'addq.w','#1,%d6');_ins(e,'move.w','%d6,0xf392:w');_carry(e,1);_branch(e,'bra.w','return');_mark(e,'clear');_carry(e,0)


def _l_choose_active_city_assault_action(e,r):
    _call(e,'project_selected_roster_strength');_call(e,'measure_self_assigned_officers');_ins(e,'cmp.l','%d0,%d2');_branch(e,'bhi.w','decline')
    _ins(e,'cmp.w','%d1,%d3');_branch(e,'bhi.w','decline');_command(e,7);_branch(e,'bra.w','return');_mark(e,'decline');_command(e,8)


def _l_project_selected_roster_strength(e,r):
    _ins(e,'lea.l','0xf72a:w,%a0');_ins(e,'lea.l','0xc800:w,%a1');_ins(e,'moveq','#0,%d0');_ins(e,'clr.w','%d1');_mark(e,'officer')
    _ins(e,'move.w','(%a0)+,%d0');_branch(e,'bmi.w','return');_ins(e,'lsl.w','#2,%d0');_ins(e,'move.l','(%a1, %d0.w),%d2',4)
    _ins(e,'add.l','%d2,%d0');_ins(e,'cmpi.l','#5000,%d2');_branch(e,'bcs.b','officer');_ins(e,'addq.w','#1,%d1');_branch(e,'bra.b','officer')


def _l_measure_self_assigned_officers(e,r):
    _ins(e,'move.w','0xf392:w,%d4');_ins(e,'lea.l','0xcd00:w,%a0');_ins(e,'lea.l','0xc800:w,%a1');_ins(e,'moveq','#0,%d2')
    _ins(e,'clr.w','%d3');_ins(e,'move.w','#255,%d4');_mark(e,'officer');_ins(e,'cmp.b','-(%a0),%d4');_branch(e,'bne.w','next')
    _ins(e,'move.w','%d4,%d5');_ins(e,'lsl.w','#2,%d5');_ins(e,'move.l','(%a1, %d5.w),%d6',4);_ins(e,'add.l','%d6,%d2');_ins(e,'cmpi.l','#5000,%d6')
    _branch(e,'bcs.w','next');_ins(e,'addq.w','#1,%d3');_mark(e,'next');_ins(e,'dbra','%d4,'+_label(e,'officer'),4)


def _l_choose_active_city_mask_action(e,r):
    _ins(e,'move.w','0xf376:w,%d0');_ins(e,'lsl.w','#1,%d0');_ins(e,'lea.l','0xe710:w,%a0');_ins(e,'move.w','(%a0, %d0.w),%d0',4)
    _ins(e,'lea.l','0xf427:w,%a0');_ins(e,'move.w','0xf392:w,%d1');_ins(e,'clr.w','%d2');_ins(e,'move.b','(%a0, %d1.w),%d2',4)
    _ins(e,'btst.l','%d2,%d0');_branch(e,'beq.w','decline');_sample_word_projection(e);_branch(e,'beq.w','decline');_command(e,8)
    _branch(e,'bra.w','return');_mark(e,'decline');_command(e,4)


def _l_choose_active_processed_city_action(e,r):
    _ins(e,'lea.l','0xea37:w,%a0');_ins(e,'move.w','0xf392:w,%d0');_ins(e,'tst.b','(%a0, %d0.w)',4)
    _branch(e,'bne.w','processed');_command(e,2);_branch(e,'bra.w','return');_mark(e,'processed');_command(e,5)


def _l_choose_active_linked_city_action(e,r):
    _call(e,'linked_city_force');_ins(e,'cmp.w','0xf376:w,%d1');_branch(e,'bne.w','other');_command(e,6);_branch(e,'bra.w','return');_mark(e,'other');_command(e,8)


def _l_linked_city_force(e,r):
    _ins(e,'lea.l','0xa050:w,%a0');_ins(e,'move.w','0xf392:w,%d0');_ins(e,'clr.w','%d1');_ins(e,'move.w','#255,%d2');_mark(e,'officer')
    _ins(e,'move.b','(%a0, %d2.w),%d1',4);_ins(e,'cmp.w','%d1,%d0');_branch(e,'beq.w','found');_ins(e,'dbra','%d2,'+_label(e,'officer'),4)
    _mark(e,'found');_ins(e,'lea.l','0xcc00:w,%a0');_ins(e,'clr.w','%d1');_ins(e,'move.b','(%a0, %d2.w),%d1',4);_ins(e,'lea.l','0xf427:w,%a0');_ins(e,'move.b','(%a0, %d1.w),%d1',4)


def _l_choose_selected_roster_resource_action(e,r):
    _call(e,'selected_roster_strength');_ins(e,'cmpi.l','#8000,%d0');_branch(e,'bcs.w','decline');_call(e,'selected_roster_troop_shortfall');_branch(e,'bcs.w','decline')
    _command(e,7);_branch(e,'bra.w','return');_mark(e,'decline');_command(e,8)


def _roster_sum(e):
    _ins(e,'lea.l','0xf72a:w,%a0');_ins(e,'lea.l','0xc800:w,%a1');_ins(e,'moveq','#0,%d0');_mark(e,'officer')
    _ins(e,'move.w','(%a0)+,%d1');_branch(e,'bmi.w','return');_ins(e,'lsl.w','#2,%d1');_ins(e,'add.l','(%a1, %d1.w),%d0',4);_branch(e,'bra.b','officer')


def _l_selected_roster_strength(e,r): _roster_sum(e)


def _l_selected_roster_troop_shortfall(e,r):
    _ins(e,'lea.l','0xf72a:w,%a0');_ins(e,'lea.l','0xb000:w,%a1');_ins(e,'lea.l','0xb200:w,%a2');_mark(e,'officer')
    _ins(e,'move.w','(%a0)+,%d0');_branch(e,'bmi.w','complete');_ins(e,'lsl.w','#1,%d0');_ins(e,'move.w','(%a1, %d0.w),%d1',4)
    _ins(e,'cmp.w','(%a2, %d0.w),%d1',4);_branch(e,'bls.b','officer');_carry(e,1);_branch(e,'bra.w','return');_mark(e,'complete');_carry(e,0)


def _l_choose_active_adjacent_group_action(e,r): _candidate_action(e,'collect_active_adjacent_groups',9,11)


def _l_collect_active_adjacent_groups(e,r):
    _ins(e,'movea.l','0xff382c:l,%a0');_ins(e,'clr.w','%d0');_ins(e,'move.b','1(%a0),%d0',4)
    _ins(e,'move.w','%d0,%d1');_ins(e,'subq.w','#1,%d1');_ins(e,'move.w','%d0,%d2');_ins(e,'addq.w','#1,%d2');_ins(e,'clr.w','%d3');_ins(e,'move.b','2(%a0),%d3',4)
    _ins(e,'move.w','%d3,%d4');_ins(e,'subq.w','#1,%d4');_ins(e,'move.w','%d3,%d5');_ins(e,'addq.w','#1,%d5')
    _ins(e,'lsl.w','#8,%d1');_ins(e,'move.b','%d3,%d1');_ins(e,'lsl.w','#8,%d2');_ins(e,'move.b','%d3,%d2');_ins(e,'lsl.w','#8,%d0')
    _ins(e,'move.w','%d0,%d3');_ins(e,'move.b','%d4,%d0');_ins(e,'move.b','%d5,%d3');_ins(e,'lea.l','0xd300:w,%a1');_ins(e,'lea.l','0x9000:w,%a2');_ins(e,'clr.w','%d4')
    _ins(e,'lea.l','0xe710:w,%a3');_ins(e,'move.w','0xf376:w,%d7');_ins(e,'lsl.w','#1,%d7');_ins(e,'move.w','(%a3, %d7.w),%d7',4)
    _mark(e,'packet');_ins(e,'move.b','(%a2),%d5');_ins(e,'andi.w','#15,%d5');_branch(e,'beq.w','terminator');_ins(e,'clr.w','%d6');_ins(e,'move.b','4(%a2),%d6',4)
    _ins(e,'cmp.b','0xf377:w,%d6');_branch(e,'beq.w','next');_ins(e,'btst.l','%d6,%d7');_branch(e,'bne.w','next')
    _ins(e,'move.b','1(%a2),%d6',4);_ins(e,'lsl.w','#8,%d6');_ins(e,'move.b','2(%a2),%d6',4)
    for register in ('%d0','%d1','%d2'):
        _ins(e,'cmp.w',register+',%d6');_branch(e,'beq.w','append')
    _ins(e,'cmp.w','%d3,%d6');_branch(e,'bne.w','next');_mark(e,'append');_ins(e,'move.w','%d4,(%a1)+')
    _mark(e,'next');_ins(e,'lea.l','13(%a2, %d5.w),%a2',4);_ins(e,'addi.w','#13,%d5');_ins(e,'add.w','%d5,%d4');_branch(e,'bra.b','packet');_mark(e,'terminator');_ins(e,'move.w','#65535,(%a1)')


def _l_choose_active_strength_action(e,r):
    _call(e,'selected_roster_comparison_strength');_call(e,'measure_lightest_active_candidate');_ins(e,'cmp.l','%d0,%d1');_branch(e,'bhi.w','decline')
    _ins(e,'move.w','%d2,0xf744:w');_command(e,10);_branch(e,'bra.w','return');_mark(e,'decline');_command(e,11)


def _l_selected_roster_comparison_strength(e,r): _roster_sum(e)


def _l_measure_lightest_active_candidate(e,r):
    _ins(e,'lea.l','0xd300:w,%a0');_ins(e,'lea.l','0xc800:w,%a2');_ins(e,'moveq','#-1,%d1');_mark(e,'candidate')
    _ins(e,'move.w','(%a0)+,%d3');_branch(e,'bmi.w','return');_ins(e,'lea.l','0x9000:w,%a1');_ins(e,'adda.w','%d3,%a1');_ins(e,'move.b','(%a1),%d4')
    _ins(e,'andi.w','#15,%d4');_ins(e,'subq.w','#1,%d4');_ins(e,'moveq','#0,%d5');_mark(e,'member');_ins(e,'clr.w','%d6')
    _ins(e,'move.b','13(%a1, %d4.w),%d6',4);_ins(e,'lsl.w','#2,%d6');_ins(e,'add.l','(%a2, %d6.w),%d5',4);_ins(e,'dbra','%d4,'+_label(e,'member'),4)
    _ins(e,'cmp.l','%d1,%d5');_branch(e,'bcc.b','candidate');_ins(e,'move.l','%d5,%d1');_ins(e,'move.w','%d3,%d2');_branch(e,'bra.b','candidate')


def _l_schedule_active_comparison_dialogue(e,r):
    _ins(e,'move.w','0xf744:w,0xefbe:w',6);_ins(e,'clr.w','0xefc6:w')
    for value,address in ((20,'0xf65a'),(181,'0xf38c'),(520,'0xf612'),(4,'0xf362'),(1,'0xf576')): _ins(e,'move.w',f'#{value},{address}:w')
    _command(e,65535)


def _l_clear_active_contact_command(e,r): _command(e,65535)
def _l_clear_active_idle_command(e,r): _command(e,65535)


def _lowerer(name):
    implementation = globals()['_l_'+name]
    def lower(e, rules):
        implementation(e,rules)
        _mark(e,'return')
    return lower


def compile_actions(source):
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    result = lower_declared(records, ACTIONS_BINDINGS,
                            {name:_lowerer(name) for name in DECLARATIONS})
    if (result['allocated_bytes'],result['instructions'],len(result['units'])) != (3542,1052,59):
        raise CompileError('all59 complete action bodies required')
    return result


# Fully executable semantic admission specification, not target instructions.
FLOW = r'''"""Live campaign action selection and packet/contact resource policy.

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
'''

SLOTS = {'measure_packet_ready_strength': {5000: ('ready_strength', 1, 2147483647)}}

def _semantic_declarations():
    tree = ast.parse(FLOW)
    approved = {}
    declarations = {}
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            approved.setdefault(node.module, set()).update(alias.name for alias in node.names)
        elif isinstance(node, ast.FunctionDef):
            signature = ast.unparse(node.args)
            result = ast.unparse(node.returns)
            body = '\n'.join(ast.unparse(statement) for statement in node.body)
            declarations[node.name] = dict(signature=signature, returns=result, flow=body,
                slots=SLOTS.get(node.name, {}))
    return declarations, approved

DECLARATIONS, APPROVED = _semantic_declarations()
