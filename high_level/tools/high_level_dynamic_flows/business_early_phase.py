"""Early scene decisions, exchange, allocation and presentation phases.

Resource bytes stay in explicitly supplied readonly tables. Hardware and
asynchronous arrivals use the shared live scene boundary. Encoded dispatch
slots are not assumed to constrain the natural full-WORD selector domain.
"""
from dataclasses import replace
from .domain import (SceneState, Cursor, Long, Word, VideoPlaneAddress, Boundary,
                     uint, u8, u16, u32, low8, low16, replace_byte, replace_word,
                     swap_words, s16, negative_word, divu_retained,
                     checked_state, checked_cursor, ram_view)
from .contexts_early_phase import (PhaseFrame, DecimalDigitsResult, checked_phase,
    SceneControllerFrame, SceneControllerOutcome, phase_from_controller,
    phase_controller_return, phase_operands, phase_logic, phase_compare,
    phase_add_word, phase_shifted_selector, phase_bit, SceneControllerConditions,
    phase_enter_call, phase_finish_call)
from .services import (advance_scene_palette_fade, append_unclipped_scene_sprites,
                       set_vram_write_address, read_vdp_plane_rle_rows_from_control,
                       sample_random_preserving_seed_carrier, enqueue_sound_command,
                       clear_scene_object_label_plane,
                       initialize_scene_object_roster_after_mode_check,
                       SceneRenderFrame)



from .services import (
    SceneRefreshMemory,SceneRefreshBoundary,FirstDeploymentFrame,first_replace,
    _first_word,_scene_refresh_flags,_scene_render_bit,_scene_render_compare,
    _scene_render_asl_word,_object_adjust_word_fields,
    _scene_controller_legacy_fields,_scene_controller_legacy_projection,
)

def _ram(state, low):
    return ram_view(state, 'ram_' + low)


def _word(state, low):
    return _ram(state, low).word()


def _put(state, low, value):
    _ram(state, low).set_word(0, u16(value))


def _increment(state, low):
    value = u16(_word(state, low) + 1)
    _put(state, low, value)
    return value


def _video_fill(state, command, value, counter, frame=None):
    state.mmio_write(0xC00004, 4, command)
    for _ in range(counter + 1):
        state.mmio_write(0xC00000, 2, value)
    if frame is None:
        return None
    frame = phase_operands(frame, phase_logic(value),
        glyph_tokens=replace_word(frame.glyph_tokens, 0xFFFF))
    if frame.live is not None:
        live = replace(frame.live,
            row_count=replace_word(frame.live.row_count, value),
            traversal=state.table(0xC00000).cursor())
        frame = phase_from_controller(state, live)
    return frame


def _clear_text(state, frame=None):
    state.mmio_write(0xC00004, 2, 0x8F02)
    return _video_fill(state, 0x60000002, 0x3333, 0xD7F, frame)


def _clear_background(state):
    _video_fill(state, 0x40000003, 0x0400, 0x4BF)


def _script(state, source, frame=None):
    state.write(0xFF700C, 2, 0xA000)
    state.write(0xFF700E, 4, source)
    state.write(0xFF7014, 2, 3)
    state.write(0xFF7016, 2, 1)
    return None if frame is None else phase_operands(frame, phase_logic(1))


def _load_panel(state, source, frame=None):
    _put(state, '8000', 0x8000)
    if frame is not None and frame.live is not None:
        live = replace(phase_controller_return(state, frame),
            source=state.table(source).cursor(), destination=VideoPlaneAddress(0xC000),
            extent=0x80, row_count=replace_word(frame.live.row_count, 18))
        called = phase_enter_call(state, live, 0x3E4B2)
        result = state.service_at(0x3AACE, called)
        if type(result) is not SceneControllerFrame:
            raise Boundary('3AACE panel decoder requires its actual complete frame return')
        result.validate(state)
        return phase_from_controller(state, phase_finish_call(state, result, 0x3E4B2))
    return read_vdp_plane_rle_rows_from_control(state, state.table(source).cursor(),
        VideoPlaneAddress(0xC000), 0x80, 18)


def _late(state, frame, name, continuation=None):
    from . import business_late_phase
    callee = getattr(business_late_phase, name)
    if frame.live is None:
        return callee(state, frame)
    if continuation is None:
        raise Boundary('complete phase needs the actual known internal call continuation')
    current = phase_controller_return(state, frame)
    actual = callee(state, phase_from_controller(state,
        phase_enter_call(state, current, continuation)))
    if type(actual) is SceneControllerOutcome:
        return actual.validate(state)
    returned = phase_controller_return(state, actual)
    return phase_from_controller(state, phase_finish_call(state, returned, continuation))

















def _upload_object_officer_name(state, frame):
    from .business_actions import upload_object_officer_name
    from .contexts_actions import DuelGlyphContext
    glyphs = DuelGlyphContext(frame.video_command, frame.foreground, frame.row_count)
    result = upload_object_officer_name(state, frame.glyph_tokens, glyphs)
    return replace(frame, video_command=result.tile_counter,
                   foreground=result.glyphs.foreground,
                   row_count=result.glyphs.remaining,
                   glyph_tokens=result.officer_offset)





def begin_scene_palette_lighten(state: SceneState, value: Long) -> Long:
    """Historical observations project the sole complete scene algorithm."""
    checked_state(state)
    actual=FirstDeploymentFrame.unobserved()
    uint(value,32)
    actual=first_replace(actual,target_x=value)
    returned=begin_scene_palette_lighten_fields(SceneRefreshMemory(state),actual)
    return returned.target_x



def snapshot_scene_palette(state: SceneState) -> None:
    """Historical observations project the sole complete scene algorithm."""
    checked_state(state)
    actual=FirstDeploymentFrame.unobserved()
    returned=snapshot_scene_palette_fields(SceneRefreshMemory(state),actual)
    return None



def restore_scene_palette(state: SceneState) -> None:
    """Historical observations project the sole complete scene algorithm."""
    checked_state(state)
    actual=FirstDeploymentFrame.unobserved()
    returned=restore_scene_palette_fields(SceneRefreshMemory(state),actual)
    return None



def append_decimal_digit(state: SceneState, value: Long, divisor: Word, destination: Cursor) -> DecimalDigitsResult:
    """Historical observations project the sole complete scene algorithm."""
    checked_state(state)
    actual=FirstDeploymentFrame.unobserved()
    uint(value,32)
    actual=first_replace(actual,target_x=value)
    uint(divisor,16)
    checked_cursor(destination,state)
    actual=first_replace(actual,unit=divisor,roster=destination)
    returned=append_decimal_digit_fields(SceneRefreshMemory(state),actual)
    return DecimalDigitsResult(returned.target_x,returned.roster).validate(state)



def encode_six_decimal_digits(state: SceneState, value: Long) -> DecimalDigitsResult:
    """Historical observations project the sole complete scene algorithm."""
    checked_state(state)
    actual=FirstDeploymentFrame.unobserved()
    uint(value,32)
    actual=first_replace(actual,target_x=value)
    returned=encode_six_decimal_digits_fields(SceneRefreshMemory(state),actual)
    return DecimalDigitsResult(returned.target_x,returned.roster).validate(state)



def adjust_scene_scroll(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    actual = _phase_legacy_fields(state,frame,0x3D970)
    return _phase_legacy_projection(state,frame,adjust_scene_scroll_fields(SceneRefreshMemory(state),actual))


def step_main_scene_phase(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    actual = _phase_legacy_fields(state,frame,0x3DCC2,True)
    return _phase_legacy_projection(state,frame,step_main_scene_phase_fields(SceneRefreshMemory(state),actual))


def step_result_scene_phase(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3dcc6)
    returned=step_result_scene_phase_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def step_confirmation_scene_phase(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3dcca)
    returned=step_confirmation_scene_phase_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def step_transfer_scene_phase(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3dcce)
    returned=step_transfer_scene_phase_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def step_primary_detail_scene_phase(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3dcd2)
    returned=step_primary_detail_scene_phase_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def step_secondary_detail_scene_phase(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3dcd6)
    returned=step_secondary_detail_scene_phase_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def step_summary_scene_phase(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3dcda)
    returned=step_summary_scene_phase_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def step_pair_transition_scene_phase(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3dcde)
    returned=step_pair_transition_scene_phase_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def step_initial_scene_phase(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3dce2)
    returned=step_initial_scene_phase_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def step_exchange_scene_phase(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3dce6)
    returned=step_exchange_scene_phase_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)






def initialize_early_scene(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3dcf8)
    returned=initialize_early_scene_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)









def process_early_scene_choice(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3dcfc)
    returned=process_early_scene_choice_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)






def append_early_scene_instruction(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3e37a)
    returned=append_early_scene_instruction_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def draw_early_scene_choice(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3e254)
    returned=draw_early_scene_choice_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)






def present_early_scene_prompt(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3dd00)
    returned=present_early_scene_prompt_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def finish_early_scene_prompt(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3dd04)
    returned=finish_early_scene_prompt_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def wait_early_scene_choice(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3dd08)
    returned=wait_early_scene_choice_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def finish_early_scene_fade(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3dd0c)
    returned=finish_early_scene_fade_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def finish_alternate_scene_fade(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3dd10)
    returned=finish_alternate_scene_fade_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def paint_scene_number_row(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3e43a)
    returned=paint_scene_number_row_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def paint_scene_number_rows(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3e42a)
    returned=paint_scene_number_rows_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def wait_exchange_scene_transition(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3e46c)
    returned=wait_exchange_scene_transition_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def process_exchange_scene_choice(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3e470)
    returned=process_exchange_scene_choice_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def finish_exchange_scene_transition(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3e474)
    returned=finish_exchange_scene_transition_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def gather_early_scene_input(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical phase observations project the sole complete live-RAM rule."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    entered=_phase_legacy_fields(state,frame,0x3e632)
    returned=gather_early_scene_input_fields(SceneRefreshMemory(state),entered)
    return _phase_legacy_projection(state,frame,returned)


def exchange_scene_pair_fields(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical phase observations project the sole complete live-RAM rule."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    entered=_phase_legacy_fields(state,frame,0x3e6e8)
    returned=exchange_scene_pair_frame_fields(SceneRefreshMemory(state),entered)
    return _phase_legacy_projection(state,frame,returned)


def exchange_scene_actor_records(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical phase observations project the sole complete live-RAM rule."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    entered=_phase_legacy_fields(state,frame,0x3e7ae)
    returned=exchange_scene_actor_records_fields(SceneRefreshMemory(state),entered)
    return _phase_legacy_projection(state,frame,returned)


def refresh_primary_actor_summary(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical phase observations project the sole complete live-RAM rule."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    entered=_phase_legacy_fields(state,frame,0x3e8a0)
    returned=refresh_primary_actor_summary_fields(SceneRefreshMemory(state),entered)
    return _phase_legacy_projection(state,frame,returned)


def process_pair_phase_counter(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3e622)
    returned=process_pair_phase_counter_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)






def _allocate_actor_rows(state, base, frame):
    command = _word(state, '8106')
    percentage = u32(_word(state, '8102') * command)
    percentage = divu_retained(percentage, 100)
    extra = _word(state, '80f2')
    actor = _ram(state, base)
    for index in range(15):
        offset = u16(index * 16)
        actor.set_word(offset + 12, low16(percentage))
        actor.set_word(offset + 14, _word(state, '80ee'))
        if extra != 0:
            extra = u16(extra - 1)
            actor.set_word(offset + 14, u16(actor.word(offset + 14) + 1))
    return replace(frame, video_command=replace_word(frame.video_command, 0xFFFF),
        foreground=percentage, mode=replace_word(frame.mode, extra))


def confirm_pair_allocation(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3e626)
    returned=confirm_pair_allocation_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def _confirm_pair_allocation(state, frame):
    _increment(state, '813c')
    state.set_status_word(0x2700)
    frame = _allocate_actor_rows(state, '817a', frame)
    frame = refresh_primary_actor_summary(state, frame)
    _clear_background(state)
    _video_fill(state, 0x60000002, 0x3333, 0xD7F)
    _script(state, 0x3B34A)
    state.set_status_word(0x2500)
    return frame


def _scene_rule_frame_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        entry: int) -> FirstDeploymentFrame:
    """Full current ABI only; no zero filling historical PhaseFrame omissions."""
    from ..high_level_remaining_flows.business_city import _resource_cost_frame
    if type(memory) is not SceneRefreshMemory:
        raise ValueError('same typed Scene rule memory required')
    return _resource_cost_frame(memory.state,frame,entry)


def _scene_rule_store_word_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        address: Long, value: Word, clear: bool = False) -> FirstDeploymentFrame:
    """Original MOVE or CLR WORD writes reuse the shared live flag/clear core."""
    from ..high_level_scene_flows.business_objects import _object_clear_word_fields
    from ..high_level_gameplay_flow.business_services import _scene_refresh_emit
    if clear:
        return _object_clear_word_fields(memory,frame,address)
    return _scene_refresh_emit(memory,frame,address,2,low16(value))


def _scene_rule_input_bit_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        address: Long, bit: Word) -> tuple[FirstDeploymentFrame, bool]:
    """Every BTST occurrence rereads its actual BYTE and changes only Z."""
    memory.sync_status(frame)
    value=memory.state.read(address,1)
    frame=_scene_render_bit(memory,frame,value,1<<bit)
    return frame,bool(value&(1<<bit))


