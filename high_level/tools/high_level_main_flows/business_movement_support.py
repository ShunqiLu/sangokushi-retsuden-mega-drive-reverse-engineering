"""Complete Scene-field successor of the frozen movement-v2 capacity rules.

confirmed: original 17C8A..17D10 and 17E3C..17EBA listing. Historical
movement-v2 acceptance remains immutable; this is its current main-flow ABI,
not a second byte-credit owner. Every view uses the supplied Scene RAM.
"""
from .domain import (
    SceneState, Boundary, uint, u8, u16, low8, low16, replace_byte,
    replace_word, checked_state, checked_table,
)
from .contexts_gameplay import (
    FirstDeploymentFrame, FirstDeploymentReturnBoundary, first_replace,
    MovementContinuationBoundary,
)


def _movement_frame(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    checked_state(state)
    if type(frame) is not FirstDeploymentFrame:
        raise ValueError('complete current movement fields required')
    frame.validate(state, True)
    for view in (frame.roster, frame.candidates, frame.controller, frame.scan,
                 frame.opponent, frame.scratch, frame.auxiliary, frame.stack_cursor):
        if view is None:
            raise Boundary('movement requires each actual address carrier')
        checked_table(view, state)
    return frame


def _movement_test(state: SceneState, frame: FirstDeploymentFrame, value, width: int) -> FirstDeploymentFrame:
    if width not in (8, 16):
        raise ValueError('original movement BYTE or WORD required')
    value = uint(value, width)
    status = (frame.status & 16) | (8 if value & (1 << (width - 1)) else 0) | (4 if value == 0 else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, status=status)


def _movement_move(state: SceneState, frame: FirstDeploymentFrame, carrier: str, value, width: int) -> FirstDeploymentFrame:
    value = uint(value, width)
    retained = frame.carrier(carrier)
    if width == 8:
        numeric = replace_byte(retained, value)
    elif width == 16:
        numeric = replace_word(retained, value)
    else:
        raise ValueError('original movement BYTE or WORD required')
    frame = first_replace(frame, **{carrier: numeric})
    return _movement_test(state, frame, value, width)


def _movement_bit(state: SceneState, frame: FirstDeploymentFrame, value, bit: int) -> FirstDeploymentFrame:
    value = uint(value, 8)
    if bit not in (0, 1):
        raise ValueError('original movement flag bit required')
    status = (frame.status & 27) | (4 if not value & (1 << bit) else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, status=status)


def _movement_compare(state: SceneState, frame: FirstDeploymentFrame, destination, source, width: int) -> FirstDeploymentFrame:
    destination, source = uint(destination, width), uint(source, width)
    if width not in (8, 16):
        raise ValueError('original movement comparison width required')
    sign, mask = 1 << (width - 1), (1 << width) - 1
    result = (destination - source) & mask
    overflow = bool((destination ^ source) & (destination ^ result) & sign)
    status = (frame.status & 16) | (8 if result & sign else 0) | (4 if result == 0 else 0) | (2 if overflow else 0) | (1 if destination < source else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, status=status)


def _movement_shift_word(state: SceneState, frame: FirstDeploymentFrame, carrier: str) -> FirstDeploymentFrame:
    value = low16(frame.carrier(carrier))
    result = u16(value << 1)
    carry = bool(value & 32768)
    status = (17 if carry else 0) | (8 if result & 32768 else 0) | (4 if result == 0 else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, **{carrier: replace_word(frame.carrier(carrier), result)}, status=status)


def _movement_add_byte(state: SceneState, frame: FirstDeploymentFrame, carrier: str, source) -> FirstDeploymentFrame:
    destination, source = low8(frame.carrier(carrier)), uint(source, 8)
    result = u8(destination + source)
    carry = destination + source > 255
    overflow = bool((~(destination ^ source)) & (destination ^ result) & 128)
    status = (17 if carry else 0) | (8 if result & 128 else 0) | (4 if result == 0 else 0) | (2 if overflow else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, **{carrier: replace_byte(frame.carrier(carrier), result)}, status=status)


def _movement_adjust_word(state: SceneState, frame: FirstDeploymentFrame, carrier: str, step: int) -> FirstDeploymentFrame:
    if step not in (-1, 1):
        raise ValueError('original movement quick increment or decrement required')
    value = low16(frame.carrier(carrier))
    result = u16(value + step)
    if step == 1:
        carry, overflow = value == 65535, value == 32767
    else:
        carry, overflow = value == 0, value == 32768
    status = (17 if carry else 0) | (8 if result & 32768 else 0) | (4 if result == 0 else 0) | (2 if overflow else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, **{carrier: replace_word(frame.carrier(carrier), result)}, status=status)


def _movement_call(state: SceneState, frame: FirstDeploymentFrame, target, continuation) -> FirstDeploymentFrame:
    """Own only this BSR slot; the caller's outer JSR slot remains untouched."""
    uint(target, 32)
    uint(continuation, 32)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    state.sr = (state.sr & 65504) | entered.status
    if target == 0x17E3C:
        result = selected_roster_capacity_fields(state, entered)
    elif target == 0x17D10:
        result = find_group_at_coordinate_fields(state, entered)
    elif target == 0x17D3C:
        result = collect_six_neighbor_candidates_fields(state, entered)
    elif target == 0x17DDC:
        result = filter_neighbor_candidates_fields(state, entered)
    elif target == 0x17EBA:
        result = read_neighbor_source_cost_fields(state, entered)
    elif target == 0x181A6:
        result = group_matches_city_head_fields(state, entered)
    elif target == 0x1802A:
        result = reserve_packed_group_member_fields(state, entered)
    elif target == 0x18158:
        result = refresh_packed_group_average_fields(state, entered)
    elif target == 0x18184:
        result = copy_selected_city_group_parameter_fields(state, entered)
    elif target == 0x1807A:
        result = split_city_resources_into_group_fields(state, entered)
    elif target == 0x181E8:
        result = append_survivors_to_packed_group_fields(state, entered)
    elif target == 0x18224:
        result = add_staged_resources_to_packed_group_fields(state, entered)
    elif target == 0x182C4:
        result = assign_city_survivor_roster_tokens_fields(state, entered)
    elif target == 0x1830A:
        result = merge_city_survivor_rosters_fields(state, entered)
    elif target == 0x35760:
        result = signed_divmod_fields(state, entered)
    elif target == 0x3576C:
        result = positive_denominator_fields(state, entered)
    elif target == 0x3577A:
        result = unsigned_divmod_fields(state, entered)
    elif target == 0x357DA:
        result = divide_longs_by_word_fields(state, entered)
    elif target == 0x260E4:
        result = present_battle_message_fields(state, entered)
    else:
        result = state.service_at(target, entered)
    if type(result) is not FirstDeploymentFrame:
        raise Boundary('movement child lacks actual complete return fields and SP')
    result = _movement_frame(state, result)
    state.sr = (state.sr & 65504) | result.status
    actual = result.stack_cursor.long()
    if actual != continuation:
        raise FirstDeploymentReturnBoundary(actual, result, continuation)
    return first_replace(result, stack_cursor=result.stack_cursor.advance(4))


def selected_roster_capacity_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """17E3C: select the real roster pair, count both, then cap at ten.

    The signed terminators are consumed by postincrement. Two flag tests read
    F6D7 separately; CLR.W D1 is a register write, not a memory read. No
    artificial roster bound replaces the original WORD wraparound.
    """
    frame = _movement_frame(state, frame)
    frame = _movement_bit(state, frame, state.read(0xFFFFF6D7, 1), 0)
    if not frame.status & 4:
        return _movement_move(state, frame, 'offset_y', 1, 16)
    frame = _movement_bit(state, frame, state.read(0xFFFFF6D7, 1), 1)
    if not frame.status & 4:
        frame = first_replace(frame, roster=state.table_at(0xFFFFF45E).cursor())
        frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF68A, 2), 16)
        frame = _movement_shift_word(state, frame, 'target_x')
        frame = _movement_move(state, frame, 'target_y', frame.roster.word(low16(frame.target_x)), 16)
        frame = _movement_compare(state, frame, low16(frame.target_y), state.read(0xFFFFF3A6, 2), 16)
        if not frame.status & 4:
            return _movement_move(state, frame, 'offset_y', 1, 16)
        frame = first_replace(frame, roster=state.table_at(0xFFFFA5A4).cursor(), auxiliary=state.table_at(0xFFFFA5CE))
    else:
        frame = first_replace(frame, roster=state.table_at(0xFFFFA027).cursor())
        frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF68A, 2), 16)
        frame = _movement_move(state, frame, 'target_y', 0, 16)
        frame = _movement_move(state, frame, 'target_y', frame.roster.byte(low16(frame.target_x)), 8)
        frame = _movement_compare(state, frame, low16(frame.target_y), state.read(0xFFFFF3A6, 2), 16)
        if not frame.status & 4:
            return _movement_move(state, frame, 'offset_y', 1, 16)
        frame = first_replace(frame, roster=state.table_at(0xFFFFA550).cursor(), auxiliary=state.table_at(0xFFFFA57A))
    frame = _movement_move(state, frame, 'offset_y', 0, 16)
    while True:
        entry = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_test(state, frame, entry, 16)
        if frame.status & 8:
            break
        frame = _movement_adjust_word(state, frame, 'offset_y', 1)
    while True:
        entry = frame.auxiliary.word()
        frame = first_replace(frame, auxiliary=frame.auxiliary.advance(2))
        frame = _movement_test(state, frame, entry, 16)
        if frame.status & 8:
            break
        frame = _movement_adjust_word(state, frame, 'offset_y', 1)
    frame = _movement_compare(state, frame, low16(frame.offset_y), 10, 16)
    if not frame.status & 5:
        frame = _movement_move(state, frame, 'offset_y', 10, 16)
    return frame


