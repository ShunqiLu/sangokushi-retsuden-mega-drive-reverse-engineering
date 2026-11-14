"""Restricted complete action AST contracts and ordinary 68000 lowering.

Only explicit semantic text is consumed. Target instruction selection remains
separate from game rules; this module never reads ROM, old assembly or caches.
"""
import ast
from .compiler_common import semantic_functions, lower_declared, CompileError
from .target import ACTIONS_BINDINGS


def _ins(e, operation, operands='', width=2):
    e.ins(operation, operands, width)


def _name(e, role):
    return e.binding.name + '_' + role


def _mark(e, role):
    e.label(_name(e, role))


def _branch(e, operation, role):
    _ins(e, operation, _name(e, role), 4 if operation.endswith('.w') else 2)


def _call(e, name, absolute=False, short=False):
    _ins(e, 'jsr' if absolute else 'bsr.b' if short else 'bsr.w',
         name + (':l' if absolute else ''), 6 if absolute else 2 if short else 4)


def _carry(e, value):
    _ins(e, 'ori.w' if value else 'andi.w',
         '#1,%sr' if value else '#65534,%sr', 4)


def _budget_sample(e, multiplier, base):
    _call(e, 'step_random', True)
    _ins(e, 'andi.l', '#65535,%d0', 6)
    _ins(e, 'move.l', '%d0,%d1')
    _ins(e, 'lsl.l', '#2,%d0')
    _ins(e, 'add.l', '%d1,%d0')
    _ins(e, 'lsl.l', '#1,%d0')
    if multiplier == 11:
        _ins(e, 'add.l', '%d1,%d0')
    else:
        _ins(e, 'add.l', '%d0,%d1')
    _ins(e, 'swap', '%d0')
    _ins(e, 'addi.w', f'#{base},%d0', 4)


def _selected_troop_budget(e, r, multiplier, reload_previous=False):
    _budget_sample(e, multiplier, r['base'])
    _ins(e, 'lea.l', '0xc800:w,%a0', 4)
    _ins(e, 'move.w', '0xf3a6:w,%d1', 4)
    _ins(e, 'lsl.w', '#2,%d1')
    _ins(e, 'move.l', '(%a0, %d1.w),%d1', 4)
    _ins(e, 'divu.w', '%d0,%d1')
    _ins(e, 'andi.l', '#65535,%d1', 6)
    _ins(e, 'move.l', '0xf39e:w,%d1' if reload_previous else '%d1,0xf39e:w', 4)


def _candidate_troop_budget(e, r, updated_state=False):
    _ins(e, 'lea.l', '0xc800:w,%a0', 4)
    _ins(e, 'lsl.w', '#2,%d5')
    _ins(e, 'move.l', '(%a0, %d5.w),%d2', 4)
    _call(e, 'step_random', True)
    _ins(e, 'andi.l', '#65535,%d0', 6)
    if not updated_state:
        _ins(e, 'move.l', '%d0,%d1')
    _ins(e, 'lsl.l', '#2,%d0')
    _ins(e, 'add.l', '%d1,%d0')
    _ins(e, 'lsl.l', '#1,%d0')
    _ins(e, 'add.l', '%d1,%d0')
    _ins(e, 'swap', '%d0')
    _ins(e, 'addi.w', f'#{r["base"]},%d0', 4)
    _ins(e, 'divu.w', '%d0,%d2')
    _ins(e, 'andi.l', '#65535,%d2', 6)
    _ins(e, 'move.l', '%d2,0xf39e:w', 4)


def _attribute_budget(e, r, read_first=False):
    if read_first:
        _ins(e, 'lea.l', '0xb400:w,%a0', 4)
        _ins(e, 'move.w', '0xf3a6:w,%d0', 4)
        _ins(e, 'lsl.w', '#1,%d0')
        _ins(e, 'move.w', '(%a0, %d0.w),%d2', 4)
        _ins(e, 'lea.l', '0xb600:w,%a0', 4)
        _ins(e, 'add.w', '(%a0, %d0.w),%d2', 4)
    _call(e, 'step_random', True)
    _ins(e, 'andi.l', '#65535,%d0', 6)
    _ins(e, 'move.l', '%d0,%d1' if read_first else '%d0,%d2')
    _ins(e, 'lsl.l', '#2,%d0')
    _ins(e, 'add.l', '%d1,%d0' if read_first else '%d2,%d0')
    _ins(e, 'swap', '%d0')
    if r['base'] <= 8:
        _ins(e, 'addq.w', f'#{r["base"]},%d0')
    else:
        raise CompileError('attribute base must retain ADDQ encoding')
    if not read_first:
        _ins(e, 'lea.l', '0xb400:w,%a0', 4)
        _ins(e, 'move.w', '0xf3a6:w,%d2', 4)
        _ins(e, 'lsl.w', '#1,%d2')
        _ins(e, 'move.w', '(%a0, %d2.w),%d3', 4)
        _ins(e, 'lea.l', '0xb600:w,%a0', 4)
        _ins(e, 'add.w', '(%a0, %d2.w),%d3', 4)
    _ins(e, 'mulu.w', '%d2,%d0' if read_first else '%d3,%d0')
    _ins(e, 'move.l', '%d0,0xf39e:w', 4)


def _lowest_rating(e, r, filtered=False):
    _ins(e, 'lea.l', '0xc300:w,%a0' if filtered else '0xd300:w,%a0', 4)
    _ins(e, 'lea.l', '0xd400:w,%a1' if filtered else '0xc300:w,%a1', 4)
    _ins(e, 'move.w', '#65535,%d0', 4)
    if not filtered:
        _ins(e, 'move.w', '#65535,%d1', 4)
    _mark(e, 'member')
    _ins(e, 'move.w', '(%a1)+,%d2' if filtered else '(%a0)+,%d2')
    _branch(e, 'bmi.w' if filtered else 'bmi.b', 'return')
    _ins(e, 'andi.w', '#255,%d2', 4)
    _ins(e, 'move.b', '(%a0, %d2.w),%d3' if filtered else '(%a1, %d2.w),%d3', 4)
    if not filtered:
        _branch(e, 'beq.b', 'member')
    _ins(e, 'cmp.b', '%d0,%d3')
    _branch(e, 'bcc.b', 'member')
    _ins(e, 'move.b', '%d3,%d0')
    _ins(e, 'move.w', '%d2,%d1')
    _branch(e, 'bra.b', 'member')
    _mark(e, 'return')


def _strongest(e, r, types, supplied_map=False, alternate_tables=False):
    if not supplied_map:
        _call(e, 'load_battlefield_map_context', True)
    _ins(e, 'lea.l', '0xd300:w,%a1', 4)
    _ins(e, 'lea.l', '0xc800:w,%a2' if alternate_tables else '0xa150:w,%a2', 4)
    _ins(e, 'lea.l', '0xa150:w,%a3' if alternate_tables else '0xc800:w,%a3', 4)
    _ins(e, 'moveq', '#0,%d4')
    _ins(e, 'move.w', '#65535,%d5', 4)
    _mark(e, 'member')
    _ins(e, 'move.w', '(%a1)+,%d3')
    _branch(e, 'bmi.w', 'return')
    _ins(e, 'andi.w', '#255,%d3', 4)
    _ins(e, 'move.w', '%d3,%d2')
    _ins(e, 'lsl.w', '#2,%d2')
    position = '%a3' if alternate_tables else '%a2'
    strength = '%a2' if alternate_tables else '%a3'
    _ins(e, 'move.w', f'({position}, %d2.w),%d1', 4)
    _ins(e, 'lsr.w', '#7,%d1')
    _ins(e, 'move.w', f'2({position}, %d2.w),%d2', 4)
    _ins(e, 'lsr.w', '#7,%d2')
    _call(e, 'read_battlefield_terrain_type', True)
    for kind in types[:-1]:
        _ins(e, 'cmpi.b', f'#{kind},%d0', 4)
        _branch(e, 'beq.w', 'score')
    _ins(e, 'cmpi.b', f'#{types[-1]},%d0', 4)
    _branch(e, 'bne.b', 'member')
    _mark(e, 'score')
    _ins(e, 'move.w', '%d3,%d0')
    _call(e, 'weighted_training_factor', True)
    _ins(e, 'lsl.w', '#2,%d0')
    _ins(e, 'mulu.w', f'2({strength}, %d0.w),%d1', 4)
    _ins(e, 'cmp.l', '%d4,%d1')
    _branch(e, r.get('score_failure', 'bls') + '.b', 'member')
    _ins(e, 'move.l', '%d1,%d4')
    _ins(e, 'move.w', '%d3,%d5')
    _branch(e, 'bra.b', 'member')
    _mark(e, 'return')


def _terrain_gate(e, r, map_relative=False):
    _call(e, 'load_battlefield_map_context', True)
    _ins(e, 'lea.l', '0xa150:w,%a1', 4)
    _ins(e, 'move.w', '%d7,%d0')
    _ins(e, 'lsl.w', '#2,%d0')
    base = '%a0' if map_relative else '%a1'
    _ins(e, 'move.w', f'({base}, %d0.w),%d1', 4)
    _ins(e, 'lsr.w', '#7,%d1')
    _ins(e, 'move.w', f'2({base}, %d0.w),%d2', 4)
    _ins(e, 'lsr.w', '#7,%d2')
    _call(e, 'read_battlefield_terrain_type', True)
    for kind in (0, 4, 7 if map_relative else 8):
        _ins(e, 'cmpi.b', f'#{kind},%d0', 4)
        _branch(e, 'beq.w', 'matched')
    _carry(e, 1 if map_relative else 0)
    _branch(e, 'bra.w', 'return')
    _mark(e, 'matched')
    _carry(e, 0 if map_relative else 1)
    _mark(e, 'return')


def _filter_candidates(e, r):
    _call(e, 'load_battlefield_map_context', True)
    for address, register in (('0xd300', '%a1'), ('0xc800', '%a2'),
                              ('0xa150', '%a3'), ('0xd400', '%a4')):
        _ins(e, 'lea.l', address + ':w,' + register, 4)
    _mark(e, 'member')
    _ins(e, 'move.w', '(%a1)+,%d3')
    _branch(e, 'bmi.w', 'terminate')
    _ins(e, 'andi.w', '#255,%d3', 4)
    _ins(e, 'move.w', '%d3,%d2')
    _ins(e, 'lsl.w', '#2,%d2')
    _ins(e, 'move.w', '(%a3, %d2.w),%d1', 4)
    _ins(e, 'lsr.w', '#7,%d1')
    _ins(e, 'move.w', '2(%a3, %d2.w),%d2', 4)
    _ins(e, 'lsr.w', '#7,%d2')
    _call(e, 'read_battlefield_terrain_type', True)
    _ins(e, 'cmpi.b', '#6,%d0', 4)
    _branch(e, 'beq.b', 'member')
    _ins(e, 'move.w', '%d3,(%a4)+')
    _branch(e, 'bra.b', 'member')
    _mark(e, 'terminate')
    _ins(e, 'move.w', '#65535,(%a4)', 4)


def _read_city_anchor(e, r):
    _ins(e, 'lea.l', '0x9fff:w,%a3', 4)
    _ins(e, 'move.w', '0xf68a:w,%d0', 4)
    _ins(e, 'clr.w', '%d2')
    _ins(e, 'move.b', '(%a3, %d0.w),%d2', 4)
    _ins(e, 'lea.l', '0xabda8:l,%a3', 6)
    _ins(e, 'lsl.w', '#5,%d0')
    _ins(e, 'lsl.w', '#1,%d2')
    _ins(e, 'add.w', '%d0,%d2')
    _ins(e, 'clr.w', '%d0')
    _ins(e, 'move.b', '(%a3, %d2.w),%d0', 4)
    _ins(e, 'clr.w', '%d1')
    _ins(e, 'move.b', '1(%a3, %d2.w),%d1', 4)


def _read_second_anchor(e, r):
    _ins(e, 'lea.l', '0xae2f6:l,%a3', 6)
    _ins(e, 'move.w', '0xf68a:w,%d2', 4)
    _ins(e, 'lsl.w', '#2,%d2')
    _ins(e, 'move.w', '(%a3, %d2.w),%d0', 4)
    _ins(e, 'lsr.w', '#3,%d0')
    _ins(e, 'lsr.w', '#7,%d0')
    _ins(e, 'move.w', '2(%a3, %d2.w),%d1', 4)
    _ins(e, 'lsr.w', '#3,%d1')
    _ins(e, 'lsr.w', '#7,%d1')


def _build_occupied(e, r):
    for address, register in (('0xa150', '%a3'), ('0xd300', '%a1'), ('0xa550', '%a2')):
        _ins(e, 'lea.l', address + ':w,' + register, 4)
    _call(e, 'append_roster_occupied_cells')
    _ins(e, 'lea.l', '0xa5a4:w,%a2', 4)
    _call(e, 'append_roster_occupied_cells')
    _ins(e, 'move.w', '#65535,(%a1)', 4)


def _append_occupied(e, r):
    _mark(e, 'member')
    _ins(e, 'move.w', '(%a2)+,%d2')
    _branch(e, 'bmi.w', 'return')
    _ins(e, 'lsl.w', '#2,%d2')
    _ins(e, 'move.w', '(%a3, %d2.w),%d3', 4)
    _branch(e, 'beq.b', 'member')
    _ins(e, 'lsr.w', '#7,%d3')
    _ins(e, 'lsr.w', '#3,%d3')
    _ins(e, 'move.b', '%d3,(%a1)+')
    _ins(e, 'move.w', '2(%a3, %d2.w),%d3', 4)
    _ins(e, 'lsr.w', '#7,%d3')
    _ins(e, 'lsr.w', '#3,%d3')
    _ins(e, 'move.b', '%d3,(%a1)+')
    _branch(e, 'bra.b', 'member')
    _mark(e, 'return')


def _find_empty(e, r):
    _mark(e, 'member')
    _ins(e, 'move.w', '(%a3)+,%d6')
    _branch(e, 'bmi.w', 'exhausted')
    _ins(e, 'lsl.w', '#2,%d6')
    _ins(e, 'tst.l', '(%a1, %d6.w)', 4)
    _branch(e, 'bne.b', 'member')
    _carry(e, 0)
    _branch(e, 'bra.w', 'return')
    _mark(e, 'exhausted')
    _carry(e, 1)
    _mark(e, 'return')


def _scan_edge(e, r, second=False):
    component = '%d3' if second else '%d2'
    center = '%d1' if second else '%d0'
    bound = 37 if second else 25
    _ins(e, 'move.w', '%d7,' + component)
    _ins(e, 'neg.w', component)
    _ins(e, 'add.w', center + ',' + component)
    _ins(e, 'cmpi.w', '#3,' + component, 4)
    _branch(e, 'bcs.w', 'decline')
    _ins(e, 'cmpi.w', f'#{bound},' + component, 4)
    _branch(e, 'bhi.w', 'decline')
    _ins(e, 'move.w', '%d7,%d4')
    if second:
        _ins(e, 'subq.w', '#2,%d4')
    _ins(e, 'neg.w', '%d4')
    _mark(e, 'cell')
    variable = '%d2' if second else '%d3'
    _ins(e, 'move.w', '%d4,' + variable)
    _ins(e, 'add.w', ('%d0' if second else '%d1') + ',' + variable)
    _ins(e, 'cmpi.w', '#3,' + variable, 4)
    _branch(e, 'bcs.w', 'next')
    _ins(e, 'cmpi.w', ('#25,' if second else '#37,') + variable, 4)
    _branch(e, 'bhi.w', 'next')
    _call(e, 'try_place_deployment_cell')
    _branch(e, 'bcc.w', 'next')
    _call(e, 'find_next_empty_position_slot', short=not second)
    _branch(e, 'bcs.w', 'complete')
    _mark(e, 'next')
    _ins(e, 'addq.w', '#2,%d4')
    _ins(e, 'cmp.w', '%d7,%d4')
    _branch(e, 'blt.b' if second else 'ble.b', 'cell')
    _mark(e, 'decline')
    _carry(e, 0)
    _branch(e, 'bra.w', 'return')
    _mark(e, 'complete')
    _carry(e, 1)
    _mark(e, 'return')


def _place_cell(e, r):
    _ins(e, 'movem.l', '%d0-%d4,-(%a7)', 4)
    _ins(e, 'lea.l', '0xd300:w,%a2', 4)
    for source, lower, upper in (('%d2', '%d0', '%d2'), ('%d3', '%d1', '%d3')):
        _ins(e, 'move.w', source + ',' + lower)
        _ins(e, 'subi.w', '#3,' + lower, 4)
        _ins(e, 'addi.w', '#3,' + upper, 4)
    _ins(e, 'clr.w', '%d4')
    _mark(e, 'occupied')
    _ins(e, 'move.b', '(%a2),%d4')
    _branch(e, 'bmi.w', 'terrain')
    for bound, branch in (('%d0', 'blt.w'), ('%d2', 'bgt.w')):
        _ins(e, 'cmp.w', bound + ',%d4')
        _branch(e, branch, 'next')
    _ins(e, 'move.b', '1(%a2),%d4', 4)
    for bound, branch in (('%d1', 'blt.w'), ('%d3', 'bgt.w')):
        _ins(e, 'cmp.w', bound + ',%d4')
        _branch(e, branch, 'next')
    _mark(e, 'reject')
    _ins(e, 'movem.l', '(%a7)+,%d0-%d4', 4)
    _carry(e, 0)
    _branch(e, 'bra.w', 'return')
    _mark(e, 'next')
    _ins(e, 'addq.w', '#2,%a2')
    _branch(e, 'bra.b', 'occupied')
    _mark(e, 'terrain')
    for register in ('%d0', '%d1'):
        _ins(e, 'addi.w', '#3,' + register, 4)
        _ins(e, 'lsl.w', '#3,' + register)
    _ins(e, 'move.w', '%d1,%d2')
    _ins(e, 'move.w', '%d0,%d1')
    _call(e, 'read_battlefield_terrain_type', True)
    for kind in (1, 6, 7):
        _ins(e, 'cmpi.b', f'#{kind},%d0', 4)
        _branch(e, 'beq.b', 'reject')
    _ins(e, 'lsl.w', '#7,%d1')
    _ins(e, 'move.w', '%d1,(%a1, %d6.w)', 4)
    _ins(e, 'lsl.w', '#7,%d2')
    _ins(e, 'move.w', '%d2,2(%a1, %d6.w)', 4)
    _ins(e, 'movem.l', '(%a7)+,%d0-%d4', 4)
    _carry(e, 1)
    _mark(e, 'return')


def _promote_primary(e, r):
    _ins(e, 'lea.l', '0xe640:w,%a0', 4)
    _ins(e, 'move.w', '0xf68c:w,%d0', 4)
    _ins(e, 'lsl.w', '#1,%d0')
    _ins(e, 'move.w', '(%a0, %d0.w),%d0', 4)
    _ins(e, 'lea.l', '0xa027:w,%a0', 4)
    _ins(e, 'move.w', '0xf68a:w,%d1', 4)
    _ins(e, 'move.b', '(%a0, %d1.w),%d1', 4)
    _ins(e, 'cmp.w', '%d0,%d1')
    _branch(e, 'beq.w', 'return')
    _ins(e, 'lea.l', '0xa550:w,%a0', 4)
    _mark(e, 'find')
    _ins(e, 'move.w', '(%a0)+,%d2')
    _branch(e, 'bmi.w', 'return')
    _ins(e, 'andi.w', '#255,%d2', 4)
    _ins(e, 'cmp.w', '%d2,%d0')
    _branch(e, 'bne.b', 'find')
    _ins(e, 'lea.l', '0xae28:w,%a2', 4)
    _ins(e, 'move.b', '#1,(%a2, %d0.w)', 6)
    _ins(e, 'lea.l', '0x9fff:w,%a0', 4)
    _ins(e, 'move.w', '0xf68a:w,%d2', 4)
    _ins(e, 'move.b', '(%a0, %d2.w),%d3', 4)
    _ins(e, 'lsl.w', '#1,%d3')
    _ins(e, 'lsl.w', '#5,%d2')
    _ins(e, 'add.w', '%d3,%d2')
    _ins(e, 'lsl.w', '#2,%d0')
    _ins(e, 'lea.l', '0xabda8:l,%a1', 6)
    _ins(e, 'lea.l', '0xff2c00:l,%a3', 6)
    for displacement in (0, 2):
        _ins(e, 'clr.w', '%d3')
        _ins(e, 'move.b', ('1' if displacement else '') + '(%a1, %d2.w),%d3', 4)
        _ins(e, 'lsl.w', '#3,%d3')
        _ins(e, 'move.w', '%d3,' + ('2' if displacement else '') + '(%a3, %d0.w)', 4)
    _ins(e, 'lea.l', '0xa150:w,%a0', 4)
    _ins(e, 'lsl.w', '#2,%d1')
    _ins(e, 'clr.w', '%d3')
    _ins(e, 'move.b', '(%a1, %d2.w),%d3', 4)
    _ins(e, 'lsl.w', '#3,%d3')
    _ins(e, 'lsl.w', '#7,%d3')
    _ins(e, 'sub.w', '(%a0, %d1.w),%d3', 4)
    _branch(e, 'bcc.w', 'x_positive')
    _ins(e, 'neg.w', '%d3')
    _mark(e, 'x_positive')
    _ins(e, 'cmpi.w', '#1024,%d3', 4)
    _branch(e, 'bhi.w', 'promote')
    _ins(e, 'clr.w', '%d3')
    _ins(e, 'move.b', '1(%a1, %d2.w),%d3', 4)
    _ins(e, 'lsl.w', '#3,%d3')
    _ins(e, 'lsl.w', '#7,%d3')
    _ins(e, 'sub.w', '2(%a0, %d1.w),%d3', 4)
    _branch(e, 'bcc.w', 'y_positive')
    _ins(e, 'neg.w', '%d3')
    _mark(e, 'y_positive')
    _ins(e, 'cmpi.w', '#1024,%d3', 4)
    _branch(e, 'bcc.w', 'promote')
    for displacement in (0, 2):
        _ins(e, 'move.w', ('2' if displacement else '') + '(%a0, %d0.w),%d3', 4)
        _ins(e, 'lsr.w', '#7,%d3')
        _ins(e, 'move.w', '%d3,' + ('2' if displacement else '') + '(%a3, %d1.w)', 4)
    _ins(e, 'lsr.w', '#2,%d1')
    _ins(e, 'move.b', '#1,(%a2, %d1.w)', 6)
    _mark(e, 'promote')
    _ins(e, 'lsr.w', '#2,%d0')
    _ins(e, 'lea.l', '0xa550:w,%a0', 4)
    _ins(e, 'lea.l', '0xa552:w,%a1', 4)
    _mark(e, 'copy')
    _ins(e, 'move.w', '(%a0)+,%d1')
    _branch(e, 'bmi.w', 'commit')
    _ins(e, 'cmp.w', '%d0,%d1')
    _branch(e, 'beq.b', 'copy')
    _ins(e, 'move.w', '%d1,(%a1)+')
    _branch(e, 'bra.b', 'copy')
    _mark(e, 'commit')
    _ins(e, 'move.w', '%d0,0xa550:w', 4)
    _ins(e, 'lea.l', '0xa027:w,%a0', 4)
    _ins(e, 'move.w', '0xf68a:w,%d1', 4)
    _ins(e, 'move.b', '%d0,(%a0, %d1.w)', 4)
    _mark(e, 'return')


