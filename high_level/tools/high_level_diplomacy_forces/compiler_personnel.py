"""Complete semantic-flow admission and ordinary 68000 target lowering.

The FLOW contract is readable business Python, not instruction bytes or an
assembly listing. Every AST node, signature, import and return is consumed;
only the declared BYTE cutoff / WORD average rule holes are editable.
"""
import ast
from copy import deepcopy

from .compiler_common import CompileError, Emitter, require_declared_names
from .target import PERSONNEL_BINDINGS, SCALAR_BINDINGS, TABLE_BINDINGS

FLOW = r'''
def settle_personnel_joining(state: GameState) -> None:
    if state.method() == 74:
        settle_bribe_joining(state)
    else:
        settle_persuasion_joining(state)


def settle_bribe_joining(state: GameState) -> None:
    if state.response() == 119:
        state.set_route(520)
        state.set_step(32)
        prepare_message(state, 85)
        state.set_message_gate(1)
        return None
    city_index = u16(state.current_city() << 2)
    amount = state.request_gold()
    previous = state.city_gold.long(city_index)
    state.city_gold.set_long(city_index, u32(previous - amount))
    amount = state.request_rice()
    previous = state.city_rice.long(city_index)
    state.city_rice.set_long(city_index, u32(previous - amount))
    city = state.selected_city()
    owner = u16(state.city_owners.byte(city))
    head = state.force_leaders.word(u16(owner << 1))
    if head == state.selected_officer():
        accepted = False
    else:
        offered = u32(state.request_gold() + state.request_rice())
        city = state.current_city()
        owner = u16(replace_byte(city, state.city_owners.byte(city)))
        head = state.force_leaders.word(u16(owner << 1))
        affinity = u16(state.officer_affinity.byte(head))
        lower = u32(low16(offered) * affinity)
        upper = u32(high16(offered) * affinity)
        offered_score = u32(swap_words(upper) + lower)
        actor = state.selected_officer()
        status = u16(state.officer_status.byte(actor))
        required = u32(status * status)
        affinity = u16(state.officer_affinity.byte(actor))
        required = u32(low16(required) * affinity)
        factor = bribe_acceptance_factor(state)
        lower = u32(low16(required) * factor)
        upper = u32(high16(required) * factor)
        required_score = u32(swap_words(upper) + lower)
        accepted = offered_score >= required_score
    if not accepted:
        penalize_force_head_affinity(state)
        reward_force_head_small_progress(state)
        state.set_route(520)
        state.set_step(32)
        state.set_message_actor(state.selected_officer())
        prepare_message(state, 91)
        return None
    reward_force_head_large_progress(state)
    transfer_joining_officer(state, state.selected_officer())
    state.set_route(520)
    state.set_step(40)
    state.set_message(90)
    state.set_message_target(state.selected_officer())
    saved_target = state.target_officer()
    state.set_target_officer(state.force_leaders.word(u16(state.current_force() << 1)))
    state.apply_returning_officer_loyalty()
    state.set_target_officer(saved_target)
    state.set_scene_queue(14)
    state.set_ui_first(0)
    state.set_ui_second(0)
    state.set_joining_refresh(0)


def bribe_acceptance_factor(state: GameState) -> Word:
    state.sample_random()
    actor = state.selected_officer()
    status = state.officer_status.byte(actor)
    band = u16(0)
    if status > 30:
        band = u16(band + 1)
        if status > 50:
            band = u16(band + 1)
            if status > 70:
                band = u16(band + 1)
                if status > 80:
                    band = u16(band + 1)
                    if status > 90:
                        band = u16(band + 1)
    index = u16(band + u16(band << 2))
    trait = u16(state.officer_traits.byte(actor) & 7)
    index = u16(u16(trait + index) << 1)
    weight = u16(state.bribe_factors.byte(index))
    weighted = u32(weight * state.seed_word())
    bias = u16(state.bribe_factors.byte(index, 1))
    return u16(high16(weighted) + bias)


def penalize_force_head_affinity(state: GameState) -> None:
    sample = low16(state.sample_random())
    scale = high16(u32(sample * 4))
    head = state.force_leaders.word(u16(state.current_force() << 1))
    affinity = u16(state.officer_affinity.byte(head))
    penalty = divu_retained(u32(affinity * scale), 100)
    previous = state.officer_affinity.byte(head)
    state.officer_affinity.set_byte(head, u8(previous - low8(penalty)))


def reward_force_head_small_progress(state: GameState) -> None:
    state.sample_random()
    seed = u32(state.seed_word())
    gain = u16(high16(u32(seed * 3)) + 1)
    head = state.force_leaders.word(u16(state.current_force() << 1))
    index = u16(head << 1)
    previous = state.progress_be.word(index)
    total = previous + gain
    state.progress_be.set_word(index, u16(total))
    if total > 65535:
        state.progress_be.set_word(index, 65535)


def reward_force_head_large_progress(state: GameState) -> None:
    sample = low16(state.sample_random())
    gain = u16(high16(u32(sample * 5)) + 1)
    head = state.force_leaders.word(u16(state.current_force() << 1))
    index = u16(head << 1)
    previous = state.progress_be.word(index)
    total = previous + gain
    state.progress_be.set_word(index, u16(total))
    if total > 65535:
        state.progress_be.set_word(index, 65535)


def transfer_joining_officer(state: GameState, officer: Word) -> None:
    officer = uint(officer, 16)
    index = u16(state.selected_city() << 1)
    index = u16(index + state.selected_city())
    index = u16(index << 2)
    if officer == state.city_orders.word(index):
        state.city_orders.set_word(index, 65535)
    elif officer == state.city_orders.word(index, 4):
        state.city_orders.set_word(index, 65535, 4)
    elif officer == state.city_orders.word(index, 8):
        state.city_orders.set_word(index, 65535, 8)
    head = state.city_heads.word(u16(state.selected_city() << 1))
    if head != officer:
        state.officer_assignments.set_byte(officer, state.city_tail())
        return None
    state.set_roster_exclusion(officer)
    count = state.build_roster(state.selected_city())
    if count != 1:
        roster = state.candidate_roster.cursor()
        attribute = u16(0)
        total = u16(0)
        while True:
            member = roster.next_word()
            if negative_word(member):
                break
            attribute = u16(replace_byte(attribute, state.officer_status.byte(member)))
            total = u16(total + attribute)
        average = divu_retained(u32(s16(total)), count)
        if low16(average) > 35:
            state.officer_assignments.set_byte(officer, state.city_tail())
            city = state.selected_city()
            state.set_roster_exclusion(65535)
            state.build_roster(city)
            choose_city_head(state, city)
            return None
    city = state.selected_city()
    old_owner = u16(state.city_owners.byte(city))
    state.city_owners.set_byte(city, state.current_force_tail())
    state.replace_city_assignments(old_owner)
    state.mark_c300_list()
    state.clear_city_orders()
    state.clear_selected_links()


def settle_persuasion_joining(state: GameState) -> None:
    if state.response() == 121:
        state.set_route(520)
        state.set_step(32)
        prepare_message(state, 85)
        state.set_message_gate(1)
        return None
    state.officer_actions.set_byte(state.selected_officer(), 1)
    city = state.selected_city()
    owner = u16(state.city_owners.byte(city))
    head = state.force_leaders.word(u16(owner << 1))
    if head == state.target_officer():
        accepted = False
    else:
        offered_score, required_score = persuasion_scores(state)
        accepted = offered_score >= required_score
    if not accepted:
        reward_actor_small_progress(state)
        penalize_actor_affinity(state)
        penalize_force_head_affinity(state)
        force = state.current_force()
        if force != state.player_force_1():
            if force != state.player_force_2():
                if force != state.player_force_3():
                    return None
        state.set_route(520)
        state.set_step(32)
        state.set_message_actor(state.selected_officer())
        prepare_message(state, 83)
        return None
    reward_actor_large_progress(state)
    transfer_joining_officer(state, state.target_officer())
    force = state.current_force()
    if force != state.player_force_1():
        if force != state.player_force_2():
            if force != state.player_force_3():
                return None
    state.set_route(520)
    state.set_step(40)
    state.set_message(92)
    state.set_message_target(state.target_officer())
    state.set_message_actor(state.selected_officer())
    state.set_scene_queue(12)
    state.set_ui_first(0)
    state.set_ui_second(0)
    state.set_selected_officer(state.target_officer())
    state.set_joining_refresh(0)
    state.set_target_officer(state.force_leaders.word(u16(state.current_force() << 1)))
    state.apply_returning_officer_loyalty()


def persuasion_scores(state: GameState) -> tuple[Long, Long]:
    target = state.target_officer()
    status = u16(state.officer_status.byte(target))
    offered = u16(100 - status)
    head = state.force_leaders.word(u16(state.current_force() << 1))
    affinity = u16(state.officer_affinity.byte(head))
    offered = u32(low16(offered) * affinity)
    actor = state.selected_officer()
    affinity = u16(state.officer_affinity.byte(actor))
    offered = u32(low16(offered) * affinity)
    ability = state.officer_ability.word(u16(actor << 1))
    lower = u32(low16(offered) * ability)
    upper = u32(high16(offered) * ability)
    offered = u32(swap_words(upper) + lower)
    factor = persuasion_factor(state)
    lower = u32(low16(offered) * factor)
    upper = u32(high16(offered) * factor)
    offered_score = u32(swap_words(upper) + lower)
    target = state.target_officer()
    affinity = u16(state.officer_affinity.byte(target))
    city = state.selected_city()
    owner = u16(state.city_owners.byte(city))
    head = state.force_leaders.word(u16(owner << 1))
    head_affinity = u16(state.officer_affinity.byte(head))
    required = u32(affinity * head_affinity)
    ability = state.officer_ability.word(u16(target << 1))
    required = u32(low16(required) * ability)
    index = u16(state.difficulty() << 1)
    weight = state.persuasion_weights.word(index)
    lower = u32(low16(required) * weight)
    upper = u32(high16(required) * weight)
    required_score = u32(lower + swap_words(upper))
    return offered_score, required_score


def persuasion_factor(state: GameState) -> Word:
    state.sample_random()
    actor = state.selected_officer()
    actor_trait = u16(state.officer_traits.byte(actor) & 7)
    actor_deficit = u16(4 - actor_trait)
    index = u16(u16(actor_deficit << 2) + actor_deficit)
    target = state.target_officer()
    target_trait = u16(state.officer_traits.byte(target) & 7)
    target_deficit = u16(replace_byte(4, u8(4 - target_trait)))
    index = u16(u16(index + target_deficit) << 1)
    weight = u16(state.persuasion_factors.byte(index))
    weighted = u32(weight * state.seed_word())
    bias = u16(state.persuasion_factors.byte(index, 1))
    return u16(high16(weighted) + bias)


def reward_actor_small_progress(state: GameState) -> None:
    state.sample_random()
    seed = u32(state.seed_word())
    gain = u16(high16(u32(seed * 3)) + 1)
    index = u16(state.selected_officer() << 1)
    previous = state.progress_be.word(index)
    total = previous + gain
    state.progress_be.set_word(index, u16(total))
    if total > 65535:
        state.progress_be.set_word(index, 65535)


def reward_actor_large_progress(state: GameState) -> None:
    sample = low16(state.sample_random())
    gain = u16(high16(u32(sample * 6)) + 5)
    index = u16(state.selected_officer() << 1)
    previous = state.progress_be.word(index)
    total = previous + gain
    state.progress_be.set_word(index, u16(total))
    if total > 65535:
        state.progress_be.set_word(index, 65535)


def penalize_actor_affinity(state: GameState) -> None:
    sample = low16(state.sample_random())
    scale = high16(u32(sample * 11))
    actor = state.selected_officer()
    affinity = u16(state.officer_affinity.byte(actor))
    penalty = divu_retained(u32(affinity * scale), 100)
    previous = state.officer_affinity.byte(actor)
    amount = low8(penalty)
    state.officer_affinity.set_byte(actor, u8(previous - amount))
    if previous < amount:
        state.officer_affinity.set_byte(actor, 0)

'''

