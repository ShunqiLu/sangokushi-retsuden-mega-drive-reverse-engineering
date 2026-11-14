"""Whole semantic commit FLOW admission and ordinary 68000 ABI lowering.

Every executable AST node is consumed by a typed flow contract. Named EDIT_
holes bind actual business literals; unsupported flow or storage edits reject.
The compatibility allocation is intentionally bounded, not a general Python
compiler. No original assembly, byte image, IR, source digest or cache is read.
"""
import ast
from .compiler_common import CompileError, Emitter, require_declared_names
from .target import COMMIT_BINDINGS, BY_NAME, TABLE_BINDINGS, SCALAR_BINDINGS


FLOW = {
    'mark_selected_roster_bit14': '''
officer = u16(officer)
roster = state.roster.cursor()
while True:
    member = roster.next_word()
    if negative_word(member):
        break
    if member == officer:
        member = u16(member | EDIT_MARK_MASK)
        roster.set_word(65534, member)
        break
''',
    'commit_roster_city_assignments': '''
choose_city_head_from_roster(state)
flag_roster_b600_candidate(state)
update_roster_c700_status(state)
state.set_command(EDIT_COMMAND)
''',
    'choose_city_head_from_roster': '''
heads = state.city_heads
city_index = u16(state.current_city() << 1)
head = heads.word(city_index)
rulers = state.force_heads
ruler_index = u16(state.force_selector() << 1)
if head == rulers.word(ruler_index):
    return
roster = state.roster.cursor()
first = state.b600
second = state.b400
status = state.c300
best = u16(0)
selected = u16(65535)
while True:
    member = roster.next_word()
    if negative_word(member):
        break
    officer = u16(member & 255)
    if status.byte(officer) < EDIT_STATUS_MIN:
        continue
    index = u16(officer << 1)
    score = u16(first.word(index) + second.word(index))
    if score > best:
        best = score
        selected = officer
if not negative_word(selected):
    heads.set_word(city_index, selected)
''',
    'flag_roster_b600_candidate': '''
roster = state.roster.cursor()
attributes = state.b600
development = state.c000
best = u16(0)
selected = u16(65535)
while True:
    member = roster.next_word()
    if negative_word(member):
        break
    officer = u16(member & 255)
    index = u16(officer << 1)
    score = attributes.word(index)
    if score < EDIT_HIGH_SCORE:
        if score < EDIT_LOW_SCORE:
            continue
        if development.word(index) < EDIT_DEVELOPMENT_MIN:
            continue
    if score >= best:
        best = score
        selected = officer
if not negative_word(selected):
    flags = state.c700
    flags.set_byte(selected, u8(flags.byte(selected) | EDIT_FLAG_MASK))
''',
    'update_roster_c700_status': '''
roster = state.roster.cursor()
flags = state.c700
categories = state.c600
development = state.c000
comparison = state.be00
while True:
    member = roster.next_word()
    if negative_word(member):
        break
    officer = u16(member & 255)
    category = u16(0)
    parameter = categories.byte(officer)
    if parameter >= EDIT_BUCKET_1:
        category = u16(category + 1)
        if parameter >= EDIT_BUCKET_2:
            category = u16(category + 1)
            if parameter >= EDIT_BUCKET_3:
                category = u16(category + 1)
                if parameter >= EDIT_BUCKET_4:
                    category = u16(category + 1)
    moving_flag = u16(roster.byte(officer) & EDIT_MOVING_MASK)
    if low8(moving_flag) >= low8(category):
        continue
    index = u16(officer << 1)
    if development.word(index) < comparison.word(index):
        category = u16(category | EDIT_COMPARISON_MASK)
    previous = flags.byte(officer)
    flags.set_byte(officer, u8((previous & EDIT_PRESERVE_MASK) | low8(category)))
''',
    'commit_city_field_order': '''
gates = state.order_gates
gate_index = u16(state.current_city() << 2)
if gates.word(gate_index) < EDIT_GATE_LIMIT:
    best, selected = select_order_officer_b600(state)
    state.set_selected_officer(selected)
    if not negative_word(selected):
        prepare_city_order_amount(state)
        orders = state.city_orders
        index = u16(state.current_city() << 1)
        index = u16(index + state.current_city())
        index = u16(index << 2)
        orders.set_word(index, state.selected_officer(), 8)
        amount = state.divide_unsigned(state.order_amount(), EDIT_ORDER_DIVISOR)
        orders.set_word(index, u16(amount), 10)
        officer = state.selected_officer()
        state.officer_flags.set_byte(officer, EDIT_ACTION_FLAG)
        mark_selected_roster_bit14(state, officer)
state.set_command(EDIT_COMMAND)
''',
    'select_order_officer_b600': '''
roster = state.roster.cursor()
attributes = state.b600
best = u16(0)
selected = u16(65535)
while True:
    member = roster.next_word()
    if negative_word(member):
        break
    if member & EDIT_MARK_MASK:
        continue
    index = u16(member << 1)
    score = attributes.word(index)
    if score > best:
        best = score
        selected = member
return best, selected
''',
    'prepare_city_order_amount': '''
balances = state.city_balances
index = u16(state.current_city() << 2)
amount, remainder = state.divide_signed(balances.long(index), EDIT_SIGNED_DIVISOR)
if amount > EDIT_ORDER_CAP:
    amount = u32(EDIT_ORDER_CAP)
state.set_order_amount(amount)
''',
    'commit_officer_training': '''
best, selected = select_training_officer_c500(state)
state.set_selected_officer(selected)
if not negative_word(selected):
    prepare_officer_training_cost(state)
    balances = state.city_balances
    index = u16(state.current_city() << 2)
    balance = balances.long(index)
    if u32(balance >> 1) >= state.order_amount():
        balance = u32(balance - state.order_amount())
        balances.set_long(index, balance)
        apply_officer_training_growth(state)
        officer = state.selected_officer()
        state.officer_flags.set_byte(officer, EDIT_ACTION_FLAG)
        mark_selected_roster_bit14(state, officer)
state.set_command(EDIT_COMMAND)
''',
    'select_training_officer_c500': '''
roster = state.roster.cursor()
training = state.c500
troops = state.c800
best = u16(65535)
selected = u16(65535)
while True:
    member = roster.next_word()
    if negative_word(member):
        break
    if member & EDIT_MARK_MASK:
        continue
    index = u16(member << 2)
    if troops.long(index) == 0:
        continue
    score = training.byte(member)
    if score < low8(best):
        best = u16((best & 65280) | score)
        selected = member
return best, selected
''',
    'prepare_officer_training_cost': '''
troops = state.c800
index = u16(state.selected_officer() << 2)
packed = state.divide_unsigned(troops.long(index), EDIT_TRAINING_DIVISOR)
cost = u32(s16(u16(packed)))
state.set_order_amount(cost)
''',
    'apply_officer_training_growth': '''
state.sample_random()
index = u16(state.selected_officer() << 1)
attribute = state.b400.word(index)
weighted = u16(u16(attribute << 2) + attribute)
development = state.c000
weighted = u16(weighted + development.word(index))
factor = u16((u32(state.seed_word() << 3) >> 16) + EDIT_FACTOR_BIAS)
gain = u16(state.divide_unsigned(u32(weighted * factor), EDIT_GROWTH_DIVISOR))
officer = u16(index >> 1)
training = state.c500
total = u16(training.byte(officer) + gain)
if total > EDIT_TRAINING_CAP:
    deficit = u16(EDIT_TRAINING_CAP - total)
    gain = u16(gain - deficit)
    total = u16(EDIT_TRAINING_CAP)
training.set_byte(officer, low8(total))
index = u16(officer << 1)
development.set_word(index, u16(development.word(index) + gain))
if development.word(index) > EDIT_DEVELOPMENT_CAP:
    development.set_word(index, EDIT_DEVELOPMENT_CAP)
''',
}
IMPORTS = {'AiState', 'Word', 'low8', 'negative_word', 's16', 'u8', 'u16', 'u32'}
PAIR_FUNCTIONS = {'select_order_officer_b600', 'select_training_officer_c500'}
BYTE_HOLES = {'EDIT_STATUS_MIN', 'EDIT_BUCKET_1', 'EDIT_BUCKET_2', 'EDIT_BUCKET_3',
              'EDIT_BUCKET_4', 'EDIT_PRESERVE_MASK', 'EDIT_ACTION_FLAG', 'EDIT_MOVING_MASK'}
