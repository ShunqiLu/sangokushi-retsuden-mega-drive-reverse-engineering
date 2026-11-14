"""Typed member-rule AST to ordinary instructions through separate ABI bindings.

No file reads, original instruction text, encoded payload, source digest, or
function-body template participates in generation.  This deliberately bounded
frontend refuses edits outside its demonstrated scalar/view/control families.
"""
import ast
from dataclasses import dataclass, asdict
from .compiler_common import CompileError, Emitter, require_declared_names
from .source_inline import inline_settlement
from .target import MEMBER_BINDINGS, MEMBER_REGISTERS, TABLE_BINDINGS, SCALAR_BINDINGS


SIGNATURES = {
    'remove_member': ((('state', 'State'), ('officer', 'Word'), ('object_view', 'Table'), ('owner', 'Word'), ('count', 'Word')), 'Outcome'),
    'finish_removal': ((('state', 'State'), ('award', 'Long')), 'Outcome'),
    'transfer_attacker': ((('state', 'State'),), 'None'),
    'transfer_defender': ((('state', 'State'),), 'None'),
    'transfer_members': ((('state', 'State'), ('destination', 'Table'), ('source', 'Table'), ('count', 'Word'), ('doubled_officer', 'Word'), ('carry', 'Word')), 'None'),
    'sync_queues': ((('state', 'State'), ('deleted', 'Word')), 'None'),
}
ANNOTATIONS = {'BattleState': 'State', 'Word': 'Word', 'Long': 'Long', 'Byte': 'Byte', 'Table': 'Table', 'RemovalOutcome': 'Outcome'}
IMPORTS = {'BattleState', 'Table', 'Word', 'Long', 'RemovalOutcome', 'u16', 'low8', 'low16',
           'replace_byte', 'mask_byte', 'zero_extend_word', 'add_low_word', 'divu_retained',
           'negative_byte', 'negative_word', 'descending_inclusive'}
NUMBERS = {'Byte', 'Word', 'Long', 'Wide'}


@dataclass(frozen=True)
class Expr:
    kind: str
    type: str
    value: object = None
    args: tuple = ()


@dataclass(frozen=True)
class Effect:
    kind: str
    target: str = ''
    value: object = None
    body: tuple = ()
    otherwise: tuple = ()


def literal(value, low=-32768, high=65535):
    if type(value) is not int or not low <= value <= high:
        raise CompileError('strict finite integer literal required')
    return value


