"""Restricted semantic source admission with ordinary mnemonic lowering.

Explicit business text only; this is an intermediate structural compiler,
not arbitrary Python compilation or full natural-gameplay acceptance.
"""
from .compiler_common import CompileError,semantic_functions,lower_declared
from .target import LATE_PHASE_BINDINGS

APPROVED={'business_actions': {'sum_live_object_rosters',
                      'update_object_action_ai',
                      'upload_object_officer_name'},
 'business_early_phase': {'adjust_scene_scroll',
                          'begin_scene_palette_lighten',
                          'encode_six_decimal_digits'},
 'contexts_actions': {'DuelGlyphContext'},
 'contexts_early_phase': {'BattleActors',
                          'PhaseFrame',
                          'SceneControllerConditions',
                          'SceneControllerFrame',
                          'SceneControllerOutcome',
                          'phase_add_word',
                          'phase_bit',
                          'phase_compare',
                          'phase_controller_return',
                          'phase_enter_call',
                          'phase_finish_call',
                          'phase_from_controller',
                          'phase_logic',
                          'phase_operands'},
 'contexts_late_phase': {'ActionIconContext',
                         'DigitPanelContext',
                         'DigitPanelResult',
                         'ForcePanelContext',
                         'LatePhaseDispatch',
                         'checked_context',
                         'checked_phase'},
 'dataclasses': {'replace'},
 'domain': {'Boundary',
            'Cursor',
            'Long',
            'SceneState',
            'Table',
            'VideoPlaneAddress',
            'Word',
            'checked_state',
            'descending_inclusive',
            'divu_retained',
            'low16',
            'low8',
            'negative_word',
            'ram_view',
            'replace_byte',
            'replace_word',
            's16',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'},
 'services': {'SceneRenderFrame',
              'clear_scene_object_label_plane',
              'enqueue_sound_command',
              'read_vdp_plane_rle_rows_from_control',
              'set_vram_write_address'}}

DECLARATIONS={'_port': {'signature': 'state, name',
           'returns': None,
           'flow': "return ram_view(state, 'ram_' + name)"},
 '_word': {'signature': 'state, name',
           'returns': None,
           'flow': 'return _port(state, name).word()'},
 '_byte': {'signature': 'state, name',
           'returns': None,
           'flow': 'return _port(state, name).byte()'},
 '_put': {'signature': 'state, name, value',
          'returns': None,
          'flow': '_port(state, name).set_word(0, u16(value))'},
 '_increment': {'signature': 'state, name, amount=1',
                'returns': None,
                'flow': '_put(state, name, _word(state, name) + amount)'},
 '_input_bit': {'signature': 'state, name, bit',
                'returns': None,
                'flow': 'return bool(_byte(state, name) & 1 << bit)'},
 '_with_scene_views': {'signature': 'state, frame, actor=None, opponent=None',
                       'returns': None,
                       'flow': 'inherited = frame.actors\n'
                               'if actor is None and inherited is not None:\n'
                               '    actor = inherited.actor\n'
                               'if opponent is None and inherited is not None:\n'
                               '    opponent = inherited.opponent\n'
                               'if actor is None or opponent is None:\n'
                               '    return replace(frame, actors=None)\n'
                               'result = replace(frame, '
                               'actors=BattleActors(state.table_at(actor.base), '
                               'state.table_at(opponent.base)))\n'
                               'if result.live is not None:\n'
                               '    result = replace(result, live=replace(result.live, '
                               'actor=actor, traversal=opponent if type(opponent) is Cursor '
                               'else opponent.cursor()))\n'
                               'return result'},
 '_clear_object_labels': {'signature': 'state, frame, continuation=None',
                          'returns': None,
                          'flow': 'if frame.live is not None:\n'
                                  '    if continuation is None:\n'
                                  "        raise Boundary('complete label clear needs its "
                                  "actual call continuation')\n"
                                  '    live = phase_controller_return(state, frame)\n'
                                  '    result = state.service_at(262940, '
                                  'phase_enter_call(state, live, continuation))\n'
                                  '    if type(result) is not SceneControllerFrame:\n'
                                  "        raise Boundary('4031C label clear requires actual "
                                  "complete current return')\n"
                                  '    result.validate(state)\n'
                                  '    return phase_from_controller(state, '
                                  'phase_finish_call(state, result, continuation))\n'
                                  'from .services import clear_scene_object_label_plane\n'
                                  'clear_scene_object_label_plane(state)\n'
                                  'return _with_scene_views(state, frame, '
                                  'opponent=state.table_at(12582912))'},
 '_clear_action_links': {'signature': 'state',
                         'returns': None,
                         'flow': "for name in ('80ca', '80cc', '80ce', '80d0'):\n"
                                 '    _put(state, name, 65535)'},
 '_blank_video_words': {'signature': 'state, command, inclusive_count',
                        'returns': None,
                        'flow': 'state.mmio_write(12582916, 4, command)\n'
                                'for _ in descending_inclusive(inclusive_count):\n'
                                '    state.mmio_write(12582912, 2, 13107)'},
 '_decode_plane': {'signature': 'state, frame, source, address, rows, continuation=None',
                   'returns': None,
                   'flow': 'from .services import read_vdp_plane_rle_rows_from_control\n'
                           "_put(state, '8000', 32768)\n"
                           'if frame.live is not None:\n'
                           '    if continuation is None:\n'
                           "        raise Boundary('complete plane decoder needs its actual "
                           "call continuation')\n"
                           '    live = replace(phase_controller_return(state, frame), '
                           'source=state.table_at(source).cursor(), '
                           'destination=VideoPlaneAddress(address), extent=128, '
                           'row_count=replace_word(frame.live.row_count, rows))\n'
                           '    result = state.service_at(240334, phase_enter_call(state, '
                           'live, continuation))\n'
                           '    if type(result) is not SceneControllerFrame:\n'
                           "        raise Boundary('3AACE prompt plane requires actual "
                           "complete decoder return')\n"
                           '    result.validate(state)\n'
                           '    return phase_from_controller(state, phase_finish_call(state, '
                           'result, continuation))\n'
                           'outcome = read_vdp_plane_rle_rows_from_control(state, '
                           'state.table_at(source).cursor(), VideoPlaneAddress(address), 128, '
                           'rows)\n'
                           'return replace(frame, video_command=outcome.command_carrier)'},
 'latch_scene_controller_inputs': {'signature': 'state: SceneState, frame: PhaseFrame',
                                   'returns': 'PhaseFrame',
                                   'flow': 'checked_phase(frame, state)\n'
                                           "if _byte(state, '80da') == 0:\n"
                                           "    _put(state, '811c', _word(state, 'f602'))\n"
                                           "    _put(state, '811e', _word(state, 'f602'))\n"
                                           "    _put(state, '8120', 0)\n"
                                           '    return phase_operands(frame, phase_logic(0))\n'
                                           "if _byte(state, '80da') == 1:\n"
                                           '    value = replace_word(frame.video_command, '
                                           "_word(state, 'f602'))\n"
                                           '    value = replace_word(value, low16(value) | '
                                           "_word(state, 'f604'))\n"
                                           "    _put(state, '811c', value)\n"
                                           "    _put(state, '811e', _word(state, 'f602'))\n"
                                           "    last = _word(state, 'f604')\n"
                                           "    _put(state, '8120', last)\n"
                                           '    return phase_operands(frame, '
                                           'phase_logic(last), video_command=value)\n'
                                           "if _byte(state, '80da') == 2:\n"
                                           '    value = replace_word(frame.video_command, '
                                           "_word(state, 'f602'))\n"
                                           '    value = replace_word(value, low16(value) | '
                                           "_word(state, 'f604'))\n"
                                           "    _put(state, '811c', value)\n"
                                           "    _put(state, '811e', _word(state, 'f604'))\n"
                                           "    last = _word(state, 'f602')\n"
                                           "    _put(state, '8120', last)\n"
                                           '    return phase_operands(frame, '
                                           'phase_logic(last), video_command=value)\n'
                                           "_put(state, '811c', _word(state, 'f604'))\n"
                                           "_put(state, '811e', _word(state, 'f604'))\n"
                                           "_put(state, '8120', 0)\n"
                                           'return phase_operands(frame, phase_logic(0))'},
 'draw_two_prompt_backgrounds': {'signature': 'state: SceneState, frame: PhaseFrame',
                                 'returns': 'PhaseFrame',
                                 'flow': 'checked_phase(frame, state)\n'
                                         'frame = _decode_plane(state, frame, 282357, 51584, '
                                         '10, 256770)\n'
                                         'return _decode_plane(state, frame, 282776, 51648, '
                                         '10, 256802)'},
 'update_secondary_scene_totals': {'signature': 'state: SceneState, frame: PhaseFrame',
                                   'returns': 'PhaseFrame',
                                   'flow': 'checked_phase(frame, state)\n'
                                           'value = replace_word(frame.video_command, '
                                           "_word(state, '8106'))\n"
                                           'value = replace_word(value, u16(low16(value) + '
                                           "_word(state, '810a')))\n"
                                           "_put(state, '8276', value)\n"
                                           "_put(state, '8278', _word(state, '810e'))\n"
                                           'return replace(frame, video_command=value)'},
 'adjust_secondary_formation_scene': {'signature': 'state: SceneState, frame: PhaseFrame',
                                      'returns': 'PhaseFrame',
                                      'flow': 'checked_phase(frame, state)\n'
                                              'if frame.live is not None:\n'
                                              '    live = phase_controller_return(state, '
                                              'frame)\n'
                                              '    frame = adjust_secondary_formation(state, '
                                              'phase_from_controller(state, '
                                              'phase_enter_call(state, live, 257248)))\n'
                                              '    live = phase_controller_return(state, '
                                              'frame)\n'
                                              '    frame = phase_from_controller(state, '
                                              'phase_finish_call(state, live, 257248))\n'
                                              'else:\n'
                                              '    frame = adjust_secondary_formation(state, '
                                              'frame)\n'
                                              'value = replace_byte(frame.video_command, '
                                              "_byte(state, '811f'))\n"
                                              'value = replace_word(value, low16(value) & '
                                              '12)\n'
                                              'frame = phase_operands(frame, '
                                              'phase_logic(low16(value)), '
                                              'video_command=value)\n'
                                              'if low16(value):\n'
                                              '    frame = _clear_object_labels(state, frame, '
                                              '257262)\n'
                                              'else:\n'
                                              "    selected = _input_bit(state, '811f', 5)\n"
                                              '    frame = phase_operands(frame, '
                                              'phase_bit(frame, selected))\n'
                                              '    if selected:\n'
                                              "        _put(state, '813a', 8)\n"
                                              "        _put(state, '813c', 0)\n"
                                              "        _put(state, '814c', 0)\n"
                                              '        frame = phase_operands(frame, '
                                              'phase_logic(0))\n'
                                              '        frame = _clear_object_labels(state, '
                                              'frame, 257290)\n'
                                              'return frame'},
 'confirm_secondary_formation_scene': {'signature': 'state: SceneState, frame: PhaseFrame',
                                       'returns': 'PhaseFrame',
                                       'flow': 'return '
                                               'adjust_secondary_formation_scene(state, '
                                               'frame)'},
 '_begin_prompt': {'signature': 'state, frame, script, mark_active, reset_side=False',
                   'returns': None,
                   'flow': 'state.set_status_word(9984)\n'
                           'if reset_side:\n'
                           "    _put(state, '8116', 0)\n"
                           'state.mmio_write(12582916, 2, 36610)\n'
                           '_blank_video_words(state, 1610612738, 3455)\n'
                           'frame = _with_scene_views(state, frame, '
                           'opponent=state.table_at(12582912))\n'
                           "_put(state, '700c', 40960)\n"
                           "_port(state, '700e').set_long(0, script)\n"
                           "_put(state, '7014', 3)\n"
                           "_put(state, '7016', 1)\n"
                           'frame = replace(frame, '
                           'glyph_tokens=replace_word(frame.glyph_tokens, 65535))\n'
                           'frame = draw_two_prompt_backgrounds(state, frame)\n'
                           'state.set_status_word(9472)\n'
                           "_increment(state, '813c')\n"
                           'if mark_active:\n'
                           "    _put(state, '813e', 1)\n"
                           'return frame'},
 'begin_transition_prompt': {'signature': 'state: SceneState, frame: PhaseFrame',
                             'returns': 'PhaseFrame',
                             'flow': 'checked_phase(frame, state)\n'
                                     'return _begin_prompt(state, frame, 242540, False)'},
 'begin_duel_handoff_prompt': {'signature': 'state: SceneState, frame: PhaseFrame',
                               'returns': 'PhaseFrame',
                               'flow': 'checked_phase(frame, state)\n'
                                       'return _begin_prompt(state, frame, 242782, True)'},
 'begin_result_confirmation_prompt': {'signature': 'state: SceneState, frame: PhaseFrame',
                                      'returns': 'PhaseFrame',
                                      'flow': 'checked_phase(frame, state)\n'
                                              'return _begin_prompt(state, frame, 242824, '
                                              'True)'},
 'begin_secondary_confirmation_prompt': {'signature': 'state: SceneState, frame: PhaseFrame',
                                         'returns': 'PhaseFrame',
                                         'flow': 'checked_phase(frame, state)\n'
                                                 'return _begin_prompt(state, frame, 242810, '
                                                 'True)'},
 'begin_primary_confirmation_prompt': {'signature': 'state: SceneState, frame: PhaseFrame',
                                       'returns': 'PhaseFrame',
                                       'flow': 'checked_phase(frame, state)\n'
                                               'return _begin_prompt(state, frame, 242846, '
                                               'True, True)'},
 '_dismiss_prompt': {'signature': 'state, frame',
                     'returns': None,
                     'flow': 'frame = _clear_object_labels(state, frame, 258114)\n'
                             "_put(state, '813a', 0)\n"
                             "_put(state, '813c', 6)\n"
                             "_put(state, '813e', 0)\n"
                             'return phase_operands(frame, phase_logic(0))'},
 'update_action_mode_prompt': {'signature': 'state: SceneState, frame: PhaseFrame',
                               'returns': 'PhaseFrame',
                               'flow': 'checked_phase(frame, state)\n'
                                       'value = replace_word(frame.video_command, '
                                       "_word(state, '811e'))\n"
                                       "if _word(state, '8144'):\n"
                                       '    value = replace_word(value, _word(state, '
                                       "'8120'))\n"
                                       "_put(state, '8122', value)\n"
                                       'frame = adjust_selected_action_mode(state, '
                                       'replace(frame, video_command=value))\n'
                                       'frame = draw_both_force_status_panels(state, frame)\n'
                                       'value = replace_word(frame.video_command, '
                                       "_word(state, '8122'))\n"
                                       'value = replace_byte(value, low8(value) & 240)\n'
                                       'if low8(value):\n'
                                       '    frame = _dismiss_prompt(state, frame)\n'
                                       'return replace(frame, video_command=value)'},
 'dismiss_action_mode_prompt': {'signature': 'state: SceneState, frame: PhaseFrame',
                                'returns': 'PhaseFrame',
                                'flow': 'checked_phase(frame, state)\n'
                                        'value = replace_byte(frame.video_command, '
                                        "_byte(state, '811d'))\n"
                                        'value = replace_byte(value, low8(value) & 240)\n'
                                        'frame = phase_operands(frame, '
                                        'phase_logic(low8(value), 8), video_command=value)\n'
                                        'if low8(value):\n'
                                        '    frame = _dismiss_prompt(state, frame)\n'
                                        'return frame'},
 '_lighten_after_confirmation': {'signature': 'state, frame',
                                 'returns': None,
                                 'flow': 'from .business_early_phase import '
                                         'begin_scene_palette_lighten\n'
                                         '_clear_action_links(state)\n'
                                         'return replace(frame, '
                                         'video_command=begin_scene_palette_lighten(state, '
                                         '1))'},
 'confirm_duel_handoff_prompt': {'signature': 'state: SceneState, frame: PhaseFrame',
                                 'returns': 'PhaseFrame',
                                 'flow': 'checked_phase(frame, state)\n'
                                         'value = replace_byte(frame.video_command, '
                                         "_byte(state, '811d'))\n"
                                         'value = replace_byte(value, low8(value) & 240)\n'
                                         'frame = phase_operands(frame, '
                                         'phase_logic(low8(value), 8), video_command=value)\n'
                                         'if low8(value) and frame.live is not None:\n'
                                         "    raise Boundary('3F0E0 duel handoff "
                                         "totals/palette require complete shared return')\n"
                                         'return commit_duel_handoff(state, frame) if '
                                         'low8(value) else frame'},
 'commit_duel_handoff': {'signature': 'state: SceneState, frame: PhaseFrame',
                         'returns': 'PhaseFrame',
                         'flow': 'checked_phase(frame, state)\n'
                                 'frame = commit_scene_battle_totals(state, frame)\n'
                                 'frame = _lighten_after_confirmation(state, frame)\n'
                                 "_increment(state, '813c')\n"
                                 "_put(state, '70f2', 0)\n"
                                 "_port(state, '70f3').set_byte(0, _byte(state, '80db'))\n"
                                 "reversed_sides = bool(_word(state, '8124'))\n"
                                 'if not reversed_sides:\n'
                                 "    pairs = (('80dc', '7070'), ('80e0', '706a'), ('8178', "
                                 "'706c'), ('8104', '706e'), ('80de', '70c0'), ('80e2', "
                                 "'70ba'), ('8278', '70bc'), ('8106', '70be'))\n"
                                 '    directory = 258410\n'
                                 'else:\n'
                                 "    pairs = (('80de', '7070'), ('80e2', '706a'), ('8278', "
                                 "'706c'), ('8106', '706e'), ('80dc', '70c0'), ('80e0', "
                                 "'70ba'), ('8178', '70bc'), ('8104', '70be'))\n"
                                 '    directory = 258500\n'
                                 'for source, destination in pairs:\n'
                                 '    _put(state, destination, _word(state, source))\n'
                                 "value = _byte(state, '80da')\n"
                                 'value = replace_word(value, u16(low16(value) << 1))\n'
                                 "_put(state, '700a', "
                                 'state.table_at(directory).word(low16(value)))\n'
                                 'return replace(frame, video_command=value)'},
 '_await_palette': {'signature': 'state, frame',
                    'returns': None,
                    'flow': "selected = _input_bit(state, '80c4', 7)\n"
                            'frame = phase_operands(frame, phase_bit(frame, selected))\n'
                            'if selected:\n'
                            "    previous = _word(state, '813c')\n"
                            "    _put(state, '813c', previous + 1)\n"
                            '    frame = phase_operands(frame, phase_add_word(previous, 1))\n'
                            'return frame'},
 'await_duel_handoff_palette': {'signature': 'state: SceneState, frame: PhaseFrame',
                                'returns': 'PhaseFrame',
                                'flow': 'checked_phase(frame, state)\n'
                                        'return _await_palette(state, frame)'},
 'await_result_palette': {'signature': 'state: SceneState, frame: PhaseFrame',
                          'returns': 'PhaseFrame',
                          'flow': 'checked_phase(frame, state)\n'
                                  'return _await_palette(state, frame)'},
 'await_secondary_result_palette': {'signature': 'state: SceneState, frame: PhaseFrame',
                                    'returns': 'PhaseFrame',
                                    'flow': 'checked_phase(frame, state)\n'
                                            'return _await_palette(state, frame)'},
 'await_primary_result_palette': {'signature': 'state: SceneState, frame: PhaseFrame',
                                  'returns': 'PhaseFrame',
                                  'flow': 'checked_phase(frame, state)\n'
                                          'return _await_palette(state, frame)'},
 'finish_duel_handoff_phase': {'signature': 'state: SceneState, frame: PhaseFrame',
                               'returns': 'PhaseFrame',
                               'flow': 'return checked_phase(frame, state)'},
 'finish_result_phase': {'signature': 'state: SceneState, frame: PhaseFrame',
                         'returns': 'PhaseFrame',
                         'flow': 'return checked_phase(frame, state)'},
 'finish_secondary_result_phase': {'signature': 'state: SceneState, frame: PhaseFrame',
                                   'returns': 'PhaseFrame',
                                   'flow': 'return checked_phase(frame, state)'},
 'finish_primary_result_phase': {'signature': 'state: SceneState, frame: PhaseFrame',
                                 'returns': 'PhaseFrame',
                                 'flow': 'return checked_phase(frame, state)'},
 '_confirm_result': {'signature': 'state, frame, mask, increment_first',
                     'returns': None,
                     'flow': 'value = replace_byte(frame.video_command, _byte(state, '
                             "'811d'))\n"
                             'value = replace_byte(value, low8(value) & mask)\n'
                             'frame = phase_operands(frame, phase_logic(low8(value), 8), '
                             'video_command=value)\n'
                             'if not low8(value):\n'
                             '    return frame\n'
                             'if frame.live is not None:\n'
                             "    raise Boundary('result confirmation totals/palette require "
                             "complete shared return')\n"
                             'if increment_first:\n'
                             "    _increment(state, '813c')\n"
                             'frame = commit_scene_battle_totals(state, frame)\n'
                             'if not increment_first:\n'
                             "    _increment(state, '813c')\n"
                             'return _lighten_after_confirmation(state, frame)'},
 'confirm_result_prompt': {'signature': 'state: SceneState, frame: PhaseFrame',
                           'returns': 'PhaseFrame',
                           'flow': 'checked_phase(frame, state)\n'
                                   'return _confirm_result(state, frame, 240, False)'},
 'confirm_secondary_result_prompt': {'signature': 'state: SceneState, frame: PhaseFrame',
                                     'returns': 'PhaseFrame',
                                     'flow': 'checked_phase(frame, state)\n'
                                             'return _confirm_result(state, frame, 240, '
                                             'True)'},
 'confirm_primary_result_prompt': {'signature': 'state: SceneState, frame: PhaseFrame',
                                   'returns': 'PhaseFrame',
                                   'flow': 'checked_phase(frame, state)\n'
                                           'return _confirm_result(state, frame, 32, True)'},
 'replace_primary_confirmation_prompt': {'signature': 'state: SceneState, frame: PhaseFrame',
                                         'returns': 'PhaseFrame',
                                         'flow': 'checked_phase(frame, state)\n'
                                                 'value = replace_byte(frame.video_command, '
                                                 "_byte(state, '811d'))\n"
                                                 'value = replace_byte(value, low8(value) & '
                                                 '32)\n'
                                                 'frame = replace(frame, '
                                                 'video_command=value)\n'
                                                 'if not low8(value):\n'
                                                 '    return frame\n'
                                                 'state.set_status_word(9984)\n'
                                                 'state.mmio_write(12582916, 2, 36610)\n'
                                                 '_blank_video_words(state, 1610612738, '
                                                 '3455)\n'
                                                 'frame = _with_scene_views(state, frame, '
                                                 'opponent=state.table_at(12582912))\n'
                                                 "_put(state, '700c', 40960)\n"
                                                 "_port(state, '700e').set_long(0, 242870)\n"
                                                 "_put(state, '7014', 3)\n"
                                                 "_put(state, '7016', 1)\n"
                                                 "_increment(state, '813c')\n"
                                                 'state.set_status_word(9472)\n'
                                                 'return replace(frame, '
                                                 'glyph_tokens=replace_word(frame.glyph_tokens, '
                                                 '65535))'},
 'normalize_secondary_squad_size': {'signature': 'state: SceneState, frame: PhaseFrame',
                                    'returns': 'PhaseFrame',
                                    'flow': 'checked_phase(frame, state)\n'
                                            'while True:\n'
                                            "    value = _word(state, '80e6')\n"
                                            "    count = _word(state, '80ea')\n"
                                            '    if count == 0:\n'
                                            "        _increment(state, '80ea')\n"
                                            '        continue\n'
                                            '    if count > 15:\n'
                                            "        _increment(state, '80ea', -1)\n"
                                            '        continue\n'
                                            '    value = divu_retained(value, count)\n'
                                            '    if low16(value) > 1000:\n'
                                            "        _increment(state, '80ea')\n"
                                            '        continue\n'
                                            '    if low16(value) <= 100:\n'
                                            "        if _word(state, '80ea') != 1:\n"
                                            "            _increment(state, '80ea', -1)\n"
                                            '            continue\n'
                                            '        if low16(value) == 0:\n'
                                            "            _put(state, '80ee', 0)\n"
                                            "            _put(state, '80f2', 0)\n"
                                            '            return replace(frame, '
                                            'video_command=value, foreground=count)\n'
                                            "    _put(state, '80ee', value)\n"
                                            '    value = swap_words(value)\n'
                                            "    _put(state, '80f2', value)\n"
                                            '    return replace(frame, video_command=value, '
                                            'foreground=count)'},
 'adjust_secondary_squad_count': {'signature': 'state: SceneState, frame: PhaseFrame',
                                  'returns': 'PhaseFrame',
                                  'flow': 'checked_phase(frame, state)\n'
                                          "if _input_bit(state, '811f', 0):\n"
                                          "    _increment(state, '80ea')\n"
                                          "if _input_bit(state, '811f', 1):\n"
                                          "    _increment(state, '80ea', -1)\n"
                                          'return frame'},
 'adjust_selected_squad_class_counts': {'signature': 'state: SceneState, frame: PhaseFrame',
                                        'returns': 'PhaseFrame',
                                        'flow': 'checked_phase(frame, state)\n'
                                                'value, capacity_index = '
                                                '(frame.video_command, frame.foreground)\n'
                                                "if _input_bit(state, '811f', 0):\n"
                                                '    value = replace_word(value, _word(state, '
                                                "'80fa'))\n"
                                                '    value = replace_word(value, '
                                                "u16(low16(value) + _word(state, '80fc')))\n"
                                                '    value = replace_word(value, '
                                                "u16(low16(value) + _word(state, '80fe')))\n"
                                                "    if low16(value) < _word(state, '80ea'):\n"
                                                '        value = replace_word(value, '
                                                "_word(state, '8144'))\n"
                                                '        value = replace_word(value, '
                                                'u16(low16(value) << 2))\n'
                                                '        selected = '
                                                'state.table_at(state.table_at(259576).long(low16(value)))\n'
                                                '        quality_band = 0\n'
                                                "        if _word(state, '8112') > 100:\n"
                                                '            quality_band = 1\n'
                                                "            if _word(state, '8112') > 200:\n"
                                                '                quality_band = 2\n'
                                                "                if _word(state, '8112') > "
                                                '300:\n'
                                                '                    quality_band = 3\n'
                                                "                    if _word(state, '8112') "
                                                '> 400:\n'
                                                '                        quality_band = 4\n'
                                                '                        if _word(state, '
                                                "'8112') > 500:\n"
                                                '                            quality_band = '
                                                '5\n'
                                                '                            if _word(state, '
                                                "'8112') > 600:\n"
                                                '                                quality_band '
                                                '= 6\n'
                                                '        value = quality_band\n'
                                                '        capacity_index = '
                                                'replace_word(capacity_index, _word(state, '
                                                "'8144'))\n"
                                                '        capacity_index = '
                                                'replace_word(capacity_index, '
                                                'u16(low16(capacity_index) << 3))\n'
                                                '        capacity_index = '
                                                'replace_word(capacity_index, '
                                                'u16(low16(capacity_index) + low16(value)))\n'
                                                '        value = replace_word(value, '
                                                'selected.word())\n'
                                                '        limit = '
                                                'state.table_at(259588).byte(low16(capacity_index))\n'
                                                '        if low8(value) < limit:\n'
                                                '            selected.set_word(0, '
                                                'u16(selected.word() + 1))\n'
                                                "if _input_bit(state, '811f', 1):\n"
                                                '    value = replace_word(value, _word(state, '
                                                "'8144'))\n"
                                                '    value = replace_word(value, '
                                                'u16(low16(value) << 2))\n'
                                                '    selected = '
                                                'state.table_at(state.table_at(259576).long(low16(value)))\n'
                                                '    if selected.word():\n'
                                                '        selected.set_word(0, '
                                                'u16(selected.word() - 1))\n'
                                                "if _input_bit(state, '811f', 5) and "
                                                "_word(state, '8144') < 2:\n"
                                                "    _increment(state, '8144')\n"
                                                "if _input_bit(state, '811f', 4) and "
                                                "_word(state, '8144'):\n"
                                                "    _increment(state, '8144', -1)\n"
                                                'return replace(frame, video_command=value, '
                                                'foreground=capacity_index)'},
 '_adjust_formation_choice': {'signature': 'state',
                              'returns': None,
                              'flow': "if _input_bit(state, '811f', 2):\n"
                                      "    _increment(state, '8144')\n"
                                      "    if _word(state, '8144') >= 5:\n"
                                      "        _put(state, '8144', 0)\n"
                                      "if _input_bit(state, '811f', 3):\n"
                                      "    reduced = u16(_word(state, '8144') - 1)\n"
                                      "    _put(state, '8144', reduced)\n"
                                      '    if negative_word(reduced):\n'
                                      "        _put(state, '8144', 4)"},
 '_deploy_formation': {'signature': 'state, frame, secondary',
                       'returns': None,
                       'flow': 'value = replace_word(frame.video_command, _word(state, '
                               "'8144'))\n"
                               'value = replace_word(value, u16(low16(value) << 2))\n'
                               'layout = '
                               'state.table_at(state.table_at(268888).long(low16(value))).cursor()\n'
                               "first = replace_word(frame.foreground, _word(state, '80fa'))\n"
                               "second = replace_word(frame.mode, _word(state, '80fc'))\n"
                               "third = replace_word(frame.row_count, _word(state, '80fe'))\n"
                               'leader_written = 0\n'
                               "actor = _port(state, '826a' if secondary else '816a')\n"
                               'end = 4294935402 if secondary else 4294935146\n'
                               'while True:\n'
                               '    if secondary:\n'
                               '        value = replace_word(value, 352)\n'
                               '        value = replace_word(value, u16(low16(value) - '
                               'layout.next_word()))\n'
                               '        actor.set_word(2, low16(value))\n'
                               '    else:\n'
                               '        actor.set_word(2, layout.next_word())\n'
                               '    actor.set_word(4, layout.next_word())\n'
                               '    actor.set_word(6, 1)\n'
                               '    actor.set_word(8, 1)\n'
                               '    if leader_written == 0:\n'
                               '        actor.set_word(0, 32771)\n'
                               '        leader_written = 1\n'
                               '    elif low16(first):\n'
                               '        actor.set_word(0, 32770)\n'
                               '        first = replace_word(first, u16(low16(first) - 1))\n'
                               '    elif low16(second):\n'
                               '        actor.set_word(0, 32769)\n'
                               '        second = replace_word(second, u16(low16(second) - '
                               '1))\n'
                               '    elif low16(third):\n'
                               '        actor.set_word(0, 32768)\n'
                               '        third = replace_word(third, u16(low16(third) - 1))\n'
                               '    else:\n'
                               '        conditions = phase_logic(third)\n'
                               '        break\n'
                               '    actor = actor.advance(16)\n'
                               '    conditions = phase_compare(actor.base, end, 32)\n'
                               '    if actor.base >= end:\n'
                               '        break\n'
                               'frame = phase_operands(frame, conditions, '
                               'video_command=value, foreground=first, mode=second, '
                               'row_count=third, tile=leader_written)\n'
                               'frame = _with_scene_views(state, frame, actor=actor, '
                               'opponent=layout)\n'
                               'if frame.live is not None:\n'
                               '    frame = phase_from_controller(state, replace(frame.live, '
                               'source=state.table_at(268888).cursor()))\n'
                               'return frame'},
 'adjust_secondary_formation': {'signature': 'state: SceneState, frame: PhaseFrame',
                                'returns': 'PhaseFrame',
                                'flow': 'checked_phase(frame, state)\n'
                                        '_adjust_formation_choice(state)\n'
                                        'return _deploy_formation(state, frame, True)'},
 'deploy_secondary_formation': {'signature': 'state: SceneState, frame: PhaseFrame',
                                'returns': 'PhaseFrame',
                                'flow': 'checked_phase(frame, state)\n'
                                        'return _deploy_formation(state, frame, True)'},
 'adjust_primary_formation': {'signature': 'state: SceneState, frame: PhaseFrame',
                              'returns': 'PhaseFrame',
                              'flow': 'checked_phase(frame, state)\n'
                                      '_adjust_formation_choice(state)\n'
                                      'return _deploy_formation(state, frame, False)'},
 'deploy_primary_formation': {'signature': 'state: SceneState, frame: PhaseFrame',
                              'returns': 'PhaseFrame',
                              'flow': 'checked_phase(frame, state)\n'
                                      'return _deploy_formation(state, frame, False)'},
 'adjust_selected_action_mode': {'signature': 'state: SceneState, frame: PhaseFrame',
                                 'returns': 'PhaseFrame',
                                 'flow': 'checked_phase(frame, state)\n'
                                         "if _byte(state, '80db') != 3:\n"
                                         "    if not _input_bit(state, '8122', 0) and (not "
                                         "_input_bit(state, '8122', 1)):\n"
                                         "        if _input_bit(state, '8123', 3):\n"
                                         "            _increment(state, '8146')\n"
                                         "            if _word(state, '8146') >= 4:\n"
                                         "                _put(state, '8146', 0)\n"
                                         "            if _word(state, '8148') == 6:\n"
                                         "                _put(state, '8146', 1)\n"
                                         "        if _input_bit(state, '8123', 2):\n"
                                         "            if _word(state, '8148') == 6:\n"
                                         "                _increment(state, '8146', -1)\n"
                                         "                if _word(state, '8146') == 0:\n"
                                         "                    _put(state, '8146', 3)\n"
                                         '            else:\n'
                                         "                _increment(state, '8146', -1)\n"
                                         '                if negative_word(_word(state, '
                                         "'8146')):\n"
                                         "                    _put(state, '8146', 3)\n"
                                         "elif _word(state, '8148') == 6:\n"
                                         "    _put(state, '8146', 2)\n"
                                         "elif not _input_bit(state, '8122', 0) and (not "
                                         "_input_bit(state, '8122', 1)):\n"
                                         "    if _input_bit(state, '8123', 3) or "
                                         "_input_bit(state, '8123', 2):\n"
                                         "        _increment(state, '8146', -2)\n"
                                         "        if negative_word(_word(state, '8146')):\n"
                                         "            _put(state, '8146', 2)\n"
                                         'value = replace_word(frame.video_command, '
                                         "_word(state, '8146'))\n"
                                         'value = replace_byte(value, '
                                         'state.table_at(260160).byte(low16(value)))\n'
                                         "if _word(state, '8144') == 0:\n"
                                         '    value = replace_word(value, u16(low16(value) + '
                                         '4))\n'
                                         'value = replace_word(value, u16(low16(value) << '
                                         '1))\n'
                                         "selected = _port(state, '812a').at(low16(value))\n"
                                         "if _input_bit(state, '8123', 0):\n"
                                         '    selected.set_word(0, u16(selected.word() + 1))\n'
                                         "    if _word(state, '8160') < 17:\n"
                                         '        if selected.word() >= 6:\n'
                                         '            selected.set_word(0, 0)\n'
                                         '    elif selected.word() > 6:\n'
                                         '        selected.set_word(0, 0)\n'
                                         "if _input_bit(state, '8123', 1):\n"
                                         '    selected.set_word(0, u16(selected.word() - 1))\n'
                                         '    if negative_word(selected.word()):\n'
                                         '        selected.set_word(0, 6)\n'
                                         "        if _word(state, '8160') < 17:\n"
                                         '            selected.set_word(0, 5)\n'
                                         'return replace(frame, video_command=value)'},
 'commit_scene_battle_totals': {'signature': 'state: SceneState, frame: PhaseFrame',
                                'returns': 'PhaseFrame',
                                'flow': 'checked_phase(frame, state)\n'
                                        'from .business_actions import '
                                        'sum_live_object_rosters\n'
                                        'outcome = sum_live_object_rosters(state, '
                                        'frame.video_command)\n'
                                        "_put(state, '8118', outcome.first_total)\n"
                                        "_put(state, '811a', outcome.second_total)\n"
                                        "_put(state, '810c', _word(state, '8178'))\n"
                                        "_put(state, '810e', _word(state, '8278'))\n"
                                        'frame = replace(frame, '
                                        'video_command=outcome.command, '
                                        'foreground=outcome.first_total, '
                                        'mode=outcome.second_total, '
                                        'row_count=outcome.first_count, '
                                        'tile=outcome.second_count)\n'
                                        'return _with_scene_views(state, frame, '
                                        'actor=outcome.roster_end)'},
 'draw_decimal_panel': {'signature': 'state: SceneState, context: DigitPanelContext',
                        'returns': 'DigitPanelResult',
                        'flow': 'checked_context(context, DigitPanelContext, state)\n'
                                'from .services import set_vram_write_address\n'
                                'source, frame = (context.source, context.frame)\n'
                                'state.mmio_write(12582916, 2, 36610)\n'
                                'command = set_vram_write_address(state, '
                                'frame.video_command)\n'
                                'started = 0\n'
                                'counter = frame.row_count\n'
                                'foreground = frame.foreground\n'
                                'for remaining in descending_inclusive(low16(counter)):\n'
                                '    digit = source.next_byte()\n'
                                '    foreground = digit\n'
                                '    if digit or low16(started) or remaining == 0:\n'
                                '        started = 1\n'
                                '        foreground = replace_word(foreground, '
                                'u16(low16(foreground) + 50272))\n'
                                '    else:\n'
                                '        foreground = replace_word(foreground, 50248)\n'
                                '    state.mmio_write(12582912, 2, low16(foreground))\n'
                                'return DigitPanelResult(source, replace(frame, '
                                'video_command=command, foreground=foreground, mode=started, '
                                'row_count=replace_word(counter, 65535)))'},
 'draw_blinking_decimal_panel': {'signature': 'state: SceneState, context: DigitPanelContext',
                                 'returns': 'DigitPanelResult',
                                 'flow': 'checked_context(context, DigitPanelContext, state)\n'
                                         'from .services import set_vram_write_address\n'
                                         "if _input_bit(state, 'f321', 4):\n"
                                         '    return draw_decimal_panel(state, context)\n'
                                         'frame = context.frame\n'
                                         'state.mmio_write(12582916, 2, 36610)\n'
                                         'command = set_vram_write_address(state, '
                                         'frame.video_command)\n'
                                         'foreground = replace_word(frame.foreground, 50248)\n'
                                         'for _ in '
                                         'descending_inclusive(low16(frame.row_count)):\n'
                                         '    state.mmio_write(12582912, 2, '
                                         'low16(foreground))\n'
                                         'return DigitPanelResult(context.source, '
                                         'replace(frame, video_command=command, '
                                         'foreground=foreground, '
                                         'row_count=replace_word(frame.row_count, 65535)))'},
 '_number_panel': {'signature': 'state, frame, number, address, count, digit_offset, '
                                'blinking=False, selected_class=None',
                   'returns': None,
                   'flow': 'from .business_early_phase import encode_six_decimal_digits\n'
                           'digits = encode_six_decimal_digits(state, number)\n'
                           'if type(address) is str:\n'
                           '    address = _word(state, address)\n'
                           'frame = replace(frame, video_command=replace_word(digits.value, '
                           'address), mode=replace_word(frame.mode, 10), row_count=count)\n'
                           'context = DigitPanelContext(_port(state, '
                           "'8000').cursor(digit_offset), frame)\n"
                           'if selected_class is not None:\n'
                           "    blinking = _word(state, '8144') == selected_class\n"
                           'outcome = draw_blinking_decimal_panel(state, context) if blinking '
                           'else draw_decimal_panel(state, context)\n'
                           'return outcome.frame'},
 'draw_secondary_squad_budget': {'signature': 'state: SceneState, frame: PhaseFrame',
                                 'returns': 'PhaseFrame',
                                 'flow': 'checked_phase(frame, state)\n'
                                         'frame = _number_panel(state, frame, _word(state, '
                                         "'80e6'), 50094, 4, 1)\n"
                                         'frame = _number_panel(state, frame, _word(state, '
                                         "'80ee'), 50480, 3, 2)\n"
                                         'return _number_panel(state, frame, _word(state, '
                                         "'80ea'), 50868, 1, 4, True)"},
 'draw_squad_class_budgets': {'signature': 'state: SceneState, frame: PhaseFrame',
                              'returns': 'PhaseFrame',
                              'flow': 'checked_phase(frame, state)\n'
                                      'frame = _number_panel(state, frame, _word(state, '
                                      "'80ea'), 49580, 1, 4)\n"
                                      'frame = _number_panel(state, frame, _word(state, '
                                      "'80fa'), 50092, 1, 4, selected_class=0)\n"
                                      'frame = _number_panel(state, frame, _word(state, '
                                      "'80fc'), 50604, 1, 4, selected_class=1)\n"
                                      'return _number_panel(state, frame, _word(state, '
                                      "'80fe'), 51116, 1, 4, selected_class=2)"},
 '_sum_active_roster': {'signature': 'state, frame, source, class_id=None',
                        'returns': None,
                        'flow': 'total = 0\n'
                                'count = replace_word(frame.foreground, 14)\n'
                                'actor = source\n'
                                'for _ in descending_inclusive(14):\n'
                                '    if actor.byte() & 128:\n'
                                '        if class_id is None or actor.byte(1) == class_id:\n'
                                '            total = replace_word(total, u16(low16(total) + '
                                'actor.word(14)))\n'
                                '    actor = actor.advance(16)\n'
                                'frame = replace(frame, video_command=total, '
                                'foreground=replace_word(count, 65535))\n'
                                'return (_with_scene_views(state, frame, actor=actor), '
                                'actor)'},
 'draw_battle_summary_numbers': {'signature': 'state: SceneState, frame: PhaseFrame',
                                 'returns': 'PhaseFrame',
                                 'flow': 'checked_phase(frame, state)\n'
                                         "for field, address in (('8176', 50592), ('8186', "
                                         "50976), ('8276', 50610), ('8286', 50994), ('8100', "
                                         "51360), ('8102', 51378)):\n"
                                         '    frame = _number_panel(state, frame, '
                                         '_word(state, field), address, 2, 3)\n'
                                         'frame, _ = _sum_active_roster(state, frame, '
                                         "_port(state, '817a'))\n"
                                         'frame = _number_panel(state, frame, '
                                         'frame.video_command, 51740, 4, 1)\n'
                                         'frame, _ = _sum_active_roster(state, frame, '
                                         "_port(state, '827a'))\n"
                                         'return _number_panel(state, frame, '
                                         'frame.video_command, 51758, 4, 1)'},
 'selected_action_mode_view': {'signature': 'state: SceneState',
                               'returns': 'Table',
                               'flow': 'checked_state(state)\n'
                                       "return _port(state, '8132' if _word(state, '8144') == "
                                       "0 else '812a')"},
 'lookup_action_mode_icon_pair': {'signature': 'state: SceneState, context: ActionIconContext',
                                  'returns': 'PhaseFrame',
                                  'flow': 'checked_context(context, ActionIconContext, '
                                          'state)\n'
                                          'frame = context.frame\n'
                                          'mode = replace_word(context.mode, '
                                          'u16(low16(context.mode) << 2))\n'
                                          'first = state.table_at(261316).word(low16(mode))\n'
                                          'second = state.table_at(261318).word(low16(mode))\n'
                                          'return replace(frame, '
                                          'video_command=replace_word(frame.video_command, '
                                          'first), foreground=replace_word(frame.foreground, '
                                          'second), mode=mode)'},
 '_icon_address': {'signature': 'state, frame, address_field, offset',
                   'returns': None,
                   'flow': 'from .services import set_vram_write_address\n'
                           'address = u16(_word(state, address_field) + offset)\n'
                           'frame = replace(frame, '
                           'video_command=replace_word(frame.video_command, address))\n'
                           'command = set_vram_write_address(state, frame.video_command)\n'
                           'return replace(frame, video_command=command)'},
 '_icon_word': {'signature': 'state, frame, mode_offset, bottom, blank',
                'returns': None,
                'flow': 'if blank:\n'
                        '    glyph = 50248\n'
                        'else:\n'
                        '    modes = selected_action_mode_view(state)\n'
                        '    mode = replace_word(frame.mode, modes.word(mode_offset))\n'
                        '    frame = lookup_action_mode_icon_pair(state, '
                        'ActionIconContext(mode, frame))\n'
                        '    glyph = low16(frame.foreground if bottom else '
                        'frame.video_command)\n'
                        'state.mmio_write(12582912, 2, glyph)\n'
                        'return frame'},
 '_icon_pair': {'signature': 'state, frame, address_field, offset, selected_index, '
                             'mode_offset',
                'returns': None,
                'flow': 'frame = _icon_address(state, frame, address_field, offset)\n'
                        "blank = _word(state, '8146') == selected_index and (not "
                        "_input_bit(state, 'f321', 4))\n"
                        'frame = _icon_word(state, frame, mode_offset, False, blank)\n'
                        'frame = _icon_address(state, frame, address_field, offset + 128)\n'
                        'return _icon_word(state, frame, mode_offset, True, blank)'},
 'draw_normal_force_status_panel': {'signature': 'state: SceneState, context: '
                                                 'ForcePanelContext',
                                    'returns': 'PhaseFrame',
                                    'flow': 'checked_context(context, ForcePanelContext, '
                                            'state)\n'
                                            'frame = _with_scene_views(state, context.frame, '
                                            'actor=context.leader)\n'
                                            'frame = _number_panel(state, frame, '
                                            "context.leader.word(14), '8010', 2, 3)\n"
                                            'for class_id, destination, count, digit in ((2, '
                                            "'8012', 3, 2), (1, '8014', 3, 2), (0, '8016', 4, "
                                            '1)):\n'
                                            '    roster = state.table_at(_port(state, '
                                            "'801c').long())\n"
                                            '    frame, _ = _sum_active_roster(state, frame, '
                                            'roster, class_id)\n'
                                            '    frame = _number_panel(state, frame, '
                                            'frame.video_command, destination, count, digit)\n'
                                            "if _word(state, '8144') != 0:\n"
                                            "    if _word(state, '801a') == 0:\n"
                                            '        return frame\n'
                                            "elif _word(state, '801a') != 0:\n"
                                            '    return frame\n'
                                            'state.mmio_write(12582916, 2, 36610)\n'
                                            'for selected_index, position_offset, mode_offset '
                                            'in ((0, 0, 6), (1, 16, 4), (2, 32, 2), (3, 50, '
                                            '0)):\n'
                                            "    frame = _icon_pair(state, frame, '8018', "
                                            'position_offset, selected_index, mode_offset)\n'
                                            'return frame'},
 'draw_special_force_status_panel': {'signature': 'state: SceneState, context: '
                                                  'ForcePanelContext',
                                     'returns': 'PhaseFrame',
                                     'flow': 'checked_context(context, ForcePanelContext, '
                                             'state)\n'
                                             'frame = _with_scene_views(state, context.frame, '
                                             'actor=context.leader)\n'
                                             'frame = _number_panel(state, frame, '
                                             "context.leader.word(14), '8010', 2, 3)\n"
                                             'frame, _ = _sum_active_roster(state, frame, '
                                             'context.leader.advance(16), 1)\n'
                                             'frame = _number_panel(state, frame, '
                                             "frame.video_command, '8012', 4, 1)\n"
                                             "if _word(state, '8144') != 0:\n"
                                             "    if _word(state, '8018') == 0:\n"
                                             '        return frame\n'
                                             "elif _word(state, '8018') != 0:\n"
                                             '    return frame\n'
                                             'state.mmio_write(12582916, 2, 36610)\n'
                                             "frame = _icon_pair(state, frame, '8014', 0, 0, "
                                             '6)\n'
                                             "return _icon_pair(state, frame, '8016', 0, 2, "
                                             '2)'},
 '_panel_configuration': {'signature': 'state, destinations, icon_address, side, roster=None',
                          'returns': None,
                          'flow': "for field, value in zip(('8010', '8012', '8014', '8016'), "
                                  'destinations):\n'
                                  '    _put(state, field, value)\n'
                                  "_put(state, '8018', icon_address)\n"
                                  'if roster is not None:\n'
                                  "    _put(state, '801a', side)\n"
                                  "    _port(state, '801c').set_long(0, roster)"},
 'draw_both_force_status_panels': {'signature': 'state: SceneState, frame: PhaseFrame',
                                   'returns': 'PhaseFrame',
                                   'flow': 'checked_phase(frame, state)\n'
                                           "if _byte(state, '80db') != 3:\n"
                                           '    _panel_configuration(state, (50194, 50208, '
                                           '50224, 50240), 50072, 0, 4294935162)\n'
                                           '    frame = draw_normal_force_status_panel(state, '
                                           "ForcePanelContext(_port(state, '826a'), frame))\n"
                                           '    _panel_configuration(state, (49810, 49824, '
                                           '49840, 49856), 49688, 1, 4294934906)\n'
                                           '    return draw_normal_force_status_panel(state, '
                                           "ForcePanelContext(_port(state, '816a'), frame))\n"
                                           '_panel_configuration(state, (50334, 50352, 50212, '
                                           '50234), 0, 0)\n'
                                           'frame = draw_special_force_status_panel(state, '
                                           "ForcePanelContext(_port(state, '826a'), frame))\n"
                                           '_panel_configuration(state, (49950, 49968, 49828, '
                                           '49850), 1, 1)\n'
                                           'return draw_special_force_status_panel(state, '
                                           "ForcePanelContext(_port(state, '816a'), frame))"},
 'dispatch_late_substate': {'signature': 'state: SceneState, frame: PhaseFrame, slot_address: '
                                         'Long',
                            'returns': 'PhaseFrame',
                            'flow': 'checked_phase(frame, state)\n'
                                    'uint(slot_address, 32)\n'
                                    'if frame.live is not None:\n'
                                    '    complete = {256272: '
                                    'adjust_secondary_formation_scene, 256276: '
                                    'confirm_secondary_formation_scene, 256280: '
                                    'update_active_battle_controls, 256284: '
                                    'latch_scene_controller_inputs, 258096: '
                                    'dismiss_action_mode_prompt, 258150: '
                                    'confirm_duel_handoff_prompt, 258154: '
                                    'await_duel_handoff_palette, 258158: '
                                    'finish_duel_handoff_phase, 258542: '
                                    'confirm_result_prompt, 258546: await_result_palette, '
                                    '258550: finish_result_phase, 258720: '
                                    'confirm_secondary_result_prompt, 258724: '
                                    'await_secondary_result_palette, 258728: '
                                    'finish_secondary_result_phase, 258902: '
                                    'confirm_primary_result_prompt, 258906: '
                                    'await_primary_result_palette, 258910: '
                                    'finish_primary_result_phase}\n'
                                    '    handler = complete.get(slot_address)\n'
                                    '    if handler is not None:\n'
                                    '        return handler(state, frame)\n'
                                    '    result = state.service_at(slot_address, '
                                    'phase_controller_return(state, frame))\n'
                                    '    if type(result) is SceneControllerOutcome:\n'
                                    '        return result.validate(state)\n'
                                    '    if type(result) is not SceneControllerFrame:\n'
                                    "        raise Boundary('phase tail requires actual "
                                    "complete frame or consumed continuation')\n"
                                    '    return phase_from_controller(state, '
                                    'result.validate(state))\n'
                                    'handlers = {257926: begin_transition_prompt, 257930: '
                                    'update_action_mode_prompt, 258096: '
                                    'dismiss_action_mode_prompt, 258146: '
                                    'begin_duel_handoff_prompt, 258150: '
                                    'confirm_duel_handoff_prompt, 258154: '
                                    'await_duel_handoff_palette, 258158: '
                                    'finish_duel_handoff_phase, 258538: '
                                    'begin_result_confirmation_prompt, 258542: '
                                    'confirm_result_prompt, 258546: await_result_palette, '
                                    '258550: finish_result_phase, 258716: '
                                    'begin_secondary_confirmation_prompt, 258720: '
                                    'confirm_secondary_result_prompt, 258724: '
                                    'await_secondary_result_palette, 258728: '
                                    'finish_secondary_result_phase, 258894: '
                                    'begin_primary_confirmation_prompt, 258898: '
                                    'replace_primary_confirmation_prompt, 258902: '
                                    'confirm_primary_result_prompt, 258906: '
                                    'await_primary_result_palette, 258910: '
                                    'finish_primary_result_phase}\n'
                                    'handler = handlers.get(slot_address)\n'
                                    'if handler is not None:\n'
                                    '    return handler(state, frame)\n'
                                    'result = state.service_at(slot_address, '
                                    'LatePhaseDispatch(slot_address, frame))\n'
                                    'return checked_phase(result, state)'},
 '_upload_officer_label': {'signature': 'state, frame, officer_field, vdp_opponent',
                           'returns': None,
                           'flow': 'from .business_actions import upload_object_officer_name\n'
                                   'from .contexts_actions import DuelGlyphContext\n'
                                   'officer = replace_word(frame.glyph_tokens, _word(state, '
                                   'officer_field))\n'
                                   'background = replace_word(frame.video_command, 3)\n'
                                   'foreground = replace_word(frame.foreground, 1)\n'
                                   'result = upload_object_officer_name(state, officer, '
                                   'DuelGlyphContext(background, foreground, '
                                   'frame.row_count))\n'
                                   'result.validate(state)\n'
                                   'frame = replace(frame, video_command=result.tile_counter, '
                                   'foreground=result.glyphs.foreground, '
                                   'row_count=result.glyphs.remaining, '
                                   'glyph_tokens=result.officer_offset)\n'
                                   'return _with_scene_views(state, frame, '
                                   'actor=state.table_at(12582912), opponent=vdp_opponent)'},
 '_update_action_ai': {'signature': 'state, frame',
                       'returns': None,
                       'flow': 'from .business_actions import update_object_action_ai\n'
                               'from .services import SceneRenderFrame\n'
                               'if frame.actors is None:\n'
                               "    raise Boundary('actual battle AI path requires inherited "
                               "live actor/opponent views')\n"
                               'inherited = SceneRenderFrame(frame.video_command, '
                               'frame.foreground, frame.mode, frame.row_count, frame.tile)\n'
                               'result = update_object_action_ai(state, frame.actors.actor, '
                               'frame.actors.opponent, inherited)\n'
                               'result.validate(state)\n'
                               'return replace(frame, video_command=result.frame.x, '
                               'foreground=result.frame.y, mode=result.frame.attributes, '
                               'row_count=result.frame.palette, tile=result.frame.tile, '
                               'actors=BattleActors(result.actor, result.opponent))'},
 'update_active_battle_controls': {'signature': 'state: SceneState, frame: PhaseFrame',
                                   'returns': 'PhaseFrame',
                                   'flow': 'checked_phase(frame, state)\n'
                                           'from .business_early_phase import '
                                           'adjust_scene_scroll\n'
                                           'from .services import enqueue_sound_command\n'
                                           'if frame.live is not None:\n'
                                           '    called = phase_enter_call(state, frame.live, '
                                           '257296)\n'
                                           '    frame = adjust_scene_scroll(state, '
                                           'phase_from_controller(state, called))\n'
                                           '    live = phase_controller_return(state, frame)\n'
                                           '    frame = phase_from_controller(state, '
                                           'phase_finish_call(state, live, 257296))\n'
                                           'else:\n'
                                           '    frame = adjust_scene_scroll(state, frame)\n'
                                           'value = replace_byte(frame.video_command, '
                                           "_byte(state, '811f'))\n"
                                           'value = replace_byte(value, low8(value) & 32)\n'
                                           'open_action_panel = bool(low8(value))\n'
                                           'frame = phase_operands(frame, '
                                           'phase_logic(low8(value), 8), '
                                           'video_command=value)\n'
                                           'if open_action_panel:\n'
                                           "    _put(state, '8144', 0)\n"
                                           "    _put(state, '8116', 1)\n"
                                           "elif _byte(state, '80da') != 0:\n"
                                           '    value = replace_byte(frame.video_command, '
                                           "_byte(state, '8121'))\n"
                                           '    value = replace_byte(value, low8(value) & '
                                           '32)\n'
                                           '    frame = phase_operands(frame, '
                                           'phase_logic(low8(value), 8), '
                                           'video_command=value)\n'
                                           '    if low8(value):\n'
                                           '        open_action_panel = True\n'
                                           "        _put(state, '8144', 1)\n"
                                           "        _put(state, '8116', 0)\n"
                                           'if open_action_panel:\n'
                                           '    value = replace_word(frame.video_command, '
                                           '173)\n'
                                           '    frame = phase_operands(frame, '
                                           'phase_logic(low16(value)), video_command=value)\n'
                                           '    if frame.live is not None:\n'
                                           "        raise Boundary('3ED4A real808A sound call "
                                           "has no complete controller return')\n"
                                           '    enqueue_sound_command(state, low8(value))\n'
                                           '    frame = replace(frame, video_command=value)\n'
                                           '    state.set_status_word(9984)\n'
                                           '    _blank_video_words(state, 1342177282, 191)\n'
                                           '    vdp_opponent = state.table_at(12582912)\n'
                                           '    frame = _with_scene_views(state, frame, '
                                           'opponent=vdp_opponent)\n'
                                           '    frame = replace(frame, '
                                           'glyph_tokens=replace_word(frame.glyph_tokens, '
                                           '65535))\n'
                                           '    state.mmio_write(12582916, 4, 1342177282)\n'
                                           '    frame = _upload_officer_label(state, frame, '
                                           "'80e0', vdp_opponent)\n"
                                           '    state.mmio_write(12582916, 4, 1367343106)\n'
                                           '    frame = _upload_officer_label(state, frame, '
                                           "'80e2', vdp_opponent)\n"
                                           "    if _byte(state, '80db') == 3:\n"
                                           '        frame = _decode_plane(state, frame, '
                                           '283291, 49152, 32)\n'
                                           '    else:\n'
                                           '        frame = _decode_plane(state, frame, '
                                           '282919, 49152, 32)\n'
                                           '        frame = _decode_plane(state, frame, '
                                           '283206, 49216, 32)\n'
                                           '    frame = draw_both_force_status_panels(state, '
                                           'frame)\n'
                                           '    state.set_status_word(9472)\n'
                                           "    _put(state, '813a', 1)\n"
                                           "    _put(state, '813c', 0)\n"
                                           "    _put(state, '813e', 1)\n"
                                           "    _put(state, '8148', _word(state, '8138'))\n"
                                           "    _put(state, '8146', 0)\n"
                                           "    if _word(state, '8148') == 6:\n"
                                           "        _put(state, '8146', 1)\n"
                                           '    return frame\n'
                                           'value = replace_byte(frame.video_command, '
                                           "_byte(state, '811d'))\n"
                                           'value = replace_byte(value, low8(value) & 64)\n'
                                           'frame = phase_operands(frame, '
                                           'phase_logic(low8(value), 8), '
                                           'video_command=value)\n'
                                           'if low8(value):\n'
                                           '    value = replace_word(frame.video_command, '
                                           '173)\n'
                                           '    frame = phase_operands(frame, '
                                           'phase_logic(low16(value)), video_command=value)\n'
                                           '    if frame.live is not None:\n'
                                           "        raise Boundary('3EE5C real808A sound call "
                                           "has no complete controller return')\n"
                                           '    enqueue_sound_command(state, low8(value))\n'
                                           '    frame = replace(frame, video_command=value)\n'
                                           '    state.set_status_word(9984)\n'
                                           '    _blank_video_words(state, 1342177282, 767)\n'
                                           '    vdp_opponent = state.table_at(12582912)\n'
                                           '    frame = _with_scene_views(state, frame, '
                                           'opponent=vdp_opponent)\n'
                                           '    frame = replace(frame, '
                                           'glyph_tokens=replace_word(frame.glyph_tokens, '
                                           '65535))\n'
                                           '    state.mmio_write(12582916, 4, 1342177282)\n'
                                           "    for officer_field in ('80dc', '80de', '80e0', "
                                           "'80e2'):\n"
                                           '        frame = _upload_officer_label(state, '
                                           'frame, officer_field, vdp_opponent)\n'
                                           '    frame = _decode_plane(state, frame, 281196, '
                                           '49152, 32)\n'
                                           "    _put(state, '813a', 2)\n"
                                           "    _put(state, '813c', 0)\n"
                                           "    _put(state, '813e', 1)\n"
                                           '    frame = draw_battle_summary_numbers(state, '
                                           'frame)\n'
                                           '    state.set_status_word(9472)\n'
                                           '    return frame\n'
                                           "if _word(state, '814c') == 0:\n"
                                           "    _put(state, '814c', 1)\n"
                                           "    _increment(state, '8160')\n"
                                           '    if frame.live is not None:\n'
                                           "        raise Boundary('3EF1A real41BAC action-AI "
                                           'call requires complete actor/presentation '
                                           "return')\n"
                                           '    frame = _update_action_ai(state, frame)\n'
                                           "primary_mode = _word(state, '8130')\n"
                                           'frame = phase_operands(frame, '
                                           'phase_compare(primary_mode, 6))\n'
                                           'if primary_mode == 6:\n'
                                           "    position = _word(state, '816c')\n"
                                           '    frame = phase_operands(frame, '
                                           'phase_compare(position, 0))\n'
                                           '    if position == 0:\n'
                                           "        _put(state, '813a', 5)\n"
                                           "        _put(state, '813c', 0)\n"
                                           "        _put(state, '8114', 4)\n"
                                           "        _put(state, '8116', 0)\n"
                                           '        return phase_operands(frame, '
                                           'phase_logic(0))\n'
                                           "secondary_mode = _word(state, '8138')\n"
                                           'frame = phase_operands(frame, '
                                           'phase_compare(secondary_mode, 6))\n'
                                           'if secondary_mode == 6:\n'
                                           "    position = _word(state, '826c')\n"
                                           '    frame = phase_operands(frame, '
                                           'phase_compare(position, 352))\n'
                                           '    if position >= 352:\n'
                                           "        _put(state, '813a', 5)\n"
                                           "        _put(state, '813c', 0)\n"
                                           "        _put(state, '8114', 5)\n"
                                           "        _put(state, '8116', 1)\n"
                                           '        return phase_operands(frame, '
                                           'phase_logic(1))\n'
                                           'return frame'}}

def _lower_adjust_secondary_formation_scene(emitter,rules):
    emitter.segment(0x3e910,0x3e918)
    emitter.ins('bra.w','scene_pc_03ecdc',4)
    emitter.ins('bra.w','scene_pc_03ecdc',4)
    emitter.segment(0x3ecdc,0x3ed0c)
    emitter.ins('bsr.w','scene_pc_03f61c',4)
    emitter.ins('move.b','0x811f:w,%d0',4)
    emitter.ins('andi.w','#0xc,%d0',4)
    emitter.ins('beq.b','scene_pc_03ecf0',2)
    emitter.ins('bsr.w','scene_pc_04031c',4)
    emitter.ins('rts','',2)
    emitter.ins('btst.b','#0x5,0x811f:w',6)
    emitter.ins('beq.b','scene_pc_03ed0a',2)
    emitter.ins('move.w','#0x8,0x813a:w',6)
    emitter.ins('clr.w','0x813c:w',4)
    emitter.ins('clr.w','0x814c:w',4)
    emitter.ins('bsr.w','scene_pc_04031c',4)
    emitter.ins('rts','',2)

def _lower_update_active_battle_controls(emitter,rules):
    emitter.segment(0x3e918,0x3e91c)
    emitter.ins('bra.w','scene_pc_03ed0c',4)
    emitter.segment(0x3ed0c,0x3ef78)
    emitter.ins('jsr','-5022(%pc)',4)
    emitter.ins('move.b','0x811f:w,%d0',4)
    emitter.ins('andi.b','#0x20,%d0',4)
    emitter.ins('bne.b','scene_pc_03ed3c',2)
    emitter.ins('tst.b','0x80da:w',4)
    emitter.ins('beq.w','scene_pc_03ee4c',4)
    emitter.ins('move.b','0x8121:w,%d0',4)
    emitter.ins('andi.b','#0x20,%d0',4)
    emitter.ins('beq.w','scene_pc_03ee4c',4)
    emitter.ins('move.w','#0x1,0x8144:w',6)
    emitter.ins('clr.w','0x8116:w',4)
    emitter.ins('bra.w','scene_pc_03ed46',4)
    emitter.ins('clr.w','0x8144:w',4)
    emitter.ins('move.w','#0x1,0x8116:w',6)
    emitter.ins('move.w','#0xad,%d0',4)
    emitter.ins('jsr','scene_pc_00808a:l',6)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.l','#0x50000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xbf,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03ed6c',4)
    emitter.ins('move.l','#0x50000002,0xc00004:l',10)
    emitter.ins('move.w','0x80e0:w,%d7',4)
    emitter.ins('move.w','#0x3,%d0',4)
    emitter.ins('move.w','#0x1,%d1',4)
    emitter.ins('bsr.w','scene_pc_0402c2',4)
    emitter.ins('move.l','#0x51800002,0xc00004:l',10)
    emitter.ins('move.w','0x80e2:w,%d7',4)
    emitter.ins('move.w','#0x3,%d0',4)
    emitter.ins('move.w','#0x1,%d1',4)
    emitter.ins('bsr.w','scene_pc_0402c2',4)
    emitter.ins('cmpi.b','#0x3,0x80db:w',6)
    emitter.ins('bne.b','scene_pc_03edd6',2)
    emitter.ins('lea.l','0x4529b:l,%a0',6)
    emitter.ins('lea.l','0xc000:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('move.w','#0x8000,0x8000:w',6)
    emitter.ins('move.w','#0x20,%d6',4)
    emitter.ins('jsr','-17142(%pc)',4)
    emitter.ins('bsr.w','scene_pc_03f9c6',4)
    emitter.ins('bra.w','scene_pc_03ee1a',4)
    emitter.ins('lea.l','0x45127:l,%a0',6)
    emitter.ins('lea.l','0xc000:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('move.w','#0x8000,0x8000:w',6)
    emitter.ins('move.w','#0x20,%d6',4)
    emitter.ins('jsr','-17182(%pc)',4)
    emitter.ins('lea.l','0x45246:l,%a0',6)
    emitter.ins('lea.l','0xc040:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('move.w','#0x8000,0x8000:w',6)
    emitter.ins('move.w','#0x20,%d6',4)
    emitter.ins('jsr','-17214(%pc)',4)
    emitter.ins('bsr.w','scene_pc_03f9c6',4)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('move.w','#0x1,0x813a:w',6)
    emitter.ins('move.w','#0x0,0x813c:w',6)
    emitter.ins('move.w','#0x1,0x813e:w',6)
    emitter.ins('move.w','0x8138:w,0x8148:w',6)
    emitter.ins('clr.w','0x8146:w',4)
    emitter.ins('cmpi.w','#0x6,0x8148:w',6)
    emitter.ins('bne.w','scene_pc_03ee4a',4)
    emitter.ins('move.w','#0x1,0x8146:w',6)
    emitter.ins('rts','',2)
    emitter.ins('move.b','0x811d:w,%d0',4)
    emitter.ins('andi.b','#0x40,%d0',4)
    emitter.ins('beq.w','scene_pc_03ef0a',4)
    emitter.ins('move.w','#0xad,%d0',4)
    emitter.ins('jsr','scene_pc_00808a:l',6)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.l','#0x50000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0x2ff,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03ee7e',4)
    emitter.ins('move.l','#0x50000002,0xc00004:l',10)
    emitter.ins('move.w','0x80dc:w,%d7',4)
    emitter.ins('move.w','#0x3,%d0',4)
    emitter.ins('move.w','#0x1,%d1',4)
    emitter.ins('bsr.w','scene_pc_0402c2',4)
    emitter.ins('move.w','0x80de:w,%d7',4)
    emitter.ins('move.w','#0x3,%d0',4)
    emitter.ins('move.w','#0x1,%d1',4)
    emitter.ins('bsr.w','scene_pc_0402c2',4)
    emitter.ins('move.w','0x80e0:w,%d7',4)
    emitter.ins('move.w','#0x3,%d0',4)
    emitter.ins('move.w','#0x1,%d1',4)
    emitter.ins('bsr.w','scene_pc_0402c2',4)
    emitter.ins('move.w','0x80e2:w,%d7',4)
    emitter.ins('move.w','#0x3,%d0',4)
    emitter.ins('move.w','#0x1,%d1',4)
    emitter.ins('bsr.w','scene_pc_0402c2',4)
    emitter.ins('lea.l','0x44a6c:l,%a0',6)
    emitter.ins('lea.l','0xc000:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('move.w','#0x8000,0x8000:w',6)
    emitter.ins('move.w','#0x20,%d6',4)
    emitter.ins('jsr','-17430(%pc)',4)
    emitter.ins('move.w','#0x2,0x813a:w',6)
    emitter.ins('move.w','#0x0,0x813c:w',6)
    emitter.ins('move.w','#0x1,0x813e:w',6)
    emitter.ins('bsr.w','scene_pc_03fe5e',4)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('rts','',2)
    emitter.ins('tst.w','0x814c:w',4)
    emitter.ins('bne.b','scene_pc_03ef1e',2)
    emitter.ins('move.w','#0x1,0x814c:w',6)
    emitter.ins('addq.w','#0x1,0x8160:w',4)
    emitter.ins('bsr.w','scene_pc_041bac',4)
    emitter.ins('cmpi.w','#0x6,0x8130:w',6)
    emitter.ins('bne.b','scene_pc_03ef4a',2)
    emitter.ins('cmpi.w','#0x0,0x816c:w',6)
    emitter.ins('bhi.w','scene_pc_03ef4a',4)
    emitter.ins('move.w','#0x5,0x813a:w',6)
    emitter.ins('move.w','#0x0,0x813c:w',6)
    emitter.ins('move.w','#0x4,0x8114:w',6)
    emitter.ins('move.w','#0x0,0x8116:w',6)
    emitter.ins('rts','',2)
    emitter.ins('cmpi.w','#0x6,0x8138:w',6)
    emitter.ins('bne.b','scene_pc_03ef76',2)
    emitter.ins('cmpi.w','#0x160,0x826c:w',6)
    emitter.ins('bcs.w','scene_pc_03ef76',4)
    emitter.ins('move.w','#0x5,0x813a:w',6)
    emitter.ins('move.w','#0x0,0x813c:w',6)
    emitter.ins('move.w','#0x5,0x8114:w',6)
    emitter.ins('move.w','#0x1,0x8116:w',6)
    emitter.ins('rts','',2)
    emitter.ins('rts','',2)

def _lower_latch_scene_controller_inputs(emitter,rules):
    emitter.segment(0x3e91c,0x3e98a)
    emitter.ins('tst.b','0x80da:w',4)
    emitter.ins('bne.b','scene_pc_03e934',2)
    emitter.ins('move.w','0xf602:w,0x811c:w',6)
    emitter.ins('move.w','0xf602:w,0x811e:w',6)
    emitter.ins('clr.w','0x8120:w',4)
    emitter.ins('rts','',2)
    emitter.ins('cmpi.b','#0x1,0x80da:w',6)
    emitter.ins('bne.b','scene_pc_03e956',2)
    emitter.ins('move.w','0xf602:w,%d0',4)
    emitter.ins('or.w','0xf604:w,%d0',4)
    emitter.ins('move.w','%d0,0x811c:w',4)
    emitter.ins('move.w','0xf602:w,0x811e:w',6)
    emitter.ins('move.w','0xf604:w,0x8120:w',6)
    emitter.ins('rts','',2)
    emitter.ins('cmpi.b','#0x2,0x80da:w',6)
    emitter.ins('bne.b','scene_pc_03e978',2)
    emitter.ins('move.w','0xf602:w,%d0',4)
    emitter.ins('or.w','0xf604:w,%d0',4)
    emitter.ins('move.w','%d0,0x811c:w',4)
    emitter.ins('move.w','0xf604:w,0x811e:w',6)
    emitter.ins('move.w','0xf602:w,0x8120:w',6)
    emitter.ins('rts','',2)
    emitter.ins('move.w','0xf604:w,0x811c:w',6)
    emitter.ins('move.w','0xf604:w,0x811e:w',6)
    emitter.ins('clr.w','0x8120:w',4)
    emitter.ins('rts','',2)

def _lower_draw_two_prompt_backgrounds(emitter,rules):
    emitter.segment(0x3eae2,0x3eb24)
    emitter.ins('lea.l','0x44ef5:l,%a0',6)
    emitter.ins('lea.l','0xc980:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('move.w','#0x8000,0x8000:w',6)
    emitter.ins('move.w','#0xa,%d6',4)
    emitter.ins('jsr','-16426(%pc)',4)
    emitter.ins('lea.l','0x45098:l,%a0',6)
    emitter.ins('lea.l','0xc9c0:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('move.w','#0x8000,0x8000:w',6)
    emitter.ins('move.w','#0xa,%d6',4)
    emitter.ins('jsr','-16458(%pc)',4)
    emitter.ins('rts','',2)

def _lower_update_secondary_scene_totals(emitter,rules):
    emitter.segment(0x3ecc8,0x3ecdc)
    emitter.ins('move.w','0x8106:w,%d0',4)
    emitter.ins('add.w','0x810a:w,%d0',4)
    emitter.ins('move.w','%d0,0x8276:w',4)
    emitter.ins('move.w','0x810e:w,0x8278:w',6)
    emitter.ins('rts','',2)

def _lower_begin_transition_prompt(emitter,rules):
    emitter.segment(0x3ef86,0x3ef8a)
    emitter.ins('bra.w','scene_pc_03ef8e',4)
    emitter.segment(0x3ef8e,0x3efe8)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03efb2',4)
    emitter.ins('move.w','#0xa000,0xff700c:l',8)
    emitter.ins('move.l','#0x3b36c,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('bsr.w','scene_pc_03eae2',4)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('rts','',2)

def _lower_update_action_mode_prompt(emitter,rules):
    emitter.segment(0x3ef8a,0x3ef8e)
    emitter.ins('bra.w','scene_pc_03efe8',4)
    emitter.segment(0x3efe8,0x3f022)
    emitter.ins('move.w','0x811e:w,%d0',4)
    emitter.ins('tst.w','0x8144:w',4)
    emitter.ins('beq.b','scene_pc_03eff6',2)
    emitter.ins('move.w','0x8120:w,%d0',4)
    emitter.ins('move.w','%d0,0x8122:w',4)
    emitter.ins('bsr.w','scene_pc_03f760',4)
    emitter.ins('bsr.w','scene_pc_03f9c6',4)
    emitter.ins('move.w','0x8122:w,%d0',4)
    emitter.ins('andi.b','#0xf0,%d0',4)
    emitter.ins('beq.b','scene_pc_03f020',2)
    emitter.ins('bsr.w','scene_pc_04031c',4)
    emitter.ins('move.w','#0x0,0x813a:w',6)
    emitter.ins('move.w','#0x6,0x813c:w',6)
    emitter.ins('clr.w','0x813e:w',4)
    emitter.ins('rts','',2)

def _lower_dismiss_action_mode_prompt(emitter,rules):
    emitter.segment(0x3f030,0x3f054)
    emitter.ins('bra.w','scene_pc_03f034',4)
    emitter.ins('move.b','0x811d:w,%d0',4)
    emitter.ins('andi.b','#0xf0,%d0',4)
    emitter.ins('beq.b','scene_pc_03f052',2)
    emitter.ins('bsr.w','scene_pc_04031c',4)
    emitter.ins('move.w','#0x0,0x813a:w',6)
    emitter.ins('move.w','#0x6,0x813c:w',6)
    emitter.ins('clr.w','0x813e:w',4)
    emitter.ins('rts','',2)

def _lower_begin_duel_handoff_prompt(emitter,rules):
    emitter.segment(0x3f062,0x3f066)
    emitter.ins('bra.w','scene_pc_03f072',4)
    emitter.segment(0x3f072,0x3f0d2)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03f096',4)
    emitter.ins('move.w','#0xa000,0xff700c:l',8)
    emitter.ins('move.l','#0x3b45e,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('bsr.w','scene_pc_03eae2',4)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('move.w','#0x1,0x813e:w',6)
    emitter.ins('rts','',2)

def _lower_confirm_duel_handoff_prompt(emitter,rules):
    emitter.segment(0x3f066,0x3f06a)
    emitter.ins('bra.w','scene_pc_03f0d2',4)
    emitter.segment(0x3f0d2,0x3f16a)
    emitter.ins('move.b','0x811d:w,%d0',4)
    emitter.ins('andi.b','#0xf0,%d0',4)
    emitter.ins('beq.w','scene_pc_03f1c2',4)
    emitter.ins('bsr.w','scene_pc_03f8dc',4)
    emitter.ins('move.w','#0xffff,0x80ca:w',6)
    emitter.ins('move.w','#0xffff,0x80cc:w',6)
    emitter.ins('move.w','#0xffff,0x80ce:w',6)
    emitter.ins('move.w','#0xffff,0x80d0:w',6)
    emitter.ins('moveq','#1,%d0',2)
    emitter.ins('jsr','-18118(%pc)',4)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('clr.w','0xff70f2:l',6)
    emitter.ins('move.b','0x80db:w,0xff70f3:l',8)
    emitter.ins('tst.w','0x8124:w',4)
    emitter.ins('bne.b','scene_pc_03f172',2)
    emitter.ins('move.w','0x80dc:w,0xff7070:l',8)
    emitter.ins('move.w','0x80e0:w,0xff706a:l',8)
    emitter.ins('move.w','0x8178:w,0xff706c:l',8)
    emitter.ins('move.w','0x8104:w,0xff706e:l',8)
    emitter.ins('move.w','0x80de:w,0xff70c0:l',8)
    emitter.ins('move.w','0x80e2:w,0xff70ba:l',8)
    emitter.ins('move.w','0x8278:w,0xff70bc:l',8)
    emitter.ins('move.w','0x8106:w,0xff70be:l',8)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.b','0x80da:w,%d0',4)
    emitter.ins('asl.w','#0x1,%d0',2)
    emitter.ins('move.w','8(%pc, %d0.w),0xff700a:l',8)
    emitter.ins('rts','',2)
    emitter.segment(0x3f172,0x3f1c4)
    emitter.ins('move.w','0x80de:w,0xff7070:l',8)
    emitter.ins('move.w','0x80e2:w,0xff706a:l',8)
    emitter.ins('move.w','0x8278:w,0xff706c:l',8)
    emitter.ins('move.w','0x8106:w,0xff706e:l',8)
    emitter.ins('move.w','0x80dc:w,0xff70c0:l',8)
    emitter.ins('move.w','0x80e0:w,0xff70ba:l',8)
    emitter.ins('move.w','0x8178:w,0xff70bc:l',8)
    emitter.ins('move.w','0x8104:w,0xff70be:l',8)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.b','0x80da:w,%d0',4)
    emitter.ins('asl.w','#0x1,%d0',2)
    emitter.ins('move.w','8(%pc, %d0.w),0xff700a:l',8)
    emitter.ins('rts','',2)

def _lower_await_duel_handoff_palette(emitter,rules):
    emitter.segment(0x3f06a,0x3f072)
    emitter.ins('bra.w','scene_pc_03f1cc',4)
    emitter.ins('bra.w','scene_pc_03f1da',4)
    emitter.segment(0x3f1cc,0x3f1dc)
    emitter.ins('btst.b','#0x7,0x80c4:w',6)
    emitter.ins('beq.w','scene_pc_03f1da',4)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('rts','',2)
    emitter.segment(0x3f1f2,0x3f1fa)
    emitter.ins('bra.w','scene_pc_03f1cc',4)
    emitter.ins('bra.w','scene_pc_03f1da',4)
    emitter.segment(0x3f2a4,0x3f2a8)
    emitter.ins('bra.w','scene_pc_03f1cc',4)
    emitter.segment(0x3f35a,0x3f35e)
    emitter.ins('bra.w','scene_pc_03f1cc',4)

def _lower_begin_result_confirmation_prompt(emitter,rules):
    emitter.segment(0x3f1ea,0x3f1ee)
    emitter.ins('bra.w','scene_pc_03f1fa',4)
    emitter.segment(0x3f1fa,0x3f25a)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03f21e',4)
    emitter.ins('move.w','#0xa000,0xff700c:l',8)
    emitter.ins('move.l','#0x3b488,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('bsr.w','scene_pc_03eae2',4)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('move.w','#0x1,0x813e:w',6)
    emitter.ins('rts','',2)

def _lower_confirm_result_prompt(emitter,rules):
    emitter.segment(0x3f1ee,0x3f1f2)
    emitter.ins('bra.w','scene_pc_03f25a',4)
    emitter.segment(0x3f25a,0x3f28e)
    emitter.ins('move.b','0x811d:w,%d0',4)
    emitter.ins('andi.b','#0xf0,%d0',4)
    emitter.ins('beq.w','scene_pc_03f28c',4)
    emitter.ins('bsr.w','scene_pc_03f8dc',4)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('move.w','#0xffff,0x80ca:w',6)
    emitter.ins('move.w','#0xffff,0x80cc:w',6)
    emitter.ins('move.w','#0xffff,0x80ce:w',6)
    emitter.ins('move.w','#0xffff,0x80d0:w',6)
    emitter.ins('moveq','#1,%d0',2)
    emitter.ins('jsr','-18514(%pc)',4)
    emitter.ins('rts','',2)

def _lower_begin_secondary_confirmation_prompt(emitter,rules):
    emitter.segment(0x3f29c,0x3f2a0)
    emitter.ins('bra.w','scene_pc_03f2ac',4)
    emitter.segment(0x3f2ac,0x3f30c)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03f2d0',4)
    emitter.ins('move.w','#0xa000,0xff700c:l',8)
    emitter.ins('move.l','#0x3b47a,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('bsr.w','scene_pc_03eae2',4)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('move.w','#0x1,0x813e:w',6)
    emitter.ins('rts','',2)

def _lower_confirm_secondary_result_prompt(emitter,rules):
    emitter.segment(0x3f2a0,0x3f2a4)
    emitter.ins('bra.w','scene_pc_03f30c',4)
    emitter.segment(0x3f2a8,0x3f2ac)
    emitter.ins('bra.w','scene_pc_03f33e',4)
    emitter.segment(0x3f30c,0x3f340)
    emitter.ins('move.b','0x811d:w,%d0',4)
    emitter.ins('andi.b','#0xf0,%d0',4)
    emitter.ins('beq.w','scene_pc_03f33e',4)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('bsr.w','scene_pc_03f8dc',4)
    emitter.ins('move.w','#0xffff,0x80ca:w',6)
    emitter.ins('move.w','#0xffff,0x80cc:w',6)
    emitter.ins('move.w','#0xffff,0x80ce:w',6)
    emitter.ins('move.w','#0xffff,0x80d0:w',6)
    emitter.ins('moveq','#1,%d0',2)
    emitter.ins('jsr','-18692(%pc)',4)
    emitter.ins('rts','',2)

def _lower_begin_primary_confirmation_prompt(emitter,rules):
    emitter.segment(0x3f34e,0x3f352)
    emitter.ins('bra.w','scene_pc_03f362',4)
    emitter.segment(0x3f362,0x3f3c8)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.w','#0x0,0x8116:w',6)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03f38c',4)
    emitter.ins('move.w','#0xa000,0xff700c:l',8)
    emitter.ins('move.l','#0x3b49e,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('bsr.w','scene_pc_03eae2',4)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('move.w','#0x1,0x813e:w',6)
    emitter.ins('rts','',2)

def _lower_replace_primary_confirmation_prompt(emitter,rules):
    emitter.segment(0x3f352,0x3f356)
    emitter.ins('bra.w','scene_pc_03f3c8',4)
    emitter.segment(0x3f3c8,0x3f42a)
    emitter.ins('move.b','0x811d:w,%d0',4)
    emitter.ins('andi.b','#0x20,%d0',4)
    emitter.ins('beq.w','scene_pc_03f428',4)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03f3f8',4)
    emitter.ins('move.w','#0xa000,0xff700c:l',8)
    emitter.ins('move.l','#0x3b4b6,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('rts','',2)

def _lower_confirm_primary_result_prompt(emitter,rules):
    emitter.segment(0x3f356,0x3f35a)
    emitter.ins('bra.w','scene_pc_03f42a',4)
    emitter.segment(0x3f35e,0x3f362)
    emitter.ins('bra.w','scene_pc_03f45c',4)
    emitter.segment(0x3f42a,0x3f45e)
    emitter.ins('move.b','0x811d:w,%d0',4)
    emitter.ins('andi.b','#0x20,%d0',4)
    emitter.ins('beq.w','scene_pc_03f45c',4)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('bsr.w','scene_pc_03f8dc',4)
    emitter.ins('move.w','#0xffff,0x80ca:w',6)
    emitter.ins('move.w','#0xffff,0x80cc:w',6)
    emitter.ins('move.w','#0xffff,0x80ce:w',6)
    emitter.ins('move.w','#0xffff,0x80d0:w',6)
    emitter.ins('moveq','#1,%d0',2)
    emitter.ins('jsr','-18978(%pc)',4)
    emitter.ins('rts','',2)

def _lower_normalize_secondary_squad_size(emitter,rules):
    emitter.segment(0x3f45e,0x3f4c2)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('moveq','#0,%d1',2)
    emitter.ins('move.w','0x80e6:w,%d0',4)
    emitter.ins('move.w','0x80ea:w,%d1',4)
    emitter.ins('bne.w','scene_pc_03f474',4)
    emitter.ins('addq.w','#0x1,0x80ea:w',4)
    emitter.ins('bra.b','scene_pc_03f45e',2)
    emitter.ins('cmpi.w','#0xf,%d1',4)
    emitter.ins('bls.w','scene_pc_03f482',4)
    emitter.ins('subq.w','#0x1,0x80ea:w',4)
    emitter.ins('bra.b','scene_pc_03f45e',2)
    emitter.ins('divu.w','%d1,%d0',2)
    emitter.ins('cmpi.w','#0x3e8,%d0',4)
    emitter.ins('bls.w','scene_pc_03f492',4)
    emitter.ins('addq.w','#0x1,0x80ea:w',4)
    emitter.ins('bra.b','scene_pc_03f45e',2)
    emitter.ins('cmpi.w','#0x64,%d0',4)
    emitter.ins('bhi.w','scene_pc_03f4a8',4)
    emitter.ins('cmpi.w','#0x1,0x80ea:w',6)
    emitter.ins('beq.b','scene_pc_03f4b4',2)
    emitter.ins('subq.w','#0x1,0x80ea:w',4)
    emitter.ins('bra.b','scene_pc_03f45e',2)
    emitter.ins('move.w','%d0,0x80ee:w',4)
    emitter.ins('swap','%d0',2)
    emitter.ins('move.w','%d0,0x80f2:w',4)
    emitter.ins('rts','',2)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('bne.b','scene_pc_03f4a8',2)
    emitter.ins('clr.w','0x80ee:w',4)
    emitter.ins('clr.w','0x80f2:w',4)
    emitter.ins('rts','',2)

def _lower_adjust_secondary_squad_count(emitter,rules):
    emitter.segment(0x3f518,0x3f532)
    emitter.ins('btst.b','#0x0,0x811f:w',6)
    emitter.ins('beq.b','scene_pc_03f524',2)
    emitter.ins('addq.w','#0x1,0x80ea:w',4)
    emitter.ins('btst.b','#0x1,0x811f:w',6)
    emitter.ins('beq.b','scene_pc_03f530',2)
    emitter.ins('subq.w','#0x1,0x80ea:w',4)
    emitter.ins('rts','',2)

def _lower_adjust_selected_squad_class_counts(emitter,rules):
    emitter.segment(0x3f532,0x3f5f8)
    emitter.ins('btst.b','#0x0,0x811f:w',6)
    emitter.ins('beq.b','scene_pc_03f5b2',2)
    emitter.ins('move.w','0x80fa:w,%d0',4)
    emitter.ins('add.w','0x80fc:w,%d0',4)
    emitter.ins('add.w','0x80fe:w,%d0',4)
    emitter.ins('cmp.w','0x80ea:w,%d0',4)
    emitter.ins('bcc.b','scene_pc_03f5b2',2)
    emitter.ins('move.w','0x8144:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('lea.l','164(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('movea.l','(%a0, %d0.w),%a1',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('cmpi.w','#0x64,0x8112:w',6)
    emitter.ins('bls.b','scene_pc_03f59a',2)
    emitter.ins('moveq','#1,%d0',2)
    emitter.ins('cmpi.w','#0xc8,0x8112:w',6)
    emitter.ins('bls.b','scene_pc_03f59a',2)
    emitter.ins('moveq','#2,%d0',2)
    emitter.ins('cmpi.w','#0x12c,0x8112:w',6)
    emitter.ins('bls.b','scene_pc_03f59a',2)
    emitter.ins('moveq','#3,%d0',2)
    emitter.ins('cmpi.w','#0x190,0x8112:w',6)
    emitter.ins('bls.b','scene_pc_03f59a',2)
    emitter.ins('moveq','#4,%d0',2)
    emitter.ins('cmpi.w','#0x1f4,0x8112:w',6)
    emitter.ins('bls.b','scene_pc_03f59a',2)
    emitter.ins('moveq','#5,%d0',2)
    emitter.ins('cmpi.w','#0x258,0x8112:w',6)
    emitter.ins('bls.b','scene_pc_03f59a',2)
    emitter.ins('moveq','#6,%d0',2)
    emitter.ins('move.w','0x8144:w,%d1',4)
    emitter.ins('asl.w','#0x3,%d1',2)
    emitter.ins('add.w','%d0,%d1',2)
    emitter.ins('move.w','(%a1),%d0',2)
    emitter.ins('lea.l','94(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('cmp.b','(%a0, %d1.w),%d0',4)
    emitter.ins('bcc.b','scene_pc_03f5b2',2)
    emitter.ins('addq.w','#0x1,(%a1)',2)
    emitter.ins('btst.b','#0x1,0x811f:w',6)
    emitter.ins('beq.b','scene_pc_03f5d0',2)
    emitter.ins('move.w','0x8144:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('lea.l','54(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('movea.l','(%a0, %d0.w),%a0',4)
    emitter.ins('tst.w','(%a0)',2)
    emitter.ins('beq.b','scene_pc_03f5d0',2)
    emitter.ins('subq.w','#0x1,(%a0)',2)
    emitter.ins('btst.b','#0x5,0x811f:w',6)
    emitter.ins('beq.b','scene_pc_03f5e4',2)
    emitter.ins('cmpi.w','#0x2,0x8144:w',6)
    emitter.ins('bcc.b','scene_pc_03f5e4',2)
    emitter.ins('addq.w','#0x1,0x8144:w',4)
    emitter.ins('btst.b','#0x4,0x811f:w',6)
    emitter.ins('beq.b','scene_pc_03f5f6',2)
    emitter.ins('tst.w','0x8144:w',4)
    emitter.ins('beq.b','scene_pc_03f5f6',2)
    emitter.ins('subq.w','#0x1,0x8144:w',4)
    emitter.ins('rts','',2)

def _lower_adjust_secondary_formation(emitter,rules):
    emitter.segment(0x3f61c,0x3f6c2)
    emitter.ins('btst.b','#0x2,0x811f:w',6)
    emitter.ins('beq.b','scene_pc_03f634',2)
    emitter.ins('addq.w','#0x1,0x8144:w',4)
    emitter.ins('cmpi.w','#0x5,0x8144:w',6)
    emitter.ins('bcs.b','scene_pc_03f634',2)
    emitter.ins('clr.w','0x8144:w',4)
    emitter.ins('btst.b','#0x3,0x811f:w',6)
    emitter.ins('beq.b','scene_pc_03f648',2)
    emitter.ins('subq.w','#0x1,0x8144:w',4)
    emitter.ins('bpl.b','scene_pc_03f648',2)
    emitter.ins('move.w','#0x4,0x8144:w',6)
    emitter.ins('move.w','0x8144:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('lea.l','9224(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('movea.l','(%a0, %d0.w),%a5',4)
    emitter.ins('move.w','0x80fa:w,%d1',4)
    emitter.ins('move.w','0x80fc:w,%d2',4)
    emitter.ins('move.w','0x80fe:w,%d3',4)
    emitter.ins('moveq','#0,%d4',2)
    emitter.ins('lea.l','0x826a:w,%a6',4)
    emitter.ins('move.w','#0x160,%d0',4)
    emitter.ins('sub.w','(%a5)+,%d0',2)
    emitter.ins('move.w','%d0,0x2(%a6)',4)
    emitter.ins('move.w','(%a5)+,0x4(%a6)',4)
    emitter.ins('move.w','#0x1,0x6(%a6)',6)
    emitter.ins('move.w','#0x1,0x8(%a6)',6)
    emitter.ins('tst.w','%d4',2)
    emitter.ins('bne.b','scene_pc_03f690',2)
    emitter.ins('move.w','#0x8003,(%a6)',4)
    emitter.ins('moveq','#1,%d4',2)
    emitter.ins('bra.b','scene_pc_03f6b2',2)
    emitter.ins('tst.w','%d1',2)
    emitter.ins('beq.b','scene_pc_03f69c',2)
    emitter.ins('move.w','#0x8002,(%a6)',4)
    emitter.ins('subq.w','#0x1,%d1',2)
    emitter.ins('bra.b','scene_pc_03f6b2',2)
    emitter.ins('tst.w','%d2',2)
    emitter.ins('beq.b','scene_pc_03f6a8',2)
    emitter.ins('move.w','#0x8001,(%a6)',4)
    emitter.ins('subq.w','#0x1,%d2',2)
    emitter.ins('bra.b','scene_pc_03f6b2',2)
    emitter.ins('tst.w','%d3',2)
    emitter.ins('beq.b','scene_pc_03f6c0',2)
    emitter.ins('move.w','#0x8000,(%a6)',4)
    emitter.ins('subq.w','#0x1,%d3',2)
    emitter.ins('adda.w','#0x10,%a6',4)
    emitter.ins('cmpa.l','#0xffff836a,%a6',6)
    emitter.ins('bcs.w','scene_pc_03f66a',4)
    emitter.ins('rts','',2)

def _lower_adjust_primary_formation(emitter,rules):
    emitter.segment(0x3f6c2,0x3f760)
    emitter.ins('btst.b','#0x2,0x811f:w',6)
    emitter.ins('beq.b','scene_pc_03f6da',2)
    emitter.ins('addq.w','#0x1,0x8144:w',4)
    emitter.ins('cmpi.w','#0x5,0x8144:w',6)
    emitter.ins('bcs.b','scene_pc_03f6da',2)
    emitter.ins('clr.w','0x8144:w',4)
    emitter.ins('btst.b','#0x3,0x811f:w',6)
    emitter.ins('beq.b','scene_pc_03f6ee',2)
    emitter.ins('subq.w','#0x1,0x8144:w',4)
    emitter.ins('bpl.b','scene_pc_03f6ee',2)
    emitter.ins('move.w','#0x4,0x8144:w',6)
    emitter.ins('move.w','0x8144:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('lea.l','9058(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('movea.l','(%a0, %d0.w),%a5',4)
    emitter.ins('move.w','0x80fa:w,%d1',4)
    emitter.ins('move.w','0x80fc:w,%d2',4)
    emitter.ins('move.w','0x80fe:w,%d3',4)
    emitter.ins('moveq','#0,%d4',2)
    emitter.ins('lea.l','0x816a:w,%a6',4)
    emitter.ins('move.w','(%a5)+,0x2(%a6)',4)
    emitter.ins('move.w','(%a5)+,0x4(%a6)',4)
    emitter.ins('move.w','#0x1,0x6(%a6)',6)
    emitter.ins('move.w','#0x1,0x8(%a6)',6)
    emitter.ins('tst.w','%d4',2)
    emitter.ins('bne.b','scene_pc_03f730',2)
    emitter.ins('move.w','#0x8003,(%a6)',4)
    emitter.ins('moveq','#1,%d4',2)
    emitter.ins('bra.b','scene_pc_03f752',2)
    emitter.ins('tst.w','%d1',2)
    emitter.ins('beq.b','scene_pc_03f73c',2)
    emitter.ins('move.w','#0x8002,(%a6)',4)
    emitter.ins('subq.w','#0x1,%d1',2)
    emitter.ins('bra.b','scene_pc_03f752',2)
    emitter.ins('tst.w','%d2',2)
    emitter.ins('beq.b','scene_pc_03f748',2)
    emitter.ins('move.w','#0x8001,(%a6)',4)
    emitter.ins('subq.w','#0x1,%d2',2)
    emitter.ins('bra.b','scene_pc_03f752',2)
    emitter.ins('tst.w','%d3',2)
    emitter.ins('beq.b','scene_pc_03f75e',2)
    emitter.ins('move.w','#0x8000,(%a6)',4)
    emitter.ins('subq.w','#0x1,%d3',2)
    emitter.ins('adda.w','#0x10,%a6',4)
    emitter.ins('cmpa.l','#0xffff826a,%a6',6)
    emitter.ins('bcs.b','scene_pc_03f710',2)
    emitter.ins('rts','',2)

def _lower_adjust_selected_action_mode(emitter,rules):
    emitter.segment(0x3f760,0x3f840)
    emitter.ins('cmpi.b','#0x3,0x80db:w',6)
    emitter.ins('beq.w','scene_pc_03f844',4)
    emitter.ins('btst.b','#0x0,0x8122:w',6)
    emitter.ins('bne.w','scene_pc_03f7d2',4)
    emitter.ins('btst.b','#0x1,0x8122:w',6)
    emitter.ins('bne.w','scene_pc_03f7d2',4)
    emitter.ins('btst.b','#0x3,0x8123:w',6)
    emitter.ins('beq.b','scene_pc_03f7a6',2)
    emitter.ins('addq.w','#0x1,0x8146:w',4)
    emitter.ins('cmpi.w','#0x4,0x8146:w',6)
    emitter.ins('bcs.b','scene_pc_03f7a6',2)
    emitter.ins('clr.w','0x8146:w',4)
    emitter.ins('cmpi.w','#0x6,0x8148:w',6)
    emitter.ins('bne.w','scene_pc_03f7a6',4)
    emitter.ins('move.w','#0x1,0x8146:w',6)
    emitter.ins('btst.b','#0x2,0x8123:w',6)
    emitter.ins('beq.b','scene_pc_03f7d2',2)
    emitter.ins('cmpi.w','#0x6,0x8148:w',6)
    emitter.ins('bne.w','scene_pc_03f7c6',4)
    emitter.ins('subq.w','#0x1,0x8146:w',4)
    emitter.ins('bne.b','scene_pc_03f7d2',2)
    emitter.ins('move.w','#0x3,0x8146:w',6)
    emitter.ins('bra.b','scene_pc_03f7d2',2)
    emitter.ins('subq.w','#0x1,0x8146:w',4)
    emitter.ins('bpl.b','scene_pc_03f7d2',2)
    emitter.ins('move.w','#0x3,0x8146:w',6)
    emitter.ins('move.w','0x8146:w,%d0',4)
    emitter.ins('lea.l','104(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('move.b','(%a0, %d0.w),%d0',4)
    emitter.ins('tst.w','0x8144:w',4)
    emitter.ins('bne.b','scene_pc_03f7e8',2)
    emitter.ins('addq.w','#0x4,%d0',2)
    emitter.ins('asl.w','#0x1,%d0',2)
    emitter.ins('lea.l','0x812a:w,%a0',4)
    emitter.ins('btst.b','#0x0,0x8123:w',6)
    emitter.ins('beq.b','scene_pc_03f81c',2)
    emitter.ins('addq.w','#0x1,(%a0, %d0.w)',4)
    emitter.ins('cmpi.w','#0xb,0x8160:w',6)
    emitter.ins('bcc.b','scene_pc_03f810',2)
    emitter.ins('cmpi.w','#0x6,(%a0, %d0.w)',6)
    emitter.ins('bcs.b','scene_pc_03f81c',2)
    emitter.ins('clr.w','(%a0, %d0.w)',4)
    emitter.ins('bra.b','scene_pc_03f81c',2)
    emitter.ins('cmpi.w','#0x6,(%a0, %d0.w)',6)
    emitter.ins('bls.b','scene_pc_03f81c',2)
    emitter.ins('clr.w','(%a0, %d0.w)',4)
    emitter.ins('btst.b','#0x1,0x8123:w',6)
    emitter.ins('beq.b','scene_pc_03f83e',2)
    emitter.ins('subq.w','#0x1,(%a0, %d0.w)',4)
    emitter.ins('bpl.b','scene_pc_03f83e',2)
    emitter.ins('move.w','#0x6,(%a0, %d0.w)',6)
    emitter.ins('cmpi.w','#0xb,0x8160:w',6)
    emitter.ins('bcc.b','scene_pc_03f83e',2)
    emitter.ins('move.w','#0x5,(%a0, %d0.w)',6)
    emitter.ins('rts','',2)
    emitter.segment(0x3f844,0x3f890)
    emitter.ins('cmpi.w','#0x6,0x8148:w',6)
    emitter.ins('bne.w','scene_pc_03f858',4)
    emitter.ins('move.w','#0x2,0x8146:w',6)
    emitter.ins('bra.w','scene_pc_03f7d2',4)
    emitter.ins('btst.b','#0x0,0x8122:w',6)
    emitter.ins('bne.w','scene_pc_03f7d2',4)
    emitter.ins('btst.b','#0x1,0x8122:w',6)
    emitter.ins('bne.w','scene_pc_03f7d2',4)
    emitter.ins('btst.b','#0x3,0x8123:w',6)
    emitter.ins('bne.b','scene_pc_03f87e',2)
    emitter.ins('btst.b','#0x2,0x8123:w',6)
    emitter.ins('beq.w','scene_pc_03f7d2',4)
    emitter.ins('subq.w','#0x2,0x8146:w',4)
    emitter.ins('bpl.w','scene_pc_03f7d2',4)
    emitter.ins('move.w','#0x2,0x8146:w',6)
    emitter.ins('bra.w','scene_pc_03f7d2',4)

def _lower_commit_scene_battle_totals(emitter,rules):
    emitter.segment(0x3f8dc,0x3f8f6)
    emitter.ins('bsr.w','scene_pc_041f08',4)
    emitter.ins('move.w','%d1,0x8118:w',4)
    emitter.ins('move.w','%d2,0x811a:w',4)
    emitter.ins('move.w','0x8178:w,0x810c:w',6)
    emitter.ins('move.w','0x8278:w,0x810e:w',6)
    emitter.ins('rts','',2)

def _lower_draw_secondary_squad_budget(emitter,rules):
    emitter.segment(0x3f8f6,0x3f9c6)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','0x80e6:w,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','#0xc3ae,%d0',4)
    emitter.ins('moveq','#4,%d3',2)
    emitter.ins('lea.l','0x8001:w,%a0',4)
    emitter.ins('bsr.w','scene_pc_03ff6e',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','0x80ee:w,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','#0xc530,%d0',4)
    emitter.ins('moveq','#3,%d3',2)
    emitter.ins('lea.l','0x8002:w,%a0',4)
    emitter.ins('bsr.w','scene_pc_03ff6e',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','0x80ea:w,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','#0xc6b4,%d0',4)
    emitter.ins('moveq','#1,%d3',2)
    emitter.ins('lea.l','0x8004:w,%a0',4)
    emitter.ins('bra.w','scene_pc_03ff4a',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','0x80ea:w,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','#0xc1ac,%d0',4)
    emitter.ins('moveq','#1,%d3',2)
    emitter.ins('lea.l','0x8004:w,%a0',4)
    emitter.ins('bsr.w','scene_pc_03ff6e',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','0x80fa:w,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','#0xc3ac,%d0',4)
    emitter.ins('moveq','#1,%d3',2)
    emitter.ins('lea.l','0x8004:w,%a0',4)
    emitter.ins('tst.w','0x8144:w',4)
    emitter.ins('bne.b','scene_pc_03f978',2)
    emitter.ins('bsr.w','scene_pc_03ff4a',4)
    emitter.ins('bra.w','scene_pc_03f97c',4)
    emitter.ins('bsr.w','scene_pc_03ff6e',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','0x80fc:w,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','#0xc5ac,%d0',4)
    emitter.ins('moveq','#1,%d3',2)
    emitter.ins('lea.l','0x8004:w,%a0',4)
    emitter.ins('cmpi.w','#0x1,0x8144:w',6)
    emitter.ins('bne.b','scene_pc_03f9a0',2)
    emitter.ins('bsr.w','scene_pc_03ff4a',4)
    emitter.ins('bra.w','scene_pc_03f9a4',4)
    emitter.ins('bsr.w','scene_pc_03ff6e',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','0x80fe:w,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','#0xc7ac,%d0',4)
    emitter.ins('moveq','#1,%d3',2)
    emitter.ins('lea.l','0x8004:w,%a0',4)
    emitter.ins('cmpi.w','#0x2,0x8144:w',6)
    emitter.ins('bne.w','scene_pc_03ff6e',4)
    emitter.ins('bra.w','scene_pc_03ff4a',4)
    emitter.segment(0x3fe5e,0x3ffa6)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','0x8176:w,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','#0xc5a0,%d0',4)
    emitter.ins('moveq','#2,%d3',2)
    emitter.ins('lea.l','0x8003:w,%a0',4)
    emitter.ins('bsr.w','scene_pc_03ff6e',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','0x8186:w,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','#0xc720,%d0',4)
    emitter.ins('moveq','#2,%d3',2)
    emitter.ins('lea.l','0x8003:w,%a0',4)
    emitter.ins('bsr.w','scene_pc_03ff6e',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','0x8276:w,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','#0xc5b2,%d0',4)
    emitter.ins('moveq','#2,%d3',2)
    emitter.ins('lea.l','0x8003:w,%a0',4)
    emitter.ins('bsr.w','scene_pc_03ff6e',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','0x8286:w,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','#0xc732,%d0',4)
    emitter.ins('moveq','#2,%d3',2)
    emitter.ins('lea.l','0x8003:w,%a0',4)
    emitter.ins('bsr.w','scene_pc_03ff6e',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','0x8100:w,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','#0xc8a0,%d0',4)
    emitter.ins('moveq','#2,%d3',2)
    emitter.ins('lea.l','0x8003:w,%a0',4)
    emitter.ins('bsr.w','scene_pc_03ff6e',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','0x8102:w,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','#0xc8b2,%d0',4)
    emitter.ins('moveq','#2,%d3',2)
    emitter.ins('lea.l','0x8003:w,%a0',4)
    emitter.ins('bsr.w','scene_pc_03ff6e',4)
    emitter.ins('move.w','#0xe,%d1',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('lea.l','0x817a:w,%a6',4)
    emitter.ins('btst.b','#0x7,(%a6)',4)
    emitter.ins('beq.b','scene_pc_03ff02',2)
    emitter.ins('add.w','0xe(%a6),%d0',4)
    emitter.ins('adda.w','#0x10,%a6',4)
    emitter.ins('dbra','%d1,scene_pc_03fef8',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','#0xca1c,%d0',4)
    emitter.ins('moveq','#4,%d3',2)
    emitter.ins('lea.l','0x8001:w,%a0',4)
    emitter.ins('bsr.w','scene_pc_03ff6e',4)
    emitter.ins('move.w','#0xe,%d1',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('lea.l','0x827a:w,%a6',4)
    emitter.ins('btst.b','#0x7,(%a6)',4)
    emitter.ins('beq.b','scene_pc_03ff30',2)
    emitter.ins('add.w','0xe(%a6),%d0',4)
    emitter.ins('adda.w','#0x10,%a6',4)
    emitter.ins('dbra','%d1,scene_pc_03ff26',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','#0xca2e,%d0',4)
    emitter.ins('moveq','#4,%d3',2)
    emitter.ins('lea.l','0x8001:w,%a0',4)
    emitter.ins('bra.w','scene_pc_03ff6e',4)
    emitter.ins('btst.b','#0x4,0xf321:w',6)
    emitter.ins('bne.b','scene_pc_03ff6e',2)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('move.w','#0xc448,%d1',4)
    emitter.ins('move.w','%d1,0xc00000:l',6)
    emitter.ins('dbra','%d3,scene_pc_03ff5e',4)
    emitter.ins('rts','',2)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('moveq','#0,%d2',2)
    emitter.ins('moveq','#0,%d1',2)
    emitter.ins('move.b','(%a0)+,%d1',2)
    emitter.ins('bne.b','scene_pc_03ff94',2)
    emitter.ins('tst.w','%d2',2)
    emitter.ins('bne.w','scene_pc_03ff94',4)
    emitter.ins('tst.w','%d3',2)
    emitter.ins('beq.w','scene_pc_03ff94',4)
    emitter.ins('move.w','#0xc448,%d1',4)
    emitter.ins('bra.b','scene_pc_03ff9a',2)
    emitter.ins('moveq','#1,%d2',2)
    emitter.ins('addi.w','#0xc460,%d1',4)
    emitter.ins('move.w','%d1,0xc00000:l',6)
    emitter.ins('dbra','%d3,scene_pc_03ff7c',4)
    emitter.ins('rts','',2)

def _lower_draw_both_force_status_panels(emitter,rules):
    emitter.segment(0x3f9c6,0x3fca8)
    emitter.ins('cmpi.b','#0x3,0x80db:w',6)
    emitter.ins('beq.w','scene_pc_03fce0',4)
    emitter.ins('move.w','#0xc412,0x8010:w',6)
    emitter.ins('move.w','#0xc420,0x8012:w',6)
    emitter.ins('move.w','#0xc430,0x8014:w',6)
    emitter.ins('move.w','#0xc440,0x8016:w',6)
    emitter.ins('move.w','#0xc398,0x8018:w',6)
    emitter.ins('clr.w','0x801a:w',4)
    emitter.ins('move.l','#0xffff827a,0x801c:w',8)
    emitter.ins('lea.l','0x826a:w,%a6',4)
    emitter.ins('bsr.w','scene_pc_03fa32',4)
    emitter.ins('move.w','#0xc292,0x8010:w',6)
    emitter.ins('move.w','#0xc2a0,0x8012:w',6)
    emitter.ins('move.w','#0xc2b0,0x8014:w',6)
    emitter.ins('move.w','#0xc2c0,0x8016:w',6)
    emitter.ins('move.w','#0xc218,0x8018:w',6)
    emitter.ins('move.w','#0x1,0x801a:w',6)
    emitter.ins('move.l','#0xffff817a,0x801c:w',8)
    emitter.ins('lea.l','0x816a:w,%a6',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','0xe(%a6),%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','0x8010:w,%d0',4)
    emitter.ins('moveq','#2,%d3',2)
    emitter.ins('lea.l','0x8003:w,%a0',4)
    emitter.ins('bsr.w','scene_pc_03ff6e',4)
    emitter.ins('move.w','#0xe,%d1',4)
    emitter.ins('movea.l','0x801c:w,%a6',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('btst.b','#0x7,(%a6)',4)
    emitter.ins('beq.b','scene_pc_03fa66',2)
    emitter.ins('cmpi.b','#0x2,0x1(%a6)',6)
    emitter.ins('bne.b','scene_pc_03fa66',2)
    emitter.ins('add.w','0xe(%a6),%d0',4)
    emitter.ins('adda.w','#0x10,%a6',4)
    emitter.ins('dbra','%d1,scene_pc_03fa54',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','0x8012:w,%d0',4)
    emitter.ins('moveq','#3,%d3',2)
    emitter.ins('lea.l','0x8002:w,%a0',4)
    emitter.ins('bsr.w','scene_pc_03ff6e',4)
    emitter.ins('move.w','#0xe,%d1',4)
    emitter.ins('movea.l','0x801c:w,%a6',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('btst.b','#0x7,(%a6)',4)
    emitter.ins('beq.b','scene_pc_03fa9c',2)
    emitter.ins('cmpi.b','#0x1,0x1(%a6)',6)
    emitter.ins('bne.b','scene_pc_03fa9c',2)
    emitter.ins('add.w','0xe(%a6),%d0',4)
    emitter.ins('adda.w','#0x10,%a6',4)
    emitter.ins('dbra','%d1,scene_pc_03fa8a',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','0x8014:w,%d0',4)
    emitter.ins('moveq','#3,%d3',2)
    emitter.ins('lea.l','0x8002:w,%a0',4)
    emitter.ins('bsr.w','scene_pc_03ff6e',4)
    emitter.ins('move.w','#0xe,%d1',4)
    emitter.ins('movea.l','0x801c:w,%a6',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('btst.b','#0x7,(%a6)',4)
    emitter.ins('beq.b','scene_pc_03fad0',2)
    emitter.ins('tst.b','0x1(%a6)',4)
    emitter.ins('bne.b','scene_pc_03fad0',2)
    emitter.ins('add.w','0xe(%a6),%d0',4)
    emitter.ins('adda.w','#0x10,%a6',4)
    emitter.ins('dbra','%d1,scene_pc_03fac0',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','0x8016:w,%d0',4)
    emitter.ins('moveq','#4,%d3',2)
    emitter.ins('lea.l','0x8001:w,%a0',4)
    emitter.ins('bsr.w','scene_pc_03ff6e',4)
    emitter.ins('tst.w','0x8144:w',4)
    emitter.ins('beq.b','scene_pc_03faf8',2)
    emitter.ins('tst.w','0x801a:w',4)
    emitter.ins('bne.b','scene_pc_03fb00',2)
    emitter.ins('rts','',2)
    emitter.ins('tst.w','0x801a:w',4)
    emitter.ins('bne.w','scene_pc_03fe5c',4)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.w','0x8018:w,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('tst.w','0x8146:w',4)
    emitter.ins('bne.b','scene_pc_03fb3c',2)
    emitter.ins('btst.b','#0x4,0xf321:w',6)
    emitter.ins('bne.b','scene_pc_03fb3c',2)
    emitter.ins('move.w','#0xc448,0xc00000:l',8)
    emitter.ins('move.w','0x8018:w,%d0',4)
    emitter.ins('addi.w','#0x80,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('move.w','#0xc448,0xc00000:l',8)
    emitter.ins('bra.b','scene_pc_03fb6c',2)
    emitter.ins('bsr.w','scene_pc_03fca8',4)
    emitter.ins('move.w','0x6(%a0),%d2',4)
    emitter.ins('bsr.w','scene_pc_03fcb8',4)
    emitter.ins('move.w','%d0,0xc00000:l',6)
    emitter.ins('move.w','0x8018:w,%d0',4)
    emitter.ins('addi.w','#0x80,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('bsr.w','scene_pc_03fca8',4)
    emitter.ins('move.w','0x6(%a0),%d2',4)
    emitter.ins('bsr.w','scene_pc_03fcb8',4)
    emitter.ins('move.w','%d1,0xc00000:l',6)
    emitter.ins('move.w','0x8018:w,%d0',4)
    emitter.ins('addi.w','#0x10,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('cmpi.w','#0x1,0x8146:w',6)
    emitter.ins('bne.b','scene_pc_03fba6',2)
    emitter.ins('btst.b','#0x4,0xf321:w',6)
    emitter.ins('bne.b','scene_pc_03fba6',2)
    emitter.ins('move.w','#0xc448,0xc00000:l',8)
    emitter.ins('move.w','0x8018:w,%d0',4)
    emitter.ins('addi.w','#0x90,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('move.w','#0xc448,0xc00000:l',8)
    emitter.ins('bra.b','scene_pc_03fbd6',2)
    emitter.ins('bsr.w','scene_pc_03fca8',4)
    emitter.ins('move.w','0x4(%a0),%d2',4)
    emitter.ins('bsr.w','scene_pc_03fcb8',4)
    emitter.ins('move.w','%d0,0xc00000:l',6)
    emitter.ins('move.w','0x8018:w,%d0',4)
    emitter.ins('addi.w','#0x90,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('bsr.w','scene_pc_03fca8',4)
    emitter.ins('move.w','0x4(%a0),%d2',4)
    emitter.ins('bsr.w','scene_pc_03fcb8',4)
    emitter.ins('move.w','%d1,0xc00000:l',6)
    emitter.ins('move.w','0x8018:w,%d0',4)
    emitter.ins('addi.w','#0x20,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('cmpi.w','#0x2,0x8146:w',6)
    emitter.ins('bne.b','scene_pc_03fc10',2)
    emitter.ins('btst.b','#0x4,0xf321:w',6)
    emitter.ins('bne.b','scene_pc_03fc10',2)
    emitter.ins('move.w','#0xc448,0xc00000:l',8)
    emitter.ins('move.w','0x8018:w,%d0',4)
    emitter.ins('addi.w','#0xa0,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('move.w','#0xc448,0xc00000:l',8)
    emitter.ins('bra.b','scene_pc_03fc40',2)
    emitter.ins('bsr.w','scene_pc_03fca8',4)
    emitter.ins('move.w','0x2(%a0),%d2',4)
    emitter.ins('bsr.w','scene_pc_03fcb8',4)
    emitter.ins('move.w','%d0,0xc00000:l',6)
    emitter.ins('move.w','0x8018:w,%d0',4)
    emitter.ins('addi.w','#0xa0,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('bsr.w','scene_pc_03fca8',4)
    emitter.ins('move.w','0x2(%a0),%d2',4)
    emitter.ins('bsr.w','scene_pc_03fcb8',4)
    emitter.ins('move.w','%d1,0xc00000:l',6)
    emitter.ins('move.w','0x8018:w,%d0',4)
    emitter.ins('addi.w','#0x32,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('cmpi.w','#0x3,0x8146:w',6)
    emitter.ins('bne.b','scene_pc_03fc7a',2)
    emitter.ins('btst.b','#0x4,0xf321:w',6)
    emitter.ins('bne.b','scene_pc_03fc7a',2)
    emitter.ins('move.w','#0xc448,0xc00000:l',8)
    emitter.ins('move.w','0x8018:w,%d0',4)
    emitter.ins('addi.w','#0xb2,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('move.w','#0xc448,0xc00000:l',8)
    emitter.ins('rts','',2)
    emitter.ins('bsr.w','scene_pc_03fca8',4)
    emitter.ins('move.w','(%a0),%d2',2)
    emitter.ins('bsr.w','scene_pc_03fcb8',4)
    emitter.ins('move.w','%d0,0xc00000:l',6)
    emitter.ins('move.w','0x8018:w,%d0',4)
    emitter.ins('addi.w','#0xb2,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('bsr.w','scene_pc_03fca8',4)
    emitter.ins('move.w','(%a0),%d2',2)
    emitter.ins('bsr.w','scene_pc_03fcb8',4)
    emitter.ins('move.w','%d1,0xc00000:l',6)
    emitter.ins('rts','',2)
    emitter.segment(0x3fce0,0x3fe5e)
    emitter.ins('move.w','#0xc49e,0x8010:w',6)
    emitter.ins('move.w','#0xc4b0,0x8012:w',6)
    emitter.ins('move.w','#0xc424,0x8014:w',6)
    emitter.ins('move.w','#0xc43a,0x8016:w',6)
    emitter.ins('clr.w','0x8018:w',4)
    emitter.ins('lea.l','0x826a:w,%a6',4)
    emitter.ins('bsr.w','scene_pc_03fd26',4)
    emitter.ins('lea.l','0x816a:w,%a6',4)
    emitter.ins('move.w','#0xc31e,0x8010:w',6)
    emitter.ins('move.w','#0xc330,0x8012:w',6)
    emitter.ins('move.w','#0xc2a4,0x8014:w',6)
    emitter.ins('move.w','#0xc2ba,0x8016:w',6)
    emitter.ins('move.w','#0x1,0x8018:w',6)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','0xe(%a6),%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','0x8010:w,%d0',4)
    emitter.ins('moveq','#2,%d3',2)
    emitter.ins('lea.l','0x8003:w,%a0',4)
    emitter.ins('bsr.w','scene_pc_03ff6e',4)
    emitter.ins('move.w','#0xe,%d1',4)
    emitter.ins('adda.w','#0x10,%a6',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('btst.b','#0x7,(%a6)',4)
    emitter.ins('beq.b','scene_pc_03fd5a',2)
    emitter.ins('cmpi.b','#0x1,0x1(%a6)',6)
    emitter.ins('bne.b','scene_pc_03fd5a',2)
    emitter.ins('add.w','0xe(%a6),%d0',4)
    emitter.ins('adda.w','#0x10,%a6',4)
    emitter.ins('dbra','%d1,scene_pc_03fd48',4)
    emitter.ins('bsr.w','scene_pc_03b2d8',4)
    emitter.ins('move.w','0x8012:w,%d0',4)
    emitter.ins('moveq','#4,%d3',2)
    emitter.ins('lea.l','0x8001:w,%a0',4)
    emitter.ins('bsr.w','scene_pc_03ff6e',4)
    emitter.ins('tst.w','0x8144:w',4)
    emitter.ins('beq.b','scene_pc_03fd82',2)
    emitter.ins('tst.w','0x8018:w',4)
    emitter.ins('bne.b','scene_pc_03fd8a',2)
    emitter.ins('rts','',2)
    emitter.ins('tst.w','0x8018:w',4)
    emitter.ins('bne.w','scene_pc_03fe5c',4)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.w','0x8014:w,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('tst.w','0x8146:w',4)
    emitter.ins('bne.b','scene_pc_03fdc6',2)
    emitter.ins('btst.b','#0x4,0xf321:w',6)
    emitter.ins('bne.b','scene_pc_03fdc6',2)
    emitter.ins('move.w','#0xc448,0xc00000:l',8)
    emitter.ins('move.w','0x8014:w,%d0',4)
    emitter.ins('addi.w','#0x80,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('move.w','#0xc448,0xc00000:l',8)
    emitter.ins('bra.b','scene_pc_03fdf6',2)
    emitter.ins('bsr.w','scene_pc_03fca8',4)
    emitter.ins('move.w','0x6(%a0),%d2',4)
    emitter.ins('bsr.w','scene_pc_03fcb8',4)
    emitter.ins('move.w','%d0,0xc00000:l',6)
    emitter.ins('move.w','0x8014:w,%d0',4)
    emitter.ins('addi.w','#0x80,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('bsr.w','scene_pc_03fca8',4)
    emitter.ins('move.w','0x6(%a0),%d2',4)
    emitter.ins('bsr.w','scene_pc_03fcb8',4)
    emitter.ins('move.w','%d1,0xc00000:l',6)
    emitter.ins('move.w','0x8016:w,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('cmpi.w','#0x2,0x8146:w',6)
    emitter.ins('bne.b','scene_pc_03fe2c',2)
    emitter.ins('btst.b','#0x4,0xf321:w',6)
    emitter.ins('bne.b','scene_pc_03fe2c',2)
    emitter.ins('move.w','#0xc448,0xc00000:l',8)
    emitter.ins('move.w','0x8016:w,%d0',4)
    emitter.ins('addi.w','#0x80,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('move.w','#0xc448,0xc00000:l',8)
    emitter.ins('bra.b','scene_pc_03fe5c',2)
    emitter.ins('bsr.w','scene_pc_03fca8',4)
    emitter.ins('move.w','0x2(%a0),%d2',4)
    emitter.ins('bsr.w','scene_pc_03fcb8',4)
    emitter.ins('move.w','%d0,0xc00000:l',6)
    emitter.ins('move.w','0x8016:w,%d0',4)
    emitter.ins('addi.w','#0x80,%d0',4)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('bsr.w','scene_pc_03fca8',4)
    emitter.ins('move.w','0x2(%a0),%d2',4)
    emitter.ins('bsr.w','scene_pc_03fcb8',4)
    emitter.ins('move.w','%d1,0xc00000:l',6)
    emitter.ins('rts','',2)

def _lower_selected_action_mode_view(emitter,rules):
    emitter.segment(0x3fca8,0x3fcb8)
    emitter.ins('lea.l','0x8132:w,%a0',4)
    emitter.ins('tst.w','0x8144:w',4)
    emitter.ins('beq.b','scene_pc_03fcb6',2)
    emitter.ins('lea.l','0x812a:w,%a0',4)
    emitter.ins('rts','',2)

def _lower_lookup_action_mode_icon_pair(emitter,rules):
    emitter.segment(0x3fcb8,0x3fcc4)
    emitter.ins('asl.w','#0x2,%d2',2)
    emitter.ins('move.w','8(%pc, %d2.w),%d0',4)
    emitter.ins('move.w','6(%pc, %d2.w),%d1',4)
    emitter.ins('rts','',2)

LOWERERS={
    'adjust_secondary_formation_scene':_lower_adjust_secondary_formation_scene,
    'update_active_battle_controls':_lower_update_active_battle_controls,
    'latch_scene_controller_inputs':_lower_latch_scene_controller_inputs,
    'draw_two_prompt_backgrounds':_lower_draw_two_prompt_backgrounds,
    'update_secondary_scene_totals':_lower_update_secondary_scene_totals,
    'begin_transition_prompt':_lower_begin_transition_prompt,
    'update_action_mode_prompt':_lower_update_action_mode_prompt,
    'dismiss_action_mode_prompt':_lower_dismiss_action_mode_prompt,
    'begin_duel_handoff_prompt':_lower_begin_duel_handoff_prompt,
    'confirm_duel_handoff_prompt':_lower_confirm_duel_handoff_prompt,
    'await_duel_handoff_palette':_lower_await_duel_handoff_palette,
    'begin_result_confirmation_prompt':_lower_begin_result_confirmation_prompt,
    'confirm_result_prompt':_lower_confirm_result_prompt,
    'begin_secondary_confirmation_prompt':_lower_begin_secondary_confirmation_prompt,
    'confirm_secondary_result_prompt':_lower_confirm_secondary_result_prompt,
    'begin_primary_confirmation_prompt':_lower_begin_primary_confirmation_prompt,
    'replace_primary_confirmation_prompt':_lower_replace_primary_confirmation_prompt,
    'confirm_primary_result_prompt':_lower_confirm_primary_result_prompt,
    'normalize_secondary_squad_size':_lower_normalize_secondary_squad_size,
    'adjust_secondary_squad_count':_lower_adjust_secondary_squad_count,
    'adjust_selected_squad_class_counts':_lower_adjust_selected_squad_class_counts,
    'adjust_secondary_formation':_lower_adjust_secondary_formation,
    'adjust_primary_formation':_lower_adjust_primary_formation,
    'adjust_selected_action_mode':_lower_adjust_selected_action_mode,
    'commit_scene_battle_totals':_lower_commit_scene_battle_totals,
    'draw_secondary_squad_budget':_lower_draw_secondary_squad_budget,
    'draw_both_force_status_panels':_lower_draw_both_force_status_panels,
    'selected_action_mode_view':_lower_selected_action_mode_view,
    'lookup_action_mode_icon_pair':_lower_lookup_action_mode_icon_pair,
}

def compile_late_phase(source, *, selected_names=None):
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    sole_active_control_fields = {name: records[name]['effects'] for name in ('_phase_action_panel_fields', '_phase_blank_panel_fields', '_phase_call_fields', '_phase_decode_panel_fields', '_phase_panel_name_fields', '_phase_statistics_panel_fields', 'adjust_scene_formation_choice_fields', 'adjust_secondary_formation_fields', 'adjust_secondary_formation_scene_fields', 'confirm_secondary_formation_scene_fields', 'deploy_scene_formation_fields', 'deploy_secondary_formation_fields', 'latch_scene_controller_inputs_fields', 'update_active_battle_controls_fields')}
    for owner in ('adjust_secondary_formation_scene', 'update_active_battle_controls', 'latch_scene_controller_inputs', 'adjust_secondary_formation'):
        records[owner]['effects'] = dict(previous=records[owner]['effects'], sole_active_control_fields=sole_active_control_fields)
    sole_pure_rule_fields = {name:records[name]['effects'] for name in ('update_secondary_scene_totals_fields', 'normalize_secondary_squad_size_fields', 'adjust_secondary_squad_count_fields', 'adjust_selected_squad_class_counts_fields', '_scene_rule_adjust_action_selection_fields', 'adjust_selected_action_mode_fields', 'commit_scene_battle_totals_fields')}
    for owner in ('update_secondary_scene_totals', 'normalize_secondary_squad_size', 'adjust_secondary_squad_count', 'adjust_selected_squad_class_counts', 'adjust_selected_action_mode', 'commit_scene_battle_totals'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'],sole_pure_rule_fields=sole_pure_rule_fields)
    sole_allocation_fields = {name:records[name]['effects'] for name in ('draw_two_prompt_backgrounds_fields', '_allocation_begin_result_fields', 'begin_transition_prompt_fields', 'begin_duel_handoff_prompt_fields', 'begin_result_confirmation_prompt_fields', 'begin_secondary_confirmation_prompt_fields', 'begin_primary_confirmation_prompt_fields', '_allocation_dismiss_result_fields', 'update_action_mode_prompt_fields', 'dismiss_action_mode_prompt_fields', 'confirm_duel_handoff_prompt_fields', 'commit_duel_handoff_fields', 'await_duel_handoff_palette_fields', '_allocation_confirm_result_fields', 'confirm_result_prompt_fields', 'confirm_secondary_result_prompt_fields', 'confirm_primary_result_prompt_fields', 'replace_primary_confirmation_prompt_fields', 'adjust_primary_formation_fields', 'deploy_primary_formation_fields', '_allocation_number_fields', 'draw_secondary_squad_budget_fields', 'draw_squad_class_budgets_fields', 'draw_blinking_decimal_panel_fields', 'draw_decimal_panel_fields', '_allocation_sum_actor_rows_fields', '_allocation_total_display_fields', 'draw_battle_summary_numbers_fields', 'selected_action_mode_view_fields', 'lookup_action_mode_icon_pair_fields', '_allocation_icon_pair_fields', '_allocation_selected_panel_fields', 'draw_normal_force_status_panel_fields', 'draw_special_force_status_panel_fields', '_allocation_panel_setup_fields', 'draw_both_force_status_panels_fields', 'finish_duel_handoff_phase_fields', 'await_result_palette_fields', 'finish_result_phase_fields', 'await_secondary_result_palette_fields', 'await_primary_result_palette_fields', 'finish_secondary_result_phase_fields', 'finish_primary_result_phase_fields')}
    for owner in ('draw_two_prompt_backgrounds', 'begin_transition_prompt', 'update_action_mode_prompt', 'dismiss_action_mode_prompt', 'begin_duel_handoff_prompt', 'confirm_duel_handoff_prompt', 'commit_duel_handoff', 'await_duel_handoff_palette', 'finish_duel_handoff_phase', 'await_result_palette', 'finish_result_phase', 'await_secondary_result_palette', 'await_primary_result_palette', 'begin_result_confirmation_prompt', 'confirm_result_prompt', 'begin_secondary_confirmation_prompt', 'confirm_secondary_result_prompt', 'finish_secondary_result_phase', 'begin_primary_confirmation_prompt', 'replace_primary_confirmation_prompt', 'confirm_primary_result_prompt', 'finish_primary_result_phase', 'adjust_primary_formation', 'deploy_primary_formation', 'draw_secondary_squad_budget', 'draw_squad_class_budgets', 'draw_battle_summary_numbers', 'draw_blinking_decimal_panel', 'draw_decimal_panel', 'draw_both_force_status_panels', 'draw_normal_force_status_panel', 'draw_special_force_status_panel', 'selected_action_mode_view', 'lookup_action_mode_icon_pair'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'],sole_allocation_fields=sole_allocation_fields)
    if selected_names is not None:
        if type(selected_names) is not tuple or selected_names != BATTLE_OBJECT_NATIVE_NAMES:
            raise CompileError('only the fixed complete B39 object-phase native family is admitted')
        selected_bindings = tuple((binding for binding in LATE_PHASE_BINDINGS if binding.name in selected_names))
        if len(selected_bindings) != len(selected_names):
            raise CompileError('all selected B39 complete physical owners are required')
        selected_lowerers = {name: LOWERERS[name] for name in selected_names}
        return lower_declared(records, selected_bindings, selected_lowerers)
    return lower_declared(records, LATE_PHASE_BINDINGS, LOWERERS)

# B39 sole active controls and shared choice/deployment fields; native lowerers unchanged.
for _module,_names in {'business_actions': ['sum_live_object_rosters',
                      'update_object_action_ai',
                      'update_object_action_ai_fields',
                      'upload_object_officer_name'],
 'business_early_phase': ['_phase_legacy_fields',
                          '_phase_legacy_projection',
                          'adjust_scene_scroll_fields',
                          'begin_scene_palette_lighten',
                          'encode_six_decimal_digits'],
 'contexts_actions': ['DuelGlyphContext'],
 'contexts_early_phase': ['BattleActors',
                          'PhaseFrame',
                          'SceneControllerConditions',
                          'SceneControllerFrame',
                          'SceneControllerOutcome',
                          'phase_add_word',
                          'phase_bit',
                          'phase_compare',
                          'phase_controller_return',
                          'phase_enter_call',
                          'phase_finish_call',
                          'phase_from_controller',
                          'phase_logic',
                          'phase_operands'],
 'contexts_late_phase': ['ActionIconContext',
                         'DigitPanelContext',
                         'DigitPanelResult',
                         'ForcePanelContext',
                         'LatePhaseDispatch',
                         'checked_context',
                         'checked_phase'],
 'domain': ['Boundary',
            'Cursor',
            'Long',
            'SceneState',
            'Table',
            'VideoPlaneAddress',
            'Word',
            'checked_state',
            'descending_inclusive',
            'divu_retained',
            'low16',
            'low8',
            'negative_word',
            'ram_view',
            'replace_byte',
            'replace_word',
            's16',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'],
 'services': ['BattlePresentationMemory',
              'FirstDeploymentFrame',
              'SceneRefreshBoundary',
              'SceneRefreshMemory',
              'SceneRenderFrame',
              '_first_byte',
              '_first_long',
              '_first_word',
              '_object_adjust_word_fields',
              '_object_clear_word_fields',
              '_presentation_call_fields',
              '_scene_refresh_decrement',
              '_scene_refresh_emit',
              '_scene_refresh_flags',
              '_scene_render_arithmetic',
              '_scene_render_asl_word',
              '_scene_render_bit',
              '_scene_render_compare',
              'clear_scene_object_label_plane',
              'clear_scene_object_label_plane_fields',
              'enqueue_sound_command_fields',
              'first_replace',
              'read_vdp_plane_rle_rows_fields',
              'read_vdp_plane_rle_rows_from_control',
              'set_vram_write_address']}.items():
    APPROVED.setdefault(_module,set()).update(_names)
DECLARATIONS.update({'_adjust_formation_choice': {'signature': 'state',
                              'returns': None,
                              'flow': 'adjust_scene_formation_choice_fields(SceneRefreshMemory(state), '
                                      'FirstDeploymentFrame.unobserved())'},
 '_deploy_formation': {'signature': 'state, frame, secondary',
                       'returns': None,
                       'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\n'
                               'actual = _phase_legacy_fields(state, frame, 259656)\n'
                               'return _phase_legacy_projection(state, frame, '
                               'deploy_scene_formation_fields(SceneRefreshMemory(state), actual, secondary))'},
 '_phase_action_panel_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                'returns': 'FirstDeploymentFrame',
                                'flow': "frame = _scene_refresh_flags(memory, _first_word(frame, 'target_x', 173), 173, 2)\n"
                                        'frame = _phase_call_fields(memory, frame, 32906, 257360)\n'
                                        'frame = _phase_blank_panel_fields(memory, frame, 191)\n'
                                        'frame = _phase_panel_name_fields(memory, frame, 4294934752, 257420)\n'
                                        'frame = _scene_refresh_emit(memory, frame, 12582916, 4, 1367343106)\n'
                                        'frame = _phase_panel_name_fields(memory, frame, 4294934754, 257446)\n'
                                        'mode = _phase_read(memory, frame, 4294934747, 1)\n'
                                        'frame = _scene_render_compare(memory, frame, mode, 3, 8)\n'
                                        'if mode == 3:\n'
                                        '    frame = _phase_decode_panel_fields(memory, frame, 283291, 49152, 257486)\n'
                                        '    frame = _phase_call_fields(memory, frame, 260550, 257490)\n'
                                        'else:\n'
                                        '    frame = _phase_decode_panel_fields(memory, frame, 282919, 49152, 257526)\n'
                                        '    frame = _phase_decode_panel_fields(memory, frame, 283206, 49216, 257558)\n'
                                        '    frame = _phase_call_fields(memory, frame, 260550, 257562)\n'
                                        'frame = memory.status_word(frame, 9472)\n'
                                        'frame = _scene_refresh_emit(memory, frame, 4294934842, 2, 1)\n'
                                        'frame = _scene_refresh_emit(memory, frame, 4294934844, 2, 0)\n'
                                        'frame = _scene_refresh_emit(memory, frame, 4294934846, 2, 1)\n'
                                        'frame = _scene_refresh_emit(memory, frame, 4294934856, 2, _phase_read(memory, frame, '
                                        '4294934840, 2))\n'
                                        'frame = _object_clear_word_fields(memory, frame, 4294934854)\n'
                                        'value = _phase_read(memory, frame, 4294934856, 2)\n'
                                        'frame = _scene_render_compare(memory, frame, value, 6, 16)\n'
                                        'if value == 6:\n'
                                        '    frame = _scene_refresh_emit(memory, frame, 4294934854, 2, 1)\n'
                                        'return memory.sync_status(frame)'},
 '_phase_blank_panel_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, counter: Word',
                               'returns': 'FirstDeploymentFrame',
                               'flow': 'frame = memory.status_word(frame, 9984)\n'
                                       'frame = _scene_refresh_emit(memory, frame, 12582916, 4, 1342177282)\n'
                                       'frame = first_replace(frame, scratch=memory.cursor_at(12582912))\n'
                                       "frame = _scene_refresh_flags(memory, _first_word(frame, 'offset_y', 13107), 13107, 2)\n"
                                       "frame = _scene_refresh_flags(memory, _first_word(frame, 'choice', counter), counter, 2)\n"
                                       'for index in range(counter + 1):\n'
                                       '    frame = _scene_refresh_emit(memory, frame, frame.scratch.base, 2, '
                                       'low16(frame.offset_y))\n'
                                       '    remaining = low16(frame.choice)\n'
                                       "    frame = _scene_refresh_decrement(frame, 'choice', remaining)\n"
                                       'return _scene_refresh_emit(memory, frame, 12582916, 4, 1342177282)'},
 '_phase_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "if (target, continuation) not in ((256284, 256246), (259612, 257248), (262940, 257262), (262940, 257290), (252272, 257296), (32906, 257360), (262850, 257420), (262850, 257446), (240342, 257486), (260550, 257490), (240342, 257526), (240342, 257558), (260550, 257562), (32906, 257634), (262850, 257694), (262850, 257710), (262850, 257726), (262850, 257742), (240342, 257774), (261726, 257796), (269228, 257822)):\n    raise ValueError('actual main phase target/continuation required')\nif frame.stack_cursor is None or frame.status is None:\n    raise SceneRefreshBoundary(target, frame, None)\n\ndef child(state, entered):\n    if target == 256284:\n        return latch_scene_controller_inputs_fields(memory, entered)\n    if target == 259612:\n        return adjust_secondary_formation_fields(memory, entered)\n    if target == 262940:\n        return clear_scene_object_label_plane_fields(memory, entered)\n    if target == 252272:\n        from .business_early_phase import adjust_scene_scroll_fields\n        return adjust_scene_scroll_fields(memory, entered)\n    if target == 32906:\n        return enqueue_sound_command_fields(memory, entered)\n    if target == 262850:\n        from .business_actions import upload_object_officer_name_frame_fields\n        return upload_object_officer_name_frame_fields(memory.state, entered)\n    if target == 260550:\n        return draw_both_force_status_panels_fields(memory, entered)\n    if target == 261726:\n        return draw_battle_summary_numbers_fields(memory, entered)\n    if target == 240342:\n        from ..high_level_scene_flows.business_scene import read_vdp_plane_rle_rows_from_control_fields\n        return read_vdp_plane_rle_rows_from_control_fields(memory, entered)\n    if target == 269228:\n        from .business_actions import update_object_action_ai_fields\n        return update_object_action_ai_fields(memory, entered)\n    raise SceneRefreshBoundary(target, memory.sync_status(entered), continuation)\nreturn _presentation_call_fields(BattlePresentationMemory(memory.state), frame, continuation, child)"},
 '_phase_decode_panel_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, source: Long, '
                                             'destination: Long, continuation: Long',
                                'returns': 'FirstDeploymentFrame',
                                'flow': 'frame = first_replace(frame, roster=memory.cursor_at(source), '
                                        'candidates=memory.cursor_at(destination))\n'
                                        "frame = _scene_refresh_flags(memory, _first_long(frame, 'offset_x', 128), 128, 4)\n"
                                        'frame = _scene_refresh_emit(memory, frame, 4294934528, 2, 32768)\n'
                                        "frame = _scene_refresh_flags(memory, _first_word(frame, 'offset_y', 32), 32, 2)\n"
                                        'return _phase_call_fields(memory, frame, 240342, continuation)'},
 '_phase_panel_name_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, officer_address: Long, '
                                           'continuation: Long',
                              'returns': 'FirstDeploymentFrame',
                              'flow': "frame = _phase_word_from_memory(memory, frame, 'choice', officer_address)\n"
                                      "frame = _scene_refresh_flags(memory, _first_word(frame, 'target_x', 3), 3, 2)\n"
                                      "frame = _scene_refresh_flags(memory, _first_word(frame, 'target_y', 1), 1, 2)\n"
                                      'return _phase_call_fields(memory, frame, 262850, continuation)'},
 '_phase_read': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, address: Long, width: Word',
                 'returns': None,
                 'flow': 'memory.sync_status(frame)\nreturn memory.state.read(address, width)'},
 '_phase_statistics_panel_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': "frame = _scene_refresh_flags(memory, _first_word(frame, 'target_x', 173), 173, 2)\n"
                                            'frame = _phase_call_fields(memory, frame, 32906, 257634)\n'
                                            'frame = _phase_blank_panel_fields(memory, frame, 767)\n'
                                            'for address, token in ((4294934748, 257694), (4294934750, 257710), (4294934752, '
                                            '257726), (4294934754, 257742)):\n'
                                            '    frame = _phase_panel_name_fields(memory, frame, address, token)\n'
                                            'frame = _phase_decode_panel_fields(memory, frame, 281196, 49152, 257774)\n'
                                            'frame = _scene_refresh_emit(memory, frame, 4294934842, 2, 2)\n'
                                            'frame = _scene_refresh_emit(memory, frame, 4294934844, 2, 0)\n'
                                            'frame = _scene_refresh_emit(memory, frame, 4294934846, 2, 1)\n'
                                            'frame = _phase_call_fields(memory, frame, 261726, 257796)\n'
                                            'return memory.status_word(frame, 9472)'},
 '_phase_word_from_memory': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, address: Long',
                             'returns': 'FirstDeploymentFrame',
                             'flow': 'value = _phase_read(memory, frame, address, 2)\n'
                                     'return _scene_refresh_flags(memory, _first_word(frame, name, value), value, 2)'},
 'adjust_scene_formation_choice_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'memory.frame(frame)\n'
                                                  'value = _phase_read(memory, frame, 4294934815, 1)\n'
                                                  'frame = _scene_render_bit(memory, frame, value, 4)\n'
                                                  'if value & 4:\n'
                                                  '    frame = _object_adjust_word_fields(memory, frame, 4294934852, 1)\n'
                                                  '    choice = _phase_read(memory, frame, 4294934852, 2)\n'
                                                  '    frame = _scene_render_compare(memory, frame, choice, 5, 16)\n'
                                                  '    if choice >= 5:\n'
                                                  '        frame = _object_clear_word_fields(memory, frame, 4294934852)\n'
                                                  'value = _phase_read(memory, frame, 4294934815, 1)\n'
                                                  'frame = _scene_render_bit(memory, frame, value, 8)\n'
                                                  'if value & 8:\n'
                                                  '    frame = _object_adjust_word_fields(memory, frame, 4294934852, 1, True)\n'
                                                  '    if frame.status is None:\n'
                                                  '        raise SceneRefreshBoundary(259648, frame, None)\n'
                                                  '    if frame.status & 8:\n'
                                                  '        frame = _scene_refresh_emit(memory, frame, 4294934852, 2, 4)\n'
                                                  'return memory.sync_status(frame)'},
 'adjust_secondary_formation': {'signature': 'state: SceneState, frame: PhaseFrame',
                                'returns': 'PhaseFrame',
                                'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\n'
                                        'actual = _phase_legacy_fields(state, frame, 259612)\n'
                                        'return _phase_legacy_projection(state, frame, '
                                        'adjust_secondary_formation_fields(SceneRefreshMemory(state), actual))'},
 'adjust_secondary_formation_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'return deploy_scene_formation_fields(memory, '
                                               'adjust_scene_formation_choice_fields(memory, frame), True)'},
 'adjust_secondary_formation_scene': {'signature': 'state: SceneState, frame: PhaseFrame',
                                      'returns': 'PhaseFrame',
                                      'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\n'
                                              'actual = _phase_legacy_fields(state, frame, 257244, True)\n'
                                              'return _phase_legacy_projection(state, frame, '
                                              'adjust_secondary_formation_scene_fields(SceneRefreshMemory(state), actual))'},
 'adjust_secondary_formation_scene_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                             'returns': 'FirstDeploymentFrame',
                                             'flow': 'memory.frame(frame)\n'
                                                     'if frame.stack_cursor is None or frame.status is None:\n'
                                                     '    raise SceneRefreshBoundary(257244, frame, None)\n'
                                                     'frame = _phase_call_fields(memory, frame, 259612, 257248)\n'
                                                     "frame = _first_byte(frame, 'target_x', _phase_read(memory, frame, "
                                                     '4294934815, 1))\n'
                                                     'value = low16(frame.target_x) & 12\n'
                                                     "frame = _scene_refresh_flags(memory, _first_word(frame, 'target_x', "
                                                     'value), value, 2)\n'
                                                     'if value:\n'
                                                     '    return _phase_call_fields(memory, frame, 262940, 257262)\n'
                                                     'value = _phase_read(memory, frame, 4294934815, 1)\n'
                                                     'frame = _scene_render_bit(memory, frame, value, 32)\n'
                                                     'if value & 32:\n'
                                                     '    frame = _scene_refresh_emit(memory, frame, 4294934842, 2, 8)\n'
                                                     '    frame = _object_clear_word_fields(memory, frame, 4294934844)\n'
                                                     '    frame = _object_clear_word_fields(memory, frame, 4294934860)\n'
                                                     '    frame = _phase_call_fields(memory, frame, 262940, 257290)\n'
                                                     'return memory.sync_status(frame)'},
 'confirm_secondary_formation_scene': {'signature': 'state: SceneState, frame: PhaseFrame',
                                       'returns': 'PhaseFrame',
                                       'flow': 'return adjust_secondary_formation_scene(state, frame)'},
 'confirm_secondary_formation_scene_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                              'returns': 'FirstDeploymentFrame',
                                              'flow': 'return adjust_secondary_formation_scene_fields(memory, frame)'},
 'deploy_scene_formation_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, secondary: bool',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'memory.frame(frame)\n'
                                           "for name in ('target_x', 'target_y', 'unit', 'count'):\n"
                                           '    if frame.carrier(name) is None:\n'
                                           '        raise SceneRefreshBoundary(259656, frame, None)\n'
                                           "frame = _phase_word_from_memory(memory, frame, 'target_x', 4294934852)\n"
                                           "frame = _scene_render_asl_word(memory, frame, 'target_x', low16(frame.target_x), 2)\n"
                                           'frame = first_replace(frame, roster=memory.cursor_at(268888))\n'
                                           'pointer = frame.roster.long(low16(frame.target_x))\n'
                                           'frame = first_replace(frame, scratch=memory.cursor_at(pointer))\n'
                                           "frame = _phase_word_from_memory(memory, frame, 'target_y', 4294934778)\n"
                                           "frame = _phase_word_from_memory(memory, frame, 'unit', 4294934780)\n"
                                           "frame = _phase_word_from_memory(memory, frame, 'count', 4294934782)\n"
                                           "frame = _scene_refresh_flags(memory, _first_long(frame, 'distance', 0), 0, 4)\n"
                                           'frame = first_replace(frame, auxiliary=memory.cursor_at(4294935146 if secondary else '
                                           '4294934890))\n'
                                           'end = 4294935402 if secondary else 4294935146\n'
                                           'while True:\n'
                                           '    if secondary:\n'
                                           "        frame = _scene_refresh_flags(memory, _first_word(frame, 'target_x', 352), "
                                           '352, 2)\n'
                                           '        value = _phase_read(memory, frame, frame.scratch.base, 2)\n'
                                           '        frame = first_replace(frame, scratch=frame.scratch.advance(2))\n'
                                           "        frame = _scene_render_arithmetic(memory, frame, 'target_x', 352, value, 16, "
                                           'True)\n'
                                           '        frame = _scene_refresh_emit(memory, frame, u32(frame.auxiliary.base + 2), 2, '
                                           'low16(frame.target_x))\n'
                                           '    else:\n'
                                           '        value = _phase_read(memory, frame, frame.scratch.base, 2)\n'
                                           '        frame = first_replace(frame, scratch=frame.scratch.advance(2))\n'
                                           '        frame = _scene_refresh_emit(memory, frame, u32(frame.auxiliary.base + 2), 2, '
                                           'value)\n'
                                           '    value = _phase_read(memory, frame, frame.scratch.base, 2)\n'
                                           '    frame = first_replace(frame, scratch=frame.scratch.advance(2))\n'
                                           '    frame = _scene_refresh_emit(memory, frame, u32(frame.auxiliary.base + 4), 2, '
                                           'value)\n'
                                           '    frame = _scene_refresh_emit(memory, frame, u32(frame.auxiliary.base + 6), 2, 1)\n'
                                           '    frame = _scene_refresh_emit(memory, frame, u32(frame.auxiliary.base + 8), 2, 1)\n'
                                           '    frame = _scene_refresh_flags(memory, frame, low16(frame.distance), 2)\n'
                                           '    if low16(frame.distance) == 0:\n'
                                           '        frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, 32771)\n'
                                           "        frame = _scene_refresh_flags(memory, _first_long(frame, 'distance', 1), 1, "
                                           '4)\n'
                                           '    else:\n'
                                           '        selected = None\n'
                                           "        for name, header in (('target_y', 32770), ('unit', 32769), ('count', "
                                           '32768)):\n'
                                           '            value = low16(frame.carrier(name))\n'
                                           '            frame = _scene_refresh_flags(memory, frame, value, 2)\n'
                                           '            if value:\n'
                                           '                selected = name\n'
                                           '                frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, '
                                           'header)\n'
                                           '                frame = _scene_render_arithmetic(memory, frame, name, value, 1, 16, '
                                           'True)\n'
                                           '                break\n'
                                           '        if selected is None:\n'
                                           '            return memory.sync_status(frame)\n'
                                           '    frame = first_replace(frame, auxiliary=frame.auxiliary.advance(16))\n'
                                           '    frame = _scene_render_compare(memory, frame, frame.auxiliary.base, end, 32)\n'
                                           '    if frame.auxiliary.base >= end:\n'
                                           '        return memory.sync_status(frame)'},
 'deploy_secondary_formation': {'signature': 'state: SceneState, frame: PhaseFrame',
                                'returns': 'PhaseFrame',
                                'flow': 'return _deploy_formation(state, frame, True)'},
 'deploy_secondary_formation_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'return deploy_scene_formation_fields(memory, frame, True)'},
 'latch_scene_controller_inputs': {'signature': 'state: SceneState, frame: PhaseFrame',
                                   'returns': 'PhaseFrame',
                                   'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\n'
                                           'actual = _phase_legacy_fields(state, frame, 256284)\n'
                                           'return _phase_legacy_projection(state, frame, '
                                           'latch_scene_controller_inputs_fields(SceneRefreshMemory(state), actual))'},
 'latch_scene_controller_inputs_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'memory.frame(frame)\n'
                                                  'mode = _phase_read(memory, frame, 4294934746, 1)\n'
                                                  'frame = _scene_refresh_flags(memory, frame, mode, 1)\n'
                                                  'if mode == 0:\n'
                                                  '    frame = _scene_refresh_emit(memory, frame, 4294934812, 2, '
                                                  '_phase_read(memory, frame, 4294964738, 2))\n'
                                                  '    frame = _scene_refresh_emit(memory, frame, 4294934814, 2, '
                                                  '_phase_read(memory, frame, 4294964738, 2))\n'
                                                  '    return _object_clear_word_fields(memory, frame, 4294934816)\n'
                                                  'mode = _phase_read(memory, frame, 4294934746, 1)\n'
                                                  'frame = _scene_render_compare(memory, frame, mode, 1, 8)\n'
                                                  'if mode == 1:\n'
                                                  '    first, second = (4294964738, 4294964740)\n'
                                                  'else:\n'
                                                  '    mode = _phase_read(memory, frame, 4294934746, 1)\n'
                                                  '    frame = _scene_render_compare(memory, frame, mode, 2, 8)\n'
                                                  '    if mode != 2:\n'
                                                  '        frame = _scene_refresh_emit(memory, frame, 4294934812, 2, '
                                                  '_phase_read(memory, frame, 4294964740, 2))\n'
                                                  '        frame = _scene_refresh_emit(memory, frame, 4294934814, 2, '
                                                  '_phase_read(memory, frame, 4294964740, 2))\n'
                                                  '        return _object_clear_word_fields(memory, frame, 4294934816)\n'
                                                  '    first, second = (4294964740, 4294964738)\n'
                                                  'if frame.target_x is None:\n'
                                                  '    raise SceneRefreshBoundary(256284, frame, None)\n'
                                                  "frame = _phase_word_from_memory(memory, frame, 'target_x', 4294964738)\n"
                                                  'value = low16(frame.target_x) | _phase_read(memory, frame, 4294964740, 2)\n'
                                                  "frame = _scene_refresh_flags(memory, _first_word(frame, 'target_x', value), "
                                                  'value, 2)\n'
                                                  'frame = _scene_refresh_emit(memory, frame, 4294934812, 2, '
                                                  'low16(frame.target_x))\n'
                                                  'frame = _scene_refresh_emit(memory, frame, 4294934814, 2, _phase_read(memory, '
                                                  'frame, first, 2))\n'
                                                  'return _scene_refresh_emit(memory, frame, 4294934816, 2, _phase_read(memory, '
                                                  'frame, second, 2))'},
 'update_active_battle_controls': {'signature': 'state: SceneState, frame: PhaseFrame',
                                   'returns': 'PhaseFrame',
                                   'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\n'
                                           'actual = _phase_legacy_fields(state, frame, 257292, True)\n'
                                           'return _phase_legacy_projection(state, frame, '
                                           'update_active_battle_controls_fields(SceneRefreshMemory(state), actual))'},
 'update_active_battle_controls_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'memory.frame(frame)\n'
                                                  'if frame.stack_cursor is None or frame.status is None:\n'
                                                  '    raise SceneRefreshBoundary(257292, frame, None)\n'
                                                  'frame = _phase_call_fields(memory, frame, 252272, 257296)\n'
                                                  "frame = _first_byte(frame, 'target_x', _phase_read(memory, frame, 4294934815, "
                                                  '1))\n'
                                                  'value = low8(frame.target_x) & 32\n'
                                                  "frame = _scene_refresh_flags(memory, _first_byte(frame, 'target_x', value), "
                                                  'value, 1)\n'
                                                  'if value:\n'
                                                  '    frame = _object_clear_word_fields(memory, frame, 4294934852)\n'
                                                  '    frame = _scene_refresh_emit(memory, frame, 4294934806, 2, 1)\n'
                                                  '    return _phase_action_panel_fields(memory, frame)\n'
                                                  'mode = _phase_read(memory, frame, 4294934746, 1)\n'
                                                  'frame = _scene_refresh_flags(memory, frame, mode, 1)\n'
                                                  'if mode:\n'
                                                  "    frame = _first_byte(frame, 'target_x', _phase_read(memory, frame, "
                                                  '4294934817, 1))\n'
                                                  '    value = low8(frame.target_x) & 32\n'
                                                  "    frame = _scene_refresh_flags(memory, _first_byte(frame, 'target_x', "
                                                  'value), value, 1)\n'
                                                  '    if value:\n'
                                                  '        frame = _scene_refresh_emit(memory, frame, 4294934852, 2, 1)\n'
                                                  '        frame = _object_clear_word_fields(memory, frame, 4294934806)\n'
                                                  '        return _phase_action_panel_fields(memory, frame)\n'
                                                  "frame = _first_byte(frame, 'target_x', _phase_read(memory, frame, 4294934813, "
                                                  '1))\n'
                                                  'value = low8(frame.target_x) & 64\n'
                                                  "frame = _scene_refresh_flags(memory, _first_byte(frame, 'target_x', value), "
                                                  'value, 1)\n'
                                                  'if value:\n'
                                                  '    return _phase_statistics_panel_fields(memory, frame)\n'
                                                  'latch = _phase_read(memory, frame, 4294934860, 2)\n'
                                                  'frame = _scene_refresh_flags(memory, frame, latch, 2)\n'
                                                  'if latch == 0:\n'
                                                  '    frame = _scene_refresh_emit(memory, frame, 4294934860, 2, 1)\n'
                                                  '    frame = _object_adjust_word_fields(memory, frame, 4294934880, 1)\n'
                                                  '    frame = _phase_call_fields(memory, frame, 269228, 257822)\n'
                                                  'mode = _phase_read(memory, frame, 4294934832, 2)\n'
                                                  'frame = _scene_render_compare(memory, frame, mode, 6, 16)\n'
                                                  'if mode == 6:\n'
                                                  '    position = _phase_read(memory, frame, 4294934892, 2)\n'
                                                  '    frame = _scene_render_compare(memory, frame, position, 0, 16)\n'
                                                  '    if position == 0:\n'
                                                  '        for address, value in ((4294934842, 5), (4294934844, 0), (4294934804, '
                                                  '4), (4294934806, 0)):\n'
                                                  '            frame = _scene_refresh_emit(memory, frame, address, 2, value)\n'
                                                  '        return memory.sync_status(frame)\n'
                                                  'mode = _phase_read(memory, frame, 4294934840, 2)\n'
                                                  'frame = _scene_render_compare(memory, frame, mode, 6, 16)\n'
                                                  'if mode == 6:\n'
                                                  '    position = _phase_read(memory, frame, 4294935148, 2)\n'
                                                  '    frame = _scene_render_compare(memory, frame, position, 352, 16)\n'
                                                  '    if position >= 352:\n'
                                                  '        for address, value in ((4294934842, 5), (4294934844, 0), (4294934804, '
                                                  '5), (4294934806, 1)):\n'
                                                  '            frame = _scene_refresh_emit(memory, frame, address, 2, value)\n'
                                                  'return memory.sync_status(frame)'}})

BATTLE_OBJECT_NATIVE_NAMES = ('adjust_secondary_formation_scene', 'update_active_battle_controls', 'latch_scene_controller_inputs', 'adjust_secondary_formation')

# D43 actual CMPA.L uses the sole full-LONG comparison; narrow movement API unchanged.
APPROVED.setdefault('services',set()).add('_first_compare_long')
DECLARATIONS.update({'deploy_scene_formation_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                'FirstDeploymentFrame, secondary: bool',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'from .services import _first_compare_long\n'
                                           'memory.frame(frame)\n'
                                           "for name in ('target_x', 'target_y', 'unit', 'count'):\n"
                                           '    if frame.carrier(name) is None:\n'
                                           '        raise SceneRefreshBoundary(259656, frame, None)\n'
                                           "frame = _phase_word_from_memory(memory, frame, 'target_x', "
                                           '4294934852)\n'
                                           "frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                           'low16(frame.target_x), 2)\n'
                                           'frame = first_replace(frame, '
                                           'roster=memory.cursor_at(268888))\n'
                                           'pointer = frame.roster.long(low16(frame.target_x))\n'
                                           'frame = first_replace(frame, '
                                           'scratch=memory.cursor_at(pointer))\n'
                                           "frame = _phase_word_from_memory(memory, frame, 'target_y', "
                                           '4294934778)\n'
                                           "frame = _phase_word_from_memory(memory, frame, 'unit', "
                                           '4294934780)\n'
                                           "frame = _phase_word_from_memory(memory, frame, 'count', "
                                           '4294934782)\n'
                                           'frame = _scene_refresh_flags(memory, _first_long(frame, '
                                           "'distance', 0), 0, 4)\n"
                                           'frame = first_replace(frame, '
                                           'auxiliary=memory.cursor_at(4294935146 if secondary else '
                                           '4294934890))\n'
                                           'end = 4294935402 if secondary else 4294935146\n'
                                           'while True:\n'
                                           '    if secondary:\n'
                                           '        frame = _scene_refresh_flags(memory, '
                                           "_first_word(frame, 'target_x', 352), 352, 2)\n"
                                           '        value = _phase_read(memory, frame, '
                                           'frame.scratch.base, 2)\n'
                                           '        frame = first_replace(frame, '
                                           'scratch=frame.scratch.advance(2))\n'
                                           '        frame = _scene_render_arithmetic(memory, frame, '
                                           "'target_x', 352, value, 16, True)\n"
                                           '        frame = _scene_refresh_emit(memory, frame, '
                                           'u32(frame.auxiliary.base + 2), 2, low16(frame.target_x))\n'
                                           '    else:\n'
                                           '        value = _phase_read(memory, frame, '
                                           'frame.scratch.base, 2)\n'
                                           '        frame = first_replace(frame, '
                                           'scratch=frame.scratch.advance(2))\n'
                                           '        frame = _scene_refresh_emit(memory, frame, '
                                           'u32(frame.auxiliary.base + 2), 2, value)\n'
                                           '    value = _phase_read(memory, frame, frame.scratch.base, '
                                           '2)\n'
                                           '    frame = first_replace(frame, '
                                           'scratch=frame.scratch.advance(2))\n'
                                           '    frame = _scene_refresh_emit(memory, frame, '
                                           'u32(frame.auxiliary.base + 4), 2, value)\n'
                                           '    frame = _scene_refresh_emit(memory, frame, '
                                           'u32(frame.auxiliary.base + 6), 2, 1)\n'
                                           '    frame = _scene_refresh_emit(memory, frame, '
                                           'u32(frame.auxiliary.base + 8), 2, 1)\n'
                                           '    frame = _scene_refresh_flags(memory, frame, '
                                           'low16(frame.distance), 2)\n'
                                           '    if low16(frame.distance) == 0:\n'
                                           '        frame = _scene_refresh_emit(memory, frame, '
                                           'frame.auxiliary.base, 2, 32771)\n'
                                           '        frame = _scene_refresh_flags(memory, '
                                           "_first_long(frame, 'distance', 1), 1, 4)\n"
                                           '    else:\n'
                                           '        selected = None\n'
                                           "        for name, header in (('target_y', 32770), ('unit', "
                                           "32769), ('count', 32768)):\n"
                                           '            value = low16(frame.carrier(name))\n'
                                           '            frame = _scene_refresh_flags(memory, frame, '
                                           'value, 2)\n'
                                           '            if value:\n'
                                           '                selected = name\n'
                                           '                frame = _scene_refresh_emit(memory, frame, '
                                           'frame.auxiliary.base, 2, header)\n'
                                           '                frame = _scene_render_arithmetic(memory, '
                                           'frame, name, value, 1, 16, True)\n'
                                           '                break\n'
                                           '        if selected is None:\n'
                                           '            return memory.sync_status(frame)\n'
                                           '    frame = first_replace(frame, '
                                           'auxiliary=frame.auxiliary.advance(16))\n'
                                           '    frame = memory.sync_status(_first_compare_long(frame, '
                                           'frame.auxiliary.base, end))\n'
                                           '    if frame.auxiliary.base >= end:\n'
                                           '        return memory.sync_status(frame)'}})

DECLARATIONS.update({'update_secondary_scene_totals': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nentered = _phase_legacy_fields(state, frame, 257224)\nreturned = update_secondary_scene_totals_fields(SceneRefreshMemory(state), entered)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'normalize_secondary_squad_size': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nentered = _phase_legacy_fields(state, frame, 259166)\nreturned = normalize_secondary_squad_size_fields(SceneRefreshMemory(state), entered)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'adjust_secondary_squad_count': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nentered = _phase_legacy_fields(state, frame, 259352)\nreturned = adjust_secondary_squad_count_fields(SceneRefreshMemory(state), entered)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'adjust_selected_squad_class_counts': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nentered = _phase_legacy_fields(state, frame, 259378)\nreturned = adjust_selected_squad_class_counts_fields(SceneRefreshMemory(state), entered)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'adjust_selected_action_mode': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nentered = _phase_legacy_fields(state, frame, 259936)\nreturned = adjust_selected_action_mode_fields(SceneRefreshMemory(state), entered)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'commit_scene_battle_totals': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nentered = _phase_legacy_fields(state, frame, 260316)\nreturned = commit_scene_battle_totals_fields(SceneRefreshMemory(state), entered)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'update_secondary_scene_totals_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _scene_rule_summary_fields(memory, frame, True)'}})

DECLARATIONS.update({'normalize_secondary_squad_size_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 259166)\nstate = memory.state\nwhile True:\n    frame = _movement_move_long(state, frame, 'target_x', 0)\n    frame = _movement_move_long(state, frame, 'target_y', 0)\n    frame = _movement_move(state, frame, 'target_x', state.read(4294934758, 2), 16)\n    frame = _movement_move(state, frame, 'target_y', state.read(4294934762, 2), 16)\n    if frame.status & 4:\n        frame = _object_adjust_word_fields(memory, frame, 4294934762, 1)\n        continue\n    frame = _movement_compare(state, frame, low16(frame.target_y), 15, 16)\n    if not frame.status & 5:\n        frame = _object_adjust_word_fields(memory, frame, 4294934762, 1, True)\n        continue\n    frame = _movement_divu_word(state, frame, 'target_x', low16(frame.target_y), 259202)\n    frame = _movement_compare(state, frame, low16(frame.target_x), 1000, 16)\n    if not frame.status & 5:\n        frame = _object_adjust_word_fields(memory, frame, 4294934762, 1)\n        continue\n    frame = _movement_compare(state, frame, low16(frame.target_x), 100, 16)\n    if frame.status & 5:\n        frame = _movement_compare(state, frame, state.read(4294934762, 2), 1, 16)\n        if not frame.status & 4:\n            frame = _object_adjust_word_fields(memory, frame, 4294934762, 1, True)\n            continue\n        frame = _movement_test(state, frame, low16(frame.target_x), 16)\n        if frame.status & 4:\n            frame = _scene_rule_store_word_fields(memory, frame, 4294934766, 0, True)\n            return _scene_rule_store_word_fields(memory, frame, 4294934770, 0, True)\n    frame = _scene_rule_store_word_fields(memory, frame, 4294934766, low16(frame.target_x))\n    frame = _movement_move_long(state, frame, 'target_x', swap_words(frame.target_x))\n    return _scene_rule_store_word_fields(memory, frame, 4294934770, low16(frame.target_x))"}})

DECLARATIONS.update({'adjust_secondary_squad_count_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 259352)\nframe, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934815, 0)\nif pressed:\n    frame = _object_adjust_word_fields(memory, frame, 4294934762, 1)\nframe, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934815, 1)\nif pressed:\n    frame = _object_adjust_word_fields(memory, frame, 4294934762, 1, True)\nreturn memory.sync_status(frame)'}})

DECLARATIONS.update({'adjust_selected_squad_class_counts_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 259378)\nstate = memory.state\nframe, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934815, 0)\nif pressed:\n    frame = _movement_move(state, frame, 'target_x', state.read(4294934778, 2), 16)\n    frame = _movement_add_word(state, frame, 'target_x', state.read(4294934780, 2))\n    frame = _movement_add_word(state, frame, 'target_x', state.read(4294934782, 2))\n    frame = _movement_compare(state, frame, low16(frame.target_x), state.read(4294934762, 2), 16)\n    if frame.status & 1:\n        frame = _movement_move(state, frame, 'target_x', state.read(4294934852, 2), 16)\n        frame = _scene_render_asl_word(memory, frame, 'target_x', low16(frame.target_x), 2)\n        frame = first_replace(frame, roster=memory.cursor_at(259576))\n        frame = first_replace(frame, candidates=memory.cursor_at(frame.roster.long(low16(frame.target_x))))\n        frame = _movement_move_long(state, frame, 'target_x', 0)\n        for band, threshold in ((1, 100), (2, 200), (3, 300), (4, 400), (5, 500), (6, 600)):\n            frame = _movement_compare(state, frame, state.read(4294934802, 2), threshold, 16)\n            if frame.status & 5:\n                break\n            frame = _movement_move_long(state, frame, 'target_x', band)\n        frame = _movement_move(state, frame, 'target_y', state.read(4294934852, 2), 16)\n        frame = _scene_render_asl_word(memory, frame, 'target_y', low16(frame.target_y), 3)\n        frame = _movement_add_word(state, frame, 'target_y', low16(frame.target_x))\n        frame = _movement_move(state, frame, 'target_x', frame.candidates.word(0), 16)\n        frame = first_replace(frame, roster=memory.cursor_at(259588))\n        frame = _movement_compare(state, frame, low8(frame.target_x), frame.roster.byte(low16(frame.target_y)), 8)\n        if frame.status & 1:\n            frame = _object_adjust_word_fields(memory, frame, frame.candidates.base, 1)\nframe, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934815, 1)\nif pressed:\n    frame = _movement_move(state, frame, 'target_x', state.read(4294934852, 2), 16)\n    frame = _scene_render_asl_word(memory, frame, 'target_x', low16(frame.target_x), 2)\n    frame = first_replace(frame, roster=memory.cursor_at(259576))\n    frame = first_replace(frame, roster=memory.cursor_at(frame.roster.long(low16(frame.target_x))))\n    frame = _movement_test(state, frame, frame.roster.word(0), 16)\n    if not frame.status & 4:\n        frame = _object_adjust_word_fields(memory, frame, frame.roster.base, 1, True)\nframe, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934815, 5)\nif pressed:\n    frame = _movement_compare(state, frame, state.read(4294934852, 2), 2, 16)\n    if frame.status & 1:\n        frame = _object_adjust_word_fields(memory, frame, 4294934852, 1)\nframe, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934815, 4)\nif pressed:\n    frame = _movement_test(state, frame, state.read(4294934852, 2), 16)\n    if not frame.status & 4:\n        frame = _object_adjust_word_fields(memory, frame, 4294934852, 1, True)\nreturn memory.sync_status(frame)"}})

DECLARATIONS.update({'_scene_rule_adjust_action_selection_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, restricted: bool', 'returns': 'FirstDeploymentFrame', 'flow': 'state = memory.state\nif restricted:\n    frame = _movement_compare(state, frame, state.read(4294934856, 2), 6, 16)\n    if frame.status & 4:\n        return _scene_rule_store_word_fields(memory, frame, 4294934854, 2)\nframe, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934818, 0)\nif pressed:\n    return frame\nframe, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934818, 1)\nif pressed:\n    return frame\nframe, forward = _scene_rule_input_bit_fields(memory, frame, 4294934819, 3)\nif restricted:\n    if not forward:\n        frame, backward = _scene_rule_input_bit_fields(memory, frame, 4294934819, 2)\n        if not backward:\n            return frame\n    frame = _object_adjust_word_fields(memory, frame, 4294934854, 2, True)\n    if frame.status & 8:\n        frame = _scene_rule_store_word_fields(memory, frame, 4294934854, 2)\n    return frame\nif forward:\n    frame = _object_adjust_word_fields(memory, frame, 4294934854, 1)\n    frame = _movement_compare(state, frame, state.read(4294934854, 2), 4, 16)\n    if not frame.status & 1:\n        frame = _scene_rule_store_word_fields(memory, frame, 4294934854, 0, True)\n        frame = _movement_compare(state, frame, state.read(4294934856, 2), 6, 16)\n        if frame.status & 4:\n            frame = _scene_rule_store_word_fields(memory, frame, 4294934854, 1)\nframe, backward = _scene_rule_input_bit_fields(memory, frame, 4294934819, 2)\nif backward:\n    frame = _movement_compare(state, frame, state.read(4294934856, 2), 6, 16)\n    special = bool(frame.status & 4)\n    frame = _object_adjust_word_fields(memory, frame, 4294934854, 1, True)\n    if special and frame.status & 4 or (not special and frame.status & 8):\n        frame = _scene_rule_store_word_fields(memory, frame, 4294934854, 3)\nreturn frame'}})

DECLARATIONS.update({'adjust_selected_action_mode_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 259936)\nstate = memory.state\nframe = _movement_compare(state, frame, state.read(4294934747, 1), 3, 8)\nframe = _scene_rule_adjust_action_selection_fields(memory, frame, bool(frame.status & 4))\nframe = _movement_move(state, frame, 'target_x', state.read(4294934854, 2), 16)\nframe = first_replace(frame, roster=memory.cursor_at(260160))\nframe = _movement_move(state, frame, 'target_x', frame.roster.byte(low16(frame.target_x)), 8)\nframe = _movement_test(state, frame, state.read(4294934852, 2), 16)\nif frame.status & 4:\n    frame = _movement_add_word(state, frame, 'target_x', 4)\nframe = _scene_render_asl_word(memory, frame, 'target_x', low16(frame.target_x), 1)\nframe = first_replace(frame, roster=memory.cursor_at(4294934826))\nframe, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934819, 0)\nif pressed:\n    address = frame.roster.address(low16(frame.target_x))\n    frame = _object_adjust_word_fields(memory, frame, address, 1)\n    frame = _movement_compare(state, frame, state.read(4294934880, 2), 11, 16)\n    fewer = bool(frame.status & 1)\n    frame = _movement_compare(state, frame, frame.roster.word(low16(frame.target_x)), 6, 16)\n    if fewer and (not frame.status & 1) or (not fewer and (not frame.status & 5)):\n        frame = _scene_rule_store_word_fields(memory, frame, address, 0, True)\nframe, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934819, 1)\nif pressed:\n    address = frame.roster.address(low16(frame.target_x))\n    frame = _object_adjust_word_fields(memory, frame, address, 1, True)\n    if frame.status & 8:\n        frame = _scene_rule_store_word_fields(memory, frame, address, 6)\n        frame = _movement_compare(state, frame, state.read(4294934880, 2), 11, 16)\n        if frame.status & 1:\n            frame = _scene_rule_store_word_fields(memory, frame, address, 5)\nreturn memory.sync_status(frame)"}})

DECLARATIONS.update({'commit_scene_battle_totals_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'from .business_actions import sum_live_object_rosters_fields\nframe = _scene_rule_frame_fields(memory, frame, 260316)\ndef child(actual, entered):\n    return sum_live_object_rosters_fields(SceneRefreshMemory(actual.state), entered)\nframe = _presentation_call_fields(BattlePresentationMemory(memory.state), frame, 260320, child)\nframe = _scene_rule_store_word_fields(memory, frame, 4294934808, low16(frame.target_y))\nframe = _scene_rule_store_word_fields(memory, frame, 4294934810, low16(frame.unit))\nframe = _scene_rule_store_word_fields(memory, frame, 4294934796, memory.state.read(4294934904, 2))\nreturn _scene_rule_store_word_fields(memory, frame, 4294934798, memory.state.read(4294935160, 2))'}})

APPROVED.setdefault('business_early_phase',set()).update({'_scene_rule_frame_fields','_scene_rule_store_word_fields','_scene_rule_input_bit_fields','_scene_rule_summary_fields'})
APPROVED.setdefault('business_actions',set()).add('sum_live_object_rosters_fields')
APPROVED.setdefault((2,'high_level_main_flows.business_movement_support'),set()).update({'_movement_move','_movement_move_long','_movement_compare','_movement_test','_movement_add_word','_movement_divu_word'})

DECLARATIONS.update({'draw_two_prompt_backgrounds': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 256738)\nreturned = draw_two_prompt_backgrounds_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'begin_transition_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 257926)\nreturned = begin_transition_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'update_action_mode_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 257930)\nreturned = update_action_mode_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'dismiss_action_mode_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258096)\nreturned = dismiss_action_mode_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'begin_duel_handoff_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258146)\nreturned = begin_duel_handoff_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'confirm_duel_handoff_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258150)\nreturned = confirm_duel_handoff_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'commit_duel_handoff': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258270)\nreturned = commit_duel_handoff_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'await_duel_handoff_palette': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258154)\nreturned = await_duel_handoff_palette_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'finish_duel_handoff_phase': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258158)\nreturned = finish_duel_handoff_phase_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'await_result_palette': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258546)\nreturned = await_result_palette_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'finish_result_phase': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258550)\nreturned = finish_result_phase_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'await_secondary_result_palette': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258724)\nreturned = await_secondary_result_palette_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'await_primary_result_palette': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258906)\nreturned = await_primary_result_palette_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'begin_result_confirmation_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258538)\nreturned = begin_result_confirmation_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'confirm_result_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258542)\nreturned = confirm_result_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'begin_secondary_confirmation_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258716)\nreturned = begin_secondary_confirmation_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'confirm_secondary_result_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258720)\nreturned = confirm_secondary_result_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'finish_secondary_result_phase': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258728)\nreturned = finish_secondary_result_phase_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'begin_primary_confirmation_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258894)\nreturned = begin_primary_confirmation_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'replace_primary_confirmation_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258898)\nreturned = replace_primary_confirmation_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'confirm_primary_result_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258902)\nreturned = confirm_primary_result_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'finish_primary_result_phase': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 258910)\nreturned = finish_primary_result_phase_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'adjust_primary_formation': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 259778)\nreturned = adjust_primary_formation_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'deploy_primary_formation': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 259822)\nreturned = deploy_primary_formation_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'draw_secondary_squad_budget': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 260342)\nreturned = draw_secondary_squad_budget_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'draw_squad_class_budgets': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 260414)\nreturned = draw_squad_class_budgets_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'draw_battle_summary_numbers': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 261726)\nreturned = draw_battle_summary_numbers_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'draw_blinking_decimal_panel': {'signature': 'state: SceneState, context: DigitPanelContext', 'returns': 'DigitPanelResult', 'flow': 'context.validate(state)\nactual = _phase_legacy_fields(state, context.frame, 261962)\nactual = first_replace(actual, roster=context.source)\nreturned = draw_blinking_decimal_panel_fields(SceneRefreshMemory(state), actual)\nreturn DigitPanelResult(returned.roster, _phase_legacy_projection(state, context.frame, returned)).validate(state)'}})

DECLARATIONS.update({'draw_decimal_panel': {'signature': 'state: SceneState, context: DigitPanelContext', 'returns': 'DigitPanelResult', 'flow': 'context.validate(state)\nactual = _phase_legacy_fields(state, context.frame, 261998)\nactual = first_replace(actual, roster=context.source)\nreturned = draw_decimal_panel_fields(SceneRefreshMemory(state), actual)\nreturn DigitPanelResult(returned.roster, _phase_legacy_projection(state, context.frame, returned)).validate(state)'}})

DECLARATIONS.update({'draw_both_force_status_panels': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 260550)\nreturned = draw_both_force_status_panels_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'draw_normal_force_status_panel': {'signature': 'state: SceneState, context: ForcePanelContext', 'returns': 'PhaseFrame', 'flow': 'context.validate(state)\nactual = _phase_legacy_fields(state, context.frame, 260658)\nactual = first_replace(actual, auxiliary=context.leader.cursor())\nreturned = draw_normal_force_status_panel_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, context.frame, returned)'}})

DECLARATIONS.update({'draw_special_force_status_panel': {'signature': 'state: SceneState, context: ForcePanelContext', 'returns': 'PhaseFrame', 'flow': 'context.validate(state)\nactual = _phase_legacy_fields(state, context.frame, 261414)\nactual = first_replace(actual, auxiliary=context.leader.cursor())\nreturned = draw_special_force_status_panel_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, context.frame, returned)'}})

DECLARATIONS.update({'selected_action_mode_view': {'signature': 'state: SceneState', 'returns': 'Table', 'flow': 'checked_state(state)\nactual = FirstDeploymentFrame.unobserved()\nreturned = selected_action_mode_view_fields(SceneRefreshMemory(state), actual)\nreturn state.table_at(returned.roster.base)'}})

DECLARATIONS.update({'lookup_action_mode_icon_pair': {'signature': 'state: SceneState, context: ActionIconContext', 'returns': 'PhaseFrame', 'flow': 'context.validate(state)\nactual = _phase_legacy_fields(state, context.frame, 261304)\nactual = first_replace(actual, unit=context.mode)\nreturned = lookup_action_mode_icon_pair_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, context.frame, returned)'}})

DECLARATIONS.update({'draw_two_prompt_backgrounds_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 256738)\nframe = _allocation_decode_panel_fields(memory, frame, 282357, 51584, 10, 256770)\nreturn _allocation_decode_panel_fields(memory, frame, 282776, 51648, 10, 256802)'}})

DECLARATIONS.update({'_allocation_begin_result_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, role', 'returns': 'FirstDeploymentFrame', 'flow': "script, token, active, reset = {'transition': (242540, 258014, False, False), 'handoff': (242782, 258242, True, False), 'result': (242824, 258634, True, False), 'secondary': (242810, 258812, True, False), 'primary': (242846, 259000, True, True)}[role]\nframe = _allocation_status_fields(memory, frame, 9984)\nif reset:\n    frame = _allocation_store_fields(memory, frame, 33046, 0)\nframe = _allocation_fill_fields(memory, frame, 1610612738, 13107, 3455, True)\nframe = _allocation_script_fields(memory, frame, script)\nframe = _allocation_call_fields(memory, frame, 256738, token)\nframe = _allocation_status_fields(memory, frame, 9472)\nframe = _allocation_adjust_ram_fields(memory, frame, 33084)\nreturn _allocation_store_fields(memory, frame, 33086, 1) if active else frame"}})

DECLARATIONS.update({'begin_transition_prompt_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 257926)\nreturn _allocation_begin_result_fields(memory, frame, 'transition')"}})

DECLARATIONS.update({'begin_duel_handoff_prompt_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 258146)\nreturn _allocation_begin_result_fields(memory, frame, 'handoff')"}})

DECLARATIONS.update({'begin_result_confirmation_prompt_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 258538)\nreturn _allocation_begin_result_fields(memory, frame, 'result')"}})

DECLARATIONS.update({'begin_secondary_confirmation_prompt_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 258716)\nreturn _allocation_begin_result_fields(memory, frame, 'secondary')"}})

DECLARATIONS.update({'begin_primary_confirmation_prompt_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 258894)\nreturn _allocation_begin_result_fields(memory, frame, 'primary')"}})

DECLARATIONS.update({'_allocation_dismiss_result_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, token: Long', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _allocation_call_fields(memory, frame, 262940, token)\nframe = _allocation_store_fields(memory, frame, 33082, 0)\nframe = _allocation_store_fields(memory, frame, 33084, 6)\nreturn _allocation_store_fields(memory, frame, 33086, 0, clear=True)'}})

DECLARATIONS.update({'update_action_mode_prompt_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 257930)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 33054)\nframe = _allocation_test_ram_fields(memory, frame, 33092)\nif not frame.status & 4:\n    frame = _allocation_ram_move_fields(memory, frame, 'target_x', 33056)\nframe = _allocation_store_fields(memory, frame, 33058, low16(frame.target_x))\nframe = _allocation_call_fields(memory, frame, 259936, 258046)\nframe = _allocation_call_fields(memory, frame, 260550, 258050)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 33058)\nframe = _allocation_mask_fields(memory, frame, 'target_x', 240, 8)\nreturn _allocation_dismiss_result_fields(memory, frame, 258064) if not frame.status & 4 else frame"}})

DECLARATIONS.update({'dismiss_action_mode_prompt_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 258096)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 33053, 8)\nframe = _allocation_mask_fields(memory, frame, 'target_x', 240, 8)\nreturn _allocation_dismiss_result_fields(memory, frame, 258114) if not frame.status & 4 else frame"}})

DECLARATIONS.update({'confirm_duel_handoff_prompt_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 258150)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 33053, 8)\nframe = _allocation_mask_fields(memory, frame, 'target_x', 240, 8)\nreturn commit_duel_handoff_fields(memory, frame) if not frame.status & 4 else frame"}})

DECLARATIONS.update({'commit_duel_handoff_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 258270)\nframe = _allocation_call_fields(memory, frame, 260316, 258274)\nframe = _allocation_link_clear_fields(memory, frame)\nframe = _allocation_call_fields(memory, frame, 240184, 258304)\nframe = _allocation_adjust_ram_fields(memory, frame, 33084)\nframe = _allocation_store_fields(memory, frame, 28914, 0, clear=True)\nframe = _allocation_store_fields(memory, frame, 28915, _allocation_read_fields(memory, frame, 4294934747, 1), 1)\nframe = _allocation_test_ram_fields(memory, frame, 33060)\nreversed_sides = not bool(frame.status & 4)\npairs = ((32990, 28784), (32994, 28778), (33400, 28780), (33030, 28782), (32988, 28864), (32992, 28858), (33144, 28860), (33028, 28862)) if reversed_sides else ((32988, 28784), (32992, 28778), (33144, 28780), (33028, 28782), (32990, 28864), (32994, 28858), (33400, 28860), (33030, 28862))\nfor source, destination in pairs:\n    frame = _allocation_store_fields(memory, frame, destination, _allocation_read_fields(memory, frame, 4294901760 | source, 2))\nframe = _allocation_move_fields(memory, frame, 'target_x', 0, 32)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32986, 8)\nframe = _scene_render_asl_word(memory, frame, 'target_x', low16(frame.target_x), 1)\ntable = memory.state.table_at(258500 if reversed_sides else 258410)\nreturn _allocation_store_fields(memory, frame, 28682, table.word(low16(frame.target_x)))"}})

DECLARATIONS.update({'await_duel_handoff_palette_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 258154)\nframe, finished = _scene_rule_input_bit_fields(memory, frame, 4294934724, 7)\nreturn _allocation_adjust_ram_fields(memory, frame, 33084) if finished else frame'}})

DECLARATIONS.update({'_allocation_confirm_result_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, role', 'returns': 'FirstDeploymentFrame', 'flow': "mask, preincrement, total_token, palette_token = {'result': (240, False, 258666, 258700), 'secondary': (240, True, 258848, 258878), 'primary': (32, True, 259134, 259164)}[role]\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 33053, 8)\nframe = _allocation_mask_fields(memory, frame, 'target_x', mask, 8)\nif frame.status & 4:\n    return frame\nif preincrement:\n    frame = _allocation_adjust_ram_fields(memory, frame, 33084)\nframe = _allocation_call_fields(memory, frame, 260316, total_token)\nif not preincrement:\n    frame = _allocation_adjust_ram_fields(memory, frame, 33084)\nframe = _allocation_link_clear_fields(memory, frame)\nreturn _allocation_call_fields(memory, frame, 240184, palette_token)"}})

DECLARATIONS.update({'confirm_result_prompt_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 258542)\nreturn _allocation_confirm_result_fields(memory, frame, 'result')"}})

DECLARATIONS.update({'confirm_secondary_result_prompt_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 258720)\nreturn _allocation_confirm_result_fields(memory, frame, 'secondary')"}})

DECLARATIONS.update({'confirm_primary_result_prompt_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 258902)\nreturn _allocation_confirm_result_fields(memory, frame, 'primary')"}})

DECLARATIONS.update({'replace_primary_confirmation_prompt_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 258898)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 33053, 8)\nframe = _allocation_mask_fields(memory, frame, 'target_x', 32, 8)\nif frame.status & 4:\n    return frame\nframe = _allocation_status_fields(memory, frame, 9984)\nframe = _allocation_fill_fields(memory, frame, 1610612738, 13107, 3455, True)\nframe = _allocation_script_fields(memory, frame, 242870)\nframe = _allocation_adjust_ram_fields(memory, frame, 33084)\nreturn _allocation_status_fields(memory, frame, 9472)"}})

DECLARATIONS.update({'adjust_primary_formation_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 259778)\nframe = adjust_scene_formation_choice_fields(memory, frame)\nreturn deploy_primary_formation_fields(memory, frame)'}})

DECLARATIONS.update({'deploy_primary_formation_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 259822)\nreturn deploy_scene_formation_fields(memory, frame, False)'}})

DECLARATIONS.update({'_allocation_number_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, low: Word, video: Word, count: Word, digit: Word, formatter_token: Long, panel_token: Long | None', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _allocation_move_fields(memory, frame, 'target_x', 0, 32)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', low)\nframe = _allocation_call_fields(memory, frame, 242392, formatter_token)\nframe = _allocation_move_fields(memory, frame, 'target_x', video)\nframe = _allocation_move_fields(memory, frame, 'count', count, 32)\nframe = first_replace(frame, roster=memory.cursor_at(4294934528 + digit))\nif panel_token is None:\n    return frame\nreturn _allocation_call_fields(memory, frame, 261998, panel_token)"}})

DECLARATIONS.update({'draw_secondary_squad_budget_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 260342)\nframe = _allocation_number_fields(memory, frame, 32998, 50094, 4, 1, 260352, 260366)\nframe = _allocation_number_fields(memory, frame, 33006, 50480, 3, 2, 260376, 260390)\nframe = _allocation_number_fields(memory, frame, 33002, 50868, 1, 4, 260400, None)\nreturn draw_blinking_decimal_panel_fields(memory, frame)'}})

DECLARATIONS.update({'draw_squad_class_budgets_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 260414)\nframe = _allocation_number_fields(memory, frame, 33002, 49580, 1, 4, 260424, 260438)\nplans = ((33018, 50092, 0, 260448, 260468, 260476), (33020, 50604, 1, 260486, 260508, 260516), (33022, 51116, 2, 260526, None, None))\nfor low, video, index, format_token, blink_token, normal_token in plans:\n    frame = _allocation_number_fields(memory, frame, low, video, 1, 4, format_token, None)\n    if index == 0:\n        frame = _allocation_test_ram_fields(memory, frame, 33092)\n    else:\n        frame = _allocation_compare_ram_fields(memory, frame, 33092, index)\n    blink = bool(frame.status & 4)\n    if blink_token is None:\n        return draw_blinking_decimal_panel_fields(memory, frame) if blink else draw_decimal_panel_fields(memory, frame)\n    frame = _allocation_call_fields(memory, frame, 261962 if blink else 261998, blink_token if blink else normal_token)\nreturn frame'}})

DECLARATIONS.update({'draw_blinking_decimal_panel_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 261962)\nframe, show = _scene_rule_input_bit_fields(memory, frame, 4294964001, 4)\nif show:\n    return draw_decimal_panel_fields(memory, frame)\nframe = _scene_refresh_emit(memory, frame, 12582916, 2, 36610)\nframe = _allocation_call_fields(memory, frame, 242352, 261982)\nframe = _allocation_move_fields(memory, frame, 'target_y', 50248)\nwhile True:\n    frame = _scene_refresh_emit(memory, frame, 12582912, 2, low16(frame.target_y))\n    frame, done = _allocation_dbword_fields(frame, 'count')\n    if done:\n        return frame"}})

DECLARATIONS.update({'draw_decimal_panel_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 261998)\nframe = _scene_refresh_emit(memory, frame, 12582916, 2, 36610)\nframe = _allocation_call_fields(memory, frame, 242352, 262010)\nframe = _allocation_move_fields(memory, frame, 'unit', 0, 32)\nwhile True:\n    frame = _allocation_move_fields(memory, frame, 'target_y', 0, 32)\n    value = frame.roster.byte()\n    frame = first_replace(frame, roster=frame.roster.advance(1))\n    frame = _allocation_move_fields(memory, frame, 'target_y', value, 8)\n    show = not bool(frame.status & 4)\n    if not show:\n        frame = _movement_test(memory.state, frame, low16(frame.unit), 16)\n        show = not bool(frame.status & 4)\n        if not show:\n            frame = _movement_test(memory.state, frame, low16(frame.count), 16)\n            show = bool(frame.status & 4)\n    if show:\n        frame = _allocation_move_fields(memory, frame, 'unit', 1, 32)\n        frame = _allocation_arithmetic_fields(memory, frame, 'target_y', 50272)\n    else:\n        frame = _allocation_move_fields(memory, frame, 'target_y', 50248)\n    frame = _scene_refresh_emit(memory, frame, 12582912, 2, low16(frame.target_y))\n    frame, done = _allocation_dbword_fields(frame, 'count')\n    if done:\n        return frame"}})

DECLARATIONS.update({'_allocation_sum_actor_rows_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, class_id: Word | None', 'returns': 'FirstDeploymentFrame', 'flow': "while True:\n    memory.sync_status(frame)\n    value = frame.auxiliary.byte()\n    frame = _scene_render_bit(memory, frame, value, 128)\n    if value & 128:\n        include = True\n        if class_id is not None:\n            member_class = frame.auxiliary.byte(1)\n            if class_id == 0:\n                frame = _movement_test(memory.state, frame, member_class, 8)\n            else:\n                frame = _movement_compare(memory.state, frame, member_class, class_id, 8)\n            include = bool(frame.status & 4)\n        if include:\n            frame = _allocation_arithmetic_fields(memory, frame, 'target_x', frame.auxiliary.word(14))\n    frame = first_replace(frame, auxiliary=frame.auxiliary.advance(16))\n    frame, done = _allocation_dbword_fields(frame, 'target_y')\n    if done:\n        return frame"}})

DECLARATIONS.update({'_allocation_total_display_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, video: Word, count: Word, digit: Word, formatter_token: Long, panel_token: Long | None, video_is_field: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _allocation_call_fields(memory, frame, 242392, formatter_token)\nif video_is_field:\n    video = _allocation_read_fields(memory, frame, 4294901760 | video, 2)\nframe = _allocation_move_fields(memory, frame, 'target_x', video)\nframe = _allocation_move_fields(memory, frame, 'count', count, 32)\nframe = first_replace(frame, roster=memory.cursor_at(4294934528 + digit))\nreturn draw_decimal_panel_fields(memory, frame) if panel_token is None else _allocation_call_fields(memory, frame, 261998, panel_token)"}})

DECLARATIONS.update({'draw_battle_summary_numbers_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 261726)\nfor low, video, format_token, panel_token in ((33142, 50592, 261736, 261750), (33158, 50976, 261760, 261774), (33398, 50610, 261784, 261798), (33414, 50994, 261808, 261822), (33024, 51360, 261832, 261846), (33026, 51378, 261856, 261870)):\n    frame = _allocation_number_fields(memory, frame, low, video, 2, 3, format_token, panel_token)\nfor base, video, format_token, panel_token in ((4294934906, 51740, 261902, 261916), (4294935162, 51758, 261948, None)):\n    frame = _allocation_move_fields(memory, frame, 'target_y', 14)\n    frame = _allocation_move_fields(memory, frame, 'target_x', 0, 32)\n    frame = first_replace(frame, auxiliary=memory.cursor_at(base))\n    frame = _allocation_sum_actor_rows_fields(memory, frame, None)\n    frame = _allocation_total_display_fields(memory, frame, video, 4, 1, format_token, panel_token)\nreturn frame"}})

DECLARATIONS.update({'selected_action_mode_view_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 261288)\nframe = first_replace(frame, roster=memory.cursor_at(4294934834))\nframe = _allocation_test_ram_fields(memory, frame, 33092)\nreturn first_replace(frame, roster=memory.cursor_at(4294934826)) if not frame.status & 4 else frame'}})

DECLARATIONS.update({'lookup_action_mode_icon_pair_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 261304)\nframe = _scene_render_asl_word(memory, frame, 'unit', low16(frame.unit), 2)\nframe = _allocation_move_fields(memory, frame, 'target_x', memory.state.table_at(261316).word(low16(frame.unit)))\nreturn _allocation_move_fields(memory, frame, 'target_y', memory.state.table_at(261318).word(low16(frame.unit)))"}})

DECLARATIONS.update({'_allocation_icon_pair_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, plan: tuple', 'returns': 'FirstDeploymentFrame', 'flow': "low, offset, index, mode_offset, top_token, blank_token, bottom_token, view_top, icon_top, view_bottom, icon_bottom = plan\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', low)\nif offset:\n    frame = _allocation_arithmetic_fields(memory, frame, 'target_x', offset)\nframe = _allocation_call_fields(memory, frame, 242352, top_token)\nif index == 0:\n    frame = _allocation_test_ram_fields(memory, frame, 33094)\nelse:\n    frame = _allocation_compare_ram_fields(memory, frame, 33094, index)\nblank = False\nif frame.status & 4:\n    frame, show = _scene_rule_input_bit_fields(memory, frame, 4294964001, 4)\n    blank = not show\nif blank:\n    frame = _scene_refresh_emit(memory, frame, 12582912, 2, 50248)\nelse:\n    frame = _allocation_call_fields(memory, frame, 261288, view_top)\n    frame = _allocation_move_fields(memory, frame, 'unit', frame.roster.word(mode_offset))\n    frame = _allocation_call_fields(memory, frame, 261304, icon_top)\n    frame = _scene_refresh_emit(memory, frame, 12582912, 2, low16(frame.target_x))\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', low)\nframe = _allocation_arithmetic_fields(memory, frame, 'target_x', offset + 128)\nframe = _allocation_call_fields(memory, frame, 242352, blank_token if blank else bottom_token)\nif blank:\n    return _scene_refresh_emit(memory, frame, 12582912, 2, 50248)\nframe = _allocation_call_fields(memory, frame, 261288, view_bottom)\nframe = _allocation_move_fields(memory, frame, 'unit', frame.roster.word(mode_offset))\nframe = _allocation_call_fields(memory, frame, 261304, icon_bottom)\nreturn _scene_refresh_emit(memory, frame, 12582912, 2, low16(frame.target_y))"}})

DECLARATIONS.update({'_allocation_selected_panel_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, low: Word', 'returns': 'tuple[FirstDeploymentFrame, bool]', 'flow': 'frame = _allocation_test_ram_fields(memory, frame, 33092)\nselected = bool(frame.status & 4)\nframe = _allocation_test_ram_fields(memory, frame, low)\nreturn (frame, bool(frame.status & 4) if selected else not bool(frame.status & 4))'}})

DECLARATIONS.update({'draw_normal_force_status_panel_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 260658)\nframe = _allocation_move_fields(memory, frame, 'target_x', 0, 32)\nframe = _allocation_move_fields(memory, frame, 'target_x', frame.auxiliary.word(14))\nframe = _allocation_total_display_fields(memory, frame, 32784, 2, 3, 260668, 260682, True)\nfor class_id, low, count, digit, format_token, panel_token in ((2, 32786, 3, 2, 260722, 260736), (1, 32788, 3, 2, 260776, 260790), (0, 32790, 4, 1, 260828, 260842)):\n    frame = _allocation_move_fields(memory, frame, 'target_y', 14)\n    frame = first_replace(frame, auxiliary=memory.cursor_at(_allocation_read_fields(memory, frame, 4294934556, 4)))\n    frame = _allocation_move_fields(memory, frame, 'target_x', 0, 32)\n    frame = _allocation_sum_actor_rows_fields(memory, frame, class_id)\n    frame = _allocation_total_display_fields(memory, frame, low, count, digit, format_token, panel_token, True)\nframe, selected = _allocation_selected_panel_fields(memory, frame, 32794)\nif not selected:\n    return frame\nframe = _scene_refresh_emit(memory, frame, 12582916, 2, 36610)\nfor plan in ((32792, 0, 0, 6, 260880, 260914, 260954, 260928, 260936, 260958, 260966), (32792, 16, 1, 4, 260984, 261020, 261060, 261034, 261042, 261064, 261072), (32792, 32, 2, 2, 261090, 261126, 261166, 261140, 261148, 261170, 261178), (32792, 50, 3, 0, 261196, 261232, 261270, 261246, 261252, 261274, 261280)):\n    frame = _allocation_icon_pair_fields(memory, frame, plan)\nreturn frame"}})

DECLARATIONS.update({'draw_special_force_status_panel_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 261414)\nframe = _allocation_move_fields(memory, frame, 'target_x', 0, 32)\nframe = _allocation_move_fields(memory, frame, 'target_x', frame.auxiliary.word(14))\nframe = _allocation_total_display_fields(memory, frame, 32784, 2, 3, 261424, 261438, True)\nframe = _allocation_move_fields(memory, frame, 'target_y', 14)\nframe = first_replace(frame, auxiliary=frame.auxiliary.advance(16))\nframe = _allocation_move_fields(memory, frame, 'target_x', 0, 32)\nframe = _allocation_sum_actor_rows_fields(memory, frame, 1)\nframe = _allocation_total_display_fields(memory, frame, 32786, 4, 1, 261478, 261492, True)\nframe, selected = _allocation_selected_panel_fields(memory, frame, 32792)\nif not selected:\n    return frame\nframe = _scene_refresh_emit(memory, frame, 12582916, 2, 36610)\nfor plan in ((32788, 0, 0, 6, 261530, 261564, 261604, 261578, 261586, 261608, 261616), (32790, 0, 2, 2, 261630, 261666, 261706, 261680, 261688, 261710, 261718)):\n    frame = _allocation_icon_pair_fields(memory, frame, plan)\nreturn frame"}})

DECLARATIONS.update({'_allocation_panel_setup_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, destinations: tuple, marker: Word, marker_low: Word, leader: Long, roster: Long | None', 'returns': 'FirstDeploymentFrame', 'flow': 'for low, value in zip((32784, 32786, 32788, 32790), destinations):\n    frame = _allocation_store_fields(memory, frame, low, value)\nif roster is not None:\n    frame = _allocation_store_fields(memory, frame, 32792, marker)\n    frame = _allocation_store_fields(memory, frame, marker_low, 0 if leader == 4294935146 else 1, clear=leader == 4294935146)\n    frame = _allocation_store_fields(memory, frame, 32796, roster, 4)\nelse:\n    frame = _allocation_store_fields(memory, frame, marker_low, marker, clear=marker == 0)\nreturn first_replace(frame, auxiliary=memory.cursor_at(leader))'}})

DECLARATIONS.update({'draw_both_force_status_panels_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 260550)\nframe = _allocation_compare_ram_fields(memory, frame, 32987, 3, 8)\nif not frame.status & 4:\n    frame = _allocation_panel_setup_fields(memory, frame, (50194, 50208, 50224, 50240), 50072, 32794, 4294935146, 4294935162)\n    frame = _allocation_call_fields(memory, frame, 260658, 260610)\n    frame = _allocation_panel_setup_fields(memory, frame, (49810, 49824, 49840, 49856), 49688, 32794, 4294934890, 4294934906)\n    return draw_normal_force_status_panel_fields(memory, frame)\nframe = _allocation_panel_setup_fields(memory, frame, (50334, 50352, 50212, 50234), 0, 32792, 4294935146, None)\nframe = _allocation_call_fields(memory, frame, 261414, 261380)\nframe = first_replace(frame, auxiliary=memory.cursor_at(4294934890))\nframe = _allocation_panel_setup_fields(memory, frame, (49950, 49968, 49828, 49850), 1, 32792, 4294934890, None)\nreturn draw_special_force_status_panel_fields(memory, frame)'}})

DECLARATIONS.update({'finish_duel_handoff_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _scene_rule_frame_fields(memory, frame, 258158)'}})

DECLARATIONS.update({'await_result_palette_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 258546)\nreturn await_duel_handoff_palette_fields(memory, frame)'}})

DECLARATIONS.update({'finish_result_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _scene_rule_frame_fields(memory, frame, 258550)'}})

DECLARATIONS.update({'await_secondary_result_palette_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 258724)\nreturn await_duel_handoff_palette_fields(memory, frame)'}})

DECLARATIONS.update({'await_primary_result_palette_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 258906)\nreturn await_duel_handoff_palette_fields(memory, frame)'}})

DECLARATIONS.update({'finish_secondary_result_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _scene_rule_frame_fields(memory, frame, 258728)'}})

DECLARATIONS.update({'finish_primary_result_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _scene_rule_frame_fields(memory, frame, 258910)'}})

# Only unreachable selected legacy tails; every surviving function still has its whole DECL.
DECLARATIONS.pop('_await_palette')
DECLARATIONS.pop('_begin_prompt')
DECLARATIONS.pop('_blank_video_words')
DECLARATIONS.pop('_clear_action_links')
DECLARATIONS.pop('_clear_object_labels')
DECLARATIONS.pop('_confirm_result')
DECLARATIONS.pop('_decode_plane')
DECLARATIONS.pop('_dismiss_prompt')
DECLARATIONS.pop('_icon_address')
DECLARATIONS.pop('_icon_pair')
DECLARATIONS.pop('_icon_word')
DECLARATIONS.pop('_lighten_after_confirmation')
DECLARATIONS.pop('_number_panel')
DECLARATIONS.pop('_panel_configuration')
DECLARATIONS.pop('_sum_active_roster')
DECLARATIONS.pop('_update_action_ai')
DECLARATIONS.pop('_upload_officer_label')
DECLARATIONS.pop('_with_scene_views')

APPROVED.setdefault('business_early_phase',set()).update(('_allocation_adjust_ram_fields', '_allocation_arithmetic_fields', '_allocation_call_fields', '_allocation_compare_ram_fields', '_allocation_dbword_fields', '_allocation_decode_panel_fields', '_allocation_fill_fields', '_allocation_link_clear_fields', '_allocation_mask_fields', '_allocation_move_fields', '_allocation_ram_move_fields', '_allocation_read_fields', '_allocation_script_fields', '_allocation_status_fields', '_allocation_store_fields', '_allocation_test_ram_fields', '_phase_legacy_fields', '_phase_legacy_projection'))

DECLARATIONS.update({'draw_two_prompt_backgrounds': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 256738)\nreturned = draw_two_prompt_backgrounds_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'begin_transition_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 257926)\nreturned = begin_transition_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'begin_duel_handoff_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258146)\nreturned = begin_duel_handoff_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'begin_result_confirmation_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258538)\nreturned = begin_result_confirmation_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'begin_secondary_confirmation_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258716)\nreturned = begin_secondary_confirmation_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'begin_primary_confirmation_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258894)\nreturned = begin_primary_confirmation_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'update_action_mode_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 257930)\nreturned = update_action_mode_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'dismiss_action_mode_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258096)\nreturned = dismiss_action_mode_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'confirm_duel_handoff_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258150)\nreturned = confirm_duel_handoff_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'commit_duel_handoff': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258270)\nreturned = commit_duel_handoff_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'await_duel_handoff_palette': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258154)\nreturned = await_duel_handoff_palette_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'await_result_palette': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258546)\nreturned = await_result_palette_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'await_secondary_result_palette': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258724)\nreturned = await_secondary_result_palette_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'await_primary_result_palette': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258906)\nreturned = await_primary_result_palette_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'finish_duel_handoff_phase': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258158)\nreturned = finish_duel_handoff_phase_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'finish_result_phase': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258550)\nreturned = finish_result_phase_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'finish_secondary_result_phase': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258728)\nreturned = finish_secondary_result_phase_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'finish_primary_result_phase': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258910)\nreturned = finish_primary_result_phase_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'confirm_result_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258542)\nreturned = confirm_result_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'confirm_secondary_result_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258720)\nreturned = confirm_secondary_result_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'confirm_primary_result_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258902)\nreturned = confirm_primary_result_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'replace_primary_confirmation_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 258898)\nreturned = replace_primary_confirmation_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'adjust_primary_formation': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 259778)\nreturned = adjust_primary_formation_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'deploy_primary_formation': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 259822)\nreturned = deploy_primary_formation_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'draw_decimal_panel': {'signature': 'state: SceneState, context: DigitPanelContext', 'returns': 'DigitPanelResult', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\ncontext.validate(state)\nactual = _phase_legacy_fields(state, context.frame, 261998)\nactual = first_replace(actual, roster=context.source)\nreturned = draw_decimal_panel_fields(SceneRefreshMemory(state), actual)\nreturn DigitPanelResult(returned.roster, _phase_legacy_projection(state, context.frame, returned)).validate(state)'}})

DECLARATIONS.update({'draw_blinking_decimal_panel': {'signature': 'state: SceneState, context: DigitPanelContext', 'returns': 'DigitPanelResult', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\ncontext.validate(state)\nactual = _phase_legacy_fields(state, context.frame, 261962)\nactual = first_replace(actual, roster=context.source)\nreturned = draw_blinking_decimal_panel_fields(SceneRefreshMemory(state), actual)\nreturn DigitPanelResult(returned.roster, _phase_legacy_projection(state, context.frame, returned)).validate(state)'}})

DECLARATIONS.update({'draw_secondary_squad_budget': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 260342)\nreturned = draw_secondary_squad_budget_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'draw_squad_class_budgets': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 260414)\nreturned = draw_squad_class_budgets_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'draw_battle_summary_numbers': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 261726)\nreturned = draw_battle_summary_numbers_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'lookup_action_mode_icon_pair': {'signature': 'state: SceneState, context: ActionIconContext', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\ncontext.validate(state)\nactual = _phase_legacy_fields(state, context.frame, 261304)\nactual = first_replace(actual, unit=context.mode)\nreturned = lookup_action_mode_icon_pair_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, context.frame, returned)'}})

DECLARATIONS.update({'draw_normal_force_status_panel': {'signature': 'state: SceneState, context: ForcePanelContext', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\ncontext.validate(state)\nactual = _phase_legacy_fields(state, context.frame, 260658)\nactual = first_replace(actual, auxiliary=context.leader.cursor())\nreturned = draw_normal_force_status_panel_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, context.frame, returned)'}})

DECLARATIONS.update({'draw_special_force_status_panel': {'signature': 'state: SceneState, context: ForcePanelContext', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\ncontext.validate(state)\nactual = _phase_legacy_fields(state, context.frame, 261414)\nactual = first_replace(actual, auxiliary=context.leader.cursor())\nreturned = draw_special_force_status_panel_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, context.frame, returned)'}})

DECLARATIONS.update({'draw_both_force_status_panels': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nactual = _phase_legacy_fields(state, frame, 260550)\nreturned = draw_both_force_status_panels_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

# Handoff full-field DECL: retain actual two absolute LONG addresses.
DECLARATIONS.update({'commit_duel_handoff_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 258270)\nframe = _allocation_call_fields(memory, frame, 260316, 258274)\nframe = _allocation_link_clear_fields(memory, frame)\nframe = _allocation_call_fields(memory, frame, 240184, 258304)\nframe = _allocation_adjust_ram_fields(memory, frame, 33084)\nframe = _object_clear_word_fields(memory, frame, 16740594)\nframe = _scene_refresh_emit(memory, frame, 16740595, 1, _allocation_read_fields(memory, frame, 4294934747, 1))\nframe = _allocation_test_ram_fields(memory, frame, 33060)\nreversed_sides = not bool(frame.status & 4)\npairs = ((32990, 28784), (32994, 28778), (33400, 28780), (33030, 28782), (32988, 28864), (32992, 28858), (33144, 28860), (33028, 28862)) if reversed_sides else ((32988, 28784), (32992, 28778), (33144, 28780), (33028, 28782), (32990, 28864), (32994, 28858), (33400, 28860), (33030, 28862))\nfor source, destination in pairs:\n    frame = _allocation_store_fields(memory, frame, destination, _allocation_read_fields(memory, frame, 4294901760 | source, 2))\nframe = _allocation_move_fields(memory, frame, 'target_x', 0, 32)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32986, 8)\nframe = _scene_render_asl_word(memory, frame, 'target_x', low16(frame.target_x), 1)\ntable = memory.state.table_at(258500 if reversed_sides else 258410)\nreturn _allocation_store_fields(memory, frame, 28682, table.word(low16(frame.target_x)))"}})

# Whole handoff DECL: both real absolute-LONG copy destinations/final selectors.
DECLARATIONS.update({'commit_duel_handoff_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 258270)\nframe = _allocation_call_fields(memory, frame, 260316, 258274)\nframe = _allocation_link_clear_fields(memory, frame)\nframe = _allocation_call_fields(memory, frame, 240184, 258304)\nframe = _allocation_adjust_ram_fields(memory, frame, 33084)\nframe = _object_clear_word_fields(memory, frame, 16740594)\nframe = _scene_refresh_emit(memory, frame, 16740595, 1, _allocation_read_fields(memory, frame, 4294934747, 1))\nframe = _allocation_test_ram_fields(memory, frame, 33060)\nreversed_sides = not bool(frame.status & 4)\npairs = ((32990, 28784), (32994, 28778), (33400, 28780), (33030, 28782), (32988, 28864), (32992, 28858), (33144, 28860), (33028, 28862)) if reversed_sides else ((32988, 28784), (32992, 28778), (33144, 28780), (33028, 28782), (32990, 28864), (32994, 28858), (33400, 28860), (33030, 28862))\nfor source, destination in pairs:\n    frame = _scene_refresh_emit(memory, frame, 16711680 | destination, 2, _allocation_read_fields(memory, frame, 4294901760 | source, 2))\nframe = _allocation_move_fields(memory, frame, 'target_x', 0, 32)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32986, 8)\nframe = _scene_render_asl_word(memory, frame, 'target_x', low16(frame.target_x), 1)\ntable = memory.state.table_at(258500 if reversed_sides else 258410)\nreturn _scene_refresh_emit(memory, frame, 16740362, 2, table.word(low16(frame.target_x)))"}})

# B120 finite late-allocation SceneFrame callees; no lowerer or role changes.
APPROVED.setdefault('business_actions',set()).add('upload_object_officer_name_frame_fields')
APPROVED.setdefault((2,'high_level_scene_flows.business_scene'),set()).add('read_vdp_plane_rle_rows_from_control_fields')
