"""Bounded typed selection AST to ordinary GNU mnemonics via separate ABI.

Generation is pure: no original image, assembly, opcode listing, private trace,
or source digest is an input. Unknown edits fail closed rather than being
silently interpreted as the canonical body. This is not a general Python or
MC68000 compiler.
"""
import ast
from dataclasses import dataclass, asdict
from .compiler_common import CompileError, Emitter, require_declared_names
from ..high_level_remaining_flows.compiler_common import (
    semantic_functions as admit_semantic_functions, CompileError as SemanticCompileError,
)
from .target import SELECTION_BINDINGS, REGISTERS, TABLE_BINDINGS, SCALAR_BINDINGS, PRESERVED

SIGNATURES = {
    'selected_attribute_average': ((('state','State'),('divisor','Word')),'Long'),
    'count_selected_deployment': ((('state','State'),),'Word'),
    'initialize_selected_assignment': ((('state','State'),('object_view','Table')),'None'),
    'selected_troop_weights': ((('state','State'),),'Pair'),
    'refresh_object_attribute_average': ((('state','State'),('object_view','Table'),('divisor','Word')),'None'),
    'submit_deployment_queue': ((('state','State'),('object_view','Table')),'None'),
    'clear_original_tail_coordinate': ((('state','State'),),'None'),
    'compact_active_deployment_queue': ((('state','State'),),'None'),
    'deployment_force_carry': ((('state','State'),),'Carry'),
}
ANNOTATIONS = {'PreparationState':'State','Table':'Table','Word':'Word','Long':'Long','CarryOutcome':'Carry'}
IMPORTS = set(ANNOTATIONS)|{'u16','u32','low8','replace_byte','zero_extend_word','add_low_byte','sub_low_byte',
                          'shift_low_word','negative_byte','negative_word','descending_inclusive'}
CURSORS = {'selected_roster','selected_attribute_roster','average_roster','active_queue','pair_queue'}
NUMBERS = {'Byte','Word','Long','Wide'}
RETURNS = {'selected_attribute_average':('total',), 'count_selected_deployment':('count',),
           'selected_troop_weights':('selected','all_members')}

@dataclass(frozen=True)
class Expr:
    kind: str
    type: str
    value: object = None
    args: tuple = ()

@dataclass(frozen=True)
class Effect:
    kind: str
    target: str = ''
    value: object = None
    body: tuple = ()
    otherwise: tuple = ()

def integer(value, low=-32768, high=65535):
    if type(value) is not int or not low<=value<=high:
        raise CompileError('strict finite scalar literal required')
    return value

def annotation(node):
    if isinstance(node,ast.Constant) and node.value is None:return 'None'
    if isinstance(node,ast.Name):return ANNOTATIONS.get(node.id)
    if (isinstance(node,ast.Subscript) and isinstance(node.value,ast.Name) and node.value.id=='tuple'
            and isinstance(node.slice,ast.Tuple) and len(node.slice.elts)==2
            and all(isinstance(n,ast.Name) and n.id=='Long' for n in node.slice.elts)):
        return 'Pair'
    return None

