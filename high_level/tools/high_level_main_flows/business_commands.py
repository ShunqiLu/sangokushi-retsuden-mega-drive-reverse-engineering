"""Structured map/menu/controller logic, mechanically drafted then reviewed.

No instruction decoder, PC state, code array, file reader or media payload is
used at runtime. Ordinary values, typed live views and structured conditionals
retain width/order quirks. This draft is not full CPU or natural-call proof.
"""
from .domain import SceneState, Boundary, u8, u16, u32, s8, s16, low8, low16, replace_byte, replace_word, swap_words, checked_state
from .services import call_target
from .contexts_tick import MapTickFrame, checked_tick_frame
from .contexts_commands import (
    ComposeCurrentCityFieldsInput,
    ComposeCurrentCityFieldsResult,
    StartCurrentCityPacketInput,
    StartCurrentCityPacketResult,
    AppendCityStatusRowInput,
    AppendCityStatusRowResult,
    AppendCityNameFieldsInput,
    AppendCityNameFieldsResult,
    StoreCityStatusValueInput,
    StoreCityStatusValueResult,
    AppendCityResourceRowInput,
    AppendCityResourceRowResult,
    AppendSelectedRosterValuesInput,
    AppendSelectedRosterValuesResult,
    CollectCityOfficersForMenuInput,
    CollectCityOfficersForMenuResult,
    CollectCityOfficersForMenuService1,
    CollectCityOfficersForMenuService2,
    CollectCityOfficersForMenuService3,
    CollectCityOfficersForMenuService4,
    CollectCityOfficersForMenuService5,
    CollectCityOfficersForMenuService6,
    CollectCityOfficersForMenuService7,
    CollectCityOfficersForMenuService8,
    AppendCurrentRosterMarksInput,
    AppendCurrentRosterMarksResult,
    RenderCurrentCityCommandLabelsInput,
    RenderCurrentCityCommandLabelsResult,
    RenderCurrentCityCommandLabelsService1,
    ComposeCityRosterRowsInput,
    ComposeCityRosterRowsResult,
    ComposeSelectedForceRowsInput,
    ComposeSelectedForceRowsResult,
    AppendCityRelationRowInput,
    AppendCityRelationRowResult,
    RenderRosterNameOrPromptInput,
    RenderRosterNameOrPromptResult,
    RenderSelectedCityPacketInput,
    RenderSelectedCityPacketResult,
    AppendForceRosterNamesInput,
    AppendForceRosterNamesResult,
    StartSelectionPromptInput,
    StartSelectionPromptResult,
    StartSelectionPromptService1,
    StartSelectionPromptService2,
    StartSelectionPromptService3,
    AppendSelectionPromptHeadingInput,
    AppendSelectionPromptHeadingResult,
    SetSelectionPromptValueInput,
    SetSelectionPromptValueResult,
    AppendSelectionPromptRowInput,
    AppendSelectionPromptRowResult,
    AppendCurrentCityOwnerInput,
    AppendCurrentCityOwnerResult,
    StoreSelectionPromptValueInput,
    StoreSelectionPromptValueResult,
    AppendSelectionPromptValueInput,
    AppendSelectionPromptValueResult,
    AppendSelectedForceHeadInput,
    AppendSelectedForceHeadResult,
    AppendSelectedForceHeadService1,
    ComposeCommandSelectionPromptInput,
    ComposeCommandSelectionPromptResult,
    ComposeCommandSelectionPromptService1,
    SetCommandSelectionCursorInput,
    SetCommandSelectionCursorResult,
    StoreCommandSelectionValueInput,
    StoreCommandSelectionValueResult,
    AppendCommandSelectionHeadingInput,
    AppendCommandSelectionHeadingResult,
    AppendCommandConfirmationRowInput,
    AppendCommandConfirmationRowResult,
    PresentCurrentCommandPromptInput,
    PresentCurrentCommandPromptResult,
    PresentCurrentCommandPromptService1,
    PresentCommandWarningInput,
    PresentCommandWarningResult,
    AppendContextualCursorCommandsInput,
    AppendContextualCursorCommandsResult,
    AppendContextualCursorCommandsService1,
    AppendContextualCursorCommandsService2,
    DrawForceSummaryInput,
    DrawForceSummaryResult,
    DrawFirstForcePromptInput,
    DrawFirstForcePromptResult,
    DrawSecondForcePromptInput,
    DrawSecondForcePromptResult,
    UpdateSelectedForcePromptInput,
    UpdateSelectedForcePromptResult,
    DrawCurrentScenarioPromptInput,
    DrawCurrentScenarioPromptResult,
    DrawCurrentScenarioPromptService1,
    DrawCurrentScenarioPromptService2,
    DrawCurrentScenarioPromptService3,
    AppendScenarioOwnerGlyphsInput,
    AppendScenarioOwnerGlyphsResult,
    AppendScenarioOwnerValueInput,
    AppendScenarioOwnerValueResult,
    DrawTitleModePromptInput,
    DrawTitleModePromptResult,
    ComposeTitleOptionPanelInput,
    ComposeTitleOptionPanelResult,
    AppendTitleOptionGlyphsInput,
    AppendTitleOptionGlyphsResult,
    AppendTitleOptionDigitInput,
    AppendTitleOptionDigitResult,
    StoreTitleOptionDigitInput,
    StoreTitleOptionDigitResult,
    SetTitleOptionMarkerInput,
    SetTitleOptionMarkerResult,
    AppendTitleOptionDecorationsInput,
    AppendTitleOptionDecorationsResult,
    AppendTitleOptionDecorationsService1,
    AppendTitleOptionDecorationValueInput,
    AppendTitleOptionDecorationValueResult,
    AppendWorldCursorCoordinatesInput,
    AppendWorldCursorCoordinatesResult,
    DrawRosterOverviewInput,
    DrawRosterOverviewResult,
    AppendRosterOverviewCursorInput,
    AppendRosterOverviewCursorResult,
    DrawRosterOverviewValuesInput,
    DrawRosterOverviewValuesResult,
    AppendSelectedCityHeadInput,
    AppendSelectedCityHeadResult,
    AppendSelectedCityHeadService1,
    AppendRosterOverviewDigitInput,
    AppendRosterOverviewDigitResult,
    RetainRosterOverviewColumnInput,
    RetainRosterOverviewColumnResult,
    ComposeOfficerDetailPanelInput,
    ComposeOfficerDetailPanelResult,
    AppendOfficerNameValueInput,
    AppendOfficerNameValueResult,
    AppendOfficerNameValueAlternate1Input,
    AppendOfficerNameValueAlternate1Result,
    AppendOfficerNameValueAlternate2Input,
    AppendOfficerNameValueAlternate2Result,
    AppendOfficerNameValueAlternate3Input,
    AppendOfficerNameValueAlternate3Result,
    AppendOfficerNameValueAlternate4Input,
    AppendOfficerNameValueAlternate4Result,
    AppendOfficerAttributeValueInput,
    AppendOfficerAttributeValueResult,
    AppendOfficerAttributeValueService1,
    AppendOfficerAttributeValueService2,
    ScaleOfficerDetailValueInput,
    ScaleOfficerDetailValueResult,
    AppendOfficerDetailCommandsInput,
    AppendOfficerDetailCommandsResult,
    AppendOfficerDetailTitleInput,
    AppendOfficerDetailTitleResult,
    DrawOfficerDetailViewInput,
    DrawOfficerDetailViewResult,
    AppendOfficerDetailRowsInput,
    AppendOfficerDetailRowsResult,
    OpenRosterSelectionMessageInput,
    OpenRosterSelectionMessageResult,
    SetRosterSelectionNoticeInput,
    SetRosterSelectionNoticeResult,
    DrawForceRelationViewInput,
    DrawForceRelationViewResult,
    AppendForceRelationCommandsInput,
    AppendForceRelationCommandsResult,
    AppendForceRelationCommandsService1,
    AppendForceRelationHeadingInput,
    AppendForceRelationHeadingResult,
    SetForceRelationMarkersInput,
    SetForceRelationMarkersResult,
    AppendForceRelationValueRowInput,
    AppendForceRelationValueRowResult,
    AppendForceRelationFooterInput,
    AppendForceRelationFooterResult,
    AppendForceRelationLabelInput,
    AppendForceRelationLabelResult,
    AppendForceRelationDigitsInput,
    AppendForceRelationDigitsResult,
    AdjustForceRelationSelectionInput,
    AdjustForceRelationSelectionResult,
    ConfirmForceRelationSelectionInput,
    ConfirmForceRelationSelectionResult,
    DrawCommandCostPanelInput,
    DrawCommandCostPanelResult,
    DrawCommandCostPanelService1,
    DrawCommandCostPanelService2,
    DrawCommandCostPanelAlternate1Input,
    DrawCommandCostPanelAlternate1Result,
    DrawCommandCostPanelAlternate1Service1,
    DrawCommandCostPanelAlternate1Service2,
    DivideAndScaleCommandValueInput,
    DivideAndScaleCommandValueResult,
    SelectedCityCommandFields,
    StoreSelectedCityCommandFields,
    AppendSelectedCityCommandInput,
    AppendSelectedCityCommandResult,
    StoreSelectedCityCommandValueInput,
    StoreSelectedCityCommandValueResult,
    AppendCityCommandHeadingInput,
    AppendCityCommandHeadingResult,
    AppendCurrentCommandDescriptionInput,
    AppendCurrentCommandDescriptionResult,
    ChooseCommandDescriptionSourceInput,
    ChooseCommandDescriptionSourceResult,
    AppendCommandDescriptionRowsInput,
    AppendCommandDescriptionRowsResult,
    AppendCommandDescriptionStatusInput,
    AppendCommandDescriptionStatusResult,
    DrawDiplomacyCommandPanelInput,
    DrawDiplomacyCommandPanelResult,
    DrawDiplomacyCommandPanelService1,
    DrawDiplomacyCommandPanelService2,
    AppendDiplomacyCommandChoicesInput,
    AppendDiplomacyCommandChoicesResult,
    SetDiplomacyCommandMarkerInput,
    SetDiplomacyCommandMarkerResult,
    DrawDiplomacyParameterPanelInput,
    DrawDiplomacyParameterPanelResult,
    DrawDiplomacyParameterPanelService1,
    DrawDiplomacyParameterPanelService2,
    DrawDiplomacyParameterPanelService3,
    DrawDiplomacyParameterPanelService4,
    DrawDiplomacyParameterPanelService5,
    DrawDiplomacyParameterPanelService6,
    DrawDiplomacyParameterPanelService7,
    DrawDiplomacyParameterPanelService8,
    DrawDiplomacyParameterPanelService9,
    DrawDiplomacyParameterPanelService10,
    DrawDiplomacyParameterPanelService11,
    DrawDiplomacyParameterPanelService12,
    DrawDiplomacyParameterPanelService13,
    DrawDiplomacyParameterPanelService14,
    DrawDiplomacyParameterPanelAlternate1Input,
    DrawDiplomacyParameterPanelAlternate1Result,
    DrawDiplomacyParameterPanelAlternate1Service1,
    DrawDiplomacyParameterPanelAlternate1Service2,
    DrawDiplomacyParameterPanelAlternate1Service3,
    DrawDiplomacyParameterPanelAlternate1Service4,
    DrawDiplomacyParameterPanelAlternate1Service5,
    DrawDiplomacyParameterPanelAlternate1Service6,
    DrawDiplomacyParameterPanelAlternate1Service7,
    DrawDiplomacyParameterPanelAlternate1Service8,
    DrawDiplomacyParameterPanelAlternate1Service9,
    DrawDiplomacyParameterPanelAlternate1Service10,
    DrawDiplomacyParameterPanelAlternate1Service11,
    DrawDiplomacyParameterPanelAlternate1Service12,
    DrawDiplomacyParameterPanelAlternate1Service13,
    DrawDiplomacyParameterPanelAlternate1Service14,
    DrawDiplomacyParameterPanelAlternate1Service15,
    DrawDiplomacyParameterPanelAlternate1Service16,
    DrawDiplomacyParameterPanelAlternate1Service17,
    DrawDiplomacyParameterPanelAlternate1Service18,
    DrawDiplomacyParameterPanelAlternate1Service19,
    DrawDiplomacyParameterPanelAlternate1Service20,
    DrawDiplomacyParameterPanelAlternate1Service21,
    DrawDiplomacyParameterPanelAlternate1Service22,
    DrawDiplomacyParameterPanelAlternate1Service23,
    DrawDiplomacyParameterPanelAlternate2Input,
    DrawDiplomacyParameterPanelAlternate2Result,
    DrawDiplomacyParameterPanelAlternate2Service1,
    DrawDiplomacyParameterPanelAlternate2Service2,
    DrawDiplomacyParameterPanelAlternate2Service3,
)

from dataclasses import replace
from .contexts_commands import CommandLabelFrame
from .domain import Word, Table, uint, checked_table

from .contexts_commands import LocationChoiceFrame
from .contexts_display_reuse import MapSpriteTransaction
from .reuse_display import append_map_sprite_transaction

from .contexts_commands import ConfirmForceRelationSelectionFields

from .contexts_commands import CommandDescriptionFields

from .contexts_commands import CommandSelectionHeadingFields

def compose_current_city_fields(state: SceneState, inputs: ComposeCurrentCityFieldsInput) -> ComposeCurrentCityFieldsResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not ComposeCurrentCityFieldsInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row)
    returned=compose_current_city_frame_fields(state,entered)
    return ComposeCurrentCityFieldsResult(destination=returned.roster,source=returned.candidates,value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def start_current_city_packet(state: SceneState, inputs: StartCurrentCityPacketInput) -> StartCurrentCityPacketResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not StartCurrentCityPacketInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),controller=inputs.descriptor,scan=inputs.records,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit,offset_y=inputs.member,choice=inputs.remaining)
    returned=start_current_city_packet_fields(state,entered)
    return StartCurrentCityPacketResult(destination=returned.roster,source=returned.candidates,descriptor=returned.controller,records=returned.scan,value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,member=returned.offset_y,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_city_status_row(state: SceneState, inputs: AppendCityStatusRowInput) -> AppendCityStatusRowResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not AppendCityStatusRowInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,target_x=inputs.value,unit=inputs.tile)
    returned=append_city_status_row_fields(state,entered)
    return AppendCityStatusRowResult(destination=returned.roster,value=returned.target_x,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_city_name_fields(state: SceneState, inputs: AppendCityNameFieldsInput) -> AppendCityNameFieldsResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not AppendCityNameFieldsInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,candidates=inputs.source,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit,offset_y=inputs.member,choice=inputs.remaining)
    returned=append_city_name_frame_fields(state,entered)
    return AppendCityNameFieldsResult(destination=returned.roster,source=returned.candidates,descriptor=returned.controller,records=returned.scan,value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,member=returned.offset_y,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def store_city_status_value(state: SceneState, inputs: StoreCityStatusValueInput) -> StoreCityStatusValueResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not StoreCityStatusValueInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,distance=inputs.offset)
    returned=store_city_status_value_fields(state,entered)
    return StoreCityStatusValueResult(destination=returned.roster,offset=returned.distance,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_city_resource_row(state: SceneState, inputs: AppendCityResourceRowInput) -> AppendCityResourceRowResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not AppendCityResourceRowInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,target_x=inputs.value,unit=inputs.tile)
    returned=append_city_resource_row_fields(state,entered)
    return AppendCityResourceRowResult(destination=returned.roster,value=returned.target_x,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_selected_roster_values(state: SceneState, inputs: AppendSelectedRosterValuesInput) -> AppendSelectedRosterValuesResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not AppendSelectedRosterValuesInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,target_x=inputs.value,unit=inputs.tile,choice=inputs.remaining)
    returned=append_selected_roster_values_fields(state,entered)
    return AppendSelectedRosterValuesResult(destination=returned.roster,value=returned.target_x,tile=returned.unit,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def collect_city_officers_for_menu(state: SceneState, inputs: CollectCityOfficersForMenuInput) -> CollectCityOfficersForMenuResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not CollectCityOfficersForMenuInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row)
    returned=collect_city_officers_for_menu_fields(state,entered)
    return CollectCityOfficersForMenuResult(destination=returned.roster,value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_current_roster_marks(state: SceneState, inputs: AppendCurrentRosterMarksInput) -> AppendCurrentRosterMarksResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendCurrentRosterMarksInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),auxiliary=inputs.port,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset)
    returned=append_current_roster_marks_frame_fields(state,entered)
    return AppendCurrentRosterMarksResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def render_current_city_command_labels(state: SceneState, inputs: RenderCurrentCityCommandLabelsInput, *, label_frame: CommandLabelFrame | None=None) -> RenderCurrentCityCommandLabelsResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not RenderCurrentCityCommandLabelsInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=inputs.source .cursor(),unit=inputs.tile,count=inputs.row,distance=inputs.offset)
    returned=render_current_city_command_labels_frame_fields(state,entered)
    return RenderCurrentCityCommandLabelsResult(source=state.table_at(returned.candidates.base),tile=returned.unit,row=returned.count,offset=returned.distance,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def compose_city_roster_rows(state: SceneState, inputs: ComposeCityRosterRowsInput) -> ComposeCityRosterRowsResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not ComposeCityRosterRowsInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit)
    returned=compose_city_roster_rows_frame_fields(state,entered)
    return ComposeCityRosterRowsResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),descriptor=state.table_at(returned.controller.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def compose_selected_force_rows(state: SceneState, inputs: ComposeSelectedForceRowsInput) -> ComposeSelectedForceRowsResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not ComposeSelectedForceRowsInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),auxiliary=inputs.port,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row)
    returned=compose_selected_force_rows_frame_fields(state,entered)
    return ComposeSelectedForceRowsResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),tile=returned.unit,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_city_relation_row(state: SceneState, inputs: AppendCityRelationRowInput) -> AppendCityRelationRowResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendCityRelationRowInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),candidates=inputs.source .cursor(),controller=inputs.descriptor,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row)
    returned=append_city_relation_row_frame_fields(state,entered)
    return AppendCityRelationRowResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),descriptor=state.table_at(returned.controller.base),value=returned.target_x,field=returned.target_y,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def render_roster_name_or_prompt(state: SceneState, inputs: RenderRosterNameOrPromptInput) -> RenderRosterNameOrPromptResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not RenderRosterNameOrPromptInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),scan=inputs.records .cursor(),opponent=inputs.palette,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_y=inputs.member,choice=inputs.remaining)
    returned=render_roster_name_or_prompt_frame_fields(state,entered)
    return RenderRosterNameOrPromptResult(records=state.table_at(returned.scan.base),palette=state.table_at(returned.opponent.base),field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,member=returned.offset_y,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def render_selected_city_packet(state: SceneState, inputs: RenderSelectedCityPacketInput) -> RenderSelectedCityPacketResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not RenderSelectedCityPacketInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),scan=inputs.records .cursor(),target_y=inputs.field,count=inputs.row,choice=inputs.remaining)
    returned=render_selected_city_packet_frame_fields(state,entered)
    return RenderSelectedCityPacketResult(palette=state.table_at(returned.opponent.base),field=returned.target_y,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_force_roster_names(state: SceneState, inputs: AppendForceRosterNamesInput) -> AppendForceRosterNamesResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendForceRosterNamesInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),scan=inputs.records .cursor(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit,offset_y=inputs.member,choice=inputs.remaining,stack_cursor=inputs.stack_cursor)
    returned=append_force_roster_names_frame_fields(state,entered)
    return AppendForceRosterNamesResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),descriptor=state.table_at(returned.controller.base),records=state.table_at(returned.scan.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,member=returned.offset_y,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def start_selection_prompt(state: SceneState, inputs: StartSelectionPromptInput) -> StartSelectionPromptResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not StartSelectionPromptInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),)
    returned=start_selection_prompt_fields(state,entered)
    return StartSelectionPromptResult(destination=returned.roster,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_selection_prompt_heading(state: SceneState, inputs: AppendSelectionPromptHeadingInput) -> AppendSelectionPromptHeadingResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not AppendSelectionPromptHeadingInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,target_x=inputs.value)
    returned=append_selection_prompt_heading_fields(state,entered)
    return AppendSelectionPromptHeadingResult(destination=returned.roster,value=returned.target_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def set_selection_prompt_value(state: SceneState, inputs: SetSelectionPromptValueInput) -> SetSelectionPromptValueResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not SetSelectionPromptValueInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,target_x=inputs.value,target_y=inputs.field)
    returned=set_selection_prompt_value_fields(state,entered)
    return SetSelectionPromptValueResult(destination=returned.roster,value=returned.target_x,field=returned.target_y,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_selection_prompt_row(state: SceneState, inputs: AppendSelectionPromptRowInput) -> AppendSelectionPromptRowResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not AppendSelectionPromptRowInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,target_x=inputs.value)
    returned=append_selection_prompt_row_fields(state,entered)
    return AppendSelectionPromptRowResult(destination=returned.roster,value=returned.target_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_current_city_owner(state: SceneState, inputs: AppendCurrentCityOwnerInput) -> AppendCurrentCityOwnerResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not AppendCurrentCityOwnerInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,target_x=inputs.value,target_y=inputs.field)
    returned=append_current_city_owner_fields(state,entered)
    return AppendCurrentCityOwnerResult(destination=returned.roster,value=returned.target_x,field=returned.target_y,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def store_selection_prompt_value(state: SceneState, inputs: StoreSelectionPromptValueInput) -> StoreSelectionPromptValueResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not StoreSelectionPromptValueInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,target_y=inputs.field)
    returned=store_selection_prompt_value_fields(state,entered)
    return StoreSelectionPromptValueResult(destination=returned.roster,field=returned.target_y,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_selection_prompt_value(state: SceneState, inputs: AppendSelectionPromptValueInput) -> AppendSelectionPromptValueResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not AppendSelectionPromptValueInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,target_y=inputs.field)
    returned=append_selection_prompt_value_fields(state,entered)
    return AppendSelectionPromptValueResult(destination=returned.roster,field=returned.target_y,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_selected_force_head(state: SceneState, inputs: AppendSelectedForceHeadInput) -> AppendSelectedForceHeadResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendSelectedForceHeadInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,stack_cursor=inputs.stack_cursor)
    returned=append_selected_force_head_frame_fields(state,entered)
    return AppendSelectedForceHeadResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),value=returned.target_x,field=returned.target_y,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def compose_command_selection_prompt(state: SceneState, inputs: ComposeCommandSelectionPromptInput) -> ComposeCommandSelectionPromptResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not ComposeCommandSelectionPromptInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),unit=inputs.tile,count=inputs.row,choice=inputs.remaining)
    returned=compose_command_selection_prompt_frame_fields(state,entered)
    return ComposeCommandSelectionPromptResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),tile=returned.unit,row=returned.count,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def set_command_selection_cursor(state: SceneState, inputs: SetCommandSelectionCursorInput) -> SetCommandSelectionCursorResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not SetCommandSelectionCursorInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),count=inputs.row)
    returned=set_command_selection_cursor_frame_fields(state,entered)
    return SetCommandSelectionCursorResult(destination=state.table_at(returned.roster.base),row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def store_command_selection_value(state: SceneState, inputs: StoreCommandSelectionValueInput) -> StoreCommandSelectionValueResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not StoreCommandSelectionValueInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),count=inputs.row)
    returned=store_command_selection_value_frame_fields(state,entered)
    return StoreCommandSelectionValueResult(destination=state.table_at(returned.roster.base),row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_command_selection_heading(state: SceneState, inputs: AppendCommandSelectionHeadingInput) -> AppendCommandSelectionHeadingResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendCommandSelectionHeadingInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),unit=inputs.tile,count=inputs.row)
    returned=append_command_selection_heading_frame_fields(state,entered)
    return AppendCommandSelectionHeadingResult(destination=state.table_at(returned.roster.base),tile=returned.unit,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)




