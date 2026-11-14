"""Finite logical-source AST admission and ordinary Z80 target lowering.

This is a constrained compatibility backend, not a general Python compiler or
an audio/CPU emulator. Source clauses are consumed individually using explicit
semantic-node-to-target ABI schedules, and the complete source AST is checked.
Unsupported semantic/topology changes fail closed. There is no file reader,
runtime assembly/IR importer, original-code payload, or assembly-text fallback.
"""
from __future__ import annotations

import ast
import copy
import sys
from collections.abc import Mapping

from . import target
from . import channel_layout


MAX_SOURCE_CHARACTERS = 4_000_000


class CompileError(ValueError):
    pass


def _stable_ast_dump(node):
    """Keep empty fields explicit across Python's AST-display default change.

    Python 3.13 added show_empty and changed its default representation. The
    compatibility contract includes those fields; this affects serialization
    only, never source topology, admitted values or target operation selection.
    Older Python versions already include empty fields by default.
    """
    if sys.version_info >= (3, 13):
        return ast.dump(node, include_attributes=False, show_empty=True)
    return ast.dump(node, include_attributes=False)


def _strict_integer(value, low, high, label):
    if type(value) is not int or not low <= value <= high:
        raise CompileError(label + ': strict bounded integer required')
    return value


def _node(tree, path):
    try:
        for item in path:
            tree = tree[item] if type(item) is int else getattr(tree, item)
    except (AttributeError, IndexError, TypeError) as error:
        raise CompileError('the declared semantic clause is absent') from error
    if not isinstance(tree, ast.AST):
        raise CompileError('the semantic binding must select an actual AST node')
    return tree


_LEVEL_HELPER = '_write_instrument_level_fields'
_LEVEL_LIVE_VALUES = ('channel_cursor', 'conditions', 'count_and_data',
                      'lookup_cursor', 'parameter_cursor', 'sample', 'stack_cursor')
_LEVEL_CALLERS = {'load_instrument': 4, 'refresh_instrument_volume': 0,
                  'adjust_channel_volume': 6, 'adjust_fm_channel_volume': 3}
_LEVEL_TEMPORARIES = {
    'inactive_words': ('alternate_group', 1),
    'pointer_low': ('observed_byte', 2),
    'pointer_high': ('observed_byte', 3),
    'level_source': ('observed_byte', 4),
    'channel_delta': ('observed_byte', 5),
    'adjusted_level': ('arithmetic_result', 6),
    'register_selector': ('observed_byte', 7),
    'write_outcome': ('updated_audio_values', 8),
    'restored_words': ('alternate_group', 9),
}


def _level_mask_node(body):
    matches = [node for statement in body for node in ast.walk(statement)
               if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitAnd)
               and isinstance(node.left, ast.Name) and node.left.id == 'sample']
    if len(matches) != 1 or not isinstance(matches[0].right, ast.Constant):
        raise CompileError('instrument level mask must be one literal byte rule')
    node = matches[0].right
    _strict_integer(node.value, 0, 255, 'instrument level mask')
    return node


def _normalize_level_helper(tree):
    """Inline one supplied algorithm, without adding a native CALL/stack layer.

    The four old tails have identical effects but different temporary names.
    Normalize only that finite alpha-renaming and the explicit seven-value
    helper transfer. Every supplied algorithm statement is then checked by the
    complete original semantic-clause contract, not replaced by saved source.
    A legacy source with four explicit tails remains admissible for comparison.
    """
    helpers = [node for node in tree.body if isinstance(node, ast.FunctionDef)
               and node.name == _LEVEL_HELPER]
    if not helpers:
        return []
    if len(helpers) != 1:
        raise CompileError('one instrument level helper definition required')
    helper = helpers[0]
    signature = ast.parse('''
def _write_instrument_level_fields(
        state: AudioState, *, channel_cursor: Word, conditions: Byte,
        count_and_data: Word, lookup_cursor: Word, parameter_cursor: Word,
        sample: Byte, stack_cursor: Word, continuation: Continuation,
) -> tuple[Word, Byte, Word, Word, Word, Byte, Word]:
    pass
''').body[0]
    if (helper.decorator_list or getattr(helper, 'type_params', []) or
            _stable_ast_dump(helper.args) != _stable_ast_dump(signature.args) or
            _stable_ast_dump(helper.returns) != _stable_ast_dump(signature.returns)):
        raise CompileError('unsupported instrument level helper signature')
    if (len(helper.body) < 3 or not isinstance(helper.body[0], ast.Expr) or
            not isinstance(helper.body[0].value, ast.Constant) or
            type(helper.body[0].value.value) is not str or
            not 1 <= len(helper.body[0].value.value) <= 4096):
        raise CompileError('bounded inert instrument level documentation required')
    expected_return = ast.parse('return ' + ', '.join(_LEVEL_LIVE_VALUES)).body[0]
    if _stable_ast_dump(helper.body[-1]) != _stable_ast_dump(expected_return):
        raise CompileError('all seven live instrument level values must be returned')
    algorithm = helper.body[1:-1]
    mask = _level_mask_node(algorithm)
    references = [node for node in ast.walk(tree) if isinstance(node, ast.Name)
                  and node.id == _LEVEL_HELPER]
    if len(references) != len(_LEVEL_CALLERS):
        raise CompileError('exactly four explicit instrument level helper calls required')
    expected_call = ast.parse(', '.join(_LEVEL_LIVE_VALUES) + ' = ' + _LEVEL_HELPER +
                              '(state, ' + ', '.join(name + '=' + name
                                  for name in _LEVEL_LIVE_VALUES) +
                              ', continuation=inputs.continuation)').body[0]
    copies = []
    for caller_name, offset in _LEVEL_CALLERS.items():
        callers = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                   and node.name == caller_name]
        if len(callers) != 1:
            raise CompileError('instrument level caller is missing or ambiguous')
        caller = callers[0]
        positions = [index for index, statement in enumerate(caller.body)
                     if any(isinstance(node, ast.Name) and node.id == _LEVEL_HELPER
                            for node in ast.walk(statement))]
        if (len(positions) != 1 or
                _stable_ast_dump(caller.body[positions[0]]) != _stable_ast_dump(expected_call)):
            raise CompileError('instrument level caller must transfer all live values unchanged')

        class InlineLevel(ast.NodeTransformer):
            def visit_Name(self, node):
                if node.id == 'continuation':
                    return ast.copy_location(ast.Attribute(
                        value=ast.Name(id='inputs', ctx=ast.Load()),
                        attr='continuation', ctx=ast.Load()), node)
                if node.id in _LEVEL_TEMPORARIES:
                    prefix, number = _LEVEL_TEMPORARIES[node.id]
                    node.id = prefix + '_' + str(number + offset)
                return node

        supplied = [InlineLevel().visit(copy.deepcopy(statement)) for statement in algorithm]
        copied_mask = _level_mask_node(supplied)
        if copied_mask.value != mask.value:
            raise CompileError('instrument level rule normalization changed its value')
        copies.append(copied_mask)
        position = positions[0]
        caller.body[position:position + 1] = supplied
    tree.body.remove(helper)
    return copies


def _bounded_domain_doc(statement):
    if (not isinstance(statement, ast.Expr) or not isinstance(statement.value, ast.Constant) or
            type(statement.value.value) is not str or not 1 <= len(statement.value.value) <= 4096):
        raise CompileError('bounded inert domain documentation required')


def _declaration_import(module, names):
    return ast.ImportFrom(module=module, names=[ast.alias(name=name) for name in names], level=1)


