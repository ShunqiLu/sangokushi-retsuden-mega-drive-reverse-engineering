"""City projects, live map queues, targeting and force-order business logic.

Compatibility arithmetic is explicitly fixed width. Readonly parameters and
sprites are external data views; unresolved real calls expose typed operands.
"""
from dataclasses import replace
from .domain import (SceneState, Table, Cursor, Long, Word, Boundary, uint,
    u8, u16, u32, s16, low8, low16, replace_byte, replace_word, swap_words,
    negative_byte, negative_word, divu_retained, descending_inclusive,
    checked_state, ram_view, data_view, VideoPlaneAddress)
from .contexts_gameplay import (ProjectValues, MapPresentation, TargetSearch,
    BattlePolicy, SetupValues, SetupPlane, GameplayCall, checked_context)
from .contexts_render import RenderFields, checked_render_fields
from .contexts_tick import MapTickFrame, checked_tick_frame



def _ram(state, name):
    return ram_view(state, 'ram_' + name)


def _word(state, name):
    return _ram(state, name).word()


def _put(state, name, value):
    _ram(state, name).set_word(0, low16(value))


def _call(state, target, operands, continuation):
    from .services import call_target
    result = call_target(state, u32(target), GameplayCall(operands, continuation))
    if type(result) is not type(operands):
        raise Boundary('real gameplay call must return its declared operands')
    return result.validate(state)


def _indexed_call(state, operands, selector, parameters, branch_base, continuation):
    displacement = data_view(state, parameters).word(low16(selector))
    target = u32(branch_base + s16(displacement))
    return _call(state, target, operands, continuation)












def settle_first_city_project(state: SceneState, values: ProjectValues) -> ProjectValues:
    """Historical partial project API projects the sole current complete core without inventing retained fields."""
    frame = settle_first_city_project_fields(state, _city_project_legacy_entry_fields(state, values))
    return _city_project_legacy_result_fields(state, frame)


def settle_second_city_project(state: SceneState, values: ProjectValues) -> ProjectValues:
    """Historical partial project API projects the sole current complete core without inventing retained fields."""
    frame = settle_second_city_project_fields(state, _city_project_legacy_entry_fields(state, values))
    return _city_project_legacy_result_fields(state, frame)


def settle_third_city_project(state: SceneState, values: ProjectValues) -> ProjectValues:
    """Historical partial project API projects the sole current complete core without inventing retained fields."""
    frame = settle_third_city_project_fields(state, _city_project_legacy_entry_fields(state, values))
    return _city_project_legacy_result_fields(state, frame)


def settle_all_city_projects(state: SceneState, values: ProjectValues) -> ProjectValues:
    """Historical partial project API projects the sole current complete core without inventing retained fields."""
    frame = settle_all_city_projects_fields(state, _city_project_legacy_entry_fields(state, values))
    return _city_project_legacy_result_fields(state, frame)


def settle_city_projects_and_refresh_map(state: SceneState, values: ProjectValues) -> ProjectValues:
    """Historical partial project API projects the sole current complete core without inventing retained fields."""
    frame = settle_city_projects_and_refresh_map_fields(state, _city_project_legacy_entry_fields(state, values))
    return _city_project_legacy_result_fields(state, frame)


