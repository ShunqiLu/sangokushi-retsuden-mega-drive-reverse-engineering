"""Finite typed business-flow admission and ordinary ABI instruction lowering.

Every function body, import use, expression, control node and return is
consumed. Supported semantic literal roles drive instruction selection; other
valid-Python modifications fail closed. No file/ROM/assembly/IR input occurs.
"""
import ast
from .compiler_common import CompileError,Emitter,require_declared_names
from .target import DISPOSITION_BINDINGS,BY_NAME,TABLE_BINDINGS,SCALAR_BINDINGS

# Typed executable semantic declarations, not target instructions or encodings.
DECLARATIONS={
  "collect_city_attached_officers": {
    "signature": "state: GameState",
    "returns": "Word",
    "flow": "output = state.candidate_roster.cursor()\ncity = state.city()\ncount = 0\nfor officer in descending_inclusive(255):\n    if state.officer_assignments.byte(officer) == low8(city):\n        output.append_word(officer)\n        count = u16(count + 1)\noutput.set_word(0, 65535)\nreturn count"
  },
  "collect_unassigned_city_officers": {
    "signature": "state: GameState",
    "returns": "Word",
    "flow": "output = state.candidate_roster.cursor()\ncity = state.city()\ncount = 0\nfor officer in descending_inclusive(255):\n    if state.alternate_assignments.byte(officer) == low8(city):\n        if not negative_byte(state.officer_assignments.byte(officer)):\n            output.append_word(officer)\n            count = u16(count + 1)\noutput.set_word(0, 65535)\nreturn count"
  },
  "rebuild_primary_after_battle": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "collect_city_attached_officers(state)\npartition_city_survivors(state)\nincoming = collect_unassigned_city_officers(state)\ntotal = u16(incoming + state.remaining_count())\nif total > 10:\n    sort_returning_officer_status(state, u16(total - 10))\nroster = state.survivor_roster.cursor()\nwhile True:\n    officer = roster.word()\n    if negative_word(officer):\n        break\n    roster.append_word(u16(officer | 16384))\nif not negative_word(state.survivor_roster.word()):\n    state.set_working_owner(state.secondary_owner_byte())\n    outcome = owner_has_other_city_carry(state)\n    if outcome.carry == 0:\n        state.set_resource_side(2)\n        packet = append_group_from_survivor_roster(state)\n        allocate_packed_group_resources(state, packet)\n    else:\n        city = u16(state.city() | 128)\n        roster = state.survivor_roster.cursor()\n        while True:\n            officer = roster.next_word()\n            if negative_word(officer):\n                break\n            officer = u16(officer & 255)\n            state.officer_assignments.set_byte(officer, low8(city))\nforce = u16(state.primary_force() << 1)\nstate.set_loyalty_source(state.force_heads.word(force))\nrestore_returning_officer_assignments(state)"
  },
  "sort_returning_officer_status": {
    "signature": "state: GameState, surplus: Word",
    "returns": "Word",
    "flow": "surplus = u16(surplus)\nstate.set_returning_count(u16(state.returning_count() + surplus))\nroster = state.remaining_roster.cursor()\ncandidates = state.candidate_roster\nstatuses = state.status_roster\ncandidates.set_word(0, 65535)\nretained_status = 0\nwhile True:\n    offset = 0\n    officer = roster.next_word()\n    if negative_word(officer):\n        break\n    retained_status = u16(replace_byte(retained_status, state.status.byte(officer)))\n    while not negative_word(candidates.word(offset)):\n        if low8(retained_status) > statuses.byte(offset, 1):\n            break\n        offset = u16(offset + 2)\n    while True:\n        displaced = candidates.word(offset)\n        candidates.set_word(offset, officer)\n        if negative_word(officer):\n            break\n        displaced_status = statuses.word(offset)\n        statuses.set_word(offset, retained_status)\n        offset = u16(offset + 2)\n        officer = displaced\n        retained_status = displaced_status\nreturning = state.survivor_roster.cursor()\nwhile not negative_word(returning.next_word()):\n    pass\nreturning = returning.advance(-2)\nsource = candidates.cursor()\nfor member in descending_inclusive(u16(surplus - 1)):\n    returning.append_word(source.next_word())\nreturning.set_word(0, 65535)\nremaining = state.remaining_roster.cursor()\ncount = 0\nwhile True:\n    officer = source.next_word()\n    remaining.append_word(officer)\n    if negative_word(officer):\n        break\n    count = u16(count + 1)\nstate.set_remaining_count(count)\nreturn count"
  },
  "partition_city_survivors": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "first = state.candidate_roster.word()\ncity = u16(state.officer_assignments.byte(first) & 63)\nowner = state.city_owners.byte(city)\nstate.set_working_owner(owner)\nruler = state.force_heads.word(u16(owner << 1))\nroster = state.candidate_roster.cursor()\nremaining = state.remaining_roster.cursor()\nreturning = state.survivor_roster.cursor()\nreturn_count = 0\nkeep_count = 0\nwhile True:\n    officer = roster.next_word()\n    if negative_word(officer):\n        break\n    if officer == ruler:\n        outcome = owner_has_other_city_carry(state)\n        if outcome.carry == 0:\n            returning.append_word(officer)\n            return_count = u16(return_count + 1)\n        else:\n            state.officer_assignments.set_byte(officer, 255)\n        continue\n    strength_index = u16(officer << 2)\n    if state.troop_strengths.long(strength_index) > 500:\n        if state.troop_strengths.long(strength_index) > 1000:\n            remaining.append_word(officer)\n            keep_count = u16(keep_count + 1)\n            continue\n        resource_index = u16(strength_index >> 1)\n        if state.officer_resources.word(resource_index) > 30:\n            remaining.append_word(officer)\n            keep_count = u16(keep_count + 1)\n            continue\n    sample = u16(state.sample_random() & 3)\n    if sample == 0:\n        returning.append_word(officer)\n        return_count = u16(return_count + 1)\n    else:\n        remaining.append_word(officer)\n        keep_count = u16(keep_count + 1)\nremaining.set_word(0, 65535)\nreturning.set_word(0, 65535)\nstate.set_returning_count(return_count)\nstate.set_remaining_count(keep_count)"
  },
  "owner_has_other_city_carry": {
    "signature": "state: GameState",
    "returns": "CarryOutcome",
    "flow": "city = u16(state.city() - 1)\nowner = state.working_owner()\nfor candidate in descending_inclusive(39):\n    if state.other_city_owners.byte(candidate) == owner:\n        if candidate != city:\n            return state.carry_result(0)\nreturn state.carry_result(1)"
  },
  "restore_returning_officer_assignments": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "roster = state.remaining_roster.cursor()\ncity = state.city()\nwhile True:\n    officer = roster.next_word()\n    if negative_word(officer):\n        return None\n    state.officer_assignments.set_byte(officer, low8(city))\n    state.set_selected_officer(officer)\n    apply_returning_officer_loyalty(state)"
  },
  "allocate_packed_group_resources": {
    "signature": "state: GameState, packet: Table",
    "returns": "None",
    "flow": "packet = state.checked_table(packet)\nmembers = u16(packet.byte() - 1)\ntotal = 0\nfor member in descending_inclusive(members):\n    officer = packet.byte(member, 13)\n    index = u16(officer << 2)\n    total = u32(total + state.troop_strengths.long(index))\n    total = u32(total + 100)\nmultiplied = u32(u32(total << 1) + total)\ngold_cost = u32(divu_retained(multiplied, 5) & 65535)\nrice_cost = gold_cost\ngold = state.city_ed84\nrice = state.city_ee24\nif state.side_flags() & 2 != 0:\n    gold = state.city_gold\n    rice = state.city_rice\ncity = u16(state.city() << 2)\navailable = gold.long(city)\nif available < gold_cost:\n    gold_cost = available\ngold.set_long(city, u32(available - gold_cost))\navailable = rice.long(city)\nif available < rice_cost:\n    rice_cost = available\nrice.set_long(city, u32(available - rice_cost))\npacket.set_byte(8, low8(gold_cost))\ngold_cost = u32(gold_cost >> 8)\npacket.set_byte(7, low8(gold_cost))\ngold_cost = u32(gold_cost >> 8)\npacket.set_byte(6, low8(gold_cost))\ngold_cost = u32(gold_cost & 4294901760 | u16(gold_cost << 8))\npacket.set_byte(5, low8(gold_cost))\npacket.set_byte(12, low8(rice_cost))\nrice_cost = u32(rice_cost >> 8)\npacket.set_byte(11, low8(rice_cost))\nrice_cost = u32(rice_cost >> 8)\npacket.set_byte(10, low8(rice_cost))\nrice_cost = u32(rice_cost & 4294901760 | u16(low16(rice_cost) >> 8))\npacket.set_byte(9, low8(rice_cost))"
  },
  "rebuild_secondary_after_battle": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "collect_unassigned_city_officers(state)\npartition_city_survivors(state)\nincoming = collect_city_attached_officers(state)\ntotal = u16(incoming + state.remaining_count())\nif total > 10:\n    sort_returning_officer_status(state, u16(total - 10))\nroster = state.survivor_roster.cursor()\nwhile True:\n    officer = roster.word()\n    if negative_word(officer):\n        break\n    roster.append_word(u16(officer | 16384))\nif not negative_word(state.survivor_roster.word()):\n    state.set_working_owner(state.primary_owner_byte())\n    outcome = owner_has_other_city_carry(state)\n    if outcome.carry == 0:\n        state.set_resource_side(0)\n        packet = append_group_from_survivor_roster(state)\n        allocate_packed_group_resources(state, packet)\n    else:\n        city = u16(state.city() | 128)\n        roster = state.survivor_roster.cursor()\n        while True:\n            officer = roster.next_word()\n            if negative_word(officer):\n                break\n            officer = u16(officer & 255)\n            state.officer_assignments.set_byte(officer, low8(city))\nforce = u16(state.secondary_force() << 1)\nstate.set_loyalty_source(state.force_heads.word(force))\nrestore_returning_officer_assignments(state)"
  }
}
APPROVED_DOMAIN={'GameState','Table','Word','CarryOutcome','u8','u16','u32','low8','low16',
                 'replace_byte','negative_byte','negative_word','descending_inclusive','divu_retained'}
