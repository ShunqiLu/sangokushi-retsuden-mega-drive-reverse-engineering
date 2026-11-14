"""Command-specific live interfaces. No absent input is supplied a fabricated zero.

Cells evolve during execution and can alias the shared stack/source bus. The
public immutable input/result protocols remain the validation boundary; these
transactions do not cache resources or invent independent hardware state.
"""
from dataclasses import dataclass
from .domain import Byte, Word


@dataclass(slots=True)
class StreamTransferCommand:
    "Declared live cells for StreamTransferCommand."
    condition_bits: Byte
    transfer_word: Word
    table_cursor: Word
    argument_cursor: Word
    command_value: Byte
    return_stack: Word


@dataclass(slots=True)
class DriverLookupCommand:
    "Declared live cells for DriverLookupCommand."
    condition_bits: Byte
    table_cursor: Word
    command_value: Byte
    return_stack: Word


@dataclass(slots=True)
class ChannelDurationCommand:
    "Declared live cells for ChannelDurationCommand."
    channel_address: Word
    condition_bits: Byte
    transfer_word: Word
    command_value: Byte
    return_stack: Word


@dataclass(slots=True)
class ChannelValueCommand:
    "Declared live cells for ChannelValueCommand."
    channel_address: Word
    condition_bits: Byte
    command_value: Byte
    return_stack: Word


@dataclass(slots=True)
class ChannelTransferCommand:
    "Declared live cells for ChannelTransferCommand."
    channel_address: Word
    condition_bits: Byte
    transfer_word: Word
    table_cursor: Word
    argument_cursor: Word
    command_value: Byte
    return_stack: Word


@dataclass(slots=True)
class ChannelPointerCommand:
    "Declared live cells for ChannelPointerCommand."
    channel_address: Word
    condition_bits: Byte
    argument_cursor: Word
    return_stack: Word


@dataclass(slots=True)
class ChannelArgumentCommand:
    "Declared live cells for ChannelArgumentCommand."
    channel_address: Word
    condition_bits: Byte
    argument_cursor: Word
    command_value: Byte
    return_stack: Word


@dataclass(slots=True)
class DriverValueCommand:
    "Declared live cells for DriverValueCommand."
    condition_bits: Byte
    command_value: Byte
    return_stack: Word


@dataclass(slots=True)
class SoundDispatchCommand:
    "Declared live cells for SoundDispatchCommand."
    auxiliary_address: Word
    channel_address: Word
    condition_bits: Byte
    transfer_word: Word
    table_cursor: Word
    argument_cursor: Word
    command_value: Byte
    return_stack: Word
