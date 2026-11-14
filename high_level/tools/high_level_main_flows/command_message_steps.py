"""Finite cooperative views of the original city-command message parents.

The editable algorithms remain in their existing business owners. Each view
only turns named child calls into yield-from; its complete inverse must equal
the actual loaded owner's complete source. No module callable is rebound.
"""
import ast
import copy
import inspect
import threading
from types import CodeType, FunctionType

from tools.high_level_main_flows.domain import checked_state
from tools.high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
from tools.high_level_scene_flows.source_artifact_cache import get_source_artifacts, read_source_text


# These are complete existing business functions, not instruction fragments.
# The integer for each callable is the exact number of syntactic substitutions.
VIEW_SPECS = {'highbank': {'_command_policy_call_fields': {'_command_policy_child_fields': 1}, '_command_detail_notice_fields': {'_command_policy_call_fields': 1}, '_command_detail_dispatch_menu_fields': {'_command_policy_call_fields': 1}, 'open_assignment_menu_dispatch_fields': {'_command_policy_call_fields': 1}, 'open_city_action_menu_dispatch_fields': {'_command_policy_call_fields': 1}, 'dispatch_city_assignment_phases_fields': {'_command_detail_dispatch_menu_fields': 1}, 'dispatch_city_action_phases_fields': {'_command_detail_dispatch_menu_fields': 1}, 'execute_city_loyalty_change_fields': {'_command_policy_call_fields': 8, '_command_detail_notice_fields': 1}, 'execute_city_training_choice_fields': {'_command_policy_call_fields': 6, '_command_detail_notice_fields': 2}, 'apply_city_training_result_fields': {'_command_policy_call_fields': 3}, 'execute_city_funds_choice_fields': {'_command_policy_call_fields': 5, '_command_detail_notice_fields': 1}, 'allocate_city_random_funds_fields': {'_command_policy_call_fields': 5}, 'show_city_funds_graphic_fields': {'_command_policy_call_fields': 2}, 'execute_city_member_transfer_detail_fields': {'_command_policy_call_fields': 5, '_command_detail_notice_fields': 1}}, 'support': {'_controller_setup_child_fields': {'_city_assignment_child_fields': 1}, '_city_assignment_child_fields': {'open_assignment_menu_dispatch_fields': 1, 'open_city_action_menu_dispatch_fields': 1, 'settle_city_projects_and_refresh_map_fields': 1}, '_city_assignment_vector_fields': {'_setup_call_fields': 1}, 'run_city_command_assignment_fields': {'_setup_call_fields': 7, '_city_assignment_vector_fields': 1}, '_map_packet_call_fields': {'apply_map_packet_supply_losses_fields': 1, 'execute_deployment_menu_fields': 1}, '_map_packet_lost_message_fields': {'_map_packet_call_fields': 1}, 'apply_map_packet_supply_losses_fields': {'_map_packet_call_fields': 2, '_map_packet_lost_message_fields': 1}, 'deduct_all_map_packet_supply_fields': {'_map_packet_call_fields': 2}, 'finish_city_command_assignment_fields': {'_setup_call_fields': 2}}, 'gameplay': {'_setup_call_fields': {'_controller_setup_child_fields': 1}, '_city_project_call_fields': {'execute_deployment_menu_fields': 1}, 'settle_city_projects_and_refresh_map_fields': {'_city_project_call_fields': 6}}, 'display': {'display_call_fields': {'display_child_fields': 1}, 'display_child_fields': {'run_city_command_assignment_fields': 1}}, 'city': {'execute_deployment_menu_fields': {'present_gameplay_message_fields': 1}}, 'commands': {'_campaign_ui_call_fields': {'_campaign_call_fields': 1}, 'draw_command_cost_panel_frame_fields': {'_campaign_ui_call_fields': 7}, 'draw_command_cost_panel_alternate_1_frame_fields': {'draw_command_cost_panel_frame_fields': 1}, '_diplomacy_first_force_turn_fields': {'display_call_fields': 7, '_diplomacy_second_force_turn_fields': 1}, '_diplomacy_second_force_turn_fields': {'display_call_fields': 12}, '_diplomacy_selected_category_fields': {'display_call_fields': 1, '_diplomacy_second_force_turn_fields': 1}, 'draw_diplomacy_parameter_panel_frame_fields': {'display_call_fields': 5, '_diplomacy_selected_category_fields': 3, 'draw_diplomacy_parameter_panel_alternate_2_frame_fields': 1, '_diplomacy_first_force_turn_fields': 1}, 'draw_diplomacy_parameter_panel_alternate_1_frame_fields': {'_diplomacy_first_force_turn_fields': 1}, 'draw_diplomacy_parameter_panel_alternate_2_frame_fields': {'display_call_fields': 3}}, 'main': {'_campaign_call_fields': {'_campaign_known_child_fields': 1}, 'initialize_city_detail_panel_fields': {'_campaign_call_fields': 1}, 'initialize_city_command_panel_fields': {'_campaign_call_fields': 1}, 'initialize_campaign_map_fields': {'_campaign_call_fields': 1}, 'initialize_campaign_audio_scene_fields': {'_campaign_call_fields': 2}}}

