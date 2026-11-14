"""Whole Main404/40C information-plane parents with actual refresh continuations.

BAEA uses the current menu descriptor and title glyph directory; C372 uploads
its fixed six-character glyph run. Historical scalar names do not decide their
roles. Existing complete Frame algorithms and synchronous children are reused.
"""
import ast
import copy
import importlib
import inspect
from types import FunctionType

from .battle_trigger_steps import BattleScenePrograms, _dump, _code_shape, _top_code
from .contexts_services import SceneRefreshMemory
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary


MODULE_PATHS = {
    'main': 'tools.high_level_main_flows.business_main',
    'commands': 'tools.high_level_main_flows.business_commands',
    'lowbank': 'tools.high_level_main_flows.business_lowbank',
    'glyph': 'tools.high_level_scene_flows.business_scene',
}
MAIN_ENTRIES = {
    0x404: 'initialize_campaign_options_fields',
    0x40C: 'initialize_campaign_command_panel_fields',
}
VIEW_SPECS = {
    'main': {
        'initialize_campaign_options_fields': {'_campaign_call_fields': 1},
        'initialize_campaign_command_panel_fields': {'_campaign_call_fields': 1},
    },
    'commands': {
        'draw_officer_detail_view_frame_fields': {'_campaign_ui_call_fields': 2},
        'draw_force_relation_view_frame_fields': {'_campaign_ui_call_fields': 2},
    },
    'lowbank': {},
    'glyph': {},
}
PANEL_CALLS = {
    (0xBAEA, 0x55C): 'draw_officer_detail_view_frame_fields',
    (0xC372, 0x564): 'draw_force_relation_view_frame_fields',
}
REFRESH_CALLS = ((0xAF48, 0xBB24), (0xAF48, 0xC3CC))
EXPECTED_SOURCE = {'main': {'initialize_campaign_options_fields': 'def initialize_campaign_options_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """404: initialize campaign options; original stage and child tokens."""\n    frame=_city_ui_frame_fields(state,frame,0x404)\n    frame=_campaign_call_fields(state,frame,0xBAEA,0x55C)\n    return frame', 'initialize_campaign_command_panel_fields': 'def initialize_campaign_command_panel_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """40C: initialize campaign command panel; original stage and child tokens."""\n    frame=_city_ui_frame_fields(state,frame,0x40C)\n    frame=_campaign_call_fields(state,frame,0xC372,0x564)\n    return frame'}, 'commands': {'draw_officer_detail_view_frame_fields': 'def draw_officer_detail_view_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """BAEA: detail screen initialization and real child/header/layout progression."""\n    frame=_city_ui_frame_fields(state,frame,0xBAEA)\n    frame=_command_panel_status_fields(state,frame,0x2700)\n    frame=_command_panel_pointer_fields(state,frame,\'auxiliary\',0xC00000)\n    frame=_movement_move(state,frame,\'target_x\',1,16)\n    frame=_movement_move(state,frame,\'target_y\',3,16)\n    for target,token in ((0xBB26,0xBB00),(0x5204,0xBB04),(0x52C2,0xBB08),(0x55B0,0xBB0C)):\n        frame=_campaign_ui_call_fields(state,frame,target,token)\n    frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x208)\n    for address in (0xFFFFF362,0xFFFFF36A,0xFFFFF394):frame=_city_ui_store_fields(state,frame,address,0,2,True)\n    return _campaign_ui_call_fields(state,frame,0xAF48,0xBB24)', 'draw_force_relation_view_frame_fields': 'def draw_force_relation_view_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """C372: initialize the relation glyph plane and then require real scene refresh."""\n    frame=_city_ui_frame_fields(state,frame,0xC372)\n    frame=_command_panel_status_fields(state,frame,0x2700)\n    frame=_command_panel_pointer_fields(state,frame,\'auxiliary\',0xC00000)\n    frame=_movement_move(state,frame,\'target_x\',1,16)\n    frame=_movement_move(state,frame,\'target_y\',3,16)\n    frame=_movement_move(state,frame,\'unit\',31,16)\n    frame=_command_panel_pointer_fields(state,frame,\'roster\',0xFFFFD300)\n    frame=_command_panel_fill_buffer_fields(state,frame,\'roster\',\'unit\')\n    frame=_command_panel_pointer_fields(state,frame,\'roster\',0x8A374)\n    frame=_movement_move(state,frame,\'count\',5,16)\n    frame=_command_panel_pointer_fields(state,frame,\'candidates\',0xFFFFD380)\n    frame=_campaign_ui_call_fields(state,frame,0xAE8A,0xC3AA)\n    frame=_city_ui_store_fields(state,frame,0xC00004,0x40200000,4)\n    frame=_city_ui_store_fields(state,frame,0xFFFFF37E,0,2,True)\n    frame=_command_panel_pointer_fields(state,frame,\'roster\',0xFFFFD300)\n    frame=_movement_move(state,frame,\'choice\',223,16)\n    frame=_command_panel_upload_fields(state,frame,\'roster\',\'choice\',frame.auxiliary.base)\n    return _campaign_ui_call_fields(state,frame,0xAF48,0xC3CC)'}, 'lowbank': {}, 'glyph': {}}
EXPECTED_REUSED_SOURCE = {'main': {}, 'commands': {'_campaign_ui_call_fields': 'def _campaign_ui_call_fields(state: SceneState, frame: FirstDeploymentFrame,\n        target: int, continuation: int) -> FirstDeploymentFrame:\n    """Use the one campaign call bridge; the caller owns its real LONG return slot."""\n    from .business_main import _campaign_call_fields\n    return _campaign_call_fields(state,frame,target,continuation)', '_city_ui_frame_fields': 'def _city_ui_frame_fields(state: SceneState, frame: FirstDeploymentFrame,\n        entry: int) -> FirstDeploymentFrame:\n    """Historical partial UI observations never invent complete register/CCR/SP inputs."""\n    checked_state(state)\n    if type(frame) is not FirstDeploymentFrame:\n        raise ValueError(\'actual full city UI fields required\')\n    values=(frame.target_x,frame.target_y,frame.unit,frame.count,frame.distance,\n        frame.offset_x,frame.offset_y,frame.choice,frame.roster,frame.candidates,\n        frame.controller,frame.scan,frame.opponent,frame.scratch,frame.auxiliary,\n        frame.stack_cursor,frame.status)\n    if any(value is None for value in values):\n        raise MovementContinuationBoundary(entry,frame,\'old city UI input did not observe the complete entry ABI\')\n    return _movement_frame(state,frame)', '_city_ui_store_fields': 'def _city_ui_store_fields(state: SceneState, frame: FirstDeploymentFrame,\n        address: int, value: int, size: int=2, clear: bool=False) -> FirstDeploymentFrame:\n    """Reuse the sole live RAM MOVE flags; actual CLR also performs its prior read."""\n    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory\n    from ..high_level_gameplay_flow.business_services import _scene_refresh_emit\n    if size not in (1,2,4) or type(clear) is not bool:\n        raise ValueError(\'actual city packet store width required\')\n    if clear:\n        state.read(address,size)\n        value=0\n    return _scene_refresh_emit(SceneRefreshMemory(state),frame,address,size,value)', '_city_ui_arithmetic_fields': 'def _city_ui_arithmetic_fields(state: SceneState, frame: FirstDeploymentFrame,\n        name: str, source: int, subtract: bool=False, width: int=16) -> FirstDeploymentFrame:\n    """Reuse existing arithmetic flags and retain the actual narrow-write high bits."""\n    destination=low8(frame.carrier(name)) if width==8 else low16(frame.carrier(name))\n    source=low8(source) if width==8 else low16(source)\n    frame,result=_movement_binary_flags(state,frame,destination,source,width,subtract)\n    value=replace_byte(frame.carrier(name),result) if width==8 else replace_word(frame.carrier(name),result)\n    return first_replace(frame,**{name:value})', '_city_ui_shift_fields': 'def _city_ui_shift_fields(state: SceneState, frame: FirstDeploymentFrame,\n        name: str, count: int) -> FirstDeploymentFrame:\n    """Existing original logical WORD shifts, including the already closed #7."""\n    if count==7:\n        from ..high_level_remaining_flows.business_city import _duel_commit_shift_fields\n        return _duel_commit_shift_fields(state,frame,name,count)\n    return _movement_fixed_shift_word(state,frame,name,count)', '_command_panel_status_fields': 'def _command_panel_status_fields(state: SceneState, frame: FirstDeploymentFrame,\n        value: int) -> FirstDeploymentFrame:\n    """Use the existing Scene supervisor/trace boundary for a real full-SR write."""\n    state.set_status_word(value)\n    return first_replace(frame,status=value&31)', '_command_panel_pointer_fields': 'def _command_panel_pointer_fields(state: SceneState, frame: FirstDeploymentFrame,\n        name: str, address: int) -> FirstDeploymentFrame:\n    """MOVEA/LEA retains CCR; cursor carriers keep their real live address type."""\n    address=u32(address)\n    if name in (\'roster\',\'candidates\',\'scan\'):\n        return first_replace(frame,**{name:state.table_at(address).cursor()})\n    if name in (\'controller\',\'opponent\',\'scratch\',\'auxiliary\'):\n        return first_replace(frame,**{name:state.table_at(address)})\n    raise ValueError(\'closed command panel address carrier required\')', '_command_panel_fill_buffer_fields': 'def _command_panel_fill_buffer_fields(state: SceneState, frame: FirstDeploymentFrame,\n        address: str, counter: str, value: int=0x11111111, clear: bool=False) -> FirstDeploymentFrame:\n    """Initialize the live packet buffer; CLR includes its original prior read."""\n    if address not in (\'roster\',\'candidates\',\'controller\'):raise ValueError(\'closed command buffer role required\')\n    while True:\n        view=getattr(frame,address)\n        frame=_city_ui_store_fields(state,frame,view.base,value,4,clear)\n        frame=first_replace(frame,**{address:view.advance(4)})\n        frame,again=_command_panel_dbra_fields(frame,counter)\n        if not again:return frame', '_command_panel_dbra_fields': 'def _command_panel_dbra_fields(frame: FirstDeploymentFrame, name: str) -> tuple[FirstDeploymentFrame, bool]:\n    """An original counted row consumes the current WORD and preserves all CCR bits."""\n    if name not in (\'target_x\',\'target_y\',\'unit\',\'count\',\'distance\',\'offset_x\',\'offset_y\',\'choice\'):\n        raise ValueError(\'actual command panel DBRA register required\')\n    remaining=u16(low16(frame.carrier(name))-1)\n    return first_replace(frame,**{name:replace_word(frame.carrier(name),remaining)}),remaining!=65535', '_command_panel_upload_fields': 'def _command_panel_upload_fields(state: SceneState, frame: FirstDeploymentFrame,\n        source: str, counter: str, destination: int, width: int=4) -> FirstDeploymentFrame:\n    """Submit live packet cells in source-postincrement order to the real supplied port.\n\n    No device is acknowledged here. SceneState rejects an unobserved hardware\n    write at the actual transfer; the remaining logical source is still complete.\n    """\n    if source not in (\'roster\',\'candidates\') or width not in (2,4):\n        raise ValueError(\'closed command packet transfer role required\')\n    while True:\n        view=getattr(frame,source)\n        value=view.word() if width==2 else view.long()\n        frame=first_replace(frame,**{source:view.advance(width)})\n        frame=_city_ui_store_fields(state,frame,destination,value,width)\n        frame,again=_command_panel_dbra_fields(frame,counter)\n        if not again:return frame', '_command_panel_row_stride_fields': 'def _command_panel_row_stride_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """BB96\'s existing bounded five-bit WORD shift, without a second numeric core."""\n    from ..high_level_battle_ai.business_formation import _first_shift_word\n    frame=_first_shift_word(frame,\'choice\',low16(frame.choice),5)\n    state.sr=(state.sr&65504)|frame.status\n    return frame', 'append_officer_detail_rows_frame_fields': 'def append_officer_detail_rows_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """BB26: live menu descriptors select the real glyph run and exact row upload count."""\n    frame=_city_ui_frame_fields(state,frame,0xBB26)\n    frame=_movement_move(state,frame,\'unit\',31,16)\n    frame=_command_panel_pointer_fields(state,frame,\'roster\',0xFFFFD300)\n    frame=_command_panel_fill_buffer_fields(state,frame,\'roster\',\'unit\')\n    frame=_movement_move(state,frame,\'choice\',state.read(0xFFFFF38C,2),16)\n    frame=_command_panel_pointer_fields(state,frame,\'candidates\',0x92878)\n    frame=_command_panel_pointer_fields(state,frame,\'controller\',frame.candidates.long())\n    frame=_city_ui_shift_fields(state,frame,\'choice\',1)\n    frame=_movement_move(state,frame,\'choice\',frame.candidates.word(low16(frame.choice+4)),16)\n    frame=first_replace(frame,controller=frame.controller.advance(s16(low16(frame.choice))))\n    frame=_movement_move(state,frame,\'choice\',0,16)\n    frame=_movement_move(state,frame,\'choice\',frame.controller.byte(1),8)\n    frame=_city_ui_store_fields(state,frame,0xFFFFF380,low16(frame.choice))\n    frame=_movement_compare(state,frame,low16(frame.choice),96,16)\n    if not frame.status&1:return frame\n    frame=_movement_move(state,frame,\'offset_y\',low16(frame.choice),16)\n    frame=_city_ui_shift_fields(state,frame,\'choice\',1)\n    frame=_city_ui_arithmetic_fields(state,frame,\'choice\',low16(frame.offset_y))\n    frame=_city_ui_shift_fields(state,frame,\'choice\',1)\n    frame=_command_panel_pointer_fields(state,frame,\'candidates\',0xBBA0)\n    frame=_command_panel_pointer_fields(state,frame,\'roster\',frame.candidates.long(low16(frame.choice)))\n    frame=_movement_move(state,frame,\'count\',frame.candidates.word(low16(frame.choice+4)),16)\n    frame=_movement_move(state,frame,\'choice\',low16(frame.count),16)\n    frame=_command_panel_pointer_fields(state,frame,\'candidates\',0xFFFFD380)\n    frame=_campaign_ui_call_fields(state,frame,0xAE8A,0xBB7E)\n    frame=_city_ui_store_fields(state,frame,0xC00004,0x40200000,4)\n    frame=_city_ui_store_fields(state,frame,0xFFFFF37E,0,2,True)\n    frame=_command_panel_pointer_fields(state,frame,\'roster\',0xFFFFD300)\n    frame=_city_ui_arithmetic_fields(state,frame,\'choice\',1)\n    frame=_command_panel_row_stride_fields(state,frame)\n    frame=_city_ui_arithmetic_fields(state,frame,\'choice\',31)\n    return _command_panel_upload_fields(state,frame,\'roster\',\'choice\',frame.auxiliary.base)'}, 'lowbank': {'_campaign_ui_frame_fields': 'def _campaign_ui_frame_fields(state: SceneState, frame: FirstDeploymentFrame,\n        entry: int) -> FirstDeploymentFrame:\n    from .business_commands import _city_ui_frame_fields\n    return _city_ui_frame_fields(state,frame,entry)', '_campaign_ui_call_fields': 'def _campaign_ui_call_fields(state: SceneState, frame: FirstDeploymentFrame,\n        target: int, token: int) -> FirstDeploymentFrame:\n    from .business_main import _campaign_call_fields\n    return _campaign_call_fields(state,frame,target,token)', '_campaign_ui_move_fields': 'def _campaign_ui_move_fields(state: SceneState, frame: FirstDeploymentFrame,\n        carrier: str, value: int, width: int=16) -> FirstDeploymentFrame:\n    from .business_movement_support import _movement_move, _movement_move_long\n    if width==32:\n        return _movement_move_long(state,frame,carrier,value)\n    return _movement_move(state,frame,carrier,value,width)', '_campaign_ui_write_fields': 'def _campaign_ui_write_fields(state: SceneState, frame: FirstDeploymentFrame,\n        pc: int, address: int, value: int, width: int=2, clear: bool=False) -> FirstDeploymentFrame:\n    from .business_main import _campaign_emit_fields\n    return _campaign_emit_fields(state,frame,pc,address,value,width,clear)', '_campaign_ui_loop_fields': 'def _campaign_ui_loop_fields(frame: FirstDeploymentFrame,\n        carrier: str) -> tuple[FirstDeploymentFrame, bool]:\n    """The DBRA WORD decrement never changes the actual CCR or register high WORD."""\n    remaining=u16(low16(frame.carrier(carrier))-1)\n    return first_replace(frame,**{carrier:replace_word(frame.carrier(carrier),remaining)}),remaining!=65535', '_campaign_ui_copy_panel_longs_fields': 'def _campaign_ui_copy_panel_longs_fields(state: SceneState, frame: FirstDeploymentFrame, source_carrier: str, count_carrier: str, instruction: int, destination: int) -> FirstDeploymentFrame:\n    """One structured DBRA panel row, retaining real cursors and ordered LONG DATA."""\n    if source_carrier not in (\'roster\', \'candidates\'):\n        raise ValueError(\'only original roster/candidates panel source views are admitted\')\n    while True:\n        source = state.checked_table(getattr(frame, source_carrier))\n        value = source.long()\n        frame = first_replace(frame, **{source_carrier: source.advance(4)})\n        frame = _campaign_ui_write_fields(state, frame, instruction, destination, value, 4)\n        frame, more = _campaign_ui_loop_fields(frame, count_carrier)\n        if not more:\n            return frame', 'draw_scene_header_glyphs_fields': 'def draw_scene_header_glyphs_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """5204..5242: decode the two genuine header runs, then transfer their full tile buffer."""\n    frame = _campaign_ui_frame_fields(state, frame, 20996)\n    frame = first_replace(frame, roster=state.table_at(565756).cursor(), candidates=state.table_at(4294955776).cursor())\n    frame = _campaign_ui_move_fields(state, frame, \'count\', 1)\n    frame = _campaign_ui_call_fields(state, frame, 44682, 21016)\n    frame = first_replace(frame, roster=state.table_at(565760).cursor())\n    frame = _campaign_ui_move_fields(state, frame, \'count\', 9)\n    frame = _campaign_ui_call_fields(state, frame, 44682, 21032)\n    frame = _campaign_ui_write_fields(state, frame, 21032, 12582916, 1509949440, 4)\n    frame = first_replace(frame, candidates=state.table_at(4294955776).cursor())\n    frame = _campaign_ui_move_fields(state, frame, \'distance\', 383)\n    return _campaign_ui_copy_panel_longs_fields(state, frame, \'candidates\', \'distance\', 21050, frame.auxiliary.base)', 'upload_selection_layout_fields': 'def upload_selection_layout_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """52C2..5330: original static rows, uniform third row and final readonly packet."""\n    frame=_campaign_ui_frame_fields(state,frame,0x52C2)\n    frame=_campaign_ui_write_fields(state,frame,0x52C2,0xC00004,0x70000001,4)\n    frame=first_replace(frame,roster=state.table_at(0x89DDC).cursor())\n    frame=_campaign_ui_move_fields(state,frame,\'distance\',23)\n    frame=_campaign_ui_copy_panel_longs_fields(state,frame,\'roster\',\'distance\',0x52D6,0xC00000)\n    frame=_campaign_ui_write_fields(state,frame,0x52E0,0xC00004,0x70A00001,4)\n    frame=first_replace(frame,roster=state.table_at(0x89F5C).cursor())\n    frame=_campaign_ui_move_fields(state,frame,\'distance\',7)\n    frame=_campaign_ui_copy_panel_longs_fields(state,frame,\'roster\',\'distance\',0x52F4,0xC00000)\n    frame=_campaign_ui_write_fields(state,frame,0x52FE,0xC00004,0x72000001,4)\n    frame=_campaign_ui_move_fields(state,frame,\'distance\',7)\n    while True:\n        frame=_campaign_ui_write_fields(state,frame,0x530C,0xC00000,0x33333333,4)\n        frame,more=_campaign_ui_loop_fields(frame,\'distance\')\n        if not more:\n            break\n    frame=first_replace(frame,roster=state.table_at(0x8A0BC).cursor())\n    frame=_campaign_ui_move_fields(state,frame,\'distance\',7)\n    return _campaign_ui_copy_panel_longs_fields(state,frame,\'roster\',\'distance\',0x5324,0xC00000)', 'draw_current_resource_glyphs_fields': 'def draw_current_resource_glyphs_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """55B0..55D0: the actual 24-LONG resource caption upload."""\n    frame=_campaign_ui_frame_fields(state,frame,0x55B0)\n    frame=first_replace(frame,roster=state.table_at(0x89EFC).cursor())\n    frame=_campaign_ui_write_fields(state,frame,0x55B6,0xC00004,0x67A00001,4)\n    frame=_campaign_ui_move_fields(state,frame,\'target_x\',23)\n    return _campaign_ui_copy_panel_longs_fields(state,frame,\'roster\',\'target_x\',0x55C4,0xC00000)'}, 'glyph': {'decode_glyph_rows_to_buffers_fields': 'def decode_glyph_rows_to_buffers_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """AE8A unique font/fill tile algorithm with real five LONG saves."""\n    memory.frame(frame)\n    if any(value is None for value in (frame.roster,frame.candidates,frame.target_x,frame.target_y,frame.count)):\n        raise SceneRefreshBoundary(0xAE8A,frame,None)\n    original = frame\n    frame = _glyph_save_fields(memory,frame,True)\n    remaining = low16(frame.count)\n    row_longs = 16\n    while True:\n        token = frame.roster.word()\n        frame = first_replace(frame,roster=frame.roster.advance(2))\n        frame = _first_word(frame,\'distance\',token)\n        if not negative_word(token):\n            frame = _first_word(frame,\'offset_x\',token)\n            high = token & 0xFF00\n            frame = _first_word(frame,\'offset_x\',high)\n            frame = _first_shift_word(frame,\'offset_x\',high,3)\n            low = token & 255\n            frame = _first_word(frame,\'distance\',low)\n            frame = _first_shift_word(frame,\'distance\',low,5)\n            offset = u16(low << 5) | u16(high << 3)\n            frame = _first_word(frame,\'distance\',offset)\n            frame = _first_long(frame,\'distance\',offset)\n            frame = first_replace(frame,controller=memory.cursor_at(0x8159C + offset))\n            frame = _first_word(frame,\'offset_x\',row_longs - 1)\n            for index in range(row_longs):\n                frame = _glyph_row_call_fields(memory,frame,0xAEBA)\n                frame = _scene_refresh_emit(memory,frame,frame.candidates.base,4,frame.choice)\n                frame = _glyph_row_call_fields(memory,frame,0xAEC0)\n                frame = _scene_refresh_emit(memory,frame,frame.candidates.base + 0x40,4,frame.choice)\n                frame = first_replace(frame,candidates=frame.candidates.advance(4))\n                frame = _scene_refresh_decrement(frame,\'offset_x\',row_longs - 1 - index)\n        else:\n            frame = _first_long(frame,\'offset_y\',0)\n            frame = _first_long(frame,\'choice\',0)\n            nibbles = 8\n            frame = _first_word(frame,\'distance\',nibbles - 1)\n            for index in range(nibbles):\n                frame = _glyph_shift_long_fields(memory,frame,\'offset_y\',4)\n                frame = _glyph_shift_long_fields(memory,frame,\'choice\',4)\n                frame = _first_word(frame,\'offset_y\',low16(frame.offset_y) | low16(frame.target_x))\n                frame = _first_word(frame,\'choice\',low16(frame.choice) | low16(frame.target_y))\n                frame = _scene_refresh_decrement(frame,\'distance\',nibbles - 1 - index)\n            frame = _first_word(frame,\'distance\',row_longs - 1)\n            for index in range(row_longs):\n                frame = _scene_refresh_emit(memory,frame,frame.candidates.base + 0x40,4,frame.offset_y)\n                destination = frame.candidates\n                frame = first_replace(frame,candidates=destination.advance(4))\n                frame = _scene_refresh_emit(memory,frame,destination.base,4,frame.offset_y)\n                frame = _scene_refresh_decrement(frame,\'distance\',row_longs - 1 - index)\n            frame = _scene_refresh_emit(memory,frame,frame.candidates.base - 0x24,4,frame.choice)\n            frame = _scene_refresh_emit(memory,frame,frame.candidates.base + 0x1C,4,frame.choice)\n        frame = first_replace(frame,candidates=frame.candidates.advance(0x40))\n        frame = _scene_refresh_decrement(frame,\'count\',remaining)\n        remaining = u16(remaining - 1)\n        if remaining == 65535:\n            return memory.sync_status(_glyph_restore_fields(memory,frame,original,True))', 'expand_glyph_row_fields': 'def expand_glyph_row_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """AF04 sole eight-pixel row: real LSL.L/ROXL.B/OR.B and retained D6."""\n    memory.frame(frame)\n    if frame.target_x is None or frame.target_y is None or frame.controller is None:\n        raise SceneRefreshBoundary(0xAF04,frame,None)\n    frame = _first_long(frame,\'choice\',0)\n    bits = frame.controller.byte()\n    frame = first_replace(frame,controller=frame.controller.advance(1))\n    frame = _first_byte(frame,\'offset_y\',bits)\n    row_bits = 8\n    frame = _first_word(frame,\'distance\',row_bits - 1)\n    for index in range(row_bits):\n        frame = _glyph_shift_long_fields(memory,frame,\'choice\',4)\n        carry = bool(bits & 128)\n        bits = u8((bits << 1) | bool(frame.status & 16))\n        carrier = None if frame.offset_y is None else replace_byte(frame.offset_y,bits)\n        status = (17 if carry else 0) | (8 if bits & 128 else 0) | (4 if bits == 0 else 0)\n        frame = first_replace(frame,offset_y=carrier,status=status)\n        color = low8(frame.target_y) if carry else low8(frame.target_x)\n        frame = _first_byte(frame,\'choice\',low8(frame.choice) | color)\n        frame = _scene_refresh_decrement(frame,\'distance\',row_bits - 1 - index)\n    return memory.sync_status(frame)', '_glyph_row_call_fields': "def _glyph_row_call_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, continuation: Long) -> FirstDeploymentFrame:\n    if continuation not in (0xAEBA,0xAEC0,0xAF38):\n        raise ValueError('real glyph-row return token required')\n    entered = frame\n    if frame.stack_cursor is not None:\n        stack = frame.stack_cursor.advance(-4)\n        stack.set_long(0,continuation)\n        entered = first_replace(frame,stack_cursor=stack)\n    result = expand_glyph_row_fields(memory,entered)\n    if frame.stack_cursor is not None:\n        actual = result.stack_cursor.long()\n        if actual != continuation:\n            raise SceneRefreshBoundary(0xAF04,result,continuation)\n        result = first_replace(result,stack_cursor=result.stack_cursor.advance(4))\n    return memory.sync_status(result)", '_glyph_shift_long_fields': 'def _glyph_shift_long_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, amount: Word) -> FirstDeploymentFrame:\n    original = frame.carrier(name)\n    if original is None:\n        raise SceneRefreshBoundary(0xAF0C,frame,None)\n    value = u32(original << amount)\n    carry = bool(original & (1 << (32 - amount)))\n    status = (17 if carry else 0) | (8 if value & 0x80000000 else 0) | (4 if value == 0 else 0)\n    return memory.sync_status(first_replace(frame,status=status,**{name:value}))', '_glyph_save_fields': 'def _glyph_save_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, include_source: bool) -> FirstDeploymentFrame:\n    if frame.stack_cursor is None:\n        return frame\n    values = (frame.choice,frame.offset_y,frame.offset_x,frame.distance)\n    if include_source:\n        values = (frame.controller.base,) + values\n    return _scene_render_push_longs(memory,frame,values)', '_glyph_restore_fields': 'def _glyph_restore_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, original: FirstDeploymentFrame, include_source: bool) -> FirstDeploymentFrame:\n    if frame.stack_cursor is None:\n        return first_replace(frame,distance=original.distance,offset_x=original.offset_x,\n            offset_y=original.offset_y,choice=original.choice,\n            controller=original.controller if include_source else frame.controller)\n    stack = frame.stack_cursor\n    values = tuple(stack.long(index * 4) for index in range(4))\n    frame = first_replace(frame,distance=values[0],offset_x=values[1],offset_y=values[2],choice=values[3])\n    if include_source:\n        frame = first_replace(frame,controller=memory.cursor_at(stack.long(16)))\n    return first_replace(frame,stack_cursor=stack.advance(20 if include_source else 16))'}}