class Frontend:
    def __init__(self,node):
        wanted,result=SIGNATURES[node.name]
        actual=tuple((a.arg,annotation(a.annotation)) for a in node.args.args)
        if (actual!=wanted or annotation(node.returns)!=result or node.decorator_list or node.args.posonlyargs
                or node.args.kwonlyargs or node.args.vararg or node.args.kwarg or node.args.defaults or node.args.kw_defaults):
            raise CompileError('exact typed selection signature required')
        self.name,self.result,self.types=node.name,result,dict(wanted)
        self.registers=REGISTERS[node.name]

    def expr(self,node):
        if isinstance(node,ast.Name):
            if node.id not in self.types:raise CompileError('undefined typed selection local')
            return Expr('local',self.types[node.id],node.id)
        if isinstance(node,ast.Constant):return Expr('constant','Word',integer(node.value))
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub) and isinstance(node.operand,ast.Constant):
            return Expr('constant','Word',integer(-integer(node.operand.value)))
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.Not):
            value=self.expr(node.operand)
            if value.type!='Bool' and not self.is_bit(value):raise CompileError('Bool or single bit inversion required')
            return Expr('not','Bool',args=(value,))
        if isinstance(node,ast.Tuple):
            values=tuple(self.expr(n) for n in node.elts)
            if tuple(v.type for v in values)!=('Long','Long'):raise CompileError('two explicit LONG results required')
            return Expr('pair','Pair',args=values)
        if isinstance(node,ast.Attribute):
            value=self.expr(node.value)
            if value.type!='State' or node.attr not in TABLE_BINDINGS or node.attr in ('active_queue','pair_queue'):
                raise CompileError('actual state view property required')
            return Expr('view','Cursor' if node.attr in CURSORS else 'Table',node.attr,(value,))
        if isinstance(node,ast.BinOp):
            values=self.expr(node.left),self.expr(node.right)
            op={ast.Add:'add',ast.Sub:'sub',ast.BitAnd:'and',ast.BitOr:'or',ast.LShift:'shl',ast.RShift:'shr'}.get(type(node.op))
            if op is None or any(v.type not in NUMBERS for v in values):raise CompileError('typed scalar arithmetic required')
            if op in ('shl','shr') and (values[1].kind!='constant' or not 1<=values[1].value<=8):
                raise CompileError('immediate shift1..8 required')
            return Expr('binary','Wide',op,values)
        if isinstance(node,ast.Compare):
            if len(node.ops)!=1 or len(node.comparators)!=1:raise CompileError('one scalar comparison required')
            left,right=self.expr(node.left),self.expr(node.comparators[0])
            op={ast.Eq:'eq',ast.NotEq:'ne'}.get(type(node.ops[0]))
            if op is None or left.type not in NUMBERS or right.type not in NUMBERS:raise CompileError('supported typed comparison required')
            if ((left.type=='Byte' and right.kind=='constant' and not 0<=right.value<=255)
                    or (right.type=='Byte' and left.kind=='constant' and not 0<=left.value<=255)):
                raise CompileError('BYTE compare literal outside unsigned width')
            return Expr('compare','Bool',op,(left,right))
        if isinstance(node,ast.Call) and not node.keywords:
            args=tuple(self.expr(n) for n in node.args)
            if isinstance(node.func,ast.Name):
                name=node.func.id
                if name=='Table' and tuple(a.type for a in args)==('State','Long'):return Expr('construct','Table',name,args)
                if name in ('u16','u32') and len(args)==1:
                    typ={'u16':'Word','u32':'Long'}[name]
                    value=args[0]
                    if value.kind=='binary':
                        if value.args[0].type!=typ or (value.args[1].type!=typ and value.args[1].kind!='constant'):
                            raise CompileError('arithmetic operands must have explicit complete result width')
                    elif value.type!=typ and value.kind!='constant':raise CompileError('explicit supported scalar width required')
                    return Expr('intrinsic',typ,name,args)
                if name=='low8' and len(args)==1 and args[0].type in ('Word','Long'):return Expr('intrinsic','Byte',name,args)
                if name=='replace_byte' and len(args)==2 and args[0].type in ('Word','Long') and args[1].type=='Byte':
                    return Expr('intrinsic',args[0].type,name,args)
                if name=='zero_extend_word' and len(args)==1 and args[0].type=='Word':return Expr('intrinsic','Long',name,args)
                if name in ('add_low_byte','sub_low_byte') and len(args)==2 and args[0].type in ('Word','Long'):
                    if args[1].type!='Byte' and not (args[1].kind=='constant' and 0<=args[1].value<=255):
                        raise CompileError('partial BYTE arithmetic requires BYTE value')
                    return Expr('intrinsic',args[0].type,name,args)
                if name=='shift_low_word' and len(args)==2 and args[0].type=='Long' and args[1].kind=='constant' and 1<=args[1].value<=8:
                    return Expr('intrinsic','Long',name,args)
                if name in ('negative_byte','negative_word') and len(args)==1 and args[0].type=={'negative_byte':'Byte','negative_word':'Word'}[name]:
                    return Expr('intrinsic','Bool',name,args)
                if name=='descending_inclusive' and len(args)==1 and args[0].type=='Word':return Expr('loop','Loop',name,args)
                if name in SIGNATURES and tuple(a.type for a in args)==tuple(t for _,t in SIGNATURES[name][0]):
                    return Expr('call',SIGNATURES[name][1],name,args)
                raise CompileError('unknown intrinsic or argument width')
            if isinstance(node.func,ast.Attribute):
                receiver=self.expr(node.func.value);method=node.func.attr
                if receiver.type=='State':
                    if method in SCALAR_BINDINGS and not args:
                        return Expr('scalar',{8:'Byte',16:'Word',32:'Long'}[SCALAR_BINDINGS[method]['width']],method,(receiver,))
                    if method in ('active_queue','pair_queue') and not args:return Expr('view','Cursor',method,(receiver,))
                    if method=='divide_unsigned' and tuple(a.type for a in args)==('Long','Word'):
                        return Expr('intrinsic','Long',method,args)
                    if method=='increment_queue_counter' and len(args)==1 and args[0].kind=='constant' and 0<=args[0].value<=65535:
                        return Expr('counter_add','None',method,args)
                    if method=='carry_result' and len(args)==1 and args[0].kind=='constant' and args[0].value in (0,1):
                        return Expr('carry','Carry',method,args)
                if receiver.type in ('Table','Cursor'):
                    if method=='cursor' and not args:return Expr('cursor','Cursor',method,(receiver,))
                    if method in ('byte','word','long') and len(args)<=2 and all(a.type=='Word' for a in args):
                        return Expr('read',{'byte':'Byte','word':'Word','long':'Long'}[method],method,(receiver,)+args)
                    if method in ('set_byte','set_word','set_long') and 2<=len(args)<=3 and args[0].type=='Word' and (len(args)==2 or args[2].type=='Word'):
                        typ={'set_byte':'Byte','set_word':'Word','set_long':'Long'}[method]
                        value=args[1]
                        if value.type!=typ and not (value.kind=='constant' and 0<=value.value<(1<<{'Byte':8,'Word':16,'Long':32}[typ])):
                            raise CompileError('exact memory store width required')
                        return Expr('store','None',method,(receiver,)+args)
                    if method=='at' and len(args)<=2 and all(a.type=='Word' for a in args):return Expr('at',receiver.type,method,(receiver,)+args)
                    if method=='advance' and len(args)==1 and args[0].kind=='constant' and 1<=abs(args[0].value)<=8:
                        return Expr('advance',receiver.type,method,(receiver,)+args)
                    if receiver.type=='Cursor':
                        if method in ('next_word','next_byte') and not args:return Expr('next','Word' if method=='next_word' else 'Byte',method,(receiver,))
                        if method=='append_byte' and len(args)==1 and (args[0].type=='Byte' or (args[0].kind=='constant' and 0<=args[0].value<=255)):
                            return Expr('append','None',method,(receiver,)+args)
                        if method=='clear_next_byte' and not args:return Expr('clear_next','None',method,(receiver,))
                        if method=='write_relative' and len(args)==2 and args[0].kind=='constant' and (args[1].type=='Byte' or (args[1].kind=='constant' and 0<=args[1].value<=255)):
                            return Expr('relative_store','None',method,(receiver,)+args)
                        if method=='copy_next_byte_relative' and len(args)==1 and args[0].kind=='constant':
                            return Expr('relative_copy','Byte',method,(receiver,)+args)
                raise CompileError('unsupported actual view/state method')
        raise CompileError('unsupported selection expression')

    @staticmethod
    def is_bit(value):
        return value.kind=='binary' and value.value=='and' and value.args[0].type in ('Byte','Word') and value.args[1].kind=='constant'

    def block(self,nodes,loop=None):
        out=[]
        for node in nodes:
            if isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and type(node.value.value) is str:continue
            if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
                name,value=node.targets[0].id,self.expr(node.value)
                if name not in self.registers or value.type not in ('Byte','Word','Long','Table','Cursor'):
                    raise CompileError('actual explicit ABI local required')
                self.types[name]=value.type;out.append(Effect('assign',name,value))
            elif isinstance(node,ast.Expr):
                value=self.expr(node.value)
                if value.type not in ('None','Byte') or value.kind not in ('store','relative_store','append','clear_next','relative_copy','counter_add','call'):
                    raise CompileError('explicit supported side effect required')
                out.append(Effect('effect',value=value))
            elif isinstance(node,ast.If):
                condition=self.expr(node.test)
                if condition.type!='Bool' and not self.is_bit(condition):raise CompileError('typed condition required')
                before=dict(self.types);yes=self.block(node.body,loop);yes_types=dict(self.types)
                self.types=dict(before);no=self.block(node.orelse,loop);no_types=dict(self.types)
                self.types={k:v for k,v in yes_types.items() if no_types.get(k)==v}
                out.append(Effect('if',value=condition,body=yes,otherwise=no))
            elif isinstance(node,ast.While) and not node.orelse:
                condition=None if isinstance(node.test,ast.Constant) and node.test.value is True else self.expr(node.test)
                if condition is not None and condition.type!='Bool':raise CompileError('typed while condition required')
                before=dict(self.types);body=self.block(node.body,'while')
                self.types={k:self.types.get(k,v) for k,v in before.items()};out.append(Effect('while',value=condition,body=body))
            elif isinstance(node,ast.For) and isinstance(node.target,ast.Name) and not node.orelse:
                value=self.expr(node.iter);name=node.target.id
                if value.type!='Loop' or value.args[0].kind!='local' or value.args[0].value!=name or name not in self.registers:
                    raise CompileError('same-storage inclusive countdown required')
                before=dict(self.types);body=self.block(node.body,'counted');self.types=dict(before)
                out.append(Effect('counted',name,value,body))
            elif isinstance(node,ast.Break) and loop:out.append(Effect('break'))
            elif isinstance(node,ast.Continue) and loop=='while':out.append(Effect('continue'))
            elif isinstance(node,ast.Pass):out.append(Effect('pass'))
            elif isinstance(node,ast.Return):
                value=Expr('void','None') if node.value is None else self.expr(node.value)
                if value.type!=self.result:raise CompileError('exact typed return/completion required')
                out.append(Effect('return',value=value))
            else:raise CompileError('unsupported selection statement or counted continue')
        return tuple(out)

