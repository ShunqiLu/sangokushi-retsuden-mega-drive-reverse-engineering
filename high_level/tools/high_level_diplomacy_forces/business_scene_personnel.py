"""Complete personnel persuasion/joining Scene-frame closure.

The readable personnel policy remains the logical reference. These twelve
original owners expose its actual live ABI: all sixteen LONG carriers, partial
register lanes, real nested CALL/WORD/MOVEM slots, RAM aliases and CCR-X. The
11624 after-response entry deliberately excludes the preceding cancel gate.
No ROM, opcode interpreter, scalar-to-frame promotion or host result is used.
"""
from ..high_level_scene_flows.domain import (
    SceneState, low8, low16, s16, u32, divu_retained,
)
from ..high_level_battle_ai.contexts_first_deployment import (
    FirstDeploymentFrame, FirstDeploymentReturnBoundary, first_replace,
)
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
from ..high_level_main_flows.business_movement_support import (
    _movement_frame, _movement_move, _movement_move_long, _movement_compare,
    _movement_fixed_shift_word, _movement_multiply_word, _movement_binary_flags,
    _movement_save_longs, _movement_restore_longs,
)
from ..high_level_ai_decision.scene_fields import (
    store_ai_value_fields, adjust_ai_carrier_fields, compare_ai_long_fields,
    step_ai_count_fields, test_ai_register_bit_fields,
)
from ..high_level_remaining_flows.business_lowbank import (
    _economy_long_shift_fields, _economy_swap_fields,
)


REAL_CALL_PAIRS=(
    (0x1173A,0x11656),(0x11874,0x1165E),(0x118D4,0x11662),
    (0x113BC,0x11666),(0x676F2,0x1169E),(0x118A2,0x116A6),
    (0x11466,0x116AE),(0x208CE,0x11718),(0x676F2,0x11732),
    (0x117F0,0x1178E),(0x83D4,0x117F6),(0x83D4,0x1187A),
    (0x83D4,0x118A8),(0x83D4,0x118DA),(0x83D4,0x113C2),
    (0x5F48,0x114D6),(0x5F48,0x1151A),(0xE1F6,0x11520),
    (0x11588,0x11538),(0x11546,0x1153C),(0x11564,0x11540),
    (0x115BC,0x11544),
)


