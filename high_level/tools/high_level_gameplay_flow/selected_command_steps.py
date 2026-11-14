"""Selected city/group commands at the original E0C4 relative-call table.

The original DF6E/E050 parents still read the live selector and table WORD.
This provider supplies their complete, already-recovered children and keeps
the two nested message paths suspended on the same Scene and physical stack.
It neither substitutes a table result nor re-enters an executed prefix.
"""
import ast
import copy
import inspect
from types import FunctionType

from . import city_command_steps
from .city_command_steps import CityCommandScenePrograms, _pin_registered_source
from .compiler_city_command_steps import EXPECTED_MODULE_AST as PARENT_SOURCE_AST
from .battle_trigger_steps import _dump, _code_shape, _top_code
from .contexts_services import SceneRefreshMemory
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
from ..high_level_remaining_flows import business_lowbank, business_city
from ..high_level_remaining_flows import compiler_lowbank, compiler_city


MAIN_ENTRY = 0x434
SELECTED_RETURN = 0xE06C
# These are unique complete entries, not a clamp on the live selector. The
# repeated zero offsets still reach FE06; exact selector 6 still takes the
# original E0BC JMP30AC6 before any source-table read or E06C CALL exists.
SELECTED_ENTRIES = {
    0xFE06: 'lowbank_coordinate_live_state_109_fields',
    0xFF58: 'lowbank_select_live_state_34_fields',
    0xFF98: 'lowbank_process_counted_records_37_fields',
    0x10224: 'lowbank_coordinate_live_state_111_fields',
    0x1022C: 'lowbank_coordinate_live_state_112_fields',
    0x10234: 'lowbank_update_record_flags_15_fields',
    0x103EA: 'lowbank_process_counted_records_38_fields',
    0x10694: 'lowbank_coordinate_live_state_113_fields',
    0x10A34: 'lowbank_coordinate_live_state_115_fields',
    0x10A3C: 'lowbank_coordinate_live_state_116_fields',
    0x10A44: 'lowbank_coordinate_live_state_117_fields',
}
VIEW_SPECS = {
    'lowbank': {
        '_lowbank_ui_call_fields': {'_lowbank_ui_known_child_fields': 1},
        'lowbank_process_counted_records_38_fields': {'_lowbank_ui_call_fields': 5},
        'lowbank_coordinate_live_state_116_fields': {'_lowbank_ui_call_fields': 1},
        'lowbank_coordinate_live_state_117_fields': {'_lowbank_ui_call_fields': 1},
    },
    'city': {
        '_deployment_menu_call_fields': {'execute_deployment_menu_fields': 1},
        'city_process_counted_records_16_fields': {'_deployment_menu_call_fields': 5},
        'city_process_counted_records_16_alternate_1_fields': {
            'city_process_counted_records_16_fields': 1},
    },
}
LOWBANK_CALLS = frozenset((
    (0x101F8, 0x1048E), (0x1058C, 0x10494), (0x5F48, 0x104C2),
    (0x30A74, 0x10536), (0x26BFA, 0x1055C),
    (0x1B604, 0x10A42), (0x1BFE0, 0x10A4A),
))
DEPLOYMENT_CALLS = frozenset((
    (0x1B90C, 0x1B608), (0x1B6C2, 0x1B620),
    (0x30A74, 0x1B68C), (0x1B968, 0x1B690), (0x1D3BC, 0x1B69E),
))
SOURCE_CONTRACT = {
    'parent': 'tools.high_level_gameplay_flow.city_command_steps',
    'parent_registry': 'tools.high_level_gameplay_flow.compiler_city_command_steps',
    'business_modules': {
        'lowbank': 'tools.high_level_remaining_flows.business_lowbank',
        'city': 'tools.high_level_remaining_flows.business_city',
    },
    'business_registries': {
        'lowbank': 'tools.high_level_remaining_flows.compiler_lowbank',
        'city': 'tools.high_level_remaining_flows.compiler_city',
    },
    'registry_table': 'DECLARATIONS',
    'table_source': 'tools.state_dispatch_word_fields.codec',
    'source_table': (0xE0C4, 0xE0EE, 0xFE06),
    'message_pairs': ((0x30A74, 0x10536), (0x30A74, 0x1B68C)),
}


