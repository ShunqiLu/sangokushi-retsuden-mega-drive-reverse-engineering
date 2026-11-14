"""Actual voice command algorithms. Fixed-width live cells, ordered bus effects and original boundaries are retained; remaining low-level compatibility clauses are not a natural hardware proof."""
from .domain import AudioState, AudioBoundary, Continuation, AlternateGroup, Byte, Word, byte, word, checked_state, u8, u16, low, high, replace_low, replace_high, logic_conditions, sum_byte, difference_byte, comparison_conditions, increment_byte, decrement_byte, sum_word, difference_word, tested_bit_conditions, copy_byte_conditions
from .contexts_commands import ChannelTransferCommand, ChannelArgumentCommand, ChannelValueCommand
from .business_commands_services import send_four_fm_fields, copy_live_byte, resolve_banked_instrument, finish_instrument_load, merge_stereo_argument

def apply_store_fm_parameters(state: AudioState, command: ChannelTransferCommand, continuation: Continuation) -> None:
    """Record the live envelope source and write its four register/value fields."""
    state.write(u16(command.channel_address + 24), u8(128))
    state.write(u16(command.channel_address + 25), u8(low(command.argument_cursor)))
    state.write(u16(command.channel_address + 26), u8(high(command.argument_cursor)))
    send_four_fm_fields(state, command, continuation)

def apply_write_fm_parameters(state: AudioState, command: ChannelTransferCommand, continuation: Continuation) -> None:
    """Write four live FM fields through the shared parameter transaction."""
    send_four_fm_fields(state, command, continuation)

