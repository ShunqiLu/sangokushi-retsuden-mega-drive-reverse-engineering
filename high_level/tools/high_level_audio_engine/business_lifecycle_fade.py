"""Actual lifecycle algorithms with ordered live bus effects, fixed-width contexts and original stack/service boundaries. No original byte payload or saved-body fallback."""
from .domain import AudioState, AudioBoundary, Continuation, AlternateGroup, Byte, Word, byte, word, checked_state, u8, u16, low, high, replace_low, replace_high, logic_conditions, sum_byte, difference_byte, comparison_conditions, increment_byte, decrement_byte, sum_word, difference_word, tested_bit_conditions, copy_byte_conditions
from .contexts_lifecycle import DriverLifecycle
from .business_lifecycle_reset import reset_driver_and_channels
from .business_lifecycle_shared import finish_sound_command

def run_begin_fadeout(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Set original fade-counter/timer policies then execute the shared fade-channel clear and silence transaction."""
    lifecycle.working_byte = u8(40)
    state.write(7181, u8(lifecycle.working_byte))
    lifecycle.working_byte = u8(6)
    state.write(7183, u8(lifecycle.working_byte))
    state.write(7182, u8(lifecycle.working_byte))
    return clear_fade_channels_and_finish(state, lifecycle, continuation)

def run_clear_fadeout_channel_flags(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Enter the shared fade-channel clear, silence and acknowledgement tail."""
    return clear_fade_channels_and_finish(state, lifecycle, continuation)

def run_advance_fadeout(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Tick the live fade timer, re-arm and decrease remaining fade steps, adjust eligible channel volumes or execute full driver reset at exhaustion."""
    lifecycle.source_cursor = u16(7181)
    live_source_byte = state.read(lifecycle.source_cursor)
    lifecycle.working_byte = u8(live_source_byte)
    lifecycle.working_byte = u8(lifecycle.working_byte | lifecycle.working_byte)
    lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
    if bool(lifecycle.condition_bits & 64):
        lifecycle.return_stack = state.consume_return(lifecycle.return_stack, continuation)
        return
    if bool(lifecycle.condition_bits & 128):
        from .business_loaders import clear_fadeout_channel_flags
        from .contexts import ClearFadeoutChannelFlagsInput
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1956)
        clear_fadeout_channel_flags_outcome = clear_fadeout_channel_flags(state, ClearFadeoutChannelFlagsInput(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1956)))
        lifecycle.paired_channel_address = clear_fadeout_channel_flags_outcome.auxiliary_cursor
        lifecycle.channel_address = clear_fadeout_channel_flags_outcome.channel_cursor
        lifecycle.condition_bits = clear_fadeout_channel_flags_outcome.conditions
        lifecycle.transfer_word = clear_fadeout_channel_flags_outcome.count_and_data
        lifecycle.source_cursor = clear_fadeout_channel_flags_outcome.lookup_cursor
        lifecycle.secondary_cursor = clear_fadeout_channel_flags_outcome.parameter_cursor
        lifecycle.working_byte = clear_fadeout_channel_flags_outcome.sample
        lifecycle.return_stack = clear_fadeout_channel_flags_outcome.stack_cursor
    live_source_byte_2 = state.read(lifecycle.source_cursor)
    state.write(lifecycle.source_cursor, u8(live_source_byte_2 & 127))
    fade_timer = state.read(7183)
    lifecycle.working_byte = u8(fade_timer)
    next_value, lifecycle.condition_bits = decrement_byte(lifecycle.working_byte, lifecycle.condition_bits)
    lifecycle.working_byte = u8(next_value)
    if bool(lifecycle.condition_bits & 64):
        fade_timer_reload = state.read(7182)
        lifecycle.working_byte = u8(fade_timer_reload)
        state.write(7183, u8(lifecycle.working_byte))
        fade_counter = state.read(7181)
        lifecycle.working_byte = u8(fade_counter)
        next_value_2, lifecycle.condition_bits = decrement_byte(lifecycle.working_byte, lifecycle.condition_bits)
        lifecycle.working_byte = u8(next_value_2)
        state.write(7181, u8(lifecycle.working_byte))
        if bool(lifecycle.condition_bits & 64):
            return reset_driver_and_channels(state, lifecycle, continuation)
        else:
            lifecycle.channel_address = u16(7232)
            lifecycle.transfer_word = replace_high(lifecycle.transfer_word, 6)
            while True:
                volume = state.read(u16(lifecycle.channel_address + 6))
                next_value_3, lifecycle.condition_bits = increment_byte(volume, lifecycle.condition_bits)
                state.write(u16(lifecycle.channel_address + 6), u8(next_value_3))
                if not lifecycle.condition_bits & 128:
                    channel_flags = state.read(u16(lifecycle.channel_address + 0))
                    lifecycle.condition_bits = state.memory_bit_conditions(channel_flags, 7, lifecycle.condition_bits, u16(lifecycle.channel_address + 0), True)
                    if not bool(lifecycle.condition_bits & 64):
                        channel_flags_2 = state.read(u16(lifecycle.channel_address + 0))
                        lifecycle.condition_bits = state.memory_bit_conditions(channel_flags_2, 2, lifecycle.condition_bits, u16(lifecycle.channel_address + 0), True)
                        if not not lifecycle.condition_bits & 64:
                            from .business_voice import refresh_instrument_volume
                            from .contexts import RefreshInstrumentVolumeInput
                            lifecycle.return_stack = state.push_word(lifecycle.return_stack, 2015)
                            refresh_instrument_volume_outcome = refresh_instrument_volume(state, RefreshInstrumentVolumeInput(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 2015)))
                            lifecycle.channel_address = refresh_instrument_volume_outcome.channel_cursor
                            lifecycle.condition_bits = refresh_instrument_volume_outcome.conditions
                            lifecycle.transfer_word = refresh_instrument_volume_outcome.count_and_data
                            lifecycle.source_cursor = refresh_instrument_volume_outcome.lookup_cursor
                            lifecycle.secondary_cursor = refresh_instrument_volume_outcome.parameter_cursor
                            lifecycle.working_byte = refresh_instrument_volume_outcome.sample
                            lifecycle.return_stack = refresh_instrument_volume_outcome.stack_cursor
                else:
                    volume_2 = state.read(u16(lifecycle.channel_address + 6))
                    next_value_4, lifecycle.condition_bits = decrement_byte(volume_2, lifecycle.condition_bits)
                    state.write(u16(lifecycle.channel_address + 6), u8(next_value_4))
                    pass
                lifecycle.secondary_cursor = u16(48)
                adjusted_value, lifecycle.condition_bits = sum_word(lifecycle.channel_address, lifecycle.secondary_cursor, lifecycle.condition_bits)
                lifecycle.channel_address = u16(adjusted_value)
                lifecycle.transfer_word = replace_high(lifecycle.transfer_word, u8(high(lifecycle.transfer_word) - 1))
                if high(lifecycle.transfer_word) != 0:
                    continue
                break
            lifecycle.return_stack = state.consume_return(lifecycle.return_stack, continuation)
            return
    else:
        state.write(7183, u8(lifecycle.working_byte))
        lifecycle.return_stack = state.consume_return(lifecycle.return_stack, continuation)
        return

def clear_fade_channels_and_finish(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Clear the original five fade-related channel flags, invoke real PSG silence and acknowledge the command."""
    lifecycle.working_byte = u8(lifecycle.working_byte ^ lifecycle.working_byte)
    lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
    state.write(7232, u8(lifecycle.working_byte))
    state.write(7520, u8(lifecycle.working_byte))
    state.write(7664, u8(lifecycle.working_byte))
    state.write(7568, u8(lifecycle.working_byte))
    state.write(7616, u8(lifecycle.working_byte))
    from .business_loaders import silence_psg_channels
    from .contexts import SilencePsgChannelsInput
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1944)
    silence_psg_channels_outcome = silence_psg_channels(state, SilencePsgChannelsInput(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1944)))
    lifecycle.paired_channel_address = silence_psg_channels_outcome.auxiliary_cursor
    lifecycle.channel_address = silence_psg_channels_outcome.channel_cursor
    lifecycle.condition_bits = silence_psg_channels_outcome.conditions
    lifecycle.transfer_word = silence_psg_channels_outcome.count_and_data
    lifecycle.source_cursor = silence_psg_channels_outcome.lookup_cursor
    lifecycle.secondary_cursor = silence_psg_channels_outcome.parameter_cursor
    lifecycle.working_byte = silence_psg_channels_outcome.sample
    lifecycle.return_stack = silence_psg_channels_outcome.stack_cursor
    pass
    return finish_sound_command(state, lifecycle, continuation)
