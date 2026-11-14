"""Complete live neighbor selection and departure-head policies.

confirmed source: dispatch_descendants.s338EC..33AB8 and33D92..33DAA.
This fragment is assembled with the two separately owned march fragments.
"""
from ..high_level_scene_flows.domain import SceneState, low8, low16, s16, u8, u16, u32, replace_byte, replace_word
from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame, FirstDeploymentReturnBoundary, first_replace
from ..high_level_main_flows.business_movement_support import (
    _movement_frame, _movement_move, _movement_move_long, _movement_test, _movement_test_long,
    _movement_compare, _movement_fixed_shift_word, _movement_shift_long,
    _movement_binary_flags, _movement_arithmetic_long, _movement_multiply_word,
    _movement_divu_word, _movement_save_longs, _movement_restore_longs, _path_carry_fields,
)
from ..high_level_ai_decision.scene_fields import (
    store_ai_value_fields, adjust_ai_carrier_fields, compare_ai_long_fields,
    shift_ai_long_fields, set_ai_flag_byte_fields, test_ai_register_bit_fields, step_ai_count_fields,
)


def choose_neighbor_relation_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """338EC: a hostile neighboring city chooses phase4, otherwise phase2."""
    frame = _movement_frame(state, frame)
    frame = _march_call_fields(state, frame, 0x33906, 0x338F0)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 4 if frame.status & 1 else 2, 16)


def hostile_neighbor_exists_carry_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33906: scan the BYTE neighbor row against the once-captured force WORD."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xD4BDA).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 3)
    frame = first_replace(frame, roster=frame.roster.advance(s16(low16(frame.target_x))))
    frame = first_replace(frame, candidates=state.table_at(0xFFFFF427).cursor())
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF376, 2), 16)
    while True:
        value = frame.roster.byte()
        frame = first_replace(frame, roster=frame.roster.advance(1))
        frame = _movement_move(state, frame, 'target_x', value, 8)
        if frame.status & 8:
            return _path_carry_fields(state, frame, 0, 0x33938)
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 255, 16)
        frame = _movement_move(state, frame, 'unit', frame.candidates.byte(low16(frame.target_x)), 8)
        if frame.status & 8:
            continue
        frame = _movement_compare(state, frame, low8(frame.unit), low8(frame.target_y), 8)
        if not frame.status & 4:
            return _path_carry_fields(state, frame, 1, 0x33930)


def choose_unowned_neighbor_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3393E: first unowned neighboring city chooses phase3, otherwise phase9."""
    frame = _movement_frame(state, frame)
    frame = _march_call_fields(state, frame, 0x33958, 0x33942)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 3 if frame.status & 1 else 9, 16)


def unowned_neighbor_exists_carry_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33958: preserve the terminator/owner TST flags before the SR C-bit write."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xD4BDA).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 3)
    frame = first_replace(frame, roster=frame.roster.advance(s16(low16(frame.target_x))))
    frame = first_replace(frame, candidates=state.table_at(0xFFFFF427).cursor())
    while True:
        value = frame.roster.byte()
        frame = first_replace(frame, roster=frame.roster.advance(1))
        frame = _movement_move(state, frame, 'target_x', value, 8)
        if frame.status & 8:
            return _path_carry_fields(state, frame, 0, 0x33982)
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 255, 16)
        frame = _movement_test(state, frame, frame.candidates.byte(low16(frame.target_x)), 8)
        if frame.status & 8:
            return _path_carry_fields(state, frame, 1, 0x3397A)


def choose_roster_troop_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33988: the complete roster count is compared with3, unsigned."""
    frame = _movement_frame(state, frame)
    frame = _march_call_fields(state, frame, 0x339A6, 0x3398C)
    frame = _movement_compare(state, frame, low16(frame.target_x), 3, 16)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 9 if frame.status & 1 else 7, 16)


def count_roster_large_troops_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """339A6: count live LONG troop values, keeping each WORD roster carrier."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF72A).cursor())
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFC800).cursor())
    while True:
        value = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'target_y', value, 16)
        if frame.status & 8:
            return frame
        frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 255, 16)
        frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
        frame = compare_ai_long_fields(state, frame, frame.candidates.long(low16(frame.target_y)), 5000)
        if not frame.status & 1:
            frame = adjust_ai_carrier_fields(state, frame, 'target_x', 1)


def choose_random_neighbor_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """339CC: a real RNG call followed by bit2 and the actual unowned test."""
    frame = _movement_frame(state, frame)
    frame = _march_call_fields(state, frame, 0x83D4, 0x339D2)
    frame = test_ai_register_bit_fields(state, frame, frame.target_x, 2)
    if not frame.status & 4:
        frame = _march_call_fields(state, frame, 0x33958, 0x339DE)
        if frame.status & 1:
            return store_ai_value_fields(state, frame, 0xFFFFF728, 5, 16)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 6, 16)


def choose_roster_troop_phase_five_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """339F4: same complete troop counter with the distinct5 threshold."""
    frame = _movement_frame(state, frame)
    frame = _march_call_fields(state, frame, 0x339A6, 0x339F6)
    frame = _movement_compare(state, frame, low16(frame.target_x), 5, 16)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 9 if frame.status & 1 else 7, 16)


def evaluate_neighbor_march_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33A10: preserve the home totals in D6/D7 while visiting real neighbors."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = _march_call_fields(state, frame, 0x33A36, 0x33A18)
    frame = _movement_move_long(state, frame, 'offset_y', frame.target_y)
    frame = _movement_move(state, frame, 'choice', low16(frame.unit), 16)
    frame = _march_call_fields(state, frame, 0x33A70, 0x33A20)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 8 if frame.status & 1 else 9, 16)


def sum_city_officer_troops_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33A36: backward256-member sum, real MOVEM and low-WORD qualifying test."""
    frame = _movement_frame(state, frame)
    names = ('count', 'distance', 'roster', 'candidates')
    frame = _movement_save_longs(state, frame, names)
    frame = first_replace(frame, roster=state.table_at(0xFFFFCC00).cursor())
    frame = _movement_move_long(state, frame, 'target_y', 0)
    frame = _movement_move(state, frame, 'unit', 0, 16)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFC800).cursor())
    frame = _movement_move(state, frame, 'count', 255, 16)
    while True:
        frame = _movement_compare(state, frame, low8(frame.target_x), frame.roster.byte(low16(frame.count)), 8)
        if frame.status & 4:
            frame = _movement_move(state, frame, 'distance', low16(frame.count), 16)
            frame = _movement_fixed_shift_word(state, frame, 'distance', 2)
            frame = _movement_move_long(state, frame, 'distance', frame.candidates.long(low16(frame.distance)))
            frame = _movement_arithmetic_long(state, frame, 'target_y', frame.distance, False)
            frame = _movement_compare(state, frame, low16(frame.distance), 5000, 16)
            if not frame.status & 1:
                frame = adjust_ai_carrier_fields(state, frame, 'unit', 1)
        frame = step_ai_count_fields(frame, 'count')
        if low16(frame.count) == 65535:
            break
    return _movement_restore_longs(state, frame, names)


