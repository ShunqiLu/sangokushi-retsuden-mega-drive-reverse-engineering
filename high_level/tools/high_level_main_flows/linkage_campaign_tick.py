"""Exact RAM-effect caller projections, never zero-filled CPU contexts.

A3DA is completely RAM-driven for DATA/RAM effects; its full legacy result
remains a strict incoming-carrier projection over the same core. 671B6 admits
the true not-due SUBQ/RTS effect path; the due path requires a current complete
MessageLayout and raises a real boundary without fabricating it.
"""
from .domain import checked_state
from .contexts_main import SceneTick, SoundWord, CampaignPointerFields
from .contexts_lowbank import PaletteRefreshFields
from .contexts_map import WorldCursorRefreshFields
from .contexts_highbank import ScrollingMessageAdvance, MessageControlFields
from .services import ServiceBinding
from .contexts_commands import AdjustForceRelationSelectionInput, AdjustForceRelationSelectionResult, SelectedCityCommandFields, ConfirmForceRelationSelectionFields, CommandDescriptionFields
from ..high_level_command_actions.contexts_message import MessagePreparation


from .contexts_map import CommandOfficerSelectionFields

def _palette_refresh_tick(state, request):
    checked_state(state)
    if type(request) is not SceneTick:
        raise ValueError('exact SceneTick effect contract required')
    from .business_lowbank import refresh_scene_palettes_fields
    return refresh_scene_palettes_fields(state)


def _scrolling_message_tick(state, request):
    checked_state(state)
    if type(request) is not SceneTick:
        raise ValueError('exact SceneTick effect contract required')
    from .business_highbank import _advance_scrolling_message_core
    return _advance_scrolling_message_core(state, None)


def _message_word_tick(state, request):
    checked_state(state)
    if type(request) is not SoundWord:
        raise ValueError('exact actual message WORD required')
    request.validate(state)
    from ..high_level_command_actions.business_reuse import prepare_scene_message_fields
    return prepare_scene_message_fields(state, request.command)


def _force_relation_tick(state, request):
    checked_state(state)
    if type(request) is not SceneTick:
        raise ValueError('exact RAM-driven SceneTick required')
    from .business_commands import adjust_force_relation_selection
    return adjust_force_relation_selection(state, AdjustForceRelationSelectionInput())


def _selected_city_command_tick(state, request):
    checked_state(state)
    if type(request) is not SceneTick:
        raise ValueError('exact RAM-driven selected-city transaction required')
    from .business_commands import append_selected_city_command_fields
    return append_selected_city_command_fields(state)


def _force_relation_confirm_tick(state, request):
    checked_state(state)
    if type(request) is not SceneTick:
        raise ValueError('exact live force-confirm SceneTick required')
    from .business_commands import confirm_force_relation_selection_fields
    return confirm_force_relation_selection_fields(state)


def _current_command_description_tick(state, request):
    checked_state(state)
    if type(request) is not SceneTick:
        raise ValueError('exact RAM-driven current-description SceneTick required')
    from .business_commands import append_current_command_description_fields
    return append_current_command_description_fields(state)


def _campaign_pointer_tick(state, request):
    checked_state(state)
    if type(request) is not SceneTick:
        raise ValueError('exact RAM-driven pointer SceneTick required')
    from .business_main import draw_campaign_pointer_fields
    return draw_campaign_pointer_fields(state)


def _command_officer_selection_tick(state, request):
    checked_state(state)
    if type(request) is not SceneTick:
        raise ValueError('exact actual campaign-selection SceneTick required')
    from .business_map import select_next_command_officer_fields
    return select_next_command_officer_fields(state)


def _message_control_tick(state, request):
    checked_state(state)
    if type(request) is not SceneTick:
        raise ValueError('exact RAM-driven special-message SceneTick required')
    from .business_highbank import dispatch_message_control_fields
    return dispatch_message_control_fields(state)


def campaign_tick_bindings():
    return (
        ServiceBinding(0x676C4, SceneTick, MessageControlFields, _message_control_tick),
        ServiceBinding(0x6198, SceneTick, CommandOfficerSelectionFields, _command_officer_selection_tick),
        ServiceBinding(0xA158, SceneTick, WorldCursorRefreshFields, _world_cursor_refresh_tick),
        ServiceBinding(0xA3DA, SceneTick, PaletteRefreshFields, _palette_refresh_tick),
        ServiceBinding(0x671B6, SceneTick, ScrollingMessageAdvance, _scrolling_message_tick),
        ServiceBinding(0x676F2, SoundWord, MessagePreparation, _message_word_tick),
        ServiceBinding(0xC764, SceneTick, AdjustForceRelationSelectionResult, _force_relation_tick),
        ServiceBinding(0xD74A, SceneTick, SelectedCityCommandFields, _selected_city_command_tick),
        ServiceBinding(0xC790, SceneTick, ConfirmForceRelationSelectionFields, _force_relation_confirm_tick),
        ServiceBinding(0xD8EC, SceneTick, CommandDescriptionFields, _current_command_description_tick),
        ServiceBinding(0x1344, SceneTick, CampaignPointerFields, _campaign_pointer_tick),
    )


def _world_cursor_refresh_tick(state, request):
    checked_state(state)
    if type(request) is not SceneTick:
        raise ValueError('exact RAM-driven world-cursor SceneTick required')
    from .business_map import refresh_world_cursor_attribute_fields
    return refresh_world_cursor_attribute_fields(state)