def _without_docstring(node):
    result = copy.deepcopy(node)
    if (result.body and isinstance(result.body[0], ast.Expr)
            and isinstance(result.body[0].value, ast.Constant)
            and type(result.body[0].value.value) is str):
        result.body.pop(0)
    return result


def _declared_node(name, declaration):
    """Reuse the existing complete normal-source declaration, not an oracle."""
    if type(declaration) is not dict or any(type(declaration.get(key)) is not str
            for key in ('signature', 'returns', 'flow')):
        raise ValueError('complete registered selected-command declaration required: ' + name)
    source = ('def ' + name + '(' + declaration['signature'] + ')'
        + (' -> ' + declaration['returns'] if declaration['returns'] else '')
        + ':\n' + '\n'.join('    ' + line for line in declaration['flow'].splitlines()))
    nodes = ast.parse(source).body
    if len(nodes) != 1 or not isinstance(nodes[0], ast.FunctionDef):
        raise ValueError('one complete declared selected-command owner required')
    return nodes[0]


def _selected_module(group, original_tree, declarations):
    """Seven complete FN views; every replacement and whole module invert."""
    if group not in VIEW_SPECS:
        raise ValueError('only the two actual selected-command business modules are admitted')
    result, restored = copy.deepcopy(original_tree), copy.deepcopy(original_tree)
    found = set()
    for index, original in enumerate(original_tree.body):
        if not isinstance(original, ast.FunctionDef) or original.name not in VIEW_SPECS[group]:
            continue
        expected = _declared_node(original.name, declarations[original.name])
        if _dump(_without_docstring(original)) != _dump(expected):
            raise ValueError('complete selected-command owner differs: ' + original.name)
        spec = VIEW_SPECS[group][original.name]
        counts, replacements = dict.fromkeys(spec, 0), []

        class Lift(ast.NodeTransformer):
            def visit_Call(self, node):
                node = self.generic_visit(node)
                if not isinstance(node.func, ast.Name) or node.func.id not in spec:
                    return node
                before = copy.deepcopy(node)
                name = node.func.id
                if node.keywords:
                    raise ValueError('original selected-command positional ABI required')
                if original.name == '_lowbank_ui_call_fields':
                    if len(node.args) != 3:
                        raise ValueError('complete original Lowbank child ABI required')
                    node.func.id = '_selected_lowbank_child'
                    node.args.append(ast.Name(id='continuation', ctx=ast.Load()))
                elif original.name == '_deployment_menu_call_fields':
                    if len(node.args) != 3:
                        raise ValueError('complete original deployment child ABI required')
                    node.func.id = '_selected_deployment_child'
                    node.args.append(ast.Name(id='continuation', ctx=ast.Load()))
                counts[name] += 1
                after = ast.copy_location(ast.YieldFrom(value=node), node)
                replacements.append((before, copy.deepcopy(after)))
                return after

        changed = Lift().visit(copy.deepcopy(original))
        if counts != spec:
            raise ValueError('all actual selected-command CALL/tail sites required: ' + original.name)
        pending = list(replacements)

        class Inverse(ast.NodeTransformer):
            def visit_YieldFrom(self, node):
                for position, (before, after) in enumerate(pending):
                    if _dump(node) == _dump(after):
                        pending.pop(position)
                        return copy.deepcopy(before)
                raise ValueError('non-admitted selected-command continuation')

        inverse = Inverse().visit(copy.deepcopy(changed))
        if pending or _dump(inverse) != _dump(original):
            raise ValueError('complete original selected-command FN inverse differs')
        result.body[index], restored.body[index] = changed, inverse
        found.add(original.name)
    if found != set(VIEW_SPECS[group]) or _dump(restored) != _dump(original_tree):
        raise ValueError('complete original selected-command module inverse differs')
    return ast.fix_missing_locations(result)


