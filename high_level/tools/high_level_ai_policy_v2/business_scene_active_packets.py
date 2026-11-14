"""Complete live third-directory policies for the original active map packet.

confirmed: editable nested_dispatch_descendants.s34F94..353FC. Selection,
partial carriers, odd-looking original scans and real CALL slots are retained;
the old scalar projections are not used as full-frame oracles.
"""
from ..high_level_scene_flows.domain import SceneState, low8, low16, s16, u16
from ..high_level_battle_ai.contexts_first_deployment import (
    FirstDeploymentFrame, FirstDeploymentReturnBoundary, first_replace,
)
from ..high_level_main_flows.business_movement_support import (
    _movement_frame, _movement_move, _movement_move_long, _movement_test,
    _movement_compare, _movement_fixed_shift_word, _path_carry_fields,
)
from ..high_level_ai_decision.scene_fields import (
    store_ai_value_fields, adjust_ai_carrier_fields, compare_ai_long_fields,
    test_ai_register_bit_fields, step_ai_count_fields,
)
from ..high_level_remaining_flows.business_lowbank import _economy_swap_fields


REAL_CALL_PAIRS = (
    (0x34FAE, 0x34F98), (0x3508A, 0x35068), (0x350B2, 0x3506C),
    (0x83D4, 0x35110), (0x35172, 0x35158), (0x351CA, 0x351A6),
    (0x351E4, 0x351B4), (0x352A4, 0x3528A),
    (0x35366, 0x35346), (0x35380, 0x3534A),
)


def _active_packet_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Only ten original nested calls; caller owns the physical LONG and RTS."""
    if (target, continuation) not in REAL_CALL_PAIRS:
        raise ValueError('actual active-packet policy CALL pair required')
    frame = _movement_frame(state, frame)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    state.sr = state.sr & 65504 | entered.status
    children = {
        0x34FAE: active_packet_terrain_contact_fields,
        0x3508A: project_selected_roster_strength_fields,
        0x350B2: measure_self_assigned_officers_fields,
        0x35172: linked_city_force_fields,
        0x351CA: selected_roster_strength_fields,
        0x351E4: selected_roster_troop_shortfall_fields,
        0x352A4: collect_active_adjacent_groups_fields,
        0x35366: selected_roster_comparison_strength_fields,
        0x35380: measure_lightest_active_candidate_fields,
    }
    if target == 0x83D4:
        from ..high_level_battle_ai.business_formation import first_deployment_random_fields
        from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
        result = first_deployment_random_fields(BattlePolicyMemory(state), entered)
    else:
        result = children[target](state, entered)
    result = _movement_frame(state, result)
    state.sr = state.sr & 65504 | result.status
    returned = result.stack_cursor.long()
    if returned != continuation:
        raise FirstDeploymentReturnBoundary(returned, result, continuation)
    return first_replace(result, stack_cursor=result.stack_cursor.advance(4))


def choose_active_packet_contact_action_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34F94: original terrain-contact carry selects command3 or8."""
    frame = _movement_frame(state, frame)
    frame = _active_packet_call_fields(state, frame, 0x34FAE, 0x34F98)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 3 if frame.status & 1 else 8, 16)


