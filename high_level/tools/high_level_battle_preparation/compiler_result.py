"""Strict semantic plans lowered to the original fixed-layout result ABI.

The frontend consumes every executable AST node. Named editable value slots
are typed and flow-coupled; other unsupported changes fail explicitly. This is
a constrained compatibility backend, not a general Python compiler. Semantic
contracts are control/data-flow descriptions, never instruction encodings,
source hashes, original-ROM reads or cached assembly inputs.
"""
import ast
from .compiler_common import CompileError, Emitter, require_declared_names
from .target import RESULT_BINDINGS


# These small flow contracts constrain the original allocation. Holes beginning
# EDIT_ bind actual source literals; repeated holes must retain one consistent
# business value. All remaining syntax, reads, writes and returns is checked.
FLOW = {'decrement_battle_3cc2_counters': '_tick_single_counter_fields(CounterMemory(state))',
 'decrement_battle_status_counters': '_tick_status_counter_fields(CounterMemory(state))',
 'select_battle_outcome_side': '\n'
                               'outcome = state.table(0xFFFF8114).word(0)\n'
                               'if outcome == EDIT_SIDE_1 or outcome == EDIT_SIDE_2:\n'
                               '    officer = state.table(0xFFFF80E0).word(0)\n'
                               'elif outcome == EDIT_SPECIAL_1 or outcome == EDIT_SPECIAL_2:\n'
                               '    state.table(0xFFFFF362).set_word(0, EDIT_MODE)\n'
                               '    return\n'
                               'else:\n'
                               '    officer = state.table(0xFFFF80E2).word(0)\n'
                               'state.table(0xFFFFF6D6).set_word(0, 0)\n'
                               'if officer == state.table(0xFFFFF702).word(0):\n'
                               '    state.table(0xFFFFF6D6).set_word(0, EDIT_NEXT_MODE)\n',
 'adjust_battle_pair_spacing': '\n'
                               'officer = u16(officer)\n'
                               'if officer == state.table(0xFFFFF702).word(0):\n'
                               '    other = state.table(0xFFFFF706).word(0)\n'
                               'else:\n'
                               '    other = state.table(0xFFFFF702).word(0)\n'
                               'coordinates = state.table(0xFFFFA150)\n'
                               'own_offset = u16(officer * 4)\n'
                               'other_offset = u16(other * 4)\n'
                               'own_x = coordinates.word(own_offset)\n'
                               'other_x = coordinates.word(other_offset)\n'
                               'x_negative = own_x < other_x\n'
                               'x_gap = u16(own_x - other_x)\n'
                               'if x_negative:\n'
                               '    x_gap = u16(-x_gap)\n'
                               'if x_gap >= EDIT_X_GAP:\n'
                               '    return\n'
                               'x_deficit = u16(x_gap - EDIT_X_GAP)\n'
                               'own_y = coordinates.word(own_offset, 2)\n'
                               'other_y = coordinates.word(other_offset, 2)\n'
                               'y_negative = own_y < other_y\n'
                               'y_gap = u16(own_y - other_y)\n'
                               'if y_negative:\n'
                               '    y_gap = u16(-y_gap)\n'
                               'if y_gap >= EDIT_Y_GAP:\n'
                               '    return\n'
                               'y_deficit = u16(y_gap - EDIT_Y_GAP)\n'
                               'if y_deficit > x_deficit:\n'
                               '    if not y_negative:\n'
                               '        y_deficit = u16(-y_deficit)\n'
                               '    previous = coordinates.word(own_offset, 2)\n'
                               '    coordinates.set_word(own_offset, u16(previous + y_deficit), 2)\n'
                               'else:\n'
                               '    if not x_negative:\n'
                               '        x_deficit = u16(-x_deficit)\n'
                               '    previous = coordinates.word(own_offset)\n'
                               '    coordinates.set_word(own_offset, u16(previous + x_deficit))\n',
 'battle_pair_removed_carry': '\n'
                              'membership = state.table(0xFFFFCC00)\n'
                              'first = state.table(0xFFFFF702).word(0)\n'
                              'if membership.byte(first) == EDIT_REMOVED:\n'
                              '    return state.set_carry(True)\n'
                              'second = state.table(0xFFFFF706).word(0)\n'
                              'if membership.byte(second) == EDIT_REMOVED:\n'
                              '    return state.set_carry(True)\n'
                              'return state.set_carry(False)\n',
 'selected_battle_roster_carry': '\n'
                                 'requested = record.word(0)\n'
                                 'if state.table(0xFFFFF6D7).byte(0) & 2:\n'
                                 '    roster = state.table(0xFFFFA5A4).cursor()\n'
                                 'else:\n'
                                 '    roster = state.table(0xFFFFA550).cursor()\n'
                                 'while True:\n'
                                 '    member = roster.next_word()\n'
                                 '    if member & 32768:\n'
                                 '        return state.set_carry(True)\n'
                                 '    if member == requested:\n'
                                 '        return state.set_carry(False)\n',
 '_tick_single_counter_fields': 'if type(memory) is not CounterMemory:\n'
                                "    raise ValueError('sealed counter memory required')\n"
                                'counters = memory.table(16727234)\n'
                                'for offset in range(EDIT_COUNT):\n'
                                '    value = counters.byte(0)\n'
                                '    if value != 0:\n'
                                '        value = u8(value - 1)\n'
                                '    counters.set_byte(0, value)\n'
                                '    counters = counters.advance(1)\n'
                                'return CounterFields(counters.base, None, value, 65535)',
 '_tick_status_counter_fields': 'if type(memory) is not CounterMemory:\n'
                                "    raise ValueError('sealed counter memory required')\n"
                                'primary = memory.table(4294944340)\n'
                                'secondary = memory.table(16727490)\n'
                                'for offset in range(EDIT_COUNT_A):\n'
                                '    value = primary.byte(0)\n'
                                '    if value != 0:\n'
                                '        value = u8(value - 1)\n'
                                '        if value & 128:\n'
                                '            if value == EDIT_SPECIAL:\n'
                                '                value = 0\n'
                                '    primary.set_byte(0, value)\n'
                                '    primary = primary.advance(1)\n'
                                '    value = secondary.byte(0)\n'
                                '    if value != 0:\n'
                                '        value = u8(value - 1)\n'
                                '    secondary.set_byte(0, value)\n'
                                '    secondary = secondary.advance(1)\n'
                                'tertiary = memory.table(4294944596)\n'
                                'for offset in range(EDIT_COUNT_B):\n'
                                '    value = tertiary.byte(0)\n'
                                '    if value != 0:\n'
                                '        value = u8(value - 1)\n'
                                '    tertiary.set_byte(0, value)\n'
                                '    tertiary = tertiary.advance(1)\n'
                                'return CounterFields(tertiary.base, secondary.base, value, 65535)',
 'tick_scene_single_counters': 'from ..high_level_scene_flows.domain import Boundary, replace_byte, '
                               'replace_word\n'
                               'if type(inputs) is not SceneCounterInput:\n'
                               "    raise ValueError('actual Scene counter input required')\n"
                               'inputs.validate(state)\n'
                               'if inputs.source is None:\n'
                               "    raise Boundary('1F13C retains actual incoming A1; missing live "
                               "source')\n"
                               'fields = _tick_single_counter_fields(CounterMemory(state))\n'
                               'return SceneCounterResult(state.table_at(fields.destination), '
                               'inputs.source, replace_byte(inputs.value, fields.last_byte), '
                               'replace_word(inputs.field, fields.loop_word), False, fields.last_byte '
                               '== 0, bool(fields.last_byte & 128), False)',
 'tick_scene_status_counters': 'from ..high_level_scene_flows.domain import replace_byte, replace_word\n'
                               'if type(inputs) is not SceneCounterInput:\n'
                               "    raise ValueError('actual Scene counter input required')\n"
                               'inputs.validate(state)\n'
                               'fields = _tick_status_counter_fields(CounterMemory(state))\n'
                               'return SceneCounterResult(state.table_at(fields.destination), '
                               'state.table_at(fields.source), replace_byte(inputs.value, '
                               'fields.last_byte), replace_word(inputs.field, fields.loop_word), False, '
                               'fields.last_byte == 0, bool(fields.last_byte & 128), False)'}