def append_command_selection_heading_fields(state: SceneState) -> CommandSelectionHeadingFields:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=append_command_selection_heading_frame_fields(state,entered)
    return CommandSelectionHeadingFields(destination=state.table_at(returned.roster.base),tile=low16(returned.unit),row=low16(returned.count),carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_command_confirmation_row(state: SceneState, inputs: AppendCommandConfirmationRowInput) -> AppendCommandConfirmationRowResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendCommandConfirmationRowInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,unit=inputs.tile,count=inputs.row)
    returned=append_command_confirmation_row_frame_fields(state,entered)
    return AppendCommandConfirmationRowResult(destination=state.table_at(returned.roster.base),value=returned.target_x,tile=returned.unit,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def present_current_command_prompt(state: SceneState, inputs: PresentCurrentCommandPromptInput) -> PresentCurrentCommandPromptResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not PresentCurrentCommandPromptInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,choice=inputs.remaining)
    returned=present_current_command_prompt_frame_fields(state,entered)
    return PresentCurrentCommandPromptResult(value=returned.target_x,field=returned.target_y,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def present_command_warning(state: SceneState, inputs: PresentCommandWarningInput) -> PresentCommandWarningResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not PresentCommandWarningInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_y=inputs.field,unit=inputs.tile)
    returned=present_command_warning_frame_fields(state,entered)
    return PresentCommandWarningResult(destination=state.table_at(returned.roster.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_contextual_cursor_commands(state: SceneState, inputs: AppendContextualCursorCommandsInput) -> AppendContextualCursorCommandsResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendContextualCursorCommandsInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value)
    returned=append_contextual_cursor_commands_frame_fields(state,entered)
    return AppendContextualCursorCommandsResult(value=returned.target_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)



def append_contextual_cursor_command_frame(state: SceneState, frame: MapTickFrame) -> MapTickFrame:
    """A370: merge the live controllers and consume either true 1A16E tail."""
    checked_tick_frame(frame, state)
    value = frame.motion_x
    field = frame.motion_y
    arithmetic_carry = False
    arithmetic_overflow = False
    value_is_zero = False
    value_is_negative = False
    read_value_1 = state.read(0xfffff612, 2)
    comparison_left = u16(read_value_1)
    comparison_right = u16(521)
    tested_value = u16(comparison_left - comparison_right)
    value_is_zero = tested_value == 0
    value_is_negative = bool(tested_value & 32768)
    arithmetic_carry = comparison_left < comparison_right
    arithmetic_overflow = bool(((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right))) & 32768)
    if not value_is_zero:
        read_value_2 = state.read(0xfffff612, 2)
        comparison_left = u16(read_value_2)
        comparison_right = u16(519)
        tested_value = u16(comparison_left - comparison_right)
        value_is_zero = tested_value == 0
        value_is_negative = bool(tested_value & 32768)
        arithmetic_carry = comparison_left < comparison_right
        arithmetic_overflow = bool(((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right))) & 32768)
        if not value_is_zero:
            read_value_3 = state.read(0xfffff376, 2)
            value = replace_word(value, u16(read_value_3))
            read_value_4 = state.read(0xfffff67c, 2)
            comparison_left = u16(low16(value))
            comparison_right = u16(read_value_4)
            tested_value = u16(comparison_left - comparison_right)
            value_is_zero = tested_value == 0
            value_is_negative = bool(tested_value & 32768)
            arithmetic_carry = comparison_left < comparison_right
            arithmetic_overflow = bool(((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right))) & 32768)
            if value_is_zero:
                read_value_5 = state.read(0xfffff604, 2)
                state.write(0xfffff602, 2, u16(read_value_5))
                tested_value = u16(read_value_5)
                value_is_zero = tested_value == 0
                value_is_negative = bool(tested_value & 32768)
                arithmetic_carry = False
                arithmetic_overflow = False
            else:
                read_value_6 = state.read(0xfffff67e, 2)
                comparison_left = u16(low16(value))
                comparison_right = u16(read_value_6)
                tested_value = u16(comparison_left - comparison_right)
                value_is_zero = tested_value == 0
                value_is_negative = bool(tested_value & 32768)
                arithmetic_carry = comparison_left < comparison_right
                arithmetic_overflow = bool(((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right))) & 32768)
                if value_is_zero:
                    read_value_7 = state.read(0xfffff604, 2)
                    state.write(0xfffff602, 2, u16(read_value_7))
                    tested_value = u16(read_value_7)
                    value_is_zero = tested_value == 0
                    value_is_negative = bool(tested_value & 32768)
                    arithmetic_carry = False
                    arithmetic_overflow = False
                else:
                    read_value_8 = state.read(0xfffff67a, 2)
                    comparison_left = u16(low16(value))
                    comparison_right = u16(read_value_8)
                    tested_value = u16(comparison_left - comparison_right)
                    value_is_zero = tested_value == 0
                    value_is_negative = bool(tested_value & 32768)
                    arithmetic_carry = comparison_left < comparison_right
                    arithmetic_overflow = bool(((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right))) & 32768)
                    if not value_is_zero:
                        read_value_9 = state.read(0xfffff604, 2)
                        value = replace_word(value, u16(read_value_9))
                        read_value_10 = state.read(0xfffff602, 2)
                        old_value_11 = u16(read_value_10)
                        amount_12 = u16(low16(value))
                        state.write(0xfffff602, 2, u16(old_value_11 | amount_12))
                        read_value_13 = state.read(0xfffff602, 2)
                        state.write(0xfffff604, 2, u16(read_value_13))
                        tested_value = u16(read_value_13)
                        value_is_zero = tested_value == 0
                        value_is_negative = bool(tested_value & 32768)
                        arithmetic_carry = False
                        arithmetic_overflow = False
        else:
            read_value_14 = state.read(0xffffefe0, 2)
            comparison_left = u16(read_value_14)
            comparison_right = u16(0)
            tested_value = u16(comparison_left - comparison_right)
            value_is_zero = tested_value == 0
            value_is_negative = bool(tested_value & 32768)
            arithmetic_carry = comparison_left < comparison_right
            arithmetic_overflow = bool(((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right))) & 32768)
            if value_is_zero:
                read_value_15 = state.read(0xfffff376, 2)
                value = replace_word(value, u16(read_value_15))
                read_value_16 = state.read(0xfffff67c, 2)
                comparison_left = u16(low16(value))
                comparison_right = u16(read_value_16)
                tested_value = u16(comparison_left - comparison_right)
                value_is_zero = tested_value == 0
                value_is_negative = bool(tested_value & 32768)
                arithmetic_carry = comparison_left < comparison_right
                arithmetic_overflow = bool(((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right))) & 32768)
                if value_is_zero:
                    read_value_17 = state.read(0xfffff604, 2)
                    state.write(0xfffff602, 2, u16(read_value_17))
                    tested_value = u16(read_value_17)
                    value_is_zero = tested_value == 0
                    value_is_negative = bool(tested_value & 32768)
                    arithmetic_carry = False
                    arithmetic_overflow = False
                else:
                    read_value_18 = state.read(0xfffff67e, 2)
                    comparison_left = u16(low16(value))
                    comparison_right = u16(read_value_18)
                    tested_value = u16(comparison_left - comparison_right)
                    value_is_zero = tested_value == 0
                    value_is_negative = bool(tested_value & 32768)
                    arithmetic_carry = comparison_left < comparison_right
                    arithmetic_overflow = bool(((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right))) & 32768)
                    if value_is_zero:
                        read_value_19 = state.read(0xfffff604, 2)
                        state.write(0xfffff602, 2, u16(read_value_19))
                        tested_value = u16(read_value_19)
                        value_is_zero = tested_value == 0
                        value_is_negative = bool(tested_value & 32768)
                        arithmetic_carry = False
                        arithmetic_overflow = False
                    else:
                        read_value_20 = state.read(0xfffff67a, 2)
                        comparison_left = u16(low16(value))
                        comparison_right = u16(read_value_20)
                        tested_value = u16(comparison_left - comparison_right)
                        value_is_zero = tested_value == 0
                        value_is_negative = bool(tested_value & 32768)
                        arithmetic_carry = comparison_left < comparison_right
                        arithmetic_overflow = bool(((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right))) & 32768)
                        if not value_is_zero:
                            read_value_21 = state.read(0xfffff604, 2)
                            value = replace_word(value, u16(read_value_21))
                            read_value_22 = state.read(0xfffff602, 2)
                            old_value_23 = u16(read_value_22)
                            amount_24 = u16(low16(value))
                            state.write(0xfffff602, 2, u16(old_value_23 | amount_24))
                            read_value_25 = state.read(0xfffff602, 2)
                            state.write(0xfffff604, 2, u16(read_value_25))
                            tested_value = u16(read_value_25)
                            value_is_zero = tested_value == 0
                            value_is_negative = bool(tested_value & 32768)
                            arithmetic_carry = False
                            arithmetic_overflow = False
            else:
                return _call_contextual_controller(state,
                    replace(frame, motion_x=value, motion_y=field,
                        carry=arithmetic_carry, zero=value_is_zero,
                        negative=value_is_negative, overflow=arithmetic_overflow))
    else:
        read_value_27 = state.read(0xfffff362, 2)
        comparison_left = u16(read_value_27)
        comparison_right = u16(15)
        tested_value = u16(comparison_left - comparison_right)
        value_is_zero = tested_value == 0
        value_is_negative = bool(tested_value & 32768)
        arithmetic_carry = comparison_left < comparison_right
        arithmetic_overflow = bool(((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right))) & 32768)
        if not (value_is_zero):
            read_value_28 = state.read(0xfffff612, 2)
            comparison_left = u16(read_value_28)
            comparison_right = u16(519)
            tested_value = u16(comparison_left - comparison_right)
            value_is_zero = tested_value == 0
            value_is_negative = bool(tested_value & 32768)
            arithmetic_carry = comparison_left < comparison_right
            arithmetic_overflow = bool(((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right))) & 32768)
            if not value_is_zero:
                read_value_29 = state.read(0xfffff376, 2)
                value = replace_word(value, u16(read_value_29))
                read_value_30 = state.read(0xfffff67c, 2)
                comparison_left = u16(low16(value))
                comparison_right = u16(read_value_30)
                tested_value = u16(comparison_left - comparison_right)
                value_is_zero = tested_value == 0
                value_is_negative = bool(tested_value & 32768)
                arithmetic_carry = comparison_left < comparison_right
                arithmetic_overflow = bool(((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right))) & 32768)
                if value_is_zero:
                    read_value_31 = state.read(0xfffff604, 2)
                    state.write(0xfffff602, 2, u16(read_value_31))
                    tested_value = u16(read_value_31)
                    value_is_zero = tested_value == 0
                    value_is_negative = bool(tested_value & 32768)
                    arithmetic_carry = False
                    arithmetic_overflow = False
                else:
                    read_value_32 = state.read(0xfffff67e, 2)
                    comparison_left = u16(low16(value))
                    comparison_right = u16(read_value_32)
                    tested_value = u16(comparison_left - comparison_right)
                    value_is_zero = tested_value == 0
                    value_is_negative = bool(tested_value & 32768)
                    arithmetic_carry = comparison_left < comparison_right
                    arithmetic_overflow = bool(((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right))) & 32768)
                    if value_is_zero:
                        read_value_33 = state.read(0xfffff604, 2)
                        state.write(0xfffff602, 2, u16(read_value_33))
                        tested_value = u16(read_value_33)
                        value_is_zero = tested_value == 0
                        value_is_negative = bool(tested_value & 32768)
                        arithmetic_carry = False
                        arithmetic_overflow = False
                    else:
                        read_value_34 = state.read(0xfffff67a, 2)
                        comparison_left = u16(low16(value))
                        comparison_right = u16(read_value_34)
                        tested_value = u16(comparison_left - comparison_right)
                        value_is_zero = tested_value == 0
                        value_is_negative = bool(tested_value & 32768)
                        arithmetic_carry = comparison_left < comparison_right
                        arithmetic_overflow = bool(((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right))) & 32768)
                        if not value_is_zero:
                            read_value_35 = state.read(0xfffff604, 2)
                            value = replace_word(value, u16(read_value_35))
                            read_value_36 = state.read(0xfffff602, 2)
                            old_value_37 = u16(read_value_36)
                            amount_38 = u16(low16(value))
                            state.write(0xfffff602, 2, u16(old_value_37 | amount_38))
                            read_value_39 = state.read(0xfffff602, 2)
                            state.write(0xfffff604, 2, u16(read_value_39))
                            tested_value = u16(read_value_39)
                            value_is_zero = tested_value == 0
                            value_is_negative = bool(tested_value & 32768)
                            arithmetic_carry = False
                            arithmetic_overflow = False
            else:
                read_value_40 = state.read(0xffffefe0, 2)
                comparison_left = u16(read_value_40)
                comparison_right = u16(0)
                tested_value = u16(comparison_left - comparison_right)
                value_is_zero = tested_value == 0
                value_is_negative = bool(tested_value & 32768)
                arithmetic_carry = comparison_left < comparison_right
                arithmetic_overflow = bool(((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right))) & 32768)
                if value_is_zero:
                    read_value_41 = state.read(0xfffff376, 2)
                    value = replace_word(value, u16(read_value_41))
                    read_value_42 = state.read(0xfffff67c, 2)
                    comparison_left = u16(low16(value))
                    comparison_right = u16(read_value_42)
                    tested_value = u16(comparison_left - comparison_right)
                    value_is_zero = tested_value == 0
                    value_is_negative = bool(tested_value & 32768)
                    arithmetic_carry = comparison_left < comparison_right
                    arithmetic_overflow = bool(((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right))) & 32768)
                    if value_is_zero:
                        read_value_43 = state.read(0xfffff604, 2)
                        state.write(0xfffff602, 2, u16(read_value_43))
                        tested_value = u16(read_value_43)
                        value_is_zero = tested_value == 0
                        value_is_negative = bool(tested_value & 32768)
                        arithmetic_carry = False
                        arithmetic_overflow = False
                    else:
                        read_value_44 = state.read(0xfffff67e, 2)
                        comparison_left = u16(low16(value))
                        comparison_right = u16(read_value_44)
                        tested_value = u16(comparison_left - comparison_right)
                        value_is_zero = tested_value == 0
                        value_is_negative = bool(tested_value & 32768)
                        arithmetic_carry = comparison_left < comparison_right
                        arithmetic_overflow = bool(((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right))) & 32768)
                        if value_is_zero:
                            read_value_45 = state.read(0xfffff604, 2)
                            state.write(0xfffff602, 2, u16(read_value_45))
                            tested_value = u16(read_value_45)
                            value_is_zero = tested_value == 0
                            value_is_negative = bool(tested_value & 32768)
                            arithmetic_carry = False
                            arithmetic_overflow = False
                        else:
                            read_value_46 = state.read(0xfffff67a, 2)
                            comparison_left = u16(low16(value))
                            comparison_right = u16(read_value_46)
                            tested_value = u16(comparison_left - comparison_right)
                            value_is_zero = tested_value == 0
                            value_is_negative = bool(tested_value & 32768)
                            arithmetic_carry = comparison_left < comparison_right
                            arithmetic_overflow = bool(((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right))) & 32768)
                            if not value_is_zero:
                                read_value_47 = state.read(0xfffff604, 2)
                                value = replace_word(value, u16(read_value_47))
                                read_value_48 = state.read(0xfffff602, 2)
                                old_value_49 = u16(read_value_48)
                                amount_50 = u16(low16(value))
                                state.write(0xfffff602, 2, u16(old_value_49 | amount_50))
                                read_value_51 = state.read(0xfffff602, 2)
                                state.write(0xfffff604, 2, u16(read_value_51))
                                tested_value = u16(read_value_51)
                                value_is_zero = tested_value == 0
                                value_is_negative = bool(tested_value & 32768)
                                arithmetic_carry = False
                                arithmetic_overflow = False
                else:
                    return _call_contextual_controller(state,
                        replace(frame, motion_x=value, motion_y=field,
                            carry=arithmetic_carry, zero=value_is_zero,
                            negative=value_is_negative, overflow=arithmetic_overflow))
    return replace(frame, motion_x=value, motion_y=field,
        carry=arithmetic_carry, zero=value_is_zero, negative=value_is_negative,
        overflow=arithmetic_overflow)


def _call_contextual_controller(state: SceneState, frame: MapTickFrame) -> MapTickFrame:
    """A394 JSR uses current operands and a real logical callee-entry SP."""
    called = replace(frame, stack_cursor=frame.stack_cursor.advance(-4))
    result = checked_tick_frame(call_target(state, 0x1A16E, called), state)
    return replace(result, stack_cursor=result.stack_cursor.advance(4))

def draw_force_summary(state: SceneState, inputs: DrawForceSummaryInput) -> DrawForceSummaryResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not DrawForceSummaryInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,count=inputs.row)
    returned=draw_force_summary_frame_fields(state,entered)
    return DrawForceSummaryResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),value=returned.target_x,field=returned.target_y,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def draw_first_force_prompt(state: SceneState, inputs: DrawFirstForcePromptInput) -> DrawFirstForcePromptResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not DrawFirstForcePromptInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_y=inputs.field,unit=inputs.tile)
    returned=draw_first_force_prompt_frame_fields(state,entered)
    return DrawFirstForcePromptResult(destination=state.table_at(returned.roster.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def draw_second_force_prompt(state: SceneState, inputs: DrawSecondForcePromptInput) -> DrawSecondForcePromptResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not DrawSecondForcePromptInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_y=inputs.field,unit=inputs.tile)
    returned=draw_second_force_prompt_frame_fields(state,entered)
    return DrawSecondForcePromptResult(destination=state.table_at(returned.roster.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def update_selected_force_prompt(state: SceneState, inputs: UpdateSelectedForcePromptInput) -> UpdateSelectedForcePromptResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not UpdateSelectedForcePromptInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field)
    returned=update_selected_force_prompt_fields(state,entered)
    return UpdateSelectedForcePromptResult(value=returned.target_x,field=returned.target_y,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def draw_current_scenario_prompt(state: SceneState, inputs: DrawCurrentScenarioPromptInput) -> DrawCurrentScenarioPromptResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not DrawCurrentScenarioPromptInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit)
    returned=draw_current_scenario_prompt_frame_fields(state,entered)
    return DrawCurrentScenarioPromptResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),roster=state.table_at(returned.scratch.base),port=state.table_at(returned.auxiliary.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_scenario_owner_glyphs(state: SceneState, inputs: AppendScenarioOwnerGlyphsInput) -> AppendScenarioOwnerGlyphsResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendScenarioOwnerGlyphsInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),scratch=inputs.roster,auxiliary=inputs.port,target_x=inputs.value,target_y=inputs.field)
    returned=append_scenario_owner_glyphs_frame_fields(state,entered)
    return AppendScenarioOwnerGlyphsResult(destination=state.table_at(returned.roster.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_scenario_owner_value(state: SceneState, inputs: AppendScenarioOwnerValueInput) -> AppendScenarioOwnerValueResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendScenarioOwnerValueInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field)
    returned=append_scenario_owner_value_frame_fields(state,entered)
    return AppendScenarioOwnerValueResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),value=returned.target_x,field=returned.target_y,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def draw_title_mode_prompt(state: SceneState, inputs: DrawTitleModePromptInput) -> DrawTitleModePromptResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not DrawTitleModePromptInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit)
    returned=draw_title_mode_prompt_frame_fields(state,entered)
    return DrawTitleModePromptResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def compose_title_option_panel(state: SceneState, inputs: ComposeTitleOptionPanelInput) -> ComposeTitleOptionPanelResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not ComposeTitleOptionPanelInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=inputs.source .cursor(),auxiliary=inputs.port,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit,offset_y=inputs.member,stack_cursor=inputs.stack_cursor)
    returned=compose_title_option_panel_frame_fields(state,entered)
    return ComposeTitleOptionPanelResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),port=state.table_at(returned.auxiliary.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,member=returned.offset_y,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_title_option_glyphs(state: SceneState, inputs: AppendTitleOptionGlyphsInput) -> AppendTitleOptionGlyphsResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendTitleOptionGlyphsInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),candidates=inputs.source .cursor(),auxiliary=inputs.port,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit,offset_y=inputs.member,stack_cursor=inputs.stack_cursor)
    returned=append_title_option_glyphs_frame_fields(state,entered)
    return AppendTitleOptionGlyphsResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),port=state.table_at(returned.auxiliary.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,member=returned.offset_y,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_title_option_digit(state: SceneState, inputs: AppendTitleOptionDigitInput) -> AppendTitleOptionDigitResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendTitleOptionDigitInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),target_x=inputs.value,unit=inputs.tile,distance=inputs.offset)
    returned=append_title_option_digit_frame_fields(state,entered)
    return AppendTitleOptionDigitResult(destination=state.table_at(returned.roster.base),tile=returned.unit,offset=returned.distance,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def store_title_option_digit(state: SceneState, inputs: StoreTitleOptionDigitInput) -> StoreTitleOptionDigitResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not StoreTitleOptionDigitInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),unit=inputs.tile)
    returned=store_title_option_digit_frame_fields(state,entered)
    return StoreTitleOptionDigitResult(destination=state.table_at(returned.roster.base),tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def set_title_option_marker(state: SceneState, inputs: SetTitleOptionMarkerInput) -> SetTitleOptionMarkerResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not SetTitleOptionMarkerInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),target_x=inputs.value,unit=inputs.tile,count=inputs.row)
    returned=set_title_option_marker_frame_fields(state,entered)
    return SetTitleOptionMarkerResult(destination=state.table_at(returned.roster.base),tile=returned.unit,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_title_option_decorations(state: SceneState, inputs: AppendTitleOptionDecorationsInput) -> AppendTitleOptionDecorationsResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendTitleOptionDecorationsInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),candidates=inputs.source .cursor(),auxiliary=inputs.port,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit,offset_y=inputs.member,stack_cursor=inputs.stack_cursor)
    returned=append_title_option_decorations_frame_fields(state,entered)
    return AppendTitleOptionDecorationsResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),port=state.table_at(returned.auxiliary.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,member=returned.offset_y,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_title_option_decoration_value(state: SceneState, inputs: AppendTitleOptionDecorationValueInput) -> AppendTitleOptionDecorationValueResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendTitleOptionDecorationValueInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),unit=inputs.tile)
    returned=append_title_option_decoration_value_frame_fields(state,entered)
    return AppendTitleOptionDecorationValueResult(destination=state.table_at(returned.roster.base),tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_world_cursor_coordinates(state: SceneState, inputs: AppendWorldCursorCoordinatesInput, *, current_frame: LocationChoiceFrame | None=None) -> AppendWorldCursorCoordinatesResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendWorldCursorCoordinatesInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile)
    returned=append_world_cursor_coordinates_frame_fields(state,entered)
    return AppendWorldCursorCoordinatesResult(destination=state.table_at(returned.roster.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def draw_roster_overview(state: SceneState, inputs: DrawRosterOverviewInput) -> DrawRosterOverviewResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not DrawRosterOverviewInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),opponent=inputs.palette,scratch=inputs.roster,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset)
    returned=draw_roster_overview_frame_fields(state,entered)
    return DrawRosterOverviewResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),descriptor=state.table_at(returned.controller.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_roster_overview_cursor(state: SceneState, inputs: AppendRosterOverviewCursorInput) -> AppendRosterOverviewCursorResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendRosterOverviewCursorInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),opponent=inputs.palette,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row)
    returned=append_roster_overview_cursor_frame_fields(state,entered)
    return AppendRosterOverviewCursorResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),descriptor=state.table_at(returned.controller.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def draw_roster_overview_values(state: SceneState, inputs: DrawRosterOverviewValuesInput) -> DrawRosterOverviewValuesResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not DrawRosterOverviewValuesInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),opponent=inputs.palette,scratch=inputs.roster,target_y=inputs.field,unit=inputs.tile)
    returned=draw_roster_overview_values_frame_fields(state,entered)
    return DrawRosterOverviewValuesResult(value=returned.target_x,field=returned.target_y,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_selected_city_head(state: SceneState, inputs: AppendSelectedCityHeadInput) -> AppendSelectedCityHeadResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendSelectedCityHeadInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,distance=inputs.offset)
    returned=append_selected_city_head_frame_fields(state,entered)
    return AppendSelectedCityHeadResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,offset=returned.distance,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_roster_overview_digit(state: SceneState, inputs: AppendRosterOverviewDigitInput) -> AppendRosterOverviewDigitResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendRosterOverviewDigitInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),opponent=inputs.palette,scratch=inputs.roster,target_y=inputs.field,unit=inputs.tile,count=inputs.row,choice=inputs.remaining)
    returned=append_roster_overview_digit_frame_fields(state,entered)
    return AppendRosterOverviewDigitResult(destination=state.table_at(returned.roster.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def retain_roster_overview_column(state: SceneState, inputs: RetainRosterOverviewColumnInput) -> RetainRosterOverviewColumnResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not RetainRosterOverviewColumnInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),opponent=inputs.palette,unit=inputs.tile,count=inputs.row)
    returned=retain_roster_overview_column_frame_fields(state,entered)
    return RetainRosterOverviewColumnResult(row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def compose_officer_detail_panel(state: SceneState, inputs: ComposeOfficerDetailPanelInput) -> ComposeOfficerDetailPanelResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not ComposeOfficerDetailPanelInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=inputs.source .cursor(),opponent=inputs.palette,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit,stack_cursor=inputs.stack_cursor)
    returned=compose_officer_detail_panel_frame_fields(state,entered)
    return ComposeOfficerDetailPanelResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),port=state.table_at(returned.auxiliary.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_officer_name_value(state: SceneState, inputs: AppendOfficerNameValueInput) -> AppendOfficerNameValueResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not AppendOfficerNameValueInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,candidates=inputs.source,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit,stack_cursor=inputs.stack_cursor)
    returned=append_officer_name_value_fields(state,entered)
    return AppendOfficerNameValueResult(destination=returned.roster,source=returned.candidates,port=returned.auxiliary,value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_officer_name_value_alternate_1(state: SceneState, inputs: AppendOfficerNameValueAlternate1Input) -> AppendOfficerNameValueAlternate1Result:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not AppendOfficerNameValueAlternate1Input:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,candidates=inputs.source,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit,stack_cursor=inputs.stack_cursor)
    returned=append_officer_name_value_alternate_1_fields(state,entered)
    return AppendOfficerNameValueAlternate1Result(destination=returned.roster,source=returned.candidates,port=returned.auxiliary,value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_officer_name_value_alternate_2(state: SceneState, inputs: AppendOfficerNameValueAlternate2Input) -> AppendOfficerNameValueAlternate2Result:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not AppendOfficerNameValueAlternate2Input:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,candidates=inputs.source,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit,stack_cursor=inputs.stack_cursor)
    returned=append_officer_name_value_alternate_2_fields(state,entered)
    return AppendOfficerNameValueAlternate2Result(destination=returned.roster,source=returned.candidates,port=returned.auxiliary,value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_officer_name_value_alternate_3(state: SceneState, inputs: AppendOfficerNameValueAlternate3Input) -> AppendOfficerNameValueAlternate3Result:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not AppendOfficerNameValueAlternate3Input:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=inputs.source,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit,stack_cursor=inputs.stack_cursor)
    returned=append_officer_name_value_alternate_3_fields(state,entered)
    return AppendOfficerNameValueAlternate3Result(destination=returned.roster,source=returned.candidates,port=returned.auxiliary,value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_officer_name_value_alternate_4(state: SceneState, inputs: AppendOfficerNameValueAlternate4Input) -> AppendOfficerNameValueAlternate4Result:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not AppendOfficerNameValueAlternate4Input:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=inputs.source,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit,stack_cursor=inputs.stack_cursor)
    returned=append_officer_name_value_alternate_4_fields(state,entered)
    return AppendOfficerNameValueAlternate4Result(destination=returned.roster,source=returned.candidates,port=returned.auxiliary,value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_officer_attribute_value(state: SceneState, inputs: AppendOfficerAttributeValueInput) -> AppendOfficerAttributeValueResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendOfficerAttributeValueInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),opponent=inputs.palette,scratch=inputs.roster,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit,stack_cursor=inputs.stack_cursor)
    returned=append_officer_attribute_value_frame_fields(state,entered)
    return AppendOfficerAttributeValueResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),port=state.table_at(returned.auxiliary.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def scale_officer_detail_value(state: SceneState, inputs: ScaleOfficerDetailValueInput) -> ScaleOfficerDetailValueResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not ScaleOfficerDetailValueInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),opponent=inputs.palette,scratch=inputs.roster,target_x=inputs.value,target_y=inputs.field,count=inputs.row)
    returned=scale_officer_detail_value_frame_fields(state,entered)
    return ScaleOfficerDetailValueResult(value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_officer_detail_commands(state: SceneState, inputs: AppendOfficerDetailCommandsInput) -> AppendOfficerDetailCommandsResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendOfficerDetailCommandsInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),opponent=inputs.palette,scratch=inputs.roster,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,stack_cursor=inputs.stack_cursor)
    returned=append_officer_detail_commands_frame_fields(state,entered)
    return AppendOfficerDetailCommandsResult(destination=state.table_at(returned.roster.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_officer_detail_title(state: SceneState, inputs: AppendOfficerDetailTitleInput) -> AppendOfficerDetailTitleResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendOfficerDetailTitleInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),opponent=inputs.palette,target_y=inputs.field,count=inputs.row)
    returned=append_officer_detail_title_frame_fields(state,entered)
    return AppendOfficerDetailTitleResult(field=returned.target_y,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def draw_officer_detail_view(state: SceneState, inputs: DrawOfficerDetailViewInput) -> DrawOfficerDetailViewResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not DrawOfficerDetailViewInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_y=inputs.member,choice=inputs.remaining)
    returned=draw_officer_detail_view_frame_fields(state,entered)
    return DrawOfficerDetailViewResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),descriptor=state.table_at(returned.controller.base),port=state.table_at(returned.auxiliary.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,member=returned.offset_y,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_officer_detail_rows(state: SceneState, inputs: AppendOfficerDetailRowsInput) -> AppendOfficerDetailRowsResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendOfficerDetailRowsInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),auxiliary=inputs.port,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,offset_y=inputs.member,choice=inputs.remaining)
    returned=append_officer_detail_rows_frame_fields(state,entered)
    return AppendOfficerDetailRowsResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),descriptor=state.table_at(returned.controller.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,member=returned.offset_y,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def open_roster_selection_message(state: SceneState, inputs: OpenRosterSelectionMessageInput) -> OpenRosterSelectionMessageResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not OpenRosterSelectionMessageInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),scan=inputs.records .cursor(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile)
    returned=open_roster_selection_message_frame_fields(state,entered)
    return OpenRosterSelectionMessageResult(source=state.table_at(returned.candidates.base),descriptor=state.table_at(returned.controller.base),records=state.table_at(returned.scan.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def set_roster_selection_notice(state: SceneState, inputs: SetRosterSelectionNoticeInput) -> SetRosterSelectionNoticeResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not SetRosterSelectionNoticeInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value)
    returned=set_roster_selection_notice_frame_fields(state,entered)
    return SetRosterSelectionNoticeResult(value=returned.target_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def draw_force_relation_view(state: SceneState, inputs: DrawForceRelationViewInput) -> DrawForceRelationViewResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not DrawForceRelationViewInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,choice=inputs.remaining)
    returned=draw_force_relation_view_frame_fields(state,entered)
    return DrawForceRelationViewResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),port=state.table_at(returned.auxiliary.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_force_relation_commands(state: SceneState, inputs: AppendForceRelationCommandsInput) -> AppendForceRelationCommandsResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not AppendForceRelationCommandsInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,choice=inputs.remaining,stack_cursor=inputs.stack_cursor)
    returned=append_force_relation_commands_fields(state,entered)
    return AppendForceRelationCommandsResult(destination=returned.roster,value=returned.target_x,field=returned.target_y,tile=returned.unit,remaining=returned.choice,stack_cursor=returned.stack_cursor,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_force_relation_heading(state: SceneState, inputs: AppendForceRelationHeadingInput) -> AppendForceRelationHeadingResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not AppendForceRelationHeadingInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,target_x=inputs.value)
    returned=append_force_relation_heading_fields(state,entered)
    return AppendForceRelationHeadingResult(destination=returned.roster,value=returned.target_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def set_force_relation_markers(state: SceneState, inputs: SetForceRelationMarkersInput) -> SetForceRelationMarkersResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not SetForceRelationMarkersInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,target_x=inputs.value,choice=inputs.remaining)
    returned=set_force_relation_markers_fields(state,entered)
    return SetForceRelationMarkersResult(destination=returned.roster,value=returned.target_x,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_force_relation_value_row(state: SceneState, inputs: AppendForceRelationValueRowInput) -> AppendForceRelationValueRowResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not AppendForceRelationValueRowInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,target_x=inputs.value)
    returned=append_force_relation_value_row_fields(state,entered)
    return AppendForceRelationValueRowResult(destination=returned.roster,value=returned.target_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_force_relation_footer(state: SceneState, inputs: AppendForceRelationFooterInput) -> AppendForceRelationFooterResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not AppendForceRelationFooterInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,target_x=inputs.value)
    returned=append_force_relation_footer_fields(state,entered)
    return AppendForceRelationFooterResult(destination=returned.roster,value=returned.target_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_force_relation_label(state: SceneState, inputs: AppendForceRelationLabelInput) -> AppendForceRelationLabelResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendForceRelationLabelInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile)
    returned=append_force_relation_label_frame_fields(state,entered)
    return AppendForceRelationLabelResult(destination=state.table_at(returned.roster.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_force_relation_digits(state: SceneState, inputs: AppendForceRelationDigitsInput) -> AppendForceRelationDigitsResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendForceRelationDigitsInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile)
    returned=append_force_relation_digits_frame_fields(state,entered)
    return AppendForceRelationDigitsResult(destination=state.table_at(returned.roster.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def adjust_force_relation_selection(state: SceneState, inputs: AdjustForceRelationSelectionInput) -> AdjustForceRelationSelectionResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AdjustForceRelationSelectionInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=adjust_force_relation_selection_frame_fields(state,entered)
    return AdjustForceRelationSelectionResult(carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def confirm_force_relation_selection(state: SceneState, inputs: ConfirmForceRelationSelectionInput) -> ConfirmForceRelationSelectionResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not ConfirmForceRelationSelectionInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile)
    returned=confirm_force_relation_selection_frame_fields(state,entered)
    return ConfirmForceRelationSelectionResult(destination=state.table_at(returned.roster.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)



def confirm_force_relation_selection_fields(state: SceneState) -> ConfirmForceRelationSelectionFields:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=confirm_force_relation_selection_frame_fields(state,entered)
    return ConfirmForceRelationSelectionFields(destination_if_written=returned.roster,value_if_written=low16(returned.target_x),field_if_written=low16(returned.target_y),tile_if_written=low16(returned.unit),carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def draw_command_cost_panel(state: SceneState, inputs: DrawCommandCostPanelInput) -> DrawCommandCostPanelResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not DrawCommandCostPanelInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),candidates=inputs.source .cursor(),controller=inputs.descriptor,scan=inputs.records .cursor(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit,offset_y=inputs.member,choice=inputs.remaining)
    returned=draw_command_cost_panel_frame_fields(state,entered)
    return DrawCommandCostPanelResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),descriptor=state.table_at(returned.controller.base),records=state.table_at(returned.scan.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,member=returned.offset_y,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def draw_command_cost_panel_alternate_1(state: SceneState, inputs: DrawCommandCostPanelAlternate1Input) -> DrawCommandCostPanelAlternate1Result:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not DrawCommandCostPanelAlternate1Input:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),controller=inputs.descriptor,scan=inputs.records .cursor(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit,offset_y=inputs.member,choice=inputs.remaining)
    returned=draw_command_cost_panel_alternate_1_frame_fields(state,entered)
    return DrawCommandCostPanelAlternate1Result(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),descriptor=state.table_at(returned.controller.base),records=state.table_at(returned.scan.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,member=returned.offset_y,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def divide_and_scale_command_value(state: SceneState, inputs: DivideAndScaleCommandValueInput) -> DivideAndScaleCommandValueResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not DivideAndScaleCommandValueInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row)
    returned=collect_force_relation_candidates_fields(state,entered)
    return DivideAndScaleCommandValueResult(destination=returned.roster,source=returned.candidates,descriptor=returned.controller,field=returned.target_y,tile=returned.unit,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def append_selected_city_command(state: SceneState, inputs: AppendSelectedCityCommandInput) -> AppendSelectedCityCommandResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendSelectedCityCommandInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=inputs.source .cursor(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit,offset_y=inputs.member)
    returned=append_selected_city_command_frame_fields(state,entered)
    return AppendSelectedCityCommandResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,member=returned.offset_y,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def store_selected_city_command_value(state: SceneState, inputs: StoreSelectedCityCommandValueInput) -> StoreSelectedCityCommandValueResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not StoreSelectedCityCommandValueInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),distance=inputs.offset,offset_x=inputs.limit)
    returned=store_selected_city_command_value_frame_fields(state,entered)
    return StoreSelectedCityCommandValueResult(destination=state.table_at(returned.roster.base),offset=returned.distance,limit=returned.offset_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_city_command_heading(state: SceneState, inputs: AppendCityCommandHeadingInput) -> AppendCityCommandHeadingResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendCityCommandHeadingInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row)
    returned=append_city_command_heading_frame_fields(state,entered)
    return AppendCityCommandHeadingResult(destination=state.table_at(returned.roster.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_current_command_description(state: SceneState, inputs: AppendCurrentCommandDescriptionInput) -> AppendCurrentCommandDescriptionResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendCurrentCommandDescriptionInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),candidates=inputs.source .cursor(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row)
    returned=append_current_command_description_frame_fields(state,entered)
    return AppendCurrentCommandDescriptionResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)




def append_current_command_description_fields(state: SceneState) -> CommandDescriptionFields:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=append_current_command_description_frame_fields(state,entered)
    return CommandDescriptionFields(destination_if_written=state.table_at(returned.roster.base),source_if_written=state.table_at(returned.candidates.base),value_if_written=low16(returned.target_x),field_if_written=low16(returned.target_y),tile_if_written=low16(returned.unit),row_if_written=low16(returned.count),carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def choose_command_description_source(state: SceneState, inputs: ChooseCommandDescriptionSourceInput) -> ChooseCommandDescriptionSourceResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not ChooseCommandDescriptionSourceInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),candidates=inputs.source .cursor(),count=inputs.row)
    returned=choose_command_description_source_frame_fields(state,entered)
    return ChooseCommandDescriptionSourceResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)



