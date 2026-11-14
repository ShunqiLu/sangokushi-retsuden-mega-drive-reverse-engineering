"""Controller setup, packet economy, command scheduling and glyph layout.

These are logical procedures, not a program-counter dispatcher. Original
numeric vector boundaries remain typed calls; media come from data views.
"""
from dataclasses import replace
from .domain import (SceneState, Table, Cursor, Long, Word, Boundary, uint,
    u8, u16, u32, s16, low8, low16, replace_byte, replace_word, swap_words,
    negative_byte, negative_word, divu_retained, descending_inclusive,
    checked_state, checked_cursor, ram_view, data_view, VideoPlaneAddress)
from .contexts_gameplay import SetupValues, SetupPlane, GameplayCall
from .contexts_scene_support import (CityCommandValues, GlyphTileLayout,
    ScenePresentation, SceneCall, checked_context)



from .services import (
    SceneRefreshMemory,SceneRefreshBoundary,FirstDeploymentFrame,first_replace,
    _first_word,_scene_refresh_emit,_scene_render_compare,sample_random_preserving_seed_fields,
    _presentation_call_fields,BattlePresentationMemory,
)

def _ram(state, name):
    return ram_view(state, 'ram_' + name)


def _word(state, name):
    return _ram(state, name).word()


def _put(state, name, value):
    _ram(state, name).set_word(0, low16(value))


def _call(state, target, values, continuation):
    from .services import call_target
    context = GameplayCall(values, continuation) if type(values) is SetupValues else SceneCall(values, continuation)
    result = call_target(state, u32(target), context)
    if type(result) is not type(values):
        raise Boundary('actual scene call must return its typed operands')
    return result.validate(state)


def _vector(state, values, selector, parameters, base, continuation):
    offset = data_view(state, parameters).word(low16(selector))
    return _call(state, u32(base + s16(offset)), values, continuation)


def _setup_checked(state, values):
    checked_state(state)
    if type(values) is not SetupValues:
        raise ValueError('setup operands required')
    return values.validate(state)


def _setup_sprite(state, values):
    from .services import append_map_sprites
    if values.source is None:
        raise Boundary('real setup sprite source required')
    sprite = append_map_sprites(state, values.source, values.value, values.position,
        values.attributes, reset_scroll=True, initialize_clip=True)
    return replace(values, value=sprite.x, position=sprite.y,
        attributes=sprite.attributes, source=sprite.source)


def refresh_setup_option_labels(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = refresh_setup_option_labels_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)


def render_packed_sprite_position(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = render_packed_sprite_position_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)


def render_setup_player_position(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = render_setup_player_position_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)


def render_selected_setup_options(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = render_selected_setup_options_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)





def cycle_second_player_choice(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = cycle_second_player_choice_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)


def cycle_third_player_choice(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = cycle_third_player_choice_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)


def read_controller_identity(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = read_controller_identity_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)


def update_connected_controller_option(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = update_connected_controller_option_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)


def advance_controller_setup_reveal(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = advance_controller_setup_reveal_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)


def advance_controller_setup_dismissal(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = advance_controller_setup_dismissal_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)


def commit_setup_options(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = commit_setup_options_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)








def run_controller_setup_and_configuration(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = run_controller_setup_and_configuration_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)


def _carry(state, value):
    status = state.read_status_word()
    state.set_status_word(status | 1 if value else status & 0xFFFE)


