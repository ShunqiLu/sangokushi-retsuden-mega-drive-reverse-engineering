"""Finite typed formation AST effects to ordinary 68000 operations.

The target layout is a compatibility constraint, not an input binary. Complete
semantic flows are admitted below; unsupported edits fail before lowering.
Common operation families share instruction selection instead of storing an
old assembly text or an opcode/byte payload.
"""
import ast

from .compiler_common import CompileError, lower_declared, semantic_functions
from .target import FORMATION_BINDINGS


def ram(e, role, register, *, long_address=False):
    bases = {
        'positions': 0xA150, 'primary_roster': 0xA550, 'secondary_roster': 0xA5A4,
        'troops': 0xC800, 'scratch': 0xD300, 'cells': 0xD310, 'owners': 0xF428,
        'variant': 0x9FFF, 'head': 0xA027, 'rulers': 0xE640, 'b200': 0xB200,
        'b400': 0xB400, 'b600': 0xB600, 'readiness': 0xC300,
        'primary_orders': 0xAF82, 'secondary_orders': 0xAF96, 'aux': 0xEA88,
    }
    base = bases[role]
    e.ins('lea.l', f'0x{base:x}:'+('l' if long_address else 'w')+',%'+register,
          6 if long_address else 4)


def readonly(e, base, register):
    e.ins('lea.l', f'0x{base:x}:l,%'+register, 6)


def pc_source(e, base, register):
    displacement = base - (e.pc + 2)
    if not -32768 <= displacement <= 32767:
        raise CompileError('signed PC source displacement required')
    e.ins('lea.l', str(displacement)+'(%pc),%'+register, 4)


def branch(e, condition, target, short=False):
    e.ins(condition + ('.b' if short else '.w'), target, 2 if short else 4)


def call(e, name, *, short=False, absolute=False):
    if absolute:
        e.ins('jsr', name+':l', 6)
    else:
        e.ins('bsr.b' if short else 'bsr.w', name, 2 if short else 4)


def random(e):
    call(e, 'step_random', absolute=True)
    e.ins('andi.l', '#0xffff,%d0', 6)


def carry(e, enabled):
    e.ins('ori.w' if enabled else 'andi.w', '#0x1,%sr' if enabled else '#0xfffe,%sr', 4)


def outcome_tail(e, selected, finish):
    carry(e, True)
    branch(e, 'bra', finish)
    e.label(selected)
    carry(e, False)
    e.label(finish)


def sum_roster(e, rules):
    ram(e, 'primary_roster', 'a0'); ram(e, 'troops', 'a1')
    e.ins('clr.w', '%d2'); e.ins('moveq', '#0,%d3')
    loop, done = e.fresh('members'), e.fresh('done')
    e.label(loop); e.ins('move.w', '(%a0)+,%d5'); branch(e, 'bmi', done)
    e.ins('addq.w', '#0x2,%d2'); e.ins('lsl.w', '#0x2,%d5')
    e.ins('add.l', '(%a1,%d5.w),%d3', 4); branch(e, 'bra', loop, True); e.label(done)


def city_assignment(e, rules):
    e.ins('move.w', '#'+str(rules.get('city_latch',39))+',%d4', 4)
    e.ins('move.w', '0xf68c:w,%d0', 4); ram(e, 'owners', 'a0')
    loop, again, done = e.fresh('city'), e.fresh('again'), e.fresh('done')
    e.label(loop); e.ins('cmp.b', '(%a0,%d4.w),%d0', 4); branch(e, 'bne', again)
    carry(e, True); branch(e, 'bra', done); e.label(again)
    e.ins('dbra', '%d4,'+loop, 4); carry(e, False); e.label(done)


def total_gate(e, rules, mode):
    yes, no, done = e.fresh('yes'), e.fresh('no'), e.fresh('done')
    if mode in ('first_relative', 'second_relative'):
        first = mode == 'first_relative'
        e.ins('move.l', ('0xf69e' if first else '0xf6a2')+':w,%d0', 4)
        e.ins('cmp.l', ('0xf6a2' if first else '0xf69e')+':w,%d0', 4)
        branch(e, 'bcc', no)
        e.ins('cmp.l', ('0xf768' if first else '0xf76c')+':w,%d0', 4)
        branch(e, 'bcc', no)
    else:
        e.ins('move.l', '0xf6a2:w,%d0', 4)
        e.ins('cmp.l', '0xf76c:w,%d0', 4)
        if mode == 'threshold':
            branch(e, 'bcc', no)
        else:
            branch(e, 'bcs', no)
            if mode == 'single':
                e.ins('tst.w', '0xa552:w', 4); branch(e, 'bpl', no)
            else:
                e.ins('tst.w', '0xa5a6:w', 4); branch(e, 'bmi', yes)
                e.ins('tst.w', '0xa5a8:w', 4); branch(e, 'bmi', yes)
                e.ins('tst.w', '0xa5aa:w', 4); branch(e, 'bpl', no)
    e.label(yes); outcome_tail(e, no, done)


def staging_bounds(e, rules):
    special, x_ok, right_ok, low_side, compare, no, done = [e.fresh(x) for x in ('special','x_ok','right_ok','low_side','compare','no','done')]
    e.ins('move.w', '0xf68a:w,%d6', 4); readonly(e, 0xAE2F6, 'a0'); e.ins('lsl.w', '#0x2,%d6')
    e.ins('cmpi.w', '#0x5c,%d6', 4); branch(e, 'beq', special)
    e.ins('move.w', '(%a0,%d6.w),%d2', 4); e.ins('move.w','%d2,%d3')
    left_cap,right_cap=e.fresh('left_cap'),e.fresh('right_cap')
    e.ins('subi.w', '#0x1000,%d2',4); branch(e,'bcs',left_cap)
    e.ins('cmpi.w','#0xc00,%d2',4); branch(e,'bcc',x_ok);e.label(left_cap);e.ins('move.w','#0xc00,%d2',4);e.label(x_ok)
    e.ins('addi.w','#0x1000,%d3',4);branch(e,'bcs',right_cap)
    e.ins('cmpi.w','#0x6400,%d3',4);branch(e,'bls',right_ok);e.label(right_cap);e.ins('move.w','#0x6400,%d3',4);e.label(right_ok)
    e.ins('move.w','0x2(%a0,%d6.w),%d4',4);e.ins('move.w','%d4,%d5')
    e.ins('cmpi.w','#0x5000,%d4',4);branch(e,'bcs',low_side)
    e.ins('subi.w','#0x3800,%d4',4);branch(e,'bra',compare);e.label(low_side)
    e.ins('addi.w','#0x3800,%d5',4);branch(e,'bra',compare);e.label(special)
    e.ins('move.w','(%a0,%d6.w),%d2',4);e.ins('move.w','%d2,%d3');e.ins('subi.w','#0x3400,%d3',4)
    e.ins('move.w','0x2(%a0,%d6.w),%d4',4);e.ins('move.w','%d4,%d5')
    e.ins('subi.w','#0xc00,%d4',4);e.ins('addi.w','#0xc00,%d5',4);e.label(compare)
    for source, bound, condition in (('d0','d2','bcs'),('d0','d3','bhi'),('d1','d4','bcs'),('d1','d5','bhi')):
        e.ins('cmp.w','%'+bound+',%'+source);branch(e,condition,no)
    outcome_tail(e,no,done)


def sample_staging(e, rules):
    e.ins('sub.w','%d2,%d3');random(e);e.ins('mulu.w','%d3,%d0');e.ins('swap','%d0');e.ins('add.w','%d0,%d2')
    e.ins('sub.w','%d4,%d5');e.ins('subi.w','#0xc00,%d5',4);random(e);e.ins('mulu.w','%d5,%d0');e.ins('swap','%d0')
    readonly(e,0xAE2F6,'a0');e.ins('move.w','0xf68a:w,%d1',4);e.ins('lsl.w','#0x2,%d1')
    lower,done=e.fresh('lower'),e.fresh('done')
    e.ins('cmpi.w','#0x5000,0x2(%a0,%d1.w)',6);branch(e,'bcs',lower)
    e.ins('add.w','%d0,%d4');branch(e,'bra',done);e.label(lower)
    e.ins('add.w','%d0,%d4');e.ins('addi.w','#0xc00,%d4',4);e.label(done)


def anchor(e, rules, horizontal, special_x, special_y):
    special,lower,done=e.fresh('special'),e.fresh('lower'),e.fresh('done')
    readonly(e,0xAE2F6,'a0');e.ins('move.w','0xf68a:w,%d0',4);e.ins('lsl.w','#0x2,%d0');e.ins('cmpi.w','#0x5c,%d0',4);branch(e,'beq',special)
    e.ins('move.w','(%a0,%d0.w),%d2',4);e.ins('addi.w' if horizontal>0 else 'subi.w',f'#{abs(horizontal):#x},%d2',4)
    e.ins('move.w','0x2(%a0,%d0.w),%d4',4);e.ins('cmpi.w','#0x5000,%d4',4);branch(e,'bcs',lower)
    e.ins('subi.w','#0xf80,%d4',4);branch(e,'bra',done);e.label(lower);e.ins('addi.w','#0xf80,%d4',4);branch(e,'bra',done)
    e.label(special);e.ins('move.w','(%a0,%d0.w),%d2',4);e.ins('subi.w',f'#{special_x:#x},%d2',4)
    e.ins('move.w','0x2(%a0,%d0.w),%d4',4);e.ins('addi.w' if special_y>0 else 'subi.w',f'#{abs(special_y):#x},%d4',4);e.label(done)


def region(e, rules, direction):
    sample,done=e.fresh('sample'),e.fresh('done')
    e.ins('move.w','(%a0,%d2.w),%d3',4)
    if direction in ('east','west'):
        e.ins('move.w','%d3,%d4');e.ins('addi.w' if direction=='east' else 'subi.w','#0x3800,%'+('d4' if direction=='east' else 'd3'),4)
    elif direction in ('lower','upper'):
        e.ins('move.w','%d3,%d4');e.ins('subi.w','#0xc00,%d3',4);e.ins('addi.w','#0xc00,%d4',4)
    elif direction=='east_flank':
        capped,cap=e.fresh('capped'),e.fresh('cap');e.ins('addi.w','#0xf80,%d3',4);e.ins('move.w','%d3,%d4');e.ins('addi.w','#0x2080,%d4',4)
        branch(e,'bcs',cap);e.ins('cmpi.w','#0x6400,%d4',4);branch(e,'bls',capped);e.label(cap);e.ins('move.w','#0x6400,%d4',4);e.label(capped)
    else:
        capped,cap=e.fresh('capped'),e.fresh('cap');e.ins('move.w','%d3,%d4');e.ins('subi.w','#0xf80,%d4',4);e.ins('subi.w','#0x3000,%d3',4)
        branch(e,'bcs',cap);e.ins('cmpi.w','#0xc00,%d3',4);branch(e,'bcc',capped);e.label(cap);e.ins('move.w','#0xc00,%d3',4);e.label(capped)
    e.ins('move.w','0x2(%a0,%d2.w),%d5',4)
    if direction in ('east','west'):
        low,high=e.fresh('low'),e.fresh('high');e.ins('move.w','%d5,%d6');e.ins('subi.w','#0x1000,%d5',4)
        e.ins('cmpi.w','#0xc00,%d5',4);branch(e,'bcc',low);e.ins('move.w','#0xc00,%d5',4);e.label(low)
        e.ins('addi.w','#0x1000,%d6',4);e.ins('cmpi.w','#0x9400,%d6',4);branch(e,'bls',high);e.ins('move.w','#0x9400,%d6',4);e.label(high)
        # East policy is genuinely lowered from its three source comparisons.
        # Registers/order remain the compatibility allocation, not the policy.
        conditions = rules['region_policy_failures']
        for bound, source, condition in zip(
                ('d4' if direction == 'east' else 'd3', 'd5', 'd6'),
                ('d0', 'd1', 'd1'), conditions):
            e.ins('cmp.w', '%'+bound+',%'+source)
            branch(e, condition, sample)
        carry(e,True);branch(e,'bra',done);e.label(sample);random(e);e.ins('mulu.w','#0x2000,%d0',4);e.ins('swap','%d0')
        if direction=='east':e.ins('add.w','%d0,%d3');e.ins('addi.w','#0xc00,%d3',4)
        else:e.ins('move.w','%d4,%d3');e.ins('sub.w','%d0,%d3');e.ins('subi.w','#0xc00,%d3',4)
        e.ins('sub.w','%d5,%d6');random(e);e.ins('mulu.w','%d6,%d0');e.ins('swap','%d0');e.ins('add.w','%d0,%d5')
    elif direction in ('lower','upper'):
        e.ins('move.w','%d5,%d6');e.ins('subi.w' if direction=='lower' else 'addi.w','#0x3400,%'+('d5' if direction=='lower' else 'd6'),4)
        for bound,source,condition in zip(('d3','d4','d5','d6'), ('d0','d0','d1','d1'), rules['region_policy_failures']):
            e.ins('cmp.w','%'+bound+',%'+source);branch(e,condition,sample)
        carry(e,True);branch(e,'bra',done);e.label(sample);random(e);e.ins('mulu.w','#0x1800,%d0',4);e.ins('swap','%d0');e.ins('add.w','%d0,%d3')
        random(e);e.ins('mulu.w','#0x1800,%d0',4);e.ins('add.w','%d0,%d5');carry(e,False)
    else:
        below=e.fresh('below');e.ins('cmpi.w','#0x5000,%d5',4);branch(e,'bcs',below);e.ins('move.w','%d5,%d6');e.ins('subi.w','#0x3800,%d5',4)
        for bound,source,condition in zip(('d3','d4','d5','d6'), ('d0','d0','d1','d1'), rules['region_policy_failures']):
            e.ins('cmp.w','%'+bound+',%'+source);branch(e,condition,sample)
        carry(e,True);branch(e,'bra',done);e.label(below);e.ins('move.w','%d5,%d6');e.ins('addi.w','#0x3800,%d6',4)
        for bound,source,condition in zip(('d3','d4','d5','d6'), ('d0','d0','d1','d1'), rules['region_policy_failures']):
            e.ins('cmp.w','%'+bound+',%'+source);branch(e,condition,sample)
        carry(e,True);branch(e,'bra',done);e.label(sample);random(e);e.ins('sub.w','%d3,%d4');e.ins('mulu.w','%d4,%d0');e.ins('swap','%d0');e.ins('add.w','%d0,%d3')
        if direction=='east_flank':e.ins('addq.w','#0x1,%d3')
        random(e);e.ins('mulu.w','#0x2000,%d0',4);e.ins('swap','%d0');e.ins('add.w','%d0,%d5');carry(e,False)
    e.label(done)


def region_wrapper(e, rules, direction, x_shift, y_shift, *, flank=False, third=False):
    x_shift = rules.get('center_horizontal', x_shift)
    y_shift = rules.get('center_vertical', y_shift)
    name='sample_or_accept_'+direction+'_formation_region' if direction in ('east','west','lower','upper') else 'sample_or_accept_'+direction+'_region'
    call(e,name);done=e.fresh('done');branch(e,'bcc',done)
    if flank:
        below=e.fresh('below');e.ins('cmpi.w','#0x5000,0x2(%a0,%d2.w)',6);branch(e,'bcs',below)
        if direction=='west_flank':e.ins('move.w','%d4,%d3')
        e.ins('move.w','%d6,%d5');e.ins('addi.w' if third else 'subi.w','#0x400,%d5',4);branch(e,'bra',done);e.label(below)
        if direction=='west_flank':e.ins('move.w','%d4,%d3')
        e.ins('subi.w' if third else 'addi.w','#0x400,%d5',4)
    else:
        if direction=='west':e.ins('move.w','%d4,%d3')
        e.ins('addi.w' if x_shift>0 else 'subi.w',f'#{abs(x_shift):#x},%d3',4)
        e.ins('addi.w',f'#{y_shift:#x},%d5',4)
    e.label(done)


def compare_shifted(e, rules):
    e.ins('movem.l','%d0-%d1,-(%a7)',4);call(e,'collect_contacts_in_speed_radius');e.ins('tst.w','0xd300:w',4)
    no,done=e.fresh('no'),e.fresh('done');branch(e,'bmi',no);call(e,'select_weakest_contact_strength')
    e.ins('move.w','%d7,%d0');call(e,'weighted_training_factor',absolute=True);e.ins('lsl.w','#0x2,%d0')
    e.ins('move.l','0x2(%a1,%d0.w),%d0',4);e.ins('mulu.w','%d1,%d0');e.ins('cmp.l','%d0,%d2');branch(e,'bhi',no)
    outcome_tail(e,no,done);e.ins('movem.l','(%a7)+,%d0-%d1',4)


def nearest_deployment(e, rules):
    ram(e,'positions','a0');ram(e,'scratch','a1');readonly(e,0xABDA8,'a2');ram(e,'variant','a3')
    e.ins('move.w','0xf68a:w,%d0',4);e.ins('clr.w','%d1');e.ins('move.b','(%a3,%d0.w),%d1',4)
    e.ins('lsl.w','#0x5,%d0');e.ins('lsl.w','#0x1,%d1');e.ins('add.w','%d1,%d0');e.ins('clr.w','%d2');e.ins('move.b','(%a2,%d0.w),%d2',4)
    e.ins('lsl.w','#0x3,%d2');e.ins('lsl.w','#0x7,%d2');e.ins('clr.w','%d3');e.ins('move.b','0x1(%a2,%d0.w),%d3',4)
    e.ins('lsl.w','#0x3,%d3');e.ins('lsl.w','#0x7,%d3');e.ins('move.w','#0xffff,%d0',4)
    loop,dx,dy,done=[e.fresh(x) for x in ('loop','dx','dy','done')]
    e.label(loop);e.ins('move.w','(%a1)+,%d4');branch(e,'bmi',done);e.ins('lsl.w','#0x2,%d4')
    e.ins('move.w','(%a0,%d4.w),%d5',4);e.ins('sub.w','%d2,%d5');branch(e,'bcc',dx);e.ins('neg.w','%d5');e.label(dx)
    e.ins('move.w','0x2(%a0,%d4.w),%d6',4);e.ins('sub.w','%d3,%d6');branch(e,'bcc',dy);e.ins('neg.w','%d6');e.label(dy)
    e.ins('add.w','%d6,%d5');e.ins('cmp.w','%d0,%d5');branch(e,'bcc',loop,True)
    e.ins('move.w','%d5,%d0');e.ins('lsr.w','#0x2,%d4');e.ins('move.w','%d4,%d1');branch(e,'bra',loop,True);e.label(done)


def relative_delta(e, rules):
    done,xdir,ydir=[e.fresh(x) for x in ('done','xdir','ydir')]
    e.ins('move.w','0xf770:w,%d0',4);e.ins('cmpi.w','#0x9,%d0',4);branch(e,'bcc',done);e.ins('lsl.w','#0x2,%d0')
    pc_source(e,0x249F0,'a0');e.ins('move.w','(%a0,%d0.w),%d1',4);e.ins('move.w','0x2(%a0,%d0.w),%d2',4)
    ram(e,'variant','a0');e.ins('move.w','0xf68a:w,%d0',4);e.ins('clr.w','%d3');e.ins('move.b','(%a0,%d0.w),%d3',4)
    readonly(e,0xABDA8,'a0');e.ins('lsl.w','#0x5,%d0');e.ins('lsl.w','#0x1,%d3');e.ins('add.w','%d3,%d0')
    e.ins('clr.w','%d3');e.ins('move.b','(%a0,%d0.w),%d3',4);e.ins('cmpi.w','#0xe,%d3',4);branch(e,'bhi',xdir);e.ins('neg.w','%d1');e.label(xdir)
    e.ins('clr.w','%d4');e.ins('move.b','0x1(%a0,%d0.w),%d4',4);e.ins('cmpi.w','#0x14,%d4',4);branch(e,'bcs',ydir);e.ins('neg.w','%d2');e.label(ydir)
    e.ins('add.w','%d1,%d3');e.ins('add.w','%d2,%d4');e.ins('move.w','%d3,%d2');e.ins('lsl.w','#0x8,%d2');e.ins('andi.w','#0xff,%d4',4);e.ins('or.w','%d4,%d2');e.label(done)


def type6_count(e, rules):
    call(e,'load_battlefield_map_context',absolute=True);ram(e,'secondary_roster','a1');ram(e,'positions','a2');e.ins('clr.w','%d3')
    loop,no,yes,done=[e.fresh(x) for x in ('loop','no','yes','done')];e.label(loop);e.ins('move.w','(%a1)+,%d4');branch(e,'bmi',yes)
    e.ins('lsl.w','#0x2,%d4');e.ins('move.w','(%a2,%d4.w),%d1',4);e.ins('move.w','0x2(%a2,%d4.w),%d2',4)
    call(e,'read_battlefield_terrain_type',absolute=True);e.ins('cmpi.b','#0x6,%d0',4);branch(e,'bne',no)
    e.ins('addq.w','#0x1,%d3');e.ins('cmpi.w','#0x4,%d3',4);branch(e,'bcs',loop,True)
    e.label(no);carry(e,False);branch(e,'bra',done);e.label(yes);carry(e,True);e.label(done)


def initialize(e,rules,second):
    if second:
        call(e,'prepare_second_side_formation_assignment');call(e,'populate_second_side_unset_positions');e.ins('clr.w','0xf6d6:w',4)
    else:
        call(e,'promote_first_side_leader');call(e,'prepare_first_side_formation_assignment');call(e,'populate_first_side_unset_positions')


def assignment(e,rules,second):
    small,copy,done=[e.fresh(x) for x in ('small','copy','done')];base=0xA5A4 if second else 0xA550
    e.ins('tst.w',f'0x{base+4:x}:w',4);branch(e,'bmi',small);e.ins('tst.w',f'0x{base+2:x}:w',4);branch(e,'bmi',small)
    call(e,'sort_side_subroster_by_weighted_troops');branch(e,'bra',copy);e.label(small);e.ins('clr.w','%d2')
    e.ins('tst.w',f'0x{base+2:x}:w',4);branch(e,'bmi',copy);e.ins('addq.w','#0x1,%d2');e.label(copy)
    call(e,'copy_second_side_position_assignment' if second else 'copy_first_side_position_assignment');e.label(done)


def sort_roster(e,rules):
    chosen,collect,scored,outer,inner,noswap=[e.fresh(x) for x in ('chosen','collect','scored','outer','inner','noswap')]
    e.ins('lea.l','0xa5a6:w,%a4',4);e.ins('btst.b','#0x1,0xf6d7:w',6);branch(e,'bne',chosen);e.ins('lea.l','0xa552:w,%a4',4);e.label(chosen)
    e.ins('movea.l','%a4,%a0');ram(e,'scratch','a1');ram(e,'b400','a2');ram(e,'troops','a3');ram(e,'aux','a6');e.ins('clr.w','%d2')
    e.label(collect);e.ins('move.w','(%a0)+,%d0');branch(e,'bmi',scored);e.ins('addq.w','#0x1,%d2');call(e,'weighted_training_factor',absolute=True)
    e.ins('lsl.w','#0x2,%d0');e.ins('move.l','(%a3,%d0.w),%d0',4);e.ins('mulu.w','%d1,%d0');e.ins('move.l','%d0,(%a1)+');branch(e,'bra',collect,True);e.label(scored)
    e.ins('move.w','%d2,%d0');e.ins('subq.w','#0x1,%d0');e.ins('lsl.w','#0x2,%d0');e.ins('clr.w','%d3');ram(e,'scratch','a1');e.ins('movea.l','%a4,%a0')
    e.label(outer);e.ins('move.w','%d0,%d4');e.ins('move.w','%d0,%d1');e.ins('lsr.w','#0x1,%d1');e.ins('move.w','%d3,%d5')
    e.label(inner);e.ins('move.l','(%a1,%d4.w),%d6',4);e.ins('cmp.l','-0x4(%a1,%d4.w),%d6',4);branch(e,rules.get('weighted_swap_failure','bcs'),noswap)
    e.ins('move.l','-0x4(%a1,%d4.w),(%a1,%d4.w)',6);e.ins('move.l','%d6,-0x4(%a1,%d4.w)',4)
    e.ins('move.w','(%a0,%d1.w),%d6',4);e.ins('move.w','-0x2(%a0,%d1.w),(%a0,%d1.w)',6);e.ins('move.w','%d6,-0x2(%a0,%d1.w)',4);e.label(noswap)
    e.ins('subq.w','#0x4,%d4');e.ins('subq.w','#0x2,%d1');e.ins('cmp.w','%d5,%d4');branch(e,'bhi',inner,True)
    e.ins('addq.w','#0x4,%d3');e.ins('cmp.w','%d0,%d3');branch(e,'bcs',outer,True)


def copy_assignment(e,rules,second):
    e.ins('move.w',('0xf68e' if second else '0xf68c')+':w,%d0',4);e.ins('lsl.w','#0x1,%d0')
    if second:
        displacement=0x24BE4-(e.pc+2);e.ins('move.w',str(displacement)+'(%pc,%d0.w),%d0',4)
    else:
        pc_source(e,0x24BE4,'a0');e.ins('move.w','(%a0,%d0.w),%d0',4)
    e.ins('lsl.w','#0x4,%d0');e.ins('add.w','%d2,%d0');e.ins('lsl.w','#0x5,%d0')
    ram(e,'secondary_orders' if second else 'primary_orders','a0');pc_source(e,0x24C00 if second else 0x2546C,'a1');e.ins('adda.w','%d0,%a1')
    for _ in range(10):e.ins('move.w','(%a1)+,(%a0)+')


def populate(e,rules,second):
    call(e,'prepare_second_side_battlefield_choices' if second else 'prepare_first_side_battlefield_choices')
    ram(e,'secondary_roster' if second else 'primary_roster','a0');ram(e,'secondary_orders' if second else 'primary_orders','a1');ram(e,'cells','a2');ram(e,'positions','a3')
    loop,done=e.fresh('member'),e.fresh('done');e.label(loop);e.ins('move.w','(%a0)+,%d0');branch(e,'bmi',done)
    e.ins('lsl.w','#0x2,%d0');e.ins('move.w','(%a1)+,%d1');e.ins('lsl.w','#0x1,%d1');e.ins('tst.w','(%a3,%d0.w)',4);branch(e,rules.get('position_failure','bne'),loop,True)
    for displacement in (0,1):
        e.ins('clr.w','%d2');e.ins('move.b',('' if displacement==0 else '0x1')+'(%a2,%d1.w),%d2',4)
        e.ins('lsl.w','#0x3,%d2');e.ins('lsl.w','#0x7,%d2');e.ins('move.w','%d2,'+('' if displacement==0 else '0x2')+'(%a3,%d0.w)',4)
    branch(e,'bra',loop,True);e.label(done)


def shuffle(e,rules):
    ram(e,'scratch','a2');e.ins('move.w','#0xf,%d2',4);loop,next_=e.fresh('sample'),e.fresh('next');e.label(loop)
    call(e,'step_random',absolute=True);e.ins('move.w','%d0,%d1');e.ins('andi.w','#0xe,%d0',4);e.ins('lsr.w','#0x4,%d1');e.ins('andi.w','#0xe,%d1',4)
    e.ins('tst.w','(%a2,%d0.w)',4);branch(e,'beq',next_);e.ins('tst.w','(%a2,%d1.w)',4);branch(e,'beq',next_)
    e.ins('move.w','(%a2,%d0.w),%d3',4);e.ins('move.w','(%a2,%d1.w),(%a2,%d0.w)',6);e.ins('move.w','%d3,(%a2,%d1.w)',4)
    e.label(next_);e.ins('dbra','%d2,'+loop,4)


def unused_point(e,rules,first):
    ram(e,'scratch','a2');e.ins('move.w','#0x5,%d0' if first else '#0x4,%d0',4)
    copy,scan=e.fresh('copy'),e.fresh('scan');e.label(copy);e.ins('move.w','(%a0)+,(%a2)+');e.ins('dbra','%d0,'+copy,4)
    e.ins('clr.w','(%a2)+')
    if first:e.ins('clr.w','(%a2)')
    else:e.ins('clr.w','(%a2)+');e.ins('clr.w','(%a2)+')
    call(e,'shuffle_nonzero_choice_slots',short=not first);ram(e,'scratch','a2');e.label(scan);e.ins('move.w','(%a2)+,%d0')
    for address in (range(0xD312,0xD322,2) if first else (0xF744,0xF746,0xF748)):
        e.ins('cmp.w',f'0x{address:x}:w,%d0',4);branch(e,'beq',scan,True)
    e.ins('move.w','%d0,(%a1)+')


