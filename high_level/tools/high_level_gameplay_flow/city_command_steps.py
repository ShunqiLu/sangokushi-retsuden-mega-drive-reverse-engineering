"""Actual Main434 command parent using the existing complete force continuations.

DF6E's E010 and selected-category branches are tails, not synthetic calls.
The two complete original parents only gain cooperative060C tails; their
existing complete cooperative force bindings use the already-restored strategy
views. No old public/private view dictionary or original module is rewritten.
"""
import ast
import copy
import inspect
from types import CodeType, FunctionType

from . import strategy_steps, message_scene_steps
from .strategy_steps import StrategicScenePrograms
from .battle_trigger_steps import _dump, _code_shape, _top_code
from .contexts_services import SceneRefreshMemory
from .compiler_strategy_steps import EXPECTED_MODULE_AST as STRATEGY_SOURCE_AST
from .compiler_message_scene_steps import EXPECTED_MODULE_AST as MESSAGE_SOURCE_AST
from ..high_level_main_flows import command_message_steps
from ..high_level_main_flows.command_message_steps import _cooperative_tree as _base_cooperative_tree
from ..high_level_main_flows.compiler_command_message_steps import (
    EXPECTED_MODULE_AST as COMMAND_SOURCE_AST, EXPECTED_OWNER_ASTS)
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary


MAIN_ENTRY = 0x434
CAMPAIGN_PAIR = (0xDF6E, 0x8E4)
COMMAND_MODULE = 'tools.high_level_main_flows.business_commands'
PARENT_NAMES = ('draw_diplomacy_parameter_panel_frame_fields',
    '_diplomacy_selected_category_fields')
FORCE_NAMES = ('_diplomacy_first_force_turn_fields',
    '_diplomacy_second_force_turn_fields')


def _pin_registered_source(module, expected_ast):
    """Reuse exact existing registries and pin loaded local functions/methods."""
    tree = ast.parse(inspect.getsource(module), filename=module.__file__)
    if _dump(tree) != expected_ast:
        raise ValueError('complete registered city-command provider source required')
    plain = compile(tree, module.__file__, 'exec', dont_inherit=True)
    bindings = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            owner = getattr(module, node.name)
            if (type(owner) is not FunctionType or owner.__globals__ is not vars(module)
                    or owner.__module__ != module.__name__ or owner.__name__ != node.name
                    or owner.__closure__ is not None or owner.__code__.co_freevars
                    or _code_shape(owner.__code__) != _code_shape(_top_code(plain, node.name))):
                raise ValueError('actual registered city-command function required: ' + node.name)
            bindings.append((module, node.name, owner, owner.__code__))
        elif isinstance(node, ast.ClassDef):
            cls = getattr(module, node.name)
            if type(cls) is not type or cls.__module__ != module.__name__ or cls.__name__ != node.name:
                raise ValueError('actual registered city-command provider class required')
            bindings.append((module, node.name, cls, None))
            class_code = _top_code(plain, node.name)
            for member in node.body:
                if not isinstance(member, ast.FunctionDef):
                    continue
                owner = vars(cls).get(member.name)
                codes = [code for code in class_code.co_consts if type(code) is CodeType
                    and code.co_name == member.name and code.co_qualname == node.name + '.' + member.name]
                if (member.decorator_list or len(codes) != 1 or type(owner) is not FunctionType
                        or owner.__globals__ is not vars(module) or owner.__module__ != module.__name__
                        or owner.__qualname__ != node.name + '.' + member.name
                        or _code_shape(owner.__code__) != _code_shape(codes[0])):
                    raise ValueError('actual registered city-command method required: ' + member.name)
                # The existing Strategic methods use real zero-argument super.
                # Only its exact compiler-created __class__ cell is admitted.
                if owner.__code__.co_freevars == ('__class__',):
                    if owner.__closure__ is None or len(owner.__closure__) != 1 or owner.__closure__[0].cell_contents is not cls:
                        raise ValueError('actual registered provider __class__ cell required')
                elif owner.__code__.co_freevars or owner.__closure__ is not None:
                    raise ValueError('no other city-command provider closure admitted')
                bindings.append((cls, member.name, owner, owner.__code__))
    return tuple(bindings)


