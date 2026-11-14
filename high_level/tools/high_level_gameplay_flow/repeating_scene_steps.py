"""Persistent original Main4B4 -> 3B732 narrative-presentation lifetime.

Only the four complete original parents/service are made cooperative. Five
story-table families remain their existing synchronous whole algorithms.
No IRQ, clock, ready flag, reset authority or physical CALL slot is invented.
"""
import ast
import copy
import inspect
from types import CodeType, FunctionType

from ..high_level_main_flows.business_movement_support import _movement_frame
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
from .contexts_services import SceneRefreshMemory
from .scene_load_steps import GameplaySceneWait
from . import battle_trigger_steps as _battle

BattleScenePrograms = _battle.BattleScenePrograms
EXPECTED_SOURCE = {'support': {'_aux_text_call_fields': 'def _aux_text_call_fields(state: SceneState, frame: '
                                      'FirstDeploymentFrame, target: Long, continuation: Long) -> '
                                      'FirstDeploymentFrame:\n'
                                      '    frame = _resource_cost_frame(state, frame, target)\n'
                                      '    stack = frame.stack_cursor.advance(-4)\n'
                                      '    stack.set_long(0, continuation)\n'
                                      '    entered = first_replace(frame, stack_cursor=stack)\n'
                                      '    children = {216932: dispatch_auxiliary_command_stage_fields, '
                                      '218130: expand_glyph_tile_sequence_fields, 218232: '
                                      'calculate_glyph_row_layout_fields, 218256: '
                                      'select_glyph_bitmap_fields, 218290: '
                                      'expand_monochrome_glyph_byte_fields, 218314: '
                                      'upload_expanded_glyph_rows_fields, 218692: '
                                      'draw_auxiliary_text_panel_border_fields, 218778: '
                                      'draw_auxiliary_text_panel_rows_fields, 218866: '
                                      'upload_auxiliary_text_panel_glyphs_fields, 218944: '
                                      'draw_auxiliary_text_panel_markers_fields, 240310: '
                                      'decode_unmasked_literal_plane_fields, 240322: '
                                      'decode_high_plane_rows_fields, 243604: '
                                      'dispatch_repeating_scene_presentation_fields, 252652: '
                                      'initialize_object_scene_video_fields, 216886: '
                                      'load_active_packet_roster_fields}\n'
                                      '    if target in children:\n'
                                      '        result = children[target](state, entered)\n'
                                      '    elif target == 240334:\n'
                                      '        result = '
                                      'read_vdp_plane_rle_rows_fields(SceneRefreshMemory(state), entered)\n'
                                      '    elif target == 240466:\n'
                                      '        result = '
                                      'write_vdp_swapped_byte_rle_stream_fields(SceneRefreshMemory(state), '
                                      'entered)\n'
                                      '    elif target == 240532:\n'
                                      '        result = '
                                      'copy_scene_palette_variant_fields(SceneRefreshMemory(state), '
                                      'entered)\n'
                                      '    elif target == 240266:\n'
                                      '        result = '
                                      'snapshot_and_clear_scene_palette_fields(SceneRefreshMemory(state), '
                                      'entered)\n'
                                      '    elif target == 26830:\n'
                                      '        from ..high_level_gameplay_flow.business_services import '
                                      'clear_video_sprite_plane_fields\n'
                                      '        result = '
                                      'clear_video_sprite_plane_fields(SceneRefreshMemory(state), entered)\n'
                                      '    elif target == 32906:\n'
                                      '        from ..high_level_gameplay_flow.business_services import '
                                      'enqueue_sound_command_fields\n'
                                      '        result = '
                                      'enqueue_sound_command_fields(SceneRefreshMemory(state), entered)\n'
                                      '    elif target == 418260:\n'
                                      '        from ..high_level_dynamic_flows.business_actions import '
                                      'upload_portrait_tiles_frame_fields\n'
                                      '        result = upload_portrait_tiles_frame_fields(state, entered)\n'
                                      '    elif target == 33736:\n'
                                      '        from ..high_level_gameplay_flow.business_services import '
                                      'wait_for_scene_sound_byte_fields\n'
                                      '        result = '
                                      'wait_for_scene_sound_byte_fields(SceneRefreshMemory(state), entered)\n'
                                      '    elif target == 242312:\n'
                                      '        from ..high_level_scene_flows.business_objects import '
                                      'append_scene_center_marker_fields\n'
                                      '        result = '
                                      'append_scene_center_marker_fields(SceneRefreshMemory(state), '
                                      'entered)\n'
                                      '    elif target == 239992:\n'
                                      '        from ..high_level_scene_flows.business_scene import '
                                      'advance_scene_palette_fade_fields\n'
                                      '        result = '
                                      'advance_scene_palette_fade_fields(SceneRefreshMemory(state), '
                                      'entered)\n'
                                      '    elif target == 242236:\n'
                                      '        from ..high_level_scene_flows.business_scene import '
                                      'finish_actor_sprite_chains_fields\n'
                                      '        result = '
                                      'finish_actor_sprite_chains_fields(SceneRefreshMemory(state), '
                                      'entered)\n'
                                      '    elif target in (211180, 211262, 211336, 211404, 211444, 211472, '
                                      '211640, 212394, 213232) and continuation == 211158:\n'
                                      '        from ..high_level_ai_policy_v2.business_scene_routes import '
                                      'execute_march_policy_fields\n'
                                      '        result = execute_march_policy_fields(state, entered, target)\n'
                                      '    elif target in (213312, 213424, 213694, 213878, 214078, 214120, '
                                      '214330, 214520, 214600, 214634, 214704, 214810, 215166, 215342, '
                                      '215538, 215596, 216016, 216074, 216402, 216482, 216526, 216834, '
                                      '216842) and continuation == 213260:\n'
                                      '        from ..high_level_ai_policy_v2.business_scene_packet_policy '
                                      'import execute_packet_policy_fields\n'
                                      '        result = execute_packet_policy_fields(state, entered, '
                                      'target)\n'
                                      '    elif target in (216980, 217188, 217320, 217394, 217428, 217506, '
                                      '217616, 217734, 217922, 218044, 218092, 218100) and continuation == '
                                      '216952:\n'
                                      '        from ..high_level_ai_policy_v2.business_scene_active_packets '
                                      'import execute_active_packet_fields\n'
                                      '        result = execute_active_packet_fields(state, entered, '
                                      'target)\n'
                                      '    else:\n'
                                      '        raise MovementContinuationBoundary(target, entered, '
                                      "'auxiliary text child lacks a complete admitted frame')\n"
                                      '    result = _resource_cost_frame(state, result, target)\n'
                                      '    token = result.stack_cursor.long()\n'
                                      '    if token != continuation:\n'
                                      "        raise MovementContinuationBoundary(token, result, 'auxiliary "
                                      "text RTS slot changed')\n"
                                      '    state.sr = state.sr & 65504 | result.status\n'
                                      '    return first_replace(result, '
                                      'stack_cursor=result.stack_cursor.advance(4))',
             'run_repeating_scene_presentation_fields': 'def run_repeating_scene_presentation_fields(state: '
                                                        'SceneState, frame: FirstDeploymentFrame) -> '
                                                        'FirstDeploymentFrame:\n'
                                                        '    """3B732\'s complete main loop, with physical '
                                                        'calls and no invented input/IRQ progress."""\n'
                                                        '    frame = _resource_cost_frame(state, frame, '
                                                        '243506)\n'
                                                        '    frame = '
                                                        '_controller_setup_interrupt_status_fields(state, '
                                                        'frame, 9984)\n'
                                                        '    frame = _movement_move(state, frame, '
                                                        "'target_x', state.read(4294964742, 2), 16)\n"
                                                        '    frame = _movement_move(state, frame, '
                                                        "'target_x', low8(frame.target_x) & 191, 8)\n"
                                                        '    frame = _setup_write_fields(state, frame, '
                                                        '12582916, low16(frame.target_x))\n'
                                                        '    frame = _aux_text_call_fields(state, frame, '
                                                        '26830, 243530)\n'
                                                        '    frame = _aux_text_call_fields(state, frame, '
                                                        '252652, 243534)\n'
                                                        '    frame = _aux_text_call_fields(state, frame, '
                                                        '240266, 243538)\n'
                                                        '    frame = _movement_move(state, frame, '
                                                        "'target_x', state.read(4294934746, 2), 16)\n"
                                                        '    frame = _setup_asl_word_fields(state, frame, '
                                                        "'target_x', 1)\n"
                                                        '    frame = _movement_move(state, frame, '
                                                        "'target_x', "
                                                        'state.table_at(243592).word(low16(frame.target_x)), '
                                                        '16)\n'
                                                        '    frame = _aux_text_call_fields(state, frame, '
                                                        '32906, 243554)\n'
                                                        '    frame = '
                                                        '_controller_setup_interrupt_status_fields(state, '
                                                        'frame, 9472)\n'
                                                        '    while True:\n'
                                                        '        frame = _setup_write_fields(state, frame, '
                                                        '4294964754, 1280)\n'
                                                        '        for target, token in ((33736, 243570), '
                                                        '(242312, 243574), (239992, 243578), (243604, '
                                                        '243582), (242236, 243588)):\n'
                                                        '            frame = _aux_text_call_fields(state, '
                                                        'frame, target, token)',
             'dispatch_repeating_scene_presentation_fields': 'def '
                                                             'dispatch_repeating_scene_presentation_fields(state: '
                                                             'SceneState, frame: FirstDeploymentFrame) -> '
                                                             'FirstDeploymentFrame:\n'
                                                             '    """3B794 real indexed JMP: enter the five '
                                                             'genuine story-table BRA owners with the same '
                                                             'full frame and caller slot. Unknown computed '
                                                             'targets retain their boundary."""\n'
                                                             '    frame = _resource_cost_frame(state, frame, '
                                                             '243604)\n'
                                                             '    frame = _movement_move(state, frame, '
                                                             "'target_x', state.read(4294934746, 2), 16)\n"
                                                             '    frame = _setup_asl_word_fields(state, '
                                                             "frame, 'target_x', 2)\n"
                                                             '    target = u32(243614 + '
                                                             's16(low16(frame.target_x)))\n'
                                                             '    if target in (243614, 243618, 243622, '
                                                             '243626, 243630):\n'
                                                             '        from '
                                                             '..high_level_scene_flows.business_scene import '
                                                             '_story_known_fields\n'
                                                             '        return '
                                                             '_story_known_fields(SceneRefreshMemory(state), '
                                                             'frame, target)\n'
                                                             '    raise MovementContinuationBoundary(target, '
                                                             "frame, 'computed presentation JMP entry "
                                                             "requires its genuine owner facade')",
             'initialize_object_scene_video_fields': 'def initialize_object_scene_video_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """3DAEC: all video registers, RAM mirrors, tile streams, planes and palette directory."""\n    frame=_resource_cost_frame(state,frame,0x3DAEC)\n    for value in (0x8F02,0x8230,0x8330,0x8407,0x8568,0x8700,0x8B00,\n            0x8C81,0x8D35,0x8F02,0x9011,0x9194,0x9200):\n        frame=_setup_write_fields(state,frame,0xC00004,value)\n    for address,value in ((0xFFFF8020,0x30),(0xFFFF8024,0),(0xFFFF8026,0x30),\n            (0xFFFF8022,0x20),(0xFFFF8028,0),(0xFFFF802A,0x20)):\n        frame=_setup_write_fields(state,frame,address,value)\n    for directory,video,token in ((0x3DC54,0,0x3DB90),(0x3DC68,0x2000,0x3DBA8),\n            (0x3DC7C,0x4000,0x3DBC0)):\n        frame=_object_scene_directory_fields(state,frame,directory)\n        frame=_movement_move(state,frame,\'target_x\',video,16)\n        frame=_aux_text_call_fields(state,frame,0x3AB52,token)\n    for source,video,token in ((0x4E090,0x8000,0x3DBCE),(0x4FBE4,0xA000,0x3DBDC)):\n        frame=first_replace(frame,roster=state.table_at(source).cursor())\n        frame=_movement_move(state,frame,\'target_x\',video,16)\n        frame=_aux_text_call_fields(state,frame,0x3AB52,token)\n    for directory,address,token in ((0x3DC90,0xE000,0x3DBFC),(0x3DCA4,0xF000,0x3DC1C)):\n        frame=_object_scene_directory_fields(state,frame,directory)\n        frame=first_replace(frame,candidates=state.table_at(address).cursor())\n        frame=_movement_move_long(state,frame,\'offset_x\',0x80)\n        frame=_aux_text_call_fields(state,frame,0x3AACE,token)\n    for source,address,target,token in ((0x45413,0xC000,0x3AAC2,0x3DC32),\n            (0x456EC,0xC040,0x3AAC2,0x3DC48)):\n        frame=first_replace(frame,roster=state.table_at(source).cursor(),candidates=state.table_at(address).cursor())\n        frame=_movement_move_long(state,frame,\'offset_x\',0x80)\n        frame=_aux_text_call_fields(state,frame,target,token)\n    frame=_movement_move(state,frame,\'target_x\',state.read(0xFFFF80DA,2),16)\n    frame=_map_presentation_arithmetic_fields(state,frame,\'target_x\',4)\n    return _aux_text_call_fields(state,frame,0x3AB94,0x3DC52)',
             '_object_scene_directory_fields': 'def _object_scene_directory_fields(state: SceneState, frame: '
                                               'FirstDeploymentFrame, directory: Long) -> '
                                               'FirstDeploymentFrame:\n'
                                               "    frame = _movement_move(state, frame, 'target_x', "
                                               'state.read(4294934746, 2), 16)\n'
                                               "    frame = _setup_asl_word_fields(state, frame, 'target_x', "
                                               '2)\n'
                                               '    frame = first_replace(frame, '
                                               'roster=state.table_at(directory).cursor())\n'
                                               '    pointer = frame.roster.long(low16(frame.target_x))\n'
                                               '    return first_replace(frame, '
                                               'roster=state.table_at(pointer).cursor())'},
 'main': {'begin_nonreturning_scripted_scene_fields': 'def begin_nonreturning_scripted_scene_fields(state: '
                                                      'SceneState, frame: FirstDeploymentFrame) -> '
                                                      'FirstDeploymentFrame:\n'
                                                      '    """4B4: begin nonreturning scripted scene; '
                                                      'original stage and child tokens."""\n'
                                                      '    frame = _city_ui_frame_fields(state, frame, '
                                                      '1204)\n'
                                                      '    state.sr = 9984\n'
                                                      '    frame = first_replace(frame, status=0)\n'
                                                      '    frame = _campaign_call_fields(state, frame, '
                                                      '243506, 1408)\n'
                                                      '    return frame'},
 'services': {'wait_for_scene_sound_byte_fields': 'def wait_for_scene_sound_byte_fields(memory: '
                                                  'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                  'FirstDeploymentFrame:\n'
                                                  '    """83C8: true SR2500, live BYTE poll, no simulated '
                                                  'sound/IRQ completion."""\n'
                                                  '    _scene_refresh_frame(memory, frame)\n'
                                                  '    frame = memory.status_word(frame, 9472)\n'
                                                  '    while True:\n'
                                                  '        value = memory.state.read(4294964754, 1)\n'
                                                  '        frame = _scene_refresh_flags(memory, frame, '
                                                  'value, 1)\n'
                                                  '        if value == 0:\n'
                                                  '            return frame\n'
                                                  "        memory.state.progress('scene-sound-byte')"},
 'boot': {'reset_console_frame_fields': 'def reset_console_frame_fields(state: SceneState, frame: '
                                        'FirstDeploymentFrame, profile: ResetProfile | None=None) -> '
                                        'FirstDeploymentFrame:\n'
                                        '    """206→300, retaining all real bootstrap MOVEM and device '
                                        'effects."""\n'
                                        '    from .business_movement_support import _movement_test_long, '
                                        '_movement_test, _movement_add_word\n'
                                        '    from .business_map import _world_map_bit_fields\n'
                                        '    frame = display_frame_fields(state, frame)\n'
                                        '    frame = _movement_test_long(state, frame, state.read(10551304, '
                                        '4))\n'
                                        '    if frame.status & 4:\n'
                                        '        frame = _movement_test(state, frame, state.read(10551308, '
                                        '2), 16)\n'
                                        '    if not frame.status & 4:\n'
                                        '        return start_game_main_loop_frame_fields(state, frame)\n'
                                        "    frame = display_address_fields(state, frame, 'scratch', 660)\n"
                                        "    for name in ('offset_x', 'offset_y', 'choice'):\n"
                                        '        value = u32(s16(frame.scratch.word()))\n'
                                        '        frame = first_replace(frame, **{name: value}, '
                                        'scratch=frame.scratch.advance(2))\n'
                                        "    for name in ('roster', 'candidates', 'controller', 'scan', "
                                        "'opponent'):\n"
                                        '        value = frame.scratch.long()\n'
                                        '        frame = first_replace(frame, '
                                        'scratch=frame.scratch.advance(4))\n'
                                        '        frame = display_address_fields(state, frame, name, value)\n'
                                        "    frame = display_move_fields(state, frame, 'target_x', "
                                        'state.read(u32(frame.candidates.base - 4351), 1), 8)\n'
                                        "    frame = display_move_fields(state, frame, 'target_x', "
                                        'low8(frame.target_x) & 15, 8)\n'
                                        '    if not frame.status & 4:\n'
                                        '        frame = display_store_fields(state, frame, 556, '
                                        'u32(frame.candidates.base + 12032), 1397049153, 4)\n'
                                        "    frame = display_move_fields(state, frame, 'target_x', "
                                        'frame.opponent.word())\n'
                                        "    frame = display_move_fields(state, frame, 'target_x', 0, 32)\n"
                                        "    frame = display_address_fields(state, frame, 'auxiliary', "
                                        'frame.target_x)\n'
                                        '    if type(profile) is not ResetProfile:\n'
                                        "        raise MovementContinuationBoundary(570, frame, 'original "
                                        "MOVE A6,USP requires the existing explicit BootstrapControl')\n"
                                        '    profile.validate(state)\n'
                                        '    profile.processor.set_user_stack(state, frame.auxiliary.base)\n'
                                        "    frame = display_move_fields(state, frame, 'target_y', 23, 32)\n"
                                        '    while True:\n'
                                        '        value = frame.scratch.byte()\n'
                                        '        frame = first_replace(frame, '
                                        'scratch=frame.scratch.advance(1))\n'
                                        "        frame = display_move_fields(state, frame, 'offset_x', "
                                        'value, 8)\n'
                                        '        frame = display_store_fields(state, frame, 576, '
                                        'frame.opponent.base, low16(frame.offset_x))\n'
                                        "        frame = _movement_add_word(state, frame, 'offset_x', "
                                        'low16(frame.choice))\n'
                                        "        frame, more = display_loop_fields(frame, 'target_y')\n"
                                        '        if not more:\n'
                                        '            break\n'
                                        '    value = frame.scratch.long()\n'
                                        '    frame = first_replace(frame, scratch=frame.scratch.advance(4))\n'
                                        '    frame = display_store_fields(state, frame, 584, '
                                        'frame.opponent.base, value, 4)\n'
                                        '    frame = display_store_fields(state, frame, 586, '
                                        'frame.scan.base, low16(frame.target_x))\n'
                                        '    frame = display_store_fields(state, frame, 588, '
                                        'frame.candidates.base, low16(frame.choice))\n'
                                        '    frame = display_store_fields(state, frame, 590, '
                                        'frame.controller.base, low16(frame.choice))\n'
                                        '    while True:\n'
                                        '        frame = _world_map_bit_fields(state, frame, '
                                        'frame.candidates.byte(), frame.target_x & 7)\n'
                                        '        if frame.status & 4:\n'
                                        '            break\n'
                                        "        state.progress('original250 sound bus request bit0')\n"
                                        "    frame = display_move_fields(state, frame, 'unit', 37, 32)\n"
                                        '    while True:\n'
                                        '        value = frame.scratch.byte()\n'
                                        '        frame = first_replace(frame, '
                                        'scratch=frame.scratch.advance(1))\n'
                                        '        frame = display_store_fields(state, frame, 598, '
                                        'frame.roster.base, value, 1)\n'
                                        '        frame = first_replace(frame, '
                                        'roster=frame.roster.advance(1))\n'
                                        "        frame, more = display_loop_fields(frame, 'unit')\n"
                                        '        if not more:\n'
                                        '            break\n'
                                        '    frame = display_store_fields(state, frame, 604, '
                                        'frame.controller.base, low16(frame.target_x))\n'
                                        '    frame = display_store_fields(state, frame, 606, '
                                        'frame.candidates.base, low16(frame.target_x))\n'
                                        '    frame = display_store_fields(state, frame, 608, '
                                        'frame.controller.base, low16(frame.choice))\n'
                                        '    while True:\n'
                                        '        frame = first_replace(frame, '
                                        'auxiliary=frame.auxiliary.advance(-4))\n'
                                        '        frame = display_store_fields(state, frame, 610, '
                                        'frame.auxiliary.base, frame.target_x, 4)\n'
                                        "        frame, more = display_loop_fields(frame, 'offset_y')\n"
                                        '        if not more:\n'
                                        '            break\n'
                                        '    for pc in (616, 618):\n'
                                        '        value = frame.scratch.long()\n'
                                        '        frame = first_replace(frame, '
                                        'scratch=frame.scratch.advance(4))\n'
                                        '        frame = display_store_fields(state, frame, pc, '
                                        'frame.opponent.base, value, 4)\n'
                                        "    frame = display_move_fields(state, frame, 'count', 31, 32)\n"
                                        '    while True:\n'
                                        '        frame = display_store_fields(state, frame, 622, '
                                        'frame.scan.base, frame.target_x, 4)\n'
                                        "        frame, more = display_loop_fields(frame, 'count')\n"
                                        '        if not more:\n'
                                        '            break\n'
                                        '    value = frame.scratch.long()\n'
                                        '    frame = first_replace(frame, scratch=frame.scratch.advance(4))\n'
                                        '    frame = display_store_fields(state, frame, 628, '
                                        'frame.opponent.base, value, 4)\n'
                                        "    frame = display_move_fields(state, frame, 'distance', 19, 32)\n"
                                        '    while True:\n'
                                        '        frame = display_store_fields(state, frame, 632, '
                                        'frame.scan.base, frame.target_x, 4)\n'
                                        "        frame, more = display_loop_fields(frame, 'distance')\n"
                                        '        if not more:\n'
                                        '            break\n'
                                        "    frame = display_move_fields(state, frame, 'offset_x', 3, 32)\n"
                                        '    while True:\n'
                                        '        value = frame.scratch.byte()\n'
                                        '        frame = first_replace(frame, '
                                        'scratch=frame.scratch.advance(1))\n'
                                        '        frame = display_store_fields(state, frame, 640, '
                                        'u32(frame.scan.base + 17), value, 1)\n'
                                        "        frame, more = display_loop_fields(frame, 'offset_x')\n"
                                        '        if not more:\n'
                                        '            break\n'
                                        '    frame = display_store_fields(state, frame, 648, '
                                        'frame.controller.base, low16(frame.target_x))\n'
                                        '    source = frame.auxiliary\n'
                                        "    for name in ('target_x', 'target_y', 'unit', 'count', "
                                        "'distance', 'offset_x', 'offset_y', 'choice', 'roster', "
                                        "'candidates', 'controller', 'scan', 'opponent', 'scratch', "
                                        "'auxiliary'):\n"
                                        '        value = source.long()\n'
                                        '        source = source.advance(4)\n'
                                        "        if name in ('roster', 'candidates', 'controller', 'scan', "
                                        "'opponent', 'scratch', 'auxiliary'):\n"
                                        '            frame = display_address_fields(state, frame, name, '
                                        'value)\n'
                                        '        else:\n'
                                        '            frame = first_replace(frame, **{name: value})\n'
                                        '    frame = display_status_fields(state, frame, 9984)\n'
                                        '    return start_game_main_loop_frame_fields(state, frame)',
          'start_game_main_loop_frame_fields': 'def start_game_main_loop_frame_fields(state: SceneState, '
                                               'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                               '    """Whole original invocation, retaining its actual 003BC '
                                               'continuation."""\n'
                                               '    from .bootstrap_steps import '
                                               'run_bootstrap_main_blocking_fields\n'
                                               '    return run_bootstrap_main_blocking_fields(state, frame)'},
 'objects': {'append_scene_center_marker_fields': 'def append_scene_center_marker_fields(memory: '
                                                  'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                  'FirstDeploymentFrame:\n'
                                                  '    """3B288: actual world origin minus 64 and the '
                                                  'original marker stream."""\n'
                                                  '    from .business_scene import _scene_render_arithmetic\n'
                                                  '    memory.frame(frame)\n'
                                                  '    if frame.stack_cursor is None:\n'
                                                  '        raise SceneRefreshBoundary(242312, frame, None)\n'
                                                  '    memory.sync_status(frame)\n'
                                                  "    frame = _first_word(frame, 'target_x', "
                                                  'memory.state.read(4294934560, 2))\n'
                                                  '    frame = _scene_render_arithmetic(memory, frame, '
                                                  "'target_x', low16(frame.target_x), 64, 16, True)\n"
                                                  "    frame = _first_word(frame, 'target_y', "
                                                  'memory.state.read(4294934562, 2))\n'
                                                  '    frame = _scene_render_arithmetic(memory, frame, '
                                                  "'target_y', low16(frame.target_y), 64, 16, True)\n"
                                                  "    frame = _first_long(frame, 'unit', 0)\n"
                                                  "    frame = _first_long(frame, 'count', 0)\n"
                                                  "    frame = _first_word(frame, 'distance', 0)\n"
                                                  '    frame = first_replace(frame, '
                                                  'roster=memory.cursor_at(242346))\n'
                                                  '    return _append_object_sprite_fields(memory, frame)'},
 'story': {'_story_add_ram_fields': 'def _story_add_ram_fields(memory: SceneRefreshMemory, frame: '
                                    'FirstDeploymentFrame, low: Word, amount: Word=1) -> '
                                    'FirstDeploymentFrame:\n'
                                    '    from .business_objects import _object_adjust_word_fields\n'
                                    '    return _object_adjust_word_fields(memory, frame, 4294901760 | low, '
                                    'amount)',
           '_story_animation_index_fields': 'def _story_animation_index_fields(memory: SceneRefreshMemory, '
                                            'frame: FirstDeploymentFrame, counter: Word, shift: Word, '
                                            'maximum: Word, reset_counter: bool, hold_last: bool=False) -> '
                                            'FirstDeploymentFrame:\n'
                                            '    frame = _story_add_ram_fields(memory, frame, counter)\n'
                                            "    frame = _story_ram_move_fields(memory, frame, 'unit', "
                                            'counter)\n'
                                            "    frame = _scene_mode_lsr_word(memory, frame, 'unit', "
                                            'low16(frame.unit), shift)\n'
                                            '    frame = _scene_render_compare(memory, frame, '
                                            'low16(frame.unit), maximum, 16)\n'
                                            '    if not frame.status & 5:\n'
                                            '        if reset_counter:\n'
                                            '            frame = _story_clear_fields(memory, frame, '
                                            'counter)\n'
                                            "        frame = _story_move_fields(memory, frame, 'unit', "
                                            'maximum if hold_last else 0, 32)\n'
                                            '    return frame',
           '_story_arithmetic_fields': 'def _story_arithmetic_fields(memory: SceneRefreshMemory, frame: '
                                       'FirstDeploymentFrame, name, value: Word, subtract: bool=False) -> '
                                       'FirstDeploymentFrame:\n'
                                       '    return _scene_render_arithmetic(memory, frame, name, '
                                       'low16(frame.carrier(name)), value, 16, subtract)',
           '_story_call_fields': 'def _story_call_fields(memory: SceneRefreshMemory, frame: '
                                 'FirstDeploymentFrame, target: Long, continuation: Long) -> '
                                 'FirstDeploymentFrame:\n'
                                 '    """Caller owns one real LONG. Unknown children stop after that '
                                 'physical write."""\n'
                                 '    memory.frame(frame)\n'
                                 '    memory.sync_status(frame)\n'
                                 '    entered = _scene_render_push_longs(memory, frame, (continuation,))\n'
                                 '    result = _story_known_fields(memory, entered, target)\n'
                                 '    memory.frame(result)\n'
                                 '    if frame.stack_cursor is not None:\n'
                                 '        actual = result.stack_cursor.long()\n'
                                 '        if actual != continuation:\n'
                                 '            raise SceneRefreshBoundary(target, result, continuation)\n'
                                 '        result = first_replace(result, '
                                 'stack_cursor=result.stack_cursor.advance(4))\n'
                                 '    return memory.sync_status(result)',
           '_story_caption_trigger_fields': 'def _story_caption_trigger_fields(memory: SceneRefreshMemory, '
                                            'frame: FirstDeploymentFrame, threshold: Word, source: Long) -> '
                                            'FirstDeploymentFrame:\n'
                                            '    frame = _story_compare_ram_fields(memory, frame, 33082, '
                                            'threshold)\n'
                                            '    if frame.status & 4:\n'
                                            '        frame = _story_status_fields(memory, frame, 9984)\n'
                                            '        frame = _story_clear_plane_fields(memory, frame)\n'
                                            '        frame = _story_script_fields(memory, frame, source)\n'
                                            '        frame = _story_status_fields(memory, frame, 9472)\n'
                                            '    return frame',
           '_story_clear_fields': 'def _story_clear_fields(memory: SceneRefreshMemory, frame: '
                                  'FirstDeploymentFrame, low: Word) -> FirstDeploymentFrame:\n'
                                  '    from .business_objects import _object_clear_word_fields\n'
                                  '    return _object_clear_word_fields(memory, frame, 4294901760 | low)',
           '_story_clear_plane_fields': 'def _story_clear_plane_fields(memory: SceneRefreshMemory, frame: '
                                        'FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                        '    from ..high_level_dynamic_flows.business_early_phase import '
                                        '_allocation_fill_fields\n'
                                        '    return _allocation_fill_fields(memory, frame, 1610612738, '
                                        '13107, 3455, True)',
           '_story_compare_ram_fields': 'def _story_compare_ram_fields(memory: SceneRefreshMemory, frame: '
                                        'FirstDeploymentFrame, low: Word, value: Word) -> '
                                        'FirstDeploymentFrame:\n'
                                        '    return _scene_render_compare(memory, frame, '
                                        '_story_read_fields(memory, frame, 4294901760 | low), value, 16)',
           '_story_confirm_page_fields': 'def _story_confirm_page_fields(memory: SceneRefreshMemory, frame: '
                                         'FirstDeploymentFrame, picture: Long, picture_return: Long, source: '
                                         'Long) -> tuple:\n'
                                         '    frame, pressed = _story_pressed_fields(memory, frame)\n'
                                         '    if not pressed:\n'
                                         '        return (frame, False)\n'
                                         '    frame = _story_status_fields(memory, frame, 9984)\n'
                                         '    frame = _story_decode_picture_fields(memory, frame, picture, '
                                         'picture_return)\n'
                                         '    frame = _story_clear_plane_fields(memory, frame)\n'
                                         '    frame = _story_script_fields(memory, frame, source)\n'
                                         '    return (_story_status_fields(memory, frame, 9472), True)',
           '_story_decimal_strip_fields': 'def _story_decimal_strip_fields(memory: SceneRefreshMemory, '
                                          'frame: FirstDeploymentFrame, role) -> FirstDeploymentFrame:\n'
                                          '    """Two/three-digit roles use the existing decimal and glyph '
                                          'algorithms exactly once."""\n'
                                          "    if role == 'officer':\n"
                                          '        counter, decimal_return, glyph_return, digits = (32996, '
                                          '262420, 262486, 3)\n'
                                          "    elif role == 'pair':\n"
                                          '        counter, decimal_return, glyph_return, digits = (32998, '
                                          '262548, 262602, 2)\n'
                                          "    elif role == 'triple':\n"
                                          '        counter, decimal_return, glyph_return, digits = (33000, '
                                          '262692, 262758, 3)\n'
                                          '    else:\n'
                                          "        raise ValueError('closed text number role required')\n"
                                          "    if role == 'triple':\n"
                                          '        frame = _story_store_fields(memory, frame, 16740364, '
                                          'low16(frame.unit))\n'
                                          '        frame = _story_store_fields(memory, frame, 16740366, '
                                          'frame.roster.base, 4)\n'
                                          '    else:\n'
                                          '        frame = _story_store_fields(memory, frame, 16740366, '
                                          'frame.roster.base, 4)\n'
                                          '        frame = _story_store_fields(memory, frame, 16740364, '
                                          'low16(frame.unit))\n'
                                          "    frame = _story_move_fields(memory, frame, 'target_x', 0, 32)\n"
                                          "    frame = _story_ram_move_fields(memory, frame, 'target_x', "
                                          'counter)\n'
                                          '    frame = _story_call_fields(memory, frame, 242392, '
                                          'decimal_return)\n'
                                          "    carriers = ('target_x', 'target_y', 'unit') if digits == 3 "
                                          "else ('target_x', 'target_y')\n"
                                          '    for name in carriers:\n'
                                          '        frame = _story_move_fields(memory, frame, name, 256)\n'
                                          '    for index, name in enumerate(carriers):\n'
                                          '        frame = _story_ram_move_fields(memory, frame, name, 32774 '
                                          '- digits + index, 8)\n'
                                          '    for index, name in enumerate(carriers):\n'
                                          '        frame = _story_store_fields(memory, frame, 4294934528 + '
                                          'index * 2, low16(frame.carrier(name)))\n'
                                          '    frame = first_replace(frame, '
                                          'roster=memory.cursor_at(4294934528), '
                                          'candidates=memory.cursor_at(4294955776))\n'
                                          '    frame = _story_text_dimensions_fields(memory, frame, digits - '
                                          '1, glyph_return)\n'
                                          '    frame = first_replace(frame, '
                                          'roster=memory.cursor_at(4294955776), '
                                          'auxiliary=memory.cursor_at(12582912))\n'
                                          "    frame = _story_move_fields(memory, frame, 'target_x', digits "
                                          '* 32 - 1)\n'
                                          "    if role == 'pair':\n"
                                          '        frame = _story_compare_ram_fields(memory, frame, 32768, '
                                          '256)\n'
                                          '        if frame.status & 4:\n'
                                          '            frame = first_replace(frame, '
                                          'roster=frame.roster.advance(128))\n'
                                          "            frame = _story_move_fields(memory, frame, 'target_x', "
                                          '_story_read_fields(memory, frame, 16740364))\n'
                                          '            frame = _story_arithmetic_fields(memory, frame, '
                                          "'target_x', 128)\n"
                                          '            frame = _story_call_fields(memory, frame, 242352, '
                                          '262642)\n'
                                          "            frame = _story_move_fields(memory, frame, 'target_x', "
                                          '31)\n'
                                          "    elif role == 'triple':\n"
                                          '        frame = _story_text_tile_fields(memory, frame, 384)\n'
                                          '        frame = _story_compare_ram_fields(memory, frame, 32768, '
                                          '256)\n'
                                          '        if frame.status & 4:\n'
                                          '            frame = first_replace(frame, '
                                          'roster=frame.roster.advance(128))\n'
                                          '            frame = _story_text_tile_fields(memory, frame, 256)\n'
                                          "            frame = _story_move_fields(memory, frame, 'target_x', "
                                          '63)\n'
                                          '            frame = _story_compare_ram_fields(memory, frame, '
                                          '32770, 256)\n'
                                          '            if frame.status & 4:\n'
                                          '                frame = first_replace(frame, '
                                          'roster=frame.roster.advance(128))\n'
                                          '                frame = _story_text_tile_fields(memory, frame, '
                                          '128)\n'
                                          '                frame = _story_move_fields(memory, frame, '
                                          "'target_x', 31)\n"
                                          '    frame = _story_upload_current_rows_fields(memory, frame)\n'
                                          "    if role != 'triple':\n"
                                          '        frame = _story_text_tile_fields(memory, frame, digits * '
                                          '128)\n'
                                          '    frame = first_replace(frame, '
                                          'roster=memory.cursor_at(_story_read_fields(memory, frame, '
                                          '16740366, 4)))\n'
                                          "    if role != 'pair':\n"
                                          '        frame = first_replace(frame, '
                                          'roster=frame.roster.advance(2))\n'
                                          '    return memory.sync_status(frame)',
           '_story_decode_picture_fields': 'def _story_decode_picture_fields(memory: SceneRefreshMemory, '
                                           'frame: FirstDeploymentFrame, source: Long, continuation: Long) '
                                           '-> FirstDeploymentFrame:\n'
                                           '    frame = first_replace(frame, '
                                           'roster=memory.cursor_at(source), '
                                           'candidates=memory.cursor_at(57344))\n'
                                           "    frame = _story_move_fields(memory, frame, 'offset_x', 128, "
                                           '32)\n'
                                           "    frame = _story_move_fields(memory, frame, 'offset_y', 18)\n"
                                           '    return _story_call_fields(memory, frame, 240334, '
                                           'continuation)',
           '_story_dispatch_fields': 'def _story_dispatch_fields(memory: SceneRefreshMemory, frame: '
                                     'FirstDeploymentFrame, table: Long) -> FirstDeploymentFrame:\n'
                                     '    """Original live stage WORD selects actual four-byte BRA CODE, not '
                                     'a fake callback."""\n'
                                     '    memory.frame(frame)\n'
                                     "    frame = _story_ram_move_fields(memory, frame, 'target_x', 33002)\n"
                                     "    frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                     'low16(frame.target_x), 2)\n'
                                     '    return _story_known_fields(memory, frame, table + '
                                     's16(low16(frame.target_x)))',
           '_story_dma_finish_fields': 'def _story_dma_finish_fields(memory: SceneRefreshMemory, frame: '
                                       'FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                       "    frame = _story_ram_move_fields(memory, frame, 'target_x', "
                                       '62982)\n'
                                       "    frame = _story_move_fields(memory, frame, 'target_x', "
                                       'low8(frame.target_x) | 64, 8)\n'
                                       '    return _story_store_fields(memory, frame, 12582916, '
                                       'low16(frame.target_x))',
           '_story_dma_setup_fields': 'def _story_dma_setup_fields(memory: SceneRefreshMemory, frame: '
                                      'FirstDeploymentFrame, words: tuple, latch: Word, retain_port: bool) '
                                      '-> FirstDeploymentFrame:\n'
                                      '    """Actual Z80 bus request/release and VDP DMA commands, never '
                                      'fabricated ACK."""\n'
                                      '    if retain_port:\n'
                                      '        frame = first_replace(frame, '
                                      'auxiliary=memory.cursor_at(12582916))\n'
                                      "    frame = _story_ram_move_fields(memory, frame, 'choice', 62982)\n"
                                      "    frame = _story_move_fields(memory, frame, 'choice', "
                                      'low8(frame.choice) | 16, 8)\n'
                                      '    frame = _story_store_fields(memory, frame, frame.auxiliary.base, '
                                      'low16(frame.choice))\n'
                                      '    frame = _story_store_fields(memory, frame, 10555648, 256)\n'
                                      '    frame = _story_store_fields(memory, frame, frame.auxiliary.base, '
                                      'words[0], 4)\n'
                                      '    frame = _story_store_fields(memory, frame, frame.auxiliary.base, '
                                      'words[1], 4)\n'
                                      '    frame = _story_store_fields(memory, frame, frame.auxiliary.base, '
                                      '38783)\n'
                                      '    frame = _story_store_fields(memory, frame, frame.auxiliary.base, '
                                      'words[2])\n'
                                      '    frame = _story_store_fields(memory, frame, 4294964768, latch)\n'
                                      '    frame = _story_store_fields(memory, frame, frame.auxiliary.base, '
                                      '_story_read_fields(memory, frame, 4294964768))\n'
                                      '    value = _story_read_fields(memory, frame, 4294917888, 1)\n'
                                      '    frame = _scene_refresh_flags(memory, frame, value, 1)\n'
                                      '    if frame.status & 4:\n'
                                      '        frame = _story_store_fields(memory, frame, 10555648, 0)\n'
                                      '    return frame',
           '_story_draw_pose_fields': 'def _story_draw_pose_fields(memory: SceneRefreshMemory, frame: '
                                      'FirstDeploymentFrame, x: Word, y: Word, target: Long, continuation: '
                                      'Long, attributes: Word | None=None) -> FirstDeploymentFrame:\n'
                                      "    frame = _story_move_fields(memory, frame, 'target_x', x)\n"
                                      "    frame = _story_move_fields(memory, frame, 'target_y', y)\n"
                                      '    if attributes is not None:\n'
                                      "        frame = _story_move_fields(memory, frame, 'distance', "
                                      'attributes)\n'
                                      '    return _story_call_fields(memory, frame, target, continuation)',
           '_story_exit_fields': 'def _story_exit_fields(memory: SceneRefreshMemory, frame: '
                                 'FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                 '    frame, pressed = _story_pressed_fields(memory, frame)\n'
                                 '    if pressed:\n'
                                 '        return _story_known_fields(memory, frame, 518)\n'
                                 '    return memory.sync_status(frame)',
           '_story_finish_stage_fields': 'def _story_finish_stage_fields(memory: SceneRefreshMemory, frame: '
                                         'FirstDeploymentFrame, counters: tuple=(33082,)) -> '
                                         'FirstDeploymentFrame:\n'
                                         '    for low in counters:\n'
                                         '        frame = _story_clear_fields(memory, frame, low)\n'
                                         '    return _story_add_ram_fields(memory, frame, 33002)',
           '_story_finish_text_stream_fields': 'def _story_finish_text_stream_fields(memory: '
                                               'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                               'FirstDeploymentFrame:\n'
                                               '    frame = _story_store_fields(memory, frame, 16740364, '
                                               'low16(frame.unit))\n'
                                               '    return _story_store_fields(memory, frame, 16740366, '
                                               'frame.roster.base, 4)',
           '_story_glyph_upload_fields': 'def _story_glyph_upload_fields(memory: SceneRefreshMemory, frame: '
                                         'FirstDeploymentFrame, rows: Word) -> FirstDeploymentFrame:\n'
                                         '    """Ordered LONG writes to the real VDP port; no RAM-backed '
                                         'device substitute."""\n'
                                         '    frame = first_replace(frame, '
                                         'auxiliary=memory.cursor_at(12582912))\n'
                                         "    frame = _story_move_fields(memory, frame, 'target_x', rows)\n"
                                         '    return _story_upload_current_rows_fields(memory, frame)',
           '_story_initialize_fields': 'def _story_initialize_fields(memory: SceneRefreshMemory, frame: '
                                       'FirstDeploymentFrame, scene) -> FirstDeploymentFrame:\n'
                                       '    """Five closed story roles share the actual plane fill and '
                                       'palette algorithm."""\n'
                                       '    memory.frame(frame)\n'
                                       "    if scene == 'prologue':\n"
                                       '        masks, palette_return, row_return, source = ((65535, 0, '
                                       '65535, 65535), 243714, None, 242904)\n'
                                       "    elif scene == 'departure':\n"
                                       '        masks, palette_return, row_return, source = ((65535,) * 4, '
                                       '246238, 246242, 243080)\n'
                                       "    elif scene == 'interlude':\n"
                                       '        masks, palette_return, row_return, source = ((65535,) * 4, '
                                       '248232, 248236, 243428)\n'
                                       "    elif scene == 'arrival':\n"
                                       '        masks, palette_return, row_return, source = ((65535,) * 4, '
                                       '248550, None, 243220)\n'
                                       "    elif scene == 'finale':\n"
                                       '        masks, palette_return, row_return, source = ((65535,) * 4, '
                                       '250298, None, None)\n'
                                       '    else:\n'
                                       "        raise ValueError('closed story initialization role "
                                       "required')\n"
                                       "    if scene != 'prologue':\n"
                                       '        frame = _story_status_fields(memory, frame, 9984)\n'
                                       '    frame = _story_palette_masks_fields(memory, frame, masks)\n'
                                       "    frame = _story_move_fields(memory, frame, 'target_x', 1, 32)\n"
                                       '    frame = _story_call_fields(memory, frame, 240160, '
                                       'palette_return)\n'
                                       '    if row_return is not None:\n'
                                       '        frame = _story_call_fields(memory, frame, 246330, '
                                       'row_return)\n'
                                       "    if scene == 'prologue':\n"
                                       '        frame = _story_status_fields(memory, frame, 9984)\n'
                                       '    frame = _story_clear_plane_fields(memory, frame)\n'
                                       '    if source is None:\n'
                                       '        frame = _story_store_fields(memory, frame, 16740372, 3)\n'
                                       '        frame = _story_store_fields(memory, frame, 16740374, 1)\n'
                                       '    else:\n'
                                       '        frame = _story_script_fields(memory, frame, source, True)\n'
                                       "    if scene == 'prologue':\n"
                                       '        frame = _story_status_fields(memory, frame, 9472)\n'
                                       '    else:\n'
                                       '        frame = _story_store_fields(memory, frame, 4294934844, 3)\n'
                                       '    frame = _story_add_ram_fields(memory, frame, 33002)\n'
                                       "    if scene != 'prologue':\n"
                                       '        frame = _story_status_fields(memory, frame, 9472)\n'
                                       '    return memory.sync_status(frame)',
           '_story_known_fields': 'def _story_known_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long) -> FirstDeploymentFrame:\n    """Genuine complete story children, including402C2 live officer-name rendering. The real caller already owns the LONG; same-state full frame and all actual DATA/device boundaries survive."""\n    memory.frame(frame)\n    if target == 26570:\n        from ..high_level_main_flows.business_lowbank import poll_controller_with_z80_bus_fields\n        return poll_controller_with_z80_bus_fields(memory.state, frame)\n    if target == 18754:\n        from ..high_level_remaining_flows.business_lowbank import lowbank_process_device_control_9_fields\n        return lowbank_process_device_control_9_fields(memory.state, frame)\n    if target == 518:\n        from ..high_level_main_flows.business_boot import reset_console_frame_fields\n        return reset_console_frame_fields(memory.state, frame)\n    if target == 238902:\n        return transfer_story_plane_dma_fields(memory, frame)\n    elif target == 239772:\n        return transfer_story_overlay_dma_fields(memory, frame)\n    elif target == 243614:\n        return dispatch_prologue_story_fields(memory, frame)\n    elif target == 243618:\n        return dispatch_departure_story_fields(memory, frame)\n    elif target == 243622:\n        return dispatch_arrival_story_fields(memory, frame)\n    elif target == 243626:\n        return dispatch_finale_story_fields(memory, frame)\n    elif target == 243630:\n        return dispatch_interlude_story_fields(memory, frame)\n    elif target == 243644:\n        return initialize_prologue_story_fields(memory, frame)\n    elif target == 243648:\n        return reveal_prologue_caption_fields(memory, frame)\n    elif target == 243652:\n        return wait_prologue_portrait_fields(memory, frame)\n    elif target == 243656:\n        return confirm_prologue_first_page_fields(memory, frame)\n    elif target == 243660:\n        return wait_prologue_second_page_fields(memory, frame)\n    elif target == 243664:\n        return reveal_prologue_second_portrait_fields(memory, frame)\n    elif target == 243668:\n        return confirm_prologue_second_page_fields(memory, frame)\n    elif target == 243672:\n        return begin_prologue_closing_caption_fields(memory, frame)\n    elif target == 243676:\n        return finish_prologue_closing_caption_fields(memory, frame)\n    elif target == 243680:\n        return confirm_prologue_exit_fields(memory, frame)\n    elif target == 243920:\n        return draw_prologue_portrait_fields(memory, frame)\n    elif target == 244400:\n        return animate_prologue_portrait_fields(memory, frame)\n    elif target == 244454:\n        return cycle_prologue_colors_fields(memory, frame)\n    elif target == 244674:\n        return select_prologue_sprite_fields(memory, frame)\n    elif target == 246172:\n        return initialize_departure_story_fields(memory, frame)\n    elif target == 246176:\n        return reveal_departure_caption_fields(memory, frame)\n    elif target == 246180:\n        return confirm_departure_first_page_fields(memory, frame)\n    elif target == 246184:\n        return wait_departure_second_page_fields(memory, frame)\n    elif target == 246188:\n        return confirm_departure_second_page_fields(memory, frame)\n    elif target == 246192:\n        return begin_departure_closing_caption_fields(memory, frame)\n    elif target == 246196:\n        return finish_departure_closing_caption_fields(memory, frame)\n    elif target == 246200:\n        return confirm_departure_exit_fields(memory, frame)\n    elif target == 246330:\n        return load_departure_tile_rows_fields(memory, frame)\n    elif target == 246402:\n        return write_departure_tile_row_fields(memory, frame)\n    elif target == 246692:\n        return animate_departure_three_layers_fields(memory, frame)\n    elif target == 246942:\n        return animate_departure_transition_fields(memory, frame)\n    elif target == 247238:\n        return animate_departure_closing_layers_fields(memory, frame)\n    elif target == 247500:\n        return select_departure_sprite_fields(memory, frame)\n    elif target == 248186:\n        return initialize_interlude_story_fields(memory, frame)\n    elif target == 248190:\n        return reveal_interlude_caption_fields(memory, frame)\n    elif target == 248194:\n        return confirm_interlude_exit_fields(memory, frame)\n    elif target == 248484:\n        return initialize_arrival_story_fields(memory, frame)\n    elif target == 248488:\n        return reveal_arrival_caption_fields(memory, frame)\n    elif target == 248492:\n        return confirm_arrival_first_page_fields(memory, frame)\n    elif target == 248496:\n        return wait_arrival_second_page_fields(memory, frame)\n    elif target == 248500:\n        return confirm_arrival_second_page_fields(memory, frame)\n    elif target == 248504:\n        return begin_arrival_closing_caption_fields(memory, frame)\n    elif target == 248508:\n        return finish_arrival_closing_caption_fields(memory, frame)\n    elif target == 248512:\n        return confirm_arrival_exit_fields(memory, frame)\n    elif target == 248766:\n        return animate_arrival_portrait_fields(memory, frame)\n    elif target == 248962:\n        return animate_arrival_zoom_fields(memory, frame)\n    elif target == 249240:\n        return animate_arrival_closing_portrait_fields(memory, frame)\n    elif target == 249352:\n        return select_arrival_sprite_fields(memory, frame)\n    elif target == 250236:\n        return initialize_finale_story_fields(memory, frame)\n    elif target == 250240:\n        return reveal_finale_caption_fields(memory, frame)\n    elif target == 250244:\n        return confirm_finale_first_page_fields(memory, frame)\n    elif target == 250248:\n        return wait_finale_scroll_fields(memory, frame)\n    elif target == 250252:\n        return advance_finale_scroll_fields(memory, frame)\n    elif target == 250256:\n        return finish_finale_closing_caption_fields(memory, frame)\n    elif target == 250260:\n        return confirm_finale_exit_fields(memory, frame)\n    elif target == 250496:\n        return animate_finale_portrait_fields(memory, frame)\n    elif target == 250694:\n        return move_finale_actor_diagonally_fields(memory, frame)\n    elif target == 250908:\n        return animate_finale_closing_portrait_fields(memory, frame)\n    elif target == 250972:\n        return select_finale_sprite_fields(memory, frame)\n    elif target == 250976:\n        return select_finale_sprite_with_attributes_fields(memory, frame)\n    elif target == 262058:\n        return advance_story_text_stream_fields(memory, frame)\n    elif target == 262398:\n        return append_story_officer_number_fields(memory, frame)\n    elif target == 262526:\n        return append_story_counter_pair_fields(memory, frame)\n    elif target == 262670:\n        return append_story_counter_triple_fields(memory, frame)\n    elif target == 240160:\n        return begin_scene_palette_darken_fields(memory, frame)\n    elif target == 240184:\n        from ..high_level_dynamic_flows.business_early_phase import begin_scene_palette_lighten_fields\n        return begin_scene_palette_lighten_fields(memory, frame)\n    elif target == 240334:\n        return read_vdp_plane_rle_rows_fields(memory, frame)\n    elif target == 242352:\n        return set_vram_write_address_fields(memory, frame)\n    elif target == 240532:\n        return copy_scene_palette_variant_fields(memory, frame)\n    elif target == 44682:\n        return decode_glyph_rows_to_buffers_fields(memory, frame)\n    elif target == 242392:\n        from ..high_level_dynamic_flows.business_early_phase import encode_six_decimal_digits_fields\n        return encode_six_decimal_digits_fields(memory, frame)\n    if target == 262850:\n        from ..high_level_dynamic_flows.business_actions import upload_object_officer_name_frame_fields\n        return upload_object_officer_name_frame_fields(memory.state, frame)\n    if target == 0x3AAC2:\n        from ..high_level_main_flows.business_scene_support import decode_high_plane_rows_fields\n        return decode_high_plane_rows_fields(memory.state, frame)\n    raise SceneRefreshBoundary(target, frame, None)\n',
           '_story_lighten_fields': 'def _story_lighten_fields(memory: SceneRefreshMemory, frame: '
                                    'FirstDeploymentFrame, continuation: Long) -> FirstDeploymentFrame:\n'
                                    "    frame = _story_move_fields(memory, frame, 'target_x', 1, 32)\n"
                                    '    return _story_call_fields(memory, frame, 240184, continuation)',
           '_story_mask_fields': 'def _story_mask_fields(memory: SceneRefreshMemory, frame: '
                                 'FirstDeploymentFrame, name, mask: Word, width: Word=16) -> '
                                 'FirstDeploymentFrame:\n'
                                 '    return _story_move_fields(memory, frame, name, frame.carrier(name) & '
                                 'mask & (1 << width) - 1, width)',
           '_story_move_fields': 'def _story_move_fields(memory: SceneRefreshMemory, frame: '
                                 'FirstDeploymentFrame, name, value: Long, width: Word=16) -> '
                                 'FirstDeploymentFrame:\n'
                                 '    """Reuse the unique width-aware MOVE implementation; retain unseen '
                                 'high bits."""\n'
                                 '    from ..high_level_dynamic_flows.business_early_phase import '
                                 '_allocation_move_fields\n'
                                 '    return _allocation_move_fields(memory, frame, name, value, width)',
           '_story_palette_masks_fields': 'def _story_palette_masks_fields(memory: SceneRefreshMemory, '
                                          'frame: FirstDeploymentFrame, masks: tuple) -> '
                                          'FirstDeploymentFrame:\n'
                                          '    if len(masks) != 4:\n'
                                          "        raise ValueError('four original palette masks required')\n"
                                          '    for index, value in enumerate(masks):\n'
                                          '        frame = _story_store_fields(memory, frame, 4294934730 + '
                                          'index * 2, value)\n'
                                          '    return frame',
           '_story_pressed_fields': 'def _story_pressed_fields(memory: SceneRefreshMemory, frame: '
                                    'FirstDeploymentFrame) -> tuple:\n'
                                    '    value = _story_read_fields(memory, frame, 4294934724, 1)\n'
                                    '    return (_scene_render_bit(memory, frame, value, 128), bool(value & '
                                    '128))',
           '_story_ram_move_fields': 'def _story_ram_move_fields(memory: SceneRefreshMemory, frame: '
                                     'FirstDeploymentFrame, name, low: Word, width: Word=16) -> '
                                     'FirstDeploymentFrame:\n'
                                     '    return _story_move_fields(memory, frame, name, '
                                     '_story_read_fields(memory, frame, 4294901760 | low, width // 8), '
                                     'width)',
           '_story_read_fields': 'def _story_read_fields(memory: SceneRefreshMemory, frame: '
                                 'FirstDeploymentFrame, address: Long, size: Word=2):\n'
                                 '    memory.sync_status(frame)\n'
                                 '    return memory.state.read(address, size)',
           '_story_rising_layer_fields': 'def _story_rising_layer_fields(memory: SceneRefreshMemory, frame: '
                                         'FirstDeploymentFrame, counter: Word, sampled_counter: Word, shift: '
                                         'Word, baseline: Word, tile: Word, attributes: Word, continuation: '
                                         'Long) -> FirstDeploymentFrame:\n'
                                         '    frame = _story_add_ram_fields(memory, frame, counter)\n'
                                         "    frame = _story_ram_move_fields(memory, frame, 'unit', "
                                         'sampled_counter)\n'
                                         "    frame = _scene_mode_lsr_word(memory, frame, 'unit', "
                                         'low16(frame.unit), shift)\n'
                                         "    frame = _story_move_fields(memory, frame, 'target_y', "
                                         'baseline)\n'
                                         "    frame = _story_arithmetic_fields(memory, frame, 'target_y', "
                                         'low16(frame.unit), True)\n'
                                         "    frame = _story_move_fields(memory, frame, 'target_x', 128)\n"
                                         "    frame = _story_move_fields(memory, frame, 'unit', tile)\n"
                                         "    frame = _story_move_fields(memory, frame, 'distance', "
                                         'attributes)\n'
                                         '    return _story_call_fields(memory, frame, 247500, continuation)',
           '_story_script_fields': 'def _story_script_fields(memory: SceneRefreshMemory, frame: '
                                   'FirstDeploymentFrame, source: Long, dimensions: bool=False) -> '
                                   'FirstDeploymentFrame:\n'
                                   '    frame = _story_store_fields(memory, frame, 16740364, 40960)\n'
                                   '    frame = _story_store_fields(memory, frame, 16740366, source, 4)\n'
                                   '    if dimensions:\n'
                                   '        frame = _story_store_fields(memory, frame, 16740372, 3)\n'
                                   '        frame = _story_store_fields(memory, frame, 16740374, 1)\n'
                                   '    return frame',
           '_story_select_sprite_fields': 'def _story_select_sprite_fields(memory: SceneRefreshMemory, '
                                          'frame: FirstDeploymentFrame, directory: Long, attributes: Word | '
                                          'None) -> FirstDeploymentFrame:\n'
                                          '    """Read the live template LONG and tail into the sole 3B13C '
                                          'packet algorithm."""\n'
                                          '    from .business_objects import _append_object_sprite_fields\n'
                                          "    frame = _scene_render_asl_word(memory, frame, 'unit', "
                                          'low16(frame.unit), 2)\n'
                                          '    address = directory + s16(low16(frame.unit))\n'
                                          '    frame = first_replace(frame, '
                                          'roster=memory.cursor_at(_story_read_fields(memory, frame, '
                                          'address, 4)))\n'
                                          "    frame = _story_move_fields(memory, frame, 'unit', 5)\n"
                                          "    frame = _story_move_fields(memory, frame, 'count', 0, 32)\n"
                                          '    if attributes is not None:\n'
                                          "        frame = _story_move_fields(memory, frame, 'distance', "
                                          'attributes)\n'
                                          '    return _append_object_sprite_fields(memory, frame)',
           '_story_status_fields': 'def _story_status_fields(memory: SceneRefreshMemory, frame: '
                                   'FirstDeploymentFrame, value: Word) -> FirstDeploymentFrame:\n'
                                   '    memory.state.set_status_word(value)\n'
                                   '    return first_replace(frame, status=value & 31)',
           '_story_store_fields': 'def _story_store_fields(memory: SceneRefreshMemory, frame: '
                                  'FirstDeploymentFrame, address: Long, value: Long, size: Word=2) -> '
                                  'FirstDeploymentFrame:\n'
                                  '    """Do not normalize bus literals: original abs.W and abs.L are '
                                  'distinct events."""\n'
                                  '    return _scene_refresh_emit(memory, frame, address, size, value)',
           '_story_text_dimensions_fields': 'def _story_text_dimensions_fields(memory: SceneRefreshMemory, '
                                            'frame: FirstDeploymentFrame, characters: Word, continuation: '
                                            'Long) -> FirstDeploymentFrame:\n'
                                            "    frame = _story_move_fields(memory, frame, 'target_x', "
                                            '_story_read_fields(memory, frame, 16740372))\n'
                                            "    frame = _story_move_fields(memory, frame, 'target_y', "
                                            '_story_read_fields(memory, frame, 16740374))\n'
                                            "    frame = _story_move_fields(memory, frame, 'count', "
                                            'characters)\n'
                                            '    return _story_call_fields(memory, frame, 44682, '
                                            'continuation)',
           '_story_text_tile_fields': 'def _story_text_tile_fields(memory: SceneRefreshMemory, frame: '
                                      'FirstDeploymentFrame, advance: Word) -> FirstDeploymentFrame:\n'
                                      "    frame = _story_move_fields(memory, frame, 'unit', "
                                      '_story_read_fields(memory, frame, 16740364))\n'
                                      "    return _story_arithmetic_fields(memory, frame, 'unit', advance)",
           '_story_timer_fields': 'def _story_timer_fields(memory: SceneRefreshMemory, frame: '
                                  'FirstDeploymentFrame, threshold: Word, masks: tuple | None, fade_return: '
                                  'Long | None, source: Long | None, counters: tuple) -> '
                                  'FirstDeploymentFrame:\n'
                                  '    """The common timed transition, preserving real comparisons and '
                                  'source-write order."""\n'
                                  '    frame = _story_add_ram_fields(memory, frame, 33082)\n'
                                  '    frame = _story_compare_ram_fields(memory, frame, 33082, threshold)\n'
                                  '    if frame.status & 1:\n'
                                  '        return frame\n'
                                  '    if masks is not None:\n'
                                  '        frame = _story_palette_masks_fields(memory, frame, masks)\n'
                                  '    if fade_return is not None:\n'
                                  '        frame = _story_lighten_fields(memory, frame, fade_return)\n'
                                  '    if source is not None:\n'
                                  '        frame = _story_status_fields(memory, frame, 9984)\n'
                                  '        frame = _story_clear_plane_fields(memory, frame)\n'
                                  '        frame = _story_script_fields(memory, frame, source)\n'
                                  '        frame = _story_status_fields(memory, frame, 9472)\n'
                                  '    return _story_finish_stage_fields(memory, frame, counters)',
           '_story_upload_current_rows_fields': 'def _story_upload_current_rows_fields(memory: '
                                                'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                'FirstDeploymentFrame:\n'
                                                '    while True:\n'
                                                '        value = _story_read_fields(memory, frame, '
                                                'frame.roster.base, 4)\n'
                                                '        frame = first_replace(frame, '
                                                'roster=frame.roster.advance(4))\n'
                                                '        frame = _story_store_fields(memory, frame, '
                                                'frame.auxiliary.base, value, 4)\n'
                                                '        counter = u16(low16(frame.target_x) - 1)\n'
                                                '        frame = first_replace(frame, '
                                                'target_x=replace_word(frame.target_x, counter))\n'
                                                '        if counter == 65535:\n'
                                                '            return frame',
           'advance_finale_scroll_fields': 'def advance_finale_scroll_fields(memory: SceneRefreshMemory, '
                                           'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                           '    """Original 3D18C complete story role; BRA prefixes add no '
                                           'slot."""\n'
                                           '    memory.frame(frame)\n'
                                           '    frame = _story_call_fields(memory, frame, 250908, 250742)\n'
                                           '    for low in (32800, 32806):\n'
                                           '        frame = _story_add_ram_fields(memory, frame, low)\n'
                                           '    for low in (32800, 32806):\n'
                                           '        value = _story_read_fields(memory, frame, 4294901760 | '
                                           'low) & 511\n'
                                           '        frame = _story_store_fields(memory, frame, 4294901760 | '
                                           'low, value)\n'
                                           '    frame = _story_compare_ram_fields(memory, frame, 32806, '
                                           '256)\n'
                                           '    if not frame.status & 5:\n'
                                           '        return frame\n'
                                           '    frame = _story_compare_ram_fields(memory, frame, 32806, '
                                           '112)\n'
                                           '    if frame.status & 1:\n'
                                           '        return frame\n'
                                           '    frame = _story_finish_stage_fields(memory, frame)\n'
                                           '    frame = _story_status_fields(memory, frame, 9984)\n'
                                           '    frame = _story_clear_plane_fields(memory, frame)\n'
                                           '    frame = _story_script_fields(memory, frame, 243406)\n'
                                           '    return _story_status_fields(memory, frame, 9472)',
           'advance_scene_palette_fade_fields': 'def advance_scene_palette_fade_fields(memory: '
                                                'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                'FirstDeploymentFrame:\n'
                                                '    """3A978: two live 32-color masks, real BSR slots, no '
                                                'fabricated color highs."""\n'
                                                '    from ..high_level_gameplay_flow.business_battle import '
                                                '_presentation_call_fields\n'
                                                '    from ..high_level_gameplay_flow.contexts_battle import '
                                                'BattlePresentationMemory\n'
                                                '    from .business_objects import '
                                                '_object_adjust_word_fields\n'
                                                '    memory.frame(frame)\n'
                                                '    memory.sync_status(frame)\n'
                                                '    mode = memory.state.read(4294934724, 2)\n'
                                                "    frame = _first_word(frame, 'target_x', mode)\n"
                                                '    if mode & 32768:\n'
                                                '        return frame\n'
                                                '    frame = _object_adjust_word_fields(memory, frame, '
                                                '4294934726, 1, True)\n'
                                                '    if not frame.status & 8:\n'
                                                '        return frame\n'
                                                '    period = mode & 255\n'
                                                "    frame = _first_word(frame, 'target_x', period)\n"
                                                '    frame = _scene_refresh_emit(memory, frame, 4294934726, '
                                                '2, period)\n'
                                                '    mode_byte = memory.state.read(4294934724, 1)\n'
                                                '    frame = _scene_render_compare(memory, frame, mode_byte, '
                                                '0, 8)\n'
                                                '    if mode_byte == 0:\n'
                                                '        frame = _object_adjust_word_fields(memory, frame, '
                                                '4294934728, 1, True)\n'
                                                '        finished = bool(frame.status & 8)\n'
                                                '    else:\n'
                                                '        frame = _object_adjust_word_fields(memory, frame, '
                                                '4294934728, 1)\n'
                                                '        shade = memory.state.read(4294934728, 2)\n'
                                                '        frame = _scene_render_compare(memory, frame, shade, '
                                                '15, 16)\n'
                                                '        finished = shade > 15\n'
                                                '    if finished:\n'
                                                '        return _scene_refresh_emit(memory, frame, '
                                                '4294934724, 2, 65535)\n'
                                                '    shade = memory.state.read(4294934728, 2)\n'
                                                "    frame = _first_word(frame, 'target_x', shade)\n"
                                                "    frame = _first_word(frame, 'target_x', shade & 14)\n"
                                                '    frame = _scene_refresh_emit(memory, frame, 4294934528, '
                                                '2, low16(frame.target_x))\n'
                                                '    frame = first_replace(frame, '
                                                'roster=memory.cursor_at(4294966016), '
                                                'candidates=memory.cursor_at(4294966144), '
                                                'controller=memory.cursor_at(4294934730))\n'
                                                "    frame = _first_long(frame, 'unit', 0)\n"
                                                "    frame = _first_long(frame, 'choice', 0)\n"
                                                '    while True:\n'
                                                "        frame = _first_long(frame, 'target_y', 31)\n"
                                                "        frame = _first_long(frame, 'offset_y', "
                                                'frame.controller.long(low16(frame.choice)))\n'
                                                '        while True:\n'
                                                '            mask = frame.offset_y\n'
                                                '            frame = first_replace(frame, offset_y=mask >> '
                                                '1, status=(17 if mask & 1 else 0) | (4 if mask >> 1 == 0 '
                                                'else 0))\n'
                                                '            memory.sync_status(frame)\n'
                                                '            if mask & 1:\n'
                                                "                frame = _first_word(frame, 'offset_x', 0)\n"
                                                "                frame = _first_word(frame, 'count', "
                                                'frame.candidates.word(low16(frame.unit)))\n'
                                                '                if frame.stack_cursor is None or any((value '
                                                'is None for value in (frame.count, frame.distance, '
                                                'frame.offset_x))):\n'
                                                '                    raise SceneRefreshBoundary(240138, '
                                                'frame, 240108)\n'
                                                '                for continuation in (240108, 240112, '
                                                '240116):\n'
                                                '\n'
                                                '                    def component(actual_memory, entered):\n'
                                                '                        return '
                                                'fade_palette_component_fields(SceneRefreshMemory(actual_memory.state), '
                                                'entered)\n'
                                                '                    frame = '
                                                '_presentation_call_fields(BattlePresentationMemory(memory.state), '
                                                'frame, continuation, component)\n'
                                                '                frame = '
                                                "_scene_fade_rotate_word_fields(memory, frame, 'offset_x', "
                                                '4)\n'
                                                '                frame = _scene_refresh_emit(memory, frame, '
                                                'u32(frame.roster.base + s16(low16(frame.unit))), 2, '
                                                'low16(frame.offset_x))\n'
                                                '            frame = _scene_render_arithmetic(memory, frame, '
                                                "'unit', low16(frame.unit), 2, 16)\n"
                                                '            frame = _scene_refresh_decrement(frame, '
                                                "'target_y', low16(frame.target_y))\n"
                                                '            if low16(frame.target_y) == 65535:\n'
                                                '                break\n'
                                                '        frame = _scene_render_arithmetic(memory, frame, '
                                                "'choice', low16(frame.choice), 4, 16)\n"
                                                '        frame = _scene_render_compare(memory, frame, '
                                                'low16(frame.choice), 8, 16)\n'
                                                '        if low16(frame.choice) >= 8:\n'
                                                '            return memory.sync_status(frame)',
           'advance_story_text_stream_fields': 'def advance_story_text_stream_fields(memory: '
                                               'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                               'FirstDeploymentFrame:\n'
                                               '    """Live text token parsing, name/number rendering and '
                                               'exact stream advancement."""\n'
                                               '    memory.frame(frame)\n'
                                               '    frame = _story_ram_move_fields(memory, frame, '
                                               "'target_y', 61400)\n"
                                               '    frame = _story_ram_move_fields(memory, frame, '
                                               "'target_x', 62240)\n"
                                               '    mask = _story_read_fields(memory, frame, 262054 + '
                                               's16(low16(frame.target_y)), 1)\n'
                                               "    frame = _story_mask_fields(memory, frame, 'target_x', "
                                               'mask, 8)\n'
                                               '    if not frame.status & 4:\n'
                                               '        return frame\n'
                                               '    value = _story_read_fields(memory, frame, 16740364)\n'
                                               '    frame = _scene_refresh_flags(memory, frame, value, 2)\n'
                                               '    if frame.status & 4:\n'
                                               '        return frame\n'
                                               "    frame = _story_move_fields(memory, frame, 'target_x', "
                                               '_story_read_fields(memory, frame, 16740364))\n'
                                               '    frame = _story_call_fields(memory, frame, 242352, '
                                               '262094)\n'
                                               '    frame = first_replace(frame, '
                                               'roster=memory.cursor_at(_story_read_fields(memory, frame, '
                                               '16740366, 4)))\n'
                                               "    frame = _story_move_fields(memory, frame, 'target_x', "
                                               '_story_read_fields(memory, frame, frame.roster.base))\n'
                                               "    frame = _story_mask_fields(memory, frame, 'target_x', "
                                               '49151)\n'
                                               '    special = False\n'
                                               '    for token, selected, alternate in ((32776, 32992, '
                                               '32994), (32782, 32988, 32990), (32778, 32994, 32992), '
                                               '(65283, 32990, 32988)):\n'
                                               '        frame = _story_ram_move_fields(memory, frame, '
                                               "'choice', selected)\n"
                                               '        frame = _story_ram_move_fields(memory, frame, '
                                               "'offset_y', alternate)\n"
                                               '        frame = _scene_render_compare(memory, frame, '
                                               'low16(frame.target_x), token, 16)\n'
                                               '        if frame.status & 4:\n'
                                               '            special = True\n'
                                               '            break\n'
                                               '    scan_following = True\n'
                                               '    if special:\n'
                                               '        value = _story_read_fields(memory, frame, '
                                               '4294934806)\n'
                                               '        frame = _scene_refresh_flags(memory, frame, value, '
                                               '2)\n'
                                               '        if not frame.status & 4:\n'
                                               '            frame = _story_move_fields(memory, frame, '
                                               "'choice', low16(frame.offset_y))\n"
                                               '        frame = _story_move_fields(memory, frame, '
                                               "'target_x', _story_read_fields(memory, frame, 16740372))\n"
                                               '        frame = _story_move_fields(memory, frame, '
                                               "'target_y', _story_read_fields(memory, frame, 16740374))\n"
                                               '        frame = _story_call_fields(memory, frame, 262850, '
                                               '262188)\n'
                                               '        frame = _story_text_tile_fields(memory, frame, 384)\n'
                                               '    else:\n'
                                               "        frame = _story_move_fields(memory, frame, 'unit', "
                                               '_story_read_fields(memory, frame, 16740364))\n'
                                               '        frame = _scene_render_bit(memory, frame, '
                                               'frame.target_x, 32768)\n'
                                               '        if not frame.status & 4:\n'
                                               '            scan_following = False\n'
                                               '        else:\n'
                                               '            frame = first_replace(frame, '
                                               'candidates=memory.cursor_at(4294955776))\n'
                                               '            frame = _story_text_dimensions_fields(memory, '
                                               'frame, 0, 262240)\n'
                                               '            frame = first_replace(frame, '
                                               'roster=memory.cursor_at(4294955776))\n'
                                               '            frame = _story_glyph_upload_fields(memory, '
                                               'frame, 31)\n'
                                               '            frame = _story_text_tile_fields(memory, frame, '
                                               '128)\n'
                                               '    if scan_following:\n'
                                               '        frame = first_replace(frame, '
                                               'roster=memory.cursor_at(_story_read_fields(memory, frame, '
                                               '16740366, 4)).advance(2))\n'
                                               '        frame = _story_move_fields(memory, frame, '
                                               "'target_x', _story_read_fields(memory, frame, "
                                               'frame.roster.base))\n'
                                               '    if not scan_following or frame.status & 8:\n'
                                               '        frame = _scene_render_compare(memory, frame, '
                                               'low16(frame.target_x), 65312, 16)\n'
                                               '        if frame.status & 4:\n'
                                               '            frame = _story_arithmetic_fields(memory, frame, '
                                               "'unit', 64)\n"
                                               '            frame = first_replace(frame, '
                                               'roster=frame.roster.advance(2))\n'
                                               '        else:\n'
                                               '            frame = _scene_render_compare(memory, frame, '
                                               'low16(frame.target_x), 32770, 16)\n'
                                               '            if frame.status & 4:\n'
                                               '                frame = first_replace(frame, '
                                               'roster=frame.roster.advance(2))\n'
                                               '                frame = _story_move_fields(memory, frame, '
                                               "'target_x', low16(frame.unit))\n"
                                               '                frame = _story_move_fields(memory, frame, '
                                               "'unit', 43264)\n"
                                               '                frame = _scene_render_compare(memory, frame, '
                                               'low16(frame.target_x), 43264, 16)\n'
                                               '                if not frame.status & 1:\n'
                                               '                    frame = _story_move_fields(memory, '
                                               "frame, 'unit', 45568)\n"
                                               '            else:\n'
                                               '                frame = _scene_render_compare(memory, frame, '
                                               'low16(frame.target_x), 32784, 16)\n'
                                               '                if frame.status & 4:\n'
                                               '                    frame = _story_call_fields(memory, '
                                               'frame, 262398, 262340)\n'
                                               '                else:\n'
                                               '                    frame = _scene_render_compare(memory, '
                                               'frame, low16(frame.target_x), 32785, 16)\n'
                                               '                    if frame.status & 4:\n'
                                               '                        frame = first_replace(frame, '
                                               'roster=frame.roster.advance(2))\n'
                                               '                        frame = _story_call_fields(memory, '
                                               'frame, 262526, 262356)\n'
                                               '                    else:\n'
                                               '                        frame = '
                                               '_scene_render_compare(memory, frame, low16(frame.target_x), '
                                               '32786, 16)\n'
                                               '                        if frame.status & 4:\n'
                                               '                            frame = first_replace(frame, '
                                               'roster=frame.roster.advance(2))\n'
                                               '                            frame = '
                                               '_story_call_fields(memory, frame, 262670, 262372)\n'
                                               '                        else:\n'
                                               '                            frame = '
                                               '_scene_render_compare(memory, frame, low16(frame.target_x), '
                                               '32768, 16)\n'
                                               '                            if frame.status & 4:\n'
                                               '                                frame = '
                                               "_story_move_fields(memory, frame, 'unit', 0)\n"
                                               '    return _story_finish_text_stream_fields(memory, frame)',
           'animate_arrival_closing_portrait_fields': 'def animate_arrival_closing_portrait_fields(memory: '
                                                      'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                      'FirstDeploymentFrame:\n'
                                                      '    memory.frame(frame)\n'
                                                      '    frame = _story_animation_index_fields(memory, '
                                                      'frame, 33084, 5, 2, True)\n'
                                                      '    frame = _story_arithmetic_fields(memory, frame, '
                                                      "'unit', 5)\n"
                                                      '    return _story_draw_pose_fields(memory, frame, '
                                                      '128, 196, 249352, 249276)',
           'animate_arrival_portrait_fields': 'def animate_arrival_portrait_fields(memory: '
                                              'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                              'FirstDeploymentFrame:\n'
                                              '    memory.frame(frame)\n'
                                              '    frame = _story_animation_index_fields(memory, frame, '
                                              '33084, 5, 3, True)\n'
                                              '    return _story_draw_pose_fields(memory, frame, 128, 192, '
                                              '249352, 248800)',
           'animate_arrival_zoom_fields': 'def animate_arrival_zoom_fields(memory: SceneRefreshMemory, '
                                          'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                          '    memory.frame(frame)\n'
                                          '    frame = _story_add_ram_fields(memory, frame, 33084)\n'
                                          "    frame = _story_ram_move_fields(memory, frame, 'unit', 33084)\n"
                                          "    frame = _scene_mode_lsr_word(memory, frame, 'unit', "
                                          'low16(frame.unit), 5)\n'
                                          "    frame = _story_move_fields(memory, frame, 'target_x', 128)\n"
                                          "    frame = _story_move_fields(memory, frame, 'target_y', 192)\n"
                                          "    frame = _story_arithmetic_fields(memory, frame, 'target_x', "
                                          'low16(frame.unit), True)\n'
                                          "    frame = _story_arithmetic_fields(memory, frame, 'target_y', "
                                          'low16(frame.unit), True)\n'
                                          "    frame = _story_move_fields(memory, frame, 'unit', 4, 32)\n"
                                          '    frame = _story_call_fields(memory, frame, 249352, 248990)\n'
                                          "    frame = _story_move_fields(memory, frame, 'target_x', 128)\n"
                                          "    frame = _story_move_fields(memory, frame, 'target_y', 192)\n"
                                          "    frame = _story_move_fields(memory, frame, 'unit', 8, 32)\n"
                                          '    return _story_call_fields(memory, frame, 249352, 249004)',
           'animate_departure_closing_layers_fields': 'def animate_departure_closing_layers_fields(memory: '
                                                      'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                      'FirstDeploymentFrame:\n'
                                                      '    memory.frame(frame)\n'
                                                      '    frame = _story_ram_move_fields(memory, frame, '
                                                      "'unit', 33092)\n"
                                                      '    frame = _scene_mode_lsr_word(memory, frame, '
                                                      "'unit', low16(frame.unit), 3)\n"
                                                      '    frame = _story_move_fields(memory, frame, '
                                                      "'target_y', 224)\n"
                                                      '    frame = _story_arithmetic_fields(memory, frame, '
                                                      "'target_y', low16(frame.unit), True)\n"
                                                      '    frame = _scene_render_compare(memory, frame, '
                                                      'low16(frame.target_y), 192, 16)\n'
                                                      '    if frame.status & 5:\n'
                                                      '        frame = _story_move_fields(memory, frame, '
                                                      "'target_y', 192)\n"
                                                      '    else:\n'
                                                      '        frame = _story_add_ram_fields(memory, frame, '
                                                      '33092)\n'
                                                      '    frame = _story_move_fields(memory, frame, '
                                                      "'target_x', 128)\n"
                                                      "    frame = _story_move_fields(memory, frame, 'unit', "
                                                      '13)\n'
                                                      '    frame = _story_move_fields(memory, frame, '
                                                      "'distance', 256)\n"
                                                      '    frame = _story_call_fields(memory, frame, 247500, '
                                                      '247282)\n'
                                                      '    frame = _story_ram_move_fields(memory, frame, '
                                                      "'target_y', 33090)\n"
                                                      '    frame = _scene_mode_lsr_word(memory, frame, '
                                                      "'target_y', low16(frame.target_y), 3)\n"
                                                      '    frame = _story_arithmetic_fields(memory, frame, '
                                                      "'target_y', 160)\n"
                                                      '    frame = _scene_render_compare(memory, frame, '
                                                      'low16(frame.target_y), 192, 16)\n'
                                                      '    if not frame.status & 1:\n'
                                                      '        frame = _story_move_fields(memory, frame, '
                                                      "'target_y', 192)\n"
                                                      '    else:\n'
                                                      '        frame = _story_add_ram_fields(memory, frame, '
                                                      '33090)\n'
                                                      '    frame = _story_move_fields(memory, frame, '
                                                      "'target_x', 128)\n"
                                                      "    frame = _story_move_fields(memory, frame, 'unit', "
                                                      '12)\n'
                                                      '    frame = _story_move_fields(memory, frame, '
                                                      "'distance', 512)\n"
                                                      '    frame = _story_call_fields(memory, frame, 247500, '
                                                      '247324)\n'
                                                      '    frame = _story_rising_layer_fields(memory, frame, '
                                                      '33084, 33084, 6, 192, 9, 512, 247356)\n'
                                                      '    frame = _story_rising_layer_fields(memory, frame, '
                                                      '33086, 33086, 5, 192, 10, 512, 247388)\n'
                                                      '    return _story_rising_layer_fields(memory, frame, '
                                                      '33088, 33088, 4, 192, 11, 512, 247420)',
           'animate_departure_three_layers_fields': 'def animate_departure_three_layers_fields(memory: '
                                                    'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                    'FirstDeploymentFrame:\n'
                                                    '    """Original layers all sample 813C, including the '
                                                    'latter two; do not repair it."""\n'
                                                    '    memory.frame(frame)\n'
                                                    '    frame = _story_rising_layer_fields(memory, frame, '
                                                    '33084, 33084, 6, 176, 0, 512, 246724)\n'
                                                    '    frame = _story_rising_layer_fields(memory, frame, '
                                                    '33086, 33084, 5, 176, 1, 512, 246756)\n'
                                                    '    return _story_rising_layer_fields(memory, frame, '
                                                    '33088, 33084, 4, 176, 2, 512, 246788)',
           'animate_departure_transition_fields': 'def animate_departure_transition_fields(memory: '
                                                  'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                  'FirstDeploymentFrame:\n'
                                                  '    memory.frame(frame)\n'
                                                  '    frame = _story_animation_index_fields(memory, frame, '
                                                  '33084, 5, 5, True)\n'
                                                  '    frame = _story_arithmetic_fields(memory, frame, '
                                                  "'unit', 3)\n"
                                                  '    return _story_draw_pose_fields(memory, frame, 128, '
                                                  '192, 247500, 246982, 256)',
           'animate_finale_closing_portrait_fields': 'def animate_finale_closing_portrait_fields(memory: '
                                                     'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                     'FirstDeploymentFrame:\n'
                                                     '    memory.frame(frame)\n'
                                                     '    frame = _story_add_ram_fields(memory, frame, '
                                                     '33084)\n'
                                                     '    frame = _story_ram_move_fields(memory, frame, '
                                                     "'unit', 33084)\n"
                                                     '    frame = _scene_mode_lsr_word(memory, frame, '
                                                     "'unit', low16(frame.unit), 4)\n"
                                                     '    frame = _scene_render_compare(memory, frame, '
                                                     'low16(frame.unit), 1, 16)\n'
                                                     '    if not frame.status & 5:\n'
                                                     '        frame = _story_move_fields(memory, frame, '
                                                     "'unit', 0, 32)\n"
                                                     '        frame = _story_clear_fields(memory, frame, '
                                                     '33084)\n'
                                                     '    frame = _story_arithmetic_fields(memory, frame, '
                                                     "'unit', 5)\n"
                                                     '    frame = _story_move_fields(memory, frame, '
                                                     "'target_x', 192)\n"
                                                     '    frame = _story_move_fields(memory, frame, '
                                                     "'target_y', 192)\n"
                                                     '    frame = _story_move_fields(memory, frame, '
                                                     "'distance', 512)\n"
                                                     '    return _story_call_fields(memory, frame, 250976, '
                                                     '250948)',
           'animate_finale_portrait_fields': 'def animate_finale_portrait_fields(memory: SceneRefreshMemory, '
                                             'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                             '    memory.frame(frame)\n'
                                             '    frame = _story_animation_index_fields(memory, frame, '
                                             '33084, 5, 3, False, True)\n'
                                             '    return _story_draw_pose_fields(memory, frame, 128, 192, '
                                             '250972, 250526)',
           'animate_prologue_portrait_fields': 'def animate_prologue_portrait_fields(memory: '
                                               'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                               'FirstDeploymentFrame:\n'
                                               '    memory.frame(frame)\n'
                                               '    frame = _story_animation_index_fields(memory, frame, '
                                               '33084, 5, 2, True)\n'
                                               "    frame = _story_arithmetic_fields(memory, frame, 'unit', "
                                               '9)\n'
                                               '    frame = _story_draw_pose_fields(memory, frame, 128, 192, '
                                               '244674, 244438)\n'
                                               "    frame = _story_move_fields(memory, frame, 'target_x', "
                                               '128)\n'
                                               "    frame = _story_move_fields(memory, frame, 'target_y', "
                                               '192)\n'
                                               "    frame = _story_move_fields(memory, frame, 'unit', 0, "
                                               '32)\n'
                                               '    return _story_call_fields(memory, frame, 244674, 244452)',
           'append_story_counter_pair_fields': 'def append_story_counter_pair_fields(memory: '
                                               'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                               'FirstDeploymentFrame:\n'
                                               '    memory.frame(frame)\n'
                                               '    return _story_decimal_strip_fields(memory, frame, '
                                               "'pair')",
           'append_story_counter_triple_fields': 'def append_story_counter_triple_fields(memory: '
                                                 'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                 'FirstDeploymentFrame:\n'
                                                 '    memory.frame(frame)\n'
                                                 '    return _story_decimal_strip_fields(memory, frame, '
                                                 "'triple')",
           'append_story_officer_number_fields': 'def append_story_officer_number_fields(memory: '
                                                 'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                 'FirstDeploymentFrame:\n'
                                                 '    memory.frame(frame)\n'
                                                 '    return _story_decimal_strip_fields(memory, frame, '
                                                 "'officer')",
           'begin_arrival_closing_caption_fields': 'def begin_arrival_closing_caption_fields(memory: '
                                                   'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                   'FirstDeploymentFrame:\n'
                                                   '    """Original 3CAB8 complete story role; BRA prefixes '
                                                   'add no slot."""\n'
                                                   '    memory.frame(frame)\n'
                                                   '    frame = _story_call_fields(memory, frame, 249240, '
                                                   '249154)\n'
                                                   '    return _story_timer_fields(memory, frame, 512, None, '
                                                   'None, 244626, (33082,))',
           'begin_departure_closing_caption_fields': 'def begin_departure_closing_caption_fields(memory: '
                                                     'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                     'FirstDeploymentFrame:\n'
                                                     '    """Original 3C1B0 complete story role; BRA '
                                                     'prefixes add no slot."""\n'
                                                     '    memory.frame(frame)\n'
                                                     '    frame = _story_call_fields(memory, frame, 247238, '
                                                     '247152)\n'
                                                     '    return _story_timer_fields(memory, frame, 512, '
                                                     'None, None, 244626, (33082,))',
           'begin_prologue_closing_caption_fields': 'def begin_prologue_closing_caption_fields(memory: '
                                                    'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                    'FirstDeploymentFrame:\n'
                                                    '    """Original 3B7D8 complete story role; BRA prefixes '
                                                    'add no slot."""\n'
                                                    '    memory.frame(frame)\n'
                                                    '    frame = _story_call_fields(memory, frame, 244400, '
                                                    '244310)\n'
                                                    '    frame = _story_call_fields(memory, frame, 244454, '
                                                    '244314)\n'
                                                    '    return _story_timer_fields(memory, frame, 512, '
                                                    'None, None, 244626, (33082,))',
           'begin_scene_palette_darken_fields': 'def begin_scene_palette_darken_fields(memory: '
                                                'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                'FirstDeploymentFrame:\n'
                                                '    frame, shade = '
                                                '_begin_scene_palette_darken_fields_core(memory, frame)\n'
                                                '    return frame',
           'confirm_arrival_exit_fields': 'def confirm_arrival_exit_fields(memory: SceneRefreshMemory, '
                                          'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                          '    """Original 3CAC0 complete story role; BRA prefixes add no '
                                          'slot."""\n'
                                          '    memory.frame(frame)\n'
                                          '    return _story_exit_fields(memory, frame)',
           'confirm_arrival_first_page_fields': 'def confirm_arrival_first_page_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """Original 3CAAC complete story role; BRA prefixes add no slot."""\n    memory.frame(frame)\n    frame = _story_call_fields(memory,frame,0x3CBBE,0x3CBE6)\n    frame, pressed = _story_pressed_fields(memory,frame)\n    if not pressed:\n        return frame\n    frame = _story_status_fields(memory,frame,0x2700)\n    frame = first_replace(frame,roster=memory.cursor_at(0x45AE1),\n        candidates=memory.cursor_at(0x0000E000))\n    frame = _story_move_fields(memory,frame,\'offset_x\',0x80,32)\n    frame = _story_move_fields(memory,frame,\'offset_y\',0x12)\n    frame = _story_call_fields(memory,frame,0x3AAC2,0x3CC0E)\n    frame = _story_clear_plane_fields(memory,frame)\n    frame = _story_script_fields(memory,frame,0x3B654)\n    frame = _story_status_fields(memory,frame,0x2500)\n    frame = _story_darken_fields(memory,frame,0x3CC50)\n    frame = _story_finish_stage_fields(memory,frame,(0x813A,0x813C))\n    return memory.sync_status(frame)\n',
           'confirm_arrival_second_page_fields': 'def confirm_arrival_second_page_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """Original 3CAB4 complete story role; BRA prefixes add no slot."""\n    memory.frame(frame)\n    frame = _story_call_fields(memory,frame,0x3CC82,0x3CCB2)\n    frame, pressed = _story_confirm_page_fields(memory,frame,0x45D70,0x3CCDA,0x3B684)\n    if not pressed:\n        return frame\n    frame = _story_palette_masks_fields(memory,frame,(0xFFFF,0xFFFF,0,0xFFFF))\n    frame = _story_darken_fields(memory,frame,0x3CD34)\n    frame = _story_finish_stage_fields(memory,frame,(0x813A,))\n    return memory.sync_status(frame)\n',
           'confirm_departure_exit_fields': 'def confirm_departure_exit_fields(memory: SceneRefreshMemory, '
                                            'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                            '    """Original 3C1B8 complete story role; BRA prefixes add no '
                                            'slot."""\n'
                                            '    memory.frame(frame)\n'
                                            '    frame = _story_call_fields(memory, frame, 247238, 247482)\n'
                                            '    return _story_exit_fields(memory, frame)',
           'confirm_departure_first_page_fields': 'def confirm_departure_first_page_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """Original 3C1A4 complete story role; BRA prefixes add no slot."""\n    memory.frame(frame)\n    frame = _story_call_fields(memory,frame,0x3C3A4,0x3C40A)\n    frame, pressed = _story_confirm_page_fields(memory,frame,0x46FCD,0x3C432,0x3B5B8)\n    if not pressed:\n        return frame\n    frame = _story_darken_fields(memory,frame,0x3C474)\n    frame = _story_finish_stage_fields(memory,frame,(0x813A,))\n    return memory.sync_status(frame)\n',
           'confirm_departure_second_page_fields': 'def confirm_departure_second_page_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """Original 3C1AC complete story role; BRA prefixes add no slot."""\n    memory.frame(frame)\n    frame = _story_call_fields(memory,frame,0x3C49E,0x3C4CC)\n    frame, pressed = _story_confirm_page_fields(memory,frame,0x47248,0x3C4F4,0x3B5E8)\n    if not pressed:\n        return frame\n    frame = _story_palette_masks_fields(memory,frame,(0xFFFF,0xFFFF,0,0xFFFF))\n    frame = _story_darken_fields(memory,frame,0x3C54E)\n    frame = _story_finish_stage_fields(memory,frame,(0x813A,0x813C,0x813E,0x8140,0x8142,0x8144))\n    return memory.sync_status(frame)\n',
           'confirm_finale_exit_fields': 'def confirm_finale_exit_fields(memory: SceneRefreshMemory, frame: '
                                         'FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                         '    """Original 3D194 complete story role; BRA prefixes add no '
                                         'slot."""\n'
                                         '    memory.frame(frame)\n'
                                         '    frame = _story_call_fields(memory, frame, 250908, 250954)\n'
                                         '    return _story_exit_fields(memory, frame)',
           'confirm_finale_first_page_fields': 'def confirm_finale_first_page_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """Original 3D184 complete story role; BRA prefixes add no slot."""\n    memory.frame(frame)\n    frame = _story_call_fields(memory,frame,0x3D280,0x3D2A4)\n    frame, pressed = _story_confirm_page_fields(memory,frame,0x4696B,0x3D2CC,0x3B6BE)\n    if not pressed:\n        return frame\n    frame = _story_darken_fields(memory,frame,0x3D30E)\n    frame = _story_finish_stage_fields(memory,frame,(0x813A,0x813C))\n    frame = _story_store_fields(memory,frame,0xFFFF8020,0x1F0)\n    frame = _story_store_fields(memory,frame,0xFFFF8026,0x1F0)\n    return memory.sync_status(frame)\n',
           'confirm_interlude_exit_fields': 'def confirm_interlude_exit_fields(memory: SceneRefreshMemory, '
                                            'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                            '    """Original 3C982 complete story role; BRA prefixes add no '
                                            'slot."""\n'
                                            '    memory.frame(frame)\n'
                                            '    frame = _story_call_fields(memory, frame, 246692, 248456)\n'
                                            '    return _story_exit_fields(memory, frame)',
           'confirm_prologue_exit_fields': 'def confirm_prologue_exit_fields(memory: SceneRefreshMemory, '
                                           'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                           '    """Original 3B7E0 complete story role; BRA prefixes add no '
                                           'slot."""\n'
                                           '    memory.frame(frame)\n'
                                           '    frame = _story_call_fields(memory, frame, 244400, 244656)\n'
                                           '    return _story_exit_fields(memory, frame)',
           'confirm_prologue_first_page_fields': 'def confirm_prologue_first_page_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """Original 3B7C8 complete story role; BRA prefixes add no slot."""\n    memory.frame(frame)\n    frame = _story_call_fields(memory,frame,0x3B8D0,0x3B906)\n    frame, pressed = _story_confirm_page_fields(memory,frame,0x4632A,0x3B92E,0x3B532)\n    if not pressed:\n        return frame\n    frame = _story_darken_fields(memory,frame,0x3B970)\n    frame = _story_finish_stage_fields(memory,frame,(0x813A,))\n    return memory.sync_status(frame)\n',
           'confirm_prologue_second_page_fields': 'def confirm_prologue_second_page_fields(memory: '
                                                  'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                  'FirstDeploymentFrame:\n'
                                                  '    """Original 3B7D4 complete story role; BRA prefixes '
                                                  'add no slot."""\n'
                                                  '    memory.frame(frame)\n'
                                                  '    frame = _story_call_fields(memory, frame, 243920, '
                                                  '244182)\n'
                                                  '    frame, pressed = _story_pressed_fields(memory, '
                                                  'frame)\n'
                                                  '    if not pressed:\n'
                                                  '        return frame\n'
                                                  '    frame = _story_status_fields(memory, frame, 9984)\n'
                                                  '    frame = _story_decode_picture_fields(memory, frame, '
                                                  '288197, 244222)\n'
                                                  '    frame = _story_store_fields(memory, frame, '
                                                  '4294934566, 0)\n'
                                                  '    frame = _story_status_fields(memory, frame, 9472)\n'
                                                  '    frame = _story_finish_stage_fields(memory, frame)\n'
                                                  '    frame = _story_status_fields(memory, frame, 9984)\n'
                                                  '    frame = _story_clear_plane_fields(memory, frame)\n'
                                                  '    frame = _story_script_fields(memory, frame, 243034)\n'
                                                  '    return _story_status_fields(memory, frame, 9472)',
           'copy_scene_palette_variant_fields': 'def copy_scene_palette_variant_fields(memory: '
                                                'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                'FirstDeploymentFrame:\n'
                                                '    frame, pair = '
                                                '_copy_scene_palette_variant_fields_core(memory, frame)\n'
                                                '    return frame',
           'cycle_prologue_colors_fields': 'def cycle_prologue_colors_fields(memory: SceneRefreshMemory, '
                                           'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                           '    """Three original palette stages; every repeated timer read '
                                           'remains live."""\n'
                                           '    memory.frame(frame)\n'
                                           "    frame = _story_ram_move_fields(memory, frame, 'target_x', "
                                           '33086)\n'
                                           "    frame = _scene_mode_lsr_word(memory, frame, 'target_x', "
                                           'low16(frame.target_x), 4)\n'
                                           '    frame = _scene_render_compare(memory, frame, '
                                           'low16(frame.target_x), 6, 16)\n'
                                           '    if frame.status & 1:\n'
                                           '        frame = _scene_render_asl_word(memory, frame, '
                                           "'target_x', low16(frame.target_x), 1)\n"
                                           '        value = _story_read_fields(memory, frame, 244484 + '
                                           's16(low16(frame.target_x)))\n'
                                           '        frame = _story_store_fields(memory, frame, 4294966044, '
                                           'value)\n'
                                           '        return _story_add_ram_fields(memory, frame, 33086)\n'
                                           '    frame = _scene_render_compare(memory, frame, '
                                           'low16(frame.target_x), 14, 16)\n'
                                           '    if frame.status & 1:\n'
                                           '        frame = _story_arithmetic_fields(memory, frame, '
                                           "'target_x', 6, True)\n"
                                           '        frame = _story_arithmetic_fields(memory, frame, '
                                           "'target_x', 9)\n"
                                           '        frame = _story_call_fields(memory, frame, 240532, '
                                           '244516)\n'
                                           '        return _story_add_ram_fields(memory, frame, 33086)\n'
                                           '    frame = _story_compare_ram_fields(memory, frame, 32806, 80)\n'
                                           '    if not frame.status & 1:\n'
                                           '        return frame\n'
                                           '    for low, value in ((64258, 3822), (64262, 3784), (64286, '
                                           '3718)):\n'
                                           '        frame = _story_store_fields(memory, frame, 4294901760 | '
                                           'low, value)\n'
                                           "    frame = _story_ram_move_fields(memory, frame, 'target_x', "
                                           '62240)\n'
                                           "    frame = _story_mask_fields(memory, frame, 'target_x', 3)\n"
                                           '    if frame.status & 4:\n'
                                           '        frame = _story_add_ram_fields(memory, frame, 32806)\n'
                                           '    return frame',
           'decode_glyph_rows_to_buffers_fields': 'def decode_glyph_rows_to_buffers_fields(memory: '
                                                  'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                  'FirstDeploymentFrame:\n'
                                                  '    """AE8A unique font/fill tile algorithm with real '
                                                  'five LONG saves."""\n'
                                                  '    memory.frame(frame)\n'
                                                  '    if any((value is None for value in (frame.roster, '
                                                  'frame.candidates, frame.target_x, frame.target_y, '
                                                  'frame.count))):\n'
                                                  '        raise SceneRefreshBoundary(44682, frame, None)\n'
                                                  '    original = frame\n'
                                                  '    frame = _glyph_save_fields(memory, frame, True)\n'
                                                  '    remaining = low16(frame.count)\n'
                                                  '    row_longs = 16\n'
                                                  '    while True:\n'
                                                  '        token = frame.roster.word()\n'
                                                  '        frame = first_replace(frame, '
                                                  'roster=frame.roster.advance(2))\n'
                                                  "        frame = _first_word(frame, 'distance', token)\n"
                                                  '        if not negative_word(token):\n'
                                                  "            frame = _first_word(frame, 'offset_x', "
                                                  'token)\n'
                                                  '            high = token & 65280\n'
                                                  "            frame = _first_word(frame, 'offset_x', high)\n"
                                                  "            frame = _first_shift_word(frame, 'offset_x', "
                                                  'high, 3)\n'
                                                  '            low = token & 255\n'
                                                  "            frame = _first_word(frame, 'distance', low)\n"
                                                  "            frame = _first_shift_word(frame, 'distance', "
                                                  'low, 5)\n'
                                                  '            offset = u16(low << 5) | u16(high << 3)\n'
                                                  "            frame = _first_word(frame, 'distance', "
                                                  'offset)\n'
                                                  "            frame = _first_long(frame, 'distance', "
                                                  'offset)\n'
                                                  '            frame = first_replace(frame, '
                                                  'controller=memory.cursor_at(529820 + offset))\n'
                                                  "            frame = _first_word(frame, 'offset_x', "
                                                  'row_longs - 1)\n'
                                                  '            for index in range(row_longs):\n'
                                                  '                frame = _glyph_row_call_fields(memory, '
                                                  'frame, 44730)\n'
                                                  '                frame = _scene_refresh_emit(memory, '
                                                  'frame, frame.candidates.base, 4, frame.choice)\n'
                                                  '                frame = _glyph_row_call_fields(memory, '
                                                  'frame, 44736)\n'
                                                  '                frame = _scene_refresh_emit(memory, '
                                                  'frame, frame.candidates.base + 64, 4, frame.choice)\n'
                                                  '                frame = first_replace(frame, '
                                                  'candidates=frame.candidates.advance(4))\n'
                                                  '                frame = _scene_refresh_decrement(frame, '
                                                  "'offset_x', row_longs - 1 - index)\n"
                                                  '        else:\n'
                                                  "            frame = _first_long(frame, 'offset_y', 0)\n"
                                                  "            frame = _first_long(frame, 'choice', 0)\n"
                                                  '            nibbles = 8\n'
                                                  "            frame = _first_word(frame, 'distance', "
                                                  'nibbles - 1)\n'
                                                  '            for index in range(nibbles):\n'
                                                  '                frame = _glyph_shift_long_fields(memory, '
                                                  "frame, 'offset_y', 4)\n"
                                                  '                frame = _glyph_shift_long_fields(memory, '
                                                  "frame, 'choice', 4)\n"
                                                  "                frame = _first_word(frame, 'offset_y', "
                                                  'low16(frame.offset_y) | low16(frame.target_x))\n'
                                                  "                frame = _first_word(frame, 'choice', "
                                                  'low16(frame.choice) | low16(frame.target_y))\n'
                                                  '                frame = _scene_refresh_decrement(frame, '
                                                  "'distance', nibbles - 1 - index)\n"
                                                  "            frame = _first_word(frame, 'distance', "
                                                  'row_longs - 1)\n'
                                                  '            for index in range(row_longs):\n'
                                                  '                frame = _scene_refresh_emit(memory, '
                                                  'frame, frame.candidates.base + 64, 4, frame.offset_y)\n'
                                                  '                destination = frame.candidates\n'
                                                  '                frame = first_replace(frame, '
                                                  'candidates=destination.advance(4))\n'
                                                  '                frame = _scene_refresh_emit(memory, '
                                                  'frame, destination.base, 4, frame.offset_y)\n'
                                                  '                frame = _scene_refresh_decrement(frame, '
                                                  "'distance', row_longs - 1 - index)\n"
                                                  '            frame = _scene_refresh_emit(memory, frame, '
                                                  'frame.candidates.base - 36, 4, frame.choice)\n'
                                                  '            frame = _scene_refresh_emit(memory, frame, '
                                                  'frame.candidates.base + 28, 4, frame.choice)\n'
                                                  '        frame = first_replace(frame, '
                                                  'candidates=frame.candidates.advance(64))\n'
                                                  "        frame = _scene_refresh_decrement(frame, 'count', "
                                                  'remaining)\n'
                                                  '        remaining = u16(remaining - 1)\n'
                                                  '        if remaining == 65535:\n'
                                                  '            return '
                                                  'memory.sync_status(_glyph_restore_fields(memory, frame, '
                                                  'original, True))',
           'dispatch_arrival_story_fields': 'def dispatch_arrival_story_fields(memory: SceneRefreshMemory, '
                                            'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                            '    return _story_dispatch_fields(memory, frame, 248484)',
           'dispatch_departure_story_fields': 'def dispatch_departure_story_fields(memory: '
                                              'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                              'FirstDeploymentFrame:\n'
                                              '    return _story_dispatch_fields(memory, frame, 246172)',
           'dispatch_finale_story_fields': 'def dispatch_finale_story_fields(memory: SceneRefreshMemory, '
                                           'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                           '    return _story_dispatch_fields(memory, frame, 250236)',
           'dispatch_interlude_story_fields': 'def dispatch_interlude_story_fields(memory: '
                                              'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                              'FirstDeploymentFrame:\n'
                                              '    return _story_dispatch_fields(memory, frame, 248186)',
           'dispatch_prologue_story_fields': 'def dispatch_prologue_story_fields(memory: SceneRefreshMemory, '
                                             'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                             '    return _story_dispatch_fields(memory, frame, 243644)',
           'draw_prologue_portrait_fields': 'def draw_prologue_portrait_fields(memory: SceneRefreshMemory, '
                                            'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                            '    memory.frame(frame)\n'
                                            "    frame = _story_move_fields(memory, frame, 'unit', 12)\n"
                                            "    frame = _story_move_fields(memory, frame, 'target_x', 128)\n"
                                            "    frame = _story_move_fields(memory, frame, 'target_y', 192)\n"
                                            '    return _story_call_fields(memory, frame, 244674, 243936)',
           'finish_actor_sprite_chains_fields': 'def finish_actor_sprite_chains_fields(memory: '
                                                'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                'FirstDeploymentFrame:\n'
                                                '    """3B23C: descending actor layers, real child slots, '
                                                'and MOVE-only reset."""\n'
                                                '    from ..high_level_gameplay_flow.business_battle import '
                                                '_presentation_call_fields\n'
                                                '    from ..high_level_gameplay_flow.contexts_battle import '
                                                'BattlePresentationMemory\n'
                                                '    memory.frame(frame)\n'
                                                "    frame = _first_long(frame, 'target_x', 28)\n"
                                                "    frame = _first_long(frame, 'target_y', 0)\n"
                                                '    frame = first_replace(frame, '
                                                'roster=memory.cursor_at(4294934596))\n'
                                                '\n'
                                                '    def child(actual_memory, entered):\n'
                                                '        return '
                                                'finish_one_actor_sprite_chain_fields(SceneRefreshMemory(actual_memory.state), '
                                                'entered)\n'
                                                '    while True:\n'
                                                '        frame = '
                                                '_presentation_call_fields(BattlePresentationMemory(memory.state), '
                                                'frame, 242246, child)\n'
                                                '        frame = _scene_render_arithmetic(memory, frame, '
                                                "'target_x', low16(frame.target_x), 4, 16, True)\n"
                                                '        if low16(frame.target_x) & 32768:\n'
                                                '            break\n'
                                                "    frame = _first_long(frame, 'target_x', 0)\n"
                                                '    for displacement in (0, 4, 8, 12, 16, 20, 24, 28):\n'
                                                '        frame = _scene_refresh_emit(memory, frame, '
                                                'u32(frame.roster.base + displacement), 4, frame.target_x)\n'
                                                '    return _scene_refresh_emit(memory, frame, 4294963968, '
                                                '1, 0)',
           'finish_arrival_closing_caption_fields': 'def finish_arrival_closing_caption_fields(memory: '
                                                    'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                    'FirstDeploymentFrame:\n'
                                                    '    """Original 3CABC complete story role; BRA prefixes '
                                                    'add no slot."""\n'
                                                    '    memory.frame(frame)\n'
                                                    '    frame = _story_call_fields(memory, frame, 249240, '
                                                    '249282)\n'
                                                    '    return _story_timer_fields(memory, frame, 7040, '
                                                    '(65535,) * 4, 249324, None, (33082,))',
           'finish_departure_closing_caption_fields': 'def finish_departure_closing_caption_fields(memory: '
                                                      'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                      'FirstDeploymentFrame:\n'
                                                      '    """Original 3C1B4 complete story role; BRA '
                                                      'prefixes add no slot."""\n'
                                                      '    memory.frame(frame)\n'
                                                      '    frame = _story_call_fields(memory, frame, 247238, '
                                                      '247426)\n'
                                                      '    return _story_timer_fields(memory, frame, 7040, '
                                                      '(65535,) * 4, 247468, None, (33082,))',
           'finish_finale_closing_caption_fields': 'def finish_finale_closing_caption_fields(memory: '
                                                   'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                   'FirstDeploymentFrame:\n'
                                                   '    """Original 3D190 complete story role; BRA prefixes '
                                                   'add no slot."""\n'
                                                   '    memory.frame(frame)\n'
                                                   '    frame = _story_call_fields(memory, frame, 250908, '
                                                   '250856)\n'
                                                   '    return _story_timer_fields(memory, frame, 960, '
                                                   '(65535,) * 4, 250898, None, (33082,))',
           'finish_prologue_closing_caption_fields': 'def finish_prologue_closing_caption_fields(memory: '
                                                     'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                     'FirstDeploymentFrame:\n'
                                                     '    """Original 3B7DC complete story role; BRA '
                                                     'prefixes add no slot."""\n'
                                                     '    memory.frame(frame)\n'
                                                     '    frame = _story_call_fields(memory, frame, 244400, '
                                                     '244570)\n'
                                                     '    frame = _story_call_fields(memory, frame, 244454, '
                                                     '244574)\n'
                                                     '    return _story_timer_fields(memory, frame, 6592, '
                                                     '(65535,) * 4, 244616, None, (33082,))',
           'initialize_arrival_story_fields': 'def initialize_arrival_story_fields(memory: '
                                              'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                              'FirstDeploymentFrame:\n'
                                              '    """Original 3CAA4 complete story role; BRA prefixes add '
                                              'no slot."""\n'
                                              '    memory.frame(frame)\n'
                                              "    return _story_initialize_fields(memory, frame, 'arrival')",
           'initialize_departure_story_fields': 'def initialize_departure_story_fields(memory: '
                                                'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                'FirstDeploymentFrame:\n'
                                                '    """Original 3C19C complete story role; BRA prefixes add '
                                                'no slot."""\n'
                                                '    memory.frame(frame)\n'
                                                '    return _story_initialize_fields(memory, frame, '
                                                "'departure')",
           'initialize_finale_story_fields': 'def initialize_finale_story_fields(memory: SceneRefreshMemory, '
                                             'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                             '    """Original 3D17C complete story role; BRA prefixes add no '
                                             'slot."""\n'
                                             '    memory.frame(frame)\n'
                                             "    return _story_initialize_fields(memory, frame, 'finale')",
           'initialize_interlude_story_fields': 'def initialize_interlude_story_fields(memory: '
                                                'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                'FirstDeploymentFrame:\n'
                                                '    """Original 3C97A complete story role; BRA prefixes add '
                                                'no slot."""\n'
                                                '    memory.frame(frame)\n'
                                                '    return _story_initialize_fields(memory, frame, '
                                                "'interlude')",
           'initialize_prologue_story_fields': 'def initialize_prologue_story_fields(memory: '
                                               'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                               'FirstDeploymentFrame:\n'
                                               '    """Original 3B7BC complete story role; BRA prefixes add '
                                               'no slot."""\n'
                                               '    memory.frame(frame)\n'
                                               '    return _story_initialize_fields(memory, frame, '
                                               "'prologue')",
           'load_departure_tile_rows_fields': 'def load_departure_tile_rows_fields(memory: '
                                              'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                              'FirstDeploymentFrame:\n'
                                              '    memory.frame(frame)\n'
                                              '    frame = first_replace(frame, '
                                              'controller=memory.cursor_at(246436))\n'
                                              '    rows = ((59424, 246344), (59552, 246352), (59680, '
                                              '246360), (59808, 246368), (59936, 246376), (60064, 246384), '
                                              '(60192, 246392), (60320, 246400))\n'
                                              '    for address, continuation in rows:\n'
                                              "        frame = _story_move_fields(memory, frame, 'target_x', "
                                              'address)\n'
                                              '        frame = _story_call_fields(memory, frame, 246402, '
                                              'continuation)\n'
                                              '    return frame',
           'move_finale_actor_diagonally_fields': 'def move_finale_actor_diagonally_fields(memory: '
                                                  'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                  'FirstDeploymentFrame:\n'
                                                  '    memory.frame(frame)\n'
                                                  '    frame = _story_compare_ram_fields(memory, frame, '
                                                  '33084, 160)\n'
                                                  '    if not frame.status & 5:\n'
                                                  '        return frame\n'
                                                  '    frame = _story_add_ram_fields(memory, frame, 33084, '
                                                  '2)\n'
                                                  "    frame = _story_move_fields(memory, frame, 'target_x', "
                                                  '48)\n'
                                                  "    frame = _story_move_fields(memory, frame, 'target_y', "
                                                  '224)\n'
                                                  '    frame = _story_arithmetic_fields(memory, frame, '
                                                  "'target_x', _story_read_fields(memory, frame, "
                                                  '4294934844))\n'
                                                  '    frame = _story_arithmetic_fields(memory, frame, '
                                                  "'target_y', _story_read_fields(memory, frame, "
                                                  '4294934844), True)\n'
                                                  '    frame = _story_arithmetic_fields(memory, frame, '
                                                  "'target_x', _story_read_fields(memory, frame, "
                                                  '4294934560))\n'
                                                  "    frame = _story_move_fields(memory, frame, 'unit', 7)\n"
                                                  '    return _story_call_fields(memory, frame, 250972, '
                                                  '250736)',
           'read_vdp_plane_rle_rows_fields': 'def read_vdp_plane_rle_rows_fields(memory: SceneRefreshMemory, '
                                             'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                             '    frame, discarded = '
                                             '_read_vdp_plane_rle_rows_fields_core(memory, frame)\n'
                                             '    return frame',
           'reveal_arrival_caption_fields': 'def reveal_arrival_caption_fields(memory: SceneRefreshMemory, '
                                            'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                            '    """Original 3CAA8 complete story role; BRA prefixes add no '
                                            'slot."""\n'
                                            '    memory.frame(frame)\n'
                                            '    frame = _story_call_fields(memory, frame, 248766, 248642)\n'
                                            '    frame = _story_caption_trigger_fields(memory, frame, 512, '
                                            '243248)\n'
                                            '    return _story_timer_fields(memory, frame, 512, (65535, '
                                            '65535, 0, 65535), 248756, None, (33082,))',
           'reveal_departure_caption_fields': 'def reveal_departure_caption_fields(memory: '
                                              'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                              'FirstDeploymentFrame:\n'
                                              '    """Original 3C1A0 complete story role; BRA prefixes add '
                                              'no slot."""\n'
                                              '    memory.frame(frame)\n'
                                              '    frame = _story_call_fields(memory, frame, 246692, '
                                              '246568)\n'
                                              '    frame = _story_caption_trigger_fields(memory, frame, 512, '
                                              '243102)\n'
                                              '    return _story_timer_fields(memory, frame, 512, (65535, '
                                              '65535, 0, 65535), 246682, None, (33082,))',
           'reveal_finale_caption_fields': 'def reveal_finale_caption_fields(memory: SceneRefreshMemory, '
                                           'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                           '    """Original 3D180 complete story role; BRA prefixes add no '
                                           'slot."""\n'
                                           '    memory.frame(frame)\n'
                                           '    frame = _story_call_fields(memory, frame, 250496, 250372)\n'
                                           '    frame = _story_caption_trigger_fields(memory, frame, 192, '
                                           '243368)\n'
                                           '    return _story_timer_fields(memory, frame, 320, (65535, '
                                           '65535, 0, 65535), 250486, None, (33082,))',
           'reveal_interlude_caption_fields': 'def reveal_interlude_caption_fields(memory: '
                                              'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                              'FirstDeploymentFrame:\n'
                                              '    """Original 3C97E complete story role; BRA prefixes add '
                                              'no slot."""\n'
                                              '    memory.frame(frame)\n'
                                              '    frame = _story_call_fields(memory, frame, 246692, '
                                              '248328)\n'
                                              '    frame = _story_caption_trigger_fields(memory, frame, 256, '
                                              '243450)\n'
                                              '    return _story_timer_fields(memory, frame, 960, (65535,) * '
                                              '4, 248442, None, (33082,))',
           'reveal_prologue_caption_fields': 'def reveal_prologue_caption_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n    """Original 3B7C0 complete story role; BRA prefixes add no slot."""\n    memory.frame(frame)\n    frame = _story_call_fields(memory,frame,0x3B8D0,0x3B85C)\n    frame = _story_add_ram_fields(memory,frame,0x813A)\n    frame = _story_compare_ram_fields(memory,frame,0x813A,0x200)\n    if frame.status & 1:\n        return frame\n    frame = _story_palette_masks_fields(memory,frame,(0,0xFFFF,0,0))\n    frame = _story_darken_fields(memory,frame,0x3B886)\n    frame = _story_status_fields(memory,frame,0x2700)\n    frame = _story_clear_plane_fields(memory,frame)\n    frame = _story_script_fields(memory,frame,0x3B506)\n    frame = _story_status_fields(memory,frame,0x2500)\n    return _story_finish_stage_fields(memory,frame,(0x813A,))\n',
           'reveal_prologue_second_portrait_fields': 'def reveal_prologue_second_portrait_fields(memory: '
                                                     'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                     'FirstDeploymentFrame:\n'
                                                     '    """Original 3B7D0 complete story role; BRA '
                                                     'prefixes add no slot."""\n'
                                                     '    memory.frame(frame)\n'
                                                     '    frame = _story_call_fields(memory, frame, 243920, '
                                                     '244126)\n'
                                                     '    return _story_timer_fields(memory, frame, 64, '
                                                     '(65535, 65535, 0, 65535), 244168, None, (33082,))',
           'select_arrival_sprite_fields': 'def select_arrival_sprite_fields(memory: SceneRefreshMemory, '
                                           'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                           '    memory.frame(frame)\n'
                                           '    return _story_select_sprite_fields(memory, frame, 249372, '
                                           '512)',
           'select_departure_sprite_fields': 'def select_departure_sprite_fields(memory: SceneRefreshMemory, '
                                             'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                             '    memory.frame(frame)\n'
                                             '    return _story_select_sprite_fields(memory, frame, 247516, '
                                             'None)',
           'select_finale_sprite_fields': 'def select_finale_sprite_fields(memory: SceneRefreshMemory, '
                                          'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                          '    memory.frame(frame)\n'
                                          "    frame = _story_move_fields(memory, frame, 'distance', 256)\n"
                                          '    return select_finale_sprite_with_attributes_fields(memory, '
                                          'frame)',
           'select_finale_sprite_with_attributes_fields': 'def '
                                                          'select_finale_sprite_with_attributes_fields(memory: '
                                                          'SceneRefreshMemory, frame: FirstDeploymentFrame) '
                                                          '-> FirstDeploymentFrame:\n'
                                                          '    """True 3D460 middle entry inherits D4; '
                                                          'neither extra call nor marker setup."""\n'
                                                          '    memory.frame(frame)\n'
                                                          '    return _story_select_sprite_fields(memory, '
                                                          'frame, 250992, None)',
           'select_prologue_sprite_fields': 'def select_prologue_sprite_fields(memory: SceneRefreshMemory, '
                                            'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                            '    memory.frame(frame)\n'
                                            '    return _story_select_sprite_fields(memory, frame, 244694, '
                                            '256)',
           'set_vram_write_address_fields': 'def set_vram_write_address_fields(memory: SceneRefreshMemory, '
                                            'frame: FirstDeploymentFrame, address: Word | None=None) -> '
                                            'FirstDeploymentFrame:\n'
                                            '    """3B2B0 sole encoding math, genuine D1 LONG save/read, '
                                            'real shift X."""\n'
                                            '    memory.frame(frame)\n'
                                            '    if address is None:\n'
                                            '        if frame.target_x is None:\n'
                                            '            raise SceneRefreshBoundary(242352, frame, None)\n'
                                            '        address = low16(frame.target_x)\n'
                                            '    uint(address, 16)\n'
                                            '    if frame.target_x is not None and low16(frame.target_x) != '
                                            'address:\n'
                                            "        raise ValueError('observed scene video WORD must agree "
                                            "with current D0')\n"
                                            '    if frame.stack_cursor is not None:\n'
                                            '        frame = _scene_render_push_longs(memory, frame, '
                                            '(frame.target_y,))\n'
                                            "    frame = _first_long(frame, 'target_x', address)\n"
                                            "    frame = _first_long(frame, 'target_y', address)\n"
                                            '    command = swap_words(address & 16383 | 16384) | address >> '
                                            '14\n'
                                            '    status = (16 if address & 8192 else 0) | (8 if command & '
                                            '2147483648 else 0) | (4 if command == 0 else 0)\n'
                                            '    frame = first_replace(frame, target_x=command, '
                                            'status=status)\n'
                                            '    frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                            'command)\n'
                                            '    if frame.stack_cursor is not None:\n'
                                            '        restored = frame.stack_cursor.long()\n'
                                            '        frame = first_replace(frame, target_y=restored, '
                                            'stack_cursor=frame.stack_cursor.advance(4))\n'
                                            '    else:\n'
                                            '        frame = first_replace(frame, target_y=None)\n'
                                            '    return memory.sync_status(frame)',
           'transfer_story_overlay_dma_fields': 'def transfer_story_overlay_dma_fields(memory: '
                                                'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                'FirstDeploymentFrame:\n'
                                                '    memory.frame(frame)\n'
                                                '    frame = _story_call_fields(memory, frame, 26570, '
                                                '239778)\n'
                                                '    frame = _story_dma_setup_fields(memory, frame, '
                                                '(2483131200, 2533135616, 20480), 131, True)\n'
                                                '    frame = _story_store_fields(memory, frame, '
                                                'frame.auxiliary.base, _story_read_fields(memory, frame, '
                                                '4294964742))\n'
                                                '    frame = _story_store_fields(memory, frame, 12582916, '
                                                '1073741840, 4)\n'
                                                '    frame = _story_store_fields(memory, frame, 12582912, '
                                                '_story_read_fields(memory, frame, 4294934564, 4), 4)\n'
                                                '    frame = _story_store_fields(memory, frame, 12582916, '
                                                '1409286147, 4)\n'
                                                '    frame = _story_store_fields(memory, frame, 12582912, '
                                                '_story_read_fields(memory, frame, 4294934568, 4), 4)\n'
                                                "    frame = _story_move_fields(memory, frame, 'target_x', "
                                                '96)\n'
                                                '    while True:\n'
                                                '        remaining = u16(low16(frame.target_x) - 1)\n'
                                                '        frame = first_replace(frame, '
                                                'target_x=replace_word(frame.target_x, remaining))\n'
                                                '        if remaining == 65535:\n'
                                                '            break\n'
                                                '    frame = _story_dma_setup_fields(memory, frame, '
                                                '(2483065664, 2533201280, 49152), 128, True)\n'
                                                '    frame = _story_store_fields(memory, frame, '
                                                'frame.auxiliary.base, _story_read_fields(memory, frame, '
                                                '4294964742))\n'
                                                '    frame = _story_dma_finish_fields(memory, frame)\n'
                                                '    return _story_call_fields(memory, frame, 262058, '
                                                '239988)',
           'transfer_story_plane_dma_fields': 'def transfer_story_plane_dma_fields(memory: '
                                              'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                              'FirstDeploymentFrame:\n'
                                              '    memory.frame(frame)\n'
                                              '    frame = _story_call_fields(memory, frame, 26570, 238908)\n'
                                              '    frame = _story_call_fields(memory, frame, 18754, 238914)\n'
                                              '    frame = _story_dma_setup_fields(memory, frame, '
                                              '(2483065664, 2533201280, 49152), 128, True)\n'
                                              '    frame = _story_store_fields(memory, frame, '
                                              'frame.auxiliary.base, _story_read_fields(memory, frame, '
                                              '4294964742))\n'
                                              '    frame = _story_clear_fields(memory, frame, 62994)\n'
                                              '    return _story_dma_finish_fields(memory, frame)',
           'wait_arrival_second_page_fields': 'def wait_arrival_second_page_fields(memory: '
                                              'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                              'FirstDeploymentFrame:\n'
                                              '    """Original 3CAB0 complete story role; BRA prefixes add '
                                              'no slot."""\n'
                                              '    memory.frame(frame)\n'
                                              '    frame = _story_call_fields(memory, frame, 248962, '
                                              '248930)\n'
                                              '    return _story_timer_fields(memory, frame, 512, None, '
                                              '248948, None, (33082, 33084))',
           'wait_departure_second_page_fields': 'def wait_departure_second_page_fields(memory: '
                                                'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                                'FirstDeploymentFrame:\n'
                                                '    """Original 3C1A8 complete story role; BRA prefixes add '
                                                'no slot."""\n'
                                                '    memory.frame(frame)\n'
                                                '    frame = _story_call_fields(memory, frame, 246942, '
                                                '246914)\n'
                                                '    return _story_timer_fields(memory, frame, 512, None, '
                                                '246932, None, (33082,))',
           'wait_finale_scroll_fields': 'def wait_finale_scroll_fields(memory: SceneRefreshMemory, frame: '
                                        'FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                        '    """Original 3D188 complete story role; BRA prefixes add no '
                                        'slot."""\n'
                                        '    memory.frame(frame)\n'
                                        '    frame = _story_call_fields(memory, frame, 250694, 250668)\n'
                                        '    return _story_timer_fields(memory, frame, 256, None, None, '
                                        'None, (33082, 33084))',
           'wait_prologue_portrait_fields': 'def wait_prologue_portrait_fields(memory: SceneRefreshMemory, '
                                            'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                            '    """Original 3B7C4 complete story role; BRA prefixes add no '
                                            'slot."""\n'
                                            '    memory.frame(frame)\n'
                                            '    frame = _story_call_fields(memory, frame, 243920, 243942)\n'
                                            '    return _story_timer_fields(memory, frame, 512, None, '
                                            '243960, None, (33082,))',
           'wait_prologue_second_page_fields': 'def wait_prologue_second_page_fields(memory: '
                                               'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                               'FirstDeploymentFrame:\n'
                                               '    """Original 3B7CC complete story role; BRA prefixes add '
                                               'no slot."""\n'
                                               '    memory.frame(frame)\n'
                                               '    frame = _story_call_fields(memory, frame, 243920, '
                                               '244094)\n'
                                               '    return _story_timer_fields(memory, frame, 512, None, '
                                               '244112, None, (33082,))',
           'write_departure_tile_row_fields': 'def write_departure_tile_row_fields(memory: '
                                              'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                              'FirstDeploymentFrame:\n'
                                              '    memory.frame(frame)\n'
                                              '    frame = _scene_render_push_longs(memory, frame, '
                                              '(frame.controller.base,))\n'
                                              '    frame = _story_store_fields(memory, frame, 12582916, '
                                              '36610)\n'
                                              '    frame = _story_call_fields(memory, frame, 242352, '
                                              '246418)\n'
                                              '    stack = frame.stack_cursor\n'
                                              '    frame = first_replace(frame, '
                                              'controller=memory.cursor_at(stack.long()), '
                                              'stack_cursor=stack.advance(4))\n'
                                              "    frame = _story_move_fields(memory, frame, 'target_x', 7, "
                                              '32)\n'
                                              '    while True:\n'
                                              '        value = _story_read_fields(memory, frame, '
                                              'frame.controller.base)\n'
                                              '        frame = first_replace(frame, '
                                              'controller=frame.controller.advance(2))\n'
                                              '        frame = _story_store_fields(memory, frame, 12582912, '
                                              'value)\n'
                                              '        remaining = u16(low16(frame.target_x) - 1)\n'
                                              '        frame = first_replace(frame, '
                                              'target_x=replace_word(frame.target_x, remaining))\n'
                                              '        if remaining == 65535:\n'
                                              '            return frame'}}
