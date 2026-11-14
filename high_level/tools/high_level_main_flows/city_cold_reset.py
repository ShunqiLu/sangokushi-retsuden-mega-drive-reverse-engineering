"""Original206 reset with an explicitly preselected persistent city main tail.

This is an additive exact owner, not an extension of the old accepted type
guards. The original reset view, RESET writes, USP/MOVEM and checksum path
remain unchanged. Its private namespace gains one different tail binding.
"""
import ast
import inspect
from types import CodeType, FunctionType, GeneratorType

from . import business_boot, bootstrap_reset, city_scene_steps
from .bootstrap_reset import PersistentColdResetSession, ResetAudioReleasePoint
from .bootstrap_steps import BootstrapMainWait
from .contexts_gameplay import MovementContinuationBoundary
from .business_movement_support import _movement_frame
from .domain import Boundary
from ..high_level_gameplay_flow.scene_load_steps import GameplaySceneWait
from ..high_level_scene_flows import source_artifact_cache


# Rendered as complete editable source contracts by the publication producer.
EXPECTED_SOURCES = {'boot': {'reset_console_frame_fields': 'def reset_console_frame_fields(state: SceneState, frame: FirstDeploymentFrame,\n        profile: ResetProfile | None = None) -> FirstDeploymentFrame:\n    """206→300, retaining all real bootstrap MOVEM and device effects."""\n    from .business_movement_support import (\n        _movement_test_long, _movement_test, _movement_add_word)\n    from .business_map import _world_map_bit_fields\n    frame = display_frame_fields(state, frame)\n    frame = _movement_test_long(state, frame, state.read(0xA10008, 4))\n    if frame.status & 4:\n        frame = _movement_test(state, frame, state.read(0xA1000C, 2), 16)\n    if not frame.status & 4:\n        return start_game_main_loop_frame_fields(state, frame)\n    frame = display_address_fields(state, frame, \'scratch\', 0x294)\n    for name in (\'offset_x\', \'offset_y\', \'choice\'):\n        value = u32(s16(frame.scratch.word()))\n        frame = first_replace(frame, **{name: value}, scratch=frame.scratch.advance(2))\n    for name in (\'roster\', \'candidates\', \'controller\', \'scan\', \'opponent\'):\n        value = frame.scratch.long()\n        frame = first_replace(frame, scratch=frame.scratch.advance(4))\n        frame = display_address_fields(state, frame, name, value)\n    frame = display_move_fields(state, frame, \'target_x\',\n        state.read(u32(frame.candidates.base - 0x10FF), 1), 8)\n    frame = display_move_fields(state, frame, \'target_x\', low8(frame.target_x) & 0xF, 8)\n    if not frame.status & 4:\n        frame = display_store_fields(state, frame, 0x22C,\n            u32(frame.candidates.base + 0x2F00), 0x53454741, 4)\n    frame = display_move_fields(state, frame, \'target_x\', frame.opponent.word())\n    frame = display_move_fields(state, frame, \'target_x\', 0, 32)\n    frame = display_address_fields(state, frame, \'auxiliary\', frame.target_x)\n    if type(profile) is not ResetProfile:\n        raise MovementContinuationBoundary(0x23A, frame,\n            \'original MOVE A6,USP requires the existing explicit BootstrapControl\')\n    profile.validate(state)\n    profile.processor.set_user_stack(state, frame.auxiliary.base)\n    frame = display_move_fields(state, frame, \'target_y\', 0x17, 32)\n    while True:\n        value = frame.scratch.byte()\n        frame = first_replace(frame, scratch=frame.scratch.advance(1))\n        frame = display_move_fields(state, frame, \'offset_x\', value, 8)\n        frame = display_store_fields(state, frame, 0x240,\n            frame.opponent.base, low16(frame.offset_x))\n        frame = _movement_add_word(state, frame, \'offset_x\', low16(frame.choice))\n        frame, more = display_loop_fields(frame, \'target_y\')\n        if not more:\n            break\n    value = frame.scratch.long()\n    frame = first_replace(frame, scratch=frame.scratch.advance(4))\n    frame = display_store_fields(state, frame, 0x248, frame.opponent.base, value, 4)\n    frame = display_store_fields(state, frame, 0x24A, frame.scan.base, low16(frame.target_x))\n    frame = display_store_fields(state, frame, 0x24C, frame.candidates.base, low16(frame.choice))\n    frame = display_store_fields(state, frame, 0x24E, frame.controller.base, low16(frame.choice))\n    while True:\n        frame = _world_map_bit_fields(state, frame, frame.candidates.byte(), frame.target_x & 7)\n        if frame.status & 4:\n            break\n        state.progress(\'original250 sound bus request bit0\')\n    frame = display_move_fields(state, frame, \'unit\', 0x25, 32)\n    while True:\n        value = frame.scratch.byte()\n        frame = first_replace(frame, scratch=frame.scratch.advance(1))\n        frame = display_store_fields(state, frame, 0x256, frame.roster.base, value, 1)\n        frame = first_replace(frame, roster=frame.roster.advance(1))\n        frame, more = display_loop_fields(frame, \'unit\')\n        if not more:\n            break\n    frame = display_store_fields(state, frame, 0x25C, frame.controller.base, low16(frame.target_x))\n    frame = display_store_fields(state, frame, 0x25E, frame.candidates.base, low16(frame.target_x))\n    frame = display_store_fields(state, frame, 0x260, frame.controller.base, low16(frame.choice))\n    while True:\n        frame = first_replace(frame, auxiliary=frame.auxiliary.advance(-4))\n        frame = display_store_fields(state, frame, 0x262, frame.auxiliary.base, frame.target_x, 4)\n        frame, more = display_loop_fields(frame, \'offset_y\')\n        if not more:\n            break\n    for pc in (0x268, 0x26A):\n        value = frame.scratch.long()\n        frame = first_replace(frame, scratch=frame.scratch.advance(4))\n        frame = display_store_fields(state, frame, pc, frame.opponent.base, value, 4)\n    frame = display_move_fields(state, frame, \'count\', 0x1F, 32)\n    while True:\n        frame = display_store_fields(state, frame, 0x26E, frame.scan.base, frame.target_x, 4)\n        frame, more = display_loop_fields(frame, \'count\')\n        if not more:\n            break\n    value = frame.scratch.long()\n    frame = first_replace(frame, scratch=frame.scratch.advance(4))\n    frame = display_store_fields(state, frame, 0x274, frame.opponent.base, value, 4)\n    frame = display_move_fields(state, frame, \'distance\', 0x13, 32)\n    while True:\n        frame = display_store_fields(state, frame, 0x278, frame.scan.base, frame.target_x, 4)\n        frame, more = display_loop_fields(frame, \'distance\')\n        if not more:\n            break\n    frame = display_move_fields(state, frame, \'offset_x\', 3, 32)\n    while True:\n        value = frame.scratch.byte()\n        frame = first_replace(frame, scratch=frame.scratch.advance(1))\n        frame = display_store_fields(state, frame, 0x280, u32(frame.scan.base + 17), value, 1)\n        frame, more = display_loop_fields(frame, \'offset_x\')\n        if not more:\n            break\n    frame = display_store_fields(state, frame, 0x288, frame.controller.base, low16(frame.target_x))\n    source = frame.auxiliary\n    for name in (\'target_x\', \'target_y\', \'unit\', \'count\', \'distance\', \'offset_x\',\n            \'offset_y\', \'choice\', \'roster\', \'candidates\', \'controller\', \'scan\',\n            \'opponent\', \'scratch\', \'auxiliary\'):\n        value = source.long()\n        source = source.advance(4)\n        if name in (\'roster\', \'candidates\', \'controller\', \'scan\', \'opponent\', \'scratch\', \'auxiliary\'):\n            frame = display_address_fields(state, frame, name, value)\n        else:\n            frame = first_replace(frame, **{name: value})\n    frame = display_status_fields(state, frame, 0x2700)\n    return start_game_main_loop_frame_fields(state, frame)', 'start_game_main_loop_frame_fields': 'def start_game_main_loop_frame_fields(state: SceneState,\n        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """Whole original invocation, retaining its actual 003BC continuation."""\n    from .bootstrap_steps import run_bootstrap_main_blocking_fields\n    return run_bootstrap_main_blocking_fields(state, frame)'}, 'reset': {'_complete_reset_view': "def _complete_reset_view(point_factory,returned_frame):\n    original = business_boot.reset_console_frame_fields\n    if (type(original) is not FunctionType or original.__module__ != business_boot.__name__\n            or original.__name__ != 'reset_console_frame_fields' or inspect.isgeneratorfunction(original)):\n        raise Boundary('actual complete original206 reset owner required')\n    parsed = ast.parse(inspect.getsource(original))\n    if len(parsed.body) != 1 or type(parsed.body[0]) is not ast.FunctionDef:\n        raise Boundary('one complete original reset function source required')\n    namespace = dict(vars(business_boot))\n    exec(compile(parsed,'<plain complete original reset identity>','exec'),namespace)\n    plain = namespace[original.__name__]\n    for attribute in ('co_code','co_consts','co_names','co_varnames','co_argcount','co_kwonlyargcount',\n            'co_freevars','co_cellvars','co_flags'):\n        if getattr(plain.__code__,attribute) != getattr(original.__code__,attribute):\n            raise Boundary('actual loaded reset owner differs from its whole source')\n    function = parsed.body[0]\n    if any(isinstance(node,ast.Name) and node.id.startswith('_cold_reset_') for node in ast.walk(function)):\n        raise Boundary('original reset source competes with private continuation names')\n    anchor = ast.parse('frame = display_store_fields(state, frame, 0x260, frame.controller.base, low16(frame.choice))').body[0]\n    sites = [index for index,node in enumerate(function.body) if _dump(node) == _dump(anchor)]\n    if len(sites) != 1:\n        raise Boundary('exact single completed original260 RESET release site required')\n    inserted = ast.parse('_cold_reset_resumed = yield _cold_reset_point(0x262, frame)\\n'\n        'frame = _cold_reset_returned_frame(_cold_reset_resumed)').body\n    view = copy.deepcopy(function)\n    site = sites[0]+1\n    view.body[site:site] = copy.deepcopy(inserted)\n    inverse = copy.deepcopy(view)\n    if [_dump(node) for node in inverse.body[site:site+2]] != [_dump(node) for node in inserted]:\n        raise Boundary('the two reset suspension inverse statements differ')\n    del inverse.body[site:site+2]\n    if _dump(inverse) != _dump(function):\n        raise Boundary('reset continuation view failed complete-function inverse AST identity')\n    namespace = dict(vars(business_boot))\n    namespace.update(_cold_reset_point=point_factory,_cold_reset_returned_frame=returned_frame)\n    module = ast.fix_missing_locations(ast.Module(body=[view],type_ignores=[]))\n    exec(compile(module,'<complete reset view with one reversible260 suspension>','exec'),namespace)\n    program = namespace[original.__name__]\n    if not inspect.isgeneratorfunction(program):\n        raise Boundary('reset view must own its actual suspended Python frame')\n    return original,program,dict(confidence='confirmed_complete_current_FN_inverse_AST_identity',\n        original_function=original.__name__,original_module=original.__module__,\n        original_top_level_statements=len(function.body),inserted_statements=2,\n        original_reset_write=0x260,next_original_point=0x262,whole_FN_inverse=True,\n        changed_original_statements=0,callee_or_global_replacement=False)", 'PersistentColdResetSession': 'class PersistentColdResetSession:\n    """One original cold reset, one AudioOnly interleave, then true00300 tail.\n\n    At262 no68000 IRQ or fabricated full frame is accepted: resume_release\n    adopts only this exact captured point/frame after external audio work.\n    Audio and devices still own every reset pulse, bus permit and DATA grant.\n    After the true00300 owner reaches3BC, main_session is its actual persistent\n    owner, not a second invocation created from an observed screenshot/state.\n    """\n    def __init__(self,state,frame,profile):\n        self.state = checked_state(state)\n        self.entry = _movement_frame(state,frame)\n        if type(profile) is not ResetProfile or frame.status != state.sr&31:\n            raise ValueError(\'actual explicit reset profile and full frame/SR required\')\n        profile.validate(state)\n        self.profile,self.thread = profile,threading.get_ident()\n        self.original,self.program_factory,self.source_contract = _complete_reset_view(self._point,self._returned_frame)\n        self.program = self.waiting = self.main_session = None\n        self.started = self.failed = False\n        self.phase = \'not-started\'\n        self.events = []\n\n    def _guard(self):\n        if (threading.get_ident() != self.thread or business_boot.reset_console_frame_fields is not self.original\n                or self.failed):\n            raise Boundary(\'persistent reset owner/thread/source is no longer available\')\n\n    def _point(self,pc,frame):\n        _movement_frame(self.state,frame)\n        if pc != 0x262 or frame.status != self.state.sr&31:\n            raise Boundary(\'actual completed260 full-frame continuation required\')\n        return ResetAudioReleasePoint(self,pc,frame,self.state.sr)\n\n    def _returned_frame(self,frame):\n        if (type(self.waiting) is not ResetAudioReleasePoint or frame is not self.waiting.frame\n                or self.state.sr != self.waiting.full_sr):\n            raise Boundary(\'audio-only interleave may not replace suspended68000 carriers/SR\')\n        return _movement_frame(self.state,frame)\n\n    def _advance(self,frame=None):\n        self._guard()\n        try:\n            point = next(self.program) if frame is None else self.program.send(frame)\n        except MovementContinuationBoundary as boundary:\n            main = getattr(boundary,\'bootstrap_main_session\',None)\n            waiting = getattr(boundary,\'bootstrap_main_wait\',None)\n            if (type(main) is not BootstrapMainSession or type(waiting) is not BootstrapMainWait\n                    or main.state is not self.state or waiting.state is not self.state\n                    or waiting is not main.waiting or boundary.target != waiting.poll\n                    or boundary.context is not waiting.frame):\n                self.failed = True\n                raise\n            # Original reset\'s tail has entered the actual nonreturning300.\n            # Its existing façade retains the whole MainSession at real3BC.\n            self.main_session,self.waiting,self.phase = main,waiting,\'original-main-tail\'\n            self.events.append((\'actual_original300_tail_handoff\',waiting.poll,\n                waiting.frame.stack_cursor.base,main.suspensions))\n            return waiting\n        except StopIteration as completion:\n            self.failed = True\n            raise Boundary(\'original nonreturning206/300 unexpectedly returned ordinarily\') from completion\n        except BaseException:\n            self.failed = True\n            raise\n        if type(point) is not ResetAudioReleasePoint or point.session is not self:\n            self.failed = True\n            raise Boundary(\'reset owner yielded a foreign or untyped point\')\n        self.waiting,self.phase = point,\'actual-audio-release\'\n        self.events.append((\'completed_original260_suspend_before262\',point.pc,\n            point.frame.stack_cursor.base,point.full_sr))\n        return point\n\n    def start(self):\n        self._guard()\n        if self.started:\n            raise Boundary(\'original reset206 prefix must never replay\')\n        self.started = True\n        self.program = self.program_factory(self.state,self.entry,self.profile)\n        return self._advance()\n\n    def resume_release(self,point):\n        self._guard()\n        if (not self.started or self.phase != \'actual-audio-release\' or point is not self.waiting\n                or type(point) is not ResetAudioReleasePoint or point.session is not self):\n            raise Boundary(\'the actual live262 audio-release point is required\')\n        frame = self._returned_frame(point.frame)\n        return self._advance(frame)\n\n    def resume_main(self,frame,pc):\n        self._guard()\n        if self.phase != \'original-main-tail\' or self.main_session is None:\n            raise Boundary(\'reset has not tail-handed to its actual original main owner\')\n        self.waiting = self.main_session.resume(frame,pc)\n        return self.waiting'}, 'city': {'_make_city_main_program': "def _make_city_main_program(state, frame):\n    from . import bootstrap_steps\n    namespace, views, originals, admissions = _compile_views(bootstrap_steps, 'bootstrap')\n    fallback = originals['_bootstrap_dispatch_call_steps']\n\n    def dispatch(actual_state, actual_frame, target, continuation):\n        if actual_state is not state:\n            raise ValueError('one actual same-Scene main invocation required')\n        if bootstrap_steps._bootstrap_dispatch_call_steps is not fallback:\n            raise ValueError('original main fallback dispatcher was rebound')\n        if target in (1176, 1144, 1168, 1112):\n            from ..high_level_gameplay_flow.battle_lifecycle_steps import BattleLifecycleScenePrograms\n            programs = BattleLifecycleScenePrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        if target == 1108:\n            from ..high_level_gameplay_flow.calendar_steps import CalendarScenePrograms\n            programs = CalendarScenePrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        if target == 1204:\n            from ..high_level_scene_flows.narrative_reset import NarrativeScenePrograms\n            programs = NarrativeScenePrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        if target in (1116, 1120, 1124, 1128, 1132, 1136, 1140):\n            from ..high_level_gameplay_flow.battle_preparation_steps import BattlePreparationPrograms\n            programs = BattlePreparationPrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        if target in (1156, 1160):\n            from ..high_level_gameplay_flow.strategy_steps import StrategicScenePrograms\n            programs = StrategicScenePrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        if target in (1148, 1152, 1164, 1172):\n            from ..high_level_gameplay_flow.battle_result_steps import BattleResultScenePrograms\n            programs = BattleResultScenePrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        if target in (1184, 1188):\n            from ..high_level_gameplay_flow.force_selection_steps import ForceSelectionScenePrograms\n            programs = ForceSelectionScenePrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        if target == 1192:\n            from ..high_level_gameplay_flow.battle_outcome_steps import BattleOutcomeScenePrograms\n            programs = BattleOutcomeScenePrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        if target == 1196:\n            from ..high_level_gameplay_flow.battle_target_steps import BattleTargetScenePrograms\n            programs = BattleTargetScenePrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        if target in (1212, 1216):\n            from ..high_level_gameplay_flow.diplomacy_panel_steps import DiplomacyPanelScenePrograms\n            programs = DiplomacyPanelScenePrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        if target in (1048, 1052, 1208):\n            from ..high_level_gameplay_flow.command_panel_steps import CommandPanelScenePrograms\n            programs = CommandPanelScenePrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        if target == 1076:\n            from ..high_level_gameplay_flow.selected_command_steps import SelectedCommandScenePrograms\n            programs = SelectedCommandScenePrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        if target in (1016, 1024, 1032, 1040, 1056, 1060, 1064, 1068, 1072):\n            from ..high_level_gameplay_flow.early_panel_steps import EarlyPanelScenePrograms\n            programs = EarlyPanelScenePrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        if target in (1080, 1088, 1092, 1096, 1104):\n            from ..high_level_gameplay_flow.roster_panel_steps import RosterPanelScenePrograms\n            programs = RosterPanelScenePrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        if target in (984, 988, 1012, 1020):\n            from ..high_level_gameplay_flow.startup_panel_steps import StartupPanelScenePrograms\n            programs = StartupPanelScenePrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        if target in (1044,):\n            from ..high_level_gameplay_flow.roster_upload_steps import RosterUploadScenePrograms\n            programs = RosterUploadScenePrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        if target in (992, 996, 1004, 1008):\n            from ..high_level_gameplay_flow.title_scene_steps import TitleScenePrograms\n            programs = TitleScenePrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        if target in (1028, 1036):\n            from ..high_level_gameplay_flow.information_panel_steps import InformationPanelScenePrograms\n            programs = InformationPanelScenePrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        if target == 1200:\n            from ..high_level_gameplay_flow.campaign_menu_steps import CampaignMenuScenePrograms\n            programs = CampaignMenuScenePrograms(state)\n            return (yield from programs.main_scene_call(state, actual_frame, target, continuation))\n        return (yield from fallback(state, actual_frame, target, continuation))\n    namespace['_city_scene_main_dispatch'] = dispatch\n    return (views['bootstrap_main_program'](state, frame), bootstrap_steps, originals, admissions)", '_compile_views': "def _compile_views(module, group):\n    filename, source = read_source_text(module)\n    artifacts = get_source_artifacts('city', module.__name__, group, source_text=source, filename=filename, transformer_codes=(_prepare_city_artifacts.__code__, _cooperative_module.__code__, _dump.__code__, _code_shape.__code__, _top_code.__code__, _compile_views.__code__), expected_contract=dict(expected=EXPECTED_WHOLE_SOURCES[group], views=LOWBANK_VIEWS), prepare=lambda: _prepare_city_artifacts(module, group, source, filename))\n    plain, derived = (artifacts['plain'], artifacts['derived'])\n    originals = {}\n    for name in EXPECTED_WHOLE_SOURCES[group]:\n        original = getattr(module, name)\n        if type(original) is not FunctionType or original.__globals__ is not vars(module) or original.__module__ != module.__name__ or (original.__name__ != name) or (original.__closure__ is not None) or (_code_shape(_top_code(plain, name)) != _code_shape(original.__code__)):\n            raise ValueError('actual complete city-scene owner required: ' + name)\n        originals[name] = original\n    namespace = dict(vars(module))\n    for name in ('_city_scene_lowbank_child', '_city_scene_main_dispatch'):\n        if name in namespace:\n            raise ValueError('private city-scene name must not shadow business binding')\n    names = LOWBANK_VIEWS if group == 'lowbank' else ('bootstrap_main_program',)\n    views = {}\n    for name in names:\n        original = originals[name]\n        view = FunctionType(_top_code(derived, name), namespace, name, original.__defaults__, None)\n        view.__kwdefaults__ = original.__kwdefaults__\n        view.__annotations__ = dict(original.__annotations__)\n        if not inspect.isgeneratorfunction(view) or view.__closure__ is not None:\n            raise ValueError('complete city-scene view must be a closure-free generator')\n        views[name] = namespace[name] = view\n    return (namespace, views, originals, artifacts['admissions'])", '_cooperative_module': 'def _cooperative_module(group, original_tree):\n    """Exact whole FN and actual whole module inverse, not a shape allowance."""\n    names = (LOWBANK_VIEWS if group == \'lowbank\' else\n        {\'bootstrap_main_program\': {\'_bootstrap_dispatch_call_steps\': 1}})\n    if group not in (\'lowbank\', \'bootstrap\'):\n        raise ValueError(\'only the finite Lowbank/main source modules are lifted\')\n    result = copy.deepcopy(original_tree)\n    inverses = {}\n    admissions = []\n    for index, original in enumerate(original_tree.body):\n        if not isinstance(original, ast.FunctionDef) or original.name not in names:\n            continue\n        expected = ast.parse(EXPECTED_WHOLE_SOURCES[group][original.name]).body\n        if len(expected) != 1 or _dump(original) != _dump(expected[0]) or index in inverses:\n            raise ValueError(\'complete reviewed city-scene source differs: \' + original.name)\n        spec = names[original.name]\n        counts = {name: 0 for name in spec}\n        changes = []\n\n        class Lift(ast.NodeTransformer):\n            def visit_Call(self, node):\n                node = self.generic_visit(node)\n                if not isinstance(node.func, ast.Name) or node.func.id not in spec:\n                    return node\n                before = copy.deepcopy(node)\n                name = node.func.id\n                counts[name] += 1\n                if group == \'bootstrap\':\n                    # Already inside the original yield-from; change its sole\n                    # private binding, not the surrounding complete main body.\n                    node.func.id = \'_city_scene_main_dispatch\'\n                    after = copy.deepcopy(node)\n                elif original.name == \'_lowbank_ui_call_fields\':\n                    node.func.id = \'_city_scene_lowbank_child\'\n                    node.args.append(ast.Name(id=\'continuation\', ctx=ast.Load()))\n                    after = ast.copy_location(ast.YieldFrom(value=node), node)\n                else:\n                    after = ast.copy_location(ast.YieldFrom(value=node), node)\n                changes.append((before, copy.deepcopy(after)))\n                return after\n\n        derived = Lift().visit(copy.deepcopy(original))\n        if counts != spec:\n            raise ValueError(\'exact city-scene propagation count differs: \' + original.name)\n        remaining = list(changes)\n\n        class Inverse(ast.NodeTransformer):\n            def visit_YieldFrom(self, node):\n                if group == \'bootstrap\':\n                    return self.generic_visit(node)\n                for position, (before, after) in enumerate(remaining):\n                    if _dump(node) == _dump(after):\n                        remaining.pop(position)\n                        return ast.copy_location(copy.deepcopy(before), node)\n                raise ValueError(\'non-admitted city-scene yield-from\')\n\n            def visit_Call(self, node):\n                if group == \'bootstrap\':\n                    for position, (before, after) in enumerate(remaining):\n                        if _dump(node) == _dump(after):\n                            remaining.pop(position)\n                            return ast.copy_location(copy.deepcopy(before), node)\n                return self.generic_visit(node)\n\n        inverse = Inverse().visit(copy.deepcopy(derived))\n        if remaining or _dump(inverse) != _dump(original):\n            raise ValueError(\'complete city-scene FN inverse differs: \' + original.name)\n        result.body[index] = derived\n        inverses[index] = inverse\n        admissions.append((original.name, counts))\n    if len(inverses) != len(names):\n        raise ValueError(\'every finite city-scene whole owner required\')\n    restored = copy.deepcopy(result)\n    for index, inverse in inverses.items():\n        restored.body[index] = inverse\n    if _dump(restored) != _dump(original_tree):\n        raise ValueError(\'complete city-scene module inverse differs\')\n    return ast.fix_missing_locations(result), admissions', '_code_shape': "def _code_shape(code):\n    return tuple(getattr(code, name) for name in (\n        'co_code', 'co_names', 'co_varnames', 'co_argcount', 'co_posonlyargcount',\n        'co_kwonlyargcount', 'co_flags', 'co_freevars', 'co_cellvars')) + (tuple(\n            _code_shape(value) if type(value) is CodeType else value\n            for value in code.co_consts),)", '_top_code': "def _top_code(code, name):\n    found = [value for value in code.co_consts if type(value) is CodeType\n        and value.co_name == name and value.co_qualname == name]\n    if len(found) != 1:\n        raise ValueError('one complete top-level city-scene owner required: ' + name)\n    return found[0]", 'PersistentCitySceneSession': 'class PersistentCitySceneSession:\n    """Whole00300, with real device/IRQ waits propagated from one entered city.\n\n    This is an explicit additive main owner, not an implicit replacement for\n    BootstrapMainSession. Callers must select it before the00300 invocation;\n    it cannot attach by rerunning a live main prefix. No incoming return slot\n    is fabricated and the original main loop remains nonreturning.\n    """\n\n    def __init__(self, state: SceneState, frame: FirstDeploymentFrame):\n        self.state = checked_state(state)\n        self.entry = _movement_frame(state, frame)\n        if frame.status != state.sr & 31:\n            raise ValueError(\'city main entry must retain actual full SR/CCR-X\')\n        self._thread = threading.get_ident()\n        self._program, self._module, self._originals, self.admissions = _make_city_main_program(state, frame)\n        self._started = self._failed = False\n        self.waiting = None\n        self.suspensions = 0\n        self.status_word = state.sr\n\n    def _require_current(self):\n        if threading.get_ident() != self._thread:\n            raise ValueError(\'city main continuation belongs to another thread\')\n        for name, original in self._originals.items():\n            if getattr(self._module, name) is not original:\n                raise ValueError(\'actual complete main owner was rebound: \' + name)\n\n    def _take(self, returned=None):\n        from ..high_level_gameplay_flow.battle_trigger_steps import BattleTriggerWait\n        self._require_current()\n        try:\n            waiting = next(self._program) if returned is None else self._program.send(returned)\n        except StopIteration:\n            self._failed = True\n            raise Boundary(\'original nonreturning city main completed without an actual continuation\')\n        except BaseException:\n            self._failed = True\n            raise\n        allowed = (BootstrapMainWait, ControllerSetupWait, ForceTurnWait, GameplaySceneWait, ScriptedSceneWait, AllocationSceneWait, DuelSceneWait, BattleTriggerWait)\n        if type(waiting) not in allowed or waiting.state is not self.state:\n            self._failed = True\n            raise ValueError(\'an actual same-Scene main/message/load/scripted wait is required\')\n        self.waiting = waiting.validate()\n        self.status_word = self.state.sr\n        self.suspensions += 1\n        return self.waiting\n\n    def start(self):\n        self._require_current()\n        if self._started:\n            raise ValueError(\'cannot replay original00300 initialization or city prefixes\')\n        self._started = True\n        return self._take()\n\n    def _live(self):\n        self._require_current()\n        if not self._started or self._failed or self.waiting is None:\n            raise ValueError(\'one live suspended city main invocation required\')\n\n    def resume_interrupt(self, returned: FirstDeploymentFrame, pc: int):\n        self._live()\n        waiting = self.waiting\n        if type(waiting) is GameplaySceneWait and (not waiting.needs_interrupt):\n            raise ValueError(\'this scene point requires an explicit device event, not an IRQ\')\n        returned = _movement_frame(self.state, returned)\n        uint(pc, 32)\n        if pc != waiting.poll:\n            raise MovementContinuationBoundary(pc, returned, \'IRQ did not RTE to the actual city/main poll\')\n        if returned.stack_cursor.base != waiting.frame.stack_cursor.base:\n            raise Boundary(\'IRQ must preserve the suspended city physical SP\')\n        if self.state.sr != self.status_word or returned.status != self.status_word & 31:\n            raise ValueError(\'IRQ must restore the original city full SR and CCR-X\')\n        return self._take(returned)\n\n    def resume(self, returned: FirstDeploymentFrame, pc: int):\n        return self.resume_interrupt(returned, pc)\n\n    def resume_device(self, event: str):\n        self._live()\n        waiting = self.waiting\n        if type(waiting) is not GameplaySceneWait or waiting.needs_interrupt or event != waiting.event:\n            raise ValueError(\'the exact suspended city device event is required\')\n        if self.state.sr != self.status_word:\n            raise ValueError(\'device progress cannot change the original full software SR\')\n        return self._take(waiting.frame)'}}