def second_choices(e,rules):
    readonly(e,0xAD870,'a0');e.ins('move.w','0xf68a:w,%d0',4);e.ins('move.w','%d0,%d1')
    for shift in (1,1,2):e.ins('lsl.w',f'#{shift:#x},%d0');e.ins('add.w','%d1,%d0')
    e.ins('lsl.w','#0x1,%d0');e.ins('adda.w','%d0,%a0');ram(e,'cells','a1');e.ins('move.w','(%a0)+,(%a1)+')
    for latch,zeros in ((4,3),(2,5)):
        ram(e,'scratch','a2');e.ins('move.w',f'#{latch:#x},%d0',4);copy=e.fresh('copy');e.label(copy);e.ins('move.w','(%a0)+,(%a2)+');e.ins('dbra','%d0,'+copy,4)
        for _ in range(zeros):e.ins('clr.w','(%a2)+')
        call(e,'shuffle_nonzero_choice_slots');ram(e,'scratch','a2');e.ins('move.w',f'#{latch:#x},%d0',4);store=e.fresh('store');e.label(store);e.ins('move.w','(%a2)+,(%a1)+');e.ins('dbra','%d0,'+store,4)
    for address in (0xF744,0xF746,0xF748):e.ins('clr.w',f'0x{address:x}:w',4)
    for index in range(4):
        call(e,'choose_unused_second_side_point')
        if index<3:e.ins('move.w',f'%d0,0x{0xF744+index*2:x}:w',4)
        e.ins('move.w',f'%d0,0x{0xFF3EC2+index*2:x}:l',6)


def promote_leader(e,rules):
    choose,scan,low,next_,finish,shift,skip,last,done=[e.fresh(x) for x in ('choose','scan','low','next','finish','shift','skip','last','done')]
    ram(e,'primary_roster','a0');e.ins('move.w','0xf68c:w,%d0',4);e.ins('lsl.w','#0x1,%d0');ram(e,'rulers','a1');e.ins('move.w','(%a1,%d0.w),%d0',4)
    find=e.fresh('find');e.label(find);e.ins('move.w','(%a0)+,%d1');branch(e,'bmi',choose);e.ins('cmp.w','%d0,%d1');branch(e,'bne',find,True);branch(e,'bra',finish)
    e.label(choose);ram(e,'primary_roster','a0');ram(e,'readiness','a1');ram(e,'b200','a2');ram(e,'b600','a3');e.ins('clr.w','%d1');e.ins('clr.w','%d2')
    e.label(scan);e.ins('move.w','(%a0)+,%d6');branch(e,'bmi',finish);e.ins('move.b','(%a1,%d6.w),%d3',4);e.ins('cmpi.b','#'+hex(rules.get('readiness_limit',90))+',%d3',4);branch(e,rules.get('readiness_class_failure','bcc'),low)
    e.ins('cmp.b','%d1,%d3');branch(e,rules.get('readiness_rank_failure','bcs'),scan,True);e.ins('move.b','%d3,%d1');e.ins('move.w','%d6,%d0');branch(e,'bra',scan,True)
    e.label(low);e.ins('move.w','%d6,%d4');e.ins('lsl.w','#0x1,%d4');e.ins('move.w','(%a2,%d4.w),%d5',4);e.ins('add.w','(%a3,%d4.w),%d5',4);e.ins('cmp.w','%d2,%d5');branch(e,rules.get('strength_rank_failure','bcs'),scan,True)
    e.ins('move.w','%d6,%d0');e.ins('move.w','%d3,%d1');e.ins('move.w','%d5,%d2');branch(e,'bra',scan,True)
    e.label(finish);ram(e,'head','a1');e.ins('move.w','0xf68a:w,%d1',4);e.ins('move.b','%d0,(%a1,%d1.w)',4)
    ram(e,'primary_roster','a0');e.ins('movea.l','%a0,%a1');e.ins('move.w','%d0,%d2');e.label(shift);e.ins('move.w','(%a0)+,%d1');branch(e,'bmi',last);e.ins('cmp.w','%d0,%d1');branch(e,'beq',shift,True)
    e.ins('move.w','%d2,(%a1)+');e.ins('move.w','%d1,%d2');branch(e,'bra',shift,True);e.label(last);e.ins('cmp.w','%d0,%d1');branch(e,'beq',done);e.ins('move.w','%d2,(%a1)');e.label(done)


def first_choices(e,rules):
    readonly(e,0xAC75E,'a0');e.ins('move.w','0xf68a:w,%d0',4);e.ins('move.w','%d0,%d1')
    for shift in (1,2,1):e.ins('lsl.w',f'#{shift:#x},%d0');e.ins('add.w','%d1,%d0')
    e.ins('lsl.w','#0x2,%d0');e.ins('adda.w','%d0,%a0');ram(e,'cells','a1');e.ins('move.w','0xf61c:w,%d0',4);e.ins('andi.w','#0x2,%d0',4);e.ins('move.w','(%a0,%d0.w),(%a1)+',4)
    choice=e.fresh('choice');e.ins('tst.w','%d0');branch(e,'bne',choice);e.ins('addq.w','#0x1,%d0');e.label(choice);e.ins('move.w','0xf68a:w,%d1',4);ram(e,'variant','a6');e.ins('move.b','%d0,(%a6,%d1.w)',4)
    e.ins('addq.w','#0x4,%a0');e.ins('movea.l','%a1,%a2');e.ins('move.w','#0x7,%d0',4);clear=e.fresh('clear');e.label(clear);e.ins('clr.w','(%a2)+');e.ins('dbra','%d0,'+clear,4)
    for _ in range(8):call(e,'choose_unused_first_side_point')
    special,fold=e.fresh('special'),e.fresh('fold');e.ins('cmpi.w','#0x17,0xf68a:w',6);branch(e,'beq',special)
    ram(e,'scratch','a2');e.ins('move.w','#0x3,%d0',4);copy=e.fresh('copy');e.label(copy);e.ins('clr.w','0x8(%a2)',4);e.ins('move.w','(%a0)+,(%a2)+');e.ins('dbra','%d0,'+copy,4);call(e,'shuffle_nonzero_choice_slots');branch(e,'bra',fold)
    e.label(special);ram(e,'scratch','a2');e.ins('move.w','#0x7,%d0',4);same=e.fresh('same');e.label(same);e.ins('clr.w','(%a2)');e.ins('dbra','%d0,'+same,4)
    selected=e.fresh('selected');e.ins('cmpi.b','#0x14,0xd311:w',6);branch(e,'bcs',selected);e.ins('adda.w','#0x4,%a0',4);e.label(selected)
    e.ins('move.w','(%a0),0xd300:w',4);e.ins('move.w','0x2(%a0),0xd302:w',6);call(e,'shuffle_nonzero_choice_slots');e.label(fold)
    e.ins('move.w','0xd300:w,(%a1)+',4);e.ins('move.w','0xd300:w,0xff3eca:l',8)
    e.ins('move.w','0xd302:w,(%a1)',4);e.ins('move.w','0xd302:w,0xff3ecc:l',8)


def _lowerers():
    out = {
        'sum_first_side_roster_troops':sum_roster,'test_force_has_city_assignment':city_assignment,
        'test_point_in_battlefield_staging_rectangle':staging_bounds,'sample_battlefield_staging_rectangle':sample_staging,
        'compare_actor_shifted_troop_word_to_weakest_contact':compare_shifted,
        'select_contact_nearest_deployment_anchor':nearest_deployment,'read_formation_relative_position_delta':relative_delta,
        'test_second_roster_type6_count_below_four':type6_count,'sort_side_subroster_by_weighted_troops':sort_roster,
        'shuffle_nonzero_choice_slots':shuffle,'prepare_second_side_battlefield_choices':second_choices,
        'prepare_first_side_battlefield_choices':first_choices,'promote_first_side_leader':promote_leader,
    }
    for name,mode in (('test_second_side_total_with_single_first_roster','single'),('test_second_side_total_with_small_second_roster','small'),('test_second_side_relative_total_shortfall','second_relative'),('test_first_side_relative_total_shortfall','first_relative'),('test_second_side_threshold_shortfall','threshold')):
        out[name]=lambda e,r,mode=mode:total_gate(e,r,mode)
    for name,args in (('read_first_side_staging_anchor',(-1024,4096,-1152)),('read_second_side_staging_anchor',(1024,4096,1152)),('read_outer_east_staging_anchor',(3072,3968,3072)),('read_outer_west_staging_anchor',(-3072,3968,-3072))):
        out[name]=lambda e,r,args=args:anchor(e,r,*args)
    for direction in ('east','west','lower','upper','east_flank','west_flank'):
        name='sample_or_accept_'+direction+('_formation_region' if direction in ('east','west','lower','upper') else '_region')
        out[name]=lambda e,r,direction=direction:region(e,r,direction)
    specs={
        'choose_east_center_first_formation_point':('east',3968,3072,False,False),
        'choose_west_center_first_formation_point':('west',-3968,3072,False,False),
        'choose_east_flank_first_formation_point':('east_flank',0,0,True,False),
        'choose_lower_center_first_formation_point':('lower',4096,9344,False,False),
        'choose_east_center_second_formation_point':('east',3968,5120,False,False),
        'choose_west_center_second_formation_point':('west',-3968,5120,False,False),
        'choose_west_flank_second_formation_point':('west_flank',0,0,True,False),
        'choose_upper_center_second_formation_point':('upper',4096,3968,False,False),
        'choose_east_center_third_formation_point':('east',3968,7168,False,False),
        'choose_west_center_third_formation_point':('west',-3968,7168,False,False),
        'choose_west_flank_third_formation_point':('west_flank',0,0,True,True),
        'choose_upper_center_third_formation_point':('upper',2048,3968,False,False),
    }
    for name,(direction,x,y,flank,third) in specs.items():
        out[name]=lambda e,r,direction=direction,x=x,y=y,flank=flank,third=third:region_wrapper(e,r,direction,x,y,flank=flank,third=third)
    for second in (True,False):
        side='second' if second else 'first'
        out['initialize_'+side+'_side_deployment']=lambda e,r,second=second:initialize(e,r,second)
        out['prepare_'+side+'_side_formation_assignment']=lambda e,r,second=second:assignment(e,r,second)
        out['copy_'+side+'_side_position_assignment']=lambda e,r,second=second:copy_assignment(e,r,second)
        out['populate_'+side+'_side_unset_positions']=lambda e,r,second=second:populate(e,r,second)
        out['choose_unused_'+side+'_side_point']=lambda e,r,second=second:unused_point(e,r,not second)
    return out


APPROVED = {'domain': {'uint', 'Cursor', 'GameState', 'Byte', 'checked_state', 'u32', 'Table', 'Long', 'CarryOutcome', 'checked_cursor', 'descending_inclusive', 'checked_table', 'negative_word', 'u8', 'low16', 'u16', 'Word'}, 'contexts_formation': {'BattleBounds', 'RegionInput', 'ShuffleSlots', 'SampledFormationPoint', 'LeaderRank', 'RosterStrength', 'DeploymentViews', 'RegionDecision', 'Point', 'ClosestBattleUnit', 'WeightedDeploymentRoster', 'SampledFlankPoint', 'EastFormationRegion', 'FormationCursors'}, 'business_geometry': {'select_weakest_contact_strength', 'read_battlefield_terrain_type', 'load_battlefield_map_context', 'collect_contacts_in_speed_radius', 'weighted_training_factor'}, (1, 'business_geometry'): {'_contact_difference', 'select_weakest_contact_strength_fields', 'collect_contacts_in_speed_radius_fields'}, (1, 'business_actions'): {'_deployment_compare_byte', '_deployment_carry', '_deployment_terrain_lookup', '_battle_action_map_fields'}}


def compile_formation(source):
    """Finite inline domain helpers plus the existing exact target ABI.

    Six region policies, five deployment policies, the leader readiness limit
    and the first center's WORD shifts feed finite target selection. Every
    other helper/body node is consumed by complete semantic admission;
    unsupported rewrites do not silently lower.
    """
    normalized, policies = _formation_policies(source)
    normalized, deployment_policies = _deployment_policies(normalized)
    helpers = {**INLINE_DECLARATIONS, **FAMILY_INLINE_DECLARATIONS, **DEPLOYMENT_INLINE_DECLARATIONS}
    records = semantic_functions(normalized, {**DECLARATIONS, **FAMILY_DECLARATIONS, **DEPLOYMENT_DECLARATIONS, **helpers}, APPROVED)
    inline = {name: records.pop(name) for name in helpers}
    for policy_name, (target_name, _, helper_names) in REGION_POLICIES.items():
        failures, policy_effect = policies[policy_name]
        record = records[target_name]
        record['rules']['region_policy_failures'] = failures
        record['effects'] += '\nfinite inlining: ' + repr({
            name: policy_effect if name == policy_name else inline[name]['effects']
            for name in helper_names})
    records['choose_east_center_first_formation_point']['effects'] += (
        '\nfinite inlining: ' + inline['translate_accepted_formation_point']['effects'])
    for name, (targets, role, _) in DEPLOYMENT_POLICIES.items():
        failure, effect = deployment_policies[name]
        for target in targets:
            records[target]['rules'][role] = failure
            records[target]['effects'] += '\nactual deployment policy: ' + effect
    records['promote_first_side_leader']['rules']['readiness_limit'] = (
        inline['leader_readiness_uses_byte_rank']['rules']['readiness_limit'])
    # The new body and its reachable supplied helper bodies are all admitted;
    # no old deployment body is consulted during expansion or generation.
    for name in DEPLOYMENT_DECLARATIONS:
        records[name]['effects'] += '\nfinite deployment expansion: ' + repr({
            helper: inline[helper]['effects'] for helper in _deployment_helper_closure(name)})
    records['test_force_has_city_assignment']['rules'].update(inline['test_force_has_city_assignment_fields']['rules'])
    for owner, core in (('sum_first_side_roster_troops', 'sum_first_side_roster_troops_fields'), ('test_force_has_city_assignment', 'test_force_has_city_assignment_fields')):
        records[owner]['effects'] += '\nactual sole order field core: ' + inline[core]['effects']
    records['test_force_has_city_assignment']['effects'] += '\nactual full-SR carry helper: ' + inline['_order_city_assignment_carry']['effects']
    for owner, core in (('test_second_side_total_with_single_first_roster', 'test_second_side_total_with_single_first_roster_fields'), ('test_second_side_total_with_small_second_roster', 'test_second_side_total_with_small_second_roster_fields')):
        records[owner]['effects'] += '\nactual sole strength/roster gate: ' + inline[core]['effects'] + inline['_read_second_side_strength_gate_fields']['effects'] + inline['_battle_roster_gate_carry']['effects']

    for owner in ('compare_actor_shifted_troop_word_to_weakest_contact', 'read_outer_east_staging_anchor', 'select_contact_nearest_deployment_anchor', 'read_formation_relative_position_delta'):
        core = owner + '_fields'
        records[owner]['rules'].update(inline[core]['rules'])
        records[owner]['effects'] += '\nactual position field algorithm: ' + repr({name:inline[name]['effects'] for name in ('_formation_position_frame', '_formation_position_enter', '_formation_position_leave', '_formation_position_carry', 'compare_actor_shifted_troop_word_to_weakest_contact_fields', 'read_outer_east_staging_anchor_fields', 'select_contact_nearest_deployment_anchor_fields', 'read_formation_relative_position_delta_fields')})
    records['read_second_side_staging_anchor']['effects'] += '\nactual second staging anchor: ' + inline['read_second_side_staging_anchor_fields']['effects']
    records['read_first_side_staging_anchor']['effects'] += '\nactual first staging anchor: ' + inline['read_first_side_staging_anchor_fields']['effects']
    for owner in ('sample_or_accept_east_formation_region', 'choose_east_center_first_formation_point', 'sample_or_accept_west_formation_region', 'choose_west_center_first_formation_point', 'sample_or_accept_east_flank_region', 'choose_east_flank_first_formation_point', 'sample_or_accept_lower_formation_region', 'choose_lower_center_first_formation_point'):
        records[owner]['effects'] += '\nsole complete first-region field algorithm: ' + repr({name:inline[name]['effects'] for name in ('_first_region_acceptance_fields', '_first_region_carry', '_first_region_context', '_first_region_draw', '_first_region_legacy_decision', '_first_region_publish', 'choose_east_center_first_formation_point_fields', 'choose_east_flank_first_formation_point_fields', 'choose_first_formation_point_fields', 'choose_lower_center_first_formation_point_fields', 'choose_west_center_first_formation_point_fields', 'read_first_formation_region_fields', 'sample_first_formation_point_fields', 'sample_or_accept_east_flank_region_fields', 'sample_or_accept_east_formation_region_fields', 'sample_or_accept_first_formation_region_fields', 'sample_or_accept_lower_formation_region_fields', 'sample_or_accept_west_formation_region_fields')})
    for owner in ('sample_or_accept_west_flank_region', 'sample_or_accept_upper_formation_region', 'choose_east_center_second_formation_point', 'choose_west_center_second_formation_point', 'choose_west_flank_second_formation_point', 'choose_upper_center_second_formation_point'):
        records[owner]['effects'] += '\nsole shared second-region fields: ' + repr({name:inline[name]['effects'] for name in ('_first_region_acceptance_fields', 'choose_east_center_second_formation_point_fields', 'choose_second_formation_point_fields', 'choose_upper_center_second_formation_point_fields', 'choose_west_center_second_formation_point_fields', 'choose_west_flank_second_formation_point_fields', 'read_first_formation_region_fields', 'sample_first_formation_point_fields', 'sample_or_accept_first_formation_region_fields', 'sample_or_accept_upper_formation_region_fields', 'sample_or_accept_west_flank_region_fields')})
    for owner in ('choose_east_center_third_formation_point', 'choose_west_center_third_formation_point', 'choose_west_flank_third_formation_point', 'choose_upper_center_third_formation_point', 'read_outer_west_staging_anchor', 'test_first_side_relative_total_shortfall', 'test_second_roster_type6_count_below_four', 'test_second_side_threshold_shortfall', 'choose_east_center_second_formation_point', 'choose_west_center_second_formation_point', 'choose_west_flank_second_formation_point', 'choose_upper_center_second_formation_point'):
        records[owner]['effects'] += '\nsole late deployment fields: ' + repr({name:inline[name]['effects'] for name in ('choose_east_center_third_formation_point_fields', 'choose_lateral_formation_point_fields', 'choose_second_formation_point_fields', 'choose_third_formation_point_fields', 'choose_upper_center_third_formation_point_fields', 'choose_west_center_third_formation_point_fields', 'choose_west_flank_third_formation_point_fields', 'read_outer_west_staging_anchor_fields', 'sample_or_accept_first_formation_region_fields', 'test_first_side_relative_total_shortfall_fields', 'test_second_roster_type6_count_below_four_fields', 'test_second_side_threshold_shortfall_fields')})
    for owner in ('initialize_second_side_deployment', 'prepare_second_side_formation_assignment', 'copy_second_side_position_assignment', 'populate_second_side_unset_positions', 'prepare_second_side_battlefield_choices', 'choose_unused_second_side_point'):
        records[owner]['effects'] += '\nsole second deployment fields: ' + repr({name:inline[name]['effects'] for name in ('initialize_second_side_deployment_fields', 'prepare_second_side_formation_assignment_fields', 'copy_second_side_position_assignment_fields', 'populate_second_side_unset_positions_fields', '_second_choice_copy_window_fields', '_second_choice_clear_scratch_fields', '_second_choice_publish_window_fields', '_second_choice_store_selected_fields', 'prepare_second_side_battlefield_choices_fields', 'choose_unused_second_side_point_fields', 'read_first_side_assignment_count_fields')})
    return lower_declared(records, FORMATION_BINDINGS, _lowerers())


DEPLOYMENT_POLICIES = {
    'weighted_neighbor_should_move_forward': (('sort_side_subroster_by_weighted_troops',), 'weighted_swap_failure', ast.GtE),
    'deployment_position_needs_assignment': (('populate_first_side_unset_positions', 'populate_second_side_unset_positions'), 'position_failure', ast.Eq),
    'leader_readiness_uses_byte_rank': (('promote_first_side_leader',), 'readiness_class_failure', ast.Lt),
    'leader_readiness_should_replace': (('promote_first_side_leader',), 'readiness_rank_failure', ast.GtE),
    'leader_strength_should_replace': (('promote_first_side_leader',), 'strength_rank_failure', ast.GtE),
}


def _deployment_policies(source):
    tree = ast.parse(source)
    failures = {ast.Lt: 'bcc', ast.LtE: 'bhi', ast.Gt: 'bls',
                ast.GtE: 'bcs', ast.Eq: 'bne', ast.NotEq: 'beq'}
    policies = {}
    for name, (_, _, canonical) in DEPLOYMENT_POLICIES.items():
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
        if len(functions) != 1:
            raise CompileError('one supplied deployment policy required: ' + name)
        fn = functions[0]
        value = fn.body[-1].value if fn.body and isinstance(fn.body[-1], ast.Return) else None
        if not (isinstance(value, ast.Compare) and len(value.ops) == len(value.comparators) == 1):
            raise CompileError(name + ': one unsigned comparison required')
        operator = type(value.ops[0])
        permitted = (ast.Eq, ast.NotEq) if name == 'deployment_position_needs_assignment' else failures
        if operator not in permitted:
            raise CompileError(name + ': unsupported typed deployment policy')
        policies[name] = failures[operator], ast.dump(fn, include_attributes=False)
        value.ops[0] = canonical()
    return ast.unparse(tree), policies


def _deployment_helper_closure(name):
    declarations = {**DEPLOYMENT_DECLARATIONS, **DEPLOYMENT_INLINE_DECLARATIONS}
    result = set()
    visited = set()
    def visit(current):
        if current in visited:
            return
        visited.add(current)
        for node in ast.walk(ast.parse(declarations[current]['flow'])):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                called = node.func.id
                if called in declarations:
                    if called in DEPLOYMENT_INLINE_DECLARATIONS:
                        result.add(called)
                    visit(called)
    visit(name)
    return tuple(sorted(result))


REGION_POLICIES = {
    'east_formation_contains': (
        'sample_or_accept_east_formation_region', (ast.LtE, ast.GtE, ast.LtE),
        ('read_east_formation_region', 'east_formation_contains', 'sample_east_formation_point')),
    'west_formation_contains': (
        'sample_or_accept_west_formation_region', (ast.GtE, ast.GtE, ast.LtE),
        ('read_west_formation_region', 'west_formation_contains', 'sample_west_formation_point')),
    'lower_formation_contains': (
        'sample_or_accept_lower_formation_region', (ast.GtE, ast.LtE, ast.GtE, ast.LtE),
        ('read_lower_formation_region', 'lower_formation_contains', 'sample_lower_formation_point')),
    'upper_formation_contains': (
        'sample_or_accept_upper_formation_region', (ast.GtE, ast.LtE, ast.GtE, ast.LtE),
        ('read_upper_formation_region', 'upper_formation_contains', 'sample_upper_formation_point')),
    'east_flank_contains': (
        'sample_or_accept_east_flank_region', (ast.GtE, ast.LtE, ast.GtE, ast.LtE),
        ('read_east_flank_region', 'east_flank_contains', 'sample_east_flank_point')),
    'west_flank_contains': (
        'sample_or_accept_west_flank_region', (ast.GtE, ast.LtE, ast.GtE, ast.LtE),
        ('read_west_flank_region', 'west_flank_contains', 'sample_west_flank_point')),
}


def _formation_policies(source):
    if type(source) is not str or len(source) > 300000:
        raise CompileError('bounded explicit Python text required')
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError) as exc:
        raise CompileError('invalid formation Python') from exc
    # False branches for CMP bound,point. Full helper admission checks operand
    # identities, ordering, types and every remaining statement after this pass.
    false_branch = {ast.Lt: 'bcc', ast.LtE: 'bhi', ast.Gt: 'bls',
                    ast.GtE: 'bcs', ast.Eq: 'bne', ast.NotEq: 'beq'}
    policies = {}
    for name, (_, canonical_operators, _) in REGION_POLICIES.items():
        matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
        if len(matches) != 1:
            raise CompileError('one explicit geometry policy required: ' + name)
        policy = matches[0]
        expression = policy.body[-1].value if policy.body and isinstance(policy.body[-1], ast.Return) else None
        if not (isinstance(expression, ast.BoolOp) and isinstance(expression.op, ast.And)
                and len(expression.values) == len(canonical_operators)
                and all(isinstance(item, ast.Compare) and len(item.ops) == 1
                        and len(item.comparators) == 1 for item in expression.values)):
            raise CompileError(name + ': ordered unsigned comparisons joined by and required')
        failures = []
        effect = ast.dump(policy, include_attributes=False)
        for item, canonical in zip(expression.values, canonical_operators):
            if type(item.ops[0]) not in false_branch:
                raise CompileError('unsupported formation geometry comparison')
            failures.append(false_branch[type(item.ops[0])])
            item.ops[0] = canonical()
        policies[name] = tuple(failures), effect
    return ast.unparse(tree), policies


FAMILY_INLINE_DECLARATIONS = {
    "read_west_formation_region": {
        "signature": "state: GameState, context: RegionInput",
        "returns": "BattleBounds",
        "flow": "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\norigin = checked_table(context.origin, state)\nright = origin.word(context.offset)\nleft = u16(right - 14336)\nanchor_y = origin.word(context.offset, 2)\nlower = u16(anchor_y - 4096)\nif lower < 3072:\n    lower = u16(3072)\nupper = u16(anchor_y + 4096)\nif upper > 37888:\n    upper = u16(37888)\nreturn BattleBounds(left, right, lower, upper)\n"
    },
    "west_formation_contains": {
        "signature": "point: Point, region: BattleBounds",
        "returns": "bool",
        "flow": "if type(point) is not Point or type(region) is not BattleBounds:\n    raise ValueError('typed west formation geometry required')\nreturn point.x >= region.left and point.y >= region.lower and (point.y <= region.upper)\n"
    },
    "sample_west_formation_point": {
        "signature": "state: GameState, region: BattleBounds",
        "returns": "SampledFormationPoint",
        "flow": "checked_state(state)\nif type(region) is not BattleBounds:\n    raise ValueError('typed west formation region required')\nsample = state.sample_random() & 65535\nx = u16(region.right - (sample * 8192 >> 16) - 3072)\nspan = u16(region.upper - region.lower)\nsample = state.sample_random() & 65535\nincrement = sample * span >> 16\nraw_y = region.lower + increment\nreturn SampledFormationPoint(Point(x, u16(raw_y)), span, raw_y > 65535)\n"
    },
    "read_lower_formation_region": {
        "signature": "state: GameState, context: RegionInput",
        "returns": "BattleBounds",
        "flow": "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\norigin = checked_table(context.origin, state)\nanchor_x = origin.word(context.offset)\nleft = u16(anchor_x - 3072)\nright = u16(anchor_x + 3072)\nupper = origin.word(context.offset, 2)\nlower = u16(upper - 13312)\nreturn BattleBounds(left, right, lower, upper)\n"
    },
    "lower_formation_contains": {
        "signature": "point: Point, region: BattleBounds",
        "returns": "bool",
        "flow": "if type(point) is not Point or type(region) is not BattleBounds:\n    raise ValueError('typed lower formation geometry required')\nreturn point.x >= region.left and point.x <= region.right and (point.y >= region.lower) and (point.y <= region.upper)\n"
    },
    "sample_lower_formation_point": {
        "signature": "state: GameState, region: BattleBounds",
        "returns": "Point",
        "flow": "checked_state(state)\nif type(region) is not BattleBounds:\n    raise ValueError('typed lower formation region required')\nsample = state.sample_random() & 65535\nx = u16(region.left + (sample * 6144 >> 16))\nsample = state.sample_random() & 65535\ny = u16(region.lower + sample * 6144)\nreturn Point(x, y)\n"
    },
    "read_upper_formation_region": {
        "signature": "state: GameState, context: RegionInput",
        "returns": "BattleBounds",
        "flow": "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\norigin = checked_table(context.origin, state)\nanchor_x = origin.word(context.offset)\nleft = u16(anchor_x - 3072)\nright = u16(anchor_x + 3072)\nlower = origin.word(context.offset, 2)\nupper = u16(lower + 13312)\nreturn BattleBounds(left, right, lower, upper)\n"
    },
    "upper_formation_contains": {
        "signature": "point: Point, region: BattleBounds",
        "returns": "bool",
        "flow": "if type(point) is not Point or type(region) is not BattleBounds:\n    raise ValueError('typed upper formation geometry required')\nreturn point.x >= region.left and point.x <= region.right and (point.y >= region.lower) and (point.y <= region.upper)\n"
    },
    "sample_upper_formation_point": {
        "signature": "state: GameState, region: BattleBounds",
        "returns": "Point",
        "flow": "checked_state(state)\nif type(region) is not BattleBounds:\n    raise ValueError('typed upper formation region required')\nsample = state.sample_random() & 65535\nx = u16(region.left + (sample * 6144 >> 16))\nsample = state.sample_random() & 65535\ny = u16(region.lower + sample * 6144)\nreturn Point(x, y)\n"
    },
    "read_east_flank_region": {
        "signature": "state: GameState, context: RegionInput",
        "returns": "BattleBounds",
        "flow": "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\norigin = checked_table(context.origin, state)\nleft = u16(origin.word(context.offset) + 3968)\nraw_right = left + 8320\nright = u16(raw_right)\nif raw_right > 65535 or right > 25600:\n    right = u16(25600)\nlower = origin.word(context.offset, 2)\nupper = lower\nif lower >= 20480:\n    lower = u16(lower - 14336)\nelse:\n    upper = u16(upper + 14336)\nreturn BattleBounds(left, right, lower, upper)\n"
    },
    "east_flank_contains": {
        "signature": "point: Point, region: BattleBounds",
        "returns": "bool",
        "flow": "if type(point) is not Point or type(region) is not BattleBounds:\n    raise ValueError('typed east flank geometry required')\nreturn point.x >= region.left and point.x <= region.right and (point.y >= region.lower) and (point.y <= region.upper)\n"
    },
    "sample_east_flank_point": {
        "signature": "state: GameState, region: BattleBounds",
        "returns": "SampledFlankPoint",
        "flow": "checked_state(state)\nif type(region) is not BattleBounds:\n    raise ValueError('typed east flank region required')\nsample = state.sample_random() & 65535\nspan = u16(region.right - region.left)\nx = u16(region.left + (sample * span >> 16) + 1)\nsample = state.sample_random() & 65535\ny = u16(region.lower + (sample * 8192 >> 16))\nreturn SampledFlankPoint(Point(x, y), span)\n"
    },
    "read_west_flank_region": {
        "signature": "state: GameState, context: RegionInput",
        "returns": "BattleBounds",
        "flow": "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\norigin = checked_table(context.origin, state)\nanchor_x = origin.word(context.offset)\nright = u16(anchor_x - 3968)\nleft = u16(anchor_x - 12288)\nif anchor_x < 12288 or left < 3072:\n    left = u16(3072)\nlower = origin.word(context.offset, 2)\nupper = lower\nif lower >= 20480:\n    lower = u16(lower - 14336)\nelse:\n    upper = u16(upper + 14336)\nreturn BattleBounds(left, right, lower, upper)\n"
    },
    "west_flank_contains": {
        "signature": "point: Point, region: BattleBounds",
        "returns": "bool",
        "flow": "if type(point) is not Point or type(region) is not BattleBounds:\n    raise ValueError('typed west flank geometry required')\nreturn point.x >= region.left and point.x <= region.right and (point.y >= region.lower) and (point.y <= region.upper)\n"
    },
    "sample_west_flank_point": {
        "signature": "state: GameState, region: BattleBounds",
        "returns": "SampledFlankPoint",
        "flow": "checked_state(state)\nif type(region) is not BattleBounds:\n    raise ValueError('typed west flank region required')\nsample = state.sample_random() & 65535\nspan = u16(region.right - region.left)\nx = u16(region.left + (sample * span >> 16))\nsample = state.sample_random() & 65535\ny = u16(region.lower + (sample * 8192 >> 16))\nreturn SampledFlankPoint(Point(x, y), span)\n"
    }
}


