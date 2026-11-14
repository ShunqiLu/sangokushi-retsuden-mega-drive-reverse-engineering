"""Complete direct method61 Scene rules and their ten original owners.

confirmed: F018..F778's remaining 864 bytes are named full-frame rules, not a
CPU interpreter. Resource-attempt/removal rules and common arithmetic effects
remain single-source in business_scene_stratagem. All real calls retain their
physical LONG return slots; the two original WORD saves remain physical RAM.
"""
from ..high_level_scene_flows.domain import SceneState, low8, low16, divu_retained
from ..high_level_battle_ai.contexts_first_deployment import (
    FirstDeploymentFrame, FirstDeploymentReturnBoundary, first_replace,
)
from ..high_level_main_flows.business_movement_support import (
    _movement_frame, _movement_move, _movement_move_long, _movement_test,
    _movement_compare, _movement_fixed_shift_word, _movement_multiply_word,
    _movement_divu_word,
)
from ..high_level_ai_decision.scene_fields import store_ai_value_fields, adjust_ai_carrier_fields
from ..high_level_remaining_flows.business_lowbank import _economy_long_shift_fields, _economy_swap_fields
from .business_scene_stratagem import (
    _stratagem_curve_fields, _stratagem_seed_sample_fields,
    _stratagem_extend_byte_fields, _stratagem_push_word_fields,
    _stratagem_pop_word_fields, _stratagem_memory_byte_fields,
    settle_method61_resource_attempt_fields, penalize_actor_small_affinity_fields,
    penalize_force_small_affinity_fields, reward_actor_small_c_progress_fields,
    remove_stratagem_target_fields, reward_actor_large_c_progress_fields,
)


REAL_CALL_PAIRS = (
    (0xF02C,0xF01C),(0xF088,0xF024),(0xF18E,0xF02A),
    (0x5F48,0xF044),(0x83D4,0xF050),
    (0xF630,0xF192),(0xF6AE,0xF19C),(0xF574,0xF1B6),
    (0xF28E,0xF1BA),(0xF2CE,0xF1BE),(0xF314,0xF1C2),
    (0xF388,0xF1C8),(0xF3C6,0xF1CC),(0xF314,0xF1D0),
    (0xF34C,0xF1E2),(0xF5F6,0xF1E6),(0x676F2,0xF22A),
    (0x83D4,0xF38E),(0x83D4,0xF3CC),(0x83D4,0xF590),
    (0xF5B6,0xF5AE),(0x5F48,0xF5EE),(0xE1F6,0xF5F4),
    (0x83D4,0xF688),(0xF71C,0xF6D0),(0x83D4,0xF6FA),
    (0x83D4,0xF766),
)


def _direct_stratagem_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Only the original finite direct-family CALL/return pairs, including F5F0."""
    if (target,continuation) not in REAL_CALL_PAIRS:
        raise ValueError('actual finite direct-stratagem CALL/return pair required')
    frame=_movement_frame(state,frame)
    stack=frame.stack_cursor.advance(-4)
    stack.set_long(0,continuation)
    entered=first_replace(frame,stack_cursor=stack)
    if target==0x83D4:
        from ..high_level_battle_ai.business_formation import first_deployment_random_fields
        from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
        returned=first_deployment_random_fields(BattlePolicyMemory(state),entered)
    elif target in (0x5F48,0xE1F6):
        from ..high_level_gameplay_flow.business_battle import build_roster_fields,choose_city_head_fields
        from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
        port=BattlePresentationMemory(state)
        returned=build_roster_fields(port,entered) if target==0x5F48 else choose_city_head_fields(port,entered)
    elif target==0x676F2:
        from ..high_level_command_actions.business_reuse import prepare_scene_message_frame_fields
        returned=prepare_scene_message_frame_fields(state,entered)
    else:
        owners={0xF02C:assess_method61_side_fields,
            0xF088:settle_method61_resource_attempt_fields,
            0xF18E:settle_method61_direct_attempt_fields,
            0xF630:choose_secondary_stratagem_target_fields,
            0xF6AE:method61_direct_probability_fields,
            0xF574:try_remove_secondary_target_fields,
            0xF28E:penalize_actor_small_affinity_fields,
            0xF2CE:penalize_force_small_affinity_fields,
            0xF314:reward_actor_small_c_progress_fields,
            0xF388:penalize_actor_large_affinity_fields,
            0xF3C6:penalize_force_large_affinity_fields,
            0xF34C:remove_stratagem_target_fields,
            0xF5F6:reward_actor_large_c_progress_fields,
            0xF5B6:remove_secondary_city_head_fields,
            0xF71C:method61_direct_factor_fields}
        returned=owners[target](state,entered)
    returned=_movement_frame(state,returned)
    actual=returned.stack_cursor.long()
    if actual!=continuation:
        raise FirstDeploymentReturnBoundary(actual,returned,continuation)
    return first_replace(returned,stack_cursor=returned.stack_cursor.advance(4))


def _direct_stratagem_affinity_debit_fields(state: SceneState,
        frame: FirstDeploymentFrame, instruction: int) -> FirstDeploymentFrame:
    """F3B4/F3F8 DIVU100 then actual BYTE SUB; the latter replaces NZVC.

    No undefined intermediate division flags are invented. The byte subtraction
    rereads live RAM, and BCC/CLR retains the original underflow clamp.
    """
    if instruction not in (0xF3B4,0xF3F8):
        raise ValueError('actual direct-stratagem affinity division site required')
    frame=first_replace(frame,unit=divu_retained(frame.unit,100))
    address=frame.roster.address(low16(frame.target_y))
    frame=_stratagem_memory_byte_fields(state,frame,address,low8(frame.unit),True)
    if frame.status&1:
        frame=store_ai_value_fields(state,frame,address,0,8,True)
    return frame


def settle_method61_stratagem_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F018: original side assessment followed by exactly one whole attempt."""
    frame=_movement_frame(state,frame)
    frame=_direct_stratagem_call_fields(state,frame,0xF02C,0xF01C)
    frame=_movement_test(state,frame,low16(frame.target_x),16)
    if frame.status&4:
        return _direct_stratagem_call_fields(state,frame,0xF088,0xF024)
    return _direct_stratagem_call_fields(state,frame,0xF18E,0xF02A)


