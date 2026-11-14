"""Structured intermediate audio logic, not a complete CPU/timing proof."""
from .domain import (AudioState, AudioBoundary, Continuation, AlternateGroup,
    Byte, Word, byte, word, checked_state, u8, u16, low, high, replace_low,
    replace_high, logic_conditions, sum_byte, difference_byte,
    comparison_conditions, increment_byte, decrement_byte, sum_word,
    difference_word, tested_bit_conditions, copy_byte_conditions)
from .contexts import (
    ReadIndexedEnvelopeInput, ReadIndexedEnvelopeResult,
    LookupInstrumentInput, LookupInstrumentResult,
    OffsetInstrumentInput, OffsetInstrumentResult,
    LoadInstrumentInput, LoadInstrumentResult,
    WriteNextInstrumentFieldInput, WriteNextInstrumentFieldResult,
    RefreshInstrumentVolumeInput, RefreshInstrumentVolumeResult,
    AdjustChannelVolumeInput, AdjustChannelVolumeResult,
    AdjustFmChannelVolumeInput, AdjustFmChannelVolumeResult,
)

from .contexts_voice import EnvelopeReadContext, InstrumentLoadContext
from .business_voice_loading import (read_envelope_byte, select_instrument_record, step_instrument_records, load_instrument_registers, write_instrument_field)

