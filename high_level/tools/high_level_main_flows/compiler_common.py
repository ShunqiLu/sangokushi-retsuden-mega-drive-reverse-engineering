"""Restricted main-workflow AST admission and ordinary GNU emission from explicit text."""
import ast
import re
from dataclasses import asdict
from .target import BINDINGS,NEW_BINDINGS,REUSED_BINDINGS,BY_NAME,validate_binding,NEW_BYTES,REUSED_BYTES,TOTAL_BYTES,INSTRUCTIONS

class CompileError(ValueError): pass

def approved_import(node, approved):
    """Cross-family imports need an exact (relative level, module) authority.

    Legacy single-package imports keep their old names. A matching leaf module
    name alone never authorizes an import from another package.
    """
    if node.level == 0 and node.module == 'dataclasses':
        return [alias.name for alias in node.names] == ['replace'] and not any(alias.asname for alias in node.names)
    key = node.module if node.level == 1 else (node.level, node.module)
    return node.level >= 1 and all(not alias.asname and alias.name in approved.get(key, set()) for alias in node.names)

def require_declared_names(functions,imported):
    builtins={'tuple','range','type','int','bool','ValueError','sum','min','str','enumerate','max','len','isinstance','abs','all','any','getattr','zip','divmod'}
    available=set(functions)|imported|builtins
    for fn in functions.values():
        if fn.type_params: raise CompileError('generic declarations outside fixed ABI')
        local={a.arg for a in ast.walk(fn) if isinstance(a,ast.arg)}
        local.update(n.name for n in ast.walk(fn) if isinstance(n,ast.FunctionDef) and n is not fn)
        local.update(n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store))
        local_imports={a.name for n in ast.walk(fn) if isinstance(n,ast.ImportFrom) for a in n.names}
        assigned=set(local)
        local.update(local_imports)
        used={n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}
        if used-local-available: raise CompileError(fn.name+': undeclared names '+repr(sorted(used-local-available)))
        if assigned&(imported|builtins|local_imports) or fn.name in imported: raise CompileError(fn.name+': typed import shadowing '+repr(sorted(assigned&(imported|builtins|local_imports))))

def semantic_functions(source,declarations,approved):
    if type(source) is not str or len(source)>800000: raise CompileError('bounded explicit Python text required')
    try: tree=ast.parse(source)
    except (SyntaxError,ValueError) as exc: raise CompileError('invalid business Python') from exc
    functions,imported={},set()
    for node in tree.body:
        if isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and type(node.value.value) is str: continue
        if isinstance(node,ast.ImportFrom):
            if node.module=='__future__' and node.level==0 and [n.name for n in node.names]==['annotations']: continue
            if not approved_import(node,approved): raise CompileError('approved explicit semantic imports required')
            imported.update(n.name for n in node.names);continue
        if not isinstance(node,ast.FunctionDef) or node.name not in declarations or node.name in functions: raise CompileError('complete function declarations required')
        if node.type_params or node.decorator_list: raise CompileError('generic/decorated ABI not supported')
        for child in ast.walk(node):
            if isinstance(child,ast.ImportFrom):
                if not approved_import(child,approved):
                    raise CompileError('approved explicit local semantic imports required')
        functions[node.name]=node
    if set(functions)!=set(declarations): raise CompileError('all complete business bodies required')
    require_declared_names(functions,imported)
    records={}
    for name,fn in functions.items():
        d=declarations[name]
        expected=ast.parse('def '+name+'('+d['signature']+')'+('->'+d['returns'] if d['returns'] else '')+':\n'+'\n'.join('    '+s for s in d['flow'].splitlines())).body[0]
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

