"""Host-side typed data interfaces for the small semantic compiler experiment.

These are not a 68000 interpreter, cart bus, stack, or exception model. The
read budget bounds host diagnostics only and is absent from generated code.
"""
from collections.abc import Mapping


def _integer(value, name):
    if type(value) is not int:
        raise ValueError(f'{name} requires an integer, not bool/float')
    return value


def u16(value):
    return _integer(value, 'WORD arithmetic') & 0xFFFF


def u32(value):
    return _integer(value, 'LONG arithmetic') & 0xFFFFFFFF


def s16(value):
    word = u16(value)
    return word - 0x10000 if word & 0x8000 else word


class DiagnosticBoundary(ValueError):
    """Incomplete host data or budget; not a reconstructed CPU exception."""


class WordCursor:
    """Consume live unsigned WORDs without inventing a terminator or snapshot."""

    def __init__(self, words, *, max_reads=65537, events=None):
        if type(max_reads) is not int or not 1 <= max_reads <= 65537:
            raise ValueError('explicit host WORD read budget 1..65537 required')
        try:
            self._iterator = iter(words)
        except TypeError as exc:
            raise ValueError('iterable roster WORDs required') from exc
        self.max_reads, self.consumed = max_reads, 0
        self.events = [] if events is None else events

    def read_word(self):
        if self.consumed >= self.max_reads:
            raise DiagnosticBoundary('explicit host roster read budget exhausted')
        try:
            value = next(self._iterator)
        except StopIteration as exc:
            raise DiagnosticBoundary('supplied roster has no negative WORD terminator') from exc
        if type(value) is not int or not 0 <= value <= 0xFFFF:
            raise ValueError('complete unsigned roster WORD required')
        self.consumed += 1
        self.events.append(('roster_WORD', value))
        return value


class LongTable:
    """Read each selected LONG live; duplicate IDs are not deduplicated.

    Host rows use a signed effective element index, preserving the target's
    low-WORD stride calculation rather than pretending all indexes are natural
    entities. The canonical low-eight-bit rule uses indexes 0..255.
    """

    def __init__(self, values, *, events=None):
        if not isinstance(values, Mapping):
            raise ValueError('live LONG mapping required')
        self.values = values
        self.events = [] if events is None else events

    def __getitem__(self, entity):
        if type(entity) is not int or not 0 <= entity <= 0xFFFF:
            raise ValueError('complete unsigned entity WORD required')
        byte_offset = s16((entity << 2) & 0xFFFF)
        element = byte_offset // 4
        if element not in self.values:
            raise DiagnosticBoundary(f'missing live troop LONG at signed element {element}')
        value = self.values[element]
        if type(value) is not int or not 0 <= value <= 0xFFFFFFFF:
            raise ValueError('complete unsigned troop LONG required')
        self.events.append(('troop_LONG', element, value))
        return value
