"""Whole startup, map-video, scenario and shared-clear Main continuations.

Only seven existing complete parents gain finite yield-from propagation.
The original services, data, hardware, frame and physical CALL owners remain
the sole implementation; no implicit device progress or new wait is created.
"""
import ast
import copy
import importlib
import inspect
from types import CodeType, FunctionType

from . import battle_trigger_steps as battle
from .contexts_services import SceneRefreshMemory
from .scene_load_steps import GameplaySceneWait
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary

BattleScenePrograms=battle.BattleScenePrograms
MODULE_PATHS={
    'main':'tools.high_level_main_flows.business_main',
    'lowbank':'tools.high_level_main_flows.business_lowbank',
    'map':'tools.high_level_main_flows.business_map',
    'commands':'tools.high_level_main_flows.business_commands',
}
MAIN_ENTRIES={0x3D8:'process_startup_scene_fields',0x3DC:'reset_menu_sprite_slots_fields',
    0x3F4:'refresh_information_panel_fields',0x3FC:'continue_platform_scene_initialization_fields'}
EXPECTED_SOURCE = {'main': {'process_startup_scene_fields': 'def process_startup_scene_fields(state: SceneState, frame: '
                                          'FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                          '    """3D8: process startup scene; original stage and child '
                                          'tokens."""\n'
                                          '    frame = _city_ui_frame_fields(state, frame, 984)\n'
                                          '    frame = _campaign_call_fields(state, frame, 37872, 1262)\n'
                                          '    return frame',
          'reset_menu_sprite_slots_fields': 'def reset_menu_sprite_slots_fields(state: SceneState, frame: '
                                            'FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                            '    """3DC/5A4: original display disable and descending '
                                            'sixteen-BYTE sprite index reset."""\n'
                                            '    frame = _campaign_screen_enter_fields(state, frame, 988)\n'
                                            "    frame = _movement_move(state, frame, 'target_x', "
                                            'state.read(4294964742, 2), 16)\n'
                                            "    frame = _movement_move(state, frame, 'target_x', "
                                            'low8(frame.target_x) & 191, 8)\n'
                                            '    frame = _campaign_emit_fields(state, frame, 1456, 12582916, '
                                            'low16(frame.target_x))\n'
                                            '    frame = _campaign_call_fields(state, frame, 41394, 1468)\n'
                                            '    frame = first_replace(frame, '
                                            'roster=state.table_at(4294964304).cursor())\n'
                                            "    frame = _movement_move(state, frame, 'target_x', 15, 16)\n"
                                            '    while True:\n'
                                            '        frame = _campaign_emit_fields(state, frame, 1476, '
                                            'frame.roster.advance(s16(low16(frame.target_x))).base, '
                                            'low8(frame.target_x), 1)\n'
                                            '        frame, more = _campaign_screen_countdown_fields(frame, '
                                            "'target_x')\n"
                                            '        if not more:\n'
                                            '            return frame',
          'refresh_information_panel_fields': 'def refresh_information_panel_fields(state: SceneState, '
                                              'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                              '    """3F4: refresh information panel; original stage and '
                                              'child tokens."""\n'
                                              '    frame = _city_ui_frame_fields(state, frame, 1012)\n'
                                              '    frame = _campaign_call_fields(state, frame, 42530, 3714)\n'
                                              '    return frame',
          'continue_platform_scene_initialization_fields': 'def '
                                                           'continue_platform_scene_initialization_fields(state: '
                                                           'SceneState, frame: FirstDeploymentFrame) -> '
                                                           'FirstDeploymentFrame:\n'
                                                           '    """3FC: continue platform scene '
                                                           'initialization; original stage and child '
                                                           'tokens."""\n'
                                                           '    frame = _city_ui_frame_fields(state, frame, '
                                                           '1020)\n'
                                                           '    return _campaign_tail_fields(state, frame, '
                                                           '1548)'},
 'lowbank': {'initialize_scene_growth_and_tiles_fields': 'def '
                                                         'initialize_scene_growth_and_tiles_fields(state: '
                                                         'SceneState, frame: FirstDeploymentFrame) -> '
                                                         'FirstDeploymentFrame:\n'
                                                         '    """93F0..949E: real initial tile image, four '
                                                         'layout rows and controller-region option."""\n'
                                                         '    from .business_movement_support import '
                                                         '_movement_arithmetic_long\n'
                                                         '    frame = _campaign_ui_frame_fields(state, '
                                                         'frame, 37872)\n'
                                                         '    state.sr = 9984\n'
                                                         '    frame = first_replace(frame, status=0)\n'
                                                         '    frame = _campaign_ui_move_fields(state, frame, '
                                                         "'target_x', state.read(4294964742, 2))\n"
                                                         '    frame = _campaign_ui_move_fields(state, frame, '
                                                         "'target_x', low8(frame.target_x) & 191, 8)\n"
                                                         '    frame = _campaign_ui_write_fields(state, '
                                                         'frame, 37884, 12582916, low16(frame.target_x))\n'
                                                         '    frame = _campaign_ui_call_fields(state, frame, '
                                                         '26830, 37896)\n'
                                                         '    frame = _campaign_ui_write_fields(state, '
                                                         'frame, 37896, 12582916, 1073741824, 4)\n'
                                                         '    frame = first_replace(frame, '
                                                         'roster=state.table_at(38230).cursor())\n'
                                                         '    frame = _campaign_ui_move_fields(state, frame, '
                                                         "'target_x', 439)\n"
                                                         '    frame = '
                                                         '_campaign_ui_copy_panel_longs_fields(state, frame, '
                                                         "'roster', 'target_x', 37914, 12582912)\n"
                                                         '    frame = _campaign_ui_move_fields(state, frame, '
                                                         "'offset_x', 11, 32)\n"
                                                         '    frame = _campaign_ui_move_fields(state, frame, '
                                                         "'offset_y', 3, 32)\n"
                                                         '    frame = _campaign_ui_move_fields(state, frame, '
                                                         "'distance', 32769)\n"
                                                         '    frame = _campaign_ui_move_fields(state, frame, '
                                                         "'target_x', 1176240131, 32)\n"
                                                         '    while True:\n'
                                                         '        frame = _campaign_ui_move_fields(state, '
                                                         "frame, 'choice', low16(frame.offset_x))\n"
                                                         '        frame = _campaign_ui_write_fields(state, '
                                                         'frame, 37940, 12582916, frame.target_x, 4)\n'
                                                         '        while True:\n'
                                                         '            frame = '
                                                         '_campaign_ui_write_fields(state, frame, 37946, '
                                                         '12582912, low16(frame.distance))\n'
                                                         '            frame = '
                                                         '_campaign_ui_arithmetic_fields(state, frame, '
                                                         "'distance', 1)\n"
                                                         '            frame, more = '
                                                         "_campaign_ui_loop_fields(frame, 'choice')\n"
                                                         '            if not more:\n'
                                                         '                break\n'
                                                         '        frame = _movement_arithmetic_long(state, '
                                                         "frame, 'target_x', 8388608)\n"
                                                         '        frame, more = '
                                                         "_campaign_ui_loop_fields(frame, 'offset_y')\n"
                                                         '        if not more:\n'
                                                         '            break\n'
                                                         '    frame = _campaign_ui_bit_fields(state, frame, '
                                                         'state.read(10551297, 1), 7)\n'
                                                         '    if not frame.status & 4:\n'
                                                         '        frame = _campaign_ui_write_fields(state, '
                                                         'frame, 37980, 12582916, 36610)\n'
                                                         '        frame = _campaign_ui_write_fields(state, '
                                                         'frame, 37988, 12582916, 1714421763, 4)\n'
                                                         '        frame = _campaign_ui_write_fields(state, '
                                                         'frame, 37998, 12582912, 32821)\n'
                                                         '        frame = _campaign_ui_write_fields(state, '
                                                         'frame, 38006, 12582912, 32822)\n'
                                                         '    frame = _campaign_ui_move_fields(state, frame, '
                                                         "'target_x', 0, 32)\n"
                                                         '    frame = _campaign_ui_call_fields(state, frame, '
                                                         '33042, 38022)\n'
                                                         '    frame = _campaign_ui_write_fields(state, '
                                                         'frame, 38022, 4294964760, 40)\n'
                                                         '    frame = _campaign_ui_write_fields(state, '
                                                         'frame, 38028, 4294964744, 300)\n'
                                                         '    state.sr = 9472\n'
                                                         '    frame = first_replace(frame, status=0)\n'
                                                         '    return _campaign_ui_write_fields(state, frame, '
                                                         '38038, 4294964754, 256)'},
 'map': {'initialize_world_map_view_frame_fields': 'def initialize_world_map_view_frame_fields(state: '
                                                   'SceneState, frame: FirstDeploymentFrame) -> '
                                                   'FirstDeploymentFrame:\n'
                                                   '    """A1B2: real video initialization, streams,160 '
                                                   'LONGs and initial28rows."""\n'
                                                   '    from .business_movement_support import '
                                                   '_movement_move\n'
                                                   '    frame = display_frame_fields(state, frame)\n'
                                                   '    frame = display_call_fields(state, frame, 26662, '
                                                   '41400)\n'
                                                   '    frame = display_store_fields(state, frame, 41400, '
                                                   '4294963144, 0, clear=True)\n'
                                                   '    frame = display_call_fields(state, frame, 26830, '
                                                   '41410)\n'
                                                   '    frame = display_store_fields(state, frame, 41410, '
                                                   '12582916, 33799)\n'
                                                   '    frame = display_store_fields(state, frame, 41418, '
                                                   '4294963988, state.read(4294964054, 2))\n'
                                                   '    frame = display_store_fields(state, frame, 41424, '
                                                   '4294963992, state.read(4294964052, 2))\n'
                                                   '    frame = display_store_fields(state, frame, 41430, '
                                                   '12582916, 1073741824, 4)\n'
                                                   '    frame = display_address_fields(state, frame, '
                                                   "'roster', 845342)\n"
                                                   '    frame = display_address_fields(state, frame, '
                                                   "'candidates', 844954)\n"
                                                   '    frame = display_move_fields(state, frame, '
                                                   "'target_x', state.read(865474, 2))\n"
                                                   '    frame = display_call_fields(state, frame, 44540, '
                                                   '41464)\n'
                                                   '    frame = display_store_fields(state, frame, 41464, '
                                                   '4294964094, 1)\n'
                                                   '    frame = display_address_fields(state, frame, '
                                                   "'roster', 865482)\n"
                                                   '    frame = display_move_fields(state, frame, '
                                                   "'target_x', 159)\n"
                                                   '    frame = display_store_fields(state, frame, 41480, '
                                                   '12582916, 2013265921, 4)\n'
                                                   '    while True:\n'
                                                   '        pixels = frame.roster.long()\n'
                                                   '        frame = first_replace(frame, '
                                                   'roster=frame.roster.advance(4))\n'
                                                   '        frame = display_store_fields(state, frame, '
                                                   '41490, 12582912, pixels, 4)\n'
                                                   '        frame, more = display_loop_fields(frame, '
                                                   "'target_x')\n"
                                                   '        if not more:\n'
                                                   '            break\n'
                                                   '    frame = display_store_fields(state, frame, 41500, '
                                                   '4294964002, 0, clear=True)\n'
                                                   '    frame = display_store_fields(state, frame, 41504, '
                                                   '4294964754, 512)\n'
                                                   "    frame = _movement_move(state, frame, 'target_x', 0, "
                                                   '16)\n'
                                                   '    for pc, address in ((41512, 4294963986), (41516, '
                                                   '4294963990), (41520, 4294964738)):\n'
                                                   '        frame = display_store_fields(state, frame, pc, '
                                                   'address, low16(frame.target_x))\n'
                                                   '    frame = display_store_fields(state, frame, 41524, '
                                                   '4294963996, 2, 1)\n'
                                                   '    frame = display_move_fields(state, frame, '
                                                   "'target_x', 1, 32)\n"
                                                   '    frame = display_call_fields(state, frame, 33042, '
                                                   '41538)\n'
                                                   '    frame = display_call_fields(state, frame, 41592, '
                                                   '41542)\n'
                                                   '    frame = display_store_fields(state, frame, 41542, '
                                                   '12582916, 35584)\n'
                                                   '    frame = display_store_fields(state, frame, 41550, '
                                                   '4294964932, 0, clear=True)\n'
                                                   '    frame = display_move_fields(state, frame, '
                                                   "'target_x', state.read(4294964132, 2))\n"
                                                   '    frame = display_move_fields(state, frame, '
                                                   "'target_x', low16(frame.target_x) & 1)\n"
                                                   '    frame = display_store_fields(state, frame, 41562, '
                                                   '4294964132, low16(frame.target_x))\n'
                                                   '    frame = display_call_fields(state, frame, 21186, '
                                                   '41572)\n'
                                                   '    frame = display_move_fields(state, frame, '
                                                   "'target_x', state.read(4294964742, 2))\n"
                                                   '    frame = display_move_fields(state, frame, '
                                                   "'target_x', low8(frame.target_x) | 64, 8)\n"
                                                   '    frame = display_store_fields(state, frame, 41580, '
                                                   '12582916, low16(frame.target_x))\n'
                                                   '    return display_status_fields(state, frame, 9472)'},
 'commands': {'draw_current_scenario_prompt_frame_fields': 'def '
                                                           'draw_current_scenario_prompt_frame_fields(state: '
                                                           'SceneState, frame: FirstDeploymentFrame) -> '
                                                           'FirstDeploymentFrame:\n'
                                                           '    """A622: scenario screen phases retain their '
                                                           'true display/audio child boundaries."""\n'
                                                           '    frame = _city_ui_frame_fields(state, frame, '
                                                           '42530)\n'
                                                           '    frame = _command_panel_status_fields(state, '
                                                           'frame, 9984)\n'
                                                           '    frame = _movement_move(state, frame, '
                                                           "'target_x', state.read(4294964742, 2), 16)\n"
                                                           '    frame = _movement_move(state, frame, '
                                                           "'target_x', low8(frame.target_x) & 191, 8)\n"
                                                           '    frame = _city_ui_store_fields(state, frame, '
                                                           '12582916, low16(frame.target_x))\n'
                                                           '    frame = _campaign_ui_call_fields(state, '
                                                           'frame, 26830, 42554)\n'
                                                           '    frame = _command_panel_pointer_fields(state, '
                                                           "frame, 'auxiliary', 12582916)\n"
                                                           '    frame = _command_panel_pointer_fields(state, '
                                                           "frame, 'scratch', 12582912)\n"
                                                           '    frame = _movement_move_long(state, frame, '
                                                           "'target_x', 5)\n"
                                                           '    frame = _campaign_ui_call_fields(state, '
                                                           'frame, 33042, 42574)\n'
                                                           '    frame = _campaign_ui_call_fields(state, '
                                                           'frame, 42622, 42578)\n'
                                                           '    frame = _campaign_ui_call_fields(state, '
                                                           'frame, 42848, 42582)\n'
                                                           '    frame = _campaign_ui_call_fields(state, '
                                                           'frame, 43054, 42588)\n'
                                                           '    frame = _city_ui_store_fields(state, frame, '
                                                           '4294964058, 0, 2, True)\n'
                                                           '    frame = _campaign_ui_call_fields(state, '
                                                           'frame, 43300, 42596)\n'
                                                           '    frame = _city_ui_store_fields(state, frame, '
                                                           '4294963990, 0, 2, True)\n'
                                                           '    frame = _city_ui_store_fields(state, frame, '
                                                           '4294963986, 0, 2, True)\n'
                                                           '    frame = _city_ui_store_fields(state, frame, '
                                                           '4294964932, 4)\n'
                                                           '    frame = _campaign_ui_call_fields(state, '
                                                           'frame, 42794, 42616)\n'
                                                           '    return _command_panel_status_fields(state, '
                                                           'frame, 9472)'}}