def active_packet_terrain_contact_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34FAE: ordered four terrain reads, original40-city window and owner test."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(state.read(0x00FF382C, 4)).cursor())
    for carrier, offset in (('target_x', 1), ('target_y', 2)):
        frame = _movement_move(state, frame, carrier, 0, 16)
        frame = _movement_move(state, frame, carrier, frame.roster.byte(0, offset), 8)
    frame = _movement_move(state, frame, 'unit', low16(frame.target_x), 16)
    frame = _movement_fixed_shift_word(state, frame, 'unit', 3)
    frame = adjust_ai_carrier_fields(state, frame, 'unit', low16(frame.target_x))
    frame = _movement_fixed_shift_word(state, frame, 'unit', 3)
    frame = adjust_ai_carrier_fields(state, frame, 'unit', low16(frame.target_y))
    frame = first_replace(frame, candidates=state.table_at(0xEE5F0).cursor().advance(s16(low16(frame.unit))))
    for displacement in (-72, -1, 1, 72):
        frame = _movement_compare(state, frame, frame.candidates.byte(0, displacement), 1, 8)
        if frame.status & 4:
            break
    else:
        return _path_carry_fields(state, frame, 0, 0x3505E)
    frame = _movement_move(state, frame, 'unit', low16(frame.target_x), 16)
    frame = adjust_ai_carrier_fields(state, frame, 'target_x', 1, subtract=True)
    frame = adjust_ai_carrier_fields(state, frame, 'unit', 1)
    for carrier in ('target_x', 'unit'):
        frame = _movement_fixed_shift_word(state, frame, carrier, 4)
    for carrier in ('target_x', 'unit'):
        frame = adjust_ai_carrier_fields(state, frame, carrier, 8)
    frame = _movement_move(state, frame, 'count', low16(frame.target_y), 16)
    frame = adjust_ai_carrier_fields(state, frame, 'target_y', 1, subtract=True)
    frame = adjust_ai_carrier_fields(state, frame, 'count', 2)
    for carrier in ('target_y', 'count'):
        frame = _movement_fixed_shift_word(state, frame, carrier, 4)
    frame = first_replace(frame, candidates=state.table_at(0xD4B66).cursor())
    frame = _movement_move(state, frame, 'offset_y', 39, 16)
    while True:
        frame = _movement_move(state, frame, 'choice', frame.candidates.word(0, 2), 16)
        frame = _movement_compare(state, frame, low16(frame.choice), low16(frame.target_x), 16)
        in_window = not bool(frame.status & 1)
        if in_window:
            frame = _movement_compare(state, frame, low16(frame.choice), low16(frame.unit), 16)
            in_window = bool(frame.status & 5)
        if in_window:
            frame = _movement_move(state, frame, 'choice', frame.candidates.word(), 16)
            frame = _movement_compare(state, frame, low16(frame.choice), low16(frame.target_y), 16)
            in_window = not bool(frame.status & 1)
        if in_window:
            frame = _movement_compare(state, frame, low16(frame.choice), low16(frame.count), 16)
            in_window = bool(frame.status & 5)
        if in_window:
            break
        frame = first_replace(frame, candidates=frame.candidates.advance(-4))
        frame = step_ai_count_fields(frame, 'offset_y')
        if low16(frame.offset_y) == 65535:
            break
    # The real no-hit D6=FFFF still indexesF428[-1]; it is not a host no-result.
    frame = first_replace(frame, candidates=state.table_at(0xFFFFF428).cursor())
    frame = _movement_move(state, frame, 'target_x', frame.candidates.byte(low16(frame.offset_y)), 8)
    frame = _movement_compare(state, frame, low8(frame.target_x), frame.roster.byte(0, 4), 8)
    if frame.status & 4:
        return _path_carry_fields(state, frame, 0, 0x3505E)
    frame = adjust_ai_carrier_fields(state, frame, 'offset_y', 1)
    frame = store_ai_value_fields(state, frame, 0xFFFFF392, low16(frame.offset_y), 16)
    return _path_carry_fields(state, frame, 1, 0x35056)


def choose_active_city_assault_action_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """35064: compare original odd roster projection against the self-assigned scan."""
    frame = _movement_frame(state, frame)
    frame = _active_packet_call_fields(state, frame, 0x3508A, 0x35068)
    frame = _active_packet_call_fields(state, frame, 0x350B2, 0x3506C)
    frame = compare_ai_long_fields(state, frame, frame.unit, frame.target_x)
    overwhelmed = not bool(frame.status & 5)
    if not overwhelmed:
        frame = _movement_compare(state, frame, low16(frame.count), low16(frame.target_y), 16)
        overwhelmed = not bool(frame.status & 5)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 8 if overwhelmed else 7, 16)