ARGS = {name: (['state', 'officer'] if name == 'adjust_battle_pair_spacing' else
               ['state', 'record'] if name == 'selected_battle_roster_carry' else ['state'])
        for name in FLOW}
ARGS.update({'_tick_single_counter_fields':['memory'],'_tick_status_counter_fields':['memory'],
    'tick_scene_single_counters':['state','inputs'],'tick_scene_status_counters':['state','inputs']})


def match_flow(actual, expected, values, location):
    """Typed AST structural match; no instruction text is used by the frontend."""
    if isinstance(expected, ast.Name) and expected.id.startswith('EDIT_'):
        if not isinstance(actual, ast.Constant) or type(actual.value) is not int:
            raise CompileError(location + ': actual integer rule literal required')
        key, value = expected.id, actual.value
        if key in values and values[key] != value:
            raise CompileError(location + ': coupled comparison/arithmetic literals disagree')
        values[key] = value
        return
    if isinstance(expected, ast.AST):
        if type(actual) is not type(expected):
            raise CompileError(location + ': unsupported semantic node ' + type(actual).__name__)
        for field in expected._fields:
            match_flow(getattr(actual, field), getattr(expected, field), values, location + '.' + field)
    elif isinstance(expected, list):
        if type(actual) is not list or len(actual) != len(expected):
            raise CompileError(location + ': every control/data-flow statement must be consumed')
        for index, (left, right) in enumerate(zip(actual, expected)):
            match_flow(left, right, values, location + '[' + str(index) + ']')
    elif type(actual) is not type(expected) or actual != expected:
        raise CompileError(location + ': unsupported rule topology/value')


