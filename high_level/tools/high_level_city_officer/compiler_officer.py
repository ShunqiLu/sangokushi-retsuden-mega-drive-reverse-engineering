"""Typed officer flow admission and ordinary instruction selection.

The admitted structural subset is deliberately finite. Semantic constants enter
the lowerer as typed slots; unknown valid Python edits fail rather than becoming
ignored business logic. No ROM, assembly, IR or opcode input is read here.
"""
import ast
from .compiler_common import CompileError,Emitter,require_declared_names
from .target import OFFICER_BINDINGS,BY_NAME,TABLE_BINDINGS,SCALAR_BINDINGS


SIGNATURES={
 'scan_city_officers':('state:GameState, city:Word, output:Cursor, count:Word','Word'),
 'mark_c300_list':('state:GameState','None'),
 'replace_city_assignments':('state:GameState, replacement:Word','None'),
 'defense_progress':('state:GameState, officer:Word, gain:Word','None'),
 'battle_progress_award':('state:GameState, officer:Word, quantity:Long, progress:Table','Word'),
 'replenish_b200_troops':('state:GameState, retained_city:Word','Word'),
 'grow_original_long_field':('state:GameState, target:Table','Long'),
 'education_factor':('state:GameState, teacher:Word, target:Word','Word'),
 'recover_unacted_officer_b200':('state:GameState','None'),
 'add_progress_be':('state:GameState, gain:Word','None'),
 'split_progress':('state:GameState, gain:Long','Word'),
 'add_progress_c000':('state:GameState, officer:Word, gain:Word','None'),
 'owner_head_lookup':('state:GameState, city:Word','Word'),
 'clear_city_orders':('state:GameState','None'),
 'clear_monthly_actions':('state:GameState','None'),
 'terrain_cell_query':('state:GameState, row:Word, column:Word','tuple[Byte,Byte]'),
 'queue_development_order':('state:GameState','None'),
 'queue_welfare_order':('state:GameState','None'),
}
# Executable semantic flow declarations, not target instruction strings.
FLOWS={
'scan_city_officers':'''city=u16(city)
count=u16(count)
for officer in descending_inclusive(255):
    assignment=state.officer_assignments.byte(officer)
    if negative_byte(assignment):
        if assignment&127==city:
            output.append_word(officer)
            count=u16(count+1)
return count''',
'mark_c300_list':'''roster=state.action_roster.cursor()
while True:
    officer=roster.next_word()
    if negative_word(officer):
        return None
    if state.officer_status.byte(officer)>=40:
        live=state.officer_status.byte(officer)
        state.officer_status.set_byte(officer,u8(live|128))''',
'replace_city_assignments':'''replacement=u16(replacement)
replacement=u16(replacement+41)
selected=u8(state.selected_city()|64)
for officer in descending_inclusive(255):
    if state.officer_assignments.byte(officer)==selected:
        state.officer_assignments.set_byte(officer,low8(replacement))''',
'defense_progress':'''officer=u16(officer)
gain=u16(gain)
index=u16(officer<<1)
gain=u16(gain<<1)
updated=u16(state.progress_be.word(index)+gain)
if updated>999:
    updated=999
state.progress_be.set_word(index,updated)
updated=u16(state.progress_c.word(index)+gain)
if updated>999:
    updated=999
state.progress_c.set_word(index,updated)''',
'battle_progress_award':'''officer=u16(officer)
quantity=u32(quantity)
divided=divu_retained(low16(quantity),100)
index=u16(officer<<1)
updated=u16(progress.word(index)+low16(divided))
if updated>999:
    updated=999
progress.set_word(index,updated)
return updated''',
'replenish_b200_troops':'''retained_city=u16(retained_city)
for officer in descending_inclusive(255):
    retained_city=u16(replace_byte(retained_city,state.officer_assignments.byte(officer)))
    if retained_city>40:
        continue
    if state.city_processed.byte(retained_city)!=0:
        continue
    retained_city=u16(officer<<1)
    capacity=state.capacities_b000.word(retained_city)
    divided=divu_retained(u32(capacity*15),100)
    updated=u16(state.troops_b200.word(retained_city)+low16(divided))
    if updated>capacity:
        updated=capacity
    state.troops_b200.set_word(retained_city,updated)
return retained_city''',
'grow_original_long_field':'''previous=target.long()
divided=divu_retained(previous,100)
updated=u32(previous+low16(divided))
if updated>1000:
    updated=1000
target.set_long(0,updated)
return updated''',
'education_factor':'''teacher=u16(teacher)
target=u16(target)
index=0
if target>=20:
    index=5
    if target>=40:
        index=10
        if target>=60:
            index=15
            if target>=80:
                index=20
if teacher>=20:
    index=u16(index+1)
    if teacher>=40:
        index=u16(index+1)
        if teacher>=60:
            index=u16(index+1)
            if teacher>=80:
                index=u16(index+1)
return u16(s8(state.education_factors.byte(index)))''',
'recover_unacted_officer_b200':'''actor=low8(state.current_force())
for officer in descending_inclusive(255):
    city=state.officer_assignments.byte(officer)
    if city>40:
        continue
    if state.city_action_gates.byte(city)!=0:
        continue
    if state.city_owners.byte(city)!=actor:
        continue
    if state.officer_actions.byte(officer)!=0:
        continue
    index=u16(officer<<1)
    capacity=state.capacities_b000.word(index)
    divided=divu_retained(u32(capacity*15),100)
    updated=u16(state.troops_b200.word(index)+low16(divided))
    if updated>state.capacities_b000.word(index):
        updated=state.capacities_b000.word(index)
    state.troops_b200.set_word(index,updated)''',
'add_progress_be':'''gain=u16(gain)
index=u16(state.selected_officer()<<1)
previous=state.progress_be.word(index)
state.progress_be.set_word(index,u16(previous+gain))
if state.progress_be.word(index)>999:
    state.progress_be.set_word(index,999)''',
'split_progress':'''gain=u32(gain)
index=u16(state.selected_officer()<<1)
divided=divu_retained(low16(gain),10)
amount=low16(divided)
previous=state.progress_be.word(index)
state.progress_be.set_word(index,u16(previous+amount))
if state.progress_be.word(index)>999:
    state.progress_be.set_word(index,999)
amount=u16(amount>>1)
previous=state.progress_c.word(index)
state.progress_c.set_word(index,u16(previous+amount))
if state.progress_c.word(index)>999:
    state.progress_c.set_word(index,999)
return amount''',
'add_progress_c000':'''officer=u16(officer)
gain=u16(gain)
index=u16(officer<<1)
previous=state.progress_c.word(index)
state.progress_c.set_word(index,u16(previous+gain))
if state.progress_c.word(index)>999:
    state.progress_c.set_word(index,999)''',
'owner_head_lookup':'''city=u16(city)
owner=state.city_owners.byte(city)
index=u16(s8(owner)<<1)
head=state.force_heads.word(index)
state.set_scene(513)
return head''',
'clear_city_orders':'''city=state.selected_city()
index=u16((u16(city<<1)+city)<<2)
state.city_orders.set_word(index,65535)
state.city_orders.set_word(index,65535,4)
state.city_orders.set_word(index,65535,8)''',
'clear_monthly_actions':'''actions=state.officer_actions.cursor()
for officer in descending_inclusive(255):
    if actions.byte()==1:
        actions.set_byte(0,0)
    actions=actions.advance(1)
gates=state.city_action_gates.cursor()
for city in descending_inclusive(39):
    flags=gates.byte()
    gates.append_byte(u8(flags&253))''',
'terrain_cell_query':'''row=u16(row)
column=u16(column)
stride=u16(row<<3)
index=u16(u16(row+stride)<<3)
index=u16(index+column)
terrain=state.terrain_cells.byte(index)
cost=state.terrain_costs.byte(terrain)
return terrain,cost''',
'queue_development_order':'''city=state.current_city()
index=u16((u16(city<<1)+state.current_city())<<2)
record=state.city_orders.at(index)
previous=record.word()
if not negative_word(previous):
    state.officer_actions.set_byte(previous,0)
    record.set_word(0,65535)
    if previous==state.selected_officer():
        return None
record.set_word(0,state.selected_officer())
record.set_word(2,state.development_amount())
officer=state.selected_officer()
state.officer_actions.set_byte(officer,2)''',
'queue_welfare_order':'''city=state.current_city()
index=u16((u16(city<<1)+state.current_city())<<2)
record=state.city_orders.at(index,4)
previous=record.word()
if not negative_word(previous):
    state.officer_actions.set_byte(previous,0)
    record.set_word(0,65535)
    if previous==state.selected_officer():
        return None
record.set_word(0,state.selected_officer())
record.set_word(2,state.development_amount())
officer=state.selected_officer()
state.officer_actions.set_byte(officer,3)''',
}
APPROVED={'GameState','Table','Cursor','Byte','Word','Long','u8','u16','u32','s8','low8','low16',
          'replace_byte','negative_byte','negative_word','divu_retained','descending_inclusive',
          'project_officer_arrival_fields'}
