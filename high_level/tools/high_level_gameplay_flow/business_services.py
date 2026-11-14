"""Video, sound-command, glyph and message logic connecting gameplay scenes.

Hardware access remains ordered and externally supplied; no host screenshot or
successful stub substitutes for a real display, interrupt or audio operation.
Readonly transfer tables and glyph data are inputs, never source-embedded art.
"""
from .domain import (
    GameplayState, Table, Cursor, Byte, Word, Long, Boundary, checked_state,
    checked_cursor, uint, u8, u16, u32, s16, low8, low16, replace_word,
    negative_word, descending_inclusive, swap_words,
)
from .contexts_services import (
    GlyphColors, GlyphStreamResult, TransferResult, SceneDisplayContext, SceneDisplayResult,
    SpriteControlContext, SpriteControlResult, MarkerResetMemory,
)


from .contexts_services import SceneRefreshMemory, SceneRefreshBoundary, SceneSoundSelectionFields, FirstDeploymentFrame, first_replace, _first_word, _first_byte, _first_long, _first_shift_word, _first_compare_word

def _control(state, size, value):
    state.write(0xC00004, size, value)


def _pixels(state, size, value):
    state.write(0xC00000, size, value)


def _wait_dma(state):
    while state.read(0xC00004, 2) & 2:
        state.progress('vdp-dma')


def _release_sound_bus_if_allowed(state):
    if state.read(0xFF3F00, 1) == 0:
        state.write(0xA11100, 2, 0)


def clear_scene_video_and_state(state: GameplayState) -> None:
    """Clear the active scene planes and its original scratch-state ranges."""
    checked_state(state)
    state.set_status_word(0x2700)
    pattern = select_scene_fill_pattern(state)
    state.write(0xFFFFF37E, 2, 0)
    _control(state, 4, 0x60A00002)
    for _ in descending_inclusive(0x59F):
        _pixels(state, 4, pattern)
    if state.read(0xFFFFF6C4, 2) == 0:
        _control(state, 4, 0x70000001)
        source = state.table(0x89DDC).cursor()
        for _ in descending_inclusive(0x17):
            _pixels(state, 4, source.next_long())
        source = state.table(0x8A07C).cursor()
        for _ in descending_inclusive(0xF):
            _pixels(state, 4, source.next_long())
    pattern = select_scene_fill_pattern(state)
    destination = state.table(0xFFFFF516).cursor()
    for _ in descending_inclusive(0x17):
        destination.append_long(pattern)
    state.write(0xFFFFF37A, 2, 0)
    state.write(0xFFFFF37C, 2, 0)
    refresh_gameplay_scene(state)


def select_scene_fill_pattern(state: GameplayState) -> Long:
    checked_state(state)
    index = u16(state.read(0xFFFFF6C4, 2) << 2)
    return state.table(0x696).long(index)


def reset_scene_input_markers(state: GameplayState) -> None:
    checked_state(state)
    _reset_scene_input_marker_fields(MarkerResetMemory(state))


def _reset_scene_input_marker_fields(memory: MarkerResetMemory) -> None:
    """4A16: preserve each original memory CLR's read-before-write cycle."""
    if type(memory) is not MarkerResetMemory:
        raise ValueError('sealed live marker memory required')
    memory.validate()
    for address in (0xFFFFF300, 0xFFFFF800, 0xFFFFF802, 0xFFFFF806):
        memory.state.read(address, 2)
        memory.write_word(address, 0)


def initialize_video_registers_and_planes(state: GameplayState) -> None:
    """Historical no-return video API projects the unique live field algorithm."""
    checked_state(state)
    initialize_video_registers_and_planes_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def clear_video_sprite_plane(state: GameplayState) -> None:
    """Historical no-return clear API projects the unique live field algorithm."""
    checked_state(state)
    clear_video_sprite_plane_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def enqueue_sound_command(state: GameplayState, command: Byte) -> None:
    """Legacy BYTE projection of the sole live two-mailbox algorithm."""
    checked_state(state)
    enqueue_sound_command_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved(),command)


def copy_video_transfer_descriptor(state: GameplayState, index: Word) -> TransferResult:
    """Historical index/source/destination observations project sole 8112."""
    checked_state(state)
    uint(index,16)
    frame = copy_video_transfer_descriptor_fields(SceneRefreshMemory(state),
        FirstDeploymentFrame.unobserved(),index)
    return TransferResult(frame.controller,frame.scan)


def wait_for_scene_sound_byte(state: GameplayState) -> None:
    checked_state(state)
    wait_for_scene_sound_byte_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def expand_glyph_row(state: GameplayState, source: Cursor, background: Byte, foreground: Byte) -> Long:
    """Historical BYTE-color API projects the sole shared Scene AF04 core."""
    from ..high_level_scene_flows.business_scene import expand_glyph_row_fields
    checked_state(state)
    checked_cursor(source,state)
    uint(background,8)
    uint(foreground,8)
    entered = first_replace(FirstDeploymentFrame.unobserved(),target_x=background,target_y=foreground,controller=source.advance(0))
    actual = expand_glyph_row_fields(SceneRefreshMemory(state),entered)
    source.base = actual.controller.base
    return actual.choice


def expand_glyph_stream(state: GameplayState, tokens: Cursor, destination: Cursor,
        colors: GlyphColors, remaining: Long) -> GlyphStreamResult:
    """Historical token/destination observations project the sole shared AF1E core."""
    from ..high_level_scene_flows.business_scene import expand_glyph_stream_fields
    checked_state(state)
    checked_cursor(tokens,state)
    checked_cursor(destination,state)
    if type(colors) is not GlyphColors:
        raise ValueError('explicit glyph colors required')
    colors.__post_init__()
    uint(remaining,32)
    entered = first_replace(FirstDeploymentFrame.unobserved(),roster=tokens.advance(0),
        candidates=destination.advance(0),target_x=colors.background,target_y=colors.foreground,count=remaining)
    actual = expand_glyph_stream_fields(SceneRefreshMemory(state),entered)
    tokens.base,destination.base = actual.roster.base,actual.candidates.base
    return GlyphStreamResult(tokens,destination,actual.count)


def refresh_gameplay_scene(state: GameplayState, retained: Long = 0) -> Long:
    checked_state(state)
    uint(retained,32)
    frame = first_replace(FirstDeploymentFrame.unobserved(),target_x=retained)
    return refresh_gameplay_scene_fields(SceneRefreshMemory(state),frame).target_x


def load_gameplay_scene(state: GameplayState) -> None:
    """Historical unobserved-SP projection, never a complete Scene return."""
    checked_state(state)
    load_gameplay_scene_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def select_sound_command_from_scene(state: GameplayState) -> Word:
    checked_state(state)
    return select_sound_command_from_scene_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved()).command


