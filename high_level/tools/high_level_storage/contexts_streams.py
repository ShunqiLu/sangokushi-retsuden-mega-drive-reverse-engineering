"""Typed, live bit buffers for the original save/load stream families.

These are codec state, not machine registers. A cursor uses the shared storage
bus, so RAM/SRAM aliases and successful DATA ordering remain visible. Buffers
carry complete fixed-width values because BYTE/WORD updates retain high bits.
"""
from dataclasses import dataclass
from .domain import Cursor, Word, Long, checked_cursor, uint


@dataclass
class BitWriter:
    cursor: Cursor
    residue: Long = 0
    bit_count: Word = 0

    def __post_init__(self):
        checked_cursor(self.cursor)
        uint(self.residue, 32, 'write residue')
        uint(self.bit_count, 16, 'write bit count')


@dataclass
class BitReader:
    cursor: Cursor
    residue: Long = 0
    bit_count: Word = 0

    def __post_init__(self):
        checked_cursor(self.cursor)
        uint(self.residue, 32, 'read residue')
        uint(self.bit_count, 16, 'read bit count')


@dataclass
class FixedFieldReadContext:
    """Retained high bits of a BYTE-loaded fixed-field value.

    Zero is the normal low-mask projection, not a proof that arbitrary direct
    callers had zero high bits. Explicit callers can supply and observe the
    complete carrier, including under edited literal masks.
    """
    value_carrier: Long = 0

    def __post_init__(self):
        uint(self.value_carrier, 32, 'fixed-field carrier')


def checked_buffer(value, expected, state):
    if type(value) is not expected:
        raise ValueError('exact typed bit buffer required')
    value.__post_init__()
    checked_cursor(value.cursor, state)
    return value
