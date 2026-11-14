"""Whole Main4B0 new-campaign setup with real controller/device continuations.

The existing0514 algorithm, menu CALL528 and commit/descriptors are reused.
Only continuation plumbing is derived; the old blocking/IRQ-only Sessions
remain independent and retain their original strict contracts.
"""
import ast
import copy
import importlib
import inspect
from types import FunctionType

from .battle_trigger_steps import BattleScenePrograms, _dump, _code_shape, _top_code
from .contexts_services import SceneRefreshMemory
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
from .compiler_campaign_menu_steps import EXPECTED_OWNER_ASTS


MODULE_PATHS = {
    'main': 'tools.high_level_main_flows.business_main',
    'campaign': 'tools.high_level_main_flows.campaign_setup_steps',
    'support': 'tools.high_level_main_flows.business_scene_support',
    'map': 'tools.high_level_main_flows.business_map',
}
MAIN_ENTRY = 0x4B0
VIEW_NAMES = {
    'main': ('initialize_post_duel_campaign_fields',),
    'campaign': ('campaign_setup_program', '_campaign_setup_menu_call_steps'),
}
CAMPAIGN_CALLS = ((0x808A, 0x522), (0x6826, 0x532), (0x3076E, 0x538),
    (0x3E54, 0x548), (0x9390, 0x54E), (0x15BE, 0x554))
SOURCE_CONTRACT = {
    'provider': 'tools.high_level_gameplay_flow.campaign_menu_steps',
    'compiler': 'tools.high_level_gameplay_flow.compiler_campaign_menu_steps',
    'external_source_tables': ('EXPECTED_OWNER_ASTS', 'EXPECTED_MODULE_AST'),
    'controller_provider': 'tools.high_level_gameplay_flow.controller_menu_steps',
}


def _campaign_menu_tree(group, original_tree):
    """Derive three entire originals; restore each FN and entire source module."""
    if group not in VIEW_NAMES:
        raise ValueError('only complete Main4B0 and campaign menu source views are admitted')
    result = copy.deepcopy(original_tree)
    restored = copy.deepcopy(original_tree)
    found = []
    for index, original in enumerate(original_tree.body):
        if not isinstance(original, ast.FunctionDef) or original.name not in VIEW_NAMES[group]:
            continue
        if _dump(original) != EXPECTED_OWNER_ASTS[MODULE_PATHS[group]][original.name]:
            raise ValueError('complete new-campaign source differs: ' + original.name)
        changed = copy.deepcopy(original)
        changes = []
        calls = []
        if original.name == '_campaign_setup_menu_call_steps':
            # The physical528 CALL/RTS surrounding these three statements is
            # retained verbatim. The lower whole controller program owns no
            # second outer return slot and forwards its actual typed waits.
            candidates = [position for position, node in enumerate(changed.body)
                if isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'child']
            if len(candidates) != 1:
                raise ValueError('one original controller Session invocation required')
            start = candidates[0]
            old_block = changed.body[start:start + 3]
            expected = ast.parse('''child = ControllerSetupSession(state, entered)
returned = child.start()
while type(returned) is ControllerSetupWait:
    waiting = returned
    irq_frame = yield waiting
    returned = child.resume(irq_frame, waiting.poll)
''').body
            if [_dump(node) for node in old_block] != [_dump(node) for node in expected]:
                raise ValueError('complete original controller start/resume block required')
            replacement = ast.parse('returned = yield from _campaign_menu_controller_program(state, entered)').body[0]
            changed.body[start:start + 3] = [ast.copy_location(replacement, old_block[0])]
            inverse = copy.deepcopy(changed)
            inverse.body[start:start + 1] = copy.deepcopy(old_block)
        else:
            class Lift(ast.NodeTransformer):
                def visit_Call(self, node):
                    node = self.generic_visit(node)
                    if not isinstance(node.func, ast.Name):
                        return node
                    name = node.func.id
                    if original.name == 'initialize_post_duel_campaign_fields':
                        if name != 'run_campaign_setup_blocking_fields':
                            return node
                        if node.keywords or len(node.args) != 2:
                            raise ValueError('whole Main4B0 facade invocation required')
                        alias, lifted = '_campaign_menu_parent', True
                        calls.append(name)
                    elif name == '_campaign_call_fields':
                        if node.keywords or len(node.args) != 4:
                            raise ValueError('actual four-argument campaign CALL required')
                        calls.append(tuple(ast.literal_eval(value) for value in node.args[2:]))
                        alias, lifted = '_campaign_menu_call', True
                    elif name == '_campaign_setup_menu_call_steps':
                        if node.keywords or len(node.args) != 4 or tuple(
                                ast.literal_eval(value) for value in node.args[2:]) != (0x305B0, 0x528):
                            raise ValueError('actual controller305B0/528 child required')
                        calls.append((0x305B0, 0x528))
                        alias, lifted = '_campaign_menu_menu_call', False
                    else:
                        return node
                    before = copy.deepcopy(node)
                    node.func.id = alias
                    after = ast.copy_location(ast.YieldFrom(value=node), node) if lifted else node
                    changes.append((before, copy.deepcopy(after)))
                    return after

            changed = Lift().visit(changed)
            expected_calls = ('run_campaign_setup_blocking_fields',) if group == 'main' else (
                CAMPAIGN_CALLS[0], (0x305B0, 0x528), *CAMPAIGN_CALLS[1:])
            if tuple(calls) != expected_calls:
                raise ValueError('all original campaign facade/CALL sites must remain exact')
            pending = list(changes)

            class Inverse(ast.NodeTransformer):
                def visit(self, node):
                    for position, (before, after) in enumerate(pending):
                        if _dump(node) == _dump(after):
                            pending.pop(position)
                            return copy.deepcopy(before)
                    return super().visit(node)

            inverse = Inverse().visit(copy.deepcopy(changed))
            if pending:
                raise ValueError('every admitted campaign continuation must invert')
        if _dump(inverse) != _dump(original):
            raise ValueError('complete original campaign FN inverse differs: ' + original.name)
        result.body[index], restored.body[index] = changed, inverse
        found.append(original.name)
    if set(found) != set(VIEW_NAMES[group]) or _dump(restored) != _dump(original_tree):
        raise ValueError('complete original campaign module inverse differs')
    return ast.fix_missing_locations(result)


