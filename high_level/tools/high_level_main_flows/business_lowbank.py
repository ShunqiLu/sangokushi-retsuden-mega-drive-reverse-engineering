"""Structured map/menu/controller logic, mechanically drafted then reviewed.

No instruction decoder, PC state, code array, file reader or media payload is
used at runtime. Ordinary values, typed live views and structured conditionals
retain width/order quirks. This draft is not full CPU or natural-call proof.
"""
from .domain import SceneState, Boundary, u8, u16, u32, s8, s16, low8, low16, replace_byte, replace_word, swap_words, checked_state
from .services import call_target
from dataclasses import replace
from .contexts_tick import MapTickFrame, checked_tick_frame
from .contexts_lowbank import PacketTransferValues
from .contexts_lowbank import (
    PollWorldMapInputInput,
    PollWorldMapInputResult,
    PollWorldMapInputService1,
    UploadWorldMapPaletteInput,
    UploadWorldMapPaletteResult,
    DrawSceneHeaderGlyphsInput,
    DrawSceneHeaderGlyphsResult,
    UploadSelectionLayoutInput,
    UploadSelectionLayoutResult,
    DrawSceneFooterGlyphsInput,
    DrawSceneFooterGlyphsResult,
    DrawCurrentResourceGlyphsInput,
    DrawCurrentResourceGlyphsResult,
    ConfigureControllerOutputsInput,
    ConfigureControllerOutputsResult,
    PollControllerWithZ80BusInput,
    PollControllerWithZ80BusResult,
    PollTwoControllerPortsInput,
    PollTwoControllerPortsResult,
    PollTwoControllerPortsAlternate1Input,
    PollTwoControllerPortsAlternate1Result,
    InitializeZ80SoundImageInput,
    InitializeZ80SoundImageResult,
    ReleaseZ80ResetInput,
    ReleaseZ80ResetResult,
    QueueSoundWordListInput,
    QueueSoundWordListResult,
    InitializeSceneGrowthAndTilesInput,
    InitializeSceneGrowthAndTilesResult,
    InitializeSceneGrowthAndTilesService1,
    PaletteRefreshFields,
    RefreshScenePalettesInput,
    RefreshScenePalettesResult,
    UploadSelectedModeTileRowsInput,
    UploadSelectedModeTileRowsResult,
    UploadSelectedTileRowInput,
    UploadSelectedTileRowResult,
)

def poll_world_map_input(state: SceneState, inputs: PollWorldMapInputInput) -> PollWorldMapInputResult:
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not PollWorldMapInputInput:
        raise ValueError('function-specific typed input required')
    inputs.validate(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=inputs.value, target_y=inputs.field, unit=inputs.tile, choice=inputs.remaining)
    observed=poll_world_map_input_fields(state,incoming)
    return PollWorldMapInputResult(destination=state.table_at(observed.roster.address), source=state.table_at(observed.candidates.address), port=state.table_at(observed.auxiliary.address), value=observed.target_x, field=observed.target_y, tile=observed.unit, remaining=observed.choice, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))


def poll_world_map_input_frame(state: SceneState, frame: MapTickFrame) -> MapTickFrame:
    """Historical MapTick observations delegate 4890; missing A2/A4/A5/CCR stay unobserved."""
    from .business_main import _campaign_legacy_observations_fields
    incoming=_campaign_legacy_observations_fields(state,frame,'world')
    observed=poll_world_map_input_fields(state,incoming)
    return replace(frame,motion_x=observed.target_x,motion_y=observed.target_y,
        attributes=observed.unit,tile_count=observed.count,officer=observed.distance,
        count=observed.offset_x,index=observed.offset_y,control_latch=observed.choice,
        source=state.table_at(observed.roster.address),
        destination=state.table_at(observed.candidates.address),
        packet=state.table_at(observed.controller.address),
        vdp_port=state.table_at(observed.auxiliary.address),stack_cursor=observed.stack_cursor)

def upload_world_map_palette(state: SceneState, inputs: UploadWorldMapPaletteInput) -> UploadWorldMapPaletteResult:
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not UploadWorldMapPaletteInput:
        raise ValueError('function-specific typed input required')
    inputs.validate(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=inputs.value)
    observed=upload_world_map_palette_fields(state,incoming)
    return UploadWorldMapPaletteResult(value=observed.target_x, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))

def draw_scene_header_glyphs(state: SceneState, inputs: DrawSceneHeaderGlyphsInput) -> DrawSceneHeaderGlyphsResult:
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not DrawSceneHeaderGlyphsInput:
        raise ValueError('function-specific typed input required')
    inputs.validate(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,auxiliary=inputs.port.cursor(), target_x=inputs.value, target_y=inputs.field, count=inputs.row, distance=inputs.offset)
    observed=draw_scene_header_glyphs_fields(state,incoming)
    return DrawSceneHeaderGlyphsResult(destination=state.table_at(observed.roster.address), source=state.table_at(observed.candidates.address), value=observed.target_x, field=observed.target_y, row=observed.count, offset=observed.distance, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))

def upload_selection_layout(state: SceneState, inputs: UploadSelectionLayoutInput) -> UploadSelectionLayoutResult:
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not UploadSelectionLayoutInput:
        raise ValueError('function-specific typed input required')
    inputs.validate(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,distance=inputs.offset)
    observed=upload_selection_layout_fields(state,incoming)
    return UploadSelectionLayoutResult(destination=state.table_at(observed.roster.address), offset=observed.distance, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))