def _joining_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Only the twenty-two real original CALL/return pairs, with physical SP."""
    if (target,continuation) not in REAL_CALL_PAIRS:
        raise ValueError('actual finite personnel CALL/return pair required')
    frame=_movement_frame(state,frame)
    stack=frame.stack_cursor.advance(-4)
    stack.set_long(0,continuation)
    entered=first_replace(frame,stack_cursor=stack)
    if target==0x83D4:
        from ..high_level_battle_ai.business_formation import first_deployment_random_fields
        from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
        returned=first_deployment_random_fields(BattlePolicyMemory(state),entered)
    elif target in (0x5F48,0xE1F6,0x208CE):
        from ..high_level_gameplay_flow.business_battle import build_roster_fields,choose_city_head_fields
        from ..high_level_gameplay_flow.business_reuse import apply_returning_officer_loyalty_fields
        from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
        port=BattlePresentationMemory(state)
        if target==0x5F48:
            returned=build_roster_fields(port,entered)
        elif target==0xE1F6:
            returned=choose_city_head_fields(port,entered)
        else:
            returned=apply_returning_officer_loyalty_fields(port,entered)
    elif target==0x676F2:
        from ..high_level_command_actions.business_reuse import prepare_scene_message_frame_fields
        returned=prepare_scene_message_frame_fields(state,entered)
    else:
        owners={0x1173A:persuasion_scores_fields,0x117F0:persuasion_factor_fields,
            0x11874:reward_actor_small_progress_fields,0x118A2:reward_actor_large_progress_fields,
            0x118D4:penalize_actor_affinity_fields,0x113BC:penalize_force_head_affinity_fields,
            0x11466:transfer_joining_officer_fields,0x11546:mark_c300_list_fields,
            0x11564:clear_city_orders_fields,0x11588:replace_city_assignments_fields,
            0x115BC:clear_selected_links_fields}
        returned=owners[target](state,entered)
    returned=_movement_frame(state,returned)
    actual=returned.stack_cursor.long()
    if actual!=continuation:
        raise FirstDeploymentReturnBoundary(actual,returned,continuation)
    return first_replace(returned,stack_cursor=returned.stack_cursor.advance(4))


def _joining_memory_arithmetic_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, source: int, width: int, subtract: bool=False) -> FirstDeploymentFrame:
    """Actual fixed-width RAM read-modify-write and its live arithmetic flags."""
    frame,result=_movement_binary_flags(state,frame,state.read(address,width//8),source,width,subtract)
    state.write(address,width//8,result)
    return frame


def _joining_push_word_fields(state: SceneState, frame: FirstDeploymentFrame,
        value: int) -> FirstDeploymentFrame:
    stack=frame.stack_cursor.advance(-2)
    frame=store_ai_value_fields(state,frame,stack.base,value,16)
    return first_replace(frame,stack_cursor=stack)


def _joining_pop_word_fields(state: SceneState, frame: FirstDeploymentFrame,
        carrier: str) -> FirstDeploymentFrame:
    value=frame.stack_cursor.word()
    frame=first_replace(frame,stack_cursor=frame.stack_cursor.advance(2))
    return _movement_move(state,frame,carrier,value,16)


def _joining_visible_force_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> tuple[FirstDeploymentFrame,bool]:
    """The original three short-circuit WORD comparisons, not a cached set."""
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
    for address in (0xFFFFF67A,0xFFFFF67C,0xFFFFF67E):
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(address,2),16)
        if frame.status&4:
            return frame,True
    return frame,False


def settle_persuasion_joining_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1161A primary entry: original response121 cancel gate and full owner."""
    frame=_movement_frame(state,frame)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),121,16)
    if not frame.status&4:
        return settle_persuasion_joining_after_response_fields(state,frame)
    frame=store_ai_value_fields(state,frame,0xFFFFF612,0x208,16)
    frame=store_ai_value_fields(state,frame,0xFFFFF362,0x20,16)
    frame=_movement_move(state,frame,'target_x',0x55,16)
    frame=_joining_call_fields(state,frame,0x676F2,0x11732)
    return store_ai_value_fields(state,frame,0xFFFFF652,1,16)


def settle_persuasion_joining_after_response_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """11624 alias: start after ten bytes; never read F38C or take cancel gate.

    A Python shared-body call creates no emulated CALL slot. The caller's
    existing three WORD saves and 33370 LONG return remain physically intact.
    """
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCD00).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_x)),1,8)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A8,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF427).cursor())
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_y)),16)
    frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF3F2,2),16)
    success=False
    if not frame.status&4:
        frame=_joining_call_fields(state,frame,0x1173A,0x11656)
        frame=compare_ai_long_fields(state,frame,frame.unit,frame.target_x)
        success=not bool(frame.status&1)
    if not success:
        for target,continuation in ((0x11874,0x1165E),(0x118D4,0x11662),(0x113BC,0x11666)):
            frame=_joining_call_fields(state,frame,target,continuation)
        frame,visible=_joining_visible_force_fields(state,frame)
        if visible:
            frame=store_ai_value_fields(state,frame,0xFFFFF612,0x208,16)
            frame=store_ai_value_fields(state,frame,0xFFFFF362,0x20,16)
            frame=_movement_move(state,frame,'target_x',0x53,16)
            frame=store_ai_value_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2),16)
            frame=_joining_call_fields(state,frame,0x676F2,0x1169E)
        return frame
    frame=_joining_call_fields(state,frame,0x118A2,0x116A6)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3F2,2),16)
    frame=_joining_call_fields(state,frame,0x11466,0x116AE)
    frame,visible=_joining_visible_force_fields(state,frame)
    if not visible:
        return frame
    for address,value in ((0xFFFFF612,0x208),(0xFFFFF362,0x28),(0xFFFFF3FE,0x5C)):
        frame=store_ai_value_fields(state,frame,address,value,16)
    frame=store_ai_value_fields(state,frame,0xFFFFF3D2,state.read(0xFFFFF3F2,2),16)
    frame=store_ai_value_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2),16)
    frame=store_ai_value_fields(state,frame,0x00FF7026,12,16)
    frame=store_ai_value_fields(state,frame,0xFFFFF386,0,16,True)
    frame=store_ai_value_fields(state,frame,0xFFFFF384,0,16,True)
    frame=store_ai_value_fields(state,frame,0xFFFFF3A6,state.read(0xFFFFF3F2,2),16)
    frame=store_ai_value_fields(state,frame,0xFFFFF64E,0,16,True)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=store_ai_value_fields(state,frame,0xFFFFF3F2,frame.roster.word(low16(frame.target_x)),16)
    return _joining_call_fields(state,frame,0x208CE,0x11718)