def _normalize_voice_domains(trees):
    """Project supplied live transactions onto the finite original target ABI.

    All seven actual domain bodies are expanded and subsequently admitted as
    part of the complete audio AST. No old body or target AST is substituted.
    Only explicit data-cell projection, declared temporary alpha-renaming and
    these fixed, nonrecursive fragment calls are supported. Native field/FM
    service calls, their stacks and all returned aliases remain real clauses.
    """
    contexts = trees['contexts_voice.py']
    domain = trees['business_voice_loading.py']
    voice = trees['business_voice.py']
    fields = target.VOICE_CONTEXT_FIELDS
    entries = target.VOICE_DOMAIN_ENTRIES
    helpers = target.VOICE_DOMAIN_HELPERS
    context_import = _declaration_import('contexts_voice', tuple(fields))
    domain_import = _declaration_import('business_voice_loading',
                                        tuple(entry[1] for entry in entries.values()))
    if len(contexts.body) != 3 + len(fields):
        raise CompileError('voice contexts must contain only declared live data cells')
    _bounded_domain_doc(contexts.body[0])
    expected_imports = (ast.ImportFrom(module='dataclasses',
                        names=[ast.alias(name='dataclass')], level=0),
                        _declaration_import('domain', ('Byte', 'Word')))
    if any(_stable_ast_dump(actual) != _stable_ast_dump(expected)
           for actual, expected in zip(contexts.body[1:3], expected_imports)):
        raise CompileError('voice context data imports differ')
    for actual, (name, cells) in zip(contexts.body[3:], fields.items()):
        if not isinstance(actual, ast.ClassDef) or actual.name != name or not actual.body:
            raise CompileError('voice context declaration or ownership differs')
        _bounded_domain_doc(actual.body[0])
        declaration = '@dataclass(slots=True)\nclass ' + name + ':\n    "Context."\n'
        declaration += ''.join('    ' + cell + ': ' +
            ('Byte' if old in ('conditions', 'sample') else 'Word') + '\n'
            for cell, old in cells.items())
        expected = ast.parse(declaration).body[0]
        checked = copy.deepcopy(actual)
        checked.body[0] = copy.deepcopy(expected.body[0])
        if _stable_ast_dump(checked) != _stable_ast_dump(expected):
            raise CompileError('voice contexts cannot hide algorithms, defaults or extra cells')
    if len(domain.body) != 3 + len(helpers):
        raise CompileError('complete uniquely owned voice domain required')
    _bounded_domain_doc(domain.body[0])
    imports = (_declaration_import('domain', ('AudioState', 'Continuation', 'u8', 'u16',
        'low', 'high', 'replace_low', 'replace_high', 'logic_conditions', 'sum_word')),
        context_import)
    if any(_stable_ast_dump(actual) != _stable_ast_dump(expected)
           for actual, expected in zip(domain.body[1:3], imports)):
        raise CompileError('voice domain imports differ')
    algorithms = {}
    for actual, (name, parameters) in zip(domain.body[3:], helpers.items()):
        signature = 'def ' + name + '(state: AudioState, ' + parameters[0] + ': ' + parameters[1]
        if len(parameters) == 4:
            signature += ', ' + parameters[2] + ': ' + parameters[3]
        expected = ast.parse(signature + ') -> None:\n    pass\n').body[0]
        if (not isinstance(actual, ast.FunctionDef) or actual.name != name or
                actual.decorator_list or getattr(actual, 'type_params', []) or
                _stable_ast_dump(actual.args) != _stable_ast_dump(expected.args) or
                _stable_ast_dump(actual.returns) != _stable_ast_dump(expected.returns) or
                len(actual.body) < 2):
            raise CompileError('unsupported voice domain function/signature')
        _bounded_domain_doc(actual.body[0])
        algorithms[name] = actual
    if len(voice.body) < 5 or any(_stable_ast_dump(actual) != _stable_ast_dump(expected)
            for actual, expected in zip(voice.body[3:5], (context_import, domain_import))):
        raise CompileError('voice entry imports must point to the actual domain owners')
    del voice.body[3:5]
    temporary_names = {
        'read_indexed_envelope': {'address_sum': 'arithmetic_result_1', 'envelope_byte': 'observed_byte_2'},
        'lookup_instrument': {'bank_base': 'observed_word_1', 'private_bank_enabled': 'observed_byte_2',
                             'local_bank_low': 'observed_byte_3', 'local_bank_high': 'observed_byte_4',
                             'address_sum': 'arithmetic_result_5'},
        'offset_instrument': {'address_sum': 'arithmetic_result_1'},
        'load_instrument': {'stereo_bits': 'observed_byte_1'},
        'write_next_instrument_field': {'fm_selector': 'observed_byte_1', 'field_byte': 'observed_byte_2'},
    }
    used = set()

    def expand_call(call, caller, active):
        name = call.func.id
        if name in active:
            raise CompileError('recursive voice fragments are unsupported')
        function = algorithms[name]
        parameters = [arg.arg for arg in function.args.args]
        if call.keywords or len(call.args) != len(parameters):
            raise CompileError('voice fragments require all explicit positional live values')
        used.add(name)
        bindings = dict(zip(parameters, call.args))
        renames = dict(temporary_names[caller])
        if name in ('write_voice_fm_register', 'call_instrument_field'):
            address = bindings['return_address']
            allowed = ({1262: 'updated_audio_values_2', 1289: 'updated_audio_values_3'}
                       if name == 'write_voice_fm_register' else
                       {1265: 'updated_audio_values_3', 1273: 'updated_audio_values_4'})
            if not isinstance(address, ast.Constant) or type(address.value) is not int or address.value not in allowed:
                raise CompileError('unsupported original voice service continuation')
            renames['hardware_outcome' if name == 'write_voice_fm_register' else 'field_outcome'] = allowed[address.value]

        class BindFragment(ast.NodeTransformer):
            def visit_Name(self, node):
                if node.id in bindings:
                    bound = copy.deepcopy(bindings[node.id])
                    if isinstance(bound, ast.Name):
                        bound.ctx = copy.deepcopy(node.ctx)
                    return ast.copy_location(bound, node)
                if node.id in renames:
                    node.id = renames[node.id]
                return node

        statements = [BindFragment().visit(copy.deepcopy(statement)) for statement in function.body[1:]]
        return expand_statements(statements, caller, (*active, name))

    def expand_statements(statements, caller, active):
        result = []
        for statement in statements:
            if (isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call)
                    and isinstance(statement.value.func, ast.Name) and statement.value.func.id in algorithms):
                result.extend(expand_call(statement.value, caller, active))
                continue
            for field, value in ast.iter_fields(statement):
                if isinstance(value, list) and value and all(isinstance(item, ast.stmt) for item in value):
                    setattr(statement, field, expand_statements(value, caller, active))
            result.append(statement)
        return result

    for caller, (context_type, algorithm) in entries.items():
        candidates = [node for node in voice.body if isinstance(node, ast.FunctionDef) and node.name == caller]
        if len(candidates) != 1:
            raise CompileError('voice entry missing or ambiguous')
        function = candidates[0]
        variable = helpers[algorithm][0]
        cells = fields[context_type]
        construction = ast.parse(variable + ' = ' + context_type + '(' +
            ', '.join(cell + '=inputs.' + old for cell, old in cells.items()) + ')').body[0]
        invocation = algorithm + '(state, ' + variable
        if len(helpers[algorithm]) == 4:
            invocation += ', inputs.continuation'
        expected_call = ast.parse(invocation + ')').body[0]
        if (len(function.body) < 7 or _stable_ast_dump(function.body[4]) != _stable_ast_dump(construction)
                or _stable_ast_dump(function.body[5]) != _stable_ast_dump(expected_call)):
            raise CompileError('voice entry must bind and transfer every declared live input')
        initialization = [ast.parse(old + ' = inputs.' + old).body[0] for old in cells.values()]
        supplied = expand_call(function.body[5].value, caller, ())
        function.body[4:6] = initialization + supplied

        class ProjectCells(ast.NodeTransformer):
            def visit_Attribute(self, node):
                if isinstance(node.value, ast.Name) and node.value.id == variable:
                    if node.attr not in cells:
                        raise CompileError('undeclared voice transaction cell')
                    return ast.copy_location(ast.Name(id=cells[node.attr], ctx=copy.deepcopy(node.ctx)), node)
                return self.generic_visit(node)

        ProjectCells().visit(function)
        if any(isinstance(node, ast.Name) and (node.id == variable or node.id in algorithms)
               for node in ast.walk(function)):
            raise CompileError('voice transaction/helper use outside the declared finite fragments')
    if used != set(algorithms):
        raise CompileError('an owned voice algorithm would be ignored during generation')
    return {name: tree for name, tree in trees.items()
            if name not in ('contexts_voice.py', 'business_voice_loading.py')}