SLOT_VALUES={
 'scan_city_officers':{255:('scan_latch',0,65535)},
 'mark_c300_list':{40:('status_threshold',0,255),128:('status_flag',0,255)},
 'replace_city_assignments':{41:('replacement_bias',0,65535),64:('selected_flag',0,65535),255:('scan_latch',0,65535)},
 'defense_progress':{999:('progress_cap',0,65535)},
 'battle_progress_award':{100:('award_divisor',1,65535),999:('progress_cap',0,65535)},
 'replenish_b200_troops':{255:('scan_latch',0,65535),40:('city_threshold',0,65535),15:('growth_factor',0,65535),100:('growth_divisor',1,65535)},
 'grow_original_long_field':{100:('growth_divisor',1,65535),1000:('long_cap',0,0xFFFFFFFF)},
 'recover_unacted_officer_b200':{255:('scan_latch',0,65535),40:('city_threshold',0,255),15:('growth_factor',0,65535),100:('growth_divisor',1,65535)},
 'add_progress_be':{999:('progress_cap',0,65535)},
 'split_progress':{10:('progress_divisor',1,65535),999:('progress_cap',0,65535)},
 'add_progress_c000':{999:('progress_cap',0,65535)},
 'owner_head_lookup':{513:('scene_value',0,65535)},
 'clear_city_orders':{65535:('empty_marker',0,65535)},
 'clear_monthly_actions':{255:('officer_latch',0,65535),39:('city_latch',0,65535)},
 'terrain_cell_query':{3:('stride_shift',1,8)},
}


