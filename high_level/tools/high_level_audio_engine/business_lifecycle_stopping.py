"""Actual lifecycle algorithms with ordered live bus effects, fixed-width contexts and original stack/service boundaries. No original byte payload or saved-body fallback."""
from .domain import AudioState, AudioBoundary, Continuation, AlternateGroup, Byte, Word, byte, word, checked_state, u8, u16, low, high, replace_low, replace_high, logic_conditions, sum_byte, difference_byte, comparison_conditions, increment_byte, decrement_byte, sum_word, difference_word, tested_bit_conditions, copy_byte_conditions
from .contexts_lifecycle import DriverLifecycle
from .business_lifecycle_reset import reset_driver_and_channels, silence_psg_and_finish

def run_stop_psg_pair(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Stop each of the two original eligible PSG records, retaining saved count and channel stride on the shared stack."""
    lifecycle.channel_address = u16(7712)
    lifecycle.transfer_word = replace_high(lifecycle.transfer_word, 2)
    lifecycle.working_byte = u8(128)
    state.write(7193, u8(lifecycle.working_byte))
    while True:
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.transfer_word)
        channel_flags = state.read(u16(lifecycle.channel_address + 0))
        lifecycle.condition_bits = state.memory_bit_conditions(channel_flags, 7, lifecycle.condition_bits, u16(lifecycle.channel_address + 0), True)
        if not lifecycle.condition_bits & 64:
            from .business_loaders import stage_channel_stop_continuations
            from .contexts import StageChannelStopContinuationsInput
            lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1352)
            stage_channel_stop_continuations_outcome = stage_channel_stop_continuations(state, StageChannelStopContinuationsInput(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1352)))
            lifecycle.paired_channel_address = stage_channel_stop_continuations_outcome.auxiliary_cursor
            lifecycle.channel_address = stage_channel_stop_continuations_outcome.channel_cursor
            lifecycle.condition_bits = stage_channel_stop_continuations_outcome.conditions
            lifecycle.transfer_word = stage_channel_stop_continuations_outcome.count_and_data
            lifecycle.source_cursor = stage_channel_stop_continuations_outcome.lookup_cursor
            lifecycle.secondary_cursor = stage_channel_stop_continuations_outcome.parameter_cursor
            lifecycle.working_byte = stage_channel_stop_continuations_outcome.sample
            lifecycle.return_stack = stage_channel_stop_continuations_outcome.stack_cursor
        lifecycle.secondary_cursor = u16(48)
        adjusted_value, lifecycle.condition_bits = sum_word(lifecycle.channel_address, lifecycle.secondary_cursor, lifecycle.condition_bits)
        lifecycle.channel_address = u16(adjusted_value)
        saved_context_word, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
        lifecycle.transfer_word = u16(saved_context_word)
        lifecycle.transfer_word = replace_high(lifecycle.transfer_word, u8(high(lifecycle.transfer_word) - 1))
        if high(lifecycle.transfer_word) != 0:
            continue
        break
    lifecycle.return_stack = state.consume_return(lifecycle.return_stack, continuation)
    return

def run_stage_channel_stop_continuations(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Push the current source cursor twice as the actual stop-tail view frames, then enter shared release; these are not synthetic new return addresses."""
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.source_cursor)
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.source_cursor)
    pass
    return release_channel_and_restore_views(state, lifecycle, continuation)