def choose_command_description_source_fields(state: SceneState, destination: Table) -> CommandDescriptionFields:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    checked_table(destination,state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=destination.cursor())
    returned=choose_command_description_source_frame_fields(state,entered)
    return CommandDescriptionFields(destination_if_written=state.table_at(returned.roster.base),source_if_written=state.table_at(returned.candidates.base),value_if_written=low16(returned.target_x),field_if_written=low16(returned.target_y),tile_if_written=low16(returned.unit),row_if_written=low16(returned.count),carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_command_description_rows(state: SceneState, inputs: AppendCommandDescriptionRowsInput) -> AppendCommandDescriptionRowsResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendCommandDescriptionRowsInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile)
    returned=append_command_description_rows_frame_fields(state,entered)
    return AppendCommandDescriptionRowsResult(destination=state.table_at(returned.roster.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)



def append_command_description_rows_fields(state: SceneState) -> CommandDescriptionFields:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=append_command_description_rows_frame_fields(state,entered)
    return CommandDescriptionFields(destination_if_written=state.table_at(returned.roster.base),source_if_written=state.table_at(returned.candidates.base),value_if_written=low16(returned.target_x),field_if_written=low16(returned.target_y),tile_if_written=low16(returned.unit),row_if_written=low16(returned.count),carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_command_description_status(state: SceneState, inputs: AppendCommandDescriptionStatusInput) -> AppendCommandDescriptionStatusResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AppendCommandDescriptionStatusInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile)
    returned=append_command_description_status_frame_fields(state,entered)
    return AppendCommandDescriptionStatusResult(destination=state.table_at(returned.roster.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)



def append_command_description_status_fields(state: SceneState) -> CommandDescriptionFields:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=append_command_description_status_frame_fields(state,entered)
    return CommandDescriptionFields(destination_if_written=state.table_at(returned.roster.base),source_if_written=state.table_at(returned.candidates.base),value_if_written=low16(returned.target_x),field_if_written=low16(returned.target_y),tile_if_written=low16(returned.unit),row_if_written=low16(returned.count),carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def draw_diplomacy_command_panel(state: SceneState, inputs: DrawDiplomacyCommandPanelInput) -> DrawDiplomacyCommandPanelResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not DrawDiplomacyCommandPanelInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,count=inputs.row)
    returned=draw_diplomacy_command_panel_frame_fields(state,entered)
    return DrawDiplomacyCommandPanelResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),roster=state.table_at(returned.scratch.base),port=state.table_at(returned.auxiliary.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def append_diplomacy_command_choices(state: SceneState, inputs: AppendDiplomacyCommandChoicesInput) -> AppendDiplomacyCommandChoicesResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not AppendDiplomacyCommandChoicesInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile)
    returned=append_diplomacy_command_choices_fields(state,entered)
    return AppendDiplomacyCommandChoicesResult(destination=returned.roster,value=returned.target_x,field=returned.target_y,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def set_diplomacy_command_marker(state: SceneState, inputs: SetDiplomacyCommandMarkerInput) -> SetDiplomacyCommandMarkerResult:
    """Historical typed observations call the sole complete rule; no missing ABI is invented."""
    checked_state(state)
    if type(inputs) is not SetDiplomacyCommandMarkerInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile)
    returned=set_diplomacy_command_marker_fields(state,entered)
    return SetDiplomacyCommandMarkerResult(destination=returned.roster,value=returned.target_x,field=returned.target_y,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def draw_diplomacy_parameter_panel(state: SceneState, inputs: DrawDiplomacyParameterPanelInput) -> DrawDiplomacyParameterPanelResult:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    from .contexts_display_fields import display_legacy_frame_fields
    entered = display_legacy_frame_fields(state, inputs, 57198)
    return draw_diplomacy_parameter_panel_frame_fields(state, entered)

def draw_diplomacy_parameter_panel_alternate_1(state: SceneState, inputs: DrawDiplomacyParameterPanelAlternate1Input) -> DrawDiplomacyParameterPanelAlternate1Result:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    from .contexts_display_fields import display_legacy_frame_fields
    entered = display_legacy_frame_fields(state, inputs, 199008)
    return draw_diplomacy_parameter_panel_alternate_1_frame_fields(state, entered)

def draw_diplomacy_parameter_panel_alternate_2(state: SceneState, inputs: DrawDiplomacyParameterPanelAlternate2Input) -> DrawDiplomacyParameterPanelAlternate2Result:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    from .contexts_display_fields import display_legacy_frame_fields
    entered = display_legacy_frame_fields(state, inputs, 421918)
    return draw_diplomacy_parameter_panel_alternate_2_frame_fields(state, entered)


def require_command_label_stack_domain(state: SceneState,
        frame: CommandLabelFrame, depth: Word) -> None:
    """Stop known stack/DATA aliases; do not claim physical stack execution.

    The established glyph service preserves semantic saved carriers, but its
    physical call/MOVEM accesses are not implemented. This compatibility
    domain protects the known label DATA footprint only, not arbitrary CPU
    return-token/interrupt behavior. Ordinary reserved stack bytes are not
    written, and full native stack-RAM equivalence is deliberately unclaimed.
    """
    checked_state(state)
    if type(frame) is not CommandLabelFrame:
        raise ValueError('complete current label frame required')
    frame.validate(state)
    uint(depth, 16, 'actual temporary label stack depth')
    physical = frame.stack_cursor.base & 0xFFFFFF
    if physical < 0xFF0000 or physical >= 0x1000000 or physical & 1:
        raise Boundary('label stack is outside the ordinary aligned RAM domain')
    top = physical & 0xFFFF
    if top < depth:
        raise Boundary('label stack window wraps the RAM boundary')
    lower = top - depth
    packet = frame.packet_cursor.base & 0xFFFFFF
    if 0xFF0000 <= packet < 0x1000000:
        packet_start = packet & 0xFFFF
        if packet_start + 512 > 65536:
            raise Boundary('label packet leaves the ordinary nonwrapping RAM domain')
        if lower < packet_start + 512 and packet_start < top + 4:
            raise Boundary('current glyph packet/physical stack alias is not implemented')
    for start, size in ((0xD300, 0x200), (0xF500, 2), (0xF578, 2),
            (0xF390, 2), (0xF38C, 2), (0xF36C, 2), (0xF65A, 2),
            (0xF612, 2), (0xF362, 2), (0xF656, 2), (0xF6C4, 2)):
        if lower < start + size and start < top + 4:
            raise Boundary('physical glyph stack/DATA alias is not yet implemented')

def render_current_city_command_label_frame(state: SceneState, frame: CommandLabelFrame) -> CommandLabelFrame:
    """The historical four-flag observation does not invent full SR-X for the sole label core."""
    checked_state(state)
    if type(frame) is not CommandLabelFrame:raise ValueError('actual historical label observations required')
    frame.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=frame.background,target_y=frame.foreground,
        unit=frame.selector,count=frame.glyph_rows,distance=frame.upload_count,offset_x=frame.code_index,
        offset_y=frame.emitted_labels,choice=frame.glyph_scratch,roster=frame.glyph_source.cursor(),
        candidates=frame.packet_cursor.cursor(),controller=frame.label_codes,scan=frame.code_lookup.cursor(),
        opponent=frame.auxiliary_view,scratch=frame.retained_view,auxiliary=frame.vdp_data_port,stack_cursor=frame.stack_cursor)
    returned=render_current_city_command_labels_frame_fields(state,entered)
    return replace(frame,background=returned.target_x,foreground=returned.target_y,selector=returned.unit,
        glyph_rows=returned.count,upload_count=returned.distance,code_index=returned.offset_x,
        emitted_labels=returned.offset_y,glyph_scratch=returned.choice,glyph_source=state.table_at(returned.roster.base),
        packet_cursor=state.table_at(returned.candidates.base),label_codes=returned.controller,
        code_lookup=state.table_at(returned.scan.base),auxiliary_view=returned.opponent,retained_view=returned.scratch,
        vdp_data_port=returned.auxiliary,stack_cursor=returned.stack_cursor,carry=bool(returned.status&1),
        zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)



def append_world_cursor_coordinate_frame(state: SceneState,
        frame: LocationChoiceFrame) -> LocationChoiceFrame:
    """AB40: genuine current cursor drawing and final AC08 conditions."""
    checked_state(state)
    if type(frame) is not LocationChoiceFrame:
        raise ValueError('complete current location frame required')
    frame.validate(state)
    suppressed=bool(state.read(0xFFFFF321,1)&8)
    if suppressed:
        # BTST only changed Z; do not clear actual incoming C/N/V.
        return replace(frame,zero=False)
    choice=state.read(0xFFFFF35C,2)&7
    attributes=replace_word(frame.sprite_attributes,choice)
    if choice:
        position=24
        if state.read(0xFFFFF35D,1)&8:
            position=160
    else:
        position=124
    attributes=replace_word(attributes,u16(low16(attributes)<<3))
    value=replace_word(frame.motion_value,low16(attributes))
    attributes=replace_word(attributes,u16(low16(attributes)<<1))
    value=replace_word(value,u16(low16(value)+low16(attributes)))
    value=replace_word(value,u16(low16(value)+16))
    attributes=replace_word(attributes,0)
    source=state.table_at(0xAB82).cursor()
    result=append_map_sprite_transaction(state,source,value,
        replace_word(frame.prompt_field,position),attributes,
        reset_scroll=True,initialize_clip=True)
    if type(result) is not MapSpriteTransaction:
        raise Boundary('AB7A requires the true complete sprite return')
    result.validate(state)
    return replace(frame,sprite_source=result.source,motion_value=result.x,
        prompt_field=result.y,sprite_attributes=result.attributes,carry=result.carry,
        zero=result.zero,negative=result.negative,overflow=result.overflow)


def append_selected_city_command_fields(state: SceneState) -> SelectedCityCommandFields:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    entered=first_replace(FirstDeploymentFrame.unobserved())
    returned=append_selected_city_command_frame_fields(state,entered)
    return SelectedCityCommandFields(destination=state.table_at(returned.roster.base),source_if_written=state.table_at(returned.candidates.base),value_word=low16(returned.target_x),field_word=low16(returned.target_y),tile_if_written=low16(returned.unit),row_if_written=low16(returned.count),offset_if_written=low16(returned.distance),limit_if_written=low16(returned.offset_x),member_if_written=low16(returned.offset_y),carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)



def store_selected_city_command_fields(state: SceneState, destination: Table, offset: Word, limit: Word) -> StoreSelectedCityCommandFields:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    checked_table(destination,state)
    uint(offset,16)
    uint(limit,16)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=destination.cursor())
    returned=store_selected_city_command_value_frame_fields(state,entered)
    return StoreSelectedCityCommandFields(destination=state.table_at(returned.roster.base),offset_word=low16(returned.distance),limit_word=low16(returned.offset_x),carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


from .contexts_gameplay import (
    FirstDeploymentFrame, FirstDeploymentReturnBoundary, MovementContinuationBoundary, first_replace,
)
from .business_movement_support import (
    _movement_frame, _movement_move, _movement_move_long, _movement_test,
    _movement_compare, _movement_binary_flags, _movement_fixed_shift_word,
    _movement_arithmetic_long, _movement_multiply_word, _movement_divu_word,
)


def _city_ui_frame_fields(state: SceneState, frame: FirstDeploymentFrame,
        entry: int) -> FirstDeploymentFrame:
    """Historical partial UI observations never invent complete register/CCR/SP inputs."""
    checked_state(state)
    if type(frame) is not FirstDeploymentFrame:
        raise ValueError('actual full city UI fields required')
    values=(frame.target_x,frame.target_y,frame.unit,frame.count,frame.distance,
        frame.offset_x,frame.offset_y,frame.choice,frame.roster,frame.candidates,
        frame.controller,frame.scan,frame.opponent,frame.scratch,frame.auxiliary,
        frame.stack_cursor,frame.status)
    if any(value is None for value in values):
        raise MovementContinuationBoundary(entry,frame,'old city UI input did not observe the complete entry ABI')
    return _movement_frame(state,frame)


def _city_ui_store_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, value: int, size: int=2, clear: bool=False) -> FirstDeploymentFrame:
    """Reuse the sole live RAM MOVE flags; actual CLR also performs its prior read."""
    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
    from ..high_level_gameplay_flow.business_services import _scene_refresh_emit
    if size not in (1,2,4) or type(clear) is not bool:
        raise ValueError('actual city packet store width required')
    if clear:
        state.read(address,size)
        value=0
    return _scene_refresh_emit(SceneRefreshMemory(state),frame,address,size,value)


def _city_ui_append_fields(state: SceneState, frame: FirstDeploymentFrame,
        value: int, size: int=2, clear: bool=False) -> FirstDeploymentFrame:
    """One real postincrement RAM write, not a render or hardware callback."""
    frame=_city_ui_store_fields(state,frame,frame.roster.base,value,size,clear)
    return first_replace(frame,roster=frame.roster.advance(size))


def _city_ui_arithmetic_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, source: int, subtract: bool=False, width: int=16) -> FirstDeploymentFrame:
    """Reuse existing arithmetic flags and retain the actual narrow-write high bits."""
    destination=low8(frame.carrier(name)) if width==8 else low16(frame.carrier(name))
    source=low8(source) if width==8 else low16(source)
    frame,result=_movement_binary_flags(state,frame,destination,source,width,subtract)
    value=replace_byte(frame.carrier(name),result) if width==8 else replace_word(frame.carrier(name),result)
    return first_replace(frame,**{name:value})


def _city_ui_memory_arithmetic_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, source: int, subtract: bool=False) -> FirstDeploymentFrame:
    """Actual WORD RMW, without a MOVE that would destroy ADD/SUB flags."""
    previous=state.read(address,2)
    frame,result=_movement_binary_flags(state,frame,previous,low16(source),16,subtract)
    state.write(address,2,result)
    return frame


def _city_ui_bit_fields(state: SceneState, frame: FirstDeploymentFrame,
        value: int, bit: int) -> FirstDeploymentFrame:
    """Shared BTST changes only Z; its original width comes from the supplied value."""
    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
    from ..high_level_scene_flows.business_scene import _scene_render_bit
    return _scene_render_bit(SceneRefreshMemory(state),frame,value,1<<bit)


def _city_ui_shift_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, count: int) -> FirstDeploymentFrame:
    """Existing original logical WORD shifts, including the already closed #7."""
    if count==7:
        from ..high_level_remaining_flows.business_city import _duel_commit_shift_fields
        return _duel_commit_shift_fields(state,frame,name,count)
    return _movement_fixed_shift_word(state,frame,name,count)


def _city_ui_child_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """One real child slot; known decimal/message cores own their existing outer bridge."""
    if target in (0x676F2,0x1270A):
        from ..high_level_remaining_flows.business_city import _deployment_menu_call_fields
        return _deployment_menu_call_fields(state,frame,target,continuation)
    stack=frame.stack_cursor.advance(-4)
    stack.set_long(0,continuation)
    entered=first_replace(frame,stack_cursor=stack)
    if target==0x4B5A:
        returned=append_city_status_row_fields(state,entered)
    elif target==0x4B7A:
        returned=append_city_name_frame_fields(state,entered)
    elif target==0x4C1A:
        returned=store_city_status_value_fields(state,entered)
    elif target==0x4C34:
        returned=append_city_resource_row_fields(state,entered)
    elif target==0x4C54:
        returned=append_selected_roster_values_fields(state,entered)
    elif target==0x56B0:
        returned=append_selection_prompt_heading_fields(state,entered)
    elif target==0x56D0:
        returned=set_selection_prompt_value_fields(state,entered)
    elif target==0x5714:
        returned=append_selection_prompt_row_fields(state,entered)
    elif target==0x5740:
        returned=append_current_city_owner_fields(state,entered)
    elif target==0x577C:
        returned=store_selection_prompt_value_fields(state,entered)
    elif target==0x5794:
        returned=append_selection_prompt_value_fields(state,entered)
    elif target==0xC420:
        returned=append_force_relation_heading_fields(state,entered)
    elif target==0xC438:
        returned=set_force_relation_markers_fields(state,entered)
    elif target==0xC466:
        returned=append_force_relation_value_row_fields(state,entered)
    elif target==0xC47E:
        returned=append_force_relation_footer_fields(state,entered)
    elif target==0xDDEC:
        returned=set_diplomacy_command_marker_fields(state,entered)
    else:
        raise MovementContinuationBoundary(target,entered,'no fabricated city UI child return')
    returned=_city_ui_frame_fields(state,returned,target)
    actual=returned.stack_cursor.long()
    if actual!=continuation:
        raise FirstDeploymentReturnBoundary(actual,returned,continuation)
    return first_replace(returned,stack_cursor=returned.stack_cursor.advance(4))


def compose_current_city_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4AB2: build the real command BYTE list from city ownership and quality thresholds."""
    frame=_city_ui_frame_fields(state,frame,0x4AB2)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF372,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC600).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF580).cursor())
    frame=_movement_move(state,frame,'count',state.read(0xFFFFF376,2),16)
    frame=_city_ui_shift_fields(state,frame,'count',1)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFE640).cursor())
    frame=_movement_compare(state,frame,low16(frame.target_x),frame.candidates.word(low16(frame.count)),16)
    if not frame.status&4:
        frame=_movement_compare(state,frame,low8(frame.target_y),20,8)
        if not frame.status&1:
            frame=first_replace(frame,candidates=state.table_at(0xFFFFC700).cursor())
            frame=_movement_move(state,frame,'unit',frame.candidates.byte(low16(frame.target_x)),8)
            frame=_movement_move(state,frame,'unit',low8(frame.unit)&7,8)
            frame=_movement_compare(state,frame,low8(frame.unit),3,8)
            if not frame.status&1:
                frame=_city_ui_append_fields(state,frame,1,1)
                frame=_city_ui_arithmetic_fields(state,frame,'unit',1)
        for threshold,command in ((15,2),(10,3)):
            frame=_movement_compare(state,frame,low8(frame.target_y),threshold,8)
            if not frame.status&1:
                frame=_city_ui_append_fields(state,frame,command,1)
                frame=_city_ui_arithmetic_fields(state,frame,'unit',1)
        frame=_movement_compare(state,frame,state.read(0xFFFFF580,1),1,8)
        if not frame.status&4:
            frame=_movement_compare(state,frame,low8(frame.target_y),5,8)
            if not frame.status&1:
                frame=_city_ui_append_fields(state,frame,4,1)
                frame=_city_ui_arithmetic_fields(state,frame,'unit',1)
    frame=_city_ui_store_fields(state,frame,0xFFFFF3B2,low16(frame.unit))
    return _city_ui_store_fields(state,frame,frame.roster.base,0,1,True)


def start_current_city_packet_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4B28: start one city RAM packet, then use its four real direct children."""
    frame=_city_ui_frame_fields(state,frame,0x4B28)
    frame=first_replace(frame,roster=state.table_at(u32(0xFFFFD100+s16(state.read(0xFFFFF31A,2)))).cursor())
    frame=_movement_move(state,frame,'unit',0xC41E,16)
    frame=_movement_move(state,frame,'choice',0,16)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFF580).cursor())
    frame=_movement_test(state,frame,frame.candidates.byte(low16(frame.choice)),8)
    if not frame.status&4:
        for target,continuation in ((0x4B5A,0x4B44),(0x4B7A,0x4B48),(0x4C34,0x4B4C)):
            frame=_city_ui_child_fields(state,frame,target,continuation)
    frame=_city_ui_child_fields(state,frame,0x4C54,0x4B50)
    frame=_city_ui_store_fields(state,frame,frame.roster.base,0,2,True)
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,240)


def _city_ui_border_row_fields(state: SceneState, frame: FirstDeploymentFrame,
        resource: bool) -> FirstDeploymentFrame:
    """City status/resource rows share only their actual ten-cell border shape."""
    frame=_city_ui_append_fields(state,frame,10)
    frame=_city_ui_append_fields(state,frame,low16(frame.unit))
    frame=_city_ui_arithmetic_fields(state,frame,'unit',128)
    frame=_city_ui_append_fields(state,frame,0xD380 if resource else 0xC380)
    frame=_movement_move(state,frame,'target_x',7,16)
    while True:
        frame=_city_ui_append_fields(state,frame,0xD381 if resource else 0xC381)
        frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
        if low16(frame.target_x)==65535:
            break
    return _city_ui_append_fields(state,frame,0xDB80 if resource else 0xCB80)


def append_city_status_row_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4B5A: append the original city status border row."""
    return _city_ui_border_row_fields(state,_city_ui_frame_fields(state,frame,0x4B5A),False)


def append_city_resource_row_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4C34: append the original city resource border row."""
    return _city_ui_border_row_fields(state,_city_ui_frame_fields(state,frame,0x4C34),True)


def store_city_status_value_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4C1A: one actual four-WORD glyph pair, with the original three D4 increments."""
    frame=_city_ui_frame_fields(state,frame,0x4C1A)
    for position in (0,1):
        frame=_city_ui_store_fields(state,frame,frame.roster.base,low16(frame.distance))
        frame=_city_ui_arithmetic_fields(state,frame,'distance',1)
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+24),low16(frame.distance))
        if not position:
            frame=_city_ui_arithmetic_fields(state,frame,'distance',1)
        frame=first_replace(frame,roster=frame.roster.advance(2))
    return frame


def append_city_name_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4B7A: actual available-command labels and their paired RAM glyph rows."""
    frame=_city_ui_frame_fields(state,frame,0x4B7A)
    frame=_movement_move(state,frame,'unit',0xC49E,16)
    frame=_movement_move(state,frame,'offset_x',0,16)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF372,2),16)
    frame=_city_ui_shift_fields(state,frame,'target_y',1)
    frame=first_replace(frame,scan=state.table_at(0xFFFFC000).cursor())
    frame=_movement_move(state,frame,'offset_y',frame.scan.word(low16(frame.target_y)),16)
    frame=first_replace(frame,scan=state.table_at(0xFFFFBE00).cursor())
    frame=_movement_compare(state,frame,low16(frame.offset_y),frame.scan.word(low16(frame.target_y)),16)
    if frame.status&1:
        frame=_movement_move(state,frame,'offset_x',4,16)
    while True:
        value=frame.candidates.byte()
        frame=first_replace(frame,candidates=frame.candidates.advance(1))
        frame=_movement_move(state,frame,'target_y',value,8)
        frame=_city_ui_arithmetic_fields(state,frame,'target_y',low8(frame.offset_x),False,8)
        frame=_city_ui_arithmetic_fields(state,frame,'choice',1)
        frame=_movement_move(state,frame,'target_y',u16(s8(low8(frame.target_y))),16)
        frame=_city_ui_shift_fields(state,frame,'target_y',2)
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+24),10)
        frame=_city_ui_append_fields(state,frame,10)
        frame=_city_ui_store_fields(state,frame,frame.roster.base,low16(frame.unit))
        frame=_city_ui_arithmetic_fields(state,frame,'unit',128)
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+24),low16(frame.unit))
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_city_ui_arithmetic_fields(state,frame,'unit',128)
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+24),0xC382)
        frame=_city_ui_append_fields(state,frame,0xC382)
        frame=first_replace(frame,controller=state.table_at(0x92C26))
        frame=_movement_move(state,frame,'count',3,16)
        while True:
            frame=_movement_move(state,frame,'distance',0xC000,16)
            frame=_movement_move(state,frame,'distance',frame.controller.byte(low16(frame.target_y)),8)
            frame=_city_ui_child_fields(state,frame,0x4C1A,0x4BE0)
            frame=_city_ui_arithmetic_fields(state,frame,'target_y',1)
            frame=first_replace(frame,count=replace_word(frame.count,u16(low16(frame.count)-1)))
            if low16(frame.count)==65535:
                break
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+24),0xCB82)
        frame=_city_ui_append_fields(state,frame,0xCB82)
        frame=first_replace(frame,roster=frame.roster.advance(24))
        frame=_movement_test(state,frame,frame.candidates.byte(),8)
        if frame.status&4:
            return frame
        frame=_city_ui_append_fields(state,frame,10)
        frame=_city_ui_append_fields(state,frame,low16(frame.unit))
        frame=_city_ui_arithmetic_fields(state,frame,'unit',128)
        frame=_city_ui_append_fields(state,frame,0xC382)
        frame=_movement_move(state,frame,'target_x',7,16)
        while True:
            frame=_city_ui_append_fields(state,frame,0xC001)
            frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
            if low16(frame.target_x)==65535:
                break
        frame=_city_ui_append_fields(state,frame,0xCB82)


