"""Complete structured-flow admission and ordinary GNU city lowering.

The control/storage contract below is semantic Python, not an original opcode
table. Runtime generation receives source text only. Every expression, call,
annotation and return is consumed; unsupported edits fail closed.
"""
import ast
from copy import deepcopy
from dataclasses import asdict

from .compiler_common import CompileError, Emitter, require_declared_names
from .target import CITY_BINDINGS


FLOW = '''
def commit_tax_rate(state: GameState) -> None:
    orders = state.city_tax_orders
    city = u16(state.chosen_city() << 2)
    orders.set_word(city, 0)
    orders.set_word(city, state.tax_rate(), 2)


def debit_city_gold(state: GameState) -> None:
    city = u16(state.chosen_city() << 2)
    gold = state.city_gold
    amount = state.order_amount()
    gold.set_long(city, u32(gold.long(city) - amount))


def schedule_transport_debit(state: GameState) -> None:
    city = u16(state.selected_city() << 2)
    orders = state.transport_orders
    kind = u16(state.transport_choice() + 1)
    orders.set_byte(city, low8(kind) | 16)
    coordinates = state.city_coordinates
    selected = u16(state.selected_city() << 2)
    y = u16(coordinates.word(selected, 2) >> 4)
    orders.set_byte(city, low8(y), 1)
    x = u16(coordinates.word(selected) >> 4)
    orders.set_byte(city, low8(x), 2)
    orders.set_byte(city, state.chosen_city_tail(), 3)
    selected = u16(state.selected_city() << 2)
    gold = state.city_gold
    rice = state.city_rice
    choice = u16(state.transport_choice() << 3)
    costs = state.transport_costs
    remaining = gold.long(selected)
    remaining = u32(remaining - costs.long(choice))
    gold.set_long(selected, remaining)
    remaining = rice.long(selected)
    remaining = u32(remaining - costs.long(choice, 4))
    rice.set_long(selected, remaining)


def commit_mutual_relationship(state: GameState) -> None:
    target = u16(state.relationship_target() << 1)
    targets = state.relationship_targets
    bit = targets.word(target)
    force = u16(state.current_force() << 1)
    relations = state.force_relationships
    flags = relations.word(force)
    flags = u32(flags | (1 << (bit & 31)))
    relations.set_word(force, u16(flags))
    target = u16(state.relationship_target() << 1)
    targets = state.relationship_targets
    target = targets.word(target)
    target = u16(target << 1)
    bit = state.current_force()
    relations = state.force_relationships
    flags = relations.word(target)
    flags = u32(flags | (1 << (bit & 31)))
    relations.set_word(target, u16(flags))


def commit_equipment_purchase(state: GameState) -> None:
    choice = u16(state.equipment_choice() << 2)
    prices = state.equipment_prices
    price = prices.long(choice)
    city = u16(state.chosen_city() << 2)
    gold = state.city_gold
    gold.set_long(city, u32(gold.long(city) - price))
    equipment = state.officer_equipment
    slot = u16(state.selected_officer() << 1)
    slot = u16(slot + state.selected_officer())
    slot = u16(slot + state.equipment_choice())
    choice = u16(state.equipment_choice() << 1)
    levels = state.equipment_levels
    level = u16(levels.word(choice) + 1)
    equipment.set_byte(slot, low8(level))
    state.set_command_mode(state.requested_mode())
    state.set_command_step(40)
    state.set_command_result(98)
    state.set_command_officer(state.selected_officer())
    state.set_command_active(1)
    state.set_scene_selector(9)


def add_selected_cost(state: GameState) -> None:
    selected = u16(state.selected_cost() << 2)
    costs = state.selected_costs
    total = costs.long(selected)
    total = u32(total + state.current_cost())
    if total <= state.cost_limit():
        state.set_current_cost(total)


def add_packet_city_resources(state: GameState, city: Word, packet: Table) -> None:
    city = u16(city)
    index = u16(city << 2)
    gold = state.city_gold
    amount = u32(packet.byte(0, 5) << 24)
    amount = u32(amount | (packet.byte(0, 6) << 16))
    amount = u32(amount | (packet.byte(0, 7) << 8))
    amount = u32(amount | packet.byte(0, 8))
    balance = gold.long(index)
    total = u32(amount + balance)
    if amount + balance > 4294967295 or total > 999999:
        total = u32(999999)
    gold.set_long(index, total)
    amount = u32(packet.byte(0, 9) << 24)
    amount = u32(amount | (packet.byte(0, 10) << 16))
    amount = u32(amount | (packet.byte(0, 11) << 8))
    amount = u32(amount | packet.byte(0, 12))
    rice = state.city_rice
    balance = rice.long(index)
    total = u32(amount + balance)
    if amount + balance > 4294967295 or total > 999999:
        total = u32(999999)
    rice.set_long(index, total)


def add_packet_city_resources_wrapped(state: GameState, city: Word, packet: Table) -> None:
    city = u16(city)
    index = u16(city << 2)
    amount = u32(packet.byte(0, 5) << 24)
    amount = u32(amount | (packet.byte(0, 6) << 16))
    amount = u32(amount | (packet.byte(0, 7) << 8))
    amount = u32(amount | packet.byte(0, 8))
    gold = state.city_gold
    total = u32(gold.long(index) + amount)
    if total > 999999:
        total = u32(999999)
    gold.set_long(index, total)
    amount = u32(packet.byte(0, 9) << 24)
    amount = u32(amount | (packet.byte(0, 10) << 16))
    amount = u32(amount | (packet.byte(0, 11) << 8))
    amount = u32(amount | packet.byte(0, 12))
    rice = state.city_rice
    total = u32(rice.long(index) + amount)
    if total > 999999:
        total = u32(999999)
    rice.set_long(index, total)


def transport_direction_or_arrival(state: GameState, packet: Table) -> CarryOutcome:
    route = state.route_bytes.at(state.route_offset())
    state.set_route_offset(u16(state.route_offset() + 1))
    if not negative_byte(route.byte(0, 1)):
        direction = u8(route.byte())
        direction = u8(direction - 1)
        if direction == 0:
            delta_x, delta_y = u16(65520), u16(0)
        else:
            direction = u8(direction - 1)
            if direction == 0:
                delta_x, delta_y = u16(0), u16(16)
            else:
                direction = u8(direction - 1)
                if direction == 0:
                    delta_x, delta_y = u16(16), u16(0)
                else:
                    delta_x, delta_y = u16(0), u16(65520)
        state.set_route_x(u16(state.route_x() + delta_x))
        state.set_route_y(u16(state.route_y() + delta_y))
        return state.carry_result(0)
    kind = u16(packet.byte() & 3)
    kind = u16(kind << 3)
    city = u16(packet.byte(0, 3) << 2)
    awards = state.transport_awards
    credit = awards.long(kind)
    gold = state.city_gold
    total = u32(credit + gold.long(city))
    if total > 999999:
        total = u32(999999)
    gold.set_long(city, total)
    credit = awards.long(kind, 4)
    rice = state.city_rice
    total = u32(credit + rice.long(city))
    if total > 999999:
        total = u32(999999)
    rice.set_long(city, total)
    packet.set_byte(0, 0)
    return state.carry_result(1)


def transport_collision(state: GameState) -> CarryOutcome:
    x = u16(state.route_x() >> 4)
    y = u16(state.route_y() >> 4)
    objects = state.transport_objects
    for remaining in descending_inclusive(u16(39)):
        if objects.byte() != 0:
            if not objects.byte() & 16:
                if low8(x) == objects.byte(0, 1):
                    if low8(y) == objects.byte(0, 2):
                        return state.carry_result(1)
        objects = objects.advance(4)
    objects = state.packed_objects
    while True:
        length = u16(objects.byte() & 15)
        if length == 0:
            return state.carry_result(0)
        if low8(x) == objects.byte(0, 1):
            if low8(y) == objects.byte(0, 2):
                return state.carry_result(1)
        objects = objects.at(length, 13)


def snapshot_city_resources(state: GameState) -> None:
    gold = state.city_gold
    city = u16(state.tail_city() << 2)
    state.set_snapshot_gold(gold.long(city))
    rice = state.city_rice
    state.set_snapshot_rice(rice.long(city))


def load_city_ed84_ee24_longs(state: GameState) -> None:
    first = state.city_ed84
    city = u16(state.tail_city() << 2)
    state.set_city_snapshot_ed84(first.long(city))
    second = state.city_ee24
    state.set_city_snapshot_ee24(second.long(city))


def commit_relationship_resource_credit(state: GameState) -> None:
    force = state.current_force()
    target = state.selected_officer()
    relations = state.force_relationships
    force = u16(force << 1)
    flags = relations.word(force)
    flags = u32(flags | (1 << (target & 31)))
    relations.set_word(force, u16(flags))
    force = u16(force >> 1)
    target = u16(target << 1)
    flags = relations.word(target)
    flags = u32(flags | (1 << (force & 31)))
    relations.set_word(target, u16(flags))
    amount = state.relationship_credit()
    resources = state.city_gold
    if state.credit_is_rice() != 0:
        resources = state.city_rice
    leader = u16(state.current_force() << 1)
    leaders = state.force_leaders
    leader = leaders.word(leader)
    assignments = state.city_assignments
    city = u16(replace_byte(leader, assignments.byte(leader)))
    city = u16(city & 63)
    city = u16(city << 2)
    total = u32(resources.long(city) + amount)
    if total > 999999:
        total = u32(999999)
    resources.set_long(city, total)


def classify_city_resources(state: GameState) -> Word:
    category = u16(65535)
    gold = state.city_gold
    rice = state.city_rice
    city = u16(state.current_city() << 2)
    if gold.long(city) >= 20000:
        category = u16(0)
        if rice.long(city) >= 20000:
            category = u16(2)
    elif rice.long(city) >= 20000:
        category = u16(1)
    return category
'''

