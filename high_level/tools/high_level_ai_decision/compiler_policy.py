"""Closed typed policy FLOW contracts and ordinary 68000 instruction selection.

Every statement, call, annotation and expression must match a supported
semantic flow. Named literal slots are editable and drive their own emitted
operations. The backend has fixed original ABI/layout bindings, not an
arbitrary-Python compiler. No files, images or opcode payloads are inputs.
"""
import ast
from copy import deepcopy

from .compiler_common import CompileError, Emitter, require_declared_names
from .target import POLICY_BINDINGS, TABLE_BINDINGS, SCALAR_BINDINGS


# This is a structured business-language contract, not target assembly.
FLOW = '''
def choose_attribute_neighbor_action(state: AiState) -> None:
    best, selected = select_foreign_neighbor_attribute_max(state)
    if not negative_word(selected):
        threshold = u16(5)
        if best < 80:
            threshold = u16(3)
        sample = state.sample_random()
        scaled = u16(u32(sample << 3) >> 16)
        if scaled < threshold:
            state.set_command(5)
            return
    state.set_command(3)

def select_foreign_neighbor_attribute_max(state: AiState) -> tuple[Word, Word]:
    neighbors = state.neighbors.at(u16(state.current_city() << 3)).cursor()
    best = u16(0)
    selected = u16(65535)
    force = state.force_selector()
    owners = state.city_owners
    first = state.b600
    second = state.b400
    status = state.c300
    processed = state.city_processed
    while True:
        city = u16(neighbors.next_byte())
        if negative_byte(city):
            break
        if owners.byte(city) == low8(force):
            continue
        if negative_byte(owners.byte(city)):
            continue
        if processed.byte(city) != 0:
            continue
        score = city_officer_attribute_max(state, city, first, second, status)
        if score > best:
            best = score
            selected = city
    return best, selected

def city_officer_attribute_max(state: AiState, city: Word, first: Table,
                               second: Table, status: Table) -> Word:
    city = u16(city)
    membership = state.city_assignments
    maximum = u16(0)
    for officer in descending_inclusive(255):
        if membership.previous_byte() != low8(city):
            continue
        if status.byte(officer) > 95:
            continue
        index = u16(officer << 1)
        if first.word(index) > maximum:
            maximum = first.word(index)
        if second.word(index) > maximum:
            maximum = second.word(index)
    return maximum

def choose_player_neighbor_action(state: AiState) -> None:
    gate = neighbor_has_player_owner(state)
    if gate.carry == 1:
        state.set_command(4)
    else:
        state.set_command(8)

def neighbor_has_player_owner(state: AiState) -> CarryOutcome:
    neighbors = state.neighbors.at(u16(state.current_city() << 3)).cursor()
    owners = state.city_owners
    while True:
        city = u16(neighbors.next_byte())
        if negative_byte(city):
            break
        owner = u16(owners.byte(city))
        if negative_byte(owner):
            continue
        if owner == state.player_first():
            return state.carry_result(1)
        if owner == state.player_second():
            return state.carry_result(1)
        if owner == state.player_third():
            return state.carry_result(1)
    return state.carry_result(0)

def choose_resource_neighbor_action(state: AiState) -> None:
    state.sample_random()
    total, selected = select_player_neighbor_resource_sum(state)
    state.set_chosen_city(selected)
    if total >= 100000:
        command = u16(6)
    elif total >= 50000:
        if u16(state.seed_word() & 7) < 5:
            command = u16(6)
        else:
            command = u16(8)
    elif total >= 10000:
        if state.seed_low_byte() & 1:
            command = u16(6)
        else:
            command = u16(8)
    else:
        if u16(state.seed_word() & 7) < 2:
            command = u16(6)
        else:
            command = u16(8)
    state.set_command(command)

def select_player_neighbor_resource_sum(state: AiState) -> tuple[Long, Word]:
    neighbors = state.neighbors.at(u16(state.current_city() << 3)).cursor()
    best = u32(0)
    selected = u16(65535)
    city = u16(0)
    owners = state.city_owners
    balances = state.city_balances
    rice = state.city_rice
    while True:
        city = u16(replace_byte(city, neighbors.next_byte()))
        if negative_byte(low8(city)):
            break
        owner = u16(owners.byte(city))
        if negative_byte(owner):
            continue
        if owner != state.player_first():
            if owner != state.player_second():
                if low8(selected) != state.player_third():
                    continue
        city = u16(city << 2)
        total = u32(balances.long(city) + rice.long(city))
        if total > best:
            best = total
            city = u16(city >> 2)
            selected = city
    return best, selected
'''

