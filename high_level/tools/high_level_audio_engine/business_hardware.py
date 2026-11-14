"""Structured intermediate audio logic, not a complete CPU/timing proof."""
from .domain import (AudioState, AudioBoundary, Continuation, AlternateGroup,
    Byte, Word, byte, word, checked_state, u8, u16, low, high, replace_low,
    replace_high, logic_conditions, sum_byte, difference_byte,
    comparison_conditions, increment_byte, decrement_byte, sum_word,
    difference_word, tested_bit_conditions, copy_byte_conditions)
from .contexts import (
    InitializeAudioDriverInput, InitializeAudioDriverResult,
    WaitFmReadyInput, WaitFmReadyResult,
    WriteChannelFmRegisterInput, WriteChannelFmRegisterResult,
    WriteFmPortZeroEntryInput, WriteFmPortZeroEntryResult,
    LookupBankedRootPointerInput, LookupBankedRootPointerResult,
    LookupPointerAfterRootInput, LookupPointerAfterRootResult,
    IndexWordPointerInput, IndexWordPointerResult,
    ReadStreamWordInput, ReadStreamWordResult,
    ServiceIm1InterruptInput, ServiceIm1InterruptResult,
    ProgramTimerAInput, ProgramTimerAResult,
    ProgramTimerBInput, ProgramTimerBResult,
    UpdateAudioDriverInput, UpdateAudioDriverResult,
    UpdateSfxChannelGroupsInput, UpdateSfxChannelGroupsResult,
    UpdateChannelGroupInput, UpdateChannelGroupResult,
    WriteFmPortOneInput, WriteFmPortOneResult,
)