def parse(source):
    if type(source) is not str: raise CompileError('explicit officer semantic text required')
    try: tree=ast.parse(source)
    except (SyntaxError,ValueError) as exc: raise CompileError('invalid officer Python source') from exc
    functions={};imported=set()
    for node in tree.body:
        if isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and type(node.value.value) is str: continue
        if isinstance(node,ast.ImportFrom):
            if node.level!=1 or node.module!='domain' or any(n.asname or n.name not in APPROVED for n in node.names):
                raise CompileError('approved explicit domain imports only')
            imported.update(n.name for n in node.names);continue
        if not isinstance(node,ast.FunctionDef) or node.name not in SIGNATURES or node.name in functions:
            raise CompileError('only18 declared officer business functions admitted')
        if node.type_params or node.decorator_list: raise CompileError('generic/decorated ABI not supported')
        functions[node.name]=node
    if set(functions)!=set(SIGNATURES): raise CompileError('all18 officer business functions required')
    require_declared_names(functions,imported)
    result={}
    for name,fn in functions.items():
        signature,returns=SIGNATURES[name]
        # The one current C23 projection has a real complete declaration.
        # Other seventeen bodies retain their original finite slot grammar.
        flow=DECLARATIONS[name]['flow'] if name in DECLARATIONS else FLOWS[name]
        text=f'def {name}({signature})->{returns}:\n'+'\n'.join('    '+line for line in flow.splitlines())
        expected=ast.parse(text).body[0]
        actual_body=list(fn.body)
        if actual_body and isinstance(actual_body[0],ast.Expr) and isinstance(actual_body[0].value,ast.Constant) and type(actual_body[0].value.value) is str:
            actual_body=actual_body[1:]
        fn=ast.FunctionDef(name=fn.name,args=fn.args,body=actual_body,decorator_list=fn.decorator_list,
                          returns=fn.returns,type_comment=fn.type_comment,type_params=fn.type_params)
        slots={};declarations=SLOT_VALUES.get(name,{})
        def compare(want,have,parent=None):
            if type(want) is not type(have): raise CompileError(name+': unsupported semantic structure')
            if isinstance(want,ast.Constant):
                if type(want.value) is not type(have.value): raise CompileError(name+': strict semantic literal type')
                spec=declarations.get(want.value) if type(want.value) is int else None
                if name.startswith('queue_') and isinstance(parent,ast.Call) and isinstance(parent.func,ast.Attribute) and parent.func.attr=='set_byte' and parent.args[-1] is want and want.value in (2,3):
                    spec=('action_value',0,255)
                if spec:
                    role,first,last=spec
                    if type(have.value) is not int or not first<=have.value<=last: raise CompileError(name+': typed '+role+' outside admitted width')
                    if role in slots and slots[role]!=have.value: raise CompileError(name+': related '+role+' uses must remain consistent')
                    slots[role]=have.value;return
                if want.value!=have.value: raise CompileError(name+': unsupported semantic literal edit')
                return
            if isinstance(want,ast.AST):
                for key,value in ast.iter_fields(want):
                    compare(value,getattr(have,key),want)
            elif type(want) is list:
                if len(want)!=len(have): raise CompileError(name+': all control/return/effect nodes must be consumed')
                for a,b in zip(want,have): compare(a,b,parent)
            elif want!=have: raise CompileError(name+': unsupported variable/type/operator edit')
        compare(expected,fn)
        result[name]=dict(slots=slots,body=actual_body,args=signature,returns=returns)
    return result


