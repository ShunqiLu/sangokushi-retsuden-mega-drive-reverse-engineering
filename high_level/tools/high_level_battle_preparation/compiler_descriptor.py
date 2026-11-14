"""Restricted typed expressions/control -> ordinary 68000 descriptor targets.

No original ROM, old assembly, captured code, IR file or opcode payload is a
generation input. Allocation/call/data bindings are explicit compatibility.
"""
import ast
from dataclasses import dataclass
from .compiler_common import CompileError, Emitter, require_declared_names
from .target import DESCRIPTOR_BINDINGS, BY_NAME, REGISTERS, TABLE_BINDINGS, SCALAR_BINDINGS

APPROVED_DOMAIN = {'PreparationState','Table','Word','Long','u16','low8','low16','replace_byte','replace_word'}
SIGNATURES = {
    'prepare_battle_mode_header':(('state','PreparationState'),),
    'prepare_battle_terrain':(('state','PreparationState'),),
    'choose_battle_order':(('state','PreparationState'),('first','Long'),('second','Long')),
    'maximum_three_live_lookup_attributes':(('state','PreparationState'),('officer','Word'),('attributes','Table')),
    'prepare_both_battle_sides':(('state','PreparationState'),('first','Long'),('second','Long')),
}
RETURNS = {'prepare_battle_mode_header':('Word',('d7',)), 'prepare_battle_terrain':('None',()),
           'choose_battle_order':('tuple[Long, Long]',('d0','d7')),
           'maximum_three_live_lookup_attributes':('Word',('d3',)), 'prepare_both_battle_sides':('None',())}
PC_DATA = {'battle_mode_parameters','terrain_parameters','attribute_weights'}


def name(node):
    if not isinstance(node,ast.Name): raise CompileError('local typed name required')
    return node.id


def integer(node):
    if isinstance(node,ast.Constant) and type(node.value) is int: return node.value
    if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub): return -integer(node.operand)
    raise CompileError('strict literal integer required; bool/float refused')


@dataclass(frozen=True)
class Operand:
    text: str
    width: int
    extra: int = 0
    kind: str = 'register'
    storage: str | None = None
    constant: int | None = None