def ensure_neighbor_capacity_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """17C8A: retain a usable occupied cell or select a filtered neighbor.

    Calls whose historical API did not observe complete CPU fields stop only
    after their real BSR token. If a complete child is supplied, consume its
    actual fields and return slot; never substitute legacy scalar success.
    """
    frame = _movement_frame(state, frame)
    frame = _movement_call(state, frame, 0x17E3C, 0x17C8E)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF6D6, 2), 16)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 3, 16)
    frame = _movement_shift_word(state, frame, 'target_x')
    frame = first_replace(frame, auxiliary=state.table_at(0xFFFFF6E8).at(low16(frame.target_x)))
    frame = _movement_shift_word(state, frame, 'target_x')
    pointer = state.table_at(0x17C7A).long(low16(frame.target_x))
    frame = first_replace(frame, scratch=state.table_at(pointer))
    frame = _movement_move(state, frame, 'choice', frame.scratch.word(), 16)
    frame = _movement_test(state, frame, frame.auxiliary.word(), 16)
    if not frame.status & 8:
        frame = _movement_move(state, frame, 'target_x', frame.auxiliary.word(), 16)
        frame = _movement_call(state, frame, 0x17D10, 0x17CB2)
        frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)
        frame = _movement_move(state, frame, 'target_x', low8(frame.target_x) & 15, 8)
        frame = _movement_add_byte(state, frame, 'target_x', low8(frame.offset_y))
        frame = _movement_compare(state, frame, low8(frame.target_x), 10, 8)
        if frame.status & 5:
            return frame
    frame = _movement_call(state, frame, 0x17D3C, 0x17CC6)
    frame = _movement_call(state, frame, 0x17DDC, 0x17CCA)
    frame = _movement_test(state, frame, low16(frame.count), 16)
    if frame.status & 4:
        return frame
    frame = _movement_move(state, frame, 'unit', low16(frame.count), 16)
    frame = _movement_adjust_word(state, frame, 'unit', -1)
    frame = first_replace(frame, roster=state.table_at(0xFFFFA954).cursor())
    while True:
        entry = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'target_x', entry, 16)
        if not frame.status & 8:
            frame.auxiliary.set_word(0, low16(frame.target_x))
            return _movement_test(state, frame, low16(frame.target_x), 16)
        frame = first_replace(frame, unit=replace_word(frame.unit, u16(low16(frame.unit) - 1)))
        if low16(frame.unit) == 65535:
            break
    frame = first_replace(frame, candidates=state.table_at(0xFFFFA954).cursor())
    frame = _movement_adjust_word(state, frame, 'count', -1)
    while True:
        entry = frame.candidates.word()
        frame = first_replace(frame, candidates=frame.candidates.advance(2))
        frame = _movement_move(state, frame, 'target_x', entry, 16)
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 32767, 16)
        frame = _movement_call(state, frame, 0x17D10, 0x17CF0)
        frame = _movement_move(state, frame, 'target_y', frame.roster.byte(), 8)
        frame = _movement_move(state, frame, 'target_y', low8(frame.target_y) & 15, 8)
        frame = _movement_add_byte(state, frame, 'target_y', low8(frame.offset_y))
        frame = _movement_compare(state, frame, low8(frame.target_y), 10, 8)
        if frame.status & 5:
            frame.auxiliary.set_word(0, low16(frame.target_x))
            return _movement_test(state, frame, low16(frame.target_x), 16)
        frame = first_replace(frame, count=replace_word(frame.count, u16(low16(frame.count) - 1)))
        if low16(frame.count) == 65535:
            break
    frame.auxiliary.set_word(0, 65535)
    return _movement_test(state, frame, 65535, 16)


# Current full ABI successors of the four frozen historical child owners.
def _movement_fixed_shift_word(state: SceneState, frame: FirstDeploymentFrame, carrier: str, amount: int, right: bool=False) -> FirstDeploymentFrame:
    if amount not in (1, 2, 3, 4, 5, 7, 8) or type(right) is not bool:
        raise ValueError('original fixed movement WORD shift required')
    value = low16(frame.carrier(carrier))
    if right:
        result = value >> amount
        carry = bool(value & (1 << (amount - 1)))
    else:
        result = u16(value << amount)
        carry = bool(value & (1 << (16 - amount)))
    status = (17 if carry else 0) | (8 if result & 32768 else 0) | (4 if result == 0 else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, **{carrier: replace_word(frame.carrier(carrier), result)}, status=status)


def _movement_add_word(state: SceneState, frame: FirstDeploymentFrame, carrier: str, source) -> FirstDeploymentFrame:
    value, source = low16(frame.carrier(carrier)), uint(source, 16)
    result = u16(value + source)
    carry = value + source > 65535
    overflow = bool((~(value ^ source)) & (value ^ result) & 32768)
    status = (17 if carry else 0) | (8 if result & 32768 else 0) | (4 if result == 0 else 0) | (2 if overflow else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, **{carrier: replace_word(frame.carrier(carrier), result)}, status=status)


def _movement_adjust_pair_word(state: SceneState, frame: FirstDeploymentFrame, carrier: str, step: int) -> FirstDeploymentFrame:
    if step not in (-2, 2):
        raise ValueError('original candidate WORD pair step required')
    value = low16(frame.carrier(carrier))
    result = u16(value + step)
    if step == 2:
        carry = value + 2 > 65535
        overflow = bool((~(value ^ 2)) & (value ^ result) & 32768)
    else:
        carry = value < 2
        overflow = bool((value ^ 2) & (value ^ result) & 32768)
    status = (17 if carry else 0) | (8 if result & 32768 else 0) | (4 if result == 0 else 0) | (2 if overflow else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, **{carrier: replace_word(frame.carrier(carrier), result)}, status=status)


def find_group_at_coordinate_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """17D10: packed-group search, returning the actual group or sentinel.

    The coordinate is destructively unpacked into D0/D1 low WORDs. D2 keeps
    its high WORD while each header is masked, and A0 advances by13+members.
    No early zero-header replacement or cached coordinate read is introduced.
    """
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    frame = _movement_move(state, frame, 'target_y', low8(frame.target_x), 8)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 8, True)
    frame = first_replace(frame, roster=state.table_at(0xFFFF9000).cursor())
    while True:
        frame = _movement_move(state, frame, 'unit', frame.roster.byte(), 8)
        frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 15, 16)
        if frame.status & 4:
            return frame
        frame = _movement_compare(state, frame, low8(frame.target_x), frame.roster.byte(0, 1), 8)
        if frame.status & 4:
            frame = _movement_compare(state, frame, low8(frame.target_y), frame.roster.byte(0, 2), 8)
            if frame.status & 4:
                return frame
        frame = first_replace(frame, roster=frame.roster.at(low16(frame.unit), 13).cursor())


def read_neighbor_source_cost_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """17EBA: wrapped72*x+y index, then both actual source BYTE reads.

    The first terrain BYTE is discarded only after its real read. The second
    read leaves D2's actual cost, D4's wrapped index, A2 and BYTE flags. Source
    assets remain external ReadOnlyData, not embedded program arrays.
    """
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'distance', low16(frame.target_x), 16)
    frame = _movement_move(state, frame, 'unit', low16(frame.distance), 16)
    frame = _movement_fixed_shift_word(state, frame, 'unit', 3)
    frame = _movement_add_word(state, frame, 'distance', low16(frame.unit))
    frame = _movement_fixed_shift_word(state, frame, 'distance', 3)
    frame = _movement_add_word(state, frame, 'distance', low16(frame.target_y))
    frame = first_replace(frame, controller=state.table_at(0xEE5F0))
    frame = _movement_move(state, frame, 'unit', 0, 16)
    frame = _movement_move(state, frame, 'unit', frame.controller.byte(low16(frame.distance)), 8)
    frame = first_replace(frame, controller=state.table_at(0x670A))
    frame = _movement_move(state, frame, 'unit', frame.controller.byte(low16(frame.distance)), 8)
    return frame


