"""Whole Battle Main family with real round/allocation/duel device propagation.

The algorithms remain the existing complete source owners. Only named calls
gain yield-from in isolated whole-module views. Old public Sessions, wait
types, source guards, hardware schedules and original business modules stay
unchanged. This module never supplies a ready bit, IRQ, clock, ACK or frame.
"""
import ast
import copy
import importlib
import inspect
from types import FunctionType, GeneratorType

from .battle_trigger_steps import BattleScenePrograms, _dump, _code_shape, _top_code
from . import battle_round_steps
from .contexts_services import SceneRefreshMemory
from ..high_level_scene_flows import duel_scene_steps
from ..high_level_dynamic_flows import allocation_steps
from ..high_level_main_flows.business_movement_support import _movement_frame
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
from .compiler_battle_lifecycle_steps import (
    MODULE_PATHS, EXPECTED_SOURCES, EXPECTED_PROVIDER_SOURCES,
    EXPECTED_PROVIDER_CONSTANTS, ALLOCATION_SPECS)


MAIN_ENTRIES = (0x498, 0x478, 0x490, 0x458)
ROUND_VIDEO_CALLS = ((0x6826, 0xDE2), (0x6826, 0xE32))
DUEL_SPRITE_CALL = (0x68CE, 0x26DD0)
DUEL_SOUND_RETURNS = (0x270CA, 0x27202, 0x2713E, 0x27276,
    0x272BE, 0x2731A, 0x27350, 0x274C2, 0x2753E)


def _whole_call_module(previous_tree, specs):
    """Exact named CALL lifts, with complete prior-FN and module inverses."""
    changed = copy.deepcopy(previous_tree)
    inverses = {}
    for index, previous in enumerate(previous_tree.body):
        if not isinstance(previous, ast.FunctionDef) or previous.name not in specs:
            continue
        spec = specs[previous.name]
        counts = {name: 0 for name in spec}
        replacements = []

        class Lift(ast.NodeTransformer):
            def visit_Call(self, node):
                node = self.generic_visit(node)
                if not isinstance(node.func, ast.Name) or node.func.id not in spec:
                    return node
                before = copy.deepcopy(node)
                name = node.func.id
                counts[name] += 1
                node.func.id = spec[name]['alias']
                after = ast.copy_location(ast.YieldFrom(value=node), node)
                replacements.append((before, copy.deepcopy(after)))
                return after

        derived = Lift().visit(copy.deepcopy(previous))
        if counts != {name: row['count'] for name, row in spec.items()}:
            raise ValueError('exact lifecycle CALL propagation count differs: ' + previous.name)
        pending = list(replacements)

        class Inverse(ast.NodeTransformer):
            def visit_YieldFrom(self, node):
                for position, (before, after) in enumerate(pending):
                    if _dump(node) == _dump(after):
                        pending.pop(position)
                        return self.visit(copy.deepcopy(before))
                return self.generic_visit(node)

        inverse = Inverse().visit(copy.deepcopy(derived))
        if pending or _dump(inverse) != _dump(previous):
            raise ValueError('complete prior lifecycle FN inverse differs: ' + previous.name)
        changed.body[index] = derived
        inverses[index] = inverse
    if len(inverses) != len(specs):
        raise ValueError('all exact complete lifecycle CALL owners required')
    restored = copy.deepcopy(changed)
    for index, inverse in inverses.items():
        restored.body[index] = inverse
    if _dump(restored) != _dump(previous_tree):
        raise ValueError('complete lifecycle source module inverse differs')
    return ast.fix_missing_locations(changed)


