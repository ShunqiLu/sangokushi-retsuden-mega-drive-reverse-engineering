"""The real Main4BC force heading and Main4C0 diplomacy panel continuations.

Keep the editable algorithms in their existing business modules. Only their
declared child calls become cooperative; no public function is rebound.
"""
import ast
import copy
import importlib
import inspect
from types import FunctionType

from .battle_trigger_steps import BattleScenePrograms, _dump, _code_shape, _top_code
from .contexts_services import SceneRefreshMemory
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
from ..high_level_scene_flows.source_artifact_cache import get_source_artifacts, read_source_text


MODULE_PATHS = {
    'main': 'tools.high_level_main_flows.business_main',
    'commands': 'tools.high_level_main_flows.business_commands',
}
MAIN_ENTRIES = {
    0x4BC: 'initialize_campaign_status_panel_fields',
    0x4C0: 'initialize_campaign_summary_panel_fields',
}
VIEW_SPECS = {
    'main': {
        'initialize_campaign_status_panel_fields': {'_campaign_call_fields': 1},
        'initialize_campaign_summary_panel_fields': {'_campaign_call_fields': 1},
    },
    'commands': {
        'draw_force_summary_frame_fields': {'_campaign_ui_call_fields': 3},
        'draw_diplomacy_command_panel_frame_fields': {'_campaign_ui_call_fields': 5},
    },
}
PANEL_CALLS = {
    (0xA456, 0x59A): 'draw_force_summary_frame_fields',
    (0xDB20, 0x5A2): 'draw_diplomacy_command_panel_frame_fields',
}
EXPECTED_SOURCE = {'main': {'initialize_campaign_status_panel_fields': 'def initialize_campaign_status_panel_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """4BC: initialize campaign status panel; original stage and child tokens."""\n    frame=_city_ui_frame_fields(state,frame,0x4BC)\n    frame=_campaign_call_fields(state,frame,0xA456,0x59A)\n    return frame', 'initialize_campaign_summary_panel_fields': 'def initialize_campaign_summary_panel_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """4C0: initialize campaign summary panel; original stage and child tokens."""\n    frame=_city_ui_frame_fields(state,frame,0x4C0)\n    frame=_campaign_call_fields(state,frame,0xDB20,0x5A2)\n    return frame'}, 'commands': {'draw_force_summary_frame_fields': 'def draw_force_summary_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """A456: selected force name and suffix, with the original privileged display refresh."""\n    frame=_city_ui_frame_fields(state,frame,0xA456)\n    frame=_command_panel_status_fields(state,frame,0x2700)\n    frame=_command_panel_pointer_fields(state,frame,\'roster\',state.read(0xFF382C,4))\n    frame=_movement_move(state,frame,\'target_x\',0,16)\n    frame=_movement_move(state,frame,\'target_x\',frame.roster.byte(4),8)\n    frame=_command_panel_pointer_fields(state,frame,\'candidates\',0xFFFFE640)\n    frame=_city_ui_shift_fields(state,frame,\'target_x\',1)\n    frame=_movement_move(state,frame,\'target_x\',frame.candidates.word(low16(frame.target_x)),16)\n    frame=_movement_move(state,frame,\'target_y\',low16(frame.target_x),16)\n    frame=_city_ui_shift_fields(state,frame,\'target_x\',1)\n    frame=_city_ui_arithmetic_fields(state,frame,\'target_x\',low16(frame.target_y))\n    frame=_city_ui_shift_fields(state,frame,\'target_x\',1)\n    frame=_command_panel_pointer_fields(state,frame,\'roster\',0x8A504+s16(low16(frame.target_x)))\n    frame=_command_panel_pointer_fields(state,frame,\'candidates\',0xFFFFD300)\n    frame=_movement_move(state,frame,\'target_x\',1,16)\n    frame=_movement_move(state,frame,\'target_y\',3,16)\n    frame=_movement_move(state,frame,\'count\',2,16)\n    frame=_campaign_ui_call_fields(state,frame,0xAE8A,0xA496)\n    frame=_command_panel_pointer_fields(state,frame,\'roster\',0xA4CA)\n    frame=_movement_move(state,frame,\'count\',0,16)\n    frame=_campaign_ui_call_fields(state,frame,0xAE8A,0xA4A6)\n    frame=_city_ui_store_fields(state,frame,0xC00004,0x41A00000,4)\n    frame=_command_panel_pointer_fields(state,frame,\'candidates\',0xFFFFD300)\n    frame=_movement_move(state,frame,\'count\',127,16)\n    frame=_command_panel_upload_fields(state,frame,\'candidates\',\'count\',0xC00000)\n    return _campaign_ui_call_fields(state,frame,0xAF48,0xA4C8)', 'draw_diplomacy_command_panel_frame_fields': 'def draw_diplomacy_command_panel_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """DB20: diplomacy labels and borders, then the true selection and interaction children."""\n    frame=_city_ui_frame_fields(state,frame,0xDB20)\n    frame=_command_panel_status_fields(state,frame,0x2700)\n    frame=_movement_move_long(state,frame,\'unit\',0x43180003)\n    frame=_movement_move(state,frame,\'target_x\',3,16)\n    while True:\n        frame=_city_ui_store_fields(state,frame,0xC00004,frame.unit,4)\n        frame=_movement_arithmetic_long(state,frame,\'unit\',0x800000)\n        frame=_movement_move(state,frame,\'target_y\',7,16)\n        frame=_command_panel_repeat_fields(state,frame,0xC00000,0,\'target_y\',4)\n        frame,again=_command_panel_dbra_fields(frame,\'target_x\')\n        if not again:break\n    frame=_city_ui_store_fields(state,frame,0xC00004,0x40A00000,4)\n    frame=_movement_move(state,frame,\'target_x\',7,16)\n    frame=_command_panel_repeat_fields(state,frame,0xC00000,0x11111113,\'target_x\',4)\n    frame=_command_panel_pointer_fields(state,frame,\'roster\',0x8A480)\n    frame=_command_panel_pointer_fields(state,frame,\'candidates\',0xFFFFD300)\n    frame=_movement_move(state,frame,\'target_x\',1,16)\n    frame=_movement_move(state,frame,\'target_y\',3,16)\n    frame=_movement_move(state,frame,\'count\',15,16)\n    frame=_campaign_ui_call_fields(state,frame,0xAE8A,0xDB88)\n    frame=_command_panel_pointer_fields(state,frame,\'candidates\',0xFFFFD300)\n    frame=_movement_move(state,frame,\'count\',511,16)\n    frame=_command_panel_upload_fields(state,frame,\'candidates\',\'count\',0xC00000)\n    frame=_command_panel_glyph_fields(state,frame,0x8A4A0,5,0xDBAE)\n    frame=_command_panel_pointer_fields(state,frame,\'candidates\',0xFFFFD300)\n    frame=_movement_move(state,frame,\'count\',191,16)\n    frame=_command_panel_upload_fields(state,frame,\'candidates\',\'count\',0xC00000)\n    frame=_command_panel_pointer_fields(state,frame,\'roster\',0x8A48E)\n    frame=_command_panel_pointer_fields(state,frame,\'candidates\',0xFFFFD300)\n    frame=_movement_move(state,frame,\'target_y\',2,16)\n    frame=_movement_move(state,frame,\'count\',14,16)\n    frame=_campaign_ui_call_fields(state,frame,0xAE8A,0xDBD8)\n    frame=_command_panel_pointer_fields(state,frame,\'candidates\',0xFFFFD300)\n    frame=_movement_move(state,frame,\'count\',479,16)\n    frame=_command_panel_upload_fields(state,frame,\'candidates\',\'count\',0xC00000)\n    frame=_command_panel_pointer_fields(state,frame,\'auxiliary\',0xC00004)\n    frame=_command_panel_pointer_fields(state,frame,\'scratch\',0xC00000)\n    frame=_city_ui_store_fields(state,frame,frame.auxiliary.base,0x42980003,4)\n    frame=_city_ui_store_fields(state,frame,frame.scratch.base,0xC380)\n    frame=_movement_move(state,frame,\'target_x\',7,16)\n    frame=_command_panel_repeat_fields(state,frame,frame.scratch.base,0xC381C381,\'target_x\',4)\n    frame=_city_ui_store_fields(state,frame,frame.scratch.base,0xCB80)\n    frame=_movement_move_long(state,frame,\'unit\',0x43180003)\n    for first_tile,last_tile in ((0xC006,0xC012),(0xC007,0xC013)):\n        frame=_city_ui_store_fields(state,frame,frame.auxiliary.base,frame.unit,4)\n        frame=_movement_arithmetic_long(state,frame,\'unit\',0x800000)\n        frame=_city_ui_store_fields(state,frame,frame.scratch.base,0xC382)\n        frame=_movement_move(state,frame,\'target_x\',5,16)\n        frame=_movement_move(state,frame,\'target_y\',first_tile,16)\n        while True:\n            frame=_city_ui_store_fields(state,frame,frame.scratch.base,low16(frame.target_y))\n            frame=_city_ui_arithmetic_fields(state,frame,\'target_y\',2)\n            frame,again=_command_panel_dbra_fields(frame,\'target_x\')\n            if not again:break\n        for tile in (0xC005,0xC001):frame=_city_ui_store_fields(state,frame,frame.scratch.base,tile)\n        frame=_movement_move(state,frame,\'target_x\',7,16)\n        frame=_movement_move(state,frame,\'target_y\',last_tile,16)\n        while True:\n            frame=_city_ui_store_fields(state,frame,frame.scratch.base,low16(frame.target_y))\n            frame=_city_ui_arithmetic_fields(state,frame,\'target_y\',2)\n            frame,again=_command_panel_dbra_fields(frame,\'target_x\')\n            if not again:break\n        frame=_city_ui_store_fields(state,frame,frame.scratch.base,0xCB82)\n    frame=_movement_move(state,frame,\'target_y\',8,16)\n    while True:\n        frame=_city_ui_store_fields(state,frame,frame.auxiliary.base,frame.unit,4)\n        frame=_movement_arithmetic_long(state,frame,\'unit\',0x800000)\n        frame=_city_ui_store_fields(state,frame,frame.scratch.base,0xC382)\n        frame=_movement_move(state,frame,\'target_x\',2,16)\n        frame=_command_panel_repeat_fields(state,frame,frame.scratch.base,0xC001C001,\'target_x\',4)\n        frame=_city_ui_store_fields(state,frame,frame.scratch.base,0xC005)\n        frame=_movement_move(state,frame,\'target_x\',3,16)\n        frame=_command_panel_repeat_fields(state,frame,frame.scratch.base,0xC001C001,\'target_x\',4)\n        frame=_city_ui_store_fields(state,frame,frame.scratch.base,0xC001CB82,4)\n        frame,again=_command_panel_dbra_fields(frame,\'target_y\')\n        if not again:break\n    frame=_city_ui_store_fields(state,frame,frame.auxiliary.base,frame.unit,4)\n    frame=_city_ui_store_fields(state,frame,frame.scratch.base,0xD380)\n    frame=_movement_move(state,frame,\'target_x\',7,16)\n    frame=_command_panel_repeat_fields(state,frame,frame.scratch.base,0xD381D381,\'target_x\',4)\n    frame=_city_ui_store_fields(state,frame,frame.scratch.base,0xDB80)\n    frame=_campaign_ui_call_fields(state,frame,0xDCF0,0xDCDE)\n    frame=_movement_move(state,frame,\'target_x\',198,16)\n    frame=_campaign_ui_call_fields(state,frame,0x676F2,0xDCE8)\n    return _campaign_ui_call_fields(state,frame,0x60C,0xDCEE)'}}
EXPECTED_REUSED_SOURCE = {'main': {}, 'commands': {'_campaign_ui_call_fields': 'def _campaign_ui_call_fields(state: SceneState, frame: FirstDeploymentFrame,\n        target: int, continuation: int) -> FirstDeploymentFrame:\n    """Use the one campaign call bridge; the caller owns its real LONG return slot."""\n    from .business_main import _campaign_call_fields\n    return _campaign_call_fields(state,frame,target,continuation)', '_command_panel_glyph_fields': 'def _command_panel_glyph_fields(state: SceneState, frame: FirstDeploymentFrame,\n        source: int, rows: int, continuation: int, stream: bool=False) -> FirstDeploymentFrame:\n    """One named glyph block uses the already restored decoder, not a copied font algorithm."""\n    frame=_command_panel_pointer_fields(state,frame,\'roster\',source)\n    frame=_command_panel_pointer_fields(state,frame,\'candidates\',0xFFFFD300)\n    frame=_movement_move(state,frame,\'count\',rows,16)\n    return _campaign_ui_call_fields(state,frame,0xAF1E if stream else 0xAE8A,continuation)', '_command_panel_upload_fields': 'def _command_panel_upload_fields(state: SceneState, frame: FirstDeploymentFrame,\n        source: str, counter: str, destination: int, width: int=4) -> FirstDeploymentFrame:\n    """Submit live packet cells in source-postincrement order to the real supplied port.\n\n    No device is acknowledged here. SceneState rejects an unobserved hardware\n    write at the actual transfer; the remaining logical source is still complete.\n    """\n    if source not in (\'roster\',\'candidates\') or width not in (2,4):\n        raise ValueError(\'closed command packet transfer role required\')\n    while True:\n        view=getattr(frame,source)\n        value=view.word() if width==2 else view.long()\n        frame=first_replace(frame,**{source:view.advance(width)})\n        frame=_city_ui_store_fields(state,frame,destination,value,width)\n        frame,again=_command_panel_dbra_fields(frame,counter)\n        if not again:return frame', '_command_panel_repeat_fields': 'def _command_panel_repeat_fields(state: SceneState, frame: FirstDeploymentFrame,\n        destination: int, value: int, counter: str, width: int=2) -> FirstDeploymentFrame:\n    """Repeated border or background cells retain the real counter and MOVE flags."""\n    if width not in (2,4):raise ValueError(\'actual border cell width required\')\n    while True:\n        frame=_city_ui_store_fields(state,frame,destination,value,width)\n        frame,again=_command_panel_dbra_fields(frame,counter)\n        if not again:return frame', '_command_panel_status_fields': 'def _command_panel_status_fields(state: SceneState, frame: FirstDeploymentFrame,\n        value: int) -> FirstDeploymentFrame:\n    """Use the existing Scene supervisor/trace boundary for a real full-SR write."""\n    state.set_status_word(value)\n    return first_replace(frame,status=value&31)', '_city_ui_store_fields': 'def _city_ui_store_fields(state: SceneState, frame: FirstDeploymentFrame,\n        address: int, value: int, size: int=2, clear: bool=False) -> FirstDeploymentFrame:\n    """Reuse the sole live RAM MOVE flags; actual CLR also performs its prior read."""\n    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory\n    from ..high_level_gameplay_flow.business_services import _scene_refresh_emit\n    if size not in (1,2,4) or type(clear) is not bool:\n        raise ValueError(\'actual city packet store width required\')\n    if clear:\n        state.read(address,size)\n        value=0\n    return _scene_refresh_emit(SceneRefreshMemory(state),frame,address,size,value)', 'append_diplomacy_command_choices_fields': 'def append_diplomacy_command_choices_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """DCF0: five original diplomacy selection roles and optional live cursor rows."""\n    frame=_city_ui_frame_fields(state,frame,0xDCF0)\n    frame=first_replace(frame,roster=state.table_at(u32(0xFFFFD100+s16(state.read(0xFFFFF31A,2)))).cursor())\n    roles=((0xC51A,0xC022,0xFFFFAFF8,0,False,0xDD10),\n        (0xC69A,0xC02E,0xFFFFAFF8,0,True,0xDD28),\n        (0xC4AE,0xC03A,0xFFFFAFFA,0,False,0xDD40),\n        (0xC62E,0xC046,0xFFFFAFFA,1,False,0xDD5A),\n        (0xC7AE,0xC052,0xFFFFAFFA,2,False,0xDD74))\n    for location,glyph,address,match,nonzero,continuation in roles:\n        frame=_movement_move(state,frame,\'target_x\',location,16)\n        frame=_movement_move(state,frame,\'target_y\',glyph,16)\n        if match:\n            frame=_movement_compare(state,frame,state.read(address,2),match,16)\n        else:\n            frame=_movement_test(state,frame,state.read(address,2),16)\n        selected=not bool(frame.status&4) if nonzero else bool(frame.status&4)\n        if selected:\n            frame=_city_ui_arithmetic_fields(state,frame,\'target_y\',60)\n        frame=_city_ui_child_fields(state,frame,0xDDEC,continuation)\n    frame=_movement_move(state,frame,\'target_x\',state.read(0xFFFFF602,1),8)\n    frame=_movement_move(state,frame,\'target_x\',low16(frame.target_x)&3,16)\n    append_cursor=not bool(frame.status&4)\n    if not append_cursor:\n        frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF321,1),3)\n        append_cursor=not bool(frame.status&4)\n    if append_cursor:\n        frame=_movement_move(state,frame,\'target_x\',0xC51A,16)\n        frame=_movement_move(state,frame,\'target_y\',state.read(0xFFFFAFF8,2),16)\n        frame=_movement_test(state,frame,state.read(0xFFFFAFFC,2),16)\n        if not frame.status&4:\n            frame=_movement_move(state,frame,\'target_x\',0xC4AE,16)\n            frame=_movement_move(state,frame,\'target_y\',state.read(0xFFFFAFFA,2),16)\n        frame=_movement_move(state,frame,\'unit\',low16(frame.target_y),16)\n        frame=_city_ui_shift_fields(state,frame,\'target_y\',1)\n        frame=_city_ui_arithmetic_fields(state,frame,\'target_y\',low16(frame.unit))\n        frame=_city_ui_shift_fields(state,frame,\'target_y\',7)\n        frame=_city_ui_arithmetic_fields(state,frame,\'target_x\',low16(frame.target_y))\n        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+16),6)\n        frame=_city_ui_append_fields(state,frame,6)\n        frame=_city_ui_store_fields(state,frame,frame.roster.base,low16(frame.target_x))\n        frame=_city_ui_arithmetic_fields(state,frame,\'target_x\',128)\n        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+16),low16(frame.target_x))\n        frame=first_replace(frame,roster=frame.roster.advance(2))\n        frame=_movement_move(state,frame,\'target_x\',2,16)\n        while True:\n            frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+16),0xC001C001,4)\n            frame=_city_ui_append_fields(state,frame,0xC001C001,4)\n            frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))\n            if low16(frame.target_x)==65535:\n                break\n        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,32)\n        frame=first_replace(frame,roster=frame.roster.advance(16))\n    frame=_city_ui_store_fields(state,frame,frame.roster.base,0,2,True)\n    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,80)', 'set_diplomacy_command_marker_fields': 'def set_diplomacy_command_marker_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """DDEC: six paired choice label cells and their actual D0/D1/D2 effects."""\n    frame=_city_ui_frame_fields(state,frame,0xDDEC)\n    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+16),6)\n    frame=_city_ui_append_fields(state,frame,6)\n    frame=_city_ui_store_fields(state,frame,frame.roster.base,low16(frame.target_x))\n    frame=_city_ui_arithmetic_fields(state,frame,\'target_x\',128)\n    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+16),low16(frame.target_x))\n    frame=first_replace(frame,roster=frame.roster.advance(2))\n    frame=_movement_move(state,frame,\'unit\',5,16)\n    while True:\n        frame=_city_ui_store_fields(state,frame,frame.roster.base,low16(frame.target_y))\n        frame=_city_ui_arithmetic_fields(state,frame,\'target_y\',1)\n        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+16),low16(frame.target_y))\n        frame=_city_ui_arithmetic_fields(state,frame,\'target_y\',1)\n        frame=first_replace(frame,roster=frame.roster.advance(2))\n        frame=first_replace(frame,unit=replace_word(frame.unit,u16(low16(frame.unit)-1)))\n        if low16(frame.unit)==65535:\n            break\n    return first_replace(frame,roster=frame.roster.advance(16))'}}


