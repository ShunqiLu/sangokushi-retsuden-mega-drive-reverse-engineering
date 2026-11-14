"""Live battle state views and fixed-width operations, not an instruction CPU."""
from dataclasses import dataclass
from typing import NewType
from tools.high_level_city_event.domain import (uint, u16, u32, s16, low16, high16,
    swap_words, replace_word, join_words, negative_long, negative_byte, divu_retained, Boundary)
from tools.high_level_city_event.arithmetic import random_sample, signed_divmod

Word = NewType('Word', int)
Long = NewType('Long', int)
Byte = NewType('Byte', int)


def u8(value):
    if type(value) is not int:
        raise ValueError('integer BYTE arithmetic required')
    return value & 255


def low8(value):
    return u8(value)


def replace_byte(value, low):
    return u32((u32(value) & 0xFFFFFF00) | u8(low))


def mask_byte(value, mask):
    uint(mask, 8, 'BYTE mask')
    return u16((u16(value) & 0xFF00) | (low8(value) & mask))


def zero_extend_word(value):
    return uint(value, 16, 'zero-extended WORD')


def add_low_word(value, amount):
    uint(value, 32, 'preserved LONG')
    uint(amount, 16, 'WORD increment')
    return (value & 0xFFFF0000) | u16(value + amount)


def negative_word(value):
    return bool(uint(value, 16, 'signed WORD') & 32768)


def signed_word(value):
    return s16(value)


def descending_inclusive(counter):
    """DBRA-style inclusive WORD countdown, including 65536 iterations at FFFF."""
    uint(counter, 16, 'countdown WORD')
    for index in range(counter, -1, -1):
        yield index


@dataclass(frozen=True)
class RemovalOutcome:
    award_word: int
    member_removed: bool = True
    abandon_two_calls: bool = True

    def __post_init__(self):
        uint(self.award_word, 16, 'removal award WORD')
        if type(self.member_removed) is not bool or type(self.abandon_two_calls) is not bool or not self.member_removed or not self.abandon_two_calls:
            raise ValueError('explicit two-call-context removal completion required')


class MemberRemoved(Exception):
    """Typed nonlocal completion to the settlement caller, not ordinary return."""
    def __init__(self, outcome):
        if type(outcome) is not RemovalOutcome:
            raise ValueError('typed removal completion required')
        self.outcome = outcome
        super().__init__('member removed; abandon two intermediate calls')


def complete_removal(outcome):
    if type(outcome) is not RemovalOutcome:
        raise ValueError('explicit removal outcome required')
    raise MemberRemoved(outcome)


class BattleState:
    def __init__(self, ram, *, max_reads=1000000):
        if type(ram) is not bytearray or len(ram) != 65536:
            raise ValueError('explicit live 64-KiB RAM required')
        uint(max_reads, 32, 'read budget')
        if not max_reads:
            raise ValueError('positive read budget required')
        self.ram, self.max_reads, self.reads, self.events = ram, max_reads, 0, []

    def read(self, address, size):
        uint(address, 32, 'read address')
        if type(size) is not int or size not in (1, 2, 4):
            raise ValueError('strict BYTE/WORD/LONG read width required')
        if self.reads >= self.max_reads:
            raise Boundary('explicit battle DATA read budget')
        bus = address & 0xFFFFFF
        if size > 1 and address & 1:
            raise Boundary('odd battle DATA read')
        if not 0xFF0000 <= bus <= 0xFFFFFF - size + 1:
            raise Boundary('outside conditional battle RAM read')
        result = int.from_bytes(self.ram[bus & 65535:(bus & 65535) + size], 'big')
        self.reads += 1
        self.events.append(('read', address, size, result))
        return result

    def write(self, address, size, value):
        uint(address, 32, 'write address')
        if type(size) is not int or size not in (1, 2, 4):
            raise ValueError('strict BYTE/WORD/LONG write width required')
        uint(value, size * 8, 'written value')
        bus = address & 0xFFFFFF
        if size > 1 and address & 1:
            raise Boundary('odd battle DATA write')
        if not 0xFF0000 <= bus <= 0xFFFFFF - size + 1:
            raise Boundary('outside conditional battle RAM write')
        self.ram[bus & 65535:(bus & 65535) + size] = value.to_bytes(size, 'big')
        self.events.append(('write', address, size, value))

    @property
    def capacity_parameters(self): return Table(self, 0xFFFFC000)
    @property
    def assignments(self): return Table(self, 0xFFFFCC00)
    @property
    def city_owners(self): return Table(self, 0xFFFFF427)
    @property
    def force_leaders(self): return Table(self, 0xFFFFE640)
    @property
    def officer_flags(self): return Table(self, 0xFFFFC700)
    @property
    def troops(self): return Table(self, 0xFFFFB200)
    @property
    def average_attributes(self): return Table(self, 0xFFFFC400)
    @property
    def packed_offsets(self): return Table(self, 0xFFFFEFBE)
    @property
    def packed_entities(self): return Table(self, 0xFFFF9000)
    @property
    def capacity_fields(self): return Table(self, 0xFFFFC800)
    @property
    def ratio_attributes(self): return Table(self, 0xFFFFB400)
    def seed(self): return self.read(0xFFFFF61C, 4)
    def store_seed(self, value): self.write(0xFFFFF61C, 4, uint(value, 32))
    def attacker_officer(self): return self.read(0xFFFFF3A6, 2)
    def defender_officer(self): return self.read(0xFFFFF3F2, 2)
    def object_index(self): return self.read(0xFFFFEFC6, 2)
    def opposing_object(self): return self.read(0x00FF382C, 4)
    def first_marker(self): return self.read(0xFFFFF744, 2)
    def second_marker(self): return self.read(0xFFFFF746, 2)
    def first_marker_tail(self): return self.read(0xFFFFF745, 1)
    def second_marker_tail(self): return self.read(0xFFFFF747, 1)
    def set_first_marker(self, value): self.write(0xFFFFF744, 2, uint(value, 16))
    def set_second_marker(self, value): self.write(0xFFFFF746, 2, uint(value, 16))
    def set_first_marker_tail(self, value): self.write(0xFFFFF745, 1, uint(value, 8))
    def set_second_marker_tail(self, value): self.write(0xFFFFF747, 1, uint(value, 8))
    def set_second_marker_header(self, value): self.write(0xFFFFF746, 1, uint(value, 8))
    def pair_queue(self): return Cursor(self, 0x00FF39B2)
    def pair_queue_offset(self): return self.read(0x00FF3BB2, 2)
    def active_queue(self): return Cursor(self, 0x00FF3000)
    def first_loss_award(self): return self.read(0xFFFFEFB8, 2)
    def second_loss_award(self): return self.read(0xFFFFEFBA, 2)
    def set_first_loss_award(self, value): self.write(0xFFFFEFB8, 2, uint(value, 16))
    def set_second_loss_award(self, value): self.write(0xFFFFEFBA, 2, uint(value, 16))
    def add_first_loss_award(self, value): self.set_first_loss_award(u16(self.first_loss_award() + uint(value, 16)))
    def add_second_loss_award(self, value): self.set_second_loss_award(u16(self.second_loss_award() + uint(value, 16)))
    def member_removed(self, award): return RemovalOutcome(low16(award))