def gather_early_scene_input_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3E632: original per-mode controller-word merge, all reads remain ordered."""
    from ..high_level_main_flows.business_movement_support import _movement_move, _movement_test, _movement_compare
    frame=_scene_rule_frame_fields(memory,frame,0x3E632)
    state=memory.state
    frame=_movement_test(state,frame,state.read(0xFFFF80DA,1),8)
    if frame.status&4:
        frame=_scene_rule_store_word_fields(memory,frame,0xFFFF811C,state.read(0xFFFFF602,2))
        frame=_scene_rule_store_word_fields(memory,frame,0xFFFF811E,state.read(0xFFFFF602,2))
        return _scene_rule_store_word_fields(memory,frame,0xFFFF8120,0,True)
    frame=_movement_compare(state,frame,state.read(0xFFFF80DA,1),2,8)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,2),16)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)|state.read(0xFFFFF604,2),16)
        frame=_scene_rule_store_word_fields(memory,frame,0xFFFF811C,low16(frame.target_x))
        frame=_scene_rule_store_word_fields(memory,frame,0xFFFF811E,state.read(0xFFFFF602,2))
        return _scene_rule_store_word_fields(memory,frame,0xFFFF8120,state.read(0xFFFFF604,2))
    frame=_movement_compare(state,frame,state.read(0xFFFF80DA,1),3,8)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF604,2),16)
    else:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,2),16)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)|state.read(0xFFFFF604,2),16)
    frame=_scene_rule_store_word_fields(memory,frame,0xFFFF811C,low16(frame.target_x))
    frame=_scene_rule_store_word_fields(memory,frame,0xFFFF811E,state.read(0xFFFFF604,2))
    return _scene_rule_store_word_fields(memory,frame,0xFFFF8120,state.read(0xFFFFF602,2))


def exchange_scene_pair_frame_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3E6E8: fourteen original side-specific WORD pairs, one ordered swap rule."""
    from ..high_level_main_flows.business_movement_support import _movement_move
    frame=_scene_rule_frame_fields(memory,frame,0x3E6E8)
    pairs=((0x80DC,0x80DE),(0x80E0,0x80E2),(0x80E4,0x80E6),(0x80E8,0x80EA),
        (0x80EC,0x80EE),(0x80F0,0x80F2),(0x80F4,0x80FA),(0x80F6,0x80FC),
        (0x80F8,0x80FE),(0x8100,0x8102),(0x8104,0x8106),(0x8108,0x810A),
        (0x810C,0x810E),(0x8110,0x8112))
    for primary,secondary in pairs:
        frame=_movement_move(memory.state,frame,'target_x',memory.state.read(0xFFFF0000|primary,2),16)
        frame=_scene_rule_store_word_fields(memory,frame,0xFFFF0000|primary,memory.state.read(0xFFFF0000|secondary,2))
        frame=_scene_rule_store_word_fields(memory,frame,0xFFFF0000|secondary,low16(frame.target_x))
    return frame


def exchange_scene_actor_records_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3E7AE: true128 WORD exchanges and D0 DBRA, both live pointers returned."""
    from ..high_level_main_flows.business_movement_support import _movement_move
    frame=_scene_rule_frame_fields(memory,frame,0x3E7AE)
    frame=_movement_move(memory.state,frame,'target_x',127,16)
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFF816A),candidates=memory.cursor_at(0xFFFF826A))
    while True:
        frame=_movement_move(memory.state,frame,'target_y',frame.roster.word(0),16)
        frame=_scene_rule_store_word_fields(memory,frame,frame.roster.base,frame.candidates.word(0))
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_scene_rule_store_word_fields(memory,frame,frame.candidates.base,low16(frame.target_y))
        frame=first_replace(frame,candidates=frame.candidates.advance(2))
        counter=u16(low16(frame.target_x)-1)
        frame=first_replace(frame,target_x=replace_word(frame.target_x,counter))
        if counter==65535:
            return frame


def _scene_rule_summary_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        secondary: bool) -> FirstDeploymentFrame:
    """Two closed side destinations share the actual ADD then MOVE/MOVE tail."""
    from ..high_level_main_flows.business_movement_support import _movement_move, _movement_add_word
    entry=0x3ECC8 if secondary else 0x3E8A0
    frame=_scene_rule_frame_fields(memory,frame,entry)
    frame=_movement_move(memory.state,frame,'target_x',memory.state.read(0xFFFF8106,2),16)
    frame=_movement_add_word(memory.state,frame,'target_x',memory.state.read(0xFFFF810A,2))
    frame=_scene_rule_store_word_fields(memory,frame,0xFFFF8276 if secondary else 0xFFFF8176,low16(frame.target_x))
    return _scene_rule_store_word_fields(memory,frame,0xFFFF8278 if secondary else 0xFFFF8178,memory.state.read(0xFFFF810E,2))


def refresh_primary_actor_summary_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3E8A0 complete primary total/count update."""
    return _scene_rule_summary_fields(memory,frame,False)

def _phase_legacy_fields(state: SceneState, frame: PhaseFrame,
        entry: Long, needs_stack: bool = False) -> FirstDeploymentFrame:
    """Observe the historical six values; missing D5/D6/X/A7 are not defaults."""
    if type(frame) is not PhaseFrame:
        raise ValueError('same-state PhaseFrame required')
    frame.validate(state)
    if frame.live is not None:
        actual = _scene_controller_legacy_fields(state,phase_controller_return(state,frame))
    else:
        actual = first_replace(FirstDeploymentFrame.unobserved(),
            target_x=frame.video_command,target_y=frame.foreground,unit=frame.mode,
            count=frame.row_count,distance=frame.tile,choice=frame.glyph_tokens)
        if frame.actors is not None:
            actual = first_replace(actual,auxiliary=frame.actors.actor.cursor(),
                scratch=frame.actors.opponent.cursor())
    if needs_stack or (actual.stack_cursor is not None and actual.status is None):
        raise SceneRefreshBoundary(entry,actual,None)
    return actual

def _phase_legacy_projection(state: SceneState, original: PhaseFrame,
        actual: FirstDeploymentFrame) -> PhaseFrame:
    """Project only observations returned by the unique business fields core."""
    for name in ('target_x','target_y','unit','count','distance','choice'):
        if actual.carrier(name) is None:
            raise Boundary('historical phase result lacks an observed retained value')
    if original.live is not None:
        return phase_from_controller(state,_scene_controller_legacy_projection(state,actual))
    actors = original.actors
    if actual.auxiliary is not None and actual.scratch is not None:
        from .contexts_early_phase import BattleActors
        actors = BattleActors(state.table_at(actual.auxiliary.base),state.table_at(actual.scratch.base))
    return replace(original,video_command=actual.target_x,foreground=actual.target_y,
        mode=actual.unit,row_count=actual.count,tile=actual.distance,
        glyph_tokens=actual.choice,actors=actors)

def adjust_scene_scroll_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3D970: two separately observed controller bits and ordered WORD RMWs."""
    memory.frame(frame)
    memory.sync_status(frame)
    value = memory.state.read(0xFFFF811C,1)
    frame = _scene_render_bit(memory,frame,value,1)
    if value & 1:
        memory.sync_status(frame)
        scroll = memory.state.read(0xFFFF8020,2)
        frame = _scene_refresh_flags(memory,frame,scroll,2)
        if scroll:
            frame = _object_adjust_word_fields(memory,frame,0xFFFF8026,2,True)
            frame = _object_adjust_word_fields(memory,frame,0xFFFF8020,2,True)
    memory.sync_status(frame)
    value = memory.state.read(0xFFFF811C,1)
    frame = _scene_render_bit(memory,frame,value,2)
    if value & 2:
        memory.sync_status(frame)
        scroll = memory.state.read(0xFFFF8020,2)
        frame = _scene_render_compare(memory,frame,scroll,144,16)
        if scroll < 144:
            frame = _object_adjust_word_fields(memory,frame,0xFFFF8026,2)
            frame = _object_adjust_word_fields(memory,frame,0xFFFF8020,2)
    return memory.sync_status(frame)

def step_main_scene_phase_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3DCC2/3E8F2: actual BSR then signed instruction-tail JMP, no new JMP slot."""
    from .business_late_phase import (_phase_call_fields,
        adjust_secondary_formation_scene_fields,update_active_battle_controls_fields,
        latch_scene_controller_inputs_fields)
    memory.frame(frame)
    if frame.stack_cursor is None or frame.status is None:
        raise SceneRefreshBoundary(0x3DCC2,frame,None)
    frame = _phase_call_fields(memory,frame,0x3E91C,0x3E8F6)
    memory.sync_status(frame)
    selector = memory.state.read(0xFFFF813C,2)
    frame = _first_word(frame,'target_x',selector)
    frame = _scene_render_asl_word(memory,frame,'target_x',selector,2)
    target = u32(0x3E900 + s16(low16(frame.target_x)))
    if target in (0x3E900,0x3E904,0x3E908,0x3E90C):
        return _allocation_known_fields(memory,frame,target)
    if target in (0x3E910,0x3E914):
        return adjust_secondary_formation_scene_fields(memory,frame)
    if target == 0x3E918:
        return update_active_battle_controls_fields(memory,frame)
    if target == 0x3E91C:
        return latch_scene_controller_inputs_fields(memory,frame)
    raise SceneRefreshBoundary(target,memory.sync_status(frame),None)


