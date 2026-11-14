"""Restricted structured Python AST -> typed effects -> ordinary GNU mnemonics.

The compiler is pure. It neither imports business at runtime nor reads a sample,
old assembly, byte/opcode tables, source hashes or prior generated artifacts.
"""
from dataclasses import dataclass, asdict
import ast
from .target import BINDINGS, BY_NAME, TABLES, SCALARS, CALLS, SIGNATURES, RETURNS, CALL_WRITES,TABLE_EXITS
from .source_inline import inline_settlement_helpers

class CompileError(ValueError): pass

@dataclass(frozen=True)
class Effect:
    operation: str
    width: int
    operands: tuple
    source_line: int

@dataclass(frozen=True)
class FunctionIR:
    name: str
    args: tuple
    body: tuple

WIDTH={'Word':16,'Long':32,'Byte':8,'Table':0,'CityState':0}
ARITH={'add16':('add',16),'sub16':('sub',16),'add32':('add',32),'sub32':('sub',32),
       'sub8':('sub',8),'mask16':('and',16),'mask32':('and',32),'mulu16':('mulu',16),
       'divu16':('divu',16),'shl16':('lsl',16),'shl32':('asl',32)}

def literal(node):
    if isinstance(node,ast.Constant) and type(node.value) is int:return node.value
    if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub):return -literal(node.operand)
    raise CompileError('strict integer literal required')

def expression(node):
    if isinstance(node,ast.Name):return ('name',node.id)
    if isinstance(node,ast.Constant):return ('constant',literal(node))
    if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub):return ('constant',literal(node))
    if isinstance(node,ast.Attribute) and isinstance(node.value,ast.Name) and node.value.id=='state':return ('field',node.attr)
    if isinstance(node,ast.Call) and not node.keywords:
        if isinstance(node.func,ast.Name):return ('call',node.func.id,tuple(expression(x) for x in node.args))
        if isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name):
            return ('method',node.func.value.id,node.func.attr,tuple(expression(x) for x in node.args))
    if isinstance(node,ast.Compare) and len(node.ops)==1 and len(node.comparators)==1:
        op=type(node.ops[0]).__name__
        if op not in ('Eq','NotEq','Lt','LtE','Gt','GtE'):raise CompileError('supported fixed-width comparison required')
        return ('compare',op,expression(node.left),expression(node.comparators[0]))
    if isinstance(node,ast.BoolOp) and isinstance(node.op,ast.And):return ('and',tuple(expression(x) for x in node.values))
    raise CompileError('unsupported semantic expression; no raw target text accepted')

def statements(nodes):
    out=[]
    for node in nodes:
        line=node.lineno
        if isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and type(node.value.value) is str:continue
        if isinstance(node,ast.AnnAssign) and isinstance(node.target,ast.Name) and isinstance(node.annotation,ast.Name) and node.annotation.id in WIDTH:
            out.append(Effect('declare',WIDTH[node.annotation.id],(node.target.id,expression(node.value)),line))
        elif isinstance(node,ast.Assign) and len(node.targets)==1:
            target=node.targets[0]
            if isinstance(target,ast.Name):names=(target.id,)
            elif isinstance(target,ast.Tuple) and all(isinstance(x,ast.Name) for x in target.elts):names=tuple(x.id for x in target.elts)
            else:raise CompileError('typed locals only; no arbitrary target mutation')
            out.append(Effect('assign',0,(names,expression(node.value)),line))
        elif isinstance(node,ast.Expr) and isinstance(node.value,ast.Call):out.append(Effect('invoke',0,(expression(node.value),),line))
        elif isinstance(node,ast.If):out.append(Effect('if',0,(expression(node.test),statements(node.body),statements(node.orelse)),line))
        elif isinstance(node,ast.While) and not node.orelse and isinstance(node.test,ast.Constant) and node.test.value is True:
            out.append(Effect('loop',0,(statements(node.body),),line))
        elif isinstance(node,ast.Break):out.append(Effect('break',0,(),line))
        elif isinstance(node,ast.Return):out.append(Effect('return',0,(() if node.value is None else expression(node.value),),line))
        else:raise CompileError('unsupported semantic statement')
    return tuple(out)

