"""Selected shared source rules, adapted to this family's own live state.

Covered original bodies and the92-byte progress tail add no new physical
coverage. No old State, compiled program, opcode list or media dump is called.
"""
from .domain import Byte, Cursor, Long, RandomSample, SceneState, Word, checked_cursor, checked_state, descending_inclusive, divu_retained, low16, low8, negative_byte, negative_word, replace_byte, replace_word, s16, swap_words, u16, u32, uint
from .contexts_reuse import ControlChoice, GlyphColors, GlyphStreamResult, SpriteControlContext, SpriteControlResult, GlyphSavedValues, SpritePacketContext, VideoClearResult

from .contexts_reuse import SceneRefreshMemory, FirstDeploymentFrame, enqueue_sound_command_fields, wait_for_scene_sound_byte_fields

def _save_glyph_values(state, saved, include_source):
    if type(saved) is not GlyphSavedValues:
        raise ValueError('actual glyph MOVEM operands required')
    saved.validate(state)
    values = (saved.working, saved.repeat, saved.response, saved.pixels)
    if include_source:
        values += (saved.glyph_source.base,)
    for value in values[::-1]:
        saved.stack.base = u32(saved.stack.base - 4)
        saved.stack.set_long(0, value)

def _restore_glyph_values(state, saved, glyph_source, include_source):
    working, repeat, response, pixels = tuple(saved.stack.next_long() for _ in range(4))
    if include_source:
        glyph_source = state.table(saved.stack.next_long())
    return GlyphSavedValues(working, repeat, response, pixels, glyph_source, saved.stack).validate(state)

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

def clear_video_sprite_plane(state: SceneState, response: Long | None = None) -> VideoClearResult | None:
    """Historical Scene facade shares the sole68CE core, not another DMA algorithm."""
    from ..high_level_gameplay_flow.business_services import clear_video_sprite_plane_fields
    from .contexts_scene import first_replace
    checked_state(state)
    if response is not None:
        uint(response,32)
    frame = first_replace(FirstDeploymentFrame.unobserved(),offset_y=response)
    actual = clear_video_sprite_plane_fields(SceneRefreshMemory(state),frame)
    if response is not None:
        return VideoClearResult(actual.offset_y,actual.choice,actual.auxiliary).validate(state)
    return None

def enqueue_sound_command(state: SceneState, command: Byte) -> None:
    """Historical BYTE interface projects the sole808A same-state core."""
    checked_state(state)
    enqueue_sound_command_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved(),command)

def wait_for_scene_sound_byte(state: SceneState) -> None:
    checked_state(state)
    wait_for_scene_sound_byte_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())

def expand_glyph_row(state: SceneState, source: Cursor, background: Byte, foreground: Byte) -> Long:
    """The historical BYTE-color result projects the sole AF04 fields."""
    from .business_scene import expand_glyph_row_fields
    from .contexts_scene import first_replace
    checked_state(state)
    checked_cursor(source,state)
    uint(background,8)
    uint(foreground,8)
    entered = first_replace(FirstDeploymentFrame.unobserved(),target_x=background,target_y=foreground,controller=source.advance(0))
    actual = expand_glyph_row_fields(SceneRefreshMemory(state),entered)
    source.base = actual.controller.base
    return actual.choice

def expand_glyph_stream(state: SceneState, tokens: Cursor, destination: Cursor,
        colors: GlyphColors, remaining: Long, saved: GlyphSavedValues | None = None) -> GlyphStreamResult:
    """Historical stream and optional MOVEM observations project the one AF1E core."""
    from .business_scene import expand_glyph_stream_fields
    from .contexts_scene import first_replace
    checked_state(state)
    checked_cursor(tokens,state)
    checked_cursor(destination,state)
    if type(colors) is not GlyphColors:
        raise ValueError('explicit glyph colors required')
    colors.__post_init__()
    uint(remaining,32)
    if saved is not None:
        _save_glyph_values(state,saved,False)
    entered = first_replace(FirstDeploymentFrame.unobserved(),roster=tokens.advance(0),
        candidates=destination.advance(0),target_x=colors.background,target_y=colors.foreground,count=remaining)
    actual = expand_glyph_stream_fields(SceneRefreshMemory(state),entered)
    tokens.base,destination.base = actual.roster.base,actual.candidates.base
    if saved is not None:
        saved = _restore_glyph_values(state,saved,actual.controller,False)
    return GlyphStreamResult(tokens,destination,actual.count,saved)

