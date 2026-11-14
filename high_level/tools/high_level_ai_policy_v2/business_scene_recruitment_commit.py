"""Original recruitment commitment through actual Scene carriers.

confirmed:332C0..33322 from dispatch_descendants.s. The selected actor and the
recruited officer remain distinct live identities. No scalar result is used
to fabricate unobserved fields; the incoming dispatcher LONG is retained.
"""
from ..high_level_scene_flows.domain import SceneState, low8, low16
from ..high_level_battle_ai.contexts_first_deployment import (
    FirstDeploymentFrame, FirstDeploymentReturnBoundary, first_replace,
)
from ..high_level_main_flows.business_movement_support import (
    _movement_frame, _movement_move, _movement_compare, _movement_fixed_shift_word,
)
from ..high_level_ai_decision.scene_fields import store_ai_value_fields, adjust_ai_carrier_fields


def _recruitment_commit_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """The two original calls; outer33054 belongs to the dispatcher."""
    if (target, continuation) not in ((0x5F48,0x332D0),(0x320A0,0x3331A)):
        raise ValueError('actual recruitment commitment CALL pair required')
    frame = _movement_frame(state, frame)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    if target == 0x5F48:
        from ..high_level_gameplay_flow.business_battle import build_roster_fields
        from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
        result = build_roster_fields(BattlePresentationMemory(state), entered)
    else:
        from ..high_level_remaining_flows.business_highbank import mark_selected_roster_bit14_fields
        result = mark_selected_roster_bit14_fields(state, entered)
    result = _movement_frame(state, result)
    returned = result.stack_cursor.long()
    if returned != continuation:
        raise FirstDeploymentReturnBoundary(returned, result, continuation)
    return first_replace(result, stack_cursor=result.stack_cursor.advance(4))


def commit_recruitment_candidate_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """332C0: recheck capacity, assign candidate, reward actor, advance8."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364,2),16)
    frame = store_ai_value_fields(state,frame,0xFFFFF630,65535,16)
    frame = _recruitment_commit_call_fields(state,frame,0x5F48,0x332D0)
    frame = _movement_compare(state,frame,low16(frame.count),10,16)
    if frame.status & 1:
        frame = _movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
        frame = first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
        frame = _movement_move(state,frame,'target_y',state.read(0xFFFFF3F2,2),16)
        frame = store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_y)),low8(frame.target_x),8)
        frame = first_replace(frame,roster=state.table_at(0xFFFFBE00).cursor())
        frame = _movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
        frame = _movement_fixed_shift_word(state,frame,'target_x',1)
        frame = _movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_x)),16)
        frame = adjust_ai_carrier_fields(state,frame,'target_y',10)
        frame = _movement_compare(state,frame,low16(frame.target_y),999,16)
        if not frame.status & 5:
            frame = _movement_move(state,frame,'target_y',999,16)
        frame = store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_x)),low16(frame.target_y),16)
        frame = _movement_fixed_shift_word(state,frame,'target_x',1,True)
        frame = first_replace(frame,roster=state.table_at(0xFFFFCD00).cursor())
        frame = store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_x)),1,8)
        frame = _recruitment_commit_call_fields(state,frame,0x320A0,0x3331A)
    return store_ai_value_fields(state,frame,0xFFFFF728,8,16)