def assess_method61_side_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F02C: build actual city roster, then the original 200-sample lottery."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A8,2),16)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF45E).cursor())
    frame=store_ai_value_fields(state,frame,0xFFFFF630,frame.roster.word(low16(frame.target_y)),16)
    frame=_direct_stratagem_call_fields(state,frame,0x5F48,0xF044)
    frame=_movement_compare(state,frame,low16(frame.count),1,16)
    if not frame.status&4:
        frame=_direct_stratagem_call_fields(state,frame,0x83D4,0xF050)
        frame=_movement_move_long(state,frame,'target_x',low16(frame.target_x))
        frame=_movement_move_long(state,frame,'target_y',frame.target_x)
        for amount,add_original in ((1,True),(3,True),(3,False)):
            frame=_economy_long_shift_fields(state,frame,'target_x',amount)
            if add_original:
                frame=adjust_ai_carrier_fields(state,frame,'target_x',frame.target_y,32)
        frame=_economy_swap_fields(state,frame,'target_x')
        frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A6,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_y',1)
        frame=first_replace(frame,roster=state.table_at(0xFFFFB600).cursor())
        frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_y)),16)
        frame=adjust_ai_carrier_fields(state,frame,'target_y',low16(frame.target_x))
        frame=_movement_compare(state,frame,low16(frame.target_y),180,16)
        result=1 if not frame.status&5 else 0
    else:
        result=0
    frame=_movement_move(state,frame,'target_x',result,16)
    return store_ai_value_fields(state,frame,0xFFFFF64A,low16(frame.target_x),16)


