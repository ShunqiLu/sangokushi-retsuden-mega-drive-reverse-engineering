"""Explicit semantic sources, complete AST admission and ordinary GNU targets."""
import ast
from dataclasses import asdict
import re
from .target import BINDINGS,NEW_BINDINGS,REUSED_BINDINGS,BY_NAME,validate_binding


class CompileError(ValueError): pass


def require_declared_names(functions,imported):
    available=set(functions)|imported|{'tuple'}
    for fn in functions.values():
        if fn.type_params: raise CompileError('generic declarations are outside fixed ABI')
        local={a.arg for a in fn.args.args}
        local.update(n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store))
        used={n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}
        if used-local-available: raise CompileError('used external names require approved explicit imports')
        if local&imported or fn.name in imported: raise CompileError('typed import shadowing is not admitted')


def semantic_functions(source,declarations,approved):
    """Consume every AST field; only named bounded semantic literal slots vary.

Declarations describe supported executable business flows, not target opcode
or source hashes. Unsupported structural edits are rejected rather than ignored.
"""
    if type(source) is not str or len(source)>300000: raise CompileError('bounded explicit Python text required')
    try: tree=ast.parse(source)
    except (SyntaxError,ValueError) as exc: raise CompileError('invalid business Python source') from exc
    functions,imported={},set()
    for node in tree.body:
        if isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and type(node.value.value) is str: continue
        if isinstance(node,ast.ImportFrom):
            allow=approved.get(node.module,set())
            if node.level!=1 or any(n.asname or n.name not in allow for n in node.names):
                raise CompileError('explicit approved semantic imports required')
            imported.update(n.name for n in node.names);continue
        if not isinstance(node,ast.FunctionDef) or node.name not in declarations or node.name in functions:
            raise CompileError('exact complete business function declarations required')
        if node.type_params or node.decorator_list: raise CompileError('generic/decorated ABI not supported')
        functions[node.name]=node
    if set(functions)!=set(declarations): raise CompileError('all complete business bodies required')
    require_declared_names(functions,imported)
    result={}
    for name,fn in functions.items():
        d=declarations[name]
        expected=ast.parse('def '+name+'('+d['signature']+')->'+d['returns']+':\n'+
                           '\n'.join('    '+line for line in d['flow'].splitlines())).body[0]
        body=list(fn.body)
        if body and isinstance(body[0],ast.Expr) and isinstance(body[0].value,ast.Constant) and type(body[0].value.value) is str: body=body[1:]
        actual=ast.FunctionDef(name=fn.name,args=fn.args,body=body,decorator_list=fn.decorator_list,
                              returns=fn.returns,type_comment=fn.type_comment,type_params=fn.type_params)
        rules={};slots=d.get('slots',{})
        def match(want,have):
            if type(want) is not type(have): raise CompileError(name+': unsupported typed AST/control edit')
            if isinstance(want,ast.Constant) and type(want.value) is int and want.value in slots:
                role,minimum,maximum=slots[want.value]
                if type(have.value) is not int or not minimum<=have.value<=maximum: raise CompileError(name+': strict bounded literal required')
                if role in rules and rules[role]!=have.value: raise CompileError(name+': consistent semantic slot required')
                rules[role]=have.value;return
            if isinstance(want,ast.AST):
                if want._fields!=have._fields: raise CompileError(name+': unsupported AST schema')
                for field in want._fields: match(getattr(want,field,None),getattr(have,field,None))
            elif type(want) is list:
                if len(want)!=len(have): raise CompileError(name+': complete control and return structure required')
                for a,b in zip(want,have):match(a,b)
            elif want!=have: raise CompileError(name+': unsupported semantic expression/ABI edit')
        match(expected,actual)
        result[name]=dict(name=name,rules=rules,effects=ast.dump(actual,include_attributes=False))
    return result