def draw_scene_footer_glyphs(state: SceneState, inputs: DrawSceneFooterGlyphsInput) -> DrawSceneFooterGlyphsResult:
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not DrawSceneFooterGlyphsInput:
        raise ValueError('function-specific typed input required')
    inputs.validate(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,auxiliary=inputs.port.cursor(), target_x=inputs.value, target_y=inputs.field, unit=inputs.tile, count=inputs.row)
    observed=draw_scene_footer_glyphs_fields(state,incoming)
    return DrawSceneFooterGlyphsResult(destination=state.table_at(observed.roster.address), source=state.table_at(observed.candidates.address), tile=observed.unit, row=observed.count, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))

def draw_current_resource_glyphs(state: SceneState, inputs: DrawCurrentResourceGlyphsInput) -> DrawCurrentResourceGlyphsResult:
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not DrawCurrentResourceGlyphsInput:
        raise ValueError('function-specific typed input required')
    inputs.validate(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=inputs.value)
    observed=draw_current_resource_glyphs_fields(state,incoming)
    return DrawCurrentResourceGlyphsResult(destination=state.table_at(observed.roster.address), value=observed.target_x, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))

def configure_controller_outputs(state: SceneState, inputs: ConfigureControllerOutputsInput) -> ConfigureControllerOutputsResult:
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not ConfigureControllerOutputsInput:
        raise ValueError('function-specific typed input required')
    inputs.validate(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=configure_controller_outputs_fields(state,incoming)
    return ConfigureControllerOutputsResult(value=observed.target_x, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))

def poll_controller_with_z80_bus(state: SceneState, inputs: PollControllerWithZ80BusInput) -> PollControllerWithZ80BusResult:
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not PollControllerWithZ80BusInput:
        raise ValueError('function-specific typed input required')
    inputs.validate(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=inputs.value, target_y=inputs.field, unit=inputs.tile)
    observed=poll_controller_with_z80_bus_fields(state,incoming)
    return PollControllerWithZ80BusResult(destination=state.table_at(observed.roster.address), source=state.table_at(observed.candidates.address), value=observed.target_x, field=observed.target_y, tile=observed.unit, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))

def poll_two_controller_ports(state: SceneState, inputs: PollTwoControllerPortsInput) -> PollTwoControllerPortsResult:
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not PollTwoControllerPortsInput:
        raise ValueError('function-specific typed input required')
    inputs.validate(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=inputs.value, target_y=inputs.field, unit=inputs.tile)
    observed=poll_two_controller_ports_fields(state,incoming)
    return PollTwoControllerPortsResult(destination=state.table_at(observed.roster.address), source=state.table_at(observed.candidates.address), value=observed.target_x, field=observed.target_y, tile=observed.unit, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))

def poll_two_controller_ports_alternate_1(state: SceneState, inputs: PollTwoControllerPortsAlternate1Input) -> PollTwoControllerPortsAlternate1Result:
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not PollTwoControllerPortsAlternate1Input:
        raise ValueError('function-specific typed input required')
    inputs.validate(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,roster=inputs.destination.cursor(), candidates=inputs.source.cursor(), target_x=inputs.value, target_y=inputs.field, unit=inputs.tile)
    observed=poll_two_controller_ports_alternate_1_fields(state,incoming)
    return PollTwoControllerPortsAlternate1Result(destination=state.table_at(observed.roster.address), source=state.table_at(observed.candidates.address), value=observed.target_x, field=observed.target_y, tile=observed.unit, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))

def initialize_z80_sound_image(state: SceneState, inputs: InitializeZ80SoundImageInput) -> InitializeZ80SoundImageResult:
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not InitializeZ80SoundImageInput:
        raise ValueError('function-specific typed input required')
    inputs.validate(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=inputs.value)
    observed=initialize_z80_sound_image_fields(state,incoming)
    return InitializeZ80SoundImageResult(destination=state.table_at(observed.roster.address), source=state.table_at(observed.candidates.address), value=observed.target_x, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))

def release_z80_reset(state: SceneState, inputs: ReleaseZ80ResetInput) -> ReleaseZ80ResetResult:
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not ReleaseZ80ResetInput:
        raise ValueError('function-specific typed input required')
    inputs.validate(state)
    incoming=FirstDeploymentFrame.unobserved()
    observed=release_z80_reset_fields(state,incoming)
    return ReleaseZ80ResetResult(carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))

def queue_sound_word_list(state: SceneState, inputs: QueueSoundWordListInput) -> QueueSoundWordListResult:
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not QueueSoundWordListInput:
        raise ValueError('function-specific typed input required')
    inputs.validate(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=inputs.value, choice=inputs.remaining)
    observed=queue_sound_word_list_fields(state,incoming)
    return QueueSoundWordListResult(source=state.table_at(observed.scan.address), descriptor=state.table_at(observed.roster.address), records=state.table_at(observed.controller.address), value=observed.target_x, remaining=observed.choice, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))