def _normalize_lifecycle_domains(trees):
    """Consume the complete supplied loading/stop/fade/reset transactions.

    Finite context projection and nested actual helper expansion retain the
    original target schedule. Terminal delegation is explicit return-to-helper,
    not an invented extra native CALL or a fabricated successful service. The
    ownership declarations contain schemas and alpha routes, never old bodies.
    """
    loaders = trees['business_loaders.py']
    contexts = trees['contexts_lifecycle.py']
    entries = target.LIFECYCLE_ENTRY_LAYOUT
    cells = target.LIFECYCLE_CONTEXT_FIELDS
    helpers = target.LIFECYCLE_SERVICE_LAYOUT
    imports = [_declaration_import('contexts_lifecycle', tuple(cells))]
    for owner, functions in target.LIFECYCLE_MODULE_FUNCTIONS.items():
        public = [row['algorithm'] for row in entries.values() if row['owner'] == owner]
        if public:
            imports.append(_declaration_import(owner[:-3], tuple(public)))
    if (len(loaders.body) < 3 + len(imports) or any(
            _stable_ast_dump(actual) != _stable_ast_dump(expected)
            for actual, expected in zip(loaders.body[3:3 + len(imports)], imports))):
        raise CompileError('complete lifecycle boundary imports must point to actual owners')
    del loaders.body[3:3 + len(imports)]
    if len(contexts.body) != 3 + len(cells):
        raise CompileError('complete lifecycle live-context declarations required')
    _bounded_domain_doc(contexts.body[0])
    context_imports = (ast.ImportFrom(module='dataclasses', names=[ast.alias(name='dataclass')], level=0),
                       _declaration_import('domain', ('Byte', 'Word')))
    if any(_stable_ast_dump(actual) != _stable_ast_dump(expected)
           for actual, expected in zip(contexts.body[1:3], context_imports)):
        raise CompileError('lifecycle context imports differ')
    for actual, (name, fields) in zip(contexts.body[3:], cells.items()):
        if not isinstance(actual, ast.ClassDef) or actual.name != name or not actual.body:
            raise CompileError('lifecycle context ownership differs')
        _bounded_domain_doc(actual.body[0])
        text = '@dataclass(slots=True)\nclass ' + name + ':\n    "Context."\n'
        text += ''.join('    ' + field + ': ' + ('Byte' if old in ('conditions', 'sample') else 'Word') + '\n'
                        for field, old in fields.items())
        expected = ast.parse(text).body[0]
        checked = copy.deepcopy(actual)
        checked.body[0] = copy.deepcopy(expected.body[0])
        if _stable_ast_dump(checked) != _stable_ast_dump(expected):
            raise CompileError('lifecycle contexts cannot hide methods, extra cells or defaults')
    domain_import = loaders.body[1]
    layouts = dict(helpers)
    layouts.update({row['algorithm']: row for row in entries.values()})
    supplied_functions = {}
    for owner, names in target.LIFECYCLE_MODULE_FUNCTIONS.items():
        module = trees[owner]
        header = [domain_import] + [_declaration_import(module_name, tuple(imported))
                                  for module_name, imported in target.LIFECYCLE_MODULE_IMPORTS[owner]]
        if len(module.body) != 1 + len(header) + len(names):
            raise CompileError(owner + ': complete sole lifecycle owner required')
        _bounded_domain_doc(module.body[0])
        if any(_stable_ast_dump(actual) != _stable_ast_dump(expected)
               for actual, expected in zip(module.body[1:1 + len(header)], header)):
            raise CompileError(owner + ': declared lifecycle imports differ')
        for actual, name in zip(module.body[1 + len(header):], names):
            layout = layouts[name]
            expected = ast.parse('def ' + name + '(state: AudioState, lifecycle: ' + layout['context'] +
                                 ', continuation: Continuation) -> None:\n    pass\n').body[0]
            if (not isinstance(actual, ast.FunctionDef) or actual.name != name or actual.decorator_list
                    or getattr(actual, 'type_params', []) or len(actual.body) < 2
                    or _stable_ast_dump(actual.args) != _stable_ast_dump(expected.args)
                    or _stable_ast_dump(actual.returns) != _stable_ast_dump(expected.returns)
                    or layout['owner'] != owner or name in supplied_functions):
                raise CompileError('unsupported lifecycle signature or actual function ownership')
            _bounded_domain_doc(actual.body[0])
            supplied_functions[name] = actual
    if set(supplied_functions) != set(layouts):
        raise CompileError('complete unique lifecycle implementations required')
    stride_body = supplied_functions['write_operator_release_group'].body[1:]
    stride_calls = [node for statement in stride_body for node in ast.walk(statement)
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'sum_byte']
    if (len(stride_calls) != 1 or len(stride_calls[0].args) != 2
            or not isinstance(stride_calls[0].args[1], ast.Constant)):
        raise CompileError('one actual literal operator-register BYTE stride required')
    stride_value = _strict_integer(stride_calls[0].args[1].value, 1, 255, 'operator-register stride')
    used_helpers, stride_nodes = set(), []
    keys = {row['algorithm']: name for name, row in entries.items()}
    keys.update({name: name for name in helpers})

    class Alpha(ast.NodeTransformer):
        def __init__(self, renames): self.renames = renames
        def visit_Name(self, node):
            if node.id == 'continuation':
                return ast.copy_location(ast.Attribute(value=ast.Name(id='inputs', ctx=ast.Load()),
                    attr='continuation', ctx=ast.Load()), node)
            if node.id in self.renames: node.id = self.renames[node.id]
            return node

    for public_name, layout in entries.items():
        candidates = [node for node in loaders.body if isinstance(node, ast.FunctionDef) and node.name == public_name]
        if len(candidates) != 1: raise CompileError('public lifecycle boundary missing or ambiguous')
        function = candidates[0]
        fields = layout['fields']
        construction = ast.parse('lifecycle = ' + layout['context'] + '(' +
            ', '.join(field + '=inputs.' + old for field, old in fields.items()) + ')').body[0]
        invocation = ast.parse(layout['algorithm'] + '(state, lifecycle, inputs.continuation)').body[0]
        if (len(function.body) != 7 or _stable_ast_dump(function.body[4]) != _stable_ast_dump(construction)
                or _stable_ast_dump(function.body[5]) != _stable_ast_dump(invocation)
                or not isinstance(function.body[6], ast.Return)):
            raise CompileError('lifecycle boundary must transfer all and only its real inputs')
        result_boundary = copy.deepcopy(function.body[6])

        def expand_function(name, aliases=None, active=()):
            if name in active: raise CompileError('recursive lifecycle fragments are not supported')
            aliases = {} if aliases is None else aliases
            renames = {readable: aliases.get(canonical, canonical)
                       for readable, canonical in layouts[name]['temporaries'].items()}
            actual = [Alpha(renames).visit(copy.deepcopy(statement)) for statement in supplied_functions[name].body[1:]]
            rows = target.LIFECYCLE_CALL_BINDINGS.get(keys[name], [])
            index = 0
            if name == 'write_operator_release_group':
                calls = [node for statement in actual for node in ast.walk(statement)
                         if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'sum_byte']
                if len(calls) != 1 or calls[0].args[1].value != stride_value:
                    raise CompileError('actual operator-register stride projection differs')
                stride_nodes.append(calls[0].args[1])

            def expand(statements):
                nonlocal index
                output = []
                for statement in statements:
                    call = statement.value if isinstance(statement, (ast.Expr, ast.Return)) else None
                    if isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and call.func.id in helpers:
                        service = call.func.id
                        terminal = isinstance(statement, ast.Return)
                        expected = ast.parse(('return ' if terminal else '') + service +
                                             '(state, lifecycle, inputs.continuation)').body[0]
                        if (_stable_ast_dump(statement) != _stable_ast_dump(expected) or index >= len(rows)
                                or rows[index]['service'] != service or rows[index]['terminal'] != terminal):
                            raise CompileError('unsupported lifecycle service routing, terminal or live binding')
                        row = rows[index]; index += 1
                        used_helpers.add(service)
                        bound = {child: aliases.get(parent, parent) for child, parent in row['temporary_aliases'].items()}
                        output.extend(expand_function(service, bound, (*active, name)))
                        continue
                    if isinstance(statement, ast.Return):
                        if statement.value is not None: raise CompileError('lifecycle fragments cannot fabricate result values')
                        output.append(copy.deepcopy(result_boundary)); continue
                    for field, value in ast.iter_fields(statement):
                        if isinstance(value, list) and value and all(isinstance(part, ast.stmt) for part in value):
                            setattr(statement, field, expand(value))
                    output.append(statement)
                return output
            expanded = expand(actual)
            if index != len(rows): raise CompileError('a declared lifecycle transaction would be ignored')
            return expanded

        initialization = [ast.parse(old + ' = inputs.' + old).body[0] for old in fields.values()]
        function.body[4:] = initialization + expand_function(layout['algorithm'])
        class ProjectCells(ast.NodeTransformer):
            def visit_Attribute(self, node):
                if isinstance(node.value, ast.Name) and node.value.id == 'lifecycle':
                    if node.attr not in fields: raise CompileError('access to absent lifecycle input/cell')
                    return ast.copy_location(ast.Name(id=fields[node.attr], ctx=copy.deepcopy(node.ctx)), node)
                return self.generic_visit(node)
        ProjectCells().visit(function)
        forbidden = set(layouts) | {'lifecycle'}
        if any(isinstance(node, ast.Name) and node.id in forbidden for node in ast.walk(function)):
            raise CompileError('lifecycle transaction use outside declared actual fragments')
    if used_helpers != set(helpers): raise CompileError('a supplied lifecycle algorithm would be ignored')
    if not stride_nodes: raise CompileError('actual operator-register stride was not consumed')
    excluded = {'contexts_lifecycle.py', *target.LIFECYCLE_MODULE_FUNCTIONS}
    return {name: tree for name, tree in trees.items() if name not in excluded}, stride_nodes