def resume_pending_sound(state: GameplayState, retained: Long = 0) -> Long:
    checked_state(state)
    uint(retained,32)
    frame = first_replace(FirstDeploymentFrame.unobserved(),target_x=retained)
    return resume_pending_sound_fields(SceneRefreshMemory(state),frame).target_x


def draw_overlay_frame(state: GameplayState) -> None:
    checked_state(state)
    draw_overlay_frame_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def draw_overlay_frame_header(state: GameplayState, command: Long) -> Long:
    checked_state(state)
    uint(command,32)
    frame = first_replace(FirstDeploymentFrame.unobserved(),target_x=command)
    return draw_overlay_frame_header_fields(SceneRefreshMemory(state),frame).target_x


def draw_overlay_frame_middle(state: GameplayState, command: Long) -> Long:
    checked_state(state)
    uint(command,32)
    frame = first_replace(FirstDeploymentFrame.unobserved(),target_x=command)
    return draw_overlay_frame_middle_fields(SceneRefreshMemory(state),frame).target_x


def draw_overlay_frame_footer(state: GameplayState, command: Long) -> Long:
    checked_state(state)
    uint(command,32)
    frame = first_replace(FirstDeploymentFrame.unobserved(),target_x=command)
    return draw_overlay_frame_footer_fields(SceneRefreshMemory(state),frame).target_x


def clear_overlay_frame(state: GameplayState) -> Long:
    checked_state(state)
    return clear_overlay_frame_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved()).target_x


def stage_sprite_word_packet(state: GameplayState, source: Cursor,
                             command: Long, rows: Word, row_command: Word) -> Long:
    """Historical scalar API projects the sole current core; no fake row high words or SP."""
    checked_state(state)
    checked_cursor(source, state)
    uint(command, 32)
    uint(rows, 16)
    uint(row_command, 16)
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=source, target_x=command)
    return stage_sprite_word_packet_fields(SceneRefreshMemory(state), frame).target_x


def present_gameplay_message(state: GameplayState) -> None:
    """Historical API only projects the one30A74 field/wait algorithm."""
    checked_state(state)
    present_gameplay_message_fields(SceneRefreshMemory(state), FirstDeploymentFrame.unobserved())

def _scene_refresh_frame(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    if type(memory) is not SceneRefreshMemory:
        raise ValueError('sealed same-state scene refresh memory required')
    return memory.frame(frame)

def _scene_refresh_flags(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, value, size) -> FirstDeploymentFrame:
    """MOVE/CLR/TST memory outcomes preserve only the actual observed X."""
    if size not in (1,2,4):
        raise ValueError('original scene DATA width required')
    uint(value,size * 8)
    sign = 1 << (size * 8 - 1)
    status = None if frame.status is None else ((frame.status & 16) | (8 if value & sign else 0) | (4 if value == 0 else 0))
    return memory.sync_status(first_replace(frame,status=status))

def _scene_refresh_emit(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, address, size, value) -> FirstDeploymentFrame:
    memory.sync_status(frame)
    memory.state.write(address,size,value)
    return _scene_refresh_flags(memory,frame,value,size)

def _scene_refresh_bit_clear(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, address, bit) -> FirstDeploymentFrame:
    """BCLR is one genuine BYTE RMW and updates Z only."""
    memory.sync_status(frame)
    previous = memory.state.read(address,1)
    memory.state.write(address,1,previous & (255 ^ (1 << bit)))
    status = None if frame.status is None else ((frame.status & 27) | (0 if previous & (1 << bit) else 4))
    return memory.sync_status(first_replace(frame,status=status))

def _scene_refresh_decrement(frame: FirstDeploymentFrame, name, counter: Word) -> FirstDeploymentFrame:
    """DBRA uses the observed local WORD and never changes CCR."""
    uint(counter,16)
    retained = frame.carrier(name)
    return first_replace(frame,**{name:None if retained is None else replace_word(retained,u16(counter - 1))})

def _scene_refresh_repeat_pixels(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, counter: Word, value: Long) -> FirstDeploymentFrame:
    frame = _first_word(frame,name,counter)
    while True:
        frame = _scene_refresh_emit(memory,frame,0xC00000,4,value)
        frame = _scene_refresh_decrement(frame,name,counter)
        counter = u16(counter - 1)
        if counter == 65535:
            return frame

def _scene_refresh_advance_command(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original ADDI.L #800000, with LONG overflow/carry and real X."""
    left = frame.target_x
    if left is None:
        raise SceneRefreshBoundary(0x1090A,frame,None)
    value = u32(left + 0x800000)
    overflow = bool(~(left ^ 0x800000) & (left ^ value) & 0x80000000)
    status = (17 if left + 0x800000 > 0xFFFFFFFF else 0) | (2 if overflow else 0) | (8 if value & 0x80000000 else 0) | (4 if value == 0 else 0)
    return memory.sync_status(first_replace(frame,target_x=value,status=status))

def _scene_refresh_call_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long, command: Byte | None = None) -> FirstDeploymentFrame:
    """Closed actual refresh children; caller owns each genuine JSR/RTS LONG."""
    _scene_refresh_frame(memory,frame)
    if (target,continuation) not in (
        (0x68A,0x614),(0x68A,0x66C),(0xAF48,0x688),
        (0x4A16,0x10744),(0xAF48,0x10750),(0x83C8,0x10756),
        (0x10814,0x1075E),(0x10896,0x1077E),(0x3969A,0x10784),
        (0x109D8,0x1078C),(0x10880,0x107E8),(0x177BE,0x107F8),
        (0x808A,0x1082E),(0x808A,0x10894),
        (0x108E2,0x108D0),(0x1093E,0x108D8),(0x10972,0x108E0)):
        raise ValueError('actual closed scene refresh child and token required')
    if command is not None and target != 0x808A:
        raise ValueError('only sound mailbox has an observed BYTE argument')
    entered = memory.sync_status(frame)
    if frame.stack_cursor is not None:
        stack = frame.stack_cursor.advance(-4)
        stack.set_long(0,continuation)
        entered = first_replace(frame,stack_cursor=stack)
    if target == 0x68A:
        result = select_scene_fill_pattern_fields(memory, entered)
    elif target == 0x4A16:
        _reset_scene_input_marker_fields(MarkerResetMemory(memory.state))
        result = _scene_refresh_flags(memory,entered,0,2)
    elif target == 0xAF48:
        result = refresh_gameplay_scene_fields(memory,entered)
    elif target == 0x83C8:
        result = wait_for_scene_sound_byte_fields(memory,entered)
    elif target == 0x10814:
        result = select_sound_command_from_scene_fields(memory,entered).frame
    elif target == 0x10896:
        result = draw_overlay_frame_fields(memory,entered)
    elif target == 0x109D8:
        result = clear_overlay_frame_fields(memory,entered)
    elif target == 0x10880:
        result = resume_pending_sound_fields(memory,entered)
    elif target == 0x808A:
        result = enqueue_sound_command_fields(memory,entered,command)
    elif target == 0x108E2:
        result = draw_overlay_frame_header_fields(memory,entered)
    elif target == 0x1093E:
        result = draw_overlay_frame_middle_fields(memory,entered)
    elif target == 0x10972:
        result = draw_overlay_frame_footer_fields(memory,entered)
    elif target == 0x3969A and entered.stack_cursor is not None:
        from ..high_level_scene_flows.business_scene import play_scripted_scene_fields
        result = play_scripted_scene_fields(memory.state, entered)
    elif target == 0x3969A and entered.stack_cursor is None:
        observed = memory.state.service_at(target,SceneDisplayContext())
        if type(observed) is not SceneDisplayResult:
            raise Boundary('legacy renderer requires its real retained output observations')
        observed.__post_init__()
        result = first_replace(entered,target_y=observed.foreground,unit=observed.glyph_count,count=observed.training_carrier,status=None)
    elif target == 0x177BE:
        from .business_battle import upload_battle_scene_labels_fields
        result = upload_battle_scene_labels_fields(memory,entered)
    else:
        result = memory.state.service_at(target,entered)
        if type(result) is not FirstDeploymentFrame:
            raise SceneRefreshBoundary(target,entered,continuation)
    _scene_refresh_frame(memory,result)
    if frame.stack_cursor is not None:
        if result.stack_cursor is None:
            raise SceneRefreshBoundary(target,result,continuation)
        memory.sync_status(result)
        actual = result.stack_cursor.long()
        if actual != continuation:
            raise SceneRefreshBoundary(target,result,continuation)
        result = first_replace(result,stack_cursor=result.stack_cursor.advance(4))
    return memory.sync_status(result)

def enqueue_sound_command_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, command: Byte | None = None) -> FirstDeploymentFrame:
    """808A: original hardware bus arbitration and two conditional mailboxes."""
    _scene_refresh_frame(memory,frame)
    if command is None:
        if frame.target_x is None:
            raise SceneRefreshBoundary(0x808A,frame,None)
        command = low8(frame.target_x)
    uint(command,8)
    memory.sync_status(frame)
    memory.state.read(0xFF3F00,1)
    memory.state.write(0xFF3F00,1,255)
    frame = _scene_refresh_emit(memory,frame,0xA11100,2,0x100)
    while True:
        value = memory.state.read(0xA11100,1)
        status = None if frame.status is None else ((frame.status & 27) | (0 if value & 1 else 4))
        frame = memory.sync_status(first_replace(frame,status=status))
        if not value & 1:
            break
        memory.state.progress('sound-bus-acquire')
    value = memory.state.read(0xA01C0A,1)
    frame = _scene_refresh_flags(memory,frame,value,1)
    if value == 0:
        frame = _scene_refresh_emit(memory,frame,0xA01C0A,1,command)
    else:
        value = memory.state.read(0xA01C0B,1)
        frame = _scene_refresh_flags(memory,frame,value,1)
        if value == 0:
            frame = _scene_refresh_emit(memory,frame,0xA01C0B,1,command)
    memory.state.read(0xFF3F00,1)
    memory.state.write(0xFF3F00,1,0)
    return _scene_refresh_emit(memory,frame,0xA11100,2,0)

