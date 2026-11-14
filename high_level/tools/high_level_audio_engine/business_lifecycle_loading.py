"""Actual lifecycle algorithms with ordered live bus effects, fixed-width contexts and original stack/service boundaries. No original byte payload or saved-body fallback."""
from .domain import AudioState, AudioBoundary, Continuation, AlternateGroup, Byte, Word, byte, word, checked_state, u8, u16, low, high, replace_low, replace_high, logic_conditions, sum_byte, difference_byte, comparison_conditions, increment_byte, decrement_byte, sum_word, difference_word, tested_bit_conditions, copy_byte_conditions
from .contexts_lifecycle import DriverLifecycle, RecordInitialization, BankInitialization
from .contexts import DispatchSoundCommandInput, DispatchLoadedSoundCommandInput
from .business_lifecycle_reset import reset_driver_and_channels
from .business_lifecycle_shared import copy_live_byte, finish_sound_command

def run_dispatch_sound_command(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Read the live command latch then execute the complete command classification and music/effect/reset/indirect lifecycle routes."""
    command_latch = state.read(7177)
    lifecycle.working_byte = u8(command_latch)
    lifecycle.condition_bits = tested_bit_conditions(lifecycle.working_byte, 7, lifecycle.condition_bits)
    if bool(lifecycle.condition_bits & 64):
        return reset_driver_and_channels(state, lifecycle, continuation)
    else:
        lifecycle.condition_bits = comparison_conditions(lifecycle.working_byte, 160)
        if bool(lifecycle.condition_bits & 1):
            return load_music_channels(state, lifecycle, continuation)
        else:
            lifecycle.condition_bits = comparison_conditions(lifecycle.working_byte, 176)
            if bool(lifecycle.condition_bits & 1):
                lifecycle.working_byte, lifecycle.condition_bits = difference_byte(lifecycle.working_byte, 160)
                inactive_accumulator = word(state.platform.exchange_alternate_accumulator(lifecycle.working_byte << 8 | lifecycle.condition_bits))
                lifecycle.working_byte, lifecycle.condition_bits = (high(inactive_accumulator), low(inactive_accumulator))
                lifecycle.working_byte = u8(lifecycle.working_byte ^ lifecycle.working_byte)
                lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
                lifecycle.transfer_word = replace_low(lifecycle.transfer_word, 6)
                return load_effect_channels(state, lifecycle, continuation)
            else:
                lifecycle.condition_bits = comparison_conditions(lifecycle.working_byte, 224)
                if bool(lifecycle.condition_bits & 1):
                    lifecycle.working_byte, lifecycle.condition_bits = difference_byte(lifecycle.working_byte, 208)
                    inactive_accumulator_2 = word(state.platform.exchange_alternate_accumulator(lifecycle.working_byte << 8 | lifecycle.condition_bits))
                    lifecycle.working_byte, lifecycle.condition_bits = (high(inactive_accumulator_2), low(inactive_accumulator_2))
                    lifecycle.working_byte = u8(128)
                    lifecycle.transfer_word = replace_low(lifecycle.transfer_word, 2)
                    pass
                    return load_effect_channels(state, lifecycle, continuation)
                else:
                    lifecycle.condition_bits = comparison_conditions(lifecycle.working_byte, 249)
                    if not lifecycle.condition_bits & 1:
                        return reset_driver_and_channels(state, lifecycle, continuation)
                    else:
                        lifecycle.working_byte, lifecycle.condition_bits = difference_byte(lifecycle.working_byte, 224)
                        lifecycle.source_cursor = u16(1325)
                        from .business_hardware import index_word_pointer
                        from .contexts import IndexWordPointerInput
                        lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1324)
                        index_word_pointer_outcome = index_word_pointer(state, IndexWordPointerInput(conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1324)))
                        lifecycle.condition_bits = index_word_pointer_outcome.conditions
                        lifecycle.transfer_word = index_word_pointer_outcome.count_and_data
                        lifecycle.source_cursor = index_word_pointer_outcome.lookup_cursor
                        lifecycle.working_byte = index_word_pointer_outcome.sample
                        lifecycle.return_stack = index_word_pointer_outcome.stack_cursor
                        indirect_live_context = DispatchSoundCommandInput(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=continuation).validate(state)
                        state.indirect_transfer('driver', lifecycle.source_cursor, indirect_live_context)

def run_dispatch_loaded_sound_command(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Classify the already-live command BYTE without rereading the latch; real indirect-transfer payload remains specific to this public entry."""
    lifecycle.condition_bits = tested_bit_conditions(lifecycle.working_byte, 7, lifecycle.condition_bits)
    if bool(lifecycle.condition_bits & 64):
        return reset_driver_and_channels(state, lifecycle, continuation)
    else:
        lifecycle.condition_bits = comparison_conditions(lifecycle.working_byte, 160)
        if bool(lifecycle.condition_bits & 1):
            return load_music_channels(state, lifecycle, continuation)
        else:
            lifecycle.condition_bits = comparison_conditions(lifecycle.working_byte, 176)
            if bool(lifecycle.condition_bits & 1):
                lifecycle.working_byte, lifecycle.condition_bits = difference_byte(lifecycle.working_byte, 160)
                inactive_accumulator = word(state.platform.exchange_alternate_accumulator(lifecycle.working_byte << 8 | lifecycle.condition_bits))
                lifecycle.working_byte, lifecycle.condition_bits = (high(inactive_accumulator), low(inactive_accumulator))
                lifecycle.working_byte = u8(lifecycle.working_byte ^ lifecycle.working_byte)
                lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
                lifecycle.transfer_word = replace_low(lifecycle.transfer_word, 6)
                return load_effect_channels(state, lifecycle, continuation)
            else:
                lifecycle.condition_bits = comparison_conditions(lifecycle.working_byte, 224)
                if bool(lifecycle.condition_bits & 1):
                    lifecycle.working_byte, lifecycle.condition_bits = difference_byte(lifecycle.working_byte, 208)
                    inactive_accumulator_2 = word(state.platform.exchange_alternate_accumulator(lifecycle.working_byte << 8 | lifecycle.condition_bits))
                    lifecycle.working_byte, lifecycle.condition_bits = (high(inactive_accumulator_2), low(inactive_accumulator_2))
                    lifecycle.working_byte = u8(128)
                    lifecycle.transfer_word = replace_low(lifecycle.transfer_word, 2)
                    pass
                    return load_effect_channels(state, lifecycle, continuation)
                else:
                    lifecycle.condition_bits = comparison_conditions(lifecycle.working_byte, 249)
                    if not lifecycle.condition_bits & 1:
                        return reset_driver_and_channels(state, lifecycle, continuation)
                    else:
                        lifecycle.working_byte, lifecycle.condition_bits = difference_byte(lifecycle.working_byte, 224)
                        lifecycle.source_cursor = u16(1325)
                        from .business_hardware import index_word_pointer
                        from .contexts import IndexWordPointerInput
                        lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1324)
                        index_word_pointer_outcome = index_word_pointer(state, IndexWordPointerInput(conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1324)))
                        lifecycle.condition_bits = index_word_pointer_outcome.conditions
                        lifecycle.transfer_word = index_word_pointer_outcome.count_and_data
                        lifecycle.source_cursor = index_word_pointer_outcome.lookup_cursor
                        lifecycle.working_byte = index_word_pointer_outcome.sample
                        lifecycle.return_stack = index_word_pointer_outcome.stack_cursor
                        indirect_live_context = DispatchLoadedSoundCommandInput(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=continuation).validate(state)
                        state.indirect_transfer('driver', lifecycle.source_cursor, indirect_live_context)