def dispatch_gameplay_command_state(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_map_presentation_legacy_map_fields(state,frame)
    returned=dispatch_gameplay_command_state_fields(state,entered)
    return _map_presentation_legacy_map_result(state,frame,returned)


def _require_packet(frame):
    if frame.packet is None:
        raise Boundary('actual live map packet is required')
    return frame.packet


def _append_map(state, frame, reset_scroll=False, initialize_clip=True):
    from .services import append_map_sprites
    if frame.source is None:
        raise Boundary('externally supplied sprite source required')
    result = append_map_sprites(state, frame.source, frame.x, frame.y, frame.attributes,
        reset_scroll=reset_scroll, initialize_clip=initialize_clip)
    return replace(frame, source=result.source, x=result.x, y=result.y, attributes=result.attributes)


def render_visible_map_packets(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_map_fields(state, frame)
    returned = render_visible_map_packets_fields(state, entered)
    return _map_presentation_legacy_map_result(state, frame, returned)


def render_selected_map_packet(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_map_fields(state, frame)
    returned = render_selected_map_packet_fields(state, entered)
    return _map_presentation_legacy_map_result(state, frame, returned)


def select_map_packet_sprite(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_map_fields(state, frame)
    returned = select_map_packet_sprite_fields(state, entered)
    return _map_presentation_legacy_map_result(state, frame, returned)


def locate_map_packet_sprite(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_map_fields(state, frame)
    returned = locate_map_packet_sprite_fields(state, entered)
    return _map_presentation_legacy_map_result(state, frame, returned)


def render_map_marker_positions(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_map_fields(state, frame)
    returned = render_map_marker_positions_fields(state, entered)
    return _map_presentation_legacy_map_result(state, frame, returned)


def _panel_destination(state):
    return _ram(state, 'd100').cursor(_word(state, 'f31a'))


def _panel_column(destination, gap, tiles):
    for row in range(len(tiles) - 1, 0, -1):
        destination.set_word(u16(gap * row), tiles[row])
    destination.append_word(tiles[0])


def append_city_currency_panel(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_map_fields(state, frame)
    returned = append_city_currency_panel_fields(state, entered)
    return _map_presentation_legacy_map_result(state, frame, returned)


def append_two_row_sequential_tiles(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_map_fields(state, frame)
    returned = append_two_row_sequential_tiles_fields(state, entered)
    return _map_presentation_legacy_map_result(state, frame, returned)


def append_city_project_panel(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_map_fields(state, frame)
    returned = append_city_project_panel_fields(state, entered)
    return _map_presentation_legacy_map_result(state, frame, returned)


def append_current_city_value(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_map_fields(state, frame)
    returned = append_current_city_value_fields(state, entered)
    return _map_presentation_legacy_map_result(state, frame, returned)


def append_selected_long_value(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_map_fields(state, frame)
    returned = append_selected_long_value_fields(state, entered)
    return _map_presentation_legacy_map_result(state, frame, returned)


def append_four_row_tile_columns(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_map_fields(state, frame)
    returned = append_four_row_tile_columns_fields(state, entered)
    return _map_presentation_legacy_map_result(state, frame, returned)


def append_four_row_status_panel(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_map_fields(state, frame)
    returned = append_four_row_status_panel_fields(state, entered)
    return _map_presentation_legacy_map_result(state, frame, returned)


def append_missing_city_queue_packets(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_map_fields(state, frame)
    returned = append_missing_city_queue_packets_fields(state, entered)
    return _map_presentation_legacy_map_result(state, frame, returned)


def sort_map_packet_queue(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_map_fields(state, frame)
    returned = sort_map_packet_queue_fields(state, entered)
    return _map_presentation_legacy_map_result(state, frame, returned)


def _upload_prompt(state, frame, parameters, remaining, command, longs, refresh=False):
    from .services import decode_glyph_rows_to_buffers, refresh_gameplay_scene
    x, y, tile = replace_word(frame.x, 1), replace_word(frame.y, 3), replace_word(frame.tile, remaining)
    result = decode_glyph_rows_to_buffers(state, data_view(state, parameters).cursor(),
        _ram(state, 'd300').cursor(), x, y, tile)
    state.write(0xC00004, 4, command)
    source = _ram(state, 'd300').cursor()
    tile = replace_word(result.remaining, u16(longs - 1))
    for _ in descending_inclusive(low16(tile)):
        state.write(0xC00000, 4, source.next_long())
    tile = replace_word(tile, 65535)
    x = refresh_gameplay_scene(state, result.background) if refresh else result.background
    return replace(frame, x=x, y=result.foreground, tile=tile, source=result.source,
        destination=source)


def upload_selected_queue_officer_name(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_map_presentation_legacy_map_fields(state,frame)
    returned=upload_selected_queue_officer_name_fields(state,entered)
    return _map_presentation_legacy_map_result(state,frame,returned)


def dispatch_queue_command_state(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_map_presentation_legacy_map_fields(state,frame)
    returned=dispatch_queue_command_state_fields(state,entered)
    return _map_presentation_legacy_map_result(state,frame,returned)


def render_city_map_entries(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_map_fields(state, frame)
    returned = render_city_map_entries_fields(state, entered)
    return _map_presentation_legacy_map_result(state, frame, returned)


def render_city_map_entry(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_map_fields(state, frame)
    returned = render_city_map_entry_fields(state, entered)
    return _map_presentation_legacy_map_result(state, frame, returned)


def upload_first_battle_prompt(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_map_presentation_legacy_map_fields(state,frame)
    returned=upload_first_battle_prompt_fields(state,entered)
    return _map_presentation_legacy_map_result(state,frame,returned)


def upload_second_battle_prompt(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_map_presentation_legacy_map_fields(state,frame)
    returned=upload_second_battle_prompt_fields(state,entered)
    return _map_presentation_legacy_map_result(state,frame,returned)


def upload_battle_action_prompt(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_map_presentation_legacy_map_fields(state,frame)
    returned=upload_battle_action_prompt_fields(state,entered)
    return _map_presentation_legacy_map_result(state,frame,returned)


def upload_battle_result_prompt(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_map_presentation_legacy_map_fields(state,frame)
    returned=upload_battle_result_prompt_fields(state,entered)
    return _map_presentation_legacy_map_result(state,frame,returned)


def upload_selected_officer_names(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_map_presentation_legacy_map_fields(state,frame)
    returned=upload_selected_officer_names_fields(state,entered)
    return _map_presentation_legacy_map_result(state,frame,returned)


def select_active_battle_controller(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_map_fields(state, frame)
    returned = select_active_battle_controller_fields(state, entered)
    return _map_presentation_legacy_map_result(state, frame, returned)


def cycle_available_direction(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_map_presentation_legacy_map_fields(state,frame)
    returned=cycle_available_direction_fields(state,entered)
    return _map_presentation_legacy_map_result(state,frame,returned)


def render_direction_choice(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_map_presentation_legacy_map_fields(state,frame)
    returned=render_direction_choice_fields(state,entered)
    return _map_presentation_legacy_map_result(state,frame,returned)


def update_direction_choice(state: SceneState, frame: MapPresentation) -> MapPresentation:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_map_presentation_legacy_map_fields(state,frame)
    returned=update_direction_choice_fields(state,entered)
    return _map_presentation_legacy_map_result(state,frame,returned)


def dispatch_target_eligibility(state: SceneState, search: TargetSearch) -> TargetSearch:
    """Historical observations project the sole current core; missing retained fields/SP stay unknown."""
    entered=_map_presentation_legacy_search_fields(state,search)
    returned=dispatch_target_eligibility_fields(state,entered)
    return _map_presentation_legacy_search_result(state,search,returned)


def append_nearby_target_candidates(state: SceneState, search: TargetSearch) -> TargetSearch:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_search_fields(state, search)
    returned = append_nearby_target_candidates_fields(state, entered)
    return _map_presentation_legacy_search_result(state, search, returned)


def build_nearby_battle_targets(state: SceneState, search: TargetSearch) -> TargetSearch:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_search_fields(state, search)
    returned = build_nearby_battle_targets_fields(state, entered)
    return _map_presentation_legacy_search_result(state, search, returned)


def _carry(state, value):
    status = state.read_status_word()
    state.set_status_word(status | 1 if value else status & 0xFFFE)


def deduct_force_supply(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """The historical main policy API projects the sole complete force-turn fields."""
    checked_context(policy, BattlePolicy, state)
    frame = deduct_force_supply_fields(state, _battle_policy_retained_frame(state, policy))
    return _battle_policy_retained_result(state, policy, frame)


def settle_both_force_supply(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """The historical main policy API projects the sole complete force-turn fields."""
    checked_context(policy, BattlePolicy, state)
    frame = settle_both_force_supply_fields(state, _battle_policy_retained_frame(state, policy))
    return _battle_policy_retained_result(state, policy, frame)


def _present_supply_notice(state, policy, force, message):
    saved_force = _word(state, 'f376')
    saved = policy.target_x, policy.target_y, policy.roster, policy.controller, policy.opponent
    _put(state, 'f376', force)
    _put(state, 'f740', message)
    result = _call(state, 0x260E4, policy, 0x22342)
    _put(state, 'f376', saved_force)
    return replace(result, target_x=saved[0], target_y=saved[1], roster=saved[2],
        controller=saved[3], opponent=saved[4])


def apply_force_supply_losses(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """The historical main policy API projects the sole complete force-turn fields."""
    checked_context(policy, BattlePolicy, state)
    frame = apply_force_supply_losses_fields(state, _battle_policy_retained_frame(state, policy))
    return _battle_policy_retained_result(state, policy, frame)


def check_battle_commanders_present(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """The historical main policy API projects the sole complete force-turn fields."""
    checked_context(policy, BattlePolicy, state)
    frame = check_battle_commanders_present_fields(state, _battle_policy_retained_frame(state, policy))
    return _battle_policy_retained_result(state, policy, frame)


def calculate_force_supply_budgets(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """The historical main policy API projects the sole complete force-turn fields."""
    checked_context(policy, BattlePolicy, state)
    frame = calculate_force_supply_budgets_fields(state, _battle_policy_retained_frame(state, policy))
    result = _battle_policy_retained_result(state, policy, frame)
    # Historical budget scan denotes A2; callers preserve their real A3 separately.
    return replace(result, scan=state.table_at(frame.controller.base).cursor(), controller=policy.controller)


def execute_secondary_force_orders(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """The historical main policy API projects the sole complete force-turn fields."""
    checked_context(policy, BattlePolicy, state)
    frame = execute_secondary_force_orders_fields(state, _battle_policy_retained_frame(state, policy))
    return _battle_policy_retained_result(state, policy, frame)


def execute_primary_force_orders(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    checked_context(policy, BattlePolicy, state)
    entered = _battle_policy_retained_frame(state, policy)
    returned = execute_primary_force_orders_frame_fields(state, entered)
    return _battle_policy_retained_result(state, policy, returned)


def process_both_battle_force_turns(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """The historical main policy API projects the sole complete force-turn fields."""
    checked_context(policy, BattlePolicy, state)
    frame = process_both_battle_force_turns_fields(state, _battle_policy_retained_frame(state, policy))
    return _battle_policy_retained_result(state, policy, frame)


def select_primary_force_order_policy(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    checked_context(policy, BattlePolicy, state)
    entered = _battle_policy_retained_frame(state, policy)
    returned = select_primary_force_order_policy_frame_fields(state, entered)
    return _battle_policy_retained_result(state, policy, returned)


def _load_battle_policy_map(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """1A438 A0 and last restored-D4 MOVE.L, within the nonstack contract."""
    from .services import BattlePolicyMemory, load_battlefield_map_fields
    checked_context(policy, BattlePolicy, state)
    source = load_battlefield_map_fields(BattlePolicyMemory(state))
    state.sr = (state.sr & 65520) | (8 if policy.distance & 2147483648 else 0) | (4 if policy.distance == 0 else 0)
    return replace(policy, roster=source.cursor())


def _read_battle_policy_anchor(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """25C02 current D0/D1/D2 and A3; last MOVE.B owns NZVC, not a reread."""
    from .services import BattlePolicyMemory, AnchorContext, read_city_deployment_anchor_fields
    checked_context(policy, BattlePolicy, state)
    fields = read_city_deployment_anchor_fields(BattlePolicyMemory(state), AnchorContext(policy.target_x, policy.target_y), policy.unit)
    fields.validate_complete(state)
    state.sr = (state.sr & 65504) | (16 if fields.extend else 0) | (8 if fields.negative else 0) | (4 if fields.zero else 0)
    return replace(policy, target_x=fields.x, target_y=fields.y, unit=fields.index, scan=fields.cells.cursor())


def initialize_battle_policy_targets(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    checked_context(policy, BattlePolicy, state)
    entered = _battle_policy_retained_frame(state, policy)
    returned = initialize_battle_policy_targets_frame_fields(state, entered)
    return _battle_policy_retained_result(state, policy, returned)


def initialize_primary_policy_targets(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    checked_context(policy, BattlePolicy, state)
    entered = _battle_policy_retained_frame(state, policy)
    returned = initialize_primary_policy_targets_frame_fields(state, entered)
    return _battle_policy_retained_result(state, policy, returned)


def initialize_secondary_policy_targets(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    checked_context(policy, BattlePolicy, state)
    entered = _battle_policy_retained_frame(state, policy)
    returned = initialize_secondary_policy_targets_frame_fields(state, entered)
    return _battle_policy_retained_result(state, policy, returned)


def collect_order_target_candidates(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    checked_context(policy, BattlePolicy, state)
    entered = _battle_policy_retained_frame(state, policy)
    returned = collect_order_target_candidates_frame_fields(state, entered)
    return _battle_policy_retained_result(state, policy, returned)


def offset_first_order_target_axis(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    checked_context(policy, BattlePolicy, state)
    entered = _battle_policy_retained_frame(state, policy)
    returned = offset_first_order_target_axis_frame_fields(state, entered)
    return _battle_policy_retained_result(state, policy, returned)


def offset_second_order_target_axis(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    checked_context(policy, BattlePolicy, state)
    entered = _battle_policy_retained_frame(state, policy)
    returned = offset_second_order_target_axis_frame_fields(state, entered)
    return _battle_policy_retained_result(state, policy, returned)


def cycle_setup_option(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = cycle_setup_option_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)





def update_first_setup_option(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = update_first_setup_option_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)


def update_second_setup_option(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = update_second_setup_option_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)


def update_third_setup_option(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = update_third_setup_option_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)


def update_fourth_setup_option(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = update_fourth_setup_option_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)





def update_setup_player_choices(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = update_setup_player_choices_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)


def render_current_setup_option(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = render_current_setup_option_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)


def advance_setup_reveal(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = advance_setup_reveal_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)


def advance_setup_dismissal(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = advance_setup_dismissal_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)


def write_setup_video_address(state: SceneState, plane: SetupPlane) -> SetupPlane:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_plane_legacy_entry_fields(state, plane)
    returned = write_setup_video_address_fields(state, entered)
    return _setup_plane_legacy_result_fields(state, plane, returned)


def advance_setup_plane_row(state: SceneState, plane: SetupPlane) -> SetupPlane:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_plane_legacy_entry_fields(state, plane)
    returned = advance_setup_plane_row_fields(state, entered)
    return _setup_plane_legacy_result_fields(state, plane, returned)


def decode_setup_plane_rows(state: SceneState, plane: SetupPlane) -> SetupPlane:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_plane_legacy_entry_fields(state, plane)
    returned = decode_setup_plane_rows_fields(state, entered)
    return _setup_plane_legacy_result_fields(state, plane, returned)


def decode_setup_plane_rows_with_masks(state: SceneState, plane: SetupPlane) -> SetupPlane:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_plane_legacy_entry_fields(state, plane)
    returned = decode_setup_plane_rows_with_masks_fields(state, entered)
    return _setup_plane_legacy_result_fields(state, plane, returned)


def initialize_setup_video(state: SceneState, values: SetupValues) -> SetupValues:
    """Historical observations project the sole current core; absent retained fields/SP remain unknown."""
    entered = _setup_legacy_entry_fields(state, values)
    returned = initialize_setup_video_fields(state, entered)
    return _setup_legacy_result_fields(state, values, returned)



def _render_from_map(frame):
    return RenderFields(frame.x, frame.y, frame.attributes, frame.tile,
        frame.officer, frame.count, frame.index, frame.remaining,
        frame.source, frame.destination, frame.packet, None, None, None, None, None)


def _render_from_tick(state, frame):
    checked_tick_frame(frame, state)
    return RenderFields(frame.motion_x, frame.motion_y, frame.attributes,
        frame.tile_count, frame.officer, frame.count, frame.index,
        frame.control_latch, frame.source, frame.destination, frame.packet,
        frame.carry, frame.zero, frame.negative, frame.overflow, frame.stack_cursor)


def _render_to_map(frame, fields):
    return replace(frame, x=fields.x, y=fields.y, attributes=fields.attributes,
        tile=fields.tile, officer=fields.officer, count=fields.count,
        index=fields.index, remaining=fields.remaining, source=fields.source,
        destination=fields.destination, packet=fields.packet)


def _render_to_tick(state, frame, fields):
    checked_render_fields(fields, state)
    result = replace(frame, motion_x=fields.x, motion_y=fields.y,
        attributes=fields.attributes, tile_count=fields.tile,
        officer=fields.officer, count=fields.count, index=fields.index,
        control_latch=fields.remaining, source=fields.source,
        destination=fields.destination, packet=fields.packet,
        carry=fields.carry, zero=fields.zero, negative=fields.negative,
        overflow=fields.overflow, stack_cursor=fields.stack_cursor)
    return checked_tick_frame(result, state)


def _render_move(fields, value, bits):
    masked = value & ((1 << bits) - 1)
    return replace(fields, carry=False, zero=masked == 0,
        negative=bool(masked & (1 << (bits - 1))), overflow=False)


def _render_compare(fields, left, right, bits):
    mask = (1 << bits) - 1
    sign = 1 << (bits - 1)
    left, right = left & mask, right & mask
    difference = (left - right) & mask
    return replace(fields, carry=left < right, zero=difference == 0,
        negative=bool(difference & sign),
        overflow=bool((left ^ right) & (left ^ difference) & sign))


def _render_add(fields, left, amount):
    left, amount = low16(left), low16(amount)
    total = left + amount
    result = u16(total)
    return replace(fields, carry=total > 65535, zero=result == 0,
        negative=bool(result & 32768),
        overflow=bool((~(left ^ amount)) & (left ^ result) & 32768))


def _render_bit(fields, value, bit):
    return replace(fields, zero=not bool(value & (1 << bit)))


def _render_packet(fields):
    if fields.packet is None:
        raise Boundary('real current map packet required')
    return fields.packet


def _render_sprite_fields(state, fields):
    from .reuse_display import append_map_sprite_transaction
    if fields.source is None:
        raise Boundary('actual external sprite source required')
    source = fields.source if type(fields.source) is Cursor else fields.source.cursor()
    fields = _render_enter_call(fields)
    result = append_map_sprite_transaction(state, source, fields.x, fields.y,
        fields.attributes, reset_scroll=False, initialize_clip=True)
    fields = _render_leave_call(fields)
    return replace(fields, source=result.source, x=result.x, y=result.y,
        attributes=result.attributes, carry=result.carry, zero=result.zero,
        negative=result.negative, overflow=result.overflow)


def _visible_map_packet_fields(state, fields):
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_render_fields(state, fields)
    returned = render_visible_map_packets_fields(state, entered)
    return _map_presentation_legacy_render_result(state, fields, returned)


def _selected_map_packet_fields(state, fields):
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_render_fields(state, fields)
    returned = render_selected_map_packet_fields(state, entered)
    return _map_presentation_legacy_render_result(state, fields, returned)


def _select_map_sprite_fields(state, fields):
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_render_fields(state, fields)
    returned = select_map_packet_sprite_fields(state, entered)
    return _map_presentation_legacy_render_result(state, fields, returned)


def _locate_map_sprite_fields(state, fields):
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_render_fields(state, fields)
    returned = locate_map_packet_sprite_fields(state, entered)
    return _map_presentation_legacy_render_result(state, fields, returned)


def _map_marker_fields(state, fields):
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_render_fields(state, fields)
    returned = render_map_marker_positions_fields(state, entered)
    return _map_presentation_legacy_render_result(state, fields, returned)


def _city_map_fields(state, fields):
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_render_fields(state, fields)
    returned = render_city_map_entries_fields(state, entered)
    return _map_presentation_legacy_render_result(state, fields, returned)


def _city_map_entry_fields(state, fields):
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_render_fields(state, fields)
    returned = render_city_map_entry_fields(state, entered)
    return _map_presentation_legacy_render_result(state, fields, returned)


def _active_controller_fields(state, fields):
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    entered = _map_presentation_legacy_render_fields(state, fields)
    returned = select_active_battle_controller_fields(state, entered)
    return _map_presentation_legacy_render_result(state, fields, returned)


def render_visible_map_packets_complete(state: SceneState, frame: MapTickFrame) -> MapTickFrame:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    observed = _render_from_tick(state, frame)
    entered = _map_presentation_legacy_render_fields(state, observed)
    returned = render_visible_map_packets_fields(state, entered)
    return _render_to_tick(state, frame, _map_presentation_legacy_render_result(state, observed, returned))


def render_city_map_entries_complete(state: SceneState, frame: MapTickFrame) -> MapTickFrame:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    observed = _render_from_tick(state, frame)
    entered = _map_presentation_legacy_render_fields(state, observed)
    returned = render_city_map_entries_fields(state, entered)
    return _render_to_tick(state, frame, _map_presentation_legacy_render_result(state, observed, returned))


def select_active_battle_controller_complete(state: SceneState, frame: MapTickFrame) -> MapTickFrame:
    """Historical observations project the sole current core; no missing address/SP/flag is invented."""
    observed = _render_from_tick(state, frame)
    entered = _map_presentation_legacy_render_fields(state, observed)
    returned = select_active_battle_controller_fields(state, entered)
    return _render_to_tick(state, frame, _map_presentation_legacy_render_result(state, observed, returned))


def _render_push_value(state, fields, value):
    if fields.stack_cursor is None:
        return fields
    stack = fields.stack_cursor.advance(-4)
    stack.set_long(0, value)
    return replace(fields, stack_cursor=stack)


def _render_pop_value(state, fields, legacy_observation):
    if fields.stack_cursor is None:
        return fields, legacy_observation
    value = fields.stack_cursor.long()
    return replace(fields, stack_cursor=fields.stack_cursor.advance(4)), value


def _render_enter_call(fields):
    if fields.stack_cursor is None:
        return fields
    return replace(fields, stack_cursor=fields.stack_cursor.advance(-4))


def _render_leave_call(fields):
    if fields.stack_cursor is None:
        return fields
    return replace(fields, stack_cursor=fields.stack_cursor.advance(4))


def _render_save_terrain(state, fields):
    if fields.source is None or fields.packet is None:
        raise Boundary('real terrain-call source and packet aliases required')
    fields = _render_push_value(state, fields, fields.packet.base)
    fields = _render_push_value(state, fields, fields.source.base)
    fields = _render_push_value(state, fields, fields.y)
    return _render_push_value(state, fields, fields.x)


def _render_restore_terrain(state, fields, legacy_observations):
    if fields.stack_cursor is None:
        return replace(fields, x=legacy_observations.x, y=legacy_observations.y,
            source=legacy_observations.source, packet=legacy_observations.packet)
    fields, x = _render_pop_value(state, fields, legacy_observations.x)
    fields, y = _render_pop_value(state, fields, legacy_observations.y)
    fields, source = _render_pop_value(state, fields, legacy_observations.source.base)
    fields, packet = _render_pop_value(state, fields, legacy_observations.packet.base)
    return replace(fields, x=x, y=y, source=state.table_at(source).cursor(),
        packet=state.table_at(packet).cursor())


def _enter_battle_policy_call(state: SceneState, policy: BattlePolicy, continuation: Long) -> BattlePolicy:
    """Current policy entry-SP, actual known BSR return LONG, no dummy slot."""
    checked_context(policy, BattlePolicy, state)
    uint(continuation, 32)
    if policy.stack_cursor is None:
        raise Boundary('complete battle-policy call requires actual current A7')
    stack = policy.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    return replace(policy, stack_cursor=stack)


def _leave_battle_policy_call(state: SceneState, policy: BattlePolicy, continuation: Long) -> BattlePolicy:
    checked_context(policy, BattlePolicy, state)
    uint(continuation, 32)
    if policy.stack_cursor is None:
        raise Boundary('complete battle-policy return requires current A7')
    actual = policy.stack_cursor.long()
    if actual != continuation:
        raise Boundary('battle-policy return slot changed to actual target ' + str(actual))
    return replace(policy, stack_cursor=policy.stack_cursor.advance(4))


def _battle_policy_second_anchor(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    from .services import BattlePolicyMemory, AnchorContext, read_city_second_deployment_anchor_fields
    checked_context(policy, BattlePolicy, state)
    fields = read_city_second_deployment_anchor_fields(BattlePolicyMemory(state),
        AnchorContext(policy.target_x, policy.target_y), policy.unit).validate_complete(state)
    state.sr = (state.sr & 65504) | (16 if fields.extend else 0) | (4 if fields.zero else 0) | (1 if fields.extend else 0)
    return replace(policy, target_x=fields.x, target_y=fields.y,
        unit=fields.index, scan=fields.cells.cursor())


def _battle_policy_occupied(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    from .services import BattlePolicyMemory, build_deployment_occupied_cell_fields
    checked_context(policy, BattlePolicy, state)
    if policy.stack_cursor is None:
        raise Boundary('complete occupied builder requires actual entry A7')
    fields = build_deployment_occupied_cell_fields(BattlePolicyMemory(state),
        policy.unit, policy.count, state.sr & 16 != 0, policy.stack_cursor).validate_complete(state)
    state.sr = (state.sr & 65504) | (16 if fields.extend else 0) | 8
    return replace(policy, unit=fields.member, count=fields.coordinate,
        candidates=fields.destination, controller=fields.source,
        scan=fields.positions.cursor(), stack_cursor=fields.stack_cursor)


def _battle_policy_empty_slot(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    from .services import BattlePolicyMemory, find_next_empty_position_slot_fields
    checked_context(policy, BattlePolicy, state)
    if policy.scan is None or policy.candidates is None:
        raise Boundary('actual A3 roster and A1 position views required')
    fields = find_next_empty_position_slot_fields(BattlePolicyMemory(state),
        policy.scan, policy.candidates, policy.offset_y, state.sr & 16 != 0).validate_complete(state)
    state.set_status_word((state.sr & 65504) | (16 if fields.extend else 0) | (8 if fields.negative else 0) | (4 if fields.zero else 0) | (1 if fields.carry else 0))
    return replace(policy, offset_y=fields.index, scan=fields.source)


def _call_battle_policy_occupied(state: SceneState, policy: BattlePolicy, continuation: Long) -> BattlePolicy:
    entered = _enter_battle_policy_call(state, policy, continuation)
    result = _battle_policy_occupied(state, entered)
    return _leave_battle_policy_call(state, result, continuation)


def _call_battle_policy_empty_slot(state: SceneState, policy: BattlePolicy, continuation: Long) -> BattlePolicy:
    entered = _enter_battle_policy_call(state, policy, continuation)
    result = _battle_policy_empty_slot(state, entered)
    return _leave_battle_policy_call(state, result, continuation)


def _call_battle_policy_second_anchor(state: SceneState, policy: BattlePolicy, continuation: Long) -> BattlePolicy:
    entered = _enter_battle_policy_call(state, policy, continuation)
    result = _battle_policy_second_anchor(state, entered)
    return _leave_battle_policy_call(state, result, continuation)


def _call_battle_policy_external(state: SceneState, target: Long, policy: BattlePolicy, continuation: Long) -> BattlePolicy:
    """An unresolved real BSR still has its real current-SP and token write."""
    entered = _enter_battle_policy_call(state, policy, continuation)
    if target == 0x17C8A:
        from .business_movement_support import ensure_neighbor_capacity_fields
        frame = ensure_neighbor_capacity_fields(state,
            _battle_policy_retained_frame(state, entered))
        result = _battle_policy_retained_result(state, entered, frame)
    elif target == 0x17F30:
        from .business_movement_support import integrate_selected_officer_into_packed_group_fields
        frame = integrate_selected_officer_into_packed_group_fields(state,
            _battle_policy_retained_frame(state, entered))
        result = _battle_policy_retained_result(state, entered, frame)
    elif target == 0x260E4:
        from .business_movement_support import present_battle_message_fields
        frame = present_battle_message_fields(state,
            _battle_policy_retained_frame(state, entered))
        result = _battle_policy_retained_result(state, entered, frame)
    elif target == 0x24314:
        from ..high_level_remaining_flows.business_highbank import evaluate_contact_position_order_fields
        frame = evaluate_contact_position_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame
        result = _battle_policy_retained_result(state, entered, frame)
    elif target == 0x24834:
        from ..high_level_remaining_flows.business_highbank import evaluate_anchor_position_order_fields
        frame = evaluate_anchor_position_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame
        result = _battle_policy_retained_result(state, entered, frame)
    elif target == 0x23C3E:
        from ..high_level_remaining_flows.business_highbank import evaluate_readiness_contact_action_fields
        frame = evaluate_readiness_contact_action_fields(state, _battle_policy_retained_frame(state, entered), True).frame
        result = _battle_policy_retained_result(state, entered, frame)
    elif target == 0x23CBC:
        from ..high_level_remaining_flows.business_highbank import evaluate_guarded_second_staging_order_fields
        frame = evaluate_guarded_second_staging_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame
        result = _battle_policy_retained_result(state, entered, frame)
    elif target == 0x23A94:
        from ..high_level_remaining_flows.business_highbank import evaluate_first_staging_position_fields
        frame = evaluate_first_staging_position_fields(state, _battle_policy_retained_frame(state, entered), True).frame
        result = _battle_policy_retained_result(state, entered, frame)
    else:
        result = _call(state, target, entered, continuation)
    return _leave_battle_policy_call(state, result, continuation)


def _battle_policy_edge_tail(state: SceneState, target: Long, policy: BattlePolicy) -> BattlePolicy:
    """Only the two confirmed BRA aliases share the edge core, without push."""
    checked_context(policy, BattlePolicy, state)
    if target == 0x25CBE:
        return _battle_policy_first_edge(state, policy, False)
    if target == 0x25D9C:
        return _battle_policy_second_edge(state, policy, False)
    raise Boundary('unknown original deployment tail target ' + str(target))


def _battle_policy_add_word(state: SceneState, left: Word, right: Word) -> Word:
    """Actual ADD.W/ADDQ.W conditions, including X, with no extra DATA read."""
    uint(left, 16)
    uint(right, 16)
    wide = left + right
    result = u16(wide)
    overflow = ((~(left ^ right)) & (left ^ result) & 32768) != 0
    state.sr = (state.sr & 65504) | (17 if wide > 65535 else 0) | (8 if result & 32768 else 0) | (4 if result == 0 else 0) | (2 if overflow else 0)
    return result


def _battle_policy_edge_conditions(state: SceneState, value: Word, maximum: Word) -> bool:
    """Only the fully known out-of-range tail closes here; valid ranges continue."""
    from .services import deployment_edge_coordinate_allowed
    uint(value, 16)
    uint(maximum, 16)
    if deployment_edge_coordinate_allowed(value, maximum):
        return False
    bound = 3 if value < 3 else maximum
    result = u16(value - bound)
    overflow = ((value ^ bound) & (value ^ result) & 32768) != 0
    state.set_status_word((state.sr & 65520) | (8 if result & 32768 else 0) | (4 if result == 0 else 0) | (2 if overflow else 0))
    return True


def _battle_policy_retained_frame(state: SceneState, policy: BattlePolicy):
    from .services import FirstDeploymentFrame
    checked_context(policy, BattlePolicy, state)
    frame = FirstDeploymentFrame(target_x=policy.target_x, target_y=policy.target_y,
        unit=policy.unit, count=policy.count, distance=policy.distance,
        offset_x=policy.offset_x, offset_y=policy.offset_y, choice=policy.choice,
        roster=policy.roster, candidates=policy.candidates, controller=policy.controller,
        scan=policy.scan, opponent=policy.opponent, scratch=policy.scratch,
        auxiliary=policy.auxiliary, stack_cursor=policy.stack_cursor,
        status=state.sr & 31)
    return frame.validate(state, complete=True)


def _battle_policy_retained_result(state: SceneState, policy: BattlePolicy, frame) -> BattlePolicy:
    from .services import FirstDeploymentFrame
    checked_context(policy, BattlePolicy, state)
    if type(frame) is not FirstDeploymentFrame:
        raise Boundary('complete deployment requires the sole actual retained frame')
    frame.validate(state, complete=True)
    state.sr = (state.sr & 65504) | frame.status
    return replace(policy, target_x=frame.target_x, target_y=frame.target_y,
        unit=frame.unit, count=frame.count, distance=frame.distance,
        offset_x=frame.offset_x, offset_y=frame.offset_y, choice=frame.choice,
        roster=frame.roster, candidates=frame.candidates, controller=frame.controller,
        scan=frame.scan, opponent=frame.opponent, scratch=frame.scratch,
        auxiliary=frame.auxiliary, stack_cursor=frame.stack_cursor).validate(state)


def _battle_policy_first_edge(state: SceneState, policy: BattlePolicy, prefix: bool) -> BattlePolicy:
    from .services import BattlePolicyMemory, scan_deployment_first_edge_fields
    frame = _battle_policy_retained_frame(state, policy)
    result = scan_deployment_first_edge_fields(BattlePolicyMemory(state), frame,
        low16(frame.target_x), low16(frame.target_y), low16(frame.choice),
        low16(frame.offset_y), prefix).validate(state)
    return _battle_policy_retained_result(state, policy, result.frame)


def _battle_policy_second_edge(state: SceneState, policy: BattlePolicy, prefix: bool) -> BattlePolicy:
    from .services import BattlePolicyMemory, scan_deployment_second_edge_fields
    frame = _battle_policy_retained_frame(state, policy)
    result = scan_deployment_second_edge_fields(BattlePolicyMemory(state), frame,
        low16(frame.target_x), low16(frame.target_y), low16(frame.choice),
        low16(frame.offset_y), prefix).validate(state)
    return _battle_policy_retained_result(state, policy, result.frame)


def _call_battle_policy_first_edge(state: SceneState, policy: BattlePolicy, continuation: Long) -> BattlePolicy:
    entered = _enter_battle_policy_call(state, policy, continuation)
    returned = _battle_policy_first_edge(state, entered, True)
    return _leave_battle_policy_call(state, returned, continuation)


def _call_battle_policy_second_edge(state: SceneState, policy: BattlePolicy, continuation: Long) -> BattlePolicy:
    entered = _enter_battle_policy_call(state, policy, continuation)
    returned = _battle_policy_second_edge(state, entered, True)
    return _leave_battle_policy_call(state, returned, continuation)


def _call_battle_policy_first_promotion(state: SceneState, policy: BattlePolicy, continuation: Long) -> BattlePolicy:
    from .services import BattlePolicyMemory, promote_first_roster_deployment_candidate_fields
    entered = _enter_battle_policy_call(state, policy, continuation)
    frame = _battle_policy_retained_frame(state, entered)
    returned = promote_first_roster_deployment_candidate_fields(BattlePolicyMemory(state), frame)
    policy = _battle_policy_retained_result(state, entered, returned)
    return _leave_battle_policy_call(state, policy, continuation)


def _call_battle_policy_second_promotion(state: SceneState, policy: BattlePolicy, continuation: Long) -> BattlePolicy:
    from .services import BattlePolicyMemory, promote_second_roster_deployment_candidate_fields
    entered = _enter_battle_policy_call(state, policy, continuation)
    frame = _battle_policy_retained_frame(state, entered)
    returned = promote_second_roster_deployment_candidate_fields(BattlePolicyMemory(state), frame)
    policy = _battle_policy_retained_result(state, entered, returned)
    return _leave_battle_policy_call(state, policy, continuation)


def _prepare_first_side_assignment_policy(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """23562 calls 2540E, not the separate 24AD0 selection dispatcher."""
    from .services import BattlePolicyMemory, prepare_first_side_assignment_fields
    frame = _battle_policy_retained_frame(state, policy)
    returned = prepare_first_side_assignment_fields(BattlePolicyMemory(state), frame)
    return _battle_policy_retained_result(state, policy, returned)


def _initialize_first_side_policy(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    from .services import BattlePolicyMemory, FirstDeploymentFrame, initialize_first_side_deployment_fields
    checked_context(policy, BattlePolicy, state)
    if policy.stack_cursor is None:
        raise Boundary('first-side deployment requires actual callee-entry A7')
    frame = FirstDeploymentFrame(target_x=policy.target_x, target_y=policy.target_y,
        unit=policy.unit, count=policy.count, distance=policy.distance,
        offset_x=policy.offset_x, offset_y=policy.offset_y, choice=policy.choice,
        roster=policy.roster, candidates=policy.candidates, controller=policy.controller,
        scan=policy.scan, opponent=policy.opponent, scratch=policy.scratch,
        auxiliary=policy.auxiliary, stack_cursor=policy.stack_cursor, status=state.sr & 31)
    frame.validate(state, True)
    returned = initialize_first_side_deployment_fields(BattlePolicyMemory(state), frame)
    returned.validate(state, True)
    state.sr = (state.sr & 65504) | returned.status
    return replace(policy, target_x=returned.target_x, target_y=returned.target_y,
        unit=returned.unit, count=returned.count, distance=returned.distance,
        offset_x=returned.offset_x, offset_y=returned.offset_y, choice=returned.choice,
        roster=returned.roster, candidates=returned.candidates, controller=returned.controller,
        scan=returned.scan, opponent=returned.opponent, scratch=returned.scratch,
        auxiliary=returned.auxiliary, stack_cursor=returned.stack_cursor)


def _call_battle_policy_leader_presence(state: SceneState, policy: BattlePolicy,
        continuation: Long) -> BattlePolicy:
    """23572 BSR235CC writes23576, then consumes the real restored fields."""
    from .services import BattlePolicyMemory, test_battlefield_leader_roster_presence_fields
    entered = _enter_battle_policy_call(state, policy, continuation)
    frame = _battle_policy_retained_frame(state, entered)
    fields = test_battlefield_leader_roster_presence_fields(BattlePolicyMemory(state), frame).validate(state)
    returned = _battle_policy_retained_result(state, entered, fields.frame)
    return _leave_battle_policy_call(state, returned, continuation)


# Complete actual primary order decision chain; external ABIs remain explicit.
def _order_move_flags(state: SceneState, value: Long, bits: Word) -> Long:
    uint(value, bits)
    state.sr = (state.sr & 65520) | (8 if value & (1 << (bits - 1)) else 0) | (4 if value == 0 else 0)
    return value


def _order_compare_flags(state: SceneState, left: Long, right: Long, bits: Word) -> None:
    uint(left, bits)
    uint(right, bits)
    mask = (1 << bits) - 1
    sign = 1 << (bits - 1)
    difference = (left - right) & mask
    overflow = bool((left ^ right) & (left ^ difference) & sign)
    state.sr = (state.sr & 65520) | (1 if left < right else 0) | (2 if overflow else 0) | (8 if difference & sign else 0) | (4 if difference == 0 else 0)


def _order_shift_left(state: SceneState, value: Long, count: Word, bits: Word) -> Long:
    uint(value, bits)
    uint(count, 16)
    if not 1 <= count <= 8:
        raise ValueError('actual bounded immediate shift required')
    shifted = (value << count) & ((1 << bits) - 1)
    carried = bool(value & (1 << (bits - count)))
    state.sr = (state.sr & 65504) | (17 if carried else 0) | (8 if shifted & (1 << (bits - 1)) else 0) | (4 if shifted == 0 else 0)
    return shifted


def _order_shift_right(state: SceneState, value: Word, count: Word) -> Word:
    uint(value, 16)
    uint(count, 16)
    if not 1 <= count <= 8:
        raise ValueError('actual bounded immediate shift required')
    shifted = value >> count
    carried = bool(value & (1 << (count - 1)))
    state.sr = (state.sr & 65504) | (17 if carried else 0) | (4 if shifted == 0 else 0)
    return shifted


def _order_full_sr_carry(state: SceneState, value: bool) -> None:
    if type(value) is not bool:
        raise ValueError('actual full-SR carry decision required')
    if not state.sr & 8192:
        raise Boundary('original order full-SR operation requires supervisor')
    if state.sr & 32768:
        raise Boundary('original order full-SR trace continuation unmodeled')
    state.set_status_word((state.sr & 65534) | int(value))


def _order_force_has_city_assignment(state: SceneState, policy: BattlePolicy, continuation: Long) -> BattlePolicy:
    from .services import BattlePolicyMemory, test_force_has_city_assignment_fields
    entered = _enter_battle_policy_call(state, policy, continuation)
    frame, _ = test_force_has_city_assignment_fields(BattlePolicyMemory(state), _battle_policy_retained_frame(state, entered))
    returned = _battle_policy_retained_result(state, entered, frame)
    return _leave_battle_policy_call(state, returned, continuation)


def _order_sum_first_side_troops(state: SceneState, policy: BattlePolicy, continuation: Long) -> BattlePolicy:
    from .services import BattlePolicyMemory, sum_first_side_roster_troops_fields
    entered = _enter_battle_policy_call(state, policy, continuation)
    frame, _, _ = sum_first_side_roster_troops_fields(BattlePolicyMemory(state), _battle_policy_retained_frame(state, entered))
    returned = _battle_policy_retained_result(state, entered, frame)
    return _leave_battle_policy_call(state, returned, continuation)


def _order_scaled_random(state: SceneState, policy: BattlePolicy, continuation: Long) -> BattlePolicy:
    """83D4 followed by the real ANDI.L/LSL.L/SWAP, consuming both returns."""
    from .services import sample_random_pair
    entered = _enter_battle_policy_call(state, policy, continuation)
    random = sample_random_pair(state)
    # The accepted pair retains the original 83EE ADD.W operands: updated
    # seed.low is the unfurled mixed.low, sample.low is their wrapped sum.
    state.sr = (state.sr & 65519) | (16 if low16(random.sample) < low16(random.updated_state) else 0)
    _order_move_flags(state, random.updated_state, 32)
    returned = replace(entered, target_x=random.sample, target_y=random.updated_state)
    returned = _leave_battle_policy_call(state, returned, continuation)
    sample = _order_move_flags(state, random.sample & 65535, 32)
    sample = _order_shift_left(state, sample, 3, 32)
    sample = _order_move_flags(state, swap_words(sample), 32)
    return replace(returned, target_x=sample)


def evaluate_primary_force_retreat_order(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """238AE: original troop/attribute/probability policy, with live aliases.

    The business role is probable; all operation widths and branches are
    confirmed by the supplied original listing. Modal callees stay explicit.
    """
    checked_context(policy, BattlePolicy, state)
    policy = replace(policy, roster=_ram(state, 'c800').cursor())
    offset = _order_move_flags(state, low16(policy.choice), 16)
    offset = _order_shift_left(state, offset, 2, 16)
    troops = _order_move_flags(state, policy.roster.long(offset), 32)
    policy = replace(policy, target_x=replace_word(policy.target_x, offset), target_y=troops)
    _order_compare_flags(state, troops, 200, 32)
    use_small_force_gate = troops <= 200
    if not use_small_force_gate:
        _order_compare_flags(state, troops, 500, 32)
        if troops <= 500:
            policy = replace(policy, roster=_ram(state, 'b000').cursor())
            offset = _order_shift_right(state, low16(policy.target_x), 1)
            skill = _order_move_flags(state, policy.roster.word(offset), 16)
            skill = _order_shift_right(state, skill, 2)
            policy = replace(policy, target_x=replace_word(policy.target_x, offset), target_y=replace_word(policy.target_y, skill), roster=_ram(state, 'b200').cursor())
            aptitude = policy.roster.word(offset)
            _order_compare_flags(state, skill, aptitude, 16)
            use_small_force_gate = skill >= aptitude
    if use_small_force_gate:
        gate = _order_move_flags(state, 2, 16)
        force = _order_move_flags(state, _word(state, 'f68c'), 16)
        offset = _order_shift_left(state, force, 1, 16)
        policy = replace(policy, unit=replace_word(policy.unit, gate), target_x=replace_word(policy.target_x, offset), roster=_ram(state, 'e640').cursor())
        ruler = policy.roster.word(offset)
        _order_compare_flags(state, low16(policy.choice), ruler, 16)
        if low16(policy.choice) == ruler:
            policy = replace(policy, unit=replace_word(policy.unit, _order_move_flags(state, 4, 16)))
            policy = _order_force_has_city_assignment(state, policy, 0x23904)
            if not state.sr & 1:
                _order_full_sr_carry(state, False)
                return policy
        policy = _order_scaled_random(state, policy, 0x23912)
        _order_compare_flags(state, low16(policy.target_x), low16(policy.unit), 16)
        if low16(policy.target_x) < low16(policy.unit):
            return _execute_primary_retreat_modal(state, policy)
    policy = _order_count_opposing_roster(state, policy, 0x23926)
    _order_compare_flags(state, low16(policy.target_x), 3, 16)
    use_default_comparison = low16(policy.target_x) < 3
    if not use_default_comparison:
        reserve = _order_move_flags(state, _ram(state, 'f69e').long(), 32)
        use_default_comparison = reserve != 0
    if not use_default_comparison:
        limit = _order_move_flags(state, _ram(state, 'f76c').long(), 32)
        limit = divu_retained(limit, 6)
        limit = _order_move_flags(state, limit & 65535, 32)
        policy = replace(policy, unit=limit)
        other = _ram(state, 'f6a2').long()
        _order_compare_flags(state, limit, other, 32)
        use_default_comparison = limit > other
    if use_default_comparison:
        policy = _order_sum_first_side_troops(state, policy, 0x23950)
        _order_compare_flags(state, low16(policy.unit), low16(policy.target_x), 16)
        if low16(policy.unit) > low16(policy.target_x):
            _order_full_sr_carry(state, False)
            return policy
        doubled = _order_shift_left(state, policy.count, 1, 32)
        policy = replace(policy, count=doubled)
        _order_compare_flags(state, doubled, policy.target_y, 32)
        if doubled > policy.target_y:
            _order_full_sr_carry(state, False)
            return policy
        strength = _order_move_flags(state, _ram(state, 'f76c').long(), 32)
        policy = replace(policy, target_x=strength)
        other = _ram(state, 'f6a2').long()
        _order_compare_flags(state, strength, other, 32)
        if strength < other:
            _order_full_sr_carry(state, False)
            return policy
    policy = replace(policy, unit=replace_word(policy.unit, _order_move_flags(state, 2, 16)))
    policy = _order_force_has_city_assignment(state, policy, 0x23972)
    if not state.sr & 1:
        _order_full_sr_carry(state, False)
        return policy
    policy = _order_scaled_random(state, policy, 0x23980)
    _order_compare_flags(state, low16(policy.target_x), low16(policy.unit), 16)
    if low16(policy.target_x) < low16(policy.unit):
        return _execute_primary_retreat_modal(state, policy)
    _order_full_sr_carry(state, False)
    return policy


def _execute_primary_retreat_modal(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """23998 modal tail: preserve true D7 WORD slot and real call boundaries."""
    _put(state, 'f3a6', _order_move_flags(state, low16(policy.choice), 16))
    if policy.stack_cursor is None:
        raise Boundary('primary retreat modal requires actual current A7')
    stack = policy.stack_cursor.advance(-2)
    stack.set_word(0, low16(policy.choice))
    _order_move_flags(state, low16(policy.choice), 16)
    policy = _call_battle_policy_external(state, 0x17C8A, replace(policy, stack_cursor=stack), 0x239A4)
    restored = policy.stack_cursor.word()
    policy = replace(policy, choice=replace_word(policy.choice, _order_move_flags(state, restored, 16)), stack_cursor=policy.stack_cursor.advance(2))
    tested = _order_move_flags(state, _word(state, 'f6e8'), 16)
    if negative_word(tested):
        _order_full_sr_carry(state, False)
        return policy
    policy = _call_battle_policy_external(state, 0x17F30, policy, 0x239B2)
    _put(state, 'f3d2', _order_move_flags(state, _word(state, 'f3a6'), 16))
    _put(state, 'f740', _order_move_flags(state, 302, 16))
    value = _ram(state, 'f6d7').byte()
    state.sr = (state.sr & 65531) | (0 if value & 2 else 4)
    _ram(state, 'f6d7').set_byte(0, value ^ 2)
    policy = _call_battle_policy_external(state, 0x260E4, policy, 0x239CA)
    value = _ram(state, 'f6d7').byte()
    state.sr = (state.sr & 65531) | (0 if value & 2 else 4)
    _ram(state, 'f6d7').set_byte(0, value ^ 2)
    _order_full_sr_carry(state, True)
    return policy


def _primary_order_tail(state: SceneState, target: Long, policy: BattlePolicy) -> BattlePolicy:
    """Actual BCS tails do not invent another call or return-token push."""
    if target == 0x23A76:
        return _primary_short_roster_tail(state, policy)
    if target == 0x242F6:
        return _primary_small_force_tail(state, policy)
    if target == 0x24816:
        return _primary_low_strength_fallback_tail(state, policy)
    from .services import call_target
    returned = call_target(state, target, policy)
    if type(returned) is not BattlePolicy:
        raise Boundary('primary order tail requires actual BattlePolicy return')
    return returned.validate(state)


def execute_primary_standard_order(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """23610: genuine first primary order handler; unknown next ABIs stop."""
    checked_context(policy, BattlePolicy, state)
    policy = _enter_battle_policy_call(state, policy, 0x23614)
    policy = evaluate_primary_force_retreat_order(state, policy)
    policy = _leave_battle_policy_call(state, policy, 0x23614)
    if state.sr & 1:
        return policy
    policy = _primary_single_roster_gate(state, policy)
    if state.sr & 1:
        return _primary_order_tail(state, 0x23A76, policy)
    policy = _primary_small_roster_gate(state, policy)
    if state.sr & 1:
        return _primary_order_tail(state, 0x242F6, policy)
    policy = _primary_city_rectangle_call(state, policy, 0x2362C)
    if state.sr & 1:
        return policy
    policy = _primary_standard_position_action(state, policy)
    if state.sr & 1:
        return policy
    return _primary_secondary_standard_action(state, policy)


def _execute_primary_indexed_order(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """23598-235AA: actual indexed word, saved A0/A1 and JSR return slot."""
    checked_context(policy, BattlePolicy, state)
    displacement = data_view(state, 'data_0235b6').word(low16(policy.target_x))
    _order_move_flags(state, displacement, 16)
    policy = replace(policy, target_x=replace_word(policy.target_x, displacement))
    if policy.stack_cursor is None or policy.roster is None or policy.candidates is None:
        raise Boundary('primary indexed order requires actual A0/A1/A7')
    stack = policy.stack_cursor.advance(-4)
    stack.set_long(0, policy.candidates.base)
    stack = stack.advance(-4)
    stack.set_long(0, policy.roster.base)
    policy = replace(policy, stack_cursor=stack, roster=state.table_at(0x23610).cursor())
    target = u32(0x23610 + s16(displacement))
    entered = _enter_battle_policy_call(state, policy, 0x235AA)
    if target == 0x23610:
        returned = execute_primary_standard_order(state, entered)
    elif target == 0x23A6E:
        returned = _primary_guarded_short_roster_tail(state, entered)
    elif target == 0x23CBC:
        from ..high_level_remaining_flows.business_highbank import evaluate_guarded_second_staging_order_fields
        frame = evaluate_guarded_second_staging_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame
        returned = _battle_policy_retained_result(state, entered, frame)
    elif target == 0x23D9E:
        from ..high_level_remaining_flows.business_highbank import evaluate_guarded_first_region_order_fields
        frame = evaluate_guarded_first_region_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame
        returned = _battle_policy_retained_result(state, entered, frame)
    elif target == 0x240BE:
        from ..high_level_remaining_flows.business_highbank import evaluate_guarded_second_region_order_fields
        frame = evaluate_guarded_second_region_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame
        returned = _battle_policy_retained_result(state, entered, frame)
    elif target == 0x242EE:
        from ..high_level_remaining_flows.business_highbank import evaluate_guarded_small_force_region_tail_fields
        frame = evaluate_guarded_small_force_region_tail_fields(state, _battle_policy_retained_frame(state, entered), True).frame
        returned = _battle_policy_retained_result(state, entered, frame)
    elif target == 0x24488:
        from ..high_level_remaining_flows.business_highbank import evaluate_guarded_third_region_order_fields
        frame = evaluate_guarded_third_region_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame
        returned = _battle_policy_retained_result(state, entered, frame)
    elif target == 0x245CC:
        from ..high_level_remaining_flows.business_highbank import evaluate_guarded_west_contact_order_fields
        frame = evaluate_guarded_west_contact_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame
        returned = _battle_policy_retained_result(state, entered, frame)
    elif target == 0x246C8:
        from ..high_level_remaining_flows.business_highbank import evaluate_guarded_first_staging_order_fields
        frame = evaluate_guarded_first_staging_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame
        returned = _battle_policy_retained_result(state, entered, frame)
    elif target == 0x24806:
        from ..high_level_remaining_flows.business_highbank import evaluate_guarded_terrain_region_order_fields
        frame = evaluate_guarded_terrain_region_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame
        returned = _battle_policy_retained_result(state, entered, frame)
    elif target == 0x24A7A:
        from ..high_level_remaining_flows.business_highbank import evaluate_guarded_alternate_anchor_order_fields
        frame = evaluate_guarded_alternate_anchor_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame
        returned = _battle_policy_retained_result(state, entered, frame)
    else:
        returned = _call(state, target, entered, 0x235AA)
    returned = _leave_battle_policy_call(state, returned, 0x235AA)
    stack = returned.stack_cursor
    roster = state.table_at(stack.long()).cursor()
    stack = stack.advance(4)
    orders = state.table_at(stack.long()).cursor()
    return replace(returned, roster=roster, candidates=orders, stack_cursor=stack.advance(4))


# Actual23618/23620 strength-gate calls and returns.
def _primary_single_roster_gate(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    from .services import BattlePolicyMemory, test_second_side_total_with_single_first_roster_fields
    entered = _enter_battle_policy_call(state, policy, 0x2361C)
    frame, _ = test_second_side_total_with_single_first_roster_fields(BattlePolicyMemory(state), _battle_policy_retained_frame(state, entered))
    returned = _battle_policy_retained_result(state, entered, frame)
    return _leave_battle_policy_call(state, returned, 0x2361C)


def _primary_small_roster_gate(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    from .services import BattlePolicyMemory, test_second_side_total_with_small_second_roster_fields
    entered = _enter_battle_policy_call(state, policy, 0x23624)
    frame, _ = test_second_side_total_with_small_second_roster_fields(BattlePolicyMemory(state), _battle_policy_retained_frame(state, entered))
    returned = _battle_policy_retained_result(state, entered, frame)
    return _leave_battle_policy_call(state, returned, 0x23624)


def _order_count_opposing_roster(state: SceneState, policy: BattlePolicy, continuation: Long) -> BattlePolicy:
    """Actual 23922 BSR/23926 return around the historical sole 226B6 core."""
    from .services import count_opposing_battle_roster_fields
    entered = _enter_battle_policy_call(state, policy, continuation)
    frame = _battle_policy_retained_frame(state, entered)
    returned = count_opposing_battle_roster_fields(state, frame)
    result = _battle_policy_retained_result(state, entered, returned)
    return _leave_battle_policy_call(state, result, continuation)


def _primary_secondary_standard_action(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """Real23638 BSR / 2363C return around the historical sole236E4 source."""
    from .services import evaluate_secondary_standard_action_fields
    entered = _enter_battle_policy_call(state, policy, 0x2363C)
    frame = _battle_policy_retained_frame(state, entered)
    result = evaluate_secondary_standard_action_fields(state, frame, True)
    returned = _battle_policy_retained_result(state, entered, result)
    return _leave_battle_policy_call(state, returned, 0x2363C)


def _primary_standard_position_action(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """Actual23630 BSR / 23634 return around sole2363E owner."""
    from .services import evaluate_standard_position_order_fields
    entered = _enter_battle_policy_call(state, policy, 0x23634)
    frame = _battle_policy_retained_frame(state, entered)
    fields = evaluate_standard_position_order_fields(state, frame, True).validate(state, True)
    returned = _battle_policy_retained_result(state, entered, fields.frame)
    return _leave_battle_policy_call(state, returned, 0x23634)


# Real city-trigger callers and the two short policy tails.
def _primary_city_rectangle_call(state: SceneState, policy: BattlePolicy, continuation: Long) -> BattlePolicy:
    """Real 23736 call, shared owner, full carriers/SR and physical return slot."""
    from .services import BattleTriggerMemory, BattleTriggerFrame, trigger_battle_for_city_rectangle_fields
    entered = _enter_battle_policy_call(state, policy, continuation)
    frame = BattleTriggerFrame(target_x=entered.target_x, target_y=entered.target_y,
        unit=entered.unit, count=entered.count, distance=entered.distance,
        offset_x=entered.offset_x, offset_y=entered.offset_y, choice=entered.choice,
        roster=entered.roster, candidates=entered.candidates,
        controller=entered.controller, scan=entered.scan, opponent=entered.opponent,
        scratch=entered.scratch, auxiliary=entered.auxiliary,
        stack_cursor=entered.stack_cursor, status=state.sr, legacy_context=None)
    returned = trigger_battle_for_city_rectangle_fields(BattleTriggerMemory(state),
        frame, low16(frame.choice)).validate_complete(state)
    state.sr = returned.status
    policy = replace(entered, target_x=returned.target_x, target_y=returned.target_y,
        unit=returned.unit, count=returned.count, distance=returned.distance,
        offset_x=returned.offset_x, offset_y=returned.offset_y, choice=returned.choice,
        roster=returned.roster, candidates=returned.candidates,
        controller=returned.controller, scan=returned.scan, opponent=returned.opponent,
        scratch=returned.scratch, auxiliary=returned.auxiliary,
        stack_cursor=returned.stack_cursor)
    return _leave_battle_policy_call(state, policy, continuation)


def _primary_short_roster_tail(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """23A76: genuine four-step policy tail; each call owns its real token."""
    checked_context(policy, BattlePolicy, state)
    policy = _primary_city_rectangle_call(state, policy, 0x23A7A)
    if state.sr & 1:
        return policy
    policy = _primary_other_city_retreat_call(state, policy, 0x23A82)
    if state.sr & 1:
        return policy
    policy = _call_battle_policy_external(state, 0x23C3E, policy, 0x23A8A)
    if state.sr & 1:
        return policy
    return _call_battle_policy_external(state, 0x23A94, policy, 0x23A92)


def _primary_small_force_tail(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """242F6: city trigger, two policy attempts, then the original next action."""
    checked_context(policy, BattlePolicy, state)
    policy = _primary_city_rectangle_call(state, policy, 0x242FA)
    if state.sr & 1:
        return policy
    policy = _primary_other_city_retreat_call(state, policy, 0x24302)
    if state.sr & 1:
        return policy
    policy = _primary_retreat_mark_call(state, policy, 0x2430A)
    if state.sr & 1:
        return policy
    return _call_battle_policy_external(state, 0x24314, policy, 0x24312)


# Actual22756 BSR return fields shared by both short tails.
def _primary_other_city_retreat_call(state: SceneState, policy: BattlePolicy, continuation: Long) -> BattlePolicy:
    """Actual short-tail22756 BSR/RTS; unique owner, full returns and true SP."""
    from .services import evaluate_other_city_retreat_order_fields
    entered = _enter_battle_policy_call(state, policy, continuation)
    frame = _battle_policy_retained_frame(state, entered)
    returned = evaluate_other_city_retreat_order_fields(state, frame, True)
    policy = _battle_policy_retained_result(state, entered, returned)
    return _leave_battle_policy_call(state, policy, continuation)


def _primary_guarded_short_roster_tail(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """23A6E: the actual alternate order, followed by the shared short tail.

    The strength leaf has its real23A72 call slot. BCS is a tail branch,
    not another call; the existing235AA caller slot remains owned upstream.
    """
    checked_context(policy, BattlePolicy, state)
    from .services import BattlePolicyMemory, test_second_side_relative_total_shortfall_fields
    entered = _enter_battle_policy_call(state, policy, 0x23A72)
    frame, _ = test_second_side_relative_total_shortfall_fields(
        BattlePolicyMemory(state), _battle_policy_retained_frame(state, entered))
    returned = _battle_policy_retained_result(state, entered, frame)
    policy = _leave_battle_policy_call(state, returned, 0x23A72)
    if state.sr & 1:
        return _primary_order_tail(state, 0x24816, policy)
    return _primary_short_roster_tail(state, policy)


def _primary_retreat_mark_call(state: SceneState, policy: BattlePolicy,
        continuation: Long) -> BattlePolicy:
    """Real22D30 caller slot around the shared complete retreat policy."""
    from .services import BattlePolicyMemory, mark_eligible_actor_for_retreat_fields
    entered = _enter_battle_policy_call(state, policy, continuation)
    frame, _ = mark_eligible_actor_for_retreat_fields(BattlePolicyMemory(state),
        _battle_policy_retained_frame(state, entered))
    returned = _battle_policy_retained_result(state, entered, frame)
    return _leave_battle_policy_call(state, returned, continuation)


def _primary_low_strength_fallback_tail(state: SceneState, policy: BattlePolicy) -> BattlePolicy:
    """24816: three actual attempts, then the original next-order call."""
    checked_context(policy, BattlePolicy, state)
    policy = _primary_city_rectangle_call(state, policy, 0x2481A)
    if state.sr & 1:
        return policy
    policy = _primary_other_city_retreat_call(state, policy, 0x24822)
    if state.sr & 1:
        return policy
    policy = _primary_retreat_mark_call(state, policy, 0x2482A)
    if state.sr & 1:
        return policy
    return _call_battle_policy_external(state, 0x24834, policy, 0x24832)


# Complete retained fields for both force turns and supply; one current algorithm per owner.
from .services import FirstDeploymentFrame
from .business_movement_support import (
    first_replace, _movement_move, _movement_test, _movement_compare,
    _movement_move_long, _movement_test_long, _movement_arithmetic_long,
    _movement_binary_flags, _movement_fixed_shift_word, _movement_add_word,
    _movement_multiply_word, _movement_save_longs, _movement_restore_longs,
    _movement_divu_word, present_battle_message_fields)
from ..high_level_remaining_flows.business_city import (
    _resource_cost_frame, _duel_menu_write_word_fields,
    _settlement_store_word_fields, _settlement_write_byte_fields,
    _special_action_shift_long, _special_action_swap,
    execute_deployment_menu_fields)


def _force_turn_policy_fields(frame: FirstDeploymentFrame) -> BattlePolicy:
    """An actual complete frame uses the existing main policy ABI, not a fabricated legacy input."""
    return BattlePolicy(target_x=frame.target_x, target_y=frame.target_y,
        unit=frame.unit, count=frame.count, distance=frame.distance,
        offset_x=frame.offset_x, offset_y=frame.offset_y, choice=frame.choice,
        roster=frame.roster, candidates=frame.candidates, controller=frame.controller,
        scan=frame.scan, opponent=frame.opponent, scratch=frame.scratch,
        auxiliary=frame.auxiliary, stack_cursor=frame.stack_cursor)


def _force_turn_call_fields(state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int) -> FirstDeploymentFrame:
    """Each real BSR/JSR writes its actual LONG; the callee never owns this outer slot."""
    frame = _resource_cost_frame(state, frame, target)
    uint(target, 32)
    uint(continuation, 32)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    if target == 139852:
        returned = settle_both_force_supply_fields(state, entered)
    elif target == 139896:
        returned = deduct_force_supply_fields(state, entered)
    elif target == 139944:
        returned = apply_force_supply_losses_fields(state, entered)
    elif target == 140246:
        returned = check_battle_commanders_present_fields(state, entered)
    elif target == 140312:
        returned = execute_secondary_force_orders_fields(state, entered)
    elif target == 140400:
        returned = calculate_force_supply_budgets_fields(state, entered)
    elif target == 144738:
        returned = execute_primary_force_orders_frame_fields(state, entered)
    elif target == 155876:
        returned = present_battle_message_fields(state, entered)
    else:
        returned = execute_deployment_menu_fields(state, target, entered)
    returned = _resource_cost_frame(state, returned, target)
    actual = returned.stack_cursor.long()
    if actual != continuation:
        from .business_movement_support import MovementContinuationBoundary
        raise MovementContinuationBoundary(actual, returned, 'actual force-turn child return token changed')
    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))


def process_both_battle_force_turns_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """221E4..2224C: supply first, real commander gate, then each non-player side's complete order chain."""
    frame = _resource_cost_frame(state, frame, 0x221E4)
    frame = _force_turn_call_fields(state, frame, 0x2224C, 0x221E8)
    frame = _force_turn_call_fields(state, frame, 0x223D6, 0x221EC)
    if frame.status & 1:
        return frame
    for affiliation, side, target, continuation in (
            (0xFFFFF68C, 0, 0x23562, 0x22216),
            (0xFFFFF68E, 2, 0x22418, 0x2223C)):
        frame = _movement_move(state, frame, 'target_x', state.read(affiliation, 2), 16)
        for player in (0xFFFFF67A, 0xFFFFF67C, 0xFFFFF67E):
            frame = _movement_compare(state, frame, low16(frame.target_x), state.read(player, 2), 16)
            if frame.status & 4:
                break
        else:
            frame = _duel_menu_write_word_fields(state, frame, 0xFFFFF6D6, side, clear=side == 0)
            frame = _force_turn_call_fields(state, frame, target, continuation)
    frame = _movement_compare(state, frame, state.read(0xFFFFF612, 2), 0x411, 16)
    if frame.status & 4:
        return frame
    return _duel_menu_write_word_fields(state, frame, 0xFFFFF6D6, 0, clear=True)


def settle_both_force_supply_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2224C..22278: actual shared troop/readiness views and two original deduction slots."""
    frame = _resource_cost_frame(state, frame, 0x2224C)
    frame = first_replace(frame, controller=state.table_at(0xFFFFC800), opponent=state.table_at(0xFFFFB200))
    frame = _duel_menu_write_word_fields(state, frame, 0xFFFFF6D6, 0, clear=True)
    frame = first_replace(frame, roster=state.table_at(0xFFFFA550).cursor(), candidates=state.table_at(0xFFFFF69E).cursor())
    frame = _force_turn_call_fields(state, frame, 0x22278, 0x22264)
    frame = _duel_menu_write_word_fields(state, frame, 0xFFFFF6D6, 2)
    frame = first_replace(frame, roster=state.table_at(0xFFFFA5A4).cursor(), candidates=state.table_at(0xFFFFF6A2).cursor())
    return _force_turn_call_fields(state, frame, 0x22278, 0x22276)


def _force_turn_divu_mask_fields(state: SceneState, frame: FirstDeploymentFrame,
        carrier: str, divisor: int, instruction: int) -> FirstDeploymentFrame:
    """The next ANDI.L defines N/Z/V/C; an original DIVU overflow retains Dn and X."""
    if (carrier, divisor, instruction) not in (('target_x', 100, 0x22292), ('count', 100, 0x22354)):
        raise ValueError('original masked force-loss division required')
    if frame.carrier(carrier) // divisor <= 65535:
        frame = _movement_divu_word(state, frame, carrier, divisor, instruction)
    return _movement_move_long(state, frame, carrier, frame.carrier(carrier) & 65535)


def deduct_force_supply_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """22278..222A8: actual masked member troop sum, subtract supply, then attrition only on borrow."""
    frame = _resource_cost_frame(state, frame, 0x22278)
    frame = first_replace(frame, scan=state.table_at(frame.roster.base).cursor())
    frame = _movement_move_long(state, frame, 'target_x', 0)
    while True:
        member = frame.scan.word()
        frame = first_replace(frame, scan=frame.scan.advance(2))
        frame = _movement_move(state, frame, 'target_y', member, 16)
        if frame.status & 8:
            break
        frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 255, 16)
        frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
        frame = _movement_arithmetic_long(state, frame, 'target_x', frame.controller.long(low16(frame.target_y)))
        frame = _movement_arithmetic_long(state, frame, 'target_x', 100)
    frame = _force_turn_divu_mask_fields(state, frame, 'target_x', 100, 0x22292)
    supply = frame.candidates.long()
    frame, remaining = _movement_binary_flags(state, frame, supply, frame.target_x, 32, True)
    frame.candidates.set_long(0, remaining)
    if not frame.status & 1:
        return frame
    frame.candidates.long()
    frame.candidates.set_long(0, 0)
    frame = _movement_test_long(state, frame, 0)
    return _force_turn_call_fields(state, frame, 0x222A8, 0x222A6)


def _force_loss_message_fields(state: SceneState, frame: FirstDeploymentFrame,
        player: int, message: int, continuation: int) -> FirstDeploymentFrame:
    """One saved F376 WORD plus original five LONGs; every restore consumes actual saved memory."""
    if (message, continuation) not in ((0xCA,0x22342), (0x142,0x223A2), (0x143,0x223C8)):
        raise ValueError('original supply-loss message phase required')
    value = state.read(0xFFFFF376, 2)
    stack = frame.stack_cursor.advance(-2)
    stack.set_word(0, value)
    frame = first_replace(frame, stack_cursor=stack)
    frame = _movement_test(state, frame, value, 16)
    saved = ('target_x','target_y','roster','controller','opponent')
    frame = _movement_save_longs(state, frame, saved)
    if message != 0xCA:
        player = state.read(player, 2)
    frame = _duel_menu_write_word_fields(state, frame, 0xFFFFF376, player)
    if message == 0xCA:
        frame = _duel_menu_write_word_fields(state, frame, 0xFFFFF3D0, low16(frame.unit))
    frame = _duel_menu_write_word_fields(state, frame, 0xFFFFF740, message)
    frame = _force_turn_call_fields(state, frame, 0x260E4, continuation)
    frame = _movement_restore_longs(state, frame, saved)
    restored = frame.stack_cursor.word()
    frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))
    return _duel_menu_write_word_fields(state, frame, 0xFFFFF376, restored)


def _force_loss_compact_member_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """The original self-relative MOVE advances A5 before its -4 destination, including negative sentinel."""
    frame = first_replace(frame, scratch=state.table_at(frame.roster.base))
    while True:
        value = frame.scratch.word()
        frame = first_replace(frame, scratch=state.table_at(u32(frame.scratch.base + 2)))
        frame = _settlement_store_word_fields(state, frame, frame.scratch, 0, value, displacement=-4)
        if frame.status & 8:
            break
    return first_replace(frame, roster=frame.roster.advance(-2))


def apply_force_supply_losses_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """222A8..223D6: sample once, decrement readiness, compact dead members or deduct original low-WORD troop percent."""
    frame = _resource_cost_frame(state, frame, 0x222A8)
    frame = _force_turn_call_fields(state, frame, 0x83D4, 0x222AE)
    frame = _movement_move_long(state, frame, 'target_x', 0)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF61C, 2), 16)
    frame = _movement_move_long(state, frame, 'target_y', frame.target_x)
    frame = _movement_move_long(state, frame, 'unit', frame.target_x)
    frame = _special_action_shift_long(state, frame, 'target_x', 1)
    frame = _movement_arithmetic_long(state, frame, 'target_x', frame.target_y)
    frame = _special_action_swap(state, frame, 'target_x')
    frame = _movement_add_word(state, frame, 'target_x', 3)
    frame = _movement_move_long(state, frame, 'target_y', frame.unit)
    frame = _special_action_shift_long(state, frame, 'target_y', 2)
    frame = _movement_arithmetic_long(state, frame, 'target_y', frame.unit)
    frame = _special_action_shift_long(state, frame, 'target_y', 1)
    frame = _movement_arithmetic_long(state, frame, 'target_y', frame.unit)
    frame = _special_action_swap(state, frame, 'target_y')
    frame = _movement_add_word(state, frame, 'target_y', 20)
    while True:
        member = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'unit', member, 16)
        if frame.status & 8:
            return frame
        frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 255, 16)
        frame = _movement_fixed_shift_word(state, frame, 'unit', 1)
        readiness = frame.opponent.word(low16(frame.unit))
        frame, value = _movement_binary_flags(state, frame, readiness, low16(frame.target_x), 16, True)
        frame.opponent.set_word(low16(frame.unit), value)
        if not frame.status & 5:
            frame = _movement_fixed_shift_word(state, frame, 'unit', 1)
            frame = _movement_move_long(state, frame, 'count', frame.controller.long(low16(frame.unit)))
            frame = _movement_multiply_word(state, frame, 'count', low16(frame.target_y))
            frame = _force_turn_divu_mask_fields(state, frame, 'count', 100, 0x22354)
            troops = frame.controller.long(low16(frame.unit))
            frame, value = _movement_binary_flags(state, frame, troops, frame.count, 32, True)
            frame.controller.set_long(low16(frame.unit), value)
            continue
        frame = _movement_fixed_shift_word(state, frame, 'unit', 1, True)
        frame = first_replace(frame, scratch=state.table_at(0xFFFFCC00))
        frame = _movement_move(state, frame, 'count', frame.scratch.byte(low16(frame.unit)), 8)
        frame = _settlement_write_byte_fields(state, frame, frame.scratch, 255, low16(frame.unit))
        frame = _force_loss_compact_member_fields(state, frame)
        frame = _movement_move(state, frame, 'count', low16(frame.count) & 63, 16)
        frame = first_replace(frame, scratch=state.table_at(0xFFFFF427))
        frame = _movement_move(state, frame, 'count', frame.scratch.byte(low16(frame.count)), 8)
        frame = _movement_move(state, frame, 'count', low16(frame.count) & 15, 16)
        for player in (0xFFFFF67A,0xFFFFF67C,0xFFFFF67E):
            frame = _movement_compare(state, frame, low16(frame.count), state.read(player, 2), 16)
            if frame.status & 4:
                break
        else:
            frame = first_replace(frame, candidates=state.table_at(0xFFFFF45E).cursor())
            frame = _movement_move(state, frame, 'count', state.read(0xFFFFF68A, 2), 16)
            frame = _movement_fixed_shift_word(state, frame, 'count', 1)
            frame = _movement_compare(state, frame, low16(frame.unit), frame.candidates.word(low16(frame.count)), 16)
            if frame.status & 4:
                frame = _force_loss_message_fields(state, frame, 0xFFFFF68C, 0x143, 0x223C8)
                continue
            frame = first_replace(frame, candidates=state.table_at(0xFFFFA027).cursor())
            frame = _movement_move(state, frame, 'count', state.read(0xFFFFF68A, 2), 16)
            frame = _movement_compare(state, frame, low8(frame.unit), frame.candidates.byte(low16(frame.count)), 8)
            if frame.status & 4:
                frame = _force_loss_message_fields(state, frame, 0xFFFFF68E, 0x142, 0x223A2)
            continue
        frame = _force_loss_message_fields(state, frame, low16(frame.count), 0xCA, 0x22342)


def check_battle_commanders_present_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """223D6..22418: actual WORD-then-BYTE secondary lookup and carry-only full-SR gate."""
    frame = _resource_cost_frame(state, frame, 0x223D6)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFCC00).cursor(), roster=state.table_at(0xFFFFA027).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF68A, 2), 16)
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(low16(frame.target_x)), 8)
    frame = _movement_compare(state, frame, frame.candidates.byte(low16(frame.target_y)), 255, 8)
    if frame.status & 4:
        state.sr |= 1
        return first_replace(frame, status=frame.status | 1)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF68A, 2), 16)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF45E).cursor())
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(low16(frame.target_x)), 8)
    frame = _movement_compare(state, frame, frame.candidates.byte(low16(frame.target_x)), 255, 8)
    carry = bool(frame.status & 4)
    state.sr = (state.sr & 65534) | int(carry)
    return first_replace(frame, status=(frame.status & 30) | int(carry))


def execute_secondary_force_orders_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """22418..22456: real second assignment, budget and live indexed orders with both saved address LONGs."""
    frame = _resource_cost_frame(state, frame, 0x22418)
    frame = _force_turn_call_fields(state, frame, 0x24B00, 0x2241C)
    frame = _force_turn_call_fields(state, frame, 0x22470, 0x22420)
    frame = first_replace(frame, roster=state.table_at(0xFFFFA5A4).cursor(), candidates=state.table_at(0xFFFFAF96).cursor())
    while True:
        member = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'choice', member, 16)
        if frame.status & 8:
            return _duel_menu_write_word_fields(state, frame, 0xFFFFF362, 0, clear=True)
        order = frame.candidates.word()
        frame = first_replace(frame, candidates=frame.candidates.advance(2))
        frame = _movement_move(state, frame, 'target_x', order, 16)
        frame = _movement_compare(state, frame, low16(frame.target_x), 255, 16)
        if frame.status & 4:
            continue
        frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
        relative = state.read(u32(0x22456 + s16(low16(frame.target_x))), 2)
        frame = _movement_move(state, frame, 'target_x', relative, 16)
        saved = ('roster','candidates')
        frame = _movement_save_longs(state, frame, saved)
        frame = first_replace(frame, roster=state.table_at(0x224DE).cursor())
        target = u32(frame.roster.base + s16(low16(frame.target_x)))
        frame = _force_turn_call_fields(state, frame, target, 0x2244A)
        frame = _movement_restore_longs(state, frame, saved)


def _force_budget_roster_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: str, destination: int, instruction: int) -> FirstDeploymentFrame:
    """The two true budget loops share one numeric core while preserving their distinct A0/A2 positions."""
    if (address, destination, instruction) not in (('roster',0xFFFFF768,0x2249E),('controller',0xFFFFF76C,0x224C8)):
        raise ValueError('original budget roster phase required')
    frame = _movement_move_long(state, frame, 'target_x', 0)
    while True:
        roster = getattr(frame, address)
        member = roster.word()
        advanced = state.table_at(u32(roster.base + 2))
        frame = first_replace(frame, **{address: advanced.cursor() if address == 'roster' else advanced})
        frame = _movement_move(state, frame, 'target_y', member, 16)
        if frame.status & 8:
            break
        frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
        frame = _movement_arithmetic_long(state, frame, 'target_x', frame.opponent.long(low16(frame.target_y)))
        frame = _movement_arithmetic_long(state, frame, 'target_x', 100)
    # Both DIVU flags are replaced by the subsequent MOVE/LSL/ADD/ANDI; overflow retains D0.
    if frame.target_x // 50 <= 65535:
        frame = _movement_divu_word(state, frame, 'target_x', 50, instruction)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
    frame = _movement_add_word(state, frame, 'target_x', low16(frame.target_y))
    frame = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)
    state.write(destination, 4, frame.target_x)
    return _movement_test_long(state, frame, frame.target_x)


def calculate_force_supply_budgets_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """22470..224DE: existing unique budget algorithm now retains actual complete A0/A2/A4 and final X."""
    frame = _resource_cost_frame(state, frame, 0x22470)
    frame = first_replace(frame, roster=state.table_at(0xFFFFA550).cursor(), controller=state.table_at(0xFFFFA5A4))
    from ..high_level_remaining_flows.business_city import _duel_menu_byte_bit_fields
    frame = _duel_menu_byte_bit_fields(state, frame, 0xFFFFF6D7, 1)
    if not frame.status & 4:
        first, second = frame.roster, frame.controller
        frame = first_replace(frame, roster=state.table_at(second.base).cursor(), controller=state.table_at(first.base))
    frame = first_replace(frame, opponent=state.table_at(0xFFFFC800))
    frame = _force_budget_roster_fields(state, frame, 'roster', 0xFFFFF768, 0x2249E)
    return _force_budget_roster_fields(state, frame, 'controller', 0xFFFFF76C, 0x224C8)


# Complete city project fields, shared steps and historical observer projections.
from .business_movement_support import _movement_compare_address


def _city_project_call_fields(state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int) -> FirstDeploymentFrame:
    """The real project BSR/JSR slot encloses only the one known current child algorithm."""
    frame = _resource_cost_frame(state, frame, target)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, uint(continuation, 32))
    entered = first_replace(frame, stack_cursor=stack)
    if target == 72106:
        result = settle_all_city_projects_fields(state, entered)
    elif target == 72144:
        result = settle_first_city_project_fields(state, entered)
    elif target == 72360:
        result = settle_second_city_project_fields(state, entered)
    elif target == 72646:
        result = settle_third_city_project_fields(state, entered)
    elif target == 72844:
        from .reuse_rules import award_defense_progress_fields
        result = award_defense_progress_fields(state, entered)
    elif target == 72906:
        from .reuse_rules import clear_completed_monthly_actions_fields
        result = clear_completed_monthly_actions_fields(state, entered)
    elif target == 33786:
        result = _city_project_save_fields(state, entered)
    else:
        result = execute_deployment_menu_fields(state, target, entered)
    result = _resource_cost_frame(state, result, target)
    actual = result.stack_cursor.long()
    if actual != continuation:
        from .business_movement_support import MovementContinuationBoundary
        raise MovementContinuationBoundary(actual, result, 'actual project child return LONG changed')
    return first_replace(result, stack_cursor=result.stack_cursor.advance(4))


def _city_project_begin_fields(state: SceneState, frame: FirstDeploymentFrame,
        table: int) -> tuple[FirstDeploymentFrame, str]:
    """Three order heads share their real index, sign-extending MOVEM.W and affiliation gate."""
    if table not in (0xFFFFE80C,0xFFFFE810,0xFFFFE814):
        raise ValueError('original project order table required')
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
    frame = _movement_add_word(state, frame, 'target_x', state.read(0xFFFFF364, 2))
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    frame = first_replace(frame, roster=state.table_at(table).cursor())
    officer = frame.roster.word(low16(frame.target_x))
    frame = first_replace(frame, unit=u32(s16(officer)))
    budget = frame.roster.word(low16(frame.target_x), 2)
    frame = first_replace(frame, count=u32(s16(budget)))
    frame = _movement_test(state, frame, low16(frame.unit), 16)
    if frame.status & 8:
        return frame, 'absent'
    frame = _movement_move(state, frame, 'distance', frame.auxiliary.byte(low16(frame.unit)), 8)
    frame = _movement_compare(state, frame, low8(frame.distance), state.read(0xFFFFF365, 1), 8)
    return frame, 'ready' if frame.status & 4 else 'cancel'


def _city_project_cancel_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Actual order WORD then task CLR.B, including the original fresh read for CLR."""
    frame = _settlement_store_word_fields(state, frame, frame.roster, low16(frame.target_x), 65535)
    return _settlement_write_byte_fields(state, frame, frame.scratch, value=0, offset=low16(frame.unit), clear=True)


def _city_project_pay_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """One live gold read and full SUB.L; insufficient funds do not debit the city."""
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFDFFC).cursor())
    frame = _movement_move_long(state, frame, 'distance', frame.candidates.long(low16(frame.target_y)))
    frame = _movement_arithmetic_long(state, frame, 'distance', frame.count, True)
    if not frame.status & 1:
        frame.candidates.set_long(low16(frame.target_y), frame.distance)
        frame = _movement_test_long(state, frame, frame.distance)
    return frame


def _city_project_divu_fields(state: SceneState, frame: FirstDeploymentFrame,
        carrier: str, divisor: int, instruction: int) -> FirstDeploymentFrame:
    """All six project DIVUs have their flags replaced immediately; overflow keeps original Dn."""
    if (carrier,divisor,instruction) not in (
            ('distance',5,0x11A12),('distance',1000,0x11A4A),
            ('distance',5,0x11AEA),('distance',60000,0x11B4C),
            ('count',50,0x11C0A),('count',1000,0x11C4A)):
        raise ValueError('original project division phase required')
    if frame.carrier(carrier) // divisor <= 65535:
        return _movement_divu_word(state, frame, carrier, divisor, instruction)
    return frame


def _city_project_aptitude_fields(state: SceneState, frame: FirstDeploymentFrame,
        division: int) -> FirstDeploymentFrame:
    """First and second projects share payment-derived effect plus intellect/2 in true live order."""
    if division not in (0x11A12,0x11AEA):
        raise ValueError('original first/second project aptitude phase required')
    frame = _movement_move_long(state, frame, 'distance', frame.count)
    frame = _city_project_divu_fields(state, frame, 'distance', 5, division)
    frame = _movement_move(state, frame, 'target_y', low16(frame.unit), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
    frame = first_replace(frame, roster=state.table_at(0xFFFFB600).cursor())
    frame = _movement_add_word(state, frame, 'distance', frame.roster.word(low16(frame.target_y)))
    frame = first_replace(frame, roster=state.table_at(0xFFFFBE00).cursor())
    frame = _movement_move(state, frame, 'target_y', frame.roster.word(low16(frame.target_y)), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1, True)
    return _movement_add_word(state, frame, 'distance', low16(frame.target_y))


def _city_project_intellect_reward_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Both reward tails use original LSL.L D2, WORD wrap, unsigned cap and the real BE00 work view."""
    frame = _special_action_shift_long(state, frame, 'unit', 1)
    frame = first_replace(frame, roster=state.table_at(0xFFFFBE00).cursor())
    frame = _movement_move(state, frame, 'target_x', frame.roster.word(low16(frame.unit)), 16)
    frame = _movement_add_word(state, frame, 'target_x', low16(frame.distance))
    frame = _movement_compare(state, frame, low16(frame.target_x), 999, 16)
    if not frame.status & 5:
        frame = _movement_move(state, frame, 'target_x', 999, 16)
    return _settlement_store_word_fields(state, frame, frame.roster, low16(frame.unit), low16(frame.target_x))


def settle_first_city_project_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """119D0..11AA8: first project payment, randomized city growth and intellect reward, with whole original cancellation tails."""
    frame = _resource_cost_frame(state, frame, 0x119D0)
    frame, phase = _city_project_begin_fields(state, frame, 0xFFFFE80C)
    if phase == 'absent':
        return frame
    if phase == 'cancel':
        return _city_project_cancel_fields(state, frame)
    frame = _city_project_pay_fields(state, frame)
    if frame.status & 1:
        return _city_project_cancel_fields(state, frame)
    frame = _city_project_aptitude_fields(state, frame, 0x11A12)
    frame = _city_project_call_fields(state, frame, 0x83D4, 0x11A34)
    frame = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)
    frame = _movement_move_long(state, frame, 'target_y', frame.target_x)
    frame = _special_action_shift_long(state, frame, 'target_x', 1)
    frame = _movement_arithmetic_long(state, frame, 'target_x', frame.target_y)
    frame = _special_action_shift_long(state, frame, 'target_x', 1)
    frame = _special_action_swap(state, frame, 'target_x')
    frame = _movement_add_word(state, frame, 'target_x', 10)
    frame = _movement_multiply_word(state, frame, 'distance', low16(frame.target_x))
    frame = _city_project_divu_fields(state, frame, 'distance', 1000, 0x11A4A)
    frame = _movement_move_long(state, frame, 'distance', u32(s16(low16(frame.distance))))
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
    frame = first_replace(frame, roster=state.table_at(0xFFFFE1DC).cursor())
    frame = _movement_move_long(state, frame, 'count', frame.roster.long(low16(frame.target_y)))
    frame = _movement_arithmetic_long(state, frame, 'count', frame.distance)
    frame = _movement_compare_address(state, frame, frame.count, 999)
    if not frame.status & 5:
        frame = _movement_move(state, frame, 'count', 999, 16)
    frame.roster.set_long(low16(frame.target_y), frame.count)
    frame = _movement_test_long(state, frame, frame.count)
    return _city_project_intellect_reward_fields(state, frame)


def settle_second_city_project_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """11AA8..11BC6: second project rate, split-word product, capped city effect and original trait reward."""
    frame = _resource_cost_frame(state, frame, 0x11AA8)
    frame, phase = _city_project_begin_fields(state, frame, 0xFFFFE810)
    if phase == 'absent':
        return frame
    if phase == 'cancel':
        return _city_project_cancel_fields(state, frame)
    frame = _city_project_pay_fields(state, frame)
    if frame.status & 1:
        return _city_project_cancel_fields(state, frame)
    frame = _city_project_aptitude_fields(state, frame, 0x11AEA)
    frame = _city_project_call_fields(state, frame, 0x83D4, 0x11B0C)
    frame = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)
    frame = _special_action_shift_long(state, frame, 'target_x', 2)
    frame = _special_action_swap(state, frame, 'target_x')
    frame = _movement_move(state, frame, 'offset_x', 8, 16)
    frame = _movement_move(state, frame, 'offset_y', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'offset_y', 2)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFE31C).cursor())
    frame = _movement_compare_address(state, frame, frame.candidates.long(low16(frame.offset_y)), 80)
    if not frame.status & 1:
        frame = _movement_move(state, frame, 'offset_x', 2, 16)
    frame = _movement_add_word(state, frame, 'target_x', low16(frame.offset_x))
    frame = _movement_multiply_word(state, frame, 'distance', low16(frame.target_x))
    frame = first_replace(frame, roster=state.table_at(0xFFFFC200).cursor())
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(low16(frame.unit)), 8)
    frame = _movement_move(state, frame, 'target_y', low16(frame.distance), 16)
    frame = _movement_multiply_word(state, frame, 'target_y', low16(frame.target_x))
    frame = _special_action_swap(state, frame, 'distance')
    frame = _movement_multiply_word(state, frame, 'distance', low16(frame.target_x))
    frame = _special_action_swap(state, frame, 'distance')
    frame = _movement_arithmetic_long(state, frame, 'distance', frame.target_y)
    frame = _city_project_divu_fields(state, frame, 'distance', 60000, 0x11B4C)
    frame = _movement_move_long(state, frame, 'distance', u32(s16(low16(frame.distance))))
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
    frame = first_replace(frame, roster=state.table_at(0xFFFFE31C).cursor())
    frame = _movement_move_long(state, frame, 'target_x', frame.roster.long(low16(frame.target_y)))
    frame = _movement_arithmetic_long(state, frame, 'target_x', frame.distance)
    frame = _movement_compare(state, frame, low16(frame.target_x), 100, 16)
    if not frame.status & 5:
        frame = _movement_move(state, frame, 'target_x', 100, 16)
    frame.roster.set_long(low16(frame.target_y), frame.target_x)
    frame = _movement_test_long(state, frame, frame.target_x)
    frame = _city_project_intellect_reward_fields(state, frame)
    frame = _movement_compare(state, frame, low16(frame.distance), 5, 16)
    if frame.status & 1:
        return frame
    frame = first_replace(frame, roster=state.table_at(0xFFFFC200).cursor())
    frame = _movement_fixed_shift_word(state, frame, 'unit', 1, True)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(low16(frame.unit)), 8)
    frame = _movement_add_word(state, frame, 'target_x', 1)
    frame = _movement_compare(state, frame, low16(frame.target_x), 100, 16)
    if not frame.status & 5:
        return frame
    return _settlement_write_byte_fields(state, frame, frame.roster, value=low8(frame.target_x), offset=low16(frame.unit))


def settle_third_city_project_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """11BC6..11C8C: third project budget*100, ability-weighted defense, original WORD cap and reward child."""
    frame = _resource_cost_frame(state, frame, 0x11BC6)
    frame, phase = _city_project_begin_fields(state, frame, 0xFFFFE814)
    if phase == 'absent':
        return frame
    if phase == 'cancel':
        return _city_project_cancel_fields(state, frame)
    frame = _movement_multiply_word(state, frame, 'count', 100)
    frame = _city_project_pay_fields(state, frame)
    if frame.status & 1:
        return _city_project_cancel_fields(state, frame)
    frame = _city_project_divu_fields(state, frame, 'count', 50, 0x11C0A)
    frame = _movement_move(state, frame, 'target_y', low16(frame.unit), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
    frame = first_replace(frame, roster=state.table_at(0xFFFFB600).cursor())
    frame = _movement_add_word(state, frame, 'count', frame.roster.word(low16(frame.target_y)))
    for address in (0xFFFFBE00,0xFFFFC000):
        frame = first_replace(frame, roster=state.table_at(address).cursor())
        frame = _movement_move(state, frame, 'distance', frame.roster.word(low16(frame.target_y)), 16)
        frame = _movement_fixed_shift_word(state, frame, 'distance', 2, True)
        frame = _movement_add_word(state, frame, 'count', low16(frame.distance))
    frame = _city_project_call_fields(state, frame, 0x83D4, 0x11C38)
    frame = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)
    frame = _movement_move_long(state, frame, 'target_y', frame.target_x)
    frame = _special_action_shift_long(state, frame, 'target_x', 1)
    frame = _movement_arithmetic_long(state, frame, 'target_x', frame.target_y)
    frame = _special_action_swap(state, frame, 'target_x')
    frame = _movement_add_word(state, frame, 'target_x', 6)
    frame = _movement_multiply_word(state, frame, 'count', low16(frame.target_x))
    frame = _city_project_divu_fields(state, frame, 'count', 1000, 0x11C4A)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    frame = first_replace(frame, roster=state.table_at(0xFFFFE59C).cursor())
    frame = _movement_move(state, frame, 'choice', frame.roster.word(low16(frame.target_x), 2), 16)
    frame = _movement_add_word(state, frame, 'choice', low16(frame.count))
    frame = _movement_compare(state, frame, low16(frame.choice), 100, 16)
    if not frame.status & 5:
        frame = _movement_move(state, frame, 'choice', 100, 16)
    frame = _settlement_store_word_fields(state, frame, frame.roster, low16(frame.target_x), low16(frame.choice), displacement=2)
    return _city_project_call_fields(state, frame, 0x11C8C, 0x11C72)


def settle_all_city_projects_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """119AA..119D0: exactly forty live cities, each consumes all three complete project cores."""
    frame = _resource_cost_frame(state, frame, 0x119AA)
    frame = _duel_menu_write_word_fields(state, frame, 0xFFFFF364, 0, clear=True)
    frame = first_replace(frame, auxiliary=state.table_at(0xFFFFCC00), scratch=state.table_at(0xFFFFCD00))
    while True:
        counter = state.read(0xFFFFF364, 2)
        frame, counter = _movement_binary_flags(state, frame, counter, 1, 16)
        state.write(0xFFFFF364, 2, counter)
        for target, continuation in ((0x119D0,0x119BE),(0x11AA8,0x119C2),(0x11BC6,0x119C6)):
            frame = _city_project_call_fields(state, frame, target, continuation)
        frame = _movement_compare(state, frame, state.read(0xFFFFF364, 2), 40, 16)
        if not frame.status & 1:
            return frame


def settle_city_projects_and_refresh_map_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1190E..119A4: whole project/cleanup/map upload and menu reset; unresolved devices keep true slots."""
    frame = _resource_cost_frame(state, frame, 0x1190E)
    frame = _city_project_call_fields(state, frame, 0x119AA, 0x11912)
    frame = _city_project_call_fields(state, frame, 0x11CCA, 0x11916)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFD300).cursor())
    frame = _movement_move(state, frame, 'count', 31, 16)
    while True:
        frame.candidates.set_long(0, 0x11111111)
        frame = first_replace(frame, candidates=frame.candidates.advance(4))
        frame = _movement_test_long(state, frame, 0x11111111)
        remaining = u16(low16(frame.count) - 1)
        frame = first_replace(frame, count=replace_word(frame.count, remaining))
        if remaining == 65535:
            break
    frame = first_replace(frame, roster=state.table_at(0x119A4).cursor())
    frame = _movement_move(state, frame, 'target_x', 1, 16)
    frame = _movement_move(state, frame, 'target_y', 3, 16)
    frame = _movement_move(state, frame, 'count', 2, 16)
    frame = _city_project_call_fields(state, frame, 0xAE8A, 0x11940)
    state.write(0xC00004, 4, 0x40200000)
    frame = _movement_test_long(state, frame, 0x40200000)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFD300).cursor())
    frame = _movement_move(state, frame, 'count', 127, 16)
    while True:
        value = frame.candidates.long()
        frame = first_replace(frame, candidates=frame.candidates.advance(4))
        state.write(0xC00000, 4, value)
        frame = _movement_test_long(state, frame, value)
        remaining = u16(low16(frame.count) - 1)
        frame = first_replace(frame, count=replace_word(frame.count, remaining))
        if remaining == 65535:
            break
    frame = _city_project_call_fields(state, frame, 0x55B0, 0x11962)
    frame = _duel_menu_write_word_fields(state, frame, 0xFFFFF362, 12)
    frame = _city_project_call_fields(state, frame, 0x30A74, 0x1196E)
    frame = _movement_test(state, frame, state.read(0xFFFFF386, 2), 16)
    if frame.status & 4:
        frame = _city_project_call_fields(state, frame, 0x83FA, 0x1197C)
    for address,value,clear in ((0xFFFFF612,0x208,False),(0xFFFFF362,19,False),
            (0xFFFFF36A,0,True),(0xFFFFF3C2,0x20A,False),(0xFFFFF3C4,0,True),(0xFFFFCEA0,0,True)):
        frame = _duel_menu_write_word_fields(state, frame, address, value, clear=clear)
    return _duel_menu_write_word_fields(state, frame, 0xFF3000, 65535)

def _city_project_legacy_entry_fields(state: SceneState, values: ProjectValues) -> FirstDeploymentFrame:
    """Only real historical ProjectValues fields are observed; other A/D/SP remain unknown."""
    checked_context(values, ProjectValues, state)
    return first_replace(FirstDeploymentFrame.unobserved(), target_x=values.city_index,
        target_y=values.record_index, unit=values.officer, count=values.budget,
        distance=values.value, offset_x=values.scale, offset_y=values.city_offset,
        choice=values.effect, roster=None if values.orders is None else values.orders.cursor(),
        scratch=values.task_flags, auxiliary=values.assignments, status=state.sr & 31)


def _city_project_legacy_result_fields(state: SceneState, frame: FirstDeploymentFrame) -> ProjectValues:
    """No CPU formula lives in this result projection; actual pointer roles match the historical API."""
    return ProjectValues(officer=frame.unit, budget=frame.count, value=frame.distance,
        scale=frame.offset_x, effect=frame.choice, city_index=frame.target_x,
        record_index=frame.target_y, city_offset=frame.offset_y,
        assignments=state.table_at(frame.auxiliary.base), task_flags=state.table_at(frame.scratch.base),
        orders=state.table_at(frame.roster.base)).validate(state)

# D49 complete current map presentation and assignment location cores.
from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
from ..high_level_gameplay_flow.business_services import refresh_gameplay_scene_fields
from ..high_level_player_commands.contexts_display import SpritePacketMemory
from ..high_level_player_commands.business_display import append_live_command_sprite_fields
from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
from ..high_level_battle_ai.business_actions import _deployment_terrain_lookup
from ..high_level_battle_ai.business_geometry import rounded_deployment_radial_distance_fields
from ..high_level_gameplay_flow.business_battle import _postbattle_bit_fields
from .business_movement_support import MovementContinuationBoundary, _movement_compare_address
from ..high_level_remaining_flows.business_city import _city_encounter_shift_word_fields
def _map_presentation_bit_fields(state: SceneState, frame: FirstDeploymentFrame,
        value: int, mask: int) -> FirstDeploymentFrame:
    frame = _postbattle_bit_fields(frame, bool(value & mask))
    state.sr = (state.sr & 65504) | frame.status
    return frame
def _map_presentation_arithmetic_fields(state: SceneState, frame: FirstDeploymentFrame,
        carrier: str, value: int, subtract: bool=False) -> FirstDeploymentFrame:
    frame, result = _movement_binary_flags(state, frame, low16(frame.carrier(carrier)), value, 16, subtract)
    return first_replace(frame, **{carrier: replace_word(frame.carrier(carrier), result)})
def _map_presentation_memory_arithmetic_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, amount: int) -> FirstDeploymentFrame:
    frame, value = _movement_binary_flags(state, frame, state.read(address, 2), amount, 16)
    state.write(address, 2, value)
    return frame
def _map_presentation_db_fields(frame: FirstDeploymentFrame, carrier: str) -> tuple:
    value = u16(low16(frame.carrier(carrier)) - 1)
    return first_replace(frame, **{carrier: replace_word(frame.carrier(carrier), value)}), value != 65535
def _map_presentation_emit_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, value: int, width: int, clear: bool=False) -> FirstDeploymentFrame:
    if width == 1:
        return _settlement_write_byte_fields(state, frame, state.table_at(address), value=value, clear=clear)
    if width == 2:
        return _duel_menu_write_word_fields(state, frame, address, value, clear=clear)
    if width != 4 or clear:
        raise ValueError('original map packet BYTE/WORD/LONG emission required')
    state.write(address, 4, value)
    return _movement_test_long(state, frame, value)
def _map_presentation_append_fields(state: SceneState, frame: FirstDeploymentFrame,
        carrier: str, value: int, width: int, clear: bool=False) -> FirstDeploymentFrame:
    view = frame.roster if carrier == 'roster' else frame.opponent
    frame = _map_presentation_emit_fields(state, frame, view.base, value, width, clear)
    return first_replace(frame, **{carrier: view.advance(width)})
def _map_presentation_tile_column_fields(state: SceneState, frame: FirstDeploymentFrame,
        gap: int, tiles: tuple) -> FirstDeploymentFrame:
    """Original high-row-first writes followed by the actual A0 postincrement."""
    for index in range(len(tiles) - 1, 0, -1):
        frame = _map_presentation_emit_fields(state, frame, u32(frame.roster.base + gap * index), tiles[index], 2)
    return _map_presentation_append_fields(state, frame, 'roster', tiles[0], 2)
def _map_presentation_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Physical known outer LONG; unknown children stop with that slot still live."""
    frame = _resource_cost_frame(state, frame, target)
    if target == 0x1A44E:
        returned, category = _deployment_terrain_lookup(BattlePolicyMemory(state), frame,
            low16(frame.target_y), low16(frame.unit), continuation=continuation)
        return returned
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    if target == 0x15E3E:
        returned = render_selected_map_packet_fields(state, entered)
    elif target == 0x15E88:
        returned = select_map_packet_sprite_fields(state, entered)
    elif target == 0x15ED0:
        returned = locate_map_packet_sprite_fields(state, entered)
    elif target == 0x15F1C:
        returned = render_map_marker_positions_fields(state, entered)
    elif target == 0x1613C:
        returned = append_two_row_sequential_tiles_fields(state, entered)
    elif target == 0x162FC:
        returned = append_four_row_tile_columns_fields(state, entered)
    elif target == 0x1636C:
        returned = append_missing_city_queue_packets_fields(state, entered)
    elif target == 0x16A04:
        returned = render_city_map_entry_fields(state, entered)
    elif target == 0x17B44:
        returned = append_nearby_target_candidates_fields(state, entered)
    elif target == 0x17B9A:
        returned = dispatch_target_eligibility_fields(state, entered)
    elif target == 0x14294:
        returned = _map_presentation_scaled_terrain_fields(state, entered)
    elif target == 0xAC10:
        returned = append_live_command_sprite_fields(SpritePacketMemory(state), entered,
            reset_scroll=False, initialize_clip=True)
    elif target == 0xAF48:
        returned = refresh_gameplay_scene_fields(SceneRefreshMemory(state), entered)
    elif target == 0x3080E:
        returned = rounded_deployment_radial_distance_fields(BattlePolicyMemory(state), entered)
    elif target in (0x1270A, 0x142A2):
        returned = execute_deployment_menu_fields(state, target, entered)
    elif target == 0x5ABC:
        from .business_commands import present_current_command_prompt_frame_fields
        returned = present_current_command_prompt_frame_fields(state, entered)
    else:
        raise MovementContinuationBoundary(target, entered, 'map presentation child lacks complete actual ABI')
    returned = _resource_cost_frame(state, returned, target)
    token = returned.stack_cursor.long()
    if token != continuation:
        raise MovementContinuationBoundary(token, returned, 'map presentation actual child return LONG changed')
    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))
def _map_presentation_scaled_terrain_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Existing14294 prefix/suffix projects the sole142A2 cell algorithm; zero new byte credit."""
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 4, True)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 4, True)
    frame = _map_presentation_call_fields(state, frame, 0x142A2, 0x1429C)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 4)
    return _movement_fixed_shift_word(state, frame, 'target_y', 4)
def render_visible_map_packets_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """15DE6: packed13+n stride, original strict viewport edges, then marker list."""
    frame = _resource_cost_frame(state, frame, 0x15DE6)
    frame = first_replace(frame, controller=state.table_at(0xFFFF9000).cursor())
    while True:
        frame = _movement_move(state, frame, 'distance', frame.controller.byte(), 8)
        if frame.status & 4:
            return _map_presentation_call_fields(state, frame, 0x15F1C, 0x15E3C)
        frame = _map_presentation_bit_fields(state, frame, frame.distance, 32)
        if frame.status & 4:
            visible = True
            for displacement, scroll, edge in ((1, 0xFFFFF314, 240), (2, 0xFFFFF318, 336)):
                frame = _movement_move(state, frame, 'offset_x', 0, 16)
                frame = _movement_move(state, frame, 'offset_x', frame.controller.byte(0, displacement), 8)
                frame = _movement_fixed_shift_word(state, frame, 'offset_x', 4)
                frame = _movement_add_word(state, frame, 'offset_x', 16)
                frame = _map_presentation_arithmetic_fields(state, frame, 'offset_x', state.read(scroll, 2), True)
                if frame.status & 1:
                    visible = False
                    break
                frame = _movement_compare(state, frame, low16(frame.offset_x), edge, 16)
                if not frame.status & 1:
                    visible = False
                    break
            if visible:
                frame = _map_presentation_call_fields(state, frame, 0x15E3E, 0x15E2A)
        frame = _movement_move(state, frame, 'offset_x', 0, 16)
        frame = _movement_move(state, frame, 'offset_x', frame.controller.byte(), 8)
        frame = _movement_move(state, frame, 'offset_x', low16(frame.offset_x) & 15, 16)
        frame = first_replace(frame, controller=frame.controller.advance(13 + s16(low16(frame.offset_x))))
def render_selected_map_packet_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _resource_cost_frame(state, frame, 0x15E3E)
    frame = _movement_compare(state, frame, state.read(0xFFFFF36C, 2), 2, 16)
    if frame.status & 4:
        frame = _movement_move(state, frame, 'target_x', frame.controller.byte(0, 4), 8)
        frame = _movement_compare(state, frame, low8(frame.target_x), state.read(0xFFFFF377, 1), 8)
        if frame.status & 4:
            frame = _movement_move(state, frame, 'target_x', frame.controller.byte(), 8)
            frame = _map_presentation_bit_fields(state, frame, frame.target_x, 16)
            if frame.status & 4:
                frame = _map_presentation_bit_fields(state, frame, state.read(0xFFFFF321, 1), 4)
                if not frame.status & 4:
                    return frame
    frame = _map_presentation_call_fields(state, frame, 0x15ED0, 0x15E64)
    frame = _map_presentation_call_fields(state, frame, 0x15E88, 0x15E68)
    frame = _movement_move(state, frame, 'unit', 0, 16)
    frame = _movement_test(state, frame, frame.controller.byte(), 8)
    if frame.status & 8:
        frame = _movement_move(state, frame, 'unit', 0x800, 16)
    frame = _duel_menu_write_word_fields(state, frame, 0xFFFFF60A, state.read(0xFFFFF314, 2))
    frame = _duel_menu_write_word_fields(state, frame, 0xFFFFF60E, state.read(0xFFFFF318, 2))
    return _map_presentation_call_fields(state, frame, 0xAC10, 0x15E86)
def select_map_packet_sprite_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _resource_cost_frame(state, frame, 0x15E88)
    frame = first_replace(frame, roster=state.table_at(0x15EB8).cursor())
    frame = _map_presentation_bit_fields(state, frame, state.read(0xFFFFF321, 1), 16)
    if not frame.status & 4:
        frame = first_replace(frame, roster=frame.roster.advance(8))
    saved = ('target_x', 'target_y', 'roster', 'controller')
    frame = _movement_save_longs(state, frame, saved)
    frame = _map_presentation_call_fields(state, frame, 0x14294, 0x15EA4)
    frame = _movement_restore_longs(state, frame, saved)
    frame = _movement_compare(state, frame, low16(frame.unit), 4, 16)
    if frame.status & 4:
        frame = first_replace(frame, roster=state.table_at(0x15EC8).cursor())
    return frame
def locate_map_packet_sprite_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _resource_cost_frame(state, frame, 0x15ED0)
    frame = _movement_compare(state, frame, state.read(0xFFFFF612, 2), 0x209, 16)
    selected = False
    if frame.status & 4:
        frame = _movement_compare(state, frame, state.read(0xFFFFF362, 2), 6, 16)
        if frame.status & 4:
            frame = _movement_move(state, frame, 'target_x', state.read(0xFF3BB4, 2), 16)
            frame = _movement_compare(state, frame, low8(frame.target_x), frame.controller.byte(0, 13), 8)
            selected = bool(frame.status & 4)
    if selected:
        frame = _movement_move(state, frame, 'target_x', state.read(0xFF3BB6, 2), 16)
        frame = _movement_add_word(state, frame, 'target_x', 8)
        frame = _movement_move(state, frame, 'target_y', state.read(0xFF3BB8, 2), 16)
    else:
        frame = _movement_move(state, frame, 'target_x', 0, 16)
        frame = _movement_move(state, frame, 'target_x', frame.controller.byte(0, 1), 8)
        frame = _movement_fixed_shift_word(state, frame, 'target_x', 4)
        frame = _movement_add_word(state, frame, 'target_x', 8)
        frame = _movement_move(state, frame, 'target_y', 0, 16)
        frame = _movement_move(state, frame, 'target_y', frame.controller.byte(0, 2), 8)
        frame = _movement_fixed_shift_word(state, frame, 'target_y', 4)
    return _movement_add_word(state, frame, 'target_y', 8)
def render_map_marker_positions_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _resource_cost_frame(state, frame, 0x15F1C)
    frame = first_replace(frame, candidates=state.table_at(0xFFFF9F00).cursor())
    while True:
        frame = _movement_move(state, frame, 'target_x', frame.candidates.word(), 16)
        frame = first_replace(frame, candidates=frame.candidates.advance(2))
        if frame.status & 8:
            return frame
        frame = _movement_move(state, frame, 'target_y', frame.candidates.word(), 16)
        frame = first_replace(frame, candidates=frame.candidates.advance(2))
        visible = True
        for carrier, scroll, edge in (('target_x', 0xFFFFF314, 240), ('target_y', 0xFFFFF318, 336)):
            frame = _movement_move(state, frame, 'unit', low16(frame.carrier(carrier)), 16)
            frame = _movement_add_word(state, frame, 'unit', 16)
            frame = _map_presentation_arithmetic_fields(state, frame, 'unit', state.read(scroll, 2), True)
            if frame.status & 1:
                visible = False
                break
            frame = _movement_compare(state, frame, low16(frame.unit), edge, 16)
            if not frame.status & 5:
                visible = False
                break
        if visible:
            frame = first_replace(frame, roster=state.table_at(0x15F6A).cursor())
            frame = _movement_move(state, frame, 'unit', 0, 16)
            frame = _duel_menu_write_word_fields(state, frame, 0xFFFFF60A, state.read(0xFFFFF314, 2))
            frame = _duel_menu_write_word_fields(state, frame, 0xFFFFF60E, state.read(0xFFFFF318, 2))
            frame = _map_presentation_call_fields(state, frame, 0xAC10, 0x15F66)
def append_two_row_sequential_tiles_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _resource_cost_frame(state, frame, 0x1613C)
    frame = _movement_move(state, frame, 'target_x', 3, 16)
    while True:
        frame = _map_presentation_emit_fields(state, frame, frame.roster.base, low16(frame.target_y), 2)
        frame = _movement_add_word(state, frame, 'target_y', 1)
        frame = _map_presentation_emit_fields(state, frame, u32(frame.roster.base + 32), low16(frame.target_y), 2)
        frame = _movement_add_word(state, frame, 'target_y', 1)
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame, again = _map_presentation_db_fields(frame, 'target_x')
        if not again:
            return frame
def append_city_currency_panel_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _resource_cost_frame(state, frame, 0x15F84)
    frame = first_replace(frame, roster=state.table_at(0xFFFFD100).cursor(state.read(0xFFFFF31A, 2)))
    for tiles in ((12, 12), (0xC0B4, 0xC234), (0xC380, 0xD380)):
        frame = _map_presentation_tile_column_fields(state, frame, 28, tiles)
    frame = _movement_move(state, frame, 'target_x', 9, 16)
    while True:
        frame = _map_presentation_tile_column_fields(state, frame, 28, (0xC381, 0xD381))
        frame, again = _map_presentation_db_fields(frame, 'target_x')
        if not again:
            break
    frame = _map_presentation_tile_column_fields(state, frame, 28, (0xCB80, 0xDB80))
    frame = first_replace(frame, roster=frame.roster.advance(28))
    for tiles in ((12, 12), (0xC134, 0xC1B4), (0xC382, 0xC382), (0xC005, 0xC006), (0xC007, 0xC008), (0xC001, 0xC001), (0xC001, 0xC001)):
        frame = _map_presentation_tile_column_fields(state, frame, 28, tiles)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF364, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFE09C).cursor())
    frame = _movement_move_long(state, frame, 'target_x', frame.candidates.long(low16(frame.target_x)))
    frame = _map_presentation_emit_fields(state, frame, 0xFFFFF3F8, frame.target_x, 4)
    frame = _movement_move(state, frame, 'target_y', 0xC386, 16)
    frame = _movement_move(state, frame, 'unit', 0xC001, 16)
    frame = first_replace(frame, auxiliary=state.table_at(0xFFFFD300).cursor())
    frame = _map_presentation_call_fields(state, frame, 0x1270A, 0x16034)
    frame = _movement_move(state, frame, 'target_x', 5, 16)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFD300).cursor())
    while True:
        value = frame.candidates.word()
        frame = first_replace(frame, candidates=frame.candidates.advance(2))
        frame = _map_presentation_emit_fields(state, frame, u32(frame.roster.base + 28), value, 2)
        frame = _map_presentation_append_fields(state, frame, 'roster', 0xC001, 2)
        frame, again = _map_presentation_db_fields(frame, 'target_x')
        if not again:
            break
    frame = _map_presentation_tile_column_fields(state, frame, 28, (0xCB82, 0xCB82))
    frame = _map_presentation_emit_fields(state, frame, u32(frame.roster.base + 28), 0, 2, True)
    return _map_presentation_memory_arithmetic_fields(state, frame, 0xFFFFF31A, 112)
def append_city_project_panel_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _resource_cost_frame(state, frame, 0x1605E)
    frame = first_replace(frame, roster=state.table_at(0xFFFFD100).cursor(state.read(0xFFFFF31A, 2)))
    for tiles in ((14, 14, 14, 14), (0xC49E, 0xC61E, 0xC69E, 0xC71E), (0xC380, 0xC382, 0xC382, 0xD380)):
        frame = _map_presentation_tile_column_fields(state, frame, 32, tiles)
    frame = _movement_move(state, frame, 'target_x', 11, 16)
    while True:
        frame = _map_presentation_tile_column_fields(state, frame, 32, (0xC381, 0xC001, 0xC001, 0xD381))
        frame, again = _map_presentation_db_fields(frame, 'target_x')
        if not again:
            break
    frame = _map_presentation_tile_column_fields(state, frame, 32, (0xCB80, 0xCB82, 0xCB82, 0xDB80))
    frame = first_replace(frame, roster=frame.roster.advance(96))
    for tiles in ((14, 14), (0xC51E, 0xC59E), (0xC382, 0xC382)):
        frame = _map_presentation_tile_column_fields(state, frame, 32, tiles)
    frame = _movement_move(state, frame, 'target_y', 0xC009, 16)
    frame = _map_presentation_call_fields(state, frame, 0x1613C, 0x16106)
    frame = _movement_move(state, frame, 'target_x', 3, 16)
    while True:
        frame = _map_presentation_tile_column_fields(state, frame, 32, (0xC001, 0xC001))
        frame, again = _map_presentation_db_fields(frame, 'target_x')
        if not again:
            break
    frame = _movement_move(state, frame, 'target_y', 0xC011, 16)
    frame = _map_presentation_call_fields(state, frame, 0x1613C, 0x16120)
    frame = _map_presentation_tile_column_fields(state, frame, 32, (0xCB82, 0xCB82))
    frame = _map_presentation_emit_fields(state, frame, u32(frame.roster.base + 32), 0, 2, True)
    frame = _map_presentation_memory_arithmetic_fields(state, frame, 0xFFFFF31A, 192)
    old = state.read(0xFFFFF3A5, 1)
    state.write(0xFFFFF3A5, 1, old | 32)
    return _map_presentation_bit_fields(state, frame, old, 32)
def append_current_city_value_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _resource_cost_frame(state, frame, 0x161D4)
    frame = first_replace(frame, roster=state.table_at(0xFFFFD100).cursor(state.read(0xFFFFF31A, 2)))
    for value in (3, 0xC5AA):
        frame = _map_presentation_append_fields(state, frame, 'roster', value, 2)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF670, 2), 16)
    frame = _movement_move(state, frame, 'target_y', 0xC386, 16)
    frame = _movement_move(state, frame, 'unit', 0, 16)
    frame = first_replace(frame, auxiliary=state.table_at(0xFFFFD300).cursor())
    frame = _map_presentation_call_fields(state, frame, 0x1270A, 0x161F8)
    frame = first_replace(frame, auxiliary=state.table_at(0xFFFFD306).cursor())
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move(state, frame, 'target_y', 2, 16)
    while True:
        frame = _movement_move(state, frame, 'unit', frame.auxiliary.word(), 16)
        frame = first_replace(frame, auxiliary=frame.auxiliary.advance(2))
        if frame.status & 4:
            frame = _movement_compare(state, frame, low16(frame.target_x), state.read(0xFFFFF39A, 2), 16)
            frame = _movement_move(state, frame, 'unit', 0xC001 if frame.status & 1 else 0xC386, 16)
        frame = _map_presentation_append_fields(state, frame, 'roster', low16(frame.unit), 2)
        frame = _movement_add_word(state, frame, 'target_x', 1)
        frame, again = _map_presentation_db_fields(frame, 'target_y')
        if not again:
            break
    frame = _map_presentation_emit_fields(state, frame, frame.roster.base, 0, 2, True)
    return _map_presentation_memory_arithmetic_fields(state, frame, 0xFFFFF31A, 10)
def append_selected_long_value_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _resource_cost_frame(state, frame, 0x1622E)
    frame = first_replace(frame, roster=state.table_at(0xFFFFD100).cursor(state.read(0xFFFFF31A, 2)))
    for value in (6, 0xC6AC):
        frame = _map_presentation_append_fields(state, frame, 'roster', value, 2)
    frame = _movement_move_long(state, frame, 'target_x', state.read(0xFFFFF3BA, 4))
    frame = _movement_move(state, frame, 'target_y', 0xC386, 16)
    frame = _movement_move(state, frame, 'unit', 0xC001, 16)
    frame = first_replace(frame, auxiliary=state.table_at(0xFFFFD300).cursor())
    frame = _map_presentation_call_fields(state, frame, 0x1270A, 0x16254)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFD300).cursor())
    frame = _movement_move(state, frame, 'target_x', 2, 16)
    while True:
        value = frame.candidates.long()
        frame = first_replace(frame, candidates=frame.candidates.advance(4))
        frame = _map_presentation_append_fields(state, frame, 'roster', value, 4)
        frame, again = _map_presentation_db_fields(frame, 'target_x')
        if not again:
            break
    frame = _map_presentation_emit_fields(state, frame, frame.roster.base, 0, 2, True)
    return _map_presentation_memory_arithmetic_fields(state, frame, 0xFFFFF31A, 16)
def append_four_row_tile_columns_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _resource_cost_frame(state, frame, 0x162FC)
    while True:
        frame = _map_presentation_emit_fields(state, frame, frame.roster.base, 0xC381, 2)
        frame = _map_presentation_emit_fields(state, frame, u32(frame.roster.base + 24), low16(frame.target_y), 2)
        frame = _movement_add_word(state, frame, 'target_y', 1)
        frame = _map_presentation_emit_fields(state, frame, u32(frame.roster.base + 48), low16(frame.target_y), 2)
        frame = _movement_add_word(state, frame, 'target_y', 1)
        frame = _map_presentation_emit_fields(state, frame, u32(frame.roster.base + 72), 0xD381, 2)
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame, again = _map_presentation_db_fields(frame, 'target_x')
        if not again:
            return frame
def append_four_row_status_panel_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _resource_cost_frame(state, frame, 0x1626C)
    frame = _map_presentation_call_fields(state, frame, 0x5ABC, 0x16272)
    frame = first_replace(frame, roster=state.table_at(0xFFFFD100).cursor(state.read(0xFFFFF31A, 2)))
    for tiles in ((10, 10, 10, 10), (0xC09C, 0xC11C, 0xC19C, 0xC21C), (0xC380, 0xC382, 0xC382, 0xD380)):
        frame = _map_presentation_tile_column_fields(state, frame, 24, tiles)
    for count, tile, token in ((5, 0xC00D, 0x162C8), (1, 0xC049, 0x162D4)):
        frame = _movement_move(state, frame, 'target_x', count, 16)
        frame = _movement_move(state, frame, 'target_y', tile, 16)
        frame = _map_presentation_call_fields(state, frame, 0x162FC, token)
    frame = _map_presentation_tile_column_fields(state, frame, 24, (0xCB80, 0xCB82, 0xCB82, 0xDB80))
    frame = _map_presentation_emit_fields(state, frame, u32(frame.roster.base + 72), 0, 2, True)
    frame = _duel_menu_write_word_fields(state, frame, 0xFFFFF3A4, state.read(0xFFFFF3A4, 2) | 0x9800)
    return _map_presentation_memory_arithmetic_fields(state, frame, 0xFFFFF31A, 96)
def append_missing_city_queue_packets_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1636C: actual packet delimiter scans, absent city records and six-byte append."""
    frame = _resource_cost_frame(state, frame, 0x1636C)
    frame = first_replace(frame, roster=state.table_at(0xFF3000).cursor(state.read(0xFF3826, 2)),
        candidates=state.table_at(0xFFFFEA38).cursor(), scan=state.table_at(0xFFFFE640).cursor())
    frame = _movement_move(state, frame, 'target_x', 39, 16)
    while True:
        frame = _movement_test(state, frame, frame.candidates.byte(low16(frame.target_x)), 8)
        if not frame.status & 4:
            frame = first_replace(frame, controller=state.table_at(0xFF3000).cursor())
            frame = _movement_move(state, frame, 'unit', low16(frame.target_x), 16)
            frame = _movement_add_word(state, frame, 'unit', 1)
            found = False
            while True:
                frame = _movement_move(state, frame, 'target_y', frame.controller.byte(), 8)
                frame = first_replace(frame, controller=frame.controller.advance(1))
                if frame.status & 8:
                    break
                for index in range(3):
                    frame = _movement_move(state, frame, 'target_y', frame.controller.byte(), 8)
                    frame = first_replace(frame, controller=frame.controller.advance(1))
                frame = _movement_compare(state, frame, low8(frame.target_y), 128, 8)
                if frame.status & 4:
                    value = frame.controller.byte()
                    frame = first_replace(frame, controller=frame.controller.advance(1))
                    frame = _movement_compare(state, frame, low8(frame.unit), value, 8)
                    if frame.status & 4:
                        found = True
                        break
                while True:
                    value = frame.controller.byte()
                    frame = first_replace(frame, controller=frame.controller.advance(1))
                    frame = _movement_test(state, frame, value, 8)
                    if frame.status & 4:
                        break
            if not found:
                frame = _map_presentation_append_fields(state, frame, 'roster', 0, 1, True)
                frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)
                frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
                frame = _map_presentation_append_fields(state, frame, 'roster', frame.scan.byte(low16(frame.target_y), 1), 1)
                for value in (1, 128, low8(frame.unit)):
                    frame = _map_presentation_append_fields(state, frame, 'roster', value, 1)
                frame = _map_presentation_append_fields(state, frame, 'roster', 0, 1, True)
                frame = _map_presentation_emit_fields(state, frame, frame.roster.base, 255, 1)
                frame = _map_presentation_memory_arithmetic_fields(state, frame, 0xFF3826, 6)
        frame, again = _map_presentation_db_fields(frame, 'target_x')
        if not again:
            return frame
def sort_map_packet_queue_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1631A: original descending insertion including strict BYTE sentinel ordering."""
    frame = _resource_cost_frame(state, frame, 0x1631A)
    frame = _map_presentation_call_fields(state, frame, 0x1636C, 0x1631E)
    frame = first_replace(frame, roster=state.table_at(0xFF3000).cursor())
    frame = _duel_menu_write_word_fields(state, frame, 0xFF39B2, 0, True)
    while True:
        value = frame.roster.byte()
        frame = first_replace(frame, roster=frame.roster.advance(1))
        frame = _movement_test(state, frame, value, 8)
        if frame.status & 8:
            return _duel_menu_write_word_fields(state, frame, 0xFF3BB2, 0, True)
        for carrier in ('target_x', 'target_y'):
            frame = _movement_move(state, frame, carrier, frame.roster.byte(), 8)
            frame = first_replace(frame, roster=frame.roster.advance(1))
        frame = first_replace(frame, candidates=state.table_at(0xFF39B2).cursor())
        while True:
            frame = _movement_compare(state, frame, low8(frame.target_y), frame.candidates.byte(), 8)
            if not frame.status & 5:
                break
            frame = first_replace(frame, candidates=frame.candidates.advance(2))
        frame = first_replace(frame, controller=state.table_at(frame.candidates.base).cursor())
        while True:
            frame = first_replace(frame, controller=frame.controller.advance(2))
            frame = _movement_test(state, frame, frame.controller.byte(), 8)
            if frame.status & 4:
                break
        frame = _map_presentation_emit_fields(state, frame, u32(frame.controller.base + 2), 0, 1, True)
        frame = first_replace(frame, scan=state.table_at(u32(frame.controller.base + 2)).cursor())
        while True:
            for index in range(2):
                frame = first_replace(frame, controller=frame.controller.advance(-1), scan=frame.scan.advance(-1))
                frame = _map_presentation_emit_fields(state, frame, frame.scan.base, frame.controller.byte(), 1)
            frame = _movement_compare_address(state, frame, frame.candidates.base, frame.controller.base)
            if not frame.status & 1:
                break
        frame = _map_presentation_emit_fields(state, frame, frame.candidates.base, low8(frame.target_y), 1)
        frame = _map_presentation_emit_fields(state, frame, u32(frame.candidates.base + 1), low8(frame.target_x), 1)
        while True:
            value = frame.roster.byte()
            frame = first_replace(frame, roster=frame.roster.advance(1))
            frame = _movement_test(state, frame, value, 8)
            if frame.status & 4:
                break
def render_city_map_entries_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _resource_cost_frame(state, frame, 0x169AA)
    frame = first_replace(frame, controller=state.table_at(0xFFFFCE9C).cursor())
    frame = _movement_move(state, frame, 'count', 39, 16)
    while True:
        frame = _movement_test(state, frame, frame.controller.byte(), 8)
        if not frame.status & 4:
            frame = _map_presentation_bit_fields(state, frame, frame.controller.byte(), 16)
            if frame.status & 4:
                visible = True
                for carrier, displacement, scroll, edge in (('target_x', 1, 0xFFFFF314, 240), ('target_y', 2, 0xFFFFF318, 336)):
                    frame = _movement_move(state, frame, carrier, 0, 16)
                    frame = _movement_move(state, frame, carrier, frame.controller.byte(0, displacement), 8)
                    frame = _movement_fixed_shift_word(state, frame, carrier, 4)
                    frame = _movement_move(state, frame, 'unit', low16(frame.carrier(carrier)), 16)
                    frame = _movement_add_word(state, frame, 'unit', 16)
                    frame = _map_presentation_arithmetic_fields(state, frame, 'unit', state.read(scroll, 2), True)
                    if frame.status & 1:
                        visible = False
                        break
                    frame = _movement_compare(state, frame, low16(frame.unit), edge, 16)
                    if not frame.status & 5:
                        visible = False
                        break
                if visible:
                    frame = _map_presentation_call_fields(state, frame, 0x16A04, 0x169FC)
        frame = first_replace(frame, controller=frame.controller.advance(-4))
        frame, again = _map_presentation_db_fields(frame, 'count')
        if not again:
            return frame
def render_city_map_entry_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _resource_cost_frame(state, frame, 0x16A04)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, frame.count)
    frame = _movement_test_long(state, first_replace(frame, stack_cursor=stack), frame.count)
    frame = _movement_compare(state, frame, state.read(0xFFFFF612, 2), 0x20A, 16)
    if frame.status & 4:
        frame = _movement_compare(state, frame, state.read(0xFFFFF362, 2), 2, 16)
        if frame.status & 4:
            frame = _movement_compare(state, frame, low16(frame.count), state.read(0xFFFFCEA0, 2), 16)
            if frame.status & 4:
                frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFCEA4, 2), 16)
                frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFCEA6, 2), 16)
    frame = first_replace(frame, roster=state.table_at(0x16A78).cursor())
    frame = _map_presentation_bit_fields(state, frame, state.read(0xFFFFF321, 1), 16)
    if frame.status & 4:
        frame = first_replace(frame, roster=frame.roster.advance(8))
    saved = ('target_x', 'target_y', 'roster', 'controller')
    frame = _movement_save_longs(state, frame, saved)
    frame = _movement_add_word(state, frame, 'target_x', 8)
    frame = _movement_add_word(state, frame, 'target_y', 8)
    frame = _map_presentation_call_fields(state, frame, 0x14294, 0x16A44)
    frame = _movement_restore_longs(state, frame, saved)
    frame = _movement_compare(state, frame, low16(frame.unit), 4, 16)
    if frame.status & 4:
        frame = first_replace(frame, roster=frame.roster.advance(16))
    frame = _movement_add_word(state, frame, 'target_y', 8)
    frame = _movement_move(state, frame, 'unit', 0, 16)
    frame = _movement_test(state, frame, frame.controller.byte(), 8)
    if frame.status & 8:
        frame = _movement_move(state, frame, 'unit', 0x800, 16)
    frame = _duel_menu_write_word_fields(state, frame, 0xFFFFF60A, state.read(0xFFFFF314, 2))
    frame = _duel_menu_write_word_fields(state, frame, 0xFFFFF60E, state.read(0xFFFFF318, 2))
    frame = _map_presentation_call_fields(state, frame, 0xAC10, 0x16A74)
    restored = frame.stack_cursor.long()
    frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(4))
    return _movement_move_long(state, frame, 'count', restored)
def build_nearby_battle_targets_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _resource_cost_frame(state, frame, 0x17A9E)
    state.set_status_word(0x2700)
    frame = first_replace(frame, status=0)
    frame = _duel_menu_write_word_fields(state, frame, 0xFFFFAF80, 0, True)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF3A6, 2), 16)
    frame = first_replace(frame, roster=state.table_at(0xFFFFC400).cursor())
    frame = _movement_move(state, frame, 'count', 0, 16)
    frame = _movement_move(state, frame, 'count', frame.roster.byte(low16(frame.target_x)), 8)
    frame = _movement_move(state, frame, 'offset_x', low16(frame.count), 16)
    frame = _movement_fixed_shift_word(state, frame, 'count', 3)
    frame = _movement_add_word(state, frame, 'count', low16(frame.offset_x))
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    frame = first_replace(frame, scan=state.table_at(0xFFFFA150).cursor())
    for carrier, displacement in (('offset_x', 0), ('offset_y', 2)):
        frame = _movement_move(state, frame, carrier, frame.scan.word(low16(frame.target_x), displacement), 16)
        frame = _city_encounter_shift_word_fields(state, frame, carrier, 7, True)
    frame = first_replace(frame, roster=state.table_at(0x945E8).cursor())
    frame = _movement_move(state, frame, 'distance', state.read(0xFFFFF68A, 2), 16)
    frame = _movement_multiply_word(state, frame, 'distance', 2240)
    frame = first_replace(frame, roster=frame.roster.advance(frame.distance), opponent=state.table_at(0xFFFFA62C).cursor())
    frame = _movement_compare(state, frame, state.read(0xFFFFF6D4, 2), 1, 16)
    skipped = False
    if frame.status & 4:
        frame = _movement_move(state, frame, 'target_y', low16(frame.offset_x), 16)
        frame = _movement_move(state, frame, 'unit', low16(frame.offset_y), 16)
        frame = _map_presentation_call_fields(state, frame, 0x1A44E, 0x17AF4)
        for terrain in (0, 4, 7):
            frame = _movement_compare(state, frame, low8(frame.target_x), terrain, 8)
            if frame.status & 4:
                break
        else:
            frame = _duel_menu_write_word_fields(state, frame, 0xFFFFAF80, 0x137)
            skipped = True
    if not skipped:
        frame = _map_presentation_bit_fields(state, frame, state.read(0xFFFFF6D7, 1), 2)
        frame = first_replace(frame, candidates=state.table_at(0xFFFFA5A4 if frame.status & 4 else 0xFFFFA550).cursor(),
            scratch=state.table_at(0xFF3BC2))
        frame = _map_presentation_call_fields(state, frame, 0x17B44, 0x17B36)
    frame = _map_presentation_emit_fields(state, frame, frame.opponent.base, 65535, 2)
    return _map_presentation_call_fields(state, frame, 0xAF48, 0x17B42)
def append_nearby_target_candidates_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _resource_cost_frame(state, frame, 0x17B44)
    while True:
        frame = _movement_move(state, frame, 'distance', frame.candidates.word(), 16)
        frame = first_replace(frame, candidates=frame.candidates.advance(2))
        if frame.status & 8:
            return frame
        frame = _movement_test(state, frame, frame.scratch.byte(low16(frame.distance)), 8)
        if not frame.status & 4:
            continue
        frame = _movement_move(state, frame, 'distance', low16(frame.distance) & 255, 16)
        frame = _movement_fixed_shift_word(state, frame, 'distance', 2)
        for carrier, displacement in (('target_y', 0), ('unit', 2)):
            frame = _movement_move(state, frame, carrier, frame.scan.word(low16(frame.distance), displacement), 16)
            frame = _city_encounter_shift_word_fields(state, frame, carrier, 7, True)
        frame = _movement_fixed_shift_word(state, frame, 'distance', 2, True)
        frame = _map_presentation_call_fields(state, frame, 0x17B9A, 0x17B68)
        if frame.status & 1:
            continue
        in_box = True
        for carrier, origin in (('target_y', frame.offset_x), ('unit', frame.offset_y)):
            frame = _map_presentation_arithmetic_fields(state, frame, carrier, low16(origin), True)
            if frame.status & 1:
                frame, value = _movement_binary_flags(state, frame, 0, low16(frame.carrier(carrier)), 16, True)
                frame = first_replace(frame, **{carrier: replace_word(frame.carrier(carrier), value)})
            frame = _movement_compare(state, frame, low16(frame.carrier(carrier)), low16(frame.count), 16)
            if not frame.status & 5:
                in_box = False
                break
            frame = _movement_multiply_word(state, frame, carrier, low16(frame.carrier(carrier)))
        if not in_box:
            continue
        frame = _movement_arithmetic_long(state, frame, 'target_y', frame.unit)
        frame = _movement_move_long(state, frame, 'target_x', frame.target_y)
        frame = _map_presentation_call_fields(state, frame, 0x3080E, 0x17B90)
        frame = _movement_compare(state, frame, low16(frame.target_x), low16(frame.count), 16)
        if frame.status & 5:
            frame = _map_presentation_append_fields(state, frame, 'opponent', low16(frame.distance), 2)
def select_active_battle_controller_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _resource_cost_frame(state, frame, 0x1A16E)
    frame = _movement_compare(state, frame, state.read(0xFFFFF612, 2), 0x407, 16)
    if frame.status & 4:
        frame = _movement_test(state, frame, state.read(0xFFFFF362, 2), 16)
        if frame.status & 4:
            return frame
        for phase in (2, 4):
            frame = _movement_compare(state, frame, state.read(0xFFFFF362, 2), phase, 16)
            if frame.status & 4:
                return frame
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF68C, 2), 16)
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF68E, 2), 16)
    frame = _map_presentation_bit_fields(state, frame, state.read(0xFFFFF6D7, 1), 2)
    if not frame.status & 4:
        frame = first_replace(frame, target_x=frame.target_y, target_y=frame.target_x)
    frame = _movement_compare(state, frame, low16(frame.target_x), state.read(0xFFFFF67A, 2), 16)
    if frame.status & 4:
        return frame
    frame = _movement_compare(state, frame, low16(frame.target_x), state.read(0xFFFFF67C, 2), 16)
    if frame.status & 4:
        return _duel_menu_write_word_fields(state, frame, 0xFFFFF602, state.read(0xFFFFF604, 2))
    frame = _movement_compare(state, frame, low16(frame.target_x), state.read(0xFFFFF67E, 2), 16)
    if frame.status & 4:
        frame = _movement_compare(state, frame, low16(frame.target_y), state.read(0xFFFFF67C, 2), 16)
    else:
        frame = _movement_compare(state, frame, low16(frame.target_y), state.read(0xFFFFF67A, 2), 16)
    if frame.status & 4:
        return frame
    return _duel_menu_write_word_fields(state, frame, 0xFFFFF602, state.read(0xFFFFF604, 2))

def _map_presentation_legacy_map_fields(state: SceneState, frame: MapPresentation) -> FirstDeploymentFrame:
    checked_context(frame, MapPresentation, state)
    return first_replace(FirstDeploymentFrame.unobserved(), target_x=frame.x,
        target_y=frame.y, unit=frame.attributes, count=frame.tile,
        distance=frame.officer, offset_x=frame.count, offset_y=frame.index,
        choice=frame.remaining, roster=frame.source, candidates=frame.destination,
        controller=frame.packet)
def _map_presentation_legacy_map_result(state: SceneState, frame: MapPresentation,
        returned: FirstDeploymentFrame) -> MapPresentation:
    return replace(frame, x=returned.target_x, y=returned.target_y,
        attributes=returned.unit, tile=returned.count, officer=returned.distance,
        count=returned.offset_x, index=returned.offset_y, remaining=returned.choice,
        source=None if returned.roster is None else returned.roster.cursor(),
        destination=None if returned.candidates is None else returned.candidates.cursor(),
        packet=None if returned.controller is None else returned.controller.cursor())
def _map_presentation_legacy_render_fields(state: SceneState, fields: RenderFields) -> FirstDeploymentFrame:
    checked_render_fields(fields, state)
    status = None
    if all(type(value) is bool for value in (fields.carry, fields.zero, fields.negative, fields.overflow)):
        status = (state.sr & 16) | int(fields.carry) | (2 if fields.overflow else 0) | (4 if fields.zero else 0) | (8 if fields.negative else 0)
    return first_replace(FirstDeploymentFrame.unobserved(), target_x=fields.x,
        target_y=fields.y, unit=fields.attributes, count=fields.tile,
        distance=fields.officer, offset_x=fields.count, offset_y=fields.index,
        choice=fields.remaining, roster=fields.source, candidates=fields.destination,
        controller=fields.packet, stack_cursor=fields.stack_cursor, status=status)
def _map_presentation_legacy_render_result(state: SceneState, fields: RenderFields,
        returned: FirstDeploymentFrame) -> RenderFields:
    return replace(fields, x=returned.target_x, y=returned.target_y,
        attributes=returned.unit, tile=returned.count, officer=returned.distance,
        count=returned.offset_x, index=returned.offset_y, remaining=returned.choice,
        source=returned.roster, destination=returned.candidates, packet=returned.controller,
        stack_cursor=returned.stack_cursor, carry=bool(returned.status & 1),
        overflow=bool(returned.status & 2), zero=bool(returned.status & 4), negative=bool(returned.status & 8))
def _map_presentation_legacy_search_fields(state: SceneState, search: TargetSearch) -> FirstDeploymentFrame:
    checked_context(search, TargetSearch, state)
    return first_replace(FirstDeploymentFrame.unobserved(), target_x=search.city,
        target_y=search.metric_x, unit=search.metric_y, count=search.count,
        distance=search.candidate, offset_x=search.origin_x, offset_y=search.origin_y,
        choice=search.limit, roster=search.terrain, candidates=search.source,
        controller=search.cities, scan=search.officers, opponent=search.destination,
        scratch=search.blocked, status=state.sr & 31)
def _map_presentation_legacy_search_result(state: SceneState, search: TargetSearch,
        returned: FirstDeploymentFrame) -> TargetSearch:
    return replace(search, city=returned.target_x, metric_x=returned.target_y,
        metric_y=returned.unit, count=returned.count, candidate=returned.distance,
        origin_x=returned.offset_x, origin_y=returned.offset_y, limit=returned.choice,
        terrain=returned.roster, source=None if returned.candidates is None else returned.candidates.cursor(),
        cities=returned.controller, officers=returned.scan,
        destination=None if returned.opponent is None else returned.opponent.cursor(), blocked=returned.scratch)

# D50 complete setup/controller and city-assignment owners.
from .business_movement_support import MovementContinuationBoundary
from ..high_level_player_commands.contexts_display import SpritePacketMemory
from ..high_level_player_commands.business_display import append_live_command_sprite_fields
from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
from ..high_level_gameplay_flow.business_services import (
    clear_video_sprite_plane_fields, initialize_video_registers_and_planes_fields,
    enqueue_sound_command_fields)
from ..high_level_scene_flows.business_scene import darken_palette_fields, _glyph_shift_long_fields
def _setup_write_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: Long, value: Long, width: int=2, clear: bool=False) -> FirstDeploymentFrame:
    """Actual MOVE/CLR memory effect, including the original CLR bus read."""
    if width not in (1,2,4) or type(clear) is not bool:
        raise ValueError('closed setup memory width required')
    value &= (1 << (width*8))-1
    if clear:
        state.read(address,width)
    state.write(address,width,value)
    return (_movement_test_long(state,frame,value) if width==4
        else _movement_test(state,frame,value,width*8))
def _setup_compare_memory_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: Long, source: Word, width: int=16) -> FirstDeploymentFrame:
    return _movement_compare(state,frame,state.read(address,width//8),source,width)
def _setup_change_word_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: Long, amount: Word, subtract: bool=False) -> FirstDeploymentFrame:
    frame,value=_movement_binary_flags(state,frame,state.read(address,2),amount,16,subtract)
    state.write(address,2,value)
    return frame
def _setup_asl_word_fields(state: SceneState, frame: FirstDeploymentFrame,
        carrier: str, amount: int) -> FirstDeploymentFrame:
    """Original option/plane ASL.W forms share the unique ordered addition flags."""
    if carrier not in ('target_x','target_y','unit','offset_x') or amount not in (1,2,8):
        raise ValueError('actual setup ASL.W role/count required')
    original=frame.carrier(carrier);value=low16(original);overflow=0
    for bit in range(amount):
        frame,value=_movement_binary_flags(state,frame,value,value,16)
        overflow |= frame.status & 2
    status=frame.status|overflow
    state.sr=(state.sr&65504)|status
    return first_replace(frame,status=status,**{carrier:replace_word(original,value)})
def _setup_coordinate_high_byte_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """ASR.W8 D0 of a packed coordinate, retaining the real C/X and upper LONG."""
    original=frame.target_x
    frame=_movement_fixed_shift_word(state,frame,'target_x',8,True)
    value=u16(s16(low16(original)) >> 8)
    status=(frame.status&17)|(8 if value&32768 else 0)|(4 if value==0 else 0)
    state.sr=(state.sr&65504)|status
    return first_replace(frame,target_x=replace_word(original,value),status=status)
def _setup_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: Long, continuation: Long) -> FirstDeploymentFrame:
    """One original CALL LONG, sole known child, and actual RTS read/pop."""
    frame=_resource_cost_frame(state,frame,target)
    stack=frame.stack_cursor.advance(-4);stack.set_long(0,continuation)
    entered=first_replace(frame,stack_cursor=stack)
    if target==0xAC08:
        result=append_live_command_sprite_fields(SpritePacketMemory(state),entered,
            reset_scroll=True,initialize_clip=True)
    elif target==0xDEA6:
        result=darken_palette_fields(SceneRefreshMemory(state),entered)
    elif target==0x68CE:
        result=clear_video_sprite_plane_fields(SceneRefreshMemory(state),entered)
    elif target==0x6826:
        result=initialize_video_registers_and_planes_fields(SceneRefreshMemory(state),entered)
    elif target==0x808A:
        result=enqueue_sound_command_fields(SceneRefreshMemory(state),entered)
    elif target==0x2B01A:
        result=cycle_setup_option_fields(state,entered)
    elif target==0x2AF8A:
        result=render_current_setup_option_fields(state,entered)
    elif target in (0x2B3C4,0x2B3D4,0x2B430):
        result=_setup_plane_rows_fields(state,entered,target)
    elif target==0x2B446:
        result=write_setup_video_address_fields(state,entered)
    elif target in (0x2AD5A,0x2AD88,0x2ADB8,0x2ADE8,0x2AE18,0x2AFB8,0x2AFE6,0x2B15E):
        children={0x2AD5A:update_first_setup_option_fields,0x2AD88:update_second_setup_option_fields,
            0x2ADB8:update_third_setup_option_fields,0x2ADE8:update_fourth_setup_option_fields,
            0x2AE18:update_setup_player_choices_fields,0x2AFB8:advance_setup_reveal_fields,
            0x2AFE6:advance_setup_dismissal_fields,0x2B15E:initialize_setup_video_fields}
        result=children[target](state,entered)
    else:
        from .business_scene_support import _controller_setup_child_fields
        result=_controller_setup_child_fields(state,entered,target)
    result=_resource_cost_frame(state,result,target)
    token=result.stack_cursor.long()
    if token!=continuation:
        raise MovementContinuationBoundary(token,result,'actual setup child return LONG changed')
    state.sr=(state.sr&65504)|result.status
    return first_replace(result,stack_cursor=result.stack_cursor.advance(4))
def _setup_update_option_fields(state: SceneState, frame: FirstDeploymentFrame,
        option: int, address: Long, maximum: Word, packet: Long,
        cycle_token: Long, render_token: Long) -> FirstDeploymentFrame:
    """Four original option gates share only their genuinely identical ordered tail."""
    valid=((0,0x00FF7026,2,0x2B084,0x2AD72,0x2AD84),
        (1,0x00FF7024,2,0x2B0B6,0x2ADA2,0x2ADB4),
        (2,0x00FF7028,1,0x2B0E8,0x2ADD2,0x2ADE4),
        (3,0x00FF702A,2,0x2B084,0x2AE02,0x2AE14))
    if (option,address,maximum,packet,cycle_token,render_token) not in valid:
        raise ValueError('closed actual four option tails required')
    frame=(_movement_test(state,frame,state.read(0x00FF7022,2),16) if option==0
        else _setup_compare_memory_fields(state,frame,0x00FF7022,option))
    if not frame.status&4:return frame
    frame=_movement_move(state,frame,'offset_x',state.read(address,2),16)
    frame=_movement_move(state,frame,'offset_y',maximum,16)
    frame=_setup_call_fields(state,frame,0x2B01A,cycle_token)
    frame=_setup_write_fields(state,frame,address,low16(frame.offset_x))
    frame=first_replace(frame,roster=state.table_at(packet).cursor())
    return _setup_call_fields(state,frame,0x2AF8A,render_token)
def update_first_setup_option_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x2AD5A)
    return _setup_update_option_fields(state,frame,0,0x00FF7026,2,0x2B084,0x2AD72,0x2AD84)
def update_second_setup_option_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x2AD88)
    return _setup_update_option_fields(state,frame,1,0x00FF7024,2,0x2B0B6,0x2ADA2,0x2ADB4)
def update_third_setup_option_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x2ADB8)
    return _setup_update_option_fields(state,frame,2,0x00FF7028,1,0x2B0E8,0x2ADD2,0x2ADE4)
def update_fourth_setup_option_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x2ADE8)
    return _setup_update_option_fields(state,frame,3,0x00FF702A,2,0x2B084,0x2AE02,0x2AE14)
def cycle_setup_option_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x2B01A)
    frame=_map_presentation_bit_fields(state,frame,state.read(0xFFFFF603,1),1)
    if not frame.status&4:
        frame=_movement_test(state,frame,low16(frame.offset_x),16)
        if frame.status&4:
            return _movement_move(state,frame,'offset_x',low16(frame.offset_y),16)
        frame=_map_presentation_arithmetic_fields(state,frame,'offset_x',1,True)
        if frame.status&4:return frame
    frame=_map_presentation_bit_fields(state,frame,state.read(0xFFFFF603,1),2)
    if frame.status&4:return frame
    frame=_movement_compare(state,frame,low16(frame.offset_x),low16(frame.offset_y),16)
    if frame.status&4:return _movement_move_long(state,frame,'offset_x',0)
    return _map_presentation_arithmetic_fields(state,frame,'offset_x',1)
def render_current_setup_option_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x2AF8A)
    frame=_movement_move(state,frame,'offset_x',state.read(0x00FF7022,2),16)
    frame=_movement_compare(state,frame,low16(frame.offset_x),5,16)
    if frame.status&4:
        # Original 2AF94/6720 reaches the same owner RTS at 2AFB6.
        return frame
    frame=_setup_asl_word_fields(state,frame,'offset_x',1)
    frame=first_replace(frame,candidates=state.table_at(0x2B050).cursor())
    frame=_movement_move(state,frame,'target_y',frame.candidates.word(low16(frame.offset_x)),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_y),16)
    frame=_setup_coordinate_high_byte_fields(state,frame)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&255,16)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_y)&255,16)
    frame=_movement_move_long(state,frame,'unit',0)
    return _setup_call_fields(state,frame,0xAC08,0x2AFB6)
def _setup_palette_transition_fields(state: SceneState, frame: FirstDeploymentFrame,
        counter: Long, packet: Long, token: Long, dismiss: bool) -> FirstDeploymentFrame:
    """The two actual palette transitions retain separate gates and live counters."""
    if (counter,packet,token,dismiss) not in ((0x00FF7040,0x2B46E,0x2AFDE,False),
        (0x00FF7042,0x2B46E,0x2B012,True)):
        raise ValueError('closed actual setup fade phases required')
    if dismiss:
        frame=_movement_test(state,frame,state.read(0x00FF703E,2),16)
        if frame.status&4:return frame
    frame=_setup_compare_memory_fields(state,frame,counter,16)
    if not frame.status&1:return frame
    if dismiss:
        frame=_movement_move(state,frame,'target_x',state.read(counter,2),16)
    else:
        frame=_movement_move(state,frame,'target_x',15,16)
        frame=_map_presentation_arithmetic_fields(state,frame,'target_x',state.read(counter,2),True)
    frame=_movement_move(state,frame,'target_y',64,16)
    frame=first_replace(frame,roster=state.table_at(packet).cursor())
    frame=_setup_call_fields(state,frame,0xDEA6,token)
    return _setup_change_word_fields(state,frame,counter,1)
def advance_setup_reveal_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x2AFB8)
    return _setup_palette_transition_fields(state,frame,0x00FF7040,0x2B46E,0x2AFDE,False)
def advance_setup_dismissal_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x2AFE6)
    return _setup_palette_transition_fields(state,frame,0x00FF7042,0x2B46E,0x2B012,True)
def update_setup_player_choices_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x2AE18)
    frame=_setup_compare_memory_fields(state,frame,0x00FF7022,5)
    fifth=bool(frame.status&4)
    if not fifth:
        frame=_setup_compare_memory_fields(state,frame,0x00FF7022,6)
    if fifth or frame.status&4:
        # Both real BEQs2AE20/2AE2C enter CLR.L D2 at2AEBC.
        render=True
    else:
        frame=_setup_compare_memory_fields(state,frame,0x00FF7022,4)
        if not frame.status&4:return frame
        frame=_map_presentation_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
        if not frame.status&4:
            frame=_movement_test(state,frame,state.read(0x00FF702C,2),16)
            if frame.status&4:
                frame=_setup_write_fields(state,frame,0x00FF702C,6)
                frame=_setup_compare_memory_fields(state,frame,0x00FF7026,2)
                if frame.status&4:frame=_setup_write_fields(state,frame,0x00FF702C,2)
            else:
                frame=_setup_change_word_fields(state,frame,0x00FF702C,1,True)
        else:
            frame=_map_presentation_bit_fields(state,frame,state.read(0xFFFFF603,1),8)
            if not frame.status&4:
                frame=_setup_compare_memory_fields(state,frame,0x00FF7026,2)
                if frame.status&1:
                    frame=_setup_compare_memory_fields(state,frame,0x00FF702C,6)
                    if frame.status&4:frame=_setup_write_fields(state,frame,0x00FF702C,0,clear=True)
                    else:frame=_setup_change_word_fields(state,frame,0x00FF702C,1)
                else:
                    frame=_setup_compare_memory_fields(state,frame,0x00FF702C,2)
                    if frame.status&4:frame=_setup_write_fields(state,frame,0x00FF702C,0,clear=True)
                    else:frame=_setup_change_word_fields(state,frame,0x00FF702C,1)
        render=True
    if render:
        frame=_movement_move_long(state,frame,'unit',0)
        frame=_movement_test(state,frame,state.read(0x00FF7026,2),16)
        if frame.status&4:address=0x2B05A
        else:
            frame=_setup_compare_memory_fields(state,frame,0x00FF7026,1)
            address=0x2B06A if frame.status&4 else 0x2B07A
        frame=first_replace(frame,scratch=state.table_at(address).cursor())
        while True:
            frame=_movement_move(state,frame,'target_x',frame.scratch.word(),16)
            frame=first_replace(frame,scratch=frame.scratch.advance(2))
            frame=_movement_compare(state,frame,low16(frame.target_x),65535,16)
            if frame.status&4:break
            frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
            frame=_setup_coordinate_high_byte_fields(state,frame)
            frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&255,16)
            frame=_movement_move(state,frame,'target_y',low16(frame.target_y)&255,16)
            frame=first_replace(frame,roster=state.table_at(0x2B10E).cursor())
            frame=_setup_call_fields(state,frame,0xAC08,0x2AF10)
    frame=_setup_compare_memory_fields(state,frame,0x00FF7026,2)
    if frame.status&1:
        frame=_movement_move(state,frame,'target_x',176,16)
        frame=_movement_move(state,frame,'target_y',256,16)
        frame=first_replace(frame,roster=state.table_at(0x2B10E).cursor())
        frame=_setup_call_fields(state,frame,0xAC08,0x2AF88)
        # The original BRA2AF88 rejoins2AF1E, not the option-count comparison.
    frame=_setup_compare_memory_fields(state,frame,0x00FF7022,6)
    if frame.status&4:
        frame=_movement_move(state,frame,'offset_x',state.read(0x00FF7030,2),16)
        frame=_setup_call_fields(state,frame,0x3051E,0x2AF34)
        frame=_setup_write_fields(state,frame,0x00FF7030,low16(frame.offset_x))
    frame=_setup_compare_memory_fields(state,frame,0x00FF7022,5)
    if frame.status&1:frame=_setup_write_fields(state,frame,0x00FF702E,0,clear=True)
    frame=_setup_compare_memory_fields(state,frame,0x00FF7022,5)
    if not frame.status&4:return frame
    frame=_movement_move(state,frame,'offset_x',state.read(0x00FF702E,2),16)
    frame=_setup_call_fields(state,frame,0x3049C,0x2AF64)
    frame=_setup_write_fields(state,frame,0x00FF702E,low16(frame.offset_x))
    return _setup_write_fields(state,frame,0x00FF7030,0,clear=True)
def write_setup_video_address_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x2B446)
    frame=_movement_save_longs(state,frame,('target_y',))
    frame=_movement_move_long(state,frame,'target_x',frame.target_x&65535)
    frame=_movement_move_long(state,frame,'target_y',frame.target_x)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&16383,16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)|16384,16)
    frame=_special_action_swap(state,frame,'target_x')
    frame=_movement_fixed_shift_word(state,frame,'target_y',8,True)
    frame=_city_encounter_shift_word_fields(state,frame,'target_y',6,True)
    frame=_movement_move_long(state,frame,'target_x',frame.target_x|frame.target_y)
    frame=_setup_write_fields(state,frame,0x00C00004,frame.target_x,4)
    return _movement_restore_longs(state,frame,('target_y',))
def _setup_advance_plane_row_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_map_presentation_arithmetic_fields(state,frame,'distance',1)
    frame=_movement_compare(state,frame,low8(frame.distance),32,8)
    if frame.status&1:return frame
    stride=frame.offset_x-4294967296 if frame.offset_x&2147483648 else frame.offset_x
    frame=first_replace(frame,candidates=frame.candidates.advance(stride))
    frame=_movement_move(state,frame,'target_x',low16(frame.candidates.base),16)
    frame=_setup_call_fields(state,frame,0x2B446,0x2B442)
    return _movement_move_long(state,frame,'distance',0)
def _setup_advance_plane_row_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        continuation: Long) -> FirstDeploymentFrame:
    if continuation not in (0x2B406,0x2B42A):raise ValueError('actual plane row tokens required')
    return _setup_call_fields(state,frame,0x2B430,continuation)
def _setup_plane_rows_fields(state: SceneState, frame: FirstDeploymentFrame,
        entry: Long) -> FirstDeploymentFrame:
    if entry not in (0x2B3C4,0x2B3D4,0x2B430):raise ValueError('actual plane entry required')
    frame=_resource_cost_frame(state,frame,entry)
    if entry==0x2B430:return _setup_advance_plane_row_fields(state,frame)
    if entry==0x2B3C4:
        frame=_setup_write_fields(state,frame,0x00FF7008,32768)
        frame=_setup_write_fields(state,frame,0x00FF700C,65535)
    frame=_setup_write_fields(state,frame,0x00C00004,36610)
    frame=_movement_move(state,frame,'target_x',low16(frame.candidates.base),16)
    frame=_setup_call_fields(state,frame,0x2B446,0x2B3E2)
    frame=_movement_move_long(state,frame,'distance',0)
    # One stream marker; both decoded-token paths retain it for the next token.
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(),8)
    frame=first_replace(frame,roster=frame.roster.advance(1))
    while True:
        frame=_movement_move(state,frame,'unit',frame.roster.byte(),8)
        frame=first_replace(frame,roster=frame.roster.advance(1))
        frame=_movement_compare(state,frame,low8(frame.target_y),low8(frame.unit),8)
        if frame.status&4:
            frame=_movement_move_long(state,frame,'count',0)
            frame=_movement_move(state,frame,'count',frame.roster.byte(),8)
            frame=first_replace(frame,roster=frame.roster.advance(1))
            if frame.status&4:return frame
            frame=_movement_move(state,frame,'unit',frame.roster.byte(),8)
            frame=first_replace(frame,roster=frame.roster.advance(1))
            frame=_setup_asl_word_fields(state,frame,'unit',8)
            frame=_movement_move(state,frame,'unit',frame.roster.byte(),8)
            frame=first_replace(frame,roster=frame.roster.advance(1))
            while True:
                # Repeated output observes the live attribute and mask again.
                frame=_movement_move(state,frame,'unit',low16(frame.unit)|state.read(0x00FF7008,2),16)
                frame=_movement_move(state,frame,'unit',low16(frame.unit)&state.read(0x00FF700C,2),16)
                frame=_setup_write_fields(state,frame,0x00C00000,low16(frame.unit))
                frame=_setup_advance_plane_row_call_fields(state,frame,0x2B42A)
                frame,again=_map_presentation_db_fields(frame,'count')
                if not again:break
        else:
            frame=_setup_asl_word_fields(state,frame,'unit',8)
            frame=_movement_move(state,frame,'unit',frame.roster.byte(),8)
            frame=first_replace(frame,roster=frame.roster.advance(1))
            frame=_movement_move(state,frame,'unit',low16(frame.unit)|state.read(0x00FF7008,2),16)
            frame=_movement_move(state,frame,'unit',low16(frame.unit)&state.read(0x00FF700C,2),16)
            frame=_setup_write_fields(state,frame,0x00C00000,low16(frame.unit))
            frame=_setup_advance_plane_row_call_fields(state,frame,0x2B406)
def decode_setup_plane_rows_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _setup_plane_rows_fields(state,frame,0x2B3C4)
def decode_setup_plane_rows_with_masks_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _setup_plane_rows_fields(state,frame,0x2B3D4)
def advance_setup_plane_row_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _setup_plane_rows_fields(state,frame,0x2B430)
def _setup_transfer_longs_fields(state: SceneState, frame: FirstDeploymentFrame,
        destination_carrier: str, increment_destination: bool) -> FirstDeploymentFrame:
    """The two exact image uploads and final palette copy retain original DBRA WORD."""
    if destination_carrier not in ('auxiliary','candidates') or type(increment_destination) is not bool:
        raise ValueError('actual setup LONG transfer destination required')
    while True:
        value=frame.roster.long();frame=first_replace(frame,roster=frame.roster.advance(4))
        destination=frame.auxiliary if destination_carrier=='auxiliary' else frame.candidates
        frame=_setup_write_fields(state,frame,destination.base,value,4)
        if increment_destination:frame=first_replace(frame,**{destination_carrier:destination.advance(4)})
        frame,again=_map_presentation_db_fields(frame,'target_x')
        if not again:return frame
def initialize_setup_video_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x2B15E)
    for register in (0x8238,0x833C,0x8406,0x857E,0x8F02,0x8C81,0x9001,0x9100,0x9200):
        frame=_setup_write_fields(state,frame,0x00C00004,register)
    for address in (0xFFFFF312,0xFFFFF314,0xFFFFF316,0xFFFFF318):
        frame=_setup_write_fields(state,frame,address,0)
    for command,pattern in ((0x40200000,0x11111111),(0x50000000,0x22222222)):
        frame=_setup_write_fields(state,frame,0x00C00004,command,4)
        frame=first_replace(frame,auxiliary=state.table_at(0x00C00000))
        frame=_movement_move_long(state,frame,'unit',pattern)
        frame=_movement_move(state,frame,'target_x',63,16)
        while True:
            frame=_setup_write_fields(state,frame,frame.auxiliary.base,frame.unit,4)
            frame,again=_map_presentation_db_fields(frame,'target_x')
            if not again:break
    frame=_setup_write_fields(state,frame,0x00C00004,0x60000001,4)
    frame=first_replace(frame,roster=state.table_at(0x2B4EE).cursor())
    frame=_movement_move_long(state,frame,'target_x',2047)
    frame=_setup_transfer_longs_fields(state,frame,'auxiliary',False)
    frame=_setup_write_fields(state,frame,0x00C00004,0x40000002,4)
    frame=first_replace(frame,roster=state.table_at(0x2D4EE).cursor())
    frame=_movement_move_long(state,frame,'target_x',2047)
    frame=_setup_transfer_longs_fields(state,frame,'auxiliary',False)
    frame=_movement_test(state,frame,state.read(0x00FF7036,2),16)
    if frame.status&4:
        source_a,source_b,token_a,token_b=0x2F4EE,0x2FA03,0x2B256,0x2B26C
    else:
        source_a,source_b,token_a,token_b=0x2FB8E,0x2FDEF,0x2B286,0x2B29C
    frame=first_replace(frame,roster=state.table_at(source_a).cursor(),candidates=state.table_at(0xE000).cursor())
    frame=_movement_move_long(state,frame,'offset_x',128)
    frame=_setup_call_fields(state,frame,0x2B3C4,token_a)
    frame=first_replace(frame,roster=state.table_at(source_b).cursor(),candidates=state.table_at(0xE040).cursor())
    frame=_movement_move_long(state,frame,'offset_x',128)
    frame=_setup_call_fields(state,frame,0x2B3C4,token_b)
    for source,destination,token in ((0x2FF1A,0xC000,0x2B2C2),(0x2FFB9,0xC040,0x2B2E8)):
        frame=first_replace(frame,roster=state.table_at(source).cursor(),candidates=state.table_at(destination).cursor())
        frame=_movement_move_long(state,frame,'offset_x',128)
        frame=_setup_write_fields(state,frame,0x00FF7008,0)
        frame=_setup_write_fields(state,frame,0x00FF700C,65535)
        frame=_setup_call_fields(state,frame,0x2B3D4,token)
    frame=first_replace(frame,roster=state.table_at(0x2B46E).cursor(),candidates=state.table_at(0xFFFFFB00).cursor())
    frame=_movement_move(state,frame,'target_x',31,16)
    return _setup_transfer_longs_fields(state,frame,'candidates',True)

def _setup_legacy_entry_fields(state: SceneState, values: SetupValues) -> FirstDeploymentFrame:
    checked_context(values,SetupValues,state)
    return first_replace(FirstDeploymentFrame.unobserved(),target_x=values.value,
        target_y=values.option,unit=values.position,count=values.attributes,
        distance=values.rows,offset_x=values.tile,offset_y=values.stride,
        choice=values.selector,roster=values.source,candidates=values.destination,
        status=state.sr&31)
def _setup_legacy_result_fields(state: SceneState, values: SetupValues,
        frame: FirstDeploymentFrame) -> SetupValues:
    return replace(values,value=frame.target_x,option=frame.target_y,
        position=frame.unit,attributes=frame.count,rows=frame.distance,
        tile=frame.offset_x,stride=frame.offset_y,selector=frame.choice,
        source=frame.roster,destination=frame.candidates)
def _setup_plane_legacy_entry_fields(state: SceneState, plane: SetupPlane) -> FirstDeploymentFrame:
    checked_context(plane,SetupPlane,state)
    return first_replace(FirstDeploymentFrame.unobserved(),target_x=plane.command,
        target_y=plane.marker,unit=plane.tile,count=plane.repeat_count,
        distance=plane.column,offset_x=plane.row_stride,roster=plane.source,
        candidates=state.table_at(plane.video_address.carrier).cursor(),status=state.sr&31)
def _setup_plane_legacy_result_fields(state: SceneState, plane: SetupPlane,
        frame: FirstDeploymentFrame) -> SetupPlane:
    return replace(plane,command=frame.target_x,marker=frame.target_y,tile=frame.unit,
        repeat_count=frame.count,column=frame.distance,row_stride=frame.offset_x,
        source=frame.roster,video_address=VideoPlaneAddress(frame.candidates.base))

# D51 complete gameplay text/direction and auxiliary object presentation.
from ..high_level_scene_flows.business_scene import decode_glyph_rows_to_buffers_fields
from .business_movement_support import _movement_fixed_shift_word, _movement_save_longs, _movement_restore_longs
def _game_text_call_fields(state: SceneState, frame: FirstDeploymentFrame, target: Long, continuation: Long) -> FirstDeploymentFrame:
    """One real caller LONG. Known children share their existing sole algorithm."""
    frame = _resource_cost_frame(state, frame, target)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    if target == 81474:
        from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_130_fields
        result = lowbank_coordinate_live_state_130_fields(state, entered)
    elif target in (0x17BBE, 0x17BF0, 0x17C1A, 0x17C36, 0x17C3C, 0x17C56):
        result = execute_deployment_menu_fields(state, target, entered)
    elif target == 44682:
        result = decode_glyph_rows_to_buffers_fields(SceneRefreshMemory(state), entered)
    elif target == 44872:
        result = refresh_gameplay_scene_fields(SceneRefreshMemory(state), entered)
    elif target == 44072:
        result = append_live_command_sprite_fields(SpritePacketMemory(state), entered, reset_scroll=False, initialize_clip=False)
    elif target == 118660:
        result = cycle_available_direction_fields(state, entered)
    elif target == 118726:
        result = render_direction_choice_fields(state, entered)
    elif target in (91768, 91976, 92056, 92824):
        result = execute_deployment_menu_fields(state, target, entered)
    elif target == 49334:
        from .business_commands import open_roster_selection_message_frame_fields
        result = open_roster_selection_message_frame_fields(state, entered)
    elif target == 81274:
        from ..high_level_remaining_flows.business_lowbank import lowbank_process_counted_records_39_fields
        result = lowbank_process_counted_records_39_fields(state, entered)
    elif target in (82000, 82958, 83850, 84844, 85592, 88602, 88672, 88950, 88958, 89114, 89214, 89284, 89488, 89510, 89552):
        result = execute_deployment_menu_fields(state, target, entered)
    else:
        raise MovementContinuationBoundary(target, entered, 'gameplay text child lacks a complete admitted frame')
    result = _resource_cost_frame(state, result, target)
    token = result.stack_cursor.long()
    if token != continuation:
        raise MovementContinuationBoundary(token, result, 'gameplay text RTS slot changed')
    state.sr = state.sr & 65504 | result.status
    return first_replace(result, stack_cursor=result.stack_cursor.advance(4))
def _game_text_upload_longs_fields(state: SceneState, frame: FirstDeploymentFrame,
        carrier: str) -> FirstDeploymentFrame:
    """Inclusive original DBRA, ordered source LONG read and real VDP write."""
    while True:
        value=frame.candidates.long()
        frame=first_replace(frame,candidates=frame.candidates.advance(4))
        frame=_setup_write_fields(state,frame,0xC00000,value,4)
        frame,again=_map_presentation_db_fields(frame,carrier)
        if not again:return frame
def _game_text_fill_longs_fields(state: SceneState, frame: FirstDeploymentFrame,
        carrier: str) -> FirstDeploymentFrame:
    while True:
        frame=_setup_write_fields(state,frame,frame.candidates.base,0x11111111,4)
        frame=first_replace(frame,candidates=frame.candidates.advance(4))
        frame,again=_map_presentation_db_fields(frame,carrier)
        if not again:return frame
def _game_text_indexed_dispatch_fields(state: SceneState, frame: FirstDeploymentFrame,
        table: Long, target_base: Long, token: Long) -> FirstDeploymentFrame:
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF362,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=_movement_move(state,frame,'target_x',state.table_at(table).word(low16(frame.target_x)),16)
    return _game_text_call_fields(state,frame,u32(target_base+s16(low16(frame.target_x))),token)
def dispatch_gameplay_command_state_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x13D48)
    return _game_text_indexed_dispatch_fields(state,frame,0x13D58,0x13D7A,0x13D56)
def dispatch_queue_command_state_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x16660)
    return _game_text_indexed_dispatch_fields(state,frame,0x16670,0x16678,0x1666E)
def upload_selected_queue_officer_name_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """165D8: queue officer lookup, font decode and two distinct text strips."""
    frame=_resource_cost_frame(state,frame,0x165D8)
    frame=_movement_move(state,frame,'target_x',1,16)
    frame=_movement_move(state,frame,'target_y',3,16)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor(),
        roster=state.table_at(state.read(0x00FF382C,4)).cursor())
    frame=_movement_move(state,frame,'distance',0,16)
    frame=_movement_move(state,frame,'distance',frame.roster.byte(4),8)
    frame=_movement_fixed_shift_word(state,frame,'distance',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'distance',frame.roster.word(low16(frame.distance)),16)
    frame=_movement_move(state,frame,'offset_x',low16(frame.distance),16)
    frame=_movement_fixed_shift_word(state,frame,'distance',1)
    frame=_map_presentation_arithmetic_fields(state,frame,'distance',low16(frame.offset_x))
    frame=_movement_fixed_shift_word(state,frame,'distance',1)
    frame=first_replace(frame,roster=state.table_at(u32(0x8A504+s16(low16(frame.distance)))).cursor())
    frame=_movement_move(state,frame,'count',2,16)
    frame=_game_text_call_fields(state,frame,0xAE8A,0x16614)
    frame=_setup_write_fields(state,frame,0xC00004,0x41A00000,4)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'count',95,16)
    frame=_game_text_upload_longs_fields(state,frame,'count')
    frame=first_replace(frame,roster=state.table_at(0x1665E).cursor(),candidates=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'count',0,16)
    frame=_game_text_call_fields(state,frame,0xAE8A,0x16640)
    frame=_setup_write_fields(state,frame,0xC00004,0x49200000,4)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'count',31,16)
    return _game_text_upload_longs_fields(state,frame,'count')
def _game_text_battle_prompt_fields(state: SceneState, frame: FirstDeploymentFrame,
        second: bool) -> FirstDeploymentFrame:
    if type(second) is not bool:raise ValueError('actual first/second prompt role required')
    state.sr=0x2700;frame=first_replace(frame,status=0)
    frame=first_replace(frame,roster=state.table_at(0x6C0C6 if second else 0x6C0AE).cursor(),
        candidates=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'target_x',1,16)
    frame=_movement_move(state,frame,'target_y',3,16)
    frame=_movement_move(state,frame,'count',11,16)
    frame=_game_text_call_fields(state,frame,0xAE8A,0x17A7A if second else 0x17A36)
    frame=_setup_write_fields(state,frame,0xC00004,0x40A00002,4)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'count',383,16)
    frame=_game_text_upload_longs_fields(state,frame,'count')
    return _game_text_call_fields(state,frame,0xAF48,0x17A9C if second else 0x17A58)