APPROVED_IMPORTS = {'CarryOutcome', 'GameState', 'Table', 'Word',
                    'descending_inclusive', 'low8', 'negative_byte',
                    'replace_byte', 'u8', 'u16', 'u32'}


def _strip_docs(node):
    node = deepcopy(node)
    if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and type(node.body[0].value.value) is str:
        node.body.pop(0)
    return node


def _holes(function):
    result = {}
    roles = []
    if function.name in {'add_packet_city_resources', 'add_packet_city_resources_wrapped', 'transport_direction_or_arrival', 'commit_relationship_resource_credit'}:
        roles.append(('resource_cap', 999999, 4294967295))
    if function.name == 'classify_city_resources':
        roles.append(('resource_threshold', 20000, 4294967295))
    # Each hole is selected by semantic position (comparison RHS and the
    # corresponding u32 saturation), never by target bytes or a source hash.
    for role, canonical, maximum in roles:
        values = []
        for node in ast.walk(function):
            if (isinstance(node, ast.Compare) and len(node.comparators) == 1
                    and isinstance(node.comparators[0], ast.Constant)
                    and ((role == 'resource_cap' and isinstance(node.left, ast.Name) and node.left.id == 'total')
                         or (role == 'resource_threshold' and isinstance(node.left, ast.Call) and isinstance(node.left.func, ast.Attribute) and node.left.func.attr == 'long'))):
                value = node.comparators[0]
                if type(value.value) is not int or not 0 <= value.value <= maximum:
                    raise CompileError('resource rule must be an unsigned LONG literal')
                values.append(value.value)
                node.comparators[0] = ast.Name(id='__'+role, ctx=ast.Load())
            if (role == 'resource_cap' and isinstance(node, ast.Assign)
                    and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                    and node.targets[0].id == 'total' and isinstance(node.value, ast.Call)
                    and isinstance(node.value.func, ast.Name) and node.value.func.id == 'u32'
                    and len(node.value.args) == 1 and isinstance(node.value.args[0], ast.Constant)):
                value = node.value.args[0]
                if type(value.value) is not int or not 0 <= value.value <= maximum:
                    raise CompileError('resource saturation must be an unsigned LONG literal')
                values.append(value.value)
                node.value.args[0] = ast.Name(id='__'+role, ctx=ast.Load())
        if not values or len(set(values)) != 1:
            raise CompileError('all uses of one resource rule must agree')
        result[role] = values[0]
    return result