COMMAND_ENTRIES = {
    0x3256A: 'dispatch_city_assignment_phases_fields',
    0x33040: 'dispatch_city_action_phases_fields',
    0x32936: 'execute_city_loyalty_change_fields',
    0x32B88: 'execute_city_training_choice_fields',
    0x32CA8: 'apply_city_training_result_fields',
    0x32DCE: 'execute_city_funds_choice_fields',
    0x32EA0: 'allocate_city_random_funds_fields',
    0x32FC6: 'show_city_funds_graphic_fields',
    0x33322: 'execute_city_member_transfer_detail_fields',
}
COMMAND_CALL_PAIRS = frozenset((
    (0x3256A, 0x3101A), (0x33040, 0x31022),
    (0x32936, 0x3257E), (0x32B88, 0x3257E), (0x32DCE, 0x3257E),
    (0x33322, 0x33054), (0x32CA8, 0x32BFC),
    (0x32EA0, 0x32E62), (0x32FC6, 0x32E6A),
))
MESSAGE_RETURNS = frozenset((
    0x329A0, 0x32A2E, 0x32BDE, 0x32C34, 0x32D44,
    0x32E5A, 0x32F04, 0x32F54, 0x3302C, 0x333E4,
))
SETUP_ENTRIES = {
    0x31014: 'open_assignment_menu_dispatch_fields',
    0x3101C: 'open_city_action_menu_dispatch_fields',
}

# Only the existing call-helper's child argument list gains the continuation.
# It is a Python routing operand, never another RAM read or physical CALL.
CHILD_ADAPTERS = {('highbank', '_command_policy_call_fields', '_command_policy_child_fields'): '_command_message_child_program', ('gameplay', '_setup_call_fields', '_controller_setup_child_fields'): '_command_message_setup_child_program', ('display', 'display_call_fields', 'display_child_fields'): '_command_message_display_child_program', ('main', '_campaign_call_fields', '_campaign_known_child_fields'): '_command_message_campaign_child_program', ('support', '_map_packet_call_fields', 'execute_deployment_menu_fields'): '_command_message_extended_deployment_program', ('gameplay', '_city_project_call_fields', 'execute_deployment_menu_fields'): '_command_message_extended_deployment_program'}

LOCAL_IMPORT_ADAPTERS = {('support', '_city_assignment_child_fields', 'open_assignment_menu_dispatch_fields'): '_command_message_open_assignment_program', ('support', '_city_assignment_child_fields', 'open_city_action_menu_dispatch_fields'): '_command_message_open_action_program', ('display', 'display_child_fields', 'run_city_command_assignment_fields'): '_command_message_assignment_program', ('city', 'execute_deployment_menu_fields', 'present_gameplay_message_fields'): '_command_message_scene_program', ('commands', '_campaign_ui_call_fields', '_campaign_call_fields'): '_command_message_campaign_call_program', ('support', '_city_assignment_child_fields', 'settle_city_projects_and_refresh_map_fields'): '_command_message_project_program'}



# The message's physical CALL already belongs to one of these exact callers.
EXTENDED_MESSAGE_RETURNS = frozenset((
    0x3099C, 0x30AF2, 0x30D60, 0x1196E, 0xC984, 0x67048,
))
MAIN_MESSAGE_ENTRIES = {
    0x418: 'initialize_city_detail_panel_fields',
    0x41C: 'initialize_city_command_panel_fields',
    0x434: 'initialize_campaign_map_fields',
    0x4B8: 'initialize_campaign_audio_scene_fields',
}
CAMPAIGN_MESSAGE_CALLS = {
    (0xC8B8, 0x574): 'draw_command_cost_panel_frame_fields',
    (0xCD20, 0x56C): 'draw_command_cost_panel_alternate_1_frame_fields',
    (0xDF6E, 0x8E4): 'draw_diplomacy_parameter_panel_frame_fields',
    (0x6701E, 0x58C): 'draw_diplomacy_parameter_panel_alternate_2_frame_fields',
}

