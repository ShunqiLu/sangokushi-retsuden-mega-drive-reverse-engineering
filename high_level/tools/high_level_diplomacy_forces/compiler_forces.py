"""Complete semantic-flow admission and ordinary GNU force lowering.

The compatibility backend owns ABI/encoding choices, not source code payloads.
Generation consumes explicit Python text only; no ROM, old ASM or file reads.
"""
import ast
from copy import deepcopy
from .compiler_common import CompileError, Emitter, require_declared_names
from .target import FORCES_BINDINGS

FLOW = r'''"""Live force reassignment, disbanding and packed/queued state cleanup.

Roles are probable; exact ordering, widths and unusual aliases are the original
compatibility contract. No natural force/city catalog or complete CPU is implied.
"""
from .domain import (GameState, Table, Word, uint, u16, u32, low8, low16, high16,
                     replace_byte, replace_word, negative_byte, negative_word,
                     descending_inclusive, divu_retained)
from .business_shared import choose_city_head


def resolve_force_reassignment(state: GameState) -> None:
    leaders = state.force_heads
    owners = state.city_owners
    assignments = state.officer_assignments
    statuses = state.officer_status
    change = state.pending_force_change()
    if not negative_word(change):
        new_force = u16(low8(change))
        old_force = u16(change >> 8)
        if old_force == state.removed_force():
            state.set_loyalty_source(leaders.word(u16(new_force << 1)))
            threshold = u16(50)
            city = u16(56)
            while True:
                if low8(old_force) == owners.byte(city):
                    reassign_city_officers(state, city, threshold, new_force, owners, assignments, statuses)
                    reduce_city_reserve(state, city, owners)
                    return_temporary_city_assignments(state, city)
                    clear_disbanded_city_orders(state, old_force)
                city = u16(city - 1)
                if city == 0:
                    break
            remove_force_group_packets(state, old_force, 0, assignments)
        else:
            state.set_loyalty_source(leaders.word(u16(old_force << 1)))
            threshold = u16(90)
            city = u16(56)
            while True:
                if low8(new_force) == owners.byte(city):
                    reassign_city_officers(state, city, threshold, old_force, owners, assignments, statuses)
                    reduce_city_reserve(state, city, owners)
                    return_temporary_city_assignments(state, city)
                    clear_disbanded_city_orders(state, old_force)
                city = u16(city - 1)
                if city == 0:
                    break
            remove_force_group_packets(state, new_force, 0, assignments)
    else:
        owners = state.other_city_owners
        heads = state.other_city_heads
        force = state.removed_force()
        for index in descending_inclusive(55):
            if owners.byte(index) == low8(force):
                if index < 40:
                    owners.set_byte(index, 255)
                    heads.set_word(u16(index << 1), 65535)
                mark_city_assignments_inactive(state, index)
                clear_disbanded_temporary_assignments(state, index)
                clear_disbanded_city_orders(state, index)
        disband_force_group_packets(state)
    state.force_heads.set_word(u16(state.removed_force() << 1), 65535)
    state.set_pending_force_change(0)
    state.set_route(524)


def reassign_city_officers(state: GameState, city: Word, status_threshold: Word,
                          new_force: Word, owners: Table, assignments: Table,
                          statuses: Table) -> None:
    city = uint(city, 16)
    status_threshold = uint(status_threshold, 16)
    new_force = uint(new_force, 16)
    owners = state.checked_table(owners)
    assignments = state.checked_table(assignments)
    statuses = state.checked_table(statuses)
    if city >= 41:
        return
    roster = state.candidate_roster.cursor()
    heads = state.city_heads
    count = u16(0)
    for officer in descending_inclusive(255):
        if assignments.byte(officer) == low8(city):
            if statuses.byte(officer) < low8(status_threshold):
                roster.append_word(officer)
                state.set_selected_officer(officer)
                state.apply_returning_officer_loyalty()
                count = u16(count + 1)
            else:
                assignments.set_byte(officer, assignments.byte(officer) | 128)
    roster.set_word(0, 65535)
    if count != 0:
        owners.set_byte(city, low8(new_force))
        choose_city_head(state, city)
        clear_transferred_city_orders(state, city)
    else:
        owners.set_byte(city, 255)
        heads.set_word(u16(city << 1), 65535)
        clear_transferred_city_orders(state, city)


def clear_transferred_city_orders(state: GameState, city: Word) -> None:
    city = uint(city, 16)
    if city >= 41:
        return
    index = u16(u16((city << 1) + city) << 2)
    orders = state.city_orders
    flags = state.officer_flags
    for displacement in (0, 4, 8):
        officer = orders.word(index, displacement)
        if not negative_word(officer):
            flags.set_byte(officer, 0)
            orders.set_word(index, 65535, displacement)


def remove_force_group_packets(state: GameState, force: Word, retained_stride: Word,
                               assignments: Table) -> None:
    force = uint(force, 16)
    retained_stride = uint(retained_stride, 16)
    assignments = state.checked_table(assignments)
    packet = state.packed_groups
    while True:
        retained_stride = u16(replace_byte(retained_stride, packet.byte() & 15))
        if low8(retained_stride) == 0:
            return
        if packet.byte(0, 4) == low8(force):
            remaining = u16(retained_stride - 1)
            for member in descending_inclusive(remaining):
                officer = u16(packet.byte(member, 13))
                assignments.set_byte(officer, assignments.byte(officer) | 128)
                assignments.set_byte(officer, assignments.byte(officer) & 191)
            remove_packet_pair_reference(state, packet)
            compact_following_packets(state, packet, retained_stride)
        else:
            packet = packet.at(retained_stride, 13)


def compact_following_packets(state: GameState, packet: Table, retained_stride: Word) -> None:
    retained_stride = uint(retained_stride, 16)
    packet = state.checked_table(packet)
    source = packet.at(retained_stride, 13).cursor()
    destination = packet.cursor()
    while True:
        count = u16(source.byte() & 15)
        if count == 0:
            break
        count = u16(count + 12)
        for remaining in descending_inclusive(count):
            destination.append_byte(source.next_byte())
    destination.set_byte(0, 0)


def remove_packet_pair_reference(state: GameState, packet: Table) -> None:
    packet = state.checked_table(packet)
    head = u16(packet.byte(0, 13))
    pairs = state.pair_references.at(state.pair_reference_offset())
    while pairs.byte() != 0:
        if pairs.byte(0, 1) == low8(head):
            source = pairs.at(0, 2).cursor()
            destination = pairs.cursor()
            while True:
                value = source.next_byte()
                destination.append_byte(value)
                if value == 0:
                    return
                destination.append_byte(source.next_byte())
        pairs = pairs.advance(2)


def reduce_city_reserve(state: GameState, city: Word, owners: Table) -> None:
    city = uint(city, 16)
    owners = state.checked_table(owners)
    if city >= 41:
        return
    if negative_byte(owners.byte(city)):
        return
    sample = u32(state.sample_random() & 65535)
    rate = u16(high16(u32(sample * 21)) + 10)
    reserves = state.city_reserves
    index = u16(city << 2)
    reserve = reserves.long(index)
    product = u32(low16(reserve) * low16(rate))
    quotient = divu_retained(product, 100)
    reserve = replace_word(reserve, u16(low16(reserve) - low16(quotient)))
    reserves.set_long(index, reserve)


def return_temporary_city_assignments(state: GameState, city: Word) -> None:
    city = uint(city, 16)
    assignments = state.officer_assignments
    alternate = state.alternate_assignments
    processed = state.city_processed
    temporary = state.temporary_city_flags
    mask = state.temporary_city_bits
    expected = u16(replace_byte(city, low8(city) | 64))
    for officer in descending_inclusive(255):
        value = u16(assignments.byte(officer))
        if low8(value) != low8(expected):
            value = u16(value & 63)
            if value < 41:
                continue
            value = u16(value | 64)
            if low8(value) != low8(expected):
                continue
        value = u16(alternate.byte(officer))
        if value == 0:
            continue
        value = u16(value & 63)
        assignments.set_byte(officer, low8(value | 128))
        alternate.set_byte(officer, 0)
        processed.set_byte(value, 0)
        temporary.set_byte(value, 0)
        slot = u16(value - 1)
        bit = slot & 7
        mask_index = u16(slot >> 3)
        mask.set_byte(mask_index, mask.byte(mask_index) & (255 ^ (1 << bit)))
        remove_officer_pair_reference(state, officer)


def remove_officer_pair_reference(state: GameState, officer: Word) -> None:
    officer = uint(officer, 16)
    source = state.pair_references.at(state.pair_reference_offset()).cursor()
    while source.next_byte() != 0:
        if source.next_byte() != low8(officer):
            continue
        while True:
            value = source.next_byte()
            source.set_byte(0, value, -3)
            if value == 0:
                return
            value = source.next_byte()
            source.set_byte(0, value, -3)


def mark_city_assignments_inactive(state: GameState, index: Word) -> None:
    index = uint(index, 16)
    city = u16(index + 1)
    assignments = state.officer_assignments.cursor()
    for officer in descending_inclusive(255):
        if assignments.next_byte() == low8(city):
            assignments.set_byte(0, assignments.byte(0, -1) | 128, -1)


def disband_force_group_packets(state: GameState) -> None:
    packet = state.packed_groups
    assignments = state.officer_assignments
    force = state.removed_force()
    while True:
        count = u16(packet.byte() & 15)
        if count == 0:
            return
        if packet.byte(0, 4) != low8(force):
            packet = packet.at(count, 13)
            continue
        for member in descending_inclusive(u16(count - 1)):
            officer = u16(packet.byte(member, 13))
            value = u16(assignments.byte(officer) & 63)
            if value != 0:
                value = u16(value | 128)
            else:
                value = u16(replace_byte(value, 129))
            assignments.set_byte(officer, low8(value))
        remove_disbanded_packet_reference(state, packet)
        source = packet.at(count, 13).cursor()
        destination = packet.cursor()
        while True:
            following_count = u16(source.byte() & 15)
            if following_count == 0:
                break
            for remaining in descending_inclusive(u16(following_count + 12)):
                destination.append_byte(source.next_byte())
        destination.set_byte(0, 0)


def remove_disbanded_packet_reference(state: GameState, packet: Table) -> None:
    packet = state.checked_table(packet)
    pairs = state.pair_references.at(state.pair_reference_offset())
    head = packet.byte(0, 13)
    while pairs.byte() != 0:
        if pairs.byte(0, 1) == head:
            source = pairs.at(0, 2).cursor()
            destination = pairs.cursor()
            while True:
                value = source.next_byte()
                destination.append_byte(value)
                if value == 0:
                    return
                destination.append_byte(source.next_byte())
        pairs = pairs.advance(2)


def clear_disbanded_temporary_assignments(state: GameState, index: Word) -> None:
    index = uint(index, 16)
    expected = u16(u16(index + 1) | 64)
    assignments = state.officer_assignments
    alternate = state.alternate_assignments
    processed = state.city_processed
    temporary = state.temporary_city_flags
    mask = state.temporary_city_bits
    for officer in descending_inclusive(255):
        value = u16(assignments.byte(officer))
        if not value & 64:
            if low8(value) < 41:
                continue
            value = u16(value | 64)
        if low8(value) != low8(expected):
            continue
        value = u16(alternate.byte(officer))
        if value == 0:
            continue
        value = u16(value & 63)
        processed.set_byte(value, 0)
        alternate.set_byte(officer, 0)
        temporary.set_byte(value, 0)
        assignments.set_byte(officer, low8(value | 128))
        slot = u16(value - 1)
        bit = slot & 7
        mask_index = u16(slot >> 3)
        mask.set_byte(mask_index, mask.byte(mask_index) & (255 ^ (1 << bit)))


def clear_disbanded_city_orders(state: GameState, index: Word) -> None:
    index = uint(index, 16)
    if index >= 40:
        return
    clear_city_queue_principals(state, index)
    offset = u16(u16((index << 1) + index) << 2)
    orders = state.other_city_orders
    flags = state.officer_flags
    for displacement in (0, 4, 8):
        officer = orders.word(offset, displacement)
        if not negative_word(officer):
            flags.set_byte(officer, 0)
            orders.set_word(offset, 65535, displacement)


def clear_city_queue_principals(state: GameState, index: Word) -> None:
    index = uint(index, 16)
    principals = state.queue_principals
    principals.set_long(u16(index << 2), 0)
    queue = state.force_queue
    slot = u16(0)
    while True:
        if queue.byte() == low8(index):
            other = u16(queue.byte(0, 1))
            principals.set_long(u16(other << 2), 0)
            mask = state.force_queue_mask()
            state.set_force_queue_mask(u16(mask & ~(1 << (slot & 31))))
            queue.set_long(0, 0)
        queue = queue.advance(4)
        slot = u16(slot + 1)
        if slot >= 16:
            break

'''