def wait_for_scene_sound_byte_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """83C8: true SR2500, live BYTE poll, no simulated sound/IRQ completion."""
    _scene_refresh_frame(memory,frame)
    frame = memory.status_word(frame,0x2500)
    while True:
        value = memory.state.read(0xFFFFF612,1)
        frame = _scene_refresh_flags(memory,frame,value,1)
        if value == 0:
            return frame
        memory.state.progress('scene-sound-byte')

def refresh_gameplay_scene_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """AF48: two real VDP bit3 edges, retained D0 high WORD, BTST-only Z."""
    _scene_refresh_frame(memory,frame)
    for edge in ('vblank-end','vblank-start'):
        while True:
            memory.sync_status(frame)
            value = memory.state.read(0xC00004,2)
            frame = _first_word(frame,'target_x',value)
            status = None if frame.status is None else ((frame.status & 27) | (0 if value & 8 else 4))
            frame = memory.sync_status(first_replace(frame,status=status))
            if (edge == 'vblank-end' and not value & 8) or (edge == 'vblank-start' and value & 8):
                break
            memory.state.progress(edge)
    return frame

def select_sound_command_from_scene_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> SceneSoundSelectionFields:
    _scene_refresh_frame(memory,frame)
    value = memory.state.read(0xFF7026,2)
    frame = _first_word(frame,'target_x',value)
    frame = _first_shift_word(frame,'target_x',value,1)
    memory.sync_status(frame)
    command = memory.cursor_at(0x10830,u16(value << 1)).word()
    frame = _first_word(frame,'target_x',command)
    frame = _scene_refresh_emit(memory,frame,0xFFFFEFD0,2,command)
    if not negative_word(command):
        frame = _scene_refresh_call_fields(memory,frame,0x808A,0x1082E,low8(command))
    return SceneSoundSelectionFields(frame,command)

def resume_pending_sound_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    _scene_refresh_frame(memory,frame)
    value = memory.state.read(0xFFFFEFD0,2)
    frame = _scene_refresh_flags(memory,frame,value,2)
    if not negative_word(value):
        frame = _first_word(frame,'target_x',0)
        memory.sync_status(frame)
        command = memory.state.read(0xFFFFF764,1)
        frame = _first_byte(frame,'target_x',command)
        frame = _scene_refresh_call_fields(memory,frame,0x808A,0x10894,command)
    return memory.sync_status(frame)

def draw_overlay_frame_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """10896: fill, external tile stream, physical header/row/footer calls."""
    _scene_refresh_frame(memory,frame)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,0x72000001)
    frame = _scene_refresh_repeat_pixels(memory,frame,'target_x',7,0x33333333)
    frame = first_replace(frame,roster=memory.cursor_at(0x8A0BC))
    frame = _first_word(frame,'target_x',63)
    counter = 63
    while True:
        memory.sync_status(frame)
        source = frame.roster
        value = source.long()
        frame = first_replace(frame,roster=source.advance(4))
        frame = _scene_refresh_emit(memory,frame,0xC00000,4,value)
        frame = _scene_refresh_decrement(frame,'target_x',counter)
        counter = u16(counter - 1)
        if counter == 65535:
            break
    frame = _first_long(frame,'target_x',0x41040003)
    frame = _scene_refresh_call_fields(memory,frame,0x108E2,0x108D0)
    frame = _first_word(frame,'unit',9)
    counter = 9
    while True:
        frame = _scene_refresh_call_fields(memory,frame,0x1093E,0x108D8)
        frame = _scene_refresh_decrement(frame,'unit',counter)
        counter = u16(counter - 1)
        if counter == 65535:
            break
    return _scene_refresh_call_fields(memory,frame,0x10972,0x108E0)

