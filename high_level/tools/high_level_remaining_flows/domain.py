"""One live game-state authority for the remaining logical source families.

Exact aliases reuse established RAM, external read-only data, hardware and
fixed-width rules. There is no copied memory or simulated register dictionary.
Unknown bus/address forms remain explicit boundaries rather than fabricated
values. This compatibility layer is intermediate; it is not final packaging.
"""
from ..high_level_main_flows.domain import (
    Boundary, Byte, Word, Long, uint, u8, u16, u32, s8, s16,
    low8, low16, high16, replace_byte, replace_word, swap_words,
    negative_byte, negative_word, negative_long, descending_inclusive,
    divu_retained, integer, unsigned, checked_word, checked_long,
    word, long, byte, low_word, low_byte, signed_word,
    add16, sub16, add32, sub32, sub8, shl16, shl32, mask16, mask32,
    clear_low_word, negate32, replace_low_word, mulu16, divu16,
    stitched_product, saturating_add32, subtract_borrow32, minimum32,
    RandomSample, ReadOnlyData, HardwareBus, SceneServices,
    typed_service_context, SceneState, Table, Cursor,
    checked_state, checked_table, checked_cursor,
    read_packed_long, store_packed_long_reverse,
    VideoPlaneAddress, StackContinuation, ram_view, data_view,
)
