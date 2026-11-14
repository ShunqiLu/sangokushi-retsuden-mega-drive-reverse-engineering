"""Original packed transport/group streams and live SRAM checksums.

The three bit-buffer formats deliberately remain distinct. They use different
carriers, masking and read/write order. High bits are retained exactly; short
records, residue writes and malformed original inputs are not normalized.
"""
from .domain import StorageState, Long, low16, s16
from .contexts_storage_fields import (
    StorageFrame, storage_entry, storage_move, storage_address,
    storage_address_step, storage_read_next, storage_write, storage_write_next,
    storage_logic, storage_binary, storage_arithmetic, storage_shift,
    storage_swap, storage_dbra, storage_call, storage_replace,
    storage_compare_value,
)
from .contexts_streams import BitWriter, BitReader, FixedFieldReadContext, checked_buffer
from .domain import Table, Cursor, Word, CarryOutcome, Boundary, checked_cursor, checked_table
from .contexts_storage_fields import storage_legacy_entry


def _storage_flush_word_residue_fields(state: StorageState, frame: StorageFrame,
                                      carrier: str) -> StorageFrame:
    """Shared original append loop: BYTE write, lane step, bit SUB, LONG shift."""
    if carrier not in ('d0','d7'):
        raise ValueError('closed storage residue carrier required')
    while True:
        frame = storage_arithmetic(state, frame, 'd4', 8, 16, True, True)
        if frame.status_word & 1:
            return frame
        value = frame.d0 if carrier == 'd0' else frame.d7
        frame = storage_write_next(state, frame, 'a0', 1, value)
        frame = storage_address_step(frame, 'a0', 1)
        frame = storage_arithmetic(state, frame, 'd4', 8, 16, True)
        frame = storage_shift(state, frame, carrier, 8, 32, True)


def append_little_endian_bitfield_frame_fields(state: StorageState,
                                               frame: StorageFrame) -> StorageFrame:
    """89E0: D0 value/D1 width, D3 residue/D4 bit count, A0 odd-lane output."""
    frame = storage_entry(state, frame)
    frame = storage_shift(state, frame, 'd0', low16(frame.d4), 32)
    frame = storage_binary(state, frame, 'd0', frame.d3, 16, 'or')
    frame = storage_arithmetic(state, frame, 'd4', frame.d1, 16)
    frame = _storage_flush_word_residue_fields(state, frame, 'd0')
    return storage_move(state, frame, 'd3', frame.d0, 16)


def write_packed_transport_orders_frame_fields(state: StorageState,
                                              frame: StorageFrame) -> StorageFrame:
    """88C6: forty live 2+7+7+6-bit CE00 records; no invented child CALL."""
    frame = storage_entry(state, frame)
    frame = storage_address(frame, 'a1', 0xFFFFCE00)
    frame = storage_move(state, frame, 'd3', 0, 16)
    frame = storage_move(state, frame, 'd4', 0, 16)
    frame = storage_move(state, frame, 'd0', 39, 16)
    while True:
        frame = storage_move(state, frame, 'd7', 0, 32)
        frame, value = storage_read_next(state, frame, 'a1', 1)
        frame = storage_move(state, frame, 'd7', value, 8)
        frame = storage_binary(state, frame, 'd7', 3, 16, 'and')
        for width, mask in ((7,127),(7,127),(6,63)):
            frame = storage_shift(state, frame, 'd7', width, 32 if width == 6 else 16)
            frame, value = storage_read_next(state, frame, 'a1', 1)
            frame = storage_move(state, frame, 'd1', value, 8)
            frame = storage_binary(state, frame, 'd1', mask, 16, 'and')
            frame = storage_binary(state, frame, 'd7', frame.d1, 16, 'or')
        frame = storage_shift(state, frame, 'd7', low16(frame.d4), 32)
        frame = storage_binary(state, frame, 'd7', frame.d3, 16, 'or')
        frame = storage_arithmetic(state, frame, 'd4', 22, 16)
        frame = _storage_flush_word_residue_fields(state, frame, 'd7')
        frame = storage_move(state, frame, 'd3', frame.d7, 16)
        frame, again = storage_dbra(frame, 'd0')
        if not again:
            break
    frame = storage_logic(state, frame, frame.d4, 16)
    if not frame.status_word & 4:
        frame = storage_write_next(state, frame, 'a0', 1, frame.d7)
        frame = storage_address_step(frame, 'a0', 1)
    return frame


