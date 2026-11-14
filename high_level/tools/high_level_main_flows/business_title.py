"""Title initialization and editable bitmap-to-tile scaling rules.

Pixel sources, palettes and layouts remain external live read-only views;
these functions contain only their original algorithms and transfer geometry.
"""

from .contexts_gameplay import FirstDeploymentFrame, FirstDeploymentReturnBoundary, MovementContinuationBoundary, first_replace
from .business_movement_support import (_movement_move, _movement_move_long,
    _movement_test, _movement_test_long, _movement_compare, _movement_add_word,
    _movement_binary_flags, _movement_arithmetic_long, _movement_divu_word,
    _movement_multiply_word, _movement_save_longs, _movement_restore_longs, _movement_shift_long)
from .domain import low8

from .domain import (SceneState, Cursor, Table, Long, Word, uint, checked_state,
    checked_cursor, checked_table, u16, u32, s16, low16, high16,
    replace_word, swap_words, divu_retained, descending_inclusive, ram_view,
    data_view, VideoPlaneAddress)
from .contexts_main import SceneTick, SoundWord, BitmapRow, BitmapTileResult
from .services import (call_target, clear_video_sprite_plane, enqueue_sound_command,
    write_vdp_swapped_byte_rle_stream, read_vdp_plane_rle_rows,
    read_vdp_plane_literal_rows, initialize_video_registers_and_planes)
from .services import (copy_scene_palette_variant,
    snapshot_and_clear_scene_palette, begin_scene_palette_darken)


def _ram(state, address):
    return ram_view(state, 'ram_%04x' % address)


def _begin_title_transfer(state, reset_scroll):
    """Incomplete legacy control entry cannot fabricate a full title-transfer frame."""
    entered=_title_frame_fields(state,FirstDeploymentFrame.unobserved(),0x3792)
    return _begin_title_transfer_fields(state,entered,reset_scroll,0x37BC)



def initialize_title_scene(state: SceneState, literal_marker: Long):
    """Historical projection: unavailable retained registers/CCR/SP are not invented."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=initialize_title_scene_fields(state,entered)
    return None


def initialize_title_scene_preserving_mode(state: SceneState, literal_marker: Long):
    """Historical projection: unavailable retained registers/CCR/SP are not invented."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=initialize_title_scene_preserving_mode_fields(state,entered)
    return None


def return_title_idle_slot(state: SceneState):
    """Historical projection: unavailable retained registers/CCR/SP are not invented."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=return_title_idle_slot_fields(state,entered)
    return None


def initialize_secondary_title_scene(state: SceneState):
    """Historical projection: unavailable retained registers/CCR/SP are not invented."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=initialize_secondary_title_scene_fields(state,entered)
    return None


def initialize_title_transition_scene(state: SceneState):
    """Historical projection: unavailable retained registers/CCR/SP are not invented."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=initialize_title_transition_scene_fields(state,entered)
    return None


def upload_title_emblem_set(state: SceneState, scale: Word):
    """Historical projection: unavailable retained registers/CCR/SP are not invented."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),unit=scale)
    returned=upload_title_emblem_set_fields(state,entered)
    return None


def scale_title_bitmap_to_tiles(state: SceneState, source: Table, destination: Cursor, source_height: Word, source_width: Word, output_height: Word):
    """Historical projection: unavailable retained registers/CCR/SP are not invented."""
    checked_state(state)
    checked_table(source,state)
    checked_cursor(destination,state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=source.cursor(),controller=state.table_at(destination.base),target_x=source_height,target_y=source_width,unit=output_height)
    returned=scale_title_bitmap_to_tiles_fields(state,entered)
    return None


def select_title_bitmap_scanline(state: SceneState, source: Table, source_height: Word, source_width: Word, vertical: Long) -> Table | None:
    """Historical projection: unavailable retained registers/CCR/SP are not invented."""
    checked_state(state)
    checked_table(source,state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=source.cursor(),target_x=source_height,target_y=source_width,distance=vertical)
    returned=select_title_bitmap_scanline_fields(state,entered)
    return None if returned.opponent.base & 2147483648 else returned.opponent