def _normalize_command_domains(trees):
    """Consume all actual command owners and shared live transactions.

    Only declared data cells, alpha-renaming and finite service-call fragments
    are normalized. Every supplied effect, condition, call, policy and return
    then participates in the complete audio contract. Saved bodies are never
    inserted; caller-result projection comes from its supplied actual boundary.
    """
    sequence = trees['business_sequence.py']
    contexts = trees['contexts_commands.py']
    services = trees['business_commands_services.py']
    entries = target.COMMAND_ENTRY_LAYOUT
    cells = target.COMMAND_CONTEXT_FIELDS
    service_layout = target.COMMAND_SERVICE_LAYOUT
    context_import = _declaration_import('contexts_commands', tuple(cells))
    imports = [context_import]
    for owner, public_names in target.COMMAND_MODULE_ENTRIES.items():
        imports.append(_declaration_import(owner[:-3], tuple(entries[name]['algorithm'] for name in public_names)))
    if len(sequence.body) < 5 + len(imports) or any(_stable_ast_dump(actual) != _stable_ast_dump(expected)
            for actual, expected in zip(sequence.body[5:5 + len(imports)], imports)):
        raise CompileError('complete command entry imports must point to actual owners')
    del sequence.body[5:5 + len(imports)]
    if len(contexts.body) != 3 + len(cells):
        raise CompileError('complete command live-context declarations required')
    _bounded_domain_doc(contexts.body[0])
    expected_imports = (ast.ImportFrom(module='dataclasses', names=[ast.alias(name='dataclass')], level=0),
                        _declaration_import('domain', ('Byte', 'Word')))
    if any(_stable_ast_dump(actual) != _stable_ast_dump(expected)
            for actual, expected in zip(contexts.body[1:3], expected_imports)):
        raise CompileError('command context imports differ')
    for actual, (name, fields) in zip(contexts.body[3:], cells.items()):
        if not isinstance(actual, ast.ClassDef) or actual.name != name or not actual.body:
            raise CompileError('command context ownership differs')
        _bounded_domain_doc(actual.body[0])
        text = '@dataclass(slots=True)\nclass ' + name + ':\n    "Context."\n'
        text += ''.join('    ' + field + ': ' + ('Byte' if old in ('conditions', 'sample') else 'Word') + '\n'
                        for field, old in fields.items())
        expected = ast.parse(text).body[0]
        checked = copy.deepcopy(actual)
        checked.body[0] = copy.deepcopy(expected.body[0])
        if _stable_ast_dump(checked) != _stable_ast_dump(expected):
            raise CompileError('command contexts cannot hide methods, extra cells or defaults')
    domain_import = sequence.body[1]
    algorithms, service_functions = {}, {}

    def validate_function(actual, name, context):
        expected = ast.parse('def ' + name + '(state: AudioState, command: ' + context +
                             ', continuation: Continuation) -> None:\n    pass\n').body[0]
        if (not isinstance(actual, ast.FunctionDef) or actual.name != name or actual.decorator_list
                or getattr(actual, 'type_params', []) or len(actual.body) < 2
                or _stable_ast_dump(actual.args) != _stable_ast_dump(expected.args)
                or _stable_ast_dump(actual.returns) != _stable_ast_dump(expected.returns)):
            raise CompileError('unsupported command-domain signature or ownership')
        _bounded_domain_doc(actual.body[0])

    if len(services.body) != 3 + len(service_layout):
        raise CompileError('complete shared command transactions required')
    _bounded_domain_doc(services.body[0])
    if (_stable_ast_dump(services.body[1]) != _stable_ast_dump(domain_import)
            or _stable_ast_dump(services.body[2]) != _stable_ast_dump(context_import)):
        raise CompileError('shared command transaction imports differ')
    for node, (name, layout) in zip(services.body[3:], service_layout.items()):
        validate_function(node, name, layout['context'])
        service_functions[name] = node
    for owner, public_names in target.COMMAND_MODULE_ENTRIES.items():
        tree = trees[owner]
        expected_contexts = tuple(dict.fromkeys(entries[name]['context'] for name in public_names))
        expected_services = tuple(dict.fromkeys(row['service'] for name in public_names
                                                for row in target.COMMAND_CALL_BINDINGS.get(name, [])))
        header = [domain_import, _declaration_import('contexts_commands', expected_contexts)]
        if expected_services:
            header.append(_declaration_import('business_commands_services', expected_services))
        if len(tree.body) != 1 + len(header) + len(public_names):
            raise CompileError(owner + ': complete sole command owner required')
        _bounded_domain_doc(tree.body[0])
        if any(_stable_ast_dump(actual) != _stable_ast_dump(expected)
                for actual, expected in zip(tree.body[1:1 + len(header)], header)):
            raise CompileError(owner + ': declared owner imports differ')
        for actual, public_name in zip(tree.body[1 + len(header):], public_names):
            layout = entries[public_name]
            validate_function(actual, layout['algorithm'], layout['context'])
            algorithms[public_name] = actual
    if set(algorithms) != set(entries):
        raise CompileError('complete unique thirty-one command implementations required')
    used_services = set()
    expected_service_call = ast.parse('service(state, command, continuation)').body[0].value
    for public_name, layout in entries.items():
        candidates = [node for node in sequence.body if isinstance(node, ast.FunctionDef) and node.name == public_name]
        if len(candidates) != 1:
            raise CompileError('public command boundary missing or ambiguous')
        function = candidates[0]
        fields = layout['fields']
        construction = ast.parse('command = ' + layout['context'] + '(' +
            ', '.join(field + '=inputs.' + old for field, old in fields.items()) + ')').body[0]
        invocation = ast.parse(layout['algorithm'] + '(state, command, inputs.continuation)').body[0]
        if (len(function.body) != 7 or _stable_ast_dump(function.body[4]) != _stable_ast_dump(construction)
                or _stable_ast_dump(function.body[5]) != _stable_ast_dump(invocation)
                or not isinstance(function.body[6], ast.Return)):
            raise CompileError('command boundary must transfer all and only its declared real inputs')
        result_boundary = copy.deepcopy(function.body[6])
        binding_rows = target.COMMAND_CALL_BINDINGS.get(public_name, [])
        binding_index = 0

        class Alpha(ast.NodeTransformer):
            def __init__(self, renames): self.renames = renames
            def visit_Name(self, node):
                if node.id == 'continuation':
                    return ast.copy_location(ast.Attribute(value=ast.Name(id='inputs', ctx=ast.Load()),
                        attr='continuation', ctx=ast.Load()), node)
                if node.id in self.renames: node.id = self.renames[node.id]
                return node

        def expand(statements, active=()):
            nonlocal binding_index
            expanded = []
            for statement in statements:
                if (isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call)
                        and isinstance(statement.value.func, ast.Name) and statement.value.func.id in service_functions):
                    call = statement.value
                    name = call.func.id
                    expected = copy.deepcopy(expected_service_call)
                    expected.func.id = name
                    # Root alpha projection has already bound its continuation.
                    expected.args[-1] = ast.Attribute(value=ast.Name(id='inputs', ctx=ast.Load()), attr='continuation', ctx=ast.Load())
                    if (_stable_ast_dump(call) != _stable_ast_dump(expected) or name in active
                            or binding_index >= len(binding_rows) or binding_rows[binding_index]['service'] != name):
                        raise CompileError('unsupported command service routing, live binding or recursion')
                    row = binding_rows[binding_index]
                    binding_index += 1
                    used_services.add(name)
                    renames = {readable: row['temporary_aliases'].get(canonical, canonical)
                               for readable, canonical in service_layout[name]['temporaries'].items()}
                    supplied = [Alpha(renames).visit(copy.deepcopy(item)) for item in service_functions[name].body[1:]]
                    expanded.extend(expand(supplied, (*active, name)))
                    continue
                if isinstance(statement, ast.Return):
                    if statement.value is not None:
                        raise CompileError('command fragments cannot fabricate a new result value')
                    expanded.append(copy.deepcopy(result_boundary))
                    continue
                for field, value in ast.iter_fields(statement):
                    if isinstance(value, list) and value and all(isinstance(part, ast.stmt) for part in value):
                        setattr(statement, field, expand(value, active))
                expanded.append(statement)
            return expanded

        supplied = [Alpha(layout['temporaries']).visit(copy.deepcopy(statement))
                    for statement in algorithms[public_name].body[1:]]
        supplied = expand(supplied)
        if binding_index != len(binding_rows):
            raise CompileError('a declared shared command transaction would be ignored')
        initialization = [ast.parse(old + ' = inputs.' + old).body[0] for old in fields.values()]
        function.body[4:] = initialization + supplied

        class ProjectCells(ast.NodeTransformer):
            def visit_Attribute(self, node):
                if isinstance(node.value, ast.Name) and node.value.id == 'command':
                    if node.attr not in fields: raise CompileError('access to absent command input/cell')
                    return ast.copy_location(ast.Name(id=fields[node.attr], ctx=copy.deepcopy(node.ctx)), node)
                return self.generic_visit(node)
        ProjectCells().visit(function)
        forbidden = set(service_functions) | {row['algorithm'] for row in entries.values()} | {'command'}
        if any(isinstance(node, ast.Name) and node.id in forbidden for node in ast.walk(function)):
            raise CompileError('command transaction use outside declared actual fragments')
    if used_services != set(service_functions):
        raise CompileError('a supplied shared command algorithm would be ignored')
    excluded = {'contexts_commands.py', 'business_commands_services.py', *target.COMMAND_MODULE_ENTRIES}
    return {name: tree for name, tree in trees.items() if name not in excluded}


