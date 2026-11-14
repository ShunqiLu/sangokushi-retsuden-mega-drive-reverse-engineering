"""Complete city-personnel joining parent, bribe outcome and probability owners.

The original five whole owners retain actual physical CALL/WORD slots and all
partial D/A/CCR-X carriers. Consequences already owned by persuasion remain
single-source; no scalar result is promoted into an invented Frame.
"""
from ..high_level_scene_flows.domain import SceneState,low8,low16
from ..high_level_battle_ai.contexts_first_deployment import (
    FirstDeploymentFrame,FirstDeploymentReturnBoundary,first_replace,
)
from ..high_level_main_flows.business_movement_support import (
    _movement_frame,_movement_move,_movement_move_long,_movement_compare,
    _movement_fixed_shift_word,_movement_multiply_word,
)
from ..high_level_remaining_flows.business_lowbank import (
    _economy_delta_fields,_economy_memory_delta_fields,
    _economy_long_shift_fields,_economy_swap_fields,_lowbank_ui_store_fields,
)

REAL_CALL_PAIRS=(
    (0x111C0,0x111B8),(0x1161A,0x111BE),(0x11312,0x1125C),
    (0x113BC,0x11276),(0x113F6,0x1127A),(0x676F2,0x11296),
    (0x1142E,0x1129E),(0x11466,0x112A6),(0x208CE,0x112D8),
    (0x676F2,0x1130A),(0x83D4,0x11318),(0x83D4,0x113FC),(0x83D4,0x11434),
)


def _city_joining_call_fields(state: SceneState,frame: FirstDeploymentFrame,
        target: int,continuation: int) -> FirstDeploymentFrame:
    if (target,continuation) not in REAL_CALL_PAIRS:
        raise ValueError('actual finite original city-joining CALL pair required')
    frame=_movement_frame(state,frame)
    stack=frame.stack_cursor.advance(-4)
    stack.set_long(0,continuation)
    entered=first_replace(frame,stack_cursor=stack)
    if target==0x83D4:
        from ..high_level_battle_ai.business_formation import first_deployment_random_fields
        from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
        returned=first_deployment_random_fields(BattlePolicyMemory(state),entered)
    elif target==0x208CE:
        from ..high_level_gameplay_flow.business_reuse import apply_returning_officer_loyalty_fields
        from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
        returned=apply_returning_officer_loyalty_fields(BattlePresentationMemory(state),entered)
    elif target==0x676F2:
        from ..high_level_command_actions.business_reuse import prepare_scene_message_frame_fields
        returned=prepare_scene_message_frame_fields(state,entered)
    elif target in (0x113BC,0x11466,0x1161A):
        from .business_scene_personnel import (
            penalize_force_head_affinity_fields,transfer_joining_officer_fields,
            settle_persuasion_joining_fields,
        )
        if target==0x113BC:
            returned=penalize_force_head_affinity_fields(state,entered)
        elif target==0x11466:
            returned=transfer_joining_officer_fields(state,entered)
        else:
            returned=settle_persuasion_joining_fields(state,entered)
    else:
        owners={0x111C0:settle_bribe_joining_fields,0x11312:bribe_acceptance_factor_fields,
            0x113F6:reward_force_head_small_progress_fields,0x1142E:reward_force_head_large_progress_fields}
        returned=owners[target](state,entered)
    returned=_movement_frame(state,returned)
    actual=returned.stack_cursor.long()
    if actual!=continuation:
        raise FirstDeploymentReturnBoundary(actual,returned,continuation)
    return first_replace(returned,stack_cursor=returned.stack_cursor.advance(4))