class Lowerer:
    def __init__(self,binding,function):
        self.binding,self.function = binding,function
        self.emitter=Emitter(binding); self.emitter.begin()
        self.regs=REGISTERS[binding.name]
        self.values={}; self.views={}; self.effects=[]; self.zero_high_byte=set()
        for arg,annotation in SIGNATURES[binding.name]:
            if annotation in ('Word','Long'):
                self.values[arg]=Operand('%'+self.regs[arg],16 if annotation=='Word' else 32,storage=self.regs[arg])
            elif annotation=='Table':self.views[arg]=(self.regs[arg],None)

    def ins(self,operation,operands='',width=2):
        self.emitter.ins(operation,operands,width)

    def reg(self,local):
        if local not in self.regs:raise CompileError('local has no compatible live allocation: '+local)
        return self.regs[local]

    def data_label(self,field): return 'prep_data_'+field

    def scalar(self,field):
        if field not in SCALAR_BINDINGS:raise CompileError('unknown scalar field')
        binding=SCALAR_BINDINGS[field]; width=binding['width']; address=binding['address']
        suffix=binding['suffix']; value=address & 65535 if suffix=='w' else address
        return Operand(f'0x{value:x}:{suffix}',width,2 if suffix=='w' else 4,'memory')

    def table_memory(self,view,method,args):
        if method not in ('byte','word','long') or len(args)>2:raise CompileError('bounded typed table read required')
        width={'byte':8,'word':16,'long':32}[method]
        offset=self.expression(args[0]) if args else Operand('#0',16,2,'immediate',constant=0)
        disp=integer(args[1]) if len(args)==2 else 0
        if not -128<=disp<=127:raise CompileError('current 68000 indexed displacement must fit signed BYTE')
        if offset.width!=16:raise CompileError('explicit wrapped WORD index required; BYTE is not an index-width substitute')
        if isinstance(view,ast.Attribute) and isinstance(view.value,ast.Name) and view.value.id=='state':
            field=view.attr
            if field not in PC_DATA:raise CompileError('unbound direct readonly table view')
            if offset.kind!='register':raise CompileError('direct PC indexed data needs live WORD register')
            base=self.data_label(field)+('+'+str(disp) if disp else '')
            return Operand(f'({base}-.-2)(%pc,{offset.text}.w)',width,2,'memory')
        local=name(view)
        if local not in self.views:raise CompileError('table local not definitely initialized')
        register,_=self.views[local]
        if offset.kind=='immediate':
            if offset.constant!=0:raise CompileError('constant table index must be explicit signed view advance')
            return Operand(f'{disp}(%{register})' if disp else f'(%{register})',width,2 if disp else 0,'memory')
        if offset.kind!='register':raise CompileError('WORD register table index required')
        return Operand(f'{disp}(%{register},{offset.text}.w)' if disp else f'(%{register},{offset.text}.w)',width,2,'memory')

    def expression(self,node):
        if isinstance(node,ast.Name):
            if node.id not in self.values:raise CompileError('value not definitely live: '+node.id)
            return self.values[node.id]
        if isinstance(node,ast.Constant) or isinstance(node,ast.UnaryOp):
            value=integer(node)
            if not 0<=value<=65535:raise CompileError('current immediate WORD out of range')
            return Operand('#'+str(value),16,2,'immediate',constant=value)
        if isinstance(node,ast.Call) and not node.keywords:
            if isinstance(node.func,ast.Name) and node.func.id in ('low8','low16') and len(node.args)==1:
                value=self.expression(node.args[0]); width=8 if node.func.id=='low8' else 16
                return Operand(value.text,width,value.extra,value.kind,value.storage,value.constant)
            if isinstance(node.func,ast.Attribute):
                owner=node.func.value; method=node.func.attr
                if isinstance(owner,ast.Name) and owner.id=='state' and not node.args:
                    return self.scalar(method)
                return self.table_memory(owner,method,node.args)
            if isinstance(node.func,ast.Name) and node.func.id in BY_NAME:
                return self.call(node)
        raise CompileError('unsupported typed value expression: '+ast.dump(node))

    def move(self,source,target,width):
        if width not in (8,16,32):raise CompileError('strict operation width required')
        if source.kind=='register' and source.storage==target:return
        self.ins('move.'+{8:'b',16:'w',32:'l'}[width],source.text+',%'+target,2+source.extra)

    def declare_view(self,target,value):
        register=self.reg(target)
        if isinstance(value,ast.Attribute) and isinstance(value.value,ast.Name) and value.value.id=='state':
            field=value.attr
            if field not in TABLE_BINDINGS:raise CompileError('unknown declared state view')
            info=TABLE_BINDINGS[field]
            if field in PC_DATA:
                self.ins('lea','('+self.data_label(field)+'-.-2)(%pc),%'+register,4)
            else:
                address=info['address']; suffix=info['suffix']; address=address&65535 if suffix=='w' else address
                self.ins('lea',f'0x{address:x}:{suffix},%{register}',4 if suffix=='w' else 6)
            self.views[target]=(register,field);return True
        if isinstance(value,ast.Call) and isinstance(value.func,ast.Attribute) and not value.keywords:
            if value.func.attr not in ('at','advance'):return False
            old=name(value.func.value)
            if old not in self.views:raise CompileError('view update requires initialized source')
            oldreg,field=self.views[old]
            if oldreg!=register:raise CompileError('view relocation requires explicit compatible storage')
            method=value.func.attr
            if method=='at' and len(value.args)==1:
                amount=self.expression(value.args[0])
                if amount.width!=16:raise CompileError('signed WORD view displacement required')
                self.ins('adda.w',amount.text+',%'+register,2+amount.extra)
            elif method=='advance' and len(value.args)==1:
                amount=integer(value.args[0])
                if not 1<=amount<=8:raise CompileError('supported address-view quick step is 1..8')
                self.ins('addq.w',f'#{amount},%{register}')
            else:return False
            self.views[target]=(register,field);return True
        return False

    def assign(self,target,value):
        if self.declare_view(target,value):return
        register=self.reg(target)
        if isinstance(value,ast.Call) and isinstance(value.func,ast.Name) and not value.keywords:
            intrinsic=value.func.id
            if intrinsic in ('replace_byte','replace_word') and len(value.args)==2:
                preserved=self.expression(value.args[0])
                if preserved.kind!='register' or preserved.storage!=register:raise CompileError('partial write must preserve actual target storage')
                width=8 if intrinsic=='replace_byte' else 16
                incoming=self.expression(value.args[1])
                if incoming.width!=width:raise CompileError('partial input width must match BYTE/WORD')
                self.move(incoming,register,width)
                self.values[target]=Operand('%'+register,preserved.width,storage=register);return
            if intrinsic=='u16' and len(value.args)==1:
                inner=value.args[0]
                if isinstance(inner,ast.BinOp):
                    if isinstance(inner.op,ast.Mult):
                        left=self.expression(inner.left); factor=integer(inner.right)
                        if factor!=3 or left.width!=16:raise CompileError('supported multiplied WORD index is factor3')
                        self.move(left,register,16);self.ins('lsl.w','#1,%'+register);self.ins('add.w',left.text+',%'+register)
                    elif isinstance(inner.op,ast.BitAnd):
                        left=self.expression(inner.left); mask=integer(inner.right)
                        if not 0<=mask<=65535:raise CompileError('WORD mask required')
                        self.move(left,register,left.width if left.width<16 else 16)
                        self.ins('andi.w',f'#{mask},%{register}',4)
                        if mask<256:self.zero_high_byte.add(register)
                    elif isinstance(inner.op,ast.LShift):
                        left=self.expression(inner.left); count=integer(inner.right)
                        if not 1<=count<=8 or left.kind!='register':raise CompileError('supported WORD immediate shift1..8')
                        self.move(left,register,16);self.ins('lsl.w',f'#{count},%{register}')
                        self.zero_high_byte.discard(register)
                    elif isinstance(inner.op,ast.Add):
                        left=self.expression(inner.left); right=self.expression(inner.right)
                        if left.storage!=register:raise CompileError('in-place WORD sum must preserve left target')
                        if right.kind=='immediate' and 1<=right.constant<=8:self.ins('addq.w',f'#{right.constant},%{register}')
                        else:self.ins('add.w',right.text+',%'+register,2+right.extra)
                        self.zero_high_byte.discard(register)
                    else:raise CompileError('unsupported wrapped WORD arithmetic')
                else:
                    incoming=self.expression(inner)
                    if incoming.kind=='immediate' and incoming.constant==0:
                        self.ins('clr.w','%'+register);self.zero_high_byte.add(register)
                    else:
                        if incoming.width==8 and register not in self.zero_high_byte:
                            raise CompileError('BYTE-to-WORD conversion needs proven clear high BYTE')
                        self.move(incoming,register,8 if incoming.width==8 else 16)
                self.values[target]=Operand('%'+register,16,storage=register);return
        incoming=self.expression(value)
        self.move(incoming,register,incoming.width)
        self.values[target]=Operand('%'+register,incoming.width,storage=register)

    def call(self,node):
        callee=name(node.func)
        if callee not in ('prepare_battle_mode_header','prepare_battle_terrain','choose_battle_order','maximum_three_live_lookup_attributes','compact_active_deployment_queue'):
            raise CompileError('callee outside complete descriptor closure')
        signature=SIGNATURES.get(callee,(('state','PreparationState'),))
        if len(node.args)!=len(signature) or node.keywords:raise CompileError('exact typed callee arity required')
        if name(node.args[0])!='state':raise CompileError('same live state required')
        for argument,(parameter,annotation) in zip(node.args[1:],signature[1:]):
            expected=REGISTERS[callee][parameter]
            if annotation=='Table':
                local=name(argument)
                if local not in self.views or self.views[local][0]!=expected:raise CompileError('callee view actual storage mismatch')
            else:
                operand=self.expression(argument)
                if operand.storage!=expected or operand.width!=(16 if annotation=='Word' else 32):raise CompileError('callee value width/storage mismatch')
        self.ins('bsr.w',callee,4)
        if callee=='maximum_three_live_lookup_attributes':return Operand('%d3',16,storage='d3')
        if callee=='prepare_battle_mode_header':return Operand('%d7',16,storage='d7')
        return Operand('',0,kind='void')

    def condition(self,test,label):
        if not isinstance(test,ast.Compare) or len(test.ops)!=1 or len(test.comparators)!=1:raise CompileError('one typed comparison required')
        left=self.expression(test.left);right=self.expression(test.comparators[0]);op=test.ops[0]
        if left.kind=='memory' and right.kind=='immediate' and right.constant==0:
            self.ins('tst.'+{8:'b',16:'w',32:'l'}[left.width],left.text,2+left.extra)
        else:
            if left.kind!='register' or (right.kind!='immediate' and right.width!=left.width):raise CompileError('matching operation-width register-left comparison required')
            suffix={8:'b',16:'w',32:'l'}[left.width]
            if right.kind=='immediate':self.ins('cmpi.'+suffix,right.text+','+left.text,2+right.extra)
            else:self.ins('cmp.'+suffix,right.text+','+left.text,2+right.extra)
        branch={ast.NotEq:'beq.w',ast.Eq:'bne.w',ast.Lt:'bcc.w'}.get(type(op))
        if branch is None:raise CompileError('unsupported comparison relation')
        self.ins(branch,label,4)

    def statement(self,node,nested=False):
        self.effects.append(dict(operation=type(node).__name__,source_line=node.lineno))
        if isinstance(node,ast.Assign) and len(node.targets)==1:
            target=node.targets[0]
            if isinstance(target,ast.Tuple):
                if len(target.elts)!=2 or any(not isinstance(n,ast.Name) or not isinstance(n.ctx,ast.Store) for n in target.elts):raise CompileError('strict pair of local targets required')
                names=[n.id for n in target.elts]
                if isinstance(node.value,ast.Tuple):
                    if len(node.value.elts)!=2 or [name(n) for n in node.value.elts]!=names[::-1]:raise CompileError('only actual live pair exchange supported')
                    regs=[self.expression(ast.Name(id=n,ctx=ast.Load())) for n in names]
                    if any(r.width!=32 or r.kind!='register' for r in regs):raise CompileError('EXG needs full LONG pair')
                    self.ins('exg',regs[0].text+','+regs[1].text)
                elif isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id=='choose_battle_order':
                    if [self.reg(n) for n in names]!=['d0','d7']:raise CompileError('callee pair return storage mismatch')
                    self.call(node.value)
                    for n,reg in zip(names,('d0','d7')):self.values[n]=Operand('%'+reg,32,storage=reg)
                else:raise CompileError('unsupported pair assignment')
            else:
                local=name(target)
                self.assign(local,node.value)
                register=self.reg(local)
                for stale in list(self.values):
                    if stale!=local and self.values[stale].storage==register:del self.values[stale]
                for stale in list(self.views):
                    if stale!=local and self.views[stale][0]==register:del self.views[stale]
        elif isinstance(node,ast.Expr) and isinstance(node.value,ast.Call):
            call=node.value
            if isinstance(call.func,ast.Name):
                self.call(call)
            elif (isinstance(call.func,ast.Attribute) and isinstance(call.func.value,ast.Name)
                  and call.func.value.id=='state' and call.func.attr.startswith('set_') and len(call.args)==1 and not call.keywords):
                target=self.scalar(call.func.attr[4:]);source=self.expression(call.args[0])
                if source.kind=='immediate' and source.constant==0:
                    self.ins('clr.'+{8:'b',16:'w',32:'l'}[target.width],target.text,2+target.extra)
                else:
                    if source.width!=target.width:raise CompileError('explicit matching payload width required for store')
                    self.ins('move.'+{8:'b',16:'w',32:'l'}[target.width],source.text+','+target.text,2+source.extra+target.extra)
            else:raise CompileError('unsupported statement effect')
        elif isinstance(node,ast.If):
            if node.orelse:raise CompileError('current descriptor if supports no alternate block')
            end=self.emitter.fresh('join');self.condition(node.test,end)
            for child in node.body:self.statement(child,True)
            self.emitter.label(end)
        elif isinstance(node,ast.Return):
            if nested:raise CompileError('nested descriptor return is not admitted')
            annotation,expected=RETURNS[self.binding.name]
            if not expected:
                if node.value is not None:raise CompileError('void result required')
            else:
                items=node.value.elts if isinstance(node.value,ast.Tuple) else [node.value]
                operands=[self.expression(item) for item in items]
                if tuple(o.storage for o in operands)!=expected:raise CompileError('complete return width/storage mismatch')
                expected_width=32 if annotation.startswith('tuple') else 16
                if any(o.width!=expected_width for o in operands):raise CompileError('return semantic width mismatch')
        else:raise CompileError('unsupported descriptor AST statement: '+type(node).__name__)

    def lower(self):
        if RETURNS[self.binding.name][1] and (not self.function.body or not isinstance(self.function.body[-1],ast.Return)):
            raise CompileError('nonvoid rule requires its explicit final typed Python return')
        if any(isinstance(node,ast.Return) for node in self.function.body[:-1]):
            raise CompileError('top-level return must be the final semantic statement')
        for node in self.function.body:self.statement(node)
        self.emitter.end()
        if sum(i['encoding_bytes'] for i in self.emitter.mapping)!=self.binding.end-self.binding.entry:
            raise CompileError('semantic edit does not fit explicit original instruction allocation')
        unit=self.emitter.unit(self.effects)
        definitions='\n'.join(f'.set {self.data_label(field)},0x{TABLE_BINDINGS[field]["address"]:x}' for field in sorted(PC_DATA))+'\n'
        unit['assembly']=definitions+unit['assembly']
        return unit