EXPECTED_BASE = {'_dump': 'def _dump(node):\n    return ast.dump(node, include_attributes=False)',
 '_code_shape': 'def _code_shape(code):\n'
                "    return tuple((getattr(code, name) for name in ('co_code', 'co_names', 'co_varnames', "
                "'co_argcount', 'co_posonlyargcount', 'co_kwonlyargcount', 'co_flags', 'co_freevars', "
                "'co_cellvars'))) + (tuple((_code_shape(value) if type(value) is CodeType else value for "
                'value in code.co_consts)),)',
 '_top_code': 'def _top_code(code, name):\n'
              '    found = [value for value in code.co_consts if type(value) is CodeType and value.co_name '
              '== name and (value.co_qualname == name)]\n'
              '    if len(found) != 1:\n'
              "        raise ValueError('one complete top-level battle parent source required: ' + name)\n"
              '    return found[0]',
 '_cooperative_tree': 'def _cooperative_tree(group, original_tree):\n'
                      '    """Finite declared call/wait replacements; inverse every whole FN/module."""\n'
                      '    result = copy.deepcopy(original_tree)\n'
                      '    inverses = {}\n'
                      '    for index, node in enumerate(original_tree.body):\n'
                      '        if not isinstance(node, ast.FunctionDef) or node.name not in '
                      'VIEW_SPECS[group]:\n'
                      '            continue\n'
                      '        if _dump(node) != '
                      '_dump(ast.parse(EXPECTED_SOURCE[group][node.name]).body[0]):\n'
                      "            raise ValueError('complete reviewed battle parent source changed: ' + "
                      'node.name)\n'
                      '        if any((isinstance(item, (ast.Yield, ast.YieldFrom)) for item in '
                      'ast.walk(node))):\n'
                      "            raise ValueError('original finite battle business owner must remain "
                      "synchronous')\n"
                      '        spec = VIEW_SPECS[group][node.name]\n'
                      '        substitutions = []\n'
                      "        counts = {name: 0 for name in spec['calls']}\n"
                      '        waits = []\n'
                      '        replacements = [(ast.parse(old).body[0], ast.parse(new).body) for old, new in '
                      "spec['statements']]\n"
                      '\n'
                      '        class Lift(ast.NodeTransformer):\n'
                      '\n'
                      '            def visit_Call(self, item):\n'
                      '                item = self.generic_visit(item)\n'
                      '                if isinstance(item.func, ast.Name) and item.func.id in counts:\n'
                      '                    before = copy.deepcopy(item)\n'
                      '                    name = item.func.id\n'
                      '                    counts[name] += 1\n'
                      "                    item.func.id = spec['calls'][name][1]\n"
                      "                    if name == 'algorithm':\n"
                      "                        item.args.append(ast.Name(id='algorithm', ctx=ast.Load()))\n"
                      "                    if item.func.id == '_battle_attribute_child':\n"
                      "                        item.args.append(ast.Name(id='continuation', "
                      'ctx=ast.Load()))\n'
                      '                    after = ast.copy_location(ast.YieldFrom(value=item), item)\n'
                      '                    substitutions.append((before, copy.deepcopy(after)))\n'
                      '                    return after\n'
                      '                return item\n'
                      '\n'
                      '            def _statement(self, item):\n'
                      '                for old, new in replacements:\n'
                      '                    if _dump(item) == _dump(old):\n'
                      '                        waits.append((copy.deepcopy(old), copy.deepcopy(new)))\n'
                      '                        return copy.deepcopy(new)\n'
                      '                return self.generic_visit(item)\n'
                      '\n'
                      '            def visit_Raise(self, item):\n'
                      '                return self._statement(item)\n'
                      '\n'
                      '            def visit_Expr(self, item):\n'
                      '                return self._statement(item)\n'
                      '        derived = Lift().visit(copy.deepcopy(node))\n'
                      "        if counts != {name: rule[0] for name, rule in spec['calls'].items()} or "
                      'len(waits) != len(replacements):\n'
                      "            raise ValueError('exact finite battle-parent substitutions differ: ' + "
                      'node.name)\n'
                      '        inverse = copy.deepcopy(derived)\n'
                      '        for old, new in waits:\n'
                      '            sites = []\n'
                      '            for parent in ast.walk(inverse):\n'
                      "                for field in ('body', 'orelse', 'finalbody'):\n"
                      '                    body = getattr(parent, field, None)\n'
                      '                    if type(body) is not list:\n'
                      '                        continue\n'
                      '                    for position in range(len(body) - len(new) + 1):\n'
                      '                        if [_dump(v) for v in body[position:position + len(new)]] == '
                      '[_dump(v) for v in new]:\n'
                      '                            sites.append((body, position))\n'
                      '            if len(sites) != 1:\n'
                      "                raise ValueError('one exact battle wait inverse required')\n"
                      '            body, position = sites[0]\n'
                      '            body[position:position + len(new)] = [old]\n'
                      '        remaining = list(substitutions)\n'
                      '\n'
                      '        class Inverse(ast.NodeTransformer):\n'
                      '\n'
                      '            def visit_YieldFrom(self, item):\n'
                      '                item = self.generic_visit(item)\n'
                      '                for position, (before, after) in enumerate(remaining):\n'
                      '                    if _dump(item) == _dump(after):\n'
                      '                        remaining.pop(position)\n'
                      '                        return copy.deepcopy(before)\n'
                      "                raise ValueError('unknown cooperative battle call substitution')\n"
                      '        inverse = Inverse().visit(inverse)\n'
                      '        if remaining or _dump(inverse) != _dump(node):\n'
                      "            raise ValueError('complete original battle-parent FN inverse differs: ' + "
                      'node.name)\n'
                      '        result.body[index] = derived\n'
                      '        inverses[index] = inverse\n'
                      '    if len(inverses) != len(VIEW_SPECS[group]):\n'
                      "        raise ValueError('all declared whole battle-parent functions required')\n"
                      '    restored = copy.deepcopy(result)\n'
                      '    for index, inverse in inverses.items():\n'
                      '        restored.body[index] = inverse\n'
                      '    if _dump(restored) != _dump(original_tree):\n'
                      "        raise ValueError('whole business source module inverse differs: ' + group)\n"
                      '    return ast.fix_missing_locations(result)',
 '_actual_fields': 'def _actual_fields(state, frame):\n'
                   '    """No initialization: retain the actual sixteen carriers and full SR."""\n'
                   '    if type(frame) is FirstDeploymentFrame:\n'
                   '        actual = _movement_frame(state, frame)\n'
                   '    elif type(frame) is BattleTriggerFrame:\n'
                   '        frame.validate_complete(state)\n'
                   '        if frame.status != state.sr:\n'
                   "            raise ValueError('trigger SR must be the actual live full SR')\n"
                   '        actual = FirstDeploymentFrame(**{name: getattr(frame, name) for name in FIELDS}, '
                   'status=frame.status & 31)\n'
                   '        actual = _movement_frame(state, actual)\n'
                   '    else:\n'
                   "        raise ValueError('one exact retained full-frame type required')\n"
                   '    if actual.status != state.sr & 31:\n'
                   "        raise ValueError('battle wait full SR/CCR-X mismatch')\n"
                   '    return actual',
 '_trigger_fields': 'def _trigger_fields(state, frame):\n'
                    '    actual = _actual_fields(state, frame)\n'
                    '    return BattleTriggerFrame(**{name: getattr(actual, name) for name in FIELDS}, '
                    'status=state.sr, legacy_context=None).validate_complete(state)',
 'BattleScenePrograms': 'class BattleScenePrograms(CityScenePrograms):\n    """Same-Scene private graph, integrated through the actual Main478/490 CALL."""\n\n    def __init__(self, state):\n        super().__init__(state)\n        import importlib\n        self.battle_modules = {group: importlib.import_module(path) for group, path in MODULE_PATHS.items()}\n        self.battle_originals = {}\n        self.battle_codes = {}\n        self.battle_views = {}\n        self.battle_namespaces = {}\n        self.battle_bindings = {}\n        self.battle_admissions = []\n        for group, module in self.battle_modules.items():\n            tree = ast.parse(inspect.getsource(module), filename=module.__file__)\n            nodes = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}\n            compiled = compile(tree, module.__file__, \'exec\', dont_inherit=True)\n            for name, source in EXPECTED_SOURCE[group].items():\n                original = getattr(module, name)\n                if name not in nodes or _dump(nodes[name]) != _dump(ast.parse(source).body[0]) or type(original) is not FunctionType or (original.__globals__ is not vars(module)) or (original.__module__ != module.__name__) or (original.__name__ != name) or (original.__closure__ is not None) or original.__code__.co_freevars or (_code_shape(original.__code__) != _code_shape(_top_code(compiled, name))):\n                    raise ValueError(\'actual unwrapped reviewed battle source owner required: \' + name)\n                self.battle_originals[group, name] = original\n                self.battle_codes[group, name] = original.__code__\n            derived = _cooperative_tree(group, tree)\n            code = compile(derived, module.__file__, \'exec\', dont_inherit=True)\n            namespace = dict(vars(module))\n            self.battle_namespaces[group] = namespace\n            for name in VIEW_SPECS[group]:\n                original = self.battle_originals[group, name]\n                view = FunctionType(_top_code(code, name), namespace, name, original.__defaults__, None)\n                view.__kwdefaults__ = original.__kwdefaults__\n                view.__annotations__ = dict(original.__annotations__)\n                if not inspect.isgeneratorfunction(view):\n                    raise ValueError(\'every declared battle view must be a genuine generator: \' + name)\n                self.battle_views[group, name] = view\n            self.battle_admissions.append(dict(group=group, whole_function_inverses=len(VIEW_SPECS[group]), whole_module_inverse=True))\n        self._battle_view_owners = dict(self.battle_views)\n        self._battle_view_codes = {key: view.__code__ for key, view in self.battle_views.items()}\n        aliases = {self._alias(group, name): view for (group, name), view in self.battle_views.items()}\n        aliases.update(_battle_irq=self._irq, _battle_trigger_irq=self._trigger_irq, _battle_round=self._round, _battle_load=self._load, _battle_refresh=self._refresh, _battle_message_clear=self._message_clear, _battle_algorithm=self._algorithm, _battle_order_dispatch=self._order_dispatch, _battle_deployment_child=self._deployment_child, _battle_attribute_child=self._attribute_child, _battle_command_call=self.views[\'highbank\', \'_command_policy_call_fields\'], _battle_campaign_call=self.views[\'main\', \'_campaign_call_fields\'], _battle_initialization_wait=self.battle_originals[\'initialization\', \'initialization_device_wait\'])\n        for group, namespace in self.battle_namespaces.items():\n            for name, value in aliases.items():\n                if name in namespace:\n                    raise ValueError(\'finite battle alias must not replace an original business name\')\n                namespace[name] = value\n                self.battle_bindings[group, name] = value\n            if group == \'battle\':\n                namespace[\'award_city_reserve_attrition_fields\'] = self.battle_views[\'battle\', \'award_city_reserve_attrition_fields\']\n                self.battle_bindings[group, \'award_city_reserve_attrition_fields\'] = namespace[\'award_city_reserve_attrition_fields\']\n        self._target_fallback = self.battle_modules[\'highbank\'].call_target\n        self._target_fallback_code = self._target_fallback.__code__\n\n    @staticmethod\n    def _alias(group, name):\n        return \'_battle_view_\' + group + \'_\' + name\n\n    def require_current(self, state):\n        super().require_current(state)\n        if not hasattr(self, \'battle_originals\'):\n            return\n        for (group, name), original in self.battle_originals.items():\n            if getattr(self.battle_modules[group], name) is not original or original.__code__ is not self.battle_codes[group, name]:\n                raise ValueError(\'actual battle dependency changed during suspension: \' + name)\n        if self.battle_views.keys() != self._battle_view_owners.keys():\n            raise ValueError(\'finite whole battle continuation graph changed\')\n        for key, view in self._battle_view_owners.items():\n            if self.battle_views[key] is not view or view.__code__ is not self._battle_view_codes[key]:\n                raise ValueError(\'whole battle continuation callable changed during suspension: \' + key[1])\n        for (group, name), value in self.battle_bindings.items():\n            if self.battle_namespaces[group].get(name) is not value:\n                raise ValueError(\'private finite battle continuation binding changed: \' + name)\n        if hasattr(self, \'_target_fallback\') and (self.battle_modules[\'highbank\'].call_target is not self._target_fallback or self._target_fallback.__code__ is not self._target_fallback_code):\n            raise ValueError(\'original attribute-order service fallback changed\')\n\n    def _irq(self, state, frame, poll):\n        self.require_current(state)\n        entered = _actual_fields(state, frame)\n        waiting = BattleTriggerWait(state, entered, state.sr, poll).validate()\n        returned = (yield waiting)\n        self.require_current(state)\n        returned = _actual_fields(state, returned)\n        if returned.stack_cursor.base != entered.stack_cursor.base or state.sr != waiting.status_word:\n            raise ValueError(\'real battle IRQ must RTE to the same physical SP and full SR\')\n        return returned\n\n    def _trigger_irq(self, memory, frame, suffix=None, expected=None):\n        self.require_current(memory.state)\n        if suffix is None and expected is None:\n            poll = 145536\n        elif (suffix, expected) == (\'f600\', 196):\n            poll = 145496\n        elif (suffix, expected) == (\'f600\', 132):\n            poll = 145518\n        else:\n            raise ValueError(\'only the original three city-trigger IRQ loops are admitted\')\n        returned = (yield from self._irq(memory.state, frame, poll))\n        return _trigger_fields(memory.state, returned)\n\n    def _forward_scene(self, session):\n        current = session.start()\n        try:\n            while type(current) in (GameplaySceneWait, ScriptedSceneWait):\n                self.require_current(self.state)\n                waiting = current\n                returned = (yield waiting)\n                self.require_current(self.state)\n                if type(waiting) is GameplaySceneWait and (not waiting.needs_interrupt):\n                    if returned is not waiting.frame:\n                        raise ValueError(\'device event cannot replace actual battle Scene frame\')\n                    current = session.resume_device(waiting.event)\n                else:\n                    current = session.resume_interrupt(returned, waiting.poll)\n            return _actual_fields(self.state, current)\n        finally:\n            session._program.close()\n\n    def _load(self, memory, frame):\n        self.require_current(memory.state)\n        return (yield from self._forward_scene(GameplaySceneLoadSession(memory.state, frame)))\n\n    def _refresh(self, memory, frame):\n        self.require_current(memory.state)\n        return (yield from self._forward_scene(GameplaySceneRefreshSession(memory.state, frame)))\n\n    def _round(self, memory, frame):\n        self.require_current(memory.state)\n        # This interface is also reached by the public23736 contact program,\n        # not only by the four Main routes already selecting Lifecycle.\n        # Construct the complete child graph once inside the entered DC0 CALL;\n        # its override/root below never calls this base method again.\n        from .battle_lifecycle_steps import BattleLifecycleScenePrograms\n        programs = BattleLifecycleScenePrograms(memory.state)\n        return (yield from self._message_waits(programs._round_entry(memory.state, frame)))\n\n    def _message_clear(self, state, frame, target, continuation):\n        self.require_current(state)\n        if (target, continuation) != (1548, 155924):\n            raise ValueError(\'only actual battle-message060C/26114 call is admitted\')\n        frame = _actual_fields(state, frame)\n        stack = frame.stack_cursor.advance(-4)\n        stack.set_long(0, continuation)\n        returned = (yield from self.battle_views[\'services\', \'clear_scene_video_and_state_fields\'](SceneRefreshMemory(state), first_replace(frame, stack_cursor=stack)))\n        returned = _actual_fields(state, returned)\n        if returned.stack_cursor.long() != continuation:\n            raise Boundary(\'actual26114 battle-message return slot changed\')\n        return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))\n\n    def _algorithm(self, memory, frame, algorithm):\n        self.require_current(memory.state)\n        allowed = tuple((self.battle_originals[\'battle\', name] for name in (\'_presentation_random_fields\', \'sample_battle_special_status_factor_fields\', \'_damage_potential_fields\', \'_damage_terrain_query_fields\'))) + (self.battle_views[\'battle\', \'award_city_reserve_attrition_fields\'],)\n        if not any((algorithm is owner for owner in allowed)):\n            raise ValueError(\'one finite original damage algorithm identity required\')\n        result = algorithm(memory, frame)\n        if type(result) is GeneratorType:\n            return (yield from result)\n        return result\n\n    def _order_dispatch(self, state, frame, target):\n        self.require_current(state)\n        if target in PRIMARY_ENTRIES:\n            return (yield from self.battle_views[\'highbank\', \'highbank_coordinate_live_state_65_fields\'](state, frame, entry=target))\n        if target == 144738:\n            return (yield from self.battle_views[\'gameplay\', \'execute_primary_force_orders_frame_fields\'](state, frame))\n        return self.battle_originals[\'display\', \'display_child_fields\'](state, frame, target)\n\n    def _deployment_child(self, state, target, frame):\n        """Finite actual secondary table/modal children; never a generic hub."""\n        self.require_current(state)\n        if target == 155876:\n            return (yield from self.battle_views[\'movement\', \'present_battle_message_fields\'](state, frame))\n        named = {140510: \'try_city_officer_movement_trigger_fields\', 140684: \'evaluate_city_officer_movement_chance_fields\', 141120: \'execute_first_retreat_continuation_fields\', 141142: \'evaluate_other_city_retreat_order_fields\', 141706: \'test_retreat_readiness_contact_fields\', 141810: \'execute_second_retreat_continuation_fields\', 143336: \'try_city_contact_readiness_action_fields\', 155602: \'attempt_first_side_contact_actions_fields\', 141288: \'update_first_retreat_position_fields\', 141830: \'update_second_retreat_position_fields\', 142470: \'choose_contact_retreat_coordinate_fields\', 142520: \'try_contact_retreat_readiness_fields\', 144016: \'preselect_city_nearest_contact_fields\'}\n        if target in named:\n            if target == 141142:\n                return (yield from self.battle_views[\'highbank\', named[target]](state, frame, True))\n            return (yield from self.battle_views[\'highbank\', named[target]](state, frame))\n        if target in (142136, 142852, 143086, 143306, 143474, 143502, 143530, 144404, 144466, 144530):\n            return (yield from self.battle_views[\'highbank\', \'execute_guarded_retreat_strategy_fields\'](state, frame, entry=target))\n        if target in (142166, 142882, 143116):\n            return (yield from self.battle_views[\'highbank\', \'update_contact_retreat_position_fields\'](state, frame, entry=target))\n        packed = (143582, 144456, 144520, 144584)\n        if target in packed:\n            return (yield from self.battle_views[\'highbank\', \'move_city_actor_to_packed_target_fields\'](state, frame, packed.index(target)))\n        first = (155658, 155948, 156236, 156414, 156680)\n        if target in first:\n            return (yield from self.battle_views[\'highbank\', \'execute_first_side_contact_action_fields\'](state, frame, first.index(target)))\n        return self.battle_originals[\'city\', \'execute_deployment_menu_fields\'](state, target, frame)\n\n    def _command_child(self, state, frame, target, continuation):\n        if target in ASYNC_DEPLOYMENT_ENTRIES:\n            self.require_current(state)\n            return (yield from self._deployment_child(state, target, frame))\n        return (yield from super()._command_child(state, frame, target, continuation))\n\n    def _attribute_child(self, state, target, frame, continuation):\n        """The actual26624 fallback has already pushed its genuine LONG."""\n        self.require_current(state)\n        if target == 155876:\n            if continuation != 157220:\n                raise ValueError(\'actual attribute-order message26624 required\')\n            return (yield from self.battle_views[\'movement\', \'present_battle_message_fields\'](state, frame))\n        return self._target_fallback(state, target, frame)\n\n    def _campaign_child(self, state, frame, target, continuation):\n        self.require_current(state)\n        if (target, continuation) == (95746, 3254):\n            return (yield from self.battle_views[\'battle\', \'initialize_battle_scene_fields\'](SceneRefreshMemory(state), frame))\n        if (target, continuation) == (99320, 3366):\n            returned, award = (yield from self.battle_views[\'battle\', \'resolve_city_battle_damage_fields\'](BattlePresentationMemory(state), frame))\n            return returned\n        if (target, continuation) == (139748, 3468):\n            return (yield from self.battle_views[\'gameplay\', \'process_both_battle_force_turns_fields\'](state, frame))\n        if (target, continuation) in ((44872, 3372), (44872, 3474)):\n            return (yield from self._refresh(SceneRefreshMemory(state), frame))\n        return (yield from super()._campaign_child(state, frame, target, continuation))\n\n    def _display_child(self, state, frame, target, continuation):\n        self.require_current(state)\n        if target in MAIN_ENTRIES:\n            if continuation != 974:\n                raise ValueError(\'actual battle Main parent must retain3CE LONG\')\n            return (yield from self.battle_views[\'main\', MAIN_ENTRIES[target]](state, frame))\n        return (yield from super()._display_child(state, frame, target, continuation))\n\n    def main_scene_call(self, state, frame, target, continuation):\n        if target not in MAIN_ENTRIES:\n            return (yield from super().main_scene_call(state, frame, target, continuation))\n        self.require_current(state)\n        if self._started or continuation != 974:\n            raise ValueError(\'one actual Main478/490 invocation required\')\n        self._started = True\n        return (yield from self.views[\'display\', \'display_call_fields\'](state, frame, target, continuation))'}
