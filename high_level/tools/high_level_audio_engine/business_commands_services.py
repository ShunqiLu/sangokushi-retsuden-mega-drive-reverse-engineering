"""Shared real command transactions: progressive copy, FM fields, stereo merge, instrument resolution/load and envelope/timer commits. Every body is an input to source generation; no code-byte payload or original-body fallback."""
from .domain import AudioState, AudioBoundary, Continuation, AlternateGroup, Byte, Word, byte, word, checked_state, u8, u16, low, high, replace_low, replace_high, logic_conditions, sum_byte, difference_byte, comparison_conditions, increment_byte, decrement_byte, sum_word, difference_word, tested_bit_conditions, copy_byte_conditions
from .contexts_commands import StreamTransferCommand, DriverLookupCommand, ChannelDurationCommand, ChannelValueCommand, ChannelTransferCommand, ChannelPointerCommand, ChannelArgumentCommand, DriverValueCommand, SoundDispatchCommand

def send_four_fm_fields(state: AudioState, command: ChannelTransferCommand, continuation: Continuation) -> None:
    """Write four register/value fields through real FM calls, adopt callback cells and retain source cursor convention."""
    command.table_cursor = u16(1249)
    command.transfer_word = replace_high(command.transfer_word, 4)
    while True:
        argument_byte = state.read(command.argument_cursor)
        command.command_value = u8(argument_byte)
        command.argument_cursor = u16(command.argument_cursor + 1)
        command.transfer_word = replace_low(command.transfer_word, command.command_value)
        table_byte = state.read(command.table_cursor)
        command.command_value = u8(table_byte)
        command.table_cursor = u16(command.table_cursor + 1)
        from .business_hardware import write_channel_fm_register
        from .contexts import WriteChannelFmRegisterInput
        command.return_stack = state.push_word(command.return_stack, 3060)
        write_channel_fm_register_outcome = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, sample=command.command_value, stack_cursor=command.return_stack, continuation=Continuation('driver', 3060)))
        command.channel_address = write_channel_fm_register_outcome.channel_cursor
        command.condition_bits = write_channel_fm_register_outcome.conditions
        command.transfer_word = write_channel_fm_register_outcome.count_and_data
        command.command_value = write_channel_fm_register_outcome.sample
        command.return_stack = write_channel_fm_register_outcome.stack_cursor
        command.transfer_word = replace_high(command.transfer_word, u8(high(command.transfer_word) - 1))
        if high(command.transfer_word) != 0:
            continue
        break
    command.argument_cursor = u16(command.argument_cursor - 1)
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def merge_stereo_argument(state: AudioState, command: ChannelTransferCommand, continuation: Continuation) -> None:
    """Merge stored stereo bits and the live argument, write channel/FM state, restore cursor roles and return."""
    stereo_bits = state.read(u16(command.channel_address + 10))
    command.command_value = u8(stereo_bits)
    command.command_value = u8(command.command_value & low(command.transfer_word))
    command.condition_bits = logic_conditions(command.command_value, True)
    command.argument_cursor, command.table_cursor = (command.table_cursor, command.argument_cursor)
    table_byte = state.read(command.table_cursor)
    command.command_value = u8(command.command_value | table_byte)
    command.condition_bits = logic_conditions(command.command_value, False)
    state.write(u16(command.channel_address + 10), u8(command.command_value))
    command.transfer_word = replace_low(command.transfer_word, command.command_value)
    command.command_value = u8(180)
    from .business_hardware import write_channel_fm_register
    from .contexts import WriteChannelFmRegisterInput
    command.return_stack = state.push_word(command.return_stack, 3455)
    write_channel_fm_register_outcome = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, sample=command.command_value, stack_cursor=command.return_stack, continuation=Continuation('driver', 3455)))
    command.channel_address = write_channel_fm_register_outcome.channel_cursor
    command.condition_bits = write_channel_fm_register_outcome.conditions
    command.transfer_word = write_channel_fm_register_outcome.count_and_data
    command.command_value = write_channel_fm_register_outcome.sample
    command.return_stack = write_channel_fm_register_outcome.stack_cursor
    command.argument_cursor, command.table_cursor = (command.table_cursor, command.argument_cursor)
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def commit_pitch_envelope(state: AudioState, command: ChannelArgumentCommand, continuation: Continuation) -> None:
    """Commit the current pitch-envelope byte and complete the real return."""
    state.write(u16(command.channel_address + 7), u8(command.command_value))
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def commit_timer_control(state: AudioState, command: ChannelTransferCommand, continuation: Continuation) -> None:
    """Commit current timer state and write chip control through the original port-zero call boundary."""
    state.write(7186, u8(command.command_value))
    command.transfer_word = replace_low(command.transfer_word, command.command_value)
    command.command_value = u8(39)
    from .business_hardware import write_fm_port_zero_entry
    from .contexts import WriteFmPortZeroEntryInput
    command.return_stack = state.push_word(command.return_stack, 3360)
    write_fm_port_zero_entry_outcome = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, sample=command.command_value, stack_cursor=command.return_stack, continuation=Continuation('driver', 3360)))
    command.channel_address = write_fm_port_zero_entry_outcome.channel_cursor
    command.condition_bits = write_fm_port_zero_entry_outcome.conditions
    command.transfer_word = write_fm_port_zero_entry_outcome.count_and_data
    command.command_value = write_fm_port_zero_entry_outcome.sample
    command.return_stack = write_fm_port_zero_entry_outcome.stack_cursor
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def resolve_banked_instrument(state: AudioState, command: ChannelTransferCommand, continuation: Continuation) -> None:
    """Resolve the bank root and selector through real pointer services, preserving saved live argument on the stack."""
    command.return_stack = state.push_word(command.return_stack, command.argument_cursor)
    command.table_cursor = u16(32768)
    command.transfer_word = replace_low(command.transfer_word, 4)
    bank_selector = state.read(u16(command.channel_address + 15))
    command.command_value = u8(bank_selector)
    command.command_value, command.condition_bits = difference_byte(command.command_value, 129)
    from .business_hardware import lookup_pointer_after_root
    from .contexts import LookupPointerAfterRootInput
    command.return_stack = state.push_word(command.return_stack, 3411)
    lookup_pointer_after_root_outcome = lookup_pointer_after_root(state, LookupPointerAfterRootInput(conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, sample=command.command_value, stack_cursor=command.return_stack, continuation=Continuation('driver', 3411)))
    command.condition_bits = lookup_pointer_after_root_outcome.conditions
    command.transfer_word = lookup_pointer_after_root_outcome.count_and_data
    command.table_cursor = lookup_pointer_after_root_outcome.lookup_cursor
    command.command_value = lookup_pointer_after_root_outcome.sample
    command.return_stack = lookup_pointer_after_root_outcome.stack_cursor
    from .business_hardware import index_word_pointer
    from .contexts import IndexWordPointerInput
    command.return_stack = state.push_word(command.return_stack, 3412)
    index_word_pointer_outcome = index_word_pointer(state, IndexWordPointerInput(conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, sample=command.command_value, stack_cursor=command.return_stack, continuation=Continuation('driver', 3412)))
    command.condition_bits = index_word_pointer_outcome.conditions
    command.transfer_word = index_word_pointer_outcome.count_and_data
    command.table_cursor = index_word_pointer_outcome.lookup_cursor
    command.command_value = index_word_pointer_outcome.sample
    command.return_stack = index_word_pointer_outcome.stack_cursor
    from .business_hardware import read_stream_word
    from .contexts import ReadStreamWordInput
    command.return_stack = state.push_word(command.return_stack, 3413)
    read_stream_word_outcome = read_stream_word(state, ReadStreamWordInput(conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, sample=command.command_value, stack_cursor=command.return_stack, continuation=Continuation('driver', 3413)))
    command.condition_bits = read_stream_word_outcome.conditions
    command.transfer_word = read_stream_word_outcome.count_and_data
    command.table_cursor = read_stream_word_outcome.lookup_cursor
    command.command_value = read_stream_word_outcome.sample
    command.return_stack = read_stream_word_outcome.stack_cursor
    instrument_selector = state.read(u16(command.channel_address + 8))
    command.command_value = u8(instrument_selector)
    command.command_value = u8(command.command_value & 127)
    command.condition_bits = logic_conditions(command.command_value, True)
    command.transfer_word = replace_high(command.transfer_word, command.command_value)
    from .business_voice import offset_instrument
    from .contexts import OffsetInstrumentInput
    command.return_stack = state.push_word(command.return_stack, 3422)
    offset_instrument_outcome = offset_instrument(state, OffsetInstrumentInput(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack, continuation=Continuation('driver', 3422)))
    command.channel_address = offset_instrument_outcome.channel_cursor
    command.condition_bits = offset_instrument_outcome.conditions
    command.transfer_word = offset_instrument_outcome.count_and_data
    command.table_cursor = offset_instrument_outcome.lookup_cursor
    command.argument_cursor = offset_instrument_outcome.parameter_cursor
    command.command_value = offset_instrument_outcome.sample
    command.return_stack = offset_instrument_outcome.stack_cursor
    pass