class Emitter:
    def __init__(self,binding):
        validate_binding(binding);self.binding,self.lines,self.mapping,self.serial=binding,[],[],0
    @property
    def pc(self): return self.binding.entry+sum(i['encoding_bytes'] for i in self.mapping)
    def begin(self): self.lines += [f'.org 0x{self.binding.entry:x}','.global '+self.binding.name,self.binding.name+':']
    def label(self,name):
        if type(name) is not str or not name.isidentifier(): raise CompileError('strict target label required')
        self.lines.append(name+':')
    def fresh(self,role):
        if type(role) is not str or not role.isidentifier(): raise CompileError('strict label role required')
        self.serial+=1;return f'{self.binding.name}_{role}_{self.serial}'
    def ins(self,operation,operands='',width=2):
        if type(operation) is not str or re.fullmatch(r'[a-z]+(?:\.[bwl])?',operation) is None: raise CompileError('ordinary target operation required')
        if type(operands) is not str or any(c in operands for c in ('\n',';')): raise CompileError('one ordinary operand statement required')
        if type(width) is not int or width not in (2,4,6,8,10): raise CompileError('strict encoding width required')
        symbol=f'hl_{self.binding.name}_{len(self.mapping)}'
        self.lines+=['.global '+symbol,symbol+':','    '+operation+(' '+operands if operands else '')]
        self.mapping.append(dict(symbol=symbol,operation=operation,operands=operands,encoding_bytes=width))
    def end(self,*,emit_completion=True):
        if type(emit_completion) is not bool: raise CompileError('strict completion control required')
        if emit_completion:self.ins('rts')
        self.lines+=['.global '+self.binding.name+'_end',self.binding.name+'_end:']
    def unit(self,effects):
        return dict(binding=asdict(self.binding),assembly='\n'.join(self.lines)+'\n',instructions=self.mapping,effects=effects)


def lower_declared(records,bindings,lowerers):
    if set(records)!=set(lowerers) or set(records)!={b.name for b in bindings}: raise CompileError('complete backend family required')
    units=[]
    for binding in bindings:
        record=records[binding.name];e=Emitter(binding);e.begin();lowerers[binding.name](e,record['rules']);e.end()
        if e.pc!=binding.end: raise CompileError(binding.name+': fixed complete extent changed')
        units.append(e.unit(record['effects']))
    return dict(units=units,allocated_bytes=sum(b.end-b.entry for b in bindings),
                instructions=sum(len(u['instructions']) for u in units),original_generation_input=False,complete_CPU=False)


def _reuse_guard(source,cycle=False):
    if type(source) is not str: raise CompileError('explicit reusable semantic source required')
    try: tree=ast.parse(source)
    except (SyntaxError,ValueError) as exc: raise CompileError('invalid reusable source') from exc
    if cycle:
        # Admit the supplied typed settlement helper family through its actual
        # finite lexical projection first. The native ABI entries retain their
        # original no-return-annotation contract; helper annotations are not
        # unexamined ABI edits. The downstream city compiler still consumes and
        # validates all original effects, controls and caller-provided bodies.
        from tools.high_level_city_cycle.source_inline import inline_settlement_helpers
        try: tree=inline_settlement_helpers(tree)
        except (SyntaxError,ValueError) as exc:
            raise CompileError('invalid reusable cycle helper family') from exc
    functions={fn.name:fn for fn in tree.body if isinstance(fn,ast.FunctionDef)}
    if cycle:
        imports=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom))]
        if (len(imports)!=1 or type(imports[0]) is not ast.ImportFrom or imports[0].level!=1
            or imports[0].module!='domain' or len(imports[0].names)!=1
            or imports[0].names[0].name!='*' or imports[0].names[0].asname is not None):
            raise CompileError('reused cycle needs explicit original semantic domain import')
        # These are the public semantic names exported by the disclosed fixed
        # domain, not an implicit compiler prelude or a read of its source file.
        names={'dataclass','Word','Long','Byte','Table','CityState','integer','unsigned','word','long','byte',
               'low_word','low_byte','signed_word','add16','sub16','add32','sub32','sub8','shl16','shl32',
               'mask16','mask32','clear_low_word','negate32','swap_words','replace_low_word','mulu16','divu16',
               'stitched_product','saturating_add32','subtract_borrow32','minimum32'}
        require_declared_names(functions,names)
    for fn in tree.body:
        if not isinstance(fn,ast.FunctionDef):continue
        if fn.type_params or fn.decorator_list or fn.args.defaults or fn.args.kw_defaults or fn.args.kwonlyargs or fn.args.posonlyargs or fn.args.vararg or fn.args.kwarg:
            raise CompileError('reused fixed ABI cannot ignore generic/default/decorated parameters')
        if cycle and (fn.returns is not None or fn.type_comment): raise CompileError('original cycle frontend has no return annotation edit family')