def pack_title_bitmap_tile_row(state: SceneState, row: BitmapRow, destination: Cursor) -> BitmapTileResult:
    """Historical projection: unavailable retained registers/CCR/SP are not invented."""
    checked_state(state)
    row.validate(state)
    checked_cursor(destination,state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),opponent=row.source,scan=destination, target_y=row.source_width,count=row.step,distance=row.vertical,offset_y=row.horizontal,choice=row.pending,offset_x=row.remaining)
    returned=pack_title_bitmap_tile_row_fields(state,entered)
    return BitmapTileResult(returned.offset_y,returned.choice)


def upload_title_bitmap_tile_rows(state: SceneState, source: Cursor, tile: Long):
    """Historical projection: unavailable retained registers/CCR/SP are not invented."""
    checked_state(state)
    checked_cursor(source,state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),controller=source,count=tile)
    returned=upload_title_bitmap_tile_rows_fields(state,entered)
    return None


"""Title control and monochrome bitmap scaling, with physical saved fields."""

def _title_frame_fields(state: SceneState, frame: FirstDeploymentFrame,
        entry: int) -> FirstDeploymentFrame:
    from ..high_level_remaining_flows.business_city import _resource_cost_frame
    return _resource_cost_frame(state, frame, entry)


def _title_write_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, value, size: int = 2, clear: bool = False) -> FirstDeploymentFrame:
    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
    from ..high_level_gameplay_flow.business_services import _scene_refresh_emit
    if size not in (1, 2, 4) or type(clear) is not bool:
        raise ValueError('actual title store width required')
    if clear:
        state.read(address, size)
    return _scene_refresh_emit(SceneRefreshMemory(state), frame, address, size, value)


def _title_shift_word_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, count: int, right: bool = False) -> FirstDeploymentFrame:
    from ..high_level_remaining_flows.business_highbank import _position_order_shift
    frame = _position_order_shift(frame, name, count, right)
    state.sr = (state.sr & 65504) | frame.status
    return frame


def _title_dbra_fields(frame: FirstDeploymentFrame, name: str) -> FirstDeploymentFrame:
    return first_replace(frame, **{name: replace_word(frame.carrier(name), u16(low16(frame.carrier(name)) - 1))})


