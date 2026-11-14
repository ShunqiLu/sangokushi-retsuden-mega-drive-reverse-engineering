"""Bounded typed numeric policies to ordinary 68000 instructions.

AST expressions determine arithmetic, live memory access and control effects.
Register allocation, short-address choices and branch widths are a separate
compatibility binding. Generation has no file reads or original-code payload.
"""
import ast
from dataclasses import dataclass, asdict
from .compiler_common import CompileError, Emitter, require_declared_names
from .source_inline import inline_settlement
from .target import NUMERIC_BINDINGS, NUMERIC_REGISTERS, SCALAR_BINDINGS, TABLE_BINDINGS, HELPERS


SIGNATURES = {
    'settle_battle': ((('state', 'State'),), 'None'),
    'loss_ratio': ((('state', 'State'),), 'Pair'),
    'defender_scaled_loss': ((('state', 'State'), ('ratio', 'Word')), 'None'),
    'attacker_heavy_loss': ((('state', 'State'), ('count_hint', 'Word')), 'None'),
    'settle_awards': ((('state', 'State'),), 'None'),
    'defender_heavy_loss': ((('state', 'State'), ('count_hint', 'Word')), 'None'),
    'attacker_light_loss': ((('state', 'State'),), 'None'),
    'transfer_attacker': ((('state', 'State'),), 'None'),
    'transfer_defender': ((('state', 'State'),), 'None'),
    'remove_member': ((('state', 'State'), ('officer', 'Word'), ('object_view', 'Table'), ('owner', 'Word'), ('count', 'Word')), 'Outcome'),
    'random_sample': ((('state', 'State'),), 'Word'),
    'signed_divmod': ((('numerator', 'Long'), ('denominator', 'Long')), 'Pair'),
}
ARG_STORAGE = {'defender_scaled_loss': ('d2',), 'attacker_heavy_loss': ('d2',),
               'defender_heavy_loss': ('d2',), 'signed_divmod': ('d1', 'd2'),
               'remove_member': ('d0', 'a2', 'd3', 'd2')}
NUMBERS = {'Word', 'Long', 'Wide'}
ANNOTATIONS = {'BattleState': 'State', 'Word': 'Word', 'Long': 'Long', 'Table': 'Table'}
INTRINSICS = {'u16', 'u32', 'low16', 'high16', 'zero_extend_word', 'add_low_word', 'divu_retained', 'complete_removal'}
IMPORTS = set(ANNOTATIONS) | INTRINSICS | {'MemberRemoved', 'random_sample', 'signed_divmod'}
RESERVED = IMPORTS | set(SIGNATURES) | {'tuple'}


@dataclass(frozen=True)
class Expr:
    kind: str
    type: str
    value: object = None
    args: tuple = ()


@dataclass(frozen=True)
class Effect:
    kind: str
    target: object = ''
    value: object = None
    body: tuple = ()
    otherwise: tuple = ()


def literal(value, low=0, high=65535):
    if type(value) is not int or not low <= value <= high:
        raise CompileError('strict finite integer literal required')
    return value


def annotation(node):
    if isinstance(node, ast.Constant) and node.value is None:
        return 'None'
    if isinstance(node, ast.Name):
        return ANNOTATIONS.get(node.id)
    if (isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id == 'tuple' and
            isinstance(node.slice, ast.Tuple) and [annotation(n) for n in node.slice.elts] == ['Long', 'Long']):
        return 'Pair'
    return None