def apply_set_voice_envelope(state: AudioState, command: ChannelArgumentCommand, continuation: Continuation) -> None:
    """Store envelope selection then read and store the live next envelope parameter."""
    state.write(u16(command.channel_address + 24), u8(command.command_value))
    command.argument_cursor = u16(command.argument_cursor + 1)
    argument_byte = state.read(command.argument_cursor)
    command.command_value = u8(argument_byte)
    state.write(u16(command.channel_address + 25), u8(command.command_value))
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def apply_adjust_psg_volume(state: AudioState, command: ChannelValueCommand, continuation: Continuation) -> None:
    """Apply the channel eligibility gate, clear the update flag, decrement envelope position and add volume."""
    channel_kind = state.read(u16(command.channel_address + 1))
    command.condition_bits = state.memory_bit_conditions(channel_kind, 7, command.condition_bits, u16(command.channel_address + 1), True)
    if bool(command.condition_bits & 64):
        command.return_stack = state.consume_return(command.return_stack, continuation)
        return
    channel_flags = state.read(u16(command.channel_address + 0))
    state.write(u16(command.channel_address + 0), u8(channel_flags & 239))
    envelope_position = state.read(u16(command.channel_address + 23))
    next_value, command.condition_bits = decrement_byte(envelope_position, command.condition_bits)
    state.write(u16(command.channel_address + 23), u8(next_value))
    volume = state.read(u16(command.channel_address + 6))
    adjusted_value, command.condition_bits = sum_byte(command.command_value, volume)
    command.command_value = u8(adjusted_value)
    state.write(u16(command.channel_address + 6), u8(command.command_value))
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def apply_load_pan_pattern(state: AudioState, command: ChannelTransferCommand, continuation: Continuation) -> None:
    """Copy five live pattern bytes into channel state, mark its next byte and preserve stream cursor convention."""
    command.return_stack = state.push_word(command.return_stack, command.channel_address)
    saved_context_word, command.return_stack = state.pop_word(command.return_stack)
    command.table_cursor = u16(saved_context_word)
    command.transfer_word = u16(17)
    adjusted_value, command.condition_bits = sum_word(command.table_cursor, command.transfer_word, command.condition_bits)
    command.table_cursor = u16(adjusted_value)
    command.argument_cursor, command.table_cursor = (command.table_cursor, command.argument_cursor)
    command.transfer_word = u16(5)
    while True:
        copy_live_byte(state, command, continuation)
        state.bus.transfer_boundary('progressive-block-copy')
        if command.transfer_word == 0:
            break
    command.command_value = u8(1)
    state.write(command.argument_cursor, u8(command.command_value))
    command.argument_cursor, command.table_cursor = (command.table_cursor, command.argument_cursor)
    command.argument_cursor = u16(command.argument_cursor - 1)
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def apply_select_instrument(state: AudioState, command: ChannelTransferCommand, continuation: Continuation) -> None:
    """Handle the channel-kind gate, live selector/bank arguments and shared instrument resolver/load phases."""
    channel_kind = state.read(u16(command.channel_address + 1))
    command.condition_bits = state.memory_bit_conditions(channel_kind, 7, command.condition_bits, u16(command.channel_address + 1), True)
    if not command.condition_bits & 64:
        argument_byte = state.read(command.argument_cursor)
        command.command_value = u8(argument_byte)
        command.command_value = u8(command.command_value | command.command_value)
        command.condition_bits = logic_conditions(command.command_value, False)
        if not command.condition_bits & 128:
            command.return_stack = state.consume_return(command.return_stack, continuation)
            return
        command.argument_cursor = u16(command.argument_cursor + 1)
        command.return_stack = state.consume_return(command.return_stack, continuation)
        return
    else:
        from .business_loaders import reset_operator_release
        from .contexts import ResetOperatorReleaseInput
        command.return_stack = state.push_word(command.return_stack, 3382)
        reset_operator_release_outcome = reset_operator_release(state, ResetOperatorReleaseInput(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, sample=command.command_value, stack_cursor=command.return_stack, continuation=Continuation('driver', 3382)))
        command.channel_address = reset_operator_release_outcome.channel_cursor
        command.condition_bits = reset_operator_release_outcome.conditions
        command.transfer_word = reset_operator_release_outcome.count_and_data
        command.command_value = reset_operator_release_outcome.sample
        command.return_stack = reset_operator_release_outcome.stack_cursor
        argument_byte_2 = state.read(command.argument_cursor)
        command.command_value = u8(argument_byte_2)
        state.write(u16(command.channel_address + 8), u8(command.command_value))
        command.return_stack = state.push_word(command.return_stack, command.command_value << 8 | command.condition_bits)
        command.argument_cursor = u16(command.argument_cursor + 1)
        argument_byte_3 = state.read(command.argument_cursor)
        command.command_value = u8(argument_byte_3)
        state.write(u16(command.channel_address + 15), u8(command.command_value))
        saved_context_word, command.return_stack = state.pop_word(command.return_stack)
        command.command_value, command.condition_bits = (high(saved_context_word), low(saved_context_word))
        command.command_value = u8(command.command_value | command.command_value)
        command.condition_bits = logic_conditions(command.command_value, False)
        if not command.condition_bits & 128:
            command.argument_cursor = u16(command.argument_cursor - 1)
            command.return_stack = state.push_word(command.return_stack, command.argument_cursor)
            command.transfer_word = replace_high(command.transfer_word, command.command_value)
            from .business_voice import lookup_instrument
            from .contexts import LookupInstrumentInput
            command.return_stack = state.push_word(command.return_stack, 3430)
            lookup_instrument_outcome = lookup_instrument(state, LookupInstrumentInput(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack, continuation=Continuation('driver', 3430)))
            command.channel_address = lookup_instrument_outcome.channel_cursor
            command.condition_bits = lookup_instrument_outcome.conditions
            command.transfer_word = lookup_instrument_outcome.count_and_data
            command.table_cursor = lookup_instrument_outcome.lookup_cursor
            command.argument_cursor = lookup_instrument_outcome.parameter_cursor
            command.command_value = lookup_instrument_outcome.sample
            command.return_stack = lookup_instrument_outcome.stack_cursor
        else:
            resolve_banked_instrument(state, command, continuation)
        finish_instrument_load(state, command, continuation)