DOMAIN_IMPORTS = {'GameState','Table','Word','uint','u16','u32','low8','low16','high16',
                  'replace_byte','replace_word','negative_byte','negative_word',
                  'descending_inclusive','divu_retained'}
SHARED_IMPORTS = {'choose_city_head'}


def _strip_docs(node):
    node = deepcopy(node)
    if (node.body and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and type(node.body[0].value.value) is str):
        node.body.pop(0)
    return node


def _holes(function):
    rules = {}
    for node in ast.walk(function):
        if function.name == 'reduce_city_reserve':
            if (isinstance(node,ast.Assign) and len(node.targets)==1
                    and isinstance(node.targets[0],ast.Name) and node.targets[0].id=='rate'
                    and isinstance(node.value,ast.Call) and len(node.value.args)==1
                    and isinstance(node.value.args[0],ast.BinOp)
                    and isinstance(node.value.args[0].right,ast.Constant)):
                value=node.value.args[0].right.value
                if type(value) is not int or not 0<=value<=65535:
                    raise CompileError('reserve baseline requires full WORD literal')
                rules['reserve_baseline']=value
                node.value.args[0].right=ast.Name(id='__reserve_baseline',ctx=ast.Load())
    return rules


def semantic_ir(source):
    if type(source) is not str:
        raise CompileError('explicit semantic force text required')
    try:
        module = _strip_docs(ast.parse(source))
    except SyntaxError as exc:
        raise CompileError('invalid semantic Python') from exc
    functions, imports = {}, set()
    for node in module.body:
        if isinstance(node,ast.ImportFrom):
            permitted = DOMAIN_IMPORTS if node.module=='domain' else SHARED_IMPORTS if node.module=='business_shared' else set()
            if node.level!=1 or not permitted:
                raise CompileError('only explicit approved typed imports required')
            for alias in node.names:
                if alias.asname is not None or alias.name not in permitted:
                    raise CompileError('unknown or aliased import')
                imports.add(alias.name)
        elif isinstance(node,ast.FunctionDef):
            if node.name in functions:
                raise CompileError('duplicate business function')
            functions[node.name]=_strip_docs(node)
        else:
            raise CompileError('complete typed functions and imports only')
    expected = {n.name:n for n in ast.parse(FLOW).body if isinstance(n,ast.FunctionDef)}
    if set(functions)!=set(expected):
        raise CompileError('all fifteen complete force functions required')
    require_declared_names(functions,imports)
    records=[]
    for name,contract in expected.items():
        function=functions[name]
        normalized=deepcopy(function)
        rules=_holes(normalized)
        _holes(contract)
        if ast.dump(normalized,include_attributes=False)!=ast.dump(contract,include_attributes=False):
            raise CompileError(name+': unsupported signature, type, control, return, call or DATA expression')
        effects=[]
        for node in ast.walk(function):
            if isinstance(node,(ast.stmt,ast.Call,ast.Compare,ast.BinOp)):
                effect={'operation':type(node).__name__,'semantic':ast.dump(node,include_attributes=False)}
                if isinstance(node,ast.Call):
                    called=node.func.attr if isinstance(node.func,ast.Attribute) else node.func.id if isinstance(node.func,ast.Name) else ''
                    effect['ordered_live_operation']=called
                    width={'byte':8,'set_byte':8,'next_byte':8,'append_byte':8,'low8':8,
                           'word':16,'set_word':16,'u16':16,'low16':16,
                           'long':32,'set_long':32,'u32':32}.get(called)
                    if width is not None:effect['value_bits']=width
                effects.append(effect)
        records.append({'name':name,'rules':rules,'effects':effects})
    return records