def settle_method61_direct_attempt_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F18E: retain selection failure, direct lottery, all penalties and message."""
    frame=_movement_frame(state,frame)
    frame=_direct_stratagem_call_fields(state,frame,0xF630,0xF192)
    frame=_movement_test(state,frame,low16(frame.target_x),16)
    if not frame.status&4:
        for target,continuation in ((0xF388,0xF1C8),(0xF3C6,0xF1CC),(0xF314,0xF1D0)):
            frame=_direct_stratagem_call_fields(state,frame,target,continuation)
        for address,value in ((0xFFFFF362,31),(0xFFFFF3FE,67)):
            frame=store_ai_value_fields(state,frame,address,value,16)
    else:
        frame=_direct_stratagem_call_fields(state,frame,0xF6AE,0xF19C)
        frame=_movement_test(state,frame,low16(frame.target_x),16)
        if frame.status&4:
            for address,value in ((0xFFFFF608,120),(0xFFFFF362,31),(0xFFFFF3FE,67)):
                frame=store_ai_value_fields(state,frame,address,value,16)
            for target,continuation in ((0xF574,0xF1B6),(0xF28E,0xF1BA),
                    (0xF2CE,0xF1BE),(0xF314,0xF1C2)):
                frame=_direct_stratagem_call_fields(state,frame,target,continuation)
        else:
            frame=_direct_stratagem_call_fields(state,frame,0xF34C,0xF1E2)
            frame=_direct_stratagem_call_fields(state,frame,0xF5F6,0xF1E6)
            for address,value in ((0xFFFFF3FE,68),(0xFFFFF362,40),(0x00FF7026,2)):
                frame=store_ai_value_fields(state,frame,address,value,16)
    frame=store_ai_value_fields(state,frame,0xFFFFF612,520,16)
    frame=_movement_move(state,frame,'target_x',66,16)
    frame=_movement_compare(state,frame,state.read(0xFFFFF3FE,2),206,16)
    target_address=0xFFFFF372 if frame.status&4 else 0xFFFFF3F2
    frame=store_ai_value_fields(state,frame,0xFFFFF3D2,state.read(target_address,2),16)
    frame=store_ai_value_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2),16)
    frame=_direct_stratagem_call_fields(state,frame,0x676F2,0xF22A)
    return store_ai_value_fields(state,frame,0xFFFFF608,120,16)


def penalize_actor_large_affinity_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F388: six-sample-plus-five deduction using the real signed BYTE lane."""
    frame=_movement_frame(state,frame)
    frame=_direct_stratagem_call_fields(state,frame,0x83D4,0xF38E)
    frame=_movement_move_long(state,frame,'target_x',low16(frame.target_x))
    frame=_stratagem_curve_fields(state,frame,6)
    frame=adjust_ai_carrier_fields(state,frame,'target_x',5)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A6,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC200).cursor())
    frame=_movement_move(state,frame,'unit',frame.roster.byte(low16(frame.target_y)),8)
    if frame.status&4:
        return frame
    frame=_stratagem_extend_byte_fields(state,frame,'unit')
    frame=_movement_multiply_word(state,frame,'unit',low16(frame.target_x))
    return _direct_stratagem_affinity_debit_fields(state,frame,0xF3B4)