def locate_selected_ruler_city(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_packet_legacy_entry_fields(state, values)
    returned = locate_selected_ruler_city_fields(state, entered)
    result = _map_packet_legacy_result_fields(state, values, returned)
    return replace(result, scratch=state.table_at(returned.roster.base))


def _packet_location(state, values, packet):
    value = replace_byte(replace_word(values.value, 0), packet.byte(1))
    value = replace_word(value, u16(low16(value) << 4)); _put(state, 'f35e', value)
    value = replace_byte(replace_word(value, 0), packet.byte(2))
    value = replace_word(value, u16(low16(value) << 4)); _put(state, 'f360', value)
    _carry(state, False)
    return replace(values, value=value, packet=packet)


def locate_selected_force_packet(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_packet_legacy_entry_fields(state, values)
    returned = locate_selected_force_packet_fields(state, entered)
    result = _map_packet_legacy_result_fields(state, values, returned)
    return replace(result, packet=returned.roster.cursor())


def _require_packet(values):
    if values.packet is None:
        raise Boundary('live packed-force packet required')
    return values.packet


def calculate_map_packet_supply(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical partial observer projects the one complete packet/turn core; missing fields stay unknown."""
    frame = calculate_map_packet_supply_fields(state, _map_packet_legacy_entry_fields(state, values))
    return _map_packet_legacy_result_fields(state, values, frame)


def sample_map_packet_loss_factors(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical partial observer projects the one complete packet/turn core; missing fields stay unknown."""
    frame = sample_map_packet_loss_factors_fields(state, _map_packet_legacy_entry_fields(state, values))
    return _map_packet_legacy_result_fields(state, values, frame)


def apply_map_packet_supply_losses(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical partial observer projects the one complete packet/turn core; missing fields stay unknown."""
    frame = apply_map_packet_supply_losses_fields(state, _map_packet_legacy_entry_fields(state, values))
    return _map_packet_legacy_result_fields(state, values, frame)


def replace_map_queue_leader(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical partial observer projects the one complete packet/turn core; missing fields stay unknown."""
    frame = replace_map_queue_leader_fields(state, _map_packet_legacy_entry_fields(state, values))
    return _map_packet_legacy_result_fields(state, values, frame)


def remove_map_queue_leader(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical partial observer projects the one complete packet/turn core; missing fields stay unknown."""
    frame = remove_map_queue_leader_fields(state, _map_packet_legacy_entry_fields(state, values))
    return _map_packet_legacy_result_fields(state, values, frame)


def compact_map_packet_survivors(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical partial observer projects the one complete packet/turn core; missing fields stay unknown."""
    frame = compact_map_packet_survivors_fields(state, _map_packet_legacy_entry_fields(state, values))
    return _map_packet_legacy_result_fields(state, values, frame)


def deduct_all_map_packet_supply(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical partial observer projects the one complete packet/turn core; missing fields stay unknown."""
    frame = deduct_all_map_packet_supply_fields(state, _map_packet_legacy_entry_fields(state, values))
    return _map_packet_legacy_result_fields(state, values, frame)


def initialize_force_turn_order(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical partial observer projects the one complete packet/turn core; missing fields stay unknown."""
    frame = initialize_force_turn_order_fields(state, _map_packet_legacy_entry_fields(state, values))
    return _map_packet_legacy_result_fields(state, values, frame)


def shuffle_force_turn_order(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical partial observer projects the one complete packet/turn core; missing fields stay unknown."""
    frame = shuffle_force_turn_order_fields(state, _map_packet_legacy_entry_fields(state, values))
    return _map_packet_legacy_result_fields(state, values, frame)


def select_next_force_turn(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical partial observer projects the one complete packet/turn core; missing fields stay unknown."""
    frame = select_next_force_turn_fields(state, _map_packet_legacy_entry_fields(state, values))
    return _map_packet_legacy_result_fields(state, values, frame)


def recover_idle_officer_readiness(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical partial observer projects the one complete packet/turn core; missing fields stay unknown."""
    frame = recover_idle_officer_readiness_fields(state, _map_packet_legacy_entry_fields(state, values))
    return _map_packet_legacy_result_fields(state, values, frame)


def clear_unassigned_officer_commands(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _map_packet_legacy_entry_fields(state, values)
    returned = clear_unassigned_officer_commands_fields(state, entered)
    return _map_packet_legacy_result_fields(state, values, returned)


def select_next_force_city(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _map_packet_legacy_entry_fields(state, values)
    returned = select_next_force_city_fields(state, entered)
    return _map_packet_legacy_result_fields(state, values, returned)


def select_next_force_map_packet(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _map_packet_legacy_entry_fields(state, values)
    returned = select_next_force_map_packet_fields(state, entered)
    return _map_packet_legacy_result_fields(state, values, returned)


def sample_city_command_policy(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _map_packet_legacy_entry_fields(state, values)
    returned = sample_city_command_policy_fields(state, entered)
    return _map_packet_legacy_result_fields(state, values, returned)


def clear_current_city_project_orders(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _map_packet_legacy_entry_fields(state, values)
    returned = clear_current_city_project_orders_fields(state, entered)
    return _map_packet_legacy_result_fields(state, values, returned)


def build_current_city_officer_roster(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _map_packet_legacy_entry_fields(state, values)
    returned = build_current_city_officer_roster_fields(state, entered)
    return _map_packet_legacy_result_fields(state, values, returned)


def run_city_command_assignment(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _map_packet_legacy_entry_fields(state, values)
    returned = run_city_command_assignment_fields(state, entered)
    return _map_packet_legacy_result_fields(state, values, returned)


def run_city_command_states(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _map_packet_legacy_entry_fields(state, values)
    returned = run_city_command_states_fields(state, entered)
    return _map_packet_legacy_result_fields(state, values, returned)


def run_map_packet_command_states(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _map_packet_legacy_entry_fields(state, values)
    returned = run_map_packet_command_states_fields(state, entered)
    return _map_packet_legacy_result_fields(state, values, returned)


def finish_city_command_assignment(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _map_packet_legacy_entry_fields(state, values)
    returned = finish_city_command_assignment_fields(state, entered)
    return _map_packet_legacy_result_fields(state, values, returned)


def retain_city_command_stage(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _map_packet_legacy_entry_fields(state, values)
    returned = retain_city_command_stage_fields(state, entered)
    return _map_packet_legacy_result_fields(state, values, returned)


def dispatch_city_assignment_state(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _map_packet_legacy_entry_fields(state, values)
    returned = dispatch_city_assignment_state_fields(state, entered)
    return _map_packet_legacy_result_fields(state, values, returned)


def _run_command_stage(state, values, parameters, base, continuation):
    while True:
        value = replace_word(values.value, _word(state, 'f728'))
        values = replace(values, value=value)
        if negative_word(low16(value)):
            return values
        value = replace_word(value, u16((low16(value) - 1) << 1))
        values = _vector(state, replace(values, value=value), value, parameters, base, continuation)


def dispatch_city_command_stage(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_map_packet_legacy_entry_fields(state,values)
    returned=dispatch_city_command_stage_fields(state,entered)
    return _map_packet_legacy_result_fields(state,values,returned)


def dispatch_map_packet_command_stage(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_map_packet_legacy_entry_fields(state,values)
    returned=dispatch_map_packet_command_stage_fields(state,entered)
    return _map_packet_legacy_result_fields(state,values,returned)


def dispatch_auxiliary_command_stage(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_map_packet_legacy_entry_fields(state,values)
    returned=dispatch_auxiliary_command_stage_fields(state,entered)
    return _map_packet_legacy_result_fields(state,values,returned)


def begin_auxiliary_command_stage(state: SceneState, values: CityCommandValues) -> CityCommandValues:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_map_packet_legacy_entry_fields(state,values)
    returned=begin_auxiliary_command_stage_fields(state,entered)
    return _map_packet_legacy_result_fields(state,values,returned)
def _glyph_cursor(state, cursor, role):
    if cursor is None:
        raise Boundary('actual live ' + role + ' cursor required')
    checked_cursor(cursor, state)
    return cursor


def upload_glyph_tile_sequence(state: SceneState, layout: GlyphTileLayout) -> GlyphTileLayout:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_aux_text_legacy_glyph_fields(state,layout)
    returned=upload_glyph_tile_sequence_fields(state,entered)
    return _aux_text_legacy_glyph_result(state,layout,returned)


def expand_glyph_tile_sequence(state: SceneState, layout: GlyphTileLayout) -> GlyphTileLayout:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_aux_text_legacy_glyph_fields(state,layout)
    returned=expand_glyph_tile_sequence_fields(state,entered)
    return _aux_text_legacy_glyph_result(state,layout,returned)


def calculate_glyph_row_layout(state: SceneState, layout: GlyphTileLayout) -> GlyphTileLayout:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_aux_text_legacy_glyph_fields(state,layout)
    returned=calculate_glyph_row_layout_fields(state,entered)
    return _aux_text_legacy_glyph_result(state,layout,returned)


def select_glyph_bitmap(state: SceneState, layout: GlyphTileLayout) -> GlyphTileLayout:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_aux_text_legacy_glyph_fields(state,layout)
    returned=select_glyph_bitmap_fields(state,entered)
    return _aux_text_legacy_glyph_result(state,layout,returned)


def expand_monochrome_glyph_byte(state: SceneState, layout: GlyphTileLayout) -> GlyphTileLayout:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_aux_text_legacy_glyph_fields(state,layout)
    returned=expand_monochrome_glyph_byte_fields(state,entered)
    return _aux_text_legacy_glyph_result(state,layout,returned)


def upload_expanded_glyph_rows(state: SceneState, layout: GlyphTileLayout) -> GlyphTileLayout:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_aux_text_legacy_glyph_fields(state,layout)
    returned=upload_expanded_glyph_rows_fields(state,entered)
    return _aux_text_legacy_glyph_result(state,layout,returned)


def initialize_auxiliary_text_panel(state: SceneState, layout: GlyphTileLayout) -> GlyphTileLayout:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_aux_text_legacy_glyph_fields(state,layout)
    returned=initialize_auxiliary_text_panel_fields(state,entered)
    return _aux_text_legacy_glyph_result(state,layout,returned)


def draw_auxiliary_text_panel_border(state: SceneState, layout: GlyphTileLayout) -> GlyphTileLayout:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_aux_text_legacy_glyph_fields(state,layout)
    returned=draw_auxiliary_text_panel_border_fields(state,entered)
    return _aux_text_legacy_glyph_result(state,layout,returned)


def draw_auxiliary_text_panel_rows(state: SceneState, layout: GlyphTileLayout) -> GlyphTileLayout:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_aux_text_legacy_glyph_fields(state,layout)
    returned=draw_auxiliary_text_panel_rows_fields(state,entered)
    return _aux_text_legacy_glyph_result(state,layout,returned)


def upload_auxiliary_text_panel_glyphs(state: SceneState, layout: GlyphTileLayout) -> GlyphTileLayout:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_aux_text_legacy_glyph_fields(state,layout)
    returned=upload_auxiliary_text_panel_glyphs_fields(state,entered)
    return _aux_text_legacy_glyph_result(state,layout,returned)


def draw_auxiliary_text_panel_markers(state: SceneState, layout: GlyphTileLayout) -> GlyphTileLayout:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_aux_text_legacy_glyph_fields(state,layout)
    returned=draw_auxiliary_text_panel_markers_fields(state,entered)
    return _aux_text_legacy_glyph_result(state,layout,returned)
def _presentation_word(state, name):
    return ram_view(state, 'ram_' + name).word()


def _presentation_store(state, name, value):
    ram_view(state, 'ram_' + name).set_word(0, low16(value))


def _presentation_call(state, target, frame, continuation):
    """A real target/continuation ABI, never a fabricated successful return."""
    from .services import call_target
    result = call_target(state, uint(target, 32), SceneCall(frame, continuation))
    if type(result) is not ScenePresentation:
        raise Boundary('presentation service must return its declared operands')
    return result.validate(state)


def _presentation_video(frame):
    if type(frame.video_address) is not VideoPlaneAddress:
        raise Boundary('this plane entry requires its actual A1 video carrier')
    return frame.video_address


def _presentation_plane_row(state, frame, decoder_continuation):
    """Shared row tail: BYTE comparison, WORD counters, full video addition."""
    from .services import set_vram_write_address
    column = replace_word(frame.tile, u16(low16(frame.tile) + 1))
    frame = replace(frame, tile=column)
    if low8(column) < 32:
        return frame, False
    rows = replace_word(frame.palette, u16(low16(frame.palette) - 1))
    frame = replace(frame, palette=rows)
    if low16(rows) == 0:
        # The inner BSR token is popped into D0 before returning from decoder.
        return replace(frame, command=decoder_continuation), True
    address = _presentation_video(frame).advance_full(frame.stride)
    command = set_vram_write_address(state, address)
    return replace(frame, command=command, tile=0, video_address=address), False


def _presentation_decode_plane_tail(state, frame):
    """The established plane decoder with explicit partial-width carriers.

    The mode/marker gate is live, but the initial marker read happens once.
    Repeated values OR the live mask on every write; DBRA includes count zero
    after a nonzero count packet, and final-row escape precedes that DBRA.
    """
    from .services import set_vram_write_address
    source = frame.source
    checked_cursor(source, state)
    address = _presentation_video(frame)
    state.write(0xC00004, 2, 0x8F02)
    frame = replace(frame, command=set_vram_write_address(state, address), tile=0)
    if _presentation_word(state, '8002') == 0:
        frame = replace(frame, foreground=replace_byte(frame.foreground, source.next_byte()))
    while True:
        value = replace_byte(frame.mode, source.next_byte())
        frame = replace(frame, mode=value)
        literal = (_presentation_word(state, '8002') != 0 or
                   low8(frame.foreground) != low8(value))
        if literal:
            value = replace_word(value, u16(low16(value) << 8))
            value = replace_byte(value, source.next_byte())
            value = replace_word(value, low16(value) | _presentation_word(state, '8000'))
            state.write(0xC00000, 2, low16(value))
            frame, escaped = _presentation_plane_row(state, replace(frame, mode=value), 0x3AB10)
            if escaped:
                return frame
        else:
            count = source.next_byte()  # MOVEQ zero before the BYTE load.
            frame = replace(frame, rows=count)
            if count == 0:
                return frame
            value = replace_byte(frame.mode, source.next_byte())
            value = replace_word(value, u16(low16(value) << 8))
            value = replace_byte(value, source.next_byte())
            frame = replace(frame, mode=value)
            while True:
                value = replace_word(frame.mode, low16(frame.mode) | _presentation_word(state, '8000'))
                state.write(0xC00000, 2, low16(value))
                frame, escaped = _presentation_plane_row(state, replace(frame, mode=value), 0x3AB2C)
                if escaped:
                    return frame
                count = u16(low16(frame.rows) - 1)
                frame = replace(frame, rows=replace_word(frame.rows, count))
                if count == 0xFFFF:
                    break


def decode_unmasked_literal_plane(state: SceneState, frame: ScenePresentation) -> ScenePresentation:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_object_scene_legacy_fields(state,frame)
    returned=decode_unmasked_literal_plane_fields(state,entered)
    return _object_scene_legacy_result(state,frame,returned)


def decode_high_plane_rows(state: SceneState, frame: ScenePresentation) -> ScenePresentation:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_object_scene_legacy_fields(state,frame)
    returned=decode_high_plane_rows_fields(state,entered)
    return _object_scene_legacy_result(state,frame,returned)


def _presentation_full_plane(state, frame):
    """Already-covered3AACE entry, not the high-mask or literal prefix."""
    _presentation_store(state, '8000', 0)
    frame = replace(frame, palette=replace_word(frame.palette, 32))
    _presentation_store(state, '8002', 0)
    return _presentation_decode_plane_tail(state, frame)


def _presentation_swapped_tiles(state, frame):
    """Already-covered swapped-byte tile stream; one initial marker read."""
    from .services import set_vram_write_address
    source = frame.source
    checked_cursor(source, state)
    state.write(0xC00004, 2, 0x8F02)
    command = set_vram_write_address(state, VideoPlaneAddress(low16(frame.command)))
    marker = replace_byte(frame.foreground, source.next_byte())
    frame = replace(frame, command=command, foreground=marker)
    while True:
        low = replace_byte(frame.mode, source.next_byte())
        frame = replace(frame, mode=low)
        if low8(marker) != low8(low):
            pixels = replace_byte(frame.tile, source.next_byte())
            pixels = replace_word(pixels, u16(low16(pixels) << 8))
            pixels = replace_byte(pixels, low8(low))
            state.write(0xC00000, 2, low16(pixels))
            frame = replace(frame, tile=pixels)
        else:
            count = source.next_byte()
            frame = replace(frame, rows=count)
            if count == 0:
                return frame
            low = replace_byte(frame.mode, source.next_byte())
            pixels = replace_byte(frame.tile, source.next_byte())
            pixels = replace_word(pixels, u16(low16(pixels) << 8))
            pixels = replace_byte(pixels, low8(low))
            frame = replace(frame, mode=low, tile=pixels)
            while True:
                state.write(0xC00000, 2, low16(pixels))
                count = u16(low16(frame.rows) - 1)
                frame = replace(frame, rows=replace_word(frame.rows, count))
                if count == 0xFFFF:
                    break


def _presentation_select_tiles(state, frame, directory_name, video_word):
    """Re-read the selector for each distinct original resource directory."""
    selected = replace_word(frame.command, _presentation_word(state, '80da'))
    selected = replace_word(selected, u16(low16(selected) << 2))
    directory = data_view(state, directory_name)
    source = state.table_at(directory.long(low16(selected))).cursor()
    frame = replace(frame, source=source, command=replace_word(selected, video_word))
    return _presentation_swapped_tiles(state, frame)


def _presentation_select_plane(state, frame, directory_name, video_address):
    selected = replace_word(frame.command, _presentation_word(state, '80da'))
    selected = replace_word(selected, u16(low16(selected) << 2))
    directory = data_view(state, directory_name)
    source = state.table_at(directory.long(low16(selected))).cursor()
    frame = replace(frame, source=source, command=selected, destination=None,
                    video_address=VideoPlaneAddress(video_address), stride=0x80)
    return _presentation_full_plane(state, frame)


def _presentation_copy_palette(state, frame):
    """Already-covered palette tail, including signed destination and D7."""
    index = replace_word(frame.command, u16(low16(frame.command) << 3))
    directory = data_view(state, 'data_03abac').cursor(low16(index))
    source = state.table_at(directory.next_long()).cursor()
    destination = state.table_at(u32(s16(directory.next_word()))).cursor()
    count = replace_word(frame.remaining, directory.next_word())
    while True:
        destination.append_long(source.next_long())
        count = replace_word(count, u16(low16(count) - 1))
        if low16(count) == 0xFFFF:
            return replace(frame, command=index, remaining=count,
                           destination=directory, video_address=None,
                           actor=source, opponent=destination)


def initialize_object_scene_video(state: SceneState, frame: ScenePresentation) -> ScenePresentation:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_object_scene_legacy_fields(state,frame)
    returned=initialize_object_scene_video_fields(state,entered)
    return _object_scene_legacy_result(state,frame,returned)


def dispatch_repeating_scene_presentation(state: SceneState, frame: ScenePresentation) -> ScenePresentation:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_object_scene_legacy_fields(state,frame)
    returned=dispatch_repeating_scene_presentation_fields(state,entered)
    return _object_scene_legacy_result(state,frame,returned)


def run_repeating_scene_presentation(state: SceneState, frame: ScenePresentation) -> ScenePresentation:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_object_scene_legacy_fields(state,frame)
    returned=run_repeating_scene_presentation_fields(state,entered)
    return _object_scene_legacy_result(state,frame,returned)


def set_uniform_conservative_orders(state: SceneState, frame: ScenePresentation) -> ScenePresentation:
    """Historical presentation only projects the sole field core; missing X/A7 stay unknown."""
    actual = _scene_formation_legacy_fields(state,frame,0x41bee,False)
    actual = set_uniform_conservative_orders_fields(SceneRefreshMemory(state),actual)
    return _scene_formation_legacy_projection(frame,actual)


def set_first_timed_formation_orders(state: SceneState, frame: ScenePresentation) -> ScenePresentation:
    """Historical presentation only projects the sole field core; missing X/A7 stay unknown."""
    actual = _scene_formation_legacy_fields(state,frame,0x41bf2,False)
    actual = set_first_timed_formation_orders_fields(SceneRefreshMemory(state),actual)
    return _scene_formation_legacy_projection(frame,actual)


def set_mixed_timed_formation_orders(state: SceneState, frame: ScenePresentation) -> ScenePresentation:
    """Historical presentation only projects the sole field core; missing X/A7 stay unknown."""
    actual = _scene_formation_legacy_fields(state,frame,0x41bf6,False)
    actual = set_mixed_timed_formation_orders_fields(SceneRefreshMemory(state),actual)
    return _scene_formation_legacy_projection(frame,actual)


def set_third_timed_formation_orders(state: SceneState, frame: ScenePresentation) -> ScenePresentation:
    """Historical presentation only projects the sole field core; missing X/A7 stay unknown."""
    actual = _scene_formation_legacy_fields(state,frame,0x41bfa,False)
    actual = set_third_timed_formation_orders_fields(SceneRefreshMemory(state),actual)
    return _scene_formation_legacy_projection(frame,actual)


def set_uniform_timed_formation_orders(state: SceneState, frame: ScenePresentation) -> ScenePresentation:
    """Historical presentation only projects the sole field core; missing X/A7 stay unknown."""
    actual = _scene_formation_legacy_fields(state,frame,0x41bfe,False)
    actual = set_uniform_timed_formation_orders_fields(SceneRefreshMemory(state),actual)
    return _scene_formation_legacy_projection(frame,actual)





def choose_first_leader_action(state: SceneState, frame: ScenePresentation) -> ScenePresentation:
    """Historical presentation only projects the sole field core; missing X/A7 stay unknown."""
    actual = _scene_formation_legacy_fields(state,frame,0x41cea,True)
    actual = choose_first_leader_action_fields(SceneRefreshMemory(state),actual)
    return _scene_formation_legacy_projection(frame,actual)


def choose_alternate_first_leader_action(state: SceneState, frame: ScenePresentation) -> ScenePresentation:
    """Historical presentation only projects the sole field core; missing X/A7 stay unknown."""
    actual = _scene_formation_legacy_fields(state,frame,0x41cf6,True)
    actual = choose_alternate_first_leader_action_fields(SceneRefreshMemory(state),actual)
    return _scene_formation_legacy_projection(frame,actual)


def choose_second_leader_action(state: SceneState, frame: ScenePresentation) -> ScenePresentation:
    """Historical presentation only projects the sole field core; missing X/A7 stay unknown."""
    actual = _scene_formation_legacy_fields(state,frame,0x41cee,True)
    actual = choose_second_leader_action_fields(SceneRefreshMemory(state),actual)
    return _scene_formation_legacy_projection(frame,actual)


def choose_third_leader_action(state: SceneState, frame: ScenePresentation) -> ScenePresentation:
    """Historical presentation only projects the sole field core; missing X/A7 stay unknown."""
    actual = _scene_formation_legacy_fields(state,frame,0x41cf2,True)
    actual = choose_third_leader_action_fields(SceneRefreshMemory(state),actual)
    return _scene_formation_legacy_projection(frame,actual)


def choose_fifth_leader_action(state: SceneState, frame: ScenePresentation) -> ScenePresentation:
    """Historical presentation only projects the sole field core; missing X/A7 stay unknown."""
    actual = _scene_formation_legacy_fields(state,frame,0x41cfa,True)
    actual = choose_fifth_leader_action_fields(SceneRefreshMemory(state),actual)
    return _scene_formation_legacy_projection(frame,actual)

def set_scene_object_formation_orders_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, kind: Word) -> FirstDeploymentFrame:
    """41BEE family: five actual branches share three live order writes."""
    if kind not in (0,1,2,3,4):
        raise ValueError('actual formation order branch required')
    memory.frame(frame)
    orders = (5,5,5)
    if kind != 0:
        threshold,early = ((4,(1,1,1)),(5,(1,1,4)),(5,(1,1,1)),(6,(4,4,4)))[kind-1]
        memory.sync_status(frame)
        elapsed = memory.state.read(0xFFFF8160,2)
        frame = _scene_render_compare(memory,frame,elapsed,threshold,16)
        if elapsed < threshold:
            orders = early
    for address,order in ((0xFFFF812A,orders[0]),(0xFFFF812C,orders[1]),(0xFFFF812E,orders[2])):
        frame = _scene_refresh_emit(memory,frame,address,2,order)
    return memory.sync_status(frame)

def _scene_formation_random_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, mask: Word, continuation: Long) -> FirstDeploymentFrame:
    """Five original JSR3B722 sites share the sole RNG and physical save slots."""
    if (mask,continuation) not in ((7, 269592), (3, 269616), (1, 269676), (1, 269696), (1, 269730)):
        raise ValueError("actual Main formation RNG arm required")
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x3B722,frame,continuation)
    def child(actual_memory,entered):
        return sample_random_preserving_seed_fields(SceneRefreshMemory(actual_memory.state),entered)
    frame = _presentation_call_fields(BattlePresentationMemory(memory.state),frame,continuation,child)
    return memory.sync_status(_first_word(frame,'target_x',low16(frame.target_x) & mask))

def choose_scene_object_leader_action_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, kind: Word) -> FirstDeploymentFrame:
    """41CEA family: four complete leader decisions; alternate first shares0.

    Timer and morale reads remain in actual order. Random-first entries read
    the timer only when the masked sample is zero. BRA/JMP aliases add no slot.
    """
    if kind not in (0,1,2,3):
        raise ValueError('actual leader action branch required')
    memory.frame(frame)
    if kind == 0:
        memory.sync_status(frame)
        elapsed = memory.state.read(0xFFFF8160,2)
        frame = _scene_render_compare(memory,frame,elapsed,6,16)
        if elapsed < 6:
            frame = _scene_refresh_emit(memory,frame,0xFFFF8130,2,4)
            frame = _scene_formation_random_fields(memory,frame,3,0x41D30)
            if low16(frame.target_x) == 0:
                frame = _scene_refresh_emit(memory,frame,0xFFFF8130,2,5)
            return memory.sync_status(frame)
        frame = _scene_refresh_emit(memory,frame,0xFFFF8130,2,5)
        morale = memory.state.read(0xFFFF8178,2)
        frame = _scene_render_compare(memory,frame,morale,40,16)
        if morale > 40:
            return memory.sync_status(frame)
        frame = _scene_formation_random_fields(memory,frame,7,0x41D18)
        if low16(frame.target_x) != 0:
            frame = _scene_refresh_emit(memory,frame,0xFFFF8130,2,4)
        return memory.sync_status(frame)
    if kind == 1:
        frame = _scene_refresh_emit(memory,frame,0xFFFF8130,2,4)
        elapsed = memory.state.read(0xFFFF8160,2)
        frame = _scene_render_compare(memory,frame,elapsed,6,16)
        if elapsed < 6:
            return memory.sync_status(frame)
        frame = _scene_refresh_emit(memory,frame,0xFFFF8130,2,1)
        elapsed = memory.state.read(0xFFFF8160,2)
        frame = _scene_render_compare(memory,frame,elapsed,10,16)
        if elapsed >= 10:
            frame = _scene_refresh_emit(memory,frame,0xFFFF8130,2,5)
        morale = memory.state.read(0xFFFF8178,2)
        frame = _scene_render_compare(memory,frame,morale,40,16)
        if morale > 40:
            return memory.sync_status(frame)
        frame = _scene_formation_random_fields(memory,frame,1,0x41D6C)
        if low16(frame.target_x) == 0:
            frame = _scene_refresh_emit(memory,frame,0xFFFF8130,2,4)
        return memory.sync_status(frame)
    continuation = 0x41D80 if kind == 2 else 0x41DA2
    threshold = 5 if kind == 2 else 6
    frame = _scene_formation_random_fields(memory,frame,1,continuation)
    if low16(frame.target_x) != 0:
        return _scene_refresh_emit(memory,frame,0xFFFF8130,2,4)
    elapsed = memory.state.read(0xFFFF8160,2)
    frame = _scene_render_compare(memory,frame,elapsed,threshold,16)
    return _scene_refresh_emit(memory,frame,0xFFFF8130,2,5 if elapsed >= threshold else 4)

def _scene_formation_legacy_fields(state: SceneState, frame: ScenePresentation,
        entry: Long, needs_stack: bool = False) -> FirstDeploymentFrame:
    """Retain only the eight actual observed values/views; X/A7 stay unknown."""
    checked_context(frame,ScenePresentation,state)
    if type(needs_stack) is not bool:
        raise ValueError('actual physical-call requirement required')
    actual = first_replace(FirstDeploymentFrame.unobserved(),
        target_x=frame.command,target_y=frame.foreground,unit=frame.mode,count=frame.rows,
        distance=frame.tile,offset_x=frame.stride,offset_y=frame.palette,choice=frame.remaining,
        roster=frame.source,candidates=frame.destination,
        auxiliary=None if frame.actor is None else frame.actor.cursor(),
        scratch=None if frame.opponent is None else frame.opponent.cursor())
    if needs_stack:
        raise SceneRefreshBoundary(entry,actual,None)
    return actual

def _scene_formation_legacy_projection(frame: ScenePresentation,
        actual: FirstDeploymentFrame) -> ScenePresentation:
    return replace(frame,command=actual.target_x,foreground=actual.target_y,mode=actual.unit,
        rows=actual.count,tile=actual.distance,stride=actual.offset_x,palette=actual.offset_y,
        remaining=actual.choice,source=actual.roster,destination=actual.candidates)

def set_uniform_conservative_orders_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return set_scene_object_formation_orders_fields(memory,frame,0)

def set_first_timed_formation_orders_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return set_scene_object_formation_orders_fields(memory,frame,1)

def set_mixed_timed_formation_orders_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return set_scene_object_formation_orders_fields(memory,frame,2)

def set_third_timed_formation_orders_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return set_scene_object_formation_orders_fields(memory,frame,3)

def set_uniform_timed_formation_orders_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return set_scene_object_formation_orders_fields(memory,frame,4)

def choose_first_leader_action_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return choose_scene_object_leader_action_fields(memory,frame,0)

def choose_alternate_first_leader_action_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return choose_scene_object_leader_action_fields(memory,frame,0)

def choose_second_leader_action_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return choose_scene_object_leader_action_fields(memory,frame,1)

def choose_third_leader_action_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return choose_scene_object_leader_action_fields(memory,frame,2)

def choose_fifth_leader_action_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return choose_scene_object_leader_action_fields(memory,frame,3)


# Sole complete map packet supply, survivor and turn-order algorithms.
from .business_movement_support import (
    _movement_move,_movement_move_long,_movement_test,_movement_test_long,
    _movement_compare,_movement_binary_flags,_movement_arithmetic_long,
    _movement_fixed_shift_word,_movement_shift_long,_movement_add_word,
    _movement_multiply_word,_movement_divu_word,_movement_save_longs,
    _movement_restore_longs,MovementContinuationBoundary,
)
from ..high_level_remaining_flows.business_city import (
    _resource_cost_frame,_settlement_store_word_fields,
    _settlement_write_byte_fields,_special_action_sub_word,
    _special_action_shift_long,_special_action_swap,execute_deployment_menu_fields,
)


def _map_packet_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Actual packet/turn child LONG; reuse one owner and consume the real RTS slot."""
    frame = _resource_cost_frame(state,frame,target)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0,uint(continuation,32))
    entered = first_replace(frame,stack_cursor=stack)
    if target == 0x30C90:
        result = calculate_map_packet_supply_fields(state,entered)
    elif target == 0x30CC2:
        result = apply_map_packet_supply_losses_fields(state,entered)
    elif target == 0x30D7E:
        result = sample_map_packet_loss_factors_fields(state,entered)
    elif target == 0x30DC6:
        result = compact_map_packet_survivors_fields(state,entered)
    elif target == 0x30E34:
        result = replace_map_queue_leader_fields(state,entered)
    elif target == 0x30E7C:
        result = remove_map_queue_leader_fields(state,entered)
    elif target == 0x30EE8:
        result = shuffle_force_turn_order_fields(state,entered)
    elif target == 0x83D4:
        from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
        from ..high_level_battle_ai.business_formation import first_deployment_random_fields
        result = first_deployment_random_fields(BattlePolicyMemory(state),entered)
    else:
        result = execute_deployment_menu_fields(state,target,entered)
    result = _resource_cost_frame(state,result,target)
    actual = result.stack_cursor.long()
    if actual != continuation:
        raise MovementContinuationBoundary(actual,result,'actual map-packet child return LONG changed')
    state.sr = (state.sr & 65504) | result.status
    return first_replace(result,stack_cursor=result.stack_cursor.advance(4))


def _map_packet_divu_fields(state: SceneState, frame: FirstDeploymentFrame,
        carrier: str, divisor: int, instruction: int) -> FirstDeploymentFrame:
    """Only supply and radius DIVUs; immediate MOVE/shift replaces undefined overflow flags."""
    if (carrier,instruction) not in (('count',0x30CB0),('unit',0x30E2C)):
        raise ValueError('original map packet DIVU site required')
    uint(divisor,16)
    if not divisor:
        raise MovementContinuationBoundary(instruction,frame,'original map packet DIVU zero trap')
    if frame.carrier(carrier)//divisor > 65535:
        return frame
    return _movement_divu_word(state,frame,carrier,divisor,instruction)


def _map_packet_survivor_store_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """One survivor emits its actual low BYTE then advances A3 without changing flags."""
    frame = _settlement_write_byte_fields(state,frame,frame.scan,value=low8(frame.distance))
    return first_replace(frame,scan=frame.scan.advance(1))


def _map_packet_lost_message_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """30D3E: two physical WORDs, fifteen MOVEM LONGs, one known message, live readback."""
    stack = frame.stack_cursor.advance(-2)
    value = state.read(0xFFFFF362,2)
    stack.set_word(0,value)
    frame = _movement_test(state,first_replace(frame,stack_cursor=stack),value,16)
    stack = frame.stack_cursor.advance(-2)
    value = state.read(0xFFFFF376,2)
    stack.set_word(0,value)
    frame = _movement_test(state,first_replace(frame,stack_cursor=stack),value,16)
    saved = ('target_x','target_y','unit','count','distance','offset_x','offset_y','choice',
        'roster','candidates','controller','scan','opponent','scratch','auxiliary')
    frame = _movement_save_longs(state,frame,saved)
    frame = _settlement_store_word_fields(state,frame,state.table_at(0xFFFFF376),0,low16(frame.unit))
    frame = _settlement_store_word_fields(state,frame,state.table_at(0xFFFFF3D0),0,low16(frame.distance))
    frame = _settlement_store_word_fields(state,frame,state.table_at(0xFFFFF740),0,202)
    frame = _settlement_store_word_fields(state,frame,state.table_at(0xFFFFF362),0,0,clear=True)
    frame = _map_packet_call_fields(state,frame,0x30A74,0x30D60)
    frame = _movement_restore_longs(state,frame,saved)
    value = frame.stack_cursor.word()
    frame = first_replace(frame,stack_cursor=frame.stack_cursor.advance(2))
    frame = _settlement_store_word_fields(state,frame,state.table_at(0xFFFFF376),0,value)
    value = frame.stack_cursor.word()
    frame = first_replace(frame,stack_cursor=frame.stack_cursor.advance(2))
    return _settlement_store_word_fields(state,frame,state.table_at(0xFFFFF362),0,value)


def calculate_map_packet_supply_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """30C90: sum member LONG troops plus100, divide10, then retained WORD times3."""
    frame = _resource_cost_frame(state,frame,0x30C90)
    frame = first_replace(frame,candidates=state.table_at(0xFFFFC800).cursor())
    frame = _movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame = _special_action_sub_word(state,frame,'target_y',1)
    frame = _movement_move_long(state,frame,'count',0)
    while True:
        frame = _movement_move(state,frame,'unit',0,16)
        frame = _movement_move(state,frame,'unit',frame.roster.byte(low16(frame.target_y),13),8)
        frame = _movement_fixed_shift_word(state,frame,'unit',2)
        frame = _movement_arithmetic_long(state,frame,'count',frame.candidates.long(low16(frame.unit)))
        frame = _movement_arithmetic_long(state,frame,'count',100)
        counter = u16(low16(frame.target_y)-1)
        frame = first_replace(frame,target_y=replace_word(frame.target_y,counter))
        if counter == 65535:
            break
    frame = _map_packet_divu_fields(state,frame,'count',10,0x30CB0)
    frame = _movement_move(state,frame,'unit',low16(frame.count),16)
    frame = _movement_fixed_shift_word(state,frame,'count',1)
    frame = _movement_add_word(state,frame,'count',low16(frame.unit))
    return _movement_move_long(state,frame,'count',frame.count & 65535)


def sample_map_packet_loss_factors_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """30D7E: save D0/D1, two real RNG slots, original6x/501x LONG scaling, restore."""
    frame = _resource_cost_frame(state,frame,0x30D7E)
    frame = _movement_save_longs(state,frame,('target_x','target_y'))
    frame = _map_packet_call_fields(state,frame,0x83D4,0x30D88)
    frame = _movement_move_long(state,frame,'target_x',frame.target_x & 65535)
    frame = _movement_move_long(state,frame,'target_y',frame.target_x)
    frame = _special_action_shift_long(state,frame,'target_x',1)
    frame = _movement_arithmetic_long(state,frame,'target_x',frame.target_y)
    frame = _special_action_shift_long(state,frame,'target_x',1)
    frame = _special_action_swap(state,frame,'target_x')
    frame = _movement_add_word(state,frame,'target_x',5)
    frame = _movement_move(state,frame,'unit',low16(frame.target_x),16)
    frame = _map_packet_call_fields(state,frame,0x83D4,0x30DA2)
    frame = _movement_move_long(state,frame,'target_x',frame.target_x & 65535)
    frame = _movement_move_long(state,frame,'target_y',frame.target_x)
    frame = _movement_shift_long(state,frame,'target_x')
    frame = _special_action_shift_long(state,frame,'target_x',1)
    frame = _movement_arithmetic_long(state,frame,'target_x',frame.target_y,True)
    frame = _special_action_shift_long(state,frame,'target_y',1)
    frame = _movement_arithmetic_long(state,frame,'target_x',frame.target_y,True)
    frame = _special_action_shift_long(state,frame,'target_y',2)
    frame = _movement_arithmetic_long(state,frame,'target_x',frame.target_y,True)
    frame = _special_action_swap(state,frame,'target_x')
    frame = _movement_add_word(state,frame,'target_x',500)
    frame = _movement_move(state,frame,'count',low16(frame.target_x),16)
    return _movement_restore_longs(state,frame,('target_x','target_y'))


def apply_map_packet_supply_losses_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """30CC2: retain every live field while consuming loss factors, survivor writes and nested message."""
    frame = _resource_cost_frame(state,frame,0x30CC2)
    frame = _settlement_store_word_fields(state,frame,state.table_at(0xFFFFCFC8),0,0,clear=True)
    frame = _settlement_write_byte_fields(state,frame,state.table_at(0xFFFFCFC9),value=frame.roster.byte(13))
    frame = _movement_move(state,frame,'choice',0,16)
    frame = first_replace(frame,candidates=state.table_at(0xFFFFC800).cursor(),
        controller=state.table_at(0xFFFFB200),scan=state.table_at(0xFFFFCFB2).cursor(),
        opponent=state.table_at(0xFFFFCC00))
    frame = _movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame = _special_action_sub_word(state,frame,'target_y',1)
    while True:
        frame = _map_packet_call_fields(state,frame,0x30D7E,0x30CE6)
        frame = _movement_move(state,frame,'distance',0,16)
        frame = _movement_move(state,frame,'distance',frame.roster.byte(low16(frame.target_y),13),8)
        frame = _movement_move(state,frame,'offset_x',low16(frame.distance),16)
        frame = _movement_fixed_shift_word(state,frame,'offset_x',1)
        frame = _movement_move(state,frame,'offset_y',frame.controller.word(low16(frame.offset_x)),16)
        frame = _special_action_sub_word(state,frame,'offset_y',low16(frame.unit))
        if not frame.status & 5:
            frame = _settlement_store_word_fields(state,frame,frame.controller,low16(frame.offset_x),low16(frame.offset_y))
            frame = _movement_fixed_shift_word(state,frame,'offset_x',1)
            frame = _movement_move(state,frame,'offset_y',frame.candidates.word(low16(frame.offset_x),2),16)
            frame = _special_action_sub_word(state,frame,'offset_y',low16(frame.count))
            if frame.status & 1:
                frame = _movement_move(state,frame,'offset_y',0,16)
            frame = _settlement_store_word_fields(state,frame,frame.candidates,low16(frame.offset_x),low16(frame.offset_y),2)
            frame = _movement_add_word(state,frame,'choice',1)
            frame = _map_packet_survivor_store_fields(state,frame)
        else:
            frame = _settlement_write_byte_fields(state,frame,frame.opponent,value=255,offset=low16(frame.distance))
            frame = _movement_move(state,frame,'unit',frame.roster.byte(4),8)
            frame = _movement_move(state,frame,'unit',low16(frame.unit) & 15,16)
            selected = False
            for address in (0xFFFFF67A,0xFFFFF67C,0xFFFFF67E):
                frame = _movement_compare(state,frame,low16(frame.unit),state.read(address,2),16)
                if frame.status & 4:
                    selected = True
                    break
            if selected:
                frame = _map_packet_lost_message_fields(state,frame)
        counter = u16(low16(frame.target_y)-1)
        frame = first_replace(frame,target_y=replace_word(frame.target_y,counter))
        if counter == 65535:
            break
    frame = _movement_compare(state,frame,low16(frame.target_x),low16(frame.choice),16)
    if not frame.status & 4:
        frame = _map_packet_call_fields(state,frame,0x30DC6,0x30D7A)
    return _movement_move(state,frame,'target_x',low16(frame.choice),16)


def replace_map_queue_leader_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """30E34: two queue references relabel together, with D0/D1/A0 physical MOVEM preservation."""
    frame = _resource_cost_frame(state,frame,0x30E34)
    saved = ('target_x','target_y','roster')
    frame = _movement_save_longs(state,frame,saved)
    frame = _movement_move(state,frame,'target_x',0,16)
    frame = _movement_move(state,frame,'target_x',frame.roster.byte(13),8)
    frame = _movement_move(state,frame,'target_y',state.read(0xFFFFCFC8,2),16)
    frame = first_replace(frame,roster=state.table_at(0x00FF39B2).cursor())
    while True:
        frame = _movement_test(state,frame,frame.roster.byte(),8)
        if frame.status & 4:
            break
        frame = _movement_compare(state,frame,low8(frame.target_y),frame.roster.byte(1),8)
        if frame.status & 4:
            frame = _settlement_write_byte_fields(state,frame,frame.roster,value=low8(frame.target_x),offset=1)
            frame = first_replace(frame,roster=state.table_at(0x00FF3000).cursor())
            while True:
                frame = first_replace(frame,roster=frame.roster.advance(1))
                frame = _movement_compare(state,frame,low8(frame.target_y),frame.roster.byte(),8)
                if frame.status & 4:
                    break
                frame = first_replace(frame,roster=frame.roster.advance(1))
                while True:
                    value = frame.roster.byte()
                    frame = first_replace(frame,roster=frame.roster.advance(1))
                    frame = _movement_test(state,frame,value,8)
                    if frame.status & 4:
                        break
            frame = _settlement_write_byte_fields(state,frame,frame.roster,value=low8(frame.target_x))
            break
        frame = first_replace(frame,roster=frame.roster.advance(2))
    return _movement_restore_longs(state,frame,saved)


def remove_map_queue_leader_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """30E7C: shift actual ranked priority/member pairs and restore four physical LONGs."""
    frame = _resource_cost_frame(state,frame,0x30E7C)
    saved = ('target_x','target_y','roster','candidates')
    frame = _movement_save_longs(state,frame,saved)
    frame = first_replace(frame,roster=state.table_at(0x00FF39B2).cursor())
    frame = _movement_move(state,frame,'target_x',state.read(0xFFFFCFC8,2),16)
    while True:
        frame = _movement_test(state,frame,frame.roster.byte(),8)
        if frame.status & 4:
            break
        frame = _movement_compare(state,frame,low8(frame.target_x),frame.roster.byte(1),8)
        if frame.status & 4:
            while True:
                value = frame.roster.byte(2)
                frame = _settlement_write_byte_fields(state,frame,frame.roster,value=value)
                if frame.status & 4:
                    break
                frame = _settlement_write_byte_fields(state,frame,frame.roster,value=frame.roster.byte(3),offset=1)
                frame = first_replace(frame,roster=frame.roster.advance(2))
            break
        frame = first_replace(frame,roster=frame.roster.advance(2))
    return _movement_restore_longs(state,frame,saved)


def compact_map_packet_survivors_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """30DC6: reversed survivor order, real leader child, packet-slide tail and BYTE-average radius."""
    frame = _resource_cost_frame(state,frame,0x30DC6)
    frame = _movement_move(state,frame,'offset_y',low16(frame.choice),16)
    if not frame.status & 4:
        frame = _special_action_sub_word(state,frame,'offset_y',1)
        frame = first_replace(frame,candidates=state.table_at(0xFFFFCFB2).cursor())
        while True:
            value = frame.candidates.byte()
            frame = first_replace(frame,candidates=frame.candidates.advance(1))
            frame = _settlement_write_byte_fields(state,frame,frame.roster,value=value,offset=low16(frame.offset_y),displacement=13)
            counter = u16(low16(frame.offset_y)-1)
            frame = first_replace(frame,offset_y=replace_word(frame.offset_y,counter))
            if counter == 65535:
                break
        frame = _settlement_write_byte_fields(state,frame,frame.roster,value=low8(frame.choice))
        frame = _map_packet_call_fields(state,frame,0x30E34,0x30DE0)
        frame = first_replace(frame,candidates=frame.roster.advance(13+s16(low16(frame.target_x))),
            controller=state.table_at(u32(frame.roster.base+13+s16(low16(frame.choice)))))
    else:
        frame = _map_packet_call_fields(state,frame,0x30E7C,0x30DF0)
        frame = first_replace(frame,candidates=frame.roster.advance(13+s16(low16(frame.target_x))),
            controller=state.table_at(frame.roster.base))
    while True:
        frame = _movement_move(state,frame,'target_y',frame.candidates.byte(),8)
        frame = _movement_move(state,frame,'target_y',low16(frame.target_y) & 15,16)
        if frame.status & 4:
            break
        frame = _movement_add_word(state,frame,'target_y',12)
        while True:
            value = frame.candidates.byte()
            frame = first_replace(frame,candidates=frame.candidates.advance(1))
            frame = _settlement_write_byte_fields(state,frame,frame.controller,value=value)
            frame = first_replace(frame,controller=state.table_at(u32(frame.controller.base+1)))
            counter = u16(low16(frame.target_y)-1)
            frame = first_replace(frame,target_y=replace_word(frame.target_y,counter))
            if counter == 65535:
                break
    frame = _settlement_write_byte_fields(state,frame,frame.controller,value=0,clear=True)
    frame = _movement_test(state,frame,low16(frame.choice),16)
    if frame.status & 4:
        return frame
    frame = first_replace(frame,candidates=state.table_at(0xFFFFC400).cursor())
    frame = _movement_move(state,frame,'offset_y',low16(frame.choice),16)
    frame = _special_action_sub_word(state,frame,'offset_y',1)
    frame = _movement_move_long(state,frame,'unit',0)
    frame = _movement_move(state,frame,'count',0,16)
    while True:
        frame = _movement_move(state,frame,'count',frame.roster.byte(low16(frame.offset_y),13),8)
        frame,value = _movement_binary_flags(state,frame,low8(frame.unit),frame.candidates.byte(low16(frame.count)),8)
        frame = first_replace(frame,unit=replace_byte(frame.unit,value))
        counter = u16(low16(frame.offset_y)-1)
        frame = first_replace(frame,offset_y=replace_word(frame.offset_y,counter))
        if counter == 65535:
            break
    frame = _map_packet_divu_fields(state,frame,'unit',low16(frame.choice),0x30E2C)
    return _settlement_write_byte_fields(state,frame,frame.roster,value=low8(frame.unit),offset=3)


def deduct_all_map_packet_supply_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """30C3A: scan compact packets, debit big-endian supply, then process genuine starvation."""
    frame = _resource_cost_frame(state,frame,0x30C3A)
    frame = first_replace(frame,roster=state.table_at(0xFFFF9000).cursor())
    while True:
        frame = _movement_move(state,frame,'target_x',frame.roster.byte(),8)
        frame = _movement_move(state,frame,'target_x',low16(frame.target_x) & 15,16)
        if frame.status & 4:
            return frame
        frame = _map_packet_call_fields(state,frame,0x30C90,0x30C4C)
        frame = _movement_move(state,frame,'unit',frame.roster.byte(9),8)
        frame = _movement_fixed_shift_word(state,frame,'unit',8)
        frame = _movement_move(state,frame,'unit',frame.roster.byte(10),8)
        frame = _movement_shift_long(state,frame,'unit')
        frame = _movement_move(state,frame,'unit',frame.roster.byte(11),8)
        frame = _movement_shift_long(state,frame,'unit')
        frame = _movement_move(state,frame,'unit',frame.roster.byte(12),8)
        frame = _movement_arithmetic_long(state,frame,'unit',frame.count,True)
        if frame.status & 1:
            frame = _map_packet_call_fields(state,frame,0x30CC2,0x30C6C)
            frame = _movement_test(state,frame,low16(frame.target_x),16)
            if frame.status & 4:
                continue
            frame = _movement_move_long(state,frame,'unit',0)
        frame = _settlement_write_byte_fields(state,frame,frame.roster,value=low8(frame.unit),offset=12)
        frame = _movement_shift_long(state,frame,'unit',True)
        frame = _settlement_write_byte_fields(state,frame,frame.roster,value=low8(frame.unit),offset=11)
        frame = _movement_shift_long(state,frame,'unit',True)
        frame = _settlement_write_byte_fields(state,frame,frame.roster,value=low8(frame.unit),offset=10)
        frame = _movement_fixed_shift_word(state,frame,'unit',8,True)
        frame = _settlement_write_byte_fields(state,frame,frame.roster,value=low8(frame.unit),offset=9)
        frame = first_replace(frame,roster=frame.roster.advance(13+s16(low16(frame.target_x))))


def initialize_force_turn_order_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """30EB4: copy the real16-byte force-order DATA, shuffle, and reset turn index/stage."""
    frame = _resource_cost_frame(state,frame,0x30EB4)
    frame = first_replace(frame,roster=state.table_at(0xFFFFF714).cursor(),
        candidates=state.table_at(0x30ED8).cursor())
    frame = _movement_move(state,frame,'target_x',15,16)
    while True:
        value = frame.candidates.byte()
        frame = first_replace(frame,candidates=frame.candidates.advance(1))
        frame = _settlement_write_byte_fields(state,frame,frame.roster,value=value)
        frame = first_replace(frame,roster=frame.roster.advance(1))
        counter = u16(low16(frame.target_x)-1)
        frame = first_replace(frame,target_x=replace_word(frame.target_x,counter))
        if counter == 65535:
            break
    frame = _map_packet_call_fields(state,frame,0x30EE8,0x30ECC)
    frame = _settlement_store_word_fields(state,frame,state.table_at(0xFFFFF724),0,0,clear=True)
    return _settlement_store_word_fields(state,frame,state.table_at(0xFFFFF600),0,176)


def shuffle_force_turn_order_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """30EE8: sixteen real RNG calls, live F61C nibble choices and negative-slot guards."""
    frame = _resource_cost_frame(state,frame,0x30EE8)
    frame = first_replace(frame,roster=state.table_at(0xFFFFF714).cursor())
    frame = _movement_move(state,frame,'choice',15,16)
    while True:
        frame = _map_packet_call_fields(state,frame,0x83D4,0x30EF6)
        frame = _movement_move(state,frame,'target_x',state.read(0xFFFFF61C,2),16)
        frame = _movement_move(state,frame,'target_x',low16(frame.target_x) & 15,16)
        frame = _movement_move(state,frame,'target_y',state.read(0xFFFFF61C,2),16)
        frame = _movement_fixed_shift_word(state,frame,'target_y',8,True)
        frame = _movement_move(state,frame,'target_y',low16(frame.target_y) & 15,16)
        frame = _movement_move(state,frame,'unit',frame.roster.byte(low16(frame.target_x)),8)
        if not frame.status & 8:
            frame = _movement_move(state,frame,'count',frame.roster.byte(low16(frame.target_y)),8)
            if not frame.status & 8:
                frame = _settlement_write_byte_fields(state,frame,frame.roster,value=low8(frame.count),offset=low16(frame.target_x))
                frame = _settlement_write_byte_fields(state,frame,frame.roster,value=low8(frame.unit),offset=low16(frame.target_y))
        counter = u16(low16(frame.choice)-1)
        frame = first_replace(frame,choice=replace_word(frame.choice,counter))
        if counter == 65535:
            return frame


def select_next_force_turn_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """30F26: sign-extend BYTE into WORD, skip inactive rulers and retain finalCLR flags."""
    frame = _resource_cost_frame(state,frame,0x30F26)
    frame = _movement_move(state,frame,'target_x',state.read(0xFFFFF724,2),16)
    frame = first_replace(frame,roster=state.table_at(0xFFFFF714).cursor(),
        candidates=state.table_at(0xFFFFE640).cursor())
    while True:
        frame = _movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
        value = low8(frame.target_y)
        frame = _movement_move(state,frame,'target_y',u16(value-256 if value & 128 else value),16)
        if frame.status & 8:
            break
        frame = _movement_add_word(state,frame,'target_x',1)
        frame = _movement_fixed_shift_word(state,frame,'target_y',1)
        frame = _movement_test(state,frame,frame.candidates.word(low16(frame.target_y)),16)
        if frame.status & 8:
            continue
        frame = _movement_fixed_shift_word(state,frame,'target_y',1,True)
        break
    frame = _settlement_store_word_fields(state,frame,state.table_at(0xFFFFF724),0,low16(frame.target_x))
    frame = _settlement_store_word_fields(state,frame,state.table_at(0xFFFFF376),0,low16(frame.target_y))
    return _settlement_store_word_fields(state,frame,state.table_at(0xFFFFF364),0,0,clear=True)


def recover_idle_officer_readiness_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """30F54: inactive-city officers gain15 percent maximum, preserving highWORDs and live reads."""
    recovery_percent = 15
    frame = _resource_cost_frame(state,frame,0x30F54)
    frame = first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor(),
        scan=state.table_at(0xFFFFB200).cursor(),opponent=state.table_at(0xFFFFB000),
        scratch=state.table_at(0xFFFFEA38))
    frame = _movement_move(state,frame,'target_x',255,16)
    while True:
        frame = _movement_move(state,frame,'target_y',0,16)
        frame = _movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
        frame = _movement_compare(state,frame,low8(frame.target_y),40,8)
        if frame.status & 5:
            frame = _movement_test(state,frame,frame.scratch.byte(low16(frame.target_y)),8)
            if frame.status & 4:
                frame = _movement_move(state,frame,'target_y',low16(frame.target_x),16)
                frame = _movement_fixed_shift_word(state,frame,'target_y',1)
                frame = _movement_move(state,frame,'unit',frame.opponent.word(low16(frame.target_y)),16)
                frame = _movement_multiply_word(state,frame,'unit',recovery_percent)
                frame = _movement_divu_word(state,frame,'unit',100,0x30F8A)
                frame = _movement_move(state,frame,'count',frame.scan.word(low16(frame.target_y)),16)
                frame = _movement_add_word(state,frame,'count',low16(frame.unit))
                frame = _movement_compare(state,frame,low16(frame.count),frame.opponent.word(low16(frame.target_y)),16)
                if not frame.status & 5:
                    frame = _movement_move(state,frame,'count',frame.opponent.word(low16(frame.target_y)),16)
                frame = _settlement_store_word_fields(state,frame,frame.scan,low16(frame.target_y),low16(frame.count))
        counter = u16(low16(frame.target_x)-1)
        frame = first_replace(frame,target_x=replace_word(frame.target_x,counter))
        if counter == 65535:
            return frame


def _map_packet_legacy_entry_fields(state: SceneState, values: CityCommandValues) -> FirstDeploymentFrame:
    """The old observer has8 LONGs but no actual A3/A6/A7; never fabricate retained fields."""
    checked_context(values,CityCommandValues,state)
    return first_replace(FirstDeploymentFrame.unobserved(),target_x=values.value,
        target_y=values.field,unit=values.member,count=values.count,distance=values.readiness_loss,
        offset_x=values.troop_rate,offset_y=values.force_index,choice=values.selected,
        roster=values.packet,candidates=values.roster,controller=values.destination,
        opponent=values.assignments,scratch=values.scratch,status=state.sr & 31)


def _map_packet_legacy_result_fields(state: SceneState, values: CityCommandValues,
        frame: FirstDeploymentFrame) -> CityCommandValues:
    """Only actual numeric results are projected; omitted physical entry fields stay unsupported."""
    return replace(values,value=frame.target_x,field=frame.target_y,member=frame.unit,
        count=frame.count,readiness_loss=frame.distance,troop_rate=frame.offset_x,
        force_index=frame.offset_y,selected=frame.choice)

# D49 complete current map presentation and assignment location cores.
from .business_gameplay import _map_presentation_db_fields, _map_presentation_arithmetic_fields
def _assignment_location_carry_fields(state: SceneState, frame: FirstDeploymentFrame,
        carry: bool) -> FirstDeploymentFrame:
    status = (frame.status | 1) if carry else (frame.status & 30)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, status=status)
def _assignment_location_store_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(0, 1), 8)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 4)
    frame = _settlement_store_word_fields(state, frame, state.table_at(0xFFFFF35E), 0, low16(frame.target_x))
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(0, 2), 8)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 4)
    frame = _settlement_store_word_fields(state, frame, state.table_at(0xFFFFF360), 0, low16(frame.target_x))
    return _assignment_location_carry_fields(state, frame, False)
def locate_selected_ruler_city_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Selected force's head affiliation, then original descending40 city fallback."""
    frame = _resource_cost_frame(state, frame, 0x309FC)
    frame = first_replace(frame, roster=state.table_at(0xFFFFE640).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF376, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
    frame = _movement_move(state, frame, 'target_x', frame.roster.word(low16(frame.target_x)), 16)
    frame = first_replace(frame, roster=state.table_at(0xFFFFCC00).cursor())
    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(low16(frame.target_x)), 8)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 63, 16)
    frame = _movement_compare(state, frame, low16(frame.target_y), 40, 16)
    if frame.status & 5:
        frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
        frame = first_replace(frame, roster=state.table_at(0xD4AC6).cursor())
        frame = _settlement_store_word_fields(state, frame, state.table_at(0xFFFFF35E), 0, frame.roster.word(low16(frame.target_y), 2))
        frame = _settlement_store_word_fields(state, frame, state.table_at(0xFFFFF360), 0, frame.roster.word(low16(frame.target_y)))
        return _assignment_location_carry_fields(state, frame, False)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF428).cursor())
    frame = _movement_move(state, frame, 'target_x', 39, 16)
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF376, 2), 16)
    while True:
        frame = _movement_compare(state, frame, low8(frame.target_y), frame.roster.byte(low16(frame.target_x)), 8)
        if frame.status & 4:
            frame = first_replace(frame, roster=state.table_at(0xD4ACA).cursor())
            frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
            frame = _settlement_store_word_fields(state, frame, state.table_at(0xFFFFF35E), 0, frame.roster.word(low16(frame.target_x), 2))
            frame = _settlement_store_word_fields(state, frame, state.table_at(0xFFFFF360), 0, frame.roster.word(low16(frame.target_x)))
            return _assignment_location_carry_fields(state, frame, False)
        frame, again = _map_presentation_db_fields(frame, 'target_x')
        if not again:
            return _assignment_location_carry_fields(state, frame, True)
