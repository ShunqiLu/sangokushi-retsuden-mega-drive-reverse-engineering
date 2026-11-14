"""Complete AI policy extents and semantic ABI; no encoded code payload."""
from dataclasses import dataclass
from .domain import VIEW_BASES, SCALARS

@dataclass(frozen=True)
class Binding:
    name:str
    entry:int
    end:int
    completion:str='return'

ECONOMY_BINDINGS=(
    Binding('select_welfare_officer',0x32260,0x3229c),
    Binding('plan_welfare_budget',0x3229c,0x322f0),
    Binding('select_development_officer',0x32340,0x3236e),
    Binding('plan_development_budget',0x3236e,0x323c2),
    Binding('select_resource_support_city',0x3244a,0x324ac),
    Binding('estimate_city_troop_requirement',0x324ac,0x324ee),
    Binding('plan_city_defense_target',0x324fa,0x32562),
    Binding('plan_force_support_action',0x32592,0x325e4),
    Binding('clear_economy_command',0x33038,0x33040),
    Binding('count_economy_roster',0x330cc,0x330de),
    Binding('select_roster_intelligence_max',0x330de,0x33106),
    Binding('plan_foreign_officer_recruitment',0x33106,0x33160),
    Binding('select_foreign_neighbor_officer',0x33160,0x331bc),
    Binding('scan_city_officer_candidate',0x331bc,0x3321a),
    Binding('choose_resource_action',0x3324c,0x33274),
    Binding('choose_training_action',0x33274,0x33292),
    Binding('select_roster_training_min',0x33292,0x332c0),
    Binding('commit_recruitment_candidate',0x332c0,0x33322),
    Binding('select_unmarked_roster_intelligence_max',0x333f4,0x33422),
    Binding('clear_candidate_city_order',0x33422,0x3346a),
    Binding('plan_equipment_action',0x3363c,0x33666),
    Binding('sort_equipment_roster',0x33666,0x336d6),
    Binding('purchase_roster_equipment',0x336d6,0x33764),
    Binding('plan_troop_purchase_action',0x33770,0x33790),
    Binding('clear_equipment_command',0x338ba,0x338c2),
)

ROUTES_BINDINGS=(
    Binding('choose_neighbor_relation_phase',0x338ec,0x33906),
    Binding('hostile_neighbor_exists_carry',0x33906,0x3393e),
    Binding('choose_unowned_neighbor_phase',0x3393e,0x33958),
    Binding('unowned_neighbor_exists_carry',0x33958,0x33988),
    Binding('choose_roster_troop_phase',0x33988,0x339a6),
    Binding('count_roster_large_troops',0x339a6,0x339cc),
    Binding('choose_random_neighbor_phase',0x339cc,0x339f4),
    Binding('choose_roster_troop_phase_five',0x339f4,0x33a10),
    Binding('evaluate_neighbor_march_phase',0x33a10,0x33a36),
    Binding('sum_city_officer_troops',0x33a36,0x33a70),
    Binding('choose_weaker_enemy_neighbor',0x33a70,0x33ab8),
    Binding('commit_unowned_neighbor_march',0x33ab8,0x33b6c),
    Binding('shortest_unowned_neighbor',0x33b6c,0x33be8),
    Binding('price_two_officer_march',0x33be8,0x33c3a),
    Binding('append_two_officer_march',0x33c3a,0x33cc8),
    Binding('restore_departing_city_head',0x33d92,0x33daa),
    Binding('commit_support_march',0x33daa,0x33e5e),
    Binding('collect_support_officers',0x33e5e,0x33f0a),
    Binding('choose_support_roster',0x33f0a,0x33faa),
    Binding('price_support_march',0x33faa,0x34030),
    Binding('append_support_march',0x34030,0x340d8),
    Binding('rebuild_departing_city_head',0x340d8,0x340f0),
    Binding('finish_support_phase',0x340f0,0x340f8),
    Binding('evaluate_packed_group_supply_phase',0x34140,0x3417a),
    Binding('price_packed_group',0x3417a,0x341b0),
    Binding('choose_group_destination_phase',0x341b0,0x341ce),
    Binding('evaluate_transport_supply_phase',0x342be,0x34300),
    Binding('reachable_transport_coordinate_carry',0x34300,0x34376),
    Binding('commit_staging_city_phase',0x34376,0x343b0),
    Binding('choose_nearest_staging_city',0x343b0,0x3443e),
    Binding('choose_destination_progress_phase',0x3443e,0x34468),
    Binding('choose_terrain_exit_phase',0x34468,0x344c6),
)

