"""Immutable outcome inputs with the original partial-width carrier explicit.

The training operand starts with a BYTE load but can be followed by WORD
subtraction. Its retained high BYTE must not be silently initialized to zero.
These contexts name that compatibility input without modeling CPU registers.
"""
from dataclasses import dataclass
from .domain import Byte, Word, Long, uint


@dataclass(frozen=True)
class DuelSettlementContext:
    training_carrier: Long

    def __post_init__(self):
        uint(self.training_carrier, 32)


@dataclass(frozen=True)
class DuelSettlementResult:
    progress_carrier: Long

    def __post_init__(self):
        uint(self.progress_carrier, 32)


@dataclass(frozen=True)
class DuelDispositionContext:
    officer: Word
    disposition: Byte

    def __post_init__(self):
        uint(self.officer, 16)
        uint(self.disposition, 8)


def checked_context(value, expected):
    if type(value) is not expected:
        raise ValueError('exact outcome-family context required')
    value.__post_init__()
    return value
