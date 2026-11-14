"""Actual timing command algorithms. Fixed-width live cells, ordered bus effects and original boundaries are retained; remaining low-level compatibility clauses are not a natural hardware proof."""
from .domain import AudioState, AudioBoundary, Continuation, AlternateGroup, Byte, Word, byte, word, checked_state, u8, u16, low, high, replace_low, replace_high, logic_conditions, sum_byte, difference_byte, comparison_conditions, increment_byte, decrement_byte, sum_word, difference_word, tested_bit_conditions, copy_byte_conditions
from .contexts_commands import StreamTransferCommand, DriverLookupCommand, ChannelDurationCommand, ChannelValueCommand, ChannelTransferCommand
from .business_commands_services import copy_live_byte, commit_timer_control

def apply_set_all_duration_multipliers(state: AudioState, command: StreamTransferCommand, continuation: Continuation) -> None:
    """Broadcast a duration BYTE through the inactive ten-channel bank and restore its cells."""
    inactive_cells = state.platform.exchange_alternate_group(AlternateGroup(command.transfer_word, command.argument_cursor, command.table_cursor))
    inactive_cells.validate()
    command.transfer_word, command.argument_cursor, command.table_cursor = (inactive_cells.count_and_data, inactive_cells.parameter_cursor, inactive_cells.lookup_cursor)
    command.transfer_word = replace_high(command.transfer_word, 10)
    command.argument_cursor = u16(48)
    command.table_cursor = u16(7234)
    while True:
        state.write(command.table_cursor, u8(command.command_value))
        adjusted_value, command.condition_bits = sum_word(command.table_cursor, command.argument_cursor, command.condition_bits)
        command.table_cursor = u16(adjusted_value)
        command.transfer_word = replace_high(command.transfer_word, u8(high(command.transfer_word) - 1))
        if high(command.transfer_word) != 0:
            continue
        break
    inactive_cells_2 = state.platform.exchange_alternate_group(AlternateGroup(command.transfer_word, command.argument_cursor, command.table_cursor))
    inactive_cells_2.validate()
    command.transfer_word, command.argument_cursor, command.table_cursor = (inactive_cells_2.count_and_data, inactive_cells_2.parameter_cursor, inactive_cells_2.lookup_cursor)
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def apply_load_timer_reloads(state: AudioState, command: StreamTransferCommand, continuation: Continuation) -> None:
    """Copy three live timer reload bytes with original source/destination/count/condition effects."""
    command.table_cursor = u16(7172)
    command.argument_cursor, command.table_cursor = (command.table_cursor, command.argument_cursor)
    copy_live_byte(state, command, continuation)
    copy_live_byte(state, command, continuation)
    copy_live_byte(state, command, continuation)
    command.argument_cursor, command.table_cursor = (command.table_cursor, command.argument_cursor)
    command.argument_cursor = u16(command.argument_cursor - 1)
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def apply_adjust_timer_reloads(state: AudioState, command: StreamTransferCommand, continuation: Continuation) -> None:
    """Apply the live WORD Timer-A delta followed by the live BYTE Timer-B delta."""
    command.argument_cursor, command.table_cursor = (command.table_cursor, command.argument_cursor)
    table_byte = state.read(command.table_cursor)
    command.transfer_word = replace_low(command.transfer_word, table_byte)
    command.table_cursor = u16(command.table_cursor + 1)
    table_byte_2 = state.read(command.table_cursor)
    command.transfer_word = replace_high(command.transfer_word, table_byte_2)
    command.table_cursor = u16(command.table_cursor + 1)
    command.argument_cursor, command.table_cursor = (command.table_cursor, command.argument_cursor)
    source_word = state.read_word_le(7172)
    command.table_cursor = u16(source_word)
    adjusted_value, command.condition_bits = sum_word(command.table_cursor, command.transfer_word, command.condition_bits)
    command.table_cursor = u16(adjusted_value)
    state.write_word_le(7172, u16(command.table_cursor))
    argument_byte = state.read(command.argument_cursor)
    command.command_value = u8(argument_byte)
    command.table_cursor = u16(7174)
    table_byte_3 = state.read(command.table_cursor)
    adjusted_value_2, command.condition_bits = sum_byte(command.command_value, table_byte_3)
    command.command_value = u8(adjusted_value_2)
    state.write(command.table_cursor, u8(command.command_value))
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def apply_adjust_note_divider(state: AudioState, command: DriverLookupCommand, continuation: Continuation) -> None:
    """Adjust the live driver divider and update both current/reload bytes in order."""
    command.table_cursor = u16(7188)
    table_byte = state.read(command.table_cursor)
    adjusted_value, command.condition_bits = sum_byte(command.command_value, table_byte)
    command.command_value = u8(adjusted_value)
    state.write(command.table_cursor, u8(command.command_value))
    command.table_cursor = u16(command.table_cursor - 1)
    state.write(command.table_cursor, u8(command.command_value))
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def apply_set_note_release_duration(state: AudioState, command: ChannelDurationCommand, continuation: Continuation) -> None:
    """Multiply the current duration through the real service and store both release counters."""
    from .business_notes import multiply_note_duration
    from .contexts import MultiplyNoteDurationInput
    command.return_stack = state.push_word(command.return_stack, 3280)
    multiply_note_duration_outcome = multiply_note_duration(state, MultiplyNoteDurationInput(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, sample=command.command_value, stack_cursor=command.return_stack, continuation=Continuation('driver', 3280)))
    command.channel_address = multiply_note_duration_outcome.channel_cursor
    command.condition_bits = multiply_note_duration_outcome.conditions
    command.transfer_word = multiply_note_duration_outcome.count_and_data
    command.command_value = multiply_note_duration_outcome.sample
    command.return_stack = multiply_note_duration_outcome.stack_cursor
    state.write(u16(command.channel_address + 30), u8(command.command_value))
    state.write(u16(command.channel_address + 31), u8(command.command_value))
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def apply_set_duration_multiplier(state: AudioState, command: ChannelValueCommand, continuation: Continuation) -> None:
    """Store the channel duration multiplier BYTE without inventing a new range rule."""
    state.write(u16(command.channel_address + 2), u8(command.command_value))
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def apply_write_timer_control(state: AudioState, command: ChannelTransferCommand, continuation: Continuation) -> None:
    """Commit the live timer-control value through the original port-zero service boundary."""
    commit_timer_control(state, command, continuation)