def upload_first_battle_prompt_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _game_text_battle_prompt_fields(state,_resource_cost_frame(state,frame,0x17A16),False)
def upload_second_battle_prompt_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _game_text_battle_prompt_fields(state,_resource_cost_frame(state,frame,0x17A5A),True)
def dispatch_target_eligibility_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x17B9A)
    frame=_movement_save_longs(state,frame,('offset_x','offset_y'))
    frame=_movement_move(state,frame,'choice',state.read(0xFFFFF6D4,2),16)
    frame=_movement_fixed_shift_word(state,frame,'choice',1)
    frame=_movement_move(state,frame,'choice',state.table_at(0x17BB2).word(low16(frame.choice)),16)
    frame=_game_text_call_fields(state,frame,u32(0x17BF0+s16(low16(frame.choice))),0x17BAC)
    return _movement_restore_longs(state,frame,('offset_x','offset_y'))
def upload_battle_action_prompt_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x17EDE)
    frame=first_replace(frame,roster=state.table_at(0x6C0DE).cursor(),candidates=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'target_x',1,16)
    frame=_movement_move(state,frame,'target_y',3,16)
    frame=_movement_move(state,frame,'count',4,16)
    frame=_game_text_call_fields(state,frame,0xAE8A,0x17EFA)
    frame=_setup_write_fields(state,frame,0xC00004,0x40A00002,4)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'count',159,16)
    return _game_text_upload_longs_fields(state,frame,'count')
