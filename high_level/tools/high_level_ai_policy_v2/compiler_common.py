"""Complete typed AI AST admission and ordinary GNU emission from explicit text."""
import ast
import re
from dataclasses import asdict
from .target import BINDINGS,NEW_BINDINGS,REUSED_BINDINGS,BY_NAME,validate_binding

class CompileError(ValueError): pass

def require_declared_names(functions,imported):
    available=set(functions)|imported|{'tuple'}
    for fn in functions.values():
        if fn.type_params: raise CompileError('generic declarations outside fixed ABI')
        local={a.arg for a in fn.args.args}
        local.update(n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store))
        used={n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}
        if used-local-available: raise CompileError('used external names need approved explicit imports')
        if local&imported or fn.name in imported: raise CompileError('typed import shadowing rejected')

def semantic_functions(source,declarations,approved):
    if type(source) is not str or len(source)>300000: raise CompileError('bounded explicit Python text required')
    try: tree=ast.parse(source)
    except (SyntaxError,ValueError) as exc: raise CompileError('invalid business Python') from exc
    functions,imported={},set()
    for node in tree.body:
        if isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and type(node.value.value) is str: continue
        if isinstance(node,ast.ImportFrom):
            allowed=approved.get(node.module,set())
            if node.level!=1 or any(n.asname or n.name not in allowed for n in node.names): raise CompileError('approved explicit semantic imports required')
            imported.update(n.name for n in node.names);continue
        if not isinstance(node,ast.FunctionDef) or node.name not in declarations or node.name in functions: raise CompileError('complete function declarations required')
        if node.type_params or node.decorator_list: raise CompileError('generic/decorated ABI not supported')
        functions[node.name]=node
    if set(functions)!=set(declarations): raise CompileError('all complete business bodies required')
    require_declared_names(functions,imported)
    records={}
    for name,fn in functions.items():
        d=declarations[name]
        expected=ast.parse('def '+name+'('+d['signature']+')->'+d['returns']+':\n'+'\n'.join('    '+s for s in d['flow'].splitlines())).body[0]
        body=list(fn.body)
        if body and isinstance(body[0],ast.Expr) and isinstance(body[0].value,ast.Constant) and type(body[0].value.value) is str: body=body[1:]
        actual=ast.FunctionDef(name=fn.name,args=fn.args,body=body,decorator_list=fn.decorator_list,returns=fn.returns,type_comment=fn.type_comment,type_params=fn.type_params)
        rules={};slots=d.get('slots',{})
        def match(want,have):
            if type(want) is not type(have): raise CompileError(name+': unsupported typed AST/control edit')
            if isinstance(want,ast.Constant) and type(want.value) is int and want.value in slots:
                role,lo,hi=slots[want.value]
                if type(have.value) is not int or not lo<=have.value<=hi: raise CompileError(name+': strict bounded literal required')
                if role in rules and rules[role]!=have.value: raise CompileError(name+': semantic slot must remain consistent')
                rules[role]=have.value;return
            if isinstance(want,ast.AST):
                if want._fields!=have._fields: raise CompileError(name+': unsupported AST schema')
                for f in want._fields: match(getattr(want,f,None),getattr(have,f,None))
            elif type(want) is list:
                if len(want)!=len(have): raise CompileError(name+': complete control/return required')
                for a,b in zip(want,have): match(a,b)
            elif want!=have: raise CompileError(name+': unsupported semantic expression/ABI edit')
        match(expected,actual)
        records[name]=dict(name=name,rules=rules,effects=ast.dump(actual,include_attributes=False))
    return records

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
        self.serial+=1;return self.binding.name+'_'+role+'_'+str(self.serial)
    def ins(self,operation,operands='',width=2):
        if type(operation) is not str or re.fullmatch(r'[a-z]+(?:\.[bwl])?',operation) is None: raise CompileError('ordinary operation required')
        if type(operands) is not str or any(c in operands for c in ('\n',';')): raise CompileError('one ordinary operand statement required')
        if type(width) is not int or width not in (2,4,6,8,10): raise CompileError('strict encoding width required')
        symbol='hl_'+self.binding.name+'_'+str(len(self.mapping))
        self.lines += ['.global '+symbol,symbol+':','    '+operation+(' '+operands if operands else '')]
        self.mapping.append(dict(symbol=symbol,operation=operation,operands=operands,encoding_bytes=width))
    def end(self,*,emit_completion=True):
        if type(emit_completion) is not bool: raise CompileError('strict completion required')
        if emit_completion: self.ins('rts')
        self.lines += ['.global '+self.binding.name+'_end',self.binding.name+'_end:']
    def unit(self,effects): return dict(binding=asdict(self.binding),assembly='\n'.join(self.lines)+'\n',instructions=self.mapping,effects=effects)

def lower_declared(records,bindings,lowerers):
    if set(records)!=set(lowerers) or set(records)!={b.name for b in bindings}: raise CompileError('complete backend family required')
    units=[]
    for b in bindings:
        e=Emitter(b);e.begin();r=records[b.name];lowerers[b.name](e,r['rules']);e.end()
        if e.pc!=b.end: raise CompileError(b.name+': fixed complete extent changed')
        units.append(e.unit(r['effects']))
    return dict(units=units,allocated_bytes=sum(b.end-b.entry for b in bindings),instructions=sum(len(u['instructions']) for u in units),original_generation_input=False,complete_CPU=False)