def _view(e,address,register,long=False):
    e.ins('lea.l',f'0x{address:x}:{"l" if long else "w"},%{register}',6 if long else 4)


def _word(e,address,register):
    e.ins('move.w',f'0x{address:x}:w,%{register}',4)


def _immediate_word(e,value,address):
    e.ins('move.w',f'#{value},0x{address:x}:w',6)


def _call(e,name):
    e.ins('bsr.w',name,4)


def _root(e,rules):
    disband, reverse, finish = (e.fresh(n) for n in ('disband','reverse_transfer','finish'))
    forward, forward_next, backward, backward_next = (e.fresh(n) for n in ('forward_city','forward_next','reverse_city','reverse_next'))
    scan, untouched, clear = (e.fresh(n) for n in ('owned_city_scan','unowned_city','clear_city_fields'))
    _view(e,0xe640,'a0');_view(e,0xf427,'a1');_view(e,0xcc00,'a2');_view(e,0xc300,'a3')
    _word(e,0xa622,'d0');e.ins('bmi.w',disband,4)
    e.ins('clr.w','%d1');e.ins('move.b','%d0,%d1');e.ins('lsr.w','#8,%d0')
    e.ins('cmp.w','0xefb0:w,%d0',4);e.ins('bne.w',reverse,4)
    e.ins('lsl.w','#1,%d1');e.ins('move.w','(%a0,%d1.w),%d2',4);e.ins('lsr.w','#1,%d1')
    e.ins('move.w','%d2,0xf3f2:w',4);e.ins('move.w','#50,%d3',4);e.ins('move.w','#56,%d2',4)
    e.label(forward);e.ins('cmp.b','(%a1,%d2.w),%d0',4);e.ins('bne.w',forward_next,4)
    e.ins('move.w','%d1,%d7');_call(e,'reassign_city_officers');_call(e,'reduce_city_reserve')
    e.ins('move.w','%d0,%d7');_call(e,'return_temporary_city_assignments')
    e.ins('move.l','%d1,-(%a7)');e.ins('move.w','%d0,%d1');_call(e,'clear_disbanded_city_orders');e.ins('move.l','(%a7)+,%d1')
    e.label(forward_next);e.ins('subq.w','#1,%d2');e.ins('bne.b',forward)
    e.ins('move.w','%d0,%d7');_call(e,'remove_force_group_packets');e.ins('bra.w',finish,4)
    e.label(reverse);e.ins('lsl.w','#1,%d0');e.ins('move.w','(%a0,%d0.w),%d2',4);e.ins('lsr.w','#1,%d0')
    e.ins('move.w','%d2,0xf3f2:w',4);e.ins('move.w','#90,%d3',4);e.ins('move.w','#56,%d2',4)
    e.label(backward);e.ins('cmp.b','(%a1,%d2.w),%d1',4);e.ins('bne.w',backward_next,4)
    e.ins('move.w','%d0,%d7');_call(e,'reassign_city_officers');_call(e,'reduce_city_reserve')
    e.ins('move.w','%d1,%d7');_call(e,'return_temporary_city_assignments')
    e.ins('move.l','%d1,-(%a7)');e.ins('move.w','%d0,%d1');_call(e,'clear_disbanded_city_orders');e.ins('move.l','(%a7)+,%d1')
    e.label(backward_next);e.ins('subq.w','#1,%d2');e.ins('bne.b',backward)
    e.ins('move.w','%d1,%d7');_call(e,'remove_force_group_packets');e.ins('bra.w',finish,4)
    e.label(disband);_view(e,0xf428,'a0');_view(e,0xf460,'a1');_word(e,0xefb0,'d0');e.ins('move.w','#55,%d1',4)
    e.label(scan);e.ins('cmp.b','(%a0,%d1.w),%d0',4);e.ins('bne.w',untouched,4)
    e.ins('cmpi.w','#40,%d1',4);e.ins('bcc.w',clear,4)
    e.ins('move.b','#255,(%a0,%d1.w)',6);e.ins('move.w','%d1,%d2');e.ins('lsl.w','#1,%d2');e.ins('move.w','#65535,(%a1,%d2.w)',6)
    e.label(clear);_call(e,'mark_city_assignments_inactive');_call(e,'clear_disbanded_temporary_assignments');_call(e,'clear_disbanded_city_orders')
    e.label(untouched);e.ins('dbra','%d1,'+scan,4);_call(e,'disband_force_group_packets')
    e.label(finish);_view(e,0xe640,'a0');_word(e,0xefb0,'d0');e.ins('lsl.w','#1,%d0')
    e.ins('move.w','#65535,(%a0,%d0.w)',6);e.ins('clr.w','0xa622:w',4);_immediate_word(e,524,0xf612)