class Lowering:
    def __init__(self,binding,effects):
        self.binding,self.effects,self.e=binding,effects,Emitter(binding)
        self.registers=REGISTERS[binding.name];self.live=dict(SIGNATURES[binding.name][0])
        self.last_zero=None;self.loops=[];self.exit=self.e.fresh('completion');self.clear=self.e.fresh('carry_clear')
    def reg(self,name):
        if name not in self.registers or name not in self.live:raise CompileError('clobbered or undefined ABI storage')
        return '%'+self.registers[name]
    def bind(self,name,typ):
        register=self.registers[name]
        self.live={k:v for k,v in self.live.items() if k not in self.registers or self.registers[k]!=register or k==name}
        self.live[name]=typ
    def ins(self,op,operands='',width=2,zero=None):
        self.e.ins(op,operands,width)
        if not (op in ('lea','adda.w','addq.w','subq.w') and operands.endswith(tuple('%a'+str(n) for n in range(7)))):
            self.last_zero=zero
    def operand(self,value):
        if value.kind=='local':return self.reg(value.value),0
        if value.kind=='constant':return '#'+str(value.value),2
        if value.kind=='scalar':
            b=SCALAR_BINDINGS[value.value];return f"0x{b['address']:x}:{b['suffix']}",2 if b['suffix']=='w' else 4
        if value.kind=='read':return self.memory(value.args[0],value.args[1:])
        if value.kind=='next':return '('+self.reg(value.args[0].value)+')+',0
        if value.kind=='intrinsic' and value.value=='low8':return self.operand(value.args[0])
        raise CompileError('operand needs a live explicit scalar local')
    def memory(self,view,args):
        if view.kind!='local' or view.type not in ('Table','Cursor'):raise CompileError('bound live view required')
        base=self.reg(view.value);offset=args[0] if args else Expr('constant','Word',0)
        disp=integer(args[1].value) if len(args)>1 and args[1].kind=='constant' else 0
        if len(args)>1 and args[1].kind!='constant':raise CompileError('constant displacement required')
        if offset.kind=='constant':
            if offset.value!=0:raise CompileError('nonzero index requires explicit WORD local')
            return (f'{disp}({base})',2) if disp else (f'({base})',0)
        if offset.type!='Word':raise CompileError('complete signed WORD index required')
        index=self.operand(offset)[0]
        if not index.startswith('%d') or not -128<=disp<=127:raise CompileError('data-register brief WORD index required')
        return f'{disp}({base},{index}.w)',2
    def branch(self,condition,label,width=4):self.e.ins('b'+condition+('.s' if width==2 else '.w'),label,width)
    def assign(self,name,value):
        target='%'+self.registers[name]
        if value.kind in ('view','cursor'):
            original=value if value.kind=='view' else value.args[0]
            if original.kind=='view':
                b=TABLE_BINDINGS[original.value];self.ins('lea',f"0x{b['address']:x}:{b['suffix']},"+target,4 if b['suffix']=='w' else 6)
            elif original.kind=='local':
                if self.reg(original.value)!=target:self.ins('movea.l',self.reg(original.value)+','+target)
            else:raise CompileError('cursor conversion needs actual bound or property view')
        elif value.kind=='construct':
            source,extension=self.operand(value.args[1]);self.ins('movea.l',source+','+target,2+extension)
        elif value.kind=='at':
            receiver,*args=value.args
            if len(args)==1 and args[0].kind in ('scalar','read'):
                if self.reg(receiver.value)!=target:raise CompileError('live ADDA must retain receiver storage')
                source,extension=self.operand(args[0]);self.ins('adda.w',source+','+target,2+extension)
            else:
                source,extension=self.memory(receiver,args);self.ins('lea',source+','+target,2+extension)
        elif value.kind=='advance':
            if self.reg(value.args[0].value)!=target:raise CompileError('pointer step needs same storage')
            amount=value.args[1].value;self.ins('addq.w' if amount>0 else 'subq.w','#'+str(abs(amount))+','+target)
        elif value.kind=='intrinsic':
            name_op,args=value.value,value.args
            if name_op in ('u16','u32'):
                typ='w' if name_op=='u16' else 'l';source=args[0]
                if source.kind=='binary':
                    left,right=source.args
                    if self.operand(left)[0]!=target:raise CompileError('arithmetic first operand must retain actual storage')
                    operand,extension=self.operand(right)
                    op=source.value
                    if op in ('shl','shr'):
                        self.ins('lsl.'+typ if op=='shl' else 'lsr.'+typ,operand+','+target,zero=name)
                    elif op in ('and','or') and right.kind=='constant':
                        mask=integer(right.value,0,65535)
                        if op=='or' and mask and not mask&(mask-1):self.ins('bset','#'+str(mask.bit_length()-1)+','+target,4)
                        else:self.ins('andi.'+typ if op=='and' else 'ori.'+typ,operand+','+target,4 if typ=='w' else 6,zero=name)
                    elif op in ('add','sub'):
                        if right.kind=='constant' and typ=='w' and 1<=right.value<=8:
                            self.ins('addq.w' if op=='add' else 'subq.w',operand+','+target,zero=name)
                        elif right.kind=='constant':self.ins(('addi.' if op=='add' else 'subi.')+typ,operand+','+target,4 if typ=='w' else 6,zero=name)
                        else:self.ins(('add.' if op=='add' else 'sub.')+typ,operand+','+target,2+extension,zero=name)
                    else:raise CompileError('supported finite arithmetic family required')
                elif source.kind=='constant' and source.value==0:
                    self.ins('clr.w',target,zero=name) if typ=='w' else self.ins('moveq','#0,'+target,zero=name)
                else:
                    operand,extension=self.operand(source)
                    if operand!=target:self.ins('move.'+typ,operand+','+target,2+extension,zero=name)
            elif name_op=='replace_byte':
                if self.operand(args[0])[0]!=target:raise CompileError('partial write retains its actual first storage')
                operand,extension=self.operand(args[1]);self.ins('move.b',operand+','+target,2+extension)
            elif name_op=='zero_extend_word':
                if self.operand(args[0])[0]!=target:raise CompileError('zero extension storage mismatch')
                self.ins('andi.l','#65535,'+target,6,zero=name)
            elif name_op in ('add_low_byte','sub_low_byte'):
                if self.operand(args[0])[0]!=target:raise CompileError('partial BYTE arithmetic storage mismatch')
                operand,extension=self.operand(args[1]);op='add' if name_op=='add_low_byte' else 'sub'
                self.ins(op+('i.b' if args[1].kind=='constant' else '.b'),operand+','+target,2+extension)
            elif name_op=='shift_low_word':
                if self.operand(args[0])[0]!=target:raise CompileError('partial WORD shift storage mismatch')
                self.ins('lsr.w','#'+str(args[1].value)+','+target)
            elif name_op=='divide_unsigned':
                if self.operand(args[0])[0]!=target:raise CompileError('DIVU retains real complete numerator storage')
                operand,extension=self.operand(args[1]);self.ins('divu.w',operand+','+target,2+extension)
            else:raise CompileError('unsupported typed assignment intrinsic')
        else:
            if value.type not in ('Byte','Word','Long'):raise CompileError('supported scalar assignment required')
            typ={'Byte':'b','Word':'w','Long':'l'}[value.type]
            source,extension=self.operand(value)
            if source!=target:self.ins('move.'+typ,source+','+target,2+extension,zero=name if typ!='b' else None)
        self.bind(name,value.type)
    def effect(self,value):
        if value.kind=='store':
            receiver,offset,source,*disp=value.args;destination,extension=self.memory(receiver,(offset,*disp))
            typ={'set_byte':'b','set_word':'w','set_long':'l'}[value.value]
            if source.kind=='constant' and source.value==0:self.ins('clr.'+typ,destination,2+extension)
            else:
                operand,source_extension=self.operand(source)
                if source.kind=='constant' and typ=='l':source_extension=4
                self.ins('move.'+typ,operand+','+destination,2+extension+source_extension)
        elif value.kind in ('append','clear_next','relative_store','relative_copy'):
            receiver=value.args[0];register=self.reg(receiver.value)
            if value.kind=='relative_copy':
                self.ins('move.b','('+register+')+,'+str(integer(value.args[1].value))+'('+register+')',4)
            elif value.kind=='clear_next':self.ins('clr.b','('+register+')+')
            else:
                source=value.args[-1];operand,extension=self.operand(source)
                if value.kind=='append':destination='('+register+')+';extra=0
                else:
                    delta=integer(value.args[1].value);destination=f'{delta}({register})' if delta else '('+register+')';extra=2 if delta else 0
                self.ins('move.b',operand+','+destination,2+extension+extra)
        elif value.kind=='counter_add':
            binding=SCALAR_BINDINGS['queue_counter'];operand=f"0x{binding['address']:x}:{binding['suffix']}"
            self.ins('addi.w','#'+str(value.args[0].value)+','+operand,4+(2 if binding['suffix']=='w' else 4))
        elif value.kind=='call':
            parameters,_=SIGNATURES[value.value]
            for (name,typ),argument in zip(parameters,value.args):
                if typ=='State':continue
                if argument.kind!='local' or self.reg(argument.value)!='%'+REGISTERS[value.value][name]:
                    raise CompileError('actual callee ABI storage mismatch')
            self.ins('bsr.w',value.value,4)
            # Non-state arguments can be clobbered by the called body. No new
            # use of an old alias may be silently regarded as preserved.
            callee_regs=set(REGISTERS[value.value].values())
            self.live={k:v for k,v in self.live.items() if k not in self.registers or self.registers[k] not in callee_regs}
        else:raise CompileError('supported side effect required')
    def condition(self,value,target,true=True,width=4):
        if value.kind=='not':return self.condition(value.args[0],target,not true,width)
        if value.kind=='intrinsic' and value.value in ('negative_byte','negative_word'):
            argument=value.args[0]
            if not (value.value=='negative_word' and argument.kind=='local' and self.last_zero==argument.value):
                operand,extension=self.operand(argument);self.ins('tst.b' if value.value=='negative_byte' else 'tst.w',operand,2+extension)
            return self.branch('mi' if true else 'pl',target,width)
        if value.kind=='binary' and value.value=='and':
            argument,mask=value.args
            limit=255 if argument.type=='Byte' else 65535;bit=integer(mask.value,1,limit)
            if bit&(bit-1):raise CompileError('single typed bit test required')
            operand,extension=self.operand(argument);self.ins('btst','#'+str(bit.bit_length()-1)+','+operand,4+extension)
            return self.branch('ne' if true else 'eq',target,width)
        if value.kind!='compare':raise CompileError('supported condition required')
        left,right=value.args
        if right.kind=='constant' and right.value==0:
            if left.kind=='relative_copy':self.effect(left)
            elif left.kind=='local' and self.last_zero==left.value:pass
            else:
                operand,extension=self.operand(left);self.ins('tst.b' if left.type=='Byte' else 'tst.w',operand,2+extension)
        elif right.kind=='constant':
            operand,extension=self.operand(left)
            if left.type not in ('Byte','Word'):raise CompileError('explicit narrow compare required')
            self.ins('cmpi.b' if left.type=='Byte' else 'cmpi.w','#'+str(right.value)+','+operand,4+extension)
        else:
            lhs,lhs_extension=self.operand(left);rhs,extension=self.operand(right)
            if lhs_extension or not lhs.startswith('%d') or left.type!=right.type:raise CompileError('same width comparison needs live first register')
            self.ins('cmp.b' if left.type=='Byte' else 'cmp.w',rhs+','+lhs,2+extension)
        code=value.value
        if not true:code={'eq':'ne','ne':'eq'}[code]
        self.branch(code,target,width)
    def return_value(self,value):
        result=SIGNATURES[self.binding.name][1]
        if result=='None':
            if value.type!='None':raise CompileError('void return required')
            return self.exit
        if result=='Carry':
            if value.kind!='carry':raise CompileError('explicit privileged carry completion required')
            return self.clear if value.args[0].value==0 else None
        actual=value.args if value.kind=='pair' else (value,)
        wanted=RETURNS[self.binding.name]
        if len(actual)!=len(wanted) or any(a.kind!='local' or a.value!=n or self.reg(a.value)!='%'+self.registers[n] for a,n in zip(actual,wanted)):
            raise CompileError('return must use the live exact result ABI storage')
        return self.exit
    def block(self,effects,fallthrough=None):
        for index,item in enumerate(effects):
            last=index==len(effects)-1
            if item.kind=='assign':self.assign(item.target,item.value)
            elif item.kind=='effect':self.effect(item.value)
            elif item.kind=='pass':pass
            elif item.kind=='return':
                target=self.return_value(item.value)
                if target is None:
                    self.ins('ori.w','#1,%sr',4);self.branch('ra',self.exit,4)
                elif not last or fallthrough!=target:self.branch('ra',target,4)
            elif item.kind in ('break','continue'):
                if not self.loops:raise CompileError('actual loop scope required')
                target=self.loops[-1][0 if item.kind=='continue' else 1]
                if fallthrough!=target:self.branch('ra',target,2)
            elif item.kind=='if':
                if len(item.body)==1 and item.body[0].kind in ('return','break','continue') and not item.otherwise:
                    transfer=item.body[0]
                    if transfer.kind=='return':target=self.return_value(transfer.value);width=4
                    else:
                        target=self.loops[-1][0 if transfer.kind=='continue' else 1];width=2 if transfer.kind=='continue' else 4
                        if transfer.kind=='break' and self.binding.name=='selected_attribute_average':width=2
                    if target is None:raise CompileError('conditional carry-one needs explicit branching family')
                    self.condition(item.value,target,True,width);continue
                other=self.e.fresh('alternative');done=self.e.fresh('join')
                self.condition(item.value,other if item.otherwise else done,False)
                before=dict(self.live);self.block(item.body);yes=dict(self.live)
                if item.otherwise:
                    self.branch('ra',done);self.e.label(other);self.live=dict(before);self.block(item.otherwise)
                    self.live={k:v for k,v in yes.items() if self.live.get(k)==v}
                else:self.live={k:v for k,v in before.items() if yes.get(k)==v}
                self.e.label(done);self.last_zero=None
            elif item.kind=='while':
                start=self.e.fresh('scan');done=self.e.fresh('scan_done');self.e.label(start)
                before=dict(self.live);self.loops.append((start,done))
                if item.value is not None and all(i.kind=='pass' for i in item.body):self.condition(item.value,start,True,2)
                else:
                    if item.value is not None:self.condition(item.value,done,False)
                    terminal=item.body and item.body[-1].kind in ('break','return')
                    tail=item.body[-1] if item.body else None
                    conditional_break=(item.value is None and tail is not None and tail.kind=='if'
                                       and not tail.otherwise and len(tail.body)==1 and tail.body[0].kind=='break')
                    if conditional_break:
                        self.block(item.body[:-1]);self.condition(tail.value,start,False,2)
                    else:
                        self.block(item.body,done if terminal and item.body[-1].kind=='break' else None)
                        if not terminal:self.branch('ra',start,2)
                self.loops.pop();self.e.label(done)
                self.live={k:v for k,v in before.items() if self.live.get(k)==v};self.last_zero=None
            elif item.kind=='counted':
                counter=self.reg(item.target);start=self.e.fresh('countdown');done=self.e.fresh('countdown_done')
                self.e.label(start);self.loops.append((start,done));self.block(item.body)
                self.loops.pop();self.e.ins('dbra',counter+','+start,4);self.e.label(done)
                self.live.pop(item.target,None);self.last_zero=None
            else:raise CompileError('supported typed effect family required')
    def finish(self):
        self.e.begin()
        for register in PRESERVED.get(self.binding.name,()):self.ins('move.l','%'+register+',-(%sp)')
        self.block(self.effects,self.exit)
        if SIGNATURES[self.binding.name][1]=='Carry':
            self.e.label(self.clear);self.ins('andi.w','#65534,%sr',4)
        self.e.label(self.exit)
        for register in reversed(PRESERVED.get(self.binding.name,())):self.ins('movea.l','(%sp)+,%'+register)
        self.e.end();return self.e.unit([asdict(e) for e in self.effects])

