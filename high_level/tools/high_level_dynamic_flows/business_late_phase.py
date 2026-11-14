"""Late scene transitions, force setup and battle numeric presentation.

These are logical operations over the same live scene RAM and supplied VDP
bus. Original partial-width carriers, read/write order, unchecked selectors,
inclusive counters and known anomalous loops remain compatibility behavior.
Readonly pointers and layout/icon parameters come from explicit resources;
this source contains neither art/audio payload nor an instruction interpreter.
"""
from dataclasses import replace
from .domain import (SceneState, Table, Cursor, Long, Word, VideoPlaneAddress,
                     Boundary, uint, u8, u16, u32, s16, low8, low16,
                     replace_byte, replace_word, swap_words, negative_word,
                     divu_retained, descending_inclusive, checked_state, ram_view)
from .contexts_early_phase import (PhaseFrame, BattleActors, SceneControllerFrame,
    SceneControllerOutcome, SceneControllerConditions, phase_from_controller,
    phase_controller_return, phase_operands, phase_logic, phase_compare,
    phase_add_word, phase_bit, phase_enter_call, phase_finish_call)
from .contexts_late_phase import (DigitPanelContext, DigitPanelResult,
    ForcePanelContext, ActionIconContext, LatePhaseDispatch, checked_phase,
    checked_context)



from .services import (
    SceneRefreshMemory,SceneRefreshBoundary,FirstDeploymentFrame,first_replace,
    _first_word,_first_byte,_first_long,_scene_refresh_flags,_scene_refresh_emit,
    _scene_render_bit,_scene_render_compare,_scene_render_asl_word,_scene_render_arithmetic,
    _object_adjust_word_fields,_object_clear_word_fields,_scene_refresh_decrement,
    _presentation_call_fields,BattlePresentationMemory,enqueue_sound_command_fields,
    clear_scene_object_label_plane_fields,read_vdp_plane_rle_rows_fields,
)

def _port(state, name):
    return ram_view(state, 'ram_' + name)


def _word(state, name):
    return _port(state, name).word()


def _byte(state, name):
    return _port(state, name).byte()


def _put(state, name, value):
    _port(state, name).set_word(0, u16(value))


def _increment(state, name, amount=1):
    _put(state, name, _word(state, name) + amount)


def _input_bit(state, name, bit):
    return bool(_byte(state, name) & (1 << bit))

















def latch_scene_controller_inputs(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    from .business_early_phase import _phase_legacy_fields,_phase_legacy_projection
    actual = _phase_legacy_fields(state,frame,0x3E91C)
    return _phase_legacy_projection(state,frame,latch_scene_controller_inputs_fields(SceneRefreshMemory(state),actual))


def draw_two_prompt_backgrounds(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 256738)
    returned = draw_two_prompt_backgrounds_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def update_secondary_scene_totals(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical phase observations project the sole complete live-RAM rule."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    entered=_phase_legacy_fields(state,frame,0x3ecc8)
    returned=update_secondary_scene_totals_fields(SceneRefreshMemory(state),entered)
    return _phase_legacy_projection(state,frame,returned)


def adjust_secondary_formation_scene(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    from .business_early_phase import _phase_legacy_fields,_phase_legacy_projection
    actual = _phase_legacy_fields(state,frame,0x3ECDC,True)
    return _phase_legacy_projection(state,frame,adjust_secondary_formation_scene_fields(SceneRefreshMemory(state),actual))


def confirm_secondary_formation_scene(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    return adjust_secondary_formation_scene(state,frame)





def begin_transition_prompt(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 257926)
    returned = begin_transition_prompt_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def begin_duel_handoff_prompt(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258146)
    returned = begin_duel_handoff_prompt_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def begin_result_confirmation_prompt(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258538)
    returned = begin_result_confirmation_prompt_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def begin_secondary_confirmation_prompt(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258716)
    returned = begin_secondary_confirmation_prompt_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def begin_primary_confirmation_prompt(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258894)
    returned = begin_primary_confirmation_prompt_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)







def update_action_mode_prompt(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 257930)
    returned = update_action_mode_prompt_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def dismiss_action_mode_prompt(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258096)
    returned = dismiss_action_mode_prompt_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)







def confirm_duel_handoff_prompt(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258150)
    returned = confirm_duel_handoff_prompt_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def commit_duel_handoff(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258270)
    returned = commit_duel_handoff_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)







def await_duel_handoff_palette(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258154)
    returned = await_duel_handoff_palette_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def await_result_palette(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258546)
    returned = await_result_palette_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def await_secondary_result_palette(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258724)
    returned = await_secondary_result_palette_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def await_primary_result_palette(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258906)
    returned = await_primary_result_palette_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def finish_duel_handoff_phase(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258158)
    returned = finish_duel_handoff_phase_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def finish_result_phase(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258550)
    returned = finish_result_phase_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def finish_secondary_result_phase(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258728)
    returned = finish_secondary_result_phase_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def finish_primary_result_phase(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258910)
    returned = finish_primary_result_phase_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)







