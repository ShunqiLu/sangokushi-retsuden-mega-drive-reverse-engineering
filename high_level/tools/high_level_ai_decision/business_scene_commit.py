"""Whole-frame city AI appointments, order submission and training.

Live tables and actual partial-width carriers are explicit. The moving-roster
read and reversed training-cap correction are original behavior, not fixes.
"""
from ..high_level_scene_flows.domain import SceneState, u8, u16, u32, low8, low16, s16, divu_retained
from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame, first_replace
from ..high_level_main_flows.business_movement_support import _movement_frame, _movement_move, _movement_move_long, _movement_test, _movement_compare, _movement_fixed_shift_word, _movement_multiply_word
from .scene_fields import store_ai_value_fields, adjust_ai_carrier_fields, compare_ai_long_fields, shift_ai_long_fields, test_ai_register_bit_fields, set_ai_flag_byte_fields, step_ai_count_fields, call_scene_ai_fields


def commit_roster_city_assignments_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """320C0: choose the head, flag a candidate, then update live roster status."""
    frame = _movement_frame(state, frame)
    frame = call_scene_ai_fields(state, frame, 0x320D4, 0x320C4)
    frame = call_scene_ai_fields(state, frame, 0x3213E, 0x320C8)
    frame = call_scene_ai_fields(state, frame, 0x32192, 0x320CC)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 5, 16)


def choose_city_head_from_roster_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """320D4: first strict best qualified officer; preserve a ruler city head."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, opponent=state.table_at(0xFFFFF45E))
    frame = _movement_move(state, frame, 'choice', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'choice', 1)
    frame = _movement_move(state, frame, 'target_x', frame.opponent.word(low16(frame.choice)), 16)
    frame = first_replace(frame, scratch=state.table_at(0xFFFFE640))
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF376, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
    frame = _movement_compare(state, frame, low16(frame.target_x), frame.scratch.word(low16(frame.target_y)), 16)
    if frame.status & 4:
        return frame
    frame = first_replace(frame, roster=state.table_at(0xFFFFF72A).cursor(), candidates=state.table_at(0xFFFFB600).cursor(), controller=state.table_at(0xFFFFB400), scan=state.table_at(0xFFFFC300).cursor())
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move(state, frame, 'target_y', 65535, 16)
    while True:
        token = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'unit', token, 16)
        if frame.status & 8:
            break
        frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 255, 16)
        frame = _movement_compare(state, frame, frame.scan.byte(low16(frame.unit)), 90, 8)
        if frame.status & 1:
            continue
        frame = _movement_move(state, frame, 'distance', low16(frame.unit), 16)
        frame = _movement_fixed_shift_word(state, frame, 'distance', 1)
        frame = _movement_move(state, frame, 'count', frame.candidates.word(low16(frame.distance)), 16)
        frame = adjust_ai_carrier_fields(state, frame, 'count', frame.controller.word(low16(frame.distance)))
        frame = _movement_compare(state, frame, low16(frame.count), low16(frame.target_x), 16)
        if frame.status & 5:
            continue
        frame = _movement_move(state, frame, 'target_x', low16(frame.count), 16)
        frame = _movement_move(state, frame, 'target_y', low16(frame.unit), 16)
    frame = _movement_test(state, frame, low16(frame.target_y), 16)
    if not frame.status & 8:
        frame = store_ai_value_fields(state, frame, frame.opponent.address(low16(frame.choice)), low16(frame.target_y), 16)
    return frame


def flag_roster_b600_candidate_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3213E: last equal-score qualifying officer receives C700 bit4."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF72A).cursor(), candidates=state.table_at(0xFFFFB600).cursor(), controller=state.table_at(0xFFFFC000))
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move(state, frame, 'target_y', 65535, 16)
    while True:
        token = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'unit', token, 16)
        if frame.status & 8:
            break
        frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 255, 16)
        frame = _movement_move(state, frame, 'count', low16(frame.unit), 16)
        frame = _movement_fixed_shift_word(state, frame, 'count', 1)
        frame = _movement_move(state, frame, 'distance', frame.candidates.word(low16(frame.count)), 16)
        frame = _movement_compare(state, frame, low16(frame.distance), 100, 16)
        if frame.status & 1:
            frame = _movement_compare(state, frame, low16(frame.distance), 95, 16)
            if frame.status & 1:
                continue
            frame = _movement_compare(state, frame, frame.controller.word(low16(frame.count)), 150, 16)
            if frame.status & 1:
                continue
        frame = _movement_compare(state, frame, low16(frame.distance), low16(frame.target_x), 16)
        if frame.status & 1:
            continue
        frame = _movement_move(state, frame, 'target_x', low16(frame.distance), 16)
        frame = _movement_move(state, frame, 'target_y', low16(frame.unit), 16)
    frame = _movement_test(state, frame, low16(frame.target_y), 16)
    if not frame.status & 8:
        frame = first_replace(frame, roster=state.table_at(0xFFFFC700).cursor())
        frame = set_ai_flag_byte_fields(state, frame, frame.roster.address(low16(frame.target_y)), 4)
    return frame


def update_roster_c700_status_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """32192: retain the original moving-A0 byte lookup, not a stable flag table."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF72A).cursor(), candidates=state.table_at(0xFFFFC700).cursor(), controller=state.table_at(0xFFFFC600), scan=state.table_at(0xFFFFC000).cursor(), opponent=state.table_at(0xFFFFBE00))
    while True:
        token = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'target_x', token, 16)
        if frame.status & 8:
            return frame
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 255, 16)
        frame = _movement_move(state, frame, 'target_y', 0, 16)
        frame = _movement_move(state, frame, 'unit', frame.controller.byte(low16(frame.target_x)), 8)
        for threshold in (5, 10, 15, 20):
            frame = _movement_compare(state, frame, low8(frame.unit), threshold, 8)
            if frame.status & 1:
                break
            frame = adjust_ai_carrier_fields(state, frame, 'target_y', 1)
        frame = _movement_move(state, frame, 'unit', frame.roster.byte(low16(frame.target_x)), 8)
        frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 7, 16)
        frame = _movement_compare(state, frame, low8(frame.unit), low8(frame.target_y), 8)
        if not frame.status & 1:
            continue
        frame = _movement_move(state, frame, 'unit', low16(frame.target_x), 16)
        frame = _movement_fixed_shift_word(state, frame, 'unit', 1)
        frame = _movement_move(state, frame, 'count', frame.scan.word(low16(frame.unit)), 16)
        frame = _movement_compare(state, frame, low16(frame.count), frame.opponent.word(low16(frame.unit)), 16)
        if frame.status & 1:
            frame = test_ai_register_bit_fields(state, frame, frame.target_y, 3)
            frame = first_replace(frame, target_y=u32(frame.target_y | 8))
        frame = _movement_move(state, frame, 'unit', frame.candidates.byte(low16(frame.target_x)), 8)
        frame = _movement_move(state, frame, 'unit', low8(frame.unit) & 16, 8)
        frame = _movement_move(state, frame, 'unit', low8(frame.unit) | low8(frame.target_y), 8)
        frame = store_ai_value_fields(state, frame, frame.candidates.address(low16(frame.target_x)), low8(frame.unit), 8)


