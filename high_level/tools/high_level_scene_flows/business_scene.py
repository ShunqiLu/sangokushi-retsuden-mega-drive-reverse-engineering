"""Scripted scenes, live glyph expansion, palettes and VDP/sprite streams.

This module expresses scene operations rather than executing instruction
records. Original width, ordered DATA, partial writes, inclusive repeats and
nonlocal completion are retained. All media and hardware are supplied inputs.
"""
from dataclasses import replace
from .domain import (SceneState, Table, Cursor, Byte, Word, Long, Boundary,
    VideoPlaneAddress, StackContinuation, checked_state, checked_table,
    checked_cursor, uint, u8, u16, u32, s16, low8, low16, high16,
    replace_byte, replace_word, swap_words, negative_word,
    descending_inclusive)
from .contexts_scene import (VdpPacketResult, VdpStreamResult,
    SwappedByteRleRetained, SwappedByteRleObservation, SwappedByteRleResult,
    DictionaryStreamResult, GlyphRowsResult, PaletteComponentResult,
    PaletteTransformResult, PaletteCopyResult, PaletteCopyFields,
    PaletteCopyCompleteResult, PaletteSnapshotResult,
    PlaneRowContext, PlaneRowResult, PlaneStreamResult, SceneFrameResult,
    ScenePlaybackResult, PacketTransferValues,
    checked_context)
from .contexts_reuse import GlyphSavedValues
from .contexts_objects import (SceneRenderFrame, SpriteBatchResult,
    SceneControllerFrame, SceneControllerConditions, checked_controller_frame)


from .contexts_scene import SceneRefreshMemory, SceneRefreshBoundary, FirstDeploymentFrame, first_replace, _first_word, _first_byte, _first_long, _first_shift_word, _scene_refresh_emit, _scene_refresh_flags, _scene_refresh_decrement, _movement_compare, _movement_binary_flags

def _ram(state, low):
    return state.table('ram_' + low)


def _word_shift(carrier, amount):
    return replace_word(carrier, u16(low16(carrier) << amount))


def _ror_word(carrier, amount):
    value = low16(carrier)
    return replace_word(carrier, u16(value >> amount | value << (16 - amount)))


def _rol_word(carrier, amount):
    value = low16(carrier)
    return replace_word(carrier, u16(value << amount | value >> (16 - amount)))


def _video_address(value):
    if type(value) is not VideoPlaneAddress:
        raise ValueError('explicit video-plane address required')
    value.__post_init__()
    return value


def flush_scene_transfer_queue(state: SceneState,
        values: PacketTransferValues | None = None) -> VdpPacketResult | None:
    """Historical four values cannot supply the actual queue caller's full ABI."""
    checked_state(state)
    frame=FirstDeploymentFrame.unobserved()
    if values is not None:
        if type(values) is not PacketTransferValues:
            raise ValueError('actual packet flush values required')
        values.validate()
        frame=first_replace(frame,target_x=values.command,target_y=values.increment,
            unit=values.address,count=values.spill)
    flush_scene_transfer_queue_fields(SceneRefreshMemory(state),frame)
    # The honest partial-frame adapter stops before mutation; there is no
    # invented full stack, retained value or false completed packet result.
    raise SceneRefreshBoundary(0xAD06,frame,None)





def write_vdp_packet_stream(state: SceneState, source: Cursor,
        values: PacketTransferValues | None = None) -> VdpPacketResult:
    """Historical observed carriers project the sole AD1C field core."""
    checked_state(state)
    checked_cursor(source,state)
    frame = first_replace(FirstDeploymentFrame.unobserved(),roster=source.advance(0))
    if values is None:
        raise SceneRefreshBoundary(0xAD1C,frame,None)
    if type(values) is not PacketTransferValues:
        raise ValueError('actual packet stream values required')
    values.validate()
    frame = first_replace(frame,target_x=values.command,target_y=values.increment,
        unit=values.address,count=values.spill)
    frame = write_vdp_packet_stream_fields(SceneRefreshMemory(state),frame)
    source.base = frame.roster.base
    values = PacketTransferValues(frame.target_x,frame.target_y,frame.unit,frame.count).validate()
    return VdpPacketResult(source,frame.unit,low16(frame.target_y),values)


def write_vdp_dictionary_repeat_stream(state: SceneState, source: Cursor,
        dictionary: Table, remaining: Word) -> DictionaryStreamResult:
    """Historical three observations project the sole full ADFC core."""
    checked_state(state)
    checked_cursor(source,state)
    checked_table(dictionary,state)
    uint(remaining,16)
    frame = first_replace(FirstDeploymentFrame.unobserved(),
        target_x=remaining,roster=source.advance(0),candidates=dictionary.cursor())
    frame = write_vdp_dictionary_repeat_stream_fields(SceneRefreshMemory(state),frame)
    source.base = frame.roster.base
    return DictionaryStreamResult(source,frame.controller,low16(frame.target_x))


def decode_glyph_rows_to_buffers(state: SceneState, source: Cursor, destination: Cursor,
        background: Long, foreground: Long, remaining: Long, saved: GlyphSavedValues | None = None) -> GlyphRowsResult:
    """Historical glyph observations project the sole AE8A fields; no full A7 claim."""
    from .business_reuse import _save_glyph_values, _restore_glyph_values
    checked_state(state)
    checked_cursor(source,state)
    checked_cursor(destination,state)
    for value in (background,foreground,remaining):
        uint(value,32)
    if saved is not None:
        _save_glyph_values(state,saved,True)
    frame = first_replace(FirstDeploymentFrame.unobserved(),target_x=background,target_y=foreground,
        count=remaining,roster=source.advance(0),candidates=destination.advance(0))
    actual = decode_glyph_rows_to_buffers_fields(SceneRefreshMemory(state),frame)
    source.base,destination.base = actual.roster.base,actual.candidates.base
    if saved is not None:
        saved = _restore_glyph_values(state,saved,saved.glyph_source,True)
    return GlyphRowsResult(source,destination,actual.count,actual.target_x,actual.target_y,saved)


def darken_palette_component(state: SceneState, shade: Long, color: Long,
        accumulated: Long, component: Long = 0) -> PaletteComponentResult:
    """Legacy observations project the sole channel rule; no invented original X."""
    checked_state(state)
    for value in (shade,color,accumulated,component):
        uint(value,32)
    frame=first_replace(FirstDeploymentFrame.unobserved(),target_x=shade,unit=color,
        count=component,distance=accumulated)
    frame=darken_palette_component_fields(SceneRefreshMemory(state),frame)
    return PaletteComponentResult(frame.unit,frame.distance,frame.count).validate(state)


def darken_palette(state: SceneState, shade: Long, count: Word,
        source: Cursor, accumulator: Long = 0, *, count_carrier: Long | None = None,
        color: Long = 0, component: Long = 0) -> PaletteTransformResult:
    """Legacy projection of one live conversion; missing actual SP/X stays a boundary."""
    checked_state(state)
    checked_cursor(source,state)
    for value in (shade,accumulator,color,component):
        uint(value,32)
    uint(count,16)
    if count_carrier is not None:
        uint(count_carrier,32)
        if low16(count_carrier)!=count:
            raise ValueError('palette count must agree with actual caller')
    frame=first_replace(FirstDeploymentFrame.unobserved(),target_x=shade,target_y=count_carrier,
        unit=color,count=component,distance=accumulator,roster=source.advance(0))
    frame=darken_palette_fields(SceneRefreshMemory(state),frame)
    source.base=frame.roster.base
    return PaletteTransformResult(source,frame.candidates,frame.target_x,frame.distance,
        frame.target_y,frame.unit,frame.count).validate(state)


def set_vram_write_address(state: SceneState, address: VideoPlaneAddress) -> Long:
    """Historical video-address projection of the sole3B2B0 field core."""
    checked_state(state)
    address = _video_address(address)
    frame = first_replace(FirstDeploymentFrame.unobserved(),target_x=address.carrier)
    return set_vram_write_address_fields(SceneRefreshMemory(state),frame).target_x


def _set_vram_write_address_frame(state: SceneState,
        current: SceneControllerFrame, address: VideoPlaneAddress,
        continuation: Long) -> SceneControllerFrame:
    """One3B2B0 encoding algorithm with the real caller BSR and D1 save.

    The physical save slot is read back after the VDP write. It may alias
    caller data or hardware; retaining the old D1 by assumption is invalid.
    The ordinary return reads its real slot; an alias that changes that
    target cannot silently continue along the known caller body.
    """
    current = checked_controller_frame(current, state)
    _video_address(address)
    uint(continuation, 32)
    stack = current.stack.advance(-4)
    stack.set_long(0, continuation)
    stack = stack.advance(-4)
    stack.set_long(0, current.y)
    command = set_vram_write_address(state, address)
    secondary = stack.long()
    stack = _scene_return_to_known_caller(state, stack.advance(4), continuation)
    return replace(current, x=command, y=secondary, stack=stack,
        conditions=SceneControllerConditions(False, command == 0,
                                             bool(command & 0x80000000), False))


def _scene_return_to_known_caller(state: SceneState, stack: Cursor,
        continuation: Long) -> Cursor:
    """One real RTS read; unknown alias-changed PC is an explicit boundary."""
    checked_cursor(stack, state)
    uint(continuation, 32)
    target = stack.long()
    if target != continuation:
        raise Boundary('live stack changed the known ordinary continuation')
    return stack.advance(4)


def write_vdp_word_rle_stream(state: SceneState, source: Cursor, video_address: VideoPlaneAddress) -> VdpStreamResult:
    checked_state(state)
    checked_cursor(source,state)
    video_address = _video_address(video_address)
    frame = first_replace(FirstDeploymentFrame.unobserved(),roster=source.advance(0),target_x=video_address.carrier)
    result = write_vdp_word_rle_stream_fields(SceneRefreshMemory(state),frame)
    source.base = result.roster.base
    return VdpStreamResult(source,video_address,result.target_x)


def _write_vdp_swapped_byte_rle_core(state: SceneState, source: Cursor,
        video_address: VideoPlaneAddress,
        current: SceneControllerFrame | None = None) -> SwappedByteRleObservation:
    """Historical observations project one decoder; no alternate RLE loop."""
    checked_state(state)
    checked_cursor(source,state)
    _video_address(video_address)
    if current is None:
        frame = first_replace(FirstDeploymentFrame.unobserved(),
            roster=source.advance(0),target_x=video_address.carrier)
    else:
        from .business_objects import _scene_controller_legacy_fields
        frame = _scene_controller_legacy_fields(state,current)
    result,marker,token,last_word = _write_vdp_swapped_byte_rle_fields_core(SceneRefreshMemory(state),frame)
    source.base = result.roster.base
    live = None
    if current is not None:
        from .business_objects import _scene_controller_legacy_projection
        live = _scene_controller_legacy_projection(state,result)
    return SwappedByteRleObservation(source,video_address,result.target_x,marker,token,last_word,live)


def write_vdp_swapped_byte_rle_stream(state: SceneState, source: Cursor,
        video_address: VideoPlaneAddress) -> VdpStreamResult:
    """Legacy three-field projection of the same 3AB52 decoder."""
    actual = _write_vdp_swapped_byte_rle_core(state, source, video_address)
    return VdpStreamResult(actual.source, actual.video_address, actual.command_carrier)


def write_vdp_swapped_byte_rle_stream_complete(state: SceneState, source: Cursor,
        video_address: VideoPlaneAddress, retained: SwappedByteRleRetained) -> SwappedByteRleResult:
    """Actual retained D1/D2/D4 project the same sole BYTE decoder."""
    checked_state(state)
    checked_cursor(source,state)
    _video_address(video_address)
    if type(retained) is not SwappedByteRleRetained:
        raise ValueError('actual partial-write observations required')
    retained.validate()
    frame = first_replace(FirstDeploymentFrame.unobserved(),roster=source.advance(0),
        target_x=video_address.carrier,unit=retained.token,distance=retained.packed_word)
    result,marker,token,last_word = _write_vdp_swapped_byte_rle_fields_core(SceneRefreshMemory(state),frame)
    source.base = result.roster.base
    # Final MOVEQ0/MOVE.B0 defines NZVC without claiming unobserved X/SP.
    return SwappedByteRleResult(source,video_address,result.target_x,
        replace_byte(retained.marker,marker),result.unit,result.count,result.distance,
        last_word,False,True,False,False)


def write_vdp_swapped_byte_rle_stream_frame(state: SceneState,
        frame: SceneControllerFrame) -> SceneControllerFrame:
    """3AB52 consumes D0's address, not A1; return every current operand.

    A1/A2..A6 and D5..D7 are untouched. Source and stack are shared live
    cursors, including aliases into the original D1 save slots.
    """
    frame = checked_controller_frame(frame, state)
    actual = _write_vdp_swapped_byte_rle_core(state, frame.source,
                                            VideoPlaneAddress(frame.x), frame)
    if actual.live is None:
        raise Boundary('complete swapped stream must return actual current operands')
    return actual.live.validate(state)


def advance_plane_row(state: SceneState, context: PlaneRowContext,
        current: SceneControllerFrame | None = None) -> PlaneRowResult:
    """Old word observations cannot fabricate an actual row entry stack/X."""
    checked_context(context,PlaneRowContext,state)
    if current is None:
        frame = first_replace(FirstDeploymentFrame.unobserved(),target_x=context.command_carrier,
            candidates=SceneRefreshMemory(state).cursor_at(context.video_address.carrier),offset_x=context.row_stride)
    else:
        from .business_objects import _scene_controller_legacy_fields
        frame = _scene_controller_legacy_fields(state,current)
    result,discarded = advance_plane_row_fields(SceneRefreshMemory(state),frame)
    live = None
    if current is not None:
        from .business_objects import _scene_controller_legacy_projection
        live = _scene_controller_legacy_projection(state,result)
    return PlaneRowResult(VideoPlaneAddress(result.candidates.base),low16(result.distance),
        low16(result.offset_y),result.target_x,discarded,live)


def read_vdp_plane_rle_rows(state: SceneState, source: Cursor,
        video_address: VideoPlaneAddress, row_stride: Long) -> PlaneStreamResult:
    """3AACE: live row decoder with the final-row nonlocal return preserved."""
    return _read_vdp_plane_rle_rows_core(state, source, video_address, row_stride)


def _read_vdp_plane_rle_rows_core(state: SceneState, source: Cursor,
        video_address: VideoPlaneAddress, row_stride: Long,
        current: SceneControllerFrame | None = None) -> PlaneStreamResult:
    """Old scalar/NZVC contract projects sole core or reports missing entry."""
    checked_state(state)
    checked_cursor(source,state)
    _video_address(video_address)
    uint(row_stride,32)
    if current is None:
        frame = first_replace(FirstDeploymentFrame.unobserved(),roster=source.advance(0),
            candidates=SceneRefreshMemory(state).cursor_at(video_address.carrier),offset_x=row_stride)
    else:
        from .business_objects import _scene_controller_legacy_fields
        frame = _scene_controller_legacy_fields(state,current)
        if frame.offset_x != row_stride:
            raise ValueError('actual live plane stride required')
    result,discarded = _read_vdp_plane_rle_rows_fields_core(SceneRefreshMemory(state),frame)
    source.base = result.roster.base
    live = None
    if current is not None:
        from .business_objects import _scene_controller_legacy_projection
        live = _scene_controller_legacy_projection(state,result)
    return PlaneStreamResult(source,VideoPlaneAddress(result.candidates.base),result.target_x,
        low16(result.distance),low16(result.offset_y),discarded,live)


def read_vdp_plane_rle_rows_frame(state: SceneState,
        frame: SceneControllerFrame) -> SceneControllerFrame:
    """Complete3AACE: actual A1 video address, full D5 stride and current rows."""
    frame = checked_controller_frame(frame, state)
    if type(frame.destination) is not VideoPlaneAddress:
        raise Boundary('3AACE requires the actual current A1 video address before DATA')
    actual = _read_vdp_plane_rle_rows_core(state, frame.source,
                                         frame.destination, frame.extent, frame)
    if actual.live is None:
        raise Boundary('complete plane stream must return actual current operands')
    return actual.live.validate(state)


def copy_scene_palette_variant(state: SceneState, variant: Long) -> PaletteCopyResult:
    """Legacy four-field observation of the same unique 3AB94 transaction."""
    fields = _copy_scene_palette_variant_fields(state, variant, None)
    return PaletteCopyResult(fields.index_carrier, fields.source,
        fields.destination, fields.directory).validate(state)


def _copy_scene_palette_variant_fields(state: SceneState, variant: Long,
        count_carrier: Long | None) -> PaletteCopyFields:
    checked_state(state)
    uint(variant,32)
    if count_carrier is not None:
        uint(count_carrier,32)
    frame = first_replace(FirstDeploymentFrame.unobserved(),target_x=variant,choice=count_carrier)
    frame,pair = _copy_scene_palette_variant_fields_core(SceneRefreshMemory(state),frame)
    return PaletteCopyFields(frame.target_x,frame.controller,frame.scan,frame.candidates,frame.choice,pair).validate(state)


def copy_scene_palette_variant_complete(state: SceneState, variant: Long,
                                        count_carrier: Long) -> PaletteCopyCompleteResult:
    """Strict current D7 and actual final MOVE.L observations, not default CCR."""
    uint(count_carrier, 32)
    fields = _copy_scene_palette_variant_fields(state, variant, count_carrier)
    return PaletteCopyCompleteResult(fields.index_carrier, fields.source,
        fields.destination, fields.directory, fields.count_carrier, False,
        fields.last_color_pair == 0, bool(fields.last_color_pair & 2147483648),
        False).validate(state)


def _begin_scene_palette_darken_core(state: SceneState, value: Long) -> tuple[Long, Word]:
    checked_state(state)
    uint(value,32)
    frame,shade = _begin_scene_palette_darken_fields_core(SceneRefreshMemory(state),
        first_replace(FirstDeploymentFrame.unobserved(),target_x=value))
    # Final store is observed by the sole algorithm, not reread from mutable RAM.
    return frame.target_x,shade


def begin_scene_palette_darken(state: SceneState, value: Long) -> Long:
    """3AA20: latch the BYTE period and initialize the descending shade."""
    value, shade = _begin_scene_palette_darken_core(state, value)
    return value


def begin_scene_palette_darken_frame(state: SceneState,
        frame: SceneControllerFrame) -> SceneControllerFrame:
    from .business_objects import _scene_controller_legacy_fields, _scene_controller_legacy_projection
    fields = begin_scene_palette_darken_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,frame))
    return _scene_controller_legacy_projection(state,fields)


def snapshot_and_clear_scene_palette(state: SceneState) -> PaletteSnapshotResult:
    checked_state(state)
    frame = snapshot_and_clear_scene_palette_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())
    return PaletteSnapshotResult(frame.roster,frame.candidates)


def snapshot_and_clear_scene_palette_frame(state: SceneState,
        frame: SceneControllerFrame) -> SceneControllerFrame:
    from .business_objects import _scene_controller_legacy_fields, _scene_controller_legacy_projection
    fields = snapshot_and_clear_scene_palette_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,frame))
    return _scene_controller_legacy_projection(state,fields)


def fade_palette_component(state: SceneState, color: Long, accumulated: Long,
        component: Long = 0) -> PaletteComponentResult:
    """The legacy three observations project the sole actual component core."""
    actual = fade_palette_component_fields(SceneRefreshMemory(state),
        first_replace(FirstDeploymentFrame.unobserved(),count=color,distance=component,offset_x=accumulated))
    return PaletteComponentResult(actual.count,actual.offset_x,actual.distance).validate(state)


def advance_scene_palette_fade(state: SceneState, retained: Long = 0) -> Long:
    """3A978: advance the fade and visit each of the two live mask LONGs."""
    return _advance_scene_palette_fade_core(state, retained)


def _scene_logic_conditions(value, width):
    value &= (1 << width) - 1
    return SceneControllerConditions(False, value == 0,
                                      bool(value & (1 << (width - 1))), False)


def _scene_subtract_conditions(left, right, width):
    mask, sign = (1 << width) - 1, 1 << (width - 1)
    left, right = left & mask, right & mask
    difference = (left - right) & mask
    return SceneControllerConditions(left < right, difference == 0,
        bool(difference & sign), bool((left ^ right) & (left ^ difference) & sign))


def _advance_scene_palette_fade_core(state: SceneState, retained: Long,
        current: SceneControllerFrame | None = None) -> Long | SceneControllerFrame:
    """Legacy projection; unobserved partial color highs/SP remain a true boundary."""
    from .business_objects import _scene_controller_legacy_fields,_scene_controller_legacy_projection
    checked_state(state)
    uint(retained,32)
    fields = (first_replace(FirstDeploymentFrame.unobserved(),target_x=retained) if current is None
        else _scene_controller_legacy_fields(state,current))
    actual = advance_scene_palette_fade_fields(SceneRefreshMemory(state),fields)
    return actual.target_x if current is None else _scene_controller_legacy_projection(state,actual)


def advance_scene_palette_fade_frame(state: SceneState,
        frame: SceneControllerFrame) -> SceneControllerFrame:
    frame = checked_controller_frame(frame, state)
    actual = _advance_scene_palette_fade_core(state, frame.x, frame)
    if type(actual) is not SceneControllerFrame:
        raise Boundary('complete palette fade requires actual current operands')
    return actual.validate(state)


def sample_random_preserving_seed_carrier(state: SceneState) -> Long:
    """Legacy scalar projection: SP/D1 were never observed by this API."""
    checked_state(state)
    return sample_random_preserving_seed_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved()).target_x


def sample_random_preserving_seed_frame(state: SceneState,
        frame: SceneControllerFrame) -> SceneControllerFrame:
    """Legacy NZVC-only input cannot supply the complete entry CCR/X."""
    from .business_objects import _scene_controller_legacy_fields, _scene_controller_legacy_projection
    fields = sample_random_preserving_seed_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,frame))
    return _scene_controller_legacy_projection(state,fields)


def finish_one_scene_sprite_chain(state: SceneState, heads: Table, layer: Word, next_link: Long) -> Long:
    checked_state(state)
    checked_table(heads,state)
    uint(layer,16)
    uint(next_link,32)
    frame = first_replace(FirstDeploymentFrame.unobserved(),roster=heads.cursor(),target_x=layer,target_y=next_link)
    return finish_one_scene_sprite_chain_fields(SceneRefreshMemory(state),frame).target_y


def clear_scene_sprite_chain_heads(state: SceneState) -> Long:
    checked_state(state)
    return clear_scene_sprite_chain_heads_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved()).target_x


def finish_scene_sprite_chains(state: SceneState) -> Long:
    checked_state(state)
    return finish_scene_sprite_chains_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved()).target_x


def finish_one_actor_sprite_chain(state: SceneState, heads: Table,
        layer: Word, next_link: Long,
        current: SceneControllerFrame | None = None) -> Long | SceneControllerFrame:
    checked_state(state)
    checked_table(heads,state)
    uint(layer,16)
    uint(next_link,32)
    if current is None:
        # A WORD layer alone does not observe the unchanged upper D0 half.
        fields = first_replace(FirstDeploymentFrame.unobserved(),roster=heads.cursor(),target_y=next_link)
    else:
        from .business_objects import _scene_controller_legacy_fields
        fields = _scene_controller_legacy_fields(state,current)
        fields = first_replace(fields,roster=heads.cursor(),target_x=replace_word(fields.target_x,layer),target_y=next_link)
    actual = finish_one_actor_sprite_chain_fields(SceneRefreshMemory(state),fields)
    if current is None:
        return actual.target_y
    from .business_objects import _scene_controller_legacy_projection
    return _scene_controller_legacy_projection(state,actual)


def finish_actor_sprite_chains(state: SceneState) -> Long:
    """3B23C: join actor layers, then clear the heads without clearing tails."""
    return _finish_actor_sprite_chains_core(state)


def _finish_actor_sprite_chains_core(state: SceneState,
        current: SceneControllerFrame | None = None) -> Long | SceneControllerFrame:
    checked_state(state)
    if current is None:
        fields = FirstDeploymentFrame.unobserved()
    else:
        from .business_objects import _scene_controller_legacy_fields
        fields = _scene_controller_legacy_fields(state,current)
    actual = finish_actor_sprite_chains_fields(SceneRefreshMemory(state),fields)
    if current is None:
        return actual.target_x
    from .business_objects import _scene_controller_legacy_projection
    return _scene_controller_legacy_projection(state,actual)


def finish_actor_sprite_chains_frame(state: SceneState,
        frame: SceneControllerFrame) -> SceneControllerFrame:
    frame = checked_controller_frame(frame, state)
    actual = _finish_actor_sprite_chains_core(state, frame)
    if type(actual) is not SceneControllerFrame:
        raise Boundary('complete actor chains require actual current operands')
    return actual.validate(state)