VIEW_SPECS = {'support': {'_aux_text_call_fields': {'calls': {'clear_video_sprite_plane_fields': [1,
                                                                                     '_repeat_clear_video'],
                                                 'enqueue_sound_command_fields': [1, '_repeat_enqueue_sound'],
                                                 'wait_for_scene_sound_byte_fields': [1,
                                                                                      '_repeat_wait_sound']},
                                       'wait': None},
             'run_repeating_scene_presentation_fields': {'calls': {'_aux_text_call_fields': [5,
                                                                                             '_repeat_call']},
                                                         'wait': None}},
 'main': {'begin_nonreturning_scripted_scene_fields': {'calls': {'_campaign_call_fields': [1,
                                                                                           '_repeat_campaign_call']},
                                                       'wait': None}},
 'services': {'wait_for_scene_sound_byte_fields': {'calls': {},
                                                   'wait': ["memory.state.progress('scene-sound-byte')",
                                                            'frame = (yield from _repeat_wait(memory, '
                                                            'frame))']}},
 'story': {},
 'boot': {},
 'objects': {}}
MODULE_PATHS = {
    'support':'tools.high_level_main_flows.business_scene_support',
    'main':'tools.high_level_main_flows.business_main',
    'services':'tools.high_level_gameplay_flow.business_services',
    'story':'tools.high_level_scene_flows.business_scene',
    'boot':'tools.high_level_main_flows.business_boot',
    'objects':'tools.high_level_scene_flows.business_objects',
}