def analyze(source):
    if type(source) is not str:
        raise CompileError('explicit result Python text required')
    try:
        tree = ast.parse(source)
    except SyntaxError as error:
        raise CompileError('valid result Python syntax required') from error
    functions, imported = {}, set()
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and type(node.value.value) is str:
            continue
        if isinstance(node, ast.ImportFrom):
            approved = {'domain': {'PreparationState', 'u8', 'u16'},
                'contexts_counter': {'CounterMemory','CounterFields','SceneCounterInput','SceneCounterResult'}}
            if node.level != 1 or any(alias.asname or alias.name not in approved.get(node.module,set()) for alias in node.names):
                raise CompileError('explicit approved domain imports required')
            imported.update(alias.name for alias in node.names)
            continue
        if not isinstance(node, ast.FunctionDef) or node.name not in FLOW or node.name in functions:
            raise CompileError('only the complete result owners and shared counter projections are admitted')
        arguments = node.args
        if (node.decorator_list or node.returns is not None or arguments.posonlyargs or arguments.kwonlyargs
                or arguments.vararg or arguments.kwarg or arguments.defaults or arguments.kw_defaults
                or [a.arg for a in arguments.args] != ARGS[node.name]):
            raise CompileError('original fixed ABI result signature required')
        for argument in arguments.args:
            if argument.annotation is not None and not (isinstance(argument.annotation, ast.Name)
                    and argument.annotation.id == ('PreparationState' if argument.arg == 'state' else 'int')):
                raise CompileError('unsupported parameter annotation')
        functions[node.name] = node
    if set(functions) != set(FLOW):
        raise CompileError('all six result functions must be supplied')
    # range and int are real Python builtins; no implicit imported intrinsics.
    require_declared_names(functions, imported | {'range', 'int', 'type', 'bool', 'ValueError',
        'Boundary', 'replace_byte', 'replace_word'})
    plans = {}
    for name, function in functions.items():
        body = list(function.body)
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and type(body[0].value.value) is str:
            body.pop(0)
        values = {}
        match_flow(body, ast.parse(FLOW[name]).body, values, name)
        for key, value in values.items():
            low, high = (1, 65536) if key.startswith('EDIT_COUNT') else ((0, 255) if key in ('EDIT_SPECIAL', 'EDIT_REMOVED') else (0, 65535))
            if not low <= value <= high:
                raise CompileError(name + ': rule literal outside its actual encoding/domain width')
        plans[name] = values
    return plans


