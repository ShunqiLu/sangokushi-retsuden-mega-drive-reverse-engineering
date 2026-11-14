"""Note and rhythm parameter streams, durations and live countdowns.

Intermediate recovered algorithms; no CPU/timing or natural playback proof.
Live bus/stack aliases and original nonlocal returns remain unchanged.
"""
from .domain import (AudioState, Continuation, word, checked_state, u8, u16, low, high, replace_low, replace_high, logic_conditions, sum_byte, difference_byte, comparison_conditions, decrement_byte, sum_word, copy_byte_conditions)
from .contexts import (ReadNoteOrDurationInput, ReadNoteOrDurationResult, MultiplyNoteDurationInput, MultiplyNoteDurationResult, DecrementNoteCountdownInput, DecrementNoteCountdownResult, ReadRhythmNoteInput, ReadRhythmNoteResult, ResumeRhythmParameterStreamInput, ResumeRhythmParameterStreamResult, ResumeNoteParameterStreamInput, ResumeNoteParameterStreamResult)

def read_note_or_duration(state: AudioState, inputs: ReadNoteOrDurationInput) -> ReadNoteOrDurationResult:
    """Read note or duration."""
    checked_state(state)
    if type(inputs) is not ReadNoteOrDurationInput:
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
    # source-effect driver:01d6:ld
    observed_byte_1 = state.read(u16(channel_cursor + 3))
    parameter_cursor = replace_low(parameter_cursor, observed_byte_1)
    # source-effect driver:01d9:ld
    observed_byte_2 = state.read(u16(channel_cursor + 4))
    parameter_cursor = replace_high(parameter_cursor, observed_byte_2)
    # source-effect driver:01dc:res
    observed_byte_3 = state.read(u16(channel_cursor + 0))
    state.write(u16(channel_cursor + 0), u8(observed_byte_3 & 253))
    # source-effect driver:01e0:res
    observed_byte_4 = state.read(u16(channel_cursor + 0))
    state.write(u16(channel_cursor + 0), u8(observed_byte_4 & 239))
    # source-effect driver:01e4:ld
    observed_byte_5 = state.read(parameter_cursor)
    sample = u8(observed_byte_5)
    # source-effect driver:01e5:inc
    parameter_cursor = u16(parameter_cursor + 1)
    # source-effect driver:01e6:cp
    conditions = comparison_conditions(sample, 224)
    # source-effect driver:01e8:jp
    if not (conditions & 1):
        # source-effect driver:0b78:ld
        lookup_cursor = u16(2948)
        # source-effect driver:0b7b:push
        stack_cursor = state.push_word(stack_cursor, lookup_cursor)
        # source-effect driver:0b7c:sub
        sample, conditions = difference_byte(sample, 224)
        # source-effect driver:0b7e:ld
        lookup_cursor = u16(2959)
        # source-effect driver:0b81:rst
        from .business_hardware import index_word_pointer
        from .contexts import IndexWordPointerInput
        stack_cursor = state.push_word(stack_cursor, 2946)
        updated_audio_values_6 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2946)))
        conditions = updated_audio_values_6.conditions
        count_and_data = updated_audio_values_6.count_and_data
        lookup_cursor = updated_audio_values_6.lookup_cursor
        sample = updated_audio_values_6.sample
        stack_cursor = updated_audio_values_6.stack_cursor
        # source-effect driver:0b82:ld
        observed_byte_7 = state.read(parameter_cursor)
        sample = u8(observed_byte_7)
        # source-effect driver:0b83:jp
        current_transfer_values_8 = ReadNoteOrDurationInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=inputs.continuation).validate(state)
        state.indirect_transfer("driver", lookup_cursor, current_transfer_values_8)
    else:
        # source-effect driver:01eb:ex
        alternate_sample_and_conditions_9 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
        sample, conditions = high(alternate_sample_and_conditions_9), low(alternate_sample_and_conditions_9)
        # source-effect driver:01ec:call
        from .business_envelopes import send_key_off
        from .contexts import SendKeyOffInput
        stack_cursor = state.push_word(stack_cursor, 495)
        updated_audio_values_10 = send_key_off(state, SendKeyOffInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 495)))
        auxiliary_cursor = updated_audio_values_10.auxiliary_cursor
        channel_cursor = updated_audio_values_10.channel_cursor
        conditions = updated_audio_values_10.conditions
        count_and_data = updated_audio_values_10.count_and_data
        lookup_cursor = updated_audio_values_10.lookup_cursor
        parameter_cursor = updated_audio_values_10.parameter_cursor
        sample = updated_audio_values_10.sample
        stack_cursor = updated_audio_values_10.stack_cursor
        # source-effect driver:01ef:call
        from .business_pan import update_pan_pattern
        from .contexts import UpdatePanPatternInput
        stack_cursor = state.push_word(stack_cursor, 498)
        updated_audio_values_11 = update_pan_pattern(state, UpdatePanPatternInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 498)))
        channel_cursor = updated_audio_values_11.channel_cursor
        conditions = updated_audio_values_11.conditions
        count_and_data = updated_audio_values_11.count_and_data
        lookup_cursor = updated_audio_values_11.lookup_cursor
        parameter_cursor = updated_audio_values_11.parameter_cursor
        sample = updated_audio_values_11.sample
        stack_cursor = updated_audio_values_11.stack_cursor
        # source-effect driver:01f2:ex
        alternate_sample_and_conditions_12 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
        sample, conditions = high(alternate_sample_and_conditions_12), low(alternate_sample_and_conditions_12)
        # source-effect driver:01f3:bit
        observed_byte_13 = state.read(u16(channel_cursor + 0))
        conditions = state.memory_bit_conditions(observed_byte_13, 3, conditions, u16(channel_cursor + 0), True)
        # source-effect driver:01f7:jp
        if not (conditions & 0x40):
            # source-effect driver:0250:ld
            lookup_cursor = replace_high(lookup_cursor, sample)
            # source-effect driver:0251:ld
            observed_byte_14 = state.read(parameter_cursor)
            sample = u8(observed_byte_14)
            # source-effect driver:0252:inc
            parameter_cursor = u16(parameter_cursor + 1)
            # source-effect driver:0253:ld
            lookup_cursor = replace_low(lookup_cursor, sample)
            # source-effect driver:0254:or
            sample = u8(sample | high(lookup_cursor))
            conditions = logic_conditions(sample, False)
            # source-effect driver:0255:jr
            if not (bool(conditions & 0x40)):
                # source-effect driver:0257:ld
                observed_byte_15 = state.read(u16(channel_cursor + 5))
                sample = u8(observed_byte_15)
                # source-effect driver:025a:ld
                count_and_data = replace_high(count_and_data, 0)
                # source-effect driver:025c:or
                sample = u8(sample | sample)
                conditions = logic_conditions(sample, False)
                # source-effect driver:025d:jp
                if not (not (conditions & 0x80)):
                    # source-effect driver:0260:dec
                    changed_byte_16, conditions = decrement_byte(high(count_and_data), conditions)
                    count_and_data = replace_high(count_and_data, changed_byte_16)
                # source-effect driver:0261:ld
                count_and_data = replace_low(count_and_data, sample)
                # source-effect driver:0262:add
                arithmetic_result_17, conditions = sum_word(lookup_cursor, count_and_data, conditions)
                lookup_cursor = u16(arithmetic_result_17)
            # source-effect driver:0263:ld
            state.write(u16(channel_cursor + 13), u8(low(lookup_cursor)))
            # source-effect driver:0266:ld
            state.write(u16(channel_cursor + 14), u8(high(lookup_cursor)))
            # source-effect driver:0269:bit
            observed_byte_18 = state.read(u16(channel_cursor + 0))
            conditions = state.memory_bit_conditions(observed_byte_18, 5, conditions, u16(channel_cursor + 0), True)
            # source-effect driver:026d:jr
            if not (bool(conditions & 0x40)):
                # source-effect driver:026f:ld
                observed_byte_19 = state.read(parameter_cursor)
                sample = u8(observed_byte_19)
                # source-effect driver:0270:inc
                parameter_cursor = u16(parameter_cursor + 1)
                # source-effect driver:0271:ld
                state.write(u16(channel_cursor + 16), u8(sample))
            # source-effect driver:0274:ld
            observed_byte_20 = state.read(parameter_cursor)
            sample = u8(observed_byte_20)
            # source-effect driver:0275:inc
            parameter_cursor = u16(parameter_cursor + 1)
            # source-effect driver:0276:call
            from .business_notes import multiply_note_duration
            from .contexts import MultiplyNoteDurationInput
            stack_cursor = state.push_word(stack_cursor, 633)
            updated_audio_values_21 = multiply_note_duration(state, MultiplyNoteDurationInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 633)))
            channel_cursor = updated_audio_values_21.channel_cursor
            conditions = updated_audio_values_21.conditions
            count_and_data = updated_audio_values_21.count_and_data
            sample = updated_audio_values_21.sample
            stack_cursor = updated_audio_values_21.stack_cursor
            # source-effect driver:0279:ld
            state.write(u16(channel_cursor + 12), u8(sample))
        else:
            # source-effect driver:01fa:or
            sample = u8(sample | sample)
            conditions = logic_conditions(sample, False)
            # source-effect driver:01fb:jp
            if not (conditions & 0x80):
                # source-effect driver:0276:call
                from .business_notes import multiply_note_duration
                from .contexts import MultiplyNoteDurationInput
                stack_cursor = state.push_word(stack_cursor, 633)
                updated_audio_values_22 = multiply_note_duration(state, MultiplyNoteDurationInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 633)))
                channel_cursor = updated_audio_values_22.channel_cursor
                conditions = updated_audio_values_22.conditions
                count_and_data = updated_audio_values_22.count_and_data
                sample = updated_audio_values_22.sample
                stack_cursor = updated_audio_values_22.stack_cursor
                # source-effect driver:0279:ld
                state.write(u16(channel_cursor + 12), u8(sample))
            else:
                # source-effect driver:01fe:sub
                sample, conditions = difference_byte(sample, 129)
                # source-effect driver:0200:jp
                if not (conditions & 0x80):
                    # source-effect driver:0208:add
                    observed_byte_23 = state.read(u16(channel_cursor + 5))
                    arithmetic_result_24, conditions = sum_byte(sample, observed_byte_23)
                    sample = u8(arithmetic_result_24)
                    # source-effect driver:020b:ld
                    lookup_cursor = u16(2278)
                    # source-effect driver:020e:push
                    stack_cursor = state.push_word(stack_cursor, ((sample << 8) | conditions))
                    # source-effect driver:020f:rst
                    from .business_hardware import index_word_pointer
                    from .contexts import IndexWordPointerInput
                    stack_cursor = state.push_word(stack_cursor, 528)
                    updated_audio_values_25 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 528)))
                    conditions = updated_audio_values_25.conditions
                    count_and_data = updated_audio_values_25.count_and_data
                    lookup_cursor = updated_audio_values_25.lookup_cursor
                    sample = updated_audio_values_25.sample
                    stack_cursor = updated_audio_values_25.stack_cursor
                    # source-effect driver:0210:pop
                    saved_audio_word_26, stack_cursor = state.pop_word(stack_cursor)
                    sample, conditions = high(saved_audio_word_26), low(saved_audio_word_26)
                    # source-effect driver:0211:bit
                    observed_byte_27 = state.read(u16(channel_cursor + 1))
                    conditions = state.memory_bit_conditions(observed_byte_27, 7, conditions, u16(channel_cursor + 1), True)
                    # source-effect driver:0215:jr
                    if not (not (conditions & 0x40)):
                        # source-effect driver:0217:push
                        stack_cursor = state.push_word(stack_cursor, parameter_cursor)
                        # source-effect driver:0218:ld
                        parameter_cursor = replace_high(parameter_cursor, 8)
                        # source-effect driver:021a:ld
                        parameter_cursor = replace_low(parameter_cursor, 12)
                        # source-effect driver:021c:ex
                        alternate_sample_and_conditions_28 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
                        sample, conditions = high(alternate_sample_and_conditions_28), low(alternate_sample_and_conditions_28)
                        # source-effect driver:021d:xor
                        sample = u8(sample ^ sample)
                        conditions = logic_conditions(sample, False)
                        while True:
                            # source-effect driver:021e:ex
                            alternate_sample_and_conditions_29 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
                            sample, conditions = high(alternate_sample_and_conditions_29), low(alternate_sample_and_conditions_29)
                            # source-effect driver:021f:sub
                            sample, conditions = difference_byte(sample, low(parameter_cursor))
                            # source-effect driver:0220:jr
                            if bool(conditions & 1):
                                break
                            # source-effect driver:0222:ex
                            alternate_sample_and_conditions_30 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
                            sample, conditions = high(alternate_sample_and_conditions_30), low(alternate_sample_and_conditions_30)
                            # source-effect driver:0223:add
                            arithmetic_result_31, conditions = sum_byte(sample, high(parameter_cursor))
                            sample = u8(arithmetic_result_31)
                            # source-effect driver:0224:jr
                            pass  # Static control continuation is structured below.
                            continue
                        # source-effect driver:0227:add
                        arithmetic_result_32, conditions = sum_byte(sample, low(parameter_cursor))
                        sample = u8(arithmetic_result_32)
                        # source-effect driver:0228:ld
                        lookup_cursor = u16(2416)
                        # source-effect driver:022b:rst
                        from .business_hardware import index_word_pointer
                        from .contexts import IndexWordPointerInput
                        stack_cursor = state.push_word(stack_cursor, 556)
                        updated_audio_values_33 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 556)))
                        conditions = updated_audio_values_33.conditions
                        count_and_data = updated_audio_values_33.count_and_data
                        lookup_cursor = updated_audio_values_33.lookup_cursor
                        sample = updated_audio_values_33.sample
                        stack_cursor = updated_audio_values_33.stack_cursor
                        # source-effect driver:022c:ex
                        alternate_sample_and_conditions_34 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
                        sample, conditions = high(alternate_sample_and_conditions_34), low(alternate_sample_and_conditions_34)
                        # source-effect driver:022d:or
                        sample = u8(sample | high(lookup_cursor))
                        conditions = logic_conditions(sample, False)
                        # source-effect driver:022e:ld
                        lookup_cursor = replace_high(lookup_cursor, sample)
                        # source-effect driver:022f:pop
                        saved_audio_word_35, stack_cursor = state.pop_word(stack_cursor)
                        parameter_cursor = u16(saved_audio_word_35)
                    # source-effect driver:0230:ld
                    state.write(u16(channel_cursor + 13), u8(low(lookup_cursor)))
                    # source-effect driver:0233:ld
                    state.write(u16(channel_cursor + 14), u8(high(lookup_cursor)))
                else:
                    # source-effect driver:0203:call
                    from .business_envelopes import stop_channel_note
                    from .contexts import StopChannelNoteInput
                    stack_cursor = state.push_word(stack_cursor, 518)
                    updated_audio_values_36 = stop_channel_note(state, StopChannelNoteInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 518)))
                    auxiliary_cursor = updated_audio_values_36.auxiliary_cursor
                    channel_cursor = updated_audio_values_36.channel_cursor
                    conditions = updated_audio_values_36.conditions
                    count_and_data = updated_audio_values_36.count_and_data
                    lookup_cursor = updated_audio_values_36.lookup_cursor
                    parameter_cursor = updated_audio_values_36.parameter_cursor
                    sample = updated_audio_values_36.sample
                    stack_cursor = updated_audio_values_36.stack_cursor
                    # source-effect driver:0206:jr
                    pass  # Static control continuation is structured below.
                # source-effect driver:0236:bit
                observed_byte_37 = state.read(u16(channel_cursor + 0))
                conditions = state.memory_bit_conditions(observed_byte_37, 5, conditions, u16(channel_cursor + 0), True)
                # source-effect driver:023a:jr
                if not (conditions & 0x40):
                    # source-effect driver:0249:ld
                    observed_byte_38 = state.read(parameter_cursor)
                    sample = u8(observed_byte_38)
                    # source-effect driver:024a:inc
                    parameter_cursor = u16(parameter_cursor + 1)
                    # source-effect driver:024b:ld
                    state.write(u16(channel_cursor + 16), u8(sample))
                    # source-effect driver:024e:jr
                    pass  # Static control continuation is structured below.
                    # source-effect driver:0274:ld
                    observed_byte_39 = state.read(parameter_cursor)
                    sample = u8(observed_byte_39)
                    # source-effect driver:0275:inc
                    parameter_cursor = u16(parameter_cursor + 1)
                    # source-effect driver:0276:call
                    from .business_notes import multiply_note_duration
                    from .contexts import MultiplyNoteDurationInput
                    stack_cursor = state.push_word(stack_cursor, 633)
                    updated_audio_values_40 = multiply_note_duration(state, MultiplyNoteDurationInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 633)))
                    channel_cursor = updated_audio_values_40.channel_cursor
                    conditions = updated_audio_values_40.conditions
                    count_and_data = updated_audio_values_40.count_and_data
                    sample = updated_audio_values_40.sample
                    stack_cursor = updated_audio_values_40.stack_cursor
                    # source-effect driver:0279:ld
                    state.write(u16(channel_cursor + 12), u8(sample))
                else:
                    # source-effect driver:023c:ld
                    observed_byte_41 = state.read(parameter_cursor)
                    sample = u8(observed_byte_41)
                    # source-effect driver:023d:or
                    sample = u8(sample | sample)
                    conditions = logic_conditions(sample, False)
                    # source-effect driver:023e:jp
                    if not (conditions & 0x80):
                        # source-effect driver:0275:inc
                        parameter_cursor = u16(parameter_cursor + 1)
                        # source-effect driver:0276:call
                        from .business_notes import multiply_note_duration
                        from .contexts import MultiplyNoteDurationInput
                        stack_cursor = state.push_word(stack_cursor, 633)
                        updated_audio_values_42 = multiply_note_duration(state, MultiplyNoteDurationInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 633)))
                        channel_cursor = updated_audio_values_42.channel_cursor
                        conditions = updated_audio_values_42.conditions
                        count_and_data = updated_audio_values_42.count_and_data
                        sample = updated_audio_values_42.sample
                        stack_cursor = updated_audio_values_42.stack_cursor
                        # source-effect driver:0279:ld
                        state.write(u16(channel_cursor + 12), u8(sample))
                    else:
                        # source-effect driver:0241:ld
                        observed_byte_43 = state.read(u16(channel_cursor + 12))
                        sample = u8(observed_byte_43)
                        # source-effect driver:0244:ld
                        state.write(u16(channel_cursor + 11), u8(sample))
                        # source-effect driver:0247:jr
                        pass  # Static control continuation is structured below.
        # source-effect driver:027c:ld
        state.write(u16(channel_cursor + 3), u8(low(parameter_cursor)))
        # source-effect driver:027f:ld
        state.write(u16(channel_cursor + 4), u8(high(parameter_cursor)))
        # source-effect driver:0282:ld
        observed_byte_44 = state.read(u16(channel_cursor + 12))
        sample = u8(observed_byte_44)
        # source-effect driver:0285:ld
        state.write(u16(channel_cursor + 11), u8(sample))
        # source-effect driver:0288:bit
        observed_byte_45 = state.read(u16(channel_cursor + 0))
        conditions = state.memory_bit_conditions(observed_byte_45, 1, conditions, u16(channel_cursor + 0), True)
        # source-effect driver:028c:ret
        if not (conditions & 0x40):
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return ReadNoteOrDurationResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
        # source-effect driver:028d:xor
        sample = u8(sample ^ sample)
        conditions = logic_conditions(sample, False)
        # source-effect driver:028e:ld
        state.write(u16(channel_cursor + 37), u8(sample))
        # source-effect driver:0291:ld
        state.write(u16(channel_cursor + 34), u8(sample))
        # source-effect driver:0294:ld
        observed_byte_46 = state.read(u16(channel_cursor + 31))
        sample = u8(observed_byte_46)
        # source-effect driver:0297:ld
        state.write(u16(channel_cursor + 30), u8(sample))
        # source-effect driver:029a:ld
        state.write(u16(channel_cursor + 23), u8(sample))
        # source-effect driver:029d:ret
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return ReadNoteOrDurationResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def multiply_note_duration(state: AudioState, inputs: MultiplyNoteDurationInput) -> MultiplyNoteDurationResult:
    """Multiply note duration."""
    checked_state(state)
    if type(inputs) is not MultiplyNoteDurationInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    channel_cursor = inputs.channel_cursor
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:029e:ld
    observed_byte_1 = state.read(u16(channel_cursor + 2))
    count_and_data = replace_high(count_and_data, observed_byte_1)
    # source-effect driver:02a1:dec
    changed_byte_2, conditions = decrement_byte(high(count_and_data), conditions)
    count_and_data = replace_high(count_and_data, changed_byte_2)
    # source-effect driver:02a2:ret
    if bool(conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return MultiplyNoteDurationResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:02a3:ld
    count_and_data = replace_low(count_and_data, sample)
    while True:
        # source-effect driver:02a4:add
        arithmetic_result_3, conditions = sum_byte(sample, low(count_and_data))
        sample = u8(arithmetic_result_3)
        # source-effect driver:02a5:djnz
        count_and_data = replace_high(count_and_data, u8(high(count_and_data) - 1))
        if high(count_and_data) != 0:
            continue
        break
    # source-effect driver:02a7:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return MultiplyNoteDurationResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor).validate(state)

def decrement_note_countdown(state: AudioState, inputs: DecrementNoteCountdownInput) -> DecrementNoteCountdownResult:
    """Decrement note countdown."""
    checked_state(state)
    if type(inputs) is not DecrementNoteCountdownInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    channel_cursor = inputs.channel_cursor
    conditions = inputs.conditions
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:0304:ld
    observed_byte_1 = state.read(u16(channel_cursor + 11))
    sample = u8(observed_byte_1)
    # source-effect driver:0307:dec
    changed_byte_2, conditions = decrement_byte(sample, conditions)
    sample = u8(changed_byte_2)
    # source-effect driver:0308:ld
    state.write(u16(channel_cursor + 11), u8(sample))
    # source-effect driver:030b:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return DecrementNoteCountdownResult(channel_cursor=channel_cursor, conditions=conditions, sample=sample, stack_cursor=stack_cursor).validate(state)

def read_rhythm_note(state: AudioState, inputs: ReadRhythmNoteInput) -> ReadRhythmNoteResult:
    """Read rhythm note."""
    checked_state(state)
    if type(inputs) is not ReadRhythmNoteInput:
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
    # source-effect driver:098f:ld
    observed_byte_1 = state.read(u16(channel_cursor + 3))
    parameter_cursor = replace_low(parameter_cursor, observed_byte_1)
    # source-effect driver:0992:ld
    observed_byte_2 = state.read(u16(channel_cursor + 4))
    parameter_cursor = replace_high(parameter_cursor, observed_byte_2)
    # source-effect driver:0995:ld
    observed_byte_3 = state.read(parameter_cursor)
    sample = u8(observed_byte_3)
    # source-effect driver:0996:inc
    parameter_cursor = u16(parameter_cursor + 1)
    # source-effect driver:0997:cp
    conditions = comparison_conditions(sample, 224)
    # source-effect driver:0999:jp
    if not (conditions & 1):
        # source-effect driver:0a3c:ld
        lookup_cursor = u16(2626)
        # source-effect driver:0a3f:jp
        pass  # Static control continuation is structured below.
        # source-effect driver:0b7b:push
        stack_cursor = state.push_word(stack_cursor, lookup_cursor)
        # source-effect driver:0b7c:sub
        sample, conditions = difference_byte(sample, 224)
        # source-effect driver:0b7e:ld
        lookup_cursor = u16(2959)
        # source-effect driver:0b81:rst
        from .business_hardware import index_word_pointer
        from .contexts import IndexWordPointerInput
        stack_cursor = state.push_word(stack_cursor, 2946)
        updated_audio_values_4 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2946)))
        conditions = updated_audio_values_4.conditions
        count_and_data = updated_audio_values_4.count_and_data
        lookup_cursor = updated_audio_values_4.lookup_cursor
        sample = updated_audio_values_4.sample
        stack_cursor = updated_audio_values_4.stack_cursor
        # source-effect driver:0b82:ld
        observed_byte_5 = state.read(parameter_cursor)
        sample = u8(observed_byte_5)
        # source-effect driver:0b83:jp
        current_transfer_values_6 = ReadRhythmNoteInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=inputs.continuation).validate(state)
        state.indirect_transfer("driver", lookup_cursor, current_transfer_values_6)
    else:
        # source-effect driver:099c:or
        sample = u8(sample | sample)
        conditions = logic_conditions(sample, False)
        # source-effect driver:099d:jp
        if not (bool(conditions & 0x80)):
            # source-effect driver:09a0:dec
            parameter_cursor = u16(parameter_cursor - 1)
            # source-effect driver:09a1:ld
            observed_byte_7 = state.read(u16(channel_cursor + 13))
            sample = u8(observed_byte_7)
        # source-effect driver:09a4:ld
        state.write(u16(channel_cursor + 13), u8(sample))
        # source-effect driver:09a7:cp
        conditions = comparison_conditions(sample, 128)
        # source-effect driver:09a9:jp
        if not (bool(conditions & 0x40)):
            # source-effect driver:09ac:push
            stack_cursor = state.push_word(stack_cursor, parameter_cursor)
            # source-effect driver:09ad:ld
            lookup_cursor = u16(7520)
            # source-effect driver:09b0:bit
            observed_byte_8 = state.read(lookup_cursor)
            conditions = state.memory_bit_conditions(observed_byte_8, 2, conditions, lookup_cursor, False)
            # source-effect driver:09b2:jr
            if not (not (conditions & 0x40)):
                # source-effect driver:09b4:and
                sample = u8(sample & 15)
                conditions = logic_conditions(sample, True)
                # source-effect driver:09b6:jr
                if not (bool(conditions & 0x40)):
                    # source-effect driver:09b8:ex
                    alternate_sample_and_conditions_9 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
                    sample, conditions = high(alternate_sample_and_conditions_9), low(alternate_sample_and_conditions_9)
                    # source-effect driver:09b9:call
                    from .business_envelopes import send_key_off
                    from .contexts import SendKeyOffInput
                    stack_cursor = state.push_word(stack_cursor, 2492)
                    updated_audio_values_10 = send_key_off(state, SendKeyOffInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2492)))
                    auxiliary_cursor = updated_audio_values_10.auxiliary_cursor
                    channel_cursor = updated_audio_values_10.channel_cursor
                    conditions = updated_audio_values_10.conditions
                    count_and_data = updated_audio_values_10.count_and_data
                    lookup_cursor = updated_audio_values_10.lookup_cursor
                    parameter_cursor = updated_audio_values_10.parameter_cursor
                    sample = updated_audio_values_10.sample
                    stack_cursor = updated_audio_values_10.stack_cursor
                    # source-effect driver:09bc:ex
                    alternate_sample_and_conditions_11 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
                    sample, conditions = high(alternate_sample_and_conditions_11), low(alternate_sample_and_conditions_11)
                    # source-effect driver:09bd:ld
                    parameter_cursor = u16(2614)
                    # source-effect driver:09c0:ex
                    parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
                    # source-effect driver:09c1:ldi
                    copied_byte = state.read(lookup_cursor)
                    state.write(parameter_cursor, copied_byte)
                    lookup_cursor = u16(lookup_cursor + 1)
                    parameter_cursor = u16(parameter_cursor + 1)
                    count_and_data = u16(count_and_data - 1)
                    conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
                    # source-effect driver:09c3:ldi
                    copied_byte = state.read(lookup_cursor)
                    state.write(parameter_cursor, copied_byte)
                    lookup_cursor = u16(lookup_cursor + 1)
                    parameter_cursor = u16(parameter_cursor + 1)
                    count_and_data = u16(count_and_data - 1)
                    conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
                    # source-effect driver:09c5:ldi
                    copied_byte = state.read(lookup_cursor)
                    state.write(parameter_cursor, copied_byte)
                    lookup_cursor = u16(lookup_cursor + 1)
                    parameter_cursor = u16(parameter_cursor + 1)
                    count_and_data = u16(count_and_data - 1)
                    conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
                    # source-effect driver:09c7:dec
                    changed_byte_12, conditions = decrement_byte(sample, conditions)
                    sample = u8(changed_byte_12)
                    # source-effect driver:09c8:ld
                    lookup_cursor = u16(2656)
                    # source-effect driver:09cb:rst
                    from .business_hardware import index_word_pointer
                    from .contexts import IndexWordPointerInput
                    stack_cursor = state.push_word(stack_cursor, 2508)
                    updated_audio_values_13 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2508)))
                    conditions = updated_audio_values_13.conditions
                    count_and_data = updated_audio_values_13.count_and_data
                    lookup_cursor = updated_audio_values_13.lookup_cursor
                    sample = updated_audio_values_13.sample
                    stack_cursor = updated_audio_values_13.stack_cursor
                    # source-effect driver:09cc:ld
                    count_and_data = u16(6)
                    # source-effect driver:09cf:ldir
                    while True:
                        copied_byte = state.read(lookup_cursor)
                        state.write(parameter_cursor, copied_byte)
                        lookup_cursor = u16(lookup_cursor + 1)
                        parameter_cursor = u16(parameter_cursor + 1)
                        count_and_data = u16(count_and_data - 1)
                        conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
                        state.bus.transfer_boundary("progressive-block-copy")
                        if count_and_data == 0:
                            break
                    # source-effect driver:09d1:call
                    from .business_loaders import initialize_channel_record
                    from .contexts import InitializeChannelRecordInput
                    stack_cursor = state.push_word(stack_cursor, 2516)
                    updated_audio_values_14 = initialize_channel_record(state, InitializeChannelRecordInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2516)))
                    conditions = updated_audio_values_14.conditions
                    count_and_data = updated_audio_values_14.count_and_data
                    lookup_cursor = updated_audio_values_14.lookup_cursor
                    parameter_cursor = updated_audio_values_14.parameter_cursor
                    sample = updated_audio_values_14.sample
                    stack_cursor = updated_audio_values_14.stack_cursor
                    # source-effect driver:09d4:ld
                    lookup_cursor = u16(7525)
                    # source-effect driver:09d7:ld
                    observed_byte_15 = state.read(u16(channel_cursor + 5))
                    sample = u8(observed_byte_15)
                    # source-effect driver:09da:add
                    observed_byte_16 = state.read(lookup_cursor)
                    arithmetic_result_17, conditions = sum_byte(sample, observed_byte_16)
                    sample = u8(arithmetic_result_17)
                    # source-effect driver:09db:ld
                    state.write(lookup_cursor, u8(sample))
                    # source-effect driver:09dc:ld
                    observed_byte_18 = state.read(7528)
                    sample = u8(observed_byte_18)
                    # source-effect driver:09df:ld
                    lookup_cursor = u16(2676)
                    # source-effect driver:09e2:rst
                    from .business_hardware import index_word_pointer
                    from .contexts import IndexWordPointerInput
                    stack_cursor = state.push_word(stack_cursor, 2531)
                    updated_audio_values_19 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2531)))
                    conditions = updated_audio_values_19.conditions
                    count_and_data = updated_audio_values_19.count_and_data
                    lookup_cursor = updated_audio_values_19.lookup_cursor
                    sample = updated_audio_values_19.sample
                    stack_cursor = updated_audio_values_19.stack_cursor
                    # source-effect driver:09e3:ld
                    observed_byte_20 = state.read(7526)
                    sample = u8(observed_byte_20)
                    # source-effect driver:09e6:ld
                    observed_byte_21 = state.read(u16(channel_cursor + 6))
                    parameter_cursor = replace_low(parameter_cursor, observed_byte_21)
                    # source-effect driver:09e9:push
                    stack_cursor = state.push_word(stack_cursor, parameter_cursor)
                    # source-effect driver:09ea:add
                    arithmetic_result_22, conditions = sum_byte(sample, low(parameter_cursor))
                    sample = u8(arithmetic_result_22)
                    # source-effect driver:09eb:ld
                    state.write(u16(channel_cursor + 6), u8(sample))
                    # source-effect driver:09ee:call
                    from .business_voice import load_instrument
                    from .contexts import LoadInstrumentInput
                    stack_cursor = state.push_word(stack_cursor, 2545)
                    updated_audio_values_23 = load_instrument(state, LoadInstrumentInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2545)))
                    channel_cursor = updated_audio_values_23.channel_cursor
                    conditions = updated_audio_values_23.conditions
                    count_and_data = updated_audio_values_23.count_and_data
                    lookup_cursor = updated_audio_values_23.lookup_cursor
                    parameter_cursor = updated_audio_values_23.parameter_cursor
                    sample = updated_audio_values_23.sample
                    stack_cursor = updated_audio_values_23.stack_cursor
                    # source-effect driver:09f1:pop
                    saved_audio_word_24, stack_cursor = state.pop_word(stack_cursor)
                    parameter_cursor = u16(saved_audio_word_24)
                    # source-effect driver:09f2:ld
                    state.write(u16(channel_cursor + 6), u8(low(parameter_cursor)))
                    # source-effect driver:09f5:call
                    from .business_loaders import reset_timer_control
                    from .contexts import ResetTimerControlInput
                    stack_cursor = state.push_word(stack_cursor, 2552)
                    updated_audio_values_25 = reset_timer_control(state, ResetTimerControlInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2552)))
                    auxiliary_cursor = updated_audio_values_25.auxiliary_cursor
                    channel_cursor = updated_audio_values_25.channel_cursor
                    conditions = updated_audio_values_25.conditions
                    count_and_data = updated_audio_values_25.count_and_data
                    lookup_cursor = updated_audio_values_25.lookup_cursor
                    parameter_cursor = updated_audio_values_25.parameter_cursor
                    sample = updated_audio_values_25.sample
                    stack_cursor = updated_audio_values_25.stack_cursor
            # source-effect driver:09f8:ld
            lookup_cursor = u16(7664)
            # source-effect driver:09fb:bit
            observed_byte_26 = state.read(lookup_cursor)
            conditions = state.memory_bit_conditions(observed_byte_26, 2, conditions, lookup_cursor, False)
            # source-effect driver:09fd:jr
            if not (not (conditions & 0x40)):
                # source-effect driver:09ff:ld
                observed_byte_27 = state.read(u16(channel_cursor + 13))
                sample = u8(observed_byte_27)
                # source-effect driver:0a02:and
                sample = u8(sample & 112)
                conditions = logic_conditions(sample, True)
                # source-effect driver:0a04:jr
                if not (bool(conditions & 0x40)):
                    # source-effect driver:0a06:ld
                    parameter_cursor = u16(2617)
                    # source-effect driver:0a09:ex
                    parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
                    # source-effect driver:0a0a:ldi
                    copied_byte = state.read(lookup_cursor)
                    state.write(parameter_cursor, copied_byte)
                    lookup_cursor = u16(lookup_cursor + 1)
                    parameter_cursor = u16(parameter_cursor + 1)
                    count_and_data = u16(count_and_data - 1)
                    conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
                    # source-effect driver:0a0c:ldi
                    copied_byte = state.read(lookup_cursor)
                    state.write(parameter_cursor, copied_byte)
                    lookup_cursor = u16(lookup_cursor + 1)
                    parameter_cursor = u16(parameter_cursor + 1)
                    count_and_data = u16(count_and_data - 1)
                    conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
                    # source-effect driver:0a0e:ldi
                    copied_byte = state.read(lookup_cursor)
                    state.write(parameter_cursor, copied_byte)
                    lookup_cursor = u16(lookup_cursor + 1)
                    parameter_cursor = u16(parameter_cursor + 1)
                    count_and_data = u16(count_and_data - 1)
                    conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
                    # source-effect driver:0a10:srl
                    shifted_byte_28 = sample
                    shift_result_29 = u8((shifted_byte_28 >> 1))
                    conditions = logic_conditions(shift_result_29) | (shifted_byte_28 & 1)
                    sample = u8(shift_result_29)
                    # source-effect driver:0a12:srl
                    shifted_byte_30 = sample
                    shift_result_31 = u8((shifted_byte_30 >> 1))
                    conditions = logic_conditions(shift_result_31) | (shifted_byte_30 & 1)
                    sample = u8(shift_result_31)
                    # source-effect driver:0a14:srl
                    shifted_byte_32 = sample
                    shift_result_33 = u8((shifted_byte_32 >> 1))
                    conditions = logic_conditions(shift_result_33) | (shifted_byte_32 & 1)
                    sample = u8(shift_result_33)
                    # source-effect driver:0a16:srl
                    shifted_byte_34 = sample
                    shift_result_35 = u8((shifted_byte_34 >> 1))
                    conditions = logic_conditions(shift_result_35) | (shifted_byte_34 & 1)
                    sample = u8(shift_result_35)
                    # source-effect driver:0a18:dec
                    changed_byte_36, conditions = decrement_byte(sample, conditions)
                    sample = u8(changed_byte_36)
                    # source-effect driver:0a19:ld
                    lookup_cursor = u16(2630)
                    # source-effect driver:0a1c:rst
                    from .business_hardware import index_word_pointer
                    from .contexts import IndexWordPointerInput
                    stack_cursor = state.push_word(stack_cursor, 2589)
                    updated_audio_values_37 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2589)))
                    conditions = updated_audio_values_37.conditions
                    count_and_data = updated_audio_values_37.count_and_data
                    lookup_cursor = updated_audio_values_37.lookup_cursor
                    sample = updated_audio_values_37.sample
                    stack_cursor = updated_audio_values_37.stack_cursor
                    # source-effect driver:0a1d:ld
                    count_and_data = u16(6)
                    # source-effect driver:0a20:ldir
                    while True:
                        copied_byte = state.read(lookup_cursor)
                        state.write(parameter_cursor, copied_byte)
                        lookup_cursor = u16(lookup_cursor + 1)
                        parameter_cursor = u16(parameter_cursor + 1)
                        count_and_data = u16(count_and_data - 1)
                        conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
                        state.bus.transfer_boundary("progressive-block-copy")
                        if count_and_data == 0:
                            break
                    # source-effect driver:0a22:call
                    from .business_loaders import initialize_channel_record
                    from .contexts import InitializeChannelRecordInput
                    stack_cursor = state.push_word(stack_cursor, 2597)
                    updated_audio_values_38 = initialize_channel_record(state, InitializeChannelRecordInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2597)))
                    conditions = updated_audio_values_38.conditions
                    count_and_data = updated_audio_values_38.count_and_data
                    lookup_cursor = updated_audio_values_38.lookup_cursor
                    parameter_cursor = updated_audio_values_38.parameter_cursor
                    sample = updated_audio_values_38.sample
                    stack_cursor = updated_audio_values_38.stack_cursor
            # source-effect driver:0a25:pop
            saved_audio_word_39, stack_cursor = state.pop_word(stack_cursor)
            parameter_cursor = u16(saved_audio_word_39)
        # source-effect driver:0a26:ld
        observed_byte_40 = state.read(parameter_cursor)
        sample = u8(observed_byte_40)
        # source-effect driver:0a27:inc
        parameter_cursor = u16(parameter_cursor + 1)
        # source-effect driver:0a28:or
        sample = u8(sample | sample)
        conditions = logic_conditions(sample, False)
        # source-effect driver:0a29:jp
        if not (conditions & 0x80):
            # source-effect driver:0276:call
            from .business_notes import multiply_note_duration
            from .contexts import MultiplyNoteDurationInput
            stack_cursor = state.push_word(stack_cursor, 633)
            updated_audio_values_41 = multiply_note_duration(state, MultiplyNoteDurationInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 633)))
            channel_cursor = updated_audio_values_41.channel_cursor
            conditions = updated_audio_values_41.conditions
            count_and_data = updated_audio_values_41.count_and_data
            sample = updated_audio_values_41.sample
            stack_cursor = updated_audio_values_41.stack_cursor
            # source-effect driver:0279:ld
            state.write(u16(channel_cursor + 12), u8(sample))
        else:
            # source-effect driver:0a2c:dec
            parameter_cursor = u16(parameter_cursor - 1)
            # source-effect driver:0a2d:ld
            observed_byte_42 = state.read(u16(channel_cursor + 12))
            sample = u8(observed_byte_42)
            # source-effect driver:0a30:ld
            state.write(u16(channel_cursor + 11), u8(sample))
            # source-effect driver:0a33:jp
            pass  # Static control continuation is structured below.
        # source-effect driver:027c:ld
        state.write(u16(channel_cursor + 3), u8(low(parameter_cursor)))
        # source-effect driver:027f:ld
        state.write(u16(channel_cursor + 4), u8(high(parameter_cursor)))
        # source-effect driver:0282:ld
        observed_byte_43 = state.read(u16(channel_cursor + 12))
        sample = u8(observed_byte_43)
        # source-effect driver:0285:ld
        state.write(u16(channel_cursor + 11), u8(sample))
        # source-effect driver:0288:bit
        observed_byte_44 = state.read(u16(channel_cursor + 0))
        conditions = state.memory_bit_conditions(observed_byte_44, 1, conditions, u16(channel_cursor + 0), True)
        # source-effect driver:028c:ret
        if not (conditions & 0x40):
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return ReadRhythmNoteResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
        # source-effect driver:028d:xor
        sample = u8(sample ^ sample)
        conditions = logic_conditions(sample, False)
        # source-effect driver:028e:ld
        state.write(u16(channel_cursor + 37), u8(sample))
        # source-effect driver:0291:ld
        state.write(u16(channel_cursor + 34), u8(sample))
        # source-effect driver:0294:ld
        observed_byte_45 = state.read(u16(channel_cursor + 31))
        sample = u8(observed_byte_45)
        # source-effect driver:0297:ld
        state.write(u16(channel_cursor + 30), u8(sample))
        # source-effect driver:029a:ld
        state.write(u16(channel_cursor + 23), u8(sample))
        # source-effect driver:029d:ret
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return ReadRhythmNoteResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def resume_rhythm_parameter_stream(state: AudioState, inputs: ResumeRhythmParameterStreamInput) -> ResumeRhythmParameterStreamResult:
    """Resume rhythm parameter stream."""
    checked_state(state)
    if type(inputs) is not ResumeRhythmParameterStreamInput:
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
    # source-effect driver:0a42:inc
    parameter_cursor = u16(parameter_cursor + 1)
    # source-effect driver:0a43:jp
    pass  # Static control continuation is structured below.
    # source-effect driver:0995:ld
    observed_byte_1 = state.read(parameter_cursor)
    sample = u8(observed_byte_1)
    # source-effect driver:0996:inc
    parameter_cursor = u16(parameter_cursor + 1)
    # source-effect driver:0997:cp
    conditions = comparison_conditions(sample, 224)
    # source-effect driver:0999:jp
    if not (conditions & 1):
        # source-effect driver:0a3c:ld
        lookup_cursor = u16(2626)
        # source-effect driver:0a3f:jp
        pass  # Static control continuation is structured below.
        # source-effect driver:0b7b:push
        stack_cursor = state.push_word(stack_cursor, lookup_cursor)
        # source-effect driver:0b7c:sub
        sample, conditions = difference_byte(sample, 224)
        # source-effect driver:0b7e:ld
        lookup_cursor = u16(2959)
        # source-effect driver:0b81:rst
        from .business_hardware import index_word_pointer
        from .contexts import IndexWordPointerInput
        stack_cursor = state.push_word(stack_cursor, 2946)
        updated_audio_values_2 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2946)))
        conditions = updated_audio_values_2.conditions
        count_and_data = updated_audio_values_2.count_and_data
        lookup_cursor = updated_audio_values_2.lookup_cursor
        sample = updated_audio_values_2.sample
        stack_cursor = updated_audio_values_2.stack_cursor
        # source-effect driver:0b82:ld
        observed_byte_3 = state.read(parameter_cursor)
        sample = u8(observed_byte_3)
        # source-effect driver:0b83:jp
        current_transfer_values_4 = ResumeRhythmParameterStreamInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=inputs.continuation).validate(state)
        state.indirect_transfer("driver", lookup_cursor, current_transfer_values_4)
    else:
        # source-effect driver:099c:or
        sample = u8(sample | sample)
        conditions = logic_conditions(sample, False)
        # source-effect driver:099d:jp
        if not (bool(conditions & 0x80)):
            # source-effect driver:09a0:dec
            parameter_cursor = u16(parameter_cursor - 1)
            # source-effect driver:09a1:ld
            observed_byte_5 = state.read(u16(channel_cursor + 13))
            sample = u8(observed_byte_5)
        # source-effect driver:09a4:ld
        state.write(u16(channel_cursor + 13), u8(sample))
        # source-effect driver:09a7:cp
        conditions = comparison_conditions(sample, 128)
        # source-effect driver:09a9:jp
        if not (bool(conditions & 0x40)):
            # source-effect driver:09ac:push
            stack_cursor = state.push_word(stack_cursor, parameter_cursor)
            # source-effect driver:09ad:ld
            lookup_cursor = u16(7520)
            # source-effect driver:09b0:bit
            observed_byte_6 = state.read(lookup_cursor)
            conditions = state.memory_bit_conditions(observed_byte_6, 2, conditions, lookup_cursor, False)
            # source-effect driver:09b2:jr
            if not (not (conditions & 0x40)):
                # source-effect driver:09b4:and
                sample = u8(sample & 15)
                conditions = logic_conditions(sample, True)
                # source-effect driver:09b6:jr
                if not (bool(conditions & 0x40)):
                    # source-effect driver:09b8:ex
                    alternate_sample_and_conditions_7 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
                    sample, conditions = high(alternate_sample_and_conditions_7), low(alternate_sample_and_conditions_7)
                    # source-effect driver:09b9:call
                    from .business_envelopes import send_key_off
                    from .contexts import SendKeyOffInput
                    stack_cursor = state.push_word(stack_cursor, 2492)
                    updated_audio_values_8 = send_key_off(state, SendKeyOffInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2492)))
                    auxiliary_cursor = updated_audio_values_8.auxiliary_cursor
                    channel_cursor = updated_audio_values_8.channel_cursor
                    conditions = updated_audio_values_8.conditions
                    count_and_data = updated_audio_values_8.count_and_data
                    lookup_cursor = updated_audio_values_8.lookup_cursor
                    parameter_cursor = updated_audio_values_8.parameter_cursor
                    sample = updated_audio_values_8.sample
                    stack_cursor = updated_audio_values_8.stack_cursor
                    # source-effect driver:09bc:ex
                    alternate_sample_and_conditions_9 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
                    sample, conditions = high(alternate_sample_and_conditions_9), low(alternate_sample_and_conditions_9)
                    # source-effect driver:09bd:ld
                    parameter_cursor = u16(2614)
                    # source-effect driver:09c0:ex
                    parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
                    # source-effect driver:09c1:ldi
                    copied_byte = state.read(lookup_cursor)
                    state.write(parameter_cursor, copied_byte)
                    lookup_cursor = u16(lookup_cursor + 1)
                    parameter_cursor = u16(parameter_cursor + 1)
                    count_and_data = u16(count_and_data - 1)
                    conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
                    # source-effect driver:09c3:ldi
                    copied_byte = state.read(lookup_cursor)
                    state.write(parameter_cursor, copied_byte)
                    lookup_cursor = u16(lookup_cursor + 1)
                    parameter_cursor = u16(parameter_cursor + 1)
                    count_and_data = u16(count_and_data - 1)
                    conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
                    # source-effect driver:09c5:ldi
                    copied_byte = state.read(lookup_cursor)
                    state.write(parameter_cursor, copied_byte)
                    lookup_cursor = u16(lookup_cursor + 1)
                    parameter_cursor = u16(parameter_cursor + 1)
                    count_and_data = u16(count_and_data - 1)
                    conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
                    # source-effect driver:09c7:dec
                    changed_byte_10, conditions = decrement_byte(sample, conditions)
                    sample = u8(changed_byte_10)
                    # source-effect driver:09c8:ld
                    lookup_cursor = u16(2656)
                    # source-effect driver:09cb:rst
                    from .business_hardware import index_word_pointer
                    from .contexts import IndexWordPointerInput
                    stack_cursor = state.push_word(stack_cursor, 2508)
                    updated_audio_values_11 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2508)))
                    conditions = updated_audio_values_11.conditions
                    count_and_data = updated_audio_values_11.count_and_data
                    lookup_cursor = updated_audio_values_11.lookup_cursor
                    sample = updated_audio_values_11.sample
                    stack_cursor = updated_audio_values_11.stack_cursor
                    # source-effect driver:09cc:ld
                    count_and_data = u16(6)
                    # source-effect driver:09cf:ldir
                    while True:
                        copied_byte = state.read(lookup_cursor)
                        state.write(parameter_cursor, copied_byte)
                        lookup_cursor = u16(lookup_cursor + 1)
                        parameter_cursor = u16(parameter_cursor + 1)
                        count_and_data = u16(count_and_data - 1)
                        conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
                        state.bus.transfer_boundary("progressive-block-copy")
                        if count_and_data == 0:
                            break
                    # source-effect driver:09d1:call
                    from .business_loaders import initialize_channel_record
                    from .contexts import InitializeChannelRecordInput
                    stack_cursor = state.push_word(stack_cursor, 2516)
                    updated_audio_values_12 = initialize_channel_record(state, InitializeChannelRecordInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2516)))
                    conditions = updated_audio_values_12.conditions
                    count_and_data = updated_audio_values_12.count_and_data
                    lookup_cursor = updated_audio_values_12.lookup_cursor
                    parameter_cursor = updated_audio_values_12.parameter_cursor
                    sample = updated_audio_values_12.sample
                    stack_cursor = updated_audio_values_12.stack_cursor
                    # source-effect driver:09d4:ld
                    lookup_cursor = u16(7525)
                    # source-effect driver:09d7:ld
                    observed_byte_13 = state.read(u16(channel_cursor + 5))
                    sample = u8(observed_byte_13)
                    # source-effect driver:09da:add
                    observed_byte_14 = state.read(lookup_cursor)
                    arithmetic_result_15, conditions = sum_byte(sample, observed_byte_14)
                    sample = u8(arithmetic_result_15)
                    # source-effect driver:09db:ld
                    state.write(lookup_cursor, u8(sample))
                    # source-effect driver:09dc:ld
                    observed_byte_16 = state.read(7528)
                    sample = u8(observed_byte_16)
                    # source-effect driver:09df:ld
                    lookup_cursor = u16(2676)
                    # source-effect driver:09e2:rst
                    from .business_hardware import index_word_pointer
                    from .contexts import IndexWordPointerInput
                    stack_cursor = state.push_word(stack_cursor, 2531)
                    updated_audio_values_17 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2531)))
                    conditions = updated_audio_values_17.conditions
                    count_and_data = updated_audio_values_17.count_and_data
                    lookup_cursor = updated_audio_values_17.lookup_cursor
                    sample = updated_audio_values_17.sample
                    stack_cursor = updated_audio_values_17.stack_cursor
                    # source-effect driver:09e3:ld
                    observed_byte_18 = state.read(7526)
                    sample = u8(observed_byte_18)
                    # source-effect driver:09e6:ld
                    observed_byte_19 = state.read(u16(channel_cursor + 6))
                    parameter_cursor = replace_low(parameter_cursor, observed_byte_19)
                    # source-effect driver:09e9:push
                    stack_cursor = state.push_word(stack_cursor, parameter_cursor)
                    # source-effect driver:09ea:add
                    arithmetic_result_20, conditions = sum_byte(sample, low(parameter_cursor))
                    sample = u8(arithmetic_result_20)
                    # source-effect driver:09eb:ld
                    state.write(u16(channel_cursor + 6), u8(sample))
                    # source-effect driver:09ee:call
                    from .business_voice import load_instrument
                    from .contexts import LoadInstrumentInput
                    stack_cursor = state.push_word(stack_cursor, 2545)
                    updated_audio_values_21 = load_instrument(state, LoadInstrumentInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2545)))
                    channel_cursor = updated_audio_values_21.channel_cursor
                    conditions = updated_audio_values_21.conditions
                    count_and_data = updated_audio_values_21.count_and_data
                    lookup_cursor = updated_audio_values_21.lookup_cursor
                    parameter_cursor = updated_audio_values_21.parameter_cursor
                    sample = updated_audio_values_21.sample
                    stack_cursor = updated_audio_values_21.stack_cursor
                    # source-effect driver:09f1:pop
                    saved_audio_word_22, stack_cursor = state.pop_word(stack_cursor)
                    parameter_cursor = u16(saved_audio_word_22)
                    # source-effect driver:09f2:ld
                    state.write(u16(channel_cursor + 6), u8(low(parameter_cursor)))
                    # source-effect driver:09f5:call
                    from .business_loaders import reset_timer_control
                    from .contexts import ResetTimerControlInput
                    stack_cursor = state.push_word(stack_cursor, 2552)
                    updated_audio_values_23 = reset_timer_control(state, ResetTimerControlInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2552)))
                    auxiliary_cursor = updated_audio_values_23.auxiliary_cursor
                    channel_cursor = updated_audio_values_23.channel_cursor
                    conditions = updated_audio_values_23.conditions
                    count_and_data = updated_audio_values_23.count_and_data
                    lookup_cursor = updated_audio_values_23.lookup_cursor
                    parameter_cursor = updated_audio_values_23.parameter_cursor
                    sample = updated_audio_values_23.sample
                    stack_cursor = updated_audio_values_23.stack_cursor
            # source-effect driver:09f8:ld
            lookup_cursor = u16(7664)
            # source-effect driver:09fb:bit
            observed_byte_24 = state.read(lookup_cursor)
            conditions = state.memory_bit_conditions(observed_byte_24, 2, conditions, lookup_cursor, False)
            # source-effect driver:09fd:jr
            if not (not (conditions & 0x40)):
                # source-effect driver:09ff:ld
                observed_byte_25 = state.read(u16(channel_cursor + 13))
                sample = u8(observed_byte_25)
                # source-effect driver:0a02:and
                sample = u8(sample & 112)
                conditions = logic_conditions(sample, True)
                # source-effect driver:0a04:jr
                if not (bool(conditions & 0x40)):
                    # source-effect driver:0a06:ld
                    parameter_cursor = u16(2617)
                    # source-effect driver:0a09:ex
                    parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
                    # source-effect driver:0a0a:ldi
                    copied_byte = state.read(lookup_cursor)
                    state.write(parameter_cursor, copied_byte)
                    lookup_cursor = u16(lookup_cursor + 1)
                    parameter_cursor = u16(parameter_cursor + 1)
                    count_and_data = u16(count_and_data - 1)
                    conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
                    # source-effect driver:0a0c:ldi
                    copied_byte = state.read(lookup_cursor)
                    state.write(parameter_cursor, copied_byte)
                    lookup_cursor = u16(lookup_cursor + 1)
                    parameter_cursor = u16(parameter_cursor + 1)
                    count_and_data = u16(count_and_data - 1)
                    conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
                    # source-effect driver:0a0e:ldi
                    copied_byte = state.read(lookup_cursor)
                    state.write(parameter_cursor, copied_byte)
                    lookup_cursor = u16(lookup_cursor + 1)
                    parameter_cursor = u16(parameter_cursor + 1)
                    count_and_data = u16(count_and_data - 1)
                    conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
                    # source-effect driver:0a10:srl
                    shifted_byte_26 = sample
                    shift_result_27 = u8((shifted_byte_26 >> 1))
                    conditions = logic_conditions(shift_result_27) | (shifted_byte_26 & 1)
                    sample = u8(shift_result_27)
                    # source-effect driver:0a12:srl
                    shifted_byte_28 = sample
                    shift_result_29 = u8((shifted_byte_28 >> 1))
                    conditions = logic_conditions(shift_result_29) | (shifted_byte_28 & 1)
                    sample = u8(shift_result_29)
                    # source-effect driver:0a14:srl
                    shifted_byte_30 = sample
                    shift_result_31 = u8((shifted_byte_30 >> 1))
                    conditions = logic_conditions(shift_result_31) | (shifted_byte_30 & 1)
                    sample = u8(shift_result_31)
                    # source-effect driver:0a16:srl
                    shifted_byte_32 = sample
                    shift_result_33 = u8((shifted_byte_32 >> 1))
                    conditions = logic_conditions(shift_result_33) | (shifted_byte_32 & 1)
                    sample = u8(shift_result_33)
                    # source-effect driver:0a18:dec
                    changed_byte_34, conditions = decrement_byte(sample, conditions)
                    sample = u8(changed_byte_34)
                    # source-effect driver:0a19:ld
                    lookup_cursor = u16(2630)
                    # source-effect driver:0a1c:rst
                    from .business_hardware import index_word_pointer
                    from .contexts import IndexWordPointerInput
                    stack_cursor = state.push_word(stack_cursor, 2589)
                    updated_audio_values_35 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2589)))
                    conditions = updated_audio_values_35.conditions
                    count_and_data = updated_audio_values_35.count_and_data
                    lookup_cursor = updated_audio_values_35.lookup_cursor
                    sample = updated_audio_values_35.sample
                    stack_cursor = updated_audio_values_35.stack_cursor
                    # source-effect driver:0a1d:ld
                    count_and_data = u16(6)
                    # source-effect driver:0a20:ldir
                    while True:
                        copied_byte = state.read(lookup_cursor)
                        state.write(parameter_cursor, copied_byte)
                        lookup_cursor = u16(lookup_cursor + 1)
                        parameter_cursor = u16(parameter_cursor + 1)
                        count_and_data = u16(count_and_data - 1)
                        conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
                        state.bus.transfer_boundary("progressive-block-copy")
                        if count_and_data == 0:
                            break
                    # source-effect driver:0a22:call
                    from .business_loaders import initialize_channel_record
                    from .contexts import InitializeChannelRecordInput
                    stack_cursor = state.push_word(stack_cursor, 2597)
                    updated_audio_values_36 = initialize_channel_record(state, InitializeChannelRecordInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2597)))
                    conditions = updated_audio_values_36.conditions
                    count_and_data = updated_audio_values_36.count_and_data
                    lookup_cursor = updated_audio_values_36.lookup_cursor
                    parameter_cursor = updated_audio_values_36.parameter_cursor
                    sample = updated_audio_values_36.sample
                    stack_cursor = updated_audio_values_36.stack_cursor
            # source-effect driver:0a25:pop
            saved_audio_word_37, stack_cursor = state.pop_word(stack_cursor)
            parameter_cursor = u16(saved_audio_word_37)
        # source-effect driver:0a26:ld
        observed_byte_38 = state.read(parameter_cursor)
        sample = u8(observed_byte_38)
        # source-effect driver:0a27:inc
        parameter_cursor = u16(parameter_cursor + 1)
        # source-effect driver:0a28:or
        sample = u8(sample | sample)
        conditions = logic_conditions(sample, False)
        # source-effect driver:0a29:jp
        if not (conditions & 0x80):
            # source-effect driver:0276:call
            from .business_notes import multiply_note_duration
            from .contexts import MultiplyNoteDurationInput
            stack_cursor = state.push_word(stack_cursor, 633)
            updated_audio_values_39 = multiply_note_duration(state, MultiplyNoteDurationInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 633)))
            channel_cursor = updated_audio_values_39.channel_cursor
            conditions = updated_audio_values_39.conditions
            count_and_data = updated_audio_values_39.count_and_data
            sample = updated_audio_values_39.sample
            stack_cursor = updated_audio_values_39.stack_cursor
            # source-effect driver:0279:ld
            state.write(u16(channel_cursor + 12), u8(sample))
        else:
            # source-effect driver:0a2c:dec
            parameter_cursor = u16(parameter_cursor - 1)
            # source-effect driver:0a2d:ld
            observed_byte_40 = state.read(u16(channel_cursor + 12))
            sample = u8(observed_byte_40)
            # source-effect driver:0a30:ld
            state.write(u16(channel_cursor + 11), u8(sample))
            # source-effect driver:0a33:jp
            pass  # Static control continuation is structured below.
        # source-effect driver:027c:ld
        state.write(u16(channel_cursor + 3), u8(low(parameter_cursor)))
        # source-effect driver:027f:ld
        state.write(u16(channel_cursor + 4), u8(high(parameter_cursor)))
        # source-effect driver:0282:ld
        observed_byte_41 = state.read(u16(channel_cursor + 12))
        sample = u8(observed_byte_41)
        # source-effect driver:0285:ld
        state.write(u16(channel_cursor + 11), u8(sample))
        # source-effect driver:0288:bit
        observed_byte_42 = state.read(u16(channel_cursor + 0))
        conditions = state.memory_bit_conditions(observed_byte_42, 1, conditions, u16(channel_cursor + 0), True)
        # source-effect driver:028c:ret
        if not (conditions & 0x40):
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return ResumeRhythmParameterStreamResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
        # source-effect driver:028d:xor
        sample = u8(sample ^ sample)
        conditions = logic_conditions(sample, False)
        # source-effect driver:028e:ld
        state.write(u16(channel_cursor + 37), u8(sample))
        # source-effect driver:0291:ld
        state.write(u16(channel_cursor + 34), u8(sample))
        # source-effect driver:0294:ld
        observed_byte_43 = state.read(u16(channel_cursor + 31))
        sample = u8(observed_byte_43)
        # source-effect driver:0297:ld
        state.write(u16(channel_cursor + 30), u8(sample))
        # source-effect driver:029a:ld
        state.write(u16(channel_cursor + 23), u8(sample))
        # source-effect driver:029d:ret
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return ResumeRhythmParameterStreamResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def resume_note_parameter_stream(state: AudioState, inputs: ResumeNoteParameterStreamInput) -> ResumeNoteParameterStreamResult:
    """Resume note parameter stream."""
    checked_state(state)
    if type(inputs) is not ResumeNoteParameterStreamInput:
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
    # source-effect driver:0b84:inc
    parameter_cursor = u16(parameter_cursor + 1)
    # source-effect driver:0b85:jp
    pass  # Static control continuation is structured below.
    # source-effect driver:01e4:ld
    observed_byte_1 = state.read(parameter_cursor)
    sample = u8(observed_byte_1)
    # source-effect driver:01e5:inc
    parameter_cursor = u16(parameter_cursor + 1)
    # source-effect driver:01e6:cp
    conditions = comparison_conditions(sample, 224)
    # source-effect driver:01e8:jp
    if not (conditions & 1):
        # source-effect driver:0b78:ld
        lookup_cursor = u16(2948)
        # source-effect driver:0b7b:push
        stack_cursor = state.push_word(stack_cursor, lookup_cursor)
        # source-effect driver:0b7c:sub
        sample, conditions = difference_byte(sample, 224)
        # source-effect driver:0b7e:ld
        lookup_cursor = u16(2959)
        # source-effect driver:0b81:rst
        from .business_hardware import index_word_pointer
        from .contexts import IndexWordPointerInput
        stack_cursor = state.push_word(stack_cursor, 2946)
        updated_audio_values_2 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 2946)))
        conditions = updated_audio_values_2.conditions
        count_and_data = updated_audio_values_2.count_and_data
        lookup_cursor = updated_audio_values_2.lookup_cursor
        sample = updated_audio_values_2.sample
        stack_cursor = updated_audio_values_2.stack_cursor
        # source-effect driver:0b82:ld
        observed_byte_3 = state.read(parameter_cursor)
        sample = u8(observed_byte_3)
        # source-effect driver:0b83:jp
        current_transfer_values_4 = ResumeNoteParameterStreamInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=inputs.continuation).validate(state)
        state.indirect_transfer("driver", lookup_cursor, current_transfer_values_4)
    else:
        # source-effect driver:01eb:ex
        alternate_sample_and_conditions_5 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
        sample, conditions = high(alternate_sample_and_conditions_5), low(alternate_sample_and_conditions_5)
        # source-effect driver:01ec:call
        from .business_envelopes import send_key_off
        from .contexts import SendKeyOffInput
        stack_cursor = state.push_word(stack_cursor, 495)
        updated_audio_values_6 = send_key_off(state, SendKeyOffInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 495)))
        auxiliary_cursor = updated_audio_values_6.auxiliary_cursor
        channel_cursor = updated_audio_values_6.channel_cursor
        conditions = updated_audio_values_6.conditions
        count_and_data = updated_audio_values_6.count_and_data
        lookup_cursor = updated_audio_values_6.lookup_cursor
        parameter_cursor = updated_audio_values_6.parameter_cursor
        sample = updated_audio_values_6.sample
        stack_cursor = updated_audio_values_6.stack_cursor
        # source-effect driver:01ef:call
        from .business_pan import update_pan_pattern
        from .contexts import UpdatePanPatternInput
        stack_cursor = state.push_word(stack_cursor, 498)
        updated_audio_values_7 = update_pan_pattern(state, UpdatePanPatternInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 498)))
        channel_cursor = updated_audio_values_7.channel_cursor
        conditions = updated_audio_values_7.conditions
        count_and_data = updated_audio_values_7.count_and_data
        lookup_cursor = updated_audio_values_7.lookup_cursor
        parameter_cursor = updated_audio_values_7.parameter_cursor
        sample = updated_audio_values_7.sample
        stack_cursor = updated_audio_values_7.stack_cursor
        # source-effect driver:01f2:ex
        alternate_sample_and_conditions_8 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
        sample, conditions = high(alternate_sample_and_conditions_8), low(alternate_sample_and_conditions_8)
        # source-effect driver:01f3:bit
        observed_byte_9 = state.read(u16(channel_cursor + 0))
        conditions = state.memory_bit_conditions(observed_byte_9, 3, conditions, u16(channel_cursor + 0), True)
        # source-effect driver:01f7:jp
        if not (conditions & 0x40):
            # source-effect driver:0250:ld
            lookup_cursor = replace_high(lookup_cursor, sample)
            # source-effect driver:0251:ld
            observed_byte_10 = state.read(parameter_cursor)
            sample = u8(observed_byte_10)
            # source-effect driver:0252:inc
            parameter_cursor = u16(parameter_cursor + 1)
            # source-effect driver:0253:ld
            lookup_cursor = replace_low(lookup_cursor, sample)
            # source-effect driver:0254:or
            sample = u8(sample | high(lookup_cursor))
            conditions = logic_conditions(sample, False)
            # source-effect driver:0255:jr
            if not (bool(conditions & 0x40)):
                # source-effect driver:0257:ld
                observed_byte_11 = state.read(u16(channel_cursor + 5))
                sample = u8(observed_byte_11)
                # source-effect driver:025a:ld
                count_and_data = replace_high(count_and_data, 0)
                # source-effect driver:025c:or
                sample = u8(sample | sample)
                conditions = logic_conditions(sample, False)
                # source-effect driver:025d:jp
                if not (not (conditions & 0x80)):
                    # source-effect driver:0260:dec
                    changed_byte_12, conditions = decrement_byte(high(count_and_data), conditions)
                    count_and_data = replace_high(count_and_data, changed_byte_12)
                # source-effect driver:0261:ld
                count_and_data = replace_low(count_and_data, sample)
                # source-effect driver:0262:add
                arithmetic_result_13, conditions = sum_word(lookup_cursor, count_and_data, conditions)
                lookup_cursor = u16(arithmetic_result_13)
            # source-effect driver:0263:ld
            state.write(u16(channel_cursor + 13), u8(low(lookup_cursor)))
            # source-effect driver:0266:ld
            state.write(u16(channel_cursor + 14), u8(high(lookup_cursor)))
            # source-effect driver:0269:bit
            observed_byte_14 = state.read(u16(channel_cursor + 0))
            conditions = state.memory_bit_conditions(observed_byte_14, 5, conditions, u16(channel_cursor + 0), True)
            # source-effect driver:026d:jr
            if not (bool(conditions & 0x40)):
                # source-effect driver:026f:ld
                observed_byte_15 = state.read(parameter_cursor)
                sample = u8(observed_byte_15)
                # source-effect driver:0270:inc
                parameter_cursor = u16(parameter_cursor + 1)
                # source-effect driver:0271:ld
                state.write(u16(channel_cursor + 16), u8(sample))
            # source-effect driver:0274:ld
            observed_byte_16 = state.read(parameter_cursor)
            sample = u8(observed_byte_16)
            # source-effect driver:0275:inc
            parameter_cursor = u16(parameter_cursor + 1)
            # source-effect driver:0276:call
            from .business_notes import multiply_note_duration
            from .contexts import MultiplyNoteDurationInput
            stack_cursor = state.push_word(stack_cursor, 633)
            updated_audio_values_17 = multiply_note_duration(state, MultiplyNoteDurationInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 633)))
            channel_cursor = updated_audio_values_17.channel_cursor
            conditions = updated_audio_values_17.conditions
            count_and_data = updated_audio_values_17.count_and_data
            sample = updated_audio_values_17.sample
            stack_cursor = updated_audio_values_17.stack_cursor
            # source-effect driver:0279:ld
            state.write(u16(channel_cursor + 12), u8(sample))
        else:
            # source-effect driver:01fa:or
            sample = u8(sample | sample)
            conditions = logic_conditions(sample, False)
            # source-effect driver:01fb:jp
            if not (conditions & 0x80):
                # source-effect driver:0276:call
                from .business_notes import multiply_note_duration
                from .contexts import MultiplyNoteDurationInput
                stack_cursor = state.push_word(stack_cursor, 633)
                updated_audio_values_18 = multiply_note_duration(state, MultiplyNoteDurationInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 633)))
                channel_cursor = updated_audio_values_18.channel_cursor
                conditions = updated_audio_values_18.conditions
                count_and_data = updated_audio_values_18.count_and_data
                sample = updated_audio_values_18.sample
                stack_cursor = updated_audio_values_18.stack_cursor
                # source-effect driver:0279:ld
                state.write(u16(channel_cursor + 12), u8(sample))
            else:
                # source-effect driver:01fe:sub
                sample, conditions = difference_byte(sample, 129)
                # source-effect driver:0200:jp
                if not (conditions & 0x80):
                    # source-effect driver:0208:add
                    observed_byte_19 = state.read(u16(channel_cursor + 5))
                    arithmetic_result_20, conditions = sum_byte(sample, observed_byte_19)
                    sample = u8(arithmetic_result_20)
                    # source-effect driver:020b:ld
                    lookup_cursor = u16(2278)
                    # source-effect driver:020e:push
                    stack_cursor = state.push_word(stack_cursor, ((sample << 8) | conditions))
                    # source-effect driver:020f:rst
                    from .business_hardware import index_word_pointer
                    from .contexts import IndexWordPointerInput
                    stack_cursor = state.push_word(stack_cursor, 528)
                    updated_audio_values_21 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 528)))
                    conditions = updated_audio_values_21.conditions
                    count_and_data = updated_audio_values_21.count_and_data
                    lookup_cursor = updated_audio_values_21.lookup_cursor
                    sample = updated_audio_values_21.sample
                    stack_cursor = updated_audio_values_21.stack_cursor
                    # source-effect driver:0210:pop
                    saved_audio_word_22, stack_cursor = state.pop_word(stack_cursor)
                    sample, conditions = high(saved_audio_word_22), low(saved_audio_word_22)
                    # source-effect driver:0211:bit
                    observed_byte_23 = state.read(u16(channel_cursor + 1))
                    conditions = state.memory_bit_conditions(observed_byte_23, 7, conditions, u16(channel_cursor + 1), True)
                    # source-effect driver:0215:jr
                    if not (not (conditions & 0x40)):
                        # source-effect driver:0217:push
                        stack_cursor = state.push_word(stack_cursor, parameter_cursor)
                        # source-effect driver:0218:ld
                        parameter_cursor = replace_high(parameter_cursor, 8)
                        # source-effect driver:021a:ld
                        parameter_cursor = replace_low(parameter_cursor, 12)
                        # source-effect driver:021c:ex
                        alternate_sample_and_conditions_24 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
                        sample, conditions = high(alternate_sample_and_conditions_24), low(alternate_sample_and_conditions_24)
                        # source-effect driver:021d:xor
                        sample = u8(sample ^ sample)
                        conditions = logic_conditions(sample, False)
                        while True:
                            # source-effect driver:021e:ex
                            alternate_sample_and_conditions_25 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
                            sample, conditions = high(alternate_sample_and_conditions_25), low(alternate_sample_and_conditions_25)
                            # source-effect driver:021f:sub
                            sample, conditions = difference_byte(sample, low(parameter_cursor))
                            # source-effect driver:0220:jr
                            if bool(conditions & 1):
                                break
                            # source-effect driver:0222:ex
                            alternate_sample_and_conditions_26 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
                            sample, conditions = high(alternate_sample_and_conditions_26), low(alternate_sample_and_conditions_26)
                            # source-effect driver:0223:add
                            arithmetic_result_27, conditions = sum_byte(sample, high(parameter_cursor))
                            sample = u8(arithmetic_result_27)
                            # source-effect driver:0224:jr
                            pass  # Static control continuation is structured below.
                            continue
                        # source-effect driver:0227:add
                        arithmetic_result_28, conditions = sum_byte(sample, low(parameter_cursor))
                        sample = u8(arithmetic_result_28)
                        # source-effect driver:0228:ld
                        lookup_cursor = u16(2416)
                        # source-effect driver:022b:rst
                        from .business_hardware import index_word_pointer
                        from .contexts import IndexWordPointerInput
                        stack_cursor = state.push_word(stack_cursor, 556)
                        updated_audio_values_29 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 556)))
                        conditions = updated_audio_values_29.conditions
                        count_and_data = updated_audio_values_29.count_and_data
                        lookup_cursor = updated_audio_values_29.lookup_cursor
                        sample = updated_audio_values_29.sample
                        stack_cursor = updated_audio_values_29.stack_cursor
                        # source-effect driver:022c:ex
                        alternate_sample_and_conditions_30 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
                        sample, conditions = high(alternate_sample_and_conditions_30), low(alternate_sample_and_conditions_30)
                        # source-effect driver:022d:or
                        sample = u8(sample | high(lookup_cursor))
                        conditions = logic_conditions(sample, False)
                        # source-effect driver:022e:ld
                        lookup_cursor = replace_high(lookup_cursor, sample)
                        # source-effect driver:022f:pop
                        saved_audio_word_31, stack_cursor = state.pop_word(stack_cursor)
                        parameter_cursor = u16(saved_audio_word_31)
                    # source-effect driver:0230:ld
                    state.write(u16(channel_cursor + 13), u8(low(lookup_cursor)))
                    # source-effect driver:0233:ld
                    state.write(u16(channel_cursor + 14), u8(high(lookup_cursor)))
                else:
                    # source-effect driver:0203:call
                    from .business_envelopes import stop_channel_note
                    from .contexts import StopChannelNoteInput
                    stack_cursor = state.push_word(stack_cursor, 518)
                    updated_audio_values_32 = stop_channel_note(state, StopChannelNoteInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 518)))
                    auxiliary_cursor = updated_audio_values_32.auxiliary_cursor
                    channel_cursor = updated_audio_values_32.channel_cursor
                    conditions = updated_audio_values_32.conditions
                    count_and_data = updated_audio_values_32.count_and_data
                    lookup_cursor = updated_audio_values_32.lookup_cursor
                    parameter_cursor = updated_audio_values_32.parameter_cursor
                    sample = updated_audio_values_32.sample
                    stack_cursor = updated_audio_values_32.stack_cursor
                    # source-effect driver:0206:jr
                    pass  # Static control continuation is structured below.
                # source-effect driver:0236:bit
                observed_byte_33 = state.read(u16(channel_cursor + 0))
                conditions = state.memory_bit_conditions(observed_byte_33, 5, conditions, u16(channel_cursor + 0), True)
                # source-effect driver:023a:jr
                if not (conditions & 0x40):
                    # source-effect driver:0249:ld
                    observed_byte_34 = state.read(parameter_cursor)
                    sample = u8(observed_byte_34)
                    # source-effect driver:024a:inc
                    parameter_cursor = u16(parameter_cursor + 1)
                    # source-effect driver:024b:ld
                    state.write(u16(channel_cursor + 16), u8(sample))
                    # source-effect driver:024e:jr
                    pass  # Static control continuation is structured below.
                    # source-effect driver:0274:ld
                    observed_byte_35 = state.read(parameter_cursor)
                    sample = u8(observed_byte_35)
                    # source-effect driver:0275:inc
                    parameter_cursor = u16(parameter_cursor + 1)
                    # source-effect driver:0276:call
                    from .business_notes import multiply_note_duration
                    from .contexts import MultiplyNoteDurationInput
                    stack_cursor = state.push_word(stack_cursor, 633)
                    updated_audio_values_36 = multiply_note_duration(state, MultiplyNoteDurationInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 633)))
                    channel_cursor = updated_audio_values_36.channel_cursor
                    conditions = updated_audio_values_36.conditions
                    count_and_data = updated_audio_values_36.count_and_data
                    sample = updated_audio_values_36.sample
                    stack_cursor = updated_audio_values_36.stack_cursor
                    # source-effect driver:0279:ld
                    state.write(u16(channel_cursor + 12), u8(sample))
                else:
                    # source-effect driver:023c:ld
                    observed_byte_37 = state.read(parameter_cursor)
                    sample = u8(observed_byte_37)
                    # source-effect driver:023d:or
                    sample = u8(sample | sample)
                    conditions = logic_conditions(sample, False)
                    # source-effect driver:023e:jp
                    if not (conditions & 0x80):
                        # source-effect driver:0275:inc
                        parameter_cursor = u16(parameter_cursor + 1)
                        # source-effect driver:0276:call
                        from .business_notes import multiply_note_duration
                        from .contexts import MultiplyNoteDurationInput
                        stack_cursor = state.push_word(stack_cursor, 633)
                        updated_audio_values_38 = multiply_note_duration(state, MultiplyNoteDurationInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 633)))
                        channel_cursor = updated_audio_values_38.channel_cursor
                        conditions = updated_audio_values_38.conditions
                        count_and_data = updated_audio_values_38.count_and_data
                        sample = updated_audio_values_38.sample
                        stack_cursor = updated_audio_values_38.stack_cursor
                        # source-effect driver:0279:ld
                        state.write(u16(channel_cursor + 12), u8(sample))
                    else:
                        # source-effect driver:0241:ld
                        observed_byte_39 = state.read(u16(channel_cursor + 12))
                        sample = u8(observed_byte_39)
                        # source-effect driver:0244:ld
                        state.write(u16(channel_cursor + 11), u8(sample))
                        # source-effect driver:0247:jr
                        pass  # Static control continuation is structured below.
        # source-effect driver:027c:ld
        state.write(u16(channel_cursor + 3), u8(low(parameter_cursor)))
        # source-effect driver:027f:ld
        state.write(u16(channel_cursor + 4), u8(high(parameter_cursor)))
        # source-effect driver:0282:ld
        observed_byte_40 = state.read(u16(channel_cursor + 12))
        sample = u8(observed_byte_40)
        # source-effect driver:0285:ld
        state.write(u16(channel_cursor + 11), u8(sample))
        # source-effect driver:0288:bit
        observed_byte_41 = state.read(u16(channel_cursor + 0))
        conditions = state.memory_bit_conditions(observed_byte_41, 1, conditions, u16(channel_cursor + 0), True)
        # source-effect driver:028c:ret
        if not (conditions & 0x40):
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return ResumeNoteParameterStreamResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
        # source-effect driver:028d:xor
        sample = u8(sample ^ sample)
        conditions = logic_conditions(sample, False)
        # source-effect driver:028e:ld
        state.write(u16(channel_cursor + 37), u8(sample))
        # source-effect driver:0291:ld
        state.write(u16(channel_cursor + 34), u8(sample))
        # source-effect driver:0294:ld
        observed_byte_42 = state.read(u16(channel_cursor + 31))
        sample = u8(observed_byte_42)
        # source-effect driver:0297:ld
        state.write(u16(channel_cursor + 30), u8(sample))
        # source-effect driver:029a:ld
        state.write(u16(channel_cursor + 23), u8(sample))
        # source-effect driver:029d:ret
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return ResumeNoteParameterStreamResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
