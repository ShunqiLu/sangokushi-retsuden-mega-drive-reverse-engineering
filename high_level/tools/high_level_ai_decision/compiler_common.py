"""Shared ordinary emitter and explicit semantic-only whole-scope composition."""
import ast
from dataclasses import asdict
import re
from .target import BINDINGS, NEW_BINDINGS, REUSED_BINDINGS, validate_binding


class CompileError(ValueError):
    pass


def require_declared_names(functions, imported_names):
    if type(functions) is not dict or type(imported_names) is not set or any(type(n) is not str for n in imported_names):
        raise CompileError('explicit current declaration/import names required')
    available = set(functions)|imported_names|{'tuple'}
    for function in functions.values():
        locals_ = {a.arg for a in function.args.args}
        locals_.update(n.id for n in ast.walk(function) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store))
        used = {n.id for n in ast.walk(function) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}
        missing = used-locals_-available
        if missing: raise CompileError('used external name lacks explicit approved import/declaration: '+','.join(sorted(missing)))


class Emitter:
    def __init__(self, binding):
        validate_binding(binding)
        self.binding,self.lines,self.mapping,self.serial = binding,[],[],0
    def begin(self):
        self.lines += [f'.org 0x{self.binding.entry:x}', '.global '+self.binding.name, self.binding.name+':']
    def label(self, name):
        if type(name) is not str or not name.isidentifier(): raise CompileError('strict target label required')
        self.lines.append(name+':')
    def fresh(self, role):
        if type(role) is not str or not role.isidentifier(): raise CompileError('strict target label role required')
        self.serial += 1
        return f'{self.binding.name}_{role}_{self.serial}'
    def ins(self, operation, operands='', width=2):
        if type(operation) is not str or type(operands) is not str or type(width) is not int or width not in (2,4,6,8,10):
            raise CompileError('strict ordinary operation/encoding width required')
        if not operation or any(c in operation for c in ('\n',';','.byte','.word','.incbin')) or '\n' in operands or ';' in operands:
            raise CompileError('one ordinary target instruction required')
        symbol=f'hl_{self.binding.name}_{len(self.mapping)}'
        self.lines += ['.global '+symbol,symbol+':','    '+operation+(' '+operands if operands else '')]
        self.mapping.append(dict(symbol=symbol,operation=operation,operands=operands,encoding_bytes=width))
    def end(self, *, emit_completion=True):
        if emit_completion:self.ins('rts')
        self.lines += ['.global '+self.binding.name+'_end',self.binding.name+'_end:']
    def unit(self, effects):
        return dict(binding=asdict(self.binding),assembly='\n'.join(self.lines)+'\n',instructions=self.mapping,effects=effects)


def compile_modules(selection_source, policy_source, officer_source, commit_source, helper_source):
    if any(type(text) is not str for text in (selection_source,policy_source,officer_source,commit_source,helper_source)):
        raise CompileError('five explicitly supplied semantic source texts required')
    from .compiler_selection import compile_selection
    from .compiler_policy import compile_policy
    from .compiler_officer import compile_officer
    from .compiler_commit import compile_commit
    from tools.high_level_city_event.compiler import compile_arithmetic_units
    halves=(compile_selection(selection_source),compile_policy(policy_source),compile_officer(officer_source),compile_commit(commit_source))
    units=sorted(sum((h['units'] for h in halves),[]),key=lambda u:u['binding']['entry'])
    if [u['binding'] for u in units]!=[asdict(b) for b in NEW_BINDINGS]:raise CompileError('all29 complete new AI bodies required')
    shared=compile_arithmetic_units(helper_source,selected=tuple(b.name for b in REUSED_BINDINGS))
    pieces=re.split(r'(?m)^\.org ',shared['assembly'])
    helper_parts={int(p.splitlines()[0],16):'.org '+p for p in pieces[1:]}
    reused=[]
    for binding in shared['bindings']:
        mappings=[]
        for item in shared['mappings'][binding.name]:
            operation,operands=item['mnemonic'],item['operands']
            width=2
            if operation in ('movem.l','movem.w'):width=4
            elif operation in ('cmpi.l','andi.l'):width=6
            elif operation=='move.l' and operands.startswith('#'):width=6
            elif ':w' in operands:width=4
            mappings.append(dict(symbol=item['symbol'],operation=operation,operands=operands,encoding_bytes=width))
        reused.append(dict(binding=dict(name=binding.name,entry=binding.entry,end=binding.end,completion='return'),
            assembly=helper_parts[binding.entry],instructions=mappings,effects=shared['effects'][binding.rule],reused=True))
    all_units=sorted(units+reused,key=lambda u:u['binding']['entry'])
    if [u['binding'] for u in all_units]!=[asdict(b) for b in BINDINGS]:raise CompileError('complete34 bodies including5 helper bindings required')
    new_bytes=sum(sum(i['encoding_bytes'] for i in u['instructions']) for u in units)
    reused_bytes=sum(sum(i['encoding_bytes'] for i in u['instructions']) for u in reused)
    instructions=sum(len(u['instructions']) for u in all_units)
    if (new_bytes,reused_bytes,instructions)!=(2036,190,696):raise CompileError('complete original code allocation/count required')
    return dict(assembly=pieces[0]+'\n'.join(u['assembly'] for u in all_units),units=all_units,new_units=units,reused_units=reused,
        allocated_bytes=2226,new_bytes=2036,reused_bytes=190,instructions=instructions,
        effects={u['binding']['name']:u['effects'] for u in all_units},
        original_generation_input=False,complete_CPU=False,complete_ROM=False)