def _reassign(e,rules):
    done, scan, next_, inactive, empty, finish = (e.fresh(n) for n in ('done','officer_scan','next_officer','inactive','empty_city','orders'))
    e.ins('cmpi.w','#41,%d2',4);e.ins('bcc.w',done,4)
    _view(e,0xf500,'a4');_view(e,0xf45e,'a5');e.ins('move.w','#255,%d4',4);e.ins('clr.w','%d5')
    e.label(scan);e.ins('cmp.b','(%a2,%d4.w),%d2',4);e.ins('bne.w',next_,4)
    e.ins('cmp.b','(%a3,%d4.w),%d3',4);e.ins('bls.w',inactive,4)
    e.ins('move.w','%d4,(%a4)+');e.ins('move.w','%d4,0xf3a6:w',4)
    e.ins('jsr','apply_returning_officer_loyalty:l',6);e.ins('addq.w','#1,%d5');e.ins('bra.w',next_,4)
    e.label(inactive);e.ins('bset.b','#7,(%a2,%d4.w)',6)
    e.label(next_);e.ins('dbra','%d4,'+scan,4);e.ins('move.w','#65535,(%a4)',4)
    e.ins('tst.w','%d5');e.ins('beq.w',empty,4)
    e.ins('move.b','%d7,(%a1,%d2.w)',4);e.ins('move.w','%d0,-(%a7)');e.ins('move.w','%d2,%d0')
    e.ins('jsr','choose_city_head:l',6);e.ins('move.w','(%a7)+,%d0');_call(e,'clear_transferred_city_orders');e.ins('bra.w',done,4)
    e.label(empty);e.ins('move.b','#255,(%a1,%d2.w)',6);e.ins('move.w','%d2,%d6');e.ins('lsl.w','#1,%d6')
    e.ins('move.w','#65535,(%a5,%d6.w)',6);_call(e,'clear_transferred_city_orders');e.label(done)


