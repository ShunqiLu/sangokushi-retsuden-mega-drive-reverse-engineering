"""Live deployment selection, weighting, queue submission and force matching.

Complete WORD identifiers and signed table addressing are compatibility duties,
not host catalog limits. Data remains live throughout repeated reads and queue
writes. CarryOutcome describes the privileged carry completion contract, not a
flag-free Boolean return or a complete host CPU state.
"""
from .domain import (
    PreparationState, Table, Word, Long, CarryOutcome, u16, u32, low8,
    replace_byte, zero_extend_word, add_low_byte, sub_low_byte, shift_low_word,
    negative_byte, negative_word, descending_inclusive,
)


def selected_attribute_average(state: PreparationState, divisor: Word) -> Long:
    divisor = u16(divisor)
    attributes = state.selected_attributes
    total = u16(0)
    roster = state.selected_attribute_roster.cursor()
    while True:
        roster_member = roster.next_word()
        if negative_word(roster_member):
            break
        roster_member = u16(roster_member & 255)
        attribute = u16(0)
        attribute = replace_byte(attribute, attributes.byte(roster_member))
        total = u16(total + attribute)
    divisor = u16(divisor & 15)
    total = zero_extend_word(total)
    total = state.divide_unsigned(total, divisor)
    return total


def count_selected_deployment(state: PreparationState) -> Word:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    frame = project_preparation_selection_fields(state, 0x1B262)
    return u16(frame.choice)


def initialize_selected_assignment(state: PreparationState, object_view: Table) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    project_preparation_selection_fields(state, 0x1B27A, object_view)


def selected_troop_weights(state: PreparationState) -> tuple[Long, Long]:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    frame = project_preparation_selection_fields(state, 0x1B40E)
    return frame.offset_x, frame.offset_y


def refresh_object_attribute_average(state: PreparationState, object_view: Table, divisor: Word) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    uint(divisor, 16)
    project_preparation_selection_fields(state, 0x1B4EA, object_view)


def submit_deployment_queue(state: PreparationState, object_view: Table) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    project_preparation_selection_fields(state, 0x1B512, object_view)


def clear_original_tail_coordinate(state: PreparationState) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    project_preparation_selection_fields(state, 0x1B578)


def compact_active_deployment_queue(state: PreparationState) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    project_preparation_selection_fields(state, 0x1B8AC)


def deployment_force_carry(state: PreparationState) -> CarryOutcome:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    frame = project_preparation_selection_fields(state, 0x1B90C)
    return CarryOutcome(int(bool(frame.status & 1)), state.sr)

from .domain import uint
from .contexts_counter import project_preparation_selection_fields
