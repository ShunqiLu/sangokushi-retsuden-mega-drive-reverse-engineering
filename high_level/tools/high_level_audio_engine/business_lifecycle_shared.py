"""Actual lifecycle algorithms with ordered live bus effects, fixed-width contexts and original stack/service boundaries. No original byte payload or saved-body fallback."""
from .domain import AudioState, AudioBoundary, Continuation, AlternateGroup, Byte, Word, byte, word, checked_state, u8, u16, low, high, replace_low, replace_high, logic_conditions, sum_byte, difference_byte, comparison_conditions, increment_byte, decrement_byte, sum_word, difference_word, tested_bit_conditions, copy_byte_conditions
from .contexts_lifecycle import DriverLifecycle

def finish_sound_command(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Store the original command-latch acknowledgement BYTE and consume its actual continuation; no synthetic success return."""
    lifecycle.working_byte = u8(128)
    state.write(7177, u8(lifecycle.working_byte))
    lifecycle.return_stack = state.consume_return(lifecycle.return_stack, continuation)
    return

def copy_live_byte(state: AudioState, lifecycle: DriverLifecycle, continuation: Continuation) -> None:
    """Read one live source byte, write it to the live secondary cursor, advance both WORD cursors and count, then update original copy conditions."""
    copied_byte = state.read(lifecycle.source_cursor)
    state.write(lifecycle.secondary_cursor, copied_byte)
    lifecycle.source_cursor = u16(lifecycle.source_cursor + 1)
    lifecycle.secondary_cursor = u16(lifecycle.secondary_cursor + 1)
    lifecycle.transfer_word = u16(lifecycle.transfer_word - 1)
    lifecycle.condition_bits = copy_byte_conditions(lifecycle.working_byte, copied_byte, lifecycle.transfer_word, lifecycle.condition_bits)