def confirm_result_prompt(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258542)
    returned = confirm_result_prompt_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def confirm_secondary_result_prompt(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258720)
    returned = confirm_secondary_result_prompt_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def confirm_primary_result_prompt(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258902)
    returned = confirm_primary_result_prompt_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def replace_primary_confirmation_prompt(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 258898)
    returned = replace_primary_confirmation_prompt_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def normalize_secondary_squad_size(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical phase observations project the sole complete live-RAM rule."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    entered=_phase_legacy_fields(state,frame,0x3f45e)
    returned=normalize_secondary_squad_size_fields(SceneRefreshMemory(state),entered)
    return _phase_legacy_projection(state,frame,returned)


def adjust_secondary_squad_count(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical phase observations project the sole complete live-RAM rule."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    entered=_phase_legacy_fields(state,frame,0x3f518)
    returned=adjust_secondary_squad_count_fields(SceneRefreshMemory(state),entered)
    return _phase_legacy_projection(state,frame,returned)


def adjust_selected_squad_class_counts(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical phase observations project the sole complete live-RAM rule."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    entered=_phase_legacy_fields(state,frame,0x3f532)
    returned=adjust_selected_squad_class_counts_fields(SceneRefreshMemory(state),entered)
    return _phase_legacy_projection(state,frame,returned)


def _adjust_formation_choice(state):
    adjust_scene_formation_choice_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def _deploy_formation(state, frame, secondary):
    from .business_early_phase import _phase_legacy_fields,_phase_legacy_projection
    actual = _phase_legacy_fields(state,frame,0x3F648)
    return _phase_legacy_projection(state,frame,deploy_scene_formation_fields(SceneRefreshMemory(state),actual,secondary))


def adjust_secondary_formation(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    from .business_early_phase import _phase_legacy_fields,_phase_legacy_projection
    actual = _phase_legacy_fields(state,frame,0x3F61C)
    return _phase_legacy_projection(state,frame,adjust_secondary_formation_fields(SceneRefreshMemory(state),actual))


def deploy_secondary_formation(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    return _deploy_formation(state,frame,True)


def adjust_primary_formation(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 259778)
    returned = adjust_primary_formation_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def deploy_primary_formation(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 259822)
    returned = deploy_primary_formation_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def adjust_selected_action_mode(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical phase observations project the sole complete live-RAM rule."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    entered=_phase_legacy_fields(state,frame,0x3f760)
    returned=adjust_selected_action_mode_fields(SceneRefreshMemory(state),entered)
    return _phase_legacy_projection(state,frame,returned)


def commit_scene_battle_totals(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical phase observations project the sole complete live-RAM rule."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    entered=_phase_legacy_fields(state,frame,0x3f8dc)
    returned=commit_scene_battle_totals_fields(SceneRefreshMemory(state),entered)
    return _phase_legacy_projection(state,frame,returned)


def draw_decimal_panel(state: SceneState, context: DigitPanelContext) -> DigitPanelResult:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    context.validate(state)
    actual = _phase_legacy_fields(state, context.frame, 261998)
    actual = first_replace(actual, roster=context.source)
    returned = draw_decimal_panel_fields(SceneRefreshMemory(state), actual)
    return DigitPanelResult(returned.roster, _phase_legacy_projection(state, context.frame, returned)).validate(state)




def draw_blinking_decimal_panel(state: SceneState, context: DigitPanelContext) -> DigitPanelResult:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    context.validate(state)
    actual = _phase_legacy_fields(state, context.frame, 261962)
    actual = first_replace(actual, roster=context.source)
    returned = draw_blinking_decimal_panel_fields(SceneRefreshMemory(state), actual)
    return DigitPanelResult(returned.roster, _phase_legacy_projection(state, context.frame, returned)).validate(state)







def draw_secondary_squad_budget(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 260342)
    returned = draw_secondary_squad_budget_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def draw_squad_class_budgets(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 260414)
    returned = draw_squad_class_budgets_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)







def draw_battle_summary_numbers(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 261726)
    returned = draw_battle_summary_numbers_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def selected_action_mode_view(state: SceneState) -> Table:
    """Historical observations project the sole complete scene algorithm."""
    checked_state(state)
    actual=FirstDeploymentFrame.unobserved()
    returned=selected_action_mode_view_fields(SceneRefreshMemory(state),actual)
    return state.table_at(returned.roster.base)



def lookup_action_mode_icon_pair(state: SceneState, context: ActionIconContext) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    context.validate(state)
    actual = _phase_legacy_fields(state, context.frame, 261304)
    actual = first_replace(actual, unit=context.mode)
    returned = lookup_action_mode_icon_pair_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, context.frame, returned)













def draw_normal_force_status_panel(state: SceneState, context: ForcePanelContext) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    context.validate(state)
    actual = _phase_legacy_fields(state, context.frame, 260658)
    actual = first_replace(actual, auxiliary=context.leader.cursor())
    returned = draw_normal_force_status_panel_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, context.frame, returned)




def draw_special_force_status_panel(state: SceneState, context: ForcePanelContext) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    context.validate(state)
    actual = _phase_legacy_fields(state, context.frame, 261414)
    actual = first_replace(actual, auxiliary=context.leader.cursor())
    returned = draw_special_force_status_panel_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, context.frame, returned)







def draw_both_force_status_panels(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    """Historical observations project the sole complete scene algorithm."""
    from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection
    actual = _phase_legacy_fields(state, frame, 260550)
    returned = draw_both_force_status_panels_fields(SceneRefreshMemory(state), actual)
    return _phase_legacy_projection(state, frame, returned)




def dispatch_late_substate(state: SceneState, frame: PhaseFrame,
                           slot_address: Long) -> PhaseFrame:
    """Resolve only the actual late-phase executable table cells.

    The caller computes its signed wrapped WORD index from live813C. This
    helper does not clamp a selector or pretend other executable cells return.
    Unknown cells remain a typed tail-JMP boundary with their real address.
    """
    checked_phase(frame, state)
    uint(slot_address, 32)
    if frame.live is not None:
        # These are proven complete named paths, not an acceptance wrapper for
        # every legacy body. Large presentation paths remain real call gaps.
        complete = {
            0x3E910: adjust_secondary_formation_scene,
            0x3E914: confirm_secondary_formation_scene,
            0x3E918: update_active_battle_controls,
            0x3E91C: latch_scene_controller_inputs,
            0x3F030: dismiss_action_mode_prompt,
            0x3F066: confirm_duel_handoff_prompt,
            0x3F06A: await_duel_handoff_palette,
            0x3F06E: finish_duel_handoff_phase,
            0x3F1EE: confirm_result_prompt,
            0x3F1F2: await_result_palette,
            0x3F1F6: finish_result_phase,
            0x3F2A0: confirm_secondary_result_prompt,
            0x3F2A4: await_secondary_result_palette,
            0x3F2A8: finish_secondary_result_phase,
            0x3F356: confirm_primary_result_prompt,
            0x3F35A: await_primary_result_palette,
            0x3F35E: finish_primary_result_phase,
        }
        handler = complete.get(slot_address)
        if handler is not None:
            return handler(state, frame)
        result = state.service_at(slot_address, phase_controller_return(state, frame))
        if type(result) is SceneControllerOutcome:
            return result.validate(state)
        if type(result) is not SceneControllerFrame:
            raise Boundary('phase tail requires actual complete frame or consumed continuation')
        return phase_from_controller(state, result.validate(state))
    handlers = {
        0x3EF86: begin_transition_prompt,
        0x3EF8A: update_action_mode_prompt,
        0x3F030: dismiss_action_mode_prompt,
        0x3F062: begin_duel_handoff_prompt,
        0x3F066: confirm_duel_handoff_prompt,
        0x3F06A: await_duel_handoff_palette,
        0x3F06E: finish_duel_handoff_phase,
        0x3F1EA: begin_result_confirmation_prompt,
        0x3F1EE: confirm_result_prompt,
        0x3F1F2: await_result_palette,
        0x3F1F6: finish_result_phase,
        0x3F29C: begin_secondary_confirmation_prompt,
        0x3F2A0: confirm_secondary_result_prompt,
        0x3F2A4: await_secondary_result_palette,
        0x3F2A8: finish_secondary_result_phase,
        0x3F34E: begin_primary_confirmation_prompt,
        0x3F352: replace_primary_confirmation_prompt,
        0x3F356: confirm_primary_result_prompt,
        0x3F35A: await_primary_result_palette,
        0x3F35E: finish_primary_result_phase,
    }
    handler = handlers.get(slot_address)
    if handler is not None:
        return handler(state, frame)
    result = state.service_at(slot_address, LatePhaseDispatch(slot_address, frame))
    return checked_phase(result, state)








def update_active_battle_controls(state: SceneState, frame: PhaseFrame) -> PhaseFrame:
    from .business_early_phase import _phase_legacy_fields,_phase_legacy_projection
    actual = _phase_legacy_fields(state,frame,0x3ED0C,True)
    return _phase_legacy_projection(state,frame,update_active_battle_controls_fields(SceneRefreshMemory(state),actual))

def _phase_read(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        address: Long, width: Word):
    memory.sync_status(frame)
    return memory.state.read(address,width)

def _phase_word_from_memory(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        name, address: Long) -> FirstDeploymentFrame:
    value = _phase_read(memory,frame,address,2)
    return _scene_refresh_flags(memory,_first_word(frame,name,value),value,2)

def _phase_call_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long) -> FirstDeploymentFrame:
    """Only the cached real target/token pairs; unknown children retain their physical slot."""
    if (target, continuation) not in ((256284, 256246), (259612, 257248), (262940, 257262), (262940, 257290), (252272, 257296), (32906, 257360), (262850, 257420), (262850, 257446), (240342, 257486), (260550, 257490), (240342, 257526), (240342, 257558), (260550, 257562), (32906, 257634), (262850, 257694), (262850, 257710), (262850, 257726), (262850, 257742), (240342, 257774), (261726, 257796), (269228, 257822)):
        raise ValueError('actual main phase target/continuation required')
    if frame.stack_cursor is None or frame.status is None:
        raise SceneRefreshBoundary(target, frame, None)

    def child(state, entered):
        if target == 256284:
            return latch_scene_controller_inputs_fields(memory, entered)
        if target == 259612:
            return adjust_secondary_formation_fields(memory, entered)
        if target == 262940:
            return clear_scene_object_label_plane_fields(memory, entered)
        if target == 252272:
            from .business_early_phase import adjust_scene_scroll_fields
            return adjust_scene_scroll_fields(memory, entered)
        if target == 32906:
            return enqueue_sound_command_fields(memory, entered)
        if target == 262850:
            from .business_actions import upload_object_officer_name_frame_fields
            return upload_object_officer_name_frame_fields(memory.state, entered)
        if target == 260550:
            return draw_both_force_status_panels_fields(memory, entered)
        if target == 261726:
            return draw_battle_summary_numbers_fields(memory, entered)
        if target == 240342:
            from ..high_level_scene_flows.business_scene import read_vdp_plane_rle_rows_from_control_fields
            return read_vdp_plane_rle_rows_from_control_fields(memory, entered)
        if target == 269228:
            from .business_actions import update_object_action_ai_fields
            return update_object_action_ai_fields(memory, entered)
        raise SceneRefreshBoundary(target, memory.sync_status(entered), continuation)
    return _presentation_call_fields(BattlePresentationMemory(memory.state), frame, continuation, child)

def latch_scene_controller_inputs_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3E91C: repeated live controller reads, full retained D0 and actual CLR read."""
    memory.frame(frame)
    mode = _phase_read(memory,frame,0xFFFF80DA,1)
    frame = _scene_refresh_flags(memory,frame,mode,1)
    if mode == 0:
        frame = _scene_refresh_emit(memory,frame,0xFFFF811C,2,_phase_read(memory,frame,0xFFFFF602,2))
        frame = _scene_refresh_emit(memory,frame,0xFFFF811E,2,_phase_read(memory,frame,0xFFFFF602,2))
        return _object_clear_word_fields(memory,frame,0xFFFF8120)
    mode = _phase_read(memory,frame,0xFFFF80DA,1)
    frame = _scene_render_compare(memory,frame,mode,1,8)
    if mode == 1:
        first,second = 0xFFFFF602,0xFFFFF604
    else:
        mode = _phase_read(memory,frame,0xFFFF80DA,1)
        frame = _scene_render_compare(memory,frame,mode,2,8)
        if mode != 2:
            frame = _scene_refresh_emit(memory,frame,0xFFFF811C,2,_phase_read(memory,frame,0xFFFFF604,2))
            frame = _scene_refresh_emit(memory,frame,0xFFFF811E,2,_phase_read(memory,frame,0xFFFFF604,2))
            return _object_clear_word_fields(memory,frame,0xFFFF8120)
        first,second = 0xFFFFF604,0xFFFFF602
    if frame.target_x is None:
        raise SceneRefreshBoundary(0x3E91C,frame,None)
    frame = _phase_word_from_memory(memory,frame,'target_x',0xFFFFF602)
    value = low16(frame.target_x) | _phase_read(memory,frame,0xFFFFF604,2)
    frame = _scene_refresh_flags(memory,_first_word(frame,'target_x',value),value,2)
    frame = _scene_refresh_emit(memory,frame,0xFFFF811C,2,low16(frame.target_x))
    frame = _scene_refresh_emit(memory,frame,0xFFFF811E,2,_phase_read(memory,frame,first,2))
    return _scene_refresh_emit(memory,frame,0xFFFF8120,2,_phase_read(memory,frame,second,2))

def adjust_scene_formation_choice_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Shared choice WORD algorithm; both historical sides project this one core."""
    memory.frame(frame)
    value = _phase_read(memory,frame,0xFFFF811F,1)
    frame = _scene_render_bit(memory,frame,value,4)
    if value & 4:
        frame = _object_adjust_word_fields(memory,frame,0xFFFF8144,1)
        choice = _phase_read(memory,frame,0xFFFF8144,2)
        frame = _scene_render_compare(memory,frame,choice,5,16)
        if choice >= 5:
            frame = _object_clear_word_fields(memory,frame,0xFFFF8144)
    value = _phase_read(memory,frame,0xFFFF811F,1)
    frame = _scene_render_bit(memory,frame,value,8)
    if value & 8:
        frame = _object_adjust_word_fields(memory,frame,0xFFFF8144,1,True)
        if frame.status is None:
            raise SceneRefreshBoundary(0x3F640,frame,None)
        if frame.status & 8:
            frame = _scene_refresh_emit(memory,frame,0xFFFF8144,2,4)
    return memory.sync_status(frame)

def deploy_scene_formation_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, secondary: bool) -> FirstDeploymentFrame:
    """One shared layout loop; 3F648 full secondary entry, primary legacy projection only."""
    from .services import _first_compare_long
    memory.frame(frame)
    for name in ('target_x','target_y','unit','count'):
        if frame.carrier(name) is None:
            raise SceneRefreshBoundary(0x3F648,frame,None)
    frame = _phase_word_from_memory(memory,frame,'target_x',0xFFFF8144)
    frame = _scene_render_asl_word(memory,frame,'target_x',low16(frame.target_x),2)
    frame = first_replace(frame,roster=memory.cursor_at(0x41A58))
    pointer = frame.roster.long(low16(frame.target_x))
    frame = first_replace(frame,scratch=memory.cursor_at(pointer))
    frame = _phase_word_from_memory(memory,frame,'target_y',0xFFFF80FA)
    frame = _phase_word_from_memory(memory,frame,'unit',0xFFFF80FC)
    frame = _phase_word_from_memory(memory,frame,'count',0xFFFF80FE)
    frame = _scene_refresh_flags(memory,_first_long(frame,'distance',0),0,4)
    frame = first_replace(frame,auxiliary=memory.cursor_at(0xFFFF826A if secondary else 0xFFFF816A))
    end = 0xFFFF836A if secondary else 0xFFFF826A
    while True:
        if secondary:
            frame = _scene_refresh_flags(memory,_first_word(frame,'target_x',352),352,2)
            value = _phase_read(memory,frame,frame.scratch.base,2)
            frame = first_replace(frame,scratch=frame.scratch.advance(2))
            frame = _scene_render_arithmetic(memory,frame,'target_x',352,value,16,True)
            frame = _scene_refresh_emit(memory,frame,u32(frame.auxiliary.base+2),2,low16(frame.target_x))
        else:
            value = _phase_read(memory,frame,frame.scratch.base,2)
            frame = first_replace(frame,scratch=frame.scratch.advance(2))
            frame = _scene_refresh_emit(memory,frame,u32(frame.auxiliary.base+2),2,value)
        value = _phase_read(memory,frame,frame.scratch.base,2)
        frame = first_replace(frame,scratch=frame.scratch.advance(2))
        frame = _scene_refresh_emit(memory,frame,u32(frame.auxiliary.base+4),2,value)
        frame = _scene_refresh_emit(memory,frame,u32(frame.auxiliary.base+6),2,1)
        frame = _scene_refresh_emit(memory,frame,u32(frame.auxiliary.base+8),2,1)
        frame = _scene_refresh_flags(memory,frame,low16(frame.distance),2)
        if low16(frame.distance) == 0:
            frame = _scene_refresh_emit(memory,frame,frame.auxiliary.base,2,0x8003)
            frame = _scene_refresh_flags(memory,_first_long(frame,'distance',1),1,4)
        else:
            selected = None
            for name,header in (('target_y',0x8002),('unit',0x8001),('count',0x8000)):
                value = low16(frame.carrier(name))
                frame = _scene_refresh_flags(memory,frame,value,2)
                if value:
                    selected = name
                    frame = _scene_refresh_emit(memory,frame,frame.auxiliary.base,2,header)
                    frame = _scene_render_arithmetic(memory,frame,name,value,1,16,True)
                    break
            if selected is None:
                return memory.sync_status(frame)
        frame = first_replace(frame,auxiliary=frame.auxiliary.advance(16))
        frame = memory.sync_status(_first_compare_long(frame,frame.auxiliary.base,end))
        if frame.auxiliary.base >= end:
            return memory.sync_status(frame)

def adjust_secondary_formation_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return deploy_scene_formation_fields(memory,adjust_scene_formation_choice_fields(memory,frame),True)

def deploy_secondary_formation_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return deploy_scene_formation_fields(memory,frame,True)

def adjust_secondary_formation_scene_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3E910/3E914 share 3ECDC with three genuine physical call continuations."""
    memory.frame(frame)
    if frame.stack_cursor is None or frame.status is None:
        raise SceneRefreshBoundary(0x3ECDC,frame,None)
    frame = _phase_call_fields(memory,frame,0x3F61C,0x3ECE0)
    frame = _first_byte(frame,'target_x',_phase_read(memory,frame,0xFFFF811F,1))
    value = low16(frame.target_x) & 12
    frame = _scene_refresh_flags(memory,_first_word(frame,'target_x',value),value,2)
    if value:
        return _phase_call_fields(memory,frame,0x4031C,0x3ECEE)
    value = _phase_read(memory,frame,0xFFFF811F,1)
    frame = _scene_render_bit(memory,frame,value,32)
    if value & 32:
        frame = _scene_refresh_emit(memory,frame,0xFFFF813A,2,8)
        frame = _object_clear_word_fields(memory,frame,0xFFFF813C)
        frame = _object_clear_word_fields(memory,frame,0xFFFF814C)
        frame = _phase_call_fields(memory,frame,0x4031C,0x3ED0A)
    return memory.sync_status(frame)

def confirm_secondary_formation_scene_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return adjust_secondary_formation_scene_fields(memory,frame)

def _phase_blank_panel_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, counter: Word) -> FirstDeploymentFrame:
    """Two original DBRA spans write repeatedly to the stationary VDP data port."""
    frame = memory.status_word(frame,0x2700)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,0x50000002)
    frame = first_replace(frame,scratch=memory.cursor_at(0xC00000))
    frame = _scene_refresh_flags(memory,_first_word(frame,'offset_y',0x3333),0x3333,2)
    frame = _scene_refresh_flags(memory,_first_word(frame,'choice',counter),counter,2)
    for index in range(counter+1):
        frame = _scene_refresh_emit(memory,frame,frame.scratch.base,2,low16(frame.offset_y))
        remaining = low16(frame.choice)
        frame = _scene_refresh_decrement(frame,'choice',remaining)
    return _scene_refresh_emit(memory,frame,0xC00004,4,0x50000002)

def _phase_panel_name_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        officer_address: Long, continuation: Long) -> FirstDeploymentFrame:
    frame = _phase_word_from_memory(memory,frame,'choice',officer_address)
    frame = _scene_refresh_flags(memory,_first_word(frame,'target_x',3),3,2)
    frame = _scene_refresh_flags(memory,_first_word(frame,'target_y',1),1,2)
    return _phase_call_fields(memory,frame,0x402C2,continuation)

def _phase_decode_panel_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        source: Long, destination: Long, continuation: Long) -> FirstDeploymentFrame:
    frame = first_replace(frame,roster=memory.cursor_at(source),candidates=memory.cursor_at(destination))
    frame = _scene_refresh_flags(memory,_first_long(frame,'offset_x',128),128,4)
    frame = _scene_refresh_emit(memory,frame,0xFFFF8000,2,0x8000)
    frame = _scene_refresh_flags(memory,_first_word(frame,'offset_y',32),32,2)
    return _phase_call_fields(memory,frame,0x3AAD6,continuation)

def _phase_action_panel_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _scene_refresh_flags(memory,_first_word(frame,'target_x',0xAD),0xAD,2)
    frame = _phase_call_fields(memory,frame,0x808A,0x3ED50)
    frame = _phase_blank_panel_fields(memory,frame,0xBF)
    frame = _phase_panel_name_fields(memory,frame,0xFFFF80E0,0x3ED8C)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,0x51800002)
    frame = _phase_panel_name_fields(memory,frame,0xFFFF80E2,0x3EDA6)
    mode = _phase_read(memory,frame,0xFFFF80DB,1)
    frame = _scene_render_compare(memory,frame,mode,3,8)
    if mode == 3:
        frame = _phase_decode_panel_fields(memory,frame,0x4529B,0xC000,0x3EDCE)
        frame = _phase_call_fields(memory,frame,0x3F9C6,0x3EDD2)
    else:
        frame = _phase_decode_panel_fields(memory,frame,0x45127,0xC000,0x3EDF6)
        frame = _phase_decode_panel_fields(memory,frame,0x45246,0xC040,0x3EE16)
        frame = _phase_call_fields(memory,frame,0x3F9C6,0x3EE1A)
    frame = memory.status_word(frame,0x2500)
    frame = _scene_refresh_emit(memory,frame,0xFFFF813A,2,1)
    frame = _scene_refresh_emit(memory,frame,0xFFFF813C,2,0)
    frame = _scene_refresh_emit(memory,frame,0xFFFF813E,2,1)
    frame = _scene_refresh_emit(memory,frame,0xFFFF8148,2,_phase_read(memory,frame,0xFFFF8138,2))
    frame = _object_clear_word_fields(memory,frame,0xFFFF8146)
    value = _phase_read(memory,frame,0xFFFF8148,2)
    frame = _scene_render_compare(memory,frame,value,6,16)
    if value == 6:
        frame = _scene_refresh_emit(memory,frame,0xFFFF8146,2,1)
    return memory.sync_status(frame)

def _phase_statistics_panel_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _scene_refresh_flags(memory,_first_word(frame,'target_x',0xAD),0xAD,2)
    frame = _phase_call_fields(memory,frame,0x808A,0x3EE62)
    frame = _phase_blank_panel_fields(memory,frame,0x2FF)
    for address,token in ((0xFFFF80DC,0x3EE9E),(0xFFFF80DE,0x3EEAE),
            (0xFFFF80E0,0x3EEBE),(0xFFFF80E2,0x3EECE)):
        frame = _phase_panel_name_fields(memory,frame,address,token)
    frame = _phase_decode_panel_fields(memory,frame,0x44A6C,0xC000,0x3EEEE)
    frame = _scene_refresh_emit(memory,frame,0xFFFF813A,2,2)
    frame = _scene_refresh_emit(memory,frame,0xFFFF813C,2,0)
    frame = _scene_refresh_emit(memory,frame,0xFFFF813E,2,1)
    frame = _phase_call_fields(memory,frame,0x3FE5E,0x3EF04)
    return memory.status_word(frame,0x2500)

def update_active_battle_controls_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3E918/3ED0C: complete active controls, both panel bodies and tick/edge decisions."""
    memory.frame(frame)
    if frame.stack_cursor is None or frame.status is None:
        raise SceneRefreshBoundary(0x3ED0C,frame,None)
    frame = _phase_call_fields(memory,frame,0x3D970,0x3ED10)
    frame = _first_byte(frame,'target_x',_phase_read(memory,frame,0xFFFF811F,1))
    value = low8(frame.target_x) & 32
    frame = _scene_refresh_flags(memory,_first_byte(frame,'target_x',value),value,1)
    if value:
        frame = _object_clear_word_fields(memory,frame,0xFFFF8144)
        frame = _scene_refresh_emit(memory,frame,0xFFFF8116,2,1)
        return _phase_action_panel_fields(memory,frame)
    mode = _phase_read(memory,frame,0xFFFF80DA,1)
    frame = _scene_refresh_flags(memory,frame,mode,1)
    if mode:
        frame = _first_byte(frame,'target_x',_phase_read(memory,frame,0xFFFF8121,1))
        value = low8(frame.target_x) & 32
        frame = _scene_refresh_flags(memory,_first_byte(frame,'target_x',value),value,1)
        if value:
            frame = _scene_refresh_emit(memory,frame,0xFFFF8144,2,1)
            frame = _object_clear_word_fields(memory,frame,0xFFFF8116)
            return _phase_action_panel_fields(memory,frame)
    frame = _first_byte(frame,'target_x',_phase_read(memory,frame,0xFFFF811D,1))
    value = low8(frame.target_x) & 64
    frame = _scene_refresh_flags(memory,_first_byte(frame,'target_x',value),value,1)
    if value:
        return _phase_statistics_panel_fields(memory,frame)
    latch = _phase_read(memory,frame,0xFFFF814C,2)
    frame = _scene_refresh_flags(memory,frame,latch,2)
    if latch == 0:
        frame = _scene_refresh_emit(memory,frame,0xFFFF814C,2,1)
        frame = _object_adjust_word_fields(memory,frame,0xFFFF8160,1)
        frame = _phase_call_fields(memory,frame,0x41BAC,0x3EF1E)
    mode = _phase_read(memory,frame,0xFFFF8130,2)
    frame = _scene_render_compare(memory,frame,mode,6,16)
    if mode == 6:
        position = _phase_read(memory,frame,0xFFFF816C,2)
        frame = _scene_render_compare(memory,frame,position,0,16)
        if position == 0:
            for address,value in ((0xFFFF813A,5),(0xFFFF813C,0),(0xFFFF8114,4),(0xFFFF8116,0)):
                frame = _scene_refresh_emit(memory,frame,address,2,value)
            return memory.sync_status(frame)
    mode = _phase_read(memory,frame,0xFFFF8138,2)
    frame = _scene_render_compare(memory,frame,mode,6,16)
    if mode == 6:
        position = _phase_read(memory,frame,0xFFFF826C,2)
        frame = _scene_render_compare(memory,frame,position,352,16)
        if position >= 352:
            for address,value in ((0xFFFF813A,5),(0xFFFF813C,0),(0xFFFF8114,5),(0xFFFF8116,1)):
                frame = _scene_refresh_emit(memory,frame,address,2,value)
    return memory.sync_status(frame)

from .business_early_phase import (
 _scene_rule_frame_fields, _scene_rule_store_word_fields, _scene_rule_input_bit_fields, _scene_rule_summary_fields,
)
from ..high_level_main_flows.business_movement_support import (
    _movement_move, _movement_move_long, _movement_compare, _movement_test,
    _movement_add_word, _movement_divu_word,
)


def update_secondary_scene_totals_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3ECC8..3ECDC exact secondary total/count update, not a guessed range."""
    return _scene_rule_summary_fields(memory,frame,True)


def normalize_secondary_squad_size_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3F45E original divisor adjustment, including its possible15/16 cycle."""
    frame=_scene_rule_frame_fields(memory,frame,0x3F45E)
    state=memory.state
    while True:
        frame=_movement_move_long(state,frame,'target_x',0)
        frame=_movement_move_long(state,frame,'target_y',0)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFF80E6,2),16)
        frame=_movement_move(state,frame,'target_y',state.read(0xFFFF80EA,2),16)
        if frame.status&4:
            frame=_object_adjust_word_fields(memory,frame,0xFFFF80EA,1)
            continue
        frame=_movement_compare(state,frame,low16(frame.target_y),15,16)
        if not frame.status&5:
            frame=_object_adjust_word_fields(memory,frame,0xFFFF80EA,1,True)
            continue
        frame=_movement_divu_word(state,frame,'target_x',low16(frame.target_y),0x3F482)
        frame=_movement_compare(state,frame,low16(frame.target_x),1000,16)
        if not frame.status&5:
            frame=_object_adjust_word_fields(memory,frame,0xFFFF80EA,1)
            continue
        frame=_movement_compare(state,frame,low16(frame.target_x),100,16)
        if frame.status&5:
            frame=_movement_compare(state,frame,state.read(0xFFFF80EA,2),1,16)
            if not frame.status&4:
                frame=_object_adjust_word_fields(memory,frame,0xFFFF80EA,1,True)
                continue
            frame=_movement_test(state,frame,low16(frame.target_x),16)
            if frame.status&4:
                frame=_scene_rule_store_word_fields(memory,frame,0xFFFF80EE,0,True)
                return _scene_rule_store_word_fields(memory,frame,0xFFFF80F2,0,True)
        frame=_scene_rule_store_word_fields(memory,frame,0xFFFF80EE,low16(frame.target_x))
        frame=_movement_move_long(state,frame,'target_x',swap_words(frame.target_x))
        return _scene_rule_store_word_fields(memory,frame,0xFFFF80F2,low16(frame.target_x))


