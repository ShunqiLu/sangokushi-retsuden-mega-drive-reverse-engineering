"""Fixed-width, live-memory interfaces for the event rules (not a CPU)."""
from __future__ import annotations

from typing import NewType

U16 = NewType('U16', int)
U32 = NewType('U32', int)


def uint(value, bits, name='value'):
    if type(value) is not int or not 0 <= value < (1 << bits):
        raise ValueError(f'{name} must be a complete unsigned {bits}-bit integer')
    return value


def checked_word(value):
    return uint(value, 16, 'WORD input')


def checked_long(value):
    return uint(value, 32, 'LONG input')


def u16(value):
    if type(value) is not int:
        raise ValueError('integer WORD arithmetic required')
    return value & 65535


def u32(value):
    if type(value) is not int:
        raise ValueError('integer LONG arithmetic required')
    return value & 0xFFFFFFFF


def s16(value):
    value = u16(value)
    return value - 65536 if value & 32768 else value


def negative_byte(value):
    return bool(u32(value) & 128)


def negative_long(value):
    return bool(u32(value) & 0x80000000)


def low16(value):
    return u32(value) & 65535


def high16(value):
    return (u32(value) >> 16) & 65535


def swap_words(value):
    return u32((low16(value) << 16) | high16(value))


def replace_byte(value, byte):
    return (u16(value) & 0xFF00) | uint(byte, 8, 'BYTE replacement')


def replace_word(value, word):
    return (u32(value) & 0xFFFF0000) | u16(word)


def join_words(high, low):
    return u32((u16(high) << 16) | u16(low))


def divu_retained(numerator, denominator):
    """68000 unsigned WORD division data result; overflow leaves input intact."""
    denominator = low16(denominator)
    if denominator == 0:
        raise ValueError('original divide-by-zero boundary')
    quotient, remainder = divmod(u32(numerator), denominator)
    return numerator if quotient > 65535 else (remainder << 16) | quotient


class Boundary(ValueError):
    pass


class EventState:
    """A conditional live 64-KiB RAM view with ordered data effects.

    ROM parameter reads are supplied separately. Addresses are compatibility
    bindings, not business names. Diagnostics do not model registers/CCR/stack.
    """
    def __init__(self, ram, parameters, *, max_reads=1000000, max_samples=65536):
        if type(ram) is not bytearray or len(ram) != 65536:
            raise ValueError('one live 64-KiB RAM bytearray required')
        if type(parameters) is not bytes or len(parameters) != 24:
            raise ValueError('24 live event parameter BYTEs required')
        uint(max_reads, 32, 'read budget')
        uint(max_samples, 32, 'sample budget')
        if max_reads == 0 or max_samples == 0:
            raise ValueError('positive explicit diagnostic budgets required')
        self.ram, self.parameters = ram, parameters
        self.max_reads, self.max_samples = max_reads, max_samples
        self.reads, self.samples, self.events = 0, 0, []

    def read(self, address, size):
        if self.reads >= self.max_reads:
            raise Boundary('explicit read budget exhausted')
        if type(address) is not int or type(size) is not int or size not in (1, 2, 4):
            raise ValueError('typed address and read width required')
        address &= 0xFFFFFFFF
        if size > 1 and address & 1:
            raise Boundary('odd WORD/LONG read')
        bus = address & 0xFFFFFF
        if not 0xFF0000 <= bus <= 0xFFFFFF - size + 1:
            raise Boundary('outside conditional RAM view')
        value = int.from_bytes(self.ram[bus & 65535:(bus & 65535) + size], 'big')
        self.reads += 1
        self.events.append(('read', address, size, value))
        return value

    def write(self, address, size, value):
        if type(address) is not int or type(size) is not int or size not in (1, 2, 4):
            raise ValueError('typed address and write width required')
        uint(value, size * 8)
        bus = address & 0xFFFFFF
        if (size > 1 and address & 1) or not 0xFF0000 <= bus <= 0xFFFFFF - size + 1:
            raise Boundary('outside/alignment conditional RAM write')
        self.ram[bus & 65535:(bus & 65535) + size] = value.to_bytes(size, 'big')
        self.events.append(('write', address & 0xFFFFFFFF, size, value))

    def owner(self, city):
        return self.read(u32(0xFFFFF428 + s16(city)), 1)

    def player_owner(self, slot):
        uint(slot, 8, 'bound owner slot')
        if slot > 2:
            raise ValueError('one of the three explicit owner WORD bindings required')
        return self.read(0xFFFFF67A + slot * 2, 2)

    def clear_queue_flag(self):
        self.write(0xFFFFD448, 2, 0)

    def queue(self):
        return Queue(self)

    def field(self, field):
        return Field(self, field)

    def seed(self):
        if self.samples >= self.max_samples:
            raise Boundary('explicit RNG-call budget exhausted')
        self.samples += 1
        return self.read(0xFFFFF61C, 4)

    def store_seed(self, value):
        self.write(0xFFFFF61C, 4, u32(value))

    def parameter(self, group, index):
        if type(group) is not str or group not in ('mask', 'factor'):
            raise ValueError('one explicit parameter group required')
        offset = s16(index) + (0 if group == 'mask' else 12)
        if not 0 <= offset < 24:
            raise Boundary('live parameter read outside supplied parameter view')
        value = self.parameters[offset]
        self.events.append(('parameter_read', group, offset, 1, value))
        return value


class Queue:
    def __init__(self, state):
        self.state, self.cursor = state, 0xFFFFD420

    def read_next(self):
        value = self.state.read(self.cursor, 1)
        self.cursor = u32(self.cursor + 1)
        return value

    def rewind_probe(self):
        self.cursor = u32(self.cursor - 1)
        return self.state.read(self.cursor, 1)

    def write(self, value):
        self.state.write(self.cursor, 1, checked_word(value) & 255)

    def write_next(self, value):
        self.write(value)
        self.cursor = u32(self.cursor + 1)


class Field:
    BASES = {'e1e0': 0xFFFFE1E0, 'e140': 0xFFFFE140, 'e320': 0xFFFFE320,
             'e000': 0xFFFFE000, 'e0a0': 0xFFFFE0A0, 'e5a0': 0xFFFFE5A0}

    def __init__(self, state, name):
        if type(name) is not str or name not in self.BASES:
            raise ValueError('neutral typed event field required')
        self.state, self.base = state, self.BASES[name]

    def read(self, offset):
        return self.state.read(u32(self.base + s16(offset)), 4)

    def write(self, offset, value):
        self.state.write(u32(self.base + s16(offset)), 4, u32(value))