def _title_child_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Parent owns its real BSR/JSR slot; callees never push it a second time."""
    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    if target == 0x3A5A:
        result = scale_title_bitmap_to_tiles_fields(state, entered)
    elif target == 0x3AA2:
        result = select_title_bitmap_scanline_fields(state, entered)
    elif target == 0x3AC0:
        result = pack_title_bitmap_tile_row_fields(state, entered)
    elif target == 0x3B02:
        result = upload_title_bitmap_tile_rows_fields(state, entered)
    elif target == 0x3A00:
        result = upload_title_emblem_set_fields(state, entered)
    elif target == 0x68CE:
        from ..high_level_gameplay_flow.business_services import clear_video_sprite_plane_fields
        result = clear_video_sprite_plane_fields(SceneRefreshMemory(state), entered)
    elif target == 0x6826:
        from ..high_level_gameplay_flow.business_services import initialize_video_registers_and_planes_fields
        result = initialize_video_registers_and_planes_fields(SceneRefreshMemory(state), entered)
    elif target == 0x3AB52:
        from ..high_level_scene_flows.business_scene import write_vdp_swapped_byte_rle_stream_fields
        result = write_vdp_swapped_byte_rle_stream_fields(SceneRefreshMemory(state), entered)
    elif target == 0x3AAB6:
        from .business_scene_support import decode_unmasked_literal_plane_fields
        result = decode_unmasked_literal_plane_fields(state, entered)
    elif target == 0x3AACE:
        from ..high_level_scene_flows.business_scene import read_vdp_plane_rle_rows_fields
        result = read_vdp_plane_rle_rows_fields(SceneRefreshMemory(state), entered)
    elif target == 0x3AB94:
        from ..high_level_scene_flows.business_scene import copy_scene_palette_variant_fields
        result = copy_scene_palette_variant_fields(SceneRefreshMemory(state), entered)
    elif target == 0x3AA8A:
        from ..high_level_scene_flows.business_scene import snapshot_and_clear_scene_palette_fields
        result = snapshot_and_clear_scene_palette_fields(SceneRefreshMemory(state), entered)
    elif target == 0x3AA20:
        from ..high_level_scene_flows.business_scene import begin_scene_palette_darken_fields
        result = begin_scene_palette_darken_fields(SceneRefreshMemory(state), entered)
    elif target == 0x808A:
        from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields
        result = enqueue_sound_command_fields(SceneRefreshMemory(state), entered)
    elif target == 0x8112:
        from ..high_level_gameplay_flow.business_services import copy_video_transfer_descriptor_fields
        result = copy_video_transfer_descriptor_fields(SceneRefreshMemory(state), entered)
    elif target == 0x353FC:
        from .business_scene_support import upload_glyph_tile_sequence_fields
        result = upload_glyph_tile_sequence_fields(state, entered)
    elif target == 0x355DA:
        from .business_scene_support import initialize_auxiliary_text_panel_fields
        result = initialize_auxiliary_text_panel_fields(state, entered)
    else:
        raise MovementContinuationBoundary(target, entered, 'actual title child/internal entry lacks a complete ABI')
    actual = result.stack_cursor.long()
    if actual != continuation:
        raise FirstDeploymentReturnBoundary(actual, result, continuation)
    return first_replace(result, stack_cursor=result.stack_cursor.advance(4))


def _begin_title_transfer_fields(state: SceneState, frame: FirstDeploymentFrame,
        reset_scroll: bool, continuation: int) -> FirstDeploymentFrame:
    """Actual full SR write and video-disable prefix, shared by three scenes."""
    if type(reset_scroll) is not bool:
        raise ValueError('actual title scroll-reset branch required')
    state.set_status_word(0x2700)
    frame = first_replace(frame, status=0)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF606, 2), 16)
    frame = _movement_move(state, frame, 'target_x', low8(frame.target_x) & 0xBF, 8)
    frame = _title_write_fields(state, frame, 0xC00004, low16(frame.target_x))
    if reset_scroll:
        frame = _movement_move(state, frame, 'target_x', 0, 16)
        for address in (0xFFFFF312, 0xFFFFF314, 0xFFFFF316, 0xFFFFF318):
            frame = _title_write_fields(state, frame, address, low16(frame.target_x))
    return _title_child_fields(state, frame, 0x68CE, continuation)


def initialize_title_scene_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3E0 BRA reaches 378E; 3E4 reaches 3792 without another CALL slot."""
    frame = _title_frame_fields(state, frame, 0x3E0)
    frame = _title_write_fields(state, frame, 0xFFFFF32E, 0, clear=True)
    return initialize_title_scene_preserving_mode_fields(state, frame)