def adjust_secondary_squad_count_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3F518 two separately read controller bits, ordered real WORD RMWs."""
    frame=_scene_rule_frame_fields(memory,frame,0x3F518)
    frame,pressed=_scene_rule_input_bit_fields(memory,frame,0xFFFF811F,0)
    if pressed:
        frame=_object_adjust_word_fields(memory,frame,0xFFFF80EA,1)
    frame,pressed=_scene_rule_input_bit_fields(memory,frame,0xFFFF811F,1)
    if pressed:
        frame=_object_adjust_word_fields(memory,frame,0xFFFF80EA,1,True)
    return memory.sync_status(frame)


def adjust_selected_squad_class_counts_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3F532 capacity-limited class allocation through actual live readonly pointers."""
    frame=_scene_rule_frame_fields(memory,frame,0x3F532)
    state=memory.state
    frame,pressed=_scene_rule_input_bit_fields(memory,frame,0xFFFF811F,0)
    if pressed:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFF80FA,2),16)
        frame=_movement_add_word(state,frame,'target_x',state.read(0xFFFF80FC,2))
        frame=_movement_add_word(state,frame,'target_x',state.read(0xFFFF80FE,2))
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFF80EA,2),16)
        if frame.status&1:
            frame=_movement_move(state,frame,'target_x',state.read(0xFFFF8144,2),16)
            frame=_scene_render_asl_word(memory,frame,'target_x',low16(frame.target_x),2)
            frame=first_replace(frame,roster=memory.cursor_at(0x3F5F8))
            frame=first_replace(frame,candidates=memory.cursor_at(frame.roster.long(low16(frame.target_x))))
            frame=_movement_move_long(state,frame,'target_x',0)
            for band,threshold in ((1,100),(2,200),(3,300),(4,400),(5,500),(6,600)):
                frame=_movement_compare(state,frame,state.read(0xFFFF8112,2),threshold,16)
                if frame.status&5:
                    break
                frame=_movement_move_long(state,frame,'target_x',band)
            frame=_movement_move(state,frame,'target_y',state.read(0xFFFF8144,2),16)
            frame=_scene_render_asl_word(memory,frame,'target_y',low16(frame.target_y),3)
            frame=_movement_add_word(state,frame,'target_y',low16(frame.target_x))
            frame=_movement_move(state,frame,'target_x',frame.candidates.word(0),16)
            frame=first_replace(frame,roster=memory.cursor_at(0x3F604))
            frame=_movement_compare(state,frame,low8(frame.target_x),frame.roster.byte(low16(frame.target_y)),8)
            if frame.status&1:
                frame=_object_adjust_word_fields(memory,frame,frame.candidates.base,1)
    frame,pressed=_scene_rule_input_bit_fields(memory,frame,0xFFFF811F,1)
    if pressed:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFF8144,2),16)
        frame=_scene_render_asl_word(memory,frame,'target_x',low16(frame.target_x),2)
        frame=first_replace(frame,roster=memory.cursor_at(0x3F5F8))
        frame=first_replace(frame,roster=memory.cursor_at(frame.roster.long(low16(frame.target_x))))
        frame=_movement_test(state,frame,frame.roster.word(0),16)
        if not frame.status&4:
            frame=_object_adjust_word_fields(memory,frame,frame.roster.base,1,True)
    frame,pressed=_scene_rule_input_bit_fields(memory,frame,0xFFFF811F,5)
    if pressed:
        frame=_movement_compare(state,frame,state.read(0xFFFF8144,2),2,16)
        if frame.status&1:
            frame=_object_adjust_word_fields(memory,frame,0xFFFF8144,1)
    frame,pressed=_scene_rule_input_bit_fields(memory,frame,0xFFFF811F,4)
    if pressed:
        frame=_movement_test(state,frame,state.read(0xFFFF8144,2),16)
        if not frame.status&4:
            frame=_object_adjust_word_fields(memory,frame,0xFFFF8144,1,True)
    return memory.sync_status(frame)


