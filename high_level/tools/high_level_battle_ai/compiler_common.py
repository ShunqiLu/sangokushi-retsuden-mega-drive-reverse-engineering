"""Complete typed battle AST admission and ordinary GNU emission from explicit text."""
import ast
import re
from dataclasses import asdict
from .target import BINDINGS,NEW_BINDINGS,REUSED_BINDINGS,BY_NAME,validate_binding

class CompileError(ValueError): pass

def require_declared_names(functions,imported):
    builtins={'tuple','range','type','int','bool','ValueError','str'}
    available=set(functions)|imported|builtins
    for fn in functions.values():
        if fn.type_params: raise CompileError('generic declarations outside fixed ABI')
        local={a.arg for a in fn.args.args}
        local.update(n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store))
        local_imports={a.name for n in ast.walk(fn) if isinstance(n,ast.ImportFrom) for a in n.names}
        local.update(local_imports)
        def loaded_names(node,bound=()):
            if isinstance(node,ast.Lambda):
                parameters={a.arg for a in (*node.args.posonlyargs,*node.args.args,*node.args.kwonlyargs)}
                if node.args.vararg: parameters.add(node.args.vararg.arg)
                if node.args.kwarg: parameters.add(node.args.kwarg.arg)
                if parameters&(imported|builtins): raise CompileError('typed lambda import shadowing rejected')
                return loaded_names(node.args,bound)|loaded_names(node.body,set(bound)|parameters)
            if isinstance(node,ast.Name) and isinstance(node.ctx,ast.Load):
                return set() if node.id in bound else {node.id}
            return set().union(*(loaded_names(child,bound) for child in ast.iter_child_nodes(node)))
        used=loaded_names(fn)
        if used-local-available: raise CompileError('used external names need approved explicit imports')
        if local&(imported|builtins) or fn.name in imported: raise CompileError('typed import shadowing rejected')

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
        for child in ast.walk(node):
            if isinstance(child,ast.ImportFrom):
                allowed=approved.get((child.level,child.module),set())
                if any(a.asname or a.name not in allowed for a in child.names):
                    raise CompileError('approved exact-level named local semantic imports required')
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



def _reuse_rng(cycle_source):
    """Consume explicit accepted logical RNG source, not an old target file."""
    from tools.high_level_diplomacy_forces.compiler_common import _reuse_guard
    from tools.high_level_city_cycle.compiler import compile_python
    _reuse_guard(cycle_source, True)
    functions = [item for item in compile_python(cycle_source)['functions']
                 if item['name'] == 'step_random']
    if len(functions) != 1:
        raise CompileError('one explicit accepted RNG body required')
    function = functions[0]
    binding = BY_NAME['step_random']
    rows = []
    for item in function['mapping']:
        operation, _, operands = item['mnemonic'].partition(' ')
        rows.append(dict(symbol=item['symbol'], operation=operation,
                         operands=operands, encoding_bytes=item['size']))
    assembly = re.sub(r'^\.section[^\n]+', f'.org 0x{binding.entry:x}',
                      function['assembly'])
    if (sum(row['encoding_bytes'] for row in rows), len(rows)) != (38, 15):
        raise CompileError('exact accepted RNG source closure required')
    return dict(binding=asdict(binding), assembly=assembly, instructions=rows,
                effects='explicit accepted logical RNG source', reused=True)


def compile_modules(geometry_source, formation_source, actions_source,
                    reuse_city_cycle):
    """All three new logical families and their one explicit reused source."""
    sources = (geometry_source, formation_source, actions_source, reuse_city_cycle)
    if any(type(source) is not str for source in sources):
        raise CompileError('four explicit logical source strings required')
    from .compiler_geometry import compile_geometry
    from .compiler_formation import compile_formation
    from .compiler_actions import compile_actions
    units = []
    for compile_family, source in zip(
            (compile_geometry, compile_formation, compile_actions), sources[:3]):
        units.extend(compile_family(source)['units'])
    units.append(_reuse_rng(reuse_city_cycle))
    units.sort(key=lambda unit: unit['binding']['entry'])
    if [unit['binding'] for unit in units] != [asdict(binding) for binding in BINDINGS]:
        raise CompileError('exact complete104-body battle AI closure required')
    total_bytes = sum(sum(row['encoding_bytes'] for row in unit['instructions'])
                      for unit in units)
    instructions = sum(len(unit['instructions']) for unit in units)
    if (total_bytes, instructions) != (7108, 2174):
        raise CompileError('exact complete battle AI scope and widths required')
    return dict(units=units,
                assembly='.cpu 68000\n.text\n' + ''.join(unit['assembly'] for unit in units),
                allocated_bytes=7108, instructions=2174,
                new_bytes=7070, reused_bytes=38,
                original_generation_input=False, complete_CPU=False)