def semantic_ir(source):
    if type(source) is not str or len(source.encode())>65536:raise CompileError('bounded immutable semantic source required')
    try:module=inline_settlement_helpers(ast.parse(source))
    except (SyntaxError, ValueError) as exc:raise CompileError('invalid business Python or settlement helper flow') from exc
    functions=[]
    for node in module.body:
        if isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and type(node.value.value) is str:continue
        if isinstance(node,ast.ImportFrom) and node.level==1 and node.module=='domain' and len(node.names)==1 and node.names[0].name=='*':continue
        if not isinstance(node,ast.FunctionDef) or node.name not in BY_NAME or node.decorator_list:raise CompileError('only declared ordinary business functions allowed')
        args=node.args
        if args.posonlyargs or args.vararg or args.kwarg or args.kwonlyargs or args.defaults:raise CompileError('plain typed positional parameters required')
        parsed=[];signature=[]
        for a in args.args:
            if not isinstance(a.annotation,ast.Name) or a.annotation.id not in WIDTH:raise CompileError('explicit semantic type required')
            signature.append((a.arg,a.annotation.id))
            parsed.append((a.arg,WIDTH[a.annotation.id]))
        if tuple(signature)!=SIGNATURES[node.name]:raise CompileError('exact semantic argument types/arity required; Table is not CityState')
        functions.append(FunctionIR(node.name,tuple(parsed),type_effects(statements(node.body),dict(parsed))))
    if len(functions)!=len(BINDINGS) or set(f.name for f in functions)!=set(BY_NAME):raise CompileError('entire eleven-entry city-cycle module required; no easy subset')
    return tuple(functions)

def result_width(e,types):
    kind=e[0]
    if kind=='name':
        if e[1] not in types:raise CompileError('undefined typed variable '+e[1])
        return types[e[1]]
    if kind in ('field',):return 0
    if kind=='constant':return 0
    if kind=='call':
        name,args=e[1:]
        if name in BY_NAME:return RETURNS.get(name,('',0))[1]
        if name=='sub8':
            if len(args)!=2:raise CompileError('binary partial BYTE subtraction required')
            result_width(args[1],types)
            return result_width(args[0],types)
        widths={'word':16,'long':32,'byte':8,'low_word':16,'low_byte':8,'signed_word':16,
                'add16':16,'sub16':16,'add32':32,'sub32':32,'shl16':16,'shl32':32,
                'mask16':16,'mask32':32,'clear_low_word':32,'negate32':32,'swap_words':32,
                'replace_low_word':32,'mulu16':32,'divu16':32,'stitched_product':32,
                'saturating_add32':32,'subtract_borrow32':32,'minimum32':32}
        if name not in widths:raise CompileError('unknown semantic intrinsic')
        for arg in args:result_width(arg,types)
        return widths[name]
    if kind=='method':
        table,name,args=e[1:]
        if table!='state' and types.get(table)!=0:raise CompileError('live table receiver required')
        for arg in args:result_width(arg,types)
        if table=='state':return SCALARS.get(name,(0,0))[1] if not name.startswith('set_') else 0
        if name=='subtract_byte':return 1
        return {'word':16,'long':32,'byte':8,'next_word':16,'next_byte':8}.get(name,0)
    if kind in ('compare','and'):return 1
    raise CompileError('unsupported semantic result type')

def type_effects(effects,types):
    """Assignments carry actual intrinsic result width, not stale annotations."""
    out=[]
    for effect in effects:
        op,args=effect.operation,effect.operands;width=effect.width
        if op=='declare':
            name,value=args;width=result_width(value,types)
            if effect.width==0 and width!=0 or effect.width!=0 and width==0:raise CompileError('table/scalar type mismatch')
            types[name]=width
        elif op=='assign':
            names,value=args;width=result_width(value,types)
            for name in names:
                types[name]=1 if name=='borrowed' else width
        elif op=='invoke':result_width(args[0],types)
        elif op=='return':width=0 if not args[0] else result_width(args[0],types)
        elif op=='if':
            result_width(args[0],types);true=dict(types);false=dict(types)
            body=type_effects(args[1],true);other=type_effects(args[2],false)
            types.update({k:true[k] for k in true.keys()&false.keys() if true[k]==false[k]})
            args=(args[0],body,other)
        elif op=='loop':
            body=type_effects(args[0],types);args=(body,)
        out.append(Effect(op,width,args,effect.source_line))
    return tuple(out)

def variable_uses(e):
    if not e:return set()
    if e[0]=='name':return set() if e[1]=='state' else {e[1]}
    if e[0] in ('constant','field'):return set()
    if e[0]=='call':return set().union(*(variable_uses(x) for x in e[2])) if e[2] else set()
    if e[0]=='method':return ({e[1]} if e[1]!='state' else set())|set().union(*(variable_uses(x) for x in e[3]))
    if e[0]=='compare':return variable_uses(e[2])|variable_uses(e[3])
    if e[0]=='and':return set().union(*(variable_uses(x) for x in e[1]))
    raise CompileError('unsupported variable-use expression')

