"""Structured intermediate audio logic, not a complete CPU/timing proof."""
from .domain import (AudioState, AudioBoundary, Continuation, AlternateGroup,
    Byte, Word, byte, word, checked_state, u8, u16, low, high, replace_low,
    replace_high, logic_conditions, sum_byte, difference_byte,
    comparison_conditions, increment_byte, decrement_byte, sum_word,
    difference_word, tested_bit_conditions, copy_byte_conditions)
from .contexts import (
    StoreFmParametersInput, StoreFmParametersResult,
    WriteFmParametersInput, WriteFmParametersResult,
    SetAllDurationMultipliersInput, SetAllDurationMultipliersResult,
    SetDriverModeInput, SetDriverModeResult,
    LoadTimerReloadsInput, LoadTimerReloadsResult,
    AdjustTimerReloadsInput, AdjustTimerReloadsResult,
    DispatchPreservingChannelInput, DispatchPreservingChannelResult,
    CopySequenceBlockInput, CopySequenceBlockResult,
    SetPitchOffsetInput, SetPitchOffsetResult,
    SetVoiceEnvelopeInput, SetVoiceEnvelopeResult,
    AdjustNoteDividerInput, AdjustNoteDividerResult,
    SetMiscDriverFieldInput, SetMiscDriverFieldResult,
    AdjustPsgVolumeInput, AdjustPsgVolumeResult,
    WriteSequenceChannelRegisterInput, WriteSequenceChannelRegisterResult,
    WriteSequencePortZeroRegisterInput, WriteSequencePortZeroRegisterResult,
    ReadRegisterParameterPairInput, ReadRegisterParameterPairResult,
    SetPitchModulationInput, SetPitchModulationResult,
    SetNoteReleaseDurationInput, SetNoteReleaseDurationResult,
    LoadPanPatternInput, LoadPanPatternResult,
    MarkNoteContinuationInput, MarkNoteContinuationResult,
    SetSpecialChannelFrequencyInput, SetSpecialChannelFrequencyResult,
    WriteTimerControlInput, WriteTimerControlResult,
    SelectInstrumentInput, SelectInstrumentResult,
    SelectBankedInstrumentInput, SelectBankedInstrumentResult,
    SetStereoPanInput, SetStereoPanResult,
    SetLfoAndStereoPanInput, SetLfoAndStereoPanResult,
    AdjustNoteTransposeInput, AdjustNoteTransposeResult,
    SetDurationMultiplierInput, SetDurationMultiplierResult,
    SetPsgNoiseInput, SetPsgNoiseResult,
    SetPsgEnvelopeInput, SetPsgEnvelopeResult,
    SetPitchEnvelopeInput, SetPitchEnvelopeResult,
    StorePitchEnvelopeInput, StorePitchEnvelopeResult,
    JumpSequencePointerInput, JumpSequencePointerResult,
    SetPitchSlideModeInput, SetPitchSlideModeResult,
    SetRawFrequencyModeInput, SetRawFrequencyModeResult,
    CallSequenceSubroutineInput, CallSequenceSubroutineResult,
    ReturnSequenceSubroutineInput, ReturnSequenceSubroutineResult,
    RepeatSequenceSectionInput, RepeatSequenceSectionResult,
)

from .contexts_sequence import SequenceCommandContext, SequenceParameterContext, SequenceReturnContext
from .business_sequence_control import (execute_channel_register, execute_port_zero_register, read_live_register_parameter, execute_absolute_jump, execute_sequence_call, execute_sequence_return, execute_sequence_repeat)

from .contexts_commands import StreamTransferCommand, DriverLookupCommand, ChannelDurationCommand, ChannelValueCommand, ChannelTransferCommand, ChannelPointerCommand, ChannelArgumentCommand, DriverValueCommand, SoundDispatchCommand
from .business_commands_timing import (apply_set_all_duration_multipliers, apply_load_timer_reloads, apply_adjust_timer_reloads, apply_adjust_note_divider, apply_set_note_release_duration, apply_set_duration_multiplier, apply_write_timer_control)
from .business_commands_pitch import (apply_set_pitch_offset, apply_set_pitch_modulation, apply_set_special_channel_frequency, apply_adjust_note_transpose, apply_set_pitch_envelope, apply_store_pitch_envelope, apply_set_pitch_slide_mode, apply_set_raw_frequency_mode)
from .business_commands_voice import (apply_store_fm_parameters, apply_write_fm_parameters, apply_set_voice_envelope, apply_adjust_psg_volume, apply_load_pan_pattern, apply_select_instrument, apply_select_banked_instrument, apply_set_stereo_pan, apply_set_lfo_and_stereo_pan, apply_set_psg_noise, apply_set_psg_envelope)
from .business_commands_state import (apply_set_driver_mode, apply_dispatch_preserving_channel, apply_copy_sequence_block, apply_set_misc_driver_field, apply_mark_note_continuation)