def upload_battle_result_prompt_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x1874A)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'target_x',31,16)
    frame=_game_text_fill_longs_fields(state,frame,'target_x')
    frame=_movement_move(state,frame,'target_x',1,16)
    frame=_movement_move(state,frame,'target_y',3,16)
    frame=_movement_move(state,frame,'count',5,16)
    frame=first_replace(frame,roster=state.table_at(0x6C168).cursor())
    frame=_game_text_call_fields(state,frame,0xAE8A,0x18774)
    frame=_setup_write_fields(state,frame,0xC00004,0x40200002,4)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'count',223,16)
    return _game_text_upload_longs_fields(state,frame,'count')
def upload_selected_officer_names_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """18792: up to five names; the first negative entry fills the remaining strip."""
    frame=_resource_cost_frame(state,frame,0x18792)
    frame=first_replace(frame,auxiliary=state.table_at(0xFFFFAF56).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF658,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=first_replace(frame,auxiliary=frame.auxiliary.advance(s16(low16(frame.target_x))))
    frame=_movement_move(state,frame,'target_x',1,16)
    frame=_setup_write_fields(state,frame,0xC00004,0x40A00002,4)
    frame=_movement_move(state,frame,'choice',4,16)
    while True:
        frame=_movement_move(state,frame,'unit',frame.auxiliary.word(),16)
        frame=first_replace(frame,auxiliary=frame.auxiliary.advance(2))
        negative=bool(frame.status&8)
        frame=_movement_move(state,frame,'target_y',3,16)
        if negative:
            frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())
            frame=_movement_move(state,frame,'count',15,16)
            frame=_game_text_fill_longs_fields(state,frame,'count')
            frame=first_replace(frame,roster=state.table_at(0x18844).cursor())
            frame=_movement_move(state,frame,'count',1,16)
            frame=_game_text_call_fields(state,frame,0xAE8A,0x18822)
            frame=_movement_move(state,frame,'count',15,16)
            frame=_game_text_fill_longs_fields(state,frame,'count')
        else:
            frame=_map_presentation_bit_fields(state,frame,frame.unit,1<<14)
            if not frame.status&4:frame=_movement_move(state,frame,'target_y',2,16)
            frame=_movement_move(state,frame,'unit',low16(frame.unit)&255,16)
            frame=_movement_move(state,frame,'count',low16(frame.unit),16)
            frame=_movement_fixed_shift_word(state,frame,'unit',1)
            frame=_map_presentation_arithmetic_fields(state,frame,'unit',low16(frame.count))
            frame=_movement_fixed_shift_word(state,frame,'unit',1)
            frame=first_replace(frame,roster=state.table_at(u32(0x8A504+s16(low16(frame.unit)))).cursor(),
                candidates=state.table_at(0xFFFFD300).cursor())
            frame=_movement_move(state,frame,'count',2,16)
            frame=_game_text_call_fields(state,frame,0xAE8A,0x187E4)
        frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())
        frame=_movement_move(state,frame,'count',95,16)
        frame=_game_text_upload_longs_fields(state,frame,'count')
        if negative:return frame
        frame,again=_map_presentation_db_fields(frame,'choice')
        if not again:return frame