def _scene_rule_adjust_action_selection_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, restricted: bool) -> FirstDeploymentFrame:
    """Closed normal/restricted menu selection roles, not a modern clamp."""
    state=memory.state
    if restricted:
        frame=_movement_compare(state,frame,state.read(0xFFFF8148,2),6,16)
        if frame.status&4:
            return _scene_rule_store_word_fields(memory,frame,0xFFFF8146,2)
    frame,pressed=_scene_rule_input_bit_fields(memory,frame,0xFFFF8122,0)
    if pressed:
        return frame
    frame,pressed=_scene_rule_input_bit_fields(memory,frame,0xFFFF8122,1)
    if pressed:
        return frame
    frame,forward=_scene_rule_input_bit_fields(memory,frame,0xFFFF8123,3)
    if restricted:
        if not forward:
            frame,backward=_scene_rule_input_bit_fields(memory,frame,0xFFFF8123,2)
            if not backward:
                return frame
        frame=_object_adjust_word_fields(memory,frame,0xFFFF8146,2,True)
        if frame.status&8:
            frame=_scene_rule_store_word_fields(memory,frame,0xFFFF8146,2)
        return frame
    if forward:
        frame=_object_adjust_word_fields(memory,frame,0xFFFF8146,1)
        frame=_movement_compare(state,frame,state.read(0xFFFF8146,2),4,16)
        if not frame.status&1:
            frame=_scene_rule_store_word_fields(memory,frame,0xFFFF8146,0,True)
            frame=_movement_compare(state,frame,state.read(0xFFFF8148,2),6,16)
            if frame.status&4:
                frame=_scene_rule_store_word_fields(memory,frame,0xFFFF8146,1)
    frame,backward=_scene_rule_input_bit_fields(memory,frame,0xFFFF8123,2)
    if backward:
        frame=_movement_compare(state,frame,state.read(0xFFFF8148,2),6,16)
        special=bool(frame.status&4)
        frame=_object_adjust_word_fields(memory,frame,0xFFFF8146,1,True)
        if (special and frame.status&4) or (not special and frame.status&8):
            frame=_scene_rule_store_word_fields(memory,frame,0xFFFF8146,3)
    return frame