def _reuse_units(cycle,selection,commit,recruitment,path,campaign,heads,arithmetic):
    """Consume eight explicit accepted source texts; never open old business files."""
    from tools.high_level_diplomacy_forces.compiler_common import _reuse_guard
    _reuse_guard(cycle,True)
    for source in (selection,commit,recruitment,path,campaign,heads,arithmetic):
        _reuse_guard(source)
    from tools.high_level_city_cycle.compiler import compile_python
    from tools.high_level_ai_decision.compiler_selection import compile_selection
    from tools.high_level_ai_decision.compiler_commit import compile_commit
    from tools.high_level_city_officer.compiler_roster import compile_roster
    from tools.high_level_movement_v2.compiler_path import compile_path
    from tools.high_level_movement_v2.compiler_campaign import compile_campaign
    from tools.high_level_diplomacy_forces.compiler_shared import compile_shared
    from tools.high_level_city_event.compiler import compile_arithmetic_units
    units=[]
    for function in compile_python(cycle)['functions']:
        if function['name'] not in ('build_roster','step_random'):
            continue
        binding=BY_NAME[function['name']]
        rows=[]
        for item in function['mapping']:
            operation,_,operands=item['mnemonic'].partition(' ')
            rows.append(dict(symbol=item['symbol'],operation=operation,operands=operands,encoding_bytes=item['size']))
        assembly=re.sub(r'^\.section[^\n]+',f'.org 0x{binding.entry:x}',function['assembly'])
        units.append(dict(binding=asdict(binding),assembly=assembly,instructions=rows,
            effects='explicit accepted cycle semantic text',reused=True))
    families=(compile_selection(selection),compile_commit(commit),compile_roster(recruitment),
        compile_path(path),compile_campaign(campaign),compile_shared(heads))
    wanted={binding.name for binding in REUSED_BINDINGS}
    for family in families:
        for unit in family['units']:
            name=unit['binding']['name']
            if name not in wanted:
                continue
            unit['binding']=asdict(BY_NAME[name]);unit['reused']=True
            units.append(unit)
    numeric=compile_arithmetic_units(arithmetic)
    pieces=re.split(r'(?m)^\.org ',numeric['assembly'])
    body_text={int(piece.splitlines()[0],16):'.org '+piece for piece in pieces[1:]}
    for binding in numeric['bindings']:
        rows=[]
        for item in numeric['mappings'][binding.name]:
            operation,operands=item['mnemonic'],item['operands']
            width=2
            if operation in ('movem.l','movem.w'): width=4
            elif operation in ('cmpi.l','andi.l'): width=6
            elif operation=='move.l' and operands.startswith('#'): width=6
            elif ':w' in operands: width=4
            rows.append(dict(symbol=item['symbol'],operation=operation,operands=operands,encoding_bytes=width))
        units.append(dict(binding=asdict(BY_NAME[binding.name]),assembly=body_text[binding.entry],
            instructions=rows,effects=numeric['effects'][binding.rule],reused=True))
    units.sort(key=lambda unit:unit['binding']['entry'])
    if [unit['binding'] for unit in units]!=[asdict(binding) for binding in REUSED_BINDINGS]:
        raise CompileError('exact thirty-body accepted helper closure required')
    if (sum(sum(row['encoding_bytes'] for row in unit['instructions']) for unit in units),
        sum(len(unit['instructions']) for unit in units))!=(1938,633):
        raise CompileError('exact accepted helper bytes and instruction counts required')
    return units


def compile_modules(economy_source,routes_source,actions_source,reuse_city_cycle,
    reuse_ai_selection,reuse_ai_commit,reuse_recruitment,reuse_path_v2,
    reuse_campaign_v2,reuse_heads,reuse_arithmetic):
    """Fixed, fully consumed semantic family: three new and eight reused texts."""
    texts=(economy_source,routes_source,actions_source,reuse_city_cycle,reuse_ai_selection,
        reuse_ai_commit,reuse_recruitment,reuse_path_v2,reuse_campaign_v2,reuse_heads,reuse_arithmetic)
    if any(type(source) is not str for source in texts):
        raise CompileError('eleven explicit semantic Python texts required')
    from .compiler_economy import compile_economy
    from .compiler_routes import compile_routes
    from .compiler_actions import compile_actions
    families=(compile_economy(economy_source),compile_routes(routes_source),compile_actions(actions_source))
    new=sorted(sum((family['units'] for family in families),[]),key=lambda unit:unit['binding']['entry'])
    if [unit['binding'] for unit in new]!=[asdict(binding) for binding in NEW_BINDINGS]:
        raise CompileError('all116 complete new AI policy bodies required')
    reused=_reuse_units(*texts[3:])
    units=sorted(new+reused,key=lambda unit:unit['binding']['entry'])
    new_bytes=sum(sum(row['encoding_bytes'] for row in unit['instructions']) for unit in new)
    reused_bytes=sum(sum(row['encoding_bytes'] for row in unit['instructions']) for unit in reused)
    instructions=sum(len(unit['instructions']) for unit in units)
    if (new_bytes,reused_bytes,instructions,len(units))!=(7696,1938,2875,146):
        raise CompileError('exact complete AI family allocation/count required')
    return dict(assembly='.cpu 68000\n.text\n.set random_sample,step_random\n'+
        '\n'.join(unit['assembly'] for unit in units),units=units,new_units=new,reused_units=reused,
        allocated_bytes=9634,new_bytes=new_bytes,reused_bytes=reused_bytes,instructions=instructions,
        effects={unit['binding']['name']:unit['effects'] for unit in units},
        original_generation_input=False,complete_CPU=False,complete_ROM=False)