def run_process_driver_stop_mode(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Handle idle, signed restore/reset and positive nonlocal stop modes, preserving the original extra stack pop before the stopping chain."""
    lifecycle.source_cursor = u16(7184)
    live_source_byte = state.read(lifecycle.source_cursor)
    lifecycle.working_byte = u8(live_source_byte)
    lifecycle.working_byte = u8(lifecycle.working_byte | lifecycle.working_byte)
    lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
    if bool(lifecycle.condition_bits & 64):
        lifecycle.return_stack = state.consume_return(lifecycle.return_stack, continuation)
        return
    if bool(lifecycle.condition_bits & 128):
        lifecycle.working_byte = u8(lifecycle.working_byte ^ lifecycle.working_byte)
        lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
        state.write(lifecycle.source_cursor, u8(lifecycle.working_byte))
        fade_counter = state.read(7181)
        lifecycle.working_byte = u8(fade_counter)
        lifecycle.working_byte = u8(lifecycle.working_byte | lifecycle.working_byte)
        lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
        if not lifecycle.condition_bits & 64:
            return reset_driver_and_channels(state, lifecycle, continuation)
        else:
            return restore_channel_pan_banks(state, lifecycle, continuation)
    else:
        saved_context_word, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
        lifecycle.secondary_cursor = u16(saved_context_word)
        next_value, lifecycle.condition_bits = decrement_byte(lifecycle.working_byte, lifecycle.condition_bits)
        lifecycle.working_byte = u8(next_value)
        if not lifecycle.condition_bits & 64:
            lifecycle.return_stack = state.consume_return(lifecycle.return_stack, continuation)
            return
        state.write(lifecycle.source_cursor, u8(2))
        pass
        return silence_stop_chip_registers(state, lifecycle, continuation)

def run_set_all_channel_activity(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Set or clear activity across ten records; clearing also calls real key-off and shared PSG silence, while restoring saved live cursors."""
    state.write(7185, u8(lifecycle.working_byte))
    lifecycle.working_byte = u8(lifecycle.working_byte | lifecycle.working_byte)
    lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
    if bool(lifecycle.condition_bits & 64):
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.channel_address)
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.secondary_cursor)
        lifecycle.channel_address = u16(7232)
        lifecycle.transfer_word = replace_high(lifecycle.transfer_word, 10)
        lifecycle.secondary_cursor = u16(48)
        while True:
            channel_flags = state.read(u16(lifecycle.channel_address + 0))
            state.write(u16(lifecycle.channel_address + 0), u8(channel_flags | 128))
            adjusted_value, lifecycle.condition_bits = sum_word(lifecycle.channel_address, lifecycle.secondary_cursor, lifecycle.condition_bits)
            lifecycle.channel_address = u16(adjusted_value)
            lifecycle.transfer_word = replace_high(lifecycle.transfer_word, u8(high(lifecycle.transfer_word) - 1))
            if high(lifecycle.transfer_word) != 0:
                continue
            break
        saved_context_word, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
        lifecycle.secondary_cursor = u16(saved_context_word)
        saved_context_word_2, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
        lifecycle.channel_address = u16(saved_context_word_2)
        lifecycle.return_stack = state.consume_return(lifecycle.return_stack, continuation)
        return
    else:
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.channel_address)
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.secondary_cursor)
        lifecycle.channel_address = u16(7232)
        lifecycle.transfer_word = replace_high(lifecycle.transfer_word, 10)
        lifecycle.secondary_cursor = u16(48)
        while True:
            channel_flags_2 = state.read(u16(lifecycle.channel_address + 0))
            state.write(u16(lifecycle.channel_address + 0), u8(channel_flags_2 & 127))
            from .business_envelopes import send_key_off_after_gate
            from .contexts import SendKeyOffAfterGateInput
            lifecycle.return_stack = state.push_word(lifecycle.return_stack, 3149)
            send_key_off_after_gate_outcome = send_key_off_after_gate(state, SendKeyOffAfterGateInput(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 3149)))
            lifecycle.paired_channel_address = send_key_off_after_gate_outcome.auxiliary_cursor
            lifecycle.channel_address = send_key_off_after_gate_outcome.channel_cursor
            lifecycle.condition_bits = send_key_off_after_gate_outcome.conditions
            lifecycle.transfer_word = send_key_off_after_gate_outcome.count_and_data
            lifecycle.source_cursor = send_key_off_after_gate_outcome.lookup_cursor
            lifecycle.secondary_cursor = send_key_off_after_gate_outcome.parameter_cursor
            lifecycle.working_byte = send_key_off_after_gate_outcome.sample
            lifecycle.return_stack = send_key_off_after_gate_outcome.stack_cursor
            adjusted_value_2, lifecycle.condition_bits = sum_word(lifecycle.channel_address, lifecycle.secondary_cursor, lifecycle.condition_bits)
            lifecycle.channel_address = u16(adjusted_value_2)
            lifecycle.transfer_word = replace_high(lifecycle.transfer_word, u8(high(lifecycle.transfer_word) - 1))
            if high(lifecycle.transfer_word) != 0:
                continue
            break
        saved_context_word_3, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
        lifecycle.secondary_cursor = u16(saved_context_word_3)
        saved_context_word_4, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
        lifecycle.channel_address = u16(saved_context_word_4)
        pass
        return silence_psg_and_finish(state, lifecycle, continuation)