def settle_personnel_joining_fields(state: SceneState,frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """111AC..111C0: original F57D BYTE74 chooses two whole policy owners."""
    frame=_movement_frame(state,frame)
    frame=_movement_compare(state,frame,state.read(0xFFFFF57D,1),74,8)
    if frame.status&4:
        return _city_joining_call_fields(state,frame,0x111C0,0x111B8)
    return _city_joining_call_fields(state,frame,0x1161A,0x111BE)


def settle_bribe_joining_fields(state: SceneState,frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """111C0..11312: original cancel, paid rejection and accepted transfer."""
    frame=_movement_frame(state,frame)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),119,16)
    if frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,32)
        frame=_movement_move(state,frame,'target_x',85,16)
        frame=_city_joining_call_fields(state,frame,0x676F2,0x1130A)
        return _lowbank_ui_store_fields(state,frame,0xFFFFF652,1)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',2)
    for base,amount in ((0xFFFFDFFC,0xFFFFF39E),(0xFFFFE09C,0xFFFFF3BA)):
        frame=first_replace(frame,roster=state.table_at(base).cursor())
        frame=_movement_move_long(state,frame,'target_y',state.read(amount,4))
        frame=_economy_memory_delta_fields(state,frame,frame.roster.address(low16(frame.target_x)),frame.target_y,32,True)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A8,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF427).cursor())
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_y)),16)
    frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF3A6,2),16)
    accepted=False
    if not frame.status&4:
        frame=_movement_move_long(state,frame,'unit',state.read(0xFFFFF39E,4))
        frame=_economy_delta_fields(state,frame,'unit',state.read(0xFFFFF3BA,4),32)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
        frame=first_replace(frame,roster=state.table_at(0xFFFFF427).cursor())
        frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_x)),8)
        frame=_movement_fixed_shift_word(state,frame,'target_x',1)
        frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
        frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
        frame=first_replace(frame,roster=state.table_at(0xFFFFC200).cursor())
        frame=_movement_move(state,frame,'count',0,16)
        frame=_movement_move(state,frame,'count',frame.roster.byte(low16(frame.target_x)),8)
        frame=_movement_move(state,frame,'target_x',low16(frame.unit),16)
        frame=_movement_multiply_word(state,frame,'target_x',low16(frame.count))
        frame=_economy_swap_fields(state,frame,'unit')
        frame=_movement_multiply_word(state,frame,'unit',low16(frame.count))
        frame=_economy_swap_fields(state,frame,'unit')
        frame=_economy_delta_fields(state,frame,'unit',frame.target_x,32)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
        frame=first_replace(frame,roster=state.table_at(0xFFFFC300).cursor())
        frame=_movement_move(state,frame,'count',0,16)
        frame=_movement_move(state,frame,'count',frame.roster.byte(low16(frame.target_x)),8)
        frame=_movement_multiply_word(state,frame,'count',low16(frame.count))
        frame=first_replace(frame,roster=state.table_at(0xFFFFC200).cursor())
        frame=_movement_move(state,frame,'distance',0,16)
        frame=_movement_move(state,frame,'distance',frame.roster.byte(low16(frame.target_x)),8)
        frame=_movement_multiply_word(state,frame,'count',low16(frame.distance))
        frame=_city_joining_call_fields(state,frame,0x11312,0x1125C)
        frame=_movement_move(state,frame,'target_y',low16(frame.count),16)
        frame=_movement_multiply_word(state,frame,'target_y',low16(frame.target_x))
        frame=_economy_swap_fields(state,frame,'count')
        frame=_movement_move_long(state,frame,'count',low16(frame.count))
        frame=_movement_multiply_word(state,frame,'count',low16(frame.target_x))
        frame=_economy_swap_fields(state,frame,'count')
        frame=_economy_delta_fields(state,frame,'count',frame.target_y,32)
        frame=_movement_compare(state,frame,frame.unit,frame.count,32)
        accepted=not bool(frame.status&1)
    if not accepted:
        frame=_city_joining_call_fields(state,frame,0x113BC,0x11276)
        frame=_city_joining_call_fields(state,frame,0x113F6,0x1127A)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,32)
        frame=_movement_move(state,frame,'target_x',91,16)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2))
        return _city_joining_call_fields(state,frame,0x676F2,0x11296)
    frame=_city_joining_call_fields(state,frame,0x1142E,0x1129E)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=_city_joining_call_fields(state,frame,0x11466,0x112A6)
    for address,value in ((0xFFFFF612,520),(0xFFFFF362,40),(0xFFFFF3FE,90)):
        frame=_lowbank_ui_store_fields(state,frame,address,value)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D2,state.read(0xFFFFF3A6,2))
    saved=state.read(0xFFFFF3F2,2)
    stack=frame.stack_cursor.advance(-2)
    frame=_lowbank_ui_store_fields(state,frame,stack.base,saved)
    frame=first_replace(frame,stack_cursor=stack,roster=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3F2,frame.roster.word(low16(frame.target_x)))
    frame=_city_joining_call_fields(state,frame,0x208CE,0x112D8)
    restored=frame.stack_cursor.word()
    frame=first_replace(frame,stack_cursor=frame.stack_cursor.advance(2))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3F2,restored)
    frame=_lowbank_ui_store_fields(state,frame,0x00FF7026,14)
    for address in (0xFFFFF386,0xFFFFF384,0xFFFFF64E):
        frame=_lowbank_ui_store_fields(state,frame,address,0,2,True)
    return frame