def initialize_scene_growth_and_tiles(state: SceneState, inputs: InitializeSceneGrowthAndTilesInput) -> InitializeSceneGrowthAndTilesResult:
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not InitializeSceneGrowthAndTilesInput:
        raise ValueError('function-specific typed input required')
    inputs.validate(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,target_x=inputs.value, distance=inputs.offset, choice=inputs.remaining)
    observed=initialize_scene_growth_and_tiles_fields(state,incoming)
    return InitializeSceneGrowthAndTilesResult(destination=state.table_at(observed.roster.address), value=observed.target_x, offset=observed.distance, limit=observed.offset_x, member=observed.offset_y, remaining=observed.choice, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))

def refresh_scene_palettes_fields(state: SceneState) -> PaletteRefreshFields:
    """One A3DA algorithm and exact final CCR, consumed by all observation facades.

    Extend is defined by the original D1 ADDQ, then by D0 ADDQ and LSL2
    only on the palette-step branch. Operands are observed once at their real
    read positions; no facade rereads RAM to reconstruct a lost flag.
    source_if_written=None retains the actual incoming A1 in full facades.
    """
    checked_state(state)
    destination = state.table_at(0xFFFFFB00)
    if state.read(0xFFFFF352, 2) < 32:
        destination = state.table_at(0xFFFFFB80)
    value_word = state.read(0xFFFFEF7A, 2)
    field_total = state.read(0xFFFFEF7C, 2) + 1
    extend = field_total > 65535
    field_word = u16(field_total)
    source_if_written = None
    if field_word >= 6:
        field_word = 0
        value_total = value_word + 1
        extend = value_total > 65535
        value_word = u16(value_total)
        if value_word >= 10:
            value_word = 0
        state.write(0xFFFFEF7A, 2, value_word)
        extend = bool(value_word & 16384)
        value_word = u16(value_word << 2)
        source_if_written = state.table_at(0xA42E)
        first_color = state.read(u32(source_if_written.base + s16(value_word)), 2)
        state.write(u32(destination.base + 50), 2, first_color)
        second_color = state.read(u32(source_if_written.base + s16(value_word) + 2), 2)
        state.write(u32(destination.base + 56), 2, second_color)
        state.write(0xFFFFF31E, 2, 1)
    state.write(0xFFFFEF7C, 2, field_word)
    return PaletteRefreshFields(destination, source_if_written, value_word, field_word,
        False, field_word == 0, bool(field_word & 0x8000), False, extend)


def refresh_scene_palettes(state: SceneState, inputs: RefreshScenePalettesInput) -> RefreshScenePalettesResult:
    """Full incoming carriers projected over the one actual A3DA field core."""
    checked_state(state)
    if type(inputs) is not RefreshScenePalettesInput:
        raise ValueError('function-specific typed input required')
    inputs.validate(state)
    fields = refresh_scene_palettes_fields(state)
    source = inputs.source if fields.source_if_written is None else fields.source_if_written
    return RefreshScenePalettesResult(destination=fields.destination, source=source,
        value=replace_word(inputs.value, fields.value_word),
        field=replace_word(inputs.field, fields.field_word),
        carry=fields.carry, zero=fields.zero, negative=fields.negative, overflow=fields.overflow)

def upload_selected_mode_tile_rows(state: SceneState, inputs: UploadSelectedModeTileRowsInput) -> UploadSelectedModeTileRowsResult:
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not UploadSelectedModeTileRowsInput:
        raise ValueError('function-specific typed input required')
    inputs.validate(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,roster=inputs.destination.cursor(), target_y=inputs.field, unit=inputs.tile, stack_cursor=inputs.stack_cursor)
    observed=upload_selected_mode_tile_rows_fields(state,incoming)
    return UploadSelectedModeTileRowsResult(destination=state.table_at(observed.roster.address), port=state.table_at(observed.auxiliary.address), field=observed.target_y, tile=observed.unit, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))

def upload_selected_tile_row(state: SceneState, inputs: UploadSelectedTileRowInput) -> UploadSelectedTileRowResult:
    """Historical observations project the one current complete core; missing ABI is not invented."""
    checked_state(state)
    if type(inputs) is not UploadSelectedTileRowInput:
        raise ValueError('function-specific typed input required')
    inputs.validate(state)
    incoming=FirstDeploymentFrame.unobserved()
    incoming=first_replace(incoming,roster=inputs.destination.cursor(), auxiliary=inputs.port.cursor(), target_y=inputs.field, unit=inputs.tile)
    observed=upload_selected_tile_row_fields(state,incoming)
    return UploadSelectedTileRowResult(field=observed.target_y, tile=observed.unit, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))


# Actual retained D/A/CCR palette interface; old APIs continue consuming the same unique field algorithm.
from .contexts_gameplay import FirstDeploymentFrame, first_replace

def refresh_scene_palettes_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A3DA complete retained-frame facade: unique core, no internal slot, real caller A7 untouched."""
    from ..high_level_remaining_flows.business_city import _resource_cost_frame
    frame = _resource_cost_frame(state, frame, 0xA3DA)
    fields = refresh_scene_palettes_fields(state).validate(state)
    source = frame.candidates if fields.source_if_written is None else fields.source_if_written.cursor()
    status = (16 if fields.extend else 0) | (1 if fields.carry else 0) | (4 if fields.zero else 0)
    status |= (8 if fields.negative else 0) | (2 if fields.overflow else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, roster=fields.destination.cursor(), candidates=source,
        target_x=replace_word(frame.target_x, fields.value_word),
        target_y=replace_word(frame.target_y, fields.field_word), status=status)


# Complete current campaign/controller successor; real devices remain real boundaries.
"""Actual controller, video-panel and Z80 upload services for campaign UI.

