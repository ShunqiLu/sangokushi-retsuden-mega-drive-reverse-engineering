"""Function-specific immutable audio inputs/results; no CPU register dictionary."""
from dataclasses import dataclass
from .domain import (AudioState, AudioBoundary, Continuation, AlternateGroup,
    Byte, Word, byte, word, checked_state, u8, u16, low, high, replace_low,
    replace_high, logic_conditions, sum_byte, difference_byte,
    comparison_conditions, increment_byte, decrement_byte, sum_word,
    difference_word, tested_bit_conditions, copy_byte_conditions)
@dataclass(frozen=True)
class InitializeAudioDriverInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class InitializeAudioDriverResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class WaitFmReadyInput:
    conditions: Byte
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class WaitFmReadyResult:
    conditions: Byte
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class WriteChannelFmRegisterInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class WriteChannelFmRegisterResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class WriteFmPortZeroEntryInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class WriteFmPortZeroEntryResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class LookupBankedRootPointerInput:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class LookupBankedRootPointerResult:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class LookupPointerAfterRootInput:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class LookupPointerAfterRootResult:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class IndexWordPointerInput:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class IndexWordPointerResult:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ReadStreamWordInput:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ReadStreamWordResult:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ServiceIm1InterruptInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ServiceIm1InterruptResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ProgramTimerAInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ProgramTimerAResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ProgramTimerBInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ProgramTimerBResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class UpdateAudioDriverInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class UpdateAudioDriverResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class UpdateSfxChannelGroupsInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class UpdateSfxChannelGroupsResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class UpdateChannelGroupInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class UpdateChannelGroupResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class UpdateFmChannelInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class UpdateFmChannelResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class WriteChannelFrequencyInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class WriteChannelFrequencyResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ChooseFrequencyScratchBlockInput:
    conditions: Byte
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ChooseFrequencyScratchBlockResult:
    conditions: Byte
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ReadNoteOrDurationInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ReadNoteOrDurationResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class MultiplyNoteDurationInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class MultiplyNoteDurationResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class UpdatePanPatternInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class UpdatePanPatternResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ResumePanPatternInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ResumePanPatternResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class DecrementNoteCountdownInput:
    channel_cursor: Word
    conditions: Byte
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class DecrementNoteCountdownResult:
    channel_cursor: Word
    conditions: Byte
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class UpdateVoiceEnvelopeInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class UpdateVoiceEnvelopeResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class InitializePitchModulationInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class InitializePitchModulationResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class UpdatePitchModulationInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class UpdatePitchModulationResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SendKeyOffInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SendKeyOffResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SendKeyOffAfterGateInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SendKeyOffAfterGateResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class CalculateChannelPitchInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class CalculateChannelPitchResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ReadIndexedEnvelopeInput:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ReadIndexedEnvelopeResult:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class LookupInstrumentInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class LookupInstrumentResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class OffsetInstrumentInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class OffsetInstrumentResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class WriteFmPortOneInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class WriteFmPortOneResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class LoadInstrumentInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class LoadInstrumentResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class WriteNextInstrumentFieldInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class WriteNextInstrumentFieldResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class DispatchSoundCommandInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class DispatchSoundCommandResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class DispatchLoadedSoundCommandInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class DispatchLoadedSoundCommandResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class StopPsgPairInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class StopPsgPairResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class StageChannelStopContinuationsInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class StageChannelStopContinuationsResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ChooseChannelViewsInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ChooseChannelViewsResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ClearNoteTailAndInitializeChannelInput:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ClearNoteTailAndInitializeChannelResult:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class InitializeChannelRecordInput:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class InitializeChannelRecordResult:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class InitializeAudioBankInput:
    conditions: Byte
    count_and_data: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class InitializeAudioBankResult:
    conditions: Byte
    count_and_data: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ProcessDriverStopModeInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ProcessDriverStopModeResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class BeginFadeoutInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class BeginFadeoutResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ClearFadeoutChannelFlagsInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ClearFadeoutChannelFlagsResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class AdvanceFadeoutInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class AdvanceFadeoutResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ClearAndResetDriverInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ClearAndResetDriverResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ResetTimerControlInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ResetTimerControlResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ResetVoiceReleaseInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ResetVoiceReleaseResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SilencePsgChannelsInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SilencePsgChannelsResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class TickNoteDividerInput:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class TickNoteDividerResult:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class PollCommandMailboxesInput:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class PollCommandMailboxesResult:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ArbitrateCommandSlotInput:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ArbitrateCommandSlotResult:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ResetVoiceOperatorsInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ResetVoiceOperatorsResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ResetOperatorReleaseInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ResetOperatorReleaseResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class WriteOperatorGroupInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class WriteOperatorGroupResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class UpdateRhythmCountdownInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class UpdateRhythmCountdownResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ReadRhythmNoteInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ReadRhythmNoteResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ResumeRhythmParameterStreamInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ResumeRhythmParameterStreamResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ResumeNoteParameterStreamInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ResumeNoteParameterStreamResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class DispatchExtendedSequenceCommandInput:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class DispatchExtendedSequenceCommandResult:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class StoreFmParametersInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class StoreFmParametersResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class WriteFmParametersInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class WriteFmParametersResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SetAllDurationMultipliersInput:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SetAllDurationMultipliersResult:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SetDriverModeInput:
    conditions: Byte
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SetDriverModeResult:
    conditions: Byte
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class LoadTimerReloadsInput:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class LoadTimerReloadsResult:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class AdjustTimerReloadsInput:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class AdjustTimerReloadsResult:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class DispatchPreservingChannelInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class DispatchPreservingChannelResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SetAllChannelActivityInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SetAllChannelActivityResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class CopySequenceBlockInput:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class CopySequenceBlockResult:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SetPitchOffsetInput:
    channel_cursor: Word
    conditions: Byte
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SetPitchOffsetResult:
    channel_cursor: Word
    conditions: Byte
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SetVoiceEnvelopeInput:
    channel_cursor: Word
    conditions: Byte
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SetVoiceEnvelopeResult:
    channel_cursor: Word
    conditions: Byte
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class AdjustNoteDividerInput:
    conditions: Byte
    lookup_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.lookup_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class AdjustNoteDividerResult:
    conditions: Byte
    lookup_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.lookup_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SetMiscDriverFieldInput:
    conditions: Byte
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SetMiscDriverFieldResult:
    conditions: Byte
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class AdjustPsgVolumeInput:
    channel_cursor: Word
    conditions: Byte
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class AdjustPsgVolumeResult:
    channel_cursor: Word
    conditions: Byte
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class WriteSequenceChannelRegisterInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class WriteSequenceChannelRegisterResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class WriteSequencePortZeroRegisterInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class WriteSequencePortZeroRegisterResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ReadRegisterParameterPairInput:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ReadRegisterParameterPairResult:
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SetPitchModulationInput:
    channel_cursor: Word
    conditions: Byte
    parameter_cursor: Word
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.parameter_cursor)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SetPitchModulationResult:
    channel_cursor: Word
    conditions: Byte
    parameter_cursor: Word
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.parameter_cursor)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class StopChannelAfterOperatorResetInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class StopChannelAfterOperatorResetResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SetNoteReleaseDurationInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SetNoteReleaseDurationResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class LoadPanPatternInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class LoadPanPatternResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class MarkNoteContinuationInput:
    channel_cursor: Word
    conditions: Byte
    parameter_cursor: Word
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.parameter_cursor)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class MarkNoteContinuationResult:
    channel_cursor: Word
    conditions: Byte
    parameter_cursor: Word
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.parameter_cursor)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SetSpecialChannelFrequencyInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SetSpecialChannelFrequencyResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class WriteTimerControlInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class WriteTimerControlResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SelectInstrumentInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SelectInstrumentResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SelectBankedInstrumentInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SelectBankedInstrumentResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SetStereoPanInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SetStereoPanResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SetLfoAndStereoPanInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SetLfoAndStereoPanResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class RefreshInstrumentVolumeInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class RefreshInstrumentVolumeResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class AdjustChannelVolumeInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class AdjustChannelVolumeResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class AdjustFmChannelVolumeInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class AdjustFmChannelVolumeResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class AdjustNoteTransposeInput:
    channel_cursor: Word
    conditions: Byte
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class AdjustNoteTransposeResult:
    channel_cursor: Word
    conditions: Byte
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SetDurationMultiplierInput:
    channel_cursor: Word
    conditions: Byte
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SetDurationMultiplierResult:
    channel_cursor: Word
    conditions: Byte
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SetPsgNoiseInput:
    channel_cursor: Word
    conditions: Byte
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SetPsgNoiseResult:
    channel_cursor: Word
    conditions: Byte
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SetPsgEnvelopeInput:
    channel_cursor: Word
    conditions: Byte
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SetPsgEnvelopeResult:
    channel_cursor: Word
    conditions: Byte
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SetPitchEnvelopeInput:
    channel_cursor: Word
    conditions: Byte
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SetPitchEnvelopeResult:
    channel_cursor: Word
    conditions: Byte
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class StorePitchEnvelopeInput:
    channel_cursor: Word
    conditions: Byte
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class StorePitchEnvelopeResult:
    channel_cursor: Word
    conditions: Byte
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class JumpSequencePointerInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class JumpSequencePointerResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SetPitchSlideModeInput:
    channel_cursor: Word
    conditions: Byte
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SetPitchSlideModeResult:
    channel_cursor: Word
    conditions: Byte
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SetRawFrequencyModeInput:
    channel_cursor: Word
    conditions: Byte
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SetRawFrequencyModeResult:
    channel_cursor: Word
    conditions: Byte
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class StopAndReleaseChannelInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class StopAndReleaseChannelResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class CallSequenceSubroutineInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class CallSequenceSubroutineResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class ReturnSequenceSubroutineInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class ReturnSequenceSubroutineResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class RepeatSequenceSectionInput:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class RepeatSequenceSectionResult:
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class EvaluateEnvelopeStepInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class EvaluateEnvelopeStepResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class StopChannelNoteInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class StopChannelNoteResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class SilenceOldPsgChannelInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class SilenceOldPsgChannelResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self

@dataclass(frozen=True)
class InitializeAudioWorkspaceInput:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word
    continuation: Continuation

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        if type(self.continuation) is not Continuation:
            raise ValueError("explicit continuation required")
        self.continuation.validate()
        return self

@dataclass(frozen=True)
class InitializeAudioWorkspaceResult:
    auxiliary_cursor: Word
    channel_cursor: Word
    conditions: Byte
    count_and_data: Word
    lookup_cursor: Word
    parameter_cursor: Word
    sample: Byte
    stack_cursor: Word

    def validate(self, state):
        checked_state(state)
        word(self.auxiliary_cursor)
        word(self.channel_cursor)
        byte(self.conditions)
        word(self.count_and_data)
        word(self.lookup_cursor)
        word(self.parameter_cursor)
        byte(self.sample)
        word(self.stack_cursor)
        return self
