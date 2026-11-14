"""Explicit audio bus, fixed-width values and compatibility boundaries.

One supplied authority owns DATA, banked resources, chips and shared stack.
There is no stored code image, PC loop, instruction model or register map.
Platform callbacks expose genuine IRQ/alternate/refresh state; unbound ones
must stop. Conditions helpers are structured arithmetic drafts, not a proof of
every undocumented F/WZ behavior. Memory BIT's full conditions are externally
supplied. The DATA budget is a diagnostic stop, not original game logic.
"""
from dataclasses import dataclass, is_dataclass
from typing import Protocol

Byte = int
Word = int


class AudioBoundary(RuntimeError):
    pass


class NonlocalReturn(AudioBoundary):
    def __init__(self, actual_target, expected_target, stack_cursor):
        self.actual_target = word(actual_target)
        self.expected_target = word(expected_target)
        self.stack_cursor = word(stack_cursor)
        super().__init__("actual shared-stack return leaves the named continuation")


def unsigned(value, bits):
    if type(value) is not int or not 0 <= value < 1 << bits:
        raise ValueError("strict unsigned audio carrier required")
    return value


def byte(value): return unsigned(value, 8)
def word(value): return unsigned(value, 16)
def u8(value): return value & 0xFF
def u16(value): return value & 0xFFFF
def low(value): return value & 0xFF
def high(value): return value >> 8 & 0xFF
def replace_low(value, part): return (value & 0xFF00) | u8(part)
def replace_high(value, part): return (value & 0xFF) | (u8(part) << 8)


def parity(value): return low(value).bit_count() % 2 == 0


def logic_conditions(value, half_carry=False):
    value = u8(value)
    return (value & 0xA8) | (0x40 if value == 0 else 0) | (4 if parity(value) else 0) | (0x10 if half_carry else 0)


def sum_byte(left, right, carry=0):
    total = left + right + carry
    result = u8(total)
    conditions = (result & 0xA8) | (0x40 if result == 0 else 0)
    conditions |= 0x10 if (left ^ right ^ result) & 0x10 else 0
    conditions |= 4 if (~(left ^ right) & (left ^ result)) & 0x80 else 0
    conditions |= 1 if total > 0xFF else 0
    return result, conditions


def difference_byte(left, right, carry=0):
    total = left - right - carry
    result = u8(total)
    conditions = (result & 0xA8) | 2 | (0x40 if result == 0 else 0)
    conditions |= 0x10 if (left ^ right ^ result) & 0x10 else 0
    conditions |= 4 if ((left ^ right) & (left ^ result)) & 0x80 else 0
    conditions |= 1 if total < 0 else 0
    return result, conditions


def comparison_conditions(left, right):
    _, conditions = difference_byte(left, right)
    return (conditions & ~0x28) | (right & 0x28)


def increment_byte(value, conditions):
    result, updated = sum_byte(value, 1)
    return result, (updated & ~1) | (conditions & 1)


def decrement_byte(value, conditions):
    result, updated = difference_byte(value, 1)
    return result, (updated & ~1) | (conditions & 1)


def sum_word(left, right, conditions):
    total = left + right
    result = u16(total)
    updated = (conditions & 0xC4) | (high(result) & 0x28)
    updated |= 0x10 if (left ^ right ^ result) & 0x1000 else 0
    updated |= 1 if total > 0xFFFF else 0
    return result, updated


def difference_word(left, right, conditions):
    total = left - right - (conditions & 1)
    result = u16(total)
    updated = (high(result) & 0xA8) | 2 | (0x40 if result == 0 else 0)
    updated |= 0x10 if (left ^ right ^ result) & 0x1000 else 0
    updated |= 4 if ((left ^ right) & (left ^ result)) & 0x8000 else 0
    updated |= 1 if total < 0 else 0
    return result, updated


def tested_bit_conditions(value, bit_index, conditions, *, address_high=None):
    selected = bool(value & (1 << bit_index))
    undocumented = value if address_high is None else address_high
    return (conditions & 1) | 0x10 | (undocumented & 0x28) | (0 if selected else 0x44) | (0x80 if bit_index == 7 and selected else 0)


def copy_byte_conditions(sample, copied_value, remaining_count, conditions):
    mixed = u8(sample + copied_value)
    return (conditions & 0xC1) | (mixed & 8) | ((mixed & 2) << 4) | (4 if remaining_count != 0 else 0)


@dataclass(frozen=True)
class AlternateGroup:
    count_and_data: Word
    parameter_cursor: Word
    lookup_cursor: Word

    def validate(self):
        word(self.count_and_data); word(self.parameter_cursor); word(self.lookup_cursor)
        return self


