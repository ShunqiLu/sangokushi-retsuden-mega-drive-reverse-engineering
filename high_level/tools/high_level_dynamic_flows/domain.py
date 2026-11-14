"""One live scene state shared by phase/action rules and earlier logical services.

Explicit type aliases, not a facade around a different runtime or a CPU model.
No ROM, media payload or hidden source loading. New neutral bindings are taken
only from original absolute-LONG RAM operands; video addresses stay separate.
"""
import re
from ..high_level_scene_flows.domain import (
    Boundary,
    uint,
    u8,
    u16,
    u32,
    s8,
    s16,
    low8,
    low16,
    high16,
    replace_byte,
    replace_word,
    swap_words,
    negative_byte,
    negative_word,
    negative_long,
    descending_inclusive,
    divu_retained,
    integer,
    unsigned,
    checked_word,
    checked_long,
    word,
    long,
    byte,
    low_word,
    low_byte,
    signed_word,
    add16,
    sub16,
    add32,
    sub32,
    sub8,
    shl16,
    shl32,
    mask16,
    mask32,
    clear_low_word,
    negate32,
    replace_low_word,
    mulu16,
    divu16,
    stitched_product,
    saturating_add32,
    subtract_borrow32,
    minimum32,
    RandomSample,
    ReadOnlyData,
    HardwareBus,
    SceneServices,
    typed_service_context,
    SceneState,
    Table,
    Cursor,
    checked_state,
    checked_table,
    checked_cursor,
    read_packed_long,
    store_packed_long_reverse,
    VideoPlaneAddress,
    StackContinuation,
    Byte,
    Word,
    Long,
    ABSOLUTE_LONG_RAM,
)

DYNAMIC_ABSOLUTE_LONG_RAM = frozenset(ABSOLUTE_LONG_RAM) | frozenset([28682, 28683, 28684, 28686, 28692, 28694, 28696, 28778, 28780, 28782, 28784, 28858, 28860, 28862, 28864, 28912, 28914, 28915])

def ram_view(state: SceneState, name: str) -> Table:
    """Return a same-state live view at the original logical bus address."""
    checked_state(state)
    if type(name) is not str or re.fullmatch(r'ram_[0-9a-f]{4}', name) is None:
        raise ValueError('explicit ram_xxxx name required')
    low = int(name[4:], 16)
    if low in DYNAMIC_ABSOLUTE_LONG_RAM:
        address = 0x00FF0000 | low
    elif low >= 0x8000:
        address = 0xFFFF0000 | low
    else:
        raise Boundary('unknown original low-RAM address form')
    return state.table(address)