def _read_saved_group_long_fields(state: StorageState,
                                  frame: StorageFrame) -> StorageFrame:
    """The original BYTE/WORD/LONG assembly order of each live group field."""
    frame, value = storage_read_next(state, frame, 'a1', 1)
    frame = storage_move(state, frame, 'd0', value, 8)
    frame = storage_shift(state, frame, 'd0', 8, 16)
    frame, value = storage_read_next(state, frame, 'a1', 1)
    frame = storage_move(state, frame, 'd0', value, 8)
    for _ in range(2):
        frame = storage_shift(state, frame, 'd0', 8, 32)
        frame, value = storage_read_next(state, frame, 'a1', 1)
        frame = storage_move(state, frame, 'd0', value, 8)
    return frame


def write_packed_group_stream_frame_fields(state: StorageState,
                                          frame: StorageFrame) -> StorageFrame:
    """8946: variable roster records and their unconditional final residue BYTE."""
    frame = storage_entry(state, frame)
    frame = storage_address(frame, 'a1', 0xFFFF9000)
    frame = storage_move(state, frame, 'd3', 0, 32)
    frame = storage_move(state, frame, 'd4', 0, 16)
    while True:
        frame, value = storage_read_next(state, frame, 'a1', 1)
        frame = storage_move(state, frame, 'd0', value, 8)
        frame = storage_binary(state, frame, 'd0', 15, 32, 'and')
        frame = storage_move(state, frame, 'd7', frame.d0, 16)
        frame = storage_move(state, frame, 'd1', 4, 16)
        frame = storage_call(state, frame, append_little_endian_bitfield_frame_fields, 0x8960)
        frame = storage_logic(state, frame, frame.d7, 16)
        if frame.status_word & 4:
            break
        for continuation in (0x8976,0x8986):
            frame, value = storage_read_next(state, frame, 'a1', 1)
            frame = storage_move(state, frame, 'd0', value, 8)
            frame = storage_binary(state, frame, 'd0', 127, 32, 'and')
            frame = storage_move(state, frame, 'd1', 7, 16)
            frame = storage_call(state, frame, append_little_endian_bitfield_frame_fields, continuation)
        frame = storage_address_step(frame, 'a1', 1)
        frame, value = storage_read_next(state, frame, 'a1', 1)
        frame = storage_move(state, frame, 'd0', value, 8)
        # 8988 owner BYTE is intentionally not masked before the four-bit call.
        frame = storage_move(state, frame, 'd1', 4, 16)
        frame = storage_call(state, frame, append_little_endian_bitfield_frame_fields, 0x8992)
        for width, continuation in ((18,0x89A8),(20,0x89BE)):
            frame = _read_saved_group_long_fields(state, frame)
            frame = storage_move(state, frame, 'd1', width, 16)
            frame = storage_call(state, frame, append_little_endian_bitfield_frame_fields, continuation)
        frame = storage_arithmetic(state, frame, 'd7', 1, 16, True)
        while True:
            frame, value = storage_read_next(state, frame, 'a1', 1)
            frame = storage_move(state, frame, 'd0', value, 8)
            frame = storage_binary(state, frame, 'd0', 255, 32, 'and')
            frame = storage_move(state, frame, 'd1', 8, 16)
            frame = storage_call(state, frame, append_little_endian_bitfield_frame_fields, 0x89D0)
            frame, again = storage_dbra(frame, 'd7')
            if not again:
                break
    frame = storage_write_next(state, frame, 'a0', 1, frame.d3)
    return storage_address_step(frame, 'a0', 1)


def checksum_saved_payload_frame_fields(state: StorageState,
                                        frame: StorageFrame) -> StorageFrame:
    """8A22: sum exactly 1EED successful odd-lane BYTE reads into D1 LONG."""
    frame = storage_entry(state, frame)
    frame = storage_address(frame, 'a0', 0x200115)
    frame = storage_move(state, frame, 'd0', 0x1EEC, 16)
    frame = storage_move(state, frame, 'd1', 0, 32)
    frame = storage_move(state, frame, 'd2', 0, 32)
    while True:
        frame, value = storage_read_next(state, frame, 'a0', 1)
        frame = storage_move(state, frame, 'd2', value, 8)
        frame = storage_arithmetic(state, frame, 'd1', frame.d2, 32)
        frame = storage_address_step(frame, 'a0', 1)
        frame, again = storage_dbra(frame, 'd0')
        if not again:
            return frame


