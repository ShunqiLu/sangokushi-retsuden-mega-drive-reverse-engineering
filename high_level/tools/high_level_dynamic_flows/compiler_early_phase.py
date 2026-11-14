"""Restricted semantic source admission with ordinary mnemonic lowering.

Explicit business text only; this is an intermediate structural compiler,
not arbitrary Python compilation or full natural-gameplay acceptance.
"""
from .compiler_common import CompileError,semantic_functions,lower_declared
from .target import EARLY_PHASE_BINDINGS

APPROVED={None: {'business_late_phase'},
 'business_actions': {'upload_portrait_tiles', 'upload_object_officer_name', 'upload_object_officer_name_frame_fields'},
 'business_late_phase': {'latch_scene_controller_inputs', 'dispatch_late_substate'},
 'contexts_actions': {'DuelGlyphContext'},
 'contexts_early_phase': {'DecimalDigitsResult',
                          'PhaseFrame',
                          'SceneControllerConditions',
                          'SceneControllerFrame',
                          'SceneControllerOutcome',
                          'checked_phase',
                          'phase_add_word',
                          'phase_bit',
                          'phase_compare',
                          'phase_controller_return',
                          'phase_enter_call',
                          'phase_finish_call',
                          'phase_from_controller',
                          'phase_logic',
                          'phase_operands',
                          'phase_shifted_selector'},
 'dataclasses': {'replace'},
 'domain': {'Boundary',
            'Cursor',
            'Long',
            'SceneState',
            'VideoPlaneAddress',
            'Word',
            'checked_cursor',
            'checked_state',
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
              'advance_scene_palette_fade',
              'append_unclipped_scene_sprites',
              'clear_scene_object_label_plane',
              'enqueue_sound_command',
              'initialize_scene_object_roster_after_mode_check',
              'read_vdp_plane_rle_rows_from_control',
              'sample_random_preserving_seed_carrier',
              'set_vram_write_address'}}

DECLARATIONS={'_ram': {'signature': 'state, low',
          'returns': None,
          'flow': "return ram_view(state, 'ram_' + low)"},
 '_word': {'signature': 'state, low',
           'returns': None,
           'flow': 'return _ram(state, low).word()'},
 '_put': {'signature': 'state, low, value',
          'returns': None,
          'flow': '_ram(state, low).set_word(0, u16(value))'},
 '_increment': {'signature': 'state, low',
                'returns': None,
                'flow': 'value = u16(_word(state, low) + 1)\n'
                        '_put(state, low, value)\n'
                        'return value'},
 '_video_fill': {'signature': 'state, command, value, counter, frame=None',
                 'returns': None,
                 'flow': 'state.mmio_write(12582916, 4, command)\n'
                         'for _ in range(counter + 1):\n'
                         '    state.mmio_write(12582912, 2, value)\n'
                         'if frame is None:\n'
                         '    return None\n'
                         'frame = phase_operands(frame, phase_logic(value), '
                         'glyph_tokens=replace_word(frame.glyph_tokens, 65535))\n'
                         'if frame.live is not None:\n'
                         '    live = replace(frame.live, '
                         'row_count=replace_word(frame.live.row_count, value), '
                         'traversal=state.table(12582912).cursor())\n'
                         '    frame = phase_from_controller(state, live)\n'
                         'return frame'},
 '_clear_text': {'signature': 'state, frame=None',
                 'returns': None,
                 'flow': 'state.mmio_write(12582916, 2, 36610)\n'
                         'return _video_fill(state, 1610612738, 13107, 3455, frame)'},
 '_clear_background': {'signature': 'state',
                       'returns': None,
                       'flow': '_video_fill(state, 1073741827, 1024, 1215)'},
 '_script': {'signature': 'state, source, frame=None',
             'returns': None,
             'flow': 'state.write(16740364, 2, 40960)\n'
                     'state.write(16740366, 4, source)\n'
                     'state.write(16740372, 2, 3)\n'
                     'state.write(16740374, 2, 1)\n'
                     'return None if frame is None else phase_operands(frame, '
                     'phase_logic(1))'},
 '_load_panel': {'signature': 'state, source, frame=None',
                 'returns': None,
                 'flow': "_put(state, '8000', 32768)\n"
                         'if frame is not None and frame.live is not None:\n'
                         '    live = replace(phase_controller_return(state, frame), '
                         'source=state.table(source).cursor(), '
                         'destination=VideoPlaneAddress(49152), extent=128, '
                         'row_count=replace_word(frame.live.row_count, 18))\n'
                         '    called = phase_enter_call(state, live, 255154)\n'
                         '    result = state.service_at(240334, called)\n'
                         '    if type(result) is not SceneControllerFrame:\n'
                         "        raise Boundary('3AACE panel decoder requires its actual "
                         "complete frame return')\n"
                         '    result.validate(state)\n'
                         '    return phase_from_controller(state, phase_finish_call(state, '
                         'result, 255154))\n'
                         'return read_vdp_plane_rle_rows_from_control(state, '
                         'state.table(source).cursor(), VideoPlaneAddress(49152), 128, 18)'},
 '_late': {'signature': 'state, frame, name, continuation=None',
           'returns': None,
           'flow': 'from . import business_late_phase\n'
                   'callee = getattr(business_late_phase, name)\n'
                   'if frame.live is None:\n'
                   '    return callee(state, frame)\n'
                   'if continuation is None:\n'
                   "    raise Boundary('complete phase needs the actual known internal call "
                   "continuation')\n"
                   'current = phase_controller_return(state, frame)\n'
                   'actual = callee(state, phase_from_controller(state, '
                   'phase_enter_call(state, current, continuation)))\n'
                   'if type(actual) is SceneControllerOutcome:\n'
                   '    return actual.validate(state)\n'
                   'returned = phase_controller_return(state, actual)\n'
                   'return phase_from_controller(state, phase_finish_call(state, returned, '
                   'continuation))'},
 '_phase_vector': {'signature': 'state, frame, gather, base',
                   'returns': None,
                   'flow': 'if frame.live is not None:\n'
                           '    continuation = u32(base - 10)\n'
                           '    called = phase_enter_call(state, frame.live, continuation)\n'
                           '    frame = gather(state, phase_from_controller(state, called))\n'
                           '    actual = phase_controller_return(state, frame)\n'
                           '    frame = phase_from_controller(state, phase_finish_call(state, '
                           'actual, continuation))\n'
                           'else:\n'
                           '    frame = gather(state, frame)\n'
                           "selector = _word(state, '813c')\n"
                           'shifted, conditions = phase_shifted_selector(selector)\n'
                           'command = replace_word(frame.video_command, shifted)\n'
                           'frame = phase_operands(frame, conditions, video_command=command)\n'
                           'slot = u32(base + s16(low16(command)))\n'
                           'if frame.live is not None:\n'
                           '    return _complete_phase_substate(state, frame, slot)\n'
                           'early = {253176: initialize_early_scene, 253180: '
                           'process_early_scene_choice, 253184: present_early_scene_prompt, '
                           '253188: finish_early_scene_prompt, 253192: '
                           'wait_early_scene_choice, 253196: finish_early_scene_fade, 253200: '
                           'finish_alternate_scene_fade, 255084: '
                           'wait_exchange_scene_transition, 255088: '
                           'process_exchange_scene_choice, 255092: '
                           'finish_exchange_scene_transition, 255522: '
                           'process_pair_phase_counter, 255526: confirm_pair_allocation, '
                           '255530: update_pair_allocation_input, 255534: '
                           'exit_pair_allocation, 256256: wait_pair_stage_motion, 256260: '
                           'advance_pair_stage_motion, 256264: '
                           'confirm_second_pair_allocation, 256268: '
                           'present_pair_stage_summary}\n'
                           'if slot in early:\n'
                           '    return early[slot](state, frame)\n'
                           'if slot in (256272, 256276, 256280, 256284):\n'
                           '    from . import business_late_phase\n'
                           '    handler = {256272: '
                           'business_late_phase.adjust_secondary_formation_scene, 256276: '
                           'business_late_phase.confirm_secondary_formation_scene, 256280: '
                           'business_late_phase.update_active_battle_controls, 256284: '
                           'business_late_phase.latch_scene_controller_inputs}[slot]\n'
                           '    return handler(state, frame)\n'
                           'from .business_late_phase import dispatch_late_substate\n'
                           'return dispatch_late_substate(state, frame, slot)'},
 '_complete_phase_substate': {'signature': 'state, frame, slot',
                              'returns': None,
                              'flow': 'handlers = {256256: wait_pair_stage_motion, 256260: '
                                      'advance_pair_stage_motion, 255522: '
                                      'process_pair_phase_counter, 255084: '
                                      'wait_exchange_scene_transition, 255092: '
                                      'finish_exchange_scene_transition}\n'
                                      'if slot in handlers:\n'
                                      '    return handlers[slot](state, frame)\n'
                                      'from .business_late_phase import '
                                      'dispatch_late_substate\n'
                                      'return dispatch_late_substate(state, frame, slot)'},
 '_late_inputs': {'signature': 'state, frame',
                  'returns': None,
                  'flow': 'from .business_late_phase import latch_scene_controller_inputs\n'
                          'return latch_scene_controller_inputs(state, frame)'},
 '_leave_early_prompt': {'signature': 'state, frame',
                         'returns': None,
                         'flow': "_put(state, '813a', 0)\n"
                                 "_put(state, '813c', 6)\n"
                                 "_put(state, '814c', 0)\n"
                                 'clear_scene_object_label_plane(state)\n'
                                 'return frame'},
 '_prepare_scene_actor_arrival': {'signature': 'state, frame',
                                  'returns': None,
                                  'flow': 'rendered = '
                                          'initialize_scene_object_roster_after_mode_check(state, '
                                          'SceneRenderFrame(frame.video_command, '
                                          'frame.foreground, frame.mode, frame.row_count, '
                                          'frame.tile))\n'
                                          'return replace(frame, video_command=rendered.x, '
                                          'foreground=rendered.y, mode=rendered.attributes, '
                                          'row_count=rendered.palette, tile=rendered.tile)'},
 '_upload_object_officer_name': {'signature': 'state, frame',
                                 'returns': None,
                                 'flow': 'from .business_actions import '
                                         'upload_object_officer_name\n'
                                         'from .contexts_actions import DuelGlyphContext\n'
                                         'glyphs = DuelGlyphContext(frame.video_command, '
                                         'frame.foreground, frame.row_count)\n'
                                         'result = upload_object_officer_name(state, '
                                         'frame.glyph_tokens, glyphs)\n'
                                         'return replace(frame, '
                                         'video_command=result.tile_counter, '
                                         'foreground=result.glyphs.foreground, '
                                         'row_count=result.glyphs.remaining, '
                                         'glyph_tokens=result.officer_offset)'},
 '_upload_portrait_tiles': {'signature': 'state, frame',
                            'returns': None,
                            'flow': 'from .business_actions import upload_portrait_tiles\n'
                                    'outcome = upload_portrait_tiles(state, '
                                    'SceneRenderFrame(frame.video_command, frame.foreground, '
                                    'frame.mode, frame.row_count, frame.tile))\n'
                                    'return replace(frame, video_command=outcome.frame.x, '
                                    'foreground=outcome.frame.y, '
                                    'mode=outcome.frame.attributes, '
                                    'row_count=outcome.frame.palette, '
                                    'tile=outcome.frame.tile)'},
 'begin_scene_palette_lighten': {'signature': 'state: SceneState, value: Long',
                                 'returns': 'Long',
                                 'flow': 'checked_state(state)\n'
                                         'uint(value, 32)\n'
                                         "period = _word(state, '80c4')\n"
                                         'if not negative_word(period):\n'
                                         '    period &= 65280\n'
                                         '    if period == 256:\n'
                                         '        return value\n'
                                         '    restore_scene_palette(state)\n'
                                         'value = replace_word(value, low16(value) & 255 | '
                                         '256)\n'
                                         "_put(state, '80c4', low16(value))\n"
                                         "_put(state, '80c6', 0)\n"
                                         "_put(state, '80c8', 0)\n"
                                         'snapshot_scene_palette(state)\n'
                                         'return advance_scene_palette_fade(state, value)'},
 'snapshot_scene_palette': {'signature': 'state: SceneState',
                            'returns': 'None',
                            'flow': 'checked_state(state)\n'
                                    "source, destination = (_ram(state, 'fb00').cursor(), "
                                    "_ram(state, 'fb80').cursor())\n"
                                    'for _ in range(32):\n'
                                    '    destination.append_long(source.next_long())'},
 'restore_scene_palette': {'signature': 'state: SceneState',
                           'returns': 'None',
                           'flow': 'checked_state(state)\n'
                                   "source, destination = (_ram(state, 'fb80').cursor(), "
                                   "_ram(state, 'fb00').cursor())\n"
                                   'for _ in range(32):\n'
                                   '    destination.append_long(source.next_long())\n'
                                   "_put(state, '80c4', 65535)"},
 'append_decimal_digit': {'signature': 'state: SceneState, value: Long, divisor: Word, '
                                       'destination: Cursor',
                          'returns': 'DecimalDigitsResult',
                          'flow': 'checked_state(state)\n'
                                  'uint(value, 32)\n'
                                  'uint(divisor, 16)\n'
                                  'checked_cursor(destination, state)\n'
                                  'value = divu_retained(value, divisor)\n'
                                  'destination.append_byte(low8(value))\n'
                                  'value = swap_words(replace_word(value, 0))\n'
                                  'return DecimalDigitsResult(value, destination)'},
 'encode_six_decimal_digits': {'signature': 'state: SceneState, value: Long',
                               'returns': 'DecimalDigitsResult',
                               'flow': 'checked_state(state)\n'
                                       'uint(value, 32)\n'
                                       "destination = _ram(state, '8000').cursor()\n"
                                       'digit = 0\n'
                                       'while True:\n'
                                       '    borrowed = value < 100000\n'
                                       '    value = u32(value - 100000)\n'
                                       '    if borrowed:\n'
                                       '        break\n'
                                       '    digit = u16(digit + 1)\n'
                                       'value = u32(value + 100000)\n'
                                       'destination.append_byte(low8(digit))\n'
                                       'for divisor in (10000, 1000, 100, 10):\n'
                                       '    result = append_decimal_digit(state, value, '
                                       'divisor, destination)\n'
                                       '    value, destination = (result.value, '
                                       'result.destination)\n'
                                       'destination.append_byte(low8(value))\n'
                                       'return DecimalDigitsResult(value, destination)'},
 'adjust_scene_scroll': {'signature': 'state: SceneState, frame: PhaseFrame',
                         'returns': 'PhaseFrame',
                         'flow': 'checked_phase(state, frame)\n'
                                 "selected = bool(_ram(state, '811c').byte() & 1)\n"
                                 'frame = phase_operands(frame, phase_bit(frame, selected))\n'
                                 'if selected:\n'
                                 "    position = _word(state, '8020')\n"
                                 '    frame = phase_operands(frame, phase_logic(position))\n'
                                 '    if position != 0:\n'
                                 "        _put(state, '8026', _word(state, '8026') - 2)\n"
                                 "        previous = _word(state, '8020')\n"
                                 "        _put(state, '8020', previous - 2)\n"
                                 '        frame = phase_operands(frame, '
                                 'phase_compare(previous, 2))\n'
                                 "selected = bool(_ram(state, '811c').byte() & 2)\n"
                                 'frame = phase_operands(frame, phase_bit(frame, selected))\n'
                                 'if selected:\n'
                                 "    position = _word(state, '8020')\n"
                                 '    frame = phase_operands(frame, phase_compare(position, '
                                 '144))\n'
                                 '    if position < 144:\n'
                                 "        _put(state, '8026', _word(state, '8026') + 2)\n"
                                 "        previous = _word(state, '8020')\n"
                                 "        _put(state, '8020', previous + 2)\n"
                                 '        frame = phase_operands(frame, '
                                 'phase_add_word(previous, 2))\n'
                                 'return frame'},
 'step_main_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame',
                           'returns': 'PhaseFrame',
                           'flow': 'checked_phase(state, frame)\n'
                                   'return _phase_vector(state, frame, _late_inputs, 256256)'},
 'step_result_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame',
                             'returns': 'PhaseFrame',
                             'flow': 'checked_phase(state, frame)\n'
                                     'return _phase_vector(state, frame, _late_inputs, '
                                     '257926)'},
 'step_confirmation_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame',
                                   'returns': 'PhaseFrame',
                                   'flow': 'checked_phase(state, frame)\n'
                                           'return _phase_vector(state, frame, _late_inputs, '
                                           '258096)'},
 'step_transfer_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame',
                               'returns': 'PhaseFrame',
                               'flow': 'checked_phase(state, frame)\n'
                                       'return _phase_vector(state, frame, _late_inputs, '
                                       '258146)'},
 'step_primary_detail_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame',
                                     'returns': 'PhaseFrame',
                                     'flow': 'checked_phase(state, frame)\n'
                                             'return _phase_vector(state, frame, '
                                             '_late_inputs, 258538)'},
 'step_secondary_detail_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame',
                                       'returns': 'PhaseFrame',
                                       'flow': 'checked_phase(state, frame)\n'
                                               'return _phase_vector(state, frame, '
                                               '_late_inputs, 258716)'},
 'step_summary_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame',
                              'returns': 'PhaseFrame',
                              'flow': 'checked_phase(state, frame)\n'
                                      'return _phase_vector(state, frame, _late_inputs, '
                                      '258894)'},
 'step_pair_transition_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame',
                                      'returns': 'PhaseFrame',
                                      'flow': 'checked_phase(state, frame)\n'
                                              'return _phase_vector(state, frame, '
                                              'gather_early_scene_input, 255522)'},
 'step_initial_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame',
                              'returns': 'PhaseFrame',
                              'flow': 'checked_phase(state, frame)\n'
                                      'return _phase_vector(state, frame, _late_inputs, '
                                      '253176)'},
 'step_exchange_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame',
                               'returns': 'PhaseFrame',
                               'flow': 'checked_phase(state, frame)\n'
                                       'return _phase_vector(state, frame, '
                                       'gather_early_scene_input, 255084)'},
 '_initialize_early_panel': {'signature': 'state, frame, script, substate, active, use_actor',
                             'returns': None,
                             'flow': 'state.set_status_word(9984)\n'
                                     '_load_panel(state, 283548)\n'
                                     "_put(state, '8116', active)\n"
                                     '_clear_text(state)\n'
                                     '_script(state, script)\n'
                                     'if substate is not None:\n'
                                     "    _put(state, '813c', substate)\n"
                                     'frame = _late(state, frame, '
                                     "'draw_two_prompt_backgrounds')\n"
                                     'if use_actor:\n'
                                     '    actor = replace_word(frame.video_command, '
                                     "_word(state, '80e0'))\n"
                                     '    foreground = replace_word(frame.foreground, 1152)\n'
                                     '    frame = replace(frame, video_command=actor, '
                                     'foreground=foreground)\n'
                                     '    frame = _upload_portrait_tiles(state, frame)\n'
                                     'if substate is None:\n'
                                     "    _increment(state, '813c')\n"
                                     'state.set_status_word(9472)\n'
                                     'return frame'},
 'initialize_early_scene': {'signature': 'state: SceneState, frame: PhaseFrame',
                            'returns': 'PhaseFrame',
                            'flow': 'checked_phase(state, frame)\n'
                                    "if _ram(state, '80da').byte() != 0 and _ram(state, "
                                    "'80da').byte() != 3:\n"
                                    "    _ram(state, '80da').byte()\n"
                                    '    return _initialize_early_panel(state, frame, 242568, '
                                    'None, 1, False)\n'
                                    "flags = _ram(state, 'c700')\n"
                                    "first = _word(state, '80e0')\n"
                                    'primary = flags.byte(first) & 3\n'
                                    "second = _word(state, '80e2')\n"
                                    'secondary = flags.byte(second) & 3\n'
                                    'comparison = u16(u8(primary - secondary) + 1)\n'
                                    'suitable = comparison <= 2\n'
                                    'if suitable:\n'
                                    "    value = u16(_word(state, '810e') + 10)\n"
                                    "    suitable = value >= _word(state, '810c')\n"
                                    'if suitable:\n'
                                    "    value = u16(_word(state, '8106') + 20)\n"
                                    "    suitable = value >= _word(state, '8104')\n"
                                    'if suitable:\n'
                                    "    suitable = _word(state, '80e6') < _word(state, "
                                    "'80e4')\n"
                                    'if suitable:\n'
                                    '    sampled = '
                                    'sample_random_preserving_seed_carrier(state)\n'
                                    '    suitable = low16(sampled) & 3 == 0\n'
                                    '    frame = replace(frame, '
                                    'video_command=replace_word(sampled, low16(sampled) & '
                                    '3))\n'
                                    'if suitable:\n'
                                    '    return _initialize_early_panel(state, frame, 242750, '
                                    '4, 1, True)\n'
                                    'return _initialize_early_panel(state, frame, 242568, 1, '
                                    '1, False)'},
 '_early_contested_roll': {'signature': 'state, frame',
                           'returns': None,
                           'flow': "flags = _ram(state, 'c700')\n"
                                   "primary = _word(state, '80e0')\n"
                                   'primary = flags.byte(primary) & 3\n'
                                   'strength = u8(5 - primary)\n'
                                   "secondary = _word(state, '80e2')\n"
                                   'secondary = flags.byte(secondary)\n'
                                   'other = u8(5 - secondary)\n'
                                   'strength = u32(low16(u32(strength * _word(state, '
                                   "'8104'))) * 100)\n"
                                   'sampled = sample_random_preserving_seed_carrier(state)\n'
                                   'factor = u16((low16(sampled) & 31) + 20)\n'
                                   "factor = u16(factor + _word(state, '8106'))\n"
                                   'other = u32(other * factor)\n'
                                   'ratio = divu_retained(strength, low16(other))\n'
                                   'frame = replace(frame, '
                                   'video_command=replace_word(sampled, factor), '
                                   'foreground=ratio, mode=other)\n'
                                   'if low16(ratio) > 100:\n'
                                   '    return (True, frame)\n'
                                   'while True:\n'
                                   '    sampled = '
                                   'sample_random_preserving_seed_carrier(state)\n'
                                   '    random_percent = low16(sampled) & 127\n'
                                   '    frame = replace(frame, '
                                   'video_command=replace_word(sampled, random_percent))\n'
                                   '    if random_percent <= 100:\n'
                                   '        break\n'
                                   'if random_percent > low16(ratio):\n'
                                   '    return (False, frame)\n'
                                   'sampled = sample_random_preserving_seed_carrier(state)\n'
                                   "index = _word(state, 'efd2')\n"
                                   'mask = state.table(254082).byte(index)\n'
                                   'command = replace_byte(sampled, low8(sampled) & mask)\n'
                                   'frame = replace(frame, video_command=command, '
                                   'foreground=replace_word(frame.foreground, index))\n'
                                   'return (low8(command) == 0, frame)'},
 '_show_choice_result': {'signature': 'state, frame, accepted',
                         'returns': None,
                         'flow': "_put(state, '8142', 0 if accepted else 1)\n"
                                 '_clear_background(state)\n'
                                 'actor = replace_word(frame.video_command, _word(state, '
                                 "'80e0'))\n"
                                 'foreground = replace_word(frame.foreground, 1152)\n'
                                 'frame = replace(frame, video_command=actor, '
                                 'foreground=foreground)\n'
                                 'frame = _upload_portrait_tiles(state, frame)\n'
                                 'if accepted:\n'
                                 '    frame = paint_scene_number_rows(state, replace(frame, '
                                 'video_command=replace_word(frame.video_command, 49954)))\n'
                                 '_clear_text(state)\n'
                                 'state.write(16740364, 2, 40960)\n'
                                 'state.write(16740372, 2, 3)\n'
                                 'state.write(16740374, 2, 1)\n'
                                 "_increment(state, '813c')\n"
                                 'state.write(16740366, 4, 242680 if accepted else 242620)\n'
                                 "flags = _ram(state, 'c700')\n"
                                 "secondary = flags.byte(_word(state, '80e2')) & 3\n"
                                 "primary = flags.byte(_word(state, '80e0'))\n"
                                 'if accepted:\n'
                                 '    primary &= 3\n'
                                 'else:\n'
                                 '    secondary &= 3\n'
                                 'if secondary >= primary:\n'
                                 '    state.write(16740366, 4, 242602 if accepted else '
                                 '242654)\n'
                                 'state.set_status_word(9472)\n'
                                 'return frame'},
 'process_early_scene_choice': {'signature': 'state: SceneState, frame: PhaseFrame',
                                'returns': 'PhaseFrame',
                                'flow': 'checked_phase(state, frame)\n'
                                        "if not _ram(state, '811f').byte() & 32:\n"
                                        "    _put(state, '813c', 6)\n"
                                        '    return frame\n'
                                        'enqueue_sound_command(state, 172)\n'
                                        "if _word(state, '8142') != 0:\n"
                                        '    return _leave_early_prompt(state, frame)\n'
                                        "if _ram(state, '80da').byte() == 1 or _ram(state, "
                                        "'80da').byte() == 2:\n"
                                        '    return _initialize_early_panel(state, frame, '
                                        '242750, 3, 0, False)\n'
                                        'state.set_status_word(9984)\n'
                                        'accepted, frame = _early_contested_roll(state, '
                                        'frame)\n'
                                        'return _show_choice_result(state, frame, accepted)'},
 '_draw_fixed_prompt': {'signature': 'state, frame, pointer',
                        'returns': None,
                        'flow': 'render = SceneRenderFrame(frame.video_command, '
                                'frame.foreground, replace_word(frame.mode, 260), 0, '
                                'replace_word(frame.tile, 1024))\n'
                                'result = append_unclipped_scene_sprites(state, '
                                'state.table(pointer).cursor(), render)\n'
                                'return replace(frame, video_command=result.frame.x, '
                                'foreground=result.frame.y, mode=result.frame.attributes, '
                                'row_count=result.frame.palette, tile=result.frame.tile)'},
 'append_early_scene_instruction': {'signature': 'state: SceneState, frame: PhaseFrame',
                                    'returns': 'PhaseFrame',
                                    'flow': 'checked_phase(state, frame)\n'
                                            'return _draw_fixed_prompt(state, frame, 254870)'},
 'draw_early_scene_choice': {'signature': 'state: SceneState, frame: PhaseFrame',
                             'returns': 'PhaseFrame',
                             'flow': 'checked_phase(state, frame)\n'
                                     'toggled = replace_byte(frame.video_command, _ram(state, '
                                     "'811f').byte())\n"
                                     'toggled = replace_word(toggled, low16(toggled) & 3)\n'
                                     'if low16(toggled) != 0:\n'
                                     "    _put(state, '8142', _word(state, '8142') ^ 1)\n"
                                     'return _draw_choice_from_selection(state, '
                                     'replace(frame, video_command=toggled))'},
 '_draw_choice_from_selection': {'signature': 'state, frame',
                                 'returns': None,
                                 'flow': "offset = 56 if _word(state, '8142') == 0 else 72\n"
                                         'command = replace_word(frame.video_command, '
                                         "u16(offset + _word(state, '8020')))\n"
                                         'frame = replace(frame, video_command=command, '
                                         'foreground=replace_word(frame.foreground, 140))\n'
                                         'return _draw_fixed_prompt(state, frame, 254606)'},
 'present_early_scene_prompt': {'signature': 'state: SceneState, frame: PhaseFrame',
                                'returns': 'PhaseFrame',
                                'flow': 'checked_phase(state, frame)\n'
                                        "if _ram(state, '811f').byte() & 32:\n"
                                        "    if _word(state, '8142') != 0:\n"
                                        '        return _leave_early_prompt(state, frame)\n'
                                        '    frame = _late(state, frame, '
                                        "'commit_duel_handoff')\n"
                                        "    _put(state, '813a', 8)\n"
                                        "    _put(state, '813c', 5)\n"
                                        'frame = replace(frame, '
                                        'video_command=replace_word(frame.video_command, '
                                        "u16(_word(state, '8020') + 112)), "
                                        'foreground=replace_word(frame.foreground, 160))\n'
                                        'frame = append_early_scene_instruction(state, '
                                        'frame)\n'
                                        'return paint_scene_number_rows(state, replace(frame, '
                                        'video_command=replace_word(frame.video_command, '
                                        '49954)))'},
 'finish_early_scene_prompt': {'signature': 'state: SceneState, frame: PhaseFrame',
                               'returns': 'PhaseFrame',
                               'flow': 'checked_phase(state, frame)\n'
                                       "if _ram(state, '80da').byte() != 0 and _ram(state, "
                                       "'80da').byte() != 3:\n"
                                       "    _put(state, '811e', _word(state, '8120'))\n"
                                       'else:\n'
                                       '    frame = replace(frame, '
                                       'video_command=replace_word(frame.video_command, '
                                       "u16(_word(state, '8020') + 112)), "
                                       'foreground=replace_word(frame.foreground, 256))\n'
                                       '    frame = append_early_scene_instruction(state, '
                                       'frame)\n'
                                       '    frame = paint_scene_number_rows(state, '
                                       'replace(frame, '
                                       'video_command=replace_word(frame.video_command, '
                                       '49978)))\n'
                                       "if _ram(state, '811f').byte() & 32:\n"
                                       "    if _word(state, '8142') != 0:\n"
                                       '        return _leave_early_prompt(state, frame)\n'
                                       '    frame = _late(state, frame, '
                                       "'commit_duel_handoff')\n"
                                       "    _put(state, '813c', 6)\n"
                                       '    return frame\n'
                                       'return draw_early_scene_choice(state, frame)'},
 'wait_early_scene_choice': {'signature': 'state: SceneState, frame: PhaseFrame',
                             'returns': 'PhaseFrame',
                             'flow': 'checked_phase(state, frame)\n'
                                     'frame = replace(frame, '
                                     'video_command=replace_word(frame.video_command, '
                                     "u16(_word(state, '8020') + 112)), "
                                     'foreground=replace_word(frame.foreground, 256))\n'
                                     'frame = append_early_scene_instruction(state, frame)\n'
                                     'frame = paint_scene_number_rows(state, replace(frame, '
                                     'video_command=replace_word(frame.video_command, '
                                     '49978)))\n'
                                     'frame = draw_early_scene_choice(state, frame)\n'
                                     "if _increment(state, '8144') < 64:\n"
                                     '    return frame\n'
                                     'state.set_status_word(9984)\n'
                                     '_clear_text(state)\n'
                                     '_script(state, 242718)\n'
                                     "_put(state, '813c', 3)\n"
                                     'state.set_status_word(9472)\n'
                                     'return frame'},
 'finish_early_scene_fade': {'signature': 'state: SceneState, frame: PhaseFrame',
                             'returns': 'PhaseFrame',
                             'flow': 'checked_phase(state, frame)\n'
                                     'frame = replace(frame, '
                                     'video_command=replace_word(frame.video_command, '
                                     "u16(_word(state, '8020') + 112)), "
                                     'foreground=replace_word(frame.foreground, 160))\n'
                                     'frame = append_early_scene_instruction(state, frame)\n'
                                     "if _ram(state, '80c4').byte() & 128:\n"
                                     "    _put(state, '813a', 3)\n"
                                     "    _put(state, '813c', 3)\n"
                                     'return frame'},
 'finish_alternate_scene_fade': {'signature': 'state: SceneState, frame: PhaseFrame',
                                 'returns': 'PhaseFrame',
                                 'flow': 'checked_phase(state, frame)\n'
                                         "if _ram(state, '80da').byte() != 1 and _ram(state, "
                                         "'80da').byte() != 2:\n"
                                         '    frame = replace(frame, '
                                         'video_command=replace_word(frame.video_command, '
                                         "u16(_word(state, '8020') + 112)), "
                                         'foreground=replace_word(frame.foreground, 256))\n'
                                         '    frame = append_early_scene_instruction(state, '
                                         'frame)\n'
                                         "if _ram(state, '80c4').byte() & 128:\n"
                                         "    _put(state, '813a', 3)\n"
                                         "    _put(state, '813c', 3)\n"
                                         'return frame'},
 'paint_scene_number_row': {'signature': 'state: SceneState, frame: PhaseFrame',
                            'returns': 'PhaseFrame',
                            'flow': 'checked_phase(state, frame)\n'
                                    'state.mmio_write(12582916, 2, 36610)\n'
                                    'set_vram_write_address(state, '
                                    'VideoPlaneAddress(frame.video_command))\n'
                                    'for _ in range(6):\n'
                                    '    state.mmio_write(12582912, 2, 58461)\n'
                                    'return replace(frame, mode=65535)'},
 'paint_scene_number_rows': {'signature': 'state: SceneState, frame: PhaseFrame',
                             'returns': 'PhaseFrame',
                             'flow': 'checked_phase(state, frame)\n'
                                     'frame = replace(frame, foreground=7)\n'
                                     'for remaining in range(7, -1, -1):\n'
                                     '    frame = paint_scene_number_row(state, frame)\n'
                                     '    frame = replace(frame, '
                                     'video_command=replace_word(frame.video_command, '
                                     'u16(low16(frame.video_command) + 128)), '
                                     'foreground=replace_word(frame.foreground, remaining - 1 '
                                     '& 65535))\n'
                                     'return frame'},
 'wait_exchange_scene_transition': {'signature': 'state: SceneState, frame: PhaseFrame',
                                    'returns': 'PhaseFrame',
                                    'flow': 'checked_phase(state, frame)\n'
                                            "_increment(state, '8142')\n"
                                            "count = _word(state, '8142')\n"
                                            'frame = phase_operands(frame, '
                                            'phase_compare(count, 32))\n'
                                            'if count < 32:\n'
                                            '    return frame\n'
                                            'state.set_status_word(9984)\n'
                                            "_put(state, '8142', 0)\n"
                                            "_increment(state, '813c')\n"
                                            'if frame.live is not None:\n'
                                            '    frame = _load_panel(state, 284735, frame)\n'
                                            '    frame = _clear_text(state, frame)\n'
                                            '    frame = _script(state, 242886, frame)\n'
                                            'else:\n'
                                            '    _load_panel(state, 284735)\n'
                                            '    _clear_text(state)\n'
                                            '    _script(state, 242886)\n'
                                            "_put(state, '8116', 1)\n"
                                            'frame = _late(state, frame, '
                                            "'draw_two_prompt_backgrounds', 255236)\n"
                                            'state.set_status_word(9472)\n'
                                            'return phase_operands(frame, '
                                            'SceneControllerConditions(False, False, False, '
                                            'False))'},
 'process_exchange_scene_choice': {'signature': 'state: SceneState, frame: PhaseFrame',
                                   'returns': 'PhaseFrame',
                                   'flow': 'checked_phase(state, frame)\n'
                                           "if not _ram(state, '811d').byte() & 32:\n"
                                           '    toggled = replace_byte(frame.video_command, '
                                           "_ram(state, '811d').byte())\n"
                                           '    toggled = replace_word(toggled, '
                                           'low16(toggled) & 3)\n'
                                           '    if low16(toggled) != 0:\n'
                                           "        _put(state, '8142', _word(state, '8142') "
                                           '^ 1)\n'
                                           '    return _draw_choice_from_selection(state, '
                                           'replace(frame, video_command=toggled))\n'
                                           'enqueue_sound_command(state, 172)\n'
                                           "if _word(state, '8142') == 0:\n"
                                           "    _put(state, '8142', 0)\n"
                                           "    _put(state, '813a', 7)\n"
                                           "    _put(state, '813c', 0)\n"
                                           "    _put(state, '814c', 0)\n"
                                           '    clear_scene_object_label_plane(state)\n'
                                           "    _put(state, '840a', 0)\n"
                                           '    return frame\n'
                                           'state.set_status_word(9984)\n'
                                           "if _ram(state, '80da').byte() != 0 and "
                                           "_ram(state, '80da').byte() != 3:\n"
                                           '    frame = _prepare_scene_actor_arrival(state, '
                                           'frame)\n'
                                           'frame = exchange_scene_pair_fields(state, frame)\n'
                                           'frame = exchange_scene_actor_records(state, '
                                           'frame)\n'
                                           'frame = _prepare_scene_actor_arrival(state, '
                                           'frame)\n'
                                           "actor = _ram(state, '816a')\n"
                                           'for index in range(16):\n'
                                           '    offset = u16(index * 16)\n'
                                           '    actor.set_word(offset + 2, u16(352 - '
                                           'actor.word(offset + 2)))\n'
                                           '    actor.set_word(offset + 6, 1)\n'
                                           '    actor.set_word(offset + 8, 1)\n'
                                           'frame = exchange_scene_pair_fields(state, frame)\n'
                                           'frame = exchange_scene_actor_records(state, '
                                           'frame)\n'
                                           'clear_scene_object_label_plane(state)\n'
                                           "_put(state, '840a', 1)\n"
                                           "_put(state, '8142', 0)\n"
                                           "_put(state, '8020', 0)\n"
                                           "_put(state, '8024', 0)\n"
                                           "_put(state, '8040', 33280)\n"
                                           "_put(state, '803a', 33280)\n"
                                           "_increment(state, '813c')\n"
                                           'state.set_status_word(9472)\n'
                                           'return frame'},
 'finish_exchange_scene_transition': {'signature': 'state: SceneState, frame: PhaseFrame',
                                      'returns': 'PhaseFrame',
                                      'flow': 'checked_phase(state, frame)\n'
                                              "position = _word(state, '8020')\n"
                                              'frame = phase_operands(frame, '
                                              'phase_compare(position, 144))\n'
                                              'if position < 144:\n'
                                              '    return frame\n'
                                              "_put(state, '8040', 0)\n"
                                              "_put(state, '803a', 0)\n"
                                              "_increment(state, '8142')\n"
                                              "count = _word(state, '8142')\n"
                                              'frame = phase_operands(frame, '
                                              'phase_compare(count, 32))\n'
                                              'if count >= 32:\n'
                                              "    _put(state, '8142', 0)\n"
                                              "    _put(state, '813a', 8)\n"
                                              "    _put(state, '813c', 0)\n"
                                              "    _put(state, '814c', 0)\n"
                                              '    frame = phase_operands(frame, '
                                              'phase_logic(0))\n'
                                              'return frame'},
 'gather_early_scene_input': {'signature': 'state: SceneState, frame: PhaseFrame',
                              'returns': 'PhaseFrame',
                              'flow': 'checked_phase(state, frame)\n'
                                      "if _ram(state, '80da').byte() == 0:\n"
                                      "    _put(state, '811c', _word(state, 'f602'))\n"
                                      "    _put(state, '811e', _word(state, 'f602'))\n"
                                      "    _put(state, '8120', 0)\n"
                                      '    return phase_operands(frame, phase_logic(0))\n'
                                      "if _ram(state, '80da').byte() == 2:\n"
                                      '    command = replace_word(frame.video_command, '
                                      "_word(state, 'f602'))\n"
                                      '    command = replace_word(command, low16(command) | '
                                      "_word(state, 'f604'))\n"
                                      "    _put(state, '811c', low16(command))\n"
                                      "    _put(state, '811e', _word(state, 'f602'))\n"
                                      "    last = _word(state, 'f604')\n"
                                      "    _put(state, '8120', last)\n"
                                      '    return phase_operands(frame, phase_logic(last), '
                                      'video_command=command)\n'
                                      "if _ram(state, '80da').byte() == 3:\n"
                                      '    command = replace_word(frame.video_command, '
                                      "_word(state, 'f604'))\n"
                                      "    _put(state, '811c', low16(command))\n"
                                      "    _put(state, '811e', _word(state, 'f604'))\n"
                                      "    last = _word(state, 'f602')\n"
                                      "    _put(state, '8120', last)\n"
                                      '    return phase_operands(frame, phase_logic(last), '
                                      'video_command=command)\n'
                                      'command = replace_word(frame.video_command, '
                                      "_word(state, 'f602'))\n"
                                      'command = replace_word(command, low16(command) | '
                                      "_word(state, 'f604'))\n"
                                      "_put(state, '811c', low16(command))\n"
                                      "_put(state, '811e', _word(state, 'f604'))\n"
                                      "last = _word(state, 'f602')\n"
                                      "_put(state, '8120', last)\n"
                                      'return phase_operands(frame, phase_logic(last), '
                                      'video_command=command)'},
 'exchange_scene_pair_fields': {'signature': 'state: SceneState, frame: PhaseFrame',
                                'returns': 'PhaseFrame',
                                'flow': 'checked_phase(state, frame)\n'
                                        "for primary, secondary in (('80dc', '80de'), "
                                        "('80e0', '80e2'), ('80e4', '80e6'), ('80e8', "
                                        "'80ea'), ('80ec', '80ee'), ('80f0', '80f2'), "
                                        "('80f4', '80fa'), ('80f6', '80fc'), ('80f8', "
                                        "'80fe'), ('8100', '8102'), ('8104', '8106'), "
                                        "('8108', '810a'), ('810c', '810e'), ('8110', "
                                        "'8112')):\n"
                                        '    saved = _word(state, primary)\n'
                                        '    _put(state, primary, _word(state, secondary))\n'
                                        '    _put(state, secondary, saved)\n'
                                        '    frame = replace(frame, '
                                        'video_command=replace_word(frame.video_command, '
                                        'saved))\n'
                                        'return frame'},
 'exchange_scene_actor_records': {'signature': 'state: SceneState, frame: PhaseFrame',
                                  'returns': 'PhaseFrame',
                                  'flow': 'checked_phase(state, frame)\n'
                                          "first, second = (_ram(state, '816a').cursor(), "
                                          "_ram(state, '826a').cursor())\n"
                                          'value = frame.foreground\n'
                                          'for _ in range(128):\n'
                                          '    value = replace_word(value, first.word())\n'
                                          '    first.append_word(second.word())\n'
                                          '    second.append_word(low16(value))\n'
                                          'return replace(frame, '
                                          'video_command=replace_word(frame.video_command, '
                                          '65535), foreground=value)'},
 'refresh_primary_actor_summary': {'signature': 'state: SceneState, frame: PhaseFrame',
                                   'returns': 'PhaseFrame',
                                   'flow': 'checked_phase(state, frame)\n'
                                           'command = replace_word(frame.video_command, '
                                           "_word(state, '8106'))\n"
                                           'command = replace_word(command, '
                                           "u16(low16(command) + _word(state, '810a')))\n"
                                           "_put(state, '8176', low16(command))\n"
                                           "_put(state, '8178', _word(state, '810e'))\n"
                                           'return replace(frame, video_command=command)'},
 'process_pair_phase_counter': {'signature': 'state: SceneState, frame: PhaseFrame',
                                'returns': 'PhaseFrame',
                                'flow': 'checked_phase(state, frame)\n'
                                        "if _ram(state, '80da').byte() != 1 and _ram(state, "
                                        "'80da').byte() != 2:\n"
                                        "    _put(state, '813a', 0)\n"
                                        "    _put(state, '813c', 0)\n"
                                        '    return phase_operands(frame, phase_logic(0))\n'
                                        "_increment(state, '8142')\n"
                                        "count = _word(state, '8142')\n"
                                        'frame = phase_operands(frame, phase_compare(count, '
                                        '64))\n'
                                        'if count < 64:\n'
                                        '    return frame\n'
                                        'if frame.live is not None:\n'
                                        "    raise Boundary('3E6CC exchange/deployment path "
                                        "requires complete shared phase returns')\n"
                                        'frame = exchange_scene_pair_fields(state, frame)\n'
                                        "if _word(state, '80e6') == 0:\n"
                                        '    frame = refresh_primary_actor_summary(state, '
                                        'frame)\n'
                                        '    frame = _late(state, frame, '
                                        "'deploy_primary_formation')\n"
                                        '    return _exit_pair_allocation(state, frame)\n'
                                        'return _prepare_secondary_allocation_panel(state, '
                                        'frame)'},
 '_allocation_valid': {'signature': 'state',
                       'returns': None,
                       'flow': "command = _word(state, '80fa')\n"
                               "command = u16(command + _word(state, '80fc'))\n"
                               "command = u16(command + _word(state, '80fe'))\n"
                               "return command == _word(state, '80ea')"},
 '_allocate_actor_rows': {'signature': 'state, base, frame',
                          'returns': None,
                          'flow': "command = _word(state, '8106')\n"
                                  "percentage = u32(_word(state, '8102') * command)\n"
                                  'percentage = divu_retained(percentage, 100)\n'
                                  "extra = _word(state, '80f2')\n"
                                  'actor = _ram(state, base)\n'
                                  'for index in range(15):\n'
                                  '    offset = u16(index * 16)\n'
                                  '    actor.set_word(offset + 12, low16(percentage))\n'
                                  "    actor.set_word(offset + 14, _word(state, '80ee'))\n"
                                  '    if extra != 0:\n'
                                  '        extra = u16(extra - 1)\n'
                                  '        actor.set_word(offset + 14, u16(actor.word(offset '
                                  '+ 14) + 1))\n'
                                  'return replace(frame, '
                                  'video_command=replace_word(frame.video_command, 65535), '
                                  'foreground=percentage, mode=replace_word(frame.mode, '
                                  'extra))'},
 'confirm_pair_allocation': {'signature': 'state: SceneState, frame: PhaseFrame',
                             'returns': 'PhaseFrame',
                             'flow': 'checked_phase(state, frame)\n'
                                     "if not _ram(state, '811f').byte() & 32:\n"
                                     '    return _finish_allocation_frame(state, frame, '
                                     'False)\n'
                                     'enqueue_sound_command(state, 172)\n'
                                     "if _word(state, '8144') != 2 or not "
                                     '_allocation_valid(state):\n'
                                     '    return _finish_allocation_frame(state, frame, '
                                     'False)\n'
                                     'return _confirm_pair_allocation(state, frame)'},
 '_confirm_pair_allocation': {'signature': 'state, frame',
                              'returns': None,
                              'flow': "_increment(state, '813c')\n"
                                      'state.set_status_word(9984)\n'
                                      "frame = _allocate_actor_rows(state, '817a', frame)\n"
                                      'frame = refresh_primary_actor_summary(state, frame)\n'
                                      '_clear_background(state)\n'
                                      '_video_fill(state, 1610612738, 13107, 3455)\n'
                                      '_script(state, 242506)\n'
                                      'state.set_status_word(9472)\n'
                                      'return frame'},
 'update_pair_allocation_input': {'signature': 'state: SceneState, frame: PhaseFrame',
                                  'returns': 'PhaseFrame',
                                  'flow': 'checked_phase(state, frame)\n'
                                          'frame = _late(state, frame, '
                                          "'adjust_primary_formation')\n"
                                          'command = replace_byte(frame.video_command, '
                                          "_ram(state, '811f').byte())\n"
                                          'command = replace_word(command, low16(command) & '
                                          '12)\n'
                                          'frame = replace(frame, video_command=command)\n'
                                          'if low16(command) != 0:\n'
                                          '    clear_scene_object_label_plane(state)\n'
                                          'return frame'},
 'exit_pair_allocation': {'signature': 'state: SceneState, frame: PhaseFrame',
                          'returns': 'PhaseFrame',
                          'flow': 'checked_phase(state, frame)\n'
                                  "if _ram(state, '811f').byte() & 32:\n"
                                  '    return _exit_pair_allocation(state, frame)\n'
                                  'return frame'},
 '_exit_pair_allocation': {'signature': 'state, frame',
                           'returns': None,
                           'flow': "_put(state, '813a', 0)\n"
                                   "_put(state, '813c', 0)\n"
                                   "_put(state, '814c', 0)\n"
                                   'clear_scene_object_label_plane(state)\n'
                                   'frame = exchange_scene_pair_fields(state, frame)\n'
                                   "_put(state, '8142', 0)\n"
                                   "_put(state, '8144', 0)\n"
                                   "_put(state, '8146', 0)\n"
                                   'return frame'},
 'wait_pair_stage_motion': {'signature': 'state: SceneState, frame: PhaseFrame',
                            'returns': 'PhaseFrame',
                            'flow': 'checked_phase(state, frame)\n'
                                    "_increment(state, '8142')\n"
                                    "count = _word(state, '8142')\n"
                                    'frame = phase_operands(frame, phase_compare(count, 64))\n'
                                    'if count >= 64:\n'
                                    "    _put(state, '8142', 0)\n"
                                    "    _put(state, '8020', 0)\n"
                                    "    _put(state, '8024', 0)\n"
                                    "    _put(state, '8040', 33280)\n"
                                    "    _put(state, '803a', 33280)\n"
                                    "    changed = _increment(state, '813c')\n"
                                    '    frame = phase_operands(frame, '
                                    'phase_add_word(u16(changed - 1), 1))\n'
                                    'return frame'},
 'advance_pair_stage_motion': {'signature': 'state: SceneState, frame: PhaseFrame',
                               'returns': 'PhaseFrame',
                               'flow': 'checked_phase(state, frame)\n'
                                       "position = _word(state, '8020')\n"
                                       'frame = phase_operands(frame, phase_compare(position, '
                                       '144))\n'
                                       'if position < 144:\n'
                                       '    return frame\n'
                                       "_put(state, '8040', 0)\n"
                                       "_put(state, '803a', 0)\n"
                                       "_increment(state, '8142')\n"
                                       "count = _word(state, '8142')\n"
                                       'frame = phase_operands(frame, phase_compare(count, '
                                       '32))\n'
                                       'if count < 32:\n'
                                       '    return frame\n'
                                       'if frame.live is not None:\n'
                                       "    raise Boundary('3E9DE allocation path still "
                                       "requires complete shared presentation returns')\n"
                                       "if _word(state, '80e6') == 0:\n"
                                       "    for field in ('80ea', '80ee', '80f2', '80fa', "
                                       "'80fc', '80fe', '8142'):\n"
                                       '        _put(state, field, 0)\n'
                                       '    frame = _late(state, frame, '
                                       "'update_secondary_scene_totals')\n"
                                       '    frame = _late(state, frame, '
                                       "'deploy_secondary_formation')\n"
                                       "    _put(state, '813a', 8)\n"
                                       "    _put(state, '813c', 0)\n"
                                       "    _put(state, '814c', 0)\n"
                                       '    clear_scene_object_label_plane(state)\n'
                                       '    return frame\n'
                                       'return _prepare_secondary_allocation_panel(state, '
                                       'frame)'},
 '_prepare_secondary_allocation_panel': {'signature': 'state, frame',
                                         'returns': None,
                                         'flow': 'state.set_status_word(9984)\n'
                                                 "_put(state, '8142', 0)\n"
                                                 "_increment(state, '813c')\n"
                                                 'frame = _late(state, frame, '
                                                 "'normalize_secondary_squad_size')\n"
                                                 '_video_fill(state, 1342177282, 13107, 191)\n'
                                                 'state.mmio_write(12582916, 4, 1342177282)\n'
                                                 'tokens = replace_word(frame.glyph_tokens, '
                                                 "_word(state, '80e2'))\n"
                                                 'frame = replace(frame, '
                                                 'video_command=replace_word(frame.video_command, '
                                                 '3), '
                                                 'foreground=replace_word(frame.foreground, '
                                                 '1), glyph_tokens=tokens)\n'
                                                 'frame = _upload_object_officer_name(state, '
                                                 'frame)\n'
                                                 '_load_panel(state, 281711)\n'
                                                 'frame = _late(state, frame, '
                                                 "'draw_secondary_squad_budget')\n"
                                                 '_clear_text(state)\n'
                                                 '_script(state, 242464)\n'
                                                 "_put(state, '8116', 1)\n"
                                                 'frame = _late(state, frame, '
                                                 "'draw_two_prompt_backgrounds')\n"
                                                 'state.set_status_word(9472)\n'
                                                 'return frame'},
 '_finish_allocation_frame': {'signature': 'state, frame, secondary',
                              'returns': None,
                              'flow': 'frame = _late(state, frame, '
                                      "'adjust_selected_squad_class_counts')\n"
                                      'return _late(state, frame, '
                                      "'draw_squad_class_budgets')"},
 'present_pair_stage_summary': {'signature': 'state: SceneState, frame: PhaseFrame',
                                'returns': 'PhaseFrame',
                                'flow': 'checked_phase(state, frame)\n'
                                        'frame = _late(state, frame, '
                                        "'adjust_secondary_squad_count')\n"
                                        'frame = _late(state, frame, '
                                        "'normalize_secondary_squad_size')\n"
                                        'frame = _late(state, frame, '
                                        "'draw_secondary_squad_budget')\n"
                                        "if not _ram(state, '811f').byte() & 32:\n"
                                        '    return frame\n'
                                        'enqueue_sound_command(state, 172)\n'
                                        "_increment(state, '813c')\n"
                                        "_put(state, '8144', 0)\n"
                                        "if _ram(state, '80db').byte() == 3:\n"
                                        "    _put(state, '80fa', 0)\n"
                                        "    _put(state, '80fc', _word(state, '80ea'))\n"
                                        "    _put(state, '80fe', 0)\n"
                                        "    if _word(state, '813a') == 7:\n"
                                        '        return _confirm_pair_allocation(state, '
                                        'frame)\n'
                                        '    return _confirm_second_pair_allocation(state, '
                                        'frame)\n'
                                        'state.set_status_word(9984)\n'
                                        '_load_panel(state, 282054)\n'
                                        'frame = _late(state, frame, '
                                        "'draw_squad_class_budgets')\n"
                                        '_clear_text(state)\n'
                                        '_script(state, 242486)\n'
                                        'state.set_status_word(9472)\n'
                                        'return frame'},
 'confirm_second_pair_allocation': {'signature': 'state: SceneState, frame: PhaseFrame',
                                    'returns': 'PhaseFrame',
                                    'flow': 'checked_phase(state, frame)\n'
                                            "if not _ram(state, '811f').byte() & 32:\n"
                                            '    return _finish_allocation_frame(state, '
                                            'frame, True)\n'
                                            'enqueue_sound_command(state, 172)\n'
                                            "if _word(state, '8144') != 2 or not "
                                            '_allocation_valid(state):\n'
                                            '    return _finish_allocation_frame(state, '
                                            'frame, True)\n'
                                            'return _confirm_second_pair_allocation(state, '
                                            'frame)'},
 '_confirm_second_pair_allocation': {'signature': 'state, frame',
                                     'returns': None,
                                     'flow': 'state.set_status_word(9984)\n'
                                             "frame = _allocate_actor_rows(state, '827a', "
                                             'frame)\n'
                                             'frame = _late(state, frame, '
                                             "'update_secondary_scene_totals')\n"
                                             "_increment(state, '813c')\n"
                                             '_clear_background(state)\n'
                                             '_video_fill(state, 1610612738, 13107, 3455)\n'
                                             '_script(state, 242506)\n'
                                             'state.set_status_word(9472)\n'
                                             'return frame'}}