def _absolute(binding):
    address=binding['address'];suffix=binding['suffix']
    return f'0x{address&65535 if suffix=="w" else address:x}:{suffix}'


class Lowerer:
    def __init__(self,name,effects):
        self.name,self.effects=name,effects;self.e=Emitter(BY_NAME[name]);self.e.begin()
        self.slots=effects['slots']
    def slot(self,name,default): return self.slots.get(name,default)
    def ins(self,op,args='',width=2): self.e.ins(op,args,width)
    def lea(self,role,reg):
        b=TABLE_BINDINGS[role];self.ins('lea.l',f'{_absolute(b)},%a{reg}',4 if b['suffix']=='w' else 6)
    def scalar(self,role,reg):
        b=SCALAR_BINDINGS[role];size={8:'b',16:'w',32:'l'}[b['width']]
        self.ins('move.'+size,f'{_absolute(b)},%d{reg}',4 if b['suffix']=='w' else 6)
    def immediate(self,op,value,destination,width=4): self.ins(op,f'#0x{value:x},{destination}',width)
    def branch(self,condition,label,short=False): self.ins(condition+('.b' if short else '.w'),label,2 if short else 4)
    def cap_register(self,reg,cap,short=False):
        done=self.e.fresh('cap_done');self.immediate('cmpi.w',cap,reg)
        self.branch('bls',done,short);self.immediate('move.w',cap,reg);self.e.label(done)
    def cap_memory(self,operand,cap,short):
        done=self.e.fresh('cap_done');self.immediate('cmpi.w',cap,operand,6)
        self.branch('bls',done,short);self.immediate('move.w',cap,operand,6);self.e.label(done)
    def finish(self):
        self.e.end();actual=sum(i['encoding_bytes'] for i in self.e.mapping)
        if actual!=self.e.binding.end-self.e.binding.entry: raise CompileError(self.name+': lowered encoding extent mismatch')
        return self.e.unit(dict(semantic_slots=self.slots,typed_parameters=self.effects['args'],typed_return=self.effects['returns'],
             complete_flow_consumed=True,host_stack_and_full_CPU=False))

    def scan_city_officers(self):
        self.lea('officer_assignments',1);self.immediate('move.w',self.slot('scan_latch',255),'%d3')
        loop,next_=self.e.fresh('scan'),self.e.fresh('next');self.e.label(loop)
        self.ins('move.b','(%a1,%d3.w),%d4',4);self.branch('bpl',next_,True)
        self.immediate('andi.w',127,'%d4');self.ins('cmp.w','%d0,%d4');self.branch('bne',next_,True)
        self.ins('move.w','%d3,(%a0)+');self.ins('addq.w','#1,%d2');self.e.label(next_)
        self.ins('dbra','%d3,'+loop,4)

    def mark_c300_list(self):
        self.lea('action_roster',0);self.lea('officer_status',1)
        loop,done=self.e.fresh('read_member'),self.e.fresh('list_end');self.e.label(loop)
        self.ins('move.w','(%a0)+,%d0');self.branch('bmi',done,True)
        self.immediate('cmpi.b',self.slot('status_threshold',40),'(%a1,%d0.w)',6)
        self.branch('bcs',loop,True);self.immediate('ori.b',self.slot('status_flag',128),'(%a1,%d0.w)',6)
        self.branch('bra',loop,True);self.e.label(done)

    def replace_city_assignments(self):
        self.ins('movem.l','%d1-%d3,-(%a7)',4);self.ins('move.w','%d1,%d2')
        self.immediate('addi.w',self.slot('replacement_bias',41),'%d2')
        self.lea('officer_assignments',0);self.scalar('selected_city',1)
        self.immediate('ori.w',self.slot('selected_flag',64),'%d1');self.lea('officer_assignments',0)
        self.immediate('move.w',self.slot('scan_latch',255),'%d3')
        loop,next_=self.e.fresh('scan'),self.e.fresh('next');self.e.label(loop)
        self.ins('cmp.b','(%a0,%d3.w),%d1',4);self.branch('bne',next_)
        self.ins('move.b','%d2,(%a0,%d3.w)',4);self.e.label(next_);self.ins('dbra','%d3,'+loop,4)
        self.ins('movem.l','(%a7)+,%d1-%d3',4)

    def defense_progress(self):
        self.ins('move.w','%d0,-(%a7)');self.ins('lsl.w','#1,%d2');self.ins('lsl.w','#1,%d3')
        for role in ('progress_be','progress_c'):
            self.lea(role,0);self.ins('move.w','(%a0,%d2.w),%d0',4);self.ins('add.w','%d3,%d0')
            self.cap_register('%d0',self.slot('progress_cap',999));self.ins('move.w','%d0,(%a0,%d2.w)',4)
        self.ins('move.w','(%a7)+,%d0')

    def battle_progress_award(self):
        self.immediate('andi.l',65535,'%d2',6);self.immediate('divu.w',self.slot('award_divisor',100),'%d2')
        self.ins('move.w','%d0,%d1');self.ins('lsl.w','#1,%d1');self.ins('move.w','(%a3,%d1.w),%d3',4)
        self.ins('add.w','%d2,%d3');self.cap_register('%d3',self.slot('progress_cap',999))
        self.ins('move.w','%d3,(%a3,%d1.w)',4)

    def replenish_b200_troops(self):
        for role,reg in (('city_processed',0),('officer_assignments',1),('capacities_b000',2),('troops_b200',3)): self.lea(role,reg)
        self.immediate('move.w',self.slot('scan_latch',255),'%d0')
        loop,next_,cap=self.e.fresh('scan'),self.e.fresh('next'),self.e.fresh('cap_done');self.e.label(loop)
        self.ins('move.b','(%a1,%d0.w),%d1',4);self.immediate('cmpi.w',self.slot('city_threshold',40),'%d1')
        self.branch('bhi',next_);self.ins('tst.b','(%a0,%d1.w)',4);self.branch('bne',next_)
        self.ins('move.w','%d0,%d1');self.ins('lsl.w','#1,%d1');self.ins('move.w','(%a2,%d1.w),%d2',4)
        self.ins('move.w','%d2,%d3');self.immediate('mulu.w',self.slot('growth_factor',15),'%d2')
        self.immediate('divu.w',self.slot('growth_divisor',100),'%d2');self.ins('move.w','(%a3,%d1.w),%d4',4)
        self.ins('add.w','%d2,%d4');self.ins('cmp.w','%d3,%d4');self.branch('bls',cap)
        self.ins('move.w','%d3,%d4');self.e.label(cap);self.ins('move.w','%d4,(%a3,%d1.w)',4)
        self.e.label(next_);self.ins('dbra','%d0,'+loop,4)

    def grow_original_long_field(self):
        self.ins('move.l','(%a0),%d1');self.ins('move.l','%d1,%d2')
        self.immediate('divu.w',self.slot('growth_divisor',100),'%d2');self.immediate('andi.l',65535,'%d2',6)
        self.ins('add.l','%d2,%d1');done=self.e.fresh('cap_done')
        self.immediate('cmpi.l',self.slot('long_cap',1000),'%d1',6);self.branch('bls',done,True)
        self.immediate('move.l',self.slot('long_cap',1000),'%d1',6);self.e.label(done);self.ins('move.l','%d1,(%a0)')

    def education_factor(self):
        self.ins('clr.w','%d3');target_done=self.e.fresh('target_band');teacher_done=self.e.fresh('teacher_band')
        for threshold,band in ((20,5),(40,10),(60,15),(80,20)):
            self.immediate('cmpi.w',threshold,'%d1');self.branch('bcs',target_done,True)
            self.immediate('move.w',band,'%d3')
        self.e.label(target_done)
        for threshold in (20,40,60,80):
            self.immediate('cmpi.w',threshold,'%d0');self.branch('bcs',teacher_done,True);self.ins('addq.w','#1,%d3')
        self.e.label(teacher_done)
        disp=TABLE_BINDINGS['education_factors']['address']-(self.e.pc+2)
        if not -32768<=disp<=32767: raise CompileError('PC readonly data base outside WORD displacement')
        self.ins('lea.l',f'{disp}(%pc),%a0',4);self.ins('nop');self.ins('move.b','(%a0,%d3.w),%d2',4);self.ins('ext.w','%d2')

    def recover_unacted_officer_b200(self):
        for role,reg in (('officer_assignments',0),('city_owners',1),('officer_actions',2),('troops_b200',3),('capacities_b000',4),('city_action_gates',5)): self.lea(role,reg)
        self.immediate('move.w',self.slot('scan_latch',255),'%d0');self.scalar('current_force',7)
        loop,next_,cap=self.e.fresh('scan'),self.e.fresh('next'),self.e.fresh('cap_done');self.e.label(loop)
        self.ins('clr.w','%d1')
        self.ins('move.b','(%a0,%d0.w),%d1',4);self.immediate('cmpi.b',self.slot('city_threshold',40),'%d1')
        self.branch('bhi',next_);self.ins('tst.b','(%a5,%d1.w)',4);self.branch('bne',next_)
        self.ins('cmp.b','(%a1,%d1.w),%d7',4);self.branch('bne',next_);self.ins('tst.b','(%a2,%d0.w)',4);self.branch('bne',next_)
        self.ins('move.w','%d0,%d1');self.ins('lsl.w','#1,%d1');self.ins('move.w','(%a4,%d1.w),%d2',4)
        self.immediate('mulu.w',self.slot('growth_factor',15),'%d2');self.immediate('divu.w',self.slot('growth_divisor',100),'%d2')
        self.ins('move.w','(%a3,%d1.w),%d3',4);self.ins('add.w','%d2,%d3');self.ins('cmp.w','(%a4,%d1.w),%d3',4)
        self.branch('bls',cap);self.ins('move.w','(%a4,%d1.w),%d3',4);self.e.label(cap);self.ins('move.w','%d3,(%a3,%d1.w)',4)
        self.e.label(next_);self.ins('dbra','%d0,'+loop,4)

    def add_progress_be(self):
        self.scalar('selected_officer',0);self.ins('lsl.w','#1,%d0');self.lea('progress_be',0)
        self.ins('add.w','%d2,(%a0,%d0.w)',4);self.cap_memory('(%a0,%d0.w)',self.slot('progress_cap',999),False)

    def split_progress(self):
        self.scalar('selected_officer',0);self.ins('lsl.w','#1,%d0');self.immediate('andi.l',65535,'%d2',6)
        self.immediate('divu.w',self.slot('progress_divisor',10),'%d2');self.lea('progress_be',0)
        self.ins('add.w','%d2,(%a0,%d0.w)',4);self.cap_memory('(%a0,%d0.w)',self.slot('progress_cap',999),True)
        self.ins('lsr.w','#1,%d2');self.lea('progress_c',0);self.ins('add.w','%d2,(%a0,%d0.w)',4)
        self.cap_memory('(%a0,%d0.w)',self.slot('progress_cap',999),True)

    def add_progress_c000(self):
        self.ins('lsl.w','#1,%d0');self.lea('progress_c',0);self.ins('add.w','%d2,(%a0,%d0.w)',4)
        self.cap_memory('(%a0,%d0.w)',self.slot('progress_cap',999),True)

    def owner_head_lookup(self):
        self.lea('city_owners',0);self.ins('move.b','(%a0,%d0.w),%d0',4);self.ins('ext.w','%d0')
        self.ins('lsl.w','#1,%d0');self.lea('force_heads',0);self.ins('move.w','(%a0,%d0.w),%d0',4)
        self.immediate('move.w',self.slot('scene_value',513),_absolute(SCALAR_BINDINGS['scene']),6)

    def clear_city_orders(self):
        self.scalar('selected_city',0);self.ins('move.w','%d0,%d1');self.ins('lsl.w','#1,%d1')
        self.ins('add.w','%d0,%d1');self.ins('lsl.w','#2,%d1');self.lea('city_orders',0)
        for displacement in (0,4,8):
            operand=('' if displacement==0 else f'0x{displacement:x}')+'(%a0,%d1.w)'
            self.immediate('move.w',self.slot('empty_marker',65535),operand,6)

    def clear_monthly_actions(self):
        self.lea('officer_actions',0);self.immediate('move.w',self.slot('officer_latch',255),'%d0')
        loop,next_=self.e.fresh('scan_actions'),self.e.fresh('next');self.e.label(loop)
        self.immediate('cmpi.b',1,'(%a0)',4);self.branch('bne',next_,True);self.ins('clr.b','(%a0)')
        self.e.label(next_);self.ins('addq.w','#1,%a0');self.ins('dbra','%d0,'+loop,4)
        self.lea('city_action_gates',0);self.immediate('move.w',self.slot('city_latch',39),'%d0')
        loop=self.e.fresh('scan_gates');self.e.label(loop);self.ins('bclr.b','#1,(%a0)+',4);self.ins('dbra','%d0,'+loop,4)

    def terrain_cell_query(self):
        self.ins('move.l','%d0,-(%a7)');self.ins('move.w','%d0,%d2')
        self.ins('lsl.w',f'#{self.slot("stride_shift",3)},%d2');self.ins('add.w','%d2,%d0')
        self.ins('lsl.w',f'#{self.slot("stride_shift",3)},%d0');self.ins('add.w','%d1,%d0')
        self.lea('terrain_cells',2);self.ins('clr.w','%d2');self.ins('move.b','(%a2,%d0.w),%d2',4)
        self.lea('terrain_costs',2);self.ins('clr.w','%d3');self.ins('move.b','(%a2,%d2.w),%d3',4)
        self.ins('move.l','(%a7)+,%d0')

    def queue(self,slot,default_action):
        self.scalar('current_city',0);self.ins('lsl.w','#1,%d0')
        self.ins('add.w',_absolute(SCALAR_BINDINGS['current_city'])+',%d0',4);self.ins('lsl.w','#2,%d0')
        self.lea('city_orders',0);self.lea('officer_actions',1)
        operand=('' if slot==0 else f'0x{slot:x}')+'(%a0,%d0.w)'
        self.ins('move.w',operand+',%d1',4);append,done=self.e.fresh('append_order'),self.e.fresh('queue_done')
        self.branch('bmi',append,True);self.ins('clr.b','(%a1,%d1.w)',4)
        self.immediate('move.w',65535,operand,6);self.ins('cmp.w',_absolute(SCALAR_BINDINGS['selected_officer'])+',%d1',4)
        self.branch('beq',done,True);self.e.label(append)
        self.ins('move.w',_absolute(SCALAR_BINDINGS['selected_officer'])+','+operand,6)
        self.ins('move.w',_absolute(SCALAR_BINDINGS['development_amount'])+f',0x{slot+2:x}(%a0,%d0.w)',6)
        self.scalar('selected_officer',0);self.lea('officer_actions',0)
        self.immediate('move.b',self.slot('action_value',default_action),'(%a0,%d0.w)',6);self.e.label(done)
    def queue_development_order(self): self.queue(0,2)
    def queue_welfare_order(self): self.queue(4,3)


