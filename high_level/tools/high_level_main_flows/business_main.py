"""Campaign scene requests, pointer/camera motion and roster state controls.

Each public function names an original entry. Shared tails are ordinary logical
helpers; external calls use explicit typed contracts and never fake completion.
"""
from dataclasses import replace
from .domain import (SceneState, Table, Cursor, Word, Long, Boundary, uint,
    checked_state, u8, u16, u32, s16, s8, low8, low16, high16, replace_word,
    replace_byte, swap_words, divu_retained, negative_word, negative_byte, descending_inclusive,
    ram_view, data_view, VideoPlaneAddress)
from .contexts_main import (SceneTick, SoundWord, GlyphStyle, GlyphPlacement,
    CameraStrip, SelectedCity, LeaderRoster, SelectedOfficer, SelectionResolution,
    CarryOutcome, FormationBitResult, RosterInput,
    LeaderRosterDetection, CampaignOwnerDetection, CameraMotionInput, CameraMotionResult,
    CameraPointerBoundaryRequest, CameraTransitionInput, CameraTransitionResult)
from .services import (call_target, enqueue_sound_command, clear_video_sprite_plane,
    decode_glyph_rows_to_buffers, refresh_gameplay_scene,
    initialize_video_registers_and_planes)
from .contexts_map import (MapCoordinate, RenderMapColumnInput, RenderMapColumnResult,
    RenderMapRowInput, RenderMapRowResult, UpdateWorldCursorFromInputsInput,
    UpdateWorldCursorFromInputsResult, RefreshWorldCursorAttributesInput,
    RefreshWorldCursorAttributesResult)
from .contexts_lowbank import RefreshScenePalettesInput, RefreshScenePalettesResult
from .contexts_display_reuse import MapSpriteResult
from .contexts_main import CampaignPointerFields
from .reuse_display import append_map_sprites
from .services import (
    write_vdp_dictionary_repeat_stream, darken_palette)


from .contexts_commands import CommandLabelFrame
from .contexts_main import RosterPanelInput, RosterPanelResult, RosterNameRequest
from .services import GlyphRowsResult

from .contexts_commands import (LocationChoiceFrame, UpdateSelectedForcePromptInput, UpdateSelectedForcePromptResult)
from .contexts_main import LocationChoiceInput, LocationChoiceResult
from .contexts_lowbank import UploadSelectedModeTileRowsInput, UploadSelectedModeTileRowsResult
from .contexts_tick import MapTickFrame, checked_tick_frame

def _ram(state, address):
    return ram_view(state, 'ram_%04x' % address)


def _word(state, address):
    return _ram(state, address).word()


def _put(state, address, value):
    _ram(state, address).set_word(0, u16(value))


def _increment(state, address, amount=1):
    _put(state, address, _word(state, address) + amount)


def _byte(state, address):
    return _ram(state, address).byte()


def _put_byte(state, address, value):
    _ram(state, address).set_byte(0, u8(value))


def _tick(state, target):
    return call_target(state, target, SceneTick())


def _sound(state, command):
    return call_target(state, 0x676F2, SoundWord(u16(command)))


def _style_call(state, target, style):
    return call_target(state, target, style)


def _carry(state, carry, selection=None):
    status = state.read_status_word()
    state.set_status_word(status | 1 if carry else status & 65534)
    return CarryOutcome(carry, selection)


def _foreground(style, value):
    return GlyphStyle(style.background, replace_word(style.foreground, value))


def _default_style(background, foreground):
    uint(background, 32)
    uint(foreground, 32)
    return GlyphStyle(replace_word(background, 1), replace_word(foreground, 3))


def _glyph(state, source, destination, style, remaining):
    style.validate(state)
    return decode_glyph_rows_to_buffers(state, source, destination,
        style.background, style.foreground, remaining)


def _upload_longs(state, source, count):
    for _ in range(count):
        state.write(0xC00000, 4, source.next_long())


def _fill_longs(state, destination, count, value):
    for _ in range(count):
        destination.append_long(value)


def _finish_transfer(state, retained=0):
    return refresh_gameplay_scene(state, retained)


def _begin_transfer(state, disable_plane=False):
    state.set_status_word(0x2700)
    if disable_plane:
        state.write(0xC00004, 2, _word(state, 0xF606) & 0xFFBF)


def process_startup_scene(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=process_startup_scene_fields(state,incoming)
    return None


def reset_menu_sprite_slots(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=reset_menu_sprite_slots_fields(state,incoming)
    return None


def initialize_campaign_screen(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_campaign_screen_fields(state,incoming)
    return None


def upload_selected_dictionary_panel(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=upload_selected_dictionary_panel_fields(state,incoming)
    return None


def initialize_campaign_menu_panels(state: SceneState, retained_background: Long=0, retained_foreground: Long=0):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=retained_background, target_y=retained_foreground)
    observed=initialize_campaign_menu_panels_fields(state,incoming)
    return None


def initialize_officer_detail_panel(state: SceneState, retained_background: Long=0, retained_foreground: Long=0):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=retained_background, target_y=retained_foreground)
    observed=initialize_officer_detail_panel_fields(state,incoming)
    return None


def upload_officer_roster_panel(state: SceneState, retained_background: Long=0, retained_foreground: Long=0, *, panel_inputs: RosterPanelInput | None=None) -> RosterPanelResult:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    from .contexts_display_fields import display_legacy_frame_fields
    entered = display_legacy_frame_fields(state, retained_background, 1044)
    return upload_officer_roster_panel_frame_fields(state, entered)


def upload_formation_caption(state: SceneState, retained_background: Long=0, retained_foreground: Long=0):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=retained_background, target_y=retained_foreground)
    observed=upload_formation_caption_fields(state,incoming)
    return None


def upload_formation_choice_caption(state: SceneState, retained_background: Long=0, retained_foreground: Long=0):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=retained_background, target_y=retained_foreground)
    observed=upload_formation_choice_caption_fields(state,incoming)
    return None


def initialize_formation_choices(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_formation_choices_fields(state,incoming)
    return None


def initialize_city_choice_caption(state: SceneState, retained_background: Long=0, retained_foreground: Long=0):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=retained_background, target_y=retained_foreground)
    observed=initialize_city_choice_caption_fields(state,incoming)
    return None


def request_affordable_action_panel(state: SceneState, retained_background: Long=0, retained_foreground: Long=0):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=retained_background, target_y=retained_foreground)
    observed=request_affordable_action_panel_fields(state,incoming)
    return None


def initialize_officer_portrait(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_officer_portrait_fields(state,incoming)
    return None


def toggle_officer_roster_selection(state: SceneState, retained_background: Long=0, retained_foreground: Long=0):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    if retained_background is not None:
        uint(retained_background,32)
    if retained_foreground is not None:
        uint(retained_foreground,32)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=retained_background,target_y=retained_foreground)
    returned=toggle_officer_roster_selection_fields(state,entered)
    return None



def initialize_education_screen(state: SceneState, retained_background: Long=0, retained_foreground: Long=0):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=retained_background, target_y=retained_foreground)
    observed=initialize_education_screen_fields(state,incoming)
    return None


def initialize_assignment_description(state: SceneState, retained_background: Long=0, retained_foreground: Long=0):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=retained_background, target_y=retained_foreground)
    observed=initialize_assignment_description_fields(state,incoming)
    return None


def initialize_assignment_choices(state: SceneState, retained_background: Long=0, retained_foreground: Long=0):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=retained_background, target_y=retained_foreground)
    observed=initialize_assignment_choices_fields(state,incoming)
    return None


def upload_assignment_caption(state: SceneState, retained_background: Long=0, retained_foreground: Long=0):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=retained_background, target_y=retained_foreground)
    observed=upload_assignment_caption_fields(state,incoming)
    return None


def wait_and_initialize_campaign_action(state: SceneState, retained: Long=0):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=retained)
    observed=wait_and_initialize_campaign_action_fields(state,incoming)
    return None


def initialize_post_duel_campaign(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_post_duel_campaign_fields(state,incoming)
    return None


def upload_three_formation_names(state: SceneState, retained_background: Long=0, retained_foreground: Long=0):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=retained_background, target_y=retained_foreground)
    observed=upload_three_formation_names_fields(state,incoming)
    return None


def upload_three_formation_names_direct(state: SceneState, retained_background: Long=0, retained_foreground: Long=0):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=retained_background, target_y=retained_foreground)
    observed=upload_three_formation_names_direct_fields(state,incoming)
    return None