def update_pair_allocation_input(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3e62a)
    returned=update_pair_allocation_input_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def exit_pair_allocation(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3e62e)
    returned=exit_pair_allocation_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)






def wait_pair_stage_motion(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3e900)
    returned=wait_pair_stage_motion_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def advance_pair_stage_motion(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3e904)
    returned=advance_pair_stage_motion_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def _prepare_secondary_allocation_panel(state, frame):
    state.set_status_word(0x2700)
    _put(state, '8142', 0)
    _increment(state, '813c')
    frame = _late(state, frame, 'normalize_secondary_squad_size')
    _video_fill(state, 0x50000002, 0x3333, 0xBF)
    state.mmio_write(0xC00004, 4, 0x50000002)
    tokens = replace_word(frame.glyph_tokens, _word(state, '80e2'))
    frame = replace(frame, video_command=replace_word(frame.video_command, 3),
                    foreground=replace_word(frame.foreground, 1), glyph_tokens=tokens)
    frame = _upload_object_officer_name(state, frame)
    _load_panel(state, 0x44C6F)
    frame = _late(state, frame, 'draw_secondary_squad_budget')
    _clear_text(state)
    _script(state, 0x3B320)
    _put(state, '8116', 1)
    frame = _late(state, frame, 'draw_two_prompt_backgrounds')
    state.set_status_word(0x2500)
    return frame


def _finish_allocation_frame(state, frame, secondary):
    frame = _late(state, frame, 'adjust_selected_squad_class_counts')
    return _late(state, frame, 'draw_squad_class_budgets')


def present_pair_stage_summary(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3e90c)
    returned=present_pair_stage_summary_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def confirm_second_pair_allocation(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    actual=_phase_legacy_fields(state,frame,0x3e908)
    returned=confirm_second_pair_allocation_fields(SceneRefreshMemory(state),actual)
    return _phase_legacy_projection(state,frame,returned)



def _confirm_second_pair_allocation(state, frame):
    state.set_status_word(0x2700)
    frame = _allocate_actor_rows(state, '827a', frame)
    frame = _late(state, frame, 'update_secondary_scene_totals')
    _increment(state, '813c')
    _clear_background(state)
    _video_fill(state, 0x60000002, 0x3333, 0xD7F)
    _script(state, 0x3B34A)
    state.set_status_word(0x2500)
    return frame

from ..high_level_main_flows.business_movement_support import _movement_move_long, _movement_multiply_word, _movement_divu_word
from ..high_level_gameplay_flow.business_battle import _presentation_call_fields
from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
from ..high_level_scene_flows.business_scene import _scene_render_arithmetic,_scene_render_push_longs


def _allocation_read_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        address: Long, width: Word):
    memory.sync_status(frame)
    return memory.state.read(address,width)


def _allocation_move_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, value: Long, width: Word=16) -> FirstDeploymentFrame:
    from ..high_level_main_flows.business_movement_support import _movement_move
    if width == 32:
        return _movement_move_long(memory.state, frame, name, value)
    return _movement_move(memory.state, frame, name, value, width)



def _allocation_ram_move_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        name, low: Word, width: Word = 16) -> FirstDeploymentFrame:
    return _allocation_move_fields(memory,frame,name,_allocation_read_fields(memory,frame,0xFFFF0000|low,width//8),width)


def _allocation_store_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, low: Word, value: Long, width: Word=2, clear: bool=False) -> FirstDeploymentFrame:
    from ..high_level_gameplay_flow.business_services import _scene_refresh_emit
    from ..high_level_scene_flows.business_objects import _object_clear_word_fields
    if clear:
        return _object_clear_word_fields(memory, frame, 4294901760 | low)
    return _scene_refresh_emit(memory, frame, 4294901760 | low, width, value)



def _allocation_test_ram_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, low: Word, width: Word=16) -> FirstDeploymentFrame:
    from ..high_level_main_flows.business_movement_support import _movement_test
    return _movement_test(memory.state, frame, _allocation_read_fields(memory, frame, 4294901760 | low, width // 8), width)



def _allocation_compare_ram_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, low: Word, value: Long, width: Word=16) -> FirstDeploymentFrame:
    from ..high_level_main_flows.business_movement_support import _movement_compare
    return _movement_compare(memory.state, frame, _allocation_read_fields(memory, frame, 4294901760 | low, width // 8), value, width)



def _allocation_mask_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        name, mask: Long, width: Word = 16) -> FirstDeploymentFrame:
    value=frame.carrier(name)&((1<<width)-1)&mask
    return _allocation_move_fields(memory,frame,name,value,width)


def _allocation_arithmetic_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        name, value: Long, width: Word = 16, subtract: bool = False) -> FirstDeploymentFrame:
    return _scene_render_arithmetic(memory,frame,name,frame.carrier(name)&((1<<width)-1),value,width,subtract)


def _allocation_adjust_ram_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        low: Word, subtract: bool = False) -> FirstDeploymentFrame:
    return _object_adjust_word_fields(memory,frame,0xFFFF0000|low,1,subtract)


def _allocation_status_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        value: Word) -> FirstDeploymentFrame:
    memory.state.set_status_word(value)
    return first_replace(frame,status=value&31)


def _allocation_dbword_fields(frame: FirstDeploymentFrame, name) -> tuple[FirstDeploymentFrame, bool]:
    value=u16(low16(frame.carrier(name))-1)
    return first_replace(frame,**{name:replace_word(frame.carrier(name),value)}),value==65535


def _allocation_restore_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        names: tuple) -> FirstDeploymentFrame:
    """MOVEM loads actual saved memory, never a Python register snapshot."""
    stack=frame.stack_cursor
    changes={}
    for name in names:
        value=stack.long()
        stack=stack.advance(4)
        changes[name]=memory.cursor_at(value) if name in ('roster','candidates','controller','scan','opponent','scratch','auxiliary') else value
    changes['stack_cursor']=stack
    return first_replace(frame,**changes)


def _allocation_fill_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, command: Long, value: Word, count: Word, reset_increment: bool=False) -> FirstDeploymentFrame:
    """Original D6 fill value/D7 DBRA and A5 VDP port; no fake device RAM."""
    from ..high_level_gameplay_flow.business_services import _scene_refresh_emit
    if reset_increment:
        frame = _scene_refresh_emit(memory, frame, 12582916, 2, 36610)
    frame = _scene_refresh_emit(memory, frame, 12582916, 4, command)
    frame = first_replace(frame, scratch=memory.cursor_at(12582912))
    frame = _allocation_move_fields(memory, frame, 'offset_y', value)
    frame = _allocation_move_fields(memory, frame, 'choice', count)
    while True:
        frame = _scene_refresh_emit(memory, frame, frame.scratch.base, 2, low16(frame.offset_y))
        frame, done = _allocation_dbword_fields(frame, 'choice')
        if done:
            return frame



def _allocation_script_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, source: Long) -> FirstDeploymentFrame:
    from ..high_level_gameplay_flow.business_services import _scene_refresh_emit
    frame = _scene_refresh_emit(memory, frame, 16740364, 2, 40960)
    frame = _scene_refresh_emit(memory, frame, 16740366, 4, source)
    frame = _scene_refresh_emit(memory, frame, 16740372, 2, 3)
    return _scene_refresh_emit(memory, frame, 16740374, 2, 1)



def _allocation_decode_panel_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        source: Long, address: Long, rows: Word, continuation: Long) -> FirstDeploymentFrame:
    """Real 3AAD6 middle-entry setup precedes its genuine caller LONG.

    The whole 3AACE decoder resets D6/8000; this actual entry skips that prefix.
    Do not silently replace it with the whole-entry adapter.
    """
    frame=first_replace(frame,roster=memory.cursor_at(source),candidates=memory.cursor_at(address))
    frame=_allocation_move_fields(memory,frame,'offset_x',0x80,32)
    frame=_allocation_store_fields(memory,frame,0x8000,0x8000)
    frame=_allocation_move_fields(memory,frame,'offset_y',rows)
    return _allocation_call_fields(memory,frame,0x3AAD6,continuation)


def _allocation_leave_prompt_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_allocation_store_fields(memory,frame,0x813A,0,clear=True)
    frame=_allocation_store_fields(memory,frame,0x813C,6)
    frame=_allocation_store_fields(memory,frame,0x814C,0,clear=True)
    return _allocation_call_fields(memory,frame,0x4031C,0x3E1C8)


def _allocation_choice_marker_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    from ..high_level_scene_flows.business_objects import _append_object_sprite_fields
    frame=_allocation_move_fields(memory,frame,'target_x',0x38)
    frame=_allocation_test_ram_fields(memory,frame,0x8142)
    if not frame.status&4:
        frame=_allocation_move_fields(memory,frame,'target_x',0x48)
    frame=_allocation_arithmetic_fields(memory,frame,'target_x',_allocation_read_fields(memory,frame,0xFFFF8020,2))
    frame=first_replace(frame,roster=memory.cursor_at(0x3E28E))
    frame=_allocation_move_fields(memory,frame,'target_y',0x8C)
    frame=_allocation_move_fields(memory,frame,'unit',0x104)
    frame=_allocation_move_fields(memory,frame,'count',0,32)
    frame=_allocation_move_fields(memory,frame,'distance',0x400)
    return _append_object_sprite_fields(memory,frame)


def _allocation_instruction_at_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        y: Word, continuation: Long) -> FirstDeploymentFrame:
    frame=_allocation_ram_move_fields(memory,frame,'target_x',0x8020)
    frame=_allocation_arithmetic_fields(memory,frame,'target_x',0x70)
    frame=_allocation_move_fields(memory,frame,'target_y',y)
    return _allocation_call_fields(memory,frame,0x3E37A,continuation)


def _allocation_xor_choice_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    value=_allocation_read_fields(memory,frame,0xFFFF8142,2)^1
    return _allocation_store_fields(memory,frame,0x8142,value)


def _allocation_link_clear_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    for low in (0x80CA,0x80CC,0x80CE,0x80D0):
        frame=_allocation_store_fields(memory,frame,low,65535)
    return _allocation_move_fields(memory,frame,'target_x',1,32)


def begin_scene_palette_lighten_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    from ..high_level_main_flows.business_movement_support import _movement_compare
    frame = _scene_rule_frame_fields(memory, frame, 240184)
    frame = _allocation_ram_move_fields(memory, frame, 'target_y', 32964)
    if not frame.status & 8:
        frame = _allocation_mask_fields(memory, frame, 'target_y', 65280)
        frame = _movement_compare(memory.state, frame, low16(frame.target_y), 256, 16)
        if frame.status & 4:
            return _allocation_known_fields(memory, frame, 240056)
        frame = _scene_render_push_longs(memory, frame, (frame.target_x,))
        frame = _allocation_call_fields(memory, frame, 240286, 240212)
        frame = _allocation_restore_fields(memory, frame, ('target_x',))
    frame = _allocation_mask_fields(memory, frame, 'target_x', 255)
    frame = _allocation_move_fields(memory, frame, 'target_x', low16(frame.target_x) | 256)
    frame = _allocation_store_fields(memory, frame, 32964, low16(frame.target_x))
    frame = _allocation_store_fields(memory, frame, 32966, 0)
    frame = _allocation_store_fields(memory, frame, 32968, 0)
    frame = _allocation_call_fields(memory, frame, 240248, 240244)
    return _allocation_known_fields(memory, frame, 239992)