def _promote_secondary(e, r):
    _ins(e, 'lea.l', '0xe640:w,%a0', 4)
    _ins(e, 'move.w', '0xf68e:w,%d0', 4)
    _ins(e, 'lsl.w', '#1,%d0')
    _ins(e, 'move.w', '(%a0, %d0.w),%d0', 4)
    _ins(e, 'lea.l', '0xf45e:w,%a0', 4)
    _ins(e, 'move.w', '0xf68a:w,%d1', 4)
    _ins(e, 'lsl.w', '#1,%d1')
    _ins(e, 'move.w', '(%a0, %d1.w),%d1', 4)
    _ins(e, 'cmp.w', '%d0,%d1')
    _branch(e, 'beq.w', 'return')
    _ins(e, 'lea.l', '0xa5a4:w,%a0', 4)
    _mark(e, 'find')
    _ins(e, 'move.w', '(%a0)+,%d2')
    _branch(e, 'bmi.w', 'return')
    _ins(e, 'andi.w', '#255,%d2', 4)
    _ins(e, 'cmp.w', '%d0,%d2')
    _branch(e, 'bne.b', 'find')
    _ins(e, 'lea.l', '0xae28:w,%a2', 4)
    _ins(e, 'move.b', '#1,(%a2, %d0.w)', 6)
    _ins(e, 'lea.l', '0xad86e:l,%a0', 6)
    _ins(e, 'move.w', '0xf68a:w,%d2', 4)
    _ins(e, 'move.w', '%d2,%d3')
    _ins(e, 'lsl.w', '#1,%d2')
    _ins(e, 'add.w', '%d3,%d2')
    _ins(e, 'lsl.w', '#1,%d2')
    _ins(e, 'add.w', '%d3,%d2')
    _ins(e, 'lsl.w', '#2,%d2')
    _ins(e, 'add.w', '%d3,%d2')
    _ins(e, 'lsl.w', '#1,%d2')
    _ins(e, 'lea.l', '0xff2c00:l,%a1', 6)
    _ins(e, 'lsl.w', '#2,%d0')
    for displacement in (0, 2):
        _ins(e, 'clr.w', '%d3')
        _ins(e, 'move.b', ('1' if displacement else '') + '(%a0, %d2.w),%d3', 4)
        _ins(e, 'lsl.w', '#3,%d3')
        _ins(e, 'lsl.w', '#7,%d3')
        _ins(e, 'move.w', '%d3,' + ('2' if displacement else '') + '(%a1, %d0.w)', 4)
    _ins(e, 'lea.l', '0xa5a4:w,%a0', 4)
    _ins(e, 'lea.l', '0xa5a6:w,%a1', 4)
    _mark(e, 'copy')
    _ins(e, 'move.w', '(%a0)+,%d2')
    _branch(e, 'bmi.w', 'commit')
    _ins(e, 'andi.w', '#255,%d2', 4)
    _ins(e, 'cmp.w', '%d0,%d2')
    _branch(e, 'beq.b', 'copy')
    _ins(e, 'move.w', '%d2,(%a1)+')
    _branch(e, 'bra.b', 'copy')
    _mark(e, 'commit')
    _ins(e, 'move.w', '%d0,0xa5a4:w', 4)
    _ins(e, 'lea.l', '0xf45e:w,%a0', 4)
    _ins(e, 'move.w', '0xf68a:w,%d1', 4)
    _ins(e, 'lsl.w', '#1,%d1')
    _ins(e, 'move.w', '%d0,(%a0, %d1.w)', 4)
    _mark(e, 'return')


LOWERERS = {
    'read_city_deployment_anchor': _read_city_anchor,
    'build_deployment_occupied_cells': _build_occupied,
    'append_roster_occupied_cells': _append_occupied,
    'find_next_empty_position_slot': _find_empty,
    'scan_deployment_first_edge': lambda e, r: _scan_edge(e, r),
    'try_place_deployment_cell': _place_cell,
    'scan_deployment_second_edge': lambda e, r: _scan_edge(e, r, True),
    'promote_first_roster_deployment_candidate': _promote_primary,
    'read_city_second_deployment_anchor': _read_second_anchor,
    'promote_second_roster_deployment_candidate': _promote_secondary,
    'select_lowest_nonzero_rating': _lowest_rating,
    'compute_selected_attribute_budget': _attribute_budget,
    'select_strongest_open_terrain_candidate': lambda e, r: _strongest(e, r, (0, 3, 7, 1)),
    'compute_selected_troop_budget_base20': lambda e, r: _selected_troop_budget(e, r, 10),
    'compute_selected_troop_budget_base30': lambda e, r: _selected_troop_budget(e, r, 11),
    'select_strongest_type1_candidate': lambda e, r: _strongest(e, r, (1,)),
    'compute_then_reload_previous_selected_budget': lambda e, r: _selected_troop_budget(e, r, 11, True),
    'test_actor_types_0_4_8': _terrain_gate,
    'select_strongest_type2_candidate': lambda e, r: _strongest(e, r, (2,)),
    'compute_selected_type2_budget_base30': lambda e, r: _selected_troop_budget(e, r, 11),
    'select_lowest_filtered_rating': lambda e, r: _lowest_rating(e, r, True),
    'compute_selected_attribute_budget_second_side': lambda e, r: _attribute_budget(e, r, True),
    'build_non_type6_candidates': _filter_candidates,
    'select_strongest_type6_candidate': lambda e, r: _strongest(e, r, (6,), alternate_tables=True),
    'compute_type6_budget_from_random_state': lambda e, r: _candidate_troop_budget(e, r, True),
    'select_strongest_open_terrain_candidate_second_side': lambda e, r: _strongest(e, r, (0, 3, 7, 1)),
    'compute_candidate_budget_base20': _candidate_troop_budget,
    'compute_candidate_budget_base30': _candidate_troop_budget,
    'select_strongest_type1_candidate_second_side': lambda e, r: _strongest(e, r, (1,)),
    'compute_type1_candidate_budget_base20': _candidate_troop_budget,
    'test_actor_map_relative_types': lambda e, r: _terrain_gate(e, r, True),
    'select_strongest_type2_candidate_with_map_context': lambda e, r: _strongest(e, r, (2,), True),
    'compute_type2_candidate_budget_base30': _candidate_troop_budget,
}


def compile_actions(source, *, selected_names=None):
    normalized, failure, actual_policy = _action_score_policy(source)
    records = semantic_functions(normalized, {**DECLARATIONS, **DOMAIN_DECLARATIONS}, APPROVED)
    first_action_fields = {name: records[name] for name in ('_action_child_frame', '_action_child_publish', '_action_factor_add_long_fields', '_action_factor_shift_long_fields', '_action_random_factor_fields', '_action_attribute_product_fields', 'select_action_lowest_rating_fields', 'select_lowest_nonzero_rating_fields', 'compute_selected_attribute_budget_fields', '_select_first_side_terrain_action_fields', 'select_strongest_open_terrain_candidate_fields', 'select_strongest_type1_candidate_fields', 'select_strongest_type2_candidate_fields', '_compute_first_selected_troop_budget_fields', 'compute_selected_troop_budget_base20_fields', 'compute_selected_troop_budget_base30_fields', 'compute_then_reload_previous_selected_budget_fields', 'compute_selected_type2_budget_base30_fields', 'test_actor_action_terrain_gate_fields', 'test_actor_types_0_4_8_fields', 'state_mixed_action_requirement_fields', 'select_lowest_filtered_rating_fields', 'test_actor_map_relative_types_fields', 'attribute_action_requirement', 'troop_action_requirement')}
    records['compute_candidate_budget_base30']['rules'].update(records['compute_candidate_budget_base30_fields']['rules'])
    records['compute_candidate_budget_base20']['rules'].update(records['compute_candidate_budget_base20_fields']['rules'])
    records['compute_type6_budget_from_random_state']['rules'].update(records['compute_type6_budget_from_random_state_fields']['rules'])
    attribute_fields = {name: records[name] for name in ATTRIBUTE_ACTION_FIELD_HELPERS}
    records['compute_selected_attribute_budget_second_side']['rules']['base'] = attribute_fields['compute_selected_attribute_budget_second_side_fields']['rules']['base']
    for owner in ('select_lowest_filtered_rating', 'compute_selected_attribute_budget_second_side', 'build_non_type6_candidates'):
        records[owner]['effects'] += '\nactual sole second-side action fields: ' + '\n'.join((attribute_fields[name]['effects'] for name in ATTRIBUTE_ACTION_FIELD_HELPERS))
    for name in ATTRIBUTE_ACTION_FIELD_HELPERS:
        records.pop(name)
    late_fields = {name: records[name] for name in LATE_TERRAIN_ACTION_FIELD_HELPERS}
    for owner, helper in (('compute_type1_candidate_budget_base20', 'compute_type1_candidate_budget_base20_fields'), ('compute_type2_candidate_budget_base30', 'compute_type2_candidate_budget_base30_fields')):
        records[owner]['rules'].update(late_fields[helper]['rules'])
    for owner in ('select_strongest_type1_candidate_second_side', 'compute_type1_candidate_budget_base20', 'test_actor_map_relative_types', 'select_strongest_type2_candidate_with_map_context', 'compute_type2_candidate_budget_base30'):
        records[owner]['effects'] += '\nactual sole late type1/type2 fields: ' + '\n'.join((late_fields[name]['effects'] for name in LATE_TERRAIN_ACTION_FIELD_HELPERS))
    for name in LATE_TERRAIN_ACTION_FIELD_HELPERS:
        records.pop(name)
    anchor_fields = records.pop('read_city_deployment_anchor_fields')
    records['read_city_deployment_anchor']['effects'] += '\nactual supplied anchor fields: ' + anchor_fields['effects']
    for owner in TERRAIN_DEPLOYMENT_OWNERS:
        records[owner]['effects'] += '\nactual sole terrain/deployment algorithms: ' + '\n'.join((records[name]['effects'] for name in TERRAIN_DEPLOYMENT_HELPERS))
    for name in TERRAIN_DEPLOYMENT_HELPERS:
        records.pop(name)
    for owner, helpers in DEPLOYMENT_FIELD_ALGORITHMS.items():
        records[owner]['effects'] += '\nactual supplied deployment fields: ' + '\n'.join((records[name]['effects'] for name in helpers))
    for name in DEPLOYMENT_FIELD_HELPERS:
        records.pop(name)
    for name in DOMAIN_HELPERS:
        records.pop(name)
    for name in SCORE_SELECTIONS:
        records[name]['rules']['score_failure'] = failure
        records[name]['effects'] += '\nfinite-inlined candidate policy: ' + actual_policy
    for name in DOMAIN_ENTRIES:
        records[name]['effects'] += '\nfinite-inlined typed domain effects: ' + '\n'.join((DOMAIN_DECLARATIONS[helper]['flow'] for helper in DOMAIN_HELPERS))
    for owner in ('select_lowest_nonzero_rating', 'compute_selected_attribute_budget', 'select_strongest_open_terrain_candidate', 'compute_selected_troop_budget_base20', 'compute_selected_troop_budget_base30', 'select_strongest_type1_candidate', 'compute_then_reload_previous_selected_budget', 'test_actor_types_0_4_8', 'select_strongest_type2_candidate', 'compute_selected_type2_budget_base30'):
        records[owner]['effects'] += '\nsole complete first-side action fields: ' + '\n'.join((first_action_fields[name]['effects'] for name in ('_action_child_frame', '_action_child_publish', '_action_factor_add_long_fields', '_action_factor_shift_long_fields', '_action_random_factor_fields', '_action_attribute_product_fields', 'select_action_lowest_rating_fields', 'select_lowest_nonzero_rating_fields', 'compute_selected_attribute_budget_fields', '_select_first_side_terrain_action_fields', 'select_strongest_open_terrain_candidate_fields', 'select_strongest_type1_candidate_fields', 'select_strongest_type2_candidate_fields', '_compute_first_selected_troop_budget_fields', 'compute_selected_troop_budget_base20_fields', 'compute_selected_troop_budget_base30_fields', 'compute_then_reload_previous_selected_budget_fields', 'compute_selected_type2_budget_base30_fields', 'test_actor_action_terrain_gate_fields', 'test_actor_types_0_4_8_fields', 'state_mixed_action_requirement_fields', 'select_lowest_filtered_rating_fields', 'test_actor_map_relative_types_fields', 'attribute_action_requirement', 'troop_action_requirement')))
    for name in ('_action_child_frame', '_action_child_publish', '_action_factor_add_long_fields', '_action_factor_shift_long_fields', '_action_random_factor_fields', '_action_attribute_product_fields', 'select_action_lowest_rating_fields', 'select_lowest_nonzero_rating_fields', 'compute_selected_attribute_budget_fields', '_select_first_side_terrain_action_fields', 'select_strongest_open_terrain_candidate_fields', 'select_strongest_type1_candidate_fields', 'select_strongest_type2_candidate_fields', '_compute_first_selected_troop_budget_fields', 'compute_selected_troop_budget_base20_fields', 'compute_selected_troop_budget_base30_fields', 'compute_then_reload_previous_selected_budget_fields', 'compute_selected_type2_budget_base30_fields', 'test_actor_action_terrain_gate_fields', 'test_actor_types_0_4_8_fields'):
        records.pop(name)
    if selected_names is not None:
        if type(selected_names) is not tuple or selected_names != CONTACT_NATIVE_NAMES:
            raise CompileError('only the fixed complete contact native family is admitted')
        selected_bindings = tuple((binding for binding in ACTIONS_BINDINGS if binding.name in selected_names))
        if len(selected_bindings) != len(selected_names):
            raise CompileError('all selected contact whole owners are required')
        selected_lowerers = {name: LOWERERS[name] for name in selected_names}
        return lower_declared({name: records[name] for name in selected_names}, selected_bindings, selected_lowerers)
    return lower_declared(records, ACTIONS_BINDINGS, LOWERERS)


def _action_score_policy(source):
    """Consume the real unsigned LONG ranking operator, not an AST decoration."""
    if type(source) is not str:
        raise CompileError('explicit action business source text required')
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError) as error:
        raise CompileError('valid action Python required') from error
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == 'is_better_action_score']
    if len(functions) != 1:
        raise CompileError('one complete action score policy required')
    function = functions[0]
    if not function.body or not isinstance(function.body[-1], ast.Return):
        raise CompileError('action score policy needs an explicit return')
    comparison = function.body[-1].value
    failures = {ast.Lt: 'bcc', ast.LtE: 'bhi', ast.Gt: 'bls',
                ast.GtE: 'bcs', ast.Eq: 'bne', ast.NotEq: 'beq'}
    if (not isinstance(comparison, ast.Compare) or len(comparison.ops) != 1
            or len(comparison.comparators) != 1 or type(comparison.ops[0]) not in failures):
        raise CompileError('one supported unsigned action-score comparison required')
    failure = failures[type(comparison.ops[0])]
    actual = ast.dump(function, include_attributes=False)
    # Only the operator is normalized for complete structural admission.
    # Operands, validation, ABI and return all still match their real flow.
    comparison.ops = [ast.Gt()]
    return ast.unparse(tree), failure, actual