def choose_weaker_enemy_neighbor_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33A70: retain the first weaker hostile neighbor, including live force rereads."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, controller=state.table_at(0xD4BDA))
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 3)
    frame = first_replace(frame, controller=frame.controller.advance(s16(low16(frame.target_x))))
    frame = first_replace(frame, scan=state.table_at(0xFFFFF427).cursor())
    while True:
        value = frame.controller.byte()
        frame = first_replace(frame, controller=frame.controller.advance(1))
        frame = _movement_move(state, frame, 'target_x', value, 8)
        if frame.status & 8:
            return _path_carry_fields(state, frame, 0, 0x33AB2)
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 255, 16)
        frame = _movement_move(state, frame, 'offset_x', frame.scan.byte(low16(frame.target_x)), 8)
        if frame.status & 8:
            continue
        frame = _movement_compare(state, frame, low8(frame.offset_x), state.read(0xFFFFF377, 1), 8)
        if frame.status & 4:
            continue
        frame = _march_call_fields(state, frame, 0x33A36, 0x33A9A)
        frame = compare_ai_long_fields(state, frame, frame.target_y, frame.offset_y)
        if not frame.status & 1:
            continue
        frame = _movement_compare(state, frame, low16(frame.unit), low16(frame.choice), 16)
        if not frame.status & 5:
            continue
        frame = store_ai_value_fields(state, frame, 0xFFFFF392, low16(frame.target_x), 16)
        frame = store_ai_value_fields(state, frame, 0xFFFFF744, low16(frame.unit), 16)
        return _path_carry_fields(state, frame, 1, 0x33AAA)


def restore_departing_city_head_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33D92: copy the remaining roster through its negative terminator, then E1F6."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF500).cursor())
    frame = first_replace(frame, candidates=state.table_at(0xFFFFF72E).cursor())
    while True:
        value = frame.candidates.word()
        frame = first_replace(frame, candidates=frame.candidates.advance(2))
        frame = store_ai_value_fields(state, frame, frame.roster.base, value, 16)
        frame = first_replace(frame, roster=frame.roster.advance(2))
        if frame.status & 8:
            break
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    return _march_call_fields(state, frame, 0xE1F6, 0x33DA8)