def stage_sprite_word_packet(state: SceneState, source: Cursor,
                             command: Long, rows: Word, row_command: Word,
                             current: SpritePacketContext | None = None) -> Long | SpritePacketContext:
    """Retain negative-token dispatch; missing handlers are explicit stops."""
    checked_state(state)
    checked_cursor(source, state)
    uint(command, 32)
    uint(rows, 16)
    uint(row_command, 16)
    if current is not None:
        if type(current) is not SpritePacketContext:
            raise ValueError('actual complete packet operands required')
        current.validate(state)
        if (current.command, low16(current.rows), low16(current.row_command)) != (command, rows, row_command) or current.source is not source:
            raise ValueError('packet arguments must agree with current caller')
        rows_carrier, row_carrier = current.rows, current.row_command
        remaining_carrier, token_carrier = current.remaining, current.token
        run_count, response = current.run_count, current.response
        rows_remaining = replace_word(current.rows_remaining, u16(rows - 1))
        glyph_source = current.glyph_source
        stack = current.stack
    destination = state.table(0xFFFFD100).cursor(state.read(0xFFFFF31A, 2))
    row_counter = u16(rows - 1)
    while True:
        destination.append_word(low16(command))
        destination.append_word(row_command)
        row_command = u16(row_command + 0x80)
        remaining = low16(command)
        if current is not None:
            row_carrier = replace_word(row_carrier, row_command)
            remaining_carrier = replace_word(remaining_carrier, remaining)
        while True:
            token = source.next_word()
            if negative_word(token):
                dispatch_offset = u16((token & 0x7FFF) >> 7) & 65534
                relative_target = state.table(0x26C4C).word(dispatch_offset)
                target = u32(0x26C58 + s16(relative_target))
                if current is None:
                    result = state.service_at(target, SpriteControlContext(
                        token, command, remaining, source, destination))
                    if type(result) is not SpriteControlResult:
                        raise ValueError('real sprite control result required')
                    result.__post_init__()
                    command, remaining = result.command, result.row_remaining
                else:
                    run_count = replace_word(run_count, token)
                    token_carrier = replace_word(token_carrier, relative_target)
                    result = state.service_at(target, SpritePacketContext(command,
                        rows_carrier, row_carrier, remaining_carrier, token_carrier,
                        run_count, response, rows_remaining, source, destination,
                        glyph_source, stack.advance(-4), False,
                        relative_target == 0, bool(relative_target & 32768), False))
                    if type(result) is not SpritePacketContext:
                        raise ValueError('complete sprite handler return required')
                    result.validate(state)
                    command, rows_carrier, row_carrier = result.command, result.rows, result.row_command
                    remaining_carrier, token_carrier = result.remaining, result.token
                    run_count, response = result.run_count, result.response
                    rows_remaining, source, destination = result.rows_remaining, result.source, result.destination
                    glyph_source = result.glyph_source
                    stack = result.stack.advance(4)
                    rows, row_command, remaining = low16(rows_carrier), low16(row_carrier), low16(remaining_carrier)
            else:
                command = swap_words(command)
                tile = u16(token | low16(command))
                destination.append_word(tile)
                command = swap_words(command)
                remaining = u16(remaining - 1)
                if current is not None:
                    token_carrier = replace_word(token_carrier, tile)
                    remaining_carrier = replace_word(remaining_carrier, remaining)
            if remaining == 0:
                break
        if current is not None:
            rows_remaining = replace_word(rows_remaining, u16(low16(rows_remaining) - 1))
            row_counter = low16(rows_remaining)
        else:
            row_counter = u16(row_counter - 1)
        if row_counter == 65535:
            break
    destination.put_word(0)
    command = replace_word(command, u16(low16(command) + 2))
    allocated = u16(u16(low16(command) * rows) << 1)
    queue_offset = state.read(0xFFFFF31A, 2)
    next_queue_offset = u16(queue_offset + allocated)
    state.write(0xFFFFF31A, 2, next_queue_offset)
    command = replace_word(low16(command) * rows, allocated)
    if current is not None:
        return SpritePacketContext(command, rows_carrier, row_carrier, remaining_carrier,
            token_carrier, run_count, response, rows_remaining, source, destination,
            glyph_source, stack, queue_offset + allocated > 65535,
            next_queue_offset == 0, bool(next_queue_offset & 32768),
            bool((~(queue_offset ^ allocated) & (queue_offset ^ next_queue_offset)) & 32768)).validate(state)
    return command

def build_battlefield_outcome_candidates(state: SceneState) -> Word:
    checked_state(state)
    destination = state.action_candidates.cursor()
    city = state.scalar('battle_scene')
    count = 0
    for officer in descending_inclusive(255):
        if state.battlefield_city_assignment.byte(officer) == low8(city):
            if not negative_byte(state.officer_city_assignment.byte(officer)):
                destination.append_word(officer)
                count = u16(count + 1)
    destination.put_word(65535)
    return count

def step_random(state: SceneState) -> Long:
    """Return full original sample carrier; its upper WORD is the old seed's."""
    return _reuse_advance_random_pair(state).sample

