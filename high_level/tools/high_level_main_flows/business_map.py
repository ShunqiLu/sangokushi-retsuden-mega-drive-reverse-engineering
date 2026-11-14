"""Structured map/menu/controller logic, mechanically drafted then reviewed.

No instruction decoder, PC state, code array, file reader or media payload is
used at runtime. Ordinary values, typed live views and structured conditionals
retain width/order quirks. This draft is not full CPU or natural-call proof.
"""
from .domain import SceneState, Boundary, u8, u16, u32, s8, s16, low8, low16, replace_byte, replace_word, swap_words, checked_state
from .services import call_target
from .contexts_map import (
    MapCoordinate,
    RestoreSceneDescriptorInput,
    RestoreSceneDescriptorResult,
    CopyTenSceneLongsInput,
    CopyTenSceneLongsResult,
    CopyFortySceneLongsInput,
    CopyFortySceneLongsResult,
    Copy128SceneLongsInput,
    Copy128SceneLongsResult,
    Copy64SceneLongsInput,
    Copy64SceneLongsResult,
    Copy256SceneLongsInput,
    Copy256SceneLongsResult,
    CopyTwentySceneLongsInput,
    CopyTwentySceneLongsResult,
    CopyEightSceneLongsInput,
    CopyEightSceneLongsResult,
    CopyScenePaletteLongsInput,
    CopyScenePaletteLongsResult,
    CopyRemainingPaletteLongsInput,
    CopyRemainingPaletteLongsResult,
    LocateCityAtWorldCursorInput,
    LocateCityAtWorldCursorResult,
    SelectPreviousCommandOfficerInput,
    SelectPreviousCommandOfficerResult,
    SelectNextCommandOfficerInput,
    SelectNextCommandOfficerResult,
    SelectNextCommandOfficerService1,
    SelectNextCommandOfficerService2,
    SelectNextCommandOfficerService3,
    SelectNextCommandOfficerService4,
    SelectNextCommandOfficerService5,
    SelectNextCommandOfficerService6,
    SelectNextCommandOfficerService7,
    SelectNextCommandOfficerService8,
    AdjustSelectedRosterMemberInput,
    AdjustSelectedRosterMemberResult,
    AdjustSelectedRosterMemberService1,
    AdjustSelectedRosterMemberService2,
    ScanRosterSelectionStatusInput,
    ScanRosterSelectionStatusResult,
    ScanCandidateRosterStatusInput,
    ScanCandidateRosterStatusResult,
    ClearOfficerGrowthFieldsInput,
    ClearOfficerGrowthFieldsResult,
    RefreshWorldMapScrollInput,
    RefreshWorldMapScrollResult,
    RefreshWorldMapScrollService1,
    RefreshWorldMapScrollService2,
    LocateMapObjectRecordInput,
    LocateMapObjectRecordResult,
    UpdateWorldCursorFromInputsInput,
    UpdateWorldCursorFromInputsResult,
    QueueMapStripTransferInput,
    QueueMapStripTransferResult,
    RefreshMapTilesAroundCursorInput,
    RefreshMapTilesAroundCursorResult,
    RefreshMapTilesAroundCursorService1,
    RefreshMapTilesAroundCursorService2,
    RefreshMapTilesAroundCursorService3,
    RefreshMapTilesAroundCursorService4,
    RenderMapColumnInput,
    RenderMapColumnResult,
    RenderMapRowInput,
    RenderMapRowResult,
    RefreshWorldCursorAttributesInput,
    RefreshWorldCursorAttributesResult,
    RefreshWorldCursorAttributesAlternate1Input,
    RefreshWorldCursorAttributesAlternate1Result,
    WorldCursorRefreshFields,
    InitializeWorldMapViewInput,
    InitializeWorldMapViewResult,
    InitializeWorldMapViewService1,
    RenderInitialMapRowsInput,
    RenderInitialMapRowsResult,
    ReadWorldMapTileInput,
    ReadWorldMapTileResult,
    ReadMapCellWordInput,
    ReadMapCellWordResult,
    ReadInitialMapColumnInput,
    ReadInitialMapColumnResult,
    ReadWrappedMapColumnInput,
    ReadWrappedMapColumnResult,
    AdvanceMapColumnSourceInput,
    AdvanceMapColumnSourceResult,
    ResolveMapColumnPacketInput,
    ResolveMapColumnPacketResult,
    AdvanceMapColumnSkipInput,
    AdvanceMapColumnSkipResult,
)

from .contexts_map import CommandOfficerSelectionFields

def restore_scene_descriptor(state: SceneState, inputs: RestoreSceneDescriptorInput) -> RestoreSceneDescriptorResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not RestoreSceneDescriptorInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field)
    returned=restore_scene_descriptor_fields(state,entered)
    return RestoreSceneDescriptorResult(destination=returned.candidates,source=returned.roster,descriptor=returned.controller,value=returned.target_x,field=returned.target_y,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def copy_ten_scene_longs(state: SceneState, inputs: CopyTenSceneLongsInput) -> CopyTenSceneLongsResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not CopyTenSceneLongsInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=inputs.destination,roster=inputs.source,target_x=inputs.value)
    returned=copy_ten_scene_longs_fields(state,entered)
    return CopyTenSceneLongsResult(destination=returned.candidates,source=returned.roster,value=returned.target_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def copy_forty_scene_longs(state: SceneState, inputs: CopyFortySceneLongsInput) -> CopyFortySceneLongsResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not CopyFortySceneLongsInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=inputs.destination,roster=inputs.source,target_x=inputs.value)
    returned=copy_forty_scene_longs_fields(state,entered)
    return CopyFortySceneLongsResult(destination=returned.candidates,source=returned.roster,value=returned.target_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def copy_128_scene_longs(state: SceneState, inputs: Copy128SceneLongsInput) -> Copy128SceneLongsResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not Copy128SceneLongsInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=inputs.destination,roster=inputs.source,target_x=inputs.value)
    returned=copy_128_scene_longs_fields(state,entered)
    return Copy128SceneLongsResult(destination=returned.candidates,source=returned.roster,value=returned.target_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def copy_64_scene_longs(state: SceneState, inputs: Copy64SceneLongsInput) -> Copy64SceneLongsResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not Copy64SceneLongsInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=inputs.destination,roster=inputs.source,target_x=inputs.value)
    returned=copy_64_scene_longs_fields(state,entered)
    return Copy64SceneLongsResult(destination=returned.candidates,source=returned.roster,value=returned.target_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def copy_256_scene_longs(state: SceneState, inputs: Copy256SceneLongsInput) -> Copy256SceneLongsResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not Copy256SceneLongsInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=inputs.destination,roster=inputs.source,target_x=inputs.value)
    returned=copy_256_scene_longs_fields(state,entered)
    return Copy256SceneLongsResult(destination=returned.candidates,source=returned.roster,value=returned.target_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def copy_twenty_scene_longs(state: SceneState, inputs: CopyTwentySceneLongsInput) -> CopyTwentySceneLongsResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not CopyTwentySceneLongsInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=inputs.destination,roster=inputs.source,target_x=inputs.value)
    returned=copy_twenty_scene_longs_fields(state,entered)
    return CopyTwentySceneLongsResult(destination=returned.candidates,source=returned.roster,value=returned.target_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def copy_eight_scene_longs(state: SceneState, inputs: CopyEightSceneLongsInput) -> CopyEightSceneLongsResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not CopyEightSceneLongsInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=inputs.destination,roster=inputs.source,target_x=inputs.value)
    returned=copy_eight_scene_longs_fields(state,entered)
    return CopyEightSceneLongsResult(destination=returned.candidates,source=returned.roster,value=returned.target_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def copy_scene_palette_longs(state: SceneState, inputs: CopyScenePaletteLongsInput) -> CopyScenePaletteLongsResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not CopyScenePaletteLongsInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=inputs.destination,roster=inputs.source,target_x=inputs.value)
    returned=copy_scene_palette_longs_fields(state,entered)
    return CopyScenePaletteLongsResult(destination=returned.candidates,source=returned.roster,value=returned.target_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def copy_remaining_palette_longs(state: SceneState, inputs: CopyRemainingPaletteLongsInput) -> CopyRemainingPaletteLongsResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not CopyRemainingPaletteLongsInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=inputs.destination,roster=inputs.source,target_x=inputs.value,target_y=inputs.field)
    returned=copy_remaining_palette_longs_fields(state,entered)
    return CopyRemainingPaletteLongsResult(destination=returned.candidates,source=returned.roster,value=returned.target_x,field=returned.target_y,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def locate_city_at_world_cursor(state: SceneState, inputs: LocateCityAtWorldCursorInput) -> LocateCityAtWorldCursorResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not LocateCityAtWorldCursorInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit)
    returned=locate_city_at_world_cursor_fields(state,entered)
    return LocateCityAtWorldCursorResult(destination=returned.roster,value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def select_previous_command_officer(state: SceneState, inputs: SelectPreviousCommandOfficerInput) -> SelectPreviousCommandOfficerResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not SelectPreviousCommandOfficerInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,offset_y=inputs.member,choice=inputs.remaining)
    returned=select_previous_command_officer_frame_fields(state,entered)
    return SelectPreviousCommandOfficerResult(destination=state.table_at(returned.roster.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,member=returned.offset_y,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def select_next_command_officer(state: SceneState, inputs: SelectNextCommandOfficerInput) -> SelectNextCommandOfficerResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not SelectNextCommandOfficerInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,choice=inputs.remaining,stack_cursor=inputs.stack_cursor)
    returned=select_next_command_officer_frame_fields(state,entered)
    return SelectNextCommandOfficerResult(destination=state.table_at(returned.roster.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)




def _command_officer_message_fields(state, value):
    """Consume the unique 676F2 WORD transaction, never guessed high halves."""
    from .services import prepare_scene_message_fields
    message = prepare_scene_message_fields(state, value)
    if message.resolved is None:
        return value, None, None, None, message.carry, message.zero, message.negative, message.overflow
    return message.layout_offset, message.resolved.item_offset, state.table_at(message.resolved.pointer), state.table_at(message.resolved.descriptor), message.carry, message.zero, message.negative, message.overflow


def _call_command_officer_force_commands(state, retained, value):
    """6222 actual current carriers and known 6228 JSR return slot.

    A SceneTick does not supply these inputs. No initial snapshot, fake stack,
    or zero-filled C3CE call is substituted when they are absent.
    """
    if retained is None or retained.stack_cursor is None:
        raise Boundary('6222 C3CE requires actual retained D0/D1/D7 and 6198 entry SP')
    from .business_commands import append_force_relation_commands
    from .contexts_commands import AppendForceRelationCommandsInput
    called_stack = retained.stack_cursor.advance(-4)
    state.write(called_stack.base, 4, 0x6228)
    result = append_force_relation_commands(state, AppendForceRelationCommandsInput(
        replace_word(retained.value, value), retained.field, retained.remaining, called_stack))
    result.validate(state)
    if result.stack_cursor.long() != 0x6228:
        raise Boundary('modified original 6222 force-command return slot')
    if result.stack_cursor.base != called_stack.base:
        raise Boundary('unexpected force-command entry-SP return')
    return SelectNextCommandOfficerResult(result.destination, result.value, result.field,
        result.tile, retained.row, result.remaining, result.carry, result.zero,
        result.negative, result.overflow).validate(state)



def _command_officer_equipment_memory(state, retained):
    """6198 genuine captured entry A7, or explicitly unobserved legacy stack."""
    from .services import EquipmentMenuMemory
    return EquipmentMenuMemory(state, None if retained is None else retained.stack_cursor)


def select_next_command_officer_fields(state: SceneState, retained: SelectNextCommandOfficerInput | None=None) -> CommandOfficerSelectionFields:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if retained is not None:
        if type(retained) is not SelectNextCommandOfficerInput:
            raise ValueError("actual historical officer input required")
        retained.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=None if retained is None else retained.destination.cursor(),target_x=None if retained is None else retained.value,target_y=None if retained is None else retained.field,unit=None if retained is None else retained.tile,count=None if retained is None else retained.row,choice=None if retained is None else retained.remaining,stack_cursor=None if retained is None else retained.stack_cursor)
    returned=select_next_command_officer_frame_fields(state,entered)
    return CommandOfficerSelectionFields(destination_if_written=state.table_at(returned.roster.base),source_if_written=state.table_at(returned.candidates.base),value_if_written=low16(returned.target_x),field_if_written=low16(returned.target_y),tile_if_written=low16(returned.unit),row_if_written=low16(returned.count),remaining_if_written=low16(returned.choice),retained_after_call=None,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2),full_value_basis=returned.target_x).validate(state)


