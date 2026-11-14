"""Whole Main4A0/4A4 selection and force-reassignment caller lifetimes.

The existing synchronous selection/reassignment algorithms remain their sole
owners. Only the two complete Main parents propagate their actual CALLs to
the mature AF48 Scene refresh continuation. No game/device progress is added.
"""
import ast
import copy
import importlib
import inspect
from types import CodeType, FunctionType

from . import battle_trigger_steps as battle
from .contexts_services import SceneRefreshMemory
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary

BattleScenePrograms=battle.BattleScenePrograms
MAIN_ENTRIES={0x4A0:'initialize_tactical_scene_fields',0x4A4:'initialize_tactical_selection_scene_fields'}
REFRESH_RETURNS=(0xE92,0xEA4)
EXPECTED_MAIN_SOURCE = {'initialize_tactical_scene_fields': 'def initialize_tactical_scene_fields(state: SceneState, frame: '
                                     'FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                     '    """4A0: initialize tactical scene; original stage and child '
                                     'tokens."""\n'
                                     '    frame = _city_ui_frame_fields(state, frame, 1184)\n'
                                     '    frame = _campaign_call_fields(state, frame, 418988, 3724)\n'
                                     '    frame = _campaign_call_fields(state, frame, 44872, 3730)\n'
                                     '    return frame',
 'initialize_tactical_selection_scene_fields': 'def initialize_tactical_selection_scene_fields(state: '
                                               'SceneState, frame: FirstDeploymentFrame) -> '
                                               'FirstDeploymentFrame:\n'
                                               '    """4A4: initialize tactical selection scene; original '
                                               'stage and child tokens."""\n'
                                               '    frame = _city_ui_frame_fields(state, frame, 1188)\n'
                                               '    state.sr = 9984\n'
                                               '    frame = first_replace(frame, status=0)\n'
                                               '    frame = _campaign_call_fields(state, frame, 419350, '
                                               '3742)\n'
                                               '    frame = _campaign_call_fields(state, frame, 44872, '
                                               '3748)\n'
                                               '    return frame'}