def store_fm_parameters(state: AudioState, inputs: StoreFmParametersInput) -> StoreFmParametersResult:
    """Store fm parameters."""
    checked_state(state)
    if type(inputs) is not StoreFmParametersInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelTransferCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        table_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_store_fm_parameters(state, command, inputs.continuation)
    return StoreFmParametersResult(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def write_fm_parameters(state: AudioState, inputs: WriteFmParametersInput) -> WriteFmParametersResult:
    """Write fm parameters."""
    checked_state(state)
    if type(inputs) is not WriteFmParametersInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelTransferCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        table_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_write_fm_parameters(state, command, inputs.continuation)
    return WriteFmParametersResult(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def set_all_duration_multipliers(state: AudioState, inputs: SetAllDurationMultipliersInput) -> SetAllDurationMultipliersResult:
    """Set all duration multipliers."""
    checked_state(state)
    if type(inputs) is not SetAllDurationMultipliersInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = StreamTransferCommand(
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        table_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_set_all_duration_multipliers(state, command, inputs.continuation)
    return SetAllDurationMultipliersResult(conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def set_driver_mode(state: AudioState, inputs: SetDriverModeInput) -> SetDriverModeResult:
    """Set driver mode."""
    checked_state(state)
    if type(inputs) is not SetDriverModeInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = DriverValueCommand(
        condition_bits=inputs.conditions,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_set_driver_mode(state, command, inputs.continuation)
    return SetDriverModeResult(conditions=command.condition_bits, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def load_timer_reloads(state: AudioState, inputs: LoadTimerReloadsInput) -> LoadTimerReloadsResult:
    """Load timer reloads."""
    checked_state(state)
    if type(inputs) is not LoadTimerReloadsInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = StreamTransferCommand(
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        table_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_load_timer_reloads(state, command, inputs.continuation)
    return LoadTimerReloadsResult(conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def adjust_timer_reloads(state: AudioState, inputs: AdjustTimerReloadsInput) -> AdjustTimerReloadsResult:
    """Adjust timer reloads."""
    checked_state(state)
    if type(inputs) is not AdjustTimerReloadsInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = StreamTransferCommand(
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        table_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_adjust_timer_reloads(state, command, inputs.continuation)
    return AdjustTimerReloadsResult(conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def dispatch_preserving_channel(state: AudioState, inputs: DispatchPreservingChannelInput) -> DispatchPreservingChannelResult:
    """Dispatch preserving channel."""
    checked_state(state)
    if type(inputs) is not DispatchPreservingChannelInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = SoundDispatchCommand(
        auxiliary_address=inputs.auxiliary_cursor,
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        table_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_dispatch_preserving_channel(state, command, inputs.continuation)
    return DispatchPreservingChannelResult(auxiliary_cursor=command.auxiliary_address, channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def copy_sequence_block(state: AudioState, inputs: CopySequenceBlockInput) -> CopySequenceBlockResult:
    """Copy sequence block."""
    checked_state(state)
    if type(inputs) is not CopySequenceBlockInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = StreamTransferCommand(
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        table_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_copy_sequence_block(state, command, inputs.continuation)
    return CopySequenceBlockResult(conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def set_pitch_offset(state: AudioState, inputs: SetPitchOffsetInput) -> SetPitchOffsetResult:
    """Set pitch offset."""
    checked_state(state)
    if type(inputs) is not SetPitchOffsetInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelValueCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_set_pitch_offset(state, command, inputs.continuation)
    return SetPitchOffsetResult(channel_cursor=command.channel_address, conditions=command.condition_bits, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def set_voice_envelope(state: AudioState, inputs: SetVoiceEnvelopeInput) -> SetVoiceEnvelopeResult:
    """Set voice envelope."""
    checked_state(state)
    if type(inputs) is not SetVoiceEnvelopeInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelArgumentCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        argument_cursor=inputs.parameter_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_set_voice_envelope(state, command, inputs.continuation)
    return SetVoiceEnvelopeResult(channel_cursor=command.channel_address, conditions=command.condition_bits, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def adjust_note_divider(state: AudioState, inputs: AdjustNoteDividerInput) -> AdjustNoteDividerResult:
    """Adjust note divider."""
    checked_state(state)
    if type(inputs) is not AdjustNoteDividerInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = DriverLookupCommand(
        condition_bits=inputs.conditions,
        table_cursor=inputs.lookup_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_adjust_note_divider(state, command, inputs.continuation)
    return AdjustNoteDividerResult(conditions=command.condition_bits, lookup_cursor=command.table_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def set_misc_driver_field(state: AudioState, inputs: SetMiscDriverFieldInput) -> SetMiscDriverFieldResult:
    """Set misc driver field."""
    checked_state(state)
    if type(inputs) is not SetMiscDriverFieldInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = DriverValueCommand(
        condition_bits=inputs.conditions,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_set_misc_driver_field(state, command, inputs.continuation)
    return SetMiscDriverFieldResult(conditions=command.condition_bits, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def adjust_psg_volume(state: AudioState, inputs: AdjustPsgVolumeInput) -> AdjustPsgVolumeResult:
    """Adjust psg volume."""
    checked_state(state)
    if type(inputs) is not AdjustPsgVolumeInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelValueCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_adjust_psg_volume(state, command, inputs.continuation)
    return AdjustPsgVolumeResult(channel_cursor=command.channel_address, conditions=command.condition_bits, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def write_sequence_channel_register(state: AudioState, inputs: WriteSequenceChannelRegisterInput) -> WriteSequenceChannelRegisterResult:
    """Write sequence channel register."""
    checked_state(state)
    if type(inputs) is not WriteSequenceChannelRegisterInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = SequenceCommandContext(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        scratch_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    execute_channel_register(state, command, inputs.continuation)
    return WriteSequenceChannelRegisterResult(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.scratch_cursor, parameter_cursor=command.argument_cursor, sample=command.command_byte, stack_cursor=command.return_stack).validate(state)

def write_sequence_port_zero_register(state: AudioState, inputs: WriteSequencePortZeroRegisterInput) -> WriteSequencePortZeroRegisterResult:
    """Write sequence port zero register."""
    checked_state(state)
    if type(inputs) is not WriteSequencePortZeroRegisterInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = SequenceCommandContext(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        scratch_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    execute_port_zero_register(state, command, inputs.continuation)
    return WriteSequencePortZeroRegisterResult(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.scratch_cursor, parameter_cursor=command.argument_cursor, sample=command.command_byte, stack_cursor=command.return_stack).validate(state)

def read_register_parameter_pair(state: AudioState, inputs: ReadRegisterParameterPairInput) -> ReadRegisterParameterPairResult:
    """Read register parameter pair."""
    checked_state(state)
    if type(inputs) is not ReadRegisterParameterPairInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = SequenceParameterContext(
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        scratch_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    read_live_register_parameter(state, command, inputs.continuation)
    return ReadRegisterParameterPairResult(conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.scratch_cursor, parameter_cursor=command.argument_cursor, sample=command.command_byte, stack_cursor=command.return_stack).validate(state)

def set_pitch_modulation(state: AudioState, inputs: SetPitchModulationInput) -> SetPitchModulationResult:
    """Set pitch modulation."""
    checked_state(state)
    if type(inputs) is not SetPitchModulationInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelPointerCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        argument_cursor=inputs.parameter_cursor,
        return_stack=inputs.stack_cursor,
    )
    apply_set_pitch_modulation(state, command, inputs.continuation)
    return SetPitchModulationResult(channel_cursor=command.channel_address, conditions=command.condition_bits, parameter_cursor=command.argument_cursor, stack_cursor=command.return_stack).validate(state)

def set_note_release_duration(state: AudioState, inputs: SetNoteReleaseDurationInput) -> SetNoteReleaseDurationResult:
    """Set note release duration."""
    checked_state(state)
    if type(inputs) is not SetNoteReleaseDurationInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelDurationCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_set_note_release_duration(state, command, inputs.continuation)
    return SetNoteReleaseDurationResult(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def load_pan_pattern(state: AudioState, inputs: LoadPanPatternInput) -> LoadPanPatternResult:
    """Load pan pattern."""
    checked_state(state)
    if type(inputs) is not LoadPanPatternInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelTransferCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        table_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_load_pan_pattern(state, command, inputs.continuation)
    return LoadPanPatternResult(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def mark_note_continuation(state: AudioState, inputs: MarkNoteContinuationInput) -> MarkNoteContinuationResult:
    """Mark note continuation."""
    checked_state(state)
    if type(inputs) is not MarkNoteContinuationInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelPointerCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        argument_cursor=inputs.parameter_cursor,
        return_stack=inputs.stack_cursor,
    )
    apply_mark_note_continuation(state, command, inputs.continuation)
    return MarkNoteContinuationResult(channel_cursor=command.channel_address, conditions=command.condition_bits, parameter_cursor=command.argument_cursor, stack_cursor=command.return_stack).validate(state)

def set_special_channel_frequency(state: AudioState, inputs: SetSpecialChannelFrequencyInput) -> SetSpecialChannelFrequencyResult:
    """Set special channel frequency."""
    checked_state(state)
    if type(inputs) is not SetSpecialChannelFrequencyInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelTransferCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        table_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_set_special_channel_frequency(state, command, inputs.continuation)
    return SetSpecialChannelFrequencyResult(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def write_timer_control(state: AudioState, inputs: WriteTimerControlInput) -> WriteTimerControlResult:
    """Write timer control."""
    checked_state(state)
    if type(inputs) is not WriteTimerControlInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelTransferCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        table_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_write_timer_control(state, command, inputs.continuation)
    return WriteTimerControlResult(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def select_instrument(state: AudioState, inputs: SelectInstrumentInput) -> SelectInstrumentResult:
    """Select instrument."""
    checked_state(state)
    if type(inputs) is not SelectInstrumentInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelTransferCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        table_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_select_instrument(state, command, inputs.continuation)
    return SelectInstrumentResult(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def select_banked_instrument(state: AudioState, inputs: SelectBankedInstrumentInput) -> SelectBankedInstrumentResult:
    """Select banked instrument."""
    checked_state(state)
    if type(inputs) is not SelectBankedInstrumentInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelTransferCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        table_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_select_banked_instrument(state, command, inputs.continuation)
    return SelectBankedInstrumentResult(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def set_stereo_pan(state: AudioState, inputs: SetStereoPanInput) -> SetStereoPanResult:
    """Set stereo pan."""
    checked_state(state)
    if type(inputs) is not SetStereoPanInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelTransferCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        table_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_set_stereo_pan(state, command, inputs.continuation)
    return SetStereoPanResult(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def set_lfo_and_stereo_pan(state: AudioState, inputs: SetLfoAndStereoPanInput) -> SetLfoAndStereoPanResult:
    """Set lfo and stereo pan."""
    checked_state(state)
    if type(inputs) is not SetLfoAndStereoPanInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelTransferCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        table_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_set_lfo_and_stereo_pan(state, command, inputs.continuation)
    return SetLfoAndStereoPanResult(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.table_cursor, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def adjust_note_transpose(state: AudioState, inputs: AdjustNoteTransposeInput) -> AdjustNoteTransposeResult:
    """Adjust note transpose."""
    checked_state(state)
    if type(inputs) is not AdjustNoteTransposeInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelValueCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_adjust_note_transpose(state, command, inputs.continuation)
    return AdjustNoteTransposeResult(channel_cursor=command.channel_address, conditions=command.condition_bits, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def set_duration_multiplier(state: AudioState, inputs: SetDurationMultiplierInput) -> SetDurationMultiplierResult:
    """Set duration multiplier."""
    checked_state(state)
    if type(inputs) is not SetDurationMultiplierInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelValueCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_set_duration_multiplier(state, command, inputs.continuation)
    return SetDurationMultiplierResult(channel_cursor=command.channel_address, conditions=command.condition_bits, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def set_psg_noise(state: AudioState, inputs: SetPsgNoiseInput) -> SetPsgNoiseResult:
    """Set psg noise."""
    checked_state(state)
    if type(inputs) is not SetPsgNoiseInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelArgumentCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        argument_cursor=inputs.parameter_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_set_psg_noise(state, command, inputs.continuation)
    return SetPsgNoiseResult(channel_cursor=command.channel_address, conditions=command.condition_bits, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def set_psg_envelope(state: AudioState, inputs: SetPsgEnvelopeInput) -> SetPsgEnvelopeResult:
    """Set psg envelope."""
    checked_state(state)
    if type(inputs) is not SetPsgEnvelopeInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelValueCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_set_psg_envelope(state, command, inputs.continuation)
    return SetPsgEnvelopeResult(channel_cursor=command.channel_address, conditions=command.condition_bits, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def set_pitch_envelope(state: AudioState, inputs: SetPitchEnvelopeInput) -> SetPitchEnvelopeResult:
    """Set pitch envelope."""
    checked_state(state)
    if type(inputs) is not SetPitchEnvelopeInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelArgumentCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        argument_cursor=inputs.parameter_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_set_pitch_envelope(state, command, inputs.continuation)
    return SetPitchEnvelopeResult(channel_cursor=command.channel_address, conditions=command.condition_bits, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def store_pitch_envelope(state: AudioState, inputs: StorePitchEnvelopeInput) -> StorePitchEnvelopeResult:
    """Store pitch envelope."""
    checked_state(state)
    if type(inputs) is not StorePitchEnvelopeInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelArgumentCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        argument_cursor=inputs.parameter_cursor,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_store_pitch_envelope(state, command, inputs.continuation)
    return StorePitchEnvelopeResult(channel_cursor=command.channel_address, conditions=command.condition_bits, parameter_cursor=command.argument_cursor, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def jump_sequence_pointer(state: AudioState, inputs: JumpSequencePointerInput) -> JumpSequencePointerResult:
    """Jump sequence pointer."""
    checked_state(state)
    if type(inputs) is not JumpSequencePointerInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = SequenceCommandContext(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        scratch_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    execute_absolute_jump(state, command, inputs.continuation)
    return JumpSequencePointerResult(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.scratch_cursor, parameter_cursor=command.argument_cursor, sample=command.command_byte, stack_cursor=command.return_stack).validate(state)

def set_pitch_slide_mode(state: AudioState, inputs: SetPitchSlideModeInput) -> SetPitchSlideModeResult:
    """Set pitch slide mode."""
    checked_state(state)
    if type(inputs) is not SetPitchSlideModeInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelValueCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_set_pitch_slide_mode(state, command, inputs.continuation)
    return SetPitchSlideModeResult(channel_cursor=command.channel_address, conditions=command.condition_bits, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def set_raw_frequency_mode(state: AudioState, inputs: SetRawFrequencyModeInput) -> SetRawFrequencyModeResult:
    """Set raw frequency mode."""
    checked_state(state)
    if type(inputs) is not SetRawFrequencyModeInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = ChannelValueCommand(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        command_value=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    apply_set_raw_frequency_mode(state, command, inputs.continuation)
    return SetRawFrequencyModeResult(channel_cursor=command.channel_address, conditions=command.condition_bits, sample=command.command_value, stack_cursor=command.return_stack).validate(state)

def call_sequence_subroutine(state: AudioState, inputs: CallSequenceSubroutineInput) -> CallSequenceSubroutineResult:
    """Call sequence subroutine."""
    checked_state(state)
    if type(inputs) is not CallSequenceSubroutineInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = SequenceCommandContext(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        scratch_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    execute_sequence_call(state, command, inputs.continuation)
    return CallSequenceSubroutineResult(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.scratch_cursor, parameter_cursor=command.argument_cursor, sample=command.command_byte, stack_cursor=command.return_stack).validate(state)

def return_sequence_subroutine(state: AudioState, inputs: ReturnSequenceSubroutineInput) -> ReturnSequenceSubroutineResult:
    """Return sequence subroutine."""
    checked_state(state)
    if type(inputs) is not ReturnSequenceSubroutineInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = SequenceReturnContext(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        scratch_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        return_stack=inputs.stack_cursor,
    )
    execute_sequence_return(state, command, inputs.continuation)
    return ReturnSequenceSubroutineResult(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.scratch_cursor, parameter_cursor=command.argument_cursor, stack_cursor=command.return_stack).validate(state)

def repeat_sequence_section(state: AudioState, inputs: RepeatSequenceSectionInput) -> RepeatSequenceSectionResult:
    """Repeat sequence section."""
    checked_state(state)
    if type(inputs) is not RepeatSequenceSectionInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    command = SequenceCommandContext(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        scratch_cursor=inputs.lookup_cursor,
        argument_cursor=inputs.parameter_cursor,
        command_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    execute_sequence_repeat(state, command, inputs.continuation)
    return RepeatSequenceSectionResult(channel_cursor=command.channel_address, conditions=command.condition_bits, count_and_data=command.transfer_word, lookup_cursor=command.scratch_cursor, parameter_cursor=command.argument_cursor, sample=command.command_byte, stack_cursor=command.return_stack).validate(state)