def _round_module(original_tree):
    """Reuse all three complete round views; add video and callback plumbing."""
    previous = battle_round_steps._cooperative_battle_tree(original_tree)
    video_view = _whole_call_module(previous, {
        '_battle_scene_round_call_fields': {
            'initialize_video_registers_and_planes_fields': {
                'alias': '_lifecycle_round_video', 'count': 1}}})
    changed = copy.deepcopy(video_view)
    # The same original presentation owner also bridges the allocation's
    # ordinary synchronous callbacks. A real generator is forwarded; a real
    # synchronous result is returned unchanged, not manufactured or seeded.
    found = []
    for index, node in enumerate(changed.body):
        if not isinstance(node, ast.FunctionDef) or node.name != '_presentation_call_fields':
            continue
        replacements = []

        class Bridge(ast.NodeTransformer):
            def visit_YieldFrom(self, item):
                call = item.value
                if not (isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
                        and call.func.id == 'algorithm' and len(call.args) == 2 and not call.keywords):
                    return self.generic_visit(item)
                before = copy.deepcopy(item)
                after = ast.copy_location(ast.YieldFrom(value=ast.Call(
                    func=ast.Name(id='_lifecycle_callback', ctx=ast.Load()),
                    args=copy.deepcopy(call.args) + [ast.Name(id='algorithm', ctx=ast.Load())],
                    keywords=[])), item)
                replacements.append((before, copy.deepcopy(after)))
                return after

        derived = Bridge().visit(copy.deepcopy(node))
        if len(replacements) != 2:
            raise ValueError('both original presentation callback sites required')
        pending = list(replacements)

        class Undo(ast.NodeTransformer):
            def visit_YieldFrom(self, item):
                for position, (before, after) in enumerate(pending):
                    if _dump(item) == _dump(after):
                        pending.pop(position)
                        return copy.deepcopy(before)
                return self.generic_visit(item)

        inverse = Undo().visit(copy.deepcopy(derived))
        if pending or _dump(inverse) != _dump(node):
            raise ValueError('whole presentation callback bridge inverse differs')
        changed.body[index] = derived
        found.append((index, inverse))
    if len(found) != 1:
        raise ValueError('one complete original presentation bridge required')
    restored = copy.deepcopy(changed)
    restored.body[found[0][0]] = found[0][1]
    if _dump(restored) != _dump(video_view):
        raise ValueError('complete round callback module inverse differs')
    return ast.fix_missing_locations(changed)


def _duel_module(group, original_tree):
    """Keep all37 original cooperative owners; add only two hardware calls."""
    previous, _ = duel_scene_steps._cooperative_duel_module(group, original_tree)
    if group != 'scene':
        return previous
    return _whole_call_module(previous, {'_duel_scene_call_fields': {
        'clear_video_sprite_plane_fields': {'alias': '_lifecycle_duel_sprite', 'count': 1},
        'enqueue_sound_command_fields': {'alias': '_lifecycle_duel_sound', 'count': 1}}})