def adjust_selected_roster_member(state: SceneState, inputs: AdjustSelectedRosterMemberInput) -> AdjustSelectedRosterMemberResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not AdjustSelectedRosterMemberInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),candidates=inputs.source .cursor(),controller=inputs.descriptor,scan=inputs.records .cursor(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit,offset_y=inputs.member,choice=inputs.remaining)
    returned=adjust_selected_roster_member_frame_fields(state,entered)
    return AdjustSelectedRosterMemberResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),descriptor=state.table_at(returned.controller.base),records=state.table_at(returned.scan.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,member=returned.offset_y,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def scan_roster_selection_status(state: SceneState, inputs: ScanRosterSelectionStatusInput) -> ScanRosterSelectionStatusResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not ScanRosterSelectionStatusInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row)
    returned=scan_roster_selection_status_fields(state,entered)
    return ScanRosterSelectionStatusResult(value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def scan_candidate_roster_status(state: SceneState, inputs: ScanCandidateRosterStatusInput) -> ScanCandidateRosterStatusResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not ScanCandidateRosterStatusInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field)
    returned=scan_candidate_roster_status_fields(state,entered)
    return ScanCandidateRosterStatusResult(destination=returned.roster,value=returned.target_x,field=returned.target_y,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def clear_officer_growth_fields(state: SceneState, inputs: ClearOfficerGrowthFieldsInput) -> ClearOfficerGrowthFieldsResult:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    from .contexts_display_fields import display_legacy_frame_fields
    entered = display_legacy_frame_fields(state, inputs, 37776)
    return clear_officer_growth_frame_fields(state, entered)

def refresh_world_map_scroll(state: SceneState, inputs: RefreshWorldMapScrollInput) -> RefreshWorldMapScrollResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not RefreshWorldMapScrollInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit)
    returned=refresh_world_map_scroll_frame_fields(state,entered)
    return RefreshWorldMapScrollResult(destination=state.table_at(returned.roster.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def locate_map_object_record(state: SceneState, inputs: LocateMapObjectRecordInput) -> LocateMapObjectRecordResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not LocateMapObjectRecordInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row)
    returned=locate_map_object_record_fields(state,entered)
    return LocateMapObjectRecordResult(destination=returned.roster,value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def update_world_cursor_from_inputs(state: SceneState, inputs: UpdateWorldCursorFromInputsInput) -> UpdateWorldCursorFromInputsResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not UpdateWorldCursorFromInputsInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),candidates=inputs.source .cursor(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile)
    returned=update_world_cursor_from_inputs_frame_fields(state,entered)
    return UpdateWorldCursorFromInputsResult(destination=state.table_at(returned.roster.base),source=state.table_at(returned.candidates.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def queue_map_strip_transfer(state: SceneState, inputs: QueueMapStripTransferInput) -> QueueMapStripTransferResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not QueueMapStripTransferInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=inputs.source,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile)
    returned=queue_map_strip_transfer_fields(state,entered)
    return QueueMapStripTransferResult(destination=returned.roster,source=returned.candidates,value=returned.target_x,field=returned.target_y,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def refresh_map_tiles_around_cursor(state: SceneState, inputs: RefreshMapTilesAroundCursorInput) -> RefreshMapTilesAroundCursorResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not RefreshMapTilesAroundCursorInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),scratch=state.table_at(inputs.roster.base),target_x=inputs.value,target_y=inputs.field,distance=inputs.offset,offset_x=inputs.limit,offset_y=inputs.member,stack_cursor=inputs.stack_cursor)
    returned=refresh_map_tiles_around_cursor_fields(state,entered)
    return RefreshMapTilesAroundCursorResult(roster=returned.scratch,value=returned.target_x,field=returned.target_y,offset=returned.distance,limit=returned.offset_x,member=returned.offset_y,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def render_map_column(state: SceneState, inputs: RenderMapColumnInput) -> RenderMapColumnResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not RenderMapColumnInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),scratch=state.table_at(inputs.roster.base),target_x=inputs.value,target_y=inputs.field,distance=inputs.offset,offset_x=inputs.limit,offset_y=inputs.member,stack_cursor=inputs.stack_cursor)
    returned=render_map_column_fields(state,entered)
    return RenderMapColumnResult(destination=returned.roster,source=returned.candidates,descriptor=returned.controller,records=returned.scan,palette=returned.opponent,roster=returned.scratch,value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,member=returned.offset_y,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def render_map_row(state: SceneState, inputs: RenderMapRowInput) -> RenderMapRowResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not RenderMapRowInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),scratch=state.table_at(inputs.roster.base),target_x=inputs.value,target_y=inputs.field,distance=inputs.offset,offset_x=inputs.limit,offset_y=inputs.member,stack_cursor=inputs.stack_cursor)
    returned=render_map_row_fields(state,entered)
    return RenderMapRowResult(destination=returned.roster,source=returned.candidates,descriptor=returned.controller,records=returned.scan,palette=returned.opponent,roster=returned.scratch,value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,member=returned.offset_y,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def refresh_world_cursor_attributes(state: SceneState, inputs: RefreshWorldCursorAttributesInput) -> RefreshWorldCursorAttributesResult:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not RefreshWorldCursorAttributesInput:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile)
    returned=refresh_world_cursor_attributes_frame_fields(state,entered)
    return RefreshWorldCursorAttributesResult(destination=state.table_at(returned.roster.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def refresh_world_cursor_attributes_alternate_1(state: SceneState, inputs: RefreshWorldCursorAttributesAlternate1Input) -> RefreshWorldCursorAttributesAlternate1Result:
    """Historical observations project the one complete core; missing SR-X/A6/SP is not invented."""
    checked_state(state)
    if type(inputs) is not RefreshWorldCursorAttributesAlternate1Input:
        raise ValueError("function-specific historical input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination .cursor(),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile)
    returned=refresh_world_cursor_attributes_alternate_1_frame_fields(state,entered)
    return RefreshWorldCursorAttributesAlternate1Result(destination=state.table_at(returned.roster.base),value=returned.target_x,field=returned.target_y,tile=returned.unit,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def initialize_world_map_view(state: SceneState, inputs: InitializeWorldMapViewInput) -> InitializeWorldMapViewResult:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    from .contexts_display_fields import display_legacy_frame_fields
    entered = display_legacy_frame_fields(state, inputs, 41394)
    return initialize_world_map_view_frame_fields(state, entered)

def render_initial_map_rows(state: SceneState, inputs: RenderInitialMapRowsInput) -> RenderInitialMapRowsResult:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    from .contexts_display_fields import display_legacy_frame_fields
    entered = display_legacy_frame_fields(state, inputs, 41592)
    return render_initial_map_rows_frame_fields(state, entered)

def read_world_map_tile(state: SceneState, inputs: ReadWorldMapTileInput) -> ReadWorldMapTileResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not ReadWorldMapTileInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,scratch=state.table_at(inputs.roster.base),target_x=inputs.value,target_y=inputs.field,distance=inputs.offset,offset_x=inputs.limit,stack_cursor=inputs.stack_cursor)
    returned=read_world_map_tile_fields(state,entered)
    return ReadWorldMapTileResult(source=returned.candidates,descriptor=returned.controller,records=returned.scan,palette=returned.opponent,roster=returned.scratch,value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,offset=returned.distance,limit=returned.offset_x,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def read_map_cell_word(state: SceneState, inputs: ReadMapCellWordInput) -> ReadMapCellWordResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not ReadMapCellWordInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=inputs.value,target_y=inputs.field)
    returned=read_map_cell_word_fields(state,entered)
    return ReadMapCellWordResult(value=returned.target_x,field=returned.target_y,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def read_initial_map_column(state: SceneState, inputs: ReadInitialMapColumnInput) -> ReadInitialMapColumnResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not ReadInitialMapColumnInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,candidates=inputs.source,controller=inputs.descriptor,scan=inputs.records,scratch=state.table_at(inputs.roster.base),target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,offset_x=inputs.limit,offset_y=inputs.member,stack_cursor=inputs.stack_cursor)
    returned=read_initial_map_column_fields(state,entered)
    return ReadInitialMapColumnResult(destination=returned.roster,source=returned.candidates,descriptor=returned.controller,records=returned.scan,palette=returned.opponent,value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,member=returned.offset_y,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def read_wrapped_map_column(state: SceneState, inputs: ReadWrappedMapColumnInput) -> ReadWrappedMapColumnResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not ReadWrappedMapColumnInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,candidates=inputs.source,controller=inputs.descriptor,scan=inputs.records,target_x=inputs.value,target_y=inputs.field,unit=inputs.tile,count=inputs.row,distance=inputs.offset,offset_x=inputs.limit,offset_y=inputs.member,stack_cursor=inputs.stack_cursor)
    returned=read_wrapped_map_column_fields(state,entered)
    return ReadWrappedMapColumnResult(destination=returned.roster,source=returned.candidates,descriptor=returned.controller,palette=returned.opponent,value=returned.target_x,field=returned.target_y,tile=returned.unit,row=returned.count,member=returned.offset_y,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def advance_map_column_source(state: SceneState, inputs: AdvanceMapColumnSourceInput) -> AdvanceMapColumnSourceResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not AdvanceMapColumnSourceInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),roster=inputs.destination,candidates=inputs.source,target_x=inputs.value,unit=inputs.tile,count=inputs.row,offset_x=inputs.limit,offset_y=inputs.member,stack_cursor=inputs.stack_cursor)
    returned=advance_map_column_source_fields(state,entered)
    return AdvanceMapColumnSourceResult(destination=returned.roster,palette=returned.opponent,value=returned.target_x,tile=returned.unit,member=returned.offset_y,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def resolve_map_column_packet(state: SceneState, inputs: ResolveMapColumnPacketInput) -> ResolveMapColumnPacketResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not ResolveMapColumnPacketInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),opponent=inputs.palette,target_x=inputs.value,count=inputs.row,offset_x=inputs.limit,offset_y=inputs.member,stack_cursor=inputs.stack_cursor)
    returned=resolve_map_column_packet_fields(state,entered)
    return ResolveMapColumnPacketResult(palette=returned.opponent,value=returned.target_x,row=returned.count,member=returned.offset_y,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)

def advance_map_column_skip(state: SceneState, inputs: AdvanceMapColumnSkipInput) -> AdvanceMapColumnSkipResult:
    """Historical observations project this sole full-field core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not AdvanceMapColumnSkipInput:
        raise ValueError("function-specific typed input required")
    inputs.validate(state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),candidates=inputs.source,opponent=inputs.palette,offset_y=inputs.member)
    returned=advance_map_column_skip_fields(state,entered)
    return AdvanceMapColumnSkipResult(palette=returned.opponent,member=returned.offset_y,remaining=returned.choice,carry=bool(returned.status&1),zero=bool(returned.status&4),negative=bool(returned.status&8),overflow=bool(returned.status&2)).validate(state)


def _world_cursor_owner_comparison(selected: int, compared: int) -> WorldCursorRefreshFields:
    """The already-read unsigned CMP.W, without another live RAM access."""
    difference = u16(selected - compared)
    return WorldCursorRefreshFields(None, selected, None, None,
        selected < compared, difference == 0, bool(difference & 32768),
        bool(((selected ^ compared) & (selected ^ difference)) & 32768))


def refresh_world_cursor_attribute_fields(state: SceneState) -> WorldCursorRefreshFields:
    """A158: first owning-force match, then one real AC10 sprite transaction."""
    checked_state(state)
    selected = state.read(0xFFFFF376, 2)
    for address in (0xFFFFF67A, 0xFFFFF67C, 0xFFFFF67E):
        compared = state.read(address, 2)
        comparison = _world_cursor_owner_comparison(selected, compared)
        if comparison.zero:
            break
    else:
        return comparison.validate(state)
    source = state.table_at(0xA198).cursor()
    # Original A178 NOP only consumes timing; it performs no RAM operation.
    x = state.read(0xFFFFF35E, 2)
    y = state.read(0xFFFFF360, 2)
    attributes = 0
    scroll_x = state.read(0xFFFFF314, 2)
    state.write(0xFFFFF60A, 2, scroll_x)
    scroll_y = state.read(0xFFFFF318, 2)
    state.write(0xFFFFF60E, 2, scroll_y)
    from .reuse_display import append_map_sprite_fields
    sprite = append_map_sprite_fields(state, source, x, y, attributes,
        reset_scroll=False, initialize_clip=True).validate(state)
    return WorldCursorRefreshFields(sprite.source, sprite.x, sprite.y,
        sprite.attributes, sprite.carry, sprite.zero, sprite.negative,
        sprite.overflow).validate(state)

from .contexts_gameplay import (
    FirstDeploymentFrame, FirstDeploymentReturnBoundary, MovementContinuationBoundary, first_replace,
)
from .business_movement_support import (
    _movement_frame, _movement_move, _movement_move_long, _movement_test,
    _movement_test_long, _movement_compare, _movement_compare_address,
    _movement_binary_flags, _movement_fixed_shift_word, _movement_multiply_word,
    _movement_divu_word, _movement_save_longs, _movement_restore_longs,
)


def _world_map_frame_fields(state: SceneState, frame: FirstDeploymentFrame,
        entry: int) -> FirstDeploymentFrame:
    """Require actual full fields; historical omissions remain honest boundaries."""
    checked_state(state)
    if type(frame) is not FirstDeploymentFrame:
        raise ValueError('actual complete world-map fields required')
    values=(frame.target_x,frame.target_y,frame.unit,frame.count,frame.distance,
        frame.offset_x,frame.offset_y,frame.choice,frame.roster,frame.candidates,
        frame.controller,frame.scan,frame.opponent,frame.scratch,frame.auxiliary,
        frame.stack_cursor,frame.status)
    if any(value is None for value in values):
        raise MovementContinuationBoundary(entry,frame,'historical map observations lack the actual complete entry ABI')
    return _movement_frame(state,frame)


def _world_map_store_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, size: int, value: int, clear: bool=False) -> FirstDeploymentFrame:
    """One actual RAM MOVE/CLR; CLR performs its original prior read."""
    if size not in (1,2,4) or type(clear) is not bool:
        raise ValueError('actual map RAM store width required')
    if clear:
        state.read(address,size)
        value=0
    state.write(address,size,value)
    if size==4:
        return _movement_test_long(state,frame,value)
    return _movement_test(state,frame,value,size*8)


def _world_map_arithmetic_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, source: int, subtract: bool=False) -> FirstDeploymentFrame:
    """WORD arithmetic delegates to the existing sole fixed-width flag core."""
    frame,value=_movement_binary_flags(state,frame,low16(frame.carrier(name)),low16(source),16,subtract)
    return first_replace(frame,**{name:replace_word(frame.carrier(name),value)})


def _world_map_shift_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, amount: int, right: bool=False) -> FirstDeploymentFrame:
    """Reuse actual logical shifts, including the existing closed #7 bridge."""
    if amount==7:
        from ..high_level_remaining_flows.business_city import _duel_commit_shift_fields
        return _duel_commit_shift_fields(state,frame,name,amount,right)
    return _movement_fixed_shift_word(state,frame,name,amount,right)


def _world_map_bit_fields(state: SceneState, frame: FirstDeploymentFrame,
        value: int, bit: int) -> FirstDeploymentFrame:
    """Register BTST/BSET/BCLR only update Z, preserving the other CCR bits."""
    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
    from ..high_level_scene_flows.business_scene import _scene_render_bit
    return _scene_render_bit(SceneRefreshMemory(state),frame,value,1<<bit)


def _world_map_child_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Closed map children own one real outer LONG and consume its live return."""
    stack=frame.stack_cursor.advance(-4)
    stack.set_long(0,continuation)
    entered=first_replace(frame,stack_cursor=stack)
    if target==0x4026:
        returned=copy_ten_scene_longs_fields(state,entered)
    elif target==0x4032:
        returned=copy_forty_scene_longs_fields(state,entered)
    elif target==0x403E:
        returned=copy_128_scene_longs_fields(state,entered)
    elif target==0x404A:
        returned=copy_64_scene_longs_fields(state,entered)
    elif target==0x4056:
        returned=copy_256_scene_longs_fields(state,entered)
    elif target==0x4062:
        returned=copy_twenty_scene_longs_fields(state,entered)
    elif target==0x406E:
        returned=copy_eight_scene_longs_fields(state,entered)
    elif target==0x407A:
        returned=copy_scene_palette_longs_fields(state,entered)
    elif target==0x4096:
        returned=copy_remaining_palette_longs_fields(state,entered)
    elif target==0xA0CC:
        returned=render_map_column_fields(state,entered)
    elif target==0xA10C:
        returned=render_map_row_fields(state,entered)
    elif target==0xAF6A:
        returned=read_world_map_tile_fields(state,entered)
    elif target==0xB054:
        returned=read_map_cell_word_fields(state,entered)
    elif target==0xB06E:
        returned=read_initial_map_column_fields(state,entered)
    elif target==0xB0B2:
        returned=read_wrapped_map_column_fields(state,entered)
    elif target==0xB0DE:
        returned=advance_map_column_source_fields(state,entered)
    elif target==0xB106:
        returned=resolve_map_column_packet_fields(state,entered)
    elif target==0xB1DA:
        returned=advance_map_column_skip_fields(state,entered)
    else:
        raise MovementContinuationBoundary(target,entered,'no fabricated map child ABI')
    returned=_world_map_frame_fields(state,returned,target)
    actual=returned.stack_cursor.long()
    if actual!=continuation:
        raise FirstDeploymentReturnBoundary(actual,returned,continuation)
    return first_replace(returned,stack_cursor=returned.stack_cursor.advance(4))


def _world_map_copy_longs_fields(state: SceneState, frame: FirstDeploymentFrame,
        last_index: int) -> FirstDeploymentFrame:
    """One shared original DBRA copy; both postincrement addresses remain live."""
    frame=_movement_move(state,frame,'target_x',last_index,16)
    while True:
        value=frame.roster.long()
        frame=first_replace(frame,roster=frame.roster.advance(4))
        frame=_world_map_store_fields(state,frame,frame.candidates.base,4,value)
        frame=first_replace(frame,candidates=frame.candidates.advance(4),
            target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
        if low16(frame.target_x)==65535:
            return frame


def copy_ten_scene_longs_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4026: exactly ten ordered LONG copies."""
    return _world_map_copy_longs_fields(state,_world_map_frame_fields(state,frame,0x4026),9)


def copy_forty_scene_longs_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4032: exactly forty ordered LONG copies."""
    return _world_map_copy_longs_fields(state,_world_map_frame_fields(state,frame,0x4032),39)


def copy_128_scene_longs_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """403E: exactly 128 ordered LONG copies."""
    return _world_map_copy_longs_fields(state,_world_map_frame_fields(state,frame,0x403E),127)


def copy_64_scene_longs_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """404A: exactly 64 ordered LONG copies."""
    return _world_map_copy_longs_fields(state,_world_map_frame_fields(state,frame,0x404A),63)


def copy_256_scene_longs_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4056: exactly 256 ordered LONG copies."""
    return _world_map_copy_longs_fields(state,_world_map_frame_fields(state,frame,0x4056),255)


def copy_twenty_scene_longs_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4062: exactly twenty ordered LONG copies."""
    return _world_map_copy_longs_fields(state,_world_map_frame_fields(state,frame,0x4062),19)


def copy_eight_scene_longs_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """406E: exactly eight ordered LONG copies."""
    return _world_map_copy_longs_fields(state,_world_map_frame_fields(state,frame,0x406E),7)


def copy_scene_palette_longs_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """407A: reorder 256 three-byte records; the original addresses advance by 3."""
    frame=_world_map_frame_fields(state,frame,0x407A)
    frame=_movement_move(state,frame,'target_x',255,16)
    while True:
        for source_offset,destination_offset in ((1,0),(0,1),(2,2)):
            value=frame.roster.byte(0,source_offset)
            frame=_world_map_store_fields(state,frame,u32(frame.candidates.base+destination_offset),1,value)
        frame=first_replace(frame,roster=frame.roster.advance(3),candidates=frame.candidates.advance(3),
            target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
        if low16(frame.target_x)==65535:
            return frame


# confirmed source operation (recovered_code.s, 0x4096 and the F000 descriptor):
# restore 256 source WORDs into the F000 BYTE column. The retained historical
# "palette"/"longs" names do not confirm a palette or a formal attribute role.
# FFFF skips the subtraction and stores low BYTE FF; every other WORD first
# subtracts B8 with the original WORD arithmetic, then stores only its low BYTE.
# Keep the source WORDs, sentinel and truncation; do not normalize their values.
def copy_remaining_palette_longs_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4096: convert 256 WORD palette entries; FFFF retains its low BYTE."""
    frame=_world_map_frame_fields(state,frame,0x4096)
    frame=_movement_move(state,frame,'target_x',255,16)
    while True:
        value=frame.roster.word()
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_movement_move(state,frame,'target_y',value,16)
        frame=_movement_compare(state,frame,low16(frame.target_y),65535,16)
        if not frame.status&4:
            frame=_world_map_arithmetic_fields(state,frame,'target_y',184,True)
        frame=_world_map_store_fields(state,frame,frame.candidates.base,1,low8(frame.target_y))
        frame=first_replace(frame,candidates=frame.candidates.advance(1),
            target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
        if low16(frame.target_x)==65535:
            return frame


def _world_map_restore_region_fields(state: SceneState, frame: FirstDeploymentFrame,
        offset: int, destination: int, target: int, continuation: int) -> FirstDeploymentFrame:
    """One descriptor pointer is reread immediately before its real copy call."""
    frame=first_replace(frame,roster=state.table_at(frame.controller.long(offset)).cursor(),
        candidates=state.table_at(u32(0xFFFF0000|destination)).cursor())
    return _world_map_child_fields(state,frame,target,continuation)


def restore_scene_descriptor_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3E54: restore all descriptor regions, palettes and original cleared work buffers."""
    frame=_world_map_frame_fields(state,frame,0x3E54)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFEFD4,2),16)
    frame=_world_map_shift_fields(state,frame,'target_x',2)
    pointer=state.table_at(0x3E48).long(low16(frame.target_x))
    frame=first_replace(frame,controller=state.table_at(pointer))
    frame=_world_map_restore_region_fields(state,frame,0,0xF428,0x4026,0x3E68)
    frame=_world_map_restore_region_fields(state,frame,4,0xF460,0x4062,0x3E74)
    frame=first_replace(frame,roster=state.table_at(frame.controller.long(8)).cursor(),
        candidates=state.table_at(0xFFFFE640).cursor())
    frame=_world_map_copy_longs_fields(state,frame,7)
    regions=((0x0C,0xE000,0x4032,0x3E92),(0x10,0xE0A0,0x4032,0x3E9E),
        (0x14,0xE140,0x4032,0x3EAA),(0x18,0xE1E0,0x4032,0x3EB6),
        (0x1C,0xE280,0x4032,0x3EC2),(0x20,0xE320,0x4032,0x3ECE),
        (0x24,0xE3C0,0x4032,0x3EDA),(0x28,0xE460,0x4032,0x3EE6),
        (0x2C,0xE500,0x4032,0x3EF2),(0x30,0xE5A0,0x4032,0x3EFE),
        (0x34,0xB000,0x403E,0x3F0A),(0x38,0xB200,0x403E,0x3F16),
        (0x3C,0xB400,0x403E,0x3F22),(0x40,0xB600,0x403E,0x3F2E),
        (0x44,0xB800,0x403E,0x3F3A),(0x48,0xBA00,0x403E,0x3F46),
        (0x4C,0xBC00,0x403E,0x3F52),(0x50,0xBE00,0x403E,0x3F5E),
        (0x54,0xC000,0x403E,0x3F6A),(0x58,0xC200,0x404A,0x3F76),
        (0x5C,0xC300,0x404A,0x3F82),(0x60,0xC400,0x404A,0x3F8E),
        (0x64,0xC500,0x404A,0x3F9A),(0x68,0xC600,0x404A,0x3FA6),
        (0x6C,0xC700,0x404A,0x3FB2),(0x70,0xC800,0x4056,0x3FBE),
        (0x74,0xCC00,0x404A,0x3FCA),(0x78,0xE710,0x406E,0x3FD6))
    for offset,destination,target,continuation in regions:
        frame=_world_map_restore_region_fields(state,frame,offset,destination,target,continuation)
    frame=_world_map_store_fields(state,frame,0xFFFFE700,2,0,True)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE818).cursor())
    frame=_movement_move(state,frame,'target_x',119,16)
    while True:
        frame=_world_map_store_fields(state,frame,frame.roster.base,4,0xFFFFFFFF)
        frame=first_replace(frame,roster=frame.roster.advance(4),
            target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
        if low16(frame.target_x)==65535:
            break
    frame=_world_map_restore_region_fields(state,frame,0x7C,0xEA88,0x407A,0x3FF8)
    frame=_world_map_restore_region_fields(state,frame,0x80,0xF000,0x4096,0x4004)
    for address,value in ((0xFFFFF376,255),(0xFFFFEFD4,0),(0xFFFF9F00,65535)):
        frame=_world_map_store_fields(state,frame,address,2,value)
    frame=_movement_move(state,frame,'target_x',255,16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFA150).cursor())
    while True:
        frame=_world_map_store_fields(state,frame,frame.roster.base,4,0,True)
        frame=first_replace(frame,roster=frame.roster.advance(4),
            target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
        if low16(frame.target_x)==65535:
            return frame


def _world_map_city_restricted_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original repeated query-mode checks, then ownership rule for commands 100/119."""
    special=False
    for query in (6,15,21):
        frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),query,16)
        if frame.status&4:
            special=True
            break
    if not special:
        frame=_movement_compare(state,frame,low16(frame.target_x),16,16)
        if not frame.status&1:
            return _world_map_city_mark_fields(state,frame)
    frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF376,2),16)
    if not frame.status&4:
        return frame
    return _world_map_city_mark_fields(state,frame)