def write_saved_state_checksum_frame_fields(state: StorageState,
                                            frame: StorageFrame) -> StorageFrame:
    """89FE: low checksum BYTE first; final shift affects only retained WORD."""
    frame = storage_entry(state, frame)
    frame = storage_call(state, frame, checksum_saved_payload_frame_fields, 0x8A02)
    for address, following_bits in ((0x20010D,32),(0x20010F,32),(0x200111,16)):
        frame = storage_write(state, frame, address, 1, frame.d1)
        frame = storage_shift(state, frame, 'd1', 8, following_bits, True)
    return storage_write(state, frame, 0x200113, 1, frame.d1)


def validate_saved_header_and_checksum_frame_fields(state: StorageState,
                                                    frame: StorageFrame) -> StorageFrame:
    """90D8: exact SEG[A] header and checksum; full-SR carry update is real."""
    frame = storage_entry(state, frame)
    valid = True
    for address, expected in ((0x200105,0x53),(0x200107,0x45),
                              (0x200109,0x47),(0x20010B,0x41)):
        frame = storage_compare_value(state, frame, state.read(address, 1), expected, 8)
        if not frame.status_word & 4:
            valid = False
            break
    if valid:
        frame = storage_call(state, frame, checksum_saved_payload_frame_fields, 0x910C)
        for address, following_bits in ((0x20010D,32),(0x20010F,32),
                                        (0x200111,16),(0x200113,0)):
            frame = storage_arithmetic(state, frame, 'd1', state.read(address, 1), 8, True, True)
            if not frame.status_word & 4:
                valid = False
                break
            if following_bits:
                frame = storage_shift(state, frame, 'd1', 8, following_bits, True)
    state.sr = frame.status_word
    state.carry_result(0 if valid else 1)
    return storage_replace(frame, status_word=state.sr)


def read_buffered_low_word_bitfield_frame_fields(state: StorageState,
                                                 frame: StorageFrame) -> StorageFrame:
    """8FFE: at most one input BYTE; D3 residue and shifts are WORD-only."""
    frame = storage_entry(state, frame)
    frame = storage_arithmetic(state, frame, 'd4', frame.d5, 16, True, True)
    if frame.status_word & 1:
        frame = storage_move(state, frame, 'd1', 0, 16)
        frame, value = storage_read_next(state, frame, 'a0', 1)
        frame = storage_move(state, frame, 'd1', value, 8)
        frame = storage_address_step(frame, 'a0', 1)
        frame = storage_shift(state, frame, 'd1', low16(frame.d4), 16)
        frame = storage_binary(state, frame, 'd3', frame.d1, 16, 'or')
        frame = storage_arithmetic(state, frame, 'd4', 8, 16)
    frame = storage_move(state, frame, 'd2', frame.d3, 16)
    frame = storage_binary(state, frame, 'd2', frame.d6, 16, 'and')
    frame = storage_shift(state, frame, 'd3', low16(frame.d5), 16, True)
    return storage_arithmetic(state, frame, 'd4', frame.d5, 16, True)


def read_packed_transport_orders_frame_fields(state: StorageState,
                                             frame: StorageFrame) -> StorageFrame:
    """8FB4: reverse-byte-order reconstruction of all forty CE00 records."""
    frame = storage_entry(state, frame)
    frame = storage_address(frame, 'a1', 0xFFFFCE00)
    frame = storage_move(state, frame, 'd3', 0, 16)
    frame = storage_move(state, frame, 'd4', 0, 16)
    frame = storage_move(state, frame, 'd7', 39, 16)
    while True:
        for width, mask, displacement, continuation in (
                (6,63,3,0x8FCC),(7,127,2,0x8FDC),
                (7,127,1,0x8FE4),(2,3,0,0x8FF4)):
            if displacement != 1:
                frame = storage_move(state, frame, 'd5', width, 16)
                frame = storage_move(state, frame, 'd6', mask, 16)
            frame = storage_call(state, frame, read_buffered_low_word_bitfield_frame_fields, continuation)
            frame = storage_write(state, frame, frame.a1+displacement, 1, frame.d2)
        frame = storage_address_step(frame, 'a1', 4)
        frame, again = storage_dbra(frame, 'd7')
        if not again:
            return frame