def _normalize_sequence_domains(trees):
    """Project supplied live transactions onto the finite original target ABI.

    All eleven actual domain bodies are expanded and subsequently admitted as
    part of the complete audio AST. No old body or target AST is substituted.
    Only explicit data-cell projection, declared temporary alpha-renaming and
    these fixed, nonrecursive fragment calls are supported. Native field/FM
    service calls, their stacks and all returned aliases remain real clauses.
    """
    contexts = trees['contexts_sequence.py']
    domain = trees['business_sequence_control.py']
    sequence = trees['business_sequence.py']
    fields = target.SEQUENCE_CONTEXT_FIELDS
    entries = target.SEQUENCE_DOMAIN_ENTRIES
    helpers = target.SEQUENCE_DOMAIN_HELPERS
    context_import = _declaration_import('contexts_sequence', tuple(fields))
    domain_import = _declaration_import('business_sequence_control',
                                        tuple(entry[1] for entry in entries.values()))
    if len(contexts.body) != 3 + len(fields):
        raise CompileError('sequence contexts must contain only declared live data cells')
    _bounded_domain_doc(contexts.body[0])
    expected_imports = (ast.ImportFrom(module='dataclasses',
                        names=[ast.alias(name='dataclass')], level=0),
                        _declaration_import('domain', ('Byte', 'Word')))
    if any(_stable_ast_dump(actual) != _stable_ast_dump(expected)
           for actual, expected in zip(contexts.body[1:3], expected_imports)):
        raise CompileError('sequence context data imports differ')
    for actual, (name, cells) in zip(contexts.body[3:], fields.items()):
        if not isinstance(actual, ast.ClassDef) or actual.name != name or not actual.body:
            raise CompileError('sequence context declaration or ownership differs')
        _bounded_domain_doc(actual.body[0])
        declaration = '@dataclass(slots=True)\nclass ' + name + ':\n    "Context."\n'
        declaration += ''.join('    ' + cell + ': ' +
            ('Byte' if old in ('conditions', 'sample') else 'Word') + '\n'
            for cell, old in cells.items())
        expected = ast.parse(declaration).body[0]
        checked = copy.deepcopy(actual)
        checked.body[0] = copy.deepcopy(expected.body[0])
        if _stable_ast_dump(checked) != _stable_ast_dump(expected):
            raise CompileError('sequence contexts cannot hide algorithms, defaults or extra cells')
    if len(domain.body) != 3 + len(helpers):
        raise CompileError('complete uniquely owned sequence domain required')
    _bounded_domain_doc(domain.body[0])
    imports = (_declaration_import('domain', ('AudioState', 'Continuation', 'u8', 'u16',
        'low', 'high', 'replace_low', 'replace_high', 'logic_conditions', 'sum_byte', 'sum_word', 'decrement_byte', 'increment_byte')),
        context_import)
    if any(_stable_ast_dump(actual) != _stable_ast_dump(expected)
           for actual, expected in zip(domain.body[1:3], imports)):
        raise CompileError('sequence domain imports differ')
    algorithms = {}
    for actual, (name, parameters) in zip(domain.body[3:], helpers.items()):
        signature = 'def ' + name + '(state: AudioState, ' + parameters[0] + ': ' + parameters[1]
        if len(parameters) == 4:
            signature += ', ' + parameters[2] + ': ' + parameters[3]
        expected = ast.parse(signature + ') -> None:\n    pass\n').body[0]
        if (not isinstance(actual, ast.FunctionDef) or actual.name != name or
                actual.decorator_list or getattr(actual, 'type_params', []) or
                _stable_ast_dump(actual.args) != _stable_ast_dump(expected.args) or
                _stable_ast_dump(actual.returns) != _stable_ast_dump(expected.returns) or
                len(actual.body) < 2):
            raise CompileError('unsupported sequence domain function/signature')
        _bounded_domain_doc(actual.body[0])
        algorithms[name] = actual
    if len(sequence.body) < 5 or any(_stable_ast_dump(actual) != _stable_ast_dump(expected)
            for actual, expected in zip(sequence.body[3:5], (context_import, domain_import))):
        raise CompileError('sequence entry imports must point to the actual domain owners')
    del sequence.body[3:5]
    temporary_names = {
        'jump_sequence_pointer': {'target_low': 'observed_byte_1', 'target_high': 'observed_byte_2'},
        'call_sequence_subroutine': {'target_high_byte': 'observed_byte_1', 'channel_base': 'saved_audio_word_2',
            'first_slot': 'observed_byte_3', 'lower_slot': 'changed_byte_4', 'live_slot': 'observed_byte_5',
            'second_slot': 'observed_byte_6', 'next_slot': 'changed_byte_7', 'return_address': 'arithmetic_result_8',
            'call_target': 'saved_audio_word_9'},
        'return_sequence_subroutine': {'channel_base': 'saved_audio_word_1', 'slot': 'observed_byte_2',
            'saved_address': 'arithmetic_result_3', 'return_low': 'observed_byte_4', 'return_high': 'observed_byte_5',
            'first_slot': 'observed_byte_6', 'higher_slot': 'changed_byte_7', 'second_slot': 'observed_byte_8',
            'next_slot': 'changed_byte_9'},
        'repeat_sequence_section': {'counter_offset': 'arithmetic_result_1', 'channel_base': 'saved_audio_word_2',
            'counter_address': 'arithmetic_result_3', 'live_count': 'observed_byte_4', 'initial_count': 'observed_byte_5',
            'live_counter': 'observed_byte_6', 'remaining': 'changed_byte_7', 'target_low': 'observed_byte_8',
            'target_high': 'observed_byte_9'},
        'read_register_parameter_pair': {'register_selector': 'observed_byte_1', 'field_value': 'observed_byte_2'},
        'write_sequence_channel_register': {'parameter_outcome': 'updated_audio_values_1', 'hardware_outcome': 'updated_audio_values_2'},
        'write_sequence_port_zero_register': {'parameter_outcome': 'updated_audio_values_1', 'hardware_outcome': 'updated_audio_values_2'},
    }
    used = set()

    def expand_call(call, caller, active):
        name = call.func.id
        if name in active:
            raise CompileError('recursive sequence fragments are unsupported')
        function = algorithms[name]
        parameters = [arg.arg for arg in function.args.args]
        if call.keywords or len(call.args) != len(parameters):
            raise CompileError('sequence fragments require all explicit positional live values')
        used.add(name)
        bindings = dict(zip(parameters, call.args))
        renames = dict(temporary_names[caller])
        if name == 'call_register_parameter_service':
            address = bindings['return_address']
            expected = {'write_sequence_channel_register': 3244, 'write_sequence_port_zero_register': 3249}.get(caller)
            if not isinstance(address, ast.Constant) or type(address.value) is not int or address.value != expected:
                raise CompileError('unsupported original register-parameter continuation')

        class BindFragment(ast.NodeTransformer):
            def visit_Name(self, node):
                if node.id in bindings:
                    bound = copy.deepcopy(bindings[node.id])
                    if isinstance(bound, ast.Name):
                        bound.ctx = copy.deepcopy(node.ctx)
                    return ast.copy_location(bound, node)
                if node.id in renames:
                    node.id = renames[node.id]
                return node

        statements = [BindFragment().visit(copy.deepcopy(statement)) for statement in function.body[1:]]
        return expand_statements(statements, caller, (*active, name))

    def expand_statements(statements, caller, active):
        result = []
        for statement in statements:
            if (isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call)
                    and isinstance(statement.value.func, ast.Name) and statement.value.func.id in algorithms):
                result.extend(expand_call(statement.value, caller, active))
                continue
            for field, value in ast.iter_fields(statement):
                if isinstance(value, list) and value and all(isinstance(item, ast.stmt) for item in value):
                    setattr(statement, field, expand_statements(value, caller, active))
            result.append(statement)
        return result

    for caller, (context_type, algorithm) in entries.items():
        candidates = [node for node in sequence.body if isinstance(node, ast.FunctionDef) and node.name == caller]
        if len(candidates) != 1:
            raise CompileError('sequence entry missing or ambiguous')
        function = candidates[0]
        variable = helpers[algorithm][0]
        cells = fields[context_type]
        construction = ast.parse(variable + ' = ' + context_type + '(' +
            ', '.join(cell + '=inputs.' + old for cell, old in cells.items()) + ')').body[0]
        invocation = algorithm + '(state, ' + variable
        if len(helpers[algorithm]) == 4:
            invocation += ', inputs.continuation'
        expected_call = ast.parse(invocation + ')').body[0]
        if (len(function.body) < 7 or _stable_ast_dump(function.body[4]) != _stable_ast_dump(construction)
                or _stable_ast_dump(function.body[5]) != _stable_ast_dump(expected_call)):
            raise CompileError('sequence entry must bind and transfer every declared live input')
        initialization = [ast.parse(old + ' = inputs.' + old).body[0] for old in cells.values()]
        supplied = expand_call(function.body[5].value, caller, ())
        if caller == 'repeat_sequence_section':
            # The supplied domain returns after either terminal branch. Its
            # one public result boundary is projected into both original exits;
            # no effect/return from a saved old body is inserted or replayed.
            if (len(function.body[6:]) != 1 or not isinstance(function.body[6], ast.Return)
                    or not supplied or not isinstance(supplied[-1], ast.If)
                    or not supplied[-1].body or not supplied[-1].orelse
                    or any(isinstance(node, ast.Return) for item in supplied for node in ast.walk(item))):
                raise CompileError('repeat requires exactly two terminal live-result branches')
            supplied[-1].body.append(copy.deepcopy(function.body[6]))
            supplied[-1].orelse.append(copy.deepcopy(function.body[6]))
            function.body[4:] = initialization + supplied
        else:
            function.body[4:6] = initialization + supplied

        class ProjectCells(ast.NodeTransformer):
            def visit_Attribute(self, node):
                if isinstance(node.value, ast.Name) and node.value.id == variable:
                    if node.attr not in cells:
                        raise CompileError('undeclared sequence transaction cell')
                    return ast.copy_location(ast.Name(id=cells[node.attr], ctx=copy.deepcopy(node.ctx)), node)
                return self.generic_visit(node)

        ProjectCells().visit(function)
        if any(isinstance(node, ast.Name) and (node.id == variable or node.id in algorithms)
               for node in ast.walk(function)):
            raise CompileError('sequence transaction/helper use outside the declared finite fragments')
    if used != set(algorithms):
        raise CompileError('an owned sequence algorithm would be ignored during generation')
    return {name: tree for name, tree in trees.items()
            if name not in ('contexts_sequence.py', 'business_sequence_control.py')}