VIEW_SPECS = {'main': {'process_startup_scene_fields': {'_campaign_call_fields': [1, '_startup_campaign_call']},
          'reset_menu_sprite_slots_fields': {'_campaign_call_fields': [1, '_startup_campaign_call']},
          'refresh_information_panel_fields': {'_campaign_call_fields': [1, '_startup_campaign_call']},
          'continue_platform_scene_initialization_fields': {'_campaign_tail_fields': [1,
                                                                                      '_startup_clear_tail']}},
 'lowbank': {'initialize_scene_growth_and_tiles_fields': {'_campaign_ui_call_fields': [2,
                                                                                       '_startup_campaign_call']}},
 'map': {'initialize_world_map_view_frame_fields': {'display_call_fields': [6, '_startup_display_call']}},
 'commands': {'draw_current_scenario_prompt_frame_fields': {'_campaign_ui_call_fields': [7,
                                                                                         '_startup_campaign_call']}}}
CALL_PAIRS = {'main': {'process_startup_scene_fields': [{'kind': 'call', 'target': 37872, 'returned': 1262}],
          'reset_menu_sprite_slots_fields': [{'kind': 'call', 'target': 41394, 'returned': 1468}],
          'refresh_information_panel_fields': [{'kind': 'call', 'target': 42530, 'returned': 3714}],
          'continue_platform_scene_initialization_fields': [{'kind': 'tail',
                                                             'target': 1548,
                                                             'returned': None}]},
 'lowbank': {'initialize_scene_growth_and_tiles_fields': [{'kind': 'call',
                                                           'target': 26830,
                                                           'returned': 37896},
                                                          {'kind': 'call',
                                                           'target': 33042,
                                                           'returned': 38022}]},
 'map': {'initialize_world_map_view_frame_fields': [{'kind': 'call', 'target': 26662, 'returned': 41400},
                                                    {'kind': 'call', 'target': 26830, 'returned': 41410},
                                                    {'kind': 'call', 'target': 44540, 'returned': 41464},
                                                    {'kind': 'call', 'target': 33042, 'returned': 41538},
                                                    {'kind': 'call', 'target': 41592, 'returned': 41542},
                                                    {'kind': 'call', 'target': 21186, 'returned': 41572}]},
 'commands': {'draw_current_scenario_prompt_frame_fields': [{'kind': 'call',
                                                             'target': 26830,
                                                             'returned': 42554},
                                                            {'kind': 'call',
                                                             'target': 33042,
                                                             'returned': 42574},
                                                            {'kind': 'call',
                                                             'target': 42622,
                                                             'returned': 42578},
                                                            {'kind': 'call',
                                                             'target': 42848,
                                                             'returned': 42582},
                                                            {'kind': 'call',
                                                             'target': 43054,
                                                             'returned': 42588},
                                                            {'kind': 'call',
                                                             'target': 43300,
                                                             'returned': 42596},
                                                            {'kind': 'call',
                                                             'target': 42794,
                                                             'returned': 42616}]}}
