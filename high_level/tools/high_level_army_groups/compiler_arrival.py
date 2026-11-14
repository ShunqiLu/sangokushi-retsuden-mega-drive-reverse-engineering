"""Whole semantic-flow admission and ordinary GNU arrival lowering.

This is a deliberately finite compiler family. Every current Python control,
type, import, call and return is consumed; unknown edits are rejected rather
than silently ignored. Runtime inputs are explicit source text only.
"""
import ast
from copy import deepcopy

from .compiler_common import CompileError, Emitter, require_declared_names
from .target import ARRIVAL_BINDINGS


FLOW = r'''
def apply_returning_officer_loyalty(state: ArmyState) -> None:
    sample = u32(state.sample_random() & 65535)
    factor = u16(high16(u32(sample * 5)) + 6)
    status = state.status
    value = u16(104)
    officer = u16(state.selected_officer() & 255)
    value = u16(replace_byte(value, low8(value - status.byte(officer))))
    value = u16(value >> 1)
    affinity = state.affinity
    source = u16(state.loyalty_source() & 255)
    influence = u16(affinity.byte(source))
    value = u32(low16(value) * low16(influence))
    value = u32(low16(value) * low16(factor))
    value = divu_retained(value, 500)
    if low16(value) > 100:
        value = u32((value & 4294901760) | 100)
    status.set_byte(officer, low8(value))


def append_group_from_survivor_roster(state: ArmyState) -> Table:
    packet = state.packed_groups
    assignments = state.city_assignments
    while True:
        count = u16(packet.byte() & 15)
        if count == 0:
            break
        packet = packet.at(count, 13)
    count = u16(0)
    roster = state.survivor_roster.cursor()
    while True:
        selected = roster.next_word()
        if negative_word(selected):
            break
        if not selected & 16384:
            continue
        packet.set_byte(count, low8(selected), 13)
        count = u16(count + 1)
        selected = u16(selected & 255)
        assignments.set_byte(selected, assignments.byte(selected) | 64)
    packet.set_byte(count, 0, 13)
    packet.set_byte(0, low8(count))
    if state.side_flags() & 2:
        force = state.secondary_force()
    else:
        force = state.primary_force()
    packet.set_byte(0, low8(force), 4)
    attributes = state.attributes
    remaining = u16(count - 1)
    total = u32(0)
    attribute = u16(0)
    for member_index in descending_inclusive(remaining):
        attribute = u16(replace_byte(attribute, packet.byte(member_index, 13)))
        attribute = u16(replace_byte(attribute, attributes.byte(attribute)))
        total = u32((total & 4294901760) | u16(low16(total) + attribute))
    total = divu_retained(total, count)
    packet.set_byte(0, low8(total), 3)
    row, column = choose_empty_neighbor_position(state)
    packet.set_byte(0, low8(row), 1)
    packet.set_byte(0, low8(column), 2)
    return packet


def choose_empty_neighbor_position(state: ArmyState) -> tuple[Word, Word]:
    neighbors = state.neighbor_offsets
    costs = state.terrain_cost
    terrain = state.terrain_cells
    selected = u16(state.city() << 2)
    coordinates = state.city_coordinates
    center_row = u16(coordinates.word(selected, 2) >> 4)
    center_column = u16(coordinates.word(selected) >> 4)
    while True:
        row = u16(center_row + neighbors.word())
        if row >= 72:
            neighbors = neighbors.advance(4)
            continue
        column = u16(center_column + neighbors.word(0, 2))
        if column >= 72:
            neighbors = neighbors.advance(4)
            continue
        cell = u16(row << 3)
        cell = u16(cell + row)
        cell = u16(cell << 3)
        cell = u16(cell + column)
        kind = u16(terrain.byte(cell))
        if negative_byte(costs.byte(kind)):
            neighbors = neighbors.advance(4)
            continue
        groups = state.packed_groups
        while True:
            count = u16(groups.byte() & 15)
            if count == 0:
                return row, column
            if low8(row) == groups.byte(0, 1):
                if low8(column) == groups.byte(0, 2):
                    break
            groups = groups.at(count, 13)
        neighbors = neighbors.advance(4)
'''

