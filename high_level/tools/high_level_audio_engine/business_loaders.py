"""Structured intermediate audio logic, not a complete CPU/timing proof."""
from .domain import (AudioState, AudioBoundary, Continuation, AlternateGroup,
    Byte, Word, byte, word, checked_state, u8, u16, low, high, replace_low,
    replace_high, logic_conditions, sum_byte, difference_byte,
    comparison_conditions, increment_byte, decrement_byte, sum_word,
    difference_word, tested_bit_conditions, copy_byte_conditions)
from .contexts import (
    DispatchSoundCommandInput, DispatchSoundCommandResult,
    DispatchLoadedSoundCommandInput, DispatchLoadedSoundCommandResult,
    StopPsgPairInput, StopPsgPairResult,
    StageChannelStopContinuationsInput, StageChannelStopContinuationsResult,
    ChooseChannelViewsInput, ChooseChannelViewsResult,
    ClearNoteTailAndInitializeChannelInput, ClearNoteTailAndInitializeChannelResult,
    InitializeChannelRecordInput, InitializeChannelRecordResult,
    InitializeAudioBankInput, InitializeAudioBankResult,
    ProcessDriverStopModeInput, ProcessDriverStopModeResult,
    BeginFadeoutInput, BeginFadeoutResult,
    ClearFadeoutChannelFlagsInput, ClearFadeoutChannelFlagsResult,
    AdvanceFadeoutInput, AdvanceFadeoutResult,
    ClearAndResetDriverInput, ClearAndResetDriverResult,
    ResetTimerControlInput, ResetTimerControlResult,
    ResetVoiceReleaseInput, ResetVoiceReleaseResult,
    SilencePsgChannelsInput, SilencePsgChannelsResult,
    TickNoteDividerInput, TickNoteDividerResult,
    ResetOperatorReleaseInput, ResetOperatorReleaseResult,
    WriteOperatorGroupInput, WriteOperatorGroupResult,
    SetAllChannelActivityInput, SetAllChannelActivityResult,
    StopChannelAfterOperatorResetInput, StopChannelAfterOperatorResetResult,
    StopAndReleaseChannelInput, StopAndReleaseChannelResult,
)

from .contexts_lifecycle import DriverLifecycle, RecordInitialization, BankInitialization, OperatorRelease
from .business_lifecycle_loading import (run_dispatch_sound_command, run_dispatch_loaded_sound_command, run_choose_channel_views, run_clear_note_tail_and_initialize_channel, run_initialize_channel_record, run_initialize_audio_bank)
from .business_lifecycle_stopping import (run_stop_psg_pair, run_stage_channel_stop_continuations, run_process_driver_stop_mode, run_set_all_channel_activity, run_stop_channel_after_operator_reset, run_stop_and_release_channel)
from .business_lifecycle_fade import (run_begin_fadeout, run_clear_fadeout_channel_flags, run_advance_fadeout)
from .business_lifecycle_reset import (run_clear_and_reset_driver, run_reset_timer_control, run_reset_voice_release, run_silence_psg_channels, run_tick_note_divider, run_reset_operator_release, run_write_operator_group)