REUSED_SOURCE = {'tools.high_level_main_flows.business_main': {'_campaign_screen_enter_fields': 'def '
                                                                                '_campaign_screen_enter_fields(state: '
                                                                                'SceneState, frame: '
                                                                                'FirstDeploymentFrame, '
                                                                                'entry: int) -> '
                                                                                'FirstDeploymentFrame:\n'
                                                                                '    frame = '
                                                                                '_city_ui_frame_fields(state, '
                                                                                'frame, entry)\n'
                                                                                '    state.sr = 9984\n'
                                                                                '    return '
                                                                                'first_replace(frame, '
                                                                                'status=0)',
                                               '_campaign_screen_countdown_fields': 'def '
                                                                                    '_campaign_screen_countdown_fields(frame: '
                                                                                    'FirstDeploymentFrame, '
                                                                                    'carrier: str) -> '
                                                                                    'tuple[FirstDeploymentFrame, '
                                                                                    'bool]:\n'
                                                                                    '    from '
                                                                                    '.business_lowbank '
                                                                                    'import '
                                                                                    '_campaign_ui_loop_fields\n'
                                                                                    '    return '
                                                                                    '_campaign_ui_loop_fields(frame, '
                                                                                    'carrier)',
                                               '_campaign_emit_fields': 'def _campaign_emit_fields(state: '
                                                                        'SceneState, frame: '
                                                                        'FirstDeploymentFrame, instruction: '
                                                                        'int, address: int, value: int, '
                                                                        'size: int=2, clear: bool=False) -> '
                                                                        'FirstDeploymentFrame:\n'
                                                                        '    """Use the real existing '
                                                                        'RAM/hardware bus; missing hardware '
                                                                        'stops at the actual write."""\n'
                                                                        '    try:\n'
                                                                        '        return '
                                                                        '_city_ui_store_fields(state, frame, '
                                                                        'address, value, size, clear)\n'
                                                                        '    except Boundary:\n'
                                                                        '        raise '
                                                                        'MovementContinuationBoundary(instruction, '
                                                                        "frame, 'actual campaign DATA access "
                                                                        "unavailable')"},
 'tools.high_level_main_flows.business_lowbank': {'_campaign_ui_call_fields': 'def '
                                                                              '_campaign_ui_call_fields(state: '
                                                                              'SceneState, frame: '
                                                                              'FirstDeploymentFrame, target: '
                                                                              'int, token: int) -> '
                                                                              'FirstDeploymentFrame:\n'
                                                                              '    from .business_main '
                                                                              'import _campaign_call_fields\n'
                                                                              '    return '
                                                                              '_campaign_call_fields(state, '
                                                                              'frame, target, token)',
                                                  'upload_selected_mode_tile_rows_fields': 'def '
                                                                                           'upload_selected_mode_tile_rows_fields(state: '
                                                                                           'SceneState, '
                                                                                           'frame: '
                                                                                           'FirstDeploymentFrame) '
                                                                                           '-> '
                                                                                           'FirstDeploymentFrame:\n'
                                                                                           '    '
                                                                                           '"""A760..A78E: '
                                                                                           'saved actual A0, '
                                                                                           'two tile rows '
                                                                                           'and original '
                                                                                           'LSL.W #5 mode '
                                                                                           'index."""\n'
                                                                                           '    frame = '
                                                                                           '_campaign_ui_frame_fields(state, '
                                                                                           'frame, 42848)\n'
                                                                                           '    stack = '
                                                                                           'frame.stack_cursor.advance(-4)\n'
                                                                                           '    '
                                                                                           'stack.set_long(0, '
                                                                                           'frame.roster.base)\n'
                                                                                           '    frame = '
                                                                                           'first_replace(frame, '
                                                                                           'stack_cursor=stack)\n'
                                                                                           '    from '
                                                                                           '.business_movement_support '
                                                                                           'import '
                                                                                           '_movement_test_long\n'
                                                                                           '    frame = '
                                                                                           '_movement_test_long(state, '
                                                                                           'frame, '
                                                                                           'frame.roster.base)\n'
                                                                                           '    frame = '
                                                                                           'first_replace(frame, '
                                                                                           'auxiliary=state.table_at(12582912).cursor(), '
                                                                                           'roster=state.table_at(42910).cursor())\n'
                                                                                           '    frame = '
                                                                                           '_campaign_ui_move_fields(state, '
                                                                                           "frame, 'unit', "
                                                                                           'state.read(4294964048, '
                                                                                           '2))\n'
                                                                                           '    frame = '
                                                                                           '_campaign_ui_shift_fields(state, '
                                                                                           "frame, 'unit', "
                                                                                           '5)\n'
                                                                                           '    frame = '
                                                                                           '_campaign_ui_write_fields(state, '
                                                                                           'frame, 42866, '
                                                                                           '12582916, '
                                                                                           '1092616195, 4)\n'
                                                                                           '    frame = '
                                                                                           '_campaign_ui_call_fields(state, '
                                                                                           'frame, 42894, '
                                                                                           '42878)\n'
                                                                                           '    frame = '
                                                                                           '_campaign_ui_write_fields(state, '
                                                                                           'frame, 42878, '
                                                                                           '12582916, '
                                                                                           '1101004803, 4)\n'
                                                                                           '    frame = '
                                                                                           '_campaign_ui_call_fields(state, '
                                                                                           'frame, 42894, '
                                                                                           '42890)\n'
                                                                                           '    restored = '
                                                                                           'frame.stack_cursor.long()\n'
                                                                                           '    return '
                                                                                           'first_replace(frame, '
                                                                                           'roster=state.table_at(restored).cursor(), '
                                                                                           'stack_cursor=frame.stack_cursor.advance(4))',
                                                  'upload_selected_tile_row_fields': 'def '
                                                                                     'upload_selected_tile_row_fields(state: '
                                                                                     'SceneState, frame: '
                                                                                     'FirstDeploymentFrame) '
                                                                                     '-> '
                                                                                     'FirstDeploymentFrame:\n'
                                                                                     '    """A78E..A79E: '
                                                                                     'eight WORDs from '
                                                                                     'passed A0/D2, keeping '
                                                                                     'each real video '
                                                                                     'write."""\n'
                                                                                     '    frame = '
                                                                                     '_campaign_ui_frame_fields(state, '
                                                                                     'frame, 42894)\n'
                                                                                     '    frame = '
                                                                                     '_campaign_ui_move_fields(state, '
                                                                                     "frame, 'target_y', 7)\n"
                                                                                     '    while True:\n'
                                                                                     '        value = '
                                                                                     'frame.roster.word(low16(frame.unit))\n'
                                                                                     '        frame = '
                                                                                     '_campaign_ui_write_fields(state, '
                                                                                     'frame, 42898, '
                                                                                     'frame.auxiliary.base, '
                                                                                     'value)\n'
                                                                                     '        frame = '
                                                                                     '_campaign_ui_arithmetic_fields(state, '
                                                                                     "frame, 'unit', 2)\n"
                                                                                     '        frame, more = '
                                                                                     '_campaign_ui_loop_fields(frame, '
                                                                                     "'target_y')\n"
                                                                                     '        if not more:\n'
                                                                                     '            return '
                                                                                     'frame'},
 'tools.high_level_main_flows.business_commands': {'_campaign_ui_call_fields': 'def '
                                                                               '_campaign_ui_call_fields(state: '
                                                                               'SceneState, frame: '
                                                                               'FirstDeploymentFrame, '
                                                                               'target: int, continuation: '
                                                                               'int) -> '
                                                                               'FirstDeploymentFrame:\n'
                                                                               '    """Use the one campaign '
                                                                               'call bridge; the caller owns '
                                                                               'its real LONG return '
                                                                               'slot."""\n'
                                                                               '    from .business_main '
                                                                               'import '
                                                                               '_campaign_call_fields\n'
                                                                               '    return '
                                                                               '_campaign_call_fields(state, '
                                                                               'frame, target, continuation)',
                                                   'append_scenario_owner_glyphs_frame_fields': 'def '
                                                                                                'append_scenario_owner_glyphs_frame_fields(state: '
                                                                                                'SceneState, '
                                                                                                'frame: '
                                                                                                'FirstDeploymentFrame) '
                                                                                                '-> '
                                                                                                'FirstDeploymentFrame:\n'
                                                                                                '    '
                                                                                                '"""A67E: '
                                                                                                'top, '
                                                                                                'twenty-four '
                                                                                                'middle and '
                                                                                                'bottom '
                                                                                                'border rows '
                                                                                                'at the '
                                                                                                'actual '
                                                                                                'ports."""\n'
                                                                                                '    frame = '
                                                                                                '_city_ui_frame_fields(state, '
                                                                                                'frame, '
                                                                                                '42622)\n'
                                                                                                '    frame = '
                                                                                                '_movement_move_long(state, '
                                                                                                'frame, '
                                                                                                "'unit', "
                                                                                                '1082130435)\n'
                                                                                                '    frame = '
                                                                                                '_city_ui_store_fields(state, '
                                                                                                'frame, '
                                                                                                'frame.auxiliary.base, '
                                                                                                'frame.unit, '
                                                                                                '4)\n'
                                                                                                '    for '
                                                                                                'value in '
                                                                                                '(0, 0, '
                                                                                                '1152):\n'
                                                                                                '        '
                                                                                                'frame = '
                                                                                                '_city_ui_store_fields(state, '
                                                                                                'frame, '
                                                                                                'frame.scratch.base, '
                                                                                                'value)\n'
                                                                                                '    frame = '
                                                                                                '_movement_move(state, '
                                                                                                'frame, '
                                                                                                "'target_y', "
                                                                                                '33, 16)\n'
                                                                                                '    frame = '
                                                                                                '_command_panel_repeat_fields(state, '
                                                                                                'frame, '
                                                                                                'frame.scratch.base, '
                                                                                                '1153, '
                                                                                                "'target_y')\n"
                                                                                                '    for '
                                                                                                'value in '
                                                                                                '(3200, 0, '
                                                                                                '0):\n'
                                                                                                '        '
                                                                                                'frame = '
                                                                                                '_city_ui_store_fields(state, '
                                                                                                'frame, '
                                                                                                'frame.scratch.base, '
                                                                                                'value)\n'
                                                                                                '    frame = '
                                                                                                '_movement_move(state, '
                                                                                                'frame, '
                                                                                                "'target_x', "
                                                                                                '23, 16)\n'
                                                                                                '    while '
                                                                                                'True:\n'
                                                                                                '        '
                                                                                                'frame = '
                                                                                                '_movement_arithmetic_long(state, '
                                                                                                'frame, '
                                                                                                "'unit', "
                                                                                                '8388608)\n'
                                                                                                '        '
                                                                                                'frame = '
                                                                                                '_city_ui_store_fields(state, '
                                                                                                'frame, '
                                                                                                'frame.auxiliary.base, '
                                                                                                'frame.unit, '
                                                                                                '4)\n'
                                                                                                '        for '
                                                                                                'value in '
                                                                                                '(0, 0, '
                                                                                                '1154):\n'
                                                                                                '            '
                                                                                                'frame = '
                                                                                                '_city_ui_store_fields(state, '
                                                                                                'frame, '
                                                                                                'frame.scratch.base, '
                                                                                                'value)\n'
                                                                                                '        '
                                                                                                'frame = '
                                                                                                '_movement_move(state, '
                                                                                                'frame, '
                                                                                                "'target_y', "
                                                                                                '33, 16)\n'
                                                                                                '        '
                                                                                                'frame = '
                                                                                                '_command_panel_repeat_fields(state, '
                                                                                                'frame, '
                                                                                                'frame.scratch.base, '
                                                                                                '1155, '
                                                                                                "'target_y')\n"
                                                                                                '        for '
                                                                                                'value in '
                                                                                                '(3202, 0, '
                                                                                                '0):\n'
                                                                                                '            '
                                                                                                'frame = '
                                                                                                '_city_ui_store_fields(state, '
                                                                                                'frame, '
                                                                                                'frame.scratch.base, '
                                                                                                'value)\n'
                                                                                                '        '
                                                                                                'frame, '
                                                                                                'again = '
                                                                                                '_command_panel_dbra_fields(frame, '
                                                                                                "'target_x')\n"
                                                                                                '        if '
                                                                                                'not again:\n'
                                                                                                '            '
                                                                                                'break\n'
                                                                                                '    frame = '
                                                                                                '_movement_arithmetic_long(state, '
                                                                                                'frame, '
                                                                                                "'unit', "
                                                                                                '8388608)\n'
                                                                                                '    frame = '
                                                                                                '_city_ui_store_fields(state, '
                                                                                                'frame, '
                                                                                                'frame.auxiliary.base, '
                                                                                                'frame.unit, '
                                                                                                '4)\n'
                                                                                                '    for '
                                                                                                'value in '
                                                                                                '(0, 0, '
                                                                                                '5248):\n'
                                                                                                '        '
                                                                                                'frame = '
                                                                                                '_city_ui_store_fields(state, '
                                                                                                'frame, '
                                                                                                'frame.scratch.base, '
                                                                                                'value)\n'
                                                                                                '    frame = '
                                                                                                '_movement_move(state, '
                                                                                                'frame, '
                                                                                                "'target_y', "
                                                                                                '33, 16)\n'
                                                                                                '    frame = '
                                                                                                '_command_panel_repeat_fields(state, '
                                                                                                'frame, '
                                                                                                'frame.scratch.base, '
                                                                                                '5249, '
                                                                                                "'target_y')\n"
                                                                                                '    for '
                                                                                                'value in '
                                                                                                '(7296, 0, '
                                                                                                '0):\n'
                                                                                                '        '
                                                                                                'frame = '
                                                                                                '_city_ui_store_fields(state, '
                                                                                                'frame, '
                                                                                                'frame.scratch.base, '
                                                                                                'value)\n'
                                                                                                '    frame = '
                                                                                                '_city_ui_store_fields(state, '
                                                                                                'frame, '
                                                                                                '12582916, '
                                                                                                '1342177282, '
                                                                                                '4)\n'
                                                                                                '    frame = '
                                                                                                '_command_panel_pointer_fields(state, '
                                                                                                'frame, '
                                                                                                "'roster', "
                                                                                                '564700)\n'
                                                                                                '    frame = '
                                                                                                '_movement_move(state, '
                                                                                                'frame, '
                                                                                                "'target_x', "
                                                                                                '95, 16)\n'
                                                                                                '    return '
                                                                                                '_command_panel_upload_fields(state, '
                                                                                                'frame, '
                                                                                                "'roster', "
                                                                                                "'target_x', "
                                                                                                '12582912)',
                                                   'draw_title_mode_prompt_frame_fields': 'def '
                                                                                          'draw_title_mode_prompt_frame_fields(state: '
                                                                                          'SceneState, '
                                                                                          'frame: '
                                                                                          'FirstDeploymentFrame) '
                                                                                          '-> '
                                                                                          'FirstDeploymentFrame:\n'
                                                                                          '    """A82E: '
                                                                                          'title headings, '
                                                                                          'four body rows '
                                                                                          'and the retained '
                                                                                          'stream '
                                                                                          'footer."""\n'
                                                                                          '    frame = '
                                                                                          '_city_ui_frame_fields(state, '
                                                                                          'frame, 43054)\n'
                                                                                          '    frame = '
                                                                                          '_city_ui_store_fields(state, '
                                                                                          'frame, 12582916, '
                                                                                          '1073741825, 4)\n'
                                                                                          '    frame = '
                                                                                          '_movement_move(state, '
                                                                                          'frame, '
                                                                                          "'target_x', 1, "
                                                                                          '8)\n'
                                                                                          '    frame = '
                                                                                          '_movement_move(state, '
                                                                                          'frame, '
                                                                                          "'target_y', 0, "
                                                                                          '8)\n'
                                                                                          '    for source, '
                                                                                          'count, token, '
                                                                                          'limit, command in '
                                                                                          '((565692, 11, '
                                                                                          '43090, 383, '
                                                                                          'None), (565780, '
                                                                                          '0, 43128, 31, '
                                                                                          'None), (565760, '
                                                                                          '9, 43166, 319, '
                                                                                          '1094713346)):\n'
                                                                                          '        frame = '
                                                                                          '_command_panel_pointer_fields(state, '
                                                                                          "frame, 'roster', "
                                                                                          'source)\n'
                                                                                          '        frame = '
                                                                                          '_movement_move(state, '
                                                                                          "frame, 'count', "
                                                                                          'count, 16)\n'
                                                                                          '        frame = '
                                                                                          '_command_panel_pointer_fields(state, '
                                                                                          'frame, '
                                                                                          "'candidates', "
                                                                                          '4294955776)\n'
                                                                                          '        frame = '
                                                                                          '_campaign_ui_call_fields(state, '
                                                                                          'frame, 44682, '
                                                                                          'token)\n'
                                                                                          '        if '
                                                                                          'command is not '
                                                                                          'None:\n'
                                                                                          '            frame '
                                                                                          '= '
                                                                                          '_city_ui_store_fields(state, '
                                                                                          'frame, 12582916, '
                                                                                          'command, 4)\n'
                                                                                          '        frame = '
                                                                                          '_movement_move(state, '
                                                                                          'frame, '
                                                                                          "'offset_x', "
                                                                                          'limit, 16)\n'
                                                                                          '        frame = '
                                                                                          '_command_panel_pointer_fields(state, '
                                                                                          'frame, '
                                                                                          "'candidates', "
                                                                                          '4294955776)\n'
                                                                                          '        frame = '
                                                                                          '_command_panel_upload_fields(state, '
                                                                                          'frame, '
                                                                                          "'candidates', "
                                                                                          "'offset_x', "
                                                                                          '12582912)\n'
                                                                                          '    frame = '
                                                                                          '_command_panel_pointer_fields(state, '
                                                                                          "frame, 'roster', "
                                                                                          '565782)\n'
                                                                                          '    frame = '
                                                                                          '_city_ui_store_fields(state, '
                                                                                          'frame, 12582916, '
                                                                                          '1476395009, 4)\n'
                                                                                          '    frame = '
                                                                                          '_movement_move(state, '
                                                                                          'frame, '
                                                                                          "'distance', 3, "
                                                                                          '16)\n'
                                                                                          '    while True:\n'
                                                                                          '        frame = '
                                                                                          '_movement_move(state, '
                                                                                          "frame, 'count', "
                                                                                          '19, 16)\n'
                                                                                          '        frame = '
                                                                                          '_command_panel_pointer_fields(state, '
                                                                                          'frame, '
                                                                                          "'candidates', "
                                                                                          '4294955776)\n'
                                                                                          '        frame = '
                                                                                          '_campaign_ui_call_fields(state, '
                                                                                          'frame, 44682, '
                                                                                          '43228)\n'
                                                                                          '        frame = '
                                                                                          '_movement_move(state, '
                                                                                          'frame, '
                                                                                          "'offset_x', 639, "
                                                                                          '16)\n'
                                                                                          '        frame = '
                                                                                          '_command_panel_pointer_fields(state, '
                                                                                          'frame, '
                                                                                          "'candidates', "
                                                                                          '4294955776)\n'
                                                                                          '        frame = '
                                                                                          '_command_panel_upload_fields(state, '
                                                                                          'frame, '
                                                                                          "'candidates', "
                                                                                          "'offset_x', "
                                                                                          '12582912)\n'
                                                                                          '        frame, '
                                                                                          'again = '
                                                                                          '_command_panel_dbra_fields(frame, '
                                                                                          "'distance')\n"
                                                                                          '        if not '
                                                                                          'again:\n'
                                                                                          '            '
                                                                                          'break\n'
                                                                                          '    frame = '
                                                                                          '_command_panel_pointer_fields(state, '
                                                                                          "frame, 'roster', "
                                                                                          '566310)\n'
                                                                                          '    frame = '
                                                                                          '_command_panel_pointer_fields(state, '
                                                                                          'frame, '
                                                                                          "'candidates', "
                                                                                          '4294955776)\n'
                                                                                          '    frame = '
                                                                                          '_movement_move(state, '
                                                                                          "frame, 'count', "
                                                                                          '9, 16)\n'
                                                                                          '    frame = '
                                                                                          '_campaign_ui_call_fields(state, '
                                                                                          'frame, 44830, '
                                                                                          '43270)\n'
                                                                                          '    frame = '
                                                                                          '_city_ui_store_fields(state, '
                                                                                          'frame, 12582916, '
                                                                                          '1073741826, 4)\n'
                                                                                          '    frame = '
                                                                                          '_command_panel_pointer_fields(state, '
                                                                                          'frame, '
                                                                                          "'candidates', "
                                                                                          '4294955776)\n'
                                                                                          '    frame = '
                                                                                          '_movement_move(state, '
                                                                                          "frame, 'unit', "
                                                                                          '79, 16)\n'
                                                                                          '    return '
                                                                                          '_command_panel_upload_fields(state, '
                                                                                          'frame, '
                                                                                          "'candidates', "
                                                                                          "'unit', 12582912)",
                                                   'compose_title_option_panel_frame_fields': 'def '
                                                                                              'compose_title_option_panel_frame_fields(state: '
                                                                                              'SceneState, '
                                                                                              'frame: '
                                                                                              'FirstDeploymentFrame) '
                                                                                              '-> '
                                                                                              'FirstDeploymentFrame:\n'
                                                                                              '    """A924: '
                                                                                              'render two '
                                                                                              'real '
                                                                                              'title-option '
                                                                                              'rows, or '
                                                                                              'their '
                                                                                              'original '
                                                                                              'out-of-range '
                                                                                              'blank '
                                                                                              'panel."""\n'
                                                                                              '    frame = '
                                                                                              '_city_ui_frame_fields(state, '
                                                                                              'frame, '
                                                                                              '43300)\n'
                                                                                              '    frame = '
                                                                                              'first_replace(frame, '
                                                                                              'roster=state.table_at(4294955264).cursor())\n'
                                                                                              '    frame = '
                                                                                              '_movement_move(state, '
                                                                                              'frame, '
                                                                                              "'target_x', "
                                                                                              'state.read(4294963994, '
                                                                                              '2), 16)\n'
                                                                                              '    frame = '
                                                                                              'first_replace(frame, '
                                                                                              'roster=frame.roster.advance(s16(low16(frame.target_x))))\n'
                                                                                              '    frame = '
                                                                                              '_movement_move(state, '
                                                                                              'frame, '
                                                                                              "'target_x', "
                                                                                              'state.read(4294964058, '
                                                                                              '2), 16)\n'
                                                                                              '    frame = '
                                                                                              '_movement_move(state, '
                                                                                              'frame, '
                                                                                              "'target_y', "
                                                                                              'low16(frame.target_x), '
                                                                                              '16)\n'
                                                                                              '    frame = '
                                                                                              '_city_ui_shift_fields(state, '
                                                                                              'frame, '
                                                                                              "'target_y', "
                                                                                              '1)\n'
                                                                                              '    frame = '
                                                                                              '_city_ui_arithmetic_fields(state, '
                                                                                              'frame, '
                                                                                              "'target_y', "
                                                                                              'low16(frame.target_x))\n'
                                                                                              '    frame = '
                                                                                              '_city_ui_shift_fields(state, '
                                                                                              'frame, '
                                                                                              "'target_y', "
                                                                                              '7)\n'
                                                                                              '    frame = '
                                                                                              '_city_ui_arithmetic_fields(state, '
                                                                                              'frame, '
                                                                                              "'target_y', "
                                                                                              '49798)\n'
                                                                                              '    frame = '
                                                                                              '_movement_move(state, '
                                                                                              'frame, '
                                                                                              "'target_x', "
                                                                                              'state.read(4294964056, '
                                                                                              '2), 16)\n'
                                                                                              '    frame = '
                                                                                              '_city_ui_arithmetic_fields(state, '
                                                                                              'frame, '
                                                                                              "'target_x', "
                                                                                              'state.read(4294964058, '
                                                                                              '2))\n'
                                                                                              '    frame = '
                                                                                              '_movement_compare(state, '
                                                                                              'frame, '
                                                                                              'low16(frame.target_x), '
                                                                                              '34, 16)\n'
                                                                                              '    if not '
                                                                                              'frame.status '
                                                                                              '& 1 and (not '
                                                                                              'frame.status '
                                                                                              '& 4):\n'
                                                                                              '        frame '
                                                                                              '= '
                                                                                              '_city_ui_store_fields(state, '
                                                                                              'frame, '
                                                                                              'u32(frame.roster.base '
                                                                                              '+ 22), 16)\n'
                                                                                              '        frame '
                                                                                              '= '
                                                                                              '_city_ui_store_fields(state, '
                                                                                              'frame, '
                                                                                              'u32(frame.roster.base '
                                                                                              '+ 80), 16)\n'
                                                                                              '        frame '
                                                                                              '= '
                                                                                              '_city_ui_store_fields(state, '
                                                                                              'frame, '
                                                                                              'u32(frame.roster.base '
                                                                                              '+ 58), 9)\n'
                                                                                              '        frame '
                                                                                              '= '
                                                                                              '_city_ui_append_fields(state, '
                                                                                              'frame, 9)\n'
                                                                                              '        for '
                                                                                              'offset, '
                                                                                              'increment in '
                                                                                              '((22, 128), '
                                                                                              '(58, 34), '
                                                                                              '(80, 162)):\n'
                                                                                              '            '
                                                                                              'frame = '
                                                                                              '_city_ui_store_fields(state, '
                                                                                              'frame, '
                                                                                              'u32(frame.roster.base '
                                                                                              '+ offset), '
                                                                                              'low16(frame.target_y))\n'
                                                                                              '            '
                                                                                              'frame = '
                                                                                              '_city_ui_memory_arithmetic_fields(state, '
                                                                                              'frame, '
                                                                                              'u32(frame.roster.base '
                                                                                              '+ offset), '
                                                                                              'increment)\n'
                                                                                              '        frame '
                                                                                              '= '
                                                                                              '_city_ui_append_fields(state, '
                                                                                              'frame, '
                                                                                              'low16(frame.target_y))\n'
                                                                                              '        frame '
                                                                                              '= '
                                                                                              '_movement_move(state, '
                                                                                              'frame, '
                                                                                              "'unit', 15, "
                                                                                              '16)\n'
                                                                                              '        while '
                                                                                              'True:\n'
                                                                                              '            '
                                                                                              'frame = '
                                                                                              '_city_ui_store_fields(state, '
                                                                                              'frame, '
                                                                                              'u32(frame.roster.base '
                                                                                              '+ 22), 1155)\n'
                                                                                              '            '
                                                                                              'frame = '
                                                                                              '_city_ui_store_fields(state, '
                                                                                              'frame, '
                                                                                              'u32(frame.roster.base '
                                                                                              '+ 80), 1155)\n'
                                                                                              '            '
                                                                                              'frame = '
                                                                                              '_movement_compare(state, '
                                                                                              'frame, '
                                                                                              'low16(frame.unit), '
                                                                                              '6, 16)\n'
                                                                                              '            '
                                                                                              'if not '
                                                                                              'frame.status '
                                                                                              '& 1 and (not '
                                                                                              'frame.status '
                                                                                              '& 4):\n'
                                                                                              '                '
                                                                                              'frame = '
                                                                                              '_city_ui_store_fields(state, '
                                                                                              'frame, '
                                                                                              'frame.roster.base, '
                                                                                              '1155)\n'
                                                                                              '                '
                                                                                              'frame = '
                                                                                              '_city_ui_store_fields(state, '
                                                                                              'frame, '
                                                                                              'u32(frame.roster.base '
                                                                                              '+ 58), 1155)\n'
                                                                                              '            '
                                                                                              'frame = '
                                                                                              'first_replace(frame, '
                                                                                              'roster=frame.roster.advance(2), '
                                                                                              'unit=replace_word(frame.unit, '
                                                                                              'u16(low16(frame.unit) '
                                                                                              '- 1)))\n'
                                                                                              '            '
                                                                                              'if '
                                                                                              'low16(frame.unit) '
                                                                                              '== 65535:\n'
                                                                                              '                '
                                                                                              'break\n'
                                                                                              '        frame '
                                                                                              '= '
                                                                                              '_city_ui_store_fields(state, '
                                                                                              'frame, '
                                                                                              'u32(frame.roster.base '
                                                                                              '+ 80), 0, 2, '
                                                                                              'True)\n'
                                                                                              '    else:\n'
                                                                                              '        frame '
                                                                                              '= '
                                                                                              '_campaign_ui_call_fields(state, '
                                                                                              'frame, 43482, '
                                                                                              '43346)\n'
                                                                                              '        frame '
                                                                                              '= '
                                                                                              '_city_ui_arithmetic_fields(state, '
                                                                                              'frame, '
                                                                                              "'target_y', "
                                                                                              '34)\n'
                                                                                              '        frame '
                                                                                              '= '
                                                                                              '_movement_move(state, '
                                                                                              'frame, '
                                                                                              "'unit', 7, "
                                                                                              '16)\n'
                                                                                              '        frame '
                                                                                              '= '
                                                                                              '_movement_compare(state, '
                                                                                              'frame, '
                                                                                              'low16(frame.target_x), '
                                                                                              '29, 16)\n'
                                                                                              '        if '
                                                                                              'not '
                                                                                              'frame.status '
                                                                                              '& 1:\n'
                                                                                              '            '
                                                                                              'frame = '
                                                                                              '_movement_move(state, '
                                                                                              'frame, '
                                                                                              "'unit', 6, "
                                                                                              '16)\n'
                                                                                              '        frame '
                                                                                              '= '
                                                                                              '_city_ui_arithmetic_fields(state, '
                                                                                              'frame, '
                                                                                              "'target_x', "
                                                                                              'low16(frame.unit))\n'
                                                                                              '        frame '
                                                                                              '= '
                                                                                              '_campaign_ui_call_fields(state, '
                                                                                              'frame, 43482, '
                                                                                              '43370)\n'
                                                                                              '    frame = '
                                                                                              '_city_ui_store_fields(state, '
                                                                                              'frame, '
                                                                                              'frame.roster.base, '
                                                                                              '0, 2, True)\n'
                                                                                              '    frame = '
                                                                                              '_city_ui_memory_arithmetic_fields(state, '
                                                                                              'frame, '
                                                                                              '4294963994, '
                                                                                              '72)\n'
                                                                                              '    return '
                                                                                              '_city_ui_memory_arithmetic_fields(state, '
                                                                                              'frame, '
                                                                                              '4294964058, '
                                                                                              '1)',
                                                   'append_scenario_owner_value_frame_fields': 'def '
                                                                                               'append_scenario_owner_value_frame_fields(state: '
                                                                                               'SceneState, '
                                                                                               'frame: '
                                                                                               'FirstDeploymentFrame) '
                                                                                               '-> '
                                                                                               'FirstDeploymentFrame:\n'
                                                                                               '    """A72A: '
                                                                                               'clear forty '
                                                                                               'owner totals '
                                                                                               'and count '
                                                                                               'the original '
                                                                                               '256 roster '
                                                                                               'BYTEs."""\n'
                                                                                               '    frame = '
                                                                                               '_city_ui_frame_fields(state, '
                                                                                               'frame, '
                                                                                               '42794)\n'
                                                                                               '    frame = '
                                                                                               '_command_panel_pointer_fields(state, '
                                                                                               'frame, '
                                                                                               "'roster', "
                                                                                               '4294960224)\n'
                                                                                               '    frame = '
                                                                                               '_movement_move(state, '
                                                                                               'frame, '
                                                                                               "'target_x', "
                                                                                               '39, 16)\n'
                                                                                               '    frame = '
                                                                                               '_command_panel_fill_buffer_fields(state, '
                                                                                               'frame, '
                                                                                               "'roster', "
                                                                                               "'target_x', "
                                                                                               '0, True)\n'
                                                                                               '    frame = '
                                                                                               '_command_panel_pointer_fields(state, '
                                                                                               'frame, '
                                                                                               "'roster', "
                                                                                               '4294960220)\n'
                                                                                               '    frame = '
                                                                                               '_command_panel_pointer_fields(state, '
                                                                                               'frame, '
                                                                                               "'candidates', "
                                                                                               '4294953984)\n'
                                                                                               '    frame = '
                                                                                               '_movement_move(state, '
                                                                                               'frame, '
                                                                                               "'target_x', "
                                                                                               '255, 16)\n'
                                                                                               '    while '
                                                                                               'True:\n'
                                                                                               '        '
                                                                                               'frame = '
                                                                                               '_movement_move(state, '
                                                                                               'frame, '
                                                                                               "'target_y', "
                                                                                               '0, 16)\n'
                                                                                               '        '
                                                                                               'frame = '
                                                                                               '_movement_move(state, '
                                                                                               'frame, '
                                                                                               "'target_y', "
                                                                                               'frame.candidates.byte(), '
                                                                                               '8)\n'
                                                                                               '        '
                                                                                               'frame = '
                                                                                               'first_replace(frame, '
                                                                                               'candidates=frame.candidates.advance(1))\n'
                                                                                               '        if '
                                                                                               'not '
                                                                                               'frame.status '
                                                                                               '& 4:\n'
                                                                                               '            '
                                                                                               'frame = '
                                                                                               '_movement_compare(state, '
                                                                                               'frame, '
                                                                                               'low8(frame.target_y), '
                                                                                               '40, 8)\n'
                                                                                               '            '
                                                                                               'if '
                                                                                               'frame.status '
                                                                                               '& 5:\n'
                                                                                               '                '
                                                                                               'frame = '
                                                                                               '_city_ui_shift_fields(state, '
                                                                                               'frame, '
                                                                                               "'target_y', "
                                                                                               '2)\n'
                                                                                               '                '
                                                                                               'frame = '
                                                                                               '_city_ui_memory_arithmetic_fields(state, '
                                                                                               'frame, '
                                                                                               'u32(frame.roster.base '
                                                                                               '+ '
                                                                                               's16(low16(frame.target_y)) '
                                                                                               '+ 2), 1)\n'
                                                                                               '        '
                                                                                               'frame, again '
                                                                                               '= '
                                                                                               '_command_panel_dbra_fields(frame, '
                                                                                               "'target_x')\n"
                                                                                               '        if '
                                                                                               'not again:\n'
                                                                                               '            '
                                                                                               'return '
                                                                                               'frame'},
 'tools.high_level_main_flows.business_map': {'render_initial_map_rows_frame_fields': 'def '
                                                                                      'render_initial_map_rows_frame_fields(state: '
                                                                                      'SceneState, frame: '
                                                                                      'FirstDeploymentFrame) '
                                                                                      '-> '
                                                                                      'FirstDeploymentFrame:\n'
                                                                                      '    """A278: original '
                                                                                      'streams, then29 rows '
                                                                                      'with real8B '
                                                                                      'MOVEM+4CALL '
                                                                                      'slots."""\n'
                                                                                      '    from '
                                                                                      '.business_movement_support '
                                                                                      'import '
                                                                                      '_movement_save_longs, '
                                                                                      '_movement_restore_longs\n'
                                                                                      '    frame = '
                                                                                      'display_frame_fields(state, '
                                                                                      'frame)\n'
                                                                                      '    frame = '
                                                                                      'display_store_fields(state, '
                                                                                      'frame, 41592, '
                                                                                      '12582916, 1073741826, '
                                                                                      '4)\n'
                                                                                      '    frame = '
                                                                                      'display_address_fields(state, '
                                                                                      "frame, 'roster', "
                                                                                      '850658)\n'
                                                                                      '    frame = '
                                                                                      'display_address_fields(state, '
                                                                                      "frame, 'candidates', "
                                                                                      '850450)\n'
                                                                                      '    frame = '
                                                                                      'display_move_fields(state, '
                                                                                      "frame, 'target_x', "
                                                                                      'state.read(865476, '
                                                                                      '2))\n'
                                                                                      '    frame = '
                                                                                      'display_call_fields(state, '
                                                                                      'frame, 44540, 41626)\n'
                                                                                      '    frame = '
                                                                                      'display_store_fields(state, '
                                                                                      'frame, 41626, '
                                                                                      '12582916, 1073741825, '
                                                                                      '4)\n'
                                                                                      '    frame = '
                                                                                      'display_address_fields(state, '
                                                                                      "frame, 'roster', "
                                                                                      '856990)\n'
                                                                                      '    frame = '
                                                                                      'display_address_fields(state, '
                                                                                      "frame, 'candidates', "
                                                                                      '856822)\n'
                                                                                      '    frame = '
                                                                                      'display_move_fields(state, '
                                                                                      "frame, 'target_x', "
                                                                                      'state.read(865480, '
                                                                                      '2))\n'
                                                                                      '    frame = '
                                                                                      'display_call_fields(state, '
                                                                                      'frame, 44540, 41660)\n'
                                                                                      '    frame = '
                                                                                      'display_store_fields(state, '
                                                                                      'frame, 41660, '
                                                                                      '12582916, 1610612738, '
                                                                                      '4)\n'
                                                                                      '    frame = '
                                                                                      'display_address_fields(state, '
                                                                                      "frame, 'roster', "
                                                                                      '856662)\n'
                                                                                      '    frame = '
                                                                                      'display_move_fields(state, '
                                                                                      "frame, 'target_x', "
                                                                                      'state.read(865478, '
                                                                                      '2))\n'
                                                                                      '    while True:\n'
                                                                                      '        pixels = '
                                                                                      'frame.roster.long()\n'
                                                                                      '        frame = '
                                                                                      'first_replace(frame, '
                                                                                      'roster=frame.roster.advance(4))\n'
                                                                                      '        frame = '
                                                                                      'display_store_fields(state, '
                                                                                      'frame, 41682, '
                                                                                      '12582912, pixels, 4)\n'
                                                                                      '        frame, more = '
                                                                                      'display_loop_fields(frame, '
                                                                                      "'target_x')\n"
                                                                                      '        if not more:\n'
                                                                                      '            break\n'
                                                                                      '    frame = '
                                                                                      'display_move_fields(state, '
                                                                                      "frame, 'target_x', "
                                                                                      '28)\n'
                                                                                      '    frame = '
                                                                                      'display_address_fields(state, '
                                                                                      "frame, 'opponent', "
                                                                                      'u32(s16(state.read(4294963988, '
                                                                                      '2))))\n'
                                                                                      '    while True:\n'
                                                                                      '        frame = '
                                                                                      '_movement_save_longs(state, '
                                                                                      "frame, ('target_x', "
                                                                                      "'opponent'))\n"
                                                                                      '        frame = '
                                                                                      'display_move_fields(state, '
                                                                                      "frame, 'target_x', "
                                                                                      'low16(frame.opponent.base))\n'
                                                                                      '        frame = '
                                                                                      'display_move_fields(state, '
                                                                                      "frame, 'target_y', "
                                                                                      'state.read(4294963992, '
                                                                                      '2))\n'
                                                                                      '        frame = '
                                                                                      'display_address_fields(state, '
                                                                                      "frame, 'roster', "
                                                                                      '529754)\n'
                                                                                      '        frame = '
                                                                                      'display_store_fields(state, '
                                                                                      'frame, 41716, '
                                                                                      '4294964008, 0, '
                                                                                      'clear=True)\n'
                                                                                      '        frame = '
                                                                                      'display_call_fields(state, '
                                                                                      'frame, 44906, 41726)\n'
                                                                                      '        frame = '
                                                                                      'display_call_fields(state, '
                                                                                      'frame, 45140, 41732)\n'
                                                                                      '        frame = '
                                                                                      'display_move_fields(state, '
                                                                                      "frame, 'target_x', "
                                                                                      'low16(frame.target_x) '
                                                                                      '| 57344)\n'
                                                                                      '        frame = '
                                                                                      'display_address_fields(state, '
                                                                                      "frame, 'roster', "
                                                                                      '4294955008)\n'
                                                                                      '        frame = '
                                                                                      'display_move_fields(state, '
                                                                                      "frame, 'target_y', "
                                                                                      '41)\n'
                                                                                      '        frame = '
                                                                                      'display_store_fields(state, '
                                                                                      'frame, 41744, '
                                                                                      'frame.roster.base, '
                                                                                      'low16(frame.target_y))\n'
                                                                                      '        frame = '
                                                                                      'first_replace(frame, '
                                                                                      'roster=frame.roster.advance(2))\n'
                                                                                      '        frame = '
                                                                                      'display_store_fields(state, '
                                                                                      'frame, 41746, '
                                                                                      'frame.roster.base, '
                                                                                      'low16(frame.target_x))\n'
                                                                                      '        frame = '
                                                                                      'first_replace(frame, '
                                                                                      'roster=frame.roster.advance(2))\n'
                                                                                      '        frame = '
                                                                                      'display_call_fields(state, '
                                                                                      'frame, 45166, 41754)\n'
                                                                                      '        frame = '
                                                                                      'display_store_fields(state, '
                                                                                      'frame, 41754, '
                                                                                      'frame.roster.base, 0, '
                                                                                      'clear=True)\n'
                                                                                      '        frame = '
                                                                                      'display_address_fields(state, '
                                                                                      "frame, 'roster', "
                                                                                      '4294955008)\n'
                                                                                      '        frame = '
                                                                                      'display_call_fields(state, '
                                                                                      'frame, 44316, 41766)\n'
                                                                                      '        frame = '
                                                                                      '_movement_restore_longs(state, '
                                                                                      "frame, ('target_x', "
                                                                                      "'opponent'))\n"
                                                                                      '        frame = '
                                                                                      'first_replace(frame, '
                                                                                      'opponent=frame.opponent.advance(8))\n'
                                                                                      '        frame, more = '
                                                                                      'display_loop_fields(frame, '
                                                                                      "'target_x')\n"
                                                                                      '        if not more:\n'
                                                                                      '            return '
                                                                                      'frame'},
 'tools.high_level_gameplay_flow.business_services': {'copy_video_transfer_descriptor_fields': 'def '
                                                                                               'copy_video_transfer_descriptor_fields(memory: '
                                                                                               'SceneRefreshMemory, '
                                                                                               'frame: '
                                                                                               'FirstDeploymentFrame, '
                                                                                               'observed_index: '
                                                                                               'Word | '
                                                                                               'None=None) '
                                                                                               '-> '
                                                                                               'FirstDeploymentFrame:\n'
                                                                                               '    """8112: '
                                                                                               'sole '
                                                                                               'descriptor '
                                                                                               'selection, '
                                                                                               'inclusive '
                                                                                               'LONG copy '
                                                                                               'and live '
                                                                                               'marker RMW.\n'
                                                                                               '\n'
                                                                                               '    The '
                                                                                               'historical '
                                                                                               'WORD index '
                                                                                               'is a real '
                                                                                               'observation, '
                                                                                               'not a '
                                                                                               'made-up D0 '
                                                                                               'high\n'
                                                                                               '    half. '
                                                                                               'Complete '
                                                                                               'Scene '
                                                                                               'callers '
                                                                                               'already '
                                                                                               'carry it in '
                                                                                               'the actual '
                                                                                               'D0 field.\n'
                                                                                               '    """\n'
                                                                                               '    from '
                                                                                               '..high_level_main_flows.business_movement_support '
                                                                                               'import '
                                                                                               '_movement_binary_flags\n'
                                                                                               '    '
                                                                                               'memory.frame(frame)\n'
                                                                                               '    if '
                                                                                               'observed_index '
                                                                                               'is None:\n'
                                                                                               '        if '
                                                                                               'frame.target_x '
                                                                                               'is None:\n'
                                                                                               '            '
                                                                                               'raise '
                                                                                               'SceneRefreshBoundary(33042, '
                                                                                               'frame, '
                                                                                               'None)\n'
                                                                                               '        '
                                                                                               'index = '
                                                                                               'low16(frame.target_x)\n'
                                                                                               '    else:\n'
                                                                                               '        '
                                                                                               'index = '
                                                                                               'uint(observed_index, '
                                                                                               '16)\n'
                                                                                               '        if '
                                                                                               'frame.target_x '
                                                                                               'is not None '
                                                                                               'and '
                                                                                               'low16(frame.target_x) '
                                                                                               '!= index:\n'
                                                                                               '            '
                                                                                               'raise '
                                                                                               "ValueError('actual "
                                                                                               'descriptor '
                                                                                               'WORD index '
                                                                                               'differs from '
                                                                                               'retained '
                                                                                               "D0')\n"
                                                                                               '    frame = '
                                                                                               'first_replace(frame, '
                                                                                               'candidates=memory.cursor_at(33068))\n'
                                                                                               '    frame = '
                                                                                               'memory.sync_status(_first_shift_word(frame, '
                                                                                               "'target_x', "
                                                                                               'index, 3))\n'
                                                                                               '    frame = '
                                                                                               'first_replace(frame, '
                                                                                               'candidates=frame.candidates.advance(s16(u16(index '
                                                                                               '<< 3))))\n'
                                                                                               '    '
                                                                                               'descriptor = '
                                                                                               'frame.candidates\n'
                                                                                               '    address '
                                                                                               '= '
                                                                                               'descriptor.long()\n'
                                                                                               '    frame = '
                                                                                               'first_replace(frame, '
                                                                                               'candidates=descriptor.advance(4), '
                                                                                               'controller=memory.cursor_at(address))\n'
                                                                                               '    '
                                                                                               'descriptor = '
                                                                                               'frame.candidates\n'
                                                                                               '    address '
                                                                                               '= '
                                                                                               'u32(s16(descriptor.word()))\n'
                                                                                               '    frame = '
                                                                                               'first_replace(frame, '
                                                                                               'candidates=descriptor.advance(2), '
                                                                                               'scan=memory.cursor_at(address))\n'
                                                                                               '    '
                                                                                               'descriptor = '
                                                                                               'frame.candidates\n'
                                                                                               '    '
                                                                                               'remaining = '
                                                                                               'descriptor.word()\n'
                                                                                               '    frame = '
                                                                                               'first_replace(frame, '
                                                                                               'candidates=descriptor.advance(2))\n'
                                                                                               '    frame = '
                                                                                               'memory.sync_status(_first_word(frame, '
                                                                                               "'choice', "
                                                                                               'remaining))\n'
                                                                                               '    while '
                                                                                               'True:\n'
                                                                                               '        '
                                                                                               'source, '
                                                                                               'destination '
                                                                                               '= '
                                                                                               '(frame.controller, '
                                                                                               'frame.scan)\n'
                                                                                               '        '
                                                                                               'value = '
                                                                                               'source.long()\n'
                                                                                               '        '
                                                                                               'frame = '
                                                                                               'first_replace(frame, '
                                                                                               'controller=source.advance(4))\n'
                                                                                               '        '
                                                                                               'frame = '
                                                                                               '_scene_refresh_emit(memory, '
                                                                                               'frame, '
                                                                                               'destination.base, '
                                                                                               '4, value)\n'
                                                                                               '        '
                                                                                               'frame = '
                                                                                               'first_replace(frame, '
                                                                                               'scan=destination.advance(4))\n'
                                                                                               '        '
                                                                                               'frame = '
                                                                                               '_scene_refresh_decrement(frame, '
                                                                                               "'choice', "
                                                                                               'remaining)\n'
                                                                                               '        '
                                                                                               'remaining = '
                                                                                               'u16(remaining '
                                                                                               '- 1)\n'
                                                                                               '        if '
                                                                                               'remaining == '
                                                                                               '65535:\n'
                                                                                               '            '
                                                                                               'break\n'
                                                                                               '    '
                                                                                               'memory.sync_status(frame)\n'
                                                                                               '    previous '
                                                                                               '= '
                                                                                               'memory.state.read(4294963998, '
                                                                                               '2)\n'
                                                                                               '    frame, '
                                                                                               'value = '
                                                                                               '_movement_binary_flags(memory.state, '
                                                                                               'frame, '
                                                                                               'previous, 1, '
                                                                                               '16)\n'
                                                                                               '    '
                                                                                               'memory.state.write(4294963998, '
                                                                                               '2, value)\n'
                                                                                               '    return '
                                                                                               'memory.sync_status(frame)'}}
