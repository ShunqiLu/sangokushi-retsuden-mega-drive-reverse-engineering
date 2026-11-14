"""Finite typed member-flow admission and ordinary 68000 instruction selection.

Explicit semantic text is the sole generation input. The isolated backend owns
target register allocation, encoding widths, call forms and save/restore ABI;
it never reads an original image, assembly source, IR or prebuilt instruction.
"""
import ast
from .compiler_common import CompileError, Emitter, require_declared_names
from .target import MEMBERS_BINDINGS


SIGNATURES = {
    'settle_battle_packed_armies': ('state:GameState', 'None'),
    'remove_defeated_packed_member': ('state:GameState,officer:Word,context:GroupContext', 'GroupContext'),
    'replace_or_remove_group_references': ('state:GameState,old_head:Word,new_head:Word', 'None'),
    'transfer_outcome_officer': ('state:GameState', 'None'),
    'detach_member_keep_group_cursor': ('state:GameState,officer:Word,context:GroupContext', 'GroupContext'),
    'replace_group_head_reference': ('state:GameState,officer:Word,group:Table', 'None'),
    'remove_group_reference': ('state:GameState,officer:Word', 'None'),
    'attach_member_shift_packet': ('state:GameState,officer:Word,context:GroupContext', 'GroupContext'),
}