# B157: exact city cold cache dependencies; all complete owner guards retained.
EXPECTED_SOURCES['city'].update({'_prepare_city_artifacts': "def _prepare_city_artifacts(module, group, source, filename):\n    original_tree = ast.parse(source, filename=filename)\n    plain = compile(original_tree, filename, 'exec', dont_inherit=True)\n    for name, expected_source in EXPECTED_WHOLE_SOURCES[group].items():\n        original = getattr(module, name)\n        nodes = [node for node in original_tree.body if isinstance(node, ast.FunctionDef) and node.name == name]\n        if len(nodes) != 1 or _dump(nodes[0]) != _dump(ast.parse(expected_source).body[0]) or type(original) is not FunctionType or (original.__globals__ is not vars(module)) or (original.__module__ != module.__name__) or (original.__name__ != name) or (original.__closure__ is not None) or (_code_shape(_top_code(plain, name)) != _code_shape(original.__code__)):\n            raise ValueError('actual complete city-scene owner required: ' + name)\n    derived_tree, admissions = _cooperative_module(group, original_tree)\n    derived = compile(derived_tree, filename, 'exec', dont_inherit=True)\n    return dict(plain=plain, derived=derived, admissions=admissions)"})
EXPECTED_SOURCES['artifacts'] = {'read_source_text': 'def read_source_text(module):\n    """Read the real whole file, preserving newlines; no linecache/mtime gate."""\n    filename = module.__file__\n    if type(filename) is not str or not filename:\n        raise ValueError(\'an actual source module filename is required\')\n    with Path(filename).open(\'r\', encoding=\'utf-8-sig\', newline=\'\') as stream:\n        return (filename, stream.read())', 'get_source_artifacts': 'def get_source_artifacts(family, module_name, group, *, source_text, filename, transformer_codes, expected_contract, prepare):\n    """Get fresh containers holding admitted immutable code, or build one miss.\n\n    The builder is called but never retained. ASTs, functions, bound methods,\n    modules, namespaces, Scenes and Frames cannot pass the artifact freezer.\n    Source text is compared exactly; CodeType epoch members compare by identity.\n    """\n    if any((type(value) is not str or not value for value in (family, module_name, group, filename))):\n        raise ValueError(\'explicit source artifact family/module/group/filename required\')\n    if type(source_text) is not str or type(transformer_codes) is not tuple:\n        raise ValueError(\'fresh complete source text and transformer CodeType tuple required\')\n    if not transformer_codes or any((type(code) is not CodeType for code in transformer_codes)):\n        raise ValueError(\'actual transformer/validator CodeType identities required\')\n    epoch = (filename, source_text, transformer_codes, _freeze(expected_contract))\n    key = (family, module_name, group)\n    with _LOCK:\n        retained = _CURRENT.get(key)\n    if retained is not None and _same_epoch(retained[0], epoch):\n        return _thaw(retained[1])\n    artifact = _freeze(prepare())\n    with _LOCK:\n        _CURRENT[key] = (epoch, artifact)\n    return _thaw(artifact)', '_freeze': "def _freeze(value):\n    if type(value) in _SCALARS or type(value) is CodeType:\n        return ('leaf', type(value), value)\n    if type(value) is dict:\n        return ('dict', tuple(((_freeze(key), _freeze(item)) for key, item in value.items())))\n    if type(value) in (list, tuple):\n        return ('list' if type(value) is list else 'tuple', tuple(map(_freeze, value)))\n    if type(value) in (set, frozenset):\n        return ('set' if type(value) is set else 'frozenset', frozenset(map(_freeze, value)))\n    raise ValueError('source artifacts may contain only CodeTypes and immutable declarations')", '_thaw': "def _thaw(value):\n    kind = value[0]\n    if kind == 'leaf':\n        return value[2]\n    if kind == 'dict':\n        return {_thaw(key): _thaw(item) for key, item in value[1]}\n    items = (_thaw(item) for item in value[1])\n    return {'list': list, 'tuple': tuple, 'set': set, 'frozenset': frozenset}[kind](items)", '_same_epoch': 'def _same_epoch(left, right):\n    return left[:2] == right[:2] and left[3] == right[3] and (len(left[2]) == len(right[2])) and all((before is after for before, after in zip(left[2], right[2])))'}