def semantic_ir(source):
    if type(source) is not str:
        raise CompileError('source must be a text string')
    try:
        module = _strip_docs(ast.parse(source))
    except SyntaxError as exc:
        raise CompileError('invalid structured Python') from exc
    imported, functions = set(), {}
    for node in module.body:
        if isinstance(node, ast.ImportFrom):
            if node.level != 1 or node.module != 'domain':
                raise CompileError('only explicit domain imports are supported')
            for item in node.names:
                if item.asname is not None or item.name not in APPROVED_IMPORTS:
                    raise CompileError('unsupported imported name')
                imported.add(item.name)
        elif isinstance(node, ast.FunctionDef):
            if node.name in functions:
                raise CompileError('duplicate business function')
            functions[node.name] = _strip_docs(node)
        else:
            raise CompileError('only imports and complete business functions are supported')
    expected = {node.name: node for node in ast.parse(FLOW).body}
    if set(functions) != set(expected):
        raise CompileError('all fourteen complete city operations are required')
    require_declared_names(functions, imported)
    records = []
    for name, contract in expected.items():
        function = functions[name]
        locals_ = {arg.arg for arg in function.args.args}
        locals_.update(node.id for node in ast.walk(function) if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store))
        loaded = {node.id for node in ast.walk(function) if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)}
        if loaded - locals_ - imported - set(functions):
            raise CompileError('used external names require actual imports')
        normalized = deepcopy(function)
        holes = _holes(normalized)
        _holes(contract)
        if ast.dump(normalized, include_attributes=False) != ast.dump(contract, include_attributes=False):
            raise CompileError(name+': unsupported control, type, width, call, storage or return edit')
        effects = []
        for node in ast.walk(function):
            if isinstance(node, (ast.stmt, ast.Call, ast.Compare, ast.BinOp)):
                row = {'operation': type(node).__name__, 'semantic': ast.dump(node, include_attributes=False)}
                if isinstance(node, ast.Call):
                    operation = node.func.attr if isinstance(node.func, ast.Attribute) else node.func.id if isinstance(node.func, ast.Name) else ''
                    bits = {'byte':8, 'set_byte':8, 'u8':8, 'low8':8, 'word':16, 'set_word':16, 'u16':16, 'long':32, 'set_long':32, 'u32':32}.get(operation)
                    if bits is not None:
                        row['value_bits'] = bits
                    row['ordered_live_operation'] = operation
                effects.append(row)
        records.append({'name':name, 'holes':holes, 'effects':effects})
    return records