def _movement_append_valid_neighbor(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Shared six repeated append blocks; branch uses the returned N bit."""
    if frame.status & 8:
        return frame
    frame = _movement_move(state, frame, 'unit', low8(frame.target_x), 8)
    frame = _movement_fixed_shift_word(state, frame, 'unit', 8)
    frame = _movement_move(state, frame, 'unit', low8(frame.target_y), 8)
    coordinate = low16(frame.unit)
    frame.roster.set_word(0, coordinate)
    frame = first_replace(frame, roster=frame.roster.advance(2))
    frame = _movement_test(state, frame, coordinate, 16)
    return _movement_adjust_word(state, frame, 'count', 1)


def collect_six_neighbor_candidates_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """17D3C: six adjacent source-valid coordinates, original incremental order.

    Each source-cost JSR owns its actual LONG return slot; NOPs preserve the
    returned CCR. Only accepted coordinates advance the live A0 output.
    """
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFA954).cursor())
    frame = _movement_move(state, frame, 'count', 0, 16)
    frame = _movement_move(state, frame, 'unit', state.read(0xFFFFF68A, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'unit', 2)
    frame = first_replace(frame, candidates=state.table_at(0xD4AC6).cursor())
    frame = _movement_move(state, frame, 'target_x', frame.candidates.word(low16(frame.unit), 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 4, True)
    frame = _movement_move(state, frame, 'target_y', frame.candidates.word(low16(frame.unit)), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 4, True)
    frame = _movement_adjust_word(state, frame, 'target_x', -1)
    frame = _movement_adjust_word(state, frame, 'target_y', -1)
    for dx, dy, continuation in ((0, 0, 0x17D62), (0, 1, 0x17D76),
                                 (1, 1, 0x17D8C), (1, -1, 0x17DA2),
                                 (0, -1, 0x17DB6), (-1, -1, 0x17DCC)):
        if dx:
            frame = _movement_adjust_word(state, frame, 'target_x', dx)
        if dy:
            frame = _movement_adjust_word(state, frame, 'target_y', dy)
        frame = _movement_call(state, frame, 0x17EBA, continuation)
        frame = _movement_append_valid_neighbor(state, frame)
    return frame


def filter_neighbor_candidates_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """17DDC: mark matching friendly groups and remove foreign-head candidates.

    Search starts at A952+(count*2), and deletion shifts only through the
    original count*2 limit. In particular, the final slot is not silently
    repaired or cleared. Zero-count, wrapped offsets and real group reads
    retain original behavior, subject only to the explicit Scene DATA budget.
    """
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFF9000).cursor(), candidates=state.table_at(0xFFFFA952).cursor())
    while True:
        frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
        if frame.status & 4:
            return frame
        frame = _movement_move(state, frame, 'target_y', frame.roster.byte(0, 1), 8)
        frame = _movement_fixed_shift_word(state, frame, 'target_y', 8)
        frame = _movement_move(state, frame, 'target_y', frame.roster.byte(0, 2), 8)
        frame = _movement_move(state, frame, 'unit', low16(frame.count), 16)
        frame = _movement_fixed_shift_word(state, frame, 'unit', 1)
        matched = False
        while True:
            frame = _movement_compare(state, frame, low16(frame.target_y), frame.candidates.word(low16(frame.unit)), 16)
            if frame.status & 4:
                matched = True
                break
            frame = _movement_adjust_pair_word(state, frame, 'unit', -2)
            if frame.status & 4:
                break
        if matched:
            frame = _movement_move(state, frame, 'target_y', frame.roster.byte(0, 4), 8)
            frame = _movement_compare(state, frame, low8(frame.target_y), low8(frame.choice), 8)
            if frame.status & 4:
                marked = frame.candidates.word(low16(frame.unit)) | 32768
                frame.candidates.set_word(low16(frame.unit), marked)
                frame = _movement_test(state, frame, marked, 16)
            else:
                frame = _movement_adjust_word(state, frame, 'count', -1)
                if frame.status & 4:
                    return frame
                frame = _movement_move(state, frame, 'distance', low16(frame.count), 16)
                frame = _movement_fixed_shift_word(state, frame, 'distance', 1)
                while True:
                    coordinate = frame.candidates.word(low16(frame.unit), 2)
                    frame.candidates.set_word(low16(frame.unit), coordinate)
                    frame = _movement_test(state, frame, coordinate, 16)
                    frame = _movement_adjust_pair_word(state, frame, 'unit', 2)
                    frame = _movement_compare(state, frame, low16(frame.unit), low16(frame.distance), 16)
                    if not frame.status & 1:
                        break
        frame = first_replace(frame, roster=frame.roster.at(low16(frame.target_x), 13).cursor())


# Current Scene successor: original packet mutation and message wait fields.
def _movement_move_long(state: SceneState, frame: FirstDeploymentFrame, carrier: str, value) -> FirstDeploymentFrame:
    value = uint(value, 32)
    status = (frame.status & 16) | (8 if value & 2147483648 else 0) | (4 if value == 0 else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, **{carrier: value}, status=status)


def _movement_mutation_flags(state: SceneState, frame: FirstDeploymentFrame, original, step: int, width: int) -> tuple[FirstDeploymentFrame, int]:
    original = uint(original, width)
    if step not in (-1, 1) or width not in (8, 16):
        raise ValueError('actual retreat BYTE increment or WORD decrement required')
    sign, mask = 1 << (width - 1), (1 << width) - 1
    result = (original + step) & mask
    if step == 1:
        carry, overflow = original == mask, original == sign - 1
    else:
        carry, overflow = original == 0, original == sign
    status = (17 if carry else 0) | (8 if result & sign else 0) | (4 if result == 0 else 0) | (2 if overflow else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, status=status), result


def _movement_compare_address(state: SceneState, frame: FirstDeploymentFrame, left, right) -> FirstDeploymentFrame:
    left, right = uint(left, 32), uint(right, 32)
    value = (left - right) & 4294967295
    overflow = bool((left ^ right) & (left ^ value) & 2147483648)
    status = (frame.status & 16) | (8 if value & 2147483648 else 0) | (4 if value == 0 else 0) | (2 if overflow else 0) | (1 if left < right else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, status=status)


def group_matches_city_head_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """181A6: actual mode-selected BYTE/WORD comparison and full-SR carry."""
    frame = _movement_frame(state, frame)
    frame = _movement_bit(state, frame, state.read(0xFFFFF6D7, 1), 1)
    if not frame.status & 4:
        frame = first_replace(frame, opponent=state.table_at(0xFFFFF45E))
        frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF68A, 2), 16)
        frame = _movement_shift_word(state, frame, 'target_y')
        frame = _movement_compare(state, frame, low16(frame.target_x), frame.opponent.word(low16(frame.target_y)), 16)
    else:
        frame = first_replace(frame, opponent=state.table_at(0xFFFFA027))
        frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF68A, 2), 16)
        frame = _movement_compare(state, frame, low8(frame.target_x), frame.opponent.byte(low16(frame.target_y)), 8)
    status = (frame.status & 30) | (1 if frame.status & 4 else 0)
    state.set_status_word((state.sr & 65504) | status)
    return first_replace(frame, status=status)


def reserve_packed_group_member_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1802A: find the true following sentinel, then reverse-shift one BYTE."""
    frame = _movement_frame(state, frame)
    start = frame.roster.at(low16(frame.target_y), 13).cursor()
    frame = first_replace(frame, candidates=start, controller=state.table_at(start.base))
    frame = _movement_test(state, frame, low16(frame.target_y), 16)
    if frame.status & 4:
        frame.candidates.byte()
        frame.candidates.set_byte(0, 0)
        frame = _movement_test(state, frame, 0, 8)
    while True:
        frame = _movement_move(state, frame, 'unit', frame.candidates.byte(), 8)
        frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 15, 16)
        if frame.status & 4:
            break
        frame = first_replace(frame, candidates=frame.candidates.at(low16(frame.unit), 13).cursor())
    frame = first_replace(frame, opponent=frame.candidates.advance(1))
    frame.opponent.byte()
    frame.opponent.set_byte(0, 0)
    frame = _movement_test(state, frame, 0, 8)
    while True:
        frame = _movement_compare_address(state, frame, frame.candidates.base, frame.controller.base)
        if frame.status & 5:
            return frame
        source = frame.candidates.advance(-1)
        frame = first_replace(frame, candidates=source)
        value = source.byte()
        destination = frame.opponent.advance(-1)
        frame = first_replace(frame, opponent=destination)
        destination.set_byte(0, value)
        frame = _movement_test(state, frame, value, 8)


def refresh_packed_group_average_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """18158: actual postincrement roster, WORD sum and packed DIVU result."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
    frame = first_replace(frame, candidates=frame.roster.advance(13))
    frame = _movement_move_long(state, frame, 'target_y', 0)
    frame = _movement_move(state, frame, 'unit', low16(frame.target_x), 16)
    frame = _movement_adjust_word(state, frame, 'unit', -1)
    frame = _movement_move(state, frame, 'count', 0, 16)
    frame = _movement_move(state, frame, 'distance', 0, 16)
    frame = first_replace(frame, controller=state.table_at(0xFFFFC400))
    while True:
        officer = frame.candidates.byte()
        frame = first_replace(frame, candidates=frame.candidates.advance(1))
        frame = _movement_move(state, frame, 'count', officer, 8)
        frame = _movement_move(state, frame, 'distance', frame.controller.byte(low16(frame.count)), 8)
        frame = _movement_add_word(state, frame, 'target_y', low16(frame.distance))
        frame = first_replace(frame, unit=replace_word(frame.unit, (low16(frame.unit) - 1) & 65535))
        if low16(frame.unit) == 65535:
            break
    divisor = low16(frame.target_x)
    if divisor == 0:
        raise MovementContinuationBoundary(0x1817C, frame, 'original zero-count DIVU requires the actual exception continuation')
    quotient, remainder = divmod(frame.target_y, divisor)
    frame = first_replace(frame, target_y=(remainder << 16) | quotient)
    frame = _movement_test(state, frame, quotient, 16)
    average = low8(frame.target_y)
    frame.roster.set_byte(0, average, 3)
    return _movement_test(state, frame, average, 8)


def copy_selected_city_group_parameter_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """18184: exact pointer-table selection and one live BYTE parameter copy."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF6D6, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    pointer = state.table_at(0x18196).long(low16(frame.target_x))
    frame = first_replace(frame, candidates=state.table_at(pointer).cursor())
    value = frame.candidates.byte(0, 1)
    frame.roster.set_byte(0, value, 4)
    return _movement_test(state, frame, value, 8)


def _movement_select_packet_for_retreat(state: SceneState, frame: FirstDeploymentFrame, continuation) -> FirstDeploymentFrame:
    """The two original shared destination-coordinate and empty-header blocks."""
    frame = _movement_move(state, frame, 'target_x', frame.controller.word(), 16)
    frame = _movement_call(state, frame, 0x17D10, continuation)
    value = low8(frame.target_x)
    frame.roster.set_byte(0, value, 1)
    frame = _movement_test(state, frame, value, 8)
    value = low8(frame.target_y)
    frame.roster.set_byte(0, value, 2)
    frame = _movement_test(state, frame, value, 8)
    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(), 8)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 15, 16)
    if frame.status & 4:
        for displacement in range(5, 14):
            frame.roster.byte(0, displacement)
            frame.roster.set_byte(0, 0, displacement)
            frame = _movement_test(state, frame, 0, 8)
    return frame