class Frontend:
    def __init__(self, node):
        expected, result = SIGNATURES[node.name]
        actual = tuple((a.arg, annotation(a.annotation)) for a in node.args.args)
        if (actual != expected or annotation(node.returns) != result or node.decorator_list or
                node.args.posonlyargs or node.args.kwonlyargs or node.args.vararg or node.args.kwarg or
                node.args.defaults or node.args.kw_defaults):
            raise CompileError('exact typed numeric ABI signature required')
        self.name, self.result, self.types = node.name, result, dict(expected)
        self.registers = NUMERIC_REGISTERS[node.name]

    def expr(self, node):
        if isinstance(node, ast.Name):
            if node.id not in self.types:
                raise CompileError('undefined numeric local')
            return Expr('local', self.types[node.id], node.id)
        if isinstance(node, ast.Constant):
            return Expr('constant', 'Word', literal(node.value))
        if isinstance(node, ast.Attribute):
            base = self.expr(node.value)
            if base.type == 'State' and node.attr in TABLE_BINDINGS:
                return Expr('view', 'Table', node.attr, (base,))
            if base.type == 'Outcome' and node.attr == 'award_word':
                return Expr('award', 'Word', node.attr, (base,))
            raise CompileError('known typed state view/outcome member required')
        if isinstance(node, ast.BinOp):
            left, right = self.expr(node.left), self.expr(node.right)
            operation = {ast.Add: 'add', ast.Sub: 'sub', ast.Mult: 'mul', ast.LShift: 'shl'}.get(type(node.op))
            if operation is None or left.type not in NUMBERS or right.type not in NUMBERS:
                raise CompileError('supported typed numeric arithmetic required')
            if operation == 'shl' and (right.kind != 'constant' or not 1 <= right.value <= 8):
                raise CompileError('finite shift1..8 required')
            return Expr('binary', 'Wide', operation, (left, right))
        if isinstance(node, ast.Compare):
            if len(node.ops) != 1 or len(node.comparators) != 1:
                raise CompileError('single unsigned comparison required')
            left, right = self.expr(node.left), self.expr(node.comparators[0])
            operation = {ast.Eq: 'eq', ast.NotEq: 'ne', ast.Lt: 'lt', ast.LtE: 'le', ast.GtE: 'ge', ast.Gt: 'gt'}.get(type(node.ops[0]))
            if operation is None or left.type != 'Word' or right.type != 'Word':
                raise CompileError('explicit WORD unsigned comparison required')
            return Expr('compare', 'Bool', operation, (left, right))
        if isinstance(node, ast.Call) and not node.keywords:
            args = tuple(self.expr(a) for a in node.args)
            if isinstance(node.func, ast.Name):
                name = node.func.id
                if name == 'Table' and tuple(a.type for a in args) == ('State', 'Long'):
                    return Expr('construct', 'Table', name, args)
                if name in ('u16', 'u32', 'low16', 'high16', 'zero_extend_word') and len(args) == 1 and args[0].type in NUMBERS:
                    if name=='u32' and not (args[0].type=='Long' or args[0].kind=='binary' and args[0].value=='mul'):
                        raise CompileError('explicit unsigned product or already-LONG wrap required')
                    if name=='u16' and args[0].type=='Wide' and args[0].value not in ('add','sub','shl'):
                        raise CompileError('WORD add/sub/shift wrap required')
                    if name=='low16' and args[0].type=='Wide':
                        raise CompileError('narrowing needs an already typed scalar')
                    if name == 'high16' and args[0].type != 'Long':
                        raise CompileError('high half needs explicit LONG')
                    if name == 'zero_extend_word' and args[0].type != 'Word':
                        raise CompileError('widening needs explicit WORD')
                    typ = 'Long' if name in ('u32', 'zero_extend_word') else 'Word'
                    return Expr('intrinsic', typ, name, args)
                if name in ('add_low_word', 'divu_retained') and tuple(a.type for a in args) == ('Long', 'Word'):
                    return Expr('intrinsic', 'Long', name, args)
                if name == 'complete_removal' and tuple(a.type for a in args) == ('Outcome',):
                    return Expr('nonlocal', 'Never', name, args)
                if name in SIGNATURES and tuple(a.type for a in args) == tuple(t for _, t in SIGNATURES[name][0]):
                    return Expr('call', SIGNATURES[name][1], name, args)
                raise CompileError('exact numeric call/intrinsic argument types required')
            if isinstance(node.func, ast.Attribute):
                receiver, method = self.expr(node.func.value), node.func.attr
                if receiver.type == 'State':
                    if method in SCALAR_BINDINGS and not args:
                        width = SCALAR_BINDINGS[method]['width']
                        if width not in (16, 32):
                            raise CompileError('numeric scalar is WORD/LONG')
                        return Expr('scalar', 'Word' if width == 16 else 'Long', method, (receiver,))
                    if method.startswith(('set_', 'add_')) and method[4:] in SCALAR_BINDINGS and tuple(a.type for a in args) == ('Word',):
                        if SCALAR_BINDINGS[method[4:]]['width'] != 16:
                            raise CompileError('numeric store exact WORD width required')
                        return Expr('store_scalar' if method.startswith('set_') else 'add_scalar', 'None', method[4:], args)
                if receiver.type == 'Table':
                    if method == 'word' and 1 <= len(args) <= 2 and all(a.type == 'Word' for a in args):
                        return Expr('read', 'Word', method, (receiver,) + args)
                    if method == 'set_word' and 2 <= len(args) <= 3 and all(a.type == 'Word' for a in args):
                        return Expr('write', 'None', method, (receiver,) + args)
                    if method == 'at' and len(args) == 1 and args[0].type == 'Word':
                        return Expr('at', 'Table', method, (receiver,) + args)
                raise CompileError('unsupported numeric view operation')
        raise CompileError('unsupported numeric expression')

    def block(self, nodes, *, depth=0, removal_handled=False):
        effects = []
        for node in nodes:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and type(node.value.value) is str:
                continue
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target, value = node.targets[0], self.expr(node.value)
                if isinstance(target, ast.Tuple):
                    if len(target.elts)!=2 or any(not isinstance(e,ast.Name) or not isinstance(e.ctx,ast.Store) for e in target.elts):
                        raise CompileError('exactly two plain paired-result destinations required')
                    names = tuple(e.id for e in target.elts)
                    if names != ('quotient', 'remainder') or value.kind != 'call' or value.type != 'Pair':
                        raise CompileError('declared two-LONG result binding required')
                    self.types.update({name: 'Long' for name in names})
                    effects.append(Effect('pair', names, value))
                elif isinstance(target, ast.Name):
                    name = target.id
                    if name in RESERVED or name not in self.registers or value.type not in ('Word', 'Long', 'Table', 'Outcome'):
                        raise CompileError('declared typed numeric ABI local required')
                    self.types[name] = value.type
                    effects.append(Effect('assign', name, value))
                else:
                    raise CompileError('simple typed numeric assignment required')
            elif isinstance(node, ast.Expr):
                value = self.expr(node.value)
                if value.kind not in ('write', 'store_scalar', 'add_scalar', 'call', 'nonlocal') or value.type not in ('None', 'Never'):
                    raise CompileError('explicit side-effect/completion required')
                if value.kind=='call' and value.value in ('attacker_heavy_loss','defender_heavy_loss') and not removal_handled:
                    raise CompileError('heavy-loss invocation must handle its nonlocal completion')
                effects.append(Effect('effect', value=value))
            elif isinstance(node, ast.If):
                condition = self.expr(node.test)
                if condition.type != 'Bool':
                    raise CompileError('typed numeric branch condition required')
                before = dict(self.types)
                yes = self.block(node.body, depth=depth+1); yes_types = dict(self.types)
                self.types = dict(before)
                no = self.block(node.orelse, depth=depth+1); no_types = dict(self.types)
                self.types = {key: typ for key, typ in yes_types.items() if no_types.get(key) == typ}
                effects.append(Effect('if', value=condition, body=yes, otherwise=no))
            elif isinstance(node, ast.Try):
                if (node.orelse or node.finalbody or len(node.handlers) != 1 or node.handlers[0].name is not None or
                        not isinstance(node.handlers[0].type, ast.Name) or node.handlers[0].type.id != 'MemberRemoved' or
                        len(node.handlers[0].body) != 1 or not isinstance(node.handlers[0].body[0], ast.Pass)):
                    raise CompileError('only declared nonlocal member-removal completion is handled')
                if self.name!='settle_battle':raise CompileError('only settlement handles nonlocal member removal')
                body = self.block(node.body, depth=depth+1, removal_handled=True)
                if len(body) != 1 or body[0].kind != 'effect' or body[0].value.kind != 'call' or body[0].value.value not in ('attacker_heavy_loss', 'defender_heavy_loss'):
                    raise CompileError('nonlocal handler requires exactly one heavy-loss context call')
                effects.append(Effect('handle_removal', body=body))
            elif isinstance(node, ast.Return):
                if depth:raise CompileError('nested return is outside the numeric target subset')
                value = self.expr(node.value) if node.value is not None else Expr('void', 'None')
                if value.type != self.result:
                    raise CompileError('exact numeric return type required')
                effects.append(Effect('return', value=value))
            else:
                raise CompileError('unsupported numeric statement')
        for index,item in enumerate(effects):
            if item.kind=='assign' and item.value.type=='Outcome':
                if item.value.kind!='call' or item.value.value!='remove_member' or index+2!=len(effects)-1:
                    raise CompileError('nonlocal result requires completion and retained pending-award tail')
                completion,tail=effects[index+1:index+3]
                if (completion.kind!='effect' or completion.value.kind!='nonlocal' or
                        completion.value.args[0].kind!='local' or completion.value.args[0].value!=item.target or
                        tail.kind!='effect' or tail.value.kind!='add_scalar' or
                        tail.value.args[0].kind!='award' or tail.value.args[0].args[0].value!=item.target):
                    raise CompileError('actual removal outcome must be completed before its pending original award tail')
        return tuple(effects)


