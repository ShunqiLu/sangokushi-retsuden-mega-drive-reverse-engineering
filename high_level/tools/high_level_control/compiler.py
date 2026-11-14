"""Limited Python semantic AST -> typed live-read/branch effects -> 68000.

This compiler accepts typed callback reads, BYTE equality-return gates and a
WORD return. Generation is pure and uses neither ROM/assembly input nor opcode
tables, precompiled fragments, source hashes or original branch displacements.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass

from .target import ABI, BINDINGS, FIELD_BITS, Binding, validate_binding

RESERVED = frozenset(('ControlReader', 'int'))


class CompileError(ValueError):
    pass


@dataclass(frozen=True)
class Effect:
    operation: str
    variable: str
    field: str | None = None
    width_bits: int = 0
    constant: int | None = None
    source_line: int = 0


def _name(node):
    if not isinstance(node, ast.Name) or not isinstance(node.ctx, (ast.Load, ast.Store)):
        raise CompileError('ordinary typed local variable required')
    return node.id


def _constant(node):
    if not isinstance(node, ast.Constant) or type(node.value) is not int or not 0 <= node.value <= 255:
        raise CompileError('complete unsigned BYTE literal comparison required')
    return node.value


def _read(node, reader):
    if (not isinstance(node, ast.Call) or node.args or node.keywords or
            not isinstance(node.func, ast.Attribute) or _name(node.func.value) != reader or
            node.func.attr not in FIELD_BITS):
        raise CompileError('zero-argument typed reader field method required')
    return node.func.attr, FIELD_BITS[node.func.attr]


def semantic_ir(source):
    if type(source) is not str or len(source.encode('utf-8')) > 65536:
        raise CompileError('bounded Python semantic source required')
    try:
        module = ast.parse(source)
    except (SyntaxError, ValueError) as error:
        raise CompileError('invalid Python source') from error
    declarations = list(module.body)
    if declarations and isinstance(declarations[0], ast.Expr) and isinstance(declarations[0].value, ast.Constant) and type(declarations[0].value.value) is str:
        declarations.pop(0)
    if declarations and isinstance(declarations[0], ast.ImportFrom):
        declaration = declarations.pop(0)
        if (declaration.module != 'domain' or declaration.level != 1 or len(declaration.names) != 1 or
                declaration.names[0].name != 'ControlReader' or declaration.names[0].asname is not None):
            raise CompileError('only the explicit ControlReader type declaration is permitted')
    if len(declarations) != 1 or not isinstance(declarations[0], ast.FunctionDef):
        raise CompileError('one ordinary typed semantic rule required')
    function = declarations[0]
    args = function.args
    if (function.name in RESERVED or function.decorator_list or args.posonlyargs or args.vararg or args.kwarg or
            args.kwonlyargs or args.defaults or len(args.args) != 1 or args.args[0].annotation is None or
            ast.unparse(args.args[0].annotation) != 'ControlReader' or function.returns is None or ast.unparse(function.returns) != 'int'):
        raise CompileError('one ControlReader input and int result, no decorators/defaults required')
    reader = args.args[0].arg
    if reader in RESERVED or reader == function.name:
        raise CompileError('input must not shadow its typed intrinsic or rule')
    body = list(function.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and type(body[0].value.value) is str:
        body.pop(0)
    if not body or len(body) > 32:
        raise CompileError('bounded nonempty sequence of reads, return gates and final return required')
    effects, types = [], {}
    result_variable = None
    for index, statement in enumerate(body):
        if isinstance(statement, ast.Assign) and len(statement.targets) == 1:
            variable = _name(statement.targets[0])
            if variable in RESERVED | {reader, function.name}:
                raise CompileError('local must not shadow a type, input or function')
            field, bits = _read(statement.value, reader)
            if variable in types and types[variable] != bits:
                raise CompileError('local type cannot change')
            if bits == 16:
                if result_variable is not None and variable != result_variable:
                    raise CompileError('fixed ABI supports one live selected WORD variable')
                result_variable = variable
            elif variable in types:
                raise CompileError('BYTE state assignments must define distinct immutable locals')
            types[variable] = bits
            effects.append(Effect('read', variable, field, bits, source_line=statement.lineno))
        elif isinstance(statement, ast.If):
            test = statement.test
            if (statement.orelse or len(statement.body) != 1 or not isinstance(statement.body[0], ast.Return) or
                    not isinstance(test, ast.Compare) or len(test.ops) != 1 or not isinstance(test.ops[0], ast.Eq) or len(test.comparators) != 1):
                raise CompileError('single BYTE equality gate returning the selected WORD required')
            variable = _name(test.left)
            returned = _name(statement.body[0].value)
            if types.get(variable) != 8 or types.get(returned) != 16 or returned != result_variable:
                raise CompileError('gate uses a defined BYTE and returns the live selected WORD')
            effects.append(Effect('return_if_equal', variable, width_bits=8,
                                  constant=_constant(test.comparators[0]), source_line=statement.lineno))
        elif isinstance(statement, ast.Return) and index == len(body) - 1:
            if isinstance(statement.value, ast.Name):
                variable = _name(statement.value)
                if variable != result_variable or types.get(variable) != 16:
                    raise CompileError('final selected WORD return required')
                effects.append(Effect('return', variable, width_bits=16, source_line=statement.lineno))
            else:
                field, bits = _read(statement.value, reader)
                if bits != 16 or result_variable is None:
                    raise CompileError('final fresh WORD read required')
                effects.extend((Effect('read', result_variable, field, bits, source_line=statement.lineno),
                                Effect('return', result_variable, width_bits=16, source_line=statement.lineno)))
        else:
            raise CompileError('unsupported semantic statement; no loops/expressions/raw assembly accepted')
    if not effects or effects[-1].operation != 'return':
        raise CompileError('every fallthrough requires an explicit WORD return')
    # The compatibility ABI reuses D1.B. A state must not be referenced after
    # another state read has overwritten that register, even if Python permits it.
    active_byte = None
    for effect in effects:
        if effect.operation == 'read' and effect.width_bits == 8:
            active_byte = effect.variable
        elif effect.operation == 'return_if_equal' and effect.variable != active_byte:
            raise CompileError('BYTE live ranges overlap the one-register target ABI')
    return tuple(effects)


def lower_m68k(effects, binding):
    validate_binding(binding)
    if type(effects) is not tuple or not 1 <= len(effects) <= 64 or any(type(effect) is not Effect for effect in effects):
        raise CompileError('typed semantic effect tuple required')
    # Public effects are rechecked; callers cannot bypass AST validation with
    # arbitrary operands, field strings, constants or unsafe live ranges.
    lines = ['.cpu 68000', '.section .text', '.global choose_control', 'choose_control:']
    locations, offset, active_byte, word_variable, local_types = [], 0, None, None, {}
    final_returns = 0
    for index, effect in enumerate(effects):
        if type(effect.variable) is not str or not effect.variable.isidentifier() or effect.variable in RESERVED:
            raise CompileError('typed non-intrinsic local name required')
        if type(effect.source_line) is not int or effect.source_line < 1:
            raise CompileError('semantic source-line mapping required')
        instructions = []
        if effect.operation == 'read':
            if type(effect.field) is not str or effect.field not in FIELD_BITS or type(effect.width_bits) is not int or effect.width_bits != FIELD_BITS[effect.field] or effect.constant is not None:
                raise CompileError('supported typed live field read required')
            if effect.variable in local_types and (effect.width_bits != 16 or local_types[effect.variable] != 16):
                raise CompileError('BYTE states are immutable and local widths cannot change')
            local_types[effect.variable] = effect.width_bits
            address = getattr(binding, effect.field)
            if effect.width_bits == 16:
                if word_variable is not None and effect.variable != word_variable:
                    raise CompileError('one selected WORD register required')
                word_variable = effect.variable
                instructions = [(f'move.w 0x{address:x}:w,%d0', 4)]
            else:
                active_byte = effect.variable
                instructions = [(f'move.b 0x{address:x}:l,%d1', 6)]
        elif effect.operation == 'return_if_equal':
            if (effect.field is not None or type(effect.width_bits) is not int or effect.width_bits != 8 or type(effect.constant) is not int or
                    not 0 <= effect.constant <= 255 or effect.variable != active_byte or word_variable is None):
                raise CompileError('supported live BYTE equality-return gate required')
            instructions = [('tst.b %d1', 2)] if effect.constant == 0 else [(f'cmpi.b #{effect.constant},%d1', 4)]
            instructions.append(('beq.b .Lcontrol_return', 2))
        elif effect.operation == 'return':
            if (index != len(effects) - 1 or effect.variable != word_variable or type(effect.width_bits) is not int or effect.width_bits != 16 or
                    effect.field is not None or effect.constant is not None):
                raise CompileError('one final selected WORD return required')
            final_returns += 1
            lines.append('.Lcontrol_return:')
            instructions = [('rts', 2)]
        else:
            raise CompileError('unsupported semantic operation')
        for instruction, size in instructions:
            lines.append('        ' + instruction)
            locations.append(dict(offset=offset, bytes=size, semantic_effect=effect.operation,
                                  field=effect.field, source_line=effect.source_line))
            offset += size
    if final_returns != 1 or offset != binding.allocated_bytes:
        raise CompileError(f'fixed compatibility allocation {binding.allocated_bytes} B; lowering selected {offset} B')
    lines.extend(('.global choose_control_end', 'choose_control_end:'))
    return '\n'.join(lines) + '\n', tuple(locations)


def compile_python(source, binding=BINDINGS[0]):
    effects = semantic_ir(source)
    assembly, mapping = lower_m68k(effects, binding)
    return dict(assembly=assembly, effects=effects, source_mapping=mapping, entry=binding.entry,
                bytes=binding.allocated_bytes, binding=binding, ABI=dict(ABI),
                semantic_rule_count=1, general_Python_compiler=False, full_CPU=False, complete_ROM=False)
