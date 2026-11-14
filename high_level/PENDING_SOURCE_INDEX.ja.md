# カートリッジのアドレスと Python ソース

[简体中文](PENDING_SOURCE_INDEX.md) · [繁體中文](PENDING_SOURCE_INDEX.zh-TW.md) · **日本語** · [English](PENDING_SOURCE_INDEX.en.md)

アドレスは線形 BIN 上の 16 進数オフセットです。表には元のコード範囲と長さ、呼び出しの入口、対応する Python 関数を記載しています。

| 原版の範囲 / バイト数 | エントリーポイント | Python ソース |
| --- | --- | --- |
| 0305B0 / 884 | 0305B0 | [run_controller_setup_and_configuration_fields](tools/high_level_main_flows/business_scene_support.py#L1883) |
| 00DF6E / 788 | 00DF6E | [draw_diplomacy_parameter_panel_frame_fields](tools/high_level_main_flows/business_commands.py#L4617) |
| 00DF6E / 788 | 030960 | [_diplomacy_first_force_turn_fields](tools/high_level_main_flows/business_commands.py#L4501) |
| 00DF6E / 788 | 06701E | [draw_diplomacy_parameter_panel_alternate_2_frame_fields](tools/high_level_main_flows/business_commands.py#L4671) |
| 03D654 / 548 | 03D654 | [run_scene_object_controller_fields](tools/high_level_scene_flows/business_objects.py#L588) |
| 0003E0 / 466 | 0003E0 | [initialize_title_scene_fields](tools/high_level_main_flows/business_title.py#L232) |
| 0003E0 / 466 | 0003E4 | [initialize_title_scene_preserving_mode_fields](tools/high_level_main_flows/business_title.py#L239) |
| 023610 / 444 | 023610 | [highbank_coordinate_live_state_65_fields](tools/high_level_remaining_flows/business_highbank.py#L15176) |
| 023610 / 444 | 023A6E | [highbank_coordinate_live_state_65_alternate_1_fields](tools/high_level_remaining_flows/business_highbank.py#L15762) |
| 023610 / 444 | 023CBC | [highbank_coordinate_live_state_65_alternate_2_fields](tools/high_level_remaining_flows/business_highbank.py#L15766) |
| 023610 / 444 | 023D9E | [highbank_coordinate_live_state_65_alternate_3_fields](tools/high_level_remaining_flows/business_highbank.py#L15770) |
| 023610 / 444 | 0240BE | [highbank_coordinate_live_state_65_alternate_4_fields](tools/high_level_remaining_flows/business_highbank.py#L15774) |
| 023610 / 444 | 0242EE | [highbank_coordinate_live_state_65_alternate_5_fields](tools/high_level_remaining_flows/business_highbank.py#L15778) |
| 023610 / 444 | 024488 | [highbank_coordinate_live_state_65_alternate_6_fields](tools/high_level_remaining_flows/business_highbank.py#L15782) |
| 023610 / 444 | 0245CC | [highbank_coordinate_live_state_65_alternate_7_fields](tools/high_level_remaining_flows/business_highbank.py#L15786) |
| 023610 / 444 | 0246C8 | [highbank_coordinate_live_state_65_alternate_8_fields](tools/high_level_remaining_flows/business_highbank.py#L15790) |
| 023610 / 444 | 024806 | [highbank_coordinate_live_state_65_alternate_9_fields](tools/high_level_remaining_flows/business_highbank.py#L15794) |
| 023610 / 444 | 024A7A | [highbank_coordinate_live_state_65_alternate_10_fields](tools/high_level_remaining_flows/business_highbank.py#L15798) |
| 01BFEC / 442 | 01BFEC | [settle_city_battle_outcome_fields](tools/high_level_gameplay_flow/business_battle.py#L2252) |
| 00C8B8 / 320 | 00C8B8 | [draw_command_cost_panel_frame_fields](tools/high_level_main_flows/business_commands.py#L4295) |
| 00C8B8 / 320 | 00CD20 | [draw_command_cost_panel_alternate_1_frame_fields](tools/high_level_main_flows/business_commands.py#L4371) |
| 032EA0 / 294 | 032EA0 | [allocate_city_random_funds_fields](tools/high_level_remaining_flows/business_highbank.py#L14327) |
| 032936 / 260 | 032936 | [execute_city_loyalty_change_fields](tools/high_level_remaining_flows/business_highbank.py#L14179) |
| 00A1B2 / 198 | 00A1B2 | [initialize_world_map_view_frame_fields](tools/high_level_main_flows/business_map.py#L1963) |
| 000DC0 / 188 | 000DC0 | [run_battle_scene_round_fields](tools/high_level_gameplay_flow/business_battle.py#L4160) |
| 017602 / 180 | 017602 | [initialize_battle_scene_fields](tools/high_level_gameplay_flow/business_battle.py#L4066) |
| 032DCE / 164 | 032DCE | [execute_city_funds_choice_fields](tools/high_level_remaining_flows/business_highbank.py#L14284) |
| 02777A / 152 | 02777A | [wait_active_duel_action_fields](tools/high_level_scene_flows/business_duel.py#L2986) |
| 02777A / 152 | 0277B8 | [wait_either_duel_action_fields](tools/high_level_scene_flows/business_duel.py#L2992) |
| 0003EC / 150 | 0003EC | [initialize_secondary_title_scene_fields](tools/high_level_main_flows/business_title.py#L307) |
| 01190E / 150 | 01190E | [settle_city_projects_and_refresh_map_fields](tools/high_level_main_flows/business_gameplay.py#L2140) |
| 0173A6 / 128 | 0173A6 | [process_third_calendar_event_fields](tools/high_level_gameplay_flow/business_calendar.py#L402) |
| 0353FC / 124 | 0353FC | [upload_glyph_tile_sequence_fields](tools/high_level_main_flows/business_scene_support.py#L2257) |
| 0353FC / 124 | 035412 | [expand_glyph_tile_sequence_fields](tools/high_level_main_flows/business_scene_support.py#L2317) |
| 0003F0 / 116 | 0003F0 | [initialize_title_transition_scene_fields](tools/high_level_main_flows/business_title.py#L334) |
| 02757A / 116 | 02757A | [perform_duel_feint_fields](tools/high_level_dynamic_flows/business_duel.py#L962) |
| 032FC6 / 108 | 032FC6 | [show_city_funds_graphic_fields](tools/high_level_remaining_flows/business_highbank.py#L14621) |
| 0008E6 / 102 | 0008E6 | [calculate_action_budget_fields](tools/high_level_main_flows/business_main.py#L1671) |
| 00A622 / 92 | 00A622 | [draw_current_scenario_prompt_frame_fields](tools/high_level_main_flows/business_commands.py#L3709) |
| 006950 / 90 | 006950 | [initialize_z80_sound_image_fields](tools/high_level_main_flows/business_lowbank.py#L455) |
| 03B732 / 86 | 03B732 | [run_repeating_scene_presentation_fields](tools/high_level_main_flows/business_scene_support.py#L2504) |
| 0260E4 / 72 | 0260E4 | [present_battle_message_fields](tools/high_level_main_flows/business_movement_support.py#L692) |
| 0004B0 / 70 | 0004B0 | [initialize_post_duel_campaign_fields](tools/high_level_main_flows/business_main.py#L4823) |
| 0003DC / 46 | 0003DC | [reset_menu_sprite_slots_fields](tools/high_level_main_flows/business_main.py#L4509) |
| 034DA2 / 44 | 034DA2 | [load_command_object_status_fields](tools/high_level_remaining_flows/business_highbank.py#L14659) |
| 017058 / 38 | 017058 | [show_calendar_event_message_fields](tools/high_level_gameplay_flow/business_calendar.py#L289) |
| 0356F2 / 30 | 0356F2 | [upload_auxiliary_text_panel_glyphs_fields](tools/high_level_main_flows/business_scene_support.py#L2438) |
| 01A47A / 24 | 01A47A | [city_coordinate_live_state_76_fields](tools/high_level_remaining_flows/business_city.py#L4253) |
| 031A0C / 24 | 031A0C | [dispatch_city_command_policy_fields](tools/high_level_remaining_flows/business_highbank.py#L12393) |
| 0338C2 / 24 | 0338C2 | [dispatch_city_command_stage_fields](tools/high_level_main_flows/business_scene_support.py#L2246) |
| 0340F8 / 24 | 0340F8 | [dispatch_map_packet_command_stage_fields](tools/high_level_main_flows/business_scene_support.py#L2248) |
| 000450 / 22 | 000450 | [initialize_training_screen_fields](tools/high_level_main_flows/business_main.py#L4174) |
| 00045C / 22 | 00045C | [initialize_learning_screen_fields](tools/high_level_main_flows/business_main.py#L4199) |
| 000474 / 22 | 000474 | [initialize_city_transfer_choices_fields](tools/high_level_main_flows/business_main.py#L4252) |
| 000478 / 22 | 000478 | [initialize_officer_search_screen_fields](tools/high_level_main_flows/business_main.py#L4262) |
| 000484 / 22 | 000484 | [initialize_support_command_screen_fields](tools/high_level_main_flows/business_main.py#L4291) |
| 0004A4 / 22 | 0004A4 | [initialize_tactical_selection_scene_fields](tools/high_level_main_flows/business_main.py#L4351) |
| 0004A8 / 22 | 0004A8 | [initialize_battle_scene_fields](tools/high_level_main_flows/business_main.py#L4361) |
| 0004AC / 22 | 0004AC | [initialize_duel_scene_fields](tools/high_level_main_flows/business_main.py#L4371) |
| 0004B8 / 22 | 0004B8 | [initialize_campaign_audio_scene_fields](tools/high_level_main_flows/business_main.py#L4390) |
| 0311E6 / 20 | 0311E6 | [finish_city_command_assignment_fields](tools/high_level_main_flows/business_scene_support.py#L2150) |
| 03DCC6 / 18 | 03DCC6 | [step_result_scene_phase_fields](tools/high_level_dynamic_flows/business_early_phase.py#L1645) |
| 0004B4 / 16 | 0004B4 | [begin_nonreturning_scripted_scene_fields](tools/high_level_main_flows/business_main.py#L4381) |
| 0003F4 / 12 | 0003F4 | [refresh_information_panel_fields](tools/high_level_main_flows/business_main.py#L4113) |
| 000404 / 12 | 000404 | [initialize_campaign_options_fields](tools/high_level_main_flows/business_main.py#L4126) |
| 000418 / 12 | 000418 | [initialize_city_detail_panel_fields](tools/high_level_main_flows/business_main.py#L4140) |
| 000458 / 12 | 000458 | [update_training_candidate_fields](tools/high_level_main_flows/business_main.py#L4192) |
| 000468 / 12 | 000468 | [update_officer_transfer_candidate_fields](tools/high_level_main_flows/business_main.py#L4226) |
| 002E8C / 8 | 002E8C | [lowbank_coordinate_live_state_27_fields](tools/high_level_remaining_flows/business_lowbank.py#L9763) |
| 002E94 / 8 | 002E94 | [lowbank_coordinate_live_state_28_fields](tools/high_level_remaining_flows/business_lowbank.py#L9767) |
| 010A3C / 8 | 010A3C | [lowbank_coordinate_live_state_116_fields](tools/high_level_remaining_flows/business_lowbank.py#L8039) |
| 010A44 / 8 | 010A44 | [lowbank_coordinate_live_state_117_fields](tools/high_level_remaining_flows/business_lowbank.py#L8043) |
| 03100C / 8 | 03100C | [open_command_phase_dispatch_fields](tools/high_level_remaining_flows/business_highbank.py#L14047) |
| 031014 / 8 | 031014 | [open_assignment_menu_dispatch_fields](tools/high_level_remaining_flows/business_highbank.py#L14054) |
| 00049C / 6 | 00049C | [return_campaign_idle_slot_fields](tools/high_level_main_flows/business_main.py#L4337) |
| 000498 / 4 | 000498 | [continue_campaign_action_display_fields](tools/high_level_main_flows/business_main.py#L4331) |
