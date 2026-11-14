"""Explicit map/menu call links on one live SceneState.

Only complete contracts are linked. Small legacy roster/camera contracts do
not acquire guessed carriers: LogicalServices stops on their exact-type
mismatch. Lazy imports avoid cycles; every handler calls an actual recovered
business function, not a stub, source reader or CPU interpreter.
"""
from .services import ServiceBinding
from .contexts_main import CameraMotionInput, CameraMotionResult, CameraTransitionInput, CameraTransitionResult
from .contexts_map import (
    AdjustSelectedRosterMemberInput, AdjustSelectedRosterMemberResult,
    RenderMapColumnInput, RenderMapColumnResult, RenderMapRowInput,
    RenderMapRowResult, UpdateWorldCursorFromInputsInput, UpdateWorldCursorFromInputsResult,
    RefreshWorldCursorAttributesInput, RefreshWorldCursorAttributesResult,
    RefreshMapTilesAroundCursorService1,
    RefreshMapTilesAroundCursorService2, RefreshMapTilesAroundCursorService3,
    RefreshMapTilesAroundCursorService4,
)
from .contexts_lowbank import RefreshScenePalettesInput, RefreshScenePalettesResult
from .contexts_commands import (
    CollectCityOfficersForMenuInput, CollectCityOfficersForMenuResult,
)


from .contexts_commands import (LocationChoiceFrame, UpdateSelectedForcePromptInput, UpdateSelectedForcePromptResult)
from .contexts_main import LocationChoiceInput, LocationChoiceResult
from .contexts_lowbank import UploadSelectedModeTileRowsInput, UploadSelectedModeTileRowsResult

def _adjust_selected_member(state, context):
    from .business_map import adjust_selected_roster_member
    return adjust_selected_roster_member(state, context)


def _collect_city_officers(state, context):
    from .business_commands import collect_city_officers_for_menu
    return collect_city_officers_for_menu(state, context)


def _render_column(state, context):
    from .business_map import render_map_column
    return render_map_column(state, context)


def _render_row(state, context):
    from .business_map import render_map_row
    return render_map_row(state, context)


def _refresh_column(state, context):
    """Adapt this call's current locals, not an entry-frame snapshot."""
    inputs = RenderMapColumnInput(
        roster=context.roster, value=context.value, field=context.field,
        offset=context.offset, limit=context.limit, member=context.member,
        stack_cursor=context.stack_cursor,
    )
    return _render_column(state, inputs)


def _refresh_row(state, context):
    inputs = RenderMapRowInput(
        roster=context.roster, value=context.value, field=context.field,
        offset=context.offset, limit=context.limit, member=context.member,
        stack_cursor=context.stack_cursor,
    )
    return _render_row(state, inputs)


def map_menu_bindings():
    """Twenty exact caller ABIs, including the complete location-choice chain.

    A01C has four sites: right/left columns and down/up rows. They share real
    callee logic but remain distinct input types. The full 62FA and4E50
    contracts are available to callers that genuinely possess all live-ins;
    partial MainRosterInput/SelectedOfficer/CameraStrip remain unbound.
    """
    return (
        ServiceBinding(0x14E0, LocationChoiceInput, LocationChoiceResult, _location_choice),
        ServiceBinding(0xAB40, LocationChoiceFrame, LocationChoiceFrame, _world_cursor_coordinates),
        ServiceBinding(0xA530, UpdateSelectedForcePromptInput, UpdateSelectedForcePromptResult, _selected_force_prompt),
        ServiceBinding(0xA760, UploadSelectedModeTileRowsInput, UploadSelectedModeTileRowsResult, _selected_mode_tile_rows),
        ServiceBinding(0x157A, LocationChoiceFrame, LocationChoiceFrame, _select_location),
        ServiceBinding(0x15BE, LocationChoiceFrame, LocationChoiceFrame, _clamp_camera_target),
        ServiceBinding(0x161E, CameraTransitionInput, CameraTransitionResult, _transition_camera),
        ServiceBinding(0x9E5E, UpdateWorldCursorFromInputsInput, UpdateWorldCursorFromInputsResult, _update_cursor),
        ServiceBinding(0xA14E, RefreshWorldCursorAttributesInput, RefreshWorldCursorAttributesResult, _refresh_cursor_attributes),
        ServiceBinding(0xA3DA, RefreshScenePalettesInput, RefreshScenePalettesResult, _refresh_palettes),
        ServiceBinding(0x16B4, CameraMotionInput, CameraMotionResult, _advance_camera),
        ServiceBinding(0x1344, CameraMotionInput, CameraMotionInput, _draw_camera_pointer),
        ServiceBinding(0x62FA, AdjustSelectedRosterMemberInput,
                       AdjustSelectedRosterMemberResult, _adjust_selected_member),
        ServiceBinding(0x4E50, CollectCityOfficersForMenuInput,
                       CollectCityOfficersForMenuResult, _collect_city_officers),
        ServiceBinding(0xA0CC, RenderMapColumnInput,
                       RenderMapColumnResult, _render_column),
        ServiceBinding(0xA10C, RenderMapRowInput,
                       RenderMapRowResult, _render_row),
        ServiceBinding(0xA0CC, RefreshMapTilesAroundCursorService1,
                       RenderMapColumnResult, _refresh_column),
        ServiceBinding(0xA0CC, RefreshMapTilesAroundCursorService2,
                       RenderMapColumnResult, _refresh_column),
        ServiceBinding(0xA10C, RefreshMapTilesAroundCursorService3,
                       RenderMapRowResult, _refresh_row),
        ServiceBinding(0xA10C, RefreshMapTilesAroundCursorService4,
                       RenderMapRowResult, _refresh_row),
    )


def _advance_camera(state, context):
    from .business_main import advance_campaign_camera_motion
    return advance_campaign_camera_motion(state, context)


def _draw_camera_pointer(state, context):
    from .business_main import draw_campaign_camera_pointer
    return draw_campaign_camera_pointer(state, context)


def _transition_camera(state, context):
    from .business_main import advance_campaign_camera_transition
    return advance_campaign_camera_transition(state, context)


def _update_cursor(state, context):
    from .business_map import update_world_cursor_from_inputs
    return update_world_cursor_from_inputs(state, context)


def _refresh_cursor_attributes(state, context):
    from .business_map import refresh_world_cursor_attributes
    return refresh_world_cursor_attributes(state, context)


def _refresh_palettes(state, context):
    from .business_lowbank import refresh_scene_palettes
    return refresh_scene_palettes(state, context)


def _location_choice(state,inputs):
    from .business_main import advance_campaign_location_choice
    return advance_campaign_location_choice(state,inputs)


def _world_cursor_coordinates(state,frame):
    from .business_commands import append_world_cursor_coordinate_frame
    return append_world_cursor_coordinate_frame(state,frame)


def _selected_force_prompt(state,inputs):
    from .business_commands import update_selected_force_prompt
    return update_selected_force_prompt(state,inputs)


def _selected_mode_tile_rows(state,inputs):
    from .business_lowbank import upload_selected_mode_tile_rows
    return upload_selected_mode_tile_rows(state,inputs)


def _select_location(state,frame):
    from .business_main import select_campaign_location_frame
    return select_campaign_location_frame(state,frame)


def _clamp_camera_target(state,frame):
    from .business_main import clamp_campaign_camera_target_frame
    return clamp_campaign_camera_target_frame(state,frame)
