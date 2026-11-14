"""Shared whole30A74 continuation with its actual AF48 and060C children.

An existing same-Scene BattleScenePrograms supplies only its reviewed refresh
and complete clear views. No old ForceTurnSession guard or public owner changes.
"""
import ast
import copy
import importlib
import inspect
from types import CodeType, FunctionType

from .battle_trigger_steps import BattleScenePrograms


MODULE_PATHS = {
    'force': 'tools.high_level_main_flows.force_turn_steps',
    'services': 'tools.high_level_gameplay_flow.business_services',
}
VIEW_SPECS = {
    'force': {'force_turn_message_program': {'_gameplay_message_call_fields': 2}},
    'services': {'_gameplay_message_call_fields': {
        'refresh_gameplay_scene_fields': 1, 'clear_scene_video_and_state_fields': 1}},
}
EXPECTED_SOURCE = {'force': {'force_turn_message_program': 'def force_turn_message_program(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """30A74..30ABE: physical two-WORD save, vblank child and completion wait.\n\n    A Scene IRQ with missing full CPU fields stops at the real busy-loop read.\n    Historical Gameplay supplies only its existing progress observations.\n    """\n    frame = _scene_refresh_frame(memory, frame)\n    saved = []\n    for address in (4294964754, 4294964066):\n        memory.sync_status(frame)\n        value = memory.state.read(address, 2)\n        saved.append(value)\n        if frame.stack_cursor is not None:\n            stack = frame.stack_cursor.advance(-2)\n            stack.set_word(0, value)\n            frame = first_replace(frame, stack_cursor=stack)\n        frame = _scene_refresh_flags(memory, frame, value, 2)\n    frame = _scene_refresh_emit(memory, frame, 4294964754, 2, 523)\n    memory.state.read(4294964736, 2)\n    frame = _scene_refresh_emit(memory, frame, 4294964736, 2, 0)\n    frame = _gameplay_message_call_fields(memory, frame, 44872, 199308)\n    frame = memory.status_word(frame, 9472)\n    while True:\n        while True:\n            memory.sync_status(frame)\n            command = memory.state.read(4294964736, 2)\n            frame = _scene_refresh_flags(memory, frame, command, 2)\n            if command:\n                break\n            frame = (yield ForceTurnWait(memory.state, frame, 199312).validate())\n        command = memory.state.read(4294964736, 2)\n        frame = _first_compare_word(frame, command, 40)\n        memory.sync_status(frame)\n        if command != 40:\n            break\n        frame = _gameplay_message_call_fields(memory, frame, 1548, 199334)\n        memory.state.read(4294964736, 2)\n        frame = _scene_refresh_emit(memory, frame, 4294964736, 2, 0)\n        frame = memory.status_word(frame, 9472)\n    frame = memory.status_word(frame, 9984)\n    for address, legacy_value in ((4294964066, saved[1]), (4294964754, saved[0])):\n        if frame.stack_cursor is None:\n            value = legacy_value\n        else:\n            value = frame.stack_cursor.word()\n            frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))\n        frame = _scene_refresh_emit(memory, frame, address, 2, value)\n    return memory.sync_status(frame)'}, 'services': {'_gameplay_message_call_fields': 'def _gameplay_message_call_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long) -> FirstDeploymentFrame:\n    """30A74\'s two real children; Scene never projects missing display ABI."""\n    frame = _scene_refresh_frame(memory, frame)\n    if (target, continuation) not in ((0xAF48, 0x30A8C), (0x60C, 0x30AA6)):\n        raise ValueError(\'original gameplay message child and token required\')\n    entered = memory.sync_status(frame)\n    if frame.stack_cursor is not None:\n        stack = frame.stack_cursor.advance(-4)\n        stack.set_long(0, continuation)\n        entered = first_replace(frame, stack_cursor=stack)\n    if target == 0xAF48:\n        returned = refresh_gameplay_scene_fields(memory, entered)\n    elif entered.stack_cursor is None:\n        clear_scene_video_and_state(memory.state)\n        returned = first_replace(entered, status=None)\n    else:\n        returned = clear_scene_video_and_state_fields(memory, entered)\n    returned = _scene_refresh_frame(memory, returned)\n    memory.sync_status(returned)\n    if frame.stack_cursor is not None:\n        actual = returned.stack_cursor.long()\n        if actual != continuation:\n            raise SceneRefreshBoundary(actual, returned, continuation)\n        returned = first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))\n    return returned'}}
EXPECTED_SYNCHRONOUS_SOURCE = {'force': {}, 'services': {'_scene_refresh_frame': "def _scene_refresh_frame(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    if type(memory) is not SceneRefreshMemory:\n        raise ValueError('sealed same-state scene refresh memory required')\n    return memory.frame(frame)", '_scene_refresh_flags': 'def _scene_refresh_flags(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, value, size) -> FirstDeploymentFrame:\n    """MOVE/CLR/TST memory outcomes preserve only the actual observed X."""\n    if size not in (1,2,4):\n        raise ValueError(\'original scene DATA width required\')\n    uint(value,size * 8)\n    sign = 1 << (size * 8 - 1)\n    status = None if frame.status is None else ((frame.status & 16) | (8 if value & sign else 0) | (4 if value == 0 else 0))\n    return memory.sync_status(first_replace(frame,status=status))', '_scene_refresh_emit': 'def _scene_refresh_emit(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, address, size, value) -> FirstDeploymentFrame:\n    memory.sync_status(frame)\n    memory.state.write(address,size,value)\n    return _scene_refresh_flags(memory,frame,value,size)'}}
EXPECTED_PROVIDER_SOURCE = {'_refresh': 'def _refresh(self, memory, frame):\n        self.require_current(memory.state)\n        return (yield from self._forward_scene(GameplaySceneRefreshSession(memory.state, frame)))', '_forward_scene': "def _forward_scene(self, session):\n        current = session.start()\n        try:\n            while type(current) in (GameplaySceneWait, ScriptedSceneWait):\n                self.require_current(self.state)\n                waiting = current\n                returned = (yield waiting)\n                self.require_current(self.state)\n                if type(waiting) is GameplaySceneWait and (not waiting.needs_interrupt):\n                    if returned is not waiting.frame:\n                        raise ValueError('device event cannot replace actual battle Scene frame')\n                    current = session.resume_device(waiting.event)\n                else:\n                    current = session.resume_interrupt(returned, waiting.poll)\n            return _actual_fields(self.state, current)\n        finally:\n            session._program.close()"}
ORIGINAL_REAL_CALLS = ((0xAF48, 0x30A8C), (0x60C, 0x30AA6))


