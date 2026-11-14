"""Actual lifecycle algorithms with ordered live bus effects, fixed-width contexts and original stack/service boundaries. No original byte payload or saved-body fallback."""
from .domain import AudioState, AudioBoundary, Continuation, AlternateGroup, Byte, Word, byte, word, checked_state, u8, u16, low, high, replace_low, replace_high, logic_conditions, sum_byte, difference_byte, comparison_conditions, increment_byte, decrement_byte, sum_word, difference_word, tested_bit_conditions, copy_byte_conditions
from .contexts_lifecycle import DriverLifecycle, OperatorRelease, RecordInitialization
from .business_lifecycle_shared import copy_live_byte, finish_sound_command

def run_clear_and_reset_driver(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Enter the shared progressive driver/channel reset transaction."""
    return reset_driver_and_channels(state, lifecycle, continuation)

def run_reset_timer_control(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Enter the shared timer-reset and command-acknowledgement tail."""
    return commit_timer_reset(state, lifecycle, continuation)

def run_reset_voice_release(state: AudioState, lifecycle: OperatorRelease, continuation: Continuation) -> None:
    """Select release registers and zero data before the shared four-operator write transaction."""
    lifecycle.working_byte = u8(144)
    lifecycle.transfer_word = replace_low(lifecycle.transfer_word, 0)
    pass
    return write_operator_release_group(state, lifecycle, continuation)

def run_silence_psg_channels(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Enter the single shared live PSG stream/saved-stack/acknowledgement transaction."""
    return silence_psg_and_finish(state, lifecycle, continuation)

def run_tick_note_divider(state: AudioState, lifecycle: RecordInitialization, continuation: Continuation) -> None:
    """Tick the divider, reload at zero and increment ten live note counters with original fixed-width conditions."""
    lifecycle.source_cursor = u16(7187)
    live_source_byte = state.read(lifecycle.source_cursor)
    lifecycle.working_byte = u8(live_source_byte)
    lifecycle.working_byte = u8(lifecycle.working_byte | lifecycle.working_byte)
    lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
    if bool(lifecycle.condition_bits & 64):
        lifecycle.return_stack = state.consume_return(lifecycle.return_stack, continuation)
        return
    live_source_byte_2 = state.read(lifecycle.source_cursor)
    next_value, lifecycle.condition_bits = decrement_byte(live_source_byte_2, lifecycle.condition_bits)
    state.write(lifecycle.source_cursor, u8(next_value))
    if not lifecycle.condition_bits & 64:
        lifecycle.return_stack = state.consume_return(lifecycle.return_stack, continuation)
        return
    divider_reload = state.read(7188)
    lifecycle.working_byte = u8(divider_reload)
    state.write(lifecycle.source_cursor, u8(lifecycle.working_byte))
    lifecycle.source_cursor = u16(7243)
    lifecycle.secondary_cursor = u16(48)
    lifecycle.transfer_word = replace_high(lifecycle.transfer_word, 10)
    while True:
        live_source_byte_3 = state.read(lifecycle.source_cursor)
        next_value_2, lifecycle.condition_bits = increment_byte(live_source_byte_3, lifecycle.condition_bits)
        state.write(lifecycle.source_cursor, u8(next_value_2))
        adjusted_value, lifecycle.condition_bits = sum_word(lifecycle.source_cursor, lifecycle.secondary_cursor, lifecycle.condition_bits)
        lifecycle.source_cursor = u16(adjusted_value)
        lifecycle.transfer_word = replace_high(lifecycle.transfer_word, u8(high(lifecycle.transfer_word) - 1))
        if high(lifecycle.transfer_word) != 0:
            continue
        break
    lifecycle.return_stack = state.consume_return(lifecycle.return_stack, continuation)
    return

def run_reset_operator_release(state: AudioState, lifecycle: OperatorRelease, continuation: Continuation) -> None:
    """Select operator reset registers and data before the shared four-operator write transaction."""
    lifecycle.working_byte = u8(128)
    lifecycle.transfer_word = replace_low(lifecycle.transfer_word, 255)
    return write_operator_release_group(state, lifecycle, continuation)

def run_write_operator_group(state: AudioState, lifecycle: OperatorRelease, continuation: Continuation) -> None:
    """Enter the single four-operator transaction with the supplied live selector/data."""
    return write_operator_release_group(state, lifecycle, continuation)

def reset_driver_and_channels(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Progressively propagate zero across driver state, reset six operator/release views through real services, clear fade state, silence PSG and commit timer reset."""
    lifecycle.source_cursor = u16(7177)
    lifecycle.secondary_cursor = u16(7178)
    lifecycle.transfer_word = u16(918)
    state.write(lifecycle.source_cursor, u8(0))
    while True:
        copy_live_byte(state, lifecycle, continuation)
        state.bus.transfer_boundary('progressive-block-copy')
        if lifecycle.transfer_word == 0:
            break
    lifecycle.channel_address = u16(1507)
    lifecycle.transfer_word = replace_high(lifecycle.transfer_word, 6)
    while True:
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.transfer_word)
        from .business_envelopes import reset_voice_operators
        from .contexts import ResetVoiceOperatorsInput
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, 2046)
        reset_voice_operators_outcome = reset_voice_operators(state, ResetVoiceOperatorsInput(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 2046)))
        lifecycle.paired_channel_address = reset_voice_operators_outcome.auxiliary_cursor
        lifecycle.channel_address = reset_voice_operators_outcome.channel_cursor
        lifecycle.condition_bits = reset_voice_operators_outcome.conditions
        lifecycle.transfer_word = reset_voice_operators_outcome.count_and_data
        lifecycle.source_cursor = reset_voice_operators_outcome.lookup_cursor
        lifecycle.secondary_cursor = reset_voice_operators_outcome.parameter_cursor
        lifecycle.working_byte = reset_voice_operators_outcome.sample
        lifecycle.return_stack = reset_voice_operators_outcome.stack_cursor
        from .business_loaders import reset_voice_release
        from .contexts import ResetVoiceReleaseInput
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, 2049)
        reset_voice_release_outcome = reset_voice_release(state, ResetVoiceReleaseInput(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 2049)))
        lifecycle.channel_address = reset_voice_release_outcome.channel_cursor
        lifecycle.condition_bits = reset_voice_release_outcome.conditions
        lifecycle.transfer_word = reset_voice_release_outcome.count_and_data
        lifecycle.working_byte = reset_voice_release_outcome.sample
        lifecycle.return_stack = reset_voice_release_outcome.stack_cursor
        lifecycle.channel_address = u16(lifecycle.channel_address + 1)
        lifecycle.channel_address = u16(lifecycle.channel_address + 1)
        saved_context_word, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
        lifecycle.transfer_word = u16(saved_context_word)
        lifecycle.transfer_word = replace_high(lifecycle.transfer_word, u8(high(lifecycle.transfer_word) - 1))
        if high(lifecycle.transfer_word) != 0:
            continue
        break
    lifecycle.transfer_word = replace_high(lifecycle.transfer_word, 7)
    lifecycle.working_byte = u8(lifecycle.working_byte ^ lifecycle.working_byte)
    lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
    state.write(7181, u8(lifecycle.working_byte))
    from .business_loaders import silence_psg_channels
    from .contexts import SilencePsgChannelsInput
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 2065)
    silence_psg_channels_outcome = silence_psg_channels(state, SilencePsgChannelsInput(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 2065)))
    lifecycle.paired_channel_address = silence_psg_channels_outcome.auxiliary_cursor
    lifecycle.channel_address = silence_psg_channels_outcome.channel_cursor
    lifecycle.condition_bits = silence_psg_channels_outcome.conditions
    lifecycle.transfer_word = silence_psg_channels_outcome.count_and_data
    lifecycle.source_cursor = silence_psg_channels_outcome.lookup_cursor
    lifecycle.secondary_cursor = silence_psg_channels_outcome.parameter_cursor
    lifecycle.working_byte = silence_psg_channels_outcome.sample
    lifecycle.return_stack = silence_psg_channels_outcome.stack_cursor
    return commit_timer_reset(state, lifecycle, continuation)