APPROVED_ARRIVAL={'append_group_from_survivor_roster','apply_returning_officer_loyalty'}
SLOT_VALUES={
    'collect_city_attached_officers':{255:('officer_latch',0,65535)},
    'collect_unassigned_city_officers':{255:('officer_latch',0,65535)},
    'rebuild_primary_after_battle':{10:('retained_limit',0,65535)},
    'rebuild_secondary_after_battle':{10:('retained_limit',0,65535)},
    'partition_city_survivors':{500:('low_strength',0,0xFFFFFFFF),1000:('high_strength',0,0xFFFFFFFF),
                              30:('resource_threshold',0,65535),3:('random_mask',0,65535)},
    'owner_has_other_city_carry':{39:('city_latch',0,65535)},
    'allocate_packed_group_resources':{100:('member_allowance',0,0xFFFFFFFF),5:('resource_divisor',1,65535)},
}


def parse(source):
    if type(source) is not str: raise CompileError('explicit disposition semantic text required')
    try: tree=ast.parse(source)
    except (SyntaxError,ValueError) as exc: raise CompileError('invalid disposition Python source') from exc
    functions={};imported=set()
    for node in tree.body:
        if isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and type(node.value.value) is str: continue
        if isinstance(node,ast.ImportFrom):
            approved=APPROVED_DOMAIN if node.module=='domain' else APPROVED_ARRIVAL if node.module=='business_arrival' else set()
            if node.level!=1 or any(n.asname or n.name not in approved for n in node.names):
                raise CompileError('approved explicit domain/arrival imports required')
            imported.update(n.name for n in node.names);continue
        if not isinstance(node,ast.FunctionDef) or node.name not in DECLARATIONS or node.name in functions:
            raise CompileError('only9 declared complete disposition functions admitted')
        if node.type_params or node.decorator_list: raise CompileError('generic/decorated ABI not admitted')
        functions[node.name]=node
    if set(functions)!=set(DECLARATIONS): raise CompileError('all9 disposition functions required')
    require_declared_names(functions,imported)
    result={}
    for name,fn in functions.items():
        declaration=DECLARATIONS[name]
        text='def '+name+'('+declaration['signature']+')->'+declaration['returns']+':\n'
        text+='\n'.join('    '+line for line in declaration['flow'].splitlines())
        expected=ast.parse(text).body[0]
        body=list(fn.body)
        if body and isinstance(body[0],ast.Expr) and isinstance(body[0].value,ast.Constant) and type(body[0].value.value) is str: body=body[1:]
        actual=ast.FunctionDef(name=fn.name,args=fn.args,body=body,decorator_list=fn.decorator_list,
                              returns=fn.returns,type_comment=fn.type_comment,type_params=fn.type_params)
        slots={}
        def compare(want,have,parent=None):
            if type(want) is not type(have): raise CompileError(name+': unsupported semantic structure')
            if isinstance(want,ast.Constant):
                if type(want.value) is not type(have.value): raise CompileError(name+': strict semantic literal type')
                spec=SLOT_VALUES.get(name,{}).get(want.value) if type(want.value) is int else None
                if name=='allocate_packed_group_resources' and want.value==5:
                    if not (isinstance(parent,ast.Call) and isinstance(parent.func,ast.Name)
                            and parent.func.id=='divu_retained' and len(parent.args)==2 and parent.args[1] is want):
                        spec=None
                if spec:
                    role,first,last=spec
                    if type(have.value) is not int or not first<=have.value<=last: raise CompileError(name+': typed '+role+' outside admitted width')
                    if role in slots and slots[role]!=have.value: raise CompileError(name+': related literal role must remain consistent')
                    slots[role]=have.value;return
                if want.value!=have.value: raise CompileError(name+': unsupported literal edit')
            elif isinstance(want,ast.AST):
                for key,value in ast.iter_fields(want): compare(value,getattr(have,key),want)
            elif type(want) is list:
                if len(want)!=len(have): raise CompileError(name+': all effect/control/return nodes required')
                for a,b in zip(want,have): compare(a,b,parent)
            elif want!=have: raise CompileError(name+': unsupported name/type/operator edit')
        compare(expected,actual)
        result[name]=dict(slots=slots,args=declaration['signature'],returns=declaration['returns'])
    return result