def run_stop_channel_after_operator_reset(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Reset voice operators through their real service then enter the shared channel-release tail."""
    from .business_envelopes import reset_voice_operators
    from .contexts import ResetVoiceOperatorsInput
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 3274)
    reset_voice_operators_outcome = reset_voice_operators(state, ResetVoiceOperatorsInput(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 3274)))
    lifecycle.paired_channel_address = reset_voice_operators_outcome.auxiliary_cursor
    lifecycle.channel_address = reset_voice_operators_outcome.channel_cursor
    lifecycle.condition_bits = reset_voice_operators_outcome.conditions
    lifecycle.transfer_word = reset_voice_operators_outcome.count_and_data
    lifecycle.source_cursor = reset_voice_operators_outcome.lookup_cursor
    lifecycle.secondary_cursor = reset_voice_operators_outcome.parameter_cursor
    lifecycle.working_byte = reset_voice_operators_outcome.sample
    lifecycle.return_stack = reset_voice_operators_outcome.stack_cursor
    pass
    return release_channel_and_restore_views(state, lifecycle, continuation)

def run_stop_and_release_channel(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Enter the single shared release/view-restoration tail with the caller-provided stack contract."""
    return release_channel_and_restore_views(state, lifecycle, continuation)

def release_channel_and_restore_views(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Clear activity and key-off the live channel, choose paired views, restore shared music voice/envelope/timer state when eligible, then unwind the original two saved view words. Unexpected returns remain boundaries."""
    channel_flags = state.read(u16(lifecycle.channel_address + 0))
    state.write(u16(lifecycle.channel_address + 0), u8(channel_flags & 127))
    lifecycle.working_byte = u8(31)
    state.write(7189, u8(lifecycle.working_byte))
    from .business_envelopes import send_key_off
    from .contexts import SendKeyOffInput
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 3635)
    send_key_off_outcome = send_key_off(state, SendKeyOffInput(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 3635)))
    lifecycle.paired_channel_address = send_key_off_outcome.auxiliary_cursor
    lifecycle.channel_address = send_key_off_outcome.channel_cursor
    lifecycle.condition_bits = send_key_off_outcome.conditions
    lifecycle.transfer_word = send_key_off_outcome.count_and_data
    lifecycle.source_cursor = send_key_off_outcome.lookup_cursor
    lifecycle.secondary_cursor = send_key_off_outcome.parameter_cursor
    lifecycle.working_byte = send_key_off_outcome.sample
    lifecycle.return_stack = send_key_off_outcome.stack_cursor
    channel_kind = state.read(u16(lifecycle.channel_address + 1))
    lifecycle.transfer_word = replace_low(lifecycle.transfer_word, channel_kind)
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.channel_address)
    from .business_loaders import choose_channel_views
    from .contexts import ChooseChannelViewsInput
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 3643)
    choose_channel_views_outcome = choose_channel_views(state, ChooseChannelViewsInput(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 3643)))
    lifecycle.paired_channel_address = choose_channel_views_outcome.auxiliary_cursor
    lifecycle.channel_address = choose_channel_views_outcome.channel_cursor
    lifecycle.condition_bits = choose_channel_views_outcome.conditions
    lifecycle.transfer_word = choose_channel_views_outcome.count_and_data
    lifecycle.source_cursor = choose_channel_views_outcome.lookup_cursor
    lifecycle.secondary_cursor = choose_channel_views_outcome.parameter_cursor
    lifecycle.working_byte = choose_channel_views_outcome.sample
    lifecycle.return_stack = choose_channel_views_outcome.stack_cursor
    channel_view_mode = state.read(7193)
    lifecycle.working_byte = u8(channel_view_mode)
    lifecycle.working_byte = u8(lifecycle.working_byte | lifecycle.working_byte)
    lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
    if not bool(lifecycle.condition_bits & 64):
        lifecycle.working_byte = u8(lifecycle.working_byte ^ lifecycle.working_byte)
        lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
        state.write(7192, u8(lifecycle.working_byte))
        channel_flags_2 = state.read(u16(lifecycle.paired_channel_address + 0))
        lifecycle.condition_bits = state.memory_bit_conditions(channel_flags_2, 7, lifecycle.condition_bits, u16(lifecycle.paired_channel_address + 0), True)
        if bool(lifecycle.condition_bits & 64):
            lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.source_cursor)
            music_voice_source = state.read_word_le(7223)
            lifecycle.source_cursor = u16(music_voice_source)
        else:
            channel_kind_3 = state.read(u16(lifecycle.channel_address + 1))
            lifecycle.working_byte = u8(channel_kind_3)
            channel_kind_4 = state.read(u16(lifecycle.paired_channel_address + 1))
            lifecycle.condition_bits = comparison_conditions(lifecycle.working_byte, channel_kind_4)
            if not lifecycle.condition_bits & 64:
                lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.source_cursor)
                music_voice_source_2 = state.read_word_le(7223)
                lifecycle.source_cursor = u16(music_voice_source_2)
            else:
                lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.paired_channel_address)
                voice_source_low = state.read(u16(lifecycle.paired_channel_address + 42))
                lifecycle.source_cursor = replace_low(lifecycle.source_cursor, voice_source_low)
                voice_source_high = state.read(u16(lifecycle.paired_channel_address + 43))
                lifecycle.source_cursor = replace_high(lifecycle.source_cursor, voice_source_high)
                pass
        saved_context_word, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
        lifecycle.channel_address = u16(saved_context_word)
        channel_flags_3 = state.read(u16(lifecycle.channel_address + 0))
        state.write(u16(lifecycle.channel_address + 0), u8(channel_flags_3 & 251))
        channel_kind_2 = state.read(u16(lifecycle.channel_address + 1))
        lifecycle.condition_bits = state.memory_bit_conditions(channel_kind_2, 7, lifecycle.condition_bits, u16(lifecycle.channel_address + 1), True)
        if not lifecycle.condition_bits & 64:
            channel_flags_4 = state.read(u16(lifecycle.channel_address + 0))
            lifecycle.condition_bits = state.memory_bit_conditions(channel_flags_4, 0, lifecycle.condition_bits, u16(lifecycle.channel_address + 0), True)
            if not bool(lifecycle.condition_bits & 64):
                envelope_source_high = state.read(u16(lifecycle.channel_address + 26))
                lifecycle.working_byte = u8(envelope_source_high)
                lifecycle.working_byte = u8(lifecycle.working_byte | lifecycle.working_byte)
                lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
                if not not lifecycle.condition_bits & 128:
                    state.write(32529, u8(lifecycle.working_byte))
                pass
        else:
            channel_flags_5 = state.read(u16(lifecycle.channel_address + 0))
            lifecycle.condition_bits = state.memory_bit_conditions(channel_flags_5, 7, lifecycle.condition_bits, u16(lifecycle.channel_address + 0), True)
            if not bool(lifecycle.condition_bits & 64):
                lifecycle.working_byte = u8(2)
                channel_kind_5 = state.read(u16(lifecycle.channel_address + 1))
                lifecycle.condition_bits = comparison_conditions(lifecycle.working_byte, channel_kind_5)
                if not not lifecycle.condition_bits & 64:
                    lifecycle.working_byte = u8(79)
                    channel_flags_6 = state.read(u16(lifecycle.channel_address + 0))
                    lifecycle.condition_bits = state.memory_bit_conditions(channel_flags_6, 0, lifecycle.condition_bits, u16(lifecycle.channel_address + 0), True)
                    if not not lifecycle.condition_bits & 64:
                        lifecycle.working_byte = u8(lifecycle.working_byte & 15)
                        lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, True)
                    from .business_sequence import write_timer_control
                    from .contexts import WriteTimerControlInput
                    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 3719)
                    write_timer_control_outcome = write_timer_control(state, WriteTimerControlInput(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 3719)))
                    lifecycle.channel_address = write_timer_control_outcome.channel_cursor
                    lifecycle.condition_bits = write_timer_control_outcome.conditions
                    lifecycle.transfer_word = write_timer_control_outcome.count_and_data
                    lifecycle.source_cursor = write_timer_control_outcome.lookup_cursor
                    lifecycle.secondary_cursor = write_timer_control_outcome.parameter_cursor
                    lifecycle.working_byte = write_timer_control_outcome.sample
                    lifecycle.return_stack = write_timer_control_outcome.stack_cursor
                instrument_selector = state.read(u16(lifecycle.channel_address + 8))
                lifecycle.working_byte = u8(instrument_selector)
                lifecycle.working_byte = u8(lifecycle.working_byte | lifecycle.working_byte)
                lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
                if not lifecycle.condition_bits & 128:
                    lifecycle.transfer_word = replace_high(lifecycle.transfer_word, lifecycle.working_byte)
                    from .business_voice import offset_instrument
                    from .contexts import OffsetInstrumentInput
                    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 3735)
                    offset_instrument_outcome = offset_instrument(state, OffsetInstrumentInput(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 3735)))
                    lifecycle.channel_address = offset_instrument_outcome.channel_cursor
                    lifecycle.condition_bits = offset_instrument_outcome.conditions
                    lifecycle.transfer_word = offset_instrument_outcome.count_and_data
                    lifecycle.source_cursor = offset_instrument_outcome.lookup_cursor
                    lifecycle.secondary_cursor = offset_instrument_outcome.parameter_cursor
                    lifecycle.working_byte = offset_instrument_outcome.sample
                    lifecycle.return_stack = offset_instrument_outcome.stack_cursor
                    from .business_voice import load_instrument
                    from .contexts import LoadInstrumentInput
                    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 3738)
                    load_instrument_outcome = load_instrument(state, LoadInstrumentInput(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 3738)))
                    lifecycle.channel_address = load_instrument_outcome.channel_cursor
                    lifecycle.condition_bits = load_instrument_outcome.conditions
                    lifecycle.transfer_word = load_instrument_outcome.count_and_data
                    lifecycle.source_cursor = load_instrument_outcome.lookup_cursor
                    lifecycle.secondary_cursor = load_instrument_outcome.parameter_cursor
                    lifecycle.working_byte = load_instrument_outcome.sample
                    lifecycle.return_stack = load_instrument_outcome.stack_cursor
                    voice_envelope = state.read(u16(lifecycle.channel_address + 24))
                    lifecycle.working_byte = u8(voice_envelope)
                    lifecycle.working_byte = u8(lifecycle.working_byte | lifecycle.working_byte)
                    lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
                    if not not lifecycle.condition_bits & 128:
                        envelope_source_low = state.read(u16(lifecycle.channel_address + 25))
                        lifecycle.secondary_cursor = replace_low(lifecycle.secondary_cursor, envelope_source_low)
                        envelope_source_high_2 = state.read(u16(lifecycle.channel_address + 26))
                        lifecycle.secondary_cursor = replace_high(lifecycle.secondary_cursor, envelope_source_high_2)
                        from .business_sequence import write_fm_parameters
                        from .contexts import WriteFmParametersInput
                        lifecycle.return_stack = state.push_word(lifecycle.return_stack, 3754)
                        write_fm_parameters_outcome_2 = write_fm_parameters(state, WriteFmParametersInput(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 3754)))
                        lifecycle.channel_address = write_fm_parameters_outcome_2.channel_cursor
                        lifecycle.condition_bits = write_fm_parameters_outcome_2.conditions
                        lifecycle.transfer_word = write_fm_parameters_outcome_2.count_and_data
                        lifecycle.source_cursor = write_fm_parameters_outcome_2.lookup_cursor
                        lifecycle.secondary_cursor = write_fm_parameters_outcome_2.parameter_cursor
                        lifecycle.working_byte = write_fm_parameters_outcome_2.sample
                        lifecycle.return_stack = write_fm_parameters_outcome_2.stack_cursor
                else:
                    from .business_sequence import select_banked_instrument
                    from .contexts import SelectBankedInstrumentInput
                    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 3729)
                    select_banked_instrument_outcome = select_banked_instrument(state, SelectBankedInstrumentInput(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 3729)))
                    lifecycle.channel_address = select_banked_instrument_outcome.channel_cursor
                    lifecycle.condition_bits = select_banked_instrument_outcome.conditions
                    lifecycle.transfer_word = select_banked_instrument_outcome.count_and_data
                    lifecycle.source_cursor = select_banked_instrument_outcome.lookup_cursor
                    lifecycle.secondary_cursor = select_banked_instrument_outcome.parameter_cursor
                    lifecycle.working_byte = select_banked_instrument_outcome.sample
                    lifecycle.return_stack = select_banked_instrument_outcome.stack_cursor
                    pass
                    from .business_sequence import write_fm_parameters
                    from .contexts import WriteFmParametersInput
                    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 3754)
                    write_fm_parameters_outcome = write_fm_parameters(state, WriteFmParametersInput(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 3754)))
                    lifecycle.channel_address = write_fm_parameters_outcome.channel_cursor
                    lifecycle.condition_bits = write_fm_parameters_outcome.conditions
                    lifecycle.transfer_word = write_fm_parameters_outcome.count_and_data
                    lifecycle.source_cursor = write_fm_parameters_outcome.lookup_cursor
                    lifecycle.secondary_cursor = write_fm_parameters_outcome.parameter_cursor
                    lifecycle.working_byte = write_fm_parameters_outcome.sample
                    lifecycle.return_stack = write_fm_parameters_outcome.stack_cursor
    saved_context_word_2, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
    lifecycle.channel_address = u16(saved_context_word_2)
    saved_context_word_3, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
    lifecycle.source_cursor = u16(saved_context_word_3)
    saved_context_word_4, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
    lifecycle.source_cursor = u16(saved_context_word_4)
    lifecycle.return_stack = state.consume_return(lifecycle.return_stack, continuation)
    return

def silence_stop_chip_registers(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Write the original two FM pan banks and seven key-off selectors, preserving accumulator/count stack frames, then silence PSG and acknowledge the command."""
    from .business_loaders import silence_psg_channels
    from .contexts import SilencePsgChannelsInput
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 2087)
    silence_psg_channels_outcome = silence_psg_channels(state, SilencePsgChannelsInput(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 2087)))
    lifecycle.paired_channel_address = silence_psg_channels_outcome.auxiliary_cursor
    lifecycle.channel_address = silence_psg_channels_outcome.channel_cursor
    lifecycle.condition_bits = silence_psg_channels_outcome.conditions
    lifecycle.transfer_word = silence_psg_channels_outcome.count_and_data
    lifecycle.source_cursor = silence_psg_channels_outcome.lookup_cursor
    lifecycle.secondary_cursor = silence_psg_channels_outcome.parameter_cursor
    lifecycle.working_byte = silence_psg_channels_outcome.sample
    lifecycle.return_stack = silence_psg_channels_outcome.stack_cursor
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.transfer_word)
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.working_byte << 8 | lifecycle.condition_bits)
    lifecycle.transfer_word = replace_high(lifecycle.transfer_word, 3)
    lifecycle.working_byte = u8(180)
    lifecycle.transfer_word = replace_low(lifecycle.transfer_word, 0)
    while True:
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.working_byte << 8 | lifecycle.condition_bits)
        from .business_hardware import write_fm_port_zero_entry
        from .contexts import WriteFmPortZeroEntryInput
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, 2097)
        write_fm_port_zero_entry_outcome = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 2097)))
        lifecycle.channel_address = write_fm_port_zero_entry_outcome.channel_cursor
        lifecycle.condition_bits = write_fm_port_zero_entry_outcome.conditions
        lifecycle.transfer_word = write_fm_port_zero_entry_outcome.count_and_data
        lifecycle.working_byte = write_fm_port_zero_entry_outcome.sample
        lifecycle.return_stack = write_fm_port_zero_entry_outcome.stack_cursor
        saved_context_word, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
        lifecycle.working_byte, lifecycle.condition_bits = (high(saved_context_word), low(saved_context_word))
        next_value, lifecycle.condition_bits = increment_byte(lifecycle.working_byte, lifecycle.condition_bits)
        lifecycle.working_byte = u8(next_value)
        lifecycle.transfer_word = replace_high(lifecycle.transfer_word, u8(high(lifecycle.transfer_word) - 1))
        if high(lifecycle.transfer_word) != 0:
            continue
        break
    lifecycle.transfer_word = replace_high(lifecycle.transfer_word, 3)
    lifecycle.working_byte = u8(180)
    while True:
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.working_byte << 8 | lifecycle.condition_bits)
        from .business_hardware import write_fm_port_one
        from .contexts import WriteFmPortOneInput
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, 2109)
        write_fm_port_one_outcome = write_fm_port_one(state, WriteFmPortOneInput(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 2109)))
        lifecycle.channel_address = write_fm_port_one_outcome.channel_cursor
        lifecycle.condition_bits = write_fm_port_one_outcome.conditions
        lifecycle.transfer_word = write_fm_port_one_outcome.count_and_data
        lifecycle.working_byte = write_fm_port_one_outcome.sample
        lifecycle.return_stack = write_fm_port_one_outcome.stack_cursor
        saved_context_word_2, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
        lifecycle.working_byte, lifecycle.condition_bits = (high(saved_context_word_2), low(saved_context_word_2))
        next_value_2, lifecycle.condition_bits = increment_byte(lifecycle.working_byte, lifecycle.condition_bits)
        lifecycle.working_byte = u8(next_value_2)
        lifecycle.transfer_word = replace_high(lifecycle.transfer_word, u8(high(lifecycle.transfer_word) - 1))
        if high(lifecycle.transfer_word) != 0:
            continue
        break
    lifecycle.transfer_word = replace_low(lifecycle.transfer_word, 0)
    lifecycle.transfer_word = replace_high(lifecycle.transfer_word, 7)
    lifecycle.working_byte = u8(40)
    while True:
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.working_byte << 8 | lifecycle.condition_bits)
        from .business_hardware import write_fm_port_zero_entry
        from .contexts import WriteFmPortZeroEntryInput
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, 2121)
        write_fm_port_zero_entry_outcome_2 = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 2121)))
        lifecycle.channel_address = write_fm_port_zero_entry_outcome_2.channel_cursor
        lifecycle.condition_bits = write_fm_port_zero_entry_outcome_2.conditions
        lifecycle.transfer_word = write_fm_port_zero_entry_outcome_2.count_and_data
        lifecycle.working_byte = write_fm_port_zero_entry_outcome_2.sample
        lifecycle.return_stack = write_fm_port_zero_entry_outcome_2.stack_cursor
        next_value_3, lifecycle.condition_bits = increment_byte(low(lifecycle.transfer_word), lifecycle.condition_bits)
        lifecycle.transfer_word = replace_low(lifecycle.transfer_word, next_value_3)
        saved_context_word_3, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
        lifecycle.working_byte, lifecycle.condition_bits = (high(saved_context_word_3), low(saved_context_word_3))
        lifecycle.transfer_word = replace_high(lifecycle.transfer_word, u8(high(lifecycle.transfer_word) - 1))
        if high(lifecycle.transfer_word) != 0:
            continue
        break
    saved_context_word_4, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
    lifecycle.working_byte, lifecycle.condition_bits = (high(saved_context_word_4), low(saved_context_word_4))
    saved_context_word_5, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
    lifecycle.transfer_word = u16(saved_context_word_5)
    return silence_psg_and_finish(state, lifecycle, continuation)