def compile_descriptor(source):
    if type(source) is not str or len(source.encode('utf-8'))>262144:raise CompileError('bounded descriptor source text required')
    try:tree=ast.parse(source)
    except (SyntaxError,ValueError) as error:raise CompileError('invalid descriptor Python') from error
    functions={};imports=set()
    for node in tree.body:
        if isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and type(node.value.value) is str:continue
        if isinstance(node,ast.ImportFrom) and node.level==1 and node.module in ('domain','business_selection'):
            approved=APPROVED_DOMAIN if node.module=='domain' else {'compact_active_deployment_queue'}
            if any(alias.asname is not None or alias.name not in approved for alias in node.names):raise CompileError('unapproved domain/helper import')
            imports.update(alias.name for alias in node.names);continue
        if not isinstance(node,ast.FunctionDef) or node.name not in RETURNS or node.name in functions:raise CompileError('exact supported descriptor declarations required')
        args=node.args
        if (node.decorator_list or args.posonlyargs or args.vararg or args.kwarg or args.kwonlyargs or args.defaults
                or tuple((a.arg,ast.unparse(a.annotation) if a.annotation else '') for a in args.args)!=SIGNATURES[node.name]
                or node.returns is None or ast.unparse(node.returns) != RETURNS[node.name][0]):raise CompileError('strict descriptor ABI annotation required')
        if any(n.id in APPROVED_DOMAIN or n.id in RETURNS for n in ast.walk(node) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store)):
            raise CompileError('local must not shadow typed intrinsics or callable rules')
        functions[node.name]=node
    if set(functions)!=set(RETURNS):raise CompileError('all five complete descriptor rules required')
    require_declared_names(functions,imports)
    units=[Lowerer(binding,functions[binding.name]).lower() for binding in DESCRIPTOR_BINDINGS]
    return dict(units=units,assembly='.cpu 68000\n.text\n'+'\n'.join(u['assembly'] for u in units),
                new_bytes=514,original_generation_input=False)