def _dump(node):
    return ast.dump(node, include_attributes=False)


def _require_literal_command_routes(node):
    """Admit only the existing literal routes whose child source is lifted."""
    routes = {}
    for branch in ast.walk(node):
        if not (isinstance(branch, ast.If) and isinstance(branch.test, ast.Compare)
                and isinstance(branch.test.left, ast.Name) and branch.test.left.id == 'target'
                and len(branch.test.ops) == 1 and isinstance(branch.test.ops[0], ast.Eq)
                and isinstance(branch.test.comparators[0], ast.Constant)
                and len(branch.body) == 1 and isinstance(branch.body[0], ast.Return)
                and isinstance(branch.body[0].value, ast.Call)
                and isinstance(branch.body[0].value.func, ast.Name)):
            continue
        address = branch.test.comparators[0].value
        if address in COMMAND_ENTRIES:
            if address in routes:
                raise ValueError('duplicate literal command-parent route')
            routes[address] = branch.body[0].value.func.id
    if routes != COMMAND_ENTRIES:
        raise ValueError('actual finite command-parent route changed')


def _code_shape(code):
    """Structural bytecode identity, not a digest or a native comparison."""
    return tuple(getattr(code, name) for name in (
        'co_code', 'co_names', 'co_varnames', 'co_argcount',
        'co_posonlyargcount', 'co_kwonlyargcount', 'co_flags',
        'co_freevars', 'co_cellvars')) + (tuple(
            _code_shape(value) if type(value) is CodeType else value
            for value in code.co_consts),)


def _current_command_owner(module, name, plain=None):
    original = getattr(module, name)
    if (type(original) is not FunctionType or original.__module__ != module.__name__
            or original.__name__ != name or original.__closure__ is not None
            or inspect.isgeneratorfunction(original)):
        raise ValueError('actual unwrapped finite command owner required: ' + name)
    if plain is not None and _code_shape(original.__code__) != _code_shape(plain):
        raise ValueError('loaded command owner differs from its complete source: ' + name)
    return original


def _loaded_owner(module, name, source_node=None):
    original = _current_command_owner(module, name)
    tree = (ast.parse(inspect.getsource(original)) if source_node is None else
        ast.Module(body=[copy.deepcopy(source_node)], type_ignores=[]))
    if len(tree.body) != 1 or type(tree.body[0]) is not ast.FunctionDef:
        raise ValueError('one complete command function source required: ' + name)
    namespace = dict(original.__globals__)
    exec(compile(tree, '<plain command owner identity>', 'exec', dont_inherit=True), namespace)
    if _code_shape(namespace[name].__code__) != _code_shape(original.__code__):
        raise ValueError('loaded command owner differs from its complete source: ' + name)
    return original, tree.body[0]


def _cooperative_tree(group, original_node):
    """Only named CALL propagation changes; reversing it restores the whole FN."""
    spec = VIEW_SPECS[group][original_node.name]
    if any(isinstance(node, (ast.Yield, ast.YieldFrom, ast.AsyncFunctionDef))
            for node in ast.walk(original_node)):
        raise ValueError('command source is already cooperative')
    substitutions = []

    class Lift(ast.NodeTransformer):
        def visit_Call(self, node):
            node = self.generic_visit(node)
            if not isinstance(node.func, ast.Name) or node.func.id not in spec:
                return node
            old = copy.deepcopy(node)
            before = node.func.id
            adapter = CHILD_ADAPTERS.get((group, original_node.name, before))
            if adapter is not None:
                node.func.id = adapter
                node.args.append(ast.Name(id='continuation', ctx=ast.Load()))
            else:
                node.func.id = LOCAL_IMPORT_ADAPTERS.get(
                    (group, original_node.name, before), before)
            substitutions.append((before, _dump(old), _dump(node)))
            return ast.copy_location(ast.YieldFrom(value=node), node)

    view = Lift().visit(copy.deepcopy(original_node))
    counts = {name: sum(row[0] == name for row in substitutions) for name in spec}
    if counts != spec:
        raise ValueError('finite command CALL substitution sites differ: ' + original_node.name)
    inverse_rows = list(substitutions)

    class Invert(ast.NodeTransformer):
        def visit_YieldFrom(self, node):
            if not isinstance(node.value, ast.Call):
                raise ValueError('unexpected command cooperative expression')
            node.value = self.generic_visit(node.value)
            for index, (before, old_dump, new_dump) in enumerate(inverse_rows):
                if _dump(node.value) == new_dump:
                    restored = copy.deepcopy(node.value)
                    adapter = CHILD_ADAPTERS.get((group, original_node.name, before))
                    if adapter is not None:
                        if (restored.func.id != adapter or not restored.args
                                or _dump(restored.args[-1]) != _dump(ast.Name(id='continuation', ctx=ast.Load()))):
                            raise ValueError('command CALL inverse routing operand differs')
                        restored.func.id = before
                        restored.args.pop()
                    else:
                        restored.func.id = before
                    if _dump(restored) != old_dump:
                        raise ValueError('command CALL inverse changed more than propagation')
                    inverse_rows.pop(index)
                    return restored
            raise ValueError('command inverse found a non-admitted yield-from')

    inverse = Invert().visit(copy.deepcopy(view))
    if inverse_rows or _dump(inverse) != _dump(original_node):
        raise ValueError('command view does not invert to its entire actual source owner')
    return view, counts