The source includes device paths in full. Missing real bus access is a genuine
boundary, never an invented readiness bit, callback, RAM mirror or successful
device return. The helpers delegate the existing arithmetic and flags cores.
"""


def _campaign_ui_frame_fields(state: SceneState, frame: FirstDeploymentFrame,
        entry: int) -> FirstDeploymentFrame:
    from .business_commands import _city_ui_frame_fields
    return _city_ui_frame_fields(state,frame,entry)


def _campaign_ui_move_fields(state: SceneState, frame: FirstDeploymentFrame,
        carrier: str, value: int, width: int=16) -> FirstDeploymentFrame:
    from .business_movement_support import _movement_move, _movement_move_long
    if width==32:
        return _movement_move_long(state,frame,carrier,value)
    return _movement_move(state,frame,carrier,value,width)


def _campaign_ui_write_fields(state: SceneState, frame: FirstDeploymentFrame,
        pc: int, address: int, value: int, width: int=2, clear: bool=False) -> FirstDeploymentFrame:
    from .business_main import _campaign_emit_fields
    return _campaign_emit_fields(state,frame,pc,address,value,width,clear)


def _campaign_ui_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, token: int) -> FirstDeploymentFrame:
    from .business_main import _campaign_call_fields
    return _campaign_call_fields(state,frame,target,token)


def _campaign_ui_bit_fields(state: SceneState, frame: FirstDeploymentFrame,
        value: int, bit: int) -> FirstDeploymentFrame:
    from .business_map import _world_map_bit_fields
    return _world_map_bit_fields(state,frame,value,bit)


def _campaign_ui_shift_fields(state: SceneState, frame: FirstDeploymentFrame,
        carrier: str, amount: int) -> FirstDeploymentFrame:
    from .business_scene_support import _aux_text_shift_word_fields
    return _aux_text_shift_word_fields(state,frame,carrier,amount)


def _campaign_ui_arithmetic_fields(state: SceneState, frame: FirstDeploymentFrame,
        carrier: str, value: int, subtract: bool=False) -> FirstDeploymentFrame:
    from .business_commands import _city_ui_arithmetic_fields
    return _city_ui_arithmetic_fields(state,frame,carrier,value,subtract)


def _campaign_ui_loop_fields(frame: FirstDeploymentFrame,
        carrier: str) -> tuple[FirstDeploymentFrame, bool]:
    """The DBRA WORD decrement never changes the actual CCR or register high WORD."""
    remaining=u16(low16(frame.carrier(carrier))-1)
    return first_replace(frame,**{carrier:replace_word(frame.carrier(carrier),remaining)}),remaining!=65535


def _campaign_ui_negate_word_fields(state: SceneState, frame: FirstDeploymentFrame,
        carrier: str) -> FirstDeploymentFrame:
    from .business_movement_support import _movement_binary_flags
    frame,value=_movement_binary_flags(state,frame,0,low16(frame.carrier(carrier)),16,True)
    return first_replace(frame,**{carrier:replace_word(frame.carrier(carrier),value)})


def _campaign_ui_controller_shift_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """6800 LSL.B #2,D0 shares the BYTE arithmetic core; logical shift clears V."""
    from .business_movement_support import _movement_binary_flags
    for step in range(2):
        value=low8(frame.target_x)
        frame,value=_movement_binary_flags(state,frame,value,value,8)
        frame=first_replace(frame,target_x=replace_byte(frame.target_x,value))
    status=frame.status&29
    state.sr=(state.sr&65504)|status
    return first_replace(frame,status=status)


def _campaign_ui_port_read_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """67F6..6826: read one real controller and append held/pressed BYTEs."""
    frame = _campaign_ui_write_fields(state, frame, 26614, frame.candidates.base, 0, 1)
    frame = _campaign_ui_move_fields(state, frame, 'target_x', frame.candidates.byte(), 8)
    frame = _campaign_ui_controller_shift_fields(state, frame)
    frame = _campaign_ui_move_fields(state, frame, 'target_x', low8(frame.target_x) & 192, 8)
    frame = _campaign_ui_write_fields(state, frame, 26630, frame.candidates.base, 64, 1)
    frame = _campaign_ui_move_fields(state, frame, 'target_y', frame.candidates.byte(), 8)
    frame = _campaign_ui_move_fields(state, frame, 'target_y', low8(frame.target_y) & 63, 8)
    frame = _campaign_ui_move_fields(state, frame, 'target_x', low8(frame.target_x) | low8(frame.target_y), 8)
    frame = _campaign_ui_move_fields(state, frame, 'target_x', low8(frame.target_x) ^ 255, 8)
    frame = _campaign_ui_move_fields(state, frame, 'target_y', low8(frame.target_x), 8)
    frame = _campaign_ui_move_fields(state, frame, 'unit', frame.roster.byte(), 8)
    frame = _campaign_ui_move_fields(state, frame, 'target_x', low8(frame.target_x) ^ low8(frame.unit), 8)
    frame = _campaign_ui_write_fields(state, frame, 26654, frame.roster.base, low8(frame.target_y), 1)
    frame = first_replace(frame, roster=frame.roster.advance(1))
    frame = _campaign_ui_move_fields(state, frame, 'target_x', low8(frame.target_x) & low8(frame.target_y), 8)
    frame = _campaign_ui_write_fields(state, frame, 26658, frame.roster.base, low8(frame.target_x), 1)
    return first_replace(frame, roster=frame.roster.advance(1))