def apply_select_banked_instrument(state: AudioState, command: ChannelTransferCommand, continuation: Continuation) -> None:
    """Resolve and load the live banked selector through the same instrument phases."""
    resolve_banked_instrument(state, command, continuation)
    finish_instrument_load(state, command, continuation)

def apply_set_stereo_pan(state: AudioState, command: ChannelTransferCommand, continuation: Continuation) -> None:
    """Preserve the declared low stereo bits and merge the live argument through the shared FM phase."""
    command.transfer_word = replace_low(command.transfer_word, 63)
    merge_stereo_argument(state, command, continuation)

def apply_set_lfo_and_stereo_pan(state: AudioState, command: ChannelTransferCommand, continuation: Continuation) -> None:
    """Write the LFO parameter first, then merge the live stereo argument through the shared phase."""
    command.transfer_word = replace_low(command.transfer_word, command.command_value)
    command.command_value = u8(34)
    from .business_hardware import write_fm_port_zero_entry
    from .contexts import WriteFmPortZeroEntryInput
    command.return_stack = state.push_word(command.return_stack, 3461)
    write_fm_port_zero_entry_outcome = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, sample=command.command_value, stack_cursor=command.return_stack, continuation=Continuation('driver', 3461)))
    command.channel_address = write_fm_port_zero_entry_outcome.channel_cursor
    command.condition_bits = write_fm_port_zero_entry_outcome.conditions
    command.transfer_word = write_fm_port_zero_entry_outcome.count_and_data
    command.command_value = write_fm_port_zero_entry_outcome.sample
    command.return_stack = write_fm_port_zero_entry_outcome.stack_cursor
    command.argument_cursor = u16(command.argument_cursor + 1)
    command.transfer_word = replace_low(command.transfer_word, 192)
    pass
    merge_stereo_argument(state, command, continuation)

def apply_set_psg_noise(state: AudioState, command: ChannelArgumentCommand, continuation: Continuation) -> None:
    """Keep channel gating, chip writes, live noise parameter and original zero/nonzero flag rules."""
    channel_kind = state.read(u16(command.channel_address + 1))
    command.condition_bits = state.memory_bit_conditions(channel_kind, 2, command.condition_bits, u16(command.channel_address + 1), True)
    if not command.condition_bits & 64:
        command.return_stack = state.consume_return(command.return_stack, continuation)
        return
    command.command_value = u8(223)
    state.write(32529, u8(command.command_value))
    argument_byte = state.read(command.argument_cursor)
    command.command_value = u8(argument_byte)
    state.write(u16(command.channel_address + 26), u8(command.command_value))
    channel_flags = state.read(u16(command.channel_address + 0))
    state.write(u16(command.channel_address + 0), u8(channel_flags | 1))
    command.command_value = u8(command.command_value | command.command_value)
    command.condition_bits = logic_conditions(command.command_value, False)
    if not not command.condition_bits & 64:
        channel_flags_2 = state.read(u16(command.channel_address + 0))
        state.write(u16(command.channel_address + 0), u8(channel_flags_2 & 254))
        command.command_value = u8(255)
    state.write(32529, u8(command.command_value))
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def apply_set_psg_envelope(state: AudioState, command: ChannelValueCommand, continuation: Continuation) -> None:
    """Store the PSG envelope only through the original channel-kind gate."""
    channel_kind = state.read(u16(command.channel_address + 1))
    command.condition_bits = state.memory_bit_conditions(channel_kind, 7, command.condition_bits, u16(command.channel_address + 1), True)
    if bool(command.condition_bits & 64):
        command.return_stack = state.consume_return(command.return_stack, continuation)
        return
    state.write(u16(command.channel_address + 8), u8(command.command_value))
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return
