"""Complete typed AST admission and ordinary GNU targets from explicit text."""
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

def semantic_functions(source, declarations, approved):
    if type(source) is not str or len(source) > 300000:
        raise CompileError('bounded explicit Python text required')
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError) as exc:
        raise CompileError('invalid business Python') from exc
    functions, imported = ({}, set())
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and (type(node.value.value) is str):
            continue
        if isinstance(node, ast.ImportFrom):
            import_key = node.module if node.level == 1 else (node.level, node.module)
            allowed = approved.get(import_key, set())
            if node.level not in (1, 2) or any((n.asname or n.name not in allowed for n in node.names)):
                raise CompileError('approved explicit semantic imports required')
            imported.update((n.name for n in node.names))
            continue
        if not isinstance(node, ast.FunctionDef) or node.name not in declarations or node.name in functions:
            raise CompileError('complete function declarations required')
        if node.type_params or node.decorator_list:
            raise CompileError('generic/decorated ABI not supported')
        functions[node.name] = node
    if set(functions) != set(declarations):
        raise CompileError('all complete business bodies required')
    require_declared_names(functions, imported)
    records = {}
    for name, fn in functions.items():
        d = declarations[name]
        expected = ast.parse('def ' + name + '(' + d['signature'] + ')->' + d['returns'] + ':\n' + '\n'.join(('    ' + s for s in d['flow'].splitlines()))).body[0]
        body = list(fn.body)
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and (type(body[0].value.value) is str):
            body = body[1:]
        actual = ast.FunctionDef(name=fn.name, args=fn.args, body=body, decorator_list=fn.decorator_list, returns=fn.returns, type_comment=fn.type_comment, type_params=fn.type_params)
        rules = {}
        slots = d.get('slots', {})

        def match(want, have):
            if type(want) is not type(have):
                raise CompileError(name + ': unsupported typed AST/control edit')
            if isinstance(want, ast.Constant) and type(want.value) is int and (want.value in slots):
                role, lo, hi = slots[want.value]
                if type(have.value) is not int or not lo <= have.value <= hi:
                    raise CompileError(name + ': strict bounded literal required')
                if role in rules and rules[role] != have.value:
                    raise CompileError(name + ': semantic slot must remain consistent')
                rules[role] = have.value
                return
            if isinstance(want, ast.AST):
                if want._fields != have._fields:
                    raise CompileError(name + ': unsupported AST schema')
                for f in want._fields:
                    match(getattr(want, f, None), getattr(have, f, None))
            elif type(want) is list:
                if len(want) != len(have):
                    raise CompileError(name + ': complete control/return required')
                for a, b in zip(want, have):
                    match(a, b)
            elif want != have:
                raise CompileError(name + ': unsupported semantic expression/ABI edit')
        match(expected, actual)
        records[name] = dict(name=name, rules=rules, effects=ast.dump(actual, include_attributes=False))
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

def _reuse_units(cycle,shared,resources):
    # The disclosed accepted pure frontends consume explicit source arguments;
    # this combination guard closes their old annotation/import blind spots.
    from tools.high_level_diplomacy_forces.compiler_common import _reuse_guard
    _reuse_guard(cycle,True);_reuse_guard(shared);_reuse_guard(resources)
    from tools.high_level_city_cycle.compiler import compile_python
    from tools.high_level_diplomacy_forces.compiler_shared import compile_shared
    from tools.high_level_city_officer.compiler_city import compile_city
    units=[]
    for f in compile_python(cycle)['functions']:
        if f['name'] not in ('build_roster','step_random'):continue
        b=BY_NAME[f['name']];items=[]
        for row in f['mapping']:
            operation,_,operands=row['mnemonic'].partition(' ')
            items.append(dict(symbol=row['symbol'],operation=operation,operands=operands,encoding_bytes=row['size']))
        text=re.sub(r'^\.section[^\n]+',f'.org 0x{b.entry:x}',f['assembly'])
        units.append(dict(binding=asdict(b),assembly=text,instructions=items,effects='explicit accepted cycle semantic source',reused=True))
    for result in (compile_shared(shared),compile_city(resources)):
        for u in result['units']:
            if u['binding']['name'] in ('choose_city_head','roster_contains_force_head_carry','add_packet_city_resources','add_packet_city_resources_wrapped'):
                u['binding']=asdict(BY_NAME[u['binding']['name']]);u['reused']=True;units.append(u)
    return sorted(units,key=lambda u:u['binding']['entry'])

def compile_modules(path_source,arrival_source,campaign_source,reuse_cycle,reuse_shared,reuse_resources):
    if any(type(s) is not str for s in (path_source,arrival_source,campaign_source,reuse_cycle,reuse_shared,reuse_resources)):
        raise CompileError('six explicit semantic source texts required')
    from .compiler_path import compile_path
    from .compiler_arrival import compile_arrival
    from .compiler_campaign import compile_campaign
    parts=(compile_path(path_source),compile_arrival(arrival_source),compile_campaign(campaign_source))
    units=sorted(sum((p['units'] for p in parts),[]),key=lambda u:u['binding']['entry'])
    reused=_reuse_units(reuse_cycle,reuse_shared,reuse_resources)
    if [u['binding'] for u in units]!=[asdict(b) for b in NEW_BINDINGS] or [u['binding'] for u in reused]!=[asdict(b) for b in REUSED_BINDINGS]:
        raise CompileError('all38new and6reused complete bodies required')
    all_units=sorted(units+reused,key=lambda u:u['binding']['entry'])
    nb=sum(sum(i['encoding_bytes'] for i in u['instructions']) for u in units)
    rb=sum(sum(i['encoding_bytes'] for i in u['instructions']) for u in reused)
    count=sum(len(u['instructions']) for u in all_units)
    if (nb,rb,count,len(all_units))!=(3394,476,1206,44): raise CompileError('complete allocation/count required')
    return dict(assembly='.cpu 68000\n.text\n'+'\n'.join(u['assembly'] for u in all_units),units=all_units,new_units=units,reused_units=reused,allocated_bytes=3870,new_bytes=nb,reused_bytes=rb,instructions=count,effects={u['binding']['name']:u['effects'] for u in all_units},original_generation_input=False,complete_CPU=False,complete_ROM=False)
