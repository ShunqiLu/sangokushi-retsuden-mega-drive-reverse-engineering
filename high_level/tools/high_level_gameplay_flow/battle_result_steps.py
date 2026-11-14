"""Whole battle result strips, formation preparation and scene-return caller.

The result/name/formation algorithms remain their existing complete owners.
Only real caller waits propagate; the original D98 status loop rereads the
actual VDP after an explicitly supplied vblank-start event.
"""
import ast
import copy
import importlib
import inspect
from types import CodeType, FunctionType

from .battle_preparation_steps import BattlePreparationPrograms
from .battle_trigger_steps import _dump, _code_shape, _top_code
from .contexts_services import SceneRefreshMemory
from .scene_load_steps import GameplaySceneWait
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
from ..high_level_main_flows.business_movement_support import _movement_frame


MAIN_ENTRIES = {
    0x47C: 'initialize_officer_search_details_fields',
    0x480: 'initialize_officer_search_choices_fields',
    0x48C: 'initialize_battle_deployment_screen_fields',
    0x494: 'wait_and_initialize_campaign_action_fields',
}
CALL_COUNTS = {
    'initialize_officer_search_details_fields': 1,
    'initialize_officer_search_choices_fields': 2,
    'initialize_battle_deployment_screen_fields': 2,
    'wait_and_initialize_campaign_action_fields': 3,
}
REFRESH_RETURNS = (0xD4A,0xD80,0xDBE)
DEVICE_POLL = 0xD98
EXPECTED_MAIN_SOURCE = {'initialize_officer_search_details_fields': 'def initialize_officer_search_details_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """47C: initialize officer search details; original stage and child tokens."""\n    frame=_city_ui_frame_fields(state,frame,0x47C)\n    state.sr=0x2700\n    frame=first_replace(frame,status=0)\n    frame=_campaign_call_fields(state,frame,0x1874A,0xD38)\n    return frame', 'initialize_officer_search_choices_fields': 'def initialize_officer_search_choices_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """480: initialize officer search choices; original stage and child tokens."""\n    frame=_city_ui_frame_fields(state,frame,0x480)\n    state.sr=0x2700\n    frame=first_replace(frame,status=0)\n    frame=_campaign_call_fields(state,frame,0x18792,0xD44)\n    frame=_campaign_call_fields(state,frame,0xAF48,0xD4A)\n    return frame', 'initialize_battle_deployment_screen_fields': 'def initialize_battle_deployment_screen_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """48C: initialize battle deployment screen; original stage and child tokens."""\n    frame=_city_ui_frame_fields(state,frame,0x48C)\n    state.sr=0x2700\n    frame=first_replace(frame,status=0)\n    frame=_campaign_call_fields(state,frame,0x24AD0,0xD7A)\n    frame=_campaign_call_fields(state,frame,0xAF48,0xD80)\n    return frame', 'wait_and_initialize_campaign_action_fields': 'def wait_and_initialize_campaign_action_fields(state: SceneState,\n        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """494/D94: poll the actual video status bit3, then original scene/action refresh."""\n    frame=_campaign_screen_enter_fields(state,frame,0x494)\n    while True:\n        frame=_movement_move(state,frame,\'target_x\',state.read(0xC00004,2),16)\n        frame=_world_map_bit_fields(state,frame,frame.target_x,3)\n        if not frame.status&4:\n            break\n    frame=_campaign_call_fields(state,frame,0x1072C,0xDAA)\n    frame=_movement_test(state,frame,state.read(0xFFFFF6C4,2),16)\n    if frame.status&4:\n        frame=_campaign_call_fields(state,frame,0x52C2,0xDB8)\n    return _campaign_call_fields(state,frame,0xAF48,0xDBE)'}
EXPECTED_REUSED_SOURCE = {'tools.high_level_main_flows.business_gameplay': {'upload_battle_result_prompt_fields': "def upload_battle_result_prompt_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    frame=_resource_cost_frame(state,frame,0x1874A)\n    frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())\n    frame=_movement_move(state,frame,'target_x',31,16)\n    frame=_game_text_fill_longs_fields(state,frame,'target_x')\n    frame=_movement_move(state,frame,'target_x',1,16)\n    frame=_movement_move(state,frame,'target_y',3,16)\n    frame=_movement_move(state,frame,'count',5,16)\n    frame=first_replace(frame,roster=state.table_at(0x6C168).cursor())\n    frame=_game_text_call_fields(state,frame,0xAE8A,0x18774)\n    frame=_setup_write_fields(state,frame,0xC00004,0x40200002,4)\n    frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())\n    frame=_movement_move(state,frame,'count',223,16)\n    return _game_text_upload_longs_fields(state,frame,'count')", 'upload_selected_officer_names_fields': 'def upload_selected_officer_names_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """18792: up to five names; the first negative entry fills the remaining strip."""\n    frame=_resource_cost_frame(state,frame,0x18792)\n    frame=first_replace(frame,auxiliary=state.table_at(0xFFFFAF56).cursor())\n    frame=_movement_move(state,frame,\'target_x\',state.read(0xFFFFF658,2),16)\n    frame=_movement_fixed_shift_word(state,frame,\'target_x\',1)\n    frame=first_replace(frame,auxiliary=frame.auxiliary.advance(s16(low16(frame.target_x))))\n    frame=_movement_move(state,frame,\'target_x\',1,16)\n    frame=_setup_write_fields(state,frame,0xC00004,0x40A00002,4)\n    frame=_movement_move(state,frame,\'choice\',4,16)\n    while True:\n        frame=_movement_move(state,frame,\'unit\',frame.auxiliary.word(),16)\n        frame=first_replace(frame,auxiliary=frame.auxiliary.advance(2))\n        negative=bool(frame.status&8)\n        frame=_movement_move(state,frame,\'target_y\',3,16)\n        if negative:\n            frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())\n            frame=_movement_move(state,frame,\'count\',15,16)\n            frame=_game_text_fill_longs_fields(state,frame,\'count\')\n            frame=first_replace(frame,roster=state.table_at(0x18844).cursor())\n            frame=_movement_move(state,frame,\'count\',1,16)\n            frame=_game_text_call_fields(state,frame,0xAE8A,0x18822)\n            frame=_movement_move(state,frame,\'count\',15,16)\n            frame=_game_text_fill_longs_fields(state,frame,\'count\')\n        else:\n            frame=_map_presentation_bit_fields(state,frame,frame.unit,1<<14)\n            if not frame.status&4:frame=_movement_move(state,frame,\'target_y\',2,16)\n            frame=_movement_move(state,frame,\'unit\',low16(frame.unit)&255,16)\n            frame=_movement_move(state,frame,\'count\',low16(frame.unit),16)\n            frame=_movement_fixed_shift_word(state,frame,\'unit\',1)\n            frame=_map_presentation_arithmetic_fields(state,frame,\'unit\',low16(frame.count))\n            frame=_movement_fixed_shift_word(state,frame,\'unit\',1)\n            frame=first_replace(frame,roster=state.table_at(u32(0x8A504+s16(low16(frame.unit)))).cursor(),\n                candidates=state.table_at(0xFFFFD300).cursor())\n            frame=_movement_move(state,frame,\'count\',2,16)\n            frame=_game_text_call_fields(state,frame,0xAE8A,0x187E4)\n        frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())\n        frame=_movement_move(state,frame,\'count\',95,16)\n        frame=_game_text_upload_longs_fields(state,frame,\'count\')\n        if negative:return frame\n        frame,again=_map_presentation_db_fields(frame,\'choice\')\n        if not again:return frame', 'select_primary_force_order_policy_frame_fields': 'def select_primary_force_order_policy_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """24AD0: true BYTE bit1, opposite call arms, shared24AF0 RTS."""\n    from .business_map import _world_map_bit_fields\n    frame = display_frame_fields(state, frame)\n    frame = _world_map_bit_fields(state, frame, state.read(4294964951, 1), 1)\n    return display_call_fields(state, frame, 152426, 150246) if frame.status & 4 else _battle_order_call_fields(state, frame, 150258, 150238)', '_battle_order_call_fields': 'def _battle_order_call_fields(state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int) -> FirstDeploymentFrame:\n    """Exactly one real CALL LONG, sole child, and its actual RTS read/pop."""\n    frame = display_frame_fields(state, frame)\n    uint(target, 32)\n    uint(continuation, 32)\n    stack = frame.stack_cursor.advance(-4)\n    stack.set_long(0, continuation)\n    entered = first_replace(frame, stack_cursor=stack)\n    returned = _battle_order_child_fields(state, entered, target)\n    returned = display_frame_fields(state, returned)\n    actual = returned.stack_cursor.long()\n    if actual != continuation:\n        raise MovementContinuationBoundary(actual, returned, \'original display child continuation changed\')\n    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))', '_battle_order_child_fields': 'def _battle_order_child_fields(state: SceneState, frame: FirstDeploymentFrame, target: int) -> FirstDeploymentFrame:\n    """Resolve the missing battle-order entries onto their sole full algorithms.\n\n    The nine indexed strategies share Highbank\'s complete retained-field\n    interface.  Existing primary entries keep their original display route.\n    Second-side initialization shares the existing live policy-memory view;\n    no register defaults, RAM copies or synthetic device answers are made.\n    """\n    frame = display_frame_fields(state, frame)\n    uint(target, 32)\n    if target in (146620, 146846, 147646, 148206, 148616, 148940, 149192, 149510, 150138):\n        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_65_fields\n        return highbank_coordinate_live_state_65_fields(state, frame, entry=target)\n    if target == 150258:\n        from ..high_level_battle_ai.business_formation import initialize_second_side_deployment_fields\n        return initialize_second_side_deployment_fields(BattlePolicyMemory(state), frame)\n    return display_child_fields(state, frame, target)'}, 'tools.high_level_main_flows.business_lowbank': {'upload_selection_layout_fields': 'def upload_selection_layout_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """52C2..5330: original static rows, uniform third row and final readonly packet."""\n    frame=_campaign_ui_frame_fields(state,frame,0x52C2)\n    frame=_campaign_ui_write_fields(state,frame,0x52C2,0xC00004,0x70000001,4)\n    frame=first_replace(frame,roster=state.table_at(0x89DDC).cursor())\n    frame=_campaign_ui_move_fields(state,frame,\'distance\',23)\n    frame=_campaign_ui_copy_panel_longs_fields(state,frame,\'roster\',\'distance\',0x52D6,0xC00000)\n    frame=_campaign_ui_write_fields(state,frame,0x52E0,0xC00004,0x70A00001,4)\n    frame=first_replace(frame,roster=state.table_at(0x89F5C).cursor())\n    frame=_campaign_ui_move_fields(state,frame,\'distance\',7)\n    frame=_campaign_ui_copy_panel_longs_fields(state,frame,\'roster\',\'distance\',0x52F4,0xC00000)\n    frame=_campaign_ui_write_fields(state,frame,0x52FE,0xC00004,0x72000001,4)\n    frame=_campaign_ui_move_fields(state,frame,\'distance\',7)\n    while True:\n        frame=_campaign_ui_write_fields(state,frame,0x530C,0xC00000,0x33333333,4)\n        frame,more=_campaign_ui_loop_fields(frame,\'distance\')\n        if not more:\n            break\n    frame=first_replace(frame,roster=state.table_at(0x8A0BC).cursor())\n    frame=_campaign_ui_move_fields(state,frame,\'distance\',7)\n    return _campaign_ui_copy_panel_longs_fields(state,frame,\'roster\',\'distance\',0x5324,0xC00000)'}, 'tools.high_level_battle_ai.business_formation': {'initialize_first_side_deployment_fields': 'def initialize_first_side_deployment_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    frame = _first_frame(memory, frame)\n    frame = _first_call(memory, frame, 0x2536E, _first_promote_frame)\n    frame = _first_call(memory, frame, 0x25372, prepare_first_side_assignment_fields)\n    return _first_call(memory, frame, 0x25376, populate_first_side_fields)', 'initialize_second_side_deployment_fields': 'def initialize_second_side_deployment_fields(memory: BattlePolicyMemory,\n        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """24AF2: assign formation, fill unset positions, then clear the phase WORD."""\n    frame = _first_frame(memory, frame)\n    frame = _first_call(memory, frame, 0x24AF6, prepare_second_side_formation_assignment_fields)\n    frame = _first_call(memory, frame, 0x24AFA, populate_second_side_unset_positions_fields)\n    phase = memory.state.table(0xFFFFF6D6)\n    phase.word()\n    phase.set_word(0, 0)\n    return _first_region_publish(memory, _first_memory_word(frame, 0))', 'prepare_second_side_formation_assignment_fields': 'def prepare_second_side_formation_assignment_fields(memory: BattlePolicyMemory,\n        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """24B00: one shared sentinel/count algorithm with the real 24B14 sort slot."""\n    frame = _first_frame(memory, frame)\n    roster = memory.state.table(0xFFFFA5A4)\n    frame, count = read_first_side_assignment_count_fields(memory, frame, roster, 0x24B14)\n    frame = _first_call(memory, frame, 0x24B28,\n        lambda memory, entered: copy_second_side_position_assignment_fields(memory, entered, count))\n    return _first_region_publish(memory, frame)', 'populate_second_side_unset_positions_fields': 'def populate_second_side_unset_positions_fields(memory: BattlePolicyMemory,\n        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """25200: reuse the sole roster/order/cell loop after actual choice generation."""\n    frame = _first_call(memory, frame, 0x25204, prepare_second_side_battlefield_choices_fields)\n    frame = first_replace(frame, roster=memory.state.table(0xFFFFA5A4).cursor(),\n        candidates=memory.state.table(0xFFFFAF96).cursor(),\n        controller=memory.state.table(0xFFFFD310), scan=memory.state.table(0xFFFFA150).cursor())\n    return _first_region_publish(memory, submit_unset_deployment_fields(memory, frame))'}}
EXPECTED_WAIT_VALIDATE = "def validate(self):\n    checked_state(self.state)\n    _movement_frame(self.state, self.frame)\n    if (self.event, self.poll) not in (('scene-sound-byte', 33740), ('vblank-end', 44876), ('vblank-start', 44892), ('sound-bus-acquire', 32920), ('vdp-dma', 26758), ('vdp-dma', 26874), ('vblank-start', 3480)):\n        raise ValueError('actual finite scene-load polling point and external event required')\n    uint(self.status_word, 16)\n    if self.state.sr != self.status_word or self.frame.status != self.status_word & 31:\n        raise ValueError('scene-load full SR and software CCR-X disagree')\n    return self"