def _allocation_palette_copy_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, restore: bool) -> FirstDeploymentFrame:
    from ..high_level_gameplay_flow.business_services import _scene_refresh_emit
    frame = _scene_rule_frame_fields(memory, frame, 240286 if restore else 240248)
    frame = _allocation_move_fields(memory, frame, 'target_y', 31, 32)
    frame = first_replace(frame, roster=memory.cursor_at(4294966144 if restore else 4294966016), candidates=memory.cursor_at(4294966016 if restore else 4294966144))
    while True:
        value = frame.roster.long()
        frame = first_replace(frame, roster=frame.roster.advance(4))
        frame = _scene_refresh_emit(memory, frame, frame.candidates.base, 4, value)
        frame = first_replace(frame, candidates=frame.candidates.advance(4))
        frame, done = _allocation_dbword_fields(frame, 'target_y')
        if done:
            break
    return _allocation_store_fields(memory, frame, 32964, 65535) if restore else frame



def snapshot_scene_palette_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _allocation_palette_copy_fields(memory,frame,False)


def restore_scene_palette_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _allocation_palette_copy_fields(memory,frame,True)


def append_decimal_digit_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    from ..high_level_gameplay_flow.business_services import _scene_refresh_emit
    frame = _scene_rule_frame_fields(memory, frame, 242454)
    frame = _movement_divu_word(memory.state, frame, 'target_x', low16(frame.unit), 242454)
    frame = _scene_refresh_emit(memory, frame, frame.roster.base, 1, low8(frame.target_x))
    frame = first_replace(frame, roster=frame.roster.advance(1))
    frame = _allocation_move_fields(memory, frame, 'target_x', 0)
    return _allocation_move_fields(memory, frame, 'target_x', swap_words(frame.target_x), 32)



def encode_six_decimal_digits_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    from ..high_level_gameplay_flow.business_services import _scene_refresh_emit
    frame = _scene_rule_frame_fields(memory, frame, 242392)
    frame = _allocation_move_fields(memory, frame, 'unit', 0)
    frame = first_replace(frame, roster=memory.cursor_at(4294934528))
    while True:
        frame = _allocation_arithmetic_fields(memory, frame, 'target_x', 100000, 32, True)
        if frame.status & 1:
            break
        frame = _allocation_arithmetic_fields(memory, frame, 'unit', 1)
    frame = _allocation_arithmetic_fields(memory, frame, 'target_x', 100000, 32)
    frame = _scene_refresh_emit(memory, frame, frame.roster.base, 1, low8(frame.unit))
    frame = first_replace(frame, roster=frame.roster.advance(1))
    for divisor, token in ((10000, 242426), (1000, 242434), (100, 242442), (10, 242450)):
        frame = _allocation_move_fields(memory, frame, 'unit', divisor)
        frame = _allocation_call_fields(memory, frame, 242454, token)
    frame = _scene_refresh_emit(memory, frame, frame.roster.base, 1, low8(frame.target_x))
    return first_replace(frame, roster=frame.roster.advance(1))



def append_early_scene_instruction_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    from ..high_level_scene_flows.business_objects import _append_object_sprite_fields
    frame=_scene_rule_frame_fields(memory,frame,0x3E37A)
    frame=first_replace(frame,roster=memory.cursor_at(0x3E396))
    frame=_allocation_move_fields(memory,frame,'unit',0x104)
    frame=_allocation_move_fields(memory,frame,'count',0,32)
    frame=_allocation_move_fields(memory,frame,'distance',0x400)
    return _append_object_sprite_fields(memory, frame)


def paint_scene_number_row_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    from ..high_level_gameplay_flow.business_services import _scene_refresh_emit
    frame = _scene_rule_frame_fields(memory, frame, 255034)
    frame = _scene_render_push_longs(memory, frame, (frame.target_y, frame.target_x))
    frame = _scene_refresh_emit(memory, frame, 12582916, 2, 36610)
    frame = _allocation_call_fields(memory, frame, 242352, 255050)
    frame = _allocation_restore_fields(memory, frame, ('target_x', 'target_y'))
    frame = _allocation_move_fields(memory, frame, 'unit', 5, 32)
    while True:
        frame = _scene_refresh_emit(memory, frame, 12582912, 2, 58461)
        frame, done = _allocation_dbword_fields(frame, 'unit')
        if done:
            return frame



def paint_scene_number_rows_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3E42A)
    frame=_allocation_move_fields(memory,frame,'target_y',7,32)
    while True:
        frame=_allocation_call_fields(memory,frame,0x3E43A,0x3E430)
        frame=_allocation_arithmetic_fields(memory,frame,'target_x',0x80)
        frame,done=_allocation_dbword_fields(frame,'target_y')
        if done:
            return frame


def _allocation_initialize_panel_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        role) -> FirstDeploymentFrame:
    """Three closed original setup paths, with distinct real child tokens."""
    token,script,substate,background_token,portrait={
        'favorable':(0x3DDB8,0x3B43E,4,0x3DE10,True),
        'ordinary':(0x3DE48,0x3B388,1,0x3DEA0,False),
        'other_mode':(0x3DECA,0x3B388,None,0x3DF1C,False),
        'allocation_mode':(0x3E158,0x3B43E,3,0x3E1B0,False)}[role]
    frame=_allocation_status_fields(memory,frame,0x2700)
    frame=_allocation_decode_panel_fields(memory,frame,0x4539C,0xC000,18,token)
    frame=_allocation_store_fields(memory,frame,0x8116,0 if role=='allocation_mode' else 1)
    frame=_allocation_fill_fields(memory,frame,0x60000002,0x3333,0xD7F,True)
    frame=_allocation_script_fields(memory,frame,script)
    if substate is not None:
        frame=_allocation_store_fields(memory,frame,0x813C,substate)
    frame=_allocation_call_fields(memory,frame,0x3EAE2,background_token)
    if portrait:
        frame=_allocation_ram_move_fields(memory,frame,'target_x',0x80E0)
        frame=_allocation_move_fields(memory,frame,'target_y',0x480)
        frame=_allocation_call_fields(memory,frame,0x661D4,0x3DE1E)
    if substate is None:
        frame=_allocation_adjust_ram_fields(memory,frame,0x813C)
    return _allocation_status_fields(memory,frame,0x2500)


def initialize_early_scene_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    from ..high_level_main_flows.business_movement_support import _movement_compare
    frame = _scene_rule_frame_fields(memory, frame, 253176)
    frame = _allocation_test_ram_fields(memory, frame, 32986, 8)
    if not frame.status & 4:
        frame = _allocation_compare_ram_fields(memory, frame, 32986, 3, 8)
        if not frame.status & 4:
            frame = _allocation_compare_ram_fields(memory, frame, 32986, 1, 8)
            return _allocation_initialize_panel_fields(memory, frame, 'other_mode')
    frame = first_replace(frame, roster=memory.cursor_at(4294952704))
    frame = _allocation_move_fields(memory, frame, 'target_y', 0, 32)
    frame = _allocation_ram_move_fields(memory, frame, 'target_x', 32992)
    frame = _allocation_move_fields(memory, frame, 'target_y', frame.roster.byte(low16(frame.target_x)), 8)
    frame = _allocation_mask_fields(memory, frame, 'target_y', 3)
    frame = _allocation_ram_move_fields(memory, frame, 'target_x', 32994)
    frame = _allocation_move_fields(memory, frame, 'target_x', frame.roster.byte(low16(frame.target_x)), 8)
    frame = _allocation_mask_fields(memory, frame, 'target_x', 3)
    frame = _allocation_arithmetic_fields(memory, frame, 'target_y', low8(frame.target_x), 8, True)
    frame = _allocation_arithmetic_fields(memory, frame, 'target_y', 1)
    frame = _movement_compare(memory.state, frame, low16(frame.target_y), 2, 16)
    if not frame.status & 5:
        return _allocation_initialize_panel_fields(memory, frame, 'ordinary')
    for own, extra, other in ((33038, 10, 33036), (33030, 20, 33028)):
        frame = _allocation_ram_move_fields(memory, frame, 'target_x', own)
        frame = _allocation_arithmetic_fields(memory, frame, 'target_x', extra)
        frame = _movement_compare(memory.state, frame, low16(frame.target_x), _allocation_read_fields(memory, frame, 4294901760 | other, 2), 16)
        if frame.status & 1:
            return _allocation_initialize_panel_fields(memory, frame, 'ordinary')
    frame = _allocation_ram_move_fields(memory, frame, 'target_x', 32998)
    frame = _movement_compare(memory.state, frame, low16(frame.target_x), _allocation_read_fields(memory, frame, 4294934756, 2), 16)
    if not frame.status & 1:
        return _allocation_initialize_panel_fields(memory, frame, 'ordinary')
    frame = _allocation_call_fields(memory, frame, 243490, 253324)
    frame = _allocation_mask_fields(memory, frame, 'target_x', 3)
    return _allocation_initialize_panel_fields(memory, frame, 'favorable' if frame.status & 4 else 'ordinary')



def _allocation_contested_roll_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> tuple[FirstDeploymentFrame, bool]:
    """Original byte strength rules, MULU/DIVU and rejection-sampled percentage."""
    from ..high_level_main_flows.business_movement_support import _movement_compare
    frame = _allocation_move_fields(memory, frame, 'target_y', 0, 32)
    frame = _allocation_move_fields(memory, frame, 'unit', 0, 32)
    frame = first_replace(frame, roster=memory.cursor_at(4294952704))
    frame = _allocation_ram_move_fields(memory, frame, 'target_x', 32992)
    frame = _allocation_move_fields(memory, frame, 'target_x', frame.roster.byte(low16(frame.target_x)), 8)
    frame = _allocation_mask_fields(memory, frame, 'target_x', 3)
    frame = _allocation_move_fields(memory, frame, 'target_y', 5, 32)
    frame = _allocation_arithmetic_fields(memory, frame, 'target_y', low8(frame.target_x), 8, True)
    frame = _allocation_ram_move_fields(memory, frame, 'target_x', 32994)
    frame = _allocation_move_fields(memory, frame, 'target_x', frame.roster.byte(low16(frame.target_x)), 8)
    frame = _allocation_move_fields(memory, frame, 'unit', 5, 32)
    frame = _allocation_arithmetic_fields(memory, frame, 'unit', low8(frame.target_x), 8, True)
    frame = _allocation_ram_move_fields(memory, frame, 'target_x', 33028)
    frame = _movement_multiply_word(memory.state, frame, 'target_y', low16(frame.target_x))
    frame = _movement_multiply_word(memory.state, frame, 'target_y', 100)
    frame = _allocation_call_fields(memory, frame, 243490, 253836)
    frame = _allocation_mask_fields(memory, frame, 'target_x', 31)
    frame = _allocation_arithmetic_fields(memory, frame, 'target_x', 20)
    frame = _allocation_arithmetic_fields(memory, frame, 'target_x', _allocation_read_fields(memory, frame, 4294934790, 2))
    frame = _movement_multiply_word(memory.state, frame, 'unit', low16(frame.target_x))
    frame = _movement_divu_word(memory.state, frame, 'target_y', low16(frame.unit), 253850)
    frame = _movement_compare(memory.state, frame, low16(frame.target_y), 100, 16)
    if not frame.status & 5:
        return (frame, True)
    while True:
        frame = _allocation_call_fields(memory, frame, 243490, 253864)
        frame = _allocation_mask_fields(memory, frame, 'target_x', 127)
        frame = _movement_compare(memory.state, frame, low16(frame.target_x), 100, 16)
        if frame.status & 5:
            break
    frame = _movement_compare(memory.state, frame, low16(frame.target_x), low16(frame.target_y), 16)
    if not frame.status & 5:
        return (frame, False)
    frame = _allocation_call_fields(memory, frame, 243490, 253884)
    frame = _allocation_ram_move_fields(memory, frame, 'target_y', 61394)
    frame = first_replace(frame, roster=memory.cursor_at(254082))
    frame = _allocation_mask_fields(memory, frame, 'target_x', frame.roster.byte(low16(frame.target_y)), 8)
    return (frame, bool(frame.status & 4))