def select_order_officer_b600_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """334CA: first strict B600 maximum among unmarked live roster WORDs."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF72A).cursor(), candidates=state.table_at(0xFFFFB600).cursor())
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move(state, frame, 'target_y', 65535, 16)
    while True:
        token = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'unit', token, 16)
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


def prepare_city_order_amount_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """334F8: original signed division and unsigned LONG cap, not a new budget."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFDFFC).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    frame = _movement_move_long(state, frame, 'target_y', frame.roster.long(low16(frame.target_x)))
    frame = _movement_move_long(state, frame, 'unit', 3)
    frame = call_scene_ai_fields(state, frame, 0x35760, 0x3350E)
    frame = compare_ai_long_fields(state, frame, frame.target_y, 99999)
    if not frame.status & 5:
        frame = _movement_move_long(state, frame, 'target_y', 99999)
    return store_ai_value_fields(state, frame, 0xFFFFF39E, frame.target_y, 32)


def commit_city_field_order_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3346A: submit the actual selected officer/amount and consume its roster bit."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFE59C).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    frame = _movement_compare(state, frame, frame.roster.word(low16(frame.target_x)), 100, 16)
    if frame.status & 1:
        frame = call_scene_ai_fields(state, frame, 0x334CA, 0x33482)
        frame = store_ai_value_fields(state, frame, 0xFFFFF3A6, low16(frame.target_y), 16)
        if not frame.status & 8:
            frame = call_scene_ai_fields(state, frame, 0x334F8, 0x3348E)
            frame = first_replace(frame, roster=state.table_at(0xFFFFE80C).cursor())
            frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
            frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
            frame = adjust_ai_carrier_fields(state, frame, 'target_x', state.read(0xFFFFF364, 2))
            frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
            frame = store_ai_value_fields(state, frame, frame.roster.address(low16(frame.target_x), 8), state.read(0xFFFFF3A6, 2), 16)
            frame = _movement_move_long(state, frame, 'target_y', state.read(0xFFFFF39E, 4))
            # DIVU overflow retains D1. Its undefined N/Z are overwritten by
            # the immediately following MOVE.W, with no branch or callback.
            frame = first_replace(frame, target_y=divu_retained(frame.target_y, 100))
            frame = store_ai_value_fields(state, frame, frame.roster.address(low16(frame.target_x), 10), low16(frame.target_y), 16)
            frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF3A6, 2), 16)
            frame = first_replace(frame, roster=state.table_at(0xFFFFCD00).cursor())
            frame = store_ai_value_fields(state, frame, frame.roster.address(low16(frame.target_x)), 1, 8)
            frame = call_scene_ai_fields(state, frame, 0x320A0, 0x334C2)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 4, 16)