def dispatch_sound_command(state: AudioState, inputs: DispatchSoundCommandInput) -> DispatchSoundCommandResult:
    """Dispatch sound command."""
    checked_state(state)
    if type(inputs) is not DispatchSoundCommandInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = DriverLifecycle(
        paired_channel_address=inputs.auxiliary_cursor,
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        source_cursor=inputs.lookup_cursor,
        secondary_cursor=inputs.parameter_cursor,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_dispatch_sound_command(state, lifecycle, inputs.continuation)
    return DispatchSoundCommandResult(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def dispatch_loaded_sound_command(state: AudioState, inputs: DispatchLoadedSoundCommandInput) -> DispatchLoadedSoundCommandResult:
    """Dispatch loaded sound command."""
    checked_state(state)
    if type(inputs) is not DispatchLoadedSoundCommandInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = DriverLifecycle(
        paired_channel_address=inputs.auxiliary_cursor,
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        source_cursor=inputs.lookup_cursor,
        secondary_cursor=inputs.parameter_cursor,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_dispatch_loaded_sound_command(state, lifecycle, inputs.continuation)
    return DispatchLoadedSoundCommandResult(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def stop_psg_pair(state: AudioState, inputs: StopPsgPairInput) -> StopPsgPairResult:
    """Stop psg pair."""
    checked_state(state)
    if type(inputs) is not StopPsgPairInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = DriverLifecycle(
        paired_channel_address=inputs.auxiliary_cursor,
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        source_cursor=inputs.lookup_cursor,
        secondary_cursor=inputs.parameter_cursor,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_stop_psg_pair(state, lifecycle, inputs.continuation)
    return StopPsgPairResult(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def stage_channel_stop_continuations(state: AudioState, inputs: StageChannelStopContinuationsInput) -> StageChannelStopContinuationsResult:
    """Stage channel stop continuations."""
    checked_state(state)
    if type(inputs) is not StageChannelStopContinuationsInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = DriverLifecycle(
        paired_channel_address=inputs.auxiliary_cursor,
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        source_cursor=inputs.lookup_cursor,
        secondary_cursor=inputs.parameter_cursor,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_stage_channel_stop_continuations(state, lifecycle, inputs.continuation)
    return StageChannelStopContinuationsResult(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def choose_channel_views(state: AudioState, inputs: ChooseChannelViewsInput) -> ChooseChannelViewsResult:
    """Choose channel views."""
    checked_state(state)
    if type(inputs) is not ChooseChannelViewsInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = DriverLifecycle(
        paired_channel_address=inputs.auxiliary_cursor,
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        source_cursor=inputs.lookup_cursor,
        secondary_cursor=inputs.parameter_cursor,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_choose_channel_views(state, lifecycle, inputs.continuation)
    return ChooseChannelViewsResult(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def clear_note_tail_and_initialize_channel(state: AudioState, inputs: ClearNoteTailAndInitializeChannelInput) -> ClearNoteTailAndInitializeChannelResult:
    """Clear note tail and initialize channel."""
    checked_state(state)
    if type(inputs) is not ClearNoteTailAndInitializeChannelInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = RecordInitialization(
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        source_cursor=inputs.lookup_cursor,
        secondary_cursor=inputs.parameter_cursor,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_clear_note_tail_and_initialize_channel(state, lifecycle, inputs.continuation)
    return ClearNoteTailAndInitializeChannelResult(conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def initialize_channel_record(state: AudioState, inputs: InitializeChannelRecordInput) -> InitializeChannelRecordResult:
    """Initialize channel record."""
    checked_state(state)
    if type(inputs) is not InitializeChannelRecordInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = RecordInitialization(
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        source_cursor=inputs.lookup_cursor,
        secondary_cursor=inputs.parameter_cursor,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_initialize_channel_record(state, lifecycle, inputs.continuation)
    return InitializeChannelRecordResult(conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def initialize_audio_bank(state: AudioState, inputs: InitializeAudioBankInput) -> InitializeAudioBankResult:
    """Initialize audio bank."""
    checked_state(state)
    if type(inputs) is not InitializeAudioBankInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = BankInitialization(
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_initialize_audio_bank(state, lifecycle, inputs.continuation)
    return InitializeAudioBankResult(conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def process_driver_stop_mode(state: AudioState, inputs: ProcessDriverStopModeInput) -> ProcessDriverStopModeResult:
    """Process driver stop mode."""
    checked_state(state)
    if type(inputs) is not ProcessDriverStopModeInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = DriverLifecycle(
        paired_channel_address=inputs.auxiliary_cursor,
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        source_cursor=inputs.lookup_cursor,
        secondary_cursor=inputs.parameter_cursor,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_process_driver_stop_mode(state, lifecycle, inputs.continuation)
    return ProcessDriverStopModeResult(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def begin_fadeout(state: AudioState, inputs: BeginFadeoutInput) -> BeginFadeoutResult:
    """Begin fadeout."""
    checked_state(state)
    if type(inputs) is not BeginFadeoutInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = DriverLifecycle(
        paired_channel_address=inputs.auxiliary_cursor,
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        source_cursor=inputs.lookup_cursor,
        secondary_cursor=inputs.parameter_cursor,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_begin_fadeout(state, lifecycle, inputs.continuation)
    return BeginFadeoutResult(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def clear_fadeout_channel_flags(state: AudioState, inputs: ClearFadeoutChannelFlagsInput) -> ClearFadeoutChannelFlagsResult:
    """Clear fadeout channel flags."""
    checked_state(state)
    if type(inputs) is not ClearFadeoutChannelFlagsInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = DriverLifecycle(
        paired_channel_address=inputs.auxiliary_cursor,
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        source_cursor=inputs.lookup_cursor,
        secondary_cursor=inputs.parameter_cursor,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_clear_fadeout_channel_flags(state, lifecycle, inputs.continuation)
    return ClearFadeoutChannelFlagsResult(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def advance_fadeout(state: AudioState, inputs: AdvanceFadeoutInput) -> AdvanceFadeoutResult:
    """Advance fadeout."""
    checked_state(state)
    if type(inputs) is not AdvanceFadeoutInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = DriverLifecycle(
        paired_channel_address=inputs.auxiliary_cursor,
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        source_cursor=inputs.lookup_cursor,
        secondary_cursor=inputs.parameter_cursor,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_advance_fadeout(state, lifecycle, inputs.continuation)
    return AdvanceFadeoutResult(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def clear_and_reset_driver(state: AudioState, inputs: ClearAndResetDriverInput) -> ClearAndResetDriverResult:
    """Clear and reset driver."""
    checked_state(state)
    if type(inputs) is not ClearAndResetDriverInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = DriverLifecycle(
        paired_channel_address=inputs.auxiliary_cursor,
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        source_cursor=inputs.lookup_cursor,
        secondary_cursor=inputs.parameter_cursor,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_clear_and_reset_driver(state, lifecycle, inputs.continuation)
    return ClearAndResetDriverResult(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def reset_timer_control(state: AudioState, inputs: ResetTimerControlInput) -> ResetTimerControlResult:
    """Reset timer control."""
    checked_state(state)
    if type(inputs) is not ResetTimerControlInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = DriverLifecycle(
        paired_channel_address=inputs.auxiliary_cursor,
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        source_cursor=inputs.lookup_cursor,
        secondary_cursor=inputs.parameter_cursor,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_reset_timer_control(state, lifecycle, inputs.continuation)
    return ResetTimerControlResult(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def reset_voice_release(state: AudioState, inputs: ResetVoiceReleaseInput) -> ResetVoiceReleaseResult:
    """Reset voice release."""
    checked_state(state)
    if type(inputs) is not ResetVoiceReleaseInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = OperatorRelease(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_reset_voice_release(state, lifecycle, inputs.continuation)
    return ResetVoiceReleaseResult(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def silence_psg_channels(state: AudioState, inputs: SilencePsgChannelsInput) -> SilencePsgChannelsResult:
    """Silence psg channels."""
    checked_state(state)
    if type(inputs) is not SilencePsgChannelsInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = DriverLifecycle(
        paired_channel_address=inputs.auxiliary_cursor,
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        source_cursor=inputs.lookup_cursor,
        secondary_cursor=inputs.parameter_cursor,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_silence_psg_channels(state, lifecycle, inputs.continuation)
    return SilencePsgChannelsResult(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def tick_note_divider(state: AudioState, inputs: TickNoteDividerInput) -> TickNoteDividerResult:
    """Tick note divider."""
    checked_state(state)
    if type(inputs) is not TickNoteDividerInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = RecordInitialization(
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        source_cursor=inputs.lookup_cursor,
        secondary_cursor=inputs.parameter_cursor,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_tick_note_divider(state, lifecycle, inputs.continuation)
    return TickNoteDividerResult(conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def reset_operator_release(state: AudioState, inputs: ResetOperatorReleaseInput) -> ResetOperatorReleaseResult:
    """Reset operator release."""
    checked_state(state)
    if type(inputs) is not ResetOperatorReleaseInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = OperatorRelease(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_reset_operator_release(state, lifecycle, inputs.continuation)
    return ResetOperatorReleaseResult(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def write_operator_group(state: AudioState, inputs: WriteOperatorGroupInput) -> WriteOperatorGroupResult:
    """Write operator group."""
    checked_state(state)
    if type(inputs) is not WriteOperatorGroupInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = OperatorRelease(
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_write_operator_group(state, lifecycle, inputs.continuation)
    return WriteOperatorGroupResult(channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def set_all_channel_activity(state: AudioState, inputs: SetAllChannelActivityInput) -> SetAllChannelActivityResult:
    """Set all channel activity."""
    checked_state(state)
    if type(inputs) is not SetAllChannelActivityInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = DriverLifecycle(
        paired_channel_address=inputs.auxiliary_cursor,
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        source_cursor=inputs.lookup_cursor,
        secondary_cursor=inputs.parameter_cursor,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_set_all_channel_activity(state, lifecycle, inputs.continuation)
    return SetAllChannelActivityResult(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def stop_channel_after_operator_reset(state: AudioState, inputs: StopChannelAfterOperatorResetInput) -> StopChannelAfterOperatorResetResult:
    """Stop channel after operator reset."""
    checked_state(state)
    if type(inputs) is not StopChannelAfterOperatorResetInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = DriverLifecycle(
        paired_channel_address=inputs.auxiliary_cursor,
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        source_cursor=inputs.lookup_cursor,
        secondary_cursor=inputs.parameter_cursor,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_stop_channel_after_operator_reset(state, lifecycle, inputs.continuation)
    return StopChannelAfterOperatorResetResult(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)

def stop_and_release_channel(state: AudioState, inputs: StopAndReleaseChannelInput) -> StopAndReleaseChannelResult:
    """Stop and release channel."""
    checked_state(state)
    if type(inputs) is not StopAndReleaseChannelInput:
        raise ValueError("function-specific immutable input required")
    inputs.validate(state)
    lifecycle = DriverLifecycle(
        paired_channel_address=inputs.auxiliary_cursor,
        channel_address=inputs.channel_cursor,
        condition_bits=inputs.conditions,
        transfer_word=inputs.count_and_data,
        source_cursor=inputs.lookup_cursor,
        secondary_cursor=inputs.parameter_cursor,
        working_byte=inputs.sample,
        return_stack=inputs.stack_cursor,
    )
    run_stop_and_release_channel(state, lifecycle, inputs.continuation)
    return StopAndReleaseChannelResult(auxiliary_cursor=lifecycle.paired_channel_address, channel_cursor=lifecycle.channel_address, conditions=lifecycle.condition_bits, count_and_data=lifecycle.transfer_word, lookup_cursor=lifecycle.source_cursor, parameter_cursor=lifecycle.secondary_cursor, sample=lifecycle.working_byte, stack_cursor=lifecycle.return_stack).validate(state)