FLOW = "\"\"\"Deployment lists, terrain selection and battle-action requirements.\n\nThese are gameplay decisions and live state transitions, not damage resolution.\nOriginal fixed-width arithmetic and anomalous choices stay explicit. Resource\ndata is supplied by named readonly views; no ROM or file is opened here.\n\"\"\"\nfrom .domain import (GameState, Table, Word, Long, CarryOutcome, checked_state,\n                     uint, u16, u32, s16, low8, low16, high16,\n                     replace_byte, replace_word, negative_byte, negative_word,\n                     divu_retained)\nfrom .contexts_actions import (AnchorContext, OccupiedCellsContext,\n    EmptySlotContext, EmptySlotResult, DeploymentCellContext,\n    DeploymentEdgeContext, PromotionContext, RatingContext, RatingSelection,\n    SelectionContext, ScoredSelection, CandidateBudgetContext,\n    TerrainActorContext, checked_context)\nfrom .business_geometry import (weighted_training_factor,\n    load_battlefield_map_context, read_battlefield_terrain_type)\n\n\ndef read_city_deployment_anchor(state: GameState, retained: AnchorContext) -> tuple[Long, Long]:\n    \"\"\"Read the city's formation BYTE pair, retaining operand upper words.\"\"\"\n    state = checked_state(state)\n    retained = checked_context(retained, AnchorContext)\n    city = state.battle_scene()\n    formation = state.scene_variant.byte(city)\n    offset = u16(u16(city << 5) + u16(formation << 1))\n    x = replace_word(retained.x, state.scene_deployment_cells.byte(offset))\n    y = replace_word(retained.y, state.scene_deployment_cells.byte(offset, 1))\n    return x, y\n\n\ndef read_city_second_deployment_anchor(state: GameState, retained: AnchorContext) -> tuple[Long, Long]:\n    state = checked_state(state)\n    retained = checked_context(retained, AnchorContext)\n    offset = u16(state.battle_scene() << 2)\n    x = replace_word(retained.x, state.scene_anchor_positions.word(offset) >> 10)\n    y = replace_word(retained.y, state.scene_anchor_positions.word(offset, 2) >> 10)\n    return x, y\n\n\ndef select_lowest_nonzero_rating(state: GameState, retained: RatingContext) -> RatingSelection:\n    state = checked_state(state)\n    retained = checked_context(retained, RatingContext)\n    source = state.action_candidates.cursor()\n    rating = replace_word(retained.rating, 65535)\n    selected = replace_word(retained.selected, 65535)\n    while True:\n        member = source.next_word()\n        if negative_word(member):\n            break\n        member = member & 255\n        value = state.officer_readiness.byte(member)\n        if value != 0 and value < low8(rating):\n            rating = replace_byte(rating, value)\n            selected = replace_word(selected, member)\n    return RatingSelection(rating, selected)\n\n\ndef select_lowest_filtered_rating(state: GameState, retained: RatingContext) -> RatingSelection:\n    \"\"\"Zero ratings are eligible; an empty selection retains its old member.\"\"\"\n    state = checked_state(state)\n    retained = checked_context(retained, RatingContext)\n    source = state.filtered_action_candidates.cursor()\n    rating = replace_word(retained.rating, 65535)\n    selected = retained.selected\n    while True:\n        member = source.next_word()\n        if negative_word(member):\n            break\n        member = member & 255\n        value = state.officer_readiness.byte(member)\n        if value < low8(rating):\n            rating = replace_byte(rating, value)\n            selected = replace_word(selected, member)\n    return RatingSelection(rating, selected)\n\n\ndef compute_selected_attribute_budget(state: GameState) -> Long:\n    state = checked_state(state)\n    sample = low16(state.sample_random())\n    factor = u16(high16(u32(sample * 5)) + 8)\n    offset = u16(state.selected_officer() << 1)\n    attributes = state.officer_word_b400.word(offset)\n    attributes = u16(attributes + state.officer_word_b600.word(offset))\n    requirement = u32(factor * attributes)\n    state.set_action_amount(requirement)\n    return requirement\n\n\ndef compute_selected_attribute_budget_second_side(state: GameState) -> Long:\n    \"\"\"Read both attributes before advancing RNG, unlike the first-side body.\"\"\"\n    state = checked_state(state)\n    offset = u16(state.selected_officer() << 1)\n    attributes = state.officer_word_b400.word(offset)\n    attributes = u16(attributes + state.officer_word_b600.word(offset))\n    sample = low16(state.sample_random())\n    factor = u16(high16(u32(sample * 5)) + 8)\n    requirement = u32(factor * attributes)\n    state.set_action_amount(requirement)\n    return requirement\n\n\ndef compute_selected_troop_budget_base20(state: GameState) -> Long:\n    state = checked_state(state)\n    sample = low16(state.sample_random())\n    divisor = u16(high16(u32(sample * 10)) + 20)\n    strength = state.officer_troops.long(u16(state.selected_officer() << 2))\n    requirement = low16(divu_retained(strength, divisor))\n    state.set_action_amount(requirement)\n    return requirement\n\n\ndef compute_selected_troop_budget_base30(state: GameState) -> Long:\n    state = checked_state(state)\n    sample = low16(state.sample_random())\n    divisor = u16(high16(u32(sample * 11)) + 30)\n    strength = state.officer_troops.long(u16(state.selected_officer() << 2))\n    requirement = low16(divu_retained(strength, divisor))\n    state.set_action_amount(requirement)\n    return requirement\n\n\ndef compute_then_reload_previous_selected_budget(state: GameState) -> Long:\n    \"\"\"Preserve the original calculation followed by a read of the old budget.\"\"\"\n    state = checked_state(state)\n    sample = low16(state.sample_random())\n    divisor = u16(high16(u32(sample * 11)) + 20)\n    strength = state.officer_troops.long(u16(state.selected_officer() << 2))\n    computed = low16(divu_retained(strength, divisor))\n    previous = state.action_amount()\n    return previous\n\n\ndef compute_selected_type2_budget_base30(state: GameState) -> Long:\n    state = checked_state(state)\n    sample = low16(state.sample_random())\n    divisor = u16(high16(u32(sample * 11)) + 30)\n    strength = state.officer_troops.long(u16(state.selected_officer() << 2))\n    requirement = low16(divu_retained(strength, divisor))\n    state.set_action_amount(requirement)\n    return requirement\n\n\ndef compute_type6_budget_from_random_state(state: GameState, candidate: CandidateBudgetContext) -> Long:\n    \"\"\"The original uses the full updated RNG state twice, not just the sample.\"\"\"\n    state = checked_state(state)\n    candidate = checked_context(candidate, CandidateBudgetContext)\n    strength = state.officer_troops.long(u16(low16(candidate.selected) << 2))\n    random = state.sample_random_pair()\n    sample = low16(random.sample)\n    scaled = u32(u32(u32(sample << 2) + random.updated_state) << 1)\n    scaled = u32(scaled + random.updated_state)\n    divisor = u16(high16(scaled) + 40)\n    requirement = low16(divu_retained(strength, divisor))\n    state.set_action_amount(requirement)\n    return requirement\n\n\ndef compute_candidate_budget_base20(state: GameState, candidate: CandidateBudgetContext) -> Long:\n    state = checked_state(state)\n    candidate = checked_context(candidate, CandidateBudgetContext)\n    strength = state.officer_troops.long(u16(low16(candidate.selected) << 2))\n    sample = low16(state.sample_random())\n    divisor = u16(high16(u32(sample * 11)) + 20)\n    requirement = low16(divu_retained(strength, divisor))\n    state.set_action_amount(requirement)\n    return requirement\n\n\ndef compute_candidate_budget_base30(state: GameState, candidate: CandidateBudgetContext) -> Long:\n    state = checked_state(state)\n    candidate = checked_context(candidate, CandidateBudgetContext)\n    strength = state.officer_troops.long(u16(low16(candidate.selected) << 2))\n    sample = low16(state.sample_random())\n    divisor = u16(high16(u32(sample * 11)) + 30)\n    requirement = low16(divu_retained(strength, divisor))\n    state.set_action_amount(requirement)\n    return requirement\n\n\ndef compute_type1_candidate_budget_base20(state: GameState, candidate: CandidateBudgetContext) -> Long:\n    state = checked_state(state)\n    candidate = checked_context(candidate, CandidateBudgetContext)\n    strength = state.officer_troops.long(u16(low16(candidate.selected) << 2))\n    sample = low16(state.sample_random())\n    divisor = u16(high16(u32(sample * 11)) + 20)\n    requirement = low16(divu_retained(strength, divisor))\n    state.set_action_amount(requirement)\n    return requirement\n\n\ndef compute_type2_candidate_budget_base30(state: GameState, candidate: CandidateBudgetContext) -> Long:\n    state = checked_state(state)\n    candidate = checked_context(candidate, CandidateBudgetContext)\n    strength = state.officer_troops.long(u16(low16(candidate.selected) << 2))\n    sample = low16(state.sample_random())\n    divisor = u16(high16(u32(sample * 11)) + 30)\n    requirement = low16(divu_retained(strength, divisor))\n    state.set_action_amount(requirement)\n    return requirement\n\n\ndef append_roster_occupied_cells(state: GameState, cells: OccupiedCellsContext) -> None:\n    \"\"\"Append position BYTE pairs through live, possibly aliased cursors.\"\"\"\n    state = checked_state(state)\n    cells = checked_context(cells, OccupiedCellsContext, state)\n    while True:\n        member = cells.source.next_word()\n        if negative_word(member):\n            break\n        offset = u16(member << 2)\n        x = cells.positions.word(offset)\n        if x == 0:\n            continue\n        cells.destination.append_byte(x >> 10)\n        y = cells.positions.word(offset, 2)\n        cells.destination.append_byte(y >> 10)\n    return None\n\n\ndef build_deployment_occupied_cells(state: GameState) -> None:\n    state = checked_state(state)\n    destination = state.formation_scratch.cursor()\n    append_roster_occupied_cells(state, OccupiedCellsContext(\n        state.primary_battle_roster.cursor(), destination, state.battle_positions))\n    append_roster_occupied_cells(state, OccupiedCellsContext(\n        state.secondary_battle_roster.cursor(), destination, state.battle_positions))\n    destination.put_word(65535)\n    return None\n\n\ndef find_next_empty_position_slot(state: GameState, slots: EmptySlotContext) -> EmptySlotResult:\n    state = checked_state(state)\n    slots = checked_context(slots, EmptySlotContext, state)\n    while True:\n        member = slots.source.next_word()\n        if negative_word(member):\n            return EmptySlotResult(member, slots.source, state.carry_result(1))\n        offset = u16(member << 2)\n        if slots.positions.long(offset) == 0:\n            return EmptySlotResult(offset, slots.source, state.carry_result(0))\n\n\ndef try_place_deployment_cell(state: GameState, cell: DeploymentCellContext) -> CarryOutcome:\n    \"\"\"Reject occupied neighborhoods and original terrain kinds 1, 6, 7.\"\"\"\n    state = checked_state(state)\n    cell = checked_context(cell, DeploymentCellContext, state)\n    left = u16(cell.x - 3)\n    right = u16(cell.x + 3)\n    top = u16(cell.y - 3)\n    bottom = u16(cell.y + 3)\n    occupied = state.formation_scratch.cursor()\n    while True:\n        x = occupied.byte()\n        if negative_byte(x):\n            break\n        if s16(left) <= x <= s16(right):\n            y = occupied.byte(0, 1)\n            if s16(top) <= y <= s16(bottom):\n                return state.carry_result(0)\n        occupied.base = occupied.advance(2).base\n    terrain = read_battlefield_terrain_type(\n        state, cell.map, u16(cell.x << 3), u16(cell.y << 3), 0)\n    if low8(terrain) == 1 or low8(terrain) == 6 or low8(terrain) == 7:\n        return state.carry_result(0)\n    cell.positions.set_word(cell.offset, u16(u16(cell.x << 3) << 7))\n    cell.positions.set_word(cell.offset, u16(u16(cell.y << 3) << 7), 2)\n    return state.carry_result(1)\n\n\ndef scan_deployment_first_edge(state: GameState, edge: DeploymentEdgeContext) -> EmptySlotResult:\n    state = checked_state(state)\n    edge = checked_context(edge, DeploymentEdgeContext, state)\n    x = u16(edge.center_x - edge.radius)\n    offset = edge.offset\n    if x < 3 or x > 25:\n        return EmptySlotResult(offset, edge.source, state.carry_result(0))\n    delta = u16(-edge.radius)\n    while True:\n        y = u16(edge.center_y + delta)\n        if 3 <= y <= 37:\n            outcome = try_place_deployment_cell(state, DeploymentCellContext(\n                edge.map, edge.positions, offset, x, y))\n            if outcome.carry != 0:\n                vacancy = find_next_empty_position_slot(state, EmptySlotContext(\n                    edge.source, edge.positions))\n                offset = vacancy.offset\n                if vacancy.outcome.carry != 0:\n                    return EmptySlotResult(offset, edge.source, state.carry_result(1))\n        delta = u16(delta + 2)\n        if s16(delta) > s16(edge.radius):\n            break\n    return EmptySlotResult(offset, edge.source, state.carry_result(0))\n\n\ndef scan_deployment_second_edge(state: GameState, edge: DeploymentEdgeContext) -> EmptySlotResult:\n    state = checked_state(state)\n    edge = checked_context(edge, DeploymentEdgeContext, state)\n    y = u16(edge.center_y - edge.radius)\n    offset = edge.offset\n    if y < 3 or y > 37:\n        return EmptySlotResult(offset, edge.source, state.carry_result(0))\n    delta = u16(-u16(edge.radius - 2))\n    while True:\n        x = u16(edge.center_x + delta)\n        if 3 <= x <= 25:\n            outcome = try_place_deployment_cell(state, DeploymentCellContext(\n                edge.map, edge.positions, offset, x, y))\n            if outcome.carry != 0:\n                vacancy = find_next_empty_position_slot(state, EmptySlotContext(\n                    edge.source, edge.positions))\n                offset = vacancy.offset\n                if vacancy.outcome.carry != 0:\n                    return EmptySlotResult(offset, edge.source, state.carry_result(1))\n        delta = u16(delta + 2)\n        if s16(delta) >= s16(edge.radius):\n            break\n    return EmptySlotResult(offset, edge.source, state.carry_result(0))\n\n\ndef promote_first_roster_deployment_candidate(state: GameState, retained: PromotionContext) -> None:\n    \"\"\"Preserve the original live forward overlap, not list.insert/memmove.\"\"\"\n    state = checked_state(state)\n    retained = checked_context(retained, PromotionContext)\n    member = state.force_rulers.word(u16(state.battle_primary_force() << 1))\n    scene = state.battle_scene()\n    previous = u16((scene & 65280) | state.scene_primary_head.byte(scene))\n    if previous == member:\n        return None\n    source = state.primary_battle_roster.cursor()\n    while True:\n        item = source.next_word()\n        if negative_word(item):\n            return None\n        if item & 255 == member:\n            break\n    state.deployed_flags.set_byte(member, 1)\n    scene = state.battle_scene()\n    formation = replace_byte(retained.formation_carrier, state.scene_variant.byte(scene))\n    cell = u16(u16(scene << 5) + u16(low16(formation) << 1))\n    member_offset = u16(member << 2)\n    x = u16(state.scene_deployment_cells.byte(cell) << 3)\n    state.global_battle_positions.set_word(member_offset, x)\n    y = u16(state.scene_deployment_cells.byte(cell, 1) << 3)\n    state.global_battle_positions.set_word(member_offset, y, 2)\n    previous_offset = u16(previous << 2)\n    x = u16(u16(state.scene_deployment_cells.byte(cell) << 3) << 7)\n    previous_x = state.battle_positions.word(previous_offset)\n    x_difference = u16(x - previous_x)\n    if x < previous_x:\n        x_difference = u16(-x_difference)\n    if x_difference <= 1024:\n        y = u16(u16(state.scene_deployment_cells.byte(cell, 1) << 3) << 7)\n        previous_y = state.battle_positions.word(previous_offset, 2)\n        y_difference = u16(y - previous_y)\n        if y < previous_y:\n            y_difference = u16(-y_difference)\n        if y_difference < 1024:\n            x = state.battle_positions.word(member_offset) >> 7\n            state.global_battle_positions.set_word(previous_offset, x)\n            y = state.battle_positions.word(member_offset, 2) >> 7\n            state.global_battle_positions.set_word(previous_offset, y, 2)\n            previous = previous_offset >> 2\n            state.deployed_flags.set_byte(previous, 1)\n    member = member_offset >> 2\n    source = state.primary_battle_roster.cursor()\n    destination = state.primary_battle_roster.cursor(2)\n    while True:\n        item = source.next_word()\n        if negative_word(item):\n            break\n        if item == member:\n            continue\n        destination.append_word(item)\n    state.primary_battle_roster.set_word(0, member)\n    state.scene_primary_head.set_byte(state.battle_scene(), low8(member))\n    return None\n\n\ndef promote_second_roster_deployment_candidate(state: GameState) -> None:\n    \"\"\"The original continues to use the candidate's four-byte index as its ID.\"\"\"\n    state = checked_state(state)\n    member = state.force_rulers.word(u16(state.battle_secondary_force() << 1))\n    previous = state.city_head_words.word(u16(state.battle_scene() << 1))\n    if previous == member:\n        return None\n    source = state.secondary_battle_roster.cursor()\n    while True:\n        item = source.next_word()\n        if negative_word(item):\n            return None\n        if item & 255 == member:\n            break\n    state.deployed_flags.set_byte(member, 1)\n    scene = state.battle_scene()\n    cell = u16(scene * 58)\n    member = u16(member << 2)\n    x = u16(u16(state.preceding_secondary_position_catalog.byte(cell) << 3) << 7)\n    state.global_battle_positions.set_word(member, x)\n    y = u16(u16(state.preceding_secondary_position_catalog.byte(cell, 1) << 3) << 7)\n    state.global_battle_positions.set_word(member, y, 2)\n    source = state.secondary_battle_roster.cursor()\n    destination = state.secondary_battle_roster.cursor(2)\n    while True:\n        item = source.next_word()\n        if negative_word(item):\n            break\n        item = item & 255\n        if item == member:\n            continue\n        destination.append_word(item)\n    state.secondary_battle_roster.set_word(0, member)\n    state.city_head_words.set_word(u16(state.battle_scene() << 1), member)\n    return None\n\n\ndef test_actor_types_0_4_8(state: GameState, actor: TerrainActorContext) -> CarryOutcome:\n    state = checked_state(state)\n    actor = checked_context(actor, TerrainActorContext)\n    map_context = load_battlefield_map_context(state)\n    offset = u16(low16(actor.actor) << 2)\n    x = state.battle_positions.word(offset) >> 7\n    y = state.battle_positions.word(offset, 2) >> 7\n    terrain = read_battlefield_terrain_type(state, map_context, x, y, actor.terrain_carrier)\n    if low8(terrain) == 0 or low8(terrain) == 4 or low8(terrain) == 8:\n        return state.carry_result(1)\n    return state.carry_result(0)\n\n\ndef test_actor_map_relative_types(state: GameState, actor: TerrainActorContext) -> CarryOutcome:\n    \"\"\"Read coordinates relative to the map base, preserving the original alias.\"\"\"\n    state = checked_state(state)\n    actor = checked_context(actor, TerrainActorContext)\n    map_context = load_battlefield_map_context(state)\n    offset = u16(low16(actor.actor) << 2)\n    x = map_context.word(offset) >> 7\n    y = map_context.word(offset, 2) >> 7\n    terrain = read_battlefield_terrain_type(state, map_context, x, y, actor.terrain_carrier)\n    if low8(terrain) == 0 or low8(terrain) == 4 or low8(terrain) == 7:\n        return state.carry_result(0)\n    return state.carry_result(1)\n\n\ndef build_non_type6_candidates(state: GameState, retained: SelectionContext) -> Table:\n    state = checked_state(state)\n    retained = checked_context(retained, SelectionContext)\n    map_context = load_battlefield_map_context(state)\n    source = state.action_candidates.cursor()\n    destination = state.filtered_action_candidates.cursor()\n    while True:\n        member = source.next_word()\n        if negative_word(member):\n            break\n        member = member & 255\n        offset = u16(member << 2)\n        x = state.battle_positions.word(offset) >> 7\n        y = state.battle_positions.word(offset, 2) >> 7\n        terrain = read_battlefield_terrain_type(state, map_context, x, y, retained.terrain_carrier)\n        if low8(terrain) != 6:\n            destination.append_word(member)\n    destination.put_word(65535)\n    return map_context\n\n\ndef select_strongest_open_terrain_candidate(state: GameState, retained: SelectionContext) -> ScoredSelection:\n    state = checked_state(state)\n    retained = checked_context(retained, SelectionContext)\n    map_context = load_battlefield_map_context(state)\n    source = state.action_candidates.cursor()\n    strongest = 0\n    selected = replace_word(retained.selected, 65535)\n    while True:\n        member = source.next_word()\n        if negative_word(member):\n            break\n        member = member & 255\n        offset = u16(member << 2)\n        x = state.battle_positions.word(offset) >> 7\n        y = state.battle_positions.word(offset, 2) >> 7\n        terrain = read_battlefield_terrain_type(state, map_context, x, y, retained.terrain_carrier)\n        if low8(terrain) != 0 and low8(terrain) != 3 and low8(terrain) != 7 and low8(terrain) != 1:\n            continue\n        training = low16(weighted_training_factor(state, member))\n        score = u32(training * state.officer_troops.word(offset, 2))\n        if score > strongest:\n            strongest = score\n            selected = replace_word(selected, member)\n    return ScoredSelection(strongest, selected, map_context)\n\n\ndef select_strongest_type1_candidate(state: GameState, retained: SelectionContext) -> ScoredSelection:\n    state = checked_state(state)\n    retained = checked_context(retained, SelectionContext)\n    map_context = load_battlefield_map_context(state)\n    source = state.action_candidates.cursor()\n    strongest = 0\n    selected = replace_word(retained.selected, 65535)\n    while True:\n        member = source.next_word()\n        if negative_word(member):\n            break\n        member = member & 255\n        offset = u16(member << 2)\n        x = state.battle_positions.word(offset) >> 7\n        y = state.battle_positions.word(offset, 2) >> 7\n        terrain = read_battlefield_terrain_type(state, map_context, x, y, retained.terrain_carrier)\n        if low8(terrain) != 1:\n            continue\n        training = low16(weighted_training_factor(state, member))\n        score = u32(training * state.officer_troops.word(offset, 2))\n        if score > strongest:\n            strongest = score\n            selected = replace_word(selected, member)\n    return ScoredSelection(strongest, selected, map_context)\n\n\ndef select_strongest_type2_candidate(state: GameState, retained: SelectionContext) -> ScoredSelection:\n    state = checked_state(state)\n    retained = checked_context(retained, SelectionContext)\n    map_context = load_battlefield_map_context(state)\n    source = state.action_candidates.cursor()\n    strongest = 0\n    selected = replace_word(retained.selected, 65535)\n    while True:\n        member = source.next_word()\n        if negative_word(member):\n            break\n        member = member & 255\n        offset = u16(member << 2)\n        x = state.battle_positions.word(offset) >> 7\n        y = state.battle_positions.word(offset, 2) >> 7\n        terrain = read_battlefield_terrain_type(state, map_context, x, y, retained.terrain_carrier)\n        if low8(terrain) != 2:\n            continue\n        training = low16(weighted_training_factor(state, member))\n        score = u32(training * state.officer_troops.word(offset, 2))\n        if score > strongest:\n            strongest = score\n            selected = replace_word(selected, member)\n    return ScoredSelection(strongest, selected, map_context)\n\n\ndef select_strongest_type6_candidate(state: GameState, retained: SelectionContext) -> ScoredSelection:\n    state = checked_state(state)\n    retained = checked_context(retained, SelectionContext)\n    map_context = load_battlefield_map_context(state)\n    source = state.action_candidates.cursor()\n    strongest = 0\n    selected = replace_word(retained.selected, 65535)\n    while True:\n        member = source.next_word()\n        if negative_word(member):\n            break\n        member = member & 255\n        offset = u16(member << 2)\n        x = state.battle_positions.word(offset) >> 7\n        y = state.battle_positions.word(offset, 2) >> 7\n        terrain = read_battlefield_terrain_type(state, map_context, x, y, retained.terrain_carrier)\n        if low8(terrain) != 6:\n            continue\n        training = low16(weighted_training_factor(state, member))\n        score = u32(training * state.officer_troops.word(offset, 2))\n        if score > strongest:\n            strongest = score\n            selected = replace_word(selected, member)\n    return ScoredSelection(strongest, selected, map_context)\n\n\ndef select_strongest_open_terrain_candidate_second_side(state: GameState, retained: SelectionContext) -> ScoredSelection:\n    state = checked_state(state)\n    retained = checked_context(retained, SelectionContext)\n    map_context = load_battlefield_map_context(state)\n    source = state.action_candidates.cursor()\n    strongest = 0\n    selected = replace_word(retained.selected, 65535)\n    while True:\n        member = source.next_word()\n        if negative_word(member):\n            break\n        member = member & 255\n        offset = u16(member << 2)\n        x = state.battle_positions.word(offset) >> 7\n        y = state.battle_positions.word(offset, 2) >> 7\n        terrain = read_battlefield_terrain_type(state, map_context, x, y, retained.terrain_carrier)\n        if low8(terrain) != 0 and low8(terrain) != 3 and low8(terrain) != 7 and low8(terrain) != 1:\n            continue\n        training = low16(weighted_training_factor(state, member))\n        score = u32(training * state.officer_troops.word(offset, 2))\n        if score > strongest:\n            strongest = score\n            selected = replace_word(selected, member)\n    return ScoredSelection(strongest, selected, map_context)\n\n\ndef select_strongest_type1_candidate_second_side(state: GameState, retained: SelectionContext) -> ScoredSelection:\n    state = checked_state(state)\n    retained = checked_context(retained, SelectionContext)\n    map_context = load_battlefield_map_context(state)\n    source = state.action_candidates.cursor()\n    strongest = 0\n    selected = replace_word(retained.selected, 65535)\n    while True:\n        member = source.next_word()\n        if negative_word(member):\n            break\n        member = member & 255\n        offset = u16(member << 2)\n        x = state.battle_positions.word(offset) >> 7\n        y = state.battle_positions.word(offset, 2) >> 7\n        terrain = read_battlefield_terrain_type(state, map_context, x, y, retained.terrain_carrier)\n        if low8(terrain) != 1:\n            continue\n        training = low16(weighted_training_factor(state, member))\n        score = u32(training * state.officer_troops.word(offset, 2))\n        if score > strongest:\n            strongest = score\n            selected = replace_word(selected, member)\n    return ScoredSelection(strongest, selected, map_context)\n\n\ndef select_strongest_type2_candidate_with_map_context(state: GameState, retained: SelectionContext, map_context: Table) -> ScoredSelection:\n    state = checked_state(state)\n    retained = checked_context(retained, SelectionContext)\n    map_context = state.checked_table(map_context)\n    source = state.action_candidates.cursor()\n    strongest = 0\n    selected = replace_word(retained.selected, 65535)\n    while True:\n        member = source.next_word()\n        if negative_word(member):\n            break\n        member = member & 255\n        offset = u16(member << 2)\n        x = state.battle_positions.word(offset) >> 7\n        y = state.battle_positions.word(offset, 2) >> 7\n        terrain = read_battlefield_terrain_type(state, map_context, x, y, retained.terrain_carrier)\n        if low8(terrain) != 2:\n            continue\n        training = low16(weighted_training_factor(state, member))\n        score = u32(training * state.officer_troops.word(offset, 2))\n        if score > strongest:\n            strongest = score\n            selected = replace_word(selected, member)\n    return ScoredSelection(strongest, selected, map_context)\n"

SLOTS = {
    'compute_selected_attribute_budget': {8: ('base', 1, 8)},
    'compute_selected_attribute_budget_second_side': {8: ('base', 1, 8)},
    'compute_selected_troop_budget_base20': {20: ('base', 1, 65535)},
    'compute_selected_troop_budget_base30': {30: ('base', 1, 65535)},
    'compute_then_reload_previous_selected_budget': {20: ('base', 1, 65535)},
    'compute_selected_type2_budget_base30': {30: ('base', 1, 65535)},
    'compute_type6_budget_from_random_state': {40: ('base', 1, 65535)},
    'compute_candidate_budget_base20': {20: ('base', 1, 65535)},
    'compute_candidate_budget_base30': {30: ('base', 1, 65535)},
    'compute_type1_candidate_budget_base20': {20: ('base', 1, 65535)},
    'compute_type2_candidate_budget_base30': {30: ('base', 1, 65535)},
}


def _semantic_declarations():
    tree = ast.parse(FLOW)
    approved, declarations = {}, {}
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            approved.setdefault(node.module, set()).update(item.name for item in node.names)
        elif isinstance(node, ast.FunctionDef):
            body = list(node.body)
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and type(body[0].value.value) is str:
                body = body[1:]
            declarations[node.name] = dict(signature=ast.unparse(node.args),
                returns=ast.unparse(node.returns),
                flow='\n'.join(ast.unparse(statement) for statement in body),
                slots=SLOTS.get(node.name, {}))
    return declarations, approved


DECLARATIONS, APPROVED = _semantic_declarations()