def commit_timer_reset(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Store the reset timer value, adopt all live FM port-zero return cells and complete the shared command acknowledgement."""
    lifecycle.working_byte = u8(15)
    state.write(7186, u8(lifecycle.working_byte))
    lifecycle.transfer_word = replace_low(lifecycle.transfer_word, lifecycle.working_byte)
    lifecycle.working_byte = u8(39)
    from .business_hardware import write_fm_port_zero_entry
    from .contexts import WriteFmPortZeroEntryInput
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 2074)
    write_fm_port_zero_entry_outcome = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 2074)))
    lifecycle.channel_address = write_fm_port_zero_entry_outcome.channel_cursor
    lifecycle.condition_bits = write_fm_port_zero_entry_outcome.conditions
    lifecycle.transfer_word = write_fm_port_zero_entry_outcome.count_and_data
    lifecycle.working_byte = write_fm_port_zero_entry_outcome.sample
    lifecycle.return_stack = write_fm_port_zero_entry_outcome.stack_cursor
    pass
    return finish_sound_command(state, lifecycle, continuation)

def silence_psg_and_finish(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Preserve live source/count stack words, stream four original PSG command bytes, restore those words and acknowledge the command."""
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.source_cursor)
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.transfer_word)
    lifecycle.source_cursor = u16(2146)
    lifecycle.transfer_word = replace_high(lifecycle.transfer_word, 4)
    while True:
        live_source_byte = state.read(lifecycle.source_cursor)
        lifecycle.working_byte = u8(live_source_byte)
        state.write(32529, u8(lifecycle.working_byte))
        lifecycle.source_cursor = u16(lifecycle.source_cursor + 1)
        lifecycle.transfer_word = replace_high(lifecycle.transfer_word, u8(high(lifecycle.transfer_word) - 1))
        if high(lifecycle.transfer_word) != 0:
            continue
        break
    saved_context_word, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
    lifecycle.transfer_word = u16(saved_context_word)
    saved_context_word_2, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
    lifecycle.source_cursor = u16(saved_context_word_2)
    pass
    return finish_sound_command(state, lifecycle, continuation)