def _clear_orders(e,rules):
    done=e.fresh('restore');e.ins('movem.l','%d0-%d1/%a0-%a1,-(%a7)',4)
    e.ins('cmpi.w','#41,%d2',4);e.ins('bcc.w',done,4)
    e.ins('move.w','%d2,%d0');e.ins('lsl.w','#1,%d0');e.ins('add.w','%d2,%d0');e.ins('lsl.w','#2,%d0')
    _view(e,0xe80c,'a0');_view(e,0xcd00,'a1')
    for displacement in (0,4,8):
        next_=e.fresh('next_order')
        e.ins('move.w',f'{displacement}(%a0,%d0.w),%d1',4);e.ins('bmi.w',next_,4)
        e.ins('clr.b','(%a1,%d1.w)',4);e.ins('move.w',f'#65535,{displacement}(%a0,%d0.w)',6);e.label(next_)
    e.label(done);e.ins('movem.l','(%a7)+,%d0-%d1/%a0-%a1',4)


def _remove_packets(e,rules):
    scan, next_, members, done = (e.fresh(n) for n in ('packet_scan','following_packet','members','done'))
    _view(e,0x9000,'a4');_view(e,0xd300,'a5')
    e.label(scan);e.ins('move.b','(%a4),%d0');e.ins('andi.b','#15,%d0',4);e.ins('beq.w',done,4)
    e.ins('cmp.b','4(%a4),%d7',4);e.ins('bne.w',next_,4)
    e.ins('move.w','%d0,%d1');e.ins('subq.w','#1,%d1');e.ins('clr.w','%d4')
    e.label(members);e.ins('clr.w','%d2');e.ins('move.b','13(%a4,%d1.w),%d2',4)
    e.ins('bset.b','#7,(%a2,%d2.w)',6);e.ins('bclr.b','#6,(%a2,%d2.w)',6)
    e.ins('dbra','%d1,'+members,4);_call(e,'remove_packet_pair_reference');_call(e,'compact_following_packets');e.ins('bra.b',scan)
    e.label(next_);e.ins('lea.l','13(%a4,%d0.w),%a4',4);e.ins('bra.b',scan);e.label(done)


