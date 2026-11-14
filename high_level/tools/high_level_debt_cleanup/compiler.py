"""Typed policy AST -> ordinary 68000 operations. This module has no file I/O."""
import ast
from dataclasses import dataclass, asdict
from .target import BINDINGS, REGISTERS, VIEW_BASES, BRANCH_HINTS, validate_binding


class CompileError(ValueError):
    pass


@dataclass(frozen=True)
class Expr:
    kind: str
    type: str
    value: object = None
    args: tuple = ()

    def __post_init__(self):
        validate_expr(self)


@dataclass(frozen=True)
class Effect:
    kind: str
    target: str = ''
    value: object = None
    body: tuple = ()
    otherwise: tuple = ()

    def __post_init__(self):
        if (type(self.kind) is not str or self.kind not in ('assign', 'effect', 'if', 'loop', 'continue') or
                type(self.target) is not str or type(self.body) is not tuple or type(self.otherwise) is not tuple or
                any(type(e) is not Effect for e in self.body + self.otherwise)):
            raise CompileError('strict typed effect shape required')
        if self.kind == 'continue':
            if self.target or self.value is not None or self.body or self.otherwise:
                raise CompileError('continue has no payload')
            return
        if type(self.value) is not Expr:
            raise CompileError('typed expression payload required')
        if self.kind == 'assign' and (not self.target.isidentifier() or self.body or self.otherwise):
            raise CompileError('strict assignment effect required')
        if self.kind == 'effect' and (self.target or self.value.type != 'None' or self.body or self.otherwise):
            raise CompileError('strict write effect required')
        if self.kind == 'if' and (self.target or self.value.type != 'Bool'):
            raise CompileError('typed branch required')
        if self.kind == 'loop' and (self.target != 'index' or self.value.type != 'Loop' or self.otherwise):
            raise CompileError('typed counted loop required')


INTRINSICS = {'u16', 'low8', 'negative_byte', 'update_flag', 'DebtState'}
METHODS = {
    ('State', 'records_reverse'): ((), 'Records'), ('State', 'records_forward'): ((), 'Records'),
    ('State', 'owners'): ((), 'Owners'), ('State', 'principals'): ((), 'Principals'),
    ('State', 'selected_word'): ((), 'Word'), ('State', 'flags'): ((), 'Word'),
    ('State', 'store_flags'): (('Word',), 'None'),
    ('Records', 'first_city'): ((), 'Byte'), ('Records', 'second_city'): ((), 'Byte'),
    ('Records', 'clear'): ((), 'None'), ('Owners', 'read'): (('Word',), 'Byte'),
    ('Principals', 'clear'): (('Word',), 'None'),
}


def _integer(value, low=0, high=65535):
    if type(value) is not int or not low <= value <= high:
        raise CompileError('strict finite integer constant required')
    return value


def validate_expr(value):
    if (type(value.kind) is not str or type(value.type) is not str or type(value.args) is not tuple or
            any(type(a) is not Expr for a in value.args)):
        raise CompileError('strict expression field types required')
    kind, typ, payload, args = value.kind, value.type, value.value, value.args
    if kind == 'local':
        if typ not in ('State', 'Word', 'Records', 'Owners', 'Principals') or type(payload) is not str or not payload.isidentifier() or args:
            raise CompileError('typed local required')
    elif kind == 'constant':
        if typ == 'Word':
            _integer(payload)
        elif typ != 'Mode' or type(payload) is not str or payload not in ('clear', 'set'):
            raise CompileError('strict WORD/mode literal required')
        if args:
            raise CompileError('literal has no operands')
    elif kind == 'method':
        if type(payload) is not str or not args or args[0].kind != 'local':
            raise CompileError('typed live receiver required')
        contract = METHODS.get((args[0].type, payload))
        if contract is None or typ != contract[1] or tuple(a.type for a in args[1:]) != contract[0]:
            raise CompileError('strict member/call contract required')
    elif kind == 'shift':
        _integer(payload, 1, 8)
        if typ != 'Wide' or len(args) != 1 or args[0].type != 'Word':
            raise CompileError('WORD shift operands required')
    elif kind in ('word', 'low8', 'negative'):
        expected = {'word': ('Word', ('Word', 'Byte', 'Wide')), 'low8': ('Byte', ('Word',)), 'negative': ('Bool', ('Byte',))}[kind]
        if payload is not None or typ != expected[0] or len(args) != 1 or args[0].type not in expected[1]:
            raise CompileError('strict unary typed operation required')
    elif kind == 'flag':
        if payload is not None or typ != 'Word' or tuple(a.type for a in args) != ('Word', 'Word', 'Mode'):
            raise CompileError('strict flag value/bit/mode required')
    elif kind == 'compare':
        if typ != 'Bool' or type(payload) is not str or payload not in ('eq', 'ne') or len(args) != 2 or any(a.type not in ('Word', 'Byte') for a in args):
            raise CompileError('typed numeric equality required')
    elif kind in ('reverse_slots', 'forward_slots'):
        _integer(payload, 1, 32767)
        if typ != 'Loop' or len(args) != 1 or args[0].type != 'Records':
            raise CompileError('typed record iterator required')
    else:
        raise CompileError('unknown expression operation')