def finish_instrument_load(state: AudioState, command: ChannelTransferCommand, continuation: Continuation) -> None:
    """Load the selected voice through its real call and restore the saved argument before returning."""
    from .business_voice import load_instrument
    from .contexts import LoadInstrumentInput
    command.return_stack = state.push_word(command.return_stack, 3433)
    load_instrument_outcome = load_instrument(state, LoadInstrumentInput(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack, continuation=Continuation('driver', 3433)))
    command.channel_address = load_instrument_outcome.channel_cursor
    command.condition_bits = load_instrument_outcome.conditions
    command.transfer_word = load_instrument_outcome.count_and_data
    command.table_cursor = load_instrument_outcome.lookup_cursor
    command.argument_cursor = load_instrument_outcome.parameter_cursor
    command.command_value = load_instrument_outcome.sample
    command.return_stack = load_instrument_outcome.stack_cursor
    saved_context_word, command.return_stack = state.pop_word(command.return_stack)
    command.argument_cursor = u16(saved_context_word)
    command.return_stack = state.consume_return(command.return_stack, continuation)
    return

def copy_live_byte(state: AudioState, command: StreamTransferCommand, continuation: Continuation) -> None:
    """Copy one live byte, advancing both WORD cursors and remaining count before updating original conditions."""
    copied_byte = state.read(command.table_cursor)
    state.write(command.argument_cursor, copied_byte)
    command.table_cursor = u16(command.table_cursor + 1)
    command.argument_cursor = u16(command.argument_cursor + 1)
    command.transfer_word = u16(command.transfer_word - 1)
    command.condition_bits = copy_byte_conditions(command.command_value, copied_byte, command.transfer_word, command.condition_bits)