def locate_selected_force_packet_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Head/member packet search and force-header search have distinct live operands."""
    frame = _resource_cost_frame(state, frame, 0x30B8E)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF376, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
    frame = first_replace(frame, roster=state.table_at(0xFFFFE640).cursor())
    frame = _movement_move(state, frame, 'target_x', frame.roster.word(low16(frame.target_x)), 16)
    frame = first_replace(frame, roster=state.table_at(0xFFFFA050).cursor())
    frame = _movement_test(state, frame, frame.roster.byte(low16(frame.target_x)), 8)
    selected_header = not bool(frame.status & 4)
    frame = first_replace(frame, roster=state.table_at(0xFFFF9000).cursor())
    if selected_header:
        frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF376, 2), 16)
        while True:
            frame = _movement_move(state, frame, 'target_y', frame.roster.byte(), 8)
            frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 15, 16)
            if frame.status & 4:
                return _assignment_location_carry_fields(state, frame, True)
            frame = _movement_compare(state, frame, low8(frame.target_x), frame.roster.byte(0, 4), 8)
            if frame.status & 4:
                return _assignment_location_store_fields(state, frame)
            frame = first_replace(frame, roster=frame.roster.advance(13 + s16(low16(frame.target_y))))
    while True:
        frame = _movement_move(state, frame, 'unit', frame.roster.byte(), 8)
        frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 15, 16)
        if frame.status & 4:
            return _assignment_location_carry_fields(state, frame, True)
        frame = _movement_compare(state, frame, low8(frame.target_y), frame.roster.byte(0, 4), 8)
        if frame.status & 4:
            frame = _movement_move(state, frame, 'count', low16(frame.unit), 16)
            frame = _map_presentation_arithmetic_fields(state, frame, 'count', 1, True)
            while True:
                frame = _movement_compare(state, frame, low8(frame.target_x), frame.roster.byte(low16(frame.count), 13), 8)
                if frame.status & 4:
                    return _assignment_location_store_fields(state, frame)
                frame, again = _map_presentation_db_fields(frame, 'count')
                if not again:
                    break
        frame = first_replace(frame, roster=frame.roster.advance(13 + s16(low16(frame.unit))))

# D50 complete setup/controller and city-assignment owners.
from .business_gameplay import (
    _setup_call_fields, _setup_write_fields, _setup_compare_memory_fields,
    _setup_change_word_fields, _setup_asl_word_fields,
    _setup_coordinate_high_byte_fields, _resource_cost_frame,
    _map_presentation_bit_fields, _map_presentation_arithmetic_fields,
    _map_presentation_db_fields,
)
from .business_movement_support import (
    MovementContinuationBoundary, _movement_move, _movement_move_long,
    _movement_test, _movement_test_long, _movement_compare,
    _movement_fixed_shift_word, _movement_binary_flags,
    _movement_save_longs, _movement_restore_longs,
)
def _controller_setup_child_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: Long) -> FirstDeploymentFrame:
    """Closed original setup callees; unknown targets retain the entered slot."""
    children={0x30088:refresh_setup_option_labels_fields,
        0x302AC:render_packed_sprite_position_fields,
        0x302C2:render_selected_setup_options_fields,
        0x30484:render_setup_player_position_fields,
        0x3049C:cycle_second_player_choice_fields,0x3051E:cycle_third_player_choice_fields,
        0x305B0:run_controller_setup_and_configuration_fields,
        0x30696:update_connected_controller_option_fields,
        0x306EE:advance_controller_setup_reveal_fields,
        0x3071A:advance_controller_setup_dismissal_fields,
        0x30742:read_controller_identity_fields,0x3076E:commit_setup_options_fields}
    if target in children:return children[target](state,frame)
    return _city_assignment_child_fields(state,frame,target)
def refresh_setup_option_labels_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x30088)
    frame=_movement_move(state,frame,'target_x',state.read(0x00FF7032,2),16)
    frame=_movement_move(state,frame,'target_y',state.read(0x00FF7026,2),16)
    frame=_movement_compare(state,frame,low16(frame.target_y),low16(frame.target_x),16)
    if frame.status&4:return frame
    frame=first_replace(frame,roster=state.table_at(0x300DE).cursor())
    frame=_setup_asl_word_fields(state,frame,'target_y',2)
    frame=first_replace(frame,roster=state.table_at(frame.roster.long(low16(frame.target_y))).cursor())
    while True:
        frame=_movement_move(state,frame,'target_x',frame.roster.word(),16)
        frame=_movement_compare(state,frame,low16(frame.target_x),65535,16)
        if frame.status&4:break
        frame=_setup_call_fields(state,frame,0x2B446,0x300B4)
        frame=_movement_move_long(state,frame,'target_x',0)
        frame=_movement_move(state,frame,'offset_x',frame.roster.word(),16)
        frame=first_replace(frame,roster=frame.roster.advance(2))
        # The original loads D5 then immediately CLR.Ls it. Preserve both.
        frame=_movement_move_long(state,frame,'offset_x',0)
        while True:
            frame=_movement_move(state,frame,'target_x',frame.roster.word(),16)
            frame=first_replace(frame,roster=frame.roster.advance(2))
            frame=_movement_compare(state,frame,low16(frame.target_x),65535,16)
            if frame.status&4:break
            frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&255,16)
            frame=_movement_move(state,frame,'target_x',low16(frame.target_x)|0x8300,16)
            frame=_setup_write_fields(state,frame,0x00C00000,low16(frame.target_x))
    return _setup_write_fields(state,frame,0x00FF7032,state.read(0x00FF7026,2))
def render_packed_sprite_position_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x302AC)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame=_setup_coordinate_high_byte_fields(state,frame)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&255,16)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_y)&255,16)
    frame=_movement_move_long(state,frame,'unit',0)
    return _setup_call_fields(state,frame,0xAC08,0x302C0)
def _controller_setup_visible_fields(state: SceneState, frame: FirstDeploymentFrame,
        option: int, first: bool=False) -> tuple:
    frame=(_movement_test(state,frame,state.read(0x00FF7022,2),16) if first
        else _setup_compare_memory_fields(state,frame,0x00FF7022,option))
    if not frame.status&4:return frame,True
    frame=_map_presentation_bit_fields(state,frame,state.read(0xFFFFF321,1),8)
    return frame,bool(frame.status&4)
def _controller_setup_option_sprite_fields(state: SceneState, frame: FirstDeploymentFrame,
        option: int, value_address: Long, coordinate_table: Long,
        sprite: Long, continuation: Long) -> FirstDeploymentFrame:
    roles=((0,0x00FF7026,0x30456,0x2B116,0x302F0),
        (1,0x00FF7024,0x3045C,0x2B124,0x30320),
        (2,0x00FF7028,0x30462,0x2B124,0x30350),
        (3,0x00FF702A,0x30466,0x2B124,0x30380))
    if (option,value_address,coordinate_table,sprite,continuation) not in roles:
        raise ValueError('closed setup option sprite roles required')
    frame,visible=_controller_setup_visible_fields(state,frame,option,option==0)
    if not visible:return frame
    frame=_movement_move(state,frame,'target_y',state.read(value_address,2),16)
    frame=_setup_asl_word_fields(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(coordinate_table).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_y)),16)
    frame=first_replace(frame,roster=state.table_at(sprite).cursor())
    return _setup_call_fields(state,frame,0x302AC,continuation)
def render_selected_setup_options_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x302C2)
    for roles in ((0,0x00FF7026,0x30456,0x2B116,0x302F0),
            (1,0x00FF7024,0x3045C,0x2B124,0x30320),
            (2,0x00FF7028,0x30462,0x2B124,0x30350),
            (3,0x00FF702A,0x30466,0x2B124,0x30380)):
        frame=_controller_setup_option_sprite_fields(state,frame,*roles)
    frame,visible=_controller_setup_visible_fields(state,frame,4)
    if visible:
        frame=_setup_compare_memory_fields(state,frame,0x00FF7026,2)
        if frame.status&4:
            frame=_setup_compare_memory_fields(state,frame,0x00FF702C,3)
            if not frame.status&1:
                frame=_setup_write_fields(state,frame,0x00FF702C,0,clear=True)
        frame=_movement_move(state,frame,'target_x',state.read(0x00FF702C,2),16)
        frame=_setup_asl_word_fields(state,frame,'target_x',1)
        frame=first_replace(frame,roster=state.table_at(0x3046C).cursor())
        frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_x)),16)
        frame=_movement_move(state,frame,'target_x',176,16)
        frame=first_replace(frame,roster=state.table_at(0x2B132).cursor())
        frame=_movement_move_long(state,frame,'unit',0)
        frame=_setup_call_fields(state,frame,0xAC08,0x303C4)
    frame=_movement_test(state,frame,state.read(0x00FF7034,2),16)
    if frame.status&4:return frame
    frame=_setup_compare_memory_fields(state,frame,0x00FF7022,5)
    if frame.status&1:return frame
    if frame.status&4:
        frame=_map_presentation_bit_fields(state,frame,state.read(0xFFFFF321,1),8)
        visible=bool(frame.status&4)
    else:visible=True
    if visible:
        frame=first_replace(frame,roster=state.table_at(0x2B13A).cursor())
        frame=_movement_move(state,frame,'target_x',state.read(0x00FF702E,2),16)
        frame=_movement_save_longs(state,frame,('target_x',))
        frame=_setup_call_fields(state,frame,0x30484,0x303FA)
        frame=_movement_restore_longs(state,frame,('target_x',))
    frame=_setup_compare_memory_fields(state,frame,0x00FF7034,2)
    if not frame.status&4:return frame
    frame=_setup_compare_memory_fields(state,frame,0x00FF7022,6)
    if frame.status&1:return frame
    if frame.status&4:
        frame=_map_presentation_bit_fields(state,frame,state.read(0xFFFFF321,1),8)
        visible=bool(frame.status&4)
    else:visible=True
    if not visible:return frame
    frame=first_replace(frame,roster=state.table_at(0x2B142).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0x00FF7030,2),16)
    frame=_movement_save_longs(state,frame,('target_x',))
    frame=_setup_call_fields(state,frame,0x30484,0x30438)
    return _movement_restore_longs(state,frame,('target_x',))
def render_setup_player_position_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x30484)
    frame=_setup_asl_word_fields(state,frame,'target_x',1)
    frame=first_replace(frame,scan=state.table_at(0x3046C).cursor())
    frame=_movement_move(state,frame,'target_y',frame.scan.word(low16(frame.target_x)),16)
    frame=_movement_move(state,frame,'target_x',176,16)
    frame=_movement_move_long(state,frame,'unit',0)
    return _setup_call_fields(state,frame,0xAC08,0x3049A)
def _controller_setup_cycle_player_fields(state: SceneState,frame: FirstDeploymentFrame,
        third: bool)->FirstDeploymentFrame:
    if type(third) is not bool:
        raise ValueError('actual second/third player role required')
    for address in (0x00FF7038,0x00FF703A):
        frame=_setup_compare_memory_fields(state,frame,address,16)
        if frame.status&1:
            return frame
    frame=_map_presentation_bit_fields(state,frame,state.read(0xFFFFF605,1),4)
    decrease=not bool(frame.status&4)
    # No direction input still reaches the original player-uniqueness checks.
    adjust=decrease
    if not decrease:
        frame=_map_presentation_bit_fields(state,frame,state.read(0xFFFFF605,1),8)
        adjust=not bool(frame.status&4)
    while True:
        if adjust:
            if decrease:
                frame=_movement_test(state,frame,low16(frame.offset_x),16)
                if frame.status&4:
                    frame=_movement_move_long(state,frame,'offset_x',2)
                    frame=_setup_compare_memory_fields(state,frame,0x00FF7026,2)
                    if not frame.status&4:
                        frame=_movement_move_long(state,frame,'offset_x',6)
                else:
                    frame=_map_presentation_arithmetic_fields(state,frame,'offset_x',1,True)
            else:
                frame=_setup_compare_memory_fields(state,frame,0x00FF7026,2)
                limit=6 if frame.status&1 else 2
                frame=_movement_compare(state,frame,low16(frame.offset_x),limit,16)
                frame=_movement_move(state,frame,'offset_x',0,16) if frame.status&4 else _map_presentation_arithmetic_fields(state,frame,'offset_x',1)
        frame=_movement_compare(state,frame,low16(frame.offset_x),state.read(0x00FF702C,2),16)
        if frame.status&4:
            # An existing collision enables the same original adjustment loop.
            adjust=True
            continue
        if third:
            frame=_movement_compare(state,frame,low16(frame.offset_x),state.read(0x00FF702E,2),16)
            if frame.status&4:
                adjust=True
                continue
        return frame
def cycle_second_player_choice_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x3049C)
    return _controller_setup_cycle_player_fields(state,frame,False)
def cycle_third_player_choice_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x3051E)
    return _controller_setup_cycle_player_fields(state,frame,True)
def _controller_setup_palette_fields(state: SceneState, frame: FirstDeploymentFrame,
        counter: Long, continuation: Long, dismiss: bool) -> FirstDeploymentFrame:
    if (counter,continuation,dismiss) not in ((0x00FF7038,0x30712,False),(0x00FF703A,0x3073A,True)):
        raise ValueError('closed controller palette roles required')
    frame=_setup_compare_memory_fields(state,frame,counter,16)
    if not frame.status&1:return frame
    if dismiss:frame=_movement_move(state,frame,'target_x',state.read(counter,2),16)
    else:
        frame=_movement_move(state,frame,'target_x',15,16)
        frame=_map_presentation_arithmetic_fields(state,frame,'target_x',state.read(counter,2),True)
    frame=_movement_move(state,frame,'target_y',64,16)
    frame=first_replace(frame,roster=state.table_at(0x2B46E).cursor())
    frame=_setup_call_fields(state,frame,0xDEA6,continuation)
    return _setup_change_word_fields(state,frame,counter,1)
def advance_controller_setup_reveal_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x306EE)
    return _controller_setup_palette_fields(state,frame,0x00FF7038,0x30712,False)
def advance_controller_setup_dismissal_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x3071A)
    return _controller_setup_palette_fields(state,frame,0x00FF703A,0x3073A,True)
def _controller_setup_byte_shift_fields(state: SceneState, frame: FirstDeploymentFrame,
        carrier: str, right: bool) -> FirstDeploymentFrame:
    """Use existing arithmetic/shift authorities, retaining the exact BYTE width."""
    if (carrier,right) not in (('target_y',False),('unit',True)):
        raise ValueError('actual controller BYTE shift role required')
    original=frame.carrier(carrier);value=low8(original)
    if right:
        frame=first_replace(frame,**{carrier:value})
        frame=_movement_fixed_shift_word(state,frame,carrier,1,True)
        status=(frame.status&17)|(8 if value>>1&128 else 0)|(4 if value>>1==0 else 0)
        state.sr=(state.sr&65504)|status
        return first_replace(frame,status=status,**{carrier:replace_byte(original,value>>1)})
    frame,value=_movement_binary_flags(state,frame,value,value,8)
    return first_replace(frame,**{carrier:replace_byte(original,value)})
def read_controller_identity_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x30742)
    frame=_setup_write_fields(state,frame,frame.roster.base,64,1)
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(),8)
    frame=_movement_move(state,frame,'target_y',low8(frame.target_x),8)
    frame=_controller_setup_byte_shift_fields(state,frame,'target_y',False)
    frame=_movement_move(state,frame,'target_x',low8(frame.target_x)|low8(frame.target_y),8)
    frame=_movement_move(state,frame,'target_x',low8(frame.target_x)&10,8)
    frame=_setup_write_fields(state,frame,frame.roster.base,0,1)
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(),8)
    frame=_movement_move(state,frame,'unit',low8(frame.target_y),8)
    frame=_controller_setup_byte_shift_fields(state,frame,'unit',True)
    frame=_movement_move(state,frame,'target_y',low8(frame.target_y)|low8(frame.unit),8)
    frame=_movement_move(state,frame,'target_y',low8(frame.target_y)&5,8)
    return _movement_move(state,frame,'target_x',low8(frame.target_x)|low8(frame.target_y),8)
def update_connected_controller_option_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x30696)
    frame=_movement_test(state,frame,state.read(0x00FF703E,2),16)
    # BNE3069C skips identity detection; the306CC display tail always runs.
    if frame.status&4:
        frame=first_replace(frame,roster=state.table_at(0x00A10005).cursor())
        frame=_setup_call_fields(state,frame,0x30742,0x306AA)
        frame=_movement_compare(state,frame,low8(frame.target_x),11,8)
        if frame.status&4:
            frame=_movement_move(state,frame,'offset_x',state.read(0x00FF7034,2),16)
            frame=_movement_move(state,frame,'offset_y',2,16)
            frame=_setup_call_fields(state,frame,0x2B01A,0x306C6)
            frame=_setup_write_fields(state,frame,0x00FF7034,low16(frame.offset_x))
        else:frame=_setup_write_fields(state,frame,0x00FF7034,0,clear=True)
    frame=_movement_move(state,frame,'target_y',state.read(0x00FF7034,2),16)
    frame=_setup_asl_word_fields(state,frame,'target_y',1)
    frame=first_replace(frame,scan=state.table_at(0x3047C).cursor())
    frame=_movement_move(state,frame,'target_x',frame.scan.word(low16(frame.target_y)),16)
    frame=first_replace(frame,roster=state.table_at(0x2B14A).cursor())
    frame=_movement_move(state,frame,'target_y',112,16)
    frame=_movement_move_long(state,frame,'unit',0)
    return _setup_call_fields(state,frame,0xAC08,0x306EC)
def commit_setup_options_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x3076E)
    frame=_setup_write_fields(state,frame,0xFFFFEFD2,state.read(0x00FF7024,2))
    frame=_movement_move(state,frame,'target_x',state.read(0x00FF7026,2),16)
    frame=_setup_write_fields(state,frame,0xFFFFEFD4,low16(frame.target_x))
    frame=_setup_write_fields(state,frame,0xFFFFEFE4,low16(frame.target_x))
    frame=_setup_write_fields(state,frame,0xFFFFF374,state.table_at(0x307E0).byte(low16(frame.target_x)),1)
    frame=_setup_write_fields(state,frame,0xFFFFF375,0,1,True)
    for source,destination in ((0x00FF7028,0xFFFFEFD6),(0x00FF702A,0xFFFFEFD8)):
        frame=_setup_write_fields(state,frame,destination,state.read(source,2))
    frame=_setup_write_fields(state,frame,0xFFFFF67C,128)
    frame=_setup_write_fields(state,frame,0xFFFFF67E,128)
    frame=_movement_move(state,frame,'target_x',state.read(0x00FF7034,2),16)
    frame=first_replace(frame,roster=state.table_at(0x00FF702C).cursor(),
        candidates=state.table_at(0x307E4).cursor())
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFEFD4,2),16)
    for step in range(2):
        frame=_movement_fixed_shift_word(state,frame,'target_y',1,False)
        frame=_map_presentation_arithmetic_fields(state,frame,'target_y',state.read(0xFFFFEFD4,2))
    frame=_movement_fixed_shift_word(state,frame,'target_y',1,False)
    frame=first_replace(frame,candidates=frame.candidates.advance(s16(low16(frame.target_y))),
        controller=state.table_at(0xFFFFF67A))
    while True:
        frame=_movement_move(state,frame,'target_y',frame.roster.word(),16)
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_movement_fixed_shift_word(state,frame,'target_y',1,False)
        frame=_setup_write_fields(state,frame,frame.controller.base,
            frame.candidates.word(low16(frame.target_y)))
        frame=first_replace(frame,controller=frame.controller.advance(2))
        frame,again=_map_presentation_db_fields(frame,'target_x')
        if not again:return frame
def _controller_setup_interrupt_status_fields(state: SceneState,
        frame: FirstDeploymentFrame, sr: Word) -> FirstDeploymentFrame:
    if sr not in (0x2700,0x2500):raise ValueError('original setup full SR required')
    state.sr=sr
    return first_replace(frame,status=sr&31)
def _controller_setup_fill_descriptor_fields(state: SceneState, frame: FirstDeploymentFrame,
        descriptor: Word, handler: Long) -> FirstDeploymentFrame:
    if (descriptor,handler) not in ((0xA0C0,0x2AA90),(0xA200,0x2AAA6),(0xA1C0,0x2AABE)):
        raise ValueError('actual controller/setup IRQ descriptor required')
    frame=_setup_write_fields(state,frame,0x00C00004,0x8F02)
    frame=_setup_write_fields(state,frame,0x00C00004,0x60000002,4)
    frame=first_replace(frame,scratch=state.table_at(0x00C00000))
    frame=_movement_move(state,frame,'offset_y',0x3333,16)
    frame=_movement_move(state,frame,'choice',0xD7F,16)
    while True:
        frame=_setup_write_fields(state,frame,frame.scratch.base,low16(frame.offset_y))
        frame,again=_map_presentation_db_fields(frame,'choice')
        if not again:break
    for address,value,width in ((0x00FF700C,descriptor,2),(0x00FF700E,handler,4),
            (0x00FF7014,3,2),(0x00FF7016,1,2)):
        frame=_setup_write_fields(state,frame,address,value,width)
    return frame
def _controller_setup_wait_irq_fields(state: SceneState, frame: FirstDeploymentFrame,
        poll: Long) -> FirstDeploymentFrame:
    if poll not in (0x30648,0x2AB6C):raise ValueError('actual setup IRQ poll required')
    frame=_setup_write_fields(state,frame,0xFFFFF612,0x800)
    frame=_movement_test(state,frame,state.read(0xFFFFF612,1),8)
    if not frame.status&4:
        raise MovementContinuationBoundary(poll,frame,'original setup poll requires real asynchronous IRQ RAM progress')
    return frame
def _controller_setup_begin_fields(state: SceneState, frame: FirstDeploymentFrame,
        main_menu: bool) -> FirstDeploymentFrame:
    if type(main_menu) is not bool:raise ValueError('actual setup phase selector required')
    frame=_controller_setup_interrupt_status_fields(state,frame,0x2700)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF606,2),16)
    frame=_movement_move(state,frame,'target_x',low8(frame.target_x)&0xBF,8)
    frame=_setup_write_fields(state,frame,0x00C00004,low16(frame.target_x))
    frame=_setup_write_fields(state,frame,0xFFFFF612,0,clear=True)
    for target,token in ((0x68CE,0x2AAEA if main_menu else 0x305CC),
            (0x6826,0x2AAF0 if main_menu else 0x305D2)):
        frame=_setup_call_fields(state,frame,target,token)
    frame=_setup_write_fields(state,frame,0x00FF7036,0 if main_menu else 1,clear=main_menu)
    frame=_setup_call_fields(state,frame,0x2B15E,0x2AAFA if main_menu else 0x305DE)
    counters=(0x00FF7022,0x00FF7040,0x00FF7042,0x00FF703E) if main_menu else (0x00FF7038,0x00FF703A,0x00FF703E)
    for address in counters:frame=_setup_write_fields(state,frame,address,0,clear=True)
    frame=_setup_call_fields(state,frame,0x2AFB8 if main_menu else 0x306EE,
        0x2AB18 if main_menu else 0x305F4)
    frame=_controller_setup_fill_descriptor_fields(state,frame,0xA200 if main_menu else 0xA0C0,
        0x2AAA6 if main_menu else 0x2AA90)
    return _controller_setup_interrupt_status_fields(state,frame,0x2500)
def _controller_setup_last_button_fields(state: SceneState, frame: FirstDeploymentFrame,
        previous: bool=False) -> FirstDeploymentFrame:
    """Original MOVEQs are distinct: forward keeps both D0/D1; back only D0."""
    if type(previous) is not bool:raise ValueError('actual setup navigation role required')
    frame=_movement_move_long(state,frame,'target_x',5)
    if not previous:frame=_movement_move_long(state,frame,'target_y',4)
    frame=_movement_test(state,frame,state.read(0x00FF7034,2),16)
    if frame.status&4:return frame
    frame=_movement_move_long(state,frame,'target_x',6)
    if not previous:frame=_movement_move_long(state,frame,'target_y',5)
    frame=_setup_compare_memory_fields(state,frame,0x00FF7034,1)
    if frame.status&4:return frame
    frame=_movement_move_long(state,frame,'target_x',7)
    return frame if previous else _movement_move_long(state,frame,'target_y',6)
def _controller_setup_main_iteration_fields(state: SceneState, frame: FirstDeploymentFrame) -> tuple:
    frame=_setup_call_fields(state,frame,0x2AFB8,0x2AB76)
    frame=_setup_call_fields(state,frame,0x2AFE6,0x2AB7C)
    frame=_movement_test(state,frame,state.read(0x00FF703E,2),16)
    if not frame.status&4:
        frame=_setup_compare_memory_fields(state,frame,0x00FF7042,16)
        return frame,not bool(frame.status&1)
    # Keep the original302C2 display-before30088-update CALL order and return slots.
    for target,token in ((0x302C2,0x2AB8C),(0x2AD5A,0x2AB92),(0x2AD88,0x2AB98),
            (0x2ADB8,0x2AB9E),(0x2ADE8,0x2ABA4),(0x2AE18,0x2ABAA),(0x30088,0x2ABB0)):
        frame=_setup_call_fields(state,frame,target,token)
    frame=_movement_test(state,frame,state.read(0x00FF7034,2),16)
    copy_player=False
    if not frame.status&4:
        frame=_setup_compare_memory_fields(state,frame,0x00FF7034,1)
        if frame.status&4:
            frame=_setup_compare_memory_fields(state,frame,0x00FF7022,5)
            copy_player=bool(frame.status&4)
        else:
            frame=_setup_compare_memory_fields(state,frame,0x00FF7022,6)
            copy_player=bool(frame.status&4)
            if not copy_player:
                frame=_setup_compare_memory_fields(state,frame,0x00FF7022,5)
                copy_player=bool(frame.status&4)
    if copy_player:
        frame=_setup_write_fields(state,frame,0xFFFFF603,state.read(0xFFFFF605,1),1)
    frame=_map_presentation_bit_fields(state,frame,state.read(0xFFFFF603,1),32)
    check_exit=False
    if not frame.status&4:
        frame=_movement_move(state,frame,'target_x',0xAC,8)
        frame=_setup_call_fields(state,frame,0x808A,0x2AC08)
        frame=_controller_setup_last_button_fields(state,frame)
        frame=_movement_compare(state,frame,frame.target_x&65535,state.read(0x00FF7022,2),16)
        if frame.status&4:
            # Original BEQ2AC30 reaches the F703E store at2AD42.
            frame=_setup_write_fields(state,frame,0x00FF703E,1)
            check_exit=True
        else:
            frame=_movement_compare(state,frame,frame.target_y&65535,state.read(0x00FF7022,2),16)
            if frame.status&4:
                frame=_controller_setup_interrupt_status_fields(state,frame,0x2700)
                frame=_controller_setup_fill_descriptor_fields(state,frame,0xA1C0,0x2AABE)
                frame=_controller_setup_interrupt_status_fields(state,frame,0x2500)
            frame=_setup_change_word_fields(state,frame,0x00FF7022,1)
    else:
        frame=_map_presentation_bit_fields(state,frame,state.read(0xFFFFF603,1),16)
        if not frame.status&4:
            frame=_controller_setup_last_button_fields(state,frame,True)
            frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0x00FF7022,2),16)
            if frame.status&4:
                frame=_setup_write_fields(state,frame,0x00FF7022,0,clear=True)
                frame=_controller_setup_interrupt_status_fields(state,frame,0x2700)
                frame=_controller_setup_fill_descriptor_fields(state,frame,0xA200,0x2AAA6)
                frame=_controller_setup_interrupt_status_fields(state,frame,0x2500)
            else:
                frame=_movement_test(state,frame,state.read(0x00FF7022,2),16)
                if not frame.status&4:frame=_setup_change_word_fields(state,frame,0x00FF7022,1,True)
    if not check_exit:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF603,1),8)
        frame=_movement_move(state,frame,'target_x',low8(frame.target_x)&128,8)
        if not frame.status&4:frame=_setup_write_fields(state,frame,0x00FF703E,1)
    frame=_setup_compare_memory_fields(state,frame,0x00FF7042,16)
    return frame,not bool(frame.status&1)
def run_controller_setup_and_configuration_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """305B0/2AACE sole cooperative owner; real waits retain a resumable session."""
    from .controller_setup_steps import run_controller_setup_blocking_fields
    return run_controller_setup_blocking_fields(state, frame)

from .business_gameplay import (
    _setup_call_fields, _setup_write_fields, _setup_compare_memory_fields,
    _setup_change_word_fields, _resource_cost_frame,
    _map_presentation_bit_fields, _map_presentation_arithmetic_fields,
    _map_presentation_db_fields,
)
from .business_movement_support import _movement_move, _movement_move_long, _movement_test, _movement_compare, _movement_fixed_shift_word, MovementContinuationBoundary
from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
from ..high_level_scene_flows.business_scene import _glyph_shift_long_fields
from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
from ..high_level_battle_ai.business_formation import first_deployment_random_fields
from .business_highbank import advance_officer_growth_levels_fields
def _city_assignment_child_fields(state: SceneState, frame: FirstDeploymentFrame, target: Long) -> FirstDeploymentFrame:
    if target == 200716:
        from ..high_level_remaining_flows.business_highbank import open_command_phase_dispatch_fields
        return open_command_phase_dispatch_fields(state, frame)
    if target == 200724:
        from ..high_level_remaining_flows.business_highbank import open_assignment_menu_dispatch_fields
        return open_assignment_menu_dispatch_fields(state, frame)
    if target == 200732:
        from ..high_level_remaining_flows.business_highbank import open_city_action_menu_dispatch_fields
        return open_city_action_menu_dispatch_fields(state, frame)
    if target == 201464:
        from ..high_level_remaining_flows.business_highbank import advance_command_notice_phase_fields
        return advance_command_notice_phase_fields(state, frame)
    if target == 201512:
        from ..high_level_remaining_flows.business_highbank import show_command_intro_fields
        return show_command_intro_fields(state, frame)
    if target == 201528:
        from ..high_level_remaining_flows.business_highbank import reset_command_intro_fields
        return reset_command_intro_fields(state, frame)
    if target == 201536:
        from ..high_level_remaining_flows.business_highbank import confirm_command_map_origin_fields
        return confirm_command_map_origin_fields(state, frame)
    if target == 201596:
        from ..high_level_remaining_flows.business_highbank import open_command_selection_fields
        return open_command_selection_fields(state, frame)
    if target == 201638:
        from ..high_level_remaining_flows.business_highbank import show_command_selected_member_fields
        return show_command_selected_member_fields(state, frame)
    if target == 201660:
        from ..high_level_remaining_flows.business_highbank import initialize_command_choice_menu_fields
        return initialize_command_choice_menu_fields(state, frame)
    if target == 201776:
        from ..high_level_remaining_flows.business_highbank import process_command_choice_menu_fields
        return process_command_choice_menu_fields(state, frame)
    if target == 202466:
        from ..high_level_remaining_flows.business_highbank import show_command_policy_notice_fields
        return show_command_policy_notice_fields(state, frame)
    if target == 202482:
        from ..high_level_remaining_flows.business_highbank import initialize_command_policy_menu_fields
        return initialize_command_policy_menu_fields(state, frame)
    if target == 202602:
        from ..high_level_remaining_flows.business_highbank import process_command_policy_menu_fields
        return process_command_policy_menu_fields(state, frame)
    if target == 203092:
        from ..high_level_remaining_flows.business_highbank import show_command_completion_fields
        return show_command_completion_fields(state, frame)
    if target == 203108:
        from ..high_level_remaining_flows.business_highbank import initialize_command_exit_menu_fields
        return initialize_command_exit_menu_fields(state, frame)
    if target == 203148:
        from ..high_level_remaining_flows.business_highbank import process_command_exit_menu_fields
        return process_command_exit_menu_fields(state, frame)
    if target == 203220:
        from ..high_level_remaining_flows.business_highbank import refresh_command_map_on_input_fields
        return refresh_command_map_on_input_fields(state, frame)
    if target == 0x338C2:
        return dispatch_city_command_stage_fields(state, frame)
    if target == 0x340F8:
        return dispatch_map_packet_command_stage_fields(state, frame)
    children = {200618: run_city_command_assignment_fields, 200682: clear_unassigned_officer_commands_fields, 200740: run_city_command_states_fields, 200772: run_map_packet_command_states_fields, 200820: select_next_force_city_fields, 200878: select_next_force_map_packet_fields, 200976: sample_city_command_policy_fields, 201084: clear_current_city_project_orders_fields, 201126: build_current_city_officer_roster_fields, 201190: finish_city_command_assignment_fields, 201210: retain_city_command_stage_fields, 201416: dispatch_city_assignment_state_fields, 59438: recover_unacted_officer_b200_fields, 59552: clear_unowned_debt_records_fields}
    if target == 201486:
        from ..high_level_remaining_flows.business_highbank import wait_command_intro_fields
        return wait_command_intro_fields(state, frame)
    if target in children:
        return children[target](state, frame)
    if target == 33748:
        return first_deployment_random_fields(BattlePolicyMemory(state), frame)
    if target == 418532:
        return advance_officer_growth_levels_fields(state, frame)
    if target == 71950:
        from .business_gameplay import settle_city_projects_and_refresh_map_fields
        return settle_city_projects_and_refresh_map_fields(state, frame)
    raise MovementContinuationBoundary(target, frame, 'original assignment child has no complete current field interface')
def clear_unassigned_officer_commands_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x30FEA)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCD00).cursor())
    frame=_movement_move(state,frame,'target_x',255,16)
    while True:
        frame=_movement_move(state,frame,'target_y',frame.roster.byte(),8)
        frame=first_replace(frame,roster=frame.roster.advance(1))
        frame=_movement_compare(state,frame,low8(frame.target_y),2,8)
        if frame.status&1:
            frame=_setup_write_fields(state,frame,u32(frame.roster.base-1),0,1,True)
        frame,again=_map_presentation_db_fields(frame,'target_x')
        if not again:return frame
def select_next_force_city_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x31074)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF427).cursor(),
        candidates=state.table_at(0xFFFFEA37).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_map_presentation_arithmetic_fields(state,frame,'target_x',1)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF376,2),16)
    while True:
        frame=_movement_compare(state,frame,low16(frame.target_x),40,16)
        if not frame.status&5:
            frame=_movement_move(state,frame,'target_x',65535,16)
            break
        frame=_movement_test(state,frame,frame.candidates.byte(low16(frame.target_x)),8)
        if frame.status&4:
            frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
            frame=_movement_compare(state,frame,low8(frame.target_y),low8(frame.unit),8)
            if frame.status&4:break
        frame=_map_presentation_arithmetic_fields(state,frame,'target_x',1)
    return _setup_write_fields(state,frame,0xFFFFF364,low16(frame.target_x))
def select_next_force_map_packet_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x310AE)
    frame=first_replace(frame,roster=state.table_at(0xFFFF9000).cursor())
    frame=first_replace(frame,roster=frame.roster.advance(s16(state.read(0xFFFFF75A,2))))
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
    while True:
        frame=_movement_move(state,frame,'target_y',frame.roster.byte(),8)
        frame=_map_presentation_bit_fields(state,frame,frame.target_y,32)
        if frame.status&4:
            frame=_movement_move(state,frame,'target_y',low16(frame.target_y)&15,16)
            if frame.status&4:return _setup_write_fields(state,frame,0xFFFFF75A,65535)
            frame=_movement_compare(state,frame,low8(frame.target_x),frame.roster.byte(4),8)
            if frame.status&4:break
        frame=_movement_move(state,frame,'target_y',low16(frame.target_y)&15,16)
        if frame.status&4:return _setup_write_fields(state,frame,0xFFFFF75A,65535)
        frame=first_replace(frame,roster=frame.roster.advance(13+s16(low16(frame.target_y))))
        frame=_map_presentation_arithmetic_fields(state,frame,'target_y',13)
        frame=_setup_change_word_fields(state,frame,0xFFFFF75A,low16(frame.target_y))
    frame=_movement_move(state,frame,'target_x',0,16)
    for offset,destination in ((1,0xFFFFF75C),(2,0xFFFFF75E),(3,0xFFFFF760)):
        frame=_movement_move(state,frame,'target_x',frame.roster.byte(offset),8)
        frame=_setup_write_fields(state,frame,destination,low16(frame.target_x))
    return frame
def sample_city_command_policy_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x31110)
    frame=_setup_call_fields(state,frame,0x83D4,0x31116)
    frame=first_replace(frame,roster=state.table_at(0x311FC).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFEFD2,2),16)
    # Closed existing generic WORD shifter, not a second policy/RNG algorithm.
    from ..high_level_remaining_flows.business_highbank import _position_order_shift
    frame=_position_order_shift(frame,'target_x',6,False)
    state.sr=(state.sr&65504)|frame.status
    frame=first_replace(frame,roster=frame.roster.advance(s16(low16(frame.target_x))))
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',2,False)
    frame=_movement_move_long(state,frame,'target_y',0)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF61C,2),16)
    frame=_glyph_shift_long_fields(SceneRefreshMemory(state),frame,'target_y',4)
    from ..high_level_remaining_flows.business_city import _special_action_swap
    frame=_special_action_swap(state,frame,'target_y')
    frame=_movement_move(state,frame,'unit',0,16)
    frame=_movement_compare(state,frame,low16(frame.target_y),frame.roster.word(low16(frame.target_x)),16)
    if not frame.status&1:
        frame=_map_presentation_arithmetic_fields(state,frame,'unit',4)
        frame=_movement_compare(state,frame,low16(frame.target_y),frame.roster.word(low16(frame.target_x),2),16)
        if not frame.status&1:frame=_map_presentation_arithmetic_fields(state,frame,'unit',4)
    frame=_setup_call_fields(state,frame,0x83D4,0x31150)
    frame=first_replace(frame,controller=state.table_at(0x312BC))
    frame=_movement_move_long(state,frame,'target_x',frame.target_x&65535)
    frame=_glyph_shift_long_fields(SceneRefreshMemory(state),frame,'target_x',3)
    frame=_special_action_swap(state,frame,'target_x')
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_compare(state,frame,low16(frame.target_x),frame.controller.word(low16(frame.unit)),16)
    if not frame.status&1:
        frame=_map_presentation_arithmetic_fields(state,frame,'target_y',1)
        frame=_movement_compare(state,frame,low16(frame.target_x),frame.controller.word(low16(frame.unit),2),16)
        if not frame.status&1:frame=_map_presentation_arithmetic_fields(state,frame,'target_y',1)
    return _setup_write_fields(state,frame,0xFFFFF726,low16(frame.target_y))
def clear_current_city_project_orders_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x3117C)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE80C).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1,False)
    frame=_map_presentation_arithmetic_fields(state,frame,'target_x',state.read(0xFFFFF364,2))
    frame=_movement_fixed_shift_word(state,frame,'target_x',2,False)
    for offset in (0,4,8):
        frame=_setup_write_fields(state,frame,frame.roster.address(low16(frame.target_x),offset),0xFFFFFFFF,4)
    return frame
def build_current_city_officer_roster_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x311A6)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF72A).cursor(),
        candidates=state.table_at(0xFFFFCC00).cursor(),controller=state.table_at(0xFFFFCD00))
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_movement_move(state,frame,'distance',0,16)
    frame=_movement_move(state,frame,'target_y',255,16)
    while True:
        frame=_movement_move(state,frame,'unit',frame.candidates.byte(low16(frame.target_y)),8)
        frame=_movement_compare(state,frame,low16(frame.unit),low16(frame.target_x),16)
        if frame.status&4:
            frame=_movement_move(state,frame,'count',low16(frame.target_y),16)
            frame=_movement_test(state,frame,frame.controller.byte(low16(frame.count)),8)
            if not frame.status&4:
                frame=_map_presentation_bit_fields(state,frame,frame.count,16384)
                frame=first_replace(frame,count=frame.count|16384)
            frame=_setup_write_fields(state,frame,frame.roster.base,low16(frame.count))
            frame=first_replace(frame,roster=frame.roster.advance(2))
            frame=_map_presentation_arithmetic_fields(state,frame,'distance',1)
        frame,again=_map_presentation_db_fields(frame,'target_y')
        if not again:break
    frame=_setup_write_fields(state,frame,frame.roster.base,65535)
    return _setup_write_fields(state,frame,0xFFFFF762,low16(frame.distance))
def run_city_command_states_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x31024)
    while True:
        frame=_setup_call_fields(state,frame,0x31074,0x31028)
        frame=_movement_test(state,frame,state.read(0xFFFFF364,2),16)
        if frame.status&8:return frame
        frame=_setup_call_fields(state,frame,0x311A6,0x31034)
        frame=_setup_write_fields(state,frame,0xFFFFF728,1)
        frame=_setup_call_fields(state,frame,0x338C2,0x31040)
def run_map_packet_command_states_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x31044)
    while True:
        frame=_setup_call_fields(state,frame,0x310AE,0x31048)
        frame=_movement_test(state,frame,state.read(0xFFFFF75A,2),16)
        if frame.status&8:return frame
        frame=_setup_write_fields(state,frame,0xFFFFF728,1)
        frame=_setup_call_fields(state,frame,0x340F8,0x3105C)
        frame=first_replace(frame,roster=state.table_at(0xFFFF9000).cursor())
        frame=first_replace(frame,roster=frame.roster.advance(s16(state.read(0xFFFFF75A,2))))
        frame=_movement_move(state,frame,'target_x',0,16)
        frame=_movement_move(state,frame,'target_x',frame.roster.byte(),8)
        frame=_map_presentation_arithmetic_fields(state,frame,'target_x',13)
        frame=_setup_change_word_fields(state,frame,0xFFFFF75A,low16(frame.target_x))
def _city_assignment_vector_fields(state: SceneState, frame: FirstDeploymentFrame,
        base: Long, table: Long, continuation: Long) -> FirstDeploymentFrame:
    if (base,table,continuation) not in ((0x3100C,0x31006,0x30FD6),(0x312F8,0x312D8,0x312D6)):
        raise ValueError('actual assignment dynamic table role required')
    frame=_movement_move(state,frame,'target_x',state.table_at(table).word(low16(frame.target_x)),16)
    return _setup_call_fields(state,frame,u32(base+s16(low16(frame.target_x))),continuation)
def run_city_command_assignment_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x30FAA)
    frame=_setup_call_fields(state,frame,0x31110,0x30FAE)
    while True:
        frame=_setup_call_fields(state,frame,0x31074,0x30FB2)
        frame=_movement_test(state,frame,state.read(0xFFFFF364,2),16)
        if frame.status&8:break
        frame=_setup_call_fields(state,frame,0x3117C,0x30FBE)
        frame=_setup_call_fields(state,frame,0x311A6,0x30FC2)
        frame=_setup_write_fields(state,frame,0xFFFFF728,1)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF726,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_x',1,False)
        frame=_city_assignment_vector_fields(state,frame,0x3100C,0x31006,0x30FD6)
    frame=_setup_call_fields(state,frame,0xE82E,0x30FDE)
    frame=_setup_call_fields(state,frame,0x30FEA,0x30FE2)
    return _setup_call_fields(state,frame,0x662E4,0x30FE8)
def finish_city_command_assignment_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x311E6)
    frame=_setup_call_fields(state,frame,0xE8A0,0x311EC)
    frame=_setup_call_fields(state,frame,0x1190E,0x311F2)
    return _setup_write_fields(state,frame,0xFFFFF36C,1)
def retain_city_command_stage_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _resource_cost_frame(state,frame,0x311FA)
def dispatch_city_assignment_state_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x312C8)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF362,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1,False)
    return _city_assignment_vector_fields(state,frame,0x312F8,0x312D8,0x312D6)

from .business_gameplay import _setup_legacy_entry_fields, _setup_legacy_result_fields

# D51 complete gameplay text/direction and auxiliary object presentation.
from .business_gameplay import (_resource_cost_frame, _setup_write_fields,
    _map_presentation_db_fields, _map_presentation_arithmetic_fields, _setup_asl_word_fields)
from ..high_level_scene_flows.business_scene import (_glyph_shift_long_fields,
    write_vdp_swapped_byte_rle_stream_fields, read_vdp_plane_rle_rows_fields,
    copy_scene_palette_variant_fields, snapshot_and_clear_scene_palette_fields)
from ..high_level_remaining_flows.business_highbank import _position_order_shift
from .business_movement_support import _movement_arithmetic_long
def _aux_text_shift_word_fields(state: SceneState, frame: FirstDeploymentFrame,
        carrier: str, amount: int) -> FirstDeploymentFrame:
    """Named projection to the existing complete WORD logical shift authority."""
    frame=_position_order_shift(frame,carrier,amount,False)
    state.sr=(state.sr&65504)|frame.status
    return frame
def _aux_text_call_fields(state: SceneState, frame: FirstDeploymentFrame, target: Long, continuation: Long) -> FirstDeploymentFrame:
    frame = _resource_cost_frame(state, frame, target)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    children = {216932: dispatch_auxiliary_command_stage_fields, 218130: expand_glyph_tile_sequence_fields, 218232: calculate_glyph_row_layout_fields, 218256: select_glyph_bitmap_fields, 218290: expand_monochrome_glyph_byte_fields, 218314: upload_expanded_glyph_rows_fields, 218692: draw_auxiliary_text_panel_border_fields, 218778: draw_auxiliary_text_panel_rows_fields, 218866: upload_auxiliary_text_panel_glyphs_fields, 218944: draw_auxiliary_text_panel_markers_fields, 240310: decode_unmasked_literal_plane_fields, 240322: decode_high_plane_rows_fields, 243604: dispatch_repeating_scene_presentation_fields, 252652: initialize_object_scene_video_fields, 216886: load_active_packet_roster_fields}
    if target in children:
        result = children[target](state, entered)
    elif target == 240334:
        result = read_vdp_plane_rle_rows_fields(SceneRefreshMemory(state), entered)
    elif target == 240466:
        result = write_vdp_swapped_byte_rle_stream_fields(SceneRefreshMemory(state), entered)
    elif target == 240532:
        result = copy_scene_palette_variant_fields(SceneRefreshMemory(state), entered)
    elif target == 240266:
        result = snapshot_and_clear_scene_palette_fields(SceneRefreshMemory(state), entered)
    elif target == 26830:
        from ..high_level_gameplay_flow.business_services import clear_video_sprite_plane_fields
        result = clear_video_sprite_plane_fields(SceneRefreshMemory(state), entered)
    elif target == 32906:
        from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields
        result = enqueue_sound_command_fields(SceneRefreshMemory(state), entered)
    elif target == 418260:
        from ..high_level_dynamic_flows.business_actions import upload_portrait_tiles_frame_fields
        result = upload_portrait_tiles_frame_fields(state, entered)
    elif target == 33736:
        from ..high_level_gameplay_flow.business_services import wait_for_scene_sound_byte_fields
        result = wait_for_scene_sound_byte_fields(SceneRefreshMemory(state), entered)
    elif target == 242312:
        from ..high_level_scene_flows.business_objects import append_scene_center_marker_fields
        result = append_scene_center_marker_fields(SceneRefreshMemory(state), entered)
    elif target == 239992:
        from ..high_level_scene_flows.business_scene import advance_scene_palette_fade_fields
        result = advance_scene_palette_fade_fields(SceneRefreshMemory(state), entered)
    elif target == 242236:
        from ..high_level_scene_flows.business_scene import finish_actor_sprite_chains_fields
        result = finish_actor_sprite_chains_fields(SceneRefreshMemory(state), entered)
    elif target in (211180, 211262, 211336, 211404, 211444, 211472, 211640, 212394, 213232) and continuation == 211158:
        from ..high_level_ai_policy_v2.business_scene_routes import execute_march_policy_fields
        result = execute_march_policy_fields(state, entered, target)
    elif target in (213312, 213424, 213694, 213878, 214078, 214120, 214330, 214520, 214600, 214634, 214704, 214810, 215166, 215342, 215538, 215596, 216016, 216074, 216402, 216482, 216526, 216834, 216842) and continuation == 213260:
        from ..high_level_ai_policy_v2.business_scene_packet_policy import execute_packet_policy_fields
        result = execute_packet_policy_fields(state, entered, target)
    elif target in (216980, 217188, 217320, 217394, 217428, 217506, 217616, 217734, 217922, 218044, 218092, 218100) and continuation == 216952:
        from ..high_level_ai_policy_v2.business_scene_active_packets import execute_active_packet_fields
        result = execute_active_packet_fields(state, entered, target)
    else:
        raise MovementContinuationBoundary(target, entered, 'auxiliary text child lacks a complete admitted frame')
    result = _resource_cost_frame(state, result, target)
    token = result.stack_cursor.long()
    if token != continuation:
        raise MovementContinuationBoundary(token, result, 'auxiliary text RTS slot changed')
    state.sr = state.sr & 65504 | result.status
    return first_replace(result, stack_cursor=result.stack_cursor.advance(4))
def _aux_text_dispatch_stage_fields(state: SceneState, frame: FirstDeploymentFrame,
        table: Long, base: Long, token: Long) -> FirstDeploymentFrame:
    """Live stage is reread on every original backwards branch, not a cached selector."""
    while True:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF728,2),16)
        if frame.status&8:return frame
        frame=_map_presentation_arithmetic_fields(state,frame,'target_x',1,True)
        frame=_movement_fixed_shift_word(state,frame,'target_x',1)
        frame=_movement_move(state,frame,'target_x',state.table_at(table).word(low16(frame.target_x)),16)
        frame=_aux_text_call_fields(state,frame,u32(base+s16(low16(frame.target_x))),token)
def dispatch_city_command_stage_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _aux_text_dispatch_stage_fields(state,_resource_cost_frame(state,frame,0x338C2),0x338DA,0x338EC,0x338D6)
def dispatch_map_packet_command_stage_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _aux_text_dispatch_stage_fields(state,_resource_cost_frame(state,frame,0x340F8),0x34110,0x34140,0x3410C)
def dispatch_auxiliary_command_stage_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _aux_text_dispatch_stage_fields(state,_resource_cost_frame(state,frame,0x34F64),0x34F7C,0x34F94,0x34F78)
def begin_auxiliary_command_stage_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x34F26)
    frame=_aux_text_call_fields(state,frame,0x34F36,0x34F2A)
    frame=_setup_write_fields(state,frame,0xFFFFF728,1)
    return _aux_text_call_fields(state,frame,0x34F64,0x34F34)
def upload_glyph_tile_sequence_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x353FC)
    frame=_setup_write_fields(state,frame,0xC00004,0x40200000,4)
    frame=first_replace(frame,roster=state.table_at(0x8991C).cursor(),candidates=state.table_at(0x89932).cursor())
    return expand_glyph_tile_sequence_fields(state,frame)
def calculate_glyph_row_layout_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """35478: one WORD layout algorithm; every intermediate shift defines real X."""
    frame=_resource_cost_frame(state,frame,0x35478)
    frame=_movement_move(state,frame,'unit',low16(frame.target_x),16)
    frame=_movement_fixed_shift_word(state,frame,'unit',3)
    frame=_map_presentation_arithmetic_fields(state,frame,'unit',20)
    frame=_movement_move(state,frame,'unit',low16(frame.unit)&0xFFE0,16)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame=_aux_text_shift_word_fields(state,frame,'target_y',6)
    frame=_map_presentation_arithmetic_fields(state,frame,'target_y',low16(frame.unit))
    frame=_movement_move(state,frame,'unit',low16(frame.target_y),16)
    return _movement_fixed_shift_word(state,frame,'unit',2,True)
def select_glyph_bitmap_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """35490: true WORD save/pop and signed-WORD font directory address."""
    frame=_resource_cost_frame(state,frame,0x35490)
    stack=frame.stack_cursor.advance(-2);stack.set_word(0,low16(frame.count))
    frame=first_replace(frame,stack_cursor=stack)
    frame=_movement_test(state,frame,low16(frame.count),16)
    frame=_movement_move(state,frame,'distance',low16(frame.count),16)
    frame=_movement_move_long(state,frame,'count',frame.count&0xFF00)
    frame=_glyph_shift_long_fields(SceneRefreshMemory(state),frame,'count',3)
    frame=_movement_move(state,frame,'distance',low16(frame.distance)&255,16)
    frame=_aux_text_shift_word_fields(state,frame,'distance',5)
    frame=_map_presentation_arithmetic_fields(state,frame,'count',low16(frame.distance))
    frame=first_replace(frame,scan=state.table_at(u32(0x8159C+s16(low16(frame.count)))).cursor())
    frame=_movement_move(state,frame,'count',frame.stack_cursor.word(),16)
    return first_replace(frame,stack_cursor=frame.stack_cursor.advance(2))
def expand_monochrome_glyph_byte_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """354B2's distinct monochrome branch retains ROXL flags when the pixel is unset.

    This is not AF04's unconditional two-colour OR row: its source is A3,
    its hard-wired set pixel is one, and BCC skips the OR entirely.
    """
    frame=_resource_cost_frame(state,frame,0x354B2)
    frame=_movement_move(state,frame,'offset_y',frame.scan.byte(),8)
    frame=first_replace(frame,scan=frame.scan.advance(1))
    frame=_movement_move_long(state,frame,'choice',0)
    frame=_movement_move(state,frame,'offset_x',7,16)
    while True:
        frame=_glyph_shift_long_fields(SceneRefreshMemory(state),frame,'choice',4)
        old=low8(frame.offset_y);carry=bool(old&128)
        bits=u8((old<<1)|bool(frame.status&16))
        status=(17 if carry else 0)|(8 if bits&128 else 0)|(4 if bits==0 else 0)
        state.sr=(state.sr&65504)|status
        frame=first_replace(frame,offset_y=replace_byte(frame.offset_y,bits),status=status)
        if carry:frame=_movement_move(state,frame,'choice',low8(frame.choice)|1,8)
        frame,again=_map_presentation_db_fields(frame,'offset_x')
        if not again:return frame
def _aux_text_clear_glyph_pair_fields(state: SceneState, frame: FirstDeploymentFrame,
        double: bool=False) -> FirstDeploymentFrame:
    frame=_movement_move_long(state,frame,'choice',0)
    offsets=(0,4) if double else (0,)
    for offset in offsets:frame=_setup_write_fields(state,frame,u32(frame.controller.base+offset),0,4)
    for offset in offsets:frame=_setup_write_fields(state,frame,u32(frame.controller.base+s16(low16(frame.target_y))+offset),0,4)
    return first_replace(frame,controller=frame.controller.advance(8 if double else 4))
def expand_glyph_tile_sequence_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Actual 35412 alternate entry and the complete sentinel/spacing/padding loop."""
    frame=_resource_cost_frame(state,frame,0x35412)
    while True:
        frame=first_replace(frame,controller=state.table_at(0xFFFFD300).cursor())
        frame=_movement_move(state,frame,'target_x',0,16)
        frame=_movement_move(state,frame,'target_x',frame.roster.byte(),8)
        frame=first_replace(frame,roster=frame.roster.advance(1))
        if frame.status&8:return frame
        if frame.status&4:continue
        frame=_aux_text_call_fields(state,frame,0x35478,0x35422)
        while True:
            frame=_movement_move(state,frame,'count',frame.candidates.word(),16)
            frame=first_replace(frame,candidates=frame.candidates.advance(2))
            frame=_aux_text_call_fields(state,frame,0x35490,0x35428)
            frame=_movement_move(state,frame,'distance',15,16)
            while True:
                frame=_aux_text_call_fields(state,frame,0x354B2,0x35430)
                frame=_setup_write_fields(state,frame,frame.controller.base,frame.choice,4)
                frame=_aux_text_call_fields(state,frame,0x354B2,0x35436)
                frame=_setup_write_fields(state,frame,u32(frame.controller.base+s16(low16(frame.target_y))),frame.choice,4)
                frame=first_replace(frame,controller=frame.controller.advance(4))
                frame=_map_presentation_arithmetic_fields(state,frame,'unit',1,True)
                frame,again=_map_presentation_db_fields(frame,'distance')
                if not again:break
            frame=_map_presentation_arithmetic_fields(state,frame,'target_x',1,True)
            if frame.status&4:break
            frame=_aux_text_clear_glyph_pair_fields(state,frame,True)
            frame=_map_presentation_arithmetic_fields(state,frame,'unit',2,True)
        frame=_movement_test(state,frame,low16(frame.unit),16)
        if not frame.status&4:
            frame=_map_presentation_arithmetic_fields(state,frame,'unit',1,True)
            while True:
                frame=_aux_text_clear_glyph_pair_fields(state,frame)
                frame,again=_map_presentation_db_fields(frame,'unit')
                if not again:break
        frame=_aux_text_call_fields(state,frame,0x354CA,0x35474)