def read_buffered_long_bitfield_frame_fields(state: StorageState,
                                             frame: StorageFrame) -> StorageFrame:
    """91C4: D0 BYTE residue/D1 bits, D2 width/D3 mask; result D4 LONG."""
    frame = storage_entry(state, frame)
    frame = storage_move(state, frame, 'd4', 0, 32)
    frame = storage_move(state, frame, 'd4', frame.d0, 8)
    frame = storage_shift(state, frame, 'd4', 8, 32, True, True)
    while True:
        frame = storage_arithmetic(state, frame, 'd1', frame.d2, 16, True, True)
        if not frame.status_word & 1:
            break
        frame, value = storage_read_next(state, frame, 'a0', 1)
        frame = storage_move(state, frame, 'd4', value, 8)
        frame = storage_move(state, frame, 'd0', frame.d4, 8)
        frame = storage_address_step(frame, 'a0', 1)
        frame = storage_arithmetic(state, frame, 'd1', 8, 16)
        frame = storage_shift(state, frame, 'd4', 8, 32, True, True)
    frame = storage_move(state, frame, 'd5', 32, 16)
    frame = storage_arithmetic(state, frame, 'd5', frame.d1, 16, True)
    while True:
        frame = storage_arithmetic(state, frame, 'd5', 8, 16, True, True)
        if frame.status_word & 5:
            break
        frame = storage_shift(state, frame, 'd4', 8, 32, True)
        frame = storage_arithmetic(state, frame, 'd5', 8, 16, True)
    frame = storage_shift(state, frame, 'd4', low16(frame.d5), 32, True)
    frame = storage_binary(state, frame, 'd4', frame.d3, 32, 'and')
    return storage_arithmetic(state, frame, 'd1', frame.d2, 16, True)


def _restore_saved_group_long_fields(state: StorageState,
                                     frame: StorageFrame) -> StorageFrame:
    for displacement, following_bits in ((3,32),(2,32),(1,16),(0,0)):
        frame = storage_write(state, frame, frame.a1+displacement, 1, frame.d4)
        if following_bits:
            frame = storage_shift(state, frame, 'd4', 8, following_bits, True)
    return storage_address_step(frame, 'a1', 4)


def read_packed_group_stream_frame_fields(state: StorageState,
                                         frame: StorageFrame) -> StorageFrame:
    """9036: restore records live, then call the unique group-attribute core."""
    from .business_load import refresh_loaded_group_attributes_frame_fields
    frame = storage_entry(state, frame)
    frame = storage_address(frame, 'a1', 0xFFFF9000)
    frame = storage_move(state, frame, 'd0', 0, 16)
    frame = storage_move(state, frame, 'd1', 0, 16)
    while True:
        frame = storage_move(state, frame, 'd2', 4, 16)
        frame = storage_move(state, frame, 'd3', 15, 32)
        frame = storage_call(state, frame, read_buffered_long_bitfield_frame_fields, 0x9048)
        frame = storage_write_next(state, frame, 'a1', 1, frame.d4)
        if frame.status_word & 4:
            break
        frame = storage_move(state, frame, 'd7', frame.d4, 16)
        frame = storage_move(state, frame, 'd2', 7, 16)
        frame = storage_move(state, frame, 'd3', 127, 32)
        frame = storage_call(state, frame, read_buffered_long_bitfield_frame_fields, 0x905A)
        frame = storage_write_next(state, frame, 'a1', 1, frame.d4)
        frame = storage_call(state, frame, read_buffered_long_bitfield_frame_fields, 0x9060)
        frame = storage_write_next(state, frame, 'a1', 1, frame.d4)
        frame = storage_address_step(frame, 'a1', 1)
        frame = storage_move(state, frame, 'd2', 4, 16)
        frame = storage_move(state, frame, 'd3', 15, 32)
        frame = storage_call(state, frame, read_buffered_long_bitfield_frame_fields, 0x906E)
        frame = storage_write_next(state, frame, 'a1', 1, frame.d4)
        for width, mask, continuation in ((18,0x3FFFF,0x907E),(20,0xFFFFF,0x90A2)):
            frame = storage_move(state, frame, 'd2', width, 16)
            frame = storage_move(state, frame, 'd3', mask, 32)
            frame = storage_call(state, frame, read_buffered_long_bitfield_frame_fields, continuation)
            frame = _restore_saved_group_long_fields(state, frame)
        frame = storage_arithmetic(state, frame, 'd7', 1, 16, True)
        while True:
            frame = storage_move(state, frame, 'd2', 8, 16)
            frame = storage_move(state, frame, 'd3', 255, 32)
            frame = storage_call(state, frame, read_buffered_long_bitfield_frame_fields, 0x90C8)
            frame = storage_write_next(state, frame, 'a1', 1, frame.d4)
            frame, again = storage_dbra(frame, 'd7')
            if not again:
                break
    return storage_call(state, frame, refresh_loaded_group_attributes_frame_fields, 0x90D6)