DOMAIN_HELPERS = ('read_selected_action_attributes', 'attribute_action_requirement', 'read_selected_action_troops', 'read_candidate_action_troops', 'troop_action_requirement', 'state_mixed_action_requirement', 'commit_action_requirement', 'action_terrain_is_eligible', 'is_better_action_score', 'observe_action_candidate', 'read_action_candidate_score', 'select_action_candidate_by_terrain')
DOMAIN_ENTRIES = ('compute_selected_attribute_budget', 'compute_selected_attribute_budget_second_side', 'compute_selected_troop_budget_base20', 'compute_selected_troop_budget_base30', 'compute_then_reload_previous_selected_budget', 'compute_selected_type2_budget_base30', 'compute_type6_budget_from_random_state', 'compute_candidate_budget_base20', 'compute_candidate_budget_base30', 'compute_type1_candidate_budget_base20', 'compute_type2_candidate_budget_base30', 'select_strongest_open_terrain_candidate', 'select_strongest_type1_candidate', 'select_strongest_type2_candidate', 'select_strongest_type6_candidate', 'select_strongest_open_terrain_candidate_second_side', 'select_strongest_type1_candidate_second_side', 'select_strongest_type2_candidate_with_map_context')
SCORE_SELECTIONS = tuple(name for name in DOMAIN_ENTRIES if name.startswith('select_strongest_'))
DOMAIN_DECLARATIONS = {'read_selected_action_attributes': {'signature': 'state: GameState', 'returns': 'Word', 'flow': 'state = checked_state(state)\noffset = u16(state.selected_officer() << 1)\nattributes = state.officer_word_b400.word(offset)\nreturn u16(attributes + state.officer_word_b600.word(offset))'}, 'attribute_action_requirement': {'signature': 'sample: Word, attributes: Word, base: Word', 'returns': 'Long', 'flow': 'uint(sample, 16)\nuint(attributes, 16)\nuint(base, 16)\nfactor = u16(high16(u32(sample * 5)) + base)\nreturn u32(factor * attributes)'}, 'read_selected_action_troops': {'signature': 'state: GameState', 'returns': 'Long', 'flow': 'state = checked_state(state)\nreturn state.officer_troops.long(u16(state.selected_officer() << 2))'}, 'read_candidate_action_troops': {'signature': 'state: GameState, candidate: CandidateBudgetContext', 'returns': 'Long', 'flow': 'state = checked_state(state)\ncandidate = checked_context(candidate, CandidateBudgetContext)\nreturn state.officer_troops.long(u16(low16(candidate.selected) << 2))'}, 'troop_action_requirement': {'signature': 'sample: Word, strength: Long, multiplier: Word, base: Word', 'returns': 'Long', 'flow': 'uint(sample, 16)\nuint(strength, 32)\nuint(multiplier, 16)\nuint(base, 16)\ndivisor = u16(high16(u32(sample * multiplier)) + base)\nreturn low16(divu_retained(strength, divisor))'}, 'state_mixed_action_requirement': {'signature': 'draw: ActionRandomDraw, strength: Long, base: Word', 'returns': 'Long', 'flow': "if type(draw) is not ActionRandomDraw:\n    raise ValueError('typed action random draw required')\nuint(strength, 32)\nuint(base, 16)\nscaled = u32(u32(u32(draw.sample << 2) + draw.updated_state) << 1)\nscaled = u32(scaled + draw.updated_state)\ndivisor = u16(high16(scaled) + base)\nreturn low16(divu_retained(strength, divisor))"}, 'commit_action_requirement': {'signature': 'state: GameState, requirement: Long', 'returns': 'Long', 'flow': 'state = checked_state(state)\nuint(requirement, 32)\nstate.set_action_amount(requirement)\nreturn requirement'}, 'compute_selected_attribute_budget': {'signature': 'state: GameState', 'returns': 'Long', 'flow': 'state = checked_state(state)\nsample = low16(state.sample_random())\nattributes = read_selected_action_attributes(state)\nreturn commit_action_requirement(state, attribute_action_requirement(sample, attributes, 8))', 'slots': {8: ('base', 1, 8)}}, 'compute_selected_attribute_budget_second_side': {'signature': 'state: GameState', 'returns': 'Long', 'flow': 'state = checked_state(state)\nattributes = read_selected_action_attributes(state)\nsample = low16(state.sample_random())\nreturn commit_action_requirement(state, attribute_action_requirement(sample, attributes, 8))', 'slots': {8: ('base', 1, 8)}}, 'compute_selected_troop_budget_base20': {'signature': 'state: GameState', 'returns': 'Long', 'flow': 'state = checked_state(state)\nsample = low16(state.sample_random())\nstrength = read_selected_action_troops(state)\nreturn commit_action_requirement(state, troop_action_requirement(sample, strength, 10, 20))', 'slots': {20: ('base', 1, 65535)}}, 'compute_selected_troop_budget_base30': {'signature': 'state: GameState', 'returns': 'Long', 'flow': 'state = checked_state(state)\nsample = low16(state.sample_random())\nstrength = read_selected_action_troops(state)\nreturn commit_action_requirement(state, troop_action_requirement(sample, strength, 11, 30))', 'slots': {30: ('base', 1, 65535)}}, 'compute_then_reload_previous_selected_budget': {'signature': 'state: GameState', 'returns': 'Long', 'flow': 'state = checked_state(state)\nsample = low16(state.sample_random())\nstrength = read_selected_action_troops(state)\ncomputed = troop_action_requirement(sample, strength, 11, 20)\nprevious = state.action_amount()\nreturn previous', 'slots': {20: ('base', 1, 65535)}}, 'compute_selected_type2_budget_base30': {'signature': 'state: GameState', 'returns': 'Long', 'flow': 'state = checked_state(state)\nsample = low16(state.sample_random())\nstrength = read_selected_action_troops(state)\nreturn commit_action_requirement(state, troop_action_requirement(sample, strength, 11, 30))', 'slots': {30: ('base', 1, 65535)}}, 'compute_type6_budget_from_random_state': {'signature': 'state: GameState, candidate: CandidateBudgetContext', 'returns': 'Long', 'flow': 'state = checked_state(state)\ncandidate = checked_context(candidate, CandidateBudgetContext)\nstrength = read_candidate_action_troops(state, candidate)\nrandom = state.sample_random_pair()\ndraw = ActionRandomDraw(low16(random.sample), random.updated_state)\nreturn commit_action_requirement(state, state_mixed_action_requirement(draw, strength, 40))', 'slots': {40: ('base', 1, 65535)}}, 'compute_candidate_budget_base20': {'signature': 'state: GameState, candidate: CandidateBudgetContext', 'returns': 'Long', 'flow': 'state = checked_state(state)\ncandidate = checked_context(candidate, CandidateBudgetContext)\nstrength = read_candidate_action_troops(state, candidate)\nsample = low16(state.sample_random())\nreturn commit_action_requirement(state, troop_action_requirement(sample, strength, 11, 20))', 'slots': {20: ('base', 1, 65535)}}, 'compute_candidate_budget_base30': {'signature': 'state: GameState, candidate: CandidateBudgetContext', 'returns': 'Long', 'flow': 'state = checked_state(state)\ncandidate = checked_context(candidate, CandidateBudgetContext)\nstrength = read_candidate_action_troops(state, candidate)\nsample = low16(state.sample_random())\nreturn commit_action_requirement(state, troop_action_requirement(sample, strength, 11, 30))', 'slots': {30: ('base', 1, 65535)}}, 'compute_type1_candidate_budget_base20': {'signature': 'state: GameState, candidate: CandidateBudgetContext', 'returns': 'Long', 'flow': 'state = checked_state(state)\ncandidate = checked_context(candidate, CandidateBudgetContext)\nstrength = read_candidate_action_troops(state, candidate)\nsample = low16(state.sample_random())\nreturn commit_action_requirement(state, troop_action_requirement(sample, strength, 11, 20))', 'slots': {20: ('base', 1, 65535)}}, 'compute_type2_candidate_budget_base30': {'signature': 'state: GameState, candidate: CandidateBudgetContext', 'returns': 'Long', 'flow': 'state = checked_state(state)\ncandidate = checked_context(candidate, CandidateBudgetContext)\nstrength = read_candidate_action_troops(state, candidate)\nsample = low16(state.sample_random())\nreturn commit_action_requirement(state, troop_action_requirement(sample, strength, 11, 30))', 'slots': {30: ('base', 1, 65535)}}, 'action_terrain_is_eligible': {'signature': 'terrain: Long, policy: ActionTerrainPolicy', 'returns': 'bool', 'flow': "uint(terrain, 32)\nif type(policy) is not ActionTerrainPolicy:\n    raise ValueError('typed action terrain policy required')\nreturn low8(terrain) in policy.kinds"}, 'is_better_action_score': {'signature': 'score: Long, strongest: Long', 'returns': 'bool', 'flow': 'uint(score, 32)\nuint(strongest, 32)\nreturn score > strongest'}, 'observe_action_candidate': {'signature': 'state: GameState, map_context: Table, member: Word, retained_terrain: Long', 'returns': 'ActionCandidate', 'flow': 'state = checked_state(state)\nmap_context = state.checked_table(map_context)\nuint(member, 16)\nuint(retained_terrain, 32)\nmember = u16(member & 255)\noffset = u16(member << 2)\nx = state.battle_positions.word(offset) >> 7\ny = state.battle_positions.word(offset, 2) >> 7\nterrain = read_battlefield_terrain_type(state, map_context, x, y, retained_terrain)\nreturn ActionCandidate(member, offset, terrain)'}, 'read_action_candidate_score': {'signature': 'state: GameState, candidate: ActionCandidate', 'returns': 'Long', 'flow': 'state = checked_state(state)\ncandidate = checked_context(candidate, ActionCandidate)\ntraining = low16(weighted_training_factor(state, candidate.member))\nreturn u32(training * state.officer_troops.word(candidate.offset, 2))'}, 'select_action_candidate_by_terrain': {'signature': 'state: GameState, retained: SelectionContext, map_context: Table, policy: ActionTerrainPolicy', 'returns': 'ScoredSelection', 'flow': "state = checked_state(state)\nretained = checked_context(retained, SelectionContext)\nmap_context = state.checked_table(map_context)\nif type(policy) is not ActionTerrainPolicy:\n    raise ValueError('typed action terrain policy required')\nsource = state.action_candidates.cursor()\nstrongest = u32(0)\nselected = replace_word(retained.selected, 65535)\nwhile True:\n    member = source.next_word()\n    if negative_word(member):\n        break\n    candidate = observe_action_candidate(state, map_context, member, retained.terrain_carrier)\n    if not action_terrain_is_eligible(candidate.terrain, policy):\n        continue\n    score = read_action_candidate_score(state, candidate)\n    if is_better_action_score(score, strongest):\n        strongest = score\n        selected = replace_word(selected, candidate.member)\nreturn ScoredSelection(strongest, selected, map_context)"}, 'select_strongest_open_terrain_candidate': {'signature': 'state: GameState, retained: SelectionContext', 'returns': 'ScoredSelection', 'flow': 'state = checked_state(state)\nretained = checked_context(retained, SelectionContext)\nmap_context = load_battlefield_map_context(state)\nreturn select_action_candidate_by_terrain(state, retained, map_context, ActionTerrainPolicy((0, 3, 7, 1)))'}, 'select_strongest_type1_candidate': {'signature': 'state: GameState, retained: SelectionContext', 'returns': 'ScoredSelection', 'flow': 'state = checked_state(state)\nretained = checked_context(retained, SelectionContext)\nmap_context = load_battlefield_map_context(state)\nreturn select_action_candidate_by_terrain(state, retained, map_context, ActionTerrainPolicy((1,)))'}, 'select_strongest_type2_candidate': {'signature': 'state: GameState, retained: SelectionContext', 'returns': 'ScoredSelection', 'flow': 'state = checked_state(state)\nretained = checked_context(retained, SelectionContext)\nmap_context = load_battlefield_map_context(state)\nreturn select_action_candidate_by_terrain(state, retained, map_context, ActionTerrainPolicy((2,)))'}, 'select_strongest_type6_candidate': {'signature': 'state: GameState, retained: SelectionContext', 'returns': 'ScoredSelection', 'flow': 'state = checked_state(state)\nretained = checked_context(retained, SelectionContext)\nmap_context = load_battlefield_map_context(state)\nreturn select_action_candidate_by_terrain(state, retained, map_context, ActionTerrainPolicy((6,)))'}, 'select_strongest_open_terrain_candidate_second_side': {'signature': 'state: GameState, retained: SelectionContext', 'returns': 'ScoredSelection', 'flow': 'state = checked_state(state)\nretained = checked_context(retained, SelectionContext)\nmap_context = load_battlefield_map_context(state)\nreturn select_action_candidate_by_terrain(state, retained, map_context, ActionTerrainPolicy((0, 3, 7, 1)))'}, 'select_strongest_type1_candidate_second_side': {'signature': 'state: GameState, retained: SelectionContext', 'returns': 'ScoredSelection', 'flow': 'state = checked_state(state)\nretained = checked_context(retained, SelectionContext)\nmap_context = load_battlefield_map_context(state)\nreturn select_action_candidate_by_terrain(state, retained, map_context, ActionTerrainPolicy((1,)))'}, 'select_strongest_type2_candidate_with_map_context': {'signature': 'state: GameState, retained: SelectionContext, map_context: Table', 'returns': 'ScoredSelection', 'flow': 'state = checked_state(state)\nretained = checked_context(retained, SelectionContext)\nmap_context = state.checked_table(map_context)\nreturn select_action_candidate_by_terrain(state, retained, map_context, ActionTerrainPolicy((2,)))'}}
APPROVED['contexts_actions'].update({'ActionTerrainPolicy', 'ActionCandidate', 'ActionRandomDraw'})


# Exact legacy projection and its single supplied field algorithm.
DOMAIN_DECLARATIONS.update({'read_city_deployment_anchor': {'signature': 'state: GameState, retained: AnchorContext', 'returns': 'tuple[Long, Long]', 'flow': 'state = checked_state(state)\nretained = checked_context(retained, AnchorContext)\nfields = read_city_deployment_anchor_fields(BattlePolicyMemory(state), retained, None)\nreturn (fields.x, fields.y)'}, 'read_city_deployment_anchor_fields': {'signature': 'memory: BattlePolicyMemory, retained: AnchorContext, retained_index: Long | None', 'returns': 'DeploymentAnchorFields', 'flow': "if type(memory) is not BattlePolicyMemory:\n    raise ValueError('typed live deployment-anchor memory required')\nretained = checked_context(retained, AnchorContext)\nif retained_index is not None:\n    uint(retained_index, 32)\ncity = memory.battle_scene()\nformation = memory.scene_variants.byte(city)\ncity_offset = u16(city << 5)\nvariant_offset = u16(formation << 1)\nwide_offset = city_offset + variant_offset\noffset = u16(wide_offset)\nindex = None if retained_index is None else replace_word(retained_index, offset)\ncells = memory.deployment_cells\nx_byte = cells.byte(offset)\nx = replace_word(retained.x, x_byte)\ny_byte = cells.byte(offset, 1)\ny = replace_word(retained.y, y_byte)\nreturn DeploymentAnchorFields(x, y, index, cells, y_byte == 0, y_byte & 128 != 0, wide_offset > 65535)"}})
APPROVED['contexts_policy_memory'] = {'BattlePolicyMemory', 'DeploymentAnchorFields'}


# Sole deployment field cores and exact complete source effects.
DOMAIN_DECLARATIONS.update({'_append_occupied_deployment_call': {'signature': 'memory: BattlePolicyMemory, fields: DeploymentOccupiedFields, continuation: Long', 'returns': 'DeploymentOccupiedFields', 'flow': 'uint(continuation, 32)\nif fields.stack_cursor is None:\n    return append_roster_occupied_cell_fields(memory, fields)\nstack = fields.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = DeploymentOccupiedFields(fields.member, fields.coordinate, fields.destination, fields.source, fields.positions, fields.extend, stack)\nresult = append_roster_occupied_cell_fields(memory, entered)\nactual = result.stack_cursor.long()\nif actual != continuation:\n    changed_deployment_return(memory, actual)\nreturn DeploymentOccupiedFields(result.member, result.coordinate, result.destination, result.source, result.positions, result.extend, result.stack_cursor.advance(4))'}, 'append_roster_occupied_cell_fields': {'signature': 'memory: BattlePolicyMemory, fields: DeploymentOccupiedFields', 'returns': 'DeploymentOccupiedFields', 'flow': "if type(memory) is not BattlePolicyMemory or type(fields) is not DeploymentOccupiedFields:\n    raise ValueError('typed same-state occupied fields required')\nfields.validate(memory.state)\nmember_carrier = fields.member\ncoordinate_carrier = fields.coordinate\nextend = fields.extend\nwhile True:\n    member = fields.source.next_word()\n    member_carrier = None if member_carrier is None else replace_word(member_carrier, member)\n    if negative_word(member):\n        break\n    offset = u16(member << 2)\n    member_carrier = None if member_carrier is None else replace_word(member_carrier, offset)\n    extend = member & 16384 != 0\n    x = fields.positions.word(offset)\n    coordinate_carrier = None if coordinate_carrier is None else replace_word(coordinate_carrier, x)\n    if x == 0:\n        continue\n    original_x = x\n    x = x >> 7 >> 3\n    coordinate_carrier = None if coordinate_carrier is None else replace_word(coordinate_carrier, x)\n    extend = original_x & 512 != 0\n    fields.destination.append_byte(x)\n    y = fields.positions.word(offset, 2)\n    coordinate_carrier = None if coordinate_carrier is None else replace_word(coordinate_carrier, y)\n    original_y = y\n    y = y >> 7 >> 3\n    coordinate_carrier = None if coordinate_carrier is None else replace_word(coordinate_carrier, y)\n    extend = original_y & 512 != 0\n    fields.destination.append_byte(y)\nreturn DeploymentOccupiedFields(member_carrier, coordinate_carrier, fields.destination, fields.source, fields.positions, extend, fields.stack_cursor).validate(memory.state)"}, 'append_roster_occupied_cells': {'signature': 'state: GameState, cells: OccupiedCellsContext', 'returns': 'None', 'flow': 'state = checked_state(state)\ncells = checked_context(cells, OccupiedCellsContext, state)\nappend_roster_occupied_cell_fields(BattlePolicyMemory(state), DeploymentOccupiedFields(None, None, cells.destination, cells.source, cells.positions, None, None))\nreturn None'}, 'build_deployment_occupied_cell_fields': {'signature': 'memory: BattlePolicyMemory, retained_member: Long | None, retained_coordinate: Long | None, retained_extend: bool | None, stack_cursor', 'returns': 'DeploymentOccupiedFields', 'flow': "if type(memory) is not BattlePolicyMemory:\n    raise ValueError('typed same-state occupied memory required')\npositions = memory.state.table(4294943056)\ndestination = memory.state.table(4294955776).cursor()\nsource = memory.state.table(4294944080).cursor()\nfields = DeploymentOccupiedFields(retained_member, retained_coordinate, destination, source, positions, retained_extend, stack_cursor).validate(memory.state)\nfields = _append_occupied_deployment_call(memory, fields, 154682)\nsource = memory.state.table(4294944164).cursor()\nfields = DeploymentOccupiedFields(fields.member, fields.coordinate, fields.destination, source, fields.positions, fields.extend, fields.stack_cursor)\nfields = _append_occupied_deployment_call(memory, fields, 154690)\nfields.destination.put_word(65535)\nreturn fields"}, 'build_deployment_occupied_cells': {'signature': 'state: GameState', 'returns': 'None', 'flow': 'state = checked_state(state)\nbuild_deployment_occupied_cell_fields(BattlePolicyMemory(state), None, None, None, None)\nreturn None'}, 'deployment_edge_coordinate_allowed': {'signature': 'coordinate: Word, maximum: Word', 'returns': 'bool', 'flow': 'uint(coordinate, 16)\nuint(maximum, 16)\nreturn 3 <= coordinate <= maximum'}, 'find_next_empty_position_slot': {'signature': 'state: GameState, slots: EmptySlotContext', 'returns': 'EmptySlotResult', 'flow': 'state = checked_state(state)\nslots = checked_context(slots, EmptySlotContext, state)\nfields = find_next_empty_position_slot_fields(BattlePolicyMemory(state), slots.source, slots.positions, None, None)\nreturn EmptySlotResult(fields.offset, slots.source, state.carry_result(1 if fields.carry else 0))'}, 'find_next_empty_position_slot_fields': {'signature': 'memory: BattlePolicyMemory, source, positions, retained_index: Long | None, retained_extend: bool | None', 'returns': 'DeploymentSlotFields', 'flow': "if type(memory) is not BattlePolicyMemory:\n    raise ValueError('typed same-state slot memory required')\nchecked_deployment_cursor(source, memory.state)\nchecked_policy_table(positions, memory.state)\nif retained_index is not None:\n    uint(retained_index, 32)\nif retained_extend is not None and type(retained_extend) is not bool:\n    raise ValueError('actual incoming X required when observed')\nindex = retained_index\nextend = retained_extend\nwhile True:\n    member = source.next_word()\n    index = None if index is None else replace_word(index, member)\n    if negative_word(member):\n        return DeploymentSlotFields(index, member, source, positions, True, False, True, extend)\n    offset = u16(member << 2)\n    index = None if index is None else replace_word(index, offset)\n    extend = member & 16384 != 0\n    value = positions.long(offset)\n    if value == 0:\n        return DeploymentSlotFields(index, offset, source, positions, False, True, False, extend)"}, 'read_city_second_deployment_anchor': {'signature': 'state: GameState, retained: AnchorContext', 'returns': 'tuple[Long, Long]', 'flow': 'state = checked_state(state)\nretained = checked_context(retained, AnchorContext)\nfields = read_city_second_deployment_anchor_fields(BattlePolicyMemory(state), retained, None)\nreturn (fields.x, fields.y)'}, 'read_city_second_deployment_anchor_fields': {'signature': 'memory: BattlePolicyMemory, retained: AnchorContext, retained_index: Long | None', 'returns': 'DeploymentAnchorFields', 'flow': "if type(memory) is not BattlePolicyMemory:\n    raise ValueError('typed live second-anchor memory required')\nretained = checked_context(retained, AnchorContext)\nif retained_index is not None:\n    uint(retained_index, 32)\noffset = u16(memory.battle_scene() << 2)\nindex = None if retained_index is None else replace_word(retained_index, offset)\ncells = memory.state.table(713462)\noriginal_x = cells.word(offset)\nx = replace_word(retained.x, original_x >> 3 >> 7)\noriginal_y = cells.word(offset, 2)\ny = replace_word(retained.y, original_y >> 3 >> 7)\nreturn DeploymentAnchorFields(x, y, index, cells, low16(y) == 0, False, original_y & 512 != 0)"}, 'scan_deployment_first_edge': {'signature': 'state: GameState, edge: DeploymentEdgeContext', 'returns': 'EmptySlotResult', 'flow': 'state = checked_state(state)\nedge = checked_context(edge, DeploymentEdgeContext, state)\nx = u16(edge.center_x - edge.radius)\noffset = edge.offset\nif not deployment_edge_coordinate_allowed(x, 25):\n    return EmptySlotResult(offset, edge.source, state.carry_result(0))\ndelta = u16(-edge.radius)\nwhile True:\n    y = u16(edge.center_y + delta)\n    if 3 <= y <= 37:\n        outcome = try_place_deployment_cell(state, DeploymentCellContext(edge.map, edge.positions, offset, x, y))\n        if outcome.carry != 0:\n            vacancy = find_next_empty_position_slot(state, EmptySlotContext(edge.source, edge.positions))\n            offset = vacancy.offset\n            if vacancy.outcome.carry != 0:\n                return EmptySlotResult(offset, edge.source, state.carry_result(1))\n    delta = u16(delta + 2)\n    if s16(delta) > s16(edge.radius):\n        break\nreturn EmptySlotResult(offset, edge.source, state.carry_result(0))'}, 'scan_deployment_second_edge': {'signature': 'state: GameState, edge: DeploymentEdgeContext', 'returns': 'EmptySlotResult', 'flow': 'state = checked_state(state)\nedge = checked_context(edge, DeploymentEdgeContext, state)\ny = u16(edge.center_y - edge.radius)\noffset = edge.offset\nif not deployment_edge_coordinate_allowed(y, 37):\n    return EmptySlotResult(offset, edge.source, state.carry_result(0))\ndelta = u16(-u16(edge.radius - 2))\nwhile True:\n    x = u16(edge.center_x + delta)\n    if 3 <= x <= 25:\n        outcome = try_place_deployment_cell(state, DeploymentCellContext(edge.map, edge.positions, offset, x, y))\n        if outcome.carry != 0:\n            vacancy = find_next_empty_position_slot(state, EmptySlotContext(edge.source, edge.positions))\n            offset = vacancy.offset\n            if vacancy.outcome.carry != 0:\n                return EmptySlotResult(offset, edge.source, state.carry_result(1))\n    delta = u16(delta + 2)\n    if s16(delta) >= s16(edge.radius):\n        break\nreturn EmptySlotResult(offset, edge.source, state.carry_result(0))'}})
APPROVED['contexts_policy_memory'].add('checked_policy_table')
APPROVED['contexts_deployment_fields'] = {'DeploymentOccupiedFields', 'DeploymentSlotFields', 'checked_deployment_cursor', 'changed_deployment_return'}
DEPLOYMENT_FIELD_HELPERS = ('_append_occupied_deployment_call', 'append_roster_occupied_cell_fields', 'build_deployment_occupied_cell_fields', 'deployment_edge_coordinate_allowed', 'find_next_empty_position_slot_fields', 'read_city_second_deployment_anchor_fields')
DEPLOYMENT_FIELD_ALGORITHMS = {'read_city_second_deployment_anchor': ['read_city_second_deployment_anchor_fields'], 'append_roster_occupied_cells': ['append_roster_occupied_cell_fields'], 'build_deployment_occupied_cells': ['build_deployment_occupied_cell_fields', '_append_occupied_deployment_call', 'append_roster_occupied_cell_fields'], 'find_next_empty_position_slot': ['find_next_empty_position_slot_fields'], 'scan_deployment_first_edge': ['deployment_edge_coordinate_allowed'], 'scan_deployment_second_edge': ['deployment_edge_coordinate_allowed']}