def _dump(node):
    return ast.dump(node, include_attributes=False)


def _code_shape(code):
    return tuple(getattr(code, name) for name in (
        'co_code', 'co_names', 'co_varnames', 'co_argcount', 'co_posonlyargcount',
        'co_kwonlyargcount', 'co_flags', 'co_freevars', 'co_cellvars')) + (tuple(
            _code_shape(value) if type(value) is CodeType else value
            for value in code.co_consts),)


def _top_code(module_code, name):
    found = [value for value in module_code.co_consts if type(value) is CodeType
        and value.co_name == name and value.co_qualname == name]
    if len(found) != 1:
        raise ValueError('one complete top-level shared message owner required: ' + name)
    return found[0]


def _cooperative_module(group, original_tree):
    """Four exact call substitutions, complete FN and source-module inverses."""
    if group not in VIEW_SPECS:
        raise ValueError('only the two finite shared message modules are lifted')
    result = copy.deepcopy(original_tree)
    inverses = {}
    for index, original in enumerate(original_tree.body):
        if not isinstance(original, ast.FunctionDef) or original.name not in VIEW_SPECS[group]:
            continue
        expected = ast.parse(EXPECTED_SOURCE[group][original.name]).body
        if len(expected) != 1 or _dump(original) != _dump(expected[0]):
            raise ValueError('complete shared message source differs: ' + original.name)
        spec = VIEW_SPECS[group][original.name]
        counts = {name: 0 for name in spec}
        replacements = []

        class Lift(ast.NodeTransformer):
            def visit_Call(self, node):
                node = self.generic_visit(node)
                if not isinstance(node.func, ast.Name) or node.func.id not in spec:
                    return node
                counts[node.func.id] += 1
                before = copy.deepcopy(node)
                after = ast.copy_location(ast.YieldFrom(value=node), node)
                replacements.append((before, copy.deepcopy(after)))
                return after

        derived = Lift().visit(copy.deepcopy(original))
        if counts != spec:
            raise ValueError('exact shared message propagation count differs: ' + original.name)
        pending = list(replacements)

        class Inverse(ast.NodeTransformer):
            def visit_YieldFrom(self, node):
                for position, (before, after) in enumerate(pending):
                    if _dump(node) == _dump(after):
                        pending.pop(position)
                        return ast.copy_location(copy.deepcopy(before), node)
                raise ValueError('non-admitted shared message yield-from')

        inverse = Inverse().visit(copy.deepcopy(derived))
        if pending or _dump(inverse) != _dump(original):
            raise ValueError('whole shared message FN inverse differs: ' + original.name)
        result.body[index] = derived
        inverses[index] = inverse
    if len(inverses) != len(VIEW_SPECS[group]):
        raise ValueError('both complete shared message owners are required')
    restored = copy.deepcopy(result)
    for index, inverse in inverses.items():
        restored.body[index] = inverse
    if _dump(restored) != _dump(original_tree):
        raise ValueError('whole shared message source-module inverse differs')
    return ast.fix_missing_locations(result)


