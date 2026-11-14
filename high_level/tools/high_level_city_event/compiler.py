"""Restricted semantic Python AST -> typed effects -> ordinary 68000 GNU.

No source hashing, original assembly, ROM, code-byte payload, or file I/O is
used here. Fixed allocation/register contracts live in target.py. Selection
families are arithmetic, live memory, branches, calls, and counted loops; none
is an entire event function's assembly template.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass

from .target import (BINDINGS, FIELD_BASES, PARAMETERS, REGISTERS, PRESERVED, LOCAL_PRESERVED,
                     CALL_STYLE, RETURN_REGISTER, validate_binding)


class CompileError(ValueError):
    pass


@dataclass(frozen=True)
class Expression:
    operation: str
    arguments: tuple
    width: int
    line: int


@dataclass(frozen=True)
class Effect:
    operation: str
    arguments: tuple
    line: int


INTRINSICS = {'u16', 'u32', 'checked_word', 'checked_long', 'low16', 'high16', 'swap_words', 'replace_byte',
              'replace_word', 'join_words', 'negative_byte', 'negative_long',
              'divu_retained', 'range'}
TYPES = {'EventState', 'U16', 'U32', 'None', 'tuple', 'str'}
METHODS = {'owner', 'player_owner', 'clear_queue_flag', 'queue', 'field', 'seed',
           'store_seed', 'parameter', 'read', 'write', 'read_next', 'write_next', 'rewind_probe'}
OPERATORS = {ast.Add: 'add', ast.Sub: 'sub', ast.Mult: 'multiply', ast.LShift: 'shift', ast.BitAnd: 'and'}
COMPARISONS = {ast.Eq: 'eq', ast.NotEq: 'ne', ast.Lt: 'lt', ast.LtE: 'le', ast.Gt: 'gt', ast.GtE: 'ge'}
FUNCTION_TYPES = {'reset_queue': 0, 'append_queue': 16, 'scale_field': 32,
                  'submit_three_fields': 16, 'submit_four_fields': 16, 'submit_classified_fields': 16,
                  'random_sample': 16, 'sample_once': 16, 'sample_small': 16, 'sample_wide': 16,
                  'wrapped_product': 32, 'divide_percent': 32, 'signed_divmod': 64,
                  'positive_denominator': 64, 'unsigned_divmod': 64, 'word_pair_divmod': 64}
ARGUMENTS = {
    'reset_queue': ('state',), 'append_queue': ('state', 'city', 'incoming_owner'),
    'scale_field': ('state', 'offset', 'factor', 'field_name'),
    'submit_three_fields': ('state', 'city', 'incoming_owner'),
    'submit_four_fields': ('state', 'city', 'incoming_owner'),
    'submit_classified_fields': ('state', 'city'), 'random_sample': ('state',),
    'sample_once': ('state',), 'sample_small': ('state',), 'sample_wide': ('state',),
    'wrapped_product': ('value', 'factor'), 'divide_percent': ('product',),
    'signed_divmod': ('numerator', 'denominator'), 'positive_denominator': ('numerator', 'denominator'),
    'unsigned_divmod': ('numerator', 'denominator'), 'word_pair_divmod': ('numerator', 'denominator')}
ANNOTATIONS = {'state': 'EventState', 'city': 'U16', 'incoming_owner': 'U16', 'offset': 'U16',
               'factor': 'U16', 'field_name': 'str', 'value': 'U32', 'product': 'U32',
               'numerator': 'U32', 'denominator': 'U32'}


class Frontend:
    def __init__(self, function):
        self.function = function
        self.defined = set(ARGUMENTS[function.name])
        self.widths = {arg.arg: {'U16': 16, 'U32': 32, 'str': 0, 'EventState': 0}[ast.unparse(arg.annotation)]
                       for arg in function.args.args}
        self.receivers = {'state': 'state'} if 'state' in self.defined else {}

    def expression(self, node):
        line = node.lineno
        if isinstance(node, ast.Name) and node.id in self.defined:
            return Expression('variable', (node.id,), self.widths.get(node.id, 32), line)
        if isinstance(node, ast.Constant) and type(node.value) in (int, str, bool):
            if type(node.value) is int and not 0 <= node.value <= 0xFFFFFFFF:
                raise CompileError('complete nonnegative fixed-width literal required')
            if type(node.value) is str and node.value not in set(FIELD_BASES) | set(PARAMETERS):
                raise CompileError('only neutral bound field identifiers are supported')
            return Expression('constant', (node.value,), 32 if type(node.value) is int else 0, line)
        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            left, right = self.expression(node.left), self.expression(node.right)
            if not left.width or not right.width:
                raise CompileError('typed integer expression required')
            return Expression(OPERATORS[type(node.op)], (left, right), max(left.width, right.width), line)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.Not)):
            value = self.expression(node.operand)
            return Expression('negate' if isinstance(node.op, ast.USub) else 'not', (value,), value.width, line)
        if isinstance(node, ast.Compare) and len(node.ops) == len(node.comparators) == 1 and type(node.ops[0]) in COMPARISONS:
            return Expression(COMPARISONS[type(node.ops[0])], (self.expression(node.left), self.expression(node.comparators[0])), 1, line)
        if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or):
            return Expression('or', tuple(self.expression(value) for value in node.values), 1, line)
        if isinstance(node, ast.Tuple):
            return Expression('tuple', tuple(self.expression(value) for value in node.elts), 64, line)
        if isinstance(node, ast.Call) and not node.keywords:
            if isinstance(node.func, ast.Name) and node.func.id in INTRINSICS | set(FUNCTION_TYPES):
                name = node.func.id
                args = tuple(self.expression(value) for value in node.args)
                counts = {'u16': 1, 'u32': 1, 'low16': 1, 'high16': 1, 'swap_words': 1,
                          'checked_word': 1, 'checked_long': 1,
                          'negative_byte': 1, 'negative_long': 1, 'replace_byte': 2,
                          'replace_word': 2, 'join_words': 2, 'divu_retained': 2, 'range': 1}
                expected = counts.get(name, len(ARGUMENTS.get(name, ())))
                if len(args) != expected:
                    raise CompileError('unsupported intrinsic/call arity')
                if name in FUNCTION_TYPES:
                    for parameter, value in zip(ARGUMENTS[name], args):
                        annotation = ANNOTATIONS[parameter]
                        if annotation == 'EventState':
                            if value.operation != 'variable' or value.arguments[0] != 'state' or self.receivers.get('state') != 'state':
                                raise CompileError('semantic call requires the actual live EventState input')
                        elif annotation == 'str':
                            if value.operation != 'constant' or type(value.arguments[0]) is not str or value.arguments[0] not in FIELD_BASES:
                                raise CompileError('semantic field call requires an explicit bound neutral identifier')
                        else:
                            bits = 16 if annotation == 'U16' else 32
                            if value.width != bits and not (value.operation == 'constant' and type(value.arguments[0]) is int and 0 <= value.arguments[0] < 1 << bits):
                                raise CompileError('semantic call argument width/type differs from its declared interface')
                width = 16 if name in ('u16', 'checked_word', 'low16', 'replace_byte') else 1 if name.startswith('negative_') else FUNCTION_TYPES.get(name, 32)
                return Expression('call', (name, *args), width, line)
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.attr in METHODS:
                receiver = node.func.value.id
                if receiver not in self.defined:
                    raise CompileError('live typed receiver must be defined')
                method = node.func.attr
                receiver_type = self.receivers.get(receiver)
                legal = {'state': {'owner', 'player_owner', 'clear_queue_flag', 'queue', 'field', 'seed', 'store_seed', 'parameter'},
                         'queue': {'read_next', 'rewind_probe', 'write', 'write_next'},
                         'field': {'read', 'write'}}
                if receiver_type not in legal or method not in legal[receiver_type]:
                    raise CompileError('method must belong to its actual live typed receiver')
                arities = {'owner': 1, 'player_owner': 1, 'clear_queue_flag': 0, 'queue': 0, 'field': 1,
                           'seed': 0, 'store_seed': 1, 'parameter': 2, 'read': 1, 'write': 2,
                           'read_next': 0, 'write_next': 1, 'rewind_probe': 0}
                # Queue.write takes one payload, Field.write takes offset+payload.
                if method == 'write':
                    arities[method] = 1 if receiver == 'queue' else 2
                if len(node.args) != arities[method]:
                    raise CompileError('typed live method arity differs')
                args = tuple(self.expression(value) for value in node.args)
                width = 8 if method in ('owner', 'parameter', 'read_next', 'rewind_probe') else 16 if method == 'player_owner' else 32 if method in ('seed', 'read') else 0
                return Expression('method', (receiver, method, *args), width, line)
        raise CompileError(f'unsupported semantic expression at line {line}')

    def statements(self, nodes):
        effects = []
        for node in nodes:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and type(node.value.value) is str:
                continue
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
                names = (target.id,) if isinstance(target, ast.Name) else tuple(x.id for x in target.elts) if isinstance(target, ast.Tuple) and all(isinstance(x, ast.Name) for x in target.elts) else ()
                if not names or any(name in INTRINSICS | TYPES | set(FUNCTION_TYPES) | {'state', 'field_name'} for name in names):
                    raise CompileError('ordinary non-shadowing typed local required')
                value = self.expression(node.value)
                if len(names) > 1 and (len(names) != 2 or value.width != 64):
                    raise CompileError('two-result quotient/remainder assignment required')
                for name in names:
                    self.defined.add(name)
                    self.widths[name] = 32 if len(names) > 1 else value.width
                    if value.operation == 'method' and value.arguments[1] in ('queue', 'field'):
                        self.receivers[name] = value.arguments[1]
                    else:
                        self.receivers.pop(name, None)
                effects.append(Effect('assign', (names, value), node.lineno))
            elif isinstance(node, ast.Expr):
                value = self.expression(node.value)
                if value.operation not in ('call', 'method'):
                    raise CompileError('only typed effect calls may discard their result')
                effects.append(Effect('evaluate', (value,), node.lineno))
            elif isinstance(node, ast.If) and not node.orelse:
                test = self.expression(node.test)
                saved_defined, saved_widths, saved_receivers = set(self.defined), dict(self.widths), dict(self.receivers)
                body = self.statements(node.body)
                # No-else branch locals are not definitely assigned on its
                # fallthrough. Mutable existing locals keep their prior type.
                self.defined, self.widths, self.receivers = saved_defined, saved_widths, saved_receivers
                effects.append(Effect('if', (test, body), node.lineno))
            elif isinstance(node, ast.While) and not node.orelse:
                effects.append(Effect('while', (self.expression(node.test), self.statements(node.body)), node.lineno))
            elif isinstance(node, ast.For) and isinstance(node.target, ast.Name) and not node.orelse:
                if node.target.id in INTRINSICS | TYPES | set(FUNCTION_TYPES) | set(ARGUMENTS[self.function.name]):
                    raise CompileError('loop local cannot shadow input/type/intrinsic/function')
                self.defined.add(node.target.id)
                self.widths[node.target.id] = 16
                effects.append(Effect('for', (node.target.id, self.expression(node.iter), self.statements(node.body)), node.lineno))
            elif isinstance(node, ast.Return):
                value = self.expression(node.value) if node.value else None
                if (value is None and FUNCTION_TYPES[self.function.name] != 0) or (value is not None and value.width != FUNCTION_TYPES[self.function.name]):
                    raise CompileError('semantic return value must match the declared fixed-width interface')
                effects.append(Effect('return', (value,), node.lineno))
            elif isinstance(node, ast.Continue):
                effects.append(Effect('continue', (), node.lineno))
            elif isinstance(node, ast.Pass):
                effects.append(Effect('pass', (), node.lineno))
            else:
                raise CompileError(f'unsupported semantic statement at line {node.lineno}')
        return tuple(effects)


def semantic_ir(source):
    if type(source) is not str or len(source.encode()) > 131072:
        raise CompileError('bounded semantic Python source required')
    try:
        module = ast.parse(source)
    except (SyntaxError, ValueError) as error:
        raise CompileError('invalid semantic Python') from error
    result = {}
    for node in module.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and type(node.value.value) is str:
            continue
        if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module in ('domain', 'arithmetic'):
            exports = (INTRINSICS - {'range'}) | (TYPES - {'None', 'tuple', 'str'}) if node.module == 'domain' else set(FUNCTION_TYPES) - {'reset_queue', 'append_queue', 'scale_field', 'submit_three_fields', 'submit_four_fields', 'submit_classified_fields'}
            if any(alias.asname is not None or alias.name not in exports for alias in node.names):
                raise CompileError('explicit typed/intrinsic imports only')
            continue
        if not isinstance(node, ast.FunctionDef) or node.name not in FUNCTION_TYPES or node.name in result:
            raise CompileError('only named typed business functions, no executable module statements')
        args = node.args
        if node.decorator_list or args.defaults or args.kw_defaults or args.posonlyargs or args.kwonlyargs or args.vararg or args.kwarg or tuple(arg.arg for arg in args.args) != ARGUMENTS[node.name]:
            raise CompileError('explicit fixed semantic interface required')
        if any(arg.annotation is None or ast.unparse(arg.annotation) != ANNOTATIONS[arg.arg] for arg in args.args):
            raise CompileError('strict fixed-width input annotations required')
        returned = ast.unparse(node.returns) if node.returns else ''
        expected_return = {0: 'None', 16: 'U16', 32: 'U32', 64: 'tuple[U32, U32]'}[FUNCTION_TYPES[node.name]]
        if returned != expected_return:
            raise CompileError('strict fixed-width result annotation required')
        frontend = Frontend(node)
        result[node.name] = frontend.statements(node.body)
    if not result:
        raise CompileError('nonempty semantic module required')
    return result


def _var(expression):
    if expression.operation != 'variable':
        raise CompileError('allocated semantic local required')
    return expression.arguments[0]


def _constant(expression):
    if expression.operation != 'constant' or type(expression.arguments[0]) not in (int, str):
        raise CompileError('typed literal required')
    return expression.arguments[0]


def _unwrap(expression):
    while expression.operation == 'call' and expression.arguments[0] in ('u16', 'u32', 'low16'):
        expression = expression.arguments[1]
    return expression


def _shape(expression):
    """Structural semantic equivalence, never source text/hash equivalence."""
    return (expression.operation, tuple(_shape(arg) if type(arg) is Expression else arg
                                       for arg in expression.arguments), expression.width)


def _is_call(expression, name):
    return expression.operation == 'call' and expression.arguments[0] == name


class Selector:
    def __init__(self, binding):
        validate_binding(binding)
        self.binding = binding
        self.registers = dict(REGISTERS[binding.rule])
        self.lines, self.mapping, self.serial = [], [], 0
        self.flags, self.saved_city, self.word_frame = None, False, False
        self.local_frame = False
        self.tail_returns = {}
        self.loop = []
        self.condition_index = 0
        self.source_line = 1

    def instruction(self, mnemonic, operands='', *, role='effect'):
        # The emitter constructs ordinary operands from strict types only.
        symbol = f'hl_{self.binding.name}_{len(self.mapping):03d}'
        self.lines.append(symbol + ':')
        self.lines.append('        ' + mnemonic + (' ' + operands if operands else ''))
        self.mapping.append(dict(instruction=len(self.mapping), line=self.source_line, operation=role,
                                 mnemonic=mnemonic, operands=operands, symbol=symbol))

    def label(self, name):
        self.lines.append(name + ':')

    def new_label(self, role):
        self.serial += 1
        return f'.L_{self.binding.name}_{role}_{self.serial}'

    def reg(self, expression):
        name = _var(_unwrap(expression))
        if name not in self.registers:
            raise CompileError(f'no compatibility allocation for semantic local {name}')
        return '%' + self.registers[name]

    def move(self, source, target, width):
        if source != target:
            self.instruction('move.' + ('b' if width == 8 else 'w' if width <= 16 else 'l'), source + ',' + target, role='copy')
            self.flags = (target, width)

    def literal(self, value, target, width):
        if type(value) is not int or not 0 <= value < 1 << width:
            raise CompileError('strict fixed-width immediate required')
        if 0 <= value <= 127:
            self.instruction('moveq', f'#{value},{target}', role='literal')
        else:
            self.instruction('move.' + ('w' if width == 16 else 'l'), f'#0x{value:x},{target}', role='literal')
        self.flags = (target, 32 if 0 <= value <= 127 else width)

    def call(self, expression, target=None):
        name, *arguments = expression.arguments
        if name not in FUNCTION_TYPES:
            raise CompileError('supported semantic callee required')
        if name == 'scale_field':
            field = _constant(arguments[-1])
            if type(field) is not str or field not in FIELD_BASES:
                raise CompileError('explicit neutral field binding required')
            label = 'scale_' + field
        else:
            label = name
        # Runtime state is a live interface, not an emitted argument pointer.
        values = [value for value, arg in zip(arguments, ARGUMENTS[name]) if arg not in ('state', 'field_name')]
        callee_args = [arg for arg in ARGUMENTS[name] if arg not in ('state', 'field_name')]
        callee_registers = REGISTERS[name]
        for arg, value in zip(callee_args, values):
            if name == 'append_queue':
                expected = '%' + callee_registers[arg]
                if self.reg(value) != expected or value.width != 16:
                    raise CompileError('append city/owner require live D7.W/D0.W arguments; unsafe shuffle rejected')
            else:
                expected = '%' + callee_registers[arg]
                self.expression(value, expected, 16 if ANNOTATIONS[arg] == 'U16' else 32)
        style = CALL_STYLE.get(name, 'word_bsr')
        if style == 'absolute':
            self.instruction('jsr', label + ':l', role='call')
        elif style == 'pc_jsr_nop':
            self.instruction('jsr', label + '(%pc)', role='call')
            self.instruction('nop', role='encoding_compatibility')
        else:
            self.instruction('bsr.' + ('b' if style == 'short_bsr' else 'w'), label, role='call')
        if target is not None:
            result = RETURN_REGISTER.get(name, 'd0')
            if not isinstance(result, str):
                raise CompileError('tuple-return call requires tuple assignment')
            self.move('%' + result, target, expression.width)
        self.flags = None

    def expression(self, value, target, width):
        op, args = value.operation, value.arguments
        if op == 'constant':
            self.literal(_constant(value), target, width)
        elif op == 'variable':
            self.move(self.reg(value), target, width)
        elif op == 'method':
            receiver, method, *values = args
            if method in ('queue', 'field'):
                field = self.binding.field if method == 'field' and values[0].operation == 'variable' else _constant(values[0]) if method == 'field' else None
                base = FIELD_BASES[field] if field else 0xD420
                self.instruction('lea', f'0x{base:x}:w,{target}', role='live_view')
            elif method == 'seed':
                self.instruction('move.l', '0xf61c:w,' + target, role='read')
                self.flags = (target, 32)
            elif method == 'read':
                index = self.reg(values[0])
                self.instruction('move.l', f'(%{self.registers[receiver]},{index}.w),{target}', role='read')
                self.flags = (target, 32)
            elif method == 'parameter':
                group, index = _constant(values[0]), self.reg(values[1])
                self.instruction('move.b', f'(event_{group}-.-2)(%pc,{index}.w),{target}', role='live_parameter_read')
                self.flags = (target, 8)
            elif method == 'owner':
                self.instruction('lea', '0xf428:w,%a0', role='live_view')
                self.instruction('move.b', f'(%a0,{self.reg(values[0])}.w),{target}', role='read')
                self.flags = (target, 8)
            else:
                raise CompileError('unsupported value-returning live method')
        elif op == 'call':
            name, *values = args
            if name in ('checked_word', 'checked_long'):
                expected = 16 if name == 'checked_word' else 32
                if values[0].operation != 'variable' or values[0].width != expected or self.reg(values[0]) != target:
                    raise CompileError('host input contract must validate the same already-typed ABI storage')
            elif name in ('u16', 'u32', 'low16'):
                if name == 'u32' and values[0].width <= 16:
                    raise CompileError('zero-extension of live WORD requires a separate supported effect')
                self.expression(values[0], target, 16 if name in ('u16', 'low16') else 32)
            elif name in ('replace_byte', 'replace_word'):
                # Partial register overwrite is a typed semantic operation.
                if values[0].operation != 'variable' or self.reg(values[0]) != target:
                    raise CompileError('partial overwrite preserved source must occupy destination storage')
                source = values[1]
                partial = 8 if name == 'replace_byte' else 16
                if source.operation == 'method':
                    self.expression(source, target, partial)
                else:
                    unwrapped = _unwrap(source)
                    if unwrapped.operation == 'add':
                        self.expression(unwrapped, target, partial)
                    else:
                        self.move(self.reg(unwrapped), target, partial)
                self.flags = (target, partial)
            elif name == 'swap_words':
                self.move(self.reg(values[0]), target, 32)
                self.instruction('swap', target, role='word_rotation')
                self.flags = (target, 32)
            elif name == 'high16':
                self.move(self.reg(values[0]), target, 32)
                self.instruction('clr.w', target, role='word_extract')
                self.instruction('swap', target, role='word_extract')
                self.flags = (target, 32)
            elif name == 'divu_retained':
                numerator, divisor = values
                numerator = _unwrap(numerator)
                if numerator.operation == 'call' and numerator.arguments[0] == 'join_words':
                    # A still-live low argument has a split-WORD ABI spill.
                    if not self.word_frame:
                        raise CompileError('join after split division requires live WORD spill')
                    high, low = numerator.arguments[1:]
                    if (high.operation != 'call' or high.arguments[0] != 'high16' or _var(high.arguments[1]) != 'high_division' or
                            low.operation != 'call' or low.arguments[0] != 'low16' or _var(low.arguments[1]) != 'numerator' or target != '%d1'):
                        raise CompileError('split numerator requires exact still-live high result and spilled original low argument')
                    self.instruction('move.w', '(%a7)+,' + target, role='live_word_restore')
                else:
                    self.expression(numerator, target, 32)
                divisor = _unwrap(divisor)
                operand = '#' + str(_constant(divisor)) if divisor.operation == 'constant' else self.reg(divisor)
                self.instruction('divu.w', operand + ',' + target, role='divide_WORD_retaining_overflow')
                self.flags = None
            elif name == 'join_words':
                if (not self.word_frame or _var(values[0]) != 'high_quotient' or
                        values[1].operation != 'call' or values[1].arguments[0] != 'low16' or
                        _var(values[1].arguments[1]) != 'low_division' or target != '%d1'):
                    raise CompileError('WORD-pair join requires allocated high quotient and retained low division')
                self.move(self.reg(values[0]), target, 16)
                self.instruction('swap', target, role='word_pair_join')
                self.flags = (target, 32)
            else:
                self.call(value, target)
        elif op == 'negate':
            self.expression(args[0], target, width)
            self.instruction('neg.' + ('w' if width == 16 else 'l'), target, role='negate')
            self.flags = (target, width)
        elif op in ('add', 'sub', 'and', 'shift'):
            left, right = args
            self.expression(left, target, width)
            if op == 'shift':
                count = _constant(right)
                if type(count) is not int or not 1 <= count <= 8:
                    raise CompileError('fixed 1..8 shift count required')
                self.instruction('asl.' + ('w' if width == 16 else 'l'), f'#{count},{target}', role='wrapped_shift')
            elif right.operation == 'constant':
                immediate = _constant(right)
                if type(immediate) is not int:
                    raise CompileError('integer arithmetic literal required')
                mnemonic = 'addq' if op == 'add' and width == 32 and 1 <= immediate <= 8 else 'subq' if op == 'sub' and width == 32 and 1 <= immediate <= 8 else {'add': 'addi', 'sub': 'subi', 'and': 'andi'}[op]
                self.instruction(mnemonic + ('.w' if width <= 16 else '.l'), f'#{immediate},{target}', role='arithmetic')
            else:
                self.instruction({'add': 'add', 'sub': 'sub', 'and': 'and'}[op] + ('.w' if width <= 16 else '.l'), self.reg(right) + ',' + target, role='arithmetic')
            self.flags = (target, width)
        elif op == 'multiply':
            # General U32 by U16 operation selected as two partial products.
            left, right = args
            if width != 32 or left.operation != 'variable' or left.width != 32 or right.operation != 'variable' or right.width != 16:
                raise CompileError('general product supports one full LONG and one full WORD; other product families must be explicit')
            source, factor = self.reg(left), self.reg(right)
            temporary = '%d4'
            self.move(source, temporary, 32)
            self.instruction('swap', temporary, role='multiply_high_half')
            self.instruction('mulu.w', factor + ',' + temporary, role='multiply_high_half')
            self.instruction('swap', temporary, role='multiply_high_half')
            self.instruction('clr.w', temporary, role='discard_high_product_overflow')
            self.move(source, target, 32)
            self.instruction('mulu.w', factor + ',' + target, role='multiply_low_half')
            self.instruction('add.l', temporary + ',' + target, role='wrapped_product_join')
            self.flags = (target, 32)
        else:
            raise CompileError(f'unsupported typed value selection {op}')

    def evaluate(self, expression):
        if expression.operation == 'call':
            self.call(expression)
            return
        receiver, method, *args = expression.arguments
        if method == 'clear_queue_flag':
            self.instruction('move.w', '#0,0xd448:w', role='write')
        elif method == 'store_seed':
            self.instruction('move.l', self.reg(args[0]) + ',0xf61c:w', role='write')
        elif method == 'rewind_probe':
            self.instruction('tst.b', '-(%a0)', role='live_predecrement_read')
        elif method == 'write':
            if receiver == 'queue':
                self.instruction('move.b', self.reg(args[0]) + ',(%a0)', role='write')
            else:
                self.instruction('move.l', self.reg(args[1]) + f',(%a0,{self.reg(args[0])}.w)', role='write')
        elif method == 'write_next':
            self.instruction('move.b', '#' + str(_constant(args[0])) + ',(%a0)+', role='live_postincrement_write')
        else:
            raise CompileError('unsupported typed side effect')
        self.flags = None

    def compare(self, test):
        op, args = test.operation, test.arguments
        if op == 'not':
            return self.compare(args[0]), True
        if op == 'call' and args[0] in ('negative_byte', 'negative_long'):
            value = args[1]
            register = self.reg(value)
            if self.flags != (register, 8 if args[0] == 'negative_byte' else 32):
                self.instruction('tst.' + ('b' if args[0] == 'negative_byte' else 'l'), register, role='sign_gate')
            return 'bmi'
        if op not in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            raise CompileError('typed comparison gate required')
        left, right = args
        if left.operation == 'method' and left.arguments[1] == 'read_next':
            self.instruction('cmpi.b', '#' + str(_constant(right)) + ',(%a0)+', role='live_postincrement_compare')
        else:
            register = self.reg(left)
            width = _unwrap(left).width if left.operation != 'call' else left.width
            width = 16 if self.binding.rule.startswith('submit_') or self.binding.rule == 'append_queue' else max(16, width)
            if right.operation == 'method' and right.arguments[1] == 'player_owner':
                slot = _constant(right.arguments[2])
                if type(slot) is not int or not 0 <= slot <= 2:
                    raise CompileError('explicit live owner WORD binding required')
                self.instruction('cmp.w', f'0x{0xF67A + 2 * slot:x}:w,{register}', role='live_compare_read')
            elif right.operation == 'constant':
                literal = _constant(right)
                if literal == 0 and self.flags == (register, width):
                    pass
                elif literal == 0:
                    self.instruction('tst.' + ('w' if width == 16 else 'l'), register, role='zero_gate')
                else:
                    self.instruction('cmpi.' + ('w' if width == 16 else 'l'), f'#{literal},{register}', role='comparison')
            else:
                self.instruction('cmp.' + ('w' if width == 16 else 'l'), self.reg(right) + ',' + register, role='comparison')
        return {'eq': 'beq', 'ne': 'bne', 'lt': 'bcs', 'le': 'bls', 'gt': 'bhi', 'ge': 'bcc'}[op]

    @staticmethod
    def inverse(branch):
        return {'beq': 'bne', 'bne': 'beq', 'bcs': 'bcc', 'bcc': 'bcs', 'bhi': 'bls', 'bls': 'bhi', 'bmi': 'bpl', 'bpl': 'bmi'}[branch]

    def gate(self, test, destination, *, when_true=True, size='b'):
        branch = self.compare(test)
        if isinstance(branch, tuple):
            branch = self.inverse(branch[0])
        if not when_true:
            branch = self.inverse(branch)
        self.instruction(branch + '.' + size, destination, role='conditional_branch')
        self.flags = None

    def returned(self, value):
        result = RETURN_REGISTER.get(self.binding.rule, 'd0')
        if value is not None and value.operation == 'call' and isinstance(result, tuple):
            self.call(value)
            value = None
        if value is not None and value.operation == 'tuple':
            items = list(zip(value.arguments, result))
            # Parallel tuple results cannot overwrite an input needed by the
            # other result. Acyclic two-result moves are scheduled accordingly.
            if len(items) != 2:
                raise CompileError('exact quotient/remainder pair required')
            if _unwrap(items[1][0]).operation == 'variable' and self.reg(items[1][0]) == '%' + items[0][1] and not (_unwrap(items[0][0]).operation == 'variable' and self.reg(items[0][0]) == '%' + items[0][1]):
                items.reverse()
            for item, register in items:
                self.expression(item, '%' + register, 32)
        elif value is not None:
            self.expression(value, '%' + result, FUNCTION_TYPES[self.binding.rule])
        for register in reversed(PRESERVED.get(self.binding.rule, ())):
            self.instruction('movem.l', '(%a7)+,%' + register, role='ABI_restore')
        if self.word_frame:
            self.instruction('move.w', '(%a7)+,%d3', role='ABI_WORD_restore')
        if self.local_frame:
            self.instruction('movem.l', '(%a7)+,' + '/'.join('%' + reg for reg in LOCAL_PRESERVED[self.binding.rule]), role='ABI_local_restore')
        self.instruction('rts', role='return')

    def early_return_label(self, value):
        register = self.reg(value) if value is not None else None
        key = register
        if key not in self.tail_returns:
            self.tail_returns[key] = (self.new_label('return'), value)
        return self.tail_returns[key][0]

    def assign(self, names, value):
        if len(names) == 2:
            result = RETURN_REGISTER.get(value.arguments[0]) if value.operation == 'call' else None
            if not isinstance(result, tuple) or tuple(self.registers.get(name) for name in names) != result:
                raise CompileError('tuple result requires exact allocated quotient/remainder destinations')
            self.call(value)
            return
        name = names[0]
        if name not in self.registers:
            raise CompileError('semantic local lacks fixed ABI allocation')
        register = '%' + self.registers[name]
        if self.registers[name] in LOCAL_PRESERVED.get(self.binding.rule, ()) and not self.local_frame:
            self.instruction('movem.l', '/'.join('%' + reg for reg in LOCAL_PRESERVED[self.binding.rule]) + ',-(%a7)', role='ABI_live_local_preserve')
            self.local_frame = True
        if name == 'offset' and _unwrap(value).operation == 'shift' and _var(_unwrap(value).arguments[0]) == 'saved_city':
            self.instruction('movem.l', '%d7,-(%a7)', role='retained_live_city_spill')
            self.saved_city = True
            self.registers['offset'] = 'd7'
            register = '%d7'
        if self.binding.rule == 'word_pair_divmod' and name == 'remainder':
            if value.operation != 'call' or value.arguments[0] != 'high16' or _var(value.arguments[1]) != 'low_division':
                raise CompileError('WORD remainder extraction requires live low division high half')
            self.instruction('swap', '%d1', role='word_remainder_extract')
            self.literal(0, register, 32)
            self.instruction('move.w', '%d1,' + register, role='word_remainder_extract')
            return
        self.expression(value, register, value.width)

    def decision_cascade(self, effects):
        """Coalesce adjacent pure relation gates, preserving their branch order.

        Supported family: small-denominator tail, equality constant pair, then
        unsigned greater-than constant/input pair. Constants/callee/operands
        come from effects. Unsupported relations fall back to ordinary lowering.
        """
        if len(effects) < 3 or any(effect.operation != 'if' for effect in effects[:3]):
            return False
        tests, bodies = zip(*(effect.arguments for effect in effects[:3]))
        if (tuple(test.operation for test in tests) != ('le', 'eq', 'gt') or
                any(len(body) != 1 or body[0].operation != 'return' for body in bodies) or
                _shape(tests[1].arguments[0]) != _shape(tests[2].arguments[0]) or
                _shape(tests[1].arguments[1]) != _shape(tests[2].arguments[1])):
            return False
        call = bodies[0][0].arguments[0]
        if call.operation != 'call' or call.arguments[0] not in FUNCTION_TYPES:
            return False
        callee = call.arguments[0]
        arguments = ARGUMENTS[callee]
        if any(self.reg(arg) != '%' + REGISTERS[callee][name] for name, arg in zip(arguments, call.arguments[1:])):
            raise CompileError('tail-call relation gate requires matching allocated arguments')
        equal, rest = self.new_label('equal_pair'), self.new_label('nontrivial_pair')
        self.source_line = effects[0].line
        self.gate(tests[0], callee)
        self.source_line = effects[1].line
        self.compare(tests[1])
        self.instruction('beq.b', equal, role='relation_gate')
        self.instruction('bls.b', rest, role='relation_gate')
        self.source_line = effects[2].line
        self.returned(bodies[2][0].arguments[0])
        self.label(equal)
        self.source_line = effects[1].line
        self.returned(bodies[1][0].arguments[0])
        self.label(rest)
        return True

    def split_product(self, effects):
        """Select two explicit WORD products and their word-rotation sum.

        This operation intentionally does not insert CLR.W. It therefore
        retains the rotated high-product contribution unlike wrapped_product.
        """
        if len(effects) < 3 or any(effect.operation != 'assign' or len(effect.arguments[0]) != 1 for effect in effects[:3]):
            return False
        names = [effect.arguments[0][0] for effect in effects[:3]]
        values = [_unwrap(effect.arguments[1]) for effect in effects[:3]]
        low, high, total = values
        if low.operation != 'multiply' or high.operation != 'multiply' or total.operation != 'add' or names[0] != names[2]:
            return False
        la, lq = low.arguments
        ha, hq = high.arguments
        if (not _is_call(effects[0].arguments[1], 'u32') or not _is_call(effects[1].arguments[1], 'u32') or
                not _is_call(la, 'low16') or not _is_call(lq, 'low16') or not _is_call(ha, 'high16') or not _is_call(hq, 'low16') or
                _shape(la.arguments[1]) != _shape(ha.arguments[1]) or _shape(lq.arguments[1]) != _shape(hq.arguments[1]) or
                total.arguments[0].operation != 'variable' or _var(total.arguments[0]) != names[0] or
                not _is_call(total.arguments[1], 'swap_words') or _var(total.arguments[1].arguments[1]) != names[1]):
            return False
        product, temporary = '%' + self.registers[names[0]], '%' + self.registers[names[1]]
        source, factor = self.reg(la.arguments[1]), self.reg(lq.arguments[1])
        if len({product, temporary, source, factor}) != 4:
            raise CompileError('split-product ABI live ranges overlap')
        self.source_line = effects[0].line
        self.move(source, product, 32)
        self.move(source, temporary, 32)
        self.instruction('swap', temporary, role='high_WORD_extract')
        self.instruction('mulu.w', factor + ',' + product, role='low_WORD_product')
        self.source_line = effects[1].line
        self.instruction('mulu.w', factor + ',' + temporary, role='high_WORD_product')
        self.source_line = effects[2].line
        self.instruction('swap', temporary, role='retained_half_rotation')
        self.instruction('add.l', temporary + ',' + product, role='wrapped_rotated_product')
        self.flags = (product, 32)
        return True

    def correction_loop(self, effects):
        """Unsigned estimate correction using SUB carry and live remainder.

        The peephole proves both complementary arithmetic expressions before
        reusing the subtraction result. It is not a function-name selection.
        """
        if len(effects) != 7 or not self.split_product(effects):
            return False
        above, remainder_effect, below, result = effects[3:]
        if above.operation != 'if' or remainder_effect.operation != 'assign' or below.operation != 'if' or result.operation != 'return':
            raise CompileError('split-product correction requires explicit carry/remainder control')
        upper_test, decrement = above.arguments
        lower_test, increment = below.arguments
        remainder = _unwrap(remainder_effect.arguments[1])
        if (upper_test.operation != 'gt' or lower_test.operation != 'le' or remainder.operation != 'sub' or
                _shape(remainder.arguments[0]) != _shape(upper_test.arguments[1]) or
                _shape(remainder.arguments[1]) != _shape(upper_test.arguments[0]) or
                _var(lower_test.arguments[1]) != remainder_effect.arguments[0][0] or
                any(len(body) != 2 or body[0].operation != 'assign' or body[1].operation != 'continue' for body in (decrement, increment))):
            raise CompileError('carry correction relations must retain the same full-LONG operands')
        product = self.reg(upper_test.arguments[0])
        if '%' + self.registers[remainder_effect.arguments[0][0]] != product:
            raise CompileError('difference/remainder requires the same live arithmetic storage')
        minus, done = self.new_label('decrement_estimate'), self.new_label('estimate_done')
        self.source_line = above.line
        self.instruction('sub.l', self.reg(upper_test.arguments[1]) + ',' + product, role='difference_and_unsigned_carry')
        self.instruction('bhi.b', minus, role='unsigned_product_gate')
        self.source_line = remainder_effect.line
        self.instruction('neg.l', product, role='unsigned_remainder')
        self.source_line = below.line
        branch = self.compare(lower_test)
        self.instruction(self.inverse(branch) + '.b', done, role='remainder_gate')
        self.body(increment)
        self.label(minus)
        self.body(decrement)
        self.label(done)
        self.source_line = result.line
        self.returned(result.arguments[0])
        return True

    def body(self, effects):
        index = 0
        # Host-only input contracts assert the same already fixed-width ABI
        # arguments; they are checked and emit no target runtime operations.
        while index < len(effects) and effects[index].operation == 'assign' and _is_call(effects[index].arguments[1], 'checked_long'):
            self.assign(*effects[index].arguments)
            index += 1
        if self.decision_cascade(effects[index:]):
            index += 3
        while index < len(effects):
            effect = effects[index]
            self.source_line = effect.line
            op, args = effect.operation, effect.arguments
            if op == 'assign':
                # Count initialization can be scheduled ahead of constructing a
                # side-effect-free RAM view. No reads/writes are reordered.
                if index + 1 < len(effects) and effects[index + 1].operation == 'for':
                    loop = effects[index + 1]
                    count = _constant(loop.arguments[1].arguments[1])
                    if type(count) is not int or not 1 <= count <= 128:
                        raise CompileError('explicit bounded DBRA allocation required')
                    self.literal(count - 1, '%' + self.registers[loop.arguments[0]], 32)
                self.assign(*args)
            elif op == 'evaluate':
                self.evaluate(args[0])
            elif op == 'for':
                label = self.new_label('counted_loop')
                self.label(label)
                self.body(args[2])
                self.instruction('dbra', '%' + self.registers[args[0]] + ',' + label, role='counted_loop')
            elif op == 'while':
                test, body = args
                label = self.new_label('loop')
                self.label(label)
                self.loop.append(label)
                if test.operation == 'constant' and test.arguments[0] is True:
                    if not self.correction_loop(body):
                        self.body(body)
                elif all(effect.operation == 'pass' for effect in body):
                    self.gate(test, label)
                else:
                    raise CompileError('only explicit rejection loops or live sentinel loops supported')
                self.loop.pop()
            elif op == 'continue':
                if not self.loop:
                    raise CompileError('continue requires an active supported loop')
                self.instruction('bra.b', self.loop[-1], role='loop_continue')
            elif op == 'if':
                test, body = args
                self.condition_index += 1
                if len(body) == 1 and body[0].operation == 'return' and self.binding.rule.startswith('submit_'):
                    destination = self.early_return_label(body[0].arguments[0])
                    size = 'b' if test.operation == 'call' and test.arguments[0] == 'negative_byte' else 'w'
                    self.gate(test, destination, size=size)
                elif test.operation == 'or':
                    enter, leave = self.new_label('or_true'), self.new_label('or_end')
                    for value in test.arguments[:-1]:
                        self.gate(value, enter)
                    self.gate(test.arguments[-1], leave, when_true=False)
                    self.label(enter)
                    self.body(body)
                    self.label(leave)
                elif len(body) == 1 and body[0].operation == 'return' and self.loop:
                    # Rejection sampling uses the inverse branch to the same
                    # live RNG call. It does not replace RNG with host random.
                    self.gate(test, self.loop[-1], when_true=False)
                    self.returned(body[0].arguments[0])
                else:
                    leave = self.new_label('if_end')
                    self.gate(test, leave, when_true=False)
                    self.body(body)
                    self.label(leave)
            elif op == 'return':
                value = args[0]
                if value is not None and value.operation == 'call' and value.arguments[0] in FUNCTION_TYPES and self.binding.rule in ('signed_divmod', 'positive_denominator'):
                    # Adjacent semantic helper is the original tail fallthrough.
                    expected = {'signed_divmod': 'positive_denominator', 'positive_denominator': 'unsigned_divmod'}[self.binding.rule]
                    if (value.arguments[0] != expected or len(value.arguments) != 3 or
                            any(argument.operation != 'variable' or argument.width != 32 or _var(argument) != name or self.reg(argument) != '%' + REGISTERS[expected][name]
                                for argument, name in zip(value.arguments[1:], ('numerator', 'denominator'))) or
                            next(binding.entry for binding in BINDINGS if binding.name == expected) != self.binding.end):
                        raise CompileError('tail fallthrough requires the exact adjacent helper and complete live numerator/denominator inputs')
                else:
                    if self.saved_city:
                        self.instruction('movem.l', '(%a7)+,%d7', role='retained_live_city_restore')
                        self.saved_city = False
                    if value is not None and _unwrap(value).operation == 'variable' and self.reg(value) in self.tail_returns:
                        label, _ = self.tail_returns.pop(self.reg(value))
                        self.label(label)
                    # Values already in the result register branch directly to
                    # shared RTS; this preserves the first event's negative gate.
                    result = RETURN_REGISTER.get(self.binding.rule, 'd0')
                    if isinstance(result, str) and '%' + result in self.tail_returns:
                        if value is not None:
                            self.expression(value, '%' + result, FUNCTION_TYPES[self.binding.rule])
                        label, _ = self.tail_returns.pop('%' + result)
                        self.label(label)
                        self.returned(None)
                    else:
                        self.returned(value)
            elif op != 'pass':
                raise CompileError('unknown typed statement effect')
            index += 1

    def lower(self, effects):
        self.label(self.binding.name)
        for register in PRESERVED.get(self.binding.rule, ()):
            self.instruction('movem.l', '%' + register + ',-(%a7)', role='ABI_preserve')
        if self.binding.rule == 'word_pair_divmod':
            self.instruction('movem.w', '%d1/%d3,-(%a7)', role='live_argument_WORD_preserve')
            self.word_frame = True
        self.body(effects)
        if self.binding.rule == 'reset_queue':
            self.returned(None)
        for label, value in self.tail_returns.values():
            self.label(label)
            self.returned(value)
        self.label(self.binding.name + '_end')
        return self.lines, self.mapping


def compile_modules(business_source, arithmetic_source, *, selected=None):
    business, arithmetic = semantic_ir(business_source), semantic_ir(arithmetic_source)
    if set(business) != {'reset_queue', 'append_queue', 'scale_field', 'submit_three_fields', 'submit_four_fields', 'submit_classified_fields'}:
        raise CompileError('complete event business module required')
    if set(arithmetic) != set(FUNCTION_TYPES) - set(business):
        raise CompileError('complete deterministic arithmetic module required')
    effects = business | arithmetic
    lines = ['.cpu 68000', '.section .text', '.equ event_mask,0x174f0', '.equ event_factor,0x174fc']
    mappings = {}
    if selected is not None and (type(selected) is not tuple or not selected or any(type(name) is not str for name in selected) or len(set(selected)) != len(selected) or not set(selected) <= {b.name for b in BINDINGS}):
        raise CompileError('explicit nonempty distinct supported unit names required')
    bindings = tuple(b for b in BINDINGS if selected is None or b.name in selected)
    for binding in BINDINGS:
        if binding not in bindings:
            lines.append(f'.equ {binding.name},0x{binding.entry:x}')
    for binding in sorted(bindings, key=lambda item: item.entry):
        lines.extend((f'.org 0x{binding.entry:x}', '.global ' + binding.name, '.global ' + binding.name + '_end'))
        selected, mapping = Selector(binding).lower(effects[binding.rule])
        lines.extend(selected)
        mappings[binding.name] = mapping
    return dict(assembly='\n'.join(lines) + '\n', effects=effects, mappings=mappings,
                allocated_bytes=sum(binding.end - binding.entry for binding in bindings), bindings=bindings,
                full_CPU=False, complete_ROM=False, original_generation_input=False)


def compile_arithmetic(source):
    """Pure shared interface: parse arithmetic and return typed effects.

    Finance may call this parser once; compiled units must still be explicitly
    selected/accounted by its own compatibility allocation, not copied bytes.
    """
    effects = semantic_ir(source)
    if set(effects) != set(FUNCTION_TYPES) - {'reset_queue', 'append_queue', 'scale_field', 'submit_three_fields', 'submit_four_fields', 'submit_classified_fields'}:
        raise CompileError('complete arithmetic source required')
    return effects


def compile_arithmetic_units(source, *, selected=('signed_divmod', 'positive_denominator', 'unsigned_divmod', 'word_pair_divmod')):
    """Pure reusable arithmetic backend, without importing any business file."""
    effects = compile_arithmetic(source)
    if type(selected) is not tuple or not selected or any(type(name) is not str or name not in effects for name in selected) or len(set(selected)) != len(selected):
        raise CompileError('explicit unique arithmetic units required')
    bindings = tuple(binding for binding in BINDINGS if binding.name in selected)
    lines = ['.cpu 68000', '.section .text']
    for binding in BINDINGS:
        if binding.name not in selected:
            lines.append(f'.equ {binding.name},0x{binding.entry:x}')
    mappings = {}
    for binding in sorted(bindings, key=lambda item: item.entry):
        lines.extend((f'.org 0x{binding.entry:x}', '.global ' + binding.name, '.global ' + binding.name + '_end'))
        selected_lines, mapping = Selector(binding).lower(effects[binding.rule])
        lines.extend(selected_lines)
        mappings[binding.name] = mapping
    return dict(assembly='\n'.join(lines) + '\n', effects=effects, mappings=mappings, bindings=bindings,
                allocated_bytes=sum(binding.end - binding.entry for binding in bindings),
                full_CPU=False, complete_ROM=False, original_generation_input=False)
