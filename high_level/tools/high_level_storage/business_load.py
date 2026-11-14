"""Full original save validation, live restore and post-load normalization.

Restore is intentionally nontransactional. Lossy positions and sentinels are
expanded only at their original points. The stream source stays on the real
cartridge odd-BYTE lane; no decoded fixture or host snapshot supplies values.
"""
from .domain import StorageState, Long, low16, s16
from .contexts_storage_fields import (
    StorageFrame, storage_entry, storage_move, storage_address,
    storage_address_step, storage_read_next, storage_write, storage_write_next,
    storage_logic, storage_arithmetic, storage_shift, storage_multiply,
    storage_divide, storage_dbra, storage_call, storage_replace,
    storage_clear_memory,
)
from .business_streams import (
    validate_saved_header_and_checksum_frame_fields, read_masked_fixed_count_frame_fields,
    read_packed_transport_orders_frame_fields, read_packed_group_stream_frame_fields,
)
from .contexts_load import RestoreOutcome
from .domain import Byte, Cursor, Boundary, checked_cursor
from .contexts_storage_fields import storage_legacy_entry


def _read_saved_column_fields(state: StorageState, frame: StorageFrame,
                              column: tuple) -> StorageFrame:
    destination, field_bits, stride, count, continuation = column
    frame = storage_address(frame, 'a1', destination)
    frame = storage_move(state, frame, 'd0', field_bits, 16)
    frame = storage_move(state, frame, 'd1', stride, 16)
    frame = storage_move(state, frame, 'd2', count, 16)
    return storage_call(state, frame, read_masked_fixed_count_frame_fields, continuation)


def _read_saved_columns_fields(state: StorageState, frame: StorageFrame,
                               columns: tuple) -> StorageFrame:
    for column in columns:
        frame = _read_saved_column_fields(state, frame, column)
    return frame


