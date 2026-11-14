"""Persistent controller configuration and new-game menu device continuations.

The menu rules remain in their original four complete source owners. Private
whole-function views propagate seventeen calls to the existing video/sound
services, without replacing public business functions or replaying a prefix.
"""
import ast
import copy
import importlib
import inspect
import threading
from types import CodeType, FunctionType

from .battle_trigger_steps import BattleScenePrograms
from .scene_load_steps import GameplaySceneWait
from ..high_level_main_flows.business_movement_support import _movement_frame
from ..high_level_main_flows.controller_setup_steps import ControllerSetupWait


MODULE_PATHS = {
    'controller': 'tools.high_level_main_flows.controller_setup_steps',
    'support': 'tools.high_level_main_flows.business_scene_support',
    'setup': 'tools.high_level_main_flows.business_gameplay',
}
VIEW_SPECS = {
    'controller': {'controller_setup_program': {
        '_controller_setup_begin_fields': (2, '_controller_menu_begin'),
        '_setup_call_fields': (4, '_controller_menu_call'),
        '_controller_setup_main_iteration_fields': (1, '_controller_menu_iteration'),
    }},
    'support': {
        '_controller_setup_begin_fields': {'_setup_call_fields': (3, '_controller_menu_call')},
        '_controller_setup_main_iteration_fields': {'_setup_call_fields': (4, '_controller_menu_call')},
    },
    'setup': {'_setup_call_fields': {
        'clear_video_sprite_plane_fields': (1, '_controller_menu_clear'),
        'initialize_video_registers_and_planes_fields': (1, '_controller_menu_initialize'),
        'enqueue_sound_command_fields': (1, '_controller_menu_sound'),
    }},
}
SERVICE_BINDINGS = {
    '_controller_menu_clear': 'clear_video_sprite_plane_fields',
    '_controller_menu_initialize': 'initialize_video_registers_and_planes_fields',
    '_controller_menu_sound': 'enqueue_sound_command_fields',
}