class GameplayMessageScenePrograms:
    """Two whole views; the caller retains and forwards the original wait types.

    BattleScenePrograms and reviewed subclasses are explicitly supported. Their
    existing same-Scene source guards remain mandatory, not replaced or relaxed.
    """

    def __init__(self, provider):
        if not isinstance(provider, BattleScenePrograms):
            raise TypeError('an existing same-Scene BattleScenePrograms provider is required')
        provider.require_current(provider.state)
        refresh = provider._refresh
        clear = provider.battle_views['services', 'clear_scene_video_and_state_fields']
        if (refresh.__self__ is not provider or refresh.__func__ is not BattleScenePrograms._refresh
                or type(clear) is not FunctionType or not inspect.isgeneratorfunction(clear)):
            raise ValueError('actual reviewed refresh and full clear providers required')
        provider_module = importlib.import_module(BattleScenePrograms.__module__)
        provider_tree = ast.parse(inspect.getsource(provider_module), filename=provider_module.__file__)
        owner = [node for node in provider_tree.body if isinstance(node, ast.ClassDef) and node.name == 'BattleScenePrograms']
        if len(owner) != 1:
            raise ValueError('complete actual BattleScenePrograms source owner required')
        class_code = _top_code(compile(provider_tree, provider_module.__file__, 'exec', dont_inherit=True), 'BattleScenePrograms')
        self.provider_methods = {}
        for name, source in EXPECTED_PROVIDER_SOURCE.items():
            nodes = [node for node in owner[0].body if isinstance(node, ast.FunctionDef) and node.name == name]
            method = getattr(provider, name)
            expected_code = [code for code in class_code.co_consts if type(code) is CodeType
                and code.co_name == name and code.co_qualname == 'BattleScenePrograms.' + name]
            if (len(nodes) != 1 or _dump(nodes[0]) != _dump(ast.parse(source).body[0])
                    or len(expected_code) != 1 or method.__self__ is not provider
                    or method.__func__ is not getattr(BattleScenePrograms, name)
                    or _code_shape(method.__func__.__code__) != _code_shape(expected_code[0])):
                raise ValueError('actual original complete Scene provider method required: ' + name)
            self.provider_methods[name] = (method.__func__, method.__func__.__code__)
        self.provider = provider
        self.state = provider.state
        self.refresh_function = refresh.__func__
        self.refresh_code = refresh.__func__.__code__
        self.clear_view = clear
        self.clear_code = clear.__code__
        self.modules = {group: importlib.import_module(path) for group, path in MODULE_PATHS.items()}
        self.originals, self.codes, self.views, self.namespaces = {}, {}, {}, {}
        for group, module in self.modules.items():
            tree = ast.parse(inspect.getsource(module), filename=module.__file__)
            plain = compile(tree, module.__file__, 'exec', dont_inherit=True)
            expected = dict(EXPECTED_SYNCHRONOUS_SOURCE.get(group, {}))
            expected.update(EXPECTED_SOURCE[group])
            for name, text in expected.items():
                nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
                original = getattr(module, name)
                if (len(nodes) != 1 or _dump(nodes[0]) != _dump(ast.parse(text).body[0])
                        or type(original) is not FunctionType or original.__globals__ is not vars(module)
                        or original.__module__ != module.__name__ or original.__name__ != name
                        or original.__closure__ is not None or original.__code__.co_freevars
                        or _code_shape(_top_code(plain, name)) != _code_shape(original.__code__)):
                    raise ValueError('actual complete unwrapped shared message owner required: ' + name)
                self.originals[group, name], self.codes[group, name] = original, original.__code__
            derived = compile(_cooperative_module(group, tree), module.__file__, 'exec', dont_inherit=True)
            namespace = self.namespaces[group] = dict(vars(module))
            for name in VIEW_SPECS[group]:
                original = self.originals[group, name]
                view = FunctionType(_top_code(derived, name), namespace, name, original.__defaults__, None)
                view.__kwdefaults__ = original.__kwdefaults__
                view.__annotations__ = dict(original.__annotations__)
                if not inspect.isgeneratorfunction(view) or view.__closure__ is not None:
                    raise ValueError('shared message view must be a complete closure-free generator')
                namespace[name] = self.views[group, name] = view
        for name in ('_scene_refresh_frame', '_scene_refresh_flags', '_scene_refresh_emit'):
            if vars(self.modules['force']).get(name) is not self.originals['services', name]:
                raise ValueError('original shared message imported helper changed: ' + name)
        self.namespaces['force']['_gameplay_message_call_fields'] = self.views['services', '_gameplay_message_call_fields']
        self.namespaces['services']['refresh_gameplay_scene_fields'] = refresh
        self.namespaces['services']['clear_scene_video_and_state_fields'] = clear
        self.view_owners = dict(self.views)
        self.view_codes = {key: view.__code__ for key, view in self.views.items()}
        keys = tuple(self.views) + (
            ('force', '_gameplay_message_call_fields'), ('services', 'refresh_gameplay_scene_fields'),
            ('services', 'clear_scene_video_and_state_fields'))
        self.bindings = {(group, name): self.namespaces[group][name] for group, name in keys}

    def require_current(self, state):
        self.provider.require_current(state)
        for name, (function, code) in self.provider_methods.items():
            method = getattr(self.provider, name)
            if method.__self__ is not self.provider or method.__func__ is not function or function.__code__ is not code:
                raise ValueError('actual shared message provider method changed: ' + name)
        refresh = self.provider._refresh
        if (state is not self.state or refresh.__self__ is not self.provider
                or refresh.__func__ is not self.refresh_function or refresh.__func__.__code__ is not self.refresh_code
                or self.provider.battle_views['services', 'clear_scene_video_and_state_fields'] is not self.clear_view
                or self.clear_view.__code__ is not self.clear_code):
            raise ValueError('actual shared message Scene/provider identity changed')
        for (group, name), original in self.originals.items():
            if getattr(self.modules[group], name) is not original or original.__code__ is not self.codes[group, name]:
                raise ValueError('actual shared message source changed: ' + name)
        for name in ('_scene_refresh_frame', '_scene_refresh_flags', '_scene_refresh_emit'):
            if vars(self.modules['force']).get(name) is not self.originals['services', name]:
                raise ValueError('actual shared message imported helper changed: ' + name)
        if self.views.keys() != self.view_owners.keys():
            raise ValueError('complete shared message view set changed')
        for key, view in self.view_owners.items():
            if self.views[key] is not view or view.__code__ is not self.view_codes[key]:
                raise ValueError('complete shared message view changed: ' + key[1])
        for (group, name), value in self.bindings.items():
            if self.namespaces[group].get(name) is not value:
                raise ValueError('private shared message binding changed: ' + name)

    def program(self, memory, frame):
        """Forward actual IRQ/device waits; no additional CALL or legacy adapter."""
        self.require_current(memory.state)
        program = self.views['force', 'force_turn_message_program'](memory, frame)
        first, received = True, None
        try:
            while True:
                self.require_current(memory.state)
                try:
                    waiting = next(program) if first else program.send(received)
                except StopIteration as finished:
                    return finished.value
                first = False
                received = yield waiting
        finally:
            program.close()