_FALLBACK_OWNERS = {'highbank': ('_command_policy_child_fields',),
    'main': ('_campaign_known_child_fields',)}


def _prepare_command_artifacts(module, group, source, filename):
    tree = ast.parse(source, filename=filename)
    functions = {}
    for name in (*VIEW_SPECS[group], *_FALLBACK_OWNERS.get(group, ())):
        nodes = [node for node in tree.body
            if type(node) is ast.FunctionDef and node.name == name]
        if len(nodes) != 1:
            raise ValueError('one complete command function source required: ' + name)
        original, node = _loaded_owner(module, name, nodes[0])
        artifact = dict(plain=original.__code__)
        if name in VIEW_SPECS[group]:
            view, counts = _cooperative_tree(group, node)
            artifact.update(derived=compile(ast.fix_missing_locations(
                ast.Module(body=[view], type_ignores=[])),
                '<finite command message continuation>', 'exec', dont_inherit=True),
                counts=counts)
        elif group == 'highbank':
            _require_literal_command_routes(node)
        functions[name] = artifact
    return functions


def _command_artifacts(module, group):
    filename, source = read_source_text(module)
    return get_source_artifacts('command-message', module.__name__, group,
        source_text=source, filename=filename,
        transformer_codes=(_prepare_command_artifacts.__code__, _loaded_owner.__code__,
            _current_command_owner.__code__, _cooperative_tree.__code__,
            _require_literal_command_routes.__code__, _dump.__code__, _code_shape.__code__),
        expected_contract=dict(views=VIEW_SPECS[group], child_adapters=CHILD_ADAPTERS,
            local_import_adapters=LOCAL_IMPORT_ADAPTERS, routes=COMMAND_ENTRIES,
            fallbacks=_FALLBACK_OWNERS.get(group, ())),
        prepare=lambda: _prepare_command_artifacts(module, group, source, filename))


