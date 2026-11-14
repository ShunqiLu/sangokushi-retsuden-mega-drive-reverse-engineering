"""Live Scene successor of the foreign-officer recruitment policy.

confirmed: complete original owners33106..33160,33160..331BC and331BC..3321A
in recovered_code.s/direct_descendants.s. The mature economy policy names
describe the decisions; these entry points additionally retain every actual
carrier, narrow arithmetic flag, live read and original nested return slot.
No scalar tuple is promoted to a CPU frame and no new formal-byte credit is
claimed. Neighbor/font/etc. source bytes remain in external owned resources.
"""
from ..high_level_scene_flows.domain import SceneState, low8, low16, s16
from ..high_level_battle_ai.contexts_first_deployment import (
    FirstDeploymentFrame, FirstDeploymentReturnBoundary, first_replace,
)
from ..high_level_main_flows.business_movement_support import (
    _movement_frame, _movement_move, _movement_test, _movement_compare,
    _movement_fixed_shift_word, _movement_save_longs, _movement_restore_longs,
)
from ..high_level_ai_decision.scene_fields import (
    store_ai_value_fields, adjust_ai_carrier_fields,
    test_ai_register_bit_fields, step_ai_count_fields,
)


def _recruitment_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Only the four actual CALL pairs; preserve the caller's outer LONG."""
    if (target, continuation) not in (
            (0x5F48, 0x33116), (0x33160, 0x33122),
            (0x83D4, 0x3313E), (0x331BC, 0x331A8)):
        raise ValueError('actual foreign-recruitment CALL pair required')
    frame = _movement_frame(state, frame)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    if target == 0x33160:
        result = select_foreign_neighbor_officer_fields(state, entered)
    elif target == 0x331BC:
        result = scan_city_officer_candidate_fields(state, entered)
    elif target == 0x5F48:
        from ..high_level_gameplay_flow.business_battle import build_roster_fields
        from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
        result = build_roster_fields(BattlePresentationMemory(state), entered)
    else:
        from ..high_level_battle_ai.business_formation import first_deployment_random_fields
        from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
        result = first_deployment_random_fields(BattlePolicyMemory(state), entered)
    result = _movement_frame(state, result)
    returned = result.stack_cursor.long()
    if returned != continuation:
        raise FirstDeploymentReturnBoundary(returned, result, continuation)
    return first_replace(result, stack_cursor=result.stack_cursor.advance(4))


def plan_foreign_officer_recruitment_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33106: build the live roster, gate capacity/candidate and lottery once."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = store_ai_value_fields(state, frame, 0xFFFFF630, 65535, 16)
    frame = _recruitment_call_fields(state, frame, 0x5F48, 0x33116)
    frame = _movement_compare(state, frame, low16(frame.count), 10, 16)
    if not frame.status & 1:
        return store_ai_value_fields(state, frame, 0xFFFFF728, 3, 16)
    frame = _recruitment_call_fields(state, frame, 0x33160, 0x33122)
    frame = _movement_test(state, frame, low16(frame.unit), 16)
    if frame.status & 8:
        return store_ai_value_fields(state, frame, 0xFFFFF728, 3, 16)
    frame = _movement_compare(state, frame, low16(frame.offset_x), 75, 16)
    if frame.status & 1:
        frame = _movement_compare(state, frame, low16(frame.offset_y), 75, 16)
        if frame.status & 1:
            return store_ai_value_fields(state, frame, 0xFFFFF728, 3, 16)
    frame = _recruitment_call_fields(state, frame, 0x83D4, 0x3313E)
    frame = test_ai_register_bit_fields(state, frame, frame.target_x, 4)
    if not frame.status & 4:
        return store_ai_value_fields(state, frame, 0xFFFFF728, 3, 16)
    frame = store_ai_value_fields(state, frame, 0xFFFFF3F2, low16(frame.unit), 16)
    frame = store_ai_value_fields(state, frame, 0xFFFFF3A8, low16(frame.count), 16)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 6, 16)