# Typed semantic contracts. These are executable Python flow declarations,
# not target mnemonic text, opcode bytes or hashes of the supplied program.
FLOWS = {
'settle_battle_packed_armies': '''transfer_outcome_officer(state)
selected=state.table(state.selected_group_pointer())
other=state.group_packets.at(state.group_offsets.word(state.selected_group_offset()))
context=GroupContext(selected,other)
officer=state.primary_officer()
if state.troops.word(u16(officer<<1))==0:
    officer=state.primary_officer()
    context=remove_defeated_packed_member(state,officer,context)
    state.set_selected_group_pointer(0)
context=GroupContext(context.target,context.source)
officer=state.secondary_officer()
if state.troops.word(u16(officer<<1))==0:
    officer=state.secondary_officer()
    context=remove_defeated_packed_member(state,officer,context)
    state.set_selected_group_pointer(context.target.address())
settle_group_at_city(state)
adjust_battle_losing_loyalty(state)''',
'remove_defeated_packed_member': '''officer=u16(officer)
context=checked_context(context,state)
group=context.source
state.officer_assignments.set_byte(officer,255)
old_head=group.byte(13)
count=group.byte()&15
if count==1:
    new_head=65535
    removed_bytes=14
    tail=group.at(count,13).cursor()
    destination=group.cursor()
else:
    group.set_byte(0,u8(group.byte()-1))
    index=0
    removed_bytes=1
    while group.byte(index,13)!=low8(officer):
        index=u16(index+1)
    while True:
        index=u16(index+1)
        if index==count:
            break
        group.set_byte(index,group.byte(index,13),12)
    tail=group.at(count,13).cursor()
    destination=group.at(count,12).cursor()
    new_head=group.byte(13)
while True:
    following_count=tail.byte()&15
    if following_count==0:
        destination.set_byte(0,0)
        break
    for copied in descending_inclusive(u16(following_count+12)):
        destination.append_byte(tail.next_byte())
replace_or_remove_group_references(state,old_head,new_head)
other=context.target
if other.address()>=group.address():
    other=other.advance(-removed_bytes)
return GroupContext(group,other)''',
'replace_or_remove_group_references': '''old_head=u16(old_head)
new_head=u16(new_head)
if new_head==old_head:
    return None
pairs=state.pair_references.at(state.pair_reference_offset()).cursor()
while True:
    if pairs.next_byte()==0:
        return None
    if pairs.next_byte()==low8(old_head):
        break
if negative_word(new_head):
    destination=pairs.advance(-2).cursor()
    while True:
        value=pairs.next_byte()
        destination.append_byte(value)
        if value==0:
            return None
        destination.append_byte(pairs.next_byte())
pairs.set_byte(65535,low8(new_head))
records=state.head_records.cursor()
while True:
    if negative_byte(records.next_byte()):
        return None
    if records.next_byte()==low8(old_head):
        records.set_byte(65535,low8(new_head))
        return None
    while records.next_byte()!=0:
        pass''',
'transfer_outcome_officer': '''outcome=state.outcome()
if outcome<6:
    return None
if outcome==6:
    officer=state.winning_officer()
else:
    officer=state.losing_officer()
source=state.table(state.selected_group_pointer())
target=state.group_packets.at(state.group_offsets.word(state.selected_group_offset()))
if officer!=state.primary_officer():
    source,target=target,source
context=detach_member_keep_group_cursor(state,officer,GroupContext(source,target))
context=attach_member_shift_packet(state,officer,context)
if officer!=state.primary_officer():
    context=GroupContext(context.target,context.source)
state.set_selected_group_pointer(context.source.address())
relative=u32(context.target.address()-state.group_packets.address())
state.group_offsets.set_word(state.selected_group_offset(),u16(relative))''',
'detach_member_keep_group_cursor': '''officer=u16(officer)
context=checked_context(context,state)
group=context.source
count=group.byte()&15
if count==1:
    removed_bytes=14
    remove_group_reference(state,officer)
    tail=group.at(count,13).cursor()
    destination=group.cursor()
else:
    removed_bytes=1
    index=0
    while group.byte(index,13)!=low8(officer):
        index=u16(index+1)
    index=u16(index+1)
    while index!=count:
        group.set_byte(index,group.byte(index,13),12)
        index=u16(index+1)
    replace_group_head_reference(state,officer,group)
    group.set_byte(0,u8(group.byte()-1))
    tail=group.at(count,13).cursor()
    destination=group.at(count,12).cursor()
while True:
    following_count=tail.byte()&15
    if following_count==0:
        destination.set_byte(0,0)
        break
    for copied in descending_inclusive(u16(following_count+12)):
        destination.append_byte(tail.next_byte())
other=context.target
if other.address()>=group.address():
    other=other.advance(-removed_bytes)
return GroupContext(group,other)''',
'replace_group_head_reference': '''officer=u16(officer)
group=checked_table(group,state)
replacement=group.byte(13)
pairs=state.pair_references.at(state.pair_reference_offset())
while pairs.byte()!=0:
    if pairs.byte(0,1)==low8(officer):
        break
    pairs=pairs.advance(2)
else:
    return None
pairs.set_byte(0,replacement,1)
records=state.head_records.cursor()
while records.byte(0,1)!=low8(officer):
    records=records.advance(1).cursor()
    while records.next_byte()!=0:
        pass
records.set_byte(0,replacement,1)''',
'remove_group_reference': '''officer=u16(officer)
pairs=state.pair_references.at(state.pair_reference_offset())
while pairs.byte()!=0:
    if pairs.byte(0,1)==low8(officer):
        break
    pairs=pairs.advance(2)
else:
    return None
source=pairs.advance(2).cursor()
destination=pairs.cursor()
while True:
    value=source.next_byte()
    destination.append_byte(value)
    if value==0:
        return None
    destination.append_byte(source.next_byte())''',
'attach_member_shift_packet': '''officer=u16(officer)
context=checked_context(context,state)
target=context.target
count=target.byte()&15
if count==10:
    added_bytes=0
    assignment=state.officer_assignments.byte(officer)&63
    if assignment<=40:
        assignment=u16(assignment|128)
        state.officer_assignments.set_byte(assignment,low8(assignment))
    else:
        assignment=u16(assignment-40)
        assignment=u16(assignment|128)
        state.officer_assignments.set_byte(officer,low8(assignment))
else:
    tail=target.at(count,13)
    destination=target.at(count,14).cursor()
    carried=tail.byte()
    while True:
        following_count=carried&15
        if following_count==0:
            destination.set_byte(0,0)
            break
        for copied in descending_inclusive(u16(following_count+12)):
            displaced=destination.byte()
            destination.append_byte(carried)
            carried=displaced
    count=target.byte()&15
    target.set_byte(0,u8(target.byte()+1))
    target.set_byte(count,low8(officer),13)
    assignment=u16(target.byte(4)+41)
    state.officer_assignments.set_byte(officer,low8(assignment))
    added_bytes=1
source=context.source
if source.address()>=target.address():
    source=source.advance(added_bytes)
return GroupContext(source,target)''',
}

APPROVED_DOMAIN = {'GameState', 'GroupContext', 'Table', 'Word', 'checked_context', 'checked_table',
                   'descending_inclusive', 'low8', 'negative_byte', 'negative_word', 'u8', 'u16', 'u32'}