class CommandMessagePrograms:
    """One private, same-Scene continuation graph; no global binding or replay.

    The object's lifetime is the real 309A0 child call. Its generators retain
    every local, branch, iteration, saved WORD and original entered CALL LONG
    while the existing ForceTurnWait passes through the parent Main session.
    """
    def __init__(self, state):
        from tools.high_level_remaining_flows import business_highbank, business_city
        from tools.high_level_main_flows import business_scene_support, business_gameplay
        from tools.high_level_main_flows import contexts_display_fields, force_turn_steps, business_commands, business_main
        self.state = checked_state(state)
        self.thread = threading.get_ident()
        self._started = False
        self.modules = dict(highbank=business_highbank, support=business_scene_support,
            gameplay=business_gameplay, display=contexts_display_fields, city=business_city,
            commands=business_commands, main=business_main)
        self.force_module = force_turn_steps
        self.message = force_turn_steps.force_turn_message_program
        self.originals, self.views, self.namespaces, self.admissions = {}, {}, {}, []
        for group, names in VIEW_SPECS.items():
            module = self.modules[group]
            artifacts = _command_artifacts(module, group)
            for name in names:
                artifact = artifacts[name]
                original = _current_command_owner(module, name, artifact['plain'])
                self.originals[(group, name)] = original
                namespace = dict(original.__globals__)
                self.namespaces[(group, name)] = namespace
                exec(artifact['derived'], namespace)
                self.views[(group, name)] = namespace[name]
                self.admissions.append(dict(group=group, function=name, substitutions=artifact['counts'],
                    complete_original_function_inverse=True))
            # Fallback source admission is cached, never its live callable.
            for name in _FALLBACK_OWNERS.get(group, ()):
                self.originals[(group, name)] = _current_command_owner(
                    module, name, artifacts[name]['plain'])
        for (group, name), namespace in self.namespaces.items():
            for dependency in VIEW_SPECS[group][name]:
                if (group, name, dependency) in CHILD_ADAPTERS:
                    continue
                alias = LOCAL_IMPORT_ADAPTERS.get((group, name, dependency))
                if alias is not None:
                    continue
                dependency_group = ('gameplay' if dependency == '_setup_call_fields'
                    else 'display' if dependency == 'display_call_fields' else group)
                namespace[dependency] = self.views[(dependency_group, dependency)]
            namespace.update(
                _command_message_child_program=self._command_child,
                _command_message_setup_child_program=self._setup_child,
                _command_message_display_child_program=self._display_child,
                _command_message_open_assignment_program=self.views[('highbank', 'open_assignment_menu_dispatch_fields')],
                _command_message_open_action_program=self.views[('highbank', 'open_city_action_menu_dispatch_fields')],
                _command_message_assignment_program=self.views[('support', 'run_city_command_assignment_fields')],
                _command_message_scene_program=self._scene_message,
                _command_message_campaign_call_program=self.views[('main', '_campaign_call_fields')],
                _command_message_campaign_child_program=self._campaign_child,
                _command_message_extended_deployment_program=self._extended_deployment,
                _command_message_project_program=self.views[('gameplay', 'settle_city_projects_and_refresh_map_fields')])

    def require_current(self, state):
        if state is not self.state or threading.get_ident() != self.thread:
            raise ValueError('command continuation belongs to another Scene or execution thread')
        for (group, name), original in self.originals.items():
            if getattr(self.modules[group], name) is not original:
                raise ValueError('actual command dependency was rebound: ' + name)
        if self.force_module.force_turn_message_program is not self.message:
            raise ValueError('actual force-turn message owner was rebound')
        if self.modules['highbank'].execute_deployment_menu_fields is not self.originals[('city', 'execute_deployment_menu_fields')]:
            raise ValueError('original command-to-deployment fallback identity changed')

    def _command_child(self, state, frame, target, continuation):
        self.require_current(state)
        if target == 0x30A74:
            if continuation not in MESSAGE_RETURNS:
                raise MovementContinuationBoundary(target, frame, 'message CALL is outside the finite command-parent scope')
            return (yield from self.views[('city', 'execute_deployment_menu_fields')](state, target, frame))
        if target in COMMAND_ENTRIES:
            if (target, continuation) not in COMMAND_CALL_PAIRS:
                raise MovementContinuationBoundary(target, frame, 'command parent does not own this actual return LONG')
            return (yield from self.views[('highbank', COMMAND_ENTRIES[target])](state, frame))
        return self.originals[('highbank', '_command_policy_child_fields')](state, frame, target)

    def _scene_message(self, memory, frame):
        self.require_current(memory.state)
        return (yield from self._message_waits(self.message(memory, frame)))

    def _message_waits(self, program):
        """Forward the identical typed wait; guard before any resumed child work."""
        received = None
        first = True
        try:
            while True:
                self.require_current(self.state)
                try:
                    waiting = next(program) if first else program.send(received)
                except StopIteration as finished:
                    return finished.value
                first = False
                received = yield waiting
        finally:
            program.close()

    def _setup_child(self, state, frame, target, continuation):
        self.require_current(state)
        if target == 0x1190E:
            if continuation != 0x311F2:
                raise MovementContinuationBoundary(target, frame, 'not the actual finish-assignment project CALL')
            return (yield from self.views[('support', '_controller_setup_child_fields')](state, frame, target))
        if target in SETUP_ENTRIES:
            if continuation != 0x30FD6:
                raise MovementContinuationBoundary(target, frame, 'not the original 31006 table CALL')
            return (yield from self.views[('support', '_controller_setup_child_fields')](state, frame, target))
        return self.originals[('support', '_controller_setup_child_fields')](state, frame, target)

    def _display_child(self, state, frame, target, continuation):
        self.require_current(state)
        if target == 0x30A74:
            return (yield from self._extended_deployment(state, target, frame, continuation))
        if target in MAIN_MESSAGE_ENTRIES:
            if continuation != 0x3CE:
                raise MovementContinuationBoundary(target, frame, 'Main message scene requires actual3CE return')
            return (yield from self.views[('main', MAIN_MESSAGE_ENTRIES[target])](state, frame))
        if target == 0x311E6:
            if continuation != 0x309A6:
                raise MovementContinuationBoundary(target, frame, 'finish-assignment requires actual309A6 return')
            return (yield from self.views[('support', 'finish_city_command_assignment_fields')](state, frame))
        if target == 0x30C3A:
            if continuation != 0x30B2A:
                raise MovementContinuationBoundary(target, frame, 'supply settlement requires actual30B2A return')
            return (yield from self.views[('support', 'deduct_all_map_packet_supply_fields')](state, frame))
        if target == 0x30FAA:
            if continuation != 0x309A0:
                raise MovementContinuationBoundary(target, frame, 'only original30960 city-assignment CALL is admitted')
            return (yield from self.views[('display', 'display_child_fields')](state, frame, target))
        return self.originals[('display', 'display_child_fields')](state, frame, target)

    def _extended_deployment(self, state, target, frame, continuation):
        """Reuse the complete deployment owner; never install/pop another slot."""
        self.require_current(state)
        if target == 0x30A74:
            if continuation not in EXTENDED_MESSAGE_RETURNS:
                raise MovementContinuationBoundary(target, frame, 'message not in the exact extended parent closure')
            return (yield from self.views[('city', 'execute_deployment_menu_fields')](state, target, frame))
        return self.originals[('city', 'execute_deployment_menu_fields')](state, target, frame)

    def _campaign_child(self, state, frame, target, continuation):
        self.require_current(state)
        if target == 0x30A74:
            if continuation != 0xC984:
                raise MovementContinuationBoundary(target, frame, 'not the actual cost-panel message return')
            return (yield from self._extended_deployment(state, target, frame, continuation))
        name = CAMPAIGN_MESSAGE_CALLS.get((target, continuation))
        if name is not None:
            return (yield from self.views[('commands', name)](state, frame))
        if any(target == pair[0] for pair in CAMPAIGN_MESSAGE_CALLS):
            raise MovementContinuationBoundary(target, frame, 'extended campaign owner does not own this return LONG')
        return self.originals[('main', '_campaign_known_child_fields')](state, frame, target)

    def second_force_tail(self, state, frame, prefix):
        """Real first-to-second BRA: no synthetic BSR and no extra stack slot."""
        self.require_current(state)
        if self._started or type(prefix) is not bool:
            raise ValueError('one actual second-force entry with explicit prefix required')
        self._started = True
        return (yield from self.views[('commands', '_diplomacy_second_force_turn_fields')](state, frame, prefix))

    def finish_assignment_call(self, state, frame, target, continuation):
        self.require_current(state)
        if self._started or (target, continuation) != (0x311E6, 0x309A6):
            raise ValueError('one actual first-force finish-assignment CALL required')
        self._started = True
        return (yield from self.views[('display', 'display_call_fields')](state, frame, target, continuation))

    def main_scene_call(self, state, frame, target, continuation):
        self.require_current(state)
        if self._started or target not in MAIN_MESSAGE_ENTRIES or continuation != 0x3CE:
            raise ValueError('one actual indexed Main scene CALL in the finite message closure required')
        self._started = True
        return (yield from self.views[('display', 'display_call_fields')](state, frame, target, continuation))

    def assignment_call(self, state, frame, target, continuation):
        self.require_current(state)
        if (target, continuation) != (0x30FAA, 0x309A0):
            raise ValueError('actual first-force city-command CALL pair required')
        if self._started:
            raise ValueError('cannot replay an entered city-command parent graph')
        self._started = True
        return (yield from self.views[('display', 'display_call_fields')](state, frame, target, continuation))


def command_assignment_call_program(state, frame, target, continuation):
    """Exact309A0 integration point: construct once, retain until actual RTS."""
    programs = CommandMessagePrograms(state)
    return (yield from programs.assignment_call(state, frame, target, continuation))


def command_second_force_program(state, frame, prefix):
    """One original BRA continuation; preserve the caller's existing LONG."""
    programs = CommandMessagePrograms(state)
    return (yield from programs.second_force_tail(state, frame, prefix))


def command_finish_assignment_call_program(state, frame, target, continuation):
    programs = CommandMessagePrograms(state)
    return (yield from programs.finish_assignment_call(state, frame, target, continuation))


def command_main_scene_call_program(state, frame, target, continuation):
    programs = CommandMessagePrograms(state)
    return (yield from programs.main_scene_call(state, frame, target, continuation))