FAMILY_DECLARATIONS = {
    "sample_or_accept_west_formation_region": {
        "signature": "state: GameState, context: RegionInput",
        "returns": "RegionDecision",
        "flow": "region = read_west_formation_region(state, context)\nif west_formation_contains(context.point, region):\n    return RegionDecision(Point(region.left, region.lower), region.right, region.upper, state.carry_result(1))\nsampled = sample_west_formation_point(state, region)\nreturn RegionDecision(sampled.point, region.right, sampled.vertical_span, state.carry_observed(int(sampled.vertical_wrap)))\n"
    },
    "sample_or_accept_lower_formation_region": {
        "signature": "state: GameState, context: RegionInput",
        "returns": "RegionDecision",
        "flow": "region = read_lower_formation_region(state, context)\nif lower_formation_contains(context.point, region):\n    return RegionDecision(Point(region.left, region.lower), region.right, region.upper, state.carry_result(1))\npoint = sample_lower_formation_point(state, region)\nreturn RegionDecision(point, region.right, region.upper, state.carry_result(0))\n"
    },
    "sample_or_accept_upper_formation_region": {
        "signature": "state: GameState, context: RegionInput",
        "returns": "RegionDecision",
        "flow": "region = read_upper_formation_region(state, context)\nif upper_formation_contains(context.point, region):\n    return RegionDecision(Point(region.left, region.lower), region.right, region.upper, state.carry_result(1))\npoint = sample_upper_formation_point(state, region)\nreturn RegionDecision(point, region.right, region.upper, state.carry_result(0))\n"
    },
    "sample_or_accept_east_flank_region": {
        "signature": "state: GameState, context: RegionInput",
        "returns": "RegionDecision",
        "flow": "region = read_east_flank_region(state, context)\nif east_flank_contains(context.point, region):\n    return RegionDecision(Point(region.left, region.lower), region.right, region.upper, state.carry_result(1))\nsampled = sample_east_flank_point(state, region)\nreturn RegionDecision(sampled.point, sampled.horizontal_span, region.upper, state.carry_result(0))\n"
    },
    "sample_or_accept_west_flank_region": {
        "signature": "state: GameState, context: RegionInput",
        "returns": "RegionDecision",
        "flow": "region = read_west_flank_region(state, context)\nif west_flank_contains(context.point, region):\n    return RegionDecision(Point(region.left, region.lower), region.right, region.upper, state.carry_result(1))\nsampled = sample_west_flank_point(state, region)\nreturn RegionDecision(sampled.point, sampled.horizontal_span, region.upper, state.carry_result(0))\n"
    }
}


INLINE_DECLARATIONS = {
    'read_east_formation_region': {
        'signature': 'state: GameState, context: RegionInput',
        'returns': 'EastFormationRegion',
        'flow': '''checked_state(state)
if type(context) is not RegionInput:
    raise ValueError('typed region input required')
origin = checked_table(context.origin, state)
left = origin.word(context.offset)
right = u16(left + 14336)
anchor_y = origin.word(context.offset, 2)
lower = u16(anchor_y - 4096)
if lower < 3072:
    lower = u16(3072)
upper = u16(anchor_y + 4096)
if upper > 37888:
    upper = u16(37888)
return EastFormationRegion(left, right, lower, upper)
''',
    },
    'east_formation_contains': {
        'signature': 'point: Point, region: EastFormationRegion',
        'returns': 'bool',
        'flow': '''if type(point) is not Point or type(region) is not EastFormationRegion:
    raise ValueError('typed east formation geometry required')
return point.x <= region.east_limit and point.y >= region.lower and point.y <= region.upper
''',
    },
    'sample_east_formation_point': {
        'signature': 'state: GameState, region: EastFormationRegion',
        'returns': 'SampledFormationPoint',
        'flow': '''checked_state(state)
if type(region) is not EastFormationRegion:
    raise ValueError('typed east formation region required')
sample = state.sample_random() & 65535
x = u16(region.anchor_x + ((sample * 8192) >> 16) + 3072)
span = u16(region.upper - region.lower)
sample = state.sample_random() & 65535
increment = (sample * span) >> 16
raw_y = region.lower + increment
return SampledFormationPoint(Point(x, u16(raw_y)), span, raw_y > 65535)
''',
    },
    'translate_accepted_formation_point': {
        'signature': 'state: GameState, result: RegionDecision, shift: Point',
        'returns': 'RegionDecision',
        'flow': '''checked_state(state)
if type(result) is not RegionDecision or type(shift) is not Point:
    raise ValueError('typed accepted formation result and shift required')
if result.carry.carry:
    raw_y = result.point.y + shift.y
    result = result.with_point(u16(result.point.x + shift.x), u16(raw_y), state.carry_observed(int(raw_y > 65535)))
return result
''',
    },
}


# Complete own-Python semantic flows are appended by the one-time author
# conversion tool. No ROM, original assembly or IR is used for that conversion.
DECLARATIONS = {'sum_first_side_roster_troops': {'signature': 'state: GameState', 'returns': 'RosterStrength', 'flow': 'checked_state(state)\n_, byte_length, total = sum_first_side_roster_troops_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())\nreturn RosterStrength(byte_length, total)'},
 'test_force_has_city_assignment': {'signature': 'state: GameState', 'returns': 'CarryOutcome', 'flow': 'checked_state(state)\n_, assigned = test_force_has_city_assignment_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())\nreturn state.carry_result(int(assigned))'},
 'test_second_side_total_with_single_first_roster': {'signature': 'state: GameState', 'returns': 'CarryOutcome', 'flow': 'checked_state(state)\n_, selected = test_second_side_total_with_single_first_roster_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())\nreturn state.carry_result(int(selected))'},
 'test_second_side_total_with_small_second_roster': {'signature': 'state: GameState', 'returns': 'CarryOutcome', 'flow': 'checked_state(state)\n_, selected = test_second_side_total_with_small_second_roster_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())\nreturn state.carry_result(int(selected))'},
 'test_point_in_battlefield_staging_rectangle': {'signature': 'state: GameState, point: Point',
                                                 'returns': 'tuple',
                                                 'flow': 'checked_state(state)\n'
                                                         'if type(point) is not Point:\n'
                                                         "    raise ValueError('typed point required')\n"
                                                         'offset = u16(state.battle_scene() << 2)\n'
                                                         'origin = state.scene_anchor_positions\n'
                                                         'if offset != 92:\n'
                                                         '    anchor_x = origin.word(offset)\n'
                                                         '    left = u16(anchor_x - 4096)\n'
                                                         '    if anchor_x < 4096 or left < 3072:\n'
                                                         '        left = u16(3072)\n'
                                                         '    right = u16(anchor_x + 4096)\n'
                                                         '    if anchor_x + 4096 > 65535 or right > 25600:\n'
                                                         '        right = u16(25600)\n'
                                                         '    anchor_y = origin.word(offset, 2)\n'
                                                         '    lower = anchor_y\n'
                                                         '    upper = anchor_y\n'
                                                         '    if lower >= 20480:\n'
                                                         '        lower = u16(lower - 14336)\n'
                                                         '    else:\n'
                                                         '        upper = u16(upper + 14336)\n'
                                                         'else:\n'
                                                         '    left = origin.word(offset)\n'
                                                         '    right = u16(left - 13312)\n'
                                                         '    anchor_y = origin.word(offset, 2)\n'
                                                         '    lower = u16(anchor_y - 3072)\n'
                                                         '    upper = u16(anchor_y + 3072)\n'
                                                         'bounds = BattleBounds(left, right, lower, upper)\n'
                                                         'if point.x >= left and point.x <= right and '
                                                         '(point.y >= lower) and (point.y <= upper):\n'
                                                         '    return (bounds, state.carry_result(1))\n'
                                                         'return (bounds, state.carry_result(0))\n'},
 'sample_battlefield_staging_rectangle': {'signature': 'state: GameState, bounds: BattleBounds',
                                          'returns': 'Point',
                                          'flow': 'checked_state(state)\n'
                                                  'if type(bounds) is not BattleBounds:\n'
                                                  "    raise ValueError('typed bounds required')\n"
                                                  'width = u16(bounds.right - bounds.left)\n'
                                                  'sample = state.sample_random() & 65535\n'
                                                  'x = u16(bounds.left + (sample * width >> 16))\n'
                                                  'height = u16(bounds.upper - bounds.lower - 3072)\n'
                                                  'sample = state.sample_random() & 65535\n'
                                                  'y = u16(sample * height >> 16)\n'
                                                  'origin = state.scene_anchor_positions\n'
                                                  'offset = u16(state.battle_scene() << 2)\n'
                                                  'if origin.word(offset, 2) >= 20480:\n'
                                                  '    y = u16(bounds.lower + y)\n'
                                                  'else:\n'
                                                  '    y = u16(bounds.lower + y + 3072)\n'
                                                  'return Point(x, y)\n'},
 'read_first_side_staging_anchor': {'signature': 'state: GameState',
                                    'returns': 'Point',
                                    'flow': 'checked_state(state)\n'
                                            'offset = u16(state.battle_scene() << 2)\n'
                                            'origin = state.scene_anchor_positions\n'
                                            'if offset != 92:\n'
                                            '    x = u16(origin.word(offset) - 1024)\n'
                                            '    y = origin.word(offset, 2)\n'
                                            '    if y >= 20480:\n'
                                            '        y = u16(y - 3968)\n'
                                            '    else:\n'
                                            '        y = u16(y + 3968)\n'
                                            'else:\n'
                                            '    x = u16(origin.word(offset) - 4096)\n'
                                            '    y = u16(origin.word(offset, 2) - 1152)\n'
                                            'return Point(x, y)\n'},
 'test_second_side_relative_total_shortfall': {'signature': 'state: GameState',
                                               'returns': 'CarryOutcome',
                                               'flow': 'checked_state(state)\n'
                                                       'total = state.secondary_strength_total()\n'
                                                       'if total < state.primary_strength_total():\n'
                                                       '    if total < state.secondary_strength_limit():\n'
                                                       '        return state.carry_result(1)\n'
                                                       'return state.carry_result(0)\n'},
 'read_second_side_staging_anchor': {'signature': 'state: GameState',
                                     'returns': 'Point',
                                     'flow': 'checked_state(state)\n'
                                             'offset = u16(state.battle_scene() << 2)\n'
                                             'origin = state.scene_anchor_positions\n'
                                             'if offset != 92:\n'
                                             '    x = u16(origin.word(offset) + 1024)\n'
                                             '    y = origin.word(offset, 2)\n'
                                             '    if y >= 20480:\n'
                                             '        y = u16(y - 3968)\n'
                                             '    else:\n'
                                             '        y = u16(y + 3968)\n'
                                             'else:\n'
                                             '    x = u16(origin.word(offset) - 4096)\n'
                                             '    y = u16(origin.word(offset, 2) + 1152)\n'
                                             'return Point(x, y)\n'},
 'sample_or_accept_east_formation_region': {'signature': 'state: GameState, context: RegionInput',
                                            'returns': 'RegionDecision',
                                            'flow': 'region = read_east_formation_region(state, context)\n'
                                                    'if east_formation_contains(context.point, region):\n'
                                                    '    return RegionDecision(Point(region.anchor_x, '
                                                    'region.lower), region.east_limit, region.upper, '
                                                    'state.carry_result(1))\n'
                                                    'sampled = sample_east_formation_point(state, region)\n'
                                                    'return RegionDecision(sampled.point, region.east_limit, '
                                                    'sampled.vertical_span, '
                                                    'state.carry_observed(int(sampled.vertical_wrap)))\n'},
 'sample_or_accept_west_formation_region': {'signature': 'state: GameState, context: RegionInput',
                                            'returns': 'RegionDecision',
                                            'flow': 'checked_state(state)\n'
                                                    'if type(context) is not RegionInput:\n'
                                                    "    raise ValueError('typed region input required')\n"
                                                    'origin = checked_table(context.origin, state)\n'
                                                    'right = origin.word(context.offset)\n'
                                                    'left = u16(right - 14336)\n'
                                                    'anchor_y = origin.word(context.offset, 2)\n'
                                                    'lower = u16(anchor_y - 4096)\n'
                                                    'if lower < 3072:\n'
                                                    '    lower = u16(3072)\n'
                                                    'upper = u16(anchor_y + 4096)\n'
                                                    'if upper > 37888:\n'
                                                    '    upper = u16(37888)\n'
                                                    'if context.point.x >= left and context.point.y >= lower '
                                                    'and (context.point.y <= upper):\n'
                                                    '    return RegionDecision(Point(left, lower), right, '
                                                    'upper, state.carry_result(1))\n'
                                                    'sample = state.sample_random() & 65535\n'
                                                    'x = u16(right - (sample * 8192 >> 16) - 3072)\n'
                                                    'span = u16(upper - lower)\n'
                                                    'sample = state.sample_random() & 65535\n'
                                                    'increment = sample * span >> 16\n'
                                                    'raw_y = lower + increment\n'
                                                    'return RegionDecision(Point(x, u16(raw_y)), right, '
                                                    'span, state.carry_observed(int(raw_y > 65535)))\n'},
 'sample_or_accept_east_flank_region': {'signature': 'state: GameState, context: RegionInput',
                                        'returns': 'RegionDecision',
                                        'flow': 'checked_state(state)\n'
                                                'if type(context) is not RegionInput:\n'
                                                "    raise ValueError('typed region input required')\n"
                                                'origin = checked_table(context.origin, state)\n'
                                                'left = u16(origin.word(context.offset) + 3968)\n'
                                                'raw_right = left + 8320\n'
                                                'right = u16(raw_right)\n'
                                                'if raw_right > 65535 or right > 25600:\n'
                                                '    right = u16(25600)\n'
                                                'lower = origin.word(context.offset, 2)\n'
                                                'upper = lower\n'
                                                'if lower >= 20480:\n'
                                                '    lower = u16(lower - 14336)\n'
                                                'else:\n'
                                                '    upper = u16(upper + 14336)\n'
                                                'if context.point.x >= left and context.point.x <= right and '
                                                '(context.point.y >= lower) and (context.point.y <= upper):\n'
                                                '    return RegionDecision(Point(left, lower), right, upper, '
                                                'state.carry_result(1))\n'
                                                'sample = state.sample_random() & 65535\n'
                                                'span = u16(right - left)\n'
                                                'x = u16(left + (sample * span >> 16) + 1)\n'
                                                'sample = state.sample_random() & 65535\n'
                                                'y = u16(lower + (sample * 8192 >> 16))\n'
                                                'return RegionDecision(Point(x, y), span, upper, '
                                                'state.carry_result(0))\n'},
 'sample_or_accept_west_flank_region': {'signature': 'state: GameState, context: RegionInput',
                                        'returns': 'RegionDecision',
                                        'flow': 'checked_state(state)\n'
                                                'if type(context) is not RegionInput:\n'
                                                "    raise ValueError('typed region input required')\n"
                                                'origin = checked_table(context.origin, state)\n'
                                                'anchor_x = origin.word(context.offset)\n'
                                                'right = u16(anchor_x - 3968)\n'
                                                'left = u16(anchor_x - 12288)\n'
                                                'if anchor_x < 12288 or left < 3072:\n'
                                                '    left = u16(3072)\n'
                                                'lower = origin.word(context.offset, 2)\n'
                                                'upper = lower\n'
                                                'if lower >= 20480:\n'
                                                '    lower = u16(lower - 14336)\n'
                                                'else:\n'
                                                '    upper = u16(upper + 14336)\n'
                                                'if context.point.x >= left and context.point.x <= right and '
                                                '(context.point.y >= lower) and (context.point.y <= upper):\n'
                                                '    return RegionDecision(Point(left, lower), right, upper, '
                                                'state.carry_result(1))\n'
                                                'sample = state.sample_random() & 65535\n'
                                                'span = u16(right - left)\n'
                                                'x = u16(left + (sample * span >> 16))\n'
                                                'sample = state.sample_random() & 65535\n'
                                                'y = u16(lower + (sample * 8192 >> 16))\n'
                                                'return RegionDecision(Point(x, y), span, upper, '
                                                'state.carry_result(0))\n'},
 'sample_or_accept_lower_formation_region': {'signature': 'state: GameState, context: RegionInput',
                                             'returns': 'RegionDecision',
                                             'flow': 'checked_state(state)\n'
                                                     'if type(context) is not RegionInput:\n'
                                                     "    raise ValueError('typed region input required')\n"
                                                     'origin = checked_table(context.origin, state)\n'
                                                     'anchor_x = origin.word(context.offset)\n'
                                                     'left = u16(anchor_x - 3072)\n'
                                                     'right = u16(anchor_x + 3072)\n'
                                                     'upper = origin.word(context.offset, 2)\n'
                                                     'lower = u16(upper - 13312)\n'
                                                     'if context.point.x >= left and context.point.x <= '
                                                     'right and (context.point.y >= lower) and '
                                                     '(context.point.y <= upper):\n'
                                                     '    return RegionDecision(Point(left, lower), right, '
                                                     'upper, state.carry_result(1))\n'
                                                     'sample = state.sample_random() & 65535\n'
                                                     'x = u16(left + (sample * 6144 >> 16))\n'
                                                     'sample = state.sample_random() & 65535\n'
                                                     'y = u16(lower + sample * 6144)\n'
                                                     'return RegionDecision(Point(x, y), right, upper, '
                                                     'state.carry_result(0))\n'},
 'sample_or_accept_upper_formation_region': {'signature': 'state: GameState, context: RegionInput',
                                             'returns': 'RegionDecision',
                                             'flow': 'checked_state(state)\n'
                                                     'if type(context) is not RegionInput:\n'
                                                     "    raise ValueError('typed region input required')\n"
                                                     'origin = checked_table(context.origin, state)\n'
                                                     'anchor_x = origin.word(context.offset)\n'
                                                     'left = u16(anchor_x - 3072)\n'
                                                     'right = u16(anchor_x + 3072)\n'
                                                     'lower = origin.word(context.offset, 2)\n'
                                                     'upper = u16(lower + 13312)\n'
                                                     'if context.point.x >= left and context.point.x <= '
                                                     'right and (context.point.y >= lower) and '
                                                     '(context.point.y <= upper):\n'
                                                     '    return RegionDecision(Point(left, lower), right, '
                                                     'upper, state.carry_result(1))\n'
                                                     'sample = state.sample_random() & 65535\n'
                                                     'x = u16(left + (sample * 6144 >> 16))\n'
                                                     'sample = state.sample_random() & 65535\n'
                                                     'y = u16(lower + sample * 6144)\n'
                                                     'return RegionDecision(Point(x, y), right, upper, '
                                                     'state.carry_result(0))\n'},
 'choose_east_center_first_formation_point': {'signature': 'state: GameState, context: RegionInput',
                                              'returns': 'RegionDecision',
                                              'flow': 'result = '
                                                      'sample_or_accept_east_formation_region(state, '
                                                      'context)\n'
                                                      'return translate_accepted_formation_point(state, '
                                                      'result, Point(3968, 3072))\n',
                                              'slots': {3968: ['center_horizontal', 1, 65535],
                                                        3072: ['center_vertical', 0, 65535]}},
 'choose_west_center_first_formation_point': {'signature': 'state: GameState, context: RegionInput',
                                              'returns': 'RegionDecision',
                                              'flow': 'result = '
                                                      'sample_or_accept_west_formation_region(state, '
                                                      'context)\n'
                                                      'if result.carry.carry:\n'
                                                      '    result = '
                                                      'result.with_point(u16(result.horizontal_limit_or_span '
                                                      '- 3968), u16(result.point.y + 3072), '
                                                      'state.carry_observed(int(result.point.y + 3072 > '
                                                      '65535)))\n'
                                                      'return result\n'},
 'choose_east_flank_first_formation_point': {'signature': 'state: GameState, context: RegionInput',
                                             'returns': 'RegionDecision',
                                             'flow': 'result = sample_or_accept_east_flank_region(state, '
                                                     'context)\n'
                                                     'if result.carry.carry:\n'
                                                     '    if context.origin.word(context.offset, 2) >= '
                                                     '20480:\n'
                                                     '        result = result.with_point(result.point.x, '
                                                     'u16(result.vertical_limit_or_span - 1024), '
                                                     'state.carry_observed(int(result.vertical_limit_or_span '
                                                     '< 1024)))\n'
                                                     '    else:\n'
                                                     '        result = result.with_point(result.point.x, '
                                                     'u16(result.point.y + 1024), '
                                                     'state.carry_observed(int(result.point.y + 1024 > '
                                                     '65535)))\n'
                                                     'return result\n'},
 'choose_lower_center_first_formation_point': {'signature': 'state: GameState, context: RegionInput',
                                               'returns': 'RegionDecision',
                                               'flow': 'result = '
                                                       'sample_or_accept_lower_formation_region(state, '
                                                       'context)\n'
                                                       'if result.carry.carry:\n'
                                                       '    result = result.with_point(u16(result.point.x + '
                                                       '4096), u16(result.point.y + 9344), '
                                                       'state.carry_observed(int(result.point.y + 9344 > '
                                                       '65535)))\n'
                                                       'return result\n'},
 'choose_east_center_second_formation_point': {'signature': 'state: GameState, context: RegionInput',
                                               'returns': 'RegionDecision',
                                               'flow': 'result = '
                                                       'sample_or_accept_east_formation_region(state, '
                                                       'context)\n'
                                                       'if result.carry.carry:\n'
                                                       '    result = result.with_point(u16(result.point.x + '
                                                       '3968), u16(result.point.y + 5120), '
                                                       'state.carry_observed(int(result.point.y + 5120 > '
                                                       '65535)))\n'
                                                       'return result\n'},
 'choose_west_center_second_formation_point': {'signature': 'state: GameState, context: RegionInput',
                                               'returns': 'RegionDecision',
                                               'flow': 'result = '
                                                       'sample_or_accept_west_formation_region(state, '
                                                       'context)\n'
                                                       'if result.carry.carry:\n'
                                                       '    result = '
                                                       'result.with_point(u16(result.horizontal_limit_or_span '
                                                       '- 3968), u16(result.point.y + 5120), '
                                                       'state.carry_observed(int(result.point.y + 5120 > '
                                                       '65535)))\n'
                                                       'return result\n'},
 'choose_west_flank_second_formation_point': {'signature': 'state: GameState, context: RegionInput',
                                              'returns': 'RegionDecision',
                                              'flow': 'result = sample_or_accept_west_flank_region(state, '
                                                      'context)\n'
                                                      'if result.carry.carry:\n'
                                                      '    if context.origin.word(context.offset, 2) >= '
                                                      '20480:\n'
                                                      '        result = '
                                                      'result.with_point(result.horizontal_limit_or_span, '
                                                      'u16(result.vertical_limit_or_span - 1024), '
                                                      'state.carry_observed(int(result.vertical_limit_or_span '
                                                      '< 1024)))\n'
                                                      '    else:\n'
                                                      '        result = '
                                                      'result.with_point(result.horizontal_limit_or_span, '
                                                      'u16(result.point.y + 1024), '
                                                      'state.carry_observed(int(result.point.y + 1024 > '
                                                      '65535)))\n'
                                                      'return result\n'},
 'choose_upper_center_second_formation_point': {'signature': 'state: GameState, context: RegionInput',
                                                'returns': 'RegionDecision',
                                                'flow': 'result = '
                                                        'sample_or_accept_upper_formation_region(state, '
                                                        'context)\n'
                                                        'if result.carry.carry:\n'
                                                        '    result = result.with_point(u16(result.point.x + '
                                                        '4096), u16(result.point.y + 3968), '
                                                        'state.carry_observed(int(result.point.y + 3968 > '
                                                        '65535)))\n'
                                                        'return result\n'},
 'choose_east_center_third_formation_point': {'signature': 'state: GameState, context: RegionInput',
                                              'returns': 'RegionDecision',
                                              'flow': 'result = '
                                                      'sample_or_accept_east_formation_region(state, '
                                                      'context)\n'
                                                      'if result.carry.carry:\n'
                                                      '    result = result.with_point(u16(result.point.x + '
                                                      '3968), u16(result.point.y + 7168), '
                                                      'state.carry_observed(int(result.point.y + 7168 > '
                                                      '65535)))\n'
                                                      'return result\n'},
 'choose_west_center_third_formation_point': {'signature': 'state: GameState, context: RegionInput',
                                              'returns': 'RegionDecision',
                                              'flow': 'result = '
                                                      'sample_or_accept_west_formation_region(state, '
                                                      'context)\n'
                                                      'if result.carry.carry:\n'
                                                      '    result = '
                                                      'result.with_point(u16(result.horizontal_limit_or_span '
                                                      '- 3968), u16(result.point.y + 7168), '
                                                      'state.carry_observed(int(result.point.y + 7168 > '
                                                      '65535)))\n'
                                                      'return result\n'},
 'choose_west_flank_third_formation_point': {'signature': 'state: GameState, context: RegionInput',
                                             'returns': 'RegionDecision',
                                             'flow': 'result = sample_or_accept_west_flank_region(state, '
                                                     'context)\n'
                                                     'if result.carry.carry:\n'
                                                     '    if context.origin.word(context.offset, 2) >= '
                                                     '20480:\n'
                                                     '        result = '
                                                     'result.with_point(result.horizontal_limit_or_span, '
                                                     'u16(result.vertical_limit_or_span + 1024), '
                                                     'state.carry_observed(int(result.vertical_limit_or_span '
                                                     '+ 1024 > 65535)))\n'
                                                     '    else:\n'
                                                     '        result = '
                                                     'result.with_point(result.horizontal_limit_or_span, '
                                                     'u16(result.point.y - 1024), '
                                                     'state.carry_observed(int(result.point.y < 1024)))\n'
                                                     'return result\n'},
 'choose_upper_center_third_formation_point': {'signature': 'state: GameState, context: RegionInput',
                                               'returns': 'RegionDecision',
                                               'flow': 'result = '
                                                       'sample_or_accept_upper_formation_region(state, '
                                                       'context)\n'
                                                       'if result.carry.carry:\n'
                                                       '    result = result.with_point(u16(result.point.x + '
                                                       '2048), u16(result.point.y + 3968), '
                                                       'state.carry_observed(int(result.point.y + 3968 > '
                                                       '65535)))\n'
                                                       'return result\n'},
 'compare_actor_shifted_troop_word_to_weakest_contact': {'signature': 'state: GameState, actor: Word',
                                                         'returns': 'CarryOutcome',
                                                         'flow': 'checked_state(state)\n'
                                                                 'uint(actor, 16)\n'
                                                                 'collect_contacts_in_speed_radius(state, '
                                                                 'actor)\n'
                                                                 'if not '
                                                                 'negative_word(state.formation_scratch.word()):\n'
                                                                 '    weakest = '
                                                                 'select_weakest_contact_strength(state)\n'
                                                                 '    factor = '
                                                                 'weighted_training_factor(state, actor)\n'
                                                                 '    shifted = '
                                                                 'weakest.troops.long(u16(actor << 2), 2)\n'
                                                                 '    strength = u32(low16(shifted) * '
                                                                 'low16(factor))\n'
                                                                 '    if weakest.strength <= strength:\n'
                                                                 '        return state.carry_result(1)\n'
                                                                 'return state.carry_result(0)\n'},
 'read_outer_east_staging_anchor': {'signature': 'state: GameState',
                                    'returns': 'Point',
                                    'flow': 'checked_state(state)\n'
                                            'offset = u16(state.battle_scene() << 2)\n'
                                            'origin = state.scene_anchor_positions\n'
                                            'if offset != 92:\n'
                                            '    x = u16(origin.word(offset) + 3072)\n'
                                            '    y = origin.word(offset, 2)\n'
                                            '    if y >= 20480:\n'
                                            '        y = u16(y - 3968)\n'
                                            '    else:\n'
                                            '        y = u16(y + 3968)\n'
                                            'else:\n'
                                            '    x = u16(origin.word(offset) - 3968)\n'
                                            '    y = u16(origin.word(offset, 2) + 3072)\n'
                                            'return Point(x, y)\n'},
 'read_outer_west_staging_anchor': {'signature': 'state: GameState',
                                    'returns': 'Point',
                                    'flow': 'checked_state(state)\n'
                                            'offset = u16(state.battle_scene() << 2)\n'
                                            'origin = state.scene_anchor_positions\n'
                                            'if offset != 92:\n'
                                            '    x = u16(origin.word(offset) - 3072)\n'
                                            '    y = origin.word(offset, 2)\n'
                                            '    if y >= 20480:\n'
                                            '        y = u16(y - 3968)\n'
                                            '    else:\n'
                                            '        y = u16(y + 3968)\n'
                                            'else:\n'
                                            '    x = u16(origin.word(offset) - 3968)\n'
                                            '    y = u16(origin.word(offset, 2) - 3072)\n'
                                            'return Point(x, y)\n'},
 'select_contact_nearest_deployment_anchor': {'signature': 'state: GameState, retained_unit: Word=0',
                                              'returns': 'ClosestBattleUnit',
                                              'flow': 'checked_state(state)\n'
                                                      'uint(retained_unit, 16)\n'
                                                      'positions = state.battle_positions\n'
                                                      'roster = state.formation_scratch.cursor()\n'
                                                      'source = state.scene_deployment_cells\n'
                                                      'scene = state.battle_scene()\n'
                                                      'variant = state.scene_variant.byte(scene)\n'
                                                      'offset = u16(u16(scene << 5) + u16(variant << 1))\n'
                                                      'anchor_x = u16(source.byte(offset) << 10)\n'
                                                      'anchor_y = u16(source.byte(offset, 1) << 10)\n'
                                                      'distance = u16(65535)\n'
                                                      'selected = retained_unit\n'
                                                      'while True:\n'
                                                      '    member = roster.next_word()\n'
                                                      '    if negative_word(member):\n'
                                                      '        break\n'
                                                      '    member_offset = u16(member << 2)\n'
                                                      '    x = positions.word(member_offset)\n'
                                                      '    x_distance = u16(x - anchor_x) if x >= anchor_x '
                                                      'else u16(anchor_x - x)\n'
                                                      '    y = positions.word(member_offset, 2)\n'
                                                      '    y_distance = u16(y - anchor_y) if y >= anchor_y '
                                                      'else u16(anchor_y - y)\n'
                                                      '    candidate = u16(x_distance + y_distance)\n'
                                                      '    if candidate < distance:\n'
                                                      '        distance = candidate\n'
                                                      '        selected = member\n'
                                                      'return ClosestBattleUnit(distance, selected)\n'},
 'read_formation_relative_position_delta': {'signature': 'state: GameState, retained_position: Word=0',
                                            'returns': 'Word',
                                            'flow': 'checked_state(state)\n'
                                                    'uint(retained_position, 16)\n'
                                                    'mode = state.deployment_step_mode()\n'
                                                    'if mode >= 9:\n'
                                                    '    return retained_position\n'
                                                    'offset = u16(mode << 2)\n'
                                                    'deltas = state.deployment_step_offsets\n'
                                                    'dx = deltas.word(offset)\n'
                                                    'dy = deltas.word(offset, 2)\n'
                                                    'scene = state.battle_scene()\n'
                                                    'variant = state.scene_variant.byte(scene)\n'
                                                    'offset = u16(u16(scene << 5) + u16(variant << 1))\n'
                                                    'cells = state.scene_deployment_cells\n'
                                                    'x = cells.byte(offset)\n'
                                                    'if x <= 14:\n'
                                                    '    dx = u16(-dx)\n'
                                                    'y = cells.byte(offset, 1)\n'
                                                    'if y >= 20:\n'
                                                    '    dy = u16(-dy)\n'
                                                    'x = u16(x + dx)\n'
                                                    'y = u16(y + dy)\n'
                                                    'return u16(x << 8 | u8(y))\n'},
 'test_first_side_relative_total_shortfall': {'signature': 'state: GameState',
                                              'returns': 'CarryOutcome',
                                              'flow': 'checked_state(state)\n'
                                                      'total = state.primary_strength_total()\n'
                                                      'if total < state.secondary_strength_total():\n'
                                                      '    if total < state.primary_strength_limit():\n'
                                                      '        return state.carry_result(1)\n'
                                                      'return state.carry_result(0)\n'},
 'test_second_roster_type6_count_below_four': {'signature': 'state: GameState',
                                               'returns': 'CarryOutcome',
                                               'flow': 'checked_state(state)\n'
                                                       'terrain = load_battlefield_map_context(state)\n'
                                                       'roster = state.secondary_battle_roster.cursor()\n'
                                                       'positions = state.battle_positions\n'
                                                       'count = u16(0)\n'
                                                       'while True:\n'
                                                       '    member = roster.next_word()\n'
                                                       '    if negative_word(member):\n'
                                                       '        return state.carry_result(1)\n'
                                                       '    offset = u16(member << 2)\n'
                                                       '    x = positions.word(offset)\n'
                                                       '    y = positions.word(offset, 2)\n'
                                                       '    kind = read_battlefield_terrain_type(state, '
                                                       'terrain, x, y)\n'
                                                       '    if u8(kind) != 6:\n'
                                                       '        return state.carry_result(0)\n'
                                                       '    count = u16(count + 1)\n'
                                                       '    if count >= 4:\n'
                                                       '        return state.carry_result(0)\n'},
 'test_second_side_threshold_shortfall': {'signature': 'state: GameState',
                                          'returns': 'CarryOutcome',
                                          'flow': 'checked_state(state)\n'
                                                  'total = state.secondary_strength_total()\n'
                                                  'if total < state.secondary_strength_limit():\n'
                                                  '    return state.carry_result(1)\n'
                                                  'return state.carry_result(0)\n'}}