def _world_map_city_mark_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """BSET.L #15 retains upper D4 and changes only the original Z flag."""
    frame=_world_map_bit_fields(state,frame,frame.distance,15)
    return first_replace(frame,distance=u32(frame.distance|(1<<15)))


def locate_city_at_world_cursor_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5CC8: find a city inside cursor bounds, then apply the live command/owner rules."""
    frame=_world_map_frame_fields(state,frame,0x5CC8)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF360,2),16)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame=_world_map_arithmetic_fields(state,frame,'target_x',20,True)
    frame=_world_map_arithmetic_fields(state,frame,'target_y',20)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF35E,2),16)
    frame=_movement_move(state,frame,'count',low16(frame.unit),16)
    frame=_world_map_arithmetic_fields(state,frame,'unit',12,True)
    frame=_world_map_arithmetic_fields(state,frame,'count',12)
    frame=_movement_move(state,frame,'distance',0,16)
    frame=first_replace(frame,roster=state.table_at(0xD4ACA).cursor())
    while True:
        frame=_movement_move(state,frame,'offset_x',frame.roster.word(),16)
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_movement_compare(state,frame,low16(frame.offset_x),low16(frame.target_x),16)
        hit=not frame.status&1
        if hit:
            frame=_movement_compare(state,frame,low16(frame.offset_x),low16(frame.target_y),16)
            hit=bool(frame.status&5)
        if hit:
            frame=_movement_move(state,frame,'offset_x',frame.roster.word(),16)
            frame=first_replace(frame,roster=frame.roster.advance(2))
            frame=_movement_compare(state,frame,low16(frame.offset_x),low16(frame.unit),16)
            hit=not frame.status&1
            if hit:
                frame=_movement_compare(state,frame,low16(frame.offset_x),low16(frame.count),16)
                hit=bool(frame.status&5)
        if hit:
            break
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_world_map_arithmetic_fields(state,frame,'distance',1)
        frame=_movement_compare(state,frame,low16(frame.distance),40,16)
        if not frame.status&1:
            frame=_movement_move(state,frame,'distance',65535,16)
            break
    frame=_movement_test(state,frame,low16(frame.distance),16)
    if frame.status&8:
        return _world_map_store_fields(state,frame,0xFFFFF364,2,low16(frame.distance))
    frame=_movement_move(state,frame,'target_x',0,16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF428).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.distance)),8)
    frame=_movement_test(state,frame,state.read(0xFFFFF36C,2),16)
    restricted=False
    relation=False
    if not frame.status&4:
        for query in (6,15,21):
            frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),query,16)
            if frame.status&4:
                return _world_map_store_fields(state,frame,0xFFFFF364,2,low16(frame.distance))
        frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),100,16)
        restricted=bool(frame.status&4)
        if not restricted:
            frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),119,16)
            restricted=bool(frame.status&4)
        if not restricted:
            frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),117,16)
            relation=bool(frame.status&4)
        if not restricted and not relation:
            frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),99,16)
            if frame.status&4:
                frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A8,2),16)
                frame=_world_map_arithmetic_fields(state,frame,'target_y',1,True)
                frame=_movement_compare(state,frame,low16(frame.distance),low16(frame.target_y),16)
                if frame.status&4:
                    frame=_movement_move(state,frame,'distance',65535,16)
                    return _world_map_store_fields(state,frame,0xFFFFF364,2,low16(frame.distance))
    if restricted:
        frame=_world_map_city_restricted_fields(state,frame)
    elif relation:
        frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF376,2),16)
        frame=_world_map_shift_fields(state,frame,'target_y',1)
        frame=first_replace(frame,roster=state.table_at(0xFFFFE710).cursor())
        frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_y)),16)
        frame=_world_map_bit_fields(state,frame,frame.target_y,frame.target_x%32)
        if frame.status&4:
            frame=_world_map_city_mark_fields(state,frame)
    else:
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF376,2),16)
        if not frame.status&4:
            frame=_world_map_city_mark_fields(state,frame)
    return _world_map_store_fields(state,frame,0xFFFFF364,2,low16(frame.distance))


def scan_roster_selection_status_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """640A: clamp the live roster window around selected row, then mark a redraw."""
    frame=_world_map_frame_fields(state,frame,0x640A)
    frame=_movement_move(state,frame,'target_y',7,16)
    frame=_movement_move(state,frame,'count',state.read(0xFFFFF3A4,2),16)
    frame=_world_map_bit_fields(state,frame,frame.count,14)
    if not frame.status&4:
        frame=_movement_move(state,frame,'target_y',5,16)
    frame=_movement_move(state,frame,'unit',low16(frame.target_y),16)
    frame=_world_map_shift_fields(state,frame,'unit',1,True)
    frame=_world_map_arithmetic_fields(state,frame,'unit',1)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF378,2),16)
    frame=_world_map_arithmetic_fields(state,frame,'target_x',low16(frame.unit),True)
    if frame.status&8:
        frame=_movement_move(state,frame,'target_x',0,16)
    frame=_movement_move(state,frame,'count',state.read(0xFFFFF654,2),16)
    frame=_world_map_arithmetic_fields(state,frame,'count',low16(frame.target_y),True)
    if frame.status&8:
        frame=_movement_move(state,frame,'count',0,16)
    frame=_movement_compare(state,frame,low16(frame.target_x),low16(frame.count),16)
    if not frame.status&5:
        frame=_movement_move(state,frame,'target_x',low16(frame.count),16)
    frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF658,2),16)
    if frame.status&4:
        return frame
    frame=_world_map_store_fields(state,frame,0xFFFFF658,2,low16(frame.target_x))
    frame=_world_map_store_fields(state,frame,0xFFFFF36A,2,0,True)
    return _world_map_store_fields(state,frame,0xFFFFF362,2,10)


def scan_candidate_roster_status_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """64CC: count selected WORD entries and update only the original commit state."""
    frame=_world_map_frame_fields(state,frame,0x64CC)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF500).cursor())
    frame=_movement_move(state,frame,'target_y',0,16)
    while True:
        value=frame.roster.word()
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_movement_move(state,frame,'target_x',value,16)
        if frame.status&8:
            break
        frame=_movement_compare(state,frame,low16(frame.target_x),0x4000,16)
        if not frame.status&1:
            frame=_world_map_arithmetic_fields(state,frame,'target_y',1)
    frame=_movement_test(state,frame,low16(frame.target_y),16)
    if frame.status&4:
        return frame
    frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),144,16)
    if not frame.status&4:
        frame=_movement_compare(state,frame,low16(frame.target_y),state.read(0xFFFFF636,2),16)
        if not frame.status&1:
            return frame
    value=state.read(0xFFFFF3A5,1)
    frame=_world_map_bit_fields(state,frame,value,0)
    state.write(0xFFFFF3A5,1,value&254)
    frame=_world_map_store_fields(state,frame,0xFFFFF612,2,520)
    frame=_world_map_store_fields(state,frame,0xFFFFF362,2,4)
    frame=_world_map_store_fields(state,frame,0xFFFFF39E,4,0,True)
    frame=_world_map_store_fields(state,frame,0xFFFFF3BA,4,0,True)
    return _world_map_store_fields(state,frame,0xFFFFF670,2,0,True)


def locate_map_object_record_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """9E14: variable-length object walk; carry reports the actual coordinate match."""
    frame=_world_map_frame_fields(state,frame,0x9E14)
    frame=first_replace(frame,roster=state.table_at(0xFFFF9000).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF35E,2),16)
    frame=_world_map_arithmetic_fields(state,frame,'target_x',2,True)
    frame=_world_map_shift_fields(state,frame,'target_x',4,True)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF360,2),16)
    frame=_world_map_arithmetic_fields(state,frame,'target_y',2,True)
    frame=_world_map_shift_fields(state,frame,'target_y',4,True)
    while True:
        frame=_movement_move(state,frame,'unit',frame.roster.byte(),8)
        if frame.status&4:
            frame=first_replace(frame,status=frame.status&30)
            state.sr=(state.sr&65504)|frame.status
            return frame
        frame=_movement_move(state,frame,'unit',low8(frame.unit)&127,8)
        frame=_movement_move(state,frame,'count',frame.roster.byte(0,4),8)
        frame=_movement_compare(state,frame,low8(frame.target_x),frame.roster.byte(0,1),8)
        if frame.status&4:
            frame=_movement_compare(state,frame,low8(frame.target_y),frame.roster.byte(0,2),8)
            if frame.status&4:
                frame=_world_map_store_fields(state,frame,0x00FF382C,4,frame.roster.base)
                frame=first_replace(frame,status=frame.status|1)
                state.sr=(state.sr&65504)|frame.status
                return frame
        frame=_movement_move(state,frame,'unit',low16(frame.unit)&15,16)
        frame=_world_map_arithmetic_fields(state,frame,'unit',13)
        frame=first_replace(frame,roster=frame.roster.advance(s16(low16(frame.unit))))


def queue_map_strip_transfer_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """9F7C: append two 18-cell strips, from actual readonly data or blank cells."""
    frame=_world_map_frame_fields(state,frame,0x9F7C)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF31A,2),16)
    frame=first_replace(frame,roster=state.table_at(u32(0xFFFFD100+s16(low16(frame.target_x)))).cursor())
    frame=_world_map_store_fields(state,frame,frame.roster.base,2,18)
    frame=_world_map_store_fields(state,frame,u32(frame.roster.base+40),2,18)
    frame=_movement_move(state,frame,'unit',17,16)
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_world_map_bit_fields(state,frame,state.read(0xFFFFF31C,1),0)
    if not frame.status&4:
        frame=_movement_move(state,frame,'target_y',40,16)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF322,2),16)
    frame=_world_map_shift_fields(state,frame,'target_x',7)
    frame=_world_map_arithmetic_fields(state,frame,'target_x',0xC102)
    frame=_world_map_arithmetic_fields(state,frame,'target_x',low16(frame.target_y))
    frame=_world_map_store_fields(state,frame,u32(frame.roster.base+2),2,low16(frame.target_x))
    frame=_world_map_arithmetic_fields(state,frame,'target_x',128)
    frame=_world_map_store_fields(state,frame,u32(frame.roster.base+42),2,low16(frame.target_x))
    frame=first_replace(frame,roster=frame.roster.advance(4))
    frame=_world_map_bit_fields(state,frame,state.read(0xFFFFF31C,1),1)
    blank=not bool(frame.status&4)
    if not blank:
        frame=first_replace(frame,candidates=state.table_at(0xD323A).cursor())
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF322,2),16)
        frame=_movement_move(state,frame,'target_y',36,16)
        frame=_movement_multiply_word(state,frame,'target_x',low16(frame.target_y))
        frame=first_replace(frame,candidates=frame.candidates.advance(s16(low16(frame.target_x))))
    for strip in (0,1):
        if strip:
            frame=_movement_move(state,frame,'unit',17,16)
            frame=first_replace(frame,roster=frame.roster.advance(4))
        while True:
            if blank:
                value=0x8000
            else:
                value=frame.candidates.word()
                frame=first_replace(frame,candidates=frame.candidates.advance(2))
            frame=_world_map_store_fields(state,frame,frame.roster.base,2,value)
            frame=first_replace(frame,roster=frame.roster.advance(2),
                unit=replace_word(frame.unit,u16(low16(frame.unit)-1)))
            if low16(frame.unit)==65535:
                break
    frame=_world_map_store_fields(state,frame,frame.roster.base,2,0,True)
    previous=state.read(0xFFFFF31A,2)
    frame,value=_movement_binary_flags(state,frame,previous,80,16)
    state.write(0xFFFFF31A,2,value)
    if not blank:
        previous=state.read(0xFFFFF322,2)
        frame,value=_movement_binary_flags(state,frame,previous,2,16)
        state.write(0xFFFFF322,2,value)
    return frame


def _world_map_scroll_axis_fields(state: SceneState, frame: FirstDeploymentFrame,
        cursor_address: int, scroll_address: int, viewport: int,
        ceiling: int, edge: int, renderer: int, near_token: int,
        far_token: int) -> FirstDeploymentFrame:
    """One closed X/Y viewport rule, with each original reread and call slot."""
    frame=_movement_move(state,frame,'target_x',state.read(cursor_address,2),16)
    frame=_world_map_arithmetic_fields(state,frame,'target_x',32,True)
    if frame.status&8:
        frame=_movement_move(state,frame,'target_x',0,16)
    frame=_movement_compare(state,frame,low16(frame.target_x),state.read(scroll_address,2),16)
    if frame.status&1:
        frame=_world_map_store_fields(state,frame,scroll_address,2,low16(frame.target_x))
        frame=first_replace(frame,scratch=state.table_at(u32(s16(low16(frame.target_x)))))
        return _world_map_child_fields(state,frame,renderer,near_token)
    frame=_movement_move(state,frame,'target_x',state.read(cursor_address,2),16)
    frame=_world_map_arithmetic_fields(state,frame,'target_x',viewport,True)
    if frame.status&8:
        frame=_movement_move(state,frame,'target_x',0,16)
    frame=_movement_compare(state,frame,low16(frame.target_x),ceiling,16)
    if not frame.status&5:
        frame=_movement_move(state,frame,'target_x',ceiling,16)
    frame=_movement_compare(state,frame,low16(frame.target_x),state.read(scroll_address,2),16)
    if not frame.status&5:
        frame=_world_map_store_fields(state,frame,scroll_address,2,low16(frame.target_x))
        frame=_world_map_arithmetic_fields(state,frame,'target_x',edge)
        frame=first_replace(frame,scratch=state.table_at(u32(s16(low16(frame.target_x)))))
        frame=_world_map_child_fields(state,frame,renderer,far_token)
    return frame


def refresh_map_tiles_around_cursor_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A01C: keep the world cursor inside the original horizontal/vertical viewport."""
    frame=_world_map_frame_fields(state,frame,0xA01C)
    frame=_world_map_scroll_axis_fields(state,frame,0xFFFFF35E,0xFFFFF314,
        192,928,224,0xA0CC,0xA03C,0xA072)
    return _world_map_scroll_axis_fields(state,frame,0xFFFFF360,0xFFFFF318,
        288,832,320,0xA10C,0xA092,0xA0C8)


