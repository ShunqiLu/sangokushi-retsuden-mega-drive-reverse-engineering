"""Whole Scene-frame method61 resource attempt and its finite real closure.

Existing stratagem policies remain the readable logical reference. These named
owners retain every actual LONG carrier, partial register lane, RAM reread,
arithmetic flag and original CALL/WORD/MOVEM stack slot. Original aliases are
preserved; there is no invented CPU, scalar-to-frame promotion or host outcome.
"""
from ..high_level_scene_flows.domain import (
    SceneState, low8, low16, s8, u16, divu_retained,
)
from ..high_level_battle_ai.contexts_first_deployment import (
    FirstDeploymentFrame, FirstDeploymentReturnBoundary, first_replace,
)
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
from ..high_level_main_flows.business_movement_support import (
    _movement_frame, _movement_move, _movement_move_long, _movement_test,
    _movement_compare, _movement_fixed_shift_word, _movement_multiply_word,
    _movement_binary_flags, _movement_save_longs, _movement_restore_longs,
)
from ..high_level_ai_decision.scene_fields import (
    store_ai_value_fields, adjust_ai_carrier_fields, compare_ai_long_fields,
    step_ai_count_fields,
)
from ..high_level_remaining_flows.business_lowbank import (
    _economy_long_shift_fields, _economy_swap_fields,
)


REAL_CALL_PAIRS=(
    (0x83D4,0xF08E),(0xF232,0xF0CE),(0x83D4,0xF0FA),
    (0xF28E,0xF116),(0xF2CE,0xF11A),(0xF314,0xF11E),
    (0xF34C,0xF136),(0xF5F6,0xF13A),(0x676F2,0xF186),
    (0x83D4,0xF27C),(0x83D4,0xF294),(0x83D4,0xF2D4),
    (0x83D4,0xF31A),(0xFDEA,0xF354),(0xF40A,0xF35E),
    (0xF4E6,0xF378),(0x83D4,0xF5FC),(0xE38E,0xF478),
    (0x83D4,0xF480),(0xF50C,0xF4AE),(0x83D4,0xF4B6),
    (0xE29E,0xF4E4),(0x5F48,0xF506),(0xE1F6,0xF50A),
    (0x5F48,0xF52E),(0x83D4,0xF53A),(0xE38E,0xE2C4),
    (0xE3E2,0xE2C8),(0x5F48,0xE2F8),(0xE1F6,0xE2FC),
)


def _stratagem_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Exactly30 original CALL sites, including PC-relativeF4E0→E29E/F4E4."""
    if (target,continuation) not in REAL_CALL_PAIRS:
        raise ValueError('actual finite method61 CALL/return pair required')
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
        # Only actual internal entry identities; no generic game/PC dispatcher.
        owners={0xF232:method61_scenario_factor_fields,
            0xF28E:penalize_actor_small_affinity_fields,
            0xF2CE:penalize_force_small_affinity_fields,
            0xF314:reward_actor_small_c_progress_fields,
            0xF34C:remove_stratagem_target_fields,
            0xF5F6:reward_actor_large_c_progress_fields,
            0xFDEA:owner_head_lookup_fields,0xF40A:settle_removed_force_head_fields,
            0xF4E6:remove_city_head_target_fields,0xF50C:reassign_or_mark_target_fields,
            0xE29E:replace_removed_force_head_fields,
            0xE38E:mark_removed_force_assignments_fields,
            0xE3E2:clear_removed_force_roster_alias_fields}
        returned=owners[target](state,entered)
    returned=_movement_frame(state,returned)
    actual=returned.stack_cursor.long()
    if actual!=continuation:
        raise FirstDeploymentReturnBoundary(actual,returned,continuation)
    return first_replace(returned,stack_cursor=returned.stack_cursor.advance(4))


def _stratagem_curve_fields(state: SceneState, frame: FirstDeploymentFrame,
        multiplier: int) -> FirstDeploymentFrame:
    """The six original finite arithmetic curves over actual D0/D1, not RNG.

    Each factor is assembled with the existing width/flag primitives in the
    original shift/add order. This helper reads no seed and chooses no outcome.
    """
    profiles={21:((2,True),(2,True)),11:((2,True),(1,True)),
        6:((1,True),(1,False)),3:((1,True),),
        10:((2,True),(1,False)),100:((1,True),(3,True),(2,False))}
    if multiplier not in profiles:
        raise ValueError('actual method61 sample curve required')
    frame=_movement_move_long(state,frame,'target_y',frame.target_x)
    for amount,add_original in profiles[multiplier]:
        frame=_economy_long_shift_fields(state,frame,'target_x',amount)
        if add_original:
            frame=adjust_ai_carrier_fields(state,frame,'target_x',frame.target_y,32)
    return _economy_swap_fields(state,frame,'target_x')


def _stratagem_seed_sample_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original MOVEQ0 followed by the real current seed WORD read."""
    frame=_movement_move_long(state,frame,'target_x',0)
    return _movement_move(state,frame,'target_x',state.read(0xFFFFF61C,2),16)