def refresh_information_panel(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=refresh_information_panel_fields(state,incoming)
    return None


def continue_platform_scene_initialization(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=continue_platform_scene_initialization_fields(state,incoming)
    return None


def initialize_campaign_options(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_campaign_options_fields(state,incoming)
    return None


def initialize_campaign_command_panel(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_campaign_command_panel_fields(state,incoming)
    return None


def initialize_city_detail_panel(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_city_detail_panel_fields(state,incoming)
    return None


def initialize_city_command_panel(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_city_command_panel_fields(state,incoming)
    return None


def initialize_campaign_map(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_campaign_map_fields(state,incoming)
    return None


def initialize_training_screen(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_training_screen_fields(state,incoming)
    return None


def update_training_candidate(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=update_training_candidate_fields(state,incoming)
    return None


def initialize_learning_screen(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_learning_screen_fields(state,incoming)
    return None


def update_learning_candidate(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=update_learning_candidate_fields(state,incoming)
    return None


def initialize_officer_transfer_screen(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_officer_transfer_screen_fields(state,incoming)
    return None


def update_officer_transfer_candidate(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=update_officer_transfer_candidate_fields(state,incoming)
    return None


def initialize_city_transfer_screen(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_city_transfer_screen_fields(state,incoming)
    return None


def initialize_city_transfer_details(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_city_transfer_details_fields(state,incoming)
    return None


def initialize_city_transfer_choices(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_city_transfer_choices_fields(state,incoming)
    return None


def initialize_officer_search_screen(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_officer_search_screen_fields(state,incoming)
    return None


def initialize_officer_search_details(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_officer_search_details_fields(state,incoming)
    return None


def initialize_officer_search_choices(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_officer_search_choices_fields(state,incoming)
    return None


def initialize_support_command_screen(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_support_command_screen_fields(state,incoming)
    return None


def initialize_support_result_screen(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_support_result_screen_fields(state,incoming)
    return None


def initialize_battle_deployment_screen(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_battle_deployment_screen_fields(state,incoming)
    return None


def initialize_battle_order_screen(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_battle_order_screen_fields(state,incoming)
    return None


def continue_campaign_action_display(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=continue_campaign_action_display_fields(state,incoming)
    return None


def initialize_tactical_scene(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_tactical_scene_fields(state,incoming)
    return None


def initialize_tactical_selection_scene(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_tactical_selection_scene_fields(state,incoming)
    return None


def initialize_battle_scene(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_battle_scene_fields(state,incoming)
    return None


def initialize_duel_scene(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_duel_scene_fields(state,incoming)
    return None


def begin_nonreturning_scripted_scene(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=begin_nonreturning_scripted_scene_fields(state,incoming)
    return None


def initialize_campaign_audio_scene(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_campaign_audio_scene_fields(state,incoming)
    return None


def initialize_campaign_status_panel(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_campaign_status_panel_fields(state,incoming)
    return None


def initialize_campaign_summary_panel(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_campaign_summary_panel_fields(state,incoming)
    return None


def return_campaign_idle_slot(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=return_campaign_idle_slot_fields(state,incoming)
    return None


def initialize_training_candidate(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=initialize_training_candidate_fields(state,incoming)
    return None


def dispatch_main_scene_slot(state: SceneState, selector: Word,
        title_literal_marker: Long | None = None):
    """The 60 original BRA slots; out-of-table signed indices stay boundaries."""
    checked_state(state)
    uint(selector, 16)
    from . import business_title
    if selector == 0:
        return process_startup_scene(state)
    if selector == 4:
        return reset_menu_sprite_slots(state)
    if selector == 8:
        if title_literal_marker is None:
            raise Boundary('title literal marker carrier must be supplied')
        return business_title.initialize_title_scene(state, title_literal_marker)
    if selector == 12:
        if title_literal_marker is None:
            raise Boundary('title literal marker carrier must be supplied')
        return business_title.initialize_title_scene_preserving_mode(state, title_literal_marker)
    if selector == 16:
        return business_title.return_title_idle_slot(state)
    if selector == 20:
        return business_title.initialize_secondary_title_scene(state)
    if selector == 24:
        return business_title.initialize_title_transition_scene(state)
    if selector == 28:
        return refresh_information_panel(state)
    if selector == 32:
        return initialize_campaign_screen(state)
    if selector == 36:
        return continue_platform_scene_initialization(state)
    if selector == 40:
        return upload_selected_dictionary_panel(state)
    if selector == 44:
        return initialize_campaign_options(state)
    if selector == 48:
        return initialize_campaign_menu_panels(state)
    if selector == 52:
        return initialize_campaign_command_panel(state)
    if selector == 56:
        return initialize_officer_detail_panel(state)
    if selector == 60:
        return upload_officer_roster_panel(state)
    if selector == 64:
        return initialize_city_detail_panel(state)
    if selector == 68:
        return initialize_city_command_panel(state)
    if selector == 72:
        return upload_formation_caption(state)
    if selector == 76:
        return upload_formation_choice_caption(state)
    if selector == 80:
        return initialize_formation_choices(state)
    if selector == 84:
        return initialize_city_choice_caption(state)
    if selector == 88:
        return request_affordable_action_panel(state)
    if selector == 92:
        return initialize_campaign_map(state)
    if selector == 96:
        return initialize_officer_portrait(state)
    if selector == 100:
        return toggle_officer_roster_selection(state)
    if selector == 104:
        return initialize_education_screen(state)
    if selector == 108:
        return initialize_assignment_description(state)
    if selector == 112:
        return initialize_assignment_choices(state)
    if selector == 116:
        return upload_assignment_caption(state)
    if selector == 120:
        return initialize_training_screen(state)
    if selector == 124:
        return initialize_training_candidate(state)
    if selector == 128:
        return update_training_candidate(state)
    if selector == 132:
        return initialize_learning_screen(state)
    if selector == 136:
        return update_learning_candidate(state)
    if selector == 140:
        return initialize_officer_transfer_screen(state)
    if selector == 144:
        return update_officer_transfer_candidate(state)
    if selector == 148:
        return initialize_city_transfer_screen(state)
    if selector == 152:
        return initialize_city_transfer_details(state)
    if selector == 156:
        return initialize_city_transfer_choices(state)
    if selector == 160:
        return initialize_officer_search_screen(state)
    if selector == 164:
        return initialize_officer_search_details(state)
    if selector == 168:
        return initialize_officer_search_choices(state)
    if selector == 172:
        return initialize_support_command_screen(state)
    if selector == 176:
        return initialize_support_result_screen(state)
    if selector == 180:
        return initialize_battle_deployment_screen(state)
    if selector == 184:
        return initialize_battle_order_screen(state)
    if selector == 188:
        return wait_and_initialize_campaign_action(state)
    if selector == 192:
        return continue_campaign_action_display(state)
    if selector == 196:
        return return_campaign_idle_slot(state)
    if selector == 200:
        return initialize_tactical_scene(state)
    if selector == 204:
        return initialize_tactical_selection_scene(state)
    if selector == 208:
        return initialize_battle_scene(state)
    if selector == 212:
        return initialize_duel_scene(state)
    if selector == 216:
        return initialize_post_duel_campaign(state)
    if selector == 220:
        return begin_nonreturning_scripted_scene(state)
    if selector == 224:
        return initialize_campaign_audio_scene(state)
    if selector == 228:
        return initialize_campaign_status_panel(state)
    if selector == 232:
        return initialize_campaign_summary_panel(state)
    if selector == 236:
        return upload_three_formation_names(state)
    return _tick(state, u32(0x3D8 + s16(selector)))


def read_selected_formation_preferences(state: SceneState, retained_mask: Long=0, retained_index: Long=0):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=retained_mask, target_y=retained_index)
    observed=read_selected_formation_preferences_fields(state,incoming)
    return None


def find_first_enabled_formation(state: SceneState, mask: Long, retained_index: Long=0) -> FormationBitResult:
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=mask, target_y=retained_index)
    observed=find_first_enabled_formation_fields(state,incoming)
    return FormationBitResult(mask=observed.target_x, index=observed.target_y)


def load_city_formation_preferences(state: SceneState):
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=load_city_formation_preferences_fields(state,incoming)
    return None


def calculate_action_budget(state: SceneState) -> Long:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=calculate_action_budget_fields(state,entered)
    return returned.target_x



def advance_unselected_roster_cursor(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=advance_unselected_roster_cursor_fields(state,entered)
    return None



def update_campaign_control(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=update_campaign_control_fields(state,entered)
    return None







def advance_campaign_world_tick(state: SceneState, frame: MapTickFrame) -> MapTickFrame:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=_campaign_legacy_observations_fields(state,frame,'world')
    returned=update_campaign_control_fields(state,entered)
    return replace(frame,motion_x=returned.target_x,motion_y=returned.target_y,attributes=returned.unit,tile_count=returned.count,officer=returned.distance,count=returned.offset_x,index=returned.offset_y,control_latch=returned.choice,source=returned.roster,destination=returned.candidates,packet=returned.controller,vdp_port=returned.auxiliary,stack_cursor=returned.stack_cursor,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2))



def advance_campaign_palette_transition(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=advance_campaign_palette_transition_fields(state,entered)
    return None



def process_campaign_mode_control(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=process_campaign_mode_control_fields(state,entered)
    return None



def detect_unassigned_packed_leaders(state: SceneState, retained_selection: Long=0) -> CarryOutcome:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    if retained_selection is not None:
        uint(retained_selection,32)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=retained_selection)
    returned=detect_unassigned_packed_leaders_fields(state,entered)
    return CarryOutcome(bool(returned.status&1),returned.target_x)



def detect_unassigned_leader_roster(state: SceneState, retained_selection: Long=0) -> CarryOutcome:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    if retained_selection is not None:
        uint(retained_selection,32)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=retained_selection)
    returned=detect_unassigned_leader_roster_fields(state,entered)
    return CarryOutcome(bool(returned.status&1),returned.target_x)



def scan_unassigned_leader_roster(state: SceneState, retained_selection: Long) -> LeaderRosterDetection:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    if retained_selection is not None:
        uint(retained_selection,32)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=retained_selection)
    returned=detect_unassigned_leader_roster_fields(state,entered)
    return LeaderRosterDetection(returned.target_x,low16(returned.target_y),state.table_at(returned.roster.base),state.table_at(returned.candidates.base),bool(returned.status&1),bool(returned.status&4),bool(returned.status&8),bool(returned.status&2))



def update_outside_map_indicator(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=update_outside_map_indicator_fields(state,entered)
    return None



def move_campaign_map_pointer(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=move_campaign_map_pointer_fields(state,entered)
    return None



def clear_pointer_cost_caches(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=clear_pointer_cost_caches_fields(state,entered)
    return None



def draw_campaign_pointer_marker(state: SceneState, retained_x: Long | None=None, retained_y: Long | None=None, retained_attributes: Long | None=None):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    if retained_x is not None:
        uint(retained_x,32)
    if retained_y is not None:
        uint(retained_y,32)
    if retained_attributes is not None:
        uint(retained_attributes,32)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=retained_x,target_y=retained_y,unit=retained_attributes)
    returned=draw_campaign_pointer_marker_fields(state,entered)
    return MapSpriteResult(returned.roster,returned.target_x,returned.target_y,returned.unit).validate(state)




def draw_campaign_pointer_fields(state: SceneState) -> CampaignPointerFields:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=draw_campaign_pointer_marker_fields(state,entered)
    return CampaignPointerFields(returned.roster,low16(returned.target_x),low16(returned.target_y),low16(returned.unit),bool(returned.status&1),bool(returned.status&4),bool(returned.status&8),bool(returned.status&2)).validate(state)



def detect_unlisted_campaign_owner(state: SceneState, retained_owner: Long=0) -> CarryOutcome:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    if retained_owner is not None:
        uint(retained_owner,32)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=retained_owner)
    returned=detect_unlisted_campaign_owner_fields(state,entered)
    return CarryOutcome(bool(returned.status&1),returned.target_x)





def compare_campaign_owner_list(state: SceneState, retained_owner: Long) -> CampaignOwnerDetection:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    if retained_owner is not None:
        uint(retained_owner,32)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=retained_owner)
    returned=detect_unlisted_campaign_owner_fields(state,entered)
    return CampaignOwnerDetection(returned.target_x,bool(returned.status&1),bool(returned.status&4),bool(returned.status&8),bool(returned.status&2))



def advance_campaign_entry_fade(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=advance_campaign_entry_fade_fields(state,entered)
    return None



def process_campaign_location_choice(state: SceneState, *, location_inputs: LocationChoiceInput | None=None) -> LocationChoiceResult:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=_campaign_legacy_observations_fields(state,location_inputs,'location_input')
    returned=process_campaign_location_choice_fields(state,entered)
    result=replace(location_inputs.frame,motion_value=returned.target_x,prompt_field=returned.target_y,sprite_attributes=returned.unit,sprite_source=returned.roster,palette_source=returned.candidates,vdp_port=returned.auxiliary,stack_cursor=returned.stack_cursor,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2))
    return LocationChoiceResult(result)



def select_campaign_location(state: SceneState, *, current_frame: LocationChoiceFrame | None=None) -> LocationChoiceFrame:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=_campaign_legacy_observations_fields(state,current_frame,'location')
    returned=select_campaign_location_fields(state,entered)
    result=replace(current_frame,motion_value=returned.target_x,prompt_field=returned.target_y,sprite_attributes=returned.unit,sprite_source=returned.roster,palette_source=returned.candidates,vdp_port=returned.auxiliary,stack_cursor=returned.stack_cursor,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2))
    return result





def clamp_campaign_camera_targets(state: SceneState, *, current_frame: LocationChoiceFrame | None=None) -> LocationChoiceFrame:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=_campaign_legacy_observations_fields(state,current_frame,'location')
    returned=clamp_campaign_camera_targets_fields(state,entered)
    result=replace(current_frame,motion_value=returned.target_x,prompt_field=returned.target_y,sprite_attributes=returned.unit,sprite_source=returned.roster,palette_source=returned.candidates,vdp_port=returned.auxiliary,stack_cursor=returned.stack_cursor,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2))
    return result



def wait_for_campaign_location_confirmation(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=wait_for_campaign_location_confirmation_fields(state,entered)
    return None



def process_campaign_camera_transition(state: SceneState, *, transition_inputs: CameraTransitionInput | None=None) -> CameraTransitionResult:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=_campaign_legacy_observations_fields(state,transition_inputs,'transition')
    returned=process_campaign_camera_transition_fields(state,entered)
    return CameraTransitionResult(value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,member=returned.offset_y,remaining=returned.choice,destination=returned.roster,source=returned.candidates,descriptor=returned.controller,records=returned.scan,palette=returned.opponent,roster=returned.scratch,stack_cursor=returned.stack_cursor,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2))



def scroll_campaign_camera_toward_pointer(state: SceneState, retained_flag: Long=0, *, camera_inputs: CameraMotionInput | None=None) -> Long:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    if retained_flag is not None:
        uint(retained_flag,32)
    entered=_campaign_legacy_observations_fields(state,camera_inputs,'camera')
    returned=scroll_campaign_camera_toward_pointer_fields(state,entered)
    return returned.target_x



def dispatch_campaign_selection_phase(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=dispatch_campaign_selection_phase_fields(state,entered)
    return None



def queue_campaign_selection_refresh(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=queue_campaign_selection_refresh_fields(state,entered)
    return None



def prepare_campaign_selection_mode(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=prepare_campaign_selection_mode_fields(state,entered)
    return None



def advance_campaign_selection_phase(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=advance_campaign_selection_phase_fields(state,entered)
    return None



def initialize_campaign_selection_mode(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=initialize_campaign_selection_mode_fields(state,entered)
    return None





def append_campaign_selection_frame(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=append_campaign_selection_frame_fields(state,entered)
    return None



def update_campaign_selection_delay(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=update_campaign_selection_delay_fields(state,entered)
    return None



def process_campaign_selection_input(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=process_campaign_selection_input_fields(state,entered)
    return None



def validate_campaign_roster_action(state: SceneState) -> CarryOutcome:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=validate_campaign_roster_action_fields(state,entered)
    return CarryOutcome(bool(returned.status&1),None)



def expire_campaign_selection_frame(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=expire_campaign_selection_frame_fields(state,entered)
    return None



def append_campaign_frame_progress(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=append_campaign_frame_progress_fields(state,entered)
    return None



def advance_campaign_frame_phase(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=advance_campaign_frame_phase_fields(state,entered)
    return None



def append_campaign_confirmation_frame(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=append_campaign_confirmation_frame_fields(state,entered)
    return None



def refresh_campaign_confirmation(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=refresh_campaign_confirmation_fields(state,entered)
    return None



def finish_campaign_selection(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=finish_campaign_selection_fields(state,entered)
    return None









def process_campaign_roster_commands(state: SceneState, input_state: RosterInput):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    if type(input_state) is not RosterInput:
        raise ValueError("actual historical roster observation required")
    input_state.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=input_state.selection)
    returned=process_campaign_roster_commands_fields(state,entered)
    return None



def trigger_campaign_selection_audio(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=trigger_campaign_selection_audio_fields(state,entered)
    return None



def update_campaign_selection_audio(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=update_campaign_selection_audio_fields(state,entered)
    return None



def animate_campaign_selection_glyph(state: SceneState, retained_foreground: Long=0, retained_tile: Long=0):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    if retained_foreground is not None:
        uint(retained_foreground,32)
    if retained_tile is not None:
        uint(retained_tile,32)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_y=retained_foreground,unit=retained_tile)
    returned=animate_campaign_selection_glyph_fields(state,entered)
    return None



def announce_selected_assignment(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=announce_selected_assignment_fields(state,entered)
    return None



def initialize_assignment_confirmation(state: SceneState, retained_foreground: Long=0, retained_tile: Long=0):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    if retained_foreground is not None:
        uint(retained_foreground,32)
    if retained_tile is not None:
        uint(retained_tile,32)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_y=retained_foreground,unit=retained_tile)
    returned=initialize_assignment_confirmation_fields(state,entered)
    return None



def process_assignment_confirmation_input(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=process_assignment_confirmation_input_fields(state,entered)
    return None



def upload_assignment_confirmation_glyph(state: SceneState, retained_foreground: Long=0, retained_tile: Long=0):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    if retained_foreground is not None:
        uint(retained_foreground,32)
    if retained_tile is not None:
        uint(retained_tile,32)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_y=retained_foreground,unit=retained_tile)
    returned=upload_assignment_confirmation_glyph_fields(state,entered)
    return None



def remove_selected_assignment(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=remove_selected_assignment_fields(state,entered)
    return None



def process_campaign_exit_input(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=process_campaign_exit_input_fields(state,entered)
    return None



def dispatch_campaign_post_selection_phase(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=dispatch_campaign_post_selection_phase_fields(state,entered)
    return None



def draw_campaign_fade_marker(state: SceneState, retained_x: Long=0, retained_y: Long=0, retained_attributes: Long=0):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    if retained_x is not None:
        uint(retained_x,32)
    if retained_y is not None:
        uint(retained_y,32)
    if retained_attributes is not None:
        uint(retained_attributes,32)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=retained_x,target_y=retained_y,unit=retained_attributes)
    returned=draw_campaign_fade_marker_fields(state,entered)
    return MapSpriteResult(returned.roster,returned.target_x,returned.target_y,returned.unit).validate(state)



def dispatch_campaign_subcommand_phase(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=dispatch_campaign_subcommand_phase_fields(state,entered)
    return None



def update_personnel_command_phase(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=update_personnel_command_phase_fields(state,entered)
    return None



def update_city_command_phase(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=update_city_command_phase_fields(state,entered)
    return None



def update_support_command_phase(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=update_support_command_phase_fields(state,entered)
    return None



def update_tactical_command_phase(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=update_tactical_command_phase_fields(state,entered)
    return None



def update_battle_command_phase(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=update_battle_command_phase_fields(state,entered)
    return None



def exit_post_campaign_message(state: SceneState):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=exit_post_campaign_message_fields(state,entered)
    return None



def dismiss_campaign_warning(state: SceneState, retained_foreground: Long=0, retained_tile: Long=0):
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    if retained_foreground is not None:
        uint(retained_foreground,32)
    if retained_tile is not None:
        uint(retained_tile,32)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_y=retained_foreground,unit=retained_tile)
    returned=dismiss_campaign_warning_fields(state,entered)
    return None



def _dispatch_campaign_handler(state, target):
    """Named handler selection using actual live table targets, not a PC engine."""
    uint(target, 32)
    if target == 0xF98:
        return advance_campaign_palette_transition(state)
    if target == 0x10DC:
        return process_campaign_mode_control(state)
    if target == 0x11A6:
        return detect_unassigned_packed_leaders(state)
    if target == 0x11EE:
        return detect_unassigned_leader_roster(state)
    if target == 0x1228:
        return update_outside_map_indicator(state)
    if target == 0x1290:
        return move_campaign_map_pointer(state)
    if target == 0x133A:
        return clear_pointer_cost_caches(state)
    if target == 0x1344:
        return draw_campaign_pointer_fields(state)
    if target == 0x13DC:
        return detect_unlisted_campaign_owner(state)
    if target == 0x1406:
        return detect_uniform_campaign_owner(state)
    if target == 0x1444:
        return advance_campaign_entry_fade(state)
    if target == 0x14E0:
        return process_campaign_location_choice(state)
    if target == 0x157A:
        return select_campaign_location(state)
    if target == 0x15BE:
        return clamp_campaign_camera_targets(state)
    if target == 0x15FC:
        return wait_for_campaign_location_confirmation(state)
    if target == 0x161E:
        return process_campaign_camera_transition(state)
    if target == 0x16B4:
        return scroll_campaign_camera_toward_pointer(state)
    if target == 0x1798:
        return dispatch_campaign_selection_phase(state)
    if target == 0x17FA:
        return queue_campaign_selection_refresh(state)
    if target == 0x1806:
        return prepare_campaign_selection_mode(state)
    if target == 0x189E:
        return advance_campaign_selection_phase(state)
    if target == 0x18A4:
        return initialize_campaign_selection_mode(state)
    if target == 0x1974:
        return append_campaign_selection_frame(state)
    if target == 0x19CC:
        return update_campaign_selection_delay(state)
    if target == 0x1A70:
        return process_campaign_selection_input(state)
    if target == 0x1C12:
        return validate_campaign_roster_action(state)
    if target == 0x1CFA:
        return expire_campaign_selection_frame(state)
    if target == 0x1D18:
        return append_campaign_frame_progress(state)
    if target == 0x1D5E:
        return advance_campaign_frame_phase(state)
    if target == 0x1D64:
        return append_campaign_confirmation_frame(state)
    if target == 0x1DCE:
        return refresh_campaign_confirmation(state)
    if target == 0x1DD6:
        return finish_campaign_selection(state)
    if target == 0x1DE8:
        raise Boundary('campaign roster handler requires actual RosterInput carrier')
    if target == 0x2004:
        return trigger_campaign_selection_audio(state)
    if target == 0x202A:
        return update_campaign_selection_audio(state)
    if target == 0x2050:
        return animate_campaign_selection_glyph(state)
    if target == 0x20B8:
        return announce_selected_assignment(state)
    if target == 0x20F0:
        return initialize_assignment_confirmation(state)
    if target == 0x2168:
        return process_assignment_confirmation_input(state)
    if target == 0x21BC:
        return upload_assignment_confirmation_glyph(state)
    if target == 0x21F2:
        return remove_selected_assignment(state)
    if target == 0x222E:
        return process_campaign_exit_input(state)
    if target == 0x224E:
        return dispatch_campaign_post_selection_phase(state)
    if target == 0x23F6:
        return draw_campaign_fade_marker(state)
    if target == 0x2416:
        return dispatch_campaign_subcommand_phase(state)
    if target == 0x36DC:
        return update_personnel_command_phase(state)
    if target == 0x36F0:
        return update_city_command_phase(state)
    if target == 0x36FE:
        return update_support_command_phase(state)
    if target == 0x370C:
        return update_tactical_command_phase(state)
    if target == 0x371A:
        return update_battle_command_phase(state)
    if target == 0x3728:
        return exit_post_campaign_message(state)
    if target == 0x3740:
        return dismiss_campaign_warning(state)
    return _tick(state, target)


def detect_uniform_campaign_owner(state: SceneState, retained_owner: Long=0) -> CarryOutcome:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    if retained_owner is not None:
        uint(retained_owner,32)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=retained_owner)
    returned=detect_uniform_campaign_owner_fields(state,entered)
    return CarryOutcome(bool(returned.status&1),returned.target_x)





def advance_campaign_camera_motion(state: SceneState, inputs: CameraMotionInput) -> CameraMotionResult:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=_campaign_legacy_observations_fields(state,inputs,'camera')
    returned=scroll_campaign_camera_toward_pointer_fields(state,entered)
    return CameraMotionResult(value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,member=returned.offset_y,remaining=returned.choice,destination=returned.roster,source=returned.candidates,descriptor=returned.controller,records=returned.scan,palette=returned.opponent,roster=returned.scratch,stack_cursor=returned.stack_cursor,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2))


def draw_campaign_camera_pointer(state: SceneState, inputs: CameraMotionInput) -> CameraMotionInput:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=_campaign_legacy_observations_fields(state,inputs,'camera')
    returned=draw_campaign_pointer_marker_fields(state,entered)
    return replace(inputs,value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,member=returned.offset_y,remaining=returned.choice,destination=returned.roster,source=returned.candidates,descriptor=returned.controller,records=returned.scan,palette=returned.opponent,roster=returned.scratch,stack_cursor=returned.stack_cursor)




def advance_campaign_camera_transition(state: SceneState, inputs: CameraTransitionInput) -> CameraTransitionResult:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=_campaign_legacy_observations_fields(state,inputs,'transition')
    returned=process_campaign_camera_transition_fields(state,entered)
    return CameraTransitionResult(value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,member=returned.offset_y,remaining=returned.choice,destination=returned.roster,source=returned.candidates,descriptor=returned.controller,records=returned.scan,palette=returned.opponent,roster=returned.scratch,stack_cursor=returned.stack_cursor,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2))



def upload_officer_roster_panel_frame(state: SceneState, inputs: RosterPanelInput) -> RosterPanelResult:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    from .contexts_display_fields import display_legacy_frame_fields
    entered = display_legacy_frame_fields(state, inputs, 21478)
    return upload_officer_roster_panel_frame_fields(state, entered)

def _decode_roster_panel_glyphs(state: SceneState, frame: CommandLabelFrame, source: Cursor, rows: Long) -> CommandLabelFrame:
    from .contexts_display_fields import display_legacy_frame_fields
    return display_legacy_frame_fields(state, None, 44682)




def advance_campaign_location_choice(state: SceneState, inputs: LocationChoiceInput) -> LocationChoiceResult:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=_campaign_legacy_observations_fields(state,inputs,'location_input')
    returned=process_campaign_location_choice_fields(state,entered)
    result=replace(inputs.frame,motion_value=returned.target_x,prompt_field=returned.target_y,sprite_attributes=returned.unit,sprite_source=returned.roster,palette_source=returned.candidates,vdp_port=returned.auxiliary,stack_cursor=returned.stack_cursor,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2))
    return LocationChoiceResult(result)



def select_campaign_location_frame(state: SceneState, frame: LocationChoiceFrame) -> LocationChoiceFrame:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=_campaign_legacy_observations_fields(state,frame,'location')
    returned=select_campaign_location_fields(state,entered)
    result=replace(frame,motion_value=returned.target_x,prompt_field=returned.target_y,sprite_attributes=returned.unit,sprite_source=returned.roster,palette_source=returned.candidates,vdp_port=returned.auxiliary,stack_cursor=returned.stack_cursor,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2))
    return result



def clamp_campaign_camera_target_frame(state: SceneState, frame: LocationChoiceFrame) -> LocationChoiceFrame:
    """Historical observations call the one complete core; unknown full ABI stays unknown."""
    checked_state(state)
    entered=_campaign_legacy_observations_fields(state,frame,'location')
    returned=clamp_campaign_camera_targets_fields(state,entered)
    result=replace(frame,motion_value=returned.target_x,prompt_field=returned.target_y,sprite_attributes=returned.unit,sprite_source=returned.roster,palette_source=returned.candidates,vdp_port=returned.auxiliary,stack_cursor=returned.stack_cursor,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2))
    return result


from .contexts_gameplay import (FirstDeploymentFrame, FirstDeploymentReturnBoundary,
    MovementContinuationBoundary, first_replace)
from .business_movement_support import (_movement_frame, _movement_move, _movement_move_long,
    _movement_test, _movement_compare, _movement_binary_flags, _movement_fixed_shift_word,
    _movement_arithmetic_long, _movement_multiply_word, _movement_divu_word)
from .business_commands import (_city_ui_frame_fields, _city_ui_store_fields, _city_ui_append_fields,
    _city_ui_arithmetic_fields, _city_ui_memory_arithmetic_fields, _city_ui_bit_fields, _city_ui_shift_fields)


def _campaign_emit_fields(state: SceneState, frame: FirstDeploymentFrame,
        instruction: int, address: int, value: int, size: int=2,
        clear: bool=False) -> FirstDeploymentFrame:
    """Use the real existing RAM/hardware bus; missing hardware stops at the actual write."""
    try:
        return _city_ui_store_fields(state,frame,address,value,size,clear)
    except Boundary:
        raise MovementContinuationBoundary(instruction,frame,'actual campaign DATA access unavailable')


def _campaign_memory_logic_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, mask: int, operation: str, size: int=2) -> FirstDeploymentFrame:
    """The three real logical RMW roles preserve X and use their original DATA width."""
    value=state.read(address,size)
    if operation=='and':
        value&=mask
    elif operation=='or':
        value|=mask
    elif operation=='xor':
        value^=mask
    else:
        raise ValueError('original campaign AND/OR/XOR role required')
    return _city_ui_store_fields(state,frame,address,value,size)


def _campaign_carry_fields(state: SceneState, frame: FirstDeploymentFrame,
        carry: bool) -> FirstDeploymentFrame:
    """Original ORI/ANDI SR carry-only results retain the actual other SR/CCR bits."""
    status=(frame.status|1) if carry else (frame.status&30)
    state.sr=(state.sr&65504)|status
    return first_replace(frame,status=status)


def _campaign_clear_bit_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, bit: int) -> FirstDeploymentFrame:
    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
    from ..high_level_gameplay_flow.business_services import _scene_refresh_bit_clear
    return _scene_refresh_bit_clear(SceneRefreshMemory(state),frame,address,bit)


def _campaign_long_shift_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, amount: int, right: bool=False) -> FirstDeploymentFrame:
    """Reuse actual long-shift primitives for the closed campaign #1/#2/#3 forms."""
    if amount not in (1,2,3):
        raise ValueError('closed original campaign LONG shift required')
    if right:
        from ..high_level_remaining_flows.business_city import _recruitment_right_long
        if amount==2:
            frame=_recruitment_right_long(state,frame,name,1)
            return _recruitment_right_long(state,frame,name,1)
        return _recruitment_right_long(state,frame,name,amount)
    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
    from ..high_level_scene_flows.business_scene import _glyph_shift_long_fields
    return _glyph_shift_long_fields(SceneRefreshMemory(state),frame,name,amount)


def _campaign_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Real physical call/RTS pair; its sole known-child routing is installed from the closed scope."""
    if target in (0x676F2,0x26BFA,0xAC08,0xA3DA,0xDEA6):
        from ..high_level_remaining_flows.business_city import _deployment_menu_call_fields
        return _deployment_menu_call_fields(state,frame,target,continuation)
    stack=frame.stack_cursor.advance(-4)
    stack.set_long(0,continuation)
    entered=first_replace(frame,stack_cursor=stack)
    returned=_campaign_known_child_fields(state,entered,target)
    returned=_city_ui_frame_fields(state,returned,target)
    actual=returned.stack_cursor.long()
    if actual!=continuation:
        raise FirstDeploymentReturnBoundary(actual,returned,continuation)
    return first_replace(returned,stack_cursor=returned.stack_cursor.advance(4))


def _campaign_tail_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int) -> FirstDeploymentFrame:
    """A real BRA/JMP reuses the incoming caller LONG; no fictional alias BSR slot."""
    return _campaign_known_child_fields(state,frame,target)


def toggle_officer_roster_selection_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """43C/982: original roster selection capacity, toggle and real glyph/video update."""
    frame=_city_ui_frame_fields(state,frame,0x43C)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_movement_move(state,frame,'target_x',1,16)
    frame=_movement_move(state,frame,'target_y',3,16)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF378,2),16)
    frame=_city_ui_shift_fields(state,frame,'unit',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF4FE).cursor())
    frame=_movement_move(state,frame,'count',frame.roster.word(low16(frame.unit)),16)
    frame=_movement_move(state,frame,'count',low16(frame.count)&255,16)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFCD00).cursor())
    frame=_movement_test(state,frame,frame.candidates.byte(low16(frame.count)),8)
    if not frame.status&4:
        frame=_movement_compare(state,frame,frame.candidates.byte(low16(frame.count)),1,8)
        if not frame.status&4:
            frame=_city_ui_store_fields(state,frame,0xFFFFF3A6,low16(frame.count))
            frame=_city_ui_store_fields(state,frame,0xFFFFF362,16)
        return frame
    frame=_movement_compare(state,frame,frame.roster.word(low16(frame.unit)),0x4000,16)
    if frame.status&1:
        frame=_movement_move(state,frame,'distance',state.read(0xFFFFF684,2),16)
        frame=_movement_compare(state,frame,low16(frame.distance),state.read(0xFFFFF686,2),16)
        if not frame.status&1:
            return frame
        frame=_movement_move(state,frame,'target_y',2,16)
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF684,1)
    else:
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF684,1,True)
    frame=_campaign_memory_logic_fields(state,frame,u32(frame.roster.base+s16(low16(frame.unit))),0x4000,'xor')
    frame=first_replace(frame,roster=state.table_at(0x8A504).cursor())
    frame=_movement_move(state,frame,'distance',low16(frame.count),16)
    frame=_city_ui_shift_fields(state,frame,'count',1)
    frame=_city_ui_arithmetic_fields(state,frame,'count',low16(frame.distance))
    frame=_city_ui_shift_fields(state,frame,'count',1)
    frame=first_replace(frame,roster=frame.roster.advance(s16(low16(frame.count))),candidates=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'count',2,16)
    frame=_campaign_call_fields(state,frame,0xAE8A,0x9F4)
    frame=_movement_move(state,frame,'target_x',0xCC80,16)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF378,2),16)
    frame=_city_ui_shift_fields(state,frame,'target_y',1)
    frame=_city_ui_arithmetic_fields(state,frame,'target_y',state.read(0xFFFFF378,2))
    frame=_city_ui_shift_fields(state,frame,'target_y',7)
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',low16(frame.target_y))
    frame=_movement_move_long(state,frame,'target_y',0)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame=_campaign_long_shift_fields(state,frame,'target_y',2)
    frame=_movement_fixed_shift_word(state,frame,'target_y',2,True)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_y)|0x4000,16)
    frame=_movement_move_long(state,frame,'target_y',swap_words(frame.target_y))
    frame=_campaign_emit_fields(state,frame,0xA14,0xC00004,frame.target_y,4)
    frame=_movement_move(state,frame,'offset_x',95,16)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())
    while True:
        value=frame.candidates.long()
        frame=first_replace(frame,candidates=frame.candidates.advance(4))
        frame=_campaign_emit_fields(state,frame,0xA22,0xC00000,value,4)
        frame=first_replace(frame,offset_x=replace_word(frame.offset_x,u16(low16(frame.offset_x)-1)))
        if low16(frame.offset_x)==65535:
            break
    return _campaign_call_fields(state,frame,0xA4A,0xA30)


def calculate_action_budget_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """8E6: path-derived action budget with original rounding and twenty-five scaling."""
    frame=_city_ui_frame_fields(state,frame,0x8E6)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3AE,2),16)
    frame=_city_ui_shift_fields(state,frame,'target_x',2)
    frame=first_replace(frame,roster=state.table_at(0xD4AC6).cursor())
    for index,destination in ((0,0xFFFFF63E),(2,0xFFFFF63C)):
        frame=_city_ui_store_fields(state,frame,destination,frame.roster.word(low16(frame.target_x),index))
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_city_ui_shift_fields(state,frame,'target_x',2)
    for index,destination in ((0,0xFFFFF642),(2,0xFFFFF640)):
        frame=_city_ui_store_fields(state,frame,destination,frame.roster.word(low16(frame.target_x),index))
    frame=_campaign_call_fields(state,frame,0x6518,0x916)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC400).cursor())
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
    frame=_movement_move_long(state,frame,'target_x',0)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF644,2),16)
    frame=_city_ui_shift_fields(state,frame,'target_x',2)
    frame=_movement_divu_word(state,frame,'target_x',low16(frame.target_y),0x92C)
    frame=_movement_move_long(state,frame,'target_x',swap_words(frame.target_x))
    frame=_movement_test(state,frame,low16(frame.target_x),16)
    if not frame.status&4:
        frame=_movement_arithmetic_long(state,frame,'target_x',0x10000)
    frame=_movement_move_long(state,frame,'target_x',swap_words(frame.target_x))
    frame=_movement_multiply_word(state,frame,'target_x',low16(frame.target_x))
    frame=_movement_move_long(state,frame,'target_y',frame.target_x)
    frame=_campaign_long_shift_fields(state,frame,'target_x',1)
    frame=_movement_arithmetic_long(state,frame,'target_x',frame.target_y)
    frame=_campaign_long_shift_fields(state,frame,'target_x',3)
    frame=_movement_arithmetic_long(state,frame,'target_x',frame.target_y)
    return _campaign_long_shift_fields(state,frame,'target_x',2,True)


def advance_unselected_roster_cursor_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A4A: actual selected-count check, packet sentinel and bit14/byte-bit6 skip rules."""
    frame=_city_ui_frame_fields(state,frame,0xA4A)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF4FE).cursor())
    frame=_movement_move(state,frame,'distance',state.read(0xFFFFF686,2),16)
    frame=_movement_compare(state,frame,low16(frame.distance),state.read(0xFFFFF684,2),16)
    exhausted=bool(frame.status&4)
    if not exhausted:
        frame=_movement_move(state,frame,'offset_x',2,16)
        while True:
            frame=_movement_move(state,frame,'offset_y',frame.roster.word(low16(frame.offset_x)),16)
            if frame.status&8:
                exhausted=True
                break
            frame=_city_ui_bit_fields(state,frame,frame.offset_y,14)
            if frame.status&4:
                break
            frame=_city_ui_arithmetic_fields(state,frame,'offset_x',2)
    if exhausted:
        frame=_city_ui_store_fields(state,frame,0xFFFFF378,state.read(0xFFFFF636,2))
        return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF378,1)
    frame=_movement_move(state,frame,'offset_x',state.read(0xFFFFF378,2),16)
    frame=_city_ui_shift_fields(state,frame,'offset_x',1)
    frame=_city_ui_arithmetic_fields(state,frame,'offset_x',2)
    frame=_movement_move(state,frame,'distance',state.read(0xFFFFF636,2),16)
    frame=_city_ui_shift_fields(state,frame,'distance',1)
    while True:
        frame=_movement_compare(state,frame,low16(frame.offset_x),low16(frame.distance),16)
        if not frame.status&5:
            frame=_city_ui_store_fields(state,frame,0xFFFFF378,state.read(0xFFFFF636,2))
            return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF378,1)
        frame=_city_ui_bit_fields(state,frame,frame.roster.byte(low16(frame.offset_x)),6)
        if frame.status&4:
            frame=_movement_fixed_shift_word(state,frame,'offset_x',1,True)
            return _city_ui_store_fields(state,frame,0xFFFFF378,low16(frame.offset_x))
        frame=_city_ui_arithmetic_fields(state,frame,'offset_x',2)


def update_campaign_control_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F10: real input/palette service calls, video command, live phase table and marker gates."""
    frame=_city_ui_frame_fields(state,frame,0xF10)
    frame=_campaign_call_fields(state,frame,0x4890,0xF16)
    frame=_campaign_call_fields(state,frame,0x4998,0xF1C)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF606,2),16)
    frame=_movement_move(state,frame,'target_x',low8(frame.target_x)|64,8)
    frame=_campaign_emit_fields(state,frame,0xF24,0xC00004,low16(frame.target_x))
    frame=_campaign_call_fields(state,frame,0xA370,0xF30)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF612,2),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&255,16)
    frame=_city_ui_shift_fields(state,frame,'target_x',1)
    frame=_movement_move(state,frame,'target_x',state.read(u32(0xF78+s16(low16(frame.target_x))),2),16)
    frame=first_replace(frame,roster=state.table_at(0xF98).cursor())
    frame=_campaign_call_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),0xF48)
    frame=_movement_test(state,frame,state.read(0xFFFFF6C4,2),16)
    if not frame.status&4:
        return frame
    frame=_movement_compare(state,frame,state.read(0xFFFFF612,2),0x200,16)
    if frame.status&4:
        frame=_movement_compare(state,frame,state.read(0xFFFFF352,2),16,16)
        if frame.status&1:
            return frame
    for target,continuation in ((0x15DE6,0xF6A),(0x169AA,0xF70),(0x679FC,0xF76)):
        frame=_campaign_call_fields(state,frame,target,continuation)
    return frame


def _campaign_notice_fields(state: SceneState, frame: FirstDeploymentFrame,
        message: int, continuation: int) -> FirstDeploymentFrame:
    frame=_movement_move(state,frame,'target_x',message,16)
    return _campaign_call_fields(state,frame,0x676F2,continuation)


def advance_campaign_palette_transition_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """F98: original multi-stage palette transition and subsequent campaign mode choice."""
    frame=_city_ui_frame_fields(state,frame,0xF98)
    frame=_movement_compare(state,frame,state.read(0xFFFFF352,2),16,16)
    if frame.status&1:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF352,2),16)
        frame=_movement_move(state,frame,'target_y',64,16)
        frame=first_replace(frame,roster=state.table_at(0xFFFFFB80).cursor())
        frame=_campaign_call_fields(state,frame,0xDEA6,0xFB4)
        frame=_movement_test(state,frame,state.read(0xFFFFF77A,2),16)
        if not frame.status&4:
            frame=_campaign_call_fields(state,frame,0x23F6,0xFC0)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF320,2),16)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&1,16)
        if frame.status&4:
            frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF352,1)
        return frame
    if frame.status&4:
        frame=_city_ui_store_fields(state,frame,0xFFFFF600,8)
        frame=_city_ui_store_fields(state,frame,0xFFFFF77A,0,2,True)
        frame=_movement_compare(state,frame,state.read(0xFFFFF764,1),0x84,8)
        if not frame.status&4:
            frame=_movement_move(state,frame,'target_x',0x84,8)
            frame=_city_ui_store_fields(state,frame,0xFFFFF764,low8(frame.target_x),1)
            frame=_campaign_call_fields(state,frame,0x808A,0xFFC)
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF352,1)
        frame=_city_ui_store_fields(state,frame,0xFFFFEFC8,0,4,True)
        return _city_ui_store_fields(state,frame,0xFFFFEFCC,0,4,True)
    frame=_movement_move(state,frame,'target_x',31,16)
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',state.read(0xFFFFF352,2),True)
    frame=_movement_move(state,frame,'target_y',64,16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFFB80).cursor())
    frame=_campaign_call_fields(state,frame,0xDEA6,0x1022)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF320,2),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&1,16)
    if not frame.status&4:
        return frame
    frame=_campaign_call_fields(state,frame,0xA3DA,0x1034)
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF352,1)
    frame=_movement_compare(state,frame,state.read(0xFFFFF352,2),32,16)
    if frame.status&1:
        return frame
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF3A5,1),0)
    if frame.status&4:
        frame=_movement_test(state,frame,state.read(0xFFFFAFFE,2),16)
        if frame.status&4:
            frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF612,1)
            frame=_movement_compare(state,frame,state.read(0xFFFFF36C,2),1,16)
            if frame.status&4:
                frame=_city_ui_store_fields(state,frame,0xFFFFF600,52)
            return frame
        frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x20E)
        frame=_movement_move(state,frame,'target_x',194,16)
        frame=_movement_compare(state,frame,state.read(0xFFFFAFFE,2),1,16)
        if not frame.status&4:
            frame=_city_ui_arithmetic_fields(state,frame,'target_x',1)
        return _campaign_call_fields(state,frame,0x676F2,0x10BE)
    for value in (6,15,21):
        frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),value,16)
        if frame.status&4:
            frame=_campaign_call_fields(state,frame,0xC11E,0x10C8)
            for address,value in ((0xFFFFF612,0x208),(0xFFFFF362,3),(0xFFFFF36A,18)):
                frame=_city_ui_store_fields(state,frame,address,value)
            return frame
    return _campaign_reset_selection_fields(state,frame)


def _campaign_reset_selection_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """The original common mode reset tail has no separate call/return token."""
    frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x206)
    frame=_city_ui_store_fields(state,frame,0xFFFFF362,0,2,True)
    frame=_city_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)
    return _city_ui_store_fields(state,frame,0xFFFFF368,0)


def detect_unassigned_packed_leaders_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """11A6: two packed leader bytes, actual negative-city ownership test and carry-only result."""
    frame=_city_ui_frame_fields(state,frame,0x11A6)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFA622,2),16)
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'target_y',low8(frame.target_x),8)
    frame=_movement_fixed_shift_word(state,frame,'target_x',8,True)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFCC00).cursor(),roster=state.table_at(0xFFFFE640).cursor())
    frame=_city_ui_shift_fields(state,frame,'target_x',1)
    frame=_movement_move(state,frame,'unit',frame.roster.word(low16(frame.target_x)),16)
    frame=_movement_compare(state,frame,frame.candidates.byte(low16(frame.unit)),255,8)
    if not frame.status&4:
        frame=_city_ui_shift_fields(state,frame,'target_y',1)
        frame=_movement_move(state,frame,'unit',frame.roster.word(low16(frame.target_y)),16)
        frame=_movement_compare(state,frame,frame.candidates.byte(low16(frame.unit)),255,8)
        if not frame.status&4:
            return _campaign_carry_fields(state,frame,False)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_y),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1,True)
    frame=_city_ui_store_fields(state,frame,0xFFFFEFB0,low16(frame.target_x))
    return _campaign_carry_fields(state,frame,True)


def detect_unassigned_leader_roster_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """11EE: backward sixteen-city leader scan and its original FFFF/negative skip behavior."""
    frame=_city_ui_frame_fields(state,frame,0x11EE)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE660).cursor(),candidates=state.table_at(0xFFFFCC00).cursor())
    frame=_movement_move(state,frame,'target_x',15,16)
    while True:
        frame=first_replace(frame,roster=frame.roster.advance(-2))
        frame=_movement_move(state,frame,'target_y',frame.roster.word(),16)
        if not frame.status&8:
            frame=_movement_compare(state,frame,frame.candidates.byte(low16(frame.target_y)),255,8)
            if frame.status&4:
                frame=_city_ui_store_fields(state,frame,0xFFFFEFB0,low16(frame.target_x))
                frame=_movement_move(state,frame,'target_x',low16(frame.target_x)|0xFF00,16)
                frame=_city_ui_store_fields(state,frame,0xFFFFA622,low16(frame.target_x))
                return _campaign_carry_fields(state,frame,True)
        frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
        if low16(frame.target_x)==65535:
            return _campaign_carry_fields(state,frame,False)


def detect_unlisted_campaign_owner_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """13DC: actual three-owner exclusion and carry-only result."""
    frame=_city_ui_frame_fields(state,frame,0x13DC)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
    for address in (0xFFFFF67A,0xFFFFF67C,0xFFFFF67E):
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(address,2),16)
        if frame.status&4:
            return _campaign_carry_fields(state,frame,False)
    return _campaign_carry_fields(state,frame,True)


def detect_uniform_campaign_owner_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1406: original forty city-owner BYTE scan and retained high BYTE F376 store."""
    frame=_city_ui_frame_fields(state,frame,0x1406)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF428).cursor())
    value=frame.roster.byte()
    frame=first_replace(frame,roster=frame.roster.advance(1))
    frame=_movement_move(state,frame,'target_x',value,8)
    listed=False
    for address in (0xFFFFF67B,0xFFFFF67D,0xFFFFF67F):
        frame=_movement_compare(state,frame,low8(frame.target_x),state.read(address,1),8)
        if frame.status&4:
            listed=True
            break
    if not listed:
        return _campaign_carry_fields(state,frame,False)
    frame=_movement_move(state,frame,'target_y',38,16)
    while True:
        value=frame.roster.byte()
        frame=first_replace(frame,roster=frame.roster.advance(1))
        frame=_movement_compare(state,frame,low8(frame.target_x),value,8)
        if not frame.status&4:
            return _campaign_carry_fields(state,frame,False)
        frame=first_replace(frame,target_y=replace_word(frame.target_y,u16(low16(frame.target_y)-1)))
        if low16(frame.target_y)==65535:
            break
    frame=_city_ui_store_fields(state,frame,0xFFFFF376,low16(frame.target_x))
    return _campaign_carry_fields(state,frame,True)


def clear_pointer_cost_caches_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x133A)
    frame=_city_ui_store_fields(state,frame,0xFFFFF39E,0,4,True)
    return _city_ui_store_fields(state,frame,0xFFFFF3BA,0,4,True)


def move_campaign_map_pointer_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1290: four independent button directions; preserve signed right/bottom gate asymmetry."""
    frame=_city_ui_frame_fields(state,frame,0x1290)
    frame=_movement_test(state,frame,state.read(0xFFFFF600,2),16)
    if not frame.status&4:
        return frame
    for bit,address,amount,subtract in ((0,0xFFFFF35E,3,True),(1,0xFFFFF35E,3,False),
            (2,0xFFFFF360,4,True),(3,0xFFFFF360,4,False)):
        frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF602,1),bit)
        if frame.status&4:
            continue
        bound=8 if subtract else 1144
        frame=_movement_compare(state,frame,state.read(address,2),bound,16)
        if subtract:
            if frame.status&5:
                continue
        elif bool(frame.status&8)==bool(frame.status&2):
            continue
        frame=_city_ui_memory_arithmetic_fields(state,frame,address,amount,subtract)
        frame=_movement_compare(state,frame,state.read(address,2),bound,16)
        clamp=bool(frame.status&1) if subtract else not bool(frame.status&5)
        if clamp:
            frame=_city_ui_store_fields(state,frame,address,bound)
    return frame


def draw_campaign_pointer_marker_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1344: original marker eligibility, screen coordinate shifts and sole AC08 sprite child."""
    frame=_city_ui_frame_fields(state,frame,0x1344)
    for address,bit in ((0xFFFFF321,2),(0xFFFFF31C,1)):
        frame=_city_ui_bit_fields(state,frame,state.read(address,1),bit)
        if not frame.status&4:
            return frame
    frame=_movement_compare(state,frame,state.read(0xFFFFF322,2),12,16)
    if frame.status&1:
        return frame
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF314,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',3,True)
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',16)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF318,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',3,True)
    frame=_city_ui_arithmetic_fields(state,frame,'target_y',8)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF31C,1),0)
    if not frame.status&4:
        frame=_city_ui_arithmetic_fields(state,frame,'target_y',160)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=first_replace(frame,roster=state.table_at(0x1392).cursor())
    return _campaign_call_fields(state,frame,0xAC08,0x1390)


def update_outside_map_indicator_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1228: pointer containment and conditional warning/unwarning, no invented display return."""
    frame=_city_ui_frame_fields(state,frame,0x1228)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF31C,1),0)
    check_coordinates=not bool(frame.status&4)
    if not check_coordinates:
        frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF31C,1),2)
        blocked=not bool(frame.status&4)
        if not blocked:
            frame=_movement_test(state,frame,state.read(0xFFFFF322,2),16)
            blocked=not bool(frame.status&4)
        check_coordinates=not blocked
    outside=False
    if check_coordinates:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF35E,2),16)
        frame=_city_ui_arithmetic_fields(state,frame,'target_x',state.read(0xFFFFF314,2),True)
        frame=_movement_compare(state,frame,low16(frame.target_x),40,16)
        outside=not bool(frame.status&5)
        if not outside:
            frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF360,2),16)
            frame=_city_ui_arithmetic_fields(state,frame,'target_x',state.read(0xFFFFF318,2),True)
            frame=_movement_compare(state,frame,low16(frame.target_x),104,16)
            outside=not bool(frame.status&5)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),3)
    if outside:
        if not frame.status&4:
            return frame
        frame=_city_ui_store_fields(state,frame,0xFFFFF600,116)
        return _campaign_call_fields(state,frame,0x5ABC,0x127A)
    if frame.status&4:
        return frame
    return _campaign_call_fields(state,frame,0x5C98,0x128E)


def process_campaign_mode_control_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """10DC: classify campaign ownership before advancing the live world/selection mode."""
    frame=_city_ui_frame_fields(state,frame,0x10DC)
    frame=_movement_compare(state,frame,state.read(0xFFFFF36C,2),3,16)
    if not frame.status&4:
        frame=_campaign_call_fields(state,frame,0x11EE,0x10EA)
        blocked=bool(frame.status&1)
        if not blocked:
            frame=_campaign_call_fields(state,frame,0x1406,0x10F2)
            if frame.status&1:
                frame=_city_ui_store_fields(state,frame,0xFFFFF600,228)
                return _campaign_call_fields(state,frame,0xA3DA,0x11A4)
            frame=_campaign_call_fields(state,frame,0x13DC,0x10FA)
            if frame.status&1:
                frame=_movement_compare(state,frame,state.read(0xFFFFF36C,2),2,16)
                reset=False
                if frame.status&4:
                    frame=_movement_compare(state,frame,state.read(0xFFFFF376,2),255,16)
                    reset=bool(frame.status&4)
                if reset:
                    frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x20A)
                    frame=_city_ui_store_fields(state,frame,0xFFFFF362,0,2,True)
                    frame=_city_ui_store_fields(state,frame,0xFFFFF36C,1)
                else:
                    frame=_city_ui_store_fields(state,frame,0xFFFFF600,176)
                    frame=_campaign_call_fields(state,frame,0x5C98,0x1146)
                return _campaign_call_fields(state,frame,0xA3DA,0x11A4)
            for target,token in ((0x1228,0x1102),(0x9E5E,0x1108),(0x1290,0x110C),
                    (0xA01C,0x1112),(0xA14E,0x1118),(0x1344,0x111C),(0x9C36,0x1122)):
                frame=_campaign_call_fields(state,frame,target,token)
            return _campaign_call_fields(state,frame,0xA3DA,0x11A4)
    else:
        frame=_campaign_call_fields(state,frame,0x11A6,0x1162)
        blocked=bool(frame.status&1)
        if not blocked:
            frame=_campaign_call_fields(state,frame,0x1406,0x116A)
            if frame.status&1:
                frame=_city_ui_store_fields(state,frame,0xFFFFF600,228)
                return _campaign_call_fields(state,frame,0xA3DA,0x11A4)
            frame=_campaign_call_fields(state,frame,0x11EE,0x1172)
            blocked=bool(frame.status&1)
            if not blocked:
                frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x209)
                frame=_city_ui_store_fields(state,frame,0xFFFFF362,5)
                frame=_city_ui_store_fields(state,frame,0xFFFFCFCC,0,2,True)
                return _campaign_call_fields(state,frame,0xA3DA,0x11A4)
    frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x20C)
    frame=_city_ui_store_fields(state,frame,0xFFFFF362,0,2,True)
    return _campaign_call_fields(state,frame,0xA3DA,0x11A4)


def advance_campaign_entry_fade_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1444: actual alternating fade-in, title wait and quarter-rate fade-out."""
    frame=_city_ui_frame_fields(state,frame,0x1444)
    frame=_movement_compare(state,frame,state.read(0xFFFFF352,2),16,16)
    if frame.status&1:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF320,2),16)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&1,16)
        if not frame.status&4:
            return frame
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF352,2),16)
        frame=_movement_move(state,frame,'target_y',64,16)
        frame=first_replace(frame,roster=state.table_at(0xFFFFFB80).cursor())
        frame=_campaign_call_fields(state,frame,0xDEA6,0x146C)
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF352,1)
        return _campaign_call_fields(state,frame,0xA3DA,0x1476)
    if frame.status&4:
        frame=_city_ui_store_fields(state,frame,0xFFFFF600,32)
        return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF352,1)
    frame=_movement_compare(state,frame,state.read(0xFFFFF35A,2),7,16)
    if frame.status&1:
        return _campaign_call_fields(state,frame,0xA924,0x149C)
    frame=_movement_compare(state,frame,state.read(0xFFFFF352,2),33,16)
    if not frame.status&1:
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF612,1)
        return _city_ui_store_fields(state,frame,0xFFFFF608,2)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF320,2),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&3,16)
    if not frame.status&4:
        return frame
    frame=_movement_move(state,frame,'target_x',32,16)
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',state.read(0xFFFFF352,2),True)
    frame=_movement_move(state,frame,'target_y',64,16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFFB80).cursor())
    frame=_campaign_call_fields(state,frame,0xDEA6,0x14CC)
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF352,1)


def process_campaign_location_choice_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """14E0: cancel, map selection, alternate location page and original confirmation sound."""
    frame=_city_ui_frame_fields(state,frame,0x14E0)
    frame=_campaign_call_fields(state,frame,0xAB40,0x14E6)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
    if not frame.status&4:
        frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x200)
        frame=_city_ui_store_fields(state,frame,0xFFFFF352,0,2,True)
    else:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF35C,2),16)
        frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
        pressed=not bool(frame.status&4)
        if not pressed:
            frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),6)
            pressed=not bool(frame.status&4)
        if not pressed:
            frame=_campaign_call_fields(state,frame,0xA530,0x150E)
        else:
            frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&7,16)
            if not frame.status&4:
                frame=_campaign_call_fields(state,frame,0x157A,0x152C)
                frame=_movement_move(state,frame,'target_x',172,16)
                frame=_campaign_call_fields(state,frame,0x808A,0x1538)
            else:
                frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF350,1)
                frame=_campaign_memory_logic_fields(state,frame,0xFFFFF350,3,'and')
                frame=_campaign_call_fields(state,frame,0xA760,0x154C)
                frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF612,1)
                frame=_city_ui_store_fields(state,frame,0xFFFFF35A,0,2,True)
    return _campaign_call_fields(state,frame,0xA3DA,0x1578)


def select_campaign_location_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """157A: live location index adjustment and actual packed coordinate table."""
    frame=_city_ui_frame_fields(state,frame,0x157A)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF35C,2),16)
    frame=_movement_compare(state,frame,low16(frame.target_x),8,16)
    if not frame.status&1:
        frame=_city_ui_arithmetic_fields(state,frame,'target_x',1,True)
        frame=_movement_compare(state,frame,state.read(0xFFFFF358,2),29,16)
        if not frame.status&1:
            frame=_city_ui_arithmetic_fields(state,frame,'target_x',1,True)
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',state.read(0xFFFFF358,2))
    frame=_city_ui_shift_fields(state,frame,'target_x',2)
    frame=first_replace(frame,roster=state.table_at(0xD4AC2).cursor())
    frame=_city_ui_store_fields(state,frame,0xFFFFF360,frame.roster.word(low16(frame.target_x)))
    frame=_city_ui_store_fields(state,frame,0xFFFFF35E,frame.roster.word(low16(frame.target_x),2))
    frame=_campaign_call_fields(state,frame,0x15BE,0x15B0)
    frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x200)
    return _city_ui_store_fields(state,frame,0xFFFFF352,0,2,True)


def clamp_campaign_camera_targets_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """15BE: the two distinct camera-axis lower/upper clamps and original final flags."""
    frame=_city_ui_frame_fields(state,frame,0x15BE)
    for source,margin,limit,destination in ((0xFFFFF35E,112,928,0xFFFFF356),
            (0xFFFFF360,160,832,0xFFFFF354)):
        frame=_movement_move(state,frame,'target_x',state.read(source,2),16)
        frame=_city_ui_arithmetic_fields(state,frame,'target_x',margin,True)
        if frame.status&8:
            frame=_movement_move(state,frame,'target_x',0,16)
        frame=_movement_compare(state,frame,low16(frame.target_x),limit,16)
        if not frame.status&5:
            frame=_movement_move(state,frame,'target_x',limit,16)
        frame=_city_ui_store_fields(state,frame,destination,low16(frame.target_x))
    return frame


def wait_for_campaign_location_confirmation_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x15FC)
    frame=_movement_compare(state,frame,state.read(0xFFFFF35A,2),7,16)
    if frame.status&1:
        frame=_campaign_call_fields(state,frame,0xA924,0x160C)
    else:
        frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x202)
    return _campaign_call_fields(state,frame,0xA3DA,0x161C)


def process_campaign_camera_transition_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """161E: scroll completion gates enter ownership/command phases without substituting child results."""
    frame=_city_ui_frame_fields(state,frame,0x161E)
    for target,token in ((0x9E5E,0x1624),(0xA14E,0x162A),(0x1344,0x162E),(0x16B4,0x1632)):
        frame=_campaign_call_fields(state,frame,target,token)
    frame=_movement_test(state,frame,low16(frame.target_x),16)
    complete=bool(frame.status&4)
    if complete:
        frame=_movement_test(state,frame,state.read(0xFFFFF322,2),16)
        complete=bool(frame.status&4)
    if complete:
        frame=_movement_test(state,frame,state.read(0xFF3938,2),16)
        if frame.status&4:
            frame=_campaign_reset_selection_fields(state,frame)
            frame=_city_ui_store_fields(state,frame,0xFFFFF36E,0,2,True)
        else:
            frame=_movement_compare(state,frame,state.read(0xFFFFF36C,2),2,16)
            if frame.status&4:
                frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x208)
                frame=_city_ui_store_fields(state,frame,0xFFFFF362,4)
            else:
                frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x206)
                frame=_city_ui_store_fields(state,frame,0xFFFFF362,19)
                frame=_city_ui_store_fields(state,frame,0xFFFFF600,232)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF3A5,1),0)
    if frame.status&4:
        frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
        if not frame.status&4:
            frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x201)
    return _campaign_call_fields(state,frame,0xA3DA,0x16B2)


def scroll_campaign_camera_toward_pointer_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """16B4: horizontal/vertical world tile refresh with signed MOVEA.W and original clamp asymmetry."""
    frame=_city_ui_frame_fields(state,frame,0x16B4)
    frame=_movement_move(state,frame,'target_x',0,16)
    for name,source,margin,limit,camera,step,extent,target,negative_token,positive_token in (
            ('target_y',0xFFFFF35E,112,928,0xFFFFF314,3,224,0xA0CC,0x16F8,0x1722),
            ('unit',0xFFFFF360,160,832,0xFFFFF318,4,320,0xA10C,0x1768,0x1792)):
        frame=_movement_move(state,frame,name,state.read(source,2),16)
        frame=_city_ui_arithmetic_fields(state,frame,name,margin,True)
        if frame.status&8:
            frame=_movement_move(state,frame,name,0,16)
        frame=_movement_compare(state,frame,low16(getattr(frame,name)),limit,16)
        if not frame.status&5:
            frame=_movement_move(state,frame,name,limit,16)
        desired=low16(getattr(frame,name))
        frame=_movement_compare(state,frame,desired,state.read(camera,2),16)
        if frame.status&4:
            continue
        increasing=not bool(frame.status&5)
        frame=_city_ui_memory_arithmetic_fields(state,frame,camera,step,not increasing)
        frame=_movement_compare(state,frame,desired,state.read(camera,2),16)
        overshot=bool(frame.status&1) if increasing else not (bool(frame.status&4) or bool(frame.status&8)!=bool(frame.status&2))
        if overshot:
            frame=_city_ui_store_fields(state,frame,camera,desired)
        frame=first_replace(frame,scratch=state.table_at(u32(s16(state.read(camera,2)))).cursor())
        if increasing:
            frame=first_replace(frame,scratch=frame.scratch.advance(extent))
        frame=_campaign_call_fields(state,frame,target,positive_token if increasing else negative_token)
        frame=_movement_move(state,frame,'target_x',1,16)
    return frame


def _campaign_indexed_phase_fields(state: SceneState, frame: FirstDeploymentFrame,
        phase_address: int, table: int, code_base: int, continuation: int) -> FirstDeploymentFrame:
    """Closed original phase-dispatch shape; actual table WORDs select actual code, never guessed modes."""
    frame=_movement_move(state,frame,'target_x',state.read(phase_address,2),16)
    frame=_city_ui_shift_fields(state,frame,'target_x',1)
    frame=_movement_move(state,frame,'target_x',state.read(u32(table+s16(low16(frame.target_x))),2),16)
    return _campaign_call_fields(state,frame,u32(code_base+s16(low16(frame.target_x))),continuation)


def dispatch_campaign_selection_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x1798)
    frame=_campaign_call_fields(state,frame,0xD8EC,0x179E)
    frame=_campaign_call_fields(state,frame,0x1344,0x17A2)
    frame=_campaign_indexed_phase_fields(state,frame,0xFFFFF362,0x17D2,0x17FA,0x17B0)
    frame=_campaign_call_fields(state,frame,0xA3DA,0x17B6)
    frame=_movement_compare(state,frame,state.read(0xFFFFF362,2),6,16)
    if frame.status&4:
        frame=_movement_compare(state,frame,state.read(0xFFFFF612,2),0x20B,16)
        if frame.status&4:
            return frame
    return _campaign_call_fields(state,frame,0xA158,0x17D0)


def queue_campaign_selection_refresh_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x17FA)
    frame=_city_ui_store_fields(state,frame,0xFFFFF600,52)
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)