APPROVED = {'AiState', 'CarryOutcome', 'Long', 'Table', 'Word',
            'descending_inclusive', 'low8', 'negative_byte', 'negative_word', 'replace_byte', 'u16', 'u32'}


def _without_doc(node):
    result = deepcopy(node)
    if (result.body and isinstance(result.body[0], ast.Expr)
            and isinstance(result.body[0].value, ast.Constant)
            and type(result.body[0].value.value) is str):
        result.body.pop(0)
    return result


def _literal_holes(function):
    """Only complete named rule positions admit typed, emitted literal edits."""
    holes = {}
    def slot(parent, key, role, bits):
        value = parent[key] if type(parent) is list else getattr(parent, key)
        if not isinstance(value, ast.Constant) or type(value.value) is not int or not 0 <= value.value < (1 << bits):
            raise CompileError('strict unsigned semantic literal required: '+role)
        if role in holes and holes[role] != value.value:
            raise CompileError('shared semantic rule literal must remain consistent: '+role)
        holes[role] = value.value
        replacement = ast.Name(id='__rule_'+role, ctx=ast.Load())
        if type(parent) is list: parent[key] = replacement
        else: setattr(parent, key, replacement)
    if function.name == 'choose_attribute_neighbor_action':
        threshold_calls = [n.value for n in ast.walk(function)
                           if isinstance(n, ast.Assign) and len(n.targets) == 1
                           and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'threshold']
        if len(threshold_calls) != 2:
            raise CompileError('both ordered attribute-chance assignments required')
        # ast.walk is breadth-first: outer threshold precedes the conditional.
        for call, role in zip(threshold_calls, ('attribute_chance', 'weak_attribute_chance')):
            if not isinstance(call, ast.Call) or len(call.args) != 1:
                raise CompileError('typed attribute chance constructor required')
            slot(call.args, 0, role, 16)
        comparisons = [n for n in ast.walk(function) if isinstance(n, ast.Compare)
                       and isinstance(n.left, ast.Name) and n.left.id == 'best']
        if len(comparisons) != 1 or len(comparisons[0].comparators) != 1:
            raise CompileError('one attribute-band gate required')
        slot(comparisons[0].comparators, 0, 'attribute_band', 16)
    elif function.name == 'city_officer_attribute_max':
        comparisons = [n for n in ast.walk(function) if isinstance(n, ast.Compare)
                       and isinstance(n.left, ast.Call) and isinstance(n.left.func, ast.Attribute)
                       and isinstance(n.left.func.value, ast.Name) and n.left.func.value.id == 'status']
        if len(comparisons) != 1 or len(comparisons[0].comparators) != 1:
            raise CompileError('one live status gate required')
        slot(comparisons[0].comparators, 0, 'officer_status_limit', 8)
    elif function.name == 'choose_resource_neighbor_action':
        totals = [n for n in ast.walk(function) if isinstance(n, ast.Compare)
                  and isinstance(n.left, ast.Name) and n.left.id == 'total']
        if len(totals) != 3:
            raise CompileError('three ordered resource bands required')
        for comparison, role in zip(totals, ('resource_high', 'resource_middle', 'resource_low')):
            if len(comparison.comparators) != 1:
                raise CompileError('one typed operand per resource comparison required')
            slot(comparison.comparators, 0, role, 32)
        seed_gates = [n for n in ast.walk(function) if isinstance(n, ast.Compare)
                      and isinstance(n.left, ast.Call)]
        if len(seed_gates) != 2:
            raise CompileError('two ordered seed-WORD gates required')
        # ast.walk breadth-first encounters the outer else before the nested elif.
        # Locate by the containing resource-band branch, not traversal order.
        root = next(n for n in function.body if isinstance(n, ast.If))
        middle = root.orelse[0]
        low = middle.orelse[0]
        slot(middle.body[0].test.comparators, 0, 'middle_chance', 16)
        slot(low.orelse[0].test.comparators, 0, 'low_chance', 16)
    return holes


