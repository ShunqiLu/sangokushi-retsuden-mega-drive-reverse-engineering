"""Complete live-table save sequence and its four quantization preparations.

Each column is deliberately packed at its original point in the stream. The
scratch columns alias later phases; there is no snapshot, transaction, new
save slot, clamping or validation of original payload values. Address-named
columns retain unconfirmed meanings instead of assigning speculative names.
"""
from .domain import StorageState, Long, low16
from .contexts_storage_fields import (
    StorageFrame, storage_entry, storage_move, storage_address,
    storage_address_step, storage_read_next, storage_write,
    storage_write_next, storage_arithmetic, storage_binary, storage_shift,
    storage_divide, storage_dbra, storage_call,
)
from .business_streams import (
    write_masked_fixed_count_frame_fields, write_packed_transport_orders_frame_fields,
    write_packed_group_stream_frame_fields, write_saved_state_checksum_frame_fields,
)
from .contexts_save import SavedForceColumnContext
from .domain import Cursor, Boundary
from .contexts_storage_fields import storage_legacy_entry


def _write_saved_column_fields(state: StorageState, frame: StorageFrame,
                               column: tuple) -> StorageFrame:
    source, field_bits, stride, count, continuation = column
    frame = storage_address(frame, 'a1', source)
    frame = storage_move(state, frame, 'd0', field_bits, 16)
    frame = storage_move(state, frame, 'd1', stride, 16)
    frame = storage_move(state, frame, 'd2', count, 16)
    return storage_call(state, frame, write_masked_fixed_count_frame_fields, continuation)


def _write_saved_columns_fields(state: StorageState, frame: StorageFrame,
                                columns: tuple) -> StorageFrame:
    for column in columns:
        frame = _write_saved_column_fields(state, frame, column)
    return frame


def write_saved_game_state_frame_fields(state: StorageState,
                                        frame: StorageFrame) -> StorageFrame:
    """83FA..8866: write header, membership, officers, cities and orders.

    The full original 1,132-byte owner returns all retained carriers and SR-X.
    Each continuation in a column record is a real BSR caller-owned LONG, not
    an instruction dispatcher. SRAM addresses are absolute LONG bus values.
    """
    frame = storage_entry(state, frame)
    for address, value in ((0x200105,0x53),(0x200107,0x45),
                           (0x200109,0x47),(0x20010B,0x41)):
        frame = storage_write(state, frame, address, 1, value)
    for source, destination in ((0xFFFFF67B,0x200115),(0xFFFFF67D,0x200117),
            (0xFFFFF67F,0x200119),(0xFFFFF374,0x20011B),(0xFFFFF375,0x20011D),
            (0xFFFFEFD3,0x20011F),(0xFFFFEFE5,0x200121),
            (0xFFFFEFD7,0x200123),(0xFFFFEFD9,0x200125)):
        frame = storage_write(state, frame, destination, 1, state.read(source, 1))
    frame = storage_address(frame, 'a0', 0x200127)

    # Membership flags are five actual unrolled moves; no Dn counter exists.
    frame = _write_saved_column_fields(state, frame, (0xFFFFA000,5,1,40,0x847C))
    frame = storage_address(frame, 'a1', 0xFFFFEFAA)
    for _ in range(5):
        frame, value = storage_read_next(state, frame, 'a1', 1)
        frame = storage_write_next(state, frame, 'a0', 1, value)
        frame = storage_address_step(frame, 'a0', 1)
    frame = _write_saved_columns_fields(state, frame, (
        (0xFFFFA028,8,1,40,0x84B2),(0xFFFFA050,8,1,256,0x84C6)))

    frame = storage_call(state, frame, stage_saved_officer_positions_frame_fields, 0x84CA)
    frame = _write_saved_columns_fields(state, frame, (
        (0xFFFFD300,8,2,256,0x84DE),(0xFFFFD500,9,2,256,0x84F2),
        (0xFFFFB200,8,2,256,0x8506),(0xFFFFB400,8,2,256,0x851A),
        (0xFFFFB600,8,2,256,0x852E)))
    frame = storage_call(state, frame, stage_scaled_officer_parameter_words_frame_fields, 0x8532)
    frame = _write_saved_columns_fields(state, frame, (
        (0xFFFFD300,5,2,256,0x8546),(0xFFFFC000,10,2,256,0x855A),
        (0xFFFFBE00,10,2,256,0x856E),(0xFFFFC200,7,1,256,0x8582),
        (0xFFFFC300,7,1,256,0x8596),(0xFFFFC400,5,1,256,0x85AA),
        (0xFFFFC500,7,1,256,0x85BE),(0xFFFFC700,5,1,256,0x85D2),
        (0xFFFFC800,14,4,256,0x85E6),(0xFFFFCC00,8,1,256,0x85FA)))

    frame = _write_saved_columns_fields(state, frame, (
        (0xFFFFE000,20,4,40,0x860E),(0xFFFFE0A0,20,4,40,0x8622),
        (0xFFFFE140,10,4,40,0x8636),(0xFFFFE1E0,10,4,40,0x864A),
        (0xFFFFE280,7,4,40,0x865E),(0xFFFFE320,7,4,40,0x8672),
        (0xFFFFE3C0,7,4,40,0x8686),(0xFFFFE5A0,7,4,40,0x869A),
        (0xFFFFF428,4,1,40,0x86AE),(0xFFFFE640,9,2,16,0x86C2),
        (0xFFFFF460,9,2,40,0x86D6),(0xFFFFE660,20,4,40,0x86EA)))
    for source in (0xFFFFE700,0xFFFFE701):
        frame = storage_write_next(state, frame, 'a0', 1, state.read(source, 1))
        frame = storage_address_step(frame, 'a0', 1)
    frame = storage_address(frame, 'a1', 0xFFFFE710)
    frame = storage_move(state, frame, 'd2', 31, 16)
    while True:
        frame, value = storage_read_next(state, frame, 'a1', 1)
        frame = storage_write_next(state, frame, 'a0', 1, value)
        frame = storage_address_step(frame, 'a0', 1)
        frame, again = storage_dbra(frame, 'd2')
        if not again:
            break
    frame = _write_saved_column_fields(state, frame, (0xFFFFE778,17,4,40,0x8720))

    frame = storage_call(state, frame, stage_saved_city_orders_frame_fields, 0x8724)
    frame = _write_saved_columns_fields(state, frame, (
        (0xFFFFD300,9,2,40,0x8738),(0xFFFFD350,14,2,40,0x874C),
        (0xFFFFD3A0,9,2,40,0x8760),(0xFFFFD3F0,7,2,40,0x8774),
        (0xFFFFD440,9,2,40,0x8788),(0xFFFFD490,10,2,40,0x879C)))
    frame = storage_address(frame, 'a1', 0xFFFFE9F8)
    frame = storage_call(state, frame, stage_saved_force_record_columns_frame_fields, 0x87A4)
    frame = _write_saved_columns_fields(state, frame, (
        (0xFFFFD300,6,1,16,0x87B8),(0xFFFFD310,6,1,16,0x87CC),
        (0xFFFFD320,8,1,16,0x87E0),(0xFFFFD330,4,1,16,0x87F4),
        (0xFFFFEA38,1,1,40,0x8808),(0xFFFFEA88,2,1,768,0x881C),
        (0xFFFFED88,18,4,40,0x8830),(0xFFFFEE28,20,4,40,0x8844),
        (0xFFFFF590,2,1,16,0x8858)))
    frame = storage_call(state, frame, write_packed_transport_orders_frame_fields, 0x885C)
    frame = storage_call(state, frame, write_packed_group_stream_frame_fields, 0x8860)
    return storage_call(state, frame, write_saved_state_checksum_frame_fields, 0x8864)