def restore_saved_game_state_frame_fields(state: StorageState,
                                          frame: StorageFrame) -> StorageFrame:
    """8A60..8EEA: validate then restore all live membership/ledger/order data.

    This complete 1,162-byte owner includes both actual RTS exits. Failed
    validation returns the real carry and checksum-clobbered frame; it does
    not pretend a successful load or read any later payload field.
    """
    frame = storage_entry(state, frame)
    frame = storage_call(state, frame, validate_saved_header_and_checksum_frame_fields, 0x8A64)
    if frame.status_word & 1:
        return frame
    for source, clear_address, destination in (
            (0x200115,0xFFFFF67A,0xFFFFF67B),(0x200117,0xFFFFF67C,0xFFFFF67D),
            (0x200119,0xFFFFF67E,0xFFFFF67F),(0x20011B,None,0xFFFFF374),
            (0x20011D,None,0xFFFFF375),(0x20011F,0xFFFFEFD2,0xFFFFEFD3),
            (0x200121,0xFFFFEFE4,0xFFFFEFE5),(0x200123,0xFFFFEFD6,0xFFFFEFD7),
            (0x200125,0xFFFFEFD8,0xFFFFEFD9)):
        if clear_address is not None:
            frame = storage_clear_memory(state, frame, clear_address, 2)
        frame = storage_write(state, frame, destination, 1, state.read(source, 1))
    frame = storage_address(frame, 'a0', 0x200127)
    frame = _read_saved_column_fields(state, frame, (0xFFFFA000,5,1,40,0x8AE6))
    frame = storage_address(frame, 'a1', 0xFFFFEFAA)
    for _ in range(5):
        frame, value = storage_read_next(state, frame, 'a0', 1)
        frame = storage_write_next(state, frame, 'a1', 1, value)
        frame = storage_address_step(frame, 'a0', 1)
    frame = _read_saved_columns_fields(state, frame, (
        (0xFFFFA028,8,1,40,0x8B1C),(0xFFFFA050,8,1,256,0x8B30),
        (0xFFFFD300,8,2,256,0x8B44),(0xFFFFD500,9,2,256,0x8B58)))
    frame = storage_call(state, frame, restore_saved_officer_positions_frame_fields, 0x8B5C)
    frame = _read_saved_columns_fields(state, frame, (
        (0xFFFFB200,8,2,256,0x8B70),(0xFFFFB400,8,2,256,0x8B84),
        (0xFFFFB600,8,2,256,0x8B98),(0xFFFFD300,5,2,256,0x8BAC)))
    frame = storage_call(state, frame, restore_scaled_officer_parameter_words_frame_fields, 0x8BB0)
    frame = _read_saved_columns_fields(state, frame, (
        (0xFFFFC000,10,2,256,0x8BC4),(0xFFFFBE00,10,2,256,0x8BD8),
        (0xFFFFC200,7,1,256,0x8BEC),(0xFFFFC300,7,1,256,0x8C00),
        (0xFFFFC400,5,1,256,0x8C14),(0xFFFFC500,7,1,256,0x8C28),
        (0xFFFFC700,5,1,256,0x8C3C),(0xFFFFC800,14,4,256,0x8C50),
        (0xFFFFCC00,8,1,256,0x8C64)))
    frame = _read_saved_columns_fields(state, frame, (
        (0xFFFFE000,20,4,40,0x8C78),(0xFFFFE0A0,20,4,40,0x8C8C),
        (0xFFFFE140,10,4,40,0x8CA0),(0xFFFFE1E0,10,4,40,0x8CB4),
        (0xFFFFE280,7,4,40,0x8CC8),(0xFFFFE320,7,4,40,0x8CDC),
        (0xFFFFE3C0,7,4,40,0x8CF0),(0xFFFFE5A0,7,4,40,0x8D04),
        (0xFFFFF428,4,1,40,0x8D18)))
    frame = storage_call(state, frame, normalize_saved_city_owner_sentinels_frame_fields, 0x8D1C)
    frame = _read_saved_column_fields(state, frame, (0xFFFFE640,9,2,16,0x8D30))
    frame = storage_call(state, frame, normalize_saved_force_head_sentinels_frame_fields, 0x8D34)
    frame = _read_saved_column_fields(state, frame, (0xFFFFF460,9,2,40,0x8D48))
    frame = storage_call(state, frame, normalize_saved_city_head_sentinels_frame_fields, 0x8D4C)
    frame = _read_saved_column_fields(state, frame, (0xFFFFE660,20,4,40,0x8D60))
    for destination in (0xFFFFE700,0xFFFFE701):
        frame, value = storage_read_next(state, frame, 'a0', 1)
        frame = storage_write(state, frame, destination, 1, value)
        frame = storage_address_step(frame, 'a0', 1)
    frame = storage_address(frame, 'a1', 0xFFFFE710)
    frame = storage_move(state, frame, 'd2', 31, 16)
    while True:
        frame, value = storage_read_next(state, frame, 'a0', 1)
        frame = storage_write_next(state, frame, 'a1', 1, value)
        frame = storage_address_step(frame, 'a0', 1)
        frame, again = storage_dbra(frame, 'd2')
        if not again:
            break
    frame = _read_saved_columns_fields(state, frame, (
        (0xFFFFE778,17,4,40,0x8D96),(0xFFFFD300,9,2,40,0x8DAA),
        (0xFFFFD350,14,2,40,0x8DBE),(0xFFFFD3A0,9,2,40,0x8DD2),
        (0xFFFFD3F0,7,2,40,0x8DE6),(0xFFFFD440,9,2,40,0x8DFA),
        (0xFFFFD490,10,2,40,0x8E0E)))
    frame = storage_call(state, frame, restore_city_orders_and_action_flags_frame_fields, 0x8E12)
    frame = _read_saved_columns_fields(state, frame, (
        (0xFFFFD300,6,1,16,0x8E26),(0xFFFFD310,6,1,16,0x8E3A),
        (0xFFFFD320,8,1,16,0x8E4E),(0xFFFFD330,4,1,16,0x8E62)))
    frame = storage_address(frame, 'a1', 0xFFFFE9F8)
    frame = storage_call(state, frame, restore_saved_force_record_columns_frame_fields, 0x8E6A)
    frame = _read_saved_columns_fields(state, frame, (
        (0xFFFFEA38,1,1,40,0x8E7E),(0xFFFFEA88,2,1,768,0x8E92),
        (0xFFFFED88,18,4,40,0x8EA6),(0xFFFFEE28,20,4,40,0x8EBA),
        (0xFFFFF590,2,1,16,0x8ECE)))
    frame = storage_call(state, frame, read_packed_transport_orders_frame_fields, 0x8ED2)
    frame = storage_call(state, frame, read_packed_group_stream_frame_fields, 0x8ED6)
    frame = storage_write(state, frame, 0x00FF3000, 2, 0xFFFF)
    frame = storage_clear_memory(state, frame, 0xFFFFF776, 2)
    value = state.read(0xFFFFAFFE, 2)
    original_d0 = frame.d0
    frame = storage_replace(frame, d0=(frame.d0 & 0xFFFF0000) | value)
    frame = storage_arithmetic(state, frame, 'd0', 1, 16)
    state.write(0xFFFFAFFE, 2, low16(frame.d0))
    return storage_replace(frame, d0=original_d0)