class Frontend:
    def __init__(self, function, binding):
        self.binding = binding
        self.names = {'state': 'State'}
        if (function.name != binding.name or function.decorator_list or function.returns is None or
                not isinstance(function.returns, ast.Constant) or function.returns.value is not None or
                len(function.args.args) != 1 or function.args.args[0].arg != 'state' or
                not isinstance(function.args.args[0].annotation, ast.Name) or
                function.args.args[0].annotation.id != 'DebtState' or function.args.posonlyargs or
                function.args.kwonlyargs or function.args.vararg or function.args.kwarg or function.args.defaults):
            raise CompileError('explicit one-state / None policy interface required')

    def expr(self, node):
        if isinstance(node, ast.Name):
            if node.id not in self.names:
                raise CompileError('undefined typed local')
            return Expr('local', self.names[node.id], node.id)
        if isinstance(node, ast.Constant):
            if type(node.value) is int:
                return Expr('constant', 'Word', _integer(node.value))
            if type(node.value) is str and node.value in ('clear', 'set'):
                return Expr('constant', 'Mode', node.value)
            raise CompileError('unsupported / bool / float literal')
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.LShift):
            value, shift = self.expr(node.left), self.expr(node.right)
            if value.type != 'Word' or shift.kind != 'constant':
                raise CompileError('WORD constant-shift operands required')
            _integer(shift.value, 1, 8)
            return Expr('shift', 'Wide', shift.value, (value,))
        if isinstance(node, ast.Compare):
            if len(node.ops) != 1 or not isinstance(node.ops[0], (ast.Eq, ast.NotEq)) or len(node.comparators) != 1:
                raise CompileError('single equality comparison required')
            left, right = self.expr(node.left), self.expr(node.comparators[0])
            if left.type not in ('Word', 'Byte') or right.type not in ('Word', 'Byte'):
                raise CompileError('numeric equality operands required')
            return Expr('compare', 'Bool', 'eq' if isinstance(node.ops[0], ast.Eq) else 'ne', (left, right))
        if isinstance(node, ast.Call) and not node.keywords:
            args = tuple(self.expr(item) for item in node.args)
            if isinstance(node.func, ast.Name):
                name = node.func.id
                if name == 'u16' and len(args) == 1 and args[0].type in ('Word', 'Byte', 'Wide'):
                    return Expr('word', 'Word', None, args)
                if name == 'low8' and len(args) == 1 and args[0].type == 'Word':
                    return Expr('low8', 'Byte', None, args)
                if name == 'negative_byte' and len(args) == 1 and args[0].type == 'Byte':
                    return Expr('negative', 'Bool', None, args)
                if name == 'update_flag' and tuple(a.type for a in args) == ('Word', 'Word', 'Mode'):
                    return Expr('flag', 'Word', None, args)
                raise CompileError('unknown or ill-typed intrinsic')
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                receiver = self.expr(node.func.value)
                member = node.func.attr
                contract = METHODS.get((receiver.type, member))
                if contract is None or tuple(a.type for a in args) != contract[0]:
                    raise CompileError('unknown member / wrong typed method arguments')
                return Expr('method', contract[1], member, (receiver,) + args)
        raise CompileError('unsupported expression, no raw source fallback')

    def block(self, nodes, in_loop=False):
        result = []
        for node in nodes:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                target = node.targets[0].id
                if target in INTRINSICS or target == 'state' or target not in REGISTERS[self.binding.name]:
                    raise CompileError('reserved or unallocated local')
                value = self.expr(node.value)
                if in_loop and (target == 'index' or value.type in ('Records', 'Owners', 'Principals')):
                    raise CompileError('counted iterator/local views cannot be rebound in its body')
                if value.type in ('None', 'Bool', 'Wide', 'Mode'):
                    raise CompileError('unsupported assignment type')
                previous = self.names.get(target)
                target_type = 'Word' if value.type == 'Byte' else value.type
                if previous is not None and previous != target_type:
                    raise CompileError('local type changed')
                self.names[target] = target_type
                result.append(Effect('assign', target, value))
            elif isinstance(node, ast.Expr):
                value = self.expr(node.value)
                if value.type != 'None':
                    raise CompileError('discarded value/effect not admitted')
                result.append(Effect('effect', value=value))
            elif isinstance(node, ast.If):
                condition = self.expr(node.test)
                if condition.type != 'Bool':
                    raise CompileError('typed Boolean condition required')
                before = dict(self.names)
                body = self.block(node.body, in_loop)
                first = dict(self.names)
                self.names = dict(before)
                other = self.block(node.orelse, in_loop)
                second = dict(self.names)
                self.names = {k: v for k, v in first.items() if second.get(k) == v}
                result.append(Effect('if', value=condition, body=body, otherwise=other))
            elif isinstance(node, ast.For):
                if (in_loop or node.orelse or not isinstance(node.target, ast.Name) or node.target.id != 'index' or
                        not isinstance(node.iter, ast.Call) or node.iter.keywords or len(node.iter.args) != 1 or
                        not isinstance(node.iter.func, ast.Attribute) or not isinstance(node.iter.func.value, ast.Name)):
                    raise CompileError('one explicit counted record loop required')
                receiver = self.expr(node.iter.func.value)
                mode = node.iter.func.attr
                count = self.expr(node.iter.args[0])
                if receiver.type != 'Records' or mode not in ('reverse_slots', 'forward_slots') or count.kind != 'constant':
                    raise CompileError('strict record iterator/count required')
                _integer(count.value, 1, 32767)
                self.names['index'] = 'Word'
                result.append(Effect('loop', 'index', Expr(mode, 'Loop', count.value, (receiver,)), self.block(node.body, True)))
            elif isinstance(node, ast.Continue) and in_loop:
                result.append(Effect('continue'))
            else:
                raise CompileError('unsupported statement / nested loop / return')
        return tuple(result)


