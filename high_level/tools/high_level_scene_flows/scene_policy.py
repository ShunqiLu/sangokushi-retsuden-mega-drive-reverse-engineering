"""Complete finite source-driven scene/display family lowering.

The supplied logical business/helper bodies are the sole semantic input to
the parent's complete AST matcher. Roles name precise policy uses; coupled
helper uses have one edit authority. All 26 physical owners retain ordinary
typed-operation lowering, including noncontiguous/shared continuation spans.
No old business/ASM/ROM/IR/object is read during generation. This is a finite
editable language, not arbitrary Python or full natural gameplay validation.

Live ordering, BYTE/WORD partial carriers, signed addressing, DBRA inclusion,
SR/hardware boundaries, record and resource topology, command formats and
nonlocal continuations remain fixed. Edited table counts/thresholds do not
prove that externally supplied media cover the new natural selection domain.
Original quirks are preserved, not repaired by these policies.
"""
from .policy_common import SourceRole as MenuRole
from .compiler_common import CompileError


ROLE_SPECS = (
    MenuRole('queue_nonempty_relation', 'flush_scene_transfer_queue', (('body', 3, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (44298,),
        coupled_uses=()),
    MenuRole('packet_wrap_width', 'write_vdp_packet_stream', (('body', 4, 'body', 3, 'body', 4, 'value', 'test', 'comparators', 0), ('body', 4, 'body', 3, 'body', 4, 'value', 'body', 'args', 0, 'right'), ('body', 4, 'body', 3, 'orelse', 2, 'body', 1, 'value', 'test', 'comparators', 0), ('body', 4, 'body', 3, 'orelse', 2, 'body', 1, 'value', 'body', 'args', 0, 'right')),
        'nonzero_word', 64, (44356, 44390),
        coupled_uses=()),
    MenuRole('dictionary_literal_ceiling', 'write_vdp_dictionary_repeat_stream', (('body', 5, 'body', 1, 'test', 'comparators', 0), ('body', 5, 'body', 1, 'orelse', 0, 'body', 1, 'orelse', 0, 'test', 'comparators', 0), ('body', 5, 'body', 1, 'orelse', 0, 'orelse', 2, 'test', 'left')),
        'word', 65024, (44562, 44602, 44642),
        coupled_uses=()),
    MenuRole('dictionary_repeat_ceiling', 'write_vdp_dictionary_repeat_stream', (('body', 5, 'body', 1, 'orelse', 0, 'test', 'comparators', 0), ('body', 5, 'body', 1, 'orelse', 0, 'body', 1, 'test', 'comparators', 0), ('body', 5, 'body', 1, 'orelse', 0, 'orelse', 2, 'test', 'comparators', 1)),
        'word', 65280, (44580, 44596, 44636),
        coupled_uses=()),
    MenuRole('glyph_row_longs', 'decode_glyph_rows_to_buffers', (('body', 8, 'body', 1, 'body', 2, 'iter', 'args', 0), ('body', 8, 'body', 1, 'orelse', 2, 'iter', 'args', 0)),
        'nonzero_word', 16, (44722, 44780),
        coupled_uses=()),
    MenuRole('glyph_fill_nibbles', 'decode_glyph_rows_to_buffers', (('body', 8, 'body', 1, 'orelse', 1, 'iter', 'args', 0),),
        'nonzero_word', 8, (44764,),
        coupled_uses=()),
    MenuRole('glyph_fill_nibble_shift', 'decode_glyph_rows_to_buffers', (('body', 8, 'body', 1, 'orelse', 1, 'body', 0, 'value', 'left', 'args', 0, 'right'), ('body', 8, 'body', 1, 'orelse', 1, 'body', 1, 'value', 'left', 'args', 0, 'right')),
        'shift', 4, (44768, 44770),
        coupled_uses=()),
    MenuRole('darken_nibble_rotation', 'darken_palette_component', (('body', 2, 'value', 'args', 1), ('body', 3, 'value', 'args', 1)),
        'shift', 4, (57076, 57078, 57034),
        coupled_uses=(('darken_palette', ('body', 13, 'body', 0, 'value', 'args', 1, 'args', 0, 'right')),)),
    MenuRole('palette_component_mask', '_advance_scene_palette_fade_core', (('body', 16, 'value', 'args', 1, 'right'),),
        'word', 14, (57082, 240140, 240062),
        coupled_uses=(('darken_palette_component', ('body', 5, 'value', 'args', 1, 'right')), ('fade_palette_component', ('body', 3, 'value', 'args', 1, 'right')))),
    MenuRole('palette_shade_ceiling', '_begin_scene_palette_darken_core', (('body', 2, 'value'),),
        'word', 15, (56998, 240028, 240174),
        coupled_uses=(('_advance_scene_palette_fade_core', ('body', 14, 'orelse', 2, 'test', 'comparators', 0)), ('darken_palette', ('body', 8, 'test', 'comparators', 0)))),
    MenuRole('darken_hang_relation', 'darken_palette', (('body', 8, 'test', 'ops', 0),),
        'unsigned_relation', '>', (57002,),
        coupled_uses=()),
    MenuRole('darken_round_step', 'darken_palette', (('body', 10, 'body', 0, 'body', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (57024,),
        coupled_uses=()),
    MenuRole('darken_dirty_step', 'darken_palette', (('body', 14, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (57054,),
        coupled_uses=()),
    MenuRole('palette_period_keep_mask', '_begin_scene_palette_darken_core', (('body', 3, 'value', 'args', 1, 'right'),),
        'word', 255, (240160, 240008),
        coupled_uses=(('_advance_scene_palette_fade_core', ('body', 12, 'value', 'args', 1, 'right')),)),
    MenuRole('palette_snapshot_longs', 'snapshot_and_clear_scene_palette', (('body', 2, 'iter', 'args', 0),),
        'nonzero_word', 32, (240266,),
        coupled_uses=()),
    MenuRole('palette_delay_step', '_advance_scene_palette_fade_core', (('body', 6, 'value'),),
        'quick', 1, (240000,),
        coupled_uses=()),
    MenuRole('palette_shade_step', '_advance_scene_palette_fade_core', (('body', 14, 'body', 0, 'value', 'args', 0, 'right'), ('body', 14, 'orelse', 0, 'value', 'args', 0, 'right')),
        'quick', 1, (240042, 240024),
        coupled_uses=()),
    MenuRole('palette_shade_end_relation', '_advance_scene_palette_fade_core', (('body', 14, 'orelse', 2, 'test', 'ops', 0),),
        'unsigned_relation', '>', (240034,),
        coupled_uses=()),
    MenuRole('fade_nibble_rotation', '_advance_scene_palette_fade_core', (('body', 20, 'body', 3, 'body', 3, 'body', 3, 'value', 'args', 1),),
        'shift', 4, (240154, 240156, 240116),
        coupled_uses=(('fade_palette_component', ('body', 9, 'value', 'args', 1)), ('fade_palette_component', ('body', 10, 'value', 'args', 1, 'right')))),
    MenuRole('word_stream_marker_relation', 'write_vdp_word_rle_stream', (('body', 5, 'body', 1, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (235114,),
        coupled_uses=()),
    MenuRole('swapped_stream_marker_relation', '_write_vdp_swapped_byte_rle_core', (('body', 8, 'body', 1, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (240484,),
        coupled_uses=()),
    MenuRole('plane_stream_marker_relation', '_read_vdp_plane_rle_rows_core', (('body', 13, 'body', 2, 'value', 'values', 1, 'ops', 0),),
        'unsigned_relation', '!=', (240380,),
        coupled_uses=()),
    MenuRole('plane_column_step', 'advance_plane_row', (('body', 2, 'value', 'elts', 0),),
        'quick', 1, (240434,),
        coupled_uses=()),
    MenuRole('plane_column_bound', 'advance_plane_row', (('body', 2, 'value', 'elts', 1),),
        'byte', 32, (240436,),
        coupled_uses=()),
    MenuRole('plane_column_end_relation', 'advance_plane_row', (('body', 8, 'test', 'ops', 0),),
        'unsigned_relation', '>=', (240440,),
        coupled_uses=()),
    MenuRole('plane_row_step', 'advance_plane_row', (('body', 2, 'value', 'elts', 2),),
        'quick', 1, (240444,),
        coupled_uses=()),
    MenuRole('plane_initial_rows', '_read_vdp_plane_rle_rows_core', (('body', 6, 'value'),),
        'word', 32, (240338,),
        coupled_uses=()),
    MenuRole('scene_chain_nonempty_relation', 'finish_one_actor_sprite_chain', (('body', 5, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (239504, 242294),
        coupled_uses=(('finish_one_scene_sprite_chain', ('body', 4, 'test', 'ops', 0)),)),
    MenuRole('sprite_capacity', '_append_scene_sprites', (('body', 4, 'test', 'comparators', 0), ('body', 16, 'body', 3, 'body', 2, 'body', 1, 'test', 'comparators', 0), ('body', 16, 'body', 7, 'body', 3, 'body', 1, 'test', 'comparators', 0), ('body', 16, 'body', 22, 'test', 'comparators', 0)),
        'byte', 128, (239012, 239366, 239526, 239756),
        coupled_uses=()),
    MenuRole('sprite_capacity_relation', '_append_scene_sprites', (('body', 4, 'test', 'ops', 0), ('body', 16, 'body', 3, 'body', 2, 'body', 1, 'test', 'ops', 0), ('body', 16, 'body', 7, 'body', 3, 'body', 1, 'test', 'ops', 0), ('body', 16, 'body', 22, 'test', 'ops', 0)),
        'unsigned_relation', '>=', (239018, 239372, 239532, 239762),
        coupled_uses=()),
    MenuRole('sprite_origin', '_append_scene_sprites', (('body', 8, 'value', 'args', 1, 'args', 0, 'right'), ('body', 11, 'value', 'args', 1, 'args', 0, 'right')),
        'word', 128, (239040, 239058, 239554, 239572),
        coupled_uses=()),
    MenuRole('sprite_flip_adjustment', '_append_scene_sprites', (('body', 10, 'body', 0, 'value', 'args', 1, 'args', 0, 'right'), ('body', 12, 'body', 0, 'value', 'args', 1, 'args', 0, 'right')),
        'word', 8, (239054, 239068, 239568, 239582),
        coupled_uses=()),
    MenuRole('sprite_horizontal_flip_bit', '_append_scene_sprites', (('body', 10, 'test', 'right'), ('body', 16, 'body', 4, 'value', 'args', 2, 'args', 0, 'right')),
        'long_bit', 32, (239048, 239172, 239562, 239622),
        coupled_uses=()),
    MenuRole('sprite_vertical_flip_bit', '_append_scene_sprites', (('body', 12, 'test', 'right'), ('body', 16, 'body', 8, 'value', 'args', 1, 'args', 2, 'args', 0, 'right')),
        'long_bit', 16, (239062, 239268, 239576, 239654),
        coupled_uses=()),
    MenuRole('sprite_clip_minimum', '_append_scene_sprites', (('body', 16, 'body', 3, 'body', 1, 'test', 'values', 0, 'comparators', 0), ('body', 16, 'body', 7, 'body', 2, 'test', 'values', 0, 'comparators', 0)),
        'word', 16, (239142, 239238),
        coupled_uses=()),
    MenuRole('sprite_clip_x_maximum', '_append_scene_sprites', (('body', 16, 'body', 3, 'body', 1, 'test', 'values', 1, 'comparators', 0),),
        'word', 112, (239150,),
        coupled_uses=()),
    MenuRole('sprite_clip_y_maximum', '_append_scene_sprites', (('body', 16, 'body', 7, 'body', 2, 'test', 'values', 1, 'comparators', 0),),
        'word', 160, (239246,),
        coupled_uses=()),
    MenuRole('sprite_clip_minimum_relation', '_append_scene_sprites', (('body', 16, 'body', 3, 'body', 1, 'test', 'values', 0, 'ops', 0), ('body', 16, 'body', 7, 'body', 2, 'test', 'values', 0, 'ops', 0)),
        'unsigned_relation', '<', (239146, 239242),
        coupled_uses=()),
    MenuRole('sprite_clip_x_maximum_relation', '_append_scene_sprites', (('body', 16, 'body', 3, 'body', 1, 'test', 'values', 1, 'ops', 0),),
        'unsigned_relation', '>', (239154,),
        coupled_uses=()),
    MenuRole('sprite_clip_y_maximum_relation', '_append_scene_sprites', (('body', 16, 'body', 7, 'body', 2, 'test', 'values', 1, 'ops', 0),),
        'unsigned_relation', '>', (239250,),
        coupled_uses=()),
    MenuRole('sprite_count_step', '_append_scene_sprites', (('body', 16, 'body', 12, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (239334, 239724),
        coupled_uses=()),
    MenuRole('sprite_palette_keep_mask', '_append_scene_sprites', (('body', 16, 'body', 13, 'value', 'right'),),
        'byte', 240, (239342, 239732),
        coupled_uses=()),
    MenuRole('sprite_palette_shift', '_append_scene_sprites', (('body', 16, 'body', 16, 'value', 'args', 0, 'right'),),
        'shift', 7, (239350, 239740),
        coupled_uses=()),
    MenuRole('marker_origin_adjustment', 'append_scene_marker_sprite', (('body', 3, 'value', 'args', 0, 'args', 1, 'args', 0, 'right'), ('body', 3, 'value', 'args', 1, 'args', 1, 'args', 0, 'right')),
        'word', 64, (239406, 239410),
        coupled_uses=()),
    MenuRole('movement_tick_mask', 'update_scripted_scene_position', (('body', 1, 'test', 'right'),),
        'word', 7, (236000,),
        coupled_uses=()),
    MenuRole('movement_counter_step', 'update_scripted_scene_position', (('body', 3, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (236018,),
        coupled_uses=()),
    MenuRole('movement_limit_relation', 'update_scripted_scene_position', (('body', 7, 'test', 'ops', 0),),
        'unsigned_relation', '>', (236048,),
        coupled_uses=()),
    MenuRole('movement_distance_mask', 'update_scripted_scene_position', (('body', 9, 'value', 'right'),),
        'byte', 15, (236100, 236116, 236132, 236148),
        coupled_uses=()),
    MenuRole('movement_left_bit', 'update_scripted_scene_position', (('body', 10, 'test', 'right'),),
        'long_bit', 16, (236060,),
        coupled_uses=()),
    MenuRole('movement_right_bit', 'update_scripted_scene_position', (('body', 10, 'orelse', 0, 'test', 'right'),),
        'long_bit', 32, (236068,),
        coupled_uses=()),
    MenuRole('movement_up_bit', 'update_scripted_scene_position', (('body', 10, 'orelse', 0, 'orelse', 0, 'test', 'right'),),
        'long_bit', 64, (236076,),
        coupled_uses=()),
    MenuRole('movement_down_bit', 'update_scripted_scene_position', (('body', 10, 'orelse', 0, 'orelse', 0, 'orelse', 0, 'test', 'right'),),
        'long_bit', 128, (236084,),
        coupled_uses=()),
    MenuRole('secondary_latched_relation', 'initialize_scripted_secondary_position', (('body', 2, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (237342,),
        coupled_uses=()),
    MenuRole('secondary_latch_value', 'initialize_scripted_secondary_position', (('body', 8, 'value', 'args', 1),),
        'word', 1, (237376,),
        coupled_uses=()),
    MenuRole('frame_direct_mode_bound', 'select_scene_object_frame', (('body', 3, 'test', 'comparators', 0),),
        'word', 27, (237706,),
        coupled_uses=()),
    MenuRole('frame_direct_mode_relation', 'select_scene_object_frame', (('body', 3, 'test', 'ops', 0),),
        'unsigned_relation', '<=', (237714,),
        coupled_uses=()),
    MenuRole('frame_sequence_bound', 'select_scene_object_frame', (('body', 4, 'test', 'comparators', 0),),
        'word', 7, (237724,),
        coupled_uses=()),
    MenuRole('frame_sequence_relation', 'select_scene_object_frame', (('body', 4, 'test', 'ops', 0),),
        'unsigned_relation', '<=', (237728,),
        coupled_uses=()),
    MenuRole('frame_sequence_tick_mask', 'select_scene_object_frame', (('body', 4, 'body', 1, 'test', 'left', 'right'),),
        'word', 7, (237738,),
        coupled_uses=()),
    MenuRole('frame_sequence_step', 'select_scene_object_frame', (('body', 4, 'body', 1, 'body', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (237746,),
        coupled_uses=()),
    MenuRole('frame_sequence_terminator', 'select_scene_object_frame', (('body', 4, 'body', 3, 'test', 'comparators', 0),),
        'byte', 255, (237768,),
        coupled_uses=()),
    MenuRole('frame_lookup_keep_mask', 'select_scene_object_frame', (('body', 5, 'value'),),
        'long', 15, (237784,),
        coupled_uses=()),
    MenuRole('script_palette_longs', '_copy_scene_palette_longs', (('body', 1, 'iter', 'args', 0),),
        'nonzero_word', 8, (235446, 235652, 235864, 237046, 238256, 238470),
        coupled_uses=()),
    MenuRole('script_palette_words', '_copy_scene_palette_words', (('body', 1, 'iter', 'args', 0),),
        'nonzero_word', 16, (235946, 235980),
        coupled_uses=()),
    MenuRole('script_fixed_x', '_draw_fixed_scene_pointer', (('body', 1, 'value', 'args', 2, 'args', 0),),
        'word', 96, (236352, 236380, 236648, 236824, 237060, 237430, 237982, 238014, 238274, 238488, 238616, 238660, 238736, 238764, 238804, 238832, 238872),
        coupled_uses=(('_draw_scripted_staged_pair', ('body', 4, 'value', 'args', 2, 'args', 0)),)),
    MenuRole('script_fixed_y', '_draw_fixed_scene_pointer', (('body', 1, 'value', 'args', 2, 'args', 1),),
        'word', 96, (236356, 236384, 236652, 236828, 237064, 237434, 237986, 238018, 238278, 238492, 238620, 238664, 238740, 238768, 238808, 238836, 238876),
        coupled_uses=(('_draw_scripted_staged_pair', ('body', 4, 'value', 'args', 2, 'args', 1)),)),
    MenuRole('script_sequence_tick_mask', '_draw_scripted_sequence', (('body', 0, 'test', 'left', 'right'), ('body', 2, 'body', 0, 'body', 1, 'test', 'left', 'right')),
        'word', 7, (235538, 235816),
        coupled_uses=()),
    MenuRole('script_sequence_step', '_draw_scripted_sequence', (('body', 0, 'body', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (235546,),
        coupled_uses=()),
    MenuRole('script_sequence_palette_frame', '_draw_scripted_sequence', (('body', 2, 'body', 0, 'test', 'comparators', 0),),
        'word', 3, (235804,),
        coupled_uses=()),
    MenuRole('script_sequence_palette_frame_relation', '_draw_scripted_sequence', (('body', 2, 'body', 0, 'test', 'ops', 0),),
        'unsigned_relation', '>=', (235808,),
        coupled_uses=()),
    MenuRole('script_sequence_palette_stop', '_draw_scripted_sequence', (('body', 2, 'body', 0, 'body', 1, 'body', 0, 'test', 'comparators', 0),),
        'word', 40, (235824,),
        coupled_uses=()),
    MenuRole('script_sequence_palette_stop_relation', '_draw_scripted_sequence', (('body', 2, 'body', 0, 'body', 1, 'body', 0, 'test', 'ops', 0),),
        'unsigned_relation', '==', (235832,),
        coupled_uses=()),
    MenuRole('script_sequence_palette_step', '_draw_scripted_sequence', (('body', 2, 'body', 0, 'body', 1, 'body', 0, 'orelse', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 4, (235836,),
        coupled_uses=()),
    MenuRole('script_first_frame', '_draw_scripted_sequence', (('body', 3, 'body', 0, 'value', 'test', 'comparators', 0),),
        'word', 1, (235630,),
        coupled_uses=()),
    MenuRole('script_first_frame_relation', '_draw_scripted_sequence', (('body', 3, 'body', 0, 'value', 'test', 'ops', 0),),
        'unsigned_relation', '==', (235634,),
        coupled_uses=()),
    MenuRole('script_other_frame_palette_offset', '_draw_scripted_sequence', (('body', 3, 'body', 0, 'value', 'orelse'),),
        'word', 32, (235638,),
        coupled_uses=()),
    MenuRole('script_arrival_step', '_draw_scripted_arrival', (('body', 0, 'body', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (236316,),
        coupled_uses=()),
    MenuRole('script_arrival_count', '_draw_scripted_arrival', (('body', 0, 'body', 1, 'test', 'comparators', 0), ('body', 0, 'body', 2, 'test', 'comparators', 0)),
        'word', 144, (236322, 236334),
        coupled_uses=()),
    MenuRole('script_arrival_equal_relation', '_draw_scripted_arrival', (('body', 0, 'body', 1, 'test', 'ops', 0),),
        'unsigned_relation', '==', (236330,),
        coupled_uses=()),
    MenuRole('script_arrival_past_relation', '_draw_scripted_arrival', (('body', 0, 'body', 2, 'test', 'ops', 0),),
        'unsigned_relation', '>', (236342,),
        coupled_uses=()),
    MenuRole('script_arrival_position_bound', '_draw_scripted_arrival', (('body', 0, 'body', 5, 'test', 'comparators', 0),),
        'word', 96, (236402,),
        coupled_uses=()),
    MenuRole('script_arrival_position_relation', '_draw_scripted_arrival', (('body', 0, 'body', 5, 'test', 'ops', 0),),
        'unsigned_relation', '>=', (236410,),
        coupled_uses=()),
    MenuRole('script_arrival_tick_mask', '_draw_scripted_arrival', (('body', 0, 'body', 5, 'body', 0, 'test', 'left', 'right'),),
        'word', 3, (236418,),
        coupled_uses=()),
    MenuRole('script_arrival_position_step', '_draw_scripted_arrival', (('body', 0, 'body', 5, 'body', 0, 'body', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (236426,),
        coupled_uses=()),
    MenuRole('script_staged_counter_step', '_draw_scripted_staged_pair', (('body', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (237398,),
        coupled_uses=()),
    MenuRole('script_staged_animation_bit', '_draw_scripted_staged_pair', (('body', 2, 'value', 'test', 'right'),),
        'long_bit', 8, (237408,),
        coupled_uses=()),
    MenuRole('script_staged_first_delay', '_draw_scripted_staged_pair', (('body', 5, 'test', 'comparators', 0),),
        'word', 32, (237452,),
        coupled_uses=()),
    MenuRole('script_staged_first_delay_relation', '_draw_scripted_staged_pair', (('body', 5, 'test', 'ops', 0),),
        'unsigned_relation', '<', (237460,),
        coupled_uses=()),
    MenuRole('script_staged_second_delay', '_draw_scripted_staged_pair', (('body', 10, 'test', 'comparators', 0),),
        'word', 64, (237502,),
        coupled_uses=()),
    MenuRole('script_staged_second_delay_relation', '_draw_scripted_staged_pair', (('body', 10, 'test', 'ops', 0),),
        'unsigned_relation', '<', (237510,),
        coupled_uses=()),
    MenuRole('script_landing_y', '_draw_scripted_landing', (('body', 2, 'test', 'comparators', 0),),
        'word', 96, (236982,),
        coupled_uses=()),
    MenuRole('script_landing_y_relation', '_draw_scripted_landing', (('body', 2, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (236990,),
        coupled_uses=()),
    MenuRole('script_landing_palette_stop', '_draw_scripted_landing', (('body', 3, 'test', 'comparators', 0),),
        'word', 20, (236994,),
        coupled_uses=()),
    MenuRole('script_landing_palette_relation', '_draw_scripted_landing', (('body', 3, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (237002,),
        coupled_uses=()),
    MenuRole('script_landing_tick_mask', '_draw_scripted_landing', (('body', 3, 'body', 0, 'test', 'left', 'right'),),
        'word', 15, (237010,),
        coupled_uses=()),
    MenuRole('script_landing_palette_step', '_draw_scripted_landing', (('body', 3, 'body', 0, 'body', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 4, (237018,),
        coupled_uses=()),
    MenuRole('script_wave_step', '_draw_scripted_wave', (('body', 2, 'value', 'args', 1, 'args', 0, 'right'), ('body', 5, 'body', 0, 'value', 'args', 1, 'args', 0, 'right'), ('body', 5, 'orelse', 0, 'value', 'args', 1, 'args', 0, 'right')),
        'quick', 2, (238070, 238112, 238122),
        coupled_uses=()),
    MenuRole('script_wave_y', '_draw_scripted_wave', (('body', 4, 'value', 'args', 1),),
        'word', 96, (238092,),
        coupled_uses=()),
    MenuRole('script_wave_tick_mask', '_draw_scripted_wave', (('body', 5, 'test', 'right'),),
        'word', 3, (238104,),
        coupled_uses=()),
    MenuRole('script_wave_terminator', '_draw_scripted_wave', (('body', 5, 'orelse', 1, 'test', 'comparators', 0),),
        'word', 255, (238144,),
        coupled_uses=()),
    MenuRole('script_wave_delay', '_draw_scripted_wave', (('body', 7, 'test', 'comparators', 0),),
        'word', 120, (238192,),
        coupled_uses=()),
    MenuRole('script_wave_delay_relation', '_draw_scripted_wave', (('body', 7, 'test', 'ops', 0),),
        'unsigned_relation', '<', (238200,),
        coupled_uses=()),
    MenuRole('script_wave_palette_stop', '_draw_scripted_wave', (('body', 8, 'test', 'comparators', 0),),
        'word', 24, (238204,),
        coupled_uses=()),
    MenuRole('script_wave_palette_relation', '_draw_scripted_wave', (('body', 8, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (238212,),
        coupled_uses=()),
    MenuRole('script_wave_palette_tick_mask', '_draw_scripted_wave', (('body', 8, 'body', 0, 'test', 'left', 'right'),),
        'word', 7, (238220,),
        coupled_uses=()),
    MenuRole('script_wave_palette_step', '_draw_scripted_wave', (('body', 8, 'body', 0, 'body', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 4, (238228,),
        coupled_uses=()),
    MenuRole('script_late_delay', '_draw_scripted_late_palette', (('body', 2, 'test', 'comparators', 0),),
        'word', 120, (238406,),
        coupled_uses=()),
    MenuRole('script_late_delay_relation', '_draw_scripted_late_palette', (('body', 2, 'test', 'ops', 0),),
        'unsigned_relation', '<', (238414,),
        coupled_uses=()),
    MenuRole('script_late_palette_stop', '_draw_scripted_late_palette', (('body', 3, 'test', 'comparators', 0),),
        'word', 24, (238418,),
        coupled_uses=()),
    MenuRole('script_late_palette_relation', '_draw_scripted_late_palette', (('body', 3, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (238426,),
        coupled_uses=()),
    MenuRole('script_late_tick_mask', '_draw_scripted_late_palette', (('body', 3, 'body', 0, 'test', 'left', 'right'),),
        'word', 15, (238434,),
        coupled_uses=()),
    MenuRole('script_late_palette_step', '_draw_scripted_late_palette', (('body', 3, 'body', 0, 'body', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 4, (238442,),
        coupled_uses=()),
    MenuRole('script_three_frame_step', '_draw_scripted_three_frame_stage', (('body', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (238542,),
        coupled_uses=()),
    MenuRole('script_three_frame_duration', '_draw_scripted_three_frame_stage', (('body', 1, 'test', 'comparators', 0),),
        'word', 128, (238548,),
        coupled_uses=()),
    MenuRole('script_three_frame_duration_relation', '_draw_scripted_three_frame_stage', (('body', 1, 'test', 'ops', 0),),
        'unsigned_relation', '<=', (238556,),
        coupled_uses=()),
    MenuRole('script_three_frame_tick_bit', '_draw_scripted_three_frame_stage', (('body', 1, 'body', 0, 'test', 'operand', 'right'),),
        'long_bit', 4, (238564,),
        coupled_uses=()),
    MenuRole('script_three_frame_index_bound', '_draw_scripted_three_frame_stage', (('body', 1, 'body', 0, 'body', 0, 'test', 'comparators', 0),),
        'word', 2, (238572,),
        coupled_uses=()),
    MenuRole('script_three_frame_index_relation', '_draw_scripted_three_frame_stage', (('body', 1, 'body', 0, 'body', 0, 'test', 'ops', 0),),
        'unsigned_relation', '>=', (238580,),
        coupled_uses=()),
    MenuRole('script_three_frame_index_step', '_draw_scripted_three_frame_stage', (('body', 1, 'body', 0, 'body', 0, 'orelse', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'word', 1, (238596,),
        coupled_uses=()),
    MenuRole('script_high_first_shift', '_draw_scripted_high_mode', (('body', 2, 'body', 0, 'value', 'args', 0, 'left', 'left', 'right'),),
        'shift', 2, (235928,),
        coupled_uses=()),
    MenuRole('script_high_first_mask', '_draw_scripted_high_mode', (('body', 2, 'body', 0, 'value', 'args', 0, 'left', 'right'),),
        'word', 3, (235930,),
        coupled_uses=()),
    MenuRole('script_high_second_shift', '_draw_scripted_high_mode', (('body', 2, 'orelse', 0, 'body', 0, 'value', 'args', 0, 'left', 'left', 'right'),),
        'shift', 3, (235962,),
        coupled_uses=()),
    MenuRole('script_high_second_mask', '_draw_scripted_high_mode', (('body', 2, 'orelse', 0, 'body', 0, 'value', 'args', 0, 'left', 'right'),),
        'word', 1, (235964,),
        coupled_uses=()),
    MenuRole('script_secondary_first_x', 'play_scripted_scene', (('body', 7, 'body', 0, 'value', 'elts', 0), ('body', 7, 'orelse', 0, 'body', 0, 'value', 'elts', 0)),
        'word', 96, (235236,),
        coupled_uses=()),
    MenuRole('script_secondary_first_y', 'play_scripted_scene', (('body', 7, 'body', 0, 'value', 'elts', 1), ('body', 7, 'orelse', 0, 'body', 0, 'value', 'elts', 1)),
        'word', 48, (235244,),
        coupled_uses=()),
    MenuRole('script_secondary_last_x', 'play_scripted_scene', (('body', 7, 'orelse', 0, 'orelse', 0, 'value', 'elts', 0),),
        'word', 144, (235266,),
        coupled_uses=()),
    MenuRole('script_secondary_last_y', 'play_scripted_scene', (('body', 7, 'orelse', 0, 'orelse', 0, 'value', 'elts', 1),),
        'word', 96, (235274,),
        coupled_uses=()),
    MenuRole('script_plane_address', 'play_scripted_scene', (('body', 19, 'body', 0, 'value', 'args', 0), ('body', 23, 'body', 1, 'value', 'args', 2, 'args', 0)),
        'word', 8192, (235354, 235418),
        coupled_uses=()),
    MenuRole('script_sound_command', 'play_scripted_scene', (('body', 27, 'body', 0, 'value', 'args', 1),),
        'word', 1536, (235464,),
        coupled_uses=()),
    MenuRole('script_elapsed_step', 'play_scripted_scene', (('body', 27, 'body', 2, 'value', 'args', 1, 'args', 0, 'right'),),
        'word', 1, (235476,),
        coupled_uses=()),
    MenuRole('script_duration_relation', 'play_scripted_scene', (('body', 27, 'body', 5, 'test', 'ops', 0),),
        'unsigned_relation', '==', (235510,),
        coupled_uses=()),
)

_OWNER_ROLE_NAMES = {'flush_scene_transfer_queue': ('queue_nonempty_relation',), 'write_vdp_packet_stream': ('packet_wrap_width',), 'write_vdp_dictionary_repeat_stream': ('dictionary_literal_ceiling', 'dictionary_repeat_ceiling'), 'decode_glyph_rows_to_buffers': ('glyph_row_longs', 'glyph_fill_nibbles', 'glyph_fill_nibble_shift'), 'darken_palette': ('darken_nibble_rotation', 'palette_shade_ceiling', 'darken_hang_relation', 'darken_round_step', 'darken_dirty_step'), 'darken_palette_component': ('darken_nibble_rotation', 'palette_component_mask'), 'write_vdp_word_rle_stream': ('word_stream_marker_relation',), 'play_scripted_scene': ('script_palette_longs', 'script_palette_words', 'script_fixed_x', 'script_fixed_y', 'script_sequence_tick_mask', 'script_sequence_step', 'script_sequence_palette_frame', 'script_sequence_palette_frame_relation', 'script_sequence_palette_stop', 'script_sequence_palette_stop_relation', 'script_sequence_palette_step', 'script_first_frame', 'script_first_frame_relation', 'script_other_frame_palette_offset', 'script_arrival_step', 'script_arrival_count', 'script_arrival_equal_relation', 'script_arrival_past_relation', 'script_arrival_position_bound', 'script_arrival_position_relation', 'script_arrival_tick_mask', 'script_arrival_position_step', 'script_staged_counter_step', 'script_staged_animation_bit', 'script_staged_first_delay', 'script_staged_first_delay_relation', 'script_staged_second_delay', 'script_staged_second_delay_relation', 'script_landing_y', 'script_landing_y_relation', 'script_landing_palette_stop', 'script_landing_palette_relation', 'script_landing_tick_mask', 'script_landing_palette_step', 'script_wave_step', 'script_wave_y', 'script_wave_tick_mask', 'script_wave_terminator', 'script_wave_delay', 'script_wave_delay_relation', 'script_wave_palette_stop', 'script_wave_palette_relation', 'script_wave_palette_tick_mask', 'script_wave_palette_step', 'script_late_delay', 'script_late_delay_relation', 'script_late_palette_stop', 'script_late_palette_relation', 'script_late_tick_mask', 'script_late_palette_step', 'script_three_frame_step', 'script_three_frame_duration', 'script_three_frame_duration_relation', 'script_three_frame_tick_bit', 'script_three_frame_index_bound', 'script_three_frame_index_relation', 'script_three_frame_index_step', 'script_high_first_shift', 'script_high_first_mask', 'script_high_second_shift', 'script_high_second_mask', 'script_secondary_first_x', 'script_secondary_first_y', 'script_secondary_last_x', 'script_secondary_last_y', 'script_plane_address', 'script_sound_command', 'script_elapsed_step', 'script_duration_relation'), 'update_scripted_scene_position': ('movement_tick_mask', 'movement_counter_step', 'movement_limit_relation', 'movement_distance_mask', 'movement_left_bit', 'movement_right_bit', 'movement_up_bit', 'movement_down_bit'), 'initialize_scripted_secondary_position': ('secondary_latched_relation', 'secondary_latch_value'), 'select_scene_object_frame': ('frame_direct_mode_bound', 'frame_direct_mode_relation', 'frame_sequence_bound', 'frame_sequence_relation', 'frame_sequence_tick_mask', 'frame_sequence_step', 'frame_sequence_terminator', 'frame_lookup_keep_mask'), 'append_clipped_scene_sprites': ('sprite_capacity', 'sprite_capacity_relation', 'sprite_origin', 'sprite_flip_adjustment', 'sprite_horizontal_flip_bit', 'sprite_vertical_flip_bit', 'sprite_clip_minimum', 'sprite_clip_x_maximum', 'sprite_clip_y_maximum', 'sprite_clip_minimum_relation', 'sprite_clip_x_maximum_relation', 'sprite_clip_y_maximum_relation', 'sprite_count_step', 'sprite_palette_keep_mask', 'sprite_palette_shift', 'marker_origin_adjustment'), 'finish_scene_sprite_chains': (), 'finish_one_scene_sprite_chain': ('scene_chain_nonempty_relation',), 'append_unclipped_scene_sprites': ('sprite_capacity', 'sprite_capacity_relation', 'sprite_origin', 'sprite_flip_adjustment', 'sprite_horizontal_flip_bit', 'sprite_vertical_flip_bit', 'sprite_count_step', 'sprite_palette_keep_mask', 'sprite_palette_shift'), 'advance_scene_palette_fade': ('palette_component_mask', 'palette_shade_ceiling', 'palette_period_keep_mask', 'palette_delay_step', 'palette_shade_step', 'palette_shade_end_relation', 'fade_nibble_rotation'), 'fade_palette_component': ('palette_component_mask', 'fade_nibble_rotation'), 'begin_scene_palette_darken': ('palette_shade_ceiling', 'palette_period_keep_mask'), 'snapshot_and_clear_scene_palette': ('palette_snapshot_longs',), 'read_vdp_plane_rle_rows': ('plane_stream_marker_relation', 'plane_column_step', 'plane_column_bound', 'plane_column_end_relation', 'plane_row_step', 'plane_initial_rows'), 'write_vdp_swapped_byte_rle_stream': ('swapped_stream_marker_relation',), 'copy_scene_palette_variant': (), 'finish_actor_sprite_chains': (), 'finish_one_actor_sprite_chain': ('scene_chain_nonempty_relation',), 'set_vram_write_address': (), 'sample_random_preserving_seed_carrier': ()}

_COUNTER_OWNERS = {'glyph_fill_nibbles': ('decode_glyph_rows_to_buffers',), 'glyph_row_longs': ('decode_glyph_rows_to_buffers',), 'palette_snapshot_longs': ('snapshot_and_clear_scene_palette',), 'script_palette_longs': ('play_scripted_scene',), 'script_palette_words': ('play_scripted_scene',)}

_BIT_OWNERS = {'movement_down_bit': ('update_scripted_scene_position',), 'movement_left_bit': ('update_scripted_scene_position',), 'movement_right_bit': ('update_scripted_scene_position',), 'movement_up_bit': ('update_scripted_scene_position',), 'script_staged_animation_bit': ('play_scripted_scene',), 'script_three_frame_tick_bit': ('play_scripted_scene',), 'sprite_horizontal_flip_bit': ('append_clipped_scene_sprites', 'append_unclipped_scene_sprites'), 'sprite_vertical_flip_bit': ('append_clipped_scene_sprites', 'append_unclipped_scene_sprites')}

_BIT_LIMITS = {'sprite_horizontal_flip_bit': 32768, 'sprite_vertical_flip_bit': 32768, 'movement_left_bit': 128, 'movement_right_bit': 128, 'movement_up_bit': 128, 'movement_down_bit': 128, 'script_staged_animation_bit': 32768, 'script_three_frame_tick_bit': 128}

_COUNT_LIMITS = {'palette_snapshot_longs': 128, 'script_palette_longs': 128, 'script_palette_words': 128}

_RELATION_SITES = {'queue_nonempty_relation': [('flush_scene_transfer_queue', 'false')], 'darken_hang_relation': [('darken_palette', 'false')], 'palette_shade_end_relation': [('advance_scene_palette_fade', 'true')], 'word_stream_marker_relation': [('write_vdp_word_rle_stream', 'false')], 'swapped_stream_marker_relation': [('write_vdp_swapped_byte_rle_stream', 'false')], 'plane_stream_marker_relation': [('read_vdp_plane_rle_rows', 'false')], 'plane_column_end_relation': [('read_vdp_plane_rle_rows', 'false')], 'scene_chain_nonempty_relation': [('finish_one_actor_sprite_chain', 'false'), ('finish_one_scene_sprite_chain', 'false')], 'sprite_capacity_relation': [('append_clipped_scene_sprites', 'false'), ('append_clipped_scene_sprites', 'true'), ('append_unclipped_scene_sprites', 'false'), ('append_unclipped_scene_sprites', 'true')], 'sprite_clip_minimum_relation': [('append_clipped_scene_sprites', 'true')], 'sprite_clip_x_maximum_relation': [('append_clipped_scene_sprites', 'true')], 'sprite_clip_y_maximum_relation': [('append_clipped_scene_sprites', 'true')], 'movement_limit_relation': [('update_scripted_scene_position', 'true')], 'secondary_latched_relation': [('initialize_scripted_secondary_position', 'true')], 'frame_direct_mode_relation': [('select_scene_object_frame', 'false')], 'frame_sequence_relation': [('select_scene_object_frame', 'false')], 'script_sequence_palette_frame_relation': [('play_scripted_scene', 'false')], 'script_sequence_palette_stop_relation': [('play_scripted_scene', 'true')], 'script_first_frame_relation': [('play_scripted_scene', 'true')], 'script_arrival_equal_relation': [('play_scripted_scene', 'true')], 'script_arrival_past_relation': [('play_scripted_scene', 'true')], 'script_arrival_position_relation': [('play_scripted_scene', 'false')], 'script_staged_first_delay_relation': [('play_scripted_scene', 'true')], 'script_staged_second_delay_relation': [('play_scripted_scene', 'true')], 'script_landing_y_relation': [('play_scripted_scene', 'true')], 'script_landing_palette_relation': [('play_scripted_scene', 'false')], 'script_wave_delay_relation': [('play_scripted_scene', 'true')], 'script_wave_palette_relation': [('play_scripted_scene', 'false')], 'script_late_delay_relation': [('play_scripted_scene', 'true')], 'script_late_palette_relation': [('play_scripted_scene', 'false')], 'script_three_frame_duration_relation': [('play_scripted_scene', 'false')], 'script_three_frame_index_relation': [('play_scripted_scene', 'false')], 'script_duration_relation': [('play_scripted_scene', 'false')]}

_TRUE_BRANCH = {'<':'bcs','<=':'bls','>':'bhi','>=':'bcc','==':'beq','!=':'bne'}
_FALSE_BRANCH = {'<':'bcc','<=':'bhi','>':'bls','>=':'bcs','==':'bne','!=':'beq'}


def owner_rules(values):
    """Map actual supplied policies to all 26 existing physical allocations.

Unsigned relations observe the original CMP/TST width and no new read. Bit
indices remain inside the actual observed width. DBRA derives count minus
one; MOVEQ counters are nonnegative and bounded, not silently truncated.
    """
    values = dict(values)
    values['sprite_clip_y_maximum_relation'] = values['sprite_clip_x_maximum_relation']
    for name, maximum in _BIT_LIMITS.items():
        value = values[name]
        if type(value) is not int or not 1 <= value <= maximum or value & value - 1:
            raise CompileError(name + ': one bit within original observed width required')
    for name, maximum in _COUNT_LIMITS.items():
        if type(values[name]) is not int or not 1 <= values[name] <= maximum:
            raise CompileError(name + ': original MOVEQ/DBRA representable count required')
    if values['dictionary_literal_ceiling'] >= values['dictionary_repeat_ceiling']:
        raise CompileError('dictionary literal/repeat classification ceilings must be ordered')
    if values['sprite_clip_minimum'] > values['sprite_clip_x_maximum'] or values['sprite_clip_minimum'] > values['sprite_clip_y_maximum']:
        raise CompileError('sprite clipping bounds must be ordered')
    result = {owner: {name: values[name] for name in names} for owner, names in _OWNER_ROLE_NAMES.items()}
    for name, owners in _COUNTER_OWNERS.items():
        for owner in owners:
            result[owner][name + '_counter'] = values[name] - 1
    for name, owners in _BIT_OWNERS.items():
        for owner in owners:
            result[owner][name + '_index'] = values[name].bit_length() - 1
    for name, sites in _RELATION_SITES.items():
        relation = values[name]
        if type(relation) is not str or relation not in _TRUE_BRANCH:
            raise CompileError(name + ': declared unsigned relation required')
        for owner, sense in sites:
            result[owner][name + '_' + sense + '_branch'] = (_TRUE_BRANCH if sense == 'true' else _FALSE_BRANCH)[relation]
    return result


def _lower_scene_family_flush_scene_transfer_queue(emitter, rules):
    emitter.segment(44294, 44316)
    emitter.ins('tst.w', '0xd100:w', 4)
    emitter.ins(rules['queue_nonempty_relation_false_branch'] + '.b', 'scene_pc_00ad12', 2)
    emitter.ins('lea.l', '0xd100:w,%a0', 4)
    emitter.ins('bsr.b', 'scene_pc_00ad1c', 2)
    emitter.ins('clr.w', '0xf31a:w', 4)
    emitter.ins('clr.w', '0xd100:w', 4)
    emitter.ins('rts', '', 2)
def _lower_scene_family_write_vdp_packet_stream(emitter, rules):
    emitter.segment(44316, 44540)
    emitter.ins('lea.l', '0xc00000:l,%a6', 6)
    emitter.ins('move.w', '#0x8f02,%d1', 4)
    emitter.ins('move.w', '(%a0)+,%d0', 2)
    emitter.ins('beq.w', 'scene_pc_00adc8', 4)
    emitter.ins('bmi.b', 'scene_pc_00ad50', 2)
    emitter.ins('moveq', '#0,%d2', 2)
    emitter.ins('move.w', '(%a0)+,%d2', 2)
    emitter.ins('clr.w', '%d3', 2)
    emitter.ins('btst.l', '#0xe,%d0', 4)
    emitter.ins('bne.b', 'scene_pc_00ad70', 2)
    emitter.ins('move.w', '%d2,%d3', 2)
    emitter.ins('andi.w', '#0x7f,%d3', 4)
    emitter.ins('lsr.w', '#0x1,%d3', 2)
    emitter.ins('add.w', '%d0,%d3', 2)
    emitter.ins('subi.w', f"#0x{rules['packet_wrap_width']:x},%d3", 4)
    emitter.ins('bcc.b', 'scene_pc_00ad4c', 2)
    emitter.ins('clr.w', '%d3', 2)
    emitter.ins('sub.w', '%d3,%d0', 2)
    emitter.ins('bra.b', 'scene_pc_00ad70', 2)
    emitter.ins('move.w', '#0x8f80,%d1', 4)
    emitter.ins('andi.w', '#0x7fff,%d0', 4)
    emitter.ins('moveq', '#0,%d2', 2)
    emitter.ins('move.w', '(%a0)+,%d2', 2)
    emitter.ins('move.w', '%d2,%d3', 2)
    emitter.ins('andi.w', '#0x1fff,%d3', 4)
    emitter.ins('lsr.w', '#0x7,%d3', 2)
    emitter.ins('add.w', '%d0,%d3', 2)
    emitter.ins('subi.w', f"#0x{rules['packet_wrap_width']:x},%d3", 4)
    emitter.ins('bcc.b', 'scene_pc_00ad6e', 2)
    emitter.ins('clr.w', '%d3', 2)
    emitter.ins('sub.w', '%d3,%d0', 2)
    emitter.ins('andi.w', '#0xbfff,%d0', 4)
    emitter.ins('subq.w', '#0x1,%d0', 2)
    emitter.ins('move.w', '%d1,0xc00004:l', 6)
    emitter.ins('lsl.l', '#0x2,%d2', 2)
    emitter.ins('lsr.w', '#0x2,%d2', 2)
    emitter.ins('ori.w', '#0x4000,%d2', 4)
    emitter.ins('swap', '%d2', 2)
    emitter.ins('move.l', '%d2,0xc00004:l', 6)
    emitter.ins('cmpi.w', '#0x8,%d0', 4)
    emitter.ins('bcc.b', 'scene_pc_00add0', 2)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('dbra', '%d0,scene_pc_00ad92', 4)
    emitter.ins('tst.w', '%d3', 2)
    emitter.ins('beq.b', 'scene_pc_00ad1c', 2)
    emitter.ins('btst.l', '#0x1,%d1', 4)
    emitter.ins('beq.b', 'scene_pc_00adaa', 2)
    emitter.ins('andi.l', '#0xff80ffff,%d2', 6)
    emitter.ins('bra.b', 'scene_pc_00adb0', 2)
    emitter.ins('andi.l', '#0xe07fffff,%d2', 6)
    emitter.ins('subq.w', '#0x1,%d3', 2)
    emitter.ins('move.l', '%d2,0xc00004:l', 6)
    emitter.ins('cmpi.w', '#0x8,%d3', 4)
    emitter.ins('bcc.b', 'scene_pc_00ade6', 2)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('dbra', '%d3,scene_pc_00adb8', 4)
    emitter.ins('bra.w', 'scene_pc_00ad1c', 4)
    emitter.ins('move.w', '%d1,0xc00004:l', 6)
    emitter.ins('rts', '', 2)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('subi.w', '#0x8,%d0', 4)
    emitter.ins('bra.b', 'scene_pc_00ad8c', 2)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('subi.w', '#0x8,%d3', 4)
    emitter.ins('bra.b', 'scene_pc_00adb8', 2)
def _lower_scene_family_write_vdp_dictionary_repeat_stream(emitter, rules):
    emitter.segment(44540, 44682)
    emitter.ins('clr.b', '%d2', 2)
    emitter.ins('lea.l', '0xc00000:l,%a6', 6)
    emitter.ins('tst.b', '%d2', 2)
    emitter.ins('beq.b', 'scene_pc_00ae0e', 2)
    emitter.ins('move.w', '(%a2)+,%d1', 2)
    emitter.ins('subq.b', '#0x1,%d2', 2)
    emitter.ins('bra.b', 'scene_pc_00ae12', 2)
    emitter.ins('move.w', '(%a0)+,%d1', 2)
    emitter.ins('subq.w', '#0x1,%d0', 2)
    emitter.ins('cmpi.w', f"#0x{rules['dictionary_literal_ceiling']:x},%d1", 4)
    emitter.ins('bcc.b', 'scene_pc_00ae24', 2)
    emitter.ins('move.w', '%d1,(%a6)', 2)
    emitter.ins('tst.b', '%d2', 2)
    emitter.ins('bne.b', 'scene_pc_00ae04', 2)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bpl.b', 'scene_pc_00ae04', 2)
    emitter.ins('rts', '', 2)
    emitter.ins('cmpi.w', f"#0x{rules['dictionary_repeat_ceiling']:x},%d1", 4)
    emitter.ins('bcc.b', 'scene_pc_00ae4a', 2)
    emitter.ins('andi.w', '#0xff,%d1', 4)
    emitter.ins('lsl.w', '#0x2,%d1', 2)
    emitter.ins('lea.l', '(%a1, %d1.w),%a2', 4)
    emitter.ins('cmpi.w', f"#0x{rules['dictionary_repeat_ceiling']:x},(%a2)", 4)
    emitter.ins('bcc.b', 'scene_pc_00ae44', 2)
    emitter.ins('cmpi.w', f"#0x{rules['dictionary_literal_ceiling']:x},(%a2)", 4)
    emitter.ins('bcs.b', 'scene_pc_00ae44', 2)
    emitter.ins('move.w', '(%a2),(%a6)', 2)
    emitter.ins('bra.b', 'scene_pc_00ae04', 2)
    emitter.ins('move.b', '#0x2,%d2', 4)
    emitter.ins('bra.b', 'scene_pc_00ae04', 2)
    emitter.ins('andi.w', '#0xff,%d1', 4)
    emitter.ins('tst.b', '%d2', 2)
    emitter.ins('beq.b', 'scene_pc_00ae58', 2)
    emitter.ins('move.w', '(%a2)+,%d3', 2)
    emitter.ins('subq.b', '#0x1,%d2', 2)
    emitter.ins('bra.b', 'scene_pc_00ae68', 2)
    emitter.ins('move.w', '(%a0)+,%d3', 2)
    emitter.ins('subq.w', '#0x1,%d0', 2)
    emitter.ins('cmpi.w', f"#0x{rules['dictionary_repeat_ceiling']:x},%d3", 4)
    emitter.ins('bcc.b', 'scene_pc_00ae68', 2)
    emitter.ins('cmpi.w', f"#0x{rules['dictionary_literal_ceiling']:x},%d3", 4)
    emitter.ins('bcc.b', 'scene_pc_00ae78', 2)
    emitter.ins('move.w', '%d3,(%a6)', 2)
    emitter.ins('dbra', '%d1,scene_pc_00ae68', 4)
    emitter.ins('tst.b', '%d2', 2)
    emitter.ins('bne.b', 'scene_pc_00ae04', 2)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bpl.b', 'scene_pc_00ae04', 2)
    emitter.ins('rts', '', 2)
    emitter.ins('andi.w', '#0xff,%d3', 4)
    emitter.ins('lsl.w', '#0x2,%d3', 2)
    emitter.ins('lea.l', '(%a1, %d3.w),%a2', 4)
    emitter.ins('move.w', '(%a2)+,%d3', 2)
    emitter.ins('move.b', '#0x1,%d2', 4)
    emitter.ins('bra.b', 'scene_pc_00ae68', 2)
def _lower_scene_family_decode_glyph_rows_to_buffers(emitter, rules):
    emitter.segment(44682, 44804)
    emitter.ins('movem.l', '%d4-%d7/%a2,-(%a7)', 4)
    emitter.ins('move.w', '(%a0)+,%d4', 2)
    emitter.ins('bmi.b', 'scene_pc_00aed8', 2)
    emitter.ins('move.w', '%d4,%d5', 2)
    emitter.ins('andi.w', '#0xff00,%d5', 4)
    emitter.ins('lsl.w', '#0x3,%d5', 2)
    emitter.ins('andi.w', '#0xff,%d4', 4)
    emitter.ins('lsl.w', '#0x5,%d4', 2)
    emitter.ins('or.w', '%d5,%d4', 2)
    emitter.ins('andi.l', '#0xffff,%d4', 6)
    emitter.ins('lea.l', '0x8159c:l,%a2', 6)
    emitter.ins('lea.l', '(%a2, %d4.l),%a2', 4)
    emitter.ins('move.w', f"#0x{rules['glyph_row_longs_counter']:x},%d5", 4)
    emitter.ins('bsr.w', 'scene_pc_00af04', 4)
    emitter.ins('move.l', '%d7,(%a1)', 2)
    emitter.ins('bsr.w', 'scene_pc_00af04', 4)
    emitter.ins('move.l', '%d7,0x40(%a1)', 4)
    emitter.ins('addq.l', '#0x4,%a1', 2)
    emitter.ins('dbra', '%d5,scene_pc_00aeb6', 4)
    emitter.ins('adda.w', '#0x40,%a1', 4)
    emitter.ins('dbra', '%d3,scene_pc_00ae8e', 4)
    emitter.ins('movem.l', '(%a7)+,%d4-%d7/%a2', 4)
    emitter.ins('rts', '', 2)
    emitter.ins('moveq', '#0,%d6', 2)
    emitter.ins('moveq', '#0,%d7', 2)
    emitter.ins('move.w', f"#0x{rules['glyph_fill_nibbles_counter']:x},%d4", 4)
    emitter.ins('lsl.l', f"#0x{rules['glyph_fill_nibble_shift']:x},%d6", 2)
    emitter.ins('lsl.l', f"#0x{rules['glyph_fill_nibble_shift']:x},%d7", 2)
    emitter.ins('or.w', '%d0,%d6', 2)
    emitter.ins('or.w', '%d1,%d7', 2)
    emitter.ins('dbra', '%d4,scene_pc_00aee0', 4)
    emitter.ins('move.w', f"#0x{rules['glyph_row_longs_counter']:x},%d4", 4)
    emitter.ins('move.l', '%d6,0x40(%a1)', 4)
    emitter.ins('move.l', '%d6,(%a1)+', 2)
    emitter.ins('dbra', '%d4,scene_pc_00aef0', 4)
    emitter.ins('move.l', '%d7,-0x24(%a1)', 4)
    emitter.ins('move.l', '%d7,0x1c(%a1)', 4)
    emitter.ins('bra.b', 'scene_pc_00aeca', 2)
def _lower_scene_family_darken_palette(emitter, rules):
    emitter.segment(56998, 57076)
    emitter.ins('cmpi.w', f"#0x{rules['palette_shade_ceiling']:x},%d0", 4)
    emitter.ins(rules['darken_hang_relation_false_branch'] + '.b', 'scene_pc_00deae', 2)
    emitter.ins('bra.b', 'scene_pc_00deac', 2)
    emitter.ins('lea.l', '0xfb00:w,%a1', 4)
    emitter.ins('btst.l', '#0x0,%d0', 4)
    emitter.ins('beq.b', 'scene_pc_00dec2', 2)
    emitter.ins('btst.b', '#0x0,0xf320:w', 6)
    emitter.ins('beq.b', 'scene_pc_00dec2', 2)
    emitter.ins('addq.w', f"#0x{rules['darken_round_step']:x},%d0", 2)
    emitter.ins('bclr.l', '#0x0,%d0', 4)
    emitter.ins('clr.w', '%d4', 2)
    emitter.ins('move.w', '(%a0)+,%d2', 2)
    emitter.ins('lsl.w', f"#0x{rules['darken_nibble_rotation']:x},%d2", 2)
    emitter.ins('bsr.w', 'scene_pc_00def4', 4)
    emitter.ins('bsr.w', 'scene_pc_00def4', 4)
    emitter.ins('bsr.w', 'scene_pc_00def4', 4)
    emitter.ins('move.w', '%d4,(%a1)+', 2)
    emitter.ins('dbra', '%d1,scene_pc_00dec6', 4)
    emitter.ins('addq.w', f"#0x{rules['darken_dirty_step']:x},0xf31e:w", 4)
    emitter.ins('move.w', '0xfb00:w,%d0', 4)
    emitter.ins('move.w', '%d0,0xfb20:w', 4)
    emitter.ins('move.w', '%d0,0xfb40:w', 4)
    emitter.ins('move.w', '%d0,0xfb60:w', 4)
    emitter.ins('rts', '', 2)
def _lower_scene_family_darken_palette_component(emitter, rules):
    emitter.segment(57076, 57096)
    emitter.ins('lsl.w', f"#0x{rules['darken_nibble_rotation']:x},%d4", 2)
    emitter.ins('rol.w', f"#0x{rules['darken_nibble_rotation']:x},%d2", 2)
    emitter.ins('move.b', '%d2,%d3', 2)
    emitter.ins('andi.w', f"#0x{rules['palette_component_mask']:x},%d3", 4)
    emitter.ins('sub.b', '%d0,%d3', 2)
    emitter.ins('bcc.b', 'scene_pc_00df04', 2)
    emitter.ins('clr.b', '%d3', 2)
    emitter.ins('or.w', '%d3,%d4', 2)
    emitter.ins('rts', '', 2)
def _lower_scene_family_write_vdp_word_rle_stream(emitter, rules):
    emitter.segment(235096, 235162)
    emitter.ins('move.w', '#0x8f02,0xc00004:l', 8)
    emitter.ins('bsr.w', 'scene_pc_03b2b0', 4)
    emitter.ins('move.b', '(%a0)+,%d1', 2)
    emitter.ins('move.b', '(%a0)+,%d2', 2)
    emitter.ins('cmp.b', '%d2,%d1', 2)
    emitter.ins(rules['word_stream_marker_relation_false_branch'] + '.w', 'scene_pc_03967c', 4)
    emitter.ins('move.b', '(%a0)+,%d4', 2)
    emitter.ins('asl.w', '#0x8,%d2', 2)
    emitter.ins('move.b', '%d4,%d2', 2)
    emitter.ins('move.w', '%d2,0xc00000:l', 6)
    emitter.ins('bra.b', 'scene_pc_039666', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.b', '(%a0)+,%d3', 2)
    emitter.ins('beq.w', 'scene_pc_039698', 4)
    emitter.ins('move.b', '(%a0)+,%d4', 2)
    emitter.ins('move.b', '(%a0)+,%d2', 2)
    emitter.ins('asl.w', '#0x8,%d4', 2)
    emitter.ins('move.b', '%d2,%d4', 2)
    emitter.ins('move.w', '%d4,0xc00000:l', 6)
    emitter.ins('dbra', '%d3,scene_pc_03968c', 4)
    emitter.ins('bra.b', 'scene_pc_039666', 2)
    emitter.ins('rts', '', 2)
def _lower_scene_family_play_scripted_scene(emitter, rules):
    emitter.segment(235162, 235602)
    emitter.ins('move.w', '#0x2700,%sr', 4)
    emitter.ins('clr.w', '0xf612:w', 4)
    emitter.ins('jsr', '4282(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('clr.l', '0xff702e:l', 6)
    emitter.ins('clr.l', '0xff703a:l', 6)
    emitter.ins('clr.w', '0xff7000:l', 6)
    emitter.ins('clr.w', '0xff7004:l', 6)
    emitter.ins('clr.w', '0xff703e:l', 6)
    emitter.ins('clr.w', '0xff7036:l', 6)
    emitter.ins('clr.w', '0xff7044:l', 6)
    emitter.ins('clr.w', '0xff703c:l', 6)
    emitter.ins('cmpi.w', '#0x18,0xff7026:l', 8)
    emitter.ins('bne.w', 'scene_pc_0396f8', 4)
    emitter.ins('move.w', f"#0x{rules['script_secondary_first_x']:x},0xff7032:l", 8)
    emitter.ins('move.w', f"#0x{rules['script_secondary_first_y']:x},0xff7034:l", 8)
    emitter.ins('bra.w', 'scene_pc_039712', 4)
    emitter.ins('cmpi.w', '#0x1c,0xff7026:l', 8)
    emitter.ins('beq.b', 'scene_pc_0396e4', 2)
    emitter.ins('move.w', f"#0x{rules['script_secondary_last_x']:x},0xff7032:l", 8)
    emitter.ins('move.w', f"#0x{rules['script_secondary_last_y']:x},0xff7034:l", 8)
    emitter.ins('move.w', '0xff7026:l,%d0', 6)
    emitter.ins('asl.w', '#0x1,%d0', 2)
    emitter.ins('lea.l', '-2964(%pc),%a0', 4)
    emitter.ins('lea.l', '-2888(%pc),%a1', 4)
    emitter.ins('move.w', '(%a0, %d0.w),%d1', 4)
    emitter.ins('move.w', '(%a1, %d0.w),%d2', 4)
    emitter.ins('move.w', '%d1,0xff7028:l', 6)
    emitter.ins('move.w', '%d2,0xff702a:l', 6)
    emitter.ins('move.w', '0xff7026:l,%d0', 6)
    emitter.ins('lea.l', '-2286(%pc),%a0', 4)
    emitter.ins('move.b', '(%a0, %d0.w),%d1', 4)
    emitter.ins('move.b', '%d1,0xff702c:l', 6)
    emitter.ins('move.w', '#0x0,%d0', 4)
    emitter.ins('cmpi.w', '#0xa,0xff7026:l', 8)
    emitter.ins('bne.w', 'scene_pc_03975e', 4)
    emitter.ins('move.w', f"#0x{rules['script_plane_address']:x},%d0", 4)
    emitter.ins('move.w', '0xff7026:l,%d3', 6)
    emitter.ins('asl.w', '#0x2,%d3', 2)
    emitter.ins('lea.l', '-4014(%pc),%a1', 4)
    emitter.ins('movea.l', '(%a1, %d3.w),%a0', 4)
    emitter.ins('bsr.w', 'scene_pc_039658', 4)
    emitter.ins('move.w', '0xff7026:l,%d0', 6)
    emitter.ins('lea.l', '-3552(%pc),%a6', 4)
    emitter.ins('move.b', '(%a6, %d0.w),%d1', 4)
    emitter.ins('cmpi.b', '#0x1,%d1', 4)
    emitter.ins('bne.w', 'scene_pc_0397a2', 4)
    emitter.ins('move.w', '0xff7026:l,%d3', 6)
    emitter.ins('addq.w', '#0x1,%d3', 2)
    emitter.ins('asl.w', '#0x2,%d3', 2)
    emitter.ins('lea.l', '-4058(%pc),%a1', 4)
    emitter.ins('movea.l', '(%a1, %d3.w),%a0', 4)
    emitter.ins('move.w', f"#0x{rules['script_plane_address']:x},%d0", 4)
    emitter.ins('bsr.w', 'scene_pc_039658', 4)
    emitter.ins('move.w', '0xff7026:l,%d3', 6)
    emitter.ins('asl.w', '#0x2,%d3', 2)
    emitter.ins('lea.l', '-3762(%pc),%a1', 4)
    emitter.ins('movea.l', '(%a1, %d3.w),%a0', 4)
    emitter.ins('lea.l', '0xfb00:w,%a1', 4)
    emitter.ins('moveq', f"#{rules['script_palette_longs_counter']},%d0", 2)
    emitter.ins('move.l', '(%a0)+,(%a1)+', 2)
    emitter.ins('dbra', '%d0,scene_pc_0397b8', 4)
    emitter.ins('bra.w', 'scene_pc_0397c2', 4)
    emitter.ins('clr.l', '%d0', 2)
    emitter.ins('move.w', '#0x2500,%sr', 4)
    emitter.ins('move.w', f"#0x{rules['script_sound_command']:x},0xf612:w", 6)
    emitter.ins('tst.b', '0xf612:w', 4)
    emitter.ins('bne.b', 'scene_pc_0397ce', 2)
    emitter.ins('addi.w', f"#0x{rules['script_elapsed_step']:x},0xff703e:l", 8)
    emitter.ins('clr.l', '%d0', 2)
    emitter.ins('move.w', '0xff7026:l,%d0', 6)
    emitter.ins('asl.w', '#0x1,%d0', 2)
    emitter.ins('clr.l', '%d1', 2)
    emitter.ins('lea.l', '-3624(%pc),%a0', 4)
    emitter.ins('move.w', '(%a0, %d0.w),%d1', 4)
    emitter.ins('cmp.w', '0xff703e:l,%d1', 6)
    emitter.ins(rules['script_duration_relation_false_branch'] + '.w', 'scene_pc_0397fc', 4)
    emitter.ins('rts', '', 2)
    emitter.ins('bsr.w', 'scene_pc_03a72e', 4)
    emitter.ins('moveq', '#0,%d0', 2)
    emitter.ins('cmpi.w', '#0xa,0xff7026:l', 8)
    emitter.ins('bcc.w', 'scene_pc_039aa6', 4)
    emitter.ins('move.w', '0xf320:w,%d0', 4)
    emitter.ins('andi.w', f"#0x{rules['script_sequence_tick_mask']:x},%d0", 4)
    emitter.ins('bne.w', 'scene_pc_039820', 4)
    emitter.ins('addq.w', f"#0x{rules['script_sequence_step']:x},0xff7004:l", 6)
    emitter.ins('moveq', '#0,%d1', 2)
    emitter.ins('move.w', '0xff7026:l,%d3', 6)
    emitter.ins('asl.w', '#0x2,%d3', 2)
    emitter.ins('lea.l', '-3610(%pc),%a1', 4)
    emitter.ins('movea.l', '(%a1, %d3.w),%a0', 4)
    emitter.ins('clr.l', '%d0', 2)
    emitter.ins('move.w', '0xff7004:l,%d0', 6)
    emitter.ins('adda.w', '%d0,%a0', 2)
    emitter.ins('move.b', '(%a0),%d1', 2)
    emitter.ins('bpl.w', 'scene_pc_039854', 4)
    emitter.ins('clr.l', '%d0', 2)
    emitter.ins('adda.w', '#0x1,%a0', 4)
    emitter.ins('move.b', '(%a0),%d1', 2)
    emitter.ins('move.w', '%d1,0xff7004:l', 6)
    emitter.ins('bra.b', 'scene_pc_039820', 2)
    emitter.segment(235604, 235876)
    emitter.ins('cmpi.w', '#0x5,0xff7026:l', 8)
    emitter.ins('beq.w', 'scene_pc_03991c', 4)
    emitter.ins('cmpi.w', '#0x1,0xff7026:l', 8)
    emitter.ins('bne.w', 'scene_pc_03988c', 4)
    emitter.ins('moveq', '#0,%d2', 2)
    emitter.ins('cmpi.w', f"#0x{rules['script_first_frame']:x},%d1", 4)
    emitter.ins(rules['script_first_frame_relation_true_branch'] + '.w', 'scene_pc_03987a', 4)
    emitter.ins('addi.w', f"#0x{rules['script_other_frame_palette_offset']:x},%d2", 4)
    emitter.ins('lea.l', '0xfb00:w,%a1', 4)
    emitter.ins('lea.l', '-2536(%pc),%a0', 4)
    emitter.ins('adda.w', '%d2,%a0', 2)
    emitter.ins('moveq', f"#{rules['script_palette_longs_counter']},%d0", 2)
    emitter.ins('move.l', '(%a0)+,(%a1)+', 2)
    emitter.ins('dbra', '%d0,scene_pc_039886', 4)
    emitter.ins('movem.w', '%d1,-(%a7)', 4)
    emitter.ins('jsr', '326(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('clr.l', '%d0', 2)
    emitter.ins('move.w', '0xff7026:l,%d3', 6)
    emitter.ins('asl.w', '#0x2,%d3', 2)
    emitter.ins('lea.l', '-3194(%pc),%a6', 4)
    emitter.ins('movea.l', '(%a6, %d3.w),%a1', 4)
    emitter.ins('asl.w', '#0x2,%d1', 2)
    emitter.ins('adda.w', '%d1,%a1', 2)
    emitter.ins('movea.l', '(%a1),%a0', 2)
    emitter.ins('move.w', '0xff7028:l,%d0', 6)
    emitter.ins('move.w', '0xff702a:l,%d1', 6)
    emitter.ins('moveq', '#4,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('moveq', '#0,%d4', 2)
    emitter.ins('jsr', '3294(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('movem.w', '(%a7)+,%d1', 4)
    emitter.ins('move.w', '0xff7026:l,%d0', 6)
    emitter.ins('lea.l', '-3896(%pc),%a6', 4)
    emitter.ins('move.b', '(%a6, %d0.w),%d2', 4)
    emitter.ins('cmpi.b', '#0x1,%d2', 4)
    emitter.ins('bne.w', 'scene_pc_039914', 4)
    emitter.ins('clr.l', '%d0', 2)
    emitter.ins('move.w', '0xff7026:l,%d3', 6)
    emitter.ins('asl.w', '#0x2,%d3', 2)
    emitter.ins('lea.l', '-2904(%pc),%a2', 4)
    emitter.ins('movea.l', '(%a2, %d3.w),%a1', 4)
    emitter.ins('asl.w', '#0x2,%d1', 2)
    emitter.ins('adda.w', '%d1,%a1', 2)
    emitter.ins('movea.l', '(%a1),%a0', 2)
    emitter.ins('move.w', '0xff7028:l,%d0', 6)
    emitter.ins('move.w', '0xff702a:l,%d1', 6)
    emitter.ins('moveq', '#4,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.l', '#0x100,%d4', 6)
    emitter.ins('jsr', '3216(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('bsr.w', 'scene_pc_03a74e', 4)
    emitter.ins('bra.w', 'scene_pc_0397c8', 4)
    emitter.ins('cmpi.w', f"#0x{rules['script_sequence_palette_frame']:x},%d1", 4)
    emitter.ins(rules['script_sequence_palette_frame_relation_false_branch'] + '.w', 'scene_pc_039960', 4)
    emitter.ins('move.w', '0xf320:w,%d0', 4)
    emitter.ins('andi.w', f"#0x{rules['script_sequence_tick_mask']:x},%d0", 4)
    emitter.ins('bne.w', 'scene_pc_039942', 4)
    emitter.ins('cmpi.w', f"#0x{rules['script_sequence_palette_stop']:x},0xff703c:l", 8)
    emitter.ins(rules['script_sequence_palette_stop_relation_true_branch'] + '.w', 'scene_pc_039960', 4)
    emitter.ins('addq.w', f"#0x{rules['script_sequence_palette_step']:x},0xff703c:l", 6)
    emitter.ins('clr.l', '%d3', 2)
    emitter.ins('move.w', '0xff703c:l,%d3', 6)
    emitter.ins('lea.l', '24(%pc),%a1', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('movea.l', '(%a1, %d3.w),%a0', 4)
    emitter.ins('lea.l', '0xfb00:w,%a1', 4)
    emitter.ins('moveq', f"#{rules['script_palette_longs_counter']},%d0", 2)
    emitter.ins('move.l', '(%a0)+,(%a1)+', 2)
    emitter.ins('dbra', '%d0,scene_pc_03995a', 4)
    emitter.ins('bra.w', 'scene_pc_039860', 4)
    emitter.segment(235924, 235992)
    emitter.ins('move.w', '0xf320:w,%d0', 4)
    emitter.ins('lsr.w', f"#0x{rules['script_high_first_shift']:x},%d0", 2)
    emitter.ins('andi.w', f"#0x{rules['script_high_first_mask']:x},%d0", 4)
    emitter.ins('asl.w', '#0x5,%d0', 2)
    emitter.ins('lea.l', '-2250(%pc),%a0', 4)
    emitter.ins('adda.w', '%d0,%a0', 2)
    emitter.ins('lea.l', '0xfb00:w,%a1', 4)
    emitter.ins('moveq', f"#{rules['script_palette_words_counter']},%d0", 2)
    emitter.ins('move.w', '(%a0)+,(%a1)+', 2)
    emitter.ins('dbra', '%d0,scene_pc_0399ac', 4)
    emitter.ins('bra.w', 'scene_pc_03a144', 4)
    emitter.ins('move.w', '0xf320:w,%d0', 4)
    emitter.ins('lsr.w', f"#0x{rules['script_high_second_shift']:x},%d0", 2)
    emitter.ins('andi.w', f"#0x{rules['script_high_second_mask']:x},%d0", 4)
    emitter.ins('asl.w', '#0x5,%d0', 2)
    emitter.ins('lea.l', '-2156(%pc),%a0', 4)
    emitter.ins('adda.w', '%d0,%a0', 2)
    emitter.ins('lea.l', '0xfb00:w,%a1', 4)
    emitter.ins('moveq', f"#{rules['script_palette_words_counter']},%d0", 2)
    emitter.ins('move.w', '(%a0)+,(%a1)+', 2)
    emitter.ins('dbra', '%d0,scene_pc_0399ce', 4)
    emitter.ins('bra.w', 'scene_pc_03a144', 4)
    emitter.segment(236198, 236296)
    emitter.ins('cmpi.w', '#0xb,0xff7026:l', 8)
    emitter.ins('bhi.w', 'scene_pc_039b10', 4)
    emitter.ins('jsr', '-220(%pc)', 4)
    emitter.ins('cmpi.w', '#0xb,0xff7026:l', 8)
    emitter.ins('bne.w', 'scene_pc_039ac8', 4)
    emitter.ins('moveq', '#1,%d1', 2)
    emitter.ins('bra.w', 'scene_pc_039aca', 4)
    emitter.ins('moveq', '#0,%d1', 2)
    emitter.ins('asl.w', '#0x2,%d1', 2)
    emitter.ins('movea.l', '58(%pc, %d1.w),%a0', 4)
    emitter.ins('move.w', '0xff7028:l,%d0', 6)
    emitter.ins('move.w', '0xff702a:l,%d1', 6)
    emitter.ins('moveq', '#4,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('cmpi.w', '#0xb,0xff7026:l', 8)
    emitter.ins('bne.w', 'scene_pc_039af2', 4)
    emitter.ins('moveq', '#0,%d4', 2)
    emitter.ins('bra.w', 'scene_pc_039af8', 4)
    emitter.ins('move.l', '#0x100,%d4', 6)
    emitter.ins('jsr', '2726(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('jsr', '3150(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('bra.w', 'scene_pc_0397c8', 4)
    emitter.segment(236304, 236468)
    emitter.ins('cmpi.w', '#0x13,0xff7026:l', 8)
    emitter.ins('bhi.w', 'scene_pc_039cf0', 4)
    emitter.ins('addq.w', f"#0x{rules['script_arrival_step']:x},0xff703c:l", 6)
    emitter.ins('cmpi.w', f"#0x{rules['script_arrival_count']:x},0xff703c:l", 8)
    emitter.ins(rules['script_arrival_equal_relation_true_branch'] + '.w', 'scene_pc_039bc0', 4)
    emitter.ins('cmpi.w', f"#0x{rules['script_arrival_count']:x},0xff703c:l", 8)
    emitter.ins(rules['script_arrival_past_relation_true_branch'] + '.w', 'scene_pc_039c4c', 4)
    emitter.ins('movea.l', '120(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', f"#0x{rules['script_fixed_x']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_y']:x},%d1", 4)
    emitter.ins('moveq', '#5,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x100,%d4', 4)
    emitter.ins('jsr', '3152(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('movea.l', '100(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', f"#0x{rules['script_fixed_x']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_y']:x},%d1", 4)
    emitter.ins('moveq', '#5,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '3124(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('cmpi.w', f"#0x{rules['script_arrival_position_bound']:x},0xff7028:l", 8)
    emitter.ins(rules['script_arrival_position_relation_false_branch'] + '.w', 'scene_pc_039b90', 4)
    emitter.ins('move.w', '0xf320:w,%d0', 4)
    emitter.ins('andi.w', f"#0x{rules['script_arrival_tick_mask']:x},%d0", 4)
    emitter.ins('bne.w', 'scene_pc_039b90', 4)
    emitter.ins('subq.w', f"#0x{rules['script_arrival_position_step']:x},0xff7028:l", 6)
    emitter.ins('movea.l', '38(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', '0xff7028:l,%d0', 6)
    emitter.ins('move.w', '0xff702a:l,%d1', 6)
    emitter.ins('moveq', '#4,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '2548(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('bra.w', 'scene_pc_039afe', 4)
    emitter.segment(236480, 236524)
    emitter.ins('move.w', '0xff7026:l,%d0', 6)
    emitter.ins('asl.w', '#0x1,%d0', 2)
    emitter.ins('lea.l', '34(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('lea.l', '76(%pc),%a1', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', '(%a0, %d0.w),%d1', 4)
    emitter.ins('move.w', '(%a1, %d0.w),%d2', 4)
    emitter.ins('move.w', '%d1,0xff7028:l', 6)
    emitter.ins('move.w', '%d2,0xff702a:l', 6)
    emitter.ins('bra.w', 'scene_pc_039c4c', 4)
    emitter.segment(236620, 236728)
    emitter.ins('move.w', '0xff7026:l,%d0', 6)
    emitter.ins('moveq', '#0,%d1', 2)
    emitter.ins('lea.l', '130(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.b', '(%a0, %d0.w),%d1', 4)
    emitter.ins('asl.w', '#0x2,%d1', 2)
    emitter.ins('movem.l', '%d0-%d1,-(%a7)', 4)
    emitter.ins('movea.l', '82(%pc, %d1.w),%a0', 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_x']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_y']:x},%d1", 4)
    emitter.ins('moveq', '#3,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '2856(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('movem.l', '(%a7)+,%d0-%d1', 4)
    emitter.ins('cmpi.w', '#0xc,%d0', 4)
    emitter.ins('beq.w', 'scene_pc_039cb4', 4)
    emitter.ins('movem.l', '%d1,-(%a7)', 4)
    emitter.ins('jsr', '-696(%pc)', 4)
    emitter.ins('movem.l', '(%a7)+,%d1', 4)
    emitter.ins('movea.l', '48(%pc, %d1.w),%a0', 4)
    emitter.ins('move.w', '0xff7028:l,%d0', 6)
    emitter.ins('move.w', '0xff702a:l,%d1', 6)
    emitter.ins('moveq', '#2,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '2288(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('bra.w', 'scene_pc_039afe', 4)
    emitter.segment(236784, 236906)
    emitter.ins('cmpi.w', '#0x15,0xff7026:l', 8)
    emitter.ins('bhi.w', 'scene_pc_039e3e', 4)
    emitter.ins('cmpi.w', '#0x14,0xff7026:l', 8)
    emitter.ins('beq.w', 'scene_pc_039d12', 4)
    emitter.ins('movea.l', '104(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('bra.w', 'scene_pc_039d18', 4)
    emitter.ins('movea.l', '86(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', f"#0x{rules['script_fixed_x']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_y']:x},%d1", 4)
    emitter.ins('moveq', '#3,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '2680(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('jsr', '-856(%pc)', 4)
    emitter.ins('moveq', '#4,%d1', 2)
    emitter.ins('cmpi.w', '#0x14,0xff7026:l', 8)
    emitter.ins('beq.w', 'scene_pc_039d48', 4)
    emitter.ins('movea.l', '48(%pc, %d1.w),%a0', 4)
    emitter.ins('bra.w', 'scene_pc_039d4c', 4)
    emitter.ins('movea.l', '32(%pc, %d1.w),%a0', 4)
    emitter.ins('move.w', '0xff7028:l,%d0', 6)
    emitter.ins('move.w', '0xff702a:l,%d1', 6)
    emitter.ins('moveq', '#2,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '2110(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('bra.w', 'scene_pc_039afe', 4)
    emitter.segment(236922, 237086)
    emitter.ins('cmpi.w', '#0x1b,0xff7026:l', 8)
    emitter.ins('beq.w', 'scene_pc_03980e', 4)
    emitter.ins('cmpi.w', '#0x1b,0xff7026:l', 8)
    emitter.ins('bhi.w', 'scene_pc_03a114', 4)
    emitter.ins('jsr', '-956(%pc)', 4)
    emitter.ins('movea.l', '134(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', '0xff7028:l,%d0', 6)
    emitter.ins('move.w', '0xff702a:l,%d1', 6)
    emitter.ins('moveq', '#5,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '2030(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('cmpi.w', f"#0x{rules['script_landing_y']:x},0xff702a:l", 8)
    emitter.ins(rules['script_landing_y_relation_true_branch'] + '.w', 'scene_pc_039e1a', 4)
    emitter.ins('cmpi.w', f"#0x{rules['script_landing_palette_stop']:x},0xff703c:l", 8)
    emitter.ins(rules['script_landing_palette_relation_false_branch'] + '.w', 'scene_pc_039dfe', 4)
    emitter.ins('move.w', '0xf320:w,%d0', 4)
    emitter.ins('andi.w', f"#0x{rules['script_landing_tick_mask']:x},%d0", 4)
    emitter.ins('bne.w', 'scene_pc_039dfe', 4)
    emitter.ins('addq.w', f"#0x{rules['script_landing_palette_step']:x},0xff703c:l", 6)
    emitter.ins('clr.l', '%d3', 2)
    emitter.ins('move.w', '0xff703c:l,%d3', 6)
    emitter.ins('lea.l', '60(%pc),%a1', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('movea.l', '(%a1, %d3.w),%a0', 4)
    emitter.ins('lea.l', '0xfb00:w,%a1', 4)
    emitter.ins('moveq', f"#{rules['script_palette_longs_counter']},%d0", 2)
    emitter.ins('move.l', '(%a0)+,(%a1)+', 2)
    emitter.ins('dbra', '%d0,scene_pc_039df8', 4)
    emitter.ins('moveq', '#4,%d0', 2)
    emitter.ins('movea.l', '28(%pc, %d0.w),%a0', 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_x']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_y']:x},%d1", 4)
    emitter.ins('moveq', '#4,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '2444(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('bra.w', 'scene_pc_039afe', 4)
    emitter.segment(237118, 237328)
    emitter.ins('cmpi.w', '#0x17,0xff7026:l', 8)
    emitter.ins('bhi.w', 'scene_pc_039f4a', 4)
    emitter.ins('jsr', '-1140(%pc)', 4)
    emitter.ins('movea.l', '192(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', '0xff7028:l,%d0', 6)
    emitter.ins('move.w', '0xff702a:l,%d1', 6)
    emitter.ins('moveq', '#5,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '1846(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.b', '0xff702c:l,%d1', 6)
    emitter.ins('move.w', '0xff7028:l,%d2', 6)
    emitter.ins('move.w', '0xff702a:l,%d3', 6)
    emitter.ins('movem.l', '%d1-%d3,-(%a7)', 4)
    emitter.ins('addq.w', '#0x1,0xff7026:l', 6)
    emitter.ins('move.w', '0xff7026:l,%d0', 6)
    emitter.ins('lea.l', '-4162(%pc),%a0', 4)
    emitter.ins('move.b', '(%a0, %d0.w),%d1', 4)
    emitter.ins('move.b', '%d1,0xff702c:l', 6)
    emitter.ins('jsr', '120(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', '0xff7032:l,0xff7028:l', 10)
    emitter.ins('move.w', '0xff7034:l,0xff702a:l', 10)
    emitter.ins('jsr', '-1250(%pc)', 4)
    emitter.ins('moveq', '#4,%d1', 2)
    emitter.ins('movea.l', '80(%pc, %d1.w),%a0', 4)
    emitter.ins('move.w', '0xff7028:l,%d0', 6)
    emitter.ins('move.w', '0xff702a:l,%d1', 6)
    emitter.ins('moveq', '#4,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '1736(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', '0xff7028:l,0xff7032:l', 10)
    emitter.ins('move.w', '0xff702a:l,0xff7034:l', 10)
    emitter.ins('movem.l', '(%a7)+,%d1-%d3', 4)
    emitter.ins('move.b', '%d1,0xff702c:l', 6)
    emitter.ins('move.w', '%d2,0xff7028:l', 6)
    emitter.ins('move.w', '%d3,0xff702a:l', 6)
    emitter.ins('subq.w', '#0x1,0xff7026:l', 6)
    emitter.ins('bra.w', 'scene_pc_039afe', 4)
    emitter.segment(237386, 237672)
    emitter.ins('cmpi.w', '#0x19,0xff7026:l', 8)
    emitter.ins('bhi.w', 'scene_pc_039d7a', 4)
    emitter.ins('addq.w', f"#0x{rules['script_staged_counter_step']:x},0xff7044:l", 6)
    emitter.ins('move.w', '0xf320:w,%d0', 4)
    emitter.ins('btst.l', f"#0x{rules['script_staged_animation_bit_index']:x},%d0", 4)
    emitter.ins('bne.w', 'scene_pc_039f6e', 4)
    emitter.ins('moveq', '#0,%d1', 2)
    emitter.ins('bra.w', 'scene_pc_039f70', 4)
    emitter.ins('moveq', '#4,%d1', 2)
    emitter.ins('jsr', '280(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', f"#0x{rules['script_fixed_x']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_y']:x},%d1", 4)
    emitter.ins('moveq', '#5,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '2074(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('cmpi.w', f"#0x{rules['script_staged_first_delay']:x},0xff7044:l", 8)
    emitter.ins(rules['script_staged_first_delay_relation_true_branch'] + '.w', 'scene_pc_03a064', 4)
    emitter.ins('jsr', '-1474(%pc)', 4)
    emitter.ins('moveq', '#8,%d1', 2)
    emitter.ins('jsr', '234(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', '0xff7028:l,%d0', 6)
    emitter.ins('move.w', '0xff702a:l,%d1', 6)
    emitter.ins('moveq', '#4,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '1510(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('cmpi.w', f"#0x{rules['script_staged_second_delay']:x},0xff7044:l", 8)
    emitter.ins(rules['script_staged_second_delay_relation_true_branch'] + '.w', 'scene_pc_03a064', 4)
    emitter.ins('move.w', '0xff7028:l,%d0', 6)
    emitter.ins('move.w', '0xff702a:l,%d1', 6)
    emitter.ins('move.b', '0xff702c:l,%d2', 6)
    emitter.ins('movem.l', '%d0-%d2,-(%a7)', 4)
    emitter.ins('addq.w', '#0x1,0xff7026:l', 6)
    emitter.ins('move.w', '0xff7026:l,%d0', 6)
    emitter.ins('lea.l', '-4510(%pc),%a0', 4)
    emitter.ins('move.b', '(%a0, %d0.w),%d1', 4)
    emitter.ins('move.b', '%d1,0xff702c:l', 6)
    emitter.ins('move.w', '0xff7032:l,0xff7028:l', 10)
    emitter.ins('move.w', '0xff7034:l,0xff702a:l', 10)
    emitter.ins('jsr', '-1592(%pc)', 4)
    emitter.ins('moveq', '#12,%d1', 2)
    emitter.ins('jsr', '116(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', '0xff7028:l,%d0', 6)
    emitter.ins('move.w', '0xff702a:l,%d1', 6)
    emitter.ins('moveq', '#4,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '1392(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', '0xff7028:l,0xff7032:l', 10)
    emitter.ins('move.w', '0xff702a:l,0xff7034:l', 10)
    emitter.ins('movem.l', '(%a7)+,%d0-%d2', 4)
    emitter.ins('move.w', '%d0,0xff7028:l', 6)
    emitter.ins('move.w', '%d1,0xff702a:l', 6)
    emitter.ins('move.b', '%d2,0xff702c:l', 6)
    emitter.ins('subq.w', '#0x1,0xff7026:l', 6)
    emitter.ins('bra.w', 'scene_pc_039afe', 4)
    emitter.segment(237844, 238040)
    emitter.ins('cmpi.w', '#0x1c,0xff7026:l', 8)
    emitter.ins('beq.w', 'scene_pc_039f56', 4)
    emitter.ins('cmpi.w', '#0x1d,0xff7026:l', 8)
    emitter.ins('bhi.w', 'scene_pc_03a12c', 4)
    emitter.ins('cmpi.w', '#0x1e,0xff7026:l', 8)
    emitter.ins('beq.w', 'scene_pc_039994', 4)
    emitter.ins('cmpi.w', '#0x1f,0xff7026:l', 8)
    emitter.ins('beq.w', 'scene_pc_0399b6', 4)
    emitter.ins('cmpi.w', '#0x20,0xff7026:l', 8)
    emitter.ins('beq.w', 'scene_pc_03a1e0', 4)
    emitter.ins('cmpi.w', '#0x21,0xff7026:l', 8)
    emitter.ins('beq.w', 'scene_pc_03a322', 4)
    emitter.ins('cmpi.w', '#0x22,0xff7026:l', 8)
    emitter.ins('beq.w', 'scene_pc_03a3ce', 4)
    emitter.ins('cmpi.w', '#0x23,0xff7026:l', 8)
    emitter.ins('beq.w', 'scene_pc_03a48a', 4)
    emitter.ins('cmpi.w', '#0x25,0xff7026:l', 8)
    emitter.ins('beq.w', 'scene_pc_03a4ce', 4)
    emitter.ins('cmpi.w', '#0x27,0xff7026:l', 8)
    emitter.ins('beq.w', 'scene_pc_03a512', 4)
    emitter.ins('cmpi.w', '#0x1f,0xff7026:l', 8)
    emitter.ins('beq.w', 'scene_pc_03a1b8', 4)
    emitter.ins('movea.l', '62(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', f"#0x{rules['script_fixed_x']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_y']:x},%d1", 4)
    emitter.ins('moveq', '#5,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '1522(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('bra.w', 'scene_pc_039afe', 4)
    emitter.ins('moveq', '#4,%d1', 2)
    emitter.ins('movea.l', '28(%pc, %d1.w),%a0', 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_x']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_y']:x},%d1", 4)
    emitter.ins('moveq', '#4,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '1490(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('bra.w', 'scene_pc_039afe', 4)
    emitter.segment(238048, 238300)
    emitter.ins('clr.l', '%d0', 2)
    emitter.ins('move.w', '0xff703c:l,%d0', 6)
    emitter.ins('lea.l', '242(%pc),%a1', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('adda.w', '%d0,%a1', 2)
    emitter.ins('move.w', '(%a1),0xff7028:l', 6)
    emitter.ins('addi.w', f"#0x{rules['script_wave_step']:x},0xff703c:l", 8)
    emitter.ins('move.w', '0xff703c:l,%d0', 6)
    emitter.ins('lea.l', '214(%pc),%a1', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('adda.w', '%d0,%a1', 2)
    emitter.ins('move.w', f"#0x{rules['script_wave_y']:x},0xff702a:l", 8)
    emitter.ins('move.w', '0xf320:w,%d0', 4)
    emitter.ins('andi.w', f"#0x{rules['script_wave_tick_mask']:x},%d0", 4)
    emitter.ins('beq.w', 'scene_pc_03a22a', 4)
    emitter.ins('subq.w', f"#0x{rules['script_wave_step']:x},0xff703c:l", 6)
    emitter.ins('bra.w', 'scene_pc_03a250', 4)
    emitter.ins('addi.w', f"#0x{rules['script_wave_step']:x},0xff703c:l", 8)
    emitter.ins('lea.l', '168(%pc),%a1', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('adda.w', '0xff703c:l,%a1', 6)
    emitter.ins('move.w', '(%a1),%d1', 2)
    emitter.ins('cmpi.w', f"#0x{rules['script_wave_terminator']:x},%d1", 4)
    emitter.ins('bne.w', 'scene_pc_03a250', 4)
    emitter.ins('move.w', '#0x0,0xff703c:l', 8)
    emitter.ins('lea.l', '-5326(%pc),%a1', 4)
    emitter.ins('movea.l', '(%a1),%a0', 2)
    emitter.ins('move.w', '0xff7028:l,%d0', 6)
    emitter.ins('move.w', '0xff702a:l,%d1', 6)
    emitter.ins('moveq', '#3,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '820(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('cmpi.w', f"#0x{rules['script_wave_delay']:x},0xff703e:l", 8)
    emitter.ins(rules['script_wave_delay_relation_true_branch'] + '.w', 'scene_pc_039afe', 4)
    emitter.ins('cmpi.w', f"#0x{rules['script_wave_palette_stop']:x},0xff7004:l", 8)
    emitter.ins(rules['script_wave_palette_relation_false_branch'] + '.w', 'scene_pc_03a2b8', 4)
    emitter.ins('move.w', '0xf320:w,%d0', 4)
    emitter.ins('andi.w', f"#0x{rules['script_wave_palette_tick_mask']:x},%d0", 4)
    emitter.ins('bne.w', 'scene_pc_03a2b8', 4)
    emitter.ins('addq.w', f"#0x{rules['script_wave_palette_step']:x},0xff7004:l", 6)
    emitter.ins('clr.l', '%d3', 2)
    emitter.ins('move.w', '0xff7004:l,%d3', 6)
    emitter.ins('lea.l', '98(%pc),%a1', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('movea.l', '(%a1, %d3.w),%a0', 4)
    emitter.ins('lea.l', '0xfb00:w,%a1', 4)
    emitter.ins('moveq', f"#{rules['script_palette_longs_counter']},%d0", 2)
    emitter.ins('move.l', '(%a0)+,(%a1)+', 2)
    emitter.ins('dbra', '%d0,scene_pc_03a2b2', 4)
    emitter.ins('lea.l', '-5430(%pc),%a1', 4)
    emitter.ins('adda.w', '#0x4,%a1', 4)
    emitter.ins('movea.l', '(%a1),%a0', 2)
    emitter.ins('move.w', f"#0x{rules['script_fixed_x']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_y']:x},%d1", 4)
    emitter.ins('moveq', '#5,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '1230(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('bra.w', 'scene_pc_039afe', 4)
    emitter.segment(238370, 238514)
    emitter.ins('jsr', '-2380(%pc)', 4)
    emitter.ins('lea.l', '-5532(%pc),%a1', 4)
    emitter.ins('movea.l', '(%a1),%a0', 2)
    emitter.ins('move.w', '0xff7028:l,%d0', 6)
    emitter.ins('move.w', '0xff702a:l,%d1', 6)
    emitter.ins('moveq', '#4,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '606(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('cmpi.w', f"#0x{rules['script_late_delay']:x},0xff703e:l", 8)
    emitter.ins(rules['script_late_delay_relation_true_branch'] + '.w', 'scene_pc_039afe', 4)
    emitter.ins('cmpi.w', f"#0x{rules['script_late_palette_stop']:x},0xff703c:l", 8)
    emitter.ins(rules['script_late_palette_relation_false_branch'] + '.w', 'scene_pc_03a38e', 4)
    emitter.ins('move.w', '0xf320:w,%d0', 4)
    emitter.ins('andi.w', f"#0x{rules['script_late_tick_mask']:x},%d0", 4)
    emitter.ins('bne.w', 'scene_pc_03a38e', 4)
    emitter.ins('addq.w', f"#0x{rules['script_late_palette_step']:x},0xff703c:l", 6)
    emitter.ins('clr.l', '%d3', 2)
    emitter.ins('move.w', '0xff703c:l,%d3', 6)
    emitter.ins('lea.l', '56(%pc),%a1', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('movea.l', '(%a1, %d3.w),%a0', 4)
    emitter.ins('lea.l', '0xfb00:w,%a1', 4)
    emitter.ins('moveq', f"#{rules['script_palette_longs_counter']},%d0", 2)
    emitter.ins('move.l', '(%a0)+,(%a1)+', 2)
    emitter.ins('dbra', '%d0,scene_pc_03a388', 4)
    emitter.ins('lea.l', '-5636(%pc),%a1', 4)
    emitter.ins('adda.w', '#0x4,%a1', 4)
    emitter.ins('movea.l', '(%a1),%a0', 2)
    emitter.ins('move.w', f"#0x{rules['script_fixed_x']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_y']:x},%d1", 4)
    emitter.ins('moveq', '#5,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '1016(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('bra.w', 'scene_pc_039afe', 4)
    emitter.segment(238542, 238642)
    emitter.ins('addq.w', f"#0x{rules['script_three_frame_step']:x},0xff7044:l", 6)
    emitter.ins('cmpi.w', f"#0x{rules['script_three_frame_duration']:x},0xff7044:l", 8)
    emitter.ins(rules['script_three_frame_duration_relation_false_branch'] + '.w', 'scene_pc_03a43e', 4)
    emitter.ins('move.b', '0xf321:w,%d0', 4)
    emitter.ins('btst.l', f"#0x{rules['script_three_frame_tick_bit_index']:x},%d0", 4)
    emitter.ins('bne.w', 'scene_pc_03a40c', 4)
    emitter.ins('cmpi.w', f"#0x{rules['script_three_frame_index_bound']:x},0xff703c:l", 8)
    emitter.ins(rules['script_three_frame_index_relation_false_branch'] + '.w', 'scene_pc_03a404', 4)
    emitter.ins('move.w', '#0x0,0xff703c:l', 8)
    emitter.ins('bra.w', 'scene_pc_03a40c', 4)
    emitter.ins('addi.w', f"#0x{rules['script_three_frame_index_step']:x},0xff703c:l", 8)
    emitter.ins('move.w', '0xff703c:l,%d1', 6)
    emitter.ins('asl.w', '#0x2,%d1', 2)
    emitter.ins('movea.l', '28(%pc, %d1.w),%a0', 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_x']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_y']:x},%d1", 4)
    emitter.ins('moveq', '#5,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '888(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('bra.w', 'scene_pc_039afe', 4)
    emitter.segment(238654, 238722)
    emitter.ins('movea.l', '66(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', f"#0x{rules['script_fixed_x']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_y']:x},%d1", 4)
    emitter.ins('moveq', '#5,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '844(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('jsr', '-2692(%pc)', 4)
    emitter.ins('moveq', '#4,%d1', 2)
    emitter.ins('movea.l', '32(%pc, %d1.w),%a0', 4)
    emitter.ins('move.w', '0xff7028:l,%d0', 6)
    emitter.ins('move.w', '0xff702a:l,%d1', 6)
    emitter.ins('moveq', '#4,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '294(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('bra.w', 'scene_pc_039afe', 4)
    emitter.segment(238730, 238790)
    emitter.ins('movea.l', '58(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', f"#0x{rules['script_fixed_x']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_y']:x},%d1", 4)
    emitter.ins('moveq', '#5,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '768(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('movea.l', '34(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', f"#0x{rules['script_fixed_x']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_y']:x},%d1", 4)
    emitter.ins('moveq', '#5,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x100,%d4', 4)
    emitter.ins('jsr', '740(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('bra.w', 'scene_pc_039afe', 4)
    emitter.segment(238798, 238858)
    emitter.ins('movea.l', '58(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', f"#0x{rules['script_fixed_x']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_y']:x},%d1", 4)
    emitter.ins('moveq', '#5,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '700(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('movea.l', '34(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', f"#0x{rules['script_fixed_x']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_y']:x},%d1", 4)
    emitter.ins('moveq', '#5,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x100,%d4', 4)
    emitter.ins('jsr', '672(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('bra.w', 'scene_pc_039afe', 4)
    emitter.segment(238866, 238898)
    emitter.ins('movea.l', '30(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', f"#0x{rules['script_fixed_x']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['script_fixed_y']:x},%d1", 4)
    emitter.ins('moveq', '#5,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('jsr', '632(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('bra.w', 'scene_pc_039afe', 4)
def _lower_scene_family_update_scripted_scene_position(emitter, rules):
    emitter.segment(235992, 236162)
    emitter.ins('movem.w', '%d1,-(%a7)', 4)
    emitter.ins('move.w', '0xf320:w,%d6', 4)
    emitter.ins('andi.w', f"#0x{rules['movement_tick_mask']:x},%d6", 4)
    emitter.ins('bne.w', 'scene_pc_039a3c', 4)
    emitter.ins('tst.b', '0xff702c:l', 6)
    emitter.ins('beq.w', 'scene_pc_039a3c', 4)
    emitter.ins('addq.w', f"#0x{rules['movement_counter_step']:x},0xff702e:l", 6)
    emitter.ins('move.w', '0xff7026:l,%d0', 6)
    emitter.ins('lea.l', '130(%pc),%a4', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.b', '(%a4, %d0.w),%d1', 4)
    emitter.ins('move.w', '0xff702e:l,%d7', 6)
    emitter.ins('cmp.b', '%d1,%d7', 2)
    emitter.ins(rules['movement_limit_relation_true_branch'] + '.w', 'scene_pc_039a3c', 4)
    emitter.ins('moveq', '#0,%d0', 2)
    emitter.ins('move.b', '0xff702c:l,%d0', 6)
    emitter.ins('btst.l', f"#0x{rules['movement_left_bit_index']:x},%d0", 4)
    emitter.ins('bne.w', 'scene_pc_039a42', 4)
    emitter.ins('btst.l', f"#0x{rules['movement_right_bit_index']:x},%d0", 4)
    emitter.ins('bne.w', 'scene_pc_039a52', 4)
    emitter.ins('btst.l', f"#0x{rules['movement_up_bit_index']:x},%d0", 4)
    emitter.ins('bne.w', 'scene_pc_039a62', 4)
    emitter.ins('btst.l', f"#0x{rules['movement_down_bit_index']:x},%d0", 4)
    emitter.ins('bne.w', 'scene_pc_039a72', 4)
    emitter.ins('movem.w', '(%a7)+,%d1', 4)
    emitter.ins('rts', '', 2)
    emitter.ins('move.w', '%d0,%d1', 2)
    emitter.ins('andi.l', f"#0x{rules['movement_distance_mask']:x},%d1", 6)
    emitter.ins('sub.w', '%d1,0xff7028:l', 6)
    emitter.ins('bra.b', 'scene_pc_039a24', 2)
    emitter.ins('move.w', '%d0,%d1', 2)
    emitter.ins('andi.l', f"#0x{rules['movement_distance_mask']:x},%d1", 6)
    emitter.ins('add.w', '%d1,0xff7028:l', 6)
    emitter.ins('bra.b', 'scene_pc_039a2c', 2)
    emitter.ins('move.w', '%d0,%d1', 2)
    emitter.ins('andi.l', f"#0x{rules['movement_distance_mask']:x},%d1", 6)
    emitter.ins('sub.w', '%d1,0xff702a:l', 6)
    emitter.ins('bra.b', 'scene_pc_039a34', 2)
    emitter.ins('move.w', '%d0,%d1', 2)
    emitter.ins('andi.l', f"#0x{rules['movement_distance_mask']:x},%d1", 6)
    emitter.ins('add.w', '%d1,0xff702a:l', 6)
    emitter.ins('bra.b', 'scene_pc_039a3c', 2)
def _lower_scene_family_initialize_scripted_secondary_position(emitter, rules):
    emitter.segment(237336, 237386)
    emitter.ins('tst.w', '0xff7036:l', 6)
    emitter.ins(rules['secondary_latched_relation_true_branch'] + '.w', 'scene_pc_039f48', 4)
    emitter.ins('asl.w', '#0x1,%d0', 2)
    emitter.ins('lea.l', '-5022(%pc),%a0', 4)
    emitter.ins('lea.l', '-4946(%pc),%a1', 4)
    emitter.ins('move.w', '(%a0, %d0.w),%d1', 4)
    emitter.ins('move.w', '(%a1, %d0.w),%d2', 4)
    emitter.ins('move.w', '%d1,0xff7032:l', 6)
    emitter.ins('move.w', '%d2,0xff7034:l', 6)
    emitter.ins('move.w', f"#0x{rules['secondary_latch_value']:x},0xff7036:l", 8)
    emitter.ins('rts', '', 2)
def _lower_scene_family_select_scene_object_frame(emitter, rules):
    emitter.segment(237706, 237796)
    emitter.ins('cmpi.w', f"#0x{rules['frame_direct_mode_bound']:x},0xff7026:l", 8)
    emitter.ins(rules['frame_direct_mode_relation_false_branch'] + '.w', 'scene_pc_03a09c', 4)
    emitter.ins('movea.l', '-46(%pc, %d1.w),%a0', 4)
    emitter.ins('rts', '', 2)
    emitter.ins('cmpi.w', f"#0x{rules['frame_sequence_bound']:x},%d1", 4)
    emitter.ins(rules['frame_sequence_relation_false_branch'] + '.w', 'scene_pc_03a0de', 4)
    emitter.ins('move.w', '0xff703c:l,%d2', 6)
    emitter.ins('andi.w', f"#0x{rules['frame_sequence_tick_mask']:x},%d0", 4)
    emitter.ins('bne.w', 'scene_pc_03a0be', 4)
    emitter.ins('addq.w', f"#0x{rules['frame_sequence_step']:x},0xff703c:l", 6)
    emitter.ins('move.w', '0xff703c:l,%d2', 6)
    emitter.ins('lea.l', '36(%pc),%a3', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.b', '(%a3, %d2.w),%d1', 4)
    emitter.ins('cmpi.b', f"#0x{rules['frame_sequence_terminator']:x},%d1", 4)
    emitter.ins('bne.w', 'scene_pc_03a0d8', 4)
    emitter.ins('clr.w', '0xff703c:l', 6)
    emitter.ins('moveq', '#0,%d1', 2)
    emitter.ins('andi.l', f"#0x{rules['frame_lookup_keep_mask']:x},%d1", 6)
    emitter.ins('movea.l', '-102(%pc, %d1.w),%a0', 4)
    emitter.ins('rts', '', 2)
def _lower_scene_family_append_clipped_scene_sprites(emitter, rules):
    emitter.segment(239008, 239432)
    emitter.ins('movem.l', '%d5-%d6/%a1,-(%a7)', 4)
    emitter.ins('cmpi.b', f"#0x{rules['sprite_capacity']:x},0xf300:w", 6)
    emitter.ins(rules['sprite_capacity_relation_true_branch'] + '.w', 'scene_pc_03a710', 4)
    emitter.ins('andi.l', '#0xffff,%d4', 6)
    emitter.ins('move.w', '%d2,%d7', 2)
    emitter.ins('andi.w', '#0xfff8,%d2', 4)
    emitter.ins('andi.w', '#0x7,%d7', 4)
    emitter.ins('asl.w', '#0x2,%d7', 2)
    emitter.ins('addi.w', f"#0x{rules['sprite_origin']:x},%d0", 4)
    emitter.ins('bmi.w', 'scene_pc_03a710', 4)
    emitter.ins('btst.l', f"#0x{rules['sprite_horizontal_flip_bit_index']:x},%d2", 4)
    emitter.ins('beq.b', 'scene_pc_03a5d2', 2)
    emitter.ins('subi.w', f"#0x{rules['sprite_flip_adjustment']:x},%d0", 4)
    emitter.ins('addi.w', f"#0x{rules['sprite_origin']:x},%d1", 4)
    emitter.ins('btst.l', f"#0x{rules['sprite_vertical_flip_bit_index']:x},%d2", 4)
    emitter.ins('beq.b', 'scene_pc_03a5e0', 2)
    emitter.ins('subi.w', f"#0x{rules['sprite_flip_adjustment']:x},%d1", 4)
    emitter.ins('clr.w', '%d5', 2)
    emitter.ins('move.b', '0xf300:w,%d5', 4)
    emitter.ins('lsl.w', '#0x3,%d5', 2)
    emitter.ins('lea.l', '0xf800:w,%a1', 4)
    emitter.ins('lea.l', '0xff7006:l,%a2', 6)
    emitter.ins('lea.l', '(%a1, %d5.w),%a1', 4)
    emitter.ins('move.w', '%d0,%d6', 2)
    emitter.ins('clr.w', '0xff7030:l', 6)
    emitter.ins('moveq', '#0,%d5', 2)
    emitter.ins('move.b', '(%a0),%d5', 2)
    emitter.ins('cmpi.b', '#0x80,%d5', 4)
    emitter.ins('beq.w', 'scene_pc_03a710', 4)
    emitter.ins('movem.l', '%d0-%d7/%a0-%a3,-(%a7)', 4)
    emitter.ins('move.w', '0xff7028:l,%d0', 6)
    emitter.ins('btst.l', '#0x7,%d5', 4)
    emitter.ins('bne.w', 'scene_pc_03a622', 4)
    emitter.ins('add.w', '%d5,%d0', 2)
    emitter.ins('bra.w', 'scene_pc_03a626', 4)
    emitter.ins('neg.b', '%d5', 2)
    emitter.ins('sub.w', '%d5,%d0', 2)
    emitter.ins('cmpi.w', f"#0x{rules['sprite_clip_minimum']:x},%d0", 4)
    emitter.ins(rules['sprite_clip_minimum_relation_true_branch'] + '.w', 'scene_pc_03a716', 4)
    emitter.ins('cmpi.w', f"#0x{rules['sprite_clip_x_maximum']:x},%d0", 4)
    emitter.ins(rules['sprite_clip_x_maximum_relation_true_branch'] + '.w', 'scene_pc_03a716', 4)
    emitter.ins('movem.l', '(%a7)+,%d0-%d7/%a0-%a3', 4)
    emitter.ins('tst.w', '0xff7030:l', 6)
    emitter.ins('bne.w', 'scene_pc_03a704', 4)
    emitter.ins('btst.l', f"#0x{rules['sprite_horizontal_flip_bit_index']:x},%d2", 4)
    emitter.ins('beq.w', 'scene_pc_03a64e', 4)
    emitter.ins('neg.b', '%d5', 2)
    emitter.ins('btst.l', '#0x7,%d5', 4)
    emitter.ins('beq.b', 'scene_pc_03a65a', 2)
    emitter.ins('neg.b', '%d5', 2)
    emitter.ins('sub.w', '%d5,%d6', 2)
    emitter.ins('bra.b', 'scene_pc_03a65c', 2)
    emitter.ins('add.w', '%d5,%d6', 2)
    emitter.ins('move.w', '%d6,(%a1)', 2)
    emitter.ins('move.w', '%d1,%d6', 2)
    emitter.ins('move.b', '0x3(%a0),%d5', 4)
    emitter.ins('clr.w', '0xff7030:l', 6)
    emitter.ins('movem.l', '%d0-%d7/%a0-%a3,-(%a7)', 4)
    emitter.ins('move.w', '0xff702a:l,%d0', 6)
    emitter.ins('btst.l', '#0x7,%d5', 4)
    emitter.ins('bne.w', 'scene_pc_03a682', 4)
    emitter.ins('add.w', '%d5,%d0', 2)
    emitter.ins('bra.w', 'scene_pc_03a686', 4)
    emitter.ins('neg.b', '%d5', 2)
    emitter.ins('sub.w', '%d5,%d0', 2)
    emitter.ins('cmpi.w', f"#0x{rules['sprite_clip_minimum']:x},%d0", 4)
    emitter.ins(rules['sprite_clip_minimum_relation_true_branch'] + '.w', 'scene_pc_03a722', 4)
    emitter.ins('cmpi.w', f"#0x{rules['sprite_clip_y_maximum']:x},%d0", 4)
    emitter.ins(rules['sprite_clip_y_maximum_relation_true_branch'] + '.w', 'scene_pc_03a722', 4)
    emitter.ins('movem.l', '(%a7)+,%d0-%d7/%a0-%a3', 4)
    emitter.ins('tst.w', '0xff7030:l', 6)
    emitter.ins('bne.w', 'scene_pc_03a704', 4)
    emitter.ins('btst.l', f"#0x{rules['sprite_vertical_flip_bit_index']:x},%d2", 4)
    emitter.ins('beq.b', 'scene_pc_03a6ac', 2)
    emitter.ins('neg.b', '%d5', 2)
    emitter.ins('btst.l', '#0x7,%d5', 4)
    emitter.ins('beq.b', 'scene_pc_03a6b8', 2)
    emitter.ins('neg.b', '%d5', 2)
    emitter.ins('sub.w', '%d5,%d6', 2)
    emitter.ins('bra.b', 'scene_pc_03a6ba', 2)
    emitter.ins('add.w', '%d5,%d6', 2)
    emitter.ins('move.w', '%d6,0x6(%a1)', 4)
    emitter.ins('move.b', '0x1(%a0),0x2(%a1)', 6)
    emitter.ins('tst.l', '(%a2, %d7.w)', 4)
    emitter.ins('bne.w', 'scene_pc_03a6d8', 4)
    emitter.ins('move.l', '%a1,(%a2, %d7.w)', 4)
    emitter.ins('move.b', '0xf300:w,0x20(%a2, %d7.w)', 6)
    emitter.ins('bra.b', 'scene_pc_03a6e2', 2)
    emitter.ins('movea.l', '0x40(%a2, %d7.w),%a3', 4)
    emitter.ins('move.b', '0xf300:w,0x3(%a3)', 6)
    emitter.ins('move.l', '%a1,0x40(%a2, %d7.w)', 4)
    emitter.ins('addq.b', f"#0x{rules['sprite_count_step']:x},0xf300:w", 4)
    emitter.ins('move.b', '0x1(%a0),%d5', 4)
    emitter.ins('andi.w', f"#0x{rules['sprite_palette_keep_mask']:x},%d5", 4)
    emitter.ins('add.b', '%d3,%d5', 2)
    emitter.ins('eor.w', '%d2,%d5', 2)
    emitter.ins('asl.w', f"#0x{rules['sprite_palette_shift']:x},%d5", 2)
    emitter.ins('or.b', '0x2(%a0),%d5', 4)
    emitter.ins('add.w', '%d4,%d5', 2)
    emitter.ins('move.w', '%d5,0x4(%a1)', 4)
    emitter.ins('addq.l', '#0x8,%a1', 2)
    emitter.ins('addq.l', '#0x4,%a0', 2)
    emitter.ins('cmpi.b', f"#0x{rules['sprite_capacity']:x},0xf300:w", 6)
    emitter.ins(rules['sprite_capacity_relation_false_branch'] + '.w', 'scene_pc_03a5f6', 4)
    emitter.ins('movem.l', '(%a7)+,%d5-%d6/%a1', 4)
    emitter.ins('rts', '', 2)
    emitter.ins('move.w', '#0x1,0xff7030:l', 8)
    emitter.ins('bra.w', 'scene_pc_03a636', 4)
    emitter.ins('move.w', '#0x1,0xff7030:l', 8)
    emitter.ins('bra.w', 'scene_pc_03a696', 4)
    emitter.ins('subi.w', f"#0x{rules['marker_origin_adjustment']:x},%d0", 4)
    emitter.ins('subi.w', f"#0x{rules['marker_origin_adjustment']:x},%d1", 4)
    emitter.ins('moveq', '#0,%d2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.w', '#0x0,%d4', 4)
    emitter.ins('lea.l', '8(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('jmp', '-422(%pc)', 4)
def _lower_scene_family_finish_scene_sprite_chains(emitter, rules):
    emitter.segment(239438, 239500)
    emitter.ins('moveq', '#28,%d0', 2)
    emitter.ins('moveq', '#0,%d1', 2)
    emitter.ins('lea.l', '0xff7006:l,%a0', 6)
    emitter.ins('bsr.b', 'scene_pc_03a78c', 2)
    emitter.ins('subq.w', '#0x4,%d0', 2)
    emitter.ins('bpl.b', 'scene_pc_03a758', 2)
    emitter.ins('lea.l', '0xff7006:l,%a0', 6)
    emitter.ins('moveq', '#0,%d0', 2)
    emitter.ins('move.l', '%d0,(%a0)', 2)
    emitter.ins('move.l', '%d0,0x4(%a0)', 4)
    emitter.ins('move.l', '%d0,0x8(%a0)', 4)
    emitter.ins('move.l', '%d0,0xc(%a0)', 4)
    emitter.ins('move.l', '%d0,0x10(%a0)', 4)
    emitter.ins('move.l', '%d0,0x14(%a0)', 4)
    emitter.ins('move.l', '%d0,0x18(%a0)', 4)
    emitter.ins('move.l', '%d0,0x1c(%a0)', 4)
    emitter.ins('move.b', '#0x0,0xf300:w', 6)
    emitter.ins('rts', '', 2)
def _lower_scene_family_finish_one_scene_sprite_chain(emitter, rules):
    emitter.segment(239500, 239522)
    emitter.ins('tst.l', '(%a0, %d0.w)', 4)
    emitter.ins(rules['scene_chain_nonempty_relation_false_branch'] + '.w', 'scene_pc_03a7a0', 4)
    emitter.ins('movea.l', '0x40(%a0, %d0.w),%a1', 4)
    emitter.ins('move.b', '%d1,0x3(%a1)', 4)
    emitter.ins('move.b', '0x20(%a0, %d0.w),%d1', 4)
    emitter.ins('rts', '', 2)
def _lower_scene_family_append_unclipped_scene_sprites(emitter, rules):
    emitter.segment(239522, 239772)
    emitter.ins('movem.l', '%d5-%d6/%a1,-(%a7)', 4)
    emitter.ins('cmpi.b', f"#0x{rules['sprite_capacity']:x},0xf300:w", 6)
    emitter.ins(rules['sprite_capacity_relation_true_branch'] + '.w', 'scene_pc_03a896', 4)
    emitter.ins('andi.l', '#0xffff,%d4', 6)
    emitter.ins('move.w', '%d2,%d7', 2)
    emitter.ins('andi.w', '#0xfff8,%d2', 4)
    emitter.ins('andi.w', '#0x7,%d7', 4)
    emitter.ins('asl.w', '#0x2,%d7', 2)
    emitter.ins('addi.w', f"#0x{rules['sprite_origin']:x},%d0", 4)
    emitter.ins('bmi.w', 'scene_pc_03a896', 4)
    emitter.ins('btst.l', f"#0x{rules['sprite_horizontal_flip_bit_index']:x},%d2", 4)
    emitter.ins('beq.b', 'scene_pc_03a7d4', 2)
    emitter.ins('subi.w', f"#0x{rules['sprite_flip_adjustment']:x},%d0", 4)
    emitter.ins('addi.w', f"#0x{rules['sprite_origin']:x},%d1", 4)
    emitter.ins('btst.l', f"#0x{rules['sprite_vertical_flip_bit_index']:x},%d2", 4)
    emitter.ins('beq.b', 'scene_pc_03a7e2', 2)
    emitter.ins('subi.w', f"#0x{rules['sprite_flip_adjustment']:x},%d1", 4)
    emitter.ins('clr.w', '%d5', 2)
    emitter.ins('move.b', '0xf300:w,%d5', 4)
    emitter.ins('lsl.w', '#0x3,%d5', 2)
    emitter.ins('lea.l', '0xf800:w,%a1', 4)
    emitter.ins('lea.l', '0xff7006:l,%a2', 6)
    emitter.ins('lea.l', '(%a1, %d5.w),%a1', 4)
    emitter.ins('move.w', '%d0,%d6', 2)
    emitter.ins('moveq', '#0,%d5', 2)
    emitter.ins('move.b', '(%a0),%d5', 2)
    emitter.ins('cmpi.b', '#0x80,%d5', 4)
    emitter.ins('beq.w', 'scene_pc_03a896', 4)
    emitter.ins('btst.l', f"#0x{rules['sprite_horizontal_flip_bit_index']:x},%d2", 4)
    emitter.ins('beq.w', 'scene_pc_03a810', 4)
    emitter.ins('neg.b', '%d5', 2)
    emitter.ins('btst.l', '#0x7,%d5', 4)
    emitter.ins('beq.b', 'scene_pc_03a81c', 2)
    emitter.ins('neg.b', '%d5', 2)
    emitter.ins('sub.w', '%d5,%d6', 2)
    emitter.ins('bra.b', 'scene_pc_03a81e', 2)
    emitter.ins('add.w', '%d5,%d6', 2)
    emitter.ins('move.w', '%d6,(%a1)', 2)
    emitter.ins('move.w', '%d1,%d6', 2)
    emitter.ins('move.b', '0x3(%a0),%d5', 4)
    emitter.ins('btst.l', f"#0x{rules['sprite_vertical_flip_bit_index']:x},%d2", 4)
    emitter.ins('beq.b', 'scene_pc_03a82e', 2)
    emitter.ins('neg.b', '%d5', 2)
    emitter.ins('btst.l', '#0x7,%d5', 4)
    emitter.ins('btst.l', '#0x7,%d5', 4)
    emitter.ins('beq.b', 'scene_pc_03a83e', 2)
    emitter.ins('neg.b', '%d5', 2)
    emitter.ins('sub.w', '%d5,%d6', 2)
    emitter.ins('bra.b', 'scene_pc_03a840', 2)
    emitter.ins('add.w', '%d5,%d6', 2)
    emitter.ins('move.w', '%d6,0x6(%a1)', 4)
    emitter.ins('move.b', '0x1(%a0),0x2(%a1)', 6)
    emitter.ins('tst.l', '(%a2, %d7.w)', 4)
    emitter.ins('bne.w', 'scene_pc_03a85e', 4)
    emitter.ins('move.l', '%a1,(%a2, %d7.w)', 4)
    emitter.ins('move.b', '0xf300:w,0x20(%a2, %d7.w)', 6)
    emitter.ins('bra.b', 'scene_pc_03a868', 2)
    emitter.ins('movea.l', '0x40(%a2, %d7.w),%a3', 4)
    emitter.ins('move.b', '0xf300:w,0x3(%a3)', 6)
    emitter.ins('move.l', '%a1,0x40(%a2, %d7.w)', 4)
    emitter.ins('addq.b', f"#0x{rules['sprite_count_step']:x},0xf300:w", 4)
    emitter.ins('move.b', '0x1(%a0),%d5', 4)
    emitter.ins('andi.w', f"#0x{rules['sprite_palette_keep_mask']:x},%d5", 4)
    emitter.ins('add.b', '%d3,%d5', 2)
    emitter.ins('eor.w', '%d2,%d5', 2)
    emitter.ins('asl.w', f"#0x{rules['sprite_palette_shift']:x},%d5", 2)
    emitter.ins('or.b', '0x2(%a0),%d5', 4)
    emitter.ins('add.w', '%d4,%d5', 2)
    emitter.ins('move.w', '%d5,0x4(%a1)', 4)
    emitter.ins('addq.l', '#0x8,%a1', 2)
    emitter.ins('addq.l', '#0x4,%a0', 2)
    emitter.ins('cmpi.b', f"#0x{rules['sprite_capacity']:x},0xf300:w", 6)
    emitter.ins(rules['sprite_capacity_relation_false_branch'] + '.w', 'scene_pc_03a7f8', 4)
    emitter.ins('movem.l', '(%a7)+,%d5-%d6/%a1', 4)
    emitter.ins('rts', '', 2)
def _lower_scene_family_advance_scene_palette_fade(emitter, rules):
    emitter.segment(239992, 240138)
    emitter.ins('move.w', '0x80c4:w,%d0', 4)
    emitter.ins('bmi.w', 'scene_pc_03a9b8', 4)
    emitter.ins('subq.w', f"#0x{rules['palette_delay_step']:x},0x80c6:w", 4)
    emitter.ins('bpl.w', 'scene_pc_03a9b8', 4)
    emitter.ins('andi.w', f"#0x{rules['palette_period_keep_mask']:x},%d0", 4)
    emitter.ins('move.w', '%d0,0x80c6:w', 4)
    emitter.ins('cmpi.b', '#0x0,0x80c4:w', 6)
    emitter.ins('beq.b', 'scene_pc_03a9aa', 2)
    emitter.ins('addq.w', f"#0x{rules['palette_shade_step']:x},0x80c8:w", 4)
    emitter.ins('cmpi.w', f"#0x{rules['palette_shade_ceiling']:x},0x80c8:w", 6)
    emitter.ins(rules['palette_shade_end_relation_true_branch'] + '.w', 'scene_pc_03a9b2', 4)
    emitter.ins('bra.w', 'scene_pc_03a9ba', 4)
    emitter.ins('subq.w', f"#0x{rules['palette_shade_step']:x},0x80c8:w", 4)
    emitter.ins('bpl.w', 'scene_pc_03a9ba', 4)
    emitter.ins('move.w', '#0xffff,0x80c4:w', 6)
    emitter.ins('rts', '', 2)
    emitter.ins('move.w', '0x80c8:w,%d0', 4)
    emitter.ins('andi.w', f"#0x{rules['palette_component_mask']:x},%d0", 4)
    emitter.ins('move.w', '%d0,0x8000:w', 4)
    emitter.ins('lea.l', '0xfb00:w,%a0', 4)
    emitter.ins('lea.l', '0xfb80:w,%a1', 4)
    emitter.ins('lea.l', '0x80ca:w,%a2', 4)
    emitter.ins('moveq', '#0,%d2', 2)
    emitter.ins('moveq', '#0,%d7', 2)
    emitter.ins('moveq', '#31,%d1', 2)
    emitter.ins('move.l', '(%a2, %d7.w),%d6', 4)
    emitter.ins('lsr.l', '#0x1,%d6', 2)
    emitter.ins('bcc.w', 'scene_pc_03a9fa', 4)
    emitter.ins('clr.w', '%d5', 2)
    emitter.ins('move.w', '(%a1, %d2.w),%d3', 4)
    emitter.ins('bsr.w', 'scene_pc_03aa0a', 4)
    emitter.ins('bsr.w', 'scene_pc_03aa0a', 4)
    emitter.ins('bsr.w', 'scene_pc_03aa0a', 4)
    emitter.ins('ror.w', f"#0x{rules['fade_nibble_rotation']:x},%d5", 2)
    emitter.ins('move.w', '%d5,(%a0, %d2.w)', 4)
    emitter.ins('addq.w', '#0x2,%d2', 2)
    emitter.ins('dbra', '%d1,scene_pc_03a9dc', 4)
    emitter.ins('addq.w', '#0x4,%d7', 2)
    emitter.ins('cmpi.w', '#0x8,%d7', 4)
    emitter.ins('bcs.b', 'scene_pc_03a9d6', 2)
    emitter.ins('rts', '', 2)
def _lower_scene_family_fade_palette_component(emitter, rules):
    emitter.segment(240138, 240160)
    emitter.ins('move.b', '%d3,%d4', 2)
    emitter.ins('andi.w', f"#0x{rules['palette_component_mask']:x},%d4", 4)
    emitter.ins('sub.b', '0x8001:w,%d4', 4)
    emitter.ins('bcc.b', 'scene_pc_03aa18', 2)
    emitter.ins('moveq', '#0,%d4', 2)
    emitter.ins('or.w', '%d4,%d5', 2)
    emitter.ins('ror.w', f"#0x{rules['fade_nibble_rotation']:x},%d5", 2)
    emitter.ins('lsr.w', f"#0x{rules['fade_nibble_rotation']:x},%d3", 2)
    emitter.ins('rts', '', 2)
def _lower_scene_family_begin_scene_palette_darken(emitter, rules):
    emitter.segment(240160, 240182)
    emitter.ins('andi.w', f"#0x{rules['palette_period_keep_mask']:x},%d0", 4)
    emitter.ins('move.w', '%d0,0x80c4:w', 4)
    emitter.ins('move.w', '#0x0,0x80c6:w', 6)
    emitter.ins('move.w', f"#0x{rules['palette_shade_ceiling']:x},0x80c8:w", 6)
    emitter.ins('rts', '', 2)
def _lower_scene_family_snapshot_and_clear_scene_palette(emitter, rules):
    emitter.segment(240266, 240286)
    emitter.ins('moveq', f"#{rules['palette_snapshot_longs_counter']},%d1", 2)
    emitter.ins('lea.l', '0xfb00:w,%a0', 4)
    emitter.ins('lea.l', '0xfb80:w,%a1', 4)
    emitter.ins('move.l', '(%a0),(%a1)+', 2)
    emitter.ins('clr.l', '(%a0)+', 2)
    emitter.ins('dbra', '%d1,scene_pc_03aa94', 4)
    emitter.ins('rts', '', 2)
def _lower_scene_family_read_vdp_plane_rle_rows(emitter, rules):
    emitter.segment(240334, 240466)
    emitter.ins('clr.w', '0x8000:w', 4)
    emitter.ins('move.w', f"#0x{rules['plane_initial_rows']:x},%d6", 4)
    emitter.ins('clr.w', '0x8002:w', 4)
    emitter.ins('move.w', '#0x8f02,0xc00004:l', 8)
    emitter.ins('move.w', '%a1,%d0', 2)
    emitter.ins('bsr.w', 'scene_pc_03b2b0', 4)
    emitter.ins('moveq', '#0,%d4', 2)
    emitter.ins('tst.w', '0x8002:w', 4)
    emitter.ins('bne.b', 'scene_pc_03aaf2', 2)
    emitter.ins('move.b', '(%a0)+,%d1', 2)
    emitter.ins('move.b', '(%a0)+,%d2', 2)
    emitter.ins('tst.w', '0x8002:w', 4)
    emitter.ins('bne.b', 'scene_pc_03ab00', 2)
    emitter.ins('cmp.b', '%d2,%d1', 2)
    emitter.ins(rules['plane_stream_marker_relation_false_branch'] + '.w', 'scene_pc_03ab12', 4)
    emitter.ins('asl.w', '#0x8,%d2', 2)
    emitter.ins('move.b', '(%a0)+,%d2', 2)
    emitter.ins('or.w', '0x8000:w,%d2', 4)
    emitter.ins('move.w', '%d2,0xc00000:l', 6)
    emitter.ins('bsr.b', 'scene_pc_03ab32', 2)
    emitter.ins('bra.b', 'scene_pc_03aaf2', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.b', '(%a0)+,%d3', 2)
    emitter.ins('beq.w', 'scene_pc_03ab50', 4)
    emitter.ins('move.b', '(%a0)+,%d2', 2)
    emitter.ins('asl.w', '#0x8,%d2', 2)
    emitter.ins('move.b', '(%a0)+,%d2', 2)
    emitter.ins('or.w', '0x8000:w,%d2', 4)
    emitter.ins('move.w', '%d2,0xc00000:l', 6)
    emitter.ins('bsr.b', 'scene_pc_03ab32', 2)
    emitter.ins('dbra', '%d3,scene_pc_03ab20', 4)
    emitter.ins('bra.b', 'scene_pc_03aaf2', 2)
    emitter.ins('addq.w', f"#0x{rules['plane_column_step']:x},%d4", 2)
    emitter.ins('cmpi.b', f"#0x{rules['plane_column_bound']:x},%d4", 4)
    emitter.ins(rules['plane_column_end_relation_false_branch'] + '.w', 'scene_pc_03ab50', 4)
    emitter.ins('subq.w', f"#0x{rules['plane_row_step']:x},%d6", 2)
    emitter.ins('bne.b', 'scene_pc_03ab46', 2)
    emitter.ins('movem.l', '(%a7)+,%d0', 4)
    emitter.ins('rts', '', 2)
    emitter.ins('adda.l', '%d5,%a1', 2)
    emitter.ins('move.w', '%a1,%d0', 2)
    emitter.ins('bsr.w', 'scene_pc_03b2b0', 4)
    emitter.ins('moveq', '#0,%d4', 2)
    emitter.ins('rts', '', 2)
def _lower_scene_family_write_vdp_swapped_byte_rle_stream(emitter, rules):
    emitter.segment(240466, 240532)
    emitter.ins('move.w', '#0x8f02,0xc00004:l', 8)
    emitter.ins('bsr.w', 'scene_pc_03b2b0', 4)
    emitter.ins('move.b', '(%a0)+,%d1', 2)
    emitter.ins('move.b', '(%a0)+,%d2', 2)
    emitter.ins('cmp.b', '%d2,%d1', 2)
    emitter.ins(rules['swapped_stream_marker_relation_false_branch'] + '.w', 'scene_pc_03ab76', 4)
    emitter.ins('move.b', '(%a0)+,%d4', 2)
    emitter.ins('asl.w', '#0x8,%d4', 2)
    emitter.ins('move.b', '%d2,%d4', 2)
    emitter.ins('move.w', '%d4,0xc00000:l', 6)
    emitter.ins('bra.b', 'scene_pc_03ab60', 2)
    emitter.ins('moveq', '#0,%d3', 2)
    emitter.ins('move.b', '(%a0)+,%d3', 2)
    emitter.ins('beq.w', 'scene_pc_03ab92', 4)
    emitter.ins('move.b', '(%a0)+,%d2', 2)
    emitter.ins('move.b', '(%a0)+,%d4', 2)
    emitter.ins('asl.w', '#0x8,%d4', 2)
    emitter.ins('move.b', '%d2,%d4', 2)
    emitter.ins('move.w', '%d4,0xc00000:l', 6)
    emitter.ins('dbra', '%d3,scene_pc_03ab86', 4)
    emitter.ins('bra.b', 'scene_pc_03ab60', 2)
    emitter.ins('rts', '', 2)
def _lower_scene_family_copy_scene_palette_variant(emitter, rules):
    emitter.segment(240532, 240556)
    emitter.ins('lea.l', '22(%pc),%a1', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('lsl.w', '#0x3,%d0', 2)
    emitter.ins('adda.w', '%d0,%a1', 2)
    emitter.ins('movea.l', '(%a1)+,%a2', 2)
    emitter.ins('movea.w', '(%a1)+,%a3', 2)
    emitter.ins('move.w', '(%a1)+,%d7', 2)
    emitter.ins('move.l', '(%a2)+,(%a3)+', 2)
    emitter.ins('dbra', '%d7,scene_pc_03aba4', 4)
    emitter.ins('rts', '', 2)
def _lower_scene_family_finish_actor_sprite_chains(emitter, rules):
    emitter.segment(242236, 242290)
    emitter.ins('moveq', '#28,%d0', 2)
    emitter.ins('moveq', '#0,%d1', 2)
    emitter.ins('lea.l', '0x8044:w,%a0', 4)
    emitter.ins('bsr.b', 'scene_pc_03b272', 2)
    emitter.ins('subq.w', '#0x4,%d0', 2)
    emitter.ins('bpl.b', 'scene_pc_03b244', 2)
    emitter.ins('moveq', '#0,%d0', 2)
    emitter.ins('move.l', '%d0,(%a0)', 2)
    emitter.ins('move.l', '%d0,0x4(%a0)', 4)
    emitter.ins('move.l', '%d0,0x8(%a0)', 4)
    emitter.ins('move.l', '%d0,0xc(%a0)', 4)
    emitter.ins('move.l', '%d0,0x10(%a0)', 4)
    emitter.ins('move.l', '%d0,0x14(%a0)', 4)
    emitter.ins('move.l', '%d0,0x18(%a0)', 4)
    emitter.ins('move.l', '%d0,0x1c(%a0)', 4)
    emitter.ins('move.b', '#0x0,0xf300:w', 6)
    emitter.ins('rts', '', 2)
def _lower_scene_family_finish_one_actor_sprite_chain(emitter, rules):
    emitter.segment(242290, 242312)
    emitter.ins('tst.l', '(%a0, %d0.w)', 4)
    emitter.ins(rules['scene_chain_nonempty_relation_false_branch'] + '.w', 'scene_pc_03b286', 4)
    emitter.ins('movea.l', '0x40(%a0, %d0.w),%a1', 4)
    emitter.ins('move.b', '%d1,0x3(%a1)', 4)
    emitter.ins('move.b', '0x20(%a0, %d0.w),%d1', 4)
    emitter.ins('rts', '', 2)
def _lower_scene_family_set_vram_write_address(emitter, rules):
    emitter.segment(242352, 242392)
    emitter.ins('movem.l', '%d1,-(%a7)', 4)
    emitter.ins('andi.l', '#0xffff,%d0', 6)
    emitter.ins('move.l', '%d0,%d1', 2)
    emitter.ins('andi.w', '#0x3fff,%d0', 4)
    emitter.ins('ori.w', '#0x4000,%d0', 4)
    emitter.ins('swap', '%d0', 2)
    emitter.ins('lsr.w', '#0x8,%d1', 2)
    emitter.ins('lsr.w', '#0x6,%d1', 2)
    emitter.ins('or.l', '%d1,%d0', 2)
    emitter.ins('move.l', '%d0,0xc00004:l', 6)
    emitter.ins('movem.l', '(%a7)+,%d1', 4)
    emitter.ins('rts', '', 2)
def _lower_scene_family_sample_random_preserving_seed_carrier(emitter, rules):
    emitter.segment(243490, 243506)
    emitter.ins('movem.l', '%d1,-(%a7)', 4)
    emitter.ins('jsr', 'scene_pc_0083d4:l', 6)
    emitter.ins('movem.l', '(%a7)+,%d1', 4)
    emitter.ins('rts', '', 2)

LOWERERS = {
    'flush_scene_transfer_queue': _lower_scene_family_flush_scene_transfer_queue,
    'write_vdp_packet_stream': _lower_scene_family_write_vdp_packet_stream,
    'write_vdp_dictionary_repeat_stream': _lower_scene_family_write_vdp_dictionary_repeat_stream,
    'decode_glyph_rows_to_buffers': _lower_scene_family_decode_glyph_rows_to_buffers,
    'darken_palette': _lower_scene_family_darken_palette,
    'darken_palette_component': _lower_scene_family_darken_palette_component,
    'write_vdp_word_rle_stream': _lower_scene_family_write_vdp_word_rle_stream,
    'play_scripted_scene': _lower_scene_family_play_scripted_scene,
    'update_scripted_scene_position': _lower_scene_family_update_scripted_scene_position,
    'initialize_scripted_secondary_position': _lower_scene_family_initialize_scripted_secondary_position,
    'select_scene_object_frame': _lower_scene_family_select_scene_object_frame,
    'append_clipped_scene_sprites': _lower_scene_family_append_clipped_scene_sprites,
    'finish_scene_sprite_chains': _lower_scene_family_finish_scene_sprite_chains,
    'finish_one_scene_sprite_chain': _lower_scene_family_finish_one_scene_sprite_chain,
    'append_unclipped_scene_sprites': _lower_scene_family_append_unclipped_scene_sprites,
    'advance_scene_palette_fade': _lower_scene_family_advance_scene_palette_fade,
    'fade_palette_component': _lower_scene_family_fade_palette_component,
    'begin_scene_palette_darken': _lower_scene_family_begin_scene_palette_darken,
    'snapshot_and_clear_scene_palette': _lower_scene_family_snapshot_and_clear_scene_palette,
    'read_vdp_plane_rle_rows': _lower_scene_family_read_vdp_plane_rle_rows,
    'write_vdp_swapped_byte_rle_stream': _lower_scene_family_write_vdp_swapped_byte_rle_stream,
    'copy_scene_palette_variant': _lower_scene_family_copy_scene_palette_variant,
    'finish_actor_sprite_chains': _lower_scene_family_finish_actor_sprite_chains,
    'finish_one_actor_sprite_chain': _lower_scene_family_finish_one_actor_sprite_chain,
    'set_vram_write_address': _lower_scene_family_set_vram_write_address,
    'sample_random_preserving_seed_carrier': _lower_scene_family_sample_random_preserving_seed_carrier,
}

# B20 role locations now point at actual sole fields, never an old source copy.
_PLAYER_FIELD_ROLE_PATHS = {'word_stream_marker_relation': {'function': 'write_vdp_word_rle_stream_fields',
                                 'paths': (('body', 7, 'body', 4, 'test', 'ops', 0),),
                                 'coupled_uses': ()},
 'scene_chain_nonempty_relation': {'function': 'finish_one_scene_sprite_chain_fields',
                                   'paths': (('body', 4, 'test', 'ops', 0),),
                                   'coupled_uses': (('finish_one_actor_sprite_chain',
                                                     ('body', 5, 'test', 'ops', 0)),)},
 'sprite_capacity': {'function': '_append_scene_sprite_fields',
                     'paths': (('body', 6, 'test', 'comparators', 0),
                               ('body', 27, 'body', 12, 'test', 'comparators', 0),
                               ('body', 5, 'value', 'args', 3),
                               ('body', 27, 'body', 11, 'value', 'args', 3)),
                     'coupled_uses': ()},
 'sprite_capacity_relation': {'function': '_append_scene_sprite_fields',
                              'paths': (('body', 6, 'test', 'ops', 0), ('body', 27, 'body', 12, 'test', 'ops', 0)),
                              'coupled_uses': ()},
 'sprite_origin': {'function': '_append_scene_sprite_fields',
                   'paths': (('body', 13, 'value', 'args', 4), ('body', 17, 'value', 'args', 4)),
                   'coupled_uses': ()},
 'sprite_flip_adjustment': {'function': '_append_scene_sprite_fields',
                            'paths': (('body', 16, 'body', 0, 'value', 'args', 4),
                                      ('body', 19, 'body', 0, 'value', 'args', 4)),
                            'coupled_uses': ()},
 'sprite_horizontal_flip_bit': {'function': '_append_scene_sprite_fields',
                                'paths': (('body', 16, 'test', 'right'),
                                          ('body', 15, 'value', 'args', 3),
                                          ('body', 27, 'body', 8, 'body', 1, 'value', 'args', 2)),
                                'coupled_uses': ()},
 'sprite_vertical_flip_bit': {'function': '_append_scene_sprite_fields',
                              'paths': (('body', 19, 'test', 'right'),
                                        ('body', 18, 'value', 'args', 3),
                                        ('body', 27, 'body', 8, 'body', 8, 'body', 1, 'value', 'args', 2)),
                              'coupled_uses': ()},
 'sprite_clip_minimum': {'function': '_scene_render_clip_axis',
                         'paths': (('body', 9, 'value', 'comparators', 0), ('body', 8, 'value', 'args', 3)),
                         'coupled_uses': ()},
 'sprite_clip_minimum_relation': {'function': '_scene_render_clip_axis',
                                  'paths': (('body', 9, 'value', 'ops', 0),),
                                  'coupled_uses': ()},
 'sprite_clip_x_maximum': {'function': '_append_scene_sprite_fields',
                           'paths': (('body', 27, 'body', 7, 'body', 0, 'value', 'args', 3),),
                           'coupled_uses': ()},
 'sprite_clip_y_maximum': {'function': '_append_scene_sprite_fields',
                           'paths': (('body', 27, 'body', 8, 'body', 7, 'body', 1, 'value', 'args', 3),),
                           'coupled_uses': ()},
 'sprite_clip_x_maximum_relation': {'function': '_scene_render_clip_axis',
                                    'paths': (('body', 10, 'body', 1, 'value', 'ops', 0),),
                                    'coupled_uses': ()},
 'sprite_clip_y_maximum_relation': {'function': '_scene_render_clip_axis',
                                    'paths': (('body', 10, 'body', 1, 'value', 'ops', 0),),
                                    'coupled_uses': ()},
 'sprite_count_step': {'function': '_append_scene_sprite_fields',
                       'paths': (('body', 27, 'body', 8, 'body', 8, 'body', 11, 'value', 'args', 3),),
                       'coupled_uses': ()},
 'sprite_palette_keep_mask': {'function': '_append_scene_sprite_fields',
                              'paths': (('body', 27, 'body', 8, 'body', 8, 'body', 14, 'value', 'right'),),
                              'coupled_uses': ()},
 'sprite_palette_shift': {'function': '_append_scene_sprite_fields',
                          'paths': (('body', 27, 'body', 8, 'body', 8, 'body', 18, 'value', 'args', 4),),
                          'coupled_uses': ()},
 'marker_origin_adjustment': {'function': 'append_scene_marker_sprite_fields',
                              'paths': (('body', 0, 'value', 'args', 4), ('body', 1, 'value', 'args', 4)),
                              'coupled_uses': ()},
 'movement_tick_mask': {'function': 'update_scripted_scene_position_fields',
                        'paths': (('body', 5, 'value', 'args', 2, 'right'), ('body', 6, 'test', 'left', 'right')),
                        'coupled_uses': ()},
 'movement_counter_step': {'function': 'update_scripted_scene_position_fields',
                           'paths': (('body', 6, 'body', 2, 'body', 1, 'value', 'args', 3),),
                           'coupled_uses': ()},
 'movement_limit_relation': {'function': 'update_scripted_scene_position_fields',
                             'paths': (('body', 6, 'body', 2, 'body', 11, 'value', 'operand', 'ops', 0),),
                             'coupled_uses': ()},
 'movement_distance_mask': {'function': 'update_scripted_scene_position_fields',
                            'paths': (('body',
                                       6,
                                       'body',
                                       2,
                                       'body',
                                       12,
                                       'body',
                                       3,
                                       'body',
                                       1,
                                       'body',
                                       1,
                                       'value',
                                       'right'),),
                            'coupled_uses': ()},
 'movement_left_bit': {'function': 'update_scripted_scene_position_fields',
                       'paths': (('body', 6, 'body', 2, 'body', 12, 'body', 3, 'iter', 'elts', 0, 'elts', 0),),
                       'coupled_uses': ()},
 'movement_right_bit': {'function': 'update_scripted_scene_position_fields',
                        'paths': (('body', 6, 'body', 2, 'body', 12, 'body', 3, 'iter', 'elts', 1, 'elts', 0),),
                        'coupled_uses': ()},
 'movement_up_bit': {'function': 'update_scripted_scene_position_fields',
                     'paths': (('body', 6, 'body', 2, 'body', 12, 'body', 3, 'iter', 'elts', 2, 'elts', 0),),
                     'coupled_uses': ()},
 'movement_down_bit': {'function': 'update_scripted_scene_position_fields',
                       'paths': (('body', 6, 'body', 2, 'body', 12, 'body', 3, 'iter', 'elts', 3, 'elts', 0),),
                       'coupled_uses': ()},
 'script_palette_longs': {'function': '_copy_scene_palette_longs_fields',
                          'paths': (('body', 2, 'value'),),
                          'coupled_uses': ()},
 'script_secondary_first_x': {'function': '_play_scripted_scene_core',
                              'paths': (('body', 8, 'body', 0, 'value', 'elts', 0),
                                        ('body', 8, 'orelse', 2, 'body', 0, 'value', 'elts', 0)),
                              'coupled_uses': ()},
 'script_secondary_first_y': {'function': '_play_scripted_scene_core',
                              'paths': (('body', 8, 'body', 0, 'value', 'elts', 1),
                                        ('body', 8, 'orelse', 2, 'body', 0, 'value', 'elts', 1)),
                              'coupled_uses': ()},
 'script_secondary_last_x': {'function': '_play_scripted_scene_core',
                             'paths': (('body', 8, 'orelse', 2, 'orelse', 0, 'value', 'elts', 0),),
                             'coupled_uses': ()},
 'script_secondary_last_y': {'function': '_play_scripted_scene_core',
                             'paths': (('body', 8, 'orelse', 2, 'orelse', 0, 'value', 'elts', 1),),
                             'coupled_uses': ()},
 'script_plane_address': {'function': '_play_scripted_scene_core',
                          'paths': (('body', 32, 'body', 0, 'value'),
                                    ('body', 45, 'body', 6, 'value', 'args', 2),
                                    ('body', 45, 'body', 7, 'value', 'args', 4)),
                          'coupled_uses': ()},
 'script_sound_command': {'function': '_play_scripted_scene_core',
                          'paths': (('body', 54, 'body', 0, 'value', 'args', 4),),
                          'coupled_uses': ()},
 'script_elapsed_step': {'function': '_play_scripted_scene_core',
                         'paths': (('body', 54, 'body', 3, 'value', 'args', 3),),
                         'coupled_uses': ()},
 'script_duration_relation': {'function': '_play_scripted_scene_core',
                              'paths': (('body', 54, 'body', 15, 'test', 'ops', 0),),
                              'coupled_uses': ()}}
ROLE_SPECS = tuple(MenuRole(role.name, _PLAYER_FIELD_ROLE_PATHS[role.name]['function'],
    _PLAYER_FIELD_ROLE_PATHS[role.name]['paths'], role.kind, role.default, role.physical_pcs,
    coupled_uses=_PLAYER_FIELD_ROLE_PATHS[role.name]['coupled_uses']) if role.name in _PLAYER_FIELD_ROLE_PATHS else role
    for role in ROLE_SPECS)

# B20 repair role paths follow the corrected sole packet source.
_PLAYER_REPAIR_ROLE_PATHS = {'word_stream_marker_relation': {'function': 'write_vdp_word_rle_stream_fields',
                                 'paths': (('body', 7, 'body', 4, 'test', 'ops', 0),),
                                 'coupled_uses': ()},
 'scene_chain_nonempty_relation': {'function': 'finish_one_scene_sprite_chain_fields',
                                   'paths': (('body', 4, 'test', 'ops', 0),),
                                   'coupled_uses': (('finish_one_actor_sprite_chain',
                                                     ('body', 5, 'test', 'ops', 0)),)},
 'sprite_capacity': {'function': '_append_scene_sprite_fields',
                     'paths': (('body', 6, 'test', 'comparators', 0),
                               ('body', 25, 'body', 14, 'test', 'comparators', 0),
                               ('body', 5, 'value', 'args', 3),
                               ('body', 25, 'body', 13, 'value', 'args', 3)),
                     'coupled_uses': ()},
 'sprite_capacity_relation': {'function': '_append_scene_sprite_fields',
                              'paths': (('body', 6, 'test', 'ops', 0), ('body', 25, 'body', 14, 'test', 'ops', 0)),
                              'coupled_uses': ()},
 'sprite_origin': {'function': '_append_scene_sprite_fields',
                   'paths': (('body', 13, 'value', 'args', 4), ('body', 17, 'value', 'args', 4)),
                   'coupled_uses': ()},
 'sprite_flip_adjustment': {'function': '_append_scene_sprite_fields',
                            'paths': (('body', 16, 'body', 0, 'value', 'args', 4),
                                      ('body', 19, 'body', 0, 'value', 'args', 4)),
                            'coupled_uses': ()},
 'sprite_horizontal_flip_bit': {'function': '_append_scene_sprite_fields',
                                'paths': (('body', 16, 'test', 'right'),
                                          ('body', 15, 'value', 'args', 3),
                                          ('body', 25, 'body', 10, 'body', 1, 'value', 'args', 2)),
                                'coupled_uses': ()},
 'sprite_vertical_flip_bit': {'function': '_append_scene_sprite_fields',
                              'paths': (('body', 19, 'test', 'right'),
                                        ('body', 18, 'value', 'args', 3),
                                        ('body', 25, 'body', 10, 'body', 8, 'body', 1, 'value', 'args', 2)),
                              'coupled_uses': ()},
 'sprite_clip_minimum': {'function': '_scene_render_clip_axis',
                         'paths': (('body', 9, 'value', 'comparators', 0), ('body', 8, 'value', 'args', 3)),
                         'coupled_uses': ()},
 'sprite_clip_minimum_relation': {'function': '_scene_render_clip_axis',
                                  'paths': (('body', 9, 'value', 'ops', 0),),
                                  'coupled_uses': ()},
 'sprite_clip_x_maximum': {'function': '_append_scene_sprite_fields',
                           'paths': (('body', 25, 'body', 9, 'body', 0, 'value', 'args', 3),),
                           'coupled_uses': ()},
 'sprite_clip_y_maximum': {'function': '_append_scene_sprite_fields',
                           'paths': (('body', 25, 'body', 10, 'body', 7, 'body', 2, 'value', 'args', 3),),
                           'coupled_uses': ()},
 'sprite_clip_x_maximum_relation': {'function': '_scene_render_clip_axis',
                                    'paths': (('body', 10, 'body', 1, 'value', 'ops', 0),),
                                    'coupled_uses': ()},
 'sprite_clip_y_maximum_relation': {'function': '_scene_render_clip_axis',
                                    'paths': (('body', 10, 'body', 1, 'value', 'ops', 0),),
                                    'coupled_uses': ()},
 'sprite_count_step': {'function': '_append_scene_sprite_fields',
                       'paths': (('body', 25, 'body', 10, 'body', 8, 'body', 11, 'value', 'args', 3),),
                       'coupled_uses': ()},
 'sprite_palette_keep_mask': {'function': '_append_scene_sprite_fields',
                              'paths': (('body', 25, 'body', 10, 'body', 8, 'body', 14, 'value', 'right'),),
                              'coupled_uses': ()},
 'sprite_palette_shift': {'function': '_append_scene_sprite_fields',
                          'paths': (('body', 25, 'body', 10, 'body', 8, 'body', 18, 'value', 'args', 4),),
                          'coupled_uses': ()},
 'marker_origin_adjustment': {'function': 'append_scene_marker_sprite_fields',
                              'paths': (('body', 0, 'value', 'args', 4), ('body', 1, 'value', 'args', 4)),
                              'coupled_uses': ()},
 'movement_tick_mask': {'function': 'update_scripted_scene_position_fields',
                        'paths': (('body', 5, 'value', 'args', 2, 'right'), ('body', 6, 'test', 'left', 'right')),
                        'coupled_uses': ()},
 'movement_counter_step': {'function': 'update_scripted_scene_position_fields',
                           'paths': (('body', 6, 'body', 2, 'body', 1, 'value', 'args', 3),),
                           'coupled_uses': ()},
 'movement_limit_relation': {'function': 'update_scripted_scene_position_fields',
                             'paths': (('body', 6, 'body', 2, 'body', 11, 'value', 'operand', 'ops', 0),),
                             'coupled_uses': ()},
 'movement_distance_mask': {'function': 'update_scripted_scene_position_fields',
                            'paths': (('body',
                                       6,
                                       'body',
                                       2,
                                       'body',
                                       12,
                                       'body',
                                       3,
                                       'body',
                                       1,
                                       'body',
                                       1,
                                       'value',
                                       'right'),),
                            'coupled_uses': ()},
 'movement_left_bit': {'function': 'update_scripted_scene_position_fields',
                       'paths': (('body', 6, 'body', 2, 'body', 12, 'body', 3, 'iter', 'elts', 0, 'elts', 0),),
                       'coupled_uses': ()},
 'movement_right_bit': {'function': 'update_scripted_scene_position_fields',
                        'paths': (('body', 6, 'body', 2, 'body', 12, 'body', 3, 'iter', 'elts', 1, 'elts', 0),),
                        'coupled_uses': ()},
 'movement_up_bit': {'function': 'update_scripted_scene_position_fields',
                     'paths': (('body', 6, 'body', 2, 'body', 12, 'body', 3, 'iter', 'elts', 2, 'elts', 0),),
                     'coupled_uses': ()},
 'movement_down_bit': {'function': 'update_scripted_scene_position_fields',
                       'paths': (('body', 6, 'body', 2, 'body', 12, 'body', 3, 'iter', 'elts', 3, 'elts', 0),),
                       'coupled_uses': ()},
 'script_palette_longs': {'function': '_copy_scene_palette_longs_fields',
                          'paths': (('body', 2, 'value'),),
                          'coupled_uses': ()},
 'script_secondary_first_x': {'function': '_play_scripted_scene_core',
                              'paths': (('body', 8, 'body', 0, 'value', 'elts', 0),
                                        ('body', 8, 'orelse', 2, 'body', 0, 'value', 'elts', 0)),
                              'coupled_uses': ()},
 'script_secondary_first_y': {'function': '_play_scripted_scene_core',
                              'paths': (('body', 8, 'body', 0, 'value', 'elts', 1),
                                        ('body', 8, 'orelse', 2, 'body', 0, 'value', 'elts', 1)),
                              'coupled_uses': ()},
 'script_secondary_last_x': {'function': '_play_scripted_scene_core',
                             'paths': (('body', 8, 'orelse', 2, 'orelse', 0, 'value', 'elts', 0),),
                             'coupled_uses': ()},
 'script_secondary_last_y': {'function': '_play_scripted_scene_core',
                             'paths': (('body', 8, 'orelse', 2, 'orelse', 0, 'value', 'elts', 1),),
                             'coupled_uses': ()},
 'script_plane_address': {'function': '_play_scripted_scene_core',
                          'paths': (('body', 32, 'body', 0, 'value'),
                                    ('body', 45, 'body', 6, 'value', 'args', 2),
                                    ('body', 45, 'body', 7, 'value', 'args', 4)),
                          'coupled_uses': ()},
 'script_sound_command': {'function': '_play_scripted_scene_core',
                          'paths': (('body', 54, 'body', 0, 'value', 'args', 4),),
                          'coupled_uses': ()},
 'script_elapsed_step': {'function': '_play_scripted_scene_core',
                         'paths': (('body', 54, 'body', 3, 'value', 'args', 3),),
                         'coupled_uses': ()},
 'script_duration_relation': {'function': '_play_scripted_scene_core',
                              'paths': (('body', 54, 'body', 15, 'test', 'ops', 0),),
                              'coupled_uses': ()}}
ROLE_SPECS = tuple(MenuRole(role.name, _PLAYER_REPAIR_ROLE_PATHS[role.name]['function'],
    _PLAYER_REPAIR_ROLE_PATHS[role.name]['paths'], role.kind, role.default, role.physical_pcs,
    coupled_uses=_PLAYER_REPAIR_ROLE_PATHS[role.name]['coupled_uses']) if role.name in _PLAYER_REPAIR_ROLE_PATHS else role
    for role in ROLE_SPECS)

# B21 actual closed mode role paths, unlifted paired/staged roles unchanged.
_CLOSED_MODE_ROLE_PATHS = {'word_stream_marker_relation': {'function': 'write_vdp_word_rle_stream_fields',
                                 'paths': (('body', 7, 'body', 4, 'test', 'ops', 0),),
                                 'coupled_uses': ()},
 'scene_chain_nonempty_relation': {'function': 'finish_one_scene_sprite_chain_fields',
                                   'paths': (('body', 4, 'test', 'ops', 0),),
                                   'coupled_uses': (('finish_one_actor_sprite_chain',
                                                     ('body', 5, 'test', 'ops', 0)),)},
 'sprite_capacity': {'function': '_append_scene_sprite_fields',
                     'paths': (('body', 6, 'test', 'comparators', 0),
                               ('body', 25, 'body', 14, 'test', 'comparators', 0),
                               ('body', 5, 'value', 'args', 3),
                               ('body', 25, 'body', 13, 'value', 'args', 3)),
                     'coupled_uses': ()},
 'sprite_capacity_relation': {'function': '_append_scene_sprite_fields',
                              'paths': (('body', 6, 'test', 'ops', 0), ('body', 25, 'body', 14, 'test', 'ops', 0)),
                              'coupled_uses': ()},
 'sprite_origin': {'function': '_append_scene_sprite_fields',
                   'paths': (('body', 13, 'value', 'args', 4), ('body', 17, 'value', 'args', 4)),
                   'coupled_uses': ()},
 'sprite_flip_adjustment': {'function': '_append_scene_sprite_fields',
                            'paths': (('body', 16, 'body', 0, 'value', 'args', 4),
                                      ('body', 19, 'body', 0, 'value', 'args', 4)),
                            'coupled_uses': ()},
 'sprite_horizontal_flip_bit': {'function': '_append_scene_sprite_fields',
                                'paths': (('body', 16, 'test', 'right'),
                                          ('body', 15, 'value', 'args', 3),
                                          ('body', 25, 'body', 10, 'body', 1, 'value', 'args', 2)),
                                'coupled_uses': ()},
 'sprite_vertical_flip_bit': {'function': '_append_scene_sprite_fields',
                              'paths': (('body', 19, 'test', 'right'),
                                        ('body', 18, 'value', 'args', 3),
                                        ('body', 25, 'body', 10, 'body', 8, 'body', 1, 'value', 'args', 2)),
                              'coupled_uses': ()},
 'sprite_clip_minimum': {'function': '_scene_render_clip_axis',
                         'paths': (('body', 9, 'value', 'comparators', 0), ('body', 8, 'value', 'args', 3)),
                         'coupled_uses': ()},
 'sprite_clip_minimum_relation': {'function': '_scene_render_clip_axis',
                                  'paths': (('body', 9, 'value', 'ops', 0),),
                                  'coupled_uses': ()},
 'sprite_clip_x_maximum': {'function': '_append_scene_sprite_fields',
                           'paths': (('body', 25, 'body', 9, 'body', 0, 'value', 'args', 3),),
                           'coupled_uses': ()},
 'sprite_clip_y_maximum': {'function': '_append_scene_sprite_fields',
                           'paths': (('body', 25, 'body', 10, 'body', 7, 'body', 2, 'value', 'args', 3),),
                           'coupled_uses': ()},
 'sprite_clip_x_maximum_relation': {'function': '_scene_render_clip_axis',
                                    'paths': (('body', 10, 'body', 1, 'value', 'ops', 0),),
                                    'coupled_uses': ()},
 'sprite_clip_y_maximum_relation': {'function': '_scene_render_clip_axis',
                                    'paths': (('body', 10, 'body', 1, 'value', 'ops', 0),),
                                    'coupled_uses': ()},
 'sprite_count_step': {'function': '_append_scene_sprite_fields',
                       'paths': (('body', 25, 'body', 10, 'body', 8, 'body', 11, 'value', 'args', 3),),
                       'coupled_uses': ()},
 'sprite_palette_keep_mask': {'function': '_append_scene_sprite_fields',
                              'paths': (('body', 25, 'body', 10, 'body', 8, 'body', 14, 'value', 'right'),),
                              'coupled_uses': ()},
 'sprite_palette_shift': {'function': '_append_scene_sprite_fields',
                          'paths': (('body', 25, 'body', 10, 'body', 8, 'body', 18, 'value', 'args', 4),),
                          'coupled_uses': ()},
 'marker_origin_adjustment': {'function': 'append_scene_marker_sprite_fields',
                              'paths': (('body', 0, 'value', 'args', 4), ('body', 1, 'value', 'args', 4)),
                              'coupled_uses': ()},
 'movement_tick_mask': {'function': 'update_scripted_scene_position_fields',
                        'paths': (('body', 5, 'value', 'args', 2, 'right'), ('body', 6, 'test', 'left', 'right')),
                        'coupled_uses': ()},
 'movement_counter_step': {'function': 'update_scripted_scene_position_fields',
                           'paths': (('body', 6, 'body', 2, 'body', 1, 'value', 'args', 3),),
                           'coupled_uses': ()},
 'movement_limit_relation': {'function': 'update_scripted_scene_position_fields',
                             'paths': (('body', 6, 'body', 2, 'body', 11, 'value', 'operand', 'ops', 0),),
                             'coupled_uses': ()},
 'movement_distance_mask': {'function': 'update_scripted_scene_position_fields',
                            'paths': (('body',
                                       6,
                                       'body',
                                       2,
                                       'body',
                                       12,
                                       'body',
                                       3,
                                       'body',
                                       1,
                                       'body',
                                       1,
                                       'value',
                                       'right'),),
                            'coupled_uses': ()},
 'movement_left_bit': {'function': 'update_scripted_scene_position_fields',
                       'paths': (('body', 6, 'body', 2, 'body', 12, 'body', 3, 'iter', 'elts', 0, 'elts', 0),),
                       'coupled_uses': ()},
 'movement_right_bit': {'function': 'update_scripted_scene_position_fields',
                        'paths': (('body', 6, 'body', 2, 'body', 12, 'body', 3, 'iter', 'elts', 1, 'elts', 0),),
                        'coupled_uses': ()},
 'movement_up_bit': {'function': 'update_scripted_scene_position_fields',
                     'paths': (('body', 6, 'body', 2, 'body', 12, 'body', 3, 'iter', 'elts', 2, 'elts', 0),),
                     'coupled_uses': ()},
 'movement_down_bit': {'function': 'update_scripted_scene_position_fields',
                       'paths': (('body', 6, 'body', 2, 'body', 12, 'body', 3, 'iter', 'elts', 3, 'elts', 0),),
                       'coupled_uses': ()},
 'script_palette_longs': {'function': '_copy_scene_palette_longs_fields',
                          'paths': (('body', 2, 'value'),),
                          'coupled_uses': ()},
 'script_secondary_first_x': {'function': '_play_scripted_scene_core',
                              'paths': (('body', 8, 'body', 0, 'value', 'elts', 0), ('body', 8, 'orelse', 2, 'body', 0, 'value', 'elts', 0)),
                              'coupled_uses': ()},
 'script_secondary_first_y': {'function': '_play_scripted_scene_core',
                              'paths': (('body', 8, 'body', 0, 'value', 'elts', 1), ('body', 8, 'orelse', 2, 'body', 0, 'value', 'elts', 1)),
                              'coupled_uses': ()},
 'script_secondary_last_x': {'function': '_play_scripted_scene_core',
                             'paths': (('body', 8, 'orelse', 2, 'orelse', 0, 'value', 'elts', 0),),
                             'coupled_uses': ()},
 'script_secondary_last_y': {'function': '_play_scripted_scene_core',
                             'paths': (('body', 8, 'orelse', 2, 'orelse', 0, 'value', 'elts', 1),),
                             'coupled_uses': ()},
 'script_plane_address': {'function': '_play_scripted_scene_core',
                          'paths': (('body', 32, 'body', 0, 'value'), ('body', 45, 'body', 6, 'value', 'args', 2), ('body', 45, 'body', 7, 'value', 'args', 4)),
                          'coupled_uses': ()},
 'script_sound_command': {'function': '_play_scripted_scene_core',
                          'paths': (('body', 54, 'body', 0, 'value', 'args', 4),),
                          'coupled_uses': ()},
 'script_elapsed_step': {'function': '_play_scripted_scene_core',
                         'paths': (('body', 54, 'body', 3, 'value', 'args', 3),),
                         'coupled_uses': ()},
 'script_duration_relation': {'function': '_play_scripted_scene_core',
                              'paths': (('body', 54, 'body', 15, 'test', 'ops', 0),),
                              'coupled_uses': ()},
 'script_palette_words': {'function': '_copy_scene_palette_words_fields',
                          'paths': (('body', 1, 'value'),),
                          'coupled_uses': ()},
 'script_fixed_x': {'function': '_scene_mode_packet_parameters',
                    'paths': (('body', 0, 'orelse', 0, 'value', 'elts', 0),),
                    'coupled_uses': (('_draw_fixed_scene_pointer', ('body', 1, 'value', 'args', 2, 'args', 0)),
                                     ('_draw_scripted_staged_pair', ('body', 4, 'value', 'args', 2, 'args', 0)))},
 'script_fixed_y': {'function': '_scene_mode_packet_parameters',
                    'paths': (('body', 0, 'orelse', 0, 'value', 'elts', 1),),
                    'coupled_uses': (('_draw_fixed_scene_pointer', ('body', 1, 'value', 'args', 2, 'args', 1)),
                                     ('_draw_scripted_staged_pair', ('body', 4, 'value', 'args', 2, 'args', 1)))},
 'script_sequence_tick_mask': {'function': '_draw_scripted_sequence_fields',
                               'paths': (('body', 4, 'value', 'args', 2, 'right'),
                                         ('body', 5, 'test', 'left', 'right'),
                                         ('body', 8, 'body', 1, 'body', 2, 'value', 'args', 2, 'right'),
                                         ('body', 8, 'body', 1, 'body', 4, 'test', 'left', 'right')),
                               'coupled_uses': ()},
 'script_sequence_step': {'function': '_draw_scripted_sequence_fields',
                          'paths': (('body', 5, 'body', 0, 'value', 'args', 3),),
                          'coupled_uses': ()},
 'script_sequence_palette_frame': {'function': '_draw_scripted_sequence_fields',
                                   'paths': (('body', 8, 'body', 1, 'test', 'comparators', 0),
                                             ('body', 8, 'body', 0, 'value', 'args', 3)),
                                   'coupled_uses': ()},
 'script_sequence_palette_frame_relation': {'function': '_draw_scripted_sequence_fields',
                                            'paths': (('body', 8, 'body', 1, 'test', 'ops', 0),),
                                            'coupled_uses': ()},
 'script_sequence_palette_stop': {'function': '_draw_scripted_sequence_fields',
                                  'paths': (('body', 8, 'body', 1, 'body', 4, 'body', 2, 'test', 'comparators', 0),
                                            ('body', 8, 'body', 1, 'body', 4, 'body', 1, 'value', 'args', 3)),
                                  'coupled_uses': ()},
 'script_sequence_palette_stop_relation': {'function': '_draw_scripted_sequence_fields',
                                           'paths': (('body',
                                                      8,
                                                      'body',
                                                      1,
                                                      'body',
                                                      4,
                                                      'body',
                                                      2,
                                                      'test',
                                                      'ops',
                                                      0),),
                                           'coupled_uses': ()},
 'script_sequence_palette_step': {'function': '_draw_scripted_sequence_fields',
                                  'paths': (('body',
                                             8,
                                             'body',
                                             1,
                                             'body',
                                             4,
                                             'body',
                                             2,
                                             'orelse',
                                             0,
                                             'value',
                                             'args',
                                             3),),
                                  'coupled_uses': ()},
 'script_first_frame': {'function': '_draw_scripted_sequence_fields',
                        'paths': (('body', 10, 'body', 2, 'value', 'test', 'comparators', 0),
                                  ('body', 10, 'body', 1, 'value', 'args', 3)),
                        'coupled_uses': ()},
 'script_first_frame_relation': {'function': '_draw_scripted_sequence_fields',
                                 'paths': (('body', 10, 'body', 2, 'value', 'test', 'ops', 0),),
                                 'coupled_uses': ()},
 'script_other_frame_palette_offset': {'function': '_draw_scripted_sequence_fields',
                                       'paths': (('body', 10, 'body', 2, 'value', 'orelse'),),
                                       'coupled_uses': ()},
 'script_arrival_step': {'function': '_draw_scripted_arrival_fields',
                         'paths': (('body', 2, 'body', 0, 'value', 'args', 3),),
                         'coupled_uses': ()},
 'script_arrival_count': {'function': '_draw_scripted_arrival_fields',
                          'paths': (('body', 2, 'body', 3, 'test', 'comparators', 0),
                                    ('body', 2, 'body', 2, 'value', 'args', 3),
                                    ('body', 2, 'body', 5, 'value', 'args', 3),
                                    ('body', 2, 'body', 6, 'test', 'comparators', 0)),
                          'coupled_uses': ()},
 'script_arrival_equal_relation': {'function': '_draw_scripted_arrival_fields',
                                   'paths': (('body', 2, 'body', 3, 'test', 'ops', 0),),
                                   'coupled_uses': ()},
 'script_arrival_past_relation': {'function': '_draw_scripted_arrival_fields',
                                  'paths': (('body', 2, 'body', 6, 'test', 'ops', 0),),
                                  'coupled_uses': ()},
 'script_arrival_position_bound': {'function': '_draw_scripted_arrival_fields',
                                   'paths': (('body', 2, 'body', 15, 'test', 'comparators', 0),
                                             ('body', 2, 'body', 14, 'value', 'args', 3)),
                                   'coupled_uses': ()},
 'script_arrival_position_relation': {'function': '_draw_scripted_arrival_fields',
                                      'paths': (('body', 2, 'body', 15, 'test', 'ops', 0),),
                                      'coupled_uses': ()},
 'script_arrival_tick_mask': {'function': '_draw_scripted_arrival_fields',
                              'paths': (('body', 2, 'body', 15, 'body', 2, 'value', 'args', 2, 'right'),
                                        ('body', 2, 'body', 15, 'body', 3, 'test', 'left', 'right')),
                              'coupled_uses': ()},
 'script_arrival_position_step': {'function': '_draw_scripted_arrival_fields',
                                  'paths': (('body', 2, 'body', 15, 'body', 3, 'body', 0, 'value', 'args', 3),),
                                  'coupled_uses': ()},
 'script_landing_y': {'function': '_draw_scripted_landing_fields',
                      'paths': (('body', 8, 'test', 'comparators', 0), ('body', 7, 'value', 'args', 3)),
                      'coupled_uses': ()},
 'script_landing_y_relation': {'function': '_draw_scripted_landing_fields',
                               'paths': (('body', 8, 'test', 'ops', 0),),
                               'coupled_uses': ()},
 'script_landing_palette_stop': {'function': '_draw_scripted_landing_fields',
                                 'paths': (('body', 11, 'test', 'comparators', 0),
                                           ('body', 10, 'value', 'args', 3)),
                                 'coupled_uses': ()},
 'script_landing_palette_relation': {'function': '_draw_scripted_landing_fields',
                                     'paths': (('body', 11, 'test', 'ops', 0),),
                                     'coupled_uses': ()},
 'script_landing_tick_mask': {'function': '_draw_scripted_landing_fields',
                              'paths': (('body', 11, 'body', 2, 'value', 'args', 2, 'right'),
                                        ('body', 11, 'body', 3, 'test', 'left', 'right')),
                              'coupled_uses': ()},
 'script_landing_palette_step': {'function': '_draw_scripted_landing_fields',
                                 'paths': (('body', 11, 'body', 3, 'body', 0, 'value', 'args', 3),),
                                 'coupled_uses': ()},
 'script_wave_step': {'function': '_draw_scripted_wave_fields',
                      'paths': (('body', 7, 'value', 'args', 3),
                                ('body', 15, 'orelse', 0, 'value', 'args', 3),
                                ('body', 15, 'body', 0, 'value', 'args', 3)),
                      'coupled_uses': ()},
 'script_wave_y': {'function': '_draw_scripted_wave_fields',
                   'paths': (('body', 11, 'value', 'args', 4),),
                   'coupled_uses': ()},
 'script_wave_tick_mask': {'function': '_draw_scripted_wave_fields',
                           'paths': (('body', 14, 'value', 'args', 2, 'right'), ('body', 15, 'test', 'right')),
                           'coupled_uses': ()},
 'script_wave_terminator': {'function': '_draw_scripted_wave_fields',
                            'paths': (('body', 15, 'orelse', 7, 'test', 'comparators', 0),
                                      ('body', 15, 'orelse', 6, 'value', 'args', 3)),
                            'coupled_uses': ()},
 'script_wave_delay': {'function': '_draw_scripted_wave_fields',
                       'paths': (('body', 22, 'test', 'comparators', 0), ('body', 21, 'value', 'args', 3)),
                       'coupled_uses': ()},
 'script_wave_delay_relation': {'function': '_draw_scripted_wave_fields',
                                'paths': (('body', 22, 'test', 'ops', 0),),
                                'coupled_uses': ()},
 'script_wave_palette_stop': {'function': '_draw_scripted_wave_fields',
                              'paths': (('body', 25, 'test', 'comparators', 0), ('body', 24, 'value', 'args', 3)),
                              'coupled_uses': ()},
 'script_wave_palette_relation': {'function': '_draw_scripted_wave_fields',
                                  'paths': (('body', 25, 'test', 'ops', 0),),
                                  'coupled_uses': ()},
 'script_wave_palette_tick_mask': {'function': '_draw_scripted_wave_fields',
                                   'paths': (('body', 25, 'body', 2, 'value', 'args', 2, 'right'),
                                             ('body', 25, 'body', 3, 'test', 'left', 'right')),
                                   'coupled_uses': ()},
 'script_wave_palette_step': {'function': '_draw_scripted_wave_fields',
                              'paths': (('body', 25, 'body', 3, 'body', 0, 'value', 'args', 3),),
                              'coupled_uses': ()},
 'script_late_delay': {'function': '_draw_scripted_late_palette_fields',
                       'paths': (('body', 9, 'test', 'comparators', 0), ('body', 8, 'value', 'args', 3)),
                       'coupled_uses': ()},
 'script_late_delay_relation': {'function': '_draw_scripted_late_palette_fields',
                                'paths': (('body', 9, 'test', 'ops', 0),),
                                'coupled_uses': ()},
 'script_late_palette_stop': {'function': '_draw_scripted_late_palette_fields',
                              'paths': (('body', 12, 'test', 'comparators', 0), ('body', 11, 'value', 'args', 3)),
                              'coupled_uses': ()},
 'script_late_palette_relation': {'function': '_draw_scripted_late_palette_fields',
                                  'paths': (('body', 12, 'test', 'ops', 0),),
                                  'coupled_uses': ()},
 'script_late_tick_mask': {'function': '_draw_scripted_late_palette_fields',
                           'paths': (('body', 12, 'body', 2, 'value', 'args', 2, 'right'),
                                     ('body', 12, 'body', 3, 'test', 'left', 'right')),
                           'coupled_uses': ()},
 'script_late_palette_step': {'function': '_draw_scripted_late_palette_fields',
                              'paths': (('body', 12, 'body', 3, 'body', 0, 'value', 'args', 3),),
                              'coupled_uses': ()},
 'script_three_frame_step': {'function': '_draw_scripted_three_frame_stage_fields',
                             'paths': (('body', 2, 'value', 'args', 3),),
                             'coupled_uses': ()},
 'script_three_frame_duration': {'function': '_draw_scripted_three_frame_stage_fields',
                                 'paths': (('body', 5, 'test', 'comparators', 0), ('body', 4, 'value', 'args', 3)),
                                 'coupled_uses': ()},
 'script_three_frame_duration_relation': {'function': '_draw_scripted_three_frame_stage_fields',
                                          'paths': (('body', 5, 'test', 'ops', 0),),
                                          'coupled_uses': ()},
 'script_three_frame_tick_bit': {'function': '_draw_scripted_three_frame_stage_fields',
                                 'paths': (('body', 5, 'body', 3, 'test', 'operand', 'right'),
                                           ('body', 5, 'body', 2, 'value', 'args', 3)),
                                 'coupled_uses': ()},
 'script_three_frame_index_bound': {'function': '_draw_scripted_three_frame_stage_fields',
                                    'paths': (('body', 5, 'body', 3, 'body', 2, 'test', 'comparators', 0),
                                              ('body', 5, 'body', 3, 'body', 1, 'value', 'args', 3)),
                                    'coupled_uses': ()},
 'script_three_frame_index_relation': {'function': '_draw_scripted_three_frame_stage_fields',
                                       'paths': (('body', 5, 'body', 3, 'body', 2, 'test', 'ops', 0),),
                                       'coupled_uses': ()},
 'script_three_frame_index_step': {'function': '_draw_scripted_three_frame_stage_fields',
                                   'paths': (('body', 5, 'body', 3, 'body', 2, 'orelse', 0, 'value', 'args', 3),),
                                   'coupled_uses': ()},
 'script_high_first_shift': {'function': '_draw_scripted_high_mode_fields',
                             'paths': (('body', 6, 'body', 3, 'value', 'left', 'right'),
                                       ('body', 6, 'body', 2, 'value', 'args', 4)),
                             'coupled_uses': ()},
 'script_high_first_mask': {'function': '_draw_scripted_high_mode_fields',
                            'paths': (('body', 6, 'body', 3, 'value', 'right'),),
                            'coupled_uses': ()},
 'script_high_second_shift': {'function': '_draw_scripted_high_mode_fields',
                              'paths': (('body', 6, 'orelse', 1, 'body', 3, 'value', 'left', 'right'),
                                        ('body', 6, 'orelse', 1, 'body', 2, 'value', 'args', 4)),
                              'coupled_uses': ()},
 'script_high_second_mask': {'function': '_draw_scripted_high_mode_fields',
                             'paths': (('body', 6, 'orelse', 1, 'body', 3, 'value', 'right'),),
                             'coupled_uses': ()}}
ROLE_SPECS = tuple(MenuRole(role.name, _CLOSED_MODE_ROLE_PATHS[role.name]['function'],
    _CLOSED_MODE_ROLE_PATHS[role.name]['paths'], role.kind, role.default, role.physical_pcs,
    coupled_uses=_CLOSED_MODE_ROLE_PATHS[role.name]['coupled_uses']) if role.name in _CLOSED_MODE_ROLE_PATHS else role
    for role in ROLE_SPECS)

# B22 every actual player mode and standalone latch/selector role is sole fields.
_PAIR_MODE_ROLE_PATHS = {'word_stream_marker_relation': {'function': 'write_vdp_word_rle_stream_fields',
                                 'paths': (('body', 7, 'body', 4, 'test', 'ops', 0),),
                                 'coupled_uses': ()},
 'scene_chain_nonempty_relation': {'function': 'finish_one_scene_sprite_chain_fields',
                                   'paths': (('body', 4, 'test', 'ops', 0),),
                                   'coupled_uses': (('finish_one_actor_sprite_chain',
                                                     ('body', 5, 'test', 'ops', 0)),)},
 'sprite_capacity': {'function': '_append_scene_sprite_fields',
                     'paths': (('body', 6, 'test', 'comparators', 0),
                               ('body', 25, 'body', 14, 'test', 'comparators', 0),
                               ('body', 5, 'value', 'args', 3),
                               ('body', 25, 'body', 13, 'value', 'args', 3)),
                     'coupled_uses': ()},
 'sprite_capacity_relation': {'function': '_append_scene_sprite_fields',
                              'paths': (('body', 6, 'test', 'ops', 0), ('body', 25, 'body', 14, 'test', 'ops', 0)),
                              'coupled_uses': ()},
 'sprite_origin': {'function': '_append_scene_sprite_fields',
                   'paths': (('body', 13, 'value', 'args', 4), ('body', 17, 'value', 'args', 4)),
                   'coupled_uses': ()},
 'sprite_flip_adjustment': {'function': '_append_scene_sprite_fields',
                            'paths': (('body', 16, 'body', 0, 'value', 'args', 4),
                                      ('body', 19, 'body', 0, 'value', 'args', 4)),
                            'coupled_uses': ()},
 'sprite_horizontal_flip_bit': {'function': '_append_scene_sprite_fields',
                                'paths': (('body', 16, 'test', 'right'),
                                          ('body', 15, 'value', 'args', 3),
                                          ('body', 25, 'body', 10, 'body', 1, 'value', 'args', 2)),
                                'coupled_uses': ()},
 'sprite_vertical_flip_bit': {'function': '_append_scene_sprite_fields',
                              'paths': (('body', 19, 'test', 'right'),
                                        ('body', 18, 'value', 'args', 3),
                                        ('body', 25, 'body', 10, 'body', 8, 'body', 1, 'value', 'args', 2)),
                              'coupled_uses': ()},
 'sprite_clip_minimum': {'function': '_scene_render_clip_axis',
                         'paths': (('body', 9, 'value', 'comparators', 0), ('body', 8, 'value', 'args', 3)),
                         'coupled_uses': ()},
 'sprite_clip_minimum_relation': {'function': '_scene_render_clip_axis',
                                  'paths': (('body', 9, 'value', 'ops', 0),),
                                  'coupled_uses': ()},
 'sprite_clip_x_maximum': {'function': '_append_scene_sprite_fields',
                           'paths': (('body', 25, 'body', 9, 'body', 0, 'value', 'args', 3),),
                           'coupled_uses': ()},
 'sprite_clip_y_maximum': {'function': '_append_scene_sprite_fields',
                           'paths': (('body', 25, 'body', 10, 'body', 7, 'body', 2, 'value', 'args', 3),),
                           'coupled_uses': ()},
 'sprite_clip_x_maximum_relation': {'function': '_scene_render_clip_axis',
                                    'paths': (('body', 10, 'body', 1, 'value', 'ops', 0),),
                                    'coupled_uses': ()},
 'sprite_clip_y_maximum_relation': {'function': '_scene_render_clip_axis',
                                    'paths': (('body', 10, 'body', 1, 'value', 'ops', 0),),
                                    'coupled_uses': ()},
 'sprite_count_step': {'function': '_append_scene_sprite_fields',
                       'paths': (('body', 25, 'body', 10, 'body', 8, 'body', 11, 'value', 'args', 3),),
                       'coupled_uses': ()},
 'sprite_palette_keep_mask': {'function': '_append_scene_sprite_fields',
                              'paths': (('body', 25, 'body', 10, 'body', 8, 'body', 14, 'value', 'right'),),
                              'coupled_uses': ()},
 'sprite_palette_shift': {'function': '_append_scene_sprite_fields',
                          'paths': (('body', 25, 'body', 10, 'body', 8, 'body', 18, 'value', 'args', 4),),
                          'coupled_uses': ()},
 'marker_origin_adjustment': {'function': 'append_scene_marker_sprite_fields',
                              'paths': (('body', 0, 'value', 'args', 4), ('body', 1, 'value', 'args', 4)),
                              'coupled_uses': ()},
 'movement_tick_mask': {'function': 'update_scripted_scene_position_fields',
                        'paths': (('body', 5, 'value', 'args', 2, 'right'), ('body', 6, 'test', 'left', 'right')),
                        'coupled_uses': ()},
 'movement_counter_step': {'function': 'update_scripted_scene_position_fields',
                           'paths': (('body', 6, 'body', 2, 'body', 1, 'value', 'args', 3),),
                           'coupled_uses': ()},
 'movement_limit_relation': {'function': 'update_scripted_scene_position_fields',
                             'paths': (('body', 6, 'body', 2, 'body', 11, 'value', 'operand', 'ops', 0),),
                             'coupled_uses': ()},
 'movement_distance_mask': {'function': 'update_scripted_scene_position_fields',
                            'paths': (('body',
                                       6,
                                       'body',
                                       2,
                                       'body',
                                       12,
                                       'body',
                                       3,
                                       'body',
                                       1,
                                       'body',
                                       1,
                                       'value',
                                       'right'),),
                            'coupled_uses': ()},
 'movement_left_bit': {'function': 'update_scripted_scene_position_fields',
                       'paths': (('body', 6, 'body', 2, 'body', 12, 'body', 3, 'iter', 'elts', 0, 'elts', 0),),
                       'coupled_uses': ()},
 'movement_right_bit': {'function': 'update_scripted_scene_position_fields',
                        'paths': (('body', 6, 'body', 2, 'body', 12, 'body', 3, 'iter', 'elts', 1, 'elts', 0),),
                        'coupled_uses': ()},
 'movement_up_bit': {'function': 'update_scripted_scene_position_fields',
                     'paths': (('body', 6, 'body', 2, 'body', 12, 'body', 3, 'iter', 'elts', 2, 'elts', 0),),
                     'coupled_uses': ()},
 'movement_down_bit': {'function': 'update_scripted_scene_position_fields',
                       'paths': (('body', 6, 'body', 2, 'body', 12, 'body', 3, 'iter', 'elts', 3, 'elts', 0),),
                       'coupled_uses': ()},
 'script_palette_longs': {'function': '_copy_scene_palette_longs_fields',
                          'paths': (('body', 2, 'value'),),
                          'coupled_uses': ()},
 'script_secondary_first_x': {'function': '_play_scripted_scene_core',
                              'paths': (('body', 9, 'body', 0, 'value', 'elts', 0), ('body', 9, 'orelse', 2, 'body', 0, 'value', 'elts', 0)),
                              'coupled_uses': ()},
 'script_secondary_first_y': {'function': '_play_scripted_scene_core',
                              'paths': (('body', 9, 'body', 0, 'value', 'elts', 1), ('body', 9, 'orelse', 2, 'body', 0, 'value', 'elts', 1)),
                              'coupled_uses': ()},
 'script_secondary_last_x': {'function': '_play_scripted_scene_core',
                             'paths': (('body', 9, 'orelse', 2, 'orelse', 0, 'value', 'elts', 0),),
                             'coupled_uses': ()},
 'script_secondary_last_y': {'function': '_play_scripted_scene_core',
                             'paths': (('body', 9, 'orelse', 2, 'orelse', 0, 'value', 'elts', 1),),
                             'coupled_uses': ()},
 'script_plane_address': {'function': '_play_scripted_scene_core',
                          'paths': (('body', 33, 'body', 0, 'value'), ('body', 46, 'body', 6, 'value', 'args', 2), ('body', 46, 'body', 7, 'value', 'args', 4)),
                          'coupled_uses': ()},
 'script_sound_command': {'function': '_play_scripted_scene_core',
                          'paths': (('body', 55, 'body', 0, 'value', 'args', 4),),
                          'coupled_uses': ()},
 'script_elapsed_step': {'function': '_play_scripted_scene_core',
                         'paths': (('body', 55, 'body', 3, 'value', 'args', 3),),
                         'coupled_uses': ()},
 'script_duration_relation': {'function': '_play_scripted_scene_core',
                              'paths': (('body', 55, 'body', 15, 'test', 'ops', 0),),
                              'coupled_uses': ()},
 'script_palette_words': {'function': '_copy_scene_palette_words_fields',
                          'paths': (('body', 1, 'value'),),
                          'coupled_uses': ()},
 'script_fixed_x': {'function': '_scene_mode_packet_parameters',
                    'paths': (('body', 0, 'orelse', 0, 'value', 'elts', 0),),
                    'coupled_uses': ()},
 'script_fixed_y': {'function': '_scene_mode_packet_parameters',
                    'paths': (('body', 0, 'orelse', 0, 'value', 'elts', 1),),
                    'coupled_uses': ()},
 'script_sequence_tick_mask': {'function': '_draw_scripted_sequence_fields',
                               'paths': (('body', 4, 'value', 'args', 2, 'right'),
                                         ('body', 5, 'test', 'left', 'right'),
                                         ('body', 8, 'body', 1, 'body', 2, 'value', 'args', 2, 'right'),
                                         ('body', 8, 'body', 1, 'body', 4, 'test', 'left', 'right')),
                               'coupled_uses': ()},
 'script_sequence_step': {'function': '_draw_scripted_sequence_fields',
                          'paths': (('body', 5, 'body', 0, 'value', 'args', 3),),
                          'coupled_uses': ()},
 'script_sequence_palette_frame': {'function': '_draw_scripted_sequence_fields',
                                   'paths': (('body', 8, 'body', 1, 'test', 'comparators', 0),
                                             ('body', 8, 'body', 0, 'value', 'args', 3)),
                                   'coupled_uses': ()},
 'script_sequence_palette_frame_relation': {'function': '_draw_scripted_sequence_fields',
                                            'paths': (('body', 8, 'body', 1, 'test', 'ops', 0),),
                                            'coupled_uses': ()},
 'script_sequence_palette_stop': {'function': '_draw_scripted_sequence_fields',
                                  'paths': (('body', 8, 'body', 1, 'body', 4, 'body', 2, 'test', 'comparators', 0),
                                            ('body', 8, 'body', 1, 'body', 4, 'body', 1, 'value', 'args', 3)),
                                  'coupled_uses': ()},
 'script_sequence_palette_stop_relation': {'function': '_draw_scripted_sequence_fields',
                                           'paths': (('body',
                                                      8,
                                                      'body',
                                                      1,
                                                      'body',
                                                      4,
                                                      'body',
                                                      2,
                                                      'test',
                                                      'ops',
                                                      0),),
                                           'coupled_uses': ()},
 'script_sequence_palette_step': {'function': '_draw_scripted_sequence_fields',
                                  'paths': (('body',
                                             8,
                                             'body',
                                             1,
                                             'body',
                                             4,
                                             'body',
                                             2,
                                             'orelse',
                                             0,
                                             'value',
                                             'args',
                                             3),),
                                  'coupled_uses': ()},
 'script_first_frame': {'function': '_draw_scripted_sequence_fields',
                        'paths': (('body', 10, 'body', 2, 'value', 'test', 'comparators', 0),
                                  ('body', 10, 'body', 1, 'value', 'args', 3)),
                        'coupled_uses': ()},
 'script_first_frame_relation': {'function': '_draw_scripted_sequence_fields',
                                 'paths': (('body', 10, 'body', 2, 'value', 'test', 'ops', 0),),
                                 'coupled_uses': ()},
 'script_other_frame_palette_offset': {'function': '_draw_scripted_sequence_fields',
                                       'paths': (('body', 10, 'body', 2, 'value', 'orelse'),),
                                       'coupled_uses': ()},
 'script_arrival_step': {'function': '_draw_scripted_arrival_fields',
                         'paths': (('body', 2, 'body', 0, 'value', 'args', 3),),
                         'coupled_uses': ()},
 'script_arrival_count': {'function': '_draw_scripted_arrival_fields',
                          'paths': (('body', 2, 'body', 3, 'test', 'comparators', 0),
                                    ('body', 2, 'body', 2, 'value', 'args', 3),
                                    ('body', 2, 'body', 5, 'value', 'args', 3),
                                    ('body', 2, 'body', 6, 'test', 'comparators', 0)),
                          'coupled_uses': ()},
 'script_arrival_equal_relation': {'function': '_draw_scripted_arrival_fields',
                                   'paths': (('body', 2, 'body', 3, 'test', 'ops', 0),),
                                   'coupled_uses': ()},
 'script_arrival_past_relation': {'function': '_draw_scripted_arrival_fields',
                                  'paths': (('body', 2, 'body', 6, 'test', 'ops', 0),),
                                  'coupled_uses': ()},
 'script_arrival_position_bound': {'function': '_draw_scripted_arrival_fields',
                                   'paths': (('body', 2, 'body', 15, 'test', 'comparators', 0),
                                             ('body', 2, 'body', 14, 'value', 'args', 3)),
                                   'coupled_uses': ()},
 'script_arrival_position_relation': {'function': '_draw_scripted_arrival_fields',
                                      'paths': (('body', 2, 'body', 15, 'test', 'ops', 0),),
                                      'coupled_uses': ()},
 'script_arrival_tick_mask': {'function': '_draw_scripted_arrival_fields',
                              'paths': (('body', 2, 'body', 15, 'body', 2, 'value', 'args', 2, 'right'),
                                        ('body', 2, 'body', 15, 'body', 3, 'test', 'left', 'right')),
                              'coupled_uses': ()},
 'script_arrival_position_step': {'function': '_draw_scripted_arrival_fields',
                                  'paths': (('body', 2, 'body', 15, 'body', 3, 'body', 0, 'value', 'args', 3),),
                                  'coupled_uses': ()},
 'script_landing_y': {'function': '_draw_scripted_landing_fields',
                      'paths': (('body', 8, 'test', 'comparators', 0), ('body', 7, 'value', 'args', 3)),
                      'coupled_uses': ()},
 'script_landing_y_relation': {'function': '_draw_scripted_landing_fields',
                               'paths': (('body', 8, 'test', 'ops', 0),),
                               'coupled_uses': ()},
 'script_landing_palette_stop': {'function': '_draw_scripted_landing_fields',
                                 'paths': (('body', 11, 'test', 'comparators', 0),
                                           ('body', 10, 'value', 'args', 3)),
                                 'coupled_uses': ()},
 'script_landing_palette_relation': {'function': '_draw_scripted_landing_fields',
                                     'paths': (('body', 11, 'test', 'ops', 0),),
                                     'coupled_uses': ()},
 'script_landing_tick_mask': {'function': '_draw_scripted_landing_fields',
                              'paths': (('body', 11, 'body', 2, 'value', 'args', 2, 'right'),
                                        ('body', 11, 'body', 3, 'test', 'left', 'right')),
                              'coupled_uses': ()},
 'script_landing_palette_step': {'function': '_draw_scripted_landing_fields',
                                 'paths': (('body', 11, 'body', 3, 'body', 0, 'value', 'args', 3),),
                                 'coupled_uses': ()},
 'script_wave_step': {'function': '_draw_scripted_wave_fields',
                      'paths': (('body', 7, 'value', 'args', 3),
                                ('body', 15, 'orelse', 0, 'value', 'args', 3),
                                ('body', 15, 'body', 0, 'value', 'args', 3)),
                      'coupled_uses': ()},
 'script_wave_y': {'function': '_draw_scripted_wave_fields',
                   'paths': (('body', 11, 'value', 'args', 4),),
                   'coupled_uses': ()},
 'script_wave_tick_mask': {'function': '_draw_scripted_wave_fields',
                           'paths': (('body', 14, 'value', 'args', 2, 'right'), ('body', 15, 'test', 'right')),
                           'coupled_uses': ()},
 'script_wave_terminator': {'function': '_draw_scripted_wave_fields',
                            'paths': (('body', 15, 'orelse', 7, 'test', 'comparators', 0),
                                      ('body', 15, 'orelse', 6, 'value', 'args', 3)),
                            'coupled_uses': ()},
 'script_wave_delay': {'function': '_draw_scripted_wave_fields',
                       'paths': (('body', 22, 'test', 'comparators', 0), ('body', 21, 'value', 'args', 3)),
                       'coupled_uses': ()},
 'script_wave_delay_relation': {'function': '_draw_scripted_wave_fields',
                                'paths': (('body', 22, 'test', 'ops', 0),),
                                'coupled_uses': ()},
 'script_wave_palette_stop': {'function': '_draw_scripted_wave_fields',
                              'paths': (('body', 25, 'test', 'comparators', 0), ('body', 24, 'value', 'args', 3)),
                              'coupled_uses': ()},
 'script_wave_palette_relation': {'function': '_draw_scripted_wave_fields',
                                  'paths': (('body', 25, 'test', 'ops', 0),),
                                  'coupled_uses': ()},
 'script_wave_palette_tick_mask': {'function': '_draw_scripted_wave_fields',
                                   'paths': (('body', 25, 'body', 2, 'value', 'args', 2, 'right'),
                                             ('body', 25, 'body', 3, 'test', 'left', 'right')),
                                   'coupled_uses': ()},
 'script_wave_palette_step': {'function': '_draw_scripted_wave_fields',
                              'paths': (('body', 25, 'body', 3, 'body', 0, 'value', 'args', 3),),
                              'coupled_uses': ()},
 'script_late_delay': {'function': '_draw_scripted_late_palette_fields',
                       'paths': (('body', 9, 'test', 'comparators', 0), ('body', 8, 'value', 'args', 3)),
                       'coupled_uses': ()},
 'script_late_delay_relation': {'function': '_draw_scripted_late_palette_fields',
                                'paths': (('body', 9, 'test', 'ops', 0),),
                                'coupled_uses': ()},
 'script_late_palette_stop': {'function': '_draw_scripted_late_palette_fields',
                              'paths': (('body', 12, 'test', 'comparators', 0), ('body', 11, 'value', 'args', 3)),
                              'coupled_uses': ()},
 'script_late_palette_relation': {'function': '_draw_scripted_late_palette_fields',
                                  'paths': (('body', 12, 'test', 'ops', 0),),
                                  'coupled_uses': ()},
 'script_late_tick_mask': {'function': '_draw_scripted_late_palette_fields',
                           'paths': (('body', 12, 'body', 2, 'value', 'args', 2, 'right'),
                                     ('body', 12, 'body', 3, 'test', 'left', 'right')),
                           'coupled_uses': ()},
 'script_late_palette_step': {'function': '_draw_scripted_late_palette_fields',
                              'paths': (('body', 12, 'body', 3, 'body', 0, 'value', 'args', 3),),
                              'coupled_uses': ()},
 'script_three_frame_step': {'function': '_draw_scripted_three_frame_stage_fields',
                             'paths': (('body', 2, 'value', 'args', 3),),
                             'coupled_uses': ()},
 'script_three_frame_duration': {'function': '_draw_scripted_three_frame_stage_fields',
                                 'paths': (('body', 5, 'test', 'comparators', 0), ('body', 4, 'value', 'args', 3)),
                                 'coupled_uses': ()},
 'script_three_frame_duration_relation': {'function': '_draw_scripted_three_frame_stage_fields',
                                          'paths': (('body', 5, 'test', 'ops', 0),),
                                          'coupled_uses': ()},
 'script_three_frame_tick_bit': {'function': '_draw_scripted_three_frame_stage_fields',
                                 'paths': (('body', 5, 'body', 3, 'test', 'operand', 'right'),
                                           ('body', 5, 'body', 2, 'value', 'args', 3)),
                                 'coupled_uses': ()},
 'script_three_frame_index_bound': {'function': '_draw_scripted_three_frame_stage_fields',
                                    'paths': (('body', 5, 'body', 3, 'body', 2, 'test', 'comparators', 0),
                                              ('body', 5, 'body', 3, 'body', 1, 'value', 'args', 3)),
                                    'coupled_uses': ()},
 'script_three_frame_index_relation': {'function': '_draw_scripted_three_frame_stage_fields',
                                       'paths': (('body', 5, 'body', 3, 'body', 2, 'test', 'ops', 0),),
                                       'coupled_uses': ()},
 'script_three_frame_index_step': {'function': '_draw_scripted_three_frame_stage_fields',
                                   'paths': (('body', 5, 'body', 3, 'body', 2, 'orelse', 0, 'value', 'args', 3),),
                                   'coupled_uses': ()},
 'script_high_first_shift': {'function': '_draw_scripted_high_mode_fields',
                             'paths': (('body', 6, 'body', 3, 'value', 'left', 'right'),
                                       ('body', 6, 'body', 2, 'value', 'args', 4)),
                             'coupled_uses': ()},
 'script_high_first_mask': {'function': '_draw_scripted_high_mode_fields',
                            'paths': (('body', 6, 'body', 3, 'value', 'right'),),
                            'coupled_uses': ()},
 'script_high_second_shift': {'function': '_draw_scripted_high_mode_fields',
                              'paths': (('body', 6, 'orelse', 1, 'body', 3, 'value', 'left', 'right'),
                                        ('body', 6, 'orelse', 1, 'body', 2, 'value', 'args', 4)),
                              'coupled_uses': ()},
 'script_high_second_mask': {'function': '_draw_scripted_high_mode_fields',
                             'paths': (('body', 6, 'orelse', 1, 'body', 3, 'value', 'right'),),
                             'coupled_uses': ()},
 'secondary_latched_relation': {'function': 'initialize_scripted_secondary_position_fields',
                                'paths': (('body', 3, 'test', 'ops', 0),),
                                'coupled_uses': ()},
 'secondary_latch_value': {'function': 'initialize_scripted_secondary_position_fields',
                           'paths': (('body', 15, 'value', 'args', 4),),
                           'coupled_uses': ()},
 'frame_direct_mode_bound': {'function': 'select_scene_object_frame_fields',
                             'paths': (('body', 3, 'test', 'comparators', 0), ('body', 2, 'value', 'args', 2)),
                             'coupled_uses': ()},
 'frame_direct_mode_relation': {'function': 'select_scene_object_frame_fields',
                                'paths': (('body', 3, 'test', 'ops', 0),),
                                'coupled_uses': ()},
 'frame_sequence_bound': {'function': 'select_scene_object_frame_fields',
                          'paths': (('body', 6, 'test', 'comparators', 0), ('body', 5, 'value', 'args', 3)),
                          'coupled_uses': ()},
 'frame_sequence_relation': {'function': 'select_scene_object_frame_fields',
                             'paths': (('body', 6, 'test', 'ops', 0),),
                             'coupled_uses': ()},
 'frame_sequence_tick_mask': {'function': 'select_scene_object_frame_fields',
                              'paths': (('body', 6, 'body', 4, 'value', 'args', 2, 'right'),
                                        ('body', 6, 'body', 5, 'test', 'left', 'right')),
                              'coupled_uses': ()},
 'frame_sequence_step': {'function': 'select_scene_object_frame_fields',
                         'paths': (('body', 6, 'body', 5, 'body', 0, 'value', 'args', 3),),
                         'coupled_uses': ()},
 'frame_sequence_terminator': {'function': 'select_scene_object_frame_fields',
                               'paths': (('body', 6, 'body', 10, 'test', 'comparators', 0),
                                         ('body', 6, 'body', 9, 'value', 'args', 3)),
                               'coupled_uses': ()},
 'frame_lookup_keep_mask': {'function': 'select_scene_object_frame_fields',
                            'paths': (('body', 6, 'body', 11, 'value', 'args', 2, 'right'),),
                            'coupled_uses': ()},
 'script_staged_counter_step': {'function': '_draw_scripted_staged_pair_fields',
                                'paths': (('body', 2, 'value', 'args', 3),),
                                'coupled_uses': ()},
 'script_staged_animation_bit': {'function': '_draw_scripted_staged_pair_fields',
                                 'paths': (('body', 6, 'value', 'test', 'right'), ('body', 5, 'value', 'args', 3)),
                                 'coupled_uses': ()},
 'script_staged_first_delay': {'function': '_draw_scripted_staged_pair_fields',
                               'paths': (('body', 13, 'test', 'comparators', 0), ('body', 12, 'value', 'args', 3)),
                               'coupled_uses': ()},
 'script_staged_first_delay_relation': {'function': '_draw_scripted_staged_pair_fields',
                                        'paths': (('body', 13, 'test', 'ops', 0),),
                                        'coupled_uses': ()},
 'script_staged_second_delay': {'function': '_draw_scripted_staged_pair_fields',
                                'paths': (('body', 21, 'test', 'comparators', 0),
                                          ('body', 20, 'value', 'args', 3)),
                                'coupled_uses': ()},
 'script_staged_second_delay_relation': {'function': '_draw_scripted_staged_pair_fields',
                                         'paths': (('body', 21, 'test', 'ops', 0),),
                                         'coupled_uses': ()}}
ROLE_SPECS = tuple(MenuRole(role.name, _PAIR_MODE_ROLE_PATHS[role.name]['function'],
    _PAIR_MODE_ROLE_PATHS[role.name]['paths'], role.kind, role.default, role.physical_pcs,
    coupled_uses=_PAIR_MODE_ROLE_PATHS[role.name]['coupled_uses']) if role.name in _PAIR_MODE_ROLE_PATHS else role
    for role in ROLE_SPECS)

# B23 glyph roles point only at the sole full-field algorithm.
_GLYPH_FIELD_ROLE_PATHS = {'glyph_row_longs': {'function': 'decode_glyph_rows_to_buffers_fields',
                     'paths': (('body', 5, 'value'),),
                     'coupled_uses': ()},
 'glyph_fill_nibbles': {'function': 'decode_glyph_rows_to_buffers_fields',
                        'paths': (('body', 6, 'body', 3, 'orelse', 2, 'value'),),
                        'coupled_uses': ()},
 'glyph_fill_nibble_shift': {'function': 'decode_glyph_rows_to_buffers_fields',
                             'paths': (('body', 6, 'body', 3, 'orelse', 4, 'body', 0, 'value', 'args', 3),
                                       ('body', 6, 'body', 3, 'orelse', 4, 'body', 1, 'value', 'args', 3)),
                             'coupled_uses': ()}}
ROLE_SPECS = tuple(MenuRole(role.name,_GLYPH_FIELD_ROLE_PATHS[role.name]['function'],
    _GLYPH_FIELD_ROLE_PATHS[role.name]['paths'],role.kind,role.default,role.physical_pcs,
    coupled_uses=_GLYPH_FIELD_ROLE_PATHS[role.name]['coupled_uses']) if role.name in _GLYPH_FIELD_ROLE_PATHS else role
    for role in ROLE_SPECS)

# B26 exact packet wrap role follows the one real WORD spill algorithm.
_PACKET_FIELD_ROLE_PATHS = {'function': '_vdp_packet_spill_fields',
 'paths': (('body', 7, 'value', 'args', 4), ('body', 8, 'test', 'comparators', 0))}
ROLE_SPECS = tuple(MenuRole(role.name,_PACKET_FIELD_ROLE_PATHS['function'],
    _PACKET_FIELD_ROLE_PATHS['paths'],role.kind,role.default,role.physical_pcs,coupled_uses=())
    if role.name == 'packet_wrap_width' else role for role in ROLE_SPECS)

# B29 tile/plane roles observe only the sole actual field kernels.
_TILE_PLANE_FIELD_ROLE_PATHS = {'swapped_stream_marker_relation': {'function': '_write_vdp_swapped_byte_rle_fields_core',
                                    'paths': (('body', 6, 'body', 2, 'test', 'ops', 0),),
                                    'coupled_uses': ()},
 'plane_stream_marker_relation': {'function': '_read_vdp_plane_rle_rows_fields_core',
                                  'paths': (('body', 15, 'body', 6, 'value', 'values', 1, 'ops', 0),),
                                  'coupled_uses': ()},
 'plane_column_step': {'function': 'advance_plane_row_fields',
                       'paths': (('body', 2, 'value', 'args', 4),),
                       'coupled_uses': ()},
 'plane_column_bound': {'function': 'advance_plane_row_fields',
                        'paths': (('body', 5, 'test', 'comparators', 0), ('body', 4, 'value', 'args', 3)),
                        'coupled_uses': ()},
 'plane_column_end_relation': {'function': 'advance_plane_row_fields',
                               'paths': (('body', 5, 'test', 'ops', 0),),
                               'coupled_uses': ()},
 'plane_row_step': {'function': 'advance_plane_row_fields',
                    'paths': (('body', 5, 'body', 0, 'value', 'args', 4),),
                    'coupled_uses': ()},
 'plane_initial_rows': {'function': '_read_vdp_plane_rle_rows_fields_core',
                        'paths': (('body', 3, 'body', 2, 'value', 'args', 2),),
                        'coupled_uses': ()}}
ROLE_SPECS = tuple(MenuRole(role.name,_TILE_PLANE_FIELD_ROLE_PATHS[role.name]['function'],
    _TILE_PLANE_FIELD_ROLE_PATHS[role.name]['paths'],role.kind,role.default,role.physical_pcs,
    coupled_uses=_TILE_PLANE_FIELD_ROLE_PATHS[role.name]['coupled_uses']) if role.name in _TILE_PLANE_FIELD_ROLE_PATHS else role
    for role in ROLE_SPECS)

# B30 sole palette fields retain existing fade/darken coupled policies.
_PALETTE_SOURCE_FIELD_ROLE_PATHS = {'palette_shade_ceiling': {'function': '_begin_scene_palette_darken_fields_core',
                           'paths': (('body', 5, 'value'),),
                           'coupled_uses': (('_advance_scene_palette_fade_core',
                                             ('body', 14, 'orelse', 2, 'test', 'comparators', 0)),
                                            ('darken_palette', ('body', 8, 'test', 'comparators', 0)))},
 'palette_period_keep_mask': {'function': '_begin_scene_palette_darken_fields_core',
                              'paths': (('body', 2, 'value', 'args', 2, 'right'),),
                              'coupled_uses': (('_advance_scene_palette_fade_core',
                                                ('body', 12, 'value', 'args', 1, 'right')),)},
 'palette_snapshot_longs': {'function': 'snapshot_and_clear_scene_palette_fields',
                            'paths': (('body', 1, 'value'),),
                            'coupled_uses': ()}}
ROLE_SPECS = tuple(MenuRole(role.name,_PALETTE_SOURCE_FIELD_ROLE_PATHS[role.name]['function'],
    _PALETTE_SOURCE_FIELD_ROLE_PATHS[role.name]['paths'],role.kind,role.default,role.physical_pcs,
    coupled_uses=_PALETTE_SOURCE_FIELD_ROLE_PATHS[role.name]['coupled_uses']) if role.name in _PALETTE_SOURCE_FIELD_ROLE_PATHS else role
    for role in ROLE_SPECS)


# Root48 moves only changed palette role paths, retaining all current coupled consumers.
_DARKEN_COMPLETE_FIELD_ROLES = {'darken_nibble_rotation': {'function': 'darken_palette_component_fields', 'paths': (('body', 2, 'value', 'args', 3), ('body', 3, 'value', 'args', 1)), 'coupled_uses': (('darken_palette_fields', ('body', 11, 'body', 5, 'value', 'args', 3)),)}, 'darken_hang_relation': {'function': 'darken_palette_fields', 'paths': (('body', 4, 'test', 'ops', 0),), 'coupled_uses': ()}, 'darken_round_step': {'function': 'darken_palette_fields', 'paths': (('body', 8, 'body', 2, 'body', 1, 'value', 'args', 3),), 'coupled_uses': ()}, 'darken_dirty_step': {'function': 'darken_palette_fields', 'paths': (('body', 13, 'value', 'args', 3),), 'coupled_uses': ()}}
ROLE_SPECS = tuple(MenuRole(role.name,_DARKEN_COMPLETE_FIELD_ROLES[role.name]['function'],_DARKEN_COMPLETE_FIELD_ROLES[role.name]['paths'],role.kind,role.default,role.physical_pcs,coupled_uses=_DARKEN_COMPLETE_FIELD_ROLES[role.name]['coupled_uses']) if role.name in _DARKEN_COMPLETE_FIELD_ROLES else role for role in ROLE_SPECS)
_DARKEN_COMPLETE_COUPLED = {'palette_component_mask': ('darken_palette_component_fields', ('body', 8, 'value', 'args', 2, 'right')), 'palette_shade_ceiling': ('darken_palette_fields', ('body', 2, 'value'))}
ROLE_SPECS = tuple(MenuRole(role.name,role.function,role.paths,role.kind,role.default,role.physical_pcs,coupled_uses=tuple(use for use in role.coupled_uses if use[0] not in ('darken_palette','darken_palette_component'))+(_DARKEN_COMPLETE_COUPLED[role.name],)) if role.name in _DARKEN_COMPLETE_COUPLED else role for role in ROLE_SPECS)

# B32 actor and Scene chain entries share one existing comparison, not a stale legacy coupled body.
ROLE_SPECS = tuple(MenuRole(role.name,'finish_one_scene_sprite_chain_fields',(('body', 4, 'test', 'ops', 0),),
    role.kind,role.default,role.physical_pcs,coupled_uses=()) if role.name == 'scene_chain_nonempty_relation' else role
    for role in ROLE_SPECS)

# B33 actual complete owners replace legacy role observations; native lowering is not newly authored.
_SCENE_ACTION_FIELD_ROLE_PATHS = {'palette_component_mask': {'function': 'advance_scene_palette_fade_fields',
                            'paths': (('body', 19, 'value', 'args', 2, 'right'),)},
 'palette_delay_step': {'function': 'advance_scene_palette_fade_fields',
                        'paths': (('body', 8, 'value', 'args', 3),)},
 'palette_shade_step': {'function': 'advance_scene_palette_fade_fields',
                        'paths': (('body', 15, 'body', 0, 'value', 'args', 3),
                                  ('body', 15, 'orelse', 0, 'value', 'args', 3))},
 'palette_shade_end_relation': {'function': 'advance_scene_palette_fade_fields',
                                'paths': (('body', 15, 'orelse', 3, 'value', 'ops', 0),)},
 'fade_nibble_rotation': {'function': 'advance_scene_palette_fade_fields',
                          'paths': (('body', 24, 'body', 2, 'body', 3, 'body', 4, 'value', 'args', 3),)}}
_SCENE_ACTION_EXTRA_COUPLED = {'palette_component_mask': (('fade_palette_component_fields', ('body', 5, 'value', 'args', 2, 'right')),), 'fade_nibble_rotation': (('fade_palette_component_fields', ('body', 12, 'value', 'args', 3)), ('fade_palette_component_fields', ('body', 13, 'value', 'args', 4)))}
ROLE_SPECS = tuple(MenuRole(role.name,_SCENE_ACTION_FIELD_ROLE_PATHS[role.name]['function'],_SCENE_ACTION_FIELD_ROLE_PATHS[role.name]['paths'],
    role.kind,role.default,role.physical_pcs,coupled_uses=tuple(use for use in role.coupled_uses
    if use[0] not in ('_advance_scene_palette_fade_core','fade_palette_component'))+_SCENE_ACTION_EXTRA_COUPLED.get(role.name,()))
    if role.name in _SCENE_ACTION_FIELD_ROLE_PATHS else role for role in ROLE_SPECS)
_SCENE_ACTION_OLD_COUPLED_REPLACEMENTS = {'palette_period_keep_mask': (('advance_scene_palette_fade_fields', ('body', 10, 'value', 'right')),), 'palette_shade_ceiling': (('advance_scene_palette_fade_fields', ('body', 15, 'orelse', 2, 'value', 'args', 3)), ('advance_scene_palette_fade_fields', ('body', 15, 'orelse', 3, 'value', 'comparators', 0)))}
ROLE_SPECS = tuple(MenuRole(role.name,role.function,role.paths,role.kind,role.default,role.physical_pcs,
    coupled_uses=tuple(use for use in role.coupled_uses if use[0] != '_advance_scene_palette_fade_core')+
    _SCENE_ACTION_OLD_COUPLED_REPLACEMENTS[role.name]) if role.name in _SCENE_ACTION_OLD_COUPLED_REPLACEMENTS
    else role for role in ROLE_SPECS)

# B125 complete current Scene policy uses; no grammar/default fallback.
_CURRENT_SCENE_ROLE_PATHS125 = {'queue_nonempty_relation': {'function': 'flush_scene_transfer_queue_fields', 'paths': (('body', 9, 'test', 'ops', 0),), 'coupled_uses': ()}, 'dictionary_literal_ceiling': {'function': 'write_vdp_dictionary_repeat_stream_fields', 'paths': (('body', 5, 'body', 1, 'value', 'args', 3), ('body', 5, 'body', 4, 'body', 5, 'body', 0, 'value', 'args', 3), ('body', 5, 'body', 7, 'body', 1, 'body', 0, 'value', 'args', 3)), 'coupled_uses': ()}, 'dictionary_repeat_ceiling': {'function': 'write_vdp_dictionary_repeat_stream_fields', 'paths': (('body', 5, 'body', 3, 'value', 'args', 3), ('body', 5, 'body', 4, 'body', 3, 'value', 'args', 3), ('body', 5, 'body', 7, 'body', 0, 'value', 'args', 3)), 'coupled_uses': ()}}
_CURRENT_SCENE_COUPLED125 = {'palette_component_mask': (('darken_palette_component_fields', ('body', 8, 'value', 'args', 2, 'right')), ('fade_palette_component_fields', ('body', 4, 'value', 'args', 2, 'right'))), 'fade_nibble_rotation': (('fade_palette_component_fields', ('body', 11, 'value', 'args', 3)), ('fade_palette_component_fields', ('body', 12, 'value', 'args', 4)))}
ROLE_SPECS = tuple(MenuRole(role.name, _CURRENT_SCENE_ROLE_PATHS125.get(role.name, {}).get('function', role.function), _CURRENT_SCENE_ROLE_PATHS125.get(role.name, {}).get('paths', role.paths), role.kind, role.default, tuple(dict.fromkeys(role.physical_pcs + ((239250,) if role.name == 'sprite_clip_x_maximum_relation' else ()))), coupled_uses=_CURRENT_SCENE_ROLE_PATHS125.get(role.name, {}).get('coupled_uses', _CURRENT_SCENE_COUPLED125.get(role.name, role.coupled_uses))) for role in ROLE_SPECS if role.name != 'sprite_clip_y_maximum_relation')


# Source140: the same two policy nodes follow the literal entry initialization guard.
_LITERAL_PLANE_ROLE_PATHS140 = {'plane_stream_marker_relation': {'function': '_read_vdp_plane_rle_rows_fields_core', 'paths': (('body', 14, 'body', 6, 'value', 'values', 1, 'ops', 0),), 'coupled_uses': ()}, 'plane_initial_rows': {'function': '_read_vdp_plane_rle_rows_fields_core', 'paths': (('body', 3, 'body', 2, 'value', 'args', 2),), 'coupled_uses': ()}}
ROLE_SPECS = tuple(MenuRole(role.name, _LITERAL_PLANE_ROLE_PATHS140[role.name]['function'], _LITERAL_PLANE_ROLE_PATHS140[role.name]['paths'], role.kind, role.default, role.physical_pcs, coupled_uses=role.coupled_uses) if role.name in _LITERAL_PLANE_ROLE_PATHS140 else role for role in ROLE_SPECS)
