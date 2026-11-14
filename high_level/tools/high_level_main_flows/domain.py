"""One live state, views and fixed-width compatibility for main workflows.

These are exact aliases to the already established live domain, not a CPU
wrapper or copied state. Additional low RAM names are supported only where
candidate17 original absolute-LONG operands establish the address form.
"""
import re

from ..high_level_dynamic_flows.domain import (
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
    VideoPlaneAddress, StackContinuation, DYNAMIC_ABSOLUTE_LONG_RAM,
)

# confirmed: selection-final01.json absolute_bus_operands, LONG RAM forms.
# A named resource, a video-plane offset and a signed WORD absolute address
# must never be silently rewritten through this low-RAM binding set.
MAIN_ABSOLUTE_LONG_RAM = DYNAMIC_ABSOLUTE_LONG_RAM | frozenset((
    0x0000, 0x3000, 0x3826, 0x382C, 0x3938, 0x39B2,
    0x3BB2, 0x3BB4, 0x3BB6, 0x3BB8, 0x3BC2, 0x3F00,
    0x7000, 0x7008, 0x700C, 0x700E, 0x7014, 0x7016,
    0x7022, 0x7024, 0x7026, 0x7028, 0x702A, 0x702C,
    0x702E, 0x7030, 0x7032, 0x7034, 0x7036, 0x7038,
    0x703A, 0x703E, 0x7040, 0x7042,
))


def ram_view(state: SceneState, name: str) -> Table:
    """Obtain the original logical RAM alias, sharing the exact supplied RAM."""
    checked_state(state)
    if type(name) is not str or re.fullmatch(r'ram_[0-9a-f]{4}', name) is None:
        raise ValueError('explicit ram_xxxx view required')
    low = int(name[4:], 16)
    if low in MAIN_ABSOLUTE_LONG_RAM:
        address = 0x00FF0000 | low
    elif low >= 0x8000:
        address = 0xFFFF0000 | low
    else:
        raise Boundary('unresolved original low-RAM address form')
    return state.table_at(address)


def data_view(state: SceneState, name: str) -> Table:
    """Name an external read-only source location without reading its content.

    The neutral data_xxxxxx ID is an analysis location, not an asset-ownership
    claim. Actual reads must be supplied by ReadOnlyData, with its one-authority
    and boundary checks. No source bytes, media arrays or directory are hidden
    here; pointers read by business rules remain live.
    """
    checked_state(state)
    if type(name) is not str or re.fullmatch(r'data_[0-9a-f]{6}', name) is None:
        raise ValueError('explicit data_xxxxxx source ID required')
    address = int(name[5:], 16)
    if address >= 0xFF0000 or state.hardware.contains(address, 1):
        raise Boundary('read-only source name cannot shadow RAM or hardware')
    return state.table_at(address)
