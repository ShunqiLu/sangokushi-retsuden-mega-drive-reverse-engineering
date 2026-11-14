"""Complete battle AI semantic bindings; addresses and extents, not code data."""
from dataclasses import dataclass
from .domain import VIEW_BASES, SCALARS


@dataclass(frozen=True)
class Binding:
    name: str
    entry: int
    end: int
    completion: str = 'return'


GEOMETRY_BINDINGS = (
    Binding('weighted_training_factor', 0xbac8, 0xbaea),
    Binding('load_battlefield_map_context', 0x1a438, 0x1a44e),
    Binding('read_battlefield_terrain_type', 0x1a44e, 0x1a47a),
    Binding('constrain_transposed_target_coordinate', 0x22b26, 0x22b38),
    Binding('compare_actor_to_weakest_contact_strength', 0x22c18, 0x22c4c),
    Binding('select_weakest_contact_strength', 0x22c4c, 0x22c78),
    Binding('constrain_pursuit_target_coordinate', 0x22c78, 0x22c86),
    Binding('test_other_side_total_shortfall', 0x22cfe, 0x22d30),
    Binding('mark_eligible_actor_for_retreat', 0x22d30, 0x22da6),
    Binding('test_actor_terrain_types_3_or_7', 0x22da6, 0x22de4),
    Binding('count_roster_nonnegative_prefix_bytes', 0x22de4, 0x22e04),
    Binding('constrain_second_pursuit_target_coordinate', 0x22ee0, 0x22eee),
    Binding('test_other_roster_single_member', 0x23046, 0x23072),
    Binding('constrain_target_near_battlefield_anchor', 0x23198, 0x23290),
    Binding('select_nearest_contact_to_battlefield_center', 0x2330a, 0x2336e),
    Binding('test_same_side_total_shortfall', 0x233e2, 0x23414),
    Binding('collect_contacts_in_speed_radius', 0x234d2, 0x23562),
    Binding('test_battlefield_leader_roster_presence', 0x235cc, 0x23610),
    Binding('rounded_radial_distance', 0x3080e, 0x30830),
    Binding('seed_radial_distance_from_thresholds', 0x30830, 0x30876),
)

FORMATION_BINDINGS = (
    Binding('sum_first_side_roster_troops', 0x239d6, 0x239f4),
    Binding('test_force_has_city_assignment', 0x239f4, 0x23a1a),
    Binding('test_second_side_total_with_single_first_roster', 0x23a1a, 0x23a3c),
    Binding('test_second_side_total_with_small_second_roster', 0x23a3c, 0x23a6e),
    Binding('test_point_in_battlefield_staging_rectangle', 0x23b08, 0x23ba6),
    Binding('sample_battlefield_staging_rectangle', 0x23ba6, 0x23bf4),
    Binding('read_first_side_staging_anchor', 0x23bf4, 0x23c3e),
    Binding('test_second_side_relative_total_shortfall', 0x23c9a, 0x23cbc),
    Binding('read_second_side_staging_anchor', 0x23d54, 0x23d9e),
    Binding('choose_east_center_first_formation_point', 0x23e68, 0x23e7a),
    Binding('sample_or_accept_east_formation_region', 0x23e7a, 0x23ef2),
    Binding('choose_west_center_first_formation_point', 0x23ef2, 0x23f06),
    Binding('sample_or_accept_west_formation_region', 0x23f06, 0x23f80),
    Binding('choose_east_flank_first_formation_point', 0x23f80, 0x23fa2),
    Binding('sample_or_accept_east_flank_region', 0x23fa2, 0x24048),
    Binding('choose_lower_center_first_formation_point', 0x24048, 0x2405a),
    Binding('sample_or_accept_lower_formation_region', 0x2405a, 0x240be),
    Binding('choose_east_center_second_formation_point', 0x24188, 0x2419a),
    Binding('choose_west_center_second_formation_point', 0x2419a, 0x241ae),
    Binding('choose_west_flank_second_formation_point', 0x241ae, 0x241d4),
    Binding('sample_or_accept_west_flank_region', 0x241d4, 0x24278),
    Binding('choose_upper_center_second_formation_point', 0x24278, 0x2428a),
    Binding('sample_or_accept_upper_formation_region', 0x2428a, 0x242ee),
    Binding('compare_actor_shifted_troop_word_to_weakest_contact', 0x243a0, 0x243dc),
    Binding('read_outer_east_staging_anchor', 0x2443e, 0x24488),
    Binding('choose_east_center_third_formation_point', 0x2456e, 0x24580),
    Binding('choose_west_center_third_formation_point', 0x24580, 0x24594),
    Binding('choose_west_flank_third_formation_point', 0x24594, 0x245ba),
    Binding('choose_upper_center_third_formation_point', 0x245ba, 0x245cc),
    Binding('read_outer_west_staging_anchor', 0x2467e, 0x246c8),
    Binding('select_contact_nearest_deployment_anchor', 0x24926, 0x24990),
    Binding('read_formation_relative_position_delta', 0x24990, 0x249f4),
    Binding('test_first_side_relative_total_shortfall', 0x24a14, 0x24a36),
    Binding('test_second_roster_type6_count_below_four', 0x24a36, 0x24a7a),
    Binding('test_second_side_threshold_shortfall', 0x24ab6, 0x24ad0),
    Binding('initialize_second_side_deployment', 0x24af2, 0x24b00),
    Binding('prepare_second_side_formation_assignment', 0x24b00, 0x24b2a),
    Binding('sort_side_subroster_by_weighted_troops', 0x24b2a, 0x24bb4),
    Binding('copy_second_side_position_assignment', 0x24bb4, 0x24be4),
    Binding('populate_second_side_unset_positions', 0x25200, 0x25246),
    Binding('prepare_second_side_battlefield_choices', 0x25246, 0x252fa),
    Binding('shuffle_nonzero_choice_slots', 0x252fa, 0x25338),
    Binding('choose_unused_second_side_point', 0x25338, 0x2536a),
    Binding('initialize_first_side_deployment', 0x2536a, 0x25378),
    Binding('promote_first_side_leader', 0x25378, 0x2540e),
    Binding('prepare_first_side_formation_assignment', 0x2540e, 0x25438),
    Binding('copy_first_side_position_assignment', 0x25438, 0x2546c),
    Binding('populate_first_side_unset_positions', 0x25a6c, 0x25ab2),
    Binding('prepare_first_side_battlefield_choices', 0x25ab2, 0x25b88),
    Binding('choose_unused_first_side_point', 0x25b88, 0x25bd8),
)

