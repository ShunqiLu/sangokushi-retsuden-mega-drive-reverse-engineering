"""Prepare both battle-side descriptors from live assignments and attributes.

Field roles beyond these confirmed reads/writes remain probable. These rules
have no register, PC or instruction representation. Fixed-width preservation
and signed source addressing are explicit typed operations.
"""
from .domain import PreparationState, Table, Word, Long, u16, low8, low16, replace_byte, replace_word
from .business_selection import compact_active_deployment_queue


def prepare_battle_mode_header(state: PreparationState) -> Word:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    frame = project_preparation_selection_fields(state, 0x1B7A2)
    return low16(frame.choice)


def prepare_battle_terrain(state: PreparationState) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    project_preparation_selection_fields(state, 0x1B850)


def choose_battle_order(state: PreparationState, first: Long, second: Long) -> tuple[Long, Long]:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    uint(first, 32)
    uint(second, 32)
    frame = project_preparation_selection_fields(state, 0x1B896, first=first, second=second)
    return frame.target_x, frame.choice


def maximum_three_live_lookup_attributes(state: PreparationState, officer: Word, attributes: Table) -> Word:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    uint(officer, 16)
    frame = project_preparation_selection_fields(state, 0x1F8D4, attributes=attributes)
    return low16(frame.count)


def prepare_both_battle_sides(state: PreparationState, first: Long, second: Long) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    uint(first, 32)
    uint(second, 32)
    project_preparation_selection_fields(state, 0x1B6C2, first=first, second=second)

from .domain import uint
from .contexts_counter import project_preparation_selection_fields
