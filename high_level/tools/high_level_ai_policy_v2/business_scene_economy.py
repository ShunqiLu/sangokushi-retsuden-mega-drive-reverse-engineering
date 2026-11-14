"""Whole-frame resource support and training-choice policies.

The support requirement's actual A4 rebind deliberately affects the next city
filter; repeated gold/rice reads stay live, with original unsigned wrapping.
"""
from ..high_level_scene_flows.domain import SceneState, u16, u32, low8, low16, divu_retained
from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame, first_replace
from ..high_level_main_flows.business_movement_support import _movement_frame, _movement_move, _movement_move_long, _movement_test, _movement_compare, _movement_fixed_shift_word, _movement_save_longs, _movement_restore_longs
from ..high_level_ai_decision.scene_fields import store_ai_value_fields, adjust_ai_carrier_fields, compare_ai_long_fields, shift_ai_long_fields, test_ai_register_bit_fields, step_ai_count_fields, call_scene_ai_fields


def estimate_city_troop_requirement_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """324AC: actual256 predecrement assignments, margin100 and packed division."""
    frame = _movement_frame(state, frame)
    frame = _movement_save_longs(state, frame, ('distance',))
    frame = first_replace(frame, opponent=state.table_at(0xFFFFCD00))
    frame = _movement_move(state, frame, 'offset_x', 255, 16)
    frame = _movement_move_long(state, frame, 'offset_y', 0)
    while True:
        frame = first_replace(frame, opponent=frame.opponent.advance(-1))
        frame = _movement_move(state, frame, 'choice', frame.opponent.byte(), 8)
        frame = _movement_move(state, frame, 'choice', low16(frame.choice) & 63, 16)
        frame = _movement_compare(state, frame, low16(frame.choice), low16(frame.count), 16)
        if frame.status & 4:
            frame = _movement_move(state, frame, 'distance', low16(frame.offset_x), 16)
            frame = _movement_fixed_shift_word(state, frame, 'distance', 2)
            frame = adjust_ai_carrier_fields(state, frame, 'offset_y', frame.roster.long(low16(frame.distance)), 32)
            frame = adjust_ai_carrier_fields(state, frame, 'offset_y', 100, 32)
        frame = step_ai_count_fields(frame, 'offset_x')
        if low16(frame.offset_x) == 65535:
            break
    packed = divu_retained(frame.offset_y, 10)
    # The original following ANDI.L overrides undefined DIVU overflow NZVC.
    frame = _movement_move_long(state, frame, 'offset_y', low16(packed))
    frame = _movement_move_long(state, frame, 'distance', frame.offset_y)
    frame = shift_ai_long_fields(state, frame, 'offset_y', 3)
    frame = adjust_ai_carrier_fields(state, frame, 'offset_y', frame.distance, 32)
    return _movement_restore_longs(state, frame, ('distance',))


def select_resource_support_city_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3244A: choose the deficient allied city's minimum wrapped cash+rice."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF376, 2), 16)
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF364, 2), 16)
    frame = first_replace(frame, roster=state.table_at(0xFFFFC800).cursor(), candidates=state.table_at(0xFFFFDFFC).cursor(), controller=state.table_at(0xFFFFE09C), opponent=state.table_at(0xFFFFEA37))
    frame = _movement_move_long(state, frame, 'unit', 0xFFFFFFFF)
    frame = _movement_move(state, frame, 'distance', 65535, 16)
    frame = first_replace(frame, scan=state.table_at(0xFFFFF450).cursor())
    frame = _movement_move(state, frame, 'count', 40, 16)
    while True:
        frame = first_replace(frame, scan=frame.scan.advance(-1))
        frame = _movement_compare(state, frame, low8(frame.target_x), frame.scan.byte(), 8)
        eligible = bool(frame.status & 4)
        if eligible:
            frame = _movement_test(state, frame, frame.opponent.byte(low16(frame.count)), 8)
            eligible = bool(frame.status & 4)
        if eligible:
            frame = _movement_compare(state, frame, low16(frame.count), low16(frame.target_y), 16)
            eligible = not bool(frame.status & 4)
        if eligible:
            frame = call_scene_ai_fields(state, frame, 0x324AC, 0x32488)
            frame = _movement_move(state, frame, 'offset_x', low16(frame.count), 16)
            frame = _movement_fixed_shift_word(state, frame, 'offset_x', 2)
            frame = compare_ai_long_fields(state, frame, frame.offset_y, frame.controller.long(low16(frame.offset_x)))
            if not frame.status & 5:
                frame = _movement_move_long(state, frame, 'choice', frame.candidates.long(low16(frame.offset_x)))
                frame = adjust_ai_carrier_fields(state, frame, 'choice', frame.controller.long(low16(frame.offset_x)), 32)
                frame = compare_ai_long_fields(state, frame, frame.choice, frame.unit)
                if frame.status & 1:
                    frame = _movement_move_long(state, frame, 'unit', frame.choice)
                    frame = _movement_move(state, frame, 'distance', low16(frame.count), 16)
        # SUBQ.W/BNE, not DBRA: the final zero WORD and flags are observable.
        frame = adjust_ai_carrier_fields(state, frame, 'count', 1, subtract=True)
        if frame.status & 4:
            return frame