def _view(e, address, register, long=False):
    e.ins('lea.l', f'0x{address:x}:{"l" if long else "w"},%{register}', 6 if long else 4)


def _scalar(e, operation, address, register, width=4):
    e.ins(operation, f'0x{address:x}:w,%{register}', width)


def _packet_amount(e, register, start):
    # Packing four BYTE reads in their original order removes all incoming
    # high bits by the final LONG shift; no extra read/zeroing is inserted.
    e.ins('move.b', f'{start}(%a0),%{register}', 4)
    e.ins('lsl.w', f'#8,%{register}', 2)
    e.ins('move.b', f'{start+1}(%a0),%{register}', 4)
    e.ins('lsl.l', f'#8,%{register}', 2)
    e.ins('move.b', f'{start+2}(%a0),%{register}', 4)
    e.ins('lsl.l', f'#8,%{register}', 2)
    e.ins('move.b', f'{start+3}(%a0),%{register}', 4)


def _cap(e, register, cap, branch_width=2):
    done = e.fresh('credit_within_limit')
    e.ins('cmpi.l', f'#{cap},%{register}', 6)
    e.ins('bls.b' if branch_width == 2 else 'bls.w', done, branch_width)
    e.ins('move.l', f'#{cap},%{register}', 6)
    e.label(done)