def integrate_selected_officer_into_packed_group_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """17F30: one-officer extraction or whole-city survivor integration.

    This current Scene successor follows the listing's exact child order,
    including the18158 call instruction at17FAC, returning17FB0.
    The unclosed historical scalar draft is not used
    as a second execution algorithm and is not a parity/completion authority.
    """
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF6D6, 2), 16)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 2, 16)
    frame = _movement_shift_word(state, frame, 'target_x')
    pointer = state.table_at(0x17F18).long(low16(frame.target_x))
    frame = first_replace(frame, roster=state.table_at(pointer).cursor())
    frame = first_replace(frame, scan=frame.roster.cursor())
    pointer = state.table_at(0x17F20).long(low16(frame.target_x))
    frame = first_replace(frame, candidates=state.table_at(pointer).cursor())
    pointer = state.table_at(0x17F28).long(low16(frame.target_x))
    frame = first_replace(frame, controller=state.table_at(pointer))
    frame, count = _movement_mutation_flags(state, frame, frame.candidates.word(), -1, 16)
    frame.candidates.set_word(0, count)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF3A6, 2), 16)
    frame = _movement_call(state, frame, 0x181A6, 0x17F52)
    if not frame.status & 1:
        while True:
            officer = frame.roster.word()
            frame = first_replace(frame, roster=frame.roster.advance(2))
            frame = _movement_move(state, frame, 'target_y', officer, 16)
            frame = _movement_compare(state, frame, low16(frame.target_y), low16(frame.target_x), 16)
            if frame.status & 4:
                break
        while True:
            officer = frame.roster.word()
            frame = first_replace(frame, roster=frame.roster.advance(2))
            frame.roster.set_word(0, officer, -4)
            frame = _movement_test(state, frame, officer, 16)
            if frame.status & 8:
                break
        frame = _movement_select_packet_for_retreat(state, frame, 0x17F68)
        frame, header = _movement_mutation_flags(state, frame, frame.roster.byte(), 1, 8)
        frame.roster.set_byte(0, header)
        frame = _movement_call(state, frame, 0x1802A, 0x17FA4)
        officer = state.read(0xFFFFF3A7, 1)
        frame.controller.set_byte(0, officer)
        frame = _movement_test(state, frame, officer, 8)
        frame = _movement_call(state, frame, 0x1807A, 0x17FAC)
        frame = _movement_call(state, frame, 0x18158, 0x17FB0)
        frame = first_replace(frame, candidates=state.table_at(0xFFFFCC00).cursor())
        frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF3A6, 2), 16)
        assignment = frame.candidates.byte(low16(frame.target_x))
        status = (frame.status & 27) | (4 if not assignment & 64 else 0)
        frame = first_replace(frame, status=status)
        state.sr = (state.sr & 65504) | status
        frame.candidates.set_byte(low16(frame.target_x), assignment | 64)
        frame = first_replace(frame, candidates=state.table_at(0xFFFFA150).cursor())
        frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
        frame.candidates.long(low16(frame.target_x))
        frame.candidates.set_long(low16(frame.target_x), 0)
        frame = _movement_test(state, frame, 0, 16)
    else:
        frame = first_replace(frame, opponent=state.table_at(frame.roster.base))
        frame = _movement_call(state, frame, 0x182C4, 0x17FD2)
        frame = _movement_move(state, frame, 'offset_y', 0, 16)
        while True:
            officer = frame.roster.word()
            frame = first_replace(frame, roster=frame.roster.advance(2))
            frame = _movement_test(state, frame, officer, 16)
            if frame.status & 8:
                break
            frame = _movement_adjust_word(state, frame, 'offset_y', 1)
        frame = _movement_select_packet_for_retreat(state, frame, 0x17FE4)
        frame = _movement_call(state, frame, 0x181E8, 0x1801C)
        frame = _movement_call(state, frame, 0x18224, 0x18020)
        frame = _movement_call(state, frame, 0x18158, 0x18024)
    return _movement_call(state, frame, 0x18184, 0x18028)


def present_battle_message_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """260E4: actual saved WORDs,2500/2700 SR, live input reads and restores.

    An unknown IRQ stops at the original wait with both live saves intact;
    it does not pretend that an arbitrary progress provider preserved CPU
    fields. The separate060C display-reset call owns its real26114 token.
    """
    frame = _movement_frame(state, frame)
    for address in (0xFFFFF612, 0xFFFFF362):
        value = state.read(address, 2)
        stack = frame.stack_cursor.advance(-2)
        stack.set_word(0, value)
        frame = first_replace(frame, stack_cursor=stack)
        frame = _movement_test(state, frame, value, 16)
    state.write(0xFFFFF612, 2, 1044)
    frame = _movement_test(state, frame, 1044, 16)
    for address in (0xFFFFF362, 0xFFFFF600):
        state.read(address, 2)
        state.write(address, 2, 0)
        frame = _movement_test(state, frame, 0, 16)
    state.set_status_word(0x2500)
    frame = first_replace(frame, status=0)
    while True:
        command = state.read(0xFFFFF600, 2)
        frame = _movement_test(state, frame, command, 16)
        if frame.status & 4:
            raise MovementContinuationBoundary(0x260FE, frame, 'battle-message input wait requires the actual full resumed IRQ fields')
        command = state.read(0xFFFFF600, 2)
        frame = _movement_compare(state, frame, command, 40, 16)
        if not frame.status & 4:
            break
        frame = _movement_call(state, frame, 0x60C, 0x26114)
        state.read(0xFFFFF600, 2)
        state.write(0xFFFFF600, 2, 0)
        frame = _movement_test(state, frame, 0, 16)
        state.set_status_word(0x2500)
        frame = first_replace(frame, status=0)
    state.set_status_word(0x2700)
    frame = first_replace(frame, status=0)
    for address in (0xFFFFF362, 0xFFFFF612):
        value = frame.stack_cursor.word()
        frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))
        state.write(address, 2, value)
        frame = _movement_test(state, frame, value, 16)
    return frame


# Current complete resource/survivor Scene descendants, shared live fields.
def _movement_binary_flags(state: SceneState, frame: FirstDeploymentFrame, destination, source, width: int, subtract: bool=False) -> tuple[FirstDeploymentFrame, int]:
    destination, source = uint(destination, width), uint(source, width)
    if width not in (8, 16, 32) or type(subtract) is not bool:
        raise ValueError('original fixed-width movement arithmetic required')
    sign, mask = 1 << (width - 1), (1 << width) - 1
    if subtract:
        result = (destination - source) & mask
        carry = destination < source
        overflow = bool((destination ^ source) & (destination ^ result) & sign)
    else:
        result = (destination + source) & mask
        carry = destination + source > mask
        overflow = bool((~(destination ^ source)) & (destination ^ result) & sign)
    status = (17 if carry else 0) | (8 if result & sign else 0) | (4 if result == 0 else 0) | (2 if overflow else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, status=status), result


def _movement_arithmetic_long(state: SceneState, frame: FirstDeploymentFrame, carrier: str, source, subtract: bool=False) -> FirstDeploymentFrame:
    frame, result = _movement_binary_flags(state, frame, frame.carrier(carrier), source, 32, subtract)
    return first_replace(frame, **{carrier: result})


def _movement_test_long(state: SceneState, frame: FirstDeploymentFrame, value) -> FirstDeploymentFrame:
    value = uint(value, 32)
    status = (frame.status & 16) | (8 if value & 2147483648 else 0) | (4 if value == 0 else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, status=status)


def _movement_shift_long(state: SceneState, frame: FirstDeploymentFrame, carrier: str, right: bool=False) -> FirstDeploymentFrame:
    if type(right) is not bool:
        raise ValueError('actual eight-bit LONG shift direction required')
    value = frame.carrier(carrier)
    if right:
        result, carry = value >> 8, bool(value & 128)
    else:
        result, carry = (value << 8) & 4294967295, bool(value & 16777216)
    status = (17 if carry else 0) | (8 if result & 2147483648 else 0) | (4 if result == 0 else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, **{carrier: result}, status=status)


def _movement_multiply_word(state: SceneState, frame: FirstDeploymentFrame, carrier: str, source) -> FirstDeploymentFrame:
    result = low16(frame.carrier(carrier)) * uint(source, 16)
    return _movement_move_long(state, frame, carrier, result)


def _movement_address_carrier(frame: FirstDeploymentFrame, name: str):
    if name == 'roster':
        return frame.roster
    if name == 'candidates':
        return frame.candidates
    if name == 'controller':
        return frame.controller
    if name == 'scan':
        return frame.scan
    if name == 'opponent':
        return frame.opponent
    if name == 'scratch':
        return frame.scratch
    if name == 'auxiliary':
        return frame.auxiliary
    if name == 'stack_cursor':
        return frame.stack_cursor
    raise ValueError('known live movement address carrier required')


def _movement_save_longs(state: SceneState, frame: FirstDeploymentFrame, names: tuple) -> FirstDeploymentFrame:
    """MC68000 predecrement MOVEM uses original A7 when A7 is included."""
    numeric = ('target_x', 'target_y', 'unit', 'count', 'distance', 'offset_x', 'offset_y', 'choice')
    stack = frame.stack_cursor
    original_sp = stack.base
    for name in names[::-1]:
        if name in numeric:
            value = frame.carrier(name)
        elif name == 'stack_cursor':
            value = original_sp
        else:
            value = _movement_address_carrier(frame, name).base
        stack = stack.advance(-4)
        stack.set_long(0, value)
    return first_replace(frame, stack_cursor=stack)


def _movement_restore_longs(state: SceneState, frame: FirstDeploymentFrame, names: tuple) -> FirstDeploymentFrame:
    """Read every actual saved LONG; MOVEM postincrement wins over loaded A7."""
    numeric = ('target_x', 'target_y', 'unit', 'count', 'distance', 'offset_x', 'offset_y', 'choice')
    stack = frame.stack_cursor
    for name in names:
        value = stack.long()
        stack = stack.advance(4)
        if name in numeric:
            frame = first_replace(frame, **{name: value})
        elif name in ('roster', 'candidates', 'scan'):
            frame = first_replace(frame, **{name: state.table_at(value).cursor()})
        elif name in ('controller', 'opponent', 'scratch', 'auxiliary'):
            frame = first_replace(frame, **{name: state.table_at(value)})
        elif name != 'stack_cursor':
            raise ValueError('known actual MOVEM restore carrier required')
    return first_replace(frame, stack_cursor=stack)