def _reuse_units(cycle,officer,debt,arrival,complete_city_source):
    for s in (officer,debt,arrival):_reuse_guard(s)
    _reuse_guard(cycle,True)
    from tools.high_level_city_cycle.compiler import compile_python
    from tools.high_level_city_officer.compiler_officer import compile_officer
    from tools.high_level_debt_cleanup.compiler import compile_source
    from tools.high_level_army_groups.compiler_arrival import compile_arrival
    units=[]
    for f in compile_python(cycle)['functions']:
        if f['name'] not in ('build_roster','step_random'):continue
        b=BY_NAME[f['name']];instructions=[]
        for item in f['mapping']:
            operation,_,operands=item['mnemonic'].partition(' ')
            instructions.append(dict(symbol=item['symbol'],operation=operation,operands=operands,encoding_bytes=item['size']))
        text=re.sub(r'^\.section[^\n]+',f'.org 0x{b.entry:x}',f['assembly'])
        units.append(dict(binding=asdict(b),assembly=text,instructions=instructions,effects='explicit accepted cycle semantic source',reused=True))
    for u in compile_officer(officer,complete_city_source=complete_city_source)['units']:
        if u['binding']['name'] in ('owner_head_lookup','mark_c300_list','clear_city_orders','replace_city_assignments'):
            u['binding']=asdict(BY_NAME[u['binding']['name']]);u['reused']=True;units.append(u)
    dc=compile_source(debt)
    pieces=re.split(r'(?m)^\.org ',dc['assembly'])
    sections={int(p.splitlines()[0],16):'.org '+p for p in pieces[1:]}
    for u in dc['units']:
        if u['binding']['name']=='clear_selected_links':
            b=BY_NAME['clear_selected_links'];u['binding']=asdict(b);u['assembly']=sections[b.entry];u['reused']=True;units.append(u)
    for u in compile_arrival(arrival,complete_city_source=complete_city_source)['units']:
        if u['binding']['name']=='apply_returning_officer_loyalty':
            u['binding']=asdict(BY_NAME[u['binding']['name']]);u['reused']=True;units.append(u)
    return sorted(units,key=lambda u:u['binding']['entry'])


def compile_modules(shared_source,stratagem_source,personnel_source,forces_source,
                    reuse_city_cycle,reuse_officer,reuse_debt,reuse_arrival,complete_city_source):
    texts=(shared_source,stratagem_source,personnel_source,forces_source,reuse_city_cycle,reuse_officer,reuse_debt,reuse_arrival,complete_city_source)
    if any(type(s) is not str for s in texts): raise CompileError('eight explicit semantic texts and complete current Scene city source required')
    from .compiler_shared import compile_shared
    from .compiler_stratagem import compile_stratagem
    from .compiler_personnel import compile_personnel
    from .compiler_forces import compile_forces
    parts=(compile_shared(shared_source),compile_stratagem(stratagem_source),compile_personnel(personnel_source),compile_forces(forces_source))
    units=sorted(sum((p['units'] for p in parts),[]),key=lambda u:u['binding']['entry'])
    reused=_reuse_units(reuse_city_cycle,reuse_officer,reuse_debt,reuse_arrival,complete_city_source)
    if [u['binding'] for u in units]!=[asdict(b) for b in NEW_BINDINGS] or [u['binding'] for u in reused]!=[asdict(b) for b in REUSED_BINDINGS]:
        raise CompileError('all56 new and8 reusable complete bodies required')
    all_units=sorted(units+reused,key=lambda u:u['binding']['entry'])
    nb=sum(sum(i['encoding_bytes'] for i in u['instructions']) for u in units)
    rb=sum(sum(i['encoding_bytes'] for i in u['instructions']) for u in reused)
    count=sum(len(u['instructions']) for u in all_units)
    if (nb,rb,count,len(all_units))!=(5492,428,1738,64): raise CompileError('complete64-body allocation/count required')
    return dict(assembly='.cpu 68000\n.text\n.set random_sample,step_random\n'+'\n'.join(u['assembly'] for u in all_units),units=all_units,
                new_units=units,reused_units=reused,allocated_bytes=5920,new_bytes=nb,reused_bytes=rb,instructions=count,
                effects={u['binding']['name']:u['effects'] for u in all_units},original_generation_input=False,
                complete_CPU=False,complete_ROM=False)