def project_selected_roster_strength_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3508A: retain MOVE.W roster id inside the same D0 LONG accumulation."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF72A).cursor(),
        candidates=state.table_at(0xFFFFC800).cursor())
    frame = _movement_move_long(state, frame, 'target_x', 0)
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    while True:
        value = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'target_x', value, 16)
        if frame.status & 8:
            return frame
        frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
        frame = _movement_move_long(state, frame, 'unit', frame.candidates.long(low16(frame.target_x)))
        frame = adjust_ai_carrier_fields(state, frame, 'target_x', frame.unit, 32)
        frame = compare_ai_long_fields(state, frame, frame.unit, 5000)
        if not frame.status & 1:
            frame = adjust_ai_carrier_fields(state, frame, 'target_y', 1)


def measure_self_assigned_officers_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """350B2: preserve the overwritten chosen-city load and predecrement self-id test."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'distance', state.read(0xFFFFF392, 2), 16)
    frame = first_replace(frame, roster=state.table_at(0xFFFFCD00).cursor(),
        candidates=state.table_at(0xFFFFC800).cursor())
    frame = _movement_move_long(state, frame, 'unit', 0)
    frame = _movement_move(state, frame, 'count', 0, 16)
    frame = _movement_move(state, frame, 'distance', 255, 16)
    while True:
        frame = first_replace(frame, roster=frame.roster.advance(-1))
        frame = _movement_compare(state, frame, low8(frame.distance), frame.roster.byte(), 8)
        if frame.status & 4:
            frame = _movement_move(state, frame, 'offset_x', low16(frame.distance), 16)
            frame = _movement_fixed_shift_word(state, frame, 'offset_x', 2)
            frame = _movement_move_long(state, frame, 'offset_y', frame.candidates.long(low16(frame.offset_x)))
            frame = adjust_ai_carrier_fields(state, frame, 'unit', frame.offset_y, 32)
            frame = compare_ai_long_fields(state, frame, frame.offset_y, 5000)
            if not frame.status & 1:
                frame = adjust_ai_carrier_fields(state, frame, 'count', 1)
        frame = step_ai_count_fields(frame, 'distance')
        if low16(frame.distance) == 65535:
            return frame


def choose_active_city_mask_action_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """350E8: relation LONG retains highWORD; original WORD-shift/SWAP gate stays."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF376, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
    frame = first_replace(frame, roster=state.table_at(0xFFFFE710).cursor())
    frame = _movement_move(state, frame, 'target_x', frame.roster.word(low16(frame.target_x)), 16)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF427).cursor())
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF392, 2), 16)
    frame = _movement_move(state, frame, 'unit', 0, 16)
    frame = _movement_move(state, frame, 'unit', frame.roster.byte(low16(frame.target_y)), 8)
    frame = test_ai_register_bit_fields(state, frame, frame.target_x, frame.unit)
    choose_eight = False
    if not frame.status & 4:
        frame = _active_packet_call_fields(state, frame, 0x83D4, 0x35110)
        frame = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)
        frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
        frame = _economy_swap_fields(state, frame, 'target_x')
        frame = _movement_test(state, frame, low16(frame.target_x), 16)
        choose_eight = not bool(frame.status & 4)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 8 if choose_eight else 4, 16)