def adjust_selected_action_mode_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3F760 complete selection/parameter edit; actual threshold is11, not17."""
    frame=_scene_rule_frame_fields(memory,frame,0x3F760)
    state=memory.state
    frame=_movement_compare(state,frame,state.read(0xFFFF80DB,1),3,8)
    frame=_scene_rule_adjust_action_selection_fields(memory,frame,bool(frame.status&4))
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFF8146,2),16)
    frame=first_replace(frame,roster=memory.cursor_at(0x3F840))
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_x)),8)
    frame=_movement_test(state,frame,state.read(0xFFFF8144,2),16)
    if frame.status&4:
        frame=_movement_add_word(state,frame,'target_x',4)
    frame=_scene_render_asl_word(memory,frame,'target_x',low16(frame.target_x),1)
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFF812A))
    frame,pressed=_scene_rule_input_bit_fields(memory,frame,0xFFFF8123,0)
    if pressed:
        address=frame.roster.address(low16(frame.target_x))
        frame=_object_adjust_word_fields(memory,frame,address,1)
        frame=_movement_compare(state,frame,state.read(0xFFFF8160,2),11,16)
        fewer=bool(frame.status&1)
        frame=_movement_compare(state,frame,frame.roster.word(low16(frame.target_x)),6,16)
        if (fewer and not frame.status&1) or (not fewer and not frame.status&5):
            frame=_scene_rule_store_word_fields(memory,frame,address,0,True)
    frame,pressed=_scene_rule_input_bit_fields(memory,frame,0xFFFF8123,1)
    if pressed:
        address=frame.roster.address(low16(frame.target_x))
        frame=_object_adjust_word_fields(memory,frame,address,1,True)
        if frame.status&8:
            frame=_scene_rule_store_word_fields(memory,frame,address,6)
            frame=_movement_compare(state,frame,state.read(0xFFFF8160,2),11,16)
            if frame.status&1:
                frame=_scene_rule_store_word_fields(memory,frame,address,5)
    return memory.sync_status(frame)


def commit_scene_battle_totals_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3F8DC real3F8E0 child LONG, unique two-roster sum and four actual WORD stores."""
    from .business_actions import sum_live_object_rosters_fields
    frame=_scene_rule_frame_fields(memory,frame,0x3F8DC)
    def child(actual,entered):
        return sum_live_object_rosters_fields(SceneRefreshMemory(actual.state),entered)
    frame=_presentation_call_fields(BattlePresentationMemory(memory.state),frame,0x3F8E0,child)
    frame=_scene_rule_store_word_fields(memory,frame,0xFFFF8118,low16(frame.target_y))
    frame=_scene_rule_store_word_fields(memory,frame,0xFFFF811A,low16(frame.unit))
    frame=_scene_rule_store_word_fields(memory,frame,0xFFFF810C,memory.state.read(0xFFFF8178,2))
    return _scene_rule_store_word_fields(memory,frame,0xFFFF810E,memory.state.read(0xFFFF8278,2))