def _allocation_show_choice_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, accepted: bool) -> FirstDeploymentFrame:
    from ..high_level_main_flows.business_movement_support import _movement_compare
    from ..high_level_gameplay_flow.business_services import _scene_refresh_emit
    frame = _allocation_store_fields(memory, frame, 33090, 0 if accepted else 1, clear=accepted)
    frame = _allocation_fill_fields(memory, frame, 1073741827, 1024, 1215)
    frame = _allocation_ram_move_fields(memory, frame, 'target_x', 32992)
    frame = _allocation_move_fields(memory, frame, 'target_y', 1152)
    frame = _allocation_call_fields(memory, frame, 418260, 253950 if accepted else 254136)
    if accepted:
        frame = _allocation_move_fields(memory, frame, 'target_x', 49954)
        frame = _allocation_call_fields(memory, frame, 255018, 253958)
    frame = _allocation_fill_fields(memory, frame, 1610612738, 13107, 3455, True)
    frame = _scene_refresh_emit(memory, frame, 16740364, 2, 40960)
    frame = _scene_refresh_emit(memory, frame, 16740372, 2, 3)
    frame = _scene_refresh_emit(memory, frame, 16740374, 2, 1)
    frame = _allocation_adjust_ram_fields(memory, frame, 33084)
    frame = _scene_refresh_emit(memory, frame, 16740366, 4, 242680 if accepted else 242620)
    frame = first_replace(frame, roster=memory.cursor_at(4294952704))
    frame = _allocation_ram_move_fields(memory, frame, 'target_x', 32994)
    frame = _allocation_move_fields(memory, frame, 'target_y', frame.roster.byte(low16(frame.target_x)), 8)
    frame = _allocation_mask_fields(memory, frame, 'target_y', 3)
    frame = _allocation_ram_move_fields(memory, frame, 'target_x', 32992)
    frame = _allocation_move_fields(memory, frame, 'target_x', frame.roster.byte(low16(frame.target_x)), 8)
    frame = _allocation_mask_fields(memory, frame, 'target_x' if accepted else 'target_y', 3)
    frame = _movement_compare(memory.state, frame, low8(frame.target_y), low8(frame.target_x), 8)
    if not frame.status & 1:
        frame = _scene_refresh_emit(memory, frame, 16740366, 4, 242602 if accepted else 242654)
    return _allocation_status_fields(memory, frame, 9472)



def process_early_scene_choice_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3DCFC)
    frame,pressed=_scene_rule_input_bit_fields(memory,frame,0xFFFF811F,5)
    if not pressed:
        return draw_early_scene_choice_fields(memory,frame)
    frame=_allocation_move_fields(memory,frame,'target_x',0xAC)
    frame=_allocation_call_fields(memory,frame,0x808A,0x3DF3A)
    frame=_allocation_test_ram_fields(memory,frame,0x8142)
    if not frame.status&4:
        return _allocation_leave_prompt_fields(memory,frame)
    frame=_allocation_compare_ram_fields(memory,frame,0x80DA,1,8)
    if not frame.status&4:
        frame=_allocation_compare_ram_fields(memory,frame,0x80DA,2,8)
    if frame.status&4:
        return _allocation_initialize_panel_fields(memory,frame,'allocation_mode')
    frame=_allocation_status_fields(memory,frame,0x2700)
    frame,accepted=_allocation_contested_roll_fields(memory,frame)
    return _allocation_show_choice_fields(memory,frame,accepted)


def draw_early_scene_choice_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3E254)
    frame=_allocation_ram_move_fields(memory,frame,'target_x',0x811F,8)
    frame=_allocation_mask_fields(memory,frame,'target_x',3)
    if not frame.status&4:
        frame=_allocation_xor_choice_fields(memory,frame)
    return _allocation_choice_marker_fields(memory,frame)


def present_early_scene_prompt_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3DD00)
    frame,pressed=_scene_rule_input_bit_fields(memory,frame,0xFFFF811F,5)
    if pressed:
        frame=_allocation_test_ram_fields(memory,frame,0x8142)
        if not frame.status&4:
            return _allocation_leave_prompt_fields(memory,frame)
        frame=_allocation_call_fields(memory,frame,0x3F0DE,0x3E1E0)
        frame=_allocation_store_fields(memory,frame,0x813A,8)
        frame=_allocation_store_fields(memory,frame,0x813C,5)
    frame=_allocation_instruction_at_fields(memory,frame,0xA0,0x3E1FC)
    frame=_allocation_move_fields(memory,frame,'target_x',0xC322)
    return _allocation_call_fields(memory,frame,0x3E42A,0x3E204)


def finish_early_scene_prompt_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3DD04)
    frame=_allocation_test_ram_fields(memory,frame,0x80DA,8)
    special=bool(frame.status&4)
    if not special:
        frame=_allocation_compare_ram_fields(memory,frame,0x80DA,3,8)
        special=bool(frame.status&4)
    if special:
        frame=_allocation_instruction_at_fields(memory,frame,0x100,0x3E22E)
        frame=_allocation_move_fields(memory,frame,'target_x',0xC33A)
        frame=_allocation_call_fields(memory,frame,0x3E42A,0x3E236)
    else:
        frame=_allocation_store_fields(memory,frame,0x811E,_allocation_read_fields(memory,frame,0xFFFF8120,2))
    frame,pressed=_scene_rule_input_bit_fields(memory,frame,0xFFFF811F,5)
    if pressed:
        frame=_allocation_test_ram_fields(memory,frame,0x8142)
        if not frame.status&4:
            return _allocation_leave_prompt_fields(memory,frame)
        frame=_allocation_call_fields(memory,frame,0x3F0DE,0x3E24C)
        return _allocation_store_fields(memory,frame,0x813C,6)
    return draw_early_scene_choice_fields(memory,frame)


def wait_early_scene_choice_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3DD08)
    frame=_allocation_instruction_at_fields(memory,frame,0x100,0x3E2A8)
    frame=_allocation_move_fields(memory,frame,'target_x',0xC33A)
    frame=_allocation_call_fields(memory,frame,0x3E42A,0x3E2B0)
    frame=_allocation_call_fields(memory,frame,0x3E254,0x3E2B4)
    frame=_allocation_adjust_ram_fields(memory,frame,0x8144)
    frame=_allocation_compare_ram_fields(memory,frame,0x8144,64)
    if frame.status&1:
        return frame
    frame=_allocation_status_fields(memory,frame,0x2700)
    frame=_allocation_fill_fields(memory,frame,0x60000002,0x3333,0xD7F,True)
    frame=_allocation_script_fields(memory,frame,0x3B41E)
    frame=_allocation_store_fields(memory,frame,0x813C,3)
    return _allocation_status_fields(memory,frame,0x2500)


def _allocation_finish_fade_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame,finished=_scene_rule_input_bit_fields(memory,frame,0xFFFF80C4,7)
    if finished:
        frame=_allocation_store_fields(memory,frame,0x813A,3)
        frame=_allocation_store_fields(memory,frame,0x813C,3)
    return frame


def finish_early_scene_fade_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3DD0C)
    frame=_allocation_instruction_at_fields(memory,frame,0xA0,0x3E32A)
    return _allocation_finish_fade_fields(memory,frame)


def finish_alternate_scene_fade_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3DD10)
    frame=_allocation_compare_ram_fields(memory,frame,0x80DA,1,8)
    if not frame.status&4:
        frame=_allocation_compare_ram_fields(memory,frame,0x80DA,2,8)
        if not frame.status&4:
            frame=_allocation_instruction_at_fields(memory,frame,0x100,0x3E362)
    return _allocation_finish_fade_fields(memory,frame)


def wait_exchange_scene_transition_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3E46C)
    frame=_allocation_adjust_ram_fields(memory,frame,0x8142)
    frame=_allocation_compare_ram_fields(memory,frame,0x8142,32)
    if frame.status&1:
        return frame
    frame=_allocation_status_fields(memory,frame,0x2700)
    frame=_allocation_store_fields(memory,frame,0x8142,0,clear=True)
    frame=_allocation_adjust_ram_fields(memory,frame,0x813C)
    frame=_allocation_decode_panel_fields(memory,frame,0x4583F,0xC000,18,0x3E4B2)
    frame=_allocation_fill_fields(memory,frame,0x60000002,0x3333,0xD7F,True)
    frame=_allocation_script_fields(memory,frame,0x3B4C6)
    frame=_allocation_store_fields(memory,frame,0x8116,1)
    frame=_allocation_call_fields(memory,frame,0x3EAE2,0x3E504)
    return _allocation_status_fields(memory,frame,0x2500)