def prepare_campaign_selection_mode_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1806: command-specific status panel, ownership refresh and the two original equipment actions."""
    frame=_city_ui_frame_fields(state,frame,0x1806)
    frame=_movement_compare(state,frame,state.read(0xFFFFF36C,2),2,16)
    eligible=False
    if not frame.status&1:
        for value in (2,4,5,16):
            frame=_movement_compare(state,frame,state.read(0xFFFFF65A,2),value,16)
            if frame.status&4:
                eligible=True
                break
    if not eligible:
        return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),3)
    if frame.status&4:
        frame=_city_ui_store_fields(state,frame,0xFFFFF600,112)
        return _campaign_call_fields(state,frame,0x1626C,0x184E)
    frame=_city_ui_store_fields(state,frame,0xFFFFF362,8)
    frame=_city_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)
    frame=_city_ui_store_fields(state,frame,0xFFFFF36E,0,2,True)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),161,16)
    if not frame.status&4:
        frame=_campaign_call_fields(state,frame,0x14574,0x1870)
    frame=_movement_compare(state,frame,state.read(0xFFFFF65A,2),5,16)
    if frame.status&4:
        frame=_movement_compare(state,frame,state.read(0xFFFFF57A,2),164,16)
        if frame.status&4:
            return _campaign_call_fields(state,frame,0x11E3C,0x188A)
        return _campaign_call_fields(state,frame,0x11CF2,0x1894)
    return frame


def advance_campaign_selection_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x189E)
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)


def initialize_campaign_selection_mode_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """18A4: real command/side gates, display initialization and live roster count caching."""
    frame=_city_ui_frame_fields(state,frame,0x18A4)
    frame=_movement_compare(state,frame,state.read(0xFFFFF36C,2),2,16)
    show_status=False
    if not frame.status&1:
        frame=_movement_compare(state,frame,state.read(0xFFFFF65A,2),4,16)
        show_status=bool(frame.status&4)
        if not show_status:
            frame=_movement_compare(state,frame,state.read(0xFFFFF36C,2),3,16)
            if frame.status&4:
                frame=_movement_compare(state,frame,state.read(0xFFFFF65A,2),18,16)
                if not frame.status&1:
                    frame=_movement_compare(state,frame,state.read(0xFFFFF65A,2),20,16)
                    show_status=bool(frame.status&5)
    if show_status:
        frame=_city_ui_store_fields(state,frame,0xFFFFF600,112)
        frame=_campaign_call_fields(state,frame,0x1626C,0x18E2)
    else:
        frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),129,16)
        if not frame.status&4:
            frame=_campaign_call_fields(state,frame,0x5694,0x18F6)
        frame=_campaign_call_fields(state,frame,0x5ABC,0x18FC)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF3A5,1),0)
    if frame.status&4:
        frame=_movement_test(state,frame,state.read(0xFFFFF36C,2),16)
        # 190A's encoded BEQ targets 190E, the same ADDQ as fall-through.
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)
        frame=_city_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)
    else:
        frame=_city_ui_store_fields(state,frame,0xFFFFF362,8)
        frame=_city_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)
        frame=_city_ui_store_fields(state,frame,0xFFFFF36E,0,2,True)
        frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),122,16)
        if frame.status&4:
            frame=_city_ui_store_fields(state,frame,0xFFFFF600,76)
        else:
            frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),102,16)
            if frame.status&4:
                frame=_city_ui_store_fields(state,frame,0xFFFFF600,56)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF3A5,1),0)
    if not frame.status&4:
        return frame
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_campaign_call_fields(state,frame,0x5F48,0x1960)
    frame=_city_ui_store_fields(state,frame,0xFFFFF636,low16(frame.count))
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_city_ui_shift_fields(state,frame,'target_x',2)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE45C).cursor())
    return _city_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))+2),low16(frame.count))


def _campaign_parallel_packet_word_fields(state: SceneState, frame: FirstDeploymentFrame,
        displacement: int, parallel: int, primary: int, parallel_clear: bool=False,
        primary_clear: bool=False) -> FirstDeploymentFrame:
    """One original parallel WORD first, then primary postincrement; CLR retains its real prior read."""
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+displacement),parallel,2,parallel_clear)
    frame=_city_ui_store_fields(state,frame,frame.roster.base,primary,2,primary_clear)
    return first_replace(frame,roster=frame.roster.advance(2))


def _campaign_frame_border_fields(state: SceneState, frame: FirstDeploymentFrame,
        confirmation: bool) -> FirstDeploymentFrame:
    """Closed selection/confirmation frame layouts share their actual packet-word algorithm only."""
    frame=first_replace(frame,roster=state.table_at(0xFFFFD100).cursor())
    frame=first_replace(frame,roster=frame.roster.advance(s16(state.read(0xFFFFF31A,2))))
    frame=_campaign_parallel_packet_word_fields(state,frame,30,13,13)
    frame=_campaign_parallel_packet_word_fields(state,frame,30,0xC134,0xC0B4)
    if confirmation:
        frame=_campaign_parallel_packet_word_fields(state,frame,30,0,0,True,True)
    frame=_campaign_parallel_packet_word_fields(state,frame,30,0xC382,0xC380)
    frame=_movement_move(state,frame,'target_x',7 if confirmation else 10,16)
    while True:
        frame=_campaign_parallel_packet_word_fields(state,frame,30,0xC001,0xC381)
        frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
        if low16(frame.target_x)==65535:
            break
    frame=_campaign_parallel_packet_word_fields(state,frame,30,0xCB82,0xCB80)
    if confirmation:
        for _ in range(2):
            frame=_campaign_parallel_packet_word_fields(state,frame,30,0,0,True,True)
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+30),0,2,True)
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,60)


def append_campaign_selection_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x1974)
    frame=_campaign_frame_border_fields(state,frame,False)
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)
    return _campaign_call_fields(state,frame,0xD74A,0x19CA)


def update_campaign_selection_delay_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """19CC: owner-sensitive frame delay and original bit14 shortcut."""
    frame=_city_ui_frame_fields(state,frame,0x19CC)
    owned=False
    for value in (6,15,21):
        frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),value,16)
        if frame.status&4:
            owned=True
            break
    if not owned:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&255,16)
        frame=first_replace(frame,roster=state.table_at(0xFFFFF427).cursor())
        frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_x)),8)
        frame=_movement_compare(state,frame,low8(frame.target_x),state.read(0xFFFFF377,1),8)
        owned=bool(frame.status&4)
    if not owned:
        frame=_movement_compare(state,frame,state.read(0xFFFFF36A,2),1,16)
        if frame.status&1:
            return _campaign_call_fields(state,frame,0x57E0,0x1A64)
    else:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A4,2),16)
        frame=_city_ui_bit_fields(state,frame,frame.target_x,14)
        threshold=5 if not frame.status&4 else 7
        frame=_movement_compare(state,frame,state.read(0xFFFFF36A,2),threshold,16)
        if frame.status&1:
            return _campaign_call_fields(state,frame,0x57E0,0x1A64)
    frame=_campaign_call_fields(state,frame,0x5A80,0x1A3A)
    frame=_movement_compare(state,frame,state.read(0xFFFFF36A,2),5,16)
    if frame.status&1:
        return _city_ui_store_fields(state,frame,0xFFFFF362,15)
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)
    frame=_city_ui_store_fields(state,frame,0xFFFFF608,6)
    frame=_campaign_memory_logic_fields(state,frame,0xFFFFF3A4,0x8400,'or')
    return _campaign_memory_logic_fields(state,frame,0xFFFFF3A4,0xFDBF,'and')


def process_campaign_selection_input_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1A70: directional page repeat, cancel and command-specific selection commit."""
    frame=_city_ui_frame_fields(state,frame,0x1A70)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,1),8)
    frame=_movement_move(state,frame,'target_x',low8(frame.target_x)&3,8)
    page_input=not bool(frame.status&4)
    if page_input:
        eligible=False
        for value in (6,15,21):
            frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),value,16)
            if frame.status&4:
                eligible=True
                break
        if not eligible:
            frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF364,2),16)
            frame=_movement_move(state,frame,'target_y',low16(frame.target_y)&255,16)
            frame=first_replace(frame,roster=state.table_at(0xFFFFF427).cursor())
            frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_y)),8)
            frame=_movement_compare(state,frame,low8(frame.target_y),state.read(0xFFFFF377,1),8)
            eligible=bool(frame.status&4)
        if eligible:
            frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF608,1,True)
            if frame.status&4:
                frame=_city_ui_bit_fields(state,frame,frame.target_x,1)
                if frame.status&4:
                    frame=_movement_test(state,frame,state.read(0xFFFFF368,2),16)
                    change=not bool(frame.status&4)
                    if change:
                        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF368,1,True)
                else:
                    frame=_movement_move(state,frame,'choice',6,16)
                    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),6)
                    if not frame.status&4:
                        frame=_movement_move(state,frame,'choice',8,16)
                    frame=_movement_compare(state,frame,low16(frame.choice),state.read(0xFFFFF368,2),16)
                    change=not bool(frame.status&5)
                    if change:
                        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF368,1)
                if change:
                    frame=_city_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)
                    frame=_city_ui_store_fields(state,frame,0xFFFFF362,5)
                return _campaign_selection_commit_fields(state,frame)
            return _campaign_selection_commit_fields(state,frame)
    frame=_movement_test(state,frame,state.read(0xFFFFF364,2),16)
    if frame.status&8:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,2),16)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&47,16)
        if frame.status&4:
            frame=_city_ui_store_fields(state,frame,0xFFFFF608,6)
            return _campaign_selection_commit_fields(state,frame)
    else:
        frame=_city_ui_store_fields(state,frame,0xFFFFF608,6)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF602,1),4)
    if not frame.status&4:
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)
        return _city_ui_store_fields(state,frame,0xFFFFF36A,13)
    return _campaign_selection_commit_fields(state,frame)