def read_indexed_envelope(state: AudioState, inputs: ReadIndexedEnvelopeInput) -> ReadIndexedEnvelopeResult:
    """Read indexed envelope."""
    checked_state(state)
    if type(inputs) is not ReadIndexedEnvelopeInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    envelope = EnvelopeReadContext(
        condition_bits=inputs.conditions,
        indexed_address=inputs.count_and_data,
        table_cursor=inputs.lookup_cursor,
        command_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    read_envelope_byte(state, envelope, inputs.continuation)
    return ReadIndexedEnvelopeResult(conditions=envelope.condition_bits, count_and_data=envelope.indexed_address, lookup_cursor=envelope.table_cursor, sample=envelope.command_byte, stack_cursor=envelope.return_stack).validate(state)

def lookup_instrument(state: AudioState, inputs: LookupInstrumentInput) -> LookupInstrumentResult:
    """Lookup instrument."""
    checked_state(state)
    if type(inputs) is not LookupInstrumentInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    voice = InstrumentLoadContext(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        instrument_cursor=inputs.lookup_cursor,
        register_cursor=inputs.parameter_cursor,
        command_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    select_instrument_record(state, voice, inputs.continuation)
    return LookupInstrumentResult(channel_cursor=voice.channel_address, conditions=voice.condition_bits, count_and_data=voice.transfer_word, lookup_cursor=voice.instrument_cursor, parameter_cursor=voice.register_cursor, sample=voice.command_byte, stack_cursor=voice.return_stack).validate(state)

def offset_instrument(state: AudioState, inputs: OffsetInstrumentInput) -> OffsetInstrumentResult:
    """Offset instrument."""
    checked_state(state)
    if type(inputs) is not OffsetInstrumentInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    voice = InstrumentLoadContext(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        instrument_cursor=inputs.lookup_cursor,
        register_cursor=inputs.parameter_cursor,
        command_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    step_instrument_records(state, voice, inputs.continuation)
    return OffsetInstrumentResult(channel_cursor=voice.channel_address, conditions=voice.condition_bits, count_and_data=voice.transfer_word, lookup_cursor=voice.instrument_cursor, parameter_cursor=voice.register_cursor, sample=voice.command_byte, stack_cursor=voice.return_stack).validate(state)

def load_instrument(state: AudioState, inputs: LoadInstrumentInput) -> LoadInstrumentResult:
    """Load instrument."""
    checked_state(state)
    if type(inputs) is not LoadInstrumentInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    voice = InstrumentLoadContext(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        instrument_cursor=inputs.lookup_cursor,
        register_cursor=inputs.parameter_cursor,
        command_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    load_instrument_registers(state, voice)
    voice.channel_address, voice.condition_bits, voice.transfer_word, voice.instrument_cursor, voice.register_cursor, voice.command_byte, voice.return_stack = _write_instrument_level_fields(
        state, channel_cursor=voice.channel_address, conditions=voice.condition_bits, count_and_data=voice.transfer_word, lookup_cursor=voice.instrument_cursor, parameter_cursor=voice.register_cursor, sample=voice.command_byte, stack_cursor=voice.return_stack,
        continuation=inputs.continuation)
    return LoadInstrumentResult(channel_cursor=voice.channel_address, conditions=voice.condition_bits, count_and_data=voice.transfer_word, lookup_cursor=voice.instrument_cursor, parameter_cursor=voice.register_cursor, sample=voice.command_byte, stack_cursor=voice.return_stack).validate(state)

def write_next_instrument_field(state: AudioState, inputs: WriteNextInstrumentFieldInput) -> WriteNextInstrumentFieldResult:
    """Write next instrument field."""
    checked_state(state)
    if type(inputs) is not WriteNextInstrumentFieldInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    voice = InstrumentLoadContext(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        instrument_cursor=inputs.lookup_cursor,
        register_cursor=inputs.parameter_cursor,
        command_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    write_instrument_field(state, voice, inputs.continuation)
    return WriteNextInstrumentFieldResult(channel_cursor=voice.channel_address, conditions=voice.condition_bits, count_and_data=voice.transfer_word, lookup_cursor=voice.instrument_cursor, parameter_cursor=voice.register_cursor, sample=voice.command_byte, stack_cursor=voice.return_stack).validate(state)

def refresh_instrument_volume(state: AudioState, inputs: RefreshInstrumentVolumeInput) -> RefreshInstrumentVolumeResult:
    """Refresh instrument volume."""
    checked_state(state)
    if type(inputs) is not RefreshInstrumentVolumeInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    channel_cursor = inputs.channel_cursor
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    lookup_cursor = inputs.lookup_cursor
    parameter_cursor = inputs.parameter_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    channel_cursor, conditions, count_and_data, lookup_cursor, parameter_cursor, sample, stack_cursor = _write_instrument_level_fields(
        state, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data,
        lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample,
        stack_cursor=stack_cursor, continuation=inputs.continuation)
    return RefreshInstrumentVolumeResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def adjust_channel_volume(state: AudioState, inputs: AdjustChannelVolumeInput) -> AdjustChannelVolumeResult:
    """Adjust channel volume."""
    checked_state(state)
    if type(inputs) is not AdjustChannelVolumeInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    channel_cursor = inputs.channel_cursor
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    lookup_cursor = inputs.lookup_cursor
    parameter_cursor = inputs.parameter_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:0da9:inc
    parameter_cursor = u16(parameter_cursor + 1)
    # source-effect driver:0daa:add
    observed_byte_1 = state.read(u16(channel_cursor + 6))
    arithmetic_result_2, conditions = sum_byte(sample, observed_byte_1)
    sample = u8(arithmetic_result_2)
    # source-effect driver:0dad:ld
    state.write(u16(channel_cursor + 6), u8(sample))
    # source-effect driver:0db0:ld
    observed_byte_3 = state.read(parameter_cursor)
    sample = u8(observed_byte_3)
    # source-effect driver:0db1:bit
    observed_byte_4 = state.read(u16(channel_cursor + 1))
    conditions = state.memory_bit_conditions(observed_byte_4, 7, conditions, u16(channel_cursor + 1), True)
    # source-effect driver:0db5:ret
    if not (conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return AdjustChannelVolumeResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0db6:add
    observed_byte_5 = state.read(u16(channel_cursor + 6))
    arithmetic_result_6, conditions = sum_byte(sample, observed_byte_5)
    sample = u8(arithmetic_result_6)
    # source-effect driver:0db9:ld
    state.write(u16(channel_cursor + 6), u8(sample))
    # source-effect driver:0dbc:jr
    pass  # Static control continuation is structured below.
    channel_cursor, conditions, count_and_data, lookup_cursor, parameter_cursor, sample, stack_cursor = _write_instrument_level_fields(
        state, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data,
        lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample,
        stack_cursor=stack_cursor, continuation=inputs.continuation)
    return AdjustChannelVolumeResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def adjust_fm_channel_volume(state: AudioState, inputs: AdjustFmChannelVolumeInput) -> AdjustFmChannelVolumeResult:
    """Adjust fm channel volume."""
    checked_state(state)
    if type(inputs) is not AdjustFmChannelVolumeInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    channel_cursor = inputs.channel_cursor
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    lookup_cursor = inputs.lookup_cursor
    parameter_cursor = inputs.parameter_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:0db1:bit
    observed_byte_1 = state.read(u16(channel_cursor + 1))
    conditions = state.memory_bit_conditions(observed_byte_1, 7, conditions, u16(channel_cursor + 1), True)
    # source-effect driver:0db5:ret
    if not (conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return AdjustFmChannelVolumeResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0db6:add
    observed_byte_2 = state.read(u16(channel_cursor + 6))
    arithmetic_result_3, conditions = sum_byte(sample, observed_byte_2)
    sample = u8(arithmetic_result_3)
    # source-effect driver:0db9:ld
    state.write(u16(channel_cursor + 6), u8(sample))
    # source-effect driver:0dbc:jr
    pass  # Static control continuation is structured below.
    channel_cursor, conditions, count_and_data, lookup_cursor, parameter_cursor, sample, stack_cursor = _write_instrument_level_fields(
        state, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data,
        lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample,
        stack_cursor=stack_cursor, continuation=inputs.continuation)
    return AdjustFmChannelVolumeResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)


def _write_instrument_level_fields(
        state: AudioState, *, channel_cursor: Word, conditions: Byte,
        count_and_data: Word, lookup_cursor: Word, parameter_cursor: Word,
        sample: Byte, stack_cursor: Word, continuation: Continuation,
) -> tuple[Word, Byte, Word, Word, Word, Byte, Word]:
    """Write the four live instrument level fields through the channel FM port.

    The source high bit requests addition of channel+6 before the seven-bit
    value mask. Re-read that delta per flagged field: source/channel/stack
    aliases are live, not cached. BC/DE/HL use the external alternate-word
    exchange at both ends; A/conditions remain the actual FM-write outcome.
    This logical helper adds no native CALL or stack layer. Consume the caller\'s
    original continuation only after the second exchange; every Boundary and
    nonlocal return propagates without a fabricated successful result.
    """
    # source-effect driver:0d8a:exx
    inactive_words = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
    inactive_words.validate()
    count_and_data, parameter_cursor, lookup_cursor = inactive_words.count_and_data, inactive_words.parameter_cursor, inactive_words.lookup_cursor
    # source-effect driver:0d8b:ld
    parameter_cursor = u16(1245)
    # source-effect driver:0d8e:ld
    pointer_low = state.read(u16(channel_cursor + 28))
    lookup_cursor = replace_low(lookup_cursor, pointer_low)
    # source-effect driver:0d91:ld
    pointer_high = state.read(u16(channel_cursor + 29))
    lookup_cursor = replace_high(lookup_cursor, pointer_high)
    # source-effect driver:0d94:ld
    count_and_data = replace_high(count_and_data, 4)
    while True:
        # source-effect driver:0d96:ld
        level_source = state.read(lookup_cursor)
        sample = u8(level_source)
        # source-effect driver:0d97:or
        sample = u8(sample | sample)
        conditions = logic_conditions(sample, False)
        # source-effect driver:0d98:jp
        if not (not (conditions & 0x80)):
            # source-effect driver:0d9b:add
            channel_delta = state.read(u16(channel_cursor + 6))
            adjusted_level, conditions = sum_byte(sample, channel_delta)
            sample = u8(adjusted_level)
        # source-effect driver:0d9e:and
        sample = u8(sample & 127)
        conditions = logic_conditions(sample, True)
        # source-effect driver:0da0:ld
        count_and_data = replace_low(count_and_data, sample)
        # source-effect driver:0da1:ld
        register_selector = state.read(parameter_cursor)
        sample = u8(register_selector)
        # source-effect driver:0da2:rst
        from .business_hardware import write_channel_fm_register
        from .contexts import WriteChannelFmRegisterInput
        stack_cursor = state.push_word(stack_cursor, 3491)
        write_outcome = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3491)))
        channel_cursor = write_outcome.channel_cursor
        conditions = write_outcome.conditions
        count_and_data = write_outcome.count_and_data
        sample = write_outcome.sample
        stack_cursor = write_outcome.stack_cursor
        # source-effect driver:0da3:inc
        parameter_cursor = u16(parameter_cursor + 1)
        # source-effect driver:0da4:inc
        lookup_cursor = u16(lookup_cursor + 1)
        # source-effect driver:0da5:djnz
        count_and_data = replace_high(count_and_data, u8(high(count_and_data) - 1))
        if high(count_and_data) != 0:
            continue
        break
    # source-effect driver:0da7:exx
    restored_words = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
    restored_words.validate()
    count_and_data, parameter_cursor, lookup_cursor = restored_words.count_and_data, restored_words.parameter_cursor, restored_words.lookup_cursor
    # source-effect driver:0da8:ret
    stack_cursor = state.consume_return(stack_cursor, continuation)
    return channel_cursor, conditions, count_and_data, lookup_cursor, parameter_cursor, sample, stack_cursor