class Lowering:
    def __init__(self, binding):
        validate_binding(binding)
        self.binding, self.regs = binding, REGISTERS[binding.name]
        self.lines, self.instructions, self.serial, self.branch_serial = [], [], 0, 0
        self.zero_byte = set()
        self.flags = None
        self.views = {}
        self.live = {}

    def fresh(self, role):
        self.serial += 1
        return f'{self.binding.name}_{role}_{self.serial}'

    def ins(self, operation, operands='', width=2):
        label = f'hl_{self.binding.name}_{len(self.instructions)}'
        self.lines += [f'.global {label}', label + ':', '    ' + operation + (' ' + operands if operands else '')]
        self.instructions.append({'symbol': label, 'operation': operation, 'operands': operands, 'encoding_bytes': width})

    def reg(self, value):
        if value.kind != 'local' or value.value not in self.regs or self.live.get(value.value) != self.regs[value.value]:
            raise CompileError('allocated local value required')
        return self.regs[value.value]

    def address(self, value):
        if value.kind != 'method':
            raise CompileError('live method source required')
        receiver = value.args[0]
        if value.value in ('first_city', 'second_city'):
            return ('(%' + self.reg(receiver) + ')', 2) if value.value == 'first_city' else ('1(%' + self.reg(receiver) + ')', 4)
        if value.value == 'read' and receiver.type == 'Owners':
            index = self.reg(value.args[1])
            return f'(%{self.reg(receiver)},%{index}.w)', 4
        if receiver.type == 'State' and value.value in ('flags', 'selected_word'):
            return ('0xe700:w' if value.value == 'flags' else '0xf3a8:w', 4)
        raise CompileError('unsupported live read source')

    def assign(self, effect):
        target, value = effect.target, effect.value
        dst = self.regs[target]
        if value.type in ('Records', 'Owners', 'Principals'):
            if value.kind != 'method' or value.args[0].type != 'State' or value.value not in VIEW_BASES:
                raise CompileError('explicit state view constructor required')
            self.ins('lea', f'0x{VIEW_BASES[value.value]:x}:w,%{dst}', 4)
            self.views[target] = value.value
            self.bind(target, dst)
            return
        if value.kind == 'word':
            value = value.args[0]
        if value.kind == 'constant':
            if value.value == 0:
                self.ins('clr.w', '%' + dst)
                self.zero_byte.add(dst)
            else:
                self.ins('move.w', f'#{value.value},%{dst}', 4)
                self.zero_byte.discard(dst)
            self.flags = (dst, 16)
        elif value.kind == 'method':
            source, width = self.address(value)
            if value.type == 'Byte':
                if dst not in self.zero_byte:
                    raise CompileError('BYTE-to-WORD assignment requires proven zero preserved upper BYTE')
                self.ins('move.b', source + ',%' + dst, width)
                self.flags = (dst, 8)
            else:
                self.ins('move.w', source + ',%' + dst, width)
                self.zero_byte.discard(dst)
                self.flags = (dst, 16)
        elif value.kind == 'shift':
            source = self.reg(value.args[0])
            if source != dst:
                self.ins('move.w', '%' + source + ',%' + dst)
            self.ins('lsl.w', f'#{value.value},%{dst}')
            self.zero_byte.discard(dst)
            self.flags = (dst, 16)
        elif value.kind == 'local':
            source = self.reg(value)
            if source != dst:
                self.ins('move.w', '%' + source + ',%' + dst)
            self.zero_byte.discard(dst)
            self.flags = (dst, 16) if source != dst else self.flags
        elif value.kind == 'flag':
            source, bit, mode = value.args
            if self.reg(source) != dst or mode.kind != 'constant' or mode.type != 'Mode':
                raise CompileError('in-place typed dynamic flag update required')
            self.ins('bclr.l' if mode.value == 'clear' else 'bset.l', '%' + self.reg(bit) + ',%' + dst)
            self.zero_byte.discard(dst)
            self.flags = None
        else:
            raise CompileError('unsupported assignment lowering')
        self.bind(target, dst)

    def bind(self, target, register):
        self.live = {name: reg for name, reg in self.live.items() if reg != register}
        self.live[target] = register

    def effect(self, value):
        if value.kind != 'method':
            raise CompileError('effect must be typed method')
        receiver = value.args[0]
        if value.value == 'clear' and receiver.type == 'Records':
            self.ins('clr.l', '(%' + self.reg(receiver) + ')')
        elif value.value == 'clear' and receiver.type == 'Principals':
            self.ins('clr.l', f'(%{self.reg(receiver)},%{self.reg(value.args[1])}.w)', 4)
        elif value.value == 'store_flags' and receiver.type == 'State':
            self.ins('move.w', '%' + self.reg(value.args[1]) + ',0xe700:w', 4)
        else:
            raise CompileError('unknown typed write effect')
        self.flags = None

    def condition(self, value):
        if value.kind == 'negative':
            source, width = self.address(value.args[0])
            self.ins('tst.b', source, width)
            self.flags = None
            return 'bmi', 'bpl'
        if value.kind != 'compare':
            raise CompileError('typed comparison required')
        left, right = value.args
        if left.kind == 'method' and left.type == 'Byte' and right.kind == 'low8':
            source, width = self.address(left)
            self.ins('cmp.b', source + ',%' + self.reg(right.args[0]), width)
        elif left.kind == 'local' and right.kind == 'constant':
            reg = self.reg(left)
            if not (right.value == 0 and self.flags in ((reg, 16), (reg, 8)) and
                    (self.flags[1] == 16 or reg in self.zero_byte)):
                self.ins('cmpi.w', f'#{right.value},%{reg}', 4)
        else:
            raise CompileError('unsupported comparison operand layout')
        self.flags = None
        return ('beq', 'bne') if value.value == 'eq' else ('bne', 'beq')

    def branch_width(self):
        hints = BRANCH_HINTS[self.binding.name]
        if self.branch_serial >= len(hints):
            raise CompileError('new branch needs explicit encoding compatibility hint')
        result = hints[self.branch_serial]
        self.branch_serial += 1
        return result

    def block(self, effects, continuation=None, footer=None):
        for position, item in enumerate(effects):
            last = position == len(effects) - 1
            if item.kind == 'assign':
                self.assign(item)
            elif item.kind == 'effect':
                self.effect(item.value)
            elif item.kind == 'continue':
                if not last or footer is None:
                    raise CompileError('terminal counted-loop continue required')
                self.ins('bra.w', footer, 4)
            elif item.kind == 'if':
                size = self.branch_width()
                true_branch, false_branch = self.condition(item.value)
                if len(item.body) == 1 and item.body[0].kind == 'continue' and not item.otherwise:
                    if footer is None:
                        raise CompileError('continue requires loop footer')
                    self.ins(true_branch + '.' + size, footer, 2 if size == 'b' else 4)
                    continue
                join = continuation if last and continuation is not None else self.fresh('join')
                alternative = self.fresh('else') if item.otherwise else join
                self.ins(false_branch + '.' + size, alternative, 2 if size == 'b' else 4)
                before = set(self.zero_byte)
                before_live = dict(self.live)
                before_views = dict(self.views)
                self.block(item.body, join, footer)
                first = set(self.zero_byte)
                first_live = dict(self.live)
                if item.otherwise:
                    self.ins('bra.' + size, join, 2 if size == 'b' else 4)
                    self.lines.append(alternative + ':')
                    self.zero_byte = set(before)
                    self.live = dict(before_live)
                    self.views = dict(before_views)
                    self.flags = None
                    self.block(item.otherwise, join, footer)
                    first &= self.zero_byte
                    first_live = {name: reg for name, reg in first_live.items() if self.live.get(name) == reg}
                else:
                    first &= before
                    first_live = {name: reg for name, reg in first_live.items() if before_live.get(name) == reg}
                self.zero_byte = first
                self.live = first_live
                self.flags = None
                if not (last and continuation is not None):
                    self.lines.append(join + ':')
            elif item.kind == 'loop':
                if footer is not None:
                    raise CompileError('nested target loop unsupported')
                value = item.value
                cursor, index = self.reg(value.args[0]), self.regs[item.target]
                direction = -1 if value.kind == 'reverse_slots' else 1
                if self.views.get(value.args[0].value) != ('records_reverse' if direction < 0 else 'records_forward'):
                    raise CompileError('iterator must match live view direction')
                loop, end = self.fresh('loop'), self.fresh('footer')
                if direction < 0:
                    self.ins('move.w', f'#{value.value - 1},%{index}', 4)
                elif index not in self.zero_byte:
                    raise CompileError('forward loop requires explicit zero WORD index')
                self.bind(item.target, index)
                self.lines.append(loop + ':')
                self.flags = None
                self.block(item.body, end, end)
                self.lines.append(end + ':')
                self.ins('subq.l' if direction < 0 else 'addq.l', '#4,%' + cursor)
                if direction < 0:
                    self.ins('dbra', '%' + index + ',' + loop, 4)
                else:
                    self.ins('addq.w', '#1,%' + index)
                    self.ins('cmpi.w', f'#{value.value},%{index}', 4)
                    self.ins('bcs.b', loop)
                # Python keeps its last yielded index, whereas the original
                # DBRA/ADDQ latch leaves FFFF/count. It is not a live value
                # after this compatibility loop; a later explicit assignment
                # may reestablish a value, but an unproven reuse is refused.
                self.live.pop(item.target, None)
                self.zero_byte.discard(index)
                self.flags = None
            else:
                raise CompileError('unknown effect kind')

    def lower(self, effects):
        name = self.binding.name
        self.lines = [f'.org 0x{self.binding.entry:x}', '.global ' + name, name + ':']
        if self.binding.preserved:
            mask = '/'.join('%' + reg for reg in self.binding.preserved)
            self.ins('movem.l', mask + ',-(%sp)', 4)
        self.block(effects)
        if self.binding.preserved:
            self.ins('movem.l', '(%sp)+,' + '/'.join('%' + reg for reg in self.binding.preserved), 4)
        self.ins('rts')
        self.lines += ['.global ' + name + '_end', name + '_end:']
        return '\n'.join(self.lines), self.instructions


