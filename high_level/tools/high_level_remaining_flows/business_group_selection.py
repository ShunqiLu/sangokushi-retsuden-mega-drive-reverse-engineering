"""Whole live group selection, contact, position and merge parents.

Original marker streams, overlapping packed records, partial LONG carriers,
ordered DATA and physical CALL slots remain observable compatibility behavior.
This module neither executes opcodes nor calls the old scalar projections.
"""
from .domain import SceneState, uint, u8, u16, u32, s8, s16, low8, low16, replace_word
from .services import FirstDeploymentFrame, first_replace, FirstDeploymentReturnBoundary, _first_compare_long
from .business_city import (
    _resource_cost_frame, _group_route_store_fields, _group_route_carry_fields,
    _group_route_bit_fields, _group_route_change_memory_bit_fields,
    _group_route_memory_delta_fields, _group_route_register_delta_fields,
    _duel_commit_sub_word_fields,
    encode_live_group_coordinate_packet_frame_fields,
)
from ..high_level_main_flows.business_movement_support import (
    _movement_move, _movement_move_long, _movement_test, _movement_test_long,
    _movement_compare, _movement_add_word, _movement_adjust_word,
    _movement_fixed_shift_word, _movement_shift_long, _movement_binary_flags,
    _movement_arithmetic_long, _movement_divu_word,
    _movement_save_longs, _movement_restore_longs,
)
from .business_lowbank import _economy_logic_fields, _economy_register_bit_fields


def _selection_compare_long_fields(state: SceneState, frame: FirstDeploymentFrame,
        left: int, right: int) -> FirstDeploymentFrame:
    frame = _first_compare_long(frame, left, right)
    state.sr = (state.sr & 65504) | frame.status
    return frame