def _storage_fixed_mask_fields(state: StorageState,
                               frame: StorageFrame) -> StorageFrame:
    frame = storage_address(frame, 'a2', 0x929A)
    frame = storage_move(state, frame, 'd5', frame.d0, 16)
    frame = storage_shift(state, frame, 'd5', 2, 16)
    mask = state.read(frame.a2+s16(low16(frame.d5)), 4)
    return storage_move(state, frame, 'd5', mask, 32)


def write_masked_fixed_count_frame_fields(state: StorageState,
                                         frame: StorageFrame) -> StorageFrame:
    """922A: D0 bits/D1 stride/D2 count, actual live LONG mask at 929A.

    The original final residue is written to source A1 at 9294, not output A0.
    That surprising encoded 1283 operation is preserved, not silently repaired.
    """
    frame = storage_entry(state, frame)
    frame = storage_arithmetic(state, frame, 'd2', 1, 16, True)
    frame = storage_move(state, frame, 'd3', 0, 16)
    frame = storage_move(state, frame, 'd4', 0, 16)
    frame = _storage_fixed_mask_fields(state, frame)
    while True:
        frame = storage_move(state, frame, 'd7', 0, 32)
        frame = storage_move(state, frame, 'd6', frame.d1, 16)
        while True:
            frame = storage_logic(state, frame, frame.d6, 16)
            if frame.status_word & 4:
                break
            frame = storage_arithmetic(state, frame, 'd6', 4, 16, True, True)
            if frame.status_word & 4:
                frame, value = storage_read_next(state, frame, 'a1', 4)
                frame = storage_move(state, frame, 'd7', value, 32)
                break
            frame = storage_arithmetic(state, frame, 'd6', 2, 16, True, True)
            if not frame.status_word & 1:
                frame = storage_swap(state, frame, 'd7')
                frame, value = storage_read_next(state, frame, 'a1', 2)
                frame = storage_move(state, frame, 'd7', value, 16)
                frame = storage_arithmetic(state, frame, 'd6', 2, 16, True)
                continue
            frame = storage_shift(state, frame, 'd7', 8, 32)
            frame, value = storage_read_next(state, frame, 'a1', 1)
            frame = storage_move(state, frame, 'd7', value, 8)
            break
        frame = storage_binary(state, frame, 'd7', frame.d5, 32, 'and')
        frame = storage_shift(state, frame, 'd7', low16(frame.d4), 32)
        frame = storage_binary(state, frame, 'd7', frame.d3, 8, 'or')
        frame = storage_arithmetic(state, frame, 'd4', frame.d0, 16)
        while True:
            frame = storage_arithmetic(state, frame, 'd4', 8, 16, True, True)
            if frame.status_word & 1:
                break
            frame = storage_write_next(state, frame, 'a0', 1, frame.d7)
            frame = storage_shift(state, frame, 'd7', 8, 32, True)
            frame = storage_address_step(frame, 'a0', 1)
            frame = storage_arithmetic(state, frame, 'd4', 8, 16, True)
        frame = storage_move(state, frame, 'd3', frame.d7, 16)
        frame, again = storage_dbra(frame, 'd2')
        if not again:
            break
    frame = storage_logic(state, frame, frame.d3, 16)
    if not frame.status_word & 4:
        frame = storage_write(state, frame, frame.a1, 1, frame.d3)
        frame = storage_address_step(frame, 'a1', 2)
    return frame