def persuasion_scores_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1173A: exact stitched LONG offer/requirement products and five live views."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3F2,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC300).cursor())
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
    frame=_movement_move(state,frame,'unit',100,16)
    frame=adjust_ai_carrier_fields(state,frame,'unit',low16(frame.target_y),16,True)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC200).cursor())
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
    frame=_movement_multiply_word(state,frame,'unit',low16(frame.target_y))
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
    frame=_movement_multiply_word(state,frame,'unit',low16(frame.target_y))
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFB600).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_x)),16)
    frame=_joining_product_unit_fields(state,frame)
    frame=_joining_call_fields(state,frame,0x117F0,0x1178E)
    frame=_joining_product_unit_fields(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3F2,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC200).cursor())
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
    frame=_movement_move(state,frame,'count',state.read(0xFFFFF3A8,2),16)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFF427).cursor())
    frame=_movement_move(state,frame,'distance',0,16)
    frame=_movement_move(state,frame,'distance',frame.candidates.byte(low16(frame.count)),8)
    frame=_movement_fixed_shift_word(state,frame,'distance',1)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'distance',frame.candidates.word(low16(frame.distance)),16)
    frame=_movement_move(state,frame,'count',0,16)
    frame=_movement_move(state,frame,'count',frame.roster.byte(low16(frame.distance)),8)
    frame=_movement_multiply_word(state,frame,'target_y',low16(frame.count))
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFB600).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
    frame=_movement_multiply_word(state,frame,'target_y',low16(frame.target_x))
    frame=_movement_move(state,frame,'count',state.read(0xFFFFEFD2,2),16)
    frame=_movement_fixed_shift_word(state,frame,'count',1)
    frame=first_replace(frame,roster=state.table_at(0x111A6).cursor())
    frame=_movement_move(state,frame,'count',frame.roster.word(low16(frame.count)),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_y),16)
    frame=_movement_multiply_word(state,frame,'target_x',low16(frame.count))
    frame=_economy_swap_fields(state,frame,'target_y')
    frame=_movement_multiply_word(state,frame,'target_y',low16(frame.count))
    frame=_economy_swap_fields(state,frame,'target_y')
    return adjust_ai_carrier_fields(state,frame,'target_x',frame.target_y,32)


def _joining_product_unit_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """The repeated original six-instruction D2×D1 stitched LONG product."""
    frame=_movement_move(state,frame,'target_x',low16(frame.unit),16)
    frame=_movement_multiply_word(state,frame,'target_x',low16(frame.target_y))
    frame=_economy_swap_fields(state,frame,'unit')
    frame=_movement_multiply_word(state,frame,'unit',low16(frame.target_y))
    frame=_economy_swap_fields(state,frame,'unit')
    return adjust_ai_carrier_fields(state,frame,'unit',frame.target_x,32)


def persuasion_factor_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """117F0: original trait WORD/BYTE asymmetry and un-clamped signed index."""
    frame=_movement_frame(state,frame)
    frame=_joining_call_fields(state,frame,0x83D4,0x117F6)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=_movement_move(state,frame,'target_y',4,16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC700).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_x)),8)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&7,16)
    frame=adjust_ai_carrier_fields(state,frame,'target_y',low16(frame.target_x),16,True)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_y),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',2)
    frame=adjust_ai_carrier_fields(state,frame,'target_x',low16(frame.target_y))
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3F2,2),16)
    frame=_movement_move(state,frame,'count',4,16)
    frame=_movement_move(state,frame,'distance',frame.roster.byte(low16(frame.target_y)),8)
    frame=_movement_move(state,frame,'distance',low16(frame.distance)&7,16)
    frame=adjust_ai_carrier_fields(state,frame,'count',low8(frame.distance),8,True)
    frame=adjust_ai_carrier_fields(state,frame,'target_x',low16(frame.count))
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=first_replace(frame,candidates=state.table_at(0x11842).cursor())
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'target_y',frame.candidates.byte(low16(frame.target_x)),8)
    frame=_movement_multiply_word(state,frame,'target_y',state.read(0xFFFFF61C,2))
    frame=_economy_swap_fields(state,frame,'target_y')
    frame=_movement_move(state,frame,'count',0,16)
    frame=_movement_move(state,frame,'count',frame.candidates.byte(low16(frame.target_x),1),8)
    return adjust_ai_carrier_fields(state,frame,'target_y',low16(frame.count))