def semantic_ir(source):
    if type(source) is not str:
        raise CompileError('explicit semantic source text required')
    try: module = ast.parse(source)
    except SyntaxError as error: raise CompileError('invalid structured Python source') from error
    functions = {}; imported = set()
    for node in _without_doc(module).body:
        if isinstance(node, ast.ImportFrom):
            if node.module != 'domain' or node.level != 1:
                raise CompileError('explicit approved domain imports required')
            for alias in node.names:
                if alias.asname is not None or alias.name not in APPROVED:
                    raise CompileError('unsupported imported name')
                imported.add(alias.name)
        elif isinstance(node, ast.FunctionDef):
            if node.name in functions or node.type_params:
                raise CompileError('unique non-generic policy functions required')
            functions[node.name] = _without_doc(node)
        else:
            raise CompileError('only imports and complete business functions supported')
    expected = {node.name: node for node in ast.parse(FLOW).body}
    if set(functions) != set(expected):
        raise CompileError('all seven complete policy bodies required')
    require_declared_names(functions, imported)
    records = []
    for name, contract in expected.items():
        function = functions[name]
        locals_ = {a.arg for a in function.args.args}
        locals_.update(n.id for n in ast.walk(function) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store))
        if locals_ & (APPROVED | set(expected)):
            raise CompileError('local or parameter shadows a declared intrinsic/function')
        normalized = deepcopy(function)
        try:
            holes = _literal_holes(normalized)
            _literal_holes(contract)
        except (AttributeError, IndexError, StopIteration, TypeError) as error:
            raise CompileError(name+': complete supported typed control shape required') from error
        if ast.dump(normalized, include_attributes=False) != ast.dump(contract, include_attributes=False):
            raise CompileError(name+': unsupported control, call, width, storage or return edit')
        effects = [dict(operation=type(n).__name__, semantic=ast.dump(n, include_attributes=False))
                   for n in ast.walk(function) if isinstance(n, (ast.stmt, ast.Call, ast.Compare, ast.BinOp))]
        records.append(dict(name=name, values=holes, effects=effects))
    return records


def _view(e, name, register):
    binding = TABLE_BINDINGS[name]
    address, suffix = binding['address'], binding['suffix']
    if suffix == 'w': address &= 65535
    e.ins('lea.l', f'0x{address:x}:{suffix},%{register}', 4 if suffix == 'w' else 6)


def _scalar(name):
    return f"0x{SCALAR_BINDINGS[name]['address'] & 65535:x}:w"


def _word(e, value, register):
    if value == 0: e.ins('clr.w', '%'+register)
    else: e.ins('move.w', f'#0x{value:x},%{register}', 4)


def _command(e, value):
    e.ins('move.w', f'#{value},'+_scalar('command'), 6)


def _neighbors(e):
    _view(e, 'neighbors', 'a0')
    e.ins('move.w', _scalar('current_city')+',%d0', 4)
    e.ins('lsl.w', '#3,%d0')
    e.ins('adda.w', '%d0,%a0')


def _attribute_action(e, values):
    low = e.fresh('weak_attribute'); random = e.fresh('sample_chance')
    ordinary = e.fresh('ordinary_command'); chosen = e.fresh('chosen_command'); done = e.fresh('return')
    e.ins('bsr.w', 'select_foreign_neighbor_attribute_max', 4)
    e.ins('tst.w', '%d2'); e.ins('bmi.w', ordinary, 4)
    e.ins('move.w', f"#{values['attribute_chance']},%d3", 4)
    e.ins('cmpi.w', f"#{values['attribute_band']},%d1", 4)
    e.ins('bcc.w', random, 4)
    e.label(low); e.ins('move.w', f"#{values['weak_attribute_chance']},%d3", 4)
    e.label(random); e.ins('jsr', 'random_sample:l', 6)
    e.ins('andi.l', '#0xffff,%d0', 6); e.ins('lsl.l', '#3,%d0'); e.ins('swap', '%d0')
    e.ins('cmp.w', '%d3,%d0'); e.ins('bcs.w', chosen, 4)
    e.label(ordinary); _command(e, 3); e.ins('bra.w', done, 4)
    e.label(chosen); _command(e, 5); e.label(done)


