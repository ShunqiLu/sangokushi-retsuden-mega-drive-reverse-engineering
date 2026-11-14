"""Typed inputs for the original saved-state staging operations.

The cursor remains live: a context does not snapshot or copy its source bytes.
Address metadata and compiler bindings belong to the private build protocol,
not to these editable business inputs.
"""
from dataclasses import dataclass

from .domain import Cursor, StorageState, checked_cursor


@dataclass(frozen=True)
class SavedForceColumnContext:
    """Four-byte force records to separate into four save scratch columns.

    The original entry accepts a source pointer, rather than choosing a fixed
    table itself. The main save flow supplies its force-record view explicitly.
    """

    source: Cursor

    def __post_init__(self):
        checked_cursor(self.source)

    def checked_for(self, state: StorageState):
        checked_cursor(self.source, state)
        return self
