"""Whole strategic Main484/488 parents and their actual nested waits.

Only finite existing calls become yield-from in private complete source
modules. All algorithms, real CALL/RTS slots, live fields and source owners
remain original; the old ForceTurnSession and its strict wait set are untouched.
"""
import ast
import copy
import importlib
import inspect
from types import CodeType, FunctionType

from .battle_trigger_steps import BattleScenePrograms
from .message_scene_steps import GameplayMessageScenePrograms
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary


MODULE_PATHS = {
    'main': 'tools.high_level_main_flows.business_main',
    'commands': 'tools.high_level_main_flows.business_commands',
    'support': 'tools.high_level_main_flows.business_scene_support',
}
VIEW_SPECS = {
    'main': {
        'initialize_support_command_screen_fields': {'_campaign_call_fields': 2},
        'initialize_support_result_screen_fields': {'_campaign_call_fields': 2},
    },
    'commands': {
        '_diplomacy_first_force_turn_fields': {
            'display_call_fields': 7, '_diplomacy_second_force_turn_fields': 1,
            '_diplomacy_show_owner_packet_fields': 1},
        '_diplomacy_second_force_turn_fields': {
            'display_call_fields': 12, '_diplomacy_show_owner_packet_fields': 1},
        '_diplomacy_show_owner_packet_fields': {'display_call_fields': 2},
    },
}
MAIN_ENTRIES = {
    0x484: 'initialize_support_command_screen_fields',
    0x488: 'initialize_support_result_screen_fields',
}
CAMPAIGN_PAIRS = ((0x30960, 0xD56), (0x34F26, 0xD68))
CAMPAIGN_REFRESH_PAIRS = ((0xAF48, 0xD5C), (0xAF48, 0xD6E))
FORCE_REFRESH_PAIRS = ((0xAF48, 0x309DE), (0xAF48, 0x30B8C))