class Frontend:
    def __init__(self, node):
        if node.name not in SIGNATURES:
            raise CompileError('unknown member business function')
        signature, result = SIGNATURES[node.name]
        actual = []
        for arg in node.args.args:
            if not isinstance(arg.annotation, ast.Name):
                raise CompileError('explicit member argument type required')
            actual.append((arg.arg, ANNOTATIONS.get(arg.annotation.id)))
        ret = 'None' if isinstance(node.returns, ast.Constant) and node.returns.value is None else ANNOTATIONS.get(getattr(node.returns, 'id', None))
        if (tuple(actual) != signature or ret != result or node.decorator_list or node.args.posonlyargs or
                node.args.kwonlyargs or node.args.vararg or node.args.kwarg or node.args.defaults or node.args.kw_defaults):
            raise CompileError('exact typed member ABI signature required')
        self.name, self.result, self.types = node.name, result, dict(signature)
        self.registers = MEMBER_REGISTERS[node.name]

    def expr(self, node):
        if isinstance(node, ast.Name):
            if node.id not in self.types:
                raise CompileError('undefined typed member local')
            return Expr('local', self.types[node.id], node.id)
        if isinstance(node, ast.Constant):
            return Expr('constant', 'Word', literal(node.value))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub) and isinstance(node.operand, ast.Constant):
            return Expr('constant', 'Word', literal(-literal(node.operand.value)))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            operand = self.expr(node.operand)
            if operand.type != 'Bool':
                raise CompileError('logical inversion needs Bool')
            return Expr('not', 'Bool', args=(operand,))
        if isinstance(node, ast.Attribute):
            base = self.expr(node.value)
            if (base.type != 'State' or node.attr not in TABLE_BINDINGS or
                    node.attr in ('pair_queue', 'active_queue')):
                raise CompileError('known semantic state view required')
            return Expr('view', 'Table', node.attr, (base,))
        if isinstance(node, ast.BinOp):
            left, right = self.expr(node.left), self.expr(node.right)
            if left.type not in NUMBERS or right.type not in NUMBERS:
                raise CompileError('typed scalar arithmetic required')
            operations = {ast.Add: 'add', ast.Sub: 'sub', ast.BitAnd: 'and', ast.LShift: 'shl', ast.RShift: 'shr'}
            operation = operations.get(type(node.op))
            if operation is None:
                raise CompileError('unsupported arithmetic family')
            if operation in ('shl', 'shr') and (right.kind != 'constant' or not 1 <= right.value <= 8):
                raise CompileError('finite shift1..8 required')
            return Expr('binary', 'Wide', operation, (left, right))
        if isinstance(node, ast.Compare):
            if len(node.ops) != 1 or len(node.comparators) != 1:
                raise CompileError('single typed comparison required')
            left, right = self.expr(node.left), self.expr(node.comparators[0])
            names = {ast.Eq: 'eq', ast.NotEq: 'ne', ast.Lt: 'lt', ast.LtE: 'le', ast.Gt: 'gt', ast.GtE: 'ge'}
            operation = names.get(type(node.ops[0]))
            if operation is None or left.type not in NUMBERS or right.type not in NUMBERS:
                raise CompileError('supported unsigned scalar comparison required')
            if ((left.type == 'Byte' and right.kind == 'constant' and not 0 <= right.value <= 255) or
                    (right.type == 'Byte' and left.kind == 'constant' and not 0 <= left.value <= 255)):
                raise CompileError('BYTE comparison literal must fit its complete unsigned width')
            return Expr('compare', 'Bool', operation, (left, right))
        if isinstance(node, ast.Call) and not node.keywords:
            args = tuple(self.expr(value) for value in node.args)
            if isinstance(node.func, ast.Name):
                name = node.func.id
                if name == 'Table' and tuple(a.type for a in args) == ('State', 'Long'):
                    return Expr('construct', 'Table', name, args)
                if name in ('u16', 'low16', 'low8', 'zero_extend_word') and len(args) == 1 and args[0].type in NUMBERS:
                    if name in ('u16', 'low16') and args[0].type == 'Byte':
                        raise CompileError('BYTE-to-WORD needs real zero-extension, not retained storage')
                    if name == 'u16' and args[0].kind == 'binary' and any(a.type != 'Word' for a in args[0].args):
                        raise CompileError('WORD arithmetic requires explicit complete WORD operands')
                    if name == 'zero_extend_word' and args[0].type != 'Word':
                        raise CompileError('explicit WORD-to-LONG widening required')
                    typ = {'u16': 'Word', 'low16': 'Word', 'low8': 'Byte', 'zero_extend_word': 'Long'}[name]
                    return Expr('intrinsic', typ, name, args)
                if name == 'replace_byte' and len(args) == 2 and args[0].type in ('Word', 'Long') and args[1].type == 'Byte':
                    return Expr('intrinsic', args[0].type, name, args)
                if name == 'mask_byte' and len(args) == 2 and args[0].type == 'Word' and args[1].kind == 'constant' and 0 <= args[1].value <= 255:
                    return Expr('intrinsic', 'Word', name, args)
                if name == 'add_low_word' and len(args) == 2 and args[0].type == 'Long' and args[1].type == 'Word':
                    return Expr('intrinsic', 'Long', name, args)
                if name == 'divu_retained' and len(args) == 2 and args[0].type == 'Long' and args[1].type == 'Word':
                    return Expr('intrinsic', 'Long', name, args)
                if name in ('negative_byte', 'negative_word') and len(args) == 1 and args[0].type == {'negative_byte': 'Byte', 'negative_word': 'Word'}[name]:
                    return Expr('intrinsic', 'Bool', name, args)
                if name == 'descending_inclusive' and len(args) == 1 and args[0].type == 'Word':
                    return Expr('intrinsic', 'Loop', name, args)
                if name in SIGNATURES and tuple(a.type for a in args) == tuple(t for _, t in SIGNATURES[name][0]):
                    return Expr('call', SIGNATURES[name][1], name, args)
                raise CompileError('unknown intrinsic or exact argument-width mismatch')
            if isinstance(node.func, ast.Attribute):
                receiver = self.expr(node.func.value)
                method = node.func.attr
                if receiver.type == 'State':
                    if method in SCALAR_BINDINGS and not args:
                        width = SCALAR_BINDINGS[method]['width']
                        return Expr('scalar', {8: 'Byte', 16: 'Word', 32: 'Long'}[width], method, (receiver,))
                    if method in ('pair_queue', 'active_queue') and not args:
                        return Expr('view', 'Cursor', method, (receiver,))
                    if method.startswith('set_') and method[4:] in SCALAR_BINDINGS and len(args) == 1:
                        width = SCALAR_BINDINGS[method[4:]]['width']
                        want = {8: ('Byte', 'Word'), 16: ('Word',), 32: ('Long',)}[width]
                        if args[0].type not in want or (width == 8 and args[0].type == 'Word' and
                                (args[0].kind != 'constant' or not 0 <= args[0].value <= 255)):
                            raise CompileError('scalar write exact width required')
                        return Expr('store_scalar', 'None', method[4:], args)
                    if method == 'member_removed' and tuple(a.type for a in args) == ('Long',):
                        return Expr('completion', 'Outcome', method, args)
                if receiver.type in ('Table', 'Cursor'):
                    if method in ('byte', 'word', 'long') and len(args) <= 2 and all(a.type == 'Word' for a in args):
                        return Expr('read', {'byte': 'Byte', 'word': 'Word', 'long': 'Long'}[method], method, (receiver,) + args)
                    if method in ('set_byte', 'set_word', 'set_long') and 2 <= len(args) <= 3 and args[0].type == 'Word' and (len(args) == 2 or args[2].type == 'Word'):
                        typ = {'set_byte': ('Byte', 'Word'), 'set_word': ('Word',), 'set_long': ('Long',)}[method]
                        if args[1].type not in typ or (method == 'set_byte' and args[1].type == 'Word' and
                                (args[1].kind != 'constant' or not 0 <= args[1].value <= 255)):
                            raise CompileError('memory write exact scalar width required')
                        return Expr('write', 'None', method, (receiver,) + args)
                    if method == 'at' and len(args) <= 2 and all(a.type == 'Word' for a in args):
                        return Expr('at', receiver.type, method, (receiver,) + args)
                    if method == 'advance' and len(args) == 1 and args[0].kind == 'constant' and -8 <= args[0].value <= 8 and args[0].value:
                        return Expr('advance', receiver.type, method, (receiver,) + args)
                    if method == 'adjust_after_insertion' and len(args) == 1 and args[0].type == 'Table' and receiver.type == 'Table':
                        return Expr('adjust', 'Table', method, (receiver,) + args)
                    if method == 'change_byte' and len(args) == 1 and args[0].kind == 'constant' and 1 <= abs(args[0].value) <= 8:
                        return Expr('change', 'None', method, (receiver,) + args)
                    if method == 'copy_next_byte' and len(args) == 1 and args[0].type in ('Table', 'Cursor'):
                        return Expr('copy', 'Byte', method, (receiver,) + args)
                    if receiver.type == 'Cursor':
                        if method == 'next_byte' and not args:
                            return Expr('next', 'Byte', method, (receiver,))
                        if method == 'write_relative' and len(args) == 2 and args[0].kind == 'constant' and args[1].type == 'Byte':
                            return Expr('relative_write', 'None', method, (receiver,) + args)
                        if method == 'copy_next_byte_relative' and len(args) == 1 and args[0].kind == 'constant':
                            return Expr('relative_copy', 'Byte', method, (receiver,) + args)
                raise CompileError('unsupported semantic view operation or argument width')
        raise CompileError('unsupported member expression')

    def block(self, statements, *, loop=False):
        result = []
        for node in statements:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and type(node.value.value) is str:
                continue
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                name, value = node.targets[0].id, self.expr(node.value)
                if name not in self.registers or value.type in ('None', 'Bool', 'Outcome', 'Loop', 'Wide', 'State'):
                    raise CompileError('explicit scalar/view ABI local required')
                self.types[name] = value.type
                result.append(Effect('assign', name, value))
            elif isinstance(node, ast.Expr):
                value = self.expr(node.value)
                if value.type not in ('None', 'Byte') or value.kind not in ('store_scalar', 'write', 'change', 'copy', 'relative_write', 'relative_copy', 'call'):
                    raise CompileError('explicit semantic side effect required')
                result.append(Effect('effect', value=value))
            elif isinstance(node, ast.If):
                condition = self.expr(node.test)
                if condition.type != 'Bool' and not (condition.kind == 'binary' and condition.value == 'and' and condition.args[0].type == 'Byte' and condition.args[1].kind == 'constant'):
                    raise CompileError('typed condition or single bit test required')
                previous = dict(self.types)
                yes = self.block(node.body, loop=loop); yes_names = dict(self.types)
                self.types = dict(previous)
                no = self.block(node.orelse, loop=loop); no_names = dict(self.types)
                self.types = {key: value for key, value in yes_names.items() if no_names.get(key) == value}
                result.append(Effect('if', value=condition, body=yes, otherwise=no))
            elif isinstance(node, ast.While) and not node.orelse:
                if isinstance(node.test, ast.Constant) and node.test.value is True:
                    condition = None
                else:
                    condition = self.expr(node.test)
                    if condition.type != 'Bool':
                        raise CompileError('typed while condition required')
                previous = dict(self.types); body = self.block(node.body, loop='while')
                self.types = {key: self.types.get(key, typ) for key, typ in previous.items()}
                result.append(Effect('while', value=condition, body=body))
            elif isinstance(node, ast.For) and isinstance(node.target, ast.Name) and not node.orelse:
                iterator = self.expr(node.iter)
                if iterator.type != 'Loop' or node.target.id not in self.registers or iterator.args[0].kind != 'local' or iterator.args[0].value != node.target.id:
                    raise CompileError('explicit same-storage inclusive countdown required')
                previous = dict(self.types); self.types[node.target.id] = 'Word'
                body = self.block(node.body, loop='counted')
                self.types = dict(previous)
                result.append(Effect('counted', node.target.id, iterator, body))
            elif isinstance(node, ast.Break) and loop:
                result.append(Effect('break'))
            elif isinstance(node, ast.Continue) and loop:
                if loop == 'counted':
                    raise CompileError('counted continue requires a validated decrement latch; currently unsupported')
                result.append(Effect('continue'))
            elif isinstance(node, ast.Pass):
                result.append(Effect('pass'))
            elif isinstance(node, ast.Return):
                value = self.expr(node.value) if node.value is not None else Expr('void', 'None')
                if value.type != self.result or (self.result == 'Outcome' and value.kind not in ('completion', 'call')):
                    raise CompileError('exact return/completion contract required')
                result.append(Effect('return', value=value))
            else:
                raise CompileError('unsupported member statement')
        return tuple(result)