def configure_controller_outputs_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """67B4..67CA: original MOVEQ and the three controller direction BYTEs."""
    frame=_campaign_ui_frame_fields(state,frame,0x67B4)
    frame=_campaign_ui_move_fields(state,frame,'target_x',64,32)
    frame=_campaign_ui_write_fields(state,frame,0x67B6,0xA10009,low8(frame.target_x),1)
    frame=_campaign_ui_write_fields(state,frame,0x67BC,0xA1000B,low8(frame.target_x),1)
    return _campaign_ui_write_fields(state,frame,0x67C2,0xA1000D,low8(frame.target_x),1)


def poll_controller_with_z80_bus_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """67CA..67E8: acquire the real Z80 bus, poll both controllers, and release it."""
    frame=_campaign_ui_frame_fields(state,frame,0x67CA)
    frame=_campaign_ui_write_fields(state,frame,0x67CA,0xA11100,256)
    while True:
        frame=_campaign_ui_bit_fields(state,frame,state.read(0xA11100,1),0)
        if frame.status&4:
            break
    frame=_campaign_ui_call_fields(state,frame,0x67E8,0x67DE)
    return _campaign_ui_write_fields(state,frame,0x67DE,0xA11100,0)


def poll_two_controller_ports_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """67E8: real first-port BSR then fall through the same second-port algorithm."""
    frame=_campaign_ui_frame_fields(state,frame,0x67E8)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF602).cursor(),
        candidates=state.table_at(0xA10003).cursor())
    frame=_campaign_ui_call_fields(state,frame,0x67F6,0x67F4)
    frame=first_replace(frame,candidates=frame.candidates.advance(2))
    return _campaign_ui_port_read_fields(state,frame)


def poll_two_controller_ports_alternate_1_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """67F6 actual alternate entry uses passed A0/A1 and no fictional parent BSR."""
    frame=_campaign_ui_frame_fields(state,frame,0x67F6)
    return _campaign_ui_port_read_fields(state,frame)


def release_z80_reset_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """69B8..69D2: real reset writes separated by the four original NOPs."""
    frame=_campaign_ui_frame_fields(state,frame,0x69B8)
    frame=_campaign_ui_write_fields(state,frame,0x69B8,0xA11200,0)
    return _campaign_ui_write_fields(state,frame,0x69C8,0xA11200,256)


def initialize_z80_sound_image_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """6950..69AA: copy the three genuine readonly sound regions through the actual bus."""
    frame = _campaign_ui_frame_fields(state, frame, 26960)
    frame = _campaign_ui_write_fields(state, frame, 26960, 10555648, 256)
    frame = _campaign_ui_call_fields(state, frame, 27064, 26972)
    while True:
        frame = _campaign_ui_bit_fields(state, frame, state.read(10555648, 1), 0)
        if frame.status & 4:
            break
    frame = first_replace(frame, roster=state.table_at(27090).cursor(), candidates=state.table_at(10485760).cursor())
    frame = _campaign_ui_move_fields(state, frame, 'target_x', 4095)
    while True:
        value = frame.roster.byte()
        frame = first_replace(frame, roster=frame.roster.advance(1))
        frame = _campaign_ui_write_fields(state, frame, 26998, frame.candidates.base, value, 1)
        frame = first_replace(frame, candidates=frame.candidates.advance(1))
        frame, more = _campaign_ui_loop_fields(frame, 'target_x')
        if not more:
            break
    frame = first_replace(frame, roster=state.table_at(31132).cursor())
    frame = _campaign_ui_move_fields(state, frame, 'target_x', 3583)
    while True:
        value = frame.roster.byte()
        frame = first_replace(frame, roster=frame.roster.advance(1))
        frame = _campaign_ui_write_fields(state, frame, 27014, frame.candidates.base, value, 1)
        frame = first_replace(frame, candidates=frame.candidates.advance(1))
        frame, more = _campaign_ui_loop_fields(frame, 'target_x')
        if not more:
            break
    frame = first_replace(frame, roster=state.table_at(27050).cursor(), candidates=state.table_at(10492928).cursor())
    frame = _campaign_ui_move_fields(state, frame, 'target_x', 12, 32)
    while True:
        value = frame.roster.byte()
        frame = first_replace(frame, roster=frame.roster.advance(1))
        frame = _campaign_ui_write_fields(state, frame, 27032, frame.candidates.base, value, 1)
        frame = first_replace(frame, candidates=frame.candidates.advance(1))
        frame, more = _campaign_ui_loop_fields(frame, 'target_x')
        if not more:
            break
    frame = _campaign_ui_call_fields(state, frame, 27064, 27040)
    return _campaign_ui_write_fields(state, frame, 27040, 10555648, 0)


