"""Named live transactions for instrument and envelope services.

These cells describe current execution values, not a decoded copy of the bank.
The shared bus still owns resources and the real stack. A hardware callback can
change the channel/transfer/command/stack cells; callers must adopt its result.
The packed transfer word deliberately couples remaining-field count and field
value as the original service does. It is not replaced by two cached counters.
Entry validation stays at the existing immutable public input boundary.
"""
from dataclasses import dataclass
from .domain import Byte, Word


@dataclass(slots=True)
class EnvelopeReadContext:
    """Indexed envelope address, byte outcome, conditions and real return stack."""
    condition_bits: Byte
    indexed_address: Word
    table_cursor: Word
    command_byte: Byte
    return_stack: Word


@dataclass(slots=True)
class InstrumentLoadContext:
    """Live instrument/register cursors and the FM service's current outcomes."""
    channel_address: Word
    condition_bits: Byte
    transfer_word: Word
    instrument_cursor: Word
    register_cursor: Word
    command_byte: Byte
    return_stack: Word