def reward_actor_small_progress_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """11874: real seed×3 high WORD plus1; saturating actor progress WORD."""
    frame=_movement_frame(state,frame)
    frame=_joining_call_fields(state,frame,0x83D4,0x1187A)
    frame=_movement_move_long(state,frame,'target_x',0)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF61C,2),16)
    frame=_movement_move_long(state,frame,'target_y',frame.target_x)
    frame=_economy_long_shift_fields(state,frame,'target_x',1)
    frame=adjust_ai_carrier_fields(state,frame,'target_x',frame.target_y,32)
    frame=_economy_swap_fields(state,frame,'target_x')
    frame=adjust_ai_carrier_fields(state,frame,'target_x',1)
    return _joining_actor_progress_store_fields(state,frame)


def reward_actor_large_progress_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """118A2: actual RNG D0×6 high WORD plus5; not a second seed fetch."""
    frame=_movement_frame(state,frame)
    frame=_joining_call_fields(state,frame,0x83D4,0x118A8)
    frame=_movement_move_long(state,frame,'target_x',low16(frame.target_x))
    frame=_movement_move_long(state,frame,'target_y',frame.target_x)
    frame=_economy_long_shift_fields(state,frame,'target_x',1)
    frame=adjust_ai_carrier_fields(state,frame,'target_x',frame.target_y,32)
    frame=_economy_long_shift_fields(state,frame,'target_x',1)
    frame=_economy_swap_fields(state,frame,'target_x')
    frame=adjust_ai_carrier_fields(state,frame,'target_x',5)
    return _joining_actor_progress_store_fields(state,frame)


def _joining_actor_progress_store_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A6,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFBE00).cursor())
    address=frame.roster.address(low16(frame.target_y))
    frame=_joining_memory_arithmetic_fields(state,frame,address,low16(frame.target_x),16)
    if frame.status&1:
        frame=store_ai_value_fields(state,frame,address,0xFFFF,16)
    return frame


def penalize_actor_affinity_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """118D4: RNG×11 affinity debit, preserving original BYTE borrow clamp."""
    frame=_movement_frame(state,frame)
    frame=_joining_call_fields(state,frame,0x83D4,0x118DA)
    frame=_movement_move_long(state,frame,'target_x',low16(frame.target_x))
    frame=_movement_move_long(state,frame,'target_y',frame.target_x)
    frame=_economy_long_shift_fields(state,frame,'target_x',2)
    frame=adjust_ai_carrier_fields(state,frame,'target_x',frame.target_y,32)
    frame=_economy_long_shift_fields(state,frame,'target_x',1)
    frame=adjust_ai_carrier_fields(state,frame,'target_x',frame.target_y,32)
    frame=_economy_swap_fields(state,frame,'target_x')
    frame=first_replace(frame,roster=state.table_at(0xFFFFC200).cursor())
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF3A6,2),16)
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.unit)),8)
    frame=_movement_multiply_word(state,frame,'target_y',low16(frame.target_x))
    # DIVU's intermediate NZVC are overwritten by the immediately following SUB.B.
    frame=first_replace(frame,target_y=divu_retained(frame.target_y,100))
    address=frame.roster.address(low16(frame.unit))
    frame=_joining_memory_arithmetic_fields(state,frame,address,low8(frame.target_y),8,True)
    if frame.status&1:
        frame=store_ai_value_fields(state,frame,address,0,8,True)
    return frame