APPROVED_ARRIVAL = {'settle_group_at_city', 'adjust_battle_losing_loyalty'}
SLOTS = {
    'remove_defeated_packed_member': {255: ('removed_assignment', 0, 255)},
    'transfer_outcome_officer': {6: ('transfer_outcome', 0, 65535)},
    'attach_member_shift_packet': {10: ('capacity_comparison', 0, 65535)},
}


def parse(source):
    if type(source) is not str:
        raise CompileError('explicit member semantic text required')
    try:
        tree = ast.parse(source)
    except (ValueError, SyntaxError) as error:
        raise CompileError('invalid member Python source') from error
    functions, imported = {}, set()
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and type(node.value.value) is str:
            continue
        if isinstance(node, ast.ImportFrom):
            approved = APPROVED_DOMAIN if node.module == 'domain' else APPROVED_ARRIVAL if node.module == 'business_arrival' else set()
            if node.level != 1 or any(item.asname or item.name not in approved for item in node.names):
                raise CompileError('explicit approved typed domain/arrival imports required')
            imported.update(item.name for item in node.names)
            continue
        if not isinstance(node, ast.FunctionDef) or node.name not in SIGNATURES or node.name in functions:
            raise CompileError('exactly eight declared member functions required')
        if node.type_params or node.decorator_list:
            raise CompileError('generic/decorated member ABI is not supported')
        functions[node.name] = node
    if set(functions) != set(SIGNATURES):
        raise CompileError('all eight member functions required')
    require_declared_names(functions, imported)
    result = {}
    for name, function in functions.items():
        signature, returned = SIGNATURES[name]
        expected = ast.parse(f'def {name}({signature})->{returned}:\n' +
                             '\n'.join('    '+line for line in FLOWS[name].splitlines())).body[0]
        body = list(function.body)
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and type(body[0].value.value) is str:
            body = body[1:]
        actual = ast.FunctionDef(name=function.name, args=function.args, body=body,
                                decorator_list=function.decorator_list, returns=function.returns,
                                type_comment=function.type_comment, type_params=function.type_params)
        slots = {}
        def compare(want, have):
            if type(want) is not type(have):
                raise CompileError(name+': unsupported typed/control structure')
            if isinstance(want, ast.Constant):
                if type(want.value) is not type(have.value):
                    raise CompileError(name+': strict semantic literal type')
                spec = SLOTS.get(name, {}).get(want.value) if type(want.value) is int else None
                if spec:
                    role, first, last = spec
                    if not first <= have.value <= last:
                        raise CompileError(name+': semantic '+role+' outside encoding width')
                    if role in slots and slots[role] != have.value:
                        raise CompileError(name+': duplicate semantic slot must agree')
                    slots[role] = have.value
                elif want.value != have.value:
                    raise CompileError(name+': unsupported semantic literal edit')
                return
            if isinstance(want, ast.AST):
                for key, value in ast.iter_fields(want):
                    compare(value, getattr(have, key))
            elif type(want) is list:
                if len(want) != len(have):
                    raise CompileError(name+': every return/control/effect must be consumed')
                for a, b in zip(want, have):
                    compare(a, b)
            elif want != have:
                raise CompileError(name+': unsupported variable/import/type/operator')
        compare(expected, actual)
        result[name] = dict(slots=slots, signature=signature, returns=returned,
                            complete_flow_consumed=True, context_return_not_void=returned=='GroupContext')
    return result