# These exact complete mature functions already have a public source contract.
# Reuse its source literals instead of copying them into another large constant.
SHARED_SOURCES={'tools.high_level_gameplay_flow.early_panel_steps':{
    'REUSED_SOURCE':{
        'tools.high_level_main_flows.business_lowbank':('upload_selection_layout_fields',),
        'tools.high_level_scene_flows.business_scene':('write_vdp_dictionary_repeat_stream_fields',),
    }}}


def _dump(node):
    return ast.dump(node,include_attributes=False)


def _code_shape(code):
    return tuple(getattr(code,name)for name in ('co_code','co_names','co_varnames',
        'co_argcount','co_posonlyargcount','co_kwonlyargcount','co_flags',
        'co_freevars','co_cellvars'))+(tuple(_code_shape(value)if type(value)is CodeType
            else value for value in code.co_consts),)


def _code_at(code,name):
    values=[value for value in code.co_consts if type(value)is CodeType and value.co_name==name]
    if len(values)!=1:raise ValueError('one complete lexical startup-panel owner required: '+name)
    return values[0]


def _context(module):
    tree=ast.parse(inspect.getsource(module),filename=module.__file__)
    return tree,compile(tree,module.__file__,'exec',dont_inherit=True)


def _actual_function(module,name,code):
    function=getattr(module,name)
    if (type(function)is not FunctionType or function.__globals__ is not vars(module)
            or function.__module__!=module.__name__ or function.__qualname__!=name
            or function.__closure__ is not None or function.__code__.co_freevars
            or _code_shape(function.__code__)!=_code_shape(_code_at(code,name))):
        raise ValueError('actual complete-module startup-panel function required: '+name)
    return function