def _movement_load_packed_resource(state: SceneState, frame: FirstDeploymentFrame, carrier: str, first: int, second_word_shift: bool=False) -> FirstDeploymentFrame:
    """Retain the original carrier before each BYTE and its exact shift widths."""
    if first not in (5, 9) or type(second_word_shift) is not bool:
        raise ValueError('actual packet resource BYTE block required')
    frame = _movement_move(state, frame, carrier, frame.roster.byte(0, first), 8)
    frame = _movement_fixed_shift_word(state, frame, carrier, 8)
    frame = _movement_move(state, frame, carrier, frame.roster.byte(0, first + 1), 8)
    if second_word_shift:
        frame = _movement_fixed_shift_word(state, frame, carrier, 8)
    else:
        frame = _movement_shift_long(state, frame, carrier)
    frame = _movement_move(state, frame, carrier, frame.roster.byte(0, first + 2), 8)
    frame = _movement_shift_long(state, frame, carrier)
    return _movement_move(state, frame, carrier, frame.roster.byte(0, first + 3), 8)


def _movement_store_packed_resource(state: SceneState, frame: FirstDeploymentFrame, carrier: str, first: int) -> FirstDeploymentFrame:
    if first not in (5, 9):
        raise ValueError('actual packet resource BYTE block required')
    for displacement, long_shift in ((first + 3, True), (first + 2, True), (first + 1, False)):
        value = low8(frame.carrier(carrier))
        frame.roster.set_byte(0, value, displacement)
        frame = _movement_test(state, frame, value, 8)
        if long_shift:
            frame = _movement_shift_long(state, frame, carrier, True)
        else:
            frame = _movement_fixed_shift_word(state, frame, carrier, 8, True)
    value = low8(frame.carrier(carrier))
    frame.roster.set_byte(0, value, first)
    return _movement_test(state, frame, value, 8)


def split_city_resources_into_group_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1807A: troop-weighted shares with real signed-division fields and RMW."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF6D6, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    pointer = state.table_at(0x1805A).long(low16(frame.target_x))
    frame = first_replace(frame, candidates=state.table_at(pointer).cursor())
    pointer = state.table_at(0x1806A).long(low16(frame.target_x))
    frame = first_replace(frame, controller=state.table_at(pointer))
    frame = _movement_move_long(state, frame, 'target_y', frame.candidates.long())
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 8, True)
    frame = first_replace(frame, opponent=state.table_at(0xFFFFC800))
    frame = _movement_move(state, frame, 'count', state.read(0xFFFFF3A6, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'count', 2)
    frame = _movement_move_long(state, frame, 'count', frame.opponent.long(low16(frame.count)))
    frame = _movement_arithmetic_long(state, frame, 'count', 100)
    frame = _movement_multiply_word(state, frame, 'target_y', low16(frame.count))
    frame = _movement_move_long(state, frame, 'distance', 0)
    frame = _movement_move(state, frame, 'distance', low16(frame.count), 16)
    while True:
        officer = frame.scan.word()
        frame = first_replace(frame, scan=frame.scan.advance(2))
        frame = _movement_move(state, frame, 'unit', officer, 16)
        if frame.status & 8:
            break
        frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 255, 16)
        frame = _movement_fixed_shift_word(state, frame, 'unit', 2)
        frame = _movement_arithmetic_long(state, frame, 'distance', frame.opponent.long(low16(frame.unit)))
        frame = _movement_arithmetic_long(state, frame, 'distance', 100)
    frame = _movement_move_long(state, frame, 'unit', frame.distance)
    frame = _movement_call(state, frame, 0x35760, 0x180C4)
    frame = _movement_shift_long(state, frame, 'target_y')
    frame, amount = _movement_binary_flags(state, frame, frame.candidates.long(), frame.target_y, 32, True)
    frame.candidates.set_long(0, amount)
    frame = _movement_load_packed_resource(state, frame, 'unit', 5)
    frame = _movement_arithmetic_long(state, frame, 'target_y', frame.unit)
    frame = _movement_compare_address(state, frame, frame.target_y, 999999)
    if not frame.status & 5:
        frame = _movement_move_long(state, frame, 'target_y', 999999)
    frame = _movement_store_packed_resource(state, frame, 'target_y', 5)
    frame = _movement_move_long(state, frame, 'target_y', frame.controller.long())
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 8, True)
    frame = _movement_multiply_word(state, frame, 'target_y', low16(frame.count))
    frame = _movement_move_long(state, frame, 'unit', frame.distance)
    frame = _movement_call(state, frame, 0x35760, 0x18114)
    frame = _movement_shift_long(state, frame, 'target_y')
    frame, amount = _movement_binary_flags(state, frame, frame.controller.long(), frame.target_y, 32, True)
    frame.controller.set_long(0, amount)
    frame = _movement_load_packed_resource(state, frame, 'unit', 9)
    frame = _movement_arithmetic_long(state, frame, 'target_y', frame.unit)
    frame = _movement_compare_address(state, frame, frame.target_y, 999999)
    if not frame.status & 5:
        frame = _movement_move_long(state, frame, 'target_y', 999999)
    return _movement_store_packed_resource(state, frame, 'target_y', 9)