# Complete current function text, injected by the private source producer.
EXPECTED_SOURCE = {'main': {'initialize_support_command_screen_fields': 'def initialize_support_command_screen_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """484: initialize support command screen; original stage and child tokens."""\n    frame=_city_ui_frame_fields(state,frame,0x484)\n    state.sr=0x2700\n    frame=first_replace(frame,status=0)\n    frame=_campaign_call_fields(state,frame,0x30960,0xD56)\n    frame=_campaign_call_fields(state,frame,0xAF48,0xD5C)\n    return frame', 'initialize_support_result_screen_fields': 'def initialize_support_result_screen_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """488: initialize support result screen; original stage and child tokens."""\n    frame=_city_ui_frame_fields(state,frame,0x488)\n    state.sr=0x2700\n    frame=first_replace(frame,status=0)\n    frame=_campaign_call_fields(state,frame,0x34F26,0xD68)\n    frame=_campaign_call_fields(state,frame,0xAF48,0xD6E)\n    return frame'}, 'commands': {'_diplomacy_first_force_turn_fields': 'def _diplomacy_first_force_turn_fields(state: SceneState,\n        frame: FirstDeploymentFrame, prefix: bool) -> FirstDeploymentFrame:\n    """30960/3096E: preserve the real player/non-player loop and two tails."""\n    from .business_movement_support import _movement_compare\n    frame = display_frame_fields(state, frame)\n    if type(prefix) is not bool:\n        raise ValueError(\'actual30960 or3096E entry required\')\n    if prefix:\n        frame = _movement_compare(state, frame, state.read(0xFFFFF36C, 2), 2, 16)\n        if not frame.status & 1:\n            return _diplomacy_second_force_turn_fields(state, frame, True)\n        frame = display_call_fields(state, frame, 0x30EB4, 0x3096E)\n    while True:\n        frame = display_call_fields(state, frame, 0x30F26, 0x30972)\n        frame = display_move_fields(state, frame, \'target_x\', state.read(0xFFFFF376, 2))\n        if frame.status & 8:\n            frame = display_call_fields(state, frame, 0x311E6, 0x309A6)\n            return display_call_fields(state, frame, 0xAF48, 0x309DE)\n        frame, owned = _diplomacy_owner_matches_fields(state, frame)\n        if not owned:\n            frame = display_store_fields(state, frame, 0x30992, 0xFFFFF362, 2)\n            frame = display_call_fields(state, frame, 0x30A74, 0x3099C)\n            frame = display_call_fields(state, frame, 0x30FAA, 0x309A0)\n            continue\n        frame = display_call_fields(state, frame, 0x309FC, 0x309AE)\n        if frame.status & 1:\n            continue\n        frame = display_store_fields(state, frame, 0x309B0, 0xFFFFF612, 0x20B)\n        frame = display_store_fields(state, frame, 0x309B6, 0xFFFFF362, 4)\n        frame = display_store_fields(state, frame, 0x309BC, 0xFFFFF36C, 0, clear=True)\n        return _diplomacy_show_owner_packet_fields(state, frame, False)', '_diplomacy_second_force_turn_fields': 'def _diplomacy_second_force_turn_fields(state: SceneState,\n        frame: FirstDeploymentFrame, prefix: bool) -> FirstDeploymentFrame:\n    """30ABE/30AC6: original second turn, fallback lookup and stock notices."""\n    frame = display_frame_fields(state, frame)\n    if type(prefix) is not bool:\n        raise ValueError(\'actual30ABE or30AC6 entry required\')\n    if prefix:\n        frame = display_store_fields(state, frame, 0x30ABE, 0xFFFFF724, 0, clear=True)\n        frame = display_call_fields(state, frame, 0x30EB4, 0x30AC6)\n    while True:\n        frame = display_call_fields(state, frame, 0x30F26, 0x30ACA)\n        frame = display_move_fields(state, frame, \'target_x\', state.read(0xFFFFF376, 2))\n        if frame.status & 8:\n            frame = display_call_fields(state, frame, 0x311FA, 0x30B04)\n            frame = display_call_fields(state, frame, 0x1631A, 0x30B0A)\n            frame = display_store_fields(state, frame, 0x30B0A, 0xFFFFF612, 0x209)\n            frame = display_store_fields(state, frame, 0x30B10, 0xFFFFF362, 5)\n            frame = display_store_fields(state, frame, 0x30B16, 0xFFFFF36C, 3)\n            frame = display_store_fields(state, frame, 0x30B1C, 0xFFFF9F00, 0xFFFF)\n            frame = display_call_fields(state, frame, 0x30F54, 0x30B26)\n            frame = display_call_fields(state, frame, 0x30C3A, 0x30B2A)\n            frame = _diplomacy_save_notice_fields(state, frame, True)\n            return display_call_fields(state, frame, 0xAF48, 0x30B8C)\n        frame, owned = _diplomacy_owner_matches_fields(state, frame)\n        if not owned:\n            frame = display_store_fields(state, frame, 0x30AEA, 0xFFFFF362, 2)\n            frame = display_call_fields(state, frame, 0x30A74, 0x30AF2)\n            frame = display_call_fields(state, frame, 0x31024, 0x30AF6)\n            frame = display_store_fields(state, frame, 0x30AF6, 0xFFFFF75A, 0, clear=True)\n            frame = display_call_fields(state, frame, 0x31044, 0x30AFE)\n            continue\n        frame = display_store_fields(state, frame, 0x30B4C, 0xFFFFF612, 0x20B)\n        frame = display_store_fields(state, frame, 0x30B52, 0xFFFFF362, 4)\n        frame = display_call_fields(state, frame, 0x309FC, 0x30B5C)\n        if frame.status & 1:\n            frame = display_call_fields(state, frame, 0x30B8E, 0x30B64)\n            if frame.status & 1:\n                continue\n        frame = display_store_fields(state, frame, 0x30B68, 0xFFFFF380, 0x85)\n        return _diplomacy_show_owner_packet_fields(state, frame, True)', '_diplomacy_show_owner_packet_fields': 'def _diplomacy_show_owner_packet_fields(state: SceneState,\n        frame: FirstDeploymentFrame, second: bool) -> FirstDeploymentFrame:\n    """The original309D2/30B80 sprite WORD packet and true AF48 tail."""\n    frame = display_move_fields(state, frame, \'target_x\', 0xC0000026, 32)\n    frame = display_move_fields(state, frame, \'target_y\', 7)\n    frame = display_move_fields(state, frame, \'unit\', 0xCA02)\n    frame = display_address_fields(state, frame, \'roster\', 0x309E0)\n    frame = display_call_fields(state, frame, 0x26BFA, 0x30B86 if second else 0x309D8)\n    return display_call_fields(state, frame, 0xAF48, 0x30B8C if second else 0x309DE)'}}
EXPECTED_SYNCHRONOUS_SOURCE = {'main': {}, 'commands': {'_diplomacy_owner_matches_fields': 'def _diplomacy_owner_matches_fields(state: SceneState,\n        frame: FirstDeploymentFrame) -> tuple[FirstDeploymentFrame, bool]:\n    """Three ordered CMP.Ws stop immediately at the actual matching owner."""\n    from .business_movement_support import _movement_compare\n    for address in (0xFFFFF67A, 0xFFFFF67C, 0xFFFFF67E):\n        frame = _movement_compare(state, frame, low16(frame.target_x), state.read(address, 2), 16)\n        if frame.status & 4:\n            return frame, True\n    return frame, False', '_diplomacy_save_notice_fields': 'def _diplomacy_save_notice_fields(state: SceneState,\n        frame: FirstDeploymentFrame, second: bool) -> FirstDeploymentFrame:\n    """E098/30B2C ordered saved notices; no extra source RAM read."""\n    frame = display_store_fields(state, frame, 0x30B2C if second else 0xE09C,\n        0xFFFFF3C2, state.read(0xFFFFF612, 2))\n    frame = display_store_fields(state, frame, 0x30B32 if second else 0xE0A2,\n        0xFFFFF3C4, state.read(0xFFFFF362, 2))\n    frame = display_store_fields(state, frame, 0x30B38 if second else 0xE0A8, 0xFFFFF612, 0x208)\n    frame = display_store_fields(state, frame, 0x30B3E if second else 0xE0AE, 0xFFFFF362, 0x13)\n    frame = display_store_fields(state, frame, 0x30B44 if second else 0xE0B4, 0xFFFFF36A, 0, clear=True)\n    return frame'}, 'support': {'begin_auxiliary_command_stage_fields': 'def begin_auxiliary_command_stage_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    frame=_resource_cost_frame(state,frame,0x34F26)\n    frame=_aux_text_call_fields(state,frame,0x34F36,0x34F2A)\n    frame=_setup_write_fields(state,frame,0xFFFFF728,1)\n    return _aux_text_call_fields(state,frame,0x34F64,0x34F34)', 'load_active_packet_roster_fields': 'def load_active_packet_roster_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """34F36..34F64: copy the active packet\'s reverse roster into F72A.\n\n    The packet\'s low nibble is the original WORD counter, not a validated\n    Python length.  A zero nibble retains the original SUBQ/DBRA underflow.\n    The caller owns its existing return LONG; this leaf does not pop it.\n    """\n    frame = _resource_cost_frame(state, frame, 216886)\n    frame = first_replace(frame, roster=state.table_at(state.read(16726060, 4)).cursor(), candidates=state.table_at(4294965034).cursor())\n    frame = _movement_move(state, frame, \'target_y\', 0, 16)\n    frame = _movement_move(state, frame, \'target_y\', frame.roster.byte(0, 4), 8)\n    frame = _setup_write_fields(state, frame, 4294964086, low16(frame.target_y))\n    frame = _movement_move(state, frame, \'target_x\', frame.roster.byte(), 8)\n    frame = _movement_move(state, frame, \'target_x\', low16(frame.target_x) & 15, 16)\n    frame = _map_presentation_arithmetic_fields(state, frame, \'target_x\', 1, True)\n    while True:\n        frame = _movement_move(state, frame, \'target_y\', 0, 16)\n        frame = _movement_move(state, frame, \'target_y\', frame.roster.byte(low16(frame.target_x), 13), 8)\n        frame = _setup_write_fields(state, frame, frame.candidates.base, low16(frame.target_y))\n        frame = first_replace(frame, candidates=frame.candidates.advance(2))\n        frame, again = _map_presentation_db_fields(frame, \'target_x\')\n        if not again:\n            break\n    return _setup_write_fields(state, frame, frame.candidates.base, 65535)', 'dispatch_auxiliary_command_stage_fields': 'def dispatch_auxiliary_command_stage_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    return _aux_text_dispatch_stage_fields(state,_resource_cost_frame(state,frame,0x34F64),0x34F7C,0x34F94,0x34F78)', '_aux_text_dispatch_stage_fields': 'def _aux_text_dispatch_stage_fields(state: SceneState, frame: FirstDeploymentFrame,\n        table: Long, base: Long, token: Long) -> FirstDeploymentFrame:\n    """Live stage is reread on every original backwards branch, not a cached selector."""\n    while True:\n        frame=_movement_move(state,frame,\'target_x\',state.read(0xFFFFF728,2),16)\n        if frame.status&8:return frame\n        frame=_map_presentation_arithmetic_fields(state,frame,\'target_x\',1,True)\n        frame=_movement_fixed_shift_word(state,frame,\'target_x\',1)\n        frame=_movement_move(state,frame,\'target_x\',state.table_at(table).word(low16(frame.target_x)),16)\n        frame=_aux_text_call_fields(state,frame,u32(base+s16(low16(frame.target_x))),token)', '_aux_text_call_fields': "def _aux_text_call_fields(state: SceneState, frame: FirstDeploymentFrame, target: Long, continuation: Long) -> FirstDeploymentFrame:\n    frame = _resource_cost_frame(state, frame, target)\n    stack = frame.stack_cursor.advance(-4)\n    stack.set_long(0, continuation)\n    entered = first_replace(frame, stack_cursor=stack)\n    children = {216932: dispatch_auxiliary_command_stage_fields, 218130: expand_glyph_tile_sequence_fields, 218232: calculate_glyph_row_layout_fields, 218256: select_glyph_bitmap_fields, 218290: expand_monochrome_glyph_byte_fields, 218314: upload_expanded_glyph_rows_fields, 218692: draw_auxiliary_text_panel_border_fields, 218778: draw_auxiliary_text_panel_rows_fields, 218866: upload_auxiliary_text_panel_glyphs_fields, 218944: draw_auxiliary_text_panel_markers_fields, 240310: decode_unmasked_literal_plane_fields, 240322: decode_high_plane_rows_fields, 243604: dispatch_repeating_scene_presentation_fields, 252652: initialize_object_scene_video_fields, 216886: load_active_packet_roster_fields}\n    if target in children:\n        result = children[target](state, entered)\n    elif target == 240334:\n        result = read_vdp_plane_rle_rows_fields(SceneRefreshMemory(state), entered)\n    elif target == 240466:\n        result = write_vdp_swapped_byte_rle_stream_fields(SceneRefreshMemory(state), entered)\n    elif target == 240532:\n        result = copy_scene_palette_variant_fields(SceneRefreshMemory(state), entered)\n    elif target == 240266:\n        result = snapshot_and_clear_scene_palette_fields(SceneRefreshMemory(state), entered)\n    elif target == 26830:\n        from ..high_level_gameplay_flow.business_services import clear_video_sprite_plane_fields\n        result = clear_video_sprite_plane_fields(SceneRefreshMemory(state), entered)\n    elif target == 32906:\n        from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields\n        result = enqueue_sound_command_fields(SceneRefreshMemory(state), entered)\n    elif target == 418260:\n        from ..high_level_dynamic_flows.business_actions import upload_portrait_tiles_frame_fields\n        result = upload_portrait_tiles_frame_fields(state, entered)\n    elif target == 33736:\n        from ..high_level_gameplay_flow.business_services import wait_for_scene_sound_byte_fields\n        result = wait_for_scene_sound_byte_fields(SceneRefreshMemory(state), entered)\n    elif target == 242312:\n        from ..high_level_scene_flows.business_objects import append_scene_center_marker_fields\n        result = append_scene_center_marker_fields(SceneRefreshMemory(state), entered)\n    elif target == 239992:\n        from ..high_level_scene_flows.business_scene import advance_scene_palette_fade_fields\n        result = advance_scene_palette_fade_fields(SceneRefreshMemory(state), entered)\n    elif target == 242236:\n        from ..high_level_scene_flows.business_scene import finish_actor_sprite_chains_fields\n        result = finish_actor_sprite_chains_fields(SceneRefreshMemory(state), entered)\n    elif target in (211180, 211262, 211336, 211404, 211444, 211472, 211640, 212394, 213232) and continuation == 211158:\n        from ..high_level_ai_policy_v2.business_scene_routes import execute_march_policy_fields\n        result = execute_march_policy_fields(state, entered, target)\n    elif target in (213312, 213424, 213694, 213878, 214078, 214120, 214330, 214520, 214600, 214634, 214704, 214810, 215166, 215342, 215538, 215596, 216016, 216074, 216402, 216482, 216526, 216834, 216842) and continuation == 213260:\n        from ..high_level_ai_policy_v2.business_scene_packet_policy import execute_packet_policy_fields\n        result = execute_packet_policy_fields(state, entered, target)\n    elif target in (216980, 217188, 217320, 217394, 217428, 217506, 217616, 217734, 217922, 218044, 218092, 218100) and continuation == 216952:\n        from ..high_level_ai_policy_v2.business_scene_active_packets import execute_active_packet_fields\n        result = execute_active_packet_fields(state, entered, target)\n    else:\n        raise MovementContinuationBoundary(target, entered, 'auxiliary text child lacks a complete admitted frame')\n    result = _resource_cost_frame(state, result, target)\n    token = result.stack_cursor.long()\n    if token != continuation:\n        raise MovementContinuationBoundary(token, result, 'auxiliary text RTS slot changed')\n    state.sr = state.sr & 65504 | result.status\n    return first_replace(result, stack_cursor=result.stack_cursor.advance(4))"}}
ORIGINAL_REAL_CALLS = ((199008, 3414), (44872, 3420), (216870, 3432), (44872, 3438), (200372, 199022), (200486, 199026), (199284, 199068), (200618, 199072), (201190, 199078), (199164, 199086), (158714, 199128), (44872, 199134), (44872, 199308), (1548, 199334), (200372, 199366), (200486, 199370), (199284, 199410), (200740, 199414), (200772, 199422), (201210, 199428), (90906, 199434), (200532, 199462), (199738, 199466), (199164, 199516), (199566, 199524), (158714, 199558), (44872, 199564), (216886, 216874), (216932, 216884))


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
        raise ValueError('one complete top-level strategic source owner required: ' + name)
    return found[0]