def live_after(body):
    """Ordinary backward CFG liveness over branches, loops, returns and break."""
    nodes={};edges={};uses={};defs={}
    def install(effect,successors):
        key=id(effect);nodes[key]=effect;edges[key]=set(successors)
        op,args=effect.operation,effect.operands
        if op=='declare':defs[key]={args[0]};uses[key]=variable_uses(args[1])
        elif op=='assign':defs[key]=set(args[0]);uses[key]=variable_uses(args[1])
        elif op in ('invoke','return'):defs[key]=set();uses[key]=variable_uses(args[0])
        elif op=='if':defs[key]=set();uses[key]=variable_uses(args[0])
        else:defs[key]=set();uses[key]=set()
        return key
    def block(effects,following,loop_exit=None):
        next_nodes=set(following)
        for effect in reversed(effects):
            op,args=effect.operation,effect.operands;key=id(effect)
            if op=='if':
                left=block(args[1],next_nodes,loop_exit);right=block(args[2],next_nodes,loop_exit);install(effect,left|right)
            elif op=='loop':
                install(effect,set());start=block(args[0],{key},next_nodes);edges[key]=start
            elif op=='break':
                if loop_exit is None:raise CompileError('break outside loop')
                install(effect,loop_exit)
            elif op=='return':install(effect,set())
            else:install(effect,next_nodes)
            next_nodes={key}
        return next_nodes
    block(body,set());inside={k:set() for k in nodes};outside={k:set() for k in nodes}
    changed=True
    while changed:
        changed=False
        for key in nodes:
            after=set().union(*(inside[k] for k in edges[key])) if edges[key] else set()
            before=uses[key]|(after-defs[key])
            if before!=inside[key] or after!=outside[key]:inside[key]=before;outside[key]=after;changed=True
    return outside

def exits(body):
    """Structured normal completion, without treating an implicit RTS as return."""
    outcomes={'fall'}
    for effect in body:
        if 'fall' not in outcomes:break
        outcomes.remove('fall');op,args=effect.operation,effect.operands
        if op=='return':outcomes.add('return')
        elif op=='break':outcomes.add('break')
        elif op=='if':outcomes.update(exits(args[1])|exits(args[2]))
        elif op=='loop':
            inner=exits(args[0])
            if 'return' in inner:outcomes.add('return')
            if 'break' in inner:outcomes.add('fall')
            # A fall through a while-True body repeats, not a normal completion.
        else:outcomes.add('fall')
    return outcomes

def table_exit_bindings(ir):
    """Prove promised pointer fields from actual typed effects at every exit.

    Unknown loop-carried binds/calls are conservative. This is an ABI fact,
    not a claim inferred from a function name or an old source template.
    """
    returns=[];registers=BY_NAME[ir.name].variables
    def mutations(expression):
        if not expression:return set()
        kind=expression[0]
        if kind=='method':
            table,method,arguments=expression[1:]
            changed={registers[table]} if table in registers and method in ('next_word','next_byte','append_word','append_long') else set()
            return changed|set().union(*(mutations(arg) for arg in arguments))
        if kind=='call':
            return {r for r in CALL_WRITES.get(expression[1],()) if r.startswith('a')}|set().union(*(mutations(arg) for arg in expression[2]))
        if kind=='compare':return mutations(expression[2])|mutations(expression[3])
        if kind=='and':return set().union(*(mutations(arg) for arg in expression[1]))
        return set()
    def block(body,states):
        for effect in body:
            op,args=effect.operation,effect.operands
            if op=='return':returns.extend(states);states=[];break
            if op=='if':
                for state in states:
                    for register in mutations(args[0]):state[register]=None
                states=block(args[1],[dict(s) for s in states])+block(args[2],[dict(s) for s in states]);continue
            if op=='loop':
                for state in states:
                    for register in tuple(state):state[register]=None
                # This first compatibility backend does not prove loop-carried
                # pointer postconditions or an early return nested in a loop.
                returns.extend(dict(state) for state in states)
                continue
            value=None;name=None
            if op=='declare':name,value=args
            elif op=='assign' and len(args[0])==1:name=args[0][0];value=args[1]
            if name is not None and registers.get(name,'').startswith('a'):
                for state in states:state[registers[name]]=value[1] if value[0]=='field' else None
            expr=args[0] if op in ('invoke','if') else value
            if expr:
                for state in states:
                    for register in mutations(expr):state[register]=None
        return states
    returns.extend(block(ir.body,[{}]))
    if not returns:return {}
    return {r:v for r,v in returns[0].items() if v is not None and all(state.get(r)==v for state in returns)}

