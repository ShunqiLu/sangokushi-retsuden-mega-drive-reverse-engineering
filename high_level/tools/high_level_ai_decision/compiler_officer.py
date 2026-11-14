"""Restricted semantic-flow compiler for the eight ordered officer queries.

FLOW is a complete structured-Python admission contract, not an opcode source.
Every accepted statement, annotation, call and return is consumed.  Two typed
rule holes are editable without changing the supported control/storage shape.
Unknown edits fail closed.  Lowering below selects ordinary GNU mnemonics from
the admitted operations and separate target ABI; it reads no files or images.
"""
import ast
from copy import deepcopy
from dataclasses import asdict

from .compiler_common import CompileError, Emitter
from .target import OFFICER_BINDINGS


# Semantic contracts deliberately contain no target PCs, registers or opcodes.
FLOW = '''
def select_roster_attribute_max(state: AiState) -> tuple[Word, Word, Word]:
    roster = state.roster.cursor()
    attributes = state.b600
    best = u16(0)
    selected = u16(65535)
    while True:
        member = roster.next_word()
        if negative_word(member):
            break
        if member & 16384:
            continue
        index = u16(member << 1)
        score = attributes.word(index)
        if score > best:
            best = score
            selected = u16(index >> 1)
    return best, selected, member

def select_foreign_nonruler_attribute_sum(state: AiState) -> tuple[Word, Word, Word]:
    neighbors = state.neighbors.at(u16(state.current_city() << 3)).cursor()
    first = state.b600
    second = state.b400
    owners = state.city_owners
    processed = state.city_processed
    status = state.c300
    best = u16(0)
    selected = u16(65535)
    selected_city = u16(65535)
    while True:
        city = u16(neighbors.next_byte())
        if negative_byte(city):
            break
        owner = u16(owners.byte(city))
        if negative_byte(owner):
            continue
        if owner == state.force_selector():
            continue
        if processed.byte(city) != 0:
            continue
        best, selected, selected_city = scan_nonruler_city_attribute_sum(
            state, city, best, selected, selected_city, first, second, status,
        )
    return best, selected, selected_city

def scan_nonruler_city_attribute_sum(
    state: AiState, city: Word, best: Word, selected: Word,
    selected_city: Word, first: Table, second: Table, status: Table,
) -> tuple[Word, Word, Word]:
    city = u16(city)
    best = u16(best)
    selected = u16(selected)
    selected_city = u16(selected_city)
    owner = u16(state.city_owners.byte(city))
    head = state.force_heads.word(u16(owner << 1))
    membership = state.officer_flags.cursor()
    for officer in descending_inclusive(u16(255)):
        if officer == head:
            continue
        if low8(city) != membership.previous_byte():
            continue
        if status.byte(officer) >= 95:
            continue
        index = u16(officer << 1)
        score = u16(first.word(index) + second.word(index))
        if score > best:
            best = score
            selected = officer
            selected_city = city
    return best, selected, selected_city

def selected_city_has_player_owner(state: AiState) -> CarryOutcome:
    owners = state.city_owners
    city = state.selected_city()
    owner = owners.byte(city)
    if owner == state.player_first():
        return state.carry_result(1)
    if owner == state.player_second():
        return state.carry_result(1)
    if owner == state.player_third():
        return state.carry_result(1)
    return state.carry_result(0)

def selected_player_officer_removed_gate(state: AiState) -> CarryOutcome:
    owners = state.city_owners
    city = state.selected_city()
    owner = owners.byte(city)
    if (owner == state.player_first() or owner == state.player_second()
            or owner == state.player_third()):
        officer = state.selected_officer()
        membership = state.officer_assignments.byte(officer)
        if membership == 255:
            return state.carry_result(1)
    return state.carry_result(0)

def select_player_neighbor_head_attribute_min(state: AiState) -> tuple[Word, Word, Word]:
    neighbors = state.neighbors.at(u16(state.current_city() << 3)).cursor()
    owners = state.city_owners
    attributes = state.b600
    heads = state.city_heads
    processed = state.city_processed
    best = u16(65535)
    selected = u16(65535)
    while True:
        city = u16(neighbors.next_byte())
        if negative_byte(city):
            break
        if processed.byte(city) != 0:
            continue
        owner = owners.byte(city)
        if (owner != state.player_first() and owner != state.player_second()
                and owner != state.player_third()):
            continue
        index = u16(city << 1)
        head = heads.word(index)
        head_index = u16(head << 1)
        score = attributes.word(head_index)
        if score < best:
            best = score
            selected = city
    return best, selected, city

def select_and_mark_roster_attribute_max(
    state: AiState, last_member: Word,
) -> tuple[Word, Word, Word]:
    last_member = u16(last_member)
    roster = state.roster.cursor()
    attributes = state.b600
    best = u16(0)
    selected = u16(65535)
    if negative_word(state.roster.word(u16(2))):
        return best, selected, last_member
    while True:
        last_member = roster.next_word()
        if negative_word(last_member):
            break
        if last_member & 16384:
            continue
        index = u16(last_member << 1)
        score = attributes.word(index)
        if score > best:
            best = score
            selected = last_member
    if negative_word(selected):
        return best, selected, last_member
    state.officer_flags.set_byte(selected, 1)
    roster = state.roster.cursor()
    while True:
        last_member = roster.next_word()
        if negative_word(last_member):
            break
        if last_member == selected:
            last_member = u16(last_member | 16384)
            roster.set_word(u16(65534), last_member)
            break
    return best, selected, last_member

def select_roster_attribute_max_preserving_id(state: AiState) -> tuple[Word, Word, Word]:
    roster = state.roster.cursor()
    attributes = state.b600
    best = u16(0)
    selected = u16(65535)
    while True:
        member = roster.next_word()
        if negative_word(member):
            break
        if member & 16384:
            continue
        index = u16(member << 1)
        score = attributes.word(index)
        if score > best:
            best = score
            selected = member
    return best, selected, member
'''