def _selection_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Only the four original inner CALLs; caller LONG and actual RTS are real."""
    if (target, continuation) not in ((0x14D34, 0x14CA8), (0x1CEA0, 0x14E3A),
            (0x15186, 0x15172), (0x154C8, 0x15374)):
        raise ValueError('original selection/merge child and return LONG required')
    frame = _resource_cost_frame(state, frame, target)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, uint(continuation, 32))
    entered = first_replace(frame, stack_cursor=stack)
    state.sr = (state.sr & 65504) | entered.status
    if target == 0x14D34:
        result = find_world_marker_record_frame_fields(state, entered)
    elif target == 0x1CEA0:
        result = encode_live_group_coordinate_packet_frame_fields(state, entered)
    elif target == 0x15186:
        result = merge_world_group_records_frame_fields(state, entered)
    else:
        from ..high_level_movement.business_arrival import collect_blocked_cargo_fields
        result = collect_blocked_cargo_fields(state, entered)
    result = _resource_cost_frame(state, result, target)
    state.sr = (state.sr & 65504) | result.status
    actual = result.stack_cursor.long()
    if actual != continuation:
        raise FirstDeploymentReturnBoundary(actual, result, continuation)
    return first_replace(result, stack_cursor=result.stack_cursor.advance(4))


def find_world_marker_record_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """14D34..14D64: live zero-separated packets, postincrement tests and carry."""
    frame = _resource_cost_frame(state, frame, 0x14D34)
    frame = first_replace(frame, candidates=state.table_at(0x00FF3000).cursor())
    while True:
        frame = first_replace(frame, candidates=frame.candidates.advance(1))
        marker = frame.candidates.byte()
        frame = first_replace(frame, candidates=frame.candidates.advance(1))
        frame = _movement_compare(state, frame, low8(frame.target_x), marker, 8)
        if frame.status & 4:
            break
        while True:
            marker = frame.candidates.byte()
            frame = first_replace(frame, candidates=frame.candidates.advance(1))
            frame = _movement_test(state, frame, marker, 8)
            if frame.status & 4:
                break
    frame = first_replace(frame, candidates=frame.candidates.advance(1))
    marker = frame.candidates.byte()
    frame = first_replace(frame, candidates=frame.candidates.advance(1))
    frame = _movement_test(state, frame, marker, 8)
    if frame.status & 8:
        return _group_route_carry_fields(state, frame, True)
    frame = _group_route_store_fields(state, frame, 0xFFFFF68A, 65535)
    return _group_route_carry_fields(state, frame, False)


def select_world_group_or_city_at_marker_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """14CA4..14D34: genuine marker child, live group/city choice and camera target."""
    frame = _resource_cost_frame(state, frame, 0x14CA4)
    frame = _selection_call_fields(state, frame, 0x14D34, 0x14CA8)
    if frame.status & 1:
        frame = _group_route_store_fields(state, frame, 0xFFFFF772, 0, clear=True)
        frame = _movement_move(state, frame, 'target_y', 0, 16)
        frame = _movement_move(state, frame, 'target_y', frame.candidates.byte(), 8)
        frame = _group_route_store_fields(state, frame, 0xFFFFF68A, low16(frame.target_y))
        frame = _movement_compare(state, frame, low16(frame.target_y), 50, 16)
        if not frame.status & 4:
            frame = first_replace(frame, candidates=state.table_at(0xD4AC6).cursor())
            frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
            frame = _movement_move(state, frame, 'unit', frame.candidates.word(low16(frame.target_y)), 16)
            frame = _movement_move(state, frame, 'target_y', frame.candidates.word(low16(frame.target_y), 2), 16)
            frame = _duel_commit_sub_word_fields(state, frame, 'target_y', 104)
            if frame.status & 1:
                frame = _movement_move(state, frame, 'target_y', 0, 16)
            frame = _duel_commit_sub_word_fields(state, frame, 'unit', 152)
            if frame.status & 1:
                frame = _movement_move(state, frame, 'unit', 0, 16)
            return _group_route_store_fields(state, frame, 0x00FF382C, 0, 4, True)
    frame = first_replace(frame, candidates=state.table_at(0xFFFF9000).cursor())
    while True:
        frame = _movement_compare(state, frame, low8(frame.target_x), frame.candidates.byte(13), 8)
        if frame.status & 4:
            break
        frame = _movement_move(state, frame, 'target_y', frame.candidates.byte(), 8)
        frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 15, 16)
        frame = first_replace(frame, candidates=frame.candidates.advance(s16(low16(frame.target_y)) + 13))
    frame = _group_route_store_fields(state, frame, 0x00FF382C, frame.candidates.base, 4)
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    frame = _movement_move(state, frame, 'target_y', frame.candidates.byte(1), 8)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 4)
    frame = _group_route_store_fields(state, frame, 0x00FF3BB6, low16(frame.target_y))
    frame = _duel_commit_sub_word_fields(state, frame, 'target_y', 104)
    if frame.status & 1:
        frame = _movement_move(state, frame, 'target_y', 0, 16)
    frame = _movement_move(state, frame, 'unit', 0, 16)
    frame = _movement_move(state, frame, 'unit', frame.candidates.byte(2), 8)
    frame = _movement_fixed_shift_word(state, frame, 'unit', 4)
    frame = _group_route_store_fields(state, frame, 0x00FF3BB8, low16(frame.unit))
    frame = _duel_commit_sub_word_fields(state, frame, 'unit', 152)
    if frame.status & 1:
        frame = _movement_move(state, frame, 'unit', 0, 16)
    return frame


def test_selected_group_enemy_contacts_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """14E20..14E58: actual MOVEM D1-D2 around the sole neighbor collector."""
    frame = _resource_cost_frame(state, frame, 0x14E20)
    frame = _movement_compare(state, frame, state.read(0xFFFFF68A, 2), 50, 16)
    if frame.status & 4:
        frame = first_replace(frame, roster=state.table_at(state.read(0x00FF382C, 4)).cursor())
        frame = _movement_save_longs(state, frame, ('target_y', 'unit'))
        frame = _selection_call_fields(state, frame, 0x1CEA0, 0x14E3A)
        frame = _movement_restore_longs(state, frame, ('target_y', 'unit'))
        frame = _movement_test(state, frame, low16(frame.target_x), 16)
        if frame.status & 4:
            frame = _group_route_memory_delta_fields(state, frame, 0x00FF3BB2, 2)
            return _group_route_carry_fields(state, frame, True)
    return _group_route_carry_fields(state, frame, False)


def set_pending_group_move_position_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """150DE..1512E: three destructive D0 WORD decrements and original facing bit."""
    frame = _resource_cost_frame(state, frame, 0x150DE)
    frame = _movement_move(state, frame, 'target_y', state.read(0x00FF3BB6, 2), 16)
    frame = _movement_move(state, frame, 'unit', state.read(0x00FF3BB8, 2), 16)
    frame = _movement_adjust_word(state, frame, 'target_x', -1)
    if frame.status & 4:
        frame = _duel_commit_sub_word_fields(state, frame, 'target_y', 16)
    else:
        frame = _movement_adjust_word(state, frame, 'target_x', -1)
        if frame.status & 4:
            frame = _movement_add_word(state, frame, 'unit', 16)
            frame = first_replace(frame, candidates=state.table_at(state.read(0x00FF382C, 4)).cursor())
            frame = _group_route_change_memory_bit_fields(state, frame, frame.candidates.base, 7, True)
        else:
            frame = _movement_adjust_word(state, frame, 'target_x', -1)
            if frame.status & 4:
                frame = _movement_add_word(state, frame, 'target_y', 16)
            else:
                frame = _duel_commit_sub_word_fields(state, frame, 'unit', 16)
                frame = first_replace(frame, candidates=state.table_at(state.read(0x00FF382C, 4)).cursor())
                frame = _group_route_change_memory_bit_fields(state, frame, frame.candidates.base, 7, False)
    frame = _group_route_store_fields(state, frame, 0x00FF3BBA, low16(frame.target_y))
    return _group_route_store_fields(state, frame, 0x00FF3BBC, low16(frame.unit))


def merge_compatible_world_groups_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1512E..15186: ordered first compatible group, true EXG and merge CALL."""
    frame = _resource_cost_frame(state, frame, 0x1512E)
    frame = first_replace(frame, roster=state.table_at(state.read(0x00FF382C, 4)).cursor())
    for carrier, displacement in (('target_y', 1), ('unit', 2), ('count', 4)):
        frame = _movement_move(state, frame, carrier, frame.roster.byte(displacement), 8)
    frame = first_replace(frame, candidates=state.table_at(0xFFFF9000).cursor())
    while True:
        frame = _movement_move(state, frame, 'target_x', frame.candidates.byte(), 8)
        frame = _group_route_bit_fields(state, frame, frame.target_x, 6)
        if frame.status & 4:
            frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
            if frame.status & 4:
                break
            frame = _selection_compare_long_fields(state, frame, frame.candidates.base, frame.roster.base)
            if not frame.status & 4:
                compatible = True
                for carrier, displacement in (('target_y', 1), ('unit', 2), ('count', 4)):
                    frame = _movement_compare(state, frame, low8(frame.carrier(carrier)),
                        frame.candidates.byte(displacement), 8)
                    if not frame.status & 4:
                        compatible = False
                        break
                if compatible:
                    frame = _selection_compare_long_fields(state, frame, frame.candidates.base, frame.roster.base)
                    if frame.status & 5:
                        frame = first_replace(frame, roster=frame.candidates, candidates=frame.roster)
                    frame = _selection_call_fields(state, frame, 0x15186, 0x15172)
                    break
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
        frame = first_replace(frame, candidates=frame.candidates.advance(s16(low16(frame.target_x)) + 13))
    return _group_route_store_fields(state, frame, 0x00FF382C, frame.roster.base, 4)