def write_operator_release_group(state: AudioState, lifecycle: OperatorRelease, continuation: Continuation) -> None:
    """Send four operator fields through real FM calls, preserving AF on the shared stack and advancing the register selector with a declared BYTE stride."""
    lifecycle.transfer_word = replace_high(lifecycle.transfer_word, 4)
    while True:
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.working_byte << 8 | lifecycle.condition_bits)
        from .business_hardware import write_channel_fm_register
        from .contexts import WriteChannelFmRegisterInput
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, 2272)
        write_channel_fm_register_outcome = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 2272)))
        lifecycle.channel_address = write_channel_fm_register_outcome.channel_cursor
        lifecycle.condition_bits = write_channel_fm_register_outcome.conditions
        lifecycle.transfer_word = write_channel_fm_register_outcome.count_and_data
        lifecycle.working_byte = write_channel_fm_register_outcome.sample
        lifecycle.return_stack = write_channel_fm_register_outcome.stack_cursor
        saved_context_word, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
        lifecycle.working_byte, lifecycle.condition_bits = (high(saved_context_word), low(saved_context_word))
        adjusted_value, lifecycle.condition_bits = sum_byte(lifecycle.working_byte, 4)
        lifecycle.working_byte = u8(adjusted_value)
        lifecycle.transfer_word = replace_high(lifecycle.transfer_word, u8(high(lifecycle.transfer_word) - 1))
        if high(lifecycle.transfer_word) != 0:
            continue
        break
    lifecycle.return_stack = state.consume_return(lifecycle.return_stack, continuation)
    return