APPROVED_DOMAIN = {
    'GameState','Word','Long','uint','u8','u16','u32','s16','low8','low16','high16',
    'replace_byte','swap_words','divu_retained','negative_word',
}
APPROVED_SHARED = {'choose_city_head','prepare_message'}


def _strip_docs(node):
    result = deepcopy(node)
    if (result.body and isinstance(result.body[0], ast.Expr)
            and isinstance(result.body[0].value, ast.Constant)
            and type(result.body[0].value.value) is str):
        result.body.pop(0)
    return result


def _rule_holes(function):
    rules = {}
    for node in ast.walk(function):
        if function.name == 'bribe_acceptance_factor':
            if (isinstance(node, ast.Compare) and isinstance(node.left, ast.Name)
                    and node.left.id == 'status' and len(node.ops) == 1
                    and isinstance(node.ops[0], ast.Gt)
                    and len(node.comparators) == 1
                    and isinstance(node.comparators[0], ast.Constant)):
                value = node.comparators[0].value
                if type(value) is not int or not 0 <= value <= 255:
                    raise CompileError('status band requires a complete unsigned BYTE')
                key = 'status_cutoff_' + str(len(rules))
                rules[key] = value
                node.comparators[0] = ast.Name(id='__' + key, ctx=ast.Load())
        if function.name == 'transfer_joining_officer':
            if (isinstance(node, ast.Compare) and isinstance(node.left, ast.Call)
                    and isinstance(node.left.func, ast.Name) and node.left.func.id == 'low16'
                    and len(node.comparators) == 1
                    and isinstance(node.comparators[0], ast.Constant)):
                value = node.comparators[0].value
                if type(value) is not int or not 0 <= value <= 65535:
                    raise CompileError('roster average requires an unsigned WORD cutoff')
                if 'average_cutoff' in rules:
                    raise CompileError('exactly one average cutoff is supported')
                rules['average_cutoff'] = value
                node.comparators[0] = ast.Name(id='__average_cutoff', ctx=ast.Load())
    if function.name == 'bribe_acceptance_factor' and len(rules) != 5:
        raise CompileError('all five ordered status bands are required')
    if function.name == 'transfer_joining_officer' and len(rules) != 1:
        raise CompileError('the original average gate is required')
    return rules