DEPLOYMENT_DECLARATIONS = {'initialize_second_side_deployment': {'signature': 'state: GameState',
                                       'returns': 'None',
                                       'flow': 'checked_state(state)\n'
                                               'prepare_second_side_formation_assignment(state)\n'
                                               'populate_second_side_unset_positions(state)\n'
                                               'state.set_battle_phase(u16(0))\n'},
 'prepare_second_side_formation_assignment': {'signature': 'state: GameState',
                                              'returns': 'None',
                                              'flow': 'checked_state(state)\n'
                                                      'count = read_assignment_subroster_count(state, '
                                                      'state.secondary_battle_roster)\n'
                                                      'copy_second_side_position_assignment(state, count)\n'},
 'sort_side_subroster_by_weighted_troops': {'signature': 'state: GameState', 'returns': 'Word', 'flow': 'checked_state(state)\nreturn sort_first_side_roster_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())[1]'},
 'copy_second_side_position_assignment': {'signature': 'state: GameState, count: Word',
                                          'returns': 'FormationCursors',
                                          'flow': 'checked_state(state)\n'
                                                  'uint(count, 16)\n'
                                                  'force = state.battle_secondary_force()\n'
                                                  'formation = state.formation_directory.word(u16(force << '
                                                  '1))\n'
                                                  'offset = formation_assignment_offset(formation, count)\n'
                                                  'destination = state.secondary_formation_orders.cursor()\n'
                                                  'source = '
                                                  'state.secondary_formation_parameters.cursor(offset)\n'
                                                  'return copy_live_formation_orders(state, source, '
                                                  'destination)\n'},
 'populate_second_side_unset_positions': {'signature': 'state: GameState',
                                          'returns': 'None',
                                          'flow': 'checked_state(state)\n'
                                                  'prepare_second_side_battlefield_choices(state)\n'
                                                  'views = DeploymentViews(state.secondary_battle_roster, '
                                                  'state.secondary_formation_orders, '
                                                  'state.deployed_cell_pairs, state.battle_positions)\n'
                                                  'submit_unset_deployment_positions(state, views)\n'},
 'prepare_second_side_battlefield_choices': {'signature': 'state: GameState',
                                             'returns': 'FormationCursors',
                                             'flow': 'checked_state(state)\n'
                                                     'source = '
                                                     'state.secondary_position_catalog.cursor(u16(state.battle_scene() '
                                                     '* 58))\n'
                                                     'destination = state.deployed_cell_pairs.cursor()\n'
                                                     'destination.append_word(source.next_word())\n'
                                                     'publish_shuffled_choice_window(state, source, '
                                                     'destination, u16(4), u16(3))\n'
                                                     'publish_shuffled_choice_window(state, source, '
                                                     'destination, u16(2), u16(5))\n'
                                                     'state.set_selected_position_1(u16(0))\n'
                                                     'state.set_selected_position_2(u16(0))\n'
                                                     'state.set_selected_position_3(u16(0))\n'
                                                     'for index in range(4):\n'
                                                     '    chosen = choose_unused_second_side_point(state, '
                                                     'source, destination)\n'
                                                     '    commit_second_side_selected_point(state, '
                                                     'u16(index), chosen)\n'
                                                     'return FormationCursors(source, destination)\n'},
 'shuffle_nonzero_choice_slots': {'signature': 'state: GameState', 'returns': 'None', 'flow': 'checked_state(state)\nshuffle_first_side_choice_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())'},
 'choose_unused_second_side_point': {'signature': 'state: GameState, source: Cursor, destination: Cursor',
                                     'returns': 'Word',
                                     'flow': 'checked_state(state)\n'
                                             'checked_cursor(source, state)\n'
                                             'checked_cursor(destination, state)\n'
                                             'choices = copy_choice_window_to_scratch(state, source, '
                                             'u16(4))\n'
                                             'for _ in range(3):\n'
                                             '    choices.append_word(u16(0))\n'
                                             'shuffle_nonzero_choice_slots(state)\n'
                                             'choices = state.formation_scratch.cursor()\n'
                                             'while True:\n'
                                             '    candidate = choices.next_word()\n'
                                             '    if candidate == state.selected_position_1():\n'
                                             '        continue\n'
                                             '    if candidate == state.selected_position_2():\n'
                                             '        continue\n'
                                             '    if candidate == state.selected_position_3():\n'
                                             '        continue\n'
                                             '    destination.append_word(candidate)\n'
                                             '    return candidate\n'},
 'initialize_first_side_deployment': {'signature': 'state: GameState', 'returns': 'None', 'flow': 'checked_state(state)\ninitialize_first_side_deployment_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())'},
 'promote_first_side_leader': {'signature': 'state: GameState', 'returns': 'Word', 'flow': 'checked_state(state)\nreturn promote_first_side_leader_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved()).selected'},
 'prepare_first_side_formation_assignment': {'signature': 'state: GameState', 'returns': 'None', 'flow': 'checked_state(state)\nprepare_first_side_assignment_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())'},
 'copy_first_side_position_assignment': {'signature': 'state: GameState, count: Word', 'returns': 'FormationCursors', 'flow': 'checked_state(state)\nframe = copy_first_side_assignment_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), count)\nreturn FormationCursors(frame.candidates, frame.roster)'},
 'populate_first_side_unset_positions': {'signature': 'state: GameState', 'returns': 'None', 'flow': 'checked_state(state)\npopulate_first_side_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())'},
 'prepare_first_side_battlefield_choices': {'signature': 'state: GameState', 'returns': 'FormationCursors', 'flow': 'checked_state(state)\nframe = prepare_first_side_choices_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())\nreturn FormationCursors(frame.roster, frame.candidates)'},
 'choose_unused_first_side_point': {'signature': 'state: GameState, source: Cursor, destination: Cursor', 'returns': 'Word', 'flow': 'checked_state(state)\nchecked_cursor(source, state)\nchecked_cursor(destination, state)\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=source, candidates=destination)\nreturned = choose_unused_first_side_fields(BattlePolicyMemory(state), frame)\nreturn low16(returned.target_x)'}}

DEPLOYMENT_INLINE_DECLARATIONS = {'read_assignment_subroster_count': {'signature': 'state: GameState, roster: Table', 'returns': 'Word', 'flow': 'checked_state(state)\nchecked_table(roster, state)\nreturn read_first_side_assignment_count_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), roster)[1]'},
 'read_weighted_deployment_roster': {'signature': 'state: GameState', 'returns': 'WeightedDeploymentRoster', 'flow': 'checked_state(state)\nframe = read_first_side_weighted_roster_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())\nreturn WeightedDeploymentRoster(frame.opponent, state.formation_scratch)'},
 'weighted_deployment_product': {'signature': 'troops: Long, factor: Long',
                                 'returns': 'Long',
                                 'flow': 'uint(troops, 32)\n'
                                         'uint(factor, 32)\n'
                                         'return u32(low16(troops) * low16(factor))\n'},
 'collect_deployment_weights': {'signature': 'state: GameState, views: WeightedDeploymentRoster', 'returns': 'Word', 'flow': "checked_state(state)\nif type(views) is not WeightedDeploymentRoster:\n    raise ValueError('live weighted roster required')\nchecked_table(views.roster, state)\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=views.roster.cursor(), candidates=views.weights.cursor(), scan=state.officer_troops.cursor())\nreturn collect_first_side_weight_fields(BattlePolicyMemory(state), frame)[1]"},
 'weighted_neighbor_should_move_forward': {'signature': 'value: Long, previous: Long',
                                           'returns': 'bool',
                                           'flow': 'uint(value, 32)\n'
                                                   'uint(previous, 32)\n'
                                                   'return value >= previous\n'},
 'swap_live_weighted_neighbors': {'signature': 'state: GameState, views: WeightedDeploymentRoster, offset: Word, member_offset: Word, value: Long', 'returns': 'None', 'flow': "checked_state(state)\nif type(views) is not WeightedDeploymentRoster:\n    raise ValueError('live weighted roster required')\nchecked_table(views.roster, state)\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=views.roster.cursor(), candidates=views.weights.cursor())\nswap_first_side_weight_fields(BattlePolicyMemory(state), frame, offset, member_offset, value)"},
 'order_live_weighted_roster': {'signature': 'state: GameState, views: WeightedDeploymentRoster, count: Word', 'returns': 'None', 'flow': "checked_state(state)\nif type(views) is not WeightedDeploymentRoster:\n    raise ValueError('live weighted roster required')\nchecked_table(views.roster, state)\nuint(count, 16)\nlimit = u16(u16(count - 1) << 2)\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=views.roster.cursor(), candidates=views.weights.cursor())\norder_first_side_weight_fields(BattlePolicyMemory(state), frame, count, limit)"},
 'formation_assignment_offset': {'signature': 'formation: Word, count: Word',
                                 'returns': 'Word',
                                 'flow': 'uint(formation, 16)\n'
                                         'uint(count, 16)\n'
                                         'return u16(u16(u16(formation << 4) + count) << 5)\n'},
 'copy_live_formation_orders': {'signature': 'state: GameState, source: Cursor, destination: Cursor', 'returns': 'FormationCursors', 'flow': 'checked_state(state)\nchecked_cursor(source, state)\nchecked_cursor(destination, state)\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=destination, candidates=source)\nframe = copy_first_side_order_fields(BattlePolicyMemory(state), frame)\nreturn FormationCursors(frame.candidates, frame.roster)'},
 'deployment_position_needs_assignment': {'signature': 'x: Word',
                                          'returns': 'bool',
                                          'flow': 'uint(x, 16)\nreturn x == 0\n'},
 'write_live_deployment_position': {'signature': 'state: GameState, views: DeploymentViews, offset: Word, order: Word', 'returns': 'None', 'flow': "checked_state(state)\nif type(views) is not DeploymentViews:\n    raise ValueError('live deployment views required')\nchecked_table(views.roster, state)\nframe = first_replace(FirstDeploymentFrame.unobserved(), controller=views.cells, scan=views.positions.cursor())\nwrite_unset_deployment_fields(BattlePolicyMemory(state), frame, offset, order)"},
 'submit_unset_deployment_positions': {'signature': 'state: GameState, views: DeploymentViews', 'returns': 'None', 'flow': "checked_state(state)\nif type(views) is not DeploymentViews:\n    raise ValueError('live deployment views required')\nchecked_table(views.roster, state)\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=views.roster.cursor(), candidates=views.orders.cursor(), controller=views.cells, scan=views.positions.cursor())\nsubmit_unset_deployment_fields(BattlePolicyMemory(state), frame)"},
 'copy_choice_window_to_scratch': {'signature': 'state: GameState, source: Cursor, count_minus_one: Word',
                                   'returns': 'Cursor',
                                   'flow': 'checked_state(state)\n'
                                           'checked_cursor(source, state)\n'
                                           'uint(count_minus_one, 16)\n'
                                           'scratch = state.formation_scratch.cursor()\n'
                                           'for _ in descending_inclusive(count_minus_one):\n'
                                           '    scratch.append_word(source.next_word())\n'
                                           'return scratch\n'},
 'publish_shuffled_choice_window': {'signature': 'state: GameState, source: Cursor, destination: Cursor, '
                                                 'count_minus_one: Word, zeros: Word',
                                    'returns': 'None',
                                    'flow': 'checked_state(state)\n'
                                            'checked_cursor(source, state)\n'
                                            'checked_cursor(destination, state)\n'
                                            'uint(count_minus_one, 16)\n'
                                            'uint(zeros, 16)\n'
                                            'scratch = copy_choice_window_to_scratch(state, source, '
                                            'count_minus_one)\n'
                                            'for _ in range(zeros):\n'
                                            '    scratch.append_word(u16(0))\n'
                                            'shuffle_nonzero_choice_slots(state)\n'
                                            'scratch = state.formation_scratch.cursor()\n'
                                            'for _ in descending_inclusive(count_minus_one):\n'
                                            '    destination.append_word(scratch.next_word())\n'},
 'commit_second_side_selected_point': {'signature': 'state: GameState, index: Word, chosen: Word',
                                       'returns': 'None',
                                       'flow': 'checked_state(state)\n'
                                               'uint(index, 16)\n'
                                               'uint(chosen, 16)\n'
                                               'if index == 0:\n'
                                               '    state.set_selected_position_1(chosen)\n'
                                               'elif index == 1:\n'
                                               '    state.set_selected_position_2(chosen)\n'
                                               'elif index == 2:\n'
                                               '    state.set_selected_position_3(chosen)\n'
                                               'state.selected_primary_positions.set_word(u16(index << 1), '
                                               'chosen)\n'},
 'shuffle_slots_from_sample': {'signature': 'sample: Word',
                               'returns': 'ShuffleSlots',
                               'flow': 'uint(sample, 16)\n'
                                       'return ShuffleSlots(u16(sample & 14), u16(sample >> 4 & 14))\n'},
 'swap_nonzero_choice_slots': {'signature': 'state: GameState, choices: Table, slots: ShuffleSlots', 'returns': 'None', 'flow': 'checked_state(state)\nswap_nonzero_choice_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), choices, slots)'},
 'first_roster_contains_leader': {'signature': 'state: GameState, selected: Word', 'returns': 'bool', 'flow': 'checked_state(state)\nreturn find_first_side_leader_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), selected)[1]'},
 'leader_readiness_uses_byte_rank': {'signature': 'readiness: Byte',
                                     'returns': 'bool',
                                     'flow': 'uint(readiness, 8)\nreturn readiness < 90\n',
                                     'slots': {90: ('readiness_limit', 0, 255)}},
 'leader_readiness_should_replace': {'signature': 'readiness: Byte, best: Byte',
                                     'returns': 'bool',
                                     'flow': 'uint(readiness, 8)\nuint(best, 8)\nreturn readiness >= best\n'},
 'leader_strength_should_replace': {'signature': 'strength: Word, best: Word',
                                    'returns': 'bool',
                                    'flow': 'uint(strength, 16)\nuint(best, 16)\nreturn strength >= best\n'},
 'read_wrapped_leader_strength': {'signature': 'state: GameState, member: Word', 'returns': 'Word', 'flow': 'checked_state(state)\nframe = first_replace(FirstDeploymentFrame.unobserved(), controller=state.officer_word_b200, scan=state.officer_word_b600.cursor())\nreturn read_first_side_strength_fields(BattlePolicyMemory(state), frame, member)[1]'},
 'choose_first_roster_fallback_leader': {'signature': 'state: GameState, selected: Word', 'returns': 'Word', 'flow': 'checked_state(state)\nreturn choose_first_side_leader_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), selected).selected'},
 'move_first_side_leader_to_front': {'signature': 'state: GameState, selected: Word', 'returns': 'None', 'flow': 'checked_state(state)\nmove_first_side_leader_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), selected)'},
 'prepare_first_side_reserve_choices': {'signature': 'state: GameState, source: Cursor', 'returns': 'None', 'flow': 'checked_state(state)\nchecked_cursor(source, state)\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=source)\nprepare_first_side_reserve_fields(BattlePolicyMemory(state), frame)'},
 'submit_first_side_reserve_choices': {'signature': 'state: GameState, destination: Cursor', 'returns': 'None', 'flow': 'checked_state(state)\nchecked_cursor(destination, state)\nframe = first_replace(FirstDeploymentFrame.unobserved(), candidates=destination)\nsubmit_first_side_reserve_fields(BattlePolicyMemory(state), frame)'}}


