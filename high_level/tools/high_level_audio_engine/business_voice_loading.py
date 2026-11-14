"""Instrument selection, live field loading and envelope-byte addressing.

The record selector reads the external bank and optional channel bank first.
Record stepping keeps the original repeated WORD additions and byte countdown;
it is not changed to a pure multiply that would invent different conditions.
Loading writes one leading field, twenty further register/value pairs, then
hands the remaining four level fields to the existing shared volume service.
Source bytes are read one at a time at their actual use: stack/source/channel
aliases may change later values. No decoded instrument array is cached here.
All Boundary/nonlocal outcomes propagate; no original behavior is repaired.
"""
from .domain import (AudioState, Continuation, u8, u16, low, high, replace_low,
                     replace_high, logic_conditions, sum_word)
from .contexts_voice import EnvelopeReadContext, InstrumentLoadContext


def read_envelope_byte(state: AudioState, envelope: EnvelopeReadContext, continuation: Continuation) -> None:
    """Address one indexed envelope byte and complete its real return."""
    envelope.indexed_address = replace_high(envelope.indexed_address, 0)
    address_sum, envelope.condition_bits = sum_word(envelope.table_cursor, envelope.indexed_address, envelope.condition_bits)
    envelope.table_cursor = u16(address_sum)
    envelope.indexed_address = replace_low(envelope.indexed_address, low(envelope.table_cursor))
    envelope.indexed_address = replace_high(envelope.indexed_address, high(envelope.table_cursor))
    envelope_byte = state.read(envelope.indexed_address)
    envelope.command_byte = u8(envelope_byte)
    envelope.return_stack = state.consume_return(envelope.return_stack, continuation)


def select_instrument_record(state: AudioState, voice: InstrumentLoadContext, continuation: Continuation) -> None:
    """Choose the live global/channel bank, then apply the record selector."""
    bank_base = state.read_word_le(7223)
    voice.instrument_cursor = u16(bank_base)
    private_bank_enabled = state.read(7193)
    voice.command_byte = u8(private_bank_enabled)
    voice.command_byte = u8(voice.command_byte | voice.command_byte)
    voice.condition_bits = logic_conditions(voice.command_byte, False)
    if not (bool(voice.condition_bits & 0x40)):
        local_bank_low = state.read(u16(voice.channel_address + 42))
        voice.instrument_cursor = replace_low(voice.instrument_cursor, local_bank_low)
        local_bank_high = state.read(u16(voice.channel_address + 43))
        voice.instrument_cursor = replace_high(voice.instrument_cursor, local_bank_high)
    step_instrument_records(state, voice, continuation)


def step_instrument_records(state: AudioState, voice: InstrumentLoadContext, continuation: Continuation) -> None:
    """Advance by 25-byte records using the original live selector countdown."""
    voice.command_byte = u8(voice.command_byte ^ voice.command_byte)
    voice.condition_bits = logic_conditions(voice.command_byte, False)
    voice.command_byte = u8(voice.command_byte | high(voice.transfer_word))
    voice.condition_bits = logic_conditions(voice.command_byte, False)
    if not (bool(voice.condition_bits & 0x40)):
        voice.register_cursor = u16(25)
        while True:
            address_sum, voice.condition_bits = sum_word(voice.instrument_cursor, voice.register_cursor, voice.condition_bits)
            voice.instrument_cursor = u16(address_sum)
            voice.transfer_word = replace_high(voice.transfer_word, u8(high(voice.transfer_word) - 1))
            if high(voice.transfer_word) != 0:
                continue
            break
    voice.return_stack = state.consume_return(voice.return_stack, continuation)


