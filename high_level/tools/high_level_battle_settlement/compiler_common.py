"""Small target emitter and joint assembly composition, with no source reads."""
from dataclasses import asdict
import ast
import re
from .target import BINDINGS, validate_binding


class CompileError(ValueError):
    pass


def require_declared_names(functions, imported_names):
    """Require actual Python bindings, not a silent compiler-only prelude.

    Parameters and assignments are local bindings; order and definite-liveness
    checks remain the typed frontend's job. Only used external names are tested,
    so deletion of an unused approved import is an ordinary harmless edit.
    """
    if type(functions) is not dict or type(imported_names) is not set or any(type(n) is not str for n in imported_names):
        raise CompileError('explicit declaration/import sets required')
    globals_available=set(functions)|imported_names|{'tuple'}
    for function in functions.values():
        local_names={a.arg for a in function.args.args}
        local_names.update(node.id for node in ast.walk(function) if isinstance(node,ast.Name) and isinstance(node.ctx,ast.Store))
        used={node.id for node in ast.walk(function) if isinstance(node,ast.Name) and isinstance(node.ctx,ast.Load)}
        absent=used-local_names-globals_available
        if absent:
            raise CompileError('used external Python names need current approved imports/declarations: '+','.join(sorted(absent)))


class Emitter:
    def __init__(self, binding):
        validate_binding(binding)
        self.binding, self.lines, self.mapping, self.serial = binding, [], [], 0
    def begin(self):
        b = self.binding
        self.lines += [f'.org 0x{b.entry:x}', '.global ' + b.name, b.name + ':']
    def label(self, name):
        if type(name) is not str or not name.isidentifier():
            raise CompileError('strict target label required')
        self.lines.append(name + ':')
    def fresh(self, role):
        if type(role) is not str or not role.isidentifier():
            raise CompileError('strict target label role required')
        self.serial += 1
        return f'{self.binding.name}_{role}_{self.serial}'
    def ins(self, operation, operands='', width=2):
        if type(operation) is not str or type(operands) is not str or type(width) is not int or width not in (2, 4, 6, 8, 10):
            raise CompileError('strict target operation/encoding width required')
        if not operation or any(c in operation for c in ('\n', ';', '.byte', '.word', '.incbin')) or '\n' in operands or ';' in operands:
            raise CompileError('one ordinary instruction required')
        symbol = f'hl_{self.binding.name}_{len(self.mapping)}'
        self.lines += ['.global ' + symbol, symbol + ':', '    ' + operation + (' ' + operands if operands else '')]
        self.mapping.append(dict(symbol=symbol, operation=operation, operands=operands, encoding_bytes=width))
    def end(self, *, emit_completion=True):
        if emit_completion:
            if self.binding.completion == 'abandon_two_calls':
                self.ins('movem.l', '(%sp)+,%d0/%a0', 4)
            self.ins('rts')
        self.lines += ['.global ' + self.binding.name + '_end', self.binding.name + '_end:']
    def unit(self, effects):
        return dict(binding=asdict(self.binding), assembly='\n'.join(self.lines) + '\n', instructions=self.mapping, effects=effects)


def compile_modules(numeric_source, members_source, helper_source):
    from .compiler_numeric import compile_numeric
    from .compiler_members import compile_members
    from tools.high_level_city_event.compiler import compile_arithmetic_units
    numeric, members = compile_numeric(numeric_source), compile_members(members_source)
    units = sorted(numeric['units'] + members['units'], key=lambda u: u['binding']['entry'])
    if [u['binding'] for u in units] != [asdict(b) for b in BINDINGS]:
        raise CompileError('complete thirteen-body settlement cluster required')
    shared = compile_arithmetic_units(helper_source, selected=('random_sample', 'signed_divmod', 'positive_denominator', 'unsigned_divmod', 'word_pair_divmod'))
    generated_parts = re.split(r'(?m)^\.org ', shared['assembly'])
    preamble = generated_parts[0]
    helper_parts = {int(part.splitlines()[0], 16): '.org ' + part for part in generated_parts[1:]}
    reused = []
    for binding in shared['bindings']:
        mappings = []
        for item in shared['mappings'][binding.name]:
            operation, operands = item['mnemonic'], item['operands']
            width = 2
            if operation in ('movem.l', 'movem.w'): width = 4
            elif operation in ('cmpi.l', 'andi.l'): width = 6
            elif operation == 'move.l' and operands.startswith('#'): width = 6
            elif ':w' in operands: width = 4
            mappings.append(dict(symbol=item['symbol'], operation=operation, operands=operands, encoding_bytes=width))
        reused.append(dict(binding=dict(name=binding.name, entry=binding.entry, end=binding.end, completion='return'),
                           assembly=helper_parts[binding.entry], instructions=mappings, effects=shared['effects'][binding.rule], reused=True))
    all_units = sorted(units + reused, key=lambda u: u['binding']['entry'])
    return dict(assembly=preamble + '\n'.join(u['assembly'] for u in all_units),
                units=all_units, new_units=units, reused_units=reused, allocated_bytes=1846, new_bytes=1656, reused_bytes=190,
                original_generation_input=False, complete_CPU=False, complete_ROM=False)