class SelectedCommandScenePrograms(CityCommandScenePrograms):
    """One real Main434, including the live E06C selected-command children.

    The inherited DF6E/force/clear parents and the shared message owner remain
    the sole algorithms. Only the original CALL propagation changes; internal
    synchronous settlement, resource caps, RNG and packet order are unaltered.
    """

    def __init__(self, state):
        super().__init__(state)
        self.selected_parent_bindings = _pin_registered_source(city_command_steps, PARENT_SOURCE_AST)
        self.selected_modules = {'lowbank': business_lowbank, 'city': business_city}
        self.selected_registries = {'lowbank': compiler_lowbank, 'city': compiler_city}
        self.selected_owners, self.selected_declarations = [], {}
        self.selected_views, self.selected_namespaces, self.selected_bindings = {}, {}, {}
        required = {
            'lowbank': set(SELECTED_ENTRIES.values()) | set(VIEW_SPECS['lowbank'])
                | {'_lowbank_ui_known_child_fields'},
            'city': set(VIEW_SPECS['city']) | {'execute_deployment_menu_fields',
                'deploy_selected_group_fields', 'deploy_selected_group_from_object_fields',
                'city_process_counted_records_15_fields', 'begin_city_group_result_notice_fields',
                'append_city_group_result_notice_fields', 'prepare_both_battle_sides_fields',
                'deployment_force_carry_fields', 'settle_complete_battle_fields',
                'settle_group_at_city_fields'},
        }
        for group, module in self.selected_modules.items():
            tree = ast.parse(inspect.getsource(module), filename=module.__file__)
            plain = compile(tree, module.__file__, 'exec', dont_inherit=True)
            nodes = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
            registry = self.selected_registries[group]
            declarations = registry.DECLARATIONS
            for name in sorted(required[group]):
                if name not in nodes or name not in declarations:
                    raise ValueError('complete registered selected-command source missing: ' + name)
                expected = _declared_node(name, declarations[name])
                if _dump(_without_docstring(nodes[name])) != _dump(expected):
                    raise ValueError('complete current selected-command source differs: ' + name)
                self.selected_declarations[group, name] = (
                    declarations, copy.deepcopy(declarations[name]))
            # Pin the loaded complete module's actual local CodeTypes and its
            # imported functions/classes too, so a suspended derived namespace
            # cannot silently route an original synchronous child elsewhere.
            for name, owner in vars(module).items():
                if type(owner) is FunctionType:
                    if owner.__module__ == module.__name__:
                        if (name not in nodes or owner.__globals__ is not vars(module)
                                or owner.__name__ != name or owner.__closure__ is not None
                                or owner.__code__.co_freevars
                                or _code_shape(owner.__code__) != _code_shape(_top_code(plain, name))):
                            raise ValueError('actual complete selected-command owner required: ' + name)
                    self.selected_owners.append((module, name, owner, owner.__code__))
                elif type(owner) is type:
                    self.selected_owners.append((module, name, owner, None))
            derived = compile(_selected_module(group, tree, declarations), module.__file__,
                'exec', dont_inherit=True)
            namespace = dict(vars(module))
            for name in ('_selected_lowbank_child', '_selected_deployment_child'):
                if name in namespace:
                    raise ValueError('private selected-command binding may not shadow original source')
            for name in VIEW_SPECS[group]:
                original = getattr(module, name)
                view = FunctionType(_top_code(derived, name), namespace, name,
                    original.__defaults__, None)
                view.__kwdefaults__, view.__annotations__ = original.__kwdefaults__, dict(original.__annotations__)
                if not inspect.isgeneratorfunction(view) or view.__closure__ is not None:
                    raise ValueError('complete selected-command view must be a closure-free generator')
                namespace[name] = self.selected_views[group, name] = view
            namespace['_selected_lowbank_child'] = self._selected_lowbank_child
            namespace['_selected_deployment_child'] = self._selected_deployment_child
            self.selected_namespaces[group] = namespace
            self.selected_bindings[group] = {name: value for name, value in namespace.items()
                if type(value) in (FunctionType, type) or name.startswith('_selected_')}
        self.selected_view_owners = dict(self.selected_views)
        self.selected_view_codes = {key: view.__code__ for key, view in self.selected_views.items()}
        self.selected_message = self.message_scene
        self.selected_message_program = type(self.message_scene).program
        self.selected_message_code = self.selected_message_program.__code__
        self.selected_entry_names = dict(SELECTED_ENTRIES)

    def require_current(self, state):
        super().require_current(state)
        if hasattr(self, 'selected_parent_bindings'):
            for holder, name, owner, code in self.selected_parent_bindings:
                actual = vars(holder).get(name)
                if actual is not owner or (code is not None and actual.__code__ is not code):
                    raise ValueError('actual selected-command parent source changed: ' + name)
        if hasattr(self, 'selected_owners'):
            for module, name, owner, code in self.selected_owners:
                actual = vars(module).get(name)
                if actual is not owner or (code is not None and actual.__code__ is not code):
                    raise ValueError('actual selected-command business binding changed: ' + name)
            for (group, name), (declarations, expected) in self.selected_declarations.items():
                if (self.selected_registries[group].DECLARATIONS is not declarations
                        or declarations.get(name) != expected):
                    raise ValueError('selected-command complete source declaration changed: ' + name)
        if hasattr(self, 'selected_view_owners'):
            if self.selected_views.keys() != self.selected_view_owners.keys():
                raise ValueError('finite selected-command view set changed')
            for key, view in self.selected_view_owners.items():
                if self.selected_views[key] is not view or view.__code__ is not self.selected_view_codes[key]:
                    raise ValueError('complete selected-command view changed: ' + key[1])
            for group, bindings in self.selected_bindings.items():
                for name, value in bindings.items():
                    if self.selected_namespaces[group].get(name) is not value:
                        raise ValueError('private selected-command namespace changed: ' + name)
            if (self.message_scene is not self.selected_message
                    or type(self.message_scene).program is not self.selected_message_program
                    or self.selected_message_program.__code__ is not self.selected_message_code
                    or SELECTED_ENTRIES != self.selected_entry_names):
                raise ValueError('same selected-command table/message owner required')

    def _selected_message(self, state, frame):
        self.require_current(state)
        # E06C and the actual10536/1B68C child LONGs are already in live RAM.
        # The shared30A74 saves/restores its own two WORDs; no replay or slot.
        return (yield from self._message_waits(
            self.selected_message.program(SceneRefreshMemory(state), frame)))

    def _selected_lowbank_child(self, state, frame, target, continuation):
        self.require_current(state)
        if (target, continuation) not in LOWBANK_CALLS:
            raise MovementContinuationBoundary(target, frame, 'not an actual selected Lowbank CALL/return pair')
        if target == 0x30A74:
            return (yield from self._selected_message(state, frame))
        if target in (0x1B604, 0x1BFE0):
            name = ('city_process_counted_records_16_fields' if target == 0x1B604
                else 'city_process_counted_records_16_alternate_1_fields')
            return (yield from self.selected_views['city', name](state, frame))
        return business_lowbank._lowbank_ui_known_child_fields(state, frame, target)

    def _selected_deployment_child(self, state, target, frame, continuation):
        self.require_current(state)
        if (target, continuation) not in DEPLOYMENT_CALLS:
            raise MovementContinuationBoundary(target, frame, 'not an actual selected deployment CALL/return pair')
        if target == 0x30A74:
            return (yield from self._selected_message(state, frame))
        return business_city.execute_deployment_menu_fields(state, target, frame)

    def _display_child(self, state, frame, target, continuation):
        self.require_current(state)
        if continuation == SELECTED_RETURN:
            name = SELECTED_ENTRIES.get(target)
            if name is None:
                raise MovementContinuationBoundary(target, frame, 'live E0C4 target has no admitted complete owner')
            if ('lowbank', name) in self.selected_views:
                return (yield from self.selected_views['lowbank', name](state, frame))
            return getattr(business_lowbank, name)(state, frame)
        return (yield from super()._display_child(state, frame, target, continuation))