def _normalize_channel_domains(trees):
    """Bind the old address schedule to supplied, uniquely owned functions.

    No function body comes from the compatibility module or a saved AST dump.
    The five new source trees own the actual algorithms. Their exact imports,
    signatures/order and all statements participate in admission; only inert
    module documentation and declared import routing are normalized. Reusing
    the old semantic address namespace does not create a second implementation.
    """
    layout = channel_layout
    wrapper = trees['business_channels.py']
    _bounded_domain_doc(wrapper.body[0] if wrapper.body else None)
    expected_exports = [_declaration_import(name[:-3], functions)
                        for name, functions in layout.MODULE_FUNCTIONS.items()]
    if ([_stable_ast_dump(node) for node in wrapper.body[1:]] !=
            [_stable_ast_dump(node) for node in expected_exports]):
        raise CompileError('channels must contain only exact compatibility re-exports')
    functions = {}
    for name, owned in layout.MODULE_FUNCTIONS.items():
        tree = trees[name]
        if len(tree.body) != 3 + len(owned):
            raise CompileError(name + ': complete sole domain implementation required')
        _bounded_domain_doc(tree.body[0])
        imports = (_declaration_import('domain', layout.DOMAIN_IMPORTS[name]),
                   _declaration_import('contexts', layout.CONTEXT_IMPORTS[name]))
        if any(_stable_ast_dump(actual) != _stable_ast_dump(expected)
               for actual, expected in zip(tree.body[1:3], imports)):
            raise CompileError(name + ': explicit domain/type imports differ')
        for node, expected in zip(tree.body[3:], owned):
            if not isinstance(node, ast.FunctionDef) or node.name != expected or expected in functions:
                raise CompileError(name + ': function ownership or order differs')
            functions[expected] = node
    if set(functions) != set(layout.CHANNEL_FUNCTION_OWNERS):
        raise CompileError('complete unique channel function ownership required')
    owner_stems = {name[:-3] for name in layout.MODULE_FUNCTIONS}
    for name, tree in trees.items():
        if name == 'business_channels.py':
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == 'business_channels':
                raise CompileError('algorithm calls must import the direct domain owner')
            if isinstance(node, ast.ImportFrom) and node.module in owner_stems:
                if (node.level != 1 or any(alias.asname is not None or
                        layout.CHANNEL_FUNCTION_OWNERS.get(alias.name) != node.module + '.py'
                        for alias in node.names)):
                    raise CompileError('cross-domain function import has the wrong owner')
                node.module = 'business_channels'
    canonical_channels = ast.Module(body=[
        ast.Expr(value=ast.Constant(value=layout.LEGACY_MODULE_DOCSTRING)),
        _declaration_import('domain', layout.LEGACY_DOMAIN_IMPORTS),
        _declaration_import('contexts', layout.LEGACY_CONTEXT_IMPORTS),
        *(functions[name] for name in layout.LEGACY_CHANNEL_FUNCTIONS),
    ], type_ignores=[])
    # This editable literal is in the supplied pitch algorithm, not target data.
    pitch_initial_high = _node(functions['calculate_channel_pitch'],
                               ['body', 11, 'value', 'args', 1])
    if not isinstance(pitch_initial_high, ast.Constant):
        raise CompileError('pitch initial high field must remain a literal byte')
    _strict_integer(pitch_initial_high.value, 0, 255, 'pitch initial high field')
    canonical = {name: tree for name, tree in trees.items()
                 if name not in layout.MODULE_FUNCTIONS}
    canonical['business_channels.py'] = canonical_channels
    return canonical, pitch_initial_high