def _startup_tree(group,original):
    """Finite named calls only; exact inverse every complete FN and module."""
    result=copy.deepcopy(original);inverses={}
    for index,node in enumerate(original.body):
        if not isinstance(node,ast.FunctionDef)or node.name not in VIEW_SPECS[group]:continue
        if _dump(node)!=_dump(ast.parse(EXPECTED_SOURCE[group][node.name]).body[0]):
            raise ValueError('whole reviewed startup-panel source changed: '+node.name)
        if any(isinstance(value,(ast.Yield,ast.YieldFrom))for value in ast.walk(node)):
            raise ValueError('original complete startup parent must remain synchronous')
        wanted=VIEW_SPECS[group][node.name];counts={name:0 for name in wanted};changes=[]

        class Lift(ast.NodeTransformer):
            def visit_Call(self,item):
                item=self.generic_visit(item)
                if isinstance(item.func,ast.Name)and item.func.id in wanted:
                    name=item.func.id;counts[name]+=1;before=copy.deepcopy(item)
                    item.func.id=wanted[name][1]
                    after=ast.copy_location(ast.YieldFrom(value=item),item)
                    changes.append((before,copy.deepcopy(after)));return after
                return item

        derived=Lift().visit(copy.deepcopy(node))
        if counts!={name:rule[0]for name,rule in wanted.items()}:
            raise ValueError('exact complete startup CALL/tail syntax count required: '+node.name)
        remaining=list(changes)

        class Inverse(ast.NodeTransformer):
            def visit_YieldFrom(self,item):
                for position,(before,after)in enumerate(remaining):
                    if _dump(item)==_dump(after):remaining.pop(position);return copy.deepcopy(before)
                raise ValueError('unadmitted startup-panel cooperative expression')

        inverse=Inverse().visit(copy.deepcopy(derived))
        if remaining or _dump(inverse)!=_dump(node):raise ValueError('whole startup-panel FN inverse differs')
        result.body[index]=derived;inverses[index]=inverse
    if len(inverses)!=len(VIEW_SPECS[group]):raise ValueError('every complete finite startup view required')
    restored=copy.deepcopy(result)
    for index,node in inverses.items():restored.body[index]=node
    if _dump(restored)!=_dump(original):raise ValueError('whole original startup business module inverse differs')
    return ast.fix_missing_locations(result)