class Lowerer:
    """Compatibility register allocation is isolated from semantic program input."""
    def __init__(self, binding, effects):
        self.e = Emitter(binding)
        self.e.begin()
        self.effects = effects

    def ins(self, op, args='', width=2): self.e.ins(op, args, width)
    def label(self, name): self.e.label(name)
    def fresh(self, role): return self.e.fresh(role)
    def branch(self, condition, label, short=False): self.ins(condition+('.b' if short else '.w'), label, 2 if short else 4)
    def immediate(self, op, value, destination, width=4): self.ins(op, f'#0x{value:x},{destination}', width)
    def slot(self, name, default): return self.effects['slots'].get(name, default)
    def call(self, name): self.ins('bsr.w', name, 4)

    def settle_battle_packed_armies(self):
        self.call('transfer_outcome_officer')
        self.ins('movea.l', '0xff382c:l,%a1', 6)
        self.ins('lea.l', '0x9000:w,%a2', 4); self.ins('lea.l', '0xefbe:w,%a3', 4)
        self.ins('move.w', '0xefc6:w,%d0', 4); self.ins('adda.w', '(%a3,%d0.w),%a2', 4)
        self.ins('lea.l', '0xb200:w,%a0', 4); self.ins('move.w', '0xf702:w,%d0', 4)
        self.ins('lsl.w', '#1,%d0'); self.ins('tst.w', '(%a0,%d0.w)', 4)
        other, arrivals = self.fresh('other_side'), self.fresh('arrivals')
        self.branch('bne', other); self.ins('move.w', '0xf702:w,%d0', 4)
        self.call('remove_defeated_packed_member'); self.ins('clr.l', '0xff382c:l', 6)
        self.label(other); self.ins('exg', '%a1,%a2'); self.ins('lea.l', '0xb200:w,%a0', 4)
        self.ins('move.w', '0xf706:w,%d0', 4); self.ins('lsl.w', '#1,%d0')
        self.ins('tst.w', '(%a0,%d0.w)', 4); self.branch('bne', arrivals)
        self.ins('move.w', '0xf706:w,%d0', 4); self.call('remove_defeated_packed_member')
        self.ins('move.l', '%a2,0xff382c:l', 6)
        self.label(arrivals); self.call('settle_group_at_city'); self.call('adjust_battle_losing_loyalty')

    def remove_defeated_packed_member(self):
        self.ins('movem.l', '%d1-%d4/%a0-%a2,-(%a7)', 4)
        self.ins('lea.l', '0xcc00:w,%a0', 4)
        self.immediate('move.b', self.slot('removed_assignment', 255), '(%a0,%d0.w)', 6)
        self.ins('clr.w', '%d3'); self.ins('move.b', '0xd(%a1),%d3', 4)
        self.ins('lea.l', '(%a1),%a0'); self.ins('move.b', '(%a1),%d1')
        self.immediate('andi.w', 15, '%d1'); self.immediate('cmpi.w', 1, '%d1')
        whole, find, shift, moved, copy, stop = [self.fresh(n) for n in ('whole','find','shift','moved','copy','stop')]
        references, corrected = self.fresh('references'), self.fresh('corrected')
        self.branch('beq', whole); self.ins('subq.b', '#1,(%a1)'); self.ins('clr.w', '%d2')
        self.immediate('move.w', 1, '%d5'); self.label(find)
        self.ins('cmp.b', '0xd(%a1,%d2.w),%d0', 4); self.branch('beq', shift)
        self.ins('addq.w', '#1,%d2'); self.branch('bra', find, True)
        self.label(shift); self.ins('addq.w', '#1,%d2'); self.ins('cmp.w', '%d2,%d1')
        self.branch('beq', moved); self.ins('move.b', '0xd(%a1,%d2.w),0xc(%a1,%d2.w)', 6)
        self.branch('bra', shift, True); self.label(moved)
        self.ins('lea.l', '0xd(%a1,%d1.w),%a2', 4); self.ins('lea.l', '0xc(%a1,%d1.w),%a1', 4)
        self.ins('clr.w', '%d4'); self.ins('move.b', '0xd(%a0),%d4', 4)
        self.label(copy); self.ins('move.b', '(%a2),%d1'); self.immediate('andi.w', 15, '%d1')
        self.branch('beq', stop); self.immediate('addi.w', 12, '%d1')
        loop = self.fresh('copy_record'); self.label(loop); self.ins('move.b', '(%a2)+,(%a1)+')
        self.ins('dbra', '%d1,'+loop, 4); self.branch('bra', copy, True)
        self.label(stop); self.ins('clr.b', '(%a1)'); self.branch('bra', references)
        self.label(whole); self.immediate('move.w', 65535, '%d4'); self.immediate('move.w', 14, '%d5')
        self.ins('lea.l', '0xd(%a1,%d1.w),%a2', 4); self.branch('bra', copy, True)
        self.label(references); self.call('replace_or_remove_group_references')
        self.ins('movem.l', '(%a7)+,%d1-%d4/%a0-%a2', 4)
        self.ins('exg', '%d1,%a1'); self.ins('exg', '%d2,%a2'); self.ins('cmp.l', '%d1,%d2')
        self.branch('bcs', corrected); self.immediate('andi.l', 65535, '%d5', 6); self.ins('sub.l', '%d5,%d2')
        self.label(corrected); self.ins('exg', '%d1,%a1'); self.ins('exg', '%d2,%a2')

    def replace_or_remove_group_references(self):
        done, find, remove, records, skip, found, shift = [self.fresh(n) for n in ('done','find','remove','records','skip','found','shift')]
        self.ins('cmp.w', '%d3,%d4'); self.branch('beq', done)
        self.ins('lea.l', '0xff39b2:l,%a0', 6); self.ins('adda.w', '0xff3bb2:l,%a0', 6)
        self.label(find); self.ins('tst.b', '(%a0)+'); self.branch('beq', done)
        self.ins('cmp.b', '(%a0)+,%d3'); self.branch('bne', find, True)
        self.ins('tst.w', '%d4'); self.branch('bmi', remove)
        self.ins('move.b', '%d4,-1(%a0)', 4); self.ins('lea.l', '0xff3000:l,%a0', 6)
        self.label(records); self.ins('tst.b', '(%a0)+'); self.branch('bmi', done)
        self.ins('cmp.b', '(%a0)+,%d3'); self.branch('beq', found)
        self.label(skip); self.ins('tst.b', '(%a0)+'); self.branch('bne', skip, True)
        self.branch('bra', records, True); self.label(found); self.ins('move.b', '%d4,-1(%a0)', 4)
        self.branch('bra', done); self.label(remove); self.ins('lea.l', '-2(%a0),%a1', 4)
        self.label(shift); self.ins('move.b', '(%a0)+,(%a1)+'); self.branch('beq', done)
        self.ins('move.b', '(%a0)+,(%a1)+'); self.branch('bra', shift, True); self.label(done)

    def transfer_outcome_officer(self):
        done, winner, load, detach, write = [self.fresh(n) for n in ('done','winner','load','detach','write')]
        self.immediate('cmpi.w', self.slot('transfer_outcome', 6), '0xffff8114:l', 8)
        self.branch('bcs', done); self.branch('beq', winner)
        self.ins('move.w', '0xffff80e2:l,%d0', 6); self.branch('bra', load)
        self.label(winner); self.ins('move.w', '0xffff80e0:l,%d0', 6); self.label(load)
        self.ins('movea.l', '0xff382c:l,%a0', 6); self.ins('lea.l', '0x9000:w,%a1', 4)
        self.ins('lea.l', '0xefbe:w,%a2', 4); self.ins('move.w', '0xefc6:w,%d1', 4)
        self.ins('adda.w', '(%a2,%d1.w),%a1', 4); self.ins('cmp.w', '0xf702:w,%d0', 4)
        self.branch('beq', detach); self.ins('exg', '%a0,%a1'); self.label(detach)
        self.ins('move.w', '%d0,-(%a7)'); self.call('detach_member_keep_group_cursor')
        self.call('attach_member_shift_packet'); self.ins('move.w', '(%a7)+,%d0')
        self.ins('cmp.w', '0xf702:w,%d0', 4); self.branch('beq', write)
        self.ins('exg', '%a0,%a1'); self.label(write); self.ins('move.l', '%a0,0xff382c:l', 6)
        self.ins('exg', '%d1,%a1'); self.immediate('subi.l', 0xFFFF9000, '%d1', 6)
        self.ins('lea.l', '0xefbe:w,%a2', 4); self.ins('move.w', '0xefc6:w,%d0', 4)
        self.ins('move.w', '%d1,(%a2,%d0.w)', 4); self.label(done)

    def detach_member_keep_group_cursor(self):
        self.ins('move.w', '%d3,-(%a7)'); self.ins('movem.l', '%d1-%d2/%a0-%a2,-(%a7)', 4)
        self.ins('move.b', '(%a0),%d1'); self.immediate('andi.w', 15, '%d1')
        self.immediate('cmpi.w', 1, '%d1')
        whole, find, shift, moved, copy, stop, corrected = [self.fresh(n) for n in ('whole','find','shift','moved','copy','stop','corrected')]
        self.branch('beq', whole); self.immediate('move.w', 1, '%d3'); self.ins('clr.w', '%d2')
        self.label(find); self.ins('cmp.b', '0xd(%a0,%d2.w),%d0', 4); self.branch('beq', shift)
        self.ins('addq.w', '#1,%d2'); self.branch('bra', find, True)
        self.label(shift); self.ins('addq.w', '#1,%d2'); next_ = self.fresh('shift_next'); self.label(next_)
        self.ins('cmp.w', '%d1,%d2'); self.branch('beq', moved)
        self.ins('move.b', '0xd(%a0,%d2.w),0xc(%a0,%d2.w)', 6)
        self.ins('addq.w', '#1,%d2'); self.branch('bra', next_, True)
        self.label(moved); self.call('replace_group_head_reference'); self.ins('subq.b', '#1,(%a0)')
        self.ins('lea.l', '0xd(%a0,%d1.w),%a1', 4); self.ins('lea.l', '0xc(%a0,%d1.w),%a2', 4)
        self.branch('bra', copy); self.label(whole); self.immediate('move.w', 14, '%d3')
        self.call('remove_group_reference'); self.ins('lea.l', '0xd(%a0,%d1.w),%a1', 4)
        self.ins('movea.l', '%a0,%a2'); self.immediate('movea.l', 0, '%a0', 6)
        self.label(copy); self.ins('move.b', '(%a1),%d1'); self.immediate('andi.w', 15, '%d1')
        self.branch('beq', stop); self.immediate('addi.w', 12, '%d1')
        loop = self.fresh('copy_record'); self.label(loop); self.ins('move.b', '(%a1)+,(%a2)+')
        self.ins('dbra', '%d1,'+loop, 4); self.branch('bra', copy, True)
        self.label(stop); self.ins('clr.b', '(%a2)'); self.ins('movem.l', '(%a7)+,%d1-%d2/%a0-%a2', 4)
        self.ins('exg', '%d0,%a0'); self.ins('exg', '%d1,%a1'); self.ins('cmp.l', '%d0,%d1')
        self.branch('bcs', corrected); self.immediate('andi.l', 65535, '%d3', 6); self.ins('sub.l', '%d3,%d1')
        self.label(corrected); self.ins('exg', '%d0,%a0'); self.ins('exg', '%d1,%a1'); self.ins('move.w', '(%a7)+,%d3')

    def replace_group_head_reference(self):
        self.ins('move.w', '%d1,-(%a7)'); self.ins('move.b', '0xd(%a0),%d1', 4)
        self.immediate('andi.w', 255, '%d1'); self.ins('lea.l', '0xff39b2:l,%a1', 6)
        self.ins('adda.w', '0xff3bb2:l,%a1', 6)
        find, found, records, skip, write, done = [self.fresh(n) for n in ('find','found','records','skip','write','done')]
        self.label(find); self.ins('tst.b', '(%a1)'); self.branch('beq', done)
        self.ins('cmp.b', '1(%a1),%d0', 4); self.branch('beq', found)
        self.ins('addq.w', '#2,%a1'); self.branch('bra', find, True)
        self.label(found); self.ins('move.b', '%d1,1(%a1)', 4); self.ins('lea.l', '0xff3000:l,%a1', 6)
        self.label(records); self.ins('cmp.b', '1(%a1),%d0', 4); self.branch('beq', write)
        self.ins('addq.w', '#1,%a1'); self.label(skip); self.ins('tst.b', '(%a1)+')
        self.branch('bne', skip, True); self.branch('bra', records, True)
        self.label(write); self.ins('move.b', '%d1,1(%a1)', 4); self.label(done); self.ins('move.w', '(%a7)+,%d1')

    def remove_group_reference(self):
        self.ins('lea.l', '0xff39b2:l,%a1', 6); self.ins('adda.w', '0xff3bb2:l,%a1', 6)
        find, found, shift, done = [self.fresh(n) for n in ('find','found','shift','done')]
        self.label(find); self.ins('tst.b', '(%a1)'); self.branch('beq', done)
        self.ins('cmp.b', '1(%a1),%d0', 4); self.branch('beq', found)
        self.ins('adda.w', '#2,%a1', 4); self.branch('bra', find, True)
        self.label(found); self.ins('lea.l', '2(%a1),%a2', 4); self.label(shift)
        self.ins('move.b', '(%a2)+,(%a1)+'); self.branch('beq', done)
        self.ins('move.b', '(%a2)+,(%a1)+'); self.branch('bra', shift, True); self.label(done)

    def attach_member_shift_packet(self):
        self.ins('move.l', '%a2,-(%a7)'); self.ins('move.b', '(%a1),%d1')
        self.immediate('andi.w', 15, '%d1'); self.immediate('cmpi.w', self.slot('capacity_comparison', 10), '%d1')
        full, carry, finish_tail, fallback_else, adjust, corrected = [self.fresh(n) for n in ('full','carry','finish_tail','fallback_else','adjust','corrected')]
        self.branch('beq', full); self.ins('lea.l', '0xd(%a1,%d1.w),%a2', 4)
        self.ins('lea.l', '0xe(%a1,%d1.w),%a3', 4); self.ins('move.b', '(%a2),%d1')
        self.label(carry); self.ins('move.b', '%d1,%d2'); self.immediate('andi.w', 15, '%d2')
        self.branch('beq', finish_tail); self.immediate('addi.w', 12, '%d2')
        loop = self.fresh('shift_record'); self.label(loop); self.ins('move.b', '(%a3),%d3')
        self.ins('move.b', '%d1,(%a3)+'); self.ins('move.b', '%d3,%d1')
        self.ins('dbra', '%d2,'+loop, 4); self.branch('bra', carry, True)
        self.label(finish_tail); self.ins('clr.b', '(%a3)'); self.ins('move.b', '(%a1),%d1')
        self.immediate('andi.w', 15, '%d1'); self.ins('addq.b', '#1,(%a1)')
        self.ins('move.b', '%d0,0xd(%a1,%d1.w)', 4); self.ins('lea.l', '0xcc00:w,%a2', 4)
        self.ins('clr.w', '%d3'); self.ins('move.b', '4(%a1),%d3', 4)
        self.immediate('addi.w', 41, '%d3'); self.ins('move.b', '%d3,(%a2,%d0.w)', 4)
        self.immediate('move.w', 1, '%d3'); self.branch('bra', adjust)
        self.label(full); self.ins('clr.w', '%d3'); self.ins('lea.l', '0xcc00:w,%a2', 4)
        self.ins('move.b', '(%a2,%d0.w),%d1', 4); self.immediate('andi.w', 63, '%d1')
        self.immediate('cmpi.w', 40, '%d1'); self.branch('bhi', fallback_else)
        self.ins('bset.l', '#7,%d1', 4); self.ins('move.b', '%d1,(%a2,%d1.w)', 4)
        self.branch('bra', adjust); self.label(fallback_else); self.immediate('subi.w', 40, '%d1')
        self.ins('bset.l', '#7,%d1', 4); self.ins('move.b', '%d1,(%a2,%d0.w)', 4)
        self.label(adjust); self.ins('exg', '%d0,%a0'); self.ins('exg', '%d1,%a1')
        self.ins('cmp.l', '%d1,%d0'); self.branch('bcs', corrected)
        self.immediate('andi.l', 65535, '%d3', 6); self.ins('add.l', '%d3,%d0')
        self.label(corrected); self.ins('exg', '%d0,%a0'); self.ins('exg', '%d1,%a1'); self.ins('movea.l', '(%a7)+,%a2')

    def finish(self):
        self.e.end()
        width = sum(row['encoding_bytes'] for row in self.e.mapping)
        if width != self.e.binding.end-self.e.binding.entry:
            raise CompileError(self.e.binding.name+': semantic lowering extent mismatch')
        return self.e.unit(dict(**self.effects, original_generation_input=False,
                               stack_and_full_registers_owned_by_backend=True, complete_CPU=False))


def compile_members(source):
    effects = parse(source)
    units = []
    for binding in MEMBERS_BINDINGS:
        lowerer = Lowerer(binding, effects[binding.name])
        getattr(lowerer, binding.name)()
        units.append(lowerer.finish())
    allocated = sum(sum(row['encoding_bytes'] for row in unit['instructions']) for unit in units)
    count = sum(len(unit['instructions']) for unit in units)
    if (allocated, count) != (896, 265):
        raise CompileError('complete eight member bodies/896 bytes/265 instructions required')
    return dict(units=units, assembly='.cpu 68000\n.text\n'+'\n'.join(unit['assembly'] for unit in units),
                effects=effects, allocated_bytes=allocated, instructions=count,
                original_generation_input=False, complete_CPU=False)