def _information_source_tree(group, original_tree):
    """Only six CALL expression sites change; invert each entire source module."""
    if group not in VIEW_SPECS:
        raise ValueError('only the reviewed information-panel source families are admitted')
    derived = copy.deepcopy(original_tree)
    inverses = {}
    for index, original in enumerate(original_tree.body):
        if not isinstance(original, ast.FunctionDef) or original.name not in VIEW_SPECS[group]:
            continue
        if _dump(original) != _dump(ast.parse(EXPECTED_SOURCE[group][original.name]).body[0]):
            raise ValueError('complete information-panel source owner changed: ' + original.name)
        if any(isinstance(node, (ast.Yield, ast.YieldFrom)) for node in ast.walk(original)):
            raise ValueError('the original complete information-panel body must remain synchronous')
        counts = {name: 0 for name in VIEW_SPECS[group][original.name]}
        substitutions = []

        class Lift(ast.NodeTransformer):
            def visit_Call(self, node):
                node = self.generic_visit(node)
                if not isinstance(node.func, ast.Name) or node.func.id not in counts:
                    return node
                before = copy.deepcopy(node)
                counts[node.func.id] += 1
                node.func.id = '_information_campaign_call'
                after = ast.copy_location(ast.YieldFrom(value=node), node)
                substitutions.append((before, copy.deepcopy(after)))
                return after

        current = Lift().visit(copy.deepcopy(original))
        if counts != VIEW_SPECS[group][original.name]:
            raise ValueError('exact information-panel CALL expression count differs: ' + original.name)
        pending = list(substitutions)

        class Inverse(ast.NodeTransformer):
            def visit_YieldFrom(self, node):
                for position, (before, after) in enumerate(pending):
                    if _dump(node) == _dump(after):
                        pending.pop(position)
                        return copy.deepcopy(before)
                raise ValueError('undeclared information-panel suspension')

        restored = Inverse().visit(copy.deepcopy(current))
        if pending or _dump(restored) != _dump(original):
            raise ValueError('whole original information-panel function inverse differs: ' + original.name)
        derived.body[index] = current
        inverses[index] = restored
    if len(inverses) != len(VIEW_SPECS[group]):
        raise ValueError('all complete information-panel functions must be present')
    restored_module = copy.deepcopy(derived)
    for index, original in inverses.items():
        restored_module.body[index] = original
    if _dump(restored_module) != _dump(original_tree):
        raise ValueError('whole original information-panel module inverse differs')
    return ast.fix_missing_locations(derived)