def _dump(node):
    return ast.dump(node, include_attributes=False)


def _code_shape(code):
    return tuple(getattr(code, name) for name in (
        'co_code', 'co_names', 'co_varnames', 'co_argcount', 'co_posonlyargcount',
        'co_kwonlyargcount', 'co_flags', 'co_freevars', 'co_cellvars')) + (tuple(
            _code_shape(value) if type(value) is CodeType else value
            for value in code.co_consts),)


def _named_code(parent, name):
    found = [value for value in parent.co_consts
        if type(value) is CodeType and value.co_name == name]
    if len(found) != 1:
        raise ValueError('one complete named source code owner required: ' + name)
    return found[0]


def _pin_sources():
    """Compare complete source/actual code once; do not execute module bodies."""
    modules = {'boot': business_boot, 'reset': bootstrap_reset, 'city': city_scene_steps,
        'artifacts': source_artifact_cache}
    pins = []
    for group, module in modules.items():
        tree = ast.parse(inspect.getsource(module), filename=module.__file__)
        plain = compile(tree, module.__file__, 'exec', dont_inherit=True)
        for name, expected in EXPECTED_SOURCES[group].items():
            nodes = [node for node in tree.body
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name == name]
            if len(nodes) != 1 or _dump(nodes[0]) != _dump(ast.parse(expected).body[0]):
                raise ValueError('complete reviewed cold/city source differs: ' + name)
            owner = getattr(module, name)
            code = _named_code(plain, name)
            if isinstance(nodes[0], ast.FunctionDef):
                if (type(owner) is not FunctionType or owner.__globals__ is not vars(module)
                        or owner.__module__ != module.__name__ or owner.__name__ != name
                        or owner.__closure__ is not None
                        or _code_shape(owner.__code__) != _code_shape(code)):
                    raise ValueError('actual complete unwrapped cold/city function required: ' + name)
                pins.append((module, name, owner, ((None, owner, owner.__code__),)))
            else:
                if type(owner) is not type or owner.__module__ != module.__name__ or owner.__name__ != name:
                    raise ValueError('actual exact city main class required')
                methods = []
                for node in nodes[0].body:
                    if not isinstance(node, ast.FunctionDef):
                        continue
                    function = vars(owner).get(node.name)
                    if (type(function) is not FunctionType or function.__globals__ is not vars(module)
                            or function.__closure__ is not None
                            or _code_shape(function.__code__) != _code_shape(_named_code(code, node.name))):
                        raise ValueError('actual complete city main method required: ' + node.name)
                    methods.append((node.name, function, function.__code__))
                pins.append((module, name, owner, tuple(methods)))
    for name in ('read_source_text', 'get_source_artifacts'):
        original = getattr(source_artifact_cache, name)
        if getattr(city_scene_steps, name) is not original:
            raise ValueError('city source artifact alias differs from its exact owner: ' + name)
        # The defining function was checked above against its complete source;
        # this second binding keeps the importing alias under the same live
        # identity and CodeType guard without changing the existing pin ABI.
        pins.append((city_scene_steps, name, original, ((None, original, original.__code__),)))
    return tuple(pins)