def _packet_credit(e, wrapped, cap):
    e.ins('move.w', '%d4,%d1' if wrapped else '%d0,%d4', 2)
    index, amount, balance, view = ('d1','d0','d2','a1') if wrapped else ('d4','d5','d5','a4')
    e.ins('lsl.w', f'#2,%{index}', 2)
    if not wrapped:
        _view(e,0xdffc,view)
    for position, (start, address) in enumerate(((5,0xdffc),(9,0xe09c))):
        _packet_amount(e, amount, start)
        if wrapped:
            _view(e,address,view)
            e.ins('move.l', f'(%{view},%{index}.w),%{balance}', 4)
            e.ins('add.l', f'%{amount},%{balance}', 2)
            _cap(e,balance,cap,4)
        else:
            if position:
                _view(e,address,view)
            e.ins('add.l', f'(%{view},%{index}.w),%{balance}', 4)
            overflow = e.fresh('credit_overflow')
            done = e.fresh('credit_store')
            e.ins('bcs.b' if position == 0 else 'bcs.w',overflow,2 if position == 0 else 4)
            e.ins('cmpi.l',f'#{cap},%{balance}',6)
            e.ins('bls.b',done,2)
            e.label(overflow)
            e.ins('move.l',f'#{cap},%{balance}',6)
            e.label(done)
        e.ins('move.l',f'%{balance},(%{view},%{index}.w)',4)


def _tax(e):
    _view(e,0xe3bc,'a0')
    _scalar(e,'move.w',0xf392,'d0')
    e.ins('lsl.w','#2,%d0',2)
    e.ins('clr.w','(%a0,%d0.w)',4)
    e.ins('move.w','0xf3b6:w,2(%a0,%d0.w)',6)


def _debit(e):
    _scalar(e,'move.w',0xf392,'d0')
    e.ins('lsl.w','#2,%d0',2)
    _view(e,0xdffc,'a0')
    _scalar(e,'move.l',0xf39e,'d1')
    e.ins('sub.l','%d1,(%a0,%d0.w)',4)


def _schedule(e):
    _scalar(e,'move.w',0xf3a8,'d0')
    e.ins('lsl.w','#2,%d0',2)
    _view(e,0xcdfc,'a0')
    _scalar(e,'move.w',0xf688,'d1')
    e.ins('addq.w','#1,%d1',2)
    e.ins('ori.b','#16,%d1',4)
    e.ins('move.b','%d1,(%a0,%d0.w)',4)
    _view(e,0xd4ac6,'a1',True)
    _scalar(e,'move.w',0xf3a8,'d1')
    e.ins('lsl.w','#2,%d1',2)
    for displacement, destination in ((2,1),(0,2)):
        e.ins('move.w',f'{displacement}(%a1,%d1.w),%d2',4)
        e.ins('lsr.w','#4,%d2',2)
        e.ins('move.b',f'%d2,{destination}(%a0,%d0.w)',4)
    e.ins('move.b','0xf393:w,3(%a0,%d0.w)',6)
    _scalar(e,'move.w',0xf3a8,'d1')
    e.ins('lsl.w','#2,%d1',2)
    _view(e,0xdffc,'a1')
    _view(e,0xe09c,'a2')
    _scalar(e,'move.w',0xf688,'d0')
    e.ins('lsl.w','#3,%d0',2)
    _view(e,0x13b68,'a0',True)
    for view, displacement in (('a1',0),('a2',4)):
        e.ins('move.l',f'(%{view},%d1.w),%d2',4)
        e.ins('sub.l',f'{displacement}(%a0,%d0.w),%d2',4)
        e.ins('move.l',f'%d2,(%{view},%d1.w)',4)


