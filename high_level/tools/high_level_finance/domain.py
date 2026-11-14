"""Typed live ports and arithmetic used by debt-interest business rules.

The unusual word rotation is intentional: the original high-product contribution
retains both halves. It must not be simplified to a normal 32-bit product.
"""
from typing import Protocol


def integers(*values):
    if any(type(value) is not int for value in values):
        raise ValueError('strict integer arithmetic operands required')


def unsigned(value: int, bits: int) -> int:
    if type(value) is not int or type(bits) is not int or bits not in (8, 16, 32):
        raise ValueError('integer and explicit supported width required')
    return value & ((1 << bits) - 1)


def signed8(value: int) -> int:
    value = unsigned(value, 8)
    return value - 256 if value & 128 else value


def sub8(left: int, right: int) -> int:
    integers(left, right)
    return unsigned(left - right, 8)


def add16(left: int, right: int) -> int:
    integers(left, right)
    return unsigned(left + right, 16)


def mul16(left: int, right: int) -> int:
    integers(left, right)
    return unsigned(left * right, 16)


def mul_u16(left: int, right: int) -> int:
    return unsigned(left, 16) * unsigned(right, 16)


def low_word(value: int) -> int:
    return unsigned(value, 16)


def high_word(value: int) -> int:
    return unsigned(value, 32) >> 16


def rotate_words(value: int) -> int:
    value = unsigned(value, 32)
    return unsigned((value << 16) | (value >> 16), 32)


def add32(left: int, right: int) -> int:
    integers(left, right)
    return unsigned(left + right, 32)


def div_signed(numerator: int, denominator: int) -> int:
    """Truncate a signed wrapping LONG toward zero, returning its bit pattern."""
    numerator = unsigned(numerator, 32)
    if type(denominator) is not int or not 1 <= denominator <= 127:
        raise ValueError('positive signed-MOVEQ-sized denominator required')
    signed = numerator - (1 << 32) if numerator & (1 << 31) else numerator
    quotient = abs(signed) // denominator
    return unsigned(-quotient if signed < 0 else quotient, 32)


class Clock(Protocol):
    def year(self) -> int: ...
    def month(self) -> int: ...


class DebtDates(Protocol):
    def year(self, offset: int) -> int: ...
    def month(self, offset: int) -> int: ...
