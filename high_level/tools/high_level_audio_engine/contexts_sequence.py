"""Live sequence-command transactions, not prefetched command payloads.

Argument and scratch cursors exchange roles in original pointer services. Keep
both live: words on the shared native stack and channel-local return slots may
alias the command bytes. The packed transfer word and command byte also evolve
while a command runs. There is no cached loop count or independent call stack.
Existing public input/result validation remains the compatibility boundary.
"""
from dataclasses import dataclass
from .domain import Byte, Word


@dataclass(slots=True)
class SequenceCommandContext:
    """Full command state, including native stack and current channel address."""
    channel_address: Word
    condition_bits: Byte
    transfer_word: Word
    scratch_cursor: Word
    argument_cursor: Word
    command_byte: Byte
    return_stack: Word


@dataclass(slots=True)
class SequenceParameterContext:
    """Parameter reader has no channel input; do not invent one for it."""
    condition_bits: Byte
    transfer_word: Word
    scratch_cursor: Word
    argument_cursor: Word
    command_byte: Byte
    return_stack: Word


@dataclass(slots=True)
class SequenceReturnContext:
    """Sequence return has no command-byte input; its slot is on the live bus."""
    channel_address: Word
    condition_bits: Byte
    transfer_word: Word
    scratch_cursor: Word
    argument_cursor: Word
    return_stack: Word