def stage_saved_officer_positions_frame_fields(state: StorageState,
                                              frame: StorageFrame) -> StorageFrame:
    """Quantize 256 live coordinate pairs into their two scratch WORD columns."""
    frame = storage_entry(state, frame)
    frame = storage_address(frame, 'a2', 0xFFFFA150)
    frame = storage_address(frame, 'a3', 0xFFFFD300)
    frame = storage_address(frame, 'a4', 0xFFFFD500)
    frame = storage_move(state, frame, 'd0', 255, 16)
    while True:
        for destination in ('a3','a4'):
            frame, coordinate = storage_read_next(state, frame, 'a2', 2)
            frame = storage_move(state, frame, 'd1', coordinate, 16)
            frame = storage_shift(state, frame, 'd1', 7, 16, True)
            frame = storage_write_next(state, frame, destination, 2, frame.d1)
        frame, again = storage_dbra(frame, 'd0')
        if not again:
            return frame


def stage_saved_city_orders_frame_fields(state: StorageState,
                                        frame: StorageFrame) -> StorageFrame:
    """Split forty six-WORD orders, preserving the FFFF quantization bypass."""
    frame = storage_entry(state, frame)
    frame = storage_address(frame, 'a1', 0xFFFFE818)
    frame = storage_address(frame, 'a2', 0xFFFFD300)
    frame = storage_move(state, frame, 'd0', 39, 16)
    while True:
        for displacement in (0,0x50,0xA0):
            frame, value = storage_read_next(state, frame, 'a1', 2)
            frame = storage_write(state, frame, frame.a2+displacement, 2, value)
        frame, value = storage_read_next(state, frame, 'a1', 2)
        frame = storage_move(state, frame, 'd1', value, 16)
        frame = storage_arithmetic(state, frame, 'd1', 0xFFFF, 16, True, True)
        if low16(frame.d1) != 0xFFFF:
            frame = storage_binary(state, frame, 'd1', 0xFFFF, 32, 'and')
            frame = storage_divide(state, frame, 'd1', 100)
        frame = storage_write(state, frame, frame.a2+0xF0, 2, frame.d1)
        for displacement in (0x140,0x190):
            frame, value = storage_read_next(state, frame, 'a1', 2)
            frame = storage_write(state, frame, frame.a2+displacement, 2, value)
        frame = storage_address_step(frame, 'a2', 2)
        frame, again = storage_dbra(frame, 'd0')
        if not again:
            return frame


