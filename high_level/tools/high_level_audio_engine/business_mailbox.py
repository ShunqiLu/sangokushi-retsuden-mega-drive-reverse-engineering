"""Structured intermediate audio logic, not a complete CPU/timing proof."""
from .domain import (AudioState, AudioBoundary, Continuation, AlternateGroup,
    Byte, Word, byte, word, checked_state, u8, u16, low, high, replace_low,
    replace_high, logic_conditions, sum_byte, difference_byte,
    comparison_conditions, increment_byte, decrement_byte, sum_word,
    difference_word, tested_bit_conditions, copy_byte_conditions)
from .contexts import (
    PollCommandMailboxesInput, PollCommandMailboxesResult,
    ArbitrateCommandSlotInput, ArbitrateCommandSlotResult,
    UpdateRhythmCountdownInput, UpdateRhythmCountdownResult,
    DispatchExtendedSequenceCommandInput, DispatchExtendedSequenceCommandResult,
)

def poll_command_mailboxes(state: AudioState, inputs: PollCommandMailboxesInput) -> PollCommandMailboxesResult:
    """Poll command mailboxes."""
    checked_state(state)
    if type(inputs) is not PollCommandMailboxesInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    lookup_cursor = inputs.lookup_cursor
    parameter_cursor = inputs.parameter_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:087f:ld
    sample, conditions = state.platform.read_refresh(conditions)
    byte(sample)
    byte(conditions)
    # source-effect driver:0881:ld
    state.write(7191, u8(sample))
    # source-effect driver:0884:ld
    parameter_cursor = u16(7178)
    # source-effect driver:0887:call
    from .business_mailbox import arbitrate_command_slot
    from .contexts import ArbitrateCommandSlotInput
    stack_cursor = state.push_word(stack_cursor, 2186)
    updated_audio_values_1 = arbitrate_command_slot(state, ArbitrateCommandSlotInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2186)))
    conditions = updated_audio_values_1.conditions
    count_and_data = updated_audio_values_1.count_and_data
    lookup_cursor = updated_audio_values_1.lookup_cursor
    parameter_cursor = updated_audio_values_1.parameter_cursor
    sample = updated_audio_values_1.sample
    stack_cursor = updated_audio_values_1.stack_cursor
    # source-effect driver:088a:ld
    parameter_cursor = u16(7179)
    # source-effect driver:088d:call
    from .business_mailbox import arbitrate_command_slot
    from .contexts import ArbitrateCommandSlotInput
    stack_cursor = state.push_word(stack_cursor, 2192)
    updated_audio_values_2 = arbitrate_command_slot(state, ArbitrateCommandSlotInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2192)))
    conditions = updated_audio_values_2.conditions
    count_and_data = updated_audio_values_2.count_and_data
    lookup_cursor = updated_audio_values_2.lookup_cursor
    parameter_cursor = updated_audio_values_2.parameter_cursor
    sample = updated_audio_values_2.sample
    stack_cursor = updated_audio_values_2.stack_cursor
    # source-effect driver:0890:ld
    parameter_cursor = u16(7180)
    # source-effect driver:0893:ld
    observed_byte_3 = state.read(parameter_cursor)
    sample = u8(observed_byte_3)
    # source-effect driver:0894:bit
    conditions = tested_bit_conditions(sample, 7, conditions)
    # source-effect driver:0896:ret
    if bool(conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return PollCommandMailboxesResult(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0897:sub
    sample, conditions = difference_byte(sample, 129)
    # source-effect driver:0899:ld
    observed_word_4 = state.read_word_le(7170)
    lookup_cursor = u16(observed_word_4)
    # source-effect driver:089c:ld
    count_and_data = replace_low(count_and_data, 0)
    # source-effect driver:089e:rst
    from .business_hardware import lookup_banked_root_pointer
    from .contexts import LookupBankedRootPointerInput
    stack_cursor = state.push_word(stack_cursor, 2207)
    updated_audio_values_5 = lookup_banked_root_pointer(state, LookupBankedRootPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2207)))
    conditions = updated_audio_values_5.conditions
    count_and_data = updated_audio_values_5.count_and_data
    lookup_cursor = updated_audio_values_5.lookup_cursor
    sample = updated_audio_values_5.sample
    stack_cursor = updated_audio_values_5.stack_cursor
    # source-effect driver:089f:ld
    count_and_data = replace_low(count_and_data, sample)
    # source-effect driver:08a0:ld
    count_and_data = replace_high(count_and_data, 0)
    # source-effect driver:08a2:add
    arithmetic_result_6, conditions = sum_word(lookup_cursor, count_and_data, conditions)
    lookup_cursor = u16(arithmetic_result_6)
    # source-effect driver:08a3:bit
    observed_byte_7 = state.read(lookup_cursor)
    conditions = state.memory_bit_conditions(observed_byte_7, 7, conditions, lookup_cursor, False)
    # source-effect driver:08a5:jr
    if bool(conditions & 0x40):
        # source-effect driver:08b5:ld
        observed_byte_8 = state.read(7192)
        sample = u8(observed_byte_8)
        # source-effect driver:08b8:cp
        observed_byte_9 = state.read(lookup_cursor)
        conditions = comparison_conditions(sample, observed_byte_9)
        # source-effect driver:08b9:jr
        if bool(conditions & 0x40):
            # source-effect driver:08bd:ld
            observed_byte_10 = state.read(parameter_cursor)
            sample = u8(observed_byte_10)
            # source-effect driver:08be:ld
            state.write(7177, u8(sample))
            # source-effect driver:08c1:ld
            observed_byte_11 = state.read(lookup_cursor)
            sample = u8(observed_byte_11)
            # source-effect driver:08c2:ld
            state.write(7192, u8(sample))
        else:
            # source-effect driver:08bb:jr
            if not (not (conditions & 1)):
                # source-effect driver:08bd:ld
                observed_byte_12 = state.read(parameter_cursor)
                sample = u8(observed_byte_12)
                # source-effect driver:08be:ld
                state.write(7177, u8(sample))
                # source-effect driver:08c1:ld
                observed_byte_13 = state.read(lookup_cursor)
                sample = u8(observed_byte_13)
                # source-effect driver:08c2:ld
                state.write(7192, u8(sample))
        # source-effect driver:08c5:xor
        sample = u8(sample ^ sample)
        conditions = logic_conditions(sample, False)
        # source-effect driver:08c6:ld
        state.write(parameter_cursor, u8(sample))
        # source-effect driver:08c7:ret
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return PollCommandMailboxesResult(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    else:
        # source-effect driver:08a7:ld
        observed_byte_14 = state.read(parameter_cursor)
        sample = u8(observed_byte_14)
        # source-effect driver:08a8:ld
        state.write(7177, u8(sample))
        # source-effect driver:08ab:xor
        sample = u8(sample ^ sample)
        conditions = logic_conditions(sample, False)
        # source-effect driver:08ac:ld
        lookup_cursor = u16(7178)
        # source-effect driver:08af:ld
        state.write(lookup_cursor, u8(sample))
        # source-effect driver:08b0:inc
        lookup_cursor = u16(lookup_cursor + 1)
        # source-effect driver:08b1:ld
        state.write(lookup_cursor, u8(sample))
        # source-effect driver:08b2:inc
        lookup_cursor = u16(lookup_cursor + 1)
        # source-effect driver:08b3:ld
        state.write(lookup_cursor, u8(sample))
        # source-effect driver:08b4:ret
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return PollCommandMailboxesResult(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def arbitrate_command_slot(state: AudioState, inputs: ArbitrateCommandSlotInput) -> ArbitrateCommandSlotResult:
    """Arbitrate command slot."""
    checked_state(state)
    if type(inputs) is not ArbitrateCommandSlotInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    lookup_cursor = inputs.lookup_cursor
    parameter_cursor = inputs.parameter_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:0893:ld
    observed_byte_1 = state.read(parameter_cursor)
    sample = u8(observed_byte_1)
    # source-effect driver:0894:bit
    conditions = tested_bit_conditions(sample, 7, conditions)
    # source-effect driver:0896:ret
    if bool(conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return ArbitrateCommandSlotResult(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0897:sub
    sample, conditions = difference_byte(sample, 129)
    # source-effect driver:0899:ld
    observed_word_2 = state.read_word_le(7170)
    lookup_cursor = u16(observed_word_2)
    # source-effect driver:089c:ld
    count_and_data = replace_low(count_and_data, 0)
    # source-effect driver:089e:rst
    from .business_hardware import lookup_banked_root_pointer
    from .contexts import LookupBankedRootPointerInput
    stack_cursor = state.push_word(stack_cursor, 2207)
    updated_audio_values_3 = lookup_banked_root_pointer(state, LookupBankedRootPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2207)))
    conditions = updated_audio_values_3.conditions
    count_and_data = updated_audio_values_3.count_and_data
    lookup_cursor = updated_audio_values_3.lookup_cursor
    sample = updated_audio_values_3.sample
    stack_cursor = updated_audio_values_3.stack_cursor
    # source-effect driver:089f:ld
    count_and_data = replace_low(count_and_data, sample)
    # source-effect driver:08a0:ld
    count_and_data = replace_high(count_and_data, 0)
    # source-effect driver:08a2:add
    arithmetic_result_4, conditions = sum_word(lookup_cursor, count_and_data, conditions)
    lookup_cursor = u16(arithmetic_result_4)
    # source-effect driver:08a3:bit
    observed_byte_5 = state.read(lookup_cursor)
    conditions = state.memory_bit_conditions(observed_byte_5, 7, conditions, lookup_cursor, False)
    # source-effect driver:08a5:jr
    if bool(conditions & 0x40):
        # source-effect driver:08b5:ld
        observed_byte_6 = state.read(7192)
        sample = u8(observed_byte_6)
        # source-effect driver:08b8:cp
        observed_byte_7 = state.read(lookup_cursor)
        conditions = comparison_conditions(sample, observed_byte_7)
        # source-effect driver:08b9:jr
        if bool(conditions & 0x40):
            # source-effect driver:08bd:ld
            observed_byte_8 = state.read(parameter_cursor)
            sample = u8(observed_byte_8)
            # source-effect driver:08be:ld
            state.write(7177, u8(sample))
            # source-effect driver:08c1:ld
            observed_byte_9 = state.read(lookup_cursor)
            sample = u8(observed_byte_9)
            # source-effect driver:08c2:ld
            state.write(7192, u8(sample))
        else:
            # source-effect driver:08bb:jr
            if not (not (conditions & 1)):
                # source-effect driver:08bd:ld
                observed_byte_10 = state.read(parameter_cursor)
                sample = u8(observed_byte_10)
                # source-effect driver:08be:ld
                state.write(7177, u8(sample))
                # source-effect driver:08c1:ld
                observed_byte_11 = state.read(lookup_cursor)
                sample = u8(observed_byte_11)
                # source-effect driver:08c2:ld
                state.write(7192, u8(sample))
        # source-effect driver:08c5:xor
        sample = u8(sample ^ sample)
        conditions = logic_conditions(sample, False)
        # source-effect driver:08c6:ld
        state.write(parameter_cursor, u8(sample))
        # source-effect driver:08c7:ret
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return ArbitrateCommandSlotResult(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    else:
        # source-effect driver:08a7:ld
        observed_byte_12 = state.read(parameter_cursor)
        sample = u8(observed_byte_12)
        # source-effect driver:08a8:ld
        state.write(7177, u8(sample))
        # source-effect driver:08ab:xor
        sample = u8(sample ^ sample)
        conditions = logic_conditions(sample, False)
        # source-effect driver:08ac:ld
        lookup_cursor = u16(7178)
        # source-effect driver:08af:ld
        state.write(lookup_cursor, u8(sample))
        # source-effect driver:08b0:inc
        lookup_cursor = u16(lookup_cursor + 1)
        # source-effect driver:08b1:ld
        state.write(lookup_cursor, u8(sample))
        # source-effect driver:08b2:inc
        lookup_cursor = u16(lookup_cursor + 1)
        # source-effect driver:08b3:ld
        state.write(lookup_cursor, u8(sample))
        # source-effect driver:08b4:ret
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return ArbitrateCommandSlotResult(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def update_rhythm_countdown(state: AudioState, inputs: UpdateRhythmCountdownInput) -> UpdateRhythmCountdownResult:
    """Update rhythm countdown."""
    checked_state(state)
    if type(inputs) is not UpdateRhythmCountdownInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    auxiliary_cursor = inputs.auxiliary_cursor
    channel_cursor = inputs.channel_cursor
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    lookup_cursor = inputs.lookup_cursor
    parameter_cursor = inputs.parameter_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:0988:call
    from .business_notes import decrement_note_countdown
    from .contexts import DecrementNoteCountdownInput
    stack_cursor = state.push_word(stack_cursor, 2443)
    updated_audio_values_1 = decrement_note_countdown(state, DecrementNoteCountdownInput(channel_cursor=channel_cursor, conditions=conditions, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2443)))
    channel_cursor = updated_audio_values_1.channel_cursor
    conditions = updated_audio_values_1.conditions
    sample = updated_audio_values_1.sample
    stack_cursor = updated_audio_values_1.stack_cursor
    # source-effect driver:098b:call
    if bool(conditions & 0x40):
        from .business_notes import read_rhythm_note
        from .contexts import ReadRhythmNoteInput
        stack_cursor = state.push_word(stack_cursor, 2446)
        updated_audio_values_2 = read_rhythm_note(state, ReadRhythmNoteInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2446)))
        auxiliary_cursor = updated_audio_values_2.auxiliary_cursor
        channel_cursor = updated_audio_values_2.channel_cursor
        conditions = updated_audio_values_2.conditions
        count_and_data = updated_audio_values_2.count_and_data
        lookup_cursor = updated_audio_values_2.lookup_cursor
        parameter_cursor = updated_audio_values_2.parameter_cursor
        sample = updated_audio_values_2.sample
        stack_cursor = updated_audio_values_2.stack_cursor
    # source-effect driver:098e:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return UpdateRhythmCountdownResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def dispatch_extended_sequence_command(state: AudioState, inputs: DispatchExtendedSequenceCommandInput) -> DispatchExtendedSequenceCommandResult:
    """Dispatch extended sequence command."""
    checked_state(state)
    if type(inputs) is not DispatchExtendedSequenceCommandInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    lookup_cursor = inputs.lookup_cursor
    parameter_cursor = inputs.parameter_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:0b88:ld
    lookup_cursor = u16(3023)
    # source-effect driver:0b8b:rst
    from .business_hardware import index_word_pointer
    from .contexts import IndexWordPointerInput
    stack_cursor = state.push_word(stack_cursor, 2956)
    updated_audio_values_1 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2956)))
    conditions = updated_audio_values_1.conditions
    count_and_data = updated_audio_values_1.count_and_data
    lookup_cursor = updated_audio_values_1.lookup_cursor
    sample = updated_audio_values_1.sample
    stack_cursor = updated_audio_values_1.stack_cursor
    # source-effect driver:0b8c:inc
    parameter_cursor = u16(parameter_cursor + 1)
    # source-effect driver:0b8d:ld
    observed_byte_2 = state.read(parameter_cursor)
    sample = u8(observed_byte_2)
    # source-effect driver:0b8e:jp
    current_transfer_values_3 = DispatchExtendedSequenceCommandInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=inputs.continuation).validate(state)
    state.indirect_transfer("driver", lookup_cursor, current_transfer_values_3)
