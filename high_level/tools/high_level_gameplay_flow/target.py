"""Gameplay-flow bindings; original addresses, no code payload.

Complete extents are compile scope, not a claim of all services being resolved.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Binding:
    name: str
    entry: int
    end: int
    completion: str = 'return'

CALENDAR_BINDINGS = (
    Binding('process_calendar_city_cycle',0x16b3a,0x16bb8),
    Binding('scan_calendar_officer_mortality',0x16eda,0x16f42),
    Binding('remove_mortal_officer_with_message',0x16f42,0x16fda),
    Binding('choose_city_head_after_mortality',0x16fda,0x16ffc),
    Binding('process_calendar_event_schedulers',0x16ffc,0x17016),
    Binding('show_calendar_event_message',0x17058,0x1707e),
    Binding('process_first_calendar_event',0x1707e,0x17158),
    Binding('show_first_calendar_event_values',0x17158,0x171a6),
    Binding('process_second_calendar_event',0x171fc,0x172f4),
    Binding('show_second_calendar_event_values',0x172f4,0x17342),
    Binding('process_third_calendar_event',0x173a6,0x17426),
    Binding('show_third_calendar_event_values',0x17426,0x17474),
)

BATTLE_BINDINGS = (
    Binding('run_battle_scene_round',0xdc0,0xe7c),
    Binding('initialize_battle_scene',0x17602,0x176b6),
    Binding('compact_active_packed_group_queue',0x176b6,0x176d2),
    Binding('remove_queued_packed_group_member',0x176d2,0x17710),
    Binding('upload_battle_background_planes',0x17710,0x17776),
    Binding('upload_battlefield_tilemap',0x17776,0x177be),
    Binding('upload_battle_scene_labels',0x177be,0x17988),
    Binding('cache_battle_roster_totals',0x17988,0x179be),
    Binding('append_force_head_glyphs',0x179d6,0x17a16),
    Binding('integrate_selected_officer_into_packed_group',0x17f30,0x1802a),
    Binding('reserve_packed_group_member_byte',0x1802a,0x1805a),
    Binding('split_city_resources_into_group',0x1807a,0x18158),
    Binding('refresh_packed_group_average',0x18158,0x18184),
    Binding('copy_selected_city_group_parameter',0x18184,0x18196),
    Binding('group_matches_city_head_carry',0x181a6,0x181e8),
    Binding('append_survivors_to_packed_group',0x181e8,0x18224),
    Binding('add_staged_resources_to_packed_group',0x18224,0x182c4),
    Binding('assign_city_survivor_roster_tokens',0x182c4,0x1830a),
    Binding('merge_city_survivor_rosters',0x1830a,0x183be),
    Binding('resolve_city_battle_damage',0x183f8,0x185ae),
    Binding('award_city_reserve_attrition',0x185e4,0x18706),
    Binding('secondary_roster_has_terrain_six_carry',0x18706,0x1874a),
    Binding('sample_battle_special_status_factor',0x1a706,0x1a78a),
    Binding('collect_battle_special_status_members',0x1a78a,0x1a7a2),
    Binding('compute_battle_damage_potential',0x1a7a2,0x1a7f4),
    Binding('settle_city_battle_outcome',0x1bfec,0x1c1a6),
    Binding('sample_city_postbattle_reserve',0x1c554,0x1c57c),
    Binding('distribute_city_battle_progress',0x1c57c,0x1c5e2),
    Binding('apply_assigned_city_light_attrition',0x1c69e,0x1c732),
    Binding('consume_city_battle_supply_long',0x1c732,0x1c78c),
    Binding('reduce_city_reserve_after_defeat',0x1c78c,0x1c7c4),
    Binding('consume_city_battle_supply_word',0x1c7c4,0x1c82c),
    Binding('consolidate_city_after_battle',0x1cb96,0x1cc26),
    Binding('clear_city_officer_links',0x1cc76,0x1cc94),
    Binding('reassign_city_flagged_officers',0x1cc94,0x1ccbe),
    Binding('rebuild_city_links_from_primary_roster',0x1d542,0x1d57a),
    Binding('classify_duel_object_result',0x1d598,0x1d634),
    Binding('city_reserve_forces_duel_carry',0x1e422,0x1e464),
    Binding('find_nearest_secondary_terrain_target',0x1e464,0x1e4e2),
    Binding('apply_postbattle_city_economic_attrition',0x217c8,0x21854),
    Binding('trigger_battle_for_city_rectangle',0x23736,0x238ae),
    Binding('present_battle_message',0x260e4,0x2612c),
)

SERVICES_BINDINGS = (
    Binding('clear_scene_video_and_state',0x60c,0x68a),
    Binding('select_scene_fill_pattern',0x68a,0x696),
    Binding('reset_scene_input_markers',0x4a16,0x4a2c),
    Binding('initialize_video_registers_and_planes',0x6826,0x68a8),
    Binding('clear_video_sprite_plane',0x68ce,0x6950),
    Binding('enqueue_sound_command',0x808a,0x80d0),
    Binding('copy_video_transfer_descriptor',0x8112,0x812c),
    Binding('wait_for_scene_sound_byte',0x83c8,0x83d4),
    Binding('expand_glyph_row',0xaf04,0xaf1e),
    Binding('expand_glyph_stream',0xaf1e,0xaf48),
    Binding('refresh_gameplay_scene',0xaf48,0xaf6a),
    Binding('load_gameplay_scene',0x1072c,0x10814),
    Binding('select_sound_command_from_scene',0x10814,0x10830),
    Binding('resume_pending_sound',0x10880,0x10896),
    Binding('draw_overlay_frame',0x10896,0x108e2),
    Binding('draw_overlay_frame_header',0x108e2,0x1093e),
    Binding('draw_overlay_frame_middle',0x1093e,0x10972),
    Binding('draw_overlay_frame_footer',0x10972,0x109d8),
    Binding('clear_overlay_frame',0x109d8,0x10a06),
    Binding('stage_sprite_word_packet',0x26bfa,0x26c4c),
    Binding('present_gameplay_message',0x30a74,0x30abe),
)

REUSE_BINDINGS = (
    Binding('build_roster',0x5f48,0x5f7c),
    Binding('step_random',0x83d4,0x83fa),
    Binding('choose_city_head',0xe1f6,0xe26c),
    Binding('roster_contains_force_head_carry',0xe26c,0xe29e),
    Binding('terrain_cell_query',0x142a2,0x142ca),
    Binding('replenish_b200_troops',0x16bb8,0x16c0a),
    Binding('grow_original_long_field',0x16c0a,0x16c2c),
    Binding('credit_primary',0x16c2c,0x16c46),
    Binding('credit_secondary',0x16c46,0x16c5c),
    Binding('commit_income',0x16c5c,0x16c72),
    Binding('scaled_income',0x16c72,0x16c98),
    Binding('deplete_income',0x16c98,0x16cfc),
    Binding('debit_primary',0x16d10,0x16d2a),
    Binding('debit_secondary',0x16d2a,0x16d40),
    Binding('settle_expense',0x16d40,0x16de0),
    Binding('settle_shortage',0x16dea,0x16eda),
    Binding('reset_queue',0x17016,0x17026),
    Binding('append_queue',0x17026,0x17058),
    Binding('submit_three_fields',0x171a6,0x171fc),
    Binding('submit_four_fields',0x17342,0x173a6),
    Binding('submit_classified_fields',0x17474,0x174f0),
    Binding('scale_e1e0',0x17514,0x1752a),
    Binding('scale_e140',0x1752a,0x17540),
    Binding('scale_e320',0x17540,0x17556),
    Binding('scale_e000',0x17556,0x1756c),
    Binding('scale_e0a0',0x1756c,0x17582),
    Binding('scale_e5a0',0x17582,0x17598),
    Binding('sample_once',0x17598,0x175a8),
    Binding('sample_small',0x175a8,0x175c2),
    Binding('sample_wide',0x175c2,0x175dc),
    Binding('wrapped_product',0x175dc,0x175ec),
    Binding('divide_percent',0x175ec,0x17602),
    Binding('sum_group_troops',0x179be,0x179d6),
    Binding('find_group_at_coordinate',0x17d10,0x17d3c),
    Binding('settle_duel_training_and_troops',0x188a6,0x189d4),
    Binding('grant_duel_fallback_progress',0x189d4,0x18a2e),
    Binding('grant_duel_troop_difference_progress',0x18a2e,0x18a54),
    Binding('remove_zero_readiness_duelist',0x18a54,0x18a94),
    Binding('settle_duel_result_roster',0x18a94,0x18ac6),
    Binding('transfer_battle_roster',0x18ac6,0x18b00),
    Binding('settle_duel_packets',0x18b00,0x18b94),
    Binding('apply_duel_disposition',0x18b94,0x18c56),
    Binding('detach_zero_readiness_duelists',0x18c56,0x18c88),
    Binding('detach_defeated_duelist',0x18c88,0x18cb4),
    Binding('load_battlefield_map_context',0x1a438,0x1a44e),
    Binding('read_battlefield_terrain_type',0x1a44e,0x1a47a),
    Binding('compute_outcome_force_ratio',0x1c1c2,0x1c2a0),
    Binding('build_city_assigned_outcome_candidates',0x1c2a0,0x1c2c8),
    Binding('build_battlefield_outcome_candidates',0x1c2c8,0x1c2fc),
    Binding('apply_battlefield_ratio_losses',0x1c2fc,0x1c39c),
    Binding('apply_city_assigned_heavy_losses',0x1c39c,0x1c466),
    Binding('consume_city_battle_resources',0x1c466,0x1c554),
    Binding('apply_battlefield_heavy_losses_and_detach',0x1c5ee,0x1c69e),
    Binding('rebuild_primary_after_battle',0x1c82c,0x1c8bc),
    Binding('sort_returning_officer_status',0x1c8bc,0x1c942),
    Binding('partition_city_survivors',0x1c942,0x1c9fe),
    Binding('owner_has_other_city_carry',0x1c9fe,0x1ca3c),
    Binding('restore_returning_officer_assignments',0x1ca3c,0x1ca60),
    Binding('allocate_packed_group_resources',0x1ca60,0x1cb08),
    Binding('rebuild_secondary_after_battle',0x1cb08,0x1cb96),
    Binding('settle_battle_packed_armies',0x1d03c,0x1d0a2),
    Binding('remove_defeated_packed_member',0x1d0a2,0x1d142),
    Binding('replace_or_remove_group_references',0x1d142,0x1d198),
    Binding('transfer_outcome_officer',0x1d198,0x1d20a),
    Binding('detach_member_keep_group_cursor',0x1d20a,0x1d29e),
    Binding('replace_group_head_reference',0x1d29e,0x1d2e8),
    Binding('remove_group_reference',0x1d2e8,0x1d318),
    Binding('attach_member_shift_packet',0x1d318,0x1d3bc),
    Binding('settle_group_at_city',0x1d3bc,0x1d40c),
    Binding('locate_group_city',0x1d40c,0x1d44c),
    Binding('credit_packed_group_resources',0x1d44c,0x1d4b8),
    Binding('erase_group_packet',0x1d4b8,0x1d4da),
    Binding('adjust_battle_losing_loyalty',0x1d4da,0x1d542),
    Binding('initialize_prebattle_head_bytes',0x1d57a,0x1d598),
    Binding('apply_returning_officer_loyalty',0x208ce,0x20930),
    Binding('append_group_from_survivor_roster',0x21514,0x2159e),
    Binding('choose_empty_neighbor_position',0x21efe,0x21f82),
    Binding('rounded_radial_distance',0x3080e,0x30830),
    Binding('seed_radial_distance_from_thresholds',0x30830,0x30876),
    Binding('signed_divmod',0x35760,0x3576c),
    Binding('positive_denominator',0x3576c,0x3577a),
    Binding('unsigned_divmod',0x3577a,0x357da),
    Binding('word_pair_divmod',0x357da,0x357f8),
)

NEW_BINDINGS = tuple(sorted(CALENDAR_BINDINGS+BATTLE_BINDINGS+SERVICES_BINDINGS,key=lambda b:b.entry))
REUSED_BINDINGS = REUSE_BINDINGS
BINDINGS = tuple(sorted(NEW_BINDINGS+REUSED_BINDINGS,key=lambda b:b.entry))
BY_NAME = {b.name:b for b in BINDINGS}
BY_ENTRY = {b.entry:b for b in BINDINGS}

def validate_binding(binding):
    if type(binding) is not Binding or BY_NAME.get(binding.name)!=binding:
        raise ValueError('declared complete target Binding required')
    if (type(binding.entry) is not int or type(binding.end) is not int or
        not 0<=binding.entry<binding.end<=0x100000 or binding.entry&1 or binding.end&1
        or binding.completion!='return'):
        raise ValueError('whole original extent required')
    return binding

if (len(NEW_BINDINGS),sum(b.end-b.entry for b in NEW_BINDINGS),len(REUSED_BINDINGS),sum(b.end-b.entry for b in REUSED_BINDINGS))!=(75,8294,83,6760):
    raise ValueError('complete new/reused physical scope required')
if len(BY_NAME)!=158 or len(BY_ENTRY)!=158 or any(a.end>b.entry for a,b in zip(BINDINGS,BINDINGS[1:])):
    raise ValueError('unique nonoverlapping semantic/physical authorities required')
