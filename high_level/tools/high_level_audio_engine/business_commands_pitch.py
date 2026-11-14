"""Actual pitch command algorithms. Fixed-width live cells, ordered bus effects and original boundaries are retained; remaining low-level compatibility clauses are not a natural hardware proof."""
from .domain import AudioState, AudioBoundary, Continuation, AlternateGroup, Byte, Word, byte, word, checked_state, u8, u16, low, high, replace_low, replace_high, logic_conditions, sum_byte, difference_byte, comparison_conditions, increment_byte, decrement_byte, sum_word, difference_word, tested_bit_conditions, copy_byte_conditions
from .contexts_commands import ChannelValueCommand, ChannelPointerCommand, ChannelTransferCommand, ChannelArgumentCommand
from .business_commands_services import copy_live_byte, commit_timer_control, commit_pitch_envelope

def apply_set_pitch_offset(state: AudioState, command: ChannelValueCommand, continuation: Continuation) -> None:
    """Store the pitch-offset BYTE in the current channel."""
    state.write(u16(command.channel_address + 16), u8(command.command_value))
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def apply_set_pitch_modulation(state: AudioState, command: ChannelPointerCommand, continuation: Continuation) -> None:
    """Record the live modulation source, mark its mode and consume the original three parameter advances."""
    state.write(u16(command.channel_address + 32), u8(low(command.argument_cursor)))
    state.write(u16(command.channel_address + 33), u8(high(command.argument_cursor)))
    state.write(u16(command.channel_address + 7), u8(128))
    command.argument_cursor = u16(command.argument_cursor + 1)
    command.argument_cursor = u16(command.argument_cursor + 1)
    command.argument_cursor = u16(command.argument_cursor + 1)
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def apply_set_special_channel_frequency(state: AudioState, command: ChannelTransferCommand, continuation: Continuation) -> None:
    """Gate the special hardware channel, fill four alternate-bank frequency words and commit timer control."""
    channel_kind = state.read(u16(command.channel_address + 1))
    command.command_value = u8(channel_kind)
    command.condition_bits = comparison_conditions(command.command_value, 2)
    if not command.condition_bits & 64:
        command.argument_cursor = u16(command.argument_cursor + 1)
        command.argument_cursor = u16(command.argument_cursor + 1)
        command.argument_cursor = u16(command.argument_cursor + 1)
        command.return_stack = state.consume_return(command.return_stack, continuation)
        return
    else:
        channel_flags = state.read(u16(command.channel_address + 0))
        state.write(u16(command.channel_address + 0), u8(channel_flags | 1))
        inactive_cells = state.platform.exchange_alternate_group(AlternateGroup(command.transfer_word, command.argument_cursor, command.table_cursor))
        inactive_cells.validate()
        command.transfer_word, command.argument_cursor, command.table_cursor = (inactive_cells.count_and_data, inactive_cells.parameter_cursor, inactive_cells.lookup_cursor)
        from .business_pitch import choose_frequency_scratch_block
        from .contexts import ChooseFrequencyScratchBlockInput
        command.return_stack = state.push_word(command.return_stack, 3327)
        choose_frequency_scratch_block_outcome = choose_frequency_scratch_block(state, ChooseFrequencyScratchBlockInput(conditions=command.condition_bits, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack, continuation=Continuation('driver', 3327)))
        command.condition_bits = choose_frequency_scratch_block_outcome.conditions
        command.argument_cursor = choose_frequency_scratch_block_outcome.parameter_cursor
        command.command_value = choose_frequency_scratch_block_outcome.sample
        command.return_stack = choose_frequency_scratch_block_outcome.stack_cursor
        command.transfer_word = replace_high(command.transfer_word, 4)
        while True:
            command.return_stack = state.push_word(command.return_stack, command.transfer_word)
            inactive_cells_3 = state.platform.exchange_alternate_group(AlternateGroup(command.transfer_word, command.argument_cursor, command.table_cursor))
            inactive_cells_3.validate()
            command.transfer_word, command.argument_cursor, command.table_cursor = (inactive_cells_3.count_and_data, inactive_cells_3.parameter_cursor, inactive_cells_3.lookup_cursor)
            argument_byte = state.read(command.argument_cursor)
            command.command_value = u8(argument_byte)
            command.argument_cursor = u16(command.argument_cursor + 1)
            inactive_cells_4 = state.platform.exchange_alternate_group(AlternateGroup(command.transfer_word, command.argument_cursor, command.table_cursor))
            inactive_cells_4.validate()
            command.transfer_word, command.argument_cursor, command.table_cursor = (inactive_cells_4.count_and_data, inactive_cells_4.parameter_cursor, inactive_cells_4.lookup_cursor)
            command.table_cursor = u16(3365)
            adjusted_value, command.condition_bits = sum_byte(command.command_value, command.command_value)
            command.command_value = u8(adjusted_value)
            command.transfer_word = replace_low(command.transfer_word, command.command_value)
            command.transfer_word = replace_high(command.transfer_word, 0)
            adjusted_value_2, command.condition_bits = sum_word(command.table_cursor, command.transfer_word, command.condition_bits)
            command.table_cursor = u16(adjusted_value_2)
            copy_live_byte(state, command, continuation)
            copy_live_byte(state, command, continuation)
            saved_context_word, command.return_stack = state.pop_word(command.return_stack)
            command.transfer_word = u16(saved_context_word)
            command.transfer_word = replace_high(command.transfer_word, u8(high(command.transfer_word) - 1))
            if high(command.transfer_word) != 0:
                continue
            break
        inactive_cells_2 = state.platform.exchange_alternate_group(AlternateGroup(command.transfer_word, command.argument_cursor, command.table_cursor))
        inactive_cells_2.validate()
        command.transfer_word, command.argument_cursor, command.table_cursor = (inactive_cells_2.count_and_data, inactive_cells_2.parameter_cursor, inactive_cells_2.lookup_cursor)
        command.argument_cursor = u16(command.argument_cursor - 1)
        command.command_value = u8(79)
        commit_timer_control(state, command, continuation)