def _append_scene_sprites(state, source, frame, clipped):
    """Five genuine old render observations project the sole sprite packet loop."""
    checked_state(state)
    checked_cursor(source,state)
    if type(frame) is not SceneRenderFrame:
        raise ValueError('explicit scene render operands required')
    frame.validate(state)
    partial = first_replace(FirstDeploymentFrame.unobserved(),target_x=frame.x,
        target_y=frame.y,unit=frame.attributes,count=frame.palette,distance=frame.tile,
        roster=source.advance(0))
    actual = _append_scene_sprite_fields(SceneRefreshMemory(state),partial,clipped)
    source.base = actual.roster.base
    return SpriteBatchResult(source,SceneRenderFrame(actual.target_x,actual.target_y,
        actual.unit,actual.count,actual.distance))


def append_clipped_scene_sprites(state: SceneState, source: Cursor,
        frame: SceneRenderFrame) -> SpriteBatchResult:
    """3A5A0: append with live X/Y clipping and partial rejected writes."""
    return _append_scene_sprites(state, source, frame, True)


def append_unclipped_scene_sprites(state: SceneState, source: Cursor,
        frame: SceneRenderFrame) -> SpriteBatchResult:
    """3A7A2: independent nonclipping entry, sharing only semantic helpers."""
    return _append_scene_sprites(state, source, frame, False)


def append_scene_marker_sprite(state: SceneState, x: Long, y: Long) -> SpriteBatchResult:
    checked_state(state)
    uint(x,32)
    uint(y,32)
    partial = first_replace(FirstDeploymentFrame.unobserved(),target_x=x,target_y=y,distance=0)
    actual = append_scene_marker_sprite_fields(SceneRefreshMemory(state),partial)
    return SpriteBatchResult(actual.roster,SceneRenderFrame(actual.target_x,actual.target_y,
        actual.unit,actual.count,actual.distance))


def update_scripted_scene_position(state: SceneState) -> None:
    checked_state(state)
    update_scripted_scene_position_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def initialize_scripted_secondary_position(state: SceneState, mode: Word) -> None:
    """Original WORD-only API projects the latch core without inventing D0 high."""
    checked_state(state)
    uint(mode,16)
    initialize_scripted_secondary_position_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved(),mode)


def select_scene_object_frame(state: SceneState, frame_offset: Long, tick_carrier: Long = 0) -> SceneFrameResult:
    """Two historical numeric observations, not a fabricated complete entry."""
    checked_state(state)
    uint(frame_offset,32)
    uint(tick_carrier,32)
    partial = first_replace(FirstDeploymentFrame.unobserved(),target_x=tick_carrier,target_y=frame_offset)
    actual = select_scene_object_frame_fields(SceneRefreshMemory(state),partial)
    return SceneFrameResult(actual.roster,actual.target_y)


def _copy_scene_palette_longs(state, source):
    partial = first_replace(FirstDeploymentFrame.unobserved(),roster=source.advance(0))
    actual = _copy_scene_palette_longs_fields(SceneRefreshMemory(state),partial)
    source.base = actual.roster.base


def _copy_scene_palette_words(state, source):
    partial = first_replace(FirstDeploymentFrame.unobserved(),roster=source.advance(0))
    actual = _copy_scene_palette_words_fields(SceneRefreshMemory(state),partial)
    source.base = actual.roster.base








def _draw_scripted_sequence(state):
    """Historical unobserved entry projects the one sequence core honestly."""
    _draw_scripted_sequence_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def _draw_scripted_arrival(state):
    _draw_scripted_arrival_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def _draw_scripted_paired_positions(state):
    _draw_scripted_paired_positions_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def _draw_scripted_staged_pair(state):
    _draw_scripted_staged_pair_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def _draw_scripted_landing(state):
    _draw_scripted_landing_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def _draw_scripted_wave(state):
    _draw_scripted_wave_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def _draw_scripted_late_palette(state):
    _draw_scripted_late_palette_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def _draw_scripted_three_frame_stage(state):
    _draw_scripted_three_frame_stage_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def _draw_scripted_high_mode(state):
    _draw_scripted_high_mode_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def _draw_scripted_scene_frame(state):
    _draw_scripted_scene_frame_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def play_scripted_scene(state: SceneState) -> ScenePlaybackResult:
    """Historical result projects one actual initialization/play algorithm."""
    checked_state(state)
    frame = _play_scripted_scene_core(state,FirstDeploymentFrame.unobserved())
    return ScenePlaybackResult(frame.target_x,frame.target_y)

def _scene_render_compare(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, left, right, width) -> FirstDeploymentFrame:
    if frame.status is None:
        return frame
    if width == 32:
        retained_x = frame.status & 16
        frame, difference = _movement_binary_flags(memory.state, frame, left, right, 32, True)
        return memory.sync_status(first_replace(frame, status=(frame.status & 15) | retained_x))
    return _movement_compare(memory.state,frame,left,right,width)

def _scene_render_bit(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, value, mask) -> FirstDeploymentFrame:
    status = None if frame.status is None else ((frame.status & 27) | (0 if value & mask else 4))
    return memory.sync_status(first_replace(frame,status=status))

def _scene_render_arithmetic(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, left, right, width, subtract=False) -> FirstDeploymentFrame:
    frame,value = _movement_binary_flags(memory.state,frame,left,right,width,subtract)
    original = frame.carrier(name)
    if width == 8:
        carrier = None if original is None else replace_byte(original,value)
    elif width == 16:
        carrier = None if original is None else replace_word(original,value)
    else:
        carrier = value
    return first_replace(frame,**{name:carrier})

def _scene_render_asl_word(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, original: Word | None, count: Word) -> FirstDeploymentFrame:
    """True ASL.W, including transient sign changes in V; no LONG cleanup."""
    if not 1 <= count <= 8:
        raise ValueError('actual bounded scene ASL.W required')
    if original is None:
        return first_replace(frame,**{name:None},status=None)
    uint(original,16)
    result = original
    overflow = False
    for index in range(count):
        old_sign = bool(result & 32768)
        result = u16(result << 1)
        overflow = overflow or old_sign != bool(result & 32768)
    carry = bool(original & (1 << (16 - count)))
    retained = frame.carrier(name)
    frame = first_replace(frame,**{name:None if retained is None else replace_word(retained,result)},
        status=(17 if carry else 0) | (2 if overflow else 0) | (8 if result & 32768 else 0) | (4 if result == 0 else 0))
    return memory.sync_status(frame)

def _scene_render_push_longs(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, values: tuple) -> FirstDeploymentFrame:
    if frame.stack_cursor is None:
        return frame
    stack = frame.stack_cursor
    for value in values:
        stack = stack.advance(-4)
        stack.set_long(0,value)
    return first_replace(frame,stack_cursor=stack)

def _scene_render_restore_sprite(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    if frame.stack_cursor is None:
        return frame
    stack = frame.stack_cursor
    extent,row_count,destination = stack.long(),stack.long(4),stack.long(8)
    return first_replace(frame,offset_x=extent,offset_y=row_count,
        candidates=memory.cursor_at(destination),stack_cursor=stack.advance(12))

def _scene_render_save_clip(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    if frame.stack_cursor is None:
        return frame
    return _scene_render_push_longs(memory,frame,(
        frame.scan.base,frame.controller.base,frame.candidates.base,frame.roster.base,
        frame.choice,frame.offset_y,frame.offset_x,frame.distance,
        frame.count,frame.unit,frame.target_y,frame.target_x))

def _scene_render_restore_clip(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    if frame.stack_cursor is None:
        return frame
    stack = frame.stack_cursor
    values = tuple(stack.long(index * 4) for index in range(12))
    return first_replace(frame,target_x=values[0],target_y=values[1],unit=values[2],
        count=values[3],distance=values[4],offset_x=values[5],offset_y=values[6],choice=values[7],
        roster=memory.cursor_at(values[8]),candidates=memory.cursor_at(values[9]),
        controller=memory.cursor_at(values[10]),scan=memory.cursor_at(values[11]),
        stack_cursor=stack.advance(48))

def _scene_render_call_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long, video: Word | None = None) -> FirstDeploymentFrame:
    """Only real known renderer children, with parent-owned outer LONGs."""
    memory.frame(frame)
    if (target,continuation) not in (
        (0x3A75E,0x396A6),(0x39658,0x39772),(0x39658,0x397A2),
        (0x3B2B0,0x39664),(0x3B2B0,0x3AAE8),(0x3B2B0,0x3AB4E),(0x3B2B0,0x3AB5E),(0x3A72E,0x39800),(0x399D8,0x39AB6),
        (0x3A5A0,0x39AFC),(0x3A74E,0x39B02),(0x3A78C,0x3A75A),
        (0x399d8,0x39894),(0x3a5a0,0x398c4),(0x3a5a0,0x39912),(0x3a74e,0x39918),(0x3a7a2,0x39b54),(0x3a7a2,0x39b70),(0x3a5a0,0x39bae),(0x3a7a2,0x39c7c),(0x399d8,0x39c92),(0x3a5a0,0x39cb2),(0x3a7a2,0x39d2c),(0x399d8,0x39d32),(0x3a5a0,0x39d64),(0x399d8,0x39d96),(0x3a5a0,0x39db4),(0x3a7a2,0x39e18),(0x3a5a0,0x3a26e),(0x3a7a2,0x3a2d6),(0x399d8,0x3a326),(0x3a5a0,0x3a344),(0x3a7a2,0x3a3ac),(0x3a7a2,0x3a42c),(0x3a7a2,0x3a458),(0x399d8,0x3a45e),(0x3a5a0,0x3a47c),(0x3a7a2,0x3a4a4),(0x3a7a2,0x3a4c0),(0x3a7a2,0x3a4e8),(0x3a7a2,0x3a504),(0x3a7a2,0x3a52c),(0x3a7a2,0x3a1d2),(0x3a7a2,0x3a1b2),
        (0x399d8,0x39e4e),(0x3a5a0,0x39e6c),(0x39f18,0x39ea2),(0x399d8,0x39ebc),(0x3a5a0,0x39eda),(0x3a08a,0x39f74),(0x3a7a2,0x39f8a),(0x399d8,0x39f9c),(0x3a08a,0x39fa2),(0x3a5a0,0x39fbc),(0x399d8,0x3a012),(0x3a08a,0x3a018),(0x3a5a0,0x3a032)):
        raise ValueError('actual renderer child and return token required')
    memory.sync_status(frame)
    entered = frame
    if frame.stack_cursor is not None:
        stack = frame.stack_cursor.advance(-4)
        stack.set_long(0,continuation)
        entered = first_replace(frame,stack_cursor=stack)
    if target == 0x3A75E:
        result = clear_scene_sprite_chain_heads_fields(memory,entered)
    elif target == 0x39658:
        result = write_vdp_word_rle_stream_fields(memory,entered,video)
    elif target == 0x3B2B0:
        result = set_vram_write_address_fields(memory,entered,video)
    elif target == 0x3A72E:
        result = append_scene_marker_sprite_fields(memory,entered)
    elif target == 0x399D8:
        result = update_scripted_scene_position_fields(memory,entered)
    elif target == 0x3A5A0:
        result = append_clipped_scene_sprites_fields(memory,entered)
    elif target == 0x3A7A2:
        result = append_unclipped_scene_sprites_fields(memory,entered)
    elif target == 0x39F18:
        result = initialize_scripted_secondary_position_fields(memory,entered)
    elif target == 0x3A08A:
        result = select_scene_object_frame_fields(memory,entered)
    elif target == 0x3A74E:
        result = finish_scene_sprite_chains_fields(memory,entered)
    else:
        result = finish_one_scene_sprite_chain_fields(memory,entered)
    memory.frame(result)
    if frame.stack_cursor is not None:
        actual = result.stack_cursor.long()
        if actual != continuation:
            raise SceneRefreshBoundary(target,result,continuation)
        result = first_replace(result,stack_cursor=result.stack_cursor.advance(4))
    return memory.sync_status(result)

def set_vram_write_address_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, address: Word | None = None) -> FirstDeploymentFrame:
    """3B2B0 sole encoding math, genuine D1 LONG save/read, real shift X."""
    memory.frame(frame)
    if address is None:
        if frame.target_x is None:
            raise SceneRefreshBoundary(0x3B2B0,frame,None)
        address = low16(frame.target_x)
    uint(address,16)
    if frame.target_x is not None and low16(frame.target_x) != address:
        raise ValueError('observed scene video WORD must agree with current D0')
    if frame.stack_cursor is not None:
        frame = _scene_render_push_longs(memory,frame,(frame.target_y,))
    frame = _first_long(frame,'target_x',address)
    frame = _first_long(frame,'target_y',address)
    command = swap_words((address & 0x3FFF) | 0x4000) | (address >> 14)
    # LSR.W8 then LSR.W6 defines X from bit13; final OR/MOVE preserve it.
    status = (16 if address & 0x2000 else 0) | (8 if command & 0x80000000 else 0) | (4 if command == 0 else 0)
    frame = first_replace(frame,target_x=command,status=status)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,command)
    if frame.stack_cursor is not None:
        restored = frame.stack_cursor.long()
        frame = first_replace(frame,target_y=restored,stack_cursor=frame.stack_cursor.advance(4))
    else:
        # The old scalar frontend never observed the preserved D1 at entry.
        frame = first_replace(frame,target_y=None)
    return memory.sync_status(frame)

def write_vdp_word_rle_stream_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, video: Word | None = None) -> FirstDeploymentFrame:
    """39658 unique literal/repeat decoder, including all BYTE partial writes."""
    memory.frame(frame)
    frame = _scene_refresh_emit(memory,frame,0xC00004,2,0x8F02)
    frame = _scene_render_call_fields(memory,frame,0x3B2B0,0x39664,video)
    source = frame.roster
    marker = source.byte()
    frame = first_replace(frame,roster=source.advance(1))
    frame = _first_byte(frame,'target_y',marker)
    while True:
        high = frame.roster.byte()
        frame = first_replace(frame,roster=frame.roster.advance(1))
        frame = _first_byte(frame,'unit',high)
        frame = _scene_render_compare(memory,frame,marker,high,8)
        if marker != high:
            low = frame.roster.byte()
            frame = first_replace(frame,roster=frame.roster.advance(1))
            frame = _first_byte(frame,'distance',low)
            original = None if frame.unit is None else low16(frame.unit)
            frame = _scene_render_asl_word(memory,frame,'unit',original,8)
            frame = _first_byte(frame,'unit',low)
            frame = _scene_refresh_emit(memory,frame,0xC00000,2,high << 8 | low)
        else:
            frame = _first_long(frame,'count',0)
            counter = frame.roster.byte()
            frame = first_replace(frame,roster=frame.roster.advance(1))
            frame = _first_byte(frame,'count',counter)
            if counter == 0:
                return memory.sync_status(frame)
            high = frame.roster.byte()
            frame = first_replace(frame,roster=frame.roster.advance(1))
            frame = _first_byte(frame,'distance',high)
            low = frame.roster.byte()
            frame = first_replace(frame,roster=frame.roster.advance(1))
            frame = _first_byte(frame,'unit',low)
            original = None if frame.distance is None else low16(frame.distance)
            frame = _scene_render_asl_word(memory,frame,'distance',original,8)
            frame = _first_byte(frame,'distance',low)
            while True:
                frame = _scene_refresh_emit(memory,frame,0xC00000,2,high << 8 | low)
                frame = _scene_refresh_decrement(frame,'count',counter)
                counter = u16(counter - 1)
                if counter == 65535:
                    break