def _panel_source_tree(group, original_tree):
    """Only ten declared CALL propagations; reverse the complete source module."""
    if group not in VIEW_SPECS:
        raise ValueError('only the two reviewed panel source groups are admitted')
    derived = copy.deepcopy(original_tree)
    inverses = {}
    for index, original in enumerate(original_tree.body):
        if not isinstance(original, ast.FunctionDef) or original.name not in VIEW_SPECS[group]:
            continue
        if _dump(original) != _dump(ast.parse(EXPECTED_SOURCE[group][original.name]).body[0]):
            raise ValueError('complete panel source owner changed: ' + original.name)
        if any(isinstance(node, (ast.Yield, ast.YieldFrom)) for node in ast.walk(original)):
            raise ValueError('the original panel body must remain synchronous')
        counts = {name: 0 for name in VIEW_SPECS[group][original.name]}
        substitutions = []

        class Lift(ast.NodeTransformer):
            def visit_Call(self, node):
                node = self.generic_visit(node)
                if not isinstance(node.func, ast.Name) or node.func.id not in counts:
                    return node
                before = copy.deepcopy(node)
                counts[node.func.id] += 1
                node.func.id = '_panel_campaign_call'
                after = ast.copy_location(ast.YieldFrom(value=node), node)
                substitutions.append((before, copy.deepcopy(after)))
                return after

        current = Lift().visit(copy.deepcopy(original))
        if counts != VIEW_SPECS[group][original.name]:
            raise ValueError('the exact original panel CALL count differs: ' + original.name)
        pending = list(substitutions)

        class Inverse(ast.NodeTransformer):
            def visit_YieldFrom(self, node):
                for position, (before, after) in enumerate(pending):
                    if _dump(node) == _dump(after):
                        pending.pop(position)
                        return copy.deepcopy(before)
                raise ValueError('undeclared panel suspension')

        restored = Inverse().visit(copy.deepcopy(current))
        if pending or _dump(restored) != _dump(original):
            raise ValueError('whole original panel function inverse differs: ' + original.name)
        derived.body[index] = current
        inverses[index] = restored
    if len(inverses) != len(VIEW_SPECS[group]):
        raise ValueError('all complete panel functions must be present')
    restored_module = copy.deepcopy(derived)
    for index, original in inverses.items():
        restored_module.body[index] = original
    if _dump(restored_module) != _dump(original_tree):
        raise ValueError('whole original panel module inverse differs')
    return ast.fix_missing_locations(derived)