APPROVED_IMPORTS = {
    'ArmyState', 'Table', 'Word', 'u8', 'u16', 'u32', 'low8', 'low16',
    'high16', 'replace_byte', 'divu_retained', 'negative_byte',
    'negative_word', 'descending_inclusive', 'project_army_arrival_fields',
}

FRAME_ARRIVAL_NAMES = (
    'settle_group_at_city', 'locate_group_city',
    'credit_packed_group_resources', 'erase_group_packet',
    'adjust_battle_losing_loyalty',
)


def _strip_docs(node):
    result = deepcopy(node)
    if (result.body and isinstance(result.body[0], ast.Expr)
            and isinstance(result.body[0].value, ast.Constant)
            and type(result.body[0].value.value) is str):
        result.body.pop(0)
    return result


def _holes(function):
    rules = {}
    if function.name == 'apply_returning_officer_loyalty':
        values = []
        for node in ast.walk(function):
            if (isinstance(node, ast.Compare) and isinstance(node.left, ast.Call)
                    and isinstance(node.left.func, ast.Name) and node.left.func.id == 'low16'
                    and len(node.comparators) == 1 and isinstance(node.comparators[0], ast.Constant)):
                value = node.comparators[0].value
                if type(value) is not int or not 0 <= value <= 65535:
                    raise CompileError('loyalty ceiling must be an unsigned WORD literal')
                values.append(value)
                node.comparators[0] = ast.Name(id='__loyalty_cap', ctx=ast.Load())
            if (isinstance(node, ast.Assign) and len(node.targets) == 1
                    and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'value'
                    and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name)
                    and node.value.func.id == 'u32' and len(node.value.args) == 1
                    and isinstance(node.value.args[0], ast.BinOp) and isinstance(node.value.args[0].op, ast.BitOr)
                    and isinstance(node.value.args[0].right, ast.Constant)):
                value = node.value.args[0].right.value
                if type(value) is not int or not 0 <= value <= 65535:
                    raise CompileError('loyalty saturation must be an unsigned WORD literal')
                values.append(value)
                node.value.args[0].right = ast.Name(id='__loyalty_cap', ctx=ast.Load())
        if len(values) != 2 or len(set(values)) != 1:
            raise CompileError('loyalty comparison and retained WORD saturation must agree')
        rules['loyalty_cap'] = values[0]
        return rules
    if function.name != 'credit_packed_group_resources':
        return rules
    values = []
    for node in ast.walk(function):
        if (isinstance(node, ast.Compare) and isinstance(node.left, ast.Name)
                and node.left.id == 'balance' and len(node.comparators) == 1
                and isinstance(node.comparators[0], ast.Constant)):
            value = node.comparators[0].value
            if type(value) is not int or not 0 <= value <= 4294967295:
                raise CompileError('resource cap must be an unsigned LONG literal')
            values.append(value)
            node.comparators[0] = ast.Name(id='__resource_cap', ctx=ast.Load())
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == 'balance'
                and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
                and node.value.func.id == 'u32'
                and len(node.value.args) == 1
                and isinstance(node.value.args[0], ast.Constant)):
            value = node.value.args[0].value
            if type(value) is not int or not 0 <= value <= 4294967295:
                raise CompileError('resource saturation must be an unsigned LONG literal')
            values.append(value)
            node.value.args[0] = ast.Name(id='__resource_cap', ctx=ast.Load())
    if len(values) != 4 or len(set(values)) != 1:
        raise CompileError('both resource comparisons and saturations must agree')
    rules['resource_cap'] = values[0]
    return rules


