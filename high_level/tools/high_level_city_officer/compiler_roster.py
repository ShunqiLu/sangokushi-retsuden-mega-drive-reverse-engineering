"""Typed whole-FLOW roster admission and ordinary M68K compatibility lowering.

The finite frontend consumes signatures, every flow node and named literal
effects. Unsupported edits fail closed. The embedded contract is Python
business grammar, not assembly/opcode/ROM data; generation performs no I/O.
"""
import ast
import copy
from .compiler_common import CompileError, Emitter, require_declared_names
from .target import ROSTER_BINDINGS, BY_NAME, TABLE_BINDINGS, SCALAR_BINDINGS

CONTRACT_SOURCE = r'''"""Live recruitment pools, roster movement and battle assignment settlement.

The public inputs are typed game state, complete WORD identifiers and live
views. List tails, wrapped offsets and unusual moving-cursor reads are kept
intentionally; a host DATA projection does not simulate the caller's stack.
"""
from .domain import (
    GameState, Table, Word, Long, CarryOutcome, descending_inclusive,
    u8, u16, u32, s16, low8, low16, replace_word, negative_word, divu_retained,
)


def initialize_recruitment_pool(state: GameState) -> None:
    state.set_next_state(27)
    state.set_allocation_pool(state.working_pool())


def commit_recruitment(state: GameState) -> None:
    index = u16(state.chosen_city() << 2)
    balances = state.balances
    balance = u32(balances.long(index) - state.cost())
    balances.set_long(index, balance)
    state.recruitment_pools.set_long(index, state.working_pool())


def settlement_progress(
    state: GameState, target_offset: Word, source_officer: Word, progress: Table,
) -> tuple[Word, Word]:
    target_offset = u16(target_offset)
    source_officer = u16(source_officer)
    doubled = u16(source_officer << 1)
    raw = progress.word(doubled)
    packed = divu_retained(u32(s16(raw)), 40)
    gain = u16(packed)
    officer = u16(doubled >> 1)
    city_index = u16(state.battle_city() << 1)
    if officer == state.city_heads.word(city_index):
        gain = u16(gain + 30)
    elif officer == state.alternate_heads.word(city_index):
        gain = u16(gain + 30)
    if state.action_flags.byte(officer) & 16:
        gain = u16(gain + 20)
    value = u16(progress.word(target_offset) + gain)
    if value > 999:
        value = u16(999)
    progress.set_word(target_offset, value)
    return value, gain


def remove_battle_roster(state: GameState, officer: Word) -> None:
    officer = u16(officer)
    if state.active_battle() == 0:
        return
    state.officer_assignments.set_byte(officer, 255)
    roster = state.battle_primary_roster.cursor()
    if officer != state.primary_officer():
        roster = state.defender_roster.cursor()
    while True:
        member = roster.next_word()
        if negative_word(member):
            return
        if u16(member & 255) == officer:
            break
    while True:
        member = roster.next_word()
        roster.set_word(65532, member)
        if negative_word(member):
            break


def apply_battle_roster_outcome(state: GameState) -> None:
    if state.active_battle() == 0:
        return
    outcome = state.outcome()
    if outcome < 6:
        return
    if outcome == 6:
        transfer_battle_roster(state, state.winning_officer())
    else:
        transfer_battle_roster(state, state.losing_officer())


def transfer_battle_roster(state: GameState, officer: Word) -> None:
    officer = u16(officer)
    source = state.defender_roster.cursor()
    target = state.secondary_transfer_roster.cursor()
    if officer == state.primary_officer():
        source = state.battle_primary_roster.cursor()
        target = state.primary_transfer_roster.cursor()
    while True:
        member = source.next_word()
        if negative_word(member):
            return
        if u16(member & 255) == officer:
            break
    while True:
        member = source.next_word()
        source.set_word(65532, member)
        if negative_word(member):
            break
    while True:
        member = target.next_word()
        if negative_word(member):
            break
    target.set_word(65534, officer)
    target.set_word(0, 65535)


def remove_original_selected_roster(state: GameState, officer: Word) -> None:
    officer = u16(officer)
    state.officer_assignments.set_byte(officer, 255)
    roster = state.battle_primary_roster.cursor()
    if officer != state.primary_officer():
        roster = state.defender_roster.cursor()
    # This older search deliberately has no negative-terminator guard.
    while True:
        member = roster.next_word()
        if u16(member & 255) == officer:
            break
    while True:
        member = roster.next_word()
        roster.set_word(65532, member)
        if negative_word(member):
            break


def assemble_defender_city_roster(state: GameState) -> Word:
    members = state.officer_flags.cursor()
    roster = state.defender_roster.cursor()
    city = state.battle_city()
    owner = u16(state.city_owners.byte(city))
    state.set_battle_owner(owner)
    doubled = u16(city << 1)
    head = state.city_heads.word(doubled)
    roster.append_word(head)
    city = u16(doubled >> 1)
    count = u16(0)
    for officer in descending_inclusive(u16(255)):
        membership = members.previous_byte()
        if membership != low8(city):
            continue
        if officer == head:
            continue
        roster.append_word(officer)
        count = u16(count + 1)
    roster.set_word(0, 65535)
    state.set_defender_count(count)
    return count


def initialize_prebattle_head_bytes(state: GameState) -> None:
    heads = state.force_heads.cursor()
    statuses = state.officer_status
    for slot in descending_inclusive(u16(15)):
        head = heads.next_word()
        if negative_word(head):
            continue
        statuses.set_byte(head, 100)


def clear_battle_assignment_state(state: GameState) -> None:
    first = state.assignment_a654.cursor()
    second = state.assignment_a754.cursor()
    third = state.assignment_ae28.cursor()
    fourth = state.assignment_ceae.cursor()
    for slot in descending_inclusive(u16(63)):
        first.append_long(0)
        second.append_long(0)
        third.append_long(0)
        fourth.append_long(0)
    state.set_clear_f6e8(65535)
    state.set_clear_f6ea(65535)
    state.set_clear_f6ec(65535)
    state.set_clear_f6ee(65535)
    state.set_clear_f6c8(0)
    state.set_clear_f6f8(0)


def copy_defender_roster_without_head(state: GameState) -> Word:
    target = state.working_roster.cursor()
    source = state.defender_tail.cursor()
    count = u16(0)
    while True:
        member = source.next_word()
        if negative_word(member):
            break
        target.append_word(member)
        count = u16(count + 1)
    target.append_word(65535)
    state.set_working_count(count)
    state.set_battle_count(count)
    return count


def ai_recruitment_capacity_gate(state: GameState) -> CarryOutcome:
    roster = state.ai_roster.cursor()
    capacities = state.capacities
    while True:
        member = roster.next_word()
        if negative_word(member):
            return state.set_carry(True)
        officer = u16(member & 255)
        offset = u16(officer << 1)
        capacity = u32(capacities.word(offset) * 100)
        moving_offset = u16(offset << 1)
        if capacity > roster.long(moving_offset):
            return state.set_carry(False)


def distribute_existing_troop_pool(state: GameState) -> CarryOutcome:
    pools = state.recruitment_pools
    index = u16(state.current_city() << 2)
    remaining = pools.long(index)
    carry = u16(0)
    if remaining != 0:
        roster = state.ai_roster.cursor()
        troops = state.troops
        capacities = state.capacities
        while True:
            member = roster.next_word()
            if negative_word(member):
                carry = u16(1)
                break
            officer = u16(member & 255)
            offset = u16(officer << 1)
            capacity = u32(capacities.word(offset) * 100)
            offset = u16(offset << 1)
            previous = troops.long(offset)
            gain = u32(capacity - previous)
            if capacity < previous:
                gain = u32(0)
            if gain > remaining:
                gain = remaining
            troops.set_long(offset, u32(troops.long(offset) + gain))
            remaining = u32(remaining - gain)
            if remaining == 0:
                break
    pools.set_long(index, remaining)
    return state.set_carry(carry != 0)


def buy_and_distribute_troops(state: GameState, retained_budget: Long) -> None:
    retained_budget = u32(retained_budget)
    roster = state.ai_roster.cursor()
    capacities = state.capacities
    balances = state.balances
    index = u16(state.current_city() << 2)
    balance = balances.long(index)
    if balance < 3000:
        return
    packed = divu_retained(balance, 200)
    quantity = low16(packed)
    remaining = replace_word(retained_budget, quantity)
    if quantity != 0:
        remaining = u32(quantity * 100)
        if remaining > 100000:
            remaining = u32(100000)
            quantity = u16(1000)
        charge = u32(quantity * 100)
        balance = u32(balance - charge)
        balances.set_long(index, balance)
        troops = state.troops
        while True:
            member = roster.next_word()
            if negative_word(member):
                break
            officer = u16(member & 255)
            offset = u16(officer << 1)
            capacity = u32(capacities.word(offset) * 100)
            offset = u16(offset << 1)
            gain = u32(capacity - troops.long(offset))
            if gain > remaining:
                gain = remaining
            troops.set_long(offset, u32(troops.long(offset) + gain))
            remaining = u32(remaining - gain)
            if remaining == 0:
                break
    index = u16(state.current_city() << 2)
    state.recruitment_pools.set_long(index, remaining)

'''