APPROVED_IMPORTS = {
    'AiState', 'CarryOutcome', 'Table', 'Word', 'descending_inclusive',
    'low8', 'negative_byte', 'negative_word', 'u16',
}


def _strip_docs(node):
    node = deepcopy(node)
    if (node.body and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and type(node.body[0].value.value) is str):
        node.body.pop(0)
    return node


def _typed_holes(function):
    """Replace only recognized semantic rule positions, retaining exact types."""
    holes = {}
    if function.name == 'scan_nonruler_city_attribute_sum':
        candidates = [node for node in ast.walk(function)
                      if isinstance(node, ast.Compare)
                      and isinstance(node.left, ast.Call)
                      and ast.dump(node.left.func) == ast.dump(ast.Attribute(
                          value=ast.Name(id='status', ctx=ast.Load()),
                          attr='byte', ctx=ast.Load()))]
        if len(candidates) != 1 or len(candidates[0].comparators) != 1:
            raise CompileError('one live status-threshold comparison is required')
        node = candidates[0].comparators[0]
        if not isinstance(node, ast.Constant) or type(node.value) is not int or not 0 <= node.value <= 255:
            raise CompileError('status threshold must be an unsigned BYTE literal')
        holes['status_threshold'] = node.value
        candidates[0].comparators[0] = ast.Name(id='__status_threshold', ctx=ast.Load())
    if function.name == 'select_and_mark_roster_attribute_max':
        candidates = [node for node in ast.walk(function)
                      if isinstance(node, ast.Call)
                      and ast.dump(node.func) == ast.dump(ast.Attribute(
                          value=ast.Attribute(value=ast.Name(id='state', ctx=ast.Load()),
                                              attr='officer_flags', ctx=ast.Load()),
                          attr='set_byte', ctx=ast.Load()))]
        if len(candidates) != 1 or len(candidates[0].args) != 2:
            raise CompileError('one ordered officer flag write is required')
        node = candidates[0].args[1]
        if not isinstance(node, ast.Constant) or type(node.value) is not int or not 0 <= node.value <= 255:
            raise CompileError('candidate flag must be an unsigned BYTE literal')
        holes['candidate_flag'] = node.value
        candidates[0].args[1] = ast.Name(id='__candidate_flag', ctx=ast.Load())
    return holes