def plan_force_support_action_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """32592: real RNG/city-count candidate and unchanged original lottery."""
    frame = _movement_frame(state, frame)
    frame = call_scene_ai_fields(state, frame, 0x83D4, 0x32598)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF376, 2), 16)
    frame = call_scene_ai_fields(state, frame, 0x325E4, 0x325A0)
    frame = _movement_move(state, frame, 'choice', low16(frame.target_y), 16)
    frame = call_scene_ai_fields(state, frame, 0x325FC, 0x325A6)
    frame = _movement_test(state, frame, low16(frame.distance), 16)
    if not frame.status & 8:
        frame = _movement_move(state, frame, 'target_y', 2, 16)
        frame = _movement_compare(state, frame, low16(frame.count), low16(frame.choice), 16)
        if frame.status & 5:
            frame = _movement_move(state, frame, 'target_y', 1, 16)
        frame = _movement_move_long(state, frame, 'target_x', 0)
        frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF61C, 2), 16)
        frame = shift_ai_long_fields(state, frame, 'target_x', 3)
        frame = _movement_move_long(state, frame, 'target_x', u32(frame.target_x << 16 | frame.target_x >> 16))
        frame = _movement_compare(state, frame, low16(frame.target_x), low16(frame.target_y), 16)
        if frame.status & 1:
            frame = store_ai_value_fields(state, frame, 0xFFFFE730, low16(frame.distance), 16)
            frame = store_ai_value_fields(state, frame, 0xFFFFF3E0, 0, 16, True)
            return store_ai_value_fields(state, frame, 0xFFFFF728, 7, 16)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 2, 16)


def choose_resource_action_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3324C: current-city gold>=10000 chooses7, otherwise4."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFDFFC).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    frame = compare_ai_long_fields(state, frame, frame.roster.long(low16(frame.target_x)), 10000)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 4 if frame.status & 1 else 7, 16)


def select_roster_training_min_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33292: WORD comparison after clearing D3.W, unlike33574's BYTE minimum."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF72A).cursor(), candidates=state.table_at(0xFFFFC500).cursor())
    frame = _movement_move(state, frame, 'target_x', 65535, 16)
    frame = _movement_move(state, frame, 'target_y', 65535, 16)
    frame = _movement_move(state, frame, 'count', 0, 16)
    while True:
        token = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'unit', token, 16)
        if frame.status & 8:
            return frame
        frame = test_ai_register_bit_fields(state, frame, frame.unit, 14)
        if not frame.status & 4:
            continue
        frame = _movement_move(state, frame, 'count', frame.candidates.byte(low16(frame.unit)), 8)
        frame = _movement_compare(state, frame, low16(frame.count), low16(frame.target_x), 16)
        if not frame.status & 1:
            continue
        frame = _movement_move(state, frame, 'target_x', low16(frame.count), 16)
        frame = _movement_move(state, frame, 'target_y', low16(frame.unit), 16)


def choose_training_action_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33274: original best training value<80 chooses8, otherwise9."""
    frame = _movement_frame(state, frame)
    frame = call_scene_ai_fields(state, frame, 0x33292, 0x33278)
    frame = _movement_compare(state, frame, low16(frame.target_x), 80, 16)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 8 if frame.status & 1 else 9, 16)