def run_choose_channel_views(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Gate FM/PSG selection, silence the prior PSG when selected, resolve three live channel-view pointer tables and preserve original AF stack frames."""
    lifecycle.condition_bits = tested_bit_conditions(low(lifecycle.transfer_word), 7, lifecycle.condition_bits)
    if not lifecycle.condition_bits & 64:
        lifecycle.working_byte = u8(31)
        from .business_envelopes import silence_old_psg_channel
        from .contexts import SilenceOldPsgChannelInput
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1687)
        silence_old_psg_channel_outcome = silence_old_psg_channel(state, SilenceOldPsgChannelInput(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1687)))
        lifecycle.paired_channel_address = silence_old_psg_channel_outcome.auxiliary_cursor
        lifecycle.channel_address = silence_old_psg_channel_outcome.channel_cursor
        lifecycle.condition_bits = silence_old_psg_channel_outcome.conditions
        lifecycle.transfer_word = silence_old_psg_channel_outcome.count_and_data
        lifecycle.source_cursor = silence_old_psg_channel_outcome.lookup_cursor
        lifecycle.secondary_cursor = silence_old_psg_channel_outcome.parameter_cursor
        lifecycle.working_byte = silence_old_psg_channel_outcome.sample
        lifecycle.return_stack = silence_old_psg_channel_outcome.stack_cursor
        lifecycle.working_byte = u8(255)
        state.write(32529, u8(lifecycle.working_byte))
        lifecycle.working_byte = u8(low(lifecycle.transfer_word))
        shift_input = lifecycle.working_byte
        shifted_value = u8(shift_input >> 1)
        lifecycle.condition_bits = logic_conditions(shifted_value) | shift_input & 1
        lifecycle.working_byte = u8(shifted_value)
        shift_input_2 = lifecycle.working_byte
        shifted_value_2 = u8(shift_input_2 >> 1)
        lifecycle.condition_bits = logic_conditions(shifted_value_2) | shift_input_2 & 1
        lifecycle.working_byte = u8(shifted_value_2)
        shift_input_3 = lifecycle.working_byte
        shifted_value_3 = u8(shift_input_3 >> 1)
        lifecycle.condition_bits = logic_conditions(shifted_value_3) | shift_input_3 & 1
        lifecycle.working_byte = u8(shifted_value_3)
        shift_input_4 = lifecycle.working_byte
        shifted_value_4 = u8(shift_input_4 >> 1)
        lifecycle.condition_bits = logic_conditions(shifted_value_4) | shift_input_4 & 1
        lifecycle.working_byte = u8(shifted_value_4)
        shift_input_5 = lifecycle.working_byte
        shifted_value_5 = u8(shift_input_5 >> 1)
        lifecycle.condition_bits = logic_conditions(shifted_value_5) | shift_input_5 & 1
        lifecycle.working_byte = u8(shifted_value_5)
        next_value, lifecycle.condition_bits = increment_byte(lifecycle.working_byte, lifecycle.condition_bits)
        lifecycle.working_byte = u8(next_value)
    else:
        lifecycle.working_byte = u8(low(lifecycle.transfer_word))
        lifecycle.working_byte, lifecycle.condition_bits = difference_byte(lifecycle.working_byte, 2)
        pass
    state.write(7218, u8(lifecycle.working_byte))
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.working_byte << 8 | lifecycle.condition_bits)
    lifecycle.source_cursor = u16(1772)
    from .business_hardware import index_word_pointer
    from .contexts import IndexWordPointerInput
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1712)
    index_word_pointer_outcome = index_word_pointer(state, IndexWordPointerInput(conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1712)))
    lifecycle.condition_bits = index_word_pointer_outcome.conditions
    lifecycle.transfer_word = index_word_pointer_outcome.count_and_data
    lifecycle.source_cursor = index_word_pointer_outcome.lookup_cursor
    lifecycle.working_byte = index_word_pointer_outcome.sample
    lifecycle.return_stack = index_word_pointer_outcome.stack_cursor
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.source_cursor)
    saved_context_word, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
    lifecycle.channel_address = u16(saved_context_word)
    saved_context_word_2, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
    lifecycle.working_byte, lifecycle.condition_bits = (high(saved_context_word_2), low(saved_context_word_2))
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.working_byte << 8 | lifecycle.condition_bits)
    lifecycle.source_cursor = u16(1756)
    from .business_hardware import index_word_pointer
    from .contexts import IndexWordPointerInput
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1721)
    index_word_pointer_outcome_2 = index_word_pointer(state, IndexWordPointerInput(conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1721)))
    lifecycle.condition_bits = index_word_pointer_outcome_2.conditions
    lifecycle.transfer_word = index_word_pointer_outcome_2.count_and_data
    lifecycle.source_cursor = index_word_pointer_outcome_2.lookup_cursor
    lifecycle.working_byte = index_word_pointer_outcome_2.sample
    lifecycle.return_stack = index_word_pointer_outcome_2.stack_cursor
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.source_cursor)
    saved_context_word_3, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
    lifecycle.paired_channel_address = u16(saved_context_word_3)
    saved_context_word_4, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
    lifecycle.working_byte, lifecycle.condition_bits = (high(saved_context_word_4), low(saved_context_word_4))
    lifecycle.source_cursor = u16(1788)
    from .business_hardware import index_word_pointer
    from .contexts import IndexWordPointerInput
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1729)
    index_word_pointer_outcome_3 = index_word_pointer(state, IndexWordPointerInput(conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1729)))
    lifecycle.condition_bits = index_word_pointer_outcome_3.conditions
    lifecycle.transfer_word = index_word_pointer_outcome_3.count_and_data
    lifecycle.source_cursor = index_word_pointer_outcome_3.lookup_cursor
    lifecycle.working_byte = index_word_pointer_outcome_3.sample
    lifecycle.return_stack = index_word_pointer_outcome_3.stack_cursor
    lifecycle.return_stack = state.consume_return(lifecycle.return_stack, continuation)
    return

def run_clear_note_tail_and_initialize_channel(state: AudioState, lifecycle: RecordInitialization, continuation: Continuation) -> None:
    """Use actual alternate AF to clear two note-tail bytes, restore AF, then initialize the shared channel record transaction."""
    inactive_accumulator = word(state.platform.exchange_alternate_accumulator(lifecycle.working_byte << 8 | lifecycle.condition_bits))
    lifecycle.working_byte, lifecycle.condition_bits = (high(inactive_accumulator), low(inactive_accumulator))
    lifecycle.working_byte = u8(lifecycle.working_byte ^ lifecycle.working_byte)
    lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
    state.write(lifecycle.secondary_cursor, u8(lifecycle.working_byte))
    lifecycle.secondary_cursor = u16(lifecycle.secondary_cursor + 1)
    state.write(lifecycle.secondary_cursor, u8(lifecycle.working_byte))
    lifecycle.secondary_cursor = u16(lifecycle.secondary_cursor + 1)
    inactive_accumulator_2 = word(state.platform.exchange_alternate_accumulator(lifecycle.working_byte << 8 | lifecycle.condition_bits))
    lifecycle.working_byte, lifecycle.condition_bits = (high(inactive_accumulator_2), low(inactive_accumulator_2))
    return initialize_channel_storage(state, lifecycle, continuation)

def run_initialize_channel_record(state: AudioState, lifecycle: RecordInitialization, continuation: Continuation) -> None:
    """Enter the single shared channel-record initialization algorithm at the original tail address."""
    return initialize_channel_storage(state, lifecycle, continuation)

def run_initialize_audio_bank(state: AudioState, lifecycle: BankInitialization, continuation: Continuation) -> None:
    """Rotate and emit the bank bits to the real bank-register bus in original order; its hardware interpretation remains a boundary."""
    source_byte = state.read(7169)
    lifecycle.working_byte = u8(source_byte)
    rotation_input = lifecycle.working_byte
    lifecycle.working_byte = u8(rotation_input << 1 | rotation_input >> 7)
    lifecycle.condition_bits = lifecycle.condition_bits & 196 | lifecycle.working_byte & 40 | rotation_input >> 7
    state.write(24576, u8(lifecycle.working_byte))
    lifecycle.transfer_word = replace_high(lifecycle.transfer_word, 8)
    source_byte_2 = state.read(7168)
    lifecycle.working_byte = u8(source_byte_2)
    while True:
        state.write(24576, u8(lifecycle.working_byte))
        rotation_input_2 = lifecycle.working_byte
        lifecycle.working_byte = u8(rotation_input_2 >> 1 | rotation_input_2 << 7)
        lifecycle.condition_bits = lifecycle.condition_bits & 196 | lifecycle.working_byte & 40 | rotation_input_2 & 1
        lifecycle.transfer_word = replace_high(lifecycle.transfer_word, u8(high(lifecycle.transfer_word) - 1))
        if high(lifecycle.transfer_word) != 0:
            continue
        break
    lifecycle.return_stack = state.consume_return(lifecycle.return_stack, continuation)
    return

def load_music_channels(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Resolve the selected music header, store divider/voice/source metadata and build FM then optional PSG records from live bytes. Shared stack/count and progressive copy are deliberate."""
    lifecycle.working_byte, lifecycle.condition_bits = difference_byte(lifecycle.working_byte, 129)
    if bool(lifecycle.condition_bits & 128):
        lifecycle.return_stack = state.consume_return(lifecycle.return_stack, continuation)
        return
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.working_byte << 8 | lifecycle.condition_bits)
    from .business_loaders import clear_and_reset_driver
    from .contexts import ClearAndResetDriverInput
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1373)
    clear_and_reset_driver_outcome = clear_and_reset_driver(state, ClearAndResetDriverInput(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1373)))
    lifecycle.paired_channel_address = clear_and_reset_driver_outcome.auxiliary_cursor
    lifecycle.channel_address = clear_and_reset_driver_outcome.channel_cursor
    lifecycle.condition_bits = clear_and_reset_driver_outcome.conditions
    lifecycle.transfer_word = clear_and_reset_driver_outcome.count_and_data
    lifecycle.source_cursor = clear_and_reset_driver_outcome.lookup_cursor
    lifecycle.secondary_cursor = clear_and_reset_driver_outcome.parameter_cursor
    lifecycle.working_byte = clear_and_reset_driver_outcome.sample
    lifecycle.return_stack = clear_and_reset_driver_outcome.stack_cursor
    saved_context_word, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
    lifecycle.working_byte, lifecycle.condition_bits = (high(saved_context_word), low(saved_context_word))
    lifecycle.transfer_word = replace_low(lifecycle.transfer_word, 4)
    from .business_hardware import lookup_banked_root_pointer
    from .contexts import LookupBankedRootPointerInput
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1377)
    lookup_banked_root_pointer_outcome = lookup_banked_root_pointer(state, LookupBankedRootPointerInput(conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1377)))
    lifecycle.condition_bits = lookup_banked_root_pointer_outcome.conditions
    lifecycle.transfer_word = lookup_banked_root_pointer_outcome.count_and_data
    lifecycle.source_cursor = lookup_banked_root_pointer_outcome.lookup_cursor
    lifecycle.working_byte = lookup_banked_root_pointer_outcome.sample
    lifecycle.return_stack = lookup_banked_root_pointer_outcome.stack_cursor
    from .business_hardware import index_word_pointer
    from .contexts import IndexWordPointerInput
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1378)
    index_word_pointer_outcome = index_word_pointer(state, IndexWordPointerInput(conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1378)))
    lifecycle.condition_bits = index_word_pointer_outcome.conditions
    lifecycle.transfer_word = index_word_pointer_outcome.count_and_data
    lifecycle.source_cursor = index_word_pointer_outcome.lookup_cursor
    lifecycle.working_byte = index_word_pointer_outcome.sample
    lifecycle.return_stack = index_word_pointer_outcome.stack_cursor
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.source_cursor)
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.source_cursor)
    from .business_hardware import read_stream_word
    from .contexts import ReadStreamWordInput
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1381)
    read_stream_word_outcome = read_stream_word(state, ReadStreamWordInput(conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1381)))
    lifecycle.condition_bits = read_stream_word_outcome.conditions
    lifecycle.transfer_word = read_stream_word_outcome.count_and_data
    lifecycle.source_cursor = read_stream_word_outcome.lookup_cursor
    lifecycle.working_byte = read_stream_word_outcome.sample
    lifecycle.return_stack = read_stream_word_outcome.stack_cursor
    state.write_word_le(7223, u16(lifecycle.source_cursor))
    saved_context_word_2, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
    lifecycle.source_cursor = u16(saved_context_word_2)
    saved_context_word_3, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
    lifecycle.paired_channel_address = u16(saved_context_word_3)
    divider_reload_value = state.read(u16(lifecycle.paired_channel_address + 5))
    lifecycle.working_byte = u8(divider_reload_value)
    state.write(7187, u8(lifecycle.working_byte))
    state.write(7188, u8(lifecycle.working_byte))
    lifecycle.secondary_cursor = u16(6)
    adjusted_value, lifecycle.condition_bits = sum_word(lifecycle.source_cursor, lifecycle.secondary_cursor, lifecycle.condition_bits)
    lifecycle.source_cursor = u16(adjusted_value)
    state.write_word_le(7219, u16(lifecycle.source_cursor))
    lifecycle.source_cursor = u16(1507)
    state.write_word_le(7221, u16(lifecycle.source_cursor))
    lifecycle.secondary_cursor = u16(7232)
    fm_record_count = state.read(u16(lifecycle.paired_channel_address + 2))
    lifecycle.transfer_word = replace_high(lifecycle.transfer_word, fm_record_count)
    record_duration_multiplier = state.read(u16(lifecycle.paired_channel_address + 4))
    lifecycle.working_byte = u8(record_duration_multiplier)
    while True:
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.transfer_word)
        channel_seed_source = state.read_word_le(7221)
        lifecycle.source_cursor = u16(channel_seed_source)
        copy_live_byte(state, lifecycle, continuation)
        copy_live_byte(state, lifecycle, continuation)
        state.write(lifecycle.secondary_cursor, u8(lifecycle.working_byte))
        lifecycle.secondary_cursor = u16(lifecycle.secondary_cursor + 1)
        state.write_word_le(7221, u16(lifecycle.source_cursor))
        sequence_source = state.read_word_le(7219)
        lifecycle.source_cursor = u16(sequence_source)
        copy_live_byte(state, lifecycle, continuation)
        copy_live_byte(state, lifecycle, continuation)
        copy_live_byte(state, lifecycle, continuation)
        copy_live_byte(state, lifecycle, continuation)
        state.write_word_le(7219, u16(lifecycle.source_cursor))
        from .business_loaders import clear_note_tail_and_initialize_channel
        from .contexts import ClearNoteTailAndInitializeChannelInput
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1448)
        clear_note_tail_and_initialize_channel_outcome = clear_note_tail_and_initialize_channel(state, ClearNoteTailAndInitializeChannelInput(conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1448)))
        lifecycle.condition_bits = clear_note_tail_and_initialize_channel_outcome.conditions
        lifecycle.transfer_word = clear_note_tail_and_initialize_channel_outcome.count_and_data
        lifecycle.source_cursor = clear_note_tail_and_initialize_channel_outcome.lookup_cursor
        lifecycle.secondary_cursor = clear_note_tail_and_initialize_channel_outcome.parameter_cursor
        lifecycle.working_byte = clear_note_tail_and_initialize_channel_outcome.sample
        lifecycle.return_stack = clear_note_tail_and_initialize_channel_outcome.stack_cursor
        saved_context_word_4, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
        lifecycle.transfer_word = u16(saved_context_word_4)
        lifecycle.transfer_word = replace_high(lifecycle.transfer_word, u8(high(lifecycle.transfer_word) - 1))
        if high(lifecycle.transfer_word) != 0:
            continue
        break
    psg_record_count = state.read(u16(lifecycle.paired_channel_address + 3))
    lifecycle.working_byte = u8(psg_record_count)
    lifecycle.working_byte = u8(lifecycle.working_byte | lifecycle.working_byte)
    lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
    if not bool(lifecycle.condition_bits & 64):
        lifecycle.transfer_word = replace_high(lifecycle.transfer_word, lifecycle.working_byte)
        lifecycle.source_cursor = u16(1521)
        state.write_word_le(7221, u16(lifecycle.source_cursor))
        lifecycle.secondary_cursor = u16(7568)
        record_duration_multiplier_2 = state.read(u16(lifecycle.paired_channel_address + 4))
        lifecycle.working_byte = u8(record_duration_multiplier_2)
        while True:
            lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.transfer_word)
            channel_seed_source_2 = state.read_word_le(7221)
            lifecycle.source_cursor = u16(channel_seed_source_2)
            copy_live_byte(state, lifecycle, continuation)
            copy_live_byte(state, lifecycle, continuation)
            state.write(lifecycle.secondary_cursor, u8(lifecycle.working_byte))
            lifecycle.secondary_cursor = u16(lifecycle.secondary_cursor + 1)
            state.write_word_le(7221, u16(lifecycle.source_cursor))
            sequence_source_2 = state.read_word_le(7219)
            lifecycle.source_cursor = u16(sequence_source_2)
            lifecycle.transfer_word = u16(6)
            while True:
                copy_live_byte(state, lifecycle, continuation)
                state.bus.transfer_boundary('progressive-block-copy')
                if lifecycle.transfer_word == 0:
                    break
            state.write_word_le(7219, u16(lifecycle.source_cursor))
            from .business_loaders import initialize_channel_record
            from .contexts import InitializeChannelRecordInput
            lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1498)
            initialize_channel_record_outcome = initialize_channel_record(state, InitializeChannelRecordInput(conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1498)))
            lifecycle.condition_bits = initialize_channel_record_outcome.conditions
            lifecycle.transfer_word = initialize_channel_record_outcome.count_and_data
            lifecycle.source_cursor = initialize_channel_record_outcome.lookup_cursor
            lifecycle.secondary_cursor = initialize_channel_record_outcome.parameter_cursor
            lifecycle.working_byte = initialize_channel_record_outcome.sample
            lifecycle.return_stack = initialize_channel_record_outcome.stack_cursor
            saved_context_word_5, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
            lifecycle.transfer_word = u16(saved_context_word_5)
            lifecycle.transfer_word = replace_high(lifecycle.transfer_word, u8(high(lifecycle.transfer_word) - 1))
            if high(lifecycle.transfer_word) != 0:
                continue
            break
    return finish_sound_command(state, lifecycle, continuation)