def _cooperative_module(group, original_tree):
    """Only five declared complete owners; full function and module inverses."""
    if group not in VIEW_SPECS:
        raise ValueError('only the two finite strategic source modules are lifted')
    result = copy.deepcopy(original_tree)
    inverses = {}
    for index, original in enumerate(original_tree.body):
        if not isinstance(original, ast.FunctionDef) or original.name not in VIEW_SPECS[group]:
            continue
        expected = ast.parse(EXPECTED_SOURCE[group][original.name]).body
        if len(expected) != 1 or _dump(original) != _dump(expected[0]):
            raise ValueError('complete strategic source differs: ' + original.name)
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
            raise ValueError('exact strategic propagation count differs: ' + original.name)
        pending = list(replacements)

        class Inverse(ast.NodeTransformer):
            def visit_YieldFrom(self, node):
                for position, (before, after) in enumerate(pending):
                    if _dump(node) == _dump(after):
                        pending.pop(position)
                        return ast.copy_location(copy.deepcopy(before), node)
                raise ValueError('non-admitted strategic yield-from')

        inverse = Inverse().visit(copy.deepcopy(derived))
        if pending or _dump(inverse) != _dump(original):
            raise ValueError('whole strategic function inverse differs: ' + original.name)
        result.body[index] = derived
        inverses[index] = inverse
    if len(inverses) != len(VIEW_SPECS[group]):
        raise ValueError('all finite strategic whole owners required')
    restored = copy.deepcopy(result)
    for index, inverse in inverses.items():
        restored.body[index] = inverse
    if _dump(restored) != _dump(original_tree):
        raise ValueError('whole strategic source-module inverse differs')
    return ast.fix_missing_locations(result)