def _stratagem_extend_byte_fields(state: SceneState, frame: FirstDeploymentFrame,
        carrier: str) -> FirstDeploymentFrame:
    return _movement_move(state,frame,carrier,u16(s8(low8(frame.carrier(carrier)))),16)


def _stratagem_push_word_fields(state: SceneState, frame: FirstDeploymentFrame,
        value: int) -> FirstDeploymentFrame:
    stack=frame.stack_cursor.advance(-2)
    frame=store_ai_value_fields(state,frame,stack.base,value,16)
    return first_replace(frame,stack_cursor=stack)


def _stratagem_pop_word_fields(state: SceneState, frame: FirstDeploymentFrame,
        carrier: str) -> FirstDeploymentFrame:
    value=frame.stack_cursor.word()
    frame=first_replace(frame,stack_cursor=frame.stack_cursor.advance(2))
    return _movement_move(state,frame,carrier,value,16)


def _stratagem_memory_byte_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, value: int, subtract: bool=False) -> FirstDeploymentFrame:
    """Actual BYTE ADDQ/SUB read-modify-write, retaining arithmetic flags."""
    frame,changed=_movement_binary_flags(state,frame,state.read(address,1),value,8,subtract)
    state.write(address,1,changed)
    return frame


def _stratagem_divide_compare_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """OriginalF0EC DIVU immediately followed byF0EE CMP; no hidden flag guess.

    CMP replaces every DIVU NZVC result, including undefined overflow NZ. X is
    unchanged by both. Overflow retains the original dividend; zero remains the
    real arithmetic boundary with all preceding DATA and CALL slots preserved.
    """
    divisor=low16(frame.target_x)
    if divisor==0:
        raise MovementContinuationBoundary(0xF0EC,frame,'original DIVU zero divisor requires its exception owner')
    frame=first_replace(frame,unit=divu_retained(frame.unit,divisor))
    return _movement_compare(state,frame,low16(frame.unit),100,16)


def _stratagem_affinity_debit_fields(state: SceneState,
        frame: FirstDeploymentFrame, instruction: int) -> FirstDeploymentFrame:
    """F2BC/F302 DIVU100 and following BYTE debit form one known-flag effect.

    The debit overwrites all arithmetic flags before its BCC. No undefined DIVU
    intermediate flags are invented or externally returned.
    """
    if instruction not in (0xF2BC,0xF302):
        raise ValueError('actual method61 affinity division site required')
    frame=first_replace(frame,unit=divu_retained(frame.unit,100))
    address=frame.roster.address(low16(frame.target_y))
    frame=_stratagem_memory_byte_fields(state,frame,address,low8(frame.unit),True)
    if frame.status&1:
        frame=store_ai_value_fields(state,frame,address,0,8,True)
    return frame