def append_selected_roster_values_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4C54: fill the remaining city menu rows using the original three/four-row layouts."""
    frame=_city_ui_frame_fields(state,frame,0x4C54)
    while True:
        frame=_movement_test(state,frame,low16(frame.choice),16)
        first=bool(frame.status&4)
        if not first:
            frame=_movement_compare(state,frame,low16(frame.choice),2,16)
            if not frame.status&5:
                return frame
        extra=(72,48,24) if first else (48,24)
        for displacement in extra:
            frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+displacement),10)
        frame=_city_ui_append_fields(state,frame,10)
        frame=_city_ui_store_fields(state,frame,frame.roster.base,low16(frame.unit))
        frame=_city_ui_arithmetic_fields(state,frame,'unit',128)
        for displacement in ((24,48,72) if first else (24,48)):
            frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+displacement),low16(frame.unit))
            frame=_city_ui_arithmetic_fields(state,frame,'unit',128)
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_movement_move(state,frame,'target_x',9,16)
        while True:
            for displacement in extra:
                frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+displacement),0,2,True)
            frame=_city_ui_append_fields(state,frame,0,2,True)
            frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
            if low16(frame.target_x)==65535:
                break
        frame=first_replace(frame,roster=frame.roster.advance(72 if first else 48))
        frame=_city_ui_arithmetic_fields(state,frame,'choice',1)


def _city_ui_collect_notice_fields(state: SceneState, frame: FirstDeploymentFrame,
        message: int, continuation: int, retain_actor: bool) -> FirstDeploymentFrame:
    """Four actual notice roles share the same sole message child, not a callback."""
    if (message,continuation,retain_actor) not in ((183,0x4F6A,False),
            (190,0x4F7C,False),(196,0x4F92,True),(201,0x4FA8,True)):
        raise ValueError('closed original officer notice role required')
    if retain_actor:
        frame=_city_ui_store_fields(state,frame,0xFFFFF3D0,low16(frame.target_x))
    frame=_movement_move(state,frame,'target_x',message,16)
    frame=_city_ui_child_fields(state,frame,0x676F2,continuation)
    return _movement_move(state,frame,'target_y',1,16)


def collect_city_officers_for_menu_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4E50: actual command-specific officer eligibility and four original notices."""
    frame=_city_ui_frame_fields(state,frame,0x4E50)
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_test(state,frame,state.read(0xFFFFF656,2),16)
    if not frame.status&4:
        return frame
    for address,value in ((0xFFFFF380,122),(0xFFFFF38C,81)):
        frame=_movement_compare(state,frame,state.read(address,2),value,16)
        if frame.status&4:
            return frame
    frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),103,16)
    if frame.status&4:
        frame=_movement_test(state,frame,state.read(0xFFFFF3B2,2),16)
        return _city_ui_arithmetic_fields(state,frame,'target_y',1) if frame.status&4 else frame
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),125,16)
    if frame.status&4:
        frame=_movement_move(state,frame,'unit',low16(frame.target_x),16)
        frame=_city_ui_shift_fields(state,frame,'unit',1)
        frame=first_replace(frame,roster=state.table_at(0xFFFFB600).cursor())
        frame=_movement_move(state,frame,'count',frame.roster.word(low16(frame.unit)),16)
        frame=_movement_compare(state,frame,low16(frame.count),100,16)
        if not frame.status&1:
            return frame
        frame=_movement_compare(state,frame,low16(frame.count),95,16)
        if not frame.status&1:
            frame=first_replace(frame,roster=state.table_at(0xFFFFC000).cursor())
            frame=_movement_compare(state,frame,frame.roster.word(low16(frame.unit)),150,16)
            if not frame.status&1:
                return frame
        return _city_ui_arithmetic_fields(state,frame,'target_y',1)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),41,16)
    if frame.status&4:
        return frame
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),30,16)
    if frame.status&4:
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF634,2),16)
        if frame.status&4:
            return _city_ui_collect_notice_fields(state,frame,183,0x4F6A,False)
        frame=first_replace(frame,roster=state.table_at(0xFFFFC300).cursor())
        frame=_movement_compare(state,frame,frame.roster.byte(low16(frame.target_x)),100,8)
        if frame.status&4:
            return _city_ui_collect_notice_fields(state,frame,196,0x4F92,True)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),88,16)
    if frame.status&4:
        frame=first_replace(frame,roster=state.table_at(0xFFFFC500).cursor())
        frame=_movement_compare(state,frame,frame.roster.byte(low16(frame.target_x)),100,8)
        if frame.status&4:
            return _city_ui_collect_notice_fields(state,frame,201,0x4FA8,True)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),98,16)
    if frame.status&4:
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF634,2),16)
        if frame.status&4:
            return _city_ui_collect_notice_fields(state,frame,190,0x4F7C,False)
    frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),100,16)
    if frame.status&4:
        return frame
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF364,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF427).cursor())
    frame=_movement_move(state,frame,'unit',frame.roster.byte(low16(frame.unit)),8)
    frame=_movement_compare(state,frame,low8(frame.unit),state.read(0xFFFFF377,1),8)
    if not frame.status&4:
        return frame
    frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),145,16)
    if frame.status&4:
        return frame
    frame=first_replace(frame,roster=state.table_at(0xFFFFCD00).cursor())
    frame=_movement_move(state,frame,'unit',frame.roster.byte(low16(frame.target_x)),8)
    if frame.status&4:
        return frame
    frame=_movement_compare(state,frame,low16(frame.unit),1,16)
    if frame.status&4:
        return _city_ui_arithmetic_fields(state,frame,'target_y',1)
    frame=_movement_move(state,frame,'target_y',1,16)
    frame=_city_ui_store_fields(state,frame,0xFFFFF3A6,low16(frame.target_x))
    return _city_ui_store_fields(state,frame,0xFFFFF362,16)


def start_selection_prompt_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5694: one live city selection packet and its three exact PC-relative child slots."""
    frame=_city_ui_frame_fields(state,frame,0x5694)
    frame=first_replace(frame,roster=state.table_at(u32(0xFFFFD100+s16(state.read(0xFFFFF31A,2)))).cursor())
    for target,continuation in ((0x56B0,0x56A0),(0x56D0,0x56A6),(0x5714,0x56AC)):
        frame=_city_ui_child_fields(state,frame,target,continuation)
    return frame


def _city_ui_selection_border_fields(state: SceneState, frame: FirstDeploymentFrame,
        footer: bool) -> FirstDeploymentFrame:
    """The two actual selection border roles share only their eleven-cell RAM layout."""
    frame=_city_ui_append_fields(state,frame,11)
    frame=_city_ui_append_fields(state,frame,0xC21C if footer else 0xC09C)
    frame=_city_ui_append_fields(state,frame,0xD380 if footer else 0xC380)
    frame=_movement_move(state,frame,'target_x',8,16)
    while True:
        frame=_city_ui_append_fields(state,frame,0xD381 if footer else 0xC381)
        frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
        if low16(frame.target_x)==65535:
            break
    frame=_city_ui_append_fields(state,frame,0xDB80 if footer else 0xCB80)
    return _city_ui_store_fields(state,frame,frame.roster.base,0,2,True)


def append_selection_prompt_heading_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """56B0: actual city-selection heading packet."""
    return _city_ui_selection_border_fields(state,_city_ui_frame_fields(state,frame,0x56B0),False)


def set_selection_prompt_value_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """56D0: paired selection value rows with real owner and value child calls."""
    frame=_city_ui_frame_fields(state,frame,0x56D0)
    for upper,lower in ((11,11),(0xC19C,0xC11C),(0xC382,0xC382)):
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+26),upper)
        frame=_city_ui_append_fields(state,frame,lower)
    frame=_city_ui_child_fields(state,frame,0x5740,0x56F2)
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+26),0xC001)
    frame=_city_ui_append_fields(state,frame,0xC001)
    frame=_city_ui_child_fields(state,frame,0x5794,0x5700)
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+26),0xCB82)
    frame=_city_ui_append_fields(state,frame,0xCB82)
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+26),0,2,True)
    return first_replace(frame,roster=frame.roster.advance(26))


def append_selection_prompt_row_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5714: append selection footer, advance the real packet length and set its flags."""
    frame=_city_ui_selection_border_fields(state,_city_ui_frame_fields(state,frame,0x5714),True)
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,104)
    return _city_ui_store_fields(state,frame,0xFFFFF3A4,state.read(0xFFFFF3A4,2)|0x9000)


def append_current_city_owner_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5740: actual two-digit owner glyph rule, including WORD ASL and LONG addition."""
    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
    from ..high_level_scene_flows.business_scene import _scene_render_asl_word
    frame=_city_ui_frame_fields(state,frame,0x5740)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&255,16)
    frame=_movement_move(state,frame,'target_y',0,16)
    while True:
        frame=_city_ui_arithmetic_fields(state,frame,'target_x',10,True)
        if frame.status&1:
            break
        frame=_city_ui_arithmetic_fields(state,frame,'target_y',1)
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',10)
    frame=_movement_test(state,frame,low16(frame.target_y),16)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_y',0xC001,16)
    else:
        frame=_city_ui_shift_fields(state,frame,'target_y',2)
        frame=_city_ui_arithmetic_fields(state,frame,'target_y',0xC0D8)
    frame=_city_ui_child_fields(state,frame,0x577C,0x576C)
    frame=_scene_render_asl_word(SceneRefreshMemory(state),frame,'target_x',low16(frame.target_x),2)
    frame=_movement_arithmetic_long(state,frame,'target_x',0xC0D8)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    return _city_ui_child_fields(state,frame,0x577C,0x577A)


def store_selection_prompt_value_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """577C: store the actual four-WORD paired owner/value glyph with three increments."""
    frame=_city_ui_frame_fields(state,frame,0x577C)
    for position in (0,26,2,28):
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+position),low16(frame.target_y))
        if position!=28:
            frame=_city_ui_arithmetic_fields(state,frame,'target_y',1)
    return first_replace(frame,roster=frame.roster.advance(4))


def append_selection_prompt_value_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5794: two real short-BSR value-glyph children, without an extra synthetic slot."""
    frame=_city_ui_frame_fields(state,frame,0x5794)
    frame=_movement_move(state,frame,'target_y',0xC300,16)
    frame=_city_ui_child_fields(state,frame,0x577C,0x579A)
    frame=_city_ui_arithmetic_fields(state,frame,'target_y',1)
    return _city_ui_child_fields(state,frame,0x577C,0x579E)


def update_selected_force_prompt_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A530: original force-page cursor timing, priority and row/page wrapping."""
    frame=_city_ui_frame_fields(state,frame,0xA530)
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF608,1,True)
    if not frame.status&4:
        return frame
    frame=_city_ui_store_fields(state,frame,0xFFFFF608,8)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,1),8)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF35C,2),16)
    direction=None
    for bit in (0,1,3,2):
        frame=_city_ui_bit_fields(state,frame,frame.target_x,bit)
        if not frame.status&4:
            direction=bit
            break
    if direction is None:
        return _city_ui_store_fields(state,frame,0xFFFFF608,1)
    if direction==0:
        frame=_movement_move(state,frame,'target_y',low16(frame.target_y)&7,16)
        if not frame.status&4:
            return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF35C,1,True)
        frame=_movement_move(state,frame,'target_y',7,16)
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF358,14,True)
        if frame.status&1:
            frame=_city_ui_store_fields(state,frame,0xFFFFF358,29)
            frame=_movement_move(state,frame,'target_y',6,16)
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF35C,low16(frame.target_y))
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF612,1)
        return _city_ui_store_fields(state,frame,0xFFFFF35A,0,2,True)
    if direction==1:
        frame=_movement_move(state,frame,'target_y',low16(frame.target_y)&7,16)
        frame=_movement_compare(state,frame,low16(frame.target_y),7,16)
        wrap=not bool(frame.status&1)
        if not wrap:
            frame=_movement_compare(state,frame,state.read(0xFFFFF358,2),29,16)
            if frame.status&4:
                frame=_movement_compare(state,frame,low16(frame.target_y),6,16)
                wrap=not bool(frame.status&1)
        if not wrap:
            return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF35C,1)
        frame=_movement_move(state,frame,'target_y',7,16)
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF358,14)
        frame=_movement_compare(state,frame,state.read(0xFFFFF358,2),40,16)
        if not frame.status&1:
            frame=_movement_move(state,frame,'target_y',6,16)
            frame=_city_ui_store_fields(state,frame,0xFFFFF358,1)
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF35C,low16(frame.target_y),True)
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF612,1)
        return _city_ui_store_fields(state,frame,0xFFFFF35A,0,2,True)
    if direction==3:
        frame=_city_ui_arithmetic_fields(state,frame,'target_y',8)
        frame=_movement_compare(state,frame,low16(frame.target_y),16,16)
        if not frame.status&1:
            return frame
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF35C,8)
        if not frame.status&1:
            return frame
    frame=_city_ui_arithmetic_fields(state,frame,'target_y',8,True)
    if frame.status&8:
        return frame
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF35C,8,True)


def append_officer_name_value_fields(state: SceneState, frame: FirstDeploymentFrame,
        entry: int=0xB92C) -> FirstDeploymentFrame:
    """B92C whole: five closed original attribute entry roles and one sole decimal tail."""
    if entry not in (0xB92C,0xB938,0xB94C,0xB958,0xB982):
        raise ValueError('actual officer attribute entry role required')
    frame=_city_ui_frame_fields(state,frame,entry)
    if entry in (0xB92C,0xB94C):
        frame=_movement_move_long(state,frame,'target_x',0)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF372,2),16)
        if entry==0xB92C:
            frame=_city_ui_shift_fields(state,frame,'target_x',1)
            frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
        else:
            frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_x)),8)
    elif entry==0xB958:
        frame=first_replace(frame,roster=state.table_at(0xFFFFB400).cursor())
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF372,2),16)
        frame=_city_ui_shift_fields(state,frame,'target_x',1)
        frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_x)),16)
        frame=first_replace(frame,roster=state.table_at(0xFFFFC500).cursor())
        frame=_movement_fixed_shift_word(state,frame,'target_x',1,True)
        frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_x)),8)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&255,16)
        frame=_movement_multiply_word(state,frame,'target_x',low16(frame.target_y))
        frame=_movement_divu_word(state,frame,'target_x',100,0xB976)
        frame=_movement_move_long(state,frame,'target_x',low16(frame.target_x))
    elif entry==0xB982:
        stack=frame.stack_cursor.advance(-4)
        frame=_city_ui_store_fields(state,frame,stack.base,frame.candidates.base,4)
        frame=first_replace(frame,stack_cursor=stack,roster=state.table_at(0xFFFFEA88).cursor())
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF372,2),16)
        frame=_city_ui_shift_fields(state,frame,'target_x',1)
        frame=_city_ui_arithmetic_fields(state,frame,'target_x',state.read(0xFFFFF372,2))
        frame=first_replace(frame,candidates=state.table_at(0xB9DE).cursor())
        frame=_movement_move(state,frame,'unit',0,16)
        frame=_movement_move(state,frame,'target_y',0,16)
        frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
        frame=_movement_move(state,frame,'unit',frame.candidates.byte(low16(frame.target_y)),8)
        for displacement in (1,2):
            frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x),displacement),8)
            frame=_movement_compare(state,frame,low8(frame.unit),frame.candidates.byte(low16(frame.target_y)),8)
            if frame.status&1:
                frame=_movement_move(state,frame,'unit',frame.candidates.byte(low16(frame.target_y)),8)
        saved=frame.stack_cursor.long()
        frame=first_replace(frame,candidates=state.table_at(saved).cursor(),stack_cursor=frame.stack_cursor.advance(4))
        frame=first_replace(frame,roster=state.table_at(0xFFFFB400).cursor())
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF372,2),16)
        frame=_city_ui_shift_fields(state,frame,'target_x',1)
        frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
        frame=_city_ui_arithmetic_fields(state,frame,'target_x',low16(frame.unit))
        frame=_movement_move_long(state,frame,'target_x',low16(frame.target_x))
    frame=_movement_move(state,frame,'target_y',0xC270,16)
    frame=_movement_move(state,frame,'unit',0xC200,16)
    frame=first_replace(frame,auxiliary=state.table_at(0xFFFFD300))
    return _city_ui_child_fields(state,frame,0x1270A,0xB94A)


def append_officer_name_value_alternate_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """B938 is a real tail entry; its caller already supplies the actual D0 value."""
    return append_officer_name_value_fields(state,frame,0xB938)


def append_officer_name_value_alternate_2_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """B94C original BYTE attribute prefix, no extra alias call slot."""
    return append_officer_name_value_fields(state,frame,0xB94C)


def append_officer_name_value_alternate_3_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """B958 original weighted attribute prefix and common sole decimal tail."""
    return append_officer_name_value_fields(state,frame,0xB958)


def append_officer_name_value_alternate_4_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """B982 original three-quality maximum prefix, live A1 LONG save/readback."""
    return append_officer_name_value_fields(state,frame,0xB982)


def collect_force_relation_candidates_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """CFEE: collect eligible forces; both original branch paths rotate exactly once."""
    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
    from ..high_level_scene_flows.business_scene import _scene_fade_rotate_word_fields
    frame=_city_ui_frame_fields(state,frame,0xCFEE)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE710).cursor())
    frame=_city_ui_shift_fields(state,frame,'target_y',1)
    frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_y)),16)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFE730).cursor(),controller=state.table_at(0xFFFFE640))
    frame=_movement_move(state,frame,'unit',15,16)
    frame=_movement_move(state,frame,'count',0,16)
    while True:
        frame=_movement_compare(state,frame,low16(frame.count),low16(frame.target_x),16)
        selected_force=bool(frame.status&4)
        frame=_scene_fade_rotate_word_fields(SceneRefreshMemory(state),frame,'target_y',1)
        if not selected_force:
            if not frame.status&1:
                frame=_movement_test(state,frame,frame.controller.word(),16)
                if not frame.status&8:
                    frame=_city_ui_store_fields(state,frame,frame.candidates.base,low16(frame.count))
                    frame=first_replace(frame,candidates=frame.candidates.advance(2))
        frame=_city_ui_arithmetic_fields(state,frame,'count',1)
        frame=first_replace(frame,controller=frame.controller.advance(2))
        frame=first_replace(frame,unit=replace_word(frame.unit,u16(low16(frame.unit)-1)))
        if low16(frame.unit)==65535:
            break
    return _city_ui_store_fields(state,frame,frame.candidates.base,65535)


def divide_and_scale_command_value_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Compatibility name; CFEE is the same sole relation-list core, not a division rule."""
    return collect_force_relation_candidates_fields(state,frame)


def append_force_relation_commands_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C3CE: initialize the real relation rows and make all seven actual direct child calls."""
    frame=_city_ui_frame_fields(state,frame,0xC3CE)
    frame=first_replace(frame,roster=state.table_at(u32(0xFFFFD100+s16(state.read(0xFFFFF31A,2)))).cursor())
    frame=_movement_move(state,frame,'target_x',0,16)
    frame=_movement_move(state,frame,'target_y',9,16)
    frame=_movement_move_long(state,frame,'unit',0x6C422)
    while True:
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),frame.unit,4)
        frame=_city_ui_arithmetic_fields(state,frame,'target_x',16)
        frame=_city_ui_arithmetic_fields(state,frame,'unit',128)
        frame=first_replace(frame,target_y=replace_word(frame.target_y,u16(low16(frame.target_y)-1)))
        if low16(frame.target_y)==65535:
            break
    frame=first_replace(frame,roster=frame.roster.advance(4))
    frame=_city_ui_child_fields(state,frame,0xC420,0xC3F8)
    frame=_movement_move(state,frame,'choice',0xC005,16)
    for target,continuation in ((0xC438,0xC402),(0xC466,0xC406),(0xC438,0xC40A),
            (0xC466,0xC40E),(0xC438,0xC412),(0xC47E,0xC416)):
        frame=_city_ui_child_fields(state,frame,target,continuation)
    frame=_city_ui_store_fields(state,frame,frame.roster.base,0,2,True)
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,120)


def _city_ui_relation_border_fields(state: SceneState, frame: FirstDeploymentFrame,
        role: int) -> FirstDeploymentFrame:
    """The original heading/value/footer are three closed four-cell border roles."""
    if role not in (0,1,2):
        raise ValueError('closed original relation border role required')
    frame=_city_ui_append_fields(state,frame,(0xC380,0xC382,0xD380)[role])
    frame=_movement_move(state,frame,'target_x',3,16)
    while True:
        frame=_city_ui_append_fields(state,frame,(0xC381,0xC001,0xD381)[role])
        frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
        if low16(frame.target_x)==65535:
            break
    end=(0xCB80,0xCB82,0xDB80)[role]
    if role==2:
        return _city_ui_append_fields(state,frame,end)
    frame=_city_ui_store_fields(state,frame,frame.roster.base,end)
    return first_replace(frame,roster=frame.roster.advance(6))


def append_force_relation_heading_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C420: relation packet heading, with its original unadvanced final store."""
    return _city_ui_relation_border_fields(state,_city_ui_frame_fields(state,frame,0xC420),0)


def set_force_relation_markers_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C438: four paired relation label cells, eight actual D7 increments."""
    frame=_city_ui_frame_fields(state,frame,0xC438)
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+16),0xC382)
    frame=_city_ui_append_fields(state,frame,0xC382)
    frame=_movement_move(state,frame,'target_x',3,16)
    while True:
        frame=_city_ui_store_fields(state,frame,frame.roster.base,low16(frame.choice))
        frame=_city_ui_arithmetic_fields(state,frame,'choice',1)
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+16),low16(frame.choice))
        frame=_city_ui_arithmetic_fields(state,frame,'choice',1)
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
        if low16(frame.target_x)==65535:
            break
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+16),0xCB82)
    frame=_city_ui_store_fields(state,frame,frame.roster.base,0xCB82)
    return first_replace(frame,roster=frame.roster.advance(22))


def append_force_relation_value_row_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C466: original blank relation value border and actual six-byte advance."""
    return _city_ui_relation_border_fields(state,_city_ui_frame_fields(state,frame,0xC466),1)


def append_force_relation_footer_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C47E: original postincrement footer cell."""
    return _city_ui_relation_border_fields(state,_city_ui_frame_fields(state,frame,0xC47E),2)


def append_diplomacy_command_choices_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """DCF0: five original diplomacy selection roles and optional live cursor rows."""
    frame=_city_ui_frame_fields(state,frame,0xDCF0)
    frame=first_replace(frame,roster=state.table_at(u32(0xFFFFD100+s16(state.read(0xFFFFF31A,2)))).cursor())
    roles=((0xC51A,0xC022,0xFFFFAFF8,0,False,0xDD10),
        (0xC69A,0xC02E,0xFFFFAFF8,0,True,0xDD28),
        (0xC4AE,0xC03A,0xFFFFAFFA,0,False,0xDD40),
        (0xC62E,0xC046,0xFFFFAFFA,1,False,0xDD5A),
        (0xC7AE,0xC052,0xFFFFAFFA,2,False,0xDD74))
    for location,glyph,address,match,nonzero,continuation in roles:
        frame=_movement_move(state,frame,'target_x',location,16)
        frame=_movement_move(state,frame,'target_y',glyph,16)
        if match:
            frame=_movement_compare(state,frame,state.read(address,2),match,16)
        else:
            frame=_movement_test(state,frame,state.read(address,2),16)
        selected=not bool(frame.status&4) if nonzero else bool(frame.status&4)
        if selected:
            frame=_city_ui_arithmetic_fields(state,frame,'target_y',60)
        frame=_city_ui_child_fields(state,frame,0xDDEC,continuation)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,1),8)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&3,16)
    append_cursor=not bool(frame.status&4)
    if not append_cursor:
        frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF321,1),3)
        append_cursor=not bool(frame.status&4)
    if append_cursor:
        frame=_movement_move(state,frame,'target_x',0xC51A,16)
        frame=_movement_move(state,frame,'target_y',state.read(0xFFFFAFF8,2),16)
        frame=_movement_test(state,frame,state.read(0xFFFFAFFC,2),16)
        if not frame.status&4:
            frame=_movement_move(state,frame,'target_x',0xC4AE,16)
            frame=_movement_move(state,frame,'target_y',state.read(0xFFFFAFFA,2),16)
        frame=_movement_move(state,frame,'unit',low16(frame.target_y),16)
        frame=_city_ui_shift_fields(state,frame,'target_y',1)
        frame=_city_ui_arithmetic_fields(state,frame,'target_y',low16(frame.unit))
        frame=_city_ui_shift_fields(state,frame,'target_y',7)
        frame=_city_ui_arithmetic_fields(state,frame,'target_x',low16(frame.target_y))
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+16),6)
        frame=_city_ui_append_fields(state,frame,6)
        frame=_city_ui_store_fields(state,frame,frame.roster.base,low16(frame.target_x))
        frame=_city_ui_arithmetic_fields(state,frame,'target_x',128)
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+16),low16(frame.target_x))
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_movement_move(state,frame,'target_x',2,16)
        while True:
            frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+16),0xC001C001,4)
            frame=_city_ui_append_fields(state,frame,0xC001C001,4)
            frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
            if low16(frame.target_x)==65535:
                break
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,32)
        frame=first_replace(frame,roster=frame.roster.advance(16))
    frame=_city_ui_store_fields(state,frame,frame.roster.base,0,2,True)
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,80)


def set_diplomacy_command_marker_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """DDEC: six paired choice label cells and their actual D0/D1/D2 effects."""
    frame=_city_ui_frame_fields(state,frame,0xDDEC)
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+16),6)
    frame=_city_ui_append_fields(state,frame,6)
    frame=_city_ui_store_fields(state,frame,frame.roster.base,low16(frame.target_x))
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',128)
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+16),low16(frame.target_x))
    frame=first_replace(frame,roster=frame.roster.advance(2))
    frame=_movement_move(state,frame,'unit',5,16)
    while True:
        frame=_city_ui_store_fields(state,frame,frame.roster.base,low16(frame.target_y))
        frame=_city_ui_arithmetic_fields(state,frame,'target_y',1)
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+16),low16(frame.target_y))
        frame=_city_ui_arithmetic_fields(state,frame,'target_y',1)
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=first_replace(frame,unit=replace_word(frame.unit,u16(low16(frame.unit)-1)))
        if low16(frame.unit)==65535:
            break
    return first_replace(frame,roster=frame.roster.advance(16))


def _campaign_ui_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Use the one campaign call bridge; the caller owns its real LONG return slot."""
    from .business_main import _campaign_call_fields
    return _campaign_call_fields(state,frame,target,continuation)


def _campaign_ui_parallel_cell_fields(state: SceneState, frame: FirstDeploymentFrame,
        value: int, offsets: tuple, clear: bool=False) -> FirstDeploymentFrame:
    """The closed two-/three-row packet roles keep the original store order and postincrement."""
    if offsets not in ((30,60),(60,30),(30,),(22,)):
        raise ValueError('actual command packet parallel-row role required')
    for offset in offsets:
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+offset),value,2,clear)
    return _city_ui_append_fields(state,frame,value,2,clear)


def _campaign_ui_change_bit_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, bit: int, set_bit: bool) -> FirstDeploymentFrame:
    """Actual BYTE BSET/BCLR, including its prior read and only-Z CCR effect."""
    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
    from ..high_level_gameplay_flow.business_services import _scene_refresh_bit_clear
    if type(set_bit) is not bool:
        raise ValueError('actual command bit operation required')
    if set_bit:
        previous=state.read(address,1)
        frame=_city_ui_bit_fields(state,frame,previous,bit)
        state.write(address,1,previous | (1 << bit))
        return frame
    return _scene_refresh_bit_clear(SceneRefreshMemory(state),frame,address,bit)