class StrategicScenePrograms(BattleScenePrograms):
    """Only actual Main484/488; all prior battle/command fallbacks are retained."""

    def __init__(self, state):
        super().__init__(state)
        self.strategy_modules = {group: importlib.import_module(path) for group, path in MODULE_PATHS.items()}
        self.strategy_originals = {}
        self.strategy_codes = {}
        self.strategy_views = {}
        self.strategy_namespaces = {}
        for group, module in self.strategy_modules.items():
            tree = ast.parse(inspect.getsource(module), filename=module.__file__)
            plain = compile(tree, module.__file__, 'exec', dont_inherit=True)
            expected = dict(EXPECTED_SYNCHRONOUS_SOURCE.get(group, {}))
            expected.update(EXPECTED_SOURCE.get(group, {}))
            for name, text in expected.items():
                nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
                original = getattr(module, name)
                if (len(nodes) != 1 or _dump(nodes[0]) != _dump(ast.parse(text).body[0])
                        or type(original) is not FunctionType or original.__globals__ is not vars(module)
                        or original.__module__ != module.__name__ or original.__name__ != name
                        or original.__closure__ is not None or original.__code__.co_freevars
                        or _code_shape(_top_code(plain, name)) != _code_shape(original.__code__)):
                    raise ValueError('actual complete unwrapped strategic owner required: ' + name)
                self.strategy_originals[group, name] = original
                self.strategy_codes[group, name] = original.__code__
            if group not in VIEW_SPECS:
                continue
            derived = compile(_cooperative_module(group, tree), module.__file__, 'exec', dont_inherit=True)
            namespace = dict(vars(module))
            self.strategy_namespaces[group] = namespace
            for name in VIEW_SPECS[group]:
                original = self.strategy_originals[group, name]
                view = FunctionType(_top_code(derived, name), namespace, name, original.__defaults__, None)
                view.__kwdefaults__ = original.__kwdefaults__
                view.__annotations__ = dict(original.__annotations__)
                if not inspect.isgeneratorfunction(view) or view.__closure__ is not None:
                    raise ValueError('strategic whole source view must be closure-free generator')
                namespace[name] = self.strategy_views[group, name] = view
        self.strategy_namespaces['main']['_campaign_call_fields'] = self.views['main', '_campaign_call_fields']
        self.strategy_namespaces['commands']['display_call_fields'] = self.views['display', 'display_call_fields']
        self.strategy_view_owners = dict(self.strategy_views)
        self.strategy_view_codes = {key: view.__code__ for key, view in self.strategy_views.items()}
        keys = tuple(self.strategy_views) + (('main', '_campaign_call_fields'), ('commands', 'display_call_fields'))
        self.strategy_bindings = {(group, name): self.strategy_namespaces[group][name] for group, name in keys}
        self.message_scene = GameplayMessageScenePrograms(self)

    def require_current(self, state):
        super().require_current(state)
        if hasattr(self, 'strategy_originals'):
            for (group, name), original in self.strategy_originals.items():
                if (getattr(self.strategy_modules[group], name) is not original
                        or original.__code__ is not self.strategy_codes[group, name]):
                    raise ValueError('actual strategic source owner was rebound: ' + name)
        if hasattr(self, 'strategy_view_owners'):
            if self.strategy_views.keys() != self.strategy_view_owners.keys():
                raise ValueError('finite strategic continuation graph changed')
            for key, view in self.strategy_view_owners.items():
                if self.strategy_views[key] is not view or view.__code__ is not self.strategy_view_codes[key]:
                    raise ValueError('complete strategic continuation changed: ' + key[1])
            for (group, name), value in self.strategy_bindings.items():
                if self.strategy_namespaces[group].get(name) is not value:
                    raise ValueError('private strategic continuation binding changed: ' + name)

    def _scene_message(self, memory, frame):
        self.require_current(memory.state)
        return (yield from self._message_waits(self.message_scene.program(memory, frame)))

    def _campaign_child(self, state, frame, target, continuation):
        self.require_current(state)
        if (target, continuation) == (0x30960, 0xD56):
            return (yield from self.strategy_views['commands', '_diplomacy_first_force_turn_fields'](state, frame, True))
        if (target, continuation) == (0x34F26, 0xD68):
            # All third-directory algorithms are mature full-frame synchronous
            # owners. Do not manufacture a generator or replay their prefix.
            return self.strategy_originals['support', 'begin_auxiliary_command_stage_fields'](state, frame)
        if (target, continuation) in CAMPAIGN_REFRESH_PAIRS:
            from .contexts_services import SceneRefreshMemory
            return (yield from self._refresh(SceneRefreshMemory(state), frame))
        return (yield from super()._campaign_child(state, frame, target, continuation))

    def _display_child(self, state, frame, target, continuation):
        self.require_current(state)
        if target in MAIN_ENTRIES:
            if continuation != 0x3CE:
                raise MovementContinuationBoundary(target, frame, 'strategic Main parent requires actual3CE LONG')
            return (yield from self.strategy_views['main', MAIN_ENTRIES[target]](state, frame))
        if (target, continuation) in FORCE_REFRESH_PAIRS:
            from .contexts_services import SceneRefreshMemory
            return (yield from self._refresh(SceneRefreshMemory(state), frame))
        return (yield from super()._display_child(state, frame, target, continuation))

    def main_scene_call(self, state, frame, target, continuation):
        if target not in MAIN_ENTRIES:
            return (yield from super().main_scene_call(state, frame, target, continuation))
        self.require_current(state)
        if self._started or continuation != 0x3CE:
            raise ValueError('one actual indexed Main484/488 invocation required')
        self._started = True
        return (yield from self.views['display', 'display_call_fields'](state, frame, target, continuation))