LITERAL_HOLES = {
    'initialize_recruitment_pool': {'next_state': (27, 0, 65535)},
    'settlement_progress': {'divisor': (40, 1, 65535), 'leader_bonus': (30, 0, 65535),
                            'action_bonus': (20, 0, 65535), 'cap': (999, 0, 65535)},
    'remove_battle_roster': {'assignment': (255, 0, 255)},
    'remove_original_selected_roster': {'assignment': (255, 0, 255)},
    'apply_battle_roster_outcome': {'transfer_threshold': (6, 0, 65535)},
    'initialize_prebattle_head_bytes': {'head_countdown': (15, 0, 65535), 'status': (100, 0, 255)},
    'clear_battle_assignment_state': {'countdown': (63, 0, 65535)},
    'ai_recruitment_capacity_gate': {'capacity_scale': (100, 0, 65535)},
    'distribute_existing_troop_pool': {'capacity_scale': (100, 0, 65535)},
    'buy_and_distribute_troops': {'minimum_balance': (3000, 0, 0xFFFFFFFF),
                                 'price_divisor': (200, 1, 65535), 'capacity_scale': (100, 0, 65535),
                                 'pool_cap': (100000, 0, 0xFFFFFFFF), 'capped_quantity': (1000, 0, 65535)},
}


