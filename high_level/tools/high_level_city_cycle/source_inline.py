"""Inline the supplied city-settlement helpers before typed effect lowering.

The helpers have no target allocations of their own. Their complete supplied
bodies are consumed; there is no stored old business body or file-read fallback.
Names intentionally match live locals of the original calling interface. This
small lexical contract is not a general Python optimizer or register allocator.
"""
import ast
from copy import deepcopy


# (typed parameters, result type, returned live local), never encoded code.
HELPERS = {
    'advance_income_depletion_tier': ((('threshold', 'Long'), ('tier', 'Word')), 'Word', 'tier'),
    'read_income_depletion_factor': ((('state', 'CityState'), ('tier', 'Word')), 'Word', 'reduction_factor'),
    'apply_income_reserve_depletion': ((('state', 'CityState'), ('city', 'Word'), ('reduction_factor', 'Word')), None, None),
    'prepare_city_expense_roster': ((('state', 'CityState'), ('city', 'Word')), 'Word', 'city'),
    'sum_roster_expense_amounts': ((('state', 'CityState'),), 'Long', 'total'),
    'sum_roster_category_fees': ((('state', 'CityState'), ('categories', 'Table')), 'Word', 'fees'),
    'calculate_city_expense': ((('state', 'CityState'), ('factor', 'Word'), ('categories', 'Table')), 'Long', 'fees'),
    'build_shortage_priority_scores': ((('state', 'CityState'),), None, None),
    'sort_shortage_priority_roster': ((('state', 'CityState'),), None, None),
    'deplete_shortage_amounts': ((('state', 'CityState'), ('outstanding', 'Long')), 'Long', 'outstanding'),
    'apply_shortage_penalties': ((('state', 'CityState'),), None, None),
}


def inline_settlement_helpers(tree):
    """Expand a complete supplied helper family, or reject partial/unsafe flow.

Old eleven-function source remains accepted without any helper declaration.
New source must supply all helpers, use each, and use lexical arguments/results
without silently discarding or substituting another live compatibility local.
The downstream typed frontend still checks all expanded statements and exits.
"""
    if not isinstance(tree, ast.Module):
        raise ValueError('an explicit parsed city module is required')
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    if len({node.name for node in functions}) != len(functions):
        raise ValueError('duplicate city function authority')
    supplied = {node.name: node for node in functions if node.name in HELPERS}
    calls = {node.func.id for node in ast.walk(tree)
             if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
             and node.func.id in HELPERS}
    if not supplied and not calls:
        return deepcopy(tree)
    if set(supplied) != set(HELPERS) or calls != set(HELPERS):
        raise ValueError('complete used settlement helper family is required')
    bodies = {}
    for name, node in supplied.items():
        signature, result_type, result_local = HELPERS[name]
        args = node.args
        if (node.decorator_list or node.type_params or args.posonlyargs or
                args.vararg or args.kwarg or args.kwonlyargs or args.defaults):
            raise ValueError('ordinary positional settlement helpers required')
        actual = tuple((arg.arg, arg.annotation.id if isinstance(arg.annotation, ast.Name) else None)
                       for arg in args.args)
        if actual != signature:
            raise ValueError('settlement helper parameters must retain their live meaning')
        valid_return = (isinstance(node.returns, ast.Name) and node.returns.id == result_type
                        if result_type else
                        isinstance(node.returns, ast.Constant) and node.returns.value is None)
        if not valid_return:
            raise ValueError('explicit settlement helper result type required')
        body = [deepcopy(statement) for statement in node.body
                if not (isinstance(statement, ast.Expr) and
                        isinstance(statement.value, ast.Constant) and
                        type(statement.value.value) is str)]
        returns = [item for statement in body for item in ast.walk(statement)
                   if isinstance(item, ast.Return)]
        if result_local:
            if (not body or not isinstance(body[-1], ast.Return) or len(returns) != 1 or
                    not isinstance(body[-1].value, ast.Name) or body[-1].value.id != result_local):
                raise ValueError('one final live-local helper result is required')
            body.pop()
        elif returns:
            raise ValueError('void helper must not introduce an early native exit')
        bodies[name] = body
    used = set()

    def expand(statements, stack=()):
        output = []
        for statement in statements:
            call = statement.value if isinstance(statement, (ast.Assign, ast.Expr)) else None
            if isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and call.func.id in HELPERS:
                name = call.func.id
                signature, _, result_local = HELPERS[name]
                if name in stack or len(stack) >= 4:
                    raise ValueError('recursive or unbounded settlement helper expansion')
                if (call.keywords or len(call.args) != len(signature) or
                        any(not isinstance(arg, ast.Name) or arg.id != param
                            for arg, (param, _) in zip(call.args, signature))):
                    raise ValueError('helper requires its actual live lexical arguments')
                if result_local:
                    if (not isinstance(statement, ast.Assign) or len(statement.targets) != 1 or
                            not isinstance(statement.targets[0], ast.Name) or
                            statement.targets[0].id != result_local):
                        raise ValueError('helper result may not be discarded or rebound')
                elif not isinstance(statement, ast.Expr):
                    raise ValueError('void helper is a statement, not a fabricated value')
                used.add(name)
                output.extend(expand(deepcopy(bodies[name]), stack + (name,)))
            else:
                statement = deepcopy(statement)
                for field in ('body', 'orelse'):
                    nested = getattr(statement, field, None)
                    if isinstance(nested, list):
                        setattr(statement, field, expand(nested, stack))
                if any(isinstance(item, ast.Call) and isinstance(item.func, ast.Name)
                       and item.func.id in HELPERS for item in ast.walk(statement)):
                    raise ValueError('helper calls must be explicit result or void statements')
                output.append(statement)
        return output

    normalized = deepcopy(tree)
    normalized.body = [node for node in normalized.body
                       if not (isinstance(node, ast.FunctionDef) and node.name in HELPERS)]
    for node in normalized.body:
        if isinstance(node, ast.FunctionDef):
            node.body = expand(node.body)
    if used != set(HELPERS):
        raise ValueError('all supplied settlement algorithms must reach original entrances')
    return ast.fix_missing_locations(normalized)