def _merge_resource_load_fields(state: SceneState, frame: FirstDeploymentFrame,
        pointer: str, carrier: str, offset: int) -> FirstDeploymentFrame:
    """Read one original packed amount through W8, L8 and L8 stages.

    BYTE moves deliberately retain the other register bytes. Reading a LONG
    instead would hide the original DATA order and partial-carrier effects.
    """
    source = getattr(frame, pointer)
    frame = _movement_move(state, frame, carrier, source.byte(0, offset), 8)
    frame = _movement_fixed_shift_word(state, frame, carrier, 8)
    frame = _movement_move(state, frame, carrier, source.byte(0, offset + 1), 8)
    for displacement in (offset + 2, offset + 3):
        frame = _movement_shift_long(state, frame, carrier)
        frame = _movement_move(state, frame, carrier, source.byte(0, displacement), 8)
    return frame


def _merge_resource_amount_fields(state: SceneState, frame: FirstDeploymentFrame,
        offset: int, result_carrier: str) -> FirstDeploymentFrame:
    """Merge one amount, cap at999999, then store in original reverse order."""
    frame = _merge_resource_load_fields(state, frame, 'roster', 'unit', offset)
    frame = _merge_resource_load_fields(state, frame, 'candidates', 'count', offset)
    other = frame.count if result_carrier == 'unit' else frame.unit
    frame = _movement_arithmetic_long(state, frame, result_carrier, other)
    frame = _selection_compare_long_fields(state, frame, frame.carrier(result_carrier), 999999)
    if not frame.status & 5:
        frame = _movement_move_long(state, frame, result_carrier, 999999)
    frame = _group_route_store_fields(state, frame, frame.roster.address(0, offset + 3),
        low8(frame.carrier(result_carrier)), 1)
    for displacement in (offset + 2, offset + 1):
        frame = _movement_shift_long(state, frame, result_carrier, True)
        frame = _group_route_store_fields(state, frame, frame.roster.address(0, displacement),
            low8(frame.carrier(result_carrier)), 1)
    frame = _movement_fixed_shift_word(state, frame, result_carrier, 8, True)
    return _group_route_store_fields(state, frame, frame.roster.address(0, offset),
        low8(frame.carrier(result_carrier)), 1)


