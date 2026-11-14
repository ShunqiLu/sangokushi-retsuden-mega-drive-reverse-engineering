"""Channel-tick coordination with live frequency, pan and envelope services.

Intermediate recovered algorithms; no CPU/timing or natural playback proof.
Live bus/stack aliases and original nonlocal returns remain unchanged.
"""
from .domain import (AudioState, Continuation, AlternateGroup, checked_state, u8, u16, low, high, replace_low, replace_high, logic_conditions, sum_byte, difference_byte, comparison_conditions, decrement_byte, sum_word, tested_bit_conditions)
from .contexts import (UpdateFmChannelInput, UpdateFmChannelResult)

def update_fm_channel(state: AudioState, inputs: UpdateFmChannelInput) -> UpdateFmChannelResult:
    """Update fm channel."""
    checked_state(state)
    if type(inputs) is not UpdateFmChannelInput:
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
    # source-effect driver:0139:bit
    observed_byte_1 = state.read(u16(channel_cursor + 1))
    conditions = state.memory_bit_conditions(observed_byte_1, 7, conditions, u16(channel_cursor + 1), True)
    # source-effect driver:013d:jp
    if not (conditions & 0x40):
        # source-effect driver:0f05:call
        from .business_notes import decrement_note_countdown
        from .contexts import DecrementNoteCountdownInput
        stack_cursor = state.push_word(stack_cursor, 3848)
        updated_audio_values_2 = decrement_note_countdown(state, DecrementNoteCountdownInput(channel_cursor=channel_cursor, conditions=conditions, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3848)))
        channel_cursor = updated_audio_values_2.channel_cursor
        conditions = updated_audio_values_2.conditions
        sample = updated_audio_values_2.sample
        stack_cursor = updated_audio_values_2.stack_cursor
        # source-effect driver:0f08:jr
        if not (conditions & 0x40):
            # source-effect driver:0f17:ld
            observed_byte_3 = state.read(u16(channel_cursor + 30))
            sample = u8(observed_byte_3)
            # source-effect driver:0f1a:or
            sample = u8(sample | sample)
            conditions = logic_conditions(sample, False)
            # source-effect driver:0f1b:jr
            if bool(conditions & 0x40):
                # source-effect driver:0f23:call
                from .business_pitch import calculate_channel_pitch
                from .contexts import CalculateChannelPitchInput
                stack_cursor = state.push_word(stack_cursor, 3878)
                updated_audio_values_4 = calculate_channel_pitch(state, CalculateChannelPitchInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3878)))
                channel_cursor = updated_audio_values_4.channel_cursor
                conditions = updated_audio_values_4.conditions
                count_and_data = updated_audio_values_4.count_and_data
                lookup_cursor = updated_audio_values_4.lookup_cursor
                parameter_cursor = updated_audio_values_4.parameter_cursor
                sample = updated_audio_values_4.sample
                stack_cursor = updated_audio_values_4.stack_cursor
                # source-effect driver:0f26:call
                from .business_pitch import update_pitch_modulation
                from .contexts import UpdatePitchModulationInput
                stack_cursor = state.push_word(stack_cursor, 3881)
                updated_audio_values_5 = update_pitch_modulation(state, UpdatePitchModulationInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3881)))
                auxiliary_cursor = updated_audio_values_5.auxiliary_cursor
                channel_cursor = updated_audio_values_5.channel_cursor
                conditions = updated_audio_values_5.conditions
                count_and_data = updated_audio_values_5.count_and_data
                lookup_cursor = updated_audio_values_5.lookup_cursor
                parameter_cursor = updated_audio_values_5.parameter_cursor
                sample = updated_audio_values_5.sample
                stack_cursor = updated_audio_values_5.stack_cursor
                # source-effect driver:0f29:bit
                observed_byte_6 = state.read(u16(channel_cursor + 0))
                conditions = state.memory_bit_conditions(observed_byte_6, 2, conditions, u16(channel_cursor + 0), True)
                # source-effect driver:0f2d:ret
                if not (conditions & 0x40):
                    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                    return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                # source-effect driver:0f2e:ld
                observed_byte_7 = state.read(u16(channel_cursor + 1))
                count_and_data = replace_low(count_and_data, observed_byte_7)
                # source-effect driver:0f31:ld
                sample = u8(low(lookup_cursor))
                # source-effect driver:0f32:and
                sample = u8(sample & 15)
                conditions = logic_conditions(sample, True)
                # source-effect driver:0f34:or
                sample = u8(sample | low(count_and_data))
                conditions = logic_conditions(sample, False)
                # source-effect driver:0f35:ld
                state.write(32529, u8(sample))
                # source-effect driver:0f38:ld
                sample = u8(low(lookup_cursor))
                # source-effect driver:0f39:and
                sample = u8(sample & 240)
                conditions = logic_conditions(sample, True)
                # source-effect driver:0f3b:or
                sample = u8(sample | high(lookup_cursor))
                conditions = logic_conditions(sample, False)
                # source-effect driver:0f3c:rrca
                rotated_sample_8 = sample
                sample = u8((rotated_sample_8 >> 1) | (rotated_sample_8 << 7))
                conditions = (conditions & 0xC4) | (sample & 0x28) | (rotated_sample_8 & 1)
                # source-effect driver:0f3d:rrca
                rotated_sample_9 = sample
                sample = u8((rotated_sample_9 >> 1) | (rotated_sample_9 << 7))
                conditions = (conditions & 0xC4) | (sample & 0x28) | (rotated_sample_9 & 1)
                # source-effect driver:0f3e:rrca
                rotated_sample_10 = sample
                sample = u8((rotated_sample_10 >> 1) | (rotated_sample_10 << 7))
                conditions = (conditions & 0xC4) | (sample & 0x28) | (rotated_sample_10 & 1)
                # source-effect driver:0f3f:rrca
                rotated_sample_11 = sample
                sample = u8((rotated_sample_11 >> 1) | (rotated_sample_11 << 7))
                conditions = (conditions & 0xC4) | (sample & 0x28) | (rotated_sample_11 & 1)
                # source-effect driver:0f40:ld
                state.write(32529, u8(sample))
                # source-effect driver:0f43:ld
                observed_byte_12 = state.read(u16(channel_cursor + 8))
                sample = u8(observed_byte_12)
                # source-effect driver:0f46:or
                sample = u8(sample | sample)
                conditions = logic_conditions(sample, False)
                # source-effect driver:0f47:ld
                count_and_data = replace_low(count_and_data, 0)
                # source-effect driver:0f49:jr
                if not (bool(conditions & 0x40)):
                    # source-effect driver:0f4b:dec
                    changed_byte_13, conditions = decrement_byte(sample, conditions)
                    sample = u8(changed_byte_13)
                    # source-effect driver:0f4c:ld
                    count_and_data = replace_low(count_and_data, 10)
                    # source-effect driver:0f4e:rst
                    from .business_hardware import lookup_banked_root_pointer
                    from .contexts import LookupBankedRootPointerInput
                    stack_cursor = state.push_word(stack_cursor, 3919)
                    updated_audio_values_14 = lookup_banked_root_pointer(state, LookupBankedRootPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3919)))
                    conditions = updated_audio_values_14.conditions
                    count_and_data = updated_audio_values_14.count_and_data
                    lookup_cursor = updated_audio_values_14.lookup_cursor
                    sample = updated_audio_values_14.sample
                    stack_cursor = updated_audio_values_14.stack_cursor
                    # source-effect driver:0f4f:rst
                    from .business_hardware import index_word_pointer
                    from .contexts import IndexWordPointerInput
                    stack_cursor = state.push_word(stack_cursor, 3920)
                    updated_audio_values_15 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3920)))
                    conditions = updated_audio_values_15.conditions
                    count_and_data = updated_audio_values_15.count_and_data
                    lookup_cursor = updated_audio_values_15.lookup_cursor
                    sample = updated_audio_values_15.sample
                    stack_cursor = updated_audio_values_15.stack_cursor
                    # source-effect driver:0f50:call
                    from .business_envelopes import evaluate_envelope_step
                    from .contexts import EvaluateEnvelopeStepInput
                    stack_cursor = state.push_word(stack_cursor, 3923)
                    updated_audio_values_16 = evaluate_envelope_step(state, EvaluateEnvelopeStepInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3923)))
                    auxiliary_cursor = updated_audio_values_16.auxiliary_cursor
                    channel_cursor = updated_audio_values_16.channel_cursor
                    conditions = updated_audio_values_16.conditions
                    count_and_data = updated_audio_values_16.count_and_data
                    lookup_cursor = updated_audio_values_16.lookup_cursor
                    parameter_cursor = updated_audio_values_16.parameter_cursor
                    sample = updated_audio_values_16.sample
                    stack_cursor = updated_audio_values_16.stack_cursor
                    # source-effect driver:0f53:ld
                    count_and_data = replace_low(count_and_data, sample)
                # source-effect driver:0f54:bit
                observed_byte_17 = state.read(u16(channel_cursor + 0))
                conditions = state.memory_bit_conditions(observed_byte_17, 4, conditions, u16(channel_cursor + 0), True)
                # source-effect driver:0f58:ret
                if not (conditions & 0x40):
                    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                    return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                # source-effect driver:0f59:ld
                observed_byte_18 = state.read(u16(channel_cursor + 6))
                sample = u8(observed_byte_18)
                # source-effect driver:0f5c:add
                arithmetic_result_19, conditions = sum_byte(sample, low(count_and_data))
                sample = u8(arithmetic_result_19)
                # source-effect driver:0f5d:bit
                conditions = tested_bit_conditions(sample, 4, conditions)
                # source-effect driver:0f5f:jr
                if not (bool(conditions & 0x40)):
                    # source-effect driver:0f61:ld
                    sample = u8(15)
                # source-effect driver:0f63:or
                observed_byte_20 = state.read(u16(channel_cursor + 1))
                sample = u8(sample | observed_byte_20)
                conditions = logic_conditions(sample, False)
                # source-effect driver:0f66:add
                arithmetic_result_21, conditions = sum_byte(sample, 16)
                sample = u8(arithmetic_result_21)
                # source-effect driver:0f68:bit
                observed_byte_22 = state.read(u16(channel_cursor + 0))
                conditions = state.memory_bit_conditions(observed_byte_22, 0, conditions, u16(channel_cursor + 0), True)
                # source-effect driver:0f6c:jr
                if not (conditions & 0x40):
                    # source-effect driver:0f72:add
                    arithmetic_result_23, conditions = sum_byte(sample, 32)
                    sample = u8(arithmetic_result_23)
                    # source-effect driver:0f74:ld
                    state.write(32529, u8(sample))
                    # source-effect driver:0f77:ret
                    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                    return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                else:
                    # source-effect driver:0f6e:ld
                    state.write(32529, u8(sample))
                    # source-effect driver:0f71:ret
                    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                    return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
            else:
                # source-effect driver:0f1d:dec
                observed_byte_24 = state.read(u16(channel_cursor + 30))
                changed_byte_25, conditions = decrement_byte(observed_byte_24, conditions)
                state.write(u16(channel_cursor + 30), u8(changed_byte_25))
                # source-effect driver:0f20:jp
                if bool(conditions & 0x40):
                    # source-effect driver:0fac:set
                    observed_byte_26 = state.read(u16(channel_cursor + 0))
                    state.write(u16(channel_cursor + 0), u8(observed_byte_26 | 16))
                    # source-effect driver:0fb0:bit
                    observed_byte_27 = state.read(u16(channel_cursor + 0))
                    conditions = state.memory_bit_conditions(observed_byte_27, 2, conditions, u16(channel_cursor + 0), True)
                    # source-effect driver:0fb4:ret
                    if not (conditions & 0x40):
                        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                        return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                    # source-effect driver:0fb5:ld
                    sample = u8(31)
                    # source-effect driver:0fb7:add
                    observed_byte_28 = state.read(u16(channel_cursor + 1))
                    arithmetic_result_29, conditions = sum_byte(sample, observed_byte_28)
                    sample = u8(arithmetic_result_29)
                    # source-effect driver:0fba:or
                    sample = u8(sample | sample)
                    conditions = logic_conditions(sample, False)
                    # source-effect driver:0fbb:ret
                    if not (conditions & 0x80):
                        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                        return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                    # source-effect driver:0fbc:ld
                    state.write(32529, u8(sample))
                    # source-effect driver:0fbf:bit
                    observed_byte_30 = state.read(u16(channel_cursor + 0))
                    conditions = state.memory_bit_conditions(observed_byte_30, 0, conditions, u16(channel_cursor + 0), True)
                    # source-effect driver:0fc3:ret
                    if bool(conditions & 0x40):
                        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                        return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                    # source-effect driver:0fc4:ld
                    sample = u8(255)
                    # source-effect driver:0fc6:ld
                    state.write(32529, u8(sample))
                    # source-effect driver:0fc9:ret
                    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                    return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                else:
                    # source-effect driver:0f23:call
                    from .business_pitch import calculate_channel_pitch
                    from .contexts import CalculateChannelPitchInput
                    stack_cursor = state.push_word(stack_cursor, 3878)
                    updated_audio_values_31 = calculate_channel_pitch(state, CalculateChannelPitchInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3878)))
                    channel_cursor = updated_audio_values_31.channel_cursor
                    conditions = updated_audio_values_31.conditions
                    count_and_data = updated_audio_values_31.count_and_data
                    lookup_cursor = updated_audio_values_31.lookup_cursor
                    parameter_cursor = updated_audio_values_31.parameter_cursor
                    sample = updated_audio_values_31.sample
                    stack_cursor = updated_audio_values_31.stack_cursor
                    # source-effect driver:0f26:call
                    from .business_pitch import update_pitch_modulation
                    from .contexts import UpdatePitchModulationInput
                    stack_cursor = state.push_word(stack_cursor, 3881)
                    updated_audio_values_32 = update_pitch_modulation(state, UpdatePitchModulationInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3881)))
                    auxiliary_cursor = updated_audio_values_32.auxiliary_cursor
                    channel_cursor = updated_audio_values_32.channel_cursor
                    conditions = updated_audio_values_32.conditions
                    count_and_data = updated_audio_values_32.count_and_data
                    lookup_cursor = updated_audio_values_32.lookup_cursor
                    parameter_cursor = updated_audio_values_32.parameter_cursor
                    sample = updated_audio_values_32.sample
                    stack_cursor = updated_audio_values_32.stack_cursor
                    # source-effect driver:0f29:bit
                    observed_byte_33 = state.read(u16(channel_cursor + 0))
                    conditions = state.memory_bit_conditions(observed_byte_33, 2, conditions, u16(channel_cursor + 0), True)
                    # source-effect driver:0f2d:ret
                    if not (conditions & 0x40):
                        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                        return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                    # source-effect driver:0f2e:ld
                    observed_byte_34 = state.read(u16(channel_cursor + 1))
                    count_and_data = replace_low(count_and_data, observed_byte_34)
                    # source-effect driver:0f31:ld
                    sample = u8(low(lookup_cursor))
                    # source-effect driver:0f32:and
                    sample = u8(sample & 15)
                    conditions = logic_conditions(sample, True)
                    # source-effect driver:0f34:or
                    sample = u8(sample | low(count_and_data))
                    conditions = logic_conditions(sample, False)
                    # source-effect driver:0f35:ld
                    state.write(32529, u8(sample))
                    # source-effect driver:0f38:ld
                    sample = u8(low(lookup_cursor))
                    # source-effect driver:0f39:and
                    sample = u8(sample & 240)
                    conditions = logic_conditions(sample, True)
                    # source-effect driver:0f3b:or
                    sample = u8(sample | high(lookup_cursor))
                    conditions = logic_conditions(sample, False)
                    # source-effect driver:0f3c:rrca
                    rotated_sample_35 = sample
                    sample = u8((rotated_sample_35 >> 1) | (rotated_sample_35 << 7))
                    conditions = (conditions & 0xC4) | (sample & 0x28) | (rotated_sample_35 & 1)
                    # source-effect driver:0f3d:rrca
                    rotated_sample_36 = sample
                    sample = u8((rotated_sample_36 >> 1) | (rotated_sample_36 << 7))
                    conditions = (conditions & 0xC4) | (sample & 0x28) | (rotated_sample_36 & 1)
                    # source-effect driver:0f3e:rrca
                    rotated_sample_37 = sample
                    sample = u8((rotated_sample_37 >> 1) | (rotated_sample_37 << 7))
                    conditions = (conditions & 0xC4) | (sample & 0x28) | (rotated_sample_37 & 1)
                    # source-effect driver:0f3f:rrca
                    rotated_sample_38 = sample
                    sample = u8((rotated_sample_38 >> 1) | (rotated_sample_38 << 7))
                    conditions = (conditions & 0xC4) | (sample & 0x28) | (rotated_sample_38 & 1)
                    # source-effect driver:0f40:ld
                    state.write(32529, u8(sample))
                    # source-effect driver:0f43:ld
                    observed_byte_39 = state.read(u16(channel_cursor + 8))
                    sample = u8(observed_byte_39)
                    # source-effect driver:0f46:or
                    sample = u8(sample | sample)
                    conditions = logic_conditions(sample, False)
                    # source-effect driver:0f47:ld
                    count_and_data = replace_low(count_and_data, 0)
                    # source-effect driver:0f49:jr
                    if not (bool(conditions & 0x40)):
                        # source-effect driver:0f4b:dec
                        changed_byte_40, conditions = decrement_byte(sample, conditions)
                        sample = u8(changed_byte_40)
                        # source-effect driver:0f4c:ld
                        count_and_data = replace_low(count_and_data, 10)
                        # source-effect driver:0f4e:rst
                        from .business_hardware import lookup_banked_root_pointer
                        from .contexts import LookupBankedRootPointerInput
                        stack_cursor = state.push_word(stack_cursor, 3919)
                        updated_audio_values_41 = lookup_banked_root_pointer(state, LookupBankedRootPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3919)))
                        conditions = updated_audio_values_41.conditions
                        count_and_data = updated_audio_values_41.count_and_data
                        lookup_cursor = updated_audio_values_41.lookup_cursor
                        sample = updated_audio_values_41.sample
                        stack_cursor = updated_audio_values_41.stack_cursor
                        # source-effect driver:0f4f:rst
                        from .business_hardware import index_word_pointer
                        from .contexts import IndexWordPointerInput
                        stack_cursor = state.push_word(stack_cursor, 3920)
                        updated_audio_values_42 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3920)))
                        conditions = updated_audio_values_42.conditions
                        count_and_data = updated_audio_values_42.count_and_data
                        lookup_cursor = updated_audio_values_42.lookup_cursor
                        sample = updated_audio_values_42.sample
                        stack_cursor = updated_audio_values_42.stack_cursor
                        # source-effect driver:0f50:call
                        from .business_envelopes import evaluate_envelope_step
                        from .contexts import EvaluateEnvelopeStepInput
                        stack_cursor = state.push_word(stack_cursor, 3923)
                        updated_audio_values_43 = evaluate_envelope_step(state, EvaluateEnvelopeStepInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3923)))
                        auxiliary_cursor = updated_audio_values_43.auxiliary_cursor
                        channel_cursor = updated_audio_values_43.channel_cursor
                        conditions = updated_audio_values_43.conditions
                        count_and_data = updated_audio_values_43.count_and_data
                        lookup_cursor = updated_audio_values_43.lookup_cursor
                        parameter_cursor = updated_audio_values_43.parameter_cursor
                        sample = updated_audio_values_43.sample
                        stack_cursor = updated_audio_values_43.stack_cursor
                        # source-effect driver:0f53:ld
                        count_and_data = replace_low(count_and_data, sample)
                    # source-effect driver:0f54:bit
                    observed_byte_44 = state.read(u16(channel_cursor + 0))
                    conditions = state.memory_bit_conditions(observed_byte_44, 4, conditions, u16(channel_cursor + 0), True)
                    # source-effect driver:0f58:ret
                    if not (conditions & 0x40):
                        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                        return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                    # source-effect driver:0f59:ld
                    observed_byte_45 = state.read(u16(channel_cursor + 6))
                    sample = u8(observed_byte_45)
                    # source-effect driver:0f5c:add
                    arithmetic_result_46, conditions = sum_byte(sample, low(count_and_data))
                    sample = u8(arithmetic_result_46)
                    # source-effect driver:0f5d:bit
                    conditions = tested_bit_conditions(sample, 4, conditions)
                    # source-effect driver:0f5f:jr
                    if not (bool(conditions & 0x40)):
                        # source-effect driver:0f61:ld
                        sample = u8(15)
                    # source-effect driver:0f63:or
                    observed_byte_47 = state.read(u16(channel_cursor + 1))
                    sample = u8(sample | observed_byte_47)
                    conditions = logic_conditions(sample, False)
                    # source-effect driver:0f66:add
                    arithmetic_result_48, conditions = sum_byte(sample, 16)
                    sample = u8(arithmetic_result_48)
                    # source-effect driver:0f68:bit
                    observed_byte_49 = state.read(u16(channel_cursor + 0))
                    conditions = state.memory_bit_conditions(observed_byte_49, 0, conditions, u16(channel_cursor + 0), True)
                    # source-effect driver:0f6c:jr
                    if not (conditions & 0x40):
                        # source-effect driver:0f72:add
                        arithmetic_result_50, conditions = sum_byte(sample, 32)
                        sample = u8(arithmetic_result_50)
                        # source-effect driver:0f74:ld
                        state.write(32529, u8(sample))
                        # source-effect driver:0f77:ret
                        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                        return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                    else:
                        # source-effect driver:0f6e:ld
                        state.write(32529, u8(sample))
                        # source-effect driver:0f71:ret
                        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                        return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
        else:
            # source-effect driver:0f0a:call
            from .business_notes import read_note_or_duration
            from .contexts import ReadNoteOrDurationInput
            stack_cursor = state.push_word(stack_cursor, 3853)
            updated_audio_values_51 = read_note_or_duration(state, ReadNoteOrDurationInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3853)))
            auxiliary_cursor = updated_audio_values_51.auxiliary_cursor
            channel_cursor = updated_audio_values_51.channel_cursor
            conditions = updated_audio_values_51.conditions
            count_and_data = updated_audio_values_51.count_and_data
            lookup_cursor = updated_audio_values_51.lookup_cursor
            parameter_cursor = updated_audio_values_51.parameter_cursor
            sample = updated_audio_values_51.sample
            stack_cursor = updated_audio_values_51.stack_cursor
            # source-effect driver:0f0d:bit
            observed_byte_52 = state.read(u16(channel_cursor + 0))
            conditions = state.memory_bit_conditions(observed_byte_52, 4, conditions, u16(channel_cursor + 0), True)
            # source-effect driver:0f11:ret
            if not (conditions & 0x40):
                stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
            # source-effect driver:0f12:call
            from .business_pitch import initialize_pitch_modulation
            from .contexts import InitializePitchModulationInput
            stack_cursor = state.push_word(stack_cursor, 3861)
            updated_audio_values_53 = initialize_pitch_modulation(state, InitializePitchModulationInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3861)))
            channel_cursor = updated_audio_values_53.channel_cursor
            conditions = updated_audio_values_53.conditions
            count_and_data = updated_audio_values_53.count_and_data
            lookup_cursor = updated_audio_values_53.lookup_cursor
            parameter_cursor = updated_audio_values_53.parameter_cursor
            sample = updated_audio_values_53.sample
            stack_cursor = updated_audio_values_53.stack_cursor
            # source-effect driver:0f15:jr
            pass  # Static control continuation is structured below.
            # source-effect driver:0f23:call
            from .business_pitch import calculate_channel_pitch
            from .contexts import CalculateChannelPitchInput
            stack_cursor = state.push_word(stack_cursor, 3878)
            updated_audio_values_54 = calculate_channel_pitch(state, CalculateChannelPitchInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3878)))
            channel_cursor = updated_audio_values_54.channel_cursor
            conditions = updated_audio_values_54.conditions
            count_and_data = updated_audio_values_54.count_and_data
            lookup_cursor = updated_audio_values_54.lookup_cursor
            parameter_cursor = updated_audio_values_54.parameter_cursor
            sample = updated_audio_values_54.sample
            stack_cursor = updated_audio_values_54.stack_cursor
            # source-effect driver:0f26:call
            from .business_pitch import update_pitch_modulation
            from .contexts import UpdatePitchModulationInput
            stack_cursor = state.push_word(stack_cursor, 3881)
            updated_audio_values_55 = update_pitch_modulation(state, UpdatePitchModulationInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3881)))
            auxiliary_cursor = updated_audio_values_55.auxiliary_cursor
            channel_cursor = updated_audio_values_55.channel_cursor
            conditions = updated_audio_values_55.conditions
            count_and_data = updated_audio_values_55.count_and_data
            lookup_cursor = updated_audio_values_55.lookup_cursor
            parameter_cursor = updated_audio_values_55.parameter_cursor
            sample = updated_audio_values_55.sample
            stack_cursor = updated_audio_values_55.stack_cursor
            # source-effect driver:0f29:bit
            observed_byte_56 = state.read(u16(channel_cursor + 0))
            conditions = state.memory_bit_conditions(observed_byte_56, 2, conditions, u16(channel_cursor + 0), True)
            # source-effect driver:0f2d:ret
            if not (conditions & 0x40):
                stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
            # source-effect driver:0f2e:ld
            observed_byte_57 = state.read(u16(channel_cursor + 1))
            count_and_data = replace_low(count_and_data, observed_byte_57)
            # source-effect driver:0f31:ld
            sample = u8(low(lookup_cursor))
            # source-effect driver:0f32:and
            sample = u8(sample & 15)
            conditions = logic_conditions(sample, True)
            # source-effect driver:0f34:or
            sample = u8(sample | low(count_and_data))
            conditions = logic_conditions(sample, False)
            # source-effect driver:0f35:ld
            state.write(32529, u8(sample))
            # source-effect driver:0f38:ld
            sample = u8(low(lookup_cursor))
            # source-effect driver:0f39:and
            sample = u8(sample & 240)
            conditions = logic_conditions(sample, True)
            # source-effect driver:0f3b:or
            sample = u8(sample | high(lookup_cursor))
            conditions = logic_conditions(sample, False)
            # source-effect driver:0f3c:rrca
            rotated_sample_58 = sample
            sample = u8((rotated_sample_58 >> 1) | (rotated_sample_58 << 7))
            conditions = (conditions & 0xC4) | (sample & 0x28) | (rotated_sample_58 & 1)
            # source-effect driver:0f3d:rrca
            rotated_sample_59 = sample
            sample = u8((rotated_sample_59 >> 1) | (rotated_sample_59 << 7))
            conditions = (conditions & 0xC4) | (sample & 0x28) | (rotated_sample_59 & 1)
            # source-effect driver:0f3e:rrca
            rotated_sample_60 = sample
            sample = u8((rotated_sample_60 >> 1) | (rotated_sample_60 << 7))
            conditions = (conditions & 0xC4) | (sample & 0x28) | (rotated_sample_60 & 1)
            # source-effect driver:0f3f:rrca
            rotated_sample_61 = sample
            sample = u8((rotated_sample_61 >> 1) | (rotated_sample_61 << 7))
            conditions = (conditions & 0xC4) | (sample & 0x28) | (rotated_sample_61 & 1)
            # source-effect driver:0f40:ld
            state.write(32529, u8(sample))
            # source-effect driver:0f43:ld
            observed_byte_62 = state.read(u16(channel_cursor + 8))
            sample = u8(observed_byte_62)
            # source-effect driver:0f46:or
            sample = u8(sample | sample)
            conditions = logic_conditions(sample, False)
            # source-effect driver:0f47:ld
            count_and_data = replace_low(count_and_data, 0)
            # source-effect driver:0f49:jr
            if not (bool(conditions & 0x40)):
                # source-effect driver:0f4b:dec
                changed_byte_63, conditions = decrement_byte(sample, conditions)
                sample = u8(changed_byte_63)
                # source-effect driver:0f4c:ld
                count_and_data = replace_low(count_and_data, 10)
                # source-effect driver:0f4e:rst
                from .business_hardware import lookup_banked_root_pointer
                from .contexts import LookupBankedRootPointerInput
                stack_cursor = state.push_word(stack_cursor, 3919)
                updated_audio_values_64 = lookup_banked_root_pointer(state, LookupBankedRootPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3919)))
                conditions = updated_audio_values_64.conditions
                count_and_data = updated_audio_values_64.count_and_data
                lookup_cursor = updated_audio_values_64.lookup_cursor
                sample = updated_audio_values_64.sample
                stack_cursor = updated_audio_values_64.stack_cursor
                # source-effect driver:0f4f:rst
                from .business_hardware import index_word_pointer
                from .contexts import IndexWordPointerInput
                stack_cursor = state.push_word(stack_cursor, 3920)
                updated_audio_values_65 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3920)))
                conditions = updated_audio_values_65.conditions
                count_and_data = updated_audio_values_65.count_and_data
                lookup_cursor = updated_audio_values_65.lookup_cursor
                sample = updated_audio_values_65.sample
                stack_cursor = updated_audio_values_65.stack_cursor
                # source-effect driver:0f50:call
                from .business_envelopes import evaluate_envelope_step
                from .contexts import EvaluateEnvelopeStepInput
                stack_cursor = state.push_word(stack_cursor, 3923)
                updated_audio_values_66 = evaluate_envelope_step(state, EvaluateEnvelopeStepInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 3923)))
                auxiliary_cursor = updated_audio_values_66.auxiliary_cursor
                channel_cursor = updated_audio_values_66.channel_cursor
                conditions = updated_audio_values_66.conditions
                count_and_data = updated_audio_values_66.count_and_data
                lookup_cursor = updated_audio_values_66.lookup_cursor
                parameter_cursor = updated_audio_values_66.parameter_cursor
                sample = updated_audio_values_66.sample
                stack_cursor = updated_audio_values_66.stack_cursor
                # source-effect driver:0f53:ld
                count_and_data = replace_low(count_and_data, sample)
            # source-effect driver:0f54:bit
            observed_byte_67 = state.read(u16(channel_cursor + 0))
            conditions = state.memory_bit_conditions(observed_byte_67, 4, conditions, u16(channel_cursor + 0), True)
            # source-effect driver:0f58:ret
            if not (conditions & 0x40):
                stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
            # source-effect driver:0f59:ld
            observed_byte_68 = state.read(u16(channel_cursor + 6))
            sample = u8(observed_byte_68)
            # source-effect driver:0f5c:add
            arithmetic_result_69, conditions = sum_byte(sample, low(count_and_data))
            sample = u8(arithmetic_result_69)
            # source-effect driver:0f5d:bit
            conditions = tested_bit_conditions(sample, 4, conditions)
            # source-effect driver:0f5f:jr
            if not (bool(conditions & 0x40)):
                # source-effect driver:0f61:ld
                sample = u8(15)
            # source-effect driver:0f63:or
            observed_byte_70 = state.read(u16(channel_cursor + 1))
            sample = u8(sample | observed_byte_70)
            conditions = logic_conditions(sample, False)
            # source-effect driver:0f66:add
            arithmetic_result_71, conditions = sum_byte(sample, 16)
            sample = u8(arithmetic_result_71)
            # source-effect driver:0f68:bit
            observed_byte_72 = state.read(u16(channel_cursor + 0))
            conditions = state.memory_bit_conditions(observed_byte_72, 0, conditions, u16(channel_cursor + 0), True)
            # source-effect driver:0f6c:jr
            if not (conditions & 0x40):
                # source-effect driver:0f72:add
                arithmetic_result_73, conditions = sum_byte(sample, 32)
                sample = u8(arithmetic_result_73)
                # source-effect driver:0f74:ld
                state.write(32529, u8(sample))
                # source-effect driver:0f77:ret
                stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
            else:
                # source-effect driver:0f6e:ld
                state.write(32529, u8(sample))
                # source-effect driver:0f71:ret
                stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    else:
        # source-effect driver:0140:call
        from .business_notes import decrement_note_countdown
        from .contexts import DecrementNoteCountdownInput
        stack_cursor = state.push_word(stack_cursor, 323)
        updated_audio_values_74 = decrement_note_countdown(state, DecrementNoteCountdownInput(channel_cursor=channel_cursor, conditions=conditions, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 323)))
        channel_cursor = updated_audio_values_74.channel_cursor
        conditions = updated_audio_values_74.conditions
        sample = updated_audio_values_74.sample
        stack_cursor = updated_audio_values_74.stack_cursor
        # source-effect driver:0143:jr
        if not (conditions & 0x40):
            # source-effect driver:015c:call
            from .business_pan import resume_pan_pattern
            from .contexts import ResumePanPatternInput
            stack_cursor = state.push_word(stack_cursor, 351)
            updated_audio_values_75 = resume_pan_pattern(state, ResumePanPatternInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 351)))
            channel_cursor = updated_audio_values_75.channel_cursor
            conditions = updated_audio_values_75.conditions
            count_and_data = updated_audio_values_75.count_and_data
            lookup_cursor = updated_audio_values_75.lookup_cursor
            parameter_cursor = updated_audio_values_75.parameter_cursor
            sample = updated_audio_values_75.sample
            stack_cursor = updated_audio_values_75.stack_cursor
            # source-effect driver:015f:bit
            observed_byte_76 = state.read(u16(channel_cursor + 0))
            conditions = state.memory_bit_conditions(observed_byte_76, 4, conditions, u16(channel_cursor + 0), True)
            # source-effect driver:0163:ret
            if not (conditions & 0x40):
                stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
            # source-effect driver:0164:call
            from .business_envelopes import update_voice_envelope
            from .contexts import UpdateVoiceEnvelopeInput
            stack_cursor = state.push_word(stack_cursor, 359)
            updated_audio_values_77 = update_voice_envelope(state, UpdateVoiceEnvelopeInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 359)))
            auxiliary_cursor = updated_audio_values_77.auxiliary_cursor
            channel_cursor = updated_audio_values_77.channel_cursor
            conditions = updated_audio_values_77.conditions
            count_and_data = updated_audio_values_77.count_and_data
            lookup_cursor = updated_audio_values_77.lookup_cursor
            parameter_cursor = updated_audio_values_77.parameter_cursor
            sample = updated_audio_values_77.sample
            stack_cursor = updated_audio_values_77.stack_cursor
            # source-effect driver:0167:ld
            observed_byte_78 = state.read(u16(channel_cursor + 30))
            sample = u8(observed_byte_78)
            # source-effect driver:016a:or
            sample = u8(sample | sample)
            conditions = logic_conditions(sample, False)
            # source-effect driver:016b:jr
            if bool(conditions & 0x40):
                # source-effect driver:0173:call
                from .business_pitch import calculate_channel_pitch
                from .contexts import CalculateChannelPitchInput
                stack_cursor = state.push_word(stack_cursor, 374)
                updated_audio_values_79 = calculate_channel_pitch(state, CalculateChannelPitchInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 374)))
                channel_cursor = updated_audio_values_79.channel_cursor
                conditions = updated_audio_values_79.conditions
                count_and_data = updated_audio_values_79.count_and_data
                lookup_cursor = updated_audio_values_79.lookup_cursor
                parameter_cursor = updated_audio_values_79.parameter_cursor
                sample = updated_audio_values_79.sample
                stack_cursor = updated_audio_values_79.stack_cursor
                # source-effect driver:0176:bit
                observed_byte_80 = state.read(u16(channel_cursor + 0))
                conditions = state.memory_bit_conditions(observed_byte_80, 6, conditions, u16(channel_cursor + 0), True)
                # source-effect driver:017a:ret
                if not (conditions & 0x40):
                    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                    return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                # source-effect driver:017b:call
                from .business_pitch import update_pitch_modulation
                from .contexts import UpdatePitchModulationInput
                stack_cursor = state.push_word(stack_cursor, 382)
                updated_audio_values_81 = update_pitch_modulation(state, UpdatePitchModulationInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 382)))
                auxiliary_cursor = updated_audio_values_81.auxiliary_cursor
                channel_cursor = updated_audio_values_81.channel_cursor
                conditions = updated_audio_values_81.conditions
                count_and_data = updated_audio_values_81.count_and_data
                lookup_cursor = updated_audio_values_81.lookup_cursor
                parameter_cursor = updated_audio_values_81.parameter_cursor
                sample = updated_audio_values_81.sample
                stack_cursor = updated_audio_values_81.stack_cursor
                # source-effect driver:017e:bit
                observed_byte_82 = state.read(u16(channel_cursor + 0))
                conditions = state.memory_bit_conditions(observed_byte_82, 2, conditions, u16(channel_cursor + 0), True)
                # source-effect driver:0182:ret
                if not (conditions & 0x40):
                    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                    return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                # source-effect driver:0183:bit
                observed_byte_83 = state.read(u16(channel_cursor + 0))
                conditions = state.memory_bit_conditions(observed_byte_83, 0, conditions, u16(channel_cursor + 0), True)
                # source-effect driver:0187:jp
                if not (conditions & 0x40):
                    # source-effect driver:0193:ld
                    observed_byte_84 = state.read(u16(channel_cursor + 1))
                    sample = u8(observed_byte_84)
                    # source-effect driver:0196:cp
                    conditions = comparison_conditions(sample, 2)
                    # source-effect driver:0198:jr
                    if not (conditions & 0x40):
                        # source-effect driver:018a:ld
                        sample = u8(164)
                        # source-effect driver:018c:ld
                        count_and_data = replace_low(count_and_data, high(lookup_cursor))
                        # source-effect driver:018d:rst
                        from .business_hardware import write_channel_fm_register
                        from .contexts import WriteChannelFmRegisterInput
                        stack_cursor = state.push_word(stack_cursor, 398)
                        updated_audio_values_85 = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 398)))
                        channel_cursor = updated_audio_values_85.channel_cursor
                        conditions = updated_audio_values_85.conditions
                        count_and_data = updated_audio_values_85.count_and_data
                        sample = updated_audio_values_85.sample
                        stack_cursor = updated_audio_values_85.stack_cursor
                        # source-effect driver:018e:ld
                        sample = u8(160)
                        # source-effect driver:0190:ld
                        count_and_data = replace_low(count_and_data, low(lookup_cursor))
                        # source-effect driver:0191:rst
                        from .business_hardware import write_channel_fm_register
                        from .contexts import WriteChannelFmRegisterInput
                        stack_cursor = state.push_word(stack_cursor, 402)
                        updated_audio_values_86 = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 402)))
                        channel_cursor = updated_audio_values_86.channel_cursor
                        conditions = updated_audio_values_86.conditions
                        count_and_data = updated_audio_values_86.count_and_data
                        sample = updated_audio_values_86.sample
                        stack_cursor = updated_audio_values_86.stack_cursor
                        # source-effect driver:0192:ret
                        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                        return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                    else:
                        # source-effect driver:019a:call
                        from .business_pitch import choose_frequency_scratch_block
                        from .contexts import ChooseFrequencyScratchBlockInput
                        stack_cursor = state.push_word(stack_cursor, 413)
                        updated_audio_values_87 = choose_frequency_scratch_block(state, ChooseFrequencyScratchBlockInput(conditions=conditions, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 413)))
                        conditions = updated_audio_values_87.conditions
                        parameter_cursor = updated_audio_values_87.parameter_cursor
                        sample = updated_audio_values_87.sample
                        stack_cursor = updated_audio_values_87.stack_cursor
                        # source-effect driver:019d:exx
                        alternate_group_88 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
                        alternate_group_88.validate()
                        count_and_data, parameter_cursor, lookup_cursor = alternate_group_88.count_and_data, alternate_group_88.parameter_cursor, alternate_group_88.lookup_cursor
                        # source-effect driver:019e:ld
                        lookup_cursor = u16(450)
                        # source-effect driver:01a1:ld
                        count_and_data = replace_high(count_and_data, 4)
                        while True:
                            # source-effect driver:01a3:ld
                            observed_byte_89 = state.read(lookup_cursor)
                            sample = u8(observed_byte_89)
                            # source-effect driver:01a4:push
                            stack_cursor = state.push_word(stack_cursor, ((sample << 8) | conditions))
                            # source-effect driver:01a5:inc
                            lookup_cursor = u16(lookup_cursor + 1)
                            # source-effect driver:01a6:exx
                            alternate_group_90 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
                            alternate_group_90.validate()
                            count_and_data, parameter_cursor, lookup_cursor = alternate_group_90.count_and_data, alternate_group_90.parameter_cursor, alternate_group_90.lookup_cursor
                            # source-effect driver:01a7:ex
                            parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
                            # source-effect driver:01a8:ld
                            observed_byte_91 = state.read(lookup_cursor)
                            count_and_data = replace_low(count_and_data, observed_byte_91)
                            # source-effect driver:01a9:inc
                            lookup_cursor = u16(lookup_cursor + 1)
                            # source-effect driver:01aa:ld
                            observed_byte_92 = state.read(lookup_cursor)
                            count_and_data = replace_high(count_and_data, observed_byte_92)
                            # source-effect driver:01ab:inc
                            lookup_cursor = u16(lookup_cursor + 1)
                            # source-effect driver:01ac:ex
                            parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
                            # source-effect driver:01ad:ld
                            observed_byte_93 = state.read(u16(channel_cursor + 13))
                            lookup_cursor = replace_low(lookup_cursor, observed_byte_93)
                            # source-effect driver:01b0:ld
                            observed_byte_94 = state.read(u16(channel_cursor + 14))
                            lookup_cursor = replace_high(lookup_cursor, observed_byte_94)
                            # source-effect driver:01b3:add
                            arithmetic_result_95, conditions = sum_word(lookup_cursor, count_and_data, conditions)
                            lookup_cursor = u16(arithmetic_result_95)
                            # source-effect driver:01b4:pop
                            saved_audio_word_96, stack_cursor = state.pop_word(stack_cursor)
                            sample, conditions = high(saved_audio_word_96), low(saved_audio_word_96)
                            # source-effect driver:01b5:push
                            stack_cursor = state.push_word(stack_cursor, ((sample << 8) | conditions))
                            # source-effect driver:01b6:ld
                            count_and_data = replace_low(count_and_data, high(lookup_cursor))
                            # source-effect driver:01b7:rst
                            from .business_hardware import write_fm_port_zero_entry
                            from .contexts import WriteFmPortZeroEntryInput
                            stack_cursor = state.push_word(stack_cursor, 440)
                            updated_audio_values_97 = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 440)))
                            channel_cursor = updated_audio_values_97.channel_cursor
                            conditions = updated_audio_values_97.conditions
                            count_and_data = updated_audio_values_97.count_and_data
                            sample = updated_audio_values_97.sample
                            stack_cursor = updated_audio_values_97.stack_cursor
                            # source-effect driver:01b8:pop
                            saved_audio_word_98, stack_cursor = state.pop_word(stack_cursor)
                            sample, conditions = high(saved_audio_word_98), low(saved_audio_word_98)
                            # source-effect driver:01b9:sub
                            sample, conditions = difference_byte(sample, 4)
                            # source-effect driver:01bb:ld
                            count_and_data = replace_low(count_and_data, low(lookup_cursor))
                            # source-effect driver:01bc:rst
                            from .business_hardware import write_fm_port_zero_entry
                            from .contexts import WriteFmPortZeroEntryInput
                            stack_cursor = state.push_word(stack_cursor, 445)
                            updated_audio_values_99 = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 445)))
                            channel_cursor = updated_audio_values_99.channel_cursor
                            conditions = updated_audio_values_99.conditions
                            count_and_data = updated_audio_values_99.count_and_data
                            sample = updated_audio_values_99.sample
                            stack_cursor = updated_audio_values_99.stack_cursor
                            # source-effect driver:01bd:exx
                            alternate_group_100 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
                            alternate_group_100.validate()
                            count_and_data, parameter_cursor, lookup_cursor = alternate_group_100.count_and_data, alternate_group_100.parameter_cursor, alternate_group_100.lookup_cursor
                            # source-effect driver:01be:djnz
                            count_and_data = replace_high(count_and_data, u8(high(count_and_data) - 1))
                            if high(count_and_data) != 0:
                                continue
                            break
                        # source-effect driver:01c0:exx
                        alternate_group_101 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
                        alternate_group_101.validate()
                        count_and_data, parameter_cursor, lookup_cursor = alternate_group_101.count_and_data, alternate_group_101.parameter_cursor, alternate_group_101.lookup_cursor
                        # source-effect driver:01c1:ret
                        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                        return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                else:
                    # source-effect driver:018a:ld
                    sample = u8(164)
                    # source-effect driver:018c:ld
                    count_and_data = replace_low(count_and_data, high(lookup_cursor))
                    # source-effect driver:018d:rst
                    from .business_hardware import write_channel_fm_register
                    from .contexts import WriteChannelFmRegisterInput
                    stack_cursor = state.push_word(stack_cursor, 398)
                    updated_audio_values_102 = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 398)))
                    channel_cursor = updated_audio_values_102.channel_cursor
                    conditions = updated_audio_values_102.conditions
                    count_and_data = updated_audio_values_102.count_and_data
                    sample = updated_audio_values_102.sample
                    stack_cursor = updated_audio_values_102.stack_cursor
                    # source-effect driver:018e:ld
                    sample = u8(160)
                    # source-effect driver:0190:ld
                    count_and_data = replace_low(count_and_data, low(lookup_cursor))
                    # source-effect driver:0191:rst
                    from .business_hardware import write_channel_fm_register
                    from .contexts import WriteChannelFmRegisterInput
                    stack_cursor = state.push_word(stack_cursor, 402)
                    updated_audio_values_103 = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 402)))
                    channel_cursor = updated_audio_values_103.channel_cursor
                    conditions = updated_audio_values_103.conditions
                    count_and_data = updated_audio_values_103.count_and_data
                    sample = updated_audio_values_103.sample
                    stack_cursor = updated_audio_values_103.stack_cursor
                    # source-effect driver:0192:ret
                    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                    return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
            else:
                # source-effect driver:016d:dec
                observed_byte_104 = state.read(u16(channel_cursor + 30))
                changed_byte_105, conditions = decrement_byte(observed_byte_104, conditions)
                state.write(u16(channel_cursor + 30), u8(changed_byte_105))
                # source-effect driver:0170:jp
                if bool(conditions & 0x40):
                    # source-effect driver:0428:ld
                    observed_byte_106 = state.read(u16(channel_cursor + 1))
                    count_and_data = replace_low(count_and_data, observed_byte_106)
                    # source-effect driver:042b:bit
                    conditions = tested_bit_conditions(low(count_and_data), 7, conditions)
                    # source-effect driver:042d:ret
                    if not (conditions & 0x40):
                        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                        return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                    # source-effect driver:042e:ld
                    sample = u8(40)
                    # source-effect driver:0430:rst
                    from .business_hardware import write_fm_port_zero_entry
                    from .contexts import WriteFmPortZeroEntryInput
                    stack_cursor = state.push_word(stack_cursor, 1073)
                    updated_audio_values_107 = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 1073)))
                    channel_cursor = updated_audio_values_107.channel_cursor
                    conditions = updated_audio_values_107.conditions
                    count_and_data = updated_audio_values_107.count_and_data
                    sample = updated_audio_values_107.sample
                    stack_cursor = updated_audio_values_107.stack_cursor
                    # source-effect driver:0431:ret
                    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                    return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                else:
                    # source-effect driver:0173:call
                    from .business_pitch import calculate_channel_pitch
                    from .contexts import CalculateChannelPitchInput
                    stack_cursor = state.push_word(stack_cursor, 374)
                    updated_audio_values_108 = calculate_channel_pitch(state, CalculateChannelPitchInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 374)))
                    channel_cursor = updated_audio_values_108.channel_cursor
                    conditions = updated_audio_values_108.conditions
                    count_and_data = updated_audio_values_108.count_and_data
                    lookup_cursor = updated_audio_values_108.lookup_cursor
                    parameter_cursor = updated_audio_values_108.parameter_cursor
                    sample = updated_audio_values_108.sample
                    stack_cursor = updated_audio_values_108.stack_cursor
                    # source-effect driver:0176:bit
                    observed_byte_109 = state.read(u16(channel_cursor + 0))
                    conditions = state.memory_bit_conditions(observed_byte_109, 6, conditions, u16(channel_cursor + 0), True)
                    # source-effect driver:017a:ret
                    if not (conditions & 0x40):
                        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                        return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                    # source-effect driver:017b:call
                    from .business_pitch import update_pitch_modulation
                    from .contexts import UpdatePitchModulationInput
                    stack_cursor = state.push_word(stack_cursor, 382)
                    updated_audio_values_110 = update_pitch_modulation(state, UpdatePitchModulationInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 382)))
                    auxiliary_cursor = updated_audio_values_110.auxiliary_cursor
                    channel_cursor = updated_audio_values_110.channel_cursor
                    conditions = updated_audio_values_110.conditions
                    count_and_data = updated_audio_values_110.count_and_data
                    lookup_cursor = updated_audio_values_110.lookup_cursor
                    parameter_cursor = updated_audio_values_110.parameter_cursor
                    sample = updated_audio_values_110.sample
                    stack_cursor = updated_audio_values_110.stack_cursor
                    # source-effect driver:017e:bit
                    observed_byte_111 = state.read(u16(channel_cursor + 0))
                    conditions = state.memory_bit_conditions(observed_byte_111, 2, conditions, u16(channel_cursor + 0), True)
                    # source-effect driver:0182:ret
                    if not (conditions & 0x40):
                        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                        return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                    # source-effect driver:0183:bit
                    observed_byte_112 = state.read(u16(channel_cursor + 0))
                    conditions = state.memory_bit_conditions(observed_byte_112, 0, conditions, u16(channel_cursor + 0), True)
                    # source-effect driver:0187:jp
                    if not (conditions & 0x40):
                        # source-effect driver:0193:ld
                        observed_byte_113 = state.read(u16(channel_cursor + 1))
                        sample = u8(observed_byte_113)
                        # source-effect driver:0196:cp
                        conditions = comparison_conditions(sample, 2)
                        # source-effect driver:0198:jr
                        if not (conditions & 0x40):
                            # source-effect driver:018a:ld
                            sample = u8(164)
                            # source-effect driver:018c:ld
                            count_and_data = replace_low(count_and_data, high(lookup_cursor))
                            # source-effect driver:018d:rst
                            from .business_hardware import write_channel_fm_register
                            from .contexts import WriteChannelFmRegisterInput
                            stack_cursor = state.push_word(stack_cursor, 398)
                            updated_audio_values_114 = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 398)))
                            channel_cursor = updated_audio_values_114.channel_cursor
                            conditions = updated_audio_values_114.conditions
                            count_and_data = updated_audio_values_114.count_and_data
                            sample = updated_audio_values_114.sample
                            stack_cursor = updated_audio_values_114.stack_cursor
                            # source-effect driver:018e:ld
                            sample = u8(160)
                            # source-effect driver:0190:ld
                            count_and_data = replace_low(count_and_data, low(lookup_cursor))
                            # source-effect driver:0191:rst
                            from .business_hardware import write_channel_fm_register
                            from .contexts import WriteChannelFmRegisterInput
                            stack_cursor = state.push_word(stack_cursor, 402)
                            updated_audio_values_115 = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 402)))
                            channel_cursor = updated_audio_values_115.channel_cursor
                            conditions = updated_audio_values_115.conditions
                            count_and_data = updated_audio_values_115.count_and_data
                            sample = updated_audio_values_115.sample
                            stack_cursor = updated_audio_values_115.stack_cursor
                            # source-effect driver:0192:ret
                            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                            return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                        else:
                            # source-effect driver:019a:call
                            from .business_pitch import choose_frequency_scratch_block
                            from .contexts import ChooseFrequencyScratchBlockInput
                            stack_cursor = state.push_word(stack_cursor, 413)
                            updated_audio_values_116 = choose_frequency_scratch_block(state, ChooseFrequencyScratchBlockInput(conditions=conditions, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 413)))
                            conditions = updated_audio_values_116.conditions
                            parameter_cursor = updated_audio_values_116.parameter_cursor
                            sample = updated_audio_values_116.sample
                            stack_cursor = updated_audio_values_116.stack_cursor
                            # source-effect driver:019d:exx
                            alternate_group_117 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
                            alternate_group_117.validate()
                            count_and_data, parameter_cursor, lookup_cursor = alternate_group_117.count_and_data, alternate_group_117.parameter_cursor, alternate_group_117.lookup_cursor
                            # source-effect driver:019e:ld
                            lookup_cursor = u16(450)
                            # source-effect driver:01a1:ld
                            count_and_data = replace_high(count_and_data, 4)
                            while True:
                                # source-effect driver:01a3:ld
                                observed_byte_118 = state.read(lookup_cursor)
                                sample = u8(observed_byte_118)
                                # source-effect driver:01a4:push
                                stack_cursor = state.push_word(stack_cursor, ((sample << 8) | conditions))
                                # source-effect driver:01a5:inc
                                lookup_cursor = u16(lookup_cursor + 1)
                                # source-effect driver:01a6:exx
                                alternate_group_119 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
                                alternate_group_119.validate()
                                count_and_data, parameter_cursor, lookup_cursor = alternate_group_119.count_and_data, alternate_group_119.parameter_cursor, alternate_group_119.lookup_cursor
                                # source-effect driver:01a7:ex
                                parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
                                # source-effect driver:01a8:ld
                                observed_byte_120 = state.read(lookup_cursor)
                                count_and_data = replace_low(count_and_data, observed_byte_120)
                                # source-effect driver:01a9:inc
                                lookup_cursor = u16(lookup_cursor + 1)
                                # source-effect driver:01aa:ld
                                observed_byte_121 = state.read(lookup_cursor)
                                count_and_data = replace_high(count_and_data, observed_byte_121)
                                # source-effect driver:01ab:inc
                                lookup_cursor = u16(lookup_cursor + 1)
                                # source-effect driver:01ac:ex
                                parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
                                # source-effect driver:01ad:ld
                                observed_byte_122 = state.read(u16(channel_cursor + 13))
                                lookup_cursor = replace_low(lookup_cursor, observed_byte_122)
                                # source-effect driver:01b0:ld
                                observed_byte_123 = state.read(u16(channel_cursor + 14))
                                lookup_cursor = replace_high(lookup_cursor, observed_byte_123)
                                # source-effect driver:01b3:add
                                arithmetic_result_124, conditions = sum_word(lookup_cursor, count_and_data, conditions)
                                lookup_cursor = u16(arithmetic_result_124)
                                # source-effect driver:01b4:pop
                                saved_audio_word_125, stack_cursor = state.pop_word(stack_cursor)
                                sample, conditions = high(saved_audio_word_125), low(saved_audio_word_125)
                                # source-effect driver:01b5:push
                                stack_cursor = state.push_word(stack_cursor, ((sample << 8) | conditions))
                                # source-effect driver:01b6:ld
                                count_and_data = replace_low(count_and_data, high(lookup_cursor))
                                # source-effect driver:01b7:rst
                                from .business_hardware import write_fm_port_zero_entry
                                from .contexts import WriteFmPortZeroEntryInput
                                stack_cursor = state.push_word(stack_cursor, 440)
                                updated_audio_values_126 = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 440)))
                                channel_cursor = updated_audio_values_126.channel_cursor
                                conditions = updated_audio_values_126.conditions
                                count_and_data = updated_audio_values_126.count_and_data
                                sample = updated_audio_values_126.sample
                                stack_cursor = updated_audio_values_126.stack_cursor
                                # source-effect driver:01b8:pop
                                saved_audio_word_127, stack_cursor = state.pop_word(stack_cursor)
                                sample, conditions = high(saved_audio_word_127), low(saved_audio_word_127)
                                # source-effect driver:01b9:sub
                                sample, conditions = difference_byte(sample, 4)
                                # source-effect driver:01bb:ld
                                count_and_data = replace_low(count_and_data, low(lookup_cursor))
                                # source-effect driver:01bc:rst
                                from .business_hardware import write_fm_port_zero_entry
                                from .contexts import WriteFmPortZeroEntryInput
                                stack_cursor = state.push_word(stack_cursor, 445)
                                updated_audio_values_128 = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 445)))
                                channel_cursor = updated_audio_values_128.channel_cursor
                                conditions = updated_audio_values_128.conditions
                                count_and_data = updated_audio_values_128.count_and_data
                                sample = updated_audio_values_128.sample
                                stack_cursor = updated_audio_values_128.stack_cursor
                                # source-effect driver:01bd:exx
                                alternate_group_129 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
                                alternate_group_129.validate()
                                count_and_data, parameter_cursor, lookup_cursor = alternate_group_129.count_and_data, alternate_group_129.parameter_cursor, alternate_group_129.lookup_cursor
                                # source-effect driver:01be:djnz
                                count_and_data = replace_high(count_and_data, u8(high(count_and_data) - 1))
                                if high(count_and_data) != 0:
                                    continue
                                break
                            # source-effect driver:01c0:exx
                            alternate_group_130 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
                            alternate_group_130.validate()
                            count_and_data, parameter_cursor, lookup_cursor = alternate_group_130.count_and_data, alternate_group_130.parameter_cursor, alternate_group_130.lookup_cursor
                            # source-effect driver:01c1:ret
                            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                            return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                    else:
                        # source-effect driver:018a:ld
                        sample = u8(164)
                        # source-effect driver:018c:ld
                        count_and_data = replace_low(count_and_data, high(lookup_cursor))
                        # source-effect driver:018d:rst
                        from .business_hardware import write_channel_fm_register
                        from .contexts import WriteChannelFmRegisterInput
                        stack_cursor = state.push_word(stack_cursor, 398)
                        updated_audio_values_131 = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 398)))
                        channel_cursor = updated_audio_values_131.channel_cursor
                        conditions = updated_audio_values_131.conditions
                        count_and_data = updated_audio_values_131.count_and_data
                        sample = updated_audio_values_131.sample
                        stack_cursor = updated_audio_values_131.stack_cursor
                        # source-effect driver:018e:ld
                        sample = u8(160)
                        # source-effect driver:0190:ld
                        count_and_data = replace_low(count_and_data, low(lookup_cursor))
                        # source-effect driver:0191:rst
                        from .business_hardware import write_channel_fm_register
                        from .contexts import WriteChannelFmRegisterInput
                        stack_cursor = state.push_word(stack_cursor, 402)
                        updated_audio_values_132 = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 402)))
                        channel_cursor = updated_audio_values_132.channel_cursor
                        conditions = updated_audio_values_132.conditions
                        count_and_data = updated_audio_values_132.count_and_data
                        sample = updated_audio_values_132.sample
                        stack_cursor = updated_audio_values_132.stack_cursor
                        # source-effect driver:0192:ret
                        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                        return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
        else:
            # source-effect driver:0145:call
            from .business_notes import read_note_or_duration
            from .contexts import ReadNoteOrDurationInput
            stack_cursor = state.push_word(stack_cursor, 328)
            updated_audio_values_133 = read_note_or_duration(state, ReadNoteOrDurationInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 328)))
            auxiliary_cursor = updated_audio_values_133.auxiliary_cursor
            channel_cursor = updated_audio_values_133.channel_cursor
            conditions = updated_audio_values_133.conditions
            count_and_data = updated_audio_values_133.count_and_data
            lookup_cursor = updated_audio_values_133.lookup_cursor
            parameter_cursor = updated_audio_values_133.parameter_cursor
            sample = updated_audio_values_133.sample
            stack_cursor = updated_audio_values_133.stack_cursor
            # source-effect driver:0148:bit
            observed_byte_134 = state.read(u16(channel_cursor + 0))
            conditions = state.memory_bit_conditions(observed_byte_134, 4, conditions, u16(channel_cursor + 0), True)
            # source-effect driver:014c:ret
            if not (conditions & 0x40):
                stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
            # source-effect driver:014d:call
            from .business_pitch import initialize_pitch_modulation
            from .contexts import InitializePitchModulationInput
            stack_cursor = state.push_word(stack_cursor, 336)
            updated_audio_values_135 = initialize_pitch_modulation(state, InitializePitchModulationInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 336)))
            channel_cursor = updated_audio_values_135.channel_cursor
            conditions = updated_audio_values_135.conditions
            count_and_data = updated_audio_values_135.count_and_data
            lookup_cursor = updated_audio_values_135.lookup_cursor
            parameter_cursor = updated_audio_values_135.parameter_cursor
            sample = updated_audio_values_135.sample
            stack_cursor = updated_audio_values_135.stack_cursor
            # source-effect driver:0150:call
            from .business_pitch import calculate_channel_pitch
            from .contexts import CalculateChannelPitchInput
            stack_cursor = state.push_word(stack_cursor, 339)
            updated_audio_values_136 = calculate_channel_pitch(state, CalculateChannelPitchInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 339)))
            channel_cursor = updated_audio_values_136.channel_cursor
            conditions = updated_audio_values_136.conditions
            count_and_data = updated_audio_values_136.count_and_data
            lookup_cursor = updated_audio_values_136.lookup_cursor
            parameter_cursor = updated_audio_values_136.parameter_cursor
            sample = updated_audio_values_136.sample
            stack_cursor = updated_audio_values_136.stack_cursor
            # source-effect driver:0153:call
            from .business_pitch import update_pitch_modulation
            from .contexts import UpdatePitchModulationInput
            stack_cursor = state.push_word(stack_cursor, 342)
            updated_audio_values_137 = update_pitch_modulation(state, UpdatePitchModulationInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 342)))
            auxiliary_cursor = updated_audio_values_137.auxiliary_cursor
            channel_cursor = updated_audio_values_137.channel_cursor
            conditions = updated_audio_values_137.conditions
            count_and_data = updated_audio_values_137.count_and_data
            lookup_cursor = updated_audio_values_137.lookup_cursor
            parameter_cursor = updated_audio_values_137.parameter_cursor
            sample = updated_audio_values_137.sample
            stack_cursor = updated_audio_values_137.stack_cursor
            # source-effect driver:0156:call
            from .business_pitch import write_channel_frequency
            from .contexts import WriteChannelFrequencyInput
            stack_cursor = state.push_word(stack_cursor, 345)
            updated_audio_values_138 = write_channel_frequency(state, WriteChannelFrequencyInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 345)))
            auxiliary_cursor = updated_audio_values_138.auxiliary_cursor
            channel_cursor = updated_audio_values_138.channel_cursor
            conditions = updated_audio_values_138.conditions
            count_and_data = updated_audio_values_138.count_and_data
            lookup_cursor = updated_audio_values_138.lookup_cursor
            parameter_cursor = updated_audio_values_138.parameter_cursor
            sample = updated_audio_values_138.sample
            stack_cursor = updated_audio_values_138.stack_cursor
            # source-effect driver:0159:jp
            pass  # Static control continuation is structured below.
            # source-effect driver:040b:ld
            observed_byte_139 = state.read(u16(channel_cursor + 13))
            sample = u8(observed_byte_139)
            # source-effect driver:040e:or
            observed_byte_140 = state.read(u16(channel_cursor + 14))
            sample = u8(sample | observed_byte_140)
            conditions = logic_conditions(sample, False)
            # source-effect driver:0411:ret
            if bool(conditions & 0x40):
                stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
            # source-effect driver:0412:ld
            observed_byte_141 = state.read(u16(channel_cursor + 0))
            sample = u8(observed_byte_141)
            # source-effect driver:0415:and
            sample = u8(sample & 6)
            conditions = logic_conditions(sample, True)
            # source-effect driver:0417:ret
            if not (conditions & 0x40):
                stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
            # source-effect driver:0418:ld
            observed_byte_142 = state.read(u16(channel_cursor + 1))
            sample = u8(observed_byte_142)
            # source-effect driver:041b:or
            sample = u8(sample | 240)
            conditions = logic_conditions(sample, False)
            # source-effect driver:041d:ld
            count_and_data = replace_low(count_and_data, sample)
            # source-effect driver:041e:ld
            sample = u8(40)
            # source-effect driver:0420:rst
            from .business_hardware import write_fm_port_zero_entry
            from .contexts import WriteFmPortZeroEntryInput
            stack_cursor = state.push_word(stack_cursor, 1057)
            updated_audio_values_143 = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 1057)))
            channel_cursor = updated_audio_values_143.channel_cursor
            conditions = updated_audio_values_143.conditions
            count_and_data = updated_audio_values_143.count_and_data
            sample = updated_audio_values_143.sample
            stack_cursor = updated_audio_values_143.stack_cursor
            # source-effect driver:0421:ret
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return UpdateFmChannelResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
