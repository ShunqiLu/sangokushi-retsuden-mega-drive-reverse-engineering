"""Stereo-pan pattern state and its shared resume entry.

Intermediate recovered algorithms; no CPU/timing or natural playback proof.
Live bus/stack aliases and original nonlocal returns remain unchanged.
"""
from .domain import (AudioState, Continuation, AlternateGroup, checked_state, u8, u16, low, replace_low, replace_high, logic_conditions, difference_byte, comparison_conditions, increment_byte, decrement_byte, sum_word)
from .contexts import (UpdatePanPatternInput, UpdatePanPatternResult, ResumePanPatternInput, ResumePanPatternResult)

def update_pan_pattern(state: AudioState, inputs: UpdatePanPatternInput) -> UpdatePanPatternResult:
    """Update pan pattern."""
    checked_state(state)
    if type(inputs) is not UpdatePanPatternInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    channel_cursor = inputs.channel_cursor
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    lookup_cursor = inputs.lookup_cursor
    parameter_cursor = inputs.parameter_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:02a8:ld
    observed_byte_1 = state.read(u16(channel_cursor + 17))
    sample = u8(observed_byte_1)
    # source-effect driver:02ab:dec
    changed_byte_2, conditions = decrement_byte(sample, conditions)
    sample = u8(changed_byte_2)
    # source-effect driver:02ac:ret
    if bool(conditions & 0x80):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return UpdatePanPatternResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:02ad:jr
    if not (conditions & 0x40):
        # source-effect driver:02ea:xor
        sample = u8(sample ^ sample)
        conditions = logic_conditions(sample, False)
        # source-effect driver:02eb:ld
        state.write(u16(channel_cursor + 19), u8(sample))
        # source-effect driver:02ee:ld
        observed_byte_3 = state.read(u16(channel_cursor + 17))
        sample = u8(observed_byte_3)
        # source-effect driver:02f1:sub
        sample, conditions = difference_byte(sample, 2)
        # source-effect driver:02f3:ret
        if bool(conditions & 0x80):
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return UpdatePanPatternResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
        # source-effect driver:02f4:jr
        pass  # Static control continuation is structured below.
        # source-effect driver:02b4:dec
        observed_byte_4 = state.read(u16(channel_cursor + 22))
        changed_byte_5, conditions = decrement_byte(observed_byte_4, conditions)
        state.write(u16(channel_cursor + 22), u8(changed_byte_5))
        # source-effect driver:02b7:ret
        if not (conditions & 0x40):
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return UpdatePanPatternResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
        # source-effect driver:02b8:exx
        alternate_group_6 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
        alternate_group_6.validate()
        count_and_data, parameter_cursor, lookup_cursor = alternate_group_6.count_and_data, alternate_group_6.parameter_cursor, alternate_group_6.lookup_cursor
        # source-effect driver:02b9:ld
        observed_byte_7 = state.read(u16(channel_cursor + 21))
        sample = u8(observed_byte_7)
        # source-effect driver:02bc:ld
        state.write(u16(channel_cursor + 22), u8(sample))
        # source-effect driver:02bf:ld
        observed_byte_8 = state.read(u16(channel_cursor + 18))
        sample = u8(observed_byte_8)
        # source-effect driver:02c2:ld
        lookup_cursor = u16(758)
        # source-effect driver:02c5:rst
        from .business_hardware import index_word_pointer
        from .contexts import IndexWordPointerInput
        stack_cursor = state.push_word(stack_cursor, 710)
        updated_audio_values_9 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 710)))
        conditions = updated_audio_values_9.conditions
        count_and_data = updated_audio_values_9.count_and_data
        lookup_cursor = updated_audio_values_9.lookup_cursor
        sample = updated_audio_values_9.sample
        stack_cursor = updated_audio_values_9.stack_cursor
        # source-effect driver:02c6:ld
        observed_byte_10 = state.read(u16(channel_cursor + 19))
        parameter_cursor = replace_low(parameter_cursor, observed_byte_10)
        # source-effect driver:02c9:inc
        observed_byte_11 = state.read(u16(channel_cursor + 19))
        changed_byte_12, conditions = increment_byte(observed_byte_11, conditions)
        state.write(u16(channel_cursor + 19), u8(changed_byte_12))
        # source-effect driver:02cc:ld
        observed_byte_13 = state.read(u16(channel_cursor + 20))
        sample = u8(observed_byte_13)
        # source-effect driver:02cf:dec
        changed_byte_14, conditions = decrement_byte(sample, conditions)
        sample = u8(changed_byte_14)
        # source-effect driver:02d0:cp
        conditions = comparison_conditions(sample, low(parameter_cursor))
        # source-effect driver:02d1:jr
        if not (not (conditions & 0x40)):
            # source-effect driver:02d3:dec
            observed_byte_15 = state.read(u16(channel_cursor + 19))
            changed_byte_16, conditions = decrement_byte(observed_byte_15, conditions)
            state.write(u16(channel_cursor + 19), u8(changed_byte_16))
            # source-effect driver:02d6:ld
            observed_byte_17 = state.read(u16(channel_cursor + 17))
            sample = u8(observed_byte_17)
            # source-effect driver:02d9:cp
            conditions = comparison_conditions(sample, 2)
            # source-effect driver:02db:jr
            if not (bool(conditions & 0x40)):
                # source-effect driver:02dd:ld
                state.write(u16(channel_cursor + 19), u8(0))
        # source-effect driver:02e1:ld
        parameter_cursor = replace_high(parameter_cursor, 0)
        # source-effect driver:02e3:add
        arithmetic_result_18, conditions = sum_word(lookup_cursor, parameter_cursor, conditions)
        lookup_cursor = u16(arithmetic_result_18)
        # source-effect driver:02e4:ex
        parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
        # source-effect driver:02e5:call
        from .business_sequence import set_stereo_pan
        from .contexts import SetStereoPanInput
        stack_cursor = state.push_word(stack_cursor, 744)
        updated_audio_values_19 = set_stereo_pan(state, SetStereoPanInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 744)))
        channel_cursor = updated_audio_values_19.channel_cursor
        conditions = updated_audio_values_19.conditions
        count_and_data = updated_audio_values_19.count_and_data
        lookup_cursor = updated_audio_values_19.lookup_cursor
        parameter_cursor = updated_audio_values_19.parameter_cursor
        sample = updated_audio_values_19.sample
        stack_cursor = updated_audio_values_19.stack_cursor
        # source-effect driver:02e8:exx
        alternate_group_20 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
        alternate_group_20.validate()
        count_and_data, parameter_cursor, lookup_cursor = alternate_group_20.count_and_data, alternate_group_20.parameter_cursor, alternate_group_20.lookup_cursor
        # source-effect driver:02e9:ret
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return UpdatePanPatternResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    else:
        # source-effect driver:02af:bit
        observed_byte_21 = state.read(u16(channel_cursor + 0))
        conditions = state.memory_bit_conditions(observed_byte_21, 1, conditions, u16(channel_cursor + 0), True)
        # source-effect driver:02b3:ret
        if not (conditions & 0x40):
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return UpdatePanPatternResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
        # source-effect driver:02b4:dec
        observed_byte_22 = state.read(u16(channel_cursor + 22))
        changed_byte_23, conditions = decrement_byte(observed_byte_22, conditions)
        state.write(u16(channel_cursor + 22), u8(changed_byte_23))
        # source-effect driver:02b7:ret
        if not (conditions & 0x40):
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return UpdatePanPatternResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
        # source-effect driver:02b8:exx
        alternate_group_24 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
        alternate_group_24.validate()
        count_and_data, parameter_cursor, lookup_cursor = alternate_group_24.count_and_data, alternate_group_24.parameter_cursor, alternate_group_24.lookup_cursor
        # source-effect driver:02b9:ld
        observed_byte_25 = state.read(u16(channel_cursor + 21))
        sample = u8(observed_byte_25)
        # source-effect driver:02bc:ld
        state.write(u16(channel_cursor + 22), u8(sample))
        # source-effect driver:02bf:ld
        observed_byte_26 = state.read(u16(channel_cursor + 18))
        sample = u8(observed_byte_26)
        # source-effect driver:02c2:ld
        lookup_cursor = u16(758)
        # source-effect driver:02c5:rst
        from .business_hardware import index_word_pointer
        from .contexts import IndexWordPointerInput
        stack_cursor = state.push_word(stack_cursor, 710)
        updated_audio_values_27 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 710)))
        conditions = updated_audio_values_27.conditions
        count_and_data = updated_audio_values_27.count_and_data
        lookup_cursor = updated_audio_values_27.lookup_cursor
        sample = updated_audio_values_27.sample
        stack_cursor = updated_audio_values_27.stack_cursor
        # source-effect driver:02c6:ld
        observed_byte_28 = state.read(u16(channel_cursor + 19))
        parameter_cursor = replace_low(parameter_cursor, observed_byte_28)
        # source-effect driver:02c9:inc
        observed_byte_29 = state.read(u16(channel_cursor + 19))
        changed_byte_30, conditions = increment_byte(observed_byte_29, conditions)
        state.write(u16(channel_cursor + 19), u8(changed_byte_30))
        # source-effect driver:02cc:ld
        observed_byte_31 = state.read(u16(channel_cursor + 20))
        sample = u8(observed_byte_31)
        # source-effect driver:02cf:dec
        changed_byte_32, conditions = decrement_byte(sample, conditions)
        sample = u8(changed_byte_32)
        # source-effect driver:02d0:cp
        conditions = comparison_conditions(sample, low(parameter_cursor))
        # source-effect driver:02d1:jr
        if not (not (conditions & 0x40)):
            # source-effect driver:02d3:dec
            observed_byte_33 = state.read(u16(channel_cursor + 19))
            changed_byte_34, conditions = decrement_byte(observed_byte_33, conditions)
            state.write(u16(channel_cursor + 19), u8(changed_byte_34))
            # source-effect driver:02d6:ld
            observed_byte_35 = state.read(u16(channel_cursor + 17))
            sample = u8(observed_byte_35)
            # source-effect driver:02d9:cp
            conditions = comparison_conditions(sample, 2)
            # source-effect driver:02db:jr
            if not (bool(conditions & 0x40)):
                # source-effect driver:02dd:ld
                state.write(u16(channel_cursor + 19), u8(0))
        # source-effect driver:02e1:ld
        parameter_cursor = replace_high(parameter_cursor, 0)
        # source-effect driver:02e3:add
        arithmetic_result_36, conditions = sum_word(lookup_cursor, parameter_cursor, conditions)
        lookup_cursor = u16(arithmetic_result_36)
        # source-effect driver:02e4:ex
        parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
        # source-effect driver:02e5:call
        from .business_sequence import set_stereo_pan
        from .contexts import SetStereoPanInput
        stack_cursor = state.push_word(stack_cursor, 744)
        updated_audio_values_37 = set_stereo_pan(state, SetStereoPanInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 744)))
        channel_cursor = updated_audio_values_37.channel_cursor
        conditions = updated_audio_values_37.conditions
        count_and_data = updated_audio_values_37.count_and_data
        lookup_cursor = updated_audio_values_37.lookup_cursor
        parameter_cursor = updated_audio_values_37.parameter_cursor
        sample = updated_audio_values_37.sample
        stack_cursor = updated_audio_values_37.stack_cursor
        # source-effect driver:02e8:exx
        alternate_group_38 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
        alternate_group_38.validate()
        count_and_data, parameter_cursor, lookup_cursor = alternate_group_38.count_and_data, alternate_group_38.parameter_cursor, alternate_group_38.lookup_cursor
        # source-effect driver:02e9:ret
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return UpdatePanPatternResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def resume_pan_pattern(state: AudioState, inputs: ResumePanPatternInput) -> ResumePanPatternResult:
    """Resume pan pattern."""
    checked_state(state)
    if type(inputs) is not ResumePanPatternInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    channel_cursor = inputs.channel_cursor
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    lookup_cursor = inputs.lookup_cursor
    parameter_cursor = inputs.parameter_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:02ee:ld
    observed_byte_1 = state.read(u16(channel_cursor + 17))
    sample = u8(observed_byte_1)
    # source-effect driver:02f1:sub
    sample, conditions = difference_byte(sample, 2)
    # source-effect driver:02f3:ret
    if bool(conditions & 0x80):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return ResumePanPatternResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:02f4:jr
    pass  # Static control continuation is structured below.
    # source-effect driver:02b4:dec
    observed_byte_2 = state.read(u16(channel_cursor + 22))
    changed_byte_3, conditions = decrement_byte(observed_byte_2, conditions)
    state.write(u16(channel_cursor + 22), u8(changed_byte_3))
    # source-effect driver:02b7:ret
    if not (conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return ResumePanPatternResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:02b8:exx
    alternate_group_4 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
    alternate_group_4.validate()
    count_and_data, parameter_cursor, lookup_cursor = alternate_group_4.count_and_data, alternate_group_4.parameter_cursor, alternate_group_4.lookup_cursor
    # source-effect driver:02b9:ld
    observed_byte_5 = state.read(u16(channel_cursor + 21))
    sample = u8(observed_byte_5)
    # source-effect driver:02bc:ld
    state.write(u16(channel_cursor + 22), u8(sample))
    # source-effect driver:02bf:ld
    observed_byte_6 = state.read(u16(channel_cursor + 18))
    sample = u8(observed_byte_6)
    # source-effect driver:02c2:ld
    lookup_cursor = u16(758)
    # source-effect driver:02c5:rst
    from .business_hardware import index_word_pointer
    from .contexts import IndexWordPointerInput
    stack_cursor = state.push_word(stack_cursor, 710)
    updated_audio_values_7 = index_word_pointer(state, IndexWordPointerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 710)))
    conditions = updated_audio_values_7.conditions
    count_and_data = updated_audio_values_7.count_and_data
    lookup_cursor = updated_audio_values_7.lookup_cursor
    sample = updated_audio_values_7.sample
    stack_cursor = updated_audio_values_7.stack_cursor
    # source-effect driver:02c6:ld
    observed_byte_8 = state.read(u16(channel_cursor + 19))
    parameter_cursor = replace_low(parameter_cursor, observed_byte_8)
    # source-effect driver:02c9:inc
    observed_byte_9 = state.read(u16(channel_cursor + 19))
    changed_byte_10, conditions = increment_byte(observed_byte_9, conditions)
    state.write(u16(channel_cursor + 19), u8(changed_byte_10))
    # source-effect driver:02cc:ld
    observed_byte_11 = state.read(u16(channel_cursor + 20))
    sample = u8(observed_byte_11)
    # source-effect driver:02cf:dec
    changed_byte_12, conditions = decrement_byte(sample, conditions)
    sample = u8(changed_byte_12)
    # source-effect driver:02d0:cp
    conditions = comparison_conditions(sample, low(parameter_cursor))
    # source-effect driver:02d1:jr
    if not (not (conditions & 0x40)):
        # source-effect driver:02d3:dec
        observed_byte_13 = state.read(u16(channel_cursor + 19))
        changed_byte_14, conditions = decrement_byte(observed_byte_13, conditions)
        state.write(u16(channel_cursor + 19), u8(changed_byte_14))
        # source-effect driver:02d6:ld
        observed_byte_15 = state.read(u16(channel_cursor + 17))
        sample = u8(observed_byte_15)
        # source-effect driver:02d9:cp
        conditions = comparison_conditions(sample, 2)
        # source-effect driver:02db:jr
        if not (bool(conditions & 0x40)):
            # source-effect driver:02dd:ld
            state.write(u16(channel_cursor + 19), u8(0))
    # source-effect driver:02e1:ld
    parameter_cursor = replace_high(parameter_cursor, 0)
    # source-effect driver:02e3:add
    arithmetic_result_16, conditions = sum_word(lookup_cursor, parameter_cursor, conditions)
    lookup_cursor = u16(arithmetic_result_16)
    # source-effect driver:02e4:ex
    parameter_cursor, lookup_cursor = lookup_cursor, parameter_cursor
    # source-effect driver:02e5:call
    from .business_sequence import set_stereo_pan
    from .contexts import SetStereoPanInput
    stack_cursor = state.push_word(stack_cursor, 744)
    updated_audio_values_17 = set_stereo_pan(state, SetStereoPanInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 744)))
    channel_cursor = updated_audio_values_17.channel_cursor
    conditions = updated_audio_values_17.conditions
    count_and_data = updated_audio_values_17.count_and_data
    lookup_cursor = updated_audio_values_17.lookup_cursor
    parameter_cursor = updated_audio_values_17.parameter_cursor
    sample = updated_audio_values_17.sample
    stack_cursor = updated_audio_values_17.stack_cursor
    # source-effect driver:02e8:exx
    alternate_group_18 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
    alternate_group_18.validate()
    count_and_data, parameter_cursor, lookup_cursor = alternate_group_18.count_and_data, alternate_group_18.parameter_cursor, alternate_group_18.lookup_cursor
    # source-effect driver:02e9:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return ResumePanPatternResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)