def semantic_ir(source):
    if type(source) is not str:
        raise CompileError('explicit business source string required')
    try:
        module = _strip_docs(ast.parse(source))
    except (SyntaxError, ValueError) as exc:
        raise CompileError('valid semantic Python required') from exc
    functions, imports = {}, set()
    for node in module.body:
        if isinstance(node, ast.ImportFrom):
            names = APPROVED_DOMAIN if node.module == 'domain' else APPROVED_SHARED if node.module == 'business_shared' else set()
            if node.level != 1 or not names:
                raise CompileError('declared domain/shared imports only')
            for item in node.names:
                if item.asname is not None or item.name not in names:
                    raise CompileError('undeclared import or renamed binding')
                imports.add(item.name)
        elif isinstance(node, ast.FunctionDef):
            if node.name in functions:
                raise CompileError('duplicate complete operation')
            functions[node.name] = _strip_docs(node)
        else:
            raise CompileError('only declared imports and complete functions are supported')
    contracts = {node.name: node for node in ast.parse(FLOW).body}
    if set(functions) != set(contracts):
        raise CompileError('all thirteen complete personnel functions required')
    require_declared_names(functions, imports)
    result = []
    for name, contract in contracts.items():
        actual = functions[name]
        normalized = deepcopy(actual)
        rules = _rule_holes(normalized)
        _rule_holes(contract)
        if ast.dump(normalized, include_attributes=False) != ast.dump(contract, include_attributes=False):
            raise CompileError(name + ': unsupported type, parameter, control, call, storage or return')
        effects = []
        for node in ast.walk(actual):
            if isinstance(node, (ast.stmt, ast.Call, ast.Compare, ast.BinOp)):
                effect = dict(operation=type(node).__name__, semantic=ast.dump(node, include_attributes=False))
                if isinstance(node, ast.Call):
                    role = node.func.attr if isinstance(node.func, ast.Attribute) else node.func.id if isinstance(node.func, ast.Name) else ''
                    effect['ordered_live_operation'] = role
                    bits = {'byte':8,'set_byte':8,'u8':8,'low8':8,'word':16,'set_word':16,
                            'next_word':16,'u16':16,'low16':16,'long':32,'set_long':32,
                            'u32':32,'swap_words':32}.get(role)
                    if bits is not None:
                        effect['value_bits'] = bits
                effects.append(effect)
        result.append(dict(name=name, rules=rules, effects=effects))
    return result