# Current fields are consumed; no second fixed body replaces the supplied AST.
DOMAIN_DECLARATIONS.update({'try_place_deployment_cell': {'signature': 'state: GameState, cell: DeploymentCellContext', 'returns': 'CarryOutcome', 'flow': 'state = checked_state(state)\ncell = checked_context(cell, DeploymentCellContext, state)\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=cell.map, candidates=cell.positions, status=state.sr & 31)\nfields = try_place_deployment_cell_fields(BattlePolicyMemory(state), frame, cell.x, cell.y, cell.offset).validate(state)\nreturn state.carry_result(1 if fields.placed else 0)'}, 'scan_deployment_first_edge': {'signature': 'state: GameState, edge: DeploymentEdgeContext', 'returns': 'EmptySlotResult', 'flow': 'state = checked_state(state)\nedge = checked_context(edge, DeploymentEdgeContext, state)\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=edge.map, candidates=edge.positions, scan=edge.source, status=state.sr & 31)\nfields = scan_deployment_first_edge_fields(BattlePolicyMemory(state), frame, edge.center_x, edge.center_y, edge.radius, edge.offset).validate(state)\nreturn EmptySlotResult(fields.offset, fields.source, state.carry_result(1 if fields.found else 0))'}, 'scan_deployment_second_edge': {'signature': 'state: GameState, edge: DeploymentEdgeContext', 'returns': 'EmptySlotResult', 'flow': 'state = checked_state(state)\nedge = checked_context(edge, DeploymentEdgeContext, state)\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=edge.map, candidates=edge.positions, scan=edge.source, status=state.sr & 31)\nfields = scan_deployment_second_edge_fields(BattlePolicyMemory(state), frame, edge.center_x, edge.center_y, edge.radius, edge.offset).validate(state)\nreturn EmptySlotResult(fields.offset, fields.source, state.carry_result(1 if fields.found else 0))'}, 'promote_first_roster_deployment_candidate': {'signature': 'state: GameState, retained: PromotionContext', 'returns': 'None', 'flow': 'state = checked_state(state)\nretained = checked_context(retained, PromotionContext)\nframe = first_replace(FirstDeploymentFrame.unobserved(), count=retained.formation_carrier, status=state.sr & 31)\npromote_first_roster_deployment_candidate_fields(BattlePolicyMemory(state), frame)\nreturn None'}, 'promote_second_roster_deployment_candidate': {'signature': 'state: GameState', 'returns': 'None', 'flow': 'state = checked_state(state)\nframe = first_replace(FirstDeploymentFrame.unobserved(), status=state.sr & 31)\npromote_second_roster_deployment_candidate_fields(BattlePolicyMemory(state), frame)\nreturn None'}, '_deployment_word': {'signature': 'carrier: Long | None, word: Word', 'returns': 'Long | None', 'flow': 'uint(word, 16)\nif carrier is None:\n    return None\nreturn replace_word(carrier, word)'}, '_deployment_byte': {'signature': 'carrier: Long | None, value: Word', 'returns': 'Long | None', 'flow': 'uint(value, 8)\nif carrier is None:\n    return None\nreturn replace_byte(carrier, value)'}, '_deployment_flags': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, status: Word', 'returns': 'FirstDeploymentFrame', 'flow': "uint(status, 8)\nif status > 31:\n    raise ValueError('actual CCR must be in the low five bits')\nmemory.state.sr = memory.state.sr & 65504 | status\nreturn first_replace(frame, status=status)"}, '_deployment_move_word': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, word: Word', 'returns': 'FirstDeploymentFrame', 'flow': "uint(word, 16)\nif frame.status is None:\n    raise ValueError('current CCR observation required')\nreturn _deployment_flags(memory, frame, frame.status & 16 | (8 if word & 32768 else 0) | (4 if word == 0 else 0))"}, '_deployment_move_byte': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, value: Word', 'returns': 'FirstDeploymentFrame', 'flow': "uint(value, 8)\nif frame.status is None:\n    raise ValueError('current CCR observation required')\nreturn _deployment_flags(memory, frame, frame.status & 16 | (8 if value & 128 else 0) | (4 if value == 0 else 0))"}, '_deployment_sum': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, left: Word, right: Word', 'returns': 'tuple[Word, FirstDeploymentFrame]', 'flow': 'uint(left, 16)\nuint(right, 16)\nwide = left + right\nvalue = u16(wide)\noverflow = ~(left ^ right) & (left ^ value) & 32768 != 0\nframe = _deployment_flags(memory, frame, (17 if wide > 65535 else 0) | (8 if value & 32768 else 0) | (4 if value == 0 else 0) | (2 if overflow else 0))\nreturn (value, frame)'}, '_deployment_difference': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, left: Word, right: Word', 'returns': 'tuple[Word, FirstDeploymentFrame]', 'flow': 'uint(left, 16)\nuint(right, 16)\nvalue = u16(left - right)\noverflow = (left ^ right) & (left ^ value) & 32768 != 0\nframe = _deployment_flags(memory, frame, (17 if left < right else 0) | (8 if value & 32768 else 0) | (4 if value == 0 else 0) | (2 if overflow else 0))\nreturn (value, frame)'}, '_deployment_compare': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, left: Word, right: Word', 'returns': 'FirstDeploymentFrame', 'flow': "uint(left, 16)\nuint(right, 16)\nif frame.status is None:\n    raise ValueError('current compare X observation required')\nvalue = u16(left - right)\noverflow = (left ^ right) & (left ^ value) & 32768 != 0\nreturn _deployment_flags(memory, frame, frame.status & 16 | (1 if left < right else 0) | (8 if value & 32768 else 0) | (4 if value == 0 else 0) | (2 if overflow else 0))"}, '_deployment_compare_byte': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, left: Word, right: Word', 'returns': 'FirstDeploymentFrame', 'flow': "uint(left, 8)\nuint(right, 8)\nif frame.status is None:\n    raise ValueError('current compare X observation required')\nvalue = left - right & 255\noverflow = (left ^ right) & (left ^ value) & 128 != 0\nreturn _deployment_flags(memory, frame, frame.status & 16 | (1 if left < right else 0) | (8 if value & 128 else 0) | (4 if value == 0 else 0) | (2 if overflow else 0))"}, '_deployment_left_shift': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, word: Word, count: Word', 'returns': 'tuple[Word, FirstDeploymentFrame]', 'flow': "uint(word, 16)\nuint(count, 16)\nif count < 1 or count > 15:\n    raise ValueError('known WORD logical shift count required')\nvalue = u16(word << count)\nshifted = word >> 16 - count & 1\nframe = _deployment_flags(memory, frame, (17 if shifted else 0) | (8 if value & 32768 else 0) | (4 if value == 0 else 0))\nreturn (value, frame)"}, '_deployment_right_shift': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, word: Word, count: Word', 'returns': 'tuple[Word, FirstDeploymentFrame]', 'flow': "uint(word, 16)\nuint(count, 16)\nif count < 1 or count > 15:\n    raise ValueError('known WORD logical shift count required')\nvalue = word >> count\nshifted = word >> count - 1 & 1\nframe = _deployment_flags(memory, frame, (17 if shifted else 0) | (4 if value == 0 else 0))\nreturn (value, frame)"}, '_deployment_carry': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, value: bool', 'returns': 'FirstDeploymentFrame', 'flow': "if type(value) is not bool:\n    raise ValueError('real carry decision required')\nif type(memory.state) is GameState:\n    memory.state.carry_result(1 if value else 0)\nelse:\n    memory.state.set_status_word(memory.state.sr & 65534 | (1 if value else 0))\nreturn first_replace(frame, status=memory.state.sr & 31)"}, '_deployment_push': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, value: Long', 'returns': 'FirstDeploymentFrame', 'flow': 'uint(value, 32)\nframe.validate(memory.state, complete=True)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, value)\nreturn first_replace(frame, stack_cursor=stack)'}, '_deployment_pop': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple[FirstDeploymentFrame, Long]', 'flow': 'frame.validate(memory.state, complete=True)\nvalue = frame.stack_cursor.long()\nreturn (first_replace(frame, stack_cursor=frame.stack_cursor.advance(4)), value)'}, '_deployment_enter': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': 'uint(continuation, 32)\nif frame.stack_cursor is None:\n    return frame\nreturn _deployment_push(memory, frame, continuation)'}, '_deployment_leave': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': 'uint(continuation, 32)\nif frame.stack_cursor is None:\n    return frame\ncurrent, target = _deployment_pop(memory, frame)\nif target != continuation:\n    raise FirstDeploymentReturnBoundary(target, current, continuation)\nreturn current'}, '_deployment_save_probe': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'if frame.stack_cursor is None:\n    return frame\nframe = _deployment_push(memory, frame, frame.distance)\nframe = _deployment_push(memory, frame, frame.count)\nframe = _deployment_push(memory, frame, frame.unit)\nframe = _deployment_push(memory, frame, frame.target_y)\nreturn _deployment_push(memory, frame, frame.target_x)'}, '_deployment_restore_probe': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, observed: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'if frame.stack_cursor is None:\n    return first_replace(frame, target_x=observed.target_x, target_y=observed.target_y, unit=observed.unit, count=observed.count, distance=observed.distance)\nframe, target_x = _deployment_pop(memory, frame)\nframe, target_y = _deployment_pop(memory, frame)\nframe, unit = _deployment_pop(memory, frame)\nframe, count = _deployment_pop(memory, frame)\nframe, distance = _deployment_pop(memory, frame)\nreturn first_replace(frame, target_x=target_x, target_y=target_y, unit=unit, count=count, distance=distance)'}, '_deployment_terrain_lookup': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, x: Word, y: Word', 'returns': 'tuple[FirstDeploymentFrame, Word]', 'flow': "if frame.roster is None:\n    raise ValueError('actual current A0 map required')\nmap_context = frame.roster\nobserved = frame\nframe = _deployment_enter(memory, frame, 154990)\nif frame.stack_cursor is not None:\n    frame = _deployment_push(memory, frame, frame.roster.base)\n    frame = _deployment_push(memory, frame, frame.count)\n    frame = _deployment_push(memory, frame, frame.unit)\n    frame = _deployment_push(memory, frame, frame.target_y)\nsample = read_battlefield_terrain_type_fields(memory, map_context, x, y, frame.target_x).validate(memory.state)\nframe = first_replace(frame, target_x=sample.carrier, roster=sample.lookup.cursor())\nframe = _deployment_flags(memory, frame, (16 if sample.extend else 0) | (8 if sample.category & 128 else 0) | (4 if sample.category == 0 else 0))\nif frame.stack_cursor is None:\n    frame = first_replace(frame, target_y=observed.target_y, unit=observed.unit, count=observed.count, roster=observed.roster)\nelse:\n    frame, target_y = _deployment_pop(memory, frame)\n    frame, unit = _deployment_pop(memory, frame)\n    frame, count = _deployment_pop(memory, frame)\n    frame, roster = _deployment_pop(memory, frame)\n    frame = first_replace(frame, target_y=target_y, unit=unit, count=count, roster=memory.state.table(roster).cursor())\nreturn (_deployment_leave(memory, frame, 154990), sample.category)"}, 'try_place_deployment_cell_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, x: Word, y: Word, offset: Word', 'returns': 'DeploymentProbeFields', 'flow': "if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:\n    raise ValueError('sealed memory and retained deployment frame required')\nframe.validate(memory.state)\nuint(x, 16)\nuint(y, 16)\nuint(offset, 16)\nif frame.roster is None or frame.candidates is None:\n    raise ValueError('actual A0 terrain and A1 position views required')\nobserved = frame\nframe = _deployment_save_probe(memory, frame)\noccupied = memory.state.table(4294955776).cursor()\nframe = first_replace(frame, controller=occupied)\nframe = _deployment_move_word(memory, frame, x)\nleft, frame = _deployment_difference(memory, frame, x, 3)\nframe = first_replace(frame, target_x=_deployment_word(frame.target_x, left))\nright, frame = _deployment_sum(memory, frame, x, 3)\nframe = first_replace(frame, unit=_deployment_word(frame.unit, right))\nframe = _deployment_move_word(memory, frame, y)\nbottom, frame = _deployment_difference(memory, frame, y, 3)\nframe = first_replace(frame, target_y=_deployment_word(frame.target_y, bottom))\ntop, frame = _deployment_sum(memory, frame, y, 3)\nframe = first_replace(frame, count=_deployment_word(frame.count, top))\nwhile True:\n    frame = first_replace(frame, distance=_deployment_word(frame.distance, 0))\n    frame = _deployment_move_word(memory, frame, 0)\n    near_x = occupied.byte()\n    frame = first_replace(frame, distance=_deployment_byte(frame.distance, near_x))\n    frame = _deployment_move_byte(memory, frame, near_x)\n    if negative_byte(near_x):\n        break\n    frame = _deployment_compare(memory, frame, near_x, left)\n    if s16(near_x) >= s16(left):\n        frame = _deployment_compare(memory, frame, near_x, right)\n        if s16(near_x) <= s16(right):\n            near_y = occupied.byte(0, 1)\n            frame = first_replace(frame, distance=_deployment_byte(frame.distance, near_y))\n            frame = _deployment_move_byte(memory, frame, near_y)\n            frame = _deployment_compare(memory, frame, near_y, bottom)\n            if s16(near_y) >= s16(bottom):\n                frame = _deployment_compare(memory, frame, near_y, top)\n                if s16(near_y) <= s16(top):\n                    frame = _deployment_restore_probe(memory, frame, observed)\n                    return DeploymentProbeFields(_deployment_carry(memory, frame, False), False)\n    occupied = occupied.advance(2)\n    frame = first_replace(frame, controller=occupied)\nterrain_x, frame = _deployment_sum(memory, frame, left, 3)\nterrain_x, frame = _deployment_left_shift(memory, frame, terrain_x, 3)\nframe = first_replace(frame, target_x=_deployment_word(frame.target_x, terrain_x))\nterrain_y, frame = _deployment_sum(memory, frame, bottom, 3)\nterrain_y, frame = _deployment_left_shift(memory, frame, terrain_y, 3)\nframe = first_replace(frame, target_y=_deployment_word(frame.target_y, terrain_y))\nframe = _deployment_move_word(memory, frame, terrain_y)\nframe = first_replace(frame, unit=_deployment_word(frame.unit, terrain_y))\nframe = _deployment_move_word(memory, frame, terrain_x)\nframe = first_replace(frame, target_y=_deployment_word(frame.target_y, terrain_x))\nframe, category = _deployment_terrain_lookup(memory, frame, terrain_x, terrain_y)\nframe = _deployment_compare_byte(memory, frame, category, 1)\nblocked = category == 1\nif not blocked:\n    frame = _deployment_compare_byte(memory, frame, category, 6)\n    blocked = category == 6\nif not blocked:\n    frame = _deployment_compare_byte(memory, frame, category, 7)\n    blocked = category == 7\nif blocked:\n    frame = _deployment_restore_probe(memory, frame, observed)\n    return DeploymentProbeFields(_deployment_carry(memory, frame, False), False)\ncurrent_x = terrain_x if frame.target_y is None else low16(frame.target_y)\ncurrent_y = terrain_y if frame.unit is None else low16(frame.unit)\nposition_x, frame = _deployment_left_shift(memory, frame, current_x, 7)\nframe = first_replace(frame, target_y=_deployment_word(frame.target_y, position_x))\nframe.candidates.set_word(offset, position_x)\nframe = _deployment_move_word(memory, frame, position_x)\nposition_y, frame = _deployment_left_shift(memory, frame, current_y, 7)\nframe = first_replace(frame, unit=_deployment_word(frame.unit, position_y))\nframe.candidates.set_word(offset, position_y, 2)\nframe = _deployment_move_word(memory, frame, position_y)\nframe = _deployment_restore_probe(memory, frame, observed)\nreturn DeploymentProbeFields(_deployment_carry(memory, frame, True), True)"}, '_deployment_probe_call': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, x: Word, y: Word, offset: Word, continuation: Long', 'returns': 'DeploymentProbeFields', 'flow': 'entered = _deployment_enter(memory, frame, continuation)\nresult = try_place_deployment_cell_fields(memory, entered, x, y, offset).validate(memory.state)\nreturn DeploymentProbeFields(_deployment_leave(memory, result.frame, continuation), result.placed)'}, '_deployment_vacancy_call': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, continuation: Long', 'returns': 'DeploymentEdgeFields', 'flow': "if frame.scan is None or frame.candidates is None:\n    raise ValueError('actual current A3 roster and A1 positions required')\nentered = _deployment_enter(memory, frame, continuation)\nvacancy = find_next_empty_position_slot_fields(memory, entered.scan, entered.candidates, entered.offset_y, entered.status & 16 != 0)\nstatus = (16 if vacancy.extend else 0) | (8 if vacancy.negative else 0) | (4 if vacancy.zero else 0) | (1 if vacancy.carry else 0)\ncurrent = _deployment_flags(memory, entered, status)\ncurrent = first_replace(current, offset_y=vacancy.index, scan=vacancy.source)\ncurrent = _deployment_carry(memory, current, vacancy.carry)\nreturn DeploymentEdgeFields(_deployment_leave(memory, current, continuation), vacancy.offset, vacancy.source, vacancy.carry)"}, 'scan_deployment_first_edge_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, center_x: Word, center_y: Word, radius: Word, offset: Word, prefix: bool=True', 'returns': 'DeploymentEdgeFields', 'flow': "frame.validate(memory.state)\nfor value in (center_x, center_y, radius, offset):\n    uint(value, 16)\nif type(prefix) is not bool or frame.scan is None:\n    raise ValueError('actual edge entry and A3 roster required')\nif prefix:\n    frame = _deployment_move_word(memory, frame, radius)\n    x, frame = _deployment_difference(memory, frame, 0, radius)\n    x, frame = _deployment_sum(memory, frame, x, center_x)\n    frame = first_replace(frame, unit=_deployment_word(frame.unit, x))\nelse:\n    if frame.unit is None:\n        raise ValueError('alternate first edge requires current D2 LONG')\n    x = low16(frame.unit)\nframe = _deployment_compare(memory, frame, x, 3)\nif x < 3:\n    return DeploymentEdgeFields(_deployment_carry(memory, frame, False), offset, frame.scan, False)\nframe = _deployment_compare(memory, frame, x, 25)\nif x > 25:\n    return DeploymentEdgeFields(_deployment_carry(memory, frame, False), offset, frame.scan, False)\nframe = _deployment_move_word(memory, frame, radius)\ndelta, frame = _deployment_difference(memory, frame, 0, radius)\nframe = first_replace(frame, distance=_deployment_word(frame.distance, delta))\nwhile True:\n    current_center_y = center_y if frame.target_y is None else low16(frame.target_y)\n    frame = _deployment_move_word(memory, frame, delta)\n    y, frame = _deployment_sum(memory, frame, delta, current_center_y)\n    frame = first_replace(frame, count=_deployment_word(frame.count, y))\n    frame = _deployment_compare(memory, frame, y, 3)\n    if y >= 3:\n        frame = _deployment_compare(memory, frame, y, 37)\n        if y <= 37:\n            result = _deployment_probe_call(memory, frame, x, y, offset, 154858)\n            frame = result.frame\n            if result.placed:\n                vacancy = _deployment_vacancy_call(memory, frame, 154864)\n                frame, offset = (vacancy.frame, vacancy.offset)\n                if vacancy.found:\n                    return DeploymentEdgeFields(_deployment_carry(memory, frame, True), offset, frame.scan, True)\n    current_delta = delta if frame.distance is None else low16(frame.distance)\n    delta, frame = _deployment_sum(memory, frame, current_delta, 2)\n    frame = first_replace(frame, distance=_deployment_word(frame.distance, delta))\n    current_radius = radius if frame.choice is None else low16(frame.choice)\n    frame = _deployment_compare(memory, frame, delta, current_radius)\n    if s16(delta) > s16(current_radius):\n        return DeploymentEdgeFields(_deployment_carry(memory, frame, False), offset, frame.scan, False)\n    if frame.unit is not None:\n        x = low16(frame.unit)"}, 'scan_deployment_second_edge_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, center_x: Word, center_y: Word, radius: Word, offset: Word, prefix: bool=True', 'returns': 'DeploymentEdgeFields', 'flow': "frame.validate(memory.state)\nfor value in (center_x, center_y, radius, offset):\n    uint(value, 16)\nif type(prefix) is not bool or frame.scan is None:\n    raise ValueError('actual edge entry and A3 roster required')\nif prefix:\n    frame = _deployment_move_word(memory, frame, radius)\n    y, frame = _deployment_difference(memory, frame, 0, radius)\n    y, frame = _deployment_sum(memory, frame, y, center_y)\n    frame = first_replace(frame, count=_deployment_word(frame.count, y))\nelse:\n    if frame.count is None:\n        raise ValueError('alternate second edge requires current D3 LONG')\n    y = low16(frame.count)\nframe = _deployment_compare(memory, frame, y, 3)\nif y < 3:\n    return DeploymentEdgeFields(_deployment_carry(memory, frame, False), offset, frame.scan, False)\nframe = _deployment_compare(memory, frame, y, 37)\nif y > 37:\n    return DeploymentEdgeFields(_deployment_carry(memory, frame, False), offset, frame.scan, False)\nframe = _deployment_move_word(memory, frame, radius)\ndelta, frame = _deployment_difference(memory, frame, radius, 2)\ndelta, frame = _deployment_difference(memory, frame, 0, delta)\nframe = first_replace(frame, distance=_deployment_word(frame.distance, delta))\nwhile True:\n    current_center_x = center_x if frame.target_x is None else low16(frame.target_x)\n    frame = _deployment_move_word(memory, frame, delta)\n    x, frame = _deployment_sum(memory, frame, delta, current_center_x)\n    frame = first_replace(frame, unit=_deployment_word(frame.unit, x))\n    frame = _deployment_compare(memory, frame, x, 3)\n    if x >= 3:\n        frame = _deployment_compare(memory, frame, x, 25)\n        if x <= 25:\n            result = _deployment_probe_call(memory, frame, x, y, offset, 155082)\n            frame = result.frame\n            if result.placed:\n                vacancy = _deployment_vacancy_call(memory, frame, 155090)\n                frame, offset = (vacancy.frame, vacancy.offset)\n                if vacancy.found:\n                    return DeploymentEdgeFields(_deployment_carry(memory, frame, True), offset, frame.scan, True)\n    current_delta = delta if frame.distance is None else low16(frame.distance)\n    delta, frame = _deployment_sum(memory, frame, current_delta, 2)\n    frame = first_replace(frame, distance=_deployment_word(frame.distance, delta))\n    current_radius = radius if frame.choice is None else low16(frame.choice)\n    frame = _deployment_compare(memory, frame, delta, current_radius)\n    if s16(delta) >= s16(current_radius):\n        return DeploymentEdgeFields(_deployment_carry(memory, frame, False), offset, frame.scan, False)\n    if frame.count is not None:\n        y = low16(frame.count)"}, 'promote_first_roster_deployment_candidate_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame.validate(memory.state)\nrulers = memory.state.table(4294960704)\nframe = first_replace(frame, roster=rulers.cursor())\nmember = memory.state.read(4294964876, 2)\nframe = first_replace(frame, target_x=_deployment_word(frame.target_x, member))\nframe = _deployment_move_word(memory, frame, member)\nmember, frame = _deployment_left_shift(memory, frame, member, 1)\nmember = rulers.word(member)\nframe = first_replace(frame, target_x=_deployment_word(frame.target_x, member))\nframe = _deployment_move_word(memory, frame, member)\nheads = memory.state.table(4294942759)\nframe = first_replace(frame, roster=heads.cursor())\nprevious = memory.battle_scene()\nframe = first_replace(frame, target_y=_deployment_word(frame.target_y, previous))\nframe = _deployment_move_word(memory, frame, previous)\nprevious_byte = heads.byte(previous)\nprevious = previous & 65280 | previous_byte\nframe = first_replace(frame, target_y=_deployment_byte(frame.target_y, previous_byte))\nframe = _deployment_move_byte(memory, frame, previous_byte)\nframe = _deployment_compare(memory, frame, previous, member)\nif previous == member:\n    return frame\nroster = memory.state.table(4294944080)\nsource = roster.cursor()\nframe = first_replace(frame, roster=source)\nwhile True:\n    item = source.next_word()\n    frame = first_replace(frame, unit=_deployment_word(frame.unit, item))\n    frame = _deployment_move_word(memory, frame, item)\n    if negative_word(item):\n        return frame\n    item &= 255\n    frame = first_replace(frame, unit=_deployment_word(frame.unit, item))\n    frame = _deployment_move_word(memory, frame, item)\n    frame = _deployment_compare(memory, frame, member, item)\n    if member == item:\n        break\ndeployed = memory.state.table(4294946344)\nframe = first_replace(frame, controller=deployed.cursor())\ndeployed.set_byte(member, 1)\nframe = _deployment_move_byte(memory, frame, 1)\nvariants = memory.scene_variants\nframe = first_replace(frame, roster=variants.cursor())\nscene = memory.battle_scene()\nframe = first_replace(frame, unit=_deployment_word(frame.unit, scene))\nframe = _deployment_move_word(memory, frame, scene)\nformation_byte = variants.byte(scene)\nif frame.count is None:\n    raise ValueError('actual retained D3 needed by first promotion variant BYTE alias')\nformation = low16(replace_byte(frame.count, formation_byte))\nframe = first_replace(frame, count=_deployment_byte(frame.count, formation_byte))\nframe = _deployment_move_byte(memory, frame, formation_byte)\nformation, frame = _deployment_left_shift(memory, frame, formation, 1)\nframe = first_replace(frame, count=_deployment_word(frame.count, formation))\ncell, frame = _deployment_left_shift(memory, frame, scene, 5)\ncell, frame = _deployment_sum(memory, frame, cell, formation)\nframe = first_replace(frame, unit=_deployment_word(frame.unit, cell))\nmember_offset, frame = _deployment_left_shift(memory, frame, member, 2)\nframe = first_replace(frame, target_x=_deployment_word(frame.target_x, member_offset))\ncells = memory.deployment_cells\npositions = memory.state.table(16722944)\nframe = first_replace(frame, candidates=cells.cursor(), scan=positions.cursor())\nframe = first_replace(frame, count=_deployment_word(frame.count, 0))\nframe = _deployment_move_word(memory, frame, 0)\nx_byte = cells.byte(cell)\nframe = first_replace(frame, count=_deployment_byte(frame.count, x_byte))\nframe = _deployment_move_byte(memory, frame, x_byte)\nx, frame = _deployment_left_shift(memory, frame, x_byte, 3)\nframe = first_replace(frame, count=_deployment_word(frame.count, x))\npositions.set_word(member_offset, x)\nframe = _deployment_move_word(memory, frame, x)\nframe = first_replace(frame, count=_deployment_word(frame.count, 0))\nframe = _deployment_move_word(memory, frame, 0)\ny_byte = cells.byte(cell, 1)\nframe = first_replace(frame, count=_deployment_byte(frame.count, y_byte))\nframe = _deployment_move_byte(memory, frame, y_byte)\ny, frame = _deployment_left_shift(memory, frame, y_byte, 3)\nframe = first_replace(frame, count=_deployment_word(frame.count, y))\npositions.set_word(member_offset, y, 2)\nframe = _deployment_move_word(memory, frame, y)\nfixed_positions = memory.state.table(4294943056)\nframe = first_replace(frame, roster=fixed_positions.cursor())\nprevious_offset, frame = _deployment_left_shift(memory, frame, previous, 2)\nframe = first_replace(frame, target_y=_deployment_word(frame.target_y, previous_offset))\nframe = first_replace(frame, count=_deployment_word(frame.count, 0))\nframe = _deployment_move_word(memory, frame, 0)\nx_byte = cells.byte(cell)\nframe = _deployment_move_byte(memory, frame, x_byte)\nx, frame = _deployment_left_shift(memory, frame, x_byte, 3)\nx, frame = _deployment_left_shift(memory, frame, x, 7)\nprevious_x = fixed_positions.word(previous_offset)\nx_difference, frame = _deployment_difference(memory, frame, x, previous_x)\nif x < previous_x:\n    x_difference, frame = _deployment_difference(memory, frame, 0, x_difference)\nframe = first_replace(frame, count=_deployment_word(frame.count, x_difference))\nframe = _deployment_compare(memory, frame, x_difference, 1024)\nif x_difference <= 1024:\n    frame = first_replace(frame, count=_deployment_word(frame.count, 0))\n    frame = _deployment_move_word(memory, frame, 0)\n    y_byte = cells.byte(cell, 1)\n    frame = _deployment_move_byte(memory, frame, y_byte)\n    y, frame = _deployment_left_shift(memory, frame, y_byte, 3)\n    y, frame = _deployment_left_shift(memory, frame, y, 7)\n    previous_y = fixed_positions.word(previous_offset, 2)\n    y_difference, frame = _deployment_difference(memory, frame, y, previous_y)\n    if y < previous_y:\n        y_difference, frame = _deployment_difference(memory, frame, 0, y_difference)\n    frame = first_replace(frame, count=_deployment_word(frame.count, y_difference))\n    frame = _deployment_compare(memory, frame, y_difference, 1024)\n    if y_difference < 1024:\n        x = fixed_positions.word(member_offset)\n        frame = _deployment_move_word(memory, frame, x)\n        x, frame = _deployment_right_shift(memory, frame, x, 7)\n        frame = first_replace(frame, count=_deployment_word(frame.count, x))\n        positions.set_word(previous_offset, x)\n        frame = _deployment_move_word(memory, frame, x)\n        y = fixed_positions.word(member_offset, 2)\n        frame = _deployment_move_word(memory, frame, y)\n        y, frame = _deployment_right_shift(memory, frame, y, 7)\n        frame = first_replace(frame, count=_deployment_word(frame.count, y))\n        positions.set_word(previous_offset, y, 2)\n        frame = _deployment_move_word(memory, frame, y)\n        previous, frame = _deployment_right_shift(memory, frame, previous_offset, 2)\n        frame = first_replace(frame, target_y=_deployment_word(frame.target_y, previous))\n        deployed.set_byte(previous, 1)\n        frame = _deployment_move_byte(memory, frame, 1)\nmember, frame = _deployment_right_shift(memory, frame, member_offset, 2)\nframe = first_replace(frame, target_x=_deployment_word(frame.target_x, member))\nsource, destination = (roster.cursor(), roster.cursor(2))\nframe = first_replace(frame, roster=source, candidates=destination)\nwhile True:\n    item = source.next_word()\n    frame = first_replace(frame, target_y=_deployment_word(frame.target_y, item))\n    frame = _deployment_move_word(memory, frame, item)\n    if negative_word(item):\n        break\n    frame = _deployment_compare(memory, frame, item, member)\n    if item == member:\n        continue\n    destination.append_word(item)\n    frame = _deployment_move_word(memory, frame, item)\nroster.set_word(0, member)\nframe = _deployment_move_word(memory, frame, member)\nframe = first_replace(frame, roster=heads.cursor())\nscene = memory.battle_scene()\nframe = first_replace(frame, target_y=_deployment_word(frame.target_y, scene))\nframe = _deployment_move_word(memory, frame, scene)\nheads.set_byte(scene, low8(member))\nreturn _deployment_move_byte(memory, frame, low8(member))"}, 'promote_second_roster_deployment_candidate_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame.validate(memory.state)\nrulers = memory.state.table(4294960704)\nframe = first_replace(frame, roster=rulers.cursor())\nmember = memory.state.read(4294964878, 2)\nframe = first_replace(frame, target_x=_deployment_word(frame.target_x, member))\nframe = _deployment_move_word(memory, frame, member)\nmember, frame = _deployment_left_shift(memory, frame, member, 1)\nmember = rulers.word(member)\nframe = first_replace(frame, target_x=_deployment_word(frame.target_x, member))\nframe = _deployment_move_word(memory, frame, member)\nheads = memory.state.table(4294964318)\nframe = first_replace(frame, roster=heads.cursor())\nscene = memory.battle_scene()\nframe = first_replace(frame, target_y=_deployment_word(frame.target_y, scene))\nframe = _deployment_move_word(memory, frame, scene)\nscene_offset, frame = _deployment_left_shift(memory, frame, scene, 1)\nprevious = heads.word(scene_offset)\nframe = first_replace(frame, target_y=_deployment_word(frame.target_y, previous))\nframe = _deployment_move_word(memory, frame, previous)\nframe = _deployment_compare(memory, frame, previous, member)\nif previous == member:\n    return frame\nroster = memory.state.table(4294944164)\nsource = roster.cursor()\nframe = first_replace(frame, roster=source)\nwhile True:\n    item = source.next_word()\n    frame = first_replace(frame, unit=_deployment_word(frame.unit, item))\n    frame = _deployment_move_word(memory, frame, item)\n    if negative_word(item):\n        return frame\n    item &= 255\n    frame = first_replace(frame, unit=_deployment_word(frame.unit, item))\n    frame = _deployment_move_word(memory, frame, item)\n    frame = _deployment_compare(memory, frame, item, member)\n    if item == member:\n        break\ndeployed = memory.state.table(4294946344)\nframe = first_replace(frame, controller=deployed.cursor())\ndeployed.set_byte(member, 1)\nframe = _deployment_move_byte(memory, frame, 1)\ncatalog = memory.state.table(710766)\nframe = first_replace(frame, roster=catalog.cursor())\nscene = memory.battle_scene()\nframe = first_replace(frame, unit=_deployment_word(frame.unit, scene))\nframe = _deployment_move_word(memory, frame, scene)\nframe = first_replace(frame, count=_deployment_word(frame.count, scene))\nframe = _deployment_move_word(memory, frame, scene)\ncell, frame = _deployment_left_shift(memory, frame, scene, 1)\ncell, frame = _deployment_sum(memory, frame, cell, scene)\ncell, frame = _deployment_left_shift(memory, frame, cell, 1)\ncell, frame = _deployment_sum(memory, frame, cell, scene)\ncell, frame = _deployment_left_shift(memory, frame, cell, 2)\ncell, frame = _deployment_sum(memory, frame, cell, scene)\ncell, frame = _deployment_left_shift(memory, frame, cell, 1)\nframe = first_replace(frame, unit=_deployment_word(frame.unit, cell))\npositions = memory.state.table(16722944)\nframe = first_replace(frame, candidates=positions.cursor())\nscaled_member, frame = _deployment_left_shift(memory, frame, member, 2)\nframe = first_replace(frame, target_x=_deployment_word(frame.target_x, scaled_member))\nframe = first_replace(frame, count=_deployment_word(frame.count, 0))\nframe = _deployment_move_word(memory, frame, 0)\nx_byte = catalog.byte(cell)\nframe = _deployment_move_byte(memory, frame, x_byte)\nx, frame = _deployment_left_shift(memory, frame, x_byte, 3)\nx, frame = _deployment_left_shift(memory, frame, x, 7)\nframe = first_replace(frame, count=_deployment_word(frame.count, x))\npositions.set_word(scaled_member, x)\nframe = _deployment_move_word(memory, frame, x)\nframe = first_replace(frame, count=_deployment_word(frame.count, 0))\nframe = _deployment_move_word(memory, frame, 0)\ny_byte = catalog.byte(cell, 1)\nframe = _deployment_move_byte(memory, frame, y_byte)\ny, frame = _deployment_left_shift(memory, frame, y_byte, 3)\ny, frame = _deployment_left_shift(memory, frame, y, 7)\nframe = first_replace(frame, count=_deployment_word(frame.count, y))\npositions.set_word(scaled_member, y, 2)\nframe = _deployment_move_word(memory, frame, y)\nsource, destination = (roster.cursor(), roster.cursor(2))\nframe = first_replace(frame, roster=source, candidates=destination)\nwhile True:\n    item = source.next_word()\n    frame = first_replace(frame, unit=_deployment_word(frame.unit, item))\n    frame = _deployment_move_word(memory, frame, item)\n    if negative_word(item):\n        break\n    item &= 255\n    frame = first_replace(frame, unit=_deployment_word(frame.unit, item))\n    frame = _deployment_move_word(memory, frame, item)\n    frame = _deployment_compare(memory, frame, item, scaled_member)\n    if item == scaled_member:\n        continue\n    destination.append_word(item)\n    frame = _deployment_move_word(memory, frame, item)\nroster.set_word(0, scaled_member)\nframe = _deployment_move_word(memory, frame, scaled_member)\nframe = first_replace(frame, roster=heads.cursor())\nscene = memory.battle_scene()\nframe = first_replace(frame, target_y=_deployment_word(frame.target_y, scene))\nframe = _deployment_move_word(memory, frame, scene)\nscene_offset, frame = _deployment_left_shift(memory, frame, scene, 1)\nframe = first_replace(frame, target_y=_deployment_word(frame.target_y, scene_offset))\nheads.set_word(scene_offset, scaled_member)\nreturn _deployment_move_word(memory, frame, scaled_member)'}})
APPROVED['business_geometry'].add('read_battlefield_terrain_type_fields')
APPROVED['contexts_first_deployment'] = {'FirstDeploymentFrame', 'FirstDeploymentReturnBoundary', 'first_replace'}
APPROVED['contexts_deployment_terrain'] = {'DeploymentProbeFields', 'DeploymentEdgeFields'}
TERRAIN_DEPLOYMENT_HELPERS = ('_deployment_word', '_deployment_byte', '_deployment_flags', '_deployment_move_word', '_deployment_move_byte', '_deployment_sum', '_deployment_difference', '_deployment_compare', '_deployment_compare_byte', '_deployment_left_shift', '_deployment_right_shift', '_deployment_carry', '_deployment_push', '_deployment_pop', '_deployment_enter', '_deployment_leave', '_deployment_save_probe', '_deployment_restore_probe', '_deployment_terrain_lookup', 'try_place_deployment_cell_fields', '_deployment_probe_call', '_deployment_vacancy_call', 'scan_deployment_first_edge_fields', 'scan_deployment_second_edge_fields', 'promote_first_roster_deployment_candidate_fields', 'promote_second_roster_deployment_candidate_fields')
TERRAIN_DEPLOYMENT_OWNERS = ('try_place_deployment_cell', 'scan_deployment_first_edge', 'scan_deployment_second_edge', 'promote_first_roster_deployment_candidate', 'promote_second_roster_deployment_candidate')