def _campaign_selection_commit_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """The real 1B3A tail is shared by directional repeat and selection confirmation; no extra slot."""
    frame=_movement_test(state,frame,state.read(0xFFFFF364,2),16)
    if frame.status&8:
        return frame
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if frame.status&4:
        return frame
    special=False
    for value in (6,15,21):
        frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),value,16)
        if frame.status&4:
            special=True
            break
    if special:
        frame=_movement_test(state,frame,state.read(0xFFFFF62E,2),16)
        if frame.status&8:
            return _campaign_selection_guarded_commit_fields(state,frame)
    else:
        frame=_movement_test(state,frame,state.read(0xFFFFF36C,2),16)
        if not frame.status&4:
            return _campaign_selection_guarded_commit_fields(state,frame)
        frame=_movement_test(state,frame,state.read(0xFFFFF62E,1),8)
        if frame.status&8:
            return frame
    frame=_movement_move(state,frame,'target_x',172,16)
    frame=_campaign_call_fields(state,frame,0x808A,0x1B90)
    frame=_city_ui_store_fields(state,frame,0xFFFFF362,8)
    for address in (0xFFFFF36A,0xFFFFF658,0xFFFFF36E):
        frame=_city_ui_store_fields(state,frame,address,0,2,True)
    frame=_city_ui_store_fields(state,frame,0xFFFFF378,1)
    return _city_ui_store_fields(state,frame,0xFFFFF656,0,2,True)


def _campaign_selection_guarded_commit_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_compare(state,frame,state.read(0xFFFFF36C,2),2,16)
    second=bool(frame.status&4)
    frame=_campaign_call_fields(state,frame,0x1C12,0x1BE0 if second else 0x1BBE)
    if frame.status&1:
        return frame
    frame=_city_ui_store_fields(state,frame,0xFFFFF392,state.read(0xFFFFF364,2))
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF394,1)
    frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x208)
    frame=_city_ui_store_fields(state,frame,0xFFFFF362,4)
    if not second:
        return frame
    frame=_city_ui_store_fields(state,frame,0xFFFFF38C,145)
    frame=_city_ui_store_fields(state,frame,0xFFFFF576,0,2,True)
    frame=_city_ui_store_fields(state,frame,0xFFFFF380,130)
    return _campaign_call_fields(state,frame,0x5ABC,0x1C10)


def validate_campaign_roster_action_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1C12/1CEA: sole roster guard, four actual notices and carry-only permission result."""
    frame=_city_ui_frame_fields(state,frame,0x1C12)
    frame=_movement_compare(state,frame,state.read(0xFFFFF36C,2),1,16)
    if not frame.status&4:
        return _campaign_carry_fields(state,frame,False)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF427).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&63,16)
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_x)),8)
    frame=_movement_compare(state,frame,low8(frame.target_x),state.read(0xFFFFF377,1),8)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF579,1),8)
        restricted=False
        for value in (13,16,22,26):
            frame=_movement_compare(state,frame,low8(frame.target_x),value,8)
            if frame.status&4:
                restricted=True
                break
        if restricted:
            frame=_movement_compare(state,frame,state.read(0xFFFFF636,2),1,16)
            if frame.status&4:
                frame=_campaign_notice_fields(state,frame,151,0x1CB4)
                return _campaign_carry_fields(state,frame,True)
    frame=_movement_compare(state,frame,low8(frame.target_x),22,8)
    if frame.status&4:
        frame=_movement_compare(state,frame,state.read(0xFFFFF636,2),10,16)
        if not frame.status&1:
            frame=_campaign_notice_fields(state,frame,185,0x1CC4)
            return _campaign_carry_fields(state,frame,True)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),38,16)
    if frame.status&4:
        frame=_movement_compare(state,frame,state.read(0xFFFFF636,2),10,16)
        if not frame.status&1:
            frame=_campaign_notice_fields(state,frame,170,0x1CD4)
            return _campaign_carry_fields(state,frame,True)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),11,16)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF364,2),16)
        frame=_city_ui_shift_fields(state,frame,'target_y',2)
        frame=first_replace(frame,roster=state.table_at(0xFFFFCDFC).cursor())
        frame=_movement_test(state,frame,frame.roster.byte(low16(frame.target_y)),8)
        if not frame.status&4:
            frame=_campaign_notice_fields(state,frame,184,0x1CF4)
            return _campaign_carry_fields(state,frame,True)
    return _campaign_carry_fields(state,frame,False)


def expire_campaign_selection_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x1CFA)
    frame=_campaign_call_fields(state,frame,0x1D18,0x1CFE)
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,1,True)
    if frame.status&8:
        frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x201)
        frame=_campaign_clear_bit_fields(state,frame,0xFFFFF31C,3)
        frame=_city_ui_store_fields(state,frame,0xFFFFF3A4,0,2,True)
    return frame


def append_campaign_frame_progress_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1D18: progress packet's two parallel forty-word rows and original DBRA carrier."""
    frame=_city_ui_frame_fields(state,frame,0x1D18)
    frame=first_replace(frame,roster=state.table_at(0xFFFFD100).cursor())
    frame=first_replace(frame,roster=frame.roster.advance(s16(state.read(0xFFFFF31A,2))))
    frame=_campaign_parallel_packet_word_fields(state,frame,84,40,40)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF36A,2),16)
    frame=_city_ui_shift_fields(state,frame,'target_x',8)
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',0xC000)
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+84),low16(frame.target_x))
    frame=_city_ui_memory_arithmetic_fields(state,frame,u32(frame.roster.base+84),128)
    frame=_city_ui_append_fields(state,frame,low16(frame.target_x))
    frame=_movement_move(state,frame,'target_x',39,16)
    while True:
        frame=_campaign_parallel_packet_word_fields(state,frame,84,0x8000,0x8000)
        frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
        if low16(frame.target_x)==65535:
            break
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+84),0,2,True)
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,168)


def advance_campaign_frame_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x1D5E)
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)


def append_campaign_confirmation_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x1D64)
    frame=_campaign_frame_border_fields(state,frame,True)
    frame=_city_ui_store_fields(state,frame,0xFFFFF600,64)
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)


def refresh_campaign_confirmation_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x1DCE)
    return _campaign_call_fields(state,frame,0x5F7C,0x1DD4)


def finish_campaign_selection_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x1DD6)
    frame=_campaign_call_fields(state,frame,0x6198,0x1DDC)
    frame=_campaign_clear_bit_fields(state,frame,0xFFFFF3A5,0)
    return _city_ui_store_fields(state,frame,0xFFFFF38E,0,2,True)


def _campaign_roster_commit_member_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """The original 1EE0 tail accepts the real D0 from its caller; no reconstructed preset selection."""
    frame=_city_ui_store_fields(state,frame,0xFFFFF3A6,low16(frame.target_x))
    frame=_campaign_clear_bit_fields(state,frame,0xFFFFF3A5,0)
    frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x208)
    return _city_ui_store_fields(state,frame,0xFFFFF362,4)


def _campaign_roster_camera_choice_fields(state: SceneState, frame: FirstDeploymentFrame,
        require_button: bool) -> FirstDeploymentFrame:
    """Real 1FA0/1FAA camera-choice tail; the two original entry roles differ only in the button read."""
    if require_button:
        frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),6)
        if frame.status&4:
            return frame
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF378,2),16)
    frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF636,2),16)
    if not frame.status&5:
        return frame
    frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x207)
    frame=_city_ui_store_fields(state,frame,0xFFFFF362,0,2,True)
    frame=_city_ui_store_fields(state,frame,0xFFFFF352,0,2,True)
    frame=_city_ui_store_fields(state,frame,0xFFFFF354,state.read(0xFFFFF318,2))
    frame=_city_ui_store_fields(state,frame,0xFFFFF356,state.read(0xFFFFF314,2))
    frame=_city_ui_shift_fields(state,frame,'target_x',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF4FE).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&255,16)
    frame=_city_ui_store_fields(state,frame,0xFFFFF372,low16(frame.target_x))
    return _city_ui_store_fields(state,frame,0xFFFFF77A,0,2,True)