def semantic_ir(source):
    if type(source) is not str:
        raise CompileError('source must be a text string')
    try:
        module = ast.parse(source)
    except SyntaxError as exc:
        raise CompileError('invalid structured Python source') from exc
    imported = set()
    functions = {}
    for node in _strip_docs(module).body:
        if isinstance(node, ast.ImportFrom):
            if node.level != 1 or node.module != 'domain':
                raise CompileError('only the explicit domain imports are supported')
            for alias in node.names:
                if alias.asname is not None or alias.name not in APPROVED_IMPORTS:
                    raise CompileError('unsupported imported name')
                imported.add(alias.name)
        elif isinstance(node, ast.FunctionDef):
            if node.name in functions:
                raise CompileError('duplicate function')
            functions[node.name] = _strip_docs(node)
        else:
            raise CompileError('only declared business functions and imports are supported')
    expected = {node.name: node for node in ast.parse(FLOW).body}
    if set(functions) != set(expected):
        raise CompileError('the complete eight-function officer contract is required')
    records = []
    for name, contract in expected.items():
        function = functions[name]
        local = {arg.arg for arg in function.args.args}
        local.update(node.id for node in ast.walk(function)
                     if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store))
        loaded = {node.id for node in ast.walk(function)
                  if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)}
        if loaded - local - imported - set(functions) - {'tuple'}:
            raise CompileError('used names must have actual imports or local declarations')
        normalized = deepcopy(function)
        holes = _typed_holes(normalized)
        _typed_holes(contract)
        if ast.dump(normalized, include_attributes=False) != ast.dump(contract, include_attributes=False):
            raise CompileError(f'{name}: unsupported control, width, storage, call or return edit')
        effects = [{'operation': type(node).__name__,
                    'semantic': ast.dump(node, include_attributes=False)}
                   for node in ast.walk(function)
                   if isinstance(node, (ast.stmt, ast.Call, ast.Compare, ast.BinOp))]
        records.append({'name': name, 'holes': holes, 'effects': effects})
    return records


def _view(emitter, address, register, long=False):
    emitter.ins('lea.l', f'0x{address:x}:{"l" if long else "w"},%{register}', 6 if long else 4)


def _word_constant(emitter, value, register):
    if value == 0:
        emitter.ins('clr.w', f'%{register}', 2)
    else:
        emitter.ins('move.w', f'#0x{value:x},%{register}', 4)


def _roster_query(emitter, preserve_identity, marking, holes):
    _view(emitter, 0xf72a, 'a0')
    _view(emitter, 0xb600, 'a1')
    _word_constant(emitter, 0, 'd0')
    _word_constant(emitter, 65535, 'd1')
    loop = emitter.fresh('next_member')
    after = emitter.fresh('selection_complete')
    finish = emitter.fresh('return')
    if marking:
        emitter.ins('tst.w', '0xf72c:w', 4)
        emitter.ins('bmi.w', finish, 4)
    emitter.label(loop)
    emitter.ins('move.w', '(%a0)+,%d2', 2)
    emitter.ins('bmi.w', after, 4)
    emitter.ins('btst.l', '#14,%d2', 4)
    emitter.ins('bne.b', loop, 2)
    if preserve_identity:
        emitter.ins('move.w', '%d2,%d3', 2)
        emitter.ins('lsl.w', '#1,%d3', 2)
        emitter.ins('move.w', '(%a1,%d3.w),%d3', 4)
    else:
        emitter.ins('lsl.w', '#1,%d2', 2)
        emitter.ins('move.w', '(%a1,%d2.w),%d3', 4)
    emitter.ins('cmp.w', '%d0,%d3', 2)
    emitter.ins('bls.b', loop, 2)
    emitter.ins('move.w', '%d3,%d0', 2)
    if not preserve_identity:
        emitter.ins('lsr.w', '#1,%d2', 2)
    emitter.ins('move.w', '%d2,%d1', 2)
    emitter.ins('bra.b', loop, 2)
    emitter.label(after)
    if marking:
        emitter.ins('tst.w', '%d1', 2)
        emitter.ins('bmi.w', finish, 4)
        _view(emitter, 0xcd00, 'a1')
        emitter.ins('move.b', f'#{holes["candidate_flag"]},(%a1,%d1.w)', 6)
        _view(emitter, 0xf72a, 'a0')
        mark = emitter.fresh('find_selected_live')
        emitter.label(mark)
        emitter.ins('move.w', '(%a0)+,%d2', 2)
        emitter.ins('bmi.w', finish, 4)
        emitter.ins('cmp.w', '%d1,%d2', 2)
        emitter.ins('bne.b', mark, 2)
        emitter.ins('bset.l', '#14,%d2', 4)
        emitter.ins('move.w', '%d2,-2(%a0)', 4)
    emitter.label(finish)