def semantic_ir(source):
    if type(source) is not str:
        raise CompileError('explicit semantic text is required')
    try:
        module = _strip_docs(ast.parse(source))
    except SyntaxError as exc:
        raise CompileError('invalid semantic Python') from exc
    functions, imports = {}, set()
    for node in module.body:
        if isinstance(node, ast.ImportFrom):
            if node.level != 1 or node.module != 'domain':
                raise CompileError('only declared domain imports are supported')
            for alias in node.names:
                if alias.asname is not None or alias.name not in APPROVED_IMPORTS:
                    raise CompileError('unsupported imported name')
                imports.add(alias.name)
        elif isinstance(node, ast.FunctionDef):
            if node.name in functions:
                raise CompileError('duplicate operation')
            functions[node.name] = _strip_docs(node)
        else:
            raise CompileError('only domain imports and complete functions are supported')
    expected = {fn.name: fn for fn in ast.parse(FLOW).body}
    # These five public scalar signatures are projections, not the native
    # code authority. Still admit their entire current bodies/imports rather
    # than substituting the historical pre-Frame operations.
    if set(DECLARATIONS) != set(FRAME_ARRIVAL_NAMES):
        raise CompileError('the five exact current arrival projections are required')
    for name, declaration in DECLARATIONS.items():
        text = 'def ' + name + '(' + declaration['signature'] + ')->' + declaration['returns'] + ':\n'
        text += '\n'.join('    ' + line for line in declaration['flow'].splitlines())
        expected[name] = ast.parse(text).body[0]
    if set(functions) != set(expected):
        raise CompileError('all eight complete arrival operations are required')
    require_declared_names(functions, imports)
    records = []
    for name, contract in expected.items():
        function = functions[name]
        normalized = deepcopy(function)
        rules = {} if name in FRAME_ARRIVAL_NAMES else _holes(normalized)
        if name not in FRAME_ARRIVAL_NAMES:
            _holes(contract)
        if ast.dump(normalized, include_attributes=False) != ast.dump(contract, include_attributes=False):
            raise CompileError(name + ': unsupported type, signature, control, call, storage or return')
        effects = []
        for node in ast.walk(function):
            if isinstance(node, (ast.stmt, ast.Call, ast.Compare, ast.BinOp)):
                row = dict(operation=type(node).__name__, semantic=ast.dump(node, include_attributes=False))
                if isinstance(node, ast.Call):
                    name_ = node.func.attr if isinstance(node.func, ast.Attribute) else node.func.id if isinstance(node.func, ast.Name) else ''
                    row['ordered_live_operation'] = name_
                    width = {'byte':8,'set_byte':8,'next_byte':8,'append_byte':8,'low8':8,'u8':8,
                             'word':16,'set_word':16,'next_word':16,'low16':16,'u16':16,
                             'long':32,'set_long':32,'u32':32}.get(name_)
                    if width is not None:
                        row['value_bits'] = width
                effects.append(row)
        records.append(dict(name=name, rules=rules, effects=effects))
    return records


def _view(e, address, register, absolute_long=False):
    e.ins('lea.l', f'0x{address:x}:{"l" if absolute_long else "w"},%{register}', 6 if absolute_long else 4)


def _packet_amount(e, start):
    e.ins('move.b', f'{start}(%a0),%d0', 4)
    e.ins('lsl.w', '#8,%d0')
    e.ins('move.b', f'{start+1}(%a0),%d0', 4)
    e.ins('lsl.l', '#8,%d0')
    e.ins('move.b', f'{start+2}(%a0),%d0', 4)
    e.ins('lsl.l', '#8,%d0')
    e.ins('move.b', f'{start+3}(%a0),%d0', 4)


def _credit_cap(e, cap):
    done = e.fresh('within_resource_limit')
    e.ins('cmpi.l', f'#{cap},%d1', 6)
    e.ins('bls.w', done, 4)
    e.ins('move.l', f'#{cap},%d1', 6)
    e.label(done)


def _settle(e, rules):
    done, assign = e.fresh('arrival_done'), e.fresh('assign_member')
    e.ins('tst.l', '0xff382c:l', 6)
    e.ins('beq.w', done, 4)
    e.ins('movea.l', '0xff382c:l,%a0', 6)
    e.ins('clr.w', '%d0')
    e.ins('move.b', '1(%a0),%d0', 4)
    e.ins('clr.w', '%d1')
    e.ins('move.b', '2(%a0),%d1', 4)
    e.ins('jsr', 'terrain_cell_query:l', 6)
    e.ins('tst.b', '%d3')
    e.ins('bpl.w', done, 4)
    e.ins('bsr.w', 'locate_group_city', 4)
    e.ins('move.b', '(%a0),%d0')
    e.ins('andi.w', '#15,%d0', 4)
    e.ins('subq.w', '#1,%d0')
    _view(e, 0xcc00, 'a1')
    e.label(assign)
    e.ins('clr.w', '%d1')
    e.ins('move.b', '13(%a0,%d0.w),%d1', 4)
    e.ins('move.b', '%d3,(%a1,%d1.w)', 4)
    e.ins('dbra', '%d0,' + assign, 4)
    e.ins('bsr.w', 'credit_packed_group_resources', 4)
    e.ins('bsr.w', 'erase_group_packet', 4)
    e.label(done)