def load_instrument_registers(state: AudioState, voice: InstrumentLoadContext) -> None:
    """Write channel stereo, leading field and main fields; retain level cursor.

    The leading field's actual hardware outcome is saved to channel+27. After
    each service call adopt every returned live cell before decrementing the
    field count. The remaining source cursor is written low then high for the
    existing level service; this stage does not consume the outer return.
    """
    voice.register_cursor = u16(1224)
    stereo_bits = state.read(u16(voice.channel_address + 10))
    voice.transfer_word = replace_low(voice.transfer_word, stereo_bits)
    voice.command_byte = u8(180)
    write_voice_fm_register(state, voice, 1262)
    call_instrument_field(state, voice, 1265)
    state.write(u16(voice.channel_address + 27), u8(voice.command_byte))
    voice.transfer_word = replace_high(voice.transfer_word, 20)
    while True:
        call_instrument_field(state, voice, 1273)
        voice.transfer_word = replace_high(voice.transfer_word, u8(high(voice.transfer_word) - 1))
        if high(voice.transfer_word) != 0:
            continue
        break
    state.write(u16(voice.channel_address + 28), u8(low(voice.instrument_cursor)))
    state.write(u16(voice.channel_address + 29), u8(high(voice.instrument_cursor)))
    pass  # The caller proceeds to the existing shared four-level service.


def write_instrument_field(state: AudioState, voice: InstrumentLoadContext, continuation: Continuation) -> None:
    """Read one register selector then one live value, write FM, complete return."""
    fm_selector = state.read(voice.register_cursor)
    voice.command_byte = u8(fm_selector)
    voice.register_cursor = u16(voice.register_cursor + 1)
    field_byte = state.read(voice.instrument_cursor)
    voice.transfer_word = replace_low(voice.transfer_word, field_byte)
    voice.instrument_cursor = u16(voice.instrument_cursor + 1)
    write_voice_fm_register(state, voice, 1289)
    voice.return_stack = state.consume_return(voice.return_stack, continuation)


def write_voice_fm_register(state: AudioState, voice: InstrumentLoadContext, return_address: int) -> None:
    """Explicit FM boundary: push the real continuation and adopt live outcomes.

    Hardware decides chip/bank readiness and returned conditions. In particular,
    don't substitute the requested selector for the actual returned command.
    Instrument/register cursors are not returned by this hardware service.
    """
    from .business_hardware import write_channel_fm_register
    from .contexts import WriteChannelFmRegisterInput
    voice.return_stack = state.push_word(voice.return_stack, return_address)
    hardware_outcome = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=voice.channel_address, conditions=voice.condition_bits, count_and_data=voice.transfer_word, sample=voice.command_byte, stack_cursor=voice.return_stack, continuation=Continuation("driver", return_address)))
    voice.channel_address = hardware_outcome.channel_cursor
    voice.condition_bits = hardware_outcome.conditions
    voice.transfer_word = hardware_outcome.count_and_data
    voice.command_byte = hardware_outcome.sample
    voice.return_stack = hardware_outcome.stack_cursor


def call_instrument_field(state: AudioState, voice: InstrumentLoadContext, return_address: int) -> None:
    """Use the existing native field-call boundary, not a cached instrument."""
    from .business_voice import write_next_instrument_field
    from .contexts import WriteNextInstrumentFieldInput
    voice.return_stack = state.push_word(voice.return_stack, return_address)
    field_outcome = write_next_instrument_field(state, WriteNextInstrumentFieldInput(channel_cursor=voice.channel_address, conditions=voice.condition_bits, count_and_data=voice.transfer_word, lookup_cursor=voice.instrument_cursor, parameter_cursor=voice.register_cursor, sample=voice.command_byte, stack_cursor=voice.return_stack, continuation=Continuation("driver", return_address)))
    voice.channel_address = field_outcome.channel_cursor
    voice.condition_bits = field_outcome.conditions
    voice.transfer_word = field_outcome.count_and_data
    voice.instrument_cursor = field_outcome.lookup_cursor
    voice.register_cursor = field_outcome.parameter_cursor
    voice.command_byte = field_outcome.sample
    voice.return_stack = field_outcome.stack_cursor