# These are source contracts, not a second implementation or executable oracle.
# Comments/docstrings are excluded; every statement, signature and return type
# is compared with the actual sole business owner before a view is constructed.
EXPECTED_SOURCE = {
    'controller': {
        'controller_setup_program': '''
def controller_setup_program(state: SceneState, frame: FirstDeploymentFrame) -> Generator[ControllerSetupWait, FirstDeploymentFrame, FirstDeploymentFrame]:
    from .business_scene_support import (_resource_cost_frame, _controller_setup_begin_fields,
        _setup_compare_memory_fields, _setup_call_fields, _movement_move, _setup_write_fields,
        _movement_test, _controller_setup_main_iteration_fields)
    frame = _resource_cost_frame(state, frame, 0x305B0)
    frame = _controller_setup_begin_fields(state, frame, False)
    while True:
        frame = yield from _wait_for_setup_irq_steps(state, frame, 0x30648)
        frame = _setup_compare_memory_fields(state, frame, 0x00FF703A, 16)
        if not frame.status & 1:
            break
        frame = _setup_call_fields(state, frame, 0x306EE, 0x3065E)
        frame = _setup_call_fields(state, frame, 0x30696, 0x30664)
        frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF603, 1), 8)
        frame = _movement_move(state, frame, 'target_x', low8(frame.target_x) & 32, 8)
        if not frame.status & 4:
            frame = _setup_write_fields(state, frame, 0x00FF703E, 1)
            frame = _movement_move(state, frame, 'target_x', 0xAC, 8)
            frame = _setup_call_fields(state, frame, 0x808A, 0x30684)
        frame = _movement_test(state, frame, state.read(0x00FF703E, 2), 16)
        if not frame.status & 4:
            frame = _setup_call_fields(state, frame, 0x3071A, 0x30692)
    frame = _controller_setup_begin_fields(state, frame, True)
    while True:
        frame = yield from _wait_for_setup_irq_steps(state, frame, 0x2AB6C)
        frame, finished = _controller_setup_main_iteration_fields(state, frame)
        if finished:
            return frame
''',
        '_wait_for_setup_irq_steps': '''
def _wait_for_setup_irq_steps(state: SceneState, frame: FirstDeploymentFrame, poll: int) -> Generator[ControllerSetupWait, FirstDeploymentFrame, FirstDeploymentFrame]:
    from .business_scene_support import _setup_write_fields, _movement_test
    if poll not in (0x30648, 0x2AB6C):
        raise ValueError('actual controller/main-menu IRQ poll required')
    frame = _setup_write_fields(state, frame, 0xFFFFF612, 0x800)
    while True:
        frame = _movement_test(state, frame, state.read(0xFFFFF612, 1), 8)
        if frame.status & 4:
            return frame
        frame = yield ControllerSetupWait(state, frame, poll).validate()
        _movement_frame(state, frame)
''',
    },
    'support': {
        '_controller_setup_begin_fields': '''
def _controller_setup_begin_fields(state: SceneState, frame: FirstDeploymentFrame, main_menu: bool) -> FirstDeploymentFrame:
    if type(main_menu) is not bool: raise ValueError('actual setup phase selector required')
    frame = _controller_setup_interrupt_status_fields(state, frame, 0x2700)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF606, 2), 16)
    frame = _movement_move(state, frame, 'target_x', low8(frame.target_x) & 0xBF, 8)
    frame = _setup_write_fields(state, frame, 0x00C00004, low16(frame.target_x))
    frame = _setup_write_fields(state, frame, 0xFFFFF612, 0, clear=True)
    for target, token in ((0x68CE, 0x2AAEA if main_menu else 0x305CC), (0x6826, 0x2AAF0 if main_menu else 0x305D2)):
        frame = _setup_call_fields(state, frame, target, token)
    frame = _setup_write_fields(state, frame, 0x00FF7036, 0 if main_menu else 1, clear=main_menu)
    frame = _setup_call_fields(state, frame, 0x2B15E, 0x2AAFA if main_menu else 0x305DE)
    counters = (0x00FF7022, 0x00FF7040, 0x00FF7042, 0x00FF703E) if main_menu else (0x00FF7038, 0x00FF703A, 0x00FF703E)
    for address in counters: frame = _setup_write_fields(state, frame, address, 0, clear=True)
    frame = _setup_call_fields(state, frame, 0x2AFB8 if main_menu else 0x306EE, 0x2AB18 if main_menu else 0x305F4)
    frame = _controller_setup_fill_descriptor_fields(state, frame, 0xA200 if main_menu else 0xA0C0, 0x2AAA6 if main_menu else 0x2AA90)
    return _controller_setup_interrupt_status_fields(state, frame, 0x2500)
''',
        '_controller_setup_main_iteration_fields': "\ndef _controller_setup_main_iteration_fields(state: SceneState, frame: FirstDeploymentFrame) -> tuple:\n    frame=_setup_call_fields(state,frame,0x2AFB8,0x2AB76)\n    frame=_setup_call_fields(state,frame,0x2AFE6,0x2AB7C)\n    frame=_movement_test(state,frame,state.read(0x00FF703E,2),16)\n    if not frame.status&4:\n        frame=_setup_compare_memory_fields(state,frame,0x00FF7042,16)\n        return frame,not bool(frame.status&1)\n    # Keep the original302C2 display-before30088-update CALL order and return slots.\n    for target,token in ((0x302C2,0x2AB8C),(0x2AD5A,0x2AB92),(0x2AD88,0x2AB98),\n            (0x2ADB8,0x2AB9E),(0x2ADE8,0x2ABA4),(0x2AE18,0x2ABAA),(0x30088,0x2ABB0)):\n        frame=_setup_call_fields(state,frame,target,token)\n    frame=_movement_test(state,frame,state.read(0x00FF7034,2),16)\n    copy_player=False\n    if not frame.status&4:\n        frame=_setup_compare_memory_fields(state,frame,0x00FF7034,1)\n        if frame.status&4:\n            frame=_setup_compare_memory_fields(state,frame,0x00FF7022,5)\n            copy_player=bool(frame.status&4)\n        else:\n            frame=_setup_compare_memory_fields(state,frame,0x00FF7022,6)\n            copy_player=bool(frame.status&4)\n            if not copy_player:\n                frame=_setup_compare_memory_fields(state,frame,0x00FF7022,5)\n                copy_player=bool(frame.status&4)\n    if copy_player:\n        frame=_setup_write_fields(state,frame,0xFFFFF603,state.read(0xFFFFF605,1),1)\n    frame=_map_presentation_bit_fields(state,frame,state.read(0xFFFFF603,1),32)\n    check_exit=False\n    if not frame.status&4:\n        frame=_movement_move(state,frame,'target_x',0xAC,8)\n        frame=_setup_call_fields(state,frame,0x808A,0x2AC08)\n        frame=_controller_setup_last_button_fields(state,frame)\n        frame=_movement_compare(state,frame,frame.target_x&65535,state.read(0x00FF7022,2),16)\n        if frame.status&4:\n            # Original BEQ2AC30 reaches the F703E store at2AD42.\n            frame=_setup_write_fields(state,frame,0x00FF703E,1)\n            check_exit=True\n        else:\n            frame=_movement_compare(state,frame,frame.target_y&65535,state.read(0x00FF7022,2),16)\n            if frame.status&4:\n                frame=_controller_setup_interrupt_status_fields(state,frame,0x2700)\n                frame=_controller_setup_fill_descriptor_fields(state,frame,0xA1C0,0x2AABE)\n                frame=_controller_setup_interrupt_status_fields(state,frame,0x2500)\n            frame=_setup_change_word_fields(state,frame,0x00FF7022,1)\n    else:\n        frame=_map_presentation_bit_fields(state,frame,state.read(0xFFFFF603,1),16)\n        if not frame.status&4:\n            frame=_controller_setup_last_button_fields(state,frame,True)\n            frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0x00FF7022,2),16)\n            if frame.status&4:\n                frame=_setup_write_fields(state,frame,0x00FF7022,0,clear=True)\n                frame=_controller_setup_interrupt_status_fields(state,frame,0x2700)\n                frame=_controller_setup_fill_descriptor_fields(state,frame,0xA200,0x2AAA6)\n                frame=_controller_setup_interrupt_status_fields(state,frame,0x2500)\n            else:\n                frame=_movement_test(state,frame,state.read(0x00FF7022,2),16)\n                if not frame.status&4:frame=_setup_change_word_fields(state,frame,0x00FF7022,1,True)\n    if not check_exit:\n        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF603,1),8)\n        frame=_movement_move(state,frame,'target_x',low8(frame.target_x)&128,8)\n        if not frame.status&4:frame=_setup_write_fields(state,frame,0x00FF703E,1)\n    frame=_setup_compare_memory_fields(state,frame,0x00FF7042,16)\n    return frame,not bool(frame.status&1)\n",
    },
    'setup': {
        '_setup_call_fields': '''
def _setup_call_fields(state: SceneState, frame: FirstDeploymentFrame, target: Long, continuation: Long) -> FirstDeploymentFrame:
    frame = _resource_cost_frame(state, frame, target)
    stack = frame.stack_cursor.advance(-4); stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    if target == 0xAC08:
        result = append_live_command_sprite_fields(SpritePacketMemory(state), entered, reset_scroll=True, initialize_clip=True)
    elif target == 0xDEA6:
        result = darken_palette_fields(SceneRefreshMemory(state), entered)
    elif target == 0x68CE:
        result = clear_video_sprite_plane_fields(SceneRefreshMemory(state), entered)
    elif target == 0x6826:
        result = initialize_video_registers_and_planes_fields(SceneRefreshMemory(state), entered)
    elif target == 0x808A:
        result = enqueue_sound_command_fields(SceneRefreshMemory(state), entered)
    elif target == 0x2B01A:
        result = cycle_setup_option_fields(state, entered)
    elif target == 0x2AF8A:
        result = render_current_setup_option_fields(state, entered)
    elif target in (0x2B3C4, 0x2B3D4, 0x2B430):
        result = _setup_plane_rows_fields(state, entered, target)
    elif target == 0x2B446:
        result = write_setup_video_address_fields(state, entered)
    elif target in (0x2AD5A, 0x2AD88, 0x2ADB8, 0x2ADE8, 0x2AE18, 0x2AFB8, 0x2AFE6, 0x2B15E):
        children = {0x2AD5A: update_first_setup_option_fields, 0x2AD88: update_second_setup_option_fields,
            0x2ADB8: update_third_setup_option_fields, 0x2ADE8: update_fourth_setup_option_fields,
            0x2AE18: update_setup_player_choices_fields, 0x2AFB8: advance_setup_reveal_fields,
            0x2AFE6: advance_setup_dismissal_fields, 0x2B15E: initialize_setup_video_fields}
        result = children[target](state, entered)
    else:
        from .business_scene_support import _controller_setup_child_fields
        result = _controller_setup_child_fields(state, entered, target)
    result = _resource_cost_frame(state, result, target)
    token = result.stack_cursor.long()
    if token != continuation:
        raise MovementContinuationBoundary(token, result, 'actual setup child return LONG changed')
    state.sr = (state.sr & 65504) | result.status
    return first_replace(result, stack_cursor=result.stack_cursor.advance(4))
''',
    },
}