def scoped_break(effects):
    """Break belongs to the nearest real loop, not any nested loop."""
    return any(e.kind=='break' or (e.kind=='if' and (scoped_break(e.body) or scoped_break(e.otherwise))) for e in effects)

def normal_fallthrough(effects):
    for e in effects:
        if e.kind=='return':return False
        if e.kind=='if' and e.otherwise and not normal_fallthrough(e.body) and not normal_fallthrough(e.otherwise):return False
        if e.kind=='while' and e.value is None and not scoped_break(e.body):return False
    return True

def contains_return(effects):
    return any(e.kind=='return' or contains_return(e.body) or contains_return(e.otherwise) for e in effects)

def _admit_selection_source(source):
    """Full current nine bodies, effective declarations and import/name guards.

    Admission is not emission: C21 projection signatures can be admitted without
    pretending their arbitrary CPU Frame is handled by the legacy Frontend.
    """
    if type(source) is not str or not source or len(source) > 100000:
        raise CompileError('bounded explicit complete selection source required')
    try:
        records = admit_semantic_functions(source, DECLARATIONS, APPROVED)
    except SemanticCompileError as error:
        raise CompileError(str(error)) from error
    functions = {node.name: node for node in ast.parse(source).body
                 if isinstance(node, ast.FunctionDef)}
    if set(functions) != set(SIGNATURES) or set(records) != set(SIGNATURES):
        raise CompileError('all nine complete current selection bodies required')
    # This checks every genuine existing typed signature before any selection.
    # It neither lowers nor executes a projection body.
    for node in functions.values():
        Frontend(node)
    return functions, records