def select_foreign_neighbor_officer_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33160: live unprocessed foreign neighbors, retaining no-winner scores.

    D0.W is cleared only once, so its BYTE reads retain the real upper lanes.
    Each city scan restores D7/A5 through its actual two-LONG MOVEM. A0 keeps
    its consumed sentinel; D4 receives FFFF on the no-candidate path while
    D5/D6 and A4 retain whatever the original scans actually left there.
    """
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xD4BDA).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 3)
    frame = first_replace(frame, roster=frame.roster.advance(s16(low16(frame.target_x))))
    frame = _movement_move(state, frame, 'choice', state.read(0xFFFFF376, 2), 16)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFB400).cursor())
    frame = first_replace(frame, controller=state.table_at(0xFFFFB600))
    frame = first_replace(frame, scan=state.table_at(0xFFFFC300).cursor())
    frame = first_replace(frame, scratch=state.table_at(0xFFFFF427))
    frame = first_replace(frame, auxiliary=state.table_at(0xFFFFEA37))
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    frame = _movement_move(state, frame, 'unit', 65535, 16)
    frame = _movement_move(state, frame, 'count', 65535, 16)
    while True:
        city = frame.roster.byte()
        frame = first_replace(frame, roster=frame.roster.advance(1))
        frame = _movement_move(state, frame, 'target_x', city, 8)
        if frame.status & 8:
            break
        frame = _movement_test(state, frame, frame.auxiliary.byte(low16(frame.target_x)), 8)
        if not frame.status & 4:
            continue
        frame = _movement_compare(state, frame, low8(frame.choice), frame.scratch.byte(low16(frame.target_x)), 8)
        if frame.status & 4:
            continue
        frame = _recruitment_call_fields(state, frame, 0x331BC, 0x331A8)
    frame = _movement_move(state, frame, 'distance', low16(frame.unit), 16)
    if frame.status & 8:
        return frame
    frame = _movement_fixed_shift_word(state, frame, 'distance', 1)
    index = low16(frame.distance)
    frame = _movement_move(state, frame, 'offset_x', frame.candidates.word(index), 16)
    return _movement_move(state, frame, 'offset_y', frame.controller.word(index), 16)


def scan_city_officer_candidate_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """331BC: descending255..0 nonleader, status<=65, strict wrapped score.

    Both the leader exclusion and city owner reread are original. Equal score
    preserves the first candidate, and an owner sentinel leaves D4/D5/D6/A4
    alone. The physical saved D7/A5 LONGs are always reread before returning.
    """
    frame = _movement_frame(state, frame)
    frame = _movement_save_longs(state, frame, ('choice', 'scratch'))
    frame = first_replace(frame, scratch=state.table_at(0xFFFFF427))
    frame = _movement_move(state, frame, 'choice', 0, 16)
    frame = _movement_move(state, frame, 'choice', frame.scratch.byte(low16(frame.target_x)), 8)
    if not frame.status & 8:
        frame = _movement_fixed_shift_word(state, frame, 'choice', 1)
        frame = first_replace(frame, scratch=state.table_at(0xFFFFE640))
        frame = _movement_move(state, frame, 'choice', frame.scratch.word(low16(frame.choice)), 16)
        frame = first_replace(frame, opponent=state.table_at(0xFFFFCC00))
        frame = _movement_move(state, frame, 'distance', 255, 16)
        while True:
            index = low16(frame.distance)
            frame = _movement_compare(state, frame, low8(frame.target_x), frame.opponent.byte(index), 8)
            eligible = bool(frame.status & 4)
            if eligible:
                frame = _movement_compare(state, frame, low8(frame.distance), low8(frame.choice), 8)
                eligible = not bool(frame.status & 4)
            if eligible:
                frame = _movement_compare(state, frame, frame.scan.byte(index), 65, 8)
                eligible = bool(frame.status & 5)
            if eligible:
                frame = _movement_move(state, frame, 'offset_x', low16(frame.distance), 16)
                frame = _movement_fixed_shift_word(state, frame, 'offset_x', 1)
                score_index = low16(frame.offset_x)
                frame = _movement_move(state, frame, 'offset_y', frame.candidates.word(score_index), 16)
                frame = adjust_ai_carrier_fields(state, frame, 'offset_y', frame.controller.word(score_index))
                frame = _movement_compare(state, frame, low16(frame.offset_y), low16(frame.target_y), 16)
                if not frame.status & 5:
                    frame = _movement_move(state, frame, 'target_y', low16(frame.offset_y), 16)
                    frame = _movement_move(state, frame, 'unit', low16(frame.distance), 16)
                    frame = _movement_move(state, frame, 'count', low16(frame.target_x), 16)
            frame = step_ai_count_fields(frame, 'distance')
            if low16(frame.distance) == 65535:
                break
    return _movement_restore_longs(state, frame, ('choice', 'scratch'))