def penalize_force_large_affinity_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F3C6: unlike F388, the original force penalty has no added five."""
    frame=_movement_frame(state,frame)
    frame=_direct_stratagem_call_fields(state,frame,0x83D4,0xF3CC)
    frame=_movement_move_long(state,frame,'target_x',low16(frame.target_x))
    frame=_stratagem_curve_fields(state,frame,6)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF376,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_y)),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC200).cursor())
    frame=_movement_move(state,frame,'unit',frame.roster.byte(low16(frame.target_y)),8)
    if frame.status&4:
        return frame
    frame=_stratagem_extend_byte_fields(state,frame,'unit')
    frame=_movement_multiply_word(state,frame,'unit',low16(frame.target_x))
    return _direct_stratagem_affinity_debit_fields(state,frame,0xF3F8)


def try_remove_secondary_target_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F574: actual trait low-three-bit gate and strict greater-than-fifty draw."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF372,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC700).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_x)),8)
    frame=_movement_move(state,frame,'target_x',low8(frame.target_x)&7,8)
    frame=_movement_compare(state,frame,low8(frame.target_x),3,8)
    if not frame.status&1:
        return frame
    frame=_direct_stratagem_call_fields(state,frame,0x83D4,0xF590)
    frame=_movement_move_long(state,frame,'target_x',low16(frame.target_x))
    frame=_stratagem_curve_fields(state,frame,100)
    frame=_movement_compare(state,frame,low16(frame.target_x),50,16)
    if not frame.status&5:
        frame=_direct_stratagem_call_fields(state,frame,0xF5B6,0xF5AE)
        frame=store_ai_value_fields(state,frame,0xFFFFF3FE,206,16)
    return frame


def remove_secondary_city_head_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F5B6: original assignment BYTE alias, mask3F and physical saved city WORD."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF372,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
    frame=store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_x)),255,8)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_y)&63,16)
    frame=_movement_move(state,frame,'unit',low16(frame.target_y),16)
    frame=_movement_fixed_shift_word(state,frame,'unit',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF45E).cursor())
    frame=_movement_compare(state,frame,low16(frame.target_x),frame.roster.word(low16(frame.unit)),16)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A8,2),16)
        frame=_stratagem_push_word_fields(state,frame,low16(frame.target_x))
        frame=store_ai_value_fields(state,frame,0xFFFFF630,65535,16)
        frame=_direct_stratagem_call_fields(state,frame,0x5F48,0xF5EE)
        frame=_stratagem_pop_word_fields(state,frame,'target_x')
        frame=_direct_stratagem_call_fields(state,frame,0xE1F6,0xF5F4)
    return frame


def choose_secondary_stratagem_target_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F630: choose strict lowest live status, preserving rereads and tie order."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A8,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF427).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_x)),8)
    frame=_stratagem_extend_byte_fields(state,frame,'target_x')
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
    frame=store_ai_value_fields(state,frame,0xFFFFF62E,frame.roster.word(low16(frame.target_x)),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF500).cursor())
    frame=_movement_move(state,frame,'unit',65535,16)
    frame=_movement_move(state,frame,'count',255,16)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFC300).cursor())
    while True:
        frame=_movement_move(state,frame,'target_x',frame.roster.word(),16)
        frame=first_replace(frame,roster=frame.roster.advance(2))
        if frame.status&8:
            break
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF3F2,2),16)
        if frame.status&4:
            continue
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF62E,2),16)
        if frame.status&4:
            continue
        frame=_movement_compare(state,frame,low8(frame.count),frame.candidates.byte(low16(frame.target_x)),8)
        if frame.status&5:
            continue
        frame=_movement_move(state,frame,'count',frame.candidates.byte(low16(frame.target_x)),8)
        frame=_movement_move(state,frame,'unit',low16(frame.target_x),16)
    frame=_movement_test(state,frame,low16(frame.unit),16)
    if frame.status&8:
        return _movement_move(state,frame,'target_x',1,16)
    frame=adjust_ai_carrier_fields(state,frame,'count',30)
    frame=_direct_stratagem_call_fields(state,frame,0x83D4,0xF688)
    frame=_movement_move_long(state,frame,'target_x',low16(frame.target_x))
    frame=_stratagem_curve_fields(state,frame,100)
    frame=_movement_compare(state,frame,low16(frame.target_x),low16(frame.count),16)
    if frame.status&5:
        return _movement_move(state,frame,'target_x',1,16)
    frame=_movement_move(state,frame,'target_x',0,16)
    return store_ai_value_fields(state,frame,0xFFFFF372,low16(frame.unit),16)


def method61_direct_probability_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F6AE: original retained DIVU, real RNG then the actual F61C seed reread."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF372,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFB400).cursor())
    frame=_movement_move(state,frame,'unit',frame.roster.word(low16(frame.target_x)),16)
    for address in (0xFFFFC000,0xFFFFB600):
        frame=first_replace(frame,roster=state.table_at(address).cursor())
        frame=adjust_ai_carrier_fields(state,frame,'unit',frame.roster.word(low16(frame.target_x)))
    frame=_direct_stratagem_call_fields(state,frame,0xF71C,0xF6D0)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3F2,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    for address in (0xFFFFB400,0xFFFFC000,0xFFFFB600):
        frame=first_replace(frame,roster=state.table_at(address).cursor())
        frame=adjust_ai_carrier_fields(state,frame,'target_x',frame.roster.word(low16(frame.target_y)))
    frame=_movement_multiply_word(state,frame,'unit',100)
    frame=_movement_divu_word(state,frame,'unit',low16(frame.target_x),0xF6F2)
    frame=_direct_stratagem_call_fields(state,frame,0x83D4,0xF6FA)
    frame=_stratagem_seed_sample_fields(state,frame)
    frame=_stratagem_curve_fields(state,frame,100)
    frame=_movement_compare(state,frame,low16(frame.target_x),low16(frame.unit),16)
    return _movement_move(state,frame,'target_x',1 if frame.status&5 else 0,16)


def method61_direct_factor_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F71C: saved numerator WORD and original role/difficulty DATA at DF3E (F766 PC+2-6186)."""
    frame=_movement_frame(state,frame)
    frame=_stratagem_push_word_fields(state,frame,low16(frame.unit))
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFEFD2,2),16)
    frame=_movement_fixed_shift_word(state,frame,'unit',1)
    frame=adjust_ai_carrier_fields(state,frame,'unit',state.read(0xFFFFEFD2,2))
    frame=_movement_fixed_shift_word(state,frame,'unit',3)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A8,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF427).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_x)),8)
    frame=_stratagem_extend_byte_fields(state,frame,'target_x')
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
    frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF3F2,2),16)
    if not frame.status&4:
        frame=adjust_ai_carrier_fields(state,frame,'unit',4)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A8,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_x',1)
        frame=first_replace(frame,roster=state.table_at(0xFFFFF45E).cursor())
        frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF3F2,2),16)
        if not frame.status&4:
            frame=adjust_ai_carrier_fields(state,frame,'unit',4)
    frame=_direct_stratagem_call_fields(state,frame,0x83D4,0xF766)
    frame=first_replace(frame,roster=state.table_at(0xDF3E).cursor())
    frame=_movement_multiply_word(state,frame,'target_x',frame.roster.word(low16(frame.unit)))
    frame=_economy_swap_fields(state,frame,'target_x')
    frame=adjust_ai_carrier_fields(state,frame,'target_x',frame.roster.word(low16(frame.unit),2))
    return _stratagem_pop_word_fields(state,frame,'unit')