def draw_overlay_frame_header_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    _scene_refresh_frame(memory,frame)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,frame.target_x)
    frame = _scene_refresh_emit(memory,frame,0xC00000,2,0xC391)
    frame = _scene_refresh_repeat_pixels(memory,frame,'target_y',8,0xC392C392)
    frame = _scene_refresh_emit(memory,frame,0xC00000,2,0xCB97)
    frame = _scene_refresh_advance_command(memory,frame)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,frame.target_x)
    frame = _scene_refresh_emit(memory,frame,0xC00000,4,0xC393C394)
    frame = _scene_refresh_repeat_pixels(memory,frame,'target_y',7,0xC395C395)
    return _scene_refresh_emit(memory,frame,0xC00000,4,0xCB98DB93)

def draw_overlay_frame_middle_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    _scene_refresh_frame(memory,frame)
    frame = _scene_refresh_advance_command(memory,frame)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,frame.target_x)
    frame = _scene_refresh_emit(memory,frame,0xC00000,4,0xC393C396)
    frame = _scene_refresh_repeat_pixels(memory,frame,'target_y',7,0x43904390)
    return _scene_refresh_emit(memory,frame,0xC00000,4,0xDB96DB93)

def draw_overlay_frame_footer_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    _scene_refresh_frame(memory,frame)
    frame = _scene_refresh_advance_command(memory,frame)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,frame.target_x)
    frame = _scene_refresh_emit(memory,frame,0xC00000,4,0xC393D398)
    frame = _scene_refresh_repeat_pixels(memory,frame,'target_y',7,0xDB95DB95)
    frame = _scene_refresh_emit(memory,frame,0xC00000,4,0xDB94DB93)
    frame = _scene_refresh_advance_command(memory,frame)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,frame.target_x)
    frame = _scene_refresh_emit(memory,frame,0xC00000,4,0xD397DB92)
    frame = _scene_refresh_repeat_pixels(memory,frame,'target_y',7,0xDB92DB92)
    return _scene_refresh_emit(memory,frame,0xC00000,4,0xDB92DB91)

def clear_overlay_frame_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    _scene_refresh_frame(memory,frame)
    frame = _first_long(frame,'target_x',0x41040003)
    frame = _first_word(frame,'target_y',13)
    counter = 13
    while True:
        frame = _scene_refresh_emit(memory,frame,0xC00004,4,frame.target_x)
        frame = _scene_refresh_repeat_pixels(memory,frame,'unit',9,0)
        frame = _scene_refresh_advance_command(memory,frame)
        frame = _scene_refresh_decrement(frame,'target_y',counter)
        counter = u16(counter - 1)
        if counter == 65535:
            return frame

def load_gameplay_scene_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1072C: one load algorithm, including physical saved sound WORD.

    The fast notification arm completes without graphics. The normal arm
    requires true full3969A/177BE returns, not SceneRenderFrame's defaults.
    """
    _scene_refresh_frame(memory,frame)
    memory.sync_status(frame)
    value = memory.state.read(0xFFFFEFD6,2)
    frame = _scene_refresh_flags(memory,frame,value,2)
    if value != 0:
        frame = _first_long(frame,'target_x',0x100000)
        frame = _scene_refresh_decrement(frame,'target_x',0)
        return _scene_refresh_emit(memory,frame,0xFF7026,2,65535)
    saved_sound = memory.state.read(0xFFFFF612,2)
    if frame.stack_cursor is not None:
        stack = frame.stack_cursor.advance(-2)
        stack.set_word(0,saved_sound)
        frame = first_replace(frame,stack_cursor=stack)
    frame = _scene_refresh_flags(memory,frame,saved_sound,2)
    frame = _scene_refresh_bit_clear(memory,frame,0xFFFFF3A5,2)
    frame = _scene_refresh_call_fields(memory,frame,0x4A16,0x10744)
    frame = _scene_refresh_emit(memory,frame,0xFFFFF612,2,0x900)
    frame = _scene_refresh_call_fields(memory,frame,0xAF48,0x10750)
    frame = _scene_refresh_call_fields(memory,frame,0x83C8,0x10756)
    frame = memory.status_word(frame,0x2700)
    frame = _scene_refresh_call_fields(memory,frame,0x10814,0x1075E)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,0x40840003)
    frame = _scene_refresh_repeat_pixels(memory,frame,'target_x',5,0)
    frame = _scene_refresh_call_fields(memory,frame,0x10896,0x1077E)
    frame = _scene_refresh_call_fields(memory,frame,0x3969A,0x10784)
    frame = memory.status_word(frame,0x2700)
    frame = _scene_refresh_call_fields(memory,frame,0x109D8,0x1078C)
    frame = _scene_refresh_emit(memory,frame,0xFF7026,2,65535)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,0x40200000)
    frame = _scene_refresh_repeat_pixels(memory,frame,'target_x',7,0x11111111)
    frame = _scene_refresh_emit(memory,frame,0xFFFFF37E,2,0)
    if frame.stack_cursor is not None:
        memory.sync_status(frame)
        saved_sound = frame.stack_cursor.word()
        frame = first_replace(frame,stack_cursor=frame.stack_cursor.advance(2))
    frame = _scene_refresh_emit(memory,frame,0xFFFFF612,2,saved_sound)
    frame = _scene_refresh_bit_clear(memory,frame,0xFFFFF3A4,3)
    frame = _scene_refresh_emit(memory,frame,0xFFFFEFC8,4,0)
    frame = _scene_refresh_emit(memory,frame,0xFFFFEFCC,4,0)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,0x78000002)
    frame = _scene_refresh_emit(memory,frame,0xC00000,4,0)
    frame = _scene_refresh_emit(memory,frame,0xC00000,4,0)
    frame = _scene_refresh_call_fields(memory,frame,0x10880,0x107E8)
    value = memory.state.read(0xFFFFF6C4,2)
    frame = _first_compare_word(frame,value,1)
    if value == 1:
        frame = _scene_refresh_call_fields(memory,frame,0x177BE,0x107F8)
    return memory.sync_status(frame)


# One complete message algorithm; legacy API projects only.
def _gameplay_message_call_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long) -> FirstDeploymentFrame:
    """30A74's two real children; Scene never projects missing display ABI."""
    frame = _scene_refresh_frame(memory, frame)
    if (target, continuation) not in ((0xAF48, 0x30A8C), (0x60C, 0x30AA6)):
        raise ValueError('original gameplay message child and token required')
    entered = memory.sync_status(frame)
    if frame.stack_cursor is not None:
        stack = frame.stack_cursor.advance(-4)
        stack.set_long(0, continuation)
        entered = first_replace(frame, stack_cursor=stack)
    if target == 0xAF48:
        returned = refresh_gameplay_scene_fields(memory, entered)
    elif entered.stack_cursor is None:
        clear_scene_video_and_state(memory.state)
        returned = first_replace(entered, status=None)
    else:
        returned = clear_scene_video_and_state_fields(memory, entered)
    returned = _scene_refresh_frame(memory, returned)
    memory.sync_status(returned)
    if frame.stack_cursor is not None:
        actual = returned.stack_cursor.long()
        if actual != continuation:
            raise SceneRefreshBoundary(actual, returned, continuation)
        returned = first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))
    return returned