class Table:
    def __init__(self, state, base):
        if type(state) is not BattleState:
            raise ValueError('typed battle state required')
        self.state, self.base = state, uint(base, 32, 'table base')

    def address(self, offset=0, disp=0):
        uint(offset, 16, 'signed WORD offset')
        if type(disp) is not int or not -32768 <= disp <= 32767:
            raise ValueError('strict finite displacement required')
        return u32(self.base + s16(offset) + disp)

    def byte(self, offset=0, disp=0): return self.state.read(self.address(offset, disp), 1)
    def word(self, offset=0, disp=0): return self.state.read(self.address(offset, disp), 2)
    def long(self, offset=0, disp=0): return self.state.read(self.address(offset, disp), 4)
    def set_byte(self, offset, value, disp=0): self.state.write(self.address(offset, disp), 1, uint(value, 8))
    def set_word(self, offset, value, disp=0): self.state.write(self.address(offset, disp), 2, uint(value, 16))
    def set_long(self, offset, value, disp=0): self.state.write(self.address(offset, disp), 4, uint(value, 32))
    def at(self, offset=0, disp=0): return type(self)(self.state, self.address(offset, disp))
    def advance(self, amount):
        if type(amount) is not int or not -0x80000000 <= amount <= 0x7FFFFFFF:
            raise ValueError('strict signed LONG step required')
        return type(self)(self.state, u32(self.base + amount))
    def advance_lowword(self, amount):
        uint(amount, 16, 'low WORD step')
        return type(self)(self.state, (self.base & 0xFFFF0000) | u16(self.base + amount))
    def change_byte(self, amount):
        if type(amount) is not int or not -128 <= amount <= 127:
            raise ValueError('strict BYTE delta required')
        self.set_byte(0, u8(self.byte() + amount))
    def adjust_after_insertion(self, other):
        if type(other) not in (Table, Cursor):
            raise ValueError('typed comparison view required')
        return self.advance_lowword(1) if self.base >= other.base else self.advance(0)
    def copy_next_byte(self, other):
        if type(other) not in (Table, Cursor):
            raise ValueError('typed destination cursor required')
        value = self.byte()
        self.base = u32(self.base + 1)
        other.set_byte(0, value)
        other.base = u32(other.base + 1)
        return value


class Cursor(Table):
    def next_byte(self):
        result = self.byte()
        self.base = u32(self.base + 1)
        return result
    def write_relative(self, delta, value):
        if type(delta) is not int or not -32768 <= delta <= 32767:
            raise ValueError('relative signed WORD delta required')
        self.state.write(u32(self.base + delta), 1, uint(value, 8))
    def copy_next_byte_relative(self, delta):
        value = self.next_byte()
        self.write_relative(delta, value)
        return value