def upload_expanded_glyph_rows_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x354CA)
    frame=first_replace(frame,controller=state.table_at(0xFFFFD300).cursor())
    frame=_movement_fixed_shift_word(state,frame,'target_y',1,True)
    frame=_map_presentation_arithmetic_fields(state,frame,'target_y',1,True)
    while True:
        value=frame.controller.long()
        frame=first_replace(frame,controller=frame.controller.advance(4))
        frame=_setup_write_fields(state,frame,0xC00000,value,4)
        frame,again=_map_presentation_db_fields(frame,'target_y')
        if not again:return frame
def draw_auxiliary_text_panel_border_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x35644)
    frame=_movement_move(state,frame,'target_x',10,16)
    frame=_movement_move(state,frame,'unit',5,16)
    while True:
        frame=_movement_move(state,frame,'distance',low16(frame.target_x),16)
        frame=_setup_write_fields(state,frame,frame.auxiliary.base,frame.target_y,4)
        frame=_movement_move(state,frame,'count',7,16)
        while True:
            frame=_setup_write_fields(state,frame,frame.scratch.base,low16(frame.distance))
            frame=_map_presentation_arithmetic_fields(state,frame,'distance',6)
            frame,again=_map_presentation_db_fields(frame,'count')
            if not again:break
        frame=_movement_compare(state,frame,low16(frame.unit),3,16)
        middle=bool(frame.status&4)
        if middle:frame=_movement_move(state,frame,'offset_x',0x210F,16)
        else:
            frame=_movement_compare(state,frame,low16(frame.unit),2,16)
            middle=bool(frame.status&4)
            if middle:frame=_movement_move(state,frame,'offset_x',0x2101,16)
        if middle:
            frame=_setup_write_fields(state,frame,frame.scratch.base,0)
            frame=_setup_write_fields(state,frame,frame.scratch.base,0)
            frame=_movement_move(state,frame,'count',13,16)
            while True:
                frame=_setup_write_fields(state,frame,frame.scratch.base,low16(frame.offset_x))
                frame=_map_presentation_arithmetic_fields(state,frame,'offset_x',1)
                frame,again=_map_presentation_db_fields(frame,'count')
                if not again:break
        frame=_map_presentation_arithmetic_fields(state,frame,'target_x',1,True)
        frame=_movement_arithmetic_long(state,frame,'target_y',0x20000,True)
        frame,again=_map_presentation_db_fields(frame,'unit')
        if not again:return frame
