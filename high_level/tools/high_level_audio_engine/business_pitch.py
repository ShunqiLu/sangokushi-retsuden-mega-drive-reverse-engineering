"""Channel frequency placement, pitch calculation and modulation state.

Intermediate recovered algorithms; no CPU/timing or natural playback proof.
Live bus/stack aliases and original nonlocal returns remain unchanged.
"""
from .domain import (AudioState, AudioBoundary, Continuation, AlternateGroup, checked_state, u8, u16, low, high, replace_low, replace_high, logic_conditions, sum_byte, difference_byte, comparison_conditions, increment_byte, decrement_byte, sum_word, difference_word, tested_bit_conditions, copy_byte_conditions)
from .contexts import (WriteChannelFrequencyInput, WriteChannelFrequencyResult, ChooseFrequencyScratchBlockInput, ChooseFrequencyScratchBlockResult, InitializePitchModulationInput, InitializePitchModulationResult, UpdatePitchModulationInput, UpdatePitchModulationResult, CalculateChannelPitchInput, CalculateChannelPitchResult)

def write_channel_frequency(state: AudioState, inputs: WriteChannelFrequencyInput) -> WriteChannelFrequencyResult:
    """Write channel frequency."""
    checked_state(state)
    if type(inputs) is not WriteChannelFrequencyInput:
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
    # source-effect driver:017e:bit
    observed_byte_1 = state.read(u16(channel_cursor + 0))
    conditions = state.memory_bit_conditions(observed_byte_1, 2, conditions, u16(channel_cursor + 0), True)
    # source-effect driver:0182:ret
    if not (conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return WriteChannelFrequencyResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0183:bit
    observed_byte_2 = state.read(u16(channel_cursor + 0))
    conditions = state.memory_bit_conditions(observed_byte_2, 0, conditions, u16(channel_cursor + 0), True)
    # source-effect driver:0187:jp
    if not (conditions & 0x40):
        # source-effect driver:0193:ld
        observed_byte_3 = state.read(u16(channel_cursor + 1))
        sample = u8(observed_byte_3)
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
            updated_audio_values_4 = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 398)))
            channel_cursor = updated_audio_values_4.channel_cursor
            conditions = updated_audio_values_4.conditions
            count_and_data = updated_audio_values_4.count_and_data
            sample = updated_audio_values_4.sample
            stack_cursor = updated_audio_values_4.stack_cursor
            # source-effect driver:018e:ld
            sample = u8(160)
            # source-effect driver:0190:ld
            count_and_data = replace_low(count_and_data, low(lookup_cursor))
            # source-effect driver:0191:rst
            from .business_hardware import write_channel_fm_register
            from .contexts import WriteChannelFmRegisterInput
            stack_cursor = state.push_word(stack_cursor, 402)
            updated_audio_values_5 = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 402)))
            channel_cursor = updated_audio_values_5.channel_cursor
            conditions = updated_audio_values_5.conditions
            count_and_data = updated_audio_values_5.count_and_data
            sample = updated_audio_values_5.sample
            stack_cursor = updated_audio_values_5.stack_cursor
            # source-effect driver:0192:ret
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return WriteChannelFrequencyResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
        else:
            # source-effect driver:019a:call
            from .business_pitch import choose_frequency_scratch_block
            from .contexts import ChooseFrequencyScratchBlockInput
            stack_cursor = state.push_word(stack_cursor, 413)
            updated_audio_values_6 = choose_frequency_scratch_block(state, ChooseFrequencyScratchBlockInput(conditions=conditions, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 413)))
            conditions = updated_audio_values_6.conditions
            parameter_cursor = updated_audio_values_6.parameter_cursor
            sample = updated_audio_values_6.sample
            stack_cursor = updated_audio_values_6.stack_cursor
            # source-effect driver:019d:exx
            alternate_group_7 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
            alternate_group_7.validate()
            count_and_data, parameter_cursor, lookup_cursor = alternate_group_7.count_and_data, alternate_group_7.parameter_cursor, alternate_group_7.lookup_cursor
            # source-effect driver:019e:ld
            lookup_cursor = u16(450)
            # source-effect driver:01a1:ld
            count_and_data = replace_high(count_and_data, 4)
            while True:
                # source-effect driver:01a3:ld
                observed_byte_8 = state.read(lookup_cursor)
                sample = u8(observed_byte_8)
                # source-effect driver:01a4:push
                stack_cursor = state.push_word(stack_cursor, ((sample << 8) | conditions))
                # source-effect driver:01a5:inc
                lookup_cursor = u16(lookup_cursor + 1)
                # source-effect driver:01a6:exx
                alternate_group_9 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
                alternate_group_9.validate()
                count_and_data, parameter_cursor, lookup_cursor = alternate_group_9.count_and_data, alternate_group_9.parameter_cursor, alternate_group_9.lookup_cursor
                # source-effect driver:01a7:ex
                parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
                # source-effect driver:01a8:ld
                observed_byte_10 = state.read(lookup_cursor)
                count_and_data = replace_low(count_and_data, observed_byte_10)
                # source-effect driver:01a9:inc
                lookup_cursor = u16(lookup_cursor + 1)
                # source-effect driver:01aa:ld
                observed_byte_11 = state.read(lookup_cursor)
                count_and_data = replace_high(count_and_data, observed_byte_11)
                # source-effect driver:01ab:inc
                lookup_cursor = u16(lookup_cursor + 1)
                # source-effect driver:01ac:ex
                parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
                # source-effect driver:01ad:ld
                observed_byte_12 = state.read(u16(channel_cursor + 13))
                lookup_cursor = replace_low(lookup_cursor, observed_byte_12)
                # source-effect driver:01b0:ld
                observed_byte_13 = state.read(u16(channel_cursor + 14))
                lookup_cursor = replace_high(lookup_cursor, observed_byte_13)
                # source-effect driver:01b3:add
                arithmetic_result_14, conditions = sum_word(lookup_cursor, count_and_data, conditions)
                lookup_cursor = u16(arithmetic_result_14)
                # source-effect driver:01b4:pop
                saved_audio_word_15, stack_cursor = state.pop_word(stack_cursor)
                sample, conditions = high(saved_audio_word_15), low(saved_audio_word_15)
                # source-effect driver:01b5:push
                stack_cursor = state.push_word(stack_cursor, ((sample << 8) | conditions))
                # source-effect driver:01b6:ld
                count_and_data = replace_low(count_and_data, high(lookup_cursor))
                # source-effect driver:01b7:rst
                from .business_hardware import write_fm_port_zero_entry
                from .contexts import WriteFmPortZeroEntryInput
                stack_cursor = state.push_word(stack_cursor, 440)
                updated_audio_values_16 = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 440)))
                channel_cursor = updated_audio_values_16.channel_cursor
                conditions = updated_audio_values_16.conditions
                count_and_data = updated_audio_values_16.count_and_data
                sample = updated_audio_values_16.sample
                stack_cursor = updated_audio_values_16.stack_cursor
                # source-effect driver:01b8:pop
                saved_audio_word_17, stack_cursor = state.pop_word(stack_cursor)
                sample, conditions = high(saved_audio_word_17), low(saved_audio_word_17)
                # source-effect driver:01b9:sub
                sample, conditions = difference_byte(sample, 4)
                # source-effect driver:01bb:ld
                count_and_data = replace_low(count_and_data, low(lookup_cursor))
                # source-effect driver:01bc:rst
                from .business_hardware import write_fm_port_zero_entry
                from .contexts import WriteFmPortZeroEntryInput
                stack_cursor = state.push_word(stack_cursor, 445)
                updated_audio_values_18 = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 445)))
                channel_cursor = updated_audio_values_18.channel_cursor
                conditions = updated_audio_values_18.conditions
                count_and_data = updated_audio_values_18.count_and_data
                sample = updated_audio_values_18.sample
                stack_cursor = updated_audio_values_18.stack_cursor
                # source-effect driver:01bd:exx
                alternate_group_19 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
                alternate_group_19.validate()
                count_and_data, parameter_cursor, lookup_cursor = alternate_group_19.count_and_data, alternate_group_19.parameter_cursor, alternate_group_19.lookup_cursor
                # source-effect driver:01be:djnz
                count_and_data = replace_high(count_and_data, u8(high(count_and_data) - 1))
                if high(count_and_data) != 0:
                    continue
                break
            # source-effect driver:01c0:exx
            alternate_group_20 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
            alternate_group_20.validate()
            count_and_data, parameter_cursor, lookup_cursor = alternate_group_20.count_and_data, alternate_group_20.parameter_cursor, alternate_group_20.lookup_cursor
            # source-effect driver:01c1:ret
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return WriteChannelFrequencyResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    else:
        # source-effect driver:018a:ld
        sample = u8(164)
        # source-effect driver:018c:ld
        count_and_data = replace_low(count_and_data, high(lookup_cursor))
        # source-effect driver:018d:rst
        from .business_hardware import write_channel_fm_register
        from .contexts import WriteChannelFmRegisterInput
        stack_cursor = state.push_word(stack_cursor, 398)
        updated_audio_values_21 = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 398)))
        channel_cursor = updated_audio_values_21.channel_cursor
        conditions = updated_audio_values_21.conditions
        count_and_data = updated_audio_values_21.count_and_data
        sample = updated_audio_values_21.sample
        stack_cursor = updated_audio_values_21.stack_cursor
        # source-effect driver:018e:ld
        sample = u8(160)
        # source-effect driver:0190:ld
        count_and_data = replace_low(count_and_data, low(lookup_cursor))
        # source-effect driver:0191:rst
        from .business_hardware import write_channel_fm_register
        from .contexts import WriteChannelFmRegisterInput
        stack_cursor = state.push_word(stack_cursor, 402)
        updated_audio_values_22 = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 402)))
        channel_cursor = updated_audio_values_22.channel_cursor
        conditions = updated_audio_values_22.conditions
        count_and_data = updated_audio_values_22.count_and_data
        sample = updated_audio_values_22.sample
        stack_cursor = updated_audio_values_22.stack_cursor
        # source-effect driver:0192:ret
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return WriteChannelFrequencyResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def choose_frequency_scratch_block(state: AudioState, inputs: ChooseFrequencyScratchBlockInput) -> ChooseFrequencyScratchBlockResult:
    """Choose frequency scratch block."""
    checked_state(state)
    if type(inputs) is not ChooseFrequencyScratchBlockInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    conditions = inputs.conditions
    parameter_cursor = inputs.parameter_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:01c6:ld
    parameter_cursor = u16(7210)
    # source-effect driver:01c9:ld
    observed_byte_1 = state.read(7193)
    sample = u8(observed_byte_1)
    # source-effect driver:01cc:or
    sample = u8(sample | sample)
    conditions = logic_conditions(sample, False)
    # source-effect driver:01cd:ret
    if bool(conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return ChooseFrequencyScratchBlockResult(conditions=conditions, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:01ce:ld
    parameter_cursor = u16(7194)
    # source-effect driver:01d1:ret
    if not (conditions & 0x80):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return ChooseFrequencyScratchBlockResult(conditions=conditions, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:01d2:ld
    parameter_cursor = u16(7202)
    # source-effect driver:01d5:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return ChooseFrequencyScratchBlockResult(conditions=conditions, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def initialize_pitch_modulation(state: AudioState, inputs: InitializePitchModulationInput) -> InitializePitchModulationResult:
    """Initialize pitch modulation."""
    checked_state(state)
    if type(inputs) is not InitializePitchModulationInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    channel_cursor = inputs.channel_cursor
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    lookup_cursor = inputs.lookup_cursor
    parameter_cursor = inputs.parameter_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:033b:bit
    observed_byte_1 = state.read(u16(channel_cursor + 7))
    conditions = state.memory_bit_conditions(observed_byte_1, 7, conditions, u16(channel_cursor + 7), True)
    # source-effect driver:033f:ret
    if bool(conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return InitializePitchModulationResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0340:bit
    observed_byte_2 = state.read(u16(channel_cursor + 0))
    conditions = state.memory_bit_conditions(observed_byte_2, 1, conditions, u16(channel_cursor + 0), True)
    # source-effect driver:0344:ret
    if not (conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return InitializePitchModulationResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0345:ld
    observed_byte_3 = state.read(u16(channel_cursor + 32))
    parameter_cursor = replace_low(parameter_cursor, observed_byte_3)
    # source-effect driver:0348:ld
    observed_byte_4 = state.read(u16(channel_cursor + 33))
    parameter_cursor = replace_high(parameter_cursor, observed_byte_4)
    # source-effect driver:034b:push
    stack_cursor = state.push_word(stack_cursor, channel_cursor)
    # source-effect driver:034d:pop
    saved_audio_word_5, stack_cursor = state.pop_word(stack_cursor)
    lookup_cursor = u16(saved_audio_word_5)
    # source-effect driver:034e:ld
    count_and_data = replace_high(count_and_data, 0)
    # source-effect driver:0350:ld
    count_and_data = replace_low(count_and_data, 36)
    # source-effect driver:0352:add
    arithmetic_result_6, conditions = sum_word(lookup_cursor, count_and_data, conditions)
    lookup_cursor = u16(arithmetic_result_6)
    # source-effect driver:0353:ex
    parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
    # source-effect driver:0354:ldi
    copied_byte = state.read(lookup_cursor)
    state.write(parameter_cursor, copied_byte)
    lookup_cursor = u16(lookup_cursor + 1)
    parameter_cursor = u16(parameter_cursor + 1)
    count_and_data = u16(count_and_data - 1)
    conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
    # source-effect driver:0356:ldi
    copied_byte = state.read(lookup_cursor)
    state.write(parameter_cursor, copied_byte)
    lookup_cursor = u16(lookup_cursor + 1)
    parameter_cursor = u16(parameter_cursor + 1)
    count_and_data = u16(count_and_data - 1)
    conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
    # source-effect driver:0358:ldi
    copied_byte = state.read(lookup_cursor)
    state.write(parameter_cursor, copied_byte)
    lookup_cursor = u16(lookup_cursor + 1)
    parameter_cursor = u16(parameter_cursor + 1)
    count_and_data = u16(count_and_data - 1)
    conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
    # source-effect driver:035a:ld
    observed_byte_7 = state.read(lookup_cursor)
    sample = u8(observed_byte_7)
    # source-effect driver:035b:srl
    shifted_byte_8 = sample
    shift_result_9 = u8((shifted_byte_8 >> 1))
    conditions = logic_conditions(shift_result_9) | (shifted_byte_8 & 1)
    sample = u8(shift_result_9)
    # source-effect driver:035d:ld
    state.write(parameter_cursor, u8(sample))
    # source-effect driver:035e:xor
    sample = u8(sample ^ sample)
    conditions = logic_conditions(sample, False)
    # source-effect driver:035f:ld
    state.write(u16(channel_cursor + 34), u8(sample))
    # source-effect driver:0362:ld
    state.write(u16(channel_cursor + 35), u8(sample))
    # source-effect driver:0365:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return InitializePitchModulationResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def update_pitch_modulation(state: AudioState, inputs: UpdatePitchModulationInput) -> UpdatePitchModulationResult:
    """Update pitch modulation."""
    checked_state(state)
    if type(inputs) is not UpdatePitchModulationInput:
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
    # source-effect driver:0366:ld
    observed_byte_1 = state.read(u16(channel_cursor + 7))
    sample = u8(observed_byte_1)
    # source-effect driver:0369:or
    sample = u8(sample | sample)
    conditions = logic_conditions(sample, False)
    # source-effect driver:036a:ret
    if bool(conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return UpdatePitchModulationResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:036b:cp
    conditions = comparison_conditions(sample, 128)
    # source-effect driver:036d:jr
    if not (conditions & 0x40):
        # source-effect driver:03b7:dec
        changed_byte_2, conditions = decrement_byte(sample, conditions)
        sample = u8(changed_byte_2)
        # source-effect driver:03b8:ex
        parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
        # source-effect driver:03b9:ld
        count_and_data = replace_low(count_and_data, 8)
        # source-effect driver:03bb:rst
        from .business_hardware import lookup_banked_root_pointer
        from .contexts import LookupBankedRootPointerInput
        stack_cursor = state.push_word(stack_cursor, 956)
        updated_audio_values_3 = lookup_banked_root_pointer(state, LookupBankedRootPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 956)))
        conditions = updated_audio_values_3.conditions
        count_and_data = updated_audio_values_3.count_and_data
        lookup_cursor = updated_audio_values_3.lookup_cursor
        sample = updated_audio_values_3.sample
        stack_cursor = updated_audio_values_3.stack_cursor
        # source-effect driver:03bc:rst
        from .business_hardware import index_word_pointer
        from .contexts import IndexWordPointerInput
        stack_cursor = state.push_word(stack_cursor, 957)
        updated_audio_values_4 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 957)))
        conditions = updated_audio_values_4.conditions
        count_and_data = updated_audio_values_4.count_and_data
        lookup_cursor = updated_audio_values_4.lookup_cursor
        sample = updated_audio_values_4.sample
        stack_cursor = updated_audio_values_4.stack_cursor
        # source-effect driver:03bd:jr
        pass  # Static control continuation is structured below.
        while True:
            # source-effect driver:03c2:push
            stack_cursor = state.push_word(stack_cursor, lookup_cursor)
            # source-effect driver:03c3:ld
            observed_byte_5 = state.read(u16(channel_cursor + 37))
            count_and_data = replace_low(count_and_data, observed_byte_5)
            # source-effect driver:03c6:call
            from .business_voice import read_indexed_envelope
            from .contexts import ReadIndexedEnvelopeInput
            stack_cursor = state.push_word(stack_cursor, 969)
            updated_audio_values_6 = read_indexed_envelope(state, ReadIndexedEnvelopeInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 969)))
            conditions = updated_audio_values_6.conditions
            count_and_data = updated_audio_values_6.count_and_data
            lookup_cursor = updated_audio_values_6.lookup_cursor
            sample = updated_audio_values_6.sample
            stack_cursor = updated_audio_values_6.stack_cursor
            # source-effect driver:03c9:pop
            saved_audio_word_7, stack_cursor = state.pop_word(stack_cursor)
            lookup_cursor = u16(saved_audio_word_7)
            # source-effect driver:03ca:bit
            conditions = tested_bit_conditions(sample, 7, conditions)
            # source-effect driver:03cc:jp
            if bool(conditions & 0x40):
                # source-effect driver:03fc:ld
                lookup_cursor = replace_high(lookup_cursor, 0)
                # source-effect driver:03fe:ld
                lookup_cursor = replace_low(lookup_cursor, sample)
                # source-effect driver:03ff:ld
                observed_byte_8 = state.read(u16(channel_cursor + 34))
                count_and_data = replace_high(count_and_data, observed_byte_8)
                # source-effect driver:0402:inc
                changed_byte_9, conditions = increment_byte(high(count_and_data), conditions)
                count_and_data = replace_high(count_and_data, changed_byte_9)
                # source-effect driver:0403:ex
                parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
                while True:
                    # source-effect driver:0404:add
                    arithmetic_result_10, conditions = sum_word(lookup_cursor, parameter_cursor, conditions)
                    lookup_cursor = u16(arithmetic_result_10)
                    # source-effect driver:0405:djnz
                    count_and_data = replace_high(count_and_data, u8(high(count_and_data) - 1))
                    if high(count_and_data) != 0:
                        continue
                    break
                # source-effect driver:0407:inc
                observed_byte_11 = state.read(u16(channel_cursor + 37))
                changed_byte_12, conditions = increment_byte(observed_byte_11, conditions)
                state.write(u16(channel_cursor + 37), u8(changed_byte_12))
                # source-effect driver:040a:ret
                stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
                return UpdatePitchModulationResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
                break
            # source-effect driver:03cf:cp
            conditions = comparison_conditions(sample, 130)
            # source-effect driver:03d1:jr
            if bool(conditions & 0x40):
                # source-effect driver:03e5:inc
                count_and_data = u16(count_and_data + 1)
                # source-effect driver:03e6:ld
                observed_byte_13 = state.read(count_and_data)
                sample = u8(observed_byte_13)
                # source-effect driver:03e7:jr
                pass  # Static control continuation is structured below.
                # source-effect driver:03bf:ld
                state.write(u16(channel_cursor + 37), u8(sample))
                continue
            else:
                # source-effect driver:03d3:cp
                conditions = comparison_conditions(sample, 128)
                # source-effect driver:03d5:jr
                if bool(conditions & 0x40):
                    # source-effect driver:03e9:xor
                    sample = u8(sample ^ sample)
                    conditions = logic_conditions(sample, False)
                    # source-effect driver:03ea:jr
                    pass  # Static control continuation is structured below.
                    # source-effect driver:03bf:ld
                    state.write(u16(channel_cursor + 37), u8(sample))
                    continue
                else:
                    # source-effect driver:03d7:cp
                    conditions = comparison_conditions(sample, 132)
                    # source-effect driver:03d9:jr
                    if not (bool(conditions & 0x40)):
                        break
                    # source-effect driver:03ec:inc
                    count_and_data = u16(count_and_data + 1)
                    # source-effect driver:03ed:ld
                    observed_byte_14 = state.read(count_and_data)
                    sample = u8(observed_byte_14)
                    # source-effect driver:03ee:add
                    observed_byte_15 = state.read(u16(channel_cursor + 34))
                    arithmetic_result_16, conditions = sum_byte(sample, observed_byte_15)
                    sample = u8(arithmetic_result_16)
                    # source-effect driver:03f1:ld
                    state.write(u16(channel_cursor + 34), u8(sample))
                    # source-effect driver:03f4:inc
                    observed_byte_17 = state.read(u16(channel_cursor + 37))
                    changed_byte_18, conditions = increment_byte(observed_byte_17, conditions)
                    state.write(u16(channel_cursor + 37), u8(changed_byte_18))
                    # source-effect driver:03f7:inc
                    observed_byte_19 = state.read(u16(channel_cursor + 37))
                    changed_byte_20, conditions = increment_byte(observed_byte_19, conditions)
                    state.write(u16(channel_cursor + 37), u8(changed_byte_20))
                    # source-effect driver:03fa:jr
                    pass  # Static control continuation is structured below.
                    continue
            raise AudioBoundary("unbound static continuation driver:None")
            break
        # source-effect driver:03db:ld
        lookup_cursor = replace_high(lookup_cursor, 255)
        # source-effect driver:03dd:jr
        if not (conditions & 1):
            # source-effect driver:03fe:ld
            lookup_cursor = replace_low(lookup_cursor, sample)
            # source-effect driver:03ff:ld
            observed_byte_21 = state.read(u16(channel_cursor + 34))
            count_and_data = replace_high(count_and_data, observed_byte_21)
            # source-effect driver:0402:inc
            changed_byte_22, conditions = increment_byte(high(count_and_data), conditions)
            count_and_data = replace_high(count_and_data, changed_byte_22)
            # source-effect driver:0403:ex
            parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
            while True:
                # source-effect driver:0404:add
                arithmetic_result_23, conditions = sum_word(lookup_cursor, parameter_cursor, conditions)
                lookup_cursor = u16(arithmetic_result_23)
                # source-effect driver:0405:djnz
                count_and_data = replace_high(count_and_data, u8(high(count_and_data) - 1))
                if high(count_and_data) != 0:
                    continue
                break
            # source-effect driver:0407:inc
            observed_byte_24 = state.read(u16(channel_cursor + 37))
            changed_byte_25, conditions = increment_byte(observed_byte_24, conditions)
            state.write(u16(channel_cursor + 37), u8(changed_byte_25))
            # source-effect driver:040a:ret
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return UpdatePitchModulationResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
        else:
            # source-effect driver:03df:set
            observed_byte_26 = state.read(u16(channel_cursor + 0))
            state.write(u16(channel_cursor + 0), u8(observed_byte_26 | 64))
            # source-effect driver:03e3:pop
            saved_audio_word_27, stack_cursor = state.pop_word(stack_cursor)
            lookup_cursor = u16(saved_audio_word_27)
            # source-effect driver:03e4:ret
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return UpdatePitchModulationResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    else:
        # source-effect driver:036f:dec
        observed_byte_28 = state.read(u16(channel_cursor + 36))
        changed_byte_29, conditions = decrement_byte(observed_byte_28, conditions)
        state.write(u16(channel_cursor + 36), u8(changed_byte_29))
        # source-effect driver:0372:ret
        if not (conditions & 0x40):
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return UpdatePitchModulationResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
        # source-effect driver:0373:inc
        observed_byte_30 = state.read(u16(channel_cursor + 36))
        changed_byte_31, conditions = increment_byte(observed_byte_30, conditions)
        state.write(u16(channel_cursor + 36), u8(changed_byte_31))
        # source-effect driver:0376:push
        stack_cursor = state.push_word(stack_cursor, lookup_cursor)
        # source-effect driver:0377:ld
        observed_byte_32 = state.read(u16(channel_cursor + 34))
        lookup_cursor = replace_low(lookup_cursor, observed_byte_32)
        # source-effect driver:037a:ld
        observed_byte_33 = state.read(u16(channel_cursor + 35))
        lookup_cursor = replace_high(lookup_cursor, observed_byte_33)
        # source-effect driver:037d:dec
        observed_byte_34 = state.read(u16(channel_cursor + 37))
        changed_byte_35, conditions = decrement_byte(observed_byte_34, conditions)
        state.write(u16(channel_cursor + 37), u8(changed_byte_35))
        # source-effect driver:0380:jr
        if not (not (conditions & 0x40)):
            # source-effect driver:0382:ld
            observed_byte_36 = state.read(u16(channel_cursor + 32))
            parameter_cursor = replace_low(parameter_cursor, observed_byte_36)
            # source-effect driver:0385:ld
            observed_byte_37 = state.read(u16(channel_cursor + 33))
            parameter_cursor = replace_high(parameter_cursor, observed_byte_37)
            # source-effect driver:0388:push
            stack_cursor = state.push_word(stack_cursor, parameter_cursor)
            # source-effect driver:0389:pop
            saved_audio_word_38, stack_cursor = state.pop_word(stack_cursor)
            auxiliary_cursor = u16(saved_audio_word_38)
            # source-effect driver:038b:ld
            observed_byte_39 = state.read(u16(auxiliary_cursor + 1))
            sample = u8(observed_byte_39)
            # source-effect driver:038e:ld
            state.write(u16(channel_cursor + 37), u8(sample))
            # source-effect driver:0391:ld
            observed_byte_40 = state.read(u16(channel_cursor + 38))
            sample = u8(observed_byte_40)
            # source-effect driver:0394:ld
            count_and_data = replace_low(count_and_data, sample)
            # source-effect driver:0395:and
            sample = u8(sample & 128)
            conditions = logic_conditions(sample, True)
            # source-effect driver:0397:rlca
            rotated_sample_41 = sample
            sample = u8((rotated_sample_41 << 1) | (rotated_sample_41 >> 7))
            conditions = (conditions & 0xC4) | (sample & 0x28) | (rotated_sample_41 >> 7)
            # source-effect driver:0398:neg
            sample, conditions = difference_byte(0, sample)
            # source-effect driver:039a:ld
            count_and_data = replace_high(count_and_data, sample)
            # source-effect driver:039b:add
            arithmetic_result_42, conditions = sum_word(lookup_cursor, count_and_data, conditions)
            lookup_cursor = u16(arithmetic_result_42)
            # source-effect driver:039c:ld
            state.write(u16(channel_cursor + 34), u8(low(lookup_cursor)))
            # source-effect driver:039f:ld
            state.write(u16(channel_cursor + 35), u8(high(lookup_cursor)))
        # source-effect driver:03a2:pop
        saved_audio_word_43, stack_cursor = state.pop_word(stack_cursor)
        count_and_data = u16(saved_audio_word_43)
        # source-effect driver:03a3:add
        arithmetic_result_44, conditions = sum_word(lookup_cursor, count_and_data, conditions)
        lookup_cursor = u16(arithmetic_result_44)
        # source-effect driver:03a4:dec
        observed_byte_45 = state.read(u16(channel_cursor + 39))
        changed_byte_46, conditions = decrement_byte(observed_byte_45, conditions)
        state.write(u16(channel_cursor + 39), u8(changed_byte_46))
        # source-effect driver:03a7:ret
        if not (conditions & 0x40):
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return UpdatePitchModulationResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
        # source-effect driver:03a8:ld
        observed_byte_47 = state.read(u16(auxiliary_cursor + 3))
        sample = u8(observed_byte_47)
        # source-effect driver:03ab:ld
        state.write(u16(channel_cursor + 39), u8(sample))
        # source-effect driver:03ae:ld
        observed_byte_48 = state.read(u16(channel_cursor + 38))
        sample = u8(observed_byte_48)
        # source-effect driver:03b1:neg
        sample, conditions = difference_byte(0, sample)
        # source-effect driver:03b3:ld
        state.write(u16(channel_cursor + 38), u8(sample))
        # source-effect driver:03b6:ret
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return UpdatePitchModulationResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def calculate_channel_pitch(state: AudioState, inputs: CalculateChannelPitchInput) -> CalculateChannelPitchResult:
    """Calculate channel pitch."""
    checked_state(state)
    if type(inputs) is not CalculateChannelPitchInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    channel_cursor = inputs.channel_cursor
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    lookup_cursor = inputs.lookup_cursor
    parameter_cursor = inputs.parameter_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:0432:ld
    count_and_data = replace_high(count_and_data, 0)
    # source-effect driver:0434:ld
    observed_byte_1 = state.read(u16(channel_cursor + 16))
    sample = u8(observed_byte_1)
    # source-effect driver:0437:or
    sample = u8(sample | sample)
    conditions = logic_conditions(sample, False)
    # source-effect driver:0438:jp
    if not (not (conditions & 0x80)):
        # source-effect driver:043b:dec
        changed_byte_2, conditions = decrement_byte(high(count_and_data), conditions)
        count_and_data = replace_high(count_and_data, changed_byte_2)
    # source-effect driver:043c:ld
    observed_byte_3 = state.read(u16(channel_cursor + 14))
    lookup_cursor = replace_high(lookup_cursor, observed_byte_3)
    # source-effect driver:043f:ld
    observed_byte_4 = state.read(u16(channel_cursor + 13))
    lookup_cursor = replace_low(lookup_cursor, observed_byte_4)
    # source-effect driver:0442:ld
    count_and_data = replace_low(count_and_data, sample)
    # source-effect driver:0443:add
    arithmetic_result_5, conditions = sum_word(lookup_cursor, count_and_data, conditions)
    lookup_cursor = u16(arithmetic_result_5)
    # source-effect driver:0444:bit
    observed_byte_6 = state.read(u16(channel_cursor + 1))
    conditions = state.memory_bit_conditions(observed_byte_6, 7, conditions, u16(channel_cursor + 1), True)
    # source-effect driver:0448:jr
    if not (not (conditions & 0x40)):
        # source-effect driver:044a:ex
        parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
        # source-effect driver:044b:ld
        sample = u8(7)
        # source-effect driver:044d:and
        sample = u8(sample & high(parameter_cursor))
        conditions = logic_conditions(sample, True)
        # source-effect driver:044e:ld
        count_and_data = replace_high(count_and_data, sample)
        # source-effect driver:044f:ld
        count_and_data = replace_low(count_and_data, low(parameter_cursor))
        # source-effect driver:0450:or
        sample = u8(sample | sample)
        conditions = logic_conditions(sample, False)
        # source-effect driver:0451:ld
        lookup_cursor = u16(643)
        # source-effect driver:0454:sbc
        arithmetic_result_7, conditions = difference_word(lookup_cursor, count_and_data, conditions)
        lookup_cursor = u16(arithmetic_result_7)
        # source-effect driver:0456:jr
        if bool(conditions & 1):
            # source-effect driver:045e:or
            sample = u8(sample | sample)
            conditions = logic_conditions(sample, False)
            # source-effect driver:045f:ld
            lookup_cursor = u16(1288)
            # source-effect driver:0462:sbc
            arithmetic_result_8, conditions = difference_word(lookup_cursor, count_and_data, conditions)
            lookup_cursor = u16(arithmetic_result_8)
            # source-effect driver:0464:jr
            if not (not (conditions & 1)):
                # source-effect driver:0466:ld
                lookup_cursor = u16(1404)
                # source-effect driver:0469:add
                arithmetic_result_9, conditions = sum_word(lookup_cursor, parameter_cursor, conditions)
                lookup_cursor = u16(arithmetic_result_9)
                # source-effect driver:046a:ex
                parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
            # source-effect driver:046b:ex
            parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
        else:
            # source-effect driver:0458:ld
            lookup_cursor = u16(64133)
            # source-effect driver:045b:add
            arithmetic_result_10, conditions = sum_word(lookup_cursor, parameter_cursor, conditions)
            lookup_cursor = u16(arithmetic_result_10)
            # source-effect driver:045c:jr
            pass  # Static control continuation is structured below.
    # source-effect driver:046c:bit
    observed_byte_11 = state.read(u16(channel_cursor + 0))
    conditions = state.memory_bit_conditions(observed_byte_11, 5, conditions, u16(channel_cursor + 0), True)
    # source-effect driver:0470:ret
    if bool(conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return CalculateChannelPitchResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0471:ld
    state.write(u16(channel_cursor + 14), u8(high(lookup_cursor)))
    # source-effect driver:0474:ld
    state.write(u16(channel_cursor + 13), u8(low(lookup_cursor)))
    # source-effect driver:0477:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return CalculateChannelPitchResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