@dataclass(frozen=True)
class Continuation:
    image: str
    expected_return_word: Word

    def validate(self):
        if self.image not in ("driver", "startup"):
            raise ValueError("explicit source-image continuation required")
        word(self.expected_return_word)
        return self


class AudioBus(Protocol):
    def read_byte(self, address: Word) -> Byte: ...
    def write_byte(self, address: Word, value: Byte) -> None: ...
    def progress(self, reason: str) -> None: ...
    def transfer_boundary(self, reason: str) -> None: ...


@dataclass(frozen=True)
class MemoryBitContext:
    value: Byte
    bit_index: int
    previous_conditions: Byte
    address: Word
    indexed: bool

    def validate(self):
        byte(self.value); byte(self.previous_conditions); word(self.address)
        if type(self.bit_index) is not int or not 0 <= self.bit_index <= 7:
            raise ValueError("strict tested bit required")
        if type(self.indexed) is not bool:
            raise ValueError("explicit memory BIT address mode required")
        return self


class AudioPlatform:
    """Explicit compatibility ports; none defaults to ready or success."""
    def interrupt_control(self, enabled: bool, deferred_one_instruction: bool):
        raise AudioBoundary("real interrupt enable/delay platform is unbound")
    def interrupt_mode(self, mode: int):
        raise AudioBoundary("real interrupt-mode platform is unbound")
    def set_interrupt_vector(self, value: Byte):
        raise AudioBoundary("real interrupt-vector platform is unbound")
    def set_refresh(self, value: Byte):
        raise AudioBoundary("real refresh-write platform is unbound")
    def read_refresh(self, previous_conditions: Byte):
        raise AudioBoundary("refresh and IFF2 conditions are external")
    def exchange_alternate_accumulator(self, current: Word):
        raise AudioBoundary("real alternate accumulator is unbound")
    def exchange_alternate_group(self, current: AlternateGroup):
        raise AudioBoundary("real alternate word group is unbound")
    def indirect_transfer(self, image: str, target: Word, context: object):
        raise AudioBoundary("actual indirect audio continuation is unbound")
    def memory_bit_conditions(self, context: MemoryBitContext):
        raise AudioBoundary("undocumented memory BIT/WZ conditions are unbound")


class AudioState:
    def __init__(self, bus: AudioBus, platform: AudioPlatform, max_data_operations: int):
        if type(max_data_operations) is not int or max_data_operations < 1:
            raise ValueError("explicit positive DATA budget required")
        self.bus, self.platform = bus, platform
        self.max_data_operations = max_data_operations
        self.data_operations = 0

    def _access(self):
        if self.data_operations >= self.max_data_operations:
            raise AudioBoundary("audio DATA budget exhausted")
        self.data_operations += 1

    def read(self, address):
        self._access()
        return byte(self.bus.read_byte(word(address)))

    def write(self, address, value):
        self._access()
        self.bus.write_byte(word(address), byte(value))

    def read_word_le(self, address):
        address = word(address)
        first = self.read(address)
        second = self.read(u16(address + 1))
        return first | (second << 8)

    def write_word_le(self, address, value):
        word(address); word(value)
        self.write(address, low(value))
        self.write(u16(address + 1), high(value))

    def push_word(self, stack_cursor, value):
        word(stack_cursor); word(value)
        self.write(u16(stack_cursor - 1), high(value))
        self.write(u16(stack_cursor - 2), low(value))
        return u16(stack_cursor - 2)

    def pop_word(self, stack_cursor):
        value = self.read_word_le(stack_cursor)
        return value, u16(stack_cursor + 2)

    def consume_return(self, stack_cursor, continuation):
        if type(continuation) is not Continuation:
            raise ValueError("explicit named continuation required")
        continuation.validate()
        actual, updated_stack = self.pop_word(stack_cursor)
        if actual != continuation.expected_return_word:
            raise NonlocalReturn(actual, continuation.expected_return_word, updated_stack)
        return updated_stack

    def indirect_transfer(self, image, target, context):
        word(target)
        if not is_dataclass(context) or isinstance(context, type):
            raise ValueError("typed actual transfer context required")
        self.platform.indirect_transfer(image, target, context)
        raise AudioBoundary("indirect continuation must not fabricate an ordinary return")

    def memory_bit_conditions(self, value, bit_index, conditions, address, indexed):
        context = MemoryBitContext(value, bit_index, conditions, address, indexed).validate()
        return byte(self.platform.memory_bit_conditions(context))


def checked_state(state):
    if type(state) is not AudioState:
        raise ValueError("single exact AudioState required")
    return state