def _city_command_module(original_tree):
    """Two whole parent/module inverses, on top of the existing exact views."""
    result = copy.deepcopy(original_tree)
    restored = copy.deepcopy(original_tree)
    selected = []
    for index, original in enumerate(original_tree.body):
        if not isinstance(original, ast.FunctionDef) or original.name not in PARENT_NAMES:
            continue
        if _dump(original) != EXPECTED_OWNER_ASTS['commands'][original.name]:
            raise ValueError('complete original city-command parent source required: ' + original.name)
        # This exact utility proves all previous CALL propagation invertible;
        # its registered body and source ownership are retained, not copied.
        previous, _ = _base_cooperative_tree('commands', original)
        replacements = []

        class LiftTail(ast.NodeTransformer):
            def visit_Call(self, node):
                node = self.generic_visit(node)
                if not isinstance(node.func, ast.Name) or node.func.id != 'display_child_fields':
                    return node
                if (node.keywords or len(node.args) != 3
                        or not isinstance(node.args[2], ast.Constant) or node.args[2].value != 0x60C):
                    raise ValueError('only the actual original JMP060C tail may be lifted')
                before = copy.deepcopy(node)
                node.func.id = '_city_command_clear_tail'
                after = ast.copy_location(ast.YieldFrom(value=node), node)
                replacements.append((before, copy.deepcopy(after)))
                return after

        changed = LiftTail().visit(copy.deepcopy(previous))
        if len(replacements) != 1:
            raise ValueError('one original JMP060C tail required in each whole parent')
        before, after = replacements[0]
        inversions = []

        class InverseTail(ast.NodeTransformer):
            def visit_YieldFrom(self, node):
                if _dump(node) == _dump(after):
                    inversions.append(True)
                    return copy.deepcopy(before)
                return self.generic_visit(node)

        inverse = InverseTail().visit(copy.deepcopy(changed))
        if len(inversions) != 1 or _dump(inverse) != _dump(previous):
            raise ValueError('whole existing command-parent view inverse differs')
        result.body[index] = changed
        # _base_cooperative_tree already proves previous -> original exactly.
        restored.body[index] = copy.deepcopy(original)
        selected.append(original.name)
    if tuple(selected) != tuple(name for name in (
            '_diplomacy_selected_category_fields', 'draw_diplomacy_parameter_panel_frame_fields')):
        raise ValueError('the two actual complete command parents must occur once')
    if _dump(restored) != _dump(original_tree):
        raise ValueError('complete original business module inverse differs')
    # Check the complete transformed module after undoing only the two tails
    # and the already-proven existing propagation, not a selected body fragment.
    whole_inverse = copy.deepcopy(result)
    for index, original in enumerate(original_tree.body):
        if isinstance(original, ast.FunctionDef) and original.name in PARENT_NAMES:
            whole_inverse.body[index] = copy.deepcopy(original)
    if _dump(whole_inverse) != _dump(original_tree):
        raise ValueError('complete city-command module inverse differs')
    return ast.fix_missing_locations(result)