DOMAIN_DECLARATIONS.update({'state_mixed_action_requirement': {'signature': 'draw: ActionRandomDraw, strength: Long, base: Word', 'returns': 'Long', 'flow': 'return state_mixed_action_requirement_fields(FirstDeploymentFrame.unobserved(), draw, strength, base).unit'}})

DOMAIN_DECLARATIONS.update({'compute_type6_budget_from_random_state': {'signature': 'state: GameState, candidate: CandidateBudgetContext', 'returns': 'Long', 'flow': 'state = checked_state(state)\ncandidate = checked_context(candidate, CandidateBudgetContext)\nframe = first_replace(FirstDeploymentFrame.unobserved(), offset_x=candidate.selected)\nreturn compute_type6_budget_from_random_state_fields(BattlePolicyMemory(state), frame).unit', 'slots': {40: ('base', 1, 65535)}}})

DOMAIN_DECLARATIONS.update({'select_action_candidate_by_terrain': {'signature': 'state: GameState, retained: SelectionContext, map_context: Table, policy: ActionTerrainPolicy', 'returns': 'ScoredSelection', 'flow': 'state = checked_state(state)\nretained = checked_context(retained, SelectionContext)\nmap_context = state.checked_table(map_context)\nframe = first_replace(FirstDeploymentFrame.unobserved(), target_x=retained.terrain_carrier, offset_x=retained.selected, roster=map_context.cursor())\nreturned = select_action_candidate_by_terrain_fields(BattlePolicyMemory(state), frame, policy)\nreturn ScoredSelection(returned.distance, returned.offset_x, returned.roster)'}})

DOMAIN_DECLARATIONS.update({'select_strongest_type6_candidate': {'signature': 'state: GameState, retained: SelectionContext', 'returns': 'ScoredSelection', 'flow': 'state = checked_state(state)\nretained = checked_context(retained, SelectionContext)\nframe = first_replace(FirstDeploymentFrame.unobserved(), target_x=retained.terrain_carrier, offset_x=retained.selected)\nreturned = select_strongest_type6_candidate_fields(BattlePolicyMemory(state), frame)\nreturn ScoredSelection(returned.distance, returned.offset_x, returned.roster)'}})