def _world_map_render_strip_fields(state: SceneState, frame: FirstDeploymentFrame,
        horizontal: bool) -> FirstDeploymentFrame:
    """Two closed strip roles share actual map lookup and RAM packet construction."""
    if horizontal:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF314,2),16)
        frame=_movement_move(state,frame,'target_y',low16(frame.scratch.base),16)
    else:
        frame=_movement_move(state,frame,'target_x',low16(frame.scratch.base),16)
        frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF318,2),16)
    frame=first_replace(frame,roster=state.table_at(0x8155A).cursor())
    frame=_world_map_store_fields(state,frame,0xFFFFF328,2,1 if horizontal else 0,not horizontal)
    frame=_world_map_child_fields(state,frame,0xAF6A,0xA124 if horizontal else 0xA0E2)
    frame=_world_map_child_fields(state,frame,0xB054,0xA12A if horizontal else 0xA0E8)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)|0xE000,16)
    frame=first_replace(frame,roster=state.table_at(u32(0xFFFFD100+s16(state.read(0xFFFFF31A,2)))).cursor())
    frame=_movement_move(state,frame,'target_y',0x801D if horizontal else 41,16)
    frame=_world_map_store_fields(state,frame,frame.roster.base,2,low16(frame.target_y))
    frame=first_replace(frame,roster=frame.roster.advance(2))
    frame=_world_map_store_fields(state,frame,frame.roster.base,2,low16(frame.target_x))
    frame=first_replace(frame,roster=frame.roster.advance(2))
    frame=_world_map_child_fields(state,frame,0xB0B2 if horizontal else 0xB06E,
        0xA144 if horizontal else 0xA102)
    frame=_world_map_store_fields(state,frame,frame.roster.base,2,0,True)
    previous=state.read(0xFFFFF31A,2)
    frame,value=_movement_binary_flags(state,frame,previous,62 if horizontal else 86,16)
    state.write(0xFFFFF31A,2,value)
    return frame