def compose_command_selection_prompt_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """57E0: build the paired option label, then execute the live indexed option formatter."""
    frame=_city_ui_frame_fields(state,frame,0x57E0)
    frame=_campaign_ui_call_fields(state,frame,0x5A42,0x57E4)
    frame=_campaign_ui_parallel_cell_fields(state,frame,0xC382,(30,60))
    frame=_movement_move(state,frame,'choice',state.read(0xFFFFF36A,2),16)
    frame=_city_ui_arithmetic_fields(state,frame,'choice',state.read(0xFFFFF368,2))
    frame=_city_ui_shift_fields(state,frame,'choice',2)
    frame=first_replace(frame,candidates=state.table_at(0x8A2B6).cursor())
    frame=_movement_move(state,frame,'count',frame.candidates.word(low16(frame.choice)),16)
    frame=_campaign_ui_call_fields(state,frame,0x5A2A,0x580C)
    frame=_movement_move(state,frame,'count',frame.candidates.word(low16(frame.choice),2),16)
    frame=_campaign_ui_call_fields(state,frame,0x5A2A,0x5814)
    frame=_movement_fixed_shift_word(state,frame,'choice',1,True)
    frame=_movement_move(state,frame,'choice',state.table_at(0x584A).word(low16(frame.choice)),16)
    target=u32(0x5864+s16(low16(frame.choice)))
    frame=_campaign_ui_call_fields(state,frame,target,0x581E)
    frame=_campaign_ui_parallel_cell_fields(state,frame,0xCB82,(30,60))
    frame=_movement_move(state,frame,'unit',0,16)
    frame=_movement_move(state,frame,'count',10,16)
    while True:
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.unit))+36),0xC001)
        frame=_city_ui_arithmetic_fields(state,frame,'unit',2)
        frame=first_replace(frame,count=replace_word(frame.count,u16(low16(frame.count)-1)))
        if low16(frame.count)==65535:
            break
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+60),0,2,True)
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,1)


def set_command_selection_cursor_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5868: prepend the cursor cell and render three successive four-cell values."""
    frame=_city_ui_frame_fields(state,frame,0x5868)
    frame=_campaign_ui_parallel_cell_fields(state,frame,0xC001,(30,))
    frame=_campaign_ui_call_fields(state,frame,0x5A2A,0x5876)
    frame=_city_ui_arithmetic_fields(state,frame,'count',1)
    frame=_campaign_ui_call_fields(state,frame,0x5A2A,0x587C)
    frame=_city_ui_arithmetic_fields(state,frame,'count',1)
    return _campaign_ui_call_fields(state,frame,0x5A2A,0x5882)


def store_command_selection_value_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5A2A: one four-glyph value across two actual RAM rows; D3 advances three times."""
    frame=_city_ui_frame_fields(state,frame,0x5A2A)
    for offset in (0,30,2,32):
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+offset),low16(frame.count))
        if offset!=32:
            frame=_city_ui_arithmetic_fields(state,frame,'count',1)
    return first_replace(frame,roster=frame.roster.advance(4))


def append_command_selection_heading_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5A42: select the real packet cursor and write the three-row option heading."""
    frame=_city_ui_frame_fields(state,frame,0x5A42)
    frame=first_replace(frame,roster=state.table_at(u32(0xFFFFD100+s16(state.read(0xFFFFF31A,2)))).cursor())
    frame=_campaign_ui_parallel_cell_fields(state,frame,13,(60,30))
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF36A,2),16)
    frame=_movement_move(state,frame,'count',low16(frame.unit),16)
    frame=_city_ui_shift_fields(state,frame,'unit',1)
    frame=_city_ui_arithmetic_fields(state,frame,'unit',low16(frame.count))
    frame=_city_ui_shift_fields(state,frame,'unit',7)
    frame=_city_ui_arithmetic_fields(state,frame,'unit',0xC1B4)
    for offset in (0,30,60):
        if offset:
            frame=_city_ui_arithmetic_fields(state,frame,'unit',128)
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+offset),low16(frame.unit))
    return first_replace(frame,roster=frame.roster.advance(2))


def append_command_confirmation_row_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5A80: append the actual option confirmation row and its terminating clear."""
    frame=_city_ui_frame_fields(state,frame,0x5A80)
    frame=first_replace(frame,roster=state.table_at(u32(0xFFFFD100+s16(state.read(0xFFFFF31A,2)))).cursor())
    frame=_city_ui_append_fields(state,frame,13)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF36A,2),16)
    frame=_movement_move(state,frame,'count',low16(frame.unit),16)
    frame=_city_ui_shift_fields(state,frame,'unit',1)
    frame=_city_ui_arithmetic_fields(state,frame,'unit',low16(frame.count))
    frame=_city_ui_shift_fields(state,frame,'unit',7)
    frame=_city_ui_arithmetic_fields(state,frame,'unit',0xC1B4)
    frame=_city_ui_append_fields(state,frame,low16(frame.unit))
    frame=_city_ui_append_fields(state,frame,0xD380)
    frame=_movement_move(state,frame,'target_x',10,16)
    while True:
        frame=_city_ui_append_fields(state,frame,0xD381)
        frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
        if low16(frame.target_x)==65535:
            break
    frame=_city_ui_append_fields(state,frame,0xDB80)
    frame=_city_ui_store_fields(state,frame,frame.roster.base,0,2,True)
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,30)


def present_current_command_prompt_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5ABC: the live mode table chooses its real prompt handler; no default success is fabricated."""
    frame=_city_ui_frame_fields(state,frame,0x5ABC)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),129,16)
    if frame.status&4:
        return frame
    frame=_movement_move_long(state,frame,'target_x',0xC000000B)
    frame=_movement_move(state,frame,'target_y',4,16)
    frame=_movement_move(state,frame,'choice',state.read(0xFFFFF36C,2),16)
    frame=_city_ui_shift_fields(state,frame,'choice',1)
    frame=_movement_move(state,frame,'choice',state.table_at(0x5AE6).word(low16(frame.choice)),16)
    frame=_campaign_ui_call_fields(state,frame,u32(0x5AEE+s16(low16(frame.choice))),0x5ADE)
    return _campaign_ui_change_bit_fields(state,frame,0xFFFFF3A4,3,True)


def present_command_warning_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5C98: submit the original counted warning packet and then clear its pending bit."""
    frame=_city_ui_frame_fields(state,frame,0x5C98)
    frame=_movement_move_long(state,frame,'target_x',0xC000000B)
    frame=_movement_move(state,frame,'target_y',4,16)
    frame=_movement_move(state,frame,'unit',0xC084,16)
    frame=first_replace(frame,roster=state.table_at(0x5CB8).cursor())
    frame=_campaign_ui_call_fields(state,frame,0x26BFA,0x5CB0)
    return _campaign_ui_change_bit_fields(state,frame,0xFFFFF3A4,3,False)


def append_contextual_cursor_commands_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A370: gate settlement updates, or merge the original two input latches by force ownership."""
    frame=_city_ui_frame_fields(state,frame,0xA370)
    frame=_movement_compare(state,frame,state.read(0xFFFFF612,2),0x209,16)
    if frame.status&4:
        frame=_movement_compare(state,frame,state.read(0xFFFFF362,2),15,16)
        if frame.status&4:
            return frame
    frame=_movement_compare(state,frame,state.read(0xFFFFF612,2),0x207,16)
    if frame.status&4:
        frame=_movement_test(state,frame,state.read(0xFFFFEFE0,2),16)
        if not frame.status&4:
            return _campaign_ui_call_fields(state,frame,0x1A16E,0xA39C)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
    for address in (0xFFFFF67C,0xFFFFF67E):
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(address,2),16)
        if frame.status&4:
            return _city_ui_store_fields(state,frame,0xFFFFF602,state.read(0xFFFFF604,2))
    frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF67A,2),16)
    if frame.status&4:
        return frame
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF604,2),16)
    frame=_city_ui_store_fields(state,frame,0xFFFFF602,state.read(0xFFFFF602,2)|low16(frame.target_x))
    return _city_ui_store_fields(state,frame,0xFFFFF604,state.read(0xFFFFF602,2))


def _campaign_ui_force_prompt_fields(state: SceneState, frame: FirstDeploymentFrame,
        second: bool) -> FirstDeploymentFrame:
    """Two original force prompt roles differ only in their real counted packet source and return."""
    if type(second) is not bool:
        raise ValueError('original first/second force prompt role required')
    frame=_city_ui_frame_fields(state,frame,0xA506 if second else 0xA4CC)
    frame=_movement_move_long(state,frame,'target_x',0xC000000A)
    frame=_movement_move(state,frame,'target_y',4,16)
    frame=_movement_move(state,frame,'unit',0xC09C,16)
    frame=first_replace(frame,roster=state.table_at(0xA520 if second else 0xA4E6).cursor())
    return _campaign_ui_call_fields(state,frame,0x26BFA,0xA51E if second else 0xA4E4)


def draw_first_force_prompt_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _campaign_ui_force_prompt_fields(state,frame,False)


def draw_second_force_prompt_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _campaign_ui_force_prompt_fields(state,frame,True)


def append_world_cursor_coordinates_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """AB40: choose the original cursor y-position and derive its x-coordinate before the real sprite call."""
    frame=_city_ui_frame_fields(state,frame,0xAB40)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF321,1),3)
    if not frame.status&4:
        return frame
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF35C,2),16)
    frame=_movement_move(state,frame,'unit',low16(frame.unit)&7,16)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_y',124,16)
    else:
        frame=_movement_move(state,frame,'target_y',24,16)
        frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF35D,1),3)
        if not frame.status&4:
            frame=_movement_move(state,frame,'target_y',160,16)
    frame=_city_ui_shift_fields(state,frame,'unit',3)
    frame=_movement_move(state,frame,'target_x',low16(frame.unit),16)
    frame=_city_ui_shift_fields(state,frame,'unit',1)
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',low16(frame.unit))
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',16)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=first_replace(frame,roster=state.table_at(0xAB82).cursor())
    return _campaign_ui_call_fields(state,frame,0xAC08,0xAB80)


def set_roster_selection_notice_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C11E: publish the actual BYTE selection as a WORD command and clear two LONG notices."""
    frame=_city_ui_frame_fields(state,frame,0xC11E)
    frame=_movement_move(state,frame,'target_x',0,16)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF578,1),8)
    frame=_city_ui_store_fields(state,frame,0xFFFFF38C,low16(frame.target_x))
    frame=_city_ui_store_fields(state,frame,0xFFFFF576,1)
    frame=_city_ui_store_fields(state,frame,0xFFFFF39E,0,4,True)
    return _city_ui_store_fields(state,frame,0xFFFFF3BA,0,4,True)


def compose_title_option_panel_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A924: render two real title-option rows, or their original out-of-range blank panel."""
    frame=_city_ui_frame_fields(state,frame,0xA924)
    frame=first_replace(frame,roster=state.table_at(0xFFFFD100).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF31A,2),16)
    frame=first_replace(frame,roster=frame.roster.advance(s16(low16(frame.target_x))))
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF35A,2),16)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame=_city_ui_shift_fields(state,frame,'target_y',1)
    frame=_city_ui_arithmetic_fields(state,frame,'target_y',low16(frame.target_x))
    frame=_city_ui_shift_fields(state,frame,'target_y',7)
    frame=_city_ui_arithmetic_fields(state,frame,'target_y',0xC286)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF358,2),16)
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',state.read(0xFFFFF35A,2))
    frame=_movement_compare(state,frame,low16(frame.target_x),34,16)
    if not frame.status&1 and not frame.status&4:
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+22),16)
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+80),16)
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+58),9)
        frame=_city_ui_append_fields(state,frame,9)
        for offset,increment in ((22,128),(58,34),(80,162)):
            frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+offset),low16(frame.target_y))
            frame=_city_ui_memory_arithmetic_fields(state,frame,u32(frame.roster.base+offset),increment)
        frame=_city_ui_append_fields(state,frame,low16(frame.target_y))
        frame=_movement_move(state,frame,'unit',15,16)
        while True:
            frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+22),0x483)
            frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+80),0x483)
            frame=_movement_compare(state,frame,low16(frame.unit),6,16)
            if not frame.status&1 and not frame.status&4:
                frame=_city_ui_store_fields(state,frame,frame.roster.base,0x483)
                frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+58),0x483)
            frame=first_replace(frame,roster=frame.roster.advance(2),unit=replace_word(frame.unit,u16(low16(frame.unit)-1)))
            if low16(frame.unit)==65535:
                break
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+80),0,2,True)
    else:
        frame=_campaign_ui_call_fields(state,frame,0xA9DA,0xA952)
        frame=_city_ui_arithmetic_fields(state,frame,'target_y',34)
        frame=_movement_move(state,frame,'unit',7,16)
        frame=_movement_compare(state,frame,low16(frame.target_x),29,16)
        if not frame.status&1:
            frame=_movement_move(state,frame,'unit',6,16)
        frame=_city_ui_arithmetic_fields(state,frame,'target_x',low16(frame.unit))
        frame=_campaign_ui_call_fields(state,frame,0xA9DA,0xA96A)
    frame=_city_ui_store_fields(state,frame,frame.roster.base,0,2,True)
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,72)
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF35A,1)


def append_title_option_glyphs_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A9DA: title border, numeric option, marker and decoration are actual three child calls."""
    frame=_city_ui_frame_fields(state,frame,0xA9DA)
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+22),16)
    frame=_city_ui_append_fields(state,frame,9)
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+22),low16(frame.target_y))
    frame=_city_ui_memory_arithmetic_fields(state,frame,u32(frame.roster.base+22),128)
    frame=_city_ui_append_fields(state,frame,low16(frame.target_y))
    for target,continuation in ((0xA9FE,0xA9F4),(0xAA4C,0xA9F8),(0xAA74,0xA9FC)):
        frame=_campaign_ui_call_fields(state,frame,target,continuation)
    return frame


def append_title_option_digit_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A9FE: original repeated-subtraction tens conversion and paired decimal glyphs."""
    frame=_city_ui_frame_fields(state,frame,0xA9FE)
    frame=_movement_move(state,frame,'distance',low16(frame.target_x),16)
    frame=_movement_compare(state,frame,low16(frame.target_x),10,16)
    if frame.status&1:
        frame=_movement_move(state,frame,'unit',0x228,16)
    else:
        frame=_movement_move(state,frame,'unit',0,16)
        while True:
            frame=_city_ui_arithmetic_fields(state,frame,'distance',10,True)
            if frame.status&1:
                break
            frame=_city_ui_arithmetic_fields(state,frame,'unit',1)
        frame=_city_ui_arithmetic_fields(state,frame,'distance',10)
        frame=_city_ui_shift_fields(state,frame,'unit',2)
        frame=_city_ui_arithmetic_fields(state,frame,'unit',0x40A)
    frame=_campaign_ui_call_fields(state,frame,0xAA34,0xAA26)
    frame=_movement_move(state,frame,'unit',low16(frame.distance),16)
    frame=_city_ui_shift_fields(state,frame,'unit',2)
    frame=_city_ui_arithmetic_fields(state,frame,'unit',0x40A)
    return _campaign_ui_call_fields(state,frame,0xAA34,0xAA32)


def store_title_option_digit_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """AA34: four glyphs across two rows, preserving the final ADDQ flags."""
    frame=_city_ui_frame_fields(state,frame,0xAA34)
    for _column in (0,1):
        frame=_city_ui_store_fields(state,frame,frame.roster.base,low16(frame.unit))
        frame=_city_ui_arithmetic_fields(state,frame,'unit',1)
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+22),low16(frame.unit))
        frame=first_replace(frame,roster=frame.roster.advance(2))
        if _column==0:
            frame=_city_ui_arithmetic_fields(state,frame,'unit',1)
    return frame


def set_title_option_marker_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """AA4C: option number selects the original eight-glyph marker strip."""
    frame=_city_ui_frame_fields(state,frame,0xAA4C)
    frame=_campaign_ui_parallel_cell_fields(state,frame,0x483,(22,))
    frame=_movement_move(state,frame,'unit',low16(frame.target_x),16)
    frame=_city_ui_shift_fields(state,frame,'unit',3)
    frame=_city_ui_arithmetic_fields(state,frame,'unit',0x2B8)
    frame=_movement_move(state,frame,'count',3,16)
    while True:
        frame=_city_ui_store_fields(state,frame,frame.roster.base,low16(frame.unit))
        frame=_city_ui_arithmetic_fields(state,frame,'unit',1)
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+22),low16(frame.unit))
        frame=_city_ui_arithmetic_fields(state,frame,'unit',1)
        frame=first_replace(frame,roster=frame.roster.advance(2),count=replace_word(frame.count,u16(low16(frame.count)-1)))
        if low16(frame.count)==65535:
            break
    return frame


def append_title_option_decorations_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """AA74: preserve nine real LONGs around the original owner-dependent live decoration handler."""
    from .business_movement_support import _movement_save_longs, _movement_restore_longs
    frame=_city_ui_frame_fields(state,frame,0xAA74)
    saved=('target_x','target_y','unit','count','distance','offset_x','offset_y','candidates','auxiliary')
    frame=_movement_save_longs(state,frame,saved)
    frame=_movement_move(state,frame,'unit',22,16)
    frame=first_replace(frame,roster=frame.roster.advance(s16(low16(frame.unit))))
    frame=_city_ui_append_fields(state,frame,0x483)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFF427).cursor())
    frame=_movement_move(state,frame,'unit',frame.candidates.byte(low16(frame.target_x)),8)
    frame=_movement_compare(state,frame,low8(frame.unit),state.read(0xFFFFF377,1),8)
    if not frame.status&4:
        frame=_campaign_ui_call_fields(state,frame,0xAB10,0xAA96)
    else:
        frame=_movement_move(state,frame,'unit',state.read(0xFFFFF350,2),16)
        frame=_city_ui_shift_fields(state,frame,'unit',1)
        frame=_movement_move(state,frame,'unit',state.table_at(0xAAAC).word(low16(frame.unit)),16)
        frame=_campaign_ui_call_fields(state,frame,u32(0xAAB4+s16(low16(frame.unit))),0xAAA6)
    return _movement_restore_longs(state,frame,saved)


def append_title_option_decoration_value_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """AB10: append the original four neutral and two decoration glyphs."""
    frame=_city_ui_frame_fields(state,frame,0xAB10)
    for counter,tile in ((3,0xC228),(1,0x488)):
        frame=_movement_move(state,frame,'unit',counter,16)
        while True:
            frame=_city_ui_append_fields(state,frame,tile)
            frame=first_replace(frame,unit=replace_word(frame.unit,u16(low16(frame.unit)-1)))
            if low16(frame.unit)==65535:
                break
    return frame


def append_force_relation_label_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C56E: place the original relation label according to the live two-choice selector."""
    frame=_city_ui_frame_fields(state,frame,0xC56E)
    frame=first_replace(frame,roster=state.table_at(0xC19A).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF386,2),16)
    frame=_city_ui_shift_fields(state,frame,'target_x',1)
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',state.read(0xFFFFF386,2))
    frame=_city_ui_shift_fields(state,frame,'target_x',3)
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',64)
    frame=_movement_move(state,frame,'target_y',136,16)
    frame=_movement_move(state,frame,'unit',0,16)
    return _campaign_ui_call_fields(state,frame,0xAC08,0xC58E)


def append_force_relation_digits_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C590: ten actual relation rows, each containing ten CLR-prior-read cells."""
    frame=_city_ui_frame_fields(state,frame,0xC590)
    frame=first_replace(frame,roster=state.table_at(u32(0xFFFFD100+s16(state.read(0xFFFFF31A,2)))).cursor())
    frame=_movement_move(state,frame,'target_x',9,16)
    frame=_movement_move(state,frame,'target_y',0xC41E,16)
    while True:
        frame=_city_ui_append_fields(state,frame,10)
        frame=_city_ui_append_fields(state,frame,low16(frame.target_y))
        frame=_city_ui_arithmetic_fields(state,frame,'target_y',128)
        frame=_movement_move(state,frame,'unit',9,16)
        while True:
            frame=_city_ui_append_fields(state,frame,0,2,True)
            frame=first_replace(frame,unit=replace_word(frame.unit,u16(low16(frame.unit)-1)))
            if low16(frame.unit)==65535:
                break
        frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
        if low16(frame.target_x)==65535:
            break
    frame=_city_ui_store_fields(state,frame,frame.roster.base,0,2,True)
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,240)


def adjust_force_relation_selection_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C764: the original repeat delay toggles a WORD selector only on expiry."""
    frame=_city_ui_frame_fields(state,frame,0xC764)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF602,1),1)
    if frame.status&4:
        frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF602,1),0)
        if frame.status&4:
            return _city_ui_store_fields(state,frame,0xFFFFF608,1)
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF608,1,True)
    if not frame.status&4:
        return frame
    frame=_city_ui_store_fields(state,frame,0xFFFFF608,12)
    return _city_ui_store_fields(state,frame,0xFFFFF386,state.read(0xFFFFF386,2)^1)


def confirm_force_relation_selection_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C790: render the current relation cursor only for the original input/animation gate."""
    frame=_city_ui_frame_fields(state,frame,0xC790)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if not frame.status&4:
        return frame
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,1),8)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&3,16)
    if frame.status&4:
        frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF321,1),3)
        if not frame.status&4:
            return frame
    frame=first_replace(frame,roster=state.table_at(0xC7D0).cursor())
    frame=_movement_move(state,frame,'target_x',64,16)
    frame=_movement_test(state,frame,state.read(0xFFFFF386,2),16)
    if not frame.status&4:
        frame=_movement_move(state,frame,'target_x',88,16)
    frame=_movement_move(state,frame,'target_y',136,16)
    frame=_movement_move(state,frame,'unit',0,16)
    return _campaign_ui_call_fields(state,frame,0xAC08,0xC7CE)


def _campaign_ui_city_record_pair_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """The selected-city two-row record tail has one algorithm and its two real value-call slots."""
    frame=_campaign_ui_parallel_cell_fields(state,frame,13,(30,))
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+30),low16(frame.unit))
    frame=_city_ui_arithmetic_fields(state,frame,'unit',128,True)
    frame=_city_ui_append_fields(state,frame,low16(frame.unit))
    frame=_city_ui_arithmetic_fields(state,frame,'unit',256)
    frame=_campaign_ui_parallel_cell_fields(state,frame,0xC382,(30,))
    frame=_movement_move(state,frame,'distance',low16(frame.target_y),16)
    frame=_movement_move(state,frame,'offset_x',3,16)
    frame=_campaign_ui_call_fields(state,frame,0xD89C,0xD7F6)
    frame=_campaign_ui_parallel_cell_fields(state,frame,0xC001,(30,))
    frame=_movement_move(state,frame,'distance',low16(frame.offset_y),16)
    frame=_movement_move(state,frame,'offset_x',5,16)
    frame=_campaign_ui_call_fields(state,frame,0xD89C,0xD80A)
    frame=_campaign_ui_parallel_cell_fields(state,frame,0xCB82,(30,))
    return first_replace(frame,roster=frame.roster.advance(30))


def append_selected_city_command_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D74A: build the owned city's three-record command panel, preserving empty-record skip and padding."""
    frame=_city_ui_frame_fields(state,frame,0xD74A)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF427).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
    frame=_movement_compare(state,frame,low16(frame.target_y),state.read(0xFFFFF376,2),16)
    if not frame.status&4:
        return frame
    frame=_city_ui_shift_fields(state,frame,'target_x',1)
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',state.read(0xFFFFF364,2))
    frame=_city_ui_shift_fields(state,frame,'target_x',2)
    frame=first_replace(frame,roster=state.table_at(u32(0xFFFFD100+s16(state.read(0xFFFFF31A,2)))).cursor())
    frame=_movement_move(state,frame,'unit',0xC704,16)
    frame=_movement_test(state,frame,state.read(0xFFFFF36C,2),16)
    if not frame.status&4:
        frame=_movement_move(state,frame,'unit',0xC404,16)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFE80C).cursor())
    frame=_movement_move(state,frame,'target_y',frame.candidates.word(low16(frame.target_x)),16)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_y)&frame.candidates.word(low16(frame.target_x),4),16)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_y)&frame.candidates.word(low16(frame.target_x),8),16)
    if not frame.status&8:
        frame=_city_ui_append_fields(state,frame,13)
        frame=_city_ui_append_fields(state,frame,low16(frame.unit))
        frame=_city_ui_arithmetic_fields(state,frame,'unit',256)
        frame=_city_ui_append_fields(state,frame,0xC380)
        frame=_movement_move(state,frame,'target_y',10,16)
        while True:
            frame=_city_ui_append_fields(state,frame,0xC381)
            frame=first_replace(frame,target_y=replace_word(frame.target_y,u16(low16(frame.target_y)-1)))
            if low16(frame.target_y)==65535:
                break
        frame=_city_ui_append_fields(state,frame,0xCB80)
        frame=_movement_move(state,frame,'target_y',0xC6E8,16)
        frame=_movement_move(state,frame,'offset_y',0xC340,16)
        while True:
            frame=_movement_move(state,frame,'count',frame.candidates.word(low16(frame.target_x)),16)
            if not frame.status&8:
                break
            frame=_city_ui_arithmetic_fields(state,frame,'target_x',4)
            frame=_city_ui_arithmetic_fields(state,frame,'target_y',8)
            frame=_city_ui_arithmetic_fields(state,frame,'offset_y',12)
        frame=_campaign_ui_city_record_pair_fields(state,frame)
        while True:
            frame=_city_ui_arithmetic_fields(state,frame,'offset_y',12)
            frame=_city_ui_arithmetic_fields(state,frame,'target_y',8)
            frame=_movement_compare(state,frame,low16(frame.target_y),0xC700,16)
            if not frame.status&1:
                break
            frame=_city_ui_arithmetic_fields(state,frame,'target_x',4)
            frame=_movement_move(state,frame,'count',frame.candidates.word(low16(frame.target_x)),16)
            if frame.status&8:
                continue
            frame=_city_ui_append_fields(state,frame,13)
            frame=_city_ui_append_fields(state,frame,low16(frame.unit))
            frame=_city_ui_arithmetic_fields(state,frame,'unit',256)
            frame=_city_ui_append_fields(state,frame,0xC382)
            frame=_movement_move(state,frame,'distance',10,16)
            while True:
                frame=_city_ui_append_fields(state,frame,0xC001)
                frame=first_replace(frame,distance=replace_word(frame.distance,u16(low16(frame.distance)-1)))
                if low16(frame.distance)==65535:
                    break
            frame=_city_ui_append_fields(state,frame,0xCB82)
            frame=_campaign_ui_city_record_pair_fields(state,frame)
        frame=_city_ui_append_fields(state,frame,13)
        frame=_city_ui_append_fields(state,frame,low16(frame.unit))
        frame=_city_ui_arithmetic_fields(state,frame,'unit',128)
        frame=_city_ui_append_fields(state,frame,0xD380)
        frame=_movement_move(state,frame,'target_x',10,16)
        while True:
            frame=_city_ui_append_fields(state,frame,0xD381)
            frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
            if low16(frame.target_x)==65535:
                break
        frame=_city_ui_append_fields(state,frame,0xDB80)
        frame=_campaign_ui_change_bit_fields(state,frame,0xFFFFF3A5,3,True)
    while True:
        frame=_movement_compare(state,frame,low16(frame.unit),0xC904,16)
        if not frame.status&1 and not frame.status&4:
            break
        frame=_city_ui_append_fields(state,frame,13)
        frame=_city_ui_append_fields(state,frame,low16(frame.unit))
        frame=_city_ui_arithmetic_fields(state,frame,'unit',128)
        frame=_movement_move(state,frame,'target_x',12,16)
        while True:
            frame=_city_ui_append_fields(state,frame,0,2,True)
            frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
            if low16(frame.target_x)==65535:
                break
    frame=_city_ui_store_fields(state,frame,frame.roster.base,0,2,True)
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,300)


def store_selected_city_command_value_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D89C: the actual D5 DBRA emits successive paired glyphs, retaining D4's high WORD."""
    frame=_city_ui_frame_fields(state,frame,0xD89C)
    while True:
        frame=_city_ui_store_fields(state,frame,frame.roster.base,low16(frame.distance))
        frame=_city_ui_arithmetic_fields(state,frame,'distance',1)
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+30),low16(frame.distance))
        frame=_city_ui_arithmetic_fields(state,frame,'distance',1)
        frame=first_replace(frame,roster=frame.roster.advance(2),offset_x=replace_word(frame.offset_x,u16(low16(frame.offset_x)-1)))
        if low16(frame.offset_x)==65535:
            break
    return frame


