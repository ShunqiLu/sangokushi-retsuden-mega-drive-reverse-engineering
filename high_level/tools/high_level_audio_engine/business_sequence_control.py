"""Sequence control flow and live register-command transactions.

These are actual algorithms, not an opcode dispatcher or cached command AST.
Four control entries manage absolute targets, the channel-local word return
area and indexed repeat counters. Three register entries read a live two-byte
parameter and use the original native service boundaries. All source/stack
accesses remain ordered, including separate updates of channel+9. Byte/word
wrap, callback outcomes and nonlocal returns deliberately retain old behavior.
The other sequence commands remain a mechanical intermediate elsewhere.
"""
from .domain import (AudioState, Continuation, u8, u16, low, high, replace_low,
                     replace_high, logic_conditions, sum_byte, sum_word,
                     decrement_byte, increment_byte)
from .contexts_sequence import SequenceCommandContext, SequenceParameterContext, SequenceReturnContext


def execute_absolute_jump(state: AudioState, command: SequenceCommandContext, continuation: Continuation) -> None:
    """Read the absolute target at the argument cursor and return target-minus-one.

    The outer stream continuation supplies the later increment. Do not advance
    here to a conventional next-byte cursor or prefetch the second target byte.
    """
    jump_from_live_parameter(state, command, continuation)


def jump_from_live_parameter(state: AudioState, command: SequenceCommandContext, continuation: Continuation) -> None:
    """Shared jump tail, used by both the absolute command and repeat-taken path."""
    command.argument_cursor, command.scratch_cursor = command.scratch_cursor, command.argument_cursor
    target_low = state.read(command.scratch_cursor)
    command.argument_cursor = replace_low(command.argument_cursor, target_low)
    command.scratch_cursor = u16(command.scratch_cursor + 1)
    target_high = state.read(command.scratch_cursor)
    command.argument_cursor = replace_high(command.argument_cursor, target_high)
    command.argument_cursor = u16(command.argument_cursor - 1)
    command.return_stack = state.consume_return(command.return_stack, continuation)


def execute_sequence_call(state: AudioState, command: SequenceCommandContext, continuation: Continuation) -> None:
    """Save the live parameter return word in the channel-local area, then jump.

    Channel+9 is decremented twice with a fresh read between operations. Native
    stack pushes preserve the target and channel before those writes. These are
    not replaced by a Python call stack or one atomic slot-index update.
    """
    command.transfer_word = replace_low(command.transfer_word, command.command_byte)
    command.argument_cursor = u16(command.argument_cursor + 1)
    target_high_byte = state.read(command.argument_cursor)
    command.command_byte = u8(target_high_byte)
    command.transfer_word = replace_high(command.transfer_word, command.command_byte)
    command.return_stack = state.push_word(command.return_stack, command.transfer_word)
    command.return_stack = state.push_word(command.return_stack, command.channel_address)
    channel_base, command.return_stack = state.pop_word(command.return_stack)
    command.scratch_cursor = u16(channel_base)
    first_slot = state.read(u16(command.channel_address + 9))
    lower_slot, command.condition_bits = decrement_byte(first_slot, command.condition_bits)
    state.write(u16(command.channel_address + 9), u8(lower_slot))
    live_slot = state.read(u16(command.channel_address + 9))
    command.transfer_word = replace_low(command.transfer_word, live_slot)
    second_slot = state.read(u16(command.channel_address + 9))
    next_slot, command.condition_bits = decrement_byte(second_slot, command.condition_bits)
    state.write(u16(command.channel_address + 9), u8(next_slot))
    command.transfer_word = replace_high(command.transfer_word, 0)
    return_address, command.condition_bits = sum_word(command.scratch_cursor, command.transfer_word, command.condition_bits)
    command.scratch_cursor = u16(return_address)
    state.write(command.scratch_cursor, u8(high(command.argument_cursor)))
    command.scratch_cursor = u16(command.scratch_cursor - 1)
    state.write(command.scratch_cursor, u8(low(command.argument_cursor)))
    call_target, command.return_stack = state.pop_word(command.return_stack)
    command.argument_cursor = u16(call_target)
    command.argument_cursor = u16(command.argument_cursor - 1)
    command.return_stack = state.consume_return(command.return_stack, continuation)