class Lowering:
    def __init__(self, binding, effects):
        self.binding, self.effects, self.e = binding, effects, Emitter(binding)
        self.registers = NUMERIC_REGISTERS[binding.name]
        self.live = dict(SIGNATURES[binding.name][0])
        self.zero_extended, self.flags, self.removal_result = set(), None, None
        self.exit = self.e.fresh('return')

    def reg(self, name):
        if name not in self.live or name not in self.registers:
            raise CompileError('undefined/clobbered numeric storage')
        return '%' + self.registers[name]

    def update(self, name, typ, zero_extended=False):
        reg = self.registers[name]
        removed = {key for key in self.live if self.registers.get(key) == reg and key != name}
        self.live = {key: value for key, value in self.live.items() if key not in removed}
        self.zero_extended -= removed | {name}
        self.live[name] = typ
        if zero_extended: self.zero_extended.add(name)

    def ins(self, operation, operands='', width=2, flags=None):
        self.e.ins(operation, operands, width)
        # MOVEA/LEA do not disturb CCR. Every other operation is conservatively
        # invalidated unless this exact scalar/width produced the current flags.
        if operation not in ('lea', 'movea.l', 'movea.w', 'adda.w'):
            self.flags = flags

    def memory(self, table, args):
        if table.kind != 'local' or table.type != 'Table':
            raise CompileError('live table binding required')
        base = self.reg(table.value)
        if not args or len(args) > 2:
            raise CompileError('explicit indexed WORD table access required')
        offset = args[0]
        displacement = 0
        if len(args) == 2:
            if args[1].kind != 'constant': raise CompileError('constant brief displacement required')
            displacement = literal(args[1].value, -128, 127)
        index, extension = self.operand(offset)
        if extension or offset.type != 'Word' or not index.startswith('%d'):
            raise CompileError('complete live data-register WORD index required')
        return f'{displacement}({base},{index}.w)', 2

    def operand(self, value):
        if value.kind == 'local': return self.reg(value.value), 0
        if value.kind == 'constant': return '#'+str(value.value), 2
        if value.kind == 'scalar':
            b = SCALAR_BINDINGS[value.value]
            return f"0x{b['address']:x}:{b['suffix']}", 2 if b['suffix'] == 'w' else 4
        if value.kind == 'read': return self.memory(value.args[0], value.args[1:])
        if value.kind == 'award':
            source = value.args[0]
            if source.kind != 'local' or self.removal_result != source.value or self.reg(source.value) != '%d1':
                raise CompileError('award must be current nonlocal removal result')
            return '%d1', 0
        if value.kind == 'intrinsic' and value.value == 'low16': return self.operand(value.args[0])
        raise CompileError('expression requires explicit numeric lowering')

    def move(self, value, target, typ=None):
        source, ext = self.operand(value)
        typ = typ or value.type
        suffix = 'l' if typ == 'Long' else 'w'
        if source == target: return
        if value.kind == 'constant' and value.value == 0:
            self.ins('clr.'+suffix, target, flags=(target, 32 if suffix == 'l' else 16))
        else:
            if value.kind == 'constant' and suffix == 'l': ext = 4
            operation = 'movea.'+suffix if target.startswith('%a') else 'move.'+suffix
            self.ins(operation, source+','+target, 2+ext, flags=(target, 32 if suffix == 'l' else 16))

    def require_first(self, value, target):
        source, ext = self.operand(value)
        if source != target or ext:
            raise CompileError('in-place operation requires its complete live first operand')

    def unsigned_operand(self, value):
        narrowed = value.kind == 'intrinsic' and value.value == 'low16'
        if value.type == 'Word' or narrowed:
            return self.operand(value)
        if value.kind == 'local' and value.type == 'Long' and value.value in self.zero_extended:
            return self.operand(value)
        raise CompileError('MULU requires WORD operands or proven zero-extended WORD')

    def multiply(self, expr, target):
        left, right = expr.args
        self.require_first(left, target)
        source, ext = self.unsigned_operand(right)
        self.unsigned_operand(left)
        # A strength reduction is admitted only for a proven unsigned WORD
        # widened to LONG. Its arithmetic constants come from the actual AST.
        if (right.kind == 'constant' and right.value in (31, 51, 60) and left.kind == 'local' and
                left.type == 'Long' and left.value in self.zero_extended):
            if target != '%d0': raise CompileError('bounded strength reduction scratch allocation required')
            self.ins('move.l', target+',%d1')
            self.live = {k: v for k, v in self.live.items() if self.registers.get(k) != 'd1'}
            if right.value == 31:
                self.ins('lsl.l', '#5,'+target); self.ins('sub.l', '%d1,'+target)
            elif right.value == 51:
                self.ins('lsl.l', '#1,'+target); self.ins('add.l', '%d1,'+target)
                self.ins('lsl.l', '#3,'+target); self.ins('add.l', '%d1,'+target)
                self.ins('lsl.l', '#1,'+target); self.ins('add.l', '%d1,'+target)
            else:
                self.ins('lsl.l', '#6,'+target); self.ins('lsl.l', '#2,%d1'); self.ins('sub.l', '%d1,'+target)
        else:
            self.ins('mulu.w', source+','+target, 2+ext)

    def value(self, value, target):
        if value.kind in ('constant', 'local', 'scalar', 'read', 'award'):
            self.move(value, target); return
        if value.kind == 'view':
            b = TABLE_BINDINGS[value.value]
            if not target.startswith('%a'): raise CompileError('view requires address register')
            self.ins('lea', f"0x{b['address']:x}:{b['suffix']},"+target, 4 if b['suffix'] == 'w' else 6); return
        if value.kind == 'construct':
            if not target.startswith('%a'): raise CompileError('constructed view requires address register')
            source, ext = self.operand(value.args[1]); self.ins('movea.l', source+','+target, 2+ext); return
        if value.kind == 'at':
            self.require_first(value.args[0], target)
            source, ext = self.operand(value.args[1]); self.ins('adda.w', source+','+target, 2+ext); return
        if value.kind == 'call':
            self.call(value)
            actual = {'random_sample': '%d0', 'remove_member': '%d1'}.get(value.value)
            if actual != target: raise CompileError('call result binding/storage mismatch')
            return
        if value.kind != 'intrinsic': raise CompileError('explicit wrapping arithmetic required')
        name, args = value.value, value.args
        if name in ('u16', 'u32') and args[0].kind == 'binary':
            expr = args[0]; left, right = expr.args
            if expr.value == 'mul' and name == 'u32':
                self.multiply(expr, target); return
            if name != 'u16': raise CompileError('bounded scalar add/sub/shift needs WORD wrap')
            if left.kind in ('local','scalar','read'):
                first_operand=self.operand(left)[0]
                if first_operand!=target and right.kind!='constant':
                    second_operand=self.operand(right)[0]
                    if target in second_operand:
                        raise CompileError('scalar assignment would clobber its still-live second operand/address')
            # Lower nested high-half arithmetic without temporary prefetches.
            if left.kind == 'intrinsic': self.value(left, target)
            else: self.move(left, target, 'Word')
            if expr.value == 'shl':
                self.ins('lsl.w', '#'+str(right.value)+','+target, flags=(target,16)); return
            source, ext = self.operand(right)
            if expr.value not in ('add','sub'): raise CompileError('unsupported WORD arithmetic')
            if right.kind == 'constant' and 1 <= right.value <= 8:
                operation = 'addq.w' if expr.value == 'add' else 'subq.w'
                width = 2
            elif right.kind == 'constant':
                operation = 'addi.w' if expr.value == 'add' else 'subi.w'; width = 4
            else:
                operation = 'add.w' if expr.value == 'add' else 'sub.w'; width = 2+ext
            self.ins(operation, source+','+target, width, flags=(target,16)); return
        if name in ('low16','u16') and args[0].kind in ('local','constant','read','scalar'):
            self.move(args[0],target,'Word');return
        if name in ('u16', 'u32', 'low16'):
            self.value(args[0], target); return
        if name == 'high16':
            self.value(args[0], target); self.ins('swap', target, flags=(target,32)); return
        if name == 'zero_extend_word':
            self.value(args[0], target)
            self.ins('andi.l', '#65535,'+target, 6, flags=(target,32)); return
        if name == 'add_low_word':
            self.require_first(args[0], target)
            source, ext = self.operand(args[1])
            if args[1].kind == 'constant' and 1 <= args[1].value <= 8:
                self.ins('addq.w', source+','+target, flags=(target,16))
            elif args[1].kind == 'constant': self.ins('addi.w', source+','+target,4,flags=(target,16))
            else:self.ins('add.w',source+','+target,2+ext,flags=(target,16))
            return
        if name == 'divu_retained':
            self.value(args[0], target)
            source, ext = self.operand(args[1]); self.ins('divu.w',source+','+target,2+ext); return
        raise CompileError('unsupported numeric intrinsic')

    def assign(self, name, value):
        target = '%'+self.registers[name]
        self.value(value, target)
        extended = value.kind == 'intrinsic' and value.value == 'zero_extend_word'
        self.update(name, value.type, extended)
        if value.type == 'Outcome': self.removal_result = name

    def call(self, value):
        name = value.value
        signature, result = SIGNATURES[name]
        nonstate = tuple(a for a in value.args if a.type != 'State')
        if any(a.kind != 'local' or self.reg(a.value) != '%'+reg for a,reg in zip(nonstate,ARG_STORAGE.get(name,()))):
            raise CompileError('callee actual live argument allocation mismatch')
        if len(nonstate) != len(ARG_STORAGE.get(name,())):
            raise CompileError('callee argument ABI arity mismatch')
        if name in HELPERS:
            self.ins('jsr', '0x'+format(HELPERS[name],'x')+':l', 6)
        else:
            self.ins('bsr.w', name, 4)
        if name == 'random_sample':
            self.live = {k:v for k,v in self.live.items() if self.registers.get(k) != 'd0'}
        elif name == 'signed_divmod' or name == 'loss_ratio':
            self.live = {k:v for k,v in self.live.items() if self.registers.get(k) not in ('d0','d1','d2','a0','a1')}
        elif name == 'remove_member':
            if self.binding.name not in ('attacker_heavy_loss','defender_heavy_loss'):
                raise CompileError('removal requires declared heavy-loss two-call context')
            self.live = {k:v for k,v in self.live.items() if self.registers.get(k) != 'd1'}
        # Other calls in the settlement orchestrator do not promise arbitrary
        # register preservation. Only its declared live ratio WORD in D2 is
        # retained by those original contracts.
        elif self.binding.name == 'settle_battle':
            self.live = {k:v for k,v in self.live.items() if self.registers.get(k) == 'd2' or k=='state'}

    def effect(self, value):
        if value.kind == 'call': self.call(value); return
        if value.kind == 'nonlocal':
            arg=value.args[0]
            if arg.kind!='local' or arg.value!=self.removal_result or self.reg(arg.value)!='%d1':
                raise CompileError('nonlocal completion must consume the actual prior removal result')
            # It is the already-emitted callee's MOVEM/RTS ABI, not a synthetic
            # jump/exception implementation. Pending original award ADD remains.
            return
        if value.kind in ('store_scalar','add_scalar'):
            b=SCALAR_BINDINGS[value.value]
            destination=f"0x{b['address']:x}:{b['suffix']}"
            source,ext=self.operand(value.args[0]);dstext=2 if b['suffix']=='w' else 4
            self.ins('move.w' if value.kind=='store_scalar' else 'add.w',source+','+destination,2+ext+dstext);return
        if value.kind=='write':
            destination,ext=self.memory(value.args[0],(value.args[1],)+value.args[3:]);source=value.args[2]
            if source.kind=='constant' and source.value==0:self.ins('clr.w',destination,2+ext)
            else:
                operand,source_ext=self.operand(source);self.ins('move.w',operand+','+destination,2+source_ext+ext)
            return
        raise CompileError('unsupported numeric effect lowering')

    def branch(self, condition, target):
        self.e.ins('b'+condition+'.w',target,4)

    def condition(self, value, target):
        left,right=value.args
        operand,ext=self.operand(left)
        if ext or not operand.startswith('%d') or right.kind!='constant':
            raise CompileError('bounded comparison requires live register WORD and literal')
        if right.value==0:
            if self.flags!=(operand,16):self.ins('tst.w',operand)
        else:self.ins('cmpi.w','#'+str(right.value)+','+operand,4)
        self.branch({'eq':'ne','ne':'eq','lt':'cc','le':'hi','ge':'cs','gt':'ls'}[value.value],target)

    def block(self, effects):
        for item in effects:
            if item.kind=='assign':self.assign(item.target,item.value)
            elif item.kind=='pair':
                if item.value.value!='loss_ratio':raise CompileError('orchestrator pair must come from live ratio call')
                self.call(item.value)
                for name,reg in zip(item.target,('d1','d2')):
                    if self.registers[name]!=reg:raise CompileError('paired result storage mismatch')
                    self.update(name,'Long')
            elif item.kind=='effect':self.effect(item.value)
            elif item.kind=='handle_removal':self.block(item.body)
            elif item.kind=='return':
                if item.value.type=='Pair':
                    if item.value.kind!='call' or item.value.value!='signed_divmod':
                        raise CompileError('paired ratio return requires exact live signed division')
                    self.call(item.value)
                elif item.value.type!='None':raise CompileError('unsupported numeric return')
            elif item.kind=='if':
                alternate=self.e.fresh('alternative');done=self.e.fresh('join')
                self.condition(item.value,alternate if item.otherwise else done)
                before=dict(self.live);extended=set(self.zero_extended)
                self.block(item.body);yes=dict(self.live);yes_extended=set(self.zero_extended)
                if item.otherwise:
                    self.branch('ra',done);self.e.label(alternate)
                    self.live=dict(before);self.zero_extended=set(extended)
                    self.block(item.otherwise);no=dict(self.live)
                    self.live={k:v for k,v in yes.items() if no.get(k)==v}
                    self.zero_extended &= yes_extended
                else:
                    self.live={k:v for k,v in before.items() if yes.get(k)==v}
                    self.zero_extended=extended & yes_extended
                self.e.label(done);self.flags=None
            else:raise CompileError('unsupported numeric control effect')

    def finish(self):
        self.e.begin();self.block(self.effects);self.e.label(self.exit);self.e.end()
        return self.e.unit([asdict(e) for e in self.effects])