def _require_pins(pins):
    for module, name, owner, methods in pins:
        if getattr(module, name) is not owner:
            raise Boundary('actual cold/city source owner was rebound: ' + name)
        for method_name, function, code in methods:
            if ((method_name is not None and vars(owner).get(method_name) is not function)
                    or function.__code__ is not code):
                raise Boundary('actual cold/city source code changed: ' + name)


def _clone_tail_binding(original, view, facade):
    """Same exact generator CodeType; one private global value differs."""
    if (type(original) is not FunctionType or original is not business_boot.reset_console_frame_fields
            or type(view) is not FunctionType or not inspect.isgeneratorfunction(view)
            or view.__closure__ is not None or view.__code__.co_freevars
            or view.__globals__.get('start_game_main_loop_frame_fields') is not
                business_boot.start_game_main_loop_frame_fields):
        raise Boundary('actual complete original reset view and unmodified tail binding required')
    namespace = dict(view.__globals__)
    namespace['start_game_main_loop_frame_fields'] = facade
    if set(namespace) != set(view.__globals__):
        raise Boundary('no additional reset namespace names may be invented')
    changed = tuple(name for name in namespace if namespace[name] is not view.__globals__[name])
    if changed != ('start_game_main_loop_frame_fields',):
        raise Boundary('only the exact reset-to00300 binding may differ')
    result = FunctionType(view.__code__, namespace, view.__name__, view.__defaults__, None)
    result.__kwdefaults__ = view.__kwdefaults__
    result.__annotations__ = dict(view.__annotations__)
    if result.__code__ is not view.__code__ or not inspect.isgeneratorfunction(result):
        raise Boundary('whole reset generator code must remain identical')
    return result