def select_training_officer_c500_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33574: real troop gate and BYTE minimum; D0's high BYTE is retained."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF72A).cursor(), candidates=state.table_at(0xFFFFC500).cursor(), controller=state.table_at(0xFFFFC800))
    frame = _movement_move(state, frame, 'target_x', 65535, 16)
    frame = _movement_move(state, frame, 'target_y', 65535, 16)
    while True:
        token = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'unit', token, 16)
        if frame.status & 8:
            return frame
        frame = test_ai_register_bit_fields(state, frame, frame.unit, 14)
        if not frame.status & 4:
            continue
        frame = _movement_move(state, frame, 'count', low16(frame.unit), 16)
        frame = _movement_fixed_shift_word(state, frame, 'count', 2)
        from ..high_level_main_flows.business_movement_support import _movement_test_long
        frame = _movement_test_long(state, frame, frame.controller.long(low16(frame.count)))
        if frame.status & 4:
            continue
        frame = _movement_move(state, frame, 'count', frame.candidates.byte(low16(frame.unit)), 8)
        frame = _movement_compare(state, frame, low8(frame.count), low8(frame.target_x), 8)
        if not frame.status & 1:
            continue
        frame = _movement_move(state, frame, 'target_x', low8(frame.count), 8)
        frame = _movement_move(state, frame, 'target_y', low16(frame.unit), 16)


def prepare_officer_training_cost_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """335AE: retain DIVU overflow data then the original sign-extended WORD cost."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFC800).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF3A6, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    frame = _movement_move_long(state, frame, 'target_y', frame.roster.long(low16(frame.target_x)))
    packed = divu_retained(frame.target_y, 10)
    # EXT.L immediately overwrites DIVU's undefined overflow flags.
    frame = _movement_move_long(state, frame, 'target_y', u32(s16(low16(packed))))
    return store_ai_value_fields(state, frame, 0xFFFFF39E, frame.target_y, 32)


def apply_officer_training_growth_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """335C8: genuine sample, stitched growth and original reversed cap correction."""
    frame = _movement_frame(state, frame)
    frame = call_scene_ai_fields(state, frame, 0x83D4, 0x335CE)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF3A6, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
    frame = first_replace(frame, roster=state.table_at(0xFFFFB400).cursor())
    frame = _movement_move(state, frame, 'unit', frame.roster.word(low16(frame.target_x)), 16)
    frame = _movement_move(state, frame, 'target_y', low16(frame.unit), 16)
    frame = _movement_fixed_shift_word(state, frame, 'unit', 2)
    frame = adjust_ai_carrier_fields(state, frame, 'unit', low16(frame.target_y))
    frame = first_replace(frame, roster=state.table_at(0xFFFFC000).cursor())
    frame = adjust_ai_carrier_fields(state, frame, 'unit', frame.roster.word(low16(frame.target_x)))
    frame = _movement_move_long(state, frame, 'target_y', 0)
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF61C, 2), 16)
    frame = shift_ai_long_fields(state, frame, 'target_y', 3)
    frame = _movement_move_long(state, frame, 'target_y', u32(frame.target_y << 16 | frame.target_y >> 16))
    frame = adjust_ai_carrier_fields(state, frame, 'target_y', 8)
    frame = _movement_multiply_word(state, frame, 'unit', low16(frame.target_y))
    frame = first_replace(frame, unit=divu_retained(frame.unit, 1000))
    # Next LSR.W overwrites NZVC before any observable operation; X is retained
    # by DIVU and then set by this actual shift. No overflow flags fabricated.
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1, True)
    frame = first_replace(frame, roster=state.table_at(0xFFFFC500).cursor())
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(low16(frame.target_x)), 8)
    frame = adjust_ai_carrier_fields(state, frame, 'target_y', low16(frame.unit))
    frame = _movement_compare(state, frame, low16(frame.target_y), 100, 16)
    if not frame.status & 5:
        frame = _movement_move(state, frame, 'count', 100, 16)
        frame = adjust_ai_carrier_fields(state, frame, 'count', low16(frame.target_y), subtract=True)
        frame = adjust_ai_carrier_fields(state, frame, 'unit', low16(frame.count), subtract=True)
        frame = _movement_move(state, frame, 'target_y', 100, 16)
    frame = store_ai_value_fields(state, frame, frame.roster.address(low16(frame.target_x)), low8(frame.target_y), 8)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
    frame = first_replace(frame, roster=state.table_at(0xFFFFC000).cursor())
    address = frame.roster.address(low16(frame.target_x))
    from ..high_level_main_flows.business_movement_support import _movement_binary_flags
    frame, development = _movement_binary_flags(state, frame, state.read(address, 2), low16(frame.unit), 16)
    state.write(address, 2, development)
    frame = _movement_compare(state, frame, state.read(address, 2), 999, 16)
    if not frame.status & 5:
        frame = store_ai_value_fields(state, frame, address, 999, 16)
    return frame


def commit_officer_training_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33524: actual half-balance eligibility, nontransactional debit and growth."""
    frame = _movement_frame(state, frame)
    frame = call_scene_ai_fields(state, frame, 0x33574, 0x33528)
    frame = store_ai_value_fields(state, frame, 0xFFFFF3A6, low16(frame.target_y), 16)
    if not frame.status & 8:
        frame = call_scene_ai_fields(state, frame, 0x335AE, 0x33534)
        frame = first_replace(frame, roster=state.table_at(0xFFFFDFFC).cursor())
        frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
        frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
        frame = _movement_move_long(state, frame, 'target_y', frame.roster.long(low16(frame.target_x)))
        frame = _movement_move_long(state, frame, 'unit', frame.target_y)
        frame = shift_ai_long_fields(state, frame, 'unit', 1, True)
        frame = compare_ai_long_fields(state, frame, frame.unit, state.read(0xFFFFF39E, 4))
        if not frame.status & 1:
            frame = adjust_ai_carrier_fields(state, frame, 'target_y', state.read(0xFFFFF39E, 4), 32, True)
            frame = store_ai_value_fields(state, frame, frame.roster.address(low16(frame.target_x)), frame.target_y, 32)
            frame = call_scene_ai_fields(state, frame, 0x335C8, 0x3355A)
            frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF3A6, 2), 16)
            frame = first_replace(frame, roster=state.table_at(0xFFFFCD00).cursor())
            frame = store_ai_value_fields(state, frame, frame.roster.address(low16(frame.target_x)), 1, 8)
            frame = call_scene_ai_fields(state, frame, 0x320A0, 0x3356C)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 9, 16)


