"""Complete Scene-frame neighbour policies, original32732..32936/33038.

The readable policy rules remain in business_policy.py. These owners add the
actual partial register lanes, flags, pointer residues and physical CALL stack
required by the same-Scene game chain. No simplified scalar result is promoted
to a fabricated complete frame; all live observations still use Scene RAM/DATA.
"""
from ..high_level_scene_flows.domain import SceneState, low8, low16, s16, u32
from ..high_level_battle_ai.contexts_first_deployment import (
    FirstDeploymentFrame, FirstDeploymentReturnBoundary, first_replace,
)
from ..high_level_main_flows.business_movement_support import (
    _movement_frame, _movement_move, _movement_move_long, _movement_test,
    _movement_compare, _movement_fixed_shift_word, _movement_arithmetic_long,
    _movement_bit, _path_carry_fields,
)
from .scene_fields import (
    store_ai_value_fields, compare_ai_long_fields, shift_ai_long_fields,
    step_ai_count_fields,
)


def _neighbor_policy_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Only six original CALL pairs; the outer3257E LONG is never fabricated."""
    if (target, continuation) not in (
            (0x32774,0x32736),(0x83D4,0x32752),(0x327CA,0x327BE),
            (0x32822,0x3280C),(0x83D4,0x3286E),(0x328D8,0x32872)):
        raise ValueError('actual neighbour-policy CALL/return pair required')
    frame=_movement_frame(state,frame)
    stack=frame.stack_cursor.advance(-4)
    stack.set_long(0,continuation)
    entered=first_replace(frame,stack_cursor=stack)
    if target==0x32774:
        returned=select_foreign_neighbor_attribute_max_fields(state,entered)
    elif target==0x327CA:
        returned=city_officer_attribute_max_fields(state,entered)
    elif target==0x32822:
        returned=neighbor_has_player_owner_fields(state,entered)
    elif target==0x328D8:
        returned=select_player_neighbor_resource_sum_fields(state,entered)
    else:
        from ..high_level_battle_ai.business_formation import first_deployment_random_fields
        from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
        returned=first_deployment_random_fields(BattlePolicyMemory(state),entered)
    returned=_movement_frame(state,returned)
    actual=returned.stack_cursor.long()
    if actual!=continuation:
        raise FirstDeploymentReturnBoundary(actual,returned,continuation)
    return first_replace(returned,stack_cursor=returned.stack_cursor.advance(4))


def _neighbor_policy_carry_fields(state: SceneState, frame: FirstDeploymentFrame,
        carry: bool) -> FirstDeploymentFrame:
    """Original3285A/32862 full-SR operations retain real privilege/trace gates."""
    if type(carry) is not bool:
        raise ValueError('actual neighbour carry outcome required')
    return _path_carry_fields(state,frame,1 if carry else 0,0x3285A if carry else 0x32862)


def choose_attribute_neighbor_action_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """32732: live foreign-neighbour maximum, real RNG and original3/5 policy."""
    frame=_movement_frame(state,frame)
    frame=_neighbor_policy_call_fields(state,frame,0x32774,0x32736)
    frame=_movement_test(state,frame,low16(frame.unit),16)
    if frame.status&8:
        return store_ai_value_fields(state,frame,0xFFFFF728,3,16)
    frame=_movement_move(state,frame,'count',5,16)
    frame=_movement_compare(state,frame,low16(frame.target_y),80,16)
    if frame.status&1:
        frame=_movement_move(state,frame,'count',3,16)
    frame=_neighbor_policy_call_fields(state,frame,0x83D4,0x32752)
    # ANDI.L #FFFF; LSL.L #3; SWAP. Full LONG/flags and upper residues matter.
    frame=_movement_move_long(state,frame,'target_x',low16(frame.target_x))
    frame=shift_ai_long_fields(state,frame,'target_x',3)
    frame=_movement_move_long(state,frame,'target_x',u32(frame.target_x<<16|frame.target_x>>16))
    frame=_movement_compare(state,frame,low16(frame.target_x),low16(frame.count),16)
    return store_ai_value_fields(state,frame,0xFFFFF728,5 if frame.status&1 else 3,16)


def select_foreign_neighbor_attribute_max_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """32774: strict maximum across live foreign/unprocessed neighbour cities."""
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(0xD4BDA).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',3)
    frame=first_replace(frame,roster=frame.roster.advance(s16(low16(frame.target_x))))
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'unit',0xFFFF,16)
    frame=_movement_move(state,frame,'count',state.read(0xFFFFF376,2),16)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFF427).cursor(),
        controller=state.table_at(0xFFFFB600).cursor(),scan=state.table_at(0xFFFFB400).cursor(),
        scratch=state.table_at(0xFFFFC300).cursor(),auxiliary=state.table_at(0xFFFFEA37).cursor())
    frame=_movement_move(state,frame,'target_x',0,16)
    while True:
        city=frame.roster.byte()
        frame=first_replace(frame,roster=frame.roster.advance(1))
        frame=_movement_move(state,frame,'target_x',city,8)
        if frame.status&8:
            return frame
        frame=_movement_compare(state,frame,low8(frame.count),frame.candidates.byte(low16(frame.target_x)),8)
        if frame.status&4:
            continue
        # The original independently rereads the owner BYTE after CMP.
        frame=_movement_test(state,frame,frame.candidates.byte(low16(frame.target_x)),8)
        if frame.status&8:
            continue
        frame=_movement_test(state,frame,frame.auxiliary.byte(low16(frame.target_x)),8)
        if not frame.status&4:
            continue
        frame=_neighbor_policy_call_fields(state,frame,0x327CA,0x327BE)
        frame=_movement_compare(state,frame,low16(frame.offset_x),low16(frame.target_y),16)
        if frame.status&5:
            continue
        frame=_movement_move(state,frame,'target_y',low16(frame.offset_x),16)
        frame=_movement_move(state,frame,'unit',low16(frame.target_x),16)


def city_officer_attribute_max_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """327CA: original256 predecrement assignments and two reread maxima."""
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,opponent=state.table_at(0xFFFFCD00).cursor())
    frame=_movement_move(state,frame,'offset_x',0,16)
    frame=_movement_move(state,frame,'offset_y',255,16)
    while True:
        frame=first_replace(frame,opponent=frame.opponent.advance(-1))
        frame=_movement_compare(state,frame,low8(frame.target_x),frame.opponent.byte(),8)
        if frame.status&4:
            frame=_movement_move(state,frame,'choice',frame.scratch.byte(low16(frame.offset_y)),8)
            frame=_movement_compare(state,frame,low8(frame.choice),95,8)
            if frame.status&5:
                frame=_movement_move(state,frame,'choice',low16(frame.offset_y),16)
                frame=_movement_fixed_shift_word(state,frame,'choice',1)
                frame=_movement_compare(state,frame,low16(frame.offset_x),frame.controller.word(low16(frame.choice)),16)
                if frame.status&1:
                    frame=_movement_move(state,frame,'offset_x',frame.controller.word(low16(frame.choice)),16)
                frame=_movement_compare(state,frame,low16(frame.offset_x),frame.scan.word(low16(frame.choice)),16)
                if frame.status&1:
                    frame=_movement_move(state,frame,'offset_x',frame.scan.word(low16(frame.choice)),16)
        # DBRA changes D6.W only. Its final FFFF and last compare flags survive.
        frame=step_ai_count_fields(frame,'offset_y')
        if low16(frame.offset_y)==0xFFFF:
            return frame


def choose_player_neighbor_action_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """32808: original player-owner carry gate chooses4 or8."""
    frame=_movement_frame(state,frame)
    frame=_neighbor_policy_call_fields(state,frame,0x32822,0x3280C)
    return store_ai_value_fields(state,frame,0xFFFFF728,4 if frame.status&1 else 8,16)


def neighbor_has_player_owner_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """32822: actual ordered three player BYTE comparisons and full-SR carry."""
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(0xD4BDA).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',3)
    frame=first_replace(frame,roster=frame.roster.advance(s16(low16(frame.target_x))),
        candidates=state.table_at(0xFFFFF427).cursor())
    frame=_movement_move(state,frame,'target_x',0,16)
    frame=_movement_move(state,frame,'target_y',0,16)
    while True:
        city=frame.roster.byte()
        frame=first_replace(frame,roster=frame.roster.advance(1))
        frame=_movement_move(state,frame,'target_x',city,8)
        if frame.status&8:
            return _neighbor_policy_carry_fields(state,frame,False)
        frame=_movement_move(state,frame,'target_y',frame.candidates.byte(low16(frame.target_x)),8)
        if frame.status&8:
            continue
        for address in (0xFFFFF67B,0xFFFFF67D,0xFFFFF67F):
            frame=_movement_compare(state,frame,low8(frame.target_y),state.read(address,1),8)
            if frame.status&4:
                return _neighbor_policy_carry_fields(state,frame,True)


def choose_resource_neighbor_action_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """32868: real RNG, wrapped neighbour funds and unchanged6/8 lottery."""
    frame=_movement_frame(state,frame)
    frame=_neighbor_policy_call_fields(state,frame,0x83D4,0x3286E)
    frame=_neighbor_policy_call_fields(state,frame,0x328D8,0x32872)
    frame=store_ai_value_fields(state,frame,0xFFFFF392,low16(frame.target_y),16)
    frame=compare_ai_long_fields(state,frame,frame.target_x,100000)
    if not frame.status&1:
        return store_ai_value_fields(state,frame,0xFFFFF728,6,16)
    frame=compare_ai_long_fields(state,frame,frame.target_x,50000)
    if not frame.status&1:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF61C,2),16)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&7,16)
        frame=_movement_compare(state,frame,low16(frame.target_x),5,16)
        return store_ai_value_fields(state,frame,0xFFFFF728,6 if frame.status&1 else 8,16)
    frame=compare_ai_long_fields(state,frame,frame.target_x,10000)
    if not frame.status&1:
        frame=_movement_bit(state,frame,state.read(0xFFFFF61D,1),0)
        return store_ai_value_fields(state,frame,0xFFFFF728,8 if frame.status&4 else 6,16)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF61C,2),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&7,16)
    frame=_movement_compare(state,frame,low16(frame.target_x),2,16)
    return store_ai_value_fields(state,frame,0xFFFFF728,6 if frame.status&1 else 8,16)


def select_player_neighbor_resource_sum_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """328D8: original strict wrapped sum; retain BUG-013's D1 third comparison."""
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(0xD4BDA).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',3)
    frame=first_replace(frame,roster=frame.roster.advance(s16(low16(frame.target_x))))
    frame=_movement_move_long(state,frame,'target_x',0)
    frame=_movement_move(state,frame,'target_y',0xFFFF,16)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=_movement_move(state,frame,'count',0,16)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFF427).cursor(),
        controller=state.table_at(0xFFFFDFFC).cursor(),scan=state.table_at(0xFFFFE09C).cursor())
    while True:
        city=frame.roster.byte()
        frame=first_replace(frame,roster=frame.roster.advance(1))
        frame=_movement_move(state,frame,'unit',city,8)
        if frame.status&8:
            return frame
        frame=_movement_move(state,frame,'count',frame.candidates.byte(low16(frame.unit)),8)
        if frame.status&8:
            continue
        frame=_movement_compare(state,frame,low8(frame.count),state.read(0xFFFFF67B,1),8)
        eligible=bool(frame.status&4)
        if not eligible:
            frame=_movement_compare(state,frame,low8(frame.count),state.read(0xFFFFF67D,1),8)
            eligible=bool(frame.status&4)
        if not eligible:
            # Original32918 compares D1.B (previous selected city), not D3.B.
            frame=_movement_compare(state,frame,low8(frame.target_y),state.read(0xFFFFF67F,1),8)
            eligible=bool(frame.status&4)
        if not eligible:
            continue
        frame=_movement_fixed_shift_word(state,frame,'unit',2)
        frame=_movement_move_long(state,frame,'distance',frame.controller.long(low16(frame.unit)))
        frame=_movement_arithmetic_long(state,frame,'distance',frame.scan.long(low16(frame.unit)))
        frame=compare_ai_long_fields(state,frame,frame.distance,frame.target_x)
        if frame.status&5:
            # Original BLS jumps before the LSR. Keep scaled D2.W on rejection.
            continue
        frame=_movement_move_long(state,frame,'target_x',frame.distance)
        frame=_movement_fixed_shift_word(state,frame,'unit',2,True)
        frame=_movement_move(state,frame,'target_y',low16(frame.unit),16)


def clear_economy_command_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33038: actual MOVE.W #FFFF,F728; retain every D/A carrier and X."""
    frame=_movement_frame(state,frame)
    return store_ai_value_fields(state,frame,0xFFFFF728,0xFFFF,16)
