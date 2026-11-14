"""Actual state command algorithms. Fixed-width live cells, ordered bus effects and original boundaries are retained; remaining low-level compatibility clauses are not a natural hardware proof."""
from .domain import AudioState, AudioBoundary, Continuation, AlternateGroup, Byte, Word, byte, word, checked_state, u8, u16, low, high, replace_low, replace_high, logic_conditions, sum_byte, difference_byte, comparison_conditions, increment_byte, decrement_byte, sum_word, difference_word, tested_bit_conditions, copy_byte_conditions
from .contexts_commands import DriverValueCommand, SoundDispatchCommand, StreamTransferCommand, ChannelPointerCommand
from .business_commands_services import copy_live_byte

def apply_set_driver_mode(state: AudioState, command: DriverValueCommand, continuation: Continuation) -> None:
    """Store the raw driver-mode BYTE; its wider scheduling meaning remains a boundary."""
    state.write(7175, u8(command.command_value))
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def apply_dispatch_preserving_channel(state: AudioState, command: SoundDispatchCommand, continuation: Continuation) -> None:
    """Dispatch a sound command with the original shared-stack channel save/restore."""
    command.return_stack = state.push_word(command.return_stack, command.channel_address)
    from .business_loaders import dispatch_loaded_sound_command
    from .contexts import DispatchLoadedSoundCommandInput
    command.return_stack = state.push_word(command.return_stack, 3121)
    dispatch_loaded_sound_command_outcome = dispatch_loaded_sound_command(state, DispatchLoadedSoundCommandInput(auxiliary_cursor=command.auxiliary_address, channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack, continuation=Continuation('driver', 3121)))
    command.auxiliary_address = dispatch_loaded_sound_command_outcome.auxiliary_cursor
    command.channel_address = dispatch_loaded_sound_command_outcome.channel_cursor
    command.condition_bits = dispatch_loaded_sound_command_outcome.conditions
    command.transfer_word = dispatch_loaded_sound_command_outcome.count_and_data
    command.table_cursor = dispatch_loaded_sound_command_outcome.lookup_cursor
    command.argument_cursor = dispatch_loaded_sound_command_outcome.parameter_cursor
    command.command_value = dispatch_loaded_sound_command_outcome.sample
    command.return_stack = dispatch_loaded_sound_command_outcome.stack_cursor
    saved_context_word, command.return_stack = state.pop_word(command.return_stack)
    command.channel_address = u16(saved_context_word)
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def apply_copy_sequence_block(state: AudioState, command: StreamTransferCommand, continuation: Continuation) -> None:
    """Read the destination/count parameters and perform progressive live copy, including zero-count wrap."""
    command.argument_cursor, command.table_cursor = (command.table_cursor, command.argument_cursor)
    table_byte = state.read(command.table_cursor)
    command.argument_cursor = replace_low(command.argument_cursor, table_byte)
    command.table_cursor = u16(command.table_cursor + 1)
    table_byte_2 = state.read(command.table_cursor)
    command.argument_cursor = replace_high(command.argument_cursor, table_byte_2)
    command.table_cursor = u16(command.table_cursor + 1)
    table_byte_3 = state.read(command.table_cursor)
    command.transfer_word = replace_low(command.transfer_word, table_byte_3)
    command.transfer_word = replace_high(command.transfer_word, 0)
    command.table_cursor = u16(command.table_cursor + 1)
    command.argument_cursor, command.table_cursor = (command.table_cursor, command.argument_cursor)
    while True:
        copy_live_byte(state, command, continuation)
        state.bus.transfer_boundary('progressive-block-copy')
        if command.transfer_word == 0:
            break
    command.argument_cursor = u16(command.argument_cursor - 1)
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def apply_set_misc_driver_field(state: AudioState, command: DriverValueCommand, continuation: Continuation) -> None:
    """Store the raw driver field; natural policy meaning is still unknown."""
    state.write(7190, u8(command.command_value))
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def apply_mark_note_continuation(state: AudioState, command: ChannelPointerCommand, continuation: Continuation) -> None:
    """Set continuation state and preserve the original parameter cursor decrement."""
    channel_flags = state.read(u16(command.channel_address + 0))
    state.write(u16(command.channel_address + 0), u8(channel_flags | 2))
    command.argument_cursor = u16(command.argument_cursor - 1)
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return