def _operand(name):
    binding = SCALAR_BINDINGS[name]
    address = binding['address']
    if binding['suffix'] == 'w':
        address &= 65535
    return '0x%x:%s' % (address, binding['suffix'])


def _load(e, name, register):
    binding = SCALAR_BINDINGS[name]
    bits, suffix = binding['width'], binding['suffix']
    e.ins('move.' + {8:'b',16:'w',32:'l'}[bits], _operand(name) + ',%' + register,
          4 if suffix == 'w' else 6)


def _write(e, name, value):
    binding = SCALAR_BINDINGS[name]
    bits, suffix = binding['width'], binding['suffix']
    width = (8 if bits == 32 else 6) + (2 if suffix == 'l' else 0)
    e.ins('move.' + {8:'b',16:'w',32:'l'}[bits], '#' + str(value) + ',' + _operand(name), width)


def _copy_scalar(e, source, destination):
    first, second = SCALAR_BINDINGS[source], SCALAR_BINDINGS[destination]
    if first['width'] != second['width']:
        raise CompileError('typed scalar-copy width mismatch')
    e.ins('move.' + {8:'b',16:'w',32:'l'}[first['width']], _operand(source) + ',' + _operand(destination),
          6 + 2*(first['suffix']=='l') + 2*(second['suffix']=='l'))


def _clear(e, name):
    binding = SCALAR_BINDINGS[name]
    e.ins('clr.' + {8:'b',16:'w',32:'l'}[binding['width']], _operand(name),
          4 if binding['suffix']=='w' else 6)


def _view(e, name, register='a0'):
    binding = TABLE_BINDINGS[name]
    address = binding['address']
    if binding['suffix'] == 'w':
        address &= 65535
    e.ins('lea.l', '0x%x:%s,%%%s' % (address,binding['suffix'],register),
          4 if binding['suffix']=='w' else 6)


def _call(e, name, absolute=False):
    e.ins('jsr' if absolute else 'bsr.w', name + (':l' if absolute else ''), 6 if absolute else 4)


def _pc_view(e, name, register='a0'):
    displacement = TABLE_BINDINGS[name]['address'] - (e.pc + 2)
    if not -32768 <= displacement <= 32767:
        raise CompileError('PC-relative source exceeds signed WORD')
    e.ins('lea.l', str(displacement) + '(%pc),%' + register, 4)


def _force_head(e, register='d1', twice=False):
    _load(e,'current_force',register)
    e.ins('lsl.w','#1,%'+register)
    _view(e,'force_leaders')
    e.ins('move.w','(%a0,%'+register+'.w),%'+register,4)
    if twice:
        e.ins('lsl.w','#1,%'+register)


def _progress_tail(e, actor=False):
    done=e.fresh('progress_saturated')
    if actor:
        _load(e,'selected_officer','d1')
        e.ins('lsl.w','#1,%d1')
    else:
        _force_head(e,'d1',True)
    _view(e,'progress_be')
    e.ins('add.w','%d0,(%a0,%d1.w)',4)
    e.ins('bcc.b',done)
    e.ins('move.w','#65535,(%a0,%d1.w)',6)
    e.label(done)


def _expanded_product(e, value, factor, output, clear_upper=False):
    # Preserve the original two low-WORD products, including the upper-product
    # SWAP contribution; this is not a mathematical unbounded LONG product.
    e.ins('move.w','%'+value+',%'+output)
    e.ins('mulu.w','%'+factor+',%'+output)
    e.ins('swap','%'+value)
    if clear_upper:
        e.ins('andi.l','#65535,%'+value,6)
    e.ins('mulu.w','%'+factor+',%'+value)
    e.ins('swap','%'+value)
    e.ins('add.l','%'+output+',%'+value)


