"""Shared finite source-policy grammar for complete gameplay families.

Roles name exact AST uses, including coupled caller/helper observations.  This
module admits complete declared source bodies and retains supplied effects; it
does not compile arbitrary Python or infer a natural indirect-handler domain.
Family modules own physical lowering and constraints, not this grammar.
"""
from __future__ import annotations

import ast
from copy import deepcopy
from dataclasses import dataclass

from .compiler_common import CompileError, semantic_functions


@dataclass(frozen=True)
class SourceRole:
    name: str
    function: str
    paths: tuple[tuple[str | int, ...], ...]
    kind: str
    default: int | str
    physical_pcs: tuple[int, ...]
    # One physical policy may also be observed by a complete caller/helper.
    # These are additional real source uses, not substituted function bodies.
    coupled_uses: tuple[tuple[str, tuple[str | int, ...]], ...] = ()


_RELATIONS = {
    ast.Lt: ('<', 'bcc'), ast.LtE: ('<=', 'bhi'),
    ast.Gt: ('>', 'bls'), ast.GtE: ('>=', 'bcs'),
    ast.Eq: ('==', 'bne'), ast.NotEq: ('!=', 'beq'),
}
_RELATION_NODES = {value[0]: key for key, value in _RELATIONS.items()}


def _at(node, path):
    try:
        for step in path:
            node = node[step] if type(step) is int else getattr(node, step)
        return node
    except (AttributeError, IndexError, KeyError, TypeError) as exc:
        raise CompileError('source policy path requires its complete source topology') from exc


def _replace_at(node, path, replacement):
    parent = _at(node, path[:-1])
    final = path[-1]
    if type(final) is int:
        parent[final] = replacement
    else:
        setattr(parent, final, replacement)


def _integer(node, role, low, high):
    if (type(node) is not ast.Constant or type(node.value) is not int
            or not low <= node.value <= high):
        raise CompileError(role + ': strict bounded integer AST literal required')
    return node.value


def _uses(role):
    """Return explicit source uses while preserving one role/edit authority."""
    if (type(role.function) is not str or type(role.paths) is not tuple
            or not role.paths or type(role.coupled_uses) is not tuple):
        raise CompileError('explicit primary and coupled source uses required')
    uses = tuple((role.function, path) for path in role.paths) + role.coupled_uses
    for use in uses:
        if (type(use) is not tuple or len(use) != 2 or type(use[0]) is not str
                or type(use[1]) is not tuple or not use[1]
                or any(type(step) not in (str, int) or
                       (type(step) is int and step < 0) for step in use[1])):
            raise CompileError('each source use needs its function and exact AST path')
    if role.kind == 'signed_word_pair' and len(uses) != 2:
        raise CompileError('one positive and one negative WORD step source use required')
    return uses


def _extract(role, nodes):
    if role.kind in ('unsigned_relation', 'signed_relation'):
        if any(type(node) not in _RELATIONS for node in nodes):
            raise CompileError(role.name + ': one declared comparison relation required')
        relations = {_RELATIONS[type(node)][0] for node in nodes}
        if len(relations) != 1:
            raise CompileError(role.name + ': its coupled comparison uses must agree')
        return relations.pop()
    if role.kind == 'signed_word_pair':
        positive = _integer(nodes[0], role.name, 1, 65535)
        negative = _integer(nodes[1], role.name, 0, 65535)
        if negative != (-positive) & 65535:
            raise CompileError(role.name + ': source negative step must equal u16(-positive step)')
        return positive
    limits = {'word': (0, 65535), 'nonzero_word': (1, 65535),
              'byte': (0, 255), 'shift': (1, 8),
              'long': (0, 0xffffffff), 'moveq': (0, 127),
              'quick': (1, 8), 'direction_mask': (1, 65535),
              'direction_bit': (1, 65535), 'long_bit': (1, 0x80000000)}
    low, high = limits[role.kind]
    values = [_integer(node, role.name, low, high) for node in nodes]
    if len(set(values)) != 1:
        raise CompileError(role.name + ': its distinct source uses must agree')
    value = values[0]
    if role.kind == 'direction_mask' and value not in (4, 8, 12):
        raise CompileError(role.name + ': supported direction WORD mask is 4, 8 or 12')
    if role.kind == 'direction_bit' and value not in (4, 8):
        raise CompileError(role.name + ': supported positive direction bit is 4 or 8')
    if role.kind == 'long_bit' and value & (value - 1):
        raise CompileError(role.name + ': confirmation must be one LONG bit, not a bit combination')
    return value