EXPECTED_SELECTION_SOURCE = {'build_ten_officer_selection_fields': 'def build_ten_officer_selection_fields(state: SceneState, frame: '
                                       'FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                       '    """664AC: rank, fill trait classes 4/3/2, then publish at most '
                                       'ten names."""\n'
                                       '    frame = _highbank_frame_fields(state, frame, 418988)\n'
                                       "    frame = _movement_move(state, frame, 'target_x', 0, 16)\n"
                                       '    frame = _highbank_child_fields(state, frame, 419076, 418994)\n'
                                       '    for trait, continuation in ((4, 419010), (3, 419026), (2, '
                                       '419042)):\n'
                                       '        frame = _movement_compare(state, frame, '
                                       'low16(frame.target_x), 10, 16)\n'
                                       '        if not frame.status & 1:\n'
                                       '            break\n'
                                       "        frame = _movement_move(state, frame, 'distance', trait, 16)\n"
                                       '        frame = _highbank_child_fields(state, frame, 419196, '
                                       'continuation)\n'
                                       '    frame = first_replace(frame, '
                                       'roster=state.table_at(4294963456).cursor(), '
                                       'candidates=state.table_at(4294964480).cursor())\n'
                                       "    frame = _movement_move(state, frame, 'target_x', 0, 16)\n"
                                       '    while True:\n'
                                       '        value = frame.roster.word()\n'
                                       '        frame = first_replace(frame, '
                                       'roster=frame.roster.advance(2))\n'
                                       '        frame = _highbank_write_fields(state, frame, '
                                       'frame.candidates.base, value)\n'
                                       '        frame = first_replace(frame, '
                                       'candidates=frame.candidates.advance(2))\n'
                                       '        if frame.status & 8:\n'
                                       '            break\n'
                                       "        frame = _movement_add_word(state, frame, 'target_x', 1)\n"
                                       '        frame = _movement_compare(state, frame, '
                                       'low16(frame.target_x), 10, 16)\n'
                                       '        if not frame.status & 1:\n'
                                       '            break\n'
                                       '    frame = _highbank_write_fields(state, frame, '
                                       'frame.candidates.base, 65535)\n'
                                       '    return _highbank_write_fields(state, frame, 4294964790, '
                                       'low16(frame.target_x))',
 'sort_high_loyalty_officers_fields': 'def sort_high_loyalty_officers_fields(state: SceneState, frame: '
                                      'FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                      '    """66504: stable descending loyalty insertion, parallel '
                                      'names/scores."""\n'
                                      '    frame = _highbank_frame_fields(state, frame, 419076)\n'
                                      '    frame = first_replace(frame, '
                                      'controller=state.table_at(4294953984), '
                                      'scan=state.table_at(4294951680).cursor(), '
                                      'opponent=state.table_at(4294964263))\n'
                                      "    frame = _movement_move(state, frame, 'target_y', "
                                      'state.read(4294963120, 2), 16)\n'
                                      "    frame = _movement_move(state, frame, 'unit', 255, 16)\n"
                                      '    frame = _highbank_write_fields(state, frame, 4294963456, 65535)\n'
                                      '    while True:\n'
                                      "        frame = _movement_move(state, frame, 'count', "
                                      'frame.controller.byte(low16(frame.unit)), 8)\n'
                                      '        eligible = not bool(frame.status & 12)\n'
                                      '        if eligible:\n'
                                      "            frame = _movement_move(state, frame, 'count', "
                                      'low16(frame.count) & 63, 16)\n'
                                      '            frame = _movement_compare(state, frame, '
                                      'low8(frame.target_y), frame.opponent.byte(low16(frame.count)), 8)\n'
                                      '            eligible = bool(frame.status & 4)\n'
                                      '        if eligible:\n'
                                      '            frame = _movement_compare(state, frame, '
                                      'frame.scan.byte(low16(frame.unit)), 90, 8)\n'
                                      '            eligible = not bool(frame.status & 1)\n'
                                      '        if eligible:\n'
                                      "            frame = _movement_move(state, frame, 'count', 0, 16)\n"
                                      "            frame = _movement_move(state, frame, 'count', "
                                      'frame.scan.byte(low16(frame.unit)), 8)\n'
                                      '            frame = first_replace(frame, '
                                      'roster=state.table_at(4294963456).cursor(), '
                                      'candidates=state.table_at(4294963712).cursor())\n'
                                      "            frame = _movement_move(state, frame, 'distance', "
                                      'low16(frame.unit), 16)\n'
                                      '            while True:\n'
                                      '                frame = _movement_test(state, frame, '
                                      'frame.roster.word(), 16)\n'
                                      '                if frame.status & 8:\n'
                                      '                    break\n'
                                      '                frame = _movement_compare(state, frame, '
                                      'low16(frame.count), frame.candidates.word(), 16)\n'
                                      '                if not frame.status & 5:\n'
                                      '                    break\n'
                                      '                frame = first_replace(frame, '
                                      'roster=frame.roster.advance(2), '
                                      'candidates=frame.candidates.advance(2))\n'
                                      '            while True:\n'
                                      "                frame = _movement_move(state, frame, 'offset_y', "
                                      'frame.candidates.word(), 16)\n'
                                      '                frame = _highbank_write_fields(state, frame, '
                                      'frame.candidates.base, low16(frame.count))\n'
                                      '                frame = first_replace(frame, '
                                      'candidates=frame.candidates.advance(2))\n'
                                      "                frame = _movement_move(state, frame, 'count', "
                                      'low16(frame.offset_y), 16)\n'
                                      "                frame = _movement_move(state, frame, 'offset_x', "
                                      'frame.roster.word(), 16)\n'
                                      '                frame = _highbank_write_fields(state, frame, '
                                      'frame.roster.base, low16(frame.distance))\n'
                                      '                frame = first_replace(frame, '
                                      'roster=frame.roster.advance(2))\n'
                                      "                frame = _movement_move(state, frame, 'distance', "
                                      'low16(frame.offset_x), 16)\n'
                                      '                if frame.status & 8:\n'
                                      '                    break\n'
                                      '            frame = _highbank_write_fields(state, frame, '
                                      'frame.roster.base, 65535)\n'
                                      "            frame = _movement_add_word(state, frame, 'target_x', 1)\n"
                                      "        frame = _highbank_dbra_fields(frame, 'unit')\n"
                                      '        if low16(frame.unit) == 65535:\n'
                                      '            return frame',
 'append_mid_loyalty_officers_by_trait_fields': 'def append_mid_loyalty_officers_by_trait_fields(state: '
                                                'SceneState, frame: FirstDeploymentFrame) -> '
                                                'FirstDeploymentFrame:\n'
                                                '    """6657C: append this requested trait without '
                                                'disturbing high-loyalty order."""\n'
                                                '    frame = _highbank_frame_fields(state, frame, 419196)\n'
                                                '    frame = first_replace(frame, '
                                                'roster=state.table_at(4294963456).cursor())\n'
                                                '    while True:\n'
                                                '        value = frame.roster.word()\n'
                                                '        frame = first_replace(frame, '
                                                'roster=frame.roster.advance(2))\n'
                                                '        frame = _movement_test(state, frame, value, 16)\n'
                                                '        if frame.status & 8:\n'
                                                '            break\n'
                                                '    frame = first_replace(frame, '
                                                'roster=frame.roster.advance(-2), '
                                                'candidates=state.table_at(4294953984).cursor(), '
                                                'controller=state.table_at(4294964263), '
                                                'scan=state.table_at(4294951680).cursor(), '
                                                'opponent=state.table_at(4294952704))\n'
                                                "    frame = _movement_move(state, frame, 'target_y', 255, "
                                                '16)\n'
                                                "    frame = _movement_move(state, frame, 'unit', "
                                                'state.read(4294963120, 2), 16)\n'
                                                '    while True:\n'
                                                "        frame = _movement_move(state, frame, 'count', "
                                                'frame.candidates.byte(low16(frame.target_y)), 8)\n'
                                                '        eligible = not bool(frame.status & 12)\n'
                                                '        if eligible:\n'
                                                "            frame = _movement_move(state, frame, 'count', "
                                                'low16(frame.count) & 63, 16)\n'
                                                '            frame = _movement_compare(state, frame, '
                                                'low8(frame.unit), '
                                                'frame.controller.byte(low16(frame.count)), 8)\n'
                                                '            eligible = bool(frame.status & 4)\n'
                                                '        if eligible:\n'
                                                '            frame = _movement_compare(state, frame, '
                                                'frame.scan.byte(low16(frame.target_y)), 80, 8)\n'
                                                '            eligible = not bool(frame.status & 1)\n'
                                                '        if eligible:\n'
                                                '            frame = _movement_compare(state, frame, '
                                                'frame.scan.byte(low16(frame.target_y)), 90, 8)\n'
                                                '            eligible = bool(frame.status & 1)\n'
                                                '        if eligible:\n'
                                                "            frame = _movement_move(state, frame, 'count', "
                                                'frame.opponent.byte(low16(frame.target_y)), 8)\n'
                                                "            frame = _movement_move(state, frame, 'count', "
                                                'low16(frame.count) & 7, 16)\n'
                                                '            frame = _movement_compare(state, frame, '
                                                'low8(frame.count), low8(frame.distance), 8)\n'
                                                '            eligible = bool(frame.status & 4)\n'
                                                '        if eligible:\n'
                                                '            frame = _highbank_write_fields(state, frame, '
                                                'frame.roster.base, low16(frame.target_y))\n'
                                                '            frame = first_replace(frame, '
                                                'roster=frame.roster.advance(2))\n'
                                                '            frame = _movement_add_word(state, frame, '
                                                "'target_x', 1)\n"
                                                "        frame = _highbank_dbra_fields(frame, 'target_y')\n"
                                                '        if low16(frame.target_y) == 65535:\n'
                                                '            return _highbank_write_fields(state, frame, '
                                                'frame.roster.base, 65535)',
 '_highbank_frame_fields': 'def _highbank_frame_fields(state: SceneState, frame: FirstDeploymentFrame, '
                           'entry: int) -> FirstDeploymentFrame:\n'
                           '    from ..high_level_remaining_flows.business_city import _resource_cost_frame\n'
                           '    return _resource_cost_frame(state, frame, entry)',
 '_highbank_write_fields': 'def _highbank_write_fields(state: SceneState, frame: FirstDeploymentFrame, '
                           'address: int, value, size: int=2, clear: bool=False) -> FirstDeploymentFrame:\n'
                           '    """MOVE/CLR memory, including the original CLR\'s physical prior read."""\n'
                           '    if size not in (1, 2, 4) or type(clear) is not bool:\n'
                           "        raise ValueError('actual Highbank memory width required')\n"
                           '    if clear:\n'
                           '        state.read(address, size)\n'
                           '    state.write(address, size, value)\n'
                           '    if size == 4:\n'
                           '        return _movement_test_long(state, frame, value)\n'
                           '    return _movement_test(state, frame, value, size * 8)',
 '_highbank_dbra_fields': 'def _highbank_dbra_fields(frame: FirstDeploymentFrame, name: str) -> '
                          'FirstDeploymentFrame:\n'
                          '    return first_replace(frame, **{name: replace_word(frame.carrier(name), '
                          'u16(low16(frame.carrier(name)) - 1))})',
 '_highbank_child_fields': 'def _highbank_child_fields(state: SceneState, frame: FirstDeploymentFrame, '
                           'target: int, continuation: int) -> FirstDeploymentFrame:\n'
                           '    """One actual child LONG; no new slot for a direct tail/JMP entry."""\n'
                           '    stack = frame.stack_cursor.advance(-4)\n'
                           '    stack.set_long(0, continuation)\n'
                           '    entered = first_replace(frame, stack_cursor=stack)\n'
                           '    result = _highbank_target_fields(state, entered, target)\n'
                           '    actual = result.stack_cursor.long()\n'
                           '    if actual != continuation:\n'
                           '        raise FirstDeploymentReturnBoundary(actual, result, continuation)\n'
                           '    return first_replace(result, stack_cursor=result.stack_cursor.advance(4))',
 '_highbank_target_fields': 'def _highbank_target_fields(state: SceneState, frame: FirstDeploymentFrame, '
                            'target: int) -> FirstDeploymentFrame:\n'
                            '    if target == 423858:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_coordinate_live_state_178_fields\n'
                            '        return highbank_coordinate_live_state_178_fields(state, frame)\n'
                            '    if target == 423940:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_coordinate_live_state_179_fields\n'
                            '        return highbank_coordinate_live_state_179_fields(state, frame)\n'
                            '    if target == 423960:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_coordinate_live_state_180_fields\n'
                            '        return highbank_coordinate_live_state_180_fields(state, frame)\n'
                            '    if target == 424024:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_coordinate_live_state_178_alternate_1_fields\n'
                            '        return highbank_coordinate_live_state_178_alternate_1_fields(state, '
                            'frame)\n'
                            '    if target == 424062:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_coordinate_live_state_178_alternate_2_fields\n'
                            '        return highbank_coordinate_live_state_178_alternate_2_fields(state, '
                            'frame)\n'
                            '    if target == 424098:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_update_live_fields_18_fields\n'
                            '        return highbank_update_live_fields_18_fields(state, frame)\n'
                            '    if target == 424104:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_select_live_state_44_fields\n'
                            '        return highbank_select_live_state_44_fields(state, frame)\n'
                            '    if target == 424120:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_update_live_fields_19_fields\n'
                            '        return highbank_update_live_fields_19_fields(state, frame)\n'
                            '    if target == 424126:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_update_live_fields_20_fields\n'
                            '        return highbank_update_live_fields_20_fields(state, frame)\n'
                            '    if target == 424132:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_update_live_fields_21_fields\n'
                            '        return highbank_update_live_fields_21_fields(state, frame)\n'
                            '    if target == 424138:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_coordinate_live_state_181_fields\n'
                            '        return highbank_coordinate_live_state_181_fields(state, frame)\n'
                            '    if target == 424156:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_coordinate_live_state_182_fields\n'
                            '        return highbank_coordinate_live_state_182_fields(state, frame)\n'
                            '    if target == 424192:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_update_live_fields_22_fields\n'
                            '        return highbank_update_live_fields_22_fields(state, frame)\n'
                            '    if target == 424198:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_update_live_fields_23_fields\n'
                            '        return highbank_update_live_fields_23_fields(state, frame)\n'
                            '    if target == 424204:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_coordinate_live_state_183_fields\n'
                            '        return highbank_coordinate_live_state_183_fields(state, frame)\n'
                            '    if target == 424222:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_coordinate_live_state_178_alternate_3_fields\n'
                            '        return highbank_coordinate_live_state_178_alternate_3_fields(state, '
                            'frame)\n'
                            '    if target == 424230:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_coordinate_live_state_178_alternate_4_fields\n'
                            '        return highbank_coordinate_live_state_178_alternate_4_fields(state, '
                            'frame)\n'
                            '    if target == 424238:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_update_live_fields_24_fields\n'
                            '        return highbank_update_live_fields_24_fields(state, frame)\n'
                            '    if target == 424244:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_update_live_fields_25_fields\n'
                            '        return highbank_update_live_fields_25_fields(state, frame)\n'
                            '    if target == 424250:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_coordinate_live_state_178_alternate_5_fields\n'
                            '        return highbank_coordinate_live_state_178_alternate_5_fields(state, '
                            'frame)\n'
                            '    if target == 424270:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_update_live_fields_26_fields\n'
                            '        return highbank_update_live_fields_26_fields(state, frame)\n'
                            '    if target == 424276:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_coordinate_live_state_178_alternate_6_fields\n'
                            '        return highbank_coordinate_live_state_178_alternate_6_fields(state, '
                            'frame)\n'
                            '    if target == 424284:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_update_live_fields_27_fields\n'
                            '        return highbank_update_live_fields_27_fields(state, frame)\n'
                            '    if target == 424290:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_update_live_fields_28_fields\n'
                            '        return highbank_update_live_fields_28_fields(state, frame)\n'
                            '    if target == 424296:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_update_live_fields_29_fields\n'
                            '        return highbank_update_live_fields_29_fields(state, frame)\n'
                            '    if target == 424302:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_update_live_fields_30_fields\n'
                            '        return highbank_update_live_fields_30_fields(state, frame)\n'
                            '    if target == 424308:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_update_live_fields_31_fields\n'
                            '        return highbank_update_live_fields_31_fields(state, frame)\n'
                            '    if target == 424314:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_update_live_fields_32_fields\n'
                            '        return highbank_update_live_fields_32_fields(state, frame)\n'
                            '    if target == 424320:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_coordinate_live_state_184_fields\n'
                            '        return highbank_coordinate_live_state_184_fields(state, frame)\n'
                            '    if target == 424376:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_coordinate_live_state_178_alternate_7_fields\n'
                            '        return highbank_coordinate_live_state_178_alternate_7_fields(state, '
                            'frame)\n'
                            '    if target == 424384:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_update_live_fields_33_fields\n'
                            '        return highbank_update_live_fields_33_fields(state, frame)\n'
                            '    if target == 424390:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_update_live_fields_34_fields\n'
                            '        return highbank_update_live_fields_34_fields(state, frame)\n'
                            '    if target == 424396:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'highbank_update_live_fields_35_fields\n'
                            '        return highbank_update_live_fields_35_fields(state, frame)\n'
                            '    if target == 422492:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'toggle_scenario_choice_fields\n'
                            '        return toggle_scenario_choice_fields(state, frame)\n'
                            '    if target == 422504:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'compose_scenario_numeric_text_fields\n'
                            '        return compose_scenario_numeric_text_fields(state, frame)\n'
                            '    if target == 422556:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'compose_scenario_numeric_text_fields_entry_6729c\n'
                            '        return compose_scenario_numeric_text_fields_entry_6729c(state, frame)\n'
                            '    if target == 422562:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'compose_scenario_member_name_fields\n'
                            '        return compose_scenario_member_name_fields(state, frame)\n'
                            '    if target == 422630:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'compose_scenario_member_name_fields_entry_672e6\n'
                            '        return compose_scenario_member_name_fields_entry_672e6(state, frame)\n'
                            '    if target == 422636:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'restore_scenario_previous_text_fields\n'
                            '        return restore_scenario_previous_text_fields(state, frame)\n'
                            '    if target == 422646:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'compose_scenario_member_name_fields_entry_672f6\n'
                            '        return compose_scenario_member_name_fields_entry_672f6(state, frame)\n'
                            '    if target == 422662:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'compose_scenario_status_pair_fields\n'
                            '        return compose_scenario_status_pair_fields(state, frame)\n'
                            '    if target == 422712:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'compose_scenario_numeric_text_fields_entry_67338\n'
                            '        return compose_scenario_numeric_text_fields_entry_67338(state, frame)\n'
                            '    if target == 422726:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'compose_scenario_numeric_text_fields_entry_67346\n'
                            '        return compose_scenario_numeric_text_fields_entry_67346(state, frame)\n'
                            '    if target == 422478:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'restore_scenario_saved_command_fields\n'
                            '        return restore_scenario_saved_command_fields(state, frame)\n'
                            '    if target == 423198:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'build_scenario_single_row_fields\n'
                            '        return build_scenario_single_row_fields(state, frame)\n'
                            '    if target == 423438:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'build_scenario_triple_columns_fields\n'
                            '        return build_scenario_triple_columns_fields(state, frame)\n'
                            '    if target == 423570:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'build_scenario_alternate_row_fields\n'
                            '        return build_scenario_alternate_row_fields(state, frame)\n'
                            '    if target == 420948:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'confirm_scenario_force_choice_fields\n'
                            '        return confirm_scenario_force_choice_fields(state, frame)\n'
                            '    if target == 423344:\n'
                            '        from ..high_level_remaining_flows.business_highbank import '
                            'build_scenario_paired_columns_fields\n'
                            '        return build_scenario_paired_columns_fields(state, frame)\n'
                            '    if target == 419076:\n'
                            '        return sort_high_loyalty_officers_fields(state, frame)\n'
                            '    if target == 419196:\n'
                            '        return append_mid_loyalty_officers_by_trait_fields(state, frame)\n'
                            '    if target == 422740:\n'
                            '        return append_scrolling_message_header_fields(state, frame)\n'
                            '    if target == 422796:\n'
                            '        return append_scrolling_message_glyph_fields(state, frame)\n'
                            '    if target == 422822:\n'
                            '        return append_scrolling_message_bitmap_fields(state, frame)\n'
                            '    if target == 423018:\n'
                            '        return lookup_message_layout_words_fields(state, frame)\n'
                            '    if target == 423054:\n'
                            '        return lookup_message_fill_pattern_fields(state, frame)\n'
                            '    if target == 423178:\n'
                            '        return lookup_message_decoration_style_fields(state, frame)\n'
                            '    if target == 44804:\n'
                            '        from ..high_level_gameplay_flow.contexts_services import '
                            'SceneRefreshMemory\n'
                            '        from ..high_level_scene_flows.business_scene import '
                            'expand_glyph_row_fields\n'
                            '        return expand_glyph_row_fields(SceneRefreshMemory(state), frame)\n'
                            '    if target == 41304:\n'
                            '        from .business_map import '
                            'refresh_world_cursor_attributes_alternate_1_frame_fields\n'
                            '        return refresh_world_cursor_attributes_alternate_1_frame_fields(state, '
                            'frame)\n'
                            '    if target == 55532:\n'
                            '        from .business_commands import '
                            'append_current_command_description_frame_fields\n'
                            '        return append_current_command_description_frame_fields(state, frame)\n'
                            '    if target == 240466:\n'
                            '        from ..high_level_gameplay_flow.contexts_services import '
                            'SceneRefreshMemory\n'
                            '        from ..high_level_scene_flows.business_scene import '
                            'write_vdp_swapped_byte_rle_stream_fields\n'
                            '        return '
                            'write_vdp_swapped_byte_rle_stream_fields(SceneRefreshMemory(state), frame)\n'
                            '    if target == 44048:\n'
                            '        from ..high_level_player_commands.contexts_display import '
                            'SpritePacketMemory\n'
                            '        from ..high_level_player_commands.business_display import '
                            'append_live_command_sprite_fields\n'
                            '        return append_live_command_sprite_fields(SpritePacketMemory(state), '
                            'frame, reset_scroll=False, initialize_clip=True)\n'
                            "    raise MovementContinuationBoundary(target, frame, 'actual Highbank child "
                            "has no admitted full-field return')"}
