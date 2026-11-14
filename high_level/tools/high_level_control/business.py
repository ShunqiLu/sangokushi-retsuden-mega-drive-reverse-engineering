"""Probable control-WORD choice; confirmed live BYTE/WORD selection logic."""
from .domain import ControlReader


def choose_control(reader: ControlReader) -> int:
    """Choose a control value without prefetching conditional fields."""
    selected = reader.default_word()
    primary_state = reader.primary_byte()
    if primary_state == 0:
        return selected
    selected = reader.alternative_word()
    if primary_state == 1:
        return selected
    secondary_state = reader.secondary_byte()
    if secondary_state == 1:
        return selected
    return reader.default_word()