def _admit(sources):
    if not isinstance(sources, Mapping):
        raise CompileError('explicit business-module-to-source mapping required')
    if (any(type(key) is not str for key in sources) or
            set(sources) != set(target.BUSINESS_MODULES)):
        raise CompileError('all declared explicit logical business sources are required')
    if not hasattr(target, 'SOURCE_TREES'):
        raise CompileError('the complete semantic-node schedule is not installed yet')
    trees = {}
    for name in target.BUSINESS_MODULES:
        source = sources[name]
        if type(source) is not str or not 1 <= len(source) <= MAX_SOURCE_CHARACTERS:
            raise CompileError('bounded source text, never a path or byte payload, required')
        try:
            trees[name] = ast.parse(source, filename=name, mode='exec')
        except (SyntaxError, ValueError, RecursionError) as error:
            raise CompileError('unsupported or malformed Python source') from error
    trees, operator_strides = _normalize_lifecycle_domains(trees)
    trees = _normalize_command_domains(trees)
    trees = _normalize_sequence_domains(trees)
    trees = _normalize_voice_domains(trees)
    trees, pitch_initial_high = _normalize_channel_domains(trees)
    level_masks = _normalize_level_helper(trees['business_voice.py'])
    repeat_site = next(site for site in target.OPERATION_SITES
                       if site['unit'] == 'driver' and site['address'] == 0x0EEF)
    repeat_bindings = [operand['value_source'] for operand in repeat_site['operands'] if 'value_source' in operand]
    if len(repeat_bindings) != 1 or repeat_bindings[0]['source'] != 'business_sequence.py':
        raise CompileError('one actual repeat-counter base binding required')
    repeat_base = _node(trees['business_sequence.py'], repeat_bindings[0]['path'])
    if not isinstance(repeat_base, ast.Constant):
        raise CompileError('repeat counter base must remain a literal BYTE')
    repeat_value = _strict_integer(repeat_base.value, 0, 255, 'repeat counter base')
    pan_site = next(site for site in target.OPERATION_SITES if site['unit'] == 'driver' and site['address'] == 0x0D70)
    pan_bindings = [operand['value_source'] for operand in pan_site['operands'] if 'value_source' in operand]
    if len(pan_bindings) != 1 or pan_bindings[0]['source'] != 'business_sequence.py':
        raise CompileError('one actual stereo retained-bits BYTE rule required')
    pan_mask = _node(trees['business_sequence.py'], pan_bindings[0]['path'])
    if not isinstance(pan_mask, ast.Constant):
        raise CompileError('stereo retained-bits rule must be a literal BYTE')
    pan_value = _strict_integer(pan_mask.value, 0, 255, 'stereo retained-bits rule')
    slot = target.EDITABLE_SLOT
    slot_node = _node(trees[slot['source_key']], slot['AST_path'])
    if not isinstance(slot_node, ast.Constant):
        raise CompileError('instrument-field count must remain a literal integer')
    value = _strict_integer(slot_node.value, slot.get('minimum', 1), slot.get('maximum', 255),
                            'instrument-field count')
    canonical = slot.get('canonical', 20)
    # These genuinely consumed count/mask/pitch/repeat-base slots are editable.
    # Every other expression, return, import, condition, call and input binding
    # participates in the full AST contract; none can be silently ignored.
    slot_node.value = canonical
    repeat_base.value = 40
    pan_mask.value = 63
    stride_values = [node.value for node in operator_strides]
    for node in operator_strides:
        node.value = 4
    mask_values = [node.value for node in level_masks]
    for node in level_masks:
        node.value = 127
    pitch_value = pitch_initial_high.value
    pitch_initial_high.value = 0
    try:
        for name, tree in trees.items():
            if _stable_ast_dump(tree) != target.SOURCE_TREES[name]:
                raise CompileError(name + ': unsupported logical-source change')
        for site in target.OPERATION_SITES:
            clause = _node(trees[site['source']], site['path'])
            if _stable_ast_dump(clause) != site['node']:
                raise CompileError('an operation no longer matches its semantic clause')
    finally:
        slot_node.value = value
        repeat_base.value = repeat_value
        pan_mask.value = pan_value
        for node, original in zip(operator_strides, stride_values):
            node.value = original
        for node, original in zip(level_masks, mask_values):
            node.value = original
        pitch_initial_high.value = pitch_value
    return trees, value


def _operand(operand, *, relative=False, unit='driver'):
    """Format admitted typed target storage, not a saved assembly string."""
    if type(operand) is not dict or type(operand.get('kind')) is not str:
        raise CompileError('typed target storage required')
    kind = operand['kind']
    if kind == 'register':
        name = operand['name']
        if name not in ('a', 'b', 'c', 'd', 'e', 'h', 'l', 'i', 'r',
                        'af', 'af_alt', 'bc', 'de', 'hl', 'sp', 'ix', 'iy'):
            raise CompileError('unsupported target register placement')
        return "af'" if name == 'af_alt' else name
    if kind == 'immediate':
        width = operand['width']
        if width not in (3, 8, 16):
            raise CompileError('unsupported fixed target immediate width')
        value = _strict_integer(operand['value'], 0, (1 << width) - 1, 'target literal')
        return str(value) if width == 3 else '$' + format(value, '02x' if width == 8 else '04x')
    if kind == 'target':
        address = _strict_integer(operand['address'], 0, 0xFFFF, 'control target')
        if relative:
            return ('z80_' if unit == 'driver' else 'boot_z80_') + format(address, '04x')
        return '$' + format(address, '04x')
    if kind == 'indirect_target':
        if operand['register'] not in ('hl', 'ix', 'iy'):
            raise CompileError('unsupported indirect target placement')
        return '(' + operand['register'] + ')'
    if kind != 'memory' or type(operand.get('EA')) is not dict:
        raise CompileError('unsupported target storage kind')
    ea = operand['EA']
    mode = ea['mode']
    if mode == 'absolute':
        address = _strict_integer(ea['address'], 0, 0xFFFF, 'absolute bus address')
        return '($' + format(address, '04x') + ')'
    if mode == 'register_indirect':
        if ea['base'] not in ('bc', 'de', 'hl'):
            raise CompileError('unsupported indirect data placement')
        return '(' + ea['base'] + ')'
    if mode == 'indexed':
        if ea['base'] not in ('ix', 'iy'):
            raise CompileError('unsupported indexed data placement')
        displacement = _strict_integer(ea['displacement'], -128, 127, 'signed channel offset')
        return '(' + ea['base'] + ('+' if displacement >= 0 else '-') + '$' + format(abs(displacement), '02x') + ')'
    raise CompileError('unsupported effective address')


def _literal_expression(node):
    """Evaluate only a literal fixed-width business expression, never Python."""
    if isinstance(node, ast.Constant) and type(node.value) is int:
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd, ast.Invert)):
        value = _literal_expression(node.operand)
        return -value if isinstance(node.op, ast.USub) else +value if isinstance(node.op, ast.UAdd) else ~value
    if isinstance(node, ast.BinOp):
        left, right = _literal_expression(node.left), _literal_expression(node.right)
        operations = {ast.Add: lambda: left + right, ast.Sub: lambda: left - right,
                      ast.Mult: lambda: left * right, ast.BitOr: lambda: left | right,
                      ast.BitAnd: lambda: left & right, ast.BitXor: lambda: left ^ right,
                      ast.LShift: lambda: left << right, ast.RShift: lambda: left >> right}
        if type(node.op) in operations:
            return operations[type(node.op)]()
    raise CompileError('target data must be read from a bound literal business expression')


def _source_value(binding, trees):
    node = _node(trees[binding['source']], binding['path'])
    if binding.get('bare_channel_offset'):
        while isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'u16' and len(node.args) == 1:
            node = node.args[0]
        if isinstance(node, ast.Name):
            value = 0
        elif isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub)):
            value = _literal_expression(node.right) * (-1 if isinstance(node.op, ast.Sub) else 1)
        else:
            raise CompileError('the live channel-relative address is not supported')
    else:
        value = _literal_expression(node)
        if binding.get('negated'):
            value = -value
        if binding.get('bit_mask_transform'):
            mask = value if binding['bit_mask_transform'] == 'set_bit_mask' else ~value & 0xFF
            if not 1 <= mask <= 0x80 or mask & (mask - 1):
                raise CompileError('a channel-bit action must supply exactly one actual BYTE mask')
            value = mask.bit_length() - 1
    width = binding['width']
    if binding.get('signed'):
        return _strict_integer(value, -(1 << (width - 1)), (1 << (width - 1)) - 1, 'source channel offset')
    return value & ((1 << width) - 1)


def _source_operand(operand, trees):
    """Resolve all data constants and called functions from the actual AST."""
    result = dict(operand)
    if 'value_source' in result:
        result['value'] = _source_value(result.pop('value_source'), trees)
    if 'callee_source' in result:
        binding = result.pop('callee_source')
        node = _node(trees[binding['source']], binding['path'])
        if not isinstance(node, ast.Name) or node.id not in target.CALLEE_ADDRESSES:
            raise CompileError('explicit named business callee required')
        result['address'] = target.CALLEE_ADDRESSES[node.id]
    if result['kind'] == 'memory':
        ea = result['EA'] = dict(result['EA'])
        if 'address_source' in ea:
            ea['address'] = _source_value(ea.pop('address_source'), trees)
        if 'displacement_source' in ea:
            ea['displacement'] = _source_value(ea.pop('displacement_source'), trees)
    return result


def _effect_expression(clause):
    if isinstance(clause, (ast.If, ast.While)):
        return clause.test
    if isinstance(clause, (ast.Assign, ast.AnnAssign, ast.Return, ast.Expr)):
        return clause.value
    return clause


def _condition_code(node):
    inverse = {'z': 'nz', 'nz': 'z', 'c': 'nc', 'nc': 'c', 'm': 'p', 'p': 'm', 'pe': 'po', 'po': 'pe'}
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        code = _condition_code(node.operand)
        return inverse[code]
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'bool' and len(node.args) == 1:
        return _condition_code(node.args[0])
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitAnd) and isinstance(node.left, ast.Name) and node.left.id == 'conditions':
        code = {0x40: 'z', 1: 'c', 0x80: 'm', 4: 'pe'}.get(_literal_expression(node.right))
        if code is not None:
            return code
    raise CompileError('the source condition is not an admitted finite outcome test')