FORCE_SOURCE_PATH='tools/high_level_diplomacy_forces/business_scene_forces.py'
REGISTRY_PATH='tools.high_level_main_flows.compiler_scene_entries'
REUSED_DEPENDENCIES={
    'tools/high_level_main_flows/business_movement_support.py':(
        '_movement_frame','_movement_move','_movement_move_long','_movement_test',
        '_movement_compare','_movement_fixed_shift_word','_movement_multiply_word',
        '_movement_divu_word','_movement_save_longs','_movement_restore_longs'),
    'tools/high_level_remaining_flows/business_lowbank.py':(
        '_economy_delta_fields','_economy_logic_fields','_economy_long_shift_fields',
        '_economy_swap_fields','_lowbank_ui_store_fields'),
    'tools/high_level_gameplay_flow/business_battle.py':('choose_city_head_fields',),
    'tools/high_level_gameplay_flow/business_reuse.py':('apply_returning_officer_loyalty_fields',),
    'tools/high_level_battle_ai/business_formation.py':('first_deployment_random_fields',),
}


def _dump(node):
    return ast.dump(node,include_attributes=False)


def _code_shape(code):
    return tuple(getattr(code,name)for name in ('co_code','co_names','co_varnames',
        'co_argcount','co_posonlyargcount','co_kwonlyargcount','co_flags',
        'co_freevars','co_cellvars'))+(tuple(_code_shape(value)if type(value)is CodeType
            else value for value in code.co_consts),)