def _result_source_tree(original_tree):
    """Four exact whole functions/eight calls/one status-loop suspension."""
    result = copy.deepcopy(original_tree)
    inverses = {}
    for index,original in enumerate(original_tree.body):
        if not isinstance(original,ast.FunctionDef) or original.name not in CALL_COUNTS:
            continue
        expected = ast.parse(EXPECTED_MAIN_SOURCE[original.name]).body
        if len(expected)!=1 or _dump(original)!=_dump(expected[0]):
            raise ValueError('complete reviewed battle-result Main owner changed: '+original.name)
        if any(isinstance(node,(ast.Yield,ast.YieldFrom)) for node in ast.walk(original)):
            raise ValueError('original battle-result source owner must remain synchronous')
        substitutions = []

        class Lift(ast.NodeTransformer):
            def visit_Call(self,node):
                node = self.generic_visit(node)
                if isinstance(node.func,ast.Name) and node.func.id=='_campaign_call_fields':
                    before = copy.deepcopy(node)
                    node.func.id = '_result_campaign_call'
                    after = ast.copy_location(ast.YieldFrom(value=node),node)
                    substitutions.append((before,copy.deepcopy(after)))
                    return after
                return node

        derived = Lift().visit(copy.deepcopy(original))
        if len(substitutions)!=CALL_COUNTS[original.name]:
            raise ValueError('exact battle-result Main call count differs: '+original.name)
        loop_before = loop_after = None
        if original.name=='wait_and_initialize_campaign_action_fields':
            loops = [node for node in derived.body if isinstance(node,ast.While)]
            expected_loop = ast.parse('while True:\n'
                "    frame = _movement_move(state, frame, 'target_x', state.read(0xC00004, 2), 16)\n"
                "    frame = _world_map_bit_fields(state, frame, frame.target_x, 3)\n"
                '    if not frame.status & 4:\n        break').body[0]
            if len(loops)!=1 or _dump(loops[0])!=_dump(expected_loop):
                raise ValueError('whole original D98 read/BTST/BEQ loop required')
            loop_before = copy.deepcopy(loops[0])
            loops[0].body.append(ast.parse('frame = (yield from _result_wait_vblank(state, frame))').body[0])
            loop_after = copy.deepcopy(loops[0])
        pending = list(substitutions)

        class Inverse(ast.NodeTransformer):
            def visit_While(self,node):
                if loop_after is not None and _dump(node)==_dump(loop_after):
                    return copy.deepcopy(loop_before)
                return self.generic_visit(node)

            def visit_YieldFrom(self,node):
                for position,(before,after) in enumerate(pending):
                    if _dump(node)==_dump(after):
                        pending.pop(position)
                        return ast.copy_location(copy.deepcopy(before),node)
                raise ValueError('unadmitted battle-result yield-from')

        inverse = Inverse().visit(copy.deepcopy(derived))
        if pending or _dump(inverse)!=_dump(original):
            raise ValueError('complete battle-result function inverse differs: '+original.name)
        result.body[index] = derived
        inverses[index] = inverse
    if len(inverses)!=4:
        raise ValueError('all four complete battle-result Main owners required')
    restored = copy.deepcopy(result)
    for index,inverse in inverses.items():
        restored.body[index] = inverse
    if _dump(restored)!=_dump(original_tree):
        raise ValueError('whole original Main module inverse differs')
    return ast.fix_missing_locations(result)