def render_map_column_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A0CC: append the real 41-cell vertical map-transfer packet."""
    return _world_map_render_strip_fields(state,_world_map_frame_fields(state,frame,0xA0CC),False)


def render_map_row_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A10C: append the real 29-cell horizontal map-transfer packet."""
    return _world_map_render_strip_fields(state,_world_map_frame_fields(state,frame,0xA10C),True)


def _world_map_read_offset_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, displacement: int, negative_sentinel: bool=False) -> FirstDeploymentFrame:
    """One actual WORD offset lookup; MOVEA and signed-sentinel tests keep their flags."""
    frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_x),displacement),16)
    if negative_sentinel:
        absent=bool(frame.status&8)
    else:
        frame=_movement_compare(state,frame,low16(frame.target_y),65535,16)
        absent=bool(frame.status&4)
    if absent:
        return first_replace(frame,**{name:state.table_at(0xFFFFFFFF)})
    frame=first_replace(frame,**{name:state.table_at(frame.opponent.base)})
    frame=_movement_move_long(state,frame,'target_y',frame.target_y&65535)
    return first_replace(frame,**{name:state.table_at(u32(frame.opponent.base+frame.target_y))})


def read_world_map_tile_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """AF6A: divide cell coordinates and resolve actual adjacent compressed tile pointers."""
    frame=_world_map_frame_fields(state,frame,0xAF6A)
    frame=_world_map_shift_fields(state,frame,'target_x',3,True)
    frame=_world_map_shift_fields(state,frame,'target_y',3,True)
    frame=_movement_save_longs(state,frame,('target_x','target_y'))
    frame=_movement_move(state,frame,'distance',frame.roster.byte(0,2),8)
    frame=_movement_move(state,frame,'distance',u16(s8(low8(frame.distance))),16)
    frame=_movement_move_long(state,frame,'target_x',u32(s16(low16(frame.target_x))))
    frame=_movement_divu_word(state,frame,'target_x',low16(frame.distance),0xAF7A)
    frame=_movement_move_long(state,frame,'unit',frame.target_x)
    frame=_movement_move_long(state,frame,'unit',swap_words(frame.unit))
    frame=_movement_move(state,frame,'offset_x',frame.roster.byte(0,3),8)
    frame=_movement_move(state,frame,'offset_x',u16(s8(low8(frame.offset_x))),16)
    frame=_movement_move_long(state,frame,'target_y',u32(s16(low16(frame.target_y))))
    frame=_movement_divu_word(state,frame,'target_y',low16(frame.offset_x),0xAF88)
    frame=_movement_move_long(state,frame,'count',frame.target_y)
    frame=_movement_move_long(state,frame,'count',swap_words(frame.count))
    frame=first_replace(frame,opponent=state.table_at(frame.roster.long(0,4)))
    frame=_movement_multiply_word(state,frame,'target_x',frame.roster.word())
    frame=_world_map_arithmetic_fields(state,frame,'target_x',low16(frame.target_y))
    frame=_world_map_shift_fields(state,frame,'target_x',1)
    frame=_world_map_read_offset_fields(state,frame,'candidates',8)
    frame=_movement_test(state,frame,state.read(0xFFFFF328,2),16)
    if frame.status&4:
        frame=_world_map_read_offset_fields(state,frame,'controller',10,True)
        frame=_world_map_read_offset_fields(state,frame,'scan',12)
        frame=_world_map_read_offset_fields(state,frame,'scratch',14)
    else:
        for name in ('controller','scan'):
            frame=_world_map_arithmetic_fields(state,frame,'target_x',frame.roster.word())
            frame=_world_map_arithmetic_fields(state,frame,'target_x',frame.roster.word())
            frame=_world_map_read_offset_fields(state,frame,name,8)
    return _movement_restore_longs(state,frame,('target_x','target_y'))


def read_map_cell_word_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """B054: exact modulo-64 cell offset using the unique DIVU/MULU primitives."""
    frame=_world_map_frame_fields(state,frame,0xB054)
    frame=_movement_move_long(state,frame,'target_x',u32(s16(low16(frame.target_x))))
    frame=_movement_divu_word(state,frame,'target_x',64,0xB056)
    frame=_movement_move_long(state,frame,'target_x',swap_words(frame.target_x))
    frame=_movement_multiply_word(state,frame,'target_x',64)
    frame=_movement_move_long(state,frame,'target_y',u32(s16(low16(frame.target_y))))
    frame=_movement_divu_word(state,frame,'target_y',64,0xB062)
    frame=_movement_move_long(state,frame,'target_y',swap_words(frame.target_y))
    frame=_world_map_arithmetic_fields(state,frame,'target_x',low16(frame.target_y))
    return _world_map_shift_fields(state,frame,'target_x',1)


def advance_map_column_source_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """B0DE: choose the live half-column compressed stream, restoring actual MOVEM values."""
    frame=_world_map_frame_fields(state,frame,0xB0DE)
    frame=_movement_save_longs(state,frame,('target_x','unit','roster'))
    frame=_movement_move_long(state,frame,'target_x',frame.candidates.base)
    if frame.status&8:
        frame=first_replace(frame,opponent=state.table_at(frame.candidates.base))
    else:
        frame=first_replace(frame,roster=state.table_at(frame.candidates.long()).cursor())
        frame=_movement_move(state,frame,'offset_y',low16(frame.offset_x),16)
        frame=_world_map_shift_fields(state,frame,'offset_y',1,True)
        frame=_movement_compare(state,frame,low16(frame.count),low16(frame.offset_y),16)
        if not frame.status&1:
            frame=_world_map_arithmetic_fields(state,frame,'unit',1)
        frame=_world_map_shift_fields(state,frame,'unit',1)
        frame=_movement_move(state,frame,'unit',frame.candidates.word(low16(frame.unit),4),16)
        frame=first_replace(frame,opponent=state.table_at(u32(frame.roster.base+s16(low16(frame.unit)))))
    return _movement_restore_longs(state,frame,('target_x','unit','roster'))


def _world_map_compressed_blank_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Absent tile streams yield the original zero cell and MOVEQ64 run length."""
    frame=_movement_move(state,frame,'offset_y',0,16)
    return _movement_move_long(state,frame,'choice',64)


def _world_map_encoded_run_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str) -> FirstDeploymentFrame:
    """The encoded bit7 distinguishes a constant run from an incrementing run."""
    frame=_movement_move_long(state,frame,name,frame.carrier(name)&65535)
    frame=_world_map_bit_fields(state,frame,frame.carrier('target_x' if name=='choice' else name),7)
    if not frame.status&4:
        carrier='target_x' if name=='choice' else name
        frame=_world_map_bit_fields(state,frame,frame.carrier(carrier),7)
        frame=first_replace(frame,**{carrier:frame.carrier(carrier)&~128})
        frame=_movement_move_long(state,frame,name,frame.carrier(name)|65536)
    return frame


def resolve_map_column_packet_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """B106: resolve one compressed run by forward or backward half-column search."""
    frame=_world_map_frame_fields(state,frame,0xB106)
    frame=_movement_move_long(state,frame,'choice',frame.opponent.base)
    if frame.status&8:
        return _world_map_compressed_blank_fields(state,frame)
    frame=_movement_move(state,frame,'offset_y',low16(frame.offset_x),16)
    frame=_world_map_shift_fields(state,frame,'offset_y',1,True)
    frame=_movement_compare(state,frame,low16(frame.count),low16(frame.offset_y),16)
    if frame.status&1:
        frame=_movement_move(state,frame,'choice',low16(frame.count),16)
        frame=_world_map_arithmetic_fields(state,frame,'choice',1)
        while True:
            frame=_movement_move(state,frame,'offset_y',frame.opponent.word(),16)
            frame=first_replace(frame,opponent=frame.opponent.advance(2))
            frame=_movement_move(state,frame,'target_x',low16(frame.offset_y),16)
            frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&2047,16)
            frame=_world_map_arithmetic_fields(state,frame,'target_x',1791,True)
            if not frame.status&1:
                break
            frame=_world_map_arithmetic_fields(state,frame,'choice',1,True)
            if frame.status&4:
                return _movement_move_long(state,frame,'choice',0)
        while True:
            frame=_movement_move(state,frame,'offset_y',frame.opponent.word(),16)
            frame=first_replace(frame,opponent=frame.opponent.advance(2))
            frame=_world_map_encoded_run_fields(state,frame,'choice')
            frame=_world_map_arithmetic_fields(state,frame,'choice',low16(frame.target_x),True)
            if not frame.status&5:
                while True:
                    frame=_movement_move(state,frame,'offset_y',frame.opponent.word(),16)
                    frame=first_replace(frame,opponent=frame.opponent.advance(2))
                    frame=_movement_move(state,frame,'target_x',low16(frame.offset_y),16)
                    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&2047,16)
                    frame=_world_map_arithmetic_fields(state,frame,'target_x',1791,True)
                    if not frame.status&1:
                        break
                    frame=_world_map_arithmetic_fields(state,frame,'choice',1,True)
                    if frame.status&4:
                        return _movement_move_long(state,frame,'choice',0)
                continue
            frame,negative=_movement_binary_flags(state,frame,0,low16(frame.choice),16,True)
            frame=first_replace(frame,choice=replace_word(frame.choice,negative))
            frame=_movement_compare_address(state,frame,frame.choice,65536)
            if not frame.status&1:
                frame=_world_map_arithmetic_fields(state,frame,'target_x',low16(frame.choice),True)
                frame=_world_map_arithmetic_fields(state,frame,'target_x',1,True)
                frame=_world_map_arithmetic_fields(state,frame,'offset_y',low16(frame.target_x))
            return frame
    frame=_movement_move(state,frame,'choice',low16(frame.offset_x),16)
    frame=_world_map_arithmetic_fields(state,frame,'choice',1,True)
    while True:
        frame=first_replace(frame,opponent=frame.opponent.advance(-2))
        frame=_movement_compare(state,frame,low16(frame.choice),low16(frame.count),16)
        if frame.status&4:
            frame=_movement_move_long(state,frame,'choice',0)
            return _world_map_reverse_cell_fields(state,frame)
        frame=_movement_move(state,frame,'target_x',frame.opponent.word(0,-2),16)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&2047,16)
        frame=_world_map_arithmetic_fields(state,frame,'target_x',1792,True)
        if not frame.status&1:
            frame=_world_map_encoded_run_fields(state,frame,'choice')
            frame=_world_map_arithmetic_fields(state,frame,'choice',low16(frame.target_x),True)
            frame=_movement_compare(state,frame,low16(frame.choice),low16(frame.count),16)
            if frame.status&5:
                return _world_map_reverse_tail_fields(state,frame)
            frame=first_replace(frame,opponent=frame.opponent.advance(-2))
            frame=_world_map_arithmetic_fields(state,frame,'choice',1,True)
        else:
            frame=_world_map_arithmetic_fields(state,frame,'choice',1,True)


def _world_map_reverse_cell_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original backward single-cell tail, no extra physical call."""
    frame=_movement_move(state,frame,'offset_y',frame.opponent.word(),16)
    frame=_movement_move(state,frame,'target_x',frame.opponent.word(0,-2),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&2047,16)
    frame=_world_map_arithmetic_fields(state,frame,'target_x',1920,True)
    if not frame.status&1:
        frame=_world_map_arithmetic_fields(state,frame,'offset_y',low16(frame.target_x))
    return first_replace(frame,opponent=frame.opponent.advance(2))