def read_masked_fixed_count_frame_fields(state: StorageState,
                                        frame: StorageFrame) -> StorageFrame:
    """931E: actual WORD residue, endian restore, signed indexed destination."""
    frame = storage_entry(state, frame)
    frame = storage_arithmetic(state, frame, 'd2', 1, 16, True)
    frame = storage_move(state, frame, 'd3', 0, 16)
    frame = storage_move(state, frame, 'd4', 0, 16)
    frame = _storage_fixed_mask_fields(state, frame)
    while True:
        frame = storage_move(state, frame, 'd7', frame.d3, 8)
        while True:
            frame = storage_arithmetic(state, frame, 'd4', frame.d0, 16, True, True)
            if not frame.status_word & 1:
                break
            frame = storage_shift(state, frame, 'd7', 8, 32, True, True)
            frame, value = storage_read_next(state, frame, 'a0', 1)
            frame = storage_move(state, frame, 'd7', value, 8)
            frame = storage_address_step(frame, 'a0', 1)
            frame = storage_arithmetic(state, frame, 'd4', 8, 16)
        frame = storage_move(state, frame, 'd3', frame.d7, 16)
        frame = storage_arithmetic(state, frame, 'd4', 8, 16, True, True)
        if frame.status_word & 5:
            frame = storage_move(state, frame, 'd6', 8, 16)
            frame = storage_arithmetic(state, frame, 'd6', frame.d4, 16, True)
            frame = storage_shift(state, frame, 'd7', low16(frame.d6), 16, True)
        else:
            frame = storage_shift(state, frame, 'd7', 8, 32, True, True)
            frame = storage_move(state, frame, 'd6', 32, 16)
            frame = storage_arithmetic(state, frame, 'd6', frame.d4, 16, True)
            while True:
                frame = storage_arithmetic(state, frame, 'd6', 8, 16, True, True)
                if frame.status_word & 5:
                    break
                frame = storage_shift(state, frame, 'd7', 8, 32, True)
                frame = storage_arithmetic(state, frame, 'd6', 8, 16, True)
            frame = storage_shift(state, frame, 'd7', low16(frame.d6), 32, True)
        frame = storage_binary(state, frame, 'd7', frame.d5, 32, 'and')
        frame = storage_move(state, frame, 'd6', frame.d1, 16)
        frame = storage_arithmetic(state, frame, 'd6', 1, 16, True)
        while True:
            frame = storage_write(state, frame, frame.a1+s16(low16(frame.d6)), 1, frame.d7)
            frame = storage_shift(state, frame, 'd7', 8, 32, True)
            frame, again = storage_dbra(frame, 'd6')
            if not again:
                break
        frame = storage_address_step(frame, 'a1', s16(low16(frame.d1)))
        frame = storage_arithmetic(state, frame, 'd4', frame.d0, 16, True)
        frame, again = storage_dbra(frame, 'd2')
        if not again:
            return frame


def append_little_endian_bitfield(state: StorageState, writer: BitWriter, value: Long, width: Word, entry_frame: StorageFrame=None) -> Long:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    checked_buffer(writer, BitWriter, state)
    if (writer.cursor.base, writer.residue, writer.bit_count, value, width) != (frame.a0, frame.d3, low16(frame.d4), frame.d0, low16(frame.d1)):
        raise ValueError('bit-writer arguments differ from complete entry')
    returned = append_little_endian_bitfield_frame_fields(state, frame)
    writer.cursor.base = returned.a0
    writer.residue = returned.d3
    writer.bit_count = low16(returned.d4)
    return returned.d0

def write_packed_transport_orders(state: StorageState, destination: Cursor, entry_frame: StorageFrame=None) -> Cursor:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    checked_cursor(destination, state)
    if destination.base != frame.a0:
        raise ValueError('save stream differs from complete entry A0')
    returned = write_packed_transport_orders_frame_fields(state, frame)
    destination.base = returned.a0
    return destination

def write_packed_group_stream(state: StorageState, destination: Cursor, entry_frame: StorageFrame=None) -> Cursor:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    checked_cursor(destination, state)
    if destination.base != frame.a0:
        raise ValueError('save stream differs from complete entry A0')
    returned = write_packed_group_stream_frame_fields(state, frame)
    destination.base = returned.a0
    return destination