def _relationship(e):
    _scalar(e,'move.w',0xf3e0,'d0')
    e.ins('lsl.w','#1,%d0',2)
    _view(e,0xe730,'a0')
    e.ins('move.w','(%a0,%d0.w),%d1',4)
    _scalar(e,'move.w',0xf376,'d0')
    e.ins('lsl.w','#1,%d0',2)
    _view(e,0xe710,'a0')
    e.ins('move.w','(%a0,%d0.w),%d2',4)
    e.ins('bset.l','%d1,%d2',2)
    e.ins('move.w','%d2,(%a0,%d0.w)',4)
    _scalar(e,'move.w',0xf3e0,'d0')
    e.ins('lsl.w','#1,%d0',2)
    _view(e,0xe730,'a0')
    e.ins('move.w','(%a0,%d0.w),%d0',4)
    e.ins('lsl.w','#1,%d0',2)
    _scalar(e,'move.w',0xf376,'d1')
    _view(e,0xe710,'a0')
    e.ins('move.w','(%a0,%d0.w),%d2',4)
    e.ins('bset.l','%d1,%d2',2)
    e.ins('move.w','%d2,(%a0,%d0.w)',4)


def _equipment(e):
    _scalar(e,'move.w',0xf3f0,'d0')
    e.ins('lsl.w','#2,%d0',2)
    _view(e,0xef6a,'a0')
    e.ins('move.l','(%a0,%d0.w),%d1',4)
    _scalar(e,'move.w',0xf392,'d2')
    e.ins('lsl.w','#2,%d2',2)
    _view(e,0xdffc,'a1')
    e.ins('sub.l','%d1,(%a1,%d2.w)',4)
    _view(e,0xea88,'a0')
    _scalar(e,'move.w',0xf3a6,'d0')
    e.ins('lsl.w','#1,%d0',2)
    _scalar(e,'add.w',0xf3a6,'d0')
    _scalar(e,'add.w',0xf3f0,'d0')
    _scalar(e,'move.w',0xf3f0,'d1')
    e.ins('lsl.w','#1,%d1',2)
    _view(e,0xef64,'a1')
    e.ins('move.w','(%a1,%d1.w),%d2',4)
    e.ins('addq.w','#1,%d2',2)
    e.ins('move.b','%d2,(%a0,%d0.w)',4)
    e.ins('move.w','0xf38a:w,0xf612:w',6)
    for value, address in ((40,0xf362),(98,0xf3fe)):
        e.ins('move.w',f'#{value},0x{address:x}:w',6)
    e.ins('move.w','0xf3a6:w,0xf3d0:w',6)
    e.ins('move.w','#1,0xf774:w',6)
    e.ins('move.w','#9,0xff7026:l',8)


def _selected_cost(e):
    _scalar(e,'move.w',0xf39a,'d1')
    e.ins('lsl.w','#2,%d1',2)
    e.ins('lea.l',f'{0x1344c-(e.pc+2)}(%pc),%a0',4)
    e.ins('nop','',2)
    e.ins('move.l','(%a0,%d1.w),%d1',4)
    _scalar(e,'add.l',0xf3f4,'d1')
    _scalar(e,'cmp.l',0xf3f8,'d1')
    finish = e.fresh('cost_above_limit')
    e.ins('bhi.w',finish,4)
    e.ins('move.l','%d1,0xf3f4:w',4)
    e.label(finish)


def _direction_or_arrival(e, cap):
    _view(e,0xff4000,'a0',True)
    e.ins('adda.w','0xceac:w,%a0',4)
    e.ins('addq.w','#1,0xceac:w',4)
    e.ins('tst.b','1(%a0)',4)
    arrive, left, down, right, move, finish = (e.fresh(role) for role in ('arrive','left','down','right','move','return'))
    e.ins('bmi.b',arrive,2)
    e.ins('move.b','(%a0),%d0',2)
    for label in (left,down,right):
        e.ins('subq.b','#1,%d0',2)
        e.ins('beq.b',label,2)
    e.ins('clr.w','%d0',2)
    e.ins('move.w','#65520,%d1',4)
    e.ins('bra.b',move,2)
    e.label(left)
    e.ins('move.w','#65520,%d0',4)
    e.ins('clr.w','%d1',2)
    e.ins('bra.b',move,2)
    e.label(down)
    e.ins('clr.w','%d0',2)
    e.ins('move.w','#16,%d1',4)
    e.ins('bra.w',move,4)
    e.label(right)
    e.ins('move.w','#16,%d0',4)
    e.ins('clr.w','%d1',2)
    e.label(move)
    e.ins('add.w','%d0,0xcea8:w',4)
    e.ins('add.w','%d1,0xceaa:w',4)
    e.ins('andi.w','#65534,%sr',4)
    e.ins('bra.w',finish,4)
    e.label(arrive)
    e.ins('clr.w','%d2',2)
    e.ins('move.b','(%a6),%d2',2)
    e.ins('andi.w','#3,%d2',4)
    e.ins('lsl.w','#3,%d2',2)
    e.ins('clr.w','%d1',2)
    e.ins('move.b','3(%a6),%d1',4)
    e.ins('lsl.w','#2,%d1',2)
    _view(e,0x13b60,'a1',True)
    for displacement, address in ((0,0xdffc),(4,0xe09c)):
        e.ins('move.l',f'{displacement}(%a1,%d2.w),%d3',4)
        _view(e,address,'a2')
        e.ins('add.l','(%a2,%d1.w),%d3',4)
        _cap(e,'d3',cap)
        e.ins('move.l','%d3,(%a2,%d1.w)',4)
    e.ins('clr.b','(%a6)',2)
    e.ins('ori.w','#1,%sr',4)
    e.label(finish)