def _world_map_reverse_tail_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original backward run tail preserves D3 in one real inner MOVEM LONG."""
    frame=_movement_save_longs(state,frame,('count',))
    frame=_world_map_arithmetic_fields(state,frame,'count',low16(frame.choice),True)
    frame=_movement_move(state,frame,'offset_y',low16(frame.target_x),16)
    frame=_world_map_arithmetic_fields(state,frame,'target_x',low16(frame.count),True)
    frame=_movement_move(state,frame,'choice',low16(frame.target_x),16)
    frame=_movement_move(state,frame,'target_x',0,16)
    frame=_movement_compare_address(state,frame,frame.choice,65536)
    if not frame.status&1:
        frame=_world_map_arithmetic_fields(state,frame,'offset_y',low16(frame.choice),True)
    frame=_movement_move(state,frame,'target_x',low16(frame.offset_y),16)
    value=frame.opponent.word()
    frame=first_replace(frame,opponent=frame.opponent.advance(2))
    frame=_world_map_arithmetic_fields(state,frame,'target_x',value)
    frame=_movement_move(state,frame,'offset_y',low16(frame.target_x),16)
    return _movement_restore_longs(state,frame,('count',))


def advance_map_column_skip_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """B1DA: consume the next real literal or encoded run without extra source reads."""
    frame=_world_map_frame_fields(state,frame,0xB1DA)
    frame=_movement_move_long(state,frame,'choice',frame.candidates.base)
    if frame.status&8:
        return _world_map_compressed_blank_fields(state,frame)
    frame=_movement_move(state,frame,'offset_y',frame.opponent.word(),16)
    frame=first_replace(frame,opponent=frame.opponent.advance(2))
    frame=_movement_move(state,frame,'choice',low16(frame.offset_y),16)
    frame=_movement_move(state,frame,'choice',low16(frame.choice)&2047,16)
    frame=_world_map_arithmetic_fields(state,frame,'choice',1792,True)
    if frame.status&1:
        return _movement_move_long(state,frame,'choice',0)
    frame=_movement_move_long(state,frame,'choice',frame.choice&65535)
    frame=_world_map_bit_fields(state,frame,frame.choice,7)
    if not frame.status&4:
        frame=_world_map_bit_fields(state,frame,frame.choice,7)
        frame=first_replace(frame,choice=frame.choice&~128)
        frame=_movement_move_long(state,frame,'choice',frame.choice|65536)
    frame=_movement_move(state,frame,'offset_y',frame.opponent.word(),16)
    return first_replace(frame,opponent=frame.opponent.advance(2))


def read_initial_map_column_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """B06E: decode a vertical strip across live neighboring compressed blocks."""
    frame=_world_map_frame_fields(state,frame,0xB06E)
    frame=_world_map_child_fields(state,frame,0xB0DE,0xB070)
    frame=_world_map_child_fields(state,frame,0xB106,0xB074)
    frame=_movement_move(state,frame,'target_x',low16(frame.offset_x),16)
    frame=_world_map_arithmetic_fields(state,frame,'target_x',low16(frame.count),True)
    while True:
        frame=_world_map_store_fields(state,frame,frame.roster.base,2,low16(frame.offset_y))
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_world_map_arithmetic_fields(state,frame,'target_y',1,True)
        if frame.status&4:
            return _world_map_store_fields(state,frame,frame.roster.base,2,0,True)
        frame=_world_map_arithmetic_fields(state,frame,'target_x',1,True)
        if frame.status&4:
            frame=first_replace(frame,candidates=state.table_at(frame.controller.base),
                controller=state.table_at(frame.scan.base),scan=state.table_at(frame.scratch.base).cursor())
            frame=_movement_move(state,frame,'count',0,16)
            frame=_movement_move(state,frame,'target_x',low16(frame.offset_x),16)
            frame=_world_map_child_fields(state,frame,0xB0DE,0xB0A8)
            frame=_world_map_child_fields(state,frame,0xB1DA,0xB0AC)
            continue
        frame=_movement_compare_address(state,frame,frame.choice,65536)
        if not frame.status&1:
            frame=_world_map_arithmetic_fields(state,frame,'offset_y',1)
        frame=first_replace(frame,choice=replace_word(frame.choice,u16(low16(frame.choice)-1)))
        if low16(frame.choice)==65535:
            frame=_world_map_child_fields(state,frame,0xB1DA,0xB09A)


def read_wrapped_map_column_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """B0B2: decode a horizontal strip, carrying real remainder and neighbor pointers."""
    frame=_world_map_frame_fields(state,frame,0xB0B2)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_y)&32767,16)
    frame=_world_map_child_fields(state,frame,0xB0DE,0xB0B8)
    frame=_world_map_child_fields(state,frame,0xB106,0xB0BA)
    while True:
        frame=_world_map_store_fields(state,frame,frame.roster.base,2,low16(frame.offset_y))
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_world_map_arithmetic_fields(state,frame,'target_y',1,True)
        if frame.status&4:
            return _world_map_store_fields(state,frame,frame.roster.base,2,0,True)
        frame=_world_map_arithmetic_fields(state,frame,'unit',1)
        frame=_movement_compare(state,frame,low16(frame.unit),low16(frame.distance),16)
        if frame.status&4:
            frame=_movement_move(state,frame,'unit',0,16)
            frame=first_replace(frame,candidates=state.table_at(frame.controller.base),
                controller=state.table_at(frame.scan.base))
            frame=_movement_move(state,frame,'target_x',low16(frame.offset_x),16)
            frame=_world_map_child_fields(state,frame,0xB0DE,0xB0D6)
            frame=_world_map_child_fields(state,frame,0xB106,0xB0D8)
        else:
            frame=_world_map_child_fields(state,frame,0xB0DE,0xB0C8)
            frame=_world_map_child_fields(state,frame,0xB106,0xB0CA)

from .business_commands import (
    _city_ui_store_fields, _city_ui_append_fields, _city_ui_arithmetic_fields,
    _city_ui_memory_arithmetic_fields, _city_ui_bit_fields, _city_ui_shift_fields,
    _campaign_ui_call_fields, _campaign_ui_parallel_cell_fields, _campaign_ui_change_bit_fields,
)


def _command_officer_blank_row_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """The previous-officer empty row keeps its actual capacity flag, clear order and phase progression."""
    frame=_city_ui_append_fields(state,frame,0xD380)
    frame=_movement_move(state,frame,'count',7,16)
    while True:
        frame=_city_ui_append_fields(state,frame,0xD381)
        frame=first_replace(frame,count=replace_word(frame.count,u16(low16(frame.count)-1)))
        if low16(frame.count)==65535:
            break
    frame=_city_ui_append_fields(state,frame,0xDB80)
    frame=_city_ui_append_fields(state,frame,0,2,True)
    frame=_city_ui_append_fields(state,frame,0,2,True)
    frame=_movement_move(state,frame,'target_x',7,16)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),6)
    if not frame.status&4:
        frame=_movement_move(state,frame,'target_x',5,16)
    frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF36A,2),16)
    if frame.status&1 or frame.status&4:
        frame=_city_ui_store_fields(state,frame,frame.roster.base,0,2,True)
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,30)
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,1)
        frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)
        return _city_ui_store_fields(state,frame,0xFFFFF3A4,state.read(0xFFFFF3A4,2)&0xFBFF)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=_movement_move(state,frame,'count',12,16)
    while True:
        for offset in (34,4):
            frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.unit))+offset),0,2,True)
        frame=_city_ui_arithmetic_fields(state,frame,'unit',2)
        frame=first_replace(frame,count=replace_word(frame.count,u16(low16(frame.count)-1)))
        if low16(frame.count)==65535:
            break
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,1)
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)
    frame=_city_ui_store_fields(state,frame,0xFFFFF3A4,state.read(0xFFFFF3A4,2)&0xFBFF)
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+60),0,2,True)
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,90)


def _command_officer_extra_row_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """The sentinel extra officer uses its distinct real three-row glyph sequence."""
    frame=_campaign_ui_parallel_cell_fields(state,frame,0xC382,(60,30))
    for _cell in (0,1):
        frame=_campaign_ui_parallel_cell_fields(state,frame,0xC001,(60,30))
    frame=_movement_move(state,frame,'target_x',3,16)
    frame=_movement_move(state,frame,'target_y',0xC0B8,16)
    while True:
        frame=_city_ui_store_fields(state,frame,frame.roster.base,low16(frame.target_y))
        frame=_city_ui_arithmetic_fields(state,frame,'target_y',1)
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+30),low16(frame.target_y))
        frame=_city_ui_arithmetic_fields(state,frame,'target_y',1)
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+60),0xC001)
        frame=first_replace(frame,roster=frame.roster.advance(2),target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
        if low16(frame.target_x)==65535:
            break
    for _cell in (0,1):
        frame=_campaign_ui_parallel_cell_fields(state,frame,0xC001,(60,30))
    frame=_campaign_ui_parallel_cell_fields(state,frame,0xCB82,(60,30))
    for _cell in (0,1):
        frame=_campaign_ui_parallel_cell_fields(state,frame,0,(60,30),True)
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,90)
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,1)


def select_previous_command_officer_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5F7C: append the actual normal, empty or extra-officer row, preserving Dn bit14 versus BYTE bit6."""
    frame=_world_map_frame_fields(state,frame,0x5F7C)
    frame=_campaign_ui_call_fields(state,frame,0x5A42,0x5F80)
    frame=_campaign_ui_parallel_cell_fields(state,frame,0,(60,30),True)
    frame=_movement_move(state,frame,'target_x',7,16)
    frame=_movement_compare(state,frame,state.read(0xFFFFF36C,2),1,16)
    load_capacity=False
    if frame.status&4:
        for command in (6,15,21):
            frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),command,16)
            if frame.status&4:
                load_capacity=True
                break
    if not load_capacity:
        frame=_movement_test(state,frame,state.read(0xFFFFF36C,2),16)
        if frame.status&4:
            frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),129,16)
            if frame.status&4:
                frame=_movement_move(state,frame,'target_x',5,16)
            else:
                load_capacity=True
        else:
            frame=_movement_move(state,frame,'target_x',5,16)
    if load_capacity:
        frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A4,2),16)
        frame=_city_ui_bit_fields(state,frame,frame.target_y,14)
        if not frame.status&4:
            frame=_movement_move(state,frame,'target_x',5,16)
    frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF36A,2),16)
    if frame.status&1 or frame.status&4:
        return _command_officer_blank_row_frame_fields(state,frame)
    frame=_movement_move(state,frame,'choice',state.read(0xFFFFF36A,2),16)
    frame=_city_ui_arithmetic_fields(state,frame,'choice',state.read(0xFFFFF658,2))
    frame=_movement_move(state,frame,'offset_y',low16(frame.choice),16)
    frame=_movement_compare(state,frame,low16(frame.offset_y),state.read(0xFFFFF636,2),16)
    if not frame.status&1:
        frame=_movement_test(state,frame,state.read(0xFFFFF656,2),16)
        if not frame.status&4:
            frame=_movement_compare(state,frame,low16(frame.offset_y),state.read(0xFFFFF636,2),16)
            if frame.status&4:
                return _command_officer_extra_row_frame_fields(state,frame)
        return _command_officer_blank_row_frame_fields(state,frame)
    frame=_campaign_ui_parallel_cell_fields(state,frame,0xC382,(30,60))
    frame=_movement_move(state,frame,'offset_y',low16(frame.choice),16)
    frame=_city_ui_shift_fields(state,frame,'choice',1)
    frame=_city_ui_arithmetic_fields(state,frame,'choice',low16(frame.offset_y))
    frame=_city_ui_shift_fields(state,frame,'choice',2)
    frame=_movement_compare(state,frame,state.read(0xFFFFF6C4,2),1,16)
    frame=_city_ui_arithmetic_fields(state,frame,'choice',0xC070 if frame.status&4 else 0xC670)
    frame=_movement_move(state,frame,'count',low16(frame.choice),16)
    frame=_campaign_ui_call_fields(state,frame,0x5868,0x6022)
    frame=_campaign_ui_parallel_cell_fields(state,frame,0xC001,(30,))
    frame=_campaign_ui_parallel_cell_fields(state,frame,0xCB82,(60,30))
    for _cell in (0,1):
        frame=_campaign_ui_parallel_cell_fields(state,frame,0,(60,30),True)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=_movement_move(state,frame,'count',7,16)
    while True:
        frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.unit))+38),0xC001)
        frame=_city_ui_arithmetic_fields(state,frame,'unit',2)
        frame=first_replace(frame,count=replace_word(frame.count,u16(low16(frame.count)-1)))
        if low16(frame.count)==65535:
            break
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,1)
    frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+60),0,2,True)
    return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,90)