def _canonical_node(role, index):
    if role.kind in ('unsigned_relation', 'signed_relation'):
        return _RELATION_NODES[role.default]()
    value = ((-role.default) & 65535) if role.kind == 'signed_word_pair' and index == 1 else role.default
    return ast.Constant(value=value)


def admit_policy_source(source, declarations, approved, *, role_specs,
                        rule_builders, bindings, grammar, constraints=()):
    """Match supplied complete bodies and attach registered physical policies."""
    if type(source) is not str or len(source) > 300000:
        raise CompileError('bounded explicit Python text required')
    role_specs = tuple(role_specs)
    if any(type(role) is not SourceRole for role in role_specs):
        raise CompileError('explicit named source-role specifications required')
    if len({role.name for role in role_specs}) != len(role_specs):
        raise CompileError('each source-policy role has one edit authority')
    role_paths = [use for role in role_specs for use in _uses(role)]
    if len(set(role_paths)) != len(role_paths):
        raise CompileError('overlapping source-policy roles are not permitted')
    source_functions = frozenset(function for function, path in role_paths)
    try:
        supplied = ast.parse(source)
    except (SyntaxError, ValueError) as exc:
        raise CompileError('invalid business Python') from exc
    normalized = deepcopy(supplied)
    functions = {}
    supplied_functions = {}
    for actual, copy in zip(supplied.body, normalized.body):
        if isinstance(actual, ast.FunctionDef):
            if actual.name in supplied_functions:
                raise CompileError('duplicate complete business declaration')
            if (actual.body and isinstance(actual.body[0], ast.Expr)
                    and isinstance(actual.body[0].value, ast.Constant)
                    and type(actual.body[0].value.value) is str):
                actual.body = actual.body[1:]
                copy.body = copy.body[1:]
            supplied_functions[actual.name] = actual
            functions[copy.name] = copy
    if not source_functions <= functions.keys():
        raise CompileError('all registered helpers and complete source bodies required')
    values, provenance = {}, []
    for role in role_specs:
        uses = _uses(role)
        nodes = [_at(supplied_functions[function], path) for function, path in uses]
        values[role.name] = _extract(role, nodes)
        for index, (function, path) in enumerate(uses):
            _replace_at(functions[function], path,
                        ast.copy_location(_canonical_node(role, index), nodes[index]))
            provenance.append(dict(role=role.name, function=function,
                                   path=list(path), value=values[role.name],
                                   supplied_node=ast.dump(nodes[index], include_attributes=False),
                                   physical_pcs=list(role.physical_pcs), kind=role.kind))
    for constraint in constraints:
        constraint(values)
    ast.fix_missing_locations(normalized)
    records = semantic_functions(ast.unparse(normalized), declarations, approved)
    # No source effect is replaced by the canonical grammar representation.
    for name, actual in supplied_functions.items():
        records[name]['effects'] = ast.dump(actual, include_attributes=False)
    owner_rules = {}
    bindings = {binding.name: binding for binding in bindings}
    for builder in rule_builders:
        extra = builder(values)
        if type(extra) is not dict or not extra or not extra.keys() <= bindings.keys():
            raise CompileError('policy family must bind declared physical owners')
        if extra.keys() & owner_rules.keys() or any(type(rules) is not dict for rules in extra.values()):
            raise CompileError('each physical owner has one policy-rule authority')
        owner_rules.update(extra)
    for name, rules in owner_rules.items():
        records[name]['rules'].update(rules)
    selected = [bindings[name] for name in owner_rules]
    policy = dict(grammar=grammar, values=values,
                  owner_rules=owner_rules, provenance=provenance,
                  supplied_effects={name: records[name]['effects']
                                    for name in sorted(source_functions)},
                  physical_owners=len(selected),
                  interface_entries=sum(len(binding.entries) for binding in selected),
                  allocated_bytes=sum(end - start for binding in selected
                                      for start, end in binding.segments),
                  general_python=False, natural_input_domain_proven=False)
    return records, policy