def initialize_audio_driver(state: AudioState, inputs: InitializeAudioDriverInput) -> InitializeAudioDriverResult:
    """Initialize audio driver."""
    checked_state(state)
    if type(inputs) is not InitializeAudioDriverInput:
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
    # source-effect driver:0000:di
    state.platform.interrupt_control(False, False)
    # source-effect driver:0001:di
    state.platform.interrupt_control(False, False)
    # source-effect driver:0002:im
    state.platform.interrupt_mode(1)
    # source-effect driver:0004:jr
    pass  # Static control continuation is structured below.
    # source-effect driver:0053:ld
    stack_cursor = u16(8189)
    # source-effect driver:0056:ld
    sample = u8(3)
    # source-effect driver:0058:ld
    state.write(8191, u8(sample))
    while True:
        # source-effect driver:005b:ei
        state.platform.interrupt_control(True, True)
        # source-effect driver:005c:ld
        observed_byte_1 = state.read(8191)
        sample = u8(observed_byte_1)
        # source-effect driver:005f:or
        sample = u8(sample | sample)
        conditions = logic_conditions(sample, False)
        # source-effect driver:0060:jp
        if not (conditions & 0x40):
            continue
        break
    # source-effect driver:0063:call
    from .business_loaders import clear_and_reset_driver
    from .contexts import ClearAndResetDriverInput
    stack_cursor = state.push_word(stack_cursor, 102)
    updated_audio_values_2 = clear_and_reset_driver(state, ClearAndResetDriverInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 102)))
    auxiliary_cursor = updated_audio_values_2.auxiliary_cursor
    channel_cursor = updated_audio_values_2.channel_cursor
    conditions = updated_audio_values_2.conditions
    count_and_data = updated_audio_values_2.count_and_data
    lookup_cursor = updated_audio_values_2.lookup_cursor
    parameter_cursor = updated_audio_values_2.parameter_cursor
    sample = updated_audio_values_2.sample
    stack_cursor = updated_audio_values_2.stack_cursor
    # source-effect driver:0066:call
    from .business_loaders import initialize_audio_bank
    from .contexts import InitializeAudioBankInput
    stack_cursor = state.push_word(stack_cursor, 105)
    updated_audio_values_3 = initialize_audio_bank(state, InitializeAudioBankInput(conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 105)))
    conditions = updated_audio_values_3.conditions
    count_and_data = updated_audio_values_3.count_and_data
    sample = updated_audio_values_3.sample
    stack_cursor = updated_audio_values_3.stack_cursor
    # source-effect driver:0069:call
    from .business_hardware import program_timer_a
    from .contexts import ProgramTimerAInput
    stack_cursor = state.push_word(stack_cursor, 108)
    updated_audio_values_4 = program_timer_a(state, ProgramTimerAInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 108)))
    channel_cursor = updated_audio_values_4.channel_cursor
    conditions = updated_audio_values_4.conditions
    count_and_data = updated_audio_values_4.count_and_data
    lookup_cursor = updated_audio_values_4.lookup_cursor
    sample = updated_audio_values_4.sample
    stack_cursor = updated_audio_values_4.stack_cursor
    # source-effect driver:006c:call
    from .business_hardware import program_timer_b
    from .contexts import ProgramTimerBInput
    stack_cursor = state.push_word(stack_cursor, 111)
    updated_audio_values_5 = program_timer_b(state, ProgramTimerBInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 111)))
    channel_cursor = updated_audio_values_5.channel_cursor
    conditions = updated_audio_values_5.conditions
    count_and_data = updated_audio_values_5.count_and_data
    lookup_cursor = updated_audio_values_5.lookup_cursor
    sample = updated_audio_values_5.sample
    stack_cursor = updated_audio_values_5.stack_cursor
    while True:
        # source-effect driver:006f:ei
        state.platform.interrupt_control(True, True)
        # source-effect driver:0070:call
        from .business_mailbox import poll_command_mailboxes
        from .contexts import PollCommandMailboxesInput
        stack_cursor = state.push_word(stack_cursor, 115)
        updated_audio_values_6 = poll_command_mailboxes(state, PollCommandMailboxesInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 115)))
        conditions = updated_audio_values_6.conditions
        count_and_data = updated_audio_values_6.count_and_data
        lookup_cursor = updated_audio_values_6.lookup_cursor
        parameter_cursor = updated_audio_values_6.parameter_cursor
        sample = updated_audio_values_6.sample
        stack_cursor = updated_audio_values_6.stack_cursor
        # source-effect driver:0073:ld
        observed_byte_7 = state.read(7175)
        sample = u8(observed_byte_7)
        # source-effect driver:0076:or
        sample = u8(sample | sample)
        conditions = logic_conditions(sample, False)
        # source-effect driver:0077:jr
        if bool(conditions & 0x40):
            continue
        # source-effect driver:0079:di
        state.platform.interrupt_control(False, False)
        # source-effect driver:007a:jp
        if not (conditions & 0x80):
            # source-effect driver:00aa:ld
            observed_byte_8 = state.read(16384)
            sample = u8(observed_byte_8)
            # source-effect driver:00ad:bit
            conditions = tested_bit_conditions(sample, 1, conditions)
            # source-effect driver:00af:jr
            if bool(conditions & 0x40):
                continue
            # source-effect driver:00b1:call
            from .business_hardware import program_timer_b
            from .contexts import ProgramTimerBInput
            stack_cursor = state.push_word(stack_cursor, 180)
            updated_audio_values_9 = program_timer_b(state, ProgramTimerBInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 180)))
            channel_cursor = updated_audio_values_9.channel_cursor
            conditions = updated_audio_values_9.conditions
            count_and_data = updated_audio_values_9.count_and_data
            lookup_cursor = updated_audio_values_9.lookup_cursor
            sample = updated_audio_values_9.sample
            stack_cursor = updated_audio_values_9.stack_cursor
            # source-effect driver:00b4:call
            from .business_hardware import update_audio_driver
            from .contexts import UpdateAudioDriverInput
            stack_cursor = state.push_word(stack_cursor, 183)
            updated_audio_values_10 = update_audio_driver(state, UpdateAudioDriverInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 183)))
            auxiliary_cursor = updated_audio_values_10.auxiliary_cursor
            channel_cursor = updated_audio_values_10.channel_cursor
            conditions = updated_audio_values_10.conditions
            count_and_data = updated_audio_values_10.count_and_data
            lookup_cursor = updated_audio_values_10.lookup_cursor
            parameter_cursor = updated_audio_values_10.parameter_cursor
            sample = updated_audio_values_10.sample
            stack_cursor = updated_audio_values_10.stack_cursor
            # source-effect driver:00b7:jr
            pass  # Static control continuation is structured below.
            continue
        # source-effect driver:007d:call
        from .business_mailbox import poll_command_mailboxes
        from .contexts import PollCommandMailboxesInput
        stack_cursor = state.push_word(stack_cursor, 128)
        updated_audio_values_11 = poll_command_mailboxes(state, PollCommandMailboxesInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 128)))
        conditions = updated_audio_values_11.conditions
        count_and_data = updated_audio_values_11.count_and_data
        lookup_cursor = updated_audio_values_11.lookup_cursor
        parameter_cursor = updated_audio_values_11.parameter_cursor
        sample = updated_audio_values_11.sample
        stack_cursor = updated_audio_values_11.stack_cursor
        # source-effect driver:0080:ld
        observed_byte_12 = state.read(16384)
        sample = u8(observed_byte_12)
        # source-effect driver:0083:and
        sample = u8(sample & 3)
        conditions = logic_conditions(sample, True)
        # source-effect driver:0085:jr
        if bool(conditions & 0x40):
            continue
        # source-effect driver:0087:bit
        conditions = tested_bit_conditions(sample, 1, conditions)
        # source-effect driver:0089:jr
        if not (bool(conditions & 0x40)):
            break
        # source-effect driver:009b:ld
        observed_byte_13 = state.read(16384)
        sample = u8(observed_byte_13)
        # source-effect driver:009e:bit
        conditions = tested_bit_conditions(sample, 0, conditions)
        # source-effect driver:00a0:jr
        if bool(conditions & 0x40):
            continue
        # source-effect driver:00a2:call
        from .business_hardware import program_timer_a
        from .contexts import ProgramTimerAInput
        stack_cursor = state.push_word(stack_cursor, 165)
        updated_audio_values_14 = program_timer_a(state, ProgramTimerAInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 165)))
        channel_cursor = updated_audio_values_14.channel_cursor
        conditions = updated_audio_values_14.conditions
        count_and_data = updated_audio_values_14.count_and_data
        lookup_cursor = updated_audio_values_14.lookup_cursor
        sample = updated_audio_values_14.sample
        stack_cursor = updated_audio_values_14.stack_cursor
        # source-effect driver:00a5:call
        from .business_hardware import update_audio_driver
        from .contexts import UpdateAudioDriverInput
        stack_cursor = state.push_word(stack_cursor, 168)
        updated_audio_values_15 = update_audio_driver(state, UpdateAudioDriverInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 168)))
        auxiliary_cursor = updated_audio_values_15.auxiliary_cursor
        channel_cursor = updated_audio_values_15.channel_cursor
        conditions = updated_audio_values_15.conditions
        count_and_data = updated_audio_values_15.count_and_data
        lookup_cursor = updated_audio_values_15.lookup_cursor
        parameter_cursor = updated_audio_values_15.parameter_cursor
        sample = updated_audio_values_15.sample
        stack_cursor = updated_audio_values_15.stack_cursor
        # source-effect driver:00a8:jr
        pass  # Static control continuation is structured below.
        continue
    # source-effect driver:008b:call
    from .business_hardware import program_timer_b
    from .contexts import ProgramTimerBInput
    stack_cursor = state.push_word(stack_cursor, 142)
    updated_audio_values_16 = program_timer_b(state, ProgramTimerBInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 142)))
    channel_cursor = updated_audio_values_16.channel_cursor
    conditions = updated_audio_values_16.conditions
    count_and_data = updated_audio_values_16.count_and_data
    lookup_cursor = updated_audio_values_16.lookup_cursor
    sample = updated_audio_values_16.sample
    stack_cursor = updated_audio_values_16.stack_cursor
    # source-effect driver:008e:ld
    lookup_cursor = u16(155)
    # source-effect driver:0091:push
    stack_cursor = state.push_word(stack_cursor, lookup_cursor)
    # source-effect driver:0092:call
    from .business_loaders import process_driver_stop_mode
    from .contexts import ProcessDriverStopModeInput
    stack_cursor = state.push_word(stack_cursor, 149)
    updated_audio_values_17 = process_driver_stop_mode(state, ProcessDriverStopModeInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 149)))
    auxiliary_cursor = updated_audio_values_17.auxiliary_cursor
    channel_cursor = updated_audio_values_17.channel_cursor
    conditions = updated_audio_values_17.conditions
    count_and_data = updated_audio_values_17.count_and_data
    lookup_cursor = updated_audio_values_17.lookup_cursor
    parameter_cursor = updated_audio_values_17.parameter_cursor
    sample = updated_audio_values_17.sample
    stack_cursor = updated_audio_values_17.stack_cursor
    # source-effect driver:0095:call
    from .business_loaders import dispatch_sound_command
    from .contexts import DispatchSoundCommandInput
    stack_cursor = state.push_word(stack_cursor, 152)
    updated_audio_values_18 = dispatch_sound_command(state, DispatchSoundCommandInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 152)))
    auxiliary_cursor = updated_audio_values_18.auxiliary_cursor
    channel_cursor = updated_audio_values_18.channel_cursor
    conditions = updated_audio_values_18.conditions
    count_and_data = updated_audio_values_18.count_and_data
    lookup_cursor = updated_audio_values_18.lookup_cursor
    parameter_cursor = updated_audio_values_18.parameter_cursor
    sample = updated_audio_values_18.sample
    stack_cursor = updated_audio_values_18.stack_cursor
    # source-effect driver:0098:jp
    pass  # Static control continuation is structured below.
    # source-effect driver:010f:ld
    sample = u8(1)
    # source-effect driver:0111:ld
    state.write(7193, u8(sample))
    # source-effect driver:0114:ld
    channel_cursor = u16(7808)
    # source-effect driver:0118:ld
    count_and_data = replace_high(count_and_data, 6)
    # source-effect driver:011a:call
    from .business_hardware import update_channel_group
    from .contexts import UpdateChannelGroupInput
    stack_cursor = state.push_word(stack_cursor, 285)
    updated_audio_values_19 = update_channel_group(state, UpdateChannelGroupInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 285)))
    auxiliary_cursor = updated_audio_values_19.auxiliary_cursor
    channel_cursor = updated_audio_values_19.channel_cursor
    conditions = updated_audio_values_19.conditions
    count_and_data = updated_audio_values_19.count_and_data
    lookup_cursor = updated_audio_values_19.lookup_cursor
    parameter_cursor = updated_audio_values_19.parameter_cursor
    sample = updated_audio_values_19.sample
    stack_cursor = updated_audio_values_19.stack_cursor
    # source-effect driver:011d:ld
    sample = u8(128)
    # source-effect driver:011f:ld
    state.write(7193, u8(sample))
    # source-effect driver:0122:ld
    count_and_data = replace_high(count_and_data, 2)
    # source-effect driver:0124:ld
    channel_cursor = u16(7712)
    while True:
        # source-effect driver:0128:push
        stack_cursor = state.push_word(stack_cursor, count_and_data)
        # source-effect driver:0129:bit
        observed_byte_20 = state.read(u16(channel_cursor + 0))
        conditions = state.memory_bit_conditions(observed_byte_20, 7, conditions, u16(channel_cursor + 0), True)
        # source-effect driver:012d:call
        if not (conditions & 0x40):
            from .business_channel_update import update_fm_channel
            from .contexts import UpdateFmChannelInput
            stack_cursor = state.push_word(stack_cursor, 304)
            updated_audio_values_21 = update_fm_channel(state, UpdateFmChannelInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 304)))
            auxiliary_cursor = updated_audio_values_21.auxiliary_cursor
            channel_cursor = updated_audio_values_21.channel_cursor
            conditions = updated_audio_values_21.conditions
            count_and_data = updated_audio_values_21.count_and_data
            lookup_cursor = updated_audio_values_21.lookup_cursor
            parameter_cursor = updated_audio_values_21.parameter_cursor
            sample = updated_audio_values_21.sample
            stack_cursor = updated_audio_values_21.stack_cursor
        # source-effect driver:0130:ld
        parameter_cursor = u16(48)
        # source-effect driver:0133:add
        arithmetic_result_22, conditions = sum_word(channel_cursor, parameter_cursor, conditions)
        channel_cursor = u16(arithmetic_result_22)
        # source-effect driver:0135:pop
        saved_audio_word_23, stack_cursor = state.pop_word(stack_cursor)
        count_and_data = u16(saved_audio_word_23)
        # source-effect driver:0136:djnz
        count_and_data = replace_high(count_and_data, u8(high(count_and_data) - 1))
        if high(count_and_data) != 0:
            continue
        break
    # source-effect driver:0138:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return InitializeAudioDriverResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def wait_fm_ready(state: AudioState, inputs: WaitFmReadyInput) -> WaitFmReadyResult:
    """Wait fm ready."""
    checked_state(state)
    if type(inputs) is not WaitFmReadyInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    conditions = inputs.conditions
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    while True:
        # source-effect driver:0008:ld
        observed_byte_1 = state.read(16384)
        sample = u8(observed_byte_1)
        # source-effect driver:000b:bit
        conditions = tested_bit_conditions(sample, 7, conditions)
        # source-effect driver:000d:jr
        if not (conditions & 0x40):
            continue
        break
    # source-effect driver:000f:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return WaitFmReadyResult(conditions=conditions, sample=sample, stack_cursor=stack_cursor).validate(state)

