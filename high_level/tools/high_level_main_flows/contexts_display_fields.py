"""Complete command/display carriers over the existing independent SceneState.

The vocabulary is logical register roles, not a PC interpreter. Arithmetic,
shifts, multiplication and flags delegate their existing sole primitives.
Each child receives the original physical LONG; unknown hardware/children
retain that actual entered frame and never acquire a synthetic return.
"""
from .domain import SceneState, uint, low16, u32, s16, replace_word
from .contexts_gameplay import FirstDeploymentFrame, first_replace, MovementContinuationBoundary
from .business_movement_support import (
    _movement_frame, _movement_move, _movement_move_long, _movement_test,
    _movement_test_long, _movement_compare, _movement_add_word,
    _movement_binary_flags, _movement_multiply_word,
    _movement_save_longs, _movement_restore_longs,
)


def display_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """All real sixteen LONGs, low CCR and physical A7, with retained full SR."""
    frame = _movement_frame(state, frame)
    state.sr = (state.sr & 65504) | frame.status
    return frame


def display_move_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, value: int, width: int = 16) -> FirstDeploymentFrame:
    return (_movement_move_long(state, frame, name, value) if width == 32
        else _movement_move(state, frame, name, value, width))


def display_store_fields(state: SceneState, frame: FirstDeploymentFrame,
        pc: int, address: int, value: int, size: int = 2,
        clear: bool = False) -> FirstDeploymentFrame:
    """Reuse original-width emit/CLR prior read; retain exact abs.W/abs.L EA."""
    from .business_main import _campaign_emit_fields
    return _campaign_emit_fields(state, frame, pc, address, value, size, clear)


def display_address_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, address: int) -> FirstDeploymentFrame:
    """LEA/MOVEA/ADDA do not modify CCR, even for sign-extended WORD EAs."""
    if name not in ('roster', 'candidates', 'controller', 'scan', 'opponent',
            'scratch', 'auxiliary', 'stack_cursor'):
        raise ValueError('actual display address role required')
    return first_replace(frame, **{name: state.table_at(u32(address)).cursor()})


def display_shift_word_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, amount: int, right: bool = False) -> FirstDeploymentFrame:
    """Delegate the sole WORD shift; larger fixed counts use the existing UI core."""
    if right:
        from .business_movement_support import _movement_fixed_shift_word
        return _movement_fixed_shift_word(state, frame, name, amount, True)
    from .business_scene_support import _aux_text_shift_word_fields
    return _aux_text_shift_word_fields(state, frame, name, amount)


def display_shift_long_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, amount: int) -> FirstDeploymentFrame:
    from ..high_level_scene_flows.business_scene import _glyph_shift_long_fields
    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
    return _glyph_shift_long_fields(SceneRefreshMemory(state), frame, name, amount)


def display_loop_fields(frame: FirstDeploymentFrame,
        name: str) -> tuple[FirstDeploymentFrame, bool]:
    """DBRA only changes its low WORD, leaving every CCR/SR bit untouched."""
    from ..high_level_gameplay_flow.business_services import _scene_refresh_decrement
    frame = _scene_refresh_decrement(frame, name, low16(frame.carrier(name)))
    return frame, low16(frame.carrier(name)) != 65535


def display_status_fields(state: SceneState, frame: FirstDeploymentFrame,
        value: int) -> FirstDeploymentFrame:
    uint(value, 16)
    state.set_status_word(value)
    return first_replace(frame, status=value & 31)