def _locate(e, rules):
    scan, following, done = e.fresh('city_scan'), e.fresh('next_city'), e.fresh('city_found')
    e.ins('clr.w', '%d0')
    e.ins('move.b', '1(%a0),%d0', 4)
    e.ins('lsl.w', '#4,%d0')
    e.ins('addq.w', '#8,%d0')
    e.ins('clr.w', '%d1')
    e.ins('move.b', '2(%a0),%d1', 4)
    e.ins('lsl.w', '#4,%d1')
    e.ins('move.w', '%d1,%d2')
    e.ins('subi.w', '#16,%d2', 4)
    _view(e, 0xd4aca, 'a1', True)
    e.ins('move.w', '#1,%d3', 4)
    e.label(scan)
    e.ins('cmp.w', '2(%a1),%d0', 4)
    e.ins('bne.w', following, 4)
    e.ins('cmp.w', '(%a1),%d1')
    e.ins('beq.w', done, 4)
    e.ins('cmp.w', '2(%a1),%d2', 4)
    e.ins('beq.w', done, 4)
    e.label(following)
    e.ins('addq.w', '#4,%a1')
    e.ins('addq.w', '#1,%d3')
    e.ins('bra.b', scan)
    e.label(done)


def _credit(e, rules):
    e.ins('lsl.w', '#2,%d3')
    for start, address in ((5, 0xdffc), (9, 0xe09c)):
        _packet_amount(e, start)
        _view(e, address, 'a1')
        e.ins('move.l', '(%a1,%d3.w),%d1', 4)
        e.ins('add.l', '%d0,%d1')
        _credit_cap(e, rules['resource_cap'])
        e.ins('move.l', '%d1,(%a1,%d3.w)', 4)


def _erase(e, rules):
    copy, done = e.fresh('copy_following_packet'), e.fresh('packet_end')
    e.ins('move.b', '(%a0),%d0')
    e.ins('andi.w', '#15,%d0', 4)
    e.ins('lea.l', '13(%a0,%d0.w),%a1', 4)
    e.ins('move.b', '(%a1),%d0')
    e.ins('andi.w', '#15,%d0', 4)
    e.ins('beq.w', done, 4)
    e.ins('addi.w', '#12,%d0', 4)
    e.label(copy)
    e.ins('move.b', '(%a1)+,(%a0)+')
    e.ins('dbra', '%d0,' + copy, 4)
    e.label(done)
    e.ins('clr.b', '(%a0)')


def _loyalty_change(e, address, done=None):
    store = e.fresh('loyalty_store')
    e.ins('move.w', f'0xffff{address:04x}:l,%d1', 6)
    e.ins('clr.w', '%d2')
    e.ins('move.b', '(%a0,%d1.w),%d2', 4)
    e.ins('sub.w', '%d0,%d2')
    e.ins('bcc.w', store, 4)
    e.ins('clr.w', '%d2')
    e.label(store)
    e.ins('move.b', '%d2,(%a0,%d1.w)', 4)
    if done is not None:
        e.ins('bra.w', done, 4)


def _losing(e, rules):
    second, done = e.fresh('secondary_loser'), e.fresh('loyalty_done')
    e.ins('jsr', 'random_sample:l', 6)
    e.ins('andi.l', '#65535,%d0', 6)
    e.ins('move.l', '%d0,%d1')
    e.ins('lsl.l', '#1,%d0')
    e.ins('add.l', '%d1,%d0')
    e.ins('swap', '%d0')
    e.ins('addq.w', '#1,%d0')
    _view(e, 0xc500, 'a0')
    e.ins('cmpi.w', '#5,0xffff8114:l', 8)
    e.ins('beq.w', second, 4)
    e.ins('cmpi.w', '#4,0xffff8114:l', 8)
    e.ins('bne.w', done, 4)
    _loyalty_change(e, 0x80e0, done)
    e.label(second)
    _loyalty_change(e, 0x80e2)
    e.label(done)


