"""Complete live-Scene transport direction, arrival credit and collision rules.

The original 16874..16922 and 16946..169AA owners retain all D/A carriers,
partial-register writes and full-SR low-bit residues. Their callers own the
existing CALL LONG and RTS read. No scalar GameState, RAM copy, route repair,
host phase update or resource payload is introduced here.
"""
from ..high_level_scene_flows.domain import (
    SceneState, low8, low16, s16, u16, replace_word,
)
from ..high_level_battle_ai.contexts_first_deployment import (
    FirstDeploymentFrame, first_replace,
)
from ..high_level_battle_ai.business_formation import _first_compare_long
from ..high_level_main_flows.business_movement_support import (
    _movement_frame, _movement_move, _movement_move_long, _movement_test,
    _movement_compare, _movement_fixed_shift_word, _movement_binary_flags,
    _movement_arithmetic_long,
)


def _credit_transport_destination_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """168C6..16920: add both actual award LONGs, wrapping before each cap."""
    # Local imports keep the city caller and its transport successor acyclic.
    from ..high_level_remaining_flows.business_city import (
        _group_route_store_fields, _group_route_carry_fields,
    )
    frame = _movement_move(state, frame, 'unit', 0, 16)
    frame = _movement_move(state, frame, 'unit', frame.auxiliary.byte(), 8)
    frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 3, 16)
    frame = _movement_fixed_shift_word(state, frame, 'unit', 3)
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    frame = _movement_move(state, frame, 'target_y', frame.auxiliary.byte(0, 3), 8)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
    frame = first_replace(frame, candidates=state.table_at(0x13B60).cursor())
    for award_displacement, resource_base in ((0, 0xFFFFDFFC), (4, 0xFFFFE09C)):
        frame = _movement_move_long(state, frame, 'count',
            frame.candidates.long(low16(frame.unit), award_displacement))
        frame = first_replace(frame, controller=state.table_at(resource_base))
        frame = _movement_arithmetic_long(state, frame, 'count',
            frame.controller.long(low16(frame.target_y)))
        frame = _first_compare_long(frame, frame.count, 999999)
        state.sr = (state.sr & 65504) | frame.status
        if not frame.status & 5:
            frame = _movement_move_long(state, frame, 'count', 999999)
        frame = _group_route_store_fields(state, frame,
            frame.controller.address(low16(frame.target_y)), frame.count, 4)
    frame = _group_route_store_fields(state, frame,
        frame.auxiliary.address(), 0, 1, True)
    return _group_route_carry_fields(state, frame, True)


def transport_direction_or_arrival_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """16874..16922: consume the real signed-indexed route or credit arrival.

    CEAC increments before the next-BYTE terminator test. Directions other
    than 1/2/3 keep the original fourth-direction fallthrough; neither the
    route nor its index is validated, clamped or replaced.
    """
    from ..high_level_remaining_flows.business_city import (
        _group_route_memory_delta_fields, _group_route_register_delta_fields,
        _group_route_carry_fields,
    )
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0x00FF4000).cursor())
    frame = first_replace(frame, roster=frame.roster.advance(
        s16(state.read(0xFFFFCEAC, 2))))
    frame = _group_route_memory_delta_fields(state, frame, 0xFFFFCEAC, 1)
    frame = _movement_test(state, frame, frame.roster.byte(0, 1), 8)
    if frame.status & 8:
        return _credit_transport_destination_fields(state, frame)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)
    frame = _group_route_register_delta_fields(state, frame, 'target_x', -1, 8)
    if frame.status & 4:
        frame = _movement_move(state, frame, 'target_x', 65520, 16)
        frame = _movement_move(state, frame, 'target_y', 0, 16)
    else:
        frame = _group_route_register_delta_fields(state, frame, 'target_x', -1, 8)
        if frame.status & 4:
            frame = _movement_move(state, frame, 'target_x', 0, 16)
            frame = _movement_move(state, frame, 'target_y', 16, 16)
        else:
            frame = _group_route_register_delta_fields(state, frame, 'target_x', -1, 8)
            if frame.status & 4:
                frame = _movement_move(state, frame, 'target_x', 16, 16)
                frame = _movement_move(state, frame, 'target_y', 0, 16)
            else:
                frame = _movement_move(state, frame, 'target_x', 0, 16)
                frame = _movement_move(state, frame, 'target_y', 65520, 16)
    for address, displacement in ((0xFFFFCEA8, frame.target_x),
                                  (0xFFFFCEAA, frame.target_y)):
        frame, value = _movement_binary_flags(state, frame,
            state.read(address, 2), low16(displacement), 16, False)
        state.write(address, 2, value)
    return _group_route_carry_fields(state, frame, False)


def transport_collision_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """16946..169AA: scan 40 transports, then the live variable-stride groups.

    The forty-record DBRA keeps CCR unchanged and retains D2's upper WORD.
    Packed group stride is the actual low nibble plus thirteen; the original
    sentinel is the only end condition, with no host iteration limit.
    """
    from ..high_level_remaining_flows.business_city import (
        _group_route_bit_fields, _group_route_carry_fields,
    )
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFCEA8, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 4, True)
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFCEAA, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 4, True)
    frame = first_replace(frame, roster=state.table_at(0xFFFFCE00).cursor())
    frame = _movement_move(state, frame, 'unit', 39, 16)
    while True:
        frame = _movement_test(state, frame, frame.roster.byte(), 8)
        if not frame.status & 4:
            frame = _group_route_bit_fields(state, frame, frame.roster.byte(), 4)
            if frame.status & 4:
                frame = _movement_compare(state, frame, low8(frame.target_x),
                    frame.roster.byte(0, 1), 8)
                if frame.status & 4:
                    frame = _movement_compare(state, frame, low8(frame.target_y),
                        frame.roster.byte(0, 2), 8)
                    if frame.status & 4:
                        return _group_route_carry_fields(state, frame, True)
        frame = first_replace(frame, roster=frame.roster.advance(4))
        frame = first_replace(frame,
            unit=replace_word(frame.unit, u16(low16(frame.unit) - 1)))
        if low16(frame.unit) == 65535:
            break
    frame = first_replace(frame, roster=state.table_at(0xFFFF9000).cursor())
    while True:
        frame = _movement_move(state, frame, 'unit', frame.roster.byte(), 8)
        frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 15, 16)
        if frame.status & 4:
            return _group_route_carry_fields(state, frame, False)
        frame = _movement_compare(state, frame, low8(frame.target_x),
            frame.roster.byte(0, 1), 8)
        if frame.status & 4:
            frame = _movement_compare(state, frame, low8(frame.target_y),
                frame.roster.byte(0, 2), 8)
            if frame.status & 4:
                return _group_route_carry_fields(state, frame, True)
        frame = first_replace(frame,
            roster=frame.roster.advance(s16(low16(frame.unit)) + 13))