def bribe_acceptance_factor_fields(state: SceneState,frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """11312..11380: actual BYTE status/trait bands and table at11380."""
    frame=_movement_frame(state,frame)
    frame=_city_joining_call_fields(state,frame,0x83D4,0x11318)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC300).cursor())
    frame=_movement_move(state,frame,'distance',frame.roster.byte(low16(frame.target_x)),8)
    frame=_movement_move(state,frame,'target_y',0,16)
    for threshold in (30,50,70,80,90):
        frame=_movement_compare(state,frame,low8(frame.distance),threshold,8)
        if frame.status&5:
            break
        frame=_economy_delta_fields(state,frame,'target_y',1)
    frame=_movement_move(state,frame,'distance',low16(frame.target_y),16)
    frame=_movement_fixed_shift_word(state,frame,'distance',2)
    frame=_economy_delta_fields(state,frame,'target_y',low16(frame.distance))
    frame=first_replace(frame,roster=state.table_at(0xFFFFC700).cursor())
    frame=_movement_move(state,frame,'distance',frame.roster.byte(low16(frame.target_x)),8)
    frame=_movement_move(state,frame,'distance',low16(frame.distance)&7,16)
    frame=_economy_delta_fields(state,frame,'distance',low16(frame.target_y))
    frame=_movement_fixed_shift_word(state,frame,'distance',1)
    # Actual11364 LEA26(PC):11366+26=11380, followed by originalNOP.
    frame=first_replace(frame,roster=state.table_at(0x11380).cursor())
    frame=_movement_move(state,frame,'target_x',0,16)
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.distance)),8)
    frame=_movement_multiply_word(state,frame,'target_x',state.read(0xFFFFF61C,2))
    frame=_economy_swap_fields(state,frame,'target_x')
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.distance),1),8)
    return _economy_delta_fields(state,frame,'target_x',low16(frame.target_y))


def _bribe_force_progress_fields(state: SceneState,frame: FirstDeploymentFrame,
        large: bool) -> FirstDeploymentFrame:
    """113FC/11434: original progress suffix caps only WORD carry, not999."""
    if type(large)is not bool:
        raise ValueError('actual small/large force progress profile required')
    if large:
        frame=_movement_move_long(state,frame,'target_x',low16(frame.target_x))
    else:
        frame=_movement_move_long(state,frame,'target_x',0)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF61C,2),16)
    frame=_movement_move_long(state,frame,'target_y',frame.target_x)
    frame=_economy_long_shift_fields(state,frame,'target_x',2 if large else 1)
    frame=_economy_delta_fields(state,frame,'target_x',frame.target_y,32)
    frame=_economy_swap_fields(state,frame,'target_x')
    frame=_economy_delta_fields(state,frame,'target_x',1)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF376,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_y)),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFBE00).cursor())
    address=frame.roster.address(low16(frame.target_y))
    frame=_economy_memory_delta_fields(state,frame,address,low16(frame.target_x),16)
    if frame.status&1:
        frame=_lowbank_ui_store_fields(state,frame,address,65535)
    return frame


def reward_force_head_small_progress_fields(state: SceneState,frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """113F6..1142E: real RNG then actual seed WORD reread and sample×3."""
    frame=_movement_frame(state,frame)
    frame=_city_joining_call_fields(state,frame,0x83D4,0x113FC)
    return _bribe_force_progress_fields(state,frame,False)


def reward_force_head_large_progress_fields(state: SceneState,frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1142E..11466: real RNG's returned lowWORD sample×5, no seed reread."""
    frame=_movement_frame(state,frame)
    frame=_city_joining_call_fields(state,frame,0x83D4,0x11434)
    return _bribe_force_progress_fields(state,frame,True)