def clear_scene_sprite_chain_heads_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3A75E genuine eight heads, D0/A0, and BYTE count clear; no tail clear."""
    memory.frame(frame)
    frame = first_replace(frame,roster=memory.cursor_at(0xFF7006))
    frame = _first_long(frame,'target_x',0)
    for offset in range(0,32,4):
        frame = _scene_refresh_emit(memory,frame,frame.roster.base + offset,4,0)
    return _scene_refresh_emit(memory,frame,0xFFFFF300,1,0)

def finish_one_scene_sprite_chain_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    layer = low16(frame.target_x)
    value = frame.roster.long(layer)
    frame = _scene_refresh_flags(memory,frame,value,4)
    if value != 0:
        frame = first_replace(frame,candidates=memory.cursor_at(frame.roster.long(layer,0x40)))
        frame = _scene_refresh_emit(memory,frame,frame.candidates.base + 3,1,low8(frame.target_y))
        frame = _first_byte(frame,'target_y',frame.roster.byte(layer,0x20))
    return memory.sync_status(frame)

def finish_scene_sprite_chains_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    frame = _first_long(frame,'target_x',28)
    frame = _first_long(frame,'target_y',0)
    frame = first_replace(frame,roster=memory.cursor_at(0xFF7006))
    while True:
        frame = _scene_render_call_fields(memory,frame,0x3A78C,0x3A75A)
        previous = low16(frame.target_x)
        frame = _scene_render_arithmetic(memory,frame,'target_x',previous,4,16,True)
        if frame.status & 8:
            return clear_scene_sprite_chain_heads_fields(memory,frame)

def _copy_scene_palette_longs_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    frame = first_replace(frame,candidates=memory.cursor_at(0xFFFFFB00))
    count = 8
    frame = _first_long(frame,'target_x',count - 1)
    for index in range(count):
        value = frame.roster.long()
        source = frame.roster.advance(4)
        destination = frame.candidates
        frame = first_replace(frame,roster=source,candidates=destination.advance(4))
        frame = _scene_refresh_emit(memory,frame,destination.base,4,value)
        frame = _scene_refresh_decrement(frame,'target_x',count - 1 - index)
    return frame

def _scene_render_clip_axis(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, address: Long, maximum: Word) -> tuple:
    """Original12-LONG clip save/RMW/restore; live slots can really alias."""
    saved = frame
    frame = _scene_render_save_clip(memory,frame)
    coordinate = memory.state.read(address,2)
    frame = _first_word(frame,'target_x',coordinate)
    delta = low8(frame.offset_x)
    frame = _scene_render_bit(memory,frame,frame.offset_x,128)
    if delta & 128:
        frame = _scene_render_arithmetic(memory,frame,'offset_x',0,delta,8,True)
        frame = _scene_render_arithmetic(memory,frame,'target_x',coordinate,low16(frame.offset_x),16,True)
    else:
        frame = _scene_render_arithmetic(memory,frame,'target_x',coordinate,low16(frame.offset_x),16)
    projected = low16(frame.target_x)
    frame = _scene_render_compare(memory,frame,projected,16,16)
    rejected = projected < 16
    if not rejected:
        frame = _scene_render_compare(memory,frame,projected,maximum,16)
        rejected = projected > maximum
    if rejected:
        frame = _scene_refresh_emit(memory,frame,0xFF7030,2,1)
    if frame.stack_cursor is not None:
        frame = _scene_render_restore_clip(memory,frame)
    else:
        # This partial projection preserves observed operands only, not a stack.
        frame = first_replace(saved,status=frame.status)
    value = memory.state.read(0xFF7030,2)
    frame = _scene_refresh_flags(memory,frame,value,2)
    return frame,value != 0

def _scene_render_apply_delta(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, flip_mask: Long, extent: Word) -> tuple:
    """Original BYTE negation order and WORD adjustment of the current extent."""
    frame = _scene_render_bit(memory,frame,frame.unit,flip_mask)
    if frame.unit & flip_mask:
        frame = _scene_render_arithmetic(memory,frame,'offset_x',0,low8(frame.offset_x),8,True)
    frame = _scene_render_bit(memory,frame,frame.offset_x,128)
    if frame.offset_x & 128:
        frame = _scene_render_arithmetic(memory,frame,'offset_x',0,low8(frame.offset_x),8,True)
        delta = low16(frame.offset_x)
        return _scene_render_arithmetic(memory,frame,'offset_y',extent,delta,16,True),u16(extent - delta)
    delta = low16(frame.offset_x)
    return _scene_render_arithmetic(memory,frame,'offset_y',extent,delta,16),u16(extent + delta)

def _append_scene_sprite_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, clipped: bool) -> FirstDeploymentFrame:
    """Sole3A5A0/3A7A2 packet loop, including both physical clipping saves."""
    memory.frame(frame)
    if type(clipped) is not bool:
        raise ValueError('actual scene clipping entry required')
    if frame.stack_cursor is not None:
        frame = _scene_render_push_longs(memory,frame,(frame.candidates.base,frame.offset_y,frame.offset_x))
    original = frame
    count = memory.state.read(0xFFFFF300,1)
    frame = _scene_render_compare(memory,frame,count,128,8)
    if count >= 128:
        return memory.sync_status(_scene_render_restore_sprite(memory,frame))
    frame = _first_long(frame,'distance',frame.distance & 65535)
    frame = _first_word(frame,'choice',low16(frame.unit))
    frame = _first_word(frame,'unit',low16(frame.unit) & 0xFFF8)
    frame = _first_word(frame,'choice',low16(frame.choice) & 7 if frame.choice is not None else low16(original.unit) & 7)
    layer = (low16(original.unit) & 7) << 2
    frame = _scene_render_asl_word(memory,frame,'choice',low16(original.unit) & 7,2)
    frame = _scene_render_arithmetic(memory,frame,'target_x',low16(frame.target_x),128,16)
    if frame.target_x & 32768:
        return memory.sync_status(_scene_render_restore_sprite(memory,frame))
    frame = _scene_render_bit(memory,frame,frame.unit,32)
    if frame.unit & 32:
        frame = _scene_render_arithmetic(memory,frame,'target_x',low16(frame.target_x),8,16,True)
    frame = _scene_render_arithmetic(memory,frame,'target_y',low16(frame.target_y),128,16)
    frame = _scene_render_bit(memory,frame,frame.unit,16)
    if frame.unit & 16:
        frame = _scene_render_arithmetic(memory,frame,'target_y',low16(frame.target_y),8,16,True)
    frame = _first_word(frame,'offset_x',0)
    count = memory.state.read(0xFFFFF300,1)
    frame = _first_byte(frame,'offset_x',count)
    frame = _first_shift_word(frame,'offset_x',count,3)
    frame = first_replace(frame,candidates=memory.cursor_at(0xFFFFF800,count << 3),controller=memory.cursor_at(0xFF7006))
    while True:
        # Both encoded backedges return to MOVE.W D0,D6, before the token read.
        frame = _first_word(frame,'offset_y',low16(frame.target_x))
        extent_word = low16(frame.target_x)
        if clipped:
            memory.state.read(0xFF7030,2)
            frame = _scene_refresh_emit(memory,frame,0xFF7030,2,0)
        frame = _first_long(frame,'offset_x',0)
        horizontal = frame.roster.byte()
        frame = _first_byte(frame,'offset_x',horizontal)
        frame = _scene_render_compare(memory,frame,horizontal,128,8)
        if horizontal == 128:
            break
        rejected = False
        if clipped:
            frame,rejected = _scene_render_clip_axis(memory,frame,0xFF7028,112)
        if not rejected:
            extent = extent_word if frame.offset_y is None else low16(frame.offset_y)
            frame,coordinate = _scene_render_apply_delta(memory,frame,32,extent)
            extent_word = coordinate
            frame = _scene_refresh_emit(memory,frame,frame.candidates.base,2,coordinate)
            frame = _first_word(frame,'offset_y',low16(frame.target_y))
            extent_word = low16(frame.target_y)
            frame = _first_byte(frame,'offset_x',frame.roster.byte(0,3))
            if clipped:
                memory.state.read(0xFF7030,2)
                frame = _scene_refresh_emit(memory,frame,0xFF7030,2,0)
                frame,rejected = _scene_render_clip_axis(memory,frame,0xFF702A,160)
            if not rejected:
                extent = extent_word if frame.offset_y is None else low16(frame.offset_y)
                frame,coordinate = _scene_render_apply_delta(memory,frame,16,extent)
                extent_word = coordinate
                frame = _scene_refresh_emit(memory,frame,frame.candidates.base + 6,2,coordinate)
                frame = _scene_refresh_emit(memory,frame,frame.candidates.base + 2,1,frame.roster.byte(0,1))
                if frame.choice is not None:
                    layer = low16(frame.choice)
                value = frame.controller.long(layer)
                frame = _scene_refresh_flags(memory,frame,value,4)
                if value == 0:
                    frame = _scene_refresh_emit(memory,frame,frame.controller.base + s16(layer),4,frame.candidates.base)
                    frame = _scene_refresh_emit(memory,frame,frame.controller.base + s16(layer) + 0x20,1,memory.state.read(0xFFFFF300,1))
                else:
                    frame = first_replace(frame,scan=memory.cursor_at(frame.controller.long(layer,0x40)))
                    frame = _scene_refresh_emit(memory,frame,frame.scan.base + 3,1,memory.state.read(0xFFFFF300,1))
                frame = _scene_refresh_emit(memory,frame,frame.controller.base + s16(layer) + 0x40,4,frame.candidates.base)
                count = memory.state.read(0xFFFFF300,1)
                frame,new_count = _movement_binary_flags(memory.state,frame,count,1,8)
                memory.state.write(0xFFFFF300,1,new_count)
                frame = _first_byte(frame,'offset_x',frame.roster.byte(0,1))
                encoded = low16(frame.offset_x) & 240
                frame = _first_word(frame,'offset_x',encoded)
                frame = _scene_render_arithmetic(memory,frame,'offset_x',low8(frame.offset_x),low8(frame.count),8)
                frame = _first_word(frame,'offset_x',low16(frame.offset_x) ^ low16(frame.unit))
                frame = _scene_render_asl_word(memory,frame,'offset_x',low16(frame.offset_x),7)
                frame = _first_byte(frame,'offset_x',low8(frame.offset_x) | frame.roster.byte(0,2))
                frame = _scene_render_arithmetic(memory,frame,'offset_x',low16(frame.offset_x),low16(frame.distance),16)
                frame = _scene_refresh_emit(memory,frame,frame.candidates.base + 4,2,low16(frame.offset_x))
                frame = first_replace(frame,candidates=frame.candidates.advance(8))
        frame = first_replace(frame,roster=frame.roster.advance(4))
        count = memory.state.read(0xFFFFF300,1)
        frame = _scene_render_compare(memory,frame,count,128,8)
        if count >= 128:
            break
    if frame.stack_cursor is not None:
        frame = _scene_render_restore_sprite(memory,frame)
    else:
        frame = first_replace(frame,offset_x=original.offset_x,offset_y=original.offset_y,candidates=original.candidates)
    return memory.sync_status(frame)

def append_clipped_scene_sprites_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _append_scene_sprite_fields(memory,frame,True)

def append_unclipped_scene_sprites_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _append_scene_sprite_fields(memory,frame,False)

def append_scene_marker_sprite_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _scene_render_arithmetic(memory,frame,'target_x',low16(frame.target_x),64,16,True)
    frame = _scene_render_arithmetic(memory,frame,'target_y',low16(frame.target_y),64,16,True)
    frame = _first_long(frame,'unit',0)
    frame = _first_long(frame,'count',0)
    frame = _first_word(frame,'distance',0)
    frame = first_replace(frame,roster=memory.cursor_at(0x3A748))
    return append_clipped_scene_sprites_fields(memory,frame)

def update_scripted_scene_position_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """399D8 sole tick/direction math; MOVEM.W restoration sign-extends D1."""
    memory.frame(frame)
    if frame.stack_cursor is not None:
        stack = frame.stack_cursor.advance(-2)
        stack.set_word(0,low16(frame.target_y))
        frame = first_replace(frame,stack_cursor=stack)
    saved = frame.target_y
    tick = memory.state.read(0xFFFFF320,2)
    frame = _first_word(frame,'offset_y',tick)
    frame = _first_word(frame,'offset_y',tick & 7)
    if tick & 7 == 0:
        movement = memory.state.read(0xFF702C,1)
        frame = _scene_refresh_flags(memory,frame,movement,1)
        if movement != 0:
            previous = memory.state.read(0xFF702E,2)
            frame,travelled = _movement_binary_flags(memory.state,frame,previous,1,16)
            memory.state.write(0xFF702E,2,travelled)
            mode = memory.state.read(0xFF7026,2)
            frame = _first_word(frame,'target_x',mode)
            frame = first_replace(frame,opponent=memory.cursor_at(0x39A82))
            limit = frame.opponent.byte(mode)
            frame = _first_byte(frame,'target_y',limit)
            travelled = memory.state.read(0xFF702E,2)
            frame = _first_word(frame,'choice',travelled)
            frame = _scene_render_compare(memory,frame,low8(travelled),limit,8)
            within_limit = not (low8(travelled) > limit)
            if within_limit:
                frame = _first_long(frame,'target_x',0)
                movement = memory.state.read(0xFF702C,1)
                frame = _first_byte(frame,'target_x',movement)
                for mask,address,subtract in ((16,0xFF7028,True),(32,0xFF7028,False),(64,0xFF702A,True),(128,0xFF702A,False)):
                    frame = _scene_render_bit(memory,frame,movement,mask)
                    if movement & mask:
                        frame = _first_word(frame,'target_y',low16(frame.target_x))
                        distance = movement & 15
                        frame = _first_long(frame,'target_y',distance)
                        previous = memory.state.read(address,2)
                        frame,value = _movement_binary_flags(memory.state,frame,previous,distance,16,subtract)
                        memory.state.write(address,2,value)
                        break
    if frame.stack_cursor is not None:
        saved = u32(s16(frame.stack_cursor.word()))
        frame = first_replace(frame,stack_cursor=frame.stack_cursor.advance(2))
    elif saved is not None:
        saved = u32(s16(low16(saved)))
    return memory.sync_status(first_replace(frame,target_y=saved))

def _play_scripted_scene_core(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3969A unique setup/play loop; remaining mode bodies stay explicit."""
    memory = SceneRefreshMemory(state)
    memory.frame(frame)
    frame = memory.status_word(frame,0x2700)
    state.read(0xFFFFF612,2)
    frame = _scene_refresh_emit(memory,frame,0xFFFFF612,2,0)
    frame = _scene_render_call_fields(memory,frame,0x3A75E,0x396A6)
    for address,size in ((0xFF702E,4),(0xFF703A,4),(0xFF7000,2),(0xFF7004,2),(0xFF703E,2),(0xFF7036,2),(0xFF7044,2),(0xFF703C,2)):
        state.read(address,size)
        frame = _scene_refresh_emit(memory,frame,address,size,0)
    mode = state.read(0xFF7026,2)
    frame = _scene_render_compare(memory,frame,mode,24,16)
    if mode == 24:
        secondary_x,secondary_y = 96,48
    else:
        mode = state.read(0xFF7026,2)
        frame = _scene_render_compare(memory,frame,mode,28,16)
        if mode == 28:
            secondary_x,secondary_y = 96,48
        else:
            secondary_x,secondary_y = 144,96
    frame = _scene_refresh_emit(memory,frame,0xFF7032,2,secondary_x)
    frame = _scene_refresh_emit(memory,frame,0xFF7034,2,secondary_y)
    mode = state.read(0xFF7026,2)
    frame = _first_word(frame,'target_x',mode)
    frame = _scene_render_asl_word(memory,frame,'target_x',mode,1)
    offset = u16(mode << 1)
    frame = first_replace(frame,roster=memory.cursor_at(0x38B88),candidates=memory.cursor_at(0x38BD8))
    x = frame.roster.word(offset)
    frame = _first_word(frame,'target_y',x)
    y = frame.candidates.word(offset)
    frame = _first_word(frame,'unit',y)
    frame = _scene_refresh_emit(memory,frame,0xFF7028,2,x)
    frame = _scene_refresh_emit(memory,frame,0xFF702A,2,y)
    mode = state.read(0xFF7026,2)
    frame = _first_word(frame,'target_x',mode)
    frame = first_replace(frame,roster=memory.cursor_at(0x38E50))
    movement = frame.roster.byte(mode)
    frame = _first_byte(frame,'target_y',movement)
    frame = _scene_refresh_emit(memory,frame,0xFF702C,1,movement)
    frame = _first_word(frame,'target_x',0)
    mode = state.read(0xFF7026,2)
    frame = _scene_render_compare(memory,frame,mode,10,16)
    video = 0
    if mode == 10:
        video = 8192
        frame = _first_word(frame,'target_x',video)
    mode = state.read(0xFF7026,2)
    frame = _first_word(frame,'count',mode)
    frame = _scene_render_asl_word(memory,frame,'count',mode,2)
    frame = first_replace(frame,candidates=memory.cursor_at(0x387BA))
    frame = first_replace(frame,roster=memory.cursor_at(frame.candidates.long(u16(mode << 2))))
    frame = _scene_render_call_fields(memory,frame,0x39658,0x39772,video)
    mode = state.read(0xFF7026,2)
    frame = _first_word(frame,'target_x',mode)
    frame = first_replace(frame,auxiliary=memory.cursor_at(0x3899A))
    dual = frame.auxiliary.byte(mode)
    frame = _first_byte(frame,'target_y',dual)
    frame = _scene_render_compare(memory,frame,dual,1,8)
    if dual == 1:
        mode = state.read(0xFF7026,2)
        frame = _first_word(frame,'count',mode)
        frame = _scene_render_arithmetic(memory,frame,'count',mode,1,16)
        frame = _scene_render_asl_word(memory,frame,'count',u16(mode + 1),2)
        frame = first_replace(frame,candidates=memory.cursor_at(0x387BA))
        frame = first_replace(frame,roster=memory.cursor_at(frame.candidates.long(u16(u16(mode + 1) << 2))))
        frame = _first_word(frame,'target_x',8192)
        frame = _scene_render_call_fields(memory,frame,0x39658,0x397A2,8192)
    mode = state.read(0xFF7026,2)
    frame = _first_word(frame,'count',mode)
    frame = _scene_render_asl_word(memory,frame,'count',mode,2)
    frame = first_replace(frame,candidates=memory.cursor_at(0x388FA))
    frame = first_replace(frame,roster=memory.cursor_at(frame.candidates.long(u16(mode << 2))))
    frame = _copy_scene_palette_longs_fields(memory,frame)
    frame = _first_long(frame,'target_x',0)
    frame = memory.status_word(frame,0x2500)
    while True:
        frame = _scene_refresh_emit(memory,frame,0xFFFFF612,2,1536)
        while True:
            value = state.read(0xFFFFF612,1)
            frame = _scene_refresh_flags(memory,frame,value,1)
            if value == 0:
                break
            state.progress('scripted-scene-sound-byte')
        previous = state.read(0xFF703E,2)
        frame,elapsed = _movement_binary_flags(state,frame,previous,1,16)
        state.write(0xFF703E,2,elapsed)
        frame = _first_long(frame,'target_x',0)
        mode = state.read(0xFF7026,2)
        frame = _first_word(frame,'target_x',mode)
        frame = _scene_render_asl_word(memory,frame,'target_x',mode,1)
        frame = _first_long(frame,'target_y',0)
        frame = first_replace(frame,roster=memory.cursor_at(0x389C2))
        duration = frame.roster.word(u16(mode << 1))
        frame = _first_word(frame,'target_y',duration)
        elapsed = state.read(0xFF703E,2)
        frame = _scene_render_compare(memory,frame,duration,elapsed,16)
        if duration == elapsed:
            return memory.sync_status(frame)
        if frame.stack_cursor is None:
            raise SceneRefreshBoundary(0x3A72E,frame,0x39800)
        frame = _scene_render_call_fields(memory,frame,0x3A72E,0x39800)
        frame = _draw_scripted_scene_frame_fields(memory,frame)

def _draw_scripted_scene_frame_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """39800 unique actual dispatch; only paired/staged live saves remain unlifted."""
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x39800,frame,None)
    frame = _first_long(frame,'target_x',0)
    frame,mode = _scene_mode_compare(memory,frame,10)
    if mode < 10:
        return _draw_scripted_sequence_fields(memory,frame)
    frame,mode = _scene_mode_compare(memory,frame,11)
    if mode <= 11:
        frame = _scene_render_call_fields(memory,frame,0x399D8,0x39AB6)
        frame,mode = _scene_mode_compare(memory,frame,11)
        selected = 1 if mode == 11 else 0
        frame = _first_long(frame,'target_y',selected)
        frame = _scene_render_asl_word(memory,frame,'target_y',selected,2)
        frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x39B08).long(selected << 2)))
        frame = _first_word(frame,'target_x',memory.state.read(0xFF7028,2))
        frame = _first_word(frame,'target_y',memory.state.read(0xFF702A,2))
        frame = _first_long(frame,'unit',4)
        frame = _first_long(frame,'count',0)
        frame,mode = _scene_mode_compare(memory,frame,11)
        frame = _first_long(frame,'distance',0 if mode == 11 else 256)
        frame = _scene_render_call_fields(memory,frame,0x3A5A0,0x39AFC)
    else:
        frame,mode = _scene_mode_compare(memory,frame,19)
        if mode <= 19:
            frame = _draw_scripted_arrival_fields(memory,frame)
        else:
            frame,mode = _scene_mode_compare(memory,frame,21)
            if mode <= 21:
                frame = _draw_scripted_two_layer_fields(memory,frame)
            else:
                frame,mode = _scene_mode_compare(memory,frame,23)
                if mode <= 23:
                    frame = _draw_scripted_paired_positions_fields(memory,frame)
                else:
                    frame,mode = _scene_mode_compare(memory,frame,25)
                    if mode <= 25:
                        frame = _draw_scripted_staged_pair_fields(memory,frame)
                    else:
                        frame,mode = _scene_mode_compare(memory,frame,27)
                        if mode == 27:
                            return _draw_scripted_sequence_fields(memory,frame)
                        frame,mode = _scene_mode_compare(memory,frame,27)
                        if mode > 27:
                            frame = _draw_scripted_high_mode_fields(memory,frame)
                        else:
                            frame = _draw_scripted_landing_fields(memory,frame)
    return _scene_render_call_fields(memory,frame,0x3A74E,0x39B02)

def play_scripted_scene_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    checked_state(state)
    if type(frame) is not FirstDeploymentFrame or frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x3969A,frame,None)
    return _play_scripted_scene_core(state,frame)

def _scene_mode_compare(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, value: Word) -> tuple:
    mode = memory.state.read(0xFF7026,2)
    return _scene_render_compare(memory,frame,mode,value,16),mode

def _scene_mode_adjust_word(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, address: Long, amount: Word, subtract: bool = False) -> tuple:
    previous = memory.state.read(address,2)
    frame,value = _movement_binary_flags(memory.state,frame,previous,amount,16,subtract)
    memory.state.write(address,2,value)
    return frame,value

def _scene_mode_packet_parameters(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, moving: bool, attributes: Long, tile: Word) -> FirstDeploymentFrame:
    """Real shared MOVE.W/MOVEQ packet operands, never default full registers."""
    if moving:
        x = memory.state.read(0xFF7028,2)
        y = memory.state.read(0xFF702A,2)
    else:
        x,y = 96,96
    frame = _first_word(frame,'target_x',x)
    frame = _first_word(frame,'target_y',y)
    frame = _first_long(frame,'unit',attributes)
    frame = _first_long(frame,'count',0)
    return _first_word(frame,'distance',tile)

def _scene_mode_restore_longs(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, names: tuple) -> FirstDeploymentFrame:
    """Actual MOVEM loads, including live aliased saved values."""
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x3988C,frame,None)
    stack = frame.stack_cursor
    values = tuple(stack.long(index * 4) for index in range(len(names)))
    return first_replace(frame,stack_cursor=stack.advance(len(names) * 4),**{name:value for name,value in zip(names,values)})

def _scene_mode_push_word(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, value: Word) -> FirstDeploymentFrame:
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x3988C,frame,None)
    stack = frame.stack_cursor.advance(-2)
    stack.set_word(0,value)
    return first_replace(frame,stack_cursor=stack)

def _scene_mode_restore_word(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name) -> FirstDeploymentFrame:
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x398C6,frame,None)
    stack = frame.stack_cursor
    return first_replace(frame,stack_cursor=stack.advance(2),**{name:u32(s16(stack.word()))})

def _scene_mode_lsr_word(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, original: Word, count: Word) -> FirstDeploymentFrame:
    value = original >> count
    carry = bool(original & (1 << (count - 1)))
    carrier = None if frame.carrier(name) is None else replace_word(frame.carrier(name),value)
    status = (17 if carry else 0) | (4 if value == 0 else 0)
    return memory.sync_status(first_replace(frame,status=status,**{name:carrier}))

def _copy_scene_palette_words_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """399AA/399CC: sole sixteen WORD copy with actual DBRA carrier."""
    frame = first_replace(frame,candidates=memory.cursor_at(0xFFFFFB00))
    count = 16
    frame = _first_long(frame,'target_x',count - 1)
    for index in range(count):
        source,destination = frame.roster,frame.candidates
        value = source.word()
        frame = first_replace(frame,roster=source.advance(2),candidates=destination.advance(2))
        frame = _scene_refresh_emit(memory,frame,destination.base,2,value)
        frame = _scene_refresh_decrement(frame,'target_x',count - 1 - index)
    return frame

def _draw_scripted_sequence_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3980E: sequence redirects, mode1/5 palettes, true WORD save and dual draw."""
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x3980E,frame,None)
    tick = memory.state.read(0xFFFFF320,2)
    frame = _first_word(frame,'target_x',tick)
    frame = _first_word(frame,'target_x',tick & 7)
    if tick & 7 == 0:
        frame,_ = _scene_mode_adjust_word(memory,frame,0xFF7004,1)
    while True:
        frame = _first_long(frame,'target_y',0)
        mode = memory.state.read(0xFF7026,2)
        frame = _first_word(frame,'count',mode)
        frame = _scene_render_asl_word(memory,frame,'count',mode,2)
        frame = first_replace(frame,candidates=memory.cursor_at(0x38A12))
        frame = first_replace(frame,roster=memory.cursor_at(frame.candidates.long(u16(mode << 2))))
        frame = _first_long(frame,'target_x',0)
        offset = memory.state.read(0xFF7004,2)
        frame = _first_word(frame,'target_x',offset)
        frame = first_replace(frame,roster=frame.roster.advance(s16(offset)))
        packet = frame.roster.byte()
        frame = _first_byte(frame,'target_y',packet)
        if not packet & 128:
            break
        frame = _first_long(frame,'target_x',0)
        frame = first_replace(frame,roster=frame.roster.advance(1))
        redirected = frame.roster.byte()
        frame = _first_byte(frame,'target_y',redirected)
        frame = _scene_refresh_emit(memory,frame,0xFF7004,2,low16(frame.target_y))
    frame,mode = _scene_mode_compare(memory,frame,5)
    if mode == 5:
        frame = _scene_render_compare(memory,frame,low16(frame.target_y),3,16)
        if low16(frame.target_y) >= 3:
            tick = memory.state.read(0xFFFFF320,2)
            frame = _first_word(frame,'target_x',tick)
            frame = _first_word(frame,'target_x',tick & 7)
            skip_palette = False
            if tick & 7 == 0:
                counter = memory.state.read(0xFF703C,2)
                frame = _scene_render_compare(memory,frame,counter,40,16)
                if counter == 40:
                    skip_palette = True
                else:
                    frame,_ = _scene_mode_adjust_word(memory,frame,0xFF703C,4)
            if not skip_palette:
                frame = _first_long(frame,'count',0)
                offset = memory.state.read(0xFF703C,2)
                frame = _first_word(frame,'count',offset)
                frame = first_replace(frame,candidates=memory.cursor_at(0x39964))
                frame = first_replace(frame,roster=memory.cursor_at(frame.candidates.long(offset)))
                frame = _copy_scene_palette_longs_fields(memory,frame)
    frame,mode = _scene_mode_compare(memory,frame,1)
    if mode == 1:
        frame = _first_long(frame,'unit',0)
        frame = _scene_render_compare(memory,frame,low16(frame.target_y),1,16)
        palette_offset = 0 if low16(frame.target_y) == 1 else 32
        if palette_offset != 0:
            frame = _scene_render_arithmetic(memory,frame,'unit',0,palette_offset,16)
        frame = first_replace(frame,candidates=memory.cursor_at(0xFFFFFB00),roster=memory.cursor_at(0x38E98 + s16(palette_offset)))
        frame = _copy_scene_palette_longs_fields(memory,frame)
    frame = _scene_mode_push_word(memory,frame,low16(frame.target_y))
    frame = _scene_render_call_fields(memory,frame,0x399D8,0x39894)
    frame = _first_long(frame,'target_x',0)
    mode = memory.state.read(0xFF7026,2)
    frame = _first_word(frame,'count',mode)
    frame = _scene_render_asl_word(memory,frame,'count',mode,2)
    frame = first_replace(frame,auxiliary=memory.cursor_at(0x38C28))
    frame = first_replace(frame,candidates=memory.cursor_at(frame.auxiliary.long(u16(mode << 2))))
    selected = low16(frame.target_y)
    frame = _scene_render_asl_word(memory,frame,'target_y',selected,2)
    frame = first_replace(frame,candidates=frame.candidates.advance(s16(u16(selected << 2))))
    frame = first_replace(frame,roster=memory.cursor_at(frame.candidates.long()))
    frame = _scene_mode_packet_parameters(memory,frame,True,4,0)
    frame = _first_long(frame,'distance',0)
    frame = _scene_render_call_fields(memory,frame,0x3A5A0,0x398C4)
    frame = _scene_mode_restore_word(memory,frame,'target_y')
    mode = memory.state.read(0xFF7026,2)
    frame = _first_word(frame,'target_x',mode)
    frame = first_replace(frame,auxiliary=memory.cursor_at(0x3899A))
    dual = frame.auxiliary.byte(mode)
    frame = _first_byte(frame,'unit',dual)
    frame = _scene_render_compare(memory,frame,dual,1,8)
    if dual == 1:
        frame = _first_long(frame,'target_x',0)
        mode = memory.state.read(0xFF7026,2)
        frame = _first_word(frame,'count',mode)
        frame = _scene_render_asl_word(memory,frame,'count',mode,2)
        frame = first_replace(frame,controller=memory.cursor_at(0x38D94))
        frame = first_replace(frame,candidates=memory.cursor_at(frame.controller.long(u16(mode << 2))))
        selected = low16(frame.target_y)
        frame = _scene_render_asl_word(memory,frame,'target_y',selected,2)
        frame = first_replace(frame,candidates=frame.candidates.advance(s16(u16(selected << 2))))
        frame = first_replace(frame,roster=memory.cursor_at(frame.candidates.long()))
        frame = _scene_mode_packet_parameters(memory,frame,True,4,256)
        frame = _first_long(frame,'distance',256)
        frame = _scene_render_call_fields(memory,frame,0x3A5A0,0x39912)
    return _scene_render_call_fields(memory,frame,0x3A74E,0x39918)

def _draw_scripted_arrival_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """39B1C..39CB8: one prearrival frame, then the original saved variant."""
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x39B1C,frame,None)
    while True:
        frame,_ = _scene_mode_adjust_word(memory,frame,0xFF703C,1)
        counter = memory.state.read(0xFF703C,2)
        frame = _scene_render_compare(memory,frame,counter,144,16)
        if counter == 144:
            mode = memory.state.read(0xFF7026,2)
            frame = _first_word(frame,'target_x',mode)
            frame = _scene_render_asl_word(memory,frame,'target_x',mode,1)
            frame = first_replace(frame,roster=memory.cursor_at(0x39BEC),candidates=memory.cursor_at(0x39C1C))
            x,y = frame.roster.word(u16(mode << 1)),frame.candidates.word(u16(mode << 1))
            frame = _first_word(frame,'target_y',x)
            frame = _first_word(frame,'unit',y)
            frame = _scene_refresh_emit(memory,frame,0xFF7028,2,x)
            frame = _scene_refresh_emit(memory,frame,0xFF702A,2,y)
            break
        counter = memory.state.read(0xFF703C,2)
        frame = _scene_render_compare(memory,frame,counter,144,16)
        if counter > 144:
            break
        frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x39BB4).long()))
        frame = _scene_mode_packet_parameters(memory,frame,False,5,256)
        frame = _scene_render_call_fields(memory,frame,0x3A7A2,0x39B54)
        frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x39BBC).long()))
        frame = _scene_mode_packet_parameters(memory,frame,False,5,0)
        frame = _scene_render_call_fields(memory,frame,0x3A7A2,0x39B70)
        position = memory.state.read(0xFF7028,2)
        frame = _scene_render_compare(memory,frame,position,96,16)
        if position >= 96:
            tick = memory.state.read(0xFFFFF320,2)
            frame = _first_word(frame,'target_x',tick)
            frame = _first_word(frame,'target_x',tick & 3)
            if tick & 3 == 0:
                frame,_ = _scene_mode_adjust_word(memory,frame,0xFF7028,1,True)
        frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x39BB8).long()))
        frame = _scene_mode_packet_parameters(memory,frame,True,4,0)
        frame = _scene_render_call_fields(memory,frame,0x3A5A0,0x39BAE)
        # 39BB0 -> 39AFE finishes this frame; 39B04 -> 397C8 waits again.
        # The caller owns that existing finish/wait path, not this branch.
        return frame
    mode = memory.state.read(0xFF7026,2)
    frame = _first_word(frame,'target_x',mode)
    frame = _first_long(frame,'target_y',0)
    frame = first_replace(frame,roster=memory.cursor_at(0x39CD8))
    variant = frame.roster.byte(mode)
    frame = _first_byte(frame,'target_y',variant)
    frame = _scene_render_asl_word(memory,frame,'target_y',variant,2)
    frame = _scene_render_push_longs(memory,frame,(frame.target_y,frame.target_x))
    frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x39CB8).long(u16(variant << 2))))
    frame = _scene_mode_packet_parameters(memory,frame,False,3,0)
    frame = _scene_render_call_fields(memory,frame,0x3A7A2,0x39C7C)
    frame = _scene_mode_restore_longs(memory,frame,('target_x','target_y'))
    frame = _scene_render_compare(memory,frame,low16(frame.target_x),12,16)
    if low16(frame.target_x) != 12:
        frame = _scene_render_push_longs(memory,frame,(frame.target_y,))
        frame = _scene_render_call_fields(memory,frame,0x399D8,0x39C92)
        frame = _scene_mode_restore_longs(memory,frame,('target_y',))
        frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x39CC8).long(low16(frame.target_y))))
        frame = _scene_mode_packet_parameters(memory,frame,True,2,0)
        frame = _scene_render_call_fields(memory,frame,0x3A5A0,0x39CB2)
    return frame

def _draw_scripted_two_layer_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """39CFC: modes14/15, live second mode comparison chooses moving object."""
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x39CFC,frame,None)
    frame,mode = _scene_mode_compare(memory,frame,20)
    table = 0x39D6A if mode == 20 else 0x39D72
    frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(table).long()))
    frame = _scene_mode_packet_parameters(memory,frame,False,3,0)
    frame = _scene_render_call_fields(memory,frame,0x3A7A2,0x39D2C)
    frame = _scene_render_call_fields(memory,frame,0x399D8,0x39D32)
    frame = _first_long(frame,'target_y',4)
    frame,mode = _scene_mode_compare(memory,frame,20)
    table = 0x39D6A if mode == 20 else 0x39D72
    frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(table).long(low16(frame.target_y))))
    frame = _scene_mode_packet_parameters(memory,frame,True,2,0)
    return _scene_render_call_fields(memory,frame,0x3A5A0,0x39D64)

def _draw_scripted_landing_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x39D92,frame,None)
    frame = _scene_render_call_fields(memory,frame,0x399D8,0x39D96)
    frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x39E1E).long()))
    frame = _scene_mode_packet_parameters(memory,frame,True,5,0)
    frame = _scene_render_call_fields(memory,frame,0x3A5A0,0x39DB4)
    y = memory.state.read(0xFF702A,2)
    frame = _scene_render_compare(memory,frame,y,96,16)
    if y != 96:
        return frame
    counter = memory.state.read(0xFF703C,2)
    frame = _scene_render_compare(memory,frame,counter,20,16)
    if counter != 20:
        tick = memory.state.read(0xFFFFF320,2)
        frame = _first_word(frame,'target_x',tick)
        frame = _first_word(frame,'target_x',tick & 15)
        if tick & 15 == 0:
            frame,_ = _scene_mode_adjust_word(memory,frame,0xFF703C,4)
            frame = _first_long(frame,'count',0)
            offset = memory.state.read(0xFF703C,2)
            frame = _first_word(frame,'count',offset)
            frame = first_replace(frame,candidates=memory.cursor_at(0x39E26))
            frame = first_replace(frame,roster=memory.cursor_at(frame.candidates.long(offset)))
            frame = _copy_scene_palette_longs_fields(memory,frame)
    frame = _first_long(frame,'target_x',4)
    frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x39E1E).long(low16(frame.target_x))))
    frame = _scene_mode_packet_parameters(memory,frame,False,4,0)
    return _scene_render_call_fields(memory,frame,0x3A7A2,0x39E18)

def _draw_scripted_wave_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3A1E0: original pointer-only advance and tick-dependent sequence stride."""
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x3A1E0,frame,None)
    frame = _first_long(frame,'target_x',0)
    offset = memory.state.read(0xFF703C,2)
    frame = _first_word(frame,'target_x',offset)
    frame = first_replace(frame,candidates=memory.cursor_at(0x3A2DC + s16(offset)))
    frame = _scene_refresh_emit(memory,frame,0xFF7028,2,frame.candidates.word())
    frame,_ = _scene_mode_adjust_word(memory,frame,0xFF703C,2)
    offset = memory.state.read(0xFF703C,2)
    frame = _first_word(frame,'target_x',offset)
    frame = first_replace(frame,candidates=memory.cursor_at(0x3A2DC + s16(offset)))
    frame = _scene_refresh_emit(memory,frame,0xFF702A,2,96)
    tick = memory.state.read(0xFFFFF320,2)
    frame = _first_word(frame,'target_x',tick)
    frame = _first_word(frame,'target_x',tick & 3)
    if tick & 3:
        frame,_ = _scene_mode_adjust_word(memory,frame,0xFF703C,2,True)
    else:
        frame,_ = _scene_mode_adjust_word(memory,frame,0xFF703C,2)
        frame = first_replace(frame,candidates=memory.cursor_at(0x3A2DC))
        offset = memory.state.read(0xFF703C,2)
        frame = first_replace(frame,candidates=frame.candidates.advance(s16(offset)))
        end = frame.candidates.word()
        frame = _first_word(frame,'target_y',end)
        frame = _scene_render_compare(memory,frame,end,255,16)
        if end == 255:
            frame = _scene_refresh_emit(memory,frame,0xFF703C,2,0)
    frame = first_replace(frame,candidates=memory.cursor_at(0x38D84))
    frame = first_replace(frame,roster=memory.cursor_at(frame.candidates.long()))
    frame = _scene_mode_packet_parameters(memory,frame,True,3,0)
    frame = _scene_render_call_fields(memory,frame,0x3A5A0,0x3A26E)
    elapsed = memory.state.read(0xFF703E,2)
    frame = _scene_render_compare(memory,frame,elapsed,120,16)
    if elapsed < 120:
        return frame
    counter = memory.state.read(0xFF7004,2)
    frame = _scene_render_compare(memory,frame,counter,24,16)
    if counter != 24:
        tick = memory.state.read(0xFFFFF320,2)
        frame = _first_word(frame,'target_x',tick)
        frame = _first_word(frame,'target_x',tick & 7)
        if tick & 7 == 0:
            frame,_ = _scene_mode_adjust_word(memory,frame,0xFF7004,4)
            frame = _first_long(frame,'count',0)
            offset = memory.state.read(0xFF7004,2)
            frame = _first_word(frame,'count',offset)
            frame = first_replace(frame,candidates=memory.cursor_at(0x3A306))
            frame = first_replace(frame,roster=memory.cursor_at(frame.candidates.long(offset)))
            frame = _copy_scene_palette_longs_fields(memory,frame)
    frame = first_replace(frame,candidates=memory.cursor_at(0x38D88))
    frame = first_replace(frame,roster=memory.cursor_at(frame.candidates.long()))
    frame = _scene_mode_packet_parameters(memory,frame,False,5,0)
    return _scene_render_call_fields(memory,frame,0x3A7A2,0x3A2D6)