def _attribute_query(e):
    _neighbors(e); _word(e, 0, 'd1'); _word(e, 65535, 'd2')
    e.ins('move.w', _scalar('force_selector')+',%d3', 4)
    for name, reg in (('city_owners','a1'), ('b600','a2'), ('b400','a3'), ('c300','a5'), ('city_processed','a6')):
        _view(e, name, reg)
    _word(e, 0, 'd0')
    loop = e.fresh('neighbor'); done = e.fresh('return')
    e.label(loop); e.ins('move.b', '(%a0)+,%d0'); e.ins('bmi.w', done, 4)
    e.ins('cmp.b', '0(%a1,%d0.w),%d3', 4); e.ins('beq.b', loop)
    e.ins('tst.b', '0(%a1,%d0.w)', 4); e.ins('bmi.b', loop)
    e.ins('tst.b', '0(%a6,%d0.w)', 4); e.ins('bne.b', loop)
    e.ins('bsr.w', 'city_officer_attribute_max', 4)
    e.ins('cmp.w', '%d1,%d5'); e.ins('bls.b', loop)
    e.ins('move.w', '%d5,%d1'); e.ins('move.w', '%d0,%d2'); e.ins('bra.b', loop)
    e.label(done)


def _attribute_scan(e, values):
    _view(e, 'city_assignments', 'a4'); _word(e, 0, 'd5'); _word(e, 255, 'd6')
    loop = e.fresh('officer'); second = e.fresh('second_attribute'); next_ = e.fresh('next_officer')
    e.label(loop); e.ins('cmp.b', '-(%a4),%d0'); e.ins('bne.w', next_, 4)
    e.ins('move.b', '0(%a5,%d6.w),%d7', 4)
    e.ins('cmpi.b', f"#{values['officer_status_limit']},%d7", 4); e.ins('bhi.w', next_, 4)
    e.ins('move.w', '%d6,%d7'); e.ins('lsl.w', '#1,%d7')
    e.ins('cmp.w', '0(%a2,%d7.w),%d5', 4); e.ins('bcc.w', second, 4)
    e.ins('move.w', '0(%a2,%d7.w),%d5', 4)
    e.label(second); e.ins('cmp.w', '0(%a3,%d7.w),%d5', 4); e.ins('bcc.w', next_, 4)
    e.ins('move.w', '0(%a3,%d7.w),%d5', 4)
    e.label(next_); e.ins('dbra', '%d6,'+loop, 4)


def _player_action(e):
    chosen = e.fresh('player_neighbor'); done = e.fresh('return')
    e.ins('bsr.w', 'neighbor_has_player_owner', 4); e.ins('bcs.w', chosen, 4)
    _command(e, 8); e.ins('bra.w', done, 4); e.label(chosen); _command(e, 4); e.label(done)


def _player_query(e):
    _neighbors(e); _view(e, 'city_owners', 'a1'); _word(e, 0, 'd0'); _word(e, 0, 'd1')
    loop = e.fresh('neighbor'); set_ = e.fresh('carry_set'); clear = e.fresh('carry_clear'); done = e.fresh('return')
    e.label(loop); e.ins('move.b', '(%a0)+,%d0'); e.ins('bmi.w', clear, 4)
    e.ins('move.b', '0(%a1,%d0.w),%d1', 4); e.ins('bmi.b', loop)
    for name in ('player_first','player_second'):
        e.ins('cmp.b', _scalar(name)+',%d1', 4); e.ins('beq.w', set_, 4)
    e.ins('cmp.b', _scalar('player_third')+',%d1', 4); e.ins('bne.b', loop)
    e.label(set_); e.ins('ori.w', '#1,%sr', 4); e.ins('bra.w', done, 4)
    e.label(clear); e.ins('andi.w', '#0xfffe,%sr', 4); e.label(done)