class Lowering:
    def __init__(self, binding, effects):
        self.binding, self.effects, self.e = binding, effects, Emitter(binding)
        self.registers = MEMBER_REGISTERS[binding.name]
        self.live = dict(SIGNATURES[binding.name][0])
        self.last_zero, self.loop_stack = None, []
        self.exit = self.e.fresh('completion')

    def reg(self, name, *, stale=False):
        if name not in self.registers or (not stale and name not in self.live):
            raise CompileError('undefined/clobbered ABI local read')
        return '%' + self.registers[name]

    def invalidate(self, name, typ):
        register = self.registers[name]
        self.live = {key: value for key, value in self.live.items() if key not in self.registers or self.registers[key] != register or key == name}
        self.live[name] = typ

    def ins(self, op, operands='', width=2, *, zero=None):
        self.e.ins(op, operands, width)
        if op not in ('lea', 'adda.w', 'addq.w') or not operands.endswith(tuple('%a'+str(i) for i in range(7))):
            self.last_zero = zero

    def operand(self, value, *, stale=False):
        if value.kind == 'local':
            return self.reg(value.value, stale=stale), 0
        if value.kind == 'constant':
            return '#'+str(value.value), 2
        if value.kind == 'scalar':
            b = SCALAR_BINDINGS[value.value]
            return f"0x{b['address']:x}:{b['suffix']}", 2 if b['suffix'] == 'w' else 4
        if value.kind == 'read':
            return self.memory(value.args[0], value.args[1:])
        if value.kind == 'next':
            return '('+self.reg(value.args[0].value)+')+', 0
        if value.kind == 'intrinsic' and value.value in ('low8', 'low16'):
            return self.operand(value.args[0], stale=stale)
        raise CompileError('expression needs explicit scalar assignment before this use')

    def memory(self, table, args):
        if table.kind != 'local' or table.type not in ('Table', 'Cursor'):
            raise CompileError('live bound view required')
        register = self.reg(table.value)
        offset = args[0] if args else Expr('constant', 'Word', 0)
        displacement = literal(args[1].value) if len(args) > 1 and args[1].kind == 'constant' else 0
        if len(args) > 1 and args[1].kind != 'constant':
            raise CompileError('constant indexed displacement required')
        if offset.kind == 'constant':
            if offset.value != 0:
                raise CompileError('constant nonzero index needs a bound WORD local')
            return (f'{displacement}({register})', 2) if displacement else (f'({register})', 0)
        if offset.type != 'Word':
            raise CompileError('complete WORD index required')
        index = self.operand(offset)[0]
        if not index.startswith('%d'):
            raise CompileError('indexed scalar must be in a data register')
        if not -128 <= displacement <= 127:
            raise CompileError('original brief-index displacement range required')
        return f'{displacement}({register},{index}.w)', 2

    def store(self, value):
        if value.kind == 'store_scalar':
            b = SCALAR_BINDINGS[value.value]
            destination = f"0x{b['address']:x}:{b['suffix']}"
            extension, typ = 2 if b['suffix'] == 'w' else 4, {8: 'b', 16: 'w', 32: 'l'}[b['width']]
            source = value.args[0]
        elif value.kind == 'write':
            table, offset, source = value.args[:3]
            destination, extension = self.memory(table, (offset,) + value.args[3:])
            typ = {'set_byte': 'b', 'set_word': 'w', 'set_long': 'l'}[value.value]
        elif value.kind == 'relative_write':
            receiver, delta, source = value.args
            destination, extension, typ = f'{literal(delta.value)}({self.reg(receiver.value)})', 2, 'b'
        else:
            raise CompileError('strict store effect required')
        if source.kind == 'constant' and source.value == 0:
            self.ins('clr.'+typ, destination, 2+extension)
        else:
            operand, source_extension = self.operand(source)
            if source.kind == 'constant' and typ == 'l': source_extension = 4
            self.ins('move.'+typ, operand+','+destination, 2+extension+source_extension)

    def assign(self, name, value, *, allow_stale=False):
        target = '%'+self.registers[name]
        if value.kind == 'view':
            b = TABLE_BINDINGS[value.value]
            self.ins('lea', f"0x{b['address']:x}:{b['suffix']},"+target, 4 if b['suffix'] == 'w' else 6)
        elif value.kind == 'construct':
            operand, extension = self.operand(value.args[1]); self.ins('movea.l', operand+','+target, 2+extension)
        elif value.kind == 'at':
            receiver, *args = value.args
            if args and args[0].kind in ('read', 'scalar') and len(args) == 1:
                if target != self.reg(receiver.value):
                    raise CompileError('live offset ADDA must preserve bound receiver storage')
                operand, extension = self.operand(args[0]); self.ins('adda.w', operand+','+target, 2+extension)
            else:
                operand, extension = self.memory(receiver, tuple(args)); self.ins('lea', operand+','+target, 2+extension)
        elif value.kind == 'advance':
            if target != self.reg(value.args[0].value):
                raise CompileError('cursor step requires unchanged ABI storage')
            amount = value.args[1].value
            self.ins(('addq.w' if amount > 0 else 'subq.w'), '#'+str(abs(amount))+','+target)
        elif value.kind == 'adjust':
            receiver, other = value.args
            if target != self.reg(receiver.value): raise CompileError('pointer correction storage mismatch')
            # Unsigned pointer comparison, then increment only the source low
            # WORD. EXG is a general storage-selection lowering, not a rule.
            dstreg, srcreg = self.reg(other.value), self.reg(receiver.value)
            if dstreg == srcreg:
                raise CompileError('pointer comparison requires two independently live ABI storages')
            count, identifier = self.reg('count'), self.reg('officer')
            self.ins('exg', count+','+dstreg); self.ins('exg', identifier+','+srcreg)
            self.ins('cmp.l', count+','+identifier)
            skip = self.e.fresh('pointer_before'); self.branch('cs', skip, 4)
            self.ins('addq.w', '#1,'+identifier)
            self.e.label(skip)
            self.ins('exg', count+','+dstreg); self.ins('exg', identifier+','+srcreg)
        elif value.kind == 'intrinsic':
            operation, args = value.value, value.args
            if operation == 'u16' and args[0].kind == 'binary':
                expr = args[0]; left, right = expr.args
                if self.operand(left)[0] != target:
                    raise CompileError('binary target first operand must be same live storage')
                if expr.value in ('add', 'sub'):
                    operand, extension = self.operand(right)
                    if right.kind == 'constant' and 1 <= right.value <= 8:
                        self.ins(('addq.w' if expr.value == 'add' else 'subq.w'), operand+','+target, zero=name)
                    elif right.kind == 'constant':
                        self.ins(('addi.w' if expr.value == 'add' else 'subi.w'), operand+','+target, 4, zero=name)
                    else:
                        self.ins(('add.w' if expr.value == 'add' else 'sub.w'), operand+','+target, 2+extension, zero=name)
                elif expr.value == 'and' and right.kind == 'constant':
                    self.ins('andi.w', '#'+str(literal(right.value,0,65535))+','+target, 4, zero=name)
                elif expr.value in ('shl','shr'):
                    self.ins('lsl.w' if expr.value == 'shl' else 'lsr.w', '#'+str(right.value)+','+target, zero=name)
                else: raise CompileError('unsupported WORD arithmetic shape')
            elif operation in ('u16','low16'):
                operand, extension = self.operand(args[0])
                if args[0].kind == 'constant' and args[0].value == 0:
                    self.ins('clr.w', target, zero=name)
                elif operand != target:
                    self.ins('move.w', operand+','+target, 2+extension, zero=name)
            elif operation == 'replace_byte':
                if self.operand(args[0], stale=allow_stale)[0] != target:
                    raise CompileError('partial BYTE write must retain its actual first-argument storage')
                operand, extension = self.operand(args[1]); self.ins('move.b', operand+','+target, 2+extension)
            elif operation == 'mask_byte':
                if self.operand(args[0])[0] != target: raise CompileError('BYTE mask storage mismatch')
                self.ins('andi.b', '#'+str(args[1].value)+','+target, 4)
            elif operation == 'zero_extend_word':
                if self.operand(args[0])[0] != target: raise CompileError('widening storage mismatch')
                self.ins('andi.l', '#65535,'+target, 6, zero=name)
            elif operation == 'add_low_word':
                if self.operand(args[0])[0] != target: raise CompileError('partial WORD add storage mismatch')
                operand, extension = self.operand(args[1]); self.ins('addi.w', operand+','+target, 2+extension, zero=name)
            elif operation == 'divu_retained':
                if self.operand(args[0])[0] != target: raise CompileError('DIVU retained-register storage mismatch')
                operand, extension = self.operand(args[1]); self.ins('divu.w', operand+','+target, 2+extension)
            else: raise CompileError('unsupported assignment intrinsic')
        else:
            if value.type not in NUMBERS:
                raise CompileError('unsupported bound assignment')
            typ = {'Byte': 'b', 'Word': 'w', 'Long': 'l'}[value.type]
            if value.kind == 'constant' and value.value == 0:
                self.ins('clr.'+typ, target, zero=name)
            else:
                operand, extension = self.operand(value)
                if operand != target:
                    if value.kind == 'constant' and typ == 'l':extension=4
                    self.ins('move.'+typ, operand+','+target, 2+extension, zero=name if value.type != 'Byte' else None)
        self.invalidate(name, value.type)

    def branch(self, condition, target, width):
        self.e.ins('b'+condition+('.s' if width == 2 else '.w'), target, width)

    def condition(self, condition, target, *, true=True, width=4):
        if condition.kind == 'not':
            return self.condition(condition.args[0], target, true=not true, width=width)
        if condition.kind == 'intrinsic' and condition.value in ('negative_byte','negative_word'):
            arg = condition.args[0]; operand, extension = self.operand(arg)
            if not (condition.value == 'negative_word' and arg.kind == 'local' and self.last_zero == arg.value):
                self.ins('tst.'+('b' if condition.value == 'negative_byte' else 'w'), operand, 2+extension)
            return self.branch('mi' if true else 'pl', target, width)
        if condition.kind == 'binary' and condition.value == 'and':
            value, bit = condition.args
            mask = literal(bit.value,1,255)
            if mask & (mask-1): raise CompileError('single memory bit test required')
            operand, extension = self.operand(value)
            if value.type != 'Byte': raise CompileError('BYTE bit test required')
            self.ins('btst', '#'+str(mask.bit_length()-1)+','+operand, 4+extension)
            return self.branch('ne' if true else 'eq', target, width)
        if condition.kind != 'compare':raise CompileError('typed condition family required')
        left, right = condition.args
        op = condition.value
        if right.kind == 'constant' and right.value == 0:
            if left.kind == 'relative_copy':
                self.effect(left)
            elif left.kind == 'local' and self.last_zero == left.value:
                pass
            else:
                operand, extension = self.operand(left)
                self.ins('tst.'+('b' if left.type == 'Byte' else 'w'), operand, 2+extension)
        elif right.kind == 'constant':
            operand, extension = self.operand(left)
            if extension or not operand.startswith('%d'):raise CompileError('immediate compare bound scalar required')
            self.ins('cmpi.'+('b' if left.type == 'Byte' else 'w'), '#'+str(literal(right.value,0,65535))+','+operand, 4)
        else:
            lhs, lhs_extension = self.operand(left);rhs, extension = self.operand(right)
            if lhs_extension or not lhs.startswith('%d'):raise CompileError('comparison first operand bound data scalar required')
            typ = 'b' if left.type == 'Byte' and right.type == 'Byte' else 'w'
            if left.type != right.type:raise CompileError('mixed-width comparison requires explicit narrowing')
            self.ins('cmp.'+typ, rhs+','+lhs, 2+extension)
        code = {'eq':'eq','ne':'ne','lt':'cs','le':'ls','gt':'hi','ge':'cc'}[op]
        if not true:code={'eq':'ne','ne':'eq','cs':'cc','cc':'cs','ls':'hi','hi':'ls'}[code]
        self.branch(code,target,width)

    def call(self, value):
        signature, result = SIGNATURES[value.value]
        target_regs = MEMBER_REGISTERS[value.value]
        for (name, typ), argument in zip(signature, value.args):
            if typ == 'State':continue
            if argument.kind != 'local' or self.reg(argument.value) != '%'+target_regs[name]:
                raise CompileError('callee actual argument storage contract mismatch')
        if result == 'Outcome' and self.binding.completion != 'context_remove':
            raise CompileError('nonlocal completion only from declared removal context')
        self.ins('bsr.w', value.value, 4)

    def completion(self, value):
        if (value.kind != 'completion' or self.binding.completion != 'abandon_two_calls' or
                len(value.args) != 1 or value.args[0].kind != 'local' or value.args[0].type != 'Long' or
                self.reg(value.args[0].value) != '%d1'):
            raise CompileError('context completion requires live exact award storage, not an ignored expression')

    def effect(self, value):
        if value.kind in ('store_scalar','write','relative_write'):return self.store(value)
        if value.kind == 'call':return self.call(value)
        if value.kind == 'change':
            operand, extension=self.memory(value.args[0],());amount=value.args[1].value
            return self.ins('addq.b' if amount>0 else 'subq.b','#'+str(abs(amount))+','+operand,2+extension)
        if value.kind == 'copy':
            source,dest=value.args
            return self.ins('move.b','('+self.reg(source.value)+')+,('+self.reg(dest.value)+')+')
        if value.kind == 'relative_copy':
            source,delta=value.args
            return self.ins('move.b','('+self.reg(source.value)+')+,'+str(literal(delta.value))+'('+self.reg(source.value)+')',4)
        raise CompileError('unsupported side-effect lowering')

    @staticmethod
    def stale_overwrite(first, second):
        if not first or not second or first.kind != second.kind or first.kind != 'assign' or first.target != second.target:return False
        a,b=first.value,second.value
        return (a.kind=='intrinsic' and a.value=='replace_byte' and a.args[0].kind=='local' and a.args[0].value==first.target and
                b.kind=='intrinsic' and b.value=='u16' and b.args[0].kind=='binary' and b.args[0].value=='and' and
                b.args[0].args[0].kind=='local' and b.args[0].args[0].value==first.target and
                b.args[0].args[1].kind=='constant' and 0<=b.args[0].args[1].value<=255)

    def block(self, effects, *, fallthrough=None):
        for index, item in enumerate(effects):
            last=index==len(effects)-1
            if item.kind=='assign':
                following=effects[index+1] if not last else None
                self.assign(item.target,item.value,allow_stale=self.stale_overwrite(item,following))
            elif item.kind=='effect':self.effect(item.value)
            elif item.kind=='pass':pass
            elif item.kind=='return':
                if item.value.kind=='call':self.call(item.value)
                elif item.value.kind=='completion':
                    self.completion(item.value)
                elif item.value.type!='None':raise CompileError('unsupported return value')
                if not last or fallthrough!=self.exit:self.branch('ra',self.exit,4)
            elif item.kind in ('break','continue'):
                if not self.loop_stack:raise CompileError('loop transfer without scope')
                target=self.loop_stack[-1][0 if item.kind=='continue' else 1]
                if fallthrough!=target:self.branch('ra',target,2)
            elif item.kind=='if':
                # Direct conditional exit is a generic control optimization; the
                # semantic condition still determines flags and branch sense.
                if len(item.body)==1 and item.body[0].kind in ('return','break','continue') and not item.otherwise:
                    transfer=item.body[0]
                    if transfer.kind=='return':
                        if transfer.value.type=='Outcome':self.completion(transfer.value)
                        target,width=self.exit,4
                    else:
                        target=self.loop_stack[-1][0 if transfer.kind=='continue' else 1]
                        width=2 if transfer.kind=='continue' else 4
                    self.condition(item.value,target,true=True,width=width)
                    continue
                alternative=self.e.fresh('alternative');done=self.e.fresh('join')
                self.condition(item.value,alternative if item.otherwise else done,true=False)
                before=dict(self.live);self.block(item.body)
                yes=dict(self.live)
                if item.otherwise:
                    self.branch('ra',done,4);self.e.label(alternative);self.live=dict(before);self.block(item.otherwise)
                    no=dict(self.live);self.live={k:v for k,v in yes.items() if no.get(k)==v}
                else:self.live={k:v for k,v in before.items() if yes.get(k)==v}
                self.e.label(done);self.last_zero=None
            elif item.kind=='while':
                start=self.e.fresh('scan');done=self.e.fresh('scan_done')
                self.e.label(start);before=dict(self.live);self.loop_stack.append((start,done))
                if item.value is not None and all(e.kind=='pass' for e in item.body):
                    self.condition(item.value,start,true=True,width=2)
                else:
                    if item.value is not None:self.condition(item.value,done,true=False)
                    terminal=item.body and item.body[-1].kind in ('break','return')
                    self.block(item.body,fallthrough=done if terminal and item.body[-1].kind=='break' else None)
                    if not terminal:self.branch('ra',start,2)
                self.loop_stack.pop();self.e.label(done)
                self.live={k:v for k,v in before.items() if self.live.get(k)==v};self.last_zero=None
            elif item.kind=='counted':
                counter=self.reg(item.target);start=self.e.fresh('countdown');done=self.e.fresh('countdown_done')
                self.e.label(start);self.loop_stack.append((start,done));self.block(item.body)
                self.loop_stack.pop();self.e.ins('dbra',counter+','+start,4);self.e.label(done)
                self.live.pop(item.target,None);self.last_zero=None
            else:raise CompileError('unsupported effect family')

    def finish(self):
        self.e.begin()
        if self.binding.name=='sync_queues':self.ins('movem.l','%d0/%a0,-(%sp)',4)
        self.block(self.effects,fallthrough=self.exit)
        self.e.label(self.exit)
        if self.binding.name=='sync_queues':self.ins('movem.l','(%sp)+,%d0/%a0',4)
        self.e.end()
        return self.e.unit([asdict(effect) for effect in self.effects])