def _compact(e,rules):
    packet, copy, done = (e.fresh(n) for n in ('following_packet','copy','done'))
    e.ins('lea.l','13(%a4,%d0.w),%a5',4);e.ins('lea.l','(%a4),%a6')
    e.label(packet);e.ins('move.b','(%a5),%d0');e.ins('andi.w','#15,%d0',4);e.ins('beq.w',done,4);e.ins('addi.w','#12,%d0',4)
    e.label(copy);e.ins('move.b','(%a5)+,(%a6)+');e.ins('dbra','%d0,'+copy,4);e.ins('bra.b',packet)
    e.label(done);e.ins('clr.b','(%a6)')


def _packet_reference(e,rules):
    scan, copy, done = (e.fresh(n) for n in ('pair_scan','copy','restore'))
    e.ins('movem.l','%d0-%d1,-(%a7)',4);e.ins('clr.w','%d0');e.ins('move.b','13(%a4),%d0',4)
    _view(e,0xff39b2,'a5',True);e.ins('adda.w','0xff3bb2:l,%a5',6)
    e.label(scan);e.ins('tst.b','(%a5)');e.ins('beq.w',done,4)
    e.ins('cmp.b','1(%a5),%d0',4);target=e.fresh('pair_found');e.ins('beq.w',target,4)
    e.ins('lea.l','2(%a5),%a5',4);e.ins('bra.b',scan);e.label(target);e.ins('lea.l','2(%a5),%a6',4)
    e.label(copy);e.ins('move.b','(%a6)+,(%a5)+');e.ins('beq.w',done,4);e.ins('move.b','(%a6)+,(%a5)+');e.ins('bra.b',copy)
    e.label(done);e.ins('movem.l','(%a7)+,%d0-%d1',4)


def _reduce(e,rules):
    done=e.fresh('done');e.ins('cmpi.w','#41,%d2',4);e.ins('bcc.w',done,4)
    e.ins('tst.b','(%a1,%d2.w)',4);e.ins('bmi.w',done,4)
    e.ins('movem.l','%d0-%d1/%a4,-(%a7)',4);e.ins('jsr','step_random:l',6)
    e.ins('andi.l','#65535,%d0',6);e.ins('move.l','%d0,%d1');e.ins('lsl.l','#2,%d0');e.ins('add.l','%d1,%d0')
    e.ins('lsl.l','#2,%d0');e.ins('add.l','%d1,%d0');e.ins('swap','%d0');e.ins('addi.w',f"#{rules['reserve_baseline']},%d0",4)
    _view(e,0xe31c,'a4');e.ins('move.w','%d2,%d1');e.ins('lsl.w','#2,%d1')
    e.ins('move.l','(%a4,%d1.w),%d4',4);e.ins('move.l','%d4,%d5');e.ins('mulu.w','%d0,%d5');e.ins('divu.w','#100,%d5',4)
    e.ins('sub.w','%d5,%d4');e.ins('move.l','%d4,(%a4,%d1.w)',4);e.ins('movem.l','(%a7)+,%d0-%d1/%a4',4);e.label(done)


def _temporary_return(e,rules):
    scan, next_, restore = (e.fresh(n) for n in ('officer_scan','next_officer','restore_assignment'))
    e.ins('movem.l','%d3-%d7/%a0-%a4,-(%a7)',4)
    for address,register in ((0xcc00,'a0'),(0xa050,'a1'),(0xea37,'a2'),(0x9fff,'a3'),(0xefaa,'a4')):_view(e,address,register)
    e.ins('move.w','%d2,%d4');e.ins('ori.b','#64,%d4',4);e.ins('move.w','#255,%d5',4)
    e.label(scan);e.ins('move.b','(%a0,%d5.w),%d6',4);e.ins('cmp.b','%d4,%d6');e.ins('beq.w',restore,4)
    e.ins('andi.w','#63,%d6',4);e.ins('cmpi.w','#41,%d6',4);e.ins('bcs.w',next_,4);e.ins('ori.w','#64,%d6',4)
    e.ins('cmp.b','%d4,%d6');e.ins('bne.w',next_,4)
    e.label(restore);e.ins('move.b','(%a1,%d5.w),%d6',4);e.ins('beq.w',next_,4);e.ins('andi.w','#63,%d6',4)
    e.ins('move.w','%d6,%d7');e.ins('bset.l','#7,%d6',4);e.ins('move.b','%d6,(%a0,%d5.w)',4)
    e.ins('clr.b','(%a1,%d5.w)',4);e.ins('bclr.l','#7,%d6',4);e.ins('clr.b','(%a2,%d6.w)',4);e.ins('clr.b','(%a3,%d6.w)',4)
    e.ins('subq.w','#1,%d6');e.ins('move.w','%d6,%d3');e.ins('lsr.w','#3,%d6');e.ins('andi.w','#7,%d3',4)
    e.ins('bclr.b','%d3,(%a4,%d6.w)',4);_call(e,'remove_officer_pair_reference')
    e.label(next_);e.ins('dbra','%d5,'+scan,4);e.ins('movem.l','(%a7)+,%d3-%d7/%a0-%a4',4)