def _lower_complete_terrain_frame(complete_city_source, projection):
    """Admit the actual full Scene owner, then lower its retained Frame ABI.

    The scalar facade is admitted separately by parse(); it is not expanded
    into the historical scalar FLOWS body. In particular the real LONG save
    and restore define the actual stack effects and final NZVC from restored
    D0 rather than from the terrain-cost BYTE.
    """
    if type(complete_city_source) is not str:
        raise CompileError('current terrain lowering requires explicit complete Scene city source')
    from ..high_level_remaining_flows import compiler_city
    records = compiler_city.semantic_functions(complete_city_source,
        compiler_city.DECLARATIONS, compiler_city.APPROVED)
    name = 'terrain_cell_query_fields'
    declaration = compiler_city.DECLARATIONS.get(name)
    if (declaration is None or declaration['signature'] !=
            'state: SceneState, frame: FirstDeploymentFrame'
            or declaration['returns'] != 'FirstDeploymentFrame'
            or name not in records or records[name]['rules']):
        raise CompileError('exact complete fixed-ABI terrain Scene rule required')
    binding = BY_NAME['terrain_cell_query']
    if (binding.entry, binding.end) != (0x142A2, 0x142CA):
        raise CompileError('actual complete terrain physical allocation required')
    emitter = Emitter(binding)
    emitter.begin()
    emitter.ins('move.l', '%d0,-(%a7)')
    emitter.ins('move.w', '%d0,%d2')
    emitter.ins('lsl.w', '#3,%d2')
    emitter.ins('add.w', '%d2,%d0')
    emitter.ins('lsl.w', '#3,%d0')
    emitter.ins('add.w', '%d1,%d0')
    for table, index, destination in (('terrain_cells', 'd0', 'd2'),
            ('terrain_costs', 'd2', 'd3')):
        info = TABLE_BINDINGS[table]
        emitter.ins('lea.l', _absolute(info) + ',%a2', 4 if info['suffix'] == 'w' else 6)
        emitter.ins('clr.w', '%' + destination)
        emitter.ins('move.b', f'(%a2,%{index}.w),%{destination}', 4)
    emitter.ins('move.l', '(%a7)+,%d0')
    emitter.end()
    if sum(row['encoding_bytes'] for row in emitter.mapping) != binding.end-binding.entry:
        raise CompileError('complete terrain Frame does not fit its original physical allocation')
    unit = emitter.unit(dict(actual_scene_algorithm=name,
        actual_scene_source='tools/high_level_remaining_flows/business_city.py',
        complete_current_Frame_effects=records[name]['effects'],
        scalar_facade_admitted_without_scalar_lowering=True,
        projection_parameters=projection['args'], projection_return=projection['returns'],
        actual_LONG_stack_save_restore=True, final_flags_from_restored_D0=True))
    return unit