def _dispatch(e, rules):
    persuasion, done = e.fresh('persuasion_method'), e.fresh('joining_done')
    e.ins('cmpi.b','#74,' + _operand('method'),6)
    e.ins('bne.b',persuasion)
    _call(e,'settle_bribe_joining')
    e.ins('bra.b',done)
    e.label(persuasion)
    _call(e,'settle_persuasion_joining')
    e.label(done)


def _bribe(e, rules):
    cancelled, failed, accepted, done = (e.fresh(n) for n in ('bribe_cancelled','bribe_failed','bribe_accepted','bribe_done'))
    e.ins('cmpi.w','#119,' + _operand('response'),6)
    e.ins('beq.w',cancelled,4)
    _load(e,'current_city','d0')
    e.ins('lsl.w','#2,%d0')
    _view(e,'city_gold')
    _load(e,'request_gold','d1')
    e.ins('sub.l','%d1,(%a0,%d0.w)',4)
    _view(e,'city_rice')
    _load(e,'request_rice','d1')
    e.ins('sub.l','%d1,(%a0,%d0.w)',4)
    _load(e,'selected_city','d0')
    _view(e,'city_owners')
    e.ins('clr.w','%d1')
    e.ins('move.b','(%a0,%d0.w),%d1',4)
    e.ins('lsl.w','#1,%d1')
    _view(e,'force_leaders')
    e.ins('move.w','(%a0,%d1.w),%d0',4)
    e.ins('cmp.w',_operand('selected_officer')+',%d0',4)
    e.ins('beq.w',failed,4)
    _load(e,'request_gold','d2')
    e.ins('add.l',_operand('request_rice')+',%d2',4)
    _load(e,'current_city','d0')
    _view(e,'city_owners')
    e.ins('move.b','(%a0,%d0.w),%d0',4)
    e.ins('lsl.w','#1,%d0')
    _view(e,'force_leaders')
    e.ins('move.w','(%a0,%d0.w),%d0',4)
    _view(e,'officer_affinity')
    e.ins('clr.w','%d3')
    e.ins('move.b','(%a0,%d0.w),%d3',4)
    _expanded_product(e,'d2','d3','d0')
    _load(e,'selected_officer','d0')
    _view(e,'officer_status')
    e.ins('clr.w','%d3')
    e.ins('move.b','(%a0,%d0.w),%d3',4)
    e.ins('mulu.w','%d3,%d3')
    _view(e,'officer_affinity')
    e.ins('clr.w','%d4')
    e.ins('move.b','(%a0,%d0.w),%d4',4)
    e.ins('mulu.w','%d4,%d3')
    _call(e,'bribe_acceptance_factor')
    _expanded_product(e,'d3','d0','d1',True)
    e.ins('cmp.l','%d3,%d2')
    e.ins('bcc.b',accepted)
    e.label(failed)
    _call(e,'penalize_force_head_affinity')
    _call(e,'reward_force_head_small_progress')
    _write(e,'route',520)
    _write(e,'step',32)
    e.ins('move.w','#91,%d0',4)
    _copy_scalar(e,'selected_officer','message_actor')
    _call(e,'prepare_message',True)
    e.ins('bra.w',done,4)
    e.label(accepted)
    _call(e,'reward_force_head_large_progress')
    _load(e,'selected_officer','d0')
    _call(e,'transfer_joining_officer')
    _write(e,'route',520)
    _write(e,'step',40)
    _write(e,'message',90)
    _copy_scalar(e,'selected_officer','message_target')
    e.ins('move.w',_operand('target_officer')+',-(%a7)',4)
    _view(e,'force_leaders')
    _load(e,'current_force','d0')
    e.ins('lsl.w','#1,%d0')
    e.ins('move.w','(%a0,%d0.w),'+_operand('target_officer'),6)
    _call(e,'apply_returning_officer_loyalty',True)
    e.ins('move.w','(%a7)+,'+_operand('target_officer'),4)
    _write(e,'scene_queue',14)
    _clear(e,'ui_first')
    _clear(e,'ui_second')
    _clear(e,'joining_refresh')
    e.ins('bra.w',done,4)
    e.label(cancelled)
    _write(e,'route',520)
    _write(e,'step',32)
    e.ins('move.w','#85,%d0',4)
    _call(e,'prepare_message',True)
    _write(e,'message_gate',1)
    e.label(done)


def _bribe_factor(e, rules):
    table = e.fresh('status_band_selected')
    _call(e,'step_random',True)
    _load(e,'selected_officer','d0')
    _view(e,'officer_status')
    e.ins('move.b','(%a0,%d0.w),%d4',4)
    e.ins('clr.w','%d1')
    for number in range(5):
        e.ins('cmpi.b','#'+str(rules['status_cutoff_'+str(number)])+',%d4',4)
        e.ins('bls.b',table)
        e.ins('addq.w','#1,%d1')
    e.label(table)
    e.ins('move.w','%d1,%d4')
    e.ins('lsl.w','#2,%d4')
    e.ins('add.w','%d4,%d1')
    _view(e,'officer_traits')
    e.ins('move.b','(%a0,%d0.w),%d4',4)
    e.ins('andi.w','#7,%d4',4)
    e.ins('add.w','%d1,%d4')
    e.ins('lsl.w','#1,%d4')
    _pc_view(e,'bribe_factors')
    e.ins('nop')
    e.ins('clr.w','%d0')
    e.ins('move.b','(%a0,%d4.w),%d0',4)
    e.ins('mulu.w',_operand('seed_word')+',%d0',4)
    e.ins('swap','%d0')
    e.ins('clr.w','%d1')
    e.ins('move.b','1(%a0,%d4.w),%d1',4)
    e.ins('add.w','%d1,%d0')