BIT_HOLES = {'EDIT_MARK_MASK', 'EDIT_FLAG_MASK', 'EDIT_COMPARISON_MASK'}


def match_flow(actual, expected, values, location):
    if isinstance(expected, ast.Name) and expected.id.startswith('EDIT_'):
        if not isinstance(actual, ast.Constant) or type(actual.value) is not int:
            raise CompileError(location + ': an actual complete integer rule literal is required')
        key, value = expected.id, actual.value
        if key in values and values[key] != value:
            raise CompileError(location + ': repeated business-rule literals must agree')
        values[key] = value
    elif isinstance(expected, ast.AST):
        if type(actual) is not type(expected):
            raise CompileError(location + ': unsupported semantic node ' + type(actual).__name__)
        for field in expected._fields:
            match_flow(getattr(actual, field), getattr(expected, field), values, location + '.' + field)
    elif isinstance(expected, list):
        if type(actual) is not list or len(actual) != len(expected):
            raise CompileError(location + ': every executable statement must be consumed')
        for index, (left, right) in enumerate(zip(actual, expected)):
            match_flow(left, right, values, location + '[' + str(index) + ']')
    elif type(actual) is not type(expected) or actual != expected:
        raise CompileError(location + ': unsupported complete flow/storage value')


def signature(name):
    extra = ', officer: Word' if name == 'mark_selected_roster_bit14' else ''
    result = 'tuple[Word, Word]' if name in PAIR_FUNCTIONS else 'None'
    return ast.parse('def ' + name + '(state: AiState' + extra + ') -> ' + result + ':\n    pass').body[0]