def _neighbor_cursor(emitter):
    _view(emitter, 0xd4bda, 'a0', True)
    emitter.ins('move.w', '0xf364:w,%d0', 4)
    emitter.ins('lsl.w', '#3,%d0', 2)
    emitter.ins('adda.w', '%d0,%a0', 2)


def _foreign_query(emitter):
    _neighbor_cursor(emitter)
    for address, register in ((0xb600,'a1'),(0xb400,'a2'),(0xf427,'a3'),(0xea37,'a5'),(0xc300,'a6')):
        _view(emitter, address, register)
    for value, register in ((0,'d0'),(65535,'d1'),(65535,'d2'),(0,'d3')):
        _word_constant(emitter, value, register)
    loop, finish = emitter.fresh('neighbor'), emitter.fresh('return')
    emitter.label(loop)
    emitter.ins('move.b', '(%a0)+,%d3', 2)
    emitter.ins('bmi.w', finish, 4)
    emitter.ins('clr.w', '%d4', 2)
    emitter.ins('move.b', '(%a3,%d3.w),%d4', 4)
    emitter.ins('bmi.b', loop, 2)
    emitter.ins('cmp.w', '0xf376:w,%d4', 4)
    emitter.ins('beq.b', loop, 2)
    emitter.ins('tst.b', '(%a5,%d3.w)', 4)
    emitter.ins('bne.b', loop, 2)
    callee = next(binding for binding in OFFICER_BINDINGS if binding.name == 'scan_nonruler_city_attribute_sum')
    emitter.ins('bsr.w', callee.name, 4)
    emitter.ins('bra.b', loop, 2)
    emitter.label(finish)


def _nonruler_scan(emitter, holes):
    emitter.ins('movem.l', '%d7/%a0,-(%a7)', 4)
    _view(emitter, 0xf427, 'a0')
    emitter.ins('clr.w', '%d7', 2)
    emitter.ins('move.b', '(%a0,%d3.w),%d7', 4)
    emitter.ins('lsl.w', '#1,%d7', 2)
    _view(emitter, 0xe640, 'a0')
    emitter.ins('move.w', '(%a0,%d7.w),%d7', 4)
    _view(emitter, 0xcd00, 'a4')
    _word_constant(emitter, 255, 'd4')
    loop, latch = emitter.fresh('officer'), emitter.fresh('countdown')
    emitter.label(loop)
    emitter.ins('cmp.w', '%d4,%d7', 2)
    emitter.ins('beq.w', latch, 4)
    emitter.ins('cmp.b', '-(%a4),%d3', 2)
    emitter.ins('bne.w', latch, 4)
    emitter.ins('cmpi.b', f'#{holes["status_threshold"]},(%a6,%d4.w)', 6)
    emitter.ins('bcc.w', latch, 4)
    emitter.ins('move.w', '%d4,%d5', 2)
    emitter.ins('lsl.w', '#1,%d5', 2)
    emitter.ins('move.w', '(%a1,%d5.w),%d6', 4)
    emitter.ins('add.w', '(%a2,%d5.w),%d6', 4)
    emitter.ins('cmp.w', '%d0,%d6', 2)
    emitter.ins('bls.w', latch, 4)
    for source, destination in (('d6','d0'),('d4','d1'),('d3','d2')):
        emitter.ins('move.w', f'%{source},%{destination}', 2)
    emitter.label(latch)
    emitter.ins('dbra', f'%d4,{loop}', 4)
    emitter.ins('movem.l', '(%a7)+,%d7/%a0', 4)