def settle_method61_resource_attempt_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F088: complete cost, lottery, failure/success and visible-force message."""
    frame=_movement_frame(state,frame)
    frame=_stratagem_call_fields(state,frame,0x83D4,0xF08E)
    frame=_movement_move_long(state,frame,'target_x',low16(frame.target_x))
    frame=_stratagem_curve_fields(state,frame,21)
    frame=adjust_ai_carrier_fields(state,frame,'target_x',20)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A6,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFB600).cursor())
    frame=_movement_move(state,frame,'unit',frame.roster.word(low16(frame.target_y)),16)
    frame=_movement_multiply_word(state,frame,'unit',low16(frame.target_x))
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',2)
    frame=first_replace(frame,roster=state.table_at(0xFFFFDFFC).cursor())
    frame=_movement_move_long(state,frame,'target_y',frame.roster.long(low16(frame.target_x)))
    frame=adjust_ai_carrier_fields(state,frame,'target_y',frame.unit,32,True)
    success=False
    if not frame.status&1:
        frame=store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_x)),frame.target_y,32)
        frame=_stratagem_call_fields(state,frame,0xF232,0xF0CE)
        frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3F2,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_y',1)
        for address in (0xFFFFB400,0xFFFFC000,0xFFFFB600):
            frame=first_replace(frame,roster=state.table_at(address).cursor())
            frame=adjust_ai_carrier_fields(state,frame,'target_x',frame.roster.word(low16(frame.target_y)))
        frame=_stratagem_divide_compare_fields(state,frame)
        success=not bool(frame.status&1)
        if not success:
            frame=_stratagem_call_fields(state,frame,0x83D4,0xF0FA)
            frame=_stratagem_seed_sample_fields(state,frame)
            frame=_stratagem_curve_fields(state,frame,100)
            frame=_movement_compare(state,frame,low16(frame.target_x),low16(frame.unit),16)
            success=bool(frame.status&5)
    if not success:
        for target,continuation in ((0xF28E,0xF116),(0xF2CE,0xF11A),(0xF314,0xF11E)):
            frame=_stratagem_call_fields(state,frame,target,continuation)
        for address,value in ((0xFFFFF3FE,67),(0xFFFFF362,31),(0xFFFFF608,120)):
            frame=store_ai_value_fields(state,frame,address,value,16)
    else:
        frame=_stratagem_call_fields(state,frame,0xF34C,0xF136)
        frame=_stratagem_call_fields(state,frame,0xF5F6,0xF13A)
        for address,value in ((0xFFFFF3FE,68),(0x00FF7026,2),(0xFFFFF362,40)):
            frame=store_ai_value_fields(state,frame,address,value,16)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
    visible=False
    for address in (0xFFFFF67A,0xFFFFF67C,0xFFFFF67E):
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(address,2),16)
        if frame.status&4:
            visible=True
            break
    if visible:
        frame=store_ai_value_fields(state,frame,0xFFFFF612,520,16)
        frame=_movement_move(state,frame,'target_x',65,16)
        frame=store_ai_value_fields(state,frame,0xFFFFF3D2,state.read(0xFFFFF3F2,2),16)
        frame=store_ai_value_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2),16)
        frame=_stratagem_call_fields(state,frame,0x676F2,0xF186)
        frame=store_ai_value_fields(state,frame,0xFFFFF608,120,16)
    return frame


def method61_scenario_factor_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F232: original saved cost WORD and role/difficulty factor tableDF1A."""
    frame=_movement_frame(state,frame)
    frame=_stratagem_push_word_fields(state,frame,low16(frame.unit))
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFEFD2,2),16)
    frame=_movement_fixed_shift_word(state,frame,'unit',1)
    frame=adjust_ai_carrier_fields(state,frame,'unit',state.read(0xFFFFEFD2,2))
    frame=_movement_fixed_shift_word(state,frame,'unit',4)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF427).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
    frame=_stratagem_extend_byte_fields(state,frame,'target_y')
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_y)),16)
    frame=_movement_compare(state,frame,low16(frame.target_y),state.read(0xFFFFF3A6,2),16)
    if not frame.status&4:
        frame=adjust_ai_carrier_fields(state,frame,'unit',4)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_x',1)
        frame=first_replace(frame,roster=state.table_at(0xFFFFF45E).cursor())
        frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF3A6,2),16)
        if not frame.status&4:
            frame=adjust_ai_carrier_fields(state,frame,'unit',4)
    frame=_stratagem_call_fields(state,frame,0x83D4,0xF27C)
    # PC-relative LEA F27E-4964 is the actual independently owned DATA DF1A.
    frame=first_replace(frame,roster=state.table_at(0xDF1A).cursor())
    frame=_movement_multiply_word(state,frame,'target_x',frame.roster.word(low16(frame.unit)))
    frame=_economy_swap_fields(state,frame,'target_x')
    frame=adjust_ai_carrier_fields(state,frame,'target_x',frame.roster.word(low16(frame.unit),2))
    return _stratagem_pop_word_fields(state,frame,'unit')