class BattleResultScenePrograms(BattlePreparationPrograms):
    """Four actual Main47C/480/48C/494 entries on the existing full Scene graph."""

    def __init__(self,state):
        super().__init__(state)
        from ..high_level_main_flows import business_main
        self.result_module = business_main
        tree = ast.parse(inspect.getsource(business_main),filename=business_main.__file__)
        plain = compile(tree,business_main.__file__,'exec',dont_inherit=True)
        self.result_originals = {}
        self.result_codes = {}
        for name,source in EXPECTED_MAIN_SOURCE.items():
            nodes = [node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name==name]
            original = getattr(business_main,name)
            if (len(nodes)!=1 or _dump(nodes[0])!=_dump(ast.parse(source).body[0])
                    or type(original)is not FunctionType or original.__globals__ is not vars(business_main)
                    or original.__module__!=business_main.__name__ or original.__name__!=name
                    or original.__closure__ is not None or original.__code__.co_freevars
                    or _code_shape(original.__code__)!=_code_shape(_top_code(plain,name))):
                raise ValueError('actual complete battle-result Main function required: '+name)
            self.result_originals[name] = original
            self.result_codes[name] = original.__code__
        derived = compile(_result_source_tree(tree),business_main.__file__,'exec',dont_inherit=True)
        self.result_namespace = dict(vars(business_main))
        aliases = {'_result_campaign_call':self.views['main','_campaign_call_fields'],
            '_result_wait_vblank':self._wait_result_vblank}
        for name,value in aliases.items():
            if name in self.result_namespace:
                raise ValueError('result aliases must not shadow original business bindings')
            self.result_namespace[name] = value
        self.result_bindings = aliases
        self.result_views = {}
        for name in CALL_COUNTS:
            original = self.result_originals[name]
            view = FunctionType(_top_code(derived,name),self.result_namespace,name,original.__defaults__,None)
            view.__kwdefaults__ = original.__kwdefaults__
            view.__annotations__ = dict(original.__annotations__)
            if not inspect.isgeneratorfunction(view) or view.__closure__ is not None:
                raise ValueError('complete closure-free battle-result generator required: '+name)
            self.result_views[name] = view
        self.result_view_owners = dict(self.result_views)
        self.result_view_codes = {name:view.__code__ for name,view in self.result_views.items()}
        self.result_reused = {}
        for path,sources in EXPECTED_REUSED_SOURCE.items():
            module = importlib.import_module(path)
            source = inspect.getsource(module)
            current_tree = ast.parse(source,filename=module.__file__)
            code = compile(current_tree,module.__file__,'exec',dont_inherit=True)
            for name,expected in sources.items():
                nodes = [node for node in current_tree.body if isinstance(node,ast.FunctionDef) and node.name==name]
                owner = getattr(module,name)
                if (len(nodes)!=1 or _dump(nodes[0])!=_dump(ast.parse(expected).body[0])
                        or type(owner)is not FunctionType or owner.__globals__ is not vars(module)
                        or owner.__module__!=module.__name__ or owner.__name__!=name
                        or owner.__closure__ is not None or owner.__code__.co_freevars
                        or _code_shape(owner.__code__)!=_code_shape(_top_code(code,name))):
                    raise ValueError('actual complete reused result function required: '+name)
                self.result_reused[path,name] = (module,owner,owner.__code__)
        from . import scene_load_steps
        wait_tree = ast.parse(inspect.getsource(scene_load_steps),filename=scene_load_steps.__file__)
        wait_class = next(node for node in wait_tree.body if isinstance(node,ast.ClassDef) and node.name=='GameplaySceneWait')
        validate = next(node for node in wait_class.body if isinstance(node,ast.FunctionDef) and node.name=='validate')
        wait_code = _top_code(compile(wait_tree,scene_load_steps.__file__,'exec',dont_inherit=True),'GameplaySceneWait')
        validate_codes = [code for code in wait_code.co_consts if type(code)is CodeType
            and code.co_name=='validate' and code.co_qualname=='GameplaySceneWait.validate']
        actual = scene_load_steps.GameplaySceneWait.validate
        if (scene_load_steps.GameplaySceneWait is not GameplaySceneWait or len(validate_codes)!=1
                or _dump(validate)!=_dump(ast.parse(EXPECTED_WAIT_VALIDATE).body[0])
                or type(actual)is not FunctionType or actual.__globals__ is not vars(scene_load_steps)
                or actual.__closure__ is not None
                or _code_shape(actual.__code__)!=_code_shape(validate_codes[0])):
            raise ValueError('actual exact D98-extended Scene wait admission required')
        self.result_wait_module = scene_load_steps
        self.result_wait_validate = actual
        self.result_wait_code = actual.__code__

    def require_current(self,state):
        super().require_current(state)
        if not hasattr(self,'result_originals'):
            return
        for name,owner in self.result_originals.items():
            if getattr(self.result_module,name)is not owner or owner.__code__ is not self.result_codes[name]:
                raise ValueError('actual result Main owner changed: '+name)
        if self.result_views.keys()!=self.result_view_owners.keys():
            raise ValueError('complete result view set changed')
        for name,view in self.result_view_owners.items():
            if self.result_views[name]is not view or view.__code__ is not self.result_view_codes[name]:
                raise ValueError('actual result view CodeType changed: '+name)
        for name,owner in self.result_bindings.items():
            if self.result_namespace.get(name)is not owner:
                raise ValueError('private result continuation binding changed: '+name)
        for (path,name),(module,owner,code) in self.result_reused.items():
            if getattr(module,name)is not owner or owner.__code__ is not code:
                raise ValueError('complete reused result callable changed: '+name)
        if (self.result_wait_module.GameplaySceneWait is not GameplaySceneWait
                or GameplaySceneWait.validate is not self.result_wait_validate
                or self.result_wait_validate.__code__ is not self.result_wait_code):
            raise ValueError('exact result device-wait source owner changed')

    def _wait_result_vblank(self,state,frame):
        """Only D98's genuine bit3-zero loop: external progress, then original reread."""
        self.require_current(state)
        memory = SceneRefreshMemory(state)
        frame = memory.sync_status(_movement_frame(state,frame))
        waiting = GameplaySceneWait(state,frame,state.sr,'vblank-start',DEVICE_POLL).validate()
        returned = (yield waiting)
        self.require_current(state)
        if returned is not waiting.frame or state.sr!=waiting.status_word:
            raise ValueError('result device progress cannot replace the frame or software SR')
        return returned

    def _campaign_child(self,state,frame,target,continuation):
        self.require_current(state)
        if target==0x1072C and continuation==0xDAA:
            return (yield from self._load(SceneRefreshMemory(state),frame))
        if target==0xAF48 and continuation in REFRESH_RETURNS:
            return (yield from self._refresh(SceneRefreshMemory(state),frame))
        return (yield from super()._campaign_child(state,frame,target,continuation))

    def _display_child(self,state,frame,target,continuation):
        self.require_current(state)
        if target in MAIN_ENTRIES:
            if continuation!=0x3CE:
                raise MovementContinuationBoundary(target,frame,'result Main parent requires original3CE LONG')
            return (yield from self.result_views[MAIN_ENTRIES[target]](state,frame))
        return (yield from super()._display_child(state,frame,target,continuation))

    def main_scene_call(self,state,frame,target,continuation):
        if target not in MAIN_ENTRIES:
            return (yield from super().main_scene_call(state,frame,target,continuation))
        self.require_current(state)
        if self._started or continuation!=0x3CE:
            raise ValueError('one actual indexed battle-result Main invocation required')
        self._started = True
        return (yield from self.views['display','display_call_fields'](state,frame,target,continuation))