def commit_unowned_neighbor_march_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33AB8: live best route, both troop gates, food debit and departure flags."""
    frame = _movement_frame(state, frame)
    frame = _march_call_fields(state, frame, 0x33B6C, 0x33ABC)
    frame = store_ai_value_fields(state, frame, 0xFFFFF644, low16(frame.target_x), 16)
    frame = store_ai_value_fields(state, frame, 0xFFFFF392, low16(frame.target_y), 16)
    frame = _march_call_fields(state, frame, 0x33666, 0x33AC8)
    frame = first_replace(frame, roster=state.table_at(0xFFFFC800).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF72A, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    frame = compare_ai_long_fields(state, frame, frame.roster.long(low16(frame.target_x)), 5000)
    fund_departure = not bool(frame.status & 1)
    if fund_departure:
        frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF72C, 2), 16)
        frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
        frame = compare_ai_long_fields(state, frame, frame.roster.long(low16(frame.target_x)), 5000)
        fund_departure = not bool(frame.status & 1)
    if fund_departure:
        frame = _march_call_fields(state, frame, 0x33BE8, 0x33AF4)
        frame = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)
        frame = store_ai_value_fields(state, frame, 0xFFFFF3BA, frame.target_x, 32)
        frame = first_replace(frame, roster=state.table_at(0xFFFFE09C).cursor())
        frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
        frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
        frame = _movement_move_long(state, frame, 'target_y', frame.roster.long(low16(frame.target_x)))
        frame = compare_ai_long_fields(state, frame, frame.target_y, state.read(0xFFFFF3BA, 4))
        if not frame.status & 1:
            frame = _movement_move_long(state, frame, 'target_y', state.read(0xFFFFF3BA, 4))
            address = frame.roster.address(low16(frame.target_x))
            previous = state.read(address, 4)
            frame, remaining = _movement_binary_flags(state, frame, previous, frame.target_y, 32, True)
            state.write(address, 4, remaining)
            frame = _march_call_fields(state, frame, 0x33C3A, 0x33B20)
            frame = _march_call_fields(state, frame, 0x33CC8, 0x33B24)
            frame = first_replace(frame, roster=state.table_at(0xFFFFCC00).cursor())
            for address in (0xFFFFF72A, 0xFFFFF72C):
                frame = _movement_move(state, frame, 'target_x', state.read(address, 2), 16)
                frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 255, 16)
                frame = set_ai_flag_byte_fields(state, frame, frame.roster.address(low16(frame.target_x)), 6)
    frame = first_replace(frame, roster=state.table_at(0xFFFFCC00).cursor(),
        candidates=state.table_at(0xFFFFF45E).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
    frame = _movement_move(state, frame, 'target_x', frame.candidates.word(low16(frame.target_x)), 16)
    frame = test_ai_register_bit_fields(state, frame, frame.roster.byte(low16(frame.target_x)), 6)
    if not frame.status & 4:
        frame = _march_call_fields(state, frame, 0x33D92, 0x33B64)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 9, 16)


def shortest_unowned_neighbor_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33B6C: original live candidate scan and six-LONG save around651C."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xD4BDA).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 3)
    frame = first_replace(frame, roster=frame.roster.advance(s16(low16(frame.target_x))),
        candidates=state.table_at(0xD4AC6).cursor())
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1, True)
    frame = _movement_move(state, frame, 'target_y', frame.candidates.word(low16(frame.target_x), 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 4, True)
    frame = store_ai_value_fields(state, frame, 0xFFFFF63C, low16(frame.target_y), 16)
    frame = _movement_move(state, frame, 'target_y', frame.candidates.word(low16(frame.target_x)), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 4, True)
    frame = store_ai_value_fields(state, frame, 0xFFFFF63E, low16(frame.target_y), 16)
    frame = _movement_move(state, frame, 'target_x', 65535, 16)
    frame = _movement_move(state, frame, 'target_y', 65535, 16)
    frame = first_replace(frame, controller=state.table_at(0xFFFFF427).cursor())
    while True:
        neighbor = frame.roster.byte()
        frame = first_replace(frame, roster=frame.roster.advance(1))
        frame = _movement_move(state, frame, 'unit', neighbor, 8)
        if frame.status & 8:
            return frame
        frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 255, 16)
        frame = _movement_test(state, frame, frame.controller.byte(low16(frame.unit)), 8)
        if not frame.status & 8:
            continue
        frame = _movement_fixed_shift_word(state, frame, 'unit', 2)
        frame = _movement_move(state, frame, 'count', frame.candidates.word(low16(frame.unit), 2), 16)
        frame = _movement_fixed_shift_word(state, frame, 'count', 4, True)
        frame = store_ai_value_fields(state, frame, 0xFFFFF640, low16(frame.count), 16)
        frame = _movement_move(state, frame, 'count', frame.candidates.word(low16(frame.unit)), 16)
        frame = _movement_fixed_shift_word(state, frame, 'count', 4, True)
        frame = store_ai_value_fields(state, frame, 0xFFFFF642, low16(frame.count), 16)
        saved = ('target_x', 'target_y', 'unit', 'roster', 'candidates', 'controller')
        frame = _movement_save_longs(state, frame, saved)
        frame = _march_call_fields(state, frame, 0x651C, 0x33BD2)
        frame = _movement_restore_longs(state, frame, saved)
        frame = _movement_compare(state, frame, low16(frame.target_x), state.read(0xFFFFF644, 2), 16)
        if frame.status & 5:
            continue
        # The original improvement path performs a second independent read.
        frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF644, 2), 16)
        frame = _movement_fixed_shift_word(state, frame, 'unit', 2, True)
        frame = _movement_move(state, frame, 'target_y', low16(frame.unit), 16)


def price_two_officer_march_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33BE8: two troops, wrapped BYTE speed mean, retained DIVU and MULU."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFC800).cursor())
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF72A, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
    frame = _movement_move_long(state, frame, 'target_x', frame.roster.long(low16(frame.target_y)))
    frame = _movement_move(state, frame, 'unit', state.read(0xFFFFF72C, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'unit', 2)
    frame = adjust_ai_carrier_fields(state, frame, 'target_x', frame.roster.long(low16(frame.unit)), 32)
    frame = adjust_ai_carrier_fields(state, frame, 'target_x', 200, 32)
    frame = _movement_divu_word(state, frame, 'target_x', 10, 0x33C06)
    frame = _movement_multiply_word(state, frame, 'target_x', 3)
    for carrier in ('target_y', 'unit'):
        frame = _movement_fixed_shift_word(state, frame, carrier, 2, True)
    frame = first_replace(frame, roster=state.table_at(0xFFFFC400).cursor())
    frame = _movement_move(state, frame, 'count', frame.roster.byte(low16(frame.target_y)), 8)
    frame = adjust_ai_carrier_fields(state, frame, 'count', frame.roster.byte(low16(frame.unit)), 8)
    frame = _movement_move(state, frame, 'count', low16(frame.count) & 255, 16)
    frame = _movement_fixed_shift_word(state, frame, 'count', 1, True)
    frame = store_ai_value_fields(state, frame, 0xFFFFF744, low16(frame.count), 16)
    frame = _movement_move_long(state, frame, 'distance', 0)
    frame = _movement_move(state, frame, 'distance', state.read(0xFFFFF644, 2), 16)
    frame = adjust_ai_carrier_fields(state, frame, 'distance', low16(frame.count))
    frame = adjust_ai_carrier_fields(state, frame, 'distance', 1, subtract=True)
    frame = _movement_divu_word(state, frame, 'distance', low16(frame.count), 0x33C32)
    frame = adjust_ai_carrier_fields(state, frame, 'distance', 3)
    return _movement_multiply_word(state, frame, 'target_x', low16(frame.distance))


def append_two_officer_march_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33C3A: actual zero-nibble tail, ordered origin/resource/member BYTEs."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFF9000).cursor())
    while True:
        frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
        if frame.status & 4:
            break
        frame = first_replace(frame, roster=frame.roster.advance(s16(low16(frame.target_x)) + 13))
    frame = store_ai_value_fields(state, frame, frame.roster.base, 0x22, 8)
    frame = first_replace(frame, candidates=state.table_at(0xD4AC6).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    for displacement, address, packet_offset in ((2, 0xFFFFF746, 1), (0, 0xFFFFF748, 2)):
        frame = _movement_move(state, frame, 'target_y', frame.candidates.word(low16(frame.target_x), displacement), 16)
        frame = store_ai_value_fields(state, frame, address, low16(frame.target_y), 16)
        frame = _movement_fixed_shift_word(state, frame, 'target_y', 4, True)
        frame = store_ai_value_fields(state, frame, frame.roster.address(0, packet_offset), low8(frame.target_y), 8)
    for source, offset in ((0xFFFFF745, 3), (0xFFFFF377, 4)):
        frame = store_ai_value_fields(state, frame, frame.roster.address(0, offset), state.read(source, 1), 8)
    for offset in (5, 6, 7, 8):
        frame = store_ai_value_fields(state, frame, frame.roster.address(0, offset), 0, 8, True)
    frame = _movement_move_long(state, frame, 'target_y', state.read(0xFFFFF3BA, 4))
    frame = store_ai_value_fields(state, frame, frame.roster.address(0, 12), low8(frame.target_y), 8)
    for offset in (11, 10):
        frame = _movement_shift_long(state, frame, 'target_y', True)
        frame = store_ai_value_fields(state, frame, frame.roster.address(0, offset), low8(frame.target_y), 8)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 8, True)
    frame = store_ai_value_fields(state, frame, frame.roster.address(0, 9), low8(frame.target_y), 8)
    frame = store_ai_value_fields(state, frame, frame.roster.address(0, 13), state.read(0xFFFFF72B, 1), 8)
    frame = store_ai_value_fields(state, frame, 0xFFFFF74A, state.read(0xFFFFF72A, 2), 16)
    frame = store_ai_value_fields(state, frame, frame.roster.address(0, 14), state.read(0xFFFFF72D, 1), 8)
    return store_ai_value_fields(state, frame, frame.roster.address(0, 15), 0, 8, True)


def build_ai_movement_packet_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33CC8: real6518 path then original queue header and33D0E child."""
    frame = _movement_frame(state, frame)
    for source, destination in ((4294965062, 4294964796), (4294965064, 4294964798)):
        frame = store_ai_value_fields(state, frame, destination, state.read(source, 2), 16)
    frame = first_replace(frame, roster=state.table_at(871110).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(4294964114, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    frame = store_ai_value_fields(state, frame, 4294964800, frame.roster.word(low16(frame.target_x), 2), 16)
    frame = store_ai_value_fields(state, frame, 4294964802, frame.roster.word(low16(frame.target_x)), 16)
    frame = _march_call_fields(state, frame, 25880, 212210)
    return append_ai_movement_packet_header_fields(state, frame)


def append_ai_path_steps_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33D0E: actual path BYTEs, retained direction WORD and low-BYTE budget."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF744, 2), 16)
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF746, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 4, True)
    frame = _movement_move(state, frame, 'unit', state.read(0xFFFFF748, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'unit', 4, True)
    frame = _movement_move(state, frame, 'offset_y', 4, 16)
    frame = first_replace(frame, scan=state.table_at(0xEE5F0).cursor(),
        opponent=state.table_at(0x670A).cursor(), candidates=state.table_at(0x00FF4000).cursor())
    while True:
        value = frame.candidates.byte()
        frame = first_replace(frame, candidates=frame.candidates.advance(1))
        frame = _movement_move(state, frame, 'count', value, 8)
        if frame.status & 8:
            break
        # Original33D3A PC-relative LEA is33D3C+002C=33D68, not33D6C.
        frame = first_replace(frame, controller=state.table_at(0x33D68).cursor())
        frame = _movement_fixed_shift_word(state, frame, 'count', 2)
        frame = adjust_ai_carrier_fields(state, frame, 'target_y', frame.controller.word(low16(frame.count)))
        frame = adjust_ai_carrier_fields(state, frame, 'unit', frame.controller.word(low16(frame.count), 2))
        frame = _movement_fixed_shift_word(state, frame, 'count', 2, True)
        frame = _march_call_fields(state, frame, 0x33D7C, 0x33D4E)
        frame = adjust_ai_carrier_fields(state, frame, 'target_x', low8(frame.distance), 8, True)
        if frame.status & 1:
            break
        frame = adjust_ai_carrier_fields(state, frame, 'offset_y', 1)
        frame = store_ai_value_fields(state, frame, frame.roster.base, low8(frame.count), 8)
        frame = first_replace(frame, roster=frame.roster.advance(1))
        frame = _movement_test(state, frame, low8(frame.target_x), 8)
        if frame.status & 4:
            break
    frame = store_ai_value_fields(state, frame, frame.roster.base, 0, 8, True)
    frame = store_ai_value_fields(state, frame, frame.roster.address(0, 1), 255, 8)
    address = 0x00FF3826
    frame, length = _movement_binary_flags(state, frame, state.read(address, 2), low16(frame.offset_y), 16)
    state.write(address, 2, length)
    return frame


def read_path_step_cost_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33D7C: exact wrapped WORD grid index and two original indexed BYTE reads."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'distance', low16(frame.target_y), 16)
    frame = _movement_fixed_shift_word(state, frame, 'distance', 3)
    frame = adjust_ai_carrier_fields(state, frame, 'distance', low16(frame.target_y))
    frame = _movement_fixed_shift_word(state, frame, 'distance', 3)
    frame = adjust_ai_carrier_fields(state, frame, 'distance', low16(frame.unit))
    frame = _movement_move(state, frame, 'offset_x', 0, 16)
    frame = _movement_move(state, frame, 'offset_x', frame.scan.byte(low16(frame.distance)), 8)
    return _movement_move(state, frame, 'distance', frame.opponent.byte(low16(frame.offset_x)), 8)


def _support_read_roster_word_fields(state, frame, pointer, carrier):
    source = getattr(frame, pointer)
    value = source.word()
    frame = first_replace(frame, **{pointer: source.advance(2)})
    return _movement_move(state, frame, carrier, value, 16)


def _support_phase_done_fields(state, frame):
    return store_ai_value_fields(state, frame, 0xFFFFF728, 65535, 16)


def commit_support_march_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33DAA: gate, choose, fund and commit one support departure.

    Food admission is strictly greater, not greater-or-equal. Funds are read
    and settled in the original order; selected full WORD identities are not
    narrowed before their departure bits are changed.
    """
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF762, 2), 16)
    frame = _movement_compare(state, frame, low16(frame.target_x), 3, 16)
    if frame.status & 1:
        return _support_phase_done_fields(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFDFFC).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    frame = _movement_move_long(state, frame, 'target_x', frame.roster.long(low16(frame.target_x)))
    frame = compare_ai_long_fields(state, frame, frame.target_x, 2000)
    if frame.status & 1:
        return _support_phase_done_fields(state, frame)
    frame = shift_ai_long_fields(state, frame, 'target_x', 1, True)
    frame = store_ai_value_fields(state, frame, 0xFFFFF39E, frame.target_x, 32)
    frame = _march_call_fields(state, frame, 0x33E5E, 0x33DD8)
    if frame.status & 1:
        return _support_phase_done_fields(state, frame)
    frame = _march_call_fields(state, frame, 0x33F0A, 0x33DE0)
    frame = _movement_test(state, frame, state.read(0xFFFFD300, 2), 16)
    if frame.status & 8:
        return _support_phase_done_fields(state, frame)
    frame = _march_call_fields(state, frame, 0x33FAA, 0x33DEC)
    frame = first_replace(frame, roster=state.table_at(0xFFFFE09C).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    frame = _movement_move_long(state, frame, 'target_y', frame.roster.long(low16(frame.target_x)))
    frame = compare_ai_long_fields(state, frame, frame.target_y, state.read(0xFFFFF3BA, 4))
    if frame.status & 5:
        return _support_phase_done_fields(state, frame)
    frame = _movement_arithmetic_long(state, frame, 'target_y', state.read(0xFFFFF3BA, 4), True)
    frame = store_ai_value_fields(state, frame, frame.roster.address(low16(frame.target_x)), frame.target_y, 32)
    frame = first_replace(frame, roster=state.table_at(0xFFFFDFFC).cursor())
    frame = _movement_move_long(state, frame, 'target_y', frame.roster.long(low16(frame.target_x)))
    frame = _movement_arithmetic_long(state, frame, 'target_y', state.read(0xFFFFF39E, 4), True)
    frame = store_ai_value_fields(state, frame, frame.roster.address(low16(frame.target_x)), frame.target_y, 32)
    frame = _march_call_fields(state, frame, 0x34030, 0x33E1E)
    frame = _march_call_fields(state, frame, 0x33CC8, 0x33E22)
    frame = first_replace(frame, roster=state.table_at(0xFFFFD300).cursor(),
        candidates=state.table_at(0xFFFFCC00).cursor())
    while True:
        frame = _support_read_roster_word_fields(state, frame, 'roster', 'target_x')
        if frame.status & 8:
            break
        frame = set_ai_flag_byte_fields(state, frame, frame.candidates.address(low16(frame.target_x)), 6)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF45E).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
    frame = _movement_move(state, frame, 'target_y', frame.roster.word(low16(frame.target_y)), 16)
    frame = test_ai_register_bit_fields(state, frame, frame.candidates.byte(low16(frame.target_y)), 6)
    if not frame.status & 4:
        frame = _march_call_fields(state, frame, 0x340D8, 0x33E56)
    return _support_phase_done_fields(state, frame)


def collect_support_officers_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33E5E: live eligibility and the original inverted partial-sort loop."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF72A).cursor(),
        candidates=state.table_at(0xFFFFF500).cursor(),
        controller=state.table_at(0xFFFFC800).cursor(),
        scan=state.table_at(0xFFFFB400).cursor(),
        opponent=state.table_at(0xFFFFD300).cursor(),
        scratch=state.table_at(0xFFFFB200).cursor(),
        auxiliary=state.table_at(0xFFFFB000).cursor())
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    while True:
        frame = _support_read_roster_word_fields(state, frame, 'roster', 'target_y')
        if frame.status & 8:
            break
        frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 255, 16)
        frame = _movement_move(state, frame, 'unit', low16(frame.target_y), 16)
        frame = _movement_fixed_shift_word(state, frame, 'unit', 2)
        frame = compare_ai_long_fields(state, frame, frame.controller.long(low16(frame.unit)), 5000)
        if frame.status & 1:
            continue
        frame = _movement_fixed_shift_word(state, frame, 'unit', 1, True)
        frame = _movement_move_long(state, frame, 'count', frame.scratch.long(low16(frame.unit)))
        frame = compare_ai_long_fields(state, frame, frame.count, frame.auxiliary.long(low16(frame.unit)))
        if frame.status & 1:
            continue
        frame = store_ai_value_fields(state, frame, frame.candidates.base, low16(frame.target_y), 16)
        frame = first_replace(frame, candidates=frame.candidates.advance(2))
        strength = frame.scan.word(low16(frame.unit))
        frame = store_ai_value_fields(state, frame, frame.opponent.base, strength, 16)
        frame = first_replace(frame, opponent=frame.opponent.advance(2))
        frame = adjust_ai_carrier_fields(state, frame, 'target_x', 2)
    frame = store_ai_value_fields(state, frame, frame.candidates.base, 65535, 16)
    for address in (0xFFFFF500, 0xFFFFF502):
        frame = _movement_test(state, frame, state.read(address, 2), 16)
        if frame.status & 8:
            return _path_carry_fields(state, frame, True, 0x33F04)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFF500).cursor(),
        controller=state.table_at(0xFFFFD300).cursor())
    while True:
        frame = _movement_move(state, frame, 'target_y', 2, 16)
        while True:
            frame = _movement_move(state, frame, 'unit', frame.controller.word(low16(frame.target_y), -2), 16)
            frame = _movement_compare(state, frame, low16(frame.unit), frame.controller.word(low16(frame.target_y)), 16)
            if frame.status & 1:
                value = frame.controller.word(low16(frame.target_y))
                frame = store_ai_value_fields(state, frame, frame.controller.address(low16(frame.target_y), -2), value, 16)
                frame = store_ai_value_fields(state, frame, frame.controller.address(low16(frame.target_y)), low16(frame.unit), 16)
                frame = _movement_move(state, frame, 'unit', frame.candidates.word(low16(frame.target_y), -2), 16)
                value = frame.candidates.word(low16(frame.target_y))
                frame = store_ai_value_fields(state, frame, frame.candidates.address(low16(frame.target_y), -2), value, 16)
                frame = store_ai_value_fields(state, frame, frame.candidates.address(low16(frame.target_y)), low16(frame.unit), 16)
            frame = adjust_ai_carrier_fields(state, frame, 'target_y', 2)
            frame = _movement_compare(state, frame, low16(frame.target_y), low16(frame.target_x), 16)
            if not frame.status & 1:
                break
        frame = adjust_ai_carrier_fields(state, frame, 'target_x', 2, subtract=True)
        frame = _movement_compare(state, frame, low16(frame.target_x), 2, 16)
        if not frame.status & 1:
            break
    return _path_carry_fields(state, frame, False, 0x33EFC)


def choose_support_roster_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33F0A: retain roster count lanes and BUG024's append after terminator."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF500).cursor(),
        candidates=state.table_at(0xFFFFD300).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF744, 2), 16)
    frame = _movement_compare(state, frame, low16(frame.target_x), 2, 16)
    if frame.status & 1:
        frame = _movement_move(state, frame, 'target_x', 2, 16)
    frame = adjust_ai_carrier_fields(state, frame, 'target_x', 1)
    frame = _movement_compare(state, frame, low16(frame.target_x), state.read(0xFFFFF762, 2), 16)
    if not frame.status & 1:
        frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF762, 2), 16)
        frame = adjust_ai_carrier_fields(state, frame, 'target_x', 1, subtract=True)
    frame = _movement_compare(state, frame, low16(frame.target_x), 2, 16)
    if frame.status & 1:
        return store_ai_value_fields(state, frame, 0xFFFFD300, 65535, 16)
    frame = _movement_compare(state, frame, low16(frame.target_x), state.read(0xFFFFF744, 2), 16)
    if frame.status & 1:
        return store_ai_value_fields(state, frame, 0xFFFFD300, 65535, 16)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)
    frame = adjust_ai_carrier_fields(state, frame, 'target_x', 1, subtract=True)
    if frame.status & 1:
        return store_ai_value_fields(state, frame, 0xFFFFD300, 65535, 16)
    while True:
        value = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = store_ai_value_fields(state, frame, frame.candidates.base, value, 16)
        frame = first_replace(frame, candidates=frame.candidates.advance(2))
        frame = step_ai_count_fields(frame, 'target_x')
        if low16(frame.target_x) == 65535:
            break
    frame = store_ai_value_fields(state, frame, frame.candidates.base, 65535, 16)
    frame = first_replace(frame, roster=state.table_at(0xFFFFC700).cursor(),
        candidates=state.table_at(0xFFFFD300).cursor())
    required_found = False
    while True:
        frame = _support_read_roster_word_fields(state, frame, 'candidates', 'target_x')
        if frame.status & 8:
            break
        frame = test_ai_register_bit_fields(state, frame, frame.roster.byte(low16(frame.target_x)), 4)
        if not frame.status & 4:
            required_found = True
            break
    if not required_found:
        frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF762, 2), 16)
        frame = adjust_ai_carrier_fields(state, frame, 'target_x', 1, subtract=True)
        frame = _movement_compare(state, frame, low16(frame.target_y), low16(frame.target_x), 16)
        if frame.status & 1:
            frame = first_replace(frame, controller=state.table_at(0xFFFFF72A).cursor())
            while True:
                frame = _support_read_roster_word_fields(state, frame, 'controller', 'target_x')
                if frame.status & 8:
                    break
                frame = test_ai_register_bit_fields(state, frame, frame.roster.byte(low16(frame.target_x)), 4)
                if frame.status & 4:
                    continue
                frame = store_ai_value_fields(state, frame, frame.candidates.base, low16(frame.target_x), 16)
                frame = store_ai_value_fields(state, frame, frame.candidates.address(0, 2), 65535, 16)
                frame = adjust_ai_carrier_fields(state, frame, 'target_y', 1)
                break
    frame = _movement_compare(state, frame, low16(frame.target_y), state.read(0xFFFFF744, 2), 16)
    if frame.status & 5:
        frame = store_ai_value_fields(state, frame, 0xFFFFD300, 65535, 16)
    return frame


def price_support_march_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33FAA: actual path, BYTE speed sum, signed rounded distance and DIVUs."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xD4AC6).cursor())
    for city_address, first_address, second_address in (
            (0xFFFFF364, 0xFFFFF63C, 0xFFFFF63E),
            (0xFFFFF392, 0xFFFFF640, 0xFFFFF642)):
        frame = _movement_move(state, frame, 'target_x', state.read(city_address, 2), 16)
        frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
        frame = store_ai_value_fields(state, frame, first_address, frame.roster.word(low16(frame.target_x), 2), 16)
        frame = store_ai_value_fields(state, frame, second_address, frame.roster.word(low16(frame.target_x)), 16)
    frame = _march_call_fields(state, frame, 0x6518, 0x33FDA)
    frame = first_replace(frame, roster=state.table_at(0xFFFFD300).cursor(),
        candidates=state.table_at(0xFFFFC400).cursor(),
        controller=state.table_at(0xFFFFC800).cursor())
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move_long(state, frame, 'target_y', 0)
    frame = _movement_move(state, frame, 'count', 0, 16)
    while True:
        frame = _support_read_roster_word_fields(state, frame, 'roster', 'unit')
        if frame.status & 8:
            break
        frame = adjust_ai_carrier_fields(state, frame, 'count', 1)
        frame = adjust_ai_carrier_fields(state, frame, 'target_x', frame.candidates.byte(low16(frame.unit)), 8)
        frame = _movement_fixed_shift_word(state, frame, 'unit', 2)
        frame = _movement_arithmetic_long(state, frame, 'target_y', frame.controller.long(low16(frame.unit)))
        frame = _movement_arithmetic_long(state, frame, 'target_y', 100)
    frame = _movement_move_long(state, frame, 'target_x', u32(s16(low16(frame.target_x))))
    frame = _movement_divu_word(state, frame, 'target_x', low16(frame.count), 0x34006)
    frame = store_ai_value_fields(state, frame, 0xFFFFF746, low16(frame.target_x), 16)
    frame = store_ai_value_fields(state, frame, 0xFFFFF748, low16(frame.count), 16)
    frame = _movement_move(state, frame, 'unit', state.read(0xFFFFF644, 2), 16)
    frame = adjust_ai_carrier_fields(state, frame, 'unit', low16(frame.target_x))
    frame = adjust_ai_carrier_fields(state, frame, 'unit', 1, subtract=True)
    frame = _movement_move_long(state, frame, 'unit', u32(s16(low16(frame.unit))))
    frame = _movement_divu_word(state, frame, 'unit', low16(frame.target_x), 0x3401A)
    frame = adjust_ai_carrier_fields(state, frame, 'unit', 2)
    frame = _movement_divu_word(state, frame, 'target_y', 10, 0x34020)
    frame = _movement_multiply_word(state, frame, 'target_y', 3)
    frame = _movement_multiply_word(state, frame, 'target_y', low16(frame.unit))
    return store_ai_value_fields(state, frame, 0xFFFFF3BA, frame.target_y, 32)


def _support_write_budget_fields(state, frame, first_slot, address):
    """Reverse BYTE stores retain the actual L8/L8/W8 carrier changes."""
    frame = _movement_move_long(state, frame, 'target_y', state.read(address, 4))
    frame = store_ai_value_fields(state, frame, frame.roster.address(0, first_slot + 3), low8(frame.target_y), 8)
    for displacement in (first_slot + 2, first_slot + 1):
        frame = _movement_shift_long(state, frame, 'target_y', True)
        frame = store_ai_value_fields(state, frame, frame.roster.address(0, displacement), low8(frame.target_y), 8)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 8, True)
    return store_ai_value_fields(state, frame, frame.roster.address(0, first_slot), low8(frame.target_y), 8)


def append_support_march_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34030: write the real packed queue tail and its unchanged terminator."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFF9000).cursor())
    while True:
        frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
        if frame.status & 4:
            break
        frame = first_replace(frame, roster=frame.roster.advance(s16(low16(frame.target_x)) + 13))
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF748, 2), 16)
    frame = test_ai_register_bit_fields(state, frame, frame.target_x, 5)
    frame = first_replace(frame, target_x=frame.target_x | 32)
    frame = store_ai_value_fields(state, frame, frame.roster.base, low8(frame.target_x), 8)
    frame = store_ai_value_fields(state, frame, frame.roster.address(0, 3), state.read(0xFFFFF747, 1), 8)
    frame = store_ai_value_fields(state, frame, frame.roster.address(0, 4), state.read(0xFFFFF377, 1), 8)
    frame = store_ai_value_fields(state, frame, 0xFFFFF744, state.read(0xFFFFF746, 2), 16)
    frame = first_replace(frame, candidates=state.table_at(0xD4AC6).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    for coordinate_slot, scratch_address, packet_slot in (
            (2, 0xFFFFF746, 1), (0, 0xFFFFF748, 2)):
        frame = _movement_move(state, frame, 'target_y', frame.candidates.word(low16(frame.target_x), coordinate_slot), 16)
        frame = store_ai_value_fields(state, frame, scratch_address, low16(frame.target_y), 16)
        frame = _movement_fixed_shift_word(state, frame, 'target_y', 4, True)
        frame = store_ai_value_fields(state, frame, frame.roster.address(0, packet_slot), low8(frame.target_y), 8)
    frame = _support_write_budget_fields(state, frame, 5, 0xFFFFF39E)
    frame = _support_write_budget_fields(state, frame, 9, 0xFFFFF3BA)
    frame = first_replace(frame, roster=frame.roster.advance(13),
        candidates=state.table_at(0xFFFFD300).cursor())
    while True:
        frame = _support_read_roster_word_fields(state, frame, 'candidates', 'target_x')
        if frame.status & 8:
            break
        frame = store_ai_value_fields(state, frame, frame.roster.base, low8(frame.target_x), 8)
        frame = first_replace(frame, roster=frame.roster.advance(1))
    frame = store_ai_value_fields(state, frame, frame.roster.base, 0, 8, clear=True)
    return store_ai_value_fields(state, frame, 0xFFFFF74A, state.read(0xFFFFD300, 2), 16)


def rebuild_departing_city_head_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """340D8: original invalidation, live roster construction and head choice."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = store_ai_value_fields(state, frame, 0xFFFFF630, 65535, 16)
    frame = _march_call_fields(state, frame, 0x5F48, 0x340E8)
    return _march_call_fields(state, frame, 0xE1F6, 0x340EE)


def finish_support_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """340F0: original MOVE.W FFFF, not a guessed success result."""
    frame = _movement_frame(state, frame)
    return _support_phase_done_fields(state, frame)


REAL_CALL_PAIRS = (
    (0x33906, 0x338F0), (0x33958, 0x33942), (0x339A6, 0x3398C),
    (0x83D4, 0x339D2), (0x33958, 0x339DE), (0x339A6, 0x339F6),
    (0x33A36, 0x33A18), (0x33A70, 0x33A20), (0x33A36, 0x33A9A),
    (0x33B6C, 0x33ABC), (0x33666, 0x33AC8), (0x33BE8, 0x33AF4),
    (0x33C3A, 0x33B20), (0x33CC8, 0x33B24), (0x33D92, 0x33B64),
    (0x651C, 0x33BD2), (0x6518, 0x33CF2), (0x33D0E, 0x33D0C),
    (0x33D7C, 0x33D4E), (0xE1F6, 0x33DA8), (0x33E5E, 0x33DD8),
    (0x33F0A, 0x33DE0), (0x33FAA, 0x33DEC), (0x34030, 0x33E1E),
    (0x33CC8, 0x33E22), (0x340D8, 0x33E56), (0x6518, 0x33FDA),
    (0x5F48, 0x340E8), (0xE1F6, 0x340EE),
)


def _march_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """The29 actual BSR/JSR LONGs; no dispatch-generated or outer return slot."""
    if (target, continuation) not in REAL_CALL_PAIRS:
        raise ValueError('actual complete route-policy CALL/return pair required')
    frame = _movement_frame(state, frame)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    if target == 0x83D4:
        from ..high_level_battle_ai.business_formation import first_deployment_random_fields
        from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
        returned = first_deployment_random_fields(BattlePolicyMemory(state), entered)
    elif target in (0x5F48, 0xE1F6):
        from ..high_level_gameplay_flow.business_battle import build_roster_fields, choose_city_head_fields
        from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
        port = BattlePresentationMemory(state)
        returned = build_roster_fields(port, entered) if target == 0x5F48 else choose_city_head_fields(port, entered)
    elif target == 0x33666:
        from .business_scene_resupply import sort_equipment_roster_fields
        returned = sort_equipment_roster_fields(state, entered)
    elif target in (0x6518, 0x651C):
        from ..high_level_main_flows.business_movement_support import build_path_fields, build_path_from_cells_fields
        returned = build_path_fields(state, entered) if target == 0x6518 else build_path_from_cells_fields(state, entered)
    else:
        returned = execute_march_policy_fields(state, entered, target)
    returned = _movement_frame(state, returned)
    actual = returned.stack_cursor.long()
    if actual != continuation:
        raise FirstDeploymentReturnBoundary(actual, returned, continuation)
    state.sr = state.sr & 65504 | returned.status
    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))