def process_campaign_roster_commands_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1DE8: actual roster wait, confirmation/cancel roles and command-specific campaign transition."""
    frame=_city_ui_frame_fields(state,frame,0x1DE8)
    frame=_movement_test(state,frame,state.read(0xFFFFF36C,2),16)
    if not frame.status&4:
        frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),103,16)
        if frame.status&4:
            frame=_movement_test(state,frame,state.read(0xFFFFF3DE,2),16)
            if frame.status&4:
                frame=_campaign_call_fields(state,frame,0x676C4,0x1E08)
                return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF3DE,1)
    frame=_campaign_call_fields(state,frame,0x62FA,0x1E16)
    frame=_movement_test(state,frame,state.read(0xFFFFF36C,2),16)
    if not frame.status&4:
        frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),102,16)
        if frame.status&4:
            frame=_campaign_call_fields(state,frame,0xC56E,0x1E2E)
    frame=_movement_test(state,frame,state.read(0xFFFFCFD2,2),16)
    confirm=False
    if not frame.status&4:
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFCFD2,1,True)
        frame=_movement_compare(state,frame,state.read(0xFFFFCFD2,2),8,16)
        if not frame.status&5:
            frame=_city_ui_store_fields(state,frame,0xFFFFCFD2,8)
    else:
        frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
        confirm=not bool(frame.status&4)
    if confirm:
        frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),129,16)
        if not frame.status&4:
            frame=_movement_test(state,frame,state.read(0xFFFFF36C,2),16)
            if frame.status&4:
                return _campaign_roster_camera_choice_fields(state,frame,False)
            for value in (6,15,21):
                frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),value,16)
                if frame.status&4:
                    return _campaign_roster_camera_choice_fields(state,frame,False)
        frame=_movement_test(state,frame,state.read(0xFFFFF656,2),16)
        if not frame.status&4:
            frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF378,2),16)
            frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF636,2),16)
            if not frame.status&5:
                return _campaign_call_fields(state,frame,0x64CC,0x1EC2)
            return _city_ui_store_fields(state,frame,0xFFFFF600,104)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF378,2),16)
        frame=_city_ui_shift_fields(state,frame,'target_x',1)
        frame=first_replace(frame,roster=state.table_at(0xFFFFF4FE).cursor())
        frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
        frame=_campaign_call_fields(state,frame,0x4E50,0x1EDA)
        frame=_movement_test(state,frame,low16(frame.target_y),16)
        if not frame.status&4:
            return frame
        return _campaign_roster_commit_member_fields(state,frame)
    frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),145,16)
    if frame.status&4:
        return _campaign_roster_camera_choice_fields(state,frame,True)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
    if frame.status&4:
        return _campaign_roster_camera_choice_fields(state,frame,True)
    for value in (6,15,21):
        frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),value,16)
        if frame.status&4:
            return _campaign_roster_commit_member_fields(state,frame)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),113,16)
    if frame.status&4:
        frame=_campaign_call_fields(state,frame,0xC11E,0x1FF0)
        frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x208)
        frame=_city_ui_store_fields(state,frame,0xFFFFF362,3)
        return _city_ui_store_fields(state,frame,0xFFFFF36A,18)
    frame=_city_ui_store_fields(state,frame,0xFFFFF322,0,2,True)
    frame=_movement_test(state,frame,state.read(0xFFFFF36C,2),16)
    if frame.status&4:
        frame=_city_ui_store_fields(state,frame,0xFFFFF362,7)
        return _city_ui_store_fields(state,frame,0xFFFFF36A,13)
    frame=_movement_compare(state,frame,state.read(0xFFFFF36C,2),2,16)
    if frame.status&4:
        frame=_movement_test(state,frame,state.read(0xFFFFF65A,2),16)
        if frame.status&4:
            frame=_city_ui_store_fields(state,frame,0xFFFFF3C2,0x205)
            frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x208)
            frame=_city_ui_store_fields(state,frame,0xFFFFF362,19)
            frame=_city_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)
            return _city_ui_store_fields(state,frame,0xFFFFF380,133)
    else:
        frame=_movement_compare(state,frame,state.read(0xFFFFF36C,2),3,16)
        if frame.status&4:
            return _campaign_roster_camera_choice_fields(state,frame,True)
        frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),103,16)
        if frame.status&4:
            frame=_campaign_call_fields(state,frame,0xC590,0x1F4C)
    frame=_city_ui_store_fields(state,frame,0xFFFFF378,0,2,True)
    frame=_city_ui_store_fields(state,frame,0xFFFFF658,0,2,True)
    frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x208)
    frame=_city_ui_store_fields(state,frame,0xFFFFF362,2)
    return _city_ui_store_fields(state,frame,0xFFFFF36A,18)


def trigger_campaign_selection_audio_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x2004)
    frame=_movement_test(state,frame,state.read(0xFFFFF652,2),16)
    if frame.status&4:
        return _campaign_call_fields(state,frame,0x674CA,0x2028)
    frame=_movement_test(state,frame,state.read(0xFFFFF36A,2),16)
    if not frame.status&4:
        return _campaign_call_fields(state,frame,0x674CA,0x2028)
    frame=_movement_test(state,frame,state.read(0xFFFFF600,2),16)
    if not frame.status&4:
        return frame
    frame=_city_ui_store_fields(state,frame,0xFFFFF600,100)
    return _campaign_call_fields(state,frame,0x674CA,0x2028)


def update_campaign_selection_audio_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x202A)
    frame=_movement_test(state,frame,state.read(0xFFFFF652,2),16)
    if not frame.status&4:
        frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF3A5,1),2)
        if frame.status&4:
            frame=_campaign_call_fields(state,frame,0xD8AE,0x2042)
    return _campaign_call_fields(state,frame,0x671B6,0x2048)


def animate_campaign_selection_glyph_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x2050)
    frame=_movement_move_long(state,frame,'target_x',0xC000000D)
    frame=_movement_move(state,frame,'target_y',3,16)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF36A,2),16)
    frame=_movement_move(state,frame,'count',low16(frame.unit),16)
    frame=_city_ui_shift_fields(state,frame,'unit',1)
    frame=_city_ui_arithmetic_fields(state,frame,'unit',low16(frame.count))
    frame=_city_ui_shift_fields(state,frame,'unit',7)
    frame=_city_ui_arithmetic_fields(state,frame,'unit',0xC234)
    frame=first_replace(frame,roster=state.table_at(0x20AC).cursor())
    frame=_campaign_call_fields(state,frame,0x26BFA,0x2074)
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,1)
    frame=_movement_move(state,frame,'target_x',7,16)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),6)
    if not frame.status&4:
        frame=_movement_move(state,frame,'target_x',5,16)
    frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF36A,2),16)
    if not frame.status&1:
        return frame
    frame=_city_ui_store_fields(state,frame,0xFFFFF362,6)
    frame=_city_ui_store_fields(state,frame,0xFFFFF608,6)
    frame=_campaign_memory_logic_fields(state,frame,0xFFFFF3A4,0x8400,'or')
    return _campaign_memory_logic_fields(state,frame,0xFFFFF3A4,0xFDBF,'and')


def announce_selected_assignment_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """20B8: assignment position chooses one of three original notices from the live twelve-byte record."""
    frame=_city_ui_frame_fields(state,frame,0x20B8)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE80C).cursor())
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF364,2),16)
    frame=_city_ui_shift_fields(state,frame,'target_y',1)
    frame=_city_ui_arithmetic_fields(state,frame,'target_y',state.read(0xFFFFF364,2))
    frame=_city_ui_shift_fields(state,frame,'target_y',2)
    frame=first_replace(frame,roster=frame.roster.advance(s16(low16(frame.target_y))))
    frame=_movement_move(state,frame,'target_x',180,16)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A6,2),16)
    frame=_movement_compare(state,frame,low16(frame.target_y),frame.roster.word(),16)
    if not frame.status&4:
        frame=_city_ui_arithmetic_fields(state,frame,'target_x',1)
        frame=_movement_compare(state,frame,low16(frame.target_y),frame.roster.word(0,4),16)
        if not frame.status&4:
            frame=_city_ui_arithmetic_fields(state,frame,'target_x',1)
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)
    return _campaign_call_fields(state,frame,0x676F2,0x20EE)


def _campaign_assignment_packet_fields(state: SceneState, frame: FirstDeploymentFrame,
        template: int, continuation: int) -> FirstDeploymentFrame:
    frame=_movement_move_long(state,frame,'target_x',0xC0000008)
    frame=_movement_move(state,frame,'target_y',7,16)
    frame=_movement_move(state,frame,'unit',0xC422,16)
    frame=first_replace(frame,roster=state.table_at(template).cursor())
    return _campaign_call_fields(state,frame,0x26BFA,continuation)


def initialize_assignment_confirmation_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x20F0)
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)
    frame=_city_ui_store_fields(state,frame,0xFFFFF600,92)
    frame=_city_ui_store_fields(state,frame,0xFFFFF386,0,2,True)
    return _campaign_assignment_packet_fields(state,frame,0x2118,0x2116)


def process_assignment_confirmation_input_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x2168)
    frame=_campaign_call_fields(state,frame,0xC764,0x216E)
    frame=_campaign_call_fields(state,frame,0xC790,0x2174)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    confirm=not bool(frame.status&4)
    if not confirm:
        frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
        if frame.status&4:
            return frame
        frame=_city_ui_store_fields(state,frame,0xFFFFF386,1)
    frame=_movement_move(state,frame,'target_x',172,16)
    frame=_campaign_call_fields(state,frame,0x808A,0x2188)
    frame=_campaign_call_fields(state,frame,0x21BC,0x218C)
    frame=_city_ui_store_fields(state,frame,0xFFFFF362,9)
    frame=_campaign_clear_bit_fields(state,frame,0xFFFFF3A4,1)
    frame=_movement_test(state,frame,state.read(0xFFFFF386,2),16)
    if frame.status&4:
        return _campaign_call_fields(state,frame,0x21F2,0x21A4)
    return frame


def upload_assignment_confirmation_glyph_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x21BC)
    return _campaign_assignment_packet_fields(state,frame,0x21D6,0x21D4)


def remove_selected_assignment_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """21F2: actual CD00 BYTE clear, retained D1 and selected assignment WORD sentinel."""
    frame=_city_ui_frame_fields(state,frame,0x21F2)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCD00).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),0,1,True)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_movement_move(state,frame,'unit',low16(frame.target_x),16)
    frame=_city_ui_shift_fields(state,frame,'target_x',1)
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',low16(frame.unit))
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',low16(frame.target_y))
    frame=_city_ui_shift_fields(state,frame,'target_x',2)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE804).cursor())
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),65535)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF3A5,1),3)
    if not frame.status&4:
        return _campaign_call_fields(state,frame,0xD74A,0x222C)
    return frame


def process_campaign_exit_input_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x222E)
    frame=_campaign_call_fields(state,frame,0xA4CC,0x2234)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,2),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&48,16)
    if not frame.status&4:
        frame=_campaign_call_fields(state,frame,0xA506,0x2246)
        frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x201)
    return frame


def dispatch_campaign_post_selection_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x224E)
    frame=_campaign_indexed_phase_fields(state,frame,0xFFFFF362,0x2264,0x2268,0x225C)
    return _campaign_call_fields(state,frame,0xA3DA,0x2262)


def draw_campaign_fade_marker_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x23F6)
    frame=first_replace(frame,roster=state.table_at(0x240E).cursor())
    frame=_movement_move(state,frame,'target_x',32,16)
    frame=_movement_move(state,frame,'target_y',24,16)
    frame=_movement_move(state,frame,'unit',0,16)
    return _campaign_call_fields(state,frame,0xAC08,0x240C)


def dispatch_campaign_subcommand_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x2416)
    frame=_campaign_indexed_phase_fields(state,frame,0xFFFFF362,0x2438,0x2490,0x2424)
    for target,token in ((0xD8EC,0x242A),(0xA158,0x2430),(0xA3DA,0x2436)):
        frame=_campaign_call_fields(state,frame,target,token)
    return frame


def update_personnel_command_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x36DC)
    for target,token in ((0x13D48,0x36E2),(0xD8EC,0x36E8),(0xA3DA,0x36EE)):
        frame=_campaign_call_fields(state,frame,target,token)
    return frame


def update_city_command_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x36F0)
    frame=_campaign_call_fields(state,frame,0x16660,0x36F6)
    return _campaign_call_fields(state,frame,0xA3DA,0x36FC)


def update_support_command_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x36FE)
    frame=_campaign_call_fields(state,frame,0x312C8,0x3704)
    return _campaign_call_fields(state,frame,0xA3DA,0x370A)


def update_tactical_command_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x370C)
    frame=_campaign_call_fields(state,frame,0x66BF4,0x3712)
    return _campaign_call_fields(state,frame,0xA3DA,0x3718)


def update_battle_command_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x371A)
    frame=_campaign_call_fields(state,frame,0x1CF58,0x3720)
    return _campaign_call_fields(state,frame,0xA3DA,0x3726)


def exit_post_campaign_message_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x3728)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,2),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&112,16)
    if not frame.status&4:
        frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x201)
        frame=_city_ui_store_fields(state,frame,0xFFFFAFFE,0,2,True)
    return frame


def dismiss_campaign_warning_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,0x3740)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,2),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&112,16)
    if frame.status&4:
        return frame
    frame=_movement_move_long(state,frame,'target_x',0xC0000026)
    frame=_movement_move(state,frame,'target_y',7,16)
    frame=_movement_move(state,frame,'unit',0xCA02,16)
    frame=first_replace(frame,roster=state.table_at(0x3772).cursor())
    frame=_campaign_call_fields(state,frame,0x26BFA,0x3764)
    frame=_campaign_clear_bit_fields(state,frame,0xFFFFF3A4,6)
    return _city_ui_store_fields(state,frame,0xFFFFF612,0x201)


def _campaign_known_child_fields(state: SceneState, frame: FirstDeploymentFrame, target: int) -> FirstDeploymentFrame:
    """Only actual complete named callees; an unclosed child retains its real committed entry SP."""
    if target == 419350:
        from ..high_level_diplomacy_forces.business_scene_forces import resolve_force_reassignment_fields
        return resolve_force_reassignment_fields(state, frame)
    if target == 92876:
        from ..high_level_movement_v2.business_scene_transport import prepare_transport_path_fields
        return prepare_transport_path_fields(state, frame)
    if target == 90732:
        from ..high_level_main_flows.business_gameplay import append_four_row_status_panel_fields
        return append_four_row_status_panel_fields(state, frame)
    if target == 83316:
        from ..high_level_player_commands.business_display import append_selected_group_panel_fields
        from ..high_level_player_commands.contexts_display import SpritePacketMemory
        return append_selected_group_panel_fields(SpritePacketMemory(state), frame)
    if target == 423620:
        from ..high_level_main_flows.business_highbank import dispatch_message_control_frame_fields
        return dispatch_message_control_frame_fields(state, frame)
    if target == 57582:
        from ..high_level_city_officer.business_scene_orders import queue_development_order_fields
        return queue_development_order_fields(state, frame)
    if target == 57652:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_103_fields
        return lowbank_coordinate_live_state_103_fields(state, frame)
    if target == 58360:
        from ..high_level_remaining_flows.business_lowbank import lowbank_update_live_fields_9_fields
        return lowbank_update_live_fields_9_fields(state, frame)
    if target == 58362:
        from ..high_level_city_officer.business_scene_orders import queue_welfare_order_fields
        return queue_welfare_order_fields(state, frame)
    if target == 58432:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_104_fields
        return lowbank_coordinate_live_state_104_fields(state, frame)
    if target == 58748:
        from ..high_level_city_officer.business_scene_orders import commit_tax_rate_fields
        return commit_tax_rate_fields(state, frame)
    if target == 58770:
        from ..high_level_command_actions.contexts_personnel import execute_personnel_scene_fields
        return execute_personnel_scene_fields(state, target, frame)
    if target == 59280:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_105_fields
        return lowbank_coordinate_live_state_105_fields(state, frame)
    if target == 59426:
        from ..high_level_remaining_flows.business_lowbank import _economy_cleanup_tail_fields
        return _economy_cleanup_tail_fields(state, frame)
    if target == 64500:
        from ..high_level_city_officer.business_scene_orders import commit_recruitment_fields
        return commit_recruitment_fields(state, frame)
    if target == 64534:
        from ..high_level_city_officer.business_scene_orders import commit_equipment_purchase_fields
        return commit_equipment_purchase_fields(state, frame)
    if target == 64640:
        from ..high_level_remaining_flows.business_lowbank import lowbank_update_live_fields_11_fields
        return lowbank_update_live_fields_11_fields(state, frame)
    if target == 64642:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_108_fields
        return lowbank_coordinate_live_state_108_fields(state, frame)
    if target == 64664:
        from ..high_level_remaining_flows.business_lowbank import lowbank_calculate_live_quotient_2_fields
        return lowbank_calculate_live_quotient_2_fields(state, frame)
    if target == 64752:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_106_alternate_1_fields
        return lowbank_coordinate_live_state_106_alternate_1_fields(state, frame)
    if target == 64756:
        from ..high_level_remaining_flows.business_lowbank import lowbank_calculate_live_quotient_3_fields
        return lowbank_calculate_live_quotient_3_fields(state, frame)
    if target == 59622:
        from ..high_level_remaining_flows.business_lowbank import lowbank_calculate_live_quotient_1_fields
        return lowbank_calculate_live_quotient_1_fields(state, frame)
    if target == 60514:
        from ..high_level_remaining_flows.business_lowbank import lowbank_scale_live_record_value_1_fields
        return lowbank_scale_live_record_value_1_fields(state, frame)
    if target == 60884:
        from ..high_level_remaining_flows.business_lowbank import lowbank_update_live_fields_10_fields
        return lowbank_update_live_fields_10_fields(state, frame)
    if target == 60886:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_107_fields
        return lowbank_coordinate_live_state_107_fields(state, frame)
    if target == 64252:
        from ..high_level_remaining_flows.business_lowbank import lowbank_update_record_flags_13_fields
        return lowbank_update_record_flags_13_fields(state, frame)
    if target == 64496:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_106_fields
        return lowbank_coordinate_live_state_106_fields(state, frame)
    if target == 9360:
        from ..high_level_remaining_flows.business_lowbank import lowbank_update_record_flags_1_fields
        return lowbank_update_record_flags_1_fields(state, frame)
    if target == 11932:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_29_fields
        return lowbank_coordinate_live_state_29_fields(state, frame)
    if target == 12006:
        from ..high_level_remaining_flows.business_lowbank import lowbank_update_record_flags_5_fields
        return lowbank_update_record_flags_5_fields(state, frame)
    if target == 12048:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_30_fields
        return lowbank_coordinate_live_state_30_fields(state, frame)
    if target == 12094:
        from ..high_level_remaining_flows.business_lowbank import lowbank_update_record_flags_6_fields
        return lowbank_update_record_flags_6_fields(state, frame)
    if target == 12144:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_31_fields
        return lowbank_coordinate_live_state_31_fields(state, frame)
    if target == 12238:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_32_fields
        return lowbank_coordinate_live_state_32_fields(state, frame)
    if target == 12252:
        from ..high_level_remaining_flows.business_lowbank import lowbank_update_record_flags_7_fields
        return lowbank_update_record_flags_7_fields(state, frame)
    if target == 12346:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_33_fields
        return lowbank_coordinate_live_state_33_fields(state, frame)
    if target == 12364:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_34_fields
        return lowbank_coordinate_live_state_34_fields(state, frame)
    if target == 12372:
        from ..high_level_remaining_flows.business_lowbank import lowbank_update_record_flags_8_fields
        return lowbank_update_record_flags_8_fields(state, frame)
    if target == 12564:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_35_fields
        return lowbank_coordinate_live_state_35_fields(state, frame)
    if target == 12602:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_36_fields
        return lowbank_coordinate_live_state_36_fields(state, frame)
    if target == 12610:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_37_fields
        return lowbank_coordinate_live_state_37_fields(state, frame)
    if target == 12630:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_38_fields
        return lowbank_coordinate_live_state_38_fields(state, frame)
    if target == 12644:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_39_fields
        return lowbank_coordinate_live_state_39_fields(state, frame)
    if target == 12724:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_40_fields
        return lowbank_coordinate_live_state_40_fields(state, frame)
    if target == 12798:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_41_fields
        return lowbank_coordinate_live_state_41_fields(state, frame)
    if target == 12866:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_42_fields
        return lowbank_coordinate_live_state_42_fields(state, frame)
    if target == 12930:
        from ..high_level_remaining_flows.business_lowbank import lowbank_process_counted_records_1_fields
        return lowbank_process_counted_records_1_fields(state, frame)
    if target == 13068:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_43_fields
        return lowbank_coordinate_live_state_43_fields(state, frame)
    if target == 13100:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_44_fields
        return lowbank_coordinate_live_state_44_fields(state, frame)
    if target == 13108:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_45_fields
        return lowbank_coordinate_live_state_45_fields(state, frame)
    if target == 13206:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_46_fields
        return lowbank_coordinate_live_state_46_fields(state, frame)
    if target == 13250:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_47_fields
        return lowbank_coordinate_live_state_47_fields(state, frame)
    if target == 13258:
        from ..high_level_remaining_flows.business_lowbank import lowbank_select_live_state_12_fields
        return lowbank_select_live_state_12_fields(state, frame)
    if target == 13288:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_48_fields
        return lowbank_coordinate_live_state_48_fields(state, frame)
    if target == 13346:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_49_fields
        return lowbank_coordinate_live_state_49_fields(state, frame)
    if target == 13360:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_50_fields
        return lowbank_coordinate_live_state_50_fields(state, frame)
    if target == 13408:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_51_fields
        return lowbank_coordinate_live_state_51_fields(state, frame)
    if target == 13442:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_52_fields
        return lowbank_coordinate_live_state_52_fields(state, frame)
    if target == 13482:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_53_fields
        return lowbank_coordinate_live_state_53_fields(state, frame)
    if target == 13538:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_54_fields
        return lowbank_coordinate_live_state_54_fields(state, frame)
    if target == 13592:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_55_fields
        return lowbank_coordinate_live_state_55_fields(state, frame)
    if target == 13664:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_56_fields
        return lowbank_coordinate_live_state_56_fields(state, frame)
    if target == 13684:
        from ..high_level_remaining_flows.business_lowbank import lowbank_select_live_state_13_fields
        return lowbank_select_live_state_13_fields(state, frame)
    if target == 13716:
        from ..high_level_remaining_flows.business_lowbank import lowbank_select_live_state_14_fields
        return lowbank_select_live_state_14_fields(state, frame)
    if target == 13748:
        from ..high_level_remaining_flows.business_lowbank import lowbank_select_live_state_15_fields
        return lowbank_select_live_state_15_fields(state, frame)
    if target == 13778:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_57_fields
        return lowbank_coordinate_live_state_57_fields(state, frame)
    if target == 13800:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_58_fields
        return lowbank_coordinate_live_state_58_fields(state, frame)
    if target == 13808:
        from ..high_level_remaining_flows.business_lowbank import lowbank_update_live_fields_4_fields
        return lowbank_update_live_fields_4_fields(state, frame)
    if target == 13828:
        from ..high_level_remaining_flows.business_lowbank import lowbank_select_live_state_16_fields
        return lowbank_select_live_state_16_fields(state, frame)
    if target == 13864:
        from ..high_level_remaining_flows.business_lowbank import lowbank_process_device_control_1_fields
        return lowbank_process_device_control_1_fields(state, frame)
    if target == 14026:
        from ..high_level_remaining_flows.business_lowbank import lowbank_select_live_state_17_fields
        return lowbank_select_live_state_17_fields(state, frame)
    if target == 8808:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_1_fields
        return lowbank_coordinate_live_state_1_fields(state, frame)
    if target == 8924:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_2_fields
        return lowbank_coordinate_live_state_2_fields(state, frame)
    if target == 23424:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_75_special_fields
        return lowbank_coordinate_live_state_75_special_fields(state, frame)
    if target == 22628:
        from ..high_level_remaining_flows.business_lowbank import lowbank_update_live_fields_5_fields
        return lowbank_update_live_fields_5_fields(state, frame)
    if target == 22690:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_73_fields
        return lowbank_coordinate_live_state_73_fields(state, frame)
    if target == 22666:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_72_fields
        return lowbank_coordinate_live_state_72_fields(state, frame)
    if target == 22826:
        from ..high_level_remaining_flows.business_lowbank import lowbank_process_counted_records_8_alternate_1_fields
        return lowbank_process_counted_records_8_alternate_1_fields(state, frame)
    if target == 22844:
        from ..high_level_remaining_flows.business_lowbank import lowbank_process_counted_records_8_alternate_2_fields
        return lowbank_process_counted_records_8_alternate_2_fields(state, frame)
    if target == 22938:
        from ..high_level_remaining_flows.business_lowbank import lowbank_process_counted_records_9_fields
        return lowbank_process_counted_records_9_fields(state, frame)
    if target == 23000:
        from ..high_level_remaining_flows.business_lowbank import lowbank_process_counted_records_9_alternate_1_fields
        return lowbank_process_counted_records_9_alternate_1_fields(state, frame)
    if target == 23026:
        from ..high_level_remaining_flows.business_lowbank import lowbank_process_counted_records_9_alternate_2_fields
        return lowbank_process_counted_records_9_alternate_2_fields(state, frame)
    if target == 22872:
        from ..high_level_remaining_flows.business_lowbank import lowbank_process_counted_records_8_alternate_3_fields
        return lowbank_process_counted_records_8_alternate_3_fields(state, frame)
    if target == 22892:
        from ..high_level_remaining_flows.business_lowbank import lowbank_process_counted_records_8_alternate_4_fields
        return lowbank_process_counted_records_8_alternate_4_fields(state, frame)
    if target == 22914:
        from ..high_level_remaining_flows.business_lowbank import lowbank_process_counted_records_8_alternate_5_fields
        return lowbank_process_counted_records_8_alternate_5_fields(state, frame)
    if target == 23056:
        from ..high_level_remaining_flows.business_lowbank import lowbank_process_counted_records_9_alternate_3_fields
        return lowbank_process_counted_records_9_alternate_3_fields(state, frame)
    if target == 20678:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_69_fields
        return lowbank_coordinate_live_state_69_fields(state, frame)
    if target == 20700:
        from ..high_level_remaining_flows.business_lowbank import lowbank_process_device_control_10_fields
        return lowbank_process_device_control_10_fields(state, frame)
    if target == 20836:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_70_fields
        return lowbank_coordinate_live_state_70_fields(state, frame)
    if target == 20882:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_71_fields
        return lowbank_coordinate_live_state_71_fields(state, frame)
    if target == 423114:
        from .business_highbank import advance_message_decoration_stage_fields
        return advance_message_decoration_stage_fields(state, frame)
    if target == 992:
        from .business_title import initialize_title_scene_fields
        return initialize_title_scene_fields(state, frame)
    if target == 996:
        from .business_title import initialize_title_scene_preserving_mode_fields
        return initialize_title_scene_preserving_mode_fields(state, frame)
    if target == 1000:
        from .business_title import return_title_idle_slot_fields
        return return_title_idle_slot_fields(state, frame)
    if target == 1004:
        from .business_title import initialize_secondary_title_scene_fields
        return initialize_secondary_title_scene_fields(state, frame)
    if target == 1008:
        from .business_title import initialize_title_transition_scene_fields
        return initialize_title_transition_scene_fields(state, frame)
    if target == 44294:
        from ..high_level_scene_flows.business_scene import flush_scene_transfer_queue_fields
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        return flush_scene_transfer_queue_fields(SceneRefreshMemory(state), frame)
    if target == 424444:
        from .business_highbank import render_force_city_markers_fields
        return render_force_city_markers_fields(state, frame)
    if target == 97418:
        from .business_movement_support import ensure_neighbor_capacity_fields
        return ensure_neighbor_capacity_fields(state, frame)
    if target == 98096:
        from .business_movement_support import integrate_selected_officer_into_packed_group_fields
        return integrate_selected_officer_into_packed_group_fields(state, frame)
    if target == 114668:
        from ..high_level_gameplay_flow.business_battle import settle_city_battle_outcome_fields
        from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
        return settle_city_battle_outcome_fields(BattlePresentationMemory(state), frame)
    if target == 154584:
        from .business_gameplay import initialize_battle_policy_targets_frame_fields
        return initialize_battle_policy_targets_frame_fields(state, frame)
    if target == 198064:
        from .business_scene_support import run_controller_setup_and_configuration_fields
        return run_controller_setup_and_configuration_fields(state, frame)
    if target == 26662:
        from ..high_level_gameplay_flow.business_services import initialize_video_registers_and_planes_fields
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        return initialize_video_registers_and_planes_fields(SceneRefreshMemory(state), frame)
    if target == 198510:
        from .business_scene_support import commit_setup_options_fields
        return commit_setup_options_fields(state, frame)
    if target == 15956:
        from .business_map import restore_scene_descriptor_fields
        return restore_scene_descriptor_fields(state, frame)
    if target == 243506:
        from .business_scene_support import run_repeating_scene_presentation_fields
        return run_repeating_scene_presentation_fields(state, frame)
    if target == 44540:
        from ..high_level_scene_flows.business_scene import write_vdp_dictionary_repeat_stream_fields
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        return write_vdp_dictionary_repeat_stream_fields(SceneRefreshMemory(state), frame)
    if target == 91608:
        from .business_gameplay import upload_selected_queue_officer_name_fields
        return upload_selected_queue_officer_name_fields(state, frame)
    if target == 89988:
        from .business_gameplay import append_city_currency_panel_fields
        return append_city_currency_panel_fields(state, frame)
    if target == 90206:
        from .business_gameplay import append_city_project_panel_fields
        return append_city_project_panel_fields(state, frame)
    if target == 90580:
        from .business_gameplay import append_current_city_value_fields
        return append_current_city_value_fields(state, frame)
    if target == 90670:
        from .business_gameplay import append_selected_long_value_fields
        return append_selected_long_value_fields(state, frame)
    if target == 92986:
        from ..high_level_gameplay_flow.business_calendar import process_calendar_city_cycle_fields
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        return process_calendar_city_cycle_fields(SceneRefreshMemory(state), frame)
    if target == 95746:
        from ..high_level_gameplay_flow.business_battle import initialize_battle_scene_fields
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        return initialize_battle_scene_fields(SceneRefreshMemory(state), frame)
    if target == 96190:
        from ..high_level_gameplay_flow.business_battle import upload_battle_scene_labels_fields
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        return upload_battle_scene_labels_fields(SceneRefreshMemory(state), frame)
    if target == 96790:
        from .business_gameplay import upload_first_battle_prompt_fields
        return upload_first_battle_prompt_fields(state, frame)
    if target == 96858:
        from .business_gameplay import upload_second_battle_prompt_fields
        return upload_second_battle_prompt_fields(state, frame)
    if target == 96926:
        from .business_gameplay import build_nearby_battle_targets_fields
        return build_nearby_battle_targets_fields(state, frame)
    if target == 98014:
        from .business_gameplay import upload_battle_action_prompt_fields
        return upload_battle_action_prompt_fields(state, frame)
    if target == 99320:
        from ..high_level_gameplay_flow.business_battle import resolve_city_battle_damage_fields
        from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
        return resolve_city_battle_damage_fields(BattlePresentationMemory(state), frame)[0]
    if target == 100170:
        from .business_gameplay import upload_battle_result_prompt_fields
        return upload_battle_result_prompt_fields(state, frame)
    if target == 100242:
        from .business_gameplay import upload_selected_officer_names_fields
        return upload_selected_officer_names_fields(state, frame)
    if target == 216870:
        from .business_scene_support import begin_auxiliary_command_stage_fields
        return begin_auxiliary_command_stage_fields(state, frame)
    if target == 150224:
        from .business_gameplay import select_primary_force_order_policy_frame_fields
        return select_primary_force_order_policy_frame_fields(state, frame)
    if target == 139748:
        from .business_gameplay import process_both_battle_force_turns_fields
        return process_both_battle_force_turns_fields(state, frame)
    if target == 67372:
        from ..high_level_gameplay_flow.business_services import load_gameplay_scene_fields
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        return load_gameplay_scene_fields(SceneRefreshMemory(state), frame)
    if target == 418988:
        from .business_highbank import build_ten_officer_selection_fields
        return build_ten_officer_selection_fields(state, frame)
    if target == 89574:
        from .business_gameplay import render_visible_map_packets_fields
        return render_visible_map_packets_fields(state, frame)
    if target == 92586:
        from .business_gameplay import render_city_map_entries_fields
        return render_city_map_entries_fields(state, frame)
    if target in (158714, 423666):
        from ..high_level_remaining_flows.business_city import execute_deployment_menu_fields
        return execute_deployment_menu_fields(state, target, frame)
    if target == 22660:
        from ..high_level_remaining_flows.business_lowbank import lowbank_select_live_state_22_fields
        return lowbank_select_live_state_22_fields(state, frame)
    if target in (1044, 21478, 37776, 41394, 41592, 57198, 199008, 199022, 199358, 199366, 421918, 262850, 418260, 418484, 418500):
        from .contexts_display_fields import display_child_fields
        return display_child_fields(state, frame, target)
    if target in (72946, 73258, 73276, 73602, 73722, 73736, 73764, 73828, 74268, 74386, 74516, 74776, 75052, 75180, 75266, 75296, 75404, 75474, 75504, 75530, 75616, 75660, 75896, 76002, 76076, 76160, 76254, 76280, 76334, 76366, 76440, 76470, 76500, 76620, 76650, 76736, 76812, 76932, 76990, 77044, 77186, 77308, 77428, 77656, 77876, 77930, 78198, 78216, 78364, 78448, 79120, 79166, 79300, 79586, 79604, 79690, 80180, 80216, 80516, 80534, 80774, 80858, 81022, 81398, 81554, 81772, 81834, 81892):
        from ..high_level_player_commands.contexts_command_fields import execute_command_menu_scene_fields
        return execute_command_menu_scene_fields(state, target, frame)
    if target == 1084:
        return toggle_officer_roster_selection_fields(state, frame)
    if target == 2278:
        return calculate_action_budget_fields(state, frame)
    if target == 2434:
        return toggle_officer_roster_selection_fields(state, frame)
    if target == 2634:
        return advance_unselected_roster_cursor_fields(state, frame)
    if target == 3856:
        return update_campaign_control_fields(state, frame)
    if target == 3992:
        return advance_campaign_palette_transition_fields(state, frame)
    if target == 4316:
        return process_campaign_mode_control_fields(state, frame)
    if target == 4518:
        return detect_unassigned_packed_leaders_fields(state, frame)
    if target == 4590:
        return detect_unassigned_leader_roster_fields(state, frame)
    if target == 4648:
        return update_outside_map_indicator_fields(state, frame)
    if target == 4752:
        return move_campaign_map_pointer_fields(state, frame)
    if target == 4922:
        return clear_pointer_cost_caches_fields(state, frame)
    if target == 4932:
        return draw_campaign_pointer_marker_fields(state, frame)
    if target == 5084:
        return detect_unlisted_campaign_owner_fields(state, frame)
    if target == 5126:
        return detect_uniform_campaign_owner_fields(state, frame)
    if target == 5188:
        return advance_campaign_entry_fade_fields(state, frame)
    if target == 5344:
        return process_campaign_location_choice_fields(state, frame)
    if target == 5498:
        return select_campaign_location_fields(state, frame)
    if target == 5566:
        return clamp_campaign_camera_targets_fields(state, frame)
    if target == 5628:
        return wait_for_campaign_location_confirmation_fields(state, frame)
    if target == 5662:
        return process_campaign_camera_transition_fields(state, frame)
    if target == 5812:
        return scroll_campaign_camera_toward_pointer_fields(state, frame)
    if target == 6040:
        return dispatch_campaign_selection_phase_fields(state, frame)
    if target == 6138:
        return queue_campaign_selection_refresh_fields(state, frame)
    if target == 6150:
        return prepare_campaign_selection_mode_fields(state, frame)
    if target == 6302:
        return advance_campaign_selection_phase_fields(state, frame)
    if target == 6308:
        return initialize_campaign_selection_mode_fields(state, frame)
    if target == 6516:
        return append_campaign_selection_frame_fields(state, frame)
    if target == 6604:
        return update_campaign_selection_delay_fields(state, frame)
    if target == 6768:
        return process_campaign_selection_input_fields(state, frame)
    if target == 7186:
        return validate_campaign_roster_action_fields(state, frame)
    if target == 7418:
        return expire_campaign_selection_frame_fields(state, frame)
    if target == 7448:
        return append_campaign_frame_progress_fields(state, frame)
    if target == 7518:
        return advance_campaign_frame_phase_fields(state, frame)
    if target == 7524:
        return append_campaign_confirmation_frame_fields(state, frame)
    if target == 7630:
        return refresh_campaign_confirmation_fields(state, frame)
    if target == 7638:
        return finish_campaign_selection_fields(state, frame)
    if target == 7656:
        return process_campaign_roster_commands_fields(state, frame)
    if target == 8196:
        return trigger_campaign_selection_audio_fields(state, frame)
    if target == 8234:
        return update_campaign_selection_audio_fields(state, frame)
    if target == 8272:
        return animate_campaign_selection_glyph_fields(state, frame)
    if target == 8376:
        return announce_selected_assignment_fields(state, frame)
    if target == 8432:
        return initialize_assignment_confirmation_fields(state, frame)
    if target == 8552:
        return process_assignment_confirmation_input_fields(state, frame)
    if target == 8636:
        return upload_assignment_confirmation_glyph_fields(state, frame)
    if target == 8690:
        return remove_selected_assignment_fields(state, frame)
    if target == 8750:
        return process_campaign_exit_input_fields(state, frame)
    if target == 8782:
        return dispatch_campaign_post_selection_phase_fields(state, frame)
    if target == 9206:
        return draw_campaign_fade_marker_fields(state, frame)
    if target == 9238:
        return dispatch_campaign_subcommand_phase_fields(state, frame)
    if target == 14044:
        return update_personnel_command_phase_fields(state, frame)
    if target == 14064:
        return update_city_command_phase_fields(state, frame)
    if target == 14078:
        return update_support_command_phase_fields(state, frame)
    if target == 14092:
        return update_tactical_command_phase_fields(state, frame)
    if target == 14106:
        return update_battle_command_phase_fields(state, frame)
    if target == 14120:
        return exit_post_campaign_message_fields(state, frame)
    if target == 14144:
        return dismiss_campaign_warning_fields(state, frame)
    if target == 25880:
        from .business_movement_support import build_path_fields
        return build_path_fields(state, frame)
    if target == 40988:
        from .business_map import refresh_map_tiles_around_cursor_fields
        return refresh_map_tiles_around_cursor_fields(state, frame)
    if target == 41164:
        from .business_map import render_map_column_fields
        return render_map_column_fields(state, frame)
    if target == 41228:
        from .business_map import render_map_row_fields
        return render_map_row_fields(state, frame)
    if target == 25804:
        from .business_map import scan_candidate_roster_status_fields
        return scan_candidate_roster_status_fields(state, frame)
    if target == 22164:
        from .business_commands import start_selection_prompt_fields
        return start_selection_prompt_fields(state, frame)
    if target == 42288:
        from .business_commands import update_selected_force_prompt_fields
        return update_selected_force_prompt_fields(state, frame)
    if target == 20048:
        from .business_commands import collect_city_officers_for_menu_fields
        return collect_city_officers_for_menu_fields(state, frame)
    if target == 32906:
        from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        return enqueue_sound_command_fields(SceneRefreshMemory(state), frame)
    if target == 44682:
        from ..high_level_scene_flows.business_scene import decode_glyph_rows_to_buffers_fields
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        return decode_glyph_rows_to_buffers_fields(SceneRefreshMemory(state), frame)
    if target == 24444:
        from .business_map import select_previous_command_officer_frame_fields
        return select_previous_command_officer_frame_fields(state, frame)
    if target == 24984:
        from .business_map import select_next_command_officer_frame_fields
        return select_next_command_officer_frame_fields(state, frame)
    if target == 25338:
        from .business_map import adjust_selected_roster_member_frame_fields
        return adjust_selected_roster_member_frame_fields(state, frame)
    if target == 39990:
        from .business_map import refresh_world_map_scroll_frame_fields
        return refresh_world_map_scroll_frame_fields(state, frame)
    if target == 40542:
        from .business_map import update_world_cursor_from_inputs_frame_fields
        return update_world_cursor_from_inputs_frame_fields(state, frame)
    if target == 41294:
        from .business_map import refresh_world_cursor_attributes_frame_fields
        return refresh_world_cursor_attributes_frame_fields(state, frame)
    if target == 41304:
        from .business_map import refresh_world_cursor_attributes_alternate_1_frame_fields
        return refresh_world_cursor_attributes_alternate_1_frame_fields(state, frame)
    if target == 22496:
        from .business_commands import compose_command_selection_prompt_frame_fields
        return compose_command_selection_prompt_frame_fields(state, frame)
    if target == 22632:
        from .business_commands import set_command_selection_cursor_frame_fields
        return set_command_selection_cursor_frame_fields(state, frame)
    if target == 23082:
        from .business_commands import store_command_selection_value_frame_fields
        return store_command_selection_value_frame_fields(state, frame)
    if target == 23106:
        from .business_commands import append_command_selection_heading_frame_fields
        return append_command_selection_heading_frame_fields(state, frame)
    if target == 23168:
        from .business_commands import append_command_confirmation_row_frame_fields
        return append_command_confirmation_row_frame_fields(state, frame)
    if target == 23228:
        from .business_commands import present_current_command_prompt_frame_fields
        return present_current_command_prompt_frame_fields(state, frame)
    if target == 23704:
        from .business_commands import present_command_warning_frame_fields
        return present_command_warning_frame_fields(state, frame)
    if target == 41840:
        from .business_commands import append_contextual_cursor_commands_frame_fields
        return append_contextual_cursor_commands_frame_fields(state, frame)
    if target == 42188:
        from .business_commands import draw_first_force_prompt_frame_fields
        return draw_first_force_prompt_frame_fields(state, frame)
    if target == 42246:
        from .business_commands import draw_second_force_prompt_frame_fields
        return draw_second_force_prompt_frame_fields(state, frame)
    if target == 43300:
        from .business_commands import compose_title_option_panel_frame_fields
        return compose_title_option_panel_frame_fields(state, frame)
    if target == 43482:
        from .business_commands import append_title_option_glyphs_frame_fields
        return append_title_option_glyphs_frame_fields(state, frame)
    if target == 43518:
        from .business_commands import append_title_option_digit_frame_fields
        return append_title_option_digit_frame_fields(state, frame)
    if target == 43572:
        from .business_commands import store_title_option_digit_frame_fields
        return store_title_option_digit_frame_fields(state, frame)
    if target == 43596:
        from .business_commands import set_title_option_marker_frame_fields
        return set_title_option_marker_frame_fields(state, frame)
    if target == 43636:
        from .business_commands import append_title_option_decorations_frame_fields
        return append_title_option_decorations_frame_fields(state, frame)
    if target == 43792:
        from .business_commands import append_title_option_decoration_value_frame_fields
        return append_title_option_decoration_value_frame_fields(state, frame)
    if target == 43840:
        from .business_commands import append_world_cursor_coordinates_frame_fields
        return append_world_cursor_coordinates_frame_fields(state, frame)
    if target == 49438:
        from .business_commands import set_roster_selection_notice_frame_fields
        return set_roster_selection_notice_frame_fields(state, frame)
    if target == 50542:
        from .business_commands import append_force_relation_label_frame_fields
        return append_force_relation_label_frame_fields(state, frame)
    if target == 50576:
        from .business_commands import append_force_relation_digits_frame_fields
        return append_force_relation_digits_frame_fields(state, frame)
    if target == 51044:
        from .business_commands import adjust_force_relation_selection_frame_fields
        return adjust_force_relation_selection_frame_fields(state, frame)
    if target == 51088:
        from .business_commands import confirm_force_relation_selection_frame_fields
        return confirm_force_relation_selection_frame_fields(state, frame)
    if target == 55114:
        from .business_commands import append_selected_city_command_frame_fields
        return append_selected_city_command_frame_fields(state, frame)
    if target == 55452:
        from .business_commands import store_selected_city_command_value_frame_fields
        return store_selected_city_command_value_frame_fields(state, frame)
    if target == 55470:
        from .business_commands import append_city_command_heading_frame_fields
        return append_city_command_heading_frame_fields(state, frame)
    if target == 55532:
        from .business_commands import append_current_command_description_frame_fields
        return append_current_command_description_frame_fields(state, frame)
    if target == 55584:
        from .business_commands import choose_command_description_source_frame_fields
        return choose_command_description_source_frame_fields(state, frame)
    if target == 55852:
        from .business_commands import append_command_description_rows_frame_fields
        return append_command_description_rows_frame_fields(state, frame)
    if target == 55950:
        from .business_commands import append_command_description_status_frame_fields
        return append_command_description_status_frame_fields(state, frame)
    if target == 19122:
        from .business_commands import compose_current_city_frame_fields
        return compose_current_city_frame_fields(state, frame)
    if target == 19240:
        from .business_commands import start_current_city_packet_fields
        return start_current_city_packet_fields(state, frame)
    if target == 23752:
        from .business_map import locate_city_at_world_cursor_fields
        return locate_city_at_world_cursor_fields(state, frame)
    if target == 25610:
        from .business_map import scan_roster_selection_status_fields
        return scan_roster_selection_status_fields(state, frame)
    if target == 40468:
        from .business_map import locate_map_object_record_fields
        return locate_map_object_record_fields(state, frame)
    if target == 40828:
        from .business_map import queue_map_strip_transfer_fields
        return queue_map_strip_transfer_fields(state, frame)
    if target == 50126:
        from .business_commands import append_force_relation_commands_fields
        return append_force_relation_commands_fields(state, frame)
    if target == 106862:
        from .business_gameplay import select_active_battle_controller_fields
        return select_active_battle_controller_fields(state, frame)
    if target == 23278:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_74_fields
        return lowbank_coordinate_live_state_74_fields(state, frame)
    if target == 23368:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_75_fields
        return lowbank_coordinate_live_state_75_fields(state, frame)
    if target == 23388:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_75_ordinary_fields
        return lowbank_coordinate_live_state_75_ordinary_fields(state, frame)
    if target == 24392:
        from ..high_level_gameplay_flow.business_battle import build_roster_fields
        from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
        return build_roster_fields(BattlePresentationMemory(state), frame)
    if target == 44048:
        from ..high_level_player_commands.business_display import append_live_command_sprite_fields
        from ..high_level_player_commands.contexts_display import SpritePacketMemory
        return append_live_command_sprite_fields(SpritePacketMemory(state), frame, reset_scroll=False, initialize_clip=True)
    if target == 20496:
        from .business_commands import append_current_roster_marks_frame_fields
        return append_current_roster_marks_frame_fields(state, frame)
    if target == 20588:
        from .business_commands import render_current_city_command_labels_frame_fields
        return render_current_city_command_labels_frame_fields(state, frame)
    if target == 21058:
        from .business_commands import compose_city_roster_rows_frame_fields
        return compose_city_roster_rows_frame_fields(state, frame)
    if target == 21296:
        from .business_commands import compose_selected_force_rows_frame_fields
        return compose_selected_force_rows_frame_fields(state, frame)
    if target == 21406:
        from .business_commands import append_city_relation_row_frame_fields
        return append_city_relation_row_frame_fields(state, frame)
    if target == 21706:
        from .business_commands import render_roster_name_or_prompt_frame_fields
        return render_roster_name_or_prompt_frame_fields(state, frame)
    if target == 21860:
        from .business_commands import render_selected_city_packet_frame_fields
        return render_selected_city_packet_frame_fields(state, frame)
    if target == 21968:
        from .business_commands import append_force_roster_names_frame_fields
        return append_force_roster_names_frame_fields(state, frame)
    if target == 22432:
        from .business_commands import append_selected_force_head_frame_fields
        return append_selected_force_head_frame_fields(state, frame)
    if target == 42070:
        from .business_commands import draw_force_summary_frame_fields
        return draw_force_summary_frame_fields(state, frame)
    if target == 42530:
        from .business_commands import draw_current_scenario_prompt_frame_fields
        return draw_current_scenario_prompt_frame_fields(state, frame)
    if target == 42622:
        from .business_commands import append_scenario_owner_glyphs_frame_fields
        return append_scenario_owner_glyphs_frame_fields(state, frame)
    if target == 42794:
        from .business_commands import append_scenario_owner_value_frame_fields
        return append_scenario_owner_value_frame_fields(state, frame)
    if target == 43054:
        from .business_commands import draw_title_mode_prompt_frame_fields
        return draw_title_mode_prompt_frame_fields(state, frame)
    if target == 45702:
        from .business_commands import draw_roster_overview_frame_fields
        return draw_roster_overview_frame_fields(state, frame)
    if target == 46100:
        from .business_commands import append_roster_overview_cursor_frame_fields
        return append_roster_overview_cursor_frame_fields(state, frame)
    if target == 46308:
        from .business_commands import draw_roster_overview_values_frame_fields
        return draw_roster_overview_values_frame_fields(state, frame)
    if target == 46520:
        from .business_commands import append_selected_city_head_frame_fields
        return append_selected_city_head_frame_fields(state, frame)
    if target == 46624:
        from .business_commands import append_roster_overview_digit_frame_fields
        return append_roster_overview_digit_frame_fields(state, frame)
    if target == 46688:
        from .business_commands import retain_roster_overview_column_frame_fields
        return retain_roster_overview_column_frame_fields(state, frame)
    if target == 46884:
        from .business_commands import compose_officer_detail_panel_frame_fields
        return compose_officer_detail_panel_frame_fields(state, frame)
    if target == 47594:
        from .business_commands import append_officer_attribute_value_frame_fields
        return append_officer_attribute_value_frame_fields(state, frame)
    if target == 47672:
        from .business_commands import scale_officer_detail_value_frame_fields
        return scale_officer_detail_value_frame_fields(state, frame)
    if target == 47708:
        from .business_commands import append_officer_detail_commands_frame_fields
        return append_officer_detail_commands_frame_fields(state, frame)
    if target == 47802:
        from .business_commands import append_officer_detail_title_frame_fields
        return append_officer_detail_title_frame_fields(state, frame)
    if target == 47850:
        from .business_commands import draw_officer_detail_view_frame_fields
        return draw_officer_detail_view_frame_fields(state, frame)
    if target == 47910:
        from .business_commands import append_officer_detail_rows_frame_fields
        return append_officer_detail_rows_frame_fields(state, frame)
    if target == 49334:
        from .business_commands import open_roster_selection_message_frame_fields
        return open_roster_selection_message_frame_fields(state, frame)
    if target == 50034:
        from .business_commands import draw_force_relation_view_frame_fields
        return draw_force_relation_view_frame_fields(state, frame)
    if target == 51384:
        from .business_commands import draw_command_cost_panel_frame_fields
        return draw_command_cost_panel_frame_fields(state, frame)
    if target == 52512:
        from .business_commands import draw_command_cost_panel_alternate_1_frame_fields
        return draw_command_cost_panel_alternate_1_frame_fields(state, frame)
    if target == 56096:
        from .business_commands import draw_diplomacy_command_panel_frame_fields
        return draw_diplomacy_command_panel_frame_fields(state, frame)
    if target == 44830:
        from ..high_level_scene_flows.business_scene import expand_glyph_stream_fields
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        return expand_glyph_stream_fields(SceneRefreshMemory(state), frame)
    if target == 44872:
        from ..high_level_gameplay_flow.business_services import refresh_gameplay_scene_fields
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        return refresh_gameplay_scene_fields(SceneRefreshMemory(state), frame)
    if target == 26830:
        from ..high_level_gameplay_flow.business_services import clear_video_sprite_plane_fields
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        return clear_video_sprite_plane_fields(SceneRefreshMemory(state), frame)
    if target == 33042:
        from ..high_level_gameplay_flow.business_services import copy_video_transfer_descriptor_fields
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        return copy_video_transfer_descriptor_fields(SceneRefreshMemory(state), frame)
    if target == 199284:
        from ..high_level_gameplay_flow.business_services import present_gameplay_message_fields
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        return present_gameplay_message_fields(SceneRefreshMemory(state), frame)
    if target == 47404:
        from .business_commands import append_officer_name_value_fields
        return append_officer_name_value_fields(state, frame)
    if target == 47416:
        from .business_commands import append_officer_name_value_alternate_1_fields
        return append_officer_name_value_alternate_1_fields(state, frame)
    if target == 47436:
        from .business_commands import append_officer_name_value_alternate_2_fields
        return append_officer_name_value_alternate_2_fields(state, frame)
    if target == 47448:
        from .business_commands import append_officer_name_value_alternate_3_fields
        return append_officer_name_value_alternate_3_fields(state, frame)
    if target == 47490:
        from .business_commands import append_officer_name_value_alternate_4_fields
        return append_officer_name_value_alternate_4_fields(state, frame)
    if target == 53230:
        from .business_commands import divide_and_scale_command_value_fields
        return divide_and_scale_command_value_fields(state, frame)
    if target == 56560:
        from .business_commands import append_diplomacy_command_choices_fields
        return append_diplomacy_command_choices_fields(state, frame)
    if target == 984:
        return process_startup_scene_fields(state, frame)
    if target == 988:
        return reset_menu_sprite_slots_fields(state, frame)
    if target == 1012:
        return refresh_information_panel_fields(state, frame)
    if target == 1016:
        return initialize_campaign_screen_fields(state, frame)
    if target == 1020:
        return continue_platform_scene_initialization_fields(state, frame)
    if target == 1024:
        return upload_selected_dictionary_panel_fields(state, frame)
    if target == 1028:
        return initialize_campaign_options_fields(state, frame)
    if target == 1032:
        return initialize_campaign_menu_panels_fields(state, frame)
    if target == 1036:
        return initialize_campaign_command_panel_fields(state, frame)
    if target == 1040:
        return initialize_officer_detail_panel_fields(state, frame)
    if target == 1048:
        return initialize_city_detail_panel_fields(state, frame)
    if target == 1052:
        return initialize_city_command_panel_fields(state, frame)
    if target == 1056:
        return upload_formation_caption_fields(state, frame)
    if target == 1060:
        return upload_formation_choice_caption_fields(state, frame)
    if target == 1064:
        return initialize_formation_choices_fields(state, frame)
    if target == 1068:
        return initialize_city_choice_caption_fields(state, frame)
    if target == 1072:
        return request_affordable_action_panel_fields(state, frame)
    if target == 1076:
        return initialize_campaign_map_fields(state, frame)
    if target == 1080:
        return initialize_officer_portrait_fields(state, frame)
    if target == 1088:
        return initialize_education_screen_fields(state, frame)
    if target == 1092:
        return initialize_assignment_description_fields(state, frame)
    if target == 1096:
        return initialize_assignment_choices_fields(state, frame)
    if target == 1100:
        return upload_assignment_caption_fields(state, frame)
    if target == 1104:
        return initialize_training_screen_fields(state, frame)
    if target == 1108:
        return initialize_training_candidate_fields(state, frame)
    if target == 1112:
        return update_training_candidate_fields(state, frame)
    if target == 1116:
        return initialize_learning_screen_fields(state, frame)
    if target == 1120:
        return update_learning_candidate_fields(state, frame)
    if target == 1124:
        return initialize_officer_transfer_screen_fields(state, frame)
    if target == 1128:
        return update_officer_transfer_candidate_fields(state, frame)
    if target == 1132:
        return initialize_city_transfer_screen_fields(state, frame)
    if target == 1136:
        return initialize_city_transfer_details_fields(state, frame)
    if target == 1140:
        return initialize_city_transfer_choices_fields(state, frame)
    if target == 1144:
        return initialize_officer_search_screen_fields(state, frame)
    if target == 1148:
        return initialize_officer_search_details_fields(state, frame)
    if target == 1152:
        return initialize_officer_search_choices_fields(state, frame)
    if target == 1156:
        return initialize_support_command_screen_fields(state, frame)
    if target == 1160:
        return initialize_support_result_screen_fields(state, frame)
    if target == 1164:
        return initialize_battle_deployment_screen_fields(state, frame)
    if target == 1168:
        return initialize_battle_order_screen_fields(state, frame)
    if target == 1172:
        return wait_and_initialize_campaign_action_fields(state, frame)
    if target == 1176:
        return continue_campaign_action_display_fields(state, frame)
    if target == 1180:
        return return_campaign_idle_slot_fields(state, frame)
    if target == 1184:
        return initialize_tactical_scene_fields(state, frame)
    if target == 1188:
        return initialize_tactical_selection_scene_fields(state, frame)
    if target == 1192:
        return initialize_battle_scene_fields(state, frame)
    if target == 1196:
        return initialize_duel_scene_fields(state, frame)
    if target == 1200:
        return initialize_post_duel_campaign_fields(state, frame)
    if target == 1204:
        return begin_nonreturning_scripted_scene_fields(state, frame)
    if target == 1208:
        return initialize_campaign_audio_scene_fields(state, frame)
    if target == 1212:
        return initialize_campaign_status_panel_fields(state, frame)
    if target == 1216:
        return initialize_campaign_summary_panel_fields(state, frame)
    if target == 1220:
        return upload_three_formation_names_fields(state, frame)
    if target == 3750:
        return upload_three_formation_names_direct_fields(state, frame)
    if target == 1888:
        return read_selected_formation_preferences_fields(state, frame)
    if target == 1930:
        return find_first_enabled_formation_fields(state, frame)
    if target == 1944:
        return load_city_formation_preferences_fields(state, frame)
    if target == 18576:
        from .business_lowbank import poll_world_map_input_fields
        return poll_world_map_input_fields(state, frame)
    if target == 18840:
        from .business_lowbank import upload_world_map_palette_fields
        return upload_world_map_palette_fields(state, frame)
    if target == 20996:
        from .business_lowbank import draw_scene_header_glyphs_fields
        return draw_scene_header_glyphs_fields(state, frame)
    if target == 21186:
        from .business_lowbank import upload_selection_layout_fields
        return upload_selection_layout_fields(state, frame)
    if target == 21360:
        from .business_lowbank import draw_scene_footer_glyphs_fields
        return draw_scene_footer_glyphs_fields(state, frame)
    if target == 21936:
        from .business_lowbank import draw_current_resource_glyphs_fields
        return draw_current_resource_glyphs_fields(state, frame)
    if target == 26548:
        from .business_lowbank import configure_controller_outputs_fields
        return configure_controller_outputs_fields(state, frame)
    if target == 26570:
        from .business_lowbank import poll_controller_with_z80_bus_fields
        return poll_controller_with_z80_bus_fields(state, frame)
    if target == 26600:
        from .business_lowbank import poll_two_controller_ports_fields
        return poll_two_controller_ports_fields(state, frame)
    if target == 26614:
        from .business_lowbank import poll_two_controller_ports_alternate_1_fields
        return poll_two_controller_ports_alternate_1_fields(state, frame)
    if target == 26960:
        from .business_lowbank import initialize_z80_sound_image_fields
        return initialize_z80_sound_image_fields(state, frame)
    if target == 27064:
        from .business_lowbank import release_z80_reset_fields
        return release_z80_reset_fields(state, frame)
    if target == 33012:
        from .business_lowbank import queue_sound_word_list_fields
        return queue_sound_word_list_fields(state, frame)
    if target == 37872:
        from .business_lowbank import initialize_scene_growth_and_tiles_fields
        return initialize_scene_growth_and_tiles_fields(state, frame)
    if target == 42848:
        from .business_lowbank import upload_selected_mode_tile_rows_fields
        return upload_selected_mode_tile_rows_fields(state, frame)
    if target == 42894:
        from .business_lowbank import upload_selected_tile_row_fields
        return upload_selected_tile_row_fields(state, frame)
    if target == 18966:
        from ..high_level_gameplay_flow.business_services import _reset_scene_input_marker_fields, _scene_refresh_flags
        from ..high_level_gameplay_flow.contexts_services import MarkerResetMemory, SceneRefreshMemory
        _reset_scene_input_marker_fields(MarkerResetMemory(state))
        return _scene_refresh_flags(SceneRefreshMemory(state), frame, 0, 2)
    if target == 81224:
        from .business_gameplay import dispatch_gameplay_command_state_fields
        return dispatch_gameplay_command_state_fields(state, frame)
    if target == 91744:
        from .business_gameplay import dispatch_queue_command_state_fields
        return dispatch_queue_command_state_fields(state, frame)
    if target == 201416:
        from .business_scene_support import dispatch_city_assignment_state_fields
        return dispatch_city_assignment_state_fields(state, frame)
    if target == 420852:
        from .business_highbank import dispatch_highbank_command_state_fields
        return dispatch_highbank_command_state_fields(state, frame)
    if target == 118616:
        from .business_gameplay import update_direction_choice_fields
        return update_direction_choice_fields(state, frame)
    if target == 422326:
        from .business_highbank import advance_scrolling_message_fields
        return advance_scrolling_message_fields(state, frame)
    if target == 67220:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_113_fields
        return lowbank_coordinate_live_state_113_fields(state, frame)
    if target == 1548:
        from ..high_level_gameplay_flow.business_services import clear_scene_video_and_state_fields
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        return clear_scene_video_and_state_fields(SceneRefreshMemory(state), frame)
    raise MovementContinuationBoundary(target, frame, 'actual campaign child full ABI not restored; caller LONG already committed')


def _campaign_legacy_observations_fields(state: SceneState, legacy, role: str) -> FirstDeploymentFrame:
    """Closed adapters retain the old observations only, not nonexistent A6 or SR-X values."""
    checked_state(state)
    if legacy is None:
        return FirstDeploymentFrame.unobserved()
    if role=='location_input':
        if type(legacy) is not LocationChoiceInput:
            raise ValueError('actual historical location input required')
        legacy.validate(state)
        legacy=legacy.frame
        role='location'
    if role=='location':
        if type(legacy) is not LocationChoiceFrame:
            raise ValueError('actual historical location frame required')
        legacy.validate(state)
        return first_replace(FirstDeploymentFrame.unobserved(),target_x=legacy.motion_value,target_y=legacy.prompt_field,unit=legacy.sprite_attributes,roster=legacy.sprite_source,candidates=legacy.palette_source,auxiliary=legacy.vdp_port,stack_cursor=legacy.stack_cursor)
    if role in ('camera','transition'):
        expected=CameraMotionInput if role=='camera' else CameraTransitionInput
        if type(legacy) is not expected:
            raise ValueError('actual historical camera input required')
        legacy.validate(state)
        return first_replace(FirstDeploymentFrame.unobserved(),target_x=legacy.value,target_y=legacy.field,unit=legacy.tile,count=legacy.row,distance=legacy.offset,offset_x=legacy.limit,offset_y=legacy.member,choice=legacy.remaining,roster=legacy.destination,candidates=legacy.source,controller=legacy.descriptor,scan=legacy.records,opponent=legacy.palette,scratch=legacy.roster,stack_cursor=legacy.stack_cursor)
    if role=='world':
        checked_tick_frame(legacy,state)
        return first_replace(FirstDeploymentFrame.unobserved(),target_x=legacy.motion_x,target_y=legacy.motion_y,unit=legacy.attributes,count=legacy.tile_count,distance=legacy.officer,offset_x=legacy.count,offset_y=legacy.index,choice=legacy.control_latch,roster=legacy.source,candidates=legacy.destination,controller=legacy.packet,auxiliary=legacy.vdp_port,stack_cursor=legacy.stack_cursor)
    raise ValueError('closed original world/camera/location observation role required')


# Complete current campaign/controller successor; real devices remain real boundaries.
"""Campaign stage setup and formation preferences using the complete live frame.