def penalize_force_head_affinity_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """113BC: RNG×4 force-head debit; unlike actor debit it has no clamp."""
    frame=_movement_frame(state,frame)
    frame=_joining_call_fields(state,frame,0x83D4,0x113C2)
    frame=_movement_move_long(state,frame,'target_x',low16(frame.target_x))
    frame=_movement_move_long(state,frame,'target_y',frame.target_x)
    frame=_economy_long_shift_fields(state,frame,'target_x',1)
    frame=adjust_ai_carrier_fields(state,frame,'target_x',frame.target_y,32)
    frame=adjust_ai_carrier_fields(state,frame,'target_x',frame.target_y,32)
    frame=_economy_swap_fields(state,frame,'target_x')
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF376,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_y)),16)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC200).cursor())
    frame=_movement_move(state,frame,'unit',frame.roster.byte(low16(frame.target_y)),8)
    frame=_movement_multiply_word(state,frame,'unit',low16(frame.target_x))
    frame=first_replace(frame,unit=divu_retained(frame.unit,100))
    return _joining_memory_arithmetic_fields(state,frame,frame.roster.address(low16(frame.target_y)),low8(frame.unit),8,True)


def transfer_joining_officer_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """11466: remove matching order, inspect remaining roster, retain/loss owner."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A8,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=adjust_ai_carrier_fields(state,frame,'target_y',state.read(0xFFFFF3A8,2))
    frame=_movement_fixed_shift_word(state,frame,'target_y',2)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE80C).cursor())
    for displacement in (0,4,8):
        frame=_movement_compare(state,frame,low16(frame.target_x),frame.roster.word(low16(frame.target_y),displacement),16)
        if frame.status&4:
            frame=store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_y),displacement),0xFFFF,16)
            break
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A8,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF45E).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_y)),16)
    frame=_movement_compare(state,frame,low16(frame.target_y),low16(frame.target_x),16)
    if not frame.status&4:
        frame=first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
        return store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_x)),state.read(0xFFFFF393,1),8)
    frame=_joining_push_word_fields(state,frame,low16(frame.target_x))
    frame=store_ai_value_fields(state,frame,0xFFFFF630,low16(frame.target_x),16)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A8,2),16)
    frame=_joining_call_fields(state,frame,0x5F48,0x114D6)
    frame=_joining_pop_word_fields(state,frame,'target_x')
    frame=_movement_compare(state,frame,low16(frame.count),1,16)
    lost=bool(frame.status&4)
    if not lost:
        frame=first_replace(frame,roster=state.table_at(0xFFFFF500).cursor(),candidates=state.table_at(0xFFFFC300).cursor())
        frame=_movement_move(state,frame,'target_y',0,16)
        frame=_movement_move(state,frame,'unit',0,16)
        while True:
            value=frame.roster.word()
            frame=first_replace(frame,roster=frame.roster.advance(2))
            frame=_movement_move(state,frame,'distance',value,16)
            if frame.status&8:
                break
            frame=_movement_move(state,frame,'target_y',frame.candidates.byte(low16(frame.distance)),8)
            frame=adjust_ai_carrier_fields(state,frame,'unit',low16(frame.target_y))
        frame=_movement_move_long(state,frame,'unit',u32(s16(low16(frame.unit))))
        divisor=low16(frame.count)
        if divisor==0:
            raise MovementContinuationBoundary(0x114F8,frame,'original DIVU zero divisor requires its exception owner')
        frame=first_replace(frame,unit=divu_retained(frame.unit,divisor))
        frame=_movement_compare(state,frame,low16(frame.unit),35,16)
        lost=bool(frame.status&5)
    if not lost:
        frame=first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
        frame=store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_x)),state.read(0xFFFFF393,1),8)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A8,2),16)
        frame=store_ai_value_fields(state,frame,0xFFFFF630,0xFFFF,16)
        frame=_joining_call_fields(state,frame,0x5F48,0x1151A)
        return _joining_call_fields(state,frame,0xE1F6,0x11520)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A8,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF427).cursor())
    # MOVE.B deliberately retains D1's upper BYTE; it is not a scalar owner ID.
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
    frame=store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_x)),state.read(0xFFFFF377,1),8)
    for target,continuation in ((0x11588,0x11538),(0x11546,0x1153C),(0x11564,0x11540),(0x115BC,0x11544)):
        frame=_joining_call_fields(state,frame,target,continuation)
    return frame


def mark_c300_list_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """11546: sentinel roster starts F502, mark only C300 BYTEs at least40."""
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF502).cursor(),candidates=state.table_at(0xFFFFC300).cursor())
    while True:
        value=frame.roster.word()
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_movement_move(state,frame,'target_x',value,16)
        if frame.status&8:
            return frame
        address=frame.candidates.address(low16(frame.target_x))
        frame=_movement_compare(state,frame,state.read(address,1),40,8)
        if not frame.status&1:
            frame=store_ai_value_fields(state,frame,address,state.read(address,1)|0x80,8)


def clear_city_orders_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """11564: original selected-city×12 index and three separate WORD stores."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A8,2),16)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=adjust_ai_carrier_fields(state,frame,'target_y',low16(frame.target_x))
    frame=_movement_fixed_shift_word(state,frame,'target_y',2)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE80C).cursor())
    for displacement in (0,4,8):
        frame=store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_y),displacement),0xFFFF,16)
    return frame