class CityColdResetSession(PersistentColdResetSession):
    """One original206 invocation, choosing its city main before actual00300.

    The base reset protocol and exact ResetAudioReleasePoint are retained.
    No old BootstrapMainSession or installation authority guard is relaxed.
    This new class has its own explicit nonreturning tail handoff contract.
    """

    def __init__(self, state, frame, profile):
        self._source_pins = _pin_sources()
        super().__init__(state, frame, profile)
        self._base_factory = self.program_factory
        self._main_code = None
        self._entered_main = False
        self.initial_device_waits = ()
        self.first_main_wait = None
        self.first_main_suspensions = None
        self.program_factory = _clone_tail_binding(self.original, self._base_factory, self._city_main_tail)
        self.source_contract = dict(self.source_contract,
            confidence='confirmed_static_whole_reset_view_private_tail_binding',
            callee_or_global_replacement=True, module_global_replacement=False,
            private_namespace_changed_names=('start_game_main_loop_frame_fields',),
            warm_and_cold_tail_calls=2, reset_generator_CodeType_identical=True,
            selected_main='PersistentCitySceneSession', additional_physical_CALL_slots=0)

    def _guard(self):
        super()._guard()
        _require_pins(self._source_pins)

    def _city_main_tail(self, state, frame):
        self._guard()
        if state is not self.state or self._entered_main or self.main_session is not None:
            raise Boundary('one original reset tail may enter its actual00300 once')
        frame = _movement_frame(state, frame)
        self._entered_main = True
        main = city_scene_steps.PersistentCitySceneSession(state, frame)
        self.main_session = main
        self._main_code = main._program.gi_code
        waiting = main.start()
        while type(waiting) is GameplaySceneWait:
            self._progress_initial_device(main, waiting)
            waiting = main.resume_device(waiting.event)
        if (type(waiting) is not BootstrapMainWait or waiting is not main.waiting
                or waiting.state is not state or waiting.poll != 0x3BC
                or main.suspensions != len(self.initial_device_waits) + 1):
            raise Boundary('original00300 must reach its first actual3BC after its startup devices')
        self.first_main_wait = waiting
        self.first_main_suspensions = main.suspensions
        boundary = MovementContinuationBoundary(waiting.poll, waiting.frame,
            'actual original reset tail retains the preselected city main at3BC')
        boundary.city_cold_reset_session = self
        boundary.city_main_session = main
        boundary.city_main_wait = waiting
        raise boundary

    def _progress_initial_device(self, main, waiting):
        """Consume only the actual startup sprite-DMA supply already bound.

        Original00300 writes request4 before its first3BC. Its indexed CALL
        enters3D8, then93F0/4EE and68CE/9408. The physical three return LONGs
        stay on the original stack throughout every68FA busy-bit poll.
        """
        self._guard()
        if (type(main) is not city_scene_steps.PersistentCitySceneSession
                or main is not self.main_session or waiting is not main.waiting
                or type(waiting) is not GameplaySceneWait or waiting.state is not self.state
                or waiting.needs_interrupt or (waiting.event, waiting.poll) != ('vdp-dma', 0x68FA)
                or main.suspensions != len(self.initial_device_waits) + 1):
            raise Boundary('one actual initial3D8/93F0 sprite-DMA continuation required')
        waiting.validate()
        stack = waiting.frame.stack_cursor
        if stack.base != 0x00FFFDF4:
            raise Boundary('initial sprite DMA must retain the real startup physical SP')
        # Observe the shared live backing for a host witness, not extra CPU
        # DATA reads that would change the original event stream/read budget.
        start = stack.base & 65535
        slots = tuple(int.from_bytes(self.state.ram[start + offset:start + offset + 4], 'big')
            for offset in (0, 4, 8))
        if slots != (0x9408, 0x4EE, 0x3CE):
            raise Boundary('initial sprite DMA must retain all three real startup CALL slots')
        self.initial_device_waits += (waiting,)
        # This routes to the existing same-Scene finite SuppliedVideoEvents.
        # Missing/exhausted slots remain a Boundary; no transfer is invented.
        self.state.progress(waiting.event)

    def _advance(self, frame=None):
        self._guard()
        try:
            point = next(self.program) if frame is None else self.program.send(frame)
        except MovementContinuationBoundary as boundary:
            main = getattr(boundary, 'city_main_session', None)
            waiting = getattr(boundary, 'city_main_wait', None)
            if (getattr(boundary, 'city_cold_reset_session', None) is not self
                    or type(main) is not city_scene_steps.PersistentCitySceneSession
                    or main is not self.main_session or type(waiting) is not BootstrapMainWait
                    or waiting is not main.waiting or waiting.state is not self.state
                    or boundary.target != waiting.poll or boundary.context is not waiting.frame):
                self.failed = True
                raise
            self.waiting, self.phase = waiting, 'original-main-tail'
            self.require_main_identity(main, waiting)
            self.events.append(('actual_original300_city_tail_handoff', waiting.poll,
                waiting.frame.stack_cursor.base, main.suspensions))
            return waiting
        except StopIteration as completion:
            self.failed = True
            raise Boundary('original nonreturning206/city00300 unexpectedly returned') from completion
        except BaseException:
            self.failed = True
            raise
        if type(point) is not ResetAudioReleasePoint or point.session is not self:
            self.failed = True
            raise Boundary('city reset yielded no actual original260/262 release point')
        self.waiting, self.phase = point, 'actual-audio-release'
        self.events.append(('completed_original260_suspend_before262', point.pc,
            point.frame.stack_cursor.base, point.full_sr))
        return point

    def require_main_identity(self, main, waiting):
        """Read-only exact same-invocation/source witness; return actual CodeType.

        The installation capture can keep its own first3BC/SP/suspension tests;
        this method proves which real, whole-derived main generator owns it.
        It grants nothing and does not read RAM, chips or cartridge DATA.
        """
        self._guard()
        if (self.phase != 'original-main-tail' or not self._entered_main
                or type(main) is not city_scene_steps.PersistentCitySceneSession
                or main is not self.main_session or main.state is not self.state
                or waiting is not self.waiting or waiting is not main.waiting
                or waiting.state is not self.state or main._failed
                or type(main._program) is not GeneratorType or main._program.gi_running
                or type(self._main_code) is not CodeType or main._program.gi_code is not self._main_code):
            raise Boundary('exact original-reset/preselected-city-main source handoff required')
        main._require_current()
        waiting.validate()
        return self._main_code

    def require_first_main_wait(self, main, waiting):
        """Prove this invocation's first3BC, not a one-suspension shortcut."""
        self.require_main_identity(main, waiting)
        if (type(waiting) is not BootstrapMainWait or waiting.poll != 0x3BC
                or waiting is not self.first_main_wait
                or main.suspensions != self.first_main_suspensions
                or self.first_main_suspensions != len(self.initial_device_waits) + 1
                or waiting.frame.stack_cursor.base != 0x00FFFE00):
            raise Boundary('the retained actual initial-device-to-first3BC witness is required')
        return True

    def resume_main(self, frame, pc):
        self._guard()
        self.require_main_identity(self.main_session, self.waiting)
        self.waiting = self.main_session.resume(frame, pc)
        return self.waiting

    def resume_device(self, event):
        self._guard()
        self.require_main_identity(self.main_session, self.waiting)
        self.waiting = self.main_session.resume_device(event)
        return self.waiting