def write_channel_fm_register(state: AudioState, inputs: WriteChannelFmRegisterInput) -> WriteChannelFmRegisterResult:
    """Write channel fm register."""
    checked_state(state)
    if type(inputs) is not WriteChannelFmRegisterInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    channel_cursor = inputs.channel_cursor
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:0010:bit
    observed_byte_1 = state.read(u16(channel_cursor + 1))
    conditions = state.memory_bit_conditions(observed_byte_1, 7, conditions, u16(channel_cursor + 1), True)
    # source-effect driver:0014:ret
    if not (conditions & 0x40):
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return WriteChannelFmRegisterResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor).validate(state)
    # source-effect driver:0015:jp
    pass  # Static control continuation is structured below.
    # source-effect driver:049e:bit
    observed_byte_2 = state.read(u16(channel_cursor + 1))
    conditions = state.memory_bit_conditions(observed_byte_2, 2, conditions, u16(channel_cursor + 1), True)
    # source-effect driver:04a2:jr
    if not (conditions & 0x40):
        # source-effect driver:04b5:bit
        observed_byte_3 = state.read(u16(channel_cursor + 0))
        conditions = state.memory_bit_conditions(observed_byte_3, 2, conditions, u16(channel_cursor + 0), True)
        # source-effect driver:04b9:ret
        if not (conditions & 0x40):
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return WriteChannelFmRegisterResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor).validate(state)
        # source-effect driver:04ba:add
        observed_byte_4 = state.read(u16(channel_cursor + 1))
        arithmetic_result_5, conditions = sum_byte(sample, observed_byte_4)
        sample = u8(arithmetic_result_5)
        # source-effect driver:04bd:sub
        sample, conditions = difference_byte(sample, 4)
        # source-effect driver:04bf:ld
        state.write(16386, u8(sample))
        # source-effect driver:04c2:rst
        from .business_hardware import wait_fm_ready
        from .contexts import WaitFmReadyInput
        stack_cursor = state.push_word(stack_cursor, 1219)
        updated_audio_values_6 = wait_fm_ready(state, WaitFmReadyInput(conditions=conditions, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 1219)))
        conditions = updated_audio_values_6.conditions
        sample = updated_audio_values_6.sample
        stack_cursor = updated_audio_values_6.stack_cursor
        # source-effect driver:04c3:ld
        sample = u8(low(count_and_data))
        # source-effect driver:04c4:ld
        state.write(16387, u8(sample))
        # source-effect driver:04c7:ret
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return WriteChannelFmRegisterResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor).validate(state)
    else:
        # source-effect driver:04a4:bit
        observed_byte_7 = state.read(u16(channel_cursor + 0))
        conditions = state.memory_bit_conditions(observed_byte_7, 2, conditions, u16(channel_cursor + 0), True)
        # source-effect driver:04a8:ret
        if not (conditions & 0x40):
            stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
            return WriteChannelFmRegisterResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor).validate(state)
        # source-effect driver:04a9:add
        observed_byte_8 = state.read(u16(channel_cursor + 1))
        arithmetic_result_9, conditions = sum_byte(sample, observed_byte_8)
        sample = u8(arithmetic_result_9)
        # source-effect driver:04ac:ld
        state.write(16384, u8(sample))
        # source-effect driver:04af:rst
        from .business_hardware import wait_fm_ready
        from .contexts import WaitFmReadyInput
        stack_cursor = state.push_word(stack_cursor, 1200)
        updated_audio_values_10 = wait_fm_ready(state, WaitFmReadyInput(conditions=conditions, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 1200)))
        conditions = updated_audio_values_10.conditions
        sample = updated_audio_values_10.sample
        stack_cursor = updated_audio_values_10.stack_cursor
        # source-effect driver:04b0:ld
        sample = u8(low(count_and_data))
        # source-effect driver:04b1:ld
        state.write(16385, u8(sample))
        # source-effect driver:04b4:ret
        stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
        return WriteChannelFmRegisterResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor).validate(state)