class CityCommandScenePrograms(StrategicScenePrograms):
    """Main434's real DF6E parent, with no extra CALL on force/clear tails."""

    def __init__(self, state):
        super().__init__(state)
        self.command_registered = (
            _pin_registered_source(strategy_steps, STRATEGY_SOURCE_AST)
            + _pin_registered_source(command_message_steps, COMMAND_SOURCE_AST)
            + _pin_registered_source(message_scene_steps, MESSAGE_SOURCE_AST))
        module = self.modules['commands']
        if module.__name__ != COMMAND_MODULE:
            raise ValueError('actual complete city-command business module required')
        tree = ast.parse(inspect.getsource(module), filename=module.__file__)
        plain = compile(tree, module.__file__, 'exec', dont_inherit=True)
        derived = compile(_city_command_module(tree), module.__file__, 'exec', dont_inherit=True)
        self.command_module = module
        self.command_originals = {}
        self.command_codes = {}
        namespace = dict(vars(module))
        self.command_namespace = namespace
        self.command_views = {}
        for name in PARENT_NAMES:
            original = self.originals['commands', name]
            if (getattr(module, name) is not original or type(original) is not FunctionType
                    or original.__globals__ is not vars(module) or original.__closure__ is not None
                    or original.__code__.co_freevars
                    or _code_shape(_top_code(plain, name)) != _code_shape(original.__code__)):
                raise ValueError('actual complete original city-command parent required: ' + name)
            self.command_originals[name] = original
            self.command_codes[name] = original.__code__
            view = FunctionType(_top_code(derived, name), namespace, name, original.__defaults__, None)
            view.__kwdefaults__ = original.__kwdefaults__
            view.__annotations__ = dict(original.__annotations__)
            if not inspect.isgeneratorfunction(view) or view.__closure__ is not None:
                raise ValueError('complete city-command parent generator required')
            namespace[name] = self.command_views[name] = view
        namespace['display_call_fields'] = self.views['display', 'display_call_fields']
        namespace['_city_command_clear_tail'] = self._clear_tail
        namespace['draw_diplomacy_parameter_panel_alternate_2_frame_fields'] = self.views[
            'commands', 'draw_diplomacy_parameter_panel_alternate_2_frame_fields']
        for name in FORCE_NAMES:
            namespace[name] = self.strategy_views['commands', name]
        self.command_view_owners = dict(self.command_views)
        self.command_view_codes = {name: view.__code__ for name, view in self.command_views.items()}
        names = PARENT_NAMES + FORCE_NAMES + ('display_call_fields', '_city_command_clear_tail',
            'draw_diplomacy_parameter_panel_alternate_2_frame_fields')
        self.command_bindings = {name: namespace[name] for name in names}
        self.command_message = self.message_scene
        if (type(self.command_message) is not message_scene_steps.GameplayMessageScenePrograms
                or self.command_message.provider is not self or self.command_message.state is not state):
            raise ValueError('one inherited same-Scene shared message provider required')

    def require_current(self, state):
        super().require_current(state)
        if hasattr(self, 'command_registered'):
            for owner, name, value, code in self.command_registered:
                if getattr(owner, name) is not value or code is not None and value.__code__ is not code:
                    raise ValueError('actual registered city-command provider changed: ' + name)
        if hasattr(self, 'command_originals'):
            for name, original in self.command_originals.items():
                if getattr(self.command_module, name) is not original or original.__code__ is not self.command_codes[name]:
                    raise ValueError('complete original city-command parent changed: ' + name)
        if hasattr(self, 'command_view_owners'):
            if self.command_views.keys() != self.command_view_owners.keys():
                raise ValueError('finite complete city-command view set changed')
            for name, view in self.command_view_owners.items():
                if self.command_views[name] is not view or view.__code__ is not self.command_view_codes[name]:
                    raise ValueError('complete private city-command parent changed: ' + name)
            for name, value in self.command_bindings.items():
                if self.command_namespace.get(name) is not value:
                    raise ValueError('private city-command binding changed: ' + name)
        if hasattr(self, 'command_message'):
            if (self.message_scene is not self.command_message or self.command_message.provider is not self
                    or self.command_message.state is not state):
                raise ValueError('same inherited city-command message instance required')
        # Shared require_current calls its provider. Do not recurse into it here.

    def _clear_tail(self, state, frame, target):
        self.require_current(state)
        if target != 0x60C:
            raise MovementContinuationBoundary(target, frame, 'only the actual command JMP060C tail is admitted')
        # Actual DFF4/E086 JMP inherits the existing8E4 LONG. Do not add/pop one.
        return (yield from self._message_waits(self.battle_views[
            'services', 'clear_scene_video_and_state_fields'](SceneRefreshMemory(state), frame)))

    def _campaign_child(self, state, frame, target, continuation):
        self.require_current(state)
        if target == CAMPAIGN_PAIR[0]:
            if continuation != CAMPAIGN_PAIR[1]:
                raise MovementContinuationBoundary(target, frame, 'city-command DF6E requires its actual8E4 LONG')
            return (yield from self.command_views['draw_diplomacy_parameter_panel_frame_fields'](state, frame))
        return (yield from super()._campaign_child(state, frame, target, continuation))