def penalize_actor_small_affinity_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F28E: actual eleven-sample factor and signed-BYTE affinity debit."""
    frame=_movement_frame(state,frame)
    frame=_stratagem_call_fields(state,frame,0x83D4,0xF294)
    frame=_movement_move_long(state,frame,'target_x',low16(frame.target_x))
    frame=_stratagem_curve_fields(state,frame,11)
    frame=adjust_ai_carrier_fields(state,frame,'target_x',10)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A6,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC200).cursor())
    frame=_movement_move(state,frame,'unit',frame.roster.byte(low16(frame.target_y)),8)
    if frame.status&4:
        return frame
    frame=_stratagem_extend_byte_fields(state,frame,'unit')
    frame=_movement_multiply_word(state,frame,'unit',low16(frame.target_x))
    return _stratagem_affinity_debit_fields(state,frame,0xF2BC)


def penalize_force_small_affinity_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F2CE: current force head and original six-sample affinity deduction."""
    frame=_movement_frame(state,frame)
    frame=_stratagem_call_fields(state,frame,0x83D4,0xF2D4)
    frame=_movement_move_long(state,frame,'target_x',low16(frame.target_x))
    frame=_stratagem_curve_fields(state,frame,6)
    frame=adjust_ai_carrier_fields(state,frame,'target_x',5)
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
    return _stratagem_affinity_debit_fields(state,frame,0xF302)


def _stratagem_credit_c_progress_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Shared original C000 WORD credit/cap suffix; no new CALL slot."""
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A6,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC000).cursor())
    frame=_movement_move(state,frame,'unit',frame.roster.word(low16(frame.target_y)),16)
    frame=adjust_ai_carrier_fields(state,frame,'unit',low16(frame.target_x))
    frame=_movement_compare(state,frame,low16(frame.unit),999,16)
    if not frame.status&5:
        frame=_movement_move(state,frame,'unit',999,16)
    return store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_y)),low16(frame.unit),16)


def reward_actor_small_c_progress_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F314: real RNG, original three-sample gain and wrapped WORD cap."""
    frame=_movement_frame(state,frame)
    frame=_stratagem_call_fields(state,frame,0x83D4,0xF31A)
    frame=_movement_move_long(state,frame,'target_x',low16(frame.target_x))
    frame=_stratagem_curve_fields(state,frame,3)
    frame=adjust_ai_carrier_fields(state,frame,'target_x',1)
    return _stratagem_credit_c_progress_fields(state,frame)