def _draw_scripted_late_palette_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x3A322,frame,None)
    frame = _scene_render_call_fields(memory,frame,0x399D8,0x3A326)
    frame = first_replace(frame,candidates=memory.cursor_at(0x38D8C))
    frame = first_replace(frame,roster=memory.cursor_at(frame.candidates.long()))
    frame = _scene_mode_packet_parameters(memory,frame,True,4,0)
    frame = _scene_render_call_fields(memory,frame,0x3A5A0,0x3A344)
    elapsed = memory.state.read(0xFF703E,2)
    frame = _scene_render_compare(memory,frame,elapsed,120,16)
    if elapsed < 120:
        return frame
    counter = memory.state.read(0xFF703C,2)
    frame = _scene_render_compare(memory,frame,counter,24,16)
    if counter != 24:
        tick = memory.state.read(0xFFFFF320,2)
        frame = _first_word(frame,'target_x',tick)
        frame = _first_word(frame,'target_x',tick & 15)
        if tick & 15 == 0:
            frame,_ = _scene_mode_adjust_word(memory,frame,0xFF703C,4)
            frame = _first_long(frame,'count',0)
            offset = memory.state.read(0xFF703C,2)
            frame = _first_word(frame,'count',offset)
            frame = first_replace(frame,candidates=memory.cursor_at(0x3A3B2))
            frame = first_replace(frame,roster=memory.cursor_at(frame.candidates.long(offset)))
            frame = _copy_scene_palette_longs_fields(memory,frame)
    frame = first_replace(frame,candidates=memory.cursor_at(0x38D90))
    frame = first_replace(frame,roster=memory.cursor_at(frame.candidates.long()))
    frame = _scene_mode_packet_parameters(memory,frame,False,5,0)
    return _scene_render_call_fields(memory,frame,0x3A7A2,0x3A3AC)

def _draw_scripted_three_frame_stage_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x3A3CE,frame,None)
    frame,_ = _scene_mode_adjust_word(memory,frame,0xFF7044,1)
    counter = memory.state.read(0xFF7044,2)
    frame = _scene_render_compare(memory,frame,counter,128,16)
    if counter <= 128:
        tick = memory.state.read(0xFFFFF321,1)
        frame = _first_byte(frame,'target_x',tick)
        frame = _scene_render_bit(memory,frame,frame.target_x,4)
        if not tick & 4:
            index = memory.state.read(0xFF703C,2)
            frame = _scene_render_compare(memory,frame,index,2,16)
            if index >= 2:
                frame = _scene_refresh_emit(memory,frame,0xFF703C,2,0)
            else:
                frame,_ = _scene_mode_adjust_word(memory,frame,0xFF703C,1)
        index = memory.state.read(0xFF703C,2)
        frame = _first_word(frame,'target_y',index)
        frame = _scene_render_asl_word(memory,frame,'target_y',index,2)
        frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x3A432).long(u16(index << 2))))
        frame = _scene_mode_packet_parameters(memory,frame,False,5,0)
        return _scene_render_call_fields(memory,frame,0x3A7A2,0x3A42C)
    frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x3A482).long()))
    frame = _scene_mode_packet_parameters(memory,frame,False,5,0)
    frame = _scene_render_call_fields(memory,frame,0x3A7A2,0x3A458)
    frame = _scene_render_call_fields(memory,frame,0x399D8,0x3A45E)
    frame = _first_long(frame,'target_y',4)
    frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x3A482).long(low16(frame.target_y))))
    frame = _scene_mode_packet_parameters(memory,frame,True,4,0)
    return _scene_render_call_fields(memory,frame,0x3A5A0,0x3A47C)

def _draw_scripted_high_mode_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x3A114,frame,None)
    frame,mode = _scene_mode_compare(memory,frame,28)
    if mode == 28:
        return _draw_scripted_staged_pair_fields(memory,frame)
    frame,_ = _scene_mode_compare(memory,frame,29)
    frame,mode = _scene_mode_compare(memory,frame,30)
    if mode == 30:
        tick = memory.state.read(0xFFFFF320,2)
        frame = _first_word(frame,'target_x',tick)
        frame = _scene_mode_lsr_word(memory,frame,'target_x',tick,2)
        selected = (tick >> 2) & 3
        frame = _first_word(frame,'target_x',selected)
        frame = _scene_render_asl_word(memory,frame,'target_x',selected,5)
        frame = first_replace(frame,roster=memory.cursor_at(0x390D8 + s16(u16(selected << 5))))
        frame = _copy_scene_palette_words_fields(memory,frame)
    else:
        frame,mode = _scene_mode_compare(memory,frame,31)
        if mode == 31:
            tick = memory.state.read(0xFFFFF320,2)
            frame = _first_word(frame,'target_x',tick)
            frame = _scene_mode_lsr_word(memory,frame,'target_x',tick,3)
            selected = (tick >> 3) & 1
            frame = _first_word(frame,'target_x',selected)
            frame = _scene_render_asl_word(memory,frame,'target_x',selected,5)
            frame = first_replace(frame,roster=memory.cursor_at(0x39158 + s16(u16(selected << 5))))
            frame = _copy_scene_palette_words_fields(memory,frame)
    frame,mode = _scene_mode_compare(memory,frame,32)
    if mode == 32:
        return _draw_scripted_wave_fields(memory,frame)
    frame,mode = _scene_mode_compare(memory,frame,33)
    if mode == 33:
        return _draw_scripted_late_palette_fields(memory,frame)
    frame,mode = _scene_mode_compare(memory,frame,34)
    if mode == 34:
        return _draw_scripted_three_frame_stage_fields(memory,frame)
    frame,mode = _scene_mode_compare(memory,frame,35)
    if mode == 35:
        frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x3A4C6).long()))
        frame = _scene_mode_packet_parameters(memory,frame,False,5,0)
        frame = _scene_render_call_fields(memory,frame,0x3A7A2,0x3A4A4)
        frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x3A4CA).long()))
        frame = _scene_mode_packet_parameters(memory,frame,False,5,256)
        return _scene_render_call_fields(memory,frame,0x3A7A2,0x3A4C0)
    frame,mode = _scene_mode_compare(memory,frame,37)
    if mode == 37:
        frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x3A50A).long()))
        frame = _scene_mode_packet_parameters(memory,frame,False,5,0)
        frame = _scene_render_call_fields(memory,frame,0x3A7A2,0x3A4E8)
        frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x3A50E).long()))
        frame = _scene_mode_packet_parameters(memory,frame,False,5,256)
        return _scene_render_call_fields(memory,frame,0x3A7A2,0x3A504)
    frame,mode = _scene_mode_compare(memory,frame,39)
    if mode == 39:
        frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x3A532).long()))
        frame = _scene_mode_packet_parameters(memory,frame,False,5,0)
        return _scene_render_call_fields(memory,frame,0x3A7A2,0x3A52C)
    frame,mode = _scene_mode_compare(memory,frame,31)
    if mode == 31:
        frame = _first_long(frame,'target_y',4)
        frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x3A1D8).long(low16(frame.target_y))))
        frame = _scene_mode_packet_parameters(memory,frame,False,4,0)
        return _scene_render_call_fields(memory,frame,0x3A7A2,0x3A1D2)
    frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x3A1D8).long()))
    frame = _scene_mode_packet_parameters(memory,frame,False,5,0)
    return _scene_render_call_fields(memory,frame,0x3A7A2,0x3A1B2)

def initialize_scripted_secondary_position_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, mode: Word | None = None) -> FirstDeploymentFrame:
    """39F18: single latch algorithm; optional mode is a real old WORD observation."""
    memory.frame(frame)
    latched = memory.state.read(0xFF7036,2)
    frame = _scene_refresh_flags(memory,frame,latched,2)
    if latched != 0:
        return frame
    if mode is None:
        if frame.target_x is None:
            raise SceneRefreshBoundary(0x39F22,frame,None)
        mode = low16(frame.target_x)
    uint(mode,16)
    if frame.target_x is not None and low16(frame.target_x) != mode:
        raise ValueError('actual secondary mode WORD disagrees with D0')
    frame = _scene_render_asl_word(memory,frame,'target_x',mode,1)
    offset = u16(mode << 1)
    frame = first_replace(frame,roster=memory.cursor_at(0x38B88),candidates=memory.cursor_at(0x38BD8))
    x,y = frame.roster.word(offset),frame.candidates.word(offset)
    frame = _first_word(frame,'target_y',x)
    frame = _first_word(frame,'unit',y)
    frame = _scene_refresh_emit(memory,frame,0xFF7032,2,x)
    frame = _scene_refresh_emit(memory,frame,0xFF7034,2,y)
    return _scene_refresh_emit(memory,frame,0xFF7036,2,1)