def _dump(node):
    return ast.dump(node,include_attributes=False)


def _code_shape(code):
    return tuple(getattr(code,name)for name in ('co_code','co_names','co_varnames',
        'co_argcount','co_posonlyargcount','co_kwonlyargcount','co_flags',
        'co_freevars','co_cellvars'))+(tuple(_code_shape(value)if type(value)is CodeType
            else value for value in code.co_consts),)


def _code_at(code,name):
    found=[item for item in code.co_consts if type(item)is CodeType and item.co_name==name]
    if len(found)!=1:raise ValueError('one complete original code owner required: '+name)
    return found[0]


def _cooperative_tree(group,original_tree):
    """Exact finite call/progress changes; inverse every whole FN and module."""
    result=copy.deepcopy(original_tree);inverses={}
    for index,node in enumerate(original_tree.body):
        if not isinstance(node,ast.FunctionDef)or node.name not in VIEW_SPECS[group]:continue
        if _dump(node)!=_dump(ast.parse(EXPECTED_SOURCE[group][node.name]).body[0]):
            raise ValueError('reviewed complete repeating-scene function changed: '+node.name)
        if any(isinstance(n,(ast.Yield,ast.YieldFrom))for n in ast.walk(node)):
            raise ValueError('original repeating-scene business owner must remain synchronous')
        spec=VIEW_SPECS[group][node.name];counts={name:0 for name in spec['calls']}
        changes=[];waits=[]
        old_wait=ast.parse(spec['wait'][0]).body[0]if spec['wait']else None
        new_wait=ast.parse(spec['wait'][1]).body[0]if spec['wait']else None

        class Lift(ast.NodeTransformer):
            def visit_Call(self,item):
                item=self.generic_visit(item)
                if isinstance(item.func,ast.Name)and item.func.id in counts:
                    before=copy.deepcopy(item);name=item.func.id;counts[name]+=1
                    item.func.id=spec['calls'][name][1]
                    after=ast.copy_location(ast.YieldFrom(value=item),item)
                    changes.append((before,copy.deepcopy(after)));return after
                return item

            def visit_Expr(self,item):
                if old_wait is not None and _dump(item)==_dump(old_wait):
                    waits.append(item);return ast.copy_location(copy.deepcopy(new_wait),item)
                return self.generic_visit(item)

        derived=Lift().visit(copy.deepcopy(node))
        if counts!={name:rule[0]for name,rule in spec['calls'].items()}or len(waits)!=(1 if spec['wait']else 0):
            raise ValueError('exact original repeating-scene call/wait count differs: '+node.name)
        remaining=list(changes)

        class Inverse(ast.NodeTransformer):
            def visit_Assign(self,item):
                if new_wait is not None and _dump(item)==_dump(new_wait):return copy.deepcopy(old_wait)
                return self.generic_visit(item)

            def visit_YieldFrom(self,item):
                for position,(before,after)in enumerate(remaining):
                    if _dump(item)==_dump(after):remaining.pop(position);return copy.deepcopy(before)
                raise ValueError('unadmitted repeating-scene cooperative call')

        inverse=Inverse().visit(copy.deepcopy(derived))
        if remaining or _dump(inverse)!=_dump(node):
            raise ValueError('complete original repeating-scene function inverse differs')
        result.body[index]=derived;inverses[index]=inverse
    if len(inverses)!=len(VIEW_SPECS[group]):raise ValueError('every finite repeating-scene view required')
    restored=copy.deepcopy(result)
    for index,node in inverses.items():restored.body[index]=node
    if _dump(restored)!=_dump(original_tree):raise ValueError('complete original business module inverse differs')
    return ast.fix_missing_locations(result)


