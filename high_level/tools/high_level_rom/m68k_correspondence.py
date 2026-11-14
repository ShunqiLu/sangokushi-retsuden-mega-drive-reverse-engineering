"""Read-only GNU M68K source/decoded-instruction correspondence.

This is a finite source notation normalizer, not an assembler, opcode
interpreter, or byte generator. Actual instruction decoding is delegated to
Capstone and the existing format_instruction. Unknown notation is refused.
"""
from __future__ import annotations

import ast
import re

from .code_registry import _operands
from ..m68k_build.source import format_instruction


_NAME = r'[A-Za-z_.$][A-Za-z0-9_.$]*'
_TOKEN = re.compile(r'0[xX][0-9a-fA-F]+|0[bB][01]+|[0-9]+|' + _NAME
    + r'|<<|>>|[()+\-*/&|^~]')
_REG = r'%(?:[da][0-7]|sp|pc|sr|ccr|usp)'


class SourceSymbols:
    """Source-derived locations plus finite .equ/.set integer expressions."""

    def __init__(self):
        self.locations = {}
        self.definitions = {}

    def expression(self, text, pc, stack=()):
        if type(text) is not str or not text or len(text) > 512:
            raise ValueError('bounded GNU integer/address expression required')
        compact = ''.join(text.split())
        tokens, position = [], 0
        while position < len(compact):
            match = _TOKEN.match(compact, position)
            if match is None:
                raise ValueError('unsupported GNU address expression: ' + text)
            tokens.append(match.group())
            position = match.end()
        names, translated = {}, []
        for token in tokens:
            if re.fullmatch(_NAME, token):
                key = 'symbol_' + str(len(names))
                names[key] = token
                translated.append(key)
            else:
                translated.append(token)
        tree = ast.parse(''.join(translated), mode='eval')
        if len(list(ast.walk(tree))) > 128:
            raise ValueError('bounded GNU expression tree required')

        def evaluate(node):
            if isinstance(node, ast.Constant) and type(node.value) is int:
                return node.value, 0
            if isinstance(node, ast.Name) and node.id in names:
                name = names[node.id]
                if name == '.':
                    return pc, 1
                if name in self.locations:
                    return self.locations[name], 1
                if name not in self.definitions or name in stack:
                    raise ValueError('unknown/cyclic current GNU source symbol: ' + name)
                value, location = self.definitions[name]
                return self.expression(value, location, stack + (name,))
            if isinstance(node, ast.UnaryOp):
                value, section = evaluate(node.operand)
                if isinstance(node.op, ast.UAdd):return value, section
                if isinstance(node.op, ast.USub):return -value, -section
                if isinstance(node.op, ast.Invert) and section == 0:return ~value, 0
            if isinstance(node, ast.BinOp):
                left, ls = evaluate(node.left)
                right, rs = evaluate(node.right)
                if isinstance(node.op, ast.Add):return left + right, ls + rs
                if isinstance(node.op, ast.Sub):return left - right, ls - rs
                if ls or rs:
                    raise ValueError('nonlinear GNU section expression is unsupported')
                if isinstance(node.op, ast.Mult):return left * right, 0
                if isinstance(node.op, ast.Div) and right:
                    return (abs(left) // abs(right)) * (-1 if (left < 0) != (right < 0) else 1), 0
                if isinstance(node.op, ast.BitAnd):return left & right, 0
                if isinstance(node.op, ast.BitOr):return left | right, 0
                if isinstance(node.op, ast.BitXor):return left ^ right, 0
                if isinstance(node.op, (ast.LShift, ast.RShift)) and 0 <= right <= 63:
                    return (left << right if isinstance(node.op, ast.LShift) else left >> right), 0
            raise ValueError('unsupported GNU constant/address expression node')

        value, section = evaluate(tree.body)
        if not -(1 << 63) <= value < 1 << 64 or section not in (0, 1):
            raise ValueError('bounded absolute or single-section GNU expression required')
        return value, section

    def pc_displacement(self, text, pc):
        """Resolve an actual PC EA, including the generator's explicit base.

        ``(target-.-2)(%pc)`` already subtracts the extension-word PC. Its
        target may be an absolute .equ/.set or a current section label; do
        not admit a general negative section coefficient to expression().
        Plain numbers remain literal displacements, while a plain section
        label still denotes a target address under the existing GNU rule.
        """
        if type(text) is not str or not text or len(text) > 512:
            raise ValueError('bounded GNU PC displacement expression required')
        compact = ''.join(text.split())
        explicit_base = re.fullmatch(r'\((.+)-\.-2\)', compact)
        if explicit_base is not None:
            target, _ = self.expression(explicit_base[1], pc)
            return target - (pc + 2)
        value, section = self.expression(text, pc)
        return value - (pc + 2) if section else value


def source_statements(assembly, rows):
    """Locate every real statement/label using current explicit row widths."""
    symbols = SourceSymbols()
    cursor, statements, repeated_definitions = 0, [], []
    for raw in assembly.splitlines():
        line = raw.split('|', 1)[0].strip()
        if not line or line.startswith('#'):
            continue
        if re.fullmatch(_NAME + ':', line):
            name = line[:-1]
            if name in symbols.locations or name in symbols.definitions:
                raise ValueError('duplicate current assembly symbol: ' + name)
            symbols.locations[name] = cursor
            continue
        match = re.fullmatch(r'\.(?:set|equ)\s+(' + _NAME + r')\s*,\s*(.+)', line)
        if match:
            name, expression = match.groups()
            if name in symbols.locations:
                raise ValueError('GNU alias conflicts with an instruction label: ' + name)
            if name in symbols.definitions:
                # Independent generated units may repeat their shared typed
                # data aliases. Retain the first authority; resolve every
                # repeat after all forward labels are known, never mutate it.
                repeated_definitions.append((name, expression, cursor))
            else:
                symbols.definitions[name] = expression, cursor
            continue
        if line.startswith('.org '):
            cursor, section = symbols.expression(line[5:].strip(), cursor)
            if section or not 0 <= cursor <= 0x100000:
                raise ValueError('explicit absolute bounded .org required')
            continue
        if (line == '.cpu 68000' or line == '.text' or line == '.section .text'
                or re.fullmatch(r'\.(?:global|globl)\s+' + _NAME, line)):
            continue
        if line.startswith('.'):
            raise ValueError('unsupported or data-emitting code directive: ' + line)
        index = len(statements)
        if index >= len(rows) or cursor != rows[index]['logical_pc']:
            raise ValueError('current source/metadata instruction placement differs')
        operation = line.split(None, 1)[0]
        if operation != rows[index]['operation']:
            raise ValueError('current generated statement/row mnemonic differs')
        statements.append(line)
        cursor += rows[index]['width']
    if len(statements) != len(rows):
        raise ValueError('complete current generated instruction sequence required')
    # Resolve every definition even when unused; no unknown source directive
    # is silently admitted merely because it did not affect a compared operand.
    resolved_definitions = {name: symbols.expression(name, 0)
        for name in symbols.definitions}
    for name, expression, location in repeated_definitions:
        # Include the alias in the recursion stack: a repeated ``name+...``
        # is a mutable/self-referential definition, not an equal declaration.
        if symbols.expression(expression, location, (name,)) != resolved_definitions[name]:
            raise ValueError('conflicting repeated GNU alias definition: ' + name)
    return tuple(statements), symbols


def _register(text):
    value = text.lower().replace('%sp', '%a7')
    if re.fullmatch(_REG, value) is None:
        raise ValueError('ordinary M68K register required: ' + text)
    return value


def _register_list(text):
    result = []
    for part in text.split('/'):
        pair = part.split('-')
        if len(pair) not in (1, 2):raise ValueError('finite MOVEM register list required')
        registers = [_register(value) for value in pair]
        if any(re.fullmatch(r'%[da][0-7]', value) is None for value in registers):
            raise ValueError('MOVEM data/address registers required')
        indices = [(0 if value[1] == 'd' else 8) + int(value[2]) for value in registers]
        if len(indices) == 1:result.append(indices[0])
        elif indices[0] <= indices[1]:result.extend(range(indices[0], indices[1] + 1))
        else:raise ValueError('ascending MOVEM range required')
    if len(set(result)) != len(result):raise ValueError('repeated MOVEM register')
    return tuple(sorted(result))


def _operation(operation, args, width):
    base, dot, size = operation.lower().partition('.')
    base = {'dbra':'dbf', 'bhs':'bcc', 'blo':'bcs', 'shs':'scc', 'slo':'scs'}.get(base, base)
    size = 'b' if size == 's' else size
    if base in ('exg', 'swap', 'lea', 'pea', 'jsr', 'jmp', 'rts', 'rte', 'rtr',
            'nop', 'reset', 'illegal', 'trap', 'trapv', 'unlk', 'moveq'):
        if size and size not in ('w', 'l'):raise ValueError('unsupported fixed-size mnemonic suffix')
        return base
    if base in ('btst', 'bset', 'bclr', 'bchg'):
        return base + ('.l' if re.fullmatch(r'%d[0-7]', args[-1]) else '.b')
    if base.startswith('db'):
        return base + '.w'
    if base.startswith('b') and base not in ('bchg', 'bclr', 'bset', 'btst'):
        return base + '.' + (size or ('b' if width == 2 else 'w'))
    if base == 'move' and any('%usp' in arg for arg in args):return 'move-usp'
    if base in ('move', 'add', 'sub', 'cmp') and args and re.fullmatch(r'%a[0-7]', args[-1]):
        base = {'move':'movea', 'add':'adda', 'sub':'suba', 'cmp':'cmpa'}[base]
    if base.startswith('s') and base not in ('sub', 'suba', 'subi', 'subq', 'subx', 'stop', 'swap'):
        return base + '.b'
    if not size:
        size = 'w'
    if size not in ('b', 'w', 'l'):
        raise ValueError('ordinary M68K data width required')
    return base + '.' + size


def _operand(text, operation, index, argc, pc, symbols):
    text = re.sub(_REG, lambda match: match.group().lower(), ''.join(text.split()), flags=re.I)
    text = text.replace('%sp', '%a7')
    base, _, size = operation.partition('.')
    if base == 'movem' and re.fullmatch(r'%[da][0-7](?:[-/]%[da][0-7])*', text):
        return 'register-list', _register_list(text)
    if re.fullmatch(_REG, text):return 'register', _register(text)
    branch = (base.startswith('db') and index == argc - 1
        or base.startswith('b') and base not in ('btst', 'bset', 'bclr', 'bchg'))
    if branch:
        value, _ = symbols.expression(text, pc)
        return 'branch-address', value & 0xffffffff
    if text.startswith('#'):
        value, _ = symbols.expression(text[1:], pc)
        bits = 8 if base in ('moveq', 'btst', 'bset', 'bclr', 'bchg', 'addq', 'subq') else dict(b=8,w=16,l=32).get(size, 16)
        return 'immediate', value & ((1 << bits) - 1)
    match = re.fullmatch(r'-\((' + _REG + r')\)', text)
    if match:return 'predecrement', _register(match[1])
    match = re.fullmatch(r'\((' + _REG + r')\)(\+)?', text)
    if match:return ('postincrement' if match[2] else 'indirect'), _register(match[1])
    match = re.fullmatch(r'(.*)\((%(?:a[0-7]|pc))(?:,(%[da][0-7])(?:\.([wl]))?(?:\*1)?)?\)', text)
    if match:
        displacement, register, indexed, index_size = match.groups()
        if register == '%pc':
            value = symbols.pc_displacement(displacement or '0', pc)
        else:
            value, section = symbols.expression(displacement or '0', pc)
            if section:
                raise ValueError('unresolved section-valued address-register displacement')
        bits = 8 if indexed else 16
        return ('indexed' if indexed else 'displacement', register,
            None if not indexed else (_register(indexed), index_size or 'w'), value & ((1 << bits) - 1))
    match = re.fullmatch(r'(.+):([wl])', text)
    if match:
        value, _ = symbols.expression(match[1], pc)
        bits = 16 if match[2] == 'w' else 32
        return 'absolute', bits, value & ((1 << bits) - 1)
    value, _ = symbols.expression(text, pc)
    return 'absolute-auto', value & 0xffffffff


def instruction_key(text, pc, width, symbols):
    operation, _, operands = text.strip().partition(' ')
    args = _operands(operands.strip())
    args = [re.sub(_REG, lambda match: match.group().lower(), ''.join(value.split()), flags=re.I)
        .replace('%sp', '%a7') for value in args]
    operation = _operation(operation, args, width)
    return operation, tuple(_operand(value, operation, index, len(args), pc, symbols)
        for index, value in enumerate(args))


def _same_operand(expected, actual):
    if expected == actual:return True
    if expected[0] == 'absolute-auto' and actual[0] == 'absolute':
        bits, value = actual[1:]
        if bits == 16 and value & 0x8000:value |= 0xffff0000
        return expected[1] == value
    return False


def verify_current_instructions(group, image, decoder):
    """Decode, never execute, every whole current generated instruction."""
    rows = group['instruction_rows']
    statements, symbols = source_statements(group['assembly'], rows)
    for row, statement in zip(rows, statements):
        pc, width = row['logical_pc'], row['width']
        raw = image[pc:pc + width]
        decoded = list(decoder.disasm(raw, pc, count=1))
        if len(decoded) != 1 or decoded[0].size != width:
            raise ValueError('actual decoded instruction width differs at ' + hex(pc))
        current = instruction_key(statement, pc, width, symbols)
        actual = instruction_key(format_instruction(decoded[0]), pc, width, SourceSymbols())
        if (current[0] != actual[0] or len(current[1]) != len(actual[1])
                or any(not _same_operand(a, b) for a, b in zip(current[1], actual[1]))):
            raise ValueError('current generated mnemonic/operands differ at ' + hex(pc)
                + ': source=' + statement + ' decoded=' + format_instruction(decoded[0]))
    return dict(instructions=len(rows), mnemonic_and_all_operands_match=True,
        comparison='source-derived symbols and finite GNU notation; existing Capstone formatter',
        instruction_execution=False)