# C22 whole current projections; legacy Frontend/native admission NOT upgraded.
DECLARATIONS = {}

DECLARATIONS.update({'prepare_battle_mode_header': {'signature': 'state: PreparationState', 'returns': 'Word', 'flow': 'frame = project_preparation_selection_fields(state, 112546)\nreturn low16(frame.choice)'}})

DECLARATIONS.update({'prepare_battle_terrain': {'signature': 'state: PreparationState', 'returns': 'None', 'flow': 'project_preparation_selection_fields(state, 112720)'}})

DECLARATIONS.update({'choose_battle_order': {'signature': 'state: PreparationState, first: Long, second: Long', 'returns': 'tuple[Long, Long]', 'flow': 'uint(first, 32)\nuint(second, 32)\nframe = project_preparation_selection_fields(state, 112790, first=first, second=second)\nreturn (frame.target_x, frame.choice)'}})

DECLARATIONS.update({'maximum_three_live_lookup_attributes': {'signature': 'state: PreparationState, officer: Word, attributes: Table', 'returns': 'Word', 'flow': 'uint(officer, 16)\nframe = project_preparation_selection_fields(state, 129236, attributes=attributes)\nreturn low16(frame.count)'}})

DECLARATIONS.update({'prepare_both_battle_sides': {'signature': 'state: PreparationState, first: Long, second: Long', 'returns': 'None', 'flow': 'uint(first, 32)\nuint(second, 32)\nproject_preparation_selection_fields(state, 112322, first=first, second=second)'}})