def analyze(source):
    if type(source) is not str:
        raise CompileError('explicit commit Python text is required')
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError) as error:
        raise CompileError('valid explicit commit syntax is required') from error
    functions, imported = {}, set()
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and type(node.value.value) is str:
            continue
        if isinstance(node, ast.ImportFrom):
            if (node.level != 1 or node.module != 'domain'
                    or any(a.asname or a.name not in IMPORTS for a in node.names)):
                raise CompileError('approved explicit domain imports only')
            imported.update(a.name for a in node.names)
            continue
        if not isinstance(node, ast.FunctionDef) or node.name not in FLOW or node.name in functions:
            raise CompileError('exactly the twelve distinct complete commit functions are required')
        wanted = signature(node.name)
        if (node.decorator_list or node.type_comment is not None or getattr(node, 'type_params', ())
                or ast.dump(node.args) != ast.dump(wanted.args)
                or ast.dump(node.returns) != ast.dump(wanted.returns)):
            raise CompileError('complete declared commit signature/return-width contract required')
        functions[node.name] = node
    if set(functions) != set(FLOW):
        raise CompileError('all twelve commit functions must be supplied')
    require_declared_names(functions, imported)
    plans = {}
    for name, node in functions.items():
        body = list(node.body)
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and type(body[0].value.value) is str:
            body.pop(0)
        values = {}
        match_flow(body, ast.parse(FLOW[name]).body, values, name)
        for key, value in values.items():
            high = 255 if key in BYTE_HOLES else 0xFFFFFFFF if key == 'EDIT_ORDER_CAP' else 65535
            if type(value) is not int or not 0 <= value <= high:
                raise CompileError(name + ': complete rule value outside admitted target width')
            if key in BIT_HOLES and (value == 0 or value & (value - 1) or value > (128 if key == 'EDIT_FLAG_MASK' else 32768)):
                raise CompileError(name + ': target bit operation needs one admitted single bit')
            if key == 'EDIT_SIGNED_DIVISOR' and not 1 <= value <= 127:
                raise CompileError(name + ': positive signed MOVEQ divisor 1..127 required')
            if key == 'EDIT_FACTOR_BIAS' and value > 65535:
                raise CompileError(name + ': complete factor WORD required')
        plans[name] = values
    return plans