def _head_penalty(e, rules):
    _call(e,'step_random',True)
    e.ins('andi.l','#65535,%d0',6)
    e.ins('move.l','%d0,%d1')
    e.ins('lsl.l','#1,%d0')
    e.ins('add.l','%d1,%d0')
    e.ins('add.l','%d1,%d0')
    e.ins('swap','%d0')
    _force_head(e)
    e.ins('clr.w','%d2')
    _view(e,'officer_affinity')
    e.ins('move.b','(%a0,%d1.w),%d2',4)
    e.ins('mulu.w','%d0,%d2')
    e.ins('divu.w','#100,%d2',4)
    e.ins('sub.b','%d2,(%a0,%d1.w)',4)


def _small_progress(e, rules, actor=False):
    _call(e,'step_random',True)
    e.ins('moveq','#0,%d0')
    _load(e,'seed_word','d0')
    e.ins('move.l','%d0,%d1')
    e.ins('lsl.l','#1,%d0')
    e.ins('add.l','%d1,%d0')
    e.ins('swap','%d0')
    e.ins('addq.w','#1,%d0')
    _progress_tail(e,actor)


def _large_head_progress(e, rules):
    _call(e,'step_random',True)
    e.ins('andi.l','#65535,%d0',6)
    e.ins('move.l','%d0,%d1')
    e.ins('lsl.l','#2,%d0')
    e.ins('add.l','%d1,%d0')
    e.ins('swap','%d0')
    e.ins('addq.w','#1,%d0')
    _progress_tail(e)


def _transfer(e, rules):
    second, third, checked, head, scan, averaged, lost, done = (
        e.fresh(n) for n in ('second_order','third_order','orders_checked','departing_head','status_scan','status_average','replace_owner','transfer_done'))
    _load(e,'selected_city','d1')
    e.ins('lsl.w','#1,%d1')
    e.ins('add.w',_operand('selected_city')+',%d1',4)
    e.ins('lsl.w','#2,%d1')
    _view(e,'city_orders')
    e.ins('cmp.w','(%a0,%d1.w),%d0',4)
    e.ins('bne.w',second,4)
    e.ins('move.w','#65535,(%a0,%d1.w)',6)
    e.ins('bra.w',checked,4)
    e.label(second)
    e.ins('cmp.w','4(%a0,%d1.w),%d0',4)
    e.ins('bne.w',third,4)
    e.ins('move.w','#65535,4(%a0,%d1.w)',6)
    e.ins('bra.w',checked,4)
    e.label(third)
    e.ins('cmp.w','8(%a0,%d1.w),%d0',4)
    e.ins('bne.w',checked,4)
    e.ins('move.w','#65535,8(%a0,%d1.w)',6)
    e.label(checked)
    _load(e,'selected_city','d1')
    e.ins('lsl.w','#1,%d1')
    _view(e,'city_heads')
    e.ins('move.w','(%a0,%d1.w),%d1',4)
    e.ins('cmp.w','%d0,%d1')
    e.ins('beq.b',head)
    _view(e,'officer_assignments')
    e.ins('move.b',_operand('city_tail')+',(%a0,%d0.w)',6)
    e.ins('bra.b',done)
    e.label(head)
    e.ins('move.w','%d0,-(%a7)')
    e.ins('move.w','%d0,'+_operand('roster_exclusion'),4)
    _load(e,'selected_city','d0')
    _call(e,'build_roster',True)
    e.ins('move.w','(%a7)+,%d0')
    e.ins('cmpi.w','#1,%d3',4)
    e.ins('beq.b',lost)
    _view(e,'candidate_roster')
    _view(e,'officer_status','a1')
    e.ins('clr.w','%d1')
    e.ins('clr.w','%d2')
    e.label(scan)
    e.ins('move.w','(%a0)+,%d4')
    e.ins('bmi.b',averaged)
    e.ins('move.b','(%a1,%d4.w),%d1',4)
    e.ins('add.w','%d1,%d2')
    e.ins('bra.b',scan)
    e.label(averaged)
    e.ins('ext.l','%d2')
    e.ins('divu.w','%d3,%d2')
    e.ins('cmpi.w','#'+str(rules['average_cutoff'])+',%d2',4)
    e.ins('bls.b',lost)
    _view(e,'officer_assignments')
    e.ins('move.b',_operand('city_tail')+',(%a0,%d0.w)',6)
    _load(e,'selected_city','d0')
    _write(e,'roster_exclusion',65535)
    _call(e,'build_roster',True)
    _call(e,'choose_city_head',True)
    e.ins('bra.b',done)
    e.label(lost)
    _load(e,'selected_city','d0')
    _view(e,'city_owners')
    e.ins('move.b','(%a0,%d0.w),%d1',4)
    e.ins('move.b',_operand('current_force_tail')+',(%a0,%d0.w)',6)
    _call(e,'replace_city_assignments')
    _call(e,'mark_c300_list')
    _call(e,'clear_city_orders')
    _call(e,'clear_selected_links')
    e.label(done)


