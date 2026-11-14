"""Scene target metadata: disjoint spans and real public entry aliases.

No opcode payload. A component is not automatically a whole function, and
actual dynamic dispatch or nonlocal continuation is never replaced by RTS.
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

SCENE_BINDINGS=(
    Binding('flush_scene_transfer_queue',0xad06,((44294, 'flush_scene_transfer_queue'),),((44294, 44316),),False,'independent_contiguous_static_return_component'),
    Binding('write_vdp_packet_stream',0xad1c,((44316, 'write_vdp_packet_stream'),),((44316, 44540),),False,'independent_contiguous_static_return_component'),
    Binding('write_vdp_dictionary_repeat_stream',0xadfc,((44540, 'write_vdp_dictionary_repeat_stream'),),((44540, 44682),),False,'independent_contiguous_static_return_component'),
    Binding('decode_glyph_rows_to_buffers',0xae8a,((44682, 'decode_glyph_rows_to_buffers'),),((44682, 44804),),False,'independent_contiguous_static_return_component'),
    Binding('darken_palette',0xdea6,((56998, 'darken_palette'),),((56998, 57076),),False,'independent_contiguous_static_return_component'),
    Binding('darken_palette_component',0xdef4,((57076, 'darken_palette_component'),),((57076, 57096),),False,'independent_contiguous_static_return_component'),
    Binding('write_vdp_word_rle_stream',0x39658,((235096, 'write_vdp_word_rle_stream'),),((235096, 235162),),False,'independent_contiguous_static_return_component'),
    Binding('play_scripted_scene',0x3969a,((235162, 'play_scripted_scene'),),((235162, 235602), (235604, 235876), (235924, 235992), (236198, 236296), (236304, 236468), (236480, 236524), (236620, 236728), (236784, 236906), (236922, 237086), (237118, 237328), (237386, 237672), (237844, 238040), (238048, 238300), (238370, 238514), (238542, 238642), (238654, 238722), (238730, 238790), (238798, 238858), (238866, 238898)),False,'complete_noncontiguous_static_return_flow'),
    Binding('update_scripted_scene_position',0x399d8,((235992, 'update_scripted_scene_position'),),((235992, 236162),),False,'independent_contiguous_static_return_component'),
    Binding('initialize_scripted_secondary_position',0x39f18,((237336, 'initialize_scripted_secondary_position'),),((237336, 237386),),False,'independent_contiguous_static_return_component'),
    Binding('select_scene_object_frame',0x3a08a,((237706, 'select_scene_object_frame'),),((237706, 237796),),False,'independent_contiguous_static_return_component'),
    Binding('append_clipped_scene_sprites',0x3a5a0,((239008, 'append_clipped_scene_sprites'), (239406, 'append_scene_marker_sprite')),((239008, 239432),),False,'independent_contiguous_static_return_component'),
    Binding('finish_scene_sprite_chains',0x3a74e,((239438, 'finish_scene_sprite_chains'), (239454, 'clear_scene_sprite_chain_heads')),((239438, 239500),),False,'independent_contiguous_static_return_component'),
    Binding('finish_one_scene_sprite_chain',0x3a78c,((239500, 'finish_one_scene_sprite_chain'),),((239500, 239522),),False,'independent_contiguous_static_return_component'),
    Binding('append_unclipped_scene_sprites',0x3a7a2,((239522, 'append_unclipped_scene_sprites'),),((239522, 239772),),False,'independent_contiguous_static_return_component'),
    Binding('advance_scene_palette_fade',0x3a978,((239992, 'advance_scene_palette_fade'),),((239992, 240138),),False,'independent_contiguous_static_return_component'),
    Binding('fade_palette_component',0x3aa0a,((240138, 'fade_palette_component'),),((240138, 240160),),False,'independent_contiguous_static_return_component'),
    Binding('begin_scene_palette_darken',0x3aa20,((240160, 'begin_scene_palette_darken'),),((240160, 240182),),False,'independent_contiguous_static_return_component'),
    Binding('snapshot_and_clear_scene_palette',0x3aa8a,((240266, 'snapshot_and_clear_scene_palette'),),((240266, 240286),),False,'independent_contiguous_static_return_component'),
    Binding('read_vdp_plane_rle_rows',0x3aace,((240334, 'read_vdp_plane_rle_rows'), (240434, 'advance_plane_row')),((240334, 240466),),False,'independent_contiguous_static_return_component'),
    Binding('write_vdp_swapped_byte_rle_stream',0x3ab52,((240466, 'write_vdp_swapped_byte_rle_stream'),),((240466, 240532),),False,'independent_contiguous_static_return_component'),
    Binding('copy_scene_palette_variant',0x3ab94,((240532, 'copy_scene_palette_variant'),),((240532, 240556),),False,'independent_contiguous_static_return_component'),
    Binding('finish_actor_sprite_chains',0x3b23c,((242236, 'finish_actor_sprite_chains'),),((242236, 242290),),False,'independent_contiguous_static_return_component'),
    Binding('finish_one_actor_sprite_chain',0x3b272,((242290, 'finish_one_actor_sprite_chain'),),((242290, 242312),),False,'independent_contiguous_static_return_component'),
    Binding('set_vram_write_address',0x3b2b0,((242352, 'set_vram_write_address'),),((242352, 242392),),False,'independent_contiguous_static_return_component'),
    Binding('sample_random_preserving_seed_carrier',0x3b722,((243490, 'sample_random_preserving_seed_carrier'),),((243490, 243506),),False,'independent_contiguous_static_return_component'),
)

DUEL_BINDINGS=(
    Binding('advance_duel_entry_palette',0x26d86,((159110, 'advance_duel_entry_palette'),),((159110, 159156),),False,'independent_contiguous_static_return_component'),
    Binding('run_duel_scene',0x26db4,((159156, 'run_duel_scene'),),((159046, 159110), (159156, 161030), (161076, 161142), (162192, 162278), (162648, 162710), (162746, 162764)),False,'flow_with_explicit_dynamic_control_boundary'),
    Binding('show_active_duel_turn_label',0x27506,((161030, 'show_active_duel_turn_label'),),((161030, 161076),),False,'flow_with_explicit_dynamic_control_boundary'),
    Binding('wait_active_duel_action',0x2777a,((161658, 'wait_active_duel_action'), (161720, 'wait_either_duel_action')),((161658, 161810),),False,'independent_contiguous_static_return_component'),
    Binding('configure_duel_weapon_motion',0x27a3a,((162362, 'configure_duel_weapon_motion'),),((162362, 162430),),False,'independent_contiguous_static_return_component'),
    Binding('refresh_duel_actors',0x27a84,((162436, 'refresh_duel_actors'),),((162436, 162494),),False,'independent_contiguous_static_return_component'),
    Binding('upload_duel_officer_name',0x27d1c,((163100, 'upload_duel_officer_name'), (163158, 'upload_duel_glyph_strip')),((163100, 163190),),False,'independent_contiguous_static_return_component'),
    Binding('clear_duel_text_plane',0x27d76,((163190, 'clear_duel_text_plane'),),((163190, 163228),),False,'independent_contiguous_static_return_component'),
    Binding('choose_duel_two_option_menu',0x27d9c,((163228, 'choose_duel_two_option_menu'),),((163228, 163324),),False,'independent_contiguous_static_return_component'),
    Binding('choose_first_duel_equipment',0x27dfc,((163324, 'choose_first_duel_equipment'), (163334, 'choose_second_duel_equipment')),((163324, 163538),),False,'independent_contiguous_static_return_component'),
    Binding('choose_duel_action_menu',0x27ed2,((163538, 'choose_duel_action_menu'),),((163538, 163854),),False,'independent_contiguous_static_return_component'),
    Binding('decode_duel_byte_lanes',0x28012,((163858, 'decode_duel_byte_lanes'), (163870, 'decode_duel_byte_lane')),((163858, 163968),),False,'independent_contiguous_static_return_component'),
    Binding('choose_duel_status_text',0x28228,((164392, 'choose_duel_status_text'),),((164392, 164416),),False,'independent_contiguous_static_return_component'),
    Binding('update_duel_actor',0x28b9a,((166810, 'update_duel_actor'), (167532, 'render_duel_actor')),((166810, 167218), (167284, 167820)),False,'complete_noncontiguous_static_return_flow'),
    Binding('scan_duel_thresholds',0x28f90,((167824, 'scan_duel_thresholds'),),((167824, 167836),),False,'independent_contiguous_static_return_component'),
    Binding('append_duel_sprite',0x28f9c,((167836, 'append_duel_sprite'),),((167836, 167992),),False,'independent_contiguous_static_return_component'),
    Binding('measure_duel_weapon_contact',0x2a22e,((172590, 'measure_duel_weapon_contact'),),((172590, 172640),),False,'independent_contiguous_static_return_component'),
    Binding('choose_duel_ai_command',0x2a29a,((172698, 'choose_duel_ai_command'),),((172698, 172808),),False,'flow_with_explicit_dynamic_control_boundary'),
    Binding('choose_duel_ai_override',0x2a5f4,((173556, 'choose_duel_ai_override'),),((173556, 173748), (173772, 173810), (173822, 173962), (174034, 174132), (174204, 174298), (174370, 174464), (174536, 174562), (174586, 174592)),False,'complete_noncontiguous_static_return_flow'),
    Binding('sample_duel_probability',0x2aa00,((174592, 'sample_duel_probability'),),((174592, 174612),),False,'independent_contiguous_static_return_component'),
    Binding('choose_duel_ai_timeout',0x2aa60,((174688, 'choose_duel_ai_timeout'),),((174688, 174734),),False,'independent_contiguous_static_return_component'),
)

OBJECTS_BINDINGS=(
    Binding('distribute_secondary_city_battle_progress',0x1c5e2,((116194, 'distribute_secondary_city_battle_progress'),),((116194, 116206),),False,'new_fragment_with_preexisting_shared_control_tail'),
    Binding('append_scene_center_marker',0x3b288,((242312, 'append_scene_center_marker'), (263238, 'draw_active_scene_object')),((241980, 242236), (242312, 242346), (263238, 263372)),False,'complete_noncontiguous_static_return_flow'),
    Binding('run_scene_object_controller',0x3d654,((251476, 'run_scene_object_controller'),),((251476, 251758), (251866, 252132)),False,'complete_noncontiguous_static_return_flow'),
    Binding('integrate_scene_coordinates',0x3d8e4,((252132, 'integrate_scene_coordinates'),),((252132, 252272),),False,'independent_contiguous_static_return_component'),
    Binding('initialize_scene_object_video',0x3d9a0,((252320, 'initialize_scene_object_video'),),((252320, 252620),),False,'independent_contiguous_static_return_component'),
    Binding('dispatch_scene_object_phase',0x3dcb8,((253112, 'dispatch_scene_object_phase'),),((253112, 253122),),False,'flow_with_explicit_dynamic_control_boundary'),
    Binding('normalize_object_squad_size',0x3f4c2,((259266, 'normalize_object_squad_size'),),((259266, 259352),),False,'independent_contiguous_static_return_component'),
    Binding('cycle_special_scene_palette',0x3f890,((260240, 'cycle_special_scene_palette'),),((260240, 260292),),False,'independent_contiguous_static_return_component'),
    Binding('clear_scene_object_label_plane',0x4031c,((262940, 'clear_scene_object_label_plane'),),((262940, 262972),),False,'independent_contiguous_static_return_component'),
    Binding('advance_scene_object_actions',0x4033c,((262972, 'advance_scene_object_actions'),),((262972, 263178),),False,'independent_contiguous_static_return_component'),
    Binding('rebuild_depth_sorted_object_queue',0x4040a,((263178, 'rebuild_depth_sorted_object_queue'),),((263178, 263238),),False,'independent_contiguous_static_return_component'),
    Binding('update_selected_object_action',0x40c94,((265364, 'update_selected_object_action'),),((265364, 265484), (265540, 265550), (265590, 265596)),False,'flow_with_explicit_dynamic_control_boundary'),
    Binding('read_object_action_mode',0x40d28,((265512, 'read_object_action_mode'),),((265512, 265540),),False,'independent_contiguous_static_return_component'),
    Binding('probe_scene_object_overlap',0x4115c,((266588, 'probe_scene_object_overlap'),),((266588, 266658),),False,'independent_contiguous_static_return_component'),
    Binding('offset_scene_object_position',0x411a2,((266658, 'offset_scene_object_position'),),((266658, 266700),),False,'independent_contiguous_static_return_component'),
    Binding('plan_scene_object_action',0x411cc,((266700, 'plan_scene_object_action'),),((266700, 267514),),False,'new_fragment_with_preexisting_shared_control_tail'),
    Binding('probe_opposing_object_overlap',0x414fa,((267514, 'probe_opposing_object_overlap'),),((267514, 267556),),False,'independent_contiguous_static_return_component'),
    Binding('initialize_scene_object_roster',0x417f6,((268278, 'initialize_scene_object_roster'),),((268278, 268888),),False,'independent_contiguous_static_return_component'),
)

REUSE_BINDINGS=(
    Binding('clear_video_sprite_plane',0x68ce,((26830, 'clear_video_sprite_plane'),),((26830, 26960),),True,'reused_complete_range_or_shared_tail'),
    Binding('enqueue_sound_command',0x808a,((32906, 'enqueue_sound_command'),),((32906, 32976),),True,'reused_complete_range_or_shared_tail'),
    Binding('wait_for_scene_sound_byte',0x83c8,((33736, 'wait_for_scene_sound_byte'),),((33736, 33748),),True,'reused_complete_range_or_shared_tail'),
    Binding('step_random',0x83d4,((33748, 'step_random'),),((33748, 33786),),True,'reused_complete_range_or_shared_tail'),
    Binding('expand_glyph_row',0xaf04,((44804, 'expand_glyph_row'),),((44804, 44830),),True,'reused_complete_range_or_shared_tail'),
    Binding('expand_glyph_stream',0xaf1e,((44830, 'expand_glyph_stream'),),((44830, 44872),),True,'reused_complete_range_or_shared_tail'),
    Binding('build_battlefield_outcome_candidates',0x1c2c8,((115400, 'build_battlefield_outcome_candidates'),),((115400, 115452),),True,'reused_complete_range_or_shared_tail'),
    Binding('distribute_battle_progress_tail',0x1c586,((116102, 'distribute_battle_progress_tail'),),((116102, 116194),),True,'reused_complete_range_or_shared_tail'),
    Binding('stage_sprite_word_packet',0x26bfa,((158714, 'stage_sprite_word_packet'),),((158714, 158796),),True,'reused_complete_range_or_shared_tail'),
    Binding('choose_first_duel_control',0x279e6,((162278, 'choose_first_duel_control'),),((162278, 162320),),True,'reused_complete_range_or_shared_tail'),
    Binding('choose_second_duel_control',0x27a10,((162320, 'choose_second_duel_control'),),((162320, 162362),),True,'reused_complete_range_or_shared_tail'),
)

NEW_BINDINGS=tuple(sorted(SCENE_BINDINGS+DUEL_BINDINGS+OBJECTS_BINDINGS,key=lambda b:b.entry))
REUSED_BINDINGS=REUSE_BINDINGS
BINDINGS=tuple(sorted(NEW_BINDINGS+REUSED_BINDINGS,key=lambda b:b.entry))
BY_NAME={binding.name:binding for binding in BINDINGS}
BY_ENTRY={pc:binding for binding in BINDINGS for pc,name in binding.entries}

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

NEW_BYTES,REUSED_BYTES,TOTAL_BYTES,INSTRUCTIONS=14260,628,14888,3903
