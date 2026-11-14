"""Restricted typed-expression Python compiler for live debt date arithmetic.

The front end lowers expression trees, not function names or source hashes. The
back end selects ordinary instruction families per typed operation, calculates
branch labels and checks live-register reuse. It reads no ROM, old assembly,
precompiled fragments, opcode table or byte cache.
"""
from __future__ import annotations
import ast
from dataclasses import dataclass
from .target import ALLOCATION, BINDING, validate_binding


class CompileError(ValueError):
    pass


@dataclass(frozen=True)
class Expr:
    operation: str
    width: int
    arguments: tuple = ()


@dataclass(frozen=True)
class Effect:
    operation: str
    target: str
    expression: Expr
    source_line: int


OPERATIONS = {
    'signed8': (16, (8,)), 'sub8': (8, (8, 8)),
    'mul16': (16, (16, 16)), 'add16': (16, (16, 16)),
    'mul_u16': (32, (16, 16)), 'low_word': (16, (32,)),
    'high_word': (16, (32,)), 'rotate_words': (32, (32,)),
    'add32': (32, (32, 32)), 'div_signed': (32, (32, 32)),
}
IMPORTS = {'Clock', 'DebtDates', *OPERATIONS}


def semantic_ir(source):
    if type(source) is not str or len(source.encode('utf-8')) > 65536:
        raise CompileError('bounded explicit Python source required')
    try:
        module = ast.parse(source)
    except (ValueError, SyntaxError) as error:
        raise CompileError('invalid Python source') from error
    body = list(module.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and type(body[0].value.value) is str:
        body.pop(0)
    if body and isinstance(body[0], ast.ImportFrom):
        imported = body.pop(0)
        if (imported.module != 'domain' or imported.level != 1 or
                {item.name for item in imported.names} != IMPORTS or
                any(item.asname is not None for item in imported.names) or len(imported.names) != len(IMPORTS)):
            raise CompileError('explicit typed domain imports required')
    if len(body) != 1 or not isinstance(body[0], ast.FunctionDef):
        raise CompileError('one typed business function required')
    function = body[0]
    args = function.args
    if function.name in IMPORTS | {'int'}:
        raise CompileError('function must not shadow a typed intrinsic or type')
    if (function.decorator_list or args.posonlyargs or args.defaults or args.kwonlyargs or
            args.vararg or args.kwarg or len(args.args) != 4 or
            [ast.unparse(arg.annotation) if arg.annotation else None for arg in args.args] != ['Clock', 'DebtDates', 'int', 'int'] or
            function.returns is None or ast.unparse(function.returns) != 'int'):
        raise CompileError('Clock, DebtDates, principal LONG, offset WORD signature required')
    names = [arg.arg for arg in args.args]
    if len(set(names)) != 4 or any(name in IMPORTS | {'int', function.name} for name in names):
        raise CompileError('inputs may not shadow intrinsics, types or function')
    clock, record, principal, offset = names
    versions = {principal: principal + '@0', offset: offset + '@0'}
    widths = {versions[principal]: 32, versions[offset]: 16}
    effects = []
    definitions = {}

    def expression(node, expected=None):
        if isinstance(node, ast.Name):
            if node.id not in versions:
                raise CompileError('defined typed local required')
            result = Expr('value', widths[versions[node.id]], (versions[node.id],))
        elif isinstance(node, ast.Constant) and type(node.value) is int:
            if expected not in (8, 16, 32) or not 0 <= node.value < (1 << expected):
                raise CompileError('in-range typed integer literal required')
            result = Expr('constant', expected, (node.value,))
        elif isinstance(node, ast.Call) and not node.keywords:
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                port, field = node.func.value.id, node.func.attr
                if field not in ('year', 'month'):
                    raise CompileError('supported live date port required')
                if port == clock and not node.args:
                    result = Expr('clock_' + field, 8)
                elif (port == record and len(node.args) == 1 and
                      isinstance(node.args[0], ast.Name) and node.args[0].id == offset):
                    result = Expr('record_' + field, 8, (Expr('value', 16, (versions[offset],)),))
                else:
                    raise CompileError('exact typed date port arguments required')
            elif isinstance(node.func, ast.Name) and node.func.id in OPERATIONS:
                bits, inputs = OPERATIONS[node.func.id]
                if len(inputs) != len(node.args):
                    raise CompileError('typed intrinsic arity mismatch')
                values = tuple(expression(arg, width) for arg, width in zip(node.args, inputs))
                if any(value.width != width for value, width in zip(values, inputs)):
                    raise CompileError('explicit intrinsic width mismatch')
                result = Expr(node.func.id, bits, values)
            else:
                raise CompileError('only whitelisted typed operations required')
        else:
            raise CompileError('unsupported expression; no raw assembly or arbitrary calls')
        if expected is not None and result.width != expected:
            raise CompileError('typed expression width mismatch')
        return result

    statements = list(function.body)
    if statements and isinstance(statements[0], ast.Expr) and isinstance(statements[0].value, ast.Constant) and type(statements[0].value.value) is str:
        statements.pop(0)
    if not 1 <= len(statements) <= 32:
        raise CompileError('bounded nonempty business statement sequence required')
    for number, statement in enumerate(statements):
        if isinstance(statement, ast.Assign) and len(statement.targets) == 1 and isinstance(statement.targets[0], ast.Name):
            name = statement.targets[0].id
            if name in IMPORTS | set(names) | {function.name, 'int'}:
                raise CompileError('local must not shadow a typed input/intrinsic')
            value = expression(statement.value)
            version = definitions.get(name, 0) + 1
            definitions[name] = version
            key = name + '@' + str(version)
            versions[name], widths[key] = key, value.width
            effects.append(Effect('assign', key, value, statement.lineno))
        elif isinstance(statement, ast.If):
            test = statement.test
            if (statement.orelse or len(statement.body) != 1 or not isinstance(statement.body[0], ast.Return) or
                    not isinstance(test, ast.Compare) or len(test.ops) != 1 or not isinstance(test.ops[0], ast.Eq) or
                    len(test.comparators) != 1 or not isinstance(test.comparators[0], ast.Constant) or
                    type(test.comparators[0].value) is not int or test.comparators[0].value != 0):
                raise CompileError('single zero gate returning input principal required')
            value = expression(test.left, 16)
            returned = expression(statement.body[0].value, 32)
            if returned != Expr('value', 32, (principal + '@0',)):
                raise CompileError('gate returns unchanged incoming principal')
            effects.append(Effect('return_if_zero', '', value, statement.lineno))
        elif isinstance(statement, ast.Return) and number == len(statements) - 1:
            effects.append(Effect('return', '', expression(statement.value, 32), statement.lineno))
        else:
            raise CompileError('unsupported statement in restricted arithmetic compiler')
    if not effects or effects[-1].operation != 'return':
        raise CompileError('explicit final typed return required')
    return tuple(effects), (principal + '@0', offset + '@0')


def references(expr):
    if expr.operation == 'value':
        return {expr.arguments[0]}
    result = set()
    for argument in expr.arguments:
        if type(argument) is Expr:
            result |= references(argument)
    return result


def strength_reduce(constant):
    """Choose wrapped-WORD (2**a+1)*2**b, without a function template."""
    if type(constant) is not int or not 1 <= constant <= 65535:
        raise CompileError('positive WORD multiplier required')
    for tail_shift in range(9):
        for inner_shift in range(1, 9):
            if ((1 << inner_shift) + 1) << tail_shift == constant:
                return inner_shift, tail_shift
    raise CompileError('multiplier has no reviewed fixed-extent shift/add family')


def lower(effects, arguments, binding=BINDING):
    validate_binding(binding)
    if type(effects) is not tuple or any(type(item) is not Effect for item in effects):
        raise CompileError('typed immutable effect tuple required')
    if type(arguments) is not tuple or len(arguments) != 2 or any(type(x) is not str for x in arguments):
        raise CompileError('typed input identities required')
    principal, offset = arguments
    locations = {principal: binding.principal_register, offset: binding.offset_register}
    widths = {principal: 32, offset: 16}
    last_use = {}
    for index, effect in enumerate(effects):
        if type(effect.source_line) is not int or effect.source_line < 1:
            raise CompileError('positive source-line mapping required')
        for reference in references(effect.expression):
            last_use[reference] = index
    lines = ['.cpu 68000', '.section .text', '.global debt_due', '.global debt_due_end', 'debt_due:']
    mapping, allocation = [], iter(ALLOCATION)
    gates, returns, byte_offset = 0, 0, 0

    def instruction(text, size, source_line):
        nonlocal byte_offset
        lines.append('    ' + text)
        mapping.append(dict(offset=byte_offset, size=size, source_line=source_line, instruction=text))
        byte_offset += size

    def loc(expr):
        if expr.operation != 'value' or expr.arguments[0] not in locations:
            raise CompileError('defined live register value required')
        key = expr.arguments[0]
        if widths.get(key) != expr.width:
            raise CompileError('SSA value width differs')
        return locations[key]

    def emit(expr, destination, index, line):
        operation, values = expr.operation, expr.arguments
        if operation == 'signed8':
            difference = values[0]
            if difference.operation != 'sub8' or len(difference.arguments) != 2:
                raise CompileError('BYTE subtraction followed by signed widening required')
            current, recorded = difference.arguments
            if current.operation not in ('clock_year', 'clock_month') or recorded.operation != current.operation.replace('clock_', 'record_'):
                raise CompileError('ordered matching live clock/record reads required')
            address = binding.year_address if current.operation == 'clock_year' else binding.month_address
            displacement = binding.year_displacement if current.operation == 'clock_year' else binding.month_displacement
            if loc(recorded.arguments[0]) != binding.offset_register:
                raise CompileError('record offset ABI differs')
            instruction(f'move.b 0x{address & 65535:04x}:w,%{destination}', 4, line)
            instruction(f'sub.b {displacement}(%{binding.record_register},%{binding.offset_register}.w),%{destination}', 4, line)
            instruction(f'ext.w %{destination}', 2, line)
        elif operation == 'mul16':
            if values[1].operation != 'constant':
                raise CompileError('fixed-shape semantic constant WORD multiplier required')
            source = loc(values[0])
            inner, tail = strength_reduce(values[1].arguments[0])
            if source != destination:
                raise CompileError('destructive WORD multiply requires same allocation')
            scratch = binding.scratch_register
            if any(reg == scratch and last_use.get(key, -1) > index for key, reg in locations.items()):
                raise CompileError('strength-reduction scratch would destroy a live value')
            instruction(f'move.w %{source},%{scratch}', 2, line)
            instruction(f'lsl.w #{inner},%{destination}', 2, line)
            instruction(f'add.w %{scratch},%{destination}', 2, line)
            if tail:
                instruction(f'lsl.w #{tail},%{destination}', 2, line)
        elif operation in ('add16', 'add32'):
            bits = 16 if operation == 'add16' else 32
            left, right = values
            if left.operation == 'rotate_words':
                source = loc(left.arguments[0])
                if source != destination:
                    raise CompileError('word rotation requires destructive source allocation')
                instruction(f'swap %{source}', 2, line)
            else:
                source = loc(left)
                if source != destination:
                    instruction(f'move.{"w" if bits == 16 else "l"} %{source},%{destination}', 2, line)
            instruction(f'add.{"w" if bits == 16 else "l"} %{loc(right)},%{destination}', 2, line)
        elif operation == 'mul_u16':
            factor, half = values
            source = loc(factor)
            if source != destination:
                instruction(f'move.w %{source},%{destination}', 2, line)
            if half.operation not in ('low_word', 'high_word'):
                raise CompileError('explicit principal WORD projection required')
            input_reg = loc(half.arguments[0])
            if half.operation == 'high_word':
                instruction(f'swap %{input_reg}', 2, line)
            instruction(f'mulu.w %{input_reg},%{destination}', 2, line)
            if half.operation == 'high_word':
                instruction(f'swap %{input_reg}', 2, line)
        elif operation == 'div_signed':
            numerator, denominator = values
            if denominator.operation != 'constant' or not 1 <= denominator.arguments[0] <= 127:
                raise CompileError('positive signed-MOVEQ denominator required')
            source = loc(numerator)
            if destination != binding.principal_register:
                raise CompileError('division output storage ABI differs')
            if last_use.get(principal, -1) > index:
                saved = binding.scratch_register
                if any(key != principal and reg == saved and last_use.get(key, -1) > index for key, reg in locations.items()):
                    raise CompileError('division preservation register is live')
                instruction(f'move.l %{locations[principal]},%{saved}', 2, line)
                locations[principal] = saved
            if source != destination:
                instruction(f'move.l %{source},%{destination}', 2, line)
            instruction(f'moveq #{denominator.arguments[0]},%d2', 2, line)
            instruction(f'jsr 0x{binding.division_entry:x}:l', 6, line)
        else:
            raise CompileError('unsupported typed lowering operation')

    for index, effect in enumerate(effects):
        if effect.operation == 'assign':
            if type(effect.target) is not str or not effect.target or effect.target in locations:
                raise CompileError('new SSA definition identity required')
            try:
                destination = next(allocation)
            except StopIteration as error:
                raise CompileError('reviewed allocation capacity exceeded') from error
            # The destination may consume an old source at this instruction but
            # cannot overwrite any other value still needed by a later effect.
            for key, register in locations.items():
                if register == destination and last_use.get(key, -1) > index:
                    if not (effect.expression.operation == 'div_signed' and key == principal):
                        raise CompileError('target allocation destroys a later live SSA value')
            emit(effect.expression, destination, index, effect.source_line)
            locations[effect.target], widths[effect.target] = destination, effect.expression.width
        elif effect.operation == 'return_if_zero':
            if gates or effect.expression.operation != 'value' or effect.expression.width != 16:
                raise CompileError('single WORD zero exit required')
            # The immediately preceding assignment must set Z from that exact
            # WORD. Reusing unrelated CCR state or inserting a TST is refused.
            previous = effects[index - 1] if index else None
            if previous is None or previous.target != effect.expression.arguments[0] or previous.expression.operation != 'add16':
                raise CompileError('zero gate requires its live WORD arithmetic flags')
            instruction('beq.w .Lreturn', 4, effect.source_line)
            gates += 1
        elif effect.operation == 'return':
            if index != len(effects) - 1 or effect.expression.operation != 'add32':
                raise CompileError('final LONG arithmetic return required')
            emit(effect.expression, binding.principal_register, index, effect.source_line)
            lines.append('.Lreturn:')
            instruction('rts', 2, effect.source_line)
            returns += 1
        else:
            raise CompileError('unknown typed effect')
    if gates != 1 or returns != 1 or byte_offset != binding.allocated_bytes:
        raise CompileError('generated body does not satisfy reviewed fixed extent')
    lines.append('debt_due_end:')
    return dict(assembly='\n'.join(lines) + '\n', source_mapping=mapping,
                external_helper=dict(entry=binding.division_entry, denominator_bits=32,
                                     admitted_denominator_range=[1, 127], helper_generated_here=False),
                bytes=byte_offset)


def compile_python(source, binding=BINDING):
    effects, arguments = semantic_ir(source)
    result = lower(effects, arguments, binding)
    result['effects'] = effects
    return result