def select_scene_object_frame_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3A08A: fixed pointers or live D0-gated BYTE sequence, no tick substitution."""
    memory.frame(frame)
    if frame.target_y is None:
        raise SceneRefreshBoundary(0x3A08A,frame,None)
    frame,mode = _scene_mode_compare(memory,frame,27)
    if mode <= 27:
        return first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x3A06A).long(low16(frame.target_y))))
    selected = low16(frame.target_y)
    frame = _scene_render_compare(memory,frame,selected,7,16)
    if selected <= 7:
        if frame.target_x is None:
            raise SceneRefreshBoundary(0x3A0AA,frame,None)
        sequence = memory.state.read(0xFF703C,2)
        frame = _first_word(frame,'unit',sequence)
        tick = low16(frame.target_x)
        frame = _first_word(frame,'target_x',tick & 7)
        if tick & 7 == 0:
            frame,_ = _scene_mode_adjust_word(memory,frame,0xFF703C,1)
            sequence = memory.state.read(0xFF703C,2)
            frame = _first_word(frame,'unit',sequence)
        frame = first_replace(frame,scan=memory.cursor_at(0x3A0E4))
        selected = frame.scan.byte(sequence)
        frame = _first_byte(frame,'target_y',selected)
        frame = _scene_render_compare(memory,frame,selected,255,8)
        if selected == 255:
            memory.state.read(0xFF703C,2)
            frame = _scene_refresh_emit(memory,frame,0xFF703C,2,0)
            frame = _first_long(frame,'target_y',0)
        frame = _first_long(frame,'target_y',frame.target_y & 15)
    return first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x3A07A).long(low16(frame.target_y))))

def _draw_scripted_paired_positions_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """39E4A: paired actor live slots with actual three LONG saves/restores."""
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x39E4A,frame,None)
    frame = _scene_render_call_fields(memory,frame,0x399D8,0x39E4E)
    frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x39F10).long()))
    frame = _scene_mode_packet_parameters(memory,frame,True,5,0)
    frame = _scene_render_call_fields(memory,frame,0x3A5A0,0x39E6C)
    frame = _first_byte(frame,'target_y',memory.state.read(0xFF702C,1))
    frame = _first_word(frame,'unit',memory.state.read(0xFF7028,2))
    frame = _first_word(frame,'count',memory.state.read(0xFF702A,2))
    frame = _scene_render_push_longs(memory,frame,(frame.count,frame.unit,frame.target_y))
    frame,_ = _scene_mode_adjust_word(memory,frame,0xFF7026,1)
    mode = memory.state.read(0xFF7026,2)
    frame = _first_word(frame,'target_x',mode)
    frame = first_replace(frame,roster=memory.cursor_at(0x38E50))
    movement = frame.roster.byte(mode)
    frame = _first_byte(frame,'target_y',movement)
    frame = _scene_refresh_emit(memory,frame,0xFF702C,1,movement)
    frame = _scene_render_call_fields(memory,frame,0x39F18,0x39EA2)
    frame = _scene_refresh_emit(memory,frame,0xFF7028,2,memory.state.read(0xFF7032,2))
    frame = _scene_refresh_emit(memory,frame,0xFF702A,2,memory.state.read(0xFF7034,2))
    frame = _scene_render_call_fields(memory,frame,0x399D8,0x39EBC)
    frame = _first_long(frame,'target_y',4)
    frame = first_replace(frame,roster=memory.cursor_at(memory.state.table_at(0x39F10).long(low16(frame.target_y))))
    frame = _scene_mode_packet_parameters(memory,frame,True,4,0)
    frame = _scene_render_call_fields(memory,frame,0x3A5A0,0x39EDA)
    frame = _scene_refresh_emit(memory,frame,0xFF7032,2,memory.state.read(0xFF7028,2))
    frame = _scene_refresh_emit(memory,frame,0xFF7034,2,memory.state.read(0xFF702A,2))
    frame = _scene_mode_restore_longs(memory,frame,('target_y','unit','count'))
    frame = _scene_refresh_emit(memory,frame,0xFF702C,1,low8(frame.target_y))
    frame = _scene_refresh_emit(memory,frame,0xFF7028,2,low16(frame.unit))
    frame = _scene_refresh_emit(memory,frame,0xFF702A,2,low16(frame.count))
    frame,_ = _scene_mode_adjust_word(memory,frame,0xFF7026,1,True)
    return frame

def _draw_scripted_staged_pair_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """39F56: delayed primary/secondary pair, shared by modes18/19/1C."""
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x39F56,frame,None)
    frame,_ = _scene_mode_adjust_word(memory,frame,0xFF7044,1)
    tick = memory.state.read(0xFFFFF320,2)
    frame = _first_word(frame,'target_x',tick)
    frame = _scene_render_bit(memory,frame,frame.target_x,8)
    selected = 4 if tick & 8 else 0
    frame = _first_long(frame,'target_y',selected)
    frame = _scene_render_call_fields(memory,frame,0x3A08A,0x39F74)
    frame = _scene_mode_packet_parameters(memory,frame,False,5,0)
    frame = _scene_render_call_fields(memory,frame,0x3A7A2,0x39F8A)
    counter = memory.state.read(0xFF7044,2)
    frame = _scene_render_compare(memory,frame,counter,32,16)
    if counter < 32:
        return frame
    frame = _scene_render_call_fields(memory,frame,0x399D8,0x39F9C)
    frame = _first_long(frame,'target_y',8)
    frame = _scene_render_call_fields(memory,frame,0x3A08A,0x39FA2)
    frame = _scene_mode_packet_parameters(memory,frame,True,4,0)
    frame = _scene_render_call_fields(memory,frame,0x3A5A0,0x39FBC)
    counter = memory.state.read(0xFF7044,2)
    frame = _scene_render_compare(memory,frame,counter,64,16)
    if counter < 64:
        return frame
    frame = _first_word(frame,'target_x',memory.state.read(0xFF7028,2))
    frame = _first_word(frame,'target_y',memory.state.read(0xFF702A,2))
    frame = _first_byte(frame,'unit',memory.state.read(0xFF702C,1))
    frame = _scene_render_push_longs(memory,frame,(frame.unit,frame.target_y,frame.target_x))
    frame,_ = _scene_mode_adjust_word(memory,frame,0xFF7026,1)
    mode = memory.state.read(0xFF7026,2)
    frame = _first_word(frame,'target_x',mode)
    frame = first_replace(frame,roster=memory.cursor_at(0x38E50))
    movement = frame.roster.byte(mode)
    frame = _first_byte(frame,'target_y',movement)
    frame = _scene_refresh_emit(memory,frame,0xFF702C,1,movement)
    frame = _scene_refresh_emit(memory,frame,0xFF7028,2,memory.state.read(0xFF7032,2))
    frame = _scene_refresh_emit(memory,frame,0xFF702A,2,memory.state.read(0xFF7034,2))
    frame = _scene_render_call_fields(memory,frame,0x399D8,0x3A012)
    frame = _first_long(frame,'target_y',12)
    frame = _scene_render_call_fields(memory,frame,0x3A08A,0x3A018)
    frame = _scene_mode_packet_parameters(memory,frame,True,4,0)
    frame = _scene_render_call_fields(memory,frame,0x3A5A0,0x3A032)
    frame = _scene_refresh_emit(memory,frame,0xFF7032,2,memory.state.read(0xFF7028,2))
    frame = _scene_refresh_emit(memory,frame,0xFF7034,2,memory.state.read(0xFF702A,2))
    frame = _scene_mode_restore_longs(memory,frame,('target_x','target_y','unit'))
    frame = _scene_refresh_emit(memory,frame,0xFF7028,2,low16(frame.target_x))
    frame = _scene_refresh_emit(memory,frame,0xFF702A,2,low16(frame.target_y))
    frame = _scene_refresh_emit(memory,frame,0xFF702C,1,low8(frame.unit))
    frame,_ = _scene_mode_adjust_word(memory,frame,0xFF7026,1,True)
    return frame

def _glyph_shift_long_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, amount: Word) -> FirstDeploymentFrame:
    original = frame.carrier(name)
    if original is None:
        raise SceneRefreshBoundary(0xAF0C,frame,None)
    value = u32(original << amount)
    carry = bool(original & (1 << (32 - amount)))
    status = (17 if carry else 0) | (8 if value & 0x80000000 else 0) | (4 if value == 0 else 0)
    return memory.sync_status(first_replace(frame,status=status,**{name:value}))

def _glyph_save_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, include_source: bool) -> FirstDeploymentFrame:
    if frame.stack_cursor is None:
        return frame
    values = (frame.choice,frame.offset_y,frame.offset_x,frame.distance)
    if include_source:
        values = (frame.controller.base,) + values
    return _scene_render_push_longs(memory,frame,values)

def _glyph_restore_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, original: FirstDeploymentFrame, include_source: bool) -> FirstDeploymentFrame:
    if frame.stack_cursor is None:
        return first_replace(frame,distance=original.distance,offset_x=original.offset_x,
            offset_y=original.offset_y,choice=original.choice,
            controller=original.controller if include_source else frame.controller)
    stack = frame.stack_cursor
    values = tuple(stack.long(index * 4) for index in range(4))
    frame = first_replace(frame,distance=values[0],offset_x=values[1],offset_y=values[2],choice=values[3])
    if include_source:
        frame = first_replace(frame,controller=memory.cursor_at(stack.long(16)))
    return first_replace(frame,stack_cursor=stack.advance(20 if include_source else 16))

def _glyph_row_call_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, continuation: Long) -> FirstDeploymentFrame:
    if continuation not in (0xAEBA,0xAEC0,0xAF38):
        raise ValueError('real glyph-row return token required')
    entered = frame
    if frame.stack_cursor is not None:
        stack = frame.stack_cursor.advance(-4)
        stack.set_long(0,continuation)
        entered = first_replace(frame,stack_cursor=stack)
    result = expand_glyph_row_fields(memory,entered)
    if frame.stack_cursor is not None:
        actual = result.stack_cursor.long()
        if actual != continuation:
            raise SceneRefreshBoundary(0xAF04,result,continuation)
        result = first_replace(result,stack_cursor=result.stack_cursor.advance(4))
    return memory.sync_status(result)

def expand_glyph_row_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """AF04 sole eight-pixel row: real LSL.L/ROXL.B/OR.B and retained D6."""
    memory.frame(frame)
    if frame.target_x is None or frame.target_y is None or frame.controller is None:
        raise SceneRefreshBoundary(0xAF04,frame,None)
    frame = _first_long(frame,'choice',0)
    bits = frame.controller.byte()
    frame = first_replace(frame,controller=frame.controller.advance(1))
    frame = _first_byte(frame,'offset_y',bits)
    row_bits = 8
    frame = _first_word(frame,'distance',row_bits - 1)
    for index in range(row_bits):
        frame = _glyph_shift_long_fields(memory,frame,'choice',4)
        carry = bool(bits & 128)
        bits = u8((bits << 1) | bool(frame.status & 16))
        carrier = None if frame.offset_y is None else replace_byte(frame.offset_y,bits)
        status = (17 if carry else 0) | (8 if bits & 128 else 0) | (4 if bits == 0 else 0)
        frame = first_replace(frame,offset_y=carrier,status=status)
        color = low8(frame.target_y) if carry else low8(frame.target_x)
        frame = _first_byte(frame,'choice',low8(frame.choice) | color)
        frame = _scene_refresh_decrement(frame,'distance',row_bits - 1 - index)
    return memory.sync_status(frame)

def decode_glyph_rows_to_buffers_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """AE8A unique font/fill tile algorithm with real five LONG saves."""
    memory.frame(frame)
    if any(value is None for value in (frame.roster,frame.candidates,frame.target_x,frame.target_y,frame.count)):
        raise SceneRefreshBoundary(0xAE8A,frame,None)
    original = frame
    frame = _glyph_save_fields(memory,frame,True)
    remaining = low16(frame.count)
    row_longs = 16
    while True:
        token = frame.roster.word()
        frame = first_replace(frame,roster=frame.roster.advance(2))
        frame = _first_word(frame,'distance',token)
        if not negative_word(token):
            frame = _first_word(frame,'offset_x',token)
            high = token & 0xFF00
            frame = _first_word(frame,'offset_x',high)
            frame = _first_shift_word(frame,'offset_x',high,3)
            low = token & 255
            frame = _first_word(frame,'distance',low)
            frame = _first_shift_word(frame,'distance',low,5)
            offset = u16(low << 5) | u16(high << 3)
            frame = _first_word(frame,'distance',offset)
            frame = _first_long(frame,'distance',offset)
            frame = first_replace(frame,controller=memory.cursor_at(0x8159C + offset))
            frame = _first_word(frame,'offset_x',row_longs - 1)
            for index in range(row_longs):
                frame = _glyph_row_call_fields(memory,frame,0xAEBA)
                frame = _scene_refresh_emit(memory,frame,frame.candidates.base,4,frame.choice)
                frame = _glyph_row_call_fields(memory,frame,0xAEC0)
                frame = _scene_refresh_emit(memory,frame,frame.candidates.base + 0x40,4,frame.choice)
                frame = first_replace(frame,candidates=frame.candidates.advance(4))
                frame = _scene_refresh_decrement(frame,'offset_x',row_longs - 1 - index)
        else:
            frame = _first_long(frame,'offset_y',0)
            frame = _first_long(frame,'choice',0)
            nibbles = 8
            frame = _first_word(frame,'distance',nibbles - 1)
            for index in range(nibbles):
                frame = _glyph_shift_long_fields(memory,frame,'offset_y',4)
                frame = _glyph_shift_long_fields(memory,frame,'choice',4)
                frame = _first_word(frame,'offset_y',low16(frame.offset_y) | low16(frame.target_x))
                frame = _first_word(frame,'choice',low16(frame.choice) | low16(frame.target_y))
                frame = _scene_refresh_decrement(frame,'distance',nibbles - 1 - index)
            frame = _first_word(frame,'distance',row_longs - 1)
            for index in range(row_longs):
                frame = _scene_refresh_emit(memory,frame,frame.candidates.base + 0x40,4,frame.offset_y)
                destination = frame.candidates
                frame = first_replace(frame,candidates=destination.advance(4))
                frame = _scene_refresh_emit(memory,frame,destination.base,4,frame.offset_y)
                frame = _scene_refresh_decrement(frame,'distance',row_longs - 1 - index)
            frame = _scene_refresh_emit(memory,frame,frame.candidates.base - 0x24,4,frame.choice)
            frame = _scene_refresh_emit(memory,frame,frame.candidates.base + 0x1C,4,frame.choice)
        frame = first_replace(frame,candidates=frame.candidates.advance(0x40))
        frame = _scene_refresh_decrement(frame,'count',remaining)
        remaining = u16(remaining - 1)
        if remaining == 65535:
            return memory.sync_status(_glyph_restore_fields(memory,frame,original,True))

def expand_glyph_stream_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """AF1E sole BYTE token stream; A2 remains the last actual font cursor."""
    memory.frame(frame)
    if any(value is None for value in (frame.roster,frame.candidates,frame.target_x,frame.target_y,frame.count)):
        raise SceneRefreshBoundary(0xAF1E,frame,None)
    original = frame
    frame = _glyph_save_fields(memory,frame,False)
    remaining = low16(frame.count)
    while True:
        frame = _first_word(frame,'distance',0)
        token = frame.roster.byte()
        frame = first_replace(frame,roster=frame.roster.advance(1))
        frame = _first_byte(frame,'distance',token)
        frame = _first_shift_word(frame,'distance',token,3)
        frame = first_replace(frame,controller=memory.cursor_at(0x896DC + (token << 3)))
        rows = 8
        frame = _first_word(frame,'offset_x',rows - 1)
        for index in range(rows):
            frame = _glyph_row_call_fields(memory,frame,0xAF38)
            destination = frame.candidates
            frame = first_replace(frame,candidates=destination.advance(4))
            frame = _scene_refresh_emit(memory,frame,destination.base,4,frame.choice)
            frame = _scene_refresh_decrement(frame,'offset_x',rows - 1 - index)
        frame = _scene_refresh_decrement(frame,'count',remaining)
        remaining = u16(remaining - 1)
        if remaining == 65535:
            return memory.sync_status(_glyph_restore_fields(memory,frame,original,False))


def _dictionary_stream_take_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        carrier: str) -> tuple[FirstDeploymentFrame, bool]:
    """Read one token from the live main or two-WORD dictionary expansion."""
    from ..high_level_main_flows.business_movement_support import _movement_move, _movement_test
    if carrier not in ('target_y', 'count'):
        raise ValueError('closed dictionary token or repeat-value role required')
    frame = _movement_test(memory.state, frame, low8(frame.unit), 8)
    from_dictionary = not bool(frame.status & 4)
    source = frame.controller if from_dictionary else frame.roster
    value = source.word()
    if from_dictionary:
        frame = first_replace(frame, controller=source.advance(2))
    else:
        frame = first_replace(frame, roster=source.advance(2))
    frame = _movement_move(memory.state, frame, carrier, value, 16)
    if from_dictionary:
        frame, remaining = _movement_binary_flags(memory.state, frame, low8(frame.unit), 1, 8, True)
        frame = first_replace(frame, unit=replace_byte(frame.unit, remaining))
    else:
        frame, remaining = _movement_binary_flags(memory.state, frame, low16(frame.target_x), 1, 16, True)
        frame = first_replace(frame, target_x=replace_word(frame.target_x, remaining))
    return frame, from_dictionary


def _dictionary_stream_finished_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> tuple[FirstDeploymentFrame, bool]:
    """Only the original post-write BYTE/WORD tests determine completion."""
    from ..high_level_main_flows.business_movement_support import _movement_test
    frame = _movement_test(memory.state, frame, low8(frame.unit), 8)
    if not frame.status & 4:
        return frame, False
    frame = _movement_test(memory.state, frame, low16(frame.target_x), 16)
    return frame, bool(frame.status & 8)


def write_vdp_dictionary_repeat_stream_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """ADFC..AE8A: live FE dictionary references and FF inclusive repetition.

    The stream, dictionary and expanded pair remain separate live views.
    Repeated dictionary comparisons are real reads. A repeat value read from
    an already expanded pair bypasses source-only reference decoding, exactly
    as the original branch does; no snapshot or recursive decoder is invented.
    """
    from ..high_level_main_flows.business_movement_support import _movement_frame, _movement_move
    frame = _movement_frame(memory.state, frame)
    memory.frame(frame)
    frame = _movement_move(memory.state, frame, 'unit', 0, 8)
    frame = first_replace(frame, auxiliary=memory.cursor_at(0xC00000))
    while True:
        frame, unused_origin = _dictionary_stream_take_fields(memory, frame, 'target_y')
        frame = _movement_compare(memory.state, frame, low16(frame.target_y), 0xFE00, 16)
        if frame.status & 1:
            frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, low16(frame.target_y))
            frame, finished = _dictionary_stream_finished_fields(memory, frame)
            if finished:
                return memory.sync_status(frame)
            continue
        frame = _movement_compare(memory.state, frame, low16(frame.target_y), 0xFF00, 16)
        if frame.status & 1:
            frame = _movement_move(memory.state, frame, 'target_y', low16(frame.target_y) & 255, 16)
            frame = memory.sync_status(_first_shift_word(frame, 'target_y', low16(frame.target_y), 2))
            frame = first_replace(frame, controller=frame.candidates.advance(s16(low16(frame.target_y))))
            frame = _movement_compare(memory.state, frame, frame.controller.word(), 0xFF00, 16)
            expand_pair = not bool(frame.status & 1)
            if not expand_pair:
                frame = _movement_compare(memory.state, frame, frame.controller.word(), 0xFE00, 16)
                expand_pair = bool(frame.status & 1)
            if expand_pair:
                frame = _movement_move(memory.state, frame, 'unit', 2, 8)
            else:
                frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, frame.controller.word())
            continue

        frame = _movement_move(memory.state, frame, 'target_y', low16(frame.target_y) & 255, 16)
        frame, from_dictionary = _dictionary_stream_take_fields(memory, frame, 'count')
        if not from_dictionary:
            frame = _movement_compare(memory.state, frame, low16(frame.count), 0xFF00, 16)
            if frame.status & 1:
                frame = _movement_compare(memory.state, frame, low16(frame.count), 0xFE00, 16)
                if not frame.status & 1:
                    frame = _movement_move(memory.state, frame, 'count', low16(frame.count) & 255, 16)
                    frame = memory.sync_status(_first_shift_word(frame, 'count', low16(frame.count), 2))
                    frame = first_replace(frame, controller=frame.candidates.advance(s16(low16(frame.count))))
                    value = frame.controller.word()
                    frame = first_replace(frame, controller=frame.controller.advance(2))
                    frame = _movement_move(memory.state, frame, 'count', value, 16)
                    frame = _movement_move(memory.state, frame, 'unit', 1, 8)
        while True:
            frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, low16(frame.count))
            frame = _scene_refresh_decrement(frame, 'target_y', low16(frame.target_y))
            if low16(frame.target_y)==65535:
                break
        frame, finished = _dictionary_stream_finished_fields(memory, frame)
        if finished:
            return memory.sync_status(frame)

def _vdp_packet_spill_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        vertical: bool) -> FirstDeploymentFrame:
    """AD3A/AD5C: sole row/column boundary arithmetic, with true WORD carry."""
    if type(vertical) is not bool:
        raise ValueError('actual packet direction required')
    mask,shift = (0x1FFF,7) if vertical else (0x7F,1)
    frame = memory.sync_status(_first_word(frame,'count',low16(frame.unit)))
    frame = memory.sync_status(_first_word(frame,'count',low16(frame.count) & mask))
    frame = _scene_mode_lsr_word(memory,frame,'count',low16(frame.count),shift)
    frame = _scene_render_arithmetic(memory,frame,'count',low16(frame.count),low16(frame.target_x),16)
    total = low16(frame.count)
    frame = _scene_render_arithmetic(memory,frame,'count',total,0x40,16,True)
    if total < 0x40:
        frame = memory.sync_status(_first_word(frame,'count',0))
    return _scene_render_arithmetic(memory,frame,'target_x',low16(frame.target_x),low16(frame.count),16,True)

def _write_vdp_packet_run_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        carrier: str, recheck_tail: bool) -> FirstDeploymentFrame:
    """AD8C/ADB8: shared eight-WORD bulk path and exact distinct tail loops.

    D0 tail returns straight to DBRA. D3 tail reexecutes CMP.W #8 after
    every successful DBRA; this real distinction retains the last flags.
    """
    if carrier not in ('target_x','count') or type(recheck_tail) is not bool:
        raise ValueError('closed original packet loop role required')
    while True:
        remaining = low16(frame.carrier(carrier))
        frame = _scene_render_compare(memory,frame,remaining,8,16)
        if remaining >= 8:
            for unused in range(8):
                source = frame.roster
                value = source.word()
                frame = first_replace(frame,roster=source.advance(2))
                frame = _scene_refresh_emit(memory,frame,frame.auxiliary.base,2,value)
            frame = _scene_render_arithmetic(memory,frame,carrier,remaining,8,16,True)
            continue
        while True:
            source = frame.roster
            value = source.word()
            frame = first_replace(frame,roster=source.advance(2))
            frame = _scene_refresh_emit(memory,frame,frame.auxiliary.base,2,value)
            frame = _scene_refresh_decrement(frame,carrier,remaining)
            remaining = u16(remaining - 1)
            if remaining == 65535:
                return frame
            if recheck_tail:
                break

def write_vdp_packet_stream_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """AD1C..ADFC: sole full live row/column VDP packet stream.

    No IRQ or completion event is invented: this original body only writes
    the supplied real VDP port and reads the actual postincrement stream.
    """
    memory.frame(frame)
    if frame.roster is None or frame.target_x is None or frame.target_y is None or frame.count is None:
        raise SceneRefreshBoundary(0xAD1C,frame,None)
    while True:
        # Actual backedges return to AD1C, before LEA and MOVE.W #8F02.
        frame = first_replace(frame,auxiliary=memory.cursor_at(0xC00000))
        frame = memory.sync_status(_first_word(frame,'target_y',0x8F02))
        source = frame.roster
        count = source.word()
        frame = first_replace(frame,roster=source.advance(2))
        frame = memory.sync_status(_first_word(frame,'target_x',count))
        if count == 0:
            return _scene_refresh_emit(memory,frame,0xC00004,2,low16(frame.target_y))
        vertical = bool(count & 0x8000)
        if vertical:
            frame = memory.sync_status(_first_word(frame,'target_y',0x8F80))
            frame = memory.sync_status(_first_word(frame,'target_x',count & 0x7FFF))
        # MOVEQ #0,D2 is a genuine definition of all 32 bits, unlike a WORD
        # or BYTE observation in a historical convenience API.
        frame = memory.sync_status(_first_long(frame,'unit',0))
        source = frame.roster
        address = source.word()
        frame = first_replace(frame,roster=source.advance(2))
        frame = memory.sync_status(_first_word(frame,'unit',address))
        if vertical:
            frame = _vdp_packet_spill_fields(memory,frame,True)
        else:
            frame = memory.sync_status(_first_word(frame,'count',0))
            frame = _scene_render_bit(memory,frame,frame.target_x,0x4000)
            if not count & 0x4000:
                frame = _vdp_packet_spill_fields(memory,frame,False)
        frame = memory.sync_status(_first_word(frame,'target_x',low16(frame.target_x) & 0xBFFF))
        frame = _scene_render_arithmetic(memory,frame,'target_x',low16(frame.target_x),1,16,True)
        frame = _scene_refresh_emit(memory,frame,0xC00004,2,low16(frame.target_y))
        frame = _glyph_shift_long_fields(memory,frame,'unit',2)
        frame = _scene_mode_lsr_word(memory,frame,'unit',low16(frame.unit),2)
        frame = memory.sync_status(_first_word(frame,'unit',low16(frame.unit) | 0x4000))
        frame = memory.sync_status(_first_long(frame,'unit',swap_words(frame.unit)))
        frame = _scene_refresh_emit(memory,frame,0xC00004,4,frame.unit)
        frame = _write_vdp_packet_run_fields(memory,frame,'target_x',False)
        spill = low16(frame.count)
        frame = _scene_refresh_flags(memory,frame,spill,2)
        if spill == 0:
            continue
        frame = _scene_render_bit(memory,frame,frame.target_y,2)
        mask = 0xFF80FFFF if frame.target_y & 2 else 0xE07FFFFF
        frame = memory.sync_status(_first_long(frame,'unit',frame.unit & mask))
        frame = _scene_render_arithmetic(memory,frame,'count',spill,1,16,True)
        frame = _scene_refresh_emit(memory,frame,0xC00004,4,frame.unit)
        frame = _write_vdp_packet_run_fields(memory,frame,'count',True)

def _scene_tile_byte_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        name) -> tuple:
    """One actual BYTE source read and A0 postincrement."""
    memory.sync_status(frame)
    value = frame.roster.byte()
    frame = first_replace(frame,roster=frame.roster.advance(1))
    return _first_byte(frame,name,value),value

def _write_vdp_swapped_byte_rle_fields_core(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> tuple:
    """3AB52's sole swapped BYTE literal/repeat algorithm and observations.

    Legacy absence of D1/D2/D4 upper bits is None, not a fabricated zero.
    Only actual ASL.W8 uses D4's incoming high BYTE and changes X.
    """
    memory.frame(frame)
    if frame.roster is None or frame.target_x is None:
        raise SceneRefreshBoundary(0x3AB52,frame,None)
    frame = _scene_refresh_emit(memory,frame,0xC00004,2,0x8F02)
    frame = _scene_render_call_fields(memory,frame,0x3B2B0,0x3AB5E)
    frame,marker = _scene_tile_byte_fields(memory,frame,'target_y')
    last_word = None
    while True:
        frame,low = _scene_tile_byte_fields(memory,frame,'unit')
        frame = _scene_render_compare(memory,frame,marker,low,8)
        if marker != low:
            frame,high = _scene_tile_byte_fields(memory,frame,'distance')
            previous = None if frame.distance is None else low16(frame.distance)
            frame = _scene_render_asl_word(memory,frame,'distance',previous,8)
            frame = _first_byte(frame,'distance',low)
            last_word = high << 8 | low
            frame = _scene_refresh_emit(memory,frame,0xC00000,2,last_word)
        else:
            frame = _first_long(frame,'count',0)
            frame,count = _scene_tile_byte_fields(memory,frame,'count')
            if count == 0:
                return memory.sync_status(frame),marker,low,last_word
            frame,low = _scene_tile_byte_fields(memory,frame,'unit')
            frame,high = _scene_tile_byte_fields(memory,frame,'distance')
            previous = None if frame.distance is None else low16(frame.distance)
            frame = _scene_render_asl_word(memory,frame,'distance',previous,8)
            frame = _first_byte(frame,'distance',low)
            last_word = high << 8 | low
            remaining = count
            while True:
                frame = _scene_refresh_emit(memory,frame,0xC00000,2,last_word)
                frame = _scene_refresh_decrement(frame,'count',remaining)
                remaining = u16(remaining - 1)
                if remaining == 65535:
                    break

def write_vdp_swapped_byte_rle_stream_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Same sole decoder for complete physical-frame callers."""
    result,marker,token,last_word = _write_vdp_swapped_byte_rle_fields_core(memory,frame)
    return result

def advance_plane_row_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> tuple:
    """3AB32: actual row transition, including nonlocal MOVEM D0 discard.

    Ordinary RTS leaves its token for the inner caller to read. At the last
    row MOVEM consumes that same real token without altering SUBQ's CCR;
    the following RTS belongs to the enclosing decoder's original caller.
    """
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x3AB32,frame,None)
    frame = _scene_render_arithmetic(memory,frame,'distance',low16(frame.distance),1,16)
    column = low16(frame.distance)
    frame = _scene_render_compare(memory,frame,low8(column),32,8)
    if low8(column) >= 32:
        frame = _scene_render_arithmetic(memory,frame,'offset_y',low16(frame.offset_y),1,16,True)
        if low16(frame.offset_y) == 0:
            memory.sync_status(frame)
            discarded = frame.stack_cursor.long()
            frame = first_replace(frame,target_x=discarded,stack_cursor=frame.stack_cursor.advance(4))
            return memory.sync_status(frame),StackContinuation(discarded)
        frame = first_replace(frame,candidates=memory.cursor_at(u32(frame.candidates.base + frame.offset_x)))
        frame = _first_word(frame,'target_x',low16(frame.candidates.base))
        frame = _scene_render_call_fields(memory,frame,0x3B2B0,0x3AB4E)
        frame = _first_long(frame,'distance',0)
    return memory.sync_status(frame),None

def _scene_plane_row_call_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, continuation: Long) -> tuple:
    """Actual literal/repeat BSR; last-row discard has no false inner RTS."""
    if continuation not in (0x3AB10,0x3AB2C):
        raise ValueError('original plane row continuation required')
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x3AB32,frame,continuation)
    memory.sync_status(frame)
    frame = _scene_render_push_longs(memory,frame,(continuation,))
    returned,discarded = advance_plane_row_fields(memory,frame)
    if discarded is not None:
        return returned,discarded
    actual = returned.stack_cursor.long()
    if actual != continuation:
        raise SceneRefreshBoundary(0x3AB32,returned,continuation)
    returned = first_replace(returned,stack_cursor=returned.stack_cursor.advance(4))
    return memory.sync_status(returned),None

def _read_vdp_plane_rle_rows_fields_core(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, from_control: bool=False, from_literal: bool=False) -> tuple:
    """One complete plane decoder. Ordinary240334 resets mask/rows/mode; control240342 resets only mode; literal240346 preserves all three. Original packet order and final-row inner-token discard are shared."""
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(240334, frame, None)
    memory.sync_status(frame)
    if not from_control and (not from_literal):
        memory.state.read(4294934528, 2)
        frame = _scene_refresh_emit(memory, frame, 4294934528, 2, 0)
        frame = _first_word(frame, 'offset_y', 32)
    memory.sync_status(frame)
    if not from_literal:
        memory.state.read(4294934530, 2)
        frame = _scene_refresh_emit(memory, frame, 4294934530, 2, 0)
    frame = _scene_refresh_emit(memory, frame, 12582916, 2, 36610)
    frame = _first_word(frame, 'target_x', low16(frame.candidates.base))
    frame = _scene_render_call_fields(memory, frame, 242352, 240360)
    frame = _first_long(frame, 'distance', 0)
    memory.sync_status(frame)
    mode = memory.state.read(4294934530, 2)
    frame = _scene_refresh_flags(memory, frame, mode, 2)
    if mode == 0:
        frame, marker = _scene_tile_byte_fields(memory, frame, 'target_y')
    while True:
        frame, high = _scene_tile_byte_fields(memory, frame, 'unit')
        memory.sync_status(frame)
        mode = memory.state.read(4294934530, 2)
        frame = _scene_refresh_flags(memory, frame, mode, 2)
        marker = low8(frame.target_y)
        if mode == 0:
            frame = _scene_render_compare(memory, frame, marker, high, 8)
        literal = mode != 0 or marker != high
        if literal:
            frame = _scene_render_asl_word(memory, frame, 'unit', low16(frame.unit), 8)
            frame, low = _scene_tile_byte_fields(memory, frame, 'unit')
            memory.sync_status(frame)
            mask = memory.state.read(4294934528, 2)
            frame = _first_word(frame, 'unit', low16(frame.unit) | mask)
            frame = _scene_refresh_emit(memory, frame, 12582912, 2, low16(frame.unit))
            frame, discarded = _scene_plane_row_call_fields(memory, frame, 240400)
            if discarded is not None:
                return (frame, discarded)
        else:
            frame = _first_long(frame, 'count', 0)
            frame, count = _scene_tile_byte_fields(memory, frame, 'count')
            if count == 0:
                return (memory.sync_status(frame), None)
            frame, high = _scene_tile_byte_fields(memory, frame, 'unit')
            frame = _scene_render_asl_word(memory, frame, 'unit', low16(frame.unit), 8)
            frame, low = _scene_tile_byte_fields(memory, frame, 'unit')
            remaining = count
            while True:
                memory.sync_status(frame)
                mask = memory.state.read(4294934528, 2)
                frame = _first_word(frame, 'unit', low16(frame.unit) | mask)
                frame = _scene_refresh_emit(memory, frame, 12582912, 2, low16(frame.unit))
                frame, discarded = _scene_plane_row_call_fields(memory, frame, 240428)
                if discarded is not None:
                    return (frame, discarded)
                frame = _scene_refresh_decrement(frame, 'count', remaining)
                remaining = u16(remaining - 1)
                if remaining == 65535:
                    break