def initialize_title_scene_preserving_mode_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _title_frame_fields(state, frame, 0x3E4)
    frame = _begin_title_transfer_fields(state, frame, True, 0x37BC)
    frame = _title_child_fields(state, frame, 0x6826, 0x37C2)
    frame = _title_write_fields(state, frame, 0xC00004, 0x60000002, 4)
    frame = first_replace(frame, scratch=state.table_at(0xC00000))
    frame = _movement_move(state, frame, 'offset_y', 0, 16)
    frame = _movement_move(state, frame, 'choice', 8191, 16)
    while True:
        frame = _title_write_fields(state, frame, frame.scratch.base, low16(frame.offset_y))
        frame = _title_dbra_fields(frame, 'choice')
        if low16(frame.choice) == 65535:
            break
    for command in (0x8F02, 0x8230, 0x8330, 0x8407, 0x855C, 0x8700,
            0x8B00, 0x8C81, 0x8D2F, 0x8F02, 0x9011, 0x9180, 0x9200):
        frame = _title_write_fields(state, frame, 0xC00004, command)
    for source_address, video_word, continuation in ((0x5D5E4, 0, 0x3858),
            (0x5F137, 0x2000, 0x3868), (0x60E6C, 0x4000, 0x3878),
            (0x6254F, 0x8000, 0x3888), (0x64340, 0xA000, 0x3898)):
        frame = first_replace(frame, roster=state.table_at(source_address).cursor())
        frame = _movement_move(state, frame, 'target_x', video_word, 16)
        frame = _title_child_fields(state, frame, 0x3AB52, continuation)
    frame = _title_write_fields(state, frame, 0xC00004, 0x8F02)
    frame = _title_write_fields(state, frame, 0xC00004, 0x6E000001, 4)
    frame = first_replace(frame, roster=state.table_at(0xD374A).cursor())
    frame = _movement_move(state, frame, 'target_x', 1023, 16)
    while True:
        value = frame.roster.long()
        frame = first_replace(frame, roster=frame.roster.advance(4))
        frame = _title_write_fields(state, frame, 0xC00000, value, 4)
        frame = _title_dbra_fields(frame, 'target_x')
        if low16(frame.target_x) == 65535:
            break
    frame = first_replace(frame, roster=state.table_at(0x655F1).cursor(), candidates=state.table_at(0xE000).cursor())
    frame = _movement_move_long(state, frame, 'offset_x', 128)
    frame = _movement_move(state, frame, 'offset_y', 32, 16)
    frame = _title_child_fields(state, frame, 0x3AAB6, 0x38DA)
    frame = first_replace(frame, roster=state.table_at(0x65DF3).cursor(), candidates=state.table_at(0xE040).cursor())
    frame = _movement_move_long(state, frame, 'offset_x', 128)
    frame = _title_child_fields(state, frame, 0x3AACE, 0x38F2)
    frame = _movement_move_long(state, frame, 'target_x', 17)
    frame = _title_child_fields(state, frame, 0x3AB94, 0x38FA)
    frame = _title_child_fields(state, frame, 0x3AA8A, 0x3900)
    for address in (0xFFFF80CA, 0xFFFF80CC, 0xFFFF80CE, 0xFFFF80D0):
        frame = _title_write_fields(state, frame, address, 65535)
    frame = _movement_move_long(state, frame, 'target_x', 1)
    frame = _title_child_fields(state, frame, 0x3AA20, 0x3920)
    frame = _title_write_fields(state, frame, 0xFFFFF32B, 0, 1, True)
    frame = _title_write_fields(state, frame, 0xFFFFF612, 0x300)
    frame = _movement_compare(state, frame, state.read(0xFFFFF600, 2), 16, 16)
    if not frame.status & 4:
        frame = _movement_move(state, frame, 'target_x', 0x81, 8)
        frame = _title_child_fields(state, frame, 0x808A, 0x393E)
        frame = _title_write_fields(state, frame, 0xFFFFF32C, 3)
    frame = _movement_move(state, frame, 'unit', state.read(0xFFFFF32C, 2), 16)
    frame = _title_child_fields(state, frame, 0x3A00, 0x394C)
    frame = _title_write_fields(state, frame, 0xFFFFF608, 4)
    state.set_status_word(0x2500)
    return first_replace(frame, status=0)


def return_title_idle_slot_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    checked_state(state)
    if type(frame) is not FirstDeploymentFrame:
        raise ValueError('actual title fields required')
    return frame.validate(state, False)


