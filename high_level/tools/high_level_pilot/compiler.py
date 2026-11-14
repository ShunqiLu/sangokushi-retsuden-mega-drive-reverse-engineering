"""Restricted Python AST -> typed effects -> independent 68000 mnemonic output.

This is one explicitly limited compilation pilot, not a general Python
compiler. No original ROM, assembly file, byte table, or hash-selected code
template is read. Unsupported syntax and incompatible fixed extents reject.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass

ENTRY, EXTENT = 0x179BE, 24
ABI = {'total_LONG': 'd0', 'count_WORD': 'd1', 'member_WORD': 'd2',
       'troop_table': 'a0', 'roster_cursor': 'a1'}
RESERVED_NAMES = frozenset(('u16', 'u32', 's16', 'WordCursor', 'LongTable'))


class CompileError(ValueError):
    pass


@dataclass(frozen=True)
class Effect:
    operation: str
    argument: int | str | None = None
    source_line: int = 0


def _constant(node):
    if isinstance(node, ast.Constant) and type(node.value) is int:
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_constant(node.operand)
    raise CompileError('literal integer required; bool/float/executable expression refused')


def _name(node):
    if not isinstance(node, ast.Name):
        raise CompileError('local typed variable required')
    return node.id


def _call(node, name):
    if (not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name)
            or node.func.id != name or len(node.args) != 1 or node.keywords):
        raise CompileError(f'one-argument {name} semantic conversion required')
    return node.args[0]


def semantic_ir(source):
    """Validate the supported rule structure and emit typed semantic effects.

    Variables may be renamed. Constants flow into emitted operations instead
    of selecting a stored original implementation. This subset supports two
    wrapping accumulators, a live WORD cursor, negative gate, mask, count step,
    and a live indexed LONG sum. Other Python programs are not accepted.
    """
    if type(source) is not str or len(source.encode('utf-8')) > 65536:
        raise CompileError('bounded Python source text required')
    try:
        module = ast.parse(source)
    except (SyntaxError, ValueError) as exc:
        raise CompileError('invalid Python source') from exc
    declarations = list(module.body)
    if declarations and isinstance(declarations[0], ast.Expr) and isinstance(declarations[0].value, ast.Constant):
        if type(declarations[0].value.value) is not str:
            raise CompileError('only a text module docstring is accepted')
        declarations.pop(0)
    if declarations and isinstance(declarations[0], ast.ImportFrom):
        imported = declarations.pop(0)
        if (imported.level != 1 or imported.module != 'domain'
                or {x.name for x in imported.names} != {'LongTable', 'WordCursor', 's16', 'u16', 'u32'}
                or any(x.asname is not None for x in imported.names)):
            raise CompileError('only explicit typed-domain declarations are allowed')
    if len(declarations) != 1 or not isinstance(declarations[0], ast.FunctionDef):
        raise CompileError('exactly one ordinary semantic function required')
    function = declarations[0]
    if function.name in RESERVED_NAMES:
        raise CompileError('function must not shadow a typed-domain intrinsic')
    args = function.args
    if (function.decorator_list or args.posonlyargs or args.vararg or args.kwarg or args.kwonlyargs
            or args.defaults or len(args.args) != 2):
        raise CompileError('two typed positional inputs, no decorators/defaults required')
    if [ast.unparse(x.annotation) if x.annotation is not None else None for x in args.args] != ['WordCursor', 'LongTable']:
        raise CompileError('WordCursor then LongTable typed inputs required')
    if function.returns is None or ast.unparse(function.returns) != 'tuple[int, int]':
        raise CompileError('explicit tuple[int, int] result required')
    roster, table = [x.arg for x in args.args]
    body = list(function.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and type(body[0].value.value) is str:
        body.pop(0)
    if len(body) != 3:
        raise CompileError('two accumulator declarations followed by one loop required')

    effects = []
    def assigned(statement):
        if not isinstance(statement, ast.Assign) or len(statement.targets) != 1:
            raise CompileError('one local assignment required')
        return _name(statement.targets[0]), statement.value
    total, expression = assigned(body[0])
    initial_total = _constant(_call(expression, 'u32'))
    if not -0x80000000 <= initial_total <= 0xFFFFFFFF:
        raise CompileError('LONG initial constant out of supported width')
    effects.append(Effect('initialize_LONG', initial_total & 0xFFFFFFFF, body[0].lineno))
    count, expression = assigned(body[1])
    initial_count = _constant(_call(expression, 'u16'))
    if not 0 <= initial_count <= 0xFFFF:
        raise CompileError('WORD initial constant out of supported width')
    effects.append(Effect('initialize_WORD', initial_count, body[1].lineno))
    loop = body[2]
    if (not isinstance(loop, ast.While) or not isinstance(loop.test, ast.Constant)
            or loop.test.value is not True or loop.orelse or len(loop.body) != 5):
        raise CompileError('unbounded semantic loop with five supported operations required')
    read, gate, mask, increment, addition = loop.body
    member, expression = assigned(read)
    if (not isinstance(expression, ast.Call) or expression.args or expression.keywords
            or not isinstance(expression.func, ast.Attribute) or expression.func.attr != 'read_word'
            or _name(expression.func.value) != roster):
        raise CompileError('live roster.read_word() required before sign gate')
    effects.extend((Effect('loop_label', source_line=loop.lineno),
                    Effect('read_cursor_WORD', source_line=read.lineno)))
    if not isinstance(gate, ast.If) or gate.orelse or len(gate.body) != 1:
        raise CompileError('one original negative-WORD return gate required')
    condition = gate.test
    if (not isinstance(condition, ast.Compare) or len(condition.ops) != 1
            or not isinstance(condition.ops[0], ast.Lt) or len(condition.comparators) != 1
            or _constant(condition.comparators[0]) != 0
            or _name(_call(condition.left, 's16')) != member):
        raise CompileError('signed16 fresh member < 0 gate required')
    returned = gate.body[0]
    if (not isinstance(returned, ast.Return) or not isinstance(returned.value, ast.Tuple)
            or [_name(x) for x in returned.value.elts] != [total, count]):
        raise CompileError('return the typed total and count required')
    effects.append(Effect('return_if_negative_WORD', source_line=gate.lineno))
    entity, expression = assigned(mask)
    if (not isinstance(expression, ast.BinOp) or not isinstance(expression.op, ast.BitAnd)
            or _name(expression.left) != member):
        raise CompileError('member mask required')
    selection_mask = _constant(expression.right)
    if not 0 <= selection_mask <= 0xFFFF:
        raise CompileError('complete WORD mask required')
    effects.append(Effect('mask_member_WORD', selection_mask, mask.lineno))
    target, expression = assigned(increment)
    expression = _call(expression, 'u16')
    if (target != count or not isinstance(expression, ast.BinOp)
            or not isinstance(expression.op, ast.Add) or _name(expression.left) != count):
        raise CompileError('wrapping count addition required')
    step = _constant(expression.right)
    if not 1 <= step <= 8:
        raise CompileError('pilot count step supports integers 1..8')
    effects.append(Effect('add_count_WORD', step, increment.lineno))
    target, expression = assigned(addition)
    expression = _call(expression, 'u32')
    if (target != total or not isinstance(expression, ast.BinOp) or not isinstance(expression.op, ast.Add)
            or _name(expression.left) != total or not isinstance(expression.right, ast.Subscript)
            or _name(expression.right.value) != table or _name(expression.right.slice) != entity):
        raise CompileError('wrapping live table-indexed total addition required')
    if len({roster, table, total, count, member, entity}) != 6:
        raise CompileError('typed inputs and locals must be distinct; unsafe aliasing refused')
    if {roster, table, total, count, member, entity} & RESERVED_NAMES:
        raise CompileError('inputs and locals must not shadow typed-domain intrinsics')
    effects.extend((Effect('add_indexed_LONG', source_line=addition.lineno),
                    Effect('repeat_loop', source_line=loop.lineno),
                    Effect('return_pair', source_line=returned.lineno)))
    return tuple(effects)


def lower_m68k(effects):
    """Select ordinary GNU mnemonics from effects and a fixed compatibility ABI.

    The ABI preserves partial WORD-register writes. Data stride and signed WORD
    EA are target-interface contracts, not embedded source bytes. Labels, not
    original branch byte strings, determine both branch displacements.
    """
    if type(effects) is not tuple or any(type(e) is not Effect for e in effects):
        raise CompileError('typed effect tuple required')
    supported_order = ('initialize_LONG', 'initialize_WORD', 'loop_label', 'read_cursor_WORD',
                       'return_if_negative_WORD', 'mask_member_WORD', 'add_count_WORD',
                       'add_indexed_LONG', 'repeat_loop', 'return_pair')
    if tuple(e.operation for e in effects) != supported_order:
        raise CompileError('unsupported effect ordering or control flow')
    lines = ['.cpu 68000', '.section .text', '.global sum_group_troops', 'sum_group_troops:']
    locations, offset = [], 0
    for effect in effects:
        op, value = effect.operation, effect.argument
        emitted = []
        if op == 'initialize_LONG':
            if type(value) is not int or not 0 <= value <= 0xFFFFFFFF:
                raise CompileError('LONG constant effect out of bounds')
            signed = value - 0x100000000 if value & 0x80000000 else value
            emitted = [(f'moveq #{signed},%d0', 2)] if -128 <= signed <= 127 else [(f'move.l #0x{value:X},%d0', 6)]
        elif op == 'initialize_WORD':
            if type(value) is not int or not 0 <= value <= 0xFFFF:
                raise CompileError('WORD constant effect out of bounds')
            emitted = [('clr.w %d1', 2)] if value == 0 else [(f'move.w #0x{value:X},%d1', 4)]
        elif op == 'loop_label':
            lines.append('.Lroster_loop:')
        elif op == 'read_cursor_WORD':
            emitted = [('move.w (%a1)+,%d2', 2)]
        elif op == 'return_if_negative_WORD':
            emitted = [('bmi.b .Lroster_return', 2)]
        elif op == 'mask_member_WORD':
            if type(value) is not int or not 0 <= value <= 0xFFFF:
                raise CompileError('WORD mask effect out of bounds')
            emitted = [(f'andi.w #0x{value:X},%d2', 4)]
        elif op == 'add_count_WORD':
            if type(value) is not int or not 1 <= value <= 8:
                raise CompileError('ADDQ constant effect out of bounds')
            emitted = [(f'addq.w #{value},%d1', 2)]
        elif op == 'add_indexed_LONG':
            emitted = [('lsl.w #2,%d2', 2), ('add.l (%a0,%d2.w),%d0', 4)]
        elif op == 'repeat_loop':
            emitted = [('bra.b .Lroster_loop', 2)]
        elif op == 'return_pair':
            lines.append('.Lroster_return:')
            emitted = [('rts', 2)]
        else:
            raise CompileError('unsupported semantic effect')
        for instruction, size in emitted:
            lines.append('        ' + instruction)
            locations.append(dict(offset=offset, bytes=size, semantic_effect=op,
                                  source_line=effect.source_line, mnemonic=instruction))
            offset += size
    if offset != EXTENT:
        raise CompileError(f'fixed pilot allocation requires {EXTENT} bytes; selected {offset}')
    return ('\n'.join(lines) + '\n'), tuple(locations)


def compile_python(source):
    effects = semantic_ir(source)
    assembly, mapping = lower_m68k(effects)
    return dict(assembly=assembly, effects=effects, source_mapping=mapping,
                entry=ENTRY, bytes=EXTENT, ABI=dict(ABI), complete_ROM=False,
                general_Python_compiler=False, full_CPU=False)