def compile_officer(source,*,only_names=None,complete_city_source=None):
    effects=parse(source)
    if only_names is not None and (type(only_names) is not tuple or only_names!=('add_progress_c000',)):
        raise CompileError('only the original add_progress_c000 emission selection is supported')
    selected=OFFICER_BINDINGS if only_names is None else tuple(binding for binding in OFFICER_BINDINGS if binding.name in only_names)
    units=[]
    for binding in selected:
        if binding.name == 'terrain_cell_query':
            units.append(_lower_complete_terrain_frame(complete_city_source, effects[binding.name]))
        else:
            lowerer=Lowerer(binding.name,effects[binding.name]);getattr(lowerer,binding.name)();units.append(lowerer.finish())
    allocated=sum(sum(i['encoding_bytes'] for i in u['instructions']) for u in units)
    instructions=sum(len(u['instructions']) for u in units)
    expected=(938,270) if only_names is None else (26,7)
    if (allocated,instructions)!=expected: raise CompileError('complete selected officer whole allocation required')
    return dict(units=units,assembly='.cpu 68000\n.text\n'+'\n'.join(u['assembly'] for u in units),
        effects={u['binding']['name']:u['effects'] for u in units},allocated_bytes=allocated,
        instructions=instructions,original_generation_input=False,complete_CPU=False,
        complete_current_catalog_admitted=True,complete_current_catalog_count=len(effects),
        current_semantic_records=effects,all_officer_bindings_emitted=only_names is None)

# C23 projection admission; normal emission now uses the explicit full Frame source.
DECLARATIONS = {}

DECLARATIONS.update({'terrain_cell_query': {'signature': 'state: GameState, row: Word, column: Word', 'returns': 'tuple[Byte, Byte]', 'flow': 'frame = project_officer_arrival_fields(state, 82594, row, column)\nreturn (low8(frame.unit), low8(frame.count))'}})
