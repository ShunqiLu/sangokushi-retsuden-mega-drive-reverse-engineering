"""Structured intermediate audio logic, not a complete CPU/timing proof."""
from .domain import (AudioState, AudioBoundary, Continuation, AlternateGroup,
    Byte, Word, byte, word, checked_state, u8, u16, low, high, replace_low,
    replace_high, logic_conditions, sum_byte, difference_byte,
    comparison_conditions, increment_byte, decrement_byte, sum_word,
    difference_word, tested_bit_conditions, copy_byte_conditions)
from .contexts import (
    InitializeAudioWorkspaceInput, InitializeAudioWorkspaceResult,
)

def initialize_audio_workspace(state: AudioState, inputs: InitializeAudioWorkspaceInput) -> InitializeAudioWorkspaceResult:
    """Initialize audio workspace."""
    checked_state(state)
    if type(inputs) is not InitializeAudioWorkspaceInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    auxiliary_cursor = inputs.auxiliary_cursor
    channel_cursor = inputs.channel_cursor
    conditions = inputs.conditions
    count_and_data = inputs.count_and_data
    lookup_cursor = inputs.lookup_cursor
    parameter_cursor = inputs.parameter_cursor
    sample = inputs.sample
    stack_cursor = inputs.stack_cursor
    # source-effect startup:0000:xor
    sample = u8(sample ^ sample)
    conditions = logic_conditions(sample, False)
    # source-effect startup:0001:ld
    count_and_data = u16(8153)
    # source-effect startup:0004:ld
    parameter_cursor = u16(39)
    # source-effect startup:0007:ld
    lookup_cursor = u16(38)
    # source-effect startup:000a:ld
    stack_cursor = u16(lookup_cursor)
    # source-effect startup:000b:ld
    state.write(lookup_cursor, u8(sample))
    # source-effect startup:000c:ldir
    while True:
        copied_byte = state.read(lookup_cursor)
        state.write(parameter_cursor, copied_byte)
        lookup_cursor = u16(lookup_cursor + 1)
        parameter_cursor = u16(parameter_cursor + 1)
        count_and_data = u16(count_and_data - 1)
        conditions = copy_byte_conditions(sample, copied_byte, count_and_data, conditions)
        state.bus.transfer_boundary("progressive-block-copy")
        if count_and_data == 0:
            break
    # source-effect startup:000e:pop
    saved_audio_word_1, stack_cursor = state.pop_word(stack_cursor)
    auxiliary_cursor = u16(saved_audio_word_1)
    # source-effect startup:0010:pop
    saved_audio_word_2, stack_cursor = state.pop_word(stack_cursor)
    channel_cursor = u16(saved_audio_word_2)
    # source-effect startup:0012:ld
    state.platform.set_interrupt_vector(sample)
    # source-effect startup:0014:ld
    state.platform.set_refresh(sample)
    # source-effect startup:0016:pop
    saved_audio_word_3, stack_cursor = state.pop_word(stack_cursor)
    parameter_cursor = u16(saved_audio_word_3)
    # source-effect startup:0017:pop
    saved_audio_word_4, stack_cursor = state.pop_word(stack_cursor)
    lookup_cursor = u16(saved_audio_word_4)
    # source-effect startup:0018:pop
    saved_audio_word_5, stack_cursor = state.pop_word(stack_cursor)
    sample, conditions = high(saved_audio_word_5), low(saved_audio_word_5)
    # source-effect startup:0019:ex
    alternate_sample_and_conditions_6 = word(state.platform.exchange_alternate_accumulator((sample << 8) | conditions))
    sample, conditions = high(alternate_sample_and_conditions_6), low(alternate_sample_and_conditions_6)
    # source-effect startup:001a:exx
    alternate_group_7 = state.platform.exchange_alternate_group(AlternateGroup(count_and_data, parameter_cursor, lookup_cursor))
    alternate_group_7.validate()
    count_and_data, parameter_cursor, lookup_cursor = alternate_group_7.count_and_data, alternate_group_7.parameter_cursor, alternate_group_7.lookup_cursor
    # source-effect startup:001b:pop
    saved_audio_word_8, stack_cursor = state.pop_word(stack_cursor)
    count_and_data = u16(saved_audio_word_8)
    # source-effect startup:001c:pop
    saved_audio_word_9, stack_cursor = state.pop_word(stack_cursor)
    parameter_cursor = u16(saved_audio_word_9)
    # source-effect startup:001d:pop
    saved_audio_word_10, stack_cursor = state.pop_word(stack_cursor)
    lookup_cursor = u16(saved_audio_word_10)
    # source-effect startup:001e:pop
    saved_audio_word_11, stack_cursor = state.pop_word(stack_cursor)
    sample, conditions = high(saved_audio_word_11), low(saved_audio_word_11)
    # source-effect startup:001f:ld
    stack_cursor = u16(lookup_cursor)
    # source-effect startup:0020:di
    state.platform.interrupt_control(False, False)
    # source-effect startup:0021:im
    state.platform.interrupt_mode(1)
    # source-effect startup:0023:ld
    state.write(lookup_cursor, u8(233))
    # source-effect startup:0025:jp
    current_transfer_values_12 = InitializeAudioWorkspaceInput(auxiliary_cursor=auxiliary_cursor, channel_cursor=channel_cursor, conditions=conditions, count_and_data=count_and_data, lookup_cursor=lookup_cursor, parameter_cursor=parameter_cursor, sample=sample, stack_cursor=stack_cursor, continuation=inputs.continuation).validate(state)
    state.indirect_transfer("startup", lookup_cursor, current_transfer_values_12)