def stage_scaled_officer_parameter_words_frame_fields(state: StorageState,
                                                     frame: StorageFrame) -> StorageFrame:
    """Stage all 256 unsigned WORD parameters after original division by five."""
    frame = storage_entry(state, frame)
    frame = storage_address(frame, 'a1', 0xFFFFB800)
    frame = storage_address(frame, 'a2', 0xFFFFD300)
    frame = storage_move(state, frame, 'd0', 255, 16)
    while True:
        frame = storage_move(state, frame, 'd1', 0, 32)
        frame, value = storage_read_next(state, frame, 'a1', 2)
        frame = storage_move(state, frame, 'd1', value, 16)
        frame = storage_divide(state, frame, 'd1', 5)
        frame = storage_write_next(state, frame, 'a2', 2, frame.d1)
        frame, again = storage_dbra(frame, 'd0')
        if not again:
            return frame


def stage_saved_force_record_columns_frame_fields(state: StorageState,
                                                frame: StorageFrame) -> StorageFrame:
    """The actual caller supplies A1; split sixteen four-BYTE force records."""
    frame = storage_entry(state, frame)
    for role, address in (('a2',0xFFFFD300),('a3',0xFFFFD310),
                          ('a4',0xFFFFD320),('a5',0xFFFFD330)):
        frame = storage_address(frame, role, address)
    frame = storage_move(state, frame, 'd0', 15, 16)
    while True:
        for destination in ('a2','a3','a4','a5'):
            frame, value = storage_read_next(state, frame, 'a1', 1)
            frame = storage_write_next(state, frame, destination, 1, value)
        frame, again = storage_dbra(frame, 'd0')
        if not again:
            return frame


def write_saved_game_state(state: StorageState, entry_frame: StorageFrame=None) -> Long:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    returned = write_saved_game_state_frame_fields(state, frame)
    return returned.d1

def begin_saved_payload(state: StorageState, entry_frame: StorageFrame=None) -> Cursor:
    raise Boundary('legacy partial storage phase has no whole entry; use the full save or restore core')

def write_saved_membership_fields(state: StorageState, destination: Cursor, entry_frame: StorageFrame=None) -> None:
    raise Boundary('legacy partial storage phase has no whole entry; use the full save or restore core')

def write_saved_officer_fields(state: StorageState, destination: Cursor, entry_frame: StorageFrame=None) -> None:
    raise Boundary('legacy partial storage phase has no whole entry; use the full save or restore core')

def write_saved_city_fields(state: StorageState, destination: Cursor, entry_frame: StorageFrame=None) -> None:
    raise Boundary('legacy partial storage phase has no whole entry; use the full save or restore core')

def write_saved_order_columns(state: StorageState, destination: Cursor, entry_frame: StorageFrame=None) -> None:
    raise Boundary('legacy partial storage phase has no whole entry; use the full save or restore core')

def write_saved_force_and_battle_fields(state: StorageState, destination: Cursor, entry_frame: StorageFrame=None) -> None:
    raise Boundary('legacy partial storage phase has no whole entry; use the full save or restore core')

def stage_saved_officer_positions(state: StorageState, entry_frame: StorageFrame=None) -> None:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    returned = stage_saved_officer_positions_frame_fields(state, frame)
    return None

def stage_saved_city_orders(state: StorageState, entry_frame: StorageFrame=None) -> None:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    returned = stage_saved_city_orders_frame_fields(state, frame)
    return None

def stage_scaled_officer_parameter_words(state: StorageState, entry_frame: StorageFrame=None) -> None:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    returned = stage_scaled_officer_parameter_words_frame_fields(state, frame)
    return None

def stage_saved_force_record_columns(state: StorageState, context: SavedForceColumnContext, entry_frame: StorageFrame=None) -> Cursor:
    """Legacy projection of the sole complete core; explicit entry_frame is required."""
    frame = storage_legacy_entry(state, entry_frame)
    context.checked_for(state)
    if context.source.base != frame.a1:
        raise ValueError('save force source differs from complete entry A1')
    returned = stage_saved_force_record_columns_frame_fields(state, frame)
    context.source.base = returned.a1
    return context.source
