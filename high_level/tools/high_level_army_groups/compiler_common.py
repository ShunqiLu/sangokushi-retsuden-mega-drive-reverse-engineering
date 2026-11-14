"""Pure explicit semantic-source composition and ordinary target emission."""
import ast
from dataclasses import asdict
import re
from .target import BINDINGS,NEW_BINDINGS,REUSED_BINDINGS,validate_binding


class CompileError(ValueError): pass


def require_declared_names(functions,imported_names):
    if type(functions) is not dict or type(imported_names) is not set or any(type(n) is not str for n in imported_names):
        raise CompileError('explicit declaration/import names required')
    available=set(functions)|imported_names|{'tuple'}
    for fn in functions.values():
        if fn.type_params: raise CompileError('generic declarations are outside fixed ABI')
        local={a.arg for a in fn.args.args}
        local.update(n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store))
        used={n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}
        if used-local-available: raise CompileError('used external names require explicit approved imports')
        if local&imported_names or fn.name in imported_names: raise CompileError('typed import cannot be shadowed')


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
        if type(role) is not str or not role.isidentifier(): raise CompileError('strict target label role required')
        self.serial+=1;return f'{self.binding.name}_{role}_{self.serial}'
    def ins(self,operation,operands='',width=2):
        if type(operation) is not str or re.fullmatch(r'[a-z]+(?:\.[bwl])?',operation) is None: raise CompileError('ordinary operation required')
        if type(operands) is not str or any(c in operands for c in ('\n',';')): raise CompileError('one ordinary operand statement required')
        if type(width) is not int or width not in (2,4,6,8,10): raise CompileError('strict encoding width required')
        symbol=f'hl_{self.binding.name}_{len(self.mapping)}'
        self.lines+=['.global '+symbol,symbol+':','    '+operation+(' '+operands if operands else '')]
        self.mapping.append(dict(symbol=symbol,operation=operation,operands=operands,encoding_bytes=width))
    def end(self,*,emit_completion=True):
        if type(emit_completion) is not bool: raise CompileError('strict completion control required')
        if emit_completion: self.ins('rts')
        self.lines+=['.global '+self.binding.name+'_end',self.binding.name+'_end:']
    def unit(self,effects):
        return dict(binding=asdict(self.binding),assembly='\n'.join(self.lines)+'\n',instructions=self.mapping,effects=effects)


def _rng_unit(source):
    from tools.high_level_city_event.compiler import compile_arithmetic_units
    compiled=compile_arithmetic_units(source,selected=('random_sample',))
    binding=compiled['bindings'][0]
    pieces=re.split(r'(?m)^\.org ',compiled['assembly'])
    parts={int(p.splitlines()[0],16):'.org '+p for p in pieces[1:]}
    instructions=[]
    for item in compiled['mappings'][binding.name]:
        op,args=item['mnemonic'],item['operands'];width=2
        if op=='move.l' and args.startswith('#'): width=6
        elif ':w' in args: width=4
        instructions.append(dict(symbol=item['symbol'],operation=op,operands=args,encoding_bytes=width))
    return dict(binding=asdict(REUSED_BINDINGS[0]),assembly=parts[binding.entry],instructions=instructions,
                effects=compiled['effects'][binding.rule],reused=True)


def compile_modules(disposition_source,members_source,arrival_source,rng_source,terrain_source,complete_city_source):
    if any(type(s) is not str for s in (disposition_source,members_source,arrival_source,rng_source,terrain_source,complete_city_source)):
        raise CompileError('six explicit semantic source texts required, including complete current Scene source')
    from .compiler_disposition import compile_disposition
    from .compiler_members import compile_members
    from .compiler_arrival import compile_arrival
    from tools.high_level_city_officer.compiler_officer import compile_officer
    parts=(compile_disposition(disposition_source),compile_members(members_source),
        compile_arrival(arrival_source,complete_city_source=complete_city_source))
    units=sorted(sum((p['units'] for p in parts),[]),key=lambda u:u['binding']['entry'])
    if [u['binding'] for u in units]!=[asdict(b) for b in NEW_BINDINGS]: raise CompileError('all25 new complete business bodies required')
    terrain=[u for u in compile_officer(terrain_source,complete_city_source=complete_city_source)['units']
        if u['binding']['name']=='terrain_cell_query']
    if len(terrain)!=1: raise CompileError('one explicit accepted terrain semantic function required')
    terrain[0]['reused']=True
    reused=[_rng_unit(rng_source),terrain[0]]
    all_units=sorted(units+reused,key=lambda u:u['binding']['entry'])
    if [u['binding'] for u in all_units]!=[asdict(b) for b in BINDINGS]: raise CompileError('complete27-body allocation required')
    new_bytes=sum(sum(i['encoding_bytes'] for i in u['instructions']) for u in units)
    reused_bytes=sum(sum(i['encoding_bytes'] for i in u['instructions']) for u in reused)
    count=sum(len(u['instructions']) for u in all_units)
    if (new_bytes,reused_bytes,count)!=(2620,78,794): raise CompileError('complete original allocation/count required')
    return dict(assembly='.cpu 68000\n.text\n'+'\n'.join(u['assembly'] for u in all_units),units=all_units,
                new_units=units,reused_units=reused,allocated_bytes=2698,new_bytes=2620,reused_bytes=78,instructions=count,
                effects={u['binding']['name']:u['effects'] for u in all_units},original_generation_input=False,
                complete_CPU=False,complete_ROM=False)