class CampaignMenuScenePrograms(BattleScenePrograms):
    """One actual4B0/3CE invocation, through menu confirmation to original554."""

    def __init__(self, state):
        super().__init__(state)
        from .controller_menu_steps import ControllerMenuPrograms
        self.menu_modules = {group: importlib.import_module(path) for group, path in MODULE_PATHS.items()}
        self.menu_owners = []
        self.menu_views, self.menu_namespaces, self.menu_bindings = {}, {}, {}
        for group, module in self.menu_modules.items():
            tree = ast.parse(inspect.getsource(module), filename=module.__file__)
            plain = compile(tree, module.__file__, 'exec', dont_inherit=True)
            nodes = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
            originals = {}
            for name, expected in EXPECTED_OWNER_ASTS[MODULE_PATHS[group]].items():
                owner = getattr(module, name)
                if (name not in nodes or _dump(nodes[name]) != expected
                        or type(owner) is not FunctionType or owner.__globals__ is not vars(module)
                        or owner.__module__ != module.__name__ or owner.__name__ != name
                        or owner.__closure__ is not None or owner.__code__.co_freevars
                        or _code_shape(owner.__code__) != _code_shape(_top_code(plain, name))):
                    raise ValueError('actual complete new-campaign owner required: ' + name)
                self.menu_owners.append((module, name, owner, owner.__code__))
                originals[name] = owner
            if group not in VIEW_NAMES:
                continue
            derived = compile(_campaign_menu_tree(group, tree), module.__file__, 'exec', dont_inherit=True)
            namespace = dict(vars(module))
            self.menu_namespaces[group] = namespace
            for name in VIEW_NAMES[group]:
                original = originals[name]
                view = FunctionType(_top_code(derived, name), namespace, name, original.__defaults__, None)
                view.__kwdefaults__, view.__annotations__ = original.__kwdefaults__, dict(original.__annotations__)
                if not inspect.isgeneratorfunction(view) or view.__closure__ is not None:
                    raise ValueError('whole new-campaign continuation must be a closure-free generator')
                self.menu_views[group, name] = view
        self.menu_view_owners = dict(self.menu_views)
        self.menu_view_codes = {key: view.__code__ for key, view in self.menu_views.items()}
        self.menu_controller = ControllerMenuPrograms(self)
        self.menu_controller_owner = self.menu_controller
        self.menu_call = self.views['main', '_campaign_call_fields']
        self.menu_call_code = self.menu_call.__code__
        self.menu_display_call = self.views['display', 'display_call_fields']
        self.menu_display_call_code = self.menu_display_call.__code__
        aliases = {
            '_campaign_menu_parent': self.menu_views['campaign', 'campaign_setup_program'],
            '_campaign_menu_menu_call': self.menu_views['campaign', '_campaign_setup_menu_call_steps'],
            '_campaign_menu_call': self.menu_call,
            '_campaign_menu_controller_program': self.menu_controller.program,
        }
        for group, namespace in self.menu_namespaces.items():
            for name, owner in aliases.items():
                if name in namespace:
                    raise ValueError('private campaign alias cannot replace an original name')
                namespace[name] = owner
            names = set(aliases)
            for (view_group, name), view in self.menu_views.items():
                if view_group == group:
                    names.update(key for key in view.__code__.co_names if key in namespace)
            self.menu_bindings[group] = {name: namespace[name] for name in names}

    def require_current(self, state):
        super().require_current(state)
        if hasattr(self, 'menu_owners'):
            for module, name, owner, code in self.menu_owners:
                if getattr(module, name) is not owner or owner.__code__ is not code:
                    raise ValueError('complete new-campaign owner changed: ' + name)
        if hasattr(self, 'menu_view_owners'):
            if self.menu_views.keys() != self.menu_view_owners.keys():
                raise ValueError('the finite new-campaign view set changed')
            for key, view in self.menu_view_owners.items():
                if self.menu_views[key] is not view or view.__code__ is not self.menu_view_codes[key]:
                    raise ValueError('whole new-campaign view changed: ' + key[1])
        if hasattr(self, 'menu_controller_owner'):
            # The lower guard checks only its own source/view bindings and
            # explicitly does not recurse back through this parent.
            if self.menu_controller is not self.menu_controller_owner:
                raise ValueError('the same controller/menu continuation owner is required')
            self.menu_controller.require_current(state)
            if (self.views['main', '_campaign_call_fields'] is not self.menu_call
                    or self.menu_call.__code__ is not self.menu_call_code
                    or self.views['display', 'display_call_fields'] is not self.menu_display_call
                    or self.menu_display_call.__code__ is not self.menu_display_call_code):
                raise ValueError('the same physical campaign/display CALL views are required')
            for group, bindings in self.menu_bindings.items():
                for name, owner in bindings.items():
                    if self.menu_namespaces[group].get(name) is not owner:
                        raise ValueError('private new-campaign namespace binding changed: ' + name)

    def _campaign_child(self, state, frame, target, continuation):
        self.require_current(state)
        if (target, continuation) == (0x808A, 0x522):
            return (yield from self.battle_views['services', 'enqueue_sound_command_fields'](
                SceneRefreshMemory(state), frame))
        if (target, continuation) == (0x6826, 0x532):
            return (yield from self.battle_views['services', 'initialize_video_registers_and_planes_fields'](
                SceneRefreshMemory(state), frame))
        return (yield from super()._campaign_child(state, frame, target, continuation))

    def _display_child(self, state, frame, target, continuation):
        self.require_current(state)
        if target == MAIN_ENTRY:
            if continuation != 0x3CE:
                raise MovementContinuationBoundary(target, frame, 'Main4B0 requires its actual3CE LONG')
            return (yield from self.menu_views['main', 'initialize_post_duel_campaign_fields'](state, frame))
        return (yield from super()._display_child(state, frame, target, continuation))

    def main_scene_call(self, state, frame, target, continuation):
        if target != MAIN_ENTRY:
            return (yield from super().main_scene_call(state, frame, target, continuation))
        self.require_current(state)
        if self._started or continuation != 0x3CE:
            raise ValueError('one original indexed Main4B0 invocation required')
        self._started = True
        return (yield from self._message_waits(self.menu_display_call(state, frame, target, continuation)))