def _code_at(code,name):
    matches=[value for value in code.co_consts if type(value)is CodeType and value.co_name==name]
    if len(matches)!=1:raise ValueError('one complete lexical force-selection source owner required: '+name)
    return matches[0]


def _source_context(module):
    tree=ast.parse(inspect.getsource(module),filename=module.__file__)
    return tree,compile(tree,module.__file__,'exec',dont_inherit=True)


def _actual_function(module,name,node,compiled):
    function=getattr(module,name)
    if (type(function)is not FunctionType or function.__globals__ is not vars(module)
            or function.__module__!=module.__name__ or function.__qualname__!=name
            or function.__closure__ is not None or function.__code__.co_freevars
            or _code_shape(function.__code__)!=_code_shape(_code_at(compiled,name))):
        raise ValueError('actual complete-module force-selection function required: '+name)
    return function


def _main_source_tree(original):
    """Exactly four yield-from changes, preserving both whole FN/module ASTs."""
    result=copy.deepcopy(original);inverses={}
    for index,node in enumerate(original.body):
        if not isinstance(node,ast.FunctionDef)or node.name not in EXPECTED_MAIN_SOURCE:continue
        if _dump(node)!=_dump(ast.parse(EXPECTED_MAIN_SOURCE[node.name]).body[0]):
            raise ValueError('whole reviewed Main4A0/4A4 source changed: '+node.name)
        if any(isinstance(value,(ast.Yield,ast.YieldFrom))for value in ast.walk(node)):
            raise ValueError('original selection Main must remain synchronous')
        changes=[]

        class Lift(ast.NodeTransformer):
            def visit_Call(self,item):
                item=self.generic_visit(item)
                if isinstance(item.func,ast.Name)and item.func.id=='_campaign_call_fields':
                    before=copy.deepcopy(item);item.func.id='_force_selection_campaign_call'
                    after=ast.copy_location(ast.YieldFrom(value=item),item)
                    changes.append((before,copy.deepcopy(after)));return after
                return item

        derived=Lift().visit(copy.deepcopy(node))
        if len(changes)!=2:raise ValueError('two real CALL expressions per whole selection Main required')
        remaining=list(changes)

        class Inverse(ast.NodeTransformer):
            def visit_YieldFrom(self,item):
                for position,(before,after)in enumerate(remaining):
                    if _dump(item)==_dump(after):remaining.pop(position);return copy.deepcopy(before)
                raise ValueError('unadmitted selection Main cooperative expression')

        inverse=Inverse().visit(copy.deepcopy(derived))
        if remaining or _dump(inverse)!=_dump(node):
            raise ValueError('entire Main4A0/4A4 function inverse differs')
        result.body[index]=derived;inverses[index]=inverse
    if len(inverses)!=2:raise ValueError('both complete original selection Main owners required')
    restored=copy.deepcopy(result)
    for index,node in inverses.items():restored.body[index]=node
    if _dump(restored)!=_dump(original):raise ValueError('whole Main business module inverse differs')
    return ast.fix_missing_locations(result)