def read_vdp_plane_rle_rows_from_literal_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """240346 internal BRA entry; preserve8002 literal mode and caller D6. No new CALL slot."""
    frame, discarded = _read_vdp_plane_rle_rows_fields_core(memory, frame, False, True)
    return frame

def read_vdp_plane_rle_rows_from_control_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3AAD6: preserve the genuine caller's8000 mask and D6 row count.

    The shared complete RLE body still performs the real8002 clear, VDP
    writes, nested row CALLs and final-row inner continuation discard.
    """
    frame, discarded = _read_vdp_plane_rle_rows_fields_core(memory, frame, True)
    return frame


def read_vdp_plane_rle_rows_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame,discarded = _read_vdp_plane_rle_rows_fields_core(memory,frame)
    return frame

def _copy_scene_palette_variant_fields_core(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> tuple:
    """3AB94's sole signed-directory lookup and inclusive LONG copy."""
    memory.frame(frame)
    if frame.target_x is None:
        raise SceneRefreshBoundary(0x3AB94,frame,None)
    frame = first_replace(frame,candidates=memory.cursor_at(0x3ABAC))
    frame = _first_shift_word(frame,'target_x',low16(frame.target_x),3)
    frame = first_replace(frame,candidates=frame.candidates.advance(s16(low16(frame.target_x))))
    memory.sync_status(frame)
    pointer = frame.candidates.long()
    frame = first_replace(frame,controller=memory.cursor_at(pointer),candidates=frame.candidates.advance(4))
    pointer = frame.candidates.word()
    frame = first_replace(frame,scan=memory.cursor_at(u32(s16(pointer))),candidates=frame.candidates.advance(2))
    counter = frame.candidates.word()
    frame = first_replace(frame,candidates=frame.candidates.advance(2))
    frame = _first_word(frame,'choice',counter)
    while True:
        memory.sync_status(frame)
        pair = frame.controller.long()
        frame.scan.set_long(0,pair)
        frame = _scene_refresh_flags(memory,frame,pair,4)
        frame = first_replace(frame,controller=frame.controller.advance(4),scan=frame.scan.advance(4))
        frame = _scene_refresh_decrement(frame,'choice',counter)
        counter = u16(counter - 1)
        if counter == 65535:
            return memory.sync_status(frame),pair

def copy_scene_palette_variant_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame,pair = _copy_scene_palette_variant_fields_core(memory,frame)
    return frame

def _begin_scene_palette_darken_fields_core(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> tuple:
    """3AA20's WORD period mask and three MOVE stores; no false CLR read."""
    memory.frame(frame)
    if frame.target_x is None:
        raise SceneRefreshBoundary(0x3AA20,frame,None)
    frame = _first_word(frame,'target_x',low16(frame.target_x) & 255)
    frame = _scene_refresh_emit(memory,frame,0xFFFF80C4,2,low16(frame.target_x))
    frame = _scene_refresh_emit(memory,frame,0xFFFF80C6,2,0)
    shade = 15
    return _scene_refresh_emit(memory,frame,0xFFFF80C8,2,shade),shade

def begin_scene_palette_darken_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame,shade = _begin_scene_palette_darken_fields_core(memory,frame)
    return frame

def snapshot_and_clear_scene_palette_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3AA8A: paired LONG copy/CLR, both genuine reads and live cursors."""
    memory.frame(frame)
    longs = 32
    frame = _first_long(frame,'target_y',longs - 1)
    frame = first_replace(frame,roster=memory.cursor_at(0xFFFFFB00),candidates=memory.cursor_at(0xFFFFFB80))
    counter = longs - 1
    while True:
        memory.sync_status(frame)
        pair = frame.roster.long()
        frame.candidates.set_long(0,pair)
        frame = _scene_refresh_flags(memory,frame,pair,4)
        frame = first_replace(frame,candidates=frame.candidates.advance(4))
        frame.roster.long()
        frame.roster.set_long(0,0)
        frame = _scene_refresh_flags(memory,frame,0,4)
        frame = first_replace(frame,roster=frame.roster.advance(4))
        frame = _scene_refresh_decrement(frame,'target_y',counter)
        counter = u16(counter - 1)
        if counter == 65535:
            return memory.sync_status(frame)


"""Original live palette conversion, not a hardware-completion substitute."""


def darken_palette_component_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """DEF4: rotate one packed color channel, subtract shade and append nibble."""
    memory.frame(frame)
    if any(value is None for value in (frame.target_x,frame.unit,frame.count,frame.distance,frame.status)):
        raise SceneRefreshBoundary(0xDEF4,frame,None)
    frame = _first_shift_word(frame,'distance',low16(frame.distance),4)
    color = _rol_word(frame.unit,4)
    flags = (8 if low16(color) & 32768 else 0) | (4 if low16(color)==0 else 0) | (low16(color) & 1)
    frame = first_replace(frame,unit=color,status=(frame.status & 16) | flags)
    memory.sync_status(frame)
    frame = _first_byte(frame,'count',low8(frame.unit))
    frame = _first_word(frame,'count',low16(frame.count) & 14)
    frame,value = _movement_binary_flags(memory.state,frame,low8(frame.count),low8(frame.target_x),8,True)
    frame = first_replace(frame,count=replace_byte(frame.count,value))
    if frame.status & 1:
        frame = _first_byte(frame,'count',0)
    return memory.sync_status(_first_word(frame,'distance',low16(frame.distance) | low16(frame.count)))


def _darken_palette_component_call_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, continuation: int) -> FirstDeploymentFrame:
    """The three actual BSR LONGs are observed once, including return aliases."""
    from ..high_level_gameplay_flow.business_battle import _presentation_call_fields
    from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
    if continuation not in (0xDED0,0xDED4,0xDED8):
        raise ValueError('original darken component return required')
    def child(actual,entered):
        return darken_palette_component_fields(SceneRefreshMemory(actual.state),entered)
    return _presentation_call_fields(BattlePresentationMemory(memory.state),frame,continuation,child)


def darken_palette_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """DEA6..DEF4: live shade/count palette conversion and final backdrop copies."""
    memory.frame(frame)
    if any(value is None for value in (frame.target_x,frame.target_y,frame.unit,
            frame.count,frame.distance,frame.roster,frame.stack_cursor,frame.status)):
        raise SceneRefreshBoundary(0xDEA6,frame,None)
    shade_ceiling = 15
    frame = _movement_compare(memory.state,frame,low16(frame.target_x),shade_ceiling,16)
    if low16(frame.target_x) > shade_ceiling:
        # Preserve the real nonprogressing branch. No invented successful palette.
        raise SceneRefreshBoundary(0xDEAC,frame,'original shade WORD above15 loops here')
    frame = first_replace(frame,candidates=memory.cursor_at(0xFFFFFB00))
    present = bool(frame.target_x & 1)
    frame = first_replace(frame,status=(frame.status & 27) | (0 if present else 4))
    if present:
        present = bool(memory.state.read(0xFFFFF320,1) & 1)
        frame = first_replace(frame,status=(frame.status & 27) | (0 if present else 4))
        if present:
            from ..high_level_main_flows.business_movement_support import _movement_add_word
            frame = _movement_add_word(memory.state,frame,'target_x',1)
    present = bool(frame.target_x & 1)
    frame = first_replace(frame,target_x=frame.target_x & 4294967294,
        status=(frame.status & 27) | (0 if present else 4))
    while True:
        # DBRA returns to this original CLR, not past it: reset every color.
        frame = _first_word(frame,'distance',0)
        memory.sync_status(frame)
        color = frame.roster.word()
        frame = first_replace(frame,roster=frame.roster.advance(2))
        frame = _first_word(frame,'unit',color)
        frame = _first_shift_word(frame,'unit',low16(frame.unit),4)
        for continuation in (0xDED0,0xDED4,0xDED8):
            frame = _darken_palette_component_call_fields(memory,frame,continuation)
        value = low16(frame.distance)
        frame.candidates.set_word(0,value)
        frame = _scene_refresh_flags(memory,frame,value,2)
        frame = first_replace(frame,candidates=frame.candidates.advance(2))
        counter = u16(low16(frame.target_y)-1)
        frame = first_replace(frame,target_y=replace_word(frame.target_y,counter))
        if counter == 65535:
            break
    previous = memory.state.read(0xFFFFF31E,2)
    frame,value = _movement_binary_flags(memory.state,frame,previous,1,16)
    memory.state.write(0xFFFFF31E,2,value)
    memory.sync_status(frame)
    frame = _first_word(frame,'target_x',memory.state.read(0xFFFFFB00,2))
    for destination in (0xFFFFFB20,0xFFFFFB40,0xFFFFFB60):
        frame = _scene_refresh_emit(memory,frame,destination,2,low16(frame.target_x))
    return memory.sync_status(frame)

def sample_random_preserving_seed_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3B722: one real D1 LONG save and 83D4 call, then live MOVEM readback.

    Only the already-shared random core defines D0/CCR. An unobserved legacy
    D1 remains unknown; no secondary carrier or physical stack is invented.
    """
    from ..high_level_battle_ai.business_formation import first_deployment_random_fields
    from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
    from ..high_level_gameplay_flow.business_battle import _presentation_call_fields
    from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
    memory.frame(frame)
    retained_secondary = frame.target_y
    frame = _scene_render_push_longs(memory,frame,(retained_secondary,))
    def child(actual_memory,entered):
        return first_deployment_random_fields(BattlePolicyMemory(actual_memory.state),entered)
    frame = _presentation_call_fields(BattlePresentationMemory(memory.state),frame,0x3B72C,child)
    if frame.stack_cursor is not None:
        retained_secondary = frame.stack_cursor.long()
        frame = first_replace(frame,stack_cursor=frame.stack_cursor.advance(4))
    return memory.sync_status(first_replace(frame,target_y=retained_secondary))

def finish_one_actor_sprite_chain_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3B272 reuses the existing 3A78C head/tail protocol without another loop."""
    if frame.target_x is None:
        raise SceneRefreshBoundary(0x3B272,frame,None)
    return finish_one_scene_sprite_chain_fields(memory,frame)

def finish_actor_sprite_chains_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3B23C: descending actor layers, real child slots, and MOVE-only reset."""
    from ..high_level_gameplay_flow.business_battle import _presentation_call_fields
    from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
    memory.frame(frame)
    frame = _first_long(frame,'target_x',28)
    frame = _first_long(frame,'target_y',0)
    frame = first_replace(frame,roster=memory.cursor_at(0xFFFF8044))
    def child(actual_memory,entered):
        return finish_one_actor_sprite_chain_fields(SceneRefreshMemory(actual_memory.state),entered)
    while True:
        frame = _presentation_call_fields(BattlePresentationMemory(memory.state),frame,0x3B246,child)
        frame = _scene_render_arithmetic(memory,frame,'target_x',low16(frame.target_x),4,16,True)
        if low16(frame.target_x) & 32768:
            break
    frame = _first_long(frame,'target_x',0)
    for displacement in (0,4,8,12,16,20,24,28):
        frame = _scene_refresh_emit(memory,frame,u32(frame.roster.base + displacement),4,frame.target_x)
    # Immediate MOVE.B zero is not CLR; there is no prior destination read.
    return _scene_refresh_emit(memory,frame,0xFFFFF300,1,0)

def _scene_fade_rotate_word_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, name: str, amount: Word) -> FirstDeploymentFrame:
    """ROR.W keeps X; its carry is the last rotated low bit, not a shift X."""
    original = frame.carrier(name)
    if original is None:
        raise SceneRefreshBoundary(0x3AA1A,frame,None)
    result = _ror_word(original,amount)
    flags = (8 if low16(result) & 32768 else 0) | (4 if low16(result) == 0 else 0)
    if low16(original) & (1 << (amount - 1)):
        flags |= 1
    status = None if frame.status is None else (frame.status & 16) | flags
    return memory.sync_status(first_replace(frame,**{name:result},status=status))

def fade_palette_component_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3AA0A: one real shade BYTE read, WORD nibble rotations and full X."""
    from .business_objects import _object_shift_word_right_fields
    memory.frame(frame)
    if any(value is None for value in (frame.count,frame.distance,frame.offset_x)):
        raise SceneRefreshBoundary(0x3AA0A,frame,None)
    frame = _first_byte(frame,'distance',low8(frame.count))
    frame = _first_word(frame,'distance',low16(frame.distance) & 14)
    memory.sync_status(frame)
    shade = memory.state.read(0xFFFF8001,1)
    frame,value = _movement_binary_flags(memory.state,frame,low8(frame.distance),shade,8,True)
    frame = first_replace(frame,distance=replace_byte(frame.distance,value))
    if frame.status & 1:
        frame = _first_long(frame,'distance',0)
    frame = _first_word(frame,'offset_x',low16(frame.offset_x) | low16(frame.distance))
    frame = _scene_fade_rotate_word_fields(memory,frame,'offset_x',4)
    frame,shifted_color = _object_shift_word_right_fields(memory,frame,'count',low16(frame.count),4)
    return memory.sync_status(frame)

def advance_scene_palette_fade_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3A978: two live 32-color masks, real BSR slots, no fabricated color highs."""
    from ..high_level_gameplay_flow.business_battle import _presentation_call_fields
    from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
    from .business_objects import _object_adjust_word_fields
    memory.frame(frame)
    memory.sync_status(frame)
    mode = memory.state.read(0xFFFF80C4,2)
    frame = _first_word(frame,'target_x',mode)
    if mode & 32768:
        return frame
    frame = _object_adjust_word_fields(memory,frame,0xFFFF80C6,1,True)
    if not frame.status & 8:
        return frame
    period = mode & 255
    frame = _first_word(frame,'target_x',period)
    frame = _scene_refresh_emit(memory,frame,0xFFFF80C6,2,period)
    mode_byte = memory.state.read(0xFFFF80C4,1)
    frame = _scene_render_compare(memory,frame,mode_byte,0,8)
    if mode_byte == 0:
        frame = _object_adjust_word_fields(memory,frame,0xFFFF80C8,1,True)
        finished = bool(frame.status & 8)
    else:
        frame = _object_adjust_word_fields(memory,frame,0xFFFF80C8,1)
        shade = memory.state.read(0xFFFF80C8,2)
        frame = _scene_render_compare(memory,frame,shade,15,16)
        finished = shade > 15
    if finished:
        return _scene_refresh_emit(memory,frame,0xFFFF80C4,2,65535)
    shade = memory.state.read(0xFFFF80C8,2)
    frame = _first_word(frame,'target_x',shade)
    frame = _first_word(frame,'target_x',shade & 14)
    frame = _scene_refresh_emit(memory,frame,0xFFFF8000,2,low16(frame.target_x))
    frame = first_replace(frame,roster=memory.cursor_at(0xFFFFFB00),
        candidates=memory.cursor_at(0xFFFFFB80),controller=memory.cursor_at(0xFFFF80CA))
    frame = _first_long(frame,'unit',0)
    frame = _first_long(frame,'choice',0)
    while True:
        frame = _first_long(frame,'target_y',31)
        frame = _first_long(frame,'offset_y',frame.controller.long(low16(frame.choice)))
        while True:
            mask = frame.offset_y
            frame = first_replace(frame,offset_y=mask >> 1,
                status=(17 if mask & 1 else 0) | (4 if mask >> 1 == 0 else 0))
            memory.sync_status(frame)
            if mask & 1:
                frame = _first_word(frame,'offset_x',0)
                frame = _first_word(frame,'count',frame.candidates.word(low16(frame.unit)))
                if frame.stack_cursor is None or any(value is None for value in (frame.count,frame.distance,frame.offset_x)):
                    raise SceneRefreshBoundary(0x3AA0A,frame,0x3A9EC)
                for continuation in (0x3A9EC,0x3A9F0,0x3A9F4):
                    def component(actual_memory,entered):
                        return fade_palette_component_fields(SceneRefreshMemory(actual_memory.state),entered)
                    frame = _presentation_call_fields(BattlePresentationMemory(memory.state),frame,continuation,component)
                frame = _scene_fade_rotate_word_fields(memory,frame,'offset_x',4)
                frame = _scene_refresh_emit(memory,frame,u32(frame.roster.base + s16(low16(frame.unit))),2,low16(frame.offset_x))
            frame = _scene_render_arithmetic(memory,frame,'unit',low16(frame.unit),2,16)
            frame = _scene_refresh_decrement(frame,'target_y',low16(frame.target_y))
            if low16(frame.target_y) == 65535:
                break
        frame = _scene_render_arithmetic(memory,frame,'choice',low16(frame.choice),4,16)
        frame = _scene_render_compare(memory,frame,low16(frame.choice),8,16)
        if low16(frame.choice) >= 8:
            return memory.sync_status(frame)