def lower(binding, values):
    e = Emitter(binding)
    e.begin()
    name = binding.name
    ins = e.ins
    label = lambda role: name + '_' + role
    mark = lambda role: e.label(label(role))
    branch = lambda op, role, width=4: ins(op, label(role), width)

    def view(view_name):
        spec = TABLE_BINDINGS[view_name]
        address = spec['address'] & 65535 if spec['suffix'] == 'w' else spec['address']
        return '0x' + format(address, 'x') + ':' + spec['suffix']

    def scalar(scalar_name):
        spec = SCALAR_BINDINGS[scalar_name]
        return '0x' + format(spec['address'] & 65535, 'x') + ':' + spec['suffix']

    def lea(view_name, register):
        ins('lea.l', view(view_name) + ',' + register, 4 if TABLE_BINDINGS[view_name]['suffix'] == 'w' else 6)

    def call(function, form='bsr.w'):
        target = BY_NAME[function]
        ins(form, function if form == 'bsr.w' else '0x' + format(target.entry, 'x') + ':l', 4 if form == 'bsr.w' else 6)

    def bit(mask):
        return mask.bit_length() - 1

    if name == 'mark_selected_roster_bit14':
        ins('movem.l', '%a0,-(%a7)', 4)
        lea('roster', '%a0')
        mark('scan')
        ins('move.w', '(%a0)+,%d1')
        branch('bmi.w', 'done')
        ins('cmp.w', '%d0,%d1')
        branch('bne.b', 'scan', 2)
        ins('bset.l', '#' + str(bit(values['EDIT_MARK_MASK'])) + ',%d1', 4)
        ins('move.w', '%d1,-2(%a0)', 4)
        mark('done')
        ins('movem.l', '(%a7)+,%a0', 4)
    elif name == 'commit_roster_city_assignments':
        for child in ('choose_city_head_from_roster', 'flag_roster_b600_candidate', 'update_roster_c700_status'):
            call(child)
        ins('move.w', '#' + str(values['EDIT_COMMAND']) + ',' + scalar('command'), 6)
    elif name == 'choose_city_head_from_roster':
        lea('city_heads', '%a4')
        ins('move.w', scalar('current_city') + ',%d7', 4)
        ins('lsl.w', '#1,%d7')
        ins('move.w', '(%a4,%d7.w),%d0', 4)
        lea('force_heads', '%a5')
        ins('move.w', scalar('force_selector') + ',%d1', 4)
        ins('lsl.w', '#1,%d1')
        ins('cmp.w', '(%a5,%d1.w),%d0', 4)
        branch('beq.w', 'done')
        for table, register in (('roster','%a0'), ('b600','%a1'), ('b400','%a2'), ('c300','%a3')):
            lea(table, register)
        ins('clr.w', '%d0')
        ins('move.w', '#65535,%d1', 4)
        mark('scan')
        ins('move.w', '(%a0)+,%d2')
        branch('bmi.w', 'finish_scan')
        ins('andi.w', '#255,%d2', 4)
        ins('cmpi.b', '#' + str(values['EDIT_STATUS_MIN']) + ',(%a3,%d2.w)', 6)
        branch('bcs.b', 'scan', 2)
        ins('move.w', '%d2,%d4')
        ins('lsl.w', '#1,%d4')
        ins('move.w', '(%a1,%d4.w),%d3', 4)
        ins('add.w', '(%a2,%d4.w),%d3', 4)
        ins('cmp.w', '%d0,%d3')
        branch('bls.b', 'scan', 2)
        ins('move.w', '%d3,%d0')
        ins('move.w', '%d2,%d1')
        branch('bra.b', 'scan', 2)
        mark('finish_scan')
        ins('tst.w', '%d1')
        branch('bmi.w', 'done')
        ins('move.w', '%d1,(%a4,%d7.w)', 4)
        mark('done')
    elif name == 'flag_roster_b600_candidate':
        for table, register in (('roster','%a0'), ('b600','%a1'), ('c000','%a2')):
            lea(table, register)
        ins('clr.w', '%d0')
        ins('move.w', '#65535,%d1', 4)
        mark('scan')
        ins('move.w', '(%a0)+,%d2')
        branch('bmi.b', 'finish_scan', 2)
        ins('andi.w', '#255,%d2', 4)
        ins('move.w', '%d2,%d3')
        ins('lsl.w', '#1,%d3')
        ins('move.w', '(%a1,%d3.w),%d4', 4)
        ins('cmpi.w', '#' + str(values['EDIT_HIGH_SCORE']) + ',%d4', 4)
        branch('bcc.w', 'eligible')
        ins('cmpi.w', '#' + str(values['EDIT_LOW_SCORE']) + ',%d4', 4)
        branch('bcs.b', 'scan', 2)
        ins('cmpi.w', '#' + str(values['EDIT_DEVELOPMENT_MIN']) + ',(%a2,%d3.w)', 6)
        branch('bcs.b', 'scan', 2)
        mark('eligible')
        ins('cmp.w', '%d0,%d4')
        branch('bcs.b', 'scan', 2)
        ins('move.w', '%d4,%d0')
        ins('move.w', '%d2,%d1')
        branch('bra.b', 'scan', 2)
        mark('finish_scan')
        ins('tst.w', '%d1')
        branch('bmi.w', 'done')
        lea('c700', '%a0')
        ins('bset.b', '#' + str(bit(values['EDIT_FLAG_MASK'])) + ',(%a0,%d1.w)', 6)
        mark('done')
    elif name == 'update_roster_c700_status':
        for table, register in (('roster','%a0'), ('c700','%a1'), ('c600','%a2'), ('c000','%a3'), ('be00','%a4')):
            lea(table, register)
        mark('scan')
        ins('move.w', '(%a0)+,%d0')
        branch('bmi.w', 'done')
        ins('andi.w', '#255,%d0', 4)
        ins('clr.w', '%d1')
        ins('move.b', '(%a2,%d0.w),%d2', 4)
        for index in range(1, 5):
            ins('cmpi.b', '#' + str(values['EDIT_BUCKET_' + str(index)]) + ',%d2', 4)
            branch('bcs.w', 'bucket_ready')
            ins('addq.w', '#1,%d1')
        mark('bucket_ready')
        ins('move.b', '(%a0,%d0.w),%d2', 4)
        ins('andi.w', '#' + str(values['EDIT_MOVING_MASK']) + ',%d2', 4)
        ins('cmp.b', '%d1,%d2')
        branch('bcc.b', 'scan', 2)
        ins('move.w', '%d0,%d2')
        ins('lsl.w', '#1,%d2')
        ins('move.w', '(%a3,%d2.w),%d3', 4)
        ins('cmp.w', '(%a4,%d2.w),%d3', 4)
        branch('bcc.w', 'store')
        ins('bset.l', '#' + str(bit(values['EDIT_COMPARISON_MASK'])) + ',%d1', 4)
        mark('store')
        ins('move.b', '(%a1,%d0.w),%d2', 4)
        ins('andi.b', '#' + str(values['EDIT_PRESERVE_MASK']) + ',%d2', 4)
        ins('or.b', '%d1,%d2')
        ins('move.b', '%d2,(%a1,%d0.w)', 4)
        branch('bra.b', 'scan', 2)
        mark('done')
    elif name == 'commit_city_field_order':
        lea('order_gates', '%a0')
        ins('move.w', scalar('current_city') + ',%d0', 4)
        ins('lsl.w', '#2,%d0')
        ins('cmpi.w', '#' + str(values['EDIT_GATE_LIMIT']) + ',(%a0,%d0.w)', 6)
        branch('bcc.w', 'done')
        call('select_order_officer_b600')
        ins('move.w', '%d1,' + scalar('selected_officer'), 4)
        branch('bmi.w', 'done')
        call('prepare_city_order_amount')
        lea('city_orders', '%a0')
        ins('move.w', scalar('current_city') + ',%d0', 4)
        ins('lsl.w', '#1,%d0')
        ins('add.w', scalar('current_city') + ',%d0', 4)
        ins('lsl.w', '#2,%d0')
        ins('move.w', scalar('selected_officer') + ',8(%a0,%d0.w)', 6)
        ins('move.l', scalar('order_amount') + ',%d1', 4)
        ins('divu.w', '#' + str(values['EDIT_ORDER_DIVISOR']) + ',%d1', 4)
        ins('move.w', '%d1,10(%a0,%d0.w)', 4)
        ins('move.w', scalar('selected_officer') + ',%d0', 4)
        lea('officer_flags', '%a0')
        ins('move.b', '#' + str(values['EDIT_ACTION_FLAG']) + ',(%a0,%d0.w)', 6)
        call('mark_selected_roster_bit14')
        mark('done')
        ins('move.w', '#' + str(values['EDIT_COMMAND']) + ',' + scalar('command'), 6)
    elif name == 'select_order_officer_b600':
        lea('roster', '%a0')
        lea('b600', '%a1')
        ins('clr.w', '%d0')
        ins('move.w', '#65535,%d1', 4)
        mark('scan')
        ins('move.w', '(%a0)+,%d2')
        branch('bmi.w', 'done')
        ins('btst.l', '#' + str(bit(values['EDIT_MARK_MASK'])) + ',%d2', 4)
        branch('bne.b', 'scan', 2)
        ins('move.w', '%d2,%d3')
        ins('lsl.w', '#1,%d3')
        ins('move.w', '(%a1,%d3.w),%d3', 4)
        ins('cmp.w', '%d0,%d3')
        branch('bls.b', 'scan', 2)
        ins('move.w', '%d3,%d0')
        ins('move.w', '%d2,%d1')
        branch('bra.b', 'scan', 2)
        mark('done')
    elif name == 'prepare_city_order_amount':
        lea('city_balances', '%a0')
        ins('move.w', scalar('current_city') + ',%d0', 4)
        ins('lsl.w', '#2,%d0')
        ins('move.l', '(%a0,%d0.w),%d1', 4)
        ins('moveq', '#' + str(values['EDIT_SIGNED_DIVISOR']) + ',%d2')
        call('signed_divmod', 'jsr')
        ins('cmpi.l', '#' + str(values['EDIT_ORDER_CAP']) + ',%d1', 6)
        branch('bls.w', 'store')
        ins('move.l', '#' + str(values['EDIT_ORDER_CAP']) + ',%d1', 6)
        mark('store')
        ins('move.l', '%d1,' + scalar('order_amount'), 4)
    elif name == 'commit_officer_training':
        call('select_training_officer_c500')
        ins('move.w', '%d1,' + scalar('selected_officer'), 4)
        branch('bmi.w', 'done')
        call('prepare_officer_training_cost')
        lea('city_balances', '%a0')
        ins('move.w', scalar('current_city') + ',%d0', 4)
        ins('lsl.w', '#2,%d0')
        ins('move.l', '(%a0,%d0.w),%d1', 4)
        ins('move.l', '%d1,%d2')
        ins('lsr.l', '#1,%d2')
        ins('cmp.l', scalar('order_amount') + ',%d2', 4)
        branch('bcs.w', 'done')
        ins('sub.l', scalar('order_amount') + ',%d1', 4)
        ins('move.l', '%d1,(%a0,%d0.w)', 4)
        call('apply_officer_training_growth')
        ins('move.w', scalar('selected_officer') + ',%d0', 4)
        lea('officer_flags', '%a0')
        ins('move.b', '#' + str(values['EDIT_ACTION_FLAG']) + ',(%a0,%d0.w)', 6)
        call('mark_selected_roster_bit14')
        mark('done')
        ins('move.w', '#' + str(values['EDIT_COMMAND']) + ',' + scalar('command'), 6)
    elif name == 'select_training_officer_c500':
        for table, register in (('roster','%a0'), ('c500','%a1'), ('c800','%a2')):
            lea(table, register)
        ins('move.w', '#65535,%d0', 4)
        ins('move.w', '#65535,%d1', 4)
        mark('scan')
        ins('move.w', '(%a0)+,%d2')
        branch('bmi.w', 'done')
        ins('btst.l', '#' + str(bit(values['EDIT_MARK_MASK'])) + ',%d2', 4)
        branch('bne.b', 'scan', 2)
        ins('move.w', '%d2,%d3')
        ins('lsl.w', '#2,%d3')
        ins('tst.l', '(%a2,%d3.w)', 4)
        branch('beq.b', 'scan', 2)
        ins('move.b', '(%a1,%d2.w),%d3', 4)
        ins('cmp.b', '%d0,%d3')
        branch('bcc.b', 'scan', 2)
        ins('move.b', '%d3,%d0')
        ins('move.w', '%d2,%d1')
        branch('bra.b', 'scan', 2)
        mark('done')
    elif name == 'prepare_officer_training_cost':
        lea('c800', '%a0')
        ins('move.w', scalar('selected_officer') + ',%d0', 4)
        ins('lsl.w', '#2,%d0')
        ins('move.l', '(%a0,%d0.w),%d1', 4)
        ins('divu.w', '#' + str(values['EDIT_TRAINING_DIVISOR']) + ',%d1', 4)
        ins('ext.l', '%d1')
        ins('move.l', '%d1,' + scalar('order_amount'), 4)
    elif name == 'apply_officer_training_growth':
        call('random_sample', 'jsr')
        ins('move.w', scalar('selected_officer') + ',%d0', 4)
        ins('lsl.w', '#1,%d0')
        lea('b400', '%a0')
        ins('move.w', '(%a0,%d0.w),%d2', 4)
        ins('move.w', '%d2,%d1')
        ins('lsl.w', '#2,%d2')
        ins('add.w', '%d1,%d2')
        lea('c000', '%a0')
        ins('add.w', '(%a0,%d0.w),%d2', 4)
        ins('moveq', '#0,%d1')
        ins('move.w', scalar('seed_word') + ',%d1', 4)
        ins('lsl.l', '#3,%d1')
        ins('swap', '%d1')
        ins('addi.w', '#' + str(values['EDIT_FACTOR_BIAS']) + ',%d1', 4)
        ins('mulu.w', '%d1,%d2')
        ins('divu.w', '#' + str(values['EDIT_GROWTH_DIVISOR']) + ',%d2', 4)
        ins('lsr.w', '#1,%d0')
        lea('c500', '%a0')
        ins('clr.w', '%d1')
        ins('move.b', '(%a0,%d0.w),%d1', 4)
        ins('add.w', '%d2,%d1')
        ins('cmpi.w', '#' + str(values['EDIT_TRAINING_CAP']) + ',%d1', 4)
        branch('bls.b', 'store', 2)
        ins('move.w', '#' + str(values['EDIT_TRAINING_CAP']) + ',%d3', 4)
        ins('sub.w', '%d1,%d3')
        ins('sub.w', '%d3,%d2')
        ins('move.w', '#' + str(values['EDIT_TRAINING_CAP']) + ',%d1', 4)
        mark('store')
        ins('move.b', '%d1,(%a0,%d0.w)', 4)
        ins('lsl.w', '#1,%d0')
        lea('c000', '%a0')
        ins('add.w', '%d2,(%a0,%d0.w)', 4)
        ins('cmpi.w', '#' + str(values['EDIT_DEVELOPMENT_CAP']) + ',(%a0,%d0.w)', 6)
        branch('bls.b', 'done', 2)
        ins('move.w', '#' + str(values['EDIT_DEVELOPMENT_CAP']) + ',(%a0,%d0.w)', 6)
        mark('done')
    else:
        raise CompileError('unsupported complete commit operation')
    e.end()
    unit = e.unit({'kind': 'typed_complete_commit_flow', 'function': name, 'rule_literals': values,
                   'flow': ast.dump(ast.parse(FLOW[name])), 'live_DATA': True,
                   'ABI_stack_owned_by_target': name == 'mark_selected_roster_bit14',
                   'complete_CPU': False})
    if sum(row['encoding_bytes'] for row in unit['instructions']) != binding.end - binding.entry:
        raise CompileError(name + ': semantic lowering changed its fixed allocation')
    return unit


def compile_commit(source):
    plans = analyze(source)
    units = [lower(binding, plans[binding.name]) for binding in COMMIT_BINDINGS]
    return {'units': units, 'effects': {u['binding']['name']: u['effects'] for u in units},
            'allocated_bytes': sum(b.end - b.entry for b in COMMIT_BINDINGS),
            'original_generation_input': False, 'complete_CPU': False}
