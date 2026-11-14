"""Dynamic-flow target metadata, not opcode payload or runtime dispatch proof.

Each shared physical component has one source authority. Public entries may
be aliases or encoded executable vector slots, not separate whole functions.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Binding:
    name:str
    entry:int
    entries:tuple
    segments:tuple
    reused:bool
    kind:str

DUEL_BINDINGS=(
    Binding('resolve_duel_attack',0x27576,((161142, 'resolve_duel_attack'),),((161142, 161146), (161158, 161376), (161382, 161404), (161410, 161658)),False,'new_flow_fragment_with_earlier_shared_control_tail'),
    Binding('perform_duel_feint',0x2757a,((161146, 'perform_duel_feint'),),((161146, 161150), (161810, 161922)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('flee_duel',0x2757e,((161150, 'flee_duel'),),((161150, 161154), (161952, 162046)),False,'new_flow_fragment_with_earlier_shared_control_tail'),
    Binding('finish_special_duel_action',0x27582,((161154, 'finish_special_duel_action'),),((161154, 161158), (162046, 162192)),False,'new_flow_fragment_with_earlier_shared_control_tail'),
    Binding('toggle_duel_turn',0x27882,((161922, 'toggle_duel_turn'),),((161922, 161952),),False,'independent_contiguous_static_return_component'),
    Binding('multiply_duel_weight',0x27abe,((162494, 'multiply_duel_weight'),),((162494, 162534),),False,'independent_contiguous_static_return_component'),
    Binding('prepare_duel_combat_statistics',0x27ae6,((162534, 'prepare_duel_combat_statistics'),),((162534, 162648),),False,'independent_contiguous_static_return_component'),
    Binding('measure_duel_spacing',0x2a26c,((172652, 'measure_duel_spacing'),),((172652, 172692),),False,'independent_contiguous_static_return_component'),
    Binding('choose_duel_cautious_rule',0x2a314,((172820, 'choose_duel_cautious_rule'), (172824, 'choose_duel_cautious_rule_alias'), (172828, 'choose_duel_balanced_rule'), (172832, 'choose_duel_balanced_rule_alias'), (172836, 'choose_duel_pressure_rule'), (172840, 'choose_duel_aggressive_rule')),((172820, 172844), (172868, 172958), (172994, 173044), (173080, 173132), (173168, 173220)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('execute_duel_cautious_rule',0x2a32c,((172844, 'execute_duel_cautious_rule'), (172848, 'execute_duel_balanced_rule'), (172852, 'execute_duel_balanced_rule_alias'), (172856, 'execute_duel_cautious_rule_alias'), (172860, 'execute_duel_pressure_rule'), (172864, 'execute_duel_aggressive_rule'), (173354, 'choose_duel_random_motion'), (174646, 'choose_duel_opponent_special')),((172844, 172868), (173258, 173430), (173472, 173556), (174612, 174682)),False,'complete_static_return_component_with_shared_entries_or_segments'),
)

ACTIONS_BINDINGS=(
    Binding('upload_object_officer_name',0x402c2,((262850, 'upload_object_officer_name'),),((262850, 262940),),False,'independent_contiguous_static_return_component'),
    Binding('start_object_left',0x40d0c,((265484, 'start_object_left'), (265488, 'start_object_right'), (265492, 'start_object_up'), (265496, 'start_object_down'), (265504, 'pursue_opposing_object'), (265508, 'sidestep_opposing_object'), (265550, 'continue_object_left'), (265554, 'continue_object_right'), (265558, 'continue_object_up'), (265562, 'continue_object_down'), (266120, 'continue_object_left_vector'), (266124, 'continue_object_right_vector'), (266128, 'continue_object_up_vector'), (266132, 'continue_object_down_vector')),((265484, 265500), (265504, 265512), (265550, 265566), (265596, 265684), (265718, 265808), (265830, 265898), (265920, 265988), (266010, 266110), (266120, 266588)),False,'new_flow_fragment_with_earlier_shared_control_tail'),
    Binding('resume_object_selected_action',0x40d1c,((265500, 'resume_object_selected_action'),),((265500, 265504),),False,'flow_with_actual_external_or_dynamic_control_boundary'),
    Binding('finish_object_action_noop',0x40d5e,((265566, 'finish_object_action_noop'),),((265566, 265570),),False,'new_flow_fragment_with_earlier_shared_control_tail'),
    Binding('resume_object_pursuit',0x40d62,((265570, 'resume_object_pursuit'), (265574, 'resume_object_pursuit_alias'), (265578, 'resume_object_pursuit_second_alias')),((265570, 265582), (266110, 266120)),False,'flow_with_actual_external_or_dynamic_control_boundary'),
    Binding('advance_object_impact',0x40d6e,((265582, 'advance_object_impact'), (265586, 'advance_object_projectile')),((265582, 265590), (267556, 267746), (267784, 267822), (268024, 268238)),False,'new_flow_fragment_with_earlier_shared_control_tail'),
    Binding('probe_object_left',0x40dd4,((265684, 'probe_object_left'),),((265684, 265706),),False,'independent_contiguous_static_return_component'),
    Binding('object_movement_speed',0x40dea,((265706, 'object_movement_speed'),),((265706, 265718),),False,'independent_contiguous_static_return_component'),
    Binding('probe_object_right',0x40e50,((265808, 'probe_object_right'),),((265808, 265830),),False,'independent_contiguous_static_return_component'),
    Binding('probe_object_up',0x40eaa,((265898, 'probe_object_up'),),((265898, 265920),),False,'independent_contiguous_static_return_component'),
    Binding('probe_object_down',0x40f04,((265988, 'probe_object_down'),),((265988, 266010),),False,'independent_contiguous_static_return_component'),
    Binding('calculate_object_impact_damage',0x4162e,((267822, 'calculate_object_impact_damage'), (267982, 'adjust_damage_for_object_guard')),((267822, 268024),),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('update_object_action_ai',0x41bac,((269228, 'update_object_action_ai'),),((269228, 269284),),False,'independent_contiguous_static_return_component'),
    Binding('dispatch_object_formation_ai',0x41be4,((269284, 'dispatch_object_formation_ai'),),((269284, 269294),),False,'flow_with_actual_external_or_dynamic_control_boundary'),
    Binding('dispatch_object_formation_fallback',0x41cd6,((269526, 'dispatch_object_formation_fallback'),),((269526, 269546), (269628, 269630)),False,'flow_with_actual_external_or_dynamic_control_boundary'),
    Binding('advance_object_retreat_checks',0x41dc0,((269760, 'advance_object_retreat_checks'),),((269690, 269692), (269760, 269790)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('trigger_object_retreat_strength',0x41dde,((269790, 'trigger_object_retreat_strength'), (269854, 'trigger_object_retreat_low_strength'), (269900, 'trigger_object_retreat_outnumbered'), (269942, 'trigger_object_retreat_morale'), (270006, 'trigger_object_retreat_quality')),((269790, 270068),),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('sum_live_object_rosters',0x41f08,((270088, 'sum_live_object_rosters'),),((270088, 270154),),False,'independent_contiguous_static_return_component'),
    Binding('choose_object_retreat_phase',0x41f4a,((270154, 'choose_object_retreat_phase'),),((270154, 270316),),False,'independent_contiguous_static_return_component'),
    Binding('upload_portrait_tiles',0x661d4,((418260, 'upload_portrait_tiles'),),((418260, 418484),),False,'independent_contiguous_static_return_component'),
    Binding('upload_scene_tile_block',0x662b4,((418484, 'upload_scene_tile_block'),),((418484, 418500),),False,'independent_contiguous_static_return_component'),
    Binding('upload_one_scene_tile',0x662c4,((418500, 'upload_one_scene_tile'),),((418500, 418532),),False,'independent_contiguous_static_return_component'),
)

EARLY_PHASE_BINDINGS=(
    Binding('begin_scene_palette_lighten',0x3aa38,((240184, 'begin_scene_palette_lighten'),),((240184, 240248),),False,'new_flow_fragment_with_earlier_shared_control_tail'),
    Binding('snapshot_scene_palette',0x3aa78,((240248, 'snapshot_scene_palette'),),((240248, 240266),),False,'independent_contiguous_static_return_component'),
    Binding('restore_scene_palette',0x3aa9e,((240286, 'restore_scene_palette'),),((240286, 240310),),False,'independent_contiguous_static_return_component'),
    Binding('encode_six_decimal_digits',0x3b2d8,((242392, 'encode_six_decimal_digits'),),((242392, 242454),),False,'independent_contiguous_static_return_component'),
    Binding('append_decimal_digit',0x3b316,((242454, 'append_decimal_digit'),),((242454, 242464),),False,'independent_contiguous_static_return_component'),
    Binding('adjust_scene_scroll',0x3d970,((252272, 'adjust_scene_scroll'),),((252272, 252320),),False,'independent_contiguous_static_return_component'),
    Binding('step_main_scene_phase',0x3dcc2,((253122, 'step_main_scene_phase'),),((253122, 253126), (256242, 256256)),False,'flow_with_actual_external_or_dynamic_control_boundary'),
    Binding('step_result_scene_phase',0x3dcc6,((253126, 'step_result_scene_phase'),),((253126, 253130), (257912, 257926)),False,'flow_with_actual_external_or_dynamic_control_boundary'),
    Binding('step_confirmation_scene_phase',0x3dcca,((253130, 'step_confirmation_scene_phase'),),((253130, 253134), (258082, 258096)),False,'flow_with_actual_external_or_dynamic_control_boundary'),
    Binding('step_transfer_scene_phase',0x3dcce,((253134, 'step_transfer_scene_phase'),),((253134, 253138), (258132, 258146)),False,'flow_with_actual_external_or_dynamic_control_boundary'),
    Binding('step_primary_detail_scene_phase',0x3dcd2,((253138, 'step_primary_detail_scene_phase'),),((253138, 253142), (258524, 258538)),False,'flow_with_actual_external_or_dynamic_control_boundary'),
    Binding('step_secondary_detail_scene_phase',0x3dcd6,((253142, 'step_secondary_detail_scene_phase'),),((253142, 253146), (258702, 258716)),False,'flow_with_actual_external_or_dynamic_control_boundary'),
    Binding('step_summary_scene_phase',0x3dcda,((253146, 'step_summary_scene_phase'),),((253146, 253150), (258880, 258894)),False,'flow_with_actual_external_or_dynamic_control_boundary'),
    Binding('step_pair_transition_scene_phase',0x3dcde,((253150, 'step_pair_transition_scene_phase'),),((253150, 253154), (255508, 255522)),False,'flow_with_actual_external_or_dynamic_control_boundary'),
    Binding('step_initial_scene_phase',0x3dce2,((253154, 'step_initial_scene_phase'),),((253154, 253158), (253162, 253176)),False,'flow_with_actual_external_or_dynamic_control_boundary'),
    Binding('step_exchange_scene_phase',0x3dce6,((253158, 'step_exchange_scene_phase'),),((253158, 253162), (255070, 255084)),False,'flow_with_actual_external_or_dynamic_control_boundary'),
    Binding('initialize_early_scene',0x3dcf8,((253176, 'initialize_early_scene'),),((253176, 253180), (253204, 253734)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('process_early_scene_choice',0x3dcfc,((253180, 'process_early_scene_choice'), (253184, 'present_early_scene_prompt'), (253188, 'finish_early_scene_prompt'), (254548, 'draw_early_scene_choice'), (255088, 'process_exchange_scene_choice')),((253180, 253192), (253734, 254082), (254086, 254606), (255088, 255092), (255242, 255452)),False,'new_flow_fragment_with_earlier_shared_control_tail'),
    Binding('wait_early_scene_choice',0x3dd08,((253192, 'wait_early_scene_choice'),),((253192, 253196), (254616, 254746)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('finish_early_scene_fade',0x3dd0c,((253196, 'finish_early_scene_fade'),),((253196, 253200), (254746, 254786)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('finish_alternate_scene_fade',0x3dd10,((253200, 'finish_alternate_scene_fade'),),((253200, 253204), (254786, 254842)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('append_early_scene_instruction',0x3e37a,((254842, 'append_early_scene_instruction'),),((254842, 254862),),False,'new_flow_fragment_with_earlier_shared_control_tail'),
    Binding('paint_scene_number_rows',0x3e42a,((255018, 'paint_scene_number_rows'),),((255018, 255034),),False,'independent_contiguous_static_return_component'),
    Binding('paint_scene_number_row',0x3e43a,((255034, 'paint_scene_number_row'),),((255034, 255070),),False,'independent_contiguous_static_return_component'),
    Binding('wait_exchange_scene_transition',0x3e46c,((255084, 'wait_exchange_scene_transition'),),((255084, 255088), (255096, 255242)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('finish_exchange_scene_transition',0x3e474,((255092, 'finish_exchange_scene_transition'),),((255092, 255096), (255452, 255508)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('process_pair_phase_counter',0x3e622,((255522, 'process_pair_phase_counter'), (255526, 'confirm_pair_allocation'), (255530, 'update_pair_allocation_input'), (255534, 'exit_pair_allocation'), (256256, 'wait_pair_stage_motion'), (256260, 'advance_pair_stage_motion'), (256264, 'confirm_second_pair_allocation'), (256268, 'present_pair_stage_summary')),((255522, 255538), (255652, 255720), (255942, 256160), (256180, 256242), (256256, 256272), (256394, 256738), (256804, 257224)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('gather_early_scene_input',0x3e632,((255538, 'gather_early_scene_input'),),((255538, 255652),),False,'independent_contiguous_static_return_component'),
    Binding('exchange_scene_pair_fields',0x3e6e8,((255720, 'exchange_scene_pair_fields'),),((255720, 255918),),False,'independent_contiguous_static_return_component'),
    Binding('exchange_scene_actor_records',0x3e7ae,((255918, 'exchange_scene_actor_records'),),((255918, 255942),),False,'independent_contiguous_static_return_component'),
    Binding('refresh_primary_actor_summary',0x3e8a0,((256160, 'refresh_primary_actor_summary'),),((256160, 256180),),False,'independent_contiguous_static_return_component'),
)

LATE_PHASE_BINDINGS=(
    Binding('adjust_secondary_formation_scene',0x3e910,((256272, 'adjust_secondary_formation_scene'), (256276, 'confirm_secondary_formation_scene')),((256272, 256280), (257244, 257292)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('update_active_battle_controls',0x3e918,((256280, 'update_active_battle_controls'),),((256280, 256284), (257292, 257912)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('latch_scene_controller_inputs',0x3e91c,((256284, 'latch_scene_controller_inputs'),),((256284, 256394),),False,'independent_contiguous_static_return_component'),
    Binding('draw_two_prompt_backgrounds',0x3eae2,((256738, 'draw_two_prompt_backgrounds'),),((256738, 256804),),False,'independent_contiguous_static_return_component'),
    Binding('update_secondary_scene_totals',0x3ecc8,((257224, 'update_secondary_scene_totals'),),((257224, 257244),),False,'independent_contiguous_static_return_component'),
    Binding('begin_transition_prompt',0x3ef86,((257926, 'begin_transition_prompt'),),((257926, 257930), (257934, 258024)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('update_action_mode_prompt',0x3ef8a,((257930, 'update_action_mode_prompt'),),((257930, 257934), (258024, 258082)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('dismiss_action_mode_prompt',0x3f030,((258096, 'dismiss_action_mode_prompt'),),((258096, 258132),),False,'independent_contiguous_static_return_component'),
    Binding('begin_duel_handoff_prompt',0x3f062,((258146, 'begin_duel_handoff_prompt'),),((258146, 258150), (258162, 258258)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('confirm_duel_handoff_prompt',0x3f066,((258150, 'confirm_duel_handoff_prompt'), (258270, 'commit_duel_handoff')),((258150, 258154), (258258, 258410), (258418, 258500)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('await_duel_handoff_palette',0x3f06a,((258154, 'await_duel_handoff_palette'), (258158, 'finish_duel_handoff_phase'), (258546, 'await_result_palette'), (258550, 'finish_result_phase'), (258724, 'await_secondary_result_palette'), (258906, 'await_primary_result_palette')),((258154, 258162), (258508, 258524), (258546, 258554), (258724, 258728), (258906, 258910)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('begin_result_confirmation_prompt',0x3f1ea,((258538, 'begin_result_confirmation_prompt'),),((258538, 258542), (258554, 258650)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('confirm_result_prompt',0x3f1ee,((258542, 'confirm_result_prompt'),),((258542, 258546), (258650, 258702)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('begin_secondary_confirmation_prompt',0x3f29c,((258716, 'begin_secondary_confirmation_prompt'),),((258716, 258720), (258732, 258828)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('confirm_secondary_result_prompt',0x3f2a0,((258720, 'confirm_secondary_result_prompt'), (258728, 'finish_secondary_result_phase')),((258720, 258724), (258728, 258732), (258828, 258880)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('begin_primary_confirmation_prompt',0x3f34e,((258894, 'begin_primary_confirmation_prompt'),),((258894, 258898), (258914, 259016)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('replace_primary_confirmation_prompt',0x3f352,((258898, 'replace_primary_confirmation_prompt'),),((258898, 258902), (259016, 259114)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('confirm_primary_result_prompt',0x3f356,((258902, 'confirm_primary_result_prompt'), (258910, 'finish_primary_result_phase')),((258902, 258906), (258910, 258914), (259114, 259166)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('normalize_secondary_squad_size',0x3f45e,((259166, 'normalize_secondary_squad_size'),),((259166, 259266),),False,'independent_contiguous_static_return_component'),
    Binding('adjust_secondary_squad_count',0x3f518,((259352, 'adjust_secondary_squad_count'),),((259352, 259378),),False,'independent_contiguous_static_return_component'),
    Binding('adjust_selected_squad_class_counts',0x3f532,((259378, 'adjust_selected_squad_class_counts'),),((259378, 259576),),False,'independent_contiguous_static_return_component'),
    Binding('adjust_secondary_formation',0x3f61c,((259612, 'adjust_secondary_formation'), (259656, 'deploy_secondary_formation')),((259612, 259778),),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('adjust_primary_formation',0x3f6c2,((259778, 'adjust_primary_formation'), (259822, 'deploy_primary_formation')),((259778, 259936),),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('adjust_selected_action_mode',0x3f760,((259936, 'adjust_selected_action_mode'),),((259936, 260160), (260164, 260240)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('commit_scene_battle_totals',0x3f8dc,((260316, 'commit_scene_battle_totals'),),((260316, 260342),),False,'independent_contiguous_static_return_component'),
    Binding('draw_secondary_squad_budget',0x3f8f6,((260342, 'draw_secondary_squad_budget'), (260414, 'draw_squad_class_budgets'), (261726, 'draw_battle_summary_numbers'), (261962, 'draw_blinking_decimal_panel'), (261998, 'draw_decimal_panel')),((260342, 260550), (261726, 262054)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('draw_both_force_status_panels',0x3f9c6,((260550, 'draw_both_force_status_panels'), (260658, 'draw_normal_force_status_panel'), (261414, 'draw_special_force_status_panel')),((260550, 261288), (261344, 261726)),False,'complete_static_return_component_with_shared_entries_or_segments'),
    Binding('selected_action_mode_view',0x3fca8,((261288, 'selected_action_mode_view'),),((261288, 261304),),False,'independent_contiguous_static_return_component'),
    Binding('lookup_action_mode_icon_pair',0x3fcb8,((261304, 'lookup_action_mode_icon_pair'),),((261304, 261316),),False,'independent_contiguous_static_return_component'),
)

NEW_BINDINGS=tuple(sorted(DUEL_BINDINGS+ACTIONS_BINDINGS+EARLY_PHASE_BINDINGS+LATE_PHASE_BINDINGS,key=lambda b:b.entry))
REUSED_BINDINGS=()
BINDINGS=NEW_BINDINGS
BY_NAME={b.name:b for b in BINDINGS}
BY_ENTRY={pc:b for b in BINDINGS for pc,name in b.entries}

def validate_binding(binding):
    if type(binding) is not Binding or BY_NAME.get(binding.name)!=binding:
        raise ValueError('declared disjoint physical Binding required')
    if type(binding.entry) is not int or type(binding.entries) is not tuple or type(binding.segments) is not tuple:
        raise ValueError('explicit entry/physical segment tuples required')
    if not binding.entries or not binding.segments or type(binding.reused) is not bool:
        raise ValueError('complete source entry/segment metadata required')
    for start,end in binding.segments:
        if type(start) is not int or type(end) is not int or not 0<=start<end<=0x100000 or start&1 or end&1:
            raise ValueError('valid original even code interval required')
    return binding

NEW_BYTES,REUSED_BYTES,TOTAL_BYTES,INSTRUCTIONS=13132,0,13132,3207