def load_effect_channels(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Resolve the banked effect header and load each selected channel view, initialize its record, associate its voice source and release the previous voice through real services."""
    state.write(7193, u8(lifecycle.working_byte))
    inactive_accumulator = word(state.platform.exchange_alternate_accumulator(lifecycle.working_byte << 8 | lifecycle.condition_bits))
    lifecycle.working_byte, lifecycle.condition_bits = (high(inactive_accumulator), low(inactive_accumulator))
    from .business_hardware import lookup_banked_root_pointer
    from .contexts import LookupBankedRootPointerInput
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1547)
    lookup_banked_root_pointer_outcome = lookup_banked_root_pointer(state, LookupBankedRootPointerInput(conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1547)))
    lifecycle.condition_bits = lookup_banked_root_pointer_outcome.conditions
    lifecycle.transfer_word = lookup_banked_root_pointer_outcome.count_and_data
    lifecycle.source_cursor = lookup_banked_root_pointer_outcome.lookup_cursor
    lifecycle.working_byte = lookup_banked_root_pointer_outcome.sample
    lifecycle.return_stack = lookup_banked_root_pointer_outcome.stack_cursor
    from .business_hardware import index_word_pointer
    from .contexts import IndexWordPointerInput
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1548)
    index_word_pointer_outcome = index_word_pointer(state, IndexWordPointerInput(conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1548)))
    lifecycle.condition_bits = index_word_pointer_outcome.conditions
    lifecycle.transfer_word = index_word_pointer_outcome.count_and_data
    lifecycle.source_cursor = index_word_pointer_outcome.lookup_cursor
    lifecycle.working_byte = index_word_pointer_outcome.sample
    lifecycle.return_stack = index_word_pointer_outcome.stack_cursor
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.source_cursor)
    from .business_hardware import read_stream_word
    from .contexts import ReadStreamWordInput
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1550)
    read_stream_word_outcome = read_stream_word(state, ReadStreamWordInput(conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1550)))
    lifecycle.condition_bits = read_stream_word_outcome.conditions
    lifecycle.transfer_word = read_stream_word_outcome.count_and_data
    lifecycle.source_cursor = read_stream_word_outcome.lookup_cursor
    lifecycle.working_byte = read_stream_word_outcome.sample
    lifecycle.return_stack = read_stream_word_outcome.stack_cursor
    state.write_word_le(7225, u16(lifecycle.source_cursor))
    lifecycle.working_byte = u8(lifecycle.working_byte ^ lifecycle.working_byte)
    lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
    state.write(7189, u8(lifecycle.working_byte))
    saved_context_word, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
    lifecycle.source_cursor = u16(saved_context_word)
    lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.source_cursor)
    saved_context_word_2, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
    lifecycle.paired_channel_address = u16(saved_context_word_2)
    record_duration_multiplier = state.read(u16(lifecycle.paired_channel_address + 2))
    lifecycle.working_byte = u8(record_duration_multiplier)
    state.write(7227, u8(lifecycle.working_byte))
    lifecycle.secondary_cursor = u16(4)
    adjusted_value, lifecycle.condition_bits = sum_word(lifecycle.source_cursor, lifecycle.secondary_cursor, lifecycle.condition_bits)
    lifecycle.source_cursor = u16(adjusted_value)
    effect_record_count = state.read(u16(lifecycle.paired_channel_address + 3))
    lifecycle.transfer_word = replace_high(lifecycle.transfer_word, effect_record_count)
    while True:
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.transfer_word)
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.source_cursor)
        lifecycle.source_cursor = u16(lifecycle.source_cursor + 1)
        live_source_byte = state.read(lifecycle.source_cursor)
        lifecycle.transfer_word = replace_low(lifecycle.transfer_word, live_source_byte)
        from .business_loaders import choose_channel_views
        from .contexts import ChooseChannelViewsInput
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1581)
        choose_channel_views_outcome = choose_channel_views(state, ChooseChannelViewsInput(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1581)))
        lifecycle.paired_channel_address = choose_channel_views_outcome.auxiliary_cursor
        lifecycle.channel_address = choose_channel_views_outcome.channel_cursor
        lifecycle.condition_bits = choose_channel_views_outcome.conditions
        lifecycle.transfer_word = choose_channel_views_outcome.count_and_data
        lifecycle.source_cursor = choose_channel_views_outcome.lookup_cursor
        lifecycle.secondary_cursor = choose_channel_views_outcome.parameter_cursor
        lifecycle.working_byte = choose_channel_views_outcome.sample
        lifecycle.return_stack = choose_channel_views_outcome.stack_cursor
        live_source_byte_2 = state.read(lifecycle.source_cursor)
        state.write(lifecycle.source_cursor, u8(live_source_byte_2 | 4))
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.channel_address)
        channel_view_mode = state.read(7193)
        lifecycle.working_byte = u8(channel_view_mode)
        lifecycle.working_byte = u8(lifecycle.working_byte | lifecycle.working_byte)
        lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
        if not bool(lifecycle.condition_bits & 64):
            saved_context_word_7, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
            lifecycle.source_cursor = u16(saved_context_word_7)
            lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.paired_channel_address)
        saved_context_word_3, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
        lifecycle.secondary_cursor = u16(saved_context_word_3)
        saved_context_word_4, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
        lifecycle.source_cursor = u16(saved_context_word_4)
        copy_live_byte(state, lifecycle, continuation)
        live_secondary_byte = state.read(lifecycle.secondary_cursor)
        lifecycle.working_byte = u8(live_secondary_byte)
        lifecycle.condition_bits = comparison_conditions(lifecycle.working_byte, 2)
        if bool(lifecycle.condition_bits & 64):
            from .business_loaders import reset_timer_control
            from .contexts import ResetTimerControlInput
            lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1604)
            reset_timer_control_outcome = reset_timer_control(state, ResetTimerControlInput(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1604)))
            lifecycle.paired_channel_address = reset_timer_control_outcome.auxiliary_cursor
            lifecycle.channel_address = reset_timer_control_outcome.channel_cursor
            lifecycle.condition_bits = reset_timer_control_outcome.conditions
            lifecycle.transfer_word = reset_timer_control_outcome.count_and_data
            lifecycle.source_cursor = reset_timer_control_outcome.lookup_cursor
            lifecycle.secondary_cursor = reset_timer_control_outcome.parameter_cursor
            lifecycle.working_byte = reset_timer_control_outcome.sample
            lifecycle.return_stack = reset_timer_control_outcome.stack_cursor
        copy_live_byte(state, lifecycle, continuation)
        source_byte = state.read(7227)
        lifecycle.working_byte = u8(source_byte)
        state.write(lifecycle.secondary_cursor, u8(lifecycle.working_byte))
        lifecycle.secondary_cursor = u16(lifecycle.secondary_cursor + 1)
        copy_live_byte(state, lifecycle, continuation)
        copy_live_byte(state, lifecycle, continuation)
        copy_live_byte(state, lifecycle, continuation)
        copy_live_byte(state, lifecycle, continuation)
        from .business_loaders import clear_note_tail_and_initialize_channel
        from .contexts import ClearNoteTailAndInitializeChannelInput
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1622)
        clear_note_tail_and_initialize_channel_outcome = clear_note_tail_and_initialize_channel(state, ClearNoteTailAndInitializeChannelInput(conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1622)))
        lifecycle.condition_bits = clear_note_tail_and_initialize_channel_outcome.conditions
        lifecycle.transfer_word = clear_note_tail_and_initialize_channel_outcome.count_and_data
        lifecycle.source_cursor = clear_note_tail_and_initialize_channel_outcome.lookup_cursor
        lifecycle.secondary_cursor = clear_note_tail_and_initialize_channel_outcome.parameter_cursor
        lifecycle.working_byte = clear_note_tail_and_initialize_channel_outcome.sample
        lifecycle.return_stack = clear_note_tail_and_initialize_channel_outcome.stack_cursor
        channel_flags = state.read(u16(lifecycle.channel_address + 0))
        lifecycle.condition_bits = state.memory_bit_conditions(channel_flags, 7, lifecycle.condition_bits, u16(lifecycle.channel_address + 0), True)
        if not bool(lifecycle.condition_bits & 64):
            channel_kind = state.read(u16(lifecycle.channel_address + 1))
            lifecycle.working_byte = u8(channel_kind)
            channel_kind_2 = state.read(u16(lifecycle.paired_channel_address + 1))
            lifecycle.condition_bits = comparison_conditions(lifecycle.working_byte, channel_kind_2)
            if not not lifecycle.condition_bits & 64:
                channel_flags_2 = state.read(u16(lifecycle.paired_channel_address + 0))
                state.write(u16(lifecycle.paired_channel_address + 0), u8(channel_flags_2 | 4))
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.source_cursor)
        effect_voice_source = state.read_word_le(7225)
        lifecycle.source_cursor = u16(effect_voice_source)
        channel_view_mode_2 = state.read(7193)
        lifecycle.working_byte = u8(channel_view_mode_2)
        lifecycle.working_byte = u8(lifecycle.working_byte | lifecycle.working_byte)
        lifecycle.condition_bits = logic_conditions(lifecycle.working_byte, False)
        if not bool(lifecycle.condition_bits & 64):
            lifecycle.return_stack = state.push_word(lifecycle.return_stack, lifecycle.paired_channel_address)
            saved_context_word_8, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
            lifecycle.channel_address = u16(saved_context_word_8)
        state.write(u16(lifecycle.channel_address + 42), u8(low(lifecycle.source_cursor)))
        state.write(u16(lifecycle.channel_address + 43), u8(high(lifecycle.source_cursor)))
        from .business_envelopes import send_key_off
        from .contexts import SendKeyOffInput
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1663)
        send_key_off_outcome = send_key_off(state, SendKeyOffInput(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1663)))
        lifecycle.paired_channel_address = send_key_off_outcome.auxiliary_cursor
        lifecycle.channel_address = send_key_off_outcome.channel_cursor
        lifecycle.condition_bits = send_key_off_outcome.conditions
        lifecycle.transfer_word = send_key_off_outcome.count_and_data
        lifecycle.source_cursor = send_key_off_outcome.lookup_cursor
        lifecycle.secondary_cursor = send_key_off_outcome.parameter_cursor
        lifecycle.working_byte = send_key_off_outcome.sample
        lifecycle.return_stack = send_key_off_outcome.stack_cursor
        from .business_loaders import reset_voice_release
        from .contexts import ResetVoiceReleaseInput
        lifecycle.return_stack = state.push_word(lifecycle.return_stack, 1666)
        reset_voice_release_outcome = reset_voice_release(state, ResetVoiceReleaseInput(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack, continuation=Continuation('driver', 1666)))
        lifecycle.channel_address = reset_voice_release_outcome.channel_cursor
        lifecycle.condition_bits = reset_voice_release_outcome.conditions
        lifecycle.transfer_word = reset_voice_release_outcome.count_and_data
        lifecycle.working_byte = reset_voice_release_outcome.sample
        lifecycle.return_stack = reset_voice_release_outcome.stack_cursor
        saved_context_word_5, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
        lifecycle.source_cursor = u16(saved_context_word_5)
        saved_context_word_6, lifecycle.return_stack = state.pop_word(lifecycle.return_stack)
        lifecycle.transfer_word = u16(saved_context_word_6)
        lifecycle.transfer_word = replace_high(lifecycle.transfer_word, u8(high(lifecycle.transfer_word) - 1))
        if high(lifecycle.transfer_word) != 0:
            continue
        break
    pass
    return finish_sound_command(state, lifecycle, continuation)

def initialize_channel_storage(state: AudioState, lifecycle: RecordInitialization, continuation: Continuation) -> None:
    """Exchange the live cursors, write the three record defaults, clear the original tail count, restore cursor roles and consume the real return."""
    lifecycle.secondary_cursor, lifecycle.source_cursor = (lifecycle.source_cursor, lifecycle.secondary_cursor)
    state.write(lifecycle.source_cursor, u8(48))
    lifecycle.source_cursor = u16(lifecycle.source_cursor + 1)
    state.write(lifecycle.source_cursor, u8(192))
    lifecycle.source_cursor = u16(lifecycle.source_cursor + 1)
    state.write(lifecycle.source_cursor, u8(1))
    lifecycle.transfer_word = replace_high(lifecycle.transfer_word, 36)
    while True:
        lifecycle.source_cursor = u16(lifecycle.source_cursor + 1)
        state.write(lifecycle.source_cursor, u8(0))
        lifecycle.transfer_word = replace_high(lifecycle.transfer_word, u8(high(lifecycle.transfer_word) - 1))
        if high(lifecycle.transfer_word) != 0:
            continue
        break
    lifecycle.source_cursor = u16(lifecycle.source_cursor + 1)
    lifecycle.secondary_cursor, lifecycle.source_cursor = (lifecycle.source_cursor, lifecycle.secondary_cursor)
    lifecycle.return_stack = state.consume_return(lifecycle.return_stack, continuation)
    return