def _player_gate(e, chosen, done):
    _load(e,'current_force','d0')
    for name in ('player_force_1','player_force_2'):
        e.ins('cmp.w',_operand(name)+',%d0',4)
        e.ins('beq.w',chosen,4)
    e.ins('cmp.w',_operand('player_force_3')+',%d0',4)
    e.ins('bne.w',done,4)
    e.label(chosen)


def _persuasion(e, rules):
    cancelled, failed, accepted, player_failed, player_accepted, done = (
        e.fresh(n) for n in ('persuasion_cancelled','persuasion_failed','persuasion_accepted','player_failed','player_accepted','persuasion_done'))
    e.ins('cmpi.w','#121,'+_operand('response'),6)
    e.ins('beq.w',cancelled,4)
    _view(e,'officer_actions')
    _load(e,'selected_officer','d0')
    e.ins('move.b','#1,(%a0,%d0.w)',6)
    _load(e,'selected_city','d0')
    _view(e,'city_owners')
    e.ins('clr.w','%d1')
    e.ins('move.b','(%a0,%d0.w),%d1',4)
    e.ins('lsl.w','#1,%d1')
    _view(e,'force_leaders')
    e.ins('move.w','(%a0,%d1.w),%d0',4)
    e.ins('cmp.w',_operand('target_officer')+',%d0',4)
    e.ins('beq.w',failed,4)
    _call(e,'persuasion_scores')
    e.ins('cmp.l','%d0,%d2')
    e.ins('bcc.b',accepted)
    e.label(failed)
    _call(e,'reward_actor_small_progress')
    _call(e,'penalize_actor_affinity')
    _call(e,'penalize_force_head_affinity')
    _player_gate(e,player_failed,done)
    _write(e,'route',520)
    _write(e,'step',32)
    e.ins('move.w','#83,%d0',4)
    _copy_scalar(e,'selected_officer','message_actor')
    _call(e,'prepare_message',True)
    e.ins('bra.w',done,4)
    e.label(accepted)
    _call(e,'reward_actor_large_progress')
    _load(e,'target_officer','d0')
    _call(e,'transfer_joining_officer')
    _player_gate(e,player_accepted,done)
    _write(e,'route',520)
    _write(e,'step',40)
    _write(e,'message',92)
    _copy_scalar(e,'target_officer','message_target')
    _copy_scalar(e,'selected_officer','message_actor')
    _write(e,'scene_queue',12)
    _clear(e,'ui_first')
    _clear(e,'ui_second')
    _copy_scalar(e,'target_officer','selected_officer')
    _clear(e,'joining_refresh')
    _view(e,'force_leaders')
    _load(e,'current_force','d0')
    e.ins('lsl.w','#1,%d0')
    e.ins('move.w','(%a0,%d0.w),'+_operand('target_officer'),6)
    _call(e,'apply_returning_officer_loyalty',True)
    e.ins('bra.w',done,4)
    e.label(cancelled)
    _write(e,'route',520)
    _write(e,'step',32)
    e.ins('move.w','#85,%d0',4)
    _call(e,'prepare_message',True)
    _write(e,'message_gate',1)
    e.label(done)


def _scores(e, rules):
    _load(e,'target_officer','d0')
    _view(e,'officer_status')
    e.ins('clr.w','%d1')
    e.ins('move.b','(%a0,%d0.w),%d1',4)
    e.ins('move.w','#100,%d2',4)
    e.ins('sub.w','%d1,%d2')
    _force_head(e,'d0')
    _view(e,'officer_affinity')
    e.ins('clr.w','%d1')
    e.ins('move.b','(%a0,%d0.w),%d1',4)
    e.ins('mulu.w','%d1,%d2')
    _load(e,'selected_officer','d0')
    e.ins('clr.w','%d1')
    e.ins('move.b','(%a0,%d0.w),%d1',4)
    e.ins('mulu.w','%d1,%d2')
    e.ins('lsl.w','#1,%d0')
    _view(e,'officer_ability')
    e.ins('move.w','(%a0,%d0.w),%d1',4)
    _expanded_product(e,'d2','d1','d0')
    _call(e,'persuasion_factor')
    _expanded_product(e,'d2','d1','d0')
    _load(e,'target_officer','d0')
    _view(e,'officer_affinity')
    e.ins('clr.w','%d1')
    e.ins('move.b','(%a0,%d0.w),%d1',4)
    _load(e,'selected_city','d3')
    _view(e,'city_owners','a1')
    e.ins('clr.w','%d4')
    e.ins('move.b','(%a1,%d3.w),%d4',4)
    e.ins('lsl.w','#1,%d4')
    _view(e,'force_leaders','a1')
    e.ins('move.w','(%a1,%d4.w),%d4',4)
    e.ins('clr.w','%d3')
    e.ins('move.b','(%a0,%d4.w),%d3',4)
    e.ins('mulu.w','%d3,%d1')
    e.ins('lsl.w','#1,%d0')
    _view(e,'officer_ability')
    e.ins('move.w','(%a0,%d0.w),%d0',4)
    e.ins('mulu.w','%d0,%d1')
    _load(e,'difficulty','d3')
    e.ins('lsl.w','#1,%d3')
    _pc_view(e,'persuasion_weights')
    e.ins('move.w','(%a0,%d3.w),%d3',4)
    e.ins('move.w','%d1,%d0')
    e.ins('mulu.w','%d3,%d0')
    e.ins('swap','%d1')
    e.ins('mulu.w','%d3,%d1')
    e.ins('swap','%d1')
    e.ins('add.l','%d1,%d0')