def _reuse_advance_random_pair(state: SceneState) -> RandomSample:
    checked_state(state)
    original = state.scalar('random_seed')
    if original == 0:
        original = 711800410
    mixed = u32(u32(u32(u32(original << 2) + original) << 3) + original)
    sample = replace_word(original, low16(mixed))
    mixed = swap_words(mixed)
    sample = replace_word(sample, u16(low16(sample) + low16(mixed)))
    mixed = swap_words(replace_word(mixed, low16(sample)))
    state.set_scalar('random_seed', mixed)
    return RandomSample(sample, mixed)

def _choose_duel_control(state:SceneState,command_carrier:Long,mode_carrier:Long,
                         primary_address:Long,secondary_address:Long)->ControlChoice:
    from .contexts_scene import first_replace
    checked_state(state)
    uint(command_carrier,32)
    uint(mode_carrier,32)
    if (primary_address,secondary_address) not in ((0xFF700A,0xFF700B),(0xFF700B,0xFF700A)):
        raise ValueError('one of the actual two control-query roles required')
    entered=first_replace(FirstDeploymentFrame.unobserved(),
        target_x=command_carrier,target_y=mode_carrier)
    actual=choose_duel_control_fields(state,entered,primary_address==0xFF700B)
    return ControlChoice(actual.target_x,actual.target_y)

def choose_first_duel_control(state:SceneState,command_carrier:Long,
                              mode_carrier:Long)->ControlChoice:
    """279E6: read live700A first; retain command/mode upper bits."""
    return _choose_duel_control(state,command_carrier,mode_carrier,0xFF700A,0xFF700B)

def choose_second_duel_control(state:SceneState,command_carrier:Long,
                               mode_carrier:Long)->ControlChoice:
    """27A10: read live700B first; do not snapshot conditional reads."""
    return _choose_duel_control(state,command_carrier,mode_carrier,0xFF700B,0xFF700A)

def distribute_battle_progress_tail(state:SceneState,count:Word,budget:Word)->None:
    """1C586 shared tail only: no roster rebuild or extra EFB8 read."""
    checked_state(state)
    uint(count,16)
    uint(budget,16)
    if count==0:
        return
    award=divu_retained(budget,count)
    roster=state.table(0xFFFFD300).cursor()
    ability,progress=state.table(0xFFFFC000),state.table(0xFFFFBE00)
    while True:
        member=roster.next_word()
        if negative_word(member):
            return
        offset=u16(member<<1)
        current=ability.word(offset)
        if current>progress.word(offset):
            ability.set_word(offset,min(u16(current+low16(award)),999))
        else:
            current=progress.word(offset)
            progress.set_word(offset,min(u16(current+low16(award)),999))


def choose_duel_control_fields(state: SceneState, frame: FirstDeploymentFrame,
        second: bool=False) -> FirstDeploymentFrame:
    """279E6/27A10: exact conditional BYTE/WORD reads, preserving original X."""
    from ..high_level_battle_ai.business_formation import _first_word, _first_byte
    from ..high_level_battle_ai.business_geometry import _contact_status
    checked_state(state)
    if type(frame) is not FirstDeploymentFrame or type(second) is not bool:
        raise ValueError('actual current control-query fields and original side required')
    frame.validate(state,frame.stack_cursor is not None)
    uint(frame.target_x,32)
    uint(frame.target_y,32)
    primary,secondary=(0x00FF700B,0x00FF700A) if second else (0x00FF700A,0x00FF700B)
    frame=_first_word(frame,'target_x',state.read(0xFFFFF602,2))
    frame=_first_byte(frame,'target_y',state.read(primary,1))
    mode=low8(frame.target_y)
    frame=_contact_status(frame,mode,8)
    if mode!=0:
        frame=_first_word(frame,'target_x',state.read(0xFFFFF604,2))
        value=(mode-1)&255
        frame=_contact_status(frame,value,8,mode<1,
            bool((mode^1)&(mode^value)&128))
        if mode!=1:
            frame=_first_byte(frame,'target_y',state.read(secondary,1))
            mode=low8(frame.target_y)
            value=(mode-1)&255
            frame=_contact_status(frame,value,8,mode<1,
                bool((mode^1)&(mode^value)&128))
            if mode!=1:
                frame=_first_word(frame,'target_x',state.read(0xFFFFF602,2))
    if frame.status is not None:
        state.sr=(state.sr&65504)|frame.status
    return frame.validate(state,frame.stack_cursor is not None)


def choose_first_duel_control_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Primary700A, then conditional700B; no callee-owned outer token."""
    return choose_duel_control_fields(state,frame,False)


def choose_second_duel_control_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Primary700B, then conditional700A; all untouched carriers pass through."""
    return choose_duel_control_fields(state,frame,True)