def lower(binding, values):
    e = Emitter(binding)
    e.begin()
    name = binding.name
    label = lambda role: name + '_' + role
    ins, mark = e.ins, lambda role: e.label(label(role))
    branch = lambda operation, role, width=4: ins(operation, label(role), width)
    if name == 'decrement_battle_3cc2_counters':
        ins('lea.l', '0xff3cc2:l,%a0', 6)
        ins('move.w', f"#{values['EDIT_COUNT']-1},%d1", 4)
        mark('tick')
        ins('move.b', '(%a0),%d0')
        branch('beq.w', 'write')
        ins('subq.b', '#1,%d0')
        mark('write')
        ins('move.b', '%d0,(%a0)+')
        ins('dbra', '%d1,' + label('tick'), 4)
    elif name == 'decrement_battle_status_counters':
        ins('lea.l', '0xa654:w,%a0', 4)
        ins('lea.l', '0xff3dc2:l,%a1', 6)
        ins('move.w', f"#{values['EDIT_COUNT_A']-1},%d1", 4)
        mark('pair_tick')
        ins('move.b', '(%a0),%d0')
        branch('beq.s', 'primary_write', 2)
        ins('subq.b', '#1,%d0')
        branch('bpl.s', 'primary_write', 2)
        ins('cmpi.b', f"#{values['EDIT_SPECIAL']},%d0", 4)
        branch('bne.s', 'primary_write', 2)
        ins('clr.b', '%d0')
        mark('primary_write')
        ins('move.b', '%d0,(%a0)+')
        ins('move.b', '(%a1),%d0')
        branch('beq.w', 'secondary_write')
        ins('subq.b', '#1,%d0')
        mark('secondary_write')
        ins('move.b', '%d0,(%a1)+')
        ins('dbra', '%d1,' + label('pair_tick'), 4)
        ins('lea.l', '0xa754:w,%a0', 4)
        ins('move.w', f"#{values['EDIT_COUNT_B']-1},%d1", 4)
        mark('tertiary_tick')
        ins('move.b', '(%a0),%d0')
        branch('beq.s', 'tertiary_write', 2)
        ins('subq.b', '#1,%d0')
        mark('tertiary_write')
        ins('move.b', '%d0,(%a0)+')
        ins('dbra', '%d1,' + label('tertiary_tick'), 4)
    elif name == 'select_battle_outcome_side':
        ins('move.w', '0xffff8114:l,%d0', 6)
        for key, role in (('EDIT_SIDE_1','first_side'),('EDIT_SIDE_2','first_side'),
                          ('EDIT_SPECIAL_1','special_mode'),('EDIT_SPECIAL_2','special_mode')):
            ins('cmpi.w', f'#{values[key]},%d0', 4)
            branch('beq.w', role)
        ins('move.w', '0xffff80e2:l,%d0', 6)
        branch('bra.w', 'commit')
        mark('first_side')
        ins('move.w', '0xffff80e0:l,%d0', 6)
        mark('commit')
        ins('clr.w', '0xf6d6:w', 4)
        ins('cmp.w', '0xf702:w,%d0', 4)
        branch('bne.w', 'done')
        ins('move.w', f"#{values['EDIT_NEXT_MODE']},0xf6d6:w", 6)
        branch('bra.w', 'done')
        mark('special_mode')
        ins('move.w', f"#{values['EDIT_MODE']},0xf362:w", 6)
        mark('done')
    elif name == 'adjust_battle_pair_spacing':
        ins('cmp.w', '0xf702:w,%d0', 4)
        branch('bne.w', 'other_is_first')
        ins('move.w', '0xf706:w,%d1', 4)
        branch('bra.w', 'coordinates')
        mark('other_is_first')
        ins('move.w', '0xf702:w,%d1', 4)
        mark('coordinates')
        ins('lea.l', '0xa150:w,%a2', 4)
        ins('move.w', '%d0,%d2')
        ins('lsl.w', '#2,%d1')
        ins('lsl.w', '#2,%d2')
        ins('clr.w', '%d3')
        for axis, reg, disp, bit, gap in (('x','%d4',0,0,values['EDIT_X_GAP']),('y','%d5',2,1,values['EDIT_Y_GAP'])):
            own = f'{disp}(%a2,%d2.w)' if disp else '(%a2,%d2.w)'
            other = f'{disp}(%a2,%d1.w)' if disp else '(%a2,%d1.w)'
            ins('move.w', own + ',' + reg, 4)
            ins('sub.w', other + ',' + reg, 4)
            branch('bcc.w', axis + '_gap')
            ins('neg.w', reg)
            ins('bset', f'#{bit},%d3', 4)
            mark(axis + '_gap')
            ins('subi.w', f'#{gap},' + reg, 4)
            branch('bcc.w', 'done')
        ins('cmp.w', '%d4,%d5')
        branch('bhi.w', 'move_y')
        ins('btst', '#0,%d3', 4)
        branch('bne.w', 'write_x')
        ins('neg.w', '%d4')
        mark('write_x')
        ins('add.w', '%d4,(%a2,%d2.w)', 4)
        branch('bra.w', 'done')
        mark('move_y')
        ins('btst', '#1,%d3', 4)
        branch('bne.w', 'write_y')
        ins('neg.w', '%d5')
        mark('write_y')
        ins('add.w', '%d5,2(%a2,%d2.w)', 4)
        mark('done')
    elif name == 'battle_pair_removed_carry':
        ins('lea.l', '0xcc00:w,%a0', 4)
        for selector in ('0xf702:w', '0xf706:w'):
            ins('move.w', selector + ',%d0', 4)
            ins('cmpi.b', f"#{values['EDIT_REMOVED']},(%a0,%d0.w)", 6)
            branch('beq.w', 'set_carry')
        ins('andi.w', '#0xfffe,%sr', 4)
        branch('bra.w', 'done')
        mark('set_carry')
        ins('ori.w', '#1,%sr', 4)
        mark('done')
    elif name == 'selected_battle_roster_carry':
        ins('move.w', '(%a1),%d2')
        ins('lea.l', '0xa5a4:w,%a2', 4)
        ins('btst.b', '#1,0xf6d7:w', 6)
        branch('bne.w', 'search')
        ins('lea.l', '0xa550:w,%a2', 4)
        mark('search')
        ins('move.w', '(%a2)+,%d3')
        branch('bmi.w', 'set_carry')
        ins('cmp.w', '%d2,%d3')
        branch('bne.s', 'search', 2)
        ins('andi.w', '#0xfffe,%sr', 4)
        branch('bra.w', 'done')
        mark('set_carry')
        ins('ori.w', '#1,%sr', 4)
        mark('done')
    else:
        raise CompileError('unknown result binding')
    e.end()
    return e.unit(dict(rule=name, editable_values=values, live_DATA_order=True,
                       original_generation_input=False, fixed_layout_ABI=True,
                       privileged_SR_boundary=name.endswith('_carry'), complete_CPU=False))


def compile_result(source):
    plans = analyze(source)
    owners = {'decrement_battle_3cc2_counters':'_tick_single_counter_fields',
        'decrement_battle_status_counters':'_tick_status_counter_fields'}
    units = [lower(binding, plans[owners.get(binding.name,binding.name)]) for binding in RESULT_BINDINGS]
    actual = {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(source).body if isinstance(n,ast.FunctionDef)}
    for unit in units:
        name=unit['binding']['name']
        if name in owners:
            unit['effects']['actual_field_algorithm']=actual[owners[name]]
            unit['effects']['actual_legacy_projection']=actual[name]
            unit['effects']['actual_scene_projection']=actual['tick_scene_single_counters' if name.endswith('3cc2_counters') else 'tick_scene_status_counters']
    if sum(len(unit['instructions']) for unit in units) != 111:
        raise CompileError('complete six-body result target required')
    return dict(units=units, new_bytes=392, reused_bytes=0, original_generation_input=False)