def _persuasion_factor(e, rules):
    _call(e,'step_random',True)
    _load(e,'selected_officer','d0')
    e.ins('move.w','#4,%d1',4)
    _view(e,'officer_traits')
    e.ins('move.b','(%a0,%d0.w),%d0',4)
    e.ins('andi.w','#7,%d0',4)
    e.ins('sub.w','%d0,%d1')
    e.ins('move.w','%d1,%d0')
    e.ins('lsl.w','#2,%d0')
    e.ins('add.w','%d1,%d0')
    _load(e,'target_officer','d1')
    e.ins('move.w','#4,%d3',4)
    e.ins('move.b','(%a0,%d1.w),%d4',4)
    e.ins('andi.w','#7,%d4',4)
    e.ins('sub.b','%d4,%d3')
    e.ins('add.w','%d3,%d0')
    e.ins('lsl.w','#1,%d0')
    _pc_view(e,'persuasion_factors','a1')
    e.ins('clr.w','%d1')
    e.ins('move.b','(%a1,%d0.w),%d1',4)
    e.ins('mulu.w',_operand('seed_word')+',%d1',4)
    e.ins('swap','%d1')
    e.ins('clr.w','%d3')
    e.ins('move.b','1(%a1,%d0.w),%d3',4)
    e.ins('add.w','%d3,%d1')


def _large_actor_progress(e, rules):
    _call(e,'step_random',True)
    e.ins('andi.l','#65535,%d0',6)
    e.ins('move.l','%d0,%d1')
    e.ins('lsl.l','#1,%d0')
    e.ins('add.l','%d1,%d0')
    e.ins('lsl.l','#1,%d0')
    e.ins('swap','%d0')
    e.ins('addi.w','#5,%d0',4)
    _progress_tail(e,True)


def _actor_penalty(e, rules):
    done = e.fresh('affinity_nonnegative')
    _call(e,'step_random',True)
    e.ins('andi.l','#65535,%d0',6)
    e.ins('move.l','%d0,%d1')
    e.ins('lsl.l','#2,%d0')
    e.ins('add.l','%d1,%d0')
    e.ins('lsl.l','#1,%d0')
    e.ins('add.l','%d1,%d0')
    e.ins('swap','%d0')
    _view(e,'officer_affinity')
    e.ins('clr.w','%d1')
    _load(e,'selected_officer','d2')
    e.ins('move.b','(%a0,%d2.w),%d1',4)
    e.ins('mulu.w','%d0,%d1')
    e.ins('divu.w','#100,%d1',4)
    e.ins('sub.b','%d1,(%a0,%d2.w)',4)
    e.ins('bcc.w',done,4)
    e.ins('clr.b','(%a0,%d2.w)',4)
    e.label(done)


LOWERERS = {
    'settle_personnel_joining':_dispatch,
    'settle_bribe_joining':_bribe,
    'bribe_acceptance_factor':_bribe_factor,
    'penalize_force_head_affinity':_head_penalty,
    'reward_force_head_small_progress':_small_progress,
    'reward_force_head_large_progress':_large_head_progress,
    'transfer_joining_officer':_transfer,
    'settle_persuasion_joining':_persuasion,
    'persuasion_scores':_scores,
    'persuasion_factor':_persuasion_factor,
    'reward_actor_small_progress':lambda e,r:_small_progress(e,r,True),
    'reward_actor_large_progress':_large_actor_progress,
    'penalize_actor_affinity':_actor_penalty,
}


def compile_personnel(source):
    records = semantic_ir(source)
    bindings = {binding.name:binding for binding in PERSONNEL_BINDINGS}
    if set(bindings) != set(LOWERERS):
        raise CompileError('thirteen complete target ABI bindings required')
    units = []
    for record in records:
        emitter = Emitter(bindings[record['name']])
        emitter.begin()
        LOWERERS[record['name']](emitter,record['rules'])
        emitter.end()
        unit = emitter.unit(record['effects'])
        if sum(row['encoding_bytes'] for row in unit['instructions']) != bindings[record['name']].end-bindings[record['name']].entry:
            raise CompileError(record['name']+': complete fixed target extent mismatch')
        units.append(unit)
    allocated = sum(sum(row['encoding_bytes'] for row in unit['instructions']) for unit in units)
    count = sum(len(unit['instructions']) for unit in units)
    if (allocated,count) != (1568,448):
        raise CompileError('complete thirteen-unit personnel allocation required')
    return dict(units=units,allocated_bytes=allocated,instructions=count,
                original_generation_input=False,complete_CPU=False)