def choose_active_processed_city_action_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """35132: the actual city BYTE decides command2 or5."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFEA37).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF392, 2), 16)
    frame = _movement_test(state, frame, frame.roster.byte(low16(frame.target_x)), 8)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 2 if frame.status & 4 else 5, 16)


def choose_active_linked_city_action_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """35154: real linked-force helper, then complete WORD comparison."""
    frame = _movement_frame(state, frame)
    frame = _active_packet_call_fields(state, frame, 0x35172, 0x35158)
    frame = _movement_compare(state, frame, low16(frame.target_y), state.read(0xFFFFF376, 2), 16)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 6 if frame.status & 4 else 8, 16)


def linked_city_force_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """35172: original reverse256 officer scan, including no-hit signedFFFF lookup."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFA050).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF392, 2), 16)
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    frame = _movement_move(state, frame, 'unit', 255, 16)
    while True:
        frame = _movement_move(state, frame, 'target_y', frame.roster.byte(low16(frame.unit)), 8)
        frame = _movement_compare(state, frame, low16(frame.target_x), low16(frame.target_y), 16)
        if frame.status & 4:
            break
        frame = step_ai_count_fields(frame, 'unit')
        if low16(frame.unit) == 65535:
            break
    frame = first_replace(frame, roster=state.table_at(0xFFFFCC00).cursor())
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(low16(frame.unit)), 8)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF427).cursor())
    return _movement_move(state, frame, 'target_y', frame.roster.byte(low16(frame.target_y)), 8)


def choose_selected_roster_resource_action_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """351A2: actual8000 gate and the original member skill/capacity carry."""
    frame = _movement_frame(state, frame)
    frame = _active_packet_call_fields(state, frame, 0x351CA, 0x351A6)
    frame = compare_ai_long_fields(state, frame, frame.target_x, 8000)
    choose_eight = bool(frame.status & 1)
    if not choose_eight:
        frame = _active_packet_call_fields(state, frame, 0x351E4, 0x351B4)
        choose_eight = bool(frame.status & 1)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 8 if choose_eight else 7, 16)


def _active_roster_strength_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """The two genuinely identical351CA/35366 owners share this entire body."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF72A).cursor(),
        candidates=state.table_at(0xFFFFC800).cursor())
    frame = _movement_move_long(state, frame, 'target_x', 0)
    while True:
        value = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'target_y', value, 16)
        if frame.status & 8:
            return frame
        frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
        frame = adjust_ai_carrier_fields(state, frame, 'target_x', frame.candidates.long(low16(frame.target_y)), 32)


def selected_roster_strength_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """351CA: original complete roster sum, no additional CALL or save slot."""
    return _active_roster_strength_fields(state, frame)


def selected_roster_troop_shortfall_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """351E4: stop only when originalB000 WORD exceedsB200 WORD; preserveC tail."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF72A).cursor(),
        candidates=state.table_at(0xFFFFB000).cursor(), controller=state.table_at(0xFFFFB200).cursor())
    while True:
        value = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'target_x', value, 16)
        if frame.status & 8:
            return _path_carry_fields(state, frame, 0, 0x3520A)
        frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
        frame = _movement_move(state, frame, 'target_y', frame.candidates.word(low16(frame.target_x)), 16)
        frame = _movement_compare(state, frame, low16(frame.target_y), frame.controller.word(low16(frame.target_x)), 16)
        if not frame.status & 5:
            return _path_carry_fields(state, frame, 1, 0x35202)


def choose_active_adjacent_group_action_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """35286: actual candidate firstWORD decides9 or11."""
    frame = _movement_frame(state, frame)
    frame = _active_packet_call_fields(state, frame, 0x352A4, 0x3528A)
    frame = _movement_test(state, frame, state.read(0xFFFFD300, 2), 16)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 11 if frame.status & 8 else 9, 16)


