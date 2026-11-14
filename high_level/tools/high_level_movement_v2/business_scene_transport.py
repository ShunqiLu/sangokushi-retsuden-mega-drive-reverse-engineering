"""Original transport preparation over complete live Scene D/A/SR/SP fields."""
from ..high_level_scene_flows.domain import SceneState, low8, low16
from ..high_level_battle_ai.contexts_first_deployment import (
    FirstDeploymentFrame, FirstDeploymentReturnBoundary, first_replace,
)
from ..high_level_main_flows.business_movement_support import (
    _movement_frame, _movement_move, _movement_fixed_shift_word, build_path_fields,
)
from ..high_level_remaining_flows.business_lowbank import _economy_logic_fields, _lowbank_ui_store_fields


def prepare_transport_path_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """16ACC..16B3A: original budget/endpoints, actual6518/16B28, mode20A."""
    frame = _movement_frame(state,frame)
    frame = _movement_move(state,frame,'target_x',state.read(0xFFFFCEA0,2),16)
    frame = _movement_fixed_shift_word(state,frame,'target_x',2)
    frame = first_replace(frame,roster=state.table_at(0xFFFFCE00).cursor())
    frame = _movement_move(state,frame,'target_y',15,16)
    frame = _movement_move(state,frame,'unit',frame.roster.byte(low16(frame.target_x)),8)
    frame = _economy_logic_fields(state,frame,'unit',3,16)
    from ..high_level_main_flows.business_movement_support import _movement_compare
    frame = _movement_compare(state,frame,low8(frame.unit),3,8)
    if frame.status & 4:
        frame = _movement_move(state,frame,'target_y',10,16)
    frame = _lowbank_ui_store_fields(state,frame,0xFFFFCEA2,low16(frame.target_y))
    for displacement,destination in ((1,0xFFFFF63C),(2,0xFFFFF63E)):
        frame = _movement_move(state,frame,'target_y',0,16)
        frame = _movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x),displacement),8)
        frame = _movement_fixed_shift_word(state,frame,'target_y',4)
        frame = _lowbank_ui_store_fields(state,frame,destination,low16(frame.target_y))
    frame = _movement_move(state,frame,'target_y',0,16)
    frame = _movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x),3),8)
    frame = _movement_fixed_shift_word(state,frame,'target_y',2)
    frame = first_replace(frame,roster=state.table_at(0xD4AC6).cursor())
    frame = _lowbank_ui_store_fields(state,frame,0xFFFFF640,frame.roster.word(low16(frame.target_y),2))
    frame = _lowbank_ui_store_fields(state,frame,0xFFFFF642,frame.roster.word(low16(frame.target_y)))
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0,0x16B28)
    frame = build_path_fields(state,first_replace(frame,stack_cursor=stack))
    actual = frame.stack_cursor.long()
    if actual != 0x16B28:
        raise FirstDeploymentReturnBoundary(actual,frame,0x16B28)
    frame = first_replace(frame,stack_cursor=frame.stack_cursor.advance(4))
    frame = _lowbank_ui_store_fields(state,frame,0xFFFFF612,0x20A)
    frame = _lowbank_ui_store_fields(state,frame,0xFFFFF362,1)
    return _lowbank_ui_store_fields(state,frame,0xFFFFCEAC,0,2,True)