def select_next_command_officer_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """6198: clear completed rows, then enter the original force/equipment/message workflow with true child slots."""
    frame=_world_map_frame_fields(state,frame,0x6198)
    frame=_movement_move(state,frame,'target_x',7,16)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),6)
    if not frame.status&4:
        frame=_movement_move(state,frame,'target_x',5,16)
    frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF36A,2),16)
    if not frame.status&1:
        last_row=bool(frame.status&4)
        frame=_campaign_ui_call_fields(state,frame,0x5A42,0x61DC if last_row else 0x61B4)
        frame=_movement_move(state,frame,'target_x',12,16)
        while True:
            frame=_campaign_ui_parallel_cell_fields(state,frame,0,(30,) if last_row else (60,30),True)
            frame=first_replace(frame,target_x=replace_word(frame.target_x,u16(low16(frame.target_x)-1)))
            if low16(frame.target_x)==65535:
                break
        if last_row:
            frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+30),0,2,True)
            frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,60)
        else:
            frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,90)
            frame=_city_ui_store_fields(state,frame,u32(frame.roster.base+60),0,2,True)
        return _city_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,1)
    frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),1)
    if not frame.status&4:
        return frame
    frame=_movement_compare(state,frame,state.read(0xFFFFF36C,2),1,16)
    if frame.status&4:
        frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),102,16)
        if frame.status&4:
            frame=_city_ui_store_fields(state,frame,0xFFFFF600,56)
            frame=_campaign_ui_call_fields(state,frame,0xC3CE,0x6228)
        else:
            frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),122,16)
            if frame.status&4:
                frame=_campaign_ui_call_fields(state,frame,0x135C4,0x6238)
                frame=_city_ui_store_fields(state,frame,0xFFFFF600,76)
                frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF378,2),16)
                frame=_city_ui_shift_fields(state,frame,'target_x',1)
                frame=first_replace(frame,roster=state.table_at(0xFFFFF4FE).cursor())
                frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
                frame=_city_ui_shift_fields(state,frame,'target_x',2)
                frame=first_replace(frame,roster=state.table_at(0xFFFFC800).cursor())
                frame=_city_ui_store_fields(state,frame,0xFFFFF3EE,frame.roster.long(low16(frame.target_x)),4)
                frame=_campaign_ui_call_fields(state,frame,0x136F4,0x625E)
                frame=_campaign_ui_call_fields(state,frame,0x1374A,0x6264)
            else:
                frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),103,16)
                if frame.status&4:
                    return _city_ui_store_fields(state,frame,0xFFFFF600,60)
        frame=_campaign_ui_change_bit_fields(state,frame,0xFFFFF3A4,1,True)
        for command in (6,15,21):
            frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),command,16)
            if frame.status&4:
                return frame
        return _campaign_ui_call_fields(state,frame,0x676C4,0x62A0)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),129,16)
    if frame.status&4:
        return frame
    frame=_movement_test(state,frame,state.read(0xFFFFF36C,2),16)
    if frame.status&4:
        return frame
    frame=first_replace(frame,roster=state.table_at(0x62D2).cursor())
    while True:
        value=frame.roster.word()
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_movement_move(state,frame,'target_x',value,16)
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF38C,2),16)
        if frame.status&4:
            break
        frame=first_replace(frame,roster=frame.roster.advance(2))
    value=frame.roster.word()
    frame=first_replace(frame,roster=frame.roster.advance(2))
    frame=_movement_move(state,frame,'target_x',value,16)
    frame=_campaign_ui_call_fields(state,frame,0x676F2,0x62CA)
    return _campaign_ui_change_bit_fields(state,frame,0xFFFFF3A4,1,True)


def adjust_selected_roster_member_frame_fields(state: SceneState, frame: FirstDeploymentFrame, entry: int=25338) -> FirstDeploymentFrame:
    """62FA: original selection-repeat delay, equipment/city refresh and real cursor placement."""
    if entry not in (25338, 25574):
        raise ValueError('actual62FA or63E6 entry required')
    frame = _world_map_frame_fields(state, frame, entry)
    if entry == 25338:
        frame = _movement_test(state, frame, state.read(4294964088, 2), 16)
        if frame.status & 4:
            frame = _city_ui_store_fields(state, frame, 4294964088, 1)
        frame = _movement_move(state, frame, 'target_x', state.read(4294964790, 2), 16)
        frame = _movement_test(state, frame, state.read(4294964822, 2), 16)
        if not frame.status & 4:
            frame = _city_ui_arithmetic_fields(state, frame, 'target_x', 1)
        frame = _city_ui_store_fields(state, frame, 4294964820, low16(frame.target_x))
        frame = _city_ui_bit_fields(state, frame, state.read(4294964738, 1), 0)
        upwards = not bool(frame.status & 4)
        if not upwards:
            frame = _city_ui_bit_fields(state, frame, state.read(4294964738, 1), 1)
            moving = not bool(frame.status & 4)
        else:
            moving = True
        expired = False
        if not moving:
            frame = _city_ui_store_fields(state, frame, 4294964744, 1)
        else:
            frame = _city_ui_memory_arithmetic_fields(state, frame, 4294964744, 1, True)
            expired = bool(frame.status & 4)
            if expired:
                frame = _city_ui_memory_arithmetic_fields(state, frame, 4294964088, 1, upwards)
                if upwards:
                    if frame.status & 4:
                        frame = _city_ui_memory_arithmetic_fields(state, frame, 4294964088, 1)
                else:
                    frame = _movement_move(state, frame, 'target_x', state.read(4294964088, 2), 16)
                    frame = _movement_compare(state, frame, low16(frame.target_x), state.read(4294964820, 2), 16)
                    if not frame.status & 1 and (not frame.status & 4):
                        frame = _city_ui_memory_arithmetic_fields(state, frame, 4294964088, 1, True)
        if expired:
            frame = _movement_compare(state, frame, state.read(4294964076, 2), 1, 16)
            if frame.status & 4:
                frame = _movement_compare(state, frame, state.read(4294964096, 2), 103, 16)
                if frame.status & 4:
                    frame = _movement_move(state, frame, 'target_x', state.read(4294964088, 2), 16)
                    frame = _city_ui_shift_fields(state, frame, 'target_x', 1)
                    frame = first_replace(frame, roster=state.table_at(4294964478).cursor())
                    frame = _city_ui_store_fields(state, frame, 4294964082, frame.roster.word(low16(frame.target_x)))
                    frame = _campaign_ui_call_fields(state, frame, 19122, 25476)
                    frame = _campaign_ui_call_fields(state, frame, 19240, 25482)
                else:
                    frame = _movement_compare(state, frame, state.read(4294964096, 2), 122, 16)
                    if frame.status & 4:
                        frame = _movement_move(state, frame, 'target_x', state.read(4294964088, 2), 16)
                        frame = _city_ui_shift_fields(state, frame, 'target_x', 1)
                        frame = first_replace(frame, roster=state.table_at(4294964478).cursor())
                        frame = _movement_move(state, frame, 'target_x', frame.roster.word(low16(frame.target_x)), 16)
                        frame = _city_ui_shift_fields(state, frame, 'target_x', 2)
                        frame = first_replace(frame, roster=state.table_at(4294952960).cursor())
                        frame = _city_ui_store_fields(state, frame, 4294964206, frame.roster.long(low16(frame.target_x)), 4)
                        frame = _campaign_ui_call_fields(state, frame, 79604, 25524)
            frame = _city_ui_store_fields(state, frame, 4294964744, 8)
        frame = _campaign_ui_call_fields(state, frame, 25610, 25534)
        for bit in (5, 4):
            frame = _city_ui_bit_fields(state, frame, state.read(4294964739, 1), bit)
            if not frame.status & 4:
                return frame
        frame = _movement_move(state, frame, 'target_x', state.read(4294964738, 1), 8)
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 3, 16)
        if frame.status & 4:
            frame = _city_ui_bit_fields(state, frame, state.read(4294964001, 1), 3)
            if frame.status & 4:
                return frame
    frame = _movement_move(state, frame, 'target_x', state.read(4294964088, 2), 16)
    frame = _city_ui_arithmetic_fields(state, frame, 'target_x', state.read(4294964824, 2), True)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)
    frame = _city_ui_shift_fields(state, frame, 'target_x', 1)
    frame = _city_ui_arithmetic_fields(state, frame, 'target_x', low16(frame.target_y))
    frame = _city_ui_shift_fields(state, frame, 'target_x', 3)
    frame = _city_ui_arithmetic_fields(state, frame, 'target_x', 8, True)
    frame = _movement_move(state, frame, 'target_y', 224, 16)
    frame = _movement_move(state, frame, 'unit', 0, 16)
    frame = first_replace(frame, roster=state.table_at(25682).cursor())
    return _campaign_ui_call_fields(state, frame, 44040, 25608)


def _world_cursor_second_force_commit_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """9DC2 shared real second-force commit tail; no invented call/return slot."""
    frame=_campaign_ui_change_bit_fields(state,frame,0xFFFFF31C,1,True)
    frame=_campaign_ui_change_bit_fields(state,frame,0xFFFFF31C,2,False)
    for address,value in ((0xFFFFF612,0x208),(0xFFFFF362,4),(0xFFFFF38C,157),(0xFFFFF65A,6)):
        frame=_city_ui_store_fields(state,frame,address,value)
    return frame


def refresh_world_map_scroll_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """9C36: actual location/object selection, ownership warning and camera/force-mode transitions."""
    frame=_world_map_frame_fields(state,frame,0x9C36)
    frame=_movement_test(state,frame,state.read(0xFFFFF600,2),16)
    if not frame.status&4:
        return frame
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF602,1),6)
    if not frame.status&4:
        frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x202)
        frame=_city_ui_store_fields(state,frame,0xFFFFF352,0,2,True)
        frame=_city_ui_store_fields(state,frame,0xFFFFF354,state.read(0xFFFFF318,2))
        frame=_city_ui_store_fields(state,frame,0xFFFFF356,state.read(0xFFFFF314,2))
        frame=_city_ui_store_fields(state,frame,0xFFFFF358,1)
        frame=_city_ui_store_fields(state,frame,0xFFFFF35C,0,2,True)
        frame=_city_ui_store_fields(state,frame,0xFFFFF350,0,2,True)
        frame=_city_ui_store_fields(state,frame,0xFFFFF376,state.read(0xFFFFF376,2)&15)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if not frame.status&4:
        frame=_campaign_ui_call_fields(state,frame,0x5CC8,0x9C80)
        frame=_movement_compare(state,frame,low16(frame.distance),65535,16)
        if not frame.status&4:
            frame=first_replace(frame,roster=state.table_at(0xFFFFEA38).cursor())
            frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
            frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&63,16)
            frame=_movement_test(state,frame,frame.roster.byte(low16(frame.target_x)),8)
            if frame.status&4:
                frame=_campaign_ui_change_bit_fields(state,frame,0xFFFFF31C,3,True)
                frame=_campaign_ui_change_bit_fields(state,frame,0xFFFFF31C,1,True)
                frame=_campaign_ui_change_bit_fields(state,frame,0xFFFFF31C,2,False)
                frame=_city_ui_store_fields(state,frame,0xFF3938,0,2,True)
                frame=_city_ui_store_fields(state,frame,0xFFFFF38E,1)
                frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF364,1)
                frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x205)
                frame=_campaign_ui_change_bit_fields(state,frame,0xFFFFF3A5,0,False)
                frame=_city_ui_store_fields(state,frame,0xFFFFF378,0,2,True)
                return _city_ui_store_fields(state,frame,0xFFFFF658,0,2,True)
            frame=_movement_move(state,frame,'target_x',197,16)
            frame=first_replace(frame,roster=state.table_at(0xFFFFF428).cursor())
            frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF364,2),16)
            frame=_movement_move(state,frame,'target_y',low16(frame.target_y)&63,16)
            frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_y)),8)
            frame=_movement_compare(state,frame,low16(frame.target_y),state.read(0xFFFFF376,2),16)
            if not frame.status&4:
                frame=_movement_move(state,frame,'target_x',143,16)
            frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x20F)
            return _campaign_ui_call_fields(state,frame,0x676F2,0x9D04)
        frame=_campaign_ui_call_fields(state,frame,0x9E14,0x9D0C)
        if frame.status&1:
            frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x205)
            frame=_city_ui_store_fields(state,frame,0xFFFFF65A,1)
            frame=_city_ui_store_fields(state,frame,0xFF3938,1)
            frame=_movement_compare(state,frame,state.read(0xFFFFF36C,2),2,16)
            if frame.status&4:
                frame=_city_ui_store_fields(state,frame,0xFFFFF38C,151)
                frame=_city_ui_store_fields(state,frame,0xFFFFF576,0,2,True)
            return frame
        frame=_movement_compare(state,frame,state.read(0xFFFFF36C,2),2,16)
        if frame.status&4:
            return _world_cursor_second_force_commit_frame_fields(state,frame)
        frame=_movement_test(state,frame,state.read(0xFFFFF36C,2),16)
        if not frame.status&4:
            return frame
        frame=_campaign_ui_change_bit_fields(state,frame,0xFFFFF31C,3,True)
        frame=_campaign_ui_change_bit_fields(state,frame,0xFFFFF31C,1,True)
        frame=_campaign_ui_change_bit_fields(state,frame,0xFFFFF31C,2,False)
        frame=_city_ui_store_fields(state,frame,0xFFFFF38E,2)
        frame=_city_ui_store_fields(state,frame,0xFFFFF576,0,2,True)
        frame=_city_ui_store_fields(state,frame,0xFFFFF396,0,2,True)
        frame=_city_ui_store_fields(state,frame,0xFFFFF36C,1)
        frame=_campaign_ui_call_fields(state,frame,0x133A,0x9D4E)
        frame=_city_ui_store_fields(state,frame,0xFFFFF65A,0,2,True)
        frame=_city_ui_store_fields(state,frame,0xFFFFCFD2,8)
        frame=_movement_move(state,frame,'target_x',172,16)
        return _campaign_ui_call_fields(state,frame,0x808A,0x9D62)
    frame=_movement_test(state,frame,state.read(0xFFFFF36C,2),16)
    if frame.status&4:
        return frame
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
    if frame.status&4:
        return frame
    frame=_movement_compare(state,frame,state.read(0xFFFFF36C,2),2,16)
    if frame.status&4:
        return _world_cursor_second_force_commit_frame_fields(state,frame)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),64,16)
    if frame.status&4:
        return frame
    frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x208)
    frame=_city_ui_store_fields(state,frame,0xFFFFF362,2)
    frame=_city_ui_store_fields(state,frame,0xFFFFF36A,18)
    frame=_movement_compare(state,frame,state.read(0xFFFFF380,2),99,16)
    if not frame.status&4:
        return frame
    frame=_city_ui_store_fields(state,frame,0xFFFFF612,0x208)
    frame=_city_ui_store_fields(state,frame,0xFFFFF362,10)
    frame=_campaign_ui_change_bit_fields(state,frame,0xFFFFF31C,2,False)
    return _campaign_ui_change_bit_fields(state,frame,0xFFFFF31C,1,True)