def _pin_class(module,cls,name,compiled,tree):
    nodes=[node for node in tree.body if isinstance(node,ast.ClassDef)and node.name==name]
    if len(nodes)!=1 or getattr(module,name)is not cls:
        raise ValueError('one actual complete force-selection parent class required: '+name)
    class_code=_code_at(compiled,name);bindings=[]
    for node in nodes[0].body:
        if not isinstance(node,ast.FunctionDef):continue
        descriptor=vars(cls).get(node.name)
        function=descriptor.__func__ if type(descriptor)is staticmethod else descriptor
        if (type(function)is not FunctionType or function.__globals__ is not vars(module)
                or function.__qualname__!=name+'.'+node.name
                or _code_shape(function.__code__)!=_code_shape(_code_at(class_code,node.name))):
            raise ValueError('actual complete-module parent method required: '+name+'.'+node.name)
        bindings.append((cls,node.name,descriptor,function,function.__code__))
    return bindings


class ForceSelectionScenePrograms(BattleScenePrograms):
    """Original two Main parents, actual3CE, four inner CALL slots, same Scene."""
    def __init__(self,state):
        if (BattleScenePrograms is not battle.BattleScenePrograms
                or ForceSelectionScenePrograms.__bases__!=(BattleScenePrograms,)):
            raise ValueError('one actual unchanged BattleScenePrograms base required')
        base_tree,base_code=_source_context(battle)
        self._selection_method_bindings=_pin_class(battle,BattleScenePrograms,
            'BattleScenePrograms',base_code,base_tree)
        own_module=inspect.getmodule(ForceSelectionScenePrograms)
        if own_module is None or vars(own_module)is not globals():
            raise ValueError('actual new force-selection provider module required')
        own_tree,own_code=_source_context(own_module)
        self._selection_method_bindings+=_pin_class(own_module,ForceSelectionScenePrograms,
            'ForceSelectionScenePrograms',own_code,own_tree)
        self._selection_classes=(BattleScenePrograms,ForceSelectionScenePrograms)
        self._selection_class_module=own_module
        self._selection_utility_bindings=[]
        for module,tree,code in ((battle,base_tree,base_code),(own_module,own_tree,own_code)):
            for node in tree.body:
                if isinstance(node,ast.FunctionDef):
                    function=_actual_function(module,node.name,node,code)
                    self._selection_utility_bindings.append((module,node.name,function,function.__code__))
        super().__init__(state)
        self.selection_originals={};self.selection_aliases=[]
        main=importlib.import_module('tools.high_level_main_flows.business_main')
        tree,code=_source_context(main)
        nodes={node.name:node for node in tree.body if isinstance(node,ast.FunctionDef)}
        for name,expected in EXPECTED_MAIN_SOURCE.items():
            if name not in nodes or _dump(nodes[name])!=_dump(ast.parse(expected).body[0]):
                raise ValueError('complete original force-selection Main source differs: '+name)
            self._remember(main,name,nodes[name],code)
        derived=compile(_main_source_tree(tree),main.__file__,'exec',dont_inherit=True)
        self.selection_namespace=dict(vars(main));alias='_force_selection_campaign_call'
        if alias in self.selection_namespace:raise ValueError('private selection alias must not shadow original source')
        self.selection_campaign_call=self.views['main','_campaign_call_fields']
        self.selection_namespace[alias]=self.selection_campaign_call
        self.selection_views={}
        for name in EXPECTED_MAIN_SOURCE:
            original=getattr(main,name)
            view=FunctionType(_code_at(derived,name),self.selection_namespace,name,original.__defaults__,None)
            view.__kwdefaults__=original.__kwdefaults__;view.__annotations__=dict(original.__annotations__)
            if not inspect.isgeneratorfunction(view):raise ValueError('complete selection Main generator required')
            self.selection_views[name]=view
        self._selection_view_owners={name:(view,view.__code__)for name,view in self.selection_views.items()}
        highbank=importlib.import_module('tools.high_level_main_flows.business_highbank')
        tree,code=_source_context(highbank)
        nodes={node.name:node for node in tree.body if isinstance(node,ast.FunctionDef)}
        for name,expected in EXPECTED_SELECTION_SOURCE.items():
            if name not in nodes or _dump(nodes[name])!=_dump(ast.parse(expected).body[0]):
                raise ValueError('whole mature officer-selection source differs: '+name)
            self._remember(highbank,name,nodes[name],code)
        self._pin_imports(highbank,tree)
        # Reuse the already public exact forces/dependency source contract.
        # Do not duplicate its fifteen algorithms or145KB frozen module AST.
        registry=importlib.import_module(REGISTRY_PATH)
        registry_tree,_=_source_context(registry);literals={}
        for node in registry_tree.body:
            if (isinstance(node,ast.Assign)and len(node.targets)==1
                    and isinstance(node.targets[0],ast.Name)
                    and node.targets[0].id in ('EXPECTED_MODULE_ASTS','EXPECTED_DEPENDENCY_ASTS')):
                literals[node.targets[0].id]=ast.literal_eval(node.value)
        if (set(literals)!={'EXPECTED_MODULE_ASTS','EXPECTED_DEPENDENCY_ASTS'}
                or registry.EXPECTED_MODULE_ASTS!=literals['EXPECTED_MODULE_ASTS']
                or registry.EXPECTED_DEPENDENCY_ASTS!=literals['EXPECTED_DEPENDENCY_ASTS']):
            raise ValueError('actual unchanged mature Scene-entry source registry required')
        self.selection_registry=registry
        self.selection_registry_modules=registry.EXPECTED_MODULE_ASTS
        self.selection_registry_dependencies=registry.EXPECTED_DEPENDENCY_ASTS
        self.selection_force_ast=registry.EXPECTED_MODULE_ASTS[FORCE_SOURCE_PATH]
        forces=importlib.import_module(FORCE_SOURCE_PATH[:-3].replace('/','.'))
        tree,code=_source_context(forces)
        if _dump(tree)!=self.selection_force_ast:
            raise ValueError('entire existing fifteen-owner force Frame module changed')
        for node in tree.body:
            if isinstance(node,ast.FunctionDef):self._remember(forces,node.name,node,code)
        constants=[node for node in tree.body if isinstance(node,ast.Assign)
            and any(isinstance(target,ast.Name)and target.id=='REAL_CALL_PAIRS'for target in node.targets)]
        if len(constants)!=1 or forces.REAL_CALL_PAIRS!=ast.literal_eval(constants[0].value):
            raise ValueError('actual finite force CALL pair table required')
        self.selection_force_module=forces;self.selection_force_pairs=forces.REAL_CALL_PAIRS
        self._pin_imports(forces,tree)
        self.selection_dependency_sources={}
        for path,names in REUSED_DEPENDENCIES.items():
            module=importlib.import_module(path[:-3].replace('/','.'));tree,code=_source_context(module)
            nodes={node.name:node for node in tree.body if isinstance(node,ast.FunctionDef)}
            for name in names:
                expected=registry.EXPECTED_DEPENDENCY_ASTS[path][name]
                if name not in nodes or _dump(nodes[name])!=expected:
                    raise ValueError('complete reused force dependency changed: '+name)
                self._remember(module,name,nodes[name],code)
                self.selection_dependency_sources[path,name]=expected
        self.selection_admissions=dict(confidence='confirmed_source_candidate_runtime_unverified',
            complete_Main_views=2,named_call_propagations=4,new_wait_types=0,
            original_outer_return=0x3CE,inner_returns=(0xE8C,0xE92,0xE9E,0xEA4),
            reused_force_owners=15,original_force_CALL_pairs=len(self.selection_force_pairs),
            officer_selection_owners=(0x664AC,0x66504,0x6657C),
            new_device_clock_or_budget=False)

    def _remember(self,module,name,node,code):
        function=_actual_function(module,name,node,code)
        self.selection_originals[module.__name__,name]=(module,function,function.__code__)
        return function

    def _pin_imports(self,module,tree):
        """Preserve the actual imported callable aliases used by mature cores."""
        for node in tree.body:
            if not isinstance(node,ast.ImportFrom):continue
            for alias in node.names:
                name=alias.asname or alias.name;value=getattr(module,name)
                if type(value)is FunctionType:
                    self.selection_aliases.append((module,name,value,value.__code__))

    def require_current(self,state):
        if (battle.BattleScenePrograms is not self._selection_classes[0]
                or BattleScenePrograms is not self._selection_classes[0]
                or self._selection_class_module.ForceSelectionScenePrograms is not self._selection_classes[1]
                or ForceSelectionScenePrograms is not self._selection_classes[1]
                or ForceSelectionScenePrograms.__bases__!=(self._selection_classes[0],)):
            raise ValueError('actual force-selection provider/base identity changed')
        for cls,name,descriptor,function,code in self._selection_method_bindings:
            if vars(cls).get(name)is not descriptor or function.__code__ is not code:
                raise ValueError('actual complete provider method changed: '+name)
        for module,name,function,code in self._selection_utility_bindings:
            if getattr(module,name)is not function or function.__code__ is not code:
                raise ValueError('actual complete provider source helper changed: '+name)
        super().require_current(state)
        if not hasattr(self,'selection_originals'):return
        for (path,name),(module,function,code)in self.selection_originals.items():
            if getattr(module,name)is not function or function.__code__ is not code:
                raise ValueError('actual mature force-selection callable changed: '+name)
        for module,name,function,code in self.selection_aliases:
            if getattr(module,name)is not function or function.__code__ is not code:
                raise ValueError('actual mature force-selection imported alias changed: '+name)
        if self.selection_views.keys()!=self._selection_view_owners.keys():
            raise ValueError('finite complete force-selection Main view set changed')
        for name,(view,code)in self._selection_view_owners.items():
            if self.selection_views[name]is not view or view.__code__ is not code:
                raise ValueError('whole force-selection private view changed: '+name)
        if self.selection_namespace.get('_force_selection_campaign_call')is not self.selection_campaign_call:
            raise ValueError('actual private selection CALL facade changed')
        registry=self.selection_registry
        if (registry.EXPECTED_MODULE_ASTS is not self.selection_registry_modules
                or registry.EXPECTED_DEPENDENCY_ASTS is not self.selection_registry_dependencies
                or registry.EXPECTED_MODULE_ASTS.get(FORCE_SOURCE_PATH)!=self.selection_force_ast
                or self.selection_force_module.REAL_CALL_PAIRS is not self.selection_force_pairs):
            raise ValueError('existing exact force source/CALL registry changed')
        for (path,name),expected in self.selection_dependency_sources.items():
            if registry.EXPECTED_DEPENDENCY_ASTS.get(path,{}).get(name)!=expected:
                raise ValueError('existing force dependency source contract changed: '+name)

    def _campaign_child(self,state,frame,target,continuation):
        self.require_current(state)
        if target==0x664AC:
            if continuation!=0xE8C:
                raise MovementContinuationBoundary(target,frame,'officer-selection parent requires originalE8C')
            return self.selection_originals['tools.high_level_main_flows.business_highbank',
                'build_ten_officer_selection_fields'][1](state,frame)
        if target==0x66616:
            if continuation!=0xE9E:
                raise MovementContinuationBoundary(target,frame,'force reassignment parent requires originalE9E')
            return self.selection_originals['tools.high_level_diplomacy_forces.business_scene_forces',
                'resolve_force_reassignment_fields'][1](state,frame)
        if target==0xAF48 and continuation in REFRESH_RETURNS:
            return (yield from self._refresh(SceneRefreshMemory(state),frame))
        return (yield from super()._campaign_child(state,frame,target,continuation))

    def _display_child(self,state,frame,target,continuation):
        self.require_current(state)
        if target in MAIN_ENTRIES:
            if continuation!=0x3CE:
                raise MovementContinuationBoundary(target,frame,'force-selection Main requires original3CE')
            return (yield from self.selection_views[MAIN_ENTRIES[target]](state,frame))
        return (yield from super()._display_child(state,frame,target,continuation))

    def main_scene_call(self,state,frame,target,continuation):
        if target not in MAIN_ENTRIES:
            return (yield from super().main_scene_call(state,frame,target,continuation))
        self.require_current(state)
        if self._started or continuation!=0x3CE:
            raise ValueError('one actual indexed force-selection Main invocation required')
        self._started=True
        return (yield from self.views['display','display_call_fields'](state,frame,target,continuation))