def write_fm_port_zero_entry(state: AudioState, inputs: WriteFmPortZeroEntryInput) -> WriteFmPortZeroEntryResult:
    """Write fm port zero entry."""
    checked_state(state)
    if type(inputs) is not WriteFmPortZeroEntryInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    channel_cursor = inputs.channel_cursor
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:0018:jp
    pass  # Static control continuation is structured below.
    # source-effect driver:04ac:ld
    state.write(16384, u8(sample))
    # source-effect driver:04af:rst
    from .business_hardware import wait_fm_ready
    from .contexts import WaitFmReadyInput
    stack_cursor = state.push_word(stack_cursor, 1200)
    updated_audio_values_1 = wait_fm_ready(state, WaitFmReadyInput(conditions=conditions, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 1200)))
    conditions = updated_audio_values_1.conditions
    sample = updated_audio_values_1.sample
    stack_cursor = updated_audio_values_1.stack_cursor
    # source-effect driver:04b0:ld
    sample = u8(low(count_and_data))
    # source-effect driver:04b1:ld
    state.write(16385, u8(sample))
    # source-effect driver:04b4:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return WriteFmPortZeroEntryResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor).validate(state)

def lookup_banked_root_pointer(state: AudioState, inputs: LookupBankedRootPointerInput) -> LookupBankedRootPointerResult:
    """Lookup banked root pointer."""
    checked_state(state)
    if type(inputs) is not LookupBankedRootPointerInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    lookup_cursor = inputs.lookup_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:0020:ld
    observed_word_1 = state.read_word_le(7170)
    lookup_cursor = u16(observed_word_1)
    # source-effect driver:0023:ld
    count_and_data = replace_high(count_and_data, 0)
    # source-effect driver:0025:jp
    pass  # Static control continuation is structured below.
    # source-effect driver:0478:add
    arithmetic_result_2, conditions = sum_word(lookup_cursor, count_and_data, conditions)
    lookup_cursor = u16(arithmetic_result_2)
    # source-effect driver:0479:ex
    alternate_sample_and_conditions_3 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
    sample, conditions = high(alternate_sample_and_conditions_3), low(alternate_sample_and_conditions_3)
    # source-effect driver:047a:rst
    from .business_hardware import read_stream_word
    from .contexts import ReadStreamWordInput
    stack_cursor = state.push_word(stack_cursor, 1147)
    updated_audio_values_4 = read_stream_word(state, ReadStreamWordInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 1147)))
    conditions = updated_audio_values_4.conditions
    count_and_data = updated_audio_values_4.count_and_data
    lookup_cursor = updated_audio_values_4.lookup_cursor
    sample = updated_audio_values_4.sample
    stack_cursor = updated_audio_values_4.stack_cursor
    # source-effect driver:047b:ex
    alternate_sample_and_conditions_5 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
    sample, conditions = high(alternate_sample_and_conditions_5), low(alternate_sample_and_conditions_5)
    # source-effect driver:047c:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return LookupBankedRootPointerResult(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def lookup_pointer_after_root(state: AudioState, inputs: LookupPointerAfterRootInput) -> LookupPointerAfterRootResult:
    """Lookup pointer after root."""
    checked_state(state)
    if type(inputs) is not LookupPointerAfterRootInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    lookup_cursor = inputs.lookup_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:0023:ld
    count_and_data = replace_high(count_and_data, 0)
    # source-effect driver:0025:jp
    pass  # Static control continuation is structured below.
    # source-effect driver:0478:add
    arithmetic_result_1, conditions = sum_word(lookup_cursor, count_and_data, conditions)
    lookup_cursor = u16(arithmetic_result_1)
    # source-effect driver:0479:ex
    alternate_sample_and_conditions_2 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
    sample, conditions = high(alternate_sample_and_conditions_2), low(alternate_sample_and_conditions_2)
    # source-effect driver:047a:rst
    from .business_hardware import read_stream_word
    from .contexts import ReadStreamWordInput
    stack_cursor = state.push_word(stack_cursor, 1147)
    updated_audio_values_3 = read_stream_word(state, ReadStreamWordInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 1147)))
    conditions = updated_audio_values_3.conditions
    count_and_data = updated_audio_values_3.count_and_data
    lookup_cursor = updated_audio_values_3.lookup_cursor
    sample = updated_audio_values_3.sample
    stack_cursor = updated_audio_values_3.stack_cursor
    # source-effect driver:047b:ex
    alternate_sample_and_conditions_4 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
    sample, conditions = high(alternate_sample_and_conditions_4), low(alternate_sample_and_conditions_4)
    # source-effect driver:047c:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return LookupPointerAfterRootResult(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def index_word_pointer(state: AudioState, inputs: IndexWordPointerInput) -> IndexWordPointerResult:
    """Index word pointer."""
    checked_state(state)
    if type(inputs) is not IndexWordPointerInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    lookup_cursor = inputs.lookup_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:0028:ld
    count_and_data = replace_low(count_and_data, sample)
    # source-effect driver:0029:ld
    count_and_data = replace_high(count_and_data, 0)
    # source-effect driver:002b:add
    arithmetic_result_1, conditions = sum_word(lookup_cursor, count_and_data, conditions)
    lookup_cursor = u16(arithmetic_result_1)
    # source-effect driver:002c:add
    arithmetic_result_2, conditions = sum_word(lookup_cursor, count_and_data, conditions)
    lookup_cursor = u16(arithmetic_result_2)
    # source-effect driver:002d:nop
    pass  # Timing-only; no fabricated device progress.
    # source-effect driver:002e:nop
    pass  # Timing-only; no fabricated device progress.
    # source-effect driver:002f:nop
    pass  # Timing-only; no fabricated device progress.
    # source-effect driver:0030:ld
    observed_byte_3 = state.read(lookup_cursor)
    sample = u8(observed_byte_3)
    # source-effect driver:0031:inc
    lookup_cursor = u16(lookup_cursor + 1)
    # source-effect driver:0032:ld
    observed_byte_4 = state.read(lookup_cursor)
    lookup_cursor = replace_high(lookup_cursor, observed_byte_4)
    # source-effect driver:0033:ld
    lookup_cursor = replace_low(lookup_cursor, sample)
    # source-effect driver:0034:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return IndexWordPointerResult(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def read_stream_word(state: AudioState, inputs: ReadStreamWordInput) -> ReadStreamWordResult:
    """Read stream word."""
    checked_state(state)
    if type(inputs) is not ReadStreamWordInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    lookup_cursor = inputs.lookup_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:0030:ld
    observed_byte_1 = state.read(lookup_cursor)
    sample = u8(observed_byte_1)
    # source-effect driver:0031:inc
    lookup_cursor = u16(lookup_cursor + 1)
    # source-effect driver:0032:ld
    observed_byte_2 = state.read(lookup_cursor)
    lookup_cursor = replace_high(lookup_cursor, observed_byte_2)
    # source-effect driver:0033:ld
    lookup_cursor = replace_low(lookup_cursor, sample)
    # source-effect driver:0034:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return ReadStreamWordResult(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def service_im1_interrupt(state: AudioState, inputs: ServiceIm1InterruptInput) -> ServiceIm1InterruptResult:
    """Service im1 interrupt."""
    checked_state(state)
    if type(inputs) is not ServiceIm1InterruptInput:
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
    # source-effect driver:0038:push
    stack_cursor = state.push_word(stack_cursor, ((sample << 8) | conditions))
    # source-effect driver:0039:push
    stack_cursor = state.push_word(stack_cursor, count_and_data)
    # source-effect driver:003a:push
    stack_cursor = state.push_word(stack_cursor, parameter_cursor)
    # source-effect driver:003b:push
    stack_cursor = state.push_word(stack_cursor, lookup_cursor)
    # source-effect driver:003c:ld
    lookup_cursor = u16(8191)
    # source-effect driver:003f:ld
    observed_byte_1 = state.read(lookup_cursor)
    sample = u8(observed_byte_1)
    # source-effect driver:0040:or
    sample = u8(sample | sample)
    conditions = logic_conditions(sample, False)
    # source-effect driver:0041:jr
    if bool(conditions & 0x40):
        # source-effect driver:0046:ld
        observed_byte_2 = state.read(7175)
        sample = u8(observed_byte_2)
        # source-effect driver:0049:or
        sample = u8(sample | sample)
        conditions = logic_conditions(sample, False)
        # source-effect driver:004a:call
        if bool(conditions & 0x40):
            from .business_hardware import update_audio_driver
            from .contexts import UpdateAudioDriverInput
            stack_cursor = state.push_word(stack_cursor, 77)
            updated_audio_values_3 = update_audio_driver(state, UpdateAudioDriverInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 77)))
            auxiliary_cursor = updated_audio_values_3.auxiliary_cursor
            channel_cursor = updated_audio_values_3.channel_cursor
            conditions = updated_audio_values_3.conditions
            count_and_data = updated_audio_values_3.count_and_data
            lookup_cursor = updated_audio_values_3.lookup_cursor
            parameter_cursor = updated_audio_values_3.parameter_cursor
            sample = updated_audio_values_3.sample
            stack_cursor = updated_audio_values_3.stack_cursor
    else:
        # source-effect driver:0043:dec
        observed_byte_4 = state.read(lookup_cursor)
        changed_byte_5, conditions = decrement_byte(observed_byte_4, conditions)
        state.write(lookup_cursor, u8(changed_byte_5))
        # source-effect driver:0044:jr
        pass  # Static control continuation is structured below.
    # source-effect driver:004d:pop
    saved_audio_word_6, stack_cursor = state.pop_word(stack_cursor)
    lookup_cursor = u16(saved_audio_word_6)
    # source-effect driver:004e:pop
    saved_audio_word_7, stack_cursor = state.pop_word(stack_cursor)
    parameter_cursor = u16(saved_audio_word_7)
    # source-effect driver:004f:pop
    saved_audio_word_8, stack_cursor = state.pop_word(stack_cursor)
    count_and_data = u16(saved_audio_word_8)
    # source-effect driver:0050:pop
    saved_audio_word_9, stack_cursor = state.pop_word(stack_cursor)
    sample, conditions = high(saved_audio_word_9), low(saved_audio_word_9)
    # source-effect driver:0051:ei
    state.platform.interrupt_control(True, True)
    # source-effect driver:0052:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return ServiceIm1InterruptResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def program_timer_a(state: AudioState, inputs: ProgramTimerAInput) -> ProgramTimerAResult:
    """Program timer a."""
    checked_state(state)
    if type(inputs) is not ProgramTimerAInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    channel_cursor = inputs.channel_cursor
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    lookup_cursor = inputs.lookup_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:00b9:ld
    observed_word_1 = state.read_word_le(7172)
    lookup_cursor = u16(observed_word_1)
    # source-effect driver:00bc:ld
    sample = u8(low(lookup_cursor))
    # source-effect driver:00bd:and
    sample = u8(sample & 3)
    conditions = logic_conditions(sample, True)
    # source-effect driver:00bf:ld
    count_and_data = replace_low(count_and_data, sample)
    # source-effect driver:00c0:ld
    sample = u8(37)
    # source-effect driver:00c2:rst
    from .business_hardware import write_fm_port_zero_entry
    from .contexts import WriteFmPortZeroEntryInput
    stack_cursor = state.push_word(stack_cursor, 195)
    updated_audio_values_2 = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 195)))
    channel_cursor = updated_audio_values_2.channel_cursor
    conditions = updated_audio_values_2.conditions
    count_and_data = updated_audio_values_2.count_and_data
    sample = updated_audio_values_2.sample
    stack_cursor = updated_audio_values_2.stack_cursor
    # source-effect driver:00c3:srl
    shifted_byte_3 = high(lookup_cursor)
    shift_result_4 = u8((shifted_byte_3 >> 1))
    conditions = logic_conditions(shift_result_4) | (shifted_byte_3 & 1)
    lookup_cursor = replace_high(lookup_cursor, shift_result_4)
    # source-effect driver:00c5:rr
    shifted_byte_5 = low(lookup_cursor)
    shift_result_6 = u8((shifted_byte_5 >> 1) | ((conditions & 1) << 7))
    conditions = logic_conditions(shift_result_6) | (shifted_byte_5 & 1)
    lookup_cursor = replace_low(lookup_cursor, shift_result_6)
    # source-effect driver:00c7:srl
    shifted_byte_7 = high(lookup_cursor)
    shift_result_8 = u8((shifted_byte_7 >> 1))
    conditions = logic_conditions(shift_result_8) | (shifted_byte_7 & 1)
    lookup_cursor = replace_high(lookup_cursor, shift_result_8)
    # source-effect driver:00c9:rr
    shifted_byte_9 = low(lookup_cursor)
    shift_result_10 = u8((shifted_byte_9 >> 1) | ((conditions & 1) << 7))
    conditions = logic_conditions(shift_result_10) | (shifted_byte_9 & 1)
    lookup_cursor = replace_low(lookup_cursor, shift_result_10)
    # source-effect driver:00cb:ld
    count_and_data = replace_low(count_and_data, low(lookup_cursor))
    # source-effect driver:00cc:ld
    sample = u8(36)
    # source-effect driver:00ce:rst
    from .business_hardware import write_fm_port_zero_entry
    from .contexts import WriteFmPortZeroEntryInput
    stack_cursor = state.push_word(stack_cursor, 207)
    updated_audio_values_11 = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 207)))
    channel_cursor = updated_audio_values_11.channel_cursor
    conditions = updated_audio_values_11.conditions
    count_and_data = updated_audio_values_11.count_and_data
    sample = updated_audio_values_11.sample
    stack_cursor = updated_audio_values_11.stack_cursor
    # source-effect driver:00cf:ld
    sample = u8(31)
    # source-effect driver:00d1:jr
    pass  # Static control continuation is structured below.
    # source-effect driver:00dc:ld
    lookup_cursor = u16(7186)
    # source-effect driver:00df:or
    observed_byte_12 = state.read(lookup_cursor)
    sample = u8(sample | observed_byte_12)
    conditions = logic_conditions(sample, False)
    # source-effect driver:00e0:ld
    count_and_data = replace_low(count_and_data, sample)
    # source-effect driver:00e1:ld
    sample = u8(39)
    # source-effect driver:00e3:rst
    from .business_hardware import write_fm_port_zero_entry
    from .contexts import WriteFmPortZeroEntryInput
    stack_cursor = state.push_word(stack_cursor, 228)
    updated_audio_values_13 = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 228)))
    channel_cursor = updated_audio_values_13.channel_cursor
    conditions = updated_audio_values_13.conditions
    count_and_data = updated_audio_values_13.count_and_data
    sample = updated_audio_values_13.sample
    stack_cursor = updated_audio_values_13.stack_cursor
    # source-effect driver:00e4:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return ProgramTimerAResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def program_timer_b(state: AudioState, inputs: ProgramTimerBInput) -> ProgramTimerBResult:
    """Program timer b."""
    checked_state(state)
    if type(inputs) is not ProgramTimerBInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    channel_cursor = inputs.channel_cursor
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    lookup_cursor = inputs.lookup_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:00d3:ld
    observed_byte_1 = state.read(7174)
    sample = u8(observed_byte_1)
    # source-effect driver:00d6:ld
    count_and_data = replace_low(count_and_data, sample)
    # source-effect driver:00d7:ld
    sample = u8(38)
    # source-effect driver:00d9:rst
    from .business_hardware import write_fm_port_zero_entry
    from .contexts import WriteFmPortZeroEntryInput
    stack_cursor = state.push_word(stack_cursor, 218)
    updated_audio_values_2 = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 218)))
    channel_cursor = updated_audio_values_2.channel_cursor
    conditions = updated_audio_values_2.conditions
    count_and_data = updated_audio_values_2.count_and_data
    sample = updated_audio_values_2.sample
    stack_cursor = updated_audio_values_2.stack_cursor
    # source-effect driver:00da:ld
    sample = u8(47)
    # source-effect driver:00dc:ld
    lookup_cursor = u16(7186)
    # source-effect driver:00df:or
    observed_byte_3 = state.read(lookup_cursor)
    sample = u8(sample | observed_byte_3)
    conditions = logic_conditions(sample, False)
    # source-effect driver:00e0:ld
    count_and_data = replace_low(count_and_data, sample)
    # source-effect driver:00e1:ld
    sample = u8(39)
    # source-effect driver:00e3:rst
    from .business_hardware import write_fm_port_zero_entry
    from .contexts import WriteFmPortZeroEntryInput
    stack_cursor = state.push_word(stack_cursor, 228)
    updated_audio_values_4 = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 228)))
    channel_cursor = updated_audio_values_4.channel_cursor
    conditions = updated_audio_values_4.conditions
    count_and_data = updated_audio_values_4.count_and_data
    sample = updated_audio_values_4.sample
    stack_cursor = updated_audio_values_4.stack_cursor
    # source-effect driver:00e4:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return ProgramTimerBResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def update_audio_driver(state: AudioState, inputs: UpdateAudioDriverInput) -> UpdateAudioDriverResult:
    """Update audio driver."""
    checked_state(state)
    if type(inputs) is not UpdateAudioDriverInput:
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
    # source-effect driver:00e5:call
    from .business_loaders import process_driver_stop_mode
    from .contexts import ProcessDriverStopModeInput
    stack_cursor = state.push_word(stack_cursor, 232)
    updated_audio_values_1 = process_driver_stop_mode(state, ProcessDriverStopModeInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 232)))
    auxiliary_cursor = updated_audio_values_1.auxiliary_cursor
    channel_cursor = updated_audio_values_1.channel_cursor
    conditions = updated_audio_values_1.conditions
    count_and_data = updated_audio_values_1.count_and_data
    lookup_cursor = updated_audio_values_1.lookup_cursor
    parameter_cursor = updated_audio_values_1.parameter_cursor
    sample = updated_audio_values_1.sample
    stack_cursor = updated_audio_values_1.stack_cursor
    # source-effect driver:00e8:call
    from .business_loaders import tick_note_divider
    from .contexts import TickNoteDividerInput
    stack_cursor = state.push_word(stack_cursor, 235)
    updated_audio_values_2 = tick_note_divider(state, TickNoteDividerInput(conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 235)))
    conditions = updated_audio_values_2.conditions
    count_and_data = updated_audio_values_2.count_and_data
    lookup_cursor = updated_audio_values_2.lookup_cursor
    parameter_cursor = updated_audio_values_2.parameter_cursor
    sample = updated_audio_values_2.sample
    stack_cursor = updated_audio_values_2.stack_cursor
    # source-effect driver:00eb:call
    from .business_loaders import advance_fadeout
    from .contexts import AdvanceFadeoutInput
    stack_cursor = state.push_word(stack_cursor, 238)
    updated_audio_values_3 = advance_fadeout(state, AdvanceFadeoutInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 238)))
    auxiliary_cursor = updated_audio_values_3.auxiliary_cursor
    channel_cursor = updated_audio_values_3.channel_cursor
    conditions = updated_audio_values_3.conditions
    count_and_data = updated_audio_values_3.count_and_data
    lookup_cursor = updated_audio_values_3.lookup_cursor
    parameter_cursor = updated_audio_values_3.parameter_cursor
    sample = updated_audio_values_3.sample
    stack_cursor = updated_audio_values_3.stack_cursor
    # source-effect driver:00ee:call
    from .business_loaders import dispatch_sound_command
    from .contexts import DispatchSoundCommandInput
    stack_cursor = state.push_word(stack_cursor, 241)
    updated_audio_values_4 = dispatch_sound_command(state, DispatchSoundCommandInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 241)))
    auxiliary_cursor = updated_audio_values_4.auxiliary_cursor
    channel_cursor = updated_audio_values_4.channel_cursor
    conditions = updated_audio_values_4.conditions
    count_and_data = updated_audio_values_4.count_and_data
    lookup_cursor = updated_audio_values_4.lookup_cursor
    parameter_cursor = updated_audio_values_4.parameter_cursor
    sample = updated_audio_values_4.sample
    stack_cursor = updated_audio_values_4.stack_cursor
    # source-effect driver:00f1:ld
    observed_byte_5 = state.read(7175)
    sample = u8(observed_byte_5)
    # source-effect driver:00f4:or
    sample = u8(sample | sample)
    conditions = logic_conditions(sample, False)
    # source-effect driver:00f5:call
    if not (conditions & 0x80):
        from .business_hardware import update_sfx_channel_groups
        from .contexts import UpdateSfxChannelGroupsInput
        stack_cursor = state.push_word(stack_cursor, 248)
        updated_audio_values_6 = update_sfx_channel_groups(state, UpdateSfxChannelGroupsInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 248)))
        auxiliary_cursor = updated_audio_values_6.auxiliary_cursor
        channel_cursor = updated_audio_values_6.channel_cursor
        conditions = updated_audio_values_6.conditions
        count_and_data = updated_audio_values_6.count_and_data
        lookup_cursor = updated_audio_values_6.lookup_cursor
        parameter_cursor = updated_audio_values_6.parameter_cursor
        sample = updated_audio_values_6.sample
        stack_cursor = updated_audio_values_6.stack_cursor
    # source-effect driver:00f8:xor
    sample = u8(sample ^ sample)
    conditions = logic_conditions(sample, False)
    # source-effect driver:00f9:ld
    state.write(7193, u8(sample))
    # source-effect driver:00fc:ld
    channel_cursor = u16(7232)
    # source-effect driver:0100:bit
    observed_byte_7 = state.read(u16(channel_cursor + 0))
    conditions = state.memory_bit_conditions(observed_byte_7, 7, conditions, u16(channel_cursor + 0), True)
    # source-effect driver:0104:call
    if not (conditions & 0x40):
        from .business_mailbox import update_rhythm_countdown
        from .contexts import UpdateRhythmCountdownInput
        stack_cursor = state.push_word(stack_cursor, 263)
        updated_audio_values_8 = update_rhythm_countdown(state, UpdateRhythmCountdownInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 263)))
        auxiliary_cursor = updated_audio_values_8.auxiliary_cursor
        channel_cursor = updated_audio_values_8.channel_cursor
        conditions = updated_audio_values_8.conditions
        count_and_data = updated_audio_values_8.count_and_data
        lookup_cursor = updated_audio_values_8.lookup_cursor
        parameter_cursor = updated_audio_values_8.parameter_cursor
        sample = updated_audio_values_8.sample
        stack_cursor = updated_audio_values_8.stack_cursor
    # source-effect driver:0107:ld
    count_and_data = replace_high(count_and_data, 9)
    # source-effect driver:0109:ld
    channel_cursor = u16(7280)
    # source-effect driver:010d:jr
    pass  # Static control continuation is structured below.
    while True:
        # source-effect driver:0128:push
        stack_cursor = state.push_word(stack_cursor, count_and_data)
        # source-effect driver:0129:bit
        observed_byte_9 = state.read(u16(channel_cursor + 0))
        conditions = state.memory_bit_conditions(observed_byte_9, 7, conditions, u16(channel_cursor + 0), True)
        # source-effect driver:012d:call
        if not (conditions & 0x40):
            from .business_channel_update import update_fm_channel
            from .contexts import UpdateFmChannelInput
            stack_cursor = state.push_word(stack_cursor, 304)
            updated_audio_values_10 = update_fm_channel(state, UpdateFmChannelInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 304)))
            auxiliary_cursor = updated_audio_values_10.auxiliary_cursor
            channel_cursor = updated_audio_values_10.channel_cursor
            conditions = updated_audio_values_10.conditions
            count_and_data = updated_audio_values_10.count_and_data
            lookup_cursor = updated_audio_values_10.lookup_cursor
            parameter_cursor = updated_audio_values_10.parameter_cursor
            sample = updated_audio_values_10.sample
            stack_cursor = updated_audio_values_10.stack_cursor
        # source-effect driver:0130:ld
        parameter_cursor = u16(48)
        # source-effect driver:0133:add
        arithmetic_result_11, conditions = sum_word(channel_cursor, parameter_cursor, conditions)
        channel_cursor = u16(arithmetic_result_11)
        # source-effect driver:0135:pop
        saved_audio_word_12, stack_cursor = state.pop_word(stack_cursor)
        count_and_data = u16(saved_audio_word_12)
        # source-effect driver:0136:djnz
        count_and_data = replace_high(count_and_data, u8(high(count_and_data) - 1))
        if high(count_and_data) != 0:
            continue
        break
    # source-effect driver:0138:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return UpdateAudioDriverResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def update_sfx_channel_groups(state: AudioState, inputs: UpdateSfxChannelGroupsInput) -> UpdateSfxChannelGroupsResult:
    """Update sfx channel groups."""
    checked_state(state)
    if type(inputs) is not UpdateSfxChannelGroupsInput:
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
    # source-effect driver:010f:ld
    sample = u8(1)
    # source-effect driver:0111:ld
    state.write(7193, u8(sample))
    # source-effect driver:0114:ld
    channel_cursor = u16(7808)
    # source-effect driver:0118:ld
    count_and_data = replace_high(count_and_data, 6)
    # source-effect driver:011a:call
    from .business_hardware import update_channel_group
    from .contexts import UpdateChannelGroupInput
    stack_cursor = state.push_word(stack_cursor, 285)
    updated_audio_values_1 = update_channel_group(state, UpdateChannelGroupInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 285)))
    auxiliary_cursor = updated_audio_values_1.auxiliary_cursor
    channel_cursor = updated_audio_values_1.channel_cursor
    conditions = updated_audio_values_1.conditions
    count_and_data = updated_audio_values_1.count_and_data
    lookup_cursor = updated_audio_values_1.lookup_cursor
    parameter_cursor = updated_audio_values_1.parameter_cursor
    sample = updated_audio_values_1.sample
    stack_cursor = updated_audio_values_1.stack_cursor
    # source-effect driver:011d:ld
    sample = u8(128)
    # source-effect driver:011f:ld
    state.write(7193, u8(sample))
    # source-effect driver:0122:ld
    count_and_data = replace_high(count_and_data, 2)
    # source-effect driver:0124:ld
    channel_cursor = u16(7712)
    while True:
        # source-effect driver:0128:push
        stack_cursor = state.push_word(stack_cursor, count_and_data)
        # source-effect driver:0129:bit
        observed_byte_2 = state.read(u16(channel_cursor + 0))
        conditions = state.memory_bit_conditions(observed_byte_2, 7, conditions, u16(channel_cursor + 0), True)
        # source-effect driver:012d:call
        if not (conditions & 0x40):
            from .business_channel_update import update_fm_channel
            from .contexts import UpdateFmChannelInput
            stack_cursor = state.push_word(stack_cursor, 304)
            updated_audio_values_3 = update_fm_channel(state, UpdateFmChannelInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 304)))
            auxiliary_cursor = updated_audio_values_3.auxiliary_cursor
            channel_cursor = updated_audio_values_3.channel_cursor
            conditions = updated_audio_values_3.conditions
            count_and_data = updated_audio_values_3.count_and_data
            lookup_cursor = updated_audio_values_3.lookup_cursor
            parameter_cursor = updated_audio_values_3.parameter_cursor
            sample = updated_audio_values_3.sample
            stack_cursor = updated_audio_values_3.stack_cursor
        # source-effect driver:0130:ld
        parameter_cursor = u16(48)
        # source-effect driver:0133:add
        arithmetic_result_4, conditions = sum_word(channel_cursor, parameter_cursor, conditions)
        channel_cursor = u16(arithmetic_result_4)
        # source-effect driver:0135:pop
        saved_audio_word_5, stack_cursor = state.pop_word(stack_cursor)
        count_and_data = u16(saved_audio_word_5)
        # source-effect driver:0136:djnz
        count_and_data = replace_high(count_and_data, u8(high(count_and_data) - 1))
        if high(count_and_data) != 0:
            continue
        break
    # source-effect driver:0138:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return UpdateSfxChannelGroupsResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def update_channel_group(state: AudioState, inputs: UpdateChannelGroupInput) -> UpdateChannelGroupResult:
    """Update channel group."""
    checked_state(state)
    if type(inputs) is not UpdateChannelGroupInput:
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
        # source-effect driver:0128:push
        stack_cursor = state.push_word(stack_cursor, count_and_data)
        # source-effect driver:0129:bit
        observed_byte_1 = state.read(u16(channel_cursor + 0))
        conditions = state.memory_bit_conditions(observed_byte_1, 7, conditions, u16(channel_cursor + 0), True)
        # source-effect driver:012d:call
        if not (conditions & 0x40):
            from .business_channel_update import update_fm_channel
            from .contexts import UpdateFmChannelInput
            stack_cursor = state.push_word(stack_cursor, 304)
            updated_audio_values_2 = update_fm_channel(state, UpdateFmChannelInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 304)))
            auxiliary_cursor = updated_audio_values_2.auxiliary_cursor
            channel_cursor = updated_audio_values_2.channel_cursor
            conditions = updated_audio_values_2.conditions
            count_and_data = updated_audio_values_2.count_and_data
            lookup_cursor = updated_audio_values_2.lookup_cursor
            parameter_cursor = updated_audio_values_2.parameter_cursor
            sample = updated_audio_values_2.sample
            stack_cursor = updated_audio_values_2.stack_cursor
        # source-effect driver:0130:ld
        parameter_cursor = u16(48)
        # source-effect driver:0133:add
        arithmetic_result_3, conditions = sum_word(channel_cursor, parameter_cursor, conditions)
        channel_cursor = u16(arithmetic_result_3)
        # source-effect driver:0135:pop
        saved_audio_word_4, stack_cursor = state.pop_word(stack_cursor)
        count_and_data = u16(saved_audio_word_4)
        # source-effect driver:0136:djnz
        count_and_data = replace_high(count_and_data, u8(high(count_and_data) - 1))
        if high(count_and_data) != 0:
            continue
        break
    # source-effect driver:0138:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return UpdateChannelGroupResult(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor).validate(state)

def write_fm_port_one(state: AudioState, inputs: WriteFmPortOneInput) -> WriteFmPortOneResult:
    """Write fm port one."""
    checked_state(state)
    if type(inputs) is not WriteFmPortOneInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    channel_cursor = inputs.channel_cursor
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect driver:04bf:ld
    state.write(16386, u8(sample))
    # source-effect driver:04c2:rst
    from .business_hardware import wait_fm_ready
    from .contexts import WaitFmReadyInput
    stack_cursor = state.push_word(stack_cursor, 1219)
    updated_audio_values_1 = wait_fm_ready(state, WaitFmReadyInput(conditions=conditions, sample=sample, stack_cursor=stack_cursor, continuation=Continuation("driver", 1219)))
    conditions = updated_audio_values_1.conditions
    sample = updated_audio_values_1.sample
    stack_cursor = updated_audio_values_1.stack_cursor
    # source-effect driver:04c3:ld
    sample = u8(low(count_and_data))
    # source-effect driver:04c4:ld
    state.write(16387, u8(sample))
    # source-effect driver:04c7:ret
    stack_cursor = state.consume_return(stack_cursor, inputs.continuation)
    return WriteFmPortOneResult(channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, sample=sample, stack_cursor=stack_cursor).validate(state)