def reward_actor_large_c_progress_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F5F6: real RNG then reread seed, ten-sample gain and original cap."""
    frame=_movement_frame(state,frame)
    frame=_stratagem_call_fields(state,frame,0x83D4,0xF5FC)
    frame=_stratagem_seed_sample_fields(state,frame)
    frame=_stratagem_curve_fields(state,frame,10)
    frame=adjust_ai_carrier_fields(state,frame,'target_x',10)
    return _stratagem_credit_c_progress_fields(state,frame)


def owner_head_lookup_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """FDEA: real signed owner-head lookup also publishes F612=0201."""
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF427).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_x)),8)
    frame=_stratagem_extend_byte_fields(state,frame,'target_x')
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
    return store_ai_value_fields(state,frame,0xFFFFF612,513,16)


def remove_stratagem_target_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F34C: distinguish actual force head, city head and ordinary target."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A8,2),16)
    frame=_stratagem_call_fields(state,frame,0xFDEA,0xF354)
    frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF3F2,2),16)
    if frame.status&4:
        frame=_stratagem_call_fields(state,frame,0xF40A,0xF35E)
    else:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A8,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_x',1)
        frame=first_replace(frame,roster=state.table_at(0xFFFFF45E).cursor())
        frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF3F2,2),16)
        if frame.status&4:
            frame=_stratagem_call_fields(state,frame,0xF4E6,0xF378)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3F2,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
    return store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_x)),255,8)


def settle_removed_force_head_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F40A: original secondary-trait branches, aliases and real E29E call."""
    frame=_movement_frame(state,frame)
    frame=_movement_test(state,frame,state.read(0xFFFFF64A,2),16)
    if not frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF372,2),16)
        frame=first_replace(frame,roster=state.table_at(0xFFFFC700).cursor())
        frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_x)),8)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&15,16)
        zero_trait=bool(frame.status&4)
        if not zero_trait:
            frame=_movement_compare(state,frame,low8(frame.target_x),2,8)
            if not frame.status&5:
                frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A8,2),16)
                frame=first_replace(frame,roster=state.table_at(0xFFFFF427).cursor())
                frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
                frame=_stratagem_extend_byte_fields(state,frame,'target_y')
                frame=_movement_fixed_shift_word(state,frame,'target_y',1)
                frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
                frame=store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_y)),state.read(0xFFFFF372,2),16)
                frame=_movement_fixed_shift_word(state,frame,'target_x',1)
                frame=first_replace(frame,roster=state.table_at(0xFFFFF45E).cursor())
                frame=store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_x)),state.read(0xFFFFF372,2),16)
                frame=_movement_fixed_shift_word(state,frame,'target_y',1,True)
                # F454 deliberately retains A0=F45E; it is not the F590 counter.
                frame=_stratagem_memory_byte_fields(state,frame,frame.roster.address(low16(frame.target_y)),1)
                frame=_movement_compare(state,frame,frame.roster.word(low16(frame.target_y)),4,16)
                if not frame.status&4:
                    return frame
                frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
                frame=_movement_fixed_shift_word(state,frame,'target_y',1)
                frame=store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_y)),0xFFFF,16)
                frame=_movement_fixed_shift_word(state,frame,'target_y',1,True)
                frame=store_ai_value_fields(state,frame,0xFFFFF64C,low16(frame.target_y),16)
                return _stratagem_call_fields(state,frame,0xE38E,0xF478)
        frame=_stratagem_call_fields(state,frame,0x83D4,0xF480 if zero_trait else 0xF4B6)
        frame=_stratagem_seed_sample_fields(state,frame)
        frame=_stratagem_curve_fields(state,frame,100)
        frame=_movement_compare(state,frame,low16(frame.target_x),70 if zero_trait else 30,16)
        if not frame.status&5:
            frame=_stratagem_call_fields(state,frame,0xF50C,0xF4AE)
        else:
            frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF372,2),16)
            frame=first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
            frame=store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_x)),255,8)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A8,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF427).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_x)),8)
    frame=_stratagem_extend_byte_fields(state,frame,'target_x')
    return _stratagem_call_fields(state,frame,0xE29E,0xF4E4)


def remove_city_head_target_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F4E6: remove target's live assignment, build actual roster and choose head."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3F2,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_y)),8)
    frame=store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_y)),255,8)
    frame=_stratagem_extend_byte_fields(state,frame,'target_x')
    frame=store_ai_value_fields(state,frame,0xFFFFF630,0xFFFF,16)
    frame=_stratagem_call_fields(state,frame,0x5F48,0xF506)
    return _stratagem_call_fields(state,frame,0xE1F6,0xF50A)


def reassign_or_mark_target_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F50C: keep F630 lookup alias and F392 high-BYTE reassignment source."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_x)),8)
    frame=_stratagem_extend_byte_fields(state,frame,'target_x')
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF630).cursor())
    frame=store_ai_value_fields(state,frame,0xFFFFF630,frame.roster.word(low16(frame.target_y)),16)
    frame=_stratagem_call_fields(state,frame,0x5F48,0xF52E)
    frame=_movement_compare(state,frame,low16(frame.count),10,16)
    assign=False
    if frame.status&1:
        frame=_stratagem_call_fields(state,frame,0x83D4,0xF53A)
        frame=_stratagem_seed_sample_fields(state,frame)
        frame=_stratagem_curve_fields(state,frame,100)
        frame=_movement_compare(state,frame,low16(frame.target_x),30,16)
        assign=bool(frame.status&5)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF372,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
    address=frame.roster.address(low16(frame.target_x))
    if assign:
        return store_ai_value_fields(state,frame,address,state.read(0xFFFFF392,1),8)
    return store_ai_value_fields(state,frame,address,state.read(address,1)|128,8)