def _without_doc(node):
    node = copy.deepcopy(node)
    if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and type(node.body[0].value.value) is str:
        node.body = node.body[1:]
    return node


def _paths(node, value, path=()):
    if isinstance(node, ast.Constant) and type(node.value) is int and node.value == value:
        yield path
    for key, child in ast.iter_fields(node):
        if isinstance(child, ast.AST):
            yield from _paths(child, value, path+(key,))
        elif isinstance(child, list):
            for index, item in enumerate(child):
                if isinstance(item, ast.AST):
                    yield from _paths(item, value, path+(key,index))


def _at(node, path):
    try:
        for part in path:
            node = node[part] if type(part) is int else getattr(node, part)
        return node
    except (AttributeError, IndexError, TypeError):
        raise CompileError('unsupported typed roster flow shape') from None


def semantic_ir(source):
    if type(source) is not str or not source or len(source) > 1048576:
        raise CompileError('one explicit finite business source str required')
    try:
        module = _without_doc(ast.parse(source))
        expected = _without_doc(ast.parse(CONTRACT_SOURCE))
    except (SyntaxError, ValueError) as error:
        raise CompileError('invalid semantic Python source') from error
    imports = set()
    functions = {}
    expected_imports = {n.name for statement in expected.body if isinstance(statement, ast.ImportFrom) for n in statement.names}
    for statement in module.body:
        if isinstance(statement, ast.ImportFrom):
            if statement.level != 1 or statement.module != 'domain':
                raise CompileError('only explicitly approved relative domain imports')
            for name in statement.names:
                if name.asname is not None or name.name not in expected_imports or name.name in imports:
                    raise CompileError('unknown, aliased or duplicate typed import')
                imports.add(name.name)
        elif isinstance(statement, ast.FunctionDef):
            if statement.name in functions:
                raise CompileError('duplicate business function')
            if statement.type_params or statement.decorator_list:
                raise CompileError('generic/decorated functions are outside this ABI')
            functions[statement.name] = statement
        else:
            raise CompileError('unsupported module statement')
    required = {b.name for b in ROSTER_BINDINGS}
    if set(functions) != required:
        raise CompileError('all14 complete roster functions required')
    require_declared_names(functions, imports)
    templates = {n.name:_without_doc(n) for n in expected.body if isinstance(n,ast.FunctionDef)}
    effects = {}
    for name, original in functions.items():
        actual = _without_doc(original)
        wanted = templates[name]
        literals = {}
        for token, (default, first, limit) in LITERAL_HOLES.get(name,{}).items():
            values = []
            for path in _paths(wanted, default):
                node = _at(actual, path)
                if not isinstance(node, ast.Constant) or type(node.value) is not int or not first <= node.value <= limit:
                    raise CompileError('strict admitted literal '+name+'.'+token)
                values.append(node.value)
                node.value = default
            if not values or len(set(values)) != 1:
                raise CompileError('repeated semantic literal effects must agree: '+name+'.'+token)
            literals[token] = values[0]
        if ast.dump(actual, include_attributes=False) != ast.dump(wanted, include_attributes=False):
            raise CompileError('unsupported signature/type/control/return/data-flow edit in '+name)
        effects[name] = dict(kind='typed_roster_flow', parameters=ast.dump(original.args,include_attributes=False),
                             result=ast.dump(original.returns,include_attributes=False),
                             consumed_AST_nodes=sum(1 for _ in ast.walk(original)), literals=literals,
                             memory='ordered live Table/Cursor effects; explicit readonly data only',
                             compiler_scope='finite whole-FLOW contract with editable typed literals',
                             caller_stack='target ABI only; host business does not simulate saved registers',
                             complete_CPU=False,natural_domain='unknown')
    return effects