def compile_source(source):
    if type(source) is not str or len(source) > 100000:
        raise CompileError('bounded text source required')
    try:
        module = ast.parse(source)
    except (SyntaxError, ValueError) as exc:
        raise CompileError('invalid Python source') from exc
    functions, imports = {}, 0
    for node in module.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and type(node.value.value) is str:
            continue
        if isinstance(node, ast.ImportFrom):
            if node.level != 1 or node.module != 'domain' or any(item.asname for item in node.names) or tuple(item.name for item in node.names) != ('DebtState', 'u16', 'low8', 'negative_byte', 'update_flag'):
                raise CompileError('only explicit typed domain import required')
            imports += 1
            continue
        if not isinstance(node, ast.FunctionDef) or node.name in functions or node.name in INTRINSICS:
            raise CompileError('only two unique typed policies admitted')
        functions[node.name] = node
    if imports != 1 or set(functions) != {b.name for b in BINDINGS}:
        raise CompileError('exact two policy declarations required')
    units, assembly = [], ['.cpu 68000', '.section .text']
    for binding in BINDINGS:
        frontend = Frontend(functions[binding.name], binding)
        effects = frontend.block(functions[binding.name].body)
        text, instructions = Lowering(binding).lower(effects)
        assembly.append(text)
        units.append({'binding': asdict(binding), 'effects': [asdict(e) for e in effects], 'instructions': instructions})
    return {'assembly': '\n\n'.join(assembly) + '\n', 'units': units,
            'allocated_bytes': sum(b.end - b.entry for b in BINDINGS), 'generation_reads_ROM_or_ASM': False}
