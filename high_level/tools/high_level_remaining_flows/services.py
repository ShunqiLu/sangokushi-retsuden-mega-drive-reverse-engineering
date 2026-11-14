"""Genuine reused semantic services and explicit typed unbound-call boundary.

No fabricated return values, fake wait completion, code-payload interpretation
or copied state. Existing functions are exact aliases on the same SceneState.
Unlinked ABIs raise UnresolvedCall with the actual target and supplied context.
"""
from ..high_level_main_flows.services import (
    UnresolvedCall, ServiceBinding, LogicalServices, call_target,
    BattlePolicyMemory, collect_contacts_in_speed_radius_fields,
    sample_battle_action_random_fields, select_strongest_type6_candidate_fields, compute_type6_budget_from_random_state_fields,
    select_strongest_open_terrain_candidate_second_side_fields, compute_candidate_budget_fields, compute_candidate_budget_base20_fields, compute_candidate_budget_base30_fields,
    clear_video_sprite_plane, enqueue_sound_command, wait_for_scene_sound_byte,
    step_random, sample_random_pair, expand_glyph_row, expand_glyph_stream,
    stage_sprite_word_packet, decode_glyph_rows_to_buffers,
    write_vdp_packet_stream, write_vdp_dictionary_repeat_stream,
    append_clipped_scene_sprites, append_unclipped_scene_sprites,
    write_vdp_word_rle_stream, write_vdp_swapped_byte_rle_stream,
    read_vdp_plane_rle_rows, read_vdp_plane_literal_rows,
    read_vdp_plane_rle_rows_from_control, advance_plane_row,
    advance_scene_palette_fade, flush_scene_transfer_queue,
    set_vram_write_address, append_scene_sprite_entries,
    copy_scene_palette_variant, snapshot_and_clear_scene_palette,
    begin_scene_palette_darken, darken_palette,
    sample_random_preserving_seed_carrier, upload_portrait_tiles,
    append_map_sprites, append_six_place_decimal_value, append_six_place_decimal_fields,
    award_defense_progress, clear_completed_monthly_actions,
    query_scaled_terrain, refresh_gameplay_scene,
    initialize_video_registers_and_planes,
    GlyphColors, GlyphStreamResult, SpriteControlContext, SpriteControlResult,
    PlaneRowContext, PlaneRowResult, PlaneStreamResult, VdpStreamResult,
    GlyphRowsResult, SceneRenderFrame, SpriteBatchContext, SpriteBatchResult,
    TileUploadResult, MapSpriteResult, DefenseProgressResult,
    MonthlyActionsResult, TerrainQueryResult,
)

# Actual same-state1DCAA carriers and the already unique arithmetic/radial cores.
from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
from ..high_level_battle_ai.contexts_first_deployment import (
    FirstDeploymentFrame, FirstDeploymentArithmeticBoundary,
    FirstDeploymentReturnBoundary, first_replace,
)
from ..high_level_battle_ai.business_formation import (
    _first_word, _first_byte, _first_long, _first_shift_word, _first_right_word,
    _first_add_word, _first_sub_word, _first_memory_word,
)
from ..high_level_battle_ai.business_geometry import rounded_deployment_radial_distance_fields


# Current complete 17C8A fields; the frozen movement-v2 baseline is untouched.
from ..high_level_main_flows.business_movement_support import ensure_neighbor_capacity_fields

# Sole second-side standard-action field authorities; caller owns outer tokens.
from ..high_level_battle_ai.business_formation import first_deployment_random_fields
from ..high_level_battle_ai.business_actions import (
    select_lowest_filtered_rating_fields,
    compute_selected_attribute_budget_second_side_fields,
    build_non_type6_candidates_fields,
)


# Current Scene-only17F30/260E4 successors, original outer slot caller-owned.
from ..high_level_main_flows.business_movement_support import (
    integrate_selected_officer_into_packed_group_fields,
    present_battle_message_fields,
)

# Sole late type1/type2 action bodies; their callers retain true outer slots.
from ..high_level_battle_ai.business_actions import (
    select_strongest_type1_candidate_second_side_fields,
    compute_type1_candidate_budget_base20_fields,
    test_actor_map_relative_types_fields,
    select_strongest_type2_candidate_with_map_context_fields,
    compute_type2_candidate_budget_base30_fields,
)

from ..high_level_battle_ai.business_geometry import select_weakest_contact_strength_fields
from ..high_level_battle_ai.business_formation import (
    compare_actor_shifted_troop_word_to_weakest_contact_fields, read_outer_east_staging_anchor_fields, select_contact_nearest_deployment_anchor_fields, read_formation_relative_position_delta_fields, test_point_in_battlefield_staging_rectangle_fields, sample_battlefield_staging_rectangle_fields,
)

from ..high_level_battle_ai.business_formation import read_second_side_staging_anchor_fields

# B15 sole presentation subcores; true outer continuations belong to callers.
from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
from ..high_level_gameplay_flow.business_battle import (
    sample_battle_special_status_factor_fields,
    collect_battle_special_status_members_fields,
    compute_battle_damage_potential_fields,
    _presentation_sub_long_fields,
)


# Current Scene arithmetic and call ABIs; no duplicated gameplay algorithm.
from ..high_level_main_flows.business_movement_support import (_movement_frame, _movement_test, _movement_move, _movement_compare, _movement_shift_word, _movement_add_byte, _movement_fixed_shift_word, _movement_add_word, _movement_move_long, _movement_binary_flags, _movement_arithmetic_long, _movement_test_long, _movement_multiply_word, _movement_divu_word, _movement_bit, _movement_save_longs, _movement_restore_longs)
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
from ..high_level_battle_ai.business_actions import (sample_battle_action_random_fields, _battle_action_map_fields, _deployment_terrain_lookup)

from ..high_level_battle_ai.business_formation import read_first_side_staging_anchor_fields


# C19 sole returning-loyalty core; caller owns outer JSR and saved officer WORD.
from ..high_level_gameplay_flow.business_reuse import apply_returning_officer_loyalty_fields

# Sole existing LONG comparison semantics used by recruitment1AC4C.
from ..high_level_battle_ai.business_formation import _first_compare_long

# Same-state AC08 sole packet owner; caller retains the outer return LONG.
from ..high_level_player_commands.contexts_display import SpritePacketMemory
from ..high_level_player_commands.business_display import append_live_command_sprite_fields

# C21 aliases to established current Scene arithmetic, not copied algorithms.
from ..high_level_main_flows.business_movement_support import (_movement_adjust_word, _movement_load_packed_resource, _movement_store_packed_resource, signed_divmod_fields)

# Sole1072C current refresh/load fields; caller retains its outer return LONG.
from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
from ..high_level_gameplay_flow.business_services import load_gameplay_scene_fields


# Complete current word-packet queue; caller retains its actual outer LONG.
from ..high_level_gameplay_flow.business_services import stage_sprite_word_packet_fields