def _lower_begin_scene_palette_lighten(emitter,rules):
    emitter.segment(0x3aa38,0x3aa78)
    emitter.ins('move.w','0x80c4:w,%d1',4)
    emitter.ins('bmi.w','scene_pc_03aa5a',4)
    emitter.ins('andi.w','#0xff00,%d1',4)
    emitter.ins('cmpi.w','#0x100,%d1',4)
    emitter.ins('beq.w','scene_pc_03a9b8',4)
    emitter.ins('movem.l','%d0,-(%a7)',4)
    emitter.ins('jsr','76(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('movem.l','(%a7)+,%d0',4)
    emitter.ins('andi.w','#0xff,%d0',4)
    emitter.ins('ori.w','#0x100,%d0',4)
    emitter.ins('move.w','%d0,0x80c4:w',4)
    emitter.ins('move.w','#0x0,0x80c6:w',6)
    emitter.ins('move.w','#0x0,0x80c8:w',6)
    emitter.ins('bsr.b','scene_pc_03aa78',2)
    emitter.ins('jmp','-254(%pc)',4)

def _lower_snapshot_scene_palette(emitter,rules):
    emitter.segment(0x3aa78,0x3aa8a)
    emitter.ins('moveq','#31,%d1',2)
    emitter.ins('lea.l','0xfb00:w,%a0',4)
    emitter.ins('lea.l','0xfb80:w,%a1',4)
    emitter.ins('move.l','(%a0)+,(%a1)+',2)
    emitter.ins('dbra','%d1,scene_pc_03aa82',4)
    emitter.ins('rts','',2)

def _lower_restore_scene_palette(emitter,rules):
    emitter.segment(0x3aa9e,0x3aab6)
    emitter.ins('moveq','#31,%d1',2)
    emitter.ins('lea.l','0xfb00:w,%a1',4)
    emitter.ins('lea.l','0xfb80:w,%a0',4)
    emitter.ins('move.l','(%a0)+,(%a1)+',2)
    emitter.ins('dbra','%d1,scene_pc_03aaa8',4)
    emitter.ins('move.w','#0xffff,0x80c4:w',6)
    emitter.ins('rts','',2)

def _lower_encode_six_decimal_digits(emitter,rules):
    emitter.segment(0x3b2d8,0x3b316)
    emitter.ins('clr.w','%d2',2)
    emitter.ins('lea.l','0x8000:w,%a0',4)
    emitter.ins('subi.l','#0x186a0,%d0',6)
    emitter.ins('bcs.b','scene_pc_03b2ea',2)
    emitter.ins('addq.w','#0x1,%d2',2)
    emitter.ins('bra.b','scene_pc_03b2de',2)
    emitter.ins('addi.l','#0x186a0,%d0',6)
    emitter.ins('move.b','%d2,(%a0)+',2)
    emitter.ins('move.w','#0x2710,%d2',4)
    emitter.ins('bsr.w','scene_pc_03b316',4)
    emitter.ins('move.w','#0x3e8,%d2',4)
    emitter.ins('bsr.w','scene_pc_03b316',4)
    emitter.ins('move.w','#0x64,%d2',4)
    emitter.ins('bsr.w','scene_pc_03b316',4)
    emitter.ins('move.w','#0xa,%d2',4)
    emitter.ins('bsr.w','scene_pc_03b316',4)
    emitter.ins('move.b','%d0,(%a0)+',2)
    emitter.ins('rts','',2)

def _lower_append_decimal_digit(emitter,rules):
    emitter.segment(0x3b316,0x3b320)
    emitter.ins('divu.w','%d2,%d0',2)
    emitter.ins('move.b','%d0,(%a0)+',2)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('swap','%d0',2)
    emitter.ins('rts','',2)

def _lower_adjust_scene_scroll(emitter,rules):
    emitter.segment(0x3d970,0x3d9a0)
    emitter.ins('btst.b','#0x0,0x811c:w',6)
    emitter.ins('beq.b','scene_pc_03d986',2)
    emitter.ins('tst.w','0x8020:w',4)
    emitter.ins('beq.b','scene_pc_03d986',2)
    emitter.ins('subq.w','#0x2,0x8026:w',4)
    emitter.ins('subq.w','#0x2,0x8020:w',4)
    emitter.ins('btst.b','#0x1,0x811c:w',6)
    emitter.ins('beq.b','scene_pc_03d99e',2)
    emitter.ins('cmpi.w','#0x90,0x8020:w',6)
    emitter.ins('bcc.b','scene_pc_03d99e',2)
    emitter.ins('addq.w','#0x2,0x8026:w',4)
    emitter.ins('addq.w','#0x2,0x8020:w',4)
    emitter.ins('rts','',2)

def _lower_step_main_scene_phase(emitter,rules):
    emitter.segment(0x3dcc2,0x3dcc6)
    emitter.ins('bra.w','scene_pc_03e8f2',4)
    emitter.segment(0x3e8f2,0x3e900)
    emitter.ins('bsr.w','scene_pc_03e91c',4)
    emitter.ins('move.w','0x813c:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('jmp','2(%pc, %d0.w)',4)

def _lower_step_result_scene_phase(emitter,rules):
    emitter.segment(0x3dcc6,0x3dcca)
    emitter.ins('bra.w','scene_pc_03ef78',4)
    emitter.segment(0x3ef78,0x3ef86)
    emitter.ins('bsr.w','scene_pc_03e91c',4)
    emitter.ins('move.w','0x813c:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('jmp','2(%pc, %d0.w)',4)

def _lower_step_confirmation_scene_phase(emitter,rules):
    emitter.segment(0x3dcca,0x3dcce)
    emitter.ins('bra.w','scene_pc_03f022',4)
    emitter.segment(0x3f022,0x3f030)
    emitter.ins('bsr.w','scene_pc_03e91c',4)
    emitter.ins('move.w','0x813c:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('jmp','2(%pc, %d0.w)',4)

def _lower_step_transfer_scene_phase(emitter,rules):
    emitter.segment(0x3dcce,0x3dcd2)
    emitter.ins('bra.w','scene_pc_03f054',4)
    emitter.segment(0x3f054,0x3f062)
    emitter.ins('bsr.w','scene_pc_03e91c',4)
    emitter.ins('move.w','0x813c:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('jmp','2(%pc, %d0.w)',4)

def _lower_step_primary_detail_scene_phase(emitter,rules):
    emitter.segment(0x3dcd2,0x3dcd6)
    emitter.ins('bra.w','scene_pc_03f1dc',4)
    emitter.segment(0x3f1dc,0x3f1ea)
    emitter.ins('bsr.w','scene_pc_03e91c',4)
    emitter.ins('move.w','0x813c:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('jmp','2(%pc, %d0.w)',4)

def _lower_step_secondary_detail_scene_phase(emitter,rules):
    emitter.segment(0x3dcd6,0x3dcda)
    emitter.ins('bra.w','scene_pc_03f28e',4)
    emitter.segment(0x3f28e,0x3f29c)
    emitter.ins('bsr.w','scene_pc_03e91c',4)
    emitter.ins('move.w','0x813c:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('jmp','2(%pc, %d0.w)',4)

def _lower_step_summary_scene_phase(emitter,rules):
    emitter.segment(0x3dcda,0x3dcde)
    emitter.ins('bra.w','scene_pc_03f340',4)
    emitter.segment(0x3f340,0x3f34e)
    emitter.ins('bsr.w','scene_pc_03e91c',4)
    emitter.ins('move.w','0x813c:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('jmp','2(%pc, %d0.w)',4)

def _lower_step_pair_transition_scene_phase(emitter,rules):
    emitter.segment(0x3dcde,0x3dce2)
    emitter.ins('bra.w','scene_pc_03e614',4)
    emitter.segment(0x3e614,0x3e622)
    emitter.ins('bsr.w','scene_pc_03e632',4)
    emitter.ins('move.w','0x813c:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('jmp','2(%pc, %d0.w)',4)

def _lower_step_initial_scene_phase(emitter,rules):
    emitter.segment(0x3dce2,0x3dce6)
    emitter.ins('bra.w','scene_pc_03dcea',4)
    emitter.segment(0x3dcea,0x3dcf8)
    emitter.ins('bsr.w','scene_pc_03e91c',4)
    emitter.ins('move.w','0x813c:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('jmp','2(%pc, %d0.w)',4)

def _lower_step_exchange_scene_phase(emitter,rules):
    emitter.segment(0x3dce6,0x3dcea)
    emitter.ins('bra.w','scene_pc_03e45e',4)
    emitter.segment(0x3e45e,0x3e46c)
    emitter.ins('bsr.w','scene_pc_03e632',4)
    emitter.ins('move.w','0x813c:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('jmp','2(%pc, %d0.w)',4)

def _lower_initialize_early_scene(emitter,rules):
    emitter.segment(0x3dcf8,0x3dcfc)
    emitter.ins('bra.w','scene_pc_03dd14',4)
    emitter.segment(0x3dd14,0x3df26)
    emitter.ins('tst.b','0x80da:w',4)
    emitter.ins('beq.b','scene_pc_03dd32',2)
    emitter.ins('cmpi.b','#0x3,0x80da:w',6)
    emitter.ins('beq.w','scene_pc_03dd32',4)
    emitter.ins('cmpi.b','#0x1,0x80da:w',6)
    emitter.ins('bne.w','scene_pc_03dea6',4)
    emitter.ins('bra.w','scene_pc_03dea6',4)
    emitter.ins('lea.l','0xc700:w,%a0',4)
    emitter.ins('moveq','#0,%d1',2)
    emitter.ins('move.w','0x80e0:w,%d0',4)
    emitter.ins('move.b','(%a0, %d0.w),%d1',4)
    emitter.ins('andi.w','#0x3,%d1',4)
    emitter.ins('move.w','0x80e2:w,%d0',4)
    emitter.ins('move.b','(%a0, %d0.w),%d0',4)
    emitter.ins('andi.w','#0x3,%d0',4)
    emitter.ins('sub.b','%d0,%d1',2)
    emitter.ins('addq.w','#0x1,%d1',2)
    emitter.ins('cmpi.w','#0x2,%d1',4)
    emitter.ins('bhi.w','scene_pc_03de24',4)
    emitter.ins('move.w','0x810e:w,%d0',4)
    emitter.ins('addi.w','#0xa,%d0',4)
    emitter.ins('cmp.w','0x810c:w,%d0',4)
    emitter.ins('bcs.w','scene_pc_03de24',4)
    emitter.ins('move.w','0x8106:w,%d0',4)
    emitter.ins('addi.w','#0x14,%d0',4)
    emitter.ins('cmp.w','0x8104:w,%d0',4)
    emitter.ins('bcs.w','scene_pc_03de24',4)
    emitter.ins('move.w','0x80e6:w,%d0',4)
    emitter.ins('cmp.w','0x80e4:w,%d0',4)
    emitter.ins('bcc.w','scene_pc_03de24',4)
    emitter.ins('jsr','-9832(%pc)',4)
    emitter.ins('andi.w','#0x3,%d0',4)
    emitter.ins('bne.w','scene_pc_03de24',4)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('lea.l','0x4539c:l,%a0',6)
    emitter.ins('lea.l','0xc000:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('move.w','#0x8000,0x8000:w',6)
    emitter.ins('move.w','#0x12,%d6',4)
    emitter.ins('jsr','-13024(%pc)',4)
    emitter.ins('move.w','#0x1,0x8116:w',6)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03ddde',4)
    emitter.ins('move.w','#0xa000,0xff700c:l',8)
    emitter.ins('move.l','#0x3b43e,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('move.w','#0x4,0x813c:w',6)
    emitter.ins('bsr.w','scene_pc_03eae2',4)
    emitter.ins('move.w','0x80e0:w,%d0',4)
    emitter.ins('move.w','#0x480,%d1',4)
    emitter.ins('jsr','scene_pc_0661d4:l',6)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('rts','',2)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('lea.l','0x4539c:l,%a0',6)
    emitter.ins('lea.l','0xc000:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('move.w','#0x8000,0x8000:w',6)
    emitter.ins('move.w','#0x12,%d6',4)
    emitter.ins('jsr','-13168(%pc)',4)
    emitter.ins('move.w','#0x1,0x8116:w',6)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03de6e',4)
    emitter.ins('move.w','#0xa000,0xff700c:l',8)
    emitter.ins('move.l','#0x3b388,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('move.w','#0x1,0x813c:w',6)
    emitter.ins('bsr.w','scene_pc_03eae2',4)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('rts','',2)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('lea.l','0x4539c:l,%a0',6)
    emitter.ins('lea.l','0xc000:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('move.w','#0x8000,0x8000:w',6)
    emitter.ins('move.w','#0x12,%d6',4)
    emitter.ins('jsr','-13298(%pc)',4)
    emitter.ins('move.w','#0x1,0x8116:w',6)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03def0',4)
    emitter.ins('move.w','#0xa000,0xff700c:l',8)
    emitter.ins('move.l','#0x3b388,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('bsr.w','scene_pc_03eae2',4)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('rts','',2)

def _lower_process_early_scene_choice(emitter,rules):
    emitter.segment(0x3dcfc,0x3dd08)
    emitter.ins('bra.w','scene_pc_03df26',4)
    emitter.ins('bra.w','scene_pc_03e1ca',4)
    emitter.ins('bra.w','scene_pc_03e206',4)
    emitter.segment(0x3df26,0x3e082)
    emitter.ins('btst.b','#0x5,0x811f:w',6)
    emitter.ins('beq.w','scene_pc_03e254',4)
    emitter.ins('move.w','#0xac,%d0',4)
    emitter.ins('jsr','scene_pc_00808a:l',6)
    emitter.ins('tst.w','0x8142:w',4)
    emitter.ins('bne.w','scene_pc_03e1b6',4)
    emitter.ins('cmpi.b','#0x1,0x80da:w',6)
    emitter.ins('beq.w','scene_pc_03e134',4)
    emitter.ins('cmpi.b','#0x2,0x80da:w',6)
    emitter.ins('beq.w','scene_pc_03e134',4)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('moveq','#0,%d1',2)
    emitter.ins('moveq','#0,%d2',2)
    emitter.ins('lea.l','0xc700:w,%a0',4)
    emitter.ins('move.w','0x80e0:w,%d0',4)
    emitter.ins('move.b','(%a0, %d0.w),%d0',4)
    emitter.ins('andi.w','#0x3,%d0',4)
    emitter.ins('moveq','#5,%d1',2)
    emitter.ins('sub.b','%d0,%d1',2)
    emitter.ins('move.w','0x80e2:w,%d0',4)
    emitter.ins('move.b','(%a0, %d0.w),%d0',4)
    emitter.ins('moveq','#5,%d2',2)
    emitter.ins('sub.b','%d0,%d2',2)
    emitter.ins('move.w','0x8104:w,%d0',4)
    emitter.ins('mulu.w','%d0,%d1',2)
    emitter.ins('mulu.w','#0x64,%d1',4)
    emitter.ins('jsr','-10344(%pc)',4)
    emitter.ins('andi.w','#0x1f,%d0',4)
    emitter.ins('addi.w','#0x14,%d0',4)
    emitter.ins('add.w','0x8106:w,%d0',4)
    emitter.ins('mulu.w','%d0,%d2',2)
    emitter.ins('divu.w','%d2,%d1',2)
    emitter.ins('cmpi.w','#0x64,%d1',4)
    emitter.ins('bhi.w','scene_pc_03dfce',4)
    emitter.ins('jsr','-10372(%pc)',4)
    emitter.ins('andi.w','#0x7f,%d0',4)
    emitter.ins('cmpi.w','#0x64,%d0',4)
    emitter.ins('bhi.b','scene_pc_03dfa4',2)
    emitter.ins('cmp.w','%d1,%d0',2)
    emitter.ins('bhi.w','scene_pc_03e086',4)
    emitter.ins('jsr','-10392(%pc)',4)
    emitter.ins('move.w','0xefd2:w,%d1',4)
    emitter.ins('lea.l','192(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('and.b','(%a0, %d1.w),%d0',4)
    emitter.ins('bne.w','scene_pc_03e086',4)
    emitter.ins('clr.w','0x8142:w',4)
    emitter.ins('move.l','#0x40000003,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x400,%d6',4)
    emitter.ins('move.w','#0x4bf,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03dfea',4)
    emitter.ins('move.w','0x80e0:w,%d0',4)
    emitter.ins('move.w','#0x480,%d1',4)
    emitter.ins('jsr','scene_pc_0661d4:l',6)
    emitter.ins('move.w','#0xc322,%d0',4)
    emitter.ins('bsr.w','scene_pc_03e42a',4)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03e026',4)
    emitter.ins('move.w','#0xa000,0xff700c:l',8)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('move.l','#0x3b3f8,0xff700e:l',10)
    emitter.ins('lea.l','0xc700:w,%a0',4)
    emitter.ins('move.w','0x80e2:w,%d0',4)
    emitter.ins('move.b','(%a0, %d0.w),%d1',4)
    emitter.ins('andi.w','#0x3,%d1',4)
    emitter.ins('move.w','0x80e0:w,%d0',4)
    emitter.ins('move.b','(%a0, %d0.w),%d0',4)
    emitter.ins('andi.w','#0x3,%d0',4)
    emitter.ins('cmp.b','%d0,%d1',2)
    emitter.ins('bcs.b','scene_pc_03e07c',2)
    emitter.ins('move.l','#0x3b3aa,0xff700e:l',10)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('rts','',2)
    emitter.segment(0x3e086,0x3e28e)
    emitter.ins('move.w','#0x1,0x8142:w',6)
    emitter.ins('move.l','#0x40000003,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x400,%d6',4)
    emitter.ins('move.w','#0x4bf,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03e0a4',4)
    emitter.ins('move.w','0x80e0:w,%d0',4)
    emitter.ins('move.w','#0x480,%d1',4)
    emitter.ins('jsr','scene_pc_0661d4:l',6)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03e0d8',4)
    emitter.ins('move.w','#0xa000,0xff700c:l',8)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('move.l','#0x3b3bc,0xff700e:l',10)
    emitter.ins('lea.l','0xc700:w,%a0',4)
    emitter.ins('move.w','0x80e2:w,%d0',4)
    emitter.ins('move.b','(%a0, %d0.w),%d1',4)
    emitter.ins('andi.w','#0x3,%d1',4)
    emitter.ins('move.w','0x80e0:w,%d0',4)
    emitter.ins('move.b','(%a0, %d0.w),%d0',4)
    emitter.ins('andi.w','#0x3,%d1',4)
    emitter.ins('cmp.b','%d0,%d1',2)
    emitter.ins('bcs.b','scene_pc_03e12e',2)
    emitter.ins('move.l','#0x3b3de,0xff700e:l',10)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('rts','',2)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('lea.l','0x4539c:l,%a0',6)
    emitter.ins('lea.l','0xc000:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('move.w','#0x8000,0x8000:w',6)
    emitter.ins('move.w','#0x12,%d6',4)
    emitter.ins('jsr','-13952(%pc)',4)
    emitter.ins('move.w','#0x0,0x8116:w',6)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03e17e',4)
    emitter.ins('move.w','#0xa000,0xff700c:l',8)
    emitter.ins('move.l','#0x3b43e,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('move.w','#0x3,0x813c:w',6)
    emitter.ins('bsr.w','scene_pc_03eae2',4)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('rts','',2)
    emitter.ins('clr.w','0x813a:w',4)
    emitter.ins('move.w','#0x6,0x813c:w',6)
    emitter.ins('clr.w','0x814c:w',4)
    emitter.ins('bsr.w','scene_pc_04031c',4)
    emitter.ins('rts','',2)
    emitter.ins('btst.b','#0x5,0x811f:w',6)
    emitter.ins('beq.w','scene_pc_03e1ec',4)
    emitter.ins('tst.w','0x8142:w',4)
    emitter.ins('bne.w','scene_pc_03e1b6',4)
    emitter.ins('bsr.w','scene_pc_03f0de',4)
    emitter.ins('move.w','#0x8,0x813a:w',6)
    emitter.ins('move.w','#0x5,0x813c:w',6)
    emitter.ins('move.w','0x8020:w,%d0',4)
    emitter.ins('addi.w','#0x70,%d0',4)
    emitter.ins('move.w','#0xa0,%d1',4)
    emitter.ins('bsr.w','scene_pc_03e37a',4)
    emitter.ins('move.w','#0xc322,%d0',4)
    emitter.ins('bsr.w','scene_pc_03e42a',4)
    emitter.ins('rts','',2)
    emitter.ins('tst.b','0x80da:w',4)
    emitter.ins('beq.b','scene_pc_03e21e',2)
    emitter.ins('cmpi.b','#0x3,0x80da:w',6)
    emitter.ins('beq.b','scene_pc_03e21e',2)
    emitter.ins('move.w','0x8120:w,0x811e:w',6)
    emitter.ins('bra.w','scene_pc_03e236',4)
    emitter.ins('move.w','0x8020:w,%d0',4)
    emitter.ins('addi.w','#0x70,%d0',4)
    emitter.ins('move.w','#0x100,%d1',4)
    emitter.ins('bsr.w','scene_pc_03e37a',4)
    emitter.ins('move.w','#0xc33a,%d0',4)
    emitter.ins('bsr.w','scene_pc_03e42a',4)
    emitter.ins('btst.b','#0x5,0x811f:w',6)
    emitter.ins('beq.w','scene_pc_03e254',4)
    emitter.ins('tst.w','0x8142:w',4)
    emitter.ins('bne.w','scene_pc_03e1b6',4)
    emitter.ins('bsr.w','scene_pc_03f0de',4)
    emitter.ins('move.w','#0x6,0x813c:w',6)
    emitter.ins('rts','',2)
    emitter.ins('move.b','0x811f:w,%d0',4)
    emitter.ins('andi.w','#0x3,%d0',4)
    emitter.ins('beq.b','scene_pc_03e264',2)
    emitter.ins('eori.w','#0x1,0x8142:w',6)
    emitter.ins('move.w','#0x38,%d0',4)
    emitter.ins('tst.w','0x8142:w',4)
    emitter.ins('beq.b','scene_pc_03e272',2)
    emitter.ins('move.w','#0x48,%d0',4)
    emitter.ins('add.w','0x8020:w,%d0',4)
    emitter.ins('lea.l','22(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','#0x8c,%d1',4)
    emitter.ins('move.w','#0x104,%d2',4)
    emitter.ins('moveq','#0,%d3',2)
    emitter.ins('move.w','#0x400,%d4',4)
    emitter.ins('jmp','-12624(%pc)',4)
    emitter.segment(0x3e470,0x3e474)
    emitter.ins('bra.w','scene_pc_03e50a',4)
    emitter.segment(0x3e50a,0x3e5dc)
    emitter.ins('btst.b','#0x5,0x811d:w',6)
    emitter.ins('beq.w','scene_pc_03e542',4)
    emitter.ins('move.w','#0xac,%d0',4)
    emitter.ins('jsr','scene_pc_00808a:l',6)
    emitter.ins('tst.w','0x8142:w',4)
    emitter.ins('bne.w','scene_pc_03e558',4)
    emitter.ins('clr.w','0x8142:w',4)
    emitter.ins('move.w','#0x7,0x813a:w',6)
    emitter.ins('clr.w','0x813c:w',4)
    emitter.ins('clr.w','0x814c:w',4)
    emitter.ins('bsr.w','scene_pc_04031c',4)
    emitter.ins('clr.w','0x840a:w',4)
    emitter.ins('rts','',2)
    emitter.ins('move.b','0x811d:w,%d0',4)
    emitter.ins('andi.w','#0x3,%d0',4)
    emitter.ins('beq.w','scene_pc_03e264',4)
    emitter.ins('eori.w','#0x1,0x8142:w',6)
    emitter.ins('bra.w','scene_pc_03e264',4)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('cmpi.b','#0x0,0x80da:w',6)
    emitter.ins('beq.b','scene_pc_03e570',2)
    emitter.ins('cmpi.b','#0x3,0x80da:w',6)
    emitter.ins('beq.b','scene_pc_03e570',2)
    emitter.ins('bsr.w','scene_pc_041818',4)
    emitter.ins('bsr.w','scene_pc_03e6e8',4)
    emitter.ins('bsr.w','scene_pc_03e7ae',4)
    emitter.ins('bsr.w','scene_pc_041818',4)
    emitter.ins('lea.l','0x816a:w,%a0',4)
    emitter.ins('move.w','#0xf,%d1',4)
    emitter.ins('move.w','#0x160,%d0',4)
    emitter.ins('sub.w','0x2(%a0),%d0',4)
    emitter.ins('move.w','%d0,0x2(%a0)',4)
    emitter.ins('move.w','#0x1,0x6(%a0)',6)
    emitter.ins('move.w','#0x1,0x8(%a0)',6)
    emitter.ins('adda.w','#0x10,%a0',4)
    emitter.ins('dbra','%d1,scene_pc_03e584',4)
    emitter.ins('bsr.w','scene_pc_03e6e8',4)
    emitter.ins('bsr.w','scene_pc_03e7ae',4)
    emitter.ins('bsr.w','scene_pc_04031c',4)
    emitter.ins('move.w','#0x1,0x840a:w',6)
    emitter.ins('clr.w','0x8142:w',4)
    emitter.ins('move.w','#0x0,0x8020:w',6)
    emitter.ins('move.w','#0x0,0x8024:w',6)
    emitter.ins('move.w','#0x8200,0x8040:w',6)
    emitter.ins('move.w','#0x8200,0x803a:w',6)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('rts','',2)

def _lower_wait_early_scene_choice(emitter,rules):
    emitter.segment(0x3dd08,0x3dd0c)
    emitter.ins('bra.w','scene_pc_03e298',4)
    emitter.segment(0x3e298,0x3e31a)
    emitter.ins('move.w','0x8020:w,%d0',4)
    emitter.ins('addi.w','#0x70,%d0',4)
    emitter.ins('move.w','#0x100,%d1',4)
    emitter.ins('bsr.w','scene_pc_03e37a',4)
    emitter.ins('move.w','#0xc33a,%d0',4)
    emitter.ins('bsr.w','scene_pc_03e42a',4)
    emitter.ins('bsr.w','scene_pc_03e254',4)
    emitter.ins('addq.w','#0x1,0x8144:w',4)
    emitter.ins('cmpi.w','#0x40,0x8144:w',6)
    emitter.ins('bcs.w','scene_pc_03e318',4)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03e2e6',4)
    emitter.ins('move.w','#0xa000,0xff700c:l',8)
    emitter.ins('move.l','#0x3b41e,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('move.w','#0x3,0x813c:w',6)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('rts','',2)

def _lower_finish_early_scene_fade(emitter,rules):
    emitter.segment(0x3dd0c,0x3dd10)
    emitter.ins('bra.w','scene_pc_03e31a',4)
    emitter.segment(0x3e31a,0x3e342)
    emitter.ins('move.w','0x8020:w,%d0',4)
    emitter.ins('addi.w','#0x70,%d0',4)
    emitter.ins('move.w','#0xa0,%d1',4)
    emitter.ins('bsr.w','scene_pc_03e37a',4)
    emitter.ins('btst.b','#0x7,0x80c4:w',6)
    emitter.ins('beq.w','scene_pc_03e340',4)
    emitter.ins('move.w','#0x3,0x813a:w',6)
    emitter.ins('move.w','#0x3,0x813c:w',6)
    emitter.ins('rts','',2)

def _lower_finish_alternate_scene_fade(emitter,rules):
    emitter.segment(0x3dd10,0x3dd14)
    emitter.ins('bra.w','scene_pc_03e342',4)
    emitter.segment(0x3e342,0x3e37a)
    emitter.ins('cmpi.b','#0x1,0x80da:w',6)
    emitter.ins('beq.b','scene_pc_03e362',2)
    emitter.ins('cmpi.b','#0x2,0x80da:w',6)
    emitter.ins('beq.b','scene_pc_03e362',2)
    emitter.ins('move.w','0x8020:w,%d0',4)
    emitter.ins('addi.w','#0x70,%d0',4)
    emitter.ins('move.w','#0x100,%d1',4)
    emitter.ins('bsr.w','scene_pc_03e37a',4)
    emitter.ins('btst.b','#0x7,0x80c4:w',6)
    emitter.ins('beq.w','scene_pc_03e378',4)
    emitter.ins('move.w','#0x3,0x813a:w',6)
    emitter.ins('move.w','#0x3,0x813c:w',6)
    emitter.ins('rts','',2)

def _lower_append_early_scene_instruction(emitter,rules):
    emitter.segment(0x3e37a,0x3e38e)
    emitter.ins('lea.l','26(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','#0x104,%d2',4)
    emitter.ins('moveq','#0,%d3',2)
    emitter.ins('move.w','#0x400,%d4',4)
    emitter.ins('jmp','-12880(%pc)',4)

def _lower_paint_scene_number_rows(emitter,rules):
    emitter.segment(0x3e42a,0x3e43a)
    emitter.ins('moveq','#7,%d1',2)
    emitter.ins('bsr.w','scene_pc_03e43a',4)
    emitter.ins('addi.w','#0x80,%d0',4)
    emitter.ins('dbra','%d1,scene_pc_03e42c',4)
    emitter.ins('rts','',2)

def _lower_paint_scene_number_row(emitter,rules):
    emitter.segment(0x3e43a,0x3e45e)
    emitter.ins('movem.l','%d0-%d1,-(%a7)',4)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('bsr.w','scene_pc_03b2b0',4)
    emitter.ins('movem.l','(%a7)+,%d0-%d1',4)
    emitter.ins('moveq','#5,%d2',2)
    emitter.ins('move.w','#0xe45d,0xc00000:l',8)
    emitter.ins('dbra','%d2,scene_pc_03e450',4)
    emitter.ins('rts','',2)

def _lower_wait_exchange_scene_transition(emitter,rules):
    emitter.segment(0x3e46c,0x3e470)
    emitter.ins('bra.w','scene_pc_03e478',4)
    emitter.segment(0x3e478,0x3e50a)
    emitter.ins('addq.w','#0x1,0x8142:w',4)
    emitter.ins('cmpi.w','#0x20,0x8142:w',6)
    emitter.ins('bcs.w','scene_pc_03e508',4)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('clr.w','0x8142:w',4)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('lea.l','0x4583f:l,%a0',6)
    emitter.ins('lea.l','0xc000:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('move.w','#0x8000,0x8000:w',6)
    emitter.ins('move.w','#0x12,%d6',4)
    emitter.ins('jsr','-14810(%pc)',4)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03e4d2',4)
    emitter.ins('move.w','#0xa000,0xff700c:l',8)
    emitter.ins('move.l','#0x3b4c6,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('move.w','#0x1,0x8116:w',6)
    emitter.ins('bsr.w','scene_pc_03eae2',4)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('rts','',2)

def _lower_finish_exchange_scene_transition(emitter,rules):
    emitter.segment(0x3e474,0x3e478)
    emitter.ins('bra.w','scene_pc_03e5dc',4)
    emitter.segment(0x3e5dc,0x3e614)
    emitter.ins('cmpi.w','#0x90,0x8020:w',6)
    emitter.ins('bcs.w','scene_pc_03e612',4)
    emitter.ins('move.w','#0x0,0x8040:w',6)
    emitter.ins('move.w','#0x0,0x803a:w',6)
    emitter.ins('addq.w','#0x1,0x8142:w',4)
    emitter.ins('cmpi.w','#0x20,0x8142:w',6)
    emitter.ins('bcs.w','scene_pc_03e612',4)
    emitter.ins('clr.w','0x8142:w',4)
    emitter.ins('move.w','#0x8,0x813a:w',6)
    emitter.ins('clr.w','0x813c:w',4)
    emitter.ins('clr.w','0x814c:w',4)
    emitter.ins('rts','',2)

def _lower_process_pair_phase_counter(emitter,rules):
    emitter.segment(0x3e622,0x3e632)
    emitter.ins('bra.w','scene_pc_03e6a4',4)
    emitter.ins('bra.w','scene_pc_03eb24',4)
    emitter.ins('bra.w','scene_pc_03e7c6',4)
    emitter.ins('bra.w','scene_pc_03e8b4',4)
    emitter.segment(0x3e6a4,0x3e6e8)
    emitter.ins('cmpi.b','#0x1,0x80da:w',6)
    emitter.ins('beq.b','scene_pc_03e6be',2)
    emitter.ins('cmpi.b','#0x2,0x80da:w',6)
    emitter.ins('beq.b','scene_pc_03e6be',2)
    emitter.ins('clr.w','0x813a:w',4)
    emitter.ins('clr.w','0x813c:w',4)
    emitter.ins('rts','',2)
    emitter.ins('addq.w','#0x1,0x8142:w',4)
    emitter.ins('cmpi.w','#0x40,0x8142:w',6)
    emitter.ins('bcs.w','scene_pc_03e6e6',4)
    emitter.ins('bsr.w','scene_pc_03e6e8',4)
    emitter.ins('tst.w','0x80e6:w',4)
    emitter.ins('bne.b','scene_pc_03e6e2',2)
    emitter.ins('bsr.w','scene_pc_03e8a0',4)
    emitter.ins('bsr.w','scene_pc_03f6ee',4)
    emitter.ins('bra.w','scene_pc_03e8d0',4)
    emitter.ins('bra.w','scene_pc_03ea1c',4)
    emitter.ins('rts','',2)
    emitter.segment(0x3e7c6,0x3e8a0)
    emitter.ins('btst.b','#0x5,0x811f:w',6)
    emitter.ins('beq.w','scene_pc_03ecbe',4)
    emitter.ins('move.w','#0xac,%d0',4)
    emitter.ins('jsr','scene_pc_00808a:l',6)
    emitter.ins('cmpi.w','#0x2,0x8144:w',6)
    emitter.ins('bne.w','scene_pc_03ecbe',4)
    emitter.ins('move.w','0x80fa:w,%d0',4)
    emitter.ins('add.w','0x80fc:w,%d0',4)
    emitter.ins('add.w','0x80fe:w,%d0',4)
    emitter.ins('cmp.w','0x80ea:w,%d0',4)
    emitter.ins('bne.w','scene_pc_03ecbe',4)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.w','0x8106:w,%d0',4)
    emitter.ins('move.w','0x8102:w,%d1',4)
    emitter.ins('mulu.w','%d0,%d1',2)
    emitter.ins('divu.w','#0x64,%d1',4)
    emitter.ins('move.w','#0xe,%d0',4)
    emitter.ins('move.w','0x80f2:w,%d2',4)
    emitter.ins('lea.l','0x817a:w,%a6',4)
    emitter.ins('move.w','%d1,0xc(%a6)',4)
    emitter.ins('move.w','0x80ee:w,0xe(%a6)',6)
    emitter.ins('tst.w','%d2',2)
    emitter.ins('beq.w','scene_pc_03e830',4)
    emitter.ins('subq.w','#0x1,%d2',2)
    emitter.ins('addq.w','#0x1,0xe(%a6)',4)
    emitter.ins('adda.w','#0x10,%a6',4)
    emitter.ins('dbra','%d0,scene_pc_03e81a',4)
    emitter.ins('bsr.w','scene_pc_03e8a0',4)
    emitter.ins('move.l','#0x40000003,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x400,%d6',4)
    emitter.ins('move.w','#0x4bf,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03e854',4)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03e872',4)
    emitter.ins('move.w','#0xa000,0xff700c:l',8)
    emitter.ins('move.l','#0x3b34a,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('rts','',2)
    emitter.segment(0x3e8b4,0x3e8f2)
    emitter.ins('bsr.w','scene_pc_03f6c2',4)
    emitter.ins('move.b','0x811f:w,%d0',4)
    emitter.ins('andi.w','#0xc,%d0',4)
    emitter.ins('beq.b','scene_pc_03e8c8',2)
    emitter.ins('bsr.w','scene_pc_04031c',4)
    emitter.ins('rts','',2)
    emitter.ins('btst.b','#0x5,0x811f:w',6)
    emitter.ins('beq.b','scene_pc_03e8f0',2)
    emitter.ins('clr.w','0x813a:w',4)
    emitter.ins('clr.w','0x813c:w',4)
    emitter.ins('clr.w','0x814c:w',4)
    emitter.ins('bsr.w','scene_pc_04031c',4)
    emitter.ins('bsr.w','scene_pc_03e6e8',4)
    emitter.ins('clr.w','0x8142:w',4)
    emitter.ins('clr.w','0x8144:w',4)
    emitter.ins('clr.w','0x8146:w',4)
    emitter.ins('rts','',2)
    emitter.segment(0x3e900,0x3e910)
    emitter.ins('bra.w','scene_pc_03e98a',4)
    emitter.ins('bra.w','scene_pc_03e9ba',4)
    emitter.ins('bra.w','scene_pc_03eb24',4)
    emitter.ins('bra.w','scene_pc_03ebe4',4)
    emitter.segment(0x3e98a,0x3eae2)
    emitter.ins('addq.w','#0x1,0x8142:w',4)
    emitter.ins('cmpi.w','#0x40,0x8142:w',6)
    emitter.ins('bcs.w','scene_pc_03eae0',4)
    emitter.ins('clr.w','0x8142:w',4)
    emitter.ins('move.w','#0x0,0x8020:w',6)
    emitter.ins('move.w','#0x0,0x8024:w',6)
    emitter.ins('move.w','#0x8200,0x8040:w',6)
    emitter.ins('move.w','#0x8200,0x803a:w',6)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('rts','',2)
    emitter.ins('cmpi.w','#0x90,0x8020:w',6)
    emitter.ins('bcs.w','scene_pc_03eae0',4)
    emitter.ins('move.w','#0x0,0x8040:w',6)
    emitter.ins('move.w','#0x0,0x803a:w',6)
    emitter.ins('addq.w','#0x1,0x8142:w',4)
    emitter.ins('cmpi.w','#0x20,0x8142:w',6)
    emitter.ins('bcs.w','scene_pc_03eae0',4)
    emitter.ins('tst.w','0x80e6:w',4)
    emitter.ins('bne.b','scene_pc_03ea1c',2)
    emitter.ins('clr.w','0x80ea:w',4)
    emitter.ins('clr.w','0x80ee:w',4)
    emitter.ins('clr.w','0x80f2:w',4)
    emitter.ins('clr.w','0x80fa:w',4)
    emitter.ins('clr.w','0x80fc:w',4)
    emitter.ins('clr.w','0x80fe:w',4)
    emitter.ins('clr.w','0x8142:w',4)
    emitter.ins('bsr.w','scene_pc_03ecc8',4)
    emitter.ins('bsr.w','scene_pc_03f648',4)
    emitter.ins('move.w','#0x8,0x813a:w',6)
    emitter.ins('clr.w','0x813c:w',4)
    emitter.ins('clr.w','0x814c:w',4)
    emitter.ins('bsr.w','scene_pc_04031c',4)
    emitter.ins('rts','',2)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('clr.w','0x8142:w',4)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('jsr','2612(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('move.l','#0x50000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xbf,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03ea46',4)
    emitter.ins('move.l','#0x50000002,0xc00004:l',10)
    emitter.ins('move.w','0x80e2:w,%d7',4)
    emitter.ins('move.w','#0x3,%d0',4)
    emitter.ins('move.w','#0x1,%d1',4)
    emitter.ins('bsr.w','scene_pc_0402c2',4)
    emitter.ins('lea.l','0x44c6f:l,%a0',6)
    emitter.ins('lea.l','0xc000:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('move.w','#0x8000,0x8000:w',6)
    emitter.ins('move.w','#0x12,%d6',4)
    emitter.ins('jsr','-16302(%pc)',4)
    emitter.ins('bsr.w','scene_pc_03f8f6',4)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03eaaa',4)
    emitter.ins('move.w','#0xa000,0xff700c:l',8)
    emitter.ins('move.l','#0x3b320,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('move.w','#0x1,0x8116:w',6)
    emitter.ins('bsr.w','scene_pc_03eae2',4)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('rts','',2)
    emitter.segment(0x3eb24,0x3ecc8)
    emitter.ins('bsr.w','scene_pc_03f518',4)
    emitter.ins('bsr.w','scene_pc_03f45e',4)
    emitter.ins('bsr.w','scene_pc_03f8f6',4)
    emitter.ins('btst.b','#0x5,0x811f:w',6)
    emitter.ins('beq.b','scene_pc_03eae0',2)
    emitter.ins('move.w','#0xac,%d0',4)
    emitter.ins('jsr','scene_pc_00808a:l',6)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('clr.w','0x8144:w',4)
    emitter.ins('cmpi.b','#0x3,0x80db:w',6)
    emitter.ins('bne.b','scene_pc_03eb6e',2)
    emitter.ins('clr.w','0x80fa:w',4)
    emitter.ins('move.w','0x80ea:w,0x80fc:w',6)
    emitter.ins('clr.w','0x80fe:w',4)
    emitter.ins('cmpi.w','#0x7,0x813a:w',6)
    emitter.ins('beq.w','scene_pc_03e7e4',4)
    emitter.ins('bra.w','scene_pc_03ec02',4)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('lea.l','0x44dc6:l,%a0',6)
    emitter.ins('lea.l','0xc000:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('move.w','#0x8000,0x8000:w',6)
    emitter.ins('move.w','#0x12,%d6',4)
    emitter.ins('jsr','-16570(%pc)',4)
    emitter.ins('bsr.w','scene_pc_03f93e',4)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03ebb6',4)
    emitter.ins('move.w','#0xa000,0xff700c:l',8)
    emitter.ins('move.l','#0x3b336,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('rts','',2)
    emitter.ins('btst.b','#0x5,0x811f:w',6)
    emitter.ins('beq.w','scene_pc_03ecbe',4)
    emitter.ins('move.w','#0xac,%d0',4)
    emitter.ins('jsr','scene_pc_00808a:l',6)
    emitter.ins('cmpi.w','#0x2,0x8144:w',6)
    emitter.ins('bne.w','scene_pc_03ecbe',4)
    emitter.ins('move.w','0x80fa:w,%d0',4)
    emitter.ins('add.w','0x80fc:w,%d0',4)
    emitter.ins('add.w','0x80fe:w,%d0',4)
    emitter.ins('cmp.w','0x80ea:w,%d0',4)
    emitter.ins('bne.w','scene_pc_03ecbe',4)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.w','0x8106:w,%d0',4)
    emitter.ins('move.w','0x8102:w,%d1',4)
    emitter.ins('mulu.w','%d0,%d1',2)
    emitter.ins('divu.w','#0x64,%d1',4)
    emitter.ins('move.w','#0xe,%d0',4)
    emitter.ins('move.w','0x80f2:w,%d2',4)
    emitter.ins('lea.l','0x827a:w,%a6',4)
    emitter.ins('move.w','%d1,0xc(%a6)',4)
    emitter.ins('move.w','0x80ee:w,0xe(%a6)',6)
    emitter.ins('tst.w','%d2',2)
    emitter.ins('beq.w','scene_pc_03ec4a',4)
    emitter.ins('subq.w','#0x1,%d2',2)
    emitter.ins('addq.w','#0x1,0xe(%a6)',4)
    emitter.ins('adda.w','#0x10,%a6',4)
    emitter.ins('dbra','%d0,scene_pc_03ec34',4)
    emitter.ins('bsr.w','scene_pc_03ecc8',4)
    emitter.ins('addq.w','#0x1,0x813c:w',4)
    emitter.ins('move.l','#0x40000003,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x400,%d6',4)
    emitter.ins('move.w','#0x4bf,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03ec72',4)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,scene_pc_03ec90',4)
    emitter.ins('move.w','#0xa000,0xff700c:l',8)
    emitter.ins('move.l','#0x3b34a,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('rts','',2)
    emitter.ins('bsr.w','scene_pc_03f532',4)
    emitter.ins('bsr.w','scene_pc_03f93e',4)
    emitter.ins('rts','',2)

def _lower_gather_early_scene_input(emitter,rules):
    emitter.segment(0x3e632,0x3e6a4)
    emitter.ins('tst.b','0x80da:w',4)
    emitter.ins('bne.b','scene_pc_03e64a',2)
    emitter.ins('move.w','0xf602:w,0x811c:w',6)
    emitter.ins('move.w','0xf602:w,0x811e:w',6)
    emitter.ins('clr.w','0x8120:w',4)
    emitter.ins('rts','',2)
    emitter.ins('cmpi.b','#0x2,0x80da:w',6)
    emitter.ins('bne.b','scene_pc_03e66c',2)
    emitter.ins('move.w','0xf602:w,%d0',4)
    emitter.ins('or.w','0xf604:w,%d0',4)
    emitter.ins('move.w','%d0,0x811c:w',4)
    emitter.ins('move.w','0xf602:w,0x811e:w',6)
    emitter.ins('move.w','0xf604:w,0x8120:w',6)
    emitter.ins('rts','',2)
    emitter.ins('cmpi.b','#0x3,0x80da:w',6)
    emitter.ins('beq.b','scene_pc_03e68e',2)
    emitter.ins('move.w','0xf602:w,%d0',4)
    emitter.ins('or.w','0xf604:w,%d0',4)
    emitter.ins('move.w','%d0,0x811c:w',4)
    emitter.ins('move.w','0xf604:w,0x811e:w',6)
    emitter.ins('move.w','0xf602:w,0x8120:w',6)
    emitter.ins('rts','',2)
    emitter.ins('move.w','0xf604:w,%d0',4)
    emitter.ins('move.w','%d0,0x811c:w',4)
    emitter.ins('move.w','0xf604:w,0x811e:w',6)
    emitter.ins('move.w','0xf602:w,0x8120:w',6)
    emitter.ins('rts','',2)

def _lower_exchange_scene_pair_fields(emitter,rules):
    emitter.segment(0x3e6e8,0x3e7ae)
    emitter.ins('move.w','0x80dc:w,%d0',4)
    emitter.ins('move.w','0x80de:w,0x80dc:w',6)
    emitter.ins('move.w','%d0,0x80de:w',4)
    emitter.ins('move.w','0x80e0:w,%d0',4)
    emitter.ins('move.w','0x80e2:w,0x80e0:w',6)
    emitter.ins('move.w','%d0,0x80e2:w',4)
    emitter.ins('move.w','0x80e4:w,%d0',4)
    emitter.ins('move.w','0x80e6:w,0x80e4:w',6)
    emitter.ins('move.w','%d0,0x80e6:w',4)
    emitter.ins('move.w','0x80e8:w,%d0',4)
    emitter.ins('move.w','0x80ea:w,0x80e8:w',6)
    emitter.ins('move.w','%d0,0x80ea:w',4)
    emitter.ins('move.w','0x80ec:w,%d0',4)
    emitter.ins('move.w','0x80ee:w,0x80ec:w',6)
    emitter.ins('move.w','%d0,0x80ee:w',4)
    emitter.ins('move.w','0x80f0:w,%d0',4)
    emitter.ins('move.w','0x80f2:w,0x80f0:w',6)
    emitter.ins('move.w','%d0,0x80f2:w',4)
    emitter.ins('move.w','0x80f4:w,%d0',4)
    emitter.ins('move.w','0x80fa:w,0x80f4:w',6)
    emitter.ins('move.w','%d0,0x80fa:w',4)
    emitter.ins('move.w','0x80f6:w,%d0',4)
    emitter.ins('move.w','0x80fc:w,0x80f6:w',6)
    emitter.ins('move.w','%d0,0x80fc:w',4)
    emitter.ins('move.w','0x80f8:w,%d0',4)
    emitter.ins('move.w','0x80fe:w,0x80f8:w',6)
    emitter.ins('move.w','%d0,0x80fe:w',4)
    emitter.ins('move.w','0x8100:w,%d0',4)
    emitter.ins('move.w','0x8102:w,0x8100:w',6)
    emitter.ins('move.w','%d0,0x8102:w',4)
    emitter.ins('move.w','0x8104:w,%d0',4)
    emitter.ins('move.w','0x8106:w,0x8104:w',6)
    emitter.ins('move.w','%d0,0x8106:w',4)
    emitter.ins('move.w','0x8108:w,%d0',4)
    emitter.ins('move.w','0x810a:w,0x8108:w',6)
    emitter.ins('move.w','%d0,0x810a:w',4)
    emitter.ins('move.w','0x810c:w,%d0',4)
    emitter.ins('move.w','0x810e:w,0x810c:w',6)
    emitter.ins('move.w','%d0,0x810e:w',4)
    emitter.ins('move.w','0x8110:w,%d0',4)
    emitter.ins('move.w','0x8112:w,0x8110:w',6)
    emitter.ins('move.w','%d0,0x8112:w',4)
    emitter.ins('rts','',2)

def _lower_exchange_scene_actor_records(emitter,rules):
    emitter.segment(0x3e7ae,0x3e7c6)
    emitter.ins('move.w','#0x7f,%d0',4)
    emitter.ins('lea.l','0x816a:w,%a0',4)
    emitter.ins('lea.l','0x826a:w,%a1',4)
    emitter.ins('move.w','(%a0),%d1',2)
    emitter.ins('move.w','(%a1),(%a0)+',2)
    emitter.ins('move.w','%d1,(%a1)+',2)
    emitter.ins('dbra','%d0,scene_pc_03e7ba',4)
    emitter.ins('rts','',2)

def _lower_refresh_primary_actor_summary(emitter,rules):
    emitter.segment(0x3e8a0,0x3e8b4)
    emitter.ins('move.w','0x8106:w,%d0',4)
    emitter.ins('add.w','0x810a:w,%d0',4)
    emitter.ins('move.w','%d0,0x8176:w',4)
    emitter.ins('move.w','0x810e:w,0x8178:w',6)
    emitter.ins('rts','',2)

LOWERERS={
    'begin_scene_palette_lighten':_lower_begin_scene_palette_lighten,
    'snapshot_scene_palette':_lower_snapshot_scene_palette,
    'restore_scene_palette':_lower_restore_scene_palette,
    'encode_six_decimal_digits':_lower_encode_six_decimal_digits,
    'append_decimal_digit':_lower_append_decimal_digit,
    'adjust_scene_scroll':_lower_adjust_scene_scroll,
    'step_main_scene_phase':_lower_step_main_scene_phase,
    'step_result_scene_phase':_lower_step_result_scene_phase,
    'step_confirmation_scene_phase':_lower_step_confirmation_scene_phase,
    'step_transfer_scene_phase':_lower_step_transfer_scene_phase,
    'step_primary_detail_scene_phase':_lower_step_primary_detail_scene_phase,
    'step_secondary_detail_scene_phase':_lower_step_secondary_detail_scene_phase,
    'step_summary_scene_phase':_lower_step_summary_scene_phase,
    'step_pair_transition_scene_phase':_lower_step_pair_transition_scene_phase,
    'step_initial_scene_phase':_lower_step_initial_scene_phase,
    'step_exchange_scene_phase':_lower_step_exchange_scene_phase,
    'initialize_early_scene':_lower_initialize_early_scene,
    'process_early_scene_choice':_lower_process_early_scene_choice,
    'wait_early_scene_choice':_lower_wait_early_scene_choice,
    'finish_early_scene_fade':_lower_finish_early_scene_fade,
    'finish_alternate_scene_fade':_lower_finish_alternate_scene_fade,
    'append_early_scene_instruction':_lower_append_early_scene_instruction,
    'paint_scene_number_rows':_lower_paint_scene_number_rows,
    'paint_scene_number_row':_lower_paint_scene_number_row,
    'wait_exchange_scene_transition':_lower_wait_exchange_scene_transition,
    'finish_exchange_scene_transition':_lower_finish_exchange_scene_transition,
    'process_pair_phase_counter':_lower_process_pair_phase_counter,
    'gather_early_scene_input':_lower_gather_early_scene_input,
    'exchange_scene_pair_fields':_lower_exchange_scene_pair_fields,
    'exchange_scene_actor_records':_lower_exchange_scene_actor_records,
    'refresh_primary_actor_summary':_lower_refresh_primary_actor_summary,
}

def compile_early_phase(source, *, selected_names=None):
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    sole_main_phase_fields = {name: records[name]['effects'] for name in ('_phase_legacy_fields', 'adjust_scene_scroll_fields', 'step_main_scene_phase_fields')}
    for owner in ('adjust_scene_scroll', 'step_main_scene_phase'):
        records[owner]['effects'] = dict(previous=records[owner]['effects'], sole_main_phase_fields=sole_main_phase_fields)
    sole_pure_rule_fields = {name:records[name]['effects'] for name in ('_scene_rule_frame_fields', '_scene_rule_store_word_fields', '_scene_rule_input_bit_fields', 'gather_early_scene_input_fields', 'exchange_scene_pair_frame_fields', 'exchange_scene_actor_records_fields', '_scene_rule_summary_fields', 'refresh_primary_actor_summary_fields')}
    for owner in ('gather_early_scene_input', 'exchange_scene_pair_fields', 'exchange_scene_actor_records', 'refresh_primary_actor_summary'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'],sole_pure_rule_fields=sole_pure_rule_fields)
    sole_allocation_fields = {name:records[name]['effects'] for name in ('_allocation_read_fields', '_allocation_move_fields', '_allocation_ram_move_fields', '_allocation_store_fields', '_allocation_test_ram_fields', '_allocation_compare_ram_fields', '_allocation_mask_fields', '_allocation_arithmetic_fields', '_allocation_adjust_ram_fields', '_allocation_status_fields', '_allocation_dbword_fields', '_allocation_restore_fields', '_allocation_fill_fields', '_allocation_script_fields', '_allocation_decode_panel_fields', '_allocation_leave_prompt_fields', '_allocation_choice_marker_fields', '_allocation_instruction_at_fields', '_allocation_xor_choice_fields', '_allocation_link_clear_fields', 'begin_scene_palette_lighten_fields', '_allocation_palette_copy_fields', 'snapshot_scene_palette_fields', 'restore_scene_palette_fields', 'append_decimal_digit_fields', 'encode_six_decimal_digits_fields', 'append_early_scene_instruction_fields', 'paint_scene_number_row_fields', 'paint_scene_number_rows_fields', '_allocation_initialize_panel_fields', 'initialize_early_scene_fields', '_allocation_contested_roll_fields', '_allocation_show_choice_fields', 'process_early_scene_choice_fields', 'draw_early_scene_choice_fields', 'present_early_scene_prompt_fields', 'finish_early_scene_prompt_fields', 'wait_early_scene_choice_fields', '_allocation_finish_fade_fields', 'finish_early_scene_fade_fields', 'finish_alternate_scene_fade_fields', 'wait_exchange_scene_transition_fields', 'process_exchange_scene_choice_fields', 'finish_exchange_scene_transition_fields', '_allocation_exit_pair_fields', '_allocation_finish_class_fields', '_allocation_roster_shares_fields', '_allocation_confirm_shares_fields', '_allocation_check_commit_fields', '_allocation_prepare_secondary_fields', 'process_pair_phase_counter_fields', 'confirm_pair_allocation_fields', 'update_pair_allocation_input_fields', 'exit_pair_allocation_fields', 'wait_pair_stage_motion_fields', 'advance_pair_stage_motion_fields', 'confirm_second_pair_allocation_fields', 'present_pair_stage_summary_fields', '_allocation_phase_fields', 'step_result_scene_phase_fields', 'step_confirmation_scene_phase_fields', 'step_transfer_scene_phase_fields', 'step_primary_detail_scene_phase_fields', 'step_secondary_detail_scene_phase_fields', 'step_summary_scene_phase_fields', 'step_pair_transition_scene_phase_fields', 'step_initial_scene_phase_fields', 'step_exchange_scene_phase_fields', '_allocation_call_fields', '_allocation_known_fields')}
    for owner in ('begin_scene_palette_lighten', 'snapshot_scene_palette', 'restore_scene_palette', 'encode_six_decimal_digits', 'append_decimal_digit', 'step_result_scene_phase', 'step_confirmation_scene_phase', 'step_transfer_scene_phase', 'step_primary_detail_scene_phase', 'step_secondary_detail_scene_phase', 'step_summary_scene_phase', 'step_pair_transition_scene_phase', 'step_initial_scene_phase', 'step_exchange_scene_phase', 'initialize_early_scene', 'process_early_scene_choice', 'present_early_scene_prompt', 'finish_early_scene_prompt', 'draw_early_scene_choice', 'process_exchange_scene_choice', 'wait_early_scene_choice', 'finish_early_scene_fade', 'finish_alternate_scene_fade', 'append_early_scene_instruction', 'paint_scene_number_rows', 'paint_scene_number_row', 'wait_exchange_scene_transition', 'finish_exchange_scene_transition', 'process_pair_phase_counter', 'confirm_pair_allocation', 'update_pair_allocation_input', 'exit_pair_allocation', 'wait_pair_stage_motion', 'advance_pair_stage_motion', 'confirm_second_pair_allocation', 'present_pair_stage_summary'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'],sole_allocation_fields=sole_allocation_fields)
    if selected_names is not None:
        if type(selected_names) is not tuple or selected_names != BATTLE_OBJECT_NATIVE_NAMES:
            raise CompileError('only the fixed complete B39 object-phase native family is admitted')
        selected_bindings = tuple((binding for binding in EARLY_PHASE_BINDINGS if binding.name in selected_names))
        if len(selected_bindings) != len(selected_names):
            raise CompileError('all selected B39 complete physical owners are required')
        selected_lowerers = {name: LOWERERS[name] for name in selected_names}
        return lower_declared(records, selected_bindings, selected_lowerers)
    return lower_declared(records, EARLY_PHASE_BINDINGS, LOWERERS)

# B39 sole main-stage controls and genuine instruction-tail routes; native lowerers unchanged.
for _module,_names in {None: ['business_late_phase'],
 'business_actions': ['upload_object_officer_name', 'upload_portrait_tiles'],
 'business_late_phase': ['_phase_call_fields',
                         'adjust_secondary_formation_scene_fields',
                         'dispatch_late_substate',
                         'latch_scene_controller_inputs',
                         'latch_scene_controller_inputs_fields',
                         'update_active_battle_controls_fields'],
 'contexts_actions': ['DuelGlyphContext'],
 'contexts_early_phase': ['BattleActors',
                          'DecimalDigitsResult',
                          'PhaseFrame',
                          'SceneControllerConditions',
                          'SceneControllerFrame',
                          'SceneControllerOutcome',
                          'checked_phase',
                          'phase_add_word',
                          'phase_bit',
                          'phase_compare',
                          'phase_controller_return',
                          'phase_enter_call',
                          'phase_finish_call',
                          'phase_from_controller',
                          'phase_logic',
                          'phase_operands',
                          'phase_shifted_selector'],
 'domain': ['Boundary',
            'Cursor',
            'Long',
            'SceneState',
            'VideoPlaneAddress',
            'Word',
            'checked_cursor',
            'checked_state',
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
 'services': ['FirstDeploymentFrame',
              'SceneRefreshBoundary',
              'SceneRefreshMemory',
              'SceneRenderFrame',
              '_first_word',
              '_object_adjust_word_fields',
              '_scene_controller_legacy_fields',
              '_scene_controller_legacy_projection',
              '_scene_refresh_flags',
              '_scene_render_asl_word',
              '_scene_render_bit',
              '_scene_render_compare',
              'advance_scene_palette_fade',
              'append_unclipped_scene_sprites',
              'clear_scene_object_label_plane',
              'enqueue_sound_command',
              'first_replace',
              'initialize_scene_object_roster_after_mode_check',
              'read_vdp_plane_rle_rows_from_control',
              'sample_random_preserving_seed_carrier',
              'set_vram_write_address']}.items():
    APPROVED.setdefault(_module,set()).update(_names)
DECLARATIONS.update({'_phase_legacy_fields': {'signature': 'state: SceneState, frame: PhaseFrame, entry: Long, needs_stack: bool=False',
                          'returns': 'FirstDeploymentFrame',
                          'flow': 'if type(frame) is not PhaseFrame:\n'
                                  "    raise ValueError('same-state PhaseFrame required')\n"
                                  'frame.validate(state)\n'
                                  'if frame.live is not None:\n'
                                  '    actual = _scene_controller_legacy_fields(state, phase_controller_return(state, '
                                  'frame))\n'
                                  'else:\n'
                                  '    actual = first_replace(FirstDeploymentFrame.unobserved(), '
                                  'target_x=frame.video_command, target_y=frame.foreground, unit=frame.mode, '
                                  'count=frame.row_count, distance=frame.tile, choice=frame.glyph_tokens)\n'
                                  '    if frame.actors is not None:\n'
                                  '        actual = first_replace(actual, auxiliary=frame.actors.actor.cursor(), '
                                  'scratch=frame.actors.opponent.cursor())\n'
                                  'if needs_stack or (actual.stack_cursor is not None and actual.status is None):\n'
                                  '    raise SceneRefreshBoundary(entry, actual, None)\n'
                                  'return actual'},
 '_phase_legacy_projection': {'signature': 'state: SceneState, original: PhaseFrame, actual: FirstDeploymentFrame',
                              'returns': 'PhaseFrame',
                              'flow': "for name in ('target_x', 'target_y', 'unit', 'count', 'distance', 'choice'):\n"
                                      '    if actual.carrier(name) is None:\n'
                                      "        raise Boundary('historical phase result lacks an observed retained "
                                      "value')\n"
                                      'if original.live is not None:\n'
                                      '    return phase_from_controller(state, '
                                      '_scene_controller_legacy_projection(state, actual))\n'
                                      'actors = original.actors\n'
                                      'if actual.auxiliary is not None and actual.scratch is not None:\n'
                                      '    from .contexts_early_phase import BattleActors\n'
                                      '    actors = BattleActors(state.table_at(actual.auxiliary.base), '
                                      'state.table_at(actual.scratch.base))\n'
                                      'return replace(original, video_command=actual.target_x, '
                                      'foreground=actual.target_y, mode=actual.unit, row_count=actual.count, '
                                      'tile=actual.distance, glyph_tokens=actual.choice, actors=actors)'},
 'adjust_scene_scroll': {'signature': 'state: SceneState, frame: PhaseFrame',
                         'returns': 'PhaseFrame',
                         'flow': 'actual = _phase_legacy_fields(state, frame, 252272)\n'
                                 'return _phase_legacy_projection(state, frame, '
                                 'adjust_scene_scroll_fields(SceneRefreshMemory(state), actual))'},
 'adjust_scene_scroll_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                'returns': 'FirstDeploymentFrame',
                                'flow': 'memory.frame(frame)\n'
                                        'memory.sync_status(frame)\n'
                                        'value = memory.state.read(4294934812, 1)\n'
                                        'frame = _scene_render_bit(memory, frame, value, 1)\n'
                                        'if value & 1:\n'
                                        '    memory.sync_status(frame)\n'
                                        '    scroll = memory.state.read(4294934560, 2)\n'
                                        '    frame = _scene_refresh_flags(memory, frame, scroll, 2)\n'
                                        '    if scroll:\n'
                                        '        frame = _object_adjust_word_fields(memory, frame, 4294934566, 2, '
                                        'True)\n'
                                        '        frame = _object_adjust_word_fields(memory, frame, 4294934560, 2, '
                                        'True)\n'
                                        'memory.sync_status(frame)\n'
                                        'value = memory.state.read(4294934812, 1)\n'
                                        'frame = _scene_render_bit(memory, frame, value, 2)\n'
                                        'if value & 2:\n'
                                        '    memory.sync_status(frame)\n'
                                        '    scroll = memory.state.read(4294934560, 2)\n'
                                        '    frame = _scene_render_compare(memory, frame, scroll, 144, 16)\n'
                                        '    if scroll < 144:\n'
                                        '        frame = _object_adjust_word_fields(memory, frame, 4294934566, 2)\n'
                                        '        frame = _object_adjust_word_fields(memory, frame, 4294934560, 2)\n'
                                        'return memory.sync_status(frame)'},
 'step_main_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame',
                           'returns': 'PhaseFrame',
                           'flow': 'actual = _phase_legacy_fields(state, frame, 253122, True)\n'
                                   'return _phase_legacy_projection(state, frame, '
                                   'step_main_scene_phase_fields(SceneRefreshMemory(state), actual))'},
 'step_main_scene_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': 'from .business_late_phase import _phase_call_fields, '
                                          'adjust_secondary_formation_scene_fields, '
                                          'update_active_battle_controls_fields, latch_scene_controller_inputs_fields\n'
                                          'memory.frame(frame)\n'
                                          'if frame.stack_cursor is None or frame.status is None:\n'
                                          '    raise SceneRefreshBoundary(253122, frame, None)\n'
                                          'frame = _phase_call_fields(memory, frame, 256284, 256246)\n'
                                          'memory.sync_status(frame)\n'
                                          'selector = memory.state.read(4294934844, 2)\n'
                                          "frame = _first_word(frame, 'target_x', selector)\n"
                                          "frame = _scene_render_asl_word(memory, frame, 'target_x', selector, 2)\n"
                                          'target = u32(256256 + s16(low16(frame.target_x)))\n'
                                          'if target in (256256, 256260, 256264, 256268):\n'
                                          '    return _allocation_known_fields(memory, frame, target)\n'
                                          'if target in (256272, 256276):\n'
                                          '    return adjust_secondary_formation_scene_fields(memory, frame)\n'
                                          'if target == 256280:\n'
                                          '    return update_active_battle_controls_fields(memory, frame)\n'
                                          'if target == 256284:\n'
                                          '    return latch_scene_controller_inputs_fields(memory, frame)\n'
                                          'raise SceneRefreshBoundary(target, memory.sync_status(frame), None)'}})

BATTLE_OBJECT_NATIVE_NAMES = ('adjust_scene_scroll', 'step_main_scene_phase')

DECLARATIONS.update({'gather_early_scene_input': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nentered = _phase_legacy_fields(state, frame, 255538)\nreturned = gather_early_scene_input_fields(SceneRefreshMemory(state), entered)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'exchange_scene_pair_fields': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nentered = _phase_legacy_fields(state, frame, 255720)\nreturned = exchange_scene_pair_frame_fields(SceneRefreshMemory(state), entered)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'exchange_scene_actor_records': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nentered = _phase_legacy_fields(state, frame, 255918)\nreturned = exchange_scene_actor_records_fields(SceneRefreshMemory(state), entered)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'refresh_primary_actor_summary': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'from .business_early_phase import _phase_legacy_fields, _phase_legacy_projection\nentered = _phase_legacy_fields(state, frame, 256160)\nreturned = refresh_primary_actor_summary_fields(SceneRefreshMemory(state), entered)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'_scene_rule_frame_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, entry: int', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_remaining_flows.business_city import _resource_cost_frame\nif type(memory) is not SceneRefreshMemory:\n    raise ValueError('same typed Scene rule memory required')\nreturn _resource_cost_frame(memory.state, frame, entry)"}})

DECLARATIONS.update({'_scene_rule_store_word_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, address: Long, value: Word, clear: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': 'from ..high_level_scene_flows.business_objects import _object_clear_word_fields\nfrom ..high_level_gameplay_flow.business_services import _scene_refresh_emit\nif clear:\n    return _object_clear_word_fields(memory, frame, address)\nreturn _scene_refresh_emit(memory, frame, address, 2, low16(value))'}})

DECLARATIONS.update({'_scene_rule_input_bit_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, address: Long, bit: Word', 'returns': 'tuple[FirstDeploymentFrame, bool]', 'flow': 'memory.sync_status(frame)\nvalue = memory.state.read(address, 1)\nframe = _scene_render_bit(memory, frame, value, 1 << bit)\nreturn (frame, bool(value & 1 << bit))'}})

DECLARATIONS.update({'gather_early_scene_input_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_movement_support import _movement_move, _movement_test, _movement_compare\nframe = _scene_rule_frame_fields(memory, frame, 255538)\nstate = memory.state\nframe = _movement_test(state, frame, state.read(4294934746, 1), 8)\nif frame.status & 4:\n    frame = _scene_rule_store_word_fields(memory, frame, 4294934812, state.read(4294964738, 2))\n    frame = _scene_rule_store_word_fields(memory, frame, 4294934814, state.read(4294964738, 2))\n    return _scene_rule_store_word_fields(memory, frame, 4294934816, 0, True)\nframe = _movement_compare(state, frame, state.read(4294934746, 1), 2, 8)\nif frame.status & 4:\n    frame = _movement_move(state, frame, 'target_x', state.read(4294964738, 2), 16)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) | state.read(4294964740, 2), 16)\n    frame = _scene_rule_store_word_fields(memory, frame, 4294934812, low16(frame.target_x))\n    frame = _scene_rule_store_word_fields(memory, frame, 4294934814, state.read(4294964738, 2))\n    return _scene_rule_store_word_fields(memory, frame, 4294934816, state.read(4294964740, 2))\nframe = _movement_compare(state, frame, state.read(4294934746, 1), 3, 8)\nif frame.status & 4:\n    frame = _movement_move(state, frame, 'target_x', state.read(4294964740, 2), 16)\nelse:\n    frame = _movement_move(state, frame, 'target_x', state.read(4294964738, 2), 16)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) | state.read(4294964740, 2), 16)\nframe = _scene_rule_store_word_fields(memory, frame, 4294934812, low16(frame.target_x))\nframe = _scene_rule_store_word_fields(memory, frame, 4294934814, state.read(4294964740, 2))\nreturn _scene_rule_store_word_fields(memory, frame, 4294934816, state.read(4294964738, 2))"}})

DECLARATIONS.update({'exchange_scene_pair_frame_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_movement_support import _movement_move\nframe = _scene_rule_frame_fields(memory, frame, 255720)\npairs = ((32988, 32990), (32992, 32994), (32996, 32998), (33000, 33002), (33004, 33006), (33008, 33010), (33012, 33018), (33014, 33020), (33016, 33022), (33024, 33026), (33028, 33030), (33032, 33034), (33036, 33038), (33040, 33042))\nfor primary, secondary in pairs:\n    frame = _movement_move(memory.state, frame, 'target_x', memory.state.read(4294901760 | primary, 2), 16)\n    frame = _scene_rule_store_word_fields(memory, frame, 4294901760 | primary, memory.state.read(4294901760 | secondary, 2))\n    frame = _scene_rule_store_word_fields(memory, frame, 4294901760 | secondary, low16(frame.target_x))\nreturn frame"}})

DECLARATIONS.update({'exchange_scene_actor_records_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_movement_support import _movement_move\nframe = _scene_rule_frame_fields(memory, frame, 255918)\nframe = _movement_move(memory.state, frame, 'target_x', 127, 16)\nframe = first_replace(frame, roster=memory.cursor_at(4294934890), candidates=memory.cursor_at(4294935146))\nwhile True:\n    frame = _movement_move(memory.state, frame, 'target_y', frame.roster.word(0), 16)\n    frame = _scene_rule_store_word_fields(memory, frame, frame.roster.base, frame.candidates.word(0))\n    frame = first_replace(frame, roster=frame.roster.advance(2))\n    frame = _scene_rule_store_word_fields(memory, frame, frame.candidates.base, low16(frame.target_y))\n    frame = first_replace(frame, candidates=frame.candidates.advance(2))\n    counter = u16(low16(frame.target_x) - 1)\n    frame = first_replace(frame, target_x=replace_word(frame.target_x, counter))\n    if counter == 65535:\n        return frame"}})

DECLARATIONS.update({'_scene_rule_summary_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, secondary: bool', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_movement_support import _movement_move, _movement_add_word\nentry = 257224 if secondary else 256160\nframe = _scene_rule_frame_fields(memory, frame, entry)\nframe = _movement_move(memory.state, frame, 'target_x', memory.state.read(4294934790, 2), 16)\nframe = _movement_add_word(memory.state, frame, 'target_x', memory.state.read(4294934794, 2))\nframe = _scene_rule_store_word_fields(memory, frame, 4294935158 if secondary else 4294934902, low16(frame.target_x))\nreturn _scene_rule_store_word_fields(memory, frame, 4294935160 if secondary else 4294934904, memory.state.read(4294934798, 2))"}})

DECLARATIONS.update({'refresh_primary_actor_summary_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _scene_rule_summary_fields(memory, frame, False)'}})

APPROVED.setdefault((2,'high_level_remaining_flows.business_city'),set()).add('_resource_cost_frame')
APPROVED.setdefault((2,'high_level_scene_flows.business_objects'),set()).add('_object_clear_word_fields')
APPROVED.setdefault((2,'high_level_gameplay_flow.business_services'),set()).add('_scene_refresh_emit')
APPROVED.setdefault((2,'high_level_main_flows.business_movement_support'),set()).update({'_movement_move','_movement_add_word','_movement_test','_movement_compare'})

APPROVED.setdefault('business_early_phase',set()).update({'_phase_legacy_fields','_phase_legacy_projection'})

DECLARATIONS.update({'begin_scene_palette_lighten': {'signature': 'state: SceneState, value: Long', 'returns': 'Long', 'flow': 'checked_state(state)\nactual = FirstDeploymentFrame.unobserved()\nuint(value, 32)\nactual = first_replace(actual, target_x=value)\nreturned = begin_scene_palette_lighten_fields(SceneRefreshMemory(state), actual)\nreturn returned.target_x'}})

DECLARATIONS.update({'snapshot_scene_palette': {'signature': 'state: SceneState', 'returns': 'None', 'flow': 'checked_state(state)\nactual = FirstDeploymentFrame.unobserved()\nreturned = snapshot_scene_palette_fields(SceneRefreshMemory(state), actual)\nreturn None'}})

DECLARATIONS.update({'restore_scene_palette': {'signature': 'state: SceneState', 'returns': 'None', 'flow': 'checked_state(state)\nactual = FirstDeploymentFrame.unobserved()\nreturned = restore_scene_palette_fields(SceneRefreshMemory(state), actual)\nreturn None'}})

DECLARATIONS.update({'encode_six_decimal_digits': {'signature': 'state: SceneState, value: Long', 'returns': 'DecimalDigitsResult', 'flow': 'checked_state(state)\nactual = FirstDeploymentFrame.unobserved()\nuint(value, 32)\nactual = first_replace(actual, target_x=value)\nreturned = encode_six_decimal_digits_fields(SceneRefreshMemory(state), actual)\nreturn DecimalDigitsResult(returned.target_x, returned.roster).validate(state)'}})

DECLARATIONS.update({'append_decimal_digit': {'signature': 'state: SceneState, value: Long, divisor: Word, destination: Cursor', 'returns': 'DecimalDigitsResult', 'flow': 'checked_state(state)\nactual = FirstDeploymentFrame.unobserved()\nuint(value, 32)\nactual = first_replace(actual, target_x=value)\nuint(divisor, 16)\nchecked_cursor(destination, state)\nactual = first_replace(actual, unit=divisor, roster=destination)\nreturned = append_decimal_digit_fields(SceneRefreshMemory(state), actual)\nreturn DecimalDigitsResult(returned.target_x, returned.roster).validate(state)'}})

DECLARATIONS.update({'step_result_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 253126)\nreturned = step_result_scene_phase_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'step_confirmation_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 253130)\nreturned = step_confirmation_scene_phase_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'step_transfer_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 253134)\nreturned = step_transfer_scene_phase_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'step_primary_detail_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 253138)\nreturned = step_primary_detail_scene_phase_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'step_secondary_detail_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 253142)\nreturned = step_secondary_detail_scene_phase_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'step_summary_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 253146)\nreturned = step_summary_scene_phase_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'step_pair_transition_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 253150)\nreturned = step_pair_transition_scene_phase_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'step_initial_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 253154)\nreturned = step_initial_scene_phase_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'step_exchange_scene_phase': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 253158)\nreturned = step_exchange_scene_phase_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'initialize_early_scene': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 253176)\nreturned = initialize_early_scene_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'process_early_scene_choice': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 253180)\nreturned = process_early_scene_choice_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'present_early_scene_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 253184)\nreturned = present_early_scene_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'finish_early_scene_prompt': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 253188)\nreturned = finish_early_scene_prompt_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'draw_early_scene_choice': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 254548)\nreturned = draw_early_scene_choice_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'process_exchange_scene_choice': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 255088)\nreturned = process_exchange_scene_choice_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'wait_early_scene_choice': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 253192)\nreturned = wait_early_scene_choice_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'finish_early_scene_fade': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 253196)\nreturned = finish_early_scene_fade_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'finish_alternate_scene_fade': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 253200)\nreturned = finish_alternate_scene_fade_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'append_early_scene_instruction': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 254842)\nreturned = append_early_scene_instruction_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'paint_scene_number_rows': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 255018)\nreturned = paint_scene_number_rows_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'paint_scene_number_row': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 255034)\nreturned = paint_scene_number_row_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'wait_exchange_scene_transition': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 255084)\nreturned = wait_exchange_scene_transition_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'finish_exchange_scene_transition': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 255092)\nreturned = finish_exchange_scene_transition_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'process_pair_phase_counter': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 255522)\nreturned = process_pair_phase_counter_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'confirm_pair_allocation': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 255526)\nreturned = confirm_pair_allocation_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'update_pair_allocation_input': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 255530)\nreturned = update_pair_allocation_input_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'exit_pair_allocation': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 255534)\nreturned = exit_pair_allocation_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'wait_pair_stage_motion': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 256256)\nreturned = wait_pair_stage_motion_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'advance_pair_stage_motion': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 256260)\nreturned = advance_pair_stage_motion_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'confirm_second_pair_allocation': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 256264)\nreturned = confirm_second_pair_allocation_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'present_pair_stage_summary': {'signature': 'state: SceneState, frame: PhaseFrame', 'returns': 'PhaseFrame', 'flow': 'actual = _phase_legacy_fields(state, frame, 256268)\nreturned = present_pair_stage_summary_fields(SceneRefreshMemory(state), actual)\nreturn _phase_legacy_projection(state, frame, returned)'}})

DECLARATIONS.update({'_allocation_read_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, address: Long, width: Word', 'returns': None, 'flow': 'memory.sync_status(frame)\nreturn memory.state.read(address, width)'}})

DECLARATIONS.update({'_allocation_move_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, value: Long, width: Word=16', 'returns': 'FirstDeploymentFrame', 'flow': 'if width == 32:\n    return _movement_move_long(memory.state, frame, name, value)\nreturn _movement_move(memory.state, frame, name, value, width)'}})

DECLARATIONS.update({'_allocation_ram_move_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, low: Word, width: Word=16', 'returns': 'FirstDeploymentFrame', 'flow': 'return _allocation_move_fields(memory, frame, name, _allocation_read_fields(memory, frame, 4294901760 | low, width // 8), width)'}})

DECLARATIONS.update({'_allocation_store_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, low: Word, value: Long, width: Word=2, clear: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': 'if clear:\n    return _object_clear_word_fields(memory, frame, 4294901760 | low)\nreturn _scene_refresh_emit(memory, frame, 4294901760 | low, width, value)'}})

DECLARATIONS.update({'_allocation_test_ram_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, low: Word, width: Word=16', 'returns': 'FirstDeploymentFrame', 'flow': 'return _movement_test(memory.state, frame, _allocation_read_fields(memory, frame, 4294901760 | low, width // 8), width)'}})

DECLARATIONS.update({'_allocation_compare_ram_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, low: Word, value: Long, width: Word=16', 'returns': 'FirstDeploymentFrame', 'flow': 'return _movement_compare(memory.state, frame, _allocation_read_fields(memory, frame, 4294901760 | low, width // 8), value, width)'}})

DECLARATIONS.update({'_allocation_mask_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, mask: Long, width: Word=16', 'returns': 'FirstDeploymentFrame', 'flow': 'value = frame.carrier(name) & (1 << width) - 1 & mask\nreturn _allocation_move_fields(memory, frame, name, value, width)'}})

DECLARATIONS.update({'_allocation_arithmetic_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, value: Long, width: Word=16, subtract: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': 'return _scene_render_arithmetic(memory, frame, name, frame.carrier(name) & (1 << width) - 1, value, width, subtract)'}})

DECLARATIONS.update({'_allocation_adjust_ram_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, low: Word, subtract: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': 'return _object_adjust_word_fields(memory, frame, 4294901760 | low, 1, subtract)'}})

DECLARATIONS.update({'_allocation_status_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, value: Word', 'returns': 'FirstDeploymentFrame', 'flow': 'memory.state.set_status_word(value)\nreturn first_replace(frame, status=value & 31)'}})

DECLARATIONS.update({'_allocation_dbword_fields': {'signature': 'frame: FirstDeploymentFrame, name', 'returns': 'tuple[FirstDeploymentFrame, bool]', 'flow': 'value = u16(low16(frame.carrier(name)) - 1)\nreturn (first_replace(frame, **{name: replace_word(frame.carrier(name), value)}), value == 65535)'}})

DECLARATIONS.update({'_allocation_restore_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, names: tuple', 'returns': 'FirstDeploymentFrame', 'flow': "stack = frame.stack_cursor\nchanges = {}\nfor name in names:\n    value = stack.long()\n    stack = stack.advance(4)\n    changes[name] = memory.cursor_at(value) if name in ('roster', 'candidates', 'controller', 'scan', 'opponent', 'scratch', 'auxiliary') else value\nchanges['stack_cursor'] = stack\nreturn first_replace(frame, **changes)"}})

DECLARATIONS.update({'_allocation_fill_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, command: Long, value: Word, count: Word, reset_increment: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': "if reset_increment:\n    frame = _scene_refresh_emit(memory, frame, 12582916, 2, 36610)\nframe = _scene_refresh_emit(memory, frame, 12582916, 4, command)\nframe = first_replace(frame, scratch=memory.cursor_at(12582912))\nframe = _allocation_move_fields(memory, frame, 'offset_y', value)\nframe = _allocation_move_fields(memory, frame, 'choice', count)\nwhile True:\n    frame = _scene_refresh_emit(memory, frame, frame.scratch.base, 2, low16(frame.offset_y))\n    frame, done = _allocation_dbword_fields(frame, 'choice')\n    if done:\n        return frame"}})

DECLARATIONS.update({'_allocation_script_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, source: Long', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_refresh_emit(memory, frame, 16740364, 2, 40960)\nframe = _scene_refresh_emit(memory, frame, 16740366, 4, source)\nframe = _scene_refresh_emit(memory, frame, 16740372, 2, 3)\nreturn _scene_refresh_emit(memory, frame, 16740374, 2, 1)'}})

DECLARATIONS.update({'_allocation_decode_panel_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, source: Long, address: Long, rows: Word, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "frame = first_replace(frame, roster=memory.cursor_at(source), candidates=memory.cursor_at(address))\nframe = _allocation_move_fields(memory, frame, 'offset_x', 128, 32)\nframe = _allocation_store_fields(memory, frame, 32768, 32768)\nframe = _allocation_move_fields(memory, frame, 'offset_y', rows)\nreturn _allocation_call_fields(memory, frame, 240342, continuation)"}})

DECLARATIONS.update({'_allocation_leave_prompt_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _allocation_store_fields(memory, frame, 33082, 0, clear=True)\nframe = _allocation_store_fields(memory, frame, 33084, 6)\nframe = _allocation_store_fields(memory, frame, 33100, 0, clear=True)\nreturn _allocation_call_fields(memory, frame, 262940, 254408)'}})

DECLARATIONS.update({'_allocation_choice_marker_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_scene_flows.business_objects import _append_object_sprite_fields\nframe = _allocation_move_fields(memory, frame, 'target_x', 56)\nframe = _allocation_test_ram_fields(memory, frame, 33090)\nif not frame.status & 4:\n    frame = _allocation_move_fields(memory, frame, 'target_x', 72)\nframe = _allocation_arithmetic_fields(memory, frame, 'target_x', _allocation_read_fields(memory, frame, 4294934560, 2))\nframe = first_replace(frame, roster=memory.cursor_at(254606))\nframe = _allocation_move_fields(memory, frame, 'target_y', 140)\nframe = _allocation_move_fields(memory, frame, 'unit', 260)\nframe = _allocation_move_fields(memory, frame, 'count', 0, 32)\nframe = _allocation_move_fields(memory, frame, 'distance', 1024)\nreturn _append_object_sprite_fields(memory, frame)"}})

DECLARATIONS.update({'_allocation_instruction_at_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, y: Word, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _allocation_ram_move_fields(memory, frame, 'target_x', 32800)\nframe = _allocation_arithmetic_fields(memory, frame, 'target_x', 112)\nframe = _allocation_move_fields(memory, frame, 'target_y', y)\nreturn _allocation_call_fields(memory, frame, 254842, continuation)"}})

DECLARATIONS.update({'_allocation_xor_choice_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'value = _allocation_read_fields(memory, frame, 4294934850, 2) ^ 1\nreturn _allocation_store_fields(memory, frame, 33090, value)'}})

DECLARATIONS.update({'_allocation_link_clear_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "for low in (32970, 32972, 32974, 32976):\n    frame = _allocation_store_fields(memory, frame, low, 65535)\nreturn _allocation_move_fields(memory, frame, 'target_x', 1, 32)"}})

DECLARATIONS.update({'begin_scene_palette_lighten_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 240184)\nframe = _allocation_ram_move_fields(memory, frame, 'target_y', 32964)\nif not frame.status & 8:\n    frame = _allocation_mask_fields(memory, frame, 'target_y', 65280)\n    frame = _movement_compare(memory.state, frame, low16(frame.target_y), 256, 16)\n    if frame.status & 4:\n        return _allocation_known_fields(memory, frame, 240056)\n    frame = _scene_render_push_longs(memory, frame, (frame.target_x,))\n    frame = _allocation_call_fields(memory, frame, 240286, 240212)\n    frame = _allocation_restore_fields(memory, frame, ('target_x',))\nframe = _allocation_mask_fields(memory, frame, 'target_x', 255)\nframe = _allocation_move_fields(memory, frame, 'target_x', low16(frame.target_x) | 256)\nframe = _allocation_store_fields(memory, frame, 32964, low16(frame.target_x))\nframe = _allocation_store_fields(memory, frame, 32966, 0)\nframe = _allocation_store_fields(memory, frame, 32968, 0)\nframe = _allocation_call_fields(memory, frame, 240248, 240244)\nreturn _allocation_known_fields(memory, frame, 239992)"}})

DECLARATIONS.update({'_allocation_palette_copy_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, restore: bool', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 240286 if restore else 240248)\nframe = _allocation_move_fields(memory, frame, 'target_y', 31, 32)\nframe = first_replace(frame, roster=memory.cursor_at(4294966144 if restore else 4294966016), candidates=memory.cursor_at(4294966016 if restore else 4294966144))\nwhile True:\n    value = frame.roster.long()\n    frame = first_replace(frame, roster=frame.roster.advance(4))\n    frame = _scene_refresh_emit(memory, frame, frame.candidates.base, 4, value)\n    frame = first_replace(frame, candidates=frame.candidates.advance(4))\n    frame, done = _allocation_dbword_fields(frame, 'target_y')\n    if done:\n        break\nreturn _allocation_store_fields(memory, frame, 32964, 65535) if restore else frame"}})

DECLARATIONS.update({'snapshot_scene_palette_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _allocation_palette_copy_fields(memory, frame, False)'}})

DECLARATIONS.update({'restore_scene_palette_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _allocation_palette_copy_fields(memory, frame, True)'}})

DECLARATIONS.update({'append_decimal_digit_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 242454)\nframe = _movement_divu_word(memory.state, frame, 'target_x', low16(frame.unit), 242454)\nframe = _scene_refresh_emit(memory, frame, frame.roster.base, 1, low8(frame.target_x))\nframe = first_replace(frame, roster=frame.roster.advance(1))\nframe = _allocation_move_fields(memory, frame, 'target_x', 0)\nreturn _allocation_move_fields(memory, frame, 'target_x', swap_words(frame.target_x), 32)"}})

DECLARATIONS.update({'encode_six_decimal_digits_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 242392)\nframe = _allocation_move_fields(memory, frame, 'unit', 0)\nframe = first_replace(frame, roster=memory.cursor_at(4294934528))\nwhile True:\n    frame = _allocation_arithmetic_fields(memory, frame, 'target_x', 100000, 32, True)\n    if frame.status & 1:\n        break\n    frame = _allocation_arithmetic_fields(memory, frame, 'unit', 1)\nframe = _allocation_arithmetic_fields(memory, frame, 'target_x', 100000, 32)\nframe = _scene_refresh_emit(memory, frame, frame.roster.base, 1, low8(frame.unit))\nframe = first_replace(frame, roster=frame.roster.advance(1))\nfor divisor, token in ((10000, 242426), (1000, 242434), (100, 242442), (10, 242450)):\n    frame = _allocation_move_fields(memory, frame, 'unit', divisor)\n    frame = _allocation_call_fields(memory, frame, 242454, token)\nframe = _scene_refresh_emit(memory, frame, frame.roster.base, 1, low8(frame.target_x))\nreturn first_replace(frame, roster=frame.roster.advance(1))"}})

APPROVED.setdefault((2, 'high_level_scene_flows.business_objects'), set()).add('_append_object_sprite_fields')
DECLARATIONS.update({'append_early_scene_instruction_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_scene_flows.business_objects import _append_object_sprite_fields\nframe = _scene_rule_frame_fields(memory, frame, 254842)\nframe = first_replace(frame, roster=memory.cursor_at(254870))\nframe = _allocation_move_fields(memory, frame, 'unit', 260)\nframe = _allocation_move_fields(memory, frame, 'count', 0, 32)\nframe = _allocation_move_fields(memory, frame, 'distance', 1024)\nreturn _append_object_sprite_fields(memory, frame)"}})

DECLARATIONS.update({'paint_scene_number_row_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 255034)\nframe = _scene_render_push_longs(memory, frame, (frame.target_y, frame.target_x))\nframe = _scene_refresh_emit(memory, frame, 12582916, 2, 36610)\nframe = _allocation_call_fields(memory, frame, 242352, 255050)\nframe = _allocation_restore_fields(memory, frame, ('target_x', 'target_y'))\nframe = _allocation_move_fields(memory, frame, 'unit', 5, 32)\nwhile True:\n    frame = _scene_refresh_emit(memory, frame, 12582912, 2, 58461)\n    frame, done = _allocation_dbword_fields(frame, 'unit')\n    if done:\n        return frame"}})

DECLARATIONS.update({'paint_scene_number_rows_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 255018)\nframe = _allocation_move_fields(memory, frame, 'target_y', 7, 32)\nwhile True:\n    frame = _allocation_call_fields(memory, frame, 255034, 255024)\n    frame = _allocation_arithmetic_fields(memory, frame, 'target_x', 128)\n    frame, done = _allocation_dbword_fields(frame, 'target_y')\n    if done:\n        return frame"}})

DECLARATIONS.update({'_allocation_initialize_panel_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, role', 'returns': 'FirstDeploymentFrame', 'flow': "token, script, substate, background_token, portrait = {'favorable': (253368, 242750, 4, 253456, True), 'ordinary': (253512, 242568, 1, 253600, False), 'other_mode': (253642, 242568, None, 253724, False), 'allocation_mode': (254296, 242750, 3, 254384, False)}[role]\nframe = _allocation_status_fields(memory, frame, 9984)\nframe = _allocation_decode_panel_fields(memory, frame, 283548, 49152, 18, token)\nframe = _allocation_store_fields(memory, frame, 33046, 0 if role == 'allocation_mode' else 1)\nframe = _allocation_fill_fields(memory, frame, 1610612738, 13107, 3455, True)\nframe = _allocation_script_fields(memory, frame, script)\nif substate is not None:\n    frame = _allocation_store_fields(memory, frame, 33084, substate)\nframe = _allocation_call_fields(memory, frame, 256738, background_token)\nif portrait:\n    frame = _allocation_ram_move_fields(memory, frame, 'target_x', 32992)\n    frame = _allocation_move_fields(memory, frame, 'target_y', 1152)\n    frame = _allocation_call_fields(memory, frame, 418260, 253470)\nif substate is None:\n    frame = _allocation_adjust_ram_fields(memory, frame, 33084)\nreturn _allocation_status_fields(memory, frame, 9472)"}})

DECLARATIONS.update({'initialize_early_scene_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 253176)\nframe = _allocation_test_ram_fields(memory, frame, 32986, 8)\nif not frame.status & 4:\n    frame = _allocation_compare_ram_fields(memory, frame, 32986, 3, 8)\n    if not frame.status & 4:\n        frame = _allocation_compare_ram_fields(memory, frame, 32986, 1, 8)\n        return _allocation_initialize_panel_fields(memory, frame, 'other_mode')\nframe = first_replace(frame, roster=memory.cursor_at(4294952704))\nframe = _allocation_move_fields(memory, frame, 'target_y', 0, 32)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32992)\nframe = _allocation_move_fields(memory, frame, 'target_y', frame.roster.byte(low16(frame.target_x)), 8)\nframe = _allocation_mask_fields(memory, frame, 'target_y', 3)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32994)\nframe = _allocation_move_fields(memory, frame, 'target_x', frame.roster.byte(low16(frame.target_x)), 8)\nframe = _allocation_mask_fields(memory, frame, 'target_x', 3)\nframe = _allocation_arithmetic_fields(memory, frame, 'target_y', low8(frame.target_x), 8, True)\nframe = _allocation_arithmetic_fields(memory, frame, 'target_y', 1)\nframe = _movement_compare(memory.state, frame, low16(frame.target_y), 2, 16)\nif not frame.status & 5:\n    return _allocation_initialize_panel_fields(memory, frame, 'ordinary')\nfor own, extra, other in ((33038, 10, 33036), (33030, 20, 33028)):\n    frame = _allocation_ram_move_fields(memory, frame, 'target_x', own)\n    frame = _allocation_arithmetic_fields(memory, frame, 'target_x', extra)\n    frame = _movement_compare(memory.state, frame, low16(frame.target_x), _allocation_read_fields(memory, frame, 4294901760 | other, 2), 16)\n    if frame.status & 1:\n        return _allocation_initialize_panel_fields(memory, frame, 'ordinary')\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32998)\nframe = _movement_compare(memory.state, frame, low16(frame.target_x), _allocation_read_fields(memory, frame, 4294934756, 2), 16)\nif not frame.status & 1:\n    return _allocation_initialize_panel_fields(memory, frame, 'ordinary')\nframe = _allocation_call_fields(memory, frame, 243490, 253324)\nframe = _allocation_mask_fields(memory, frame, 'target_x', 3)\nreturn _allocation_initialize_panel_fields(memory, frame, 'favorable' if frame.status & 4 else 'ordinary')"}})

DECLARATIONS.update({'_allocation_contested_roll_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'tuple[FirstDeploymentFrame, bool]', 'flow': "frame = _allocation_move_fields(memory, frame, 'target_y', 0, 32)\nframe = _allocation_move_fields(memory, frame, 'unit', 0, 32)\nframe = first_replace(frame, roster=memory.cursor_at(4294952704))\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32992)\nframe = _allocation_move_fields(memory, frame, 'target_x', frame.roster.byte(low16(frame.target_x)), 8)\nframe = _allocation_mask_fields(memory, frame, 'target_x', 3)\nframe = _allocation_move_fields(memory, frame, 'target_y', 5, 32)\nframe = _allocation_arithmetic_fields(memory, frame, 'target_y', low8(frame.target_x), 8, True)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32994)\nframe = _allocation_move_fields(memory, frame, 'target_x', frame.roster.byte(low16(frame.target_x)), 8)\nframe = _allocation_move_fields(memory, frame, 'unit', 5, 32)\nframe = _allocation_arithmetic_fields(memory, frame, 'unit', low8(frame.target_x), 8, True)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 33028)\nframe = _movement_multiply_word(memory.state, frame, 'target_y', low16(frame.target_x))\nframe = _movement_multiply_word(memory.state, frame, 'target_y', 100)\nframe = _allocation_call_fields(memory, frame, 243490, 253836)\nframe = _allocation_mask_fields(memory, frame, 'target_x', 31)\nframe = _allocation_arithmetic_fields(memory, frame, 'target_x', 20)\nframe = _allocation_arithmetic_fields(memory, frame, 'target_x', _allocation_read_fields(memory, frame, 4294934790, 2))\nframe = _movement_multiply_word(memory.state, frame, 'unit', low16(frame.target_x))\nframe = _movement_divu_word(memory.state, frame, 'target_y', low16(frame.unit), 253850)\nframe = _movement_compare(memory.state, frame, low16(frame.target_y), 100, 16)\nif not frame.status & 5:\n    return (frame, True)\nwhile True:\n    frame = _allocation_call_fields(memory, frame, 243490, 253864)\n    frame = _allocation_mask_fields(memory, frame, 'target_x', 127)\n    frame = _movement_compare(memory.state, frame, low16(frame.target_x), 100, 16)\n    if frame.status & 5:\n        break\nframe = _movement_compare(memory.state, frame, low16(frame.target_x), low16(frame.target_y), 16)\nif not frame.status & 5:\n    return (frame, False)\nframe = _allocation_call_fields(memory, frame, 243490, 253884)\nframe = _allocation_ram_move_fields(memory, frame, 'target_y', 61394)\nframe = first_replace(frame, roster=memory.cursor_at(254082))\nframe = _allocation_mask_fields(memory, frame, 'target_x', frame.roster.byte(low16(frame.target_y)), 8)\nreturn (frame, bool(frame.status & 4))"}})

DECLARATIONS.update({'_allocation_show_choice_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, accepted: bool', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _allocation_store_fields(memory, frame, 33090, 0 if accepted else 1, clear=accepted)\nframe = _allocation_fill_fields(memory, frame, 1073741827, 1024, 1215)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32992)\nframe = _allocation_move_fields(memory, frame, 'target_y', 1152)\nframe = _allocation_call_fields(memory, frame, 418260, 253950 if accepted else 254136)\nif accepted:\n    frame = _allocation_move_fields(memory, frame, 'target_x', 49954)\n    frame = _allocation_call_fields(memory, frame, 255018, 253958)\nframe = _allocation_fill_fields(memory, frame, 1610612738, 13107, 3455, True)\nframe = _scene_refresh_emit(memory, frame, 16740364, 2, 40960)\nframe = _scene_refresh_emit(memory, frame, 16740372, 2, 3)\nframe = _scene_refresh_emit(memory, frame, 16740374, 2, 1)\nframe = _allocation_adjust_ram_fields(memory, frame, 33084)\nframe = _scene_refresh_emit(memory, frame, 16740366, 4, 242680 if accepted else 242620)\nframe = first_replace(frame, roster=memory.cursor_at(4294952704))\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32994)\nframe = _allocation_move_fields(memory, frame, 'target_y', frame.roster.byte(low16(frame.target_x)), 8)\nframe = _allocation_mask_fields(memory, frame, 'target_y', 3)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32992)\nframe = _allocation_move_fields(memory, frame, 'target_x', frame.roster.byte(low16(frame.target_x)), 8)\nframe = _allocation_mask_fields(memory, frame, 'target_x' if accepted else 'target_y', 3)\nframe = _movement_compare(memory.state, frame, low8(frame.target_y), low8(frame.target_x), 8)\nif not frame.status & 1:\n    frame = _scene_refresh_emit(memory, frame, 16740366, 4, 242602 if accepted else 242654)\nreturn _allocation_status_fields(memory, frame, 9472)"}})

DECLARATIONS.update({'process_early_scene_choice_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 253180)\nframe, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934815, 5)\nif not pressed:\n    return draw_early_scene_choice_fields(memory, frame)\nframe = _allocation_move_fields(memory, frame, 'target_x', 172)\nframe = _allocation_call_fields(memory, frame, 32906, 253754)\nframe = _allocation_test_ram_fields(memory, frame, 33090)\nif not frame.status & 4:\n    return _allocation_leave_prompt_fields(memory, frame)\nframe = _allocation_compare_ram_fields(memory, frame, 32986, 1, 8)\nif not frame.status & 4:\n    frame = _allocation_compare_ram_fields(memory, frame, 32986, 2, 8)\nif frame.status & 4:\n    return _allocation_initialize_panel_fields(memory, frame, 'allocation_mode')\nframe = _allocation_status_fields(memory, frame, 9984)\nframe, accepted = _allocation_contested_roll_fields(memory, frame)\nreturn _allocation_show_choice_fields(memory, frame, accepted)"}})

DECLARATIONS.update({'draw_early_scene_choice_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 254548)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 33055, 8)\nframe = _allocation_mask_fields(memory, frame, 'target_x', 3)\nif not frame.status & 4:\n    frame = _allocation_xor_choice_fields(memory, frame)\nreturn _allocation_choice_marker_fields(memory, frame)"}})

DECLARATIONS.update({'present_early_scene_prompt_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 253184)\nframe, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934815, 5)\nif pressed:\n    frame = _allocation_test_ram_fields(memory, frame, 33090)\n    if not frame.status & 4:\n        return _allocation_leave_prompt_fields(memory, frame)\n    frame = _allocation_call_fields(memory, frame, 258270, 254432)\n    frame = _allocation_store_fields(memory, frame, 33082, 8)\n    frame = _allocation_store_fields(memory, frame, 33084, 5)\nframe = _allocation_instruction_at_fields(memory, frame, 160, 254460)\nframe = _allocation_move_fields(memory, frame, 'target_x', 49954)\nreturn _allocation_call_fields(memory, frame, 255018, 254468)"}})

DECLARATIONS.update({'finish_early_scene_prompt_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 253188)\nframe = _allocation_test_ram_fields(memory, frame, 32986, 8)\nspecial = bool(frame.status & 4)\nif not special:\n    frame = _allocation_compare_ram_fields(memory, frame, 32986, 3, 8)\n    special = bool(frame.status & 4)\nif special:\n    frame = _allocation_instruction_at_fields(memory, frame, 256, 254510)\n    frame = _allocation_move_fields(memory, frame, 'target_x', 49978)\n    frame = _allocation_call_fields(memory, frame, 255018, 254518)\nelse:\n    frame = _allocation_store_fields(memory, frame, 33054, _allocation_read_fields(memory, frame, 4294934816, 2))\nframe, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934815, 5)\nif pressed:\n    frame = _allocation_test_ram_fields(memory, frame, 33090)\n    if not frame.status & 4:\n        return _allocation_leave_prompt_fields(memory, frame)\n    frame = _allocation_call_fields(memory, frame, 258270, 254540)\n    return _allocation_store_fields(memory, frame, 33084, 6)\nreturn draw_early_scene_choice_fields(memory, frame)"}})

DECLARATIONS.update({'wait_early_scene_choice_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 253192)\nframe = _allocation_instruction_at_fields(memory, frame, 256, 254632)\nframe = _allocation_move_fields(memory, frame, 'target_x', 49978)\nframe = _allocation_call_fields(memory, frame, 255018, 254640)\nframe = _allocation_call_fields(memory, frame, 254548, 254644)\nframe = _allocation_adjust_ram_fields(memory, frame, 33092)\nframe = _allocation_compare_ram_fields(memory, frame, 33092, 64)\nif frame.status & 1:\n    return frame\nframe = _allocation_status_fields(memory, frame, 9984)\nframe = _allocation_fill_fields(memory, frame, 1610612738, 13107, 3455, True)\nframe = _allocation_script_fields(memory, frame, 242718)\nframe = _allocation_store_fields(memory, frame, 33084, 3)\nreturn _allocation_status_fields(memory, frame, 9472)"}})

DECLARATIONS.update({'_allocation_finish_fade_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame, finished = _scene_rule_input_bit_fields(memory, frame, 4294934724, 7)\nif finished:\n    frame = _allocation_store_fields(memory, frame, 33082, 3)\n    frame = _allocation_store_fields(memory, frame, 33084, 3)\nreturn frame'}})

DECLARATIONS.update({'finish_early_scene_fade_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 253196)\nframe = _allocation_instruction_at_fields(memory, frame, 160, 254762)\nreturn _allocation_finish_fade_fields(memory, frame)'}})

DECLARATIONS.update({'finish_alternate_scene_fade_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 253200)\nframe = _allocation_compare_ram_fields(memory, frame, 32986, 1, 8)\nif not frame.status & 4:\n    frame = _allocation_compare_ram_fields(memory, frame, 32986, 2, 8)\n    if not frame.status & 4:\n        frame = _allocation_instruction_at_fields(memory, frame, 256, 254818)\nreturn _allocation_finish_fade_fields(memory, frame)'}})

DECLARATIONS.update({'wait_exchange_scene_transition_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 255084)\nframe = _allocation_adjust_ram_fields(memory, frame, 33090)\nframe = _allocation_compare_ram_fields(memory, frame, 33090, 32)\nif frame.status & 1:\n    return frame\nframe = _allocation_status_fields(memory, frame, 9984)\nframe = _allocation_store_fields(memory, frame, 33090, 0, clear=True)\nframe = _allocation_adjust_ram_fields(memory, frame, 33084)\nframe = _allocation_decode_panel_fields(memory, frame, 284735, 49152, 18, 255154)\nframe = _allocation_fill_fields(memory, frame, 1610612738, 13107, 3455, True)\nframe = _allocation_script_fields(memory, frame, 242886)\nframe = _allocation_store_fields(memory, frame, 33046, 1)\nframe = _allocation_call_fields(memory, frame, 256738, 255236)\nreturn _allocation_status_fields(memory, frame, 9472)'}})

DECLARATIONS.update({'process_exchange_scene_choice_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, 255088)\nframe, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934813, 5)\nif not pressed:\n    frame = _allocation_ram_move_fields(memory, frame, 'target_x', 33053, 8)\n    frame = _allocation_mask_fields(memory, frame, 'target_x', 3)\n    if not frame.status & 4:\n        frame = _allocation_xor_choice_fields(memory, frame)\n    return _allocation_choice_marker_fields(memory, frame)\nframe = _allocation_move_fields(memory, frame, 'target_x', 172)\nframe = _allocation_call_fields(memory, frame, 32906, 255262)\nframe = _allocation_test_ram_fields(memory, frame, 33090)\nif frame.status & 4:\n    frame = _allocation_store_fields(memory, frame, 33090, 0, clear=True)\n    frame = _allocation_store_fields(memory, frame, 33082, 7)\n    frame = _allocation_store_fields(memory, frame, 33084, 0, clear=True)\n    frame = _allocation_store_fields(memory, frame, 33100, 0, clear=True)\n    frame = _allocation_call_fields(memory, frame, 262940, 255292)\n    return _allocation_store_fields(memory, frame, 33802, 0, clear=True)\nframe = _allocation_status_fields(memory, frame, 9984)\nframe = _allocation_compare_ram_fields(memory, frame, 32986, 0, 8)\nif not frame.status & 4:\n    frame = _allocation_compare_ram_fields(memory, frame, 32986, 3, 8)\n    if not frame.status & 4:\n        frame = _allocation_call_fields(memory, frame, 268312, 255344)\nframe = _allocation_call_fields(memory, frame, 255720, 255348)\nframe = _allocation_call_fields(memory, frame, 255918, 255352)\nframe = _allocation_call_fields(memory, frame, 268312, 255356)\nframe = first_replace(frame, roster=memory.cursor_at(4294934890))\nframe = _allocation_move_fields(memory, frame, 'target_y', 15)\nwhile True:\n    frame = _allocation_move_fields(memory, frame, 'target_x', 352)\n    frame = _allocation_arithmetic_fields(memory, frame, 'target_x', frame.roster.word(2), subtract=True)\n    frame = _scene_refresh_emit(memory, frame, frame.roster.base + 2, 2, low16(frame.target_x))\n    frame = _scene_refresh_emit(memory, frame, frame.roster.base + 6, 2, 1)\n    frame = _scene_refresh_emit(memory, frame, frame.roster.base + 8, 2, 1)\n    frame = first_replace(frame, roster=frame.roster.advance(16))\n    frame, done = _allocation_dbword_fields(frame, 'target_y')\n    if done:\n        break\nframe = _allocation_call_fields(memory, frame, 255720, 255400)\nframe = _allocation_call_fields(memory, frame, 255918, 255404)\nframe = _allocation_call_fields(memory, frame, 262940, 255408)\nframe = _allocation_store_fields(memory, frame, 33802, 1)\nframe = _allocation_store_fields(memory, frame, 33090, 0, clear=True)\nfor low, value in ((32800, 0), (32804, 0), (32832, 33280), (32826, 33280)):\n    frame = _allocation_store_fields(memory, frame, low, value)\nframe = _allocation_adjust_ram_fields(memory, frame, 33084)\nreturn _allocation_status_fields(memory, frame, 9472)"}})

DECLARATIONS.update({'finish_exchange_scene_transition_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 255092)\nframe = _allocation_compare_ram_fields(memory, frame, 32800, 144)\nif frame.status & 1:\n    return frame\nframe = _allocation_store_fields(memory, frame, 32832, 0)\nframe = _allocation_store_fields(memory, frame, 32826, 0)\nframe = _allocation_adjust_ram_fields(memory, frame, 33090)\nframe = _allocation_compare_ram_fields(memory, frame, 33090, 32)\nif not frame.status & 1:\n    frame = _allocation_store_fields(memory, frame, 33090, 0, clear=True)\n    frame = _allocation_store_fields(memory, frame, 33082, 8)\n    frame = _allocation_store_fields(memory, frame, 33084, 0, clear=True)\n    frame = _allocation_store_fields(memory, frame, 33100, 0, clear=True)\nreturn frame'}})

DECLARATIONS.update({'_allocation_exit_pair_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'for low in (33082, 33084, 33100):\n    frame = _allocation_store_fields(memory, frame, low, 0, clear=True)\nframe = _allocation_call_fields(memory, frame, 262940, 256224)\nframe = _allocation_call_fields(memory, frame, 255720, 256228)\nfor low in (33090, 33092, 33094):\n    frame = _allocation_store_fields(memory, frame, low, 0, clear=True)\nreturn frame'}})

DECLARATIONS.update({'_allocation_finish_class_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _allocation_call_fields(memory, frame, 259378, 257218)\nreturn _allocation_call_fields(memory, frame, 260414, 257222)'}})

DECLARATIONS.update({'_allocation_roster_shares_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, secondary: bool', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _allocation_ram_move_fields(memory, frame, 'target_x', 33030)\nframe = _allocation_ram_move_fields(memory, frame, 'target_y', 33026)\nframe = _movement_multiply_word(memory.state, frame, 'target_y', low16(frame.target_x))\nframe = _movement_divu_word(memory.state, frame, 'target_y', 100, 257060 if secondary else 256010)\nframe = _allocation_move_fields(memory, frame, 'target_x', 14)\nframe = _allocation_ram_move_fields(memory, frame, 'unit', 33010)\nframe = first_replace(frame, auxiliary=memory.cursor_at(4294935162 if secondary else 4294934906))\nwhile True:\n    frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base + 12, 2, low16(frame.target_y))\n    frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base + 14, 2, _allocation_read_fields(memory, frame, 4294934766, 2))\n    frame = _movement_test(memory.state, frame, low16(frame.unit), 16)\n    if not frame.status & 4:\n        frame = _allocation_arithmetic_fields(memory, frame, 'unit', 1, subtract=True)\n        frame = _object_adjust_word_fields(memory, frame, frame.auxiliary.base + 14, 1)\n    frame = first_replace(frame, auxiliary=frame.auxiliary.advance(16))\n    frame, done = _allocation_dbword_fields(frame, 'target_x')\n    if done:\n        return frame"}})

DECLARATIONS.update({'_allocation_confirm_shares_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, secondary: bool', 'returns': 'FirstDeploymentFrame', 'flow': 'if not secondary:\n    frame = _allocation_adjust_ram_fields(memory, frame, 33084)\nframe = _allocation_status_fields(memory, frame, 9984)\nframe = _allocation_roster_shares_fields(memory, frame, secondary)\nframe = _allocation_call_fields(memory, frame, 257224 if secondary else 256160, 257110 if secondary else 256060)\nif secondary:\n    frame = _allocation_adjust_ram_fields(memory, frame, 33084)\nframe = _allocation_fill_fields(memory, frame, 1073741827, 1024, 1215)\nframe = _allocation_fill_fields(memory, frame, 1610612738, 13107, 3455)\nframe = _allocation_script_fields(memory, frame, 242506)\nreturn _allocation_status_fields(memory, frame, 9472)'}})

DECLARATIONS.update({'_allocation_check_commit_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, secondary: bool', 'returns': 'FirstDeploymentFrame', 'flow': "frame, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934815, 5)\nif not pressed:\n    return _allocation_finish_class_fields(memory, frame)\nframe = _allocation_move_fields(memory, frame, 'target_x', 172)\nframe = _allocation_call_fields(memory, frame, 32906, 257016 if secondary else 255962)\nframe = _allocation_compare_ram_fields(memory, frame, 33092, 2)\nif not frame.status & 4:\n    return _allocation_finish_class_fields(memory, frame)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 33018)\nframe = _allocation_arithmetic_fields(memory, frame, 'target_x', _allocation_read_fields(memory, frame, 4294934780, 2))\nframe = _allocation_arithmetic_fields(memory, frame, 'target_x', _allocation_read_fields(memory, frame, 4294934782, 2))\nframe = _movement_compare(memory.state, frame, low16(frame.target_x), _allocation_read_fields(memory, frame, 4294934762, 2), 16)\nif not frame.status & 4:\n    return _allocation_finish_class_fields(memory, frame)\nreturn _allocation_confirm_shares_fields(memory, frame, secondary)"}})

DECLARATIONS.update({'_allocation_prepare_secondary_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _allocation_status_fields(memory, frame, 9984)\nframe = _allocation_store_fields(memory, frame, 33090, 0, clear=True)\nframe = _allocation_adjust_ram_fields(memory, frame, 33084)\nframe = _allocation_call_fields(memory, frame, 259166, 256556)\nframe = _allocation_fill_fields(memory, frame, 1342177282, 13107, 191)\nframe = _scene_refresh_emit(memory, frame, 12582916, 4, 1342177282)\nframe = _allocation_ram_move_fields(memory, frame, 'choice', 32994)\nframe = _allocation_move_fields(memory, frame, 'target_x', 3)\nframe = _allocation_move_fields(memory, frame, 'target_y', 1)\nframe = _allocation_call_fields(memory, frame, 262850, 256614)\nframe = _allocation_decode_panel_fields(memory, frame, 281711, 49152, 18, 256646)\nframe = _allocation_call_fields(memory, frame, 260342, 256650)\nframe = _allocation_fill_fields(memory, frame, 1610612738, 13107, 3455, True)\nframe = _allocation_script_fields(memory, frame, 242464)\nframe = _allocation_store_fields(memory, frame, 33046, 1)\nframe = _allocation_call_fields(memory, frame, 256738, 256732)\nreturn _allocation_status_fields(memory, frame, 9472)"}})

DECLARATIONS.update({'process_pair_phase_counter_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 255522)\nframe = _allocation_compare_ram_fields(memory, frame, 32986, 1, 8)\nif not frame.status & 4:\n    frame = _allocation_compare_ram_fields(memory, frame, 32986, 2, 8)\n    if not frame.status & 4:\n        frame = _allocation_store_fields(memory, frame, 33082, 0, clear=True)\n        return _allocation_store_fields(memory, frame, 33084, 0, clear=True)\nframe = _allocation_adjust_ram_fields(memory, frame, 33090)\nframe = _allocation_compare_ram_fields(memory, frame, 33090, 64)\nif frame.status & 1:\n    return frame\nframe = _allocation_call_fields(memory, frame, 255720, 255696)\nframe = _allocation_test_ram_fields(memory, frame, 32998)\nif not frame.status & 4:\n    return _allocation_prepare_secondary_fields(memory, frame)\nframe = _allocation_call_fields(memory, frame, 256160, 255706)\nframe = _allocation_call_fields(memory, frame, 259822, 255710)\nreturn _allocation_exit_pair_fields(memory, frame)'}})

DECLARATIONS.update({'confirm_pair_allocation_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'frame = _scene_rule_frame_fields(memory, frame, 255526)\n'
                                            'frame = _allocation_call_fields(memory, frame, 259352, 256808)\n'
                                            'frame = _allocation_call_fields(memory, frame, 259166, 256812)\n'
                                            'frame = _allocation_call_fields(memory, frame, 260342, 256816)\n'
                                            'frame, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934815, '
                                            '5)\n'
                                            'if not pressed:\n'
                                            '    return frame\n'
                                            "frame = _allocation_move_fields(memory, frame, 'target_x', 172)\n"
                                            'frame = _allocation_call_fields(memory, frame, 32906, 256834)\n'
                                            'frame = _allocation_adjust_ram_fields(memory, frame, 33084)\n'
                                            'frame = _allocation_store_fields(memory, frame, 33092, 0, clear=True)\n'
                                            'frame = _allocation_compare_ram_fields(memory, frame, 32987, 3, 8)\n'
                                            'if frame.status & 4:\n'
                                            '    frame = _allocation_store_fields(memory, frame, 33018, 0, '
                                            'clear=True)\n'
                                            '    frame = _allocation_store_fields(memory, frame, 33020, '
                                            '_allocation_read_fields(memory, frame, 4294934762, 2))\n'
                                            '    frame = _allocation_store_fields(memory, frame, 33022, 0, '
                                            'clear=True)\n'
                                            '    frame = _allocation_compare_ram_fields(memory, frame, 33082, 7)\n'
                                            '    return _allocation_confirm_shares_fields(memory, frame, not '
                                            'bool(frame.status & 4))\n'
                                            'frame = _allocation_status_fields(memory, frame, 9984)\n'
                                            'frame = _allocation_decode_panel_fields(memory, frame, 282054, 49152, 18, '
                                            '256914)\n'
                                            'frame = _allocation_call_fields(memory, frame, 260414, 256918)\n'
                                            'frame = _allocation_fill_fields(memory, frame, 1610612738, 13107, 3455, '
                                            'True)\n'
                                            'frame = _allocation_script_fields(memory, frame, 242486)\n'
                                            'return _allocation_status_fields(memory, frame, 9472)'}})

DECLARATIONS.update({'update_pair_allocation_input_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                         'returns': 'FirstDeploymentFrame',
                                         'flow': 'frame = _scene_rule_frame_fields(memory, frame, 255530)\n'
                                                 'return _allocation_check_commit_fields(memory, frame, False)'}})

DECLARATIONS.update({'exit_pair_allocation_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                 'returns': 'FirstDeploymentFrame',
                                 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 255534)\n'
                                         'frame = _allocation_call_fields(memory, frame, 259778, 256184)\n'
                                         "frame = _allocation_ram_move_fields(memory, frame, 'target_x', 33055, 8)\n"
                                         "frame = _allocation_mask_fields(memory, frame, 'target_x', 12)\n"
                                         'if not frame.status & 4:\n'
                                         '    frame = _allocation_call_fields(memory, frame, 262940, 256198)\n'
                                         'return frame'}})

DECLARATIONS.update({'wait_pair_stage_motion_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 256256)\nframe = _allocation_adjust_ram_fields(memory, frame, 33090)\nframe = _allocation_compare_ram_fields(memory, frame, 33090, 64)\nif frame.status & 1:\n    return frame\nframe = _allocation_store_fields(memory, frame, 33090, 0, clear=True)\nfor low, value in ((32800, 0), (32804, 0), (32832, 33280), (32826, 33280)):\n    frame = _allocation_store_fields(memory, frame, low, value)\nreturn _allocation_adjust_ram_fields(memory, frame, 33084)'}})

DECLARATIONS.update({'advance_pair_stage_motion_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _scene_rule_frame_fields(memory, frame, 256260)\nframe = _allocation_compare_ram_fields(memory, frame, 32800, 144)\nif frame.status & 1:\n    return frame\nframe = _allocation_store_fields(memory, frame, 32832, 0)\nframe = _allocation_store_fields(memory, frame, 32826, 0)\nframe = _allocation_adjust_ram_fields(memory, frame, 33090)\nframe = _allocation_compare_ram_fields(memory, frame, 33090, 32)\nif frame.status & 1:\n    return frame\nframe = _allocation_test_ram_fields(memory, frame, 32998)\nif not frame.status & 4:\n    return _allocation_prepare_secondary_fields(memory, frame)\nfor low in (33002, 33006, 33010, 33018, 33020, 33022, 33090):\n    frame = _allocation_store_fields(memory, frame, low, 0, clear=True)\nframe = _allocation_call_fields(memory, frame, 257224, 256516)\nframe = _allocation_call_fields(memory, frame, 259656, 256520)\nframe = _allocation_store_fields(memory, frame, 33082, 8)\nframe = _allocation_store_fields(memory, frame, 33084, 0, clear=True)\nframe = _allocation_store_fields(memory, frame, 33100, 0, clear=True)\nreturn _allocation_call_fields(memory, frame, 262940, 256538)'}})

DECLARATIONS.update({'confirm_second_pair_allocation_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                           'returns': 'FirstDeploymentFrame',
                                           'flow': 'frame = _scene_rule_frame_fields(memory, frame, 256264)\n'
                                                   'frame = _allocation_call_fields(memory, frame, 259352, 256808)\n'
                                                   'frame = _allocation_call_fields(memory, frame, 259166, 256812)\n'
                                                   'frame = _allocation_call_fields(memory, frame, 260342, 256816)\n'
                                                   'frame, pressed = _scene_rule_input_bit_fields(memory, frame, '
                                                   '4294934815, 5)\n'
                                                   'if not pressed:\n'
                                                   '    return frame\n'
                                                   "frame = _allocation_move_fields(memory, frame, 'target_x', 172)\n"
                                                   'frame = _allocation_call_fields(memory, frame, 32906, 256834)\n'
                                                   'frame = _allocation_adjust_ram_fields(memory, frame, 33084)\n'
                                                   'frame = _allocation_store_fields(memory, frame, 33092, 0, '
                                                   'clear=True)\n'
                                                   'frame = _allocation_compare_ram_fields(memory, frame, 32987, 3, '
                                                   '8)\n'
                                                   'if frame.status & 4:\n'
                                                   '    frame = _allocation_store_fields(memory, frame, 33018, 0, '
                                                   'clear=True)\n'
                                                   '    frame = _allocation_store_fields(memory, frame, 33020, '
                                                   '_allocation_read_fields(memory, frame, 4294934762, 2))\n'
                                                   '    frame = _allocation_store_fields(memory, frame, 33022, 0, '
                                                   'clear=True)\n'
                                                   '    frame = _allocation_compare_ram_fields(memory, frame, 33082, '
                                                   '7)\n'
                                                   '    return _allocation_confirm_shares_fields(memory, frame, not '
                                                   'bool(frame.status & 4))\n'
                                                   'frame = _allocation_status_fields(memory, frame, 9984)\n'
                                                   'frame = _allocation_decode_panel_fields(memory, frame, 282054, '
                                                   '49152, 18, 256914)\n'
                                                   'frame = _allocation_call_fields(memory, frame, 260414, 256918)\n'
                                                   'frame = _allocation_fill_fields(memory, frame, 1610612738, 13107, '
                                                   '3455, True)\n'
                                                   'frame = _allocation_script_fields(memory, frame, 242486)\n'
                                                   'return _allocation_status_fields(memory, frame, 9472)'}})

DECLARATIONS.update({'present_pair_stage_summary_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'frame = _scene_rule_frame_fields(memory, frame, 256268)\n'
                                               'return _allocation_check_commit_fields(memory, frame, True)'}})

DECLARATIONS.update({'_allocation_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, entry: Long, base: Long, gather: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_rule_frame_fields(memory, frame, entry)\nframe = _allocation_call_fields(memory, frame, gather, continuation)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 33084)\nframe = _scene_render_asl_word(memory, frame, 'target_x', low16(frame.target_x), 2)\nreturn _allocation_known_fields(memory, frame, u32(base + s16(low16(frame.target_x))))"}})

DECLARATIONS.update({'step_result_scene_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _allocation_phase_fields(memory, frame, 253126, 257926, 256284, 257916)'}})

DECLARATIONS.update({'step_confirmation_scene_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _allocation_phase_fields(memory, frame, 253130, 258096, 256284, 258086)'}})

DECLARATIONS.update({'step_transfer_scene_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _allocation_phase_fields(memory, frame, 253134, 258146, 256284, 258136)'}})

DECLARATIONS.update({'step_primary_detail_scene_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _allocation_phase_fields(memory, frame, 253138, 258538, 256284, 258528)'}})

DECLARATIONS.update({'step_secondary_detail_scene_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _allocation_phase_fields(memory, frame, 253142, 258716, 256284, 258706)'}})

DECLARATIONS.update({'step_summary_scene_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _allocation_phase_fields(memory, frame, 253146, 258894, 256284, 258884)'}})

DECLARATIONS.update({'step_pair_transition_scene_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _allocation_phase_fields(memory, frame, 253150, 255522, 255538, 255512)'}})

DECLARATIONS.update({'step_initial_scene_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _allocation_phase_fields(memory, frame, 253154, 253176, 256284, 253166)'}})

DECLARATIONS.update({'step_exchange_scene_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _allocation_phase_fields(memory, frame, 253158, 255084, 255538, 255074)'}})

DECLARATIONS.update({'_allocation_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "if (target, continuation) not in ((32906, 253754), (32906, 255262), (32906, 255962), (32906, 256834), (32906, 257016), (240184, 258304), (240184, 258700), (240184, 258878), (240184, 259164), (240248, 240244), (240286, 240212), (240342, 253368), (240342, 253512), (240342, 253642), (240342, 254296), (240342, 255154), (240342, 256646), (240342, 256770), (240342, 256802), (240342, 256914), (242352, 255050), (242352, 260880), (242352, 260914), (242352, 260954), (242352, 260984), (242352, 261020), (242352, 261060), (242352, 261090), (242352, 261126), (242352, 261166), (242352, 261196), (242352, 261232), (242352, 261270), (242352, 261530), (242352, 261564), (242352, 261604), (242352, 261630), (242352, 261666), (242352, 261706), (242352, 261982), (242352, 262010), (242392, 260352), (242392, 260376), (242392, 260400), (242392, 260424), (242392, 260448), (242392, 260486), (242392, 260526), (242392, 260668), (242392, 260722), (242392, 260776), (242392, 260828), (242392, 261424), (242392, 261478), (242392, 261736), (242392, 261760), (242392, 261784), (242392, 261808), (242392, 261832), (242392, 261856), (242392, 261902), (242392, 261948), (242454, 242426), (242454, 242434), (242454, 242442), (242454, 242450), (243490, 253324), (243490, 253836), (243490, 253864), (243490, 253884), (254548, 254644), (254842, 254460), (254842, 254510), (254842, 254632), (254842, 254762), (254842, 254818), (255018, 253958), (255018, 254468), (255018, 254518), (255018, 254640), (255034, 255024), (255538, 255074), (255538, 255512), (255720, 255348), (255720, 255400), (255720, 255696), (255720, 256228), (255918, 255352), (255918, 255404), (256160, 255706), (256160, 256060), (256284, 253166), (256284, 257916), (256284, 258086), (256284, 258136), (256284, 258528), (256284, 258706), (256284, 258884), (256738, 253456), (256738, 253600), (256738, 253724), (256738, 254384), (256738, 255236), (256738, 256732), (256738, 258014), (256738, 258242), (256738, 258634), (256738, 258812), (256738, 259000), (257224, 256516), (257224, 257110), (258270, 254432), (258270, 254540), (259166, 256556), (259166, 256812), (259352, 256808), (259378, 257218), (259656, 256520), (259778, 256184), (259822, 255710), (259936, 258046), (260316, 258274), (260316, 258666), (260316, 258848), (260316, 259134), (260342, 256650), (260342, 256816), (260414, 256918), (260414, 257222), (260550, 258050), (260658, 260610), (261288, 260928), (261288, 260958), (261288, 261034), (261288, 261064), (261288, 261140), (261288, 261170), (261288, 261246), (261288, 261274), (261288, 261578), (261288, 261608), (261288, 261680), (261288, 261710), (261304, 260936), (261304, 260966), (261304, 261042), (261304, 261072), (261304, 261148), (261304, 261178), (261304, 261252), (261304, 261280), (261304, 261586), (261304, 261616), (261304, 261688), (261304, 261718), (261414, 261380), (261962, 260468), (261962, 260508), (261998, 260366), (261998, 260390), (261998, 260438), (261998, 260476), (261998, 260516), (261998, 260682), (261998, 260736), (261998, 260790), (261998, 260842), (261998, 261438), (261998, 261492), (261998, 261750), (261998, 261774), (261998, 261798), (261998, 261822), (261998, 261846), (261998, 261870), (261998, 261916), (262850, 256614), (262940, 254408), (262940, 255292), (262940, 255408), (262940, 256198), (262940, 256224), (262940, 256538), (262940, 258064), (262940, 258114), (268312, 255344), (268312, 255356), (418260, 253470), (418260, 253950), (418260, 254136)):\n    raise ValueError('actual C52 target and caller return token required')\ndef child(actual_memory, entered):\n    return _allocation_known_fields(memory, entered, target, continuation)\nreturn _presentation_call_fields(BattlePresentationMemory(memory.state), frame, continuation, child)"}})

DECLARATIONS.update({'_allocation_known_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long | None=None', 'returns': 'FirstDeploymentFrame', 'flow': 'if target == 32906:\n    from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields\n    return enqueue_sound_command_fields(memory, frame)\nif target == 239522:\n    from ..high_level_scene_flows.business_scene import append_unclipped_scene_sprites_fields\n    return append_unclipped_scene_sprites_fields(memory, frame)\nif target == 239992:\n    from ..high_level_scene_flows.business_scene import advance_scene_palette_fade_fields\n    return advance_scene_palette_fade_fields(memory, frame)\nif target == 240184:\n    return begin_scene_palette_lighten_fields(memory, frame)\nif target == 240248:\n    return snapshot_scene_palette_fields(memory, frame)\nif target == 240286:\n    return restore_scene_palette_fields(memory, frame)\nif target == 242352:\n    from ..high_level_scene_flows.business_scene import set_vram_write_address_fields\n    return set_vram_write_address_fields(memory, frame)\nif target == 242392:\n    return encode_six_decimal_digits_fields(memory, frame)\nif target == 242454:\n    return append_decimal_digit_fields(memory, frame)\nif target == 243490:\n    from ..high_level_scene_flows.business_scene import sample_random_preserving_seed_fields\n    return sample_random_preserving_seed_fields(memory, frame)\nif target == 253126:\n    return step_result_scene_phase_fields(memory, frame)\nif target == 253130:\n    return step_confirmation_scene_phase_fields(memory, frame)\nif target == 253134:\n    return step_transfer_scene_phase_fields(memory, frame)\nif target == 253138:\n    return step_primary_detail_scene_phase_fields(memory, frame)\nif target == 253142:\n    return step_secondary_detail_scene_phase_fields(memory, frame)\nif target == 253146:\n    return step_summary_scene_phase_fields(memory, frame)\nif target == 253150:\n    return step_pair_transition_scene_phase_fields(memory, frame)\nif target == 253154:\n    return step_initial_scene_phase_fields(memory, frame)\nif target == 253158:\n    return step_exchange_scene_phase_fields(memory, frame)\nif target == 253176:\n    return initialize_early_scene_fields(memory, frame)\nif target == 253180:\n    return process_early_scene_choice_fields(memory, frame)\nif target == 253184:\n    return present_early_scene_prompt_fields(memory, frame)\nif target == 253188:\n    return finish_early_scene_prompt_fields(memory, frame)\nif target == 253192:\n    return wait_early_scene_choice_fields(memory, frame)\nif target == 253196:\n    return finish_early_scene_fade_fields(memory, frame)\nif target == 253200:\n    return finish_alternate_scene_fade_fields(memory, frame)\nif target == 254548:\n    return draw_early_scene_choice_fields(memory, frame)\nif target == 254842:\n    return append_early_scene_instruction_fields(memory, frame)\nif target == 255018:\n    return paint_scene_number_rows_fields(memory, frame)\nif target == 255034:\n    return paint_scene_number_row_fields(memory, frame)\nif target == 255084:\n    return wait_exchange_scene_transition_fields(memory, frame)\nif target == 255088:\n    return process_exchange_scene_choice_fields(memory, frame)\nif target == 255092:\n    return finish_exchange_scene_transition_fields(memory, frame)\nif target == 255522:\n    return process_pair_phase_counter_fields(memory, frame)\nif target == 255526:\n    return confirm_pair_allocation_fields(memory, frame)\nif target == 255530:\n    return update_pair_allocation_input_fields(memory, frame)\nif target == 255534:\n    return exit_pair_allocation_fields(memory, frame)\nif target == 255538:\n    return gather_early_scene_input_fields(memory, frame)\nif target == 255720:\n    return exchange_scene_pair_frame_fields(memory, frame)\nif target == 255918:\n    return exchange_scene_actor_records_fields(memory, frame)\nif target == 256160:\n    return refresh_primary_actor_summary_fields(memory, frame)\nif target == 256256:\n    return wait_pair_stage_motion_fields(memory, frame)\nif target == 256260:\n    return advance_pair_stage_motion_fields(memory, frame)\nif target == 256264:\n    return confirm_second_pair_allocation_fields(memory, frame)\nif target == 256268:\n    return present_pair_stage_summary_fields(memory, frame)\nif target == 256272:\n    from .business_late_phase import adjust_secondary_formation_scene_fields\n    return adjust_secondary_formation_scene_fields(memory, frame)\nif target == 256276:\n    from .business_late_phase import confirm_secondary_formation_scene_fields\n    return confirm_secondary_formation_scene_fields(memory, frame)\nif target == 256280:\n    from .business_late_phase import update_active_battle_controls_fields\n    return update_active_battle_controls_fields(memory, frame)\nif target == 256284:\n    from .business_late_phase import latch_scene_controller_inputs_fields\n    return latch_scene_controller_inputs_fields(memory, frame)\nif target == 256738:\n    from .business_late_phase import draw_two_prompt_backgrounds_fields\n    return draw_two_prompt_backgrounds_fields(memory, frame)\nif target == 257224:\n    from .business_late_phase import update_secondary_scene_totals_fields\n    return update_secondary_scene_totals_fields(memory, frame)\nif target == 257926:\n    from .business_late_phase import begin_transition_prompt_fields\n    return begin_transition_prompt_fields(memory, frame)\nif target == 257930:\n    from .business_late_phase import update_action_mode_prompt_fields\n    return update_action_mode_prompt_fields(memory, frame)\nif target == 258096:\n    from .business_late_phase import dismiss_action_mode_prompt_fields\n    return dismiss_action_mode_prompt_fields(memory, frame)\nif target == 258146:\n    from .business_late_phase import begin_duel_handoff_prompt_fields\n    return begin_duel_handoff_prompt_fields(memory, frame)\nif target == 258150:\n    from .business_late_phase import confirm_duel_handoff_prompt_fields\n    return confirm_duel_handoff_prompt_fields(memory, frame)\nif target == 258154:\n    from .business_late_phase import await_duel_handoff_palette_fields\n    return await_duel_handoff_palette_fields(memory, frame)\nif target == 258158:\n    from .business_late_phase import finish_duel_handoff_phase_fields\n    return finish_duel_handoff_phase_fields(memory, frame)\nif target == 258270:\n    from .business_late_phase import commit_duel_handoff_fields\n    return commit_duel_handoff_fields(memory, frame)\nif target == 258538:\n    from .business_late_phase import begin_result_confirmation_prompt_fields\n    return begin_result_confirmation_prompt_fields(memory, frame)\nif target == 258542:\n    from .business_late_phase import confirm_result_prompt_fields\n    return confirm_result_prompt_fields(memory, frame)\nif target == 258546:\n    from .business_late_phase import await_result_palette_fields\n    return await_result_palette_fields(memory, frame)\nif target == 258550:\n    from .business_late_phase import finish_result_phase_fields\n    return finish_result_phase_fields(memory, frame)\nif target == 258716:\n    from .business_late_phase import begin_secondary_confirmation_prompt_fields\n    return begin_secondary_confirmation_prompt_fields(memory, frame)\nif target == 258720:\n    from .business_late_phase import confirm_secondary_result_prompt_fields\n    return confirm_secondary_result_prompt_fields(memory, frame)\nif target == 258724:\n    from .business_late_phase import await_secondary_result_palette_fields\n    return await_secondary_result_palette_fields(memory, frame)\nif target == 258728:\n    from .business_late_phase import finish_secondary_result_phase_fields\n    return finish_secondary_result_phase_fields(memory, frame)\nif target == 258894:\n    from .business_late_phase import begin_primary_confirmation_prompt_fields\n    return begin_primary_confirmation_prompt_fields(memory, frame)\nif target == 258898:\n    from .business_late_phase import replace_primary_confirmation_prompt_fields\n    return replace_primary_confirmation_prompt_fields(memory, frame)\nif target == 258902:\n    from .business_late_phase import confirm_primary_result_prompt_fields\n    return confirm_primary_result_prompt_fields(memory, frame)\nif target == 258906:\n    from .business_late_phase import await_primary_result_palette_fields\n    return await_primary_result_palette_fields(memory, frame)\nif target == 258910:\n    from .business_late_phase import finish_primary_result_phase_fields\n    return finish_primary_result_phase_fields(memory, frame)\nif target == 259166:\n    from .business_late_phase import normalize_secondary_squad_size_fields\n    return normalize_secondary_squad_size_fields(memory, frame)\nif target == 259352:\n    from .business_late_phase import adjust_secondary_squad_count_fields\n    return adjust_secondary_squad_count_fields(memory, frame)\nif target == 259378:\n    from .business_late_phase import adjust_selected_squad_class_counts_fields\n    return adjust_selected_squad_class_counts_fields(memory, frame)\nif target == 259656:\n    from .business_late_phase import deploy_secondary_formation_fields\n    return deploy_secondary_formation_fields(memory, frame)\nif target == 259778:\n    from .business_late_phase import adjust_primary_formation_fields\n    return adjust_primary_formation_fields(memory, frame)\nif target == 259822:\n    from .business_late_phase import deploy_primary_formation_fields\n    return deploy_primary_formation_fields(memory, frame)\nif target == 259936:\n    from .business_late_phase import adjust_selected_action_mode_fields\n    return adjust_selected_action_mode_fields(memory, frame)\nif target == 260316:\n    from .business_late_phase import commit_scene_battle_totals_fields\n    return commit_scene_battle_totals_fields(memory, frame)\nif target == 260342:\n    from .business_late_phase import draw_secondary_squad_budget_fields\n    return draw_secondary_squad_budget_fields(memory, frame)\nif target == 260414:\n    from .business_late_phase import draw_squad_class_budgets_fields\n    return draw_squad_class_budgets_fields(memory, frame)\nif target == 260550:\n    from .business_late_phase import draw_both_force_status_panels_fields\n    return draw_both_force_status_panels_fields(memory, frame)\nif target == 260658:\n    from .business_late_phase import draw_normal_force_status_panel_fields\n    return draw_normal_force_status_panel_fields(memory, frame)\nif target == 261288:\n    from .business_late_phase import selected_action_mode_view_fields\n    return selected_action_mode_view_fields(memory, frame)\nif target == 261304:\n    from .business_late_phase import lookup_action_mode_icon_pair_fields\n    return lookup_action_mode_icon_pair_fields(memory, frame)\nif target == 261414:\n    from .business_late_phase import draw_special_force_status_panel_fields\n    return draw_special_force_status_panel_fields(memory, frame)\nif target == 261726:\n    from .business_late_phase import draw_battle_summary_numbers_fields\n    return draw_battle_summary_numbers_fields(memory, frame)\nif target == 261962:\n    from .business_late_phase import draw_blinking_decimal_panel_fields\n    return draw_blinking_decimal_panel_fields(memory, frame)\nif target == 261998:\n    from .business_late_phase import draw_decimal_panel_fields\n    return draw_decimal_panel_fields(memory, frame)\nif target == 262940:\n    from ..high_level_scene_flows.business_objects import clear_scene_object_label_plane_fields\n    return clear_scene_object_label_plane_fields(memory, frame)\nraise SceneRefreshBoundary(target, memory.sync_status(frame), continuation)'}})

# Only unreachable selected legacy tails; every surviving function still has its whole DECL.
DECLARATIONS.pop('_allocation_valid')
DECLARATIONS.pop('_complete_phase_substate')
DECLARATIONS.pop('_draw_choice_from_selection')
DECLARATIONS.pop('_draw_fixed_prompt')
DECLARATIONS.pop('_early_contested_roll')
DECLARATIONS.pop('_exit_pair_allocation')
DECLARATIONS.pop('_initialize_early_panel')
DECLARATIONS.pop('_late_inputs')
DECLARATIONS.pop('_leave_early_prompt')
DECLARATIONS.pop('_phase_vector')
DECLARATIONS.pop('_prepare_scene_actor_arrival')
DECLARATIONS.pop('_show_choice_result')
DECLARATIONS.pop('_upload_portrait_tiles')

APPROVED.setdefault('business_late_phase',set()).update(('adjust_primary_formation_fields', 'adjust_secondary_formation_scene_fields', 'adjust_secondary_squad_count_fields', 'adjust_selected_action_mode_fields', 'adjust_selected_squad_class_counts_fields', 'await_duel_handoff_palette_fields', 'await_primary_result_palette_fields', 'await_result_palette_fields', 'await_secondary_result_palette_fields', 'begin_duel_handoff_prompt_fields', 'begin_primary_confirmation_prompt_fields', 'begin_result_confirmation_prompt_fields', 'begin_secondary_confirmation_prompt_fields', 'begin_transition_prompt_fields', 'commit_duel_handoff_fields', 'commit_scene_battle_totals_fields', 'confirm_duel_handoff_prompt_fields', 'confirm_primary_result_prompt_fields', 'confirm_result_prompt_fields', 'confirm_secondary_formation_scene_fields', 'confirm_secondary_result_prompt_fields', 'deploy_primary_formation_fields', 'deploy_secondary_formation_fields', 'dismiss_action_mode_prompt_fields', 'draw_battle_summary_numbers_fields', 'draw_blinking_decimal_panel_fields', 'draw_both_force_status_panels_fields', 'draw_decimal_panel_fields', 'draw_normal_force_status_panel_fields', 'draw_secondary_squad_budget_fields', 'draw_special_force_status_panel_fields', 'draw_squad_class_budgets_fields', 'draw_two_prompt_backgrounds_fields', 'finish_duel_handoff_phase_fields', 'finish_primary_result_phase_fields', 'finish_result_phase_fields', 'finish_secondary_result_phase_fields', 'latch_scene_controller_inputs_fields', 'lookup_action_mode_icon_pair_fields', 'normalize_secondary_squad_size_fields', 'replace_primary_confirmation_prompt_fields', 'selected_action_mode_view_fields', 'update_action_mode_prompt_fields', 'update_active_battle_controls_fields', 'update_secondary_scene_totals_fields'))

APPROVED.setdefault((2, 'high_level_gameplay_flow.business_battle'),set()).update(('_presentation_call_fields',))

APPROVED.setdefault((2, 'high_level_gameplay_flow.business_services'),set()).update(('_scene_refresh_emit', 'enqueue_sound_command_fields'))

APPROVED.setdefault((2, 'high_level_gameplay_flow.contexts_battle'),set()).update(('BattlePresentationMemory',))

APPROVED.setdefault((2, 'high_level_main_flows.business_movement_support'),set()).update(('_movement_compare', '_movement_divu_word', '_movement_move', '_movement_move_long', '_movement_multiply_word', '_movement_test'))

APPROVED.setdefault((2, 'high_level_scene_flows.business_objects'),set()).update(('_object_clear_word_fields', 'clear_scene_object_label_plane_fields'))

APPROVED.setdefault((2, 'high_level_scene_flows.business_scene'), set()).update(('_scene_render_arithmetic', '_scene_render_push_longs', 'advance_scene_palette_fade_fields', 'append_unclipped_scene_sprites_fields', 'sample_random_preserving_seed_fields', 'set_vram_write_address_fields', 'read_vdp_plane_rle_rows_from_control_fields'))

DECLARATIONS.update({'_allocation_move_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, value: Long, width: Word=16', 'returns': 'FirstDeploymentFrame', 'flow': 'from ..high_level_main_flows.business_movement_support import _movement_move\nif width == 32:\n    return _movement_move_long(memory.state, frame, name, value)\nreturn _movement_move(memory.state, frame, name, value, width)'}})

DECLARATIONS.update({'_allocation_store_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, low: Word, value: Long, width: Word=2, clear: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': 'from ..high_level_gameplay_flow.business_services import _scene_refresh_emit\nfrom ..high_level_scene_flows.business_objects import _object_clear_word_fields\nif clear:\n    return _object_clear_word_fields(memory, frame, 4294901760 | low)\nreturn _scene_refresh_emit(memory, frame, 4294901760 | low, width, value)'}})

DECLARATIONS.update({'_allocation_test_ram_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, low: Word, width: Word=16', 'returns': 'FirstDeploymentFrame', 'flow': 'from ..high_level_main_flows.business_movement_support import _movement_test\nreturn _movement_test(memory.state, frame, _allocation_read_fields(memory, frame, 4294901760 | low, width // 8), width)'}})

DECLARATIONS.update({'_allocation_compare_ram_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, low: Word, value: Long, width: Word=16', 'returns': 'FirstDeploymentFrame', 'flow': 'from ..high_level_main_flows.business_movement_support import _movement_compare\nreturn _movement_compare(memory.state, frame, _allocation_read_fields(memory, frame, 4294901760 | low, width // 8), value, width)'}})

DECLARATIONS.update({'_allocation_fill_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, command: Long, value: Word, count: Word, reset_increment: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_gameplay_flow.business_services import _scene_refresh_emit\nif reset_increment:\n    frame = _scene_refresh_emit(memory, frame, 12582916, 2, 36610)\nframe = _scene_refresh_emit(memory, frame, 12582916, 4, command)\nframe = first_replace(frame, scratch=memory.cursor_at(12582912))\nframe = _allocation_move_fields(memory, frame, 'offset_y', value)\nframe = _allocation_move_fields(memory, frame, 'choice', count)\nwhile True:\n    frame = _scene_refresh_emit(memory, frame, frame.scratch.base, 2, low16(frame.offset_y))\n    frame, done = _allocation_dbword_fields(frame, 'choice')\n    if done:\n        return frame"}})

DECLARATIONS.update({'_allocation_script_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, source: Long', 'returns': 'FirstDeploymentFrame', 'flow': 'from ..high_level_gameplay_flow.business_services import _scene_refresh_emit\nframe = _scene_refresh_emit(memory, frame, 16740364, 2, 40960)\nframe = _scene_refresh_emit(memory, frame, 16740366, 4, source)\nframe = _scene_refresh_emit(memory, frame, 16740372, 2, 3)\nreturn _scene_refresh_emit(memory, frame, 16740374, 2, 1)'}})

DECLARATIONS.update({'begin_scene_palette_lighten_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_movement_support import _movement_compare\nframe = _scene_rule_frame_fields(memory, frame, 240184)\nframe = _allocation_ram_move_fields(memory, frame, 'target_y', 32964)\nif not frame.status & 8:\n    frame = _allocation_mask_fields(memory, frame, 'target_y', 65280)\n    frame = _movement_compare(memory.state, frame, low16(frame.target_y), 256, 16)\n    if frame.status & 4:\n        return _allocation_known_fields(memory, frame, 240056)\n    frame = _scene_render_push_longs(memory, frame, (frame.target_x,))\n    frame = _allocation_call_fields(memory, frame, 240286, 240212)\n    frame = _allocation_restore_fields(memory, frame, ('target_x',))\nframe = _allocation_mask_fields(memory, frame, 'target_x', 255)\nframe = _allocation_move_fields(memory, frame, 'target_x', low16(frame.target_x) | 256)\nframe = _allocation_store_fields(memory, frame, 32964, low16(frame.target_x))\nframe = _allocation_store_fields(memory, frame, 32966, 0)\nframe = _allocation_store_fields(memory, frame, 32968, 0)\nframe = _allocation_call_fields(memory, frame, 240248, 240244)\nreturn _allocation_known_fields(memory, frame, 239992)"}})

DECLARATIONS.update({'_allocation_palette_copy_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, restore: bool', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_gameplay_flow.business_services import _scene_refresh_emit\nframe = _scene_rule_frame_fields(memory, frame, 240286 if restore else 240248)\nframe = _allocation_move_fields(memory, frame, 'target_y', 31, 32)\nframe = first_replace(frame, roster=memory.cursor_at(4294966144 if restore else 4294966016), candidates=memory.cursor_at(4294966016 if restore else 4294966144))\nwhile True:\n    value = frame.roster.long()\n    frame = first_replace(frame, roster=frame.roster.advance(4))\n    frame = _scene_refresh_emit(memory, frame, frame.candidates.base, 4, value)\n    frame = first_replace(frame, candidates=frame.candidates.advance(4))\n    frame, done = _allocation_dbword_fields(frame, 'target_y')\n    if done:\n        break\nreturn _allocation_store_fields(memory, frame, 32964, 65535) if restore else frame"}})

DECLARATIONS.update({'append_decimal_digit_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_gameplay_flow.business_services import _scene_refresh_emit\nframe = _scene_rule_frame_fields(memory, frame, 242454)\nframe = _movement_divu_word(memory.state, frame, 'target_x', low16(frame.unit), 242454)\nframe = _scene_refresh_emit(memory, frame, frame.roster.base, 1, low8(frame.target_x))\nframe = first_replace(frame, roster=frame.roster.advance(1))\nframe = _allocation_move_fields(memory, frame, 'target_x', 0)\nreturn _allocation_move_fields(memory, frame, 'target_x', swap_words(frame.target_x), 32)"}})

DECLARATIONS.update({'encode_six_decimal_digits_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_gameplay_flow.business_services import _scene_refresh_emit\nframe = _scene_rule_frame_fields(memory, frame, 242392)\nframe = _allocation_move_fields(memory, frame, 'unit', 0)\nframe = first_replace(frame, roster=memory.cursor_at(4294934528))\nwhile True:\n    frame = _allocation_arithmetic_fields(memory, frame, 'target_x', 100000, 32, True)\n    if frame.status & 1:\n        break\n    frame = _allocation_arithmetic_fields(memory, frame, 'unit', 1)\nframe = _allocation_arithmetic_fields(memory, frame, 'target_x', 100000, 32)\nframe = _scene_refresh_emit(memory, frame, frame.roster.base, 1, low8(frame.unit))\nframe = first_replace(frame, roster=frame.roster.advance(1))\nfor divisor, token in ((10000, 242426), (1000, 242434), (100, 242442), (10, 242450)):\n    frame = _allocation_move_fields(memory, frame, 'unit', divisor)\n    frame = _allocation_call_fields(memory, frame, 242454, token)\nframe = _scene_refresh_emit(memory, frame, frame.roster.base, 1, low8(frame.target_x))\nreturn first_replace(frame, roster=frame.roster.advance(1))"}})

DECLARATIONS.update({'paint_scene_number_row_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_gameplay_flow.business_services import _scene_refresh_emit\nframe = _scene_rule_frame_fields(memory, frame, 255034)\nframe = _scene_render_push_longs(memory, frame, (frame.target_y, frame.target_x))\nframe = _scene_refresh_emit(memory, frame, 12582916, 2, 36610)\nframe = _allocation_call_fields(memory, frame, 242352, 255050)\nframe = _allocation_restore_fields(memory, frame, ('target_x', 'target_y'))\nframe = _allocation_move_fields(memory, frame, 'unit', 5, 32)\nwhile True:\n    frame = _scene_refresh_emit(memory, frame, 12582912, 2, 58461)\n    frame, done = _allocation_dbword_fields(frame, 'unit')\n    if done:\n        return frame"}})

DECLARATIONS.update({'initialize_early_scene_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_movement_support import _movement_compare\nframe = _scene_rule_frame_fields(memory, frame, 253176)\nframe = _allocation_test_ram_fields(memory, frame, 32986, 8)\nif not frame.status & 4:\n    frame = _allocation_compare_ram_fields(memory, frame, 32986, 3, 8)\n    if not frame.status & 4:\n        frame = _allocation_compare_ram_fields(memory, frame, 32986, 1, 8)\n        return _allocation_initialize_panel_fields(memory, frame, 'other_mode')\nframe = first_replace(frame, roster=memory.cursor_at(4294952704))\nframe = _allocation_move_fields(memory, frame, 'target_y', 0, 32)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32992)\nframe = _allocation_move_fields(memory, frame, 'target_y', frame.roster.byte(low16(frame.target_x)), 8)\nframe = _allocation_mask_fields(memory, frame, 'target_y', 3)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32994)\nframe = _allocation_move_fields(memory, frame, 'target_x', frame.roster.byte(low16(frame.target_x)), 8)\nframe = _allocation_mask_fields(memory, frame, 'target_x', 3)\nframe = _allocation_arithmetic_fields(memory, frame, 'target_y', low8(frame.target_x), 8, True)\nframe = _allocation_arithmetic_fields(memory, frame, 'target_y', 1)\nframe = _movement_compare(memory.state, frame, low16(frame.target_y), 2, 16)\nif not frame.status & 5:\n    return _allocation_initialize_panel_fields(memory, frame, 'ordinary')\nfor own, extra, other in ((33038, 10, 33036), (33030, 20, 33028)):\n    frame = _allocation_ram_move_fields(memory, frame, 'target_x', own)\n    frame = _allocation_arithmetic_fields(memory, frame, 'target_x', extra)\n    frame = _movement_compare(memory.state, frame, low16(frame.target_x), _allocation_read_fields(memory, frame, 4294901760 | other, 2), 16)\n    if frame.status & 1:\n        return _allocation_initialize_panel_fields(memory, frame, 'ordinary')\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32998)\nframe = _movement_compare(memory.state, frame, low16(frame.target_x), _allocation_read_fields(memory, frame, 4294934756, 2), 16)\nif not frame.status & 1:\n    return _allocation_initialize_panel_fields(memory, frame, 'ordinary')\nframe = _allocation_call_fields(memory, frame, 243490, 253324)\nframe = _allocation_mask_fields(memory, frame, 'target_x', 3)\nreturn _allocation_initialize_panel_fields(memory, frame, 'favorable' if frame.status & 4 else 'ordinary')"}})

DECLARATIONS.update({'_allocation_contested_roll_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'tuple[FirstDeploymentFrame, bool]', 'flow': "from ..high_level_main_flows.business_movement_support import _movement_compare\nframe = _allocation_move_fields(memory, frame, 'target_y', 0, 32)\nframe = _allocation_move_fields(memory, frame, 'unit', 0, 32)\nframe = first_replace(frame, roster=memory.cursor_at(4294952704))\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32992)\nframe = _allocation_move_fields(memory, frame, 'target_x', frame.roster.byte(low16(frame.target_x)), 8)\nframe = _allocation_mask_fields(memory, frame, 'target_x', 3)\nframe = _allocation_move_fields(memory, frame, 'target_y', 5, 32)\nframe = _allocation_arithmetic_fields(memory, frame, 'target_y', low8(frame.target_x), 8, True)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32994)\nframe = _allocation_move_fields(memory, frame, 'target_x', frame.roster.byte(low16(frame.target_x)), 8)\nframe = _allocation_move_fields(memory, frame, 'unit', 5, 32)\nframe = _allocation_arithmetic_fields(memory, frame, 'unit', low8(frame.target_x), 8, True)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 33028)\nframe = _movement_multiply_word(memory.state, frame, 'target_y', low16(frame.target_x))\nframe = _movement_multiply_word(memory.state, frame, 'target_y', 100)\nframe = _allocation_call_fields(memory, frame, 243490, 253836)\nframe = _allocation_mask_fields(memory, frame, 'target_x', 31)\nframe = _allocation_arithmetic_fields(memory, frame, 'target_x', 20)\nframe = _allocation_arithmetic_fields(memory, frame, 'target_x', _allocation_read_fields(memory, frame, 4294934790, 2))\nframe = _movement_multiply_word(memory.state, frame, 'unit', low16(frame.target_x))\nframe = _movement_divu_word(memory.state, frame, 'target_y', low16(frame.unit), 253850)\nframe = _movement_compare(memory.state, frame, low16(frame.target_y), 100, 16)\nif not frame.status & 5:\n    return (frame, True)\nwhile True:\n    frame = _allocation_call_fields(memory, frame, 243490, 253864)\n    frame = _allocation_mask_fields(memory, frame, 'target_x', 127)\n    frame = _movement_compare(memory.state, frame, low16(frame.target_x), 100, 16)\n    if frame.status & 5:\n        break\nframe = _movement_compare(memory.state, frame, low16(frame.target_x), low16(frame.target_y), 16)\nif not frame.status & 5:\n    return (frame, False)\nframe = _allocation_call_fields(memory, frame, 243490, 253884)\nframe = _allocation_ram_move_fields(memory, frame, 'target_y', 61394)\nframe = first_replace(frame, roster=memory.cursor_at(254082))\nframe = _allocation_mask_fields(memory, frame, 'target_x', frame.roster.byte(low16(frame.target_y)), 8)\nreturn (frame, bool(frame.status & 4))"}})

DECLARATIONS.update({'_allocation_show_choice_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, accepted: bool', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_movement_support import _movement_compare\nfrom ..high_level_gameplay_flow.business_services import _scene_refresh_emit\nframe = _allocation_store_fields(memory, frame, 33090, 0 if accepted else 1, clear=accepted)\nframe = _allocation_fill_fields(memory, frame, 1073741827, 1024, 1215)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32992)\nframe = _allocation_move_fields(memory, frame, 'target_y', 1152)\nframe = _allocation_call_fields(memory, frame, 418260, 253950 if accepted else 254136)\nif accepted:\n    frame = _allocation_move_fields(memory, frame, 'target_x', 49954)\n    frame = _allocation_call_fields(memory, frame, 255018, 253958)\nframe = _allocation_fill_fields(memory, frame, 1610612738, 13107, 3455, True)\nframe = _scene_refresh_emit(memory, frame, 16740364, 2, 40960)\nframe = _scene_refresh_emit(memory, frame, 16740372, 2, 3)\nframe = _scene_refresh_emit(memory, frame, 16740374, 2, 1)\nframe = _allocation_adjust_ram_fields(memory, frame, 33084)\nframe = _scene_refresh_emit(memory, frame, 16740366, 4, 242680 if accepted else 242620)\nframe = first_replace(frame, roster=memory.cursor_at(4294952704))\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32994)\nframe = _allocation_move_fields(memory, frame, 'target_y', frame.roster.byte(low16(frame.target_x)), 8)\nframe = _allocation_mask_fields(memory, frame, 'target_y', 3)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 32992)\nframe = _allocation_move_fields(memory, frame, 'target_x', frame.roster.byte(low16(frame.target_x)), 8)\nframe = _allocation_mask_fields(memory, frame, 'target_x' if accepted else 'target_y', 3)\nframe = _movement_compare(memory.state, frame, low8(frame.target_y), low8(frame.target_x), 8)\nif not frame.status & 1:\n    frame = _scene_refresh_emit(memory, frame, 16740366, 4, 242602 if accepted else 242654)\nreturn _allocation_status_fields(memory, frame, 9472)"}})

DECLARATIONS.update({'process_exchange_scene_choice_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_gameplay_flow.business_services import _scene_refresh_emit\nframe = _scene_rule_frame_fields(memory, frame, 255088)\nframe, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934813, 5)\nif not pressed:\n    frame = _allocation_ram_move_fields(memory, frame, 'target_x', 33053, 8)\n    frame = _allocation_mask_fields(memory, frame, 'target_x', 3)\n    if not frame.status & 4:\n        frame = _allocation_xor_choice_fields(memory, frame)\n    return _allocation_choice_marker_fields(memory, frame)\nframe = _allocation_move_fields(memory, frame, 'target_x', 172)\nframe = _allocation_call_fields(memory, frame, 32906, 255262)\nframe = _allocation_test_ram_fields(memory, frame, 33090)\nif frame.status & 4:\n    frame = _allocation_store_fields(memory, frame, 33090, 0, clear=True)\n    frame = _allocation_store_fields(memory, frame, 33082, 7)\n    frame = _allocation_store_fields(memory, frame, 33084, 0, clear=True)\n    frame = _allocation_store_fields(memory, frame, 33100, 0, clear=True)\n    frame = _allocation_call_fields(memory, frame, 262940, 255292)\n    return _allocation_store_fields(memory, frame, 33802, 0, clear=True)\nframe = _allocation_status_fields(memory, frame, 9984)\nframe = _allocation_compare_ram_fields(memory, frame, 32986, 0, 8)\nif not frame.status & 4:\n    frame = _allocation_compare_ram_fields(memory, frame, 32986, 3, 8)\n    if not frame.status & 4:\n        frame = _allocation_call_fields(memory, frame, 268312, 255344)\nframe = _allocation_call_fields(memory, frame, 255720, 255348)\nframe = _allocation_call_fields(memory, frame, 255918, 255352)\nframe = _allocation_call_fields(memory, frame, 268312, 255356)\nframe = first_replace(frame, roster=memory.cursor_at(4294934890))\nframe = _allocation_move_fields(memory, frame, 'target_y', 15)\nwhile True:\n    frame = _allocation_move_fields(memory, frame, 'target_x', 352)\n    frame = _allocation_arithmetic_fields(memory, frame, 'target_x', frame.roster.word(2), subtract=True)\n    frame = _scene_refresh_emit(memory, frame, frame.roster.base + 2, 2, low16(frame.target_x))\n    frame = _scene_refresh_emit(memory, frame, frame.roster.base + 6, 2, 1)\n    frame = _scene_refresh_emit(memory, frame, frame.roster.base + 8, 2, 1)\n    frame = first_replace(frame, roster=frame.roster.advance(16))\n    frame, done = _allocation_dbword_fields(frame, 'target_y')\n    if done:\n        break\nframe = _allocation_call_fields(memory, frame, 255720, 255400)\nframe = _allocation_call_fields(memory, frame, 255918, 255404)\nframe = _allocation_call_fields(memory, frame, 262940, 255408)\nframe = _allocation_store_fields(memory, frame, 33802, 1)\nframe = _allocation_store_fields(memory, frame, 33090, 0, clear=True)\nfor low, value in ((32800, 0), (32804, 0), (32832, 33280), (32826, 33280)):\n    frame = _allocation_store_fields(memory, frame, low, value)\nframe = _allocation_adjust_ram_fields(memory, frame, 33084)\nreturn _allocation_status_fields(memory, frame, 9472)"}})

DECLARATIONS.update({'_allocation_roster_shares_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, secondary: bool', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_movement_support import _movement_test\nfrom ..high_level_gameplay_flow.business_services import _scene_refresh_emit\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 33030)\nframe = _allocation_ram_move_fields(memory, frame, 'target_y', 33026)\nframe = _movement_multiply_word(memory.state, frame, 'target_y', low16(frame.target_x))\nframe = _movement_divu_word(memory.state, frame, 'target_y', 100, 257060 if secondary else 256010)\nframe = _allocation_move_fields(memory, frame, 'target_x', 14)\nframe = _allocation_ram_move_fields(memory, frame, 'unit', 33010)\nframe = first_replace(frame, auxiliary=memory.cursor_at(4294935162 if secondary else 4294934906))\nwhile True:\n    frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base + 12, 2, low16(frame.target_y))\n    frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base + 14, 2, _allocation_read_fields(memory, frame, 4294934766, 2))\n    frame = _movement_test(memory.state, frame, low16(frame.unit), 16)\n    if not frame.status & 4:\n        frame = _allocation_arithmetic_fields(memory, frame, 'unit', 1, subtract=True)\n        frame = _object_adjust_word_fields(memory, frame, frame.auxiliary.base + 14, 1)\n    frame = first_replace(frame, auxiliary=frame.auxiliary.advance(16))\n    frame, done = _allocation_dbword_fields(frame, 'target_x')\n    if done:\n        return frame"}})

DECLARATIONS.update({'_allocation_check_commit_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, secondary: bool', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_movement_support import _movement_compare\nframe, pressed = _scene_rule_input_bit_fields(memory, frame, 4294934815, 5)\nif not pressed:\n    return _allocation_finish_class_fields(memory, frame)\nframe = _allocation_move_fields(memory, frame, 'target_x', 172)\nframe = _allocation_call_fields(memory, frame, 32906, 257016 if secondary else 255962)\nframe = _allocation_compare_ram_fields(memory, frame, 33092, 2)\nif not frame.status & 4:\n    return _allocation_finish_class_fields(memory, frame)\nframe = _allocation_ram_move_fields(memory, frame, 'target_x', 33018)\nframe = _allocation_arithmetic_fields(memory, frame, 'target_x', _allocation_read_fields(memory, frame, 4294934780, 2))\nframe = _allocation_arithmetic_fields(memory, frame, 'target_x', _allocation_read_fields(memory, frame, 4294934782, 2))\nframe = _movement_compare(memory.state, frame, low16(frame.target_x), _allocation_read_fields(memory, frame, 4294934762, 2), 16)\nif not frame.status & 4:\n    return _allocation_finish_class_fields(memory, frame)\nreturn _allocation_confirm_shares_fields(memory, frame, secondary)"}})

DECLARATIONS.update({'_allocation_prepare_secondary_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_gameplay_flow.business_services import _scene_refresh_emit\nframe = _allocation_status_fields(memory, frame, 9984)\nframe = _allocation_store_fields(memory, frame, 33090, 0, clear=True)\nframe = _allocation_adjust_ram_fields(memory, frame, 33084)\nframe = _allocation_call_fields(memory, frame, 259166, 256556)\nframe = _allocation_fill_fields(memory, frame, 1342177282, 13107, 191)\nframe = _scene_refresh_emit(memory, frame, 12582916, 4, 1342177282)\nframe = _allocation_ram_move_fields(memory, frame, 'choice', 32994)\nframe = _allocation_move_fields(memory, frame, 'target_x', 3)\nframe = _allocation_move_fields(memory, frame, 'target_y', 1)\nframe = _allocation_call_fields(memory, frame, 262850, 256614)\nframe = _allocation_decode_panel_fields(memory, frame, 281711, 49152, 18, 256646)\nframe = _allocation_call_fields(memory, frame, 260342, 256650)\nframe = _allocation_fill_fields(memory, frame, 1610612738, 13107, 3455, True)\nframe = _allocation_script_fields(memory, frame, 242464)\nframe = _allocation_store_fields(memory, frame, 33046, 1)\nframe = _allocation_call_fields(memory, frame, 256738, 256732)\nreturn _allocation_status_fields(memory, frame, 9472)"}})

DECLARATIONS.update({'_allocation_known_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long | None=None', 'returns': 'FirstDeploymentFrame', 'flow': 'if target == 32906:\n    from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields\n    return enqueue_sound_command_fields(memory, frame)\nif target == 239522:\n    from ..high_level_scene_flows.business_scene import append_unclipped_scene_sprites_fields\n    return append_unclipped_scene_sprites_fields(memory, frame)\nif target == 239992:\n    from ..high_level_scene_flows.business_scene import advance_scene_palette_fade_fields\n    return advance_scene_palette_fade_fields(memory, frame)\nif target == 240056:\n    return memory.sync_status(frame)\nif target == 240184:\n    return begin_scene_palette_lighten_fields(memory, frame)\nif target == 240248:\n    return snapshot_scene_palette_fields(memory, frame)\nif target == 240286:\n    return restore_scene_palette_fields(memory, frame)\nif target == 240342:\n    from ..high_level_scene_flows.business_scene import read_vdp_plane_rle_rows_from_control_fields\n    return read_vdp_plane_rle_rows_from_control_fields(memory, frame)\nif target == 242352:\n    from ..high_level_scene_flows.business_scene import set_vram_write_address_fields\n    return set_vram_write_address_fields(memory, frame)\nif target == 242392:\n    return encode_six_decimal_digits_fields(memory, frame)\nif target == 242454:\n    return append_decimal_digit_fields(memory, frame)\nif target == 243490:\n    from ..high_level_scene_flows.business_scene import sample_random_preserving_seed_fields\n    return sample_random_preserving_seed_fields(memory, frame)\nif target == 253126:\n    return step_result_scene_phase_fields(memory, frame)\nif target == 253130:\n    return step_confirmation_scene_phase_fields(memory, frame)\nif target == 253134:\n    return step_transfer_scene_phase_fields(memory, frame)\nif target == 253138:\n    return step_primary_detail_scene_phase_fields(memory, frame)\nif target == 253142:\n    return step_secondary_detail_scene_phase_fields(memory, frame)\nif target == 253146:\n    return step_summary_scene_phase_fields(memory, frame)\nif target == 253150:\n    return step_pair_transition_scene_phase_fields(memory, frame)\nif target == 253154:\n    return step_initial_scene_phase_fields(memory, frame)\nif target == 253158:\n    return step_exchange_scene_phase_fields(memory, frame)\nif target == 253176:\n    return initialize_early_scene_fields(memory, frame)\nif target == 253180:\n    return process_early_scene_choice_fields(memory, frame)\nif target == 253184:\n    return present_early_scene_prompt_fields(memory, frame)\nif target == 253188:\n    return finish_early_scene_prompt_fields(memory, frame)\nif target == 253192:\n    return wait_early_scene_choice_fields(memory, frame)\nif target == 253196:\n    return finish_early_scene_fade_fields(memory, frame)\nif target == 253200:\n    return finish_alternate_scene_fade_fields(memory, frame)\nif target == 254548:\n    return draw_early_scene_choice_fields(memory, frame)\nif target == 254842:\n    return append_early_scene_instruction_fields(memory, frame)\nif target == 255018:\n    return paint_scene_number_rows_fields(memory, frame)\nif target == 255034:\n    return paint_scene_number_row_fields(memory, frame)\nif target == 255084:\n    return wait_exchange_scene_transition_fields(memory, frame)\nif target == 255088:\n    return process_exchange_scene_choice_fields(memory, frame)\nif target == 255092:\n    return finish_exchange_scene_transition_fields(memory, frame)\nif target == 255522:\n    return process_pair_phase_counter_fields(memory, frame)\nif target == 255526:\n    return confirm_pair_allocation_fields(memory, frame)\nif target == 255530:\n    return update_pair_allocation_input_fields(memory, frame)\nif target == 255534:\n    return exit_pair_allocation_fields(memory, frame)\nif target == 255538:\n    return gather_early_scene_input_fields(memory, frame)\nif target == 255720:\n    return exchange_scene_pair_frame_fields(memory, frame)\nif target == 255918:\n    return exchange_scene_actor_records_fields(memory, frame)\nif target == 256160:\n    return refresh_primary_actor_summary_fields(memory, frame)\nif target == 256256:\n    return wait_pair_stage_motion_fields(memory, frame)\nif target == 256260:\n    return advance_pair_stage_motion_fields(memory, frame)\nif target == 256264:\n    return confirm_second_pair_allocation_fields(memory, frame)\nif target == 256268:\n    return present_pair_stage_summary_fields(memory, frame)\nif target == 256272:\n    from .business_late_phase import adjust_secondary_formation_scene_fields\n    return adjust_secondary_formation_scene_fields(memory, frame)\nif target == 256276:\n    from .business_late_phase import confirm_secondary_formation_scene_fields\n    return confirm_secondary_formation_scene_fields(memory, frame)\nif target == 256280:\n    from .business_late_phase import update_active_battle_controls_fields\n    return update_active_battle_controls_fields(memory, frame)\nif target == 256284:\n    from .business_late_phase import latch_scene_controller_inputs_fields\n    return latch_scene_controller_inputs_fields(memory, frame)\nif target == 256738:\n    from .business_late_phase import draw_two_prompt_backgrounds_fields\n    return draw_two_prompt_backgrounds_fields(memory, frame)\nif target == 257224:\n    from .business_late_phase import update_secondary_scene_totals_fields\n    return update_secondary_scene_totals_fields(memory, frame)\nif target == 257926:\n    from .business_late_phase import begin_transition_prompt_fields\n    return begin_transition_prompt_fields(memory, frame)\nif target == 257930:\n    from .business_late_phase import update_action_mode_prompt_fields\n    return update_action_mode_prompt_fields(memory, frame)\nif target == 258096:\n    from .business_late_phase import dismiss_action_mode_prompt_fields\n    return dismiss_action_mode_prompt_fields(memory, frame)\nif target == 258146:\n    from .business_late_phase import begin_duel_handoff_prompt_fields\n    return begin_duel_handoff_prompt_fields(memory, frame)\nif target == 258150:\n    from .business_late_phase import confirm_duel_handoff_prompt_fields\n    return confirm_duel_handoff_prompt_fields(memory, frame)\nif target == 258154:\n    from .business_late_phase import await_duel_handoff_palette_fields\n    return await_duel_handoff_palette_fields(memory, frame)\nif target == 258158:\n    from .business_late_phase import finish_duel_handoff_phase_fields\n    return finish_duel_handoff_phase_fields(memory, frame)\nif target == 258270:\n    from .business_late_phase import commit_duel_handoff_fields\n    return commit_duel_handoff_fields(memory, frame)\nif target == 258538:\n    from .business_late_phase import begin_result_confirmation_prompt_fields\n    return begin_result_confirmation_prompt_fields(memory, frame)\nif target == 258542:\n    from .business_late_phase import confirm_result_prompt_fields\n    return confirm_result_prompt_fields(memory, frame)\nif target == 258546:\n    from .business_late_phase import await_result_palette_fields\n    return await_result_palette_fields(memory, frame)\nif target == 258550:\n    from .business_late_phase import finish_result_phase_fields\n    return finish_result_phase_fields(memory, frame)\nif target == 258716:\n    from .business_late_phase import begin_secondary_confirmation_prompt_fields\n    return begin_secondary_confirmation_prompt_fields(memory, frame)\nif target == 258720:\n    from .business_late_phase import confirm_secondary_result_prompt_fields\n    return confirm_secondary_result_prompt_fields(memory, frame)\nif target == 258724:\n    from .business_late_phase import await_secondary_result_palette_fields\n    return await_secondary_result_palette_fields(memory, frame)\nif target == 258728:\n    from .business_late_phase import finish_secondary_result_phase_fields\n    return finish_secondary_result_phase_fields(memory, frame)\nif target == 258894:\n    from .business_late_phase import begin_primary_confirmation_prompt_fields\n    return begin_primary_confirmation_prompt_fields(memory, frame)\nif target == 258898:\n    from .business_late_phase import replace_primary_confirmation_prompt_fields\n    return replace_primary_confirmation_prompt_fields(memory, frame)\nif target == 258902:\n    from .business_late_phase import confirm_primary_result_prompt_fields\n    return confirm_primary_result_prompt_fields(memory, frame)\nif target == 258906:\n    from .business_late_phase import await_primary_result_palette_fields\n    return await_primary_result_palette_fields(memory, frame)\nif target == 258910:\n    from .business_late_phase import finish_primary_result_phase_fields\n    return finish_primary_result_phase_fields(memory, frame)\nif target == 259166:\n    from .business_late_phase import normalize_secondary_squad_size_fields\n    return normalize_secondary_squad_size_fields(memory, frame)\nif target == 259352:\n    from .business_late_phase import adjust_secondary_squad_count_fields\n    return adjust_secondary_squad_count_fields(memory, frame)\nif target == 259378:\n    from .business_late_phase import adjust_selected_squad_class_counts_fields\n    return adjust_selected_squad_class_counts_fields(memory, frame)\nif target == 259656:\n    from .business_late_phase import deploy_secondary_formation_fields\n    return deploy_secondary_formation_fields(memory, frame)\nif target == 259778:\n    from .business_late_phase import adjust_primary_formation_fields\n    return adjust_primary_formation_fields(memory, frame)\nif target == 259822:\n    from .business_late_phase import deploy_primary_formation_fields\n    return deploy_primary_formation_fields(memory, frame)\nif target == 259936:\n    from .business_late_phase import adjust_selected_action_mode_fields\n    return adjust_selected_action_mode_fields(memory, frame)\nif target == 260316:\n    from .business_late_phase import commit_scene_battle_totals_fields\n    return commit_scene_battle_totals_fields(memory, frame)\nif target == 260342:\n    from .business_late_phase import draw_secondary_squad_budget_fields\n    return draw_secondary_squad_budget_fields(memory, frame)\nif target == 260414:\n    from .business_late_phase import draw_squad_class_budgets_fields\n    return draw_squad_class_budgets_fields(memory, frame)\nif target == 260550:\n    from .business_late_phase import draw_both_force_status_panels_fields\n    return draw_both_force_status_panels_fields(memory, frame)\nif target == 260658:\n    from .business_late_phase import draw_normal_force_status_panel_fields\n    return draw_normal_force_status_panel_fields(memory, frame)\nif target == 261288:\n    from .business_late_phase import selected_action_mode_view_fields\n    return selected_action_mode_view_fields(memory, frame)\nif target == 261304:\n    from .business_late_phase import lookup_action_mode_icon_pair_fields\n    return lookup_action_mode_icon_pair_fields(memory, frame)\nif target == 261414:\n    from .business_late_phase import draw_special_force_status_panel_fields\n    return draw_special_force_status_panel_fields(memory, frame)\nif target == 261726:\n    from .business_late_phase import draw_battle_summary_numbers_fields\n    return draw_battle_summary_numbers_fields(memory, frame)\nif target == 261962:\n    from .business_late_phase import draw_blinking_decimal_panel_fields\n    return draw_blinking_decimal_panel_fields(memory, frame)\nif target == 261998:\n    from .business_late_phase import draw_decimal_panel_fields\n    return draw_decimal_panel_fields(memory, frame)\nif target == 262850:\n    from .business_actions import upload_object_officer_name_frame_fields\n    return upload_object_officer_name_frame_fields(memory.state, frame)\nif target == 262940:\n    from ..high_level_scene_flows.business_objects import clear_scene_object_label_plane_fields\n    return clear_scene_object_label_plane_fields(memory, frame)\nraise SceneRefreshBoundary(target, memory.sync_status(frame), continuation)'}})


# EARLY_OBJECTS_FULL_SOURCE_TWO_REAL_ROUTES121; two exact semantic import additions, all old permissions retained.
DECLARATIONS.update({'_allocation_known_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long | None=None', 'returns': 'FirstDeploymentFrame', 'flow': 'if target == 32906:\n    from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields\n    return enqueue_sound_command_fields(memory, frame)\nif target == 239522:\n    from ..high_level_scene_flows.business_scene import append_unclipped_scene_sprites_fields\n    return append_unclipped_scene_sprites_fields(memory, frame)\nif target == 239992:\n    from ..high_level_scene_flows.business_scene import advance_scene_palette_fade_fields\n    return advance_scene_palette_fade_fields(memory, frame)\nif target == 240056:\n    return memory.sync_status(frame)\nif target == 240184:\n    return begin_scene_palette_lighten_fields(memory, frame)\nif target == 240248:\n    return snapshot_scene_palette_fields(memory, frame)\nif target == 240286:\n    return restore_scene_palette_fields(memory, frame)\nif target == 240342:\n    from ..high_level_scene_flows.business_scene import read_vdp_plane_rle_rows_from_control_fields\n    return read_vdp_plane_rle_rows_from_control_fields(memory, frame)\nif target == 242352:\n    from ..high_level_scene_flows.business_scene import set_vram_write_address_fields\n    return set_vram_write_address_fields(memory, frame)\nif target == 242392:\n    return encode_six_decimal_digits_fields(memory, frame)\nif target == 242454:\n    return append_decimal_digit_fields(memory, frame)\nif target == 243490:\n    from ..high_level_scene_flows.business_scene import sample_random_preserving_seed_fields\n    return sample_random_preserving_seed_fields(memory, frame)\nif target == 253126:\n    return step_result_scene_phase_fields(memory, frame)\nif target == 253130:\n    return step_confirmation_scene_phase_fields(memory, frame)\nif target == 253134:\n    return step_transfer_scene_phase_fields(memory, frame)\nif target == 253138:\n    return step_primary_detail_scene_phase_fields(memory, frame)\nif target == 253142:\n    return step_secondary_detail_scene_phase_fields(memory, frame)\nif target == 253146:\n    return step_summary_scene_phase_fields(memory, frame)\nif target == 253150:\n    return step_pair_transition_scene_phase_fields(memory, frame)\nif target == 253154:\n    return step_initial_scene_phase_fields(memory, frame)\nif target == 253158:\n    return step_exchange_scene_phase_fields(memory, frame)\nif target == 253176:\n    return initialize_early_scene_fields(memory, frame)\nif target == 253180:\n    return process_early_scene_choice_fields(memory, frame)\nif target == 253184:\n    return present_early_scene_prompt_fields(memory, frame)\nif target == 253188:\n    return finish_early_scene_prompt_fields(memory, frame)\nif target == 253192:\n    return wait_early_scene_choice_fields(memory, frame)\nif target == 253196:\n    return finish_early_scene_fade_fields(memory, frame)\nif target == 253200:\n    return finish_alternate_scene_fade_fields(memory, frame)\nif target == 254548:\n    return draw_early_scene_choice_fields(memory, frame)\nif target == 254842:\n    return append_early_scene_instruction_fields(memory, frame)\nif target == 255018:\n    return paint_scene_number_rows_fields(memory, frame)\nif target == 255034:\n    return paint_scene_number_row_fields(memory, frame)\nif target == 255084:\n    return wait_exchange_scene_transition_fields(memory, frame)\nif target == 255088:\n    return process_exchange_scene_choice_fields(memory, frame)\nif target == 255092:\n    return finish_exchange_scene_transition_fields(memory, frame)\nif target == 255522:\n    return process_pair_phase_counter_fields(memory, frame)\nif target == 255526:\n    return confirm_pair_allocation_fields(memory, frame)\nif target == 255530:\n    return update_pair_allocation_input_fields(memory, frame)\nif target == 255534:\n    return exit_pair_allocation_fields(memory, frame)\nif target == 255538:\n    return gather_early_scene_input_fields(memory, frame)\nif target == 255720:\n    return exchange_scene_pair_frame_fields(memory, frame)\nif target == 255918:\n    return exchange_scene_actor_records_fields(memory, frame)\nif target == 256160:\n    return refresh_primary_actor_summary_fields(memory, frame)\nif target == 256256:\n    return wait_pair_stage_motion_fields(memory, frame)\nif target == 256260:\n    return advance_pair_stage_motion_fields(memory, frame)\nif target == 256264:\n    return confirm_second_pair_allocation_fields(memory, frame)\nif target == 256268:\n    return present_pair_stage_summary_fields(memory, frame)\nif target == 256272:\n    from .business_late_phase import adjust_secondary_formation_scene_fields\n    return adjust_secondary_formation_scene_fields(memory, frame)\nif target == 256276:\n    from .business_late_phase import confirm_secondary_formation_scene_fields\n    return confirm_secondary_formation_scene_fields(memory, frame)\nif target == 256280:\n    from .business_late_phase import update_active_battle_controls_fields\n    return update_active_battle_controls_fields(memory, frame)\nif target == 256284:\n    from .business_late_phase import latch_scene_controller_inputs_fields\n    return latch_scene_controller_inputs_fields(memory, frame)\nif target == 256738:\n    from .business_late_phase import draw_two_prompt_backgrounds_fields\n    return draw_two_prompt_backgrounds_fields(memory, frame)\nif target == 257224:\n    from .business_late_phase import update_secondary_scene_totals_fields\n    return update_secondary_scene_totals_fields(memory, frame)\nif target == 257926:\n    from .business_late_phase import begin_transition_prompt_fields\n    return begin_transition_prompt_fields(memory, frame)\nif target == 257930:\n    from .business_late_phase import update_action_mode_prompt_fields\n    return update_action_mode_prompt_fields(memory, frame)\nif target == 258096:\n    from .business_late_phase import dismiss_action_mode_prompt_fields\n    return dismiss_action_mode_prompt_fields(memory, frame)\nif target == 258146:\n    from .business_late_phase import begin_duel_handoff_prompt_fields\n    return begin_duel_handoff_prompt_fields(memory, frame)\nif target == 258150:\n    from .business_late_phase import confirm_duel_handoff_prompt_fields\n    return confirm_duel_handoff_prompt_fields(memory, frame)\nif target == 258154:\n    from .business_late_phase import await_duel_handoff_palette_fields\n    return await_duel_handoff_palette_fields(memory, frame)\nif target == 258158:\n    from .business_late_phase import finish_duel_handoff_phase_fields\n    return finish_duel_handoff_phase_fields(memory, frame)\nif target == 258270:\n    from .business_late_phase import commit_duel_handoff_fields\n    return commit_duel_handoff_fields(memory, frame)\nif target == 258538:\n    from .business_late_phase import begin_result_confirmation_prompt_fields\n    return begin_result_confirmation_prompt_fields(memory, frame)\nif target == 258542:\n    from .business_late_phase import confirm_result_prompt_fields\n    return confirm_result_prompt_fields(memory, frame)\nif target == 258546:\n    from .business_late_phase import await_result_palette_fields\n    return await_result_palette_fields(memory, frame)\nif target == 258550:\n    from .business_late_phase import finish_result_phase_fields\n    return finish_result_phase_fields(memory, frame)\nif target == 258716:\n    from .business_late_phase import begin_secondary_confirmation_prompt_fields\n    return begin_secondary_confirmation_prompt_fields(memory, frame)\nif target == 258720:\n    from .business_late_phase import confirm_secondary_result_prompt_fields\n    return confirm_secondary_result_prompt_fields(memory, frame)\nif target == 258724:\n    from .business_late_phase import await_secondary_result_palette_fields\n    return await_secondary_result_palette_fields(memory, frame)\nif target == 258728:\n    from .business_late_phase import finish_secondary_result_phase_fields\n    return finish_secondary_result_phase_fields(memory, frame)\nif target == 258894:\n    from .business_late_phase import begin_primary_confirmation_prompt_fields\n    return begin_primary_confirmation_prompt_fields(memory, frame)\nif target == 258898:\n    from .business_late_phase import replace_primary_confirmation_prompt_fields\n    return replace_primary_confirmation_prompt_fields(memory, frame)\nif target == 258902:\n    from .business_late_phase import confirm_primary_result_prompt_fields\n    return confirm_primary_result_prompt_fields(memory, frame)\nif target == 258906:\n    from .business_late_phase import await_primary_result_palette_fields\n    return await_primary_result_palette_fields(memory, frame)\nif target == 258910:\n    from .business_late_phase import finish_primary_result_phase_fields\n    return finish_primary_result_phase_fields(memory, frame)\nif target == 259166:\n    from .business_late_phase import normalize_secondary_squad_size_fields\n    return normalize_secondary_squad_size_fields(memory, frame)\nif target == 259352:\n    from .business_late_phase import adjust_secondary_squad_count_fields\n    return adjust_secondary_squad_count_fields(memory, frame)\nif target == 259378:\n    from .business_late_phase import adjust_selected_squad_class_counts_fields\n    return adjust_selected_squad_class_counts_fields(memory, frame)\nif target == 259656:\n    from .business_late_phase import deploy_secondary_formation_fields\n    return deploy_secondary_formation_fields(memory, frame)\nif target == 259778:\n    from .business_late_phase import adjust_primary_formation_fields\n    return adjust_primary_formation_fields(memory, frame)\nif target == 259822:\n    from .business_late_phase import deploy_primary_formation_fields\n    return deploy_primary_formation_fields(memory, frame)\nif target == 259936:\n    from .business_late_phase import adjust_selected_action_mode_fields\n    return adjust_selected_action_mode_fields(memory, frame)\nif target == 260316:\n    from .business_late_phase import commit_scene_battle_totals_fields\n    return commit_scene_battle_totals_fields(memory, frame)\nif target == 260342:\n    from .business_late_phase import draw_secondary_squad_budget_fields\n    return draw_secondary_squad_budget_fields(memory, frame)\nif target == 260414:\n    from .business_late_phase import draw_squad_class_budgets_fields\n    return draw_squad_class_budgets_fields(memory, frame)\nif target == 260550:\n    from .business_late_phase import draw_both_force_status_panels_fields\n    return draw_both_force_status_panels_fields(memory, frame)\nif target == 260658:\n    from .business_late_phase import draw_normal_force_status_panel_fields\n    return draw_normal_force_status_panel_fields(memory, frame)\nif target == 261288:\n    from .business_late_phase import selected_action_mode_view_fields\n    return selected_action_mode_view_fields(memory, frame)\nif target == 261304:\n    from .business_late_phase import lookup_action_mode_icon_pair_fields\n    return lookup_action_mode_icon_pair_fields(memory, frame)\nif target == 261414:\n    from .business_late_phase import draw_special_force_status_panel_fields\n    return draw_special_force_status_panel_fields(memory, frame)\nif target == 261726:\n    from .business_late_phase import draw_battle_summary_numbers_fields\n    return draw_battle_summary_numbers_fields(memory, frame)\nif target == 261962:\n    from .business_late_phase import draw_blinking_decimal_panel_fields\n    return draw_blinking_decimal_panel_fields(memory, frame)\nif target == 261998:\n    from .business_late_phase import draw_decimal_panel_fields\n    return draw_decimal_panel_fields(memory, frame)\nif target == 262850:\n    from .business_actions import upload_object_officer_name_frame_fields\n    return upload_object_officer_name_frame_fields(memory.state, frame)\nif target == 262940:\n    from ..high_level_scene_flows.business_objects import clear_scene_object_label_plane_fields\n    return clear_scene_object_label_plane_fields(memory, frame)\nif target == 268312:\n    from ..high_level_scene_flows.business_objects import initialize_scene_object_roster_after_mode_check_fields\n    return initialize_scene_object_roster_after_mode_check_fields(memory, frame)\nif target == 418260:\n    from .business_actions import upload_portrait_tiles_frame_fields\n    return upload_portrait_tiles_frame_fields(memory.state, frame)\nraise SceneRefreshBoundary(target, memory.sync_status(frame), continuation)'}})
APPROVED.setdefault((2,'high_level_scene_flows.business_objects'),set()).add('initialize_scene_object_roster_after_mode_check_fields')
APPROVED.setdefault('business_actions',set()).add('upload_portrait_tiles_frame_fields')