def _officer_pair(e,rules):
    scan, copy, done = (e.fresh(n) for n in ('pair_scan','copy','restore'))
    e.ins('movem.l','%a0,-(%a7)',4);_view(e,0xff39b2,'a0',True);e.ins('adda.w','0xff3bb2:l,%a0',6)
    e.label(scan);e.ins('tst.b','(%a0)+');e.ins('beq.w',done,4);e.ins('cmp.b','(%a0)+,%d5');e.ins('bne.b',scan)
    e.label(copy);e.ins('move.b','(%a0)+,-3(%a0)',4);e.ins('beq.w',done,4);e.ins('move.b','(%a0)+,-3(%a0)',4);e.ins('bra.b',copy)
    e.label(done);e.ins('movem.l','(%a7)+,%a0',4)


def _mark_inactive(e,rules):
    scan, next_ = e.fresh('assignment_scan'), e.fresh('next_assignment')
    e.ins('movem.l','%d0-%d1/%a0,-(%a7)',4);e.ins('addq.w','#1,%d1');_view(e,0xcc00,'a0');e.ins('move.w','#255,%d0',4)
    e.label(scan);e.ins('cmp.b','(%a0)+,%d1');e.ins('bne.w',next_,4);e.ins('bset.b','#7,-1(%a0)',6)
    e.label(next_);e.ins('dbra','%d0,'+scan,4);e.ins('movem.l','(%a7)+,%d0-%d1/%a0',4)


def _disband_packets(e,rules):
    scan, members, fallback, store, next_, copy, terminator, found, done = (e.fresh(n) for n in ('packet_scan','member','fallback','store','following_packet','copy','terminator','owned_packet','restore'))
    e.ins('movem.l','%d0-%d4/%a0-%a3,-(%a7)',4);_view(e,0x9000,'a0');_view(e,0xcc00,'a1');_word(e,0xefb0,'d0')
    e.label(scan);e.ins('move.b','(%a0),%d1');e.ins('andi.w','#15,%d1',4);e.ins('beq.w',done,4)
    e.ins('cmp.b','4(%a0),%d0',4);e.ins('beq.w',found,4);e.ins('lea.l','13(%a0,%d1.w),%a0',4);e.ins('bra.b',scan)
    e.label(found);e.ins('move.w','%d1,%d2');e.ins('subq.w','#1,%d2');e.ins('clr.w','%d3')
    e.label(members);e.ins('move.b','13(%a0,%d2.w),%d3',4);e.ins('move.b','(%a1,%d3.w),%d4',4)
    e.ins('andi.w','#63,%d4',4);e.ins('beq.w',fallback,4);e.ins('bset.l','#7,%d4',4);e.ins('bra.w',store,4)
    e.label(fallback);e.ins('move.b','#129,%d4',4);e.label(store);e.ins('move.b','%d4,(%a1,%d3.w)',4);e.ins('dbra','%d2,'+members,4)
    _call(e,'remove_disbanded_packet_reference');e.ins('lea.l','13(%a0,%d1.w),%a2',4);e.ins('movea.l','%a0,%a3')
    e.label(next_);e.ins('move.b','(%a2),%d1');e.ins('andi.w','#15,%d1',4);e.ins('beq.w',terminator,4);e.ins('addi.w','#12,%d1',4)
    e.label(copy);e.ins('move.b','(%a2)+,(%a3)+');e.ins('dbra','%d1,'+copy,4);e.ins('bra.b',next_)
    e.label(terminator);e.ins('clr.b','(%a3)');e.ins('bra.b',scan)
    e.label(done);e.ins('movem.l','(%a7)+,%d0-%d4/%a0-%a3',4)


def _disband_pair(e,rules):
    scan, found, copy, done = (e.fresh(n) for n in ('pair_scan','pair_found','copy','restore'))
    e.ins('movem.l','%d0/%a1-%a2,-(%a7)',4);_view(e,0xff39b2,'a1',True);e.ins('adda.w','0xff3bb2:l,%a1',6)
    e.ins('move.b','13(%a0),%d0',4);e.label(scan);e.ins('tst.b','(%a1)');e.ins('beq.w',done,4)
    e.ins('cmp.b','1(%a1),%d0',4);e.ins('beq.w',found,4);e.ins('addq.w','#2,%a1');e.ins('bra.b',scan)
    e.label(found);e.ins('lea.l','2(%a1),%a2',4);e.label(copy);e.ins('move.b','(%a2)+,(%a1)+');e.ins('beq.w',done,4)
    e.ins('move.b','(%a2)+,(%a1)+');e.ins('bra.b',copy);e.label(done);e.ins('movem.l','(%a7)+,%d0/%a1-%a2',4)