def cycle_available_direction_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x1CF84)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFEFBE).cursor())
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFEFC6,2),16)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF603,1),8)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&12,16)
    if frame.status&4:return frame
    frame=_map_presentation_bit_fields(state,frame,frame.target_x,4)
    backwards=bool(frame.status&4)
    while True:
        frame=_map_presentation_arithmetic_fields(state,frame,'target_y',2,backwards)
        frame=_movement_move(state,frame,'target_y',low16(frame.target_y)&7,16)
        frame=_movement_test(state,frame,frame.candidates.word(low16(frame.target_y)),16)
        if not frame.status&8:break
    return _setup_write_fields(state,frame,0xFFFFEFC6,low16(frame.target_y))
def render_direction_choice_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x1CFC6)
    frame=_map_presentation_bit_fields(state,frame,state.read(0xFFFFF321,1),16)
    if not frame.status&4:return frame
    frame=first_replace(frame,roster=state.table_at(0x1D022).cursor(),controller=state.table_at(0x1D012).cursor())
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFEFC6,2),16)
    frame=_movement_fixed_shift_word(state,frame,'unit',1)
    frame=first_replace(frame,candidates=state.table_at(state.read(0x00FF382C,4)).cursor())
    frame=_movement_move(state,frame,'target_x',0,16)
    frame=_movement_move(state,frame,'target_x',frame.candidates.byte(1),8)
    frame=_map_presentation_arithmetic_fields(state,frame,'target_x',frame.controller.word(low16(frame.unit)))
    frame=_movement_fixed_shift_word(state,frame,'target_x',4)
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'target_y',frame.candidates.byte(2),8)
    frame=_map_presentation_arithmetic_fields(state,frame,'target_y',frame.controller.word(low16(frame.unit),2))
    frame=_movement_fixed_shift_word(state,frame,'target_y',4)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=_setup_write_fields(state,frame,0xFFFFF60A,state.read(0xFFFFF314,2))
    frame=_setup_write_fields(state,frame,0xFFFFF60E,state.read(0xFFFFF318,2))
    return _game_text_call_fields(state,frame,0xAC28,0x1D010)