def display_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Exactly one real CALL LONG, sole child, and its actual RTS read/pop."""
    frame = display_frame_fields(state, frame)
    uint(target, 32)
    uint(continuation, 32)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    returned = display_child_fields(state, entered, target)
    returned = display_frame_fields(state, returned)
    actual = returned.stack_cursor.long()
    if actual != continuation:
        raise MovementContinuationBoundary(actual, returned,
            'original display child continuation changed')
    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))


def display_child_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int) -> FirstDeploymentFrame:
    """Named fixed-entry routing; BRA/JMP callers add no physical slot."""
    frame = display_frame_fields(state, frame)
    if target in (0x402C2, 0x661D4, 0x662B4, 0x662C4):
        from ..high_level_dynamic_flows.business_actions import (
            upload_object_officer_name_frame_fields, upload_portrait_tiles_frame_fields,
            upload_scene_tile_block_frame_fields, upload_one_scene_tile_frame_fields)
        if target == 0x402C2:
            return upload_object_officer_name_frame_fields(state, frame)
        if target == 0x661D4:
            return upload_portrait_tiles_frame_fields(state, frame)
        if target == 0x662B4:
            return upload_scene_tile_block_frame_fields(state, frame)
        return upload_one_scene_tile_frame_fields(state, frame)
    if target in (0x9390, 0xA1B2, 0xA278):
        from .business_map import (clear_officer_growth_frame_fields,
            initialize_world_map_view_frame_fields, render_initial_map_rows_frame_fields)
        if target == 0x9390:
            return clear_officer_growth_frame_fields(state, frame)
        if target == 0xA1B2:
            return initialize_world_map_view_frame_fields(state, frame)
        return render_initial_map_rows_frame_fields(state, frame)
    if target in (0x414, 0x53E6):
        from .business_main import upload_officer_roster_panel_frame_fields
        return upload_officer_roster_panel_frame_fields(state, frame)
    if target in (0xDF6E, 0x30960, 0x3096E, 0x30ABE, 0x30AC6, 0x6701E):
        from .business_commands import (draw_diplomacy_parameter_panel_frame_fields,
            _diplomacy_first_force_turn_fields, _diplomacy_second_force_turn_fields,
            draw_diplomacy_parameter_panel_alternate_2_frame_fields)
        if target == 0xDF6E:
            return draw_diplomacy_parameter_panel_frame_fields(state, frame)
        if target in (0x30960, 0x3096E):
            return _diplomacy_first_force_turn_fields(state, frame, target == 0x30960)
        if target in (0x30ABE, 0x30AC6):
            return _diplomacy_second_force_turn_fields(state, frame, target == 0x30ABE)
        return draw_diplomacy_parameter_panel_alternate_2_frame_fields(state, frame)
    if target in (0x23562, 0x24AD0, 0x25BD8, 0x25BE8, 0x25C6A,
            0x25DEA, 0x25DF2, 0x25EF0):
        from .business_gameplay import (
            execute_primary_force_orders_frame_fields, select_primary_force_order_policy_frame_fields,
            initialize_battle_policy_targets_frame_fields, initialize_primary_policy_targets_frame_fields,
            collect_order_target_candidates_frame_fields, offset_first_order_target_axis_frame_fields,
            offset_second_order_target_axis_frame_fields, initialize_secondary_policy_targets_frame_fields)
        if target == 0x23562:
            return execute_primary_force_orders_frame_fields(state, frame)
        if target == 0x24AD0:
            return select_primary_force_order_policy_frame_fields(state, frame)
        if target == 0x25BD8:
            return initialize_battle_policy_targets_frame_fields(state, frame)
        if target == 0x25BE8:
            return initialize_primary_policy_targets_frame_fields(state, frame)
        if target == 0x25C6A:
            return collect_order_target_candidates_frame_fields(state, frame)
        if target == 0x25DEA:
            return offset_first_order_target_axis_frame_fields(state, frame)
        if target == 0x25DF2:
            return offset_second_order_target_axis_frame_fields(state, frame)
        return initialize_secondary_policy_targets_frame_fields(state, frame)
    if target in (0xAE8A, 0xADFC, 0xAD1C):
        from ..high_level_scene_flows.business_scene import (
            decode_glyph_rows_to_buffers_fields, write_vdp_dictionary_repeat_stream_fields,
            write_vdp_packet_stream_fields)
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        memory = SceneRefreshMemory(state)
        if target == 0xAE8A:
            return decode_glyph_rows_to_buffers_fields(memory, frame)
        if target == 0xADFC:
            return write_vdp_dictionary_repeat_stream_fields(memory, frame)
        return write_vdp_packet_stream_fields(memory, frame)
    if target == 0x6826:
        from ..high_level_gameplay_flow.business_services import initialize_video_registers_and_planes_fields
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        return initialize_video_registers_and_planes_fields(SceneRefreshMemory(state), frame)
    if target == 0x22470:
        from .business_gameplay import calculate_force_supply_budgets_fields
        return calculate_force_supply_budgets_fields(state, frame)
    if target == 0x23610:
        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_65_fields
        return highbank_coordinate_live_state_65_fields(state, frame)
    if target == 0x23A6E:
        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_65_fields
        return highbank_coordinate_live_state_65_fields(state, frame, entry=0x23A6E)
    if target in (0x670B8, 0x67126):
        from .business_highbank import select_highest_trait_officer_fields, calculate_force_command_budget_fields
        if target == 0x670B8:
            return select_highest_trait_officer_fields(state, frame)
        return calculate_force_command_budget_fields(state, frame)
    if target in (0x309FC, 0x30B8E, 0x30C3A, 0x30EB4, 0x30F26,
            0x30F54, 0x30FAA, 0x31024, 0x31044, 0x311E6, 0x311FA):
        from .business_scene_support import (
            locate_selected_ruler_city_fields, locate_selected_force_packet_fields,
            deduct_all_map_packet_supply_fields, initialize_force_turn_order_fields,
            select_next_force_turn_fields, recover_idle_officer_readiness_fields,
            run_city_command_assignment_fields, run_city_command_states_fields,
            run_map_packet_command_states_fields, finish_city_command_assignment_fields,
            retain_city_command_stage_fields)
        if target == 0x309FC:
            return locate_selected_ruler_city_fields(state, frame)
        if target == 0x30B8E:
            return locate_selected_force_packet_fields(state, frame)
        if target == 0x30C3A:
            return deduct_all_map_packet_supply_fields(state, frame)
        if target == 0x30EB4:
            return initialize_force_turn_order_fields(state, frame)
        if target == 0x30F26:
            return select_next_force_turn_fields(state, frame)
        if target == 0x30F54:
            return recover_idle_officer_readiness_fields(state, frame)
        if target == 0x30FAA:
            return run_city_command_assignment_fields(state, frame)
        if target == 0x31024:
            return run_city_command_states_fields(state, frame)
        if target == 0x31044:
            return run_map_packet_command_states_fields(state, frame)
        if target == 0x311E6:
            return finish_city_command_assignment_fields(state, frame)
        return retain_city_command_stage_fields(state, frame)
    if target in (0x1A438, 0x235CC, 0x2540E, 0x2536A, 0x25C02,
            0x25C2A, 0x25C9C, 0x25CB8, 0x25CBE, 0x25D96, 0x25D9C,
            0x25DF8, 0x25F0A, 0x25F28):
        from .business_gameplay import _primary_target_child_frame_fields
        return _primary_target_child_frame_fields(state, frame, target)
    if target == 90906:
        from .business_gameplay import sort_map_packet_queue_fields
        return sort_map_packet_queue_fields(state, frame)
    if target == 44906:
        from .business_map import read_world_map_tile_fields
        return read_world_map_tile_fields(state, frame)
    if target == 45140:
        from .business_map import read_map_cell_word_fields
        return read_map_cell_word_fields(state, frame)
    if target == 45166:
        from .business_map import read_initial_map_column_fields
        return read_initial_map_column_fields(state, frame)
    from .business_main import _campaign_known_child_fields
    return _campaign_known_child_fields(state, frame, target)


def display_legacy_frame_fields(state: SceneState, observed, entry: int) -> FirstDeploymentFrame:
    """Only an actually supplied complete frame can enter a whole legacy projection."""
    if type(observed) is not FirstDeploymentFrame:
        raise MovementContinuationBoundary(entry, FirstDeploymentFrame.unobserved(),
            "historical display API did not observe all sixteen LONGs, full CCR-X and physical SP")
    return display_frame_fields(state, observed)