def _returning(e, rules):
    store = e.fresh('returning_status_store')
    e.ins('movem.l', '%d0-%d4/%a0-%a1,-(%a7)', 4)
    e.ins('jsr', 'random_sample:l', 6)
    e.ins('andi.l', '#65535,%d0', 6)
    e.ins('move.l', '%d0,%d1')
    e.ins('lsl.l', '#2,%d0')
    e.ins('add.l', '%d1,%d0')
    e.ins('swap', '%d0')
    e.ins('addi.w', '#6,%d0', 4)
    _view(e, 0xc300, 'a0')
    e.ins('move.w', '#104,%d1', 4)
    e.ins('move.w', '0xf3a6:w,%d2', 4)
    e.ins('andi.w', '#255,%d2', 4)
    e.ins('sub.b', '(%a0,%d2.w),%d1', 4)
    e.ins('lsr.w', '#1,%d1')
    _view(e, 0xc200, 'a1')
    e.ins('move.w', '0xf3f2:w,%d4', 4)
    e.ins('andi.w', '#255,%d4', 4)
    e.ins('clr.w', '%d3')
    e.ins('move.b', '(%a1,%d4.w),%d3', 4)
    e.ins('mulu.w', '%d3,%d1')
    e.ins('mulu.w', '%d0,%d1')
    e.ins('divu.w', '#500,%d1', 4)
    e.ins('cmpi.w', f"#{rules['loyalty_cap']},%d1", 4)
    e.ins('bls.w', store, 4)
    e.ins('move.w', f"#{rules['loyalty_cap']},%d1", 4)
    e.label(store)
    e.ins('move.b', '%d1,(%a0,%d2.w)', 4)
    e.ins('movem.l', '(%a7)+,%d0-%d4/%a0-%a1', 4)


def _append(e, rules):
    scan = e.fresh('find_packet_end')
    roster = e.fresh('survivor_roster')
    roster_done = e.fresh('roster_done')
    end = e.fresh('packet_found')
    second, force_done = e.fresh('secondary_force'), e.fresh('force_selected')
    average = e.fresh('attribute_average')
    _view(e, 0x9000, 'a0')
    _view(e, 0xcc00, 'a2')
    e.label(scan)
    e.ins('move.b', '(%a0),%d0')
    e.ins('andi.w', '#15,%d0', 4)
    e.ins('beq.w', end, 4)
    e.ins('lea.l', '13(%a0,%d0.w),%a0', 4)
    e.ins('bra.b', scan)
    e.label(end)
    e.ins('clr.w', '%d0')
    _view(e, 0xaf56, 'a1')
    e.label(roster)
    e.ins('move.w', '(%a1)+,%d1')
    e.ins('bmi.w', roster_done, 4)
    e.ins('btst.l', '#14,%d1', 4)
    e.ins('beq.b', roster)
    e.ins('move.b', '%d1,13(%a0,%d0.w)', 4)
    e.ins('addq.w', '#1,%d0')
    e.ins('andi.w', '#255,%d1', 4)
    e.ins('bset.b', '#6,(%a2,%d1.w)', 6)
    e.ins('bra.b', roster)
    e.label(roster_done)
    e.ins('clr.b', '13(%a0,%d0.w)', 4)
    e.ins('move.b', '%d0,(%a0)')
    e.ins('btst.b', '#1,0xf6d7:w', 6)
    e.ins('bne.w', second, 4)
    e.ins('move.w', '0xf68c:w,%d1', 4)
    e.ins('bra.w', force_done, 4)
    e.label(second)
    e.ins('move.w', '0xf68e:w,%d1', 4)
    e.label(force_done)
    e.ins('move.b', '%d1,4(%a0)', 4)
    _view(e, 0xc400, 'a1')
    e.ins('move.w', '%d0,%d1')
    e.ins('subq.w', '#1,%d1')
    e.ins('moveq', '#0,%d2')
    e.ins('clr.w', '%d3')
    e.label(average)
    e.ins('move.b', '13(%a0,%d1.w),%d3', 4)
    e.ins('move.b', '(%a1,%d3.w),%d3', 4)
    e.ins('add.w', '%d3,%d2')
    e.ins('dbra', '%d1,' + average, 4)
    e.ins('divu.w', '%d0,%d2')
    e.ins('move.b', '%d2,3(%a0)', 4)
    e.ins('bsr.w', 'choose_empty_neighbor_position', 4)
    e.ins('move.b', '%d0,1(%a0)', 4)
    e.ins('move.b', '%d1,2(%a0)', 4)