def append_survivors_to_packed_group_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """181E8: original forward overlap copy followed by roster drain."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
    frame = first_replace(frame, candidates=frame.roster.at(low16(frame.target_x), 13).cursor())
    frame = first_replace(frame, scan=frame.candidates.cursor())
    frame, header = _movement_binary_flags(state, frame, frame.roster.byte(), low8(frame.offset_y), 8)
    frame.roster.set_byte(0, header)
    frame = _movement_add_word(state, frame, 'target_x', low16(frame.offset_y))
    frame = first_replace(frame, controller=frame.roster.at(low16(frame.target_x), 13))
    while True:
        frame = _movement_move(state, frame, 'target_x', frame.candidates.byte(), 8)
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
        if frame.status & 4:
            break
        frame = _movement_add_word(state, frame, 'target_x', 12)
        while True:
            value = frame.candidates.byte()
            frame = first_replace(frame, candidates=frame.candidates.advance(1))
            frame.controller.set_byte(0, value)
            frame = first_replace(frame, controller=frame.controller.advance(1))
            frame = _movement_test(state, frame, value, 8)
            frame = first_replace(frame, target_x=replace_word(frame.target_x, (low16(frame.target_x) - 1) & 65535))
            if low16(frame.target_x) == 65535:
                break
    while True:
        frame.controller.byte()
        frame.controller.set_byte(0, 0)
        frame = _movement_test(state, frame, 0, 8)
        frame = _movement_move(state, frame, 'target_x', frame.opponent.word(), 16)
        if frame.status & 8:
            return frame
        frame.opponent.set_word(0, 65535)
        frame = first_replace(frame, opponent=frame.opponent.advance(2))
        frame = _movement_test(state, frame, 65535, 16)
        value = low8(frame.target_x)
        frame.scan.set_byte(0, value)
        frame = first_replace(frame, scan=frame.scan.advance(1))
        frame = _movement_test(state, frame, value, 8)


def add_staged_resources_to_packed_group_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """18224: two capped resources; retain the second original WORD shift."""
    frame = _movement_frame(state, frame)
    frame = _movement_bit(state, frame, state.read(0xFFFFF6D7, 1), 1)
    if frame.status & 4:
        frame = first_replace(frame, scan=state.table_at(0xFFFFF696).cursor(), opponent=state.table_at(0xFFFFF69E))
    else:
        frame = first_replace(frame, scan=state.table_at(0xFFFFF69A).cursor(), opponent=state.table_at(0xFFFFF6A2))
    frame = _movement_load_packed_resource(state, frame, 'target_x', 5)
    frame = _movement_arithmetic_long(state, frame, 'target_x', frame.scan.long())
    frame = _movement_compare_address(state, frame, frame.target_x, 999999)
    if not frame.status & 5:
        frame = _movement_move_long(state, frame, 'target_x', 999999)
    frame = _movement_store_packed_resource(state, frame, 'target_x', 5)
    frame = _movement_load_packed_resource(state, frame, 'target_x', 9, True)
    frame = _movement_arithmetic_long(state, frame, 'target_x', frame.opponent.long())
    frame = _movement_compare_address(state, frame, frame.target_x, 999999)
    if not frame.status & 5:
        frame = _movement_move_long(state, frame, 'target_x', 999999)
    frame = _movement_store_packed_resource(state, frame, 'target_x', 9)
    for view in (frame.scan, frame.opponent):
        view.long()
        view.set_long(0, 0)
        frame = _movement_test_long(state, frame, 0)
    return frame


def assign_city_survivor_roster_tokens_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """182C4: merge first, then original owner+105 tokens and cleared positions."""
    frame = _movement_frame(state, frame)
    saved = ('target_x', 'target_y', 'unit', 'count', 'roster', 'opponent', 'scratch')
    frame = _movement_save_longs(state, frame, saved)
    frame = _movement_call(state, frame, 0x1830A, 0x182CC)
    frame = first_replace(frame, roster=state.table_at(0xFFFFCC00).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF68A, 2), 16)
    frame = _movement_move(state, frame, 'count', state.read(0xFFFFF68C, 2), 16)
    frame = _movement_bit(state, frame, state.read(0xFFFFF6D7, 1), 1)
    if not frame.status & 4:
        frame = _movement_move(state, frame, 'count', state.read(0xFFFFF68E, 2), 16)
    frame = _movement_add_word(state, frame, 'count', 105)
    frame = first_replace(frame, scratch=state.table_at(0xFFFFA150))
    while True:
        officer = frame.opponent.word()
        frame = first_replace(frame, opponent=frame.opponent.advance(2))
        frame = _movement_move(state, frame, 'target_y', officer, 16)
        if frame.status & 8:
            return _movement_restore_longs(state, frame, saved)
        frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 255, 16)
        value = low8(frame.count)
        frame.roster.set_byte(low16(frame.target_y), value)
        frame = _movement_test(state, frame, value, 8)
        frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
        frame.scratch.long(low16(frame.target_y))
        frame.scratch.set_long(low16(frame.target_y), 0)
        frame = _movement_test_long(state, frame, 0)


def merge_city_survivor_rosters_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1830A: append the actual second roster and release over-ten tail members.

    Every MOVEM save/restore uses live RAM. Only the original three visible
    owners show messages, through the shared current260E4 core and real slots.
    """
    frame = _movement_frame(state, frame)
    saved = ('target_x', 'target_y', 'unit', 'scan', 'opponent', 'scratch', 'auxiliary')
    frame = _movement_save_longs(state, frame, saved)
    frame = first_replace(frame, scratch=state.table_at(0xFFFFA57A))
    frame = _movement_bit(state, frame, state.read(0xFFFFF6D7, 1), 1)
    if not frame.status & 4:
        frame = first_replace(frame, scratch=state.table_at(0xFFFFA5CE))
    frame = first_replace(frame, scan=frame.scratch.cursor())
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    while True:
        officer = frame.opponent.word()
        frame = first_replace(frame, opponent=frame.opponent.advance(2))
        frame = _movement_test(state, frame, officer, 16)
        if frame.status & 8:
            break
        frame = _movement_adjust_word(state, frame, 'target_x', 1)
    frame = first_replace(frame, opponent=frame.opponent.advance(-2))
    while True:
        officer = frame.scratch.word()
        frame = first_replace(frame, scratch=frame.scratch.advance(2))
        frame.opponent.set_word(0, officer)
        frame = first_replace(frame, opponent=frame.opponent.advance(2))
        frame = _movement_test(state, frame, officer, 16)
        if frame.status & 8:
            break
        frame = _movement_adjust_word(state, frame, 'target_x', 1)
    frame.scan.set_word(0, 65535)
    frame = _movement_test(state, frame, 65535, 16)
    frame = _movement_compare(state, frame, low16(frame.target_x), 10, 16)
    if frame.status & 5:
        return _movement_restore_longs(state, frame, saved)
    frame, extra = _movement_binary_flags(state, frame, low16(frame.target_x), 11, 16, True)
    frame = first_replace(frame, target_x=replace_word(frame.target_x, extra), opponent=frame.opponent.advance(-2))
    frame = _movement_move(state, frame, 'unit', state.read(0xFFFFF68A, 2), 16)
    old_bit = bool(frame.unit & 128)
    status = (frame.status & 27) | (0 if old_bit else 4)
    frame = first_replace(frame, unit=frame.unit | 128, status=status)
    state.sr = (state.sr & 65504) | status
    frame = first_replace(frame, auxiliary=state.table_at(0xFFFFCC00))
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF68C, 2), 16)
    frame = _movement_bit(state, frame, state.read(0xFFFFF6D7, 1), 1)
    if not frame.status & 4:
        frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF68E, 2), 16)
    visible = False
    for address in (0xFFFFF67A, 0xFFFFF67C, 0xFFFFF67E):
        frame = _movement_compare(state, frame, low16(frame.target_y), state.read(address, 2), 16)
        if frame.status & 4:
            visible = True
            break
    all_saved = ('target_x', 'target_y', 'unit', 'count', 'distance', 'offset_x', 'offset_y', 'choice',
                 'roster', 'candidates', 'controller', 'scan', 'opponent', 'scratch', 'auxiliary', 'stack_cursor')
    while True:
        source = frame.opponent.advance(-2)
        frame = first_replace(frame, opponent=source)
        frame = _movement_move(state, frame, 'target_y', source.word(), 16)
        if visible:
            state.write(0xFFFFF3D0, 2, low16(frame.target_y))
            frame = _movement_test(state, frame, low16(frame.target_y), 16)
        token = low8(frame.unit)
        frame.auxiliary.set_byte(low16(frame.target_y), token)
        frame = _movement_test(state, frame, token, 8)
        if visible:
            frame = _movement_save_longs(state, frame, all_saved)
            state.write(0xFFFFF740, 2, 320)
            frame = _movement_test(state, frame, 320, 16)
            frame = _movement_call(state, frame, 0x260E4, 0x183AC)
            frame = _movement_restore_longs(state, frame, all_saved)
        frame = first_replace(frame, target_x=replace_word(frame.target_x, (low16(frame.target_x) - 1) & 65535))
        if low16(frame.target_x) == 65535:
            break
    frame.opponent.set_word(0, 65535)
    frame = _movement_test(state, frame, 65535, 16)
    return _movement_restore_longs(state, frame, saved)


def _movement_divu_word(state: SceneState, frame: FirstDeploymentFrame, carrier: str, divisor, instruction) -> FirstDeploymentFrame:
    divisor = uint(divisor, 16)
    if divisor == 0:
        raise MovementContinuationBoundary(instruction, frame, 'original DIVU requires its actual divide-by-zero exception fields')
    quotient, remainder = divmod(frame.carrier(carrier), divisor)
    if quotient > 65535:
        raise MovementContinuationBoundary(instruction, frame, 'original DIVU overflow leaves N/Z undefined for the complete return')
    result = (remainder << 16) | quotient
    frame = first_replace(frame, **{carrier: result})
    return _movement_test(state, frame, quotient, 16)


def divide_longs_by_word_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """357DA: two DIVUs with original D1/D3 WORD saves, swaps and live restores."""
    frame = _movement_frame(state, frame)
    stack = frame.stack_cursor.advance(-2)
    stack.set_word(0, low16(frame.count))
    stack = stack.advance(-2)
    stack.set_word(0, low16(frame.target_y))
    frame = first_replace(frame, stack_cursor=stack)
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    swapped = ((frame.target_y << 16) | (frame.target_y >> 16)) & 4294967295
    frame = _movement_move_long(state, frame, 'target_y', swapped)
    frame = _movement_divu_word(state, frame, 'target_y', low16(frame.unit), 0x357E2)
    frame = _movement_move(state, frame, 'count', low16(frame.target_y), 16)
    saved_word = frame.stack_cursor.word()
    frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))
    frame = _movement_move(state, frame, 'target_y', saved_word, 16)
    frame = _movement_divu_word(state, frame, 'target_y', low16(frame.unit), 0x357E8)
    swapped = ((frame.target_y << 16) | (frame.target_y >> 16)) & 4294967295
    frame = _movement_move_long(state, frame, 'target_y', swapped)
    frame = _movement_move_long(state, frame, 'unit', 0)
    frame = _movement_move(state, frame, 'unit', low16(frame.target_y), 16)
    frame = _movement_move(state, frame, 'target_y', low16(frame.count), 16)
    swapped = ((frame.target_y << 16) | (frame.target_y >> 16)) & 4294967295
    frame = _movement_move_long(state, frame, 'target_y', swapped)
    saved_word = frame.stack_cursor.word()
    frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))
    return _movement_move(state, frame, 'count', saved_word, 16)


def unsigned_divmod_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3577A: original corrected quotient estimate, not a replacement divmod."""
    frame = _movement_frame(state, frame)
    frame = _movement_compare_address(state, frame, frame.unit, 65535)
    if frame.status & 5:
        return divide_longs_by_word_fields(state, frame)
    frame = _movement_compare_address(state, frame, frame.unit, frame.target_y)
    if frame.status & 4:
        frame = _movement_move_long(state, frame, 'target_y', 1)
        return _movement_move_long(state, frame, 'unit', 0)
    if not frame.status & 5:
        frame = _movement_move_long(state, frame, 'unit', frame.target_y)
        return _movement_move_long(state, frame, 'target_y', 0)
    saved = ('count', 'distance', 'offset_x')
    frame = _movement_save_longs(state, frame, saved)
    frame = _movement_move_long(state, frame, 'count', frame.unit)
    frame = _movement_move(state, frame, 'count', 0, 16)
    swapped = ((frame.count << 16) | (frame.count >> 16)) & 4294967295
    frame = _movement_move_long(state, frame, 'count', swapped)
    frame = _movement_arithmetic_long(state, frame, 'count', 1)
    frame = _movement_move_long(state, frame, 'distance', frame.target_y)
    frame = _movement_move_long(state, frame, 'offset_x', frame.unit)
    frame = _movement_move_long(state, frame, 'unit', frame.count)
    frame = _movement_call(state, frame, 0x357DA, 0x357A8)
    frame = _movement_move_long(state, frame, 'unit', frame.offset_x)
    frame = _movement_divu_word(state, frame, 'unit', low16(frame.count), 0x357AA)
    frame = _movement_divu_word(state, frame, 'target_y', low16(frame.unit), 0x357AC)
    frame = _movement_move_long(state, frame, 'target_y', frame.target_y & 65535)
    while True:
        frame = _movement_move_long(state, frame, 'unit', frame.offset_x)
        frame = _movement_move_long(state, frame, 'count', frame.offset_x)
        swapped = ((frame.count << 16) | (frame.count >> 16)) & 4294967295
        frame = _movement_move_long(state, frame, 'count', swapped)
        frame = _movement_multiply_word(state, frame, 'unit', low16(frame.target_y))
        frame = _movement_multiply_word(state, frame, 'count', low16(frame.target_y))
        swapped = ((frame.count << 16) | (frame.count >> 16)) & 4294967295
        frame = _movement_move_long(state, frame, 'count', swapped)
        frame = _movement_arithmetic_long(state, frame, 'unit', frame.count)
        frame = _movement_arithmetic_long(state, frame, 'unit', frame.distance, True)
        if not frame.status & 5:
            frame = _movement_arithmetic_long(state, frame, 'target_y', 1, True)
            continue
        frame, remainder = _movement_binary_flags(state, frame, 0, frame.unit, 32, True)
        frame = first_replace(frame, unit=remainder)
        frame = _movement_compare_address(state, frame, frame.offset_x, frame.unit)
        if not frame.status & 5:
            return _movement_restore_longs(state, frame, saved)
        frame = _movement_arithmetic_long(state, frame, 'target_y', 1)


def positive_denominator_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3576C: signed numerator correction, with actual35774 internal BSR."""
    frame = _movement_frame(state, frame)
    frame = _movement_test_long(state, frame, frame.target_y)
    if not frame.status & 8:
        return unsigned_divmod_fields(state, frame)
    frame, positive = _movement_binary_flags(state, frame, 0, frame.target_y, 32, True)
    frame = first_replace(frame, target_y=positive)
    frame = _movement_call(state, frame, 0x3577A, 0x35774)
    frame, quotient = _movement_binary_flags(state, frame, 0, frame.target_y, 32, True)
    frame = first_replace(frame, target_y=quotient)
    frame, remainder = _movement_binary_flags(state, frame, 0, frame.unit, 32, True)
    return first_replace(frame, unit=remainder)