class Lowerer:
    def __init__(self,ir,registry):
        self.ir=ir;self.binding=BY_NAME[ir.name];self.regs=dict(self.binding.variables)
        self.registry=registry;self.pointer_registers={}
        self.live=live_after(ir.body);self.carry_live=False
        self.types=dict(ir.args);self.types.pop('state');self.lines=[];self.mapping=[];self.serial=0;self.offset=0
        self.table_fields={};self.bind_counts={};self.last_flags=None
        self.zero_high={f'd{i}':False for i in range(8)}
        self.zero_byte_high={f'd{i}':False for i in range(8)}
        self.return_label=f'.L_{ir.name}_return'
    def label(self,name):
        self.lines.append(name+':');self.last_flags=None;self.carry_live=False
        # At joins a value may come from either path. No optimistic promotion
        # from a partial WORD write to a Python zero-extended LONG is allowed.
        self.zero_high={register:False for register in self.zero_high}
        self.zero_byte_high={register:False for register in self.zero_byte_high}
    def fresh(self):self.serial+=1;return f'.L_{self.ir.name}_{self.serial}'
    def reg(self,name):
        if type(name) is not str or name not in self.regs or self.regs[name]=='carry':raise CompileError('unbound semantic variable: '+str(name))
        return '%'+self.regs[name]
    def emit(self,mnemonic,size,effect):
        if any(c in mnemonic for c in ('\n','\r',';')):raise CompileError('unsafe generated operand')
        symbol=f'{self.ir.name}_instruction_{len(self.mapping):03d}'
        self.lines.extend(('.global '+symbol,symbol+':','        '+mnemonic))
        self.mapping.append(dict(symbol=symbol,offset=self.offset,size=size,operation=effect.operation,width=effect.width,source_line=effect.source_line,mnemonic=mnemonic))
        self.offset+=size
        operation=mnemonic.split()[0].split('.')[0]
        if operation not in ('lea','nop','rts') and not operation.startswith('b'):self.carry_live=False
        operands=mnemonic.split(' ',1)[1] if ' ' in mnemonic else ''
        destination=operands.rsplit(',',1)[-1].lstrip('%')
        if destination in self.zero_high:
            if operation=='moveq':self.zero_high[destination]=0<=int(operands.split(',')[0][1:],0)<=65535
            elif mnemonic.startswith('move.l '):
                source=operands.split(',')[0]
                self.zero_high[destination]=(0<=int(source[1:],0)<=65535) if source.startswith('#') else self.zero_high.get(source.lstrip('%'),False)
            elif mnemonic.startswith('andi.l '):self.zero_high[destination]=int(operands.split(',')[0][1:],0)<=65535
            elif operation=='swap' or operation in ('mulu','divu') or '.l ' in mnemonic:self.zero_high[destination]=False
            if operation=='moveq':self.zero_byte_high[destination]=0<=int(operands.split(',')[0][1:],0)<=255
            elif mnemonic.startswith(('move.l ','move.w ')):
                source=operands.split(',')[0]
                self.zero_byte_high[destination]=(0<=int(source[1:],0)<=255) if source.startswith('#') else self.zero_byte_high.get(source.lstrip('%'),False)
            elif mnemonic.startswith(('andi.l ','andi.w ')):self.zero_byte_high[destination]=int(operands.split(',')[0][1:],0)<=255
            elif mnemonic.startswith('clr.w '):self.zero_byte_high[destination]=True
            elif operation=='swap' or operation in ('mulu','divu') or '.l ' in mnemonic or '.w ' in mnemonic:self.zero_byte_high[destination]=False
    def write_guard(self,name,effect,register=None):
        register=self.regs.get(name) if register is None else register
        for other in self.live[id(effect)]:
            if other!=name and self.regs.get(other)==register:raise CompileError('live semantic variables overlap target storage: '+name+'/'+other)
    def suffix(self,width):
        if width not in (8,16,32):raise CompileError('explicit operand width required')
        return {8:'b',16:'w',32:'l'}[width]
    def integer(self,e):
        if e[0]=='constant':return e[1]
        if e[0]=='call' and e[1] in ('word','long','byte') and len(e[2])==1 and e[2][0][0]=='constant':return e[2][0][1]&((1<<{'word':16,'long':32,'byte':8}[e[1]])-1)
        raise CompileError('typed constant required')
    def operand(self,e,width):
        if e[0]=='name':
            register=self.reg(e[1])
            if width==32 and self.types.get(e[1]) in (8,16) and not self.zero_high.get(register.lstrip('%'),False):
                raise CompileError('partial local cannot be promoted to LONG with unproved zero upper bits')
            if width in (16,32) and self.types.get(e[1])==8 and not self.zero_byte_high.get(register.lstrip('%'),False):
                raise CompileError('partial BYTE local cannot be promoted with unproved high BYTE bits')
            return register,0
        if e[0]=='call' and e[1] in ('low_word','low_byte') and len(e[2])==1:
            narrow=16 if e[1]=='low_word' else 8;inner=e[2][0]
            if width>narrow:
                if inner[0]!='name':raise CompileError('narrowed live read cannot silently feed a wider operand')
                register=self.reg(inner[1]).lstrip('%')
                if not self.zero_high.get(register,False) or narrow==8 and not self.zero_byte_high.get(register,False):
                    raise CompileError('explicit narrowing cannot be ignored for a wider operand')
            return self.operand(inner,width)
        if e[0]=='constant' or e[0]=='call' and e[1] in ('word','long','byte'):
            v=self.integer(e)&((1<<width)-1);return '#0x'+format(v,'x'),4 if width==32 else 2
        if e[0]=='method':
            table,method,args=e[1:]
            if table=='state' and method in SCALARS and not args:
                address,actual=SCALARS[method]
                if actual!=width:raise CompileError('scalar access width differs')
                return f'0x{address:x}:w',2
            if method in ('word','long','byte'):
                actual={'byte':8,'word':16,'long':32}[method]
                if actual!=width:raise CompileError('table access width differs')
                return self.table_operand(table,args)
            if method in ('next_word','next_byte') and not args:
                if width!={'next_word':16,'next_byte':8}[method]:raise CompileError('cursor width differs')
                return '('+self.reg(table)+')+',0
        raise CompileError('unsupported typed operand')
    def table_operand(self,table,args):
        if not 1<=len(args)<=2 or args[0][0]!='name':raise CompileError('WORD-indexed table operand required')
        displacement=0 if len(args)==1 else self.integer(args[1])
        if not -128<=displacement<=127:raise CompileError('brief signed BYTE displacement required')
        text='' if displacement==0 else str(displacement)
        return text+'('+self.reg(table)+','+self.reg(args[0][1])+'.w)',2
    def bind(self,name,field,effect):
        if field not in TABLES:raise CompileError('unknown semantic table')
        ordinal=self.bind_counts.get(name,0)+1;self.bind_counts[name]=ordinal
        phase={('settle_expense','roster',2):('a0',{'member':'d3'}),
               ('settle_shortage','scores',2):('a0',{}),('settle_shortage','roster',2):('a1',{}),
               ('settle_shortage','roster',3):('a0',{}),('settle_shortage','roster',4):('a0',{}),
               ('settle_shortage','modifiers',2):('a1',{})}.get((self.ir.name,name,ordinal))
        if phase:self.regs[name]=phase[0];self.regs.update(phase[1])
        self.write_guard(name,effect)
        self.table_fields[name]=field;address=TABLES[field]
        self.pointer_registers[self.regs[name]]=field
        if address<=65535:operand=f'0x{address:x}:w'
        else:operand=field+'(%pc)'
        self.emit('lea '+operand+','+self.reg(name),4,effect)
        if self.ir.name=='settle_expense' and field=='expense_parameters':self.emit('nop',2,effect)
    def call(self,name,args,effect,destination=None):
        if name not in BY_NAME:raise CompileError('unknown semantic call')
        callee=self.registry[name]
        if len(args)!=len(callee.args) or not args or args[0]!=('name','state'):raise CompileError('complete semantic call arguments required')
        for actual,(formal,bits) in zip(args[1:],callee.args[1:]):
            wanted=BY_NAME[name].variables[formal]
            if result_width(actual,self.types)!=bits:raise CompileError('call argument actual width differs from semantic signature')
            if actual[0]=='field':
                if self.pointer_registers.get(wanted)!=actual[1]:raise CompileError('call pointer is not established by a real prior effect')
            else:
                if actual[0]=='call' and actual[1]=='low_word':actual=actual[2][0]
                if actual[0]!='name' or self.regs.get(actual[1])!=wanted:raise CompileError('call violates its explicit live ABI')
        actual_tables=table_exit_bindings(callee) if name in TABLE_EXITS else {}
        if name in TABLE_EXITS:
            if any(actual_tables.get(register)!=field for register,field in TABLE_EXITS[name].items()):raise CompileError('callee actual exit pointer violates the caller compatibility postcondition')
        for register in CALL_WRITES[name]:self.pointer_registers.pop(register,None)
        self.pointer_registers.update(actual_tables)
        returned={'scaled_income':'d3','build_roster':'d3','step_random':'d0'}
        if destination is not None and self.regs[destination]!=returned.get(name):raise CompileError('call result requires compatible bound storage')
        for variable in self.live[id(effect)]:
            if variable!=destination and self.regs.get(variable) in CALL_WRITES[name]:raise CompileError('semantic local stays live across a callee clobber: '+variable)
        # Explicit compatibility ABI is independent of rule constants. The live
        # threshold pointer is already established by scaled_income, not loaded
        # from an imagined default at the direct-helper entry.
        self.emit(f'{CALLS[name]} {name}'+(':l' if CALLS[name]=='jsr' else ''),6 if CALLS[name]=='jsr' else 4,effect)
        self.last_flags=None;self.carry_live=False
    def assign(self,name,e,width,effect):
        if e[0]=='field':self.bind(name,e[1],effect);return
        dst=self.reg(name);self.write_guard(name,effect)
        if e[0]=='call':
            operation,args=e[1:]
            if operation in BY_NAME:self.call(operation,args,effect,name);return
            if operation in ('word','long','byte'):
                bits={'word':16,'long':32,'byte':8}[operation];v=self.integer(e)&((1<<bits)-1)
                if v==0 and bits!=32:self.emit(f'clr.{self.suffix(bits)} '+dst,2,effect)
                elif bits==32 and (v<=127 or v>=0xFFFFFF80):self.emit(f'moveq #{v if v<=127 else v-0x100000000},'+dst,2,effect)
                else:self.emit(f'move.{self.suffix(bits)} #0x{v:x},'+dst,6 if bits==32 else 4,effect)
                self.last_flags=(name,bits);return
            if operation in ('low_word','low_byte'):
                bits=16 if operation=='low_word' else 8;src,extra=self.operand(args[0],bits)
                self.emit(f'move.{self.suffix(bits)} {src},{dst}',2+extra,effect);self.last_flags=(name,bits);return
            if operation in ('swap_words','negate32','clear_low_word'):
                if args!=(('name',name),):raise CompileError('in-place width operation required')
                instruction={'swap_words':'swap','negate32':'neg.l','clear_low_word':'clr.w'}[operation]
                self.emit(instruction+' '+dst,2,effect);self.last_flags=(name,16 if operation=='clear_low_word' else 32);return
            if operation=='replace_low_word':
                if args[0]!=('name',name):raise CompileError('in-place partial assignment required')
                src,extra=self.operand(args[1],16);self.emit(f'move.w {src},{dst}',2+extra,effect);self.last_flags=(name,16);return
            if operation=='stitched_product':
                if args[0]!=('name',name) or self.binding.scratch is None:raise CompileError('explicit stitched-product scratch ABI required')
                src,extra=self.operand(args[1],16);scratch='%'+self.binding.scratch
                self.write_guard(name,effect,self.binding.scratch)
                for instruction in (f'move.l {dst},{scratch}',f'mulu.w {src},{dst}',f'swap {scratch}',f'mulu.w {src},{scratch}',f'swap {scratch}',f'add.l {scratch},{dst}'):
                    self.emit(instruction,2+extra if instruction.startswith('mulu') else 2,effect)
                self.last_flags=(name,32);return
            if operation in ('saturating_add32','minimum32'):
                if args[0]!=('name',name):raise CompileError('in-place saturation required')
                end=self.fresh();src,extra=self.operand(args[1],32)
                if operation=='saturating_add32':
                    self.emit(f'add.l {src},{dst}',2+extra,effect);self.emit('bcc.b '+end,2,effect);self.emit('moveq #-1,'+dst,2,effect)
                else:
                    self.emit(f'cmpi.l {src},{dst}',2+extra,effect);self.emit('bls.b '+end,2,effect);self.emit(f'move.l {src},{dst}',2+extra,effect)
                self.label(end);return
            if operation in ARITH:
                mnemonic,bits=ARITH[operation]
                if len(args)!=2:raise CompileError('binary fixed-width arithmetic required')
                # MULU consumes a WORD; DIVU consumes its entire LONG numerator.
                # Masks may themselves clear promotion bits before they matter.
                consume=32 if operation=='divu16' else bits
                clears=(operation in ('mask16','mask32') and self.integer(args[1])<=((1<<result_width(args[0],self.types))-1))
                if not clears:self.operand(args[0],consume)
                if args[0]!=('name',name):self.assign(name,args[0],bits,effect)
                right,extra=self.operand(args[1],bits)
                if operation.startswith('shl'):
                    count=self.integer(args[1])
                    if not 1<=count<=8:raise CompileError('immediate shift count1..8 required')
                    self.emit(f'{mnemonic}.{self.suffix(bits)} #{count},{dst}',2,effect)
                elif mnemonic=='and':self.emit(f'andi.{self.suffix(bits)} {right},{dst}',2+extra,effect)
                elif mnemonic in ('add','sub') and right.startswith('#') and 1<=self.integer(args[1])<=8:
                    self.emit(f'{mnemonic}q.{self.suffix(bits)} #{self.integer(args[1])},{dst}',2,effect)
                else:self.emit(f'{mnemonic}.{self.suffix(bits)} {right},{dst}',2+extra,effect)
                self.types[name]=width
                self.last_flags=(name,bits);return
            raise CompileError('unsupported arithmetic intrinsic: '+operation)
        if e[0]=='method':
            method=e[2];bits={'word':16,'long':32,'byte':8,'next_word':16,'next_byte':8}.get(method)
            if e[1]=='state':bits=SCALARS.get(method,(0,0))[1]
            if not bits:raise CompileError('unsupported read expression')
            src,extra=self.operand(e,bits);self.emit(f'move.{self.suffix(bits)} {src},{dst}',2+extra,effect);self.last_flags=(name,bits);return
        if e[0]=='name':
            bits=width or self.types[name];src,_=self.operand(e,bits)
            if src!=dst:self.emit(f'move.{self.suffix(bits)} {src},{dst}',2,effect)
            self.last_flags=(name,bits);return
        raise CompileError('unsupported assignment')
    def invoke(self,e,effect):
        if e[0]=='call':self.call(e[1],e[2],effect);return
        if e[0]!='method':raise CompileError('typed call/write required')
        table,method,args=e[1:]
        if table=='state' and method.startswith('set_') and method[4:] in SCALARS and len(args)==1:
            address,bits=SCALARS[method[4:]];src,extra=self.operand(args[0],bits)
            self.emit(f'move.{self.suffix(bits)} {src},0x{address:x}:w',4+extra,effect);self.last_flags=None;return
        if method in ('append_word','append_long','put_word') and len(args)==1:
            bits=32 if method=='append_long' else 16;src,extra=self.operand(args[0],bits)
            dst='('+self.reg(table)+')'+('' if method=='put_word' else '+')
            self.emit(f'move.{self.suffix(bits)} {src},{dst}',2+extra,effect);self.last_flags=None;return
        if method.startswith('set_') or method.startswith('subtract_'):
            bits={'word':16,'long':32,'byte':8}.get(method.rsplit('_',1)[1]);
            if bits is None or len(args) not in (2,3):raise CompileError('typed indexed store required')
            dst,extra_dst=self.table_operand(table,(args[0],*args[2:]));src,extra=self.operand(args[1],bits)
            if method.startswith('set_') and src=='#0x0':instruction='clr.'+self.suffix(bits)+' '+dst;size=2+extra_dst
            else:instruction=('sub' if method.startswith('subtract_') else 'move')+'.'+self.suffix(bits)+' '+src+','+dst;size=2+extra+extra_dst
            self.emit(instruction,size,effect);self.last_flags=None;return
        raise CompileError('unsupported memory write')
    def branch(self,test,target,when_true,effect,loop_tail=False):
        if test[0]=='and':
            if when_true:raise CompileError('short-circuit AND requires fallthrough true branch')
            for part in test[1]:self.branch(part,target,False,effect)
            return
        if test==('name','borrowed'):
            if not self.carry_live:raise CompileError('saved Python borrow is no longer the live target carry; unsupported edit refused')
            wide=self.ir.name=='settle_expense';self.emit(('bcs' if when_true else 'bcc')+('.w ' if wide else '.b ')+target,4 if wide else 2,effect);return
        if test[0]!='compare':raise CompileError('typed comparison required')
        op,left,right=test[1:];signed=False
        if left[0]=='call' and left[1]=='signed_word':left=left[2][0];bits=16;signed=True
        elif left[0]=='call' and left[1] in ('low_word','low_byte'):bits=16 if left[1]=='low_word' else 8;left=left[2][0]
        elif left[0]=='name':bits=self.types.get(left[1],0)
        else:raise CompileError('comparison needs a typed local')
        if not bits:raise CompileError('comparison width unknown')
        register=self.reg(left[1]);zero=right[0]=='constant' and right[1]==0
        if signed and not zero:raise CompileError('nonzero signed comparison is outside the supported backend')
        if right[0]=='constant':
            if not 0<=right[1]<(1<<bits):raise CompileError('comparison literal is outside its semantic operand width')
        elif result_width(right,self.types)>bits:raise CompileError('comparison cannot silently truncate its wider right operand')
        if zero:
            reusable=self.last_flags==(left[1],bits) and (signed or loop_tail or self.ir.name=='step_random')
            if not reusable:self.emit('tst.'+self.suffix(bits)+' '+register,2,effect)
            if signed and op in ('Lt','GtE'):true='bmi' if op=='Lt' else 'bpl';false='bpl' if op=='Lt' else 'bmi'
            elif op in ('Eq','NotEq'):true='beq' if op=='Eq' else 'bne';false='bne' if op=='Eq' else 'beq'
            else:raise CompileError('unsupported zero sign comparison')
        else:
            src,extra=self.operand(right,bits);self.emit(('cmpi' if src.startswith('#') else 'cmp')+'.'+self.suffix(bits)+' '+src+','+register,2+extra,effect)
            true={'Eq':'beq','NotEq':'bne','Lt':'bcs','LtE':'bls','Gt':'bhi','GtE':'bcc'}[op]
            false={'Eq':'bne','NotEq':'beq','Lt':'bcc','LtE':'bhi','Gt':'bls','GtE':'bcs'}[op]
        self.emit((true if when_true else false)+'.b '+target,2,effect)
    def block(self,effects,loop=None):
        for index,effect in enumerate(effects):
            op,args=effect.operation,effect.operands
            if op=='declare':
                name,e=args
                if name not in self.regs:raise CompileError('local has no fixed ABI binding')
                self.assign(name,e,effect.width,effect);self.types[name]=effect.width
            elif op=='assign':
                names,e=args
                if len(names)==2 and e[0:2]==('call','subtract_borrow32'):
                    name,flag=names
                    if flag!='borrowed' or e[2][0]!=('name',name):raise CompileError('typed subtraction result and carry required')
                    self.write_guard(name,effect);right,extra=self.operand(e[2][1],32);self.emit('sub.l '+right+','+self.reg(name),2+extra,effect);self.last_flags=None;self.carry_live=True
                elif len(names)==1 and e[0]=='method' and e[2]=='subtract_byte':
                    if names!=('borrowed',):raise CompileError('carry-producing BYTE subtraction must bind the declared bool')
                    self.invoke(e,effect);self.carry_live=True
                elif len(names)==1:self.assign(names[0],e,effect.width,effect);self.types[names[0]]=effect.width
                else:raise CompileError('unsupported multiple result')
            elif op=='invoke':self.invoke(args[0],effect)
            elif op=='return':
                self.validate_return(effect)
                if index!=len(effects)-1:self.emit('bra.b '+self.return_label,2,effect)
                # A single early semantic return is selected directly by its gate.
            elif op=='break':
                if loop is None:raise CompileError('break outside a loop')
                self.emit('bra.b '+loop[1],2,effect)
            elif op=='if':
                test,body,otherwise=args;tail=index==len(effects)-1
                if len(body)==1 and body[0].operation in ('break','return') and not otherwise:
                    if body[0].operation=='return':self.validate_return(body[0])
                    destination=loop[1] if body[0].operation=='break' and loop else self.return_label
                    if tail and loop and body[0].operation=='break':self.branch(test,loop[0],False,effect,True)
                    else:self.branch(test,destination,True,effect)
                else:
                    end=self.fresh();alternative=self.fresh() if otherwise else end
                    direct_loop=tail and loop and not otherwise
                    self.branch(test,loop[0] if direct_loop else alternative,False,effect)
                    self.block(body,loop)
                    if otherwise:self.emit('bra.b '+end,2,effect);self.label(alternative);self.block(otherwise,loop)
                    self.label(end)
            elif op=='loop':
                begin,end=self.fresh(),self.fresh();self.label(begin);body=args[0];self.block(body,(begin,end))
                terminal=(body and body[-1].operation=='if' and len(body[-1].operands[1])==1 and body[-1].operands[1][0].operation=='break')
                if not terminal:self.emit('bra.b '+begin,2,effect)
                self.label(end)
            else:raise CompileError('unknown typed effect')
    def validate_return(self,effect):
        expected=RETURNS.get(self.ir.name);value=effect.operands[0]
        if expected is None:
            if value:raise CompileError('void compatibility operation cannot ignore a Python return value')
        elif not value or value[0]!='name' or self.regs.get(value[1])!=expected[0] or effect.width!=expected[1]:raise CompileError('return expression does not match its actual typed output storage')
    def lower(self):
        if self.ir.name in RETURNS and 'fall' in exits(self.ir.body):raise CompileError('nonvoid semantic function can complete without its actual return value')
        self.lines=['.section .text.'+self.ir.name+',"ax"','.global '+self.ir.name,self.ir.name+':']
        self.block(self.ir.body);self.label(self.return_label)
        self.emit('rts',2,Effect('return',0,(),max(e.source_line for e in self.ir.body)))
        self.lines.extend(('.global '+self.ir.name+'_end',self.ir.name+'_end:'))
        return dict(name=self.ir.name,entry=self.binding.entry,allocated_bytes=self.binding.size,
                    selected_bytes=self.offset,assembly='\n'.join(self.lines)+'\n',mapping=self.mapping)

def compile_python(source):
    ir=semantic_ir(source);registry={f.name:f for f in ir};functions=[Lowerer(f,registry).lower() for f in ir]
    if any(f['allocated_bytes']!=f['selected_bytes'] for f in functions):raise CompileError('ordinary lowering exceeds or shrinks a fixed compatibility allocation')
    # External typed-table symbols stay unresolved until the ordinary linker
    # assigns original data addresses. An assembler-time absolute equate would
    # be mistaken for a large section-relative MC68000 PC displacement.
    preamble='.cpu 68000\n'
    return dict(assembly=preamble+'\n'.join(f['assembly'] for f in functions),functions=functions,
        effects=[asdict(f) for f in ir],original_generation_inputs=False,full_CPU=False,
        complete_ROM=False,general_Python_compiler=False,expected_unique_bytes=sum(b.size for b in BINDINGS))