def _choose(e, rules):
    next_neighbor, neighbor, group, done = (e.fresh(n) for n in ('next_neighbor','candidate_neighbor','packed_collision','position_free'))
    displacement = 0x21f82 - (e.pc + 2)
    e.ins('lea.l', f'{displacement}(%pc),%a6', 4)
    _view(e, 0x670a, 'a5', True)
    _view(e, 0xee5f0, 'a4', True)
    e.ins('move.w', '0xf68a:w,%d0', 4)
    e.ins('lsl.w', '#2,%d0')
    _view(e, 0xd4ac6, 'a1', True)
    e.ins('move.w', '2(%a1,%d0.w),%d7', 4)
    e.ins('lsr.w', '#4,%d7')
    e.ins('move.w', '0(%a1,%d0.w),%d6', 4)
    e.ins('lsr.w', '#4,%d6')
    e.label(neighbor)
    e.ins('move.w', '%d7,%d0')
    e.ins('add.w', '(%a6),%d0')
    e.ins('cmpi.w', '#72,%d0', 4)
    e.ins('bcc.w', next_neighbor, 4)
    e.ins('move.w', '%d6,%d1')
    e.ins('add.w', '2(%a6),%d1', 4)
    e.ins('cmpi.w', '#72,%d1', 4)
    e.ins('bcc.w', next_neighbor, 4)
    e.ins('move.w', '%d0,%d2')
    e.ins('lsl.w', '#3,%d2')
    e.ins('add.w', '%d0,%d2')
    e.ins('lsl.w', '#3,%d2')
    e.ins('add.w', '%d1,%d2')
    e.ins('clr.w', '%d3')
    e.ins('move.b', '(%a4,%d2.w),%d3', 4)
    e.ins('tst.b', '(%a5,%d3.w)', 4)
    e.ins('bmi.b', next_neighbor)
    _view(e, 0x9000, 'a1')
    e.label(group)
    e.ins('move.b', '(%a1),%d2')
    e.ins('andi.w', '#15,%d2', 4)
    e.ins('beq.w', done, 4)
    e.ins('cmp.b', '1(%a1),%d0', 4)
    no_collision = e.fresh('different_row')
    e.ins('bne.w', no_collision, 4)
    e.ins('cmp.b', '2(%a1),%d1', 4)
    e.ins('beq.w', next_neighbor, 4)
    e.label(no_collision)
    e.ins('lea.l', '13(%a1,%d2.w),%a1', 4)
    e.ins('bra.b', group)
    e.label(next_neighbor)
    e.ins('adda.w', '#4,%a6', 4)
    e.ins('bra.b', neighbor)
    e.label(done)


LOWERERS = {
    'settle_group_at_city': _settle,
    'locate_group_city': _locate,
    'credit_packed_group_resources': _credit,
    'erase_group_packet': _erase,
    'adjust_battle_losing_loyalty': _losing,
    'apply_returning_officer_loyalty': _returning,
    'append_group_from_survivor_roster': _append,
    'choose_empty_neighbor_position': _choose,
}


def _frame_arrival_records(complete_city_source):
    """Admit the whole current Scene catalog before selecting its five bodies."""
    from ..high_level_remaining_flows.compiler_city import (
        DECLARATIONS as CITY_DECLARATIONS, APPROVED as CITY_APPROVED,
    )
    from ..high_level_remaining_flows.compiler_common import (
        semantic_functions, CompileError as SceneCompileError,
    )
    try:
        records = semantic_functions(complete_city_source, CITY_DECLARATIONS, CITY_APPROVED)
    except SceneCompileError as error:
        raise CompileError('complete current arrival Frame source: ' + str(error)) from error
    if any(name + '_fields' not in records for name in FRAME_ARRIVAL_NAMES):
        raise CompileError('all five complete current arrival Frame bodies are required')
    return records