def _collision(e):
    _scalar(e,'move.w',0xcea8,'d0')
    e.ins('lsr.w','#4,%d0',2)
    _scalar(e,'move.w',0xceaa,'d1')
    e.ins('lsr.w','#4,%d1',2)
    _view(e,0xce00,'a0')
    e.ins('move.w','#39,%d2',4)
    scan, next_, packed, more, empty, found, finish = (e.fresh(role) for role in ('transport_scan','transport_next','packed_scan','packed_next','no_collision','collision','return'))
    e.label(scan)
    e.ins('tst.b','(%a0)',2)
    e.ins('beq.b',next_,2)
    e.ins('btst.b','#4,(%a0)',4)
    e.ins('bne.b',next_,2)
    e.ins('cmp.b','1(%a0),%d0',4)
    e.ins('bne.b',next_,2)
    e.ins('cmp.b','2(%a0),%d1',4)
    e.ins('bne.b',next_,2)
    e.ins('bra.w',found,4)
    e.label(next_)
    e.ins('addq.w','#4,%a0',2)
    e.ins('dbra',f'%d2,{scan}',4)
    _view(e,0x9000,'a0')
    e.label(packed)
    e.ins('move.b','(%a0),%d2',2)
    e.ins('andi.w','#15,%d2',4)
    e.ins('beq.b',empty,2)
    e.ins('cmp.b','1(%a0),%d0',4)
    e.ins('bne.b',more,2)
    e.ins('cmp.b','2(%a0),%d1',4)
    e.ins('bne.b',more,2)
    e.ins('bra.w',found,4)
    e.label(more)
    e.ins('lea.l','13(%a0,%d2.w),%a0',4)
    e.ins('bra.b',packed,2)
    e.label(empty)
    e.ins('andi.w','#65534,%sr',4)
    e.ins('bra.w',finish,4)
    e.label(found)
    e.ins('ori.w','#1,%sr',4)
    e.label(finish)


def _snapshot(e, alternate):
    _view(e,0xed84 if alternate else 0xdffc,'a0')
    _scalar(e,'move.w',0xf68a,'d0')
    e.ins('lsl.w','#2,%d0',2)
    e.ins('move.l',f'(%a0,%d0.w),0x{0xf696 if alternate else 0xf69a:x}:w',6)
    _view(e,0xee24 if alternate else 0xe09c,'a0')
    e.ins('move.l',f'(%a0,%d0.w),0x{0xf69e if alternate else 0xf6a2:x}:w',6)