# B101 genuine full-catalog Frame60 ordinary frontend.
def _lower_maximum_three_live_lookup_attributes_fields(binding, effects):
    """Existing descriptor register/PC-data ABI, complete current Frame core.

    The admitted field algorithm is the three live selector maximum, with the
    original reread on a successful BYTE comparison. Emit ordinary target
    instructions through the existing Emitter, never old bytes or an opcode
    payload. Generic policy editing is not admitted by this fixed frontend.
    """
    emitter = Emitter(binding)
    emitter.begin()
    registers = REGISTERS[binding.name]
    officer, index = registers['officer'], registers['index']
    maximum, selector = registers['maximum'], registers['selector']
    attributes, weights = registers['attributes'], registers['weights']
    emitter.ins('move.w', f'%{officer},%{index}')
    emitter.ins('lsl.w', f'#1,%{index}')
    emitter.ins('add.w', f'%{officer},%{index}')
    emitter.ins('lea', f'(prep_data_attribute_weights-.-2)(%pc),%{weights}', 4)
    emitter.ins('clr.w', f'%{maximum}')
    emitter.ins('clr.w', f'%{selector}')
    emitter.ins('move.b', f'(%{attributes},%{index}.w),%{selector}', 4)
    emitter.ins('move.b', f'(%{weights},%{selector}.w),%{maximum}', 4)
    for displacement in (1, 2):
        emitter.ins('addq.w', f'#4,%{weights}')
        emitter.ins('move.b', f'{displacement}(%{attributes},%{index}.w),%{selector}', 4)
        emitter.ins('cmp.b', f'(%{weights},%{selector}.w),%{maximum}', 4)
        join = emitter.fresh('join')
        emitter.ins('bcc.w', join, 4)
        emitter.ins('move.b', f'(%{weights},%{selector}.w),%{maximum}', 4)
        emitter.label(join)
    emitter.end()
    if sum(row['encoding_bytes'] for row in emitter.mapping) != binding.end-binding.entry:
        raise CompileError('complete Frame60 does not fit its genuine physical allocation')
    unit = emitter.unit(effects)
    definitions = '\n'.join(f'.set prep_data_{field},0x{TABLE_BINDINGS[field]["address"]:x}'
                            for field in sorted(PC_DATA))+'\n'
    unit['assembly'] = definitions+unit['assembly']
    return unit


