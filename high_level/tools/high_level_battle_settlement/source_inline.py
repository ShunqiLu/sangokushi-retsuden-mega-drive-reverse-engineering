"""Finite expansion of supplied settlement algorithms before typed lowering.

Only signatures/result/local roles are allocated here. Complete supplied helper
bodies participate in generation; no old body or target instruction is stored.
This is a lexical domain contract, not a general Python optimizer.
"""
import ast
from copy import deepcopy
from .inline_contracts import HELPERS


CONTEXT_FIELDS = {
    'RatioInputs': ('numerator', 'denominator'),
    'PackedTailRepair': ('deleted', 'copy_source', 'copy_target', 'remaining_count'),
}


def dump(node):
    return ast.dump(node, include_attributes=False)


def inline_settlement(tree, family):
    if not isinstance(tree, ast.Module) or family not in HELPERS:
        raise ValueError('explicit parsed settlement family required')
    contracts = HELPERS[family]
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    if len(functions) != sum(isinstance(n, ast.FunctionDef) for n in tree.body):
        raise ValueError('duplicate settlement source function authority')
    imports = set()
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            if any(a.asname is not None or a.name == '*' for a in node.names):
                raise ValueError('explicit nonaliased settlement imports required')
            imports.update(a.name for a in node.names)
    globals_available = set(functions) | imports | {'tuple', 'bool'}
    for node in functions.values():
        if node.type_params:
            raise ValueError('generic settlement type parameters unsupported')
        local = {a.arg for a in node.args.args} | {
            n.id for n in ast.walk(node) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}
        if local & (imports | set(functions)):
            raise ValueError('settlement intrinsic/helper shadowing unsupported')
        used = {n.id for n in ast.walk(node) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
        if used - local - globals_available:
            raise ValueError('actual settlement imports/declarations required: ' + ','.join(sorted(used - local - globals_available)))
    supplied = {n: functions[n] for n in contracts if n in functions}
    if not supplied:
        return deepcopy(tree), dict(family=family, helpers=0, expanded_calls=0)
    if set(supplied) != set(contracts):
        raise ValueError('complete settlement helper family required')
    bodies = {}
    results = {}
    for name, node in supplied.items():
        spec = contracts[name]
        args = node.args
        actual = [(a.arg, ast.unparse(a.annotation)) for a in args.args]
        if (actual != [tuple(a) for a in spec['params']] or node.decorator_list or
                args.posonlyargs or args.kwonlyargs or args.vararg or args.kwarg or
                args.defaults or args.kw_defaults or ast.unparse(node.returns) != spec['result']):
            raise ValueError('exact settlement helper signature required: ' + name)
        body = [deepcopy(s) for s in node.body if not (isinstance(s, ast.Expr) and
                isinstance(s.value, ast.Constant) and type(s.value.value) is str)]
        if spec['kind'] == 'expression':
            for param, typ in spec['params']:
                width = 32 if typ == 'Long' else 16
                expected = ast.parse('uint(' + param + ', ' + str(width) + ')').body[0]
                if not body or dump(body.pop(0)) != dump(expected):
                    raise ValueError('exact pre-DATA typed policy admission required')
        returns = [n for s in body for n in ast.walk(s) if isinstance(n, ast.Return)]
        if spec['returned'] is None:
            if returns:
                raise ValueError('void settlement helper cannot add a native return')
            result = None
        else:
            if not body or not isinstance(body[-1], ast.Return) or len(returns) != 1:
                raise ValueError('one terminal settlement helper result required')
            result = body.pop().value
            if spec['kind'] != 'expression' and dump(result) != dump(ast.parse(spec['returned'], mode='eval').body):
                raise ValueError('actual helper result local/view contract required')
        if spec['kind'] == 'expression' and body:
            raise ValueError('pure policy permits only typed admission and supplied result')
        bodies[name], results[name] = body, result
    used_helpers = set()
    expanded_calls = 0

    class Substitute(ast.NodeTransformer):
        def __init__(self, names, fields=None):
            self.names, self.fields = names, fields or {}

        def visit_Name(self, node):
            if node.id in self.names:
                replacement = deepcopy(self.names[node.id])
                if hasattr(replacement, 'ctx'):
                    replacement.ctx = node.ctx
                return replacement
            return node

        def visit_Attribute(self, node):
            if isinstance(node.value, ast.Name) and (node.value.id, node.attr) in self.fields:
                return deepcopy(self.fields[node.value.id, node.attr])
            return self.generic_visit(node)

        def visit_Call(self, node):
            nonlocal expanded_calls
            node = self.generic_visit(node)
            if isinstance(node.func, ast.Name) and node.func.id in contracts:
                name = node.func.id
                if contracts[name]['kind'] != 'expression':
                    return node
                spec = contracts[name]
                if node.keywords or len(node.args) != len(spec['params']):
                    raise ValueError('exact policy argument arity required')
                expression = results[name]
                replacements = {}
                for arg, (param, _) in zip(node.args, spec['params']):
                    # Policy actuals are plain locals. They cannot reread or reorder
                    # a DATA expression through substitution or duplicate an effect.
                    if not isinstance(arg, ast.Name) or arg.id != param:
                        raise ValueError('policy requires its complete live lexical argument')
                    replacements[param] = arg
                used_helpers.add(name)
                expanded_calls += 1
                return Substitute(replacements).visit(deepcopy(expression))
            return node

    def expand(statements, stack=(), fields=None):
        nonlocal expanded_calls
        fields = dict(fields or {})
        output = []
        for original in statements:
            if isinstance(original, ast.Assign):
                assigned = {n.id for target in original.targets for n in ast.walk(target)
                            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}
                if assigned & {name for name, _ in fields}:
                    raise ValueError('live settlement result context cannot be rebound')
            statement = Substitute({}, fields).visit(deepcopy(original))
            value = statement.value if isinstance(statement, (ast.Assign, ast.Expr)) else None
            if (isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and
                    value.func.id in contracts and contracts[value.func.id]['kind'] != 'expression'):
                name, spec = value.func.id, contracts[value.func.id]
                if name in stack or len(stack) >= 8:
                    raise ValueError('recursive settlement helper expansion unsupported')
                if (value.keywords or len(value.args) != len(spec['params']) or
                        any(not isinstance(arg, ast.Name) or arg.id != param
                            for arg, (param, _) in zip(value.args, spec['params']))):
                    raise ValueError('helper requires actual live lexical arguments: ' + name)
                result = results[name]
                if result is None:
                    if not isinstance(statement, ast.Expr):
                        raise ValueError('void helper cannot invent a result')
                elif not isinstance(statement, ast.Assign) or len(statement.targets) != 1:
                    raise ValueError('helper result must be captured exactly')
                elif spec['kind'] == 'context':
                    target = statement.targets[0]
                    if not isinstance(target, ast.Name) or target.id in functions or target.id in imports:
                        raise ValueError('named domain result required')
                    for field, local in zip(CONTEXT_FIELDS[spec['result']], result.args):
                        fields[target.id, field] = deepcopy(local)
                elif dump(statement.targets[0]) != dump(ast.parse(spec['returned'] + ' = None').body[0].targets[0]):
                    raise ValueError('helper output local/tuple cannot be ignored or rebound')
                used_helpers.add(name)
                expanded_calls += 1
                output += expand(bodies[name], stack + (name,), fields)
                continue
            for attr in ('body', 'orelse', 'finalbody'):
                nested = getattr(statement, attr, None)
                if isinstance(nested, list):
                    setattr(statement, attr, expand(nested, stack, fields))
            if isinstance(statement, ast.Try):
                for handler in statement.handlers:
                    handler.body = expand(handler.body, stack, fields)
            if any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in contracts
                   for n in ast.walk(statement)):
                raise ValueError('helper must be an explicit pure policy/result/void statement')
            output.append(statement)
        return output

    normalized = deepcopy(tree)
    normalized.body = [n for n in normalized.body if not (isinstance(n, ast.FunctionDef) and n.name in contracts)]
    for node in normalized.body:
        if isinstance(node, ast.FunctionDef):
            node.body = expand(node.body)
    if used_helpers != set(contracts):
        raise ValueError('every supplied helper must reach an original settlement entrance')
    retained = []
    for node in normalized.body:
        if isinstance(node, ast.ImportFrom) and node.module == 'contexts_settlement':
            if node.level != 1 or any(a.name not in CONTEXT_FIELDS for a in node.names):
                raise ValueError('only explicit settlement domain contexts are permitted')
            continue
        if isinstance(node, ast.ImportFrom) and node.module == 'domain':
            node.names = [a for a in node.names if a.name != 'uint']
        retained.append(node)
    normalized.body = retained
    return ast.fix_missing_locations(normalized), dict(family=family, helpers=len(contracts), expanded_calls=expanded_calls)