from .business_early_phase import _allocation_adjust_ram_fields, _allocation_arithmetic_fields, _allocation_call_fields, _allocation_compare_ram_fields, _allocation_dbword_fields, _allocation_decode_panel_fields, _allocation_fill_fields, _allocation_link_clear_fields, _allocation_mask_fields, _allocation_move_fields, _allocation_ram_move_fields, _allocation_read_fields, _allocation_script_fields, _allocation_status_fields, _allocation_store_fields, _allocation_test_ram_fields


def draw_two_prompt_backgrounds_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3EAE2)
    frame=_allocation_decode_panel_fields(memory,frame,0x44EF5,0xC980,10,0x3EB02)
    return _allocation_decode_panel_fields(memory,frame,0x45098,0xC9C0,10,0x3EB22)


def _allocation_begin_result_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        role) -> FirstDeploymentFrame:
    script,token,active,reset={
        'transition':(0x3B36C,0x3EFDE,False,False),
        'handoff':(0x3B45E,0x3F0C2,True,False),
        'result':(0x3B488,0x3F24A,True,False),
        'secondary':(0x3B47A,0x3F2FC,True,False),
        'primary':(0x3B49E,0x3F3B8,True,True)}[role]
    frame=_allocation_status_fields(memory,frame,0x2700)
    if reset:
        frame=_allocation_store_fields(memory,frame,0x8116,0)
    frame=_allocation_fill_fields(memory,frame,0x60000002,0x3333,0xD7F,True)
    frame=_allocation_script_fields(memory,frame,script)
    frame=_allocation_call_fields(memory,frame,0x3EAE2,token)
    frame=_allocation_status_fields(memory,frame,0x2500)
    frame=_allocation_adjust_ram_fields(memory,frame,0x813C)
    return _allocation_store_fields(memory,frame,0x813E,1) if active else frame


def begin_transition_prompt_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3EF86)
    return _allocation_begin_result_fields(memory,frame,'transition')


def begin_duel_handoff_prompt_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3F062)
    return _allocation_begin_result_fields(memory,frame,'handoff')


def begin_result_confirmation_prompt_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3F1EA)
    return _allocation_begin_result_fields(memory,frame,'result')


def begin_secondary_confirmation_prompt_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3F29C)
    return _allocation_begin_result_fields(memory,frame,'secondary')


def begin_primary_confirmation_prompt_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3F34E)
    return _allocation_begin_result_fields(memory,frame,'primary')


def _allocation_dismiss_result_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        token: Long) -> FirstDeploymentFrame:
    frame=_allocation_call_fields(memory,frame,0x4031C,token)
    frame=_allocation_store_fields(memory,frame,0x813A,0)
    frame=_allocation_store_fields(memory,frame,0x813C,6)
    return _allocation_store_fields(memory,frame,0x813E,0,clear=True)


def update_action_mode_prompt_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3EF8A)
    frame=_allocation_ram_move_fields(memory,frame,'target_x',0x811E)
    frame=_allocation_test_ram_fields(memory,frame,0x8144)
    if not frame.status&4:
        frame=_allocation_ram_move_fields(memory,frame,'target_x',0x8120)
    frame=_allocation_store_fields(memory,frame,0x8122,low16(frame.target_x))
    frame=_allocation_call_fields(memory,frame,0x3F760,0x3EFFE)
    frame=_allocation_call_fields(memory,frame,0x3F9C6,0x3F002)
    frame=_allocation_ram_move_fields(memory,frame,'target_x',0x8122)
    frame=_allocation_mask_fields(memory,frame,'target_x',0xF0,8)
    return _allocation_dismiss_result_fields(memory,frame,0x3F010) if not frame.status&4 else frame


def dismiss_action_mode_prompt_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3F030)
    frame=_allocation_ram_move_fields(memory,frame,'target_x',0x811D,8)
    frame=_allocation_mask_fields(memory,frame,'target_x',0xF0,8)
    return _allocation_dismiss_result_fields(memory,frame,0x3F042) if not frame.status&4 else frame


def confirm_duel_handoff_prompt_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3F066)
    frame=_allocation_ram_move_fields(memory,frame,'target_x',0x811D,8)
    frame=_allocation_mask_fields(memory,frame,'target_x',0xF0,8)
    return commit_duel_handoff_fields(memory,frame) if not frame.status&4 else frame


def commit_duel_handoff_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3F0DE)
    frame=_allocation_call_fields(memory,frame,0x3F8DC,0x3F0E2)
    frame=_allocation_link_clear_fields(memory,frame)
    frame=_allocation_call_fields(memory,frame,0x3AA38,0x3F100)
    frame=_allocation_adjust_ram_fields(memory,frame,0x813C)
    frame=_object_clear_word_fields(memory,frame,0x00FF70F2)
    frame=_scene_refresh_emit(memory,frame,0x00FF70F3,1,_allocation_read_fields(memory,frame,0xFFFF80DB,1))
    frame=_allocation_test_ram_fields(memory,frame,0x8124)
    reversed_sides=not bool(frame.status&4)
    pairs=((0x80DE,0x7070),(0x80E2,0x706A),(0x8278,0x706C),(0x8106,0x706E),
        (0x80DC,0x70C0),(0x80E0,0x70BA),(0x8178,0x70BC),(0x8104,0x70BE)) if reversed_sides else (
        (0x80DC,0x7070),(0x80E0,0x706A),(0x8178,0x706C),(0x8104,0x706E),
        (0x80DE,0x70C0),(0x80E2,0x70BA),(0x8278,0x70BC),(0x8106,0x70BE))
    for source,destination in pairs:
        frame=_scene_refresh_emit(memory,frame,0x00FF0000|destination,2,_allocation_read_fields(memory,frame,0xFFFF0000|source,2))
    frame=_allocation_move_fields(memory,frame,'target_x',0,32)
    frame=_allocation_ram_move_fields(memory,frame,'target_x',0x80DA,8)
    frame=_scene_render_asl_word(memory,frame,'target_x',low16(frame.target_x),1)
    table=memory.state.table_at(0x3F1C4 if reversed_sides else 0x3F16A)
    return _scene_refresh_emit(memory,frame,0x00FF700A,2,table.word(low16(frame.target_x)))


def await_duel_handoff_palette_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3F06A)
    frame,finished=_scene_rule_input_bit_fields(memory,frame,0xFFFF80C4,7)
    return _allocation_adjust_ram_fields(memory,frame,0x813C) if finished else frame


def _allocation_confirm_result_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        role) -> FirstDeploymentFrame:
    mask,preincrement,total_token,palette_token={
        'result':(0xF0,False,0x3F26A,0x3F28C),
        'secondary':(0xF0,True,0x3F320,0x3F33E),
        'primary':(0x20,True,0x3F43E,0x3F45C)}[role]
    frame=_allocation_ram_move_fields(memory,frame,'target_x',0x811D,8)
    frame=_allocation_mask_fields(memory,frame,'target_x',mask,8)
    if frame.status&4:
        return frame
    if preincrement:
        frame=_allocation_adjust_ram_fields(memory,frame,0x813C)
    frame=_allocation_call_fields(memory,frame,0x3F8DC,total_token)
    if not preincrement:
        frame=_allocation_adjust_ram_fields(memory,frame,0x813C)
    frame=_allocation_link_clear_fields(memory,frame)
    return _allocation_call_fields(memory,frame,0x3AA38,palette_token)


def confirm_result_prompt_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3F1EE)
    return _allocation_confirm_result_fields(memory,frame,'result')


def confirm_secondary_result_prompt_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3F2A0)
    return _allocation_confirm_result_fields(memory,frame,'secondary')


def confirm_primary_result_prompt_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3F356)
    return _allocation_confirm_result_fields(memory,frame,'primary')


def replace_primary_confirmation_prompt_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3F352)
    frame=_allocation_ram_move_fields(memory,frame,'target_x',0x811D,8)
    frame=_allocation_mask_fields(memory,frame,'target_x',0x20,8)
    if frame.status&4:
        return frame
    frame=_allocation_status_fields(memory,frame,0x2700)
    frame=_allocation_fill_fields(memory,frame,0x60000002,0x3333,0xD7F,True)
    frame=_allocation_script_fields(memory,frame,0x3B4B6)
    frame=_allocation_adjust_ram_fields(memory,frame,0x813C)
    return _allocation_status_fields(memory,frame,0x2500)