class BattleLifecycleScenePrograms(BattleScenePrograms):
    """Existing four Main routes plus one same-Scene nested device graph."""

    def __init__(self, state):
        super().__init__(state)
        self.lifecycle_modules = {group: importlib.import_module(path) for group, path in MODULE_PATHS.items()}
        self.lifecycle_originals = {}
        self.lifecycle_codes = {}
        self.lifecycle_trees = {}
        self.lifecycle_plain = {}
        self.lifecycle_registered = []
        for group, sources in EXPECTED_SOURCES.items():
            module = self.lifecycle_modules[group]
            tree = ast.parse(inspect.getsource(module), filename=module.__file__)
            plain = compile(tree, module.__file__, 'exec', dont_inherit=True)
            self.lifecycle_trees[group], self.lifecycle_plain[group] = tree, plain
            nodes = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
            for name, text in sources.items():
                owner = getattr(module, name)
                if (name not in nodes or _dump(nodes[name]) != _dump(ast.parse(text).body[0])
                        or type(owner) is not FunctionType or owner.__globals__ is not vars(module)
                        or owner.__module__ != module.__name__ or owner.__name__ != name
                        or owner.__closure__ is not None or owner.__code__.co_freevars
                        or inspect.isgeneratorfunction(owner)
                        or _code_shape(owner.__code__) != _code_shape(_top_code(plain, name))):
                    raise ValueError('actual complete lifecycle business owner required: ' + name)
                self.lifecycle_originals[group, name] = owner
                self.lifecycle_codes[group, name] = owner.__code__
        providers = dict(round=battle_round_steps, duel=duel_scene_steps, allocation=allocation_steps)
        for group, sources in EXPECTED_PROVIDER_SOURCES.items():
            module = providers[group]
            tree = ast.parse(inspect.getsource(module), filename=module.__file__)
            plain = compile(tree, module.__file__, 'exec', dont_inherit=True)
            nodes = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
            for name, text in sources.items():
                owner = getattr(module, name)
                if (name not in nodes or _dump(nodes[name]) != _dump(ast.parse(text).body[0])
                        or type(owner) is not FunctionType or owner.__globals__ is not vars(module)
                        or owner.__closure__ is not None or owner.__code__.co_freevars
                        or _code_shape(owner.__code__) != _code_shape(_top_code(plain, name))):
                    raise ValueError('actual complete lifecycle source utility required: ' + name)
                self.lifecycle_registered.append((module, name, owner, owner.__code__))
            for name, expected in EXPECTED_PROVIDER_CONSTANTS[group].items():
                actual = getattr(module, name)
                if actual != expected:
                    raise ValueError('existing exact lifecycle source contract changed: ' + name)
                self.lifecycle_registered.append((module, name, actual, None))
        self.lifecycle_round = {}
        self.lifecycle_duel = {}
        self.lifecycle_allocation = {}
        self.lifecycle_namespaces = {}
        self.lifecycle_bindings = []
        self._make_round_views()
        self._make_duel_views()
        self._make_allocation_views()
        self.lifecycle_view_owners = dict(self.lifecycle_round | self.lifecycle_duel | self.lifecycle_allocation)
        self.lifecycle_view_codes = {key: value.__code__ for key, value in self.lifecycle_view_owners.items()}

    def _views(self, role, group, tree, names, destination):
        module = self.lifecycle_modules[group]
        code = compile(tree, module.__file__, 'exec', dont_inherit=True)
        namespace = dict(vars(module))
        self.lifecycle_namespaces[role, group] = namespace
        for name in names:
            owner = self.lifecycle_originals[group, name]
            view = FunctionType(_top_code(code, name), namespace, name, owner.__defaults__, None)
            view.__kwdefaults__ = owner.__kwdefaults__
            view.__annotations__ = dict(owner.__annotations__)
            if not inspect.isgeneratorfunction(view) or view.__closure__ is not None:
                raise ValueError('whole lifecycle view must retain its generator: ' + name)
            destination[role, group, name] = view
            self._bind(namespace, name, view)
        return namespace

    def _bind(self, namespace, name, value):
        namespace[name] = value
        self.lifecycle_bindings.append((namespace, name, value))

    def _make_round_views(self):
        namespace = self._views('round', 'battle', _round_module(self.lifecycle_trees['battle']),
            battle_round_steps.BATTLE_VIEWS, self.lifecycle_round)
        self._bind(namespace, '_battle_round_allocation_program', self._allocation_entry)
        self._bind(namespace, '_battle_round_duel_program', self._duel_entry)
        self._bind(namespace, '_lifecycle_round_video', self.battle_views[
            'services', 'initialize_video_registers_and_planes_fields'])
        self._bind(namespace, '_lifecycle_callback', self._callback)
        main = self._views('round', 'main', battle_round_steps._cooperative_main_tree(
            self.lifecycle_trees['main']), (battle_round_steps.MAIN_VIEW,), self.lifecycle_round)
        self._bind(main, 'battle_scene_round_program', self._round_entry)

    def _make_duel_views(self):
        for group, source_group in (('scene', 'duel_scene'), ('action', 'duel_action'), ('battle', 'battle')):
            self._views('duel', source_group, _duel_module(group, self.lifecycle_trees[source_group]),
                tuple(duel_scene_steps.VIEW_SPECS[group]), self.lifecycle_duel)
        scene = self.lifecycle_namespaces['duel', 'duel_scene']
        action = self.lifecycle_namespaces['duel', 'duel_action']
        bridge = self.lifecycle_duel['duel', 'battle', '_presentation_call_fields']
        self._bind(scene, '_presentation_call_fields', bridge)
        self._bind(action, '_presentation_call_fields', bridge)
        self._bind(scene, '_persistent_duel_action_entry', self.lifecycle_duel[
            'duel', 'duel_action', 'execute_indexed_duel_action_fields'])
        self._bind(action, '_persistent_duel_active_wait', self.lifecycle_duel[
            'duel', 'duel_scene', 'wait_active_duel_action_fields'])
        self._bind(action, '_persistent_duel_either_wait', self.lifecycle_duel[
            'duel', 'duel_scene', 'wait_either_duel_action_fields'])
        self._bind(scene, 'DuelSceneWait', duel_scene_steps.DuelSceneWait)
        self._bind(scene, '_lifecycle_duel_sprite', self.battle_views['services', 'clear_video_sprite_plane_fields'])
        self._bind(scene, '_lifecycle_duel_sound', self.battle_views['services', 'enqueue_sound_command_fields'])

    def _make_allocation_views(self):
        wait = allocation_steps.EXPECTED_OWNERS['wait']
        wait_tree = allocation_steps._cooperative_tree(self.lifecycle_trees['services'], 'wait', wait['name'])
        namespace = self._views('allocation', 'services', wait_tree, (wait['name'],), self.lifecycle_allocation)
        self._bind(namespace, 'AllocationSceneWait', allocation_steps.AllocationSceneWait)
        for group, spec in ALLOCATION_SPECS.items():
            self._views('allocation', group, _whole_call_module(self.lifecycle_trees[group], spec),
                tuple(spec), self.lifecycle_allocation)
        aliases = {'_lifecycle_allocation_services_enqueue_sound_command_fields': self.battle_views[
            'services', 'enqueue_sound_command_fields'],
            '_lifecycle_allocation_services_clear_video_sprite_plane_fields': self.battle_views[
                'services', 'clear_video_sprite_plane_fields'],
            '_lifecycle_allocation_services_wait_for_scene_sound_byte_fields': self.lifecycle_allocation[
                'allocation', 'services', 'wait_for_scene_sound_byte_fields'],
            '_lifecycle_allocation_battle__presentation_call_fields': self.lifecycle_round[
                'round', 'battle', '_presentation_call_fields']}
        for (_, group, name), view in self.lifecycle_allocation.items():
            aliases['_lifecycle_allocation_' + group + '_' + name] = view
        for (role, _), namespace in self.lifecycle_namespaces.items():
            if role != 'allocation':
                continue
            for name, value in aliases.items():
                if name in namespace:
                    raise ValueError('lifecycle allocation alias must not shadow original source binding')
                self._bind(namespace, name, value)

    def require_current(self, state):
        super().require_current(state)
        if hasattr(self, 'lifecycle_originals'):
            for (group, name), owner in self.lifecycle_originals.items():
                if (getattr(self.lifecycle_modules[group], name) is not owner
                        or owner.__code__ is not self.lifecycle_codes[group, name]):
                    raise ValueError('actual complete lifecycle business owner changed: ' + name)
        if hasattr(self, 'lifecycle_registered'):
            for module, name, owner, code in self.lifecycle_registered:
                if getattr(module, name) is not owner or code is not None and owner.__code__ is not code:
                    raise ValueError('actual lifecycle source utility/contract changed: ' + name)
        if hasattr(self, 'lifecycle_view_owners'):
            current = self.lifecycle_round | self.lifecycle_duel | self.lifecycle_allocation
            if current.keys() != self.lifecycle_view_owners.keys():
                raise ValueError('finite lifecycle whole-view graph changed')
            for key, owner in self.lifecycle_view_owners.items():
                if current[key] is not owner or owner.__code__ is not self.lifecycle_view_codes[key]:
                    raise ValueError('complete lifecycle generator identity changed: ' + key[2])
            for namespace, name, value in self.lifecycle_bindings:
                if namespace.get(name) is not value:
                    raise ValueError('private lifecycle whole-view binding changed: ' + name)

    def _callback(self, memory, frame, algorithm):
        self.require_current(memory.state)
        result = algorithm(memory, frame)
        if type(result) is GeneratorType:
            return (yield from result)
        return result

    def _allocation_entry(self, state, frame):
        self.require_current(state)
        frame = _movement_frame(state, frame)
        frame.validate(state, True)
        if frame.status != state.sr & 31:
            raise ValueError('actual complete allocation entry SR/CCR-X required')
        return (yield from self._message_waits(self.lifecycle_allocation[
            'allocation', 'objects', 'run_scene_object_controller_fields'](SceneRefreshMemory(state), frame)))

    def _duel_entry(self, state, frame):
        self.require_current(state)
        frame = _movement_frame(state, frame)
        frame.validate(state, True)
        if frame.status != state.sr & 31:
            raise ValueError('actual complete duel entry SR/CCR-X required')
        stack = frame.stack_cursor.base
        result = yield from self._message_waits(self.lifecycle_duel[
            'duel', 'duel_scene', 'run_duel_scene_fields'](state, frame))
        result = _movement_frame(state, result)
        result.validate(state, True)
        if result.stack_cursor.base != stack or result.status != state.sr & 31:
            raise ValueError('completed whole duel must retain its actual incoming SP and full SR')
        return result

    def _round_entry(self, state, frame):
        self.require_current(state)
        frame = _movement_frame(state, frame)
        frame.validate(state, True)
        if frame.status != state.sr & 31:
            raise ValueError('actual complete round entry SR/CCR-X required')
        return (yield from self._message_waits(self.lifecycle_round[
            'round', 'battle', 'run_battle_scene_round_fields'](SceneRefreshMemory(state), frame)))

    def _round(self, memory, frame):
        return (yield from self._round_entry(memory.state, frame))

    def _display_child(self, state, frame, target, continuation):
        self.require_current(state)
        if target == 0x498:
            if continuation != 0x3CE:
                raise MovementContinuationBoundary(target, frame, 'whole Main498 requires its existing3CE LONG')
            return (yield from self._message_waits(self.lifecycle_round[
                'round', 'main', battle_round_steps.MAIN_VIEW](state, frame)))
        return (yield from super()._display_child(state, frame, target, continuation))

    def main_scene_call(self, state, frame, target, continuation):
        if target != 0x498:
            return (yield from super().main_scene_call(state, frame, target, continuation))
        self.require_current(state)
        if self._started or continuation != 0x3CE:
            raise ValueError('one actual indexed Main498/3CE invocation required')
        self._started = True
        return (yield from self.views['display', 'display_call_fields'](state, frame, target, continuation))