def execute_sequence_return(state: AudioState, command: SequenceReturnContext, continuation: Continuation) -> None:
    """Read the saved word, then perform the two original live slot increments."""
    command.return_stack = state.push_word(command.return_stack, command.channel_address)
    channel_base, command.return_stack = state.pop_word(command.return_stack)
    command.scratch_cursor = u16(channel_base)
    slot = state.read(u16(command.channel_address + 9))
    command.transfer_word = replace_low(command.transfer_word, slot)
    command.transfer_word = replace_high(command.transfer_word, 0)
    saved_address, command.condition_bits = sum_word(command.scratch_cursor, command.transfer_word, command.condition_bits)
    command.scratch_cursor = u16(saved_address)
    return_low = state.read(command.scratch_cursor)
    command.argument_cursor = replace_low(command.argument_cursor, return_low)
    command.scratch_cursor = u16(command.scratch_cursor + 1)
    return_high = state.read(command.scratch_cursor)
    command.argument_cursor = replace_high(command.argument_cursor, return_high)
    first_slot = state.read(u16(command.channel_address + 9))
    higher_slot, command.condition_bits = increment_byte(first_slot, command.condition_bits)
    state.write(u16(command.channel_address + 9), u8(higher_slot))
    second_slot = state.read(u16(command.channel_address + 9))
    next_slot, command.condition_bits = increment_byte(second_slot, command.condition_bits)
    state.write(u16(command.channel_address + 9), u8(next_slot))
    command.return_stack = state.consume_return(command.return_stack, continuation)


def execute_sequence_repeat(state: AudioState, command: SequenceCommandContext, continuation: Continuation) -> None:
    """Maintain one indexed live BYTE counter and choose jump or fall-through.

    A zero counter is loaded from the next live argument, then freshly read and
    decremented. A loaded zero wraps to 255 as originally written. The counter
    byte can alias stream/native-stack bytes, so neither reload nor decrement
    is cached. The taken path shares the exact absolute-jump tail.
    """
    command.argument_cursor = u16(command.argument_cursor + 1)
    counter_offset, command.condition_bits = sum_byte(command.command_byte, 40)
    command.command_byte = u8(counter_offset)
    command.transfer_word = replace_low(command.transfer_word, command.command_byte)
    command.transfer_word = replace_high(command.transfer_word, 0)
    command.return_stack = state.push_word(command.return_stack, command.channel_address)
    channel_base, command.return_stack = state.pop_word(command.return_stack)
    command.scratch_cursor = u16(channel_base)
    counter_address, command.condition_bits = sum_word(command.scratch_cursor, command.transfer_word, command.condition_bits)
    command.scratch_cursor = u16(counter_address)
    live_count = state.read(command.scratch_cursor)
    command.command_byte = u8(live_count)
    command.command_byte = u8(command.command_byte | command.command_byte)
    command.condition_bits = logic_conditions(command.command_byte, False)
    if not (not (command.condition_bits & 0x40)):
        initial_count = state.read(command.argument_cursor)
        command.command_byte = u8(initial_count)
        state.write(command.scratch_cursor, u8(command.command_byte))
    command.argument_cursor = u16(command.argument_cursor + 1)
    live_counter = state.read(command.scratch_cursor)
    remaining, command.condition_bits = decrement_byte(live_counter, command.condition_bits)
    state.write(command.scratch_cursor, u8(remaining))
    if not (command.condition_bits & 0x40):
        jump_from_live_parameter(state, command, continuation)
    else:
        command.argument_cursor = u16(command.argument_cursor + 1)
        command.return_stack = state.consume_return(command.return_stack, continuation)