def compile_maximum_lookup_fields(complete_city_source):
    """Entire current RemainingCity FN/DECLARE catalog -> one whole Frame60.

    This is a new ordinary typed entrance, not the historical scalar facade.
    The existing compiler admits all current field functions before selection;
    the whole root has no legacy scalar rules or cached generation input.
    Complete named memory/interface closure is separately retained by callers.
    """
    from ..high_level_remaining_flows import compiler_city as field_compiler
    if type(complete_city_source) is not str:
        raise CompileError('complete current editable field source text required')
    tree = ast.parse(complete_city_source)
    functions = {node.name:node for node in tree.body if isinstance(node,ast.FunctionDef)}
    records = field_compiler.semantic_functions(complete_city_source,
        field_compiler.DECLARATIONS,field_compiler.APPROVED)
    if set(records) != set(functions):
        raise CompileError('entire normal current Frame catalog required before whole selection')
    root = 'maximum_three_live_lookup_attributes_fields'
    declaration = field_compiler.DECLARATIONS[root]
    if (declaration['signature'] != 'state: SceneState, frame: FirstDeploymentFrame'
            or declaration['returns'] != 'FirstDeploymentFrame' or records[root]['rules']):
        raise CompileError('actual complete Frame60 root/DECLARE, never scalar projection')
    binding = BY_NAME['maximum_three_live_lookup_attributes']
    unit = _lower_maximum_three_live_lookup_attributes_fields(binding, records[root]['effects'])
    return dict(units=[unit],assembly='.cpu 68000\n.text\n'+unit['assembly'],
        new_bytes=binding.end-binding.entry,original_generation_input=False,
        complete_current_catalog=True,full_catalog_function_count=len(records),
        effective_current_root_DECLARE=dict(declaration),
        sole_complete_current_Frame_effects=records[root]['effects'],
        actual_current_ordinary_lowerer='_lower_maximum_three_live_lookup_attributes_fields',
        selected_projection_frontend_used=False,old_scalar_frontend_unchanged=True)