def _relationship_credit(e, cap):
    _scalar(e,'move.w',0xf376,'d0')
    _scalar(e,'move.w',0xf3a6,'d1')
    _view(e,0xe710,'a0')
    e.ins('lsl.w','#1,%d0',2)
    e.ins('move.w','(%a0,%d0.w),%d2',4)
    e.ins('bset.l','%d1,%d2',2)
    e.ins('move.w','%d2,(%a0,%d0.w)',4)
    e.ins('lsr.w','#1,%d0',2)
    e.ins('lsl.w','#1,%d1',2)
    e.ins('move.w','(%a0,%d1.w),%d2',4)
    e.ins('bset.l','%d0,%d2',2)
    e.ins('move.w','%d2,(%a0,%d1.w)',4)
    _scalar(e,'move.l',0xf3c8,'d0')
    _view(e,0xdffc,'a0')
    e.ins('tst.w','0xf742:w',4)
    gold = e.fresh('selected_resource')
    e.ins('beq.w',gold,4)
    _view(e,0xe09c,'a0')
    e.label(gold)
    _scalar(e,'move.w',0xf376,'d1')
    e.ins('lsl.w','#1,%d1',2)
    _view(e,0xe640,'a1')
    e.ins('move.w','(%a1,%d1.w),%d1',4)
    _view(e,0xcc00,'a1')
    e.ins('move.b','(%a1,%d1.w),%d1',4)
    e.ins('andi.w','#63,%d1',4)
    e.ins('lsl.w','#2,%d1',2)
    e.ins('move.l','(%a0,%d1.w),%d2',4)
    e.ins('add.l','%d0,%d2',2)
    _cap(e,'d2',cap,4)
    e.ins('move.l','%d2,(%a0,%d1.w)',4)


def _classify(e, threshold):
    e.ins('move.w','#65535,%d0',4)
    _view(e,0xdffc,'a0')
    _view(e,0xe09c,'a1')
    _scalar(e,'move.w',0xf364,'d1')
    e.ins('lsl.w','#2,%d1',2)
    poor, finish = e.fresh('gold_below_threshold'), e.fresh('return')
    e.ins('cmpi.l',f'#{threshold},(%a0,%d1.w)',8)
    e.ins('bcs.w',poor,4)
    e.ins('clr.w','%d0',2)
    e.ins('cmpi.l',f'#{threshold},(%a1,%d1.w)',8)
    e.ins('bcs.w',finish,4)
    e.ins('move.w','#2,%d0',4)
    e.ins('bra.w',finish,4)
    e.label(poor)
    e.ins('cmpi.l',f'#{threshold},(%a1,%d1.w)',8)
    e.ins('bcs.w',finish,4)
    e.ins('move.w','#1,%d0',4)
    e.label(finish)


def compile_city(source):
    """Pure source-text compilation of fourteen full city operations."""
    records = semantic_ir(source)
    units = []
    emitters = {'commit_tax_rate':_tax, 'debit_city_gold':_debit,
                'schedule_transport_debit':_schedule,
                'commit_mutual_relationship':_relationship,
                'commit_equipment_purchase':_equipment,
                'add_selected_cost':_selected_cost,
                'transport_collision':_collision}
    for record in records:
        binding = next(item for item in CITY_BINDINGS if item.name == record['name'])
        e = Emitter(binding)
        e.begin()
        name, holes = record['name'], record['holes']
        if name in emitters:
            emitters[name](e)
        elif name.startswith('add_packet_city_resources'):
            _packet_credit(e,name.endswith('_wrapped'),holes['resource_cap'])
        elif name == 'transport_direction_or_arrival':
            _direction_or_arrival(e,holes['resource_cap'])
        elif name in ('snapshot_city_resources','load_city_ed84_ee24_longs'):
            _snapshot(e,name.startswith('load_'))
        elif name == 'commit_relationship_resource_credit':
            _relationship_credit(e,holes['resource_cap'])
        elif name == 'classify_city_resources':
            _classify(e,holes['resource_threshold'])
        else:
            raise CompileError('unbound city operation')
        e.end()
        unit = e.unit(record['effects'])
        unit.setdefault('binding',asdict(binding))
        if sum(row['encoding_bytes'] for row in unit['instructions']) != binding.end-binding.entry:
            raise CompileError(name+': lowering does not fit the complete declared body')
        units.append(unit)
    return {'units':units, 'allocated_bytes':1098,
            'instructions':sum(len(unit['instructions']) for unit in units),
            'semantic_family':'ordered_city_ledgers_transport', 'complete_CPU':False}