def count_force_cities_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """325E4: real40 BYTE owners; retain D0 and every caller-supplied high lane."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF428).cursor())
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    frame = _movement_move(state, frame, 'unit', 39, 16)
    while True:
        owner = frame.roster.byte()
        frame = first_replace(frame, roster=frame.roster.advance(1))
        frame = _movement_compare(state, frame, low8(frame.target_x), owner, 8)
        if frame.status & 4:
            frame = adjust_ai_carrier_fields(state, frame, 'target_y', 1)
        frame = step_ai_count_fields(frame, 'unit')
        if low16(frame.unit) == 65535:
            return frame


def select_force_by_city_count_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """325FC: live relation/mask/ruler tests and first strict city-count maximum."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, scan=state.table_at(0xFFFFE640).cursor(), candidates=state.table_at(0x32660).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF376, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 4)
    frame = first_replace(frame, candidates=frame.candidates.advance(s16(low16(frame.target_x))))
    frame = _movement_move(state, frame, 'count', 0, 16)
    frame = _movement_move(state, frame, 'distance', 65535, 16)
    frame = _movement_move(state, frame, 'target_x', 13, 16)
    frame = _movement_move(state, frame, 'offset_x', state.read(0xFFFFF376, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'offset_x', 1)
    frame = first_replace(frame, controller=state.table_at(0xFFFFE710))
    frame = _movement_move(state, frame, 'offset_x', frame.controller.word(low16(frame.offset_x)), 16)
    while True:
        frame = first_replace(frame, candidates=frame.candidates.advance(-1))
        frame = _movement_compare(state, frame, frame.candidates.byte(), 1, 8)
        eligible = bool(frame.status & 5)
        if eligible:
            frame = test_ai_register_bit_fields(state, frame, frame.offset_x, low16(frame.target_x))
            eligible = bool(frame.status & 4)
        if eligible:
            frame = _movement_move(state, frame, 'offset_y', low16(frame.target_x), 16)
            frame = _movement_fixed_shift_word(state, frame, 'offset_y', 1)
            frame = _movement_test(state, frame, frame.scan.word(low16(frame.offset_y)), 16)
            eligible = not bool(frame.status & 8)
        if eligible:
            frame = call_scene_ai_fields(state, frame, 0x325E4, 0x32642)
            frame = _movement_compare(state, frame, low16(frame.target_y), low16(frame.count), 16)
            if not frame.status & 5:
                frame = _movement_move(state, frame, 'count', low16(frame.target_y), 16)
                frame = _movement_move(state, frame, 'distance', low16(frame.target_x), 16)
        frame = step_ai_count_fields(frame, 'target_x')
        if low16(frame.target_x) == 65535:
            return frame