def checksum_saved_payload(state: StorageState, entry_frame: StorageFrame=None) -> Long:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    returned = checksum_saved_payload_frame_fields(state, frame)
    return returned.d1

def write_saved_state_checksum(state: StorageState, entry_frame: StorageFrame=None) -> Long:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    returned = write_saved_state_checksum_frame_fields(state, frame)
    return returned.d1

def read_buffered_low_word_bitfield(state: StorageState, reader: BitReader, width: Word, mask: Word, entry_frame: StorageFrame=None) -> Word:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    checked_buffer(reader, BitReader, state)
    if (reader.cursor.base, reader.residue, reader.bit_count, width, mask) != (frame.a0, frame.d3, low16(frame.d4), low16(frame.d5), low16(frame.d6)):
        raise ValueError('WORD reader arguments differ from complete entry')
    returned = read_buffered_low_word_bitfield_frame_fields(state, frame)
    reader.cursor.base = returned.a0
    reader.residue = returned.d3
    reader.bit_count = low16(returned.d4)
    return low16(returned.d2)

def read_packed_transport_orders(state: StorageState, source: Cursor, entry_frame: StorageFrame=None) -> Cursor:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    checked_cursor(source, state)
    if source.base != frame.a0:
        raise ValueError('load stream differs from complete entry A0')
    returned = read_packed_transport_orders_frame_fields(state, frame)
    source.base = returned.a0
    return source

def read_buffered_long_bitfield(state: StorageState, reader: BitReader, width: Word, mask: Long, entry_frame: StorageFrame=None) -> Long:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    checked_buffer(reader, BitReader, state)
    if (reader.cursor.base, reader.residue, reader.bit_count, width, mask) != (frame.a0, frame.d0, low16(frame.d1), low16(frame.d2), frame.d3):
        raise ValueError('LONG reader arguments differ from complete entry')
    returned = read_buffered_long_bitfield_frame_fields(state, frame)
    reader.cursor.base = returned.a0
    reader.residue = returned.d0
    reader.bit_count = low16(returned.d1)
    return returned.d4

def read_packed_group_stream(state: StorageState, source: Cursor, entry_frame: StorageFrame=None) -> Cursor:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    checked_cursor(source, state)
    if source.base != frame.a0:
        raise ValueError('load stream differs from complete entry A0')
    returned = read_packed_group_stream_frame_fields(state, frame)
    source.base = returned.a0
    return source

def validate_saved_header_and_checksum(state: StorageState, entry_frame: StorageFrame=None) -> CarryOutcome:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    returned = validate_saved_header_and_checksum_frame_fields(state, frame)
    return CarryOutcome(returned.status_word & 1, returned.status_word)

def write_masked_fixed_count_fields(state: StorageState, source: Table, destination: Cursor, bit_width: Word, source_width: Word, record_count: Word, entry_frame: StorageFrame=None) -> Cursor:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    checked_table(source, state)
    checked_cursor(destination, state)
    if (source.base, destination.base, bit_width, source_width, record_count) != (frame.a1, frame.a0, low16(frame.d0), low16(frame.d1), low16(frame.d2)):
        raise ValueError('fixed writer arguments differ from complete entry')
    returned = write_masked_fixed_count_frame_fields(state, frame)
    destination.base = returned.a0
    return destination

def read_masked_fixed_count_fields(state: StorageState, source: Cursor, destination: Table, bit_width: Word, destination_width: Word, record_count: Word, retained: FixedFieldReadContext=None, entry_frame: StorageFrame=None) -> Cursor:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    checked_cursor(source, state)
    checked_table(destination, state)
    if (source.base, destination.base, bit_width, destination_width, record_count) != (frame.a0, frame.a1, low16(frame.d0), low16(frame.d1), low16(frame.d2)):
        raise ValueError('fixed reader arguments differ from complete entry')
    if retained is not None:
        if type(retained) is not FixedFieldReadContext:
            raise ValueError('exact fixed-field retained context required')
        retained.__post_init__()
        if retained.value_carrier != frame.d7:
            raise ValueError('fixed reader retained LONG differs from entry D7')
    returned = read_masked_fixed_count_frame_fields(state, frame)
    source.base = returned.a0
    if retained is not None:
        retained.value_carrier = returned.d7
    return source