def present_gameplay_message_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """30A74..30ABE: physical two-WORD save, vblank child and completion wait.

    A Scene IRQ with missing full CPU fields stops at the real busy-loop read.
    Historical Gameplay supplies only its existing progress observations.
    """
    frame = _scene_refresh_frame(memory, frame)
    saved = []
    for address in (0xFFFFF612, 0xFFFFF362):
        memory.sync_status(frame)
        value = memory.state.read(address, 2)
        saved.append(value)
        if frame.stack_cursor is not None:
            stack = frame.stack_cursor.advance(-2)
            stack.set_word(0, value)
            frame = first_replace(frame, stack_cursor=stack)
        frame = _scene_refresh_flags(memory, frame, value, 2)
    frame = _scene_refresh_emit(memory, frame, 0xFFFFF612, 2, 523)
    memory.state.read(0xFFFFF600, 2)
    frame = _scene_refresh_emit(memory, frame, 0xFFFFF600, 2, 0)
    frame = _gameplay_message_call_fields(memory, frame, 0xAF48, 0x30A8C)
    frame = memory.status_word(frame, 0x2500)
    while True:
        while True:
            memory.sync_status(frame)
            command = memory.state.read(0xFFFFF600, 2)
            frame = _scene_refresh_flags(memory, frame, command, 2)
            if command:
                break
            if frame.stack_cursor is not None:
                raise SceneRefreshBoundary(0x30A90, frame, None)
            memory.state.progress('message-scene')
        command = memory.state.read(0xFFFFF600, 2)
        frame = _first_compare_word(frame, command, 40)
        memory.sync_status(frame)
        if command != 40:
            break
        frame = _gameplay_message_call_fields(memory, frame, 0x60C, 0x30AA6)
        memory.state.read(0xFFFFF600, 2)
        frame = _scene_refresh_emit(memory, frame, 0xFFFFF600, 2, 0)
        frame = memory.status_word(frame, 0x2500)
    frame = memory.status_word(frame, 0x2700)
    for address, legacy_value in ((0xFFFFF362, saved[1]), (0xFFFFF612, saved[0])):
        if frame.stack_cursor is None:
            value = legacy_value
        else:
            value = frame.stack_cursor.word()
            frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))
        frame = _scene_refresh_emit(memory, frame, address, 2, value)
    return memory.sync_status(frame)