def _absolute(binding):
    address=binding['address'];suffix=binding['suffix']
    return f'0x{address&65535 if suffix=="w" else address:x}:{suffix}'


class Lowerer:
    def __init__(self,name,effects):
        self.name,self.effects=name,effects
        self.e=Emitter(BY_NAME[name]);self.e.begin();self.slots=effects['slots']
    def slot(self,name,default): return self.slots.get(name,default)
    def ins(self,op,args='',width=2): self.e.ins(op,args,width)
    def lea(self,role,reg):
        binding=TABLE_BINDINGS[role];self.ins('lea.l',f'{_absolute(binding)},%a{reg}',4 if binding['suffix']=='w' else 6)
    def scalar(self,role,reg):
        binding=SCALAR_BINDINGS[role]
        self.ins('move.'+{8:'b',16:'w',32:'l'}[binding['width']],f'{_absolute(binding)},%d{reg}',4 if binding['suffix']=='w' else 6)
    def immediate(self,op,value,destination,width=4): self.ins(op,f'#0x{value:x},{destination}',width)
    def branch(self,op,label,short=False): self.ins(op+('.b' if short else '.w'),label,2 if short else 4)
    def call(self,name,absolute=False):
        self.ins('jsr' if absolute else 'bsr.w',name+':l' if absolute else name,6 if absolute else 4)
    def finish(self):
        self.e.end()
        if sum(i['encoding_bytes'] for i in self.e.mapping)!=self.e.binding.end-self.e.binding.entry:
            raise CompileError(self.name+': complete lowered extent mismatch')
        return self.e.unit(dict(semantic_slots=self.slots,typed_parameters=self.effects['args'],typed_return=self.effects['returns'],
                                complete_flow_consumed=True,host_stack_and_full_CPU=False))

    def collect_city_attached_officers(self):
        self.lea('officer_assignments',0);self.lea('candidate_roster',1)
        self.immediate('move.w',self.slot('officer_latch',255),'%d1');self.scalar('city',2);self.ins('clr.w','%d3')
        loop,next_=self.e.fresh('city_scan'),self.e.fresh('next_officer');self.e.label(loop)
        self.ins('cmp.b','(%a0,%d1.w),%d2',4);self.branch('bne',next_)
        self.ins('move.w','%d1,(%a1)+');self.ins('addq.w','#1,%d3');self.e.label(next_)
        self.ins('dbra','%d1,'+loop,4);self.immediate('move.w',65535,'(%a1)')

    def collect_unassigned_city_officers(self):
        self.lea('alternate_assignments',0);self.lea('candidate_roster',1);self.lea('officer_assignments',2)
        self.scalar('city',0);self.immediate('move.w',self.slot('officer_latch',255),'%d2');self.ins('clr.w','%d3')
        loop,next_=self.e.fresh('alternate_scan'),self.e.fresh('next_officer');self.e.label(loop)
        self.ins('cmp.b','(%a0,%d2.w),%d0',4);self.branch('bne',next_)
        self.ins('tst.b','(%a2,%d2.w)',4);self.branch('bmi',next_)
        self.ins('move.w','%d2,(%a1)+');self.ins('addq.w','#1,%d3');self.e.label(next_)
        self.ins('dbra','%d2,'+loop,4);self.immediate('move.w',65535,'(%a1)')

    def rebuild(self,primary):
        first='collect_city_attached_officers' if primary else 'collect_unassigned_city_officers'
        second='collect_unassigned_city_officers' if primary else 'collect_city_attached_officers'
        self.call(first);self.call('partition_city_survivors');self.call(second)
        self.ins('move.w','%d3,%d0');self.ins('add.w',_absolute(SCALAR_BINDINGS['remaining_count'])+',%d0',4)
        self.immediate('subi.w',self.slot('retained_limit',10),'%d0')
        mark,marked,assign,finish,assign_loop,assign_done=[self.e.fresh(n) for n in ('mark_roster','marked_roster','assign_local','finish','assign_loop','assign_done')]
        self.branch('bls',mark);self.call('sort_returning_officer_status');self.e.label(mark)
        self.lea('survivor_roster',0);mark_loop=self.e.fresh('mark_loop');self.e.label(mark_loop)
        self.ins('move.w','(%a0),%d0');self.branch('bmi',marked)
        self.ins('bset.l','#14,%d0',4);self.ins('move.w','%d0,(%a0)+');self.branch('bra',mark_loop,True)
        self.e.label(marked);self.ins('tst.w',_absolute(TABLE_BINDINGS['survivor_roster']),4);self.branch('bmi',finish)
        owner='secondary_owner_byte' if primary else 'primary_owner_byte'
        self.ins('move.b',_absolute(SCALAR_BINDINGS[owner])+','+_absolute(SCALAR_BINDINGS['working_owner']),6)
        self.call('owner_has_other_city_carry');self.branch('bcs',assign)
        if primary:self.immediate('move.w',2,_absolute(SCALAR_BINDINGS['resource_side']),6)
        else:self.ins('clr.w',_absolute(SCALAR_BINDINGS['resource_side']),4)
        self.call('append_group_from_survivor_roster',True);self.call('allocate_packed_group_resources');self.branch('bra',finish)
        self.e.label(assign)
        if not primary: self.lea('survivor_roster',0)
        self.scalar('city',0);self.ins('bset.l','#7,%d0',4)
        if primary: self.lea('survivor_roster',0)
        self.lea('officer_assignments',1);self.e.label(assign_loop)
        self.ins('move.w','(%a0)+,%d1');self.branch('bmi',assign_done);self.immediate('andi.w',255,'%d1')
        self.ins('move.b','%d0,(%a1,%d1.w)',4);self.branch('bra',assign_loop,True);self.e.label(assign_done)
        self.e.label(finish);self.lea('force_heads',0);self.scalar('primary_force' if primary else 'secondary_force',0)
        self.ins('lsl.w','#1,%d0');self.ins('move.w','(%a0,%d0.w),'+_absolute(SCALAR_BINDINGS['loyalty_source']),6)
        self.call('restore_returning_officer_assignments')
    def rebuild_primary_after_battle(self): self.rebuild(True)
    def rebuild_secondary_after_battle(self): self.rebuild(False)

    def sort_returning_officer_status(self):
        self.ins('add.w','%d0,'+_absolute(SCALAR_BINDINGS['returning_count']),4)
        self.lea('remaining_roster',0);self.lea('status',3);self.lea('candidate_roster',1);self.lea('status_roster',2)
        self.immediate('move.w',65535,_absolute(TABLE_BINDINGS['candidate_roster']),6);self.ins('clr.w','%d2')
        outer,search,insert,finish,terminator,copy,rest=[self.e.fresh(n) for n in ('read_remaining','find_position','insert_shift','sorted','returning_tail','copy_returning','copy_remaining')]
        self.e.label(outer);self.ins('clr.w','%d3');self.ins('move.w','(%a0)+,%d1');self.branch('bmi',finish)
        self.ins('move.b','(%a3,%d1.w),%d2',4);self.e.label(search)
        self.ins('tst.w','(%a1,%d3.w)',4);self.branch('bmi',insert)
        self.ins('cmp.b','1(%a2,%d3.w),%d2',4);self.branch('bhi',insert)
        self.ins('addq.w','#2,%d3');self.branch('bra',search,True);self.e.label(insert)
        self.ins('move.w','(%a1,%d3.w),%d4',4);self.ins('move.w','%d1,(%a1,%d3.w)',4);self.branch('bmi',outer,True)
        self.ins('move.w','(%a2,%d3.w),%d5',4);self.ins('move.w','%d2,(%a2,%d3.w)',4)
        self.ins('addq.w','#2,%d3');self.ins('move.w','%d4,%d1');self.ins('move.w','%d5,%d2');self.branch('bra',insert,True)
        self.e.label(finish);self.lea('survivor_roster',0);self.e.label(terminator)
        self.ins('tst.w','(%a0)+');self.branch('bpl',terminator,True);self.ins('subq.w','#2,%a0')
        self.ins('subq.w','#1,%d0');self.lea('candidate_roster',1);self.e.label(copy)
        self.ins('move.w','(%a1)+,(%a0)+');self.ins('dbra','%d0,'+copy,4);self.immediate('move.w',65535,'(%a0)')
        self.lea('remaining_roster',0);self.ins('clr.w','%d1');self.e.label(rest)
        self.ins('move.w','(%a1)+,(%a0)+');done=self.e.fresh('remaining_end');self.branch('bmi',done)
        self.ins('addq.w','#1,%d1');self.branch('bra',rest,True);self.e.label(done)
        self.ins('move.w','%d1,'+_absolute(SCALAR_BINDINGS['remaining_count']),4)

    def partition_city_survivors(self):
        self.lea('officer_assignments',0);self.lea('city_owners',1);self.lea('force_heads',2)
        self.ins('move.w',_absolute(TABLE_BINDINGS['candidate_roster'])+',%d0',4);self.ins('clr.w','%d1')
        self.ins('move.b','(%a0,%d0.w),%d1',4);self.immediate('andi.w',63,'%d1');self.ins('clr.w','%d0')
        self.ins('move.b','(%a1,%d1.w),%d0',4);self.ins('move.b','%d0,'+_absolute(SCALAR_BINDINGS['working_owner']),4)
        self.ins('lsl.w','#1,%d0');self.ins('move.w','(%a2,%d0.w),%d7',4)
        for role,reg in (('candidate_roster',0),('troop_strengths',1),('officer_resources',2),('remaining_roster',3),('survivor_roster',4),('officer_assignments',5)):self.lea(role,reg)
        self.ins('clr.w','%d2');self.ins('clr.w','%d3')
        loop,finish,keep,small,returned,discard=[self.e.fresh(n) for n in ('partition','finish','keep','small','returned','discard')]
        self.e.label(loop);self.ins('move.w','(%a0)+,%d6');self.branch('bmi',finish)
        self.ins('cmp.w','%d7,%d6');self.branch('beq',small);self.ins('move.w','%d6,%d4');self.ins('lsl.w','#2,%d4')
        sample=self.e.fresh('sample_loss')
        self.immediate('cmpi.l',self.slot('low_strength',500),'(%a1,%d4.w)',8);self.branch('bls',sample)
        self.immediate('cmpi.l',self.slot('high_strength',1000),'(%a1,%d4.w)',8);self.branch('bhi',keep)
        self.ins('lsr.w','#1,%d4');self.immediate('cmpi.w',self.slot('resource_threshold',30),'(%a2,%d4.w)',6);self.branch('bhi',keep)
        self.e.label(sample);self.call('random_sample',True);self.immediate('andi.w',self.slot('random_mask',3),'%d0');self.branch('bne',keep)
        self.e.label(returned);self.ins('move.w','%d6,(%a4)+');self.ins('addq.w','#1,%d2');self.branch('bra',loop,True)
        self.e.label(small);self.call('owner_has_other_city_carry');self.branch('bcs',discard)
        self.ins('move.w','%d6,(%a4)+');self.ins('addq.w','#1,%d2');self.branch('bra',loop,True)
        self.e.label(discard);self.immediate('move.b',255,'(%a5,%d6.w)',6);self.branch('bra',loop,True)
        self.e.label(keep);self.ins('move.w','%d6,(%a3)+');self.ins('addq.w','#1,%d3');self.branch('bra',loop,True)
        self.e.label(finish);self.immediate('move.w',65535,'(%a3)');self.immediate('move.w',65535,'(%a4)')
        self.ins('move.w','%d2,'+_absolute(SCALAR_BINDINGS['returning_count']),4)
        self.ins('move.w','%d3,'+_absolute(SCALAR_BINDINGS['remaining_count']),4)

    def owner_has_other_city_carry(self):
        self.ins('movem.l','%d0-%d2/%a0,-(%a7)',4);self.lea('other_city_owners',0);self.scalar('city',0)
        self.ins('subq.w','#1,%d0');self.immediate('move.w',self.slot('city_latch',39),'%d1');self.scalar('working_owner',2)
        loop,next_,other,done=[self.e.fresh(n) for n in ('scan_other','next_city','has_other','carry_done')]
        self.e.label(loop);self.ins('cmp.b','(%a0,%d1.w),%d2',4);self.branch('bne',next_)
        self.ins('cmp.w','%d0,%d1');self.branch('bne',other);self.e.label(next_);self.ins('dbra','%d1,'+loop,4)
        self.ins('movem.l','(%a7)+,%d0-%d2/%a0',4);self.immediate('ori.w',1,'%sr');self.branch('bra',done)
        self.e.label(other);self.ins('movem.l','(%a7)+,%d0-%d2/%a0',4);self.immediate('andi.w',65534,'%sr');self.e.label(done)

    def restore_returning_officer_assignments(self):
        self.lea('remaining_roster',0);self.lea('officer_assignments',1);self.scalar('city',1)
        loop,done=self.e.fresh('restore_assignment'),self.e.fresh('restored');self.e.label(loop)
        self.ins('move.w','(%a0)+,%d0');self.branch('bmi',done);self.ins('move.b','%d1,(%a1,%d0.w)',4)
        self.ins('move.w','%d0,'+_absolute(SCALAR_BINDINGS['selected_officer']),4)
        self.call('apply_returning_officer_loyalty',True);self.branch('bra',loop,True);self.e.label(done)

    def allocate_packed_group_resources(self):
        self.lea('troop_strengths',1);self.ins('move.b','(%a0),%d0');self.immediate('andi.w',255,'%d0')
        self.ins('subq.w','#1,%d0');self.ins('moveq','#0,%d1');loop=self.e.fresh('sum_members');self.e.label(loop)
        self.ins('clr.w','%d2');self.ins('move.b','13(%a0,%d0.w),%d2',4);self.ins('lsl.w','#2,%d2')
        self.ins('add.l','(%a1,%d2.w),%d1',4);self.immediate('addi.l',self.slot('member_allowance',100),'%d1',6)
        self.ins('dbra','%d0,'+loop,4);self.ins('move.l','%d1,%d2');self.ins('lsl.l','#1,%d2');self.ins('add.l','%d1,%d2')
        self.immediate('divu.w',self.slot('resource_divisor',5),'%d2');self.immediate('andi.l',65535,'%d2',6);self.ins('move.l','%d2,%d3')
        self.lea('city_ed84',1);self.lea('city_ee24',2);self.ins('btst.b','#1,'+_absolute(SCALAR_BINDINGS['side_flags']),6)
        bank=self.e.fresh('bank_selected');self.branch('beq',bank);self.lea('city_gold',1);self.lea('city_rice',2);self.e.label(bank)
        self.scalar('city',0);self.ins('lsl.w','#2,%d0');self.ins('move.l','(%a1,%d0.w),%d1',4)
        gold=self.e.fresh('gold_cost');self.ins('cmp.l','%d2,%d1');self.branch('bcc',gold);self.ins('move.l','%d1,%d2');self.e.label(gold)
        self.ins('sub.l','%d2,%d1');self.ins('move.l','%d1,(%a1,%d0.w)',4);self.ins('move.l','(%a2,%d0.w),%d1',4)
        rice=self.e.fresh('rice_cost');self.ins('cmp.l','%d3,%d1');self.branch('bcc',rice);self.ins('move.l','%d1,%d3');self.e.label(rice)
        self.ins('sub.l','%d3,%d1');self.ins('move.l','%d1,(%a2,%d0.w)',4)
        self.ins('move.b','%d2,8(%a0)',4);self.ins('lsr.l','#8,%d2');self.ins('move.b','%d2,7(%a0)',4)
        self.ins('lsr.l','#8,%d2');self.ins('move.b','%d2,6(%a0)',4);self.ins('lsl.w','#8,%d2');self.ins('move.b','%d2,5(%a0)',4)
        self.ins('move.b','%d3,12(%a0)',4);self.ins('lsr.l','#8,%d3');self.ins('move.b','%d3,11(%a0)',4)
        self.ins('lsr.l','#8,%d3');self.ins('move.b','%d3,10(%a0)',4);self.ins('lsr.w','#8,%d3');self.ins('move.b','%d3,9(%a0)',4)


def compile_disposition(source):
    effects=parse(source);units=[]
    for binding in DISPOSITION_BINDINGS:
        lowerer=Lowerer(binding.name,effects[binding.name]);getattr(lowerer,binding.name)();units.append(lowerer.finish())
    allocated=sum(sum(i['encoding_bytes'] for i in u['instructions']) for u in units)
    instructions=sum(len(u['instructions']) for u in units)
    if (allocated,instructions)!=(966,279): raise CompileError('all9 disposition bodies/966B/279 instructions required')
    return dict(units=units,assembly='.cpu 68000\n.text\n'+'\n'.join(u['assembly'] for u in units),
                effects={u['binding']['name']:u['effects'] for u in units},allocated_bytes=allocated,
                instructions=instructions,original_generation_input=False,complete_CPU=False)