Physical dispatch-table BRA entries reuse their incoming call slot. Real child
calls retain the original LONG return tokens; devices never become fake RAM.
"""

from .business_map import _world_map_bit_fields


def process_startup_scene_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3D8: process startup scene; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x3D8)
    frame=_campaign_call_fields(state,frame,0x93F0,0x4EE)
    return frame


def refresh_information_panel_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3F4: refresh information panel; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x3F4)
    frame=_campaign_call_fields(state,frame,0xA622,0xE82)
    return frame


def continue_platform_scene_initialization_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3FC: continue platform scene initialization; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x3FC)
    return _campaign_tail_fields(state,frame,0x60C)


def initialize_campaign_options_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """404: initialize campaign options; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x404)
    frame=_campaign_call_fields(state,frame,0xBAEA,0x55C)
    return frame


def initialize_campaign_command_panel_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """40C: initialize campaign command panel; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x40C)
    frame=_campaign_call_fields(state,frame,0xC372,0x564)
    return frame


def initialize_city_detail_panel_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """418: initialize city detail panel; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x418)
    frame=_campaign_call_fields(state,frame,0xC8B8,0x574)
    return frame


def initialize_city_command_panel_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """41C: initialize city command panel; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x41C)
    frame=_campaign_call_fields(state,frame,0xCD20,0x56C)
    return frame


def initialize_campaign_map_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """434: initialize campaign map; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x434)
    frame=_campaign_call_fields(state,frame,0xDF6E,0x8E4)
    return frame