ASSEMBLY_PREFIX='.cpu 68000\n.text\n.set main_pc_00060c,0x60c\n.set main_pc_000dc0,0xdc0\n.set main_pc_004a16,0x4a16\n.set main_pc_005f48,0x5f48\n.set main_pc_006518,0x6518\n.set main_pc_006826,0x6826\n.set main_pc_0068ce,0x68ce\n.set main_pc_00808a,0x808a\n.set main_pc_008112,0x8112\n.set main_pc_0083c8,0x83c8\n.set main_pc_0083d4,0x83d4\n.set main_pc_0083fa,0x83fa\n.set main_pc_00ac08,0xac08\n.set main_pc_00ac10,0xac10\n.set main_pc_00ac28,0xac28\n.set main_pc_00ad06,0xad06\n.set main_pc_00ad1c,0xad1c\n.set main_pc_00adfc,0xadfc\n.set main_pc_00ae8a,0xae8a\n.set main_pc_00af04,0xaf04\n.set main_pc_00af1e,0xaf1e\n.set main_pc_00af48,0xaf48\n.set main_pc_00dea6,0xdea6\n.set main_pc_00e82e,0xe82e\n.set main_pc_00e8a0,0xe8a0\n.set main_pc_01072c,0x1072c\n.set main_pc_011c8c,0x11c8c\n.set main_pc_011cca,0x11cca\n.set main_pc_011cf2,0x11cf2\n.set main_pc_011e3c,0x11e3c\n.set main_pc_01270a,0x1270a\n.set main_pc_0135c4,0x135c4\n.set main_pc_0136f4,0x136f4\n.set main_pc_01374a,0x1374a\n.set main_pc_014294,0x14294\n.set main_pc_014574,0x14574\n.set main_pc_016acc,0x16acc\n.set main_pc_016b3a,0x16b3a\n.set main_pc_017602,0x17602\n.set main_pc_0177be,0x177be\n.set main_pc_017c8a,0x17c8a\n.set main_pc_017f30,0x17f30\n.set main_pc_0183f8,0x183f8\n.set main_pc_01a438,0x1a438\n.set main_pc_01a44e,0x1a44e\n.set main_pc_01bfec,0x1bfec\n.set main_pc_0235cc,0x235cc\n.set main_pc_024af2,0x24af2\n.set main_pc_024b00,0x24b00\n.set main_pc_02536a,0x2536a\n.set main_pc_02540e,0x2540e\n.set main_pc_025c02,0x25c02\n.set main_pc_025c2a,0x25c2a\n.set main_pc_025c9c,0x25c9c\n.set main_pc_025cb8,0x25cb8\n.set main_pc_025cbe,0x25cbe\n.set main_pc_025d96,0x25d96\n.set main_pc_025d9c,0x25d9c\n.set main_pc_025df8,0x25df8\n.set main_pc_025f0a,0x25f0a\n.set main_pc_025f28,0x25f28\n.set main_pc_0260e4,0x260e4\n.set main_pc_026bfa,0x26bfa\n.set main_pc_03080e,0x3080e\n.set main_pc_030a74,0x30a74\n.set main_pc_034f36,0x34f36\n.set main_pc_03aa20,0x3aa20\n.set main_pc_03aa8a,0x3aa8a\n.set main_pc_03aace,0x3aace\n.set main_pc_03aad6,0x3aad6\n.set main_pc_03aada,0x3aada\n.set main_pc_03ab52,0x3ab52\n.set main_pc_03ab94,0x3ab94\n.set main_pc_041d3c,0x41d3c\n.set main_pc_041d7a,0x41d7a\n.set main_pc_0661d4,0x661d4\n.set main_pc_066616,0x66616\n.set main_pc_0676f2,0x676f2\n'
EXTERNAL_TARGET_SYMBOLS=[1548, 3520, 18966, 24392, 25880, 26662, 26830, 32906, 33042, 33736, 33748, 33786, 44040, 44048, 44072, 44294, 44316, 44540, 44682, 44804, 44830, 44872, 56998, 59438, 59552, 67372, 72844, 72906, 72946, 73276, 75530, 79300, 79604, 79690, 82580, 83316, 92876, 92986, 95746, 96190, 97418, 98096, 99320, 107576, 107598, 114668, 144844, 150258, 150272, 152426, 152590, 154626, 154666, 154780, 154808, 154814, 155030, 155036, 155128, 155402, 155432, 155876, 158714, 198670, 199284, 216886, 240160, 240266, 240334, 240342, 240346, 240466, 240532, 269628, 269690, 418260, 419350, 423666]

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
        labels(('main_pc_'+format(pc,'06x'),row['symbol']))
        lines.append('    '+row['operation']+(' '+row['operands'] if row['operands'] else ''))
        previous=pc+row['encoding_bytes']
    if previous is not None:labels(ends.get(previous,()))
    return '\n'.join(lines)+'\n'

def compile_modules(sources):
    from importlib import import_module
    from .target import MODULE_ROLES
    if type(sources) is not dict or set(sources)!=set(MODULE_ROLES) or any(type(v) is not str for v in sources.values()):
        raise CompileError('all declared business modules as explicit texts required')
    units=[]
    for name in MODULE_ROLES:
        compiler=import_module('.compiler_'+name.removeprefix('business_'),__package__)
        units.extend(compiler.compile_source(sources[name])['units'])
    units.sort(key=lambda unit:unit['binding']['entry'])
    if [unit['binding'] for unit in units]!=[asdict(binding) for binding in BINDINGS]:
        raise CompileError('complete disjoint source authority required')
    count=sum(len(unit['instructions']) for unit in units)
    total=sum(row['encoding_bytes'] for unit in units for row in unit['instructions'])
    if count!=INSTRUCTIONS or total!=TOTAL_BYTES:
        raise CompileError('complete physical instruction scope required')
    return dict(units=units,assembly=render_physical(units),allocated_bytes=total,
        instructions=count,new_bytes=NEW_BYTES,reused_bytes=REUSED_BYTES,
        original_generation_input=False,opaque_opcode_payload=False,
        complete_CPU=False,whole_closed_workflow=False,external_target_symbols=EXTERNAL_TARGET_SYMBOLS)