DOMAIN_DECLARATIONS.update({'_deployment_terrain_lookup': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, x: Word, y: Word, continuation: Long=154990', 'returns': 'tuple[FirstDeploymentFrame, Word]', 'flow': "if frame.roster is None:\n    raise ValueError('actual current A0 map required')\nmap_context = frame.roster\nobserved = frame\nframe = _deployment_enter(memory, frame, continuation)\nif frame.stack_cursor is not None:\n    frame = _deployment_push(memory, frame, frame.roster.base)\n    frame = _deployment_push(memory, frame, frame.count)\n    frame = _deployment_push(memory, frame, frame.unit)\n    frame = _deployment_push(memory, frame, frame.target_y)\nsample = read_battlefield_terrain_type_fields(memory, map_context, x, y, frame.target_x).validate(memory.state)\nframe = first_replace(frame, target_x=sample.carrier, roster=sample.lookup.cursor())\nframe = _deployment_flags(memory, frame, (16 if sample.extend else 0) | (8 if sample.category & 128 else 0) | (4 if sample.category == 0 else 0))\nif frame.stack_cursor is None:\n    frame = first_replace(frame, target_y=observed.target_y, unit=observed.unit, count=observed.count, roster=observed.roster)\nelse:\n    frame, target_y = _deployment_pop(memory, frame)\n    frame, unit = _deployment_pop(memory, frame)\n    frame, count = _deployment_pop(memory, frame)\n    frame, roster = _deployment_pop(memory, frame)\n    frame = first_replace(frame, target_y=target_y, unit=unit, count=count, roster=memory.state.table(roster).cursor())\nreturn (_deployment_leave(memory, frame, continuation), sample.category)"}})

DOMAIN_DECLARATIONS.update({'sample_battle_action_random_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:\n    raise ValueError('same-state memory and actual battle action fields required')\nframe.validate(memory.state, frame.stack_cursor is not None)\nframe = _deployment_enter(memory, frame, continuation)\nframe = first_deployment_random_fields(memory, frame)\nmemory.state.sr = memory.state.sr & 65504 | frame.status\nreturn _deployment_leave(memory, frame, continuation)"}})

DOMAIN_DECLARATIONS.update({'_battle_action_map_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame.validate(memory.state, frame.stack_cursor is not None)\nobserved = frame.distance\nif frame.stack_cursor is not None:\n    frame = _deployment_push(memory, frame, observed)\nmap_context = load_battlefield_map_fields(memory)\nframe = first_replace(frame, roster=map_context.cursor())\nif frame.stack_cursor is not None:\n    frame, observed = _deployment_pop(memory, frame)\nframe = first_replace(frame, distance=observed)\nif observed is not None:\n    frame = _contact_status(frame, observed, 32)\nelse:\n    frame = first_replace(frame, status=None)\nreturn frame'}})

DOMAIN_DECLARATIONS.update({'select_action_candidate_by_terrain_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, policy: ActionTerrainPolicy, terrain_return: Long | None=None, training_return: Long | None=None', 'returns': 'FirstDeploymentFrame', 'flow': "if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:\n    raise ValueError('same current candidate memory and fields required')\nif type(policy) is not ActionTerrainPolicy:\n    raise ValueError('original typed terrain policy required')\nstate = memory.state\ncomplete = frame.stack_cursor is not None\nframe.validate(state, complete)\nif complete and (terrain_return, training_return) != (157578, 157592):\n    raise ValueError('actual type6 lookup and training continuations required')\nchecked_policy_table(frame.roster, state)\nframe = first_replace(frame, candidates=state.table(4294955776).cursor(), controller=state.table(4294952960).cursor(), scan=state.table(4294943056).cursor(), distance=0)\nframe = _contact_status(frame, 0, 32)\nframe = first_replace(frame, offset_x=_contact_retained_word(frame.offset_x, 65535))\nframe = _contact_status(frame, 65535, 16)\nwhile True:\n    source = frame.candidates\n    member = source.word()\n    frame = first_replace(frame, candidates=source.advance(2), count=_contact_retained_word(frame.count, member))\n    frame = _contact_status(frame, member, 16)\n    if negative_word(member):\n        return frame.validate(state, complete)\n    member &= 255\n    frame = first_replace(frame, count=_contact_retained_word(frame.count, member))\n    frame = _contact_status(frame, member, 16)\n    frame = first_replace(frame, unit=_contact_retained_word(frame.unit, member))\n    frame = _contact_status(frame, member, 16)\n    offset, frame = _deployment_left_shift(memory, frame, member, 2)\n    frame = first_replace(frame, unit=_contact_retained_word(frame.unit, offset))\n    x = frame.scan.word(offset)\n    frame = first_replace(frame, target_y=_contact_retained_word(frame.target_y, x))\n    frame = _contact_status(frame, x, 16)\n    x, frame = _deployment_right_shift(memory, frame, x, 7)\n    frame = first_replace(frame, target_y=_contact_retained_word(frame.target_y, x))\n    y = frame.scan.word(offset, 2)\n    frame = first_replace(frame, unit=_contact_retained_word(frame.unit, y))\n    frame = _contact_status(frame, y, 16)\n    y, frame = _deployment_right_shift(memory, frame, y, 7)\n    frame = first_replace(frame, unit=_contact_retained_word(frame.unit, y))\n    frame, terrain = _deployment_terrain_lookup(memory, frame, x, y, 157578 if terrain_return is None else terrain_return)\n    if policy.kinds == (6,):\n        frame = _deployment_compare_byte(memory, frame, terrain, 6)\n    if not action_terrain_is_eligible(frame.target_x, policy):\n        continue\n    member = member if frame.count is None else low16(frame.count)\n    frame = first_replace(frame, target_x=_contact_retained_word(frame.target_x, member))\n    frame = _contact_status(frame, member, 16)\n    entered = _deployment_enter(memory, frame, 157592 if training_return is None else training_return)\n    trained = weighted_training_factor_fields(memory, entered, member)\n    frame = _deployment_leave(memory, trained.frame, 157592 if training_return is None else training_return)\n    offset, frame = _deployment_left_shift(memory, frame, low16(frame.target_x), 2)\n    frame = first_replace(frame, target_x=_contact_retained_word(frame.target_x, offset))\n    troops = frame.controller.word(offset, 2)\n    score = low16(frame.target_y) * troops\n    frame = first_replace(frame, target_y=score)\n    frame = _contact_status(frame, score, 32)\n    strongest = frame.distance\n    compared = u32(score - strongest)\n    frame = _contact_status(frame, compared, 32, score < strongest, bool((score ^ strongest) & (score ^ compared) & 2147483648))\n    if is_better_action_score(score, strongest):\n        frame = first_replace(frame, distance=score)\n        frame = _contact_status(frame, score, 32)\n        member = member if frame.count is None else low16(frame.count)\n        frame = first_replace(frame, offset_x=_contact_retained_word(frame.offset_x, member))\n        frame = _contact_status(frame, member, 16)"}})

DOMAIN_DECLARATIONS.update({'select_strongest_type6_candidate_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame.validate(memory.state, frame.stack_cursor is not None)\nframe = _deployment_enter(memory, frame, 157528)\nframe = _battle_action_map_fields(memory, frame)\nframe = _deployment_leave(memory, frame, 157528)\nreturn select_action_candidate_by_terrain_fields(memory, frame, ActionTerrainPolicy((6,)), 157578, 157592)'}})

DOMAIN_DECLARATIONS.update({'state_mixed_action_requirement_fields': {'signature': 'frame: FirstDeploymentFrame, draw: ActionRandomDraw, strength: Long, base: Word', 'returns': 'FirstDeploymentFrame', 'flow': "if type(frame) is not FirstDeploymentFrame or type(draw) is not ActionRandomDraw:\n    raise ValueError('current fields and actual full random-state draw required')\nuint(strength, 32)\nuint(base, 16)\nvalue = draw.sample\nframe = first_replace(frame, target_x=value, target_y=draw.updated_state, unit=strength)\nframe = _contact_status(frame, value, 32)\nprevious = value\nvalue = u32(value << 2)\nframe = first_replace(frame, target_x=value)\nframe = _contact_status(frame, value, 32, bool(previous & 1073741824), False, bool(previous & 1073741824))\nprevious = value\nwide = value + draw.updated_state\nvalue = u32(wide)\nframe = first_replace(frame, target_x=value)\nframe = _contact_status(frame, value, 32, wide > 4294967295, bool(~(previous ^ draw.updated_state) & (previous ^ value) & 2147483648), wide > 4294967295)\nprevious = value\nvalue = u32(value << 1)\nframe = first_replace(frame, target_x=value)\nframe = _contact_status(frame, value, 32, bool(previous & 2147483648), False, bool(previous & 2147483648))\nprevious = value\nwide = value + draw.updated_state\nvalue = u32(wide)\nframe = first_replace(frame, target_x=value)\nframe = _contact_status(frame, value, 32, wide > 4294967295, bool(~(previous ^ draw.updated_state) & (previous ^ value) & 2147483648), wide > 4294967295)\nvalue = u32(value << 16 | value >> 16)\nframe = first_replace(frame, target_x=value)\nframe = _contact_status(frame, value, 32)\nprevious = low16(value)\nwide = previous + base\ndivisor = u16(wide)\nframe = first_replace(frame, target_x=replace_word(value, divisor))\nframe = _contact_status(frame, divisor, 16, wide > 65535, bool(~(previous ^ base) & (previous ^ divisor) & 32768), wide > 65535)\ndivided = divu_retained(strength, divisor)\nrequirement = low16(divided)\nframe = first_replace(frame, unit=requirement)\nreturn _contact_status(frame, requirement, 32)"}})

DOMAIN_DECLARATIONS.update({'compute_type6_budget_from_random_state_fields': {'slots': {40: ('base', 1, 65535)}, 'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame.validate(memory.state, frame.stack_cursor is not None)\nuint(frame.offset_x, 32)\ntroops = memory.state.table(4294952960).cursor()\nframe = first_replace(frame, roster=troops)\noffset, frame = _deployment_left_shift(memory, frame, low16(frame.offset_x), 2)\nframe = first_replace(frame, offset_x=replace_word(frame.offset_x, offset))\nstrength = troops.long(offset)\nframe = first_replace(frame, unit=strength)\nframe = _contact_status(frame, strength, 32)\nframe = sample_battle_action_random_fields(memory, frame, 157626)\ndraw = ActionRandomDraw(low16(frame.target_x), frame.target_y)\nframe = state_mixed_action_requirement_fields(frame, draw, frame.unit, 40)\nmemory.state.write(4294964126, 4, frame.unit)\nframe = _contact_status(frame, frame.unit, 32)\nmemory.state.sr = memory.state.sr & 65504 | frame.status\nreturn frame.validate(memory.state, frame.stack_cursor is not None)'}})

DOMAIN_HELPERS += ('sample_battle_action_random_fields', '_battle_action_map_fields', 'select_action_candidate_by_terrain_fields', 'select_strongest_type6_candidate_fields', 'state_mixed_action_requirement_fields', 'compute_type6_budget_from_random_state_fields')
APPROVED['business_geometry'].update({'_contact_status', '_contact_retained_word', 'load_battlefield_map_fields', 'weighted_training_factor_fields'})
APPROVED.setdefault('business_formation', set()).add('first_deployment_random_fields')

# B13 exact whole supplied field bodies; C13 shared helpers stay sole-owned.
DOMAIN_DECLARATIONS.update({'compute_selected_attribute_budget_second_side': {'signature': 'state: GameState',
                                                   'returns': 'Long',
                                                   'flow': 'state = checked_state(state)\n'
                                                           'frame = '
                                                           'compute_selected_attribute_budget_second_side_fields(BattlePolicyMemory(state), '
                                                           'FirstDeploymentFrame.unobserved())\n'
                                                           'return frame.target_x'},
 'read_selected_action_attributes': {'signature': 'state: GameState',
                                     'returns': 'Word',
                                     'flow': 'state = checked_state(state)\n'
                                             'frame, attributes = '
                                             'read_selected_action_attribute_fields(BattlePolicyMemory(state), '
                                             'FirstDeploymentFrame.unobserved())\n'
                                             'return attributes'}})
DECLARATIONS.update({'build_non_type6_candidates': {'signature': 'state: GameState, retained: SelectionContext',
                                'returns': 'Table',
                                'flow': 'state = checked_state(state)\n'
                                        'retained = checked_context(retained, SelectionContext)\n'
                                        'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                        'target_x=retained.terrain_carrier, target_y=retained.selected)\n'
                                        'frame = '
                                        'build_non_type6_candidates_fields(BattlePolicyMemory(state), '
                                        'frame)\n'
                                        'return state.checked_table(frame.roster)'},
 'build_non_type6_candidates_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'if type(memory) is not BattlePolicyMemory or type(frame) is '
                                               'not FirstDeploymentFrame:\n'
                                               "    raise ValueError('same-state candidate-filter memory and "
                                               "actual frame required')\n"
                                               'frame.validate(memory.state, frame.stack_cursor is not '
                                               'None)\n'
                                               'frame = _deployment_enter(memory, frame, 157336)\n'
                                               'frame = _battle_action_map_fields(memory, frame)\n'
                                               'frame = _deployment_leave(memory, frame, 157336)\n'
                                               'source = memory.state.table(4294955776).cursor()\n'
                                               'unused_troops = memory.state.table(4294952960).cursor()\n'
                                               'positions = memory.state.table(4294943056).cursor()\n'
                                               'destination = memory.state.table(4294956032).cursor()\n'
                                               'frame = first_replace(frame, candidates=source, '
                                               'controller=unused_troops, scan=positions, '
                                               'opponent=destination)\n'
                                               'while True:\n'
                                               '    member = source.next_word()\n'
                                               "    frame = _first_word(frame, 'count', member)\n"
                                               '    if negative_word(member):\n'
                                               '        break\n'
                                               '    member = member & 255\n'
                                               "    frame = _first_word(frame, 'count', member)\n"
                                               "    frame = _first_word(frame, 'unit', member)\n"
                                               "    frame = _first_shift_word(frame, 'unit', member, 2)\n"
                                               '    offset = u16(member << 2)\n'
                                               '    x_fixed = positions.word(offset)\n'
                                               "    frame = _first_word(frame, 'target_y', x_fixed)\n"
                                               "    frame = _first_right_word(frame, 'target_y', x_fixed, "
                                               '7)\n'
                                               '    x = x_fixed >> 7\n'
                                               '    y_fixed = positions.word(offset, 2)\n'
                                               "    frame = _first_word(frame, 'unit', y_fixed)\n"
                                               "    frame = _first_right_word(frame, 'unit', y_fixed, 7)\n"
                                               '    y = y_fixed >> 7\n'
                                               '    frame, terrain = _deployment_terrain_lookup(memory, '
                                               'frame, x, y, 157384)\n'
                                               '    frame = _deployment_compare_byte(memory, frame, terrain, '
                                               '6)\n'
                                               '    if terrain != 6:\n'
                                               '        if frame.count is not None:\n'
                                               '            member = low16(frame.count)\n'
                                               '        destination.append_word(member)\n'
                                               '        frame = _first_memory_word(frame, member)\n'
                                               'destination.put_word(65535)\n'
                                               'frame = _first_memory_word(frame, 65535)\n'
                                               'if frame.status is not None:\n'
                                               '    memory.state.sr = memory.state.sr & 65504 | '
                                               'frame.status\n'
                                               'return frame.validate(memory.state, frame.stack_cursor is '
                                               'not None)'},
 'compute_selected_attribute_budget_second_side_fields': {'signature': 'memory: BattlePolicyMemory, frame: '
                                                                       'FirstDeploymentFrame',
                                                          'returns': 'FirstDeploymentFrame',
                                                          'flow': 'if type(memory) is not BattlePolicyMemory '
                                                                  'or type(frame) is not '
                                                                  'FirstDeploymentFrame:\n'
                                                                  "    raise ValueError('same-state "
                                                                  'action-budget memory and actual frame '
                                                                  "required')\n"
                                                                  'frame.validate(memory.state, '
                                                                  'frame.stack_cursor is not None)\n'
                                                                  'frame, attributes = '
                                                                  'read_selected_action_attribute_fields(memory, '
                                                                  'frame)\n'
                                                                  'frame = _deployment_enter(memory, frame, '
                                                                  '157306)\n'
                                                                  'frame = '
                                                                  'first_deployment_random_fields(memory, '
                                                                  'frame)\n'
                                                                  'frame = _deployment_leave(memory, frame, '
                                                                  '157306)\n'
                                                                  'sample = low16(frame.target_x)\n'
                                                                  'requirement = '
                                                                  'attribute_action_requirement(sample, '
                                                                  'attributes, 8)\n'
                                                                  'frame = first_replace(frame, '
                                                                  'target_y=sample, status=0)\n'
                                                                  "frame = _first_long(frame, 'target_x', "
                                                                  'requirement)\n'
                                                                  'memory.state.write(4294964126, 4, '
                                                                  'requirement)\n'
                                                                  'memory.state.sr = memory.state.sr & 65504 '
                                                                  '| frame.status\n'
                                                                  'return frame.validate(memory.state, '
                                                                  'frame.stack_cursor is not None)',
                                                          'slots': {8: ('base', 1, 8)}},
 'read_selected_action_attribute_fields': {'signature': 'memory: BattlePolicyMemory, frame: '
                                                        'FirstDeploymentFrame',
                                           'returns': 'tuple[FirstDeploymentFrame, Word]',
                                           'flow': 'if type(memory) is not BattlePolicyMemory or type(frame) '
                                                   'is not FirstDeploymentFrame:\n'
                                                   "    raise ValueError('same-state selected attributes and "
                                                   "actual frame required')\n"
                                                   'frame.validate(memory.state, frame.stack_cursor is not '
                                                   'None)\n'
                                                   'attributes_one = '
                                                   'memory.state.table(4294947840).cursor()\n'
                                                   'frame = first_replace(frame, roster=attributes_one)\n'
                                                   'selected = memory.state.read(4294964134, 2)\n'
                                                   "frame = _first_word(frame, 'target_x', selected)\n"
                                                   "frame = _first_shift_word(frame, 'target_x', selected, "
                                                   '1)\n'
                                                   'offset = u16(selected << 1)\n'
                                                   'attributes = attributes_one.word(offset)\n'
                                                   "frame = _first_word(frame, 'unit', attributes)\n"
                                                   'attributes_two = '
                                                   'memory.state.table(4294948352).cursor()\n'
                                                   'frame = first_replace(frame, roster=attributes_two)\n'
                                                   'additional = attributes_two.word(offset)\n'
                                                   "frame = _first_add_word(frame, 'unit', attributes, "
                                                   'additional)\n'
                                                   'attributes = u16(attributes + additional)\n'
                                                   'if frame.status is not None:\n'
                                                   '    memory.state.sr = memory.state.sr & 65504 | '
                                                   'frame.status\n'
                                                   'return (frame, attributes)'},
 'select_lowest_filtered_rating': {'signature': 'state: GameState, retained: RatingContext',
                                   'returns': 'RatingSelection',
                                   'flow': 'state = checked_state(state)\n'
                                           'retained = checked_context(retained, RatingContext)\n'
                                           'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                           'target_x=retained.rating, target_y=retained.selected)\n'
                                           'frame = '
                                           'select_lowest_filtered_rating_fields(BattlePolicyMemory(state), '
                                           'frame)\n'
                                           'return RatingSelection(frame.target_x, frame.target_y)'},
 'select_lowest_filtered_rating_fields': {'signature': 'memory: BattlePolicyMemory, frame: '
                                                       'FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'if type(memory) is not BattlePolicyMemory or type(frame) '
                                                  'is not FirstDeploymentFrame:\n'
                                                  "    raise ValueError('same-state rating memory and actual "
                                                  "field frame required')\n"
                                                  'frame.validate(memory.state, frame.stack_cursor is not '
                                                  'None)\n'
                                                  'uint(frame.target_x, 32)\n'
                                                  'uint(frame.target_y, 32)\n'
                                                  'ratings = memory.state.table(4294951680).cursor()\n'
                                                  'source = memory.state.table(4294956032).cursor()\n'
                                                  'frame = first_replace(frame, roster=ratings, '
                                                  'candidates=source)\n'
                                                  "frame = _first_word(frame, 'target_x', 65535)\n"
                                                  'while True:\n'
                                                  '    member = source.next_word()\n'
                                                  "    frame = _first_word(frame, 'unit', member)\n"
                                                  '    if negative_word(member):\n'
                                                  '        break\n'
                                                  '    member = member & 255\n'
                                                  "    frame = _first_word(frame, 'unit', member)\n"
                                                  '    value = ratings.byte(member)\n'
                                                  "    frame = _first_byte(frame, 'count', value)\n"
                                                  '    if frame.status is not None:\n'
                                                  '        frame = _deployment_compare_byte(memory, frame, '
                                                  'value, low8(frame.target_x))\n'
                                                  '    if value < low8(frame.target_x):\n'
                                                  "        frame = _first_byte(frame, 'target_x', value)\n"
                                                  "        frame = _first_word(frame, 'target_y', member)\n"
                                                  'if frame.status is not None:\n'
                                                  '    memory.state.sr = memory.state.sr & 65504 | '
                                                  'frame.status\n'
                                                  'return frame.validate(memory.state, frame.stack_cursor is '
                                                  'not None)'}})
APPROVED.setdefault('business_formation', set()).update({'_first_right_word', '_first_word', '_first_byte', '_first_memory_word', '_first_shift_word', 'first_deployment_random_fields', '_first_long', '_first_add_word'})
ATTRIBUTE_ACTION_FIELD_HELPERS = ('build_non_type6_candidates_fields', 'compute_selected_attribute_budget_second_side_fields', 'read_selected_action_attribute_fields', 'select_lowest_filtered_rating_fields')

DOMAIN_DECLARATIONS.update({'troop_action_requirement': {'signature': 'sample: Word, strength: Long, multiplier: Word, base: Word', 'returns': 'Long', 'flow': 'uint(sample, 16)\nuint(strength, 32)\nuint(multiplier, 16)\nuint(base, 16)\nif multiplier == 11:\n    return state_mixed_action_requirement_fields(FirstDeploymentFrame.unobserved(), ActionRandomDraw(sample, sample), strength, base).unit\ndivisor = u16(high16(u32(sample * multiplier)) + base)\nreturn low16(divu_retained(strength, divisor))'}})

DOMAIN_DECLARATIONS.update({'compute_candidate_budget_base20': {'signature': 'state: GameState, candidate: CandidateBudgetContext', 'returns': 'Long', 'flow': 'state = checked_state(state)\ncandidate = checked_context(candidate, CandidateBudgetContext)\nframe = first_replace(FirstDeploymentFrame.unobserved(), offset_x=candidate.selected)\nreturn compute_candidate_budget_base20_fields(BattlePolicyMemory(state), frame).unit', 'slots': {20: ('base', 1, 65535)}}})

DOMAIN_DECLARATIONS.update({'compute_candidate_budget_base30': {'signature': 'state: GameState, candidate: CandidateBudgetContext', 'returns': 'Long', 'flow': 'state = checked_state(state)\ncandidate = checked_context(candidate, CandidateBudgetContext)\nframe = first_replace(FirstDeploymentFrame.unobserved(), offset_x=candidate.selected)\nreturn compute_candidate_budget_base30_fields(BattlePolicyMemory(state), frame).unit', 'slots': {30: ('base', 1, 65535)}}})

DOMAIN_DECLARATIONS.update({'select_strongest_open_terrain_candidate_second_side': {'signature': 'state: GameState, retained: SelectionContext', 'returns': 'ScoredSelection', 'flow': 'state = checked_state(state)\nretained = checked_context(retained, SelectionContext)\nframe = first_replace(FirstDeploymentFrame.unobserved(), target_x=retained.terrain_carrier, offset_x=retained.selected)\nreturned = select_strongest_open_terrain_candidate_second_side_fields(BattlePolicyMemory(state), frame)\nreturn ScoredSelection(returned.distance, returned.offset_x, returned.roster)'}})

DOMAIN_DECLARATIONS.update({'select_action_candidate_by_terrain_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, policy: ActionTerrainPolicy, terrain_return: Long | None=None, training_return: Long | None=None, positions_in_controller: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': "if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:\n    raise ValueError('same current candidate memory and fields required')\nif type(policy) is not ActionTerrainPolicy:\n    raise ValueError('original typed terrain policy required')\nstate = memory.state\ncomplete = frame.stack_cursor is not None\nframe.validate(state, complete)\nif type(positions_in_controller) is not bool:\n    raise ValueError('actual candidate pointer-role selector required')\nif complete:\n    uint(terrain_return, 32)\n    uint(training_return, 32)\nchecked_policy_table(frame.roster, state)\nframe = first_replace(frame, candidates=state.table(4294955776).cursor(), controller=state.table(4294943056 if positions_in_controller else 4294952960).cursor(), scan=state.table(4294952960 if positions_in_controller else 4294943056).cursor(), distance=0)\nframe = _contact_status(frame, 0, 32)\nframe = first_replace(frame, offset_x=_contact_retained_word(frame.offset_x, 65535))\nframe = _contact_status(frame, 65535, 16)\nwhile True:\n    source = frame.candidates\n    member = source.word()\n    frame = first_replace(frame, candidates=source.advance(2), count=_contact_retained_word(frame.count, member))\n    frame = _contact_status(frame, member, 16)\n    if negative_word(member):\n        return frame.validate(state, complete)\n    member &= 255\n    frame = first_replace(frame, count=_contact_retained_word(frame.count, member))\n    frame = _contact_status(frame, member, 16)\n    frame = first_replace(frame, unit=_contact_retained_word(frame.unit, member))\n    frame = _contact_status(frame, member, 16)\n    offset, frame = _deployment_left_shift(memory, frame, member, 2)\n    frame = first_replace(frame, unit=_contact_retained_word(frame.unit, offset))\n    positions = frame.controller if positions_in_controller else frame.scan\n    x = positions.word(offset)\n    frame = first_replace(frame, target_y=_contact_retained_word(frame.target_y, x))\n    frame = _contact_status(frame, x, 16)\n    x, frame = _deployment_right_shift(memory, frame, x, 7)\n    frame = first_replace(frame, target_y=_contact_retained_word(frame.target_y, x))\n    y = positions.word(offset, 2)\n    frame = first_replace(frame, unit=_contact_retained_word(frame.unit, y))\n    frame = _contact_status(frame, y, 16)\n    y, frame = _deployment_right_shift(memory, frame, y, 7)\n    frame = first_replace(frame, unit=_contact_retained_word(frame.unit, y))\n    frame, terrain = _deployment_terrain_lookup(memory, frame, x, y, 157578 if terrain_return is None else terrain_return)\n    for kind in policy.kinds:\n        frame = _deployment_compare_byte(memory, frame, terrain, kind)\n        if terrain == kind:\n            break\n    if not action_terrain_is_eligible(frame.target_x, policy):\n        continue\n    member = member if frame.count is None else low16(frame.count)\n    frame = first_replace(frame, target_x=_contact_retained_word(frame.target_x, member))\n    frame = _contact_status(frame, member, 16)\n    entered = _deployment_enter(memory, frame, 157592 if training_return is None else training_return)\n    trained = weighted_training_factor_fields(memory, entered, member)\n    frame = _deployment_leave(memory, trained.frame, 157592 if training_return is None else training_return)\n    offset, frame = _deployment_left_shift(memory, frame, low16(frame.target_x), 2)\n    frame = first_replace(frame, target_x=_contact_retained_word(frame.target_x, offset))\n    troop_table = frame.scan if positions_in_controller else frame.controller\n    troops = troop_table.word(offset, 2)\n    score = low16(frame.target_y) * troops\n    frame = first_replace(frame, target_y=score)\n    frame = _contact_status(frame, score, 32)\n    strongest = frame.distance\n    compared = u32(score - strongest)\n    frame = _contact_status(frame, compared, 32, score < strongest, bool((score ^ strongest) & (score ^ compared) & 2147483648))\n    if is_better_action_score(score, strongest):\n        frame = first_replace(frame, distance=score)\n        frame = _contact_status(frame, score, 32)\n        member = member if frame.count is None else low16(frame.count)\n        frame = first_replace(frame, offset_x=_contact_retained_word(frame.offset_x, member))\n        frame = _contact_status(frame, member, 16)"}})

DOMAIN_DECLARATIONS.update({'select_strongest_open_terrain_candidate_second_side_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame.validate(memory.state, frame.stack_cursor is not None)\nframe = _deployment_enter(memory, frame, 157786)\nframe = _battle_action_map_fields(memory, frame)\nframe = _deployment_leave(memory, frame, 157786)\nreturn select_action_candidate_by_terrain_fields(memory, frame, ActionTerrainPolicy((0, 3, 7, 1)), 157836, 157874, True)'}})

DOMAIN_DECLARATIONS.update({'compute_candidate_budget_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, base: Word, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': 'frame.validate(memory.state, frame.stack_cursor is not None)\nuint(frame.offset_x, 32)\nuint(base, 16)\nuint(continuation, 32)\ntroops = memory.state.table(4294952960).cursor()\nframe = first_replace(frame, roster=troops)\noffset, frame = _deployment_left_shift(memory, frame, low16(frame.offset_x), 2)\nframe = first_replace(frame, offset_x=replace_word(frame.offset_x, offset))\nstrength = troops.long(offset)\nframe = first_replace(frame, unit=strength)\nframe = _contact_status(frame, strength, 32)\nframe = sample_battle_action_random_fields(memory, frame, continuation)\nsample = low16(frame.target_x)\nframe = state_mixed_action_requirement_fields(frame, ActionRandomDraw(sample, sample), frame.unit, base)\nmemory.state.write(4294964126, 4, frame.unit)\nframe = _contact_status(frame, frame.unit, 32)\nmemory.state.sr = memory.state.sr & 65504 | frame.status\nreturn frame.validate(memory.state, frame.stack_cursor is not None)'}})

DOMAIN_DECLARATIONS.update({'compute_candidate_budget_base20_fields': {'slots': {20: ('base', 1, 65535)}, 'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return compute_candidate_budget_fields(memory, frame, 20, 157908)'}})

DOMAIN_DECLARATIONS.update({'compute_candidate_budget_base30_fields': {'slots': {30: ('base', 1, 65535)}, 'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return compute_candidate_budget_fields(memory, frame, 30, 158082)'}})

DOMAIN_HELPERS += ('select_strongest_open_terrain_candidate_second_side_fields', 'compute_candidate_budget_fields', 'compute_candidate_budget_base20_fields', 'compute_candidate_budget_base30_fields')

# B14 exact late-action full fields, shared ranking/math remain sole-owned.
DOMAIN_DECLARATIONS.update({'compute_type1_candidate_budget_base20': {'signature': 'state: GameState, candidate: CandidateBudgetContext',
                                           'returns': 'Long',
                                           'flow': 'state = checked_state(state)\n'
                                                   'candidate = checked_context(candidate, '
                                                   'CandidateBudgetContext)\n'
                                                   'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                                   'offset_x=candidate.selected)\n'
                                                   'frame = '
                                                   'compute_type1_candidate_budget_base20_fields(BattlePolicyMemory(state), '
                                                   'frame)\n'
                                                   'return frame.unit'},
 'compute_type2_candidate_budget_base30': {'signature': 'state: GameState, candidate: CandidateBudgetContext',
                                           'returns': 'Long',
                                           'flow': 'state = checked_state(state)\n'
                                                   'candidate = checked_context(candidate, '
                                                   'CandidateBudgetContext)\n'
                                                   'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                                   'offset_x=candidate.selected)\n'
                                                   'frame = '
                                                   'compute_type2_candidate_budget_base30_fields(BattlePolicyMemory(state), '
                                                   'frame)\n'
                                                   'return frame.unit'},
 'select_strongest_type1_candidate_second_side': {'signature': 'state: GameState, retained: SelectionContext',
                                                  'returns': 'ScoredSelection',
                                                  'flow': 'state = checked_state(state)\n'
                                                          'retained = checked_context(retained, '
                                                          'SelectionContext)\n'
                                                          'frame = '
                                                          'first_replace(FirstDeploymentFrame.unobserved(), '
                                                          'offset_x=retained.selected, '
                                                          'target_x=retained.terrain_carrier)\n'
                                                          'frame = '
                                                          'select_strongest_type1_candidate_second_side_fields(BattlePolicyMemory(state), '
                                                          'frame)\n'
                                                          'return ScoredSelection(frame.distance, '
                                                          'frame.offset_x, '
                                                          'state.checked_table(frame.roster))'},
 'select_strongest_type2_candidate_with_map_context': {'signature': 'state: GameState, retained: '
                                                                    'SelectionContext, map_context: Table',
                                                       'returns': 'ScoredSelection',
                                                       'flow': 'state = checked_state(state)\n'
                                                               'retained = checked_context(retained, '
                                                               'SelectionContext)\n'
                                                               'map_context = '
                                                               'state.checked_table(map_context)\n'
                                                               'frame = '
                                                               'first_replace(FirstDeploymentFrame.unobserved(), '
                                                               'roster=map_context.cursor(), '
                                                               'offset_x=retained.selected, '
                                                               'target_x=retained.terrain_carrier)\n'
                                                               'frame = '
                                                               'select_strongest_type2_candidate_with_map_context_fields(BattlePolicyMemory(state), '
                                                               'frame)\n'
                                                               'return ScoredSelection(frame.distance, '
                                                               'frame.offset_x, '
                                                               'state.checked_table(frame.roster))'}})