def _credit_frame_rules(complete_city_source):
    """Read the admitted cap from its compare, branch and saturation operands."""
    function = next(node for node in ast.parse(complete_city_source).body
        if isinstance(node, ast.FunctionDef) and node.name == 'credit_packed_group_resources_fields')
    values = []
    for node in ast.walk(function):
        if (isinstance(node, ast.Compare) and len(node.ops) == 1 and isinstance(node.ops[0], ast.Gt)
                and isinstance(node.left, ast.Attribute) and node.left.attr == 'target_y'
                and len(node.comparators) == 1 and isinstance(node.comparators[0], ast.Constant)):
            values.append(node.comparators[0].value)
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
            continue
        if node.func.id == '_first_compare_long' and len(node.args) == 3:
            if isinstance(node.args[-1], ast.Constant):
                values.append(node.args[-1].value)
        elif node.func.id == '_movement_move_long' and len(node.args) == 4:
            if isinstance(node.args[-1], ast.Constant):
                values.append(node.args[-1].value)
    if (len(values) != 3 or any(type(value) is not int or not 0 <= value <= 0xFFFFFFFF for value in values)
            or len(set(values)) != 1):
        raise CompileError('admitted Frame resource compare and saturation must share one LONG cap')
    return {'resource_cap': values[0]}


def compile_arrival(source, *, complete_city_source):
    """Lower eight current bodies, using actual full Frames for the five projections."""
    records = semantic_ir(source)
    frame_records = _frame_arrival_records(complete_city_source)
    credit_rules = _credit_frame_rules(complete_city_source)
    bindings = {binding.name: binding for binding in ARRIVAL_BINDINGS}
    if set(bindings) != set(LOWERERS):
        raise CompileError('eight target ABI bindings are required')
    units = []
    for record in records:
        if record['name'] in FRAME_ARRIVAL_NAMES:
            frame_record = frame_records[record['name'] + '_fields']
            record = dict(record, effects=frame_record['effects'],
                rules=credit_rules if record['name'] == 'credit_packed_group_resources' else {})
        emitter = Emitter(bindings[record['name']])
        emitter.begin()
        LOWERERS[record['name']](emitter, record['rules'])
        emitter.end()
        unit = emitter.unit(record['effects'])
        if sum(i['encoding_bytes'] for i in unit['instructions']) != bindings[record['name']].end - bindings[record['name']].entry:
            raise CompileError(record['name'] + ': fixed complete extent exceeded')
        units.append(unit)
    allocated = sum(sum(i['encoding_bytes'] for i in u['instructions']) for u in units)
    instructions = sum(len(u['instructions']) for u in units)
    if (allocated, instructions) != (758, 221):
        raise CompileError('complete eight-unit arrival allocation is required')
    return dict(units=units, allocated_bytes=allocated, instructions=instructions,
                complete_current_catalog_admitted=True,
                complete_frame_arrival_names=list(FRAME_ARRIVAL_NAMES),
                complete_scene_catalog_count=len(frame_records),
                scalar_projection_is_not_complete_Frame=True,
                original_generation_input=False, complete_CPU=False)

# Exact current C23 projection bodies. Native effects come from the admitted
# complete Scene owners above; the three remaining scalar bodies use FLOW.
DECLARATIONS = {}

DECLARATIONS.update({'settle_group_at_city': {'signature': 'state: ArmyState', 'returns': 'None', 'flow': 'project_army_arrival_fields(state, 119740)'}})

DECLARATIONS.update({'locate_group_city': {'signature': 'state: ArmyState, packet: Table', 'returns': 'Word', 'flow': 'frame = project_army_arrival_fields(state, 119820, packet)\nreturn low16(frame.count)'}})

DECLARATIONS.update({'credit_packed_group_resources': {'signature': 'state: ArmyState, packet: Table, city: Word', 'returns': 'None', 'flow': 'project_army_arrival_fields(state, 119884, packet, city)'}})

DECLARATIONS.update({'erase_group_packet': {'signature': 'state: ArmyState, packet: Table', 'returns': 'Table', 'flow': 'frame = project_army_arrival_fields(state, 119992, packet)\nreturn state.table(frame.roster.base)'}})

DECLARATIONS.update({'adjust_battle_losing_loyalty': {'signature': 'state: ArmyState', 'returns': 'None', 'flow': 'project_army_arrival_fields(state, 120026)'}})