ACTIONS_BINDINGS=(
    Binding('locate_packet_contact_city',0x344c6,0x3453a),
    Binding('choose_city_assault_action',0x3453a,0x34564),
    Binding('measure_packet_ready_strength',0x34564,0x345c2),
    Binding('measure_chosen_city_strength',0x345c2,0x345f8),
    Binding('choose_city_mask_action',0x345f8,0x34648),
    Binding('choose_processed_city_action',0x34648,0x3466a),
    Binding('choose_linked_city_action',0x3466a,0x346b0),
    Binding('choose_packet_resource_action',0x346b0,0x346c6),
    Binding('packet_resource_shortfall',0x346c6,0x3471a),
    Binding('count_linked_force_officers',0x3473a,0x3477a),
    Binding('build_limited_packet_roster',0x3477a,0x347de),
    Binding('rank_packet_roster',0x347de,0x34854),
    Binding('partition_ranked_packet_roster',0x34854,0x34870),
    Binding('choose_adjacent_group_action',0x3487e,0x3489c),
    Binding('collect_adjacent_hostile_groups',0x3489c,0x3492e),
    Binding('choose_adjacent_strength_action',0x3492e,0x3495a),
    Binding('store_packet_strength',0x3495a,0x34986),
    Binding('select_largest_hostile_candidate',0x34986,0x349ba),
    Binding('measure_unmasked_candidate_strength',0x349ba,0x349f2),
    Binding('queue_packet_stationary_command',0x349f2,0x34a2c),
    Binding('choose_reachable_city_action',0x34a2c,0x34a64),
    Binding('packet_resource_range',0x34a64,0x34ad0),
    Binding('collect_reachable_hostile_cities',0x34ad0,0x34b58),
    Binding('select_lightest_reachable_city',0x34b58,0x34b98),
    Binding('measure_indexed_city_strength',0x34b98,0x34bd0),
    Binding('queue_packet_march_action',0x34bd0,0x34c0a),
    Binding('choose_reachable_group_action',0x34c0a,0x34c3e),
    Binding('store_packet_comparison_strength',0x34c3e,0x34c6a),
    Binding('collect_reachable_hostile_groups',0x34c6a,0x34d0c),
    Binding('select_lightest_group_candidate',0x34d0c,0x34d30),
    Binding('measure_group_candidate_strength',0x34d30,0x34d52),
    Binding('purchase_packet_supplies',0x34dce,0x34dfc),
    Binding('load_packet_cash',0x34dfc,0x34e1c),
    Binding('fill_packet_troop_deficits',0x34e1c,0x34e5c),
    Binding('buy_packet_food',0x34e5c,0x34eb6),
    Binding('buy_packet_equipment',0x34eb6,0x34f02),
    Binding('clear_packet_supply_command',0x34f02,0x34f0a),
    Binding('choose_packet_readiness_action',0x34f0a,0x34f26),
    Binding('load_active_packet_roster',0x34f36,0x34f64),
    Binding('choose_active_packet_contact_action',0x34f94,0x34fae),
    Binding('active_packet_terrain_contact',0x34fae,0x35064),
    Binding('choose_active_city_assault_action',0x35064,0x3508a),
    Binding('project_selected_roster_strength',0x3508a,0x350b2),
    Binding('measure_self_assigned_officers',0x350b2,0x350e8),
    Binding('choose_active_city_mask_action',0x350e8,0x35132),
    Binding('choose_active_processed_city_action',0x35132,0x35154),
    Binding('choose_active_linked_city_action',0x35154,0x35172),
    Binding('linked_city_force',0x35172,0x351a2),
    Binding('choose_selected_roster_resource_action',0x351a2,0x351ca),
    Binding('selected_roster_strength',0x351ca,0x351e4),
    Binding('selected_roster_troop_shortfall',0x351e4,0x35210),
    Binding('choose_active_adjacent_group_action',0x35286,0x352a4),
    Binding('collect_active_adjacent_groups',0x352a4,0x35342),
    Binding('choose_active_strength_action',0x35342,0x35366),
    Binding('selected_roster_comparison_strength',0x35366,0x35380),
    Binding('measure_lightest_active_candidate',0x35380,0x353bc),
    Binding('schedule_active_comparison_dialogue',0x353bc,0x353ec),
    Binding('clear_active_contact_command',0x353ec,0x353f4),
    Binding('clear_active_idle_command',0x353f4,0x353fc),
)