def draw_auxiliary_text_panel_rows_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x3569A)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF348,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',2)
    frame=first_replace(frame,roster=state.table_at(state.table_at(0x35710).long(low16(frame.target_x))).cursor())
    frame=_movement_move(state,frame,'count',8,16)
    frame=first_replace(frame,roster=frame.roster.advance(1))
    while True:
        frame=_movement_move(state,frame,'distance',frame.roster.byte(),8)
        frame=first_replace(frame,roster=frame.roster.advance(1))
        frame=_movement_move(state,frame,'distance',low16(frame.distance)&255,16)
        frame=_movement_move(state,frame,'offset_x',low16(frame.distance),16)
        frame=_movement_fixed_shift_word(state,frame,'offset_x',1)
        frame=_map_presentation_arithmetic_fields(state,frame,'offset_x',5)
        frame=_movement_fixed_shift_word(state,frame,'offset_x',3,True)
        frame=_movement_fixed_shift_word(state,frame,'distance',1)
        frame=_map_presentation_arithmetic_fields(state,frame,'distance',low16(frame.offset_x))
        frame=_movement_move(state,frame,'offset_x',low16(frame.unit),16)
        frame=_map_presentation_arithmetic_fields(state,frame,'offset_x',low16(frame.distance))
        frame=_movement_move(state,frame,'offset_y',low16(frame.distance),16)
        frame=_map_presentation_arithmetic_fields(state,frame,'offset_y',1,True)
        frame=_setup_write_fields(state,frame,frame.auxiliary.base,frame.target_y,4)
        while True:
            frame=_setup_write_fields(state,frame,frame.scratch.base,low16(frame.offset_x))
            frame=_map_presentation_arithmetic_fields(state,frame,'offset_x',1)
            frame,again=_map_presentation_db_fields(frame,'offset_y')
            if not again:break
        frame=_movement_arithmetic_long(state,frame,'target_y',0x20000,True)
        frame=_setup_write_fields(state,frame,frame.auxiliary.base,frame.target_y,4)
        frame=_movement_move(state,frame,'offset_y',low16(frame.distance),16)
        frame=_map_presentation_arithmetic_fields(state,frame,'offset_y',1,True)
        while True:
            frame=_setup_write_fields(state,frame,frame.scratch.base,low16(frame.unit))
            frame=_map_presentation_arithmetic_fields(state,frame,'unit',1)
            frame,again=_map_presentation_db_fields(frame,'offset_y')
            if not again:break
        frame=_movement_arithmetic_long(state,frame,'target_y',0x40000,True)
        frame=_map_presentation_arithmetic_fields(state,frame,'unit',low16(frame.distance))
        frame,again=_map_presentation_db_fields(frame,'count')
        if not again:return frame