def initialize_secondary_title_scene_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _title_frame_fields(state, frame, 0x3EC)
    frame = _begin_title_transfer_fields(state, frame, True, 0x3B8E)
    for command in (0x8230, 0x8338, 0x8406, 0x855C):
        frame = _title_write_fields(state, frame, 0xC00004, command)
    frame = _movement_move_long(state, frame, 'target_x', 4)
    frame = _title_child_fields(state, frame, 0x8112, 0x3BB6)
    frame = _title_child_fields(state, frame, 0x353FC, 0x3BBC)
    for address, value, clear in ((0xFFFFF33E, 0xC17C, False), (0xFFFFF340, 0xC17C, False),
            (0xFFFFF33C, 1, False), (0xFFFFF342, 0, True), (0xFFFFF344, 0, True),
            (0xFFFFF346, 0xFE10, False), (0xFFFFF32E, 0, True)):
        frame = _title_write_fields(state, frame, address, value, 2, clear)
    frame = _title_write_fields(state, frame, 0xFFFFF32B, 0, 1, True)
    frame = _title_write_fields(state, frame, 0xFFFFF608, 4)
    frame = _title_write_fields(state, frame, 0xFFFFF612, 0x303)
    state.set_status_word(0x2500)
    return first_replace(frame, status=0)


def _title_increment_word_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int) -> FirstDeploymentFrame:
    previous = state.read(address, 2)
    frame, value = _movement_binary_flags(state, frame, previous, 1, 16)
    state.write(address, 2, value)
    return frame


def initialize_title_transition_scene_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _title_frame_fields(state, frame, 0x3F0)
    frame = _begin_title_transfer_fields(state, frame, False, 0x3C0E)
    for command in (0x8230, 0x8338, 0x8406, 0x855C):
        frame = _title_write_fields(state, frame, 0xC00004, command)
    frame = _title_child_fields(state, frame, 0x355DA, 0x3C34)
    frame = _title_increment_word_fields(state, frame, 0xFFFFF348)
    frame = _title_write_fields(state, frame, 0xFFFFF316, 0, clear=True)
    frame = _movement_move(state, frame, 'target_x', 15, 16)
    frame = first_replace(frame, roster=state.table_at(0xFFFFFB00).cursor())
    while True:
        frame = _title_write_fields(state, frame, frame.roster.base, 0, 4, True)
        frame = first_replace(frame, roster=frame.roster.advance(4))
        frame = _title_dbra_fields(frame, 'target_x')
        if low16(frame.target_x) == 65535:
            break
    frame = _title_increment_word_fields(state, frame, 0xFFFFF31E)
    frame = _title_increment_word_fields(state, frame, 0xFFFFF34C)
    frame = _title_write_fields(state, frame, 0xFFFFF32E, 0, clear=True)
    frame = _title_write_fields(state, frame, 0xFFFFF32B, 0, 1, True)
    frame = _title_write_fields(state, frame, 0xFFFFF608, 4)
    state.set_status_word(0x2500)
    return first_replace(frame, status=0)