def append_city_command_heading_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D8AE: eight six-glyph title rows and the original description-enable bit."""
    frame=_city_ui_frame_fields(state,frame,0xD8AE)
    frame=first_replace(frame,roster=state.table_at(u32(0xFFFFD100+s16(state.read(0xFFFFF31A,2)))).cursor())
    frame=_movement_move(state,frame,'target_x',0xC3A0,16)
    frame=_movement_move(state,frame,'target_y',0x8005,16)
    frame=_movement_move(state,frame,'unit',7,16)
    while True:
        frame=_city_ui_append_fields(state,frame,6)
        frame=_city_ui_append_fields(state,frame,low16(frame.target_x))
        frame=_city_ui_arithmetic_fields(state,frame,'target_x',128)
        frame=_movement_move(state,frame,'count',5,16)
        while True:
            frame=_city_ui_append_fields(state,frame,low16(frame.target_y))
            frame=_city_ui_arithmetic_fields(state,frame,'target_y',1)
            frame=first_replace(frame,count=replace_word(frame.count,u16(low16(frame.count)-1)))
            if low16(frame.count)==65535:
                break
        frame=first_replace(frame,unit=replace_word(frame.unit,u16(low16(frame.unit)-1)))
        if low16(frame.unit)==65535:
            break
    frame=_city_ui_store_fields(state,frame,frame.roster.base,0,2,True)
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,128)
    return _campaign_ui_change_bit_fields(state,frame,0xFFFFF3A5,2,True)


def append_current_command_description_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D8EC: original description gate, its two status children, live source choice and actual sprite submission."""
    frame=_city_ui_frame_fields(state,frame,0xD8EC)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF3A5,1),2)
    if frame.status&4:
        return frame
    frame=_campaign_ui_call_fields(state,frame,0xDA2C,0xD8F8)
    frame=_campaign_ui_call_fields(state,frame,0xDA8E,0xD8FC)
    frame=first_replace(frame,roster=state.table_at(0xD978).cursor())
    frame=_movement_move(state,frame,'target_x',56,16)
    frame=_movement_move(state,frame,'target_y',128,16)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=_city_ui_store_fields(state,frame,0xFFFFF60A,0,2,True)
    frame=_city_ui_store_fields(state,frame,0xFFFFF60E,0,2,True)
    frame=_campaign_ui_call_fields(state,frame,0xD920,0xD918)
    return _campaign_ui_call_fields(state,frame,0xAC08,0xD91E)


def choose_command_description_source_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D920: two real phase roles choose a WORD offset from the live description table."""
    frame=_city_ui_frame_fields(state,frame,0xD920)
    table_base=0xDA1C
    frame=_movement_compare(state,frame,state.read(0xFFFFF362,2),7,16)
    if frame.status&4:
        table_base=0xDA1A
        frame=_movement_move(state,frame,'count',state.read(0xFFFFF36A,2),16)
        frame=_movement_compare(state,frame,low16(frame.count),6,16)
        if not frame.status&1 and not frame.status&4:
            return frame
        frame=_city_ui_arithmetic_fields(state,frame,'count',2,True)
        if frame.status&8:
            frame=_movement_move(state,frame,'count',0,16)
        frame=_city_ui_shift_fields(state,frame,'count',2)
    else:
        frame=_movement_compare(state,frame,state.read(0xFFFFF362,2),3,16)
        if not frame.status&4:
            return frame
        frame=_movement_compare(state,frame,state.read(0xFFFFF36A,2),3,16)
        if frame.status&1 or frame.status&4:
            return frame
        frame=_movement_move(state,frame,'count',10,16)
        frame=_city_ui_arithmetic_fields(state,frame,'count',state.read(0xFFFFF36A,2),True)
        if frame.status&8:
            frame=_movement_move(state,frame,'count',0,16)
        frame=_city_ui_shift_fields(state,frame,'count',1)
    frame=first_replace(frame,candidates=state.table_at(table_base).cursor())
    frame=_movement_move(state,frame,'count',frame.candidates.word(low16(frame.count)),16)
    return first_replace(frame,roster=frame.roster.advance(s16(low16(frame.count))))


def append_command_description_rows_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """DA2C: preserve the phase/progress gates and draw the actual alignment-sensitive status sprite."""
    frame=_city_ui_frame_fields(state,frame,0xDA2C)
    frame=_movement_compare(state,frame,state.read(0xFFFFF362,2),3,16)
    if frame.status&4:
        frame=_movement_compare(state,frame,state.read(0xFFFFF36A,2),7,16)
        if not frame.status&1:
            return frame
    else:
        frame=_movement_compare(state,frame,state.read(0xFFFFF362,2),7,16)
        if frame.status&4:
            frame=_movement_compare(state,frame,state.read(0xFFFFF36A,2),4,16)
            if frame.status&1 or frame.status&4:
                return frame
    frame=first_replace(frame,roster=state.table_at(0xDA7E).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF320,2),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&248,16)
    if frame.status&4:
        frame=first_replace(frame,roster=frame.roster.advance(8))
    frame=_movement_move(state,frame,'target_x',80,16)
    frame=_movement_move(state,frame,'target_y',136,16)
    frame=_movement_move(state,frame,'unit',0,16)
    return _campaign_ui_call_fields(state,frame,0xAC08,0xDA7C)


def append_command_description_status_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """DA8E: original blinking status and live packet feedback, without a fabricated device acknowledgement."""
    frame=_city_ui_frame_fields(state,frame,0xDA8E)
    frame=_movement_compare(state,frame,state.read(0xFFFFF362,2),3,16)
    if frame.status&4:
        frame=_movement_compare(state,frame,state.read(0xFFFFF36A,2),5,16)
        if not frame.status&1:
            return frame
    else:
        frame=_movement_compare(state,frame,state.read(0xFFFFF362,2),7,16)
        if frame.status&4:
            frame=_movement_compare(state,frame,state.read(0xFFFFF36A,2),5,16)
            if frame.status&1 or frame.status&4:
                return frame
    frame=first_replace(frame,roster=state.table_at(0xDB10).cursor())
    frame=_movement_test(state,frame,state.read(0xFFFFF778,2),16)
    if not frame.status&4:
        frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF321,1),3)
        if not frame.status&4:
            frame=first_replace(frame,roster=frame.roster.advance(8))
    frame=_movement_move(state,frame,'target_x',96,16)
    frame=_movement_move(state,frame,'target_y',144,16)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=_campaign_ui_call_fields(state,frame,0xAC08,0xDAE4)
    frame=_movement_test(state,frame,state.read(0xFFFFF778,2),16)
    if not frame.status&4:
        frame=_movement_compare(state,frame,state.read(0xFFFFF77C,2),0x403A,16)
        if frame.status&4:
            frame=_city_ui_store_fields(state,frame,0xFFFFF778,0,2,True)
    else:
        frame=_movement_compare(state,frame,state.read(0xFFFFF77C,2),0x4039,16)
        if frame.status&4:
            frame=_city_ui_store_fields(state,frame,0xFFFFF778,1)
    return frame

from .business_movement_support import _movement_save_longs, _movement_restore_longs


def _command_panel_pointer_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, address: int) -> FirstDeploymentFrame:
    """MOVEA/LEA retains CCR; cursor carriers keep their real live address type."""
    address=u32(address)
    if name in ('roster','candidates','scan'):
        return first_replace(frame,**{name:state.table_at(address).cursor()})
    if name in ('controller','opponent','scratch','auxiliary'):
        return first_replace(frame,**{name:state.table_at(address)})
    raise ValueError('closed command panel address carrier required')


def _command_panel_dbra_fields(frame: FirstDeploymentFrame, name: str) -> tuple[FirstDeploymentFrame, bool]:
    """An original counted row consumes the current WORD and preserves all CCR bits."""
    if name not in ('target_x','target_y','unit','count','distance','offset_x','offset_y','choice'):
        raise ValueError('actual command panel DBRA register required')
    remaining=u16(low16(frame.carrier(name))-1)
    return first_replace(frame,**{name:replace_word(frame.carrier(name),remaining)}),remaining!=65535


def _command_panel_upload_fields(state: SceneState, frame: FirstDeploymentFrame,
        source: str, counter: str, destination: int, width: int=4) -> FirstDeploymentFrame:
    """Submit live packet cells in source-postincrement order to the real supplied port.

    No device is acknowledged here. SceneState rejects an unobserved hardware
    write at the actual transfer; the remaining logical source is still complete.
    """
    if source not in ('roster','candidates') or width not in (2,4):
        raise ValueError('closed command packet transfer role required')
    while True:
        view=getattr(frame,source)
        value=view.word() if width==2 else view.long()
        frame=first_replace(frame,**{source:view.advance(width)})
        frame=_city_ui_store_fields(state,frame,destination,value,width)
        frame,again=_command_panel_dbra_fields(frame,counter)
        if not again:return frame


def _command_panel_glyph_fields(state: SceneState, frame: FirstDeploymentFrame,
        source: int, rows: int, continuation: int, stream: bool=False) -> FirstDeploymentFrame:
    """One named glyph block uses the already restored decoder, not a copied font algorithm."""
    frame=_command_panel_pointer_fields(state,frame,'roster',source)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'count',rows,16)
    return _campaign_ui_call_fields(state,frame,0xAF1E if stream else 0xAE8A,continuation)


def _command_panel_copy_fields(state: SceneState, frame: FirstDeploymentFrame,
        counter: str, width: int=4) -> FirstDeploymentFrame:
    """Copy an actual live packet between A0/A1 with both original postincrements."""
    while True:
        value=frame.roster.long() if width==4 else frame.roster.word()
        frame=first_replace(frame,roster=frame.roster.advance(width))
        frame=_city_ui_store_fields(state,frame,frame.candidates.base,value,width)
        frame=first_replace(frame,candidates=frame.candidates.advance(width))
        frame,again=_command_panel_dbra_fields(frame,counter)
        if not again:return frame


def _command_panel_value_upload_fields(state: SceneState, frame: FirstDeploymentFrame,
        command: int, source: int=0xFFFFD306, count: int=2) -> FirstDeploymentFrame:
    """Publish one completed officer value block through its original A4 WORD port."""
    frame=_city_ui_store_fields(state,frame,0xC00004,command,4)
    frame=_command_panel_pointer_fields(state,frame,'candidates',source)
    frame=_movement_move(state,frame,'target_x',count,16)
    return _command_panel_upload_fields(state,frame,'candidates','target_x',frame.opponent.base,2)


def _command_panel_row_stride_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """BB96's existing bounded five-bit WORD shift, without a second numeric core."""
    from ..high_level_battle_ai.business_formation import _first_shift_word
    frame=_first_shift_word(frame,'choice',low16(frame.choice),5)
    state.sr=(state.sr&65504)|frame.status
    return frame


def _command_panel_repeat_fields(state: SceneState, frame: FirstDeploymentFrame,
        destination: int, value: int, counter: str, width: int=2) -> FirstDeploymentFrame:
    """Repeated border or background cells retain the real counter and MOVE flags."""
    if width not in (2,4):raise ValueError('actual border cell width required')
    while True:
        frame=_city_ui_store_fields(state,frame,destination,value,width)
        frame,again=_command_panel_dbra_fields(frame,counter)
        if not again:return frame


def _command_panel_status_fields(state: SceneState, frame: FirstDeploymentFrame,
        value: int) -> FirstDeploymentFrame:
    """Use the existing Scene supervisor/trace boundary for a real full-SR write."""
    state.set_status_word(value)
    return first_replace(frame,status=value&31)


def _command_panel_fill_buffer_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: str, counter: str, value: int=0x11111111, clear: bool=False) -> FirstDeploymentFrame:
    """Initialize the live packet buffer; CLR includes its original prior read."""
    if address not in ('roster','candidates','controller'):raise ValueError('closed command buffer role required')
    while True:
        view=getattr(frame,address)
        frame=_city_ui_store_fields(state,frame,view.base,value,4,clear)
        frame=first_replace(frame,**{address:view.advance(4)})
        frame,again=_command_panel_dbra_fields(frame,counter)
        if not again:return frame


def append_current_roster_marks_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5010: initialize roster glyph rows, decode both runs and publish their live tiles."""
    frame=_city_ui_frame_fields(state,frame,0x5010)
    frame=_movement_move(state,frame,'unit',31,16)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_command_panel_fill_buffer_fields(state,frame,'candidates','unit')
    frame=_command_panel_pointer_fields(state,frame,'roster',0x8A1BC)
    frame=_movement_move(state,frame,'count',24,16)
    frame=_campaign_ui_call_fields(state,frame,0xAE8A,0x5032)
    frame=_city_ui_store_fields(state,frame,0xC00004,0x40200000,4)
    frame=_movement_move(state,frame,'distance',0x33F,16)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_command_panel_upload_fields(state,frame,'candidates','distance',frame.auxiliary.base)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'count',2,16)
    frame=_campaign_ui_call_fields(state,frame,0xAE8A,0x5058)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'distance',159,16)
    frame=_command_panel_upload_fields(state,frame,'candidates','distance',frame.auxiliary.base)
    return _city_ui_store_fields(state,frame,0xFFFFF37E,0,2,True)


def render_current_city_command_labels_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """506C: live WORD-dispatched label, packet upload and original blank continuation."""
    frame=_city_ui_frame_fields(state,frame,0x506C)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),129,16)
    if frame.status&4:return frame
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF36C,2),16)
    frame=_city_ui_shift_fields(state,frame,'unit',1)
    frame=_movement_move(state,frame,'unit',state.read(u32(0x50BE+s16(low16(frame.unit))),2),16)
    frame=_campaign_ui_call_fields(state,frame,u32(0x50C6+s16(low16(frame.unit))),0x5088)
    frame=_city_ui_store_fields(state,frame,0xC00004,0x74000001,4)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_command_panel_upload_fields(state,frame,'candidates','distance',0xC00000)
    frame=_city_ui_store_fields(state,frame,0xC00004,0x76000001,4)
    frame=_movement_move(state,frame,'count',7,16)
    return _command_panel_repeat_fields(state,frame,0xC00000,0x11111111,'count',4)


def compose_city_roster_rows_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5242: current city name, its live ruler and its subordinate relation row."""
    frame=_city_ui_frame_fields(state,frame,0x5242)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF364,2),16)
    frame=_city_ui_shift_fields(state,frame,'unit',2)
    frame=_command_panel_pointer_fields(state,frame,'roster',0x8A212+s16(low16(frame.unit)))
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'count',1,16)
    frame=_campaign_ui_call_fields(state,frame,0xAE8A,0x5260)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=_movement_move(state,frame,'distance',state.read(0xFFFFF364,2),16)
    frame=_movement_move(state,frame,'distance',low16(frame.distance)&255,16)
    frame=_command_panel_pointer_fields(state,frame,'controller',0xFFFFF427)
    frame=_movement_move(state,frame,'unit',frame.controller.byte(low16(frame.distance)),8)
    frame=_movement_move(state,frame,'unit',u16(s8(low8(frame.unit))),16)
    frame=_city_ui_store_fields(state,frame,0xFFFFF62E,low8(frame.unit),1)
    if not frame.status&8:
        frame=_command_panel_pointer_fields(state,frame,'controller',0xFFFFE640)
        frame=_city_ui_shift_fields(state,frame,'unit',1)
        frame=_movement_move(state,frame,'unit',frame.controller.word(low16(frame.unit)),16)
        frame=_city_ui_store_fields(state,frame,0xFFFFF634,low16(frame.unit))
    frame=_campaign_ui_call_fields(state,frame,0x539E,0x528C)
    frame=_movement_move(state,frame,'distance',state.read(0xFFFFF364,2),16)
    frame=_city_ui_shift_fields(state,frame,'distance',1)
    frame=_command_panel_pointer_fields(state,frame,'controller',0xFFFFF45E)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=_movement_move(state,frame,'unit',frame.controller.word(low16(frame.distance)),16)
    frame=_city_ui_store_fields(state,frame,0xFFFFF630,low16(frame.unit))
    frame=_campaign_ui_call_fields(state,frame,0x539E,0x52A4)
    frame=_city_ui_store_fields(state,frame,0xC00004,0x60000001,4)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'offset_x',255,16)
    return _command_panel_upload_fields(state,frame,'candidates','offset_x',0xC00000)


def compose_selected_force_rows_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5330: five-byte selected force stream with its real forty-LONG upload."""
    frame=_city_ui_frame_fields(state,frame,0x5330)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF364,2),16)
    frame=_movement_move(state,frame,'unit',low16(frame.unit)&255,16)
    frame=_movement_move(state,frame,'count',low16(frame.unit),16)
    frame=_city_ui_shift_fields(state,frame,'unit',2)
    frame=_city_ui_arithmetic_fields(state,frame,'unit',low16(frame.count))
    frame=_command_panel_pointer_fields(state,frame,'roster',0x8A421+s16(low16(frame.unit)))
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'count',4,16)
    frame=_campaign_ui_call_fields(state,frame,0xAF1E,0x5356)
    frame=_city_ui_store_fields(state,frame,0xC00004,0x65800001,4)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'unit',39,16)
    return _command_panel_upload_fields(state,frame,'candidates','unit',frame.auxiliary.base)


def append_city_relation_row_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """539E: a real officer-name row or the original blank six-row placeholder."""
    frame=_city_ui_frame_fields(state,frame,0x539E)
    frame=_movement_test(state,frame,low16(frame.unit),16)
    if not frame.status&8:
        frame=_movement_move(state,frame,'count',low16(frame.unit),16)
        frame=_city_ui_shift_fields(state,frame,'count',1)
        frame=_city_ui_arithmetic_fields(state,frame,'count',low16(frame.unit))
        frame=_city_ui_shift_fields(state,frame,'count',1)
        frame=_command_panel_pointer_fields(state,frame,'roster',0x8A504+s16(low16(frame.count)))
        frame=_movement_move(state,frame,'count',2,16)
        return _campaign_ui_call_fields(state,frame,0xAE8A,0x53BE)
    frame=_command_panel_pointer_fields(state,frame,'controller',s16(low16(frame.candidates.base)))
    frame=_movement_move(state,frame,'count',95,16)
    frame=_command_panel_fill_buffer_fields(state,frame,'controller','count')
    frame=_movement_move(state,frame,'count',5,16)
    while True:
        frame=_city_ui_store_fields(state,frame,frame.candidates.base+28,0x33333333,4)
        frame=first_replace(frame,candidates=frame.candidates.advance(64))
        frame,again=_command_panel_dbra_fields(frame,'count')
        if not again:return frame


def render_roster_name_or_prompt_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """54CA/559E: choose the original prompt by live roster membership and mode."""
    frame=_city_ui_frame_fields(state,frame,0x54CA)
    frame=_movement_compare(state,frame,state.read(0xFFFFF6C4,2),1,16)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_y',3,16)
        frame=_movement_compare(state,frame,low16(frame.choice),0x4000,16)
        return _movement_move(state,frame,'target_y',2,16) if not frame.status&1 else frame
    frame=_movement_move(state,frame,'target_y',3,16)
    frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),0x100,16)
    if frame.status&4:return frame
    frame=_movement_test(state,frame,state.read(0xFFFFF656,2),16)
    if not frame.status&4:
        frame=_movement_move(state,frame,'offset_y',low16(frame.choice),16)
        frame=_movement_move(state,frame,'offset_y',low16(frame.offset_y)&255,16)
        frame=_command_panel_pointer_fields(state,frame,'scan',0xFFFFCD00)
        frame=_movement_move(state,frame,'distance',frame.scan.byte(low16(frame.offset_y)),8)
        if not frame.status&4:return _movement_move(state,frame,'target_y',5,16)
        frame=_movement_compare(state,frame,low16(frame.choice),0x4000,16)
        return _movement_move(state,frame,'target_y',4,16) if not frame.status&1 else frame
    for address,value,width in ((0xFFFFF36C,1,2),(0xFFFFF579,8,1),(0xFFFFF380,0x7A,2),(0xFFFFF38C,0x51,2)):
        frame=_movement_compare(state,frame,state.read(address,width),value,width*8)
        if (address==0xFFFFF36C and not frame.status&4) or (address!=0xFFFFF36C and frame.status&4):return frame
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF364,2),16)
    frame=_command_panel_pointer_fields(state,frame,'scan',0xFFFFF427)
    frame=_movement_move(state,frame,'unit',frame.scan.byte(low16(frame.unit)),8)
    frame=_movement_compare(state,frame,low8(frame.unit),state.read(0xFFFFF377,1),8)
    if not frame.status&4:return frame
    frame=_command_panel_pointer_fields(state,frame,'scan',0xFFFFCD00)
    frame=_movement_move(state,frame,'distance',frame.scan.byte(low16(frame.choice)),8)
    if frame.status&4:return frame
    frame=_movement_move(state,frame,'target_y',4,16)
    frame=_movement_compare(state,frame,low8(frame.distance),1,8)
    return frame if frame.status&4 else _campaign_ui_call_fields(state,frame,0x5564,0x553E)


def render_selected_city_packet_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5564: recognize the three assigned officer WORDs before clearing the live mark."""
    frame=_city_ui_frame_fields(state,frame,0x5564)
    frame=_command_panel_pointer_fields(state,frame,'opponent',0xFFFFE80C)
    frame=_movement_move(state,frame,'count',state.read(0xFFFFF364,2),16)
    frame=_city_ui_shift_fields(state,frame,'count',1)
    frame=_city_ui_arithmetic_fields(state,frame,'count',state.read(0xFFFFF364,2))
    frame=_city_ui_shift_fields(state,frame,'count',2)
    for displacement in (0,4,8):
        frame=_movement_compare(state,frame,low16(frame.choice),frame.opponent.word(low16(frame.count+displacement)),16)
        if frame.status&4:return _movement_move(state,frame,'target_y',5,16)
    frame=_movement_move(state,frame,'target_y',3,16)
    return _city_ui_store_fields(state,frame,u32(frame.scan.base+s16(low16(frame.choice))),0,1,True)


def append_force_roster_names_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """55D0: preserve D2/A3 physically, invalidate mismatched members and draw three rows."""
    frame=_city_ui_frame_fields(state,frame,0x55D0)
    frame=_movement_save_longs(state,frame,('unit','scan'))
    frame=_movement_move(state,frame,'target_x',1,16)
    frame=_movement_move(state,frame,'target_y',3,16)
    frame=_command_panel_pointer_fields(state,frame,'roster',0x8A46A)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'count',5,16)
    frame=_campaign_ui_call_fields(state,frame,0xAE8A,0x55F0)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_city_ui_store_fields(state,frame,0xC00004,0x5D000003,4)
    frame=_movement_move(state,frame,'count',0xBF,16)
    frame=_command_panel_upload_fields(state,frame,'candidates','count',0xC00000)
    frame=_movement_move(state,frame,'offset_x',2,16)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'distance',state.read(0xFFFFF364,2),16)
    frame=_city_ui_shift_fields(state,frame,'distance',1)
    frame=_city_ui_arithmetic_fields(state,frame,'distance',state.read(0xFFFFF364,2))
    frame=_city_ui_shift_fields(state,frame,'distance',2)
    frame=_command_panel_pointer_fields(state,frame,'controller',0xFFFFE80C)
    frame=_command_panel_pointer_fields(state,frame,'scan',0xFFFFCC00)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF364,2),16)
    while True:
        frame=_movement_move(state,frame,'offset_y',frame.controller.word(low16(frame.distance)),16)
        available=not frame.status&8
        if available:
            frame=_movement_compare(state,frame,low8(frame.unit),frame.scan.byte(low16(frame.offset_y)),8)
            available=bool(frame.status&4)
            if not available:frame=_city_ui_store_fields(state,frame,u32(frame.controller.base+s16(low16(frame.distance))),65535)
        if available:
            frame=_movement_move(state,frame,'choice',low16(frame.offset_y),16)
            frame=_city_ui_shift_fields(state,frame,'choice',1)
            frame=_city_ui_arithmetic_fields(state,frame,'choice',low16(frame.offset_y))
            frame=_city_ui_shift_fields(state,frame,'choice',1)
            frame=_command_panel_pointer_fields(state,frame,'roster',0x8A504+s16(low16(frame.choice)))
        else:frame=_command_panel_pointer_fields(state,frame,'roster',0x568E)
        frame=_movement_move(state,frame,'count',2,16)
        frame=_campaign_ui_call_fields(state,frame,0xAE8A,0x5666)
        frame=_city_ui_arithmetic_fields(state,frame,'distance',4)
        frame,again=_command_panel_dbra_fields(frame,'offset_x')
        if not again:break
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_city_ui_store_fields(state,frame,0xC00004,0x68000001,4)
    frame=_movement_move(state,frame,'target_x',0x11F,16)
    frame=_command_panel_upload_fields(state,frame,'candidates','target_x',0xC00000)
    return _movement_restore_longs(state,frame,('unit','scan'))


def append_selected_force_head_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """57A0: sum the actual selected roster troops and its city's reserve into E4FC."""
    frame=_city_ui_frame_fields(state,frame,0x57A0)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&255,16)
    frame=_campaign_ui_call_fields(state,frame,0x5F48,0x57AC)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFF500)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFC800)
    frame=_movement_move_long(state,frame,'target_x',0)
    while True:
        frame=_movement_move(state,frame,'target_y',frame.roster.word(),16)
        frame=first_replace(frame,roster=frame.roster.advance(2))
        if frame.status&8:break
        frame=_city_ui_shift_fields(state,frame,'target_y',2)
        frame=_movement_arithmetic_long(state,frame,'target_x',frame.candidates.long(low16(frame.target_y)))
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFE774)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF364,2),16)
    frame=_city_ui_shift_fields(state,frame,'target_y',2)
    frame=_movement_arithmetic_long(state,frame,'target_x',frame.roster.long(low16(frame.target_y)))
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFE4FC)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF364,2),16)
    frame=_city_ui_shift_fields(state,frame,'target_y',2)
    return _city_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_y))),frame.target_x,4)


def draw_force_summary_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A456: selected force name and suffix, with the original privileged display refresh."""
    frame=_city_ui_frame_fields(state,frame,0xA456)
    frame=_command_panel_status_fields(state,frame,0x2700)
    frame=_command_panel_pointer_fields(state,frame,'roster',state.read(0xFF382C,4))
    frame=_movement_move(state,frame,'target_x',0,16)
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(4),8)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFE640)
    frame=_city_ui_shift_fields(state,frame,'target_x',1)
    frame=_movement_move(state,frame,'target_x',frame.candidates.word(low16(frame.target_x)),16)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame=_city_ui_shift_fields(state,frame,'target_x',1)
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',low16(frame.target_y))
    frame=_city_ui_shift_fields(state,frame,'target_x',1)
    frame=_command_panel_pointer_fields(state,frame,'roster',0x8A504+s16(low16(frame.target_x)))
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'target_x',1,16)
    frame=_movement_move(state,frame,'target_y',3,16)
    frame=_movement_move(state,frame,'count',2,16)
    frame=_campaign_ui_call_fields(state,frame,0xAE8A,0xA496)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xA4CA)
    frame=_movement_move(state,frame,'count',0,16)
    frame=_campaign_ui_call_fields(state,frame,0xAE8A,0xA4A6)
    frame=_city_ui_store_fields(state,frame,0xC00004,0x41A00000,4)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'count',127,16)
    frame=_command_panel_upload_fields(state,frame,'candidates','count',0xC00000)
    return _campaign_ui_call_fields(state,frame,0xAF48,0xA4C8)


def draw_current_scenario_prompt_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A622: scenario screen phases retain their true display/audio child boundaries."""
    frame=_city_ui_frame_fields(state,frame,0xA622)
    frame=_command_panel_status_fields(state,frame,0x2700)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF606,2),16)
    frame=_movement_move(state,frame,'target_x',low8(frame.target_x)&0xBF,8)
    frame=_city_ui_store_fields(state,frame,0xC00004,low16(frame.target_x))
    frame=_campaign_ui_call_fields(state,frame,0x68CE,0xA63A)
    frame=_command_panel_pointer_fields(state,frame,'auxiliary',0xC00004)
    frame=_command_panel_pointer_fields(state,frame,'scratch',0xC00000)
    frame=_movement_move_long(state,frame,'target_x',5)
    frame=_campaign_ui_call_fields(state,frame,0x8112,0xA64E)
    frame=_campaign_ui_call_fields(state,frame,0xA67E,0xA652)
    frame=_campaign_ui_call_fields(state,frame,0xA760,0xA656)
    frame=_campaign_ui_call_fields(state,frame,0xA82E,0xA65C)
    frame=_city_ui_store_fields(state,frame,0xFFFFF35A,0,2,True)
    frame=_campaign_ui_call_fields(state,frame,0xA924,0xA664)
    frame=_city_ui_store_fields(state,frame,0xFFFFF316,0,2,True)
    frame=_city_ui_store_fields(state,frame,0xFFFFF312,0,2,True)
    frame=_city_ui_store_fields(state,frame,0xFFFFF6C4,4)
    frame=_campaign_ui_call_fields(state,frame,0xA72A,0xA678)
    return _command_panel_status_fields(state,frame,0x2500)