def initialize_assignment_choices_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """448: initialize assignment choices; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x448)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_movement_move(state,frame,'target_x',0x1,16)
    frame=_movement_move(state,frame,'target_y',0x3,16)
    frame=_campaign_call_fields(state,frame,0x506C,0xC40)
    frame=_campaign_call_fields(state,frame,0xAF48,0xC46)
    frame=_campaign_emit_fields(state,frame,0xC46,0xFFFFF37E,0,clear=True)
    return frame


def initialize_training_screen_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """450: initialize training screen; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x450)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x16ACC,0xC9A)
    frame=_campaign_call_fields(state,frame,0xAF48,0xCA0)
    return frame


def initialize_training_candidate_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """454: initialize training candidate; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x454)
    frame=_campaign_call_fields(state,frame,0x16B3A,0xCA8)
    frame=_campaign_emit_fields(state,frame,0xCA8,0xFFFFF376,0xFFFE)
    return frame


def update_training_candidate_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """458: update training candidate; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x458)
    frame=_campaign_call_fields(state,frame,0x17602,0xCB6)
    return frame


def initialize_learning_screen_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """45C: initialize learning screen; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x45C)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x177BE,0xCC2)
    frame=_campaign_call_fields(state,frame,0xAF48,0xCC8)
    return frame


def update_learning_candidate_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """460: update learning candidate; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x460)
    frame=_campaign_call_fields(state,frame,0x17A16,0xCD0)
    return frame


def initialize_officer_transfer_screen_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """464: initialize officer transfer screen; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x464)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x17A5A,0xCDC)
    frame=_campaign_call_fields(state,frame,0xAF48,0xCE2)
    return frame


def update_officer_transfer_candidate_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """468: update officer transfer candidate; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x468)
    frame=_campaign_call_fields(state,frame,0x17A9E,0xCEA)
    return frame


def initialize_city_transfer_screen_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """46C: initialize city transfer screen; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x46C)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x17C8A,0xCF6)
    frame=_campaign_call_fields(state,frame,0xAF48,0xCFC)
    return frame


def initialize_city_transfer_details_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """470: initialize city transfer details; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x470)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x17EDE,0xD08)
    return frame


def initialize_city_transfer_choices_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """474: initialize city transfer choices; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x474)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x17F30,0xD14)
    frame=_campaign_call_fields(state,frame,0xAF48,0xD1A)
    return frame


def initialize_officer_search_screen_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """478: initialize officer search screen; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x478)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x183F8,0xD26)
    frame=_campaign_call_fields(state,frame,0xAF48,0xD2C)
    return frame


def initialize_officer_search_details_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """47C: initialize officer search details; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x47C)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x1874A,0xD38)
    return frame


def initialize_officer_search_choices_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """480: initialize officer search choices; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x480)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x18792,0xD44)
    frame=_campaign_call_fields(state,frame,0xAF48,0xD4A)
    return frame


def initialize_support_command_screen_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """484: initialize support command screen; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x484)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x30960,0xD56)
    frame=_campaign_call_fields(state,frame,0xAF48,0xD5C)
    return frame


def initialize_support_result_screen_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """488: initialize support result screen; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x488)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x34F26,0xD68)
    frame=_campaign_call_fields(state,frame,0xAF48,0xD6E)
    return frame


def initialize_battle_deployment_screen_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """48C: initialize battle deployment screen; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x48C)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x24AD0,0xD7A)
    frame=_campaign_call_fields(state,frame,0xAF48,0xD80)
    return frame


def initialize_battle_order_screen_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """490: initialize battle order screen; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x490)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x221E4,0xD8C)
    frame=_campaign_call_fields(state,frame,0xAF48,0xD92)
    return frame


def continue_campaign_action_display_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """498: continue campaign action display; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x498)
    return _campaign_tail_fields(state,frame,0xDC0)


def return_campaign_idle_slot_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """49C: return campaign idle slot; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x49C)
    return frame


def initialize_tactical_scene_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4A0: initialize tactical scene; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x4A0)
    frame=_campaign_call_fields(state,frame,0x664AC,0xE8C)
    frame=_campaign_call_fields(state,frame,0xAF48,0xE92)
    return frame


def initialize_tactical_selection_scene_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4A4: initialize tactical selection scene; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x4A4)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x66616,0xE9E)
    frame=_campaign_call_fields(state,frame,0xAF48,0xEA4)
    return frame


def initialize_battle_scene_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4A8: initialize battle scene; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x4A8)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x1BFEC,0x4FA)
    frame=_campaign_call_fields(state,frame,0xAF48,0x500)
    return frame


def initialize_duel_scene_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4AC: initialize duel scene; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x4AC)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x25BD8,0x50C)
    frame=_campaign_call_fields(state,frame,0xAF48,0x512)
    return frame


def begin_nonreturning_scripted_scene_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4B4: begin nonreturning scripted scene; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x4B4)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x3B732,0x580)
    return frame


def initialize_campaign_audio_scene_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4B8: initialize campaign audio scene; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x4B8)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x6701E,0x58C)
    frame=_campaign_call_fields(state,frame,0xAF48,0x592)
    return frame


def initialize_campaign_status_panel_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4BC: initialize campaign status panel; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x4BC)
    frame=_campaign_call_fields(state,frame,0xA456,0x59A)
    return frame


def initialize_campaign_summary_panel_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4C0: initialize campaign summary panel; original stage and child tokens."""
    frame=_city_ui_frame_fields(state,frame,0x4C0)
    frame=_campaign_call_fields(state,frame,0xDB20,0x5A2)
    return frame


def read_selected_formation_preferences_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """760..78A: load three city masks and store their first enabled formation indices."""
    frame=_city_ui_frame_fields(state,frame,0x760)
    frame=_campaign_call_fields(state,frame,0x798,0x764)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFEFB2,2),16)
    frame=_campaign_call_fields(state,frame,0x78A,0x76C)
    frame=_campaign_emit_fields(state,frame,0x76C,0xFFFFEF64,low16(frame.target_y))
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFEFB4,2),16)
    frame=_campaign_call_fields(state,frame,0x78A,0x778)
    frame=_campaign_emit_fields(state,frame,0x778,0xFFFFEF66,low16(frame.target_y))
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFEFB6,2),16)
    frame=_campaign_call_fields(state,frame,0x78A,0x784)
    return _campaign_emit_fields(state,frame,0x784,0xFFFFEF68,low16(frame.target_y))


def find_first_enabled_formation_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """78A..798: register BTST search; a zero mask keeps the original endless loop."""
    frame=_city_ui_frame_fields(state,frame,0x78A)
    frame=_movement_move(state,frame,'target_y',0,16)
    while True:
        frame=_world_map_bit_fields(state,frame,frame.target_x,low16(frame.target_y)&31)
        if not frame.status&4:
            return frame
        frame=_city_ui_arithmetic_fields(state,frame,'target_y',1)


def load_city_formation_preferences_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """798..7BC: original three-BYTE table lookup retains the live register high words."""
    frame=_city_ui_frame_fields(state,frame,0x798)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',state.read(0xFFFFF364,2))
    frame=first_replace(frame,roster=state.table_at(0xD4B67).cursor())
    frame=_campaign_emit_fields(state,frame,0x7A8,0xFFFFEFB3,frame.roster.byte(low16(frame.target_x)),1)
    frame=_campaign_emit_fields(state,frame,0x7AE,0xFFFFEFB5,frame.roster.advance(1).byte(low16(frame.target_x)),1)
    return _campaign_emit_fields(state,frame,0x7B4,0xFFFFEFB7,frame.roster.advance(2).byte(low16(frame.target_x)),1)


def initialize_formation_choices_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """428/742: formation masks, optional choice caption, then the original display service."""
    frame=_city_ui_frame_fields(state,frame,0x428)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_call_fields(state,frame,0x760,0x74A)
    frame=_movement_compare(state,frame,state.read(0xFFFFF36C,2),2,16)
    if not frame.status&4:
        frame=_campaign_call_fields(state,frame,0xEA6,0x758)
    return _campaign_call_fields(state,frame,0xAF48,0x75E)


"""Complete campaign captions, selection descriptions and screen composition.

The readable stages preserve their real child tokens, original queue reads and
device transfers. Device waits and unresolved children remain true boundaries;
the source after them is retained rather than replaced with a fake success.
"""


def _campaign_screen_enter_fields(state: SceneState, frame: FirstDeploymentFrame,
        entry: int) -> FirstDeploymentFrame:
    frame=_city_ui_frame_fields(state,frame,entry)
    state.sr=0x2700
    return first_replace(frame,status=0)


def _campaign_screen_style_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_move(state,frame,'target_x',1,16)
    return _movement_move(state,frame,'target_y',3,16)


def _campaign_screen_countdown_fields(frame: FirstDeploymentFrame,
        carrier: str) -> tuple[FirstDeploymentFrame, bool]:
    from .business_lowbank import _campaign_ui_loop_fields
    return _campaign_ui_loop_fields(frame,carrier)


def _campaign_screen_transfer_fields(state: SceneState, frame: FirstDeploymentFrame,
        source: str, counter: str, pc: int, address: int=0xC00000) -> FirstDeploymentFrame:
    from .business_lowbank import _campaign_ui_copy_panel_longs_fields
    return _campaign_ui_copy_panel_longs_fields(state,frame,source,counter,pc,address)


def _campaign_screen_fill_fields(state: SceneState, frame: FirstDeploymentFrame, counter: str, value: int, pc: int, buffer: bool) -> FirstDeploymentFrame:
    """An original LONG fill loop; a RAM-buffer fill advances passed A1, a video fill does not."""
    while True:
        address = frame.candidates.base if buffer else 12582912
        frame = _campaign_emit_fields(state, frame, pc, address, value, 4)
        if buffer:
            frame = first_replace(frame, candidates=frame.candidates.advance(4))
        frame, more = _campaign_screen_countdown_fields(frame, counter)
        if not more:
            return frame


def reset_menu_sprite_slots_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3DC/5A4: original display disable and descending sixteen-BYTE sprite index reset."""
    frame = _campaign_screen_enter_fields(state, frame, 988)
    frame = _movement_move(state, frame, 'target_x', state.read(4294964742, 2), 16)
    frame = _movement_move(state, frame, 'target_x', low8(frame.target_x) & 191, 8)
    frame = _campaign_emit_fields(state, frame, 1456, 12582916, low16(frame.target_x))
    frame = _campaign_call_fields(state, frame, 41394, 1468)
    frame = first_replace(frame, roster=state.table_at(4294964304).cursor())
    frame = _movement_move(state, frame, 'target_x', 15, 16)
    while True:
        frame = _campaign_emit_fields(state, frame, 1476, frame.roster.advance(s16(low16(frame.target_x))).base, low8(frame.target_x), 1)
        frame, more = _campaign_screen_countdown_fields(frame, 'target_x')
        if not more:
            return frame


