"""Restricted dynamic-flow AST admission and ordinary GNU emission from explicit text."""
import ast
import re
from dataclasses import asdict
from .target import BINDINGS,NEW_BINDINGS,REUSED_BINDINGS,BY_NAME,validate_binding,NEW_BYTES,REUSED_BYTES,TOTAL_BYTES,INSTRUCTIONS

class CompileError(ValueError): pass

def require_declared_names(functions,imported):
    builtins={'tuple','range','type','int','bool','ValueError','sum','min','str','enumerate','max','len','isinstance','abs','all','any','getattr','zip'}
    available=set(functions)|imported|builtins
    for fn in functions.values():
        if fn.type_params: raise CompileError('generic declarations outside fixed ABI')
        local={a.arg for a in ast.walk(fn) if isinstance(a,ast.arg)}
        local.update(n.name for n in ast.walk(fn) if isinstance(n,ast.FunctionDef) and n is not fn)
        local.update(n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store))
        local.update(a.name for n in ast.walk(fn) if isinstance(n,ast.ImportFrom) for a in n.names)
        used={n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}
        if used-local-available: raise CompileError('used external names need approved explicit imports')
        if local&(imported|builtins) or fn.name in imported: raise CompileError('typed import shadowing rejected')

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
            if node.module == '__future__' and node.level == 0 and ([n.name for n in node.names] == ['annotations']):
                continue
            allowed = approved.get((node.level, node.module), approved.get(node.module, set()) if node.level == 1 or (node.level == 0 and node.module == 'dataclasses') else set())
            if (node.level != 1 and (node.level, node.module) not in approved) and (not (node.level == 0 and node.module == 'dataclasses' and ([n.name for n in node.names] == ['replace']))) or any((n.asname or n.name not in allowed for n in node.names)):
                raise CompileError('approved explicit semantic imports required')
            imported.update((n.name for n in node.names))
            continue
        if not isinstance(node, ast.FunctionDef) or node.name not in declarations or node.name in functions:
            raise CompileError('complete function declarations required')
        if node.type_params or node.decorator_list:
            raise CompileError('generic/decorated ABI not supported')
        for child in ast.walk(node):
            if isinstance(child, ast.ImportFrom):
                if (child.level != 1 and (child.level, child.module) not in approved) and (not (child.level == 0 and child.module == 'dataclasses' and ([n.name for n in child.names] == ['replace']))) or any((n.asname or n.name not in approved.get((child.level, child.module), approved.get(child.module, set()) if child.level == 1 or (child.level == 0 and child.module == 'dataclasses') else set()) for n in child.names)):
                    raise CompileError('approved explicit local semantic imports required')
        functions[node.name] = node
    if set(functions) != set(declarations):
        raise CompileError('all complete business bodies required')
    require_declared_names(functions, imported)
    records = {}
    for name, fn in functions.items():
        d = declarations[name]
        expected = ast.parse('def ' + name + '(' + d['signature'] + ')' + ('->' + d['returns'] if d['returns'] else '') + ':\n' + '\n'.join(('    ' + s for s in d['flow'].splitlines()))).body[0]
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

ASSEMBLY_PREFIX='.cpu 68000\n.text\n.set scene_pc_00808a,0x808a\n.set scene_pc_0083d4,0x83d4\n.set scene_pc_00ae8a,0xae8a\n.set scene_pc_026d46,0x26d46\n.set scene_pc_02777a,0x2777a\n.set scene_pc_0277b8,0x277b8\n.set scene_pc_027d76,0x27d76\n.set scene_pc_028228,0x28228\n.set scene_pc_02a22e,0x2a22e\n.set scene_pc_035760,0x35760\n.set scene_pc_03a9b8,0x3a9b8\n.set scene_pc_03b2b0,0x3b2b0\n.set scene_pc_04031c,0x4031c\n.set scene_pc_040cac,0x40cac\n.set scene_pc_040d28,0x40d28\n.set scene_pc_040d76,0x40d76\n.set scene_pc_040d7a,0x40d7a\n.set scene_pc_04115c,0x4115c\n.set scene_pc_0411a2,0x411a2\n.set scene_pc_0414fa,0x414fa\n.set scene_pc_041818,0x41818\n'
EXTERNAL_TARGET_SYMBOLS=[32906, 33748, 44682, 159046, 161658, 161720, 163190, 164392, 172590, 218976, 240056, 242352, 262940, 265388, 265512, 265590, 265594, 266588, 266658, 267514, 268312]