def append_scenario_owner_glyphs_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A67E: top, twenty-four middle and bottom border rows at the actual ports."""
    frame=_city_ui_frame_fields(state,frame,0xA67E)
    frame=_movement_move_long(state,frame,'unit',0x40800003)
    frame=_city_ui_store_fields(state,frame,frame.auxiliary.base,frame.unit,4)
    for value in (0,0,0x480):frame=_city_ui_store_fields(state,frame,frame.scratch.base,value)
    frame=_movement_move(state,frame,'target_y',0x21,16)
    frame=_command_panel_repeat_fields(state,frame,frame.scratch.base,0x481,'target_y')
    for value in (0xC80,0,0):frame=_city_ui_store_fields(state,frame,frame.scratch.base,value)
    frame=_movement_move(state,frame,'target_x',0x17,16)
    while True:
        frame=_movement_arithmetic_long(state,frame,'unit',0x800000)
        frame=_city_ui_store_fields(state,frame,frame.auxiliary.base,frame.unit,4)
        for value in (0,0,0x482):frame=_city_ui_store_fields(state,frame,frame.scratch.base,value)
        frame=_movement_move(state,frame,'target_y',0x21,16)
        frame=_command_panel_repeat_fields(state,frame,frame.scratch.base,0x483,'target_y')
        for value in (0xC82,0,0):frame=_city_ui_store_fields(state,frame,frame.scratch.base,value)
        frame,again=_command_panel_dbra_fields(frame,'target_x')
        if not again:break
    frame=_movement_arithmetic_long(state,frame,'unit',0x800000)
    frame=_city_ui_store_fields(state,frame,frame.auxiliary.base,frame.unit,4)
    for value in (0,0,0x1480):frame=_city_ui_store_fields(state,frame,frame.scratch.base,value)
    frame=_movement_move(state,frame,'target_y',0x21,16)
    frame=_command_panel_repeat_fields(state,frame,frame.scratch.base,0x1481,'target_y')
    for value in (0x1C80,0,0):frame=_city_ui_store_fields(state,frame,frame.scratch.base,value)
    frame=_city_ui_store_fields(state,frame,0xC00004,0x50000002,4)
    frame=_command_panel_pointer_fields(state,frame,'roster',0x89DDC)
    frame=_movement_move(state,frame,'target_x',0x5F,16)
    return _command_panel_upload_fields(state,frame,'roster','target_x',0xC00000)


def append_scenario_owner_value_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A72A: clear forty owner totals and count the original 256 roster BYTEs."""
    frame=_city_ui_frame_fields(state,frame,0xA72A)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFE460)
    frame=_movement_move(state,frame,'target_x',39,16)
    frame=_command_panel_fill_buffer_fields(state,frame,'roster','target_x',0,True)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFE45C)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFCC00)
    frame=_movement_move(state,frame,'target_x',255,16)
    while True:
        frame=_movement_move(state,frame,'target_y',0,16)
        frame=_movement_move(state,frame,'target_y',frame.candidates.byte(),8)
        frame=first_replace(frame,candidates=frame.candidates.advance(1))
        if not frame.status&4:
            frame=_movement_compare(state,frame,low8(frame.target_y),40,8)
            if frame.status&5:
                frame=_city_ui_shift_fields(state,frame,'target_y',2)
                frame=_city_ui_memory_arithmetic_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_y))+2),1)
        frame,again=_command_panel_dbra_fields(frame,'target_x')
        if not again:return frame


def draw_title_mode_prompt_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A82E: title headings, four body rows and the retained stream footer."""
    frame=_city_ui_frame_fields(state,frame,0xA82E)
    frame=_city_ui_store_fields(state,frame,0xC00004,0x40000001,4)
    frame=_movement_move(state,frame,'target_x',1,8)
    frame=_movement_move(state,frame,'target_y',0,8)
    for source,count,token,limit,command in ((0x8A1BC,11,0xA852,383,None),(0x8A214,0,0xA878,31,None),(0x8A200,9,0xA89E,319,0x41400002)):
        frame=_command_panel_pointer_fields(state,frame,'roster',source)
        frame=_movement_move(state,frame,'count',count,16)
        frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
        frame=_campaign_ui_call_fields(state,frame,0xAE8A,token)
        if command is not None:frame=_city_ui_store_fields(state,frame,0xC00004,command,4)
        frame=_movement_move(state,frame,'offset_x',limit,16)
        frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
        frame=_command_panel_upload_fields(state,frame,'candidates','offset_x',0xC00000)
    frame=_command_panel_pointer_fields(state,frame,'roster',0x8A216)
    frame=_city_ui_store_fields(state,frame,0xC00004,0x58000001,4)
    frame=_movement_move(state,frame,'distance',3,16)
    while True:
        frame=_movement_move(state,frame,'count',19,16)
        frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
        frame=_campaign_ui_call_fields(state,frame,0xAE8A,0xA8DC)
        frame=_movement_move(state,frame,'offset_x',639,16)
        frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
        frame=_command_panel_upload_fields(state,frame,'candidates','offset_x',0xC00000)
        frame,again=_command_panel_dbra_fields(frame,'distance')
        if not again:break
    frame=_command_panel_pointer_fields(state,frame,'roster',0x8A426)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'count',9,16)
    frame=_campaign_ui_call_fields(state,frame,0xAF1E,0xA906)
    frame=_city_ui_store_fields(state,frame,0xC00004,0x40000002,4)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'unit',79,16)
    return _command_panel_upload_fields(state,frame,'candidates','unit',0xC00000)


def draw_roster_overview_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """B286: names, affiliations and roster category, with actual A4/A5 display ports."""
    frame=_city_ui_frame_fields(state,frame,0xB286)
    frame=_movement_move(state,frame,'target_x',1,16)
    frame=_movement_move(state,frame,'target_y',3,16)
    frame=_command_panel_glyph_fields(state,frame,0x8A38C,25,0xB2A2)
    frame=_city_ui_store_fields(state,frame,frame.scratch.base,0x40000001,4)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'count',0x33F,16)
    frame=_command_panel_upload_fields(state,frame,'candidates','count',frame.opponent.base)
    frame=_command_panel_pointer_fields(state,frame,'roster',0x89F7C)
    frame=_movement_move(state,frame,'count',63,16)
    frame=_command_panel_upload_fields(state,frame,'roster','count',0xC00000)
    frame=_command_panel_glyph_fields(state,frame,0x8A426,9,0xB2DE,True)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'count',79,16)
    frame=_command_panel_upload_fields(state,frame,'candidates','count',0xC00000)
    frame=_command_panel_glyph_fields(state,frame,0x8A3C0,0,0xB304)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'count',31,16)
    frame=_command_panel_upload_fields(state,frame,'candidates','count',0xC00000)
    frame=_campaign_ui_call_fields(state,frame,0xB414,0xB31A)
    frame=_movement_move(state,frame,'count',state.read(0xFFFFF372,2),16)
    frame=_movement_move(state,frame,'distance',low16(frame.count),16)
    frame=_city_ui_shift_fields(state,frame,'count',1)
    frame=_city_ui_arithmetic_fields(state,frame,'count',low16(frame.distance))
    frame=_city_ui_shift_fields(state,frame,'count',1)
    frame=_command_panel_glyph_fields(state,frame,0x8A504+s16(low16(frame.count)),2,0xB33E)
    frame=_city_ui_store_fields(state,frame,frame.scratch.base,0x50000001,4)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'count',95,16)
    frame=_command_panel_upload_fields(state,frame,'candidates','count',frame.opponent.base)
    frame=_command_panel_glyph_fields(state,frame,0x8A3C2,9,0xB366)
    frame=_city_ui_store_fields(state,frame,frame.scratch.base,0x58000001,4)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'count',319,16)
    frame=_command_panel_upload_fields(state,frame,'candidates','count',frame.opponent.base)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF372,2),16)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFE640)
    frame=_movement_move(state,frame,'count',15,16)
    found=False
    while True:
        value=frame.roster.word()
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_movement_compare(state,frame,low16(frame.unit),value,16)
        if frame.status&4:
            frame=_city_ui_store_fields(state,frame,0xFFFFF63A,128)
            frame=_command_panel_pointer_fields(state,frame,'roster',0xB40C)
            found=True
            break
        frame,again=_command_panel_dbra_fields(frame,'count')
        if not again:break
    if not found:
        frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFC700)
        frame=_movement_move(state,frame,'unit',frame.roster.byte(low16(frame.unit)),8)
        frame=_movement_move(state,frame,'unit',low16(frame.unit)&15,16)
        frame=_movement_compare(state,frame,low16(frame.unit),4,16)
        if not frame.status&5:frame=_city_ui_arithmetic_fields(state,frame,'unit',3,True)
        frame=_city_ui_store_fields(state,frame,0xFFFFF63A,low16(frame.unit))
        frame=_city_ui_shift_fields(state,frame,'unit',3)
        frame=_command_panel_pointer_fields(state,frame,'roster',0x8A3D6+s16(low16(frame.unit)))
    frame=_movement_move(state,frame,'count',3,16)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_campaign_ui_call_fields(state,frame,0xAE8A,0xB3D4)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'count',127,16)
    frame=_command_panel_upload_fields(state,frame,'candidates','count',frame.opponent.base)
    frame=_command_panel_glyph_fields(state,frame,0x8A1D8,3,0xB3F6)
    frame=_city_ui_store_fields(state,frame,frame.scratch.base,0x60000001,4)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'count',191,16)
    return _command_panel_upload_fields(state,frame,'candidates','count',frame.opponent.base)


def append_roster_overview_cursor_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """B414: the three live affiliation BYTEs select three-word names, then one glyph run."""
    frame=_city_ui_frame_fields(state,frame,0xB414)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFEA88)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF372,2),16)
    frame=_city_ui_shift_fields(state,frame,'unit',1)
    frame=_city_ui_arithmetic_fields(state,frame,'unit',state.read(0xFFFFF372,2))
    frame=_command_panel_pointer_fields(state,frame,'roster',frame.roster.base+s16(low16(frame.unit)))
    frame=_command_panel_pointer_fields(state,frame,'controller',0x8A4C8)
    frame=_movement_move(state,frame,'unit',0,16)
    for offset in (0,1,2):
        frame=_movement_move(state,frame,'unit',frame.roster.byte(offset),8)
        if frame.status&4:
            for unused in range(3):
                frame=_city_ui_store_fields(state,frame,frame.candidates.base,63)
                frame=first_replace(frame,candidates=frame.candidates.advance(2))
        else:
            frame=_city_ui_shift_fields(state,frame,'unit',1)
            frame=_city_ui_arithmetic_fields(state,frame,'unit',frame.roster.byte(offset),width=8)
            frame=_city_ui_shift_fields(state,frame,'unit',1)
            for displacement in (0,2,4):
                value=frame.controller.word(low16(frame.unit+displacement))
                frame=_city_ui_store_fields(state,frame,frame.candidates.base,value)
                frame=first_replace(frame,candidates=frame.candidates.advance(2))
        if offset!=2:frame=first_replace(frame,controller=frame.controller.advance(18))
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFD300)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD320)
    frame=_movement_move(state,frame,'count',8,16)
    frame=_campaign_ui_call_fields(state,frame,0xAE8A,0xB4CA)
    frame=_city_ui_store_fields(state,frame,0xC00004,0x53800001,4)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFD320)
    frame=_movement_move(state,frame,'count',287,16)
    return _command_panel_upload_fields(state,frame,'roster','count',frame.opponent.base)


def draw_roster_overview_values_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """B4E4: retain all border counters and both special column markers."""
    frame=_city_ui_frame_fields(state,frame,0xB4E4)
    frame=_movement_move_long(state,frame,'target_x',0x40020003)
    frame=_city_ui_store_fields(state,frame,frame.scratch.base,frame.target_x,4)
    frame=_city_ui_store_fields(state,frame,frame.opponent.base,0xC268)
    frame=_movement_move(state,frame,'target_y',35,16)
    frame=_command_panel_repeat_fields(state,frame,frame.opponent.base,0xC269,'target_y')
    frame=_city_ui_store_fields(state,frame,frame.opponent.base,0xCA68)
    frame=_movement_move(state,frame,'target_y',24,16)
    while True:
        frame=_movement_arithmetic_long(state,frame,'target_x',0x800000)
        frame=_city_ui_store_fields(state,frame,frame.scratch.base,frame.target_x,4)
        frame=_city_ui_store_fields(state,frame,frame.opponent.base,0xC26A)
        frame=_movement_move(state,frame,'unit',35,16)
        frame=_command_panel_repeat_fields(state,frame,frame.opponent.base,0xC200,'unit')
        frame=_city_ui_store_fields(state,frame,frame.opponent.base,0xCA6A)
        frame,again=_command_panel_dbra_fields(frame,'target_y')
        if not again:break
    frame=_movement_arithmetic_long(state,frame,'target_x',0x800000)
    frame=_city_ui_store_fields(state,frame,frame.scratch.base,frame.target_x,4)
    frame=_city_ui_store_fields(state,frame,frame.opponent.base,0xD268)
    frame=_movement_move(state,frame,'target_y',35,16)
    frame=_command_panel_repeat_fields(state,frame,frame.opponent.base,0xD269,'target_y')
    frame=_city_ui_store_fields(state,frame,frame.opponent.base,0xDA68)
    frame=_city_ui_store_fields(state,frame,frame.scratch.base,0x8F80)
    for command in (0x461A0003,0x46320003):
        frame=_city_ui_store_fields(state,frame,frame.scratch.base,command,4)
        frame=_movement_move(state,frame,'target_x',13,16)
        frame=_command_panel_repeat_fields(state,frame,frame.opponent.base,0xC26E,'target_x')
        frame=_city_ui_store_fields(state,frame,frame.opponent.base,0xC26C)
    frame=_city_ui_store_fields(state,frame,frame.scratch.base,0x8F02)
    frame=_city_ui_store_fields(state,frame,frame.scratch.base,0x45820003,4)
    frame=_city_ui_store_fields(state,frame,frame.opponent.base,0xC26B)
    frame=_movement_move(state,frame,'target_x',35,16)
    while True:
        frame=_movement_compare(state,frame,low16(frame.target_x),24,16)
        marker=bool(frame.status&4)
        if not marker:
            frame=_movement_compare(state,frame,low16(frame.target_x),12,16)
            marker=bool(frame.status&4)
        frame=_city_ui_store_fields(state,frame,frame.opponent.base,0xC26D if marker else 0xC26F)
        frame,again=_command_panel_dbra_fields(frame,'target_x')
        if not again:break
    frame=_city_ui_store_fields(state,frame,frame.opponent.base,0xCA6B)
    frame=_city_ui_store_fields(state,frame,frame.scratch.base,0x47140003,4)
    for unused in range(3):frame=_city_ui_store_fields(state,frame,frame.opponent.base,0xC26F)
    return frame


def append_selected_city_head_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """B5B8: real city-head query, eight copied LONGs and original grid tile advancement."""
    frame=_city_ui_frame_fields(state,frame,0xB5B8)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF372,2),16)
    frame=_movement_move(state,frame,'target_y',5,16)
    frame=_campaign_ui_call_fields(state,frame,0x661D4,0xB5C6)
    frame=_city_ui_store_fields(state,frame,0xFFFFF31E,0,2,True)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFFB00)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFFB80)
    frame=_movement_move(state,frame,'target_x',7,16)
    frame=_command_panel_copy_fields(state,frame,'target_x')
    frame=_movement_move_long(state,frame,'target_x',0x40840003)
    frame=_movement_move(state,frame,'target_y',0x8005,16)
    frame=_movement_move(state,frame,'unit',7,16)
    while True:
        frame=_city_ui_store_fields(state,frame,0xC00004,frame.target_x,4)
        frame=_movement_arithmetic_long(state,frame,'target_x',0x800000)
        frame=_movement_move(state,frame,'distance',5,16)
        while True:
            frame=_city_ui_store_fields(state,frame,0xC00000,low16(frame.target_y))
            frame=_city_ui_arithmetic_fields(state,frame,'target_y',1)
            frame,again=_command_panel_dbra_fields(frame,'distance')
            if not again:break
        frame,again=_command_panel_dbra_fields(frame,'unit')
        if not again:break
    frame=_city_ui_store_fields(state,frame,0xC00004,0x43080003,4)
    return _city_ui_store_fields(state,frame,0xC00000,0x803D803E,4)


def append_roster_overview_digit_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """B620: twenty real coordinate records, with two existing column calls per row."""
    from ..high_level_remaining_flows.business_city import _special_action_shift_long, _special_action_swap
    frame=_city_ui_frame_fields(state,frame,0xB620)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xB66A)
    frame=_movement_move(state,frame,'choice',19,16)
    while True:
        frame=_movement_move_long(state,frame,'target_x',0)
        frame=_movement_move(state,frame,'target_x',frame.roster.word(),16)
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_special_action_shift_long(state,frame,'target_x',2)
        frame=_movement_fixed_shift_word(state,frame,'target_x',2,True)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)|0x4000,16)
        frame=_special_action_swap(state,frame,'target_x')
        frame=_movement_move(state,frame,'target_y',frame.roster.word(),16)
        frame=first_replace(frame,roster=frame.roster.advance(2))
        while True:
            frame=_city_ui_store_fields(state,frame,frame.scratch.base,frame.target_x,4)
            frame=_movement_move(state,frame,'unit',frame.roster.word(),16)
            frame=first_replace(frame,roster=frame.roster.advance(2))
            frame=_campaign_ui_call_fields(state,frame,0xB660,0xB640)
            frame=_city_ui_arithmetic_fields(state,frame,'unit',1)
            frame=_movement_move_long(state,frame,'count',frame.target_x)
            frame=_movement_arithmetic_long(state,frame,'count',0x800000)
            frame=_city_ui_store_fields(state,frame,frame.scratch.base,frame.count,4)
            frame=_campaign_ui_call_fields(state,frame,0xB660,0xB650)
            frame=_movement_arithmetic_long(state,frame,'target_x',0x40000)
            frame,again=_command_panel_dbra_fields(frame,'target_y')
            if not again:break
        frame,again=_command_panel_dbra_fields(frame,'choice')
        if not again:return frame


def retain_roster_overview_column_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """B660: two live WORD cells; the final MOVE, not ADD, provides NZVC."""
    frame=_city_ui_frame_fields(state,frame,0xB660)
    frame=_movement_move(state,frame,'count',low16(frame.unit),16)
    frame=_city_ui_store_fields(state,frame,frame.opponent.base,low16(frame.count))
    frame=_city_ui_arithmetic_fields(state,frame,'count',2)
    return _city_ui_store_fields(state,frame,frame.opponent.base,low16(frame.count))


def compose_officer_detail_panel_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """B724: editable attribute groups share the single existing decimal/name core."""
    frame=_city_ui_frame_fields(state,frame,0xB724)
    attributes=((0xFFFFBE00,0xB72C,0x44300003),(0xFFFFC000,0xB74C,0x44460003),
        (0xFFFFB200,0xB76C,0x46940003),(0xFFFFB000,0xB78C,0x47940003),
        (0xFFFFB400,0xB7AC,0x49940003),(0xFFFFB600,0xB7CC,0x4B140003),
        (0xFFFFB800,0xB7EC,0x482C0003))
    for source,token,command in attributes:
        frame=_command_panel_pointer_fields(state,frame,'roster',source)
        frame=_campaign_ui_call_fields(state,frame,0xB92C,token)
        frame=_command_panel_value_upload_fields(state,frame,command)
    frame=_campaign_ui_call_fields(state,frame,0xB958,0xB808)
    frame=_command_panel_value_upload_fields(state,frame,0x46C60003)
    frame=_campaign_ui_call_fields(state,frame,0xB982,0xB824)
    frame=_command_panel_value_upload_fields(state,frame,0x48460003)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFC200)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF372,2),16)
    frame=_movement_compare(state,frame,frame.roster.byte(low16(frame.target_x)),100,8)
    if not frame.status&5:
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),100,1)
    frame=_campaign_ui_call_fields(state,frame,0xB94C,0xB858)
    frame=_command_panel_value_upload_fields(state,frame,0x4C940003)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFC400)
    frame=_campaign_ui_call_fields(state,frame,0xB94C,0xB878)
    frame=_command_panel_value_upload_fields(state,frame,0x49AE0003,0xFFFFD308,1)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFC500)
    frame=_campaign_ui_call_fields(state,frame,0xB94C,0xB898)
    frame=_command_panel_value_upload_fields(state,frame,0x4CAC0003)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFC800)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF372,2),16)
    frame=_city_ui_shift_fields(state,frame,'target_x',2)
    frame=_movement_move_long(state,frame,'target_x',frame.roster.long(low16(frame.target_x)))
    frame=_campaign_ui_call_fields(state,frame,0xB938,0xB8C2)
    frame=_command_panel_value_upload_fields(state,frame,0x4B280003,0xFFFFD302,4)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFE640)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF372,2),16)
    frame=_movement_move(state,frame,'target_y',15,16)
    while True:
        value=frame.roster.word()
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_movement_compare(state,frame,low16(frame.target_x),value,16)
        if frame.status&4:
            for address in (0xFFFFD306,0xFFFFD308,0xFFFFD30A):frame=_city_ui_store_fields(state,frame,address,0xC26F)
            break
        frame,again=_command_panel_dbra_fields(frame,'target_y')
        if not again:
            frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFC300)
            frame=_campaign_ui_call_fields(state,frame,0xB94C,0xB912)
            break
    return _command_panel_value_upload_fields(state,frame,0x46AC0003)


def append_officer_attribute_value_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """B9EA: selected attribute digits use the unique six-place decimal ABI."""
    frame=_city_ui_frame_fields(state,frame,0xB9EA)
    frame=_movement_move_long(state,frame,'target_x',0)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF372,2),16)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFC600)
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_y)),8)
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=_command_panel_pointer_fields(state,frame,'auxiliary',0xFFFFD300)
    frame=_city_ui_child_fields(state,frame,0x1270A,0xBA06)
    frame=_movement_move_long(state,frame,'target_y',0x40B00003)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD308)
    frame=_movement_move(state,frame,'target_x',frame.candidates.word(),16)
    frame=first_replace(frame,candidates=frame.candidates.advance(2))
    if not frame.status&4:
        frame=_city_ui_shift_fields(state,frame,'target_x',2)
        frame=_city_ui_arithmetic_fields(state,frame,'target_x',0xC2BC)
        frame=_campaign_ui_call_fields(state,frame,0xBA38,0xBA1E)
    frame=_movement_move(state,frame,'target_x',frame.candidates.word(),16)
    if frame.status&4:frame=_movement_move(state,frame,'target_x',10,16)
    frame=_city_ui_shift_fields(state,frame,'target_x',2)
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',0xC2BC)
    return _campaign_ui_call_fields(state,frame,0xBA38,0xBA34)


def scale_officer_detail_value_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """BA38: two tile columns; D1 advances only after both original rows are written."""
    frame=_city_ui_frame_fields(state,frame,0xBA38)
    frame=_movement_move_long(state,frame,'unit',frame.target_y)
    frame=_movement_move(state,frame,'count',low16(frame.target_x),16)
    frame=_city_ui_store_fields(state,frame,frame.scratch.base,frame.unit,4)
    frame=_city_ui_store_fields(state,frame,frame.opponent.base,low16(frame.count))
    frame=_city_ui_arithmetic_fields(state,frame,'count',2)
    frame=_city_ui_store_fields(state,frame,frame.opponent.base,low16(frame.count))
    frame=_movement_arithmetic_long(state,frame,'unit',0x800000)
    frame=_city_ui_store_fields(state,frame,frame.scratch.base,frame.unit,4)
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',1)
    frame=_city_ui_store_fields(state,frame,frame.opponent.base,low16(frame.target_x))
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',2)
    frame=_city_ui_store_fields(state,frame,frame.opponent.base,low16(frame.target_x))
    return _movement_arithmetic_long(state,frame,'target_y',0x40000)


def append_officer_detail_commands_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """BA5C: forty live city slots and the original officer type bit choose the command labels."""
    frame=_city_ui_frame_fields(state,frame,0xBA5C)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFF460)
    frame=_movement_move(state,frame,'target_y',39,16)
    while True:
        frame=_movement_move(state,frame,'unit',frame.roster.word(),16)
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_movement_compare(state,frame,low16(frame.unit),state.read(0xFFFFF372,2),16)
        if frame.status&4:
            for tile,command,token in ((0xC300,0x43120003,0xBA80),(0xC301,0x43920003,0xBA8E)):
                frame=_movement_move(state,frame,'target_y',tile,16)
                frame=_city_ui_store_fields(state,frame,frame.scratch.base,command,4)
                frame=_campaign_ui_call_fields(state,frame,0xBABA,token)
            break
        frame,again=_command_panel_dbra_fields(frame,'target_y')
        if not again:break
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF372,2),16)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFC700)
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_x)),8)
    frame=_city_ui_bit_fields(state,frame,frame.target_x,4)
    if not frame.status&4:
        for tile,command,token in ((0xC308,0x44920003,0xBAAC),(0xC309,0x45120003,0xBAB8)):
            frame=_movement_move(state,frame,'target_y',tile,16)
            frame=_city_ui_store_fields(state,frame,frame.scratch.base,command,4)
            frame=_campaign_ui_call_fields(state,frame,0xBABA,token)
    return frame


def append_officer_detail_title_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """BABA: four actual label cells, retaining the final ADDQ flags."""
    frame=_city_ui_frame_fields(state,frame,0xBABA)
    frame=_movement_move(state,frame,'count',3,16)
    while True:
        frame=_city_ui_store_fields(state,frame,frame.opponent.base,low16(frame.target_y))
        frame=_city_ui_arithmetic_fields(state,frame,'target_y',2)
        frame,again=_command_panel_dbra_fields(frame,'count')
        if not again:return frame


def draw_officer_detail_view_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """BAEA: detail screen initialization and real child/header/layout progression."""
    frame=_city_ui_frame_fields(state,frame,0xBAEA)
    frame=_command_panel_status_fields(state,frame,0x2700)
    frame=_command_panel_pointer_fields(state,frame,'auxiliary',0xC00000)
    frame=_movement_move(state,frame,'target_x',1,16)
    frame=_movement_move(state,frame,'target_y',3,16)
    for target,token in ((0xBB26,0xBB00),(0x5204,0xBB04),(0x52C2,0xBB08),(0x55B0,0xBB0C)):
        frame=_campaign_ui_call_fields(state,frame,target,token)
    frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x208)
    for address in (0xFFFFF362,0xFFFFF36A,0xFFFFF394):frame=_city_ui_store_fields(state,frame,address,0,2,True)
    return _campaign_ui_call_fields(state,frame,0xAF48,0xBB24)


def append_officer_detail_rows_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """BB26: live menu descriptors select the real glyph run and exact row upload count."""
    frame=_city_ui_frame_fields(state,frame,0xBB26)
    frame=_movement_move(state,frame,'unit',31,16)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFD300)
    frame=_command_panel_fill_buffer_fields(state,frame,'roster','unit')
    frame=_movement_move(state,frame,'choice',state.read(0xFFFFF38C,2),16)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0x92878)
    frame=_command_panel_pointer_fields(state,frame,'controller',frame.candidates.long())
    frame=_city_ui_shift_fields(state,frame,'choice',1)
    frame=_movement_move(state,frame,'choice',frame.candidates.word(low16(frame.choice+4)),16)
    frame=first_replace(frame,controller=frame.controller.advance(s16(low16(frame.choice))))
    frame=_movement_move(state,frame,'choice',0,16)
    frame=_movement_move(state,frame,'choice',frame.controller.byte(1),8)
    frame=_city_ui_store_fields(state,frame,0xFFFFF380,low16(frame.choice))
    frame=_movement_compare(state,frame,low16(frame.choice),96,16)
    if not frame.status&1:return frame
    frame=_movement_move(state,frame,'offset_y',low16(frame.choice),16)
    frame=_city_ui_shift_fields(state,frame,'choice',1)
    frame=_city_ui_arithmetic_fields(state,frame,'choice',low16(frame.offset_y))
    frame=_city_ui_shift_fields(state,frame,'choice',1)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xBBA0)
    frame=_command_panel_pointer_fields(state,frame,'roster',frame.candidates.long(low16(frame.choice)))
    frame=_movement_move(state,frame,'count',frame.candidates.word(low16(frame.choice+4)),16)
    frame=_movement_move(state,frame,'choice',low16(frame.count),16)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD380)
    frame=_campaign_ui_call_fields(state,frame,0xAE8A,0xBB7E)
    frame=_city_ui_store_fields(state,frame,0xC00004,0x40200000,4)
    frame=_city_ui_store_fields(state,frame,0xFFFFF37E,0,2,True)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFD300)
    frame=_city_ui_arithmetic_fields(state,frame,'choice',1)
    frame=_command_panel_row_stride_fields(state,frame)
    frame=_city_ui_arithmetic_fields(state,frame,'choice',31)
    return _command_panel_upload_fields(state,frame,'roster','choice',frame.auxiliary.base)


def open_roster_selection_message_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C0B6: live indexed command BYTE, roster history and real sound handshake."""
    frame=_city_ui_frame_fields(state,frame,0xC0B6)
    frame=_city_ui_store_fields(state,frame,0xFFFFCFD2,8)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF388,2),16)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF384,2),16)
    frame=_city_ui_arithmetic_fields(state,frame,'target_y',1)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF386,2),16)
    if not frame.status&4:
        frame=_city_ui_arithmetic_fields(state,frame,'unit',1,True)
        while True:
            frame=_city_ui_arithmetic_fields(state,frame,'target_x',low16(frame.target_y))
            frame,again=_command_panel_dbra_fields(frame,'unit')
            if not again:break
    frame=_command_panel_pointer_fields(state,frame,'candidates',0x92878)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF38C,2),16)
    frame=_city_ui_shift_fields(state,frame,'target_y',1)
    frame=_command_panel_pointer_fields(state,frame,'controller',frame.candidates.long())
    frame=_movement_move(state,frame,'target_y',frame.candidates.word(low16(frame.target_y+4)),16)
    frame=first_replace(frame,controller=frame.controller.advance(s16(low16(frame.target_y))))
    frame=_movement_move(state,frame,'target_x',frame.controller.byte(low16(frame.target_x+2)),8)
    frame=_movement_compare(state,frame,low8(frame.target_x),255,8)
    if frame.status&4:return _command_panel_status_fields(state,frame,state.read_status_word()|1)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF576,2),16)
    frame=_command_panel_pointer_fields(state,frame,'scan',0xFFFFF578)
    frame=_city_ui_store_fields(state,frame,u32(frame.scan.base+s16(low16(frame.unit))),low8(frame.target_x),1)
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF576,1)
    frame=_city_ui_store_fields(state,frame,0xFFFFF38C,low16(frame.target_x))
    frame=_movement_move(state,frame,'target_x',0xAC,16)
    frame=_campaign_ui_call_fields(state,frame,0x808A,0xC110)
    return _command_panel_status_fields(state,frame,state.read_status_word()&65534)