def execute_march_policy_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int) -> FirstDeploymentFrame:
    """Closed named whole-owner vocabulary, with no extra synthetic CALL."""
    frame = _movement_frame(state, frame)
    owners = {
        0x338EC: choose_neighbor_relation_phase_fields,
        0x33906: hostile_neighbor_exists_carry_fields,
        0x3393E: choose_unowned_neighbor_phase_fields,
        0x33958: unowned_neighbor_exists_carry_fields,
        0x33988: choose_roster_troop_phase_fields,
        0x339A6: count_roster_large_troops_fields,
        0x339CC: choose_random_neighbor_phase_fields,
        0x339F4: choose_roster_troop_phase_five_fields,
        0x33A10: evaluate_neighbor_march_phase_fields,
        0x33A36: sum_city_officer_troops_fields,
        0x33A70: choose_weaker_enemy_neighbor_fields,
        0x33AB8: commit_unowned_neighbor_march_fields,
        0x33B6C: shortest_unowned_neighbor_fields,
        0x33BE8: price_two_officer_march_fields,
        0x33C3A: append_two_officer_march_fields,
        0x33CC8: build_ai_movement_packet_fields,
        0x33D0E: append_ai_path_steps_fields,
        0x33D7C: read_path_step_cost_fields,
        0x33D92: restore_departing_city_head_fields,
        0x33DAA: commit_support_march_fields,
        0x33E5E: collect_support_officers_fields,
        0x33F0A: choose_support_roster_fields,
        0x33FAA: price_support_march_fields,
        0x34030: append_support_march_fields,
        0x340D8: rebuild_departing_city_head_fields,
        0x340F0: finish_support_phase_fields,
    }
    if target not in owners:
        raise ValueError('target outside the complete first route-policy family')
    return owners[target](state, frame)


def append_ai_movement_packet_header_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Exact0x33cf2 shared original tail; no extra physical CALL."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(16723968).cursor().advance(s16(state.read(16726054, 2))))
    frame = store_ai_value_fields(state, frame, frame.roster.base, 0, 8, True)
    frame = first_replace(frame, roster=frame.roster.advance(1))
    for source in (4294965067, 4294965061):
        value = state.read(source, 1)
        frame = store_ai_value_fields(state, frame, frame.roster.base, value, 8)
        frame = first_replace(frame, roster=frame.roster.advance(1))
    return _march_call_fields(state, frame, 212238, 212236)