def update_direction_choice_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_resource_cost_frame(state,frame,0x1CF58)
    frame=_game_text_call_fields(state,frame,0x1CF84,0x1CF5C)
    frame=_game_text_call_fields(state,frame,0x1CFC6,0x1CF60)
    frame=_map_presentation_bit_fields(state,frame,state.read(0xFFFFF603,1),32)
    if frame.status&4:return frame
    frame=_game_text_call_fields(state,frame,0xC0B6,0x1CF70)
    for address,value in ((0xFFFFF612,208),(0xFFFFF362,3),(0xFFFFF36A,18)):
        frame=_setup_write_fields(state,frame,address,value)
    return frame


# C59 complete display/order ABI; historical algorithms are projections only.
"""Complete primary-force order preparation and candidate collection.

The assignment/map/anchor/edge algorithms are the existing sole policy
cores. New bodies supply the actual D/A/CCR-X/SP calling contract, original
indexed WORD target, real MOVEM LONG saves, and original carry/stop branches.
Unknown order handlers retain the actual235AA slot instead of returning.
"""
from .contexts_display_fields import (
    display_frame_fields, display_move_fields, display_store_fields,
    display_address_fields, display_shift_word_fields, display_call_fields,
    display_child_fields,
)


def _primary_target_child_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame, target: int) -> FirstDeploymentFrame:
    """Complete-frame projections of the existing unique policy dependencies."""
    from .services import BattlePolicyMemory
    frame = display_frame_fields(state, frame)
    if target == 0x1A438:
        from ..high_level_battle_ai.business_actions import _battle_action_map_fields
        return _battle_action_map_fields(BattlePolicyMemory(state), frame)
    if target == 0x235CC:
        from .services import test_battlefield_leader_roster_presence_fields
        return test_battlefield_leader_roster_presence_fields(BattlePolicyMemory(state), frame).validate(state).frame
    if target in (0x2540E, 0x2536A):
        from .services import prepare_first_side_assignment_fields, initialize_first_side_deployment_fields
        if target == 0x2540E:
            return prepare_first_side_assignment_fields(BattlePolicyMemory(state), frame)
        return initialize_first_side_deployment_fields(BattlePolicyMemory(state), frame)
    if target in (0x25C02, 0x25C2A, 0x25C9C, 0x25F0A,
            0x25CB8, 0x25CBE, 0x25D96, 0x25D9C):
        policy = _force_turn_policy_fields(frame)
        if target == 0x25C02:
            returned = _read_battle_policy_anchor(state, policy)
        elif target == 0x25C2A:
            returned = _battle_policy_occupied(state, policy)
        elif target == 0x25C9C:
            returned = _battle_policy_empty_slot(state, policy)
        elif target == 0x25F0A:
            returned = _battle_policy_second_anchor(state, policy)
        elif target in (0x25CB8, 0x25CBE):
            returned = _battle_policy_first_edge(state, policy, target == 0x25CB8)
        else:
            returned = _battle_policy_second_edge(state, policy, target == 0x25D96)
        return _battle_policy_retained_frame(state, returned)
    if target in (0x25DF8, 0x25F28):
        from .services import (promote_first_roster_deployment_candidate_fields,
            promote_second_roster_deployment_candidate_fields)
        if target == 0x25DF8:
            return promote_first_roster_deployment_candidate_fields(BattlePolicyMemory(state), frame)
        return promote_second_roster_deployment_candidate_fields(BattlePolicyMemory(state), frame)
    from .business_main import _campaign_known_child_fields
    return _campaign_known_child_fields(state, frame, target)