def signed_divmod_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """35760: signed denominator correction; fallthrough is not an extra call."""
    frame = _movement_frame(state, frame)
    frame = _movement_test_long(state, frame, frame.unit)
    if not frame.status & 8:
        return positive_denominator_fields(state, frame)
    frame, positive = _movement_binary_flags(state, frame, 0, frame.unit, 32, True)
    frame = first_replace(frame, unit=positive)
    frame = _movement_call(state, frame, 0x3576C, 0x35768)
    frame, quotient = _movement_binary_flags(state, frame, 0, frame.target_y, 32, True)
    return first_replace(frame, target_y=quotient)


"""Sole current Scene path rules, inheriting the existing weighted-frontier design.

The helpers below group business operations, not decoded instruction execution.
Every original narrow carrier, real DATA access and physical save/call slot is
explicit. No unreachable-target limit or fabricated frontier success is added.
"""


def _path_store_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, value: int, width: int) -> FirstDeploymentFrame:
    """Original RAM MOVE and its flags; this is not a hardware callback."""
    if width not in (8,16):
        raise ValueError('path store requires its actual BYTE or WORD width')
    state.write(address,width//8,uint(value,width))
    return _movement_test(state,frame,value,width)


def _path_adjust_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, amount: int, width: int=16) -> FirstDeploymentFrame:
    """Reuse the sole fixed-width arithmetic; keep the untouched high bits."""
    if amount not in (-1,1,2) or width not in (8,16):
        raise ValueError('original path quick adjustment required')
    old=low8(frame.carrier(name)) if width==8 else low16(frame.carrier(name))
    frame,value=_movement_binary_flags(state,frame,old,abs(amount),width,amount<0)
    retained=replace_byte(frame.carrier(name),value) if width==8 else replace_word(frame.carrier(name),value)
    return first_replace(frame,**{name:retained})


def _path_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Own only the actual inner BSR LONG, never the external caller's slot."""
    stack=frame.stack_cursor.advance(-4)
    stack.set_long(0,uint(continuation,32))
    entered=first_replace(frame,stack_cursor=stack)
    if target==0x6562:
        returned=initialize_path_grid_fields(state,entered)
    elif target==0x6624:
        returned=normalize_path_coordinates_fields(state,entered)
    elif target==0x664E:
        returned=expand_path_frontier_fields(state,entered)
    elif target==0x66C2:
        returned=visit_path_neighbor_fields(state,entered)
    elif target==0x66EE:
        returned=path_neighbor_is_goal_fields(state,entered)
    elif target==0x6710:
        returned=mark_path_direction_fields(state,entered)
    elif target==0x672C:
        returned=read_path_direction_fields(state,entered)
    elif target==0x6748:
        returned=read_path_cost_fields(state,entered)
    elif target==0x6764:
        returned=reconstruct_path_fields(state,entered)
    elif target==0x678E:
        returned=step_back_path_fields(state,entered)
    else:
        raise MovementContinuationBoundary(target,entered,'unknown path child retains its actual call slot')
    returned=_movement_frame(state,returned)
    actual=returned.stack_cursor.long()
    if actual!=continuation:
        raise FirstDeploymentReturnBoundary(actual,returned,continuation)
    return first_replace(returned,stack_cursor=returned.stack_cursor.advance(4))


def _path_carry_fields(state: SceneState, frame: FirstDeploymentFrame,
        carry: int, instruction: int) -> FirstDeploymentFrame:
    """Original full-SR bit operation, without simulated trap/trace progress."""
    if carry not in (0,1):
        raise ValueError('actual carry zero or one required')
    if not state.sr&0x2000 or state.sr&0x8000:
        raise MovementContinuationBoundary(instruction,frame,'original privileged/trace SR continuation is not observed')
    status=(frame.status&30)|carry
    state.set_status_word((state.sr&65504)|status)
    return first_replace(frame,status=status)


def _path_grid_index_fields(state: SceneState, frame: FirstDeploymentFrame,
        coordinate: str) -> FirstDeploymentFrame:
    """The shared WORD row-stride calculation, retaining the real D2 prefix."""
    if coordinate not in ('target_x','distance'):
        raise ValueError('only the original D0 or D4 grid index carrier is valid')
    frame=_movement_move(state,frame,'unit',low16(frame.carrier(coordinate)),16)
    frame=_movement_fixed_shift_word(state,frame,'unit',3)
    frame=_movement_add_word(state,frame,coordinate,low16(frame.unit))
    frame=_movement_fixed_shift_word(state,frame,coordinate,3)
    frame=_movement_add_word(state,frame,coordinate,low16(frame.target_y))
    frame=_movement_fixed_shift_word(state,frame,coordinate,1)
    return first_replace(frame,controller=state.table_at(0xFF0000))