ACTIONS_BINDINGS = (
    Binding('read_city_deployment_anchor', 0x25c02, 0x25c2a),
    Binding('build_deployment_occupied_cells', 0x25c2a, 0x25c48),
    Binding('append_roster_occupied_cells', 0x25c48, 0x25c6a),
    Binding('find_next_empty_position_slot', 0x25c9c, 0x25cb8),
    Binding('scan_deployment_first_edge', 0x25cb8, 0x25d08),
    Binding('try_place_deployment_cell', 0x25d08, 0x25d96),
    Binding('scan_deployment_second_edge', 0x25d96, 0x25dea),
    Binding('promote_first_roster_deployment_candidate', 0x25df8, 0x25ef0),
    Binding('read_city_second_deployment_anchor', 0x25f0a, 0x25f28),
    Binding('promote_second_roster_deployment_candidate', 0x25f28, 0x25fd2),
    Binding('select_lowest_nonzero_rating', 0x26086, 0x260b0),
    Binding('compute_selected_attribute_budget', 0x260b0, 0x260e4),
    Binding('select_strongest_open_terrain_candidate', 0x261a4, 0x26214),
    Binding('compute_selected_troop_budget_base20', 0x26214, 0x2624c),
    Binding('compute_selected_troop_budget_base30', 0x262c6, 0x262fe),
    Binding('select_strongest_type1_candidate', 0x26378, 0x263d0),
    Binding('compute_then_reload_previous_selected_budget', 0x263d0, 0x26408),
    Binding('test_actor_types_0_4_8', 0x2648a, 0x264d0),
    Binding('select_strongest_type2_candidate', 0x264d0, 0x26528),
    Binding('compute_selected_type2_budget_base30', 0x26528, 0x26560),
    Binding('select_lowest_filtered_rating', 0x26638, 0x2665e),
    Binding('compute_selected_attribute_budget_second_side', 0x2665e, 0x26692),
    Binding('build_non_type6_candidates', 0x26692, 0x266d8),
    Binding('select_strongest_type6_candidate', 0x26752, 0x267aa),
    Binding('compute_type6_budget_from_random_state', 0x267aa, 0x267dc),
    Binding('select_strongest_open_terrain_candidate_second_side', 0x26854, 0x268c4),
    Binding('compute_candidate_budget_base20', 0x268c4, 0x268f8),
    Binding('compute_candidate_budget_base30', 0x26972, 0x269a6),
    Binding('select_strongest_type1_candidate_second_side', 0x26a20, 0x26a78),
    Binding('compute_type1_candidate_budget_base20', 0x26a78, 0x26aac),
    Binding('test_actor_map_relative_types', 0x26b2e, 0x26b74),
    Binding('select_strongest_type2_candidate_with_map_context', 0x26b74, 0x26bc6),
    Binding('compute_type2_candidate_budget_base30', 0x26bc6, 0x26bfa),
)

REUSED_BINDINGS = (Binding('step_random', 0x83D4, 0x83FA),)
NEW_BINDINGS = tuple(sorted(GEOMETRY_BINDINGS + FORMATION_BINDINGS + ACTIONS_BINDINGS,
                            key=lambda binding: binding.entry))
BINDINGS = tuple(sorted(NEW_BINDINGS + REUSED_BINDINGS,
                        key=lambda binding: binding.entry))
BY_NAME = {binding.name: binding for binding in BINDINGS}
BY_ENTRY = {binding.entry: binding for binding in BINDINGS}
ALTERNATE_ENTRY = {}


def validate_binding(binding):
    if type(binding) is not Binding or type(binding.name) is not str:
        raise ValueError('strict semantic Binding required')
    if not binding.name.isidentifier() or BY_NAME.get(binding.name) != binding:
        raise ValueError('declared complete semantic binding required')
    if (type(binding.entry) is not int or type(binding.end) is not int
            or not 0 <= binding.entry < binding.end <= 0x100000
            or binding.entry & 1 or binding.end & 1
            or binding.completion != 'return'):
        raise ValueError('fixed complete original returning extent required')
    return binding


if (len(NEW_BINDINGS), sum(b.end - b.entry for b in NEW_BINDINGS)) != (103, 7070):
    raise ValueError('exact selected battle AI extent required')
if len(BY_NAME) != len(BINDINGS) or len(BY_ENTRY) != len(BINDINGS):
    raise ValueError('unique semantic and physical authorities required')
if any(first.end > second.entry for first, second in zip(BINDINGS, BINDINGS[1:])):
    raise ValueError('unexplained battle AI binding overlap')