def execute_primary_force_orders_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """23562: assignment, budget, ordered leader scan and actual indexed CALL."""
    from .business_movement_support import _movement_compare, _movement_save_longs, _movement_restore_longs
    frame = display_frame_fields(state, frame)
    frame = display_call_fields(state, frame, 152590, 144742)
    frame = display_call_fields(state, frame, 140400, 144746)
    frame = display_address_fields(state, frame, 'roster', 4294944080)
    frame = display_address_fields(state, frame, 'candidates', 4294946690)
    while True:
        frame = display_call_fields(state, frame, 144844, 144758)
        if frame.status & 1:
            break
        frame = _movement_compare(state, frame, state.read(4294964754, 2), 1041, 16)
        if frame.status & 4:
            break
        leader = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = display_move_fields(state, frame, 'choice', leader)
        if frame.status & 8:
            break
        order = frame.candidates.word()
        frame = first_replace(frame, candidates=frame.candidates.advance(2))
        frame = display_move_fields(state, frame, 'target_x', order)
        frame = _movement_compare(state, frame, low16(frame.target_x), 255, 16)
        if frame.status & 4:
            continue
        frame = display_store_fields(state, frame, 144786, 4294965104, low16(frame.target_x))
        frame = display_shift_word_fields(state, frame, 'target_x', 1)
        table_word = state.read(u32(144822 + s16(low16(frame.target_x))), 2)
        frame = display_move_fields(state, frame, 'target_x', table_word)
        frame = _movement_save_longs(state, frame, ('roster', 'candidates'))
        frame = display_address_fields(state, frame, 'roster', 144912)
        target = u32(frame.roster.base + s16(low16(frame.target_x)))
        frame = _battle_order_call_fields(state, frame, target, 144810)
        frame = _movement_restore_longs(state, frame, ('roster', 'candidates'))
    return display_store_fields(state, frame, 144816, 4294964066, 0, clear=True)