def upload_world_map_palette_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4998..49D6: original signed scroll values and paired video-plane coordinates."""
    frame=_campaign_ui_frame_fields(state,frame,0x4998)
    frame=_campaign_ui_write_fields(state,frame,0x4998,0xC00004,0x7C000002,4)
    frame=_campaign_ui_move_fields(state,frame,'target_x',state.read(0xFFFFF316,2))
    frame=_campaign_ui_negate_word_fields(state,frame,'target_x')
    frame=_campaign_ui_write_fields(state,frame,0x49A8,0xC00000,low16(frame.target_x))
    frame=_campaign_ui_move_fields(state,frame,'target_x',state.read(0xFFFFF318,2))
    frame=_campaign_ui_negate_word_fields(state,frame,'target_x')
    frame=_campaign_ui_write_fields(state,frame,0x49B4,0xC00000,low16(frame.target_x))
    frame=_campaign_ui_write_fields(state,frame,0x49BA,0xC00004,0x40000010,4)
    frame=_campaign_ui_write_fields(state,frame,0x49C4,0xC00000,state.read(0xFFFFF312,2))
    return _campaign_ui_write_fields(state,frame,0x49CC,0xC00000,state.read(0xFFFFF314,2))


def _campaign_ui_copy_panel_longs_fields(state: SceneState, frame: FirstDeploymentFrame, source_carrier: str, count_carrier: str, instruction: int, destination: int) -> FirstDeploymentFrame:
    """One structured DBRA panel row, retaining real cursors and ordered LONG DATA."""
    if source_carrier not in ('roster', 'candidates'):
        raise ValueError('only original roster/candidates panel source views are admitted')
    while True:
        source = state.checked_table(getattr(frame, source_carrier))
        value = source.long()
        frame = first_replace(frame, **{source_carrier: source.advance(4)})
        frame = _campaign_ui_write_fields(state, frame, instruction, destination, value, 4)
        frame, more = _campaign_ui_loop_fields(frame, count_carrier)
        if not more:
            return frame


def draw_scene_header_glyphs_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5204..5242: decode the two genuine header runs, then transfer their full tile buffer."""
    frame = _campaign_ui_frame_fields(state, frame, 20996)
    frame = first_replace(frame, roster=state.table_at(565756).cursor(), candidates=state.table_at(4294955776).cursor())
    frame = _campaign_ui_move_fields(state, frame, 'count', 1)
    frame = _campaign_ui_call_fields(state, frame, 44682, 21016)
    frame = first_replace(frame, roster=state.table_at(565760).cursor())
    frame = _campaign_ui_move_fields(state, frame, 'count', 9)
    frame = _campaign_ui_call_fields(state, frame, 44682, 21032)
    frame = _campaign_ui_write_fields(state, frame, 21032, 12582916, 1509949440, 4)
    frame = first_replace(frame, candidates=state.table_at(4294955776).cursor())
    frame = _campaign_ui_move_fields(state, frame, 'distance', 383)
    return _campaign_ui_copy_panel_longs_fields(state, frame, 'candidates', 'distance', 21050, frame.auxiliary.base)


def upload_selection_layout_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """52C2..5330: original static rows, uniform third row and final readonly packet."""
    frame=_campaign_ui_frame_fields(state,frame,0x52C2)
    frame=_campaign_ui_write_fields(state,frame,0x52C2,0xC00004,0x70000001,4)
    frame=first_replace(frame,roster=state.table_at(0x89DDC).cursor())
    frame=_campaign_ui_move_fields(state,frame,'distance',23)
    frame=_campaign_ui_copy_panel_longs_fields(state,frame,'roster','distance',0x52D6,0xC00000)
    frame=_campaign_ui_write_fields(state,frame,0x52E0,0xC00004,0x70A00001,4)
    frame=first_replace(frame,roster=state.table_at(0x89F5C).cursor())
    frame=_campaign_ui_move_fields(state,frame,'distance',7)
    frame=_campaign_ui_copy_panel_longs_fields(state,frame,'roster','distance',0x52F4,0xC00000)
    frame=_campaign_ui_write_fields(state,frame,0x52FE,0xC00004,0x72000001,4)
    frame=_campaign_ui_move_fields(state,frame,'distance',7)
    while True:
        frame=_campaign_ui_write_fields(state,frame,0x530C,0xC00000,0x33333333,4)
        frame,more=_campaign_ui_loop_fields(frame,'distance')
        if not more:
            break
    frame=first_replace(frame,roster=state.table_at(0x8A0BC).cursor())
    frame=_campaign_ui_move_fields(state,frame,'distance',7)
    return _campaign_ui_copy_panel_longs_fields(state,frame,'roster','distance',0x5324,0xC00000)