def upload_title_emblem_set_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3A00: seven descriptor-driven emblems; physical eight-LONG MOVEM."""
    frame = _title_frame_fields(state, frame, 0x3A00)
    saved = ('target_x', 'target_y', 'unit', 'count', 'offset_x', 'roster', 'candidates', 'controller')
    frame = _movement_save_longs(state, frame, saved)
    frame = first_replace(frame, roster=state.table_at(0x3A3E).cursor())
    frame = _movement_move(state, frame, 'count', 0x300, 16)
    frame = _movement_move(state, frame, 'offset_x', 6, 16)
    while True:
        pointer = frame.roster.long()
        frame = first_replace(frame, candidates=state.table_at(pointer).cursor(), roster=frame.roster.advance(4), controller=state.table_at(0xFFFFD100))
        frame = _movement_move(state, frame, 'target_x', 32, 16)
        frame = _movement_move(state, frame, 'target_y', 32, 16)
        frame = _title_child_fields(state, frame, 0x3A5A, 0x3A24)
        frame = first_replace(frame, controller=state.table_at(0xFFFFD100))
        frame = _title_child_fields(state, frame, 0x3B02, 0x3A2E)
        frame = _movement_add_word(state, frame, 'count', 16)
        frame = _title_dbra_fields(frame, 'offset_x')
        if low16(frame.offset_x) == 65535:
            return _movement_restore_longs(state, frame, saved)


def scale_title_bitmap_to_tiles_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3A5A: fixed-point resampling; one scanline selector and one eight-pixel packer."""
    frame = _title_frame_fields(state, frame, 0x3A5A)
    saved = ('target_x', 'target_y', 'unit', 'count', 'distance', 'offset_x', 'offset_y', 'choice',
        'roster', 'candidates', 'controller', 'scan', 'opponent', 'scratch', 'auxiliary')
    frame = _movement_save_longs(state, frame, saved)
    frame = _movement_move_long(state, frame, 'count', 0)
    frame = _movement_move(state, frame, 'count', low16(frame.target_y), 16)
    frame = _title_shift_word_fields(state, frame, 'count', 8)
    frame = _movement_divu_word(state, frame, 'count', low16(frame.unit), 0x3A64)
    frame = _movement_move_long(state, frame, 'count', frame.count & 65535)
    frame = _movement_shift_long(state, frame, 'count')
    frame = _movement_move(state, frame, 'unit', low16(frame.target_x), 16)
    frame = _movement_move_long(state, frame, 'distance', 0)
    while True:
        frame = _movement_move(state, frame, 'offset_x', low16(frame.target_y), 16)
        frame = _movement_move_long(state, frame, 'offset_y', 0)
        frame = first_replace(frame, scan=state.table_at(frame.controller.base).cursor())
        frame = _title_child_fields(state, frame, 0x3AA2, 0x3A7C)
        frame = _movement_save_longs(state, frame, ('target_x', 'unit'))
        while True:
            frame = _title_child_fields(state, frame, 0x3AC0, 0x3A84)
            frame, value = _movement_binary_flags(state, frame, low16(frame.offset_x), 8, 16, True)
            frame = first_replace(frame, offset_x=replace_word(frame.offset_x, value))
            if frame.status & 5:
                break
            frame = first_replace(frame, scan=frame.scan.advance(128))
        frame = _movement_restore_longs(state, frame, ('target_x', 'unit'))
        frame = _movement_arithmetic_long(state, frame, 'distance', frame.count)
        frame, value = _movement_binary_flags(state, frame, low16(frame.unit), 1, 16, True)
        frame = first_replace(frame, unit=replace_word(frame.unit, value))
        if frame.status & 4:
            return _movement_restore_longs(state, frame, saved)
        frame = first_replace(frame, controller=frame.controller.advance(4))


def select_title_bitmap_scanline_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _title_frame_fields(state, frame, 0x3AA2)
    frame = _movement_move(state, frame, 'choice', low16(frame.target_y), 16)
    frame = _title_shift_word_fields(state, frame, 'choice', 3, True)
    frame = _movement_move_long(state, frame, 'distance', swap_words(frame.distance))
    frame = _movement_compare(state, frame, low16(frame.distance), low16(frame.target_x), 16)
    if not frame.status & 1:
        frame = first_replace(frame, opponent=state.table_at(0xFFFFFFFF))
        return _movement_move_long(state, frame, 'distance', swap_words(frame.distance))
    frame = _movement_multiply_word(state, frame, 'choice', low16(frame.distance))
    frame = _movement_move_long(state, frame, 'distance', swap_words(frame.distance))
    return first_replace(frame, opponent=state.table_at(u32(frame.candidates.base + s16(low16(frame.choice)))))