def select_primary_force_order_policy_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """24AD0: true BYTE bit1, opposite call arms, shared24AF0 RTS."""
    from .business_map import _world_map_bit_fields
    frame = display_frame_fields(state, frame)
    frame = _world_map_bit_fields(state, frame, state.read(4294964951, 1), 1)
    return display_call_fields(state, frame, 152426, 150246) if frame.status & 4 else _battle_order_call_fields(state, frame, 150258, 150238)


def initialize_battle_policy_targets_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """25BD8: same map core and both real child initialization slots."""
    frame = display_frame_fields(state, frame)
    frame = display_call_fields(state, frame, 0x1A438, 0x25BDE)
    frame = display_call_fields(state, frame, 0x25BE8, 0x25BE2)
    return display_call_fields(state, frame, 0x25EF0, 0x25BE6)


def initialize_primary_policy_targets_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """25BE8: original anchor/occupied call order, A550 and D7.low=2."""
    frame = display_frame_fields(state, frame)
    frame = display_call_fields(state, frame, 0x25C02, 0x25BEC)
    frame = display_call_fields(state, frame, 0x25C2A, 0x25BF0)
    frame = display_address_fields(state, frame, 'scan', 0xFFFFA550)
    frame = display_move_fields(state, frame, 'choice', 2)
    frame = display_call_fields(state, frame, 0x25C6A, 0x25BFC)
    return display_call_fields(state, frame, 0x25DF8, 0x25C00)


def initialize_secondary_policy_targets_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """25EF0: actual second anchor, A5A4/D7.low=4, second promotion."""
    frame = display_frame_fields(state, frame)
    frame = display_call_fields(state, frame, 0x25F0A, 0x25EF4)
    frame = display_call_fields(state, frame, 0x25C2A, 0x25EF8)
    frame = display_address_fields(state, frame, 'scan', 0xFFFFA5A4)
    frame = display_move_fields(state, frame, 'choice', 4)
    frame = display_call_fields(state, frame, 0x25C6A, 0x25F04)
    return display_call_fields(state, frame, 0x25F28, 0x25F08)


def collect_order_target_candidates_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """25C6A: true carry gates between each real edge/offset child."""
    from .business_movement_support import _movement_add_word
    frame = display_frame_fields(state, frame)
    frame = display_address_fields(state, frame, 'candidates', 0xFFFFA150)
    frame = display_call_fields(state, frame, 0x25C9C, 0x25C72)
    if frame.status & 1:
        return frame
    while True:
        for target, continuation in ((0x25CB8, 0x25C7A), (0x25D96, 0x25C82),
                (0x25DEA, 0x25C8A), (0x25DF2, 0x25C92)):
            frame = display_call_fields(state, frame, target, continuation)
            if frame.status & 1:
                return frame
        frame = _movement_add_word(state, frame, 'choice', 2)


def offset_first_order_target_axis_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """25DEA: real D2 MOVE+ADD, then BRA25CBE; no added call LONG."""
    from .business_movement_support import _movement_add_word
    frame = display_frame_fields(state, frame)
    frame = display_move_fields(state, frame, 'unit', low16(frame.choice))
    frame = _movement_add_word(state, frame, 'unit', low16(frame.target_x))
    return _primary_target_child_frame_fields(state, frame, 0x25CBE)


def offset_second_order_target_axis_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """25DF2: real D3 MOVE+ADD, then BRA25D9C; no manufactured RTS."""
    from .business_movement_support import _movement_add_word
    frame = display_frame_fields(state, frame)
    frame = display_move_fields(state, frame, 'count', low16(frame.choice))
    frame = _movement_add_word(state, frame, 'count', low16(frame.target_y))
    return _primary_target_child_frame_fields(state, frame, 0x25D9C)


def _city_project_save_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Invoke the single complete 83FA storage core on this exact live bus.

    All sixteen physical LONG carriers and the complete SR pass through the
    storage frame.  The outer project JSR slot remains caller-owned; internal
    storage BSRs keep their original slots.  No RAM, SRAM or ROM is copied.
    """
    frame = _resource_cost_frame(state, frame, 33786)
    from ..high_level_storage.contexts_scene_storage import SceneStorageState
    from ..high_level_storage.contexts_storage_fields import StorageFrame
    from ..high_level_storage.business_save import write_saved_game_state_frame_fields
    storage = SceneStorageState(state)
    entered = StorageFrame(d0=frame.target_x, d1=frame.target_y, d2=frame.unit, d3=frame.count, d4=frame.distance, d5=frame.offset_x, d6=frame.offset_y, d7=frame.choice, a0=frame.roster.base, a1=frame.candidates.base, a2=frame.controller.base, a3=frame.scan.base, a4=frame.opponent.base, a5=frame.scratch.base, a6=frame.auxiliary.base, stack_cursor=frame.stack_cursor.base, status_word=state.sr & 65504 | frame.status)
    returned = write_saved_game_state_frame_fields(storage, entered)
    if type(returned) is not StorageFrame:
        from .business_movement_support import MovementContinuationBoundary
        raise MovementContinuationBoundary(33786, frame, 'complete storage return frame required')
    returned.validate(storage)
    state.sr = returned.status_word
    return first_replace(frame, target_x=returned.d0, target_y=returned.d1, unit=returned.d2, count=returned.d3, distance=returned.d4, offset_x=returned.d5, offset_y=returned.d6, choice=returned.d7, roster=state.table_at(returned.a0).cursor(), candidates=state.table_at(returned.a1).cursor(), controller=state.table_at(returned.a2).cursor(), scan=state.table_at(returned.a3).cursor(), opponent=state.table_at(returned.a4).cursor(), scratch=state.table_at(returned.a5).cursor(), auxiliary=state.table_at(returned.a6).cursor(), stack_cursor=state.table_at(returned.stack_cursor).cursor(), status=returned.status_word & 31)


def _battle_order_child_fields(state: SceneState, frame: FirstDeploymentFrame, target: int) -> FirstDeploymentFrame:
    """Resolve the missing battle-order entries onto their sole full algorithms.

    The nine indexed strategies share Highbank's complete retained-field
    interface.  Existing primary entries keep their original display route.
    Second-side initialization shares the existing live policy-memory view;
    no register defaults, RAM copies or synthetic device answers are made.
    """
    frame = display_frame_fields(state, frame)
    uint(target, 32)
    if target in (146620, 146846, 147646, 148206, 148616, 148940, 149192, 149510, 150138):
        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_65_fields
        return highbank_coordinate_live_state_65_fields(state, frame, entry=target)
    if target == 150258:
        from ..high_level_battle_ai.business_formation import initialize_second_side_deployment_fields
        return initialize_second_side_deployment_fields(BattlePolicyMemory(state), frame)
    return display_child_fields(state, frame, target)


def _battle_order_call_fields(state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int) -> FirstDeploymentFrame:
    """Exactly one real CALL LONG, sole child, and its actual RTS read/pop."""
    frame = display_frame_fields(state, frame)
    uint(target, 32)
    uint(continuation, 32)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    returned = _battle_order_child_fields(state, entered, target)
    returned = display_frame_fields(state, returned)
    actual = returned.stack_cursor.long()
    if actual != continuation:
        raise MovementContinuationBoundary(actual, returned, 'original display child continuation changed')
    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))