def apply_adjust_note_transpose(state: AudioState, command: ChannelValueCommand, continuation: Continuation) -> None:
    """Add the current transpose BYTE and commit the fixed-width arithmetic outcome."""
    transpose = state.read(u16(command.channel_address + 5))
    adjusted_value, command.condition_bits = sum_byte(command.command_value, transpose)
    command.command_value = u8(adjusted_value)
    state.write(u16(command.channel_address + 5), u8(command.command_value))
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def apply_set_pitch_envelope(state: AudioState, command: ChannelArgumentCommand, continuation: Continuation) -> None:
    """Consume the argument, apply channel-kind selection and commit the shared envelope field."""
    command.argument_cursor = u16(command.argument_cursor + 1)
    channel_kind = state.read(u16(command.channel_address + 1))
    command.condition_bits = state.memory_bit_conditions(channel_kind, 7, command.condition_bits, u16(command.channel_address + 1), True)
    if not not command.condition_bits & 64:
        argument_byte = state.read(command.argument_cursor)
        command.command_value = u8(argument_byte)
    commit_pitch_envelope(state, command, continuation)

def apply_store_pitch_envelope(state: AudioState, command: ChannelArgumentCommand, continuation: Continuation) -> None:
    """Commit the shared pitch-envelope field and real return."""
    commit_pitch_envelope(state, command, continuation)

def apply_set_pitch_slide_mode(state: AudioState, command: ChannelValueCommand, continuation: Continuation) -> None:
    """Preserve the one-value slide policy, separate flag updates and offset clear."""
    command.condition_bits = comparison_conditions(command.command_value, 1)
    if not command.condition_bits & 64:
        channel_flags = state.read(u16(command.channel_address + 0))
        state.write(u16(command.channel_address + 0), u8(channel_flags & 253))
        channel_flags_2 = state.read(u16(command.channel_address + 0))
        state.write(u16(command.channel_address + 0), u8(channel_flags_2 & 223))
        command.command_value = u8(command.command_value ^ command.command_value)
        command.condition_bits = logic_conditions(command.command_value, False)
        state.write(u16(command.channel_address + 16), u8(command.command_value))
        command.return_stack = state.consume_return(command.return_stack, continuation)
        return
    else:
        channel_flags_3 = state.read(u16(command.channel_address + 0))
        state.write(u16(command.channel_address + 0), u8(channel_flags_3 | 32))
        command.return_stack = state.consume_return(command.return_stack, continuation)
        return

def apply_set_raw_frequency_mode(state: AudioState, command: ChannelValueCommand, continuation: Continuation) -> None:
    """Preserve the one-value raw-frequency policy and live channel flag update."""
    command.condition_bits = comparison_conditions(command.command_value, 1)
    if not command.condition_bits & 64:
        channel_flags = state.read(u16(command.channel_address + 0))
        state.write(u16(command.channel_address + 0), u8(channel_flags & 247))
        command.return_stack = state.consume_return(command.return_stack, continuation)
        return
    else:
        channel_flags_2 = state.read(u16(command.channel_address + 0))
        state.write(u16(command.channel_address + 0), u8(channel_flags_2 | 8))
        command.return_stack = state.consume_return(command.return_stack, continuation)
        return