def process_exchange_scene_choice_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    from ..high_level_gameplay_flow.business_services import _scene_refresh_emit
    frame = _scene_rule_frame_fields(memory, frame, 255088)
    frame, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934813, 5)
    if not pressed:
        frame = _allocation_ram_move_fields(memory, frame, 'target_x', 33053, 8)
        frame = _allocation_mask_fields(memory, frame, 'target_x', 3)
        if not frame.status & 4:
            frame = _allocation_xor_choice_fields(memory, frame)
        return _allocation_choice_marker_fields(memory, frame)
    frame = _allocation_move_fields(memory, frame, 'target_x', 172)
    frame = _allocation_call_fields(memory, frame, 32906, 255262)
    frame = _allocation_test_ram_fields(memory, frame, 33090)
    if frame.status & 4:
        frame = _allocation_store_fields(memory, frame, 33090, 0, clear=True)
        frame = _allocation_store_fields(memory, frame, 33082, 7)
        frame = _allocation_store_fields(memory, frame, 33084, 0, clear=True)
        frame = _allocation_store_fields(memory, frame, 33100, 0, clear=True)
        frame = _allocation_call_fields(memory, frame, 262940, 255292)
        return _allocation_store_fields(memory, frame, 33802, 0, clear=True)
    frame = _allocation_status_fields(memory, frame, 9984)
    frame = _allocation_compare_ram_fields(memory, frame, 32986, 0, 8)
    if not frame.status & 4:
        frame = _allocation_compare_ram_fields(memory, frame, 32986, 3, 8)
        if not frame.status & 4:
            frame = _allocation_call_fields(memory, frame, 268312, 255344)
    frame = _allocation_call_fields(memory, frame, 255720, 255348)
    frame = _allocation_call_fields(memory, frame, 255918, 255352)
    frame = _allocation_call_fields(memory, frame, 268312, 255356)
    frame = first_replace(frame, roster=memory.cursor_at(4294934890))
    frame = _allocation_move_fields(memory, frame, 'target_y', 15)
    while True:
        frame = _allocation_move_fields(memory, frame, 'target_x', 352)
        frame = _allocation_arithmetic_fields(memory, frame, 'target_x', frame.roster.word(2), subtract=True)
        frame = _scene_refresh_emit(memory, frame, frame.roster.base + 2, 2, low16(frame.target_x))
        frame = _scene_refresh_emit(memory, frame, frame.roster.base + 6, 2, 1)
        frame = _scene_refresh_emit(memory, frame, frame.roster.base + 8, 2, 1)
        frame = first_replace(frame, roster=frame.roster.advance(16))
        frame, done = _allocation_dbword_fields(frame, 'target_y')
        if done:
            break
    frame = _allocation_call_fields(memory, frame, 255720, 255400)
    frame = _allocation_call_fields(memory, frame, 255918, 255404)
    frame = _allocation_call_fields(memory, frame, 262940, 255408)
    frame = _allocation_store_fields(memory, frame, 33802, 1)
    frame = _allocation_store_fields(memory, frame, 33090, 0, clear=True)
    for low, value in ((32800, 0), (32804, 0), (32832, 33280), (32826, 33280)):
        frame = _allocation_store_fields(memory, frame, low, value)
    frame = _allocation_adjust_ram_fields(memory, frame, 33084)
    return _allocation_status_fields(memory, frame, 9472)



def finish_exchange_scene_transition_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3E474)
    frame=_allocation_compare_ram_fields(memory,frame,0x8020,144)
    if frame.status&1:
        return frame
    frame=_allocation_store_fields(memory,frame,0x8040,0)
    frame=_allocation_store_fields(memory,frame,0x803A,0)
    frame=_allocation_adjust_ram_fields(memory,frame,0x8142)
    frame=_allocation_compare_ram_fields(memory,frame,0x8142,32)
    if not frame.status&1:
        frame=_allocation_store_fields(memory,frame,0x8142,0,clear=True)
        frame=_allocation_store_fields(memory,frame,0x813A,8)
        frame=_allocation_store_fields(memory,frame,0x813C,0,clear=True)
        frame=_allocation_store_fields(memory,frame,0x814C,0,clear=True)
    return frame


def _allocation_exit_pair_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    for low in (0x813A,0x813C,0x814C):
        frame=_allocation_store_fields(memory,frame,low,0,clear=True)
    frame=_allocation_call_fields(memory,frame,0x4031C,0x3E8E0)
    frame=_allocation_call_fields(memory,frame,0x3E6E8,0x3E8E4)
    for low in (0x8142,0x8144,0x8146):
        frame=_allocation_store_fields(memory,frame,low,0,clear=True)
    return frame


def _allocation_finish_class_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_allocation_call_fields(memory,frame,0x3F532,0x3ECC2)
    return _allocation_call_fields(memory,frame,0x3F93E,0x3ECC6)


def _allocation_roster_shares_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, secondary: bool) -> FirstDeploymentFrame:
    """Fifteen original percentage/remainder rows, no invented distribution cap."""
    from ..high_level_main_flows.business_movement_support import _movement_test
    from ..high_level_gameplay_flow.business_services import _scene_refresh_emit
    frame = _allocation_ram_move_fields(memory, frame, 'target_x', 33030)
    frame = _allocation_ram_move_fields(memory, frame, 'target_y', 33026)
    frame = _movement_multiply_word(memory.state, frame, 'target_y', low16(frame.target_x))
    frame = _movement_divu_word(memory.state, frame, 'target_y', 100, 257060 if secondary else 256010)
    frame = _allocation_move_fields(memory, frame, 'target_x', 14)
    frame = _allocation_ram_move_fields(memory, frame, 'unit', 33010)
    frame = first_replace(frame, auxiliary=memory.cursor_at(4294935162 if secondary else 4294934906))
    while True:
        frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base + 12, 2, low16(frame.target_y))
        frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base + 14, 2, _allocation_read_fields(memory, frame, 4294934766, 2))
        frame = _movement_test(memory.state, frame, low16(frame.unit), 16)
        if not frame.status & 4:
            frame = _allocation_arithmetic_fields(memory, frame, 'unit', 1, subtract=True)
            frame = _object_adjust_word_fields(memory, frame, frame.auxiliary.base + 14, 1)
        frame = first_replace(frame, auxiliary=frame.auxiliary.advance(16))
        frame, done = _allocation_dbword_fields(frame, 'target_x')
        if done:
            return frame



def _allocation_confirm_shares_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        secondary: bool) -> FirstDeploymentFrame:
    if not secondary:
        frame=_allocation_adjust_ram_fields(memory,frame,0x813C)
    frame=_allocation_status_fields(memory,frame,0x2700)
    frame=_allocation_roster_shares_fields(memory,frame,secondary)
    frame=_allocation_call_fields(memory,frame,0x3ECC8 if secondary else 0x3E8A0,0x3EC56 if secondary else 0x3E83C)
    if secondary:
        frame=_allocation_adjust_ram_fields(memory,frame,0x813C)
    frame=_allocation_fill_fields(memory,frame,0x40000003,0x400,0x4BF)
    frame=_allocation_fill_fields(memory,frame,0x60000002,0x3333,0xD7F)
    frame=_allocation_script_fields(memory,frame,0x3B34A)
    return _allocation_status_fields(memory,frame,0x2500)


def _allocation_check_commit_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, secondary: bool) -> FirstDeploymentFrame:
    from ..high_level_main_flows.business_movement_support import _movement_compare
    frame, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934815, 5)
    if not pressed:
        return _allocation_finish_class_fields(memory, frame)
    frame = _allocation_move_fields(memory, frame, 'target_x', 172)
    frame = _allocation_call_fields(memory, frame, 32906, 257016 if secondary else 255962)
    frame = _allocation_compare_ram_fields(memory, frame, 33092, 2)
    if not frame.status & 4:
        return _allocation_finish_class_fields(memory, frame)
    frame = _allocation_ram_move_fields(memory, frame, 'target_x', 33018)
    frame = _allocation_arithmetic_fields(memory, frame, 'target_x', _allocation_read_fields(memory, frame, 4294934780, 2))
    frame = _allocation_arithmetic_fields(memory, frame, 'target_x', _allocation_read_fields(memory, frame, 4294934782, 2))
    frame = _movement_compare(memory.state, frame, low16(frame.target_x), _allocation_read_fields(memory, frame, 4294934762, 2), 16)
    if not frame.status & 4:
        return _allocation_finish_class_fields(memory, frame)
    return _allocation_confirm_shares_fields(memory, frame, secondary)



def _allocation_prepare_secondary_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    from ..high_level_gameplay_flow.business_services import _scene_refresh_emit
    frame = _allocation_status_fields(memory, frame, 9984)
    frame = _allocation_store_fields(memory, frame, 33090, 0, clear=True)
    frame = _allocation_adjust_ram_fields(memory, frame, 33084)
    frame = _allocation_call_fields(memory, frame, 259166, 256556)
    frame = _allocation_fill_fields(memory, frame, 1342177282, 13107, 191)
    frame = _scene_refresh_emit(memory, frame, 12582916, 4, 1342177282)
    frame = _allocation_ram_move_fields(memory, frame, 'choice', 32994)
    frame = _allocation_move_fields(memory, frame, 'target_x', 3)
    frame = _allocation_move_fields(memory, frame, 'target_y', 1)
    frame = _allocation_call_fields(memory, frame, 262850, 256614)
    frame = _allocation_decode_panel_fields(memory, frame, 281711, 49152, 18, 256646)
    frame = _allocation_call_fields(memory, frame, 260342, 256650)
    frame = _allocation_fill_fields(memory, frame, 1610612738, 13107, 3455, True)
    frame = _allocation_script_fields(memory, frame, 242464)
    frame = _allocation_store_fields(memory, frame, 33046, 1)
    frame = _allocation_call_fields(memory, frame, 256738, 256732)
    return _allocation_status_fields(memory, frame, 9472)



def process_pair_phase_counter_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3E622)
    frame=_allocation_compare_ram_fields(memory,frame,0x80DA,1,8)
    if not frame.status&4:
        frame=_allocation_compare_ram_fields(memory,frame,0x80DA,2,8)
        if not frame.status&4:
            frame=_allocation_store_fields(memory,frame,0x813A,0,clear=True)
            return _allocation_store_fields(memory,frame,0x813C,0,clear=True)
    frame=_allocation_adjust_ram_fields(memory,frame,0x8142)
    frame=_allocation_compare_ram_fields(memory,frame,0x8142,64)
    if frame.status&1:
        return frame
    frame=_allocation_call_fields(memory,frame,0x3E6E8,0x3E6D0)
    frame=_allocation_test_ram_fields(memory,frame,0x80E6)
    if not frame.status&4:
        return _allocation_prepare_secondary_fields(memory,frame)
    frame=_allocation_call_fields(memory,frame,0x3E8A0,0x3E6DA)
    frame=_allocation_call_fields(memory,frame,0x3F6EE,0x3E6DE)
    return _allocation_exit_pair_fields(memory,frame)


def confirm_pair_allocation_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _scene_rule_frame_fields(memory, frame, 255526)
    frame = _allocation_call_fields(memory, frame, 259352, 256808)
    frame = _allocation_call_fields(memory, frame, 259166, 256812)
    frame = _allocation_call_fields(memory, frame, 260342, 256816)
    frame, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934815, 5)
    if not pressed:
        return frame
    frame = _allocation_move_fields(memory, frame, 'target_x', 172)
    frame = _allocation_call_fields(memory, frame, 32906, 256834)
    frame = _allocation_adjust_ram_fields(memory, frame, 33084)
    frame = _allocation_store_fields(memory, frame, 33092, 0, clear=True)
    frame = _allocation_compare_ram_fields(memory, frame, 32987, 3, 8)
    if frame.status & 4:
        frame = _allocation_store_fields(memory, frame, 33018, 0, clear=True)
        frame = _allocation_store_fields(memory, frame, 33020, _allocation_read_fields(memory, frame, 4294934762, 2))
        frame = _allocation_store_fields(memory, frame, 33022, 0, clear=True)
        frame = _allocation_compare_ram_fields(memory, frame, 33082, 7)
        return _allocation_confirm_shares_fields(memory, frame, not bool(frame.status & 4))
    frame = _allocation_status_fields(memory, frame, 9984)
    frame = _allocation_decode_panel_fields(memory, frame, 282054, 49152, 18, 256914)
    frame = _allocation_call_fields(memory, frame, 260414, 256918)
    frame = _allocation_fill_fields(memory, frame, 1610612738, 13107, 3455, True)
    frame = _allocation_script_fields(memory, frame, 242486)
    return _allocation_status_fields(memory, frame, 9472)