def collect_active_adjacent_groups_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """352A4: four actual wrapped coordinates, live force and dynamicLONG relation mask."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(state.read(0x00FF382C, 4)).cursor())
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(0, 1), 8)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)
    frame = adjust_ai_carrier_fields(state, frame, 'target_y', 1, subtract=True)
    frame = _movement_move(state, frame, 'unit', low16(frame.target_x), 16)
    frame = adjust_ai_carrier_fields(state, frame, 'unit', 1)
    frame = _movement_move(state, frame, 'count', 0, 16)
    frame = _movement_move(state, frame, 'count', frame.roster.byte(0, 2), 8)
    frame = _movement_move(state, frame, 'distance', low16(frame.count), 16)
    frame = adjust_ai_carrier_fields(state, frame, 'distance', 1, subtract=True)
    frame = _movement_move(state, frame, 'offset_x', low16(frame.count), 16)
    frame = adjust_ai_carrier_fields(state, frame, 'offset_x', 1)
    for carrier in ('target_y', 'unit'):
        frame = _movement_fixed_shift_word(state, frame, carrier, 8)
        frame = _movement_move(state, frame, carrier, low8(frame.count), 8)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 8)
    frame = _movement_move(state, frame, 'count', low16(frame.target_x), 16)
    frame = _movement_move(state, frame, 'target_x', low8(frame.distance), 8)
    frame = _movement_move(state, frame, 'count', low8(frame.offset_x), 8)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFD300).cursor(),
        controller=state.table_at(0xFFFF9000).cursor())
    frame = _movement_move(state, frame, 'distance', 0, 16)
    frame = first_replace(frame, scan=state.table_at(0xFFFFE710).cursor())
    frame = _movement_move(state, frame, 'choice', state.read(0xFFFFF376, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'choice', 1)
    frame = _movement_move(state, frame, 'choice', frame.scan.word(low16(frame.choice)), 16)
    while True:
        frame = _movement_move(state, frame, 'offset_x', frame.controller.byte(), 8)
        frame = _movement_move(state, frame, 'offset_x', low16(frame.offset_x) & 15, 16)
        if frame.status & 4:
            return store_ai_value_fields(state, frame, frame.candidates.base, 65535, 16)
        frame = _movement_move(state, frame, 'offset_y', 0, 16)
        frame = _movement_move(state, frame, 'offset_y', frame.controller.byte(0, 4), 8)
        frame = _movement_compare(state, frame, low8(frame.offset_y), state.read(0xFFFFF377, 1), 8)
        eligible = not bool(frame.status & 4)
        if eligible:
            frame = test_ai_register_bit_fields(state, frame, frame.choice, frame.offset_y)
            eligible = bool(frame.status & 4)
        if eligible:
            frame = _movement_move(state, frame, 'offset_y', frame.controller.byte(0, 1), 8)
            frame = _movement_fixed_shift_word(state, frame, 'offset_y', 8)
            frame = _movement_move(state, frame, 'offset_y', frame.controller.byte(0, 2), 8)
            for carrier in ('target_x', 'target_y', 'unit', 'count'):
                frame = _movement_compare(state, frame, low16(frame.offset_y), low16(frame.carrier(carrier)), 16)
                if frame.status & 4:
                    frame = store_ai_value_fields(state, frame, frame.candidates.base, low16(frame.distance), 16)
                    frame = first_replace(frame, candidates=frame.candidates.advance(2))
                    break
        frame = first_replace(frame, controller=frame.controller.advance(s16(low16(frame.offset_x)) + 13))
        frame = adjust_ai_carrier_fields(state, frame, 'offset_x', 13)
        frame = adjust_ai_carrier_fields(state, frame, 'distance', low16(frame.offset_x))


def choose_active_strength_action_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """35342: real whole-roster sum and retained fallbackD2 candidate."""
    frame = _movement_frame(state, frame)
    frame = _active_packet_call_fields(state, frame, 0x35366, 0x35346)
    frame = _active_packet_call_fields(state, frame, 0x35380, 0x3534A)
    frame = compare_ai_long_fields(state, frame, frame.target_y, frame.target_x)
    if not frame.status & 5:
        return store_ai_value_fields(state, frame, 0xFFFFF728, 11, 16)
    frame = store_ai_value_fields(state, frame, 0xFFFFF744, low16(frame.unit), 16)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 10, 16)


def selected_roster_comparison_strength_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """35366: second original identical roster sum; helper adds no CALL slot."""
    return _active_roster_strength_fields(state, frame)


def measure_lightest_active_candidate_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """35380: original do-first member sums, strict-improvement and preservedD2 fallback."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFD300).cursor(),
        controller=state.table_at(0xFFFFC800).cursor())
    frame = _movement_move_long(state, frame, 'target_y', 0xFFFFFFFF)
    while True:
        value = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'count', value, 16)
        if frame.status & 8:
            return frame
        frame = first_replace(frame, candidates=state.table_at(0xFFFF9000).cursor().advance(s16(low16(frame.count))))
        frame = _movement_move(state, frame, 'distance', frame.candidates.byte(), 8)
        frame = _movement_move(state, frame, 'distance', low16(frame.distance) & 15, 16)
        frame = adjust_ai_carrier_fields(state, frame, 'distance', 1, subtract=True)
        frame = _movement_move_long(state, frame, 'offset_x', 0)
        frame = _movement_move(state, frame, 'offset_y', 0, 16)
        while True:
            frame = _movement_move(state, frame, 'offset_y', frame.candidates.byte(low16(frame.distance), 13), 8)
            frame = _movement_fixed_shift_word(state, frame, 'offset_y', 2)
            frame = adjust_ai_carrier_fields(state, frame, 'offset_x', frame.controller.long(low16(frame.offset_y)), 32)
            frame = step_ai_count_fields(frame, 'distance')
            if low16(frame.distance) == 65535:
                break
        frame = compare_ai_long_fields(state, frame, frame.offset_x, frame.target_y)
        if frame.status & 1:
            frame = _movement_move_long(state, frame, 'target_y', frame.offset_x)
            frame = _movement_move(state, frame, 'unit', low16(frame.count), 16)