# All new supplied field helpers are full-body admitted and closure-expanded.
DEPLOYMENT_INLINE_DECLARATIONS.update({'_first_add_word': {'signature': 'frame: FirstDeploymentFrame, name, left: Word, right: Word', 'returns': 'FirstDeploymentFrame', 'flow': 'uint(left, 16)\nuint(right, 16)\nwide = left + right\nvalue = u16(wide)\noverflow = not (left ^ right) & 32768 and bool((left ^ value) & 32768)\nretained = frame.carrier(name)\ncarrier = None if retained is None else replace_word(retained, value)\nstatus = (17 if wide > 65535 else 0) | (2 if overflow else 0) | (8 if value & 32768 else 0) | (4 if value == 0 else 0)\nreturn first_replace(frame, **{name: carrier}, status=status)'}, '_first_byte': {'signature': 'frame: FirstDeploymentFrame, name, value: Byte', 'returns': 'FirstDeploymentFrame', 'flow': 'uint(value, 8)\nretained = frame.carrier(name)\ncarrier = None if retained is None else replace_byte(retained, value)\nstatus = None if frame.status is None else frame.status & 16 | (8 if value & 128 else 0) | (4 if value == 0 else 0)\nreturn first_replace(frame, **{name: carrier}, status=status)'}, '_first_call': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, continuation: Long, algorithm', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _first_frame(memory, frame)\nuint(continuation, 32)\nif frame.stack_cursor is None:\n    return algorithm(memory, frame)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nreturned = algorithm(memory, first_replace(frame, stack_cursor=stack))\nreturned = _first_frame(memory, returned)\ntarget = returned.stack_cursor.long()\nif target != continuation:\n    raise FirstDeploymentReturnBoundary(target, returned, continuation)\nreturn first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))'}, '_first_compare_word': {'signature': 'frame: FirstDeploymentFrame, left: Word, right: Word', 'returns': 'FirstDeploymentFrame', 'flow': 'uint(left, 16)\nuint(right, 16)\nvalue = u16(left - right)\noverflow = bool((left ^ right) & (left ^ value) & 32768)\nstatus = None if frame.status is None else frame.status & 16 | (1 if left < right else 0) | (2 if overflow else 0) | (8 if value & 32768 else 0) | (4 if value == 0 else 0)\nreturn first_replace(frame, status=status)'}, '_first_counter_end': {'signature': 'frame: FirstDeploymentFrame, name', 'returns': 'FirstDeploymentFrame', 'flow': 'retained = frame.carrier(name)\ncarrier = None if retained is None else replace_word(retained, 65535)\nreturn first_replace(frame, **{name: carrier})'}, '_first_frame': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:\n    raise ValueError('one same-state deployment memory and actual frame required')\nreturn frame.validate(memory.state, type(memory.state) is not GameState)"}, '_first_memory_word': {'signature': 'frame: FirstDeploymentFrame, value: Word', 'returns': 'FirstDeploymentFrame', 'flow': 'uint(value, 16)\nstatus = None if frame.status is None else frame.status & 16 | (8 if value & 32768 else 0) | (4 if value == 0 else 0)\nreturn first_replace(frame, status=status)'}, '_first_pending_call': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _first_frame(memory, frame)\nif frame.stack_cursor is None:\n    raise ValueError('legacy incomplete callee cannot produce a complete field return')\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\ncalled = first_replace(frame, stack_cursor=stack)\nmemory.state.sr = memory.state.sr & 65504 | called.status\nreturned = memory.state.service_at(target, called)\nif type(returned) is not FirstDeploymentFrame:\n    raise ValueError('genuine deployment callee must return complete current fields')\nreturned = _first_frame(memory, returned)\nactual_target = returned.stack_cursor.long()\nif actual_target != continuation:\n    raise FirstDeploymentReturnBoundary(actual_target, returned, continuation)\nreturn first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))"}, '_first_promote_frame': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return promote_first_side_leader_fields(memory, frame).frame'}, '_first_shift_word': {'signature': 'frame: FirstDeploymentFrame, name, original: Word, count: Word', 'returns': 'FirstDeploymentFrame', 'flow': "uint(original, 16)\nuint(count, 16)\nif not 1 <= count <= 8:\n    raise ValueError('original bounded WORD shift required')\nvalue = u16(original << count)\nbit = bool(original & 1 << 16 - count)\nretained = frame.carrier(name)\ncarrier = None if retained is None else replace_word(retained, value)\nstatus = (17 if bit else 0) | (8 if value & 32768 else 0) | (4 if value == 0 else 0)\nreturn first_replace(frame, **{name: carrier}, status=status)"}, '_first_transfer_word': {'signature': 'frame: FirstDeploymentFrame, destination, source', 'returns': 'FirstDeploymentFrame', 'flow': 'carrier = frame.carrier(source)\nif carrier is None:\n    return first_replace(frame, **{destination: None}, status=None)\nreturn _first_word(frame, destination, low16(carrier))'}, '_first_word': {'signature': 'frame: FirstDeploymentFrame, name, value: Word', 'returns': 'FirstDeploymentFrame', 'flow': 'uint(value, 16)\nretained = frame.carrier(name)\nvalue_carrier = None if retained is None else replace_word(retained, value)\nstatus = None if frame.status is None else frame.status & 16 | (8 if value & 32768 else 0) | (4 if value == 0 else 0)\nreturn first_replace(frame, **{name: value_carrier}, status=status)'}, 'choose_first_side_leader_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, selected: Word', 'returns': 'FirstLeaderFields', 'flow': "frame = _first_frame(memory, frame)\nuint(selected, 16)\nroster = memory.state.table(4294944080).cursor()\nreadiness = memory.state.table(4294951680).cursor()\nskill = memory.state.table(4294947328)\nloyalty = memory.state.table(4294948352)\nframe = first_replace(frame, roster=roster, candidates=readiness, controller=skill, scan=loyalty.cursor())\nframe = _first_word(_first_word(frame, 'target_y', 0), 'unit', 0)\nbest_readiness, best_strength = (0, 0)\nwhile True:\n    member = roster.next_word()\n    frame = _first_word(frame, 'offset_y', member)\n    if negative_word(member):\n        return FirstLeaderFields(frame, selected)\n    rank = readiness.byte(member)\n    frame = _first_byte(frame, 'count', rank)\n    if leader_readiness_uses_byte_rank(rank):\n        if leader_readiness_should_replace(rank, best_readiness):\n            best_readiness = rank\n            selected = member\n            frame = _first_byte(frame, 'target_y', rank)\n            frame = _first_word(frame, 'target_x', selected)\n    else:\n        frame, strength = read_first_side_strength_fields(memory, frame, member)\n        if leader_strength_should_replace(strength, best_strength):\n            selected = member\n            best_readiness, best_strength = (rank, strength)\n            frame = _first_word(frame, 'target_x', selected)\n            frame = _first_transfer_word(frame, 'target_y', 'count')\n            frame = _first_word(frame, 'unit', strength)"}, 'copy_first_side_assignment_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, count: Word', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _first_frame(memory, frame)\nuint(count, 16)\nforce = memory.state.read(4294964876, 2)\nframe = _first_word(frame, 'target_x', force)\nframe = _first_shift_word(frame, 'target_x', force, 1)\ndirectory = memory.state.table(150500)\nformation = directory.word(u16(force << 1))\nframe = _first_word(frame, 'target_x', formation)\nframe = _first_shift_word(frame, 'target_x', formation, 4)\nintermediate = u16(formation << 4)\nframe = _first_add_word(frame, 'target_x', intermediate, count)\nintermediate = u16(intermediate + count)\nframe = _first_shift_word(frame, 'target_x', intermediate, 5)\noffset = formation_assignment_offset(formation, count)\ndestination = memory.state.table(4294946690).cursor()\nsource = memory.state.table(152684).cursor(offset)\nframe = first_replace(frame, roster=destination, candidates=source)\nreturn copy_first_side_order_fields(memory, frame)"}, 'copy_first_side_order_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _first_frame(memory, frame)\ndestination, source = (frame.roster, frame.candidates)\nchecked_policy_table(destination, memory.state)\nchecked_policy_table(source, memory.state)\nfor _ in range(10):\n    word = source.next_word()\n    destination.append_word(word)\n    frame = first_replace(frame, status=None if frame.status is None else frame.status & 16 | (8 if word & 32768 else 0) | (4 if word == 0 else 0))\nreturn frame'}, 'find_first_side_leader_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, selected: Word', 'returns': 'tuple[FirstDeploymentFrame, bool]', 'flow': "frame = _first_frame(memory, frame)\nuint(selected, 16)\nroster = memory.state.table(4294944080).cursor()\nframe = first_replace(frame, roster=roster)\nwhile True:\n    member = roster.next_word()\n    frame = _first_word(frame, 'target_y', member)\n    if negative_word(member):\n        return (frame, False)\n    frame = _first_compare_word(frame, member, selected)\n    if member == selected:\n        return (frame, True)"}, 'first_side_choice_prefix_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _first_frame(memory, frame)\nscene = memory.battle_scene()\nframe = _first_word(frame, 'target_x', scene)\nframe = _first_word(frame, 'target_y', scene)\noffset = scene\nfor shift in (1, 2, 1):\n    frame = _first_shift_word(frame, 'target_x', offset, shift)\n    offset = u16(offset << shift)\n    frame = _first_add_word(frame, 'target_x', offset, scene)\n    offset = u16(offset + scene)\nframe = _first_shift_word(frame, 'target_x', offset, 2)\nsource = memory.state.table(706398).cursor(u16(offset << 2))\ndestination = memory.state.table(4294955792).cursor()\nchoice = u16(memory.state.read(4294964764, 2) & 2)\nframe = _first_word(frame, 'target_x', choice)\ndestination.append_word(source.word(choice))\nif choice == 0:\n    frame = _first_add_word(frame, 'target_x', choice, 1)\n    choice = 1\nscene = memory.battle_scene()\nframe = _first_word(frame, 'target_y', scene)\nvariant = memory.state.table(4294942719)\nvariant.set_byte(scene, u8(choice))\nsource.base = source.advance(4).base\nclear = destination.cursor()\nframe = first_replace(frame, roster=source, candidates=destination, controller=clear, auxiliary=variant)\nframe = _first_word(frame, 'target_x', 7)\nfor _ in descending_inclusive(7):\n    clear.word()\n    clear.append_word(0)\nframe = _first_counter_end(frame, 'target_x')\nreturn first_replace(frame, status=None if frame.status is None else frame.status & 16 | 4)"}, 'initialize_first_side_deployment_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _first_frame(memory, frame)\nframe = _first_call(memory, frame, 152430, _first_promote_frame)\nframe = _first_call(memory, frame, 152434, prepare_first_side_assignment_fields)\nreturn _first_call(memory, frame, 152438, populate_first_side_fields)'}, 'move_first_side_leader_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, selected: Word', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _first_frame(memory, frame)\nuint(selected, 16)\nhead = memory.state.table(4294942759)\nscene = memory.battle_scene()\nframe = _first_word(frame, 'target_y', scene)\nhead.set_byte(scene, u8(selected))\nsource = memory.state.table(4294944080).cursor()\ndestination = memory.state.table(4294944080).cursor()\nframe = first_replace(frame, roster=source, candidates=destination)\npending = selected\nframe = _first_word(frame, 'unit', pending)\nwhile True:\n    member = source.next_word()\n    frame = _first_word(frame, 'target_y', member)\n    if negative_word(member):\n        break\n    frame = _first_compare_word(frame, member, selected)\n    if member == selected:\n        continue\n    destination.append_word(pending)\n    frame = _first_word(frame, 'unit', member)\n    pending = member\nframe = _first_compare_word(frame, member, selected)\nif member != selected:\n    destination.put_word(pending)\n    frame = _first_word(frame, 'unit', pending)\nreturn frame"}, 'populate_first_side_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _first_call(memory, frame, 154224, prepare_first_side_choices_fields)\nroster = memory.state.table(4294944080).cursor()\norders = memory.state.table(4294946690).cursor()\ncells = memory.state.table(4294955792)\npositions = memory.state.table(4294943056)\nframe = first_replace(frame, roster=roster, candidates=orders, controller=cells, scan=positions.cursor())\nreturn submit_unset_deployment_fields(memory, frame)'}, 'prepare_first_side_assignment_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _first_frame(memory, frame)\nroster = memory.state.table(4294944080)\nframe, count = read_first_side_assignment_count_fields(memory, frame, roster)\nreturn _first_call(memory, frame, 152630, lambda memory, frame: copy_first_side_assignment_fields(memory, frame, count))'}, 'prepare_first_side_choices_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = first_side_choice_prefix_fields(memory, frame)\nsource, destination = (frame.roster, frame.candidates)\nfor continuation in (154372, 154376, 154380, 154384, 154388, 154392, 154396, 154400):\n    frame = _first_call(memory, frame, continuation, choose_unused_first_side_fields)\n    source, destination = (frame.roster, frame.candidates)\nframe = prepare_first_side_reserve_fields(memory, frame)\nreturn submit_first_side_reserve_fields(memory, frame)'}, 'prepare_first_side_reserve_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _first_frame(memory, frame)\nsource = frame.roster\nchecked_policy_table(source, memory.state)\nscratch = memory.state.table(4294955776).cursor()\nframe = first_replace(frame, controller=scratch)\nif memory.battle_scene() != 23:\n    frame = _first_word(frame, 'target_x', 3)\n    for _ in descending_inclusive(3):\n        scratch.word(0, 8)\n        scratch.set_word(0, 0, 8)\n        word = source.next_word()\n        scratch.append_word(word)\n        frame = _first_memory_word(frame, word)\n    frame = _first_counter_end(frame, 'target_x')\n    continuation = 154432\nelse:\n    frame = _first_word(frame, 'target_x', 7)\n    for _ in descending_inclusive(7):\n        scratch.word()\n        scratch.put_word(0)\n        frame = _first_memory_word(frame, 0)\n    frame = _first_counter_end(frame, 'target_x')\n    if memory.state.read(4294955793, 1) >= 20:\n        source.base = source.advance(4).base\n    word = source.word()\n    memory.state.table(4294955776).set_word(0, word)\n    frame = _first_memory_word(frame, word)\n    word = source.word(2)\n    memory.state.table(4294955776).set_word(2, word)\n    frame = _first_memory_word(frame, word)\n    continuation = 154478\nreturn _first_call(memory, frame, continuation, shuffle_first_side_choice_fields)"}, 'promote_first_side_leader_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstLeaderFields', 'flow': "frame = _first_frame(memory, frame)\nforce = memory.state.read(4294964876, 2)\nframe = _first_word(frame, 'target_x', force)\nframe = _first_shift_word(frame, 'target_x', force, 1)\nrulers = memory.state.table(4294960704).cursor()\nselected = rulers.word(u16(force << 1))\nframe = _first_word(frame, 'target_x', selected)\nframe = first_replace(frame, candidates=rulers)\nframe, found = find_first_side_leader_fields(memory, frame, selected)\nif not found:\n    result = choose_first_side_leader_fields(memory, frame, selected)\n    frame, selected = (result.frame, result.selected)\nframe = move_first_side_leader_fields(memory, frame, selected)\nreturn FirstLeaderFields(frame, selected)"}, 'read_first_side_assignment_count_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, roster', 'returns': 'tuple[FirstDeploymentFrame, Word]', 'flow': "frame = _first_frame(memory, frame)\nchecked_policy_table(roster, memory.state)\nthird = roster.word(4)\nframe = _first_memory_word(frame, third)\nif not negative_word(third):\n    second = roster.word(2)\n    frame = _first_memory_word(frame, second)\n    if not negative_word(second):\n        if type(memory.state) is GameState and frame.stack_cursor is None:\n            frame, count = sort_first_side_roster_fields(memory, frame)\n        else:\n            frame = _first_call(memory, frame, 152610, _first_sorted_frame)\n            count = low16(frame.unit)\n        return (frame, count)\ncount = 0\nframe = _first_word(frame, 'unit', count)\nsecond = roster.word(2)\nframe = _first_memory_word(frame, second)\nif not negative_word(second):\n    frame = _first_add_word(frame, 'unit', count, 1)\n    count = 1\nreturn (frame, count)"}, 'read_first_side_strength_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, member: Word', 'returns': 'tuple[FirstDeploymentFrame, Word]', 'flow': "frame = _first_frame(memory, frame)\nuint(member, 16)\nchecked_policy_table(frame.controller, memory.state)\nchecked_policy_table(frame.scan, memory.state)\nframe = _first_word(frame, 'distance', member)\nframe = _first_shift_word(frame, 'distance', member, 1)\noffset = u16(member << 1)\nfirst = frame.controller.word(offset)\nframe = _first_word(frame, 'offset_x', first)\nsecond = frame.scan.word(offset)\nframe = _first_add_word(frame, 'offset_x', first, second)\nreturn (frame, u16(first + second))"}, 'submit_first_side_reserve_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _first_frame(memory, frame)\ndestination = frame.candidates\nchecked_policy_table(destination, memory.state)\nscratch = memory.state.table(4294955776)\nselected = memory.state.table(16727754)\nword = scratch.word()\ndestination.append_word(word)\nframe = _first_memory_word(frame, word)\nword = scratch.word()\nselected.set_word(0, word)\nframe = _first_memory_word(frame, word)\nword = scratch.word(2)\ndestination.put_word(word)\nframe = _first_memory_word(frame, word)\nword = scratch.word(2)\nselected.set_word(2, word)\nreturn _first_memory_word(frame, word)'}, 'submit_unset_deployment_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _first_frame(memory, frame)\nroster, orders, cells, positions = (frame.roster, frame.candidates, frame.controller, frame.scan)\nchecked_policy_table(roster, memory.state)\nchecked_policy_table(orders, memory.state)\nchecked_policy_table(cells, memory.state)\nchecked_policy_table(positions, memory.state)\nwhile True:\n    member = roster.next_word()\n    frame = _first_word(frame, 'target_x', member)\n    if negative_word(member):\n        return frame\n    frame = _first_shift_word(frame, 'target_x', member, 2)\n    offset = u16(member << 2)\n    order = orders.next_word()\n    frame = _first_word(frame, 'target_y', order)\n    frame = _first_shift_word(frame, 'target_y', order, 1)\n    order = u16(order << 1)\n    if deployment_position_needs_assignment(positions.word(offset)):\n        frame = write_unset_deployment_fields(memory, frame, offset, order)"}, 'write_unset_deployment_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, offset: Word, order: Word', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _first_frame(memory, frame)\nuint(offset, 16)\nuint(order, 16)\ncells, positions = (frame.controller, frame.scan)\nchecked_policy_table(cells, memory.state)\nchecked_policy_table(positions, memory.state)\nfor displacement in (0, 1):\n    frame = _first_word(frame, 'unit', 0)\n    value = cells.byte(order, displacement)\n    frame = _first_byte(frame, 'unit', value)\n    frame = _first_shift_word(frame, 'unit', value, 3)\n    frame = _first_shift_word(frame, 'unit', u16(value << 3), 7)\n    positions.set_word(offset, u16(value << 10), displacement * 2)\nreturn frame"}})
APPROVED['domain'].update({'replace_byte', 'replace_word'})
APPROVED['contexts_policy_memory'] = {'BattlePolicyMemory', 'checked_policy_table'}
APPROVED['contexts_first_deployment'] = {'FirstDeploymentFrame', 'FirstLeaderFields', 'FirstDeploymentReturnBoundary', 'first_replace'}

DEPLOYMENT_INLINE_DECLARATIONS.update({'_first_compare_long': {'signature': 'frame: FirstDeploymentFrame, left: Long, right: Long', 'returns': 'FirstDeploymentFrame', 'flow': 'uint(left, 32)\nuint(right, 32)\nvalue = u32(left - right)\noverflow = bool((left ^ right) & (left ^ value) & 2147483648)\nstatus = None if frame.status is None else frame.status & 16 | (1 if left < right else 0) | (2 if overflow else 0) | (8 if value & 2147483648 else 0) | (4 if value == 0 else 0)\nreturn first_replace(frame, status=status)'}, '_first_long': {'signature': 'frame: FirstDeploymentFrame, name, value: Long', 'returns': 'FirstDeploymentFrame', 'flow': 'uint(value, 32)\nstatus = None if frame.status is None else frame.status & 16 | (8 if value & 2147483648 else 0) | (4 if value == 0 else 0)\nreturn first_replace(frame, **{name: value}, status=status)'}, '_first_right_word': {'signature': 'frame: FirstDeploymentFrame, name, original: Word, count: Word', 'returns': 'FirstDeploymentFrame', 'flow': "uint(original, 16)\nuint(count, 16)\nif not 1 <= count <= 8:\n    raise ValueError('bounded original WORD shift required')\nvalue = original >> count\nbit = bool(original & 1 << count - 1)\nretained = frame.carrier(name)\ncarrier = None if retained is None else replace_word(retained, value)\nstatus = (17 if bit else 0) | (4 if value == 0 else 0)\nreturn first_replace(frame, **{name: carrier}, status=status)"}, '_first_sorted_frame': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return sort_first_side_roster_fields(memory, frame)[0]'}, '_first_sub_word': {'signature': 'frame: FirstDeploymentFrame, name, left: Word, right: Word', 'returns': 'FirstDeploymentFrame', 'flow': 'uint(left, 16)\nuint(right, 16)\nvalue = u16(left - right)\nretained = frame.carrier(name)\ncarrier = None if retained is None else replace_word(retained, value)\noverflow = bool((left ^ right) & (left ^ value) & 32768)\nstatus = (17 if left < right else 0) | (2 if overflow else 0) | (8 if value & 32768 else 0) | (4 if value == 0 else 0)\nreturn first_replace(frame, **{name: carrier}, status=status)'}, '_first_training_frame': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, member: Word', 'returns': 'FirstDeploymentFrame', 'flow': 'return weighted_training_factor_fields(memory, frame, member).frame'}, 'choose_unused_first_side_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _first_frame(memory, frame)\nsource, destination = (frame.roster, frame.candidates)\nchecked_policy_table(source, memory.state)\nchecked_policy_table(destination, memory.state)\nchoices = memory.state.table(4294955776).cursor()\nframe = first_replace(frame, controller=choices)\nframe = _first_word(frame, 'target_x', 5)\nfor _ in descending_inclusive(5):\n    word = source.next_word()\n    choices.append_word(word)\n    frame = _first_memory_word(frame, word)\nframe = _first_counter_end(frame, 'target_x')\nchoices.word()\nchoices.append_word(0)\nframe = _first_memory_word(frame, 0)\nchoices.word()\nchoices.put_word(0)\nframe = _first_memory_word(frame, 0)\nframe = _first_call(memory, frame, 154526, shuffle_first_side_choice_fields)\nchoices = memory.state.table(4294955776).cursor()\nframe = first_replace(frame, controller=choices)\ndeployed = memory.state.table(4294955792)\nwhile True:\n    candidate = choices.next_word()\n    frame = _first_word(frame, 'target_x', candidate)\n    duplicate = False\n    for offset in range(2, 18, 2):\n        previous = deployed.word(offset)\n        frame = _first_compare_word(frame, candidate, previous)\n        if candidate == previous:\n            duplicate = True\n            break\n    if not duplicate:\n        destination.append_word(candidate)\n        return _first_memory_word(frame, candidate)"}, 'collect_first_side_weight_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple[FirstDeploymentFrame, Word]', 'flow': "frame = _first_frame(memory, frame)\nsource, weights = (frame.roster, frame.candidates)\nchecked_policy_table(source, memory.state)\nchecked_policy_table(weights, memory.state)\nchecked_policy_table(frame.scan, memory.state)\nframe = _first_word(frame, 'unit', 0)\ncount = 0\nwhile True:\n    member = source.next_word()\n    frame = _first_word(frame, 'target_x', member)\n    if negative_word(member):\n        break\n    frame = _first_add_word(frame, 'unit', count, 1)\n    count = u16(count + 1)\n    frame = _first_call(memory, frame, 150366, lambda memory, frame: _first_training_frame(memory, frame, member))\n    source = frame.roster\n    current = member if type(memory.state) is GameState and frame.target_x is None else low16(frame.target_x)\n    frame = _first_shift_word(frame, 'target_x', current, 2)\n    troops = frame.scan.long(u16(current << 2))\n    frame = _first_long(frame, 'target_x', troops)\n    product = weighted_deployment_product(troops, frame.target_y)\n    frame = _first_long(frame, 'target_x', product)\n    weights = frame.candidates\n    weights.append_long(product)\nreturn (frame, count)"}, 'first_deployment_random_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame',
 'returns': 'FirstDeploymentFrame',
 'flow': 'if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:\n'
         "    raise ValueError('same-state RNG memory and actual frame required')\n"
         'frame.validate(memory.state, frame.stack_cursor is not None)\n'
         'sample = memory.sample_random_pair()\n'
         'uint(sample.sample, 32)\n'
         'uint(sample.updated_state, 32)\n'
         'high_mixed = low16(sample.updated_state)\n'
         'low_mixed = u16(low16(sample.sample) - high_mixed)\n'
         'extend = low_mixed + high_mixed > 65535\n'
         'status = (16 if extend else 0) | (8 if sample.updated_state & 2147483648 else 0) | (4 if '
         'sample.updated_state == 0 else 0)\n'
         'return first_replace(frame, target_x=sample.sample, target_y=sample.updated_state, '
         'status=status)'}, 'order_first_side_weight_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, count: Word, limit: Word', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _first_frame(memory, frame)\nuint(count, 16)\nuint(limit, 16)\nstart = 0\nwhile True:\n    offset = limit\n    frame = _first_word(frame, 'distance', offset)\n    frame = _first_word(frame, 'target_y', offset)\n    member_offset = u16(offset >> 1)\n    frame = _first_right_word(frame, 'target_y', offset, 1)\n    frame = _first_word(frame, 'offset_x', start)\n    while True:\n        value = frame.candidates.long(offset)\n        frame = _first_long(frame, 'offset_y', value)\n        previous = frame.candidates.long(offset, -4)\n        frame = _first_compare_long(frame, value, previous)\n        if weighted_neighbor_should_move_forward(value, previous):\n            frame = swap_first_side_weight_fields(memory, frame, offset, member_offset, value)\n        frame = _first_sub_word(frame, 'distance', offset, 4)\n        offset = u16(offset - 4)\n        frame = _first_sub_word(frame, 'target_y', member_offset, 2)\n        member_offset = u16(member_offset - 2)\n        frame = _first_compare_word(frame, offset, start)\n        if not offset > start:\n            break\n    frame = _first_add_word(frame, 'count', start, 4)\n    start = u16(start + 4)\n    frame = _first_compare_word(frame, start, limit)\n    if not start < limit:\n        return frame"}, 'read_first_side_weighted_roster_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _first_frame(memory, frame)\nalternate = bool(memory.state.read(4294964951, 1) & 2)\nselected = memory.state.table(4294944166 if alternate else 4294944082)\nframe = first_replace(frame, roster=selected.cursor(), candidates=memory.state.table(4294955776).cursor(), controller=memory.state.table(4294947840), scan=memory.state.table(4294952960).cursor(), opponent=selected, auxiliary=memory.state.table(4294961800))\nreturn frame'}, 'shuffle_first_side_choice_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _first_frame(memory, frame)\nchoices = memory.state.table(4294955776).cursor()\nframe = first_replace(frame, controller=choices)\nframe = _first_word(frame, 'unit', 15)\nfor counter in descending_inclusive(15):\n    frame = _first_call(memory, frame, 152328, first_deployment_random_fields)\n    sample = low16(frame.target_x)\n    frame = _first_transfer_word(frame, 'target_y', 'target_x')\n    slots = shuffle_slots_from_sample(sample)\n    frame = _first_word(frame, 'target_x', slots.first)\n    frame = _first_right_word(frame, 'target_y', sample, 4)\n    frame = _first_word(frame, 'target_y', slots.second)\n    frame = swap_nonzero_choice_fields(memory, frame, choices, slots)\n    retained = frame.unit\n    frame = first_replace(frame, unit=None if retained is None else replace_word(retained, u16(counter - 1)))\nreturn _first_counter_end(frame, 'unit')"}, 'sort_first_side_roster_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple[FirstDeploymentFrame, Word]', 'flow': "frame = read_first_side_weighted_roster_fields(memory, frame)\nframe, count = collect_first_side_weight_fields(memory, frame)\nframe = _first_transfer_word(frame, 'target_x', 'unit')\nframe = _first_sub_word(frame, 'target_x', count, 1)\nlimit = u16(u16(count - 1) << 2)\nframe = _first_shift_word(frame, 'target_x', u16(count - 1), 2)\nframe = _first_word(frame, 'count', 0)\nweights = memory.state.table(4294955776).cursor()\nroster = frame.opponent.cursor()\nframe = first_replace(frame, roster=roster, candidates=weights)\nreturn (order_first_side_weight_fields(memory, frame, count, limit), count)"}, 'swap_first_side_weight_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, offset: Word, member_offset: Word, value: Long', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _first_frame(memory, frame)\nuint(offset, 16)\nuint(member_offset, 16)\nuint(value, 32)\nprevious = frame.candidates.long(offset, -4)\nframe.candidates.set_long(offset, previous)\nframe = _first_long(frame, 'offset_y', value)\nframe.candidates.set_long(offset, value, -4)\nmember = frame.roster.word(member_offset)\nframe = _first_word(frame, 'offset_y', member)\nprevious_member = frame.roster.word(member_offset, -2)\nframe.roster.set_word(member_offset, previous_member)\nframe = _first_memory_word(frame, previous_member)\nframe.roster.set_word(member_offset, member, -2)\nreturn _first_memory_word(frame, member)"}, 'swap_nonzero_choice_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, choices, slots: ShuffleSlots', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _first_frame(memory, frame)\nchecked_policy_table(choices, memory.state)\nif type(slots) is not ShuffleSlots:\n    raise ValueError('typed shuffle slots required')\nfirst = choices.word(slots.first)\nframe = _first_memory_word(frame, first)\nif first == 0:\n    return frame\nsecond = choices.word(slots.second)\nframe = _first_memory_word(frame, second)\nif second == 0:\n    return frame\nfirst = choices.word(slots.first)\nframe = _first_word(frame, 'count', first)\nsecond = choices.word(slots.second)\nchoices.set_word(slots.first, second)\nframe = _first_memory_word(frame, second)\nchoices.set_word(slots.second, first)\nreturn _first_memory_word(frame, first)"}})
APPROVED['business_geometry'].add('weighted_training_factor_fields')


# Original239D6/239F4 unique complete field kernels.
INLINE_DECLARATIONS.update({'sum_first_side_roster_troops_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple[FirstDeploymentFrame, Word, Long]', 'flow': "frame = _first_frame(memory, frame)\nroster = memory.state.table(4294944080).cursor()\ntroops = memory.state.table(4294952960).cursor()\nframe = first_replace(frame, roster=roster, candidates=troops)\nframe = _first_word(frame, 'unit', 0)\nframe = first_replace(frame, count=0, status=None if frame.status is None else frame.status & 16 | 4)\nbyte_length, total = (0, 0)\nwhile True:\n    member = roster.next_word()\n    frame = _first_word(frame, 'offset_x', member)\n    if negative_word(member):\n        return (frame, byte_length, total)\n    frame = _first_add_word(frame, 'unit', byte_length, 2)\n    byte_length = u16(byte_length + 2)\n    frame = _first_shift_word(frame, 'offset_x', member, 2)\n    amount = troops.long(u16(member << 2))\n    wide = total + amount\n    value = u32(wide)\n    overflow = bool(~(total ^ amount) & (total ^ value) & 2147483648)\n    status = (17 if wide > 4294967295 else 0) | (8 if value & 2147483648 else 0) | (4 if value == 0 else 0) | (2 if overflow else 0)\n    total = value\n    frame = first_replace(frame, count=total, status=status)"}, 'test_force_has_city_assignment_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple[FirstDeploymentFrame, bool]', 'flow': "frame = _first_frame(memory, frame)\nframe = _first_word(frame, 'distance', 39)\nforce = memory.state.read(4294964876, 2)\nframe = _first_word(frame, 'target_x', force)\nowners = memory.state.table(4294964264).cursor()\nframe = first_replace(frame, roster=owners)\nfor city in descending_inclusive(39):\n    owner = owners.byte(city)\n    left = u8(force)\n    difference = u8(left - owner)\n    overflow = bool((left ^ owner) & (left ^ difference) & 128)\n    status = None if frame.status is None else frame.status & 16 | (1 if left < owner else 0) | (2 if overflow else 0) | (8 if difference & 128 else 0) | (4 if difference == 0 else 0)\n    frame = first_replace(frame, status=status)\n    if left == owner:\n        return (_order_city_assignment_carry(memory, frame, True), True)\n    if frame.distance is not None:\n        frame = first_replace(frame, distance=replace_word(frame.distance, u16(city - 1)))\nreturn (_order_city_assignment_carry(memory, frame, False), False)", 'slots': {39: ['city_latch', 0, 65535]}}, '_order_city_assignment_carry': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, assigned: bool', 'returns': 'FirstDeploymentFrame', 'flow': "if type(assigned) is not bool:\n    raise ValueError('actual city assignment result required')\nif not memory.state.sr & 8192:\n    raise Boundary('original city-assignment full-SR operation requires supervisor')\nif memory.state.sr & 32768:\n    raise Boundary('original city-assignment trace continuation unmodeled')\nstatus = None if frame.status is None else frame.status & 30 | int(assigned)\nreturn first_replace(frame, status=status)"}})
APPROVED['domain'].add('Boundary')