# One current complete word-packet CPU queue successor.
def stage_sprite_word_packet_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26BFA..26C4C: full current Scene word-packet queue and dynamic control.

    This RAM staging routine does not pretend to render or progress hardware.
    Negative control words retain the actual indexed target and JSR26C36 slot;
    missing control-child fields stop there instead of accepting old scalar
    handler results as a complete CPU return.
    """
    from ..high_level_scene_flows.domain import SceneState
    from ..high_level_main_flows.business_movement_support import _movement_binary_flags
    from ..high_level_battle_ai.business_formation import _first_sub_word, _first_memory_word, _first_right_word
    frame = _scene_refresh_frame(memory, frame)
    if type(memory.state) is not SceneState or any(value is None for value in (
            frame.target_x,frame.target_y,frame.unit,frame.count,frame.distance,
            frame.offset_x,frame.offset_y,frame.choice,frame.roster,frame.candidates,
            frame.controller,frame.scan,frame.opponent,frame.scratch,frame.auxiliary,
            frame.stack_cursor,frame.status)):
        raise SceneRefreshBoundary(0x26BFA,frame,None)
    frame.validate(memory.state,True)
    destination = memory.cursor_at(0xFFFFD100)
    frame = first_replace(frame,candidates=destination)
    queued = memory.state.read(0xFFFFF31A,2)
    destination = destination.advance(s16(queued))
    frame = first_replace(frame,candidates=destination)
    rows = low16(frame.target_y)
    frame = _first_word(frame,'choice',rows)
    frame = _first_sub_word(frame,'choice',rows,1)
    for counter in descending_inclusive(u16(rows - 1)):
        destination.set_word(0,low16(frame.target_x))
        destination = destination.advance(2)
        frame = first_replace(frame,candidates=destination)
        frame = _first_memory_word(frame,low16(frame.target_x))
        destination.set_word(0,low16(frame.unit))
        destination = destination.advance(2)
        frame = first_replace(frame,candidates=destination)
        frame = _first_memory_word(frame,low16(frame.unit))
        from ..high_level_battle_ai.business_formation import _first_add_word
        frame = _first_add_word(frame,'unit',low16(frame.unit),128)
        frame = _first_word(frame,'count',low16(frame.target_x))
        while True:
            token = frame.roster.word()
            frame = first_replace(frame,roster=frame.roster.advance(2))
            frame = _first_word(frame,'distance',token)
            if negative_word(token):
                frame = _first_word(frame,'offset_x',low16(frame.distance))
                frame = _first_word(frame,'distance',low16(frame.distance) & 32767)
                frame = _first_right_word(frame,'distance',low16(frame.distance),7)
                before = frame.distance
                frame = first_replace(frame,distance=before & 4294967294,
                    status=(frame.status & 27) | (0 if before & 1 else 4))
                relative = memory.state.table(0x26C4C).word(low16(frame.distance))
                frame = _first_word(frame,'distance',relative)
                target = u32(0x26C58 + s16(relative))
                stack = frame.stack_cursor.advance(-4)
                stack.set_long(0,0x26C36)
                entered = first_replace(frame,stack_cursor=stack)
                memory.sync_status(entered)
                if target == 0x26C58:
                    frame = repeat_word_packet_control_fields(memory,entered)
                elif target == 0x26C72:
                    frame = increment_word_packet_control_fields(memory,entered)
                elif target == 0x26C8E:
                    frame = append_word_decimal_packet_control_fields(memory,entered)
                elif target == 0x26CD6:
                    frame = append_long_decimal_packet_control_fields(memory,entered)
                elif target == 0x26D1C:
                    frame = append_even_tile_pair_control_fields(memory,entered)
                elif target == 0x26D30:
                    frame = append_odd_tile_pair_control_fields(memory,entered)
                else:
                    raise SceneRefreshBoundary(target,entered,0x26C36)
                actual = frame.stack_cursor.long()
                if actual != 0x26C36:
                    raise SceneRefreshBoundary(actual,frame,0x26C36)
                frame = first_replace(frame,stack_cursor=frame.stack_cursor.advance(4))
                destination = frame.candidates
                frame = _first_memory_word(frame,low16(frame.count))
                if low16(frame.count) == 0:
                    break
                continue
            frame = _first_long(frame,'target_x',swap_words(frame.target_x))
            frame = _first_word(frame,'distance',low16(frame.distance) | low16(frame.target_x))
            destination.set_word(0,low16(frame.distance))
            destination = destination.advance(2)
            frame = first_replace(frame,candidates=destination)
            frame = _first_memory_word(frame,low16(frame.distance))
            frame = _first_long(frame,'target_x',swap_words(frame.target_x))
            frame = _first_sub_word(frame,'count',low16(frame.count),1)
            frame = _first_memory_word(frame,low16(frame.count))
            if low16(frame.count) == 0:
                break
        frame = first_replace(frame,choice=replace_word(frame.choice,u16(counter - 1)))
    destination.word()
    destination.set_word(0,0)
    frame = _first_memory_word(frame,0)
    frame = _first_add_word(frame,'target_x',low16(frame.target_x),2)
    frame = _first_long(frame,'target_x',low16(frame.target_x) * low16(frame.target_y))
    frame = _first_shift_word(frame,'target_x',low16(frame.target_x),1)
    previous = memory.state.read(0xFFFFF31A,2)
    frame,value = _movement_binary_flags(memory.state,frame,previous,low16(frame.target_x),16)
    memory.state.write(0xFFFFF31A,2,value)
    memory.sync_status(frame)
    return memory.frame(frame)


# Sole repeated/ascending negative word-packet controls.
"""One repeat/ascending word-packet core, two original handler entries."""


def _word_packet_copy_run_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, increasing: bool) -> FirstDeploymentFrame:
    """26C58/26C72: real D5 low-BYTE count, live A0/A1 and wrapped DBRA.

    Repeat and ascending tiles differ only by the actual ADDQ.W2 after each
    write. Both preserve high carriers, the original zero-count65536 path,
    and the final SUB.W/SWAP CCR rather than a normalized count or tile list.
    """
    from ..high_level_scene_flows.domain import SceneState
    from ..high_level_battle_ai.business_formation import _first_sub_word, _first_add_word, _first_memory_word
    if type(increasing) is not bool:
        raise ValueError('actual repeated or ascending word control required')
    frame = _scene_refresh_frame(memory, frame)
    entry = 0x26C72 if increasing else 0x26C58
    if type(memory.state) is not SceneState or any(value is None for value in (
            frame.target_x,frame.target_y,frame.unit,frame.count,frame.distance,
            frame.offset_x,frame.offset_y,frame.choice,frame.roster,frame.candidates,
            frame.controller,frame.scan,frame.opponent,frame.scratch,frame.auxiliary,
            frame.stack_cursor,frame.status)):
        raise SceneRefreshBoundary(entry,frame,None)
    frame.validate(memory.state,True)
    frame = _first_word(frame,'offset_x',low16(frame.offset_x) & 255)
    frame = _first_long(frame,'target_x',swap_words(frame.target_x))
    token = frame.roster.word()
    frame = first_replace(frame,roster=frame.roster.advance(2))
    frame = _first_word(frame,'distance',token)
    frame = _first_word(frame,'distance',low16(frame.distance) | low16(frame.target_x))
    count = low16(frame.offset_x)
    frame = _first_word(frame,'offset_y',count)
    frame = _first_sub_word(frame,'offset_y',count,1)
    for counter in descending_inclusive(u16(count - 1)):
        frame.candidates.set_word(0,low16(frame.distance))
        frame = first_replace(frame,candidates=frame.candidates.advance(2))
        frame = _first_memory_word(frame,low16(frame.distance))
        if increasing:
            frame = _first_add_word(frame,'distance',low16(frame.distance),2)
        # DBRA changes only this retained WORD, not CCR.
        frame = first_replace(frame,offset_y=replace_word(frame.offset_y,u16(counter - 1)))
    frame = _first_sub_word(frame,'count',low16(frame.count),low16(frame.offset_x))
    frame = _first_long(frame,'target_x',swap_words(frame.target_x))
    return memory.sync_status(frame)


def repeat_word_packet_control_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26C58..26C72: repeat one actual tile through the sole copy core."""
    return _word_packet_copy_run_fields(memory,frame,False)


def increment_word_packet_control_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26C72..26C8E: write tiles stepping by the original WORD increment2."""
    return _word_packet_copy_run_fields(memory,frame,True)

def _word_packet_numeric_control_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, wide: bool) -> FirstDeploymentFrame:
    """26C8E/26CD6 numeric slices: one decimal core, true six-LONG MOVEM and calls.

    The original reads an indirect WORD or LONG value, formats six tiles at
    D300 through1270A, then copies the selected trailing cells into A1.
    The low-BYTE zero count still means65536 DBRA cells; no normalization.
    """
    from ..high_level_scene_flows.domain import SceneState
    from ..high_level_player_commands.business_budget import _six_place_decimal_fields
    from ..high_level_player_commands.contexts_numeric import DecimalMemory
    from ..high_level_main_flows.business_movement_support import _movement_save_longs, _movement_restore_longs
    from ..high_level_battle_ai.business_formation import _first_sub_word, _first_memory_word
    if type(wide) is not bool:
        raise ValueError('actual WORD or LONG numeric control required')
    entry,continuation = (0x26CD6,0x26CF4) if wide else (0x26C8E,0x26CAE)
    frame = _scene_refresh_frame(memory,frame)
    if type(memory.state) is not SceneState or frame.stack_cursor is None:
        raise SceneRefreshBoundary(entry,frame,None)
    frame.validate(memory.state,True)
    frame = _first_word(frame,'offset_x',low16(frame.offset_x) & 255)
    pointer = frame.roster.long()
    frame = first_replace(frame,roster=frame.roster.advance(4),controller=memory.cursor_at(pointer))
    saved_names = ('target_x','target_y','unit','count','distance','offset_x')
    frame = _movement_save_longs(memory.state,frame,saved_names)
    if wide:
        value = frame.controller.long()
        frame = _first_long(frame,'target_x',value)
    else:
        frame = _first_long(frame,'target_x',0)
        value = frame.controller.word()
        frame = _first_word(frame,'target_x',value)
    digit_tile = memory.cursor_at(0xFFFFF692).word()
    frame = _first_word(frame,'target_y',digit_tile)
    blank_tile = memory.cursor_at(0xFFFFF694).word()
    frame = _first_word(frame,'unit',blank_tile)
    frame = first_replace(frame,auxiliary=memory.cursor_at(0xFFFFD300))
    memory.sync_status(frame)
    numeric = DecimalMemory(memory.state,frame.stack_cursor)
    numeric.enter_call(continuation)
    formatted = _six_place_decimal_fields(numeric,frame.target_x,
        low16(frame.target_y),low16(frame.unit),frame.auxiliary)
    numeric.leave_call(continuation)
    # These are actual1270A final scalar observations, not another decimal loop.
    frame = first_replace(frame,target_x=formatted.remainder,stack_cursor=numeric.stack_cursor,auxiliary=formatted.destination)
    frame = _first_word(frame,'count',formatted.divisor)
    frame = _first_word(frame,'distance',formatted.started)
    frame = _first_word(frame,'offset_x',formatted.glyph)
    # Last ADD.W D1,D5 then MOVE.W D5,(A6)+ retains only that ADD's X.
    status = (16 if formatted.glyph < digit_tile else 0) | (8 if formatted.glyph & 32768 else 0) | (4 if formatted.glyph == 0 else 0)
    frame = memory.sync_status(first_replace(frame,status=status))
    frame = _movement_restore_longs(memory.state,frame,saved_names)
    frame = _first_word(frame,'distance',6)
    frame = _first_sub_word(frame,'distance',6,low16(frame.offset_x))
    frame = _first_shift_word(frame,'distance',low16(frame.distance),1)
    frame = first_replace(frame,controller=memory.cursor_at(0xFFFFD300).advance(s16(low16(frame.distance))))
    count = low16(frame.offset_x)
    frame = _first_word(frame,'distance',count)
    frame = _first_sub_word(frame,'distance',count,1)
    frame = _first_long(frame,'target_x',swap_words(frame.target_x))
    for counter in descending_inclusive(u16(count - 1)):
        tile = frame.controller.word()
        frame = first_replace(frame,controller=frame.controller.advance(2))
        frame = _first_word(frame,'offset_y',tile)
        frame = _first_word(frame,'offset_y',low16(frame.offset_y) | low16(frame.target_x))
        frame.candidates.set_word(0,low16(frame.offset_y))
        frame = first_replace(frame,candidates=frame.candidates.advance(2))
        frame = _first_memory_word(frame,low16(frame.offset_y))
        frame = first_replace(frame,distance=replace_word(frame.distance,u16(counter - 1)))
    frame = _first_long(frame,'target_x',swap_words(frame.target_x))
    frame = _first_sub_word(frame,'count',low16(frame.count),low16(frame.offset_x))
    return memory.sync_status(frame)

def append_word_decimal_packet_control_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26C8E indirect unsigned WORD value, same numeric slice core."""
    return _word_packet_numeric_control_fields(memory,frame,False)

