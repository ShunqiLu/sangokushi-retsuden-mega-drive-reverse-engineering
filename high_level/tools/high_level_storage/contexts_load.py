"""Named load outcome, separate from processor/exception state."""
from dataclasses import dataclass
from .domain import Cursor, checked_cursor


@dataclass(frozen=True)
class RestoreOutcome:
    restored: bool
    source_tail: Cursor | None

    def __post_init__(self):
        if type(self.restored) is not bool:
            raise ValueError('strict restored bool required')
        if self.restored:
            checked_cursor(self.source_tail)
        elif self.source_tail is not None:
            raise ValueError('rejected save has no restoration payload cursor')
