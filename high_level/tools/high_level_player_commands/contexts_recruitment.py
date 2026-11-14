"""Typed inputs for the recruitment and candidate-list display routines.

Tile identifiers are UI layout parameters, not embedded images. Destinations
remain live cursors: overlapping rows and scratch storage are not snapshotted.
The full scalar carriers retain the original upper WORD where an entry only
changes its lower WORD.
"""
from dataclasses import dataclass
from .domain import Long, Cursor, checked_cursor, uint


@dataclass(frozen=True)
class TilePairContext:
    destination: Cursor
    tile: Long
    counter: Long

    def __post_init__(self):
        checked_cursor(self.destination)
        uint(self.tile, 32)
        uint(self.counter, 32)


@dataclass(frozen=True)
class TilePairResult:
    destination: Cursor
    next_tile: Long
    remaining_counter: Long

    def __post_init__(self):
        checked_cursor(self.destination)
        uint(self.next_tile, 32)
        uint(self.remaining_counter, 32)


@dataclass(frozen=True)
class SeparatorRowContext:
    destination: Cursor
    coordinate: Long

    def __post_init__(self):
        checked_cursor(self.destination)
        uint(self.coordinate, 32)


@dataclass(frozen=True)
class SeparatorRowResult:
    destination: Cursor
    next_coordinate: Long

    def __post_init__(self):
        checked_cursor(self.destination)
        uint(self.next_coordinate, 32)


def checked_context(value, expected, state=None):
    """Reject malformed or foreign live views before the first DATA access."""
    if type(value) is not expected:
        raise ValueError('exact recruitment-family context required')
    value.__post_init__()
    checked_cursor(value.destination, state)
    return value
