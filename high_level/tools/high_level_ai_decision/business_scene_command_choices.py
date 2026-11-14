"""Live city-command eligibility, resource classes and roster selection.

confirmed: six complete original owners32404,32B10,32B42,32D72,333F4,
33422. The existing scalar policies remain independent readable evidence;
these entries carry the actual Scene, sixteen LONGs, physical SP and full SR.
No outer CALL is recreated here. Original unchecked indexes and tie/overflow
rules are retained; this module does not supply device events or fix game bugs.
"""
from ..high_level_scene_flows.domain import SceneState, low8, low16
from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame, first_replace
from ..high_level_main_flows.business_movement_support import (
    _movement_frame, _movement_move, _movement_compare, _movement_test,
    _movement_fixed_shift_word, _path_carry_fields,
)
from .scene_fields import (
    store_ai_value_fields, adjust_ai_carrier_fields, compare_ai_long_fields,
    test_ai_register_bit_fields,
)


def classify_city_resources_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """32404..3244A: two live LONG balances, original20000 thresholds."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', 65535, 16)
    frame = first_replace(frame, roster=state.table_at(0xFFFFDFFC).cursor(),
        candidates=state.table_at(0xFFFFE09C).cursor())
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
    frame = compare_ai_long_fields(state, frame,
        frame.roster.long(low16(frame.target_y)), 20000)
    if frame.status & 1:
        frame = compare_ai_long_fields(state, frame,
            frame.candidates.long(low16(frame.target_y)), 20000)
        if not frame.status & 1:
            frame = _movement_move(state, frame, 'target_x', 1, 16)
        return frame
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = compare_ai_long_fields(state, frame,
        frame.candidates.long(low16(frame.target_y)), 20000)
    if not frame.status & 1:
        frame = _movement_move(state, frame, 'target_x', 2, 16)
    return frame


def _command_owner_match_fields(state, frame):
    """The three ordered BYTE comparisons shared by the two original gates."""
    for address in (0xFFFFF67B, 0xFFFFF67D, 0xFFFFF67F):
        frame = _movement_compare(state, frame, low8(frame.target_x), state.read(address, 1), 8)
        if frame.status & 4:
            return frame, True
    return frame, False


def _command_carry_fields(state, frame, enabled, instruction):
    """Real privileged SR operation; reuse its trace/supervisor boundary too."""
    return _path_carry_fields(state, frame, int(enabled), instruction)


def selected_city_has_player_owner_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """32B10..32B42: preserve D0's WORD/BYTE lanes and actual final CMP flags."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF427).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF3A8, 2), 16)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(low16(frame.target_x)), 8)
    frame, owned = _command_owner_match_fields(state, frame)
    return _command_carry_fields(state, frame, owned, 0x32B3C if owned else 0x32B34)


def selected_player_officer_removed_gate_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """32B42..32B88: only player-owned city paths read officer membership."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF427).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF3A8, 2), 16)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(low16(frame.target_x)), 8)
    frame, owned = _command_owner_match_fields(state, frame)
    if not owned:
        return _command_carry_fields(state, frame, False, 0x32B7A)
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF3A6, 2), 16)
    frame = first_replace(frame, roster=state.table_at(0xFFFFCC00).cursor())
    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(low16(frame.target_y)), 8)
    frame = _movement_compare(state, frame, low8(frame.target_y), 255, 8)
    removed = bool(frame.status & 4)
    return _command_carry_fields(state, frame, removed, 0x32B82 if removed else 0x32B7A)


def _scan_unmarked_command_roster_fields(state, frame):
    """Original sentinel loop, strict unsigned maximum and first-winner ties."""
    while True:
        officer = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'unit', officer, 16)
        if frame.status & 8:
            return frame
        frame = test_ai_register_bit_fields(state, frame, frame.unit, 14)
        if not frame.status & 4:
            continue
        frame = _movement_move(state, frame, 'count', low16(frame.unit), 16)
        frame = _movement_fixed_shift_word(state, frame, 'count', 1)
        frame = _movement_move(state, frame, 'count', frame.candidates.word(low16(frame.count)), 16)
        frame = _movement_compare(state, frame, low16(frame.count), low16(frame.target_x), 16)
        if frame.status & 5:
            continue
        frame = _movement_move(state, frame, 'target_x', low16(frame.count), 16)
        frame = _movement_move(state, frame, 'target_y', low16(frame.unit), 16)


def select_and_mark_roster_attribute_max_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """32D72..32DCE: guard second member; select, action-mark, then roster BSET."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF72A).cursor(),
        candidates=state.table_at(0xFFFFB600).cursor())
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move(state, frame, 'target_y', 65535, 16)
    frame = _movement_test(state, frame, state.read(0xFFFFF72C, 2), 16)
    if frame.status & 8:
        return frame
    frame = _scan_unmarked_command_roster_fields(state, frame)
    frame = _movement_test(state, frame, low16(frame.target_y), 16)
    if frame.status & 8:
        return frame
    frame = first_replace(frame, candidates=state.table_at(0xFFFFCD00).cursor())
    frame = store_ai_value_fields(state, frame,
        frame.candidates.address(low16(frame.target_y)), 1, 8)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF72A).cursor())
    while True:
        officer = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'unit', officer, 16)
        if frame.status & 8:
            return frame
        frame = _movement_compare(state, frame, low16(frame.unit), low16(frame.target_y), 16)
        if not frame.status & 4:
            continue
        frame = test_ai_register_bit_fields(state, frame, frame.unit, 14)
        frame = first_replace(frame, unit=frame.unit | 16384)
        return store_ai_value_fields(state, frame, frame.roster.address(0, -2), low16(frame.unit), 16)


def select_unmarked_roster_intelligence_max_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """333F4..33422: selection without32D72's early guard or write side effects."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF72A).cursor(),
        candidates=state.table_at(0xFFFFB600).cursor())
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move(state, frame, 'target_y', 65535, 16)
    return _scan_unmarked_command_roster_fields(state, frame)


def clear_candidate_city_order_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33422..3346A: first of three matching city orders only; live city reread."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFE80C).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF3A8, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
    frame = adjust_ai_carrier_fields(state, frame, 'target_x', state.read(0xFFFFF3A8, 2))
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF3F2, 2), 16)
    for displacement in (0, 4, 8):
        index = low16(frame.target_x)
        frame = _movement_compare(state, frame, low16(frame.target_y), frame.roster.word(index, displacement), 16)
        if frame.status & 4:
            return store_ai_value_fields(state, frame, frame.roster.address(index, displacement), 65535, 16)
    return frame