def initialize_campaign_screen_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3F8/C4C/B210: complete initial composition and campaign-mode bookkeeping."""
    frame=_campaign_screen_enter_fields(state,frame,0x3F8)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF606,2),16)
    frame=_movement_move(state,frame,'target_x',low8(frame.target_x)&191,8)
    frame=_campaign_emit_fields(state,frame,0xB21C,0xC00004,low16(frame.target_x))
    frame=_campaign_emit_fields(state,frame,0xB222,0xC00004,0x8407)
    frame=_campaign_call_fields(state,frame,0x68CE,0xB230)
    frame=first_replace(frame,opponent=state.table_at(0xC00000).cursor(),scratch=state.table_at(0xC00004).cursor())
    frame=_campaign_call_fields(state,frame,0xB4E4,0xB240)
    frame=_campaign_call_fields(state,frame,0xB5B8,0xB244)
    frame=_campaign_call_fields(state,frame,0xB286,0xB248)
    frame=_campaign_call_fields(state,frame,0xB620,0xB24C)
    frame=_campaign_call_fields(state,frame,0xB724,0xB250)
    frame=_campaign_call_fields(state,frame,0xB9EA,0xB254)
    frame=_campaign_call_fields(state,frame,0xBA5C,0xB258)
    frame=_campaign_emit_fields(state,frame,0xB258,0xFFFFFBC2,0x0CCC0EC0,4)
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF352,1)
    frame=_campaign_emit_fields(state,frame,0xB264,0xFFFFF3A4,1)
    frame=_movement_compare(state,frame,state.read(0xFFFFF6C4,2),5,16)
    if not frame.status&4:
        frame=_campaign_emit_fields(state,frame,0xB274,0xFFFFEFE0,state.read(0xFFFFF6C4,2))
    frame=_campaign_emit_fields(state,frame,0xB27A,0xFFFFF6C4,5)
    state.sr=0x2500
    return first_replace(frame,status=0)


def upload_selected_dictionary_panel_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """400/5CE: genuine dictionary decode, sound packet selection and display refresh."""
    frame=_campaign_screen_enter_fields(state,frame,0x400)
    frame=_campaign_emit_fields(state,frame,0x5D2,0xC00004,0x40000000,4)
    frame=first_replace(frame,roster=state.table_at(0xCE61E).cursor(),candidates=state.table_at(0xCE49A).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xD34C2,2),16)
    frame=_campaign_call_fields(state,frame,0xADFC,0x5F4)
    frame=_campaign_emit_fields(state,frame,0x5F4,0xFFFFF37E,1)
    frame=_movement_move(state,frame,'target_x',1,16)
    frame=_campaign_call_fields(state,frame,0x80F4,0x604)
    return _campaign_call_fields(state,frame,0xAF48,0x60A)


def initialize_campaign_menu_panels_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """408/4FAE: complete menu layers, actual selected-city optional layers and final refresh."""
    frame=_campaign_screen_enter_fields(state,frame,0x408)
    frame=first_replace(frame,auxiliary=state.table_at(0xC00000).cursor())
    frame=_campaign_screen_style_fields(state,frame)
    frame=_campaign_call_fields(state,frame,0x5010,0x4FC4)
    frame=_campaign_call_fields(state,frame,0x506C,0x4FC8)
    frame=_campaign_call_fields(state,frame,0x5204,0x4FCC)
    frame=_campaign_call_fields(state,frame,0x52C2,0x4FD0)
    frame=_campaign_call_fields(state,frame,0x5370,0x4FD4)
    frame=_campaign_call_fields(state,frame,0x55B0,0x4FD8)
    frame=_movement_compare(state,frame,state.read(0xFFFFF364,2),65535,16)
    if not frame.status&4:
        frame=_campaign_screen_style_fields(state,frame)
        frame=_campaign_call_fields(state,frame,0x5242,0x4FEE)
        frame=_campaign_call_fields(state,frame,0x5330,0x4FF2)
        frame=_campaign_call_fields(state,frame,0x55D0,0x4FF6)
    frame=_world_map_bit_fields(state,frame,state.read(0xFFFFF3A5,1),0)
    if frame.status&4:
        frame=_campaign_call_fields(state,frame,0x57A0,0x5002)
    frame=_campaign_emit_fields(state,frame,0x5002,0xFFFFF398,1)
    return _campaign_call_fields(state,frame,0xAF48,0x500E)


def initialize_officer_detail_panel_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """410/4A54: officer header, original selected roster index and two detail descendants."""
    frame = _campaign_screen_enter_fields(state, frame, 1040)
    frame = first_replace(frame, auxiliary=state.table_at(12582912).cursor())
    frame = _campaign_screen_style_fields(state, frame)
    frame = first_replace(frame, roster=state.table_at(601098).cursor(), candidates=state.table_at(4294955776).cursor())
    frame = _movement_move(state, frame, 'count', 15, 16)
    frame = _campaign_call_fields(state, frame, 44682, 19066)
    frame = _campaign_emit_fields(state, frame, 19066, 12582916, 1084227584, 4)
    frame = first_replace(frame, roster=state.table_at(4294955776).cursor())
    frame = _movement_move(state, frame, 'target_x', 511, 16)
    frame = _campaign_screen_transfer_fields(state, frame, 'roster', 'target_x', 19084, frame.auxiliary.base)
    frame = _movement_move(state, frame, 'target_x', state.read(4294964088, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
    frame = first_replace(frame, roster=state.table_at(4294964478).cursor())
    frame = _campaign_emit_fields(state, frame, 19100, 4294964082, frame.roster.word(low16(frame.target_x)))
    frame = _campaign_call_fields(state, frame, 19122, 19110)
    frame = _campaign_call_fields(state, frame, 19240, 19114)
    return _campaign_call_fields(state, frame, 44872, 19120)


def upload_formation_caption_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """420/6A6: formation heading packet and full288-LONG video transfer."""
    frame=_campaign_screen_enter_fields(state,frame,0x420)
    frame=first_replace(frame,roster=state.table_at(0x8A444).cursor(),candidates=state.table_at(0xFFFFD300).cursor())
    frame=_campaign_screen_style_fields(state,frame)
    frame=_movement_move(state,frame,'count',8,16)
    frame=_campaign_call_fields(state,frame,0xAE8A,0x6C6)
    frame=_campaign_emit_fields(state,frame,0x6C6,0xC00004,0x40A00000,4)
    frame=first_replace(frame,roster=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'target_x',287,16)
    frame=_campaign_screen_transfer_fields(state,frame,'roster','target_x',0x6D8)
    return _campaign_call_fields(state,frame,0xAF48,0x6E8)


def upload_formation_choice_caption_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """424/6EA: original blank prefix, caption and choice-panel refresh."""
    frame=_campaign_screen_enter_fields(state,frame,0x424)
    frame=first_replace(frame,roster=state.table_at(0x8A456).cursor(),candidates=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'count',31,16)
    frame=_campaign_screen_fill_fields(state,frame,'count',0x11111111,0x6FC,True)
    frame=_campaign_screen_style_fields(state,frame)
    frame=_movement_move(state,frame,'count',5,16)
    frame=_campaign_call_fields(state,frame,0xAE8A,0x718)
    frame=_campaign_emit_fields(state,frame,0x718,0xC00004,0x40200000,4)
    frame=first_replace(frame,roster=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'unit',223,16)
    frame=_campaign_screen_transfer_fields(state,frame,'roster','unit',0x72A)
    frame=_campaign_call_fields(state,frame,0x506C,0x73A)
    return _campaign_call_fields(state,frame,0xAF48,0x740)


def initialize_city_choice_caption_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """42C/7BC: selected-city heading, choice panel and original command30."""
    frame=_campaign_screen_enter_fields(state,frame,0x42C)
    frame=first_replace(frame,roster=state.table_at(0x8A438).cursor(),candidates=state.table_at(0xFFFFD300).cursor())
    frame=_campaign_screen_style_fields(state,frame)
    frame=_movement_move(state,frame,'count',5,16)
    frame=_campaign_call_fields(state,frame,0xAE8A,0x7DC)
    frame=_campaign_emit_fields(state,frame,0x7DC,0xC00004,0x40A00000,4)
    frame=first_replace(frame,roster=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'target_x',191,16)
    frame=_campaign_screen_transfer_fields(state,frame,'roster','target_x',0x7EE)
    frame=_campaign_screen_style_fields(state,frame)
    frame=_campaign_call_fields(state,frame,0x506C,0x806)
    frame=_campaign_emit_fields(state,frame,0x806,0xFFFFF362,30)
    return _campaign_call_fields(state,frame,0xAF48,0x812)


def request_affordable_action_panel_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """430/814: actual action cost, budget comparison and original denied-action tail."""
    from ..high_level_battle_ai.business_formation import _first_compare_long
    frame=_campaign_screen_enter_fields(state,frame,0x430)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'target_x',31,16)
    frame=_campaign_screen_fill_fields(state,frame,'target_x',0x11111111,0x820,True)
    frame=_campaign_screen_style_fields(state,frame)
    frame=_movement_move(state,frame,'count',2,16)
    frame=first_replace(frame,roster=state.table_at(0x8D8).cursor())
    frame=_campaign_call_fields(state,frame,0xAE8A,0x842)
    frame=_campaign_emit_fields(state,frame,0x842,0xC00004,0x50000000,4)
    frame=first_replace(frame,roster=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'target_x',223,16)
    frame=_campaign_screen_transfer_fields(state,frame,'roster','target_x',0x854)
    frame=_campaign_screen_style_fields(state,frame)
    frame=_campaign_call_fields(state,frame,0x506C,0x86C)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),39,16)
    if frame.status&4:
        frame=_campaign_call_fields(state,frame,0x8E6,0x878)
        frame=_campaign_emit_fields(state,frame,0x878,0xFFFFF39E,frame.target_x,4)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A8,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_x',2)
        frame=first_replace(frame,roster=state.table_at(0xFFFFDFFC).cursor())
        frame=_movement_move_long(state,frame,'target_x',frame.roster.long(low16(frame.target_x)))
        frame=_first_compare_long(frame,frame.target_x,state.read(0xFFFFF39E,4))
        state.sr=(state.sr&65504)|frame.status
        if frame.status&1:
            frame=_campaign_emit_fields(state,frame,0x890,0xFFFFF362,2)
            frame=_campaign_emit_fields(state,frame,0x896,0xFFFFF362,35)
            frame=_campaign_emit_fields(state,frame,0x89C,0xFFFFF608,120)
            frame=_movement_move(state,frame,'target_x',189,16)
            frame=_campaign_call_fields(state,frame,0x676F2,0x8AC)
            return _campaign_tail_fields(state,frame,0x60C)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),177,16)
    selected=bool(frame.status&4)
    if not selected:
        frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),186,16)
        selected=bool(frame.status&4)
    if selected:
        frame=_campaign_call_fields(state,frame,0x165D8,0x8CA)
    frame=_campaign_emit_fields(state,frame,0x8CA,0xFFFFF362,18)
    return _campaign_call_fields(state,frame,0xAF48,0x8D6)


def initialize_officer_portrait_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """438/94C: actual officer portrait callback and complete128-LONG blank fill."""
    frame=_campaign_screen_enter_fields(state,frame,0x438)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=_movement_move(state,frame,'target_y',5,16)
    frame=_campaign_call_fields(state,frame,0x661D4,0x95E)
    frame=_campaign_emit_fields(state,frame,0x95E,0xC00004,0x6E000001,4)
    frame=_movement_move(state,frame,'target_x',127,16)
    frame=_campaign_screen_fill_fields(state,frame,'target_x',0x33333333,0x96C,False)
    return _campaign_call_fields(state,frame,0xAF48,0x980)


def initialize_education_screen_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """440/AAA: text/blank packet, original education values and message106 tail."""
    frame=_campaign_screen_enter_fields(state,frame,0x440)
    frame=first_replace(frame,roster=state.table_at(0x6BF3A).cursor(),candidates=state.table_at(0xFFFFD300).cursor())
    frame=_campaign_screen_style_fields(state,frame)
    frame=_movement_move(state,frame,'count',2,16)
    frame=_campaign_call_fields(state,frame,0xAE8A,0xACA)
    frame=_movement_move(state,frame,'count',15,16)
    frame=_campaign_screen_fill_fields(state,frame,'count',0x11111111,0xACE,True)
    frame=first_replace(frame,roster=state.table_at(0x6BF40).cursor())
    frame=_movement_move(state,frame,'count',0,16)
    frame=_campaign_call_fields(state,frame,0xAE8A,0xAE8)
    frame=_movement_move(state,frame,'count',15,16)
    frame=_campaign_screen_fill_fields(state,frame,'count',0x11111111,0xAEC,True)
    frame=_campaign_emit_fields(state,frame,0xAF6,0xC00004,0x40A00000,4)
    frame=first_replace(frame,roster=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'target_x',159,16)
    frame=_campaign_screen_transfer_fields(state,frame,'roster','target_x',0xB08)
    frame=_campaign_call_fields(state,frame,0x15F84,0xB18)
    frame=_campaign_call_fields(state,frame,0x1605E,0xB1E)
    frame=_campaign_call_fields(state,frame,0x161D4,0xB24)
    frame=_campaign_call_fields(state,frame,0x1622E,0xB2A)
    frame=_campaign_emit_fields(state,frame,0xB2A,0xFFFFF612,521)
    frame=_campaign_emit_fields(state,frame,0xB30,0xFFFFF670,0,clear=True)
    frame=_campaign_emit_fields(state,frame,0xB34,0xFFFFF362,1)
    frame=_movement_move(state,frame,'target_x',106,16)
    frame=_campaign_call_fields(state,frame,0x676F2,0xB44)
    return _campaign_tail_fields(state,frame,0x60C)


def initialize_assignment_description_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """444/B48: selected member's real occupation name and both complete description buffers."""
    frame = _campaign_screen_enter_fields(state, frame, 1092)
    frame = first_replace(frame, auxiliary=state.table_at(12582912).cursor(), candidates=state.table_at(4294955776).cursor())
    frame = _movement_move(state, frame, 'target_x', 31, 16)
    frame = _campaign_screen_fill_fields(state, frame, 'target_x', 286331153, 2906, True)
    frame = first_replace(frame, roster=state.table_at(442122).cursor())
    frame = _campaign_screen_style_fields(state, frame)
    frame = _movement_move(state, frame, 'count', 1, 16)
    frame = _campaign_call_fields(state, frame, 44682, 2940)
    frame = _movement_compare(state, frame, state.read(4294964108, 2), 183, 16)
    if frame.status & 4:
        frame = first_replace(frame, roster=state.table_at(4294963134).cursor())
        frame = first_replace(frame, roster=frame.roster.advance(s16(state.read(4294963142, 2))))
        frame = _movement_move(state, frame, 'distance', frame.roster.word(), 16)
        frame = first_replace(frame, roster=state.table_at(4294938624).cursor().advance(s16(low16(frame.distance))))
    else:
        frame = first_replace(frame, roster=state.table_at(state.read(16726060, 4)).cursor())
    frame = _movement_move(state, frame, 'distance', 0, 16)
    frame = _movement_move(state, frame, 'distance', frame.roster.advance(4).byte(), 8)
    frame = _movement_fixed_shift_word(state, frame, 'distance', 1)
    frame = first_replace(frame, roster=state.table_at(4294960704).cursor())
    frame = _movement_move(state, frame, 'distance', frame.roster.word(low16(frame.distance)), 16)
    frame = _movement_move(state, frame, 'offset_x', low16(frame.distance), 16)
    frame = _movement_fixed_shift_word(state, frame, 'distance', 1)
    frame = _city_ui_arithmetic_fields(state, frame, 'distance', low16(frame.offset_x))
    frame = _movement_fixed_shift_word(state, frame, 'distance', 1)
    frame = first_replace(frame, roster=state.table_at(566532).cursor().advance(s16(low16(frame.distance))))
    frame = _movement_move(state, frame, 'count', 2, 16)
    frame = _campaign_call_fields(state, frame, 44682, 3018)
    frame = first_replace(frame, roster=state.table_at(442130).cursor())
    frame = _movement_move(state, frame, 'count', 19, 16)
    frame = _campaign_call_fields(state, frame, 44682, 3034)
    frame = _campaign_emit_fields(state, frame, 3034, 12582916, 1075838976, 4)
    frame = _movement_move(state, frame, 'count', 927, 16)
    frame = first_replace(frame, roster=state.table_at(4294955776).cursor())
    frame = _campaign_screen_transfer_fields(state, frame, 'roster', 'count', 3052, frame.auxiliary.base)
    frame = first_replace(frame, roster=state.table_at(442180).cursor(), candidates=state.table_at(4294955776).cursor())
    frame = _movement_move(state, frame, 'count', 9, 16)
    frame = _campaign_call_fields(state, frame, 44682, 3078)
    frame = first_replace(frame, candidates=state.table_at(4294955776).cursor())
    frame = _movement_move(state, frame, 'count', 319, 16)
    frame = _campaign_screen_transfer_fields(state, frame, 'candidates', 'count', 3086, frame.auxiliary.base)
    frame = _campaign_call_fields(state, frame, 21360, 3098)
    frame = _campaign_call_fields(state, frame, 20588, 3104)
    frame = _campaign_call_fields(state, frame, 21936, 3110)
    return _campaign_call_fields(state, frame, 44872, 3116)


def upload_assignment_caption_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """44C/C52: assignment heading and the real160-LONG caption buffer."""
    frame=_campaign_screen_enter_fields(state,frame,0x44C)
    frame=first_replace(frame,roster=state.table_at(0x8A476).cursor(),candidates=state.table_at(0xFFFFD300).cursor())
    frame=_campaign_screen_style_fields(state,frame)
    frame=_movement_move(state,frame,'count',4,16)
    frame=_campaign_call_fields(state,frame,0xAE8A,0xC72)
    frame=_campaign_emit_fields(state,frame,0xC72,0xC00004,0x40A00000,4)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'target_x',159,16)
    return _campaign_screen_transfer_fields(state,frame,'candidates','target_x',0xC84)


def wait_and_initialize_campaign_action_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """494/D94: poll the actual video status bit3, then original scene/action refresh."""
    frame=_campaign_screen_enter_fields(state,frame,0x494)
    while True:
        frame=_movement_move(state,frame,'target_x',state.read(0xC00004,2),16)
        frame=_world_map_bit_fields(state,frame,frame.target_x,3)
        if not frame.status&4:
            break
    frame=_campaign_call_fields(state,frame,0x1072C,0xDAA)
    frame=_movement_test(state,frame,state.read(0xFFFFF6C4,2),16)
    if frame.status&4:
        frame=_campaign_call_fields(state,frame,0x52C2,0xDB8)
    return _campaign_call_fields(state,frame,0xAF48,0xDBE)


def initialize_post_duel_campaign_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """04B0/0514 original new-game caller; complete cooperative child retained."""
    from .campaign_setup_steps import run_campaign_setup_blocking_fields
    return run_campaign_setup_blocking_fields(state, frame)


def upload_three_formation_names_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4C4/EA6: three six-BYTE name slices, genuine glyph decoding and tile strip."""
    frame = _campaign_screen_enter_fields(state, frame, 1220)
    frame = first_replace(frame, roster=state.table_at(4294955776).cursor(), candidates=state.table_at(566478).cursor(), controller=state.table_at(4294963044).cursor())
    frame = _movement_move(state, frame, 'target_x', 2, 16)
    while True:
        frame = _movement_move(state, frame, 'target_y', frame.controller.word(), 16)
        frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
        frame = _city_ui_arithmetic_fields(state, frame, 'target_y', frame.controller.word())
        frame = first_replace(frame, controller=frame.controller.advance(2))
        frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
        for offset, pc in ((0, 3780), (2, 3784), (4, 3788)):
            value = frame.candidates.advance(offset).word(low16(frame.target_y))
            frame = _campaign_emit_fields(state, frame, pc, frame.roster.base, value)
            frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = first_replace(frame, candidates=frame.candidates.advance(18))
        frame, more = _campaign_screen_countdown_fields(frame, 'target_x')
        if not more:
            break
    frame = first_replace(frame, roster=state.table_at(4294955776).cursor(), candidates=state.table_at(4294955808).cursor())
    frame = _campaign_screen_style_fields(state, frame)
    frame = _movement_move(state, frame, 'count', 8, 16)
    frame = _campaign_call_fields(state, frame, 44682, 3826)
    frame = _campaign_emit_fields(state, frame, 3826, 12582916, 1402994688, 4)
    frame = first_replace(frame, candidates=state.table_at(4294955808).cursor())
    frame = _movement_move(state, frame, 'count', 287, 16)
    return _campaign_screen_transfer_fields(state, frame, 'candidates', 'count', 3844)


def upload_three_formation_names_direct_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """EA6 actual body entry of4C4, same owner core and no additional CALL slot."""
    return upload_three_formation_names_fields(state,frame)


# C59 complete display/order ABI; historical algorithms are projections only.
"""One full officer-roster upload, shared by original414 BRA and53E6 body.

Actual roster WORDs, glyph source, all retained LONGs, stack saves inside
AE8A, VDP DATA and AF48 edge waits stay live. Historical label carriers
never stand in for missing D/A/SP or supply a successful device response.
"""
from .contexts_display_fields import (
    display_frame_fields, display_move_fields, display_store_fields,
    display_address_fields, display_shift_word_fields, display_loop_fields,
    display_call_fields, display_status_fields,
)


def _roster_panel_pixels_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame, optional: bool) -> FirstDeploymentFrame:
    """One96/64 LONG loop, preserving actual D5 counter and A1 postincrement."""
    if type(optional) is not bool:
        raise ValueError('actual normal/optional roster tile strip required')
    frame = display_move_fields(state, frame, 'offset_x', 0x3F if optional else 0x5F)
    frame = display_address_fields(state, frame, 'candidates', 0xFFFFD300)
    while True:
        pixels = frame.candidates.long()
        frame = first_replace(frame, candidates=frame.candidates.advance(4))
        frame = display_store_fields(state, frame, 0x54A8 if optional else 0x5468,
            0xC00000, pixels, 4)
        frame, more = display_loop_fields(frame, 'offset_x')
        if not more:
            return frame


def upload_officer_roster_panel_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """414→53E6; real name/prompt, optional glyphs, labels and AF48 tail."""
    from .business_movement_support import _movement_compare, _movement_test, _movement_add_word
    frame = display_frame_fields(state, frame)
    frame = display_status_fields(state, frame, 0x2700)
    frame = display_store_fields(state, frame, 0x53EA, 0xC00004, 0x40200000, 4)
    frame = display_move_fields(state, frame, 'target_x', 0x1F)
    while True:
        frame = display_store_fields(state, frame, 0x53F8, 0xC00000, 0x11111111, 4)
        frame, more = display_loop_fields(frame, 'target_x')
        if not more:
            break
    frame = display_move_fields(state, frame, 'target_x', 1)
    frame = display_move_fields(state, frame, 'target_y', 3)
    frame = _movement_compare(state, frame, state.read(0xFFFFF6C4, 2), 1, 16)
    frame = display_store_fields(state, frame, 0x5426 if frame.status & 4 else 0x5418,
        0xC00004, 0x4E000000 if frame.status & 4 else 0x4E000003, 4)
    frame = display_address_fields(state, frame, 'controller', 0xFFFFF500)
    while True:
        officer = frame.controller.word()
        frame = first_replace(frame, controller=frame.controller.advance(2))
        frame = display_move_fields(state, frame, 'offset_x', officer)
        frame = display_move_fields(state, frame, 'choice', low16(frame.offset_x))
        if frame.status & 8:
            break
        frame = display_move_fields(state, frame, 'offset_x', low16(frame.offset_x) & 0xFF)
        frame = display_address_fields(state, frame, 'roster', 0x8A504)
        frame = display_move_fields(state, frame, 'offset_y', low16(frame.offset_x))
        frame = display_shift_word_fields(state, frame, 'offset_x', 1)
        frame = _movement_add_word(state, frame, 'offset_x', low16(frame.offset_y))
        frame = display_shift_word_fields(state, frame, 'offset_x', 1)
        frame = first_replace(frame, roster=frame.roster.advance(s16(low16(frame.offset_x))))
        frame = display_call_fields(state, frame, 0x54CA, 0x5452)
        frame = display_address_fields(state, frame, 'candidates', 0xFFFFD300)
        frame = display_move_fields(state, frame, 'count', 2)
        frame = display_call_fields(state, frame, 0xAE8A, 0x5460)
        frame = _roster_panel_pixels_frame_fields(state, frame, False)
    frame = display_move_fields(state, frame, 'target_x', 1)
    frame = display_move_fields(state, frame, 'target_y', 3)
    frame = _movement_test(state, frame, state.read(0xFFFFF656, 2), 16)
    if not frame.status & 4:
        frame = display_address_fields(state, frame, 'roster', 0x54C6)
        frame = display_address_fields(state, frame, 'candidates', 0xFFFFD300)
        frame = display_move_fields(state, frame, 'count', 1)
        frame = display_call_fields(state, frame, 0xAE8A, 0x5496)
        frame = display_store_fields(state, frame, 0x5496, 0xC00004, 0x57000000, 4)
        frame = _roster_panel_pixels_frame_fields(state, frame, True)
    frame = _movement_test(state, frame, state.read(0xFFFFF6C4, 2), 16)
    if frame.status & 4:
        frame = display_call_fields(state, frame, 0x506C, 0x54BE)
    return display_call_fields(state, frame, 0xAF48, 0x54C4)