def compile_selection(source, only_names=None):
    """Admit all nine current bodies, then normally lower explicit old Bindings.

    With no selection this still attempts the whole original cluster and fails
    closed on unsupported C21 projection operations. With an explicit original
    name tuple, no source/declaration is sliced and only those units are emitted.
    """
    functions, records = _admit_selection_source(source)
    if only_names is None:
        bindings = SELECTION_BINDINGS
    else:
        if (type(only_names) is not tuple or not only_names
                or any(type(name) is not str for name in only_names)
                or len(set(only_names)) != len(only_names)
                or not set(only_names) <= set(SIGNATURES)):
            raise CompileError('nonempty unique original selection Binding names required')
        bindings = tuple(binding for binding in SELECTION_BINDINGS
                         if binding.name in only_names)
        if tuple(binding.name for binding in bindings) != only_names:
            raise CompileError('original physical Binding order required')
    units = []
    for binding in bindings:
        frontend = Frontend(functions[binding.name])
        effects = frontend.block(functions[binding.name].body)
        if frontend.result in ('Long', 'Pair', 'Carry') and (not effects or effects[-1].kind != 'return'):
            raise CompileError('required result cannot silently fall through')
        if frontend.result == 'Word' and (normal_fallthrough(effects) or not contains_return(effects)):
            raise CompileError('count result requires explicit return on every normal completion')
        units.append(Lowering(binding, effects).finish())
    return dict(units=units, allocated_bytes=sum(binding.end-binding.entry for binding in bindings),
                complete_current_catalog_admitted=True, complete_current_catalog_count=len(records),
                current_semantic_records=records,
                all_selection_bindings_emitted=bindings == SELECTION_BINDINGS,
                scalar_projection_is_not_complete_Frame=True,
                original_generation_input=False, complete_CPU=False)