def update_pair_allocation_input_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _scene_rule_frame_fields(memory, frame, 255530)
    return _allocation_check_commit_fields(memory, frame, False)


def exit_pair_allocation_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _scene_rule_frame_fields(memory, frame, 255534)
    frame = _allocation_call_fields(memory, frame, 259778, 256184)
    frame = _allocation_ram_move_fields(memory, frame, 'target_x', 33055, 8)
    frame = _allocation_mask_fields(memory, frame, 'target_x', 12)
    if not frame.status & 4:
        frame = _allocation_call_fields(memory, frame, 262940, 256198)
    return frame


def wait_pair_stage_motion_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3E900)
    frame=_allocation_adjust_ram_fields(memory,frame,0x8142)
    frame=_allocation_compare_ram_fields(memory,frame,0x8142,64)
    if frame.status&1:
        return frame
    frame=_allocation_store_fields(memory,frame,0x8142,0,clear=True)
    for low,value in ((0x8020,0),(0x8024,0),(0x8040,0x8200),(0x803A,0x8200)):
        frame=_allocation_store_fields(memory,frame,low,value)
    return _allocation_adjust_ram_fields(memory,frame,0x813C)


def advance_pair_stage_motion_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3E904)
    frame=_allocation_compare_ram_fields(memory,frame,0x8020,144)
    if frame.status&1:
        return frame
    frame=_allocation_store_fields(memory,frame,0x8040,0)
    frame=_allocation_store_fields(memory,frame,0x803A,0)
    frame=_allocation_adjust_ram_fields(memory,frame,0x8142)
    frame=_allocation_compare_ram_fields(memory,frame,0x8142,32)
    if frame.status&1:
        return frame
    frame=_allocation_test_ram_fields(memory,frame,0x80E6)
    if not frame.status&4:
        return _allocation_prepare_secondary_fields(memory,frame)
    for low in (0x80EA,0x80EE,0x80F2,0x80FA,0x80FC,0x80FE,0x8142):
        frame=_allocation_store_fields(memory,frame,low,0,clear=True)
    frame=_allocation_call_fields(memory,frame,0x3ECC8,0x3EA04)
    frame=_allocation_call_fields(memory,frame,0x3F648,0x3EA08)
    frame=_allocation_store_fields(memory,frame,0x813A,8)
    frame=_allocation_store_fields(memory,frame,0x813C,0,clear=True)
    frame=_allocation_store_fields(memory,frame,0x814C,0,clear=True)
    return _allocation_call_fields(memory,frame,0x4031C,0x3EA1A)


def confirm_second_pair_allocation_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _scene_rule_frame_fields(memory, frame, 256264)
    frame = _allocation_call_fields(memory, frame, 259352, 256808)
    frame = _allocation_call_fields(memory, frame, 259166, 256812)
    frame = _allocation_call_fields(memory, frame, 260342, 256816)
    frame, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934815, 5)
    if not pressed:
        return frame
    frame = _allocation_move_fields(memory, frame, 'target_x', 172)
    frame = _allocation_call_fields(memory, frame, 32906, 256834)
    frame = _allocation_adjust_ram_fields(memory, frame, 33084)
    frame = _allocation_store_fields(memory, frame, 33092, 0, clear=True)
    frame = _allocation_compare_ram_fields(memory, frame, 32987, 3, 8)
    if frame.status & 4:
        frame = _allocation_store_fields(memory, frame, 33018, 0, clear=True)
        frame = _allocation_store_fields(memory, frame, 33020, _allocation_read_fields(memory, frame, 4294934762, 2))
        frame = _allocation_store_fields(memory, frame, 33022, 0, clear=True)
        frame = _allocation_compare_ram_fields(memory, frame, 33082, 7)
        return _allocation_confirm_shares_fields(memory, frame, not bool(frame.status & 4))
    frame = _allocation_status_fields(memory, frame, 9984)
    frame = _allocation_decode_panel_fields(memory, frame, 282054, 49152, 18, 256914)
    frame = _allocation_call_fields(memory, frame, 260414, 256918)
    frame = _allocation_fill_fields(memory, frame, 1610612738, 13107, 3455, True)
    frame = _allocation_script_fields(memory, frame, 242486)
    return _allocation_status_fields(memory, frame, 9472)


def present_pair_stage_summary_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _scene_rule_frame_fields(memory, frame, 256268)
    return _allocation_check_commit_fields(memory, frame, True)


def _allocation_phase_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        entry: Long, base: Long, gather: Long, continuation: Long) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,entry)
    frame=_allocation_call_fields(memory,frame,gather,continuation)
    frame=_allocation_ram_move_fields(memory,frame,'target_x',0x813C)
    frame=_scene_render_asl_word(memory,frame,'target_x',low16(frame.target_x),2)
    # These are executable BRA cells: JMP neither reads a WORD nor pushes a slot.
    return _allocation_known_fields(memory,frame,u32(base+s16(low16(frame.target_x))))


def step_result_scene_phase_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _allocation_phase_fields(memory,frame,0x3DCC6,0x3EF86,0x3E91C,0x3EF7C)


def step_confirmation_scene_phase_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _allocation_phase_fields(memory,frame,0x3DCCA,0x3F030,0x3E91C,0x3F026)


def step_transfer_scene_phase_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _allocation_phase_fields(memory,frame,0x3DCCE,0x3F062,0x3E91C,0x3F058)


def step_primary_detail_scene_phase_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _allocation_phase_fields(memory,frame,0x3DCD2,0x3F1EA,0x3E91C,0x3F1E0)


def step_secondary_detail_scene_phase_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _allocation_phase_fields(memory,frame,0x3DCD6,0x3F29C,0x3E91C,0x3F292)


def step_summary_scene_phase_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _allocation_phase_fields(memory,frame,0x3DCDA,0x3F34E,0x3E91C,0x3F344)


def step_pair_transition_scene_phase_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _allocation_phase_fields(memory,frame,0x3DCDE,0x3E622,0x3E632,0x3E618)


def step_initial_scene_phase_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _allocation_phase_fields(memory,frame,0x3DCE2,0x3DCF8,0x3E91C,0x3DCEE)


def step_exchange_scene_phase_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _allocation_phase_fields(memory,frame,0x3DCE6,0x3E46C,0x3E632,0x3E462)


def _allocation_call_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        target: Long, continuation: Long) -> FirstDeploymentFrame:
    """Only original direct calls: one physical LONG write/read/pop per child."""
    if (target,continuation) not in ((32906, 253754), (32906, 255262), (32906, 255962), (32906, 256834), (32906, 257016), (240184, 258304), (240184, 258700), (240184, 258878), (240184, 259164), (240248, 240244), (240286, 240212), (240342, 253368), (240342, 253512), (240342, 253642), (240342, 254296), (240342, 255154), (240342, 256646), (240342, 256770), (240342, 256802), (240342, 256914), (242352, 255050), (242352, 260880), (242352, 260914), (242352, 260954), (242352, 260984), (242352, 261020), (242352, 261060), (242352, 261090), (242352, 261126), (242352, 261166), (242352, 261196), (242352, 261232), (242352, 261270), (242352, 261530), (242352, 261564), (242352, 261604), (242352, 261630), (242352, 261666), (242352, 261706), (242352, 261982), (242352, 262010), (242392, 260352), (242392, 260376), (242392, 260400), (242392, 260424), (242392, 260448), (242392, 260486), (242392, 260526), (242392, 260668), (242392, 260722), (242392, 260776), (242392, 260828), (242392, 261424), (242392, 261478), (242392, 261736), (242392, 261760), (242392, 261784), (242392, 261808), (242392, 261832), (242392, 261856), (242392, 261902), (242392, 261948), (242454, 242426), (242454, 242434), (242454, 242442), (242454, 242450), (243490, 253324), (243490, 253836), (243490, 253864), (243490, 253884), (254548, 254644), (254842, 254460), (254842, 254510), (254842, 254632), (254842, 254762), (254842, 254818), (255018, 253958), (255018, 254468), (255018, 254518), (255018, 254640), (255034, 255024), (255538, 255074), (255538, 255512), (255720, 255348), (255720, 255400), (255720, 255696), (255720, 256228), (255918, 255352), (255918, 255404), (256160, 255706), (256160, 256060), (256284, 253166), (256284, 257916), (256284, 258086), (256284, 258136), (256284, 258528), (256284, 258706), (256284, 258884), (256738, 253456), (256738, 253600), (256738, 253724), (256738, 254384), (256738, 255236), (256738, 256732), (256738, 258014), (256738, 258242), (256738, 258634), (256738, 258812), (256738, 259000), (257224, 256516), (257224, 257110), (258270, 254432), (258270, 254540), (259166, 256556), (259166, 256812), (259352, 256808), (259378, 257218), (259656, 256520), (259778, 256184), (259822, 255710), (259936, 258046), (260316, 258274), (260316, 258666), (260316, 258848), (260316, 259134), (260342, 256650), (260342, 256816), (260414, 256918), (260414, 257222), (260550, 258050), (260658, 260610), (261288, 260928), (261288, 260958), (261288, 261034), (261288, 261064), (261288, 261140), (261288, 261170), (261288, 261246), (261288, 261274), (261288, 261578), (261288, 261608), (261288, 261680), (261288, 261710), (261304, 260936), (261304, 260966), (261304, 261042), (261304, 261072), (261304, 261148), (261304, 261178), (261304, 261252), (261304, 261280), (261304, 261586), (261304, 261616), (261304, 261688), (261304, 261718), (261414, 261380), (261962, 260468), (261962, 260508), (261998, 260366), (261998, 260390), (261998, 260438), (261998, 260476), (261998, 260516), (261998, 260682), (261998, 260736), (261998, 260790), (261998, 260842), (261998, 261438), (261998, 261492), (261998, 261750), (261998, 261774), (261998, 261798), (261998, 261822), (261998, 261846), (261998, 261870), (261998, 261916), (262850, 256614), (262940, 254408), (262940, 255292), (262940, 255408), (262940, 256198), (262940, 256224), (262940, 256538), (262940, 258064), (262940, 258114), (268312, 255344), (268312, 255356), (418260, 253470), (418260, 253950), (418260, 254136)):
        raise ValueError('actual C52 target and caller return token required')
    def child(actual_memory,entered):
        return _allocation_known_fields(memory,entered,target,continuation)
    return _presentation_call_fields(BattlePresentationMemory(memory.state),frame,continuation,child)