def replace_removed_force_head_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """E29E: live leader replacement and exact force-roster scanning residues."""
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF590).cursor())
    address=frame.roster.address(low16(frame.target_x))
    frame=_stratagem_memory_byte_fields(state,frame,address,1)
    frame=_movement_compare(state,frame,state.read(address,1),4,8)
    if not frame.status&5:
        frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
        frame=_movement_fixed_shift_word(state,frame,'target_y',1)
        frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
        frame=store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_y)),0xFFFF,16)
        frame=store_ai_value_fields(state,frame,0xFFFFF64C,low16(frame.target_x),16)
        frame=_stratagem_call_fields(state,frame,0xE38E,0xE2C4)
        return _stratagem_call_fields(state,frame,0xE3E2,0xE2C8)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'unit',frame.roster.word(low16(frame.target_y)),16)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFCC00).cursor())
    frame=_movement_move(state,frame,'count',frame.candidates.byte(low16(frame.unit)),8)
    frame=store_ai_value_fields(state,frame,frame.candidates.address(low16(frame.unit)),255,8)
    frame=_stratagem_push_word_fields(state,frame,low16(frame.target_x))
    frame=_stratagem_extend_byte_fields(state,frame,'count')
    frame=_movement_move(state,frame,'target_x',low16(frame.count),16)
    frame=store_ai_value_fields(state,frame,0xFFFFF630,0xFFFF,16)
    frame=_stratagem_call_fields(state,frame,0x5F48,0xE2F8)
    frame=_stratagem_call_fields(state,frame,0xE1F6,0xE2FC)
    frame=_stratagem_pop_word_fields(state,frame,'target_x')
    frame=first_replace(frame,roster=state.table_at(0xFFFFF450).cursor(),
        candidates=state.table_at(0xFFFFF5A0).cursor())
    frame=_movement_move(state,frame,'target_y',39,16)
    while True:
        frame=first_replace(frame,roster=frame.roster.advance(-1))
        frame=_movement_compare(state,frame,low8(frame.target_x),frame.roster.byte(),8)
        if frame.status&4:
            frame=store_ai_value_fields(state,frame,frame.candidates.base,low8(frame.target_y),8)
            frame=first_replace(frame,candidates=frame.candidates.advance(1))
        frame=step_ai_count_fields(frame,'target_y')
        if low16(frame.target_y)==0xFFFF:
            break
    frame=store_ai_value_fields(state,frame,frame.candidates.base,255,8)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCD00).cursor())
    frame=_movement_move(state,frame,'target_y',255,16)
    frame=_movement_move_long(state,frame,'offset_x',0)
    # Original leaves D4 unchanged if no strict positive candidate is found.
    while True:
        frame=first_replace(frame,candidates=state.table_at(0xFFFFF5A0).cursor(),
            roster=frame.roster.advance(-1))
        frame=_movement_move(state,frame,'unit',frame.roster.byte(),8)
        eligible=not bool(frame.status&12)
        if eligible:
            frame=adjust_ai_carrier_fields(state,frame,'unit',1,8,True)
            eligible=False
            while True:
                city=frame.candidates.byte()
                frame=first_replace(frame,candidates=frame.candidates.advance(1))
                frame=_movement_move(state,frame,'count',city,8)
                if frame.status&8:
                    break
                frame=_movement_compare(state,frame,low8(frame.count),low8(frame.unit),8)
                if frame.status&4:
                    eligible=True
                    break
                if frame.status&1:
                    break
        if eligible:
            frame=_movement_move(state,frame,'offset_y',low16(frame.target_y),16)
            frame=_movement_fixed_shift_word(state,frame,'offset_y',1)
            frame=first_replace(frame,controller=state.table_at(0xFFFFC000).cursor())
            frame=_movement_move_long(state,frame,'choice',0)
            frame=_movement_move(state,frame,'choice',frame.controller.word(low16(frame.offset_y)),16)
            frame=first_replace(frame,controller=state.table_at(0xFFFFBE00).cursor())
            frame=adjust_ai_carrier_fields(state,frame,'choice',frame.controller.word(low16(frame.offset_y)))
            if frame.status&1:
                frame=adjust_ai_carrier_fields(state,frame,'choice',0x10000,32)
            frame=compare_ai_long_fields(state,frame,frame.choice,frame.offset_x)
            if not frame.status&5:
                frame=_movement_move_long(state,frame,'offset_x',frame.choice)
                frame=_movement_move(state,frame,'distance',low16(frame.target_y),16)
        frame=step_ai_count_fields(frame,'target_y')
        if low16(frame.target_y)==0xFFFF:
            break
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
    frame=store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_y)),low16(frame.distance),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.distance)),8)
    frame=_stratagem_extend_byte_fields(state,frame,'target_y')
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF45E).cursor())
    frame=store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_y)),low16(frame.distance),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC300).cursor())
    return store_ai_value_fields(state,frame,frame.roster.address(low16(frame.distance)),0,8,True)