def _resource_action(e, values):
    under_middle = e.fresh('under_middle'); under_low = e.fresh('under_low')
    chosen = e.fresh('resource_command'); ordinary = e.fresh('ordinary_command'); done = e.fresh('return')
    e.ins('jsr', 'random_sample:l', 6); e.ins('bsr.w', 'select_player_neighbor_resource_sum', 4)
    e.ins('move.w', '%d1,'+_scalar('chosen_city'), 4)
    e.ins('cmpi.l', f"#{values['resource_high']},%d0", 6); e.ins('bcc.w', chosen, 4)
    e.ins('cmpi.l', f"#{values['resource_middle']},%d0", 6); e.ins('bcs.w', under_middle, 4)
    e.ins('move.w', _scalar('seed_word')+',%d0', 4); e.ins('andi.w', '#7,%d0', 4)
    e.ins('cmpi.w', f"#{values['middle_chance']},%d0", 4); e.ins('bcs.w', chosen, 4); e.ins('bra.w', ordinary, 4)
    e.label(under_middle); e.ins('cmpi.l', f"#{values['resource_low']},%d0", 6); e.ins('bcs.w', under_low, 4)
    e.ins('btst.b', '#0,'+_scalar('seed_low_byte'), 6); e.ins('bne.w', chosen, 4); e.ins('bra.w', ordinary, 4)
    e.label(under_low); e.ins('move.w', _scalar('seed_word')+',%d0', 4); e.ins('andi.w', '#7,%d0', 4)
    e.ins('cmpi.w', f"#{values['low_chance']},%d0", 4); e.ins('bcc.w', ordinary, 4)
    e.label(chosen); _command(e, 6); e.ins('bra.w', done, 4)
    e.label(ordinary); _command(e, 8); e.label(done)


def _resource_query(e):
    _neighbors(e); e.ins('moveq', '#0,%d0'); _word(e, 65535, 'd1'); _word(e, 0, 'd2'); _word(e, 0, 'd3')
    for name, reg in (('city_owners','a1'), ('city_balances','a2'), ('city_rice','a3')): _view(e, name, reg)
    loop = e.fresh('neighbor'); sum_ = e.fresh('sum_live_resources'); done = e.fresh('return')
    e.label(loop); e.ins('move.b', '(%a0)+,%d2'); e.ins('bmi.w', done, 4)
    e.ins('move.b', '0(%a1,%d2.w),%d3', 4); e.ins('bmi.b', loop)
    for name in ('player_first', 'player_second'):
        e.ins('cmp.b', _scalar(name)+',%d3', 4); e.ins('beq.w', sum_, 4)
    e.ins('cmp.b', _scalar('player_third')+',%d1', 4); e.ins('bne.b', loop)
    e.label(sum_); e.ins('lsl.w', '#2,%d2'); e.ins('move.l', '0(%a2,%d2.w),%d4', 4)
    e.ins('add.l', '0(%a3,%d2.w),%d4', 4); e.ins('cmp.l', '%d0,%d4'); e.ins('bls.b', loop)
    e.ins('move.l', '%d4,%d0'); e.ins('lsr.w', '#2,%d2'); e.ins('move.w', '%d2,%d1'); e.ins('bra.b', loop)
    e.label(done)


LOWERERS = {'choose_attribute_neighbor_action': _attribute_action,
            'select_foreign_neighbor_attribute_max': _attribute_query,
            'city_officer_attribute_max': _attribute_scan,
            'choose_player_neighbor_action': _player_action,
            'neighbor_has_player_owner': _player_query,
            'choose_resource_neighbor_action': _resource_action,
            'select_player_neighbor_resource_sum': _resource_query}


def compile_policy(source):
    records = {r['name']: r for r in semantic_ir(source)}
    units = []
    for binding in POLICY_BINDINGS:
        record = records[binding.name]; e = Emitter(binding); e.begin()
        lower = LOWERERS[binding.name]
        if record['values']: lower(e, record['values'])
        else: lower(e)
        e.end()
        if sum(i['encoding_bytes'] for i in e.mapping) != binding.end-binding.entry:
            raise CompileError('typed target allocation differs: '+binding.name)
        units.append(e.unit(dict(typed_semantic_values=record['values'],
                                semantic_operations=record['effects'], live_DATA=True,
                                natural_domain='unknown', complete_CPU=False)))
    count = sum(len(u['instructions']) for u in units)
    if count != 146: raise CompileError('complete policy instruction allocation differs')
    return dict(units=units, effects={u['binding']['name']: u['effects'] for u in units},
                new_bytes=516, instructions=count, original_generation_input=False)