def replace_city_assignments_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """11588: exact three-LONG MOVEM and descending full256 assignment scan."""
    frame=_movement_frame(state,frame)
    saved=('target_y','unit','count')
    frame=_movement_save_longs(state,frame,saved)
    frame=_movement_move(state,frame,'unit',low16(frame.target_y),16)
    frame=adjust_ai_carrier_fields(state,frame,'unit',41)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A8,2),16)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_y)|0x40,16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
    frame=_movement_move(state,frame,'count',255,16)
    while True:
        frame=_movement_compare(state,frame,low8(frame.target_y),frame.roster.byte(low16(frame.count)),8)
        if frame.status&4:
            frame=store_ai_value_fields(state,frame,frame.roster.address(low16(frame.count)),low8(frame.unit),8)
        frame=step_ai_count_fields(frame,'count')
        if low16(frame.count)==0xFFFF:
            break
    return _movement_restore_longs(state,frame,saved)


def clear_selected_links_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """115BC: six-LONG MOVEM, sixteen debt pairs, live debt-mask BCLR alias."""
    frame=_movement_frame(state,frame)
    saved=('target_x','target_y','unit','roster','candidates','controller')
    frame=_movement_save_longs(state,frame,saved)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE65C).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A8,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',2)
    frame=store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_x)),0,32,True)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE9F8).cursor(),
        candidates=state.table_at(0xFFFFF427).cursor(),controller=state.table_at(0xFFFFE65C))
    frame=_movement_move(state,frame,'target_x',0,16)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A8,2),16)
    while True:
        frame=_movement_compare(state,frame,low8(frame.target_y),frame.roster.byte(),8)
        matched=bool(frame.status&4)
        if matched:
            frame=_movement_move(state,frame,'unit',0,16)
            frame=_movement_move(state,frame,'unit',frame.roster.byte(0,1),8)
            frame=_movement_fixed_shift_word(state,frame,'unit',2)
            frame=store_ai_value_fields(state,frame,frame.controller.address(low16(frame.unit)),0,32,True)
        else:
            frame=_movement_compare(state,frame,low8(frame.target_y),frame.roster.byte(0,1),8)
            matched=bool(frame.status&4)
        if matched:
            frame=store_ai_value_fields(state,frame,frame.roster.base,0,32,True)
            frame=_movement_move(state,frame,'unit',state.read(0xFFFFE700,2),16)
            # Dynamic BCLR.L changes only Z, retains X, and mutates the real D2.
            bit=frame.target_x&31
            frame=test_ai_register_bit_fields(state,frame,frame.unit,frame.target_x)
            frame=first_replace(frame,unit=frame.unit&~(1<<bit))
            frame=store_ai_value_fields(state,frame,0xFFFFE700,low16(frame.unit),16)
        frame=first_replace(frame,roster=frame.roster.advance(4))
        frame=adjust_ai_carrier_fields(state,frame,'target_x',1)
        frame=_movement_compare(state,frame,low16(frame.target_x),16,16)
        if not frame.status&1:
            break
    return _movement_restore_longs(state,frame,saved)