class Emitter:
    """Physical segments and ordinary instructions, not a virtual machine."""
    def __init__(self,binding):
        validate_binding(binding)
        self.binding=binding
        self.instructions=[]
        self.current=None
        self.segment_index=-1

    def segment(self,start,end):
        if self.current is not None and self.current!=self.binding.segments[self.segment_index][1]:
            raise CompileError('complete preceding segment required')
        self.segment_index+=1
        if self.segment_index>=len(self.binding.segments) or (start,end)!=self.binding.segments[self.segment_index]:
            raise CompileError('declared ordered physical segment required')
        self.current=start

    def ins(self,operation,operands='',width=2):
        if type(operation) is not str or re.fullmatch(r'[a-z]+(?:\.[bwl])?',operation) is None:
            raise CompileError('ordinary mnemonic required')
        if type(operands) is not str or any(c in operands for c in ('\n',';')):
            raise CompileError('one ordinary operand expression required')
        if type(width) is not int or width not in (2,4,6,8,10):
            raise CompileError('original instruction width required')
        if self.current is None or self.current+width>self.binding.segments[self.segment_index][1]:
            raise CompileError('instruction outside current physical segment')
        symbol='hl_'+self.binding.name+'_'+str(len(self.instructions))
        self.instructions.append(dict(symbol=symbol,operation=operation,operands=operands,
            encoding_bytes=width,target_PC=self.current,segment_index=self.segment_index))
        self.current+=width

    def unit(self,effects):
        if self.segment_index+1!=len(self.binding.segments) or self.current!=self.binding.segments[-1][1]:
            raise CompileError('all complete physical segments required')
        return dict(binding=asdict(self.binding),instructions=self.instructions,effects=effects)

def lower_declared(records,bindings,lowerers):
    if set(lowerers)!={b.name for b in bindings} or not set(lowerers)<=set(records):
        raise CompileError('complete physical lowerer coverage required')
    units=[]
    for binding in bindings:
        emitter=Emitter(binding)
        lowerers[binding.name](emitter,records[binding.name]['rules'])
        units.append(emitter.unit(records[binding.name]['effects']))
    return dict(units=units,original_generation_input=False,whole_closed_workflow=False)

def render_physical(units):
    """Interleaved components are emitted in actual PC order, never by entry."""
    instructions=sorted((row for unit in units for row in unit['instructions']),key=lambda r:r['target_PC'])
    if len({row['target_PC'] for row in instructions})!=len(instructions):
        raise CompileError('one instruction authority per physical PC required')
    beginnings,ends,entries={},{},{}
    for binding in BINDINGS:
        for index,(start,end) in enumerate(binding.segments):
            beginnings.setdefault(start,[]).append(binding.name+'_segment_'+str(index))
            ends.setdefault(end,[]).append(binding.name+'_segment_'+str(index)+'_end')
        for pc,name in binding.entries:
            entries.setdefault(pc,[]).append(name)
    lines=[ASSEMBLY_PREFIX]
    previous=None
    def labels(names):
        for name in names:lines.extend(('.global '+name,name+':'))
    for row in instructions:
        pc=row['target_PC']
        if previous is not None:
            labels(ends.get(previous,()))
        if previous!=pc:lines.append('.org 0x'+format(pc,'x'))
        labels(beginnings.get(pc,()))
        labels(entries.get(pc,()))
        labels(('scene_pc_'+format(pc,'06x'),row['symbol']))
        lines.append('    '+row['operation']+(' '+row['operands'] if row['operands'] else ''))
        previous=pc+row['encoding_bytes']
    if previous is not None:labels(ends.get(previous,()))
    return '\n'.join(lines)+'\n'

def compile_modules(duel_source,actions_source,early_phase_source,late_phase_source):
    from .compiler_duel import compile_duel
    from .compiler_actions import compile_actions
    from .compiler_early_phase import compile_early_phase
    from .compiler_late_phase import compile_late_phase
    sources=(duel_source,actions_source,early_phase_source,late_phase_source)
    if any(type(source) is not str for source in sources):
        raise CompileError('four explicit logical business texts required')
    units=[]
    for compiler,source in zip((compile_duel,compile_actions,compile_early_phase,compile_late_phase),sources):
        units.extend(compiler(source)['units'])
    units.sort(key=lambda u:u['binding']['entry'])
    if [u['binding'] for u in units]!=[asdict(b) for b in BINDINGS]:
        raise CompileError('complete disjoint target bindings required')
    count=sum(len(u['instructions']) for u in units)
    total=sum(row['encoding_bytes'] for u in units for row in u['instructions'])
    if count!=INSTRUCTIONS or total!=TOTAL_BYTES:
        raise CompileError('complete target instruction/physical byte scope required')
    return dict(units=units,assembly=render_physical(units),allocated_bytes=total,
        instructions=count,new_bytes=NEW_BYTES,reused_bytes=REUSED_BYTES,
        original_generation_input=False,opaque_opcode_payload=False,
        complete_CPU=False,whole_closed_workflow=False,
        external_target_symbols=EXTERNAL_TARGET_SYMBOLS)