def restore_channel_pan_banks(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Restore pan through original activity/eligibility gates across six music and eight effect views, with live FM outcomes and original channel stride."""
    lifecycle.channel_address = u16(7280)
    lifecycle.transfer_word = replace_high(lifecycle.transfer_word, 6)
    while True:
        activity_mode = state.read(7185)
        lifecycle.working_byte = u8(activity_mode)
        lifecycle.working_byte = u8(lifecycle.working_byte | lifecycle.working_byte)
        lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
        if not lifecycle.condition_bits & 64:
            stereo_bits = state.read(u16(lifecycle.channel_address + 10))
            lifecycle.transfer_word = replace_low(lifecycle.transfer_word, stereo_bits)
            lifecycle.working_byte = u8(180)
            from .business_hardware import write_channel_fm_register
            from .contexts import WriteChannelFmRegisterInput
            lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1873)
            write_channel_fm_register_outcome = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1873)))
            lifecycle.channel_address = write_channel_fm_register_outcome.channel_cursor
            lifecycle.condition_bits = write_channel_fm_register_outcome.conditions
            lifecycle.transfer_word = write_channel_fm_register_outcome.count_and_data
            lifecycle.working_byte = write_channel_fm_register_outcome.sample
            lifecycle.return_stack = write_channel_fm_register_outcome.stack_cursor
        else:
            channel_flags = state.read(u16(lifecycle.channel_address + 0))
            lifecycle.condition_bits = state.memory_bit_conditions(channel_flags, 7, lifecycle.condition_bits, u16(lifecycle.channel_address + 0), True)
            if not bool(lifecycle.condition_bits & 64):
                stereo_bits_2 = state.read(u16(lifecycle.channel_address + 10))
                lifecycle.transfer_word = replace_low(lifecycle.transfer_word, stereo_bits_2)
                lifecycle.working_byte = u8(180)
                from .business_hardware import write_channel_fm_register
                from .contexts import WriteChannelFmRegisterInput
                lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1873)
                write_channel_fm_register_outcome_2 = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1873)))
                lifecycle.channel_address = write_channel_fm_register_outcome_2.channel_cursor
                lifecycle.condition_bits = write_channel_fm_register_outcome_2.conditions
                lifecycle.transfer_word = write_channel_fm_register_outcome_2.count_and_data
                lifecycle.working_byte = write_channel_fm_register_outcome_2.sample
                lifecycle.return_stack = write_channel_fm_register_outcome_2.stack_cursor
        lifecycle.secondary_cursor = u16(48)
        adjusted_value, lifecycle.condition_bits = sum_word(lifecycle.channel_address, lifecycle.secondary_cursor, lifecycle.condition_bits)
        lifecycle.channel_address = u16(adjusted_value)
        lifecycle.transfer_word = replace_high(lifecycle.transfer_word, u8(high(lifecycle.transfer_word) - 1))
        if high(lifecycle.transfer_word) != 0:
            continue
        break
    lifecycle.channel_address = u16(7712)
    lifecycle.transfer_word = replace_high(lifecycle.transfer_word, 8)
    while True:
        channel_flags_2 = state.read(u16(lifecycle.channel_address + 0))
        lifecycle.condition_bits = state.memory_bit_conditions(channel_flags_2, 7, lifecycle.condition_bits, u16(lifecycle.channel_address + 0), True)
        if not bool(lifecycle.condition_bits & 64):
            channel_kind = state.read(u16(lifecycle.channel_address + 1))
            lifecycle.condition_bits = state.memory_bit_conditions(channel_kind, 7, lifecycle.condition_bits, u16(lifecycle.channel_address + 1), True)
            if not not lifecycle.condition_bits & 64:
                stereo_bits_3 = state.read(u16(lifecycle.channel_address + 10))
                lifecycle.transfer_word = replace_low(lifecycle.transfer_word, stereo_bits_3)
                lifecycle.working_byte = u8(180)
                from .business_hardware import write_channel_fm_register
                from .contexts import WriteChannelFmRegisterInput
                lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1904)
                write_channel_fm_register_outcome_3 = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1904)))
                lifecycle.channel_address = write_channel_fm_register_outcome_3.channel_cursor
                lifecycle.condition_bits = write_channel_fm_register_outcome_3.conditions
                lifecycle.transfer_word = write_channel_fm_register_outcome_3.count_and_data
                lifecycle.working_byte = write_channel_fm_register_outcome_3.sample
                lifecycle.return_stack = write_channel_fm_register_outcome_3.stack_cursor
        lifecycle.secondary_cursor = u16(48)
        adjusted_value_2, lifecycle.condition_bits = sum_word(lifecycle.channel_address, lifecycle.secondary_cursor, lifecycle.condition_bits)
        lifecycle.channel_address = u16(adjusted_value_2)
        lifecycle.transfer_word = replace_high(lifecycle.transfer_word, u8(high(lifecycle.transfer_word) - 1))
        if high(lifecycle.transfer_word) != 0:
            continue
        break
    lifecycle.return_stack = state.consume_return(lifecycle.return_stack, continuation)
    return