def schedule_active_comparison_dialogue_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """353BC: original request fields, not host acknowledgement or an executed command."""
    frame = _movement_frame(state, frame)
    frame = store_ai_value_fields(state, frame, 0xFFFFEFBE, state.read(0xFFFFF744, 2), 16)
    frame = store_ai_value_fields(state, frame, 0xFFFFEFC6, 0, 16, True)
    for address, value in ((0xFFFFF65A, 20), (0xFFFFF38C, 181), (0xFFFFF612, 0x208),
            (0xFFFFF362, 4), (0xFFFFF576, 1), (0xFFFFF728, 65535)):
        frame = store_ai_value_fields(state, frame, address, value, 16)
    return frame


def clear_active_contact_command_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """353EC: original explicit commandFFFF store and return."""
    return store_ai_value_fields(state, _movement_frame(state, frame), 0xFFFFF728, 65535, 16)


def clear_active_idle_command_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """353F4: distinct original owner, same explicit commandFFFF store."""
    return store_ai_value_fields(state, _movement_frame(state, frame), 0xFFFFF728, 65535, 16)


def execute_active_packet_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int) -> FirstDeploymentFrame:
    """The twelve actual34F7C targets, entered with the caller's existing34F78 LONG."""
    frame = _movement_frame(state, frame)
    roots = {
        0x34F94: choose_active_packet_contact_action_fields,
        0x35064: choose_active_city_assault_action_fields,
        0x350E8: choose_active_city_mask_action_fields,
        0x35132: choose_active_processed_city_action_fields,
        0x35154: choose_active_linked_city_action_fields,
        0x351A2: choose_selected_roster_resource_action_fields,
        0x35286: choose_active_adjacent_group_action_fields,
        0x35342: choose_active_strength_action_fields,
        0x353BC: schedule_active_comparison_dialogue_fields,
        0x353EC: clear_active_contact_command_fields,
        0x353F4: clear_active_idle_command_fields,
    }
    if target == 0x35210:
        from ..high_level_remaining_flows.business_highbank import finish_command_object_removal_fields
        return finish_command_object_removal_fields(state, frame)
    if target not in roots:
        raise ValueError('target outside the original active-packet twelve-entry directory')
    return roots[target](state, frame)