def draw_force_relation_view_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C372: initialize the relation glyph plane and then require real scene refresh."""
    frame=_city_ui_frame_fields(state,frame,0xC372)
    frame=_command_panel_status_fields(state,frame,0x2700)
    frame=_command_panel_pointer_fields(state,frame,'auxiliary',0xC00000)
    frame=_movement_move(state,frame,'target_x',1,16)
    frame=_movement_move(state,frame,'target_y',3,16)
    frame=_movement_move(state,frame,'unit',31,16)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFD300)
    frame=_command_panel_fill_buffer_fields(state,frame,'roster','unit')
    frame=_command_panel_pointer_fields(state,frame,'roster',0x8A374)
    frame=_movement_move(state,frame,'count',5,16)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD380)
    frame=_campaign_ui_call_fields(state,frame,0xAE8A,0xC3AA)
    frame=_city_ui_store_fields(state,frame,0xC00004,0x40200000,4)
    frame=_city_ui_store_fields(state,frame,0xFFFFF37E,0,2,True)
    frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFD300)
    frame=_movement_move(state,frame,'choice',223,16)
    frame=_command_panel_upload_fields(state,frame,'roster','choice',frame.auxiliary.base)
    return _campaign_ui_call_fields(state,frame,0xAF48,0xC3CC)


def draw_command_cost_panel_frame_fields(state: SceneState, frame: FirstDeploymentFrame, entry: int=0xC8B8) -> FirstDeploymentFrame:
    """C8B8/CD20: true alternate setup and whole cost/name/portrait/message flow."""
    if entry not in (0xC8B8,0xCD20):raise ValueError('actual cost-panel entry required')
    frame=_city_ui_frame_fields(state,frame,entry)
    if entry==0xCD20:
        frame=_command_panel_status_fields(state,frame,0x2700)
        frame=_movement_move(state,frame,'target_x',1,16)
        frame=_movement_move(state,frame,'target_y',3,16)
        frame=_command_panel_glyph_fields(state,frame,0x8A430,3,0xCD40)
        frame=_city_ui_store_fields(state,frame,0xC00004,0x55A00000,4)
        frame=_command_panel_pointer_fields(state,frame,'roster',0xFFFFD300)
        frame=_movement_move(state,frame,'target_x',127,16)
        frame=_command_panel_upload_fields(state,frame,'roster','target_x',0xC00000)
        frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),0x36,16)
        if not frame.status&4:return _campaign_ui_call_fields(state,frame,0xAF48,0xCD70)
        # The original BRA reaches the primary body without a second return slot.
    frame=_command_panel_status_fields(state,frame,0x2700)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
    frame=_campaign_ui_call_fields(state,frame,0xCFEE,0xC8C4)
    frame=_movement_test(state,frame,state.read(0xFFFFE730,2),16)
    if frame.status&8:
        frame=_city_ui_store_fields(state,frame,0xFFFFF740,203)
        frame=_city_ui_store_fields(state,frame,0xFFFFF362,0,2,True)
        frame=_campaign_ui_call_fields(state,frame,0x30A74,0xC984)
        frame=_campaign_ui_call_fields(state,frame,0xC11E,0xC988)
        for address,value in ((0xFFFFF612,0x208),(0xFFFFF362,3),(0xFFFFF36A,18)):
            frame=_city_ui_store_fields(state,frame,address,value)
    else:
        frame=_movement_move(state,frame,'target_x',1,16)
        frame=_movement_move(state,frame,'target_y',3,16)
        frame=_city_ui_store_fields(state,frame,0xC00004,0x40A00000,4)
        frame=_command_panel_pointer_fields(state,frame,'scan',0xFFFFE730)
        frame=_command_panel_pointer_fields(state,frame,'controller',0xFFFFE640)
        frame=_movement_move(state,frame,'distance',0,16)
        while True:
            frame=_movement_move(state,frame,'choice',frame.scan.word(),16)
            frame=first_replace(frame,scan=frame.scan.advance(2))
            if frame.status&8:break
            frame=_city_ui_shift_fields(state,frame,'choice',1)
            frame=_movement_move(state,frame,'choice',frame.controller.word(low16(frame.choice)),16)
            frame=_command_panel_pointer_fields(state,frame,'roster',0x8A504)
            frame=_movement_move(state,frame,'offset_y',low16(frame.choice),16)
            frame=_city_ui_shift_fields(state,frame,'choice',1)
            frame=_city_ui_arithmetic_fields(state,frame,'choice',low16(frame.offset_y))
            frame=_city_ui_shift_fields(state,frame,'choice',1)
            frame=_command_panel_pointer_fields(state,frame,'roster',frame.roster.base+s16(low16(frame.choice)))
            frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
            frame=_movement_move(state,frame,'count',2,16)
            frame=_campaign_ui_call_fields(state,frame,0xAE8A,0xC914)
            frame=_movement_move(state,frame,'offset_x',95,16)
            frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
            frame=_command_panel_upload_fields(state,frame,'candidates','offset_x',0xC00000)
        frame=_city_ui_store_fields(state,frame,0xC00004,0x4E000003,4)
        frame=_command_panel_pointer_fields(state,frame,'controller',0xFFFFE640)
        frame=_command_panel_pointer_fields(state,frame,'scan',0xFFFFE730)
        frame=_movement_move(state,frame,'target_y',0,16)
        while True:
            frame=_movement_move(state,frame,'target_x',frame.scan.word(),16)
            frame=first_replace(frame,scan=frame.scan.advance(2))
            if frame.status&8:break
            frame=_city_ui_shift_fields(state,frame,'target_x',7)
            frame=_command_panel_pointer_fields(state,frame,'roster',0x94728+s16(low16(frame.target_x)))
            frame=_movement_move(state,frame,'target_x',31,16)
            frame=_command_panel_upload_fields(state,frame,'roster','target_x',0xC00000)
            frame=_city_ui_arithmetic_fields(state,frame,'target_y',1)
            # Retain the original live D7 counter, including the negative sentinel.
            frame,again=_command_panel_dbra_fields(frame,'choice')
            if not again:break
        frame=_city_ui_store_fields(state,frame,0xFFFFF3D8,low16(frame.target_y))
        frame=_movement_move(state,frame,'target_x',1,16)
        frame=_movement_move(state,frame,'target_y',3,16)
        frame=_campaign_ui_call_fields(state,frame,0x506C,0xC970)
    frame=_city_ui_store_fields(state,frame,0xFFFFF3DE,0,2,True)
    return _campaign_ui_call_fields(state,frame,0xAF48,0xC9A4)


def draw_command_cost_panel_alternate_1_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """CD20 is an actual alternate entry of the same indivisible cost-panel owner."""
    return draw_command_cost_panel_frame_fields(state,frame,0xCD20)


def draw_diplomacy_command_panel_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """DB20: diplomacy labels and borders, then the true selection and interaction children."""
    frame=_city_ui_frame_fields(state,frame,0xDB20)
    frame=_command_panel_status_fields(state,frame,0x2700)
    frame=_movement_move_long(state,frame,'unit',0x43180003)
    frame=_movement_move(state,frame,'target_x',3,16)
    while True:
        frame=_city_ui_store_fields(state,frame,0xC00004,frame.unit,4)
        frame=_movement_arithmetic_long(state,frame,'unit',0x800000)
        frame=_movement_move(state,frame,'target_y',7,16)
        frame=_command_panel_repeat_fields(state,frame,0xC00000,0,'target_y',4)
        frame,again=_command_panel_dbra_fields(frame,'target_x')
        if not again:break
    frame=_city_ui_store_fields(state,frame,0xC00004,0x40A00000,4)
    frame=_movement_move(state,frame,'target_x',7,16)
    frame=_command_panel_repeat_fields(state,frame,0xC00000,0x11111113,'target_x',4)
    frame=_command_panel_pointer_fields(state,frame,'roster',0x8A480)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'target_x',1,16)
    frame=_movement_move(state,frame,'target_y',3,16)
    frame=_movement_move(state,frame,'count',15,16)
    frame=_campaign_ui_call_fields(state,frame,0xAE8A,0xDB88)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'count',511,16)
    frame=_command_panel_upload_fields(state,frame,'candidates','count',0xC00000)
    frame=_command_panel_glyph_fields(state,frame,0x8A4A0,5,0xDBAE)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'count',191,16)
    frame=_command_panel_upload_fields(state,frame,'candidates','count',0xC00000)
    frame=_command_panel_pointer_fields(state,frame,'roster',0x8A48E)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'target_y',2,16)
    frame=_movement_move(state,frame,'count',14,16)
    frame=_campaign_ui_call_fields(state,frame,0xAE8A,0xDBD8)
    frame=_command_panel_pointer_fields(state,frame,'candidates',0xFFFFD300)
    frame=_movement_move(state,frame,'count',479,16)
    frame=_command_panel_upload_fields(state,frame,'candidates','count',0xC00000)
    frame=_command_panel_pointer_fields(state,frame,'auxiliary',0xC00004)
    frame=_command_panel_pointer_fields(state,frame,'scratch',0xC00000)
    frame=_city_ui_store_fields(state,frame,frame.auxiliary.base,0x42980003,4)
    frame=_city_ui_store_fields(state,frame,frame.scratch.base,0xC380)
    frame=_movement_move(state,frame,'target_x',7,16)
    frame=_command_panel_repeat_fields(state,frame,frame.scratch.base,0xC381C381,'target_x',4)
    frame=_city_ui_store_fields(state,frame,frame.scratch.base,0xCB80)
    frame=_movement_move_long(state,frame,'unit',0x43180003)
    for first_tile,last_tile in ((0xC006,0xC012),(0xC007,0xC013)):
        frame=_city_ui_store_fields(state,frame,frame.auxiliary.base,frame.unit,4)
        frame=_movement_arithmetic_long(state,frame,'unit',0x800000)
        frame=_city_ui_store_fields(state,frame,frame.scratch.base,0xC382)
        frame=_movement_move(state,frame,'target_x',5,16)
        frame=_movement_move(state,frame,'target_y',first_tile,16)
        while True:
            frame=_city_ui_store_fields(state,frame,frame.scratch.base,low16(frame.target_y))
            frame=_city_ui_arithmetic_fields(state,frame,'target_y',2)
            frame,again=_command_panel_dbra_fields(frame,'target_x')
            if not again:break
        for tile in (0xC005,0xC001):frame=_city_ui_store_fields(state,frame,frame.scratch.base,tile)
        frame=_movement_move(state,frame,'target_x',7,16)
        frame=_movement_move(state,frame,'target_y',last_tile,16)
        while True:
            frame=_city_ui_store_fields(state,frame,frame.scratch.base,low16(frame.target_y))
            frame=_city_ui_arithmetic_fields(state,frame,'target_y',2)
            frame,again=_command_panel_dbra_fields(frame,'target_x')
            if not again:break
        frame=_city_ui_store_fields(state,frame,frame.scratch.base,0xCB82)
    frame=_movement_move(state,frame,'target_y',8,16)
    while True:
        frame=_city_ui_store_fields(state,frame,frame.auxiliary.base,frame.unit,4)
        frame=_movement_arithmetic_long(state,frame,'unit',0x800000)
        frame=_city_ui_store_fields(state,frame,frame.scratch.base,0xC382)
        frame=_movement_move(state,frame,'target_x',2,16)
        frame=_command_panel_repeat_fields(state,frame,frame.scratch.base,0xC001C001,'target_x',4)
        frame=_city_ui_store_fields(state,frame,frame.scratch.base,0xC005)
        frame=_movement_move(state,frame,'target_x',3,16)
        frame=_command_panel_repeat_fields(state,frame,frame.scratch.base,0xC001C001,'target_x',4)
        frame=_city_ui_store_fields(state,frame,frame.scratch.base,0xC001CB82,4)
        frame,again=_command_panel_dbra_fields(frame,'target_y')
        if not again:break
    frame=_city_ui_store_fields(state,frame,frame.auxiliary.base,frame.unit,4)
    frame=_city_ui_store_fields(state,frame,frame.scratch.base,0xD380)
    frame=_movement_move(state,frame,'target_x',7,16)
    frame=_command_panel_repeat_fields(state,frame,frame.scratch.base,0xD381D381,'target_x',4)
    frame=_city_ui_store_fields(state,frame,frame.scratch.base,0xDB80)
    frame=_campaign_ui_call_fields(state,frame,0xDCF0,0xDCDE)
    frame=_movement_move(state,frame,'target_x',198,16)
    frame=_campaign_ui_call_fields(state,frame,0x676F2,0xDCE8)
    return _campaign_ui_call_fields(state,frame,0x60C,0xDCEE)


# C59 complete display/order ABI; historical algorithms are projections only.
"""One original diplomacy parameter owner with its two real entry aliases.

DF6E command-menu policy,30960 city turns and6701E message preparation
share named continuation phases. Actual indexed WORD targets remain live;
there is no generated PC loop, callback result, device ACK or prefix credit.
"""
from .contexts_display_fields import (
    display_frame_fields, display_move_fields, display_store_fields,
    display_address_fields, display_shift_word_fields, display_loop_fields,
    display_call_fields, display_child_fields, display_status_fields,
)


def _diplomacy_owner_matches_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> tuple[FirstDeploymentFrame, bool]:
    """Three ordered CMP.Ws stop immediately at the actual matching owner."""
    from .business_movement_support import _movement_compare
    for address in (0xFFFFF67A, 0xFFFFF67C, 0xFFFFF67E):
        frame = _movement_compare(state, frame, low16(frame.target_x), state.read(address, 2), 16)
        if frame.status & 4:
            return frame, True
    return frame, False


def _diplomacy_show_owner_packet_fields(state: SceneState,
        frame: FirstDeploymentFrame, second: bool) -> FirstDeploymentFrame:
    """The original309D2/30B80 sprite WORD packet and true AF48 tail."""
    frame = display_move_fields(state, frame, 'target_x', 0xC0000026, 32)
    frame = display_move_fields(state, frame, 'target_y', 7)
    frame = display_move_fields(state, frame, 'unit', 0xCA02)
    frame = display_address_fields(state, frame, 'roster', 0x309E0)
    frame = display_call_fields(state, frame, 0x26BFA, 0x30B86 if second else 0x309D8)
    return display_call_fields(state, frame, 0xAF48, 0x30B8C if second else 0x309DE)


def _diplomacy_first_force_turn_fields(state: SceneState,
        frame: FirstDeploymentFrame, prefix: bool) -> FirstDeploymentFrame:
    """30960/3096E: preserve the real player/non-player loop and two tails."""
    from .business_movement_support import _movement_compare
    frame = display_frame_fields(state, frame)
    if type(prefix) is not bool:
        raise ValueError('actual30960 or3096E entry required')
    if prefix:
        frame = _movement_compare(state, frame, state.read(0xFFFFF36C, 2), 2, 16)
        if not frame.status & 1:
            return _diplomacy_second_force_turn_fields(state, frame, True)
        frame = display_call_fields(state, frame, 0x30EB4, 0x3096E)
    while True:
        frame = display_call_fields(state, frame, 0x30F26, 0x30972)
        frame = display_move_fields(state, frame, 'target_x', state.read(0xFFFFF376, 2))
        if frame.status & 8:
            frame = display_call_fields(state, frame, 0x311E6, 0x309A6)
            return display_call_fields(state, frame, 0xAF48, 0x309DE)
        frame, owned = _diplomacy_owner_matches_fields(state, frame)
        if not owned:
            frame = display_store_fields(state, frame, 0x30992, 0xFFFFF362, 2)
            frame = display_call_fields(state, frame, 0x30A74, 0x3099C)
            frame = display_call_fields(state, frame, 0x30FAA, 0x309A0)
            continue
        frame = display_call_fields(state, frame, 0x309FC, 0x309AE)
        if frame.status & 1:
            continue
        frame = display_store_fields(state, frame, 0x309B0, 0xFFFFF612, 0x20B)
        frame = display_store_fields(state, frame, 0x309B6, 0xFFFFF362, 4)
        frame = display_store_fields(state, frame, 0x309BC, 0xFFFFF36C, 0, clear=True)
        return _diplomacy_show_owner_packet_fields(state, frame, False)


def _diplomacy_save_notice_fields(state: SceneState,
        frame: FirstDeploymentFrame, second: bool) -> FirstDeploymentFrame:
    """E098/30B2C ordered saved notices; no extra source RAM read."""
    frame = display_store_fields(state, frame, 0x30B2C if second else 0xE09C,
        0xFFFFF3C2, state.read(0xFFFFF612, 2))
    frame = display_store_fields(state, frame, 0x30B32 if second else 0xE0A2,
        0xFFFFF3C4, state.read(0xFFFFF362, 2))
    frame = display_store_fields(state, frame, 0x30B38 if second else 0xE0A8, 0xFFFFF612, 0x208)
    frame = display_store_fields(state, frame, 0x30B3E if second else 0xE0AE, 0xFFFFF362, 0x13)
    frame = display_store_fields(state, frame, 0x30B44 if second else 0xE0B4, 0xFFFFF36A, 0, clear=True)
    return frame


def _diplomacy_second_force_turn_fields(state: SceneState,
        frame: FirstDeploymentFrame, prefix: bool) -> FirstDeploymentFrame:
    """30ABE/30AC6: original second turn, fallback lookup and stock notices."""
    frame = display_frame_fields(state, frame)
    if type(prefix) is not bool:
        raise ValueError('actual30ABE or30AC6 entry required')
    if prefix:
        frame = display_store_fields(state, frame, 0x30ABE, 0xFFFFF724, 0, clear=True)
        frame = display_call_fields(state, frame, 0x30EB4, 0x30AC6)
    while True:
        frame = display_call_fields(state, frame, 0x30F26, 0x30ACA)
        frame = display_move_fields(state, frame, 'target_x', state.read(0xFFFFF376, 2))
        if frame.status & 8:
            frame = display_call_fields(state, frame, 0x311FA, 0x30B04)
            frame = display_call_fields(state, frame, 0x1631A, 0x30B0A)
            frame = display_store_fields(state, frame, 0x30B0A, 0xFFFFF612, 0x209)
            frame = display_store_fields(state, frame, 0x30B10, 0xFFFFF362, 5)
            frame = display_store_fields(state, frame, 0x30B16, 0xFFFFF36C, 3)
            frame = display_store_fields(state, frame, 0x30B1C, 0xFFFF9F00, 0xFFFF)
            frame = display_call_fields(state, frame, 0x30F54, 0x30B26)
            frame = display_call_fields(state, frame, 0x30C3A, 0x30B2A)
            frame = _diplomacy_save_notice_fields(state, frame, True)
            return display_call_fields(state, frame, 0xAF48, 0x30B8C)
        frame, owned = _diplomacy_owner_matches_fields(state, frame)
        if not owned:
            frame = display_store_fields(state, frame, 0x30AEA, 0xFFFFF362, 2)
            frame = display_call_fields(state, frame, 0x30A74, 0x30AF2)
            frame = display_call_fields(state, frame, 0x31024, 0x30AF6)
            frame = display_store_fields(state, frame, 0x30AF6, 0xFFFFF75A, 0, clear=True)
            frame = display_call_fields(state, frame, 0x31044, 0x30AFE)
            continue
        frame = display_store_fields(state, frame, 0x30B4C, 0xFFFFF612, 0x20B)
        frame = display_store_fields(state, frame, 0x30B52, 0xFFFFF362, 4)
        frame = display_call_fields(state, frame, 0x309FC, 0x30B5C)
        if frame.status & 1:
            frame = display_call_fields(state, frame, 0x30B8E, 0x30B64)
            if frame.status & 1:
                continue
        frame = display_store_fields(state, frame, 0x30B68, 0xFFFFF380, 0x85)
        return _diplomacy_show_owner_packet_fields(state, frame, True)


def _diplomacy_selected_category_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """E050..E0C4: live category WORD and original FE06-based indexed call."""
    from .business_movement_support import _movement_compare, _movement_test
    frame = display_move_fields(state, frame, 'target_x', state.read(0xFFFFF65A, 2))
    frame = _movement_compare(state, frame, low16(frame.target_x), 6, 16)
    if frame.status & 4:
        return _diplomacy_second_force_turn_fields(state, frame, False)
    frame = display_shift_word_fields(state, frame, 'target_x', 1)
    frame = display_move_fields(state, frame, 'target_x',
        state.read(u32(0xE0C4 + s16(low16(frame.target_x))), 2))
    frame = display_address_fields(state, frame, 'roster', 0xFE06)
    frame = display_call_fields(state, frame,
        u32(frame.roster.base + s16(low16(frame.target_x))), 0xE06C)
    frame = _movement_test(state, frame, state.read(0xFFFFF36C, 2), 16)
    if not frame.status & 4:
        frame = display_store_fields(state, frame, 0xE074, 0xFFFFF380, 0x85)
    frame = display_store_fields(state, frame, 0xE07A, 0xFFFFF65A, 0, clear=True)
    frame = _movement_compare(state, frame, state.read(0xFFFFF600, 2), 0x28, 16)
    if frame.status & 4:
        return display_child_fields(state, frame, 0x60C)
    frame = _movement_test(state, frame, state.read(0xFFFFF612, 2), 16)
    if frame.status & 4:
        frame = display_store_fields(state, frame, 0xE092, 0xFFFFF612, 0x201)
    frame = display_store_fields(state, frame, 0xE098, 0xFFFFF576, 0, clear=True)
    return _diplomacy_save_notice_fields(state, frame, False)


def draw_diplomacy_parameter_panel_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """DF6E normal entry: preserve full SR literal, true table and all tails."""
    from .business_movement_support import _movement_compare, _movement_binary_flags
    frame = display_frame_fields(state, frame)
    frame = display_status_fields(state, frame, 0x2700)
    frame = display_store_fields(state, frame, 0xDF72, 0xFFFFEF78, 0, clear=True)
    frame = display_store_fields(state, frame, 0xDF76, 0x00FF7026, 0xFFFF)
    frame = _movement_compare(state, frame, state.read(0xFFFFF36C, 2), 2, 16)
    if frame.status & 4:
        return _diplomacy_selected_category_fields(state, frame)
    frame = _movement_compare(state, frame, state.read(0xFFFFF36C, 2), 3, 16)
    if frame.status & 4:
        return _diplomacy_selected_category_fields(state, frame)
    frame = _movement_compare(state, frame, state.read(0xFFFFF65A, 2), 0x11, 16)
    if frame.status & 4:
        return _diplomacy_selected_category_fields(state, frame)
    for category in (6, 0xF, 0x15):
        frame = _movement_compare(state, frame, state.read(0xFFFFF579, 1), category, 8)
        if frame.status & 4:
            break
    else:
        frame = display_store_fields(state, frame, 0xDFBA, 0xFFFFF650, 1)
    frame = display_move_fields(state, frame, 'target_x', 0)
    frame = display_move_fields(state, frame, 'target_x', state.read(0xFFFFF579, 1), 8)
    frame, value = _movement_binary_flags(state, frame, low16(frame.target_x), 4, 16, True)
    frame = first_replace(frame, target_x=replace_word(frame.target_x, value))
    frame = display_shift_word_fields(state, frame, 'target_x', 1)
    frame = display_move_fields(state, frame, 'target_x',
        state.read(u32(0xE024 + s16(low16(frame.target_x))), 2))
    frame = display_address_fields(state, frame, 'roster', 0xE0EE)
    frame = display_call_fields(state, frame,
        u32(frame.roster.base + s16(low16(frame.target_x))), 0xDFD8)
    frame = display_call_fields(state, frame, 0x1406, 0xDFDE)
    if frame.status & 1:
        return draw_diplomacy_parameter_panel_alternate_2_frame_fields(state, frame)
    frame = _movement_compare(state, frame, state.read(0xFFFFF579, 1), 0xFF, 8)
    if frame.status & 4:
        return _diplomacy_first_force_turn_fields(state, frame, False)
    frame = _movement_compare(state, frame, state.read(0xFFFFF600, 2), 0x28, 16)
    if frame.status & 4:
        return display_child_fields(state, frame, 0x60C)
    frame = display_store_fields(state, frame, 0xDFFA, 0xFFFFF612, state.read(0xFFFFF38A, 2))
    frame = display_call_fields(state, frame, 0xC11E, 0xE006)
    frame = display_call_fields(state, frame, 0x133A, 0xE00C)
    return display_call_fields(state, frame, 0xAF48, 0xE022)


def draw_diplomacy_parameter_panel_alternate_1_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Actual30960 alias, not the DF6E prefix or a fabricated caller."""
    return _diplomacy_first_force_turn_fields(state, frame, True)


def draw_diplomacy_parameter_panel_alternate_2_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """6701E: both2048 LONG clear streams and actual selection/budget calls."""
    from .business_movement_support import _movement_compare, _movement_add_word
    frame = display_frame_fields(state, frame)
    frame = display_move_fields(state, frame, 'target_x', 0x7FF)
    frame = display_address_fields(state, frame, 'roster', 0x00FF7000)
    frame = display_address_fields(state, frame, 'candidates', 0xFFFF8000)
    while True:
        frame = display_store_fields(state, frame, 0x6702C, frame.roster.base, 0, 4, True)
        frame = first_replace(frame, roster=frame.roster.advance(4))
        frame = display_store_fields(state, frame, 0x6702E, frame.candidates.base, 0, 4, True)
        frame = first_replace(frame, candidates=frame.candidates.advance(4))
        frame, more = display_loop_fields(frame, 'target_x')
        if not more:
            break
    frame = display_call_fields(state, frame, 0x670B8, 0x67038)
    frame = display_store_fields(state, frame, 0x67038, 0xFFFFF740, 0x9D)
    frame = display_store_fields(state, frame, 0x6703E, 0xFFFFF362, 0, clear=True)
    frame = display_call_fields(state, frame, 0x30A74, 0x67048)
    frame = display_call_fields(state, frame, 0x67126, 0x6704C)
    frame = display_move_fields(state, frame, 'target_x', 0)
    frame = _movement_compare(state, frame, low16(frame.target_y), 0x50, 16)
    if frame.status & 1:
        frame = _movement_add_word(state, frame, 'target_x', 1)
        frame = _movement_compare(state, frame, low16(frame.target_y), 0x28, 16)
        if frame.status & 1:
            frame = _movement_add_word(state, frame, 'target_x', 1)
    frame = display_store_fields(state, frame, 0x67062, 0xFFFF80DA, low16(frame.target_x))
    frame = display_move_fields(state, frame, 'target_x', state.read(0xFFFFF376, 2))
    frame = display_shift_word_fields(state, frame, 'target_x', 1)
    frame = display_address_fields(state, frame, 'roster', 0xFFFFE640)
    frame = display_move_fields(state, frame, 'target_y',
        state.read(u32(frame.roster.base + s16(low16(frame.target_x))), 2))
    frame = display_store_fields(state, frame, 0x67076, 0xFFFF80DC, low16(frame.target_y))
    frame = display_store_fields(state, frame, 0x6707C, 0xFFFF80DE, low16(frame.target_y))
    frame = display_move_fields(state, frame, 'target_x', 0)
    frame = display_move_fields(state, frame, 'target_x', state.read(0xFFFFF374, 1), 8)
    frame = _movement_add_word(state, frame, 'target_x', 0xB8)
    frame = display_store_fields(state, frame, 0x6708C, 0xFFFF80E4, low16(frame.target_x))
    frame = display_move_fields(state, frame, 'target_x', state.read(0xFFFFF375, 1), 8)
    frame = _movement_add_word(state, frame, 'target_x', 1)
    frame = display_store_fields(state, frame, 0x67098, 0xFFFF80E6, low16(frame.target_x))
    frame = display_store_fields(state, frame, 0x6709E, 0xFFFF80E8, state.read(0xFFFFEFDC, 2))
    frame = display_store_fields(state, frame, 0x670A6, 0xFFFFF352, 0, clear=True)
    frame = display_store_fields(state, frame, 0x670AA, 0xFFFFF612, 0x20C)
    return display_store_fields(state, frame, 0x670B0, 0xFFFFF362, 8)