def append_long_decimal_packet_control_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26CD6 indirect LONG value, same numeric slice core."""
    return _word_packet_numeric_control_fields(memory,frame,True)

def _word_packet_tile_pair_control_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, odd: bool) -> FirstDeploymentFrame:
    """26D1C/26D30 descriptor tile pairs; no font/glyph rendering algorithm."""
    from ..high_level_scene_flows.domain import SceneState
    from ..high_level_battle_ai.business_formation import _first_add_word, _first_sub_word, _first_memory_word
    if type(odd) is not bool:
        raise ValueError('actual even or odd tile-pair control required')
    frame = _scene_refresh_frame(memory,frame)
    entry = 0x26D30 if odd else 0x26D1C
    if type(memory.state) is not SceneState or frame.roster is None or frame.candidates is None or frame.count is None or frame.offset_x is None:
        raise SceneRefreshBoundary(entry,frame,None)
    pointer = frame.roster.long()
    frame = first_replace(frame,roster=frame.roster.advance(4),controller=memory.cursor_at(pointer))
    tile = frame.controller.word()
    frame = _first_word(frame,'offset_x',tile)
    frame = _first_shift_word(frame,'offset_x',tile,2)
    base = memory.cursor_at(0xFFFFEF76).word()
    frame = _first_add_word(frame,'offset_x',low16(frame.offset_x),base)
    if odd:
        frame = _first_add_word(frame,'offset_x',low16(frame.offset_x),1)
    frame.candidates.set_word(0,low16(frame.offset_x))
    frame = first_replace(frame,candidates=frame.candidates.advance(2))
    frame = _first_memory_word(frame,low16(frame.offset_x))
    frame = _first_add_word(frame,'offset_x',low16(frame.offset_x),2)
    frame.candidates.set_word(0,low16(frame.offset_x))
    frame = first_replace(frame,candidates=frame.candidates.advance(2))
    frame = _first_memory_word(frame,low16(frame.offset_x))
    frame = _first_sub_word(frame,'count',low16(frame.count),2)
    return memory.sync_status(frame)

def append_even_tile_pair_control_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26D1C publishes descriptor*4+EF76 and its second tile."""
    return _word_packet_tile_pair_control_fields(memory,frame,False)