def _dump(node):
    return ast.dump(node, include_attributes=False)


def _without_docstring(node):
    result = copy.deepcopy(node)
    if (result.body and isinstance(result.body[0], ast.Expr)
            and isinstance(result.body[0].value, ast.Constant)
            and isinstance(result.body[0].value.value, str)):
        result.body.pop(0)
    return result


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
        raise ValueError('one complete top-level controller-menu owner required: ' + name)
    return found[0]


def _cooperative_module(group, original_tree):
    """Only declared CALLs and their local import aliases change; inverse all."""
    result = copy.deepcopy(original_tree)
    restored = copy.deepcopy(original_tree)
    changed = 0
    for index, original in enumerate(original_tree.body):
        if not isinstance(original, ast.FunctionDef) or original.name not in VIEW_SPECS[group]:
            continue
        spec = VIEW_SPECS[group][original.name]
        counts = {name: 0 for name in spec}
        calls, imports = [], []

        class Lift(ast.NodeTransformer):
            def visit_ImportFrom(self, node):
                before = copy.deepcopy(node)
                retained = []
                for item in node.names:
                    if item.name in spec:
                        if group != 'controller' or node.level != 1 or node.module != 'business_scene_support' or item.asname is not None:
                            raise ValueError('only original local setup imports may be renamed')
                        # A renamed import would still bind the old synchronous
                        # callable and shadow the private generator global.
                        # Remove exactly these three local bindings instead.
                    else:
                        retained.append(item)
                node.names = retained
                if _dump(before) != _dump(node):
                    imports.append((before, copy.deepcopy(node)))
                return node

            def visit_Call(self, node):
                node = self.generic_visit(node)
                if not isinstance(node.func, ast.Name) or node.func.id not in spec:
                    return node
                name = node.func.id
                before = copy.deepcopy(node)
                counts[name] += 1
                node.func.id = spec[name][1]
                after = ast.copy_location(ast.YieldFrom(value=node), node)
                calls.append((before, copy.deepcopy(after)))
                return after

        derived = Lift().visit(copy.deepcopy(original))
        if counts != {name: value[0] for name, value in spec.items()}:
            raise ValueError('exact whole controller-menu propagation count changed: ' + original.name)
        if len(imports) != (1 if group == 'controller' else 0):
            raise ValueError('complete controller local-import shape changed')
        pending_calls, pending_imports = list(calls), list(imports)

        class Inverse(ast.NodeTransformer):
            def visit_ImportFrom(self, node):
                for position, (before, after) in enumerate(pending_imports):
                    if _dump(node) == _dump(after):
                        pending_imports.pop(position)
                        return copy.deepcopy(before)
                return node

            def visit_YieldFrom(self, node):
                for position, (before, after) in enumerate(pending_calls):
                    if _dump(node) == _dump(after):
                        pending_calls.pop(position)
                        return ast.copy_location(copy.deepcopy(before), node)
                # The two original IRQ yield-from expressions are not new.
                return self.generic_visit(node)

        inverse = Inverse().visit(copy.deepcopy(derived))
        if pending_calls or pending_imports or _dump(inverse) != _dump(original):
            raise ValueError('whole controller-menu function inverse differs: ' + original.name)
        result.body[index] = derived
        restored.body[index] = inverse
        changed += 1
    if changed != len(VIEW_SPECS[group]) or _dump(restored) != _dump(original_tree):
        raise ValueError('whole controller-menu source-module inverse differs: ' + group)
    return ast.fix_missing_locations(result)