def _class_bindings(module,cls,name,tree,code):
    nodes=[node for node in tree.body if isinstance(node,ast.ClassDef)and node.name==name]
    if len(nodes)!=1 or getattr(module,name)is not cls:raise ValueError('actual startup provider/base class required')
    class_code=_code_at(code,name);result=[]
    for node in nodes[0].body:
        if not isinstance(node,ast.FunctionDef):continue
        descriptor=vars(cls).get(node.name)
        function=descriptor.__func__ if type(descriptor)is staticmethod else descriptor
        if (type(function)is not FunctionType or function.__globals__ is not vars(module)
                or function.__qualname__!=name+'.'+node.name
                or _code_shape(function.__code__)!=_code_shape(_code_at(class_code,node.name))):
            raise ValueError('actual complete-context startup class method required: '+node.name)
        result.append((cls,node.name,descriptor,function,function.__code__))
    return result


class StartupPanelScenePrograms(BattleScenePrograms):
    """Exact four Main3CE parents and their actual93F0/A1B2/A622 lifetimes."""
    def __init__(self,state):
        if (BattleScenePrograms is not battle.BattleScenePrograms
                or StartupPanelScenePrograms.__bases__!=(BattleScenePrograms,)):
            raise ValueError('actual unchanged BattleScenePrograms base required')
        own=inspect.getmodule(StartupPanelScenePrograms)
        if own is None or vars(own)is not globals():raise ValueError('actual startup-panel provider module required')
        self._startup_classes=(BattleScenePrograms,StartupPanelScenePrograms,own)
        self._startup_methods=[];self._startup_utilities=[]
        for module,cls,name in ((battle,BattleScenePrograms,'BattleScenePrograms'),
                (own,StartupPanelScenePrograms,'StartupPanelScenePrograms')):
            tree,code=_context(module)
            self._startup_methods+=_class_bindings(module,cls,name,tree,code)
            for node in tree.body:
                if isinstance(node,ast.FunctionDef):
                    function=_actual_function(module,node.name,code)
                    self._startup_utilities.append((module,node.name,function,function.__code__))
        super().__init__(state)
        self.startup_originals={};self.startup_views={};self.startup_namespaces={}
        self.startup_bindings={};self.startup_imports=[];self.startup_shared=[]
        self._startup_import_names=set();self.startup_namespace_functions={}
        self.startup_modules={group:importlib.import_module(path)for group,path in MODULE_PATHS.items()}
        for group,module in self.startup_modules.items():
            tree,code=_context(module)
            for name,source in EXPECTED_SOURCE[group].items():self._remember(module,name,source,tree,code)
            derived=compile(_startup_tree(group,tree),module.__file__,'exec',dont_inherit=True)
            namespace=dict(vars(module));self.startup_namespaces[group]=namespace
            for name,source in EXPECTED_SOURCE[group].items():
                for item in ast.walk(ast.parse(source)):
                    if isinstance(item,ast.Name)and isinstance(item.ctx,ast.Load):
                        value=namespace.get(item.id)
                        if type(value)is FunctionType:
                            self.startup_namespace_functions[group,item.id]=(value,value.__code__)
            for name in VIEW_SPECS[group]:
                original=getattr(module,name)
                view=FunctionType(_code_at(derived,name),namespace,name,original.__defaults__,None)
                view.__kwdefaults__=original.__kwdefaults__;view.__annotations__=dict(original.__annotations__)
                if not inspect.isgeneratorfunction(view):raise ValueError('whole startup parent generator required')
                self.startup_views[group,name]=view
        self._startup_view_owners={key:(view,view.__code__)for key,view in self.startup_views.items()}
        aliases={'_startup_campaign_call':self.views['main','_campaign_call_fields'],
            '_startup_display_call':self.views['display','display_call_fields'],
            '_startup_clear_tail':self._clear_tail}
        for group,namespace in self.startup_namespaces.items():
            for name,value in aliases.items():
                if name in namespace:raise ValueError('private startup alias must not shadow original business')
                namespace[name]=value;self.startup_bindings[group,name]=value
        for path,sources in REUSED_SOURCE.items():
            module=importlib.import_module(path);tree,code=_context(module)
            for name,source in sources.items():self._remember(module,name,source,tree,code)
        for path,fields in SHARED_SOURCES.items():
            shared=importlib.import_module(path);tree,_=_context(shared)
            for field,modules in fields.items():
                assignments=[node for node in tree.body if isinstance(node,ast.Assign)
                    and len(node.targets)==1 and isinstance(node.targets[0],ast.Name)and node.targets[0].id==field]
                actual=getattr(shared,field)
                if len(assignments)!=1 or actual!=ast.literal_eval(assignments[0].value):
                    raise ValueError('existing exact startup dependency source registry required')
                for source_path,names in modules.items():
                    module=importlib.import_module(source_path);source_tree,code=_context(module)
                    for name in names:
                        source=actual[source_path][name]
                        self._remember(module,name,source,source_tree,code)
                        self.startup_shared.append((shared,field,actual,source_path,name,source))
        self.startup_admissions=dict(confidence='confirmed_source_candidate_runtime_unverified',
            whole_views=7,CALL_propagations=18,tail_propagations=1,
            outer_return=0x3CE,clear_tail=(0x3FC,0x60C),
            existing_device_polls=(0x6886,0x68FA,0xAF4C,0xAF5C),
            new_wait_types=0,new_device_ready_clock_or_budget=False)

    def _remember(self,module,name,source,tree,code):
        nodes=[node for node in tree.body if isinstance(node,ast.FunctionDef)and node.name==name]
        if len(nodes)!=1 or _dump(nodes[0])!=_dump(ast.parse(source).body[0]):
            raise ValueError('whole original startup child/helper source differs: '+name)
        function=_actual_function(module,name,code)
        self.startup_originals[module.__name__,name]=(module,function,function.__code__)
        bindings={item.id for item in ast.walk(nodes[0])if isinstance(item,ast.Name)and isinstance(item.ctx,ast.Load)}
        for node in tree.body:
            if isinstance(node,ast.ImportFrom):
                bindings.update(alias.asname or alias.name for alias in node.names)
        for binding in bindings:
            value=getattr(module,binding,None);key=(module.__name__,binding)
            if type(value)is FunctionType and key not in self._startup_import_names:
                if value.__globals__ is vars(module):_actual_function(module,binding,code)
                self._startup_import_names.add(key)
                self.startup_imports.append((module,binding,value,value.__code__))

    def require_current(self,state):
        base,cls,module=self._startup_classes
        if (BattleScenePrograms is not base or battle.BattleScenePrograms is not base
                or StartupPanelScenePrograms is not cls or module.StartupPanelScenePrograms is not cls
                or cls.__bases__!=(base,)):
            raise ValueError('actual startup provider/base class identity changed')
        for owner,name,descriptor,function,code in self._startup_methods:
            if vars(owner).get(name)is not descriptor or function.__code__ is not code:
                raise ValueError('actual startup/base complete method changed: '+name)
        for module,name,function,code in self._startup_utilities:
            if getattr(module,name)is not function or function.__code__ is not code:
                raise ValueError('actual startup/base source utility changed: '+name)
        super().require_current(state)
        if not hasattr(self,'startup_originals'):return
        for (path,name),(module,function,code)in self.startup_originals.items():
            if getattr(module,name)is not function or function.__code__ is not code:
                raise ValueError('actual startup business owner changed: '+name)
        for module,name,function,code in self.startup_imports:
            if getattr(module,name)is not function or function.__code__ is not code:
                raise ValueError('actual startup imported callable changed: '+name)
        if self.startup_views.keys()!=self._startup_view_owners.keys():raise ValueError('finite complete startup graph changed')
        for key,(view,code)in self._startup_view_owners.items():
            if self.startup_views[key]is not view or view.__code__ is not code:
                raise ValueError('whole private startup CodeType changed: '+key[1])
        for (group,name),value in self.startup_bindings.items():
            if self.startup_namespaces[group].get(name)is not value:
                raise ValueError('private startup continuation binding changed: '+name)
        for (group,name),(function,code)in self.startup_namespace_functions.items():
            if self.startup_namespaces[group].get(name)is not function or function.__code__ is not code:
                raise ValueError('actual private startup business-global binding changed: '+name)
        for shared,field,actual,path,name,source in self.startup_shared:
            if getattr(shared,field)is not actual or actual.get(path,{}).get(name)!=source:
                raise ValueError('existing shared mature startup source contract changed: '+name)

    def _forward_device(self,program):
        first=True;returned=None
        try:
            while True:
                self.require_current(self.state)
                try:waiting=next(program)if first else program.send(returned)
                except StopIteration as finished:return finished.value
                first=False
                if type(waiting)is not GameplaySceneWait or waiting.state is not self.state or waiting.needs_interrupt:
                    raise ValueError('one actual same-Scene existing startup device wait required')
                waiting.validate();returned=yield waiting
                self.require_current(self.state)
                if returned is not waiting.frame or self.state.sr!=waiting.status_word:
                    raise ValueError('explicit startup device progress must retain real frame and full SR')
        finally:program.close()

    def _service(self,state,frame,name):
        self.require_current(state)
        if name not in ('initialize_video_registers_and_planes_fields','clear_video_sprite_plane_fields',
                'clear_scene_video_and_state_fields'):
            raise ValueError('one finite actual complete startup service required')
        return (yield from self._forward_device(self.battle_views['services',name](SceneRefreshMemory(state),frame)))

    def _clear_tail(self,state,frame,target):
        self.require_current(state)
        if target!=0x60C:raise MovementContinuationBoundary(target,frame,'only original3FC BRA060C is admitted')
        # Original3FC is a BRA: incoming3CE is reused, not pushed or popped here.
        return (yield from self._service(state,frame,'clear_scene_video_and_state_fields'))

    def _campaign_child(self,state,frame,target,continuation):
        self.require_current(state)
        parents={0x93F0:(0x4EE,'lowbank','initialize_scene_growth_and_tiles_fields'),
            0xA1B2:(0x5BC,'map','initialize_world_map_view_frame_fields'),
            0xA622:(0xE82,'commands','draw_current_scenario_prompt_frame_fields')}
        if target in parents:
            expected,group,name=parents[target]
            if continuation!=expected:raise MovementContinuationBoundary(target,frame,'actual startup parent CALL slot differs')
            return (yield from self.startup_views[group,name](state,frame))
        if target==0x68CE and continuation in (0x9408,0xA63A):
            return (yield from self._service(state,frame,'clear_video_sprite_plane_fields'))
        return (yield from super()._campaign_child(state,frame,target,continuation))

    def _display_child(self,state,frame,target,continuation):
        self.require_current(state)
        if target in MAIN_ENTRIES:
            if continuation!=0x3CE:raise MovementContinuationBoundary(target,frame,'startup Main requires actual3CE')
            return (yield from self.startup_views['main',MAIN_ENTRIES[target]](state,frame))
        if (target,continuation)==(0x6826,0xA1B8):
            return (yield from self._service(state,frame,'initialize_video_registers_and_planes_fields'))
        if (target,continuation)==(0x68CE,0xA1C2):
            return (yield from self._service(state,frame,'clear_video_sprite_plane_fields'))
        return (yield from super()._display_child(state,frame,target,continuation))

    def main_scene_call(self,state,frame,target,continuation):
        if target not in MAIN_ENTRIES:return (yield from super().main_scene_call(state,frame,target,continuation))
        self.require_current(state)
        if self._started or continuation!=0x3CE:raise ValueError('one actual indexed startup Main invocation required')
        self._started=True
        return (yield from self.views['display','display_call_fields'](state,frame,target,continuation))