def _merge_count_down_fields(frame: FirstDeploymentFrame, carrier: str):
    """The original inclusive low-WORD DBRA changes no CCR or X."""
    remaining = u16(low16(frame.carrier(carrier)) - 1)
    return first_replace(frame, **{carrier: replace_word(frame.carrier(carrier), remaining)}), remaining != 65535


def merge_world_group_records_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """15186..152BE: live overlapping relocation, resource caps and march speed.

    A0 remains the destination descriptor. A1 starts at the source descriptor,
    participates in the actual relocation, and ends after the combined roster.
    The original caller owns the one physical RTS slot; this body does not pop
    it. Zero counts still enter the original do-first loops, not a host guard.
    """
    frame = _resource_cost_frame(state, frame, 0x15186)
    frame = _movement_move(state, frame, 'target_x', frame.candidates.byte(), 8)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(), 8)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 15, 16)
    frame = _movement_move(state, frame, 'unit', low16(frame.target_y), 16)
    frame = _movement_add_word(state, frame, 'target_y', low16(frame.target_x))
    frame = _group_route_store_fields(state, frame, frame.roster.base, low8(frame.target_y), 1)
    frame = _movement_add_word(state, frame, 'unit', 13)
    frame = first_replace(frame, opponent=state.table_at(frame.roster.address(low16(frame.unit))).cursor())

    # The second packed amount accumulates in D3, unlike the first in D2.
    frame = _merge_resource_amount_fields(state, frame, 5, 'unit')
    frame = _merge_resource_amount_fields(state, frame, 9, 'count')

    # Retain source members before moving any overlapping descriptors.
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    frame = first_replace(frame, controller=state.table_at(0xFFFFF65C).cursor())
    while True:
        member = frame.candidates.byte(low16(frame.target_y), 13)
        frame = _group_route_store_fields(state, frame, frame.controller.base, member, 1)
        frame = first_replace(frame, controller=frame.controller.advance(1))
        frame = _movement_add_word(state, frame, 'target_y', 1)
        frame = _movement_compare(state, frame, low16(frame.target_y), low16(frame.target_x), 16)
        if not frame.status & 1:
            break
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)
    frame = _movement_add_word(state, frame, 'target_y', 13)
    frame = first_replace(frame,
        controller=state.table_at(frame.candidates.address(low16(frame.target_y))).cursor(),
        scan=state.table_at(frame.candidates.address(low16(frame.target_x))).cursor(),
        scratch=state.table_at(frame.candidates.base).cursor())
    frame = first_replace(frame, candidates=state.table_at(frame.scan.base).cursor())
    frame = _selection_compare_long_fields(state, frame, frame.opponent.base, frame.scratch.base)
    if not frame.status & 4:
        while True:
            frame = first_replace(frame, scratch=frame.scratch.advance(-1))
            moved = frame.scratch.byte()
            frame = first_replace(frame, scan=frame.scan.advance(-1))
            frame = _group_route_store_fields(state, frame, frame.scan.base, moved, 1)
            frame = _selection_compare_long_fields(state, frame, frame.opponent.base, frame.scratch.base)
            if not frame.status & 1:
                break

    # Copy the retained source roster into the destination's insertion point.
    frame = first_replace(frame, auxiliary=state.table_at(0xFFFFF65C).cursor())
    frame, remaining = _movement_binary_flags(state, frame, low16(frame.target_x), 1, 16, True)
    frame = first_replace(frame, target_x=replace_word(frame.target_x, remaining))
    while True:
        member = frame.auxiliary.byte()
        frame = first_replace(frame, auxiliary=frame.auxiliary.advance(1))
        frame = _group_route_store_fields(state, frame, frame.opponent.base, member, 1)
        frame = first_replace(frame, opponent=frame.opponent.advance(1))
        frame, more = _merge_count_down_fields(frame, 'target_x')
        if not more:
            break

    # Compact whole following packets; the terminal clear is exactly one BYTE.
    while True:
        frame = _movement_move(state, frame, 'target_x', frame.controller.byte(), 8)
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
        if frame.status & 4:
            break
        frame = _movement_add_word(state, frame, 'target_x', 12)
        while True:
            value = frame.controller.byte()
            frame = first_replace(frame, controller=frame.controller.advance(1))
            frame = _group_route_store_fields(state, frame, frame.candidates.base, value, 1)
            frame = first_replace(frame, candidates=frame.candidates.advance(1))
            frame, more = _merge_count_down_fields(frame, 'target_x')
            if not more:
                break
    frame = _group_route_store_fields(state, frame, frame.candidates.base, 0, 1, True)

    # Recompute the merged descriptor's original WORD-summed mean march speed.
    frame = first_replace(frame,
        candidates=state.table_at(frame.roster.address(0, 13)).cursor(),
        controller=state.table_at(0xFFFFC400).cursor())
    frame = _movement_move_long(state, frame, 'target_x', 0)
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    frame = _movement_move(state, frame, 'unit', frame.roster.byte(), 8)
    frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 15, 16)
    frame = _movement_move(state, frame, 'count', low16(frame.unit), 16)
    frame, remaining = _movement_binary_flags(state, frame, low16(frame.count), 1, 16, True)
    frame = first_replace(frame, count=replace_word(frame.count, remaining))
    while True:
        member = frame.candidates.byte()
        frame = first_replace(frame, candidates=frame.candidates.advance(1))
        frame = _movement_move(state, frame, 'target_y', member, 8)
        frame = _movement_move(state, frame, 'distance', 0, 16)
        frame = _movement_move(state, frame, 'distance', frame.controller.byte(low16(frame.target_y)), 8)
        frame = _movement_add_word(state, frame, 'target_x', low16(frame.distance))
        frame, more = _merge_count_down_fields(frame, 'count')
        if not more:
            break
    frame = _movement_divu_word(state, frame, 'target_x', low16(frame.unit), 0x152B6)
    return _group_route_store_fields(state, frame, frame.roster.address(0, 3), low8(frame.target_x), 1)