def read_live_register_parameter(state: AudioState, command: SequenceParameterContext, continuation: Continuation) -> None:
    """Read selector before value using the original two-cursor swap protocol."""
    command.argument_cursor, command.scratch_cursor = command.scratch_cursor, command.argument_cursor
    register_selector = state.read(command.scratch_cursor)
    command.command_byte = u8(register_selector)
    command.scratch_cursor = u16(command.scratch_cursor + 1)
    field_value = state.read(command.scratch_cursor)
    command.transfer_word = replace_low(command.transfer_word, field_value)
    command.argument_cursor, command.scratch_cursor = command.scratch_cursor, command.argument_cursor
    command.return_stack = state.consume_return(command.return_stack, continuation)


def execute_channel_register(state: AudioState, command: SequenceCommandContext, continuation: Continuation) -> None:
    """Read current parameters through their CALL boundary, then write channel FM."""
    call_register_parameter_service(state, command, 3244)
    write_channel_register_service(state, command)
    command.return_stack = state.consume_return(command.return_stack, continuation)


def execute_port_zero_register(state: AudioState, command: SequenceCommandContext, continuation: Continuation) -> None:
    """Read current parameters through their CALL boundary, then write port zero."""
    call_register_parameter_service(state, command, 3249)
    write_port_zero_register_service(state, command)
    command.return_stack = state.consume_return(command.return_stack, continuation)


def call_register_parameter_service(state: AudioState, command: SequenceCommandContext, return_address: int) -> None:
    """Preserve the real parameter CALL stack and every returned six-cell alias."""
    from .business_sequence import read_register_parameter_pair
    from .contexts import ReadRegisterParameterPairInput
    command.return_stack = state.push_word(command.return_stack, return_address)
    parameter_outcome = read_register_parameter_pair(state, ReadRegisterParameterPairInput(conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.scratch_cursor, parameter_cursor=command.argument_cursor, sample=command.command_byte, stack_cursor=command.return_stack, continuation=Continuation("driver", return_address)))
    command.condition_bits = parameter_outcome.conditions
    command.transfer_word = parameter_outcome.count_and_data
    command.scratch_cursor = parameter_outcome.lookup_cursor
    command.argument_cursor = parameter_outcome.parameter_cursor
    command.command_byte = parameter_outcome.sample
    command.return_stack = parameter_outcome.stack_cursor


def write_channel_register_service(state: AudioState, command: SequenceCommandContext) -> None:
    """Explicit channel-FM service, adopting all five current returned cells."""
    from .business_hardware import write_channel_fm_register
    from .contexts import WriteChannelFmRegisterInput
    command.return_stack = state.push_word(command.return_stack, 3245)
    hardware_outcome = write_channel_fm_register(state, WriteChannelFmRegisterInput(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, sample=command.command_byte, stack_cursor=command.return_stack, continuation=Continuation("driver", 3245)))
    command.channel_address = hardware_outcome.channel_cursor
    command.condition_bits = hardware_outcome.conditions
    command.transfer_word = hardware_outcome.count_and_data
    command.command_byte = hardware_outcome.sample
    command.return_stack = hardware_outcome.stack_cursor


def write_port_zero_register_service(state: AudioState, command: SequenceCommandContext) -> None:
    """Explicit port-zero service, adopting all five current returned cells."""
    from .business_hardware import write_fm_port_zero_entry
    from .contexts import WriteFmPortZeroEntryInput
    command.return_stack = state.push_word(command.return_stack, 3250)
    hardware_outcome = write_fm_port_zero_entry(state, WriteFmPortZeroEntryInput(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, sample=command.command_byte, stack_cursor=command.return_stack, continuation=Continuation("driver", 3250)))
    command.channel_address = hardware_outcome.channel_cursor
    command.condition_bits = hardware_outcome.conditions
    command.transfer_word = hardware_outcome.count_and_data
    command.command_byte = hardware_outcome.sample
    command.return_stack = hardware_outcome.stack_cursor