# Root: sole23C9A complete gate; legacy projection has the same authority.
DECLARATIONS.update({"test_second_side_relative_total_shortfall":{"signature":"state: GameState","returns":"CarryOutcome","flow":"checked_state(state)\n_, selected = test_second_side_relative_total_shortfall_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())\nreturn state.carry_result(int(selected))"}})
INLINE_DECLARATIONS.update({"test_second_side_relative_total_shortfall_fields":{"signature":"memory: BattlePolicyMemory, frame: FirstDeploymentFrame","returns":"tuple[FirstDeploymentFrame, bool]","flow":"frame = _first_frame(memory, frame)\ntotal = memory.state.read(4294964898, 4)\nstatus = None if frame.status is None else frame.status & 16 | (8 if total & 2147483648 else 0) | (4 if total == 0 else 0)\nframe = first_replace(frame, target_x=total, status=status)\nprimary = memory.state.read(4294964894, 4)\nframe = _first_compare_long(frame, total, primary)\nselected = False\nif total < primary:\n    limit = memory.state.read(4294965100, 4)\n    frame = _first_compare_long(frame, total, limit)\n    selected = total < limit\nreturn (_battle_roster_gate_carry(memory, frame, selected), selected)"}})


# Complete actual second-side strength/roster fields.
INLINE_DECLARATIONS.update({'_read_second_side_strength_gate_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple[FirstDeploymentFrame, bool]', 'flow': 'frame = _first_frame(memory, frame)\ntotal = memory.state.read(4294964898, 4)\nstatus = None if frame.status is None else frame.status & 16 | (8 if total & 2147483648 else 0) | (4 if total == 0 else 0)\nframe = first_replace(frame, target_x=total, status=status)\nlimit = memory.state.read(4294965100, 4)\nframe = _first_compare_long(frame, total, limit)\nreturn (frame, total >= limit)'}, '_battle_roster_gate_carry': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, selected: bool', 'returns': 'FirstDeploymentFrame', 'flow': "if type(selected) is not bool:\n    raise ValueError('actual strength/roster gate decision required')\nif not memory.state.sr & 8192:\n    raise Boundary('original strength gate full-SR operation requires supervisor')\nif memory.state.sr & 32768:\n    raise Boundary('original strength gate trace continuation unmodeled')\nstatus = None if frame.status is None else frame.status & 30 | int(selected)\nreturn first_replace(frame, status=status)"}, 'test_second_side_total_with_single_first_roster_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple[FirstDeploymentFrame, bool]', 'flow': 'frame, enough_strength = _read_second_side_strength_gate_fields(memory, frame)\nselected = False\nif enough_strength:\n    second = memory.state.read(4294944082, 2)\n    frame = _first_memory_word(frame, second)\n    selected = negative_word(second)\nreturn (_battle_roster_gate_carry(memory, frame, selected), selected)'}, 'test_second_side_total_with_small_second_roster_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple[FirstDeploymentFrame, bool]', 'flow': 'frame, enough_strength = _read_second_side_strength_gate_fields(memory, frame)\nselected = False\nif enough_strength:\n    for address in (4294944166, 4294944168, 4294944170):\n        member = memory.state.read(address, 2)\n        frame = _first_memory_word(frame, member)\n        if negative_word(member):\n            selected = True\n            break\nreturn (_battle_roster_gate_carry(memory, frame, selected), selected)'}})

# Root: current whole staging cores and WORD-only legacy projections.
DECLARATIONS.update({'test_point_in_battlefield_staging_rectangle': {'signature': 'state: GameState, point: Point', 'returns': 'tuple', 'flow': "checked_state(state)\nif type(point) is not Point:\n    raise ValueError('typed point required')\nframe = first_replace(FirstDeploymentFrame.unobserved(), target_x=point.x, target_y=point.y, unit=0, count=0, distance=0, offset_x=0, offset_y=0, status=state.sr & 31)\nframe = test_point_in_battlefield_staging_rectangle_fields(BattlePolicyMemory(state), frame)\nbounds = BattleBounds(low16(frame.unit), low16(frame.count), low16(frame.distance), low16(frame.offset_x))\nreturn (bounds, state.carry_result(frame.status & 1))"}, 'sample_battlefield_staging_rectangle': {'signature': 'state: GameState, bounds: BattleBounds', 'returns': 'Point', 'flow': "checked_state(state)\nif type(bounds) is not BattleBounds:\n    raise ValueError('typed bounds required')\nframe = first_replace(FirstDeploymentFrame.unobserved(), target_x=0, target_y=0, unit=bounds.left, count=bounds.right, distance=bounds.lower, offset_x=bounds.upper, status=state.sr & 31)\nframe = sample_battlefield_staging_rectangle_fields(BattlePolicyMemory(state), frame)\nreturn Point(low16(frame.unit), low16(frame.distance))"}})
INLINE_DECLARATIONS.update({'test_point_in_battlefield_staging_rectangle_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _first_frame(memory, frame)\nframe = _first_word(frame, 'offset_y', memory.state.read(4294964874, 2))\nframe = first_replace(frame, roster=memory.state.table(713462).cursor())\nframe = _first_shift_word(frame, 'offset_y', low16(frame.offset_y), 2)\noffset = low16(frame.offset_y)\nframe = _first_compare_word(frame, offset, 92)\nframe = _first_word(frame, 'unit', frame.roster.word(offset))\nframe = _first_transfer_word(frame, 'count', 'unit')\nif offset != 92:\n    frame = _first_sub_word(frame, 'unit', low16(frame.unit), 4096)\n    if frame.status & 1:\n        frame = _first_word(frame, 'unit', 3072)\n    else:\n        frame = _first_compare_word(frame, low16(frame.unit), 3072)\n        if frame.status & 1:\n            frame = _first_word(frame, 'unit', 3072)\n    frame = _first_add_word(frame, 'count', low16(frame.count), 4096)\n    if frame.status & 1:\n        frame = _first_word(frame, 'count', 25600)\n    else:\n        frame = _first_compare_word(frame, low16(frame.count), 25600)\n        if not frame.status & 5:\n            frame = _first_word(frame, 'count', 25600)\n    frame = _first_word(frame, 'distance', frame.roster.word(offset, 2))\n    frame = _first_transfer_word(frame, 'offset_x', 'distance')\n    frame = _first_compare_word(frame, low16(frame.distance), 20480)\n    if frame.status & 1:\n        frame = _first_add_word(frame, 'offset_x', low16(frame.offset_x), 14336)\n    else:\n        frame = _first_sub_word(frame, 'distance', low16(frame.distance), 14336)\nelse:\n    frame = _first_sub_word(frame, 'count', low16(frame.count), 13312)\n    frame = _first_word(frame, 'distance', frame.roster.word(offset, 2))\n    frame = _first_transfer_word(frame, 'offset_x', 'distance')\n    frame = _first_sub_word(frame, 'distance', low16(frame.distance), 3072)\n    frame = _first_add_word(frame, 'offset_x', low16(frame.offset_x), 3072)\nfor coordinate, limit, lower_bound in ((frame.target_x, frame.unit, True), (frame.target_x, frame.count, False), (frame.target_y, frame.distance, True), (frame.target_y, frame.offset_x, False)):\n    frame = _first_compare_word(frame, low16(coordinate), low16(limit))\n    outside = bool(frame.status & 1) if lower_bound else not bool(frame.status & 5)\n    if outside:\n        return _battle_roster_gate_carry(memory, frame, False)\nreturn _battle_roster_gate_carry(memory, frame, True)"}, '_staging_scaled_sample_fields': {'signature': 'frame: FirstDeploymentFrame, span: Word', 'returns': 'FirstDeploymentFrame', 'flow': "uint(span, 16)\nframe = _first_long(frame, 'target_x', low16(frame.target_x))\nframe = _first_long(frame, 'target_x', low16(frame.target_x) * span)\nproduct = frame.target_x\nswapped = u32(low16(product) << 16 | product >> 16)\nreturn _first_long(frame, 'target_x', swapped)"}, 'sample_battlefield_staging_rectangle_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _first_frame(memory, frame)\nframe = _first_sub_word(frame, 'count', low16(frame.count), low16(frame.unit))\nframe = _first_call(memory, frame, 146350, first_deployment_random_fields)\nframe = _staging_scaled_sample_fields(frame, low16(frame.count))\nframe = _first_add_word(frame, 'unit', low16(frame.unit), low16(frame.target_x))\nframe = _first_sub_word(frame, 'offset_x', low16(frame.offset_x), low16(frame.distance))\nframe = _first_sub_word(frame, 'offset_x', low16(frame.offset_x), 3072)\nframe = _first_call(memory, frame, 146374, first_deployment_random_fields)\nframe = _staging_scaled_sample_fields(frame, low16(frame.offset_x))\nframe = first_replace(frame, roster=memory.state.table(713462).cursor())\nframe = _first_word(frame, 'target_y', memory.state.read(4294964874, 2))\nframe = _first_shift_word(frame, 'target_y', low16(frame.target_y), 2)\nframe = _first_compare_word(frame, frame.roster.word(low16(frame.target_y), 2), 20480)\nlower_side = bool(frame.status & 1)\nframe = _first_add_word(frame, 'distance', low16(frame.distance), low16(frame.target_x))\nif lower_side:\n    frame = _first_add_word(frame, 'distance', low16(frame.distance), 3072)\nreturn frame"}})

FAMILY_DECLARATIONS.update({'compare_actor_shifted_troop_word_to_weakest_contact': {'signature': 'state: GameState, actor: Word', 'returns': 'CarryOutcome', 'flow': 'checked_state(state)\nuint(actor, 16)\nframe = first_replace(FirstDeploymentFrame.unobserved(), choice=actor)\nframe, accepted = compare_actor_shifted_troop_word_to_weakest_contact_fields(BattlePolicyMemory(state), frame)\nreturn state.carry_result(int(accepted))'}})

FAMILY_DECLARATIONS.update({'read_outer_east_staging_anchor': {'signature': 'state: GameState', 'returns': 'Point', 'flow': 'checked_state(state)\nreturn read_outer_east_staging_anchor_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())[1]'}})

FAMILY_DECLARATIONS.update({'select_contact_nearest_deployment_anchor': {'signature': 'state: GameState, retained_unit: Word=0', 'returns': 'ClosestBattleUnit', 'flow': 'checked_state(state)\nuint(retained_unit, 16)\nreturn select_contact_nearest_deployment_anchor_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), retained_unit)[1]'}})

FAMILY_DECLARATIONS.update({'read_formation_relative_position_delta': {'signature': 'state: GameState, retained_position: Word=0', 'returns': 'Word', 'flow': 'checked_state(state)\nuint(retained_position, 16)\nreturn read_formation_relative_position_delta_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), retained_position)[1]'}})

INLINE_DECLARATIONS.update({'_formation_position_frame': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:\n    raise ValueError('same-state position memory and sole actual frame required')\nreturn frame.validate(memory.state, frame.stack_cursor is not None)"}})

INLINE_DECLARATIONS.update({'_formation_position_enter': {'signature': 'frame: FirstDeploymentFrame, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': 'uint(continuation, 32)\nif frame.stack_cursor is None:\n    return frame\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nreturn first_replace(frame, stack_cursor=stack)'}})

INLINE_DECLARATIONS.update({'_formation_position_leave': {'signature': 'frame: FirstDeploymentFrame, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': 'uint(continuation, 32)\nif frame.stack_cursor is None:\n    return frame\nstack = frame.stack_cursor\ntarget = stack.long()\nif target != continuation:\n    raise FirstDeploymentReturnBoundary(target, frame, continuation)\nreturn first_replace(frame, stack_cursor=stack.advance(4))'}})

INLINE_DECLARATIONS.update({'_formation_position_carry': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, enabled: bool', 'returns': 'FirstDeploymentFrame', 'flow': "if type(enabled) is not bool:\n    raise ValueError('actual position carry outcome required')\nif type(memory.state) is not GameState:\n    if not memory.state.sr & 8192:\n        raise Boundary('original position full-SR operation requires supervisor')\n    if memory.state.sr & 32768:\n        raise Boundary('position trace continuation remains unmodeled')\nstatus = None if frame.status is None else frame.status & 30 | int(enabled)\nif type(memory.state) is not GameState and status is not None:\n    memory.state.sr = memory.state.sr & 65504 | status\nreturn first_replace(frame, status=status)"}})

INLINE_DECLARATIONS.update({'compare_actor_shifted_troop_word_to_weakest_contact_fields': {'slots': {}, 'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': "from .business_geometry import collect_contacts_in_speed_radius_fields, select_weakest_contact_strength_fields\nframe = _formation_position_frame(memory, frame)\nuint(frame.choice, 32)\nretained_x, retained_y = (frame.target_x, frame.target_y)\nstack = frame.stack_cursor\nif stack is not None:\n    stack = stack.advance(-4)\n    stack.set_long(0, retained_y)\n    stack = stack.advance(-4)\n    stack.set_long(0, retained_x)\n    frame = first_replace(frame, stack_cursor=stack)\nentered = _formation_position_enter(frame, 148392)\nframe = collect_contacts_in_speed_radius_fields(memory, entered).frame\nframe = _formation_position_leave(frame, 148392)\ncontacts = memory.state.read(4294955776, 2)\nframe = _first_memory_word(frame, contacts)\naccepted = False\nif not negative_word(contacts):\n    entered = _formation_position_enter(frame, 148404)\n    frame = select_weakest_contact_strength_fields(memory, entered, 0 if entered.count is None else low16(entered.count), 0 if entered.target_y is None else entered.target_y)[0]\n    frame = _formation_position_leave(frame, 148404)\n    actor = low16(frame.choice)\n    frame = _first_word(frame, 'target_x', actor)\n    entered = _formation_position_enter(frame, 148412)\n    frame = weighted_training_factor_fields(memory, entered, actor).frame\n    frame = _formation_position_leave(frame, 148412)\n    actor = actor if frame.target_x is None else low16(frame.target_x)\n    frame = _first_shift_word(frame, 'target_x', actor, 2)\n    troops = frame.candidates.long(u16(actor << 2), 2)\n    frame = first_replace(frame, target_x=troops)\n    frame = _first_long(frame, 'target_x', troops)\n    strength = low16(troops) * low16(frame.target_y)\n    frame = _first_long(frame, 'target_x', strength)\n    frame = _first_compare_long(frame, frame.unit, strength)\n    accepted = frame.unit <= strength\nframe = _formation_position_carry(memory, frame, accepted)\nstack = frame.stack_cursor\nif stack is not None:\n    retained_x = stack.long()\n    stack = stack.advance(4)\n    retained_y = stack.long()\n    stack = stack.advance(4)\nframe = first_replace(frame, target_x=retained_x, target_y=retained_y, stack_cursor=stack)\nreturn (frame, accepted)"}})

INLINE_DECLARATIONS.update({'read_outer_east_staging_anchor_fields': {'slots': {}, 'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': "frame = _formation_position_frame(memory, frame)\norigin = memory.state.table(713462).cursor()\nframe = first_replace(frame, roster=origin)\nscene = memory.battle_scene()\nframe = _first_word(frame, 'target_x', scene)\noffset = u16(scene << 2)\nframe = _first_shift_word(frame, 'target_x', scene, 2)\nframe = _first_compare_word(frame, offset, 92)\nx = origin.word(offset)\nframe = _first_word(frame, 'unit', x)\nif offset == 92:\n    frame = _first_sub_word(frame, 'unit', x, 3968)\n    x = u16(x - 3968)\n    y = origin.word(offset, 2)\n    frame = _first_word(frame, 'distance', y)\n    frame = _first_add_word(frame, 'distance', y, 3072)\n    y = u16(y + 3072)\nelse:\n    frame = _first_add_word(frame, 'unit', x, 3072)\n    x = u16(x + 3072)\n    y = origin.word(offset, 2)\n    frame = _first_word(frame, 'distance', y)\n    frame = _first_compare_word(frame, y, 20480)\n    if y >= 20480:\n        frame = _first_sub_word(frame, 'distance', y, 3968)\n        y = u16(y - 3968)\n    else:\n        frame = _first_add_word(frame, 'distance', y, 3968)\n        y = u16(y + 3968)\nreturn (frame, Point(x, y))"}})

INLINE_DECLARATIONS.update({'select_contact_nearest_deployment_anchor_fields': {'slots': {}, 'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, retained_unit: Word | None=None', 'returns': 'tuple', 'flow': "from .business_geometry import _contact_difference\nframe = _formation_position_frame(memory, frame)\nif retained_unit is None:\n    uint(frame.target_y, 32)\n    retained_unit = low16(frame.target_y)\nuint(retained_unit, 16)\npositions = memory.state.table(4294943056).cursor()\nsource = memory.state.table(4294955776).cursor()\ncells = memory.deployment_cells.cursor()\nvariants = memory.scene_variants.cursor()\nframe = first_replace(frame, roster=positions, candidates=source, controller=cells, scan=variants)\nscene = memory.battle_scene()\nframe = _first_word(frame, 'target_x', scene)\nframe = _first_word(frame, 'target_y', 0)\nvariant = variants.byte(scene)\nframe = _first_byte(frame, 'target_y', variant)\nframe = _first_shift_word(frame, 'target_x', scene, 5)\nframe = _first_shift_word(frame, 'target_y', variant, 1)\noffset = u16(u16(scene << 5) + u16(variant << 1))\nframe = _first_add_word(frame, 'target_x', u16(scene << 5), u16(variant << 1))\nframe = _first_word(frame, 'unit', 0)\nx = cells.byte(offset)\nframe = _first_byte(frame, 'unit', x)\nframe = _first_shift_word(frame, 'unit', x, 3)\nframe = _first_shift_word(frame, 'unit', u16(x << 3), 7)\nanchor_x = u16(x << 10)\nframe = _first_word(frame, 'count', 0)\ny = cells.byte(offset, 1)\nframe = _first_byte(frame, 'count', y)\nframe = _first_shift_word(frame, 'count', y, 3)\nframe = _first_shift_word(frame, 'count', u16(y << 3), 7)\nanchor_y = u16(y << 10)\ndistance, selected = (65535, u16(variant << 1))\nframe = _first_word(frame, 'target_x', distance)\nwhile True:\n    source = frame.candidates\n    member = source.word()\n    frame = first_replace(frame, candidates=source.advance(2))\n    frame = _first_word(frame, 'distance', member)\n    if negative_word(member):\n        return (frame, ClosestBattleUnit(distance, selected))\n    offset = u16(member << 2)\n    frame = _first_shift_word(frame, 'distance', member, 2)\n    x = frame.roster.word(offset)\n    frame = _first_word(frame, 'offset_x', x)\n    frame, dx = _contact_difference(frame, x, anchor_x)\n    frame = first_replace(frame, offset_x=None if frame.offset_x is None else replace_word(frame.offset_x, dx))\n    y = frame.roster.word(offset, 2)\n    frame = _first_word(frame, 'offset_y', y)\n    frame, dy = _contact_difference(frame, y, anchor_y)\n    frame = first_replace(frame, offset_y=None if frame.offset_y is None else replace_word(frame.offset_y, dy))\n    frame = _first_add_word(frame, 'offset_x', dx, dy)\n    candidate = u16(dx + dy)\n    frame = _first_compare_word(frame, candidate, distance)\n    if candidate >= distance:\n        continue\n    distance = candidate\n    frame = _first_word(frame, 'target_x', candidate)\n    frame = _first_right_word(frame, 'distance', offset, 2)\n    selected = offset >> 2\n    frame = _first_word(frame, 'target_y', selected)"}})

INLINE_DECLARATIONS.update({'read_formation_relative_position_delta_fields': {'slots': {}, 'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, retained_position: Word | None=None', 'returns': 'tuple', 'flow': "frame = _formation_position_frame(memory, frame)\nif retained_position is None:\n    uint(frame.unit, 32)\n    retained_position = low16(frame.unit)\nuint(retained_position, 16)\nmode = memory.state.read(4294965104, 2)\nframe = _first_word(frame, 'target_x', mode)\nframe = _first_compare_word(frame, mode, 9)\nif mode >= 9:\n    return (frame, retained_position)\noffset = u16(mode << 2)\nframe = _first_shift_word(frame, 'target_x', mode, 2)\ndeltas = memory.state.table(150000).cursor()\nframe = first_replace(frame, roster=deltas)\ndx = deltas.word(offset)\nframe = _first_word(frame, 'target_y', dx)\ndy = deltas.word(offset, 2)\nframe = _first_word(frame, 'unit', dy)\nvariants = memory.scene_variants.cursor()\nframe = first_replace(frame, roster=variants)\nscene = memory.battle_scene()\nframe = _first_word(frame, 'target_x', scene)\nframe = _first_word(frame, 'count', 0)\nvariant = variants.byte(scene)\nframe = _first_byte(frame, 'count', variant)\ncells = memory.deployment_cells.cursor()\nframe = first_replace(frame, roster=cells)\nframe = _first_shift_word(frame, 'target_x', scene, 5)\nframe = _first_shift_word(frame, 'count', variant, 1)\noffset = u16(u16(scene << 5) + u16(variant << 1))\nframe = _first_add_word(frame, 'target_x', u16(scene << 5), u16(variant << 1))\nframe = _first_word(frame, 'count', 0)\nx = cells.byte(offset)\nframe = _first_byte(frame, 'count', x)\nframe = _first_compare_word(frame, x, 14)\nif x <= 14:\n    frame = _first_sub_word(frame, 'target_y', 0, dx)\n    dx = u16(-dx)\nframe = _first_word(frame, 'distance', 0)\ny = cells.byte(offset, 1)\nframe = _first_byte(frame, 'distance', y)\nframe = _first_compare_word(frame, y, 20)\nif y >= 20:\n    frame = _first_sub_word(frame, 'unit', 0, dy)\n    dy = u16(-dy)\nframe = _first_add_word(frame, 'count', x, dx)\nx = u16(x + dx)\nframe = _first_add_word(frame, 'distance', y, dy)\ny = u16(y + dy)\nframe = _first_word(frame, 'unit', x)\nframe = _first_shift_word(frame, 'unit', x, 8)\nframe = _first_word(frame, 'distance', u16(y & 255))\npacked = u16(u16(x << 8) | u8(y))\nframe = _first_word(frame, 'unit', packed)\nreturn (frame, packed)"}})

APPROVED['business_geometry'].update({'collect_contacts_in_speed_radius_fields', 'select_weakest_contact_strength_fields', '_contact_difference'})

FAMILY_DECLARATIONS.update({'read_second_side_staging_anchor': {'signature': 'state: GameState', 'returns': 'Point', 'flow': 'checked_state(state)\nreturn read_second_side_staging_anchor_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())[1]'}})

INLINE_DECLARATIONS.update({'read_second_side_staging_anchor_fields': {'slots': {}, 'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': "frame = _formation_position_frame(memory, frame)\norigin = memory.state.table(713462).cursor()\nframe = first_replace(frame, roster=origin)\nscene = memory.battle_scene()\nframe = _first_word(frame, 'target_x', scene)\noffset = u16(scene << 2)\nframe = _first_shift_word(frame, 'target_x', scene, 2)\nframe = _first_compare_word(frame, offset, 92)\nx = origin.word(offset)\nframe = _first_word(frame, 'unit', x)\nif offset == 92:\n    frame = _first_sub_word(frame, 'unit', x, 4096)\n    x = u16(x - 4096)\n    y = origin.word(offset, 2)\n    frame = _first_word(frame, 'distance', y)\n    frame = _first_add_word(frame, 'distance', y, 1152)\n    y = u16(y + 1152)\nelse:\n    frame = _first_add_word(frame, 'unit', x, 1024)\n    x = u16(x + 1024)\n    y = origin.word(offset, 2)\n    frame = _first_word(frame, 'distance', y)\n    frame = _first_compare_word(frame, y, 20480)\n    if y >= 20480:\n        frame = _first_sub_word(frame, 'distance', y, 3968)\n        y = u16(y - 3968)\n    else:\n        frame = _first_add_word(frame, 'distance', y, 3968)\n        y = u16(y + 3968)\nreturn (frame, Point(x, y))"}})

FAMILY_DECLARATIONS.update({'read_first_side_staging_anchor': {'signature': 'state: GameState', 'returns': 'Point', 'flow': 'checked_state(state)\nreturn read_first_side_staging_anchor_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())[1]'}})

INLINE_DECLARATIONS.update({'read_first_side_staging_anchor_fields': {'slots': {}, 'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': "frame = _formation_position_frame(memory, frame)\norigin = memory.state.table(713462).cursor()\nframe = first_replace(frame, roster=origin)\nscene = memory.battle_scene()\nframe = _first_word(frame, 'target_x', scene)\noffset = u16(scene << 2)\nframe = _first_shift_word(frame, 'target_x', scene, 2)\nframe = _first_compare_word(frame, offset, 92)\nx = origin.word(offset)\nframe = _first_word(frame, 'unit', x)\nif offset == 92:\n    frame = _first_sub_word(frame, 'unit', x, 4096)\n    x = u16(x - 4096)\n    y = origin.word(offset, 2)\n    frame = _first_word(frame, 'distance', y)\n    frame = _first_sub_word(frame, 'distance', y, 1152)\n    y = u16(y - 1152)\nelse:\n    frame = _first_sub_word(frame, 'unit', x, 1024)\n    x = u16(x - 1024)\n    y = origin.word(offset, 2)\n    frame = _first_word(frame, 'distance', y)\n    frame = _first_compare_word(frame, y, 20480)\n    if y >= 20480:\n        frame = _first_sub_word(frame, 'distance', y, 3968)\n        y = u16(y - 3968)\n    else:\n        frame = _first_add_word(frame, 'distance', y, 3968)\n        y = u16(y + 3968)\nreturn (frame, Point(x, y))"}})


# Complete sole read_east_formation_region supplied body.
INLINE_DECLARATIONS.update({'read_east_formation_region': {'signature': 'state: GameState, context: RegionInput', 'returns': 'EastFormationRegion', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nreturn read_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), context.origin, context.offset, 1)[1]"}})


# Complete sole sample_east_formation_point supplied body.
INLINE_DECLARATIONS.update({'sample_east_formation_point': {'signature': 'state: GameState, region: EastFormationRegion', 'returns': 'SampledFormationPoint', 'flow': 'checked_state(state)\nvalues = sample_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), region, 1)\nreturn SampledFormationPoint(values[1], values[3], values[4])'}})


# Complete sole sample_or_accept_east_formation_region supplied body.
DECLARATIONS.update({'sample_or_accept_east_formation_region': {'signature': 'state: GameState, context: RegionInput', 'returns': 'RegionDecision', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nvalues = sample_or_accept_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 1, context.origin, context.offset, context.point)\nreturn _first_region_legacy_decision(state, values)"}})


# Complete sole choose_east_center_first_formation_point supplied body.
DECLARATIONS.update({'choose_east_center_first_formation_point': {'signature': 'state: GameState, context: RegionInput', 'returns': 'RegionDecision', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nvalues = choose_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 1, context.origin, context.offset, context.point)\nreturn _first_region_legacy_decision(state, values)"}})


# Complete sole read_west_formation_region supplied body.
FAMILY_INLINE_DECLARATIONS.update({'read_west_formation_region': {'signature': 'state: GameState, context: RegionInput', 'returns': 'BattleBounds', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nreturn read_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), context.origin, context.offset, 2)[1]"}})


# Complete sole sample_west_formation_point supplied body.
FAMILY_INLINE_DECLARATIONS.update({'sample_west_formation_point': {'signature': 'state: GameState, region: BattleBounds', 'returns': 'SampledFormationPoint', 'flow': 'checked_state(state)\nvalues = sample_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), region, 2)\nreturn SampledFormationPoint(values[1], values[3], values[4])'}})


# Complete sole sample_or_accept_west_formation_region supplied body.
FAMILY_DECLARATIONS.update({'sample_or_accept_west_formation_region': {'signature': 'state: GameState, context: RegionInput', 'returns': 'RegionDecision', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nvalues = sample_or_accept_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 2, context.origin, context.offset, context.point)\nreturn _first_region_legacy_decision(state, values)"}})


# Complete sole choose_west_center_first_formation_point supplied body.
DECLARATIONS.update({'choose_west_center_first_formation_point': {'signature': 'state: GameState, context: RegionInput', 'returns': 'RegionDecision', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nvalues = choose_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 2, context.origin, context.offset, context.point)\nreturn _first_region_legacy_decision(state, values)"}})


# Complete sole read_east_flank_region supplied body.
FAMILY_INLINE_DECLARATIONS.update({'read_east_flank_region': {'signature': 'state: GameState, context: RegionInput', 'returns': 'BattleBounds', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nreturn read_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), context.origin, context.offset, 3)[1]"}})


# Complete sole sample_east_flank_point supplied body.
FAMILY_INLINE_DECLARATIONS.update({'sample_east_flank_point': {'signature': 'state: GameState, region: BattleBounds', 'returns': 'SampledFlankPoint', 'flow': 'checked_state(state)\nvalues = sample_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), region, 3)\nreturn SampledFlankPoint(values[1], values[2])'}})


# Complete sole sample_or_accept_east_flank_region supplied body.
FAMILY_DECLARATIONS.update({'sample_or_accept_east_flank_region': {'signature': 'state: GameState, context: RegionInput', 'returns': 'RegionDecision', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nvalues = sample_or_accept_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 3, context.origin, context.offset, context.point)\nreturn _first_region_legacy_decision(state, values)"}})


# Complete sole choose_east_flank_first_formation_point supplied body.
DECLARATIONS.update({'choose_east_flank_first_formation_point': {'signature': 'state: GameState, context: RegionInput', 'returns': 'RegionDecision', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nvalues = choose_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 3, context.origin, context.offset, context.point)\nreturn _first_region_legacy_decision(state, values)"}})


# Complete sole read_lower_formation_region supplied body.
FAMILY_INLINE_DECLARATIONS.update({'read_lower_formation_region': {'signature': 'state: GameState, context: RegionInput', 'returns': 'BattleBounds', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nreturn read_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), context.origin, context.offset, 4)[1]"}})


# Complete sole sample_lower_formation_point supplied body.
FAMILY_INLINE_DECLARATIONS.update({'sample_lower_formation_point': {'signature': 'state: GameState, region: BattleBounds', 'returns': 'Point', 'flow': 'checked_state(state)\nvalues = sample_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), region, 4)\nreturn values[1]'}})


# Complete sole sample_or_accept_lower_formation_region supplied body.
FAMILY_DECLARATIONS.update({'sample_or_accept_lower_formation_region': {'signature': 'state: GameState, context: RegionInput', 'returns': 'RegionDecision', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nvalues = sample_or_accept_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 4, context.origin, context.offset, context.point)\nreturn _first_region_legacy_decision(state, values)"}})


# Complete sole choose_lower_center_first_formation_point supplied body.
DECLARATIONS.update({'choose_lower_center_first_formation_point': {'signature': 'state: GameState, context: RegionInput', 'returns': 'RegionDecision', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nvalues = choose_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 4, context.origin, context.offset, context.point)\nreturn _first_region_legacy_decision(state, values)"}})


# Complete sole _first_region_acceptance_fields supplied body.
INLINE_DECLARATIONS.update({'_first_region_acceptance_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, point: Point, region, kind: int', 'returns': 'tuple', 'flow': "if kind == 1:\n    accepted = east_formation_contains(point, region)\n    comparisons = ((point.x, region.east_limit, False), (point.y, region.lower, True), (point.y, region.upper, False))\nelif kind == 2:\n    accepted = west_formation_contains(point, region)\n    comparisons = ((point.x, region.left, True), (point.y, region.lower, True), (point.y, region.upper, False))\nelif kind == 3:\n    accepted = east_flank_contains(point, region)\n    comparisons = ((point.x, region.left, True), (point.x, region.right, False), (point.y, region.lower, True), (point.y, region.upper, False))\nelif kind == 4:\n    accepted = lower_formation_contains(point, region)\n    comparisons = ((point.x, region.left, True), (point.x, region.right, False), (point.y, region.lower, True), (point.y, region.upper, False))\nelse:\n    raise ValueError('one original first formation policy required')\nfor value, bound, minimum in comparisons:\n    frame = _first_compare_word(frame, value, bound)\n    outside = value < bound if minimum else value > bound\n    if outside:\n        break\nreturn (_first_region_publish(memory, frame), accepted)"}})


# Complete sole _first_region_carry supplied body.
INLINE_DECLARATIONS.update({'_first_region_carry': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, enabled: bool', 'returns': 'FirstDeploymentFrame', 'flow': 'from .business_actions import _deployment_carry\nframe = _first_region_publish(memory, frame)\nreturn _deployment_carry(memory, frame, enabled)'}})


# Complete sole _first_region_context supplied body.
INLINE_DECLARATIONS.update({'_first_region_context': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, origin=None, offset=None, point=None', 'returns': 'tuple', 'flow': "frame = _first_frame(memory, frame)\nif origin is None:\n    origin = frame.roster\nchecked_policy_table(origin, memory.state)\nif offset is None:\n    uint(frame.unit, 32)\n    offset = low16(frame.unit)\nuint(offset, 16)\nif point is None:\n    uint(frame.target_x, 32)\n    uint(frame.target_y, 32)\n    point = Point(low16(frame.target_x), low16(frame.target_y))\nif type(point) is not Point:\n    raise ValueError('actual first formation point WORDs required')\nreturn (frame, origin, offset, point)"}})


# Complete sole _first_region_draw supplied body.
INLINE_DECLARATIONS.update({'_first_region_draw': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, continuation: Long, multiplier: Word, swapped: bool=True', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _first_region_publish(memory, frame)\nframe = _first_call(memory, frame, continuation, first_deployment_random_fields)\nframe = _first_long(frame, 'target_x', frame.target_x & 65535)\nframe = _first_long(frame, 'target_x', low16(frame.target_x) * uint(multiplier, 16))\nif swapped:\n    sample = frame.target_x\n    frame = _first_long(frame, 'target_x', u32(sample << 16 | sample >> 16))\nreturn _first_region_publish(memory, frame)"}})


# Complete sole _first_region_legacy_decision supplied body.
INLINE_DECLARATIONS.update({'_first_region_legacy_decision': {'signature': 'state: GameState, values: tuple', 'returns': 'RegionDecision', 'flow': 'frame, point, horizontal, vertical, carry = values\nreturn RegionDecision(point, horizontal, vertical, state.carry_observed(int(carry)))'}})


# Complete sole _first_region_publish supplied body.
INLINE_DECLARATIONS.update({'_first_region_publish': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'if frame.status is not None:\n    memory.state.sr = memory.state.sr & 65504 | frame.status\nreturn frame'}})


# Complete sole choose_east_center_first_formation_point_fields supplied body.
INLINE_DECLARATIONS.update({'choose_east_center_first_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'return choose_first_formation_point_fields(memory, frame, 1)'}})


# Complete sole choose_east_flank_first_formation_point_fields supplied body.
INLINE_DECLARATIONS.update({'choose_east_flank_first_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'return choose_first_formation_point_fields(memory, frame, 3)'}})


# Complete sole choose_first_formation_point_fields supplied body.
INLINE_DECLARATIONS.update({'choose_first_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, kind: int, origin=None, offset=None, point=None', 'returns': 'tuple', 'flow': "frame, origin, offset, point = _first_region_context(memory, frame, origin, offset, point)\ncontinuation = 147052 if kind == 1 else 147190 if kind == 2 else 147332 if kind == 3 else 147532 if kind == 4 else None\nuint(continuation, 32)\nframe = _first_region_publish(memory, frame)\nentered = _formation_position_enter(frame, continuation)\nframe, result, horizontal, vertical, carry = sample_or_accept_first_formation_region_fields(memory, entered, kind, origin, offset, point)\nframe = _formation_position_leave(frame, continuation)\nif carry:\n    if kind == 1:\n        frame = _first_add_word(frame, 'count', result.x, 3968)\n        x = u16(result.x + 3968)\n        frame = _first_add_word(frame, 'offset_x', result.y, 3072)\n        y = u16(result.y + 3072)\n    elif kind == 2:\n        frame = _first_word(frame, 'count', horizontal)\n        frame = _first_sub_word(frame, 'count', horizontal, 3968)\n        x = u16(horizontal - 3968)\n        frame = _first_add_word(frame, 'offset_x', result.y, 3072)\n        y = u16(result.y + 3072)\n    elif kind == 3:\n        anchor_y = origin.word(offset, 2)\n        frame = _first_compare_word(frame, anchor_y, 20480)\n        x = result.x\n        if anchor_y >= 20480:\n            frame = _first_word(frame, 'offset_x', vertical)\n            frame = _first_sub_word(frame, 'offset_x', vertical, 1024)\n            y = u16(vertical - 1024)\n        else:\n            frame = _first_add_word(frame, 'offset_x', result.y, 1024)\n            y = u16(result.y + 1024)\n    else:\n        frame = _first_add_word(frame, 'count', result.x, 4096)\n        x = u16(result.x + 4096)\n        frame = _first_add_word(frame, 'offset_x', result.y, 9344)\n        y = u16(result.y + 9344)\n    result, carry = (Point(x, y), bool(frame.status & 1))\nreturn (_first_region_publish(memory, frame), result, horizontal, vertical, carry)"}})


# Complete sole choose_lower_center_first_formation_point_fields supplied body.
INLINE_DECLARATIONS.update({'choose_lower_center_first_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'return choose_first_formation_point_fields(memory, frame, 4)'}})


# Complete sole choose_west_center_first_formation_point_fields supplied body.
INLINE_DECLARATIONS.update({'choose_west_center_first_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'return choose_first_formation_point_fields(memory, frame, 2)'}})


# Complete sole read_first_formation_region_fields supplied body.
INLINE_DECLARATIONS.update({'read_first_formation_region_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, origin, offset: Word, kind: int', 'returns': 'tuple', 'flow': "frame = _first_frame(memory, frame)\nchecked_policy_table(origin, memory.state)\nuint(offset, 16)\nif kind not in (1, 2, 3, 4):\n    raise ValueError('one actual first formation region required')\nanchor_x = origin.word(offset)\nframe = _first_word(frame, 'count', anchor_x)\nif kind == 3:\n    frame = _first_add_word(frame, 'count', anchor_x, 3968)\n    left = u16(anchor_x + 3968)\n    frame = _first_word(frame, 'distance', left)\n    frame = _first_add_word(frame, 'distance', left, 8320)\n    right = u16(left + 8320)\n    if frame.status & 1:\n        right = 25600\n        frame = _first_word(frame, 'distance', right)\n    else:\n        frame = _first_compare_word(frame, right, 25600)\n        if right > 25600:\n            right = 25600\n            frame = _first_word(frame, 'distance', right)\nelse:\n    frame = _first_word(frame, 'distance', anchor_x)\n    if kind == 1:\n        left, right = (anchor_x, u16(anchor_x + 14336))\n        frame = _first_add_word(frame, 'distance', anchor_x, 14336)\n    elif kind == 2:\n        left, right = (u16(anchor_x - 14336), anchor_x)\n        frame = _first_sub_word(frame, 'count', anchor_x, 14336)\n    else:\n        left, right = (u16(anchor_x - 3072), u16(anchor_x + 3072))\n        frame = _first_sub_word(frame, 'count', anchor_x, 3072)\n        frame = _first_add_word(frame, 'distance', anchor_x, 3072)\nanchor_y = origin.word(offset, 2)\nframe = _first_word(frame, 'offset_x', anchor_y)\nif kind == 3:\n    frame = _first_compare_word(frame, anchor_y, 20480)\n    frame = _first_word(frame, 'offset_y', anchor_y)\n    lower, upper = (anchor_y, anchor_y)\n    if anchor_y >= 20480:\n        lower = u16(anchor_y - 14336)\n        frame = _first_sub_word(frame, 'offset_x', anchor_y, 14336)\n    else:\n        upper = u16(anchor_y + 14336)\n        frame = _first_add_word(frame, 'offset_y', anchor_y, 14336)\nelse:\n    frame = _first_word(frame, 'offset_y', anchor_y)\n    if kind == 4:\n        lower, upper = (u16(anchor_y - 13312), anchor_y)\n        frame = _first_sub_word(frame, 'offset_x', anchor_y, 13312)\n    else:\n        lower, upper = (u16(anchor_y - 4096), u16(anchor_y + 4096))\n        frame = _first_sub_word(frame, 'offset_x', anchor_y, 4096)\n        frame = _first_compare_word(frame, lower, 3072)\n        if lower < 3072:\n            lower = 3072\n            frame = _first_word(frame, 'offset_x', lower)\n        frame = _first_add_word(frame, 'offset_y', anchor_y, 4096)\n        frame = _first_compare_word(frame, upper, 37888)\n        if upper > 37888:\n            upper = 37888\n            frame = _first_word(frame, 'offset_y', upper)\nregion = EastFormationRegion(left, right, lower, upper) if kind == 1 else BattleBounds(left, right, lower, upper)\nreturn (_first_region_publish(memory, frame), region)"}})


# Complete sole sample_first_formation_point_fields supplied body.
INLINE_DECLARATIONS.update({'sample_first_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, region, kind: int', 'returns': 'tuple', 'flow': "frame = _first_frame(memory, frame)\nif kind == 1:\n    if type(region) is not EastFormationRegion:\n        raise ValueError('east first formation limits required')\n    first_return, second_return = (147146, 147172)\n    initial_x, horizontal = (region.anchor_x, region.east_limit)\nelif kind in (2, 3, 4):\n    if type(region) is not BattleBounds:\n        raise ValueError('first formation wrapped bounds required')\n    first_return, second_return = (147286, 147314) if kind == 2 else (147486, 147508) if kind == 3 else (147608, 147628)\n    initial_x, horizontal = (region.left, region.right)\nelse:\n    raise ValueError('one actual first formation sampler required')\nvertical = region.upper\nif kind == 3:\n    frame = _first_region_publish(memory, frame)\n    frame = _first_call(memory, frame, first_return, first_deployment_random_fields)\n    frame = _first_long(frame, 'target_x', frame.target_x & 65535)\n    horizontal = u16(region.right - region.left)\n    frame = _first_sub_word(frame, 'distance', region.right, region.left)\n    frame = _first_long(frame, 'target_x', low16(frame.target_x) * horizontal)\n    product = frame.target_x\n    frame = _first_long(frame, 'target_x', u32(product << 16 | product >> 16))\n    x = u16(initial_x + low16(frame.target_x))\n    frame = _first_add_word(frame, 'count', initial_x, low16(frame.target_x))\n    frame = _first_add_word(frame, 'count', x, 1)\n    x = u16(x + 1)\nelse:\n    frame = _first_region_draw(memory, frame, first_return, 6144 if kind == 4 else 8192)\n    draw = low16(frame.target_x)\n    if kind == 2:\n        frame = _first_word(frame, 'count', region.right)\n        frame = _first_sub_word(frame, 'count', region.right, draw)\n        x = u16(region.right - draw)\n        frame = _first_sub_word(frame, 'count', x, 3072)\n        x = u16(x - 3072)\n    else:\n        frame = _first_add_word(frame, 'count', initial_x, draw)\n        x = u16(initial_x + draw)\n        if kind == 1:\n            frame = _first_add_word(frame, 'count', x, 3072)\n            x = u16(x + 3072)\nif kind in (1, 2):\n    vertical = u16(region.upper - region.lower)\n    frame = _first_sub_word(frame, 'offset_y', region.upper, region.lower)\n    frame = _first_region_draw(memory, frame, second_return, vertical)\nelse:\n    frame = _first_region_draw(memory, frame, second_return, 6144 if kind == 4 else 8192, kind != 4)\ndraw = low16(frame.target_x)\nframe = _first_add_word(frame, 'offset_x', region.lower, draw)\ny = u16(region.lower + draw)\ncarry = bool(frame.status & 1)\nif kind in (3, 4):\n    frame = _first_region_carry(memory, frame, False)\n    carry = False\nreturn (_first_region_publish(memory, frame), Point(x, y), horizontal, vertical, carry)"}})


# Complete sole sample_or_accept_east_flank_region_fields supplied body.
INLINE_DECLARATIONS.update({'sample_or_accept_east_flank_region_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'return sample_or_accept_first_formation_region_fields(memory, frame, 3)'}})


# Complete sole sample_or_accept_east_formation_region_fields supplied body.
INLINE_DECLARATIONS.update({'sample_or_accept_east_formation_region_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'return sample_or_accept_first_formation_region_fields(memory, frame, 1)'}})


# Complete sole sample_or_accept_first_formation_region_fields supplied body.
INLINE_DECLARATIONS.update({'sample_or_accept_first_formation_region_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, kind: int, origin=None, offset=None, point=None', 'returns': 'tuple', 'flow': 'frame, origin, offset, point = _first_region_context(memory, frame, origin, offset, point)\nframe, region = read_first_formation_region_fields(memory, frame, origin, offset, kind)\nframe, accepted = _first_region_acceptance_fields(memory, frame, point, region, kind)\nif accepted:\n    frame = _first_region_carry(memory, frame, True)\n    x = region.anchor_x if kind == 1 else region.left\n    horizontal = region.east_limit if kind == 1 else region.right\n    return (frame, Point(x, region.lower), horizontal, region.upper, True)\nreturn sample_first_formation_point_fields(memory, frame, region, kind)'}})


# Complete sole sample_or_accept_lower_formation_region_fields supplied body.
INLINE_DECLARATIONS.update({'sample_or_accept_lower_formation_region_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'return sample_or_accept_first_formation_region_fields(memory, frame, 4)'}})


# Complete sole sample_or_accept_west_formation_region_fields supplied body.
INLINE_DECLARATIONS.update({'sample_or_accept_west_formation_region_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'return sample_or_accept_first_formation_region_fields(memory, frame, 2)'}})

APPROVED.setdefault('business_actions', set()).add('_deployment_carry')


# Complete current sole _first_region_acceptance_fields field body.
INLINE_DECLARATIONS.update({'_first_region_acceptance_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, point: Point, region, kind: int', 'returns': 'tuple', 'flow': "if kind == 1:\n    accepted = east_formation_contains(point, region)\n    comparisons = ((point.x, region.east_limit, False), (point.y, region.lower, True), (point.y, region.upper, False))\nelif kind == 2:\n    accepted = west_formation_contains(point, region)\n    comparisons = ((point.x, region.left, True), (point.y, region.lower, True), (point.y, region.upper, False))\nelif kind == 3:\n    accepted = east_flank_contains(point, region)\n    comparisons = ((point.x, region.left, True), (point.x, region.right, False), (point.y, region.lower, True), (point.y, region.upper, False))\nelif kind == 4:\n    accepted = lower_formation_contains(point, region)\n    comparisons = ((point.x, region.left, True), (point.x, region.right, False), (point.y, region.lower, True), (point.y, region.upper, False))\nelif kind == 5:\n    accepted = west_flank_contains(point, region)\n    comparisons = ((point.x, region.left, True), (point.x, region.right, False), (point.y, region.lower, True), (point.y, region.upper, False))\nelif kind == 6:\n    accepted = upper_formation_contains(point, region)\n    comparisons = ((point.x, region.left, True), (point.x, region.right, False), (point.y, region.lower, True), (point.y, region.upper, False))\nelse:\n    raise ValueError('one original first or second formation policy required')\nfor value, bound, minimum in comparisons:\n    frame = _first_compare_word(frame, value, bound)\n    outside = value < bound if minimum else value > bound\n    if outside:\n        break\nreturn (_first_region_publish(memory, frame), accepted)"}})


# Complete current sole choose_east_center_second_formation_point field body.
DECLARATIONS.update({'choose_east_center_second_formation_point': {'signature': 'state: GameState, context: RegionInput', 'returns': 'RegionDecision', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nvalues = choose_second_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 1, context.origin, context.offset, context.point)\nreturn _first_region_legacy_decision(state, values)"}})


# Complete current sole choose_east_center_second_formation_point_fields field body.
INLINE_DECLARATIONS.update({'choose_east_center_second_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'return choose_second_formation_point_fields(memory, frame, 1)'}})


# Complete current sole choose_second_formation_point_fields field body.
INLINE_DECLARATIONS.update({'choose_second_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, kind: int, origin=None, offset=None, point=None', 'returns': 'tuple', 'flow': "frame, origin, offset, point = _first_region_context(memory, frame, origin, offset, point)\ncontinuation = 147852 if kind == 1 else 147870 if kind == 2 else 147890 if kind == 5 else 148092 if kind == 6 else None\nuint(continuation, 32)\nframe = _first_region_publish(memory, frame)\nentered = _formation_position_enter(frame, continuation)\nframe, result, horizontal, vertical, carry = sample_or_accept_first_formation_region_fields(memory, entered, kind, origin, offset, point)\nframe = _formation_position_leave(frame, continuation)\nif carry:\n    if kind == 1:\n        frame = _first_add_word(frame, 'count', result.x, 3968)\n        x = u16(result.x + 3968)\n        frame = _first_add_word(frame, 'offset_x', result.y, 5120)\n        y = u16(result.y + 5120)\n    elif kind == 2:\n        frame = _first_word(frame, 'count', horizontal)\n        frame = _first_sub_word(frame, 'count', horizontal, 3968)\n        x = u16(horizontal - 3968)\n        frame = _first_add_word(frame, 'offset_x', result.y, 5120)\n        y = u16(result.y + 5120)\n    elif kind == 5:\n        anchor_y = origin.word(offset, 2)\n        frame = _first_compare_word(frame, anchor_y, 20480)\n        frame = _first_word(frame, 'count', horizontal)\n        x = horizontal\n        if anchor_y >= 20480:\n            frame = _first_word(frame, 'offset_x', vertical)\n            frame = _first_sub_word(frame, 'offset_x', vertical, 1024)\n            y = u16(vertical - 1024)\n        else:\n            frame = _first_add_word(frame, 'offset_x', result.y, 1024)\n            y = u16(result.y + 1024)\n    else:\n        frame = _first_add_word(frame, 'count', result.x, 4096)\n        x = u16(result.x + 4096)\n        frame = _first_add_word(frame, 'offset_x', result.y, 3968)\n        y = u16(result.y + 3968)\n    result, carry = (Point(x, y), bool(frame.status & 1))\nreturn (_first_region_publish(memory, frame), result, horizontal, vertical, carry)"}})


# Complete current sole choose_upper_center_second_formation_point field body.
DECLARATIONS.update({'choose_upper_center_second_formation_point': {'signature': 'state: GameState, context: RegionInput', 'returns': 'RegionDecision', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nvalues = choose_second_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 6, context.origin, context.offset, context.point)\nreturn _first_region_legacy_decision(state, values)"}})


# Complete current sole choose_upper_center_second_formation_point_fields field body.
INLINE_DECLARATIONS.update({'choose_upper_center_second_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'return choose_second_formation_point_fields(memory, frame, 6)'}})


# Complete current sole choose_west_center_second_formation_point field body.
DECLARATIONS.update({'choose_west_center_second_formation_point': {'signature': 'state: GameState, context: RegionInput', 'returns': 'RegionDecision', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nvalues = choose_second_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 2, context.origin, context.offset, context.point)\nreturn _first_region_legacy_decision(state, values)"}})


# Complete current sole choose_west_center_second_formation_point_fields field body.
INLINE_DECLARATIONS.update({'choose_west_center_second_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'return choose_second_formation_point_fields(memory, frame, 2)'}})


# Complete current sole choose_west_flank_second_formation_point field body.
DECLARATIONS.update({'choose_west_flank_second_formation_point': {'signature': 'state: GameState, context: RegionInput', 'returns': 'RegionDecision', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nvalues = choose_second_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 5, context.origin, context.offset, context.point)\nreturn _first_region_legacy_decision(state, values)"}})


# Complete current sole choose_west_flank_second_formation_point_fields field body.
INLINE_DECLARATIONS.update({'choose_west_flank_second_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'return choose_second_formation_point_fields(memory, frame, 5)'}})


# Complete current sole read_first_formation_region_fields field body.
INLINE_DECLARATIONS.update({'read_first_formation_region_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, origin, offset: Word, kind: int', 'returns': 'tuple', 'flow': "frame = _first_frame(memory, frame)\nchecked_policy_table(origin, memory.state)\nuint(offset, 16)\nif kind not in (1, 2, 3, 4, 5, 6):\n    raise ValueError('one actual first formation region required')\nanchor_x = origin.word(offset)\nframe = _first_word(frame, 'count', anchor_x)\nif kind == 3:\n    frame = _first_add_word(frame, 'count', anchor_x, 3968)\n    left = u16(anchor_x + 3968)\n    frame = _first_word(frame, 'distance', left)\n    frame = _first_add_word(frame, 'distance', left, 8320)\n    right = u16(left + 8320)\n    if frame.status & 1:\n        right = 25600\n        frame = _first_word(frame, 'distance', right)\n    else:\n        frame = _first_compare_word(frame, right, 25600)\n        if right > 25600:\n            right = 25600\n            frame = _first_word(frame, 'distance', right)\nelse:\n    frame = _first_word(frame, 'distance', anchor_x)\n    if kind == 1:\n        left, right = (anchor_x, u16(anchor_x + 14336))\n        frame = _first_add_word(frame, 'distance', anchor_x, 14336)\n    elif kind == 2:\n        left, right = (u16(anchor_x - 14336), anchor_x)\n        frame = _first_sub_word(frame, 'count', anchor_x, 14336)\n    elif kind == 5:\n        right = u16(anchor_x - 3968)\n        frame = _first_sub_word(frame, 'distance', anchor_x, 3968)\n        left = u16(anchor_x - 12288)\n        frame = _first_sub_word(frame, 'count', anchor_x, 12288)\n        if frame.status & 1:\n            left = 3072\n            frame = _first_word(frame, 'count', left)\n        else:\n            frame = _first_compare_word(frame, left, 3072)\n            if left < 3072:\n                left = 3072\n                frame = _first_word(frame, 'count', left)\n    else:\n        left, right = (u16(anchor_x - 3072), u16(anchor_x + 3072))\n        frame = _first_sub_word(frame, 'count', anchor_x, 3072)\n        frame = _first_add_word(frame, 'distance', anchor_x, 3072)\nanchor_y = origin.word(offset, 2)\nframe = _first_word(frame, 'offset_x', anchor_y)\nif kind in (3, 5):\n    frame = _first_compare_word(frame, anchor_y, 20480)\n    frame = _first_word(frame, 'offset_y', anchor_y)\n    lower, upper = (anchor_y, anchor_y)\n    if anchor_y >= 20480:\n        lower = u16(anchor_y - 14336)\n        frame = _first_sub_word(frame, 'offset_x', anchor_y, 14336)\n    else:\n        upper = u16(anchor_y + 14336)\n        frame = _first_add_word(frame, 'offset_y', anchor_y, 14336)\nelse:\n    frame = _first_word(frame, 'offset_y', anchor_y)\n    if kind == 4:\n        lower, upper = (u16(anchor_y - 13312), anchor_y)\n        frame = _first_sub_word(frame, 'offset_x', anchor_y, 13312)\n    elif kind == 6:\n        lower, upper = (anchor_y, u16(anchor_y + 13312))\n        frame = _first_add_word(frame, 'offset_y', anchor_y, 13312)\n    else:\n        lower, upper = (u16(anchor_y - 4096), u16(anchor_y + 4096))\n        frame = _first_sub_word(frame, 'offset_x', anchor_y, 4096)\n        frame = _first_compare_word(frame, lower, 3072)\n        if lower < 3072:\n            lower = 3072\n            frame = _first_word(frame, 'offset_x', lower)\n        frame = _first_add_word(frame, 'offset_y', anchor_y, 4096)\n        frame = _first_compare_word(frame, upper, 37888)\n        if upper > 37888:\n            upper = 37888\n            frame = _first_word(frame, 'offset_y', upper)\nregion = EastFormationRegion(left, right, lower, upper) if kind == 1 else BattleBounds(left, right, lower, upper)\nreturn (_first_region_publish(memory, frame), region)"}})


# Complete current sole read_upper_formation_region field body.
FAMILY_INLINE_DECLARATIONS.update({'read_upper_formation_region': {'signature': 'state: GameState, context: RegionInput', 'returns': 'BattleBounds', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nreturn read_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), context.origin, context.offset, 6)[1]"}})


# Complete current sole read_west_flank_region field body.
FAMILY_INLINE_DECLARATIONS.update({'read_west_flank_region': {'signature': 'state: GameState, context: RegionInput', 'returns': 'BattleBounds', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nreturn read_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), context.origin, context.offset, 5)[1]"}})


# Complete current sole sample_first_formation_point_fields field body.
INLINE_DECLARATIONS.update({'sample_first_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, region, kind: int', 'returns': 'tuple', 'flow': "frame = _first_frame(memory, frame)\nif kind == 1:\n    if type(region) is not EastFormationRegion:\n        raise ValueError('east first formation limits required')\n    first_return, second_return = (147146, 147172)\n    initial_x, horizontal = (region.anchor_x, region.east_limit)\nelif kind in (2, 3, 4, 5, 6):\n    if type(region) is not BattleBounds:\n        raise ValueError('first formation wrapped bounds required')\n    first_return, second_return = (147286, 147314) if kind == 2 else (147486, 147508) if kind == 3 else (147608, 147628) if kind == 4 else (148048, 148068) if kind == 5 else (148168, 148188)\n    initial_x, horizontal = (region.left, region.right)\nelse:\n    raise ValueError('one actual first formation sampler required')\nvertical = region.upper\nif kind in (3, 5):\n    frame = _first_region_publish(memory, frame)\n    frame = _first_call(memory, frame, first_return, first_deployment_random_fields)\n    frame = _first_long(frame, 'target_x', frame.target_x & 65535)\n    horizontal = u16(region.right - region.left)\n    frame = _first_sub_word(frame, 'distance', region.right, region.left)\n    frame = _first_long(frame, 'target_x', low16(frame.target_x) * horizontal)\n    product = frame.target_x\n    frame = _first_long(frame, 'target_x', u32(product << 16 | product >> 16))\n    x = u16(initial_x + low16(frame.target_x))\n    frame = _first_add_word(frame, 'count', initial_x, low16(frame.target_x))\n    if kind == 3:\n        frame = _first_add_word(frame, 'count', x, 1)\n        x = u16(x + 1)\nelse:\n    frame = _first_region_draw(memory, frame, first_return, 6144 if kind in (4, 6) else 8192)\n    draw = low16(frame.target_x)\n    if kind == 2:\n        frame = _first_word(frame, 'count', region.right)\n        frame = _first_sub_word(frame, 'count', region.right, draw)\n        x = u16(region.right - draw)\n        frame = _first_sub_word(frame, 'count', x, 3072)\n        x = u16(x - 3072)\n    else:\n        frame = _first_add_word(frame, 'count', initial_x, draw)\n        x = u16(initial_x + draw)\n        if kind == 1:\n            frame = _first_add_word(frame, 'count', x, 3072)\n            x = u16(x + 3072)\nif kind in (1, 2):\n    vertical = u16(region.upper - region.lower)\n    frame = _first_sub_word(frame, 'offset_y', region.upper, region.lower)\n    frame = _first_region_draw(memory, frame, second_return, vertical)\nelse:\n    frame = _first_region_draw(memory, frame, second_return, 6144 if kind in (4, 6) else 8192, kind not in (4, 6))\ndraw = low16(frame.target_x)\nframe = _first_add_word(frame, 'offset_x', region.lower, draw)\ny = u16(region.lower + draw)\ncarry = bool(frame.status & 1)\nif kind in (3, 4, 5, 6):\n    frame = _first_region_carry(memory, frame, False)\n    carry = False\nreturn (_first_region_publish(memory, frame), Point(x, y), horizontal, vertical, carry)"}})


# Complete current sole sample_or_accept_upper_formation_region field body.
FAMILY_DECLARATIONS.update({'sample_or_accept_upper_formation_region': {'signature': 'state: GameState, context: RegionInput', 'returns': 'RegionDecision', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nvalues = sample_or_accept_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 6, context.origin, context.offset, context.point)\nreturn _first_region_legacy_decision(state, values)"}})


# Complete current sole sample_or_accept_upper_formation_region_fields field body.
INLINE_DECLARATIONS.update({'sample_or_accept_upper_formation_region_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'return sample_or_accept_first_formation_region_fields(memory, frame, 6)'}})


# Complete current sole sample_or_accept_west_flank_region field body.
FAMILY_DECLARATIONS.update({'sample_or_accept_west_flank_region': {'signature': 'state: GameState, context: RegionInput', 'returns': 'RegionDecision', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nvalues = sample_or_accept_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 5, context.origin, context.offset, context.point)\nreturn _first_region_legacy_decision(state, values)"}})


# Complete current sole sample_or_accept_west_flank_region_fields field body.
INLINE_DECLARATIONS.update({'sample_or_accept_west_flank_region_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'return sample_or_accept_first_formation_region_fields(memory, frame, 5)'}})


# Complete current sole sample_upper_formation_point field body.
FAMILY_INLINE_DECLARATIONS.update({'sample_upper_formation_point': {'signature': 'state: GameState, region: BattleBounds', 'returns': 'Point', 'flow': 'checked_state(state)\nvalues = sample_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), region, 6)\nreturn values[1]'}})


# Complete current sole sample_west_flank_point field body.
FAMILY_INLINE_DECLARATIONS.update({'sample_west_flank_point': {'signature': 'state: GameState, region: BattleBounds', 'returns': 'SampledFlankPoint', 'flow': 'checked_state(state)\nvalues = sample_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), region, 5)\nreturn SampledFlankPoint(values[1], values[2])'}})


# Whole current sole choose_east_center_third_formation_point body.
DECLARATIONS.update({'choose_east_center_third_formation_point': {'signature': 'state: GameState, context: RegionInput', 'returns': 'RegionDecision', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nvalues = choose_third_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 1, context.origin, context.offset, context.point)\nreturn _first_region_legacy_decision(state, values)"}})


# Whole current sole choose_east_center_third_formation_point_fields body.
INLINE_DECLARATIONS.update({'choose_east_center_third_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'return choose_third_formation_point_fields(memory, frame, 1)'}})


# Whole current sole choose_lateral_formation_point_fields body.
INLINE_DECLARATIONS.update({'choose_lateral_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, kind: int, family: int, origin=None, offset=None, point=None', 'returns': 'tuple', 'flow': "if family not in (2, 3):\n    raise ValueError('actual lateral wrapper family required')\nframe, origin, offset, point = _first_region_context(memory, frame, origin, offset, point)\nif family == 2:\n    continuation = 147852 if kind == 1 else 147870 if kind == 2 else 147890 if kind == 5 else 148092 if kind == 6 else None\nelse:\n    continuation = 148850 if kind == 1 else 148868 if kind == 2 else 148888 if kind == 5 else 148926 if kind == 6 else None\nuint(continuation, 32)\nframe = _first_region_publish(memory, frame)\nentered = _formation_position_enter(frame, continuation)\nframe, result, horizontal, vertical, carry = sample_or_accept_first_formation_region_fields(memory, entered, kind, origin, offset, point)\nframe = _formation_position_leave(frame, continuation)\nif carry:\n    if kind == 1:\n        frame = _first_add_word(frame, 'count', result.x, 3968)\n        x = u16(result.x + 3968)\n        frame = _first_add_word(frame, 'offset_x', result.y, 5120 if family == 2 else 7168)\n        y = u16(result.y + (5120 if family == 2 else 7168))\n    elif kind == 2:\n        frame = _first_word(frame, 'count', horizontal)\n        frame = _first_sub_word(frame, 'count', horizontal, 3968)\n        x = u16(horizontal - 3968)\n        frame = _first_add_word(frame, 'offset_x', result.y, 5120 if family == 2 else 7168)\n        y = u16(result.y + (5120 if family == 2 else 7168))\n    elif kind == 5:\n        anchor_y = origin.word(offset, 2)\n        frame = _first_compare_word(frame, anchor_y, 20480)\n        frame = _first_word(frame, 'count', horizontal)\n        x = horizontal\n        if anchor_y >= 20480:\n            frame = _first_word(frame, 'offset_x', vertical)\n            if family == 2:\n                frame = _first_sub_word(frame, 'offset_x', vertical, 1024)\n                y = u16(vertical - 1024)\n            else:\n                frame = _first_add_word(frame, 'offset_x', vertical, 1024)\n                y = u16(vertical + 1024)\n        elif family == 2:\n            frame = _first_add_word(frame, 'offset_x', result.y, 1024)\n            y = u16(result.y + 1024)\n        else:\n            frame = _first_sub_word(frame, 'offset_x', result.y, 1024)\n            y = u16(result.y - 1024)\n    else:\n        shift = 4096 if family == 2 else 2048\n        frame = _first_add_word(frame, 'count', result.x, shift)\n        x = u16(result.x + shift)\n        frame = _first_add_word(frame, 'offset_x', result.y, 3968)\n        y = u16(result.y + 3968)\n    result, carry = (Point(x, y), bool(frame.status & 1))\nreturn (_first_region_publish(memory, frame), result, horizontal, vertical, carry)"}})


# Whole current sole choose_second_formation_point_fields body.
INLINE_DECLARATIONS.update({'choose_second_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, kind: int, origin=None, offset=None, point=None', 'returns': 'tuple', 'flow': 'return choose_lateral_formation_point_fields(memory, frame, kind, 2, origin, offset, point)'}})


# Whole current sole choose_third_formation_point_fields body.
INLINE_DECLARATIONS.update({'choose_third_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, kind: int, origin=None, offset=None, point=None', 'returns': 'tuple', 'flow': 'return choose_lateral_formation_point_fields(memory, frame, kind, 3, origin, offset, point)'}})


# Whole current sole choose_upper_center_third_formation_point body.
DECLARATIONS.update({'choose_upper_center_third_formation_point': {'signature': 'state: GameState, context: RegionInput', 'returns': 'RegionDecision', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nvalues = choose_third_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 6, context.origin, context.offset, context.point)\nreturn _first_region_legacy_decision(state, values)"}})


# Whole current sole choose_upper_center_third_formation_point_fields body.
INLINE_DECLARATIONS.update({'choose_upper_center_third_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'return choose_third_formation_point_fields(memory, frame, 6)'}})


# Whole current sole choose_west_center_third_formation_point body.
DECLARATIONS.update({'choose_west_center_third_formation_point': {'signature': 'state: GameState, context: RegionInput', 'returns': 'RegionDecision', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nvalues = choose_third_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 2, context.origin, context.offset, context.point)\nreturn _first_region_legacy_decision(state, values)"}})


# Whole current sole choose_west_center_third_formation_point_fields body.
INLINE_DECLARATIONS.update({'choose_west_center_third_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'return choose_third_formation_point_fields(memory, frame, 2)'}})


# Whole current sole choose_west_flank_third_formation_point body.
DECLARATIONS.update({'choose_west_flank_third_formation_point': {'signature': 'state: GameState, context: RegionInput', 'returns': 'RegionDecision', 'flow': "checked_state(state)\nif type(context) is not RegionInput:\n    raise ValueError('typed region input required')\nvalues = choose_third_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 5, context.origin, context.offset, context.point)\nreturn _first_region_legacy_decision(state, values)"}})


# Whole current sole choose_west_flank_third_formation_point_fields body.
INLINE_DECLARATIONS.update({'choose_west_flank_third_formation_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'return choose_third_formation_point_fields(memory, frame, 5)'}})


# Whole current sole read_outer_west_staging_anchor body.
DECLARATIONS.update({'read_outer_west_staging_anchor': {'signature': 'state: GameState', 'returns': 'Point', 'flow': 'checked_state(state)\nreturn read_outer_west_staging_anchor_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())[1]'}})


# Whole current sole read_outer_west_staging_anchor_fields body.
INLINE_DECLARATIONS.update({'read_outer_west_staging_anchor_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': "frame = _formation_position_frame(memory, frame)\norigin = memory.state.table(713462).cursor()\nframe = first_replace(frame, roster=origin)\nscene = memory.battle_scene()\nframe = _first_word(frame, 'target_x', scene)\noffset = u16(scene << 2)\nframe = _first_shift_word(frame, 'target_x', scene, 2)\nframe = _first_compare_word(frame, offset, 92)\nx = origin.word(offset)\nframe = _first_word(frame, 'unit', x)\nif offset == 92:\n    frame = _first_sub_word(frame, 'unit', x, 3968)\n    x = u16(x - 3968)\n    y = origin.word(offset, 2)\n    frame = _first_word(frame, 'distance', y)\n    frame = _first_sub_word(frame, 'distance', y, 3072)\n    y = u16(y - 3072)\nelse:\n    frame = _first_sub_word(frame, 'unit', x, 3072)\n    x = u16(x - 3072)\n    y = origin.word(offset, 2)\n    frame = _first_word(frame, 'distance', y)\n    frame = _first_compare_word(frame, y, 20480)\n    if y >= 20480:\n        frame = _first_sub_word(frame, 'distance', y, 3968)\n        y = u16(y - 3968)\n    else:\n        frame = _first_add_word(frame, 'distance', y, 3968)\n        y = u16(y + 3968)\nreturn (_first_region_publish(memory, frame), Point(x, y))"}})


# Whole current sole test_first_side_relative_total_shortfall body.
DECLARATIONS.update({'test_first_side_relative_total_shortfall': {'signature': 'state: GameState', 'returns': 'CarryOutcome', 'flow': 'checked_state(state)\n_, selected = test_first_side_relative_total_shortfall_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())\nreturn state.carry_observed(int(selected))'}})


# Whole current sole test_first_side_relative_total_shortfall_fields body.
INLINE_DECLARATIONS.update({'test_first_side_relative_total_shortfall_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': "frame = _first_frame(memory, frame)\ntotal = memory.state.read(4294964894, 4)\nframe = _first_long(frame, 'target_x', total)\nsecondary = memory.state.read(4294964898, 4)\nframe = _first_compare_long(frame, total, secondary)\nselected = False\nif total < secondary:\n    limit = memory.state.read(4294965096, 4)\n    frame = _first_compare_long(frame, total, limit)\n    selected = total < limit\nreturn (_first_region_carry(memory, frame, selected), selected)"}})


# Whole current sole test_second_roster_type6_count_below_four body.
DECLARATIONS.update({'test_second_roster_type6_count_below_four': {'signature': 'state: GameState', 'returns': 'CarryOutcome', 'flow': 'checked_state(state)\n_, selected = test_second_roster_type6_count_below_four_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())\nreturn state.carry_observed(int(selected))'}})


# Whole current sole test_second_roster_type6_count_below_four_fields body.
INLINE_DECLARATIONS.update({'test_second_roster_type6_count_below_four_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': "from .business_actions import _battle_action_map_fields, _deployment_terrain_lookup, _deployment_compare_byte\nframe = _first_frame(memory, frame)\nframe = _first_region_publish(memory, frame)\nframe = _first_call(memory, frame, 150076, _battle_action_map_fields)\nroster = memory.state.table(4294944164).cursor()\npositions = memory.state.table(4294943056).cursor()\nframe = first_replace(frame, candidates=roster, controller=positions)\nframe = _first_word(frame, 'count', 0)\ncount = 0\nwhile True:\n    member = roster.next_word()\n    frame = _first_word(frame, 'distance', member)\n    if negative_word(member):\n        return (_first_region_carry(memory, frame, True), True)\n    offset = u16(member << 2)\n    frame = _first_shift_word(frame, 'distance', member, 2)\n    x = positions.word(offset)\n    frame = _first_word(frame, 'target_y', x)\n    y = positions.word(offset, 2)\n    frame = _first_word(frame, 'unit', y)\n    frame = _first_region_publish(memory, frame)\n    frame, category = _deployment_terrain_lookup(memory, frame, x, y, 150108)\n    frame = _deployment_compare_byte(memory, frame, u8(category), 6)\n    if u8(category) != 6:\n        return (_first_region_carry(memory, frame, False), False)\n    frame = _first_add_word(frame, 'count', count, 1)\n    count = u16(count + 1)\n    frame = _first_compare_word(frame, count, 4)\n    if count >= 4:\n        return (_first_region_carry(memory, frame, False), False)"}})


# Whole current sole test_second_side_threshold_shortfall body.
DECLARATIONS.update({'test_second_side_threshold_shortfall': {'signature': 'state: GameState', 'returns': 'CarryOutcome', 'flow': 'checked_state(state)\n_, selected = test_second_side_threshold_shortfall_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())\nreturn state.carry_observed(int(selected))'}})


# Whole current sole test_second_side_threshold_shortfall_fields body.
INLINE_DECLARATIONS.update({'test_second_side_threshold_shortfall_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': "frame = _first_frame(memory, frame)\ntotal = memory.state.read(4294964898, 4)\nframe = _first_long(frame, 'target_x', total)\nlimit = memory.state.read(4294965100, 4)\nframe = _first_compare_long(frame, total, limit)\nselected = total < limit\nreturn (_first_region_carry(memory, frame, selected), selected)"}})

APPROVED.setdefault('business_actions', set()).update({'_battle_action_map_fields', '_deployment_terrain_lookup', '_deployment_compare_byte'})

DEPLOYMENT_DECLARATIONS.update({'initialize_second_side_deployment': {'signature': 'state: GameState', 'returns': 'None', 'flow': 'checked_state(state)\ninitialize_second_side_deployment_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())'}})

DEPLOYMENT_DECLARATIONS.update({'prepare_second_side_formation_assignment': {'signature': 'state: GameState', 'returns': 'None', 'flow': 'checked_state(state)\nprepare_second_side_formation_assignment_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())'}})

DEPLOYMENT_DECLARATIONS.update({'copy_second_side_position_assignment': {'signature': 'state: GameState, count: Word', 'returns': 'FormationCursors', 'flow': 'checked_state(state)\nuint(count, 16)\nframe = copy_second_side_position_assignment_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), count)\nreturn FormationCursors(frame.candidates, frame.roster)'}})

DEPLOYMENT_DECLARATIONS.update({'populate_second_side_unset_positions': {'signature': 'state: GameState', 'returns': 'None', 'flow': 'checked_state(state)\npopulate_second_side_unset_positions_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())'}})

DEPLOYMENT_DECLARATIONS.update({'prepare_second_side_battlefield_choices': {'signature': 'state: GameState', 'returns': 'FormationCursors', 'flow': 'checked_state(state)\nframe = prepare_second_side_battlefield_choices_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())\nreturn FormationCursors(frame.roster, frame.candidates)'}})

DEPLOYMENT_DECLARATIONS.update({'choose_unused_second_side_point': {'signature': 'state: GameState, source: Cursor, destination: Cursor', 'returns': 'Word', 'flow': 'checked_state(state)\nchecked_cursor(source, state)\nchecked_cursor(destination, state)\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=source, candidates=destination)\nframe = choose_unused_second_side_point_fields(BattlePolicyMemory(state), frame)\nreturn low16(frame.target_x)'}})

DEPLOYMENT_INLINE_DECLARATIONS.update({'copy_choice_window_to_scratch': {'signature': 'state: GameState, source: Cursor, count_minus_one: Word', 'returns': 'Cursor', 'flow': 'checked_state(state)\nchecked_cursor(source, state)\nuint(count_minus_one, 16)\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=source)\nframe = _second_choice_copy_window_fields(BattlePolicyMemory(state), frame, count_minus_one)\nreturn frame.controller'}})

DEPLOYMENT_INLINE_DECLARATIONS.update({'publish_shuffled_choice_window': {'signature': 'state: GameState, source: Cursor, destination: Cursor, count_minus_one: Word, zeros: Word', 'returns': 'None', 'flow': "checked_state(state)\nchecked_cursor(source, state)\nchecked_cursor(destination, state)\nuint(count_minus_one, 16)\nuint(zeros, 16)\nif (count_minus_one, zeros) == (4, 3):\n    continuation = 152192\nelif (count_minus_one, zeros) == (2, 5):\n    continuation = 152234\nelse:\n    raise Boundary('historical choice-window helper has no real source call site for this plan')\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=source, candidates=destination)\n_second_choice_publish_window_fields(BattlePolicyMemory(state), frame, count_minus_one, zeros, continuation)"}})

DEPLOYMENT_INLINE_DECLARATIONS.update({'commit_second_side_selected_point': {'signature': 'state: GameState, index: Word, chosen: Word', 'returns': 'None', 'flow': 'checked_state(state)\nuint(index, 16)\nuint(chosen, 16)\n_second_choice_store_selected_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), index, chosen)'}})

DEPLOYMENT_INLINE_DECLARATIONS.update({'read_first_side_assignment_count_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, roster, continuation: Long=152610', 'returns': 'tuple[FirstDeploymentFrame, Word]', 'flow': "frame = _first_frame(memory, frame)\nif continuation not in (152610, 150292):\n    raise ValueError('actual first/second assignment sort continuation required')\nchecked_policy_table(roster, memory.state)\nthird = roster.word(4)\nframe = _first_memory_word(frame, third)\nif not negative_word(third):\n    second = roster.word(2)\n    frame = _first_memory_word(frame, second)\n    if not negative_word(second):\n        if type(memory.state) is GameState and frame.stack_cursor is None:\n            frame, count = sort_first_side_roster_fields(memory, frame)\n        else:\n            frame = _first_call(memory, frame, continuation, _first_sorted_frame)\n            count = low16(frame.unit)\n        return (frame, count)\ncount = 0\nframe = _first_word(frame, 'unit', count)\nsecond = roster.word(2)\nframe = _first_memory_word(frame, second)\nif not negative_word(second):\n    frame = _first_add_word(frame, 'unit', count, 1)\n    count = 1\nreturn (frame, count)"}})

DEPLOYMENT_INLINE_DECLARATIONS.update({'initialize_second_side_deployment_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _first_frame(memory, frame)\nframe = _first_call(memory, frame, 150262, prepare_second_side_formation_assignment_fields)\nframe = _first_call(memory, frame, 150266, populate_second_side_unset_positions_fields)\nphase = memory.state.table(4294964950)\nphase.word()\nphase.set_word(0, 0)\nreturn _first_region_publish(memory, _first_memory_word(frame, 0))'}})

DEPLOYMENT_INLINE_DECLARATIONS.update({'prepare_second_side_formation_assignment_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _first_frame(memory, frame)\nroster = memory.state.table(4294944164)\nframe, count = read_first_side_assignment_count_fields(memory, frame, roster, 150292)\nframe = _first_call(memory, frame, 150312, lambda memory, entered: copy_second_side_position_assignment_fields(memory, entered, count))\nreturn _first_region_publish(memory, frame)'}})

DEPLOYMENT_INLINE_DECLARATIONS.update({'copy_second_side_position_assignment_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, count: Word=None', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _first_frame(memory, frame)\nif count is None:\n    count = low16(frame.unit)\nuint(count, 16)\nforce = memory.state.read(4294964878, 2)\nframe = _first_word(frame, 'target_x', force)\nframe = _first_shift_word(frame, 'target_x', force, 1)\ndirectory = memory.state.table(150500)\nformation = directory.word(u16(force << 1))\nframe = _first_word(frame, 'target_x', formation)\nframe = _first_shift_word(frame, 'target_x', formation, 4)\nintermediate = u16(formation << 4)\nframe = _first_add_word(frame, 'target_x', intermediate, count)\nintermediate = u16(intermediate + count)\nframe = _first_shift_word(frame, 'target_x', intermediate, 5)\noffset = formation_assignment_offset(formation, count)\nframe = first_replace(frame, roster=memory.state.table(4294946710).cursor(), candidates=memory.state.table(150528).cursor(offset))\nreturn _first_region_publish(memory, copy_first_side_order_fields(memory, frame))"}})

DEPLOYMENT_INLINE_DECLARATIONS.update({'populate_second_side_unset_positions_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _first_call(memory, frame, 152068, prepare_second_side_battlefield_choices_fields)\nframe = first_replace(frame, roster=memory.state.table(4294944164).cursor(), candidates=memory.state.table(4294946710).cursor(), controller=memory.state.table(4294955792), scan=memory.state.table(4294943056).cursor())\nreturn _first_region_publish(memory, submit_unset_deployment_fields(memory, frame))'}})

DEPLOYMENT_INLINE_DECLARATIONS.update({'_second_choice_copy_window_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, count_minus_one: Word', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _first_frame(memory, frame)\nuint(count_minus_one, 16)\nsource = frame.roster\nchecked_policy_table(source, memory.state)\nscratch = memory.state.table(4294955776).cursor()\nframe = first_replace(frame, controller=scratch)\nframe = _first_word(frame, 'target_x', count_minus_one)\nfor counter in descending_inclusive(count_minus_one):\n    word = source.next_word()\n    scratch.append_word(word)\n    frame = _first_memory_word(frame, word)\n    retained = frame.target_x\n    frame = first_replace(frame, target_x=None if retained is None else replace_word(retained, u16(counter - 1)))\nreturn frame"}})

DEPLOYMENT_INLINE_DECLARATIONS.update({'_second_choice_clear_scratch_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, zeros: Word', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _first_frame(memory, frame)\nuint(zeros, 16)\nscratch = frame.controller\nchecked_policy_table(scratch, memory.state)\nif zeros:\n    for _ in descending_inclusive(zeros - 1):\n        scratch.word()\n        scratch.append_word(0)\n        frame = _first_memory_word(frame, 0)\nreturn frame'}})

DEPLOYMENT_INLINE_DECLARATIONS.update({'_second_choice_publish_window_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, count_minus_one: Word, zeros: Word, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "if (count_minus_one, zeros, continuation) not in ((4, 3, 152192), (2, 5, 152234)):\n    raise ValueError('actual second deployment choice-window plan required')\nframe = _second_choice_copy_window_fields(memory, frame, count_minus_one)\nframe = _second_choice_clear_scratch_fields(memory, frame, zeros)\nframe = _first_call(memory, _first_region_publish(memory, frame), continuation, shuffle_first_side_choice_fields)\nscratch = memory.state.table(4294955776).cursor()\nframe = first_replace(frame, controller=scratch)\nframe = _first_word(frame, 'target_x', count_minus_one)\nfor counter in descending_inclusive(count_minus_one):\n    word = scratch.next_word()\n    frame.candidates.append_word(word)\n    frame = _first_memory_word(frame, word)\n    retained = frame.target_x\n    frame = first_replace(frame, target_x=None if retained is None else replace_word(retained, u16(counter - 1)))\nreturn frame"}})

DEPLOYMENT_INLINE_DECLARATIONS.update({'_second_choice_store_selected_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, index: Word, chosen: Word', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _first_frame(memory, frame)\nuint(index, 16)\nuint(chosen, 16)\nif index < 3:\n    memory.state.table(4294965060).set_word(u16(index << 1), chosen)\n    frame = _first_memory_word(frame, chosen)\nmemory.state.table(16727746).set_word(u16(index << 1), chosen)\nreturn _first_memory_word(frame, chosen)'}})

DEPLOYMENT_INLINE_DECLARATIONS.update({'prepare_second_side_battlefield_choices_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _first_frame(memory, frame)\nframe = first_replace(frame, roster=memory.state.table(710768).cursor())\nscene = memory.battle_scene()\nframe = _first_word(frame, 'target_x', scene)\nframe = _first_word(frame, 'target_y', scene)\noffset = scene\nfor shift in (1, 1, 2):\n    frame = _first_shift_word(frame, 'target_x', offset, shift)\n    offset = u16(offset << shift)\n    frame = _first_add_word(frame, 'target_x', offset, scene)\n    offset = u16(offset + scene)\nframe = _first_shift_word(frame, 'target_x', offset, 1)\noffset = u16(offset << 1)\nframe = first_replace(frame, roster=frame.roster.advance(s16(offset)), candidates=memory.state.table(4294955792).cursor())\nword = frame.roster.next_word()\nframe.candidates.append_word(word)\nframe = _first_memory_word(frame, word)\nframe = _second_choice_publish_window_fields(memory, frame, 4, 3, 152192)\nframe = _second_choice_publish_window_fields(memory, frame, 2, 5, 152234)\nselected = memory.state.table(4294965060)\nfor offset in (0, 2, 4):\n    selected.word(offset)\n    selected.set_word(offset, 0)\n    frame = _first_memory_word(frame, 0)\nfor index, continuation in ((0, 152264), (1, 152278), (2, 152292), (3, 152306)):\n    frame = _first_call(memory, _first_region_publish(memory, frame), continuation, choose_unused_second_side_point_fields)\n    frame = _second_choice_store_selected_fields(memory, frame, index, low16(frame.target_x))\nreturn _first_region_publish(memory, frame)"}})

DEPLOYMENT_INLINE_DECLARATIONS.update({'choose_unused_second_side_point_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _second_choice_copy_window_fields(memory, frame, 4)\nframe = _second_choice_clear_scratch_fields(memory, frame, 3)\nframe = _first_call(memory, _first_region_publish(memory, frame), 152398, shuffle_first_side_choice_fields)\nscratch = memory.state.table(4294955776).cursor()\nframe = first_replace(frame, controller=scratch)\nwhile True:\n    candidate = scratch.next_word()\n    frame = _first_word(frame, 'target_x', candidate)\n    selected = memory.state.read(4294965060, 2)\n    frame = _first_compare_word(frame, candidate, selected)\n    if candidate == selected:\n        continue\n    selected = memory.state.read(4294965062, 2)\n    frame = _first_compare_word(frame, candidate, selected)\n    if candidate == selected:\n        continue\n    selected = memory.state.read(4294965064, 2)\n    frame = _first_compare_word(frame, candidate, selected)\n    if candidate == selected:\n        continue\n    frame.candidates.append_word(candidate)\n    return _first_region_publish(memory, _first_memory_word(frame, candidate))"}})

APPROVED.setdefault('domain', set()).update({'s16'})