def compile_numeric(source):
    if type(source) is not str or not source or len(source)>100000:
        raise CompileError('bounded numeric business source required')
    try:tree=ast.parse(source)
    except (SyntaxError,RecursionError) as error:raise CompileError('invalid numeric business syntax') from error
    try:tree, inline = inline_settlement(tree, 'numeric')
    except (ValueError, TypeError, AttributeError, RecursionError) as error:
        raise CompileError('unsupported supplied numeric helper flow: ' + str(error)) from error
    functions={};imported_names=set()
    for node in tree.body:
        if isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and type(node.value.value) is str:continue
        if (isinstance(node,ast.ImportFrom) and node.level==1 and node.module=='domain' and
                all(a.name in IMPORTS and a.asname is None for a in node.names)):
            imported_names.update(a.name for a in node.names);continue
        if (isinstance(node,ast.ImportFrom) and node.level==1 and node.module=='business_members' and
                all(a.name in ('remove_member','transfer_attacker','transfer_defender') and a.asname is None for a in node.names)):
            imported_names.update(a.name for a in node.names);continue
        if isinstance(node,ast.FunctionDef) and node.name in NUMERIC_REGISTERS and node.name not in functions:
            functions[node.name]=node;continue
        raise CompileError('only seven declared numeric policies and approved imports allowed')
    if set(functions)!=set(NUMERIC_REGISTERS):raise CompileError('all seven numeric business bodies required')
    require_declared_names(functions,imported_names)
    units=[]
    for binding in NUMERIC_BINDINGS:
        f=Frontend(functions[binding.name]);effects=f.block(functions[binding.name].body)
        if f.result=='Pair' and (not effects or effects[-1].kind!='return'):
            raise CompileError('paired output requires explicit typed return')
        if any(e.kind=='return' for e in effects[:-1]):raise CompileError('nonterminal return unsupported')
        unit = Lowering(binding,effects).finish()
        if sum(row['encoding_bytes'] for row in unit['instructions']) != binding.end - binding.entry:
            raise CompileError('edited numeric flow exceeds its complete target extent')
        units.append(unit)
    return dict(units=units,allocated_bytes=728,original_generation_input=False,complete_CPU=False,inline=inline)