def _clear_temporary(e,rules):
    scan, compare, next_ = (e.fresh(n) for n in ('officer_scan','compare_city','next_officer'))
    e.ins('movem.l','%d0-%d3/%a0-%a5,-(%a7)',4);e.ins('addq.w','#1,%d1');e.ins('ori.w','#64,%d1',4)
    for address,register in ((0xcc00,'a0'),(0xa050,'a1'),(0xea37,'a3'),(0x9fff,'a4'),(0xefaa,'a5')):_view(e,address,register)
    e.ins('move.w','#255,%d0',4);e.label(scan);e.ins('move.b','(%a0,%d0.w),%d2',4)
    e.ins('btst.l','#6,%d2',4);e.ins('bne.w',compare,4);e.ins('cmpi.b','#41,%d2',4);e.ins('bcs.w',next_,4);e.ins('bset.l','#6,%d2',4)
    e.label(compare);e.ins('cmp.b','%d1,%d2');e.ins('bne.w',next_,4);e.ins('move.b','(%a1,%d0.w),%d2',4)
    e.ins('beq.w',next_,4);e.ins('andi.w','#63,%d2',4);e.ins('clr.b','(%a3,%d2.w)',4);e.ins('clr.b','(%a1,%d0.w)',4);e.ins('clr.b','(%a4,%d2.w)',4)
    e.ins('bset.l','#7,%d2',4);e.ins('move.b','%d2,(%a0,%d0.w)',4);e.ins('bclr.l','#7,%d2',4)
    e.ins('subq.w','#1,%d2');e.ins('move.w','%d2,%d3');e.ins('lsr.w','#3,%d2');e.ins('andi.w','#7,%d3',4)
    e.ins('bclr.b','%d3,(%a5,%d2.w)',4);e.label(next_);e.ins('dbra','%d0,'+scan,4);e.ins('movem.l','(%a7)+,%d0-%d3/%a0-%a5',4)


def _clear_disband_orders(e,rules):
    done=e.fresh('done');e.ins('cmpi.w','#40,%d1',4);e.ins('bcc.w',done,4)
    e.ins('movem.l','%d0-%d1/%a0-%a1,-(%a7)',4);_call(e,'clear_city_queue_principals')
    _view(e,0xe818,'a0');_view(e,0xcd00,'a1');e.ins('move.w','%d1,%d0');e.ins('lsl.w','#1,%d0');e.ins('add.w','%d1,%d0');e.ins('lsl.w','#2,%d0')
    for displacement in (0,4,8):
        next_=e.fresh('next_order');e.ins('move.w',f'{displacement}(%a0,%d0.w),%d1',4);e.ins('bmi.w',next_,4)
        e.ins('clr.b','(%a1,%d1.w)',4);e.ins('move.w',f'#65535,{displacement}(%a0,%d0.w)',6);e.label(next_)
    e.ins('movem.l','(%a7)+,%d0-%d1/%a0-%a1',4);e.label(done)


def _queue_principals(e,rules):
    scan, next_ = e.fresh('queue_scan'),e.fresh('next_slot')
    e.ins('move.l','%d2,-(%a7)');_view(e,0xe65c,'a0');e.ins('move.w','%d1,%d0');e.ins('lsl.w','#2,%d0');e.ins('clr.l','(%a0,%d0.w)',4)
    _view(e,0xe9f8,'a0');_view(e,0xe65c,'a1');e.ins('clr.w','%d0');e.label(scan);e.ins('cmp.b','(%a0),%d1');e.ins('bne.w',next_,4)
    e.ins('clr.w','%d2');e.ins('move.b','1(%a0),%d2',4);e.ins('lsl.w','#2,%d2');e.ins('clr.l','(%a1,%d2.w)',4)
    _word(e,0xe700,'d2');e.ins('bclr.l','%d0,%d2');e.ins('move.w','%d2,0xe700:w',4);e.ins('clr.l','(%a0)')
    e.label(next_);e.ins('addq.l','#4,%a0');e.ins('addq.w','#1,%d0');e.ins('cmpi.w','#16,%d0',4);e.ins('bcs.b',scan);e.ins('move.l','(%a7)+,%d2')


LOWERERS = {
    'resolve_force_reassignment':_root,'reassign_city_officers':_reassign,
    'clear_transferred_city_orders':_clear_orders,'remove_force_group_packets':_remove_packets,
    'compact_following_packets':_compact,'remove_packet_pair_reference':_packet_reference,
    'reduce_city_reserve':_reduce,'return_temporary_city_assignments':_temporary_return,
    'remove_officer_pair_reference':_officer_pair,'mark_city_assignments_inactive':_mark_inactive,
    'disband_force_group_packets':_disband_packets,'remove_disbanded_packet_reference':_disband_pair,
    'clear_disbanded_temporary_assignments':_clear_temporary,'clear_disbanded_city_orders':_clear_disband_orders,
    'clear_city_queue_principals':_queue_principals,
}


def compile_forces(source):
    records=semantic_ir(source)
    bindings={binding.name:binding for binding in FORCES_BINDINGS}
    if set(bindings)!=set(LOWERERS):raise CompileError('fifteen complete target ABI bindings required')
    units=[]
    for record in records:
        emitter=Emitter(bindings[record['name']]);emitter.begin()
        LOWERERS[record['name']](emitter,record['rules']);emitter.end()
        unit=emitter.unit(record['effects'])
        if sum(i['encoding_bytes'] for i in unit['instructions'])!=bindings[record['name']].end-bindings[record['name']].entry:
            raise CompileError(record['name']+': complete fixed extent mismatch')
        units.append(unit)
    allocated=sum(sum(i['encoding_bytes'] for i in u['instructions']) for u in units)
    count=sum(len(u['instructions']) for u in units)
    if (allocated,count)!=(1406,406):raise CompileError('all fifteen original bodies required')
    return {'units':units,'allocated_bytes':allocated,'instructions':count,
            'original_generation_input':False,'complete_CPU':False}