def adjust_primary_formation_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3F6C2)
    frame=adjust_scene_formation_choice_fields(memory,frame)
    return deploy_primary_formation_fields(memory,frame)


def deploy_primary_formation_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3F6EE)
    return deploy_scene_formation_fields(memory,frame,False)


def _allocation_number_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        low: Word, video: Word, count: Word, digit: Word,
        formatter_token: Long, panel_token: Long | None) -> FirstDeploymentFrame:
    frame=_allocation_move_fields(memory,frame,'target_x',0,32)
    frame=_allocation_ram_move_fields(memory,frame,'target_x',low)
    frame=_allocation_call_fields(memory,frame,0x3B2D8,formatter_token)
    frame=_allocation_move_fields(memory,frame,'target_x',video)
    frame=_allocation_move_fields(memory,frame,'count',count,32)
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFF8000+digit))
    if panel_token is None:
        return frame
    return _allocation_call_fields(memory,frame,0x3FF6E,panel_token)


def draw_secondary_squad_budget_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3F8F6)
    frame=_allocation_number_fields(memory,frame,0x80E6,0xC3AE,4,1,0x3F900,0x3F90E)
    frame=_allocation_number_fields(memory,frame,0x80EE,0xC530,3,2,0x3F918,0x3F926)
    frame=_allocation_number_fields(memory,frame,0x80EA,0xC6B4,1,4,0x3F930,None)
    return draw_blinking_decimal_panel_fields(memory,frame)


def draw_squad_class_budgets_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3F93E)
    frame=_allocation_number_fields(memory,frame,0x80EA,0xC1AC,1,4,0x3F948,0x3F956)
    plans=((0x80FA,0xC3AC,0,0x3F960,0x3F974,0x3F97C),
        (0x80FC,0xC5AC,1,0x3F986,0x3F99C,0x3F9A4),
        (0x80FE,0xC7AC,2,0x3F9AE,None,None))
    for low,video,index,format_token,blink_token,normal_token in plans:
        frame=_allocation_number_fields(memory,frame,low,video,1,4,format_token,None)
        if index==0:
            frame=_allocation_test_ram_fields(memory,frame,0x8144)
        else:
            frame=_allocation_compare_ram_fields(memory,frame,0x8144,index)
        blink=bool(frame.status&4)
        if blink_token is None:
            return draw_blinking_decimal_panel_fields(memory,frame) if blink else draw_decimal_panel_fields(memory,frame)
        frame=_allocation_call_fields(memory,frame,0x3FF4A if blink else 0x3FF6E,blink_token if blink else normal_token)
    return frame


def draw_blinking_decimal_panel_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3FF4A)
    frame,show=_scene_rule_input_bit_fields(memory,frame,0xFFFFF321,4)
    if show:
        return draw_decimal_panel_fields(memory,frame)
    frame=_scene_refresh_emit(memory,frame,0xC00004,2,0x8F02)
    frame=_allocation_call_fields(memory,frame,0x3B2B0,0x3FF5E)
    frame=_allocation_move_fields(memory,frame,'target_y',0xC448)
    while True:
        frame=_scene_refresh_emit(memory,frame,0xC00000,2,low16(frame.target_y))
        frame,done=_allocation_dbword_fields(frame,'count')
        if done:
            return frame


def draw_decimal_panel_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3FF6E)
    frame=_scene_refresh_emit(memory,frame,0xC00004,2,0x8F02)
    frame=_allocation_call_fields(memory,frame,0x3B2B0,0x3FF7A)
    frame=_allocation_move_fields(memory,frame,'unit',0,32)
    while True:
        frame=_allocation_move_fields(memory,frame,'target_y',0,32)
        value=frame.roster.byte()
        frame=first_replace(frame,roster=frame.roster.advance(1))
        frame=_allocation_move_fields(memory,frame,'target_y',value,8)
        show=not bool(frame.status&4)
        if not show:
            frame=_movement_test(memory.state,frame,low16(frame.unit),16)
            show=not bool(frame.status&4)
            if not show:
                frame=_movement_test(memory.state,frame,low16(frame.count),16)
                show=bool(frame.status&4)
        if show:
            frame=_allocation_move_fields(memory,frame,'unit',1,32)
            frame=_allocation_arithmetic_fields(memory,frame,'target_y',0xC460)
        else:
            frame=_allocation_move_fields(memory,frame,'target_y',0xC448)
        frame=_scene_refresh_emit(memory,frame,0xC00000,2,low16(frame.target_y))
        frame,done=_allocation_dbword_fields(frame,'count')
        if done:
            return frame


def _allocation_sum_actor_rows_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        class_id: Word | None) -> FirstDeploymentFrame:
    """One live fifteen-row sum for class-specific and all-active displays."""
    while True:
        memory.sync_status(frame)
        value=frame.auxiliary.byte()
        frame=_scene_render_bit(memory,frame,value,128)
        if value&128:
            include=True
            if class_id is not None:
                member_class=frame.auxiliary.byte(1)
                if class_id==0:
                    frame=_movement_test(memory.state,frame,member_class,8)
                else:
                    frame=_movement_compare(memory.state,frame,member_class,class_id,8)
                include=bool(frame.status&4)
            if include:
                frame=_allocation_arithmetic_fields(memory,frame,'target_x',frame.auxiliary.word(14))
        frame=first_replace(frame,auxiliary=frame.auxiliary.advance(16))
        frame,done=_allocation_dbword_fields(frame,'target_y')
        if done:
            return frame


def _allocation_total_display_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        video: Word, count: Word, digit: Word,
        formatter_token: Long, panel_token: Long | None, video_is_field: bool = False) -> FirstDeploymentFrame:
    frame=_allocation_call_fields(memory,frame,0x3B2D8,formatter_token)
    if video_is_field:
        video=_allocation_read_fields(memory,frame,0xFFFF0000|video,2)
    frame=_allocation_move_fields(memory,frame,'target_x',video)
    frame=_allocation_move_fields(memory,frame,'count',count,32)
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFF8000+digit))
    return draw_decimal_panel_fields(memory,frame) if panel_token is None else _allocation_call_fields(memory,frame,0x3FF6E,panel_token)


def draw_battle_summary_numbers_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3FE5E)
    for low,video,format_token,panel_token in (
        (0x8176,0xC5A0,0x3FE68,0x3FE76),(0x8186,0xC720,0x3FE80,0x3FE8E),
        (0x8276,0xC5B2,0x3FE98,0x3FEA6),(0x8286,0xC732,0x3FEB0,0x3FEBE),
        (0x8100,0xC8A0,0x3FEC8,0x3FED6),(0x8102,0xC8B2,0x3FEE0,0x3FEEE)):
        frame=_allocation_number_fields(memory,frame,low,video,2,3,format_token,panel_token)
    for base,video,format_token,panel_token in (
        (0xFFFF817A,0xCA1C,0x3FF0E,0x3FF1C),(0xFFFF827A,0xCA2E,0x3FF3C,None)):
        frame=_allocation_move_fields(memory,frame,'target_y',14)
        frame=_allocation_move_fields(memory,frame,'target_x',0,32)
        frame=first_replace(frame,auxiliary=memory.cursor_at(base))
        frame=_allocation_sum_actor_rows_fields(memory,frame,None)
        frame=_allocation_total_display_fields(memory,frame,video,4,1,format_token,panel_token)
    return frame


def selected_action_mode_view_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3FCA8)
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFF8132))
    frame=_allocation_test_ram_fields(memory,frame,0x8144)
    return first_replace(frame,roster=memory.cursor_at(0xFFFF812A)) if not frame.status&4 else frame


def lookup_action_mode_icon_pair_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3FCB8)
    frame=_scene_render_asl_word(memory,frame,'unit',low16(frame.unit),2)
    frame=_allocation_move_fields(memory,frame,'target_x',memory.state.table_at(0x3FCC4).word(low16(frame.unit)))
    return _allocation_move_fields(memory,frame,'target_y',memory.state.table_at(0x3FCC6).word(low16(frame.unit)))