def compile_members(source):
    if type(source) is not str or not source or len(source)>100000:
        raise CompileError('bounded member business source string required')
    try:tree=ast.parse(source)
    except (SyntaxError,RecursionError) as error:raise CompileError('invalid member business syntax') from error
    try:tree, inline = inline_settlement(tree, 'members')
    except (ValueError, TypeError, AttributeError, RecursionError) as error:
        raise CompileError('unsupported supplied member helper flow: ' + str(error)) from error
    functions={};imported_names=set()
    for node in tree.body:
        if isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and type(node.value.value) is str:continue
        if isinstance(node,ast.ImportFrom) and node.module=='domain' and node.level==1 and all(alias.name in IMPORTS and alias.asname is None for alias in node.names):
            imported_names.update(alias.name for alias in node.names)
            continue
        if isinstance(node,ast.FunctionDef) and node.name in SIGNATURES and node.name not in functions:
            functions[node.name]=node;continue
        raise CompileError('only explicit member functions and approved domain imports allowed')
    if set(functions)!=set(SIGNATURES):raise CompileError('all six member bodies required')
    require_declared_names(functions, imported_names)
    units=[]
    for binding in MEMBER_BINDINGS:
        frontend=Frontend(functions[binding.name]);effects=frontend.block(functions[binding.name].body)
        if SIGNATURES[binding.name][1]!='None' and (not effects or effects[-1].kind!='return'):
            raise CompileError('normal fallthrough requires explicit nonlocal completion result')
        unit = Lowering(binding,effects).finish()
        if sum(row['encoding_bytes'] for row in unit['instructions']) != binding.end - binding.entry:
            raise CompileError('edited member flow exceeds its complete target extent')
        units.append(unit)
    return dict(units=units,allocated_bytes=sum(binding.end-binding.entry for binding in MEMBER_BINDINGS),
                original_generation_input=False,complete_CPU=False,inline=inline)