class InformationPanelScenePrograms(BattleScenePrograms):
    """One original indexed parent retaining all real child LONGs and full Frame."""

    def __init__(self, state):
        super().__init__(state)
        self.information_modules = {group: importlib.import_module(path)
            for group, path in MODULE_PATHS.items()}
        self.information_originals, self.information_codes = {}, {}
        self.information_views, self.information_namespaces, self.information_bindings = {}, {}, {}
        for group, module in self.information_modules.items():
            tree = ast.parse(inspect.getsource(module), filename=module.__file__)
            plain = compile(tree, module.__file__, 'exec', dont_inherit=True)
            expected = dict(EXPECTED_REUSED_SOURCE.get(group, {}))
            expected.update(EXPECTED_SOURCE[group])
            for name, source in expected.items():
                nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
                owner = getattr(module, name)
                if (len(nodes) != 1 or _dump(nodes[0]) != _dump(ast.parse(source).body[0])
                        or type(owner) is not FunctionType or owner.__globals__ is not vars(module)
                        or owner.__module__ != module.__name__ or owner.__name__ != name
                        or owner.__closure__ is not None or owner.__code__.co_freevars
                        or _code_shape(owner.__code__) != _code_shape(_top_code(plain, name))):
                    raise ValueError('actual complete unwrapped information-panel function required: ' + name)
                self.information_originals[group, name], self.information_codes[group, name] = owner, owner.__code__
            if not VIEW_SPECS[group]:
                continue
            code = compile(_information_source_tree(group, tree), module.__file__, 'exec', dont_inherit=True)
            namespace = self.information_namespaces[group] = dict(vars(module))
            if '_information_campaign_call' in namespace:
                raise ValueError('the private information-panel alias cannot shadow an original binding')
            namespace['_information_campaign_call'] = self.views['main', '_campaign_call_fields']
            self.information_bindings[group, '_information_campaign_call'] = namespace['_information_campaign_call']
            for name in VIEW_SPECS[group]:
                owner = self.information_originals[group, name]
                view = FunctionType(_top_code(code, name), namespace, name, owner.__defaults__, None)
                view.__kwdefaults__, view.__annotations__ = owner.__kwdefaults__, dict(owner.__annotations__)
                if not inspect.isgeneratorfunction(view) or view.__closure__ is not None:
                    raise ValueError('a complete closure-free information-panel generator is required')
                self.information_views[group, name] = view
        self.information_view_owners = dict(self.information_views)
        self.information_view_codes = {key: view.__code__ for key, view in self.information_views.items()}

    def require_current(self, state):
        super().require_current(state)
        if not hasattr(self, 'information_originals'):
            return
        for key, owner in self.information_originals.items():
            if (getattr(self.information_modules[key[0]], key[1]) is not owner
                    or owner.__code__ is not self.information_codes[key]):
                raise ValueError('the actual information-panel source owner changed: ' + key[1])
        if self.information_views.keys() != self.information_view_owners.keys():
            raise ValueError('the complete information-panel view set changed')
        for key, view in self.information_view_owners.items():
            if self.information_views[key] is not view or view.__code__ is not self.information_view_codes[key]:
                raise ValueError('the actual information-panel view changed: ' + key[1])
        for (group, name), value in self.information_bindings.items():
            if self.information_namespaces[group].get(name) is not value:
                raise ValueError('the private information-panel call binding changed')

    def _campaign_child(self, state, frame, target, continuation):
        self.require_current(state)
        name = PANEL_CALLS.get((target, continuation))
        if name is not None:
            return (yield from self.information_views['commands', name](state, frame))
        if target in (0xBAEA, 0xC372):
            raise MovementContinuationBoundary(target, frame, 'information parent requires its original Main LONG')
        if (target, continuation) in REFRESH_CALLS:
            # The complete inherited CALL bridge has already pushed this LONG.
            # Do not add another wrapper CALL around the actual AF48 program.
            return (yield from self._refresh(SceneRefreshMemory(state), frame))
        return (yield from super()._campaign_child(state, frame, target, continuation))

    def _display_child(self, state, frame, target, continuation):
        self.require_current(state)
        if target in MAIN_ENTRIES:
            if continuation != 0x3CE:
                raise MovementContinuationBoundary(target, frame, 'information Main requires original3CE LONG')
            return (yield from self.information_views['main', MAIN_ENTRIES[target]](state, frame))
        return (yield from super()._display_child(state, frame, target, continuation))

    def main_scene_call(self, state, frame, target, continuation):
        if target not in MAIN_ENTRIES:
            return (yield from super().main_scene_call(state, frame, target, continuation))
        self.require_current(state)
        if self._started or continuation != 0x3CE:
            raise ValueError('one actual Main404/40C information-plane invocation required')
        self._started = True
        return (yield from self.views['display', 'display_call_fields'](state, frame, target, continuation))