def _allocation_known_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long | None=None) -> FirstDeploymentFrame:
    """Named business dispatch; unknown children/tails remain a real boundary."""
    if target == 32906:
        from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields
        return enqueue_sound_command_fields(memory, frame)
    if target == 239522:
        from ..high_level_scene_flows.business_scene import append_unclipped_scene_sprites_fields
        return append_unclipped_scene_sprites_fields(memory, frame)
    if target == 239992:
        from ..high_level_scene_flows.business_scene import advance_scene_palette_fade_fields
        return advance_scene_palette_fade_fields(memory, frame)
    if target == 240056:
        return memory.sync_status(frame)
    if target == 240184:
        return begin_scene_palette_lighten_fields(memory, frame)
    if target == 240248:
        return snapshot_scene_palette_fields(memory, frame)
    if target == 240286:
        return restore_scene_palette_fields(memory, frame)
    if target == 240342:
        from ..high_level_scene_flows.business_scene import read_vdp_plane_rle_rows_from_control_fields
        return read_vdp_plane_rle_rows_from_control_fields(memory, frame)
    if target == 242352:
        from ..high_level_scene_flows.business_scene import set_vram_write_address_fields
        return set_vram_write_address_fields(memory, frame)
    if target == 242392:
        return encode_six_decimal_digits_fields(memory, frame)
    if target == 242454:
        return append_decimal_digit_fields(memory, frame)
    if target == 243490:
        from ..high_level_scene_flows.business_scene import sample_random_preserving_seed_fields
        return sample_random_preserving_seed_fields(memory, frame)
    if target == 253126:
        return step_result_scene_phase_fields(memory, frame)
    if target == 253130:
        return step_confirmation_scene_phase_fields(memory, frame)
    if target == 253134:
        return step_transfer_scene_phase_fields(memory, frame)
    if target == 253138:
        return step_primary_detail_scene_phase_fields(memory, frame)
    if target == 253142:
        return step_secondary_detail_scene_phase_fields(memory, frame)
    if target == 253146:
        return step_summary_scene_phase_fields(memory, frame)
    if target == 253150:
        return step_pair_transition_scene_phase_fields(memory, frame)
    if target == 253154:
        return step_initial_scene_phase_fields(memory, frame)
    if target == 253158:
        return step_exchange_scene_phase_fields(memory, frame)
    if target == 253176:
        return initialize_early_scene_fields(memory, frame)
    if target == 253180:
        return process_early_scene_choice_fields(memory, frame)
    if target == 253184:
        return present_early_scene_prompt_fields(memory, frame)
    if target == 253188:
        return finish_early_scene_prompt_fields(memory, frame)
    if target == 253192:
        return wait_early_scene_choice_fields(memory, frame)
    if target == 253196:
        return finish_early_scene_fade_fields(memory, frame)
    if target == 253200:
        return finish_alternate_scene_fade_fields(memory, frame)
    if target == 254548:
        return draw_early_scene_choice_fields(memory, frame)
    if target == 254842:
        return append_early_scene_instruction_fields(memory, frame)
    if target == 255018:
        return paint_scene_number_rows_fields(memory, frame)
    if target == 255034:
        return paint_scene_number_row_fields(memory, frame)
    if target == 255084:
        return wait_exchange_scene_transition_fields(memory, frame)
    if target == 255088:
        return process_exchange_scene_choice_fields(memory, frame)
    if target == 255092:
        return finish_exchange_scene_transition_fields(memory, frame)
    if target == 255522:
        return process_pair_phase_counter_fields(memory, frame)
    if target == 255526:
        return confirm_pair_allocation_fields(memory, frame)
    if target == 255530:
        return update_pair_allocation_input_fields(memory, frame)
    if target == 255534:
        return exit_pair_allocation_fields(memory, frame)
    if target == 255538:
        return gather_early_scene_input_fields(memory, frame)
    if target == 255720:
        return exchange_scene_pair_frame_fields(memory, frame)
    if target == 255918:
        return exchange_scene_actor_records_fields(memory, frame)
    if target == 256160:
        return refresh_primary_actor_summary_fields(memory, frame)
    if target == 256256:
        return wait_pair_stage_motion_fields(memory, frame)
    if target == 256260:
        return advance_pair_stage_motion_fields(memory, frame)
    if target == 256264:
        return confirm_second_pair_allocation_fields(memory, frame)
    if target == 256268:
        return present_pair_stage_summary_fields(memory, frame)
    if target == 256272:
        from .business_late_phase import adjust_secondary_formation_scene_fields
        return adjust_secondary_formation_scene_fields(memory, frame)
    if target == 256276:
        from .business_late_phase import confirm_secondary_formation_scene_fields
        return confirm_secondary_formation_scene_fields(memory, frame)
    if target == 256280:
        from .business_late_phase import update_active_battle_controls_fields
        return update_active_battle_controls_fields(memory, frame)
    if target == 256284:
        from .business_late_phase import latch_scene_controller_inputs_fields
        return latch_scene_controller_inputs_fields(memory, frame)
    if target == 256738:
        from .business_late_phase import draw_two_prompt_backgrounds_fields
        return draw_two_prompt_backgrounds_fields(memory, frame)
    if target == 257224:
        from .business_late_phase import update_secondary_scene_totals_fields
        return update_secondary_scene_totals_fields(memory, frame)
    if target == 257926:
        from .business_late_phase import begin_transition_prompt_fields
        return begin_transition_prompt_fields(memory, frame)
    if target == 257930:
        from .business_late_phase import update_action_mode_prompt_fields
        return update_action_mode_prompt_fields(memory, frame)
    if target == 258096:
        from .business_late_phase import dismiss_action_mode_prompt_fields
        return dismiss_action_mode_prompt_fields(memory, frame)
    if target == 258146:
        from .business_late_phase import begin_duel_handoff_prompt_fields
        return begin_duel_handoff_prompt_fields(memory, frame)
    if target == 258150:
        from .business_late_phase import confirm_duel_handoff_prompt_fields
        return confirm_duel_handoff_prompt_fields(memory, frame)
    if target == 258154:
        from .business_late_phase import await_duel_handoff_palette_fields
        return await_duel_handoff_palette_fields(memory, frame)
    if target == 258158:
        from .business_late_phase import finish_duel_handoff_phase_fields
        return finish_duel_handoff_phase_fields(memory, frame)
    if target == 258270:
        from .business_late_phase import commit_duel_handoff_fields
        return commit_duel_handoff_fields(memory, frame)
    if target == 258538:
        from .business_late_phase import begin_result_confirmation_prompt_fields
        return begin_result_confirmation_prompt_fields(memory, frame)
    if target == 258542:
        from .business_late_phase import confirm_result_prompt_fields
        return confirm_result_prompt_fields(memory, frame)
    if target == 258546:
        from .business_late_phase import await_result_palette_fields
        return await_result_palette_fields(memory, frame)
    if target == 258550:
        from .business_late_phase import finish_result_phase_fields
        return finish_result_phase_fields(memory, frame)
    if target == 258716:
        from .business_late_phase import begin_secondary_confirmation_prompt_fields
        return begin_secondary_confirmation_prompt_fields(memory, frame)
    if target == 258720:
        from .business_late_phase import confirm_secondary_result_prompt_fields
        return confirm_secondary_result_prompt_fields(memory, frame)
    if target == 258724:
        from .business_late_phase import await_secondary_result_palette_fields
        return await_secondary_result_palette_fields(memory, frame)
    if target == 258728:
        from .business_late_phase import finish_secondary_result_phase_fields
        return finish_secondary_result_phase_fields(memory, frame)
    if target == 258894:
        from .business_late_phase import begin_primary_confirmation_prompt_fields
        return begin_primary_confirmation_prompt_fields(memory, frame)
    if target == 258898:
        from .business_late_phase import replace_primary_confirmation_prompt_fields
        return replace_primary_confirmation_prompt_fields(memory, frame)
    if target == 258902:
        from .business_late_phase import confirm_primary_result_prompt_fields
        return confirm_primary_result_prompt_fields(memory, frame)
    if target == 258906:
        from .business_late_phase import await_primary_result_palette_fields
        return await_primary_result_palette_fields(memory, frame)
    if target == 258910:
        from .business_late_phase import finish_primary_result_phase_fields
        return finish_primary_result_phase_fields(memory, frame)
    if target == 259166:
        from .business_late_phase import normalize_secondary_squad_size_fields
        return normalize_secondary_squad_size_fields(memory, frame)
    if target == 259352:
        from .business_late_phase import adjust_secondary_squad_count_fields
        return adjust_secondary_squad_count_fields(memory, frame)
    if target == 259378:
        from .business_late_phase import adjust_selected_squad_class_counts_fields
        return adjust_selected_squad_class_counts_fields(memory, frame)
    if target == 259656:
        from .business_late_phase import deploy_secondary_formation_fields
        return deploy_secondary_formation_fields(memory, frame)
    if target == 259778:
        from .business_late_phase import adjust_primary_formation_fields
        return adjust_primary_formation_fields(memory, frame)
    if target == 259822:
        from .business_late_phase import deploy_primary_formation_fields
        return deploy_primary_formation_fields(memory, frame)
    if target == 259936:
        from .business_late_phase import adjust_selected_action_mode_fields
        return adjust_selected_action_mode_fields(memory, frame)
    if target == 260316:
        from .business_late_phase import commit_scene_battle_totals_fields
        return commit_scene_battle_totals_fields(memory, frame)
    if target == 260342:
        from .business_late_phase import draw_secondary_squad_budget_fields
        return draw_secondary_squad_budget_fields(memory, frame)
    if target == 260414:
        from .business_late_phase import draw_squad_class_budgets_fields
        return draw_squad_class_budgets_fields(memory, frame)
    if target == 260550:
        from .business_late_phase import draw_both_force_status_panels_fields
        return draw_both_force_status_panels_fields(memory, frame)
    if target == 260658:
        from .business_late_phase import draw_normal_force_status_panel_fields
        return draw_normal_force_status_panel_fields(memory, frame)
    if target == 261288:
        from .business_late_phase import selected_action_mode_view_fields
        return selected_action_mode_view_fields(memory, frame)
    if target == 261304:
        from .business_late_phase import lookup_action_mode_icon_pair_fields
        return lookup_action_mode_icon_pair_fields(memory, frame)
    if target == 261414:
        from .business_late_phase import draw_special_force_status_panel_fields
        return draw_special_force_status_panel_fields(memory, frame)
    if target == 261726:
        from .business_late_phase import draw_battle_summary_numbers_fields
        return draw_battle_summary_numbers_fields(memory, frame)
    if target == 261962:
        from .business_late_phase import draw_blinking_decimal_panel_fields
        return draw_blinking_decimal_panel_fields(memory, frame)
    if target == 261998:
        from .business_late_phase import draw_decimal_panel_fields
        return draw_decimal_panel_fields(memory, frame)
    if target == 262850:
        from .business_actions import upload_object_officer_name_frame_fields
        return upload_object_officer_name_frame_fields(memory.state, frame)
    if target == 262940:
        from ..high_level_scene_flows.business_objects import clear_scene_object_label_plane_fields
        return clear_scene_object_label_plane_fields(memory, frame)
    if target == 268312:
        from ..high_level_scene_flows.business_objects import initialize_scene_object_roster_after_mode_check_fields
        return initialize_scene_object_roster_after_mode_check_fields(memory, frame)
    if target == 418260:
        from .business_actions import upload_portrait_tiles_frame_fields
        return upload_portrait_tiles_frame_fields(memory.state, frame)
    raise SceneRefreshBoundary(target, memory.sync_status(frame), continuation)