def upload_auxiliary_text_panel_glyphs_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x356F2)
    frame=_setup_write_fields(state,frame,0xC00004,0x60200000,4)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF348,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',2)
    frame=first_replace(frame,roster=state.table_at(state.table_at(0x35710).long(low16(frame.target_x))).cursor(),
        candidates=state.table_at(state.table_at(0x35728).long(low16(frame.target_x))).cursor())
    return _aux_text_call_fields(state,frame,0x35412,0x3570E)
def draw_auxiliary_text_panel_markers_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x35740)
    for carrier,value in (('auxiliary',0x43420003),('scratch',0x00350036),
            ('scratch',0x00370038),('auxiliary',0x44440003),('scratch',0x003D003E)):
        address=frame.auxiliary.base if carrier=='auxiliary' else frame.scratch.base
        frame=_setup_write_fields(state,frame,address,value,4)
    return frame
def initialize_auxiliary_text_panel_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x355DA)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF348,2),16)
    frame=_movement_move(state,frame,'target_x',state.table_at(0x3563E).byte(low16(frame.target_x)),8)
    frame=_setup_write_fields(state,frame,0xFFFFF34A,low16(frame.target_x))
    frame=_movement_move(state,frame,'target_y',5,16)
    frame=_aux_text_call_fields(state,frame,0x661D4,0x355F0)
    frame=first_replace(frame,roster=state.table_at(0xFFFFFB00).cursor(),candidates=state.table_at(0xFFFFFB80).cursor())
    frame=_movement_move(state,frame,'target_x',7,16)
    while True:
        value=frame.roster.long();frame=first_replace(frame,roster=frame.roster.advance(4))
        frame=_setup_write_fields(state,frame,frame.candidates.base,value,4)
        frame=first_replace(frame,candidates=frame.candidates.advance(4))
        frame,again=_map_presentation_db_fields(frame,'target_x')
        if not again:break
    frame=_setup_write_fields(state,frame,frame.candidates.base,0xEEE,4)
    frame=first_replace(frame,auxiliary=state.table_at(0xC00004).cursor(),scratch=state.table_at(0xC00000).cursor())
    frame=_movement_move_long(state,frame,'target_y',0x41CA0003)
    frame=_setup_write_fields(state,frame,frame.auxiliary.base,0x8F80)
    frame=_aux_text_call_fields(state,frame,0x35644,0x35622)
    frame=_movement_arithmetic_long(state,frame,'target_y',0x840000,True)
    frame=_movement_move(state,frame,'unit',0x211D,16)
    frame=_aux_text_call_fields(state,frame,0x3569A,0x35630)
    frame=_setup_write_fields(state,frame,frame.auxiliary.base,0x8F02)
    frame=_aux_text_call_fields(state,frame,0x356F2,0x35638)
    return _aux_text_call_fields(state,frame,0x35740,0x3563C)