def _pin_base():
    """Pin the actual reviewed base class, methods and complete-module codes."""
    if (BattleScenePrograms is not _battle.BattleScenePrograms
            or RepeatingScenePrograms.__bases__!=(BattleScenePrograms,)):
        raise ValueError('one actual unchanged BattleScenePrograms base required')
    tree=ast.parse(inspect.getsource(_battle),filename=_battle.__file__)
    candidates=[node for node in tree.body if isinstance(node,ast.ClassDef)and node.name=='BattleScenePrograms']
    if len(candidates)!=1 or _dump(candidates[0])!=_dump(ast.parse(EXPECTED_BASE['BattleScenePrograms']).body[0]):
        raise ValueError('complete reviewed BattleScenePrograms source changed')
    compiled=compile(tree,_battle.__file__,'exec',dont_inherit=True)
    cls_code=_code_at(compiled,'BattleScenePrograms');methods={}
    for method in candidates[0].body:
        if not isinstance(method,ast.FunctionDef):continue
        descriptor=vars(BattleScenePrograms).get(method.name)
        function=descriptor.__func__ if type(descriptor)is staticmethod else descriptor
        if (type(function)is not FunctionType or function.__globals__ is not vars(_battle)
                or function.__module__!=_battle.__name__
                or function.__qualname__!='BattleScenePrograms.'+method.name
                or _code_shape(function.__code__)!=_code_shape(_code_at(cls_code,method.name))):
            raise ValueError('actual complete-module battle base method required: '+method.name)
        methods[method.name]=(function,function.__code__)
    functions={}
    for name,source in EXPECTED_BASE.items():
        if name=='BattleScenePrograms':continue
        nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name==name]
        function=getattr(_battle,name)
        if (len(nodes)!=1 or _dump(nodes[0])!=_dump(ast.parse(source).body[0])
                or type(function)is not FunctionType or function.__globals__ is not vars(_battle)
                or _code_shape(function.__code__)!=_code_shape(_code_at(compiled,name))):
            raise ValueError('actual complete battle base utility required: '+name)
        functions[name]=(function,function.__code__)
    return methods,functions