def draw_scene_footer_glyphs_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5370..539E: the original strip decode and 80-LONG transfer."""
    frame = _campaign_ui_frame_fields(state, frame, 21360)
    frame = first_replace(frame, roster=state.table_at(566310).cursor(), candidates=state.table_at(4294955776).cursor())
    frame = _campaign_ui_move_fields(state, frame, 'count', 9)
    frame = _campaign_ui_call_fields(state, frame, 44830, 21380)
    frame = _campaign_ui_write_fields(state, frame, 21380, 12582916, 1891631105, 4)
    frame = first_replace(frame, candidates=state.table_at(4294955776).cursor())
    frame = _campaign_ui_move_fields(state, frame, 'unit', 79)
    return _campaign_ui_copy_panel_longs_fields(state, frame, 'candidates', 'unit', 21398, frame.auxiliary.base)


def draw_current_resource_glyphs_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """55B0..55D0: the actual 24-LONG resource caption upload."""
    frame=_campaign_ui_frame_fields(state,frame,0x55B0)
    frame=first_replace(frame,roster=state.table_at(0x89EFC).cursor())
    frame=_campaign_ui_write_fields(state,frame,0x55B6,0xC00004,0x67A00001,4)
    frame=_campaign_ui_move_fields(state,frame,'target_x',23)
    return _campaign_ui_copy_panel_longs_fields(state,frame,'roster','target_x',0x55C4,0xC00000)


def queue_sound_word_list_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """80F4..8112: descriptor index, original signed destination and LONG word-list copy."""
    frame = _campaign_ui_frame_fields(state, frame, 33012)
    frame = first_replace(frame, candidates=state.table_at(33068).cursor())
    frame = _campaign_ui_shift_fields(state, frame, 'target_x', 3)
    frame = first_replace(frame, candidates=frame.candidates.advance(s16(low16(frame.target_x))))
    source = frame.candidates.long()
    frame = first_replace(frame, controller=state.table_at(source).cursor(), candidates=frame.candidates.advance(4))
    target = s16(frame.candidates.word()) & 4294967295
    frame = first_replace(frame, scan=state.table_at(target).cursor(), candidates=frame.candidates.advance(2))
    frame = first_replace(frame, scan=state.table_at(u32(frame.scan.base + 128)).cursor())
    frame = _campaign_ui_move_fields(state, frame, 'choice', frame.candidates.word())
    frame = first_replace(frame, candidates=frame.candidates.advance(2))
    while True:
        value = frame.controller.long()
        frame = first_replace(frame, controller=frame.controller.advance(4))
        frame = _campaign_ui_write_fields(state, frame, 33030, frame.scan.address(), value, 4)
        frame = first_replace(frame, scan=frame.scan.advance(4))
        frame, more = _campaign_ui_loop_fields(frame, 'choice')
        if not more:
            break
    from .business_commands import _city_ui_memory_arithmetic_fields
    return _city_ui_memory_arithmetic_fields(state, frame, 4294963998, 1)


def upload_selected_tile_row_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A78E..A79E: eight WORDs from passed A0/D2, keeping each real video write."""
    frame = _campaign_ui_frame_fields(state, frame, 42894)
    frame = _campaign_ui_move_fields(state, frame, 'target_y', 7)
    while True:
        value = frame.roster.word(low16(frame.unit))
        frame = _campaign_ui_write_fields(state, frame, 42898, frame.auxiliary.base, value)
        frame = _campaign_ui_arithmetic_fields(state, frame, 'unit', 2)
        frame, more = _campaign_ui_loop_fields(frame, 'target_y')
        if not more:
            return frame


def upload_selected_mode_tile_rows_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """A760..A78E: saved actual A0, two tile rows and original LSL.W #5 mode index."""
    frame = _campaign_ui_frame_fields(state, frame, 42848)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, frame.roster.base)
    frame = first_replace(frame, stack_cursor=stack)
    from .business_movement_support import _movement_test_long
    frame = _movement_test_long(state, frame, frame.roster.base)
    frame = first_replace(frame, auxiliary=state.table_at(12582912).cursor(), roster=state.table_at(42910).cursor())
    frame = _campaign_ui_move_fields(state, frame, 'unit', state.read(4294964048, 2))
    frame = _campaign_ui_shift_fields(state, frame, 'unit', 5)
    frame = _campaign_ui_write_fields(state, frame, 42866, 12582916, 1092616195, 4)
    frame = _campaign_ui_call_fields(state, frame, 42894, 42878)
    frame = _campaign_ui_write_fields(state, frame, 42878, 12582916, 1101004803, 4)
    frame = _campaign_ui_call_fields(state, frame, 42894, 42890)
    restored = frame.stack_cursor.long()
    return first_replace(frame, roster=state.table_at(restored).cursor(), stack_cursor=frame.stack_cursor.advance(4))