def flush_scene_transfer_queue_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Actual BSR.B atAD10 writes its one LONG return AD12, not AD14."""
    from ..high_level_remaining_flows.business_city import _resource_cost_frame
    from ..high_level_main_flows.business_movement_support import _movement_test
    from ..high_level_gameplay_flow.business_battle import _presentation_call_fields
    from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
    if type(memory) is not SceneRefreshMemory:
        raise ValueError('actual same Scene transfer memory required')
    state = memory.state
    frame = _resource_cost_frame(state, frame, 44294)
    queued_words = state.read(4294955264, 2)
    frame = _movement_test(state, frame, queued_words, 16)
    if queued_words != 0:
        frame = first_replace(frame, roster=memory.cursor_at(4294955264))

        def child(actual, entered):
            return write_vdp_packet_stream_fields(SceneRefreshMemory(actual.state), entered)
        frame = _presentation_call_fields(BattlePresentationMemory(state), frame, 44306, child)
    for address in (4294963994, 4294955264):
        state.read(address, 2)
        state.write(address, 2, 0)
        frame = _movement_test(state, frame, 0, 16)
    return frame


# C53 named Scene presentation roles; true hardware/callee boundaries retained.
def _story_move_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        name, value: Long, width: Word = 16) -> FirstDeploymentFrame:
    """Reuse the unique width-aware MOVE implementation; retain unseen high bits."""
    from ..high_level_dynamic_flows.business_early_phase import _allocation_move_fields
    return _allocation_move_fields(memory, frame, name, value, width)


def _story_read_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        address: Long, size: Word = 2):
    memory.sync_status(frame)
    return memory.state.read(address, size)


def _story_ram_move_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        name, low: Word, width: Word = 16) -> FirstDeploymentFrame:
    return _story_move_fields(memory, frame, name,
        _story_read_fields(memory, frame, 0xFFFF0000 | low, width // 8), width)


def _story_store_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        address: Long, value: Long, size: Word = 2) -> FirstDeploymentFrame:
    """Do not normalize bus literals: original abs.W and abs.L are distinct events."""
    return _scene_refresh_emit(memory, frame, address, size, value)


def _story_clear_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        low: Word) -> FirstDeploymentFrame:
    from .business_objects import _object_clear_word_fields
    return _object_clear_word_fields(memory, frame, 0xFFFF0000 | low)


def _story_add_ram_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        low: Word, amount: Word = 1) -> FirstDeploymentFrame:
    from .business_objects import _object_adjust_word_fields
    return _object_adjust_word_fields(memory, frame, 0xFFFF0000 | low, amount)


def _story_compare_ram_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        low: Word, value: Word) -> FirstDeploymentFrame:
    return _scene_render_compare(memory, frame,
        _story_read_fields(memory, frame, 0xFFFF0000 | low), value, 16)


def _story_arithmetic_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        name, value: Word, subtract: bool = False) -> FirstDeploymentFrame:
    return _scene_render_arithmetic(memory, frame, name,
        low16(frame.carrier(name)), value, 16, subtract)


def _story_status_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        value: Word) -> FirstDeploymentFrame:
    memory.state.set_status_word(value)
    return first_replace(frame, status=value & 31)


def _story_mask_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        name, mask: Word, width: Word = 16) -> FirstDeploymentFrame:
    return _story_move_fields(memory, frame, name,
        frame.carrier(name) & mask & ((1 << width) - 1), width)


def _story_palette_masks_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        masks: tuple) -> FirstDeploymentFrame:
    if len(masks) != 4:
        raise ValueError('four original palette masks required')
    for index, value in enumerate(masks):
        frame = _story_store_fields(memory, frame, 0xFFFF80CA + index * 2, value)
    return frame


def _story_clear_plane_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    from ..high_level_dynamic_flows.business_early_phase import _allocation_fill_fields
    return _allocation_fill_fields(memory, frame, 0x60000002, 0x3333, 0x0D7F, True)


def _story_script_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        source: Long, dimensions: bool = False) -> FirstDeploymentFrame:
    frame = _story_store_fields(memory, frame, 0x00FF700C, 0xA000)
    frame = _story_store_fields(memory, frame, 0x00FF700E, source, 4)
    if dimensions:
        frame = _story_store_fields(memory, frame, 0x00FF7014, 3)
        frame = _story_store_fields(memory, frame, 0x00FF7016, 1)
    return frame


def _story_finish_stage_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        counters: tuple = (0x813A,)) -> FirstDeploymentFrame:
    for low in counters:
        frame = _story_clear_fields(memory, frame, low)
    return _story_add_ram_fields(memory, frame, 0x80EA)


def _story_pressed_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> tuple:
    value = _story_read_fields(memory, frame, 0xFFFF80C4, 1)
    return _scene_render_bit(memory, frame, value, 128), bool(value & 128)


def _story_lighten_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        continuation: Long) -> FirstDeploymentFrame:
    frame = _story_move_fields(memory, frame, 'target_x', 1, 32)
    return _story_call_fields(memory, frame, 0x3AA38, continuation)


def _story_darken_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        continuation: Long) -> FirstDeploymentFrame:
    """The original MOVEQ1 and CALL3AA20; reuse the sole palette owner."""
    frame = _story_move_fields(memory, frame, 'target_x', 1, 32)
    return _story_call_fields(memory, frame, 0x3AA20, continuation)


def _story_call_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        target: Long, continuation: Long) -> FirstDeploymentFrame:
    """Caller owns one real LONG. Unknown children stop after that physical write."""
    memory.frame(frame)
    memory.sync_status(frame)
    entered = _scene_render_push_longs(memory, frame, (continuation,))
    result = _story_known_fields(memory, entered, target)
    memory.frame(result)
    if frame.stack_cursor is not None:
        actual = result.stack_cursor.long()
        if actual != continuation:
            raise SceneRefreshBoundary(target, result, continuation)
        result = first_replace(result, stack_cursor=result.stack_cursor.advance(4))
    return memory.sync_status(result)


def _story_decode_picture_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        source: Long, continuation: Long) -> FirstDeploymentFrame:
    frame = first_replace(frame, roster=memory.cursor_at(source),
        candidates=memory.cursor_at(0x0000E000))
    frame = _story_move_fields(memory, frame, 'offset_x', 0x80, 32)
    frame = _story_move_fields(memory, frame, 'offset_y', 0x12)
    return _story_call_fields(memory, frame, 0x3AACE, continuation)


def _story_glyph_upload_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        rows: Word) -> FirstDeploymentFrame:
    """Ordered LONG writes to the real VDP port; no RAM-backed device substitute."""
    frame = first_replace(frame, auxiliary=memory.cursor_at(0x00C00000))
    frame = _story_move_fields(memory, frame, 'target_x', rows)
    return _story_upload_current_rows_fields(memory,frame)

def _story_initialize_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        scene) -> FirstDeploymentFrame:
    """Five closed story roles share the actual plane fill and palette algorithm."""
    memory.frame(frame)
    if scene == 'prologue':
        masks, palette_return, row_return, source = (0xFFFF,0,0xFFFF,0xFFFF),0x3B802,None,0x3B4D8
    elif scene == 'departure':
        masks, palette_return, row_return, source = (0xFFFF,)*4,0x3C1DE,0x3C1E2,0x3B588
    elif scene == 'interlude':
        masks, palette_return, row_return, source = (0xFFFF,)*4,0x3C9A8,0x3C9AC,0x3B6E4
    elif scene == 'arrival':
        masks, palette_return, row_return, source = (0xFFFF,)*4,0x3CAE6,None,0x3B614
    elif scene == 'finale':
        masks, palette_return, row_return, source = (0xFFFF,)*4,0x3D1BA,None,None
    else:
        raise ValueError('closed story initialization role required')
    if scene != 'prologue':
        frame = _story_status_fields(memory,frame,0x2700)
    frame = _story_palette_masks_fields(memory,frame,masks)
    frame = _story_move_fields(memory,frame,'target_x',1,32)
    frame = _story_call_fields(memory,frame,0x3AA20,palette_return)
    if row_return is not None:
        frame = _story_call_fields(memory,frame,0x3C23A,row_return)
    if scene == 'prologue':
        frame = _story_status_fields(memory,frame,0x2700)
    frame = _story_clear_plane_fields(memory,frame)
    if source is None:
        frame = _story_store_fields(memory,frame,0x00FF7014,3)
        frame = _story_store_fields(memory,frame,0x00FF7016,1)
    else:
        frame = _story_script_fields(memory,frame,source,True)
    if scene == 'prologue':
        frame = _story_status_fields(memory,frame,0x2500)
    else:
        frame = _story_store_fields(memory,frame,0xFFFF813C,3)
    frame = _story_add_ram_fields(memory,frame,0x80EA)
    if scene != 'prologue':
        frame = _story_status_fields(memory,frame,0x2500)
    return memory.sync_status(frame)


def _story_timer_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        threshold: Word, masks: tuple | None, fade_return: Long | None,
        source: Long | None, counters: tuple) -> FirstDeploymentFrame:
    """The common timed transition, preserving real comparisons and source-write order."""
    frame = _story_add_ram_fields(memory,frame,0x813A)
    frame = _story_compare_ram_fields(memory,frame,0x813A,threshold)
    if frame.status & 1:
        return frame
    if masks is not None:
        frame = _story_palette_masks_fields(memory,frame,masks)
    if fade_return is not None:
        frame = _story_lighten_fields(memory,frame,fade_return)
    if source is not None:
        frame = _story_status_fields(memory,frame,0x2700)
        frame = _story_clear_plane_fields(memory,frame)
        frame = _story_script_fields(memory,frame,source)
        frame = _story_status_fields(memory,frame,0x2500)
    return _story_finish_stage_fields(memory,frame,counters)


def _story_caption_trigger_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        threshold: Word, source: Long) -> FirstDeploymentFrame:
    frame = _story_compare_ram_fields(memory,frame,0x813A,threshold)
    if frame.status & 4:
        frame = _story_status_fields(memory,frame,0x2700)
        frame = _story_clear_plane_fields(memory,frame)
        frame = _story_script_fields(memory,frame,source)
        frame = _story_status_fields(memory,frame,0x2500)
    return frame


def _story_confirm_page_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        picture: Long, picture_return: Long, source: Long) -> tuple:
    frame, pressed = _story_pressed_fields(memory,frame)
    if not pressed:
        return frame,False
    frame = _story_status_fields(memory,frame,0x2700)
    frame = _story_decode_picture_fields(memory,frame,picture,picture_return)
    frame = _story_clear_plane_fields(memory,frame)
    frame = _story_script_fields(memory,frame,source)
    return _story_status_fields(memory,frame,0x2500),True


def _story_exit_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame, pressed = _story_pressed_fields(memory,frame)
    if pressed:
        return _story_known_fields(memory,frame,0x206)
    return memory.sync_status(frame)


def initialize_prologue_story_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3B7BC complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    return _story_initialize_fields(memory,frame,'prologue')

def initialize_departure_story_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3C19C complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    return _story_initialize_fields(memory,frame,'departure')

def initialize_interlude_story_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3C97A complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    return _story_initialize_fields(memory,frame,'interlude')

def initialize_arrival_story_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3CAA4 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    return _story_initialize_fields(memory,frame,'arrival')

def initialize_finale_story_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3D17C complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    return _story_initialize_fields(memory,frame,'finale')

def reveal_prologue_caption_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3B7C0 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3B8D0,0x3B85C)
    frame = _story_add_ram_fields(memory,frame,0x813A)
    frame = _story_compare_ram_fields(memory,frame,0x813A,0x200)
    if frame.status & 1:
        return frame
    frame = _story_palette_masks_fields(memory,frame,(0,0xFFFF,0,0))
    frame = _story_darken_fields(memory,frame,0x3B886)
    frame = _story_status_fields(memory,frame,0x2700)
    frame = _story_clear_plane_fields(memory,frame)
    frame = _story_script_fields(memory,frame,0x3B506)
    frame = _story_status_fields(memory,frame,0x2500)
    return _story_finish_stage_fields(memory,frame,(0x813A,))

def wait_prologue_portrait_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3B7C4 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3B8D0,0x3B8E6)
    return _story_timer_fields(memory,frame,0x200,None,0x3B8F8,None,(0x813A,))

def wait_prologue_second_page_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3B7CC complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3B8D0,0x3B97E)
    return _story_timer_fields(memory,frame,0x200,None,0x3B990,None,(0x813A,))

def reveal_prologue_second_portrait_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3B7D0 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3B8D0,0x3B99E)
    return _story_timer_fields(memory,frame,0x40,(0xFFFF,0xFFFF,0,0xFFFF),0x3B9C8,None,(0x813A,))

def begin_prologue_closing_caption_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3B7D8 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3BAB0,0x3BA56)
    frame = _story_call_fields(memory,frame,0x3BAE6,0x3BA5A)
    return _story_timer_fields(memory,frame,0x200,None,None,0x3BB92,(0x813A,))

def finish_prologue_closing_caption_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3B7DC complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3BAB0,0x3BB5A)
    frame = _story_call_fields(memory,frame,0x3BAE6,0x3BB5E)
    return _story_timer_fields(memory,frame,0x19C0,(0xFFFF,)*4,0x3BB88,None,(0x813A,))

def wait_departure_second_page_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3C1A8 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3C49E,0x3C482)
    return _story_timer_fields(memory,frame,0x200,None,0x3C494,None,(0x813A,))

def begin_departure_closing_caption_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3C1B0 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3C5C6,0x3C570)
    return _story_timer_fields(memory,frame,0x200,None,None,0x3BB92,(0x813A,))

def finish_departure_closing_caption_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3C1B4 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3C5C6,0x3C682)
    return _story_timer_fields(memory,frame,0x1B80,(0xFFFF,)*4,0x3C6AC,None,(0x813A,))

def wait_arrival_second_page_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3CAB0 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3CC82,0x3CC62)
    return _story_timer_fields(memory,frame,0x200,None,0x3CC74,None,(0x813A,0x813C))

def begin_arrival_closing_caption_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3CAB8 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3CD98,0x3CD42)
    return _story_timer_fields(memory,frame,0x200,None,None,0x3BB92,(0x813A,))

def finish_arrival_closing_caption_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3CABC complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3CD98,0x3CDC2)
    return _story_timer_fields(memory,frame,0x1B80,(0xFFFF,)*4,0x3CDEC,None,(0x813A,))

def wait_finale_scroll_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3D188 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3D346,0x3D32C)
    return _story_timer_fields(memory,frame,0x100,None,None,None,(0x813A,0x813C))

def finish_finale_closing_caption_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3D190 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3D41C,0x3D3E8)
    return _story_timer_fields(memory,frame,0x3C0,(0xFFFF,)*4,0x3D412,None,(0x813A,))

def reveal_departure_caption_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3C1A0 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3C3A4,0x3C328)
    frame = _story_caption_trigger_fields(memory,frame,0x200,0x3B59E)
    return _story_timer_fields(memory,frame,0x200,(0xFFFF,0xFFFF,0,0xFFFF),0x3C39A,None,(0x813A,))

def reveal_interlude_caption_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3C97E complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3C3A4,0x3CA08)
    frame = _story_caption_trigger_fields(memory,frame,0x100,0x3B6FA)
    return _story_timer_fields(memory,frame,0x3C0,(0xFFFF,)*4,0x3CA7A,None,(0x813A,))

def reveal_arrival_caption_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3CAA8 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3CBBE,0x3CB42)
    frame = _story_caption_trigger_fields(memory,frame,0x200,0x3B630)
    return _story_timer_fields(memory,frame,0x200,(0xFFFF,0xFFFF,0,0xFFFF),0x3CBB4,None,(0x813A,))

def reveal_finale_caption_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3D180 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3D280,0x3D204)
    frame = _story_caption_trigger_fields(memory,frame,0xC0,0x3B6A8)
    return _story_timer_fields(memory,frame,0x140,(0xFFFF,0xFFFF,0,0xFFFF),0x3D276,None,(0x813A,))

def confirm_prologue_exit_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3B7E0 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3BAB0,0x3BBB0)
    return _story_exit_fields(memory,frame)

def confirm_departure_exit_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3C1B8 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3C5C6,0x3C6BA)
    return _story_exit_fields(memory,frame)

def confirm_interlude_exit_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3C982 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3C3A4,0x3CA88)
    return _story_exit_fields(memory,frame)

def confirm_finale_exit_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3D194 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3D41C,0x3D44A)
    return _story_exit_fields(memory,frame)

def confirm_arrival_exit_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3CAC0 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    return _story_exit_fields(memory,frame)

def confirm_prologue_first_page_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3B7C8 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3B8D0,0x3B906)
    frame, pressed = _story_confirm_page_fields(memory,frame,0x4632A,0x3B92E,0x3B532)
    if not pressed:
        return frame
    frame = _story_darken_fields(memory,frame,0x3B970)
    frame = _story_finish_stage_fields(memory,frame,(0x813A,))
    return memory.sync_status(frame)

def confirm_departure_first_page_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3C1A4 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3C3A4,0x3C40A)
    frame, pressed = _story_confirm_page_fields(memory,frame,0x46FCD,0x3C432,0x3B5B8)
    if not pressed:
        return frame
    frame = _story_darken_fields(memory,frame,0x3C474)
    frame = _story_finish_stage_fields(memory,frame,(0x813A,))
    return memory.sync_status(frame)

def confirm_departure_second_page_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3C1AC complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3C49E,0x3C4CC)
    frame, pressed = _story_confirm_page_fields(memory,frame,0x47248,0x3C4F4,0x3B5E8)
    if not pressed:
        return frame
    frame = _story_palette_masks_fields(memory,frame,(0xFFFF,0xFFFF,0,0xFFFF))
    frame = _story_darken_fields(memory,frame,0x3C54E)
    frame = _story_finish_stage_fields(memory,frame,(0x813A,0x813C,0x813E,0x8140,0x8142,0x8144))
    return memory.sync_status(frame)

def confirm_arrival_first_page_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3CAAC complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3CBBE,0x3CBE6)
    frame, pressed = _story_pressed_fields(memory,frame)
    if not pressed:
        return frame
    frame = _story_status_fields(memory,frame,0x2700)
    frame = first_replace(frame,roster=memory.cursor_at(0x45AE1),
        candidates=memory.cursor_at(0x0000E000))
    frame = _story_move_fields(memory,frame,'offset_x',0x80,32)
    frame = _story_move_fields(memory,frame,'offset_y',0x12)
    frame = _story_call_fields(memory,frame,0x3AAC2,0x3CC0E)
    frame = _story_clear_plane_fields(memory,frame)
    frame = _story_script_fields(memory,frame,0x3B654)
    frame = _story_status_fields(memory,frame,0x2500)
    frame = _story_darken_fields(memory,frame,0x3CC50)
    frame = _story_finish_stage_fields(memory,frame,(0x813A,0x813C))
    return memory.sync_status(frame)

def confirm_arrival_second_page_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3CAB4 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3CC82,0x3CCB2)
    frame, pressed = _story_confirm_page_fields(memory,frame,0x45D70,0x3CCDA,0x3B684)
    if not pressed:
        return frame
    frame = _story_palette_masks_fields(memory,frame,(0xFFFF,0xFFFF,0,0xFFFF))
    frame = _story_darken_fields(memory,frame,0x3CD34)
    frame = _story_finish_stage_fields(memory,frame,(0x813A,))
    return memory.sync_status(frame)

def confirm_finale_first_page_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3D184 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3D280,0x3D2A4)
    frame, pressed = _story_confirm_page_fields(memory,frame,0x4696B,0x3D2CC,0x3B6BE)
    if not pressed:
        return frame
    frame = _story_darken_fields(memory,frame,0x3D30E)
    frame = _story_finish_stage_fields(memory,frame,(0x813A,0x813C))
    frame = _story_store_fields(memory,frame,0xFFFF8020,0x1F0)
    frame = _story_store_fields(memory,frame,0xFFFF8026,0x1F0)
    return memory.sync_status(frame)

def confirm_prologue_second_page_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3B7D4 complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3B8D0,0x3B9D6)
    frame, pressed = _story_pressed_fields(memory,frame)
    if not pressed:
        return frame
    frame = _story_status_fields(memory,frame,0x2700)
    frame = _story_decode_picture_fields(memory,frame,0x465C5,0x3B9FE)
    frame = _story_store_fields(memory,frame,0xFFFF8026,0)
    frame = _story_status_fields(memory,frame,0x2500)
    frame = _story_finish_stage_fields(memory,frame)
    frame = _story_status_fields(memory,frame,0x2700)
    frame = _story_clear_plane_fields(memory,frame)
    frame = _story_script_fields(memory,frame,0x3B55A)
    return _story_status_fields(memory,frame,0x2500)

def advance_finale_scroll_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original 3D18C complete story role; BRA prefixes add no slot."""
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x3D41C,0x3D376)
    for low in (0x8020,0x8026):
        frame = _story_add_ram_fields(memory,frame,low)
    for low in (0x8020,0x8026):
        value = _story_read_fields(memory,frame,0xFFFF0000|low) & 0x1FF
        frame = _story_store_fields(memory,frame,0xFFFF0000|low,value)
    frame = _story_compare_ram_fields(memory,frame,0x8026,0x100)
    if not (frame.status & 5):
        return frame
    frame = _story_compare_ram_fields(memory,frame,0x8026,0x70)
    if frame.status & 1:
        return frame
    frame = _story_finish_stage_fields(memory,frame)
    frame = _story_status_fields(memory,frame,0x2700)
    frame = _story_clear_plane_fields(memory,frame)
    frame = _story_script_fields(memory,frame,0x3B6CE)
    return _story_status_fields(memory,frame,0x2500)

def _story_select_sprite_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        directory: Long, attributes: Word | None) -> FirstDeploymentFrame:
    """Read the live template LONG and tail into the sole 3B13C packet algorithm."""
    from .business_objects import _append_object_sprite_fields
    frame = _scene_render_asl_word(memory,frame,'unit',low16(frame.unit),2)
    address = directory + s16(low16(frame.unit))
    frame = first_replace(frame,roster=memory.cursor_at(_story_read_fields(memory,frame,address,4)))
    frame = _story_move_fields(memory,frame,'unit',5)
    frame = _story_move_fields(memory,frame,'count',0,32)
    if attributes is not None:
        frame = _story_move_fields(memory,frame,'distance',attributes)
    return _append_object_sprite_fields(memory,frame)


def select_prologue_sprite_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    return _story_select_sprite_fields(memory,frame,0x3BBD6,0x100)


def select_departure_sprite_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    return _story_select_sprite_fields(memory,frame,0x3C6DC,None)


def select_arrival_sprite_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    return _story_select_sprite_fields(memory,frame,0x3CE1C,0x200)


def select_finale_sprite_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    frame = _story_move_fields(memory,frame,'distance',0x100)
    return select_finale_sprite_with_attributes_fields(memory,frame)


def select_finale_sprite_with_attributes_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """True 3D460 middle entry inherits D4; neither extra call nor marker setup."""
    memory.frame(frame)
    return _story_select_sprite_fields(memory,frame,0x3D470,None)


def draw_prologue_portrait_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    frame = _story_move_fields(memory,frame,'unit',12)
    frame = _story_move_fields(memory,frame,'target_x',0x80)
    frame = _story_move_fields(memory,frame,'target_y',0xC0)
    return _story_call_fields(memory,frame,0x3BBC2,0x3B8E0)


def _story_animation_index_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        counter: Word, shift: Word, maximum: Word, reset_counter: bool,
        hold_last: bool = False) -> FirstDeploymentFrame:
    frame = _story_add_ram_fields(memory,frame,counter)
    frame = _story_ram_move_fields(memory,frame,'unit',counter)
    frame = _scene_mode_lsr_word(memory,frame,'unit',low16(frame.unit),shift)
    frame = _scene_render_compare(memory,frame,low16(frame.unit),maximum,16)
    if not (frame.status & 5):
        if reset_counter:
            frame = _story_clear_fields(memory,frame,counter)
        frame = _story_move_fields(memory,frame,'unit',maximum if hold_last else 0,32)
    return frame


def _story_draw_pose_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        x: Word, y: Word, target: Long, continuation: Long,
        attributes: Word | None = None) -> FirstDeploymentFrame:
    frame = _story_move_fields(memory,frame,'target_x',x)
    frame = _story_move_fields(memory,frame,'target_y',y)
    if attributes is not None:
        frame = _story_move_fields(memory,frame,'distance',attributes)
    return _story_call_fields(memory,frame,target,continuation)


def animate_prologue_portrait_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    frame = _story_animation_index_fields(memory,frame,0x813C,5,2,True)
    frame = _story_arithmetic_fields(memory,frame,'unit',9)
    frame = _story_draw_pose_fields(memory,frame,0x80,0xC0,0x3BBC2,0x3BAD6)
    frame = _story_move_fields(memory,frame,'target_x',0x80)
    frame = _story_move_fields(memory,frame,'target_y',0xC0)
    frame = _story_move_fields(memory,frame,'unit',0,32)
    return _story_call_fields(memory,frame,0x3BBC2,0x3BAE4)


def cycle_prologue_colors_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Three original palette stages; every repeated timer read remains live."""
    memory.frame(frame)
    frame = _story_ram_move_fields(memory,frame,'target_x',0x813E)
    frame = _scene_mode_lsr_word(memory,frame,'target_x',low16(frame.target_x),4)
    frame = _scene_render_compare(memory,frame,low16(frame.target_x),6,16)
    if frame.status & 1:
        frame = _scene_render_asl_word(memory,frame,'target_x',low16(frame.target_x),1)
        value = _story_read_fields(memory,frame,0x3BB04+s16(low16(frame.target_x)))
        frame = _story_store_fields(memory,frame,0xFFFFFB1C,value)
        return _story_add_ram_fields(memory,frame,0x813E)
    frame = _scene_render_compare(memory,frame,low16(frame.target_x),14,16)
    if frame.status & 1:
        frame = _story_arithmetic_fields(memory,frame,'target_x',6,True)
        frame = _story_arithmetic_fields(memory,frame,'target_x',9)
        frame = _story_call_fields(memory,frame,0x3AB94,0x3BB24)
        return _story_add_ram_fields(memory,frame,0x813E)
    frame = _story_compare_ram_fields(memory,frame,0x8026,0x50)
    if not (frame.status & 1):
        return frame
    for low,value in ((0xFB02,0xEEE),(0xFB06,0xEC8),(0xFB1E,0xE86)):
        frame = _story_store_fields(memory,frame,0xFFFF0000|low,value)
    frame = _story_ram_move_fields(memory,frame,'target_x',0xF320)
    frame = _story_mask_fields(memory,frame,'target_x',3)
    if frame.status & 4:
        frame = _story_add_ram_fields(memory,frame,0x8026)
    return frame


def load_departure_tile_rows_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    frame = first_replace(frame,controller=memory.cursor_at(0x3C2A4))
    rows = ((0xE820,0x3C248),(0xE8A0,0x3C250),(0xE920,0x3C258),(0xE9A0,0x3C260),
        (0xEA20,0x3C268),(0xEAA0,0x3C270),(0xEB20,0x3C278),(0xEBA0,0x3C280))
    for address,continuation in rows:
        frame = _story_move_fields(memory,frame,'target_x',address)
        frame = _story_call_fields(memory,frame,0x3C282,continuation)
    return frame


def write_departure_tile_row_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    frame = _scene_render_push_longs(memory,frame,(frame.controller.base,))
    frame = _story_store_fields(memory,frame,0x00C00004,0x8F02)
    frame = _story_call_fields(memory,frame,0x3B2B0,0x3C292)
    stack = frame.stack_cursor
    frame = first_replace(frame,controller=memory.cursor_at(stack.long()),stack_cursor=stack.advance(4))
    frame = _story_move_fields(memory,frame,'target_x',7,32)
    while True:
        value = _story_read_fields(memory,frame,frame.controller.base)
        frame = first_replace(frame,controller=frame.controller.advance(2))
        frame = _story_store_fields(memory,frame,0x00C00000,value)
        remaining = u16(low16(frame.target_x)-1)
        frame = first_replace(frame,target_x=replace_word(frame.target_x,remaining))
        if remaining == 0xFFFF:
            return frame


def _story_rising_layer_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        counter: Word, sampled_counter: Word, shift: Word, baseline: Word,
        tile: Word, attributes: Word, continuation: Long) -> FirstDeploymentFrame:
    frame = _story_add_ram_fields(memory,frame,counter)
    frame = _story_ram_move_fields(memory,frame,'unit',sampled_counter)
    frame = _scene_mode_lsr_word(memory,frame,'unit',low16(frame.unit),shift)
    frame = _story_move_fields(memory,frame,'target_y',baseline)
    frame = _story_arithmetic_fields(memory,frame,'target_y',low16(frame.unit),True)
    frame = _story_move_fields(memory,frame,'target_x',0x80)
    frame = _story_move_fields(memory,frame,'unit',tile)
    frame = _story_move_fields(memory,frame,'distance',attributes)
    return _story_call_fields(memory,frame,0x3C6CC,continuation)


def animate_departure_three_layers_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original layers all sample 813C, including the latter two; do not repair it."""
    memory.frame(frame)
    frame = _story_rising_layer_fields(memory,frame,0x813C,0x813C,6,0xB0,0,0x200,0x3C3C4)
    frame = _story_rising_layer_fields(memory,frame,0x813E,0x813C,5,0xB0,1,0x200,0x3C3E4)
    return _story_rising_layer_fields(memory,frame,0x8140,0x813C,4,0xB0,2,0x200,0x3C404)


def animate_departure_transition_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    frame = _story_animation_index_fields(memory,frame,0x813C,5,5,True)
    frame = _story_arithmetic_fields(memory,frame,'unit',3)
    return _story_draw_pose_fields(memory,frame,0x80,0xC0,0x3C6CC,0x3C4C6,0x100)


def animate_departure_closing_layers_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    frame = _story_ram_move_fields(memory,frame,'unit',0x8144)
    frame = _scene_mode_lsr_word(memory,frame,'unit',low16(frame.unit),3)
    frame = _story_move_fields(memory,frame,'target_y',0xE0)
    frame = _story_arithmetic_fields(memory,frame,'target_y',low16(frame.unit),True)
    frame = _scene_render_compare(memory,frame,low16(frame.target_y),0xC0,16)
    if frame.status & 5:
        frame = _story_move_fields(memory,frame,'target_y',0xC0)
    else:
        frame = _story_add_ram_fields(memory,frame,0x8144)
    frame = _story_move_fields(memory,frame,'target_x',0x80)
    frame = _story_move_fields(memory,frame,'unit',13)
    frame = _story_move_fields(memory,frame,'distance',0x100)
    frame = _story_call_fields(memory,frame,0x3C6CC,0x3C5F2)
    frame = _story_ram_move_fields(memory,frame,'target_y',0x8142)
    frame = _scene_mode_lsr_word(memory,frame,'target_y',low16(frame.target_y),3)
    frame = _story_arithmetic_fields(memory,frame,'target_y',0xA0)
    frame = _scene_render_compare(memory,frame,low16(frame.target_y),0xC0,16)
    if not (frame.status & 1):
        frame = _story_move_fields(memory,frame,'target_y',0xC0)
    else:
        frame = _story_add_ram_fields(memory,frame,0x8142)
    frame = _story_move_fields(memory,frame,'target_x',0x80)
    frame = _story_move_fields(memory,frame,'unit',12)
    frame = _story_move_fields(memory,frame,'distance',0x200)
    frame = _story_call_fields(memory,frame,0x3C6CC,0x3C61C)
    frame = _story_rising_layer_fields(memory,frame,0x813C,0x813C,6,0xC0,9,0x200,0x3C63C)
    frame = _story_rising_layer_fields(memory,frame,0x813E,0x813E,5,0xC0,10,0x200,0x3C65C)
    return _story_rising_layer_fields(memory,frame,0x8140,0x8140,4,0xC0,11,0x200,0x3C67C)


def animate_arrival_portrait_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    frame = _story_animation_index_fields(memory,frame,0x813C,5,3,True)
    return _story_draw_pose_fields(memory,frame,0x80,0xC0,0x3CE08,0x3CBE0)


def animate_arrival_zoom_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    frame = _story_add_ram_fields(memory,frame,0x813C)
    frame = _story_ram_move_fields(memory,frame,'unit',0x813C)
    frame = _scene_mode_lsr_word(memory,frame,'unit',low16(frame.unit),5)
    frame = _story_move_fields(memory,frame,'target_x',0x80)
    frame = _story_move_fields(memory,frame,'target_y',0xC0)
    frame = _story_arithmetic_fields(memory,frame,'target_x',low16(frame.unit),True)
    frame = _story_arithmetic_fields(memory,frame,'target_y',low16(frame.unit),True)
    frame = _story_move_fields(memory,frame,'unit',4,32)
    frame = _story_call_fields(memory,frame,0x3CE08,0x3CC9E)
    frame = _story_move_fields(memory,frame,'target_x',0x80)
    frame = _story_move_fields(memory,frame,'target_y',0xC0)
    frame = _story_move_fields(memory,frame,'unit',8,32)
    return _story_call_fields(memory,frame,0x3CE08,0x3CCAC)