def append_odd_tile_pair_control_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26D30 retains the original extra ADDQ.W1 before both tile writes."""
    return _word_packet_tile_pair_control_fields(memory,frame,True)

def _video_plane_dma_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, sprite: bool) -> FirstDeploymentFrame:
    """Shared exact DMA control tail; an active unobserved device is not success."""
    if type(sprite) is not bool:
        raise ValueError('actual video initialization or sprite-plane entry required')
    frame = _scene_refresh_frame(memory, frame)
    frame = first_replace(frame, auxiliary=memory.cursor_at(12582916))
    frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, 36609)
    register = memory.cursor_at(4294964742).word()
    frame = _first_word(frame, 'choice', register)
    frame = _first_byte(frame, 'choice', low8(register) | 16)
    frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, register | 16)
    frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 4, 2483000391 if sprite else 2483000575)
    frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, 38784)
    frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 4, 2013266050 if sprite else 1073741952)
    frame = _scene_refresh_emit(memory, frame, 12582912, 2, 246 if sprite else 0)
    while True:
        response = frame.auxiliary.word()
        frame = _first_word(frame, 'choice', response)
        frame = _first_word(frame, 'choice', response & 2)
        if response & 2 == 0:
            break
        memory.state.progress('vdp-dma')
        frame = first_replace(frame, status=memory.state.sr & 31)
    released = memory.cursor_at(16727808).byte()
    frame = _scene_refresh_flags(memory, frame, released, 1)
    if released == 0:
        frame = _scene_refresh_emit(memory, frame, 10555648, 2, 0)
    restored = memory.cursor_at(4294964742).word()
    frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, restored)
    return _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, 36610)

def initialize_video_registers_and_planes_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """6826 sole live register catalog, zero plane and physical DMA-control fields."""
    frame = _scene_refresh_frame(memory,frame)
    frame = first_replace(frame,roster=memory.cursor_at(0xC00004),candidates=memory.cursor_at(0xC00000),controller=memory.cursor_at(0x68A8))
    frame = _first_long(frame,'choice',18)
    for counter in descending_inclusive(18):
        register = frame.controller.word()
        frame = first_replace(frame,controller=frame.controller.advance(2))
        frame = _scene_refresh_emit(memory,frame,frame.roster.base,2,register)
        frame = _scene_refresh_decrement(frame,'choice',counter)
    initial = memory.cursor_at(0x68AA).word()
    frame = _scene_refresh_emit(memory,frame,0xFFFFF606,2,initial)
    frame = _first_long(frame,'target_x',0)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,0xC0000000)
    frame = _first_word(frame,'choice',63)
    for counter in descending_inclusive(63):
        frame = _scene_refresh_emit(memory,frame,frame.candidates.base,2,low16(frame.target_x))
        frame = _scene_refresh_decrement(frame,'choice',counter)
    return memory.sync_status(_video_plane_dma_fields(memory,frame,False))

def clear_video_sprite_plane_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """68CE sole sprite-plane clear; ordered bus writes and actual D6/D7/A6 return."""
    frame = _video_plane_dma_fields(memory,frame,True)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,0x40000010)
    frame = _scene_refresh_emit(memory,frame,0xC00000,4,0)
    frame = _scene_refresh_emit(memory,frame,0xFFFFF312,4,0)
    frame = _scene_refresh_emit(memory,frame,0xFFFFF316,4,0)
    frame = first_replace(frame,auxiliary=memory.cursor_at(0xFFFFF800))
    frame = _first_long(frame,'choice',0)
    frame = _first_word(frame,'offset_y',159)
    for counter in descending_inclusive(159):
        destination = frame.auxiliary
        frame = first_replace(frame,auxiliary=destination.advance(4))
        frame = _scene_refresh_emit(memory,frame,destination.base,4,frame.choice)
        frame = _scene_refresh_decrement(frame,'offset_y',counter)
    return memory.sync_status(frame)

def copy_video_transfer_descriptor_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        observed_index: Word | None = None) -> FirstDeploymentFrame:
    """8112: sole descriptor selection, inclusive LONG copy and live marker RMW.

    The historical WORD index is a real observation, not a made-up D0 high
    half. Complete Scene callers already carry it in the actual D0 field.
    """
    from ..high_level_main_flows.business_movement_support import _movement_binary_flags
    memory.frame(frame)
    if observed_index is None:
        if frame.target_x is None:
            raise SceneRefreshBoundary(0x8112,frame,None)
        index = low16(frame.target_x)
    else:
        index = uint(observed_index,16)
        if frame.target_x is not None and low16(frame.target_x) != index:
            raise ValueError('actual descriptor WORD index differs from retained D0')
    frame = first_replace(frame,candidates=memory.cursor_at(0x812C))
    frame = memory.sync_status(_first_shift_word(frame,'target_x',index,3))
    frame = first_replace(frame,candidates=frame.candidates.advance(s16(u16(index << 3))))
    descriptor = frame.candidates
    address = descriptor.long()
    frame = first_replace(frame,candidates=descriptor.advance(4),controller=memory.cursor_at(address))
    descriptor = frame.candidates
    address = u32(s16(descriptor.word()))
    frame = first_replace(frame,candidates=descriptor.advance(2),scan=memory.cursor_at(address))
    descriptor = frame.candidates
    remaining = descriptor.word()
    frame = first_replace(frame,candidates=descriptor.advance(2))
    frame = memory.sync_status(_first_word(frame,'choice',remaining))
    while True:
        source,destination = frame.controller,frame.scan
        value = source.long()
        # Source postincrement occurs before destination addressing, as in
        # MOVE.L (A2)+,(A3)+; overlapping live memory is never snapshotted.
        frame = first_replace(frame,controller=source.advance(4))
        frame = _scene_refresh_emit(memory,frame,destination.base,4,value)
        frame = first_replace(frame,scan=destination.advance(4))
        frame = _scene_refresh_decrement(frame,'choice',remaining)
        remaining = u16(remaining - 1)
        if remaining == 65535:
            break
    memory.sync_status(frame)
    previous = memory.state.read(0xFFFFF31E,2)
    frame,value = _movement_binary_flags(memory.state,frame,previous,1,16)
    memory.state.write(0xFFFFF31E,2,value)
    return memory.sync_status(frame)


def select_scene_fill_pattern_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """68A: retain D0 high WORD, original two-bit shift/X and full D1 pattern."""
    frame = _scene_refresh_frame(memory, frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x68A, frame, None)
    memory.sync_status(frame)
    frame = _first_word(frame, 'target_x', memory.state.read(0xFFFFF6C4, 2))
    frame = _first_shift_word(frame, 'target_x', low16(frame.target_x), 2)
    memory.sync_status(frame)
    pattern = memory.cursor_at(0x696).long(s16(low16(frame.target_x)))
    return memory.sync_status(_first_long(frame, 'target_y', pattern))


def clear_scene_video_and_state_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """60C: clear active video/RAM planes with the genuine selector and VDP wait."""
    frame = _scene_refresh_frame(memory, frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x60C, frame, None)
    frame = memory.status_word(frame, 0x2700)
    frame = _scene_refresh_call_fields(memory, frame, 0x68A, 0x614)
    memory.sync_status(frame)
    memory.state.read(0xFFFFF37E, 2)
    frame = _scene_refresh_emit(memory, frame, 0xFFFFF37E, 2, 0)
    frame = _scene_refresh_emit(memory, frame, 0xC00004, 4, 0x60A00002)
    frame = _scene_refresh_repeat_pixels(memory, frame, 'target_x', 0x59F, frame.target_y)
    memory.sync_status(frame)
    active = memory.state.read(0xFFFFF6C4, 2)
    frame = _scene_refresh_flags(memory, frame, active, 2)
    if active == 0:
        frame = _scene_refresh_emit(memory, frame, 0xC00004, 4, 0x70000001)
        for address, count in ((0x89DDC, 0x17), (0x8A07C, 0xF)):
            frame = first_replace(frame, roster=memory.cursor_at(address))
            frame = _first_word(frame, 'target_x', count)
            for counter in descending_inclusive(count):
                memory.sync_status(frame)
                source = frame.roster
                value = source.long()
                frame = first_replace(frame, roster=source.advance(4))
                frame = _scene_refresh_emit(memory, frame, 0xC00000, 4, value)
                frame = _scene_refresh_decrement(frame, 'target_x', counter)
    frame = _scene_refresh_call_fields(memory, frame, 0x68A, 0x66C)
    frame = first_replace(frame, roster=memory.cursor_at(0xFFFFF516))
    frame = _first_word(frame, 'target_x', 0x17)
    for counter in descending_inclusive(0x17):
        destination = frame.roster
        frame = first_replace(frame, roster=destination.advance(4))
        frame = _scene_refresh_emit(memory, frame, destination.base, 4, frame.target_y)
        frame = _scene_refresh_decrement(frame, 'target_x', counter)
    for address in (0xFFFFF37A, 0xFFFFF37C):
        memory.sync_status(frame)
        memory.state.read(address, 2)
        frame = _scene_refresh_emit(memory, frame, address, 2, 0)
    return _scene_refresh_call_fields(memory, frame, 0xAF48, 0x688)