def poll_world_map_input_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4890..4942: controller polling and the two genuine DMA command sequences."""
    from .business_movement_support import _movement_test
    frame = _campaign_ui_frame_fields(state, frame, 18576)
    frame = _campaign_ui_call_fields(state, frame, 26570, 18582)
    frame = first_replace(frame, auxiliary=state.table_at(12582916).cursor())
    frame = _campaign_ui_move_fields(state, frame, 'choice', state.read(4294964742, 2))
    frame = _campaign_ui_move_fields(state, frame, 'choice', low8(frame.choice) | 16, 8)
    frame = _campaign_ui_write_fields(state, frame, 18596, frame.auxiliary.base, low16(frame.choice))
    frame = _campaign_ui_write_fields(state, frame, 18598, 10555648, 256)
    frame = _campaign_ui_write_fields(state, frame, 18606, frame.auxiliary.base, 2483131200, 4)
    frame = _campaign_ui_write_fields(state, frame, 18612, frame.auxiliary.base, 2533135616, 4)
    frame = _campaign_ui_write_fields(state, frame, 18618, frame.auxiliary.base, 38783)
    frame = _campaign_ui_write_fields(state, frame, 18622, frame.auxiliary.base, 30720)
    frame = _campaign_ui_write_fields(state, frame, 18626, 4294964768, 130)
    frame = _campaign_ui_write_fields(state, frame, 18632, frame.auxiliary.base, state.read(4294964768, 2))
    frame = _movement_test(state, frame, state.read(16727808, 1), 8)
    if frame.status & 4:
        frame = _campaign_ui_write_fields(state, frame, 18644, 10555648, 0)
    frame = _campaign_ui_write_fields(state, frame, 18652, frame.auxiliary.base, state.read(4294964742, 2))
    frame = _movement_test(state, frame, state.read(4294963998, 2), 16)
    if not frame.status & 4:
        frame = first_replace(frame, auxiliary=state.table_at(12582916).cursor())
        frame = _campaign_ui_move_fields(state, frame, 'choice', state.read(4294964742, 2))
        frame = _campaign_ui_move_fields(state, frame, 'choice', low8(frame.choice) | 16, 8)
        frame = _campaign_ui_write_fields(state, frame, 18678, frame.auxiliary.base, low16(frame.choice))
        frame = _campaign_ui_write_fields(state, frame, 18680, 10555648, 256)
        frame = _campaign_ui_write_fields(state, frame, 18688, frame.auxiliary.base, 2483065664, 4)
        frame = _campaign_ui_write_fields(state, frame, 18694, frame.auxiliary.base, 2533201280, 4)
        frame = _campaign_ui_write_fields(state, frame, 18700, frame.auxiliary.base, 38783)
        frame = _campaign_ui_write_fields(state, frame, 18704, frame.auxiliary.base, 49152)
        frame = _campaign_ui_write_fields(state, frame, 18708, 4294964768, 128)
        frame = _campaign_ui_write_fields(state, frame, 18714, frame.auxiliary.base, state.read(4294964768, 2))
        frame = _movement_test(state, frame, state.read(16727808, 1), 8)
        if frame.status & 4:
            frame = _campaign_ui_write_fields(state, frame, 18726, 10555648, 0)
        frame = _campaign_ui_write_fields(state, frame, 18734, frame.auxiliary.base, state.read(4294964742, 2))
        frame = _campaign_ui_write_fields(state, frame, 18738, 4294963998, 0, clear=True)
    frame = _campaign_ui_call_fields(state, frame, 18966, 18746)
    return _campaign_ui_call_fields(state, frame, 44294, 18752)


def initialize_scene_growth_and_tiles_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """93F0..949E: real initial tile image, four layout rows and controller-region option."""
    from .business_movement_support import _movement_arithmetic_long
    frame=_campaign_ui_frame_fields(state,frame,0x93F0)
    state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_campaign_ui_move_fields(state,frame,'target_x',state.read(0xFFFFF606,2))
    frame=_campaign_ui_move_fields(state,frame,'target_x',low8(frame.target_x)&191,8)
    frame=_campaign_ui_write_fields(state,frame,0x93FC,0xC00004,low16(frame.target_x))
    frame=_campaign_ui_call_fields(state,frame,0x68CE,0x9408)
    frame=_campaign_ui_write_fields(state,frame,0x9408,0xC00004,0x40000000,4)
    frame=first_replace(frame,roster=state.table_at(0x9556).cursor())
    frame=_campaign_ui_move_fields(state,frame,'target_x',439)
    frame=_campaign_ui_copy_panel_longs_fields(state,frame,'roster','target_x',0x941A,0xC00000)
    frame=_campaign_ui_move_fields(state,frame,'offset_x',11,32)
    frame=_campaign_ui_move_fields(state,frame,'offset_y',3,32)
    frame=_campaign_ui_move_fields(state,frame,'distance',0x8001)
    frame=_campaign_ui_move_fields(state,frame,'target_x',0x461C0003,32)
    while True:
        frame=_campaign_ui_move_fields(state,frame,'choice',low16(frame.offset_x))
        frame=_campaign_ui_write_fields(state,frame,0x9434,0xC00004,frame.target_x,4)
        while True:
            frame=_campaign_ui_write_fields(state,frame,0x943A,0xC00000,low16(frame.distance))
            frame=_campaign_ui_arithmetic_fields(state,frame,'distance',1)
            frame,more=_campaign_ui_loop_fields(frame,'choice')
            if not more:
                break
        frame=_movement_arithmetic_long(state,frame,'target_x',0x00800000)
        frame,more=_campaign_ui_loop_fields(frame,'offset_y')
        if not more:
            break
    frame=_campaign_ui_bit_fields(state,frame,state.read(0xA10001,1),7)
    if not frame.status&4:
        frame=_campaign_ui_write_fields(state,frame,0x945C,0xC00004,0x8F02)
        frame=_campaign_ui_write_fields(state,frame,0x9464,0xC00004,0x66300003,4)
        frame=_campaign_ui_write_fields(state,frame,0x946E,0xC00000,0x8035)
        frame=_campaign_ui_write_fields(state,frame,0x9476,0xC00000,0x8036)
    frame=_campaign_ui_move_fields(state,frame,'target_x',0,32)
    frame=_campaign_ui_call_fields(state,frame,0x8112,0x9486)
    frame=_campaign_ui_write_fields(state,frame,0x9486,0xFFFFF618,40)
    frame=_campaign_ui_write_fields(state,frame,0x948C,0xFFFFF608,300)
    state.sr=0x2500
    frame=first_replace(frame,status=0)
    return _campaign_ui_write_fields(state,frame,0x9496,0xFFFFF612,256)
