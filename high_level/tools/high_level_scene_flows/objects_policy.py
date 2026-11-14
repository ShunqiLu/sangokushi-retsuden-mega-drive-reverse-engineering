"""Finite source-driven lowering of the complete scene-object lifecycle family.

Eighteen physical owners retain their original spans, call allocation, WORD and
BYTE partial writes, live waits and nonlocal continuation. Named role values
come from the complete supplied business source; no original/source/IR/object
fallback exists here. Resource layout, dynamic target domain, IRQ/full CPU and
unregistered structural changes are deliberately not inferred.
"""
from __future__ import annotations

from .compiler_common import CompileError
from .policy_common import SourceRole as MenuRole


ROLE_SPECS = (
    MenuRole('object_coordinate_fraction_shift', 'integrate_scene_coordinates', (('body', 1, 'body', 3, 'body', 0, 'value', 'right'), ('body', 1, 'body', 3, 'orelse', 0, 'value', 'right')),
        'shift', 8, (252156, 252164, 252202, 252210, 252248, 252256),
        coupled_uses=()),
    MenuRole('object_progress_budget_shift', 'distribute_secondary_city_battle_progress', (('body', 3, 'value', 'args', 0, 'right'),),
        'shift', 1, (116202,),
        coupled_uses=()),
    MenuRole('object_squad_count_cap', '_normalize_object_squad_fields', (('body', 1, 'body', 2, 'orelse', 0, 'test', 'comparators', 0),),
        'word', 15, (259288,),
        coupled_uses=()),
    MenuRole('object_squad_upper_size', '_normalize_object_squad_fields', (('body', 1, 'body', 2, 'orelse', 0, 'orelse', 2, 'test', 'comparators', 0),),
        'word', 1000, (259304,),
        coupled_uses=()),
    MenuRole('object_squad_lower_size', '_normalize_object_squad_fields', (('body', 1, 'body', 2, 'orelse', 0, 'orelse', 2, 'orelse', 0, 'test', 'values', 0, 'comparators', 0),),
        'word', 100, (259318,),
        coupled_uses=()),
    MenuRole('object_squad_decrease_floor', '_normalize_object_squad_fields', (('body', 1, 'body', 2, 'orelse', 0, 'orelse', 2, 'orelse', 0, 'test', 'values', 1, 'comparators', 0),),
        'word', 1, (259326,),
        coupled_uses=()),
    MenuRole('object_squad_increase_step', '_normalize_object_squad_fields', (('body', 1, 'body', 2, 'body', 0, 'value', 'args', 1, 'args', 0, 'right'), ('body', 1, 'body', 2, 'orelse', 0, 'orelse', 2, 'body', 0, 'value', 'args', 1, 'args', 0, 'right')),
        'quick', 1, (259282, 259312),
        coupled_uses=()),
    MenuRole('object_squad_decrease_step', '_normalize_object_squad_fields', (('body', 1, 'body', 2, 'orelse', 0, 'body', 0, 'value', 'args', 1, 'args', 0, 'right'), ('body', 1, 'body', 2, 'orelse', 0, 'orelse', 2, 'orelse', 0, 'body', 0, 'value', 'args', 1, 'args', 0, 'right')),
        'quick', 1, (259296, 259334),
        coupled_uses=()),
    MenuRole('object_squad_cap_relation', '_normalize_object_squad_fields', (('body', 1, 'body', 2, 'orelse', 0, 'test', 'ops', 0),),
        'unsigned_relation', '>', (259292,),
        coupled_uses=()),
    MenuRole('object_squad_upper_relation', '_normalize_object_squad_fields', (('body', 1, 'body', 2, 'orelse', 0, 'orelse', 2, 'test', 'ops', 0),),
        'unsigned_relation', '>', (259308,),
        coupled_uses=()),
    MenuRole('object_squad_lower_relation', '_normalize_object_squad_fields', (('body', 1, 'body', 2, 'orelse', 0, 'orelse', 2, 'orelse', 0, 'test', 'values', 0, 'ops', 0),),
        'unsigned_relation', '<=', (259322,),
        coupled_uses=()),
    MenuRole('object_squad_floor_relation', '_normalize_object_squad_fields', (('body', 1, 'body', 2, 'orelse', 0, 'orelse', 2, 'orelse', 0, 'test', 'values', 1, 'ops', 0),),
        'unsigned_relation', '>', (259332,),
        coupled_uses=()),
    MenuRole('object_palette_tick_shift', 'cycle_special_scene_palette_complete', (('body', 7, 'value', 'left', 'right'),),
        'shift', 3, (260260,),
        coupled_uses=()),
    MenuRole('object_label_fill_tile', 'clear_scene_object_label_plane_complete', (('body', 2, 'body', 0, 'value', 'args', 2), ('body', 3, 'value', 'keywords', 1, 'value', 'args', 1), ('body', 3, 'value', 'keywords', 3, 'value', 'args', 0)),
        'word', 1024, (262956,),
        coupled_uses=()),
    MenuRole('object_sprite_capacity', '_append_sprite_entries_complete', (('body', 13, 'test', 'comparators', 0), ('body', 26, 'body', 23, 'test', 'comparators', 0), ('body', 12, 'value', 'args', 1), ('body', 26, 'body', 22, 'value', 'args', 1)),
        'byte', 80, (241984, 242220),
        coupled_uses=()),
    MenuRole('object_sprite_x_origin_bias', '_append_sprite_entries_complete', (('body', 18, 'value', 'args', 1, 'args', 0, 'right'), ('body', 19, 'body', 0, 'value', 'args', 0, 'args', 0, 'right'), ('body', 19, 'body', 0, 'value', 'args', 1)),
        'word', 128, (242016,),
        coupled_uses=()),
    MenuRole('object_sprite_y_origin_bias', '_append_sprite_entries_complete', (('body', 21, 'value', 'args', 1, 'args', 0, 'right'),),
        'word', 128, (242038,),
        coupled_uses=()),
    MenuRole('object_sprite_x_flip_correction', '_append_sprite_entries_complete', (('body', 20, 'body', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'word', 8, (242030,),
        coupled_uses=()),
    MenuRole('object_sprite_y_flip_correction', '_append_sprite_entries_complete', (('body', 22, 'body', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'word', 8, (242048,),
        coupled_uses=()),
    MenuRole('object_sprite_count_step', '_append_sprite_entries_complete', (('body', 26, 'body', 12, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (242188,),
        coupled_uses=()),
    MenuRole('object_center_marker_x_offset', 'append_scene_center_marker_complete', (('body', 1, 'value', 'keywords', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'word', 64, (242316,),
        coupled_uses=()),
    MenuRole('object_center_marker_y_offset', 'append_scene_center_marker_complete', (('body', 1, 'value', 'keywords', 1, 'value', 'args', 1, 'args', 0, 'right'),),
        'word', 64, (242324,),
        coupled_uses=()),
    MenuRole('object_animation_side_bias', 'draw_active_scene_object_complete', (('body', 7, 'body', 0, 'body', 0, 'value', 'args', 0, 'right'), ('body', 7, 'orelse', 0, 'body', 0, 'value', 'args', 0, 'right')),
        'word', 96, (263294, 263310),
        coupled_uses=()),
    MenuRole('object_animation_phase_shift', 'draw_active_scene_object_complete', (('body', 8, 'value', 'args', 0, 'right', 'args', 0, 'right'),),
        'shift', 2, (263318,),
        coupled_uses=()),
    MenuRole('object_animation_tick_shift', 'draw_active_scene_object_complete', (('body', 9, 'value', 'args', 0, 'left', 'left', 'right'),),
        'shift', 3, (263326,),
        coupled_uses=()),
    MenuRole('object_animation_tick_mask', 'draw_active_scene_object_complete', (('body', 9, 'value', 'args', 0, 'left', 'right'),),
        'word', 3, (263328,),
        coupled_uses=()),
    MenuRole('object_animation_attributes', 'draw_active_scene_object_complete', (('body', 17, 'value', 'keywords', 2, 'value', 'args', 1),),
        'word', 5, (263350,),
        coupled_uses=()),
    MenuRole('object_offset_negative_magnitude_mask', 'offset_scene_object_position_complete', (('body', 2, 'body', 2, 'body', 0, 'value'),),
        'word', 127, (266664, 266684),
        coupled_uses=()),
    MenuRole('object_overlap_horizontal_relation', 'probe_scene_object_overlap_complete', (('body', 7, 'body', 0, 'body', 2, 'test', 'ops', 0),),
        'unsigned_relation', '==', (266620,),
        coupled_uses=()),
    MenuRole('object_overlap_vertical_relation', 'probe_scene_object_overlap_complete', (('body', 7, 'body', 0, 'body', 2, 'body', 2, 'test', 'ops', 0),),
        'unsigned_relation', '==', (266630,),
        coupled_uses=()),
    MenuRole('object_queue_tick_mask', 'rebuild_depth_sorted_object_queue_complete', (('body', 1, 'value', 'right'),),
        'word', 15, (263182,),
        coupled_uses=()),
    MenuRole('object_queue_maximum_depth', 'rebuild_depth_sorted_object_queue_complete', (('body', 5, 'iter', 'args', 0),),
        'moveq', 30, (263194,),
        coupled_uses=()),
    MenuRole('object_queue_depth_shift', 'rebuild_depth_sorted_object_queue_complete', (('body', 5, 'body', 1, 'body', 0, 'body', 0, 'value', 'right'),),
        'shift', 4, (263210,),
        coupled_uses=()),
    MenuRole('object_queue_depth_relation', 'rebuild_depth_sorted_object_queue_complete', (('body', 5, 'body', 1, 'body', 0, 'body', 2, 'test', 'ops', 0),),
        'unsigned_relation', '==', (263214,),
        coupled_uses=()),
    MenuRole('object_action_timer_step', 'advance_scene_object_actions_complete', (('body', 13, 'value', 'args', 0, 'right'), ('body', 15, 'value', 'keywords', 0, 'value', 'args', 1)),
        'quick', 1, (263048,),
        coupled_uses=()),
    MenuRole('object_action_slot_step', 'advance_scene_object_actions_complete', (('body', 17, 'body', 0, 'value', 'args', 0, 'right'),),
        'quick', 1, (263056,),
        coupled_uses=()),
    MenuRole('object_action_slot_bound', 'advance_scene_object_actions_complete', (('body', 17, 'body', 2, 'test', 'comparators', 0),),
        'word', 16, (263060,),
        coupled_uses=()),
    MenuRole('object_action_slot_relation', 'advance_scene_object_actions_complete', (('body', 17, 'body', 2, 'test', 'ops', 0),),
        'unsigned_relation', '>=', (263066,),
        coupled_uses=()),
    MenuRole('object_action_class_step', 'advance_scene_object_actions_complete', (('body', 17, 'body', 2, 'body', 1, 'value', 'args', 0, 'right'),),
        'quick', 1, (263126,),
        coupled_uses=()),
    MenuRole('object_action_class_bound', 'advance_scene_object_actions_complete', (('body', 17, 'body', 2, 'body', 3, 'test', 'comparators', 0),),
        'word', 4, (263130,),
        coupled_uses=()),
    MenuRole('object_action_class_relation', 'advance_scene_object_actions_complete', (('body', 17, 'body', 2, 'body', 3, 'test', 'ops', 0),),
        'unsigned_relation', '>=', (263136,),
        coupled_uses=()),
    MenuRole('object_action_side_step', 'advance_scene_object_actions_complete', (('body', 17, 'body', 2, 'body', 3, 'body', 1, 'value', 'args', 0, 'right'),),
        'quick', 1, (263142,),
        coupled_uses=()),
    MenuRole('object_action_side_bound', 'advance_scene_object_actions_complete', (('body', 17, 'body', 2, 'body', 3, 'body', 3, 'test', 'comparators', 0),),
        'word', 3, (263146,),
        coupled_uses=()),
    MenuRole('object_action_side_relation', 'advance_scene_object_actions_complete', (('body', 17, 'body', 2, 'body', 3, 'body', 3, 'test', 'ops', 0),),
        'unsigned_relation', '>=', (263152,),
        coupled_uses=()),
    MenuRole('object_action_slow_class_bound', 'advance_scene_object_actions_complete', (('body', 20, 'test', 'comparators', 0), ('body', 20, 'orelse', 0, 'value', 'args', 1)),
        'word', 2, (263162,),
        coupled_uses=()),
    MenuRole('object_action_slow_class_relation', 'advance_scene_object_actions_complete', (('body', 20, 'test', 'ops', 0),),
        'unsigned_relation', '>=', (263168,),
        coupled_uses=()),
    MenuRole('object_action_slow_timer', 'advance_scene_object_actions_complete', (('body', 20, 'body', 0, 'value', 'args', 1), ('body', 20, 'body', 1, 'value', 'args', 0)),
        'word', 1, (263170,),
        coupled_uses=()),
    MenuRole('object_action_matching_class_relation', 'advance_scene_object_actions_complete', (('body', 17, 'body', 11, 'test', 'ops', 0),),
        'unsigned_relation', '==', (263114,),
        coupled_uses=()),
    MenuRole('object_selection_x_limit', '_select_scene_object_action_complete', (('body', 17, 'orelse', 3, 'test', 'comparators', 0), ('body', 17, 'orelse', 2, 'value', 'keywords', 0, 'value', 'args', 1)),
        'word', 512, (265446,),
        coupled_uses=()),
    MenuRole('object_selection_x_relation', '_select_scene_object_action_complete', (('body', 17, 'orelse', 3, 'test', 'ops', 0),),
        'unsigned_relation', '>=', (265452,),
        coupled_uses=()),
    MenuRole('object_selection_random_mask', '_select_scene_object_action_complete', (('body', 17, 'orelse', 6, 'value', 'args', 1, 'right'),),
        'word', 3, (265460,),
        coupled_uses=()),
    MenuRole('object_selection_plan_relation', '_select_scene_object_action_complete', (('body', 17, 'orelse', 8, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (265464,),
        coupled_uses=()),
    MenuRole('object_video_row_stride', 'initialize_scene_object_video_complete', (('body', 4, 'body', 3, 'value', 'keywords', 3, 'value'), ('body', 4, 'body', 3, 'value', 'keywords', 4, 'value', 'args', 0)),
        'long', 128, (252518, 252552, 252580, 252608),
        coupled_uses=()),
    MenuRole('object_plan_long_range_mode', 'plan_scene_object_action_complete', (('body', 10, 'test', 'comparators', 0), ('body', 6, 'value', 'keywords', 2, 'value', 'args', 1)),
        'word', 6, (266724, 266850),
        coupled_uses=()),
    MenuRole('object_plan_long_mode_relation', 'plan_scene_object_action_complete', (('body', 10, 'test', 'ops', 0),),
        'unsigned_relation', '==', (266730, 266856),
        coupled_uses=()),
    MenuRole('object_plan_long_range_member', 'plan_scene_object_action_complete', (('body', 10, 'body', 4, 'test', 'comparators', 0), ('body', 13, 'test', 'comparators', 0), ('body', 10, 'body', 4, 'body', 0, 'value', 'args', 0, 'keywords', 0, 'value', 'args', 1), ('body', 13, 'body', 0, 'value', 'args', 0, 'keywords', 0, 'value', 'args', 1)),
        'byte', 1, (266764, 266890, 267090),
        coupled_uses=()),
    MenuRole('object_plan_member_relation', 'plan_scene_object_action_complete', (('body', 10, 'body', 4, 'test', 'ops', 0), ('body', 13, 'test', 'ops', 0)),
        'unsigned_relation', '!=', (266770, 266896, 267096),
        coupled_uses=()),
    MenuRole('object_plan_mode_short_positive', 'plan_scene_object_action_complete', (('body', 10, 'body', 0, 'value', 'body'),),
        'word', 16, (266746,),
        coupled_uses=()),
    MenuRole('object_plan_mode_short_negative', 'plan_scene_object_action_complete', (('body', 10, 'body', 0, 'value', 'orelse'),),
        'word', 32784, (266872,),
        coupled_uses=()),
    MenuRole('object_plan_mode_long_distance_0', 'plan_scene_object_action_complete', (('body', 10, 'body', 6, 'iter', 'elts', 0, 'elts', 0),),
        'word', 32, (266786, 266912),
        coupled_uses=()),
    MenuRole('object_plan_mode_long_distance_1', 'plan_scene_object_action_complete', (('body', 10, 'body', 6, 'iter', 'elts', 1, 'elts', 0),),
        'word', 48, (266804, 266930),
        coupled_uses=()),
    MenuRole('object_plan_mode_long_distance_2', 'plan_scene_object_action_complete', (('body', 10, 'body', 6, 'iter', 'elts', 2, 'elts', 0),),
        'word', 64, (266822, 266948),
        coupled_uses=()),
    MenuRole('object_plan_short_west', 'plan_scene_object_action_complete', (('body', 11, 'iter', 'elts', 0, 'elts', 2),),
        'word', 32784, (266982,),
        coupled_uses=()),
    MenuRole('object_plan_short_east', 'plan_scene_object_action_complete', (('body', 11, 'iter', 'elts', 1, 'elts', 2),),
        'word', 16, (267012,),
        coupled_uses=()),
    MenuRole('object_plan_short_south', 'plan_scene_object_action_complete', (('body', 11, 'iter', 'elts', 2, 'elts', 3),),
        'word', 16, (267046,),
        coupled_uses=()),
    MenuRole('object_plan_short_north', 'plan_scene_object_action_complete', (('body', 11, 'iter', 'elts', 3, 'elts', 3),),
        'word', 32784, (267076,),
        coupled_uses=()),
    MenuRole('object_plan_long_west_0', 'plan_scene_object_action_complete', (('body', 14, 'iter', 'elts', 0, 'elts', 2, 'elts', 0, 'elts', 0),),
        'word', 32800, (267112,),
        coupled_uses=()),
    MenuRole('object_plan_long_west_1', 'plan_scene_object_action_complete', (('body', 14, 'iter', 'elts', 0, 'elts', 2, 'elts', 1, 'elts', 0),),
        'word', 32816, (267130,),
        coupled_uses=()),
    MenuRole('object_plan_long_west_2', 'plan_scene_object_action_complete', (('body', 14, 'iter', 'elts', 0, 'elts', 2, 'elts', 2, 'elts', 0),),
        'word', 32832, (267148,),
        coupled_uses=()),
    MenuRole('object_plan_long_east_0', 'plan_scene_object_action_complete', (('body', 14, 'iter', 'elts', 1, 'elts', 2, 'elts', 0, 'elts', 0),),
        'word', 32, (267178,),
        coupled_uses=()),
    MenuRole('object_plan_long_east_1', 'plan_scene_object_action_complete', (('body', 14, 'iter', 'elts', 1, 'elts', 2, 'elts', 1, 'elts', 0),),
        'word', 48, (267196,),
        coupled_uses=()),
    MenuRole('object_plan_long_east_2', 'plan_scene_object_action_complete', (('body', 14, 'iter', 'elts', 1, 'elts', 2, 'elts', 2, 'elts', 0),),
        'word', 64, (267214,),
        coupled_uses=()),
    MenuRole('object_plan_long_south_0', 'plan_scene_object_action_complete', (('body', 14, 'iter', 'elts', 2, 'elts', 2, 'elts', 0, 'elts', 1),),
        'word', 32, (267248,),
        coupled_uses=()),
    MenuRole('object_plan_long_south_1', 'plan_scene_object_action_complete', (('body', 14, 'iter', 'elts', 2, 'elts', 2, 'elts', 1, 'elts', 1),),
        'word', 3, (267266,),
        coupled_uses=()),
    MenuRole('object_plan_long_south_2', 'plan_scene_object_action_complete', (('body', 14, 'iter', 'elts', 2, 'elts', 2, 'elts', 2, 'elts', 1),),
        'word', 64, (267284,),
        coupled_uses=()),
    MenuRole('object_plan_long_north_0', 'plan_scene_object_action_complete', (('body', 14, 'iter', 'elts', 3, 'elts', 2, 'elts', 0, 'elts', 1),),
        'word', 32800, (267314,),
        coupled_uses=()),
    MenuRole('object_plan_long_north_1', 'plan_scene_object_action_complete', (('body', 14, 'iter', 'elts', 3, 'elts', 2, 'elts', 1, 'elts', 1),),
        'word', 32816, (267332,),
        coupled_uses=()),
    MenuRole('object_plan_long_north_2', 'plan_scene_object_action_complete', (('body', 14, 'iter', 'elts', 3, 'elts', 2, 'elts', 2, 'elts', 1),),
        'word', 32832, (267350,),
        coupled_uses=()),
    MenuRole('object_plan_short_sound', 'plan_scene_object_action_complete', (('body', 9, 'body', 9, 'value', 'args', 1, 'orelse'),),
        'byte', 167, (267504,),
        coupled_uses=()),
    MenuRole('object_plan_long_sound', 'plan_scene_object_action_complete', (('body', 9, 'body', 9, 'value', 'args', 1, 'body'),),
        'byte', 162, (267404,),
        coupled_uses=()),
    MenuRole('object_roster_initial_count', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 0, 'value', 'args', 1),),
        'word', 1, (268336,),
        coupled_uses=()),
    MenuRole('object_roster_troop_minimum', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 1, 'test', 'comparators', 0),),
        'word', 100, (268342,),
        coupled_uses=()),
    MenuRole('object_roster_small_troop_bound', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 1, 'body', 0, 'test', 'comparators', 0),),
        'word', 1500, (268352,),
        coupled_uses=()),
    MenuRole('object_roster_medium_troop_bound', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 1, 'body', 0, 'orelse', 0, 'test', 'comparators', 0),),
        'word', 5000, (268384,),
        coupled_uses=()),
    MenuRole('object_roster_large_troop_bound', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 1, 'body', 0, 'orelse', 0, 'orelse', 1, 'test', 'comparators', 0),),
        'word', 10000, (268422,),
        coupled_uses=()),
    MenuRole('object_roster_maximum_count', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 1, 'body', 0, 'orelse', 0, 'orelse', 0, 'value', 'args', 1),),
        'word', 15, (268416,),
        coupled_uses=()),
    MenuRole('object_roster_minimum_relation', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 1, 'test', 'ops', 0),),
        'unsigned_relation', '>=', (268348,),
        coupled_uses=()),
    MenuRole('object_roster_small_relation', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 1, 'body', 0, 'test', 'ops', 0),),
        'unsigned_relation', '<', (268358,),
        coupled_uses=()),
    MenuRole('object_roster_medium_relation', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 1, 'body', 0, 'orelse', 0, 'test', 'ops', 0),),
        'unsigned_relation', '<', (268390,),
        coupled_uses=()),
    MenuRole('object_roster_large_relation', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 1, 'body', 0, 'orelse', 0, 'orelse', 1, 'test', 'ops', 0),),
        'unsigned_relation', '<', (268428,),
        coupled_uses=()),
    MenuRole('object_roster_count_random_mask', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 1, 'body', 0, 'body', 0, 'body', 1, 'value', 'right'), ('body', 7, 'body', 1, 'body', 0, 'orelse', 0, 'body', 0, 'body', 1, 'value', 'right'), ('body', 7, 'body', 1, 'body', 0, 'orelse', 0, 'orelse', 1, 'body', 0, 'body', 1, 'value', 'right')),
        'word', 15, (268364, 268396, 268434),
        coupled_uses=()),
    MenuRole('object_roster_small_random_bound', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 1, 'body', 0, 'body', 0, 'body', 3, 'test', 'comparators', 0),),
        'word', 9, (268368,),
        coupled_uses=()),
    MenuRole('object_roster_other_random_bound', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 1, 'body', 0, 'orelse', 0, 'body', 0, 'body', 3, 'test', 'comparators', 0), ('body', 7, 'body', 1, 'body', 0, 'orelse', 0, 'orelse', 1, 'body', 0, 'body', 3, 'test', 'comparators', 0)),
        'word', 5, (268400, 268438),
        coupled_uses=()),
    MenuRole('object_roster_small_accept_relation', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 1, 'body', 0, 'body', 0, 'body', 3, 'test', 'ops', 0),),
        'unsigned_relation', '<=', (268372,),
        coupled_uses=()),
    MenuRole('object_roster_other_accept_relation', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 1, 'body', 0, 'orelse', 0, 'body', 0, 'body', 3, 'test', 'ops', 0), ('body', 7, 'body', 1, 'body', 0, 'orelse', 0, 'orelse', 1, 'body', 0, 'body', 3, 'test', 'ops', 0)),
        'unsigned_relation', '<=', (268404, 268442),
        coupled_uses=()),
    MenuRole('object_roster_small_count_bias', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 1, 'body', 0, 'body', 1, 'value', 'keywords', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (268374,),
        coupled_uses=()),
    MenuRole('object_roster_medium_count_bias', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 1, 'body', 0, 'orelse', 0, 'body', 1, 'value', 'keywords', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 5, (268406,),
        coupled_uses=()),
    MenuRole('object_roster_large_count_bias', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 1, 'body', 0, 'orelse', 0, 'orelse', 1, 'body', 1, 'value', 'keywords', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'word', 10, (268444,),
        coupled_uses=()),
    MenuRole('object_roster_partition_0_quality', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'iter', 'elts', 0, 'elts', 0),),
        'word', 100, (268464,),
        coupled_uses=()),
    MenuRole('object_roster_partition_0_first_count', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'iter', 'elts', 0, 'elts', 1), ('body', 7, 'body', 3, 'value', 'elts', 0)),
        'moveq', 0, (268460,),
        coupled_uses=()),
    MenuRole('object_roster_partition_0_second_count', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'iter', 'elts', 0, 'elts', 2), ('body', 7, 'body', 3, 'value', 'elts', 1)),
        'moveq', 2, (268462,),
        coupled_uses=()),
    MenuRole('object_roster_partition_1_quality', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'iter', 'elts', 1, 'elts', 0),),
        'word', 200, (268478,),
        coupled_uses=()),
    MenuRole('object_roster_partition_1_first_count', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'iter', 'elts', 1, 'elts', 1),),
        'moveq', 1, (268474,),
        coupled_uses=()),
    MenuRole('object_roster_partition_1_second_count', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'iter', 'elts', 1, 'elts', 2),),
        'moveq', 3, (268476,),
        coupled_uses=()),
    MenuRole('object_roster_partition_2_quality', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'iter', 'elts', 2, 'elts', 0),),
        'word', 300, (268492,),
        coupled_uses=()),
    MenuRole('object_roster_partition_2_first_count', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'iter', 'elts', 2, 'elts', 1),),
        'moveq', 3, (268488,),
        coupled_uses=()),
    MenuRole('object_roster_partition_2_second_count', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'iter', 'elts', 2, 'elts', 2),),
        'moveq', 4, (268490,),
        coupled_uses=()),
    MenuRole('object_roster_partition_3_quality', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'iter', 'elts', 3, 'elts', 0),),
        'word', 400, (268506,),
        coupled_uses=()),
    MenuRole('object_roster_partition_3_first_count', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'iter', 'elts', 3, 'elts', 1),),
        'moveq', 5, (268502,),
        coupled_uses=()),
    MenuRole('object_roster_partition_3_second_count', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'iter', 'elts', 3, 'elts', 2),),
        'moveq', 5, (268504,),
        coupled_uses=()),
    MenuRole('object_roster_partition_4_quality', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'iter', 'elts', 4, 'elts', 0),),
        'word', 500, (268520,),
        coupled_uses=()),
    MenuRole('object_roster_partition_4_first_count', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'iter', 'elts', 4, 'elts', 1),),
        'moveq', 6, (268516,),
        coupled_uses=()),
    MenuRole('object_roster_partition_4_second_count', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'iter', 'elts', 4, 'elts', 2),),
        'moveq', 6, (268518,),
        coupled_uses=()),
    MenuRole('object_roster_partition_5_quality', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'iter', 'elts', 5, 'elts', 0),),
        'word', 600, (268534,),
        coupled_uses=()),
    MenuRole('object_roster_partition_5_first_count', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'iter', 'elts', 5, 'elts', 1),),
        'moveq', 7, (268530,),
        coupled_uses=()),
    MenuRole('object_roster_partition_5_second_count', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'iter', 'elts', 5, 'elts', 2),),
        'moveq', 7, (268532,),
        coupled_uses=()),
    MenuRole('object_roster_partition_relation', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'body', 1, 'test', 'ops', 0),),
        'unsigned_relation', '<=', (268470, 268484, 268498, 268512, 268526, 268540),
        coupled_uses=()),
    MenuRole('object_roster_partition_last_0', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'orelse', 0, 'value', 'elts', 0),),
        'moveq', 8, (268544,),
        coupled_uses=()),
    MenuRole('object_roster_partition_last_1', 'initialize_scene_object_roster_complete', (('body', 7, 'body', 4, 'orelse', 0, 'value', 'elts', 1),),
        'moveq', 8, (268546,),
        coupled_uses=()),
    MenuRole('object_roster_layout_random_mask', 'initialize_scene_object_roster_complete', (('body', 8, 'body', 1, 'value', 'right'),),
        'word', 7, (268622,),
        coupled_uses=()),
    MenuRole('object_roster_layout_bound', 'initialize_scene_object_roster_complete', (('body', 8, 'body', 3, 'test', 'comparators', 0),),
        'word', 4, (268626,),
        coupled_uses=()),
    MenuRole('object_roster_layout_relation', 'initialize_scene_object_roster_complete', (('body', 8, 'body', 3, 'test', 'ops', 0),),
        'unsigned_relation', '<=', (268630,),
        coupled_uses=()),
    MenuRole('object_roster_member_consume_step', 'initialize_scene_object_roster_complete', (('body', 18, 'body', 0, 'orelse', 0, 'body', 0, 'value', 'elts', 1, 'args', 0, 'right'), ('body', 18, 'body', 0, 'orelse', 0, 'orelse', 0, 'body', 0, 'value', 'elts', 1, 'args', 0, 'right'), ('body', 18, 'body', 0, 'orelse', 0, 'orelse', 0, 'orelse', 0, 'body', 0, 'value', 'elts', 1, 'args', 0, 'right')),
        'quick', 1, (268700, 268720, 268736),
        coupled_uses=()),
    MenuRole('object_roster_member_counter_step', 'initialize_scene_object_roster_complete', (('body', 18, 'body', 4, 'value', 'args', 0, 'right'),),
        'quick', 1, (268742,),
        coupled_uses=()),
    MenuRole('object_roster_quality_divisor', 'initialize_scene_object_roster_complete', (('body', 21, 'value', 'args', 1),),
        'nonzero_word', 100, (268762,),
        coupled_uses=()),
    MenuRole('object_roster_remainder_consume_step', 'initialize_scene_object_roster_complete', (('body', 24, 'body', 2, 'body', 0, 'value', 'args', 0, 'right'),),
        'quick', 1, (268794,),
        coupled_uses=()),
    MenuRole('object_roster_remainder_spread_step', 'initialize_scene_object_roster_complete', (('body', 24, 'body', 2, 'body', 1, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (268796,),
        coupled_uses=()),
    MenuRole('object_controller_video_mask', '_scene_video_command', (('body', 1, 'value', 'args', 1, 'right'),),
        'byte', 191, (251484, 251966, 252008, 252044, 252086),
        coupled_uses=()),
    MenuRole('object_controller_palette_start_shade', 'run_scene_object_controller_complete', (('body', 3, 'body', 10, 'value', 'keywords', 0, 'value'), ('body', 3, 'body', 10, 'value', 'keywords', 1, 'value', 'args', 0)),
        'moveq', 1, (251544,),
        coupled_uses=()),
    MenuRole('object_controller_default_action_mode', 'run_scene_object_controller_complete', (('body', 3, 'body', 15, 'orelse', 5, 'body', 0, 'value', 'args', 1),),
        'word', 5, (251694, 251700, 251706, 251712, 251718, 251724, 251730, 251736),
        coupled_uses=()),
    MenuRole('object_controller_start_sound', 'run_scene_object_controller_complete', (('body', 3, 'body', 17, 'value', 'args', 1), ('body', 3, 'body', 18, 'value', 'keywords', 1, 'value', 'args', 0)),
        'byte', 142, (251872,),
        coupled_uses=()),
    MenuRole('object_controller_restart_mask', 'run_scene_object_controller_complete', (('body', 3, 'body', 21, 'body', 22, 'value', 'args', 1, 'right'), ('body', 3, 'body', 21, 'body', 24, 'test', 'comparators', 0), ('body', 3, 'body', 21, 'body', 23, 'value', 'keywords', 1, 'value', 'args', 1)),
        'byte', 240, (252102, 252106),
        coupled_uses=()),
    MenuRole('object_controller_restart_relation', 'run_scene_object_controller_complete', (('body', 3, 'body', 21, 'body', 24, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (252110,),
        coupled_uses=()),
    MenuRole('object_controller_variant_bound', 'run_scene_object_controller_complete', (('body', 3, 'body', 21, 'body', 25, 'test', 'comparators', 0),),
        'byte', 3, (252114,),
        coupled_uses=()),
    MenuRole('object_controller_variant_relation', 'run_scene_object_controller_complete', (('body', 3, 'body', 21, 'body', 25, 'test', 'ops', 0),),
        'unsigned_relation', '<', (252120,),
        coupled_uses=()),
    MenuRole('object_controller_variant_step', 'run_scene_object_controller_complete', (('body', 3, 'body', 21, 'body', 25, 'body', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (252124,),
        coupled_uses=()),
    MenuRole('object_controller_terminal_phase_relation_0', 'run_scene_object_controller_complete', (('body', 3, 'body', 21, 'body', 16, 'test', 'ops', 0),),
        'unsigned_relation', '==', (251942,),
        coupled_uses=()),
    MenuRole('object_controller_terminal_phase_relation_1', 'run_scene_object_controller_complete', (('body', 3, 'body', 21, 'body', 17, 'test', 'values', 1, 'ops', 0),),
        'unsigned_relation', '==', (251984,),
        coupled_uses=()),
    MenuRole('object_controller_terminal_phase_relation_2', 'run_scene_object_controller_complete', (('body', 3, 'body', 21, 'body', 18, 'test', 'values', 1, 'ops', 0),),
        'unsigned_relation', '==', (252026,),
        coupled_uses=()),
    MenuRole('object_controller_terminal_phase_relation_3', 'run_scene_object_controller_complete', (('body', 3, 'body', 21, 'body', 19, 'test', 'values', 1, 'ops', 0),),
        'unsigned_relation', '==', (252062,),
        coupled_uses=()),
    MenuRole('object_controller_terminal_subphase_relation_0', 'run_scene_object_controller_complete', (('body', 3, 'body', 21, 'body', 16, 'body', 0, 'test', 'ops', 0),),
        'unsigned_relation', '==', (251950,),
        coupled_uses=()),
    MenuRole('object_controller_terminal_subphase_relation_1', 'run_scene_object_controller_complete', (('body', 3, 'body', 21, 'body', 17, 'body', 0, 'test', 'ops', 0),),
        'unsigned_relation', '==', (251992,),
        coupled_uses=()),
    MenuRole('object_controller_terminal_subphase_relation_2', 'run_scene_object_controller_complete', (('body', 3, 'body', 21, 'body', 18, 'body', 0, 'test', 'ops', 0),),
        'unsigned_relation', '==', (252034,),
        coupled_uses=()),
    MenuRole('object_controller_final_subphase_relation', 'run_scene_object_controller_complete', (('body', 3, 'body', 21, 'body', 19, 'body', 0, 'test', 'ops', 0),),
        'unsigned_relation', '==', (252070,),
        coupled_uses=()),
)

_TRUE_BRANCH = {'<': 'bcs', '<=': 'bls', '>': 'bhi', '>=': 'bcc', '==': 'beq', '!=': 'bne'}
_FALSE_BRANCH = {'<': 'bcc', '<=': 'bhi', '>': 'bls', '>=': 'bcs', '==': 'bne', '!=': 'beq'}

_OWNER_ROLES = {'distribute_secondary_city_battle_progress': ('object_progress_budget_shift',), 'append_scene_center_marker': ('object_sprite_capacity', 'object_sprite_x_origin_bias', 'object_sprite_y_origin_bias', 'object_sprite_x_flip_correction', 'object_sprite_y_flip_correction', 'object_sprite_count_step', 'object_center_marker_x_offset', 'object_center_marker_y_offset', 'object_animation_side_bias', 'object_animation_phase_shift', 'object_animation_tick_shift', 'object_animation_tick_mask', 'object_animation_attributes'), 'run_scene_object_controller': ('object_controller_video_mask', 'object_controller_palette_start_shade', 'object_controller_default_action_mode', 'object_controller_start_sound', 'object_controller_restart_mask', 'object_controller_restart_relation', 'object_controller_variant_bound', 'object_controller_variant_relation', 'object_controller_variant_step', 'object_controller_terminal_phase_relation_0', 'object_controller_terminal_phase_relation_1', 'object_controller_terminal_phase_relation_2', 'object_controller_terminal_phase_relation_3', 'object_controller_terminal_subphase_relation_0', 'object_controller_terminal_subphase_relation_1', 'object_controller_terminal_subphase_relation_2', 'object_controller_final_subphase_relation'), 'integrate_scene_coordinates': ('object_coordinate_fraction_shift',), 'initialize_scene_object_video': ('object_video_row_stride',), 'dispatch_scene_object_phase': (), 'normalize_object_squad_size': ('object_squad_count_cap', 'object_squad_upper_size', 'object_squad_lower_size', 'object_squad_decrease_floor', 'object_squad_increase_step', 'object_squad_decrease_step', 'object_squad_cap_relation', 'object_squad_upper_relation', 'object_squad_lower_relation', 'object_squad_floor_relation'), 'cycle_special_scene_palette': ('object_palette_tick_shift',), 'clear_scene_object_label_plane': ('object_label_fill_tile',), 'advance_scene_object_actions': ('object_action_timer_step', 'object_action_slot_step', 'object_action_slot_bound', 'object_action_slot_relation', 'object_action_class_step', 'object_action_class_bound', 'object_action_class_relation', 'object_action_side_step', 'object_action_side_bound', 'object_action_side_relation', 'object_action_slow_class_bound', 'object_action_slow_class_relation', 'object_action_slow_timer', 'object_action_matching_class_relation'), 'rebuild_depth_sorted_object_queue': ('object_queue_tick_mask', 'object_queue_maximum_depth', 'object_queue_depth_shift', 'object_queue_depth_relation'), 'update_selected_object_action': ('object_selection_x_limit', 'object_selection_x_relation', 'object_selection_random_mask', 'object_selection_plan_relation'), 'read_object_action_mode': (), 'probe_scene_object_overlap': ('object_overlap_horizontal_relation', 'object_overlap_vertical_relation'), 'offset_scene_object_position': ('object_offset_negative_magnitude_mask',), 'plan_scene_object_action': ('object_plan_long_range_mode', 'object_plan_long_mode_relation', 'object_plan_long_range_member', 'object_plan_member_relation', 'object_plan_mode_short_positive', 'object_plan_mode_short_negative', 'object_plan_mode_long_distance_0', 'object_plan_mode_long_distance_1', 'object_plan_mode_long_distance_2', 'object_plan_short_west', 'object_plan_short_east', 'object_plan_short_south', 'object_plan_short_north', 'object_plan_long_west_0', 'object_plan_long_west_1', 'object_plan_long_west_2', 'object_plan_long_east_0', 'object_plan_long_east_1', 'object_plan_long_east_2', 'object_plan_long_south_0', 'object_plan_long_south_1', 'object_plan_long_south_2', 'object_plan_long_north_0', 'object_plan_long_north_1', 'object_plan_long_north_2', 'object_plan_short_sound', 'object_plan_long_sound', 'object_plan_mode_long_distance_0_encoded_041222', 'object_plan_mode_long_distance_0_encoded_0412a0', 'object_plan_mode_long_distance_1_encoded_041234', 'object_plan_mode_long_distance_1_encoded_0412b2', 'object_plan_mode_long_distance_2_encoded_041246', 'object_plan_mode_long_distance_2_encoded_0412c4'), 'probe_opposing_object_overlap': (), 'initialize_scene_object_roster': ('object_roster_initial_count', 'object_roster_troop_minimum', 'object_roster_small_troop_bound', 'object_roster_medium_troop_bound', 'object_roster_large_troop_bound', 'object_roster_maximum_count', 'object_roster_minimum_relation', 'object_roster_small_relation', 'object_roster_medium_relation', 'object_roster_large_relation', 'object_roster_count_random_mask', 'object_roster_small_random_bound', 'object_roster_other_random_bound', 'object_roster_small_accept_relation', 'object_roster_other_accept_relation', 'object_roster_small_count_bias', 'object_roster_medium_count_bias', 'object_roster_large_count_bias', 'object_roster_partition_0_quality', 'object_roster_partition_0_first_count', 'object_roster_partition_0_second_count', 'object_roster_partition_1_quality', 'object_roster_partition_1_first_count', 'object_roster_partition_1_second_count', 'object_roster_partition_2_quality', 'object_roster_partition_2_first_count', 'object_roster_partition_2_second_count', 'object_roster_partition_3_quality', 'object_roster_partition_3_first_count', 'object_roster_partition_3_second_count', 'object_roster_partition_4_quality', 'object_roster_partition_4_first_count', 'object_roster_partition_4_second_count', 'object_roster_partition_5_quality', 'object_roster_partition_5_first_count', 'object_roster_partition_5_second_count', 'object_roster_partition_relation', 'object_roster_partition_last_0', 'object_roster_partition_last_1', 'object_roster_layout_random_mask', 'object_roster_layout_bound', 'object_roster_layout_relation', 'object_roster_member_consume_step', 'object_roster_member_counter_step', 'object_roster_quality_divisor', 'object_roster_remainder_consume_step', 'object_roster_remainder_spread_step')}
_CONSTRAINTS = {'object_sprite_capacity': (1, 80), 'object_animation_tick_mask': (0, 3), 'object_offset_negative_magnitude_mask': (0, 127), 'object_action_slot_bound': (1, 16), 'object_action_class_bound': (1, 4), 'object_action_side_bound': (1, 3), 'object_plan_mode_short_negative': (32768, 65535), 'object_plan_mode_long_distance_0': (0, 32767), 'object_plan_mode_long_distance_1': (0, 32767), 'object_plan_mode_long_distance_2': (0, 32767), 'object_plan_short_west': (32768, 65535), 'object_plan_short_east': (0, 32767), 'object_plan_short_south': (0, 32767), 'object_plan_short_north': (32768, 65535), 'object_plan_long_west_0': (32768, 65535), 'object_plan_long_west_1': (32768, 65535), 'object_plan_long_west_2': (32768, 65535), 'object_plan_long_east_0': (0, 32767), 'object_plan_long_east_1': (0, 32767), 'object_plan_long_east_2': (0, 32767), 'object_plan_long_south_0': (0, 32767), 'object_plan_long_south_1': (0, 32767), 'object_plan_long_south_2': (0, 32767), 'object_plan_long_north_0': (32768, 65535), 'object_plan_long_north_1': (32768, 65535), 'object_plan_long_north_2': (32768, 65535), 'object_roster_initial_count': (1, 15), 'object_roster_maximum_count': (1, 15), 'object_roster_count_random_mask': (0, 15), 'object_roster_partition_0_first_count': (0, 15), 'object_roster_partition_0_second_count': (0, 15), 'object_roster_partition_1_first_count': (0, 15), 'object_roster_partition_1_second_count': (0, 15), 'object_roster_partition_2_first_count': (0, 15), 'object_roster_partition_2_second_count': (0, 15), 'object_roster_partition_3_first_count': (0, 15), 'object_roster_partition_3_second_count': (0, 15), 'object_roster_partition_4_first_count': (0, 15), 'object_roster_partition_4_second_count': (0, 15), 'object_roster_partition_5_first_count': (0, 15), 'object_roster_partition_5_second_count': (0, 15), 'object_roster_partition_last_0': (0, 15), 'object_roster_partition_last_1': (0, 15), 'object_roster_layout_random_mask': (0, 7), 'object_roster_layout_bound': (0, 4), 'object_controller_default_action_mode': (0, 9), 'object_controller_variant_bound': (0, 3)}

def owner_rules(values):
    """Validate all actual role values and give every owner its real rules.

    No rule is read by numeric value or falls back to a canonical literal.
    Fixed vector/layout owners are still completely lowered; no RAM address,
    directory topology, IRQ/SR protocol or continuation token is a policy slot.
    """
    checked = {}
    limits = {'word': (0, 65535), 'byte': (0, 255), 'long': (0, 0xffffffff),
              'nonzero_word': (1, 65535), 'quick': (1, 8), 'shift': (1, 8), 'moveq': (0, 127)}
    for role in ROLE_SPECS:
        if role.name not in values:
            raise CompileError('all complete scene-object source roles required')
        value = values[role.name]
        if role.kind == 'unsigned_relation':
            if type(value) is not str or value not in _TRUE_BRANCH:
                raise CompileError(role.name + ': supported unsigned relation required')
        else:
            low, high = limits[role.kind]
            if type(value) is not int or not low <= value <= high:
                raise CompileError(role.name + ': strict bounded source integer required')
            constraint = _CONSTRAINTS.get(role.name)
            if type(constraint) is tuple and not constraint[0] <= value <= constraint[1]:
                raise CompileError(role.name + ': source data/record domain bound required')
        checked[role.name] = value
    # The existing readonly layout directory has five possible entries. These
    # relation edits cannot turn its original rejection guard into index widening.
    if checked['object_roster_layout_relation'] not in ('<', '<=', '=='):
        raise CompileError('layout acceptance may restrict the five-entry directory, not widen it')
    # Source-derived sign-magnitude outputs, with no second literal authority.
    checked['object_plan_mode_long_distance_0_encoded_041222'] = checked['object_plan_mode_long_distance_0']
    checked['object_plan_mode_long_distance_0_encoded_0412a0'] = checked['object_plan_mode_long_distance_0'] | 32768
    checked['object_plan_mode_long_distance_1_encoded_041234'] = checked['object_plan_mode_long_distance_1']
    checked['object_plan_mode_long_distance_1_encoded_0412b2'] = checked['object_plan_mode_long_distance_1'] | 32768
    checked['object_plan_mode_long_distance_2_encoded_041246'] = checked['object_plan_mode_long_distance_2']
    checked['object_plan_mode_long_distance_2_encoded_0412c4'] = checked['object_plan_mode_long_distance_2'] | 32768
    owners = {}
    for owner, names in _OWNER_ROLES.items():
        rules = {name: checked[name] for name in names}
        for role in ROLE_SPECS:
            if role.name in rules and role.kind == 'unsigned_relation':
                rules[role.name + '_true_branch'] = _TRUE_BRANCH[rules[role.name]]
                rules[role.name + '_false_branch'] = _FALSE_BRANCH[rules[role.name]]
        owners[owner] = rules
    return owners


def lower_distribute_secondary_city_battle_progress(emitter, rules):
    emitter.segment(116194, 116206)
    emitter.ins('bsr.w', 'scene_pc_01c2c8', 4)
    emitter.ins('move.w', '0xefba:w,%d0', 4)
    emitter.ins('lsl.w', f"#0x{rules['object_progress_budget_shift']:x},%d0", 2)
    emitter.ins('bra.b', 'scene_pc_01c586', 2)

def lower_append_scene_center_marker(emitter, rules):
    emitter.segment(241980, 242236)
    emitter.ins('movem.l', '%d5-%d6/%a1,-(%a7)', 4)
    emitter.ins('cmpi.b', f"#0x{rules['object_sprite_capacity']:x},0xf300:w", 6)
    emitter.ins('bcc.w', 'scene_pc_03b236', 4)
    emitter.ins('andi.l', '#0xffff,%d4', 6)
    emitter.ins('move.w', '%d2,%d7', 2)
    emitter.ins('andi.w', '#0xfff8,%d2', 4)
    emitter.ins('andi.w', '#0x7,%d7', 4)
    emitter.ins('asl.w', '#0x2,%d7', 2)
    emitter.ins('sub.w', '0x8020:w,%d0', 4)
    emitter.ins('addi.w', f"#0x{rules['object_sprite_x_origin_bias']:x},%d0", 4)
    emitter.ins('bmi.w', 'scene_pc_03b236', 4)
    emitter.ins('btst.l', '#0x5,%d2', 4)
    emitter.ins('beq.b', 'scene_pc_03b172', 2)
    emitter.ins('subi.w', f"#0x{rules['object_sprite_x_flip_correction']:x},%d0", 4)
    emitter.ins('sub.w', '0x8022:w,%d1', 4)
    emitter.ins('addi.w', f"#0x{rules['object_sprite_y_origin_bias']:x},%d1", 4)
    emitter.ins('btst.l', '#0x4,%d2', 4)
    emitter.ins('beq.b', 'scene_pc_03b184', 2)
    emitter.ins('subi.w', f"#0x{rules['object_sprite_y_flip_correction']:x},%d1", 4)
    emitter.ins('clr.w', '%d5', 2)
    emitter.ins('move.b', '0xf300:w,%d5', 4)
    emitter.ins('lsl.w', '#0x3,%d5', 2)
    emitter.ins('lea.l', '0xf800:w,%a1', 4)
    emitter.ins('lea.l', '0x8044:w,%a2', 4)
    emitter.ins('lea.l', '(%a1, %d5.w),%a1', 4)
    emitter.ins('move.w', '%d0,%d6', 2)
    emitter.ins('moveq', '#0,%d5', 2)
    emitter.ins('move.b', '(%a0),%d5', 2)
    emitter.ins('cmpi.b', '#0x80,%d5', 4)
    emitter.ins('beq.w', 'scene_pc_03b236', 4)
    emitter.ins('btst.l', '#0x5,%d2', 4)
    emitter.ins('beq.w', 'scene_pc_03b1b0', 4)
    emitter.ins('neg.b', '%d5', 2)
    emitter.ins('btst.l', '#0x7,%d5', 4)
    emitter.ins('beq.b', 'scene_pc_03b1bc', 2)
    emitter.ins('neg.b', '%d5', 2)
    emitter.ins('sub.w', '%d5,%d6', 2)
    emitter.ins('bra.b', 'scene_pc_03b1be', 2)
    emitter.ins('add.w', '%d5,%d6', 2)
    emitter.ins('move.w', '%d6,(%a1)', 2)
    emitter.ins('move.w', '%d1,%d6', 2)
    emitter.ins('move.b', '0x3(%a0),%d5', 4)
    emitter.ins('btst.l', '#0x4,%d2', 4)
    emitter.ins('beq.b', 'scene_pc_03b1ce', 2)
    emitter.ins('neg.b', '%d5', 2)
    emitter.ins('btst.l', '#0x7,%d5', 4)
    emitter.ins('btst.l', '#0x7,%d5', 4)
    emitter.ins('beq.b', 'scene_pc_03b1de', 2)
    emitter.ins('neg.b', '%d5', 2)
    emitter.ins('sub.w', '%d5,%d6', 2)
    emitter.ins('bra.b', 'scene_pc_03b1e0', 2)
    emitter.ins('add.w', '%d5,%d6', 2)
    emitter.ins('move.w', '%d6,0x6(%a1)', 4)
    emitter.ins('move.b', '0x1(%a0),0x2(%a1)', 6)
    emitter.ins('tst.l', '(%a2, %d7.w)', 4)
    emitter.ins('bne.w', 'scene_pc_03b1fe', 4)
    emitter.ins('move.l', '%a1,(%a2, %d7.w)', 4)
    emitter.ins('move.b', '0xf300:w,0x20(%a2, %d7.w)', 6)
    emitter.ins('bra.b', 'scene_pc_03b208', 2)
    emitter.ins('movea.l', '0x40(%a2, %d7.w),%a3', 4)
    emitter.ins('move.b', '0xf300:w,0x3(%a3)', 6)
    emitter.ins('move.l', '%a1,0x40(%a2, %d7.w)', 4)
    emitter.ins('addq.b', f"#0x{rules['object_sprite_count_step']:x},0xf300:w", 4)
    emitter.ins('move.b', '0x1(%a0),%d5', 4)
    emitter.ins('andi.w', '#0xf0,%d5', 4)
    emitter.ins('add.b', '%d3,%d5', 2)
    emitter.ins('eor.w', '%d2,%d5', 2)
    emitter.ins('asl.w', '#0x7,%d5', 2)
    emitter.ins('or.b', '0x2(%a0),%d5', 4)
    emitter.ins('add.w', '%d4,%d5', 2)
    emitter.ins('move.w', '%d5,0x4(%a1)', 4)
    emitter.ins('addq.l', '#0x8,%a1', 2)
    emitter.ins('addq.l', '#0x4,%a0', 2)
    emitter.ins('cmpi.b', f"#0x{rules['object_sprite_capacity']:x},0xf300:w", 6)
    emitter.ins('bcs.w', 'scene_pc_03b198', 4)
    emitter.ins('movem.l', '(%a7)+,%d5-%d6/%a1', 4)
    emitter.ins('rts', '', 2)
    emitter.segment(242312, 242346)
    emitter.ins('move.w', '0x8020:w,%d0', 4)
    emitter.ins('subi.w', f"#0x{rules['object_center_marker_x_offset']:x},%d0", 4)
    emitter.ins('move.w', '0x8022:w,%d1', 4)
    emitter.ins('subi.w', f"#0x{rules['object_center_marker_y_offset']:x},%d1", 4)
    emitter.ins('moveq', '#0,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('lea.l', '8(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('jmp', '-364(%pc)', 4)
    emitter.segment(263238, 263372)
    emitter.ins('tst.w', '0x813e:w', 4)
    emitter.ins('bne.b', 'scene_pc_040452', 2)
    emitter.ins('jsr', '2118(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', '(%a6),%d0', 2)
    emitter.ins('andi.w', '#0xff,%d0', 4)
    emitter.ins('moveq', '#0,%d1', 2)
    emitter.ins('lea.l', '112(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.b', '(%a0, %d0.w),%d1', 4)
    emitter.ins('cmpi.b', '#0x3,0x80db:w', 6)
    emitter.ins('bne.b', 'scene_pc_040470', 2)
    emitter.ins('move.b', '0x4(%a0, %d0.w),%d1', 4)
    emitter.ins('tst.w', '0x8124:w', 4)
    emitter.ins('bne.b', 'scene_pc_040486', 2)
    emitter.ins('cmpa.l', '#0xffff826a,%a6', 6)
    emitter.ins('bcs.b', 'scene_pc_040492', 2)
    emitter.ins('addi.w', f"#0x{rules['object_animation_side_bias']:x},%d1", 4)
    emitter.ins('bra.w', 'scene_pc_040492', 4)
    emitter.ins('cmpa.l', '#0xffff826a,%a6', 6)
    emitter.ins('bcc.b', 'scene_pc_040492', 2)
    emitter.ins('addi.w', f"#0x{rules['object_animation_side_bias']:x},%d1", 4)
    emitter.ins('move.w', '0x8(%a6),%d0', 4)
    emitter.ins('asl.w', f"#0x{rules['object_animation_phase_shift']:x},%d0", 2)
    emitter.ins('add.w', '%d0,%d1', 2)
    emitter.ins('move.w', '0xf320:w,%d0', 4)
    emitter.ins('lsr.w', f"#0x{rules['object_animation_tick_shift']:x},%d0", 2)
    emitter.ins('andi.w', f"#0x{rules['object_animation_tick_mask']:x},%d0", 4)
    emitter.ins('add.w', '%d1,%d0', 2)
    emitter.ins('move.w', '%d0,%d4', 2)
    emitter.ins('asl.w', '#0x2,%d0', 2)
    emitter.ins('movea.l', '40(%pc, %d0.w),%a0', 4)
    emitter.ins('move.w', '0x2(%a6),%d0', 4)
    emitter.ins('move.w', '0x4(%a6),%d1', 4)
    emitter.ins('move.w', f"#0x{rules['object_animation_attributes']:x},%d2", 4)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('asl.w', '#0x1,%d4', 2)
    emitter.ins('lea.l', '788(%pc),%a1', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', '(%a1, %d4.w),%d4', 4)
    emitter.ins('jmp', '-21390(%pc)', 4)

def lower_run_scene_object_controller(emitter, rules):
    emitter.segment(251476, 251758)
    emitter.ins('move.w', '#0x2700,%sr', 4)
    emitter.ins('move.w', '0xf606:w,%d0', 4)
    emitter.ins('andi.b', f"#0x{rules['object_controller_video_mask']:x},%d0", 4)
    emitter.ins('move.w', '%d0,0xc00004:l', 6)
    emitter.ins('jsr', 'scene_pc_0068ce:l', 6)
    emitter.ins('move.w', '#0x2,0xf6c4:w', 6)
    emitter.ins('bsr.w', 'scene_pc_03d9a0', 4)
    emitter.ins('moveq', '#0,%d0', 2)
    emitter.ins('move.b', '0x80db:w,%d0', 4)
    emitter.ins('jsr', '-10986(%pc)', 4)
    emitter.ins('move.w', '#0xffff,0x80ca:w', 6)
    emitter.ins('move.w', '#0xffff,0x80cc:w', 6)
    emitter.ins('move.w', '#0xffff,0x80ce:w', 6)
    emitter.ins('move.w', '#0xffff,0x80d0:w', 6)
    emitter.ins('moveq', f"#{rules['object_controller_palette_start_shade']},%d0", 2)
    emitter.ins('jsr', '-11388(%pc)', 4)
    emitter.ins('jsr', '-11286(%pc)', 4)
    emitter.ins('cmpi.w', '#0x3,0x813a:w', 6)
    emitter.ins('bne.w', 'scene_pc_03d712', 4)
    emitter.ins('bsr.w', 'scene_pc_04031c', 4)
    emitter.ins('move.w', '#0x0,0x813a:w', 6)
    emitter.ins('move.w', '#0x6,0x813c:w', 6)
    emitter.ins('clr.w', '0x813e:w', 4)
    emitter.ins('tst.w', '0x8124:w', 4)
    emitter.ins('bne.b', 'scene_pc_03d6f6', 2)
    emitter.ins('move.w', '0xff706c:l,0x8178:w', 8)
    emitter.ins('move.w', '0xff70bc:l,0x8278:w', 8)
    emitter.ins('cmpi.b', '#0x1,0xff70f0:l', 8)
    emitter.ins('bne.w', 'scene_pc_03d6ec', 4)
    emitter.ins('move.w', '#0x6,0x8130:w', 6)
    emitter.ins('bra.w', 'scene_pc_03d7e0', 4)
    emitter.ins('move.w', '#0x6,0x8138:w', 6)
    emitter.ins('bra.w', 'scene_pc_03d7e0', 4)
    emitter.ins('move.w', '0xff706c:l,0x8278:w', 8)
    emitter.ins('move.w', '0xff70bc:l,0x8178:w', 8)
    emitter.ins('cmpi.b', '#0x1,0xff70f0:l', 8)
    emitter.ins('beq.b', 'scene_pc_03d6ec', 2)
    emitter.ins('bra.b', 'scene_pc_03d6e2', 2)
    emitter.ins('move.w', '#0x0,0x8020:w', 6)
    emitter.ins('move.l', '#0x0,0x8024:w', 8)
    emitter.ins('move.w', '#0x107,%d0', 4)
    emitter.ins('lea.l', '0x812a:w,%a0', 4)
    emitter.ins('clr.w', '(%a0)+', 2)
    emitter.ins('dbra', '%d0,scene_pc_03d728', 4)
    emitter.ins('move.w', f"#0x{rules['object_controller_default_action_mode']:x},0x812a:w", 6)
    emitter.ins('move.w', f"#0x{rules['object_controller_default_action_mode']:x},0x812c:w", 6)
    emitter.ins('move.w', f"#0x{rules['object_controller_default_action_mode']:x},0x812e:w", 6)
    emitter.ins('move.w', f"#0x{rules['object_controller_default_action_mode']:x},0x8130:w", 6)
    emitter.ins('move.w', f"#0x{rules['object_controller_default_action_mode']:x},0x8132:w", 6)
    emitter.ins('move.w', f"#0x{rules['object_controller_default_action_mode']:x},0x8134:w", 6)
    emitter.ins('move.w', f"#0x{rules['object_controller_default_action_mode']:x},0x8136:w", 6)
    emitter.ins('move.w', f"#0x{rules['object_controller_default_action_mode']:x},0x8138:w", 6)
    emitter.ins('move.w', '#0x9,0x813a:w', 6)
    emitter.ins('move.w', '#0x0,0x813c:w', 6)
    emitter.ins('bra.w', 'scene_pc_03d7da', 4)
    emitter.segment(251866, 252132)
    emitter.ins('jsr', '16410(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', f"#0x{rules['object_controller_start_sound']:x},%d0", 4)
    emitter.ins('jsr', 'scene_pc_00808a:l', 6)
    emitter.ins('move.w', '#0x2500,%sr', 4)
    emitter.ins('move.w', '#0x500,0xf612:w', 6)
    emitter.ins('jsr', 'scene_pc_0083c8:l', 6)
    emitter.ins('clr.w', '0xf612:w', 4)
    emitter.ins('jsr', '-9592(%pc)', 4)
    emitter.ins('bsr.w', 'scene_pc_03f890', 4)
    emitter.ins('jsr', '-11920(%pc)', 4)
    emitter.ins('jsr', '1196(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('jsr', '11050(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('jsr', '-9692(%pc)', 4)
    emitter.ins('jsr', '200(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('cmpi.w', '#0x3,0x813a:w', 6)
    emitter.ins(rules['object_controller_terminal_phase_relation_0_false_branch'] + '.b', 'scene_pc_03d84a', 2)
    emitter.ins('cmpi.w', '#0x3,0x813c:w', 6)
    emitter.ins(rules['object_controller_terminal_subphase_relation_0_false_branch'] + '.b', 'scene_pc_03d84a', 2)
    emitter.ins('move.w', '#0x1,0x8114:w', 6)
    emitter.ins('move.w', '#0x2700,%sr', 4)
    emitter.ins('move.w', '0xf606:w,%d0', 4)
    emitter.ins('andi.b', f"#0x{rules['object_controller_video_mask']:x},%d0", 4)
    emitter.ins('move.w', '%d0,0xc00004:l', 6)
    emitter.ins('rts', '', 2)
    emitter.ins('cmpi.w', '#0x4,0x813a:w', 6)
    emitter.ins(rules['object_controller_terminal_phase_relation_1_false_branch'] + '.b', 'scene_pc_03d874', 2)
    emitter.ins('cmpi.w', '#0x3,0x813c:w', 6)
    emitter.ins(rules['object_controller_terminal_subphase_relation_1_false_branch'] + '.b', 'scene_pc_03d874', 2)
    emitter.ins('move.w', '#0x0,0x8114:w', 6)
    emitter.ins('move.w', '#0x2700,%sr', 4)
    emitter.ins('move.w', '0xf606:w,%d0', 4)
    emitter.ins('andi.b', f"#0x{rules['object_controller_video_mask']:x},%d0", 4)
    emitter.ins('move.w', '%d0,0xc00004:l', 6)
    emitter.ins('rts', '', 2)
    emitter.ins('cmpi.w', '#0x5,0x813a:w', 6)
    emitter.ins(rules['object_controller_terminal_phase_relation_2_false_branch'] + '.b', 'scene_pc_03d898', 2)
    emitter.ins('cmpi.w', '#0x3,0x813c:w', 6)
    emitter.ins(rules['object_controller_terminal_subphase_relation_2_false_branch'] + '.b', 'scene_pc_03d898', 2)
    emitter.ins('move.w', '#0x2700,%sr', 4)
    emitter.ins('move.w', '0xf606:w,%d0', 4)
    emitter.ins('andi.b', f"#0x{rules['object_controller_video_mask']:x},%d0", 4)
    emitter.ins('move.w', '%d0,0xc00004:l', 6)
    emitter.ins('rts', '', 2)
    emitter.ins('cmpi.w', '#0x6,0x813a:w', 6)
    emitter.ins(rules['object_controller_terminal_phase_relation_3_false_branch'] + '.b', 'scene_pc_03d8c2', 2)
    emitter.ins('cmpi.w', '#0x4,0x813c:w', 6)
    emitter.ins(rules['object_controller_final_subphase_relation_false_branch'] + '.b', 'scene_pc_03d8c2', 2)
    emitter.ins('move.w', '#0x6,0x8114:w', 6)
    emitter.ins('move.w', '#0x2700,%sr', 4)
    emitter.ins('move.w', '0xf606:w,%d0', 4)
    emitter.ins('andi.b', f"#0x{rules['object_controller_video_mask']:x},%d0", 4)
    emitter.ins('move.w', '%d0,0xc00004:l', 6)
    emitter.ins('rts', '', 2)
    emitter.ins('move.b', '0xf602:w,%d0', 4)
    emitter.ins('andi.b', f"#0x{rules['object_controller_restart_mask']:x},%d0", 4)
    emitter.ins('cmpi.b', f"#0x{rules['object_controller_restart_mask']:x},%d0", 4)
    emitter.ins(rules['object_controller_restart_relation_true_branch'] + '.w', 'scene_pc_03d7ee', 4)
    emitter.ins('cmpi.b', f"#0x{rules['object_controller_variant_bound']:x},0x80db:w", 6)
    emitter.ins(rules['object_controller_variant_relation_false_branch'] + '.w', 'scene_pc_03d654', 4)
    emitter.ins('addq.b', f"#0x{rules['object_controller_variant_step']:x},0x80db:w", 4)
    emitter.ins('bra.w', 'scene_pc_03d654', 4)

def lower_integrate_scene_coordinates(emitter, rules):
    emitter.segment(252132, 252272)
    emitter.ins('move.w', '0x8024:w,%d0', 4)
    emitter.ins('swap', '%d0', 2)
    emitter.ins('move.w', '0x802c:w,%d0', 4)
    emitter.ins('moveq', '#0,%d1', 2)
    emitter.ins('move.w', '0x8038:w,%d1', 4)
    emitter.ins('bpl.w', 'scene_pc_03d904', 4)
    emitter.ins('andi.w', '#0x7fff,%d1', 4)
    emitter.ins('asl.l', f"#0x{rules['object_coordinate_fraction_shift']:x},%d1", 2)
    emitter.ins('add.l', '%d1,%d0', 2)
    emitter.ins('bra.w', 'scene_pc_03d908', 4)
    emitter.ins('asl.l', f"#0x{rules['object_coordinate_fraction_shift']:x},%d1", 2)
    emitter.ins('sub.l', '%d1,%d0', 2)
    emitter.ins('move.w', '%d0,0x802c:w', 4)
    emitter.ins('swap', '%d0', 2)
    emitter.ins('move.w', '%d0,0x8024:w', 4)
    emitter.ins('move.w', '0x8026:w,%d0', 4)
    emitter.ins('swap', '%d0', 2)
    emitter.ins('move.w', '0x802e:w,%d0', 4)
    emitter.ins('moveq', '#0,%d1', 2)
    emitter.ins('move.w', '0x803a:w,%d1', 4)
    emitter.ins('bpl.w', 'scene_pc_03d932', 4)
    emitter.ins('andi.w', '#0x7fff,%d1', 4)
    emitter.ins('asl.l', f"#0x{rules['object_coordinate_fraction_shift']:x},%d1", 2)
    emitter.ins('add.l', '%d1,%d0', 2)
    emitter.ins('bra.w', 'scene_pc_03d936', 4)
    emitter.ins('asl.l', f"#0x{rules['object_coordinate_fraction_shift']:x},%d1", 2)
    emitter.ins('sub.l', '%d1,%d0', 2)
    emitter.ins('move.w', '%d0,0x802e:w', 4)
    emitter.ins('swap', '%d0', 2)
    emitter.ins('move.w', '%d0,0x8026:w', 4)
    emitter.ins('move.w', '0x8020:w,%d0', 4)
    emitter.ins('swap', '%d0', 2)
    emitter.ins('move.w', '0x8034:w,%d0', 4)
    emitter.ins('moveq', '#0,%d1', 2)
    emitter.ins('move.w', '0x8040:w,%d1', 4)
    emitter.ins('bpl.w', 'scene_pc_03d960', 4)
    emitter.ins('andi.w', '#0x7fff,%d1', 4)
    emitter.ins('asl.l', f"#0x{rules['object_coordinate_fraction_shift']:x},%d1", 2)
    emitter.ins('add.l', '%d1,%d0', 2)
    emitter.ins('bra.w', 'scene_pc_03d964', 4)
    emitter.ins('asl.l', f"#0x{rules['object_coordinate_fraction_shift']:x},%d1", 2)
    emitter.ins('sub.l', '%d1,%d0', 2)
    emitter.ins('move.w', '%d0,0x8034:w', 4)
    emitter.ins('swap', '%d0', 2)
    emitter.ins('move.w', '%d0,0x8020:w', 4)
    emitter.ins('rts', '', 2)

def lower_initialize_scene_object_video(emitter, rules):
    emitter.segment(252320, 252620)
    emitter.ins('move.w', '#0x8f02,0xc00004:l', 8)
    emitter.ins('move.w', '#0x8230,0xc00004:l', 8)
    emitter.ins('move.w', '#0x8330,0xc00004:l', 8)
    emitter.ins('move.w', '#0x8407,0xc00004:l', 8)
    emitter.ins('move.w', '#0x8568,0xc00004:l', 8)
    emitter.ins('move.w', '#0x8700,0xc00004:l', 8)
    emitter.ins('move.w', '#0x8b00,0xc00004:l', 8)
    emitter.ins('move.w', '#0x8c81,0xc00004:l', 8)
    emitter.ins('move.w', '#0x8d35,0xc00004:l', 8)
    emitter.ins('move.w', '#0x8f02,0xc00004:l', 8)
    emitter.ins('move.w', '#0x9011,0xc00004:l', 8)
    emitter.ins('move.w', '#0x9194,0xc00004:l', 8)
    emitter.ins('move.w', '#0x9200,0xc00004:l', 8)
    emitter.ins('lea.l', '0x473e4:l,%a0', 6)
    emitter.ins('move.w', '#0x0,%d0', 4)
    emitter.ins('bsr.w', 'scene_pc_03ab52', 4)
    emitter.ins('lea.l', '0x492e8:l,%a0', 6)
    emitter.ins('move.w', '#0x2000,%d0', 4)
    emitter.ins('bsr.w', 'scene_pc_03ab52', 4)
    emitter.ins('lea.l', '0x4a9a2:l,%a0', 6)
    emitter.ins('move.w', '#0x4000,%d0', 4)
    emitter.ins('bsr.w', 'scene_pc_03ab52', 4)
    emitter.ins('lea.l', '0x4c5ac:l,%a0', 6)
    emitter.ins('move.w', '#0x6000,%d0', 4)
    emitter.ins('bsr.w', 'scene_pc_03ab52', 4)
    emitter.ins('lea.l', '0x4e090:l,%a0', 6)
    emitter.ins('move.w', '#0x8000,%d0', 4)
    emitter.ins('bsr.w', 'scene_pc_03ab52', 4)
    emitter.ins('moveq', '#0,%d0', 2)
    emitter.ins('move.b', '0x80db:w,%d0', 4)
    emitter.ins('asl.w', '#0x2,%d0', 2)
    emitter.ins('lea.l', '116(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('movea.l', '(%a0, %d0.w),%a0', 4)
    emitter.ins('lea.l', '0xe000:l,%a1', 6)
    emitter.ins('move.l', f"#0x{rules['object_video_row_stride']:x},%d5", 6)
    emitter.ins('jsr', '-12192(%pc)', 4)
    emitter.ins('moveq', '#0,%d0', 2)
    emitter.ins('move.b', '0x80db:w,%d0', 4)
    emitter.ins('asl.w', '#0x2,%d0', 2)
    emitter.ins('lea.l', '98(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('movea.l', '(%a0, %d0.w),%a0', 4)
    emitter.ins('lea.l', '0xe040:l,%a1', 6)
    emitter.ins('move.l', f"#0x{rules['object_video_row_stride']:x},%d5", 6)
    emitter.ins('jsr', '-12226(%pc)', 4)
    emitter.ins('moveq', '#0,%d0', 2)
    emitter.ins('move.b', '0x80db:w,%d0', 4)
    emitter.ins('asl.w', '#0x2,%d0', 2)
    emitter.ins('movea.l', '48(%pc, %d0.w),%a0', 4)
    emitter.ins('lea.l', '0xf000:l,%a1', 6)
    emitter.ins('move.l', f"#0x{rules['object_video_row_stride']:x},%d5", 6)
    emitter.ins('jsr', '-12254(%pc)', 4)
    emitter.ins('moveq', '#0,%d0', 2)
    emitter.ins('move.b', '0x80db:w,%d0', 4)
    emitter.ins('asl.w', '#0x2,%d0', 2)
    emitter.ins('movea.l', '36(%pc, %d0.w),%a0', 4)
    emitter.ins('lea.l', '0xf040:l,%a1', 6)
    emitter.ins('move.l', f"#0x{rules['object_video_row_stride']:x},%d5", 6)
    emitter.ins('jsr', '-12282(%pc)', 4)
    emitter.ins('rts', '', 2)

def lower_dispatch_scene_object_phase(emitter, rules):
    emitter.segment(253112, 253122)
    emitter.ins('move.w', '0x813a:w,%d0', 4)
    emitter.ins('asl.w', '#0x2,%d0', 2)
    emitter.ins('jmp', '2(%pc, %d0.w)', 4)

def lower_normalize_object_squad_size(emitter, rules):
    emitter.segment(259266, 259352)
    emitter.ins('moveq', '#0,%d0', 2)
    emitter.ins('moveq', '#0,%d1', 2)
    emitter.ins('move.w', '0x80e4:w,%d0', 4)
    emitter.ins('move.w', '0x80e8:w,%d1', 4)
    emitter.ins('bne.w', 'scene_pc_03f4d8', 4)
    emitter.ins('addq.w', f"#0x{rules['object_squad_increase_step']:x},0x80e8:w", 4)
    emitter.ins('bra.b', 'scene_pc_03f4c2', 2)
    emitter.ins('cmpi.w', f"#0x{rules['object_squad_count_cap']:x},%d1", 4)
    emitter.ins(rules['object_squad_cap_relation_false_branch'] + '.w', 'scene_pc_03f4e6', 4)
    emitter.ins('subq.w', f"#0x{rules['object_squad_decrease_step']:x},0x80e8:w", 4)
    emitter.ins('bra.b', 'scene_pc_03f4c2', 2)
    emitter.ins('divu.w', '%d1,%d0', 2)
    emitter.ins('cmpi.w', f"#0x{rules['object_squad_upper_size']:x},%d0", 4)
    emitter.ins(rules['object_squad_upper_relation_false_branch'] + '.w', 'scene_pc_03f4f6', 4)
    emitter.ins('addq.w', f"#0x{rules['object_squad_increase_step']:x},0x80e8:w", 4)
    emitter.ins('bra.b', 'scene_pc_03f4c2', 2)
    emitter.ins('cmpi.w', f"#0x{rules['object_squad_lower_size']:x},%d0", 4)
    emitter.ins(rules['object_squad_lower_relation_false_branch'] + '.w', 'scene_pc_03f50c', 4)
    emitter.ins('cmpi.w', f"#0x{rules['object_squad_decrease_floor']:x},0x80e8:w", 6)
    emitter.ins(rules['object_squad_floor_relation_false_branch'] + '.b', 'scene_pc_03f50c', 2)
    emitter.ins('subq.w', f"#0x{rules['object_squad_decrease_step']:x},0x80e8:w", 4)
    emitter.ins('bra.b', 'scene_pc_03f4c2', 2)
    emitter.ins('move.w', '%d0,0x80ec:w', 4)
    emitter.ins('swap', '%d0', 2)
    emitter.ins('move.w', '%d0,0x80f0:w', 4)
    emitter.ins('rts', '', 2)

def lower_cycle_special_scene_palette(emitter, rules):
    emitter.segment(260240, 260292)
    emitter.ins('cmpi.b', '#0x3,0x80db:w', 6)
    emitter.ins('bne.b', 'scene_pc_03f8c2', 2)
    emitter.ins('btst.b', '#0x7,0x80c4:w', 6)
    emitter.ins('beq.b', 'scene_pc_03f8c2', 2)
    emitter.ins('move.w', '0xf320:w,%d0', 4)
    emitter.ins('lsr.w', f"#0x{rules['object_palette_tick_shift']:x},%d0", 2)
    emitter.ins('andi.w', '#0x6,%d0', 4)
    emitter.ins('lea.l', '24(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', '(%a0, %d0.w),0xfb02:w', 6)
    emitter.ins('move.w', '0x8(%a0, %d0.w),0xfb04:w', 6)
    emitter.ins('move.w', '0x10(%a0, %d0.w),0xfb06:w', 6)
    emitter.ins('rts', '', 2)

def lower_clear_scene_object_label_plane(emitter, rules):
    emitter.segment(262940, 262972)
    emitter.ins('move.l', '#0x40000003,0xc00004:l', 10)
    emitter.ins('lea.l', '0xc00000:l,%a5', 6)
    emitter.ins('move.w', f"#0x{rules['object_label_fill_tile']:x},%d6", 4)
    emitter.ins('move.w', '#0x7ff,%d7', 4)
    emitter.ins('move.w', '%d6,(%a5)', 2)
    emitter.ins('dbra', '%d7,scene_pc_040334', 4)
    emitter.ins('rts', '', 2)

def lower_advance_scene_object_actions(emitter, rules):
    emitter.segment(262972, 263178)
    emitter.ins('bsr.w', 'scene_pc_04040a', 4)
    emitter.ins('lea.l', '0x836a:w,%a5', 4)
    emitter.ins('tst.l', '(%a5)', 2)
    emitter.ins('beq.b', 'scene_pc_040360', 2)
    emitter.ins('movea.l', '(%a5)+,%a6', 2)
    emitter.ins('btst.b', '#0x7,(%a6)', 4)
    emitter.ins('beq.b', 'scene_pc_040344', 2)
    emitter.ins('movem.l', '%a5,-(%a7)', 4)
    emitter.ins('jsr', '240(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('movem.l', '(%a7)+,%a5', 4)
    emitter.ins('bra.b', 'scene_pc_040344', 2)
    emitter.ins('tst.w', '0x814c:w', 4)
    emitter.ins('beq.w', 'scene_pc_040408', 4)
    emitter.ins('cmpi.w', '#0x2,0x8152:w', 6)
    emitter.ins('beq.w', 'scene_pc_040384', 4)
    emitter.ins('tst.w', '0x813e:w', 4)
    emitter.ins('bne.w', 'scene_pc_040408', 4)
    emitter.ins('cmpi.w', '#0x1,0x8152:w', 6)
    emitter.ins('beq.w', 'scene_pc_040408', 4)
    emitter.ins('clr.w', '0x8152:w', 4)
    emitter.ins('subq.w', f"#0x{rules['object_action_timer_step']:x},0x8154:w", 4)
    emitter.ins('bpl.w', 'scene_pc_040408', 4)
    emitter.ins('addq.w', f"#0x{rules['object_action_slot_step']:x},0x8150:w", 4)
    emitter.ins('cmpi.w', f"#0x{rules['object_action_slot_bound']:x},0x8150:w", 6)
    emitter.ins(rules['object_action_slot_relation_true_branch'] + '.b', 'scene_pc_0403d2', 2)
    emitter.ins('lea.l', '0x816a:w,%a0', 4)
    emitter.ins('cmpi.w', '#0x1,0x814c:w', 6)
    emitter.ins('beq.w', 'scene_pc_0403ae', 4)
    emitter.ins('lea.l', '0x826a:w,%a0', 4)
    emitter.ins('move.w', '0x8150:w,%d0', 4)
    emitter.ins('asl.w', '#0x4,%d0', 2)
    emitter.ins('btst.b', '#0x7,(%a0, %d0.w)', 6)
    emitter.ins('beq.w', 'scene_pc_040390', 4)
    emitter.ins('move.w', '(%a0, %d0.w),%d0', 4)
    emitter.ins('andi.w', '#0x7f,%d0', 4)
    emitter.ins('cmp.w', '0x814e:w,%d0', 4)
    emitter.ins(rules['object_action_matching_class_relation_false_branch'] + '.w', 'scene_pc_040390', 4)
    emitter.ins('bra.w', 'scene_pc_0403f6', 4)
    emitter.ins('clr.w', '0x8150:w', 4)
    emitter.ins('addq.w', f"#0x{rules['object_action_class_step']:x},0x814e:w", 4)
    emitter.ins('cmpi.w', f"#0x{rules['object_action_class_bound']:x},0x814e:w", 6)
    emitter.ins(rules['object_action_class_relation_false_branch'] + '.b', 'scene_pc_0403f6', 2)
    emitter.ins('clr.w', '0x814e:w', 4)
    emitter.ins('addq.w', f"#0x{rules['object_action_side_step']:x},0x814c:w", 4)
    emitter.ins('cmpi.w', f"#0x{rules['object_action_side_bound']:x},0x814c:w", 6)
    emitter.ins(rules['object_action_side_relation_false_branch'] + '.b', 'scene_pc_0403f6', 2)
    emitter.ins('clr.w', '0x814c:w', 4)
    emitter.ins('clr.w', '0x8154:w', 4)
    emitter.ins('cmpi.w', f"#0x{rules['object_action_slow_class_bound']:x},0x814e:w", 6)
    emitter.ins(rules['object_action_slow_class_relation_false_branch'] + '.b', 'scene_pc_040408', 2)
    emitter.ins('move.w', f"#0x{rules['object_action_slow_timer']:x},0x8154:w", 6)
    emitter.ins('rts', '', 2)

def lower_rebuild_depth_sorted_object_queue(emitter, rules):
    emitter.segment(263178, 263238)
    emitter.ins('move.w', '0xf320:w,%d0', 4)
    emitter.ins('andi.w', f"#0x{rules['object_queue_tick_mask']:x},%d0", 4)
    emitter.ins('bne.w', 'scene_pc_040444', 4)
    emitter.ins('lea.l', '0x836a:w,%a5', 4)
    emitter.ins('moveq', f"#{rules['object_queue_maximum_depth']},%d0", 2)
    emitter.ins('lea.l', '0x816a:w,%a6', 4)
    emitter.ins('btst.b', '#0x7,(%a6)', 4)
    emitter.ins('beq.b', 'scene_pc_040432', 2)
    emitter.ins('move.w', '0x2(%a6),%d1', 4)
    emitter.ins('lsr.w', f"#0x{rules['object_queue_depth_shift']:x},%d1", 2)
    emitter.ins('cmp.w', '%d0,%d1', 2)
    emitter.ins(rules['object_queue_depth_relation_false_branch'] + '.b', 'scene_pc_040432', 2)
    emitter.ins('move.l', '%a6,(%a5)+', 2)
    emitter.ins('adda.w', '#0x10,%a6', 4)
    emitter.ins('cmpa.l', '#0xffff836a,%a6', 6)
    emitter.ins('bcs.b', 'scene_pc_040420', 2)
    emitter.ins('dbra', '%d0,scene_pc_04041c', 4)
    emitter.ins('clr.l', '(%a5)', 2)
    emitter.ins('rts', '', 2)

def lower_update_selected_object_action(emitter, rules):
    emitter.segment(265364, 265484)
    emitter.ins('cmpa.l', '#0xffff826a,%a6', 6)
    emitter.ins('bcs.b', 'scene_pc_040cac', 2)
    emitter.ins('lea.l', '0x826a:w,%a5', 4)
    emitter.ins('cmpi.w', '#0x2,0x814c:w', 6)
    emitter.ins('bne.w', 'scene_pc_040d7a', 4)
    emitter.ins('bra.b', 'scene_pc_040cba', 2)
    emitter.ins('lea.l', '0x816a:w,%a5', 4)
    emitter.ins('cmpi.w', '#0x1,0x814c:w', 6)
    emitter.ins('bne.w', 'scene_pc_040d7a', 4)
    emitter.ins('move.w', '(%a6),%d0', 2)
    emitter.ins('andi.w', '#0x7f,%d0', 4)
    emitter.ins('cmp.w', '0x814e:w,%d0', 4)
    emitter.ins('bne.w', 'scene_pc_040d7a', 4)
    emitter.ins('moveq', '#0,%d0', 2)
    emitter.ins('move.w', '0x8150:w,%d0', 4)
    emitter.ins('asl.w', '#0x4,%d0', 2)
    emitter.ins('movea.w', '%d0,%a0', 2)
    emitter.ins('adda.l', '%a5,%a0', 2)
    emitter.ins('cmpa.l', '%a6,%a0', 2)
    emitter.ins('bne.w', 'scene_pc_040d7a', 4)
    emitter.ins('tst.w', '0x8152:w', 4)
    emitter.ins('bne.b', 'scene_pc_040d44', 2)
    emitter.ins('move.w', '#0x1,0x8152:w', 6)
    emitter.ins('cmpi.w', f"#0x{rules['object_selection_x_limit']:x},0x2(%a6)", 6)
    emitter.ins(rules['object_selection_x_relation_true_branch'] + '.w', 'scene_pc_040d76', 4)
    emitter.ins('jsr', '-21968(%pc)', 4)
    emitter.ins('andi.w', f"#0x{rules['object_selection_random_mask']:x},%d0", 4)
    emitter.ins(rules['object_selection_plan_relation_false_branch'] + '.b', 'scene_pc_040cfe', 2)
    emitter.ins('bsr.w', 'scene_pc_0411cc', 4)
    emitter.ins('bsr.w', 'scene_pc_040d28', 4)
    emitter.ins('move.w', '%d0,0x815a:w', 4)
    emitter.ins('asl.w', '#0x2,%d0', 2)
    emitter.ins('jmp', '2(%pc, %d0.w)', 4)
    emitter.segment(265540, 265550)
    emitter.ins('move.w', '0x815a:w,%d0', 4)
    emitter.ins('asl.w', '#0x2,%d0', 2)
    emitter.ins('jmp', '2(%pc, %d0.w)', 4)
    emitter.segment(265590, 265596)
    emitter.ins('clr.w', '0x8152:w', 4)
    emitter.ins('rts', '', 2)

def lower_read_object_action_mode(emitter, rules):
    emitter.segment(265512, 265540)
    emitter.ins('moveq', '#0,%d0', 2)
    emitter.ins('move.b', '0x1(%a6),%d0', 4)
    emitter.ins('cmpa.l', '#0xffff826a,%a6', 6)
    emitter.ins('bcs.b', 'scene_pc_040d38', 2)
    emitter.ins('addq.w', '#0x4,%d0', 2)
    emitter.ins('asl.w', '#0x1,%d0', 2)
    emitter.ins('lea.l', '0x812a:w,%a0', 4)
    emitter.ins('move.w', '(%a0, %d0.w),%d0', 4)
    emitter.ins('rts', '', 2)

def lower_probe_scene_object_overlap(emitter, rules):
    emitter.segment(266588, 266658)
    emitter.ins('move.l', '0x2(%a6),%d3', 4)
    emitter.ins('bsr.w', 'scene_pc_0411a2', 4)
    emitter.ins('moveq', '#0,%d0', 2)
    emitter.ins('lea.l', '0x816a:w,%a5', 4)
    emitter.ins('btst.b', '#0x7,(%a5)', 4)
    emitter.ins('beq.b', 'scene_pc_041190', 2)
    emitter.ins('cmpa.l', '%a5,%a6', 2)
    emitter.ins('beq.b', 'scene_pc_041190', 2)
    emitter.ins('move.w', '0x2(%a5),%d1', 4)
    emitter.ins('cmp.w', '0x2(%a6),%d1', 4)
    emitter.ins(rules['object_overlap_horizontal_relation_false_branch'] + '.b', 'scene_pc_041190', 2)
    emitter.ins('move.w', '0x4(%a5),%d1', 4)
    emitter.ins('cmp.w', '0x4(%a6),%d1', 4)
    emitter.ins(rules['object_overlap_vertical_relation_false_branch'] + '.b', 'scene_pc_041190', 2)
    emitter.ins('moveq', '#1,%d0', 2)
    emitter.ins('move.l', '%d3,0x2(%a6)', 4)
    emitter.ins('rts', '', 2)
    emitter.ins('adda.w', '#0x10,%a5', 4)
    emitter.ins('cmpa.l', '#0xffff836a,%a5', 6)
    emitter.ins('bcs.b', 'scene_pc_04116a', 2)
    emitter.ins('move.l', '%d3,0x2(%a6)', 4)
    emitter.ins('rts', '', 2)

def lower_offset_scene_object_position(emitter, rules):
    emitter.segment(266658, 266700)
    emitter.ins('move.w', '%d0,%d2', 2)
    emitter.ins('bpl.w', 'scene_pc_0411b2', 4)
    emitter.ins('andi.w', f"#0x{rules['object_offset_negative_magnitude_mask']:x},%d0", 4)
    emitter.ins('sub.w', '%d0,0x2(%a6)', 4)
    emitter.ins('bra.b', 'scene_pc_0411b6', 2)
    emitter.ins('add.w', '%d0,0x2(%a6)', 4)
    emitter.ins('move.w', '%d1,%d2', 2)
    emitter.ins('bpl.w', 'scene_pc_0411c6', 4)
    emitter.ins('andi.w', f"#0x{rules['object_offset_negative_magnitude_mask']:x},%d1", 4)
    emitter.ins('sub.w', '%d1,0x4(%a6)', 4)
    emitter.ins('bra.b', 'scene_pc_0411ca', 2)
    emitter.ins('add.w', '%d1,0x4(%a6)', 4)
    emitter.ins('rts', '', 2)

def lower_plan_scene_object_action(emitter, rules):
    emitter.segment(266700, 267514)
    emitter.ins('moveq', '#0,%d0', 2)
    emitter.ins('move.b', '0x1(%a6),%d0', 4)
    emitter.ins('cmpa.l', '#0xffff826a,%a6', 6)
    emitter.ins('bcs.w', 'scene_pc_04125c', 4)
    emitter.ins('addq.w', '#0x4,%d0', 2)
    emitter.ins('asl.w', '#0x1,%d0', 2)
    emitter.ins('lea.l', '0x812a:w,%a0', 4)
    emitter.ins('cmpi.w', f"#0x{rules['object_plan_long_range_mode']:x},(%a0, %d0.w)", 6)
    emitter.ins(rules['object_plan_long_mode_relation_false_branch'] + '.w', 'scene_pc_0412da', 4)
    emitter.ins('move.w', '#0x0,0x8000:w', 6)
    emitter.ins('move.w', '#0x1,0x8158:w', 6)
    emitter.ins('move.w', f"#0x{rules['object_plan_mode_short_positive']:x},%d0", 4)
    emitter.ins('move.w', '#0x0,%d1', 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041498', 4)
    emitter.ins('cmpi.b', f"#0x{rules['object_plan_long_range_member']:x},0x1(%a6)", 6)
    emitter.ins(rules['object_plan_member_relation_true_branch'] + '.w', 'scene_pc_041496', 4)
    emitter.ins('move.w', '#0x0,0x8000:w', 6)
    emitter.ins('move.w', '#0x1,0x8158:w', 6)
    emitter.ins('move.w', f"#0x{rules['object_plan_mode_long_distance_0_encoded_041222']:x},%d0", 4)
    emitter.ins('move.w', '#0x0,%d1', 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041464', 4)
    emitter.ins('move.w', f"#0x{rules['object_plan_mode_long_distance_1_encoded_041234']:x},%d0", 4)
    emitter.ins('move.w', '#0x0,%d1', 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041464', 4)
    emitter.ins('move.w', f"#0x{rules['object_plan_mode_long_distance_2_encoded_041246']:x},%d0", 4)
    emitter.ins('move.w', '#0x0,%d1', 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041464', 4)
    emitter.ins('bra.w', 'scene_pc_041496', 4)
    emitter.ins('asl.w', '#0x1,%d0', 2)
    emitter.ins('lea.l', '0x812a:w,%a0', 4)
    emitter.ins('cmpi.w', f"#0x{rules['object_plan_long_range_mode']:x},(%a0, %d0.w)", 6)
    emitter.ins(rules['object_plan_long_mode_relation_false_branch'] + '.w', 'scene_pc_0412da', 4)
    emitter.ins('move.w', '#0x1,0x8000:w', 6)
    emitter.ins('move.w', '#0x0,0x8158:w', 6)
    emitter.ins('move.w', f"#0x{rules['object_plan_mode_short_negative']:x},%d0", 4)
    emitter.ins('move.w', '#0x0,%d1', 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041498', 4)
    emitter.ins('cmpi.b', f"#0x{rules['object_plan_long_range_member']:x},0x1(%a6)", 6)
    emitter.ins(rules['object_plan_member_relation_true_branch'] + '.w', 'scene_pc_041496', 4)
    emitter.ins('move.w', '#0x1,0x8000:w', 6)
    emitter.ins('move.w', '#0x0,0x8158:w', 6)
    emitter.ins('move.w', f"#0x{rules['object_plan_mode_long_distance_0_encoded_0412a0']:x},%d0", 4)
    emitter.ins('move.w', '#0x0,%d1', 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041464', 4)
    emitter.ins('move.w', f"#0x{rules['object_plan_mode_long_distance_1_encoded_0412b2']:x},%d0", 4)
    emitter.ins('move.w', '#0x0,%d1', 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041464', 4)
    emitter.ins('move.w', f"#0x{rules['object_plan_mode_long_distance_2_encoded_0412c4']:x},%d0", 4)
    emitter.ins('move.w', '#0x0,%d1', 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041464', 4)
    emitter.ins('bra.w', 'scene_pc_041496', 4)
    emitter.ins('move.w', '#0x1,0x8000:w', 6)
    emitter.ins('move.w', '#0x0,0x8158:w', 6)
    emitter.ins('move.w', f"#0x{rules['object_plan_short_west']:x},%d0", 4)
    emitter.ins('move.w', '#0x0,%d1', 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041498', 4)
    emitter.ins('move.w', '#0x0,0x8000:w', 6)
    emitter.ins('move.w', '#0x1,0x8158:w', 6)
    emitter.ins('move.w', f"#0x{rules['object_plan_short_east']:x},%d0", 4)
    emitter.ins('move.w', '#0x0,%d1', 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041498', 4)
    emitter.ins('move.w', '#0x2,0x8000:w', 6)
    emitter.ins('move.w', '#0x3,0x8158:w', 6)
    emitter.ins('move.w', '#0x0,%d0', 4)
    emitter.ins('move.w', f"#0x{rules['object_plan_short_south']:x},%d1", 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041498', 4)
    emitter.ins('move.w', '#0x3,0x8000:w', 6)
    emitter.ins('move.w', '#0x6,0x8158:w', 6)
    emitter.ins('move.w', '#0x0,%d0', 4)
    emitter.ins('move.w', f"#0x{rules['object_plan_short_north']:x},%d1", 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041498', 4)
    emitter.ins('cmpi.b', f"#0x{rules['object_plan_long_range_member']:x},0x1(%a6)", 6)
    emitter.ins(rules['object_plan_member_relation_true_branch'] + '.w', 'scene_pc_041496', 4)
    emitter.ins('move.w', '#0x1,0x8000:w', 6)
    emitter.ins('move.w', '#0x0,0x8158:w', 6)
    emitter.ins('move.w', f"#0x{rules['object_plan_long_west_0']:x},%d0", 4)
    emitter.ins('move.w', '#0x0,%d1', 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041464', 4)
    emitter.ins('move.w', f"#0x{rules['object_plan_long_west_1']:x},%d0", 4)
    emitter.ins('move.w', '#0x0,%d1', 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041464', 4)
    emitter.ins('move.w', f"#0x{rules['object_plan_long_west_2']:x},%d0", 4)
    emitter.ins('move.w', '#0x0,%d1', 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041464', 4)
    emitter.ins('move.w', '#0x0,0x8000:w', 6)
    emitter.ins('move.w', '#0x1,0x8158:w', 6)
    emitter.ins('move.w', f"#0x{rules['object_plan_long_east_0']:x},%d0", 4)
    emitter.ins('move.w', '#0x0,%d1', 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041464', 4)
    emitter.ins('move.w', f"#0x{rules['object_plan_long_east_1']:x},%d0", 4)
    emitter.ins('move.w', '#0x0,%d1', 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041464', 4)
    emitter.ins('move.w', f"#0x{rules['object_plan_long_east_2']:x},%d0", 4)
    emitter.ins('move.w', '#0x0,%d1', 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041464', 4)
    emitter.ins('move.w', '#0x2,0x8000:w', 6)
    emitter.ins('move.w', '#0x3,0x8158:w', 6)
    emitter.ins('move.w', '#0x0,%d0', 4)
    emitter.ins('move.w', f"#0x{rules['object_plan_long_south_0']:x},%d1", 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041464', 4)
    emitter.ins('move.w', '#0x0,%d0', 4)
    emitter.ins('move.w', f"#0x{rules['object_plan_long_south_1']:x},%d1", 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041464', 4)
    emitter.ins('move.w', '#0x0,%d0', 4)
    emitter.ins('move.w', f"#0x{rules['object_plan_long_south_2']:x},%d1", 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041464', 4)
    emitter.ins('move.w', '#0x3,0x8000:w', 6)
    emitter.ins('move.w', '#0x6,0x8158:w', 6)
    emitter.ins('move.w', '#0x0,%d0', 4)
    emitter.ins('move.w', f"#0x{rules['object_plan_long_north_0']:x},%d1", 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041464', 4)
    emitter.ins('move.w', '#0x0,%d0', 4)
    emitter.ins('move.w', f"#0x{rules['object_plan_long_north_1']:x},%d1", 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.w', 'scene_pc_041464', 4)
    emitter.ins('move.w', '#0x0,%d0', 4)
    emitter.ins('move.w', f"#0x{rules['object_plan_long_north_2']:x},%d1", 4)
    emitter.ins('bsr.w', 'scene_pc_0414fa', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('beq.w', 'scene_pc_041496', 4)
    emitter.ins('move.l', '%a5,0x815c:w', 4)
    emitter.ins('move.w', '#0x9,0x815a:w', 6)
    emitter.ins('clr.w', '0x8162:w', 4)
    emitter.ins('move.w', '0x2(%a6),0x8164:w', 6)
    emitter.ins('move.w', '0x4(%a6),0x8166:w', 6)
    emitter.ins('clr.w', '0x8168:w', 4)
    emitter.ins('move.w', '0x8000:w,0x8(%a6)', 6)
    emitter.ins('movem.l', '(%a7)+,%d0', 4)
    emitter.ins('move.w', f"#0x{rules['object_plan_long_sound']:x},%d0", 4)
    emitter.ins('jsr', 'scene_pc_00808a:l', 6)
    emitter.ins('rts', '', 2)
    emitter.ins('cmpa.l', '#0xffff816a,%a5', 6)
    emitter.ins('beq.b', 'scene_pc_0414a8', 2)
    emitter.ins('cmpa.l', '#0xffff826a,%a5', 6)
    emitter.ins('bne.b', 'scene_pc_0414d8', 2)
    emitter.ins('cmpi.w', '#0x3,0x814e:w', 6)
    emitter.ins('bne.b', 'scene_pc_0414d8', 2)
    emitter.ins('movem.l', '(%a7)+,%d0', 4)
    emitter.ins('move.w', '0x814c:w,%d0', 4)
    emitter.ins('subq.w', '#0x1,%d0', 2)
    emitter.ins('move.w', '%d0,0x8176:w', 4)
    emitter.ins('move.w', '#0x3,0x813a:w', 6)
    emitter.ins('move.w', '#0x0,0x813c:w', 6)
    emitter.ins('move.w', '#0x1,0x813e:w', 6)
    emitter.ins('move.w', '#0x2,0x8152:w', 6)
    emitter.ins('rts', '', 2)
    emitter.ins('move.l', '%a5,0x815c:w', 4)
    emitter.ins('move.w', '#0x8,0x815a:w', 6)
    emitter.ins('clr.w', '0x8162:w', 4)
    emitter.ins('move.w', '0x8000:w,0x8(%a6)', 6)
    emitter.ins('movem.l', '(%a7)+,%d0', 4)
    emitter.ins('move.w', f"#0x{rules['object_plan_short_sound']:x},%d0", 4)
    emitter.ins('jmp', 'scene_pc_00808a:l', 6)

def lower_probe_opposing_object_overlap(emitter, rules):
    emitter.segment(267514, 267556)
    emitter.ins('bsr.w', 'scene_pc_04115c', 4)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('beq.w', 'scene_pc_041520', 4)
    emitter.ins('cmpa.l', '#0xffff826a,%a6', 6)
    emitter.ins('bcs.b', 'scene_pc_041516', 2)
    emitter.ins('cmpa.l', '#0xffff826a,%a5', 6)
    emitter.ins('bcc.b', 'scene_pc_041520', 2)
    emitter.ins('rts', '', 2)
    emitter.ins('cmpa.l', '#0xffff826a,%a5', 6)
    emitter.ins('bcs.b', 'scene_pc_041520', 2)
    emitter.ins('rts', '', 2)
    emitter.ins('moveq', '#0,%d0', 2)
    emitter.ins('rts', '', 2)

def lower_initialize_scene_object_roster(emitter, rules):
    emitter.segment(268278, 268888)
    emitter.ins('move.w', '#0xff,%d0', 4)
    emitter.ins('lea.l', '0x816a:w,%a6', 4)
    emitter.ins('clr.w', '(%a6)+', 2)
    emitter.ins('dbra', '%d0,scene_pc_0417fe', 4)
    emitter.ins('cmpi.b', '#0x1,0x80da:w', 6)
    emitter.ins('beq.w', 'scene_pc_041a1a', 4)
    emitter.ins('cmpi.b', '#0x2,0x80da:w', 6)
    emitter.ins('beq.w', 'scene_pc_041a1a', 4)
    emitter.ins('clr.w', '0x80e8:w', 4)
    emitter.ins('clr.w', '0x80f4:w', 4)
    emitter.ins('clr.w', '0x80f6:w', 4)
    emitter.ins('clr.w', '0x80f8:w', 4)
    emitter.ins('tst.w', '0x80e4:w', 4)
    emitter.ins('beq.w', 'scene_pc_04194a', 4)
    emitter.ins('move.w', f"#0x{rules['object_roster_initial_count']:x},0x80e8:w", 6)
    emitter.ins('cmpi.w', f"#0x{rules['object_roster_troop_minimum']:x},0x80e4:w", 6)
    emitter.ins(rules['object_roster_minimum_relation_false_branch'] + '.w', 'scene_pc_0418a8', 4)
    emitter.ins('cmpi.w', f"#0x{rules['object_roster_small_troop_bound']:x},0x80e4:w", 6)
    emitter.ins(rules['object_roster_small_relation_false_branch'] + '.b', 'scene_pc_041860', 2)
    emitter.ins('jsr', '-24872(%pc)', 4)
    emitter.ins('andi.w', f"#0x{rules['object_roster_count_random_mask']:x},%d0", 4)
    emitter.ins('cmpi.w', f"#0x{rules['object_roster_small_random_bound']:x},%d0", 4)
    emitter.ins(rules['object_roster_small_accept_relation_false_branch'] + '.b', 'scene_pc_041848', 2)
    emitter.ins('addq.w', f"#0x{rules['object_roster_small_count_bias']:x},%d0", 2)
    emitter.ins('move.w', '%d0,0x80e8:w', 4)
    emitter.ins('bra.w', 'scene_pc_0418a8', 4)
    emitter.ins('cmpi.w', f"#0x{rules['object_roster_medium_troop_bound']:x},0x80e4:w", 6)
    emitter.ins(rules['object_roster_medium_relation_false_branch'] + '.b', 'scene_pc_041880', 2)
    emitter.ins('jsr', '-24904(%pc)', 4)
    emitter.ins('andi.w', f"#0x{rules['object_roster_count_random_mask']:x},%d0", 4)
    emitter.ins('cmpi.w', f"#0x{rules['object_roster_other_random_bound']:x},%d0", 4)
    emitter.ins(rules['object_roster_other_accept_relation_false_branch'] + '.b', 'scene_pc_041868', 2)
    emitter.ins('addq.w', f"#0x{rules['object_roster_medium_count_bias']:x},%d0", 2)
    emitter.ins('move.w', '%d0,0x80e8:w', 4)
    emitter.ins('bra.w', 'scene_pc_0418a8', 4)
    emitter.ins('move.w', f"#0x{rules['object_roster_maximum_count']:x},0x80e8:w", 6)
    emitter.ins('cmpi.w', f"#0x{rules['object_roster_large_troop_bound']:x},0x80e4:w", 6)
    emitter.ins(rules['object_roster_large_relation_false_branch'] + '.b', 'scene_pc_0418a8', 2)
    emitter.ins('jsr', '-24942(%pc)', 4)
    emitter.ins('andi.w', f"#0x{rules['object_roster_count_random_mask']:x},%d0", 4)
    emitter.ins('cmpi.w', f"#0x{rules['object_roster_other_random_bound']:x},%d0", 4)
    emitter.ins(rules['object_roster_other_accept_relation_false_branch'] + '.b', 'scene_pc_04188e', 2)
    emitter.ins('addi.w', f"#0x{rules['object_roster_large_count_bias']:x},%d0", 4)
    emitter.ins('move.w', '%d0,0x80e8:w', 4)
    emitter.ins('bra.w', 'scene_pc_0418a8', 4)
    emitter.ins('bsr.w', 'scene_pc_03f4c2', 4)
    emitter.ins('moveq', f"#{rules['object_roster_partition_0_first_count']},%d0", 2)
    emitter.ins('moveq', f"#{rules['object_roster_partition_0_second_count']},%d1", 2)
    emitter.ins('cmpi.w', f"#0x{rules['object_roster_partition_0_quality']:x},0x8110:w", 6)
    emitter.ins(rules['object_roster_partition_relation_true_branch'] + '.w', 'scene_pc_041904', 4)
    emitter.ins('moveq', f"#{rules['object_roster_partition_1_first_count']},%d0", 2)
    emitter.ins('moveq', f"#{rules['object_roster_partition_1_second_count']},%d1", 2)
    emitter.ins('cmpi.w', f"#0x{rules['object_roster_partition_1_quality']:x},0x8110:w", 6)
    emitter.ins(rules['object_roster_partition_relation_true_branch'] + '.w', 'scene_pc_041904', 4)
    emitter.ins('moveq', f"#{rules['object_roster_partition_2_first_count']},%d0", 2)
    emitter.ins('moveq', f"#{rules['object_roster_partition_2_second_count']},%d1", 2)
    emitter.ins('cmpi.w', f"#0x{rules['object_roster_partition_2_quality']:x},0x8110:w", 6)
    emitter.ins(rules['object_roster_partition_relation_true_branch'] + '.w', 'scene_pc_041904', 4)
    emitter.ins('moveq', f"#{rules['object_roster_partition_3_first_count']},%d0", 2)
    emitter.ins('moveq', f"#{rules['object_roster_partition_3_second_count']},%d1", 2)
    emitter.ins('cmpi.w', f"#0x{rules['object_roster_partition_3_quality']:x},0x8110:w", 6)
    emitter.ins(rules['object_roster_partition_relation_true_branch'] + '.w', 'scene_pc_041904', 4)
    emitter.ins('moveq', f"#{rules['object_roster_partition_4_first_count']},%d0", 2)
    emitter.ins('moveq', f"#{rules['object_roster_partition_4_second_count']},%d1", 2)
    emitter.ins('cmpi.w', f"#0x{rules['object_roster_partition_4_quality']:x},0x8110:w", 6)
    emitter.ins(rules['object_roster_partition_relation_true_branch'] + '.w', 'scene_pc_041904', 4)
    emitter.ins('moveq', f"#{rules['object_roster_partition_5_first_count']},%d0", 2)
    emitter.ins('moveq', f"#{rules['object_roster_partition_5_second_count']},%d1", 2)
    emitter.ins('cmpi.w', f"#0x{rules['object_roster_partition_5_quality']:x},0x8110:w", 6)
    emitter.ins(rules['object_roster_partition_relation_true_branch'] + '.w', 'scene_pc_041904', 4)
    emitter.ins('moveq', f"#{rules['object_roster_partition_last_0']},%d0", 2)
    emitter.ins('moveq', f"#{rules['object_roster_partition_last_1']},%d1", 2)
    emitter.ins('clr.w', '0x80f4:w', 4)
    emitter.ins('clr.w', '0x80f6:w', 4)
    emitter.ins('clr.w', '0x80f8:w', 4)
    emitter.ins('move.w', '0x80e8:w,%d2', 4)
    emitter.ins('sub.w', '%d0,%d2', 2)
    emitter.ins('bpl.b', 'scene_pc_041920', 2)
    emitter.ins('move.w', '0x80e8:w,0x80f4:w', 6)
    emitter.ins('bra.b', 'scene_pc_041934', 2)
    emitter.ins('move.w', '%d0,0x80f4:w', 4)
    emitter.ins('move.w', '%d2,0x80f6:w', 4)
    emitter.ins('sub.w', '%d1,%d2', 2)
    emitter.ins('bmi.b', 'scene_pc_041934', 2)
    emitter.ins('move.w', '%d1,0x80f6:w', 4)
    emitter.ins('move.w', '%d2,0x80f8:w', 4)
    emitter.ins('cmpi.b', '#0x3,0x80db:w', 6)
    emitter.ins('bne.b', 'scene_pc_04194a', 2)
    emitter.ins('clr.w', '0x80f4:w', 4)
    emitter.ins('move.w', '0x80e8:w,0x80f6:w', 6)
    emitter.ins('clr.w', '0x80f8:w', 4)
    emitter.ins('jsr', '-25130(%pc)', 4)
    emitter.ins('andi.w', f"#0x{rules['object_roster_layout_random_mask']:x},%d0", 4)
    emitter.ins('cmpi.w', f"#0x{rules['object_roster_layout_bound']:x},%d0", 4)
    emitter.ins(rules['object_roster_layout_relation_false_branch'] + '.b', 'scene_pc_041934', 2)
    emitter.ins('move.w', '%d0,0x814a:w', 4)
    emitter.ins('asl.w', '#0x2,%d0', 2)
    emitter.ins('lea.l', '248(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('movea.l', '(%a0, %d0.w),%a5', 4)
    emitter.ins('move.w', '0x80f4:w,%d0', 4)
    emitter.ins('move.w', '0x80f6:w,%d1', 4)
    emitter.ins('move.w', '0x80f8:w,%d2', 4)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('lea.l', '0x816a:w,%a6', 4)
    emitter.ins('tst.w', '%d3', 2)
    emitter.ins('bne.b', 'scene_pc_04198c', 2)
    emitter.ins('move.w', '(%a5)+,0x2(%a6)', 4)
    emitter.ins('move.w', '(%a5)+,0x4(%a6)', 4)
    emitter.ins('move.w', '#0x8003,(%a6)', 4)
    emitter.ins('bra.b', 'scene_pc_0419c6', 2)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('beq.b', 'scene_pc_0419a0', 2)
    emitter.ins('move.w', '(%a5)+,0x2(%a6)', 4)
    emitter.ins('move.w', '(%a5)+,0x4(%a6)', 4)
    emitter.ins('move.w', '#0x8002,(%a6)', 4)
    emitter.ins('subq.w', f"#0x{rules['object_roster_member_consume_step']:x},%d0", 2)
    emitter.ins('bra.b', 'scene_pc_0419c6', 2)
    emitter.ins('tst.w', '%d1', 2)
    emitter.ins('beq.b', 'scene_pc_0419b4', 2)
    emitter.ins('move.w', '(%a5)+,0x2(%a6)', 4)
    emitter.ins('move.w', '(%a5)+,0x4(%a6)', 4)
    emitter.ins('move.w', '#0x8001,(%a6)', 4)
    emitter.ins('subq.w', f"#0x{rules['object_roster_member_consume_step']:x},%d1", 2)
    emitter.ins('bra.b', 'scene_pc_0419c6', 2)
    emitter.ins('tst.w', '%d2', 2)
    emitter.ins('beq.b', 'scene_pc_0419d0', 2)
    emitter.ins('move.w', '(%a5)+,0x2(%a6)', 4)
    emitter.ins('move.w', '(%a5)+,0x4(%a6)', 4)
    emitter.ins('subq.w', f"#0x{rules['object_roster_member_consume_step']:x},%d2", 2)
    emitter.ins('move.w', '#0x8000,(%a6)', 4)
    emitter.ins('addq.w', f"#0x{rules['object_roster_member_counter_step']:x},%d3", 2)
    emitter.ins('adda.w', '#0x10,%a6', 4)
    emitter.ins('bra.w', 'scene_pc_04197a', 4)
    emitter.ins('move.w', '0x8104:w,%d0', 4)
    emitter.ins('move.w', '0x8100:w,%d1', 4)
    emitter.ins('mulu.w', '%d0,%d1', 2)
    emitter.ins('divu.w', f"#0x{rules['object_roster_quality_divisor']:x},%d1", 4)
    emitter.ins('move.w', '#0xe,%d0', 4)
    emitter.ins('move.w', '0x80f0:w,%d2', 4)
    emitter.ins('lea.l', '0x817a:w,%a6', 4)
    emitter.ins('move.w', '%d1,0xc(%a6)', 4)
    emitter.ins('move.w', '0x80ec:w,0xe(%a6)', 6)
    emitter.ins('tst.w', '%d2', 2)
    emitter.ins('beq.w', 'scene_pc_041a00', 4)
    emitter.ins('subq.w', f"#0x{rules['object_roster_remainder_consume_step']:x},%d2", 2)
    emitter.ins('addq.w', f"#0x{rules['object_roster_remainder_spread_step']:x},0xe(%a6)", 4)
    emitter.ins('adda.w', '#0x10,%a6', 4)
    emitter.ins('dbra', '%d0,scene_pc_0419ea', 4)
    emitter.ins('move.w', '0x8104:w,%d0', 4)
    emitter.ins('add.w', '0x8108:w,%d0', 4)
    emitter.ins('move.w', '%d0,0x8176:w', 4)
    emitter.ins('move.w', '0x810c:w,0x8178:w', 6)
    emitter.ins('clr.w', '0x814c:w', 4)
    emitter.ins('clr.w', '0x814e:w', 4)
    emitter.ins('clr.w', '0x8150:w', 4)
    emitter.ins('clr.w', '0x8152:w', 4)
    emitter.ins('clr.w', '0x8154:w', 4)
    emitter.ins('clr.w', '0x8156:w', 4)
    emitter.ins('clr.w', '0x8158:w', 4)
    emitter.ins('clr.w', '0x815a:w', 4)
    emitter.ins('clr.w', '0x815c:w', 4)
    emitter.ins('clr.w', '0x815e:w', 4)
    emitter.ins('clr.w', '0x8160:w', 4)
    emitter.ins('clr.w', '0x8162:w', 4)
    emitter.ins('clr.w', '0x8164:w', 4)
    emitter.ins('clr.w', '0x8166:w', 4)
    emitter.ins('clr.w', '0x8168:w', 4)
    emitter.ins('rts', '', 2)

LOWERERS = {
    'distribute_secondary_city_battle_progress': lower_distribute_secondary_city_battle_progress,
    'append_scene_center_marker': lower_append_scene_center_marker,
    'run_scene_object_controller': lower_run_scene_object_controller,
    'integrate_scene_coordinates': lower_integrate_scene_coordinates,
    'initialize_scene_object_video': lower_initialize_scene_object_video,
    'dispatch_scene_object_phase': lower_dispatch_scene_object_phase,
    'normalize_object_squad_size': lower_normalize_object_squad_size,
    'cycle_special_scene_palette': lower_cycle_special_scene_palette,
    'clear_scene_object_label_plane': lower_clear_scene_object_label_plane,
    'advance_scene_object_actions': lower_advance_scene_object_actions,
    'rebuild_depth_sorted_object_queue': lower_rebuild_depth_sorted_object_queue,
    'update_selected_object_action': lower_update_selected_object_action,
    'read_object_action_mode': lower_read_object_action_mode,
    'probe_scene_object_overlap': lower_probe_scene_object_overlap,
    'offset_scene_object_position': lower_offset_scene_object_position,
    'plan_scene_object_action': lower_plan_scene_object_action,
    'probe_opposing_object_overlap': lower_probe_opposing_object_overlap,
    'initialize_scene_object_roster': lower_initialize_scene_object_roster,
}

# B28 actual object controller/video policies point only at sole field bodies.
_OBJECT_FIELD_ROLE_PATHS = {'object_controller_video_mask': {'function': '_scene_object_video_command_fields',
                                  'paths': (('body', 2, 'value', 'args', 2, 'right'),),
                                  'coupled_uses': ()},
 'object_controller_palette_start_shade': {'function': 'run_scene_object_controller_fields',
                                           'paths': (('body', 2, 'body', 10, 'value', 'args', 2),),
                                           'coupled_uses': ()},
 'object_controller_default_action_mode': {'function': 'run_scene_object_controller_fields',
                                           'paths': (('body',
                                                      2,
                                                      'body',
                                                      16,
                                                      'orelse',
                                                      6,
                                                      'body',
                                                      0,
                                                      'value',
                                                      'args',
                                                      4),),
                                           'coupled_uses': ()},
 'object_controller_start_sound': {'function': 'run_scene_object_controller_fields',
                                   'paths': (('body', 2, 'body', 17, 'value', 'args', 2),),
                                   'coupled_uses': ()},
 'object_controller_restart_mask': {'function': 'run_scene_object_controller_fields',
                                    'paths': (('body',
                                               2,
                                               'body',
                                               20,
                                               'body',
                                               14,
                                               'value',
                                               'args',
                                               2,
                                               'right'),
                                              ('body', 2, 'body', 20, 'body', 16, 'test', 'comparators', 0),
                                              ('body', 2, 'body', 20, 'body', 15, 'value', 'args', 3)),
                                    'coupled_uses': ()},
 'object_controller_restart_relation': {'function': 'run_scene_object_controller_fields',
                                        'paths': (('body', 2, 'body', 20, 'body', 16, 'test', 'ops', 0),),
                                        'coupled_uses': ()},
 'object_controller_variant_bound': {'function': 'run_scene_object_controller_fields',
                                     'paths': (('body', 2, 'body', 20, 'body', 19, 'test', 'comparators', 0),
                                               ('body', 2, 'body', 20, 'body', 18, 'value', 'args', 3)),
                                     'coupled_uses': ()},
 'object_controller_variant_relation': {'function': 'run_scene_object_controller_fields',
                                        'paths': (('body', 2, 'body', 20, 'body', 19, 'test', 'ops', 0),),
                                        'coupled_uses': ()},
 'object_controller_variant_step': {'function': 'run_scene_object_controller_fields',
                                    'paths': (('body',
                                               2,
                                               'body',
                                               20,
                                               'body',
                                               19,
                                               'body',
                                               2,
                                               'value',
                                               'args',
                                               3),),
                                    'coupled_uses': ()},
 'object_controller_terminal_phase_relation_0': {'function': 'run_scene_object_controller_fields',
                                                 'paths': (('body',
                                                            2,
                                                            'body',
                                                            20,
                                                            'body',
                                                            8,
                                                            'test',
                                                            'ops',
                                                            0),),
                                                 'coupled_uses': ()},
 'object_controller_terminal_phase_relation_1': {'function': 'run_scene_object_controller_fields',
                                                 'paths': (('body',
                                                            2,
                                                            'body',
                                                            20,
                                                            'body',
                                                            9,
                                                            'body',
                                                            2,
                                                            'test',
                                                            'ops',
                                                            0),),
                                                 'coupled_uses': ()},
 'object_controller_terminal_phase_relation_2': {'function': 'run_scene_object_controller_fields',
                                                 'paths': (('body',
                                                            2,
                                                            'body',
                                                            20,
                                                            'body',
                                                            10,
                                                            'body',
                                                            2,
                                                            'test',
                                                            'ops',
                                                            0),),
                                                 'coupled_uses': ()},
 'object_controller_terminal_phase_relation_3': {'function': 'run_scene_object_controller_fields',
                                                 'paths': (('body',
                                                            2,
                                                            'body',
                                                            20,
                                                            'body',
                                                            11,
                                                            'body',
                                                            2,
                                                            'test',
                                                            'ops',
                                                            0),),
                                                 'coupled_uses': ()},
 'object_controller_terminal_subphase_relation_0': {'function': 'run_scene_object_controller_fields',
                                                    'paths': (('body',
                                                               2,
                                                               'body',
                                                               20,
                                                               'body',
                                                               8,
                                                               'body',
                                                               2,
                                                               'test',
                                                               'ops',
                                                               0),),
                                                    'coupled_uses': ()},
 'object_controller_terminal_subphase_relation_1': {'function': 'run_scene_object_controller_fields',
                                                    'paths': (('body',
                                                               2,
                                                               'body',
                                                               20,
                                                               'body',
                                                               9,
                                                               'body',
                                                               2,
                                                               'body',
                                                               2,
                                                               'test',
                                                               'ops',
                                                               0),),
                                                    'coupled_uses': ()},
 'object_controller_terminal_subphase_relation_2': {'function': 'run_scene_object_controller_fields',
                                                    'paths': (('body',
                                                               2,
                                                               'body',
                                                               20,
                                                               'body',
                                                               10,
                                                               'body',
                                                               2,
                                                               'body',
                                                               2,
                                                               'test',
                                                               'ops',
                                                               0),),
                                                    'coupled_uses': ()},
 'object_controller_final_subphase_relation': {'function': 'run_scene_object_controller_fields',
                                               'paths': (('body',
                                                          2,
                                                          'body',
                                                          20,
                                                          'body',
                                                          11,
                                                          'body',
                                                          2,
                                                          'body',
                                                          2,
                                                          'test',
                                                          'ops',
                                                          0),),
                                               'coupled_uses': ()},
 'object_video_row_stride': {'function': 'initialize_scene_object_video_fields',
                             'paths': (('body', 4, 'body', 8, 'value', 'args', 2),),
                             'coupled_uses': ()}}
ROLE_SPECS = tuple(MenuRole(role.name,_OBJECT_FIELD_ROLE_PATHS[role.name]['function'],
    _OBJECT_FIELD_ROLE_PATHS[role.name]['paths'],role.kind,role.default,role.physical_pcs,
    coupled_uses=_OBJECT_FIELD_ROLE_PATHS[role.name]['coupled_uses']) if role.name in _OBJECT_FIELD_ROLE_PATHS else role
    for role in ROLE_SPECS)

# B31 object roster/normalization/label policies follow their sole full-field bodies.
_OBJECT_ROSTER_FIELD_ROLE_PATHS = {'object_squad_count_cap': {'function': 'normalize_object_squad_size_fields',
                            'paths': (('body', 3, 'body', 8, 'test', 'comparators', 0),
                                      ('body', 3, 'body', 7, 'value', 'args', 3)),
                            'coupled_uses': ()},
 'object_squad_upper_size': {'function': 'normalize_object_squad_size_fields',
                             'paths': (('body', 3, 'body', 12, 'test', 'comparators', 0),
                                       ('body', 3, 'body', 11, 'value', 'args', 3)),
                             'coupled_uses': ()},
 'object_squad_lower_size': {'function': 'normalize_object_squad_size_fields',
                             'paths': (('body', 3, 'body', 14, 'test', 'comparators', 0),
                                       ('body', 3, 'body', 13, 'value', 'args', 3)),
                             'coupled_uses': ()},
 'object_squad_decrease_floor': {'function': 'normalize_object_squad_size_fields',
                                 'paths': (('body', 3, 'body', 14, 'body', 2, 'test', 'comparators', 0),
                                           ('body', 3, 'body', 14, 'body', 1, 'value', 'args', 3)),
                                 'coupled_uses': ()},
 'object_squad_increase_step': {'function': 'normalize_object_squad_size_fields',
                                'paths': (('body', 3, 'body', 6, 'body', 0, 'value', 'args', 3),
                                          ('body', 3, 'body', 12, 'body', 0, 'value', 'args', 3)),
                                'coupled_uses': ()},
 'object_squad_decrease_step': {'function': 'normalize_object_squad_size_fields',
                                'paths': (('body', 3, 'body', 8, 'body', 0, 'value', 'args', 3),
                                          ('body', 3, 'body', 14, 'body', 2, 'body', 0, 'value', 'args', 3)),
                                'coupled_uses': ()},
 'object_squad_cap_relation': {'function': 'normalize_object_squad_size_fields',
                               'paths': (('body', 3, 'body', 8, 'test', 'ops', 0),),
                               'coupled_uses': ()},
 'object_squad_upper_relation': {'function': 'normalize_object_squad_size_fields',
                                 'paths': (('body', 3, 'body', 12, 'test', 'ops', 0),),
                                 'coupled_uses': ()},
 'object_squad_lower_relation': {'function': 'normalize_object_squad_size_fields',
                                 'paths': (('body', 3, 'body', 14, 'test', 'ops', 0),),
                                 'coupled_uses': ()},
 'object_squad_floor_relation': {'function': 'normalize_object_squad_size_fields',
                                 'paths': (('body', 3, 'body', 14, 'body', 2, 'test', 'ops', 0),),
                                 'coupled_uses': ()},
 'object_label_fill_tile': {'function': 'clear_scene_object_label_plane_fields',
                            'paths': (('body', 3, 'value', 'args', 2),),
                            'coupled_uses': ()},
 'object_roster_initial_count': {'function': '_initialize_scene_object_roster_tail_fields',
                                 'paths': (('body', 7, 'body', 0, 'value', 'args', 4),),
                                 'coupled_uses': ()},
 'object_roster_troop_minimum': {'function': '_initialize_scene_object_roster_tail_fields',
                                 'paths': (('body', 7, 'body', 3, 'test', 'comparators', 0),
                                           ('body', 7, 'body', 2, 'value', 'args', 3)),
                                 'coupled_uses': ()},
 'object_roster_small_troop_bound': {'function': '_initialize_scene_object_roster_tail_fields',
                                     'paths': (('body', 7, 'body', 3, 'body', 2, 'test', 'comparators', 0),
                                               ('body', 7, 'body', 3, 'body', 1, 'value', 'args', 3)),
                                     'coupled_uses': ()},
 'object_roster_medium_troop_bound': {'function': '_initialize_scene_object_roster_tail_fields',
                                      'paths': (('body',
                                                 7,
                                                 'body',
                                                 3,
                                                 'body',
                                                 2,
                                                 'orelse',
                                                 2,
                                                 'test',
                                                 'comparators',
                                                 0),
                                                ('body',
                                                 7,
                                                 'body',
                                                 3,
                                                 'body',
                                                 2,
                                                 'orelse',
                                                 1,
                                                 'value',
                                                 'args',
                                                 3)),
                                      'coupled_uses': ()},
 'object_roster_large_troop_bound': {'function': '_initialize_scene_object_roster_tail_fields',
                                     'paths': (('body',
                                                7,
                                                'body',
                                                3,
                                                'body',
                                                2,
                                                'orelse',
                                                2,
                                                'orelse',
                                                3,
                                                'test',
                                                'comparators',
                                                0),
                                               ('body',
                                                7,
                                                'body',
                                                3,
                                                'body',
                                                2,
                                                'orelse',
                                                2,
                                                'orelse',
                                                2,
                                                'value',
                                                'args',
                                                3)),
                                     'coupled_uses': ()},
 'object_roster_maximum_count': {'function': '_initialize_scene_object_roster_tail_fields',
                                 'paths': (('body',
                                            7,
                                            'body',
                                            3,
                                            'body',
                                            2,
                                            'orelse',
                                            2,
                                            'orelse',
                                            0,
                                            'value',
                                            'args',
                                            4),),
                                 'coupled_uses': ()},
 'object_roster_minimum_relation': {'function': '_initialize_scene_object_roster_tail_fields',
                                    'paths': (('body', 7, 'body', 3, 'test', 'ops', 0),),
                                    'coupled_uses': ()},
 'object_roster_small_relation': {'function': '_initialize_scene_object_roster_tail_fields',
                                  'paths': (('body', 7, 'body', 3, 'body', 2, 'test', 'ops', 0),),
                                  'coupled_uses': ()},
 'object_roster_medium_relation': {'function': '_initialize_scene_object_roster_tail_fields',
                                   'paths': (('body', 7, 'body', 3, 'body', 2, 'orelse', 2, 'test', 'ops', 0),),
                                   'coupled_uses': ()},
 'object_roster_large_relation': {'function': '_initialize_scene_object_roster_tail_fields',
                                  'paths': (('body',
                                             7,
                                             'body',
                                             3,
                                             'body',
                                             2,
                                             'orelse',
                                             2,
                                             'orelse',
                                             3,
                                             'test',
                                             'ops',
                                             0),),
                                  'coupled_uses': ()},
 'object_roster_count_random_mask': {'function': '_object_count_draw_fields',
                                     'paths': (('body', 1, 'body', 1, 'value', 'right'),),
                                     'coupled_uses': ()},
 'object_roster_small_random_bound': {'function': '_initialize_scene_object_roster_tail_fields',
                                      'paths': (('body', 7, 'body', 3, 'body', 2, 'body', 0, 'value', 'args', 3),),
                                      'coupled_uses': ()},
 'object_roster_other_random_bound': {'function': '_initialize_scene_object_roster_tail_fields',
                                      'paths': (('body',
                                                 7,
                                                 'body',
                                                 3,
                                                 'body',
                                                 2,
                                                 'orelse',
                                                 2,
                                                 'body',
                                                 0,
                                                 'value',
                                                 'args',
                                                 3),
                                                ('body',
                                                 7,
                                                 'body',
                                                 3,
                                                 'body',
                                                 2,
                                                 'orelse',
                                                 2,
                                                 'orelse',
                                                 3,
                                                 'body',
                                                 0,
                                                 'value',
                                                 'args',
                                                 3)),
                                      'coupled_uses': ()},
 'object_roster_small_accept_relation': {'function': '_object_count_draw_fields',
                                         'paths': (('body', 1, 'body', 4, 'value', 'body', 'ops', 0),),
                                         'coupled_uses': ()},
 'object_roster_other_accept_relation': {'function': '_object_count_draw_fields',
                                         'paths': (('body', 1, 'body', 4, 'value', 'orelse', 'ops', 0),),
                                         'coupled_uses': ()},
 'object_roster_small_count_bias': {'function': '_initialize_scene_object_roster_tail_fields',
                                    'paths': (('body', 7, 'body', 3, 'body', 2, 'body', 0, 'value', 'args', 4),),
                                    'coupled_uses': ()},
 'object_roster_medium_count_bias': {'function': '_initialize_scene_object_roster_tail_fields',
                                     'paths': (('body',
                                                7,
                                                'body',
                                                3,
                                                'body',
                                                2,
                                                'orelse',
                                                2,
                                                'body',
                                                0,
                                                'value',
                                                'args',
                                                4),),
                                     'coupled_uses': ()},
 'object_roster_large_count_bias': {'function': '_initialize_scene_object_roster_tail_fields',
                                    'paths': (('body',
                                               7,
                                               'body',
                                               3,
                                               'body',
                                               2,
                                               'orelse',
                                               2,
                                               'orelse',
                                               3,
                                               'body',
                                               0,
                                               'value',
                                               'args',
                                               4),),
                                    'coupled_uses': ()},
 'object_roster_partition_0_quality': {'function': '_initialize_scene_object_roster_tail_fields',
                                       'paths': (('body', 7, 'body', 5, 'iter', 'elts', 0, 'elts', 0),),
                                       'coupled_uses': ()},
 'object_roster_partition_0_first_count': {'function': '_initialize_scene_object_roster_tail_fields',
                                           'paths': (('body', 7, 'body', 5, 'iter', 'elts', 0, 'elts', 1),),
                                           'coupled_uses': ()},
 'object_roster_partition_0_second_count': {'function': '_initialize_scene_object_roster_tail_fields',
                                            'paths': (('body', 7, 'body', 5, 'iter', 'elts', 0, 'elts', 2),),
                                            'coupled_uses': ()},
 'object_roster_partition_1_quality': {'function': '_initialize_scene_object_roster_tail_fields',
                                       'paths': (('body', 7, 'body', 5, 'iter', 'elts', 1, 'elts', 0),),
                                       'coupled_uses': ()},
 'object_roster_partition_1_first_count': {'function': '_initialize_scene_object_roster_tail_fields',
                                           'paths': (('body', 7, 'body', 5, 'iter', 'elts', 1, 'elts', 1),),
                                           'coupled_uses': ()},
 'object_roster_partition_1_second_count': {'function': '_initialize_scene_object_roster_tail_fields',
                                            'paths': (('body', 7, 'body', 5, 'iter', 'elts', 1, 'elts', 2),),
                                            'coupled_uses': ()},
 'object_roster_partition_2_quality': {'function': '_initialize_scene_object_roster_tail_fields',
                                       'paths': (('body', 7, 'body', 5, 'iter', 'elts', 2, 'elts', 0),),
                                       'coupled_uses': ()},
 'object_roster_partition_2_first_count': {'function': '_initialize_scene_object_roster_tail_fields',
                                           'paths': (('body', 7, 'body', 5, 'iter', 'elts', 2, 'elts', 1),),
                                           'coupled_uses': ()},
 'object_roster_partition_2_second_count': {'function': '_initialize_scene_object_roster_tail_fields',
                                            'paths': (('body', 7, 'body', 5, 'iter', 'elts', 2, 'elts', 2),),
                                            'coupled_uses': ()},
 'object_roster_partition_3_quality': {'function': '_initialize_scene_object_roster_tail_fields',
                                       'paths': (('body', 7, 'body', 5, 'iter', 'elts', 3, 'elts', 0),),
                                       'coupled_uses': ()},
 'object_roster_partition_3_first_count': {'function': '_initialize_scene_object_roster_tail_fields',
                                           'paths': (('body', 7, 'body', 5, 'iter', 'elts', 3, 'elts', 1),),
                                           'coupled_uses': ()},
 'object_roster_partition_3_second_count': {'function': '_initialize_scene_object_roster_tail_fields',
                                            'paths': (('body', 7, 'body', 5, 'iter', 'elts', 3, 'elts', 2),),
                                            'coupled_uses': ()},
 'object_roster_partition_4_quality': {'function': '_initialize_scene_object_roster_tail_fields',
                                       'paths': (('body', 7, 'body', 5, 'iter', 'elts', 4, 'elts', 0),),
                                       'coupled_uses': ()},
 'object_roster_partition_4_first_count': {'function': '_initialize_scene_object_roster_tail_fields',
                                           'paths': (('body', 7, 'body', 5, 'iter', 'elts', 4, 'elts', 1),),
                                           'coupled_uses': ()},
 'object_roster_partition_4_second_count': {'function': '_initialize_scene_object_roster_tail_fields',
                                            'paths': (('body', 7, 'body', 5, 'iter', 'elts', 4, 'elts', 2),),
                                            'coupled_uses': ()},
 'object_roster_partition_5_quality': {'function': '_initialize_scene_object_roster_tail_fields',
                                       'paths': (('body', 7, 'body', 5, 'iter', 'elts', 5, 'elts', 0),),
                                       'coupled_uses': ()},
 'object_roster_partition_5_first_count': {'function': '_initialize_scene_object_roster_tail_fields',
                                           'paths': (('body', 7, 'body', 5, 'iter', 'elts', 5, 'elts', 1),),
                                           'coupled_uses': ()},
 'object_roster_partition_5_second_count': {'function': '_initialize_scene_object_roster_tail_fields',
                                            'paths': (('body', 7, 'body', 5, 'iter', 'elts', 5, 'elts', 2),),
                                            'coupled_uses': ()},
 'object_roster_partition_relation': {'function': '_initialize_scene_object_roster_tail_fields',
                                      'paths': (('body', 7, 'body', 5, 'body', 4, 'test', 'ops', 0),),
                                      'coupled_uses': ()},
 'object_roster_partition_last_0': {'function': '_initialize_scene_object_roster_tail_fields',
                                    'paths': (('body', 7, 'body', 5, 'orelse', 0, 'value', 'args', 2),),
                                    'coupled_uses': ()},
 'object_roster_partition_last_1': {'function': '_initialize_scene_object_roster_tail_fields',
                                    'paths': (('body', 7, 'body', 5, 'orelse', 1, 'value', 'args', 2),),
                                    'coupled_uses': ()},
 'object_roster_layout_random_mask': {'function': '_initialize_scene_object_roster_tail_fields',
                                      'paths': (('body', 9, 'body', 2, 'value', 'right'),),
                                      'coupled_uses': ()},
 'object_roster_layout_bound': {'function': '_initialize_scene_object_roster_tail_fields',
                                'paths': (('body', 9, 'body', 5, 'test', 'comparators', 0),
                                          ('body', 9, 'body', 4, 'value', 'args', 3)),
                                'coupled_uses': ()},
 'object_roster_layout_relation': {'function': '_initialize_scene_object_roster_tail_fields',
                                   'paths': (('body', 9, 'body', 5, 'test', 'ops', 0),),
                                   'coupled_uses': ()},
 'object_roster_member_consume_step': {'function': '_initialize_scene_object_roster_tail_fields',
                                       'paths': (('body', 20, 'body', 3, 'body', 0, 'value', 'args', 4),
                                                 ('body', 20, 'body', 5, 'body', 0, 'value', 'args', 4)),
                                       'coupled_uses': ()},
 'object_roster_member_counter_step': {'function': '_initialize_scene_object_roster_tail_fields',
                                       'paths': (('body', 20, 'body', 6, 'value', 'args', 4),),
                                       'coupled_uses': ()},
 'object_roster_quality_divisor': {'function': '_initialize_scene_object_roster_tail_fields',
                                   'paths': (('body', 24, 'value', 'args', 3),),
                                   'coupled_uses': ()},
 'object_roster_remainder_consume_step': {'function': '_initialize_scene_object_roster_tail_fields',
                                          'paths': (('body', 29, 'body', 3, 'body', 0, 'value', 'args', 4),),
                                          'coupled_uses': ()},
 'object_roster_remainder_spread_step': {'function': '_initialize_scene_object_roster_tail_fields',
                                         'paths': (('body', 29, 'body', 3, 'body', 1, 'value', 'args', 3),),
                                         'coupled_uses': ()}}
ROLE_SPECS = tuple(MenuRole(role.name,_OBJECT_ROSTER_FIELD_ROLE_PATHS[role.name]['function'],
    _OBJECT_ROSTER_FIELD_ROLE_PATHS[role.name]['paths'],role.kind,role.default,role.physical_pcs,
    coupled_uses=_OBJECT_ROSTER_FIELD_ROLE_PATHS[role.name]['coupled_uses']) if role.name in _OBJECT_ROSTER_FIELD_ROLE_PATHS else role
    for role in ROLE_SPECS)

# B32 tight object render/integration/palette values belong to the sole field bodies.
_OBJECT_RENDER_FIELD_ROLE_PATHS = {'object_coordinate_fraction_shift': {'function': 'integrate_scene_coordinates_fields',
                                      'paths': (('body', 2, 'body', 12, 'value', 'args', 2),),
                                      'coupled_uses': ()},
 'object_palette_tick_shift': {'function': 'cycle_special_scene_palette_fields',
                               'paths': (('body', 11, 'value', 'args', 4),),
                               'coupled_uses': ()},
 'object_sprite_capacity': {'function': '_append_object_sprite_fields',
                            'paths': (('body', 9, 'test', 'comparators', 0),
                                      ('body', 30, 'body', 33, 'test', 'comparators', 0),
                                      ('body', 8, 'value', 'args', 3),
                                      ('body', 30, 'body', 32, 'value', 'args', 3)),
                            'coupled_uses': ()},
 'object_sprite_x_origin_bias': {'function': '_append_object_sprite_fields',
                                 'paths': (('body', 16, 'value', 'args', 4),),
                                 'coupled_uses': ()},
 'object_sprite_x_flip_correction': {'function': '_append_object_sprite_fields',
                                     'paths': (('body', 19, 'body', 0, 'value', 'args', 4),),
                                     'coupled_uses': ()},
 'object_center_marker_x_offset': {'function': 'append_scene_center_marker_fields',
                                   'paths': (('body', 5, 'value', 'args', 4),),
                                   'coupled_uses': ()},
 'object_sprite_y_origin_bias': {'function': '_append_object_sprite_fields',
                                 'paths': (('body', 21, 'value', 'args', 4),),
                                 'coupled_uses': ()},
 'object_sprite_y_flip_correction': {'function': '_append_object_sprite_fields',
                                     'paths': (('body', 23, 'body', 0, 'value', 'args', 4),),
                                     'coupled_uses': ()},
 'object_center_marker_y_offset': {'function': 'append_scene_center_marker_fields',
                                   'paths': (('body', 7, 'value', 'args', 4),),
                                   'coupled_uses': ()},
 'object_sprite_count_step': {'function': '_append_object_sprite_fields',
                              'paths': (('body', 30, 'body', 19, 'value', 'args', 3),),
                              'coupled_uses': ()},
 'object_animation_side_bias': {'function': 'draw_active_scene_object_fields',
                                'paths': (('body', 18, 'body', 0, 'value', 'args', 4),),
                                'coupled_uses': ()},
 'object_animation_phase_shift': {'function': 'draw_active_scene_object_fields',
                                  'paths': (('body', 20, 'value', 'args', 4),),
                                  'coupled_uses': ()},
 'object_animation_tick_shift': {'function': 'draw_active_scene_object_fields',
                                 'paths': (('body', 24, 'value', 'args', 4),),
                                 'coupled_uses': ()},
 'object_animation_tick_mask': {'function': 'draw_active_scene_object_fields',
                                'paths': (('body', 25, 'value', 'args', 2, 'right'),),
                                'coupled_uses': ()},
 'object_animation_attributes': {'function': 'draw_active_scene_object_fields',
                                 'paths': (('body', 33, 'value', 'args', 2),),
                                 'coupled_uses': ()}}
ROLE_SPECS = tuple(MenuRole(role.name,_OBJECT_RENDER_FIELD_ROLE_PATHS[role.name]['function'],
    _OBJECT_RENDER_FIELD_ROLE_PATHS[role.name]['paths'],role.kind,role.default,role.physical_pcs,
    coupled_uses=_OBJECT_RENDER_FIELD_ROLE_PATHS[role.name]['coupled_uses']) if role.name in _OBJECT_RENDER_FIELD_ROLE_PATHS else role
    for role in ROLE_SPECS)

# B33 actual complete owners replace legacy role observations; native lowering is not newly authored.
_OBJECT_ACTION_FIELD_ROLE_PATHS = {'object_offset_negative_magnitude_mask': {'function': 'offset_scene_object_position_fields',
                                           'paths': (('body', 3, 'body', 3, 'body', 0, 'value'),)},
 'object_overlap_horizontal_relation': {'function': 'probe_scene_object_overlap_fields',
                                        'paths': (('body',
                                                   8,
                                                   'body',
                                                   3,
                                                   'body',
                                                   1,
                                                   'body',
                                                   4,
                                                   'test',
                                                   'ops',
                                                   0),)},
 'object_overlap_vertical_relation': {'function': 'probe_scene_object_overlap_fields',
                                      'paths': (('body',
                                                 8,
                                                 'body',
                                                 3,
                                                 'body',
                                                 1,
                                                 'body',
                                                 4,
                                                 'body',
                                                 4,
                                                 'value',
                                                 'ops',
                                                 0),)},
 'object_queue_tick_mask': {'function': 'rebuild_depth_sorted_object_queue_fields',
                            'paths': (('body', 5, 'value', 'args', 2, 'right'),
                                      ('body', 6, 'test', 'right'))},
 'object_queue_maximum_depth': {'function': 'rebuild_depth_sorted_object_queue_fields',
                                'paths': (('body', 8, 'value', 'args', 2),)},
 'object_queue_depth_shift': {'function': 'rebuild_depth_sorted_object_queue_fields',
                              'paths': (('body', 9, 'body', 1, 'body', 2, 'body', 2, 'value', 'args', 4),)},
 'object_queue_depth_relation': {'function': 'rebuild_depth_sorted_object_queue_fields',
                                 'paths': (('body', 9, 'body', 1, 'body', 2, 'body', 4, 'test', 'ops', 0),)},
 'object_action_timer_step': {'function': 'advance_scene_object_actions_fields',
                              'paths': (('body', 13, 'value', 'args', 3),)},
 'object_action_slot_step': {'function': 'advance_scene_object_actions_fields',
                             'paths': (('body', 15, 'body', 0, 'value', 'args', 3),)},
 'object_action_class_step': {'function': 'advance_scene_object_actions_fields',
                              'paths': (('body', 15, 'body', 3, 'body', 1, 'value', 'args', 3),)},
 'object_action_side_step': {'function': 'advance_scene_object_actions_fields',
                             'paths': (('body', 15, 'body', 3, 'body', 4, 'body', 1, 'value', 'args', 3),)},
 'object_action_slot_bound': {'function': 'advance_scene_object_actions_fields',
                              'paths': (('body', 15, 'body', 3, 'test', 'comparators', 0),
                                        ('body', 15, 'body', 2, 'value', 'args', 3))},
 'object_action_slot_relation': {'function': 'advance_scene_object_actions_fields',
                                 'paths': (('body', 15, 'body', 3, 'test', 'ops', 0),)},
 'object_action_class_bound': {'function': 'advance_scene_object_actions_fields',
                               'paths': (('body', 15, 'body', 3, 'body', 4, 'test', 'comparators', 0),
                                         ('body', 15, 'body', 3, 'body', 3, 'value', 'args', 3))},
 'object_action_class_relation': {'function': 'advance_scene_object_actions_fields',
                                  'paths': (('body', 15, 'body', 3, 'body', 4, 'test', 'ops', 0),)},
 'object_action_side_bound': {'function': 'advance_scene_object_actions_fields',
                              'paths': (('body',
                                         15,
                                         'body',
                                         3,
                                         'body',
                                         4,
                                         'body',
                                         4,
                                         'test',
                                         'comparators',
                                         0),
                                        ('body', 15, 'body', 3, 'body', 4, 'body', 3, 'value', 'args', 3))},
 'object_action_side_relation': {'function': 'advance_scene_object_actions_fields',
                                 'paths': (('body', 15, 'body', 3, 'body', 4, 'body', 4, 'test', 'ops', 0),)},
 'object_action_slow_class_bound': {'function': 'advance_scene_object_actions_fields',
                                    'paths': (('body', 19, 'test', 'comparators', 0),
                                              ('body', 18, 'value', 'args', 3))},
 'object_action_slow_class_relation': {'function': 'advance_scene_object_actions_fields',
                                       'paths': (('body', 19, 'test', 'ops', 0),)},
 'object_action_slow_timer': {'function': 'advance_scene_object_actions_fields',
                              'paths': (('body', 19, 'body', 0, 'value', 'args', 4),)},
 'object_action_matching_class_relation': {'function': 'advance_scene_object_actions_fields',
                                           'paths': (('body', 15, 'body', 19, 'test', 'ops', 0),)},
 'object_selection_x_limit': {'function': 'update_selected_object_action_fields',
                              'paths': (('body', 25, 'orelse', 3, 'test', 'comparators', 0),
                                        ('body', 25, 'orelse', 2, 'value', 'args', 3))},
 'object_selection_x_relation': {'function': 'update_selected_object_action_fields',
                                 'paths': (('body', 25, 'orelse', 3, 'test', 'ops', 0),)},
 'object_selection_random_mask': {'function': 'update_selected_object_action_fields',
                                  'paths': (('body', 25, 'orelse', 5, 'value', 'args', 2, 'right'),)},
 'object_selection_plan_relation': {'function': 'update_selected_object_action_fields',
                                    'paths': (('body', 25, 'orelse', 6, 'test', 'ops', 0),)}}
ROLE_SPECS = tuple(MenuRole(role.name,_OBJECT_ACTION_FIELD_ROLE_PATHS[role.name]['function'],_OBJECT_ACTION_FIELD_ROLE_PATHS[role.name]['paths'],
    role.kind,role.default,role.physical_pcs,coupled_uses=role.coupled_uses) if role.name in _OBJECT_ACTION_FIELD_ROLE_PATHS else role
    for role in ROLE_SPECS)

# ROSTER_SOLE_TAIL_NORMAL_POLICY_EFFECTS123; physical policies and defaults retained, sole newtail AST paths.

# B34 whole planner roles consume its sole full-field branch plans/finish core.
_OBJECT_PLANNER_FIELD_ROLE_PATHS = {'object_plan_long_range_mode': {'function': 'plan_scene_object_action_fields',
                                 'paths': (('body', 9, 'test', 'comparators', 0),
                                           ('body', 5, 'value', 'args', 3))},
 'object_plan_long_mode_relation': {'function': 'plan_scene_object_action_fields',
                                    'paths': (('body', 9, 'test', 'ops', 0),)},
 'object_plan_long_range_member': {'function': 'plan_scene_object_action_fields',
                                   'paths': (('body', 9, 'body', 5, 'test', 'comparators', 0),
                                             ('body', 13, 'test', 'comparators', 0),
                                             ('body', 9, 'body', 4, 'value', 'args', 3),
                                             ('body', 12, 'value', 'args', 3))},
 'object_plan_member_relation': {'function': 'plan_scene_object_action_fields',
                                 'paths': (('body', 9, 'body', 5, 'test', 'ops', 0),
                                           ('body', 13, 'test', 'ops', 0))},
 'object_plan_mode_short_positive': {'function': 'plan_scene_object_action_fields',
                                     'paths': (('body', 9, 'body', 0, 'value', 'body'),)},
 'object_plan_mode_short_negative': {'function': 'plan_scene_object_action_fields',
                                     'paths': (('body', 9, 'body', 0, 'value', 'orelse'),)},
 'object_plan_mode_long_distance_0': {'function': 'plan_scene_object_action_fields',
                                      'paths': (('body', 9, 'body', 7, 'iter', 'elts', 0, 'elts', 0),)},
 'object_plan_mode_long_distance_1': {'function': 'plan_scene_object_action_fields',
                                      'paths': (('body', 9, 'body', 7, 'iter', 'elts', 1, 'elts', 0),)},
 'object_plan_mode_long_distance_2': {'function': 'plan_scene_object_action_fields',
                                      'paths': (('body', 9, 'body', 7, 'iter', 'elts', 2, 'elts', 0),)},
 'object_plan_short_west': {'function': 'plan_scene_object_action_fields',
                            'paths': (('body', 10, 'iter', 'elts', 0, 'elts', 2),)},
 'object_plan_short_east': {'function': 'plan_scene_object_action_fields',
                            'paths': (('body', 10, 'iter', 'elts', 1, 'elts', 2),)},
 'object_plan_short_south': {'function': 'plan_scene_object_action_fields',
                             'paths': (('body', 10, 'iter', 'elts', 2, 'elts', 3),)},
 'object_plan_short_north': {'function': 'plan_scene_object_action_fields',
                             'paths': (('body', 10, 'iter', 'elts', 3, 'elts', 3),)},
 'object_plan_long_west_0': {'function': 'plan_scene_object_action_fields',
                             'paths': (('body', 14, 'iter', 'elts', 0, 'elts', 2, 'elts', 0, 'elts', 0),)},
 'object_plan_long_west_1': {'function': 'plan_scene_object_action_fields',
                             'paths': (('body', 14, 'iter', 'elts', 0, 'elts', 2, 'elts', 1, 'elts', 0),)},
 'object_plan_long_west_2': {'function': 'plan_scene_object_action_fields',
                             'paths': (('body', 14, 'iter', 'elts', 0, 'elts', 2, 'elts', 2, 'elts', 0),)},
 'object_plan_long_east_0': {'function': 'plan_scene_object_action_fields',
                             'paths': (('body', 14, 'iter', 'elts', 1, 'elts', 2, 'elts', 0, 'elts', 0),)},
 'object_plan_long_east_1': {'function': 'plan_scene_object_action_fields',
                             'paths': (('body', 14, 'iter', 'elts', 1, 'elts', 2, 'elts', 1, 'elts', 0),)},
 'object_plan_long_east_2': {'function': 'plan_scene_object_action_fields',
                             'paths': (('body', 14, 'iter', 'elts', 1, 'elts', 2, 'elts', 2, 'elts', 0),)},
 'object_plan_long_south_0': {'function': 'plan_scene_object_action_fields',
                              'paths': (('body', 14, 'iter', 'elts', 2, 'elts', 2, 'elts', 0, 'elts', 1),)},
 'object_plan_long_south_1': {'function': 'plan_scene_object_action_fields',
                              'paths': (('body', 14, 'iter', 'elts', 2, 'elts', 2, 'elts', 1, 'elts', 1),)},
 'object_plan_long_south_2': {'function': 'plan_scene_object_action_fields',
                              'paths': (('body', 14, 'iter', 'elts', 2, 'elts', 2, 'elts', 2, 'elts', 1),)},
 'object_plan_long_north_0': {'function': 'plan_scene_object_action_fields',
                              'paths': (('body', 14, 'iter', 'elts', 3, 'elts', 2, 'elts', 0, 'elts', 1),)},
 'object_plan_long_north_1': {'function': 'plan_scene_object_action_fields',
                              'paths': (('body', 14, 'iter', 'elts', 3, 'elts', 2, 'elts', 1, 'elts', 1),)},
 'object_plan_long_north_2': {'function': 'plan_scene_object_action_fields',
                              'paths': (('body', 14, 'iter', 'elts', 3, 'elts', 2, 'elts', 2, 'elts', 1),)},
 'object_plan_short_sound': {'function': '_object_planner_finish_fields',
                             'paths': (('body', 9, 'value', 'args', 2, 'orelse'),)},
 'object_plan_long_sound': {'function': '_object_planner_finish_fields',
                            'paths': (('body', 9, 'value', 'args', 2, 'body'),)}}
ROLE_SPECS = tuple(MenuRole(role.name,_OBJECT_PLANNER_FIELD_ROLE_PATHS[role.name]['function'],
    _OBJECT_PLANNER_FIELD_ROLE_PATHS[role.name]['paths'],role.kind,role.default,role.physical_pcs,
    coupled_uses=role.coupled_uses) if role.name in _OBJECT_PLANNER_FIELD_ROLE_PATHS else role for role in ROLE_SPECS)

# B35 selection middle/direct-route role positions remain actual field observations.
_OBJECT_ACTION_FIELD_ROLE_PATHS = {'object_offset_negative_magnitude_mask': {'function': 'offset_scene_object_position_fields',
                                           'paths': (('body', 3, 'body', 3, 'body', 0, 'value'),)},
 'object_overlap_horizontal_relation': {'function': 'probe_scene_object_overlap_fields',
                                        'paths': (('body',
                                                   8,
                                                   'body',
                                                   3,
                                                   'body',
                                                   1,
                                                   'body',
                                                   4,
                                                   'test',
                                                   'ops',
                                                   0),)},
 'object_overlap_vertical_relation': {'function': 'probe_scene_object_overlap_fields',
                                      'paths': (('body',
                                                 8,
                                                 'body',
                                                 3,
                                                 'body',
                                                 1,
                                                 'body',
                                                 4,
                                                 'body',
                                                 4,
                                                 'value',
                                                 'ops',
                                                 0),)},
 'object_queue_tick_mask': {'function': 'rebuild_depth_sorted_object_queue_fields',
                            'paths': (('body', 5, 'value', 'args', 2, 'right'),
                                      ('body', 6, 'test', 'right'))},
 'object_queue_maximum_depth': {'function': 'rebuild_depth_sorted_object_queue_fields',
                                'paths': (('body', 8, 'value', 'args', 2),)},
 'object_queue_depth_shift': {'function': 'rebuild_depth_sorted_object_queue_fields',
                              'paths': (('body', 9, 'body', 1, 'body', 2, 'body', 2, 'value', 'args', 4),)},
 'object_queue_depth_relation': {'function': 'rebuild_depth_sorted_object_queue_fields',
                                 'paths': (('body', 9, 'body', 1, 'body', 2, 'body', 4, 'test', 'ops', 0),)},
 'object_action_timer_step': {'function': 'advance_scene_object_actions_fields',
                              'paths': (('body', 13, 'value', 'args', 3),)},
 'object_action_slot_step': {'function': 'advance_scene_object_actions_fields',
                             'paths': (('body', 15, 'body', 0, 'value', 'args', 3),)},
 'object_action_class_step': {'function': 'advance_scene_object_actions_fields',
                              'paths': (('body', 15, 'body', 3, 'body', 1, 'value', 'args', 3),)},
 'object_action_side_step': {'function': 'advance_scene_object_actions_fields',
                             'paths': (('body', 15, 'body', 3, 'body', 4, 'body', 1, 'value', 'args', 3),)},
 'object_action_slot_bound': {'function': 'advance_scene_object_actions_fields',
                              'paths': (('body', 15, 'body', 3, 'test', 'comparators', 0),
                                        ('body', 15, 'body', 2, 'value', 'args', 3))},
 'object_action_slot_relation': {'function': 'advance_scene_object_actions_fields',
                                 'paths': (('body', 15, 'body', 3, 'test', 'ops', 0),)},
 'object_action_class_bound': {'function': 'advance_scene_object_actions_fields',
                               'paths': (('body', 15, 'body', 3, 'body', 4, 'test', 'comparators', 0),
                                         ('body', 15, 'body', 3, 'body', 3, 'value', 'args', 3))},
 'object_action_class_relation': {'function': 'advance_scene_object_actions_fields',
                                  'paths': (('body', 15, 'body', 3, 'body', 4, 'test', 'ops', 0),)},
 'object_action_side_bound': {'function': 'advance_scene_object_actions_fields',
                              'paths': (('body',
                                         15,
                                         'body',
                                         3,
                                         'body',
                                         4,
                                         'body',
                                         4,
                                         'test',
                                         'comparators',
                                         0),
                                        ('body', 15, 'body', 3, 'body', 4, 'body', 3, 'value', 'args', 3))},
 'object_action_side_relation': {'function': 'advance_scene_object_actions_fields',
                                 'paths': (('body', 15, 'body', 3, 'body', 4, 'body', 4, 'test', 'ops', 0),)},
 'object_action_slow_class_bound': {'function': 'advance_scene_object_actions_fields',
                                    'paths': (('body', 19, 'test', 'comparators', 0),
                                              ('body', 18, 'value', 'args', 3))},
 'object_action_slow_class_relation': {'function': 'advance_scene_object_actions_fields',
                                       'paths': (('body', 19, 'test', 'ops', 0),)},
 'object_action_slow_timer': {'function': 'advance_scene_object_actions_fields',
                              'paths': (('body', 19, 'body', 0, 'value', 'args', 4),)},
 'object_action_matching_class_relation': {'function': 'advance_scene_object_actions_fields',
                                           'paths': (('body', 15, 'body', 19, 'test', 'ops', 0),)},
 'object_selection_x_limit': {'function': 'update_selected_object_action_fields',
                              'paths': (('body', 26, 'orelse', 3, 'test', 'comparators', 0),
                                        ('body', 26, 'orelse', 2, 'value', 'args', 3))},
 'object_selection_x_relation': {'function': 'update_selected_object_action_fields',
                                 'paths': (('body', 26, 'orelse', 3, 'test', 'ops', 0),)},
 'object_selection_random_mask': {'function': 'update_selected_object_action_fields',
                                  'paths': (('body', 26, 'orelse', 5, 'value', 'args', 2, 'right'),)},
 'object_selection_plan_relation': {'function': 'update_selected_object_action_fields',
                                    'paths': (('body', 26, 'orelse', 6, 'test', 'ops', 0),)}}
ROLE_SPECS = tuple(MenuRole(role.name,_OBJECT_ACTION_FIELD_ROLE_PATHS[role.name]['function'],_OBJECT_ACTION_FIELD_ROLE_PATHS[role.name]['paths'],
    role.kind,role.default,role.physical_pcs,coupled_uses=role.coupled_uses) if role.name in _OBJECT_ACTION_FIELD_ROLE_PATHS else role
    for role in ROLE_SPECS)