def decode_unmasked_literal_plane_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """240310 literal prefix: clear mask, set literal mode, then BRA into the same complete240346 decoder tail. Preserve D6 and the original outer CALL token."""
    frame = _resource_cost_frame(state, frame, 240310)
    frame = _setup_write_fields(state, frame, 4294934528, 0, clear=True)
    frame = _setup_write_fields(state, frame, 4294934530, 1)
    from ..high_level_scene_flows.business_scene import read_vdp_plane_rle_rows_from_literal_fields
    return read_vdp_plane_rle_rows_from_literal_fields(SceneRefreshMemory(state), frame)
def decode_high_plane_rows_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3AAC2 high-plane prefix: preserve the original mask, D6, full frame and outer CALL token; BRA3AAD6 enters the sole complete decoder."""
    frame = _resource_cost_frame(state, frame, 240322)
    frame = _setup_write_fields(state, frame, 4294934528, 32768)
    frame = _movement_move(state, frame, 'offset_y', 32, 16)
    from ..high_level_scene_flows.business_scene import read_vdp_plane_rle_rows_from_control_fields
    return read_vdp_plane_rle_rows_from_control_fields(SceneRefreshMemory(state), frame)
def dispatch_repeating_scene_presentation_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3B794 real indexed JMP: enter the five genuine story-table BRA owners with the same full frame and caller slot. Unknown computed targets retain their boundary."""
    frame = _resource_cost_frame(state, frame, 243604)
    frame = _movement_move(state, frame, 'target_x', state.read(4294934746, 2), 16)
    frame = _setup_asl_word_fields(state, frame, 'target_x', 2)
    target = u32(243614 + s16(low16(frame.target_x)))
    if target in (243614, 243618, 243622, 243626, 243630):
        from ..high_level_scene_flows.business_scene import _story_known_fields
        return _story_known_fields(SceneRefreshMemory(state), frame, target)
    raise MovementContinuationBoundary(target, frame, 'computed presentation JMP entry requires its genuine owner facade')