class RepeatingScenePrograms(BattleScenePrograms):
    """Actual Main4B4/3CE and never-reentered3B732/580, on the same Scene."""
    def __init__(self,state):
        self._repeat_base_methods,self._repeat_base_functions=_pin_base()
        self._repeat_base_class=BattleScenePrograms
        self._repeat_class=RepeatingScenePrograms
        self._repeat_methods={name:(function,function.__code__)
            for name,function in vars(RepeatingScenePrograms).items()if type(function)is FunctionType}
        self._repeat_base_methods['__init__'][0](self,state)
        import importlib
        self.repeat_modules={group:importlib.import_module(path)for group,path in MODULE_PATHS.items()}
        self.repeat_originals={};self.repeat_original_codes={};self.repeat_views={}
        self.repeat_namespaces={};self.repeat_bindings={}
        for group,module in self.repeat_modules.items():
            tree=ast.parse(inspect.getsource(module),filename=module.__file__)
            nodes={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
            plain=compile(tree,module.__file__,'exec',dont_inherit=True)
            for name,source in EXPECTED_SOURCE[group].items():
                function=getattr(module,name)
                if (name not in nodes or _dump(nodes[name])!=_dump(ast.parse(source).body[0])
                        or type(function)is not FunctionType or function.__globals__ is not vars(module)
                        or function.__module__!=module.__name__ or function.__name__!=name
                        or function.__closure__ is not None or function.__code__.co_freevars
                        or _code_shape(function.__code__)!=_code_shape(_code_at(plain,name))):
                    raise ValueError('actual complete repeating-scene dependency required: '+name)
                self.repeat_originals[group,name]=function;self.repeat_original_codes[group,name]=function.__code__
            derived=compile(_cooperative_tree(group,tree),module.__file__,'exec',dont_inherit=True)
            namespace=dict(vars(module));self.repeat_namespaces[group]=namespace
            for name in VIEW_SPECS[group]:
                original=self.repeat_originals[group,name]
                view=FunctionType(_code_at(derived,name),namespace,name,original.__defaults__,None)
                view.__kwdefaults__=original.__kwdefaults__;view.__annotations__=dict(original.__annotations__)
                if not inspect.isgeneratorfunction(view):raise ValueError('whole repeating-scene view must be cooperative')
                self.repeat_views[group,name]=view
        self._repeat_view_owners=dict(self.repeat_views)
        self._repeat_view_codes={key:view.__code__ for key,view in self.repeat_views.items()}
        aliases={
            '_repeat_call':self.repeat_views['support','_aux_text_call_fields'],
            '_repeat_campaign_call':self.views['main','_campaign_call_fields'],
            '_repeat_clear_video':self._clear_video,
            '_repeat_enqueue_sound':self._enqueue_sound,
            '_repeat_wait_sound':self.repeat_views['services','wait_for_scene_sound_byte_fields'],
            '_repeat_wait':self._repeat_wait,
        }
        for group,namespace in self.repeat_namespaces.items():
            for name,value in aliases.items():
                if name in namespace:raise ValueError('private repeating-scene alias must not shadow original owner')
                namespace[name]=value;self.repeat_bindings[group,name]=value
        self.repeat_admissions=dict(whole_cooperative_views=4,
            source_owners=sum(len(v)for v in EXPECTED_SOURCE.values()),
            physical_outer_slots=[0x3CE,0x580],sound_wait_return=0x3B772,
            prefix_reentered=False,new_wait_types=0)

    def _require_repeat_base(self):
        if (BattleScenePrograms is not self._repeat_base_class
                or _battle.BattleScenePrograms is not self._repeat_base_class
                or RepeatingScenePrograms is not self._repeat_class
                or RepeatingScenePrograms.__bases__!=(self._repeat_base_class,)):
            raise ValueError('actual repeating-scene base class changed')
        for name,(function,code)in self._repeat_methods.items():
            if vars(self._repeat_class).get(name)is not function or function.__code__ is not code:
                raise ValueError('actual repeating-scene coordinator method changed: '+name)
        for name,(function,code)in self._repeat_base_methods.items():
            descriptor=vars(self._repeat_base_class).get(name)
            actual=descriptor.__func__ if type(descriptor)is staticmethod else descriptor
            if actual is not function or function.__code__ is not code:
                raise ValueError('actual battle base method changed across repeating wait: '+name)
        for name,(function,code)in self._repeat_base_functions.items():
            if getattr(_battle,name)is not function or function.__code__ is not code:
                raise ValueError('actual battle base utility changed across repeating wait: '+name)

    def require_current(self,state):
        self._require_repeat_base()
        self._repeat_base_methods['require_current'][0](self,state)
        if not hasattr(self,'repeat_originals'):return
        for (group,name),original in self.repeat_originals.items():
            if (getattr(self.repeat_modules[group],name)is not original
                    or original.__code__ is not self.repeat_original_codes[group,name]):
                raise ValueError('actual repeating-scene dependency changed: '+name)
        if self.repeat_views.keys()!=self._repeat_view_owners.keys():raise ValueError('finite repeating-scene graph changed')
        for key,view in self._repeat_view_owners.items():
            if self.repeat_views[key]is not view or view.__code__ is not self._repeat_view_codes[key]:
                raise ValueError('whole repeating-scene private view changed: '+key[1])
        for (group,name),value in self.repeat_bindings.items():
            if self.repeat_namespaces[group].get(name)is not value:
                raise ValueError('private repeating-scene continuation binding changed: '+name)

    def _repeat_wait(self,memory,frame):
        self.require_current(memory.state)
        if type(memory)is not SceneRefreshMemory:raise ValueError('actual Scene refresh memory required')
        frame=memory.sync_status(_movement_frame(memory.state,frame))
        wait=GameplaySceneWait(memory.state,frame,memory.state.sr,'scene-sound-byte',0x83CC).validate()
        returned=yield wait
        self.require_current(memory.state)
        returned=_movement_frame(memory.state,returned)
        if (returned.stack_cursor.base!=frame.stack_cursor.base or memory.state.sr!=wait.status_word
                or returned.status!=(wait.status_word&31)):
            raise ValueError('actual83CC IRQ must restore the same physical SP and complete SR')
        return returned

    def _forward_waits(self,program):
        """Guard both sides of the reused exact device-view suspensions."""
        first=True;received=None
        try:
            while True:
                self.require_current(self.state)
                try:waiting=next(program)if first else program.send(received)
                except StopIteration as finished:return finished.value
                first=False
                if type(waiting)is not GameplaySceneWait or waiting.state is not self.state:
                    raise ValueError('one exact same-Scene reused initialization wait required')
                waiting.validate()
                received=yield waiting
                self.require_current(self.state)
                if waiting.needs_interrupt or received is not waiting.frame or self.state.sr!=waiting.status_word:
                    raise ValueError('device progress must retain the actual waiting frame and full SR')
        finally:
            program.close()

    def _clear_video(self,memory,frame):
        self.require_current(memory.state)
        return (yield from self._forward_waits(
            self.battle_views['services','clear_video_sprite_plane_fields'](memory,frame)))

    def _enqueue_sound(self,memory,frame,command=None):
        self.require_current(memory.state)
        return (yield from self._forward_waits(
            self.battle_views['services','enqueue_sound_command_fields'](memory,frame,command)))

    def _campaign_child(self,state,frame,target,continuation):
        self.require_current(state)
        if (target,continuation)==(0x3B732,0x580):
            return (yield from self.repeat_views['support','run_repeating_scene_presentation_fields'](state,frame))
        return (yield from super()._campaign_child(state,frame,target,continuation))

    def _display_child(self,state,frame,target,continuation):
        self.require_current(state)
        if target==0x4B4:
            if continuation!=0x3CE:raise MovementContinuationBoundary(target,frame,'actual Main4B4 requires3CE')
            return (yield from self.repeat_views['main','begin_nonreturning_scripted_scene_fields'](state,frame))
        return (yield from super()._display_child(state,frame,target,continuation))

    def main_scene_call(self,state,frame,target,continuation):
        if target!=0x4B4:return (yield from super().main_scene_call(state,frame,target,continuation))
        self.require_current(state)
        if self._started or continuation!=0x3CE:
            raise ValueError('one actual Main4B4/3CE invocation required')
        self._started=True
        return (yield from self.views['display','display_call_fields'](state,frame,target,continuation))

# B168: seven original story darken CALLs; one exact shared helper.
EXPECTED_SOURCE['story']['_story_darken_fields'] = 'def _story_darken_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,\n        continuation: Long) -> FirstDeploymentFrame:\n    """The original MOVEQ1 and CALL3AA20; reuse the sole palette owner."""\n    frame = _story_move_fields(memory, frame, \'target_x\', 1, 32)\n    return _story_call_fields(memory, frame, 0x3AA20, continuation)\n'