def restore_saved_officer_positions_frame_fields(state: StorageState,
                                                frame: StorageFrame) -> StorageFrame:
    """8EEA: restore 256 lossy coordinate pairs without a new range clamp."""
    frame = storage_entry(state, frame)
    frame = storage_address(frame, 'a2', 0xFFFFA150)
    frame = storage_address(frame, 'a3', 0xFFFFD300)
    frame = storage_address(frame, 'a4', 0xFFFFD500)
    frame = storage_move(state, frame, 'd0', 255, 16)
    while True:
        for source in ('a3','a4'):
            frame, value = storage_read_next(state, frame, source, 2)
            frame = storage_move(state, frame, 'd1', value, 16)
            frame = storage_shift(state, frame, 'd1', 7, 16)
            frame = storage_write_next(state, frame, 'a2', 2, frame.d1)
        frame, again = storage_dbra(frame, 'd0')
        if not again:
            return frame


def _restore_city_order_word_fields(state: StorageState, frame: StorageFrame,
                                    displacement: int, sentinel: int,
                                    assignment: int) -> StorageFrame:
    value = state.read(frame.a1+displacement, 2)
    frame = storage_move(state, frame, 'd1', value, 16)
    frame = storage_arithmetic(state, frame, 'd1', sentinel, 16, True, True)
    if frame.status_word & 4:
        frame = storage_move(state, frame, 'd1', 0xFFFF, 16)
    elif assignment:
        frame = storage_write(state, frame, frame.a3+s16(low16(frame.d1)), 1, assignment)
    return storage_write_next(state, frame, 'a2', 2, frame.d1)


def restore_city_orders_and_action_flags_frame_fields(state: StorageState,
                                                    frame: StorageFrame) -> StorageFrame:
    """8F0C: expand six scratch WORDs per city and mark actual CD00 indices."""
    frame = storage_entry(state, frame)
    frame = storage_address(frame, 'a1', 0xFFFFD300)
    frame = storage_address(frame, 'a2', 0xFFFFE818)
    frame = storage_address(frame, 'a3', 0xFFFFCD00)
    frame = storage_move(state, frame, 'd0', 39, 16)
    while True:
        for displacement, sentinel, assignment in ((0,0x1FF,2),(0x50,0x3FFF,0),
                                                    (0xA0,0x1FF,3)):
            frame = _restore_city_order_word_fields(state, frame, displacement, sentinel, assignment)
        frame = storage_move(state, frame, 'd1', state.read(frame.a1+0xF0, 2), 16)
        frame = storage_arithmetic(state, frame, 'd1', 0x7F, 16, True, True)
        if frame.status_word & 4:
            frame = storage_move(state, frame, 'd1', 0xFFFF, 16)
        else:
            frame = storage_multiply(state, frame, 'd1', 100)
        frame = storage_write_next(state, frame, 'a2', 2, frame.d1)
        for displacement, sentinel, assignment in ((0x140,0x1FF,4),(0x190,0x3FF,0)):
            frame = _restore_city_order_word_fields(state, frame, displacement, sentinel, assignment)
        frame = storage_address_step(frame, 'a1', 2)
        frame, again = storage_dbra(frame, 'd0')
        if not again:
            return frame