def pack_title_bitmap_tile_row_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3AC0: byte bit index becomes eight four-bit pixels, with real WORD/LONG saves."""
    from ..high_level_remaining_flows.business_city import _special_action_shift_long
    frame = _title_frame_fields(state, frame, 0x3AC0)
    frame = _movement_move_long(state, frame, 'target_x', frame.opponent.base)
    if frame.status & 8:
        frame = _movement_move_long(state, frame, 'choice', 0)
        return _title_write_fields(state, frame, frame.scan.base, frame.choice, 4)
    stack = frame.stack_cursor.advance(-4)
    frame = _title_write_fields(state, frame, stack.base, frame.offset_x, 4)
    frame = first_replace(frame, stack_cursor=stack)
    frame = _movement_move(state, frame, 'target_x', 7, 16)
    while True:
        frame = _special_action_shift_long(state, frame, 'choice', 4)
        frame = _movement_move_long(state, frame, 'offset_y', swap_words(frame.offset_y))
        frame = _movement_compare(state, frame, low16(frame.offset_y), low16(frame.target_y), 16)
        if not frame.status & 1:
            frame = _movement_move(state, frame, 'offset_x', 0, 8)
        else:
            stack = frame.stack_cursor.advance(-2)
            frame = _title_write_fields(state, frame, stack.base, low16(frame.target_x))
            frame = first_replace(frame, stack_cursor=stack)
            frame = _movement_move(state, frame, 'offset_x', low16(frame.offset_y), 16)
            frame = _title_shift_word_fields(state, frame, 'offset_x', 3, True)
            frame = _movement_move(state, frame, 'offset_x', frame.opponent.byte(low16(frame.offset_x)), 8)
            frame = _movement_move(state, frame, 'target_x', low16(frame.offset_y), 16)
            frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 7, 16)
            bit = frame.target_x & 31
            status = (frame.status & 27) | (0 if frame.offset_x & (1 << bit) else 4)
            state.sr = (state.sr & 65504) | status
            frame = first_replace(frame, status=status)
            if not frame.status & 4:
                frame = _movement_move(state, frame, 'choice', low16(frame.choice) | 15, 16)
            restored = frame.stack_cursor.word()
            frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))
            frame = _movement_move(state, frame, 'target_x', restored, 16)
        frame = _movement_move_long(state, frame, 'offset_y', swap_words(frame.offset_y))
        frame = _movement_arithmetic_long(state, frame, 'offset_y', frame.count)
        frame = _title_dbra_fields(frame, 'target_x')
        if low16(frame.target_x) == 65535:
            break
    restored = frame.stack_cursor.long()
    frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(4))
    frame = _movement_move_long(state, frame, 'offset_x', restored)
    return _title_write_fields(state, frame, frame.scan.base, frame.choice, 4)


def upload_title_bitmap_tile_rows_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3B02: 256 real video WORDs; preserve D3/D7/A2 through physical MOVEM."""
    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
    from ..high_level_scene_flows.business_scene import _glyph_shift_long_fields
    frame = _title_frame_fields(state, frame, 0x3B02)
    saved = ('count', 'choice', 'controller')
    frame = _movement_save_longs(state, frame, saved)
    frame = _glyph_shift_long_fields(SceneRefreshMemory(state), frame, 'count', 7)
    frame = _movement_move_long(state, frame, 'count', frame.count & 0x3FF80)
    frame = _title_shift_word_fields(state, frame, 'count', 2, True)
    frame = _movement_move(state, frame, 'count', low16(frame.count) | 0x4000, 16)
    frame = _movement_move_long(state, frame, 'count', swap_words(frame.count))
    frame = _title_write_fields(state, frame, 0xC00004, frame.count, 4)
    frame = _movement_move(state, frame, 'choice', 255, 16)
    while True:
        value = frame.controller.word()
        frame = first_replace(frame, controller=frame.controller.advance(2))
        frame = _title_write_fields(state, frame, 0xC00000, value)
        frame = _title_dbra_fields(frame, 'choice')
        if low16(frame.choice) == 65535:
            break
    frame = _title_write_fields(state, frame, 0xFFFFD100, 0, clear=True)
    return _movement_restore_longs(state, frame, saved)
