"""Named budget/display values and explicit live cursors, not CPU snapshots."""
from dataclasses import dataclass
from .domain import Cursor, Long, Word, checked_cursor, u16, uint


@dataclass(frozen=True)
class DecimalPlaceResult:
    remainder: Long
    started: Word

    def __post_init__(self):
        uint(self.remainder, 32)
        uint(self.started, 16)


@dataclass(frozen=True)
class ResourceRowInput:
    """Live row: D0's full tile/numeric carrier, row WORD and actual output."""
    destination: Cursor
    tile_carrier: Long
    row: Word

    def __post_init__(self):
        checked_cursor(self.destination)
        uint(self.tile_carrier, 32)
        uint(self.row, 16)

    def validate(self, state):
        checked_cursor(self.destination, state)
        return self


@dataclass(frozen=True)
class CommittedResourceRowInput:
    """12E74: keep D0.high; only loaded D2.low reaches numeric D0 at12EA8."""
    destination: Cursor
    tile_carrier: Long
    row: Word
    loaded_amount: Long

    def __post_init__(self):
        checked_cursor(self.destination)
        uint(self.tile_carrier, 32)
        uint(self.row, 16)
        uint(self.loaded_amount, 32)

    def validate(self, state):
        checked_cursor(self.destination, state)
        return self


@dataclass(frozen=True)
class ResourceRowsInput:
    """Independent12DFC requires a genuine incoming full D0, never default0."""
    destination: Cursor
    numeric_carrier: Long

    def __post_init__(self):
        checked_cursor(self.destination)
        uint(self.numeric_carrier, 32)

    def validate(self, state):
        checked_cursor(self.destination, state)
        return self


@dataclass(frozen=True)
class ResourceRowsResult:
    """Observed current A0/D0 after a row; not all registers/CCR/CPU state."""
    destination: Cursor
    numeric_carrier: Long

    def __post_init__(self):
        checked_cursor(self.destination)
        uint(self.numeric_carrier, 32)

    def validate(self, state):
        checked_cursor(self.destination, state)
        return self


@dataclass(frozen=True)
class CommandColumns:
    destination: Cursor
    pitch: Word

    def __post_init__(self):
        checked_cursor(self.destination)
        uint(self.pitch, 16)

    def append_pair(self, foreground: Word, following: Word):
        foreground = uint(foreground, 16)
        following = uint(following, 16)
        self.destination.set_word(self.pitch, following)
        self.destination.append_word(foreground)

    def append_run(self, foreground: Word, following: Word, length: Word):
        uint(length, 16)
        for _ in range(length):
            self.append_pair(foreground, following)

    def append_numbered_pair(self, tile: Word, length: Long) -> Word:
        tile = uint(tile, 16)
        uint(length, 32)
        for _ in range(length):
            self.destination.put_word(tile)
            tile = u16(tile + 1)
            self.destination.set_word(self.pitch, tile)
            tile = u16(tile + 1)
            self.destination.base = self.destination.advance(2).base
        return tile

    def next_row(self):
        self.destination.base = self.destination.advance(self.pitch).base