def mark_removed_force_assignments_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """E38E: real five-LONG MOVEM, next-BYTE OR alias and double pointer step."""
    frame=_movement_frame(state,frame)
    saved=('target_x','target_y','unit','roster','candidates')
    frame=_movement_save_longs(state,frame,saved)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF64C,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF450).cursor(),
        candidates=state.table_at(0xFFFFF5A0).cursor())
    frame=_movement_move(state,frame,'target_y',39,16)
    while True:
        frame=first_replace(frame,roster=frame.roster.advance(-1))
        frame=_movement_compare(state,frame,low8(frame.target_x),frame.roster.byte(),8)
        if frame.status&4:
            frame=store_ai_value_fields(state,frame,frame.candidates.base,low8(frame.target_y),8)
            frame=first_replace(frame,candidates=frame.candidates.advance(1))
        frame=step_ai_count_fields(frame,'target_y')
        if low16(frame.target_y)==0xFFFF:
            break
    frame=store_ai_value_fields(state,frame,frame.candidates.base,255,8)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
    frame=_movement_move(state,frame,'target_x',255,16)
    while True:
        frame=first_replace(frame,candidates=state.table_at(0xFFFFF5A0).cursor())
        assignment=frame.roster.byte()
        frame=first_replace(frame,roster=frame.roster.advance(1))
        frame=_movement_move(state,frame,'unit',assignment,8)
        if not frame.status&12:
            frame=adjust_ai_carrier_fields(state,frame,'unit',1,8,True)
            while True:
                city=frame.candidates.byte()
                frame=first_replace(frame,candidates=frame.candidates.advance(1))
                frame=_movement_move(state,frame,'target_y',city,8)
                if frame.status&8:
                    break
                frame=_movement_compare(state,frame,low8(frame.target_y),low8(frame.unit),8)
                if frame.status&4:
                    frame=store_ai_value_fields(state,frame,frame.roster.base,frame.roster.byte()|128,8)
                    break
                if frame.status&1:
                    break
        # Original ADDA.W1 occurs in addition to the actual (A0)+ above.
        frame=first_replace(frame,roster=frame.roster.advance(1))
        frame=step_ai_count_fields(frame,'target_x')
        if low16(frame.target_x)==0xFFFF:
            return _movement_restore_longs(state,frame,saved)


def clear_removed_force_roster_alias_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """E3E2: live postincrement F5A0 alias, not the unused CC00 A1 view."""
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF5A0).cursor(),
        candidates=state.table_at(0xFFFFCC00).cursor())
    frame=_movement_move(state,frame,'target_x',0,16)
    while True:
        city=frame.roster.byte()
        frame=first_replace(frame,roster=frame.roster.advance(1))
        frame=_movement_move(state,frame,'target_x',city,8)
        if frame.status&8:
            return frame
        frame=store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_x)),0,8,True)