# Complete current nine-body admission; projection admission is not native emission.
APPROVED = {'contexts_counter': {'project_preparation_selection_fields'},
 'domain': {'CarryOutcome',
            'Long',
            'PreparationState',
            'Table',
            'Word',
            'add_low_byte',
            'descending_inclusive',
            'low8',
            'negative_byte',
            'negative_word',
            'replace_byte',
            'shift_low_word',
            'sub_low_byte',
            'u16',
            'u32',
            'uint',
            'zero_extend_word'}}

DECLARATIONS = {'selected_attribute_average': {'signature': 'state: PreparationState, divisor: Word',
                                'returns': 'Long',
                                'flow': 'divisor = u16(divisor)\n'
                                        'attributes = state.selected_attributes\n'
                                        'total = u16(0)\n'
                                        'roster = state.selected_attribute_roster.cursor()\n'
                                        'while True:\n'
                                        '    roster_member = roster.next_word()\n'
                                        '    if negative_word(roster_member):\n'
                                        '        break\n'
                                        '    roster_member = u16(roster_member & 255)\n'
                                        '    attribute = u16(0)\n'
                                        '    attribute = replace_byte(attribute, '
                                        'attributes.byte(roster_member))\n'
                                        '    total = u16(total + attribute)\n'
                                        'divisor = u16(divisor & 15)\n'
                                        'total = zero_extend_word(total)\n'
                                        'total = state.divide_unsigned(total, divisor)\n'
                                        'return total'},
 'count_selected_deployment': {'signature': 'state: PreparationState',
                               'returns': 'Word',
                               'flow': 'frame = project_preparation_selection_fields(state, 111202)\n'
                                       'return u16(frame.choice)'},
 'initialize_selected_assignment': {'signature': 'state: PreparationState, object_view: Table',
                                    'returns': 'None',
                                    'flow': 'project_preparation_selection_fields(state, 111226, '
                                            'object_view)'},
 'selected_troop_weights': {'signature': 'state: PreparationState',
                            'returns': 'tuple[Long, Long]',
                            'flow': 'frame = project_preparation_selection_fields(state, 111630)\n'
                                    'return (frame.offset_x, frame.offset_y)'},
 'refresh_object_attribute_average': {'signature': 'state: PreparationState, object_view: Table, divisor: '
                                                   'Word',
                                      'returns': 'None',
                                      'flow': 'uint(divisor, 16)\n'
                                              'project_preparation_selection_fields(state, 111850, '
                                              'object_view)'},
 'submit_deployment_queue': {'signature': 'state: PreparationState, object_view: Table',
                             'returns': 'None',
                             'flow': 'project_preparation_selection_fields(state, 111890, object_view)'},
 'clear_original_tail_coordinate': {'signature': 'state: PreparationState',
                                    'returns': 'None',
                                    'flow': 'project_preparation_selection_fields(state, 111992)'},
 'compact_active_deployment_queue': {'signature': 'state: PreparationState',
                                     'returns': 'None',
                                     'flow': 'project_preparation_selection_fields(state, 112812)'},
 'deployment_force_carry': {'signature': 'state: PreparationState',
                            'returns': 'CarryOutcome',
                            'flow': 'frame = project_preparation_selection_fields(state, 112908)\n'
                                    'return CarryOutcome(int(bool(frame.status & 1)), state.sr)'}}
