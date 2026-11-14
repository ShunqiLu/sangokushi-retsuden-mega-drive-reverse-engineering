"""Voice envelopes, release/key-off gates, operator reset and silence lifetime.

Intermediate recovered algorithms; no CPU/timing or natural playback proof.
Live bus/stack aliases and original nonlocal returns remain unchanged.
"""
from .domain import (AudioState, Continuation, checked_state, u8, u16, low, high, replace_low, replace_high, logic_conditions, sum_byte, comparison_conditions, increment_byte, decrement_byte, tested_bit_conditions)
from .contexts import (UpdateVoiceEnvelopeInput, UpdateVoiceEnvelopeResult, SendKeyOffInput, SendKeyOffResult, SendKeyOffAfterGateInput, SendKeyOffAfterGateResult, ResetVoiceOperatorsInput, ResetVoiceOperatorsResult, EvaluateEnvelopeStepInput, EvaluateEnvelopeStepResult, StopChannelNoteInput, StopChannelNoteResult, SilenceOldPsgChannelInput, SilenceOldPsgChannelResult)

def update_voice_envelope(state: AudioState, inputs: UpdateVoiceEnvelopeInput) -> UpdateVoiceEnvelopeResult:
    """Update voice envelope."""
    checked_state(state)
    if type(inputs) is not UpdateVoiceEnvelopeInput:
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
    # source-effect driver:030c:ld
    observed_byte_1 = state.read(u16(channel_cursor + 24))
    sample = u8(observed_byte_1)
    # source-effect driver:030f:or
    sample = u8(sample | sample)
    conditions = logic_conditions(sample, False)
    # source-effect driver:0310:ret
    if bool(conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return UpdateVoiceEnvelopeResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0311:ret
    if bool(conditions & 0x80):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return UpdateVoiceEnvelopeResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0312:dec
    changed_byte_2, conditions = decrement_byte(sample, conditions)
    sample = u8(changed_byte_2)
    # source-effect driver:0313:ld
    count_and_data = replace_low(count_and_data, 10)
    # source-effect driver:0315:rst
    from .business_hardware import lookup_banked_root_pointer
    from .contexts import LookupBankedRootPointerInput
    stack_cursor = state.push_word(stack_cursor, 790)
    updated_audio_values_3 = lookup_banked_root_pointer(state, LookupBankedRootPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 790)))
    conditions = updated_audio_values_3.conditions
    count_and_data = updated_audio_values_3.count_and_data
    lookup_cursor = updated_audio_values_3.lookup_cursor
    sample = updated_audio_values_3.sample
    stack_cursor = updated_audio_values_3.stack_cursor
    # source-effect driver:0316:rst
    from .business_hardware import index_word_pointer
    from .contexts import IndexWordPointerInput
    stack_cursor = state.push_word(stack_cursor, 791)
    updated_audio_values_4 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 791)))
    conditions = updated_audio_values_4.conditions
    count_and_data = updated_audio_values_4.count_and_data
    lookup_cursor = updated_audio_values_4.lookup_cursor
    sample = updated_audio_values_4.sample
    stack_cursor = updated_audio_values_4.stack_cursor
    # source-effect driver:0317:call
    from .business_envelopes import evaluate_envelope_step
    from .contexts import EvaluateEnvelopeStepInput
    stack_cursor = state.push_word(stack_cursor, 794)
    updated_audio_values_5 = evaluate_envelope_step(state, EvaluateEnvelopeStepInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 794)))
    auxiliary_cursor = updated_audio_values_5.auxiliary_cursor
    channel_cursor = updated_audio_values_5.channel_cursor
    conditions = updated_audio_values_5.conditions
    count_and_data = updated_audio_values_5.count_and_data
    lookup_cursor = updated_audio_values_5.lookup_cursor
    parameter_cursor = updated_audio_values_5.parameter_cursor
    sample = updated_audio_values_5.sample
    stack_cursor = updated_audio_values_5.stack_cursor
    # source-effect driver:031a:ld
    observed_byte_6 = state.read(u16(channel_cursor + 29))
    lookup_cursor = replace_high(lookup_cursor, observed_byte_6)
    # source-effect driver:031d:ld
    observed_byte_7 = state.read(u16(channel_cursor + 28))
    lookup_cursor = replace_low(lookup_cursor, observed_byte_7)
    # source-effect driver:0320:ld
    parameter_cursor = u16(1245)
    # source-effect driver:0323:ld
    count_and_data = replace_high(count_and_data, 4)
    # source-effect driver:0325:ld
    observed_byte_8 = state.read(u16(channel_cursor + 25))
    count_and_data = replace_low(count_and_data, observed_byte_8)
    while True:
        # source-effect driver:0328:push
        stack_cursor = state.push_word(stack_cursor, ((sample << 8) | conditions))
        # source-effect driver:0329:sra
        shifted_byte_9 = low(count_and_data)
        shift_result_10 = u8((shifted_byte_9 >> 1) | (shifted_byte_9 & 0x80))
        conditions = logic_conditions(shift_result_10) | (shifted_byte_9 & 1)
        count_and_data = replace_low(count_and_data, shift_result_10)
        # source-effect driver:032b:push
        stack_cursor = state.push_word(stack_cursor, count_and_data)
        # source-effect driver:032c:jr
        if not (not (conditions & 1)):
            # source-effect driver:032e:add
            observed_byte_11 = state.read(lookup_cursor)
            arithmetic_result_12, conditions = sum_byte(sample, observed_byte_11)
            sample = u8(arithmetic_result_12)
            # source-effect driver:032f:and
            sample = u8(sample & 127)
            conditions = logic_conditions(sample, True)
            # source-effect driver:0331:ld
            count_and_data = replace_low(count_and_data, sample)
            # source-effect driver:0332:ld
            observed_byte_13 = state.read(parameter_cursor)
            sample = u8(observed_byte_13)
            # source-effect driver:0333:rst
            from .business_hardware import write_channel_fm_register
            from .contexts import WriteChannelFmRegisterInput
            stack_cursor = state.push_word(stack_cursor, 820)
            updated_audio_values_14 = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 820)))
            channel_cursor = updated_audio_values_14.channel_cursor
            conditions = updated_audio_values_14.conditions
            count_and_data = updated_audio_values_14.count_and_data
            sample = updated_audio_values_14.sample
            stack_cursor = updated_audio_values_14.stack_cursor
        # source-effect driver:0334:pop
        saved_audio_word_15, stack_cursor = state.pop_word(stack_cursor)
        count_and_data = u16(saved_audio_word_15)
        # source-effect driver:0335:inc
        parameter_cursor = u16(parameter_cursor + 1)
        # source-effect driver:0336:inc
        lookup_cursor = u16(lookup_cursor + 1)
        # source-effect driver:0337:pop
        saved_audio_word_16, stack_cursor = state.pop_word(stack_cursor)
        sample, conditions = high(saved_audio_word_16), low(saved_audio_word_16)
        # source-effect driver:0338:djnz
        count_and_data = replace_high(count_and_data, u8(high(count_and_data) - 1))
        if high(count_and_data) != 0:
            continue
        break
    # source-effect driver:033a:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return UpdateVoiceEnvelopeResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def send_key_off(state: AudioState, inputs: SendKeyOffInput) -> SendKeyOffResult:
    """Send key off."""
    checked_state(state)
    if type(inputs) is not SendKeyOffInput:
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
    # source-effect driver:0422:ld
    observed_byte_1 = state.read(u16(channel_cursor + 0))
    sample = u8(observed_byte_1)
    # source-effect driver:0425:and
    sample = u8(sample & 6)
    conditions = logic_conditions(sample, True)
    # source-effect driver:0427:ret
    if not (conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return SendKeyOffResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0428:ld
    observed_byte_2 = state.read(u16(channel_cursor + 1))
    count_and_data = replace_low(count_and_data, observed_byte_2)
    # source-effect driver:042b:bit
    conditions = tested_bit_conditions(low(count_and_data), 7, conditions)
    # source-effect driver:042d:ret
    if not (conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return SendKeyOffResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:042e:ld
    sample = u8(40)
    # source-effect driver:0430:rst
    from .business_hardware import write_fm_port_zero_entry
    from .contexts import WriteFmPortZeroEntryInput
    stack_cursor = state.push_word(stack_cursor, 1073)
    updated_audio_values_3 = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 1073)))
    channel_cursor = updated_audio_values_3.channel_cursor
    conditions = updated_audio_values_3.conditions
    count_and_data = updated_audio_values_3.count_and_data
    sample = updated_audio_values_3.sample
    stack_cursor = updated_audio_values_3.stack_cursor
    # source-effect driver:0431:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return SendKeyOffResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def send_key_off_after_gate(state: AudioState, inputs: SendKeyOffAfterGateInput) -> SendKeyOffAfterGateResult:
    """Send key off after gate."""
    checked_state(state)
    if type(inputs) is not SendKeyOffAfterGateInput:
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
    # source-effect driver:0428:ld
    observed_byte_1 = state.read(u16(channel_cursor + 1))
    count_and_data = replace_low(count_and_data, observed_byte_1)
    # source-effect driver:042b:bit
    conditions = tested_bit_conditions(low(count_and_data), 7, conditions)
    # source-effect driver:042d:ret
    if not (conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return SendKeyOffAfterGateResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:042e:ld
    sample = u8(40)
    # source-effect driver:0430:rst
    from .business_hardware import write_fm_port_zero_entry
    from .contexts import WriteFmPortZeroEntryInput
    stack_cursor = state.push_word(stack_cursor, 1073)
    updated_audio_values_2 = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 1073)))
    channel_cursor = updated_audio_values_2.channel_cursor
    conditions = updated_audio_values_2.conditions
    count_and_data = updated_audio_values_2.count_and_data
    sample = updated_audio_values_2.sample
    stack_cursor = updated_audio_values_2.stack_cursor
    # source-effect driver:0431:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return SendKeyOffAfterGateResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def reset_voice_operators(state: AudioState, inputs: ResetVoiceOperatorsInput) -> ResetVoiceOperatorsResult:
    """Reset voice operators."""
    checked_state(state)
    if type(inputs) is not ResetVoiceOperatorsInput:
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
    # source-effect driver:08c8:call
    from .business_loaders import reset_operator_release
    from .contexts import ResetOperatorReleaseInput
    stack_cursor = state.push_word(stack_cursor, 2251)
    updated_audio_values_1 = reset_operator_release(state, ResetOperatorReleaseInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2251)))
    channel_cursor = updated_audio_values_1.channel_cursor
    conditions = updated_audio_values_1.conditions
    count_and_data = updated_audio_values_1.count_and_data
    sample = updated_audio_values_1.sample
    stack_cursor = updated_audio_values_1.stack_cursor
    # source-effect driver:08cb:ld
    sample = u8(64)
    # source-effect driver:08cd:ld
    count_and_data = replace_low(count_and_data, 127)
    # source-effect driver:08cf:call
    from .business_loaders import write_operator_group
    from .contexts import WriteOperatorGroupInput
    stack_cursor = state.push_word(stack_cursor, 2258)
    updated_audio_values_2 = write_operator_group(state, WriteOperatorGroupInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2258)))
    channel_cursor = updated_audio_values_2.channel_cursor
    conditions = updated_audio_values_2.conditions
    count_and_data = updated_audio_values_2.count_and_data
    sample = updated_audio_values_2.sample
    stack_cursor = updated_audio_values_2.stack_cursor
    # source-effect driver:08d2:ld
    observed_byte_3 = state.read(u16(channel_cursor + 1))
    count_and_data = replace_low(count_and_data, observed_byte_3)
    # source-effect driver:08d5:jp
    pass  # Static control continuation is structured below.
    # source-effect driver:042e:ld
    sample = u8(40)
    # source-effect driver:0430:rst
    from .business_hardware import write_fm_port_zero_entry
    from .contexts import WriteFmPortZeroEntryInput
    stack_cursor = state.push_word(stack_cursor, 1073)
    updated_audio_values_4 = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 1073)))
    channel_cursor = updated_audio_values_4.channel_cursor
    conditions = updated_audio_values_4.conditions
    count_and_data = updated_audio_values_4.count_and_data
    sample = updated_audio_values_4.sample
    stack_cursor = updated_audio_values_4.stack_cursor
    # source-effect driver:0431:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return ResetVoiceOperatorsResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def evaluate_envelope_step(state: AudioState, inputs: EvaluateEnvelopeStepInput) -> EvaluateEnvelopeStepResult:
    """Evaluate envelope step."""
    checked_state(state)
    if type(inputs) is not EvaluateEnvelopeStepInput:
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
    while True:
        # source-effect driver:0f7b:push
        stack_cursor = state.push_word(stack_cursor, lookup_cursor)
        # source-effect driver:0f7c:ld
        observed_byte_1 = state.read(u16(channel_cursor + 23))
        count_and_data = replace_low(count_and_data, observed_byte_1)
        # source-effect driver:0f7f:call
        from .business_voice import read_indexed_envelope
        from .contexts import ReadIndexedEnvelopeInput
        stack_cursor = state.push_word(stack_cursor, 3970)
        updated_audio_values_2 = read_indexed_envelope(state, ReadIndexedEnvelopeInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3970)))
        conditions = updated_audio_values_2.conditions
        count_and_data = updated_audio_values_2.count_and_data
        lookup_cursor = updated_audio_values_2.lookup_cursor
        sample = updated_audio_values_2.sample
        stack_cursor = updated_audio_values_2.stack_cursor
        # source-effect driver:0f82:pop
        saved_audio_word_3, stack_cursor = state.pop_word(stack_cursor)
        lookup_cursor = u16(saved_audio_word_3)
        # source-effect driver:0f83:bit
        conditions = tested_bit_conditions(sample, 7, conditions)
        # source-effect driver:0f85:jr
        if bool(conditions & 0x40):
            # source-effect driver:0fa8:inc
            observed_byte_4 = state.read(u16(channel_cursor + 23))
            changed_byte_5, conditions = increment_byte(observed_byte_4, conditions)
            state.write(u16(channel_cursor + 23), u8(changed_byte_5))
            # source-effect driver:0fab:ret
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return EvaluateEnvelopeStepResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
            break
        # source-effect driver:0f87:cp
        conditions = comparison_conditions(sample, 131)
        # source-effect driver:0f89:jr
        if bool(conditions & 0x40):
            break
        # source-effect driver:0f8b:cp
        conditions = comparison_conditions(sample, 129)
        # source-effect driver:0f8d:jr
        if bool(conditions & 0x40):
            # source-effect driver:0fa2:pop
            saved_audio_word_6, stack_cursor = state.pop_word(stack_cursor)
            lookup_cursor = u16(saved_audio_word_6)
            # source-effect driver:0fa3:set
            observed_byte_7 = state.read(u16(channel_cursor + 0))
            state.write(u16(channel_cursor + 0), u8(observed_byte_7 | 16))
            # source-effect driver:0fa7:ret
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return EvaluateEnvelopeStepResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
            break
        # source-effect driver:0f8f:cp
        conditions = comparison_conditions(sample, 128)
        # source-effect driver:0f91:jr
        if bool(conditions & 0x40):
            # source-effect driver:0f9f:xor
            sample = u8(sample ^ sample)
            conditions = logic_conditions(sample, False)
            # source-effect driver:0fa0:jr
            pass  # Static control continuation is structured below.
        else:
            # source-effect driver:0f93:inc
            count_and_data = u16(count_and_data + 1)
            # source-effect driver:0f94:ld
            observed_byte_8 = state.read(count_and_data)
            sample = u8(observed_byte_8)
            # source-effect driver:0f95:jr
            pass  # Static control continuation is structured below.
        # source-effect driver:0f78:ld
        state.write(u16(channel_cursor + 23), u8(sample))
        continue
    # source-effect driver:0f97:set
    observed_byte_9 = state.read(u16(channel_cursor + 0))
    state.write(u16(channel_cursor + 0), u8(observed_byte_9 | 16))
    # source-effect driver:0f9b:pop
    saved_audio_word_10, stack_cursor = state.pop_word(stack_cursor)
    lookup_cursor = u16(saved_audio_word_10)
    # source-effect driver:0f9c:jp
    pass  # Static control continuation is structured below.
    # source-effect driver:0fac:set
    observed_byte_11 = state.read(u16(channel_cursor + 0))
    state.write(u16(channel_cursor + 0), u8(observed_byte_11 | 16))
    # source-effect driver:0fb0:bit
    observed_byte_12 = state.read(u16(channel_cursor + 0))
    conditions = state.memory_bit_conditions(observed_byte_12, 2, conditions, u16(channel_cursor + 0), True)
    # source-effect driver:0fb4:ret
    if not (conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return EvaluateEnvelopeStepResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0fb5:ld
    sample = u8(31)
    # source-effect driver:0fb7:add
    observed_byte_13 = state.read(u16(channel_cursor + 1))
    arithmetic_result_14, conditions = sum_byte(sample, observed_byte_13)
    sample = u8(arithmetic_result_14)
    # source-effect driver:0fba:or
    sample = u8(sample | sample)
    conditions = logic_conditions(sample, False)
    # source-effect driver:0fbb:ret
    if not (conditions & 0x80):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return EvaluateEnvelopeStepResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0fbc:ld
    state.write(32529, u8(sample))
    # source-effect driver:0fbf:bit
    observed_byte_15 = state.read(u16(channel_cursor + 0))
    conditions = state.memory_bit_conditions(observed_byte_15, 0, conditions, u16(channel_cursor + 0), True)
    # source-effect driver:0fc3:ret
    if bool(conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return EvaluateEnvelopeStepResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0fc4:ld
    sample = u8(255)
    # source-effect driver:0fc6:ld
    state.write(32529, u8(sample))
    # source-effect driver:0fc9:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return EvaluateEnvelopeStepResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def stop_channel_note(state: AudioState, inputs: StopChannelNoteInput) -> StopChannelNoteResult:
    """Stop channel note."""
    checked_state(state)
    if type(inputs) is not StopChannelNoteInput:
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
    # source-effect driver:0fac:set
    observed_byte_1 = state.read(u16(channel_cursor + 0))
    state.write(u16(channel_cursor + 0), u8(observed_byte_1 | 16))
    # source-effect driver:0fb0:bit
    observed_byte_2 = state.read(u16(channel_cursor + 0))
    conditions = state.memory_bit_conditions(observed_byte_2, 2, conditions, u16(channel_cursor + 0), True)
    # source-effect driver:0fb4:ret
    if not (conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return StopChannelNoteResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0fb5:ld
    sample = u8(31)
    # source-effect driver:0fb7:add
    observed_byte_3 = state.read(u16(channel_cursor + 1))
    arithmetic_result_4, conditions = sum_byte(sample, observed_byte_3)
    sample = u8(arithmetic_result_4)
    # source-effect driver:0fba:or
    sample = u8(sample | sample)
    conditions = logic_conditions(sample, False)
    # source-effect driver:0fbb:ret
    if not (conditions & 0x80):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return StopChannelNoteResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0fbc:ld
    state.write(32529, u8(sample))
    # source-effect driver:0fbf:bit
    observed_byte_5 = state.read(u16(channel_cursor + 0))
    conditions = state.memory_bit_conditions(observed_byte_5, 0, conditions, u16(channel_cursor + 0), True)
    # source-effect driver:0fc3:ret
    if bool(conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return StopChannelNoteResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0fc4:ld
    sample = u8(255)
    # source-effect driver:0fc6:ld
    state.write(32529, u8(sample))
    # source-effect driver:0fc9:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return StopChannelNoteResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def silence_old_psg_channel(state: AudioState, inputs: SilenceOldPsgChannelInput) -> SilenceOldPsgChannelResult:
    """Silence old psg channel."""
    checked_state(state)
    if type(inputs) is not SilenceOldPsgChannelInput:
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
    # source-effect driver:0fb5:ld
    sample = u8(31)
    # source-effect driver:0fb7:add
    observed_byte_1 = state.read(u16(channel_cursor + 1))
    arithmetic_result_2, conditions = sum_byte(sample, observed_byte_1)
    sample = u8(arithmetic_result_2)
    # source-effect driver:0fba:or
    sample = u8(sample | sample)
    conditions = logic_conditions(sample, False)
    # source-effect driver:0fbb:ret
    if not (conditions & 0x80):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return SilenceOldPsgChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0fbc:ld
    state.write(32529, u8(sample))
    # source-effect driver:0fbf:bit
    observed_byte_3 = state.read(u16(channel_cursor + 0))
    conditions = state.memory_bit_conditions(observed_byte_3, 0, conditions, u16(channel_cursor + 0), True)
    # source-effect driver:0fc3:ret
    if bool(conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return SilenceOldPsgChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0fc4:ld
    sample = u8(255)
    # source-effect driver:0fc6:ld
    state.write(32529, u8(sample))
    # source-effect driver:0fc9:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return SilenceOldPsgChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
