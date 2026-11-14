"""Explicit live lifecycle transactions, without fabricated absent inputs.

The source/secondary cursors exchange roles during record loading and may alias
the shared stack. transfer_word couples a count with hardware data; these are
not independent cached fields. BYTE/WORD updates, original continuation frames
and unbound hardware/alternate conditions remain the public boundary contract.
"""
from dataclasses import dataclass
from .domain import Byte, Word


@dataclass(slots=True)
class DriverLifecycle:
    "Declared live cells for DriverLifecycle."
    paired_channel_address: Word
    channel_address: Word
    condition_bits: Byte
    transfer_word: Word
    source_cursor: Word
    secondary_cursor: Word
    working_byte: Byte
    return_stack: Word


@dataclass(slots=True)
class RecordInitialization:
    "Declared live cells for RecordInitialization."
    condition_bits: Byte
    transfer_word: Word
    source_cursor: Word
    secondary_cursor: Word
    working_byte: Byte
    return_stack: Word


@dataclass(slots=True)
class BankInitialization:
    "Declared live cells for BankInitialization."
    condition_bits: Byte
    transfer_word: Word
    working_byte: Byte
    return_stack: Word


@dataclass(slots=True)
class OperatorRelease:
    "Declared live cells for OperatorRelease."
    channel_address: Word
    condition_bits: Byte
    transfer_word: Word
    working_byte: Byte
    return_stack: Word