def test_pending_group_destination_frame_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """152BE: actual group/city scans and the obstacle-cargo CALL, full live ABI.

    D4's retained high BYTE is deliberately part of the later WORD relation
    index; D2's DBRA lane keeps its incoming high WORD. A matching foreign
    obstacle invokes154C8/15374 and then takes the original1537E set-C tail,
    even though the older scalar projection returned clear-C after that call.
    """
    frame = _resource_cost_frame(state, frame, 0x152BE)
    frame = _movement_move(state, frame, 'target_x', state.read(0x00FF3BBA, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 4, True)
    frame = _movement_move(state, frame, 'target_y', state.read(0x00FF3BBC, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 4, True)
    frame = first_replace(frame, roster=state.table_at(state.read(0x00FF382C, 4)).cursor())
    frame = _movement_move(state, frame, 'unit', frame.roster.byte(), 8)
    frame = _economy_logic_fields(state, frame, 'unit', 15, 16)
    frame = _movement_move(state, frame, 'distance', frame.roster.byte(0, 4), 8)
    frame = first_replace(frame, candidates=state.table_at(0xFFFF9000).cursor())
    while True:
        frame = _movement_move(state, frame, 'count', frame.candidates.byte(), 8)
        frame = _economy_logic_fields(state, frame, 'count', 15, 16)
        if frame.status & 4:
            break
        frame = _movement_compare(state, frame, low8(frame.target_x), frame.candidates.byte(0, 1), 8)
        same_position = bool(frame.status & 4)
        if same_position:
            frame = _movement_compare(state, frame, low8(frame.target_y), frame.candidates.byte(0, 2), 8)
            same_position = bool(frame.status & 4)
        if same_position:
            frame = _movement_compare(state, frame, low8(frame.distance), frame.candidates.byte(0, 4), 8)
            if not frame.status & 4:
                return _group_route_carry_fields(state, frame, True)
            frame = first_replace(frame, controller=state.table_at(0x00FF3000).cursor().advance(
                s16(state.read(0x00FF3826, 2))))
            frame = _movement_test(state, frame, frame.controller.byte(0, 1), 8)
            if not frame.status & 4:
                return _group_route_carry_fields(state, frame, False)
            frame = _movement_move(state, frame, 'distance', low16(frame.count), 16)
            frame = _group_route_register_delta_fields(state, frame, 'distance', low16(frame.unit))
            frame = _movement_compare(state, frame, low16(frame.distance), 10, 16)
            return _group_route_carry_fields(state, frame, not bool(frame.status & 5))
        frame = _group_route_register_delta_fields(state, frame, 'count', 13)
        frame = first_replace(frame, candidates=frame.candidates.advance(s16(low16(frame.count))))

    frame = first_replace(frame, candidates=state.table_at(0xFFFFCE9C).cursor())
    frame = _movement_move(state, frame, 'unit', 39, 16)
    while True:
        frame = _movement_test(state, frame, frame.candidates.byte(), 8)
        same_position = not bool(frame.status & 4)
        if same_position:
            frame = _movement_compare(state, frame, low8(frame.target_x), frame.candidates.byte(0, 1), 8)
            same_position = bool(frame.status & 4)
        if same_position:
            frame = _movement_compare(state, frame, low8(frame.target_y), frame.candidates.byte(0, 2), 8)
            same_position = bool(frame.status & 4)
        if same_position:
            break
        frame = first_replace(frame, candidates=frame.candidates.advance(-4))
        frame = first_replace(frame, unit=replace_word(frame.unit, u16(low16(frame.unit) - 1)))
        if low16(frame.unit) == 65535:
            return _group_route_carry_fields(state, frame, False)

    frame = first_replace(frame, scan=state.table_at(0xFFFFE710).cursor())
    frame = _movement_move(state, frame, 'choice', low16(frame.distance), 16)
    frame = _movement_fixed_shift_word(state, frame, 'choice', 1)
    frame = _movement_move(state, frame, 'choice', frame.scan.word(low16(frame.choice)), 16)
    frame = first_replace(frame, scan=state.table_at(0xFFFFF428).cursor())
    frame = _movement_move(state, frame, 'count', frame.scan.byte(low16(frame.unit)), 8)
    frame = _movement_compare(state, frame, low8(frame.distance), low8(frame.count), 8)
    if frame.status & 4:
        return _group_route_carry_fields(state, frame, True)
    frame = _movement_move(state, frame, 'count', u16(s8(low8(frame.count))), 16)
    # This helper's clear=False role is precisely BTST.L, not BSET.L.
    frame = _economy_register_bit_fields(state, frame, 'choice', frame.count)
    if not frame.status & 4:
        return _group_route_carry_fields(state, frame, True)
    frame = first_replace(frame, roster=frame.candidates)
    frame = _selection_call_fields(state, frame, 0x154C8, 0x15374)
    return _group_route_carry_fields(state, frame, True)