def _player_gate(emitter, removed):
    _view(emitter, 0xf427, 'a0')
    emitter.ins('move.w', '0xf3a8:w,%d0', 4)
    emitter.ins('move.b', '(%a0,%d0.w),%d0', 4)
    owned, clear, set_carry, finish = (emitter.fresh(role) for role in ('owned','clear','set','return'))
    for position, address in enumerate((0xf67b,0xf67d,0xf67f)):
        emitter.ins('cmp.b', f'0x{address:x}:w,%d0', 4)
        if removed and position == 2:
            emitter.ins('bne.w', clear, 4)
        else:
            emitter.ins('beq.w', owned if removed else set_carry, 4)
    if removed:
        emitter.label(owned)
        emitter.ins('move.w', '0xf3a6:w,%d1', 4)
        _view(emitter, 0xcc00, 'a0')
        emitter.ins('move.b', '(%a0,%d1.w),%d1', 4)
        emitter.ins('cmpi.b', '#255,%d1', 4)
        emitter.ins('beq.w', set_carry, 4)
    emitter.label(clear)
    emitter.ins('andi.w', '#0xfffe,%sr', 4)
    emitter.ins('bra.w', finish, 4)
    emitter.label(set_carry)
    emitter.ins('ori.w', '#1,%sr', 4)
    emitter.label(finish)


def _head_minimum(emitter):
    _neighbor_cursor(emitter)
    for address, register in ((0xf427,'a1'),(0xb600,'a2'),(0xf45e,'a3'),(0xea37,'a4')):
        _view(emitter, address, register)
    for value, register in ((65535,'d0'),(65535,'d1'),(0,'d2')):
        _word_constant(emitter, value, register)
    loop, owned, finish = (emitter.fresh(role) for role in ('neighbor','owned','return'))
    emitter.label(loop)
    emitter.ins('move.b', '(%a0)+,%d2', 2)
    emitter.ins('bmi.w', finish, 4)
    emitter.ins('tst.b', '(%a4,%d2.w)', 4)
    emitter.ins('bne.b', loop, 2)
    emitter.ins('move.b', '(%a1,%d2.w),%d3', 4)
    for position, address in enumerate((0xf67b,0xf67d,0xf67f)):
        emitter.ins('cmp.b', f'0x{address:x}:w,%d3', 4)
        emitter.ins('bne.b' if position == 2 else 'beq.w', loop if position == 2 else owned, 2 if position == 2 else 4)
    emitter.label(owned)
    emitter.ins('move.w', '%d2,%d3', 2)
    emitter.ins('lsl.w', '#1,%d3', 2)
    emitter.ins('move.w', '(%a3,%d3.w),%d3', 4)
    emitter.ins('lsl.w', '#1,%d3', 2)
    emitter.ins('move.w', '(%a2,%d3.w),%d3', 4)
    emitter.ins('cmp.w', '%d0,%d3', 2)
    emitter.ins('bcc.b', loop, 2)
    emitter.ins('move.w', '%d3,%d0', 2)
    emitter.ins('move.w', '%d2,%d1', 2)
    emitter.ins('bra.b', loop, 2)
    emitter.label(finish)


def compile_officer(source):
    """Consume the complete supported source and emit eight ordinary GNU units."""
    records = semantic_ir(source)
    units = []
    for record in records:
        binding = next(item for item in OFFICER_BINDINGS if item.name == record['name'])
        emitter = Emitter(binding)
        emitter.begin()
        name = record['name']
        if name in ('select_roster_attribute_max', 'select_roster_attribute_max_preserving_id',
                    'select_and_mark_roster_attribute_max'):
            _roster_query(emitter, name != 'select_roster_attribute_max',
                          name == 'select_and_mark_roster_attribute_max', record['holes'])
        elif name == 'select_foreign_nonruler_attribute_sum':
            _foreign_query(emitter)
        elif name == 'scan_nonruler_city_attribute_sum':
            _nonruler_scan(emitter, record['holes'])
        elif name in ('selected_city_has_player_owner', 'selected_player_officer_removed_gate'):
            _player_gate(emitter, name == 'selected_player_officer_removed_gate')
        elif name == 'select_player_neighbor_head_attribute_min':
            _head_minimum(emitter)
        else:
            raise CompileError('unbound officer operation')
        emitter.end()
        unit = emitter.unit(record['effects'])
        # Some compatible emitters expose binding through unit(), others don't.
        unit.setdefault('binding', asdict(binding))
        if sum(row['encoding_bytes'] for row in unit['instructions']) != binding.end - binding.entry:
            raise CompileError('lowering does not fit the declared complete body')
        units.append(unit)
    return {'units': units, 'allocated_bytes': 576,
            'instructions': sum(len(unit['instructions']) for unit in units),
            'semantic_family': 'ordered_officer_queries', 'complete_CPU': False}