def animate_arrival_closing_portrait_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    frame = _story_animation_index_fields(memory,frame,0x813C,5,2,True)
    frame = _story_arithmetic_fields(memory,frame,'unit',5)
    return _story_draw_pose_fields(memory,frame,0x80,0xC4,0x3CE08,0x3CDBC)


def animate_finale_portrait_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    frame = _story_animation_index_fields(memory,frame,0x813C,5,3,False,True)
    return _story_draw_pose_fields(memory,frame,0x80,0xC0,0x3D45C,0x3D29E)


def move_finale_actor_diagonally_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    frame = _story_compare_ram_fields(memory,frame,0x813C,0xA0)
    if not (frame.status & 5):
        return frame
    frame = _story_add_ram_fields(memory,frame,0x813C,2)
    frame = _story_move_fields(memory,frame,'target_x',0x30)
    frame = _story_move_fields(memory,frame,'target_y',0xE0)
    frame = _story_arithmetic_fields(memory,frame,'target_x',_story_read_fields(memory,frame,0xFFFF813C))
    frame = _story_arithmetic_fields(memory,frame,'target_y',_story_read_fields(memory,frame,0xFFFF813C),True)
    frame = _story_arithmetic_fields(memory,frame,'target_x',_story_read_fields(memory,frame,0xFFFF8020))
    frame = _story_move_fields(memory,frame,'unit',7)
    return _story_call_fields(memory,frame,0x3D45C,0x3D370)


def animate_finale_closing_portrait_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    frame = _story_add_ram_fields(memory,frame,0x813C)
    frame = _story_ram_move_fields(memory,frame,'unit',0x813C)
    frame = _scene_mode_lsr_word(memory,frame,'unit',low16(frame.unit),4)
    frame = _scene_render_compare(memory,frame,low16(frame.unit),1,16)
    if not (frame.status & 5):
        frame = _story_move_fields(memory,frame,'unit',0,32)
        frame = _story_clear_fields(memory,frame,0x813C)
    frame = _story_arithmetic_fields(memory,frame,'unit',5)
    frame = _story_move_fields(memory,frame,'target_x',0xC0)
    frame = _story_move_fields(memory,frame,'target_y',0xC0)
    frame = _story_move_fields(memory,frame,'distance',0x200)
    return _story_call_fields(memory,frame,0x3D460,0x3D444)

def _story_text_dimensions_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        characters: Word, continuation: Long) -> FirstDeploymentFrame:
    frame = _story_move_fields(memory,frame,'target_x',_story_read_fields(memory,frame,0x00FF7014))
    frame = _story_move_fields(memory,frame,'target_y',_story_read_fields(memory,frame,0x00FF7016))
    frame = _story_move_fields(memory,frame,'count',characters)
    return _story_call_fields(memory,frame,0xAE8A,continuation)


def _story_upload_current_rows_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    while True:
        value = _story_read_fields(memory,frame,frame.roster.base,4)
        frame = first_replace(frame,roster=frame.roster.advance(4))
        frame = _story_store_fields(memory,frame,frame.auxiliary.base,value,4)
        counter = u16(low16(frame.target_x)-1)
        frame = first_replace(frame,target_x=replace_word(frame.target_x,counter))
        if counter == 0xFFFF:
            return frame


def _story_text_tile_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        advance: Word) -> FirstDeploymentFrame:
    frame = _story_move_fields(memory,frame,'unit',_story_read_fields(memory,frame,0x00FF700C))
    return _story_arithmetic_fields(memory,frame,'unit',advance)


def _story_decimal_strip_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        role) -> FirstDeploymentFrame:
    """Two/three-digit roles use the existing decimal and glyph algorithms exactly once."""
    if role == 'officer':
        counter,decimal_return,glyph_return,digits = 0x80E4,0x40114,0x40156,3
    elif role == 'pair':
        counter,decimal_return,glyph_return,digits = 0x80E6,0x40194,0x401CA,2
    elif role == 'triple':
        counter,decimal_return,glyph_return,digits = 0x80E8,0x40224,0x40266,3
    else:
        raise ValueError('closed text number role required')
    if role == 'triple':
        frame = _story_store_fields(memory,frame,0x00FF700C,low16(frame.unit))
        frame = _story_store_fields(memory,frame,0x00FF700E,frame.roster.base,4)
    else:
        frame = _story_store_fields(memory,frame,0x00FF700E,frame.roster.base,4)
        frame = _story_store_fields(memory,frame,0x00FF700C,low16(frame.unit))
    frame = _story_move_fields(memory,frame,'target_x',0,32)
    frame = _story_ram_move_fields(memory,frame,'target_x',counter)
    frame = _story_call_fields(memory,frame,0x3B2D8,decimal_return)
    carriers = ('target_x','target_y','unit') if digits == 3 else ('target_x','target_y')
    for name in carriers:
        frame = _story_move_fields(memory,frame,name,0x100)
    for index,name in enumerate(carriers):
        frame = _story_ram_move_fields(memory,frame,name,0x8006-digits+index,8)
    for index,name in enumerate(carriers):
        frame = _story_store_fields(memory,frame,0xFFFF8000+index*2,low16(frame.carrier(name)))
    frame = first_replace(frame,roster=memory.cursor_at(0xFFFF8000),candidates=memory.cursor_at(0xFFFFD300))
    frame = _story_text_dimensions_fields(memory,frame,digits-1,glyph_return)
    frame = first_replace(frame,roster=memory.cursor_at(0xFFFFD300),auxiliary=memory.cursor_at(0x00C00000))
    frame = _story_move_fields(memory,frame,'target_x',digits*32-1)
    if role == 'pair':
        frame = _story_compare_ram_fields(memory,frame,0x8000,0x100)
        if frame.status & 4:
            frame = first_replace(frame,roster=frame.roster.advance(0x80))
            frame = _story_move_fields(memory,frame,'target_x',_story_read_fields(memory,frame,0x00FF700C))
            frame = _story_arithmetic_fields(memory,frame,'target_x',0x80)
            frame = _story_call_fields(memory,frame,0x3B2B0,0x401F2)
            frame = _story_move_fields(memory,frame,'target_x',0x1F)
    elif role == 'triple':
        frame = _story_text_tile_fields(memory,frame,0x180)
        frame = _story_compare_ram_fields(memory,frame,0x8000,0x100)
        if frame.status & 4:
            frame = first_replace(frame,roster=frame.roster.advance(0x80))
            frame = _story_text_tile_fields(memory,frame,0x100)
            frame = _story_move_fields(memory,frame,'target_x',0x3F)
            frame = _story_compare_ram_fields(memory,frame,0x8002,0x100)
            if frame.status & 4:
                frame = first_replace(frame,roster=frame.roster.advance(0x80))
                frame = _story_text_tile_fields(memory,frame,0x80)
                frame = _story_move_fields(memory,frame,'target_x',0x1F)
    frame = _story_upload_current_rows_fields(memory,frame)
    if role != 'triple':
        frame = _story_text_tile_fields(memory,frame,digits*0x80)
    frame = first_replace(frame,roster=memory.cursor_at(_story_read_fields(memory,frame,0x00FF700E,4)))
    if role != 'pair':
        frame = first_replace(frame,roster=frame.roster.advance(2))
    return memory.sync_status(frame)


def append_story_officer_number_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    return _story_decimal_strip_fields(memory,frame,'officer')


def append_story_counter_pair_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    return _story_decimal_strip_fields(memory,frame,'pair')


def append_story_counter_triple_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    return _story_decimal_strip_fields(memory,frame,'triple')


def advance_story_text_stream_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Live text token parsing, name/number rendering and exact stream advancement."""
    memory.frame(frame)
    frame = _story_ram_move_fields(memory,frame,'target_y',0xEFD8)
    frame = _story_ram_move_fields(memory,frame,'target_x',0xF320)
    mask = _story_read_fields(memory,frame,0x3FFA6+s16(low16(frame.target_y)),1)
    frame = _story_mask_fields(memory,frame,'target_x',mask,8)
    if not (frame.status & 4):
        return frame
    value = _story_read_fields(memory,frame,0x00FF700C)
    frame = _scene_refresh_flags(memory,frame,value,2)
    if frame.status & 4:
        return frame
    frame = _story_move_fields(memory,frame,'target_x',_story_read_fields(memory,frame,0x00FF700C))
    frame = _story_call_fields(memory,frame,0x3B2B0,0x3FFCE)
    frame = first_replace(frame,roster=memory.cursor_at(_story_read_fields(memory,frame,0x00FF700E,4)))
    frame = _story_move_fields(memory,frame,'target_x',_story_read_fields(memory,frame,frame.roster.base))
    frame = _story_mask_fields(memory,frame,'target_x',0xBFFF)
    special = False
    for token,selected,alternate in ((0x8008,0x80E0,0x80E2),(0x800E,0x80DC,0x80DE),
            (0x800A,0x80E2,0x80E0),(0xFF03,0x80DE,0x80DC)):
        frame = _story_ram_move_fields(memory,frame,'choice',selected)
        frame = _story_ram_move_fields(memory,frame,'offset_y',alternate)
        frame = _scene_render_compare(memory,frame,low16(frame.target_x),token,16)
        if frame.status & 4:
            special = True
            break
    scan_following = True
    if special:
        value = _story_read_fields(memory,frame,0xFFFF8116)
        frame = _scene_refresh_flags(memory,frame,value,2)
        if not (frame.status & 4):
            frame = _story_move_fields(memory,frame,'choice',low16(frame.offset_y))
        frame = _story_move_fields(memory,frame,'target_x',_story_read_fields(memory,frame,0x00FF7014))
        frame = _story_move_fields(memory,frame,'target_y',_story_read_fields(memory,frame,0x00FF7016))
        frame = _story_call_fields(memory,frame,0x402C2,0x4002C)
        frame = _story_text_tile_fields(memory,frame,0x180)
    else:
        frame = _story_move_fields(memory,frame,'unit',_story_read_fields(memory,frame,0x00FF700C))
        frame = _scene_render_bit(memory,frame,frame.target_x,0x8000)
        if not (frame.status & 4):
            # 40042 BNE goes directly to 4008C token comparisons. It does not
            # consume another WORD or finalize this control token early.
            scan_following = False
        else:
            frame = first_replace(frame,candidates=memory.cursor_at(0xFFFFD300))
            frame = _story_text_dimensions_fields(memory,frame,0,0x40060)
            frame = first_replace(frame,roster=memory.cursor_at(0xFFFFD300))
            frame = _story_glyph_upload_fields(memory,frame,0x1F)
            frame = _story_text_tile_fields(memory,frame,0x80)
    if scan_following:
        frame = first_replace(frame,roster=memory.cursor_at(_story_read_fields(memory,frame,0x00FF700E,4)).advance(2))
        frame = _story_move_fields(memory,frame,'target_x',_story_read_fields(memory,frame,frame.roster.base))
    if not scan_following or frame.status & 8:
        frame = _scene_render_compare(memory,frame,low16(frame.target_x),0xFF20,16)
        if frame.status & 4:
            frame = _story_arithmetic_fields(memory,frame,'unit',0x40)
            frame = first_replace(frame,roster=frame.roster.advance(2))
        else:
            frame = _scene_render_compare(memory,frame,low16(frame.target_x),0x8002,16)
            if frame.status & 4:
                frame = first_replace(frame,roster=frame.roster.advance(2))
                frame = _story_move_fields(memory,frame,'target_x',low16(frame.unit))
                frame = _story_move_fields(memory,frame,'unit',0xA900)
                frame = _scene_render_compare(memory,frame,low16(frame.target_x),0xA900,16)
                if not (frame.status & 1):
                    frame = _story_move_fields(memory,frame,'unit',0xB200)
            else:
                frame = _scene_render_compare(memory,frame,low16(frame.target_x),0x8010,16)
                if frame.status & 4:
                    frame = _story_call_fields(memory,frame,0x400FE,0x400C4)
                else:
                    frame = _scene_render_compare(memory,frame,low16(frame.target_x),0x8011,16)
                    if frame.status & 4:
                        frame = first_replace(frame,roster=frame.roster.advance(2))
                        frame = _story_call_fields(memory,frame,0x4017E,0x400D4)
                    else:
                        frame = _scene_render_compare(memory,frame,low16(frame.target_x),0x8012,16)
                        if frame.status & 4:
                            frame = first_replace(frame,roster=frame.roster.advance(2))
                            frame = _story_call_fields(memory,frame,0x4020E,0x400E4)
                        else:
                            frame = _scene_render_compare(memory,frame,low16(frame.target_x),0x8000,16)
                            if frame.status & 4:
                                frame = _story_move_fields(memory,frame,'unit',0)
    return _story_finish_text_stream_fields(memory,frame)


def _story_finish_text_stream_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _story_store_fields(memory,frame,0x00FF700C,low16(frame.unit))
    return _story_store_fields(memory,frame,0x00FF700E,frame.roster.base,4)

def _story_dma_setup_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        words: tuple, latch: Word, retain_port: bool) -> FirstDeploymentFrame:
    """Actual Z80 bus request/release and VDP DMA commands, never fabricated ACK."""
    if retain_port:
        frame = first_replace(frame,auxiliary=memory.cursor_at(0x00C00004))
    frame = _story_ram_move_fields(memory,frame,'choice',0xF606)
    frame = _story_move_fields(memory,frame,'choice',low8(frame.choice)|16,8)
    frame = _story_store_fields(memory,frame,frame.auxiliary.base,low16(frame.choice))
    frame = _story_store_fields(memory,frame,0x00A11100,0x100)
    frame = _story_store_fields(memory,frame,frame.auxiliary.base,words[0],4)
    frame = _story_store_fields(memory,frame,frame.auxiliary.base,words[1],4)
    frame = _story_store_fields(memory,frame,frame.auxiliary.base,0x977F)
    frame = _story_store_fields(memory,frame,frame.auxiliary.base,words[2])
    frame = _story_store_fields(memory,frame,0xFFFFF620,latch)
    frame = _story_store_fields(memory,frame,frame.auxiliary.base,_story_read_fields(memory,frame,0xFFFFF620))
    value = _story_read_fields(memory,frame,0xFFFF3F00,1)
    frame = _scene_refresh_flags(memory,frame,value,1)
    if frame.status & 4:
        frame = _story_store_fields(memory,frame,0x00A11100,0)
    return frame


def _story_dma_finish_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _story_ram_move_fields(memory,frame,'target_x',0xF606)
    frame = _story_move_fields(memory,frame,'target_x',low8(frame.target_x)|64,8)
    return _story_store_fields(memory,frame,0x00C00004,low16(frame.target_x))


def transfer_story_plane_dma_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x67CA,0x3A53C)
    frame = _story_call_fields(memory,frame,0x4942,0x3A542)
    frame = _story_dma_setup_fields(memory,frame,(0x94009340,0x96FD9580,0xC000),0x80,True)
    frame = _story_store_fields(memory,frame,frame.auxiliary.base,_story_read_fields(memory,frame,0xFFFFF606))
    frame = _story_clear_fields(memory,frame,0xF612)
    return _story_dma_finish_fields(memory,frame)


def transfer_story_overlay_dma_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    memory.frame(frame)
    frame = _story_call_fields(memory,frame,0x67CA,0x3A8A2)
    frame = _story_dma_setup_fields(memory,frame,(0x94019340,0x96FC9500,0x5000),0x83,True)
    frame = _story_store_fields(memory,frame,frame.auxiliary.base,_story_read_fields(memory,frame,0xFFFFF606))
    frame = _story_store_fields(memory,frame,0x00C00004,0x40000010,4)
    frame = _story_store_fields(memory,frame,0x00C00000,_story_read_fields(memory,frame,0xFFFF8024,4),4)
    frame = _story_store_fields(memory,frame,0x00C00004,0x54000003,4)
    frame = _story_store_fields(memory,frame,0x00C00000,_story_read_fields(memory,frame,0xFFFF8028,4),4)
    frame = _story_move_fields(memory,frame,'target_x',0x60)
    while True:
        remaining = u16(low16(frame.target_x)-1)
        frame = first_replace(frame,target_x=replace_word(frame.target_x,remaining))
        if remaining == 0xFFFF:
            break
    frame = _story_dma_setup_fields(memory,frame,(0x94009340,0x96FD9580,0xC000),0x80,True)
    frame = _story_store_fields(memory,frame,frame.auxiliary.base,_story_read_fields(memory,frame,0xFFFFF606))
    frame = _story_dma_finish_fields(memory,frame)
    return _story_call_fields(memory,frame,0x3FFAA,0x3A974)

def _story_dispatch_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        table: Long) -> FirstDeploymentFrame:
    """Original live stage WORD selects actual four-byte BRA CODE, not a fake callback."""
    memory.frame(frame)
    frame = _story_ram_move_fields(memory,frame,'target_x',0x80EA)
    frame = _scene_render_asl_word(memory,frame,'target_x',low16(frame.target_x),2)
    return _story_known_fields(memory,frame,table+s16(low16(frame.target_x)))


def dispatch_prologue_story_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _story_dispatch_fields(memory,frame,0x3B7BC)


def dispatch_departure_story_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _story_dispatch_fields(memory,frame,0x3C19C)


def dispatch_arrival_story_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _story_dispatch_fields(memory,frame,0x3CAA4)


def dispatch_finale_story_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _story_dispatch_fields(memory,frame,0x3D17C)


def dispatch_interlude_story_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _story_dispatch_fields(memory,frame,0x3C97A)


def _story_known_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long) -> FirstDeploymentFrame:
    """Genuine complete story children, including402C2 live officer-name rendering. The real caller already owns the LONG; same-state full frame and all actual DATA/device boundaries survive."""
    memory.frame(frame)
    if target == 26570:
        from ..high_level_main_flows.business_lowbank import poll_controller_with_z80_bus_fields
        return poll_controller_with_z80_bus_fields(memory.state, frame)
    if target == 18754:
        from ..high_level_remaining_flows.business_lowbank import lowbank_process_device_control_9_fields
        return lowbank_process_device_control_9_fields(memory.state, frame)
    if target == 518:
        from ..high_level_main_flows.business_boot import reset_console_frame_fields
        return reset_console_frame_fields(memory.state, frame)
    if target == 238902:
        return transfer_story_plane_dma_fields(memory, frame)
    elif target == 239772:
        return transfer_story_overlay_dma_fields(memory, frame)
    elif target == 243614:
        return dispatch_prologue_story_fields(memory, frame)
    elif target == 243618:
        return dispatch_departure_story_fields(memory, frame)
    elif target == 243622:
        return dispatch_arrival_story_fields(memory, frame)
    elif target == 243626:
        return dispatch_finale_story_fields(memory, frame)
    elif target == 243630:
        return dispatch_interlude_story_fields(memory, frame)
    elif target == 243644:
        return initialize_prologue_story_fields(memory, frame)
    elif target == 243648:
        return reveal_prologue_caption_fields(memory, frame)
    elif target == 243652:
        return wait_prologue_portrait_fields(memory, frame)
    elif target == 243656:
        return confirm_prologue_first_page_fields(memory, frame)
    elif target == 243660:
        return wait_prologue_second_page_fields(memory, frame)
    elif target == 243664:
        return reveal_prologue_second_portrait_fields(memory, frame)
    elif target == 243668:
        return confirm_prologue_second_page_fields(memory, frame)
    elif target == 243672:
        return begin_prologue_closing_caption_fields(memory, frame)
    elif target == 243676:
        return finish_prologue_closing_caption_fields(memory, frame)
    elif target == 243680:
        return confirm_prologue_exit_fields(memory, frame)
    elif target == 243920:
        return draw_prologue_portrait_fields(memory, frame)
    elif target == 244400:
        return animate_prologue_portrait_fields(memory, frame)
    elif target == 244454:
        return cycle_prologue_colors_fields(memory, frame)
    elif target == 244674:
        return select_prologue_sprite_fields(memory, frame)
    elif target == 246172:
        return initialize_departure_story_fields(memory, frame)
    elif target == 246176:
        return reveal_departure_caption_fields(memory, frame)
    elif target == 246180:
        return confirm_departure_first_page_fields(memory, frame)
    elif target == 246184:
        return wait_departure_second_page_fields(memory, frame)
    elif target == 246188:
        return confirm_departure_second_page_fields(memory, frame)
    elif target == 246192:
        return begin_departure_closing_caption_fields(memory, frame)
    elif target == 246196:
        return finish_departure_closing_caption_fields(memory, frame)
    elif target == 246200:
        return confirm_departure_exit_fields(memory, frame)
    elif target == 246330:
        return load_departure_tile_rows_fields(memory, frame)
    elif target == 246402:
        return write_departure_tile_row_fields(memory, frame)
    elif target == 246692:
        return animate_departure_three_layers_fields(memory, frame)
    elif target == 246942:
        return animate_departure_transition_fields(memory, frame)
    elif target == 247238:
        return animate_departure_closing_layers_fields(memory, frame)
    elif target == 247500:
        return select_departure_sprite_fields(memory, frame)
    elif target == 248186:
        return initialize_interlude_story_fields(memory, frame)
    elif target == 248190:
        return reveal_interlude_caption_fields(memory, frame)
    elif target == 248194:
        return confirm_interlude_exit_fields(memory, frame)
    elif target == 248484:
        return initialize_arrival_story_fields(memory, frame)
    elif target == 248488:
        return reveal_arrival_caption_fields(memory, frame)
    elif target == 248492:
        return confirm_arrival_first_page_fields(memory, frame)
    elif target == 248496:
        return wait_arrival_second_page_fields(memory, frame)
    elif target == 248500:
        return confirm_arrival_second_page_fields(memory, frame)
    elif target == 248504:
        return begin_arrival_closing_caption_fields(memory, frame)
    elif target == 248508:
        return finish_arrival_closing_caption_fields(memory, frame)
    elif target == 248512:
        return confirm_arrival_exit_fields(memory, frame)
    elif target == 248766:
        return animate_arrival_portrait_fields(memory, frame)
    elif target == 248962:
        return animate_arrival_zoom_fields(memory, frame)
    elif target == 249240:
        return animate_arrival_closing_portrait_fields(memory, frame)
    elif target == 249352:
        return select_arrival_sprite_fields(memory, frame)
    elif target == 250236:
        return initialize_finale_story_fields(memory, frame)
    elif target == 250240:
        return reveal_finale_caption_fields(memory, frame)
    elif target == 250244:
        return confirm_finale_first_page_fields(memory, frame)
    elif target == 250248:
        return wait_finale_scroll_fields(memory, frame)
    elif target == 250252:
        return advance_finale_scroll_fields(memory, frame)
    elif target == 250256:
        return finish_finale_closing_caption_fields(memory, frame)
    elif target == 250260:
        return confirm_finale_exit_fields(memory, frame)
    elif target == 250496:
        return animate_finale_portrait_fields(memory, frame)
    elif target == 250694:
        return move_finale_actor_diagonally_fields(memory, frame)
    elif target == 250908:
        return animate_finale_closing_portrait_fields(memory, frame)
    elif target == 250972:
        return select_finale_sprite_fields(memory, frame)
    elif target == 250976:
        return select_finale_sprite_with_attributes_fields(memory, frame)
    elif target == 262058:
        return advance_story_text_stream_fields(memory, frame)
    elif target == 262398:
        return append_story_officer_number_fields(memory, frame)
    elif target == 262526:
        return append_story_counter_pair_fields(memory, frame)
    elif target == 262670:
        return append_story_counter_triple_fields(memory, frame)
    elif target == 240160:
        return begin_scene_palette_darken_fields(memory, frame)
    elif target == 240184:
        from ..high_level_dynamic_flows.business_early_phase import begin_scene_palette_lighten_fields
        return begin_scene_palette_lighten_fields(memory, frame)
    elif target == 240334:
        return read_vdp_plane_rle_rows_fields(memory, frame)
    elif target == 242352:
        return set_vram_write_address_fields(memory, frame)
    elif target == 240532:
        return copy_scene_palette_variant_fields(memory, frame)
    elif target == 44682:
        return decode_glyph_rows_to_buffers_fields(memory, frame)
    elif target == 242392:
        from ..high_level_dynamic_flows.business_early_phase import encode_six_decimal_digits_fields
        return encode_six_decimal_digits_fields(memory, frame)
    if target == 262850:
        from ..high_level_dynamic_flows.business_actions import upload_object_officer_name_frame_fields
        return upload_object_officer_name_frame_fields(memory.state, frame)
    if target == 0x3AAC2:
        from ..high_level_main_flows.business_scene_support import decode_high_plane_rows_fields
        return decode_high_plane_rows_fields(memory.state, frame)
    raise SceneRefreshBoundary(target, frame, None)