DECLARATIONS.update({'compute_type1_candidate_budget_base20_fields': {'signature': 'memory: BattlePolicyMemory, frame: '
                                                               'FirstDeploymentFrame',
                                                  'returns': 'FirstDeploymentFrame',
                                                  'flow': 'return compute_candidate_budget_fields(memory, '
                                                          'frame, 20, 158344)',
                                                  'slots': {20: ('base', 1, 65535)}},
 'compute_type2_candidate_budget_base30_fields': {'signature': 'memory: BattlePolicyMemory, frame: '
                                                               'FirstDeploymentFrame',
                                                  'returns': 'FirstDeploymentFrame',
                                                  'flow': 'return compute_candidate_budget_fields(memory, '
                                                          'frame, 30, 158678)',
                                                  'slots': {30: ('base', 1, 65535)}},
 'select_strongest_type1_candidate_second_side_fields': {'signature': 'memory: BattlePolicyMemory, frame: '
                                                                      'FirstDeploymentFrame',
                                                         'returns': 'FirstDeploymentFrame',
                                                         'flow': 'frame.validate(memory.state, '
                                                                 'frame.stack_cursor is not None)\n'
                                                                 'frame = _deployment_enter(memory, frame, '
                                                                 '158246)\n'
                                                                 'frame = _battle_action_map_fields(memory, '
                                                                 'frame)\n'
                                                                 'frame = _deployment_leave(memory, frame, '
                                                                 '158246)\n'
                                                                 'return '
                                                                 'select_action_candidate_by_terrain_fields(memory, '
                                                                 'frame, ActionTerrainPolicy((1,)), 158296, '
                                                                 '158310, True)'},
 'select_strongest_type2_candidate_with_map_context_fields': {'signature': 'memory: BattlePolicyMemory, '
                                                                           'frame: FirstDeploymentFrame',
                                                              'returns': 'FirstDeploymentFrame',
                                                              'flow': 'frame.validate(memory.state, '
                                                                      'frame.stack_cursor is not None)\n'
                                                                      'checked_policy_table(frame.roster, '
                                                                      'memory.state)\n'
                                                                      'return '
                                                                      'select_action_candidate_by_terrain_fields(memory, '
                                                                      'frame, ActionTerrainPolicy((2,)), '
                                                                      '158630, 158644, True)'},
 'test_actor_map_relative_types': {'signature': 'state: GameState, actor: TerrainActorContext',
                                   'returns': 'CarryOutcome',
                                   'flow': 'state = checked_state(state)\n'
                                           'actor = checked_context(actor, TerrainActorContext)\n'
                                           'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                           'choice=actor.actor, target_x=actor.terrain_carrier)\n'
                                           'frame = '
                                           'test_actor_map_relative_types_fields(BattlePolicyMemory(state), '
                                           'frame)\n'
                                           'return state.carry_result(1 if frame.status & 1 else 0)'},
 'test_actor_map_relative_types_fields': {'signature': 'memory: BattlePolicyMemory, frame: '
                                                       'FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'if type(memory) is not BattlePolicyMemory or type(frame) '
                                                  'is not FirstDeploymentFrame:\n'
                                                  "    raise ValueError('same-state actor terrain memory and "
                                                  "actual frame required')\n"
                                                  'frame.validate(memory.state, frame.stack_cursor is not '
                                                  'None)\n'
                                                  'uint(frame.choice, 32)\n'
                                                  'frame = _deployment_enter(memory, frame, 158516)\n'
                                                  'frame = _battle_action_map_fields(memory, frame)\n'
                                                  'frame = _deployment_leave(memory, frame, 158516)\n'
                                                  'frame = first_replace(frame, '
                                                  'candidates=memory.state.table(4294943056).cursor())\n'
                                                  'actor = low16(frame.choice)\n'
                                                  "frame = _first_word(frame, 'target_x', actor)\n"
                                                  "frame = _first_shift_word(frame, 'target_x', actor, 2)\n"
                                                  'offset = u16(actor << 2)\n'
                                                  'x_fixed = frame.roster.word(offset)\n'
                                                  "frame = _first_word(frame, 'target_y', x_fixed)\n"
                                                  "frame = _first_right_word(frame, 'target_y', x_fixed, 7)\n"
                                                  'x = x_fixed >> 7\n'
                                                  'y_fixed = frame.roster.word(offset, 2)\n'
                                                  "frame = _first_word(frame, 'unit', y_fixed)\n"
                                                  "frame = _first_right_word(frame, 'unit', y_fixed, 7)\n"
                                                  'y = y_fixed >> 7\n'
                                                  'frame, terrain = _deployment_terrain_lookup(memory, '
                                                  'frame, x, y, 158542)\n'
                                                  'frame = _deployment_compare_byte(memory, frame, terrain, '
                                                  '0)\n'
                                                  'if terrain == 0:\n'
                                                  '    return _deployment_carry(memory, frame, '
                                                  'False).validate(memory.state, frame.stack_cursor is not '
                                                  'None)\n'
                                                  'frame = _deployment_compare_byte(memory, frame, terrain, '
                                                  '4)\n'
                                                  'if terrain == 4:\n'
                                                  '    return _deployment_carry(memory, frame, '
                                                  'False).validate(memory.state, frame.stack_cursor is not '
                                                  'None)\n'
                                                  'frame = _deployment_compare_byte(memory, frame, terrain, '
                                                  '7)\n'
                                                  'return _deployment_carry(memory, frame, terrain != '
                                                  '7).validate(memory.state, frame.stack_cursor is not '
                                                  'None)'}})
LATE_TERRAIN_ACTION_FIELD_HELPERS = ('select_strongest_type1_candidate_second_side_fields', 'compute_type1_candidate_budget_base20_fields', 'test_actor_map_relative_types_fields', 'select_strongest_type2_candidate_with_map_context_fields', 'compute_type2_candidate_budget_base30_fields')

DOMAIN_DECLARATIONS.update({'select_lowest_nonzero_rating': {'signature': 'state: GameState, retained: RatingContext', 'returns': 'RatingSelection', 'flow': 'state = checked_state(state)\nretained = checked_context(retained, RatingContext)\nframe = first_replace(FirstDeploymentFrame.unobserved(), target_x=retained.rating, target_y=retained.selected)\nframe = select_lowest_nonzero_rating_fields(BattlePolicyMemory(state), frame)\nreturn RatingSelection(frame.target_x, frame.target_y)'}})

DOMAIN_DECLARATIONS.update({'compute_selected_attribute_budget': {'signature': 'state: GameState', 'returns': 'Long', 'flow': 'state = checked_state(state)\nreturn compute_selected_attribute_budget_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 8).target_x', 'slots': {8: ('base', 1, 8)}}})

DOMAIN_DECLARATIONS.update({'select_strongest_open_terrain_candidate': {'signature': 'state: GameState, retained: SelectionContext', 'returns': 'ScoredSelection', 'flow': 'state = checked_state(state)\nretained = checked_context(retained, SelectionContext)\nframe = first_replace(FirstDeploymentFrame.unobserved(), target_x=retained.terrain_carrier, offset_x=retained.selected)\nframe = select_strongest_open_terrain_candidate_fields(BattlePolicyMemory(state), frame)\nreturn ScoredSelection(frame.distance, frame.offset_x, frame.roster)'}})

DOMAIN_DECLARATIONS.update({'compute_selected_troop_budget_base20': {'signature': 'state: GameState', 'returns': 'Long', 'flow': 'state = checked_state(state)\nreturn compute_selected_troop_budget_base20_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 20).target_y', 'slots': {20: ('base', 1, 65535)}}})

DOMAIN_DECLARATIONS.update({'compute_selected_troop_budget_base30': {'signature': 'state: GameState', 'returns': 'Long', 'flow': 'state = checked_state(state)\nreturn compute_selected_troop_budget_base30_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 30).target_y', 'slots': {30: ('base', 1, 65535)}}})

DOMAIN_DECLARATIONS.update({'select_strongest_type1_candidate': {'signature': 'state: GameState, retained: SelectionContext', 'returns': 'ScoredSelection', 'flow': 'state = checked_state(state)\nretained = checked_context(retained, SelectionContext)\nframe = first_replace(FirstDeploymentFrame.unobserved(), target_x=retained.terrain_carrier, offset_x=retained.selected)\nframe = select_strongest_type1_candidate_fields(BattlePolicyMemory(state), frame)\nreturn ScoredSelection(frame.distance, frame.offset_x, frame.roster)'}})

DOMAIN_DECLARATIONS.update({'compute_then_reload_previous_selected_budget': {'signature': 'state: GameState', 'returns': 'Long', 'flow': 'state = checked_state(state)\nreturn compute_then_reload_previous_selected_budget_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 20).target_y', 'slots': {20: ('base', 1, 65535)}}})

DOMAIN_DECLARATIONS.update({'test_actor_types_0_4_8': {'signature': 'state: GameState, actor: TerrainActorContext', 'returns': 'CarryOutcome', 'flow': 'state = checked_state(state)\nactor = checked_context(actor, TerrainActorContext)\nframe = first_replace(FirstDeploymentFrame.unobserved(), choice=actor.actor, target_x=actor.terrain_carrier)\nframe = test_actor_types_0_4_8_fields(BattlePolicyMemory(state), frame)\nreturn state.carry_result(int(bool(frame.status & 1)))'}})

DOMAIN_DECLARATIONS.update({'select_strongest_type2_candidate': {'signature': 'state: GameState, retained: SelectionContext', 'returns': 'ScoredSelection', 'flow': 'state = checked_state(state)\nretained = checked_context(retained, SelectionContext)\nframe = first_replace(FirstDeploymentFrame.unobserved(), target_x=retained.terrain_carrier, offset_x=retained.selected)\nframe = select_strongest_type2_candidate_fields(BattlePolicyMemory(state), frame)\nreturn ScoredSelection(frame.distance, frame.offset_x, frame.roster)'}})

DOMAIN_DECLARATIONS.update({'compute_selected_type2_budget_base30': {'signature': 'state: GameState', 'returns': 'Long', 'flow': 'state = checked_state(state)\nreturn compute_selected_type2_budget_base30_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 30).target_y', 'slots': {30: ('base', 1, 65535)}}})

DOMAIN_DECLARATIONS.update({'attribute_action_requirement': {'signature': 'sample: Word, attributes: Word, base: Word', 'returns': 'Long', 'flow': "uint(sample, 16)\nuint(attributes, 16)\nuint(base, 16)\nframe = _action_random_factor_fields(FirstDeploymentFrame.unobserved(), ActionRandomDraw(sample, sample), base, 5, 'unit')\nreturn _action_attribute_product_fields(frame, attributes).target_x"}})

DOMAIN_DECLARATIONS.update({'troop_action_requirement': {'signature': 'sample: Word, strength: Long, multiplier: Word, base: Word', 'returns': 'Long', 'flow': 'uint(sample, 16)\nuint(strength, 32)\nuint(multiplier, 16)\nuint(base, 16)\nif multiplier in (10, 11):\n    frame = _action_random_factor_fields(FirstDeploymentFrame.unobserved(), ActionRandomDraw(sample, sample), base, multiplier)\n    return low16(divu_retained(strength, low16(frame.target_x)))\ndivisor = u16(high16(u32(sample * multiplier)) + base)\nreturn low16(divu_retained(strength, divisor))'}})

DOMAIN_DECLARATIONS.update({'state_mixed_action_requirement_fields': {'signature': 'frame: FirstDeploymentFrame, draw: ActionRandomDraw, strength: Long, base: Word', 'returns': 'FirstDeploymentFrame', 'flow': "if type(frame) is not FirstDeploymentFrame or type(draw) is not ActionRandomDraw:\n    raise ValueError('current fields and actual full random-state draw required')\nuint(strength, 32)\nuint(base, 16)\nframe = first_replace(frame, unit=strength)\nframe = _action_random_factor_fields(frame, draw, base)\ndivided = divu_retained(strength, low16(frame.target_x))\nreturn _first_long(frame, 'unit', low16(divided))"}})

DOMAIN_DECLARATIONS.update({'select_lowest_filtered_rating_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return select_action_lowest_rating_fields(memory, frame, False)'}})

DOMAIN_DECLARATIONS.update({'test_actor_map_relative_types_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return test_actor_action_terrain_gate_fields(memory, frame, False)'}})

DOMAIN_DECLARATIONS.update({'_action_child_frame': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:\n    raise ValueError('same-state action memory and actual child frame required')\nreturn frame.validate(memory.state, frame.stack_cursor is not None)"}})

DOMAIN_DECLARATIONS.update({'_action_child_publish': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'if frame.status is not None:\n    memory.state.sr = memory.state.sr & 65504 | frame.status\nreturn frame.validate(memory.state, frame.stack_cursor is not None)'}})

DOMAIN_DECLARATIONS.update({'_action_factor_add_long_fields': {'signature': 'frame: FirstDeploymentFrame, carrier: str, source: Long', 'returns': 'FirstDeploymentFrame', 'flow': "if carrier not in ('target_x', 'target_y', 'unit'):\n    raise ValueError('actual budget-factor LONG destination required')\nleft = uint(frame.carrier(carrier), 32)\nsource = uint(source, 32)\nwide = left + source\nvalue = u32(wide)\nframe = first_replace(frame, **{carrier: value})\nreturn _contact_status(frame, value, 32, wide > 4294967295, bool(~(left ^ source) & (left ^ value) & 2147483648), wide > 4294967295)"}})

DOMAIN_DECLARATIONS.update({'_action_factor_shift_long_fields': {'signature': 'frame: FirstDeploymentFrame, amount: int', 'returns': 'FirstDeploymentFrame', 'flow': "if amount not in (1, 2):\n    raise ValueError('actual action-factor LONG shift required')\nbefore = uint(frame.target_x, 32)\nvalue = u32(before << amount)\ncarry = bool(before & 1 << 32 - amount)\nframe = first_replace(frame, target_x=value)\nreturn _contact_status(frame, value, 32, carry, False, carry)"}})

DOMAIN_DECLARATIONS.update({'_action_random_factor_fields': {'signature': "frame: FirstDeploymentFrame, draw: ActionRandomDraw, base: Word, multiplier: Word=11, scratch: str='target_y'", 'returns': 'FirstDeploymentFrame', 'flow': "if type(frame) is not FirstDeploymentFrame or type(draw) is not ActionRandomDraw:\n    raise ValueError('actual random draw and current factor fields required')\nuint(base, 16)\nif multiplier not in (5, 10, 11) or scratch not in ('target_y', 'unit'):\n    raise ValueError('actual attribute/troop factor role required')\nframe = _first_long(frame, 'target_x', uint(draw.sample, 16))\nframe = _first_long(frame, scratch, uint(draw.updated_state, 32))\nframe = _action_factor_shift_long_fields(frame, 2)\nframe = _action_factor_add_long_fields(frame, 'target_x', frame.carrier(scratch))\nif multiplier != 5:\n    frame = _action_factor_shift_long_fields(frame, 1)\n    if multiplier == 10:\n        frame = _action_factor_add_long_fields(frame, scratch, frame.target_x)\n    else:\n        frame = _action_factor_add_long_fields(frame, 'target_x', frame.carrier(scratch))\nvalue = u32(frame.target_x << 16 | frame.target_x >> 16)\nframe = _first_long(frame, 'target_x', value)\nreturn _first_add_word(frame, 'target_x', low16(value), base)"}})

DOMAIN_DECLARATIONS.update({'_action_attribute_product_fields': {'signature': 'frame: FirstDeploymentFrame, attributes: Word', 'returns': 'FirstDeploymentFrame', 'flow': "uint(attributes, 16)\nreturn _first_long(frame, 'target_x', low16(frame.target_x) * attributes)"}})

DOMAIN_DECLARATIONS.update({'select_action_lowest_rating_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, first_side: bool', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _action_child_frame(memory, frame)\nif type(first_side) is not bool:\n    raise ValueError('actual first/filtered-side rating role required')\nuint(frame.target_x, 32)\nuint(frame.target_y, 32)\nratings = memory.state.table(4294951680).cursor()\nsource = memory.state.table(4294955776 if first_side else 4294956032).cursor()\nframe = first_replace(frame, roster=source if first_side else ratings, candidates=ratings if first_side else source)\nframe = _first_word(frame, 'target_x', 65535)\nif first_side:\n    frame = _first_word(frame, 'target_y', 65535)\nwhile True:\n    member = source.next_word()\n    frame = _first_word(frame, 'unit', member)\n    if negative_word(member):\n        break\n    member &= 255\n    frame = _first_word(frame, 'unit', member)\n    value = ratings.byte(member)\n    frame = _first_byte(frame, 'count', value)\n    if first_side and value == 0:\n        continue\n    if frame.status is not None:\n        frame = _deployment_compare_byte(memory, frame, value, low8(frame.target_x))\n    if value < low8(frame.target_x):\n        frame = _first_byte(frame, 'target_x', value)\n        frame = _first_word(frame, 'target_y', member)\nreturn _action_child_publish(memory, frame)"}})

DOMAIN_DECLARATIONS.update({'select_lowest_nonzero_rating_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return select_action_lowest_rating_fields(memory, frame, True)'}})

DOMAIN_DECLARATIONS.update({'compute_selected_attribute_budget_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, base: Word=8', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _action_child_frame(memory, frame)\nframe = sample_battle_action_random_fields(memory, frame, 155830)\nsample = low16(frame.target_x)\nframe = _action_random_factor_fields(frame, ActionRandomDraw(sample, sample), base, 5, 'unit')\nfirst = memory.state.table(4294947840).cursor()\nframe = first_replace(frame, roster=first)\nselected = memory.state.read(4294964134, 2)\nframe = _first_word(frame, 'unit', selected)\nframe = _first_shift_word(frame, 'unit', selected, 1)\noffset = u16(selected << 1)\nattributes = first.word(offset)\nframe = _first_word(frame, 'count', attributes)\nsecond = memory.state.table(4294948352).cursor()\nframe = first_replace(frame, roster=second)\nadditional = second.word(offset)\nframe = _first_add_word(frame, 'count', attributes, additional)\nframe = _action_attribute_product_fields(frame, u16(attributes + additional))\nmemory.state.write(4294964126, 4, frame.target_x)\nframe = _first_long(frame, 'target_x', frame.target_x)\nreturn _action_child_publish(memory, frame)"}})

DOMAIN_DECLARATIONS.update({'_select_first_side_terrain_action_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, kind: int', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _action_child_frame(memory, frame)\nif kind == 0:\n    map_return, terrain_return, training_return = (156074, 156124, 156162)\n    policy = ActionTerrainPolicy((0, 3, 7, 1))\nelif kind == 1:\n    map_return, terrain_return, training_return = (156542, 156592, 156606)\n    policy = ActionTerrainPolicy((1,))\nelif kind == 2:\n    map_return, terrain_return, training_return = (156886, 156936, 156950)\n    policy = ActionTerrainPolicy((2,))\nelse:\n    raise ValueError('actual first-side open/type1/type2 ranking role required')\nframe = _deployment_enter(memory, frame, map_return)\nframe = _battle_action_map_fields(memory, frame)\nframe = _deployment_leave(memory, frame, map_return)\nframe = select_action_candidate_by_terrain_fields(memory, frame, policy, terrain_return, training_return, True)\nreturn _action_child_publish(memory, frame)"}})

DOMAIN_DECLARATIONS.update({'select_strongest_open_terrain_candidate_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _select_first_side_terrain_action_fields(memory, frame, 0)'}})

DOMAIN_DECLARATIONS.update({'select_strongest_type1_candidate_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _select_first_side_terrain_action_fields(memory, frame, 1)'}})

DOMAIN_DECLARATIONS.update({'select_strongest_type2_candidate_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _select_first_side_terrain_action_fields(memory, frame, 2)'}})

DOMAIN_DECLARATIONS.update({'_compute_first_selected_troop_budget_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, role: int, base: Word', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _action_child_frame(memory, frame)\nif role == 0:\n    continuation, multiplier, reload_previous = (156186, 10, False)\nelif role == 1:\n    continuation, multiplier, reload_previous = (156364, 11, False)\nelif role == 2:\n    continuation, multiplier, reload_previous = (156630, 11, True)\nelif role == 3:\n    continuation, multiplier, reload_previous = (156974, 11, False)\nelse:\n    raise ValueError('actual first-side selected-troop budget role required')\nframe = sample_battle_action_random_fields(memory, frame, continuation)\nsample = low16(frame.target_x)\nframe = _action_random_factor_fields(frame, ActionRandomDraw(sample, sample), base, multiplier)\ntroops = memory.state.table(4294952960).cursor()\nframe = first_replace(frame, roster=troops)\nselected = memory.state.read(4294964134, 2)\nframe = _first_word(frame, 'target_y', selected)\nframe = _first_shift_word(frame, 'target_y', selected, 2)\nstrength = troops.long(u16(selected << 2))\nframe = _first_long(frame, 'target_y', strength)\ndivided = divu_retained(strength, low16(frame.target_x))\nframe = _first_long(frame, 'target_y', low16(divided))\nif reload_previous:\n    frame = _first_long(frame, 'target_y', memory.state.read(4294964126, 4))\nelse:\n    memory.state.write(4294964126, 4, frame.target_y)\n    frame = _first_long(frame, 'target_y', frame.target_y)\nreturn _action_child_publish(memory, frame)"}})

DOMAIN_DECLARATIONS.update({'compute_selected_troop_budget_base20_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, base: Word=20', 'returns': 'FirstDeploymentFrame', 'flow': 'return _compute_first_selected_troop_budget_fields(memory, frame, 0, base)'}})

DOMAIN_DECLARATIONS.update({'compute_selected_troop_budget_base30_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, base: Word=30', 'returns': 'FirstDeploymentFrame', 'flow': 'return _compute_first_selected_troop_budget_fields(memory, frame, 1, base)'}})

DOMAIN_DECLARATIONS.update({'compute_then_reload_previous_selected_budget_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, base: Word=20', 'returns': 'FirstDeploymentFrame', 'flow': 'return _compute_first_selected_troop_budget_fields(memory, frame, 2, base)'}})

DOMAIN_DECLARATIONS.update({'compute_selected_type2_budget_base30_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, base: Word=30', 'returns': 'FirstDeploymentFrame', 'flow': 'return _compute_first_selected_troop_budget_fields(memory, frame, 3, base)'}})

DOMAIN_DECLARATIONS.update({'test_actor_action_terrain_gate_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, first_side: bool', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _action_child_frame(memory, frame)\nif type(first_side) is not bool:\n    raise ValueError('actual first/second actor terrain gate required')\nuint(frame.choice, 32)\nmap_return, terrain_return = (156816, 156842) if first_side else (158516, 158542)\nframe = _deployment_enter(memory, frame, map_return)\nframe = _battle_action_map_fields(memory, frame)\nframe = _deployment_leave(memory, frame, map_return)\npositions = memory.state.table(4294943056).cursor()\nframe = first_replace(frame, candidates=positions)\nactor = low16(frame.choice)\nframe = _first_word(frame, 'target_x', actor)\nframe = _first_shift_word(frame, 'target_x', actor, 2)\ncoordinate_source = positions if first_side else frame.roster\noffset = u16(actor << 2)\nx_fixed = coordinate_source.word(offset)\nframe = _first_word(frame, 'target_y', x_fixed)\nframe = _first_right_word(frame, 'target_y', x_fixed, 7)\ny_fixed = coordinate_source.word(offset, 2)\nframe = _first_word(frame, 'unit', y_fixed)\nframe = _first_right_word(frame, 'unit', y_fixed, 7)\nframe, category = _deployment_terrain_lookup(memory, frame, x_fixed >> 7, y_fixed >> 7, terrain_return)\naccepted = False\nfor kind in (0, 4, 8) if first_side else (0, 4, 7):\n    frame = _deployment_compare_byte(memory, frame, category, kind)\n    if category == kind:\n        accepted = True\n        break\nframe = _deployment_carry(memory, frame, accepted if first_side else not accepted)\nreturn _action_child_publish(memory, frame)"}})

DOMAIN_DECLARATIONS.update({'test_actor_types_0_4_8_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return test_actor_action_terrain_gate_fields(memory, frame, True)'}})

CONTACT_NATIVE_NAMES = ('select_lowest_nonzero_rating', 'compute_selected_attribute_budget', 'select_strongest_open_terrain_candidate', 'compute_selected_troop_budget_base20', 'compute_selected_troop_budget_base30', 'select_strongest_type1_candidate', 'compute_then_reload_previous_selected_budget', 'test_actor_types_0_4_8', 'select_strongest_type2_candidate', 'compute_selected_type2_budget_base30')

APPROVED[(1,'business_formation')] = APPROVED['business_formation']