REUSED_BINDINGS=(
    Binding('build_roster',0x5f48,0x5f7c),
    Binding('build_path',0x6518,0x6562),
    Binding('initialize_path_grid',0x6562,0x6624),
    Binding('normalize_path_coordinates',0x6624,0x664e),
    Binding('expand_path_frontier',0x664e,0x66c2),
    Binding('visit_path_neighbor',0x66c2,0x66ee),
    Binding('path_neighbor_is_goal',0x66ee,0x670a),
    Binding('mark_path_direction',0x6710,0x672c),
    Binding('read_path_direction',0x672c,0x6748),
    Binding('read_path_cost',0x6748,0x6764),
    Binding('reconstruct_path',0x6764,0x678e),
    Binding('step_back_path',0x678e,0x67b4),
    Binding('step_random',0x83d4,0x83fa),
    Binding('choose_city_head',0xe1f6,0xe26c),
    Binding('roster_contains_force_head_carry',0xe26c,0xe29e),
    Binding('mark_selected_roster_bit14',0x320a0,0x320c0),
    Binding('count_force_cities',0x325e4,0x325fc),
    Binding('select_force_by_city_count',0x325fc,0x32652),
    Binding('ai_recruitment_capacity_gate',0x33790,0x337c6),
    Binding('distribute_existing_troop_pool',0x337c6,0x3382e),
    Binding('buy_and_distribute_troops',0x3382e,0x338ba),
    Binding('build_ai_movement_packet',0x33cc8,0x33d0e),
    Binding('append_ai_path_steps',0x33d0e,0x33d6c),
    Binding('read_path_step_cost',0x33d7c,0x33d92),
    Binding('choose_ai_destination',0x341ce,0x34280),
    Binding('city_roster_full_carry',0x34280,0x342be),
    Binding('signed_divmod',0x35760,0x3576c),
    Binding('positive_denominator',0x3576c,0x3577a),
    Binding('unsigned_divmod',0x3577a,0x357da),
    Binding('word_pair_divmod',0x357da,0x357f8),
)

NEW_BINDINGS=tuple(sorted(ECONOMY_BINDINGS+ROUTES_BINDINGS+ACTIONS_BINDINGS,key=lambda b:b.entry))
BINDINGS=tuple(sorted(NEW_BINDINGS+REUSED_BINDINGS,key=lambda b:b.entry))
BY_NAME={b.name:b for b in BINDINGS}
TABLE_BINDINGS={n:dict(address=a,suffix='w' if a>=0xFFFF8000 else 'l') for n,a in VIEW_BASES.items()}
SCALAR_BINDINGS={n:dict(address=a,width=s*8,suffix='w' if a>=0xFFFF8000 else 'l') for n,(a,s) in SCALARS.items()}
ALTERNATE_ENTRY=0x651C

def validate_binding(value):
    if (type(value) is not Binding or type(value.name) is not str or
        type(value.entry) is not int or type(value.end) is not int or
        type(value.completion) is not str or value not in BINDINGS):
        raise ValueError('strict complete AI policy Binding required')