def _path_occupied_cell_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """One existing transport/group obstruction rule, not a second grid algorithm."""
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'target_y',frame.candidates.byte(0,1),8)
    frame=_movement_move(state,frame,'unit',low16(frame.target_y),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',3)
    frame=_movement_add_word(state,frame,'target_y',low16(frame.unit))
    frame=_movement_fixed_shift_word(state,frame,'target_y',3)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=_movement_move(state,frame,'unit',frame.candidates.byte(0,2),8)
    frame=_movement_add_word(state,frame,'target_y',low16(frame.unit))
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    return _path_store_fields(state,frame,frame.roster.address(low16(frame.target_y)),127,16)


def build_path_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """6518: normalize pixel coordinates, then run the sole weighted frontier."""
    frame=_movement_frame(state,frame)
    frame=_path_call_fields(state,frame,0x6624,0x651C)
    return build_path_from_cells_fields(state,frame)


def build_path_from_cells_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """651C genuine middle entry; no additional call exists at the shared tail."""
    frame=_movement_frame(state,frame)
    frame=_path_call_fields(state,frame,0x6562,0x6520)
    frame=first_replace(frame,scratch=state.table_at(0xFF4000),auxiliary=state.table_at(0xFF4800))
    frame=_path_store_fields(state,frame,frame.scratch.base,state.read(0xFFFFF641,1),8)
    frame=_path_store_fields(state,frame,frame.scratch.address(0,1),state.read(0xFFFFF643,1),8)
    frame=_path_store_fields(state,frame,frame.scratch.address(0,2),1,8)
    frame=_path_store_fields(state,frame,frame.scratch.address(0,3),255,8)
    frame=_movement_move(state,frame,'offset_x',0,16)
    while True:
        frame=first_replace(frame,roster=frame.scratch.cursor(),candidates=frame.auxiliary.cursor())
        frame=_path_call_fields(state,frame,0x664E,0x654C)
        if frame.status&1:
            break
        frame=first_replace(frame,scratch=frame.auxiliary,auxiliary=frame.scratch)
        frame=_path_adjust_fields(state,frame,'offset_x',1)
    frame=_path_adjust_fields(state,frame,'offset_x',1)
    frame=_path_store_fields(state,frame,0xFFFFF644,low16(frame.offset_x),16)
    return _path_call_fields(state,frame,0x6764,0x6560)


def initialize_path_grid_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """6562: terrain costs, transport/group obstacles, and the city-marker pairs."""
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(0xFF0000).cursor(),
        candidates=state.table_at(0xEE5F0).cursor(),controller=state.table_at(0x670A))
    frame=_movement_move(state,frame,'target_x',5183,16)
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'unit',0,16)
    while True:
        terrain=frame.candidates.byte()
        frame=first_replace(frame,candidates=frame.candidates.advance(1))
        frame=_movement_move(state,frame,'target_y',terrain,8)
        frame=_movement_move(state,frame,'unit',frame.controller.byte(low16(frame.target_y)),8)
        frame=_path_store_fields(state,frame,frame.roster.base,low16(frame.unit),16)
        frame=first_replace(frame,roster=frame.roster.advance(2),
            target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
        if low16(frame.target_x)==65535:
            break
    frame=first_replace(frame,roster=state.table_at(0xFF0000).cursor(),candidates=state.table_at(0xFFFFCE00).cursor())
    frame=_movement_move(state,frame,'target_x',39,16)
    while True:
        frame=_movement_test(state,frame,frame.candidates.byte(),8)
        if not frame.status&4:
            value=frame.candidates.byte()
            status=(frame.status&27)|(4 if not value&16 else 0)
            state.sr=(state.sr&65504)|status
            frame=first_replace(frame,status=status)
            if frame.status&4:
                frame=_path_occupied_cell_fields(state,frame)
        frame=first_replace(frame,candidates=frame.candidates.advance(4),
            target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
        if low16(frame.target_x)==65535:
            break
    frame=first_replace(frame,candidates=state.table_at(0xFFFF9000).cursor())
    while True:
        frame=_movement_move(state,frame,'target_x',frame.candidates.byte(),8)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&15,16)
        if frame.status&4:
            break
        frame=_path_occupied_cell_fields(state,frame)
        frame=first_replace(frame,candidates=frame.candidates.at(low16(frame.target_x),13).cursor())
    frame=first_replace(frame,candidates=state.table_at(0xD4ACA).cursor())
    frame=_movement_move(state,frame,'target_x',39,16)
    while True:
        first=frame.candidates.word()
        frame=first_replace(frame,candidates=frame.candidates.advance(2))
        frame=_movement_move(state,frame,'target_y',first,16)
        frame=_movement_fixed_shift_word(state,frame,'target_y',4,True)
        second=frame.candidates.word()
        frame=first_replace(frame,candidates=frame.candidates.advance(2))
        frame=_movement_move(state,frame,'unit',second,16)
        frame=_movement_fixed_shift_word(state,frame,'unit',4,True)
        frame=_movement_move(state,frame,'count',low16(frame.unit),16)
        frame=_movement_fixed_shift_word(state,frame,'unit',3)
        frame=_movement_add_word(state,frame,'unit',low16(frame.count))
        frame=_movement_fixed_shift_word(state,frame,'unit',3)
        frame=_movement_add_word(state,frame,'unit',low16(frame.target_y))
        frame=_movement_fixed_shift_word(state,frame,'unit',1)
        frame=_path_store_fields(state,frame,frame.roster.address(low16(frame.unit),-2),255,16)
        frame=_path_store_fields(state,frame,frame.roster.address(low16(frame.unit)),255,16)
        frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
        if low16(frame.target_x)==65535:
            return frame


def normalize_path_coordinates_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """6624: original four live WORD coordinates are divided by sixteen in order."""
    frame=_movement_frame(state,frame)
    for address in (0xFFFFF63C,0xFFFFF63E,0xFFFFF640,0xFFFFF642):
        frame=_movement_move(state,frame,'target_x',state.read(address,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_x',4,True)
        frame=_path_store_fields(state,frame,address,low16(frame.target_x),16)
    return frame


def expand_path_frontier_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """664E: retain countdown nodes or test four original neighbors, in order."""
    frame=_movement_frame(state,frame)
    while True:
        frame=_movement_move(state,frame,'target_x',0,16)
        first=frame.roster.byte()
        frame=first_replace(frame,roster=frame.roster.advance(1))
        frame=_movement_move(state,frame,'target_x',first,8)
        frame=_movement_move(state,frame,'target_y',0,16)
        second=frame.roster.byte()
        frame=first_replace(frame,roster=frame.roster.advance(1))
        frame=_movement_move(state,frame,'target_y',second,8)
        countdown=frame.roster.byte()
        frame=first_replace(frame,roster=frame.roster.advance(1))
        frame=_movement_move(state,frame,'unit',countdown,8)
        frame=_path_adjust_fields(state,frame,'unit',-1,8)
        if not frame.status&4:
            for name in ('target_x','target_y','unit'):
                frame=_path_store_fields(state,frame,frame.candidates.base,low8(frame.carrier(name)),8)
                frame=first_replace(frame,candidates=frame.candidates.advance(1))
        else:
            frame=_path_adjust_fields(state,frame,'target_x',-1)
            if not frame.status&1:
                frame=_movement_move(state,frame,'count',3,16)
                frame=_path_call_fields(state,frame,0x66C2,0x6672)
                if frame.status&1:
                    return frame
            frame=_path_adjust_fields(state,frame,'target_x',1)
            frame=_path_adjust_fields(state,frame,'target_y',-1)
            if not frame.status&1:
                frame=_movement_move(state,frame,'count',2,16)
                frame=_path_call_fields(state,frame,0x66C2,0x6684)
                if frame.status&1:
                    return frame
            frame=_path_adjust_fields(state,frame,'target_y',2)
            frame=_movement_compare(state,frame,low16(frame.target_y),72,16)
            if frame.status&1:
                frame=_movement_move(state,frame,'count',4,16)
                frame=_path_call_fields(state,frame,0x66C2,0x6698)
                if frame.status&1:
                    return frame
            frame=_path_adjust_fields(state,frame,'target_x',1)
            frame=_movement_compare(state,frame,low16(frame.target_x),72,16)
            if frame.status&1:
                frame=_path_adjust_fields(state,frame,'target_y',-1)
                frame=_movement_move(state,frame,'count',1,16)
                frame=_path_call_fields(state,frame,0x66C2,0x66B0)
                if frame.status&1:
                    return frame
        frame=_movement_test(state,frame,frame.roster.byte(),8)
        if frame.status&8:
            break
    frame=_path_store_fields(state,frame,frame.candidates.base,255,8)
    return _path_carry_fields(state,frame,0,0x66BC)


def visit_path_neighbor_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """66C2: stop at the goal, else enqueue only unvisited traversable cells."""
    from .domain import s8
    frame=_movement_frame(state,frame)
    frame=_path_call_fields(state,frame,0x66EE,0x66C6)
    if frame.status&1:
        return frame
    frame=_path_call_fields(state,frame,0x672C,0x66CE)
    frame=_movement_test(state,frame,low8(frame.unit),8)
    if not frame.status&4:
        return _path_carry_fields(state,frame,0,0x66E8)
    frame=_path_call_fields(state,frame,0x6748,0x66D6)
    frame=_movement_test(state,frame,low8(frame.unit),8)
    if frame.status&8:
        return _path_carry_fields(state,frame,0,0x66E8)
    frame=_path_store_fields(state,frame,frame.candidates.base,low8(frame.target_x),8)
    frame=first_replace(frame,candidates=frame.candidates.advance(1))
    frame=_movement_move(state,frame,'target_x',u16(s8(low8(frame.target_x))),16)
    frame=_path_store_fields(state,frame,frame.candidates.base,low8(frame.target_y),8)
    frame=first_replace(frame,candidates=frame.candidates.advance(1))
    frame=_movement_move(state,frame,'target_y',u16(s8(low8(frame.target_y))),16)
    frame=_path_store_fields(state,frame,frame.candidates.base,low8(frame.unit),8)
    frame=first_replace(frame,candidates=frame.candidates.advance(1))
    frame=_path_call_fields(state,frame,0x6710,0x66E8)
    return _path_carry_fields(state,frame,0,0x66E8)


def path_neighbor_is_goal_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """66EE: exact live destination comparison and original mark-before-carry."""
    frame=_movement_frame(state,frame)
    frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF63C,2),16)
    if frame.status&4:
        frame=_movement_compare(state,frame,low16(frame.target_y),state.read(0xFFFFF63E,2),16)
        if frame.status&4:
            frame=_path_call_fields(state,frame,0x6710,0x66FE)
            return _path_carry_fields(state,frame,1,0x66FE)
    return _path_carry_fields(state,frame,0,0x6704)


def mark_path_direction_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """6710: real LONG D0 save/readback surrounds the shared grid-index core."""
    frame=_movement_frame(state,frame)
    stack=frame.stack_cursor.advance(-4)
    stack.set_long(0,frame.target_x)
    frame=first_replace(frame,stack_cursor=stack)
    frame=_movement_test_long(state,frame,frame.target_x)
    frame=_path_grid_index_fields(state,frame,'target_x')
    frame=_path_store_fields(state,frame,frame.controller.address(low16(frame.target_x)),low8(frame.count),8)
    restored=frame.stack_cursor.long()
    frame=first_replace(frame,stack_cursor=frame.stack_cursor.advance(4))
    return _movement_move_long(state,frame,'target_x',restored)


def read_path_direction_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """672C: WORD D0 save; the loaded BYTE retains D2's real index prefix."""
    frame=_movement_frame(state,frame)
    stack=frame.stack_cursor.advance(-2)
    stack.set_word(0,low16(frame.target_x))
    frame=first_replace(frame,stack_cursor=stack)
    frame=_movement_test(state,frame,low16(frame.target_x),16)
    frame=_path_grid_index_fields(state,frame,'target_x')
    frame=_movement_move(state,frame,'unit',frame.controller.byte(low16(frame.target_x)),8)
    restored=frame.stack_cursor.word()
    frame=first_replace(frame,stack_cursor=frame.stack_cursor.advance(2))
    return _movement_move(state,frame,'target_x',restored,16)


def read_path_cost_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """6748: original D4 index and CLR.W D2 precede the live cost BYTE read."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'distance',low16(frame.target_x),16)
    frame=_path_grid_index_fields(state,frame,'distance')
    frame=_movement_move(state,frame,'unit',0,16)
    return _movement_move(state,frame,'unit',frame.controller.byte(low16(frame.distance),1),8)


def reconstruct_path_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """6764: follow the existing direction BYTEs backwards until the real source."""
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(0xFF4000).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF63C,2),16)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF63E,2),16)
    while True:
        frame=_path_call_fields(state,frame,0x672C,0x6774)
        frame=_path_store_fields(state,frame,frame.roster.base,low8(frame.unit),8)
        frame=first_replace(frame,roster=frame.roster.advance(1))
        frame=_path_call_fields(state,frame,0x678E,0x677A)
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF640,2),16)
        if frame.status&4:
            frame=_movement_compare(state,frame,low16(frame.target_y),state.read(0xFFFFF642,2),16)
            if frame.status&4:
                break
    return _path_store_fields(state,frame,frame.roster.base,255,8)


def step_back_path_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """678E: original decrementing direction dispatch, including retained D2 BYTE."""
    frame=_movement_frame(state,frame)
    frame=_path_adjust_fields(state,frame,'unit',-1,8)
    if frame.status&4:
        return _path_adjust_fields(state,frame,'target_x',-1)
    frame=_path_adjust_fields(state,frame,'unit',-1,8)
    if frame.status&4:
        return _path_adjust_fields(state,frame,'target_y',1)
    frame=_path_adjust_fields(state,frame,'unit',-1,8)
    if frame.status&4:
        return _path_adjust_fields(state,frame,'target_x',1)
    return _path_adjust_fields(state,frame,'target_y',-1)