class ControllerMenuPrograms:
    """Four same-Scene whole views; no new machine, media or outer CALL slot.

    The owning CampaignMenuScenePrograms retains the real 305B0/528 caller.
    This object has no scheduler or device outcome, and cannot be re-entered.
    """

    def __init__(self, scene_programs):
        if not isinstance(scene_programs, BattleScenePrograms):
            raise TypeError('the existing same-Scene BattleScenePrograms provider is required')
        scene_programs.require_current(scene_programs.state)
        self.provider = scene_programs
        self.state = scene_programs.state
        self._thread = threading.get_ident()
        self._started = False
        self.modules = {group: importlib.import_module(path) for group, path in MODULE_PATHS.items()}
        self.originals, self.codes, self.views, self.namespaces = {}, {}, {}, {}
        self.service_views = {}
        for alias, name in SERVICE_BINDINGS.items():
            key = ('services', name)
            view = scene_programs.battle_views[key]
            if (view is not scene_programs._battle_view_owners[key]
                    or view.__code__ is not scene_programs._battle_view_codes[key]
                    or type(view) is not FunctionType or not inspect.isgeneratorfunction(view)):
                raise ValueError('the actual existing cooperative menu device service is required: ' + name)
            self.service_views[alias] = (view, view.__code__)
        for group, module in self.modules.items():
            tree = ast.parse(inspect.getsource(module), filename=module.__file__)
            plain = compile(tree, module.__file__, 'exec', dont_inherit=True)
            nodes = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
            for name, expected in EXPECTED_SOURCE[group].items():
                original = getattr(module, name)
                if (name not in nodes or _dump(_without_docstring(nodes[name])) != _dump(ast.parse(expected).body[0])
                        or type(original) is not FunctionType or original.__globals__ is not vars(module)
                        or original.__module__ != module.__name__ or original.__name__ != name
                        or original.__closure__ is not None or original.__code__.co_freevars
                        or _code_shape(original.__code__) != _code_shape(_top_code(plain, name))):
                    raise ValueError('actual complete unwrapped menu source owner required: ' + name)
                self.originals[group, name], self.codes[group, name] = original, original.__code__
            derived = compile(_cooperative_module(group, tree), module.__file__, 'exec', dont_inherit=True)
            namespace = self.namespaces[group] = dict(vars(module))
            for name in VIEW_SPECS[group]:
                original = self.originals[group, name]
                view = FunctionType(_top_code(derived, name), namespace, name, original.__defaults__, None)
                view.__kwdefaults__ = original.__kwdefaults__
                view.__annotations__ = dict(original.__annotations__)
                if not inspect.isgeneratorfunction(view):
                    raise ValueError('every complete controller-menu view must be a genuine generator')
                self.views[group, name] = view
        if self.modules['support']._setup_call_fields is not self.originals['setup', '_setup_call_fields']:
            raise ValueError('original setup CALL import must name its sole full-frame owner')
        if self.modules['controller'].ControllerSetupWait is not ControllerSetupWait:
            raise ValueError('the existing exact controller IRQ wait class is required')
        aliases = {
            '_controller_menu_begin': self.views['support', '_controller_setup_begin_fields'],
            '_controller_menu_iteration': self.views['support', '_controller_setup_main_iteration_fields'],
            '_controller_menu_call': self.views['setup', '_setup_call_fields'],
        }
        aliases.update({name: pair[0] for name, pair in self.service_views.items()})
        self.bindings = {}
        for group, namespace in self.namespaces.items():
            for name, value in aliases.items():
                if name in namespace:
                    raise ValueError('private menu alias must not replace an original source name')
                namespace[name] = value
                self.bindings[group, name] = value
        self.view_owners = dict(self.views)
        self.view_codes = {key: view.__code__ for key, view in self.views.items()}

    def require_current(self, state):
        """Check this child only: do not recurse through the owning provider."""
        if (state is not self.state or self.provider.state is not state
                or threading.get_ident() != self._thread):
            raise ValueError('the actual same-Scene controller invocation/thread is required')
        for (group, name), original in self.originals.items():
            if getattr(self.modules[group], name) is not original or original.__code__ is not self.codes[group, name]:
                raise ValueError('actual controller-menu source changed while suspended: ' + name)
        if (self.modules['support']._setup_call_fields is not self.originals['setup', '_setup_call_fields']
                or self.modules['controller'].ControllerSetupWait is not ControllerSetupWait):
            raise ValueError('original controller CALL/wait bindings changed')
        if self.views.keys() != self.view_owners.keys():
            raise ValueError('the complete finite controller-menu view set changed')
        for key, view in self.view_owners.items():
            if self.views[key] is not view or view.__code__ is not self.view_codes[key]:
                raise ValueError('actual whole controller-menu continuation changed: ' + key[1])
        for alias, (view, code) in self.service_views.items():
            if (self.provider.battle_views['services', SERVICE_BINDINGS[alias]] is not view
                    or view.__code__ is not code):
                raise ValueError('actual same-provider menu device continuation changed')
        for (group, name), value in self.bindings.items():
            if self.namespaces[group].get(name) is not value:
                raise ValueError('private controller-menu whole-view binding changed: ' + name)

    def program(self, state, frame):
        """Forward real IRQ/device waits; never synthesize an ACK or pop528."""
        self.require_current(state)
        if self._started:
            raise ValueError('cannot replay controller/main-menu initialization prefix')
        self._started = True
        frame = _movement_frame(state, frame)
        entry_sp = frame.stack_cursor.base
        if frame.status != state.sr & 31:
            raise ValueError('actual menu entry frame and full Scene SR disagree')
        program = self.views['controller', 'controller_setup_program'](state, frame)
        first, received = True, None
        try:
            while True:
                self.require_current(state)
                try:
                    waiting = next(program) if first else program.send(received)
                except StopIteration as finished:
                    result = _movement_frame(state, finished.value)
                    if result.stack_cursor.base != entry_sp or result.status != state.sr & 31:
                        raise ValueError('whole controller/menu return must preserve incoming CALL/SR')
                    return result
                first = False
                if type(waiting) not in (ControllerSetupWait, GameplaySceneWait) or waiting.state is not state:
                    raise ValueError('actual same-Scene controller IRQ or existing device wait required')
                waiting.validate()
                status_word = state.sr
                received = yield waiting
                self.require_current(state)
                received = _movement_frame(state, received)
                if (received.stack_cursor.base != waiting.frame.stack_cursor.base
                        or state.sr != status_word or received.status != status_word & 31):
                    raise ValueError('real menu wait continuation must preserve physical SP/full SR')
                if type(waiting) is GameplaySceneWait and not waiting.needs_interrupt and received is not waiting.frame:
                    raise ValueError('real device progress cannot replace the retained menu frame')
        finally:
            program.close()