def run_repeating_scene_presentation_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3B732's complete main loop, with physical calls and no invented input/IRQ progress."""
    frame=_resource_cost_frame(state,frame,0x3B732)
    frame=_controller_setup_interrupt_status_fields(state,frame,0x2700)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF606,2),16)
    frame=_movement_move(state,frame,'target_x',low8(frame.target_x)&0xBF,8)
    frame=_setup_write_fields(state,frame,0xC00004,low16(frame.target_x))
    frame=_aux_text_call_fields(state,frame,0x68CE,0x3B74A)
    frame=_aux_text_call_fields(state,frame,0x3DAEC,0x3B74E)
    frame=_aux_text_call_fields(state,frame,0x3AA8A,0x3B752)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFF80DA,2),16)
    frame=_setup_asl_word_fields(state,frame,'target_x',1)
    frame=_movement_move(state,frame,'target_x',state.table_at(0x3B788).word(low16(frame.target_x)),16)
    frame=_aux_text_call_fields(state,frame,0x808A,0x3B762)
    frame=_controller_setup_interrupt_status_fields(state,frame,0x2500)
    while True:
        frame=_setup_write_fields(state,frame,0xFFFFF612,0x500)
        for target,token in ((0x83C8,0x3B772),(0x3B288,0x3B776),
                (0x3A978,0x3B77A),(0x3B794,0x3B77E),(0x3B23C,0x3B784)):
            frame=_aux_text_call_fields(state,frame,target,token)
def _object_scene_directory_fields(state: SceneState, frame: FirstDeploymentFrame,
        directory: Long) -> FirstDeploymentFrame:
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFF80DA,2),16)
    frame=_setup_asl_word_fields(state,frame,'target_x',2)
    frame=first_replace(frame,roster=state.table_at(directory).cursor())
    pointer=frame.roster.long(low16(frame.target_x))
    return first_replace(frame,roster=state.table_at(pointer).cursor())
def initialize_object_scene_video_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3DAEC: all video registers, RAM mirrors, tile streams, planes and palette directory."""
    frame=_resource_cost_frame(state,frame,0x3DAEC)
    for value in (0x8F02,0x8230,0x8330,0x8407,0x8568,0x8700,0x8B00,
            0x8C81,0x8D35,0x8F02,0x9011,0x9194,0x9200):
        frame=_setup_write_fields(state,frame,0xC00004,value)
    for address,value in ((0xFFFF8020,0x30),(0xFFFF8024,0),(0xFFFF8026,0x30),
            (0xFFFF8022,0x20),(0xFFFF8028,0),(0xFFFF802A,0x20)):
        frame=_setup_write_fields(state,frame,address,value)
    for directory,video,token in ((0x3DC54,0,0x3DB90),(0x3DC68,0x2000,0x3DBA8),
            (0x3DC7C,0x4000,0x3DBC0)):
        frame=_object_scene_directory_fields(state,frame,directory)
        frame=_movement_move(state,frame,'target_x',video,16)
        frame=_aux_text_call_fields(state,frame,0x3AB52,token)
    for source,video,token in ((0x4E090,0x8000,0x3DBCE),(0x4FBE4,0xA000,0x3DBDC)):
        frame=first_replace(frame,roster=state.table_at(source).cursor())
        frame=_movement_move(state,frame,'target_x',video,16)
        frame=_aux_text_call_fields(state,frame,0x3AB52,token)
    for directory,address,token in ((0x3DC90,0xE000,0x3DBFC),(0x3DCA4,0xF000,0x3DC1C)):
        frame=_object_scene_directory_fields(state,frame,directory)
        frame=first_replace(frame,candidates=state.table_at(address).cursor())
        frame=_movement_move_long(state,frame,'offset_x',0x80)
        frame=_aux_text_call_fields(state,frame,0x3AACE,token)
    for source,address,target,token in ((0x45413,0xC000,0x3AAC2,0x3DC32),
            (0x456EC,0xC040,0x3AAC2,0x3DC48)):
        frame=first_replace(frame,roster=state.table_at(source).cursor(),candidates=state.table_at(address).cursor())
        frame=_movement_move_long(state,frame,'offset_x',0x80)
        frame=_aux_text_call_fields(state,frame,target,token)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFF80DA,2),16)
    frame=_map_presentation_arithmetic_fields(state,frame,'target_x',4)
    return _aux_text_call_fields(state,frame,0x3AB94,0x3DC52)

def _aux_text_legacy_glyph_fields(state: SceneState, layout: GlyphTileLayout) -> FirstDeploymentFrame:
    checked_context(layout,GlyphTileLayout,state)
    return first_replace(FirstDeploymentFrame.unobserved(),target_x=layout.value,
        target_y=layout.row_stride,unit=layout.remaining,count=layout.glyph,
        distance=layout.rows,offset_x=layout.shift_count,offset_y=layout.packed_bits,
        choice=layout.pixels,roster=layout.counts,candidates=layout.identifiers,
        controller=layout.destination,scan=layout.bitmap)
def _aux_text_legacy_glyph_result(state: SceneState, layout: GlyphTileLayout,
        frame: FirstDeploymentFrame) -> GlyphTileLayout:
    return replace(layout,value=frame.target_x,row_stride=frame.target_y,
        remaining=frame.unit,glyph=frame.count,rows=frame.distance,
        shift_count=frame.offset_x,packed_bits=frame.offset_y,pixels=frame.choice,
        counts=frame.roster,identifiers=frame.candidates,bitmap=frame.scan,
        destination=None if frame.controller is None else frame.controller.cursor()).validate(state)
def _object_scene_legacy_fields(state: SceneState, observed: ScenePresentation) -> FirstDeploymentFrame:
    """Independent VideoPlaneAddress is an observed physical A1, not an invented RAM pointer."""
    checked_context(observed,ScenePresentation,state)
    destination=observed.destination
    if observed.video_address is not None:
        destination=state.table_at(observed.video_address.carrier).cursor()
    return first_replace(FirstDeploymentFrame.unobserved(),target_x=observed.command,
        target_y=observed.foreground,unit=observed.mode,count=observed.rows,
        distance=observed.tile,offset_x=observed.stride,offset_y=observed.palette,
        choice=observed.remaining,roster=observed.source,candidates=destination,
        controller=observed.actor,scan=observed.opponent)
def _object_scene_legacy_result(state: SceneState, observed: ScenePresentation,
        frame: FirstDeploymentFrame) -> ScenePresentation:
    destination=None if frame.candidates is None else frame.candidates.cursor()
    address=observed.video_address
    if address is not None and destination is not None:
        address=VideoPlaneAddress(destination.base);destination=None
    return replace(observed,command=frame.target_x,foreground=frame.target_y,
        mode=frame.unit,rows=frame.count,tile=frame.distance,stride=frame.offset_x,
        palette=frame.offset_y,remaining=frame.choice,source=frame.roster,
        destination=destination,actor=frame.controller,opponent=frame.scan,
        video_address=address).validate(state)


def recover_unacted_officer_b200_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """E82E: recover eligible own-force idle officers, with the actual CPU fields.

    Preserve the original inclusive city40 bound and WORD addition wrap before
    the live capacity comparisons. D4/D5/D6, A6 and entry A7 are untouched;
    DBRA changes only D0's WORD, never CCR. There is no nested CALL here.
    """
    frame = _resource_cost_frame(state, frame, 0xE82E)
    frame = first_replace(frame,
        roster=state.table_at(0xFFFFCC00).cursor(),
        candidates=state.table_at(0xFFFFF427).cursor(),
        controller=state.table_at(0xFFFFCD00).cursor(),
        scan=state.table_at(0xFFFFB200).cursor(),
        opponent=state.table_at(0xFFFFB000),
        scratch=state.table_at(0xFFFFEA38))
    frame = _movement_move(state, frame, 'target_x', 255, 16)
    frame = _movement_move(state, frame, 'choice', state.read(0xFFFFF376, 2), 16)
    while True:
        frame = _movement_move(state, frame, 'target_y', 0, 16)
        frame = _movement_move(state, frame, 'target_y',
            frame.roster.byte(s16(low16(frame.target_x))), 8)
        frame = _movement_compare(state, frame, low8(frame.target_y), 40, 8)
        if frame.status & 5:
            city = s16(low16(frame.target_y))
            frame = _movement_test(state, frame, frame.scratch.byte(city), 8)
            if frame.status & 4:
                frame = _movement_compare(state, frame, low8(frame.choice),
                    frame.candidates.byte(city), 8)
                if frame.status & 4:
                    frame = _movement_test(state, frame,
                        frame.controller.byte(s16(low16(frame.target_x))), 8)
                    if frame.status & 4:
                        frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)
                        frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
                        offset = s16(low16(frame.target_y))
                        frame = _movement_move(state, frame, 'unit', frame.opponent.word(offset), 16)
                        frame = _movement_multiply_word(state, frame, 'unit', 15)
                        frame = _movement_divu_word(state, frame, 'unit', 100, 0xE880)
                        frame = _movement_move(state, frame, 'count', frame.scan.word(offset), 16)
                        frame = _movement_add_word(state, frame, 'count', low16(frame.unit))
                        frame = _movement_compare(state, frame, low16(frame.count), frame.opponent.word(offset), 16)
                        if not frame.status & 5:
                            frame = _movement_move(state, frame, 'count', frame.opponent.word(offset), 16)
                        frame = _settlement_store_word_fields(state, frame, frame.scan,
                            offset, low16(frame.count))
        frame, more = _map_presentation_db_fields(frame, 'target_x')
        if not more:
            return frame


def load_active_packet_roster_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34F36..34F64: copy the active packet's reverse roster into F72A.

    The packet's low nibble is the original WORD counter, not a validated
    Python length.  A zero nibble retains the original SUBQ/DBRA underflow.
    The caller owns its existing return LONG; this leaf does not pop it.
    """
    frame = _resource_cost_frame(state, frame, 216886)
    frame = first_replace(frame, roster=state.table_at(state.read(16726060, 4)).cursor(), candidates=state.table_at(4294965034).cursor())
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(0, 4), 8)
    frame = _setup_write_fields(state, frame, 4294964086, low16(frame.target_y))
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
    frame = _map_presentation_arithmetic_fields(state, frame, 'target_x', 1, True)
    while True:
        frame = _movement_move(state, frame, 'target_y', 0, 16)
        frame = _movement_move(state, frame, 'target_y', frame.roster.byte(low16(frame.target_x), 13), 8)
        frame = _setup_write_fields(state, frame, frame.candidates.base, low16(frame.target_y))
        frame = first_replace(frame, candidates=frame.candidates.advance(2))
        frame, again = _map_presentation_db_fields(frame, 'target_x')
        if not again:
            break
    return _setup_write_fields(state, frame, frame.candidates.base, 65535)


def _clear_invalid_debt_record_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Shared E8B8/E8D2 inline tail: clear one live record and its flag.

    CLR retains the actual original bus read. Dynamic BCLR modifies only Z
    and the indexed bit of D3's LONG; the following MOVE.W supplies final NZ.
    This Python helper adds no original CALL, return token or SP adjustment.
    """
    frame = _setup_write_fields(state, frame, frame.roster.base, 0, 4, True)
    frame = _movement_move(state, frame, 'count', state.read(0xFFFFE700, 2), 16)
    record_mask = 1 << (low16(frame.target_x) & 31)
    frame = _map_presentation_bit_fields(state, frame, frame.count, record_mask)
    frame = first_replace(frame, count=frame.count & ~record_mask)
    return _setup_write_fields(state, frame, 0xFFFFE700, low16(frame.count))


def clear_unowned_debt_records_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """E8A0: remove debt records whose first or second city has no owner.

    Scan the original sixteen records in descending slot order. A zero first
    city alone means an empty slot; the second city is not additionally masked,
    clamped or zero-filtered. Any negative owner BYTE triggers cleanup. Preserve
    D0/D3 upper WORDs, unused D/A carriers, X, the actual caller SP, and the
    original final A0 one record before the table. SUBQ.L A0/DBRA change no CCR.
    """
    frame = _resource_cost_frame(state, frame, 0xE8A0)
    frame = first_replace(frame,
        roster=state.table_at(0xFFFFEA34).cursor(),
        candidates=state.table_at(0xFFFFF427).cursor())
    frame = _movement_move(state, frame, 'target_x', 15, 16)
    while True:
        frame = _movement_move(state, frame, 'count', 0, 16)
        frame = _movement_move(state, frame, 'count', frame.roster.byte(), 8)
        if not frame.status & 4:
            frame = _movement_test(state, frame,
                frame.candidates.byte(s16(low16(frame.count))), 8)
            if frame.status & 8:
                frame = _clear_invalid_debt_record_fields(state, frame)
            else:
                frame = _movement_move(state, frame, 'count', frame.roster.byte(0, 1), 8)
                frame = _movement_test(state, frame,
                    frame.candidates.byte(s16(low16(frame.count))), 8)
                if frame.status & 8:
                    frame = _clear_invalid_debt_record_fields(state, frame)
        frame = first_replace(frame, roster=frame.roster.advance(-4))
        frame, more = _map_presentation_db_fields(frame, 'target_x')
        if not more:
            return frame