def update_world_cursor_from_inputs_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """9E5E: scroll and commit the real cursor, including the original visibility toggle and audio request."""
    frame=_world_map_frame_fields(state,frame,0x9E5E)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF31C,1),1)
    if frame.status&4:
        frame=_movement_compare(state,frame,state.read(0xFFFFF322,2),18,16)
        if frame.status&1:
            frame=_campaign_ui_call_fields(state,frame,0x9F7C,0x9E76)
            frame=_movement_test(state,frame,state.read(0xFFFFF37E,2),16)
            if frame.status&4:
                frame=_city_ui_store_fields(state,frame,0xFFFFF600,44)
    else:
        frame=_movement_test(state,frame,state.read(0xFFFFF322,2),16)
        if not frame.status&4:
            frame=_city_ui_memory_arithmetic_fields(state,frame,0xFFFFF322,2,True)
            frame=_campaign_ui_call_fields(state,frame,0x9F7C,0x9E98)
        else:
            frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF31C,1),3)
            if not frame.status&4:
                frame=_movement_compare(state,frame,state.read(0xFFFFF38E,2),2,16)
                if frame.status&4:
                    frame=_city_ui_store_fields(state,frame,0xFFFFF600,48)
                    frame=_city_ui_store_fields(state,frame,0xFFFFF38A,state.read(0xFFFFF612,2))
                    frame=_city_ui_store_fields(state,frame,0xFFFFF38C,0,2,True)
            else:
                frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF31C,1),2)
                if not frame.status&4:
                    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF360,2),16)
                    frame=_city_ui_arithmetic_fields(state,frame,'target_x',state.read(0xFFFFF318,2),True)
                    frame=_movement_compare(state,frame,low16(frame.target_x),160,16)
                    frame=_campaign_ui_change_bit_fields(state,frame,0xFFFFF31C,0,bool(frame.status&1))
                    frame=_campaign_ui_change_bit_fields(state,frame,0xFFFFF31C,1,False)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),7)
    if not frame.status&4:
        frame=_city_ui_store_fields(state,frame,0xFFFFF31C,state.read(0xFFFFF31C,1)^4,1)
        frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF31C,1),2)
        if not frame.status&4:
            frame=_movement_move(state,frame,'target_x',173,16)
            frame=_campaign_ui_call_fields(state,frame,0x808A,0x9F18)
        frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF31C,1),2)
        if frame.status&4:
            frame=_campaign_ui_change_bit_fields(state,frame,0xFFFFF31C,1,True)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF31C,1),2)
    if frame.status&4:
        return frame
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF360,2),16)
    frame=_city_ui_arithmetic_fields(state,frame,'target_x',state.read(0xFFFFF318,2),True)
    frame=_movement_compare(state,frame,low16(frame.target_x),160,16)
    near_side=bool(frame.status&1)
    frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF31C,1),0)
    set_pending=bool(frame.status&4) if near_side else not bool(frame.status&4)
    return _campaign_ui_change_bit_fields(state,frame,0xFFFFF31C,1,set_pending)


def _world_cursor_attributes_role_frame_fields(state: SceneState, frame: FirstDeploymentFrame,
        skip_animation: bool) -> FirstDeploymentFrame:
    """A14E/A158 share one owner-matching algorithm; the real middle entry only skips its animation BTST."""
    if type(skip_animation) is not bool:
        raise ValueError('original world cursor entry role required')
    frame=_world_map_frame_fields(state,frame,0xA158 if skip_animation else 0xA14E)
    if not skip_animation:
        frame=_city_ui_bit_fields(state,frame,state.read(0xFFFFF321,1),3)
        if not frame.status&4:
            return frame
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
    for address in (0xFFFFF67A,0xFFFFF67C,0xFFFFF67E):
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(address,2),16)
        if frame.status&4:
            frame=first_replace(frame,roster=state.table_at(0xA198).cursor())
            frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF35E,2),16)
            frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF360,2),16)
            frame=_movement_move(state,frame,'unit',0,16)
            frame=_city_ui_store_fields(state,frame,0xFFFFF60A,state.read(0xFFFFF314,2))
            frame=_city_ui_store_fields(state,frame,0xFFFFF60E,state.read(0xFFFFF318,2))
            return _campaign_ui_call_fields(state,frame,0xAC10,0xA196)
    return frame


def refresh_world_cursor_attributes_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _world_cursor_attributes_role_frame_fields(state,frame,False)


def refresh_world_cursor_attributes_alternate_1_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _world_cursor_attributes_role_frame_fields(state,frame,True)


# C59 complete display/order ABI; historical algorithms are projections only.
"""Full growth buckets and initial world-map uploads over the original views.

Confirmed9390..93BE andA1B2..A332. Data directories remain external typed
readonly allocations; all VDP writes, complete-child calls and real stack
saves keep their original order. Missing hardware is never RAM-emulated.
"""
from .contexts_display_fields import (
    display_frame_fields, display_move_fields, display_store_fields,
    display_address_fields, display_shift_word_fields, display_loop_fields,
    display_call_fields, display_status_fields,
)


def clear_officer_growth_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """9390: actual256 score sums and live93BE threshold bucket scan."""
    from .business_movement_support import (
        _movement_compare, _movement_add_word)
    frame = display_frame_fields(state, frame)
    frame = display_address_fields(state, frame, 'roster', 0xFFFFC600)
    frame = display_address_fields(state, frame, 'candidates', 0xFFFFC000)
    frame = display_address_fields(state, frame, 'controller', 0xFFFFBE00)
    frame = display_move_fields(state, frame, 'target_x', 0xFF)
    while True:
        score = frame.candidates.word()
        frame = first_replace(frame, candidates=frame.candidates.advance(2))
        frame = display_move_fields(state, frame, 'target_y', score)
        increment = frame.controller.word()
        frame = first_replace(frame, controller=frame.controller.advance(2))
        frame = _movement_add_word(state, frame, 'target_y', increment)
        frame = display_move_fields(state, frame, 'unit', 1)
        frame = display_address_fields(state, frame, 'scan', 0x93BE)
        while True:
            threshold = frame.scan.word()
            frame = first_replace(frame, scan=frame.scan.advance(2))
            frame = _movement_compare(state, frame, low16(frame.target_y), threshold, 16)
            if frame.status & 1:
                break
            frame = _movement_add_word(state, frame, 'unit', 1)
        frame = display_store_fields(state, frame, 0x93B6,
            frame.roster.base, low8(frame.unit), 1)
        frame = first_replace(frame, roster=frame.roster.advance(1))
        frame, more = display_loop_fields(frame, 'target_x')
        if not more:
            return frame


def initialize_world_map_view_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A1B2: real video initialization, streams,160 LONGs and initial28rows."""
    from .business_movement_support import _movement_move
    frame = display_frame_fields(state, frame)
    frame = display_call_fields(state, frame, 0x6826, 0xA1B8)
    frame = display_store_fields(state, frame, 0xA1B8, 0xFFFFEFC8, 0, clear=True)
    frame = display_call_fields(state, frame, 0x68CE, 0xA1C2)
    frame = display_store_fields(state, frame, 0xA1C2, 0xC00004, 0x8407)
    frame = display_store_fields(state, frame, 0xA1CA,
        0xFFFFF314, state.read(0xFFFFF356, 2))
    frame = display_store_fields(state, frame, 0xA1D0,
        0xFFFFF318, state.read(0xFFFFF354, 2))
    frame = display_store_fields(state, frame, 0xA1D6, 0xC00004, 0x40000000, 4)
    frame = display_address_fields(state, frame, 'roster', 0xCE61E)
    frame = display_address_fields(state, frame, 'candidates', 0xCE49A)
    frame = display_move_fields(state, frame, 'target_x', state.read(0xD34C2, 2))
    frame = display_call_fields(state, frame, 0xADFC, 0xA1F8)
    frame = display_store_fields(state, frame, 0xA1F8, 0xFFFFF37E, 1)
    frame = display_address_fields(state, frame, 'roster', 0xD34CA)
    frame = display_move_fields(state, frame, 'target_x', 0x9F)
    frame = display_store_fields(state, frame, 0xA208, 0xC00004, 0x78000001, 4)
    while True:
        pixels = frame.roster.long()
        frame = first_replace(frame, roster=frame.roster.advance(4))
        frame = display_store_fields(state, frame, 0xA212, 0xC00000, pixels, 4)
        frame, more = display_loop_fields(frame, 'target_x')
        if not more:
            break
    frame = display_store_fields(state, frame, 0xA21C, 0xFFFFF322, 0, clear=True)
    frame = display_store_fields(state, frame, 0xA220, 0xFFFFF612, 0x200)
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    for pc, address in ((0xA228, 0xFFFFF312), (0xA22C, 0xFFFFF316),
            (0xA230, 0xFFFFF602)):
        frame = display_store_fields(state, frame, pc, address, low16(frame.target_x))
    frame = display_store_fields(state, frame, 0xA234, 0xFFFFF31C, 2, 1)
    frame = display_move_fields(state, frame, 'target_x', 1, 32)
    frame = display_call_fields(state, frame, 0x8112, 0xA242)
    frame = display_call_fields(state, frame, 0xA278, 0xA246)
    frame = display_store_fields(state, frame, 0xA246, 0xC00004, 0x8B00)
    frame = display_store_fields(state, frame, 0xA24E, 0xFFFFF6C4, 0, clear=True)
    frame = display_move_fields(state, frame, 'target_x', state.read(0xFFFFF3A4, 2))
    frame = display_move_fields(state, frame, 'target_x', low16(frame.target_x) & 1)
    frame = display_store_fields(state, frame, 0xA25A, 0xFFFFF3A4, low16(frame.target_x))
    frame = display_call_fields(state, frame, 0x52C2, 0xA264)
    frame = display_move_fields(state, frame, 'target_x', state.read(0xFFFFF606, 2))
    frame = display_move_fields(state, frame, 'target_x', low8(frame.target_x) | 0x40, 8)
    frame = display_store_fields(state, frame, 0xA26C, 0xC00004, low16(frame.target_x))
    return display_status_fields(state, frame, 0x2500)


def render_initial_map_rows_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A278: original streams, then29 rows with real8B MOVEM+4CALL slots."""
    from .business_movement_support import _movement_save_longs, _movement_restore_longs
    frame = display_frame_fields(state, frame)
    frame = display_store_fields(state, frame, 0xA278, 0xC00004, 0x40000002, 4)
    frame = display_address_fields(state, frame, 'roster', 0xCFAE2)
    frame = display_address_fields(state, frame, 'candidates', 0xCFA12)
    frame = display_move_fields(state, frame, 'target_x', state.read(0xD34C4, 2))
    frame = display_call_fields(state, frame, 0xADFC, 0xA29A)
    frame = display_store_fields(state, frame, 0xA29A, 0xC00004, 0x40000001, 4)
    frame = display_address_fields(state, frame, 'roster', 0xD139E)
    frame = display_address_fields(state, frame, 'candidates', 0xD12F6)
    frame = display_move_fields(state, frame, 'target_x', state.read(0xD34C8, 2))
    frame = display_call_fields(state, frame, 0xADFC, 0xA2BC)
    frame = display_store_fields(state, frame, 0xA2BC, 0xC00004, 0x60000002, 4)
    frame = display_address_fields(state, frame, 'roster', 0xD1256)
    frame = display_move_fields(state, frame, 'target_x', state.read(0xD34C6, 2))
    while True:
        pixels = frame.roster.long()
        frame = first_replace(frame, roster=frame.roster.advance(4))
        frame = display_store_fields(state, frame, 0xA2D2, 0xC00000, pixels, 4)
        frame, more = display_loop_fields(frame, 'target_x')
        if not more:
            break
    frame = display_move_fields(state, frame, 'target_x', 0x1C)
    frame = display_address_fields(state, frame, 'opponent',
        u32(s16(state.read(0xFFFFF314, 2))))
    while True:
        frame = _movement_save_longs(state, frame, ('target_x', 'opponent'))
        frame = display_move_fields(state, frame, 'target_x', low16(frame.opponent.base))
        frame = display_move_fields(state, frame, 'target_y', state.read(0xFFFFF318, 2))
        frame = display_address_fields(state, frame, 'roster', 0x8155A)
        frame = display_store_fields(state, frame, 0xA2F4, 0xFFFFF328, 0, clear=True)
        frame = display_call_fields(state, frame, 0xAF6A, 0xA2FE)
        frame = display_call_fields(state, frame, 0xB054, 0xA304)
        frame = display_move_fields(state, frame, 'target_x', low16(frame.target_x) | 0xE000)
        frame = display_address_fields(state, frame, 'roster', 0xFFFFD000)
        frame = display_move_fields(state, frame, 'target_y', 0x29)
        frame = display_store_fields(state, frame, 0xA310, frame.roster.base, low16(frame.target_y))
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = display_store_fields(state, frame, 0xA312, frame.roster.base, low16(frame.target_x))
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = display_call_fields(state, frame, 0xB06E, 0xA31A)
        frame = display_store_fields(state, frame, 0xA31A, frame.roster.base, 0, clear=True)
        frame = display_address_fields(state, frame, 'roster', 0xFFFFD000)
        frame = display_call_fields(state, frame, 0xAD1C, 0xA326)
        frame = _movement_restore_longs(state, frame, ('target_x', 'opponent'))
        frame = first_replace(frame, opponent=frame.opponent.advance(8))
        frame, more = display_loop_fields(frame, 'target_x')
        if not more:
            return frame