def _allocation_icon_pair_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        plan: tuple) -> FirstDeploymentFrame:
    """Closed normal/special icon positions share one exact two-row algorithm."""
    low,offset,index,mode_offset,top_token,blank_token,bottom_token,view_top,icon_top,view_bottom,icon_bottom=plan
    frame=_allocation_ram_move_fields(memory,frame,'target_x',low)
    if offset:
        frame=_allocation_arithmetic_fields(memory,frame,'target_x',offset)
    frame=_allocation_call_fields(memory,frame,0x3B2B0,top_token)
    if index==0:
        frame=_allocation_test_ram_fields(memory,frame,0x8146)
    else:
        frame=_allocation_compare_ram_fields(memory,frame,0x8146,index)
    blank=False
    if frame.status&4:
        frame,show=_scene_rule_input_bit_fields(memory,frame,0xFFFFF321,4)
        blank=not show
    if blank:
        frame=_scene_refresh_emit(memory,frame,0xC00000,2,0xC448)
    else:
        frame=_allocation_call_fields(memory,frame,0x3FCA8,view_top)
        frame=_allocation_move_fields(memory,frame,'unit',frame.roster.word(mode_offset))
        frame=_allocation_call_fields(memory,frame,0x3FCB8,icon_top)
        frame=_scene_refresh_emit(memory,frame,0xC00000,2,low16(frame.target_x))
    frame=_allocation_ram_move_fields(memory,frame,'target_x',low)
    frame=_allocation_arithmetic_fields(memory,frame,'target_x',offset+0x80)
    frame=_allocation_call_fields(memory,frame,0x3B2B0,blank_token if blank else bottom_token)
    if blank:
        return _scene_refresh_emit(memory,frame,0xC00000,2,0xC448)
    frame=_allocation_call_fields(memory,frame,0x3FCA8,view_bottom)
    frame=_allocation_move_fields(memory,frame,'unit',frame.roster.word(mode_offset))
    frame=_allocation_call_fields(memory,frame,0x3FCB8,icon_bottom)
    return _scene_refresh_emit(memory,frame,0xC00000,2,low16(frame.target_y))


def _allocation_selected_panel_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        low: Word) -> tuple[FirstDeploymentFrame, bool]:
    frame=_allocation_test_ram_fields(memory,frame,0x8144)
    selected=bool(frame.status&4)
    frame=_allocation_test_ram_fields(memory,frame,low)
    return frame,bool(frame.status&4) if selected else not bool(frame.status&4)


def draw_normal_force_status_panel_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3FA32)
    frame=_allocation_move_fields(memory,frame,'target_x',0,32)
    frame=_allocation_move_fields(memory,frame,'target_x',frame.auxiliary.word(14))
    frame=_allocation_total_display_fields(memory,frame,0x8010,2,3,0x3FA3C,0x3FA4A,True)
    for class_id,low,count,digit,format_token,panel_token in (
        (2,0x8012,3,2,0x3FA72,0x3FA80),(1,0x8014,3,2,0x3FAA8,0x3FAB6),
        (0,0x8016,4,1,0x3FADC,0x3FAEA)):
        frame=_allocation_move_fields(memory,frame,'target_y',14)
        frame=first_replace(frame,auxiliary=memory.cursor_at(_allocation_read_fields(memory,frame,0xFFFF801C,4)))
        frame=_allocation_move_fields(memory,frame,'target_x',0,32)
        frame=_allocation_sum_actor_rows_fields(memory,frame,class_id)
        frame=_allocation_total_display_fields(memory,frame,low,count,digit,format_token,panel_token,True)
    frame,selected=_allocation_selected_panel_fields(memory,frame,0x801A)
    if not selected:
        return frame
    frame=_scene_refresh_emit(memory,frame,0xC00004,2,0x8F02)
    for plan in (
        (0x8018,0,0,6,0x3FB10,0x3FB32,0x3FB5A,0x3FB40,0x3FB48,0x3FB5E,0x3FB66),
        (0x8018,0x10,1,4,0x3FB78,0x3FB9C,0x3FBC4,0x3FBAA,0x3FBB2,0x3FBC8,0x3FBD0),
        (0x8018,0x20,2,2,0x3FBE2,0x3FC06,0x3FC2E,0x3FC14,0x3FC1C,0x3FC32,0x3FC3A),
        (0x8018,0x32,3,0,0x3FC4C,0x3FC70,0x3FC96,0x3FC7E,0x3FC84,0x3FC9A,0x3FCA0)):
        frame=_allocation_icon_pair_fields(memory,frame,plan)
    return frame


def draw_special_force_status_panel_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3FD26)
    frame=_allocation_move_fields(memory,frame,'target_x',0,32)
    frame=_allocation_move_fields(memory,frame,'target_x',frame.auxiliary.word(14))
    frame=_allocation_total_display_fields(memory,frame,0x8010,2,3,0x3FD30,0x3FD3E,True)
    frame=_allocation_move_fields(memory,frame,'target_y',14)
    frame=first_replace(frame,auxiliary=frame.auxiliary.advance(16))
    frame=_allocation_move_fields(memory,frame,'target_x',0,32)
    frame=_allocation_sum_actor_rows_fields(memory,frame,1)
    frame=_allocation_total_display_fields(memory,frame,0x8012,4,1,0x3FD66,0x3FD74,True)
    frame,selected=_allocation_selected_panel_fields(memory,frame,0x8018)
    if not selected:
        return frame
    frame=_scene_refresh_emit(memory,frame,0xC00004,2,0x8F02)
    for plan in (
        (0x8014,0,0,6,0x3FD9A,0x3FDBC,0x3FDE4,0x3FDCA,0x3FDD2,0x3FDE8,0x3FDF0),
        (0x8016,0,2,2,0x3FDFE,0x3FE22,0x3FE4A,0x3FE30,0x3FE38,0x3FE4E,0x3FE56)):
        frame=_allocation_icon_pair_fields(memory,frame,plan)
    return frame


def _allocation_panel_setup_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        destinations: tuple, marker: Word, marker_low: Word,
        leader: Long, roster: Long | None) -> FirstDeploymentFrame:
    for low,value in zip((0x8010,0x8012,0x8014,0x8016),destinations):
        frame=_allocation_store_fields(memory,frame,low,value)
    if roster is not None:
        frame=_allocation_store_fields(memory,frame,0x8018,marker)
        frame=_allocation_store_fields(memory,frame,marker_low,0 if leader==0xFFFF826A else 1,clear=leader==0xFFFF826A)
        frame=_allocation_store_fields(memory,frame,0x801C,roster,4)
    else:
        frame=_allocation_store_fields(memory,frame,marker_low,marker,clear=marker==0)
    return first_replace(frame,auxiliary=memory.cursor_at(leader))


def draw_both_force_status_panels_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_scene_rule_frame_fields(memory,frame,0x3F9C6)
    frame=_allocation_compare_ram_fields(memory,frame,0x80DB,3,8)
    if not frame.status&4:
        frame=_allocation_panel_setup_fields(memory,frame,(0xC412,0xC420,0xC430,0xC440),0xC398,0x801A,0xFFFF826A,0xFFFF827A)
        frame=_allocation_call_fields(memory,frame,0x3FA32,0x3FA02)
        frame=_allocation_panel_setup_fields(memory,frame,(0xC292,0xC2A0,0xC2B0,0xC2C0),0xC218,0x801A,0xFFFF816A,0xFFFF817A)
        return draw_normal_force_status_panel_fields(memory,frame)
    frame=_allocation_panel_setup_fields(memory,frame,(0xC49E,0xC4B0,0xC424,0xC43A),0,0x8018,0xFFFF826A,None)
    frame=_allocation_call_fields(memory,frame,0x3FD26,0x3FD04)
    # This side's A6 is assigned before its four destination WORD writes.
    frame=first_replace(frame,auxiliary=memory.cursor_at(0xFFFF816A))
    frame=_allocation_panel_setup_fields(memory,frame,(0xC31E,0xC330,0xC2A4,0xC2BA),1,0x8018,0xFFFF816A,None)
    return draw_special_force_status_panel_fields(memory,frame)


def finish_duel_handoff_phase_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Actual named BRA/RTS alias; no synthetic call slot or algorithm."""
    return _scene_rule_frame_fields(memory,frame,0x3f06e)



def await_result_palette_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Actual named BRA/RTS alias; no synthetic call slot or algorithm."""
    frame=_scene_rule_frame_fields(memory,frame,0x3f1f2)
    return await_duel_handoff_palette_fields(memory,frame)



def finish_result_phase_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Actual named BRA/RTS alias; no synthetic call slot or algorithm."""
    return _scene_rule_frame_fields(memory,frame,0x3f1f6)



def await_secondary_result_palette_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Actual named BRA/RTS alias; no synthetic call slot or algorithm."""
    frame=_scene_rule_frame_fields(memory,frame,0x3f2a4)
    return await_duel_handoff_palette_fields(memory,frame)



def await_primary_result_palette_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Actual named BRA/RTS alias; no synthetic call slot or algorithm."""
    frame=_scene_rule_frame_fields(memory,frame,0x3f35a)
    return await_duel_handoff_palette_fields(memory,frame)



def finish_secondary_result_phase_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Actual named BRA/RTS alias; no synthetic call slot or algorithm."""
    return _scene_rule_frame_fields(memory,frame,0x3f2a8)



def finish_primary_result_phase_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Actual named BRA/RTS alias; no synthetic call slot or algorithm."""
    return _scene_rule_frame_fields(memory,frame,0x3f35e)