def restore_scaled_officer_parameter_words_frame_fields(state: StorageState,
                                                       frame: StorageFrame) -> StorageFrame:
    """901C: expand the live quantized WORDs with original unsigned MULU five."""
    frame = storage_entry(state, frame)
    frame = storage_address(frame, 'a1', 0xFFFFD300)
    frame = storage_address(frame, 'a2', 0xFFFFB800)
    frame = storage_move(state, frame, 'd0', 255, 16)
    while True:
        frame, value = storage_read_next(state, frame, 'a1', 2)
        frame = storage_move(state, frame, 'd1', value, 16)
        frame = storage_multiply(state, frame, 'd1', 5)
        frame = storage_write_next(state, frame, 'a2', 2, frame.d1)
        frame, again = storage_dbra(frame, 'd0')
        if not again:
            return frame


def _normalize_saved_sentinels_fields(state: StorageState, frame: StorageFrame,
                                      address: Long, counter: int,
                                      bits: int, sentinel: int) -> StorageFrame:
    frame = storage_address(frame, 'a1', address)
    frame = storage_move(state, frame, 'd0', counter, 16)
    while True:
        frame = storage_move(state, frame, 'd1', state.read(frame.a1, bits//8), bits)
        frame = storage_arithmetic(state, frame, 'd1', sentinel, bits, True, True)
        if frame.status_word & 4:
            frame = storage_move(state, frame, 'd1', (1 << bits)-1, bits)
        frame = storage_write_next(state, frame, 'a1', bits//8, frame.d1)
        frame, again = storage_dbra(frame, 'd0')
        if not again:
            return frame


def normalize_saved_force_head_sentinels_frame_fields(state: StorageState,
                                                      frame: StorageFrame) -> StorageFrame:
    return _normalize_saved_sentinels_fields(state, storage_entry(state, frame),
        0xFFFFE640, 15, 16, 0x1FF)


def normalize_saved_city_head_sentinels_frame_fields(state: StorageState,
                                                     frame: StorageFrame) -> StorageFrame:
    return _normalize_saved_sentinels_fields(state, storage_entry(state, frame),
        0xFFFFF460, 39, 16, 0x1FF)


def normalize_saved_city_owner_sentinels_frame_fields(state: StorageState,
                                                      frame: StorageFrame) -> StorageFrame:
    return _normalize_saved_sentinels_fields(state, storage_entry(state, frame),
        0xFFFFF428, 39, 8, 0xF)


def restore_saved_force_record_columns_frame_fields(state: StorageState,
                                                   frame: StorageFrame) -> StorageFrame:
    """91A2: actual A1 destination supplied by parent; reconstruct sixteen records."""
    frame = storage_entry(state, frame)
    for role, address in (('a2',0xFFFFD300),('a3',0xFFFFD310),
                          ('a4',0xFFFFD320),('a5',0xFFFFD330)):
        frame = storage_address(frame, role, address)
    frame = storage_move(state, frame, 'd0', 15, 16)
    while True:
        for source in ('a2','a3','a4','a5'):
            frame, value = storage_read_next(state, frame, source, 1)
            frame = storage_write_next(state, frame, 'a1', 1, value)
        frame, again = storage_dbra(frame, 'd0')
        if not again:
            return frame


def refresh_loaded_group_attributes_frame_fields(state: StorageState,
                                                  frame: StorageFrame) -> StorageFrame:
    """91F8: recompute each live packet's mean C400 BYTE using retained WORD count."""
    frame = storage_entry(state, frame)
    frame = storage_address(frame, 'a1', 0xFFFF9000)
    frame = storage_address(frame, 'a2', 0xFFFFC400)
    while True:
        frame = storage_move(state, frame, 'd0', state.read(frame.a1, 1), 8)
        if frame.status_word & 4:
            return frame
        frame = storage_move(state, frame, 'd1', frame.d0, 16)
        frame = storage_arithmetic(state, frame, 'd1', 1, 16, True)
        frame = storage_move(state, frame, 'd2', 0, 32)
        while True:
            frame = storage_move(state, frame, 'd3', 0, 16)
            frame = storage_move(state, frame, 'd3',
                state.read(frame.a1+s16(low16(frame.d1))+13, 1), 8)
            frame = storage_move(state, frame, 'd3',
                state.read(frame.a2+s16(low16(frame.d3)), 1), 8)
            frame = storage_arithmetic(state, frame, 'd2', frame.d3, 16)
            frame, again = storage_dbra(frame, 'd1')
            if not again:
                break
        frame = storage_divide(state, frame, 'd2', frame.d0)
        frame = storage_write(state, frame, frame.a1+3, 1, frame.d2)
        frame = storage_address_step(frame, 'a1', s16(low16(frame.d0))+13)


def restore_saved_game_state(state: StorageState, entry_frame: StorageFrame=None) -> RestoreOutcome:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    returned = restore_saved_game_state_frame_fields(state, frame)
    if returned.status_word & 1:
        return RestoreOutcome(False, None)
    return RestoreOutcome(True, state.table(returned.a0).cursor())

def restore_saved_metadata(state: StorageState, entry_frame: StorageFrame=None) -> None:
    raise Boundary('legacy partial storage phase has no whole entry; use the full save or restore core')

def begin_loaded_membership_fields(state: StorageState, entry_frame: StorageFrame=None) -> Cursor:
    raise Boundary('legacy partial storage phase has no whole entry; use the full save or restore core')

def restore_loaded_officer_fields(state: StorageState, source: Cursor, entry_frame: StorageFrame=None) -> Cursor:
    raise Boundary('legacy partial storage phase has no whole entry; use the full save or restore core')

def restore_loaded_city_fields(state: StorageState, source: Cursor, entry_frame: StorageFrame=None) -> Cursor:
    raise Boundary('legacy partial storage phase has no whole entry; use the full save or restore core')

def restore_saved_links_and_orders(state: StorageState, source: Cursor, entry_frame: StorageFrame=None) -> Cursor:
    raise Boundary('legacy partial storage phase has no whole entry; use the full save or restore core')

def restore_saved_force_and_battle_fields(state: StorageState, source: Cursor, entry_frame: StorageFrame=None) -> Cursor:
    raise Boundary('legacy partial storage phase has no whole entry; use the full save or restore core')

def restore_saved_officer_positions(state: StorageState, entry_frame: StorageFrame=None) -> None:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    returned = restore_saved_officer_positions_frame_fields(state, frame)
    return None

def restore_city_orders_and_action_flags(state: StorageState, entry_frame: StorageFrame=None) -> None:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    returned = restore_city_orders_and_action_flags_frame_fields(state, frame)
    return None

def restore_scaled_officer_parameter_words(state: StorageState, entry_frame: StorageFrame=None) -> None:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    returned = restore_scaled_officer_parameter_words_frame_fields(state, frame)
    return None

def normalize_saved_force_head_sentinels(state: StorageState, entry_frame: StorageFrame=None) -> None:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    returned = normalize_saved_force_head_sentinels_frame_fields(state, frame)
    return None

def normalize_saved_city_head_sentinels(state: StorageState, entry_frame: StorageFrame=None) -> None:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    returned = normalize_saved_city_head_sentinels_frame_fields(state, frame)
    return None

def normalize_saved_city_owner_sentinels(state: StorageState, entry_frame: StorageFrame=None) -> None:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    returned = normalize_saved_city_owner_sentinels_frame_fields(state, frame)
    return None

def restore_saved_force_record_columns(state: StorageState, destination: Cursor, entry_frame: StorageFrame=None) -> None:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    checked_cursor(destination, state)
    if destination.base != frame.a1:
        raise ValueError('restore force destination differs from entry A1')
    returned = restore_saved_force_record_columns_frame_fields(state, frame)
    destination.base = returned.a1
    return None

def refresh_loaded_group_attributes(state: StorageState, retained_header_high_byte: Byte=0, entry_frame: StorageFrame=None) -> None:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    if retained_header_high_byte != frame.d0 >> 8 & 255:
        raise ValueError('retained group count WORD differs from complete entry')
    returned = refresh_loaded_group_attributes_frame_fields(state, frame)
    return None
