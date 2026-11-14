"""Ordinary target emitter and pure explicit composition of three semantic texts."""
import ast
from dataclasses import asdict
import re
from .target import BINDINGS,validate_binding


class CompileError(ValueError):
    pass


def require_declared_names(functions, imported_names):
    available=set(functions)|imported_names|{'tuple'}
    for fn in functions.values():
        if fn.type_params: raise CompileError('generic declarations are outside fixed ABI')
        local={a.arg for a in fn.args.args}
        local.update(n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store))
        used={n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}
        missing=used-local-available
        if missing: raise CompileError('used external name requires declared approved import: '+','.join(sorted(missing)))
        if local&imported_names or fn.name in imported_names: raise CompileError('typed import cannot be shadowed')


class Emitter:
    def __init__(self,binding):
        validate_binding(binding);self.binding,self.lines,self.mapping,self.serial=binding,[],[],0
    @property
    def pc(self): return self.binding.entry+sum(item['encoding_bytes'] for item in self.mapping)
    def begin(self): self.lines += [f'.org 0x{self.binding.entry:x}','.global '+self.binding.name,self.binding.name+':']
    def label(self,name):
        if type(name) is not str or not name.isidentifier(): raise CompileError('strict label required')
        self.lines.append(name+':')
    def fresh(self,role):
        if type(role) is not str or not role.isidentifier(): raise CompileError('strict label role required')
        self.serial+=1;return f'{self.binding.name}_{role}_{self.serial}'
    def ins(self,operation,operands='',width=2):
        if type(operation) is not str or re.fullmatch(r'[a-z]+(?:\.[bwl])?',operation) is None:
            raise CompileError('ordinary target operation required')
        if type(operands) is not str or any(c in operands for c in ('\n',';')):
            raise CompileError('one ordinary operand statement required')
        if type(width) is not int or width not in (2,4,6,8,10): raise CompileError('strict encoding width required')
        symbol=f'hl_{self.binding.name}_{len(self.mapping)}'
        self.lines += ['.global '+symbol,symbol+':','    '+operation+(' '+operands if operands else '')]
        self.mapping.append(dict(symbol=symbol,operation=operation,operands=operands,encoding_bytes=width))
    def end(self,*,emit_completion=True):
        if type(emit_completion) is not bool: raise CompileError('strict completion control required')
        if emit_completion: self.ins('rts')
        self.lines += ['.global '+self.binding.name+'_end',self.binding.name+'_end:']
    def unit(self,effects):
        return dict(binding=asdict(self.binding),assembly='\n'.join(self.lines)+'\n',instructions=self.mapping,effects=effects)


def compile_modules(city_source,officer_source,roster_source,complete_city_source):
    if any(type(s) is not str for s in (city_source,officer_source,roster_source,complete_city_source)):
        raise CompileError('three explicit semantic texts and complete current Scene city source required')
    from .compiler_city import compile_city
    from .compiler_officer import compile_officer
    from .compiler_roster import compile_roster
    pieces=(compile_city(city_source),compile_officer(officer_source,complete_city_source=complete_city_source),compile_roster(roster_source))
    units=sorted(sum((p['units'] for p in pieces),[]),key=lambda u:u['binding']['entry'])
    if [u['binding'] for u in units]!=[asdict(b) for b in BINDINGS]: raise CompileError('all46 complete business bodies required')
    allocated=sum(sum(i['encoding_bytes'] for i in u['instructions']) for u in units)
    count=sum(len(u['instructions']) for u in units)
    if (allocated,count)!=(2896,824): raise CompileError('complete original46-unit allocation required')
    assembly='.cpu 68000\n.text\n'+'\n'.join(u['assembly'] for u in units)
    return dict(assembly=assembly,units=units,new_units=units,reused_units=[],allocated_bytes=allocated,
        new_bytes=allocated,reused_bytes=0,instructions=count,effects={u['binding']['name']:u['effects'] for u in units},
        original_generation_input=False,complete_CPU=False,complete_ROM=False)