# Complete actual Duel fields role topology125: finite new typed leaves only.
# Existing kinds, complete-body admission, path guards and owner widths stay
# unchanged.  A CCR relation is derived from the supplied real C/Z predicate,
# never returned from role.default.  Inverse is the explicit other arm of the
# same physical comparison, not an inferred general Python condition.
_CCR_RELATIONS125 = {(1, False): '<', (1, True): '>=',
                     (4, False): '==', (4, True): '!='}
_CCR_COMPLEMENTS125 = {'<': '>=', '>=': '<', '==': '!=', '!=': '=='}
_pre_fields_extract125 = _extract
_pre_fields_canonical125 = _canonical_node


def _frame_ccr_relation125(node, role):
    negated = False
    if type(node) is ast.UnaryOp and type(node.op) is ast.Not:
        negated = True
        node = node.operand
    if not (type(node) is ast.BinOp and type(node.op) is ast.BitAnd
            and type(node.left) is ast.Attribute and node.left.attr == 'status'
            and type(node.left.value) is ast.Name and node.left.value.id == 'frame'
            and type(node.right) is ast.Constant and type(node.right.value) is int
            and node.right.value in (1, 4)):
        raise CompileError(role.name + ': exact live Frame C/Z predicate required')
    value = _CCR_RELATIONS125[(node.right.value, negated)]
    return _CCR_COMPLEMENTS125[value] if role.kind == 'frame_ccr_inverse_relation' else value


def _extract(role, nodes):
    if role.kind in ('frame_ccr_relation', 'frame_ccr_inverse_relation'):
        values = {_frame_ccr_relation125(node, role) for node in nodes}
        if len(values) != 1:
            raise CompileError(role.name + ': explicit coupled live CCR predicates must agree')
        return values.pop()
    if role.kind == 'long_bit_index':
        values = {_integer(node, role.name, 0, 31) for node in nodes}
        if len(values) != 1:
            raise CompileError(role.name + ': coupled actual LONG bit indices must agree')
        return 1 << values.pop()
    if role.kind == 'dbra_word_count':
        values = {_integer(node, role.name, 0, 65534) for node in nodes}
        if len(values) != 1:
            raise CompileError(role.name + ': coupled actual DBRA WORD counters must agree')
        return values.pop() + 1
    return _pre_fields_extract125(role, nodes)


def _canonical_node(role, index):
    if role.kind in ('frame_ccr_relation', 'frame_ccr_inverse_relation'):
        value = role.default
        if value not in _CCR_COMPLEMENTS125:
            raise CompileError(role.name + ': canonical C/Z relation required')
        if role.kind == 'frame_ccr_inverse_relation':
            value = _CCR_COMPLEMENTS125[value]
        bit, negated = next(key for key, relation in _CCR_RELATIONS125.items() if relation == value)
        node = ast.BinOp(left=ast.Attribute(value=ast.Name(id='frame', ctx=ast.Load()),
            attr='status', ctx=ast.Load()), op=ast.BitAnd(), right=ast.Constant(value=bit))
        return ast.UnaryOp(op=ast.Not(), operand=node) if negated else node
    if role.kind == 'long_bit_index':
        value = role.default
        if type(value) is not int or not 1 <= value <= 0x80000000 or value & (value - 1):
            raise CompileError(role.name + ': canonical single LONG bit required')
        return ast.Constant(value=value.bit_length()-1)
    if role.kind == 'dbra_word_count':
        if type(role.default) is not int or not 1 <= role.default <= 65535:
            raise CompileError(role.name + ': canonical bounded DBRA WORD count required')
        return ast.Constant(value=role.default-1)
    return _pre_fields_canonical125(role, index)