def _prepare_panel_artifacts(module, group, source, filename):
    tree = ast.parse(source, filename=filename)
    plain = compile(tree, filename, 'exec', dont_inherit=True)
    expected = dict(EXPECTED_REUSED_SOURCE.get(group, {}))
    expected.update(EXPECTED_SOURCE[group])
    for name, expected_source in expected.items():
        nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
        owner = getattr(module, name)
        if (len(nodes) != 1 or _dump(nodes[0]) != _dump(ast.parse(expected_source).body[0])
                or type(owner) is not FunctionType or owner.__globals__ is not vars(module)
                or owner.__module__ != module.__name__ or owner.__name__ != name
                or owner.__closure__ is not None or owner.__code__.co_freevars
                or _code_shape(owner.__code__) != _code_shape(_top_code(plain, name))):
            raise ValueError('actual complete unwrapped panel function required: ' + name)
    derived = compile(_panel_source_tree(group, tree), filename, 'exec', dont_inherit=True)
    return dict(plain=plain, derived=derived)


class DiplomacyPanelScenePrograms(BattleScenePrograms):
    """One original indexed invocation, including the real privileged refresh."""

    def __init__(self, state):
        super().__init__(state)
        self.panel_modules = {group: importlib.import_module(path)
            for group, path in MODULE_PATHS.items()}
        self.panel_originals, self.panel_codes = {}, {}
        self.panel_views, self.panel_namespaces, self.panel_bindings = {}, {}, {}
        for group, module in self.panel_modules.items():
            filename, source = read_source_text(module)
            artifacts = get_source_artifacts('diplomacy-panel', module.__name__, group,
                source_text=source, filename=filename,
                transformer_codes=(_prepare_panel_artifacts.__code__, _panel_source_tree.__code__,
                    _dump.__code__, _code_shape.__code__, _top_code.__code__),
                expected_contract=dict(expected=EXPECTED_SOURCE[group],
                    reused=EXPECTED_REUSED_SOURCE.get(group, {}), views=VIEW_SPECS[group]),
                prepare=lambda: _prepare_panel_artifacts(module, group, source, filename))
            plain, code = artifacts['plain'], artifacts['derived']
            expected = dict(EXPECTED_REUSED_SOURCE.get(group, {}))
            expected.update(EXPECTED_SOURCE[group])
            for name in expected:
                owner = getattr(module, name)
                if (type(owner) is not FunctionType or owner.__globals__ is not vars(module)
                        or owner.__module__ != module.__name__ or owner.__name__ != name
                        or owner.__closure__ is not None or owner.__code__.co_freevars
                        or _code_shape(owner.__code__) != _code_shape(_top_code(plain, name))):
                    raise ValueError('actual complete unwrapped panel function required: ' + name)
                self.panel_originals[group, name], self.panel_codes[group, name] = owner, owner.__code__
            namespace = self.panel_namespaces[group] = dict(vars(module))
            if '_panel_campaign_call' in namespace:
                raise ValueError('the panel alias cannot shadow an original binding')
            namespace['_panel_campaign_call'] = self.views['main', '_campaign_call_fields']
            self.panel_bindings[group, '_panel_campaign_call'] = namespace['_panel_campaign_call']
            for name in VIEW_SPECS[group]:
                owner = self.panel_originals[group, name]
                view = FunctionType(_top_code(code, name), namespace, name, owner.__defaults__, None)
                view.__kwdefaults__, view.__annotations__ = owner.__kwdefaults__, dict(owner.__annotations__)
                if not inspect.isgeneratorfunction(view) or view.__closure__ is not None:
                    raise ValueError('a complete closure-free panel generator is required')
                self.panel_views[group, name] = view
        self.panel_view_owners = dict(self.panel_views)
        self.panel_view_codes = {key: view.__code__ for key, view in self.panel_views.items()}

    def require_current(self, state):
        super().require_current(state)
        if not hasattr(self, 'panel_originals'):
            return
        for key, owner in self.panel_originals.items():
            if (getattr(self.panel_modules[key[0]], key[1]) is not owner
                    or owner.__code__ is not self.panel_codes[key]):
                raise ValueError('the actual panel source owner changed: ' + key[1])
        if self.panel_views.keys() != self.panel_view_owners.keys():
            raise ValueError('the complete panel view set changed')
        for key, view in self.panel_view_owners.items():
            if self.panel_views[key] is not view or view.__code__ is not self.panel_view_codes[key]:
                raise ValueError('the actual panel view changed: ' + key[1])
        for (group, name), value in self.panel_bindings.items():
            if self.panel_namespaces[group].get(name) is not value:
                raise ValueError('the private panel call binding changed')

    def _campaign_child(self, state, frame, target, continuation):
        self.require_current(state)
        name = PANEL_CALLS.get((target, continuation))
        if name is not None:
            return (yield from self.panel_views['commands', name](state, frame))
        if target in (0xA456, 0xDB20):
            raise MovementContinuationBoundary(target, frame, 'panel child requires its original Main LONG')
        if (target, continuation) == (0xAF48, 0xA4C8):
            return (yield from self._refresh(SceneRefreshMemory(state), frame))
        if (target, continuation) == (0x60C, 0xDCEE):
            # The inherited campaign bridge already pushed DCEE. The actual
            # clear view owns its children, not another outer CALL/RTS pair.
            program = self.battle_views['services', 'clear_scene_video_and_state_fields'](
                SceneRefreshMemory(state), frame)
            return (yield from self._message_waits(program))
        return (yield from super()._campaign_child(state, frame, target, continuation))

    def _display_child(self, state, frame, target, continuation):
        self.require_current(state)
        if target in MAIN_ENTRIES:
            if continuation != 0x3CE:
                raise MovementContinuationBoundary(target, frame, 'panel Main requires original3CE LONG')
            return (yield from self.panel_views['main', MAIN_ENTRIES[target]](state, frame))
        return (yield from super()._display_child(state, frame, target, continuation))

    def main_scene_call(self, state, frame, target, continuation):
        if target not in MAIN_ENTRIES:
            return (yield from super().main_scene_call(state, frame, target, continuation))
        self.require_current(state)
        if self._started or continuation != 0x3CE:
            raise ValueError('one actual indexed force-heading/diplomacy Main invocation required')
        self._started = True
        return (yield from self.views['display', 'display_call_fields'](state, frame, target, continuation))