def _semantic_operator(site, clause, trees):
    """Check expression/effect compatibility before using ABI encoding hints."""
    hinted = site['operator']
    clauses = [_node(trees[site['source']], path) for path in site.get('paths', [site['path']])]
    expressions = [_effect_expression(one) for one in clauses]
    calls = {node.func.id for expression in expressions for node in ast.walk(expression)
             if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    arithmetic_helpers = {
        'sum_byte': 'ADD', 'sum_word': 'ADD', 'difference_word': 'SBC',
        'comparison_conditions': 'CP', 'tested_bit_conditions': 'BIT',
        'increment_byte': 'INC', 'decrement_byte': 'DEC',
    }
    selected = {arithmetic_helpers[name] for name in calls if name in arithmetic_helpers}
    # A clause can contain a result and its flag update; only a compatible
    # native effect may consume it. Storage/register allocation remains bound.
    if selected and hinted not in selected and hinted not in ('LD', 'SUB', 'NEG', 'JUMP', 'RET', 'DJNZ', 'CALL', 'RST'):
        raise CompileError('source arithmetic helper and target effect disagree')
    if hinted in ('DI', 'EI'):
        controls = [node for expression in expressions for node in ast.walk(expression) if isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute) and node.func.attr == 'interrupt_control']
        if len(controls) != 1 or not controls[0].args or not isinstance(controls[0].args[0], ast.Constant) or type(controls[0].args[0].value) is not bool:
            raise CompileError('explicit interrupt-control semantic action required')
        return 'EI' if controls[0].args[0].value else 'DI'
    if hinted == 'NOP' and not isinstance(clause, (ast.Pass, ast.Expr)):
        raise CompileError('explicit timing-only semantic clause required')
    if hinted in ('CALL', 'RST') and not any(isinstance(node, ast.Call) for expression in expressions for node in ast.walk(expression)):
        raise CompileError('the native call must consume an actual business call')
    if hinted in ('JUMP', 'DJNZ') and not isinstance(clause, (ast.If, ast.While, ast.Break, ast.Continue, ast.Expr, ast.Assign, ast.Return, ast.Pass)):
        raise CompileError('explicit logical control clause required')
    return hinted


def _ordinary_instruction(site, clause, trees):
    """Select one ordinary operation from its consumed logical AST clause.

The finite lowering schedule supplies compatibility storage and encoding
choices. It is not an array of precompiled bytes or a full assembly string;
the source AST, including every condition/call/return, is admitted above and
each instruction here is tied to an explicit actual clause and effect.
"""
    if not isinstance(clause, ast.AST) or type(site.get('effect')) is not str:
        raise CompileError('actual semantic source clause and effect are required')
    operation = _semantic_operator(site, clause, trees)
    allowed = {'LD', 'LDI', 'LDIR', 'INC', 'DEC', 'ADD', 'SUB', 'SBC', 'AND', 'OR', 'XOR', 'CP',
               'BIT', 'SET', 'RES', 'SRL', 'SRA', 'RR', 'RLCA', 'RRCA', 'NEG', 'EX', 'EXX',
               'PUSH', 'POP', 'JUMP', 'DJNZ', 'CALL', 'RST', 'RET', 'DI', 'EI', 'IM', 'NOP'}
    if operation not in allowed:
        raise CompileError('unsupported ordinary Z80 selection')
    operands = [_source_operand(operand, trees) for operand in site['operands']]
    encoding = site['encoding']
    if operation == 'JUMP':
        mnemonic = 'jr' if encoding == 'relative8' else 'jp'
    else:
        mnemonic = operation.lower()
    if operation in ('AND', 'OR', 'XOR', 'SUB', 'CP'):
        if operands[0] != {'kind': 'register', 'name': 'a', 'width': 8}:
            raise CompileError('implicit accumulator selection differs')
        operands = operands[1:]
    if operation == 'IM':
        return mnemonic + ' ' + str(operands[0]['value'])
    values = [_operand(operand, relative=encoding == 'relative8', unit=site['unit']) for operand in operands]
    binding = site.get('condition_source')
    condition = None
    if binding is not None:
        condition = _condition_code(_node(trees[binding['source']], binding['path']))
        if binding['inverted']:
            condition = {'z': 'nz', 'nz': 'z', 'c': 'nc', 'nc': 'c', 'm': 'p', 'p': 'm', 'pe': 'po', 'po': 'pe'}[condition]
    elif site['condition'] is not None:
        raise CompileError('target conditions cannot fall back to stored flags')
    if condition is not None:
        if condition not in ('nz', 'z', 'nc', 'c', 'po', 'pe', 'p', 'm'):
            raise CompileError('unsupported source-condition placement')
        values.insert(0, condition)
    return mnemonic + (' ' + ','.join(values) if values else '')


def generate(sources: Mapping[str, str]) -> dict[str, str]:
    """Pure explicit-source lowering to two separate native code images."""
    trees, instrument_count = _admit(sources)
    result = {}
    for unit in ('driver', 'startup'):
        rows = target.UNITS[unit]['rows']
        prefix = 'z80_' if unit == 'driver' else 'boot_z80_'
        entry = '_start' if unit == 'driver' else '_boot_start'
        sites = [site for site in target.OPERATION_SITES if site['unit'] == unit]
        if [(site['address']) for site in sites] != [row['address'] for row in rows]:
            raise CompileError('semantic operation coverage differs from complete explicit layout')
        lines = ['; Finite logical-AST lowering; no source bytes, runtime IR or old assembly input.',
                 '.text', entry + ':']
        for row, site in zip(rows, sites):
            clause = _node(trees[site['source']], site['path'])
            label = prefix + format(row['address'], '04x')
            lines.extend(['.org 0x' + format(row['address'], 'x'), label + ':',
                          '    ' + _ordinary_instruction(site, clause, trees), label + '_end:'])
        result[unit] = '\n'.join(lines) + '\n'
    return result


def inspect_sources(sources: Mapping[str, str]) -> dict:
    """Expose actual clause coverage without filesystem or native tools."""
    _admit(sources)
    return {'source_modules': len(target.BUSINESS_MODULES),
            'channel_domain_modules': list(channel_layout.MODULE_FUNCTIONS),
            'channel_function_owners': dict(channel_layout.CHANNEL_FUNCTION_OWNERS),
            'channels_compatibility_has_algorithm_body': False,
            'semantic_schedule_module_names': list(target.SOURCE_TREES),
            'normalization_uses_supplied_owned_function_AST': True,
            'voice_context_source': 'contexts_voice.py',
            'voice_algorithm_owner': 'business_voice_loading.py',
            'voice_domain_entries': dict(target.VOICE_DOMAIN_ENTRIES),
            'voice_domain_fragments': list(target.VOICE_DOMAIN_HELPERS),
            'voice_context_fields': dict(target.VOICE_CONTEXT_FIELDS),
            'voice_domain_body_fallback': False,
            'sequence_context_source': 'contexts_sequence.py',
            'sequence_algorithm_owner': 'business_sequence_control.py',
            'sequence_domain_entries': dict(target.SEQUENCE_DOMAIN_ENTRIES),
            'sequence_domain_fragments': list(target.SEQUENCE_DOMAIN_HELPERS),
            'sequence_context_fields': dict(target.SEQUENCE_CONTEXT_FIELDS),
            'sequence_domain_body_fallback': False,
            'sequence_editable_rule': 'repeat counter base literal BYTE at 0EEF',
            'command_algorithm_owners': dict(target.COMMAND_MODULE_ENTRIES),
            'command_actual_services': list(target.COMMAND_SERVICE_LAYOUT),
            'command_context_source': 'contexts_commands.py',
            'command_contexts': dict(target.COMMAND_CONTEXT_FIELDS),
            'command_body_fallback': False,
            'command_editable_rule': 'stereo retained-bits literal BYTE at 0D70',
            'lifecycle_context_source': 'contexts_lifecycle.py',
            'lifecycle_contexts': dict(target.LIFECYCLE_CONTEXT_FIELDS),
            'lifecycle_actual_owners': dict(target.LIFECYCLE_MODULE_FUNCTIONS),
            'lifecycle_actual_transactions': list(target.LIFECYCLE_SERVICE_LAYOUT),
            'lifecycle_body_fallback': False,
            'lifecycle_editable_rule': 'operator-register stride literal BYTE at 08E1',
            'source_operation_sites': len(target.OPERATION_SITES),
            'instructions': sum(len(unit['rows']) for unit in target.UNITS.values()),
            'instruction_bytes': sum(row['size'] for unit in target.UNITS.values() for row in unit['rows']),
            'original_identified_bytes': target.ORIGINAL_IDENTIFIED_BYTES,
            'continuation_supplement_bytes': target.CONTINUATION_SUPPLEMENT_BYTES,
            'runtime_file_reads': False, 'whole_assembly_string_fallback': False,
            'full_AST_consumed': True, 'general_Python_compiler': False,
            'complete_CPU': False, 'complete_audio_playback': False}


compile_sources = generate