def _table(name):
    item=TABLE_BINDINGS[name]
    return f"0x{item['address']&65535:x}:w" if item['suffix']=='w' else f"0x{item['address']:x}:l"


def _scalar(name, long_address=False):
    item=SCALAR_BINDINGS[name]
    return f"0x{item['address']:x}:l" if long_address else f"0x{item['address']&65535:x}:w"


def _lea(e, name, register): e.ins('lea.l',_table(name)+','+register,4)
def _branch(e, condition, label, short=False): e.ins('b'+condition+('.b' if short else '.w'),label,2 if short else 4)
def _imm(value): return '#'+str(value)


def lower(name, effects):
    binding=BY_NAME[name];e=Emitter(binding);e.begin()
    h=effects['literals']
    def ins(op, operands='', width=2): e.ins(op,operands,width)
    if name=='initialize_recruitment_pool':
        ins('move.w',_imm(h['next_state'])+','+_scalar('next_state'),6)
        ins('move.l',_scalar('working_pool')+','+_scalar('allocation_pool'),6)
    elif name=='commit_recruitment':
        ins('move.w',_scalar('chosen_city')+',%d0',4);_lea(e,'balances','%a0')
        ins('lsl.w','#2,%d0');ins('move.l','(%a0,%d0.w),%d1',4)
        ins('sub.l',_scalar('cost')+',%d1',4);ins('move.l','%d1,(%a0,%d0.w)',4)
        _lea(e,'recruitment_pools','%a0');ins('move.l',_scalar('working_pool')+',(%a0,%d0.w)',6)
    elif name=='settlement_progress':
        bonus=e.fresh('leader_bonus');flags=e.fresh('flags');target=e.fresh('target');store=e.fresh('store')
        ins('lsl.w','#1,%d1');ins('move.w','(%a3,%d1.w),%d2',4);ins('ext.l','%d2')
        ins('divu.w',_imm(h['divisor'])+',%d2',4);ins('lsr.w','#1,%d1')
        ins('move.w',_scalar('battle_city')+',%d3',4);ins('lsl.w','#1,%d3')
        _lea(e,'city_heads','%a5');ins('cmp.w','(%a5,%d3.w),%d1',4);_branch(e,'eq',bonus)
        _lea(e,'alternate_heads','%a5');ins('cmp.w','(%a5,%d3.w),%d1',4);_branch(e,'ne',flags)
        e.label(bonus);ins('addi.w',_imm(h['leader_bonus'])+',%d2',4)
        e.label(flags);_lea(e,'action_flags','%a5');ins('btst.b','#4,(%a5,%d1.w)',6)
        _branch(e,'eq',target);ins('addi.w',_imm(h['action_bonus'])+',%d2',4)
        e.label(target);ins('move.w','(%a3,%d0.w),%d3',4);ins('add.w','%d2,%d3')
        ins('cmpi.w',_imm(h['cap'])+',%d3',4);_branch(e,'ls',store)
        ins('move.w',_imm(h['cap'])+',%d3',4);e.label(store);ins('move.w','%d3,(%a3,%d0.w)',4)
    elif name=='remove_battle_roster':
        selected=e.fresh('selected');scan=e.fresh('scan');compact=e.fresh('compact');finish=e.fresh('finish')
        ins('movem.l','%d2/%a0,-(%a7)',4);ins('tst.w',_scalar('active_battle'),4);_branch(e,'eq',finish)
        _lea(e,'officer_assignments','%a0');ins('move.b',_imm(h['assignment'])+',(%a0,%d1.w)',6)
        _lea(e,'battle_primary_roster','%a0');ins('cmp.w',_scalar('primary_officer')+',%d1',4)
        _branch(e,'eq',selected);_lea(e,'defender_roster','%a0');e.label(selected);e.label(scan)
        ins('move.w','(%a0)+,%d2');_branch(e,'mi',finish);ins('andi.w','#255,%d2',4)
        ins('cmp.w','%d1,%d2');_branch(e,'ne',scan,True);e.label(compact)
        ins('move.w','(%a0)+,-4(%a0)',4);_branch(e,'pl',compact,True)
        e.label(finish);ins('movem.l','(%a7)+,%d2/%a0',4)
    elif name=='apply_battle_roster_outcome':
        other=e.fresh('other');finish=e.fresh('finish')
        ins('tst.w',_scalar('active_battle'),4);_branch(e,'eq',finish)
        ins('cmpi.w',_imm(h['transfer_threshold'])+','+_scalar('outcome',True),8)
        _branch(e,'cs',finish);_branch(e,'ne',other)
        ins('move.w',_scalar('winning_officer',True)+',%d0',6)
        ins('bsr.w','transfer_battle_roster',4);_branch(e,'ra',finish)
        e.label(other);ins('move.w',_scalar('losing_officer',True)+',%d0',6)
        ins('bsr.w','transfer_battle_roster',4);e.label(finish)
    elif name=='transfer_battle_roster':
        selected=e.fresh('selected');scan=e.fresh('scan');compact=e.fresh('compact');append=e.fresh('append');finish=e.fresh('finish')
        _lea(e,'defender_roster','%a0');_lea(e,'secondary_transfer_roster','%a1')
        ins('cmp.w',_scalar('primary_officer')+',%d0',4);_branch(e,'ne',selected)
        _lea(e,'battle_primary_roster','%a0');_lea(e,'primary_transfer_roster','%a1')
        e.label(selected);e.label(scan);ins('move.w','(%a0)+,%d1');_branch(e,'mi',finish)
        ins('andi.w','#255,%d1',4);ins('cmp.w','%d0,%d1');_branch(e,'ne',scan,True)
        e.label(compact);ins('move.w','(%a0)+,-4(%a0)',4);_branch(e,'pl',compact,True)
        e.label(append);ins('tst.w','(%a1)+');_branch(e,'pl',append,True)
        ins('move.w','%d0,-2(%a1)',4);ins('move.w','#65535,(%a1)',4);e.label(finish)
    elif name=='remove_original_selected_roster':
        selected=e.fresh('selected');scan=e.fresh('scan');compact=e.fresh('compact')
        _lea(e,'officer_assignments','%a0');ins('move.b',_imm(h['assignment'])+',(%a0,%d0.w)',6)
        _lea(e,'battle_primary_roster','%a1');ins('cmp.w',_scalar('primary_officer')+',%d0',4)
        _branch(e,'eq',selected);_lea(e,'defender_roster','%a1');e.label(selected);e.label(scan)
        ins('move.w','(%a1)+,%d1');ins('andi.w','#255,%d1',4);ins('cmp.w','%d0,%d1');_branch(e,'ne',scan,True)
        e.label(compact);ins('move.w','(%a1)+,-4(%a1)',4);_branch(e,'pl',compact,True)
    elif name=='assemble_defender_city_roster':
        scan=e.fresh('scan');skip=e.fresh('skip')
        _lea(e,'officer_flags','%a0');_lea(e,'defender_roster','%a1');_lea(e,'city_owners','%a2')
        ins('move.w',_scalar('battle_city')+',%d0',4);ins('clr.w','%d4');ins('move.b','(%a2,%d0.w),%d4',4)
        ins('move.w','%d4,'+_scalar('battle_owner'),4);_lea(e,'city_heads','%a2');ins('lsl.w','#1,%d0')
        ins('move.w','(%a2,%d0.w),%d4',4);ins('move.w','%d4,(%a1)+');ins('lsr.w','#1,%d0')
        ins('move.w','#255,%d1',4);ins('clr.w','%d3');e.label(scan);ins('move.b','-(%a0),%d2')
        ins('cmp.b','%d0,%d2');_branch(e,'ne',skip);ins('cmp.w','%d4,%d1');_branch(e,'eq',skip)
        ins('move.w','%d1,(%a1)+');ins('addq.w','#1,%d3');e.label(skip);ins('dbra','%d1,'+scan,4)
        ins('move.w','#65535,(%a1)',4);ins('move.w','%d3,'+_scalar('defender_count'),4)
    elif name=='initialize_prebattle_head_bytes':
        scan=e.fresh('scan');skip=e.fresh('skip')
        _lea(e,'force_heads','%a0');_lea(e,'officer_status','%a1');ins('move.w',_imm(h['head_countdown'])+',%d0',4)
        e.label(scan);ins('move.w','(%a0)+,%d1');_branch(e,'mi',skip)
        ins('move.b',_imm(h['status'])+',(%a1,%d1.w)',6);e.label(skip);ins('dbra','%d0,'+scan,4)
    elif name=='clear_battle_assignment_state':
        loop=e.fresh('loop')
        for table,reg in (('assignment_a654','%a0'),('assignment_a754','%a1'),('assignment_ae28','%a2'),('assignment_ceae','%a3')):
            _lea(e,table,reg)
        ins('move.w',_imm(h['countdown'])+',%d0',4);e.label(loop)
        for reg in ('%a0','%a1','%a2','%a3'):ins('clr.l','('+reg+')+')
        ins('dbra','%d0,'+loop,4)
        for scalar in ('clear_f6e8','clear_f6ea','clear_f6ec','clear_f6ee'):
            ins('move.w','#65535,'+_scalar(scalar),6)
        for scalar in ('clear_f6c8','clear_f6f8'):ins('clr.w',_scalar(scalar),4)
    elif name=='copy_defender_roster_without_head':
        scan=e.fresh('scan');finish=e.fresh('finish')
        _lea(e,'working_roster','%a0');_lea(e,'defender_tail','%a1');ins('clr.w','%d1')
        e.label(scan);ins('move.w','(%a1)+,%d2');_branch(e,'mi',finish,True)
        ins('move.w','%d2,(%a0)+');ins('addq.w','#1,%d1');_branch(e,'ra',scan,True)
        e.label(finish);ins('move.w','#65535,(%a0)+',4)
        ins('move.w','%d1,'+_scalar('working_count'),4);ins('move.w','%d1,'+_scalar('battle_count'),4)
    elif name=='ai_recruitment_capacity_gate':
        scan=e.fresh('scan');negative=e.fresh('negative');finish=e.fresh('finish')
        _lea(e,'ai_roster','%a0');_lea(e,'troops','%a1');_lea(e,'capacities','%a2')
        e.label(scan);ins('move.w','(%a0)+,%d0');_branch(e,'mi',negative)
        ins('andi.w','#255,%d0',4);ins('lsl.w','#1,%d0');ins('move.w','(%a2,%d0.w),%d1',4)
        ins('mulu.w',_imm(h['capacity_scale'])+',%d1',4);ins('lsl.w','#1,%d0')
        ins('cmp.l','(%a0,%d0.w),%d1',4);_branch(e,'ls',scan,True)
        ins('andi.w','#65534,%sr',4);_branch(e,'ra',finish)
        e.label(negative);ins('ori.w','#1,%sr',4);e.label(finish)
    elif name=='distribute_existing_troop_pool':
        scan=e.fresh('scan');no_borrow=e.fresh('no_borrow');fits=e.fresh('fits');normal=e.fresh('normal');negative=e.fresh('negative');finish=e.fresh('finish')
        _lea(e,'recruitment_pools','%a0');ins('move.w',_scalar('current_city')+',%d0',4);ins('lsl.w','#2,%d0')
        ins('move.l','(%a0,%d0.w),%d1',4);_branch(e,'eq',normal)
        _lea(e,'ai_roster','%a1');_lea(e,'troops','%a2');_lea(e,'capacities','%a3')
        e.label(scan);ins('move.w','(%a1)+,%d2');_branch(e,'mi',negative)
        ins('andi.w','#255,%d2',4);ins('lsl.w','#1,%d2');ins('move.w','(%a3,%d2.w),%d3',4)
        ins('mulu.w',_imm(h['capacity_scale'])+',%d3',4);ins('lsl.w','#1,%d2')
        ins('sub.l','(%a2,%d2.w),%d3',4);_branch(e,'cc',no_borrow);ins('moveq','#0,%d3');e.label(no_borrow)
        ins('cmp.l','%d1,%d3');_branch(e,'ls',fits);ins('move.l','%d1,%d3');e.label(fits)
        ins('add.l','%d3,(%a2,%d2.w)',4);ins('sub.l','%d3,%d1');_branch(e,'eq',normal);_branch(e,'ra',scan,True)
        e.label(normal);ins('move.l','%d1,(%a0,%d0.w)',4);ins('andi.w','#65534,%sr',4);_branch(e,'ra',finish)
        e.label(negative);ins('move.l','%d1,(%a0,%d0.w)',4);ins('ori.w','#1,%sr',4);e.label(finish)
    elif name=='buy_and_distribute_troops':
        charge=e.fresh('charge');scan=e.fresh('scan');fits=e.fresh('fits');pool=e.fresh('pool');finish=e.fresh('finish')
        _lea(e,'ai_roster','%a0');_lea(e,'capacities','%a3');_lea(e,'balances','%a1')
        ins('move.w',_scalar('current_city')+',%d0',4);ins('lsl.w','#2,%d0');ins('move.l','(%a1,%d0.w),%d3',4)
        ins('cmpi.l',_imm(h['minimum_balance'])+',%d3',6);_branch(e,'cs',finish);ins('move.l','%d3,%d1')
        ins('divu.w',_imm(h['price_divisor'])+',%d1',4);ins('move.w','%d1,%d4');_branch(e,'eq',pool)
        ins('mulu.w',_imm(h['capacity_scale'])+',%d4',4);ins('cmpi.l',_imm(h['pool_cap'])+',%d4',6)
        _branch(e,'ls',charge);ins('move.l',_imm(h['pool_cap'])+',%d4',6)
        ins('move.w',_imm(h['capped_quantity'])+',%d1',4);e.label(charge);ins('mulu.w',_imm(h['capacity_scale'])+',%d1',4)
        ins('sub.l','%d1,%d3');ins('move.l','%d3,(%a1,%d0.w)',4);_lea(e,'troops','%a2')
        e.label(scan);ins('move.w','(%a0)+,%d0');_branch(e,'mi',pool);ins('andi.w','#255,%d0',4)
        ins('lsl.w','#1,%d0');ins('move.w','(%a3,%d0.w),%d1',4);ins('mulu.w',_imm(h['capacity_scale'])+',%d1',4)
        ins('lsl.w','#1,%d0');ins('sub.l','(%a2,%d0.w),%d1',4);ins('cmp.l','%d4,%d1')
        _branch(e,'ls',fits);ins('move.l','%d4,%d1');e.label(fits);ins('add.l','%d1,(%a2,%d0.w)',4)
        ins('sub.l','%d1,%d4');_branch(e,'ne',scan,True);e.label(pool);_lea(e,'recruitment_pools','%a0')
        ins('move.w',_scalar('current_city')+',%d0',4);ins('lsl.w','#2,%d0');ins('move.l','%d4,(%a0,%d0.w)',4);e.label(finish)
    else:
        raise CompileError('unsupported typed roster effect')
    e.end()
    if e.pc!=binding.end:
        raise CompileError('typed lowering fixed extent mismatch for '+name)
    return e.unit(effects)


def compile_roster(source):
    effects=semantic_ir(source)
    units=[lower(binding.name,effects[binding.name]) for binding in ROSTER_BINDINGS]
    allocated=sum(sum(row['encoding_bytes'] for row in unit['instructions']) for unit in units)
    count=sum(len(unit['instructions']) for unit in units)
    if (allocated,count)!=(860,246):
        raise CompileError('complete14-function allocation required')
    return dict(units=units,effects=effects,allocated_bytes=allocated,instructions=count,
                original_generation_input=False,complete_CPU=False,natural_domain='unknown')


# Editable legacy data-view declaration; the full Scene/Frame provider is separate.
# GameState here is not the full register, status, and stack ABI.
DECLARATIONS = {}

DECLARATIONS.update({'initialize_prebattle_head_bytes': {'signature': 'state: GameState', 'returns': 'None', 'flow': 'heads = state.force_heads.cursor()\nstatuses = state.officer_status\nfor slot in descending_inclusive(u16(15)):\n    head = heads.next_word()\n    if negative_word(head):\n        continue\n    statuses.set_byte(head, 100)'}})
