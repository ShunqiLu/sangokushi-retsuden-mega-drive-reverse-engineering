"""Restricted semantic source admission with ordinary mnemonic lowering.

Reads explicit source text only. This is an intermediate structural compiler,
not a general Python compiler or full-console/indirect-handler implementation.
"""
from .compiler_common import CompileError,semantic_functions,lower_declared
from .menu_policy_duel import admit_menu_source
from .action_policy_duel import (ROLE_SPECS as _ACTION_ROLES,
                               owner_rules as _action_rules,
                               LOWERERS as _ACTION_LOWERERS)
from .ai_policy_duel import (ROLE_SPECS as _AI_ROLES,
                           owner_rules as _ai_rules,
                           LOWERERS as _AI_LOWERERS)
from .actor_policy_duel import (ROLE_SPECS as _ACTOR_ROLES,
                              owner_rules as _actor_rules,
                              LOWERERS as _ACTOR_LOWERERS)
from .flow_policy_duel import (ROLE_SPECS as _FLOW_ROLES,
                             owner_rules as _flow_rules,
                             LOWERERS as _FLOW_LOWERERS)
from .target import DUEL_BINDINGS
from .field_policy_duel import admit_selected_duel_fields

APPROVED={'business_reuse': {'choose_first_duel_control',
                    'choose_second_duel_control',
                    'clear_video_sprite_plane',
                    'enqueue_sound_command',
                    'expand_glyph_stream',
                    'stage_sprite_word_packet',
                    'step_random'},
 'business_scene': {'darken_palette', 'decode_glyph_rows_to_buffers', 'flush_scene_transfer_queue'},
 'contexts_duel': {'DuelAIContext',
                   'DuelAIResult',
                   'DuelActionContext',
                   'DuelActionResult',
                   'DuelActorContext',
                   'DuelActorResult',
                   'DuelContact',
                   'DuelControlContext',
                   'DuelGlyphContext',
                   'DuelLaneResult',
                   'DuelProbability',
                   'DuelSceneContext',
                   'DuelSceneResult',
                   'DuelSpriteResult'},
 'contexts_reuse': {'GlyphColors'},
 'domain': {'Boundary',
            'Cursor',
            'Long',
            'SceneState',
            'Table',
            'Word',
            'divu_retained',
            'high16',
            'low16',
            'low8',
            'negative_long',
            'negative_word',
            'replace_byte',
            'replace_word',
            's16',
            's8',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'}}

DECLARATIONS={'_live_table': {'signature': 'state, value',
                 'returns': None,
                 'flow': 'if not isinstance(value, Table) or value.state is not state:\n'
                         "    raise ValueError('live same-state Table required')\n"
                         'return value'},
 '_live_cursor': {'signature': 'state, value',
                  'returns': None,
                  'flow': 'if not isinstance(value, Cursor) or value.state is not state:\n'
                          "    raise ValueError('live same-state Cursor required')\n"
                          'return value'},
 '_duel_frame': {'signature': 'state',
                 'returns': None,
                 'flow': 'state.set_status_word(9472)\n'
                         "state.set_scalar('ram_f612_word', 1792)\n"
                         'while state.read(4294964754, 1) != 0:\n'
                         "    state.progress('duel_frame_low_byte_ack')"},
 '_sound': {'signature': 'state, command',
            'returns': None,
            'flow': 'from .business_reuse import enqueue_sound_command\n'
                    "return enqueue_sound_command(state, uint(command, 8, 'sound command'))"},
 '_random': {'signature': 'state',
             'returns': None,
             'flow': 'from .business_reuse import step_random\nreturn step_random(state)'},
 '_first_controls': {'signature': 'state, controls',
                     'returns': None,
                     'flow': 'from .business_reuse import choose_first_duel_control\n'
                             'result = choose_first_duel_control(state, controls.command, '
                             'controls.mode)\n'
                             'return DuelControlContext(result.command, result.mode_carrier)'},
 '_second_controls': {'signature': 'state, controls',
                      'returns': None,
                      'flow': 'from .business_reuse import choose_second_duel_control\n'
                              'result = choose_second_duel_control(state, controls.command, '
                              'controls.mode)\n'
                              'return DuelControlContext(result.command, result.mode_carrier)'},
 '_upload_longs': {'signature': 'state, source, count_latch',
                   'returns': None,
                   'flow': 'source = _live_cursor(state, source)\n'
                           "counter = uint(count_latch, 16, 'count latch')\n"
                           'while True:\n'
                           '    state.mmio_write(12582912, 4, source.next_long())\n'
                           '    counter = u16(counter - 1)\n'
                           '    if counter == 65535:\n'
                           '        return source'},
 '_upload_words': {'signature': 'state, source, count_latch',
                   'returns': None,
                   'flow': 'source = _live_cursor(state, source)\n'
                           "counter = uint(count_latch, 16, 'count latch')\n"
                           'while True:\n'
                           '    state.mmio_write(12582912, 2, source.next_word())\n'
                           '    counter = u16(counter - 1)\n'
                           '    if counter == 65535:\n'
                           '        return source'},
 'advance_duel_entry_palette': {'signature': 'state: SceneState',
                                'returns': 'None',
                                'flow': 'from .business_scene import darken_palette\n'
                                        "if state.scalar('ram_70f8_word') >= 16:\n"
                                        '    return\n'
                                        "intensity = u16(15 - state.scalar('ram_70f8_word'))\n"
                                        'darken_palette(state, intensity, 64, '
                                        'state.table(163968).cursor())\n'
                                        "state.set_scalar('ram_70f8_word', "
                                        "u16(state.scalar('ram_70f8_word') + 1))"},
 'show_active_duel_turn_label': {'signature': 'state: SceneState',
                                 'returns': 'Long',
                                 'flow': 'from .business_reuse import stage_sprite_word_packet\n'
                                         'source = state.table(164256).cursor()\n'
                                         'row_command = 60424\n'
                                         "if state.scalar('ram_7008_word') & 1:\n"
                                         '    source = state.table(164278).cursor()\n'
                                         '    row_command = 60484\n'
                                         'return stage_sprite_word_packet(state, source, 1610612740, 1, '
                                         'row_command)'},
 'wait_active_duel_action': {'signature': 'state: SceneState, controls: '
                                          'DuelControlContext=DuelControlContext()',
                             'returns': 'DuelControlContext',
                             'flow': 'controls.validate()\n'
                                     'while True:\n'
                                     '    _duel_frame(state)\n'
                                     "    state.set_scalar('ram_70fa_word', "
                                     "u16(state.scalar('ram_70fa_word') - 1))\n"
                                     '    refresh_duel_actors(state)\n'
                                     "    if state.scalar('ram_700c_word') != 0:\n"
                                     '        continue\n'
                                     '    controls = _first_controls(state, controls)\n'
                                     "    if negative_word(state.scalar('ram_7018_word')):\n"
                                     '        controls = _second_controls(state, controls)\n'
                                     '    controls = DuelControlContext(replace_word(controls.command, '
                                     'low16(controls.command) & 112), controls.mode)\n'
                                     '    if low16(controls.command) != 0:\n'
                                     '        state.set_status_word(9984)\n'
                                     '        return controls'},
 'wait_either_duel_action': {'signature': 'state: SceneState, controls: '
                                          'DuelControlContext=DuelControlContext()',
                             'returns': 'DuelControlContext',
                             'flow': 'controls.validate()\n'
                                     "if state.scalar('ram_700a_byte') == 3:\n"
                                     '    return wait_active_duel_action(state, controls)\n'
                                     "if state.scalar('ram_700b_byte') == 3:\n"
                                     '    return wait_active_duel_action(state, controls)\n'
                                     'while True:\n'
                                     '    _duel_frame(state)\n'
                                     "    state.set_scalar('ram_70fa_word', "
                                     "u16(state.scalar('ram_70fa_word') - 1))\n"
                                     '    refresh_duel_actors(state)\n'
                                     "    if state.scalar('ram_700c_word') != 0:\n"
                                     '        continue\n'
                                     '    first = _first_controls(state, controls)\n'
                                     '    second = _second_controls(state, first)\n'
                                     '    combined = u16(low16(second.command) | low16(first.command)) '
                                     '& 112\n'
                                     '    controls = DuelControlContext(replace_word(second.command, '
                                     'combined), second.mode)\n'
                                     '    if combined != 0:\n'
                                     '        state.set_status_word(9984)\n'
                                     '        return controls'},
 'configure_duel_weapon_motion': {'signature': 'state: SceneState, actor: Table',
                                  'returns': 'None',
                                  'flow': 'actor = _live_table(state, actor)\n'
                                          'attribute = actor.word(30)\n'
                                          'mode_offset = u16(actor.word(12) << 1)\n'
                                          'penalty = state.table(162430).word(mode_offset)\n'
                                          'difference = u16(attribute - penalty)\n'
                                          'if attribute < penalty:\n'
                                          '    difference = 0\n'
                                          'elif difference >= 80:\n'
                                          '    difference = 80\n'
                                          'delay = u16(80 - difference)\n'
                                          'actor.set_long(18, u32(difference * 1792 + 24576))\n'
                                          'actor.set_word(22, low16(divu_retained(delay, 2)))'},
 'refresh_duel_actors': {'signature': 'state: SceneState',
                         'returns': 'None',
                         'flow': 'first, second = (state.table(16740432), state.table(16740512))\n'
                                 'first.set_word(0, 0)\n'
                                 'render_duel_actor(state, first, second)\n'
                                 'second.set_word(0, 0)\n'
                                 'render_duel_actor(state, second, first)'},
 'upload_duel_officer_name': {'signature': 'state: SceneState, officer: Word, colors: DuelGlyphContext',
                              'returns': 'DuelGlyphContext',
                              'flow': "officer = uint(officer, 16, 'officer')\n"
                                      'colors.validate()\n'
                                      'source = state.table(566532).cursor(u16(officer * 6))\n'
                                      'remaining = replace_word(colors.remaining, 2)\n'
                                      'if source.word(4) == 63:\n'
                                      '    remaining = replace_word(remaining, 1)\n'
                                      '    shade = u8(u16(low16(colors.background) << 4) | '
                                      'low16(colors.background))\n'
                                      '    first, second = (state.table(4294955776).cursor(), '
                                      'state.table(4294956096).cursor())\n'
                                      '    for _ in range(64):\n'
                                      '        first.append_byte(shade)\n'
                                      '        second.append_byte(shade)\n'
                                      '    return _expand_and_upload_duel_glyphs(state, source, first, '
                                      'DuelGlyphContext(colors.background, colors.foreground, '
                                      'remaining))\n'
                                      'return upload_duel_glyph_strip(state, source, '
                                      'DuelGlyphContext(colors.background, colors.foreground, '
                                      'remaining))'},
 'upload_duel_glyph_strip': {'signature': 'state: SceneState, source: Cursor, colors: DuelGlyphContext',
                             'returns': 'DuelGlyphContext',
                             'flow': 'return _expand_and_upload_duel_glyphs(state, source, '
                                     'state.table(4294955776).cursor(), colors)'},
 '_expand_and_upload_duel_glyphs': {'signature': 'state, source, destination, colors',
                                    'returns': None,
                                    'flow': 'from .business_scene import decode_glyph_rows_to_buffers\n'
                                            'source = _live_cursor(state, source)\n'
                                            'colors.validate()\n'
                                            'result = decode_glyph_rows_to_buffers(state, source, '
                                            'destination, colors.background, colors.foreground, '
                                            'colors.remaining)\n'
                                            '_upload_longs(state, state.table(4294955776).cursor(), '
                                            '95)\n'
                                            'return DuelGlyphContext(result.background, '
                                            'result.foreground, result.remaining)'},
 'clear_duel_text_plane': {'signature': 'state: SceneState',
                           'returns': 'None',
                           'flow': "state.set_scalar('ram_d100_word', 0)\n"
                                   'state.mmio_write(12582916, 4, 1174405123)\n'
                                   'for _ in range(640):\n'
                                   '    state.mmio_write(12582912, 4, 286331153)'},
 'choose_duel_two_option_menu': {'signature': 'state: SceneState, choice: Table, controls: '
                                              'DuelControlContext',
                                 'returns': 'DuelControlContext',
                                 'flow': 'choice = _live_table(state, choice)\n'
                                         'controls.validate()\n'
                                         'selected = choice.word()\n'
                                         'direction = low16(controls.command) & 12\n'
                                         'if direction:\n'
                                         '    delta = 1 if direction & 8 else 65535\n'
                                         '    selected = u16(selected + delta)\n'
                                         '    if selected < 2:\n'
                                         '        choice.set_word(0, selected)\n'
                                         'controls = _first_controls(state, controls)\n'
                                         'if low16(controls.command) & 32:\n'
                                         '    return controls\n'
                                         'direction = low16(controls.command) & 12\n'
                                         "if direction or state.scalar('ram_7008_word') & 8:\n"
                                         '    append_duel_sprite(state, 200, u16(choice.word() * 56 + '
                                         '121), 67, 32768)\n'
                                         "state.set_scalar('ram_70fa_word', "
                                         "u16(state.scalar('ram_70fa_word') - 1))\n"
                                         'return controls'},
 '_equipment_available': {'signature': 'equipment, option',
                          'returns': None,
                          'flow': 'if option == 0:\n'
                                  '    return equipment.word(2) != 0\n'
                                  'if option == 1:\n'
                                  '    return equipment.word(0) != 0\n'
                                  'return equipment.word(4) != 0'},
 '_choose_duel_equipment': {'signature': 'state, choice, equipment, controls',
                            'returns': None,
                            'flow': 'choice = _live_table(state, choice)\n'
                                    'equipment = _live_table(state, equipment)\n'
                                    'controls.validate()\n'
                                    'while not _equipment_available(equipment, choice.word()):\n'
                                    '    choice.set_word(0, u16(choice.word() + 1))\n'
                                    '    if choice.word() >= 3:\n'
                                    '        choice.set_word(0, 0)\n'
                                    'selected = choice.word()\n'
                                    'direction = low16(controls.command) & 12\n'
                                    'if direction:\n'
                                    '    delta = 1 if direction & 8 else 65535\n'
                                    '    while True:\n'
                                    '        selected = u16(selected + delta)\n'
                                    '        if negative_word(selected):\n'
                                    '            selected = 2\n'
                                    '        elif selected >= 3:\n'
                                    '            selected = 0\n'
                                    '        if _equipment_available(equipment, selected):\n'
                                    '            break\n'
                                    '    if selected < 3:\n'
                                    '        choice.set_word(0, selected)\n'
                                    'controls = _first_controls(state, controls)\n'
                                    'if low16(controls.command) & 32:\n'
                                    '    return controls\n'
                                    "if low16(controls.command) & 12 or state.scalar('ram_7008_word') & "
                                    '8:\n'
                                    '    append_duel_sprite(state, 200, u16(choice.word() * 56 + 104), '
                                    '67, 32768)\n'
                                    "state.set_scalar('ram_70fa_word', "
                                    "u16(state.scalar('ram_70fa_word') - 1))\n"
                                    'return controls'},
 'choose_first_duel_equipment': {'signature': 'state: SceneState, choice: Table, controls: '
                                              'DuelControlContext',
                                 'returns': 'DuelControlContext',
                                 'flow': 'return _choose_duel_equipment(state, choice, '
                                         'state.table(16740474), controls)'},
 'choose_second_duel_equipment': {'signature': 'state: SceneState, choice: Table, controls: '
                                               'DuelControlContext',
                                  'returns': 'DuelControlContext',
                                  'flow': 'return _choose_duel_equipment(state, choice, '
                                          'state.table(16740554), controls)'},
 'choose_duel_action_menu': {'signature': 'state: SceneState, controls: DuelControlContext',
                             'returns': 'DuelControlContext',
                             'flow': 'controls.validate()\n'
                                     "second = negative_word(state.scalar('ram_7018_word'))\n"
                                     'actor = state.table(16740512 if second else 16740432)\n'
                                     'restricted = actor.word(26) == actor.word(32)\n'
                                     'if not restricted:\n'
                                     "    selected = state.scalar('ram_7018_word')\n"
                                     '    direction = low16(controls.command) & 15\n'
                                     '    if direction:\n'
                                     '        if direction & 8:\n'
                                     '            delta = 1\n'
                                     '        elif direction & 4:\n'
                                     '            delta = 65535\n'
                                     '        elif direction & 2:\n'
                                     '            delta = 2\n'
                                     '        else:\n'
                                     '            delta = 65534\n'
                                     '        selected = u16(selected & 65280 | u8(selected + delta))\n'
                                     '        if low8(selected) < 4:\n'
                                     "            state.set_scalar('ram_7018_word', selected)\n"
                                     '    controls = _first_controls(state, controls)\n'
                                     '    if low16(controls.command) & 32:\n'
                                     '        return controls\n'
                                     '    if low16(controls.command) & 15 or '
                                     "state.scalar('ram_7008_word') & 8:\n"
                                     "        x = u16((state.scalar('ram_7018_word') & 2) * 12 + 176)\n"
                                     "        y = u16((state.scalar('ram_7018_word') & 1) * 48 + 136)\n"
                                     '        append_duel_sprite(state, x, y, 67, 32768)\n'
                                     'else:\n'
                                     "    selected = state.scalar('ram_7019_byte')\n"
                                     '    if low16(controls.command) & 8:\n'
                                     '        selected = u16(selected + 1)\n'
                                     '        if selected == 2:\n'
                                     '            selected = u16(selected + 1)\n'
                                     '        if selected >= 4:\n'
                                     '            selected = 0\n'
                                     '    if low16(controls.command) & 4:\n'
                                     '        if selected == 3:\n'
                                     '            selected = u16(selected - 1)\n'
                                     '        selected = u16(selected - 1)\n'
                                     '        if negative_word(selected):\n'
                                     '            selected = 3\n'
                                     "    state.set_scalar('ram_7019_byte', low8(selected))\n"
                                     '    controls = _first_controls(state, controls)\n'
                                     '    if low16(controls.command) & 32:\n'
                                     '        return controls\n'
                                     '    if low16(controls.command) & 15 or '
                                     "state.scalar('ram_7008_word') & 8:\n"
                                     "        index = state.scalar('ram_7018_word') & 3\n"
                                     '        y = state.table(163854).byte(index)\n'
                                     '        append_duel_sprite(state, 200, y, 67, 32768)\n'
                                     "state.set_scalar('ram_70fa_word', "
                                     "u16(state.scalar('ram_70fa_word') - 1))\n"
                                     'return controls'},
 'decode_duel_byte_lanes': {'signature': 'state: SceneState, source: Cursor, destination: Cursor, '
                                         'length: Word, repeat_value: Long=0, pair_value: Long=0',
                            'returns': 'DuelLaneResult',
                            'flow': 'source = _live_cursor(state, source)\n'
                                    'destination = _live_cursor(state, destination)\n'
                                    "length = uint(length, 16, 'length')\n"
                                    'saved_address = destination.address()\n'
                                    'result = decode_duel_byte_lane(state, source, destination, length, '
                                    'repeat_value, pair_value)\n'
                                    'return decode_duel_byte_lane(state, result.source, '
                                    'state.table(saved_address + 1).cursor(), length, '
                                    'result.repeat_value, result.pair_value)'},
 'decode_duel_byte_lane': {'signature': 'state: SceneState, source: Cursor, destination: Cursor, '
                                        'length: Word, repeat_value: Long=0, pair_value: Long=0',
                           'returns': 'DuelLaneResult',
                           'flow': 'source = _live_cursor(state, source)\n'
                                   'destination = _live_cursor(state, destination)\n'
                                   "remaining = uint(length, 16, 'length')\n"
                                   "repeat_value = uint(repeat_value, 32, 'repeat value')\n"
                                   "pair_value = uint(pair_value, 32, 'pair value')\n"
                                   'while remaining != 0:\n'
                                   '    token = source.next_byte()\n'
                                   '    if token < 128:\n'
                                   '        count = token\n'
                                   '        for _ in range(count + 1):\n'
                                   '            destination.set_byte(0, source.next_byte())\n'
                                   '            destination = destination.advance(2)\n'
                                   '            remaining = u16(remaining - 1)\n'
                                   '    elif not token & 64:\n'
                                   '        count = token & 63\n'
                                   '        repeat_value = replace_byte(repeat_value, '
                                   'source.next_byte())\n'
                                   '        for _ in range(count + 1):\n'
                                   '            destination.set_byte(0, low8(repeat_value))\n'
                                   '            destination = destination.advance(2)\n'
                                   '            remaining = u16(remaining - 1)\n'
                                   '    elif not token & 32:\n'
                                   '        count = token & 31\n'
                                   '        repeat_value = replace_byte(repeat_value, '
                                   'source.next_byte())\n'
                                   '        pair_value = replace_byte(pair_value, source.next_byte())\n'
                                   '        for _ in range(count + 1):\n'
                                   '            destination.set_byte(0, low8(repeat_value))\n'
                                   '            destination = destination.advance(2)\n'
                                   '            destination.set_byte(0, low8(pair_value))\n'
                                   '            destination = destination.advance(2)\n'
                                   '            remaining = u16(remaining - 2)\n'
                                   '    else:\n'
                                   '        count = token & 31\n'
                                   '        repeat_value = replace_byte(repeat_value, '
                                   'source.next_byte())\n'
                                   '        for _ in range(count + 1):\n'
                                   '            destination.set_byte(0, low8(repeat_value))\n'
                                   '            destination = destination.advance(2)\n'
                                   '            remaining = u16(remaining - 1)\n'
                                   '            repeat_value = replace_word(repeat_value, '
                                   'u16(low16(repeat_value) + 1))\n'
                                   'return DuelLaneResult(source, destination, remaining, repeat_value, '
                                   'pair_value)'},
 'choose_duel_status_text': {'signature': 'state: SceneState, selection: Word, retained: Long=0',
                             'returns': 'Long',
                             'flow': "selection = uint(selection, 16, 'selection')\n"
                                     "retained = uint(retained, 32, 'retained text selection')\n"
                                     'displacement = u16(selection << 2)\n'
                                     'pointer = state.table(164416).long(displacement)\n'
                                     "state.set_scalar('ram_700e_long', pointer)\n"
                                     "state.set_scalar('ram_700c_word', 50688)\n"
                                     'return replace_word(retained, displacement)'},
 'scan_duel_thresholds': {'signature': 'state: SceneState, value: Word, thresholds: Cursor',
                          'returns': 'Word',
                          'flow': "value = uint(value, 16, 'value')\n"
                                  'thresholds = _live_cursor(state, thresholds)\n'
                                  'offset = 65534\n'
                                  'while True:\n'
                                  '    offset = u16(offset + 2)\n'
                                  '    threshold = thresholds.next_word()\n'
                                  '    if value < threshold:\n'
                                  '        return offset'},
 'append_duel_sprite': {'signature': 'state: SceneState, x: Word, y: Word, pattern: Word, attributes: '
                                     'Word',
                        'returns': 'DuelSpriteResult',
                        'flow': "x = uint(x, 16, 'x')\n"
                                "y = uint(y, 16, 'y')\n"
                                "pattern = uint(pattern, 16, 'pattern')\n"
                                "attributes = uint(attributes, 16, 'attributes')\n"
                                "destination = state.table(state.scalar('ram_7002_long')).cursor()\n"
                                'template = state.table(state.table(167992).long(u16(pattern << '
                                '2))).cursor()\n'
                                "next_sprite = state.scalar('ram_7000_word')\n"
                                'if destination.address() != 4294965248:\n'
                                '    destination.set_byte(0, low8(next_sprite), displacement=-5)\n'
                                'next_sprite = u16(next_sprite + 1)\n'
                                'flip = attributes & 6144\n'
                                'attributes &= 59391\n'
                                'extent = 0\n'
                                'while True:\n'
                                '    destination.append_word(u16(s8(template.byte(2)) + x + 128))\n'
                                '    size = u16(template.byte(1) << 8) | next_sprite\n'
                                '    next_sprite = u16(next_sprite + 1)\n'
                                '    destination.append_word(size)\n'
                                '    extent = u16((s16(size) >> 7 & 24) + 8)\n'
                                '    destination.append_word(u16(template.word(4) + attributes) ^ '
                                'flip)\n'
                                '    position = u16(s8(template.byte(3)))\n'
                                '    if flip & 2048:\n'
                                '        position = u16(-position - extent)\n'
                                '    destination.append_word(u16(position + y + 128))\n'
                                '    template = template.advance(6)\n'
                                '    if template.byte(0, displacement=-6) & 128:\n'
                                '        break\n'
                                'destination.set_byte(0, 0, displacement=-5)\n'
                                "state.set_scalar('ram_7002_long', destination.address())\n"
                                'next_sprite = u16(next_sprite - 1)\n'
                                "state.set_scalar('ram_7000_word', next_sprite)\n"
                                'return DuelSpriteResult(destination, next_sprite, extent)'},
 'measure_duel_weapon_contact': {'signature': 'state: SceneState, actor: Table, opponent: Table',
                                 'returns': 'DuelContact',
                                 'flow': 'actor = _live_table(state, actor)\n'
                                         'opponent = _live_table(state, opponent)\n'
                                         'mode_offset = u16(actor.word(12) << 1)\n'
                                         'reach = state.table(172640).word(mode_offset)\n'
                                         'if not actor.byte(24) & 8:\n'
                                         '    reach = u16(-reach)\n'
                                         'relative = u16(reach + actor.word(14) - opponent.word(14))\n'
                                         'magnitude = u16(-relative) if negative_word(relative) else '
                                         'relative\n'
                                         'facing_relative = u16(-relative) if actor.byte(24) & 8 else '
                                         'relative\n'
                                         'limit = state.table(172646).word(mode_offset)\n'
                                         'distance = u16(magnitude - limit)\n'
                                         'return DuelContact(distance, facing_relative, magnitude < '
                                         'limit)'},
 'sample_duel_probability': {'signature': 'state: SceneState, source_word: Word',
                             'returns': 'DuelProbability',
                             'flow': "source_word = uint(source_word, 16, 'probability word')\n"
                                     'mask = source_word & 7\n'
                                     'threshold = source_word >> 4\n'
                                     'sample = _random(state)\n'
                                     'masked = low16(sample) & mask\n'
                                     'return DuelProbability(replace_word(sample, masked), mask, '
                                     'threshold, masked < threshold)'},
 'choose_duel_ai_timeout': {'signature': 'state: SceneState, actor: Table, opponent: Table, command: '
                                         'Long, override: Word',
                            'returns': 'DuelAIResult',
                            'flow': 'actor = _live_table(state, actor)\n'
                                    'opponent = _live_table(state, opponent)\n'
                                    "command = uint(command, 32, 'command')\n"
                                    "override = uint(override, 16, 'override')\n"
                                    "if state.scalar('ram_70fa_word') > 6144:\n"
                                    "    if state.scalar('ram_700a_word') == 771:\n"
                                    '        readiness = actor.word(28)\n'
                                    '        if readiness <= opponent.word(28):\n'
                                    '            return DuelAIResult(replace_word(command, readiness), '
                                    '0, 0, 67)\n'
                                    'return DuelAIResult(0, 0, 0, override)'},
 '_copy_duel_palette': {'signature': 'state, source_base, destination_base',
                        'returns': None,
                        'flow': 'source = state.table(source_base).cursor()\n'
                                'destination = state.table(destination_base).cursor()\n'
                                'for _ in range(8):\n'
                                '    destination.append_word(source.next_word())'},
 'update_duel_actor': {'signature': 'state: SceneState, actor: Table, opponent: Table, context: '
                                    'DuelActorContext=DuelActorContext()',
                       'returns': 'DuelActorResult',
                       'flow': 'actor = _live_table(state, actor)\n'
                               'opponent = _live_table(state, opponent)\n'
                               'context.validate()\n'
                               'for offset in (8, 10, 38, 40):\n'
                               '    if actor.word(offset) != 0:\n'
                               '        actor.set_word(offset, u16(actor.word(offset) - 1))\n'
                               'flash_time = actor.word(40)\n'
                               'if flash_time != 0:\n'
                               '    source = 163968 if actor.address() == 16740432 else 164000\n'
                               '    destination = 4294966016 if actor.address() == 16740432 else '
                               '4294966048\n'
                               '    if not flash_time & 1:\n'
                               '        source = 164112\n'
                               '    _copy_duel_palette(state, source, destination)\n'
                               'command = replace_word(context.command, actor.word())\n'
                               'damage = context.damage\n'
                               'comparison = context.comparison\n'
                               'advance_attack = False\n'
                               'if not negative_word(actor.word(2)):\n'
                               '    direction = 0\n'
                               '    if not low16(command) & 256:\n'
                               '        direction = 1\n'
                               '        if low16(command) & 512:\n'
                               '            direction = 2\n'
                               '    actor.set_byte(3, direction)\n'
                               '    if low16(command) & 16:\n'
                               '        actor.set_byte(2, actor.byte(2) | 128)\n'
                               '        actor.set_byte(2, actor.byte(2) & 191)\n'
                               '        actor.set_word(4, 0)\n'
                               '        actor.set_word(8, actor.word(22))\n'
                               '    else:\n'
                               '        actor.set_word(2, actor.word(2) & 16383)\n'
                               '        if low16(command) & 8192:\n'
                               '            actor.set_byte(2, actor.byte(2) | 64)\n'
                               'else:\n'
                               '    command = replace_word(command, actor.word(4))\n'
                               '    if actor.word(8) == 0:\n'
                               '        if low16(command) == 4:\n'
                               '            contact = measure_duel_weapon_contact(state, actor, '
                               'opponent)\n'
                               '            if contact.borrowed:\n'
                               '                if opponent.byte(2) & 64:\n'
                               '                    comparison = replace_word(comparison, actor.word(2) '
                               '& 3)\n'
                               '                    opponent_kind = opponent.word(2) & 3\n'
                               '                    if opponent_kind == low16(comparison):\n'
                               '                        _sound(state, 160)\n'
                               '                        command = u32(s16(low16(command)))\n'
                               '                        comparison = u32(s16(low16(comparison)))\n'
                               '                    else:\n'
                               '                        command, comparison, damage = '
                               '_apply_duel_strike(state, actor, opponent, command, comparison)\n'
                               '                else:\n'
                               '                    command, comparison, damage = '
                               '_apply_duel_strike(state, actor, opponent, command, comparison)\n'
                               '        advance_attack = True\n'
                               'if advance_attack:\n'
                               '    actor.set_word(8, 4)\n'
                               '    command = replace_word(command, u16(low16(command) + 1))\n'
                               '    if low16(command) >= 5:\n'
                               '        command = replace_word(command, 0)\n'
                               '        actor.set_byte(2, actor.byte(2) & 127)\n'
                               '    actor.set_word(4, low16(command))\n'
                               'flash_time = actor.word(38)\n'
                               'if flash_time != 0:\n'
                               '    source = 163968 if actor.address() == 16740432 else 164000\n'
                               '    destination = 4294966016 if actor.address() == 16740432 else '
                               '4294966048\n'
                               '    glow = 1024 if actor.address() == 16740432 else 2048\n'
                               '    if not flash_time & 1:\n'
                               '        source = 164096\n'
                               '    actor.set_word(0, actor.word() & 62451 | glow)\n'
                               '    _copy_duel_palette(state, source, destination)\n'
                               'if actor.byte(2) & 16:\n'
                               '    if actor.word(10) == 0:\n'
                               '        actor.set_byte(2, actor.byte(2) & 239)\n'
                               'else:\n'
                               '    command = replace_word(command, actor.word())\n'
                               '    comparison = replace_word(comparison, low16(command))\n'
                               '    requested = low16(command) & 12\n'
                               '    blocked = False\n'
                               '    if requested:\n'
                               '        facing = 4 if actor.byte(24) & 8 else 8\n'
                               '        requested &= facing\n'
                               "        if requested and state.scalar('ram_7008_word') & 15 == 0:\n"
                               '            actor.set_byte(2, actor.byte(2) | 16)\n'
                               '            actor.set_word(10, 48)\n'
                               '            blocked = True\n'
                               '    if not blocked and low16(comparison) & 3072:\n'
                               '        actor.set_byte(2, actor.byte(2) | 32)\n'
                               '        position = actor.long(18)\n'
                               '        motion_time = actor.word(40)\n'
                               '        motion_time |= actor.word(38)\n'
                               '        if motion_time != 0:\n'
                               '            position = u32(position + 32768)\n'
                               '        if not low16(comparison) & 2048:\n'
                               '            position = u32(-position)\n'
                               '        position = u32(position + actor.long(14))\n'
                               '        separation = u32(position - opponent.long(14))\n'
                               '        if negative_long(separation):\n'
                               '            separation = u32(-separation)\n'
                               '        distance = high16(separation)\n'
                               '        if 16 <= distance < 224:\n'
                               '            actor.set_long(14, position)\n'
                               'render_duel_actor(state, actor, opponent)\n'
                               'return DuelActorResult(command, comparison, damage)'},
 '_apply_duel_strike': {'signature': 'state, actor, opponent, saved_command, saved_comparison',
                        'returns': None,
                        'flow': '_sound(state, 167)\n'
                                'opponent.set_word(38, 60)\n'
                                'rolled = low16(_random(state)) & 7\n'
                                'if rolled >= 6:\n'
                                '    rolled = u16(rolled - 4)\n'
                                'attribute = actor.word(30)\n'
                                'offset = scan_duel_thresholds(state, attribute, '
                                'state.table(167218).cursor())\n'
                                'damage = u16(rolled + state.table(167230).word(offset))\n'
                                'strength = actor.word(30)\n'
                                'weapon = actor.word(12)\n'
                                'if weapon == 0:\n'
                                '    equipment_index = u16(actor.word(44) << 1)\n'
                                '    strength = u16(strength + '
                                'state.table(167242).word(equipment_index))\n'
                                'elif weapon <= 1:\n'
                                '    equipment_index = u16(actor.word(42) << 1)\n'
                                '    strength = u16(strength + '
                                'state.table(167250).word(equipment_index))\n'
                                'else:\n'
                                '    equipment_index = u16(actor.word(46) << 1)\n'
                                '    strength = u16(strength + '
                                'state.table(167258).word(equipment_index))\n'
                                'product = u32(damage * strength)\n'
                                'kind = u16((actor.word(2) & 3) << 1)\n'
                                'divisor = state.table(167278).word(kind)\n'
                                'damage = divu_retained(product, divisor)\n'
                                'command = u32(s16(low16(saved_command)))\n'
                                'comparison = u32(s16(low16(saved_comparison)))\n'
                                'if actor.word(28) != 0:\n'
                                '    remaining = u16(opponent.word(28) - low16(damage))\n'
                                '    opponent.set_word(28, remaining)\n'
                                '    if negative_word(remaining):\n'
                                '        opponent.set_word(28, 0)\n'
                                'return (command, comparison, damage)'},
 'render_duel_actor': {'signature': 'state: SceneState, actor: Table, opponent: Table',
                       'returns': 'None',
                       'flow': 'actor = _live_table(state, actor)\n'
                               'opponent = _live_table(state, opponent)\n'
                               'if actor.byte(2) & 8:\n'
                               '    return\n'
                               'if actor.word(28) == 0:\n'
                               '    mode = actor.word(12)\n'
                               '    pattern = state.table(167820).byte(mode)\n'
                               '    attributes = actor.word(24)\n'
                               "    y = u16(actor.word(14) - state.scalar('ram_7006_word'))\n"
                               '    x = 84 if actor.byte(2) & 16 else 88\n'
                               '    append_duel_sprite(state, x, y, pattern, attributes)\n'
                               'else:\n'
                               '    mode_offset = u16(actor.word(12) * 18)\n'
                               '    pose = u16(actor.byte(3) * 6 + mode_offset)\n'
                               '    animation = actor.word(4)\n'
                               '    if actor.byte(2) & 64:\n'
                               '        animation = 5\n'
                               '    pose = u16(pose + animation)\n'
                               '    x = 84 if actor.byte(2) & 16 else 88\n'
                               "    y = u16(actor.word(14) - state.scalar('ram_7006_word'))\n"
                               '    append_duel_sprite(state, x, y, pose, actor.word(24))\n'
                               '_render_duel_movement_overlay(state, actor)'},
 '_render_duel_movement_overlay': {'signature': 'state, actor',
                                   'returns': None,
                                   'flow': 'if not actor.byte(2) & 32:\n'
                                           '    return\n'
                                           'if actor.word(10) == 0:\n'
                                           '    actor.set_word(10, 10)\n'
                                           '    animation = u16(actor.word(6) + 1)\n'
                                           '    if animation >= 5:\n'
                                           '        animation = 1\n'
                                           '        if actor.word() & 3072 == 0:\n'
                                           '            actor.set_byte(2, actor.byte(2) & 223)\n'
                                           '            animation = 0\n'
                                           '    actor.set_word(6, animation)\n'
                                           "y = u16(actor.word(14) - state.scalar('ram_7006_word'))\n"
                                           'pattern = 62 if actor.word(12) == 0 else 54\n'
                                           'pattern = u16(pattern + actor.word(6))\n'
                                           'if actor.byte(2) & 16:\n'
                                           "    pattern = u16((state.scalar('ram_7008_word') >> 4 & 1) "
                                           '+ 60)\n'
                                           'append_duel_sprite(state, 88, y, pattern, actor.word(24))'},
 'choose_duel_ai_override': {'signature': 'state: SceneState, actor: Table, opponent: Table, '
                                          'threshold_offset: Word',
                             'returns': 'Word',
                             'flow': 'actor = _live_table(state, actor)\n'
                                     'opponent = _live_table(state, opponent)\n'
                                     "threshold_offset = uint(threshold_offset, 16, 'threshold "
                                     "offset')\n"
                                     "if state.scalar('ram_7008_word') & 7:\n"
                                     '    return 0\n'
                                     'if actor.address() == 16740432:\n'
                                     '    opponent_readiness = opponent.word(28)\n'
                                     '    if opponent_readiness < 51:\n'
                                     '        if low16(_random(state)) & 1 == 0:\n'
                                     '            return 64\n'
                                     '    elif low16(_random(state)) & 3 == 0:\n'
                                     '        return 64\n'
                                     '    opponent_strength = opponent.word(30)\n'
                                     '    own_strength = actor.word(30)\n'
                                     '    readiness = actor.word(28)\n'
                                     '    if readiness < 40:\n'
                                     '        return 67 if low16(_random(state)) & 3 else 0\n'
                                     '    if readiness >= 70:\n'
                                     '        if opponent_strength >= own_strength:\n'
                                     '            return 67 if low16(_random(state)) & 1 else 0\n'
                                     '        return 67 if low16(_random(state)) & 3 == 0 else 0\n'
                                     '    if opponent_strength < own_strength:\n'
                                     '        return 67 if low16(_random(state)) & 1 else 0\n'
                                     '    return 67 if low16(_random(state)) & 3 else 0\n'
                                     'opponent_readiness = opponent.word(28)\n'
                                     'readiness = actor.word(28)\n'
                                     'if opponent_readiness < readiness:\n'
                                     '    if sample_duel_probability(state, '
                                     'state.table(174562).word(threshold_offset)).borrowed:\n'
                                     '        return 64\n'
                                     '    if sample_duel_probability(state, '
                                     'state.table(174574).word(threshold_offset)).borrowed:\n'
                                     '        return 33\n'
                                     '    return 0\n'
                                     'if readiness >= 80:\n'
                                     '    return 0\n'
                                     'if readiness >= 50:\n'
                                     '    opponent_strength = opponent.word(30)\n'
                                     '    own_strength = actor.word(30)\n'
                                     '    first_source = 173748 if opponent_strength >= own_strength '
                                     'else 173810\n'
                                     '    if sample_duel_probability(state, '
                                     'state.table(first_source).word(threshold_offset)).borrowed:\n'
                                     '        return 67\n'
                                     '    if sample_duel_probability(state, '
                                     'state.table(173760).word(threshold_offset)).borrowed:\n'
                                     '        return 64\n'
                                     '    return 0\n'
                                     'opponent_strength = opponent.word(30)\n'
                                     'opponent_offset = scan_duel_thresholds(state, opponent_strength, '
                                     'state.table(172808).cursor())\n'
                                     'if opponent_offset < 4:\n'
                                     '    source = 174370\n'
                                     'elif opponent_offset < 8:\n'
                                     '    source = 174204\n'
                                     'elif opponent_offset == 8:\n'
                                     '    source = 174040\n'
                                     'else:\n'
                                     '    source = 173868\n'
                                     'if _sample_duel_live_mode_pair(state, source, threshold_offset, '
                                     'False):\n'
                                     '    return 67\n'
                                     'if _sample_duel_live_mode_pair(state, source, threshold_offset, '
                                     'True):\n'
                                     '    return 66\n'
                                     'return 0'},
 '_sample_duel_live_mode_pair': {'signature': 'state, source, threshold_offset, second',
                                 'returns': None,
                                 'flow': 'if source == 174040:\n'
                                         '    base = 174132\n'
                                         'elif source == 174204:\n'
                                         '    base = 174298\n'
                                         'elif source == 174370:\n'
                                         '    base = 174464\n'
                                         'else:\n'
                                         '    base = 173962\n'
                                         "mode = state.scalar('ram_efd2_word')\n"
                                         'offset = 0 if mode == 0 else 24 if mode == 2 else 12\n'
                                         'if second:\n'
                                         '    offset += 36\n'
                                         'source_word = state.table(base).word(u16(threshold_offset + '
                                         'offset))\n'
                                         'return sample_duel_probability(state, source_word).borrowed'},
 'choose_duel_ai_command': {'signature': 'state: SceneState, actor: Table, opponent: Table, context: '
                                         'DuelAIContext=DuelAIContext()',
                            'returns': 'DuelAIResult',
                            'flow': 'actor = _live_table(state, actor)\n'
                                    'opponent = _live_table(state, opponent)\n'
                                    'context.validate()\n'
                                    'command = context.command\n'
                                    'threshold_offset = context.threshold_offset\n'
                                    'override = context.override\n'
                                    'if actor.word(34) != 0:\n'
                                    '    actor.set_word(34, u16(actor.word(34) - 1))\n'
                                    'readiness = actor.word(28)\n'
                                    'command = replace_word(command, readiness)\n'
                                    'if readiness == 0:\n'
                                    '    actor.set_word(2, 0)\n'
                                    '    actor.set_word(4, 0)\n'
                                    '    return DuelAIResult(command, context.comparison, '
                                    'threshold_offset, override)\n'
                                    'opponent_readiness = opponent.word(28)\n'
                                    'command = replace_word(command, opponent_readiness)\n'
                                    'if opponent_readiness == 0:\n'
                                    '    return DuelAIResult(replace_word(command, 256), '
                                    'context.comparison, threshold_offset, override)\n'
                                    'if actor.word(34) == 0:\n'
                                    '    command = _random(state)\n'
                                    '    command = replace_word(command, u16((low16(command) & 31) + '
                                    '30))\n'
                                    '    actor.set_word(34, low16(command))\n'
                                    '    attribute = actor.word(30)\n'
                                    '    threshold_offset = scan_duel_thresholds(state, attribute, '
                                    'state.table(172808).cursor())\n'
                                    '    override = choose_duel_ai_override(state, actor, opponent, '
                                    'threshold_offset)\n'
                                    '    timed = choose_duel_ai_timeout(state, actor, opponent, '
                                    'command, override)\n'
                                    '    command, override = (timed.command, timed.override)\n'
                                    '    command = replace_word(command, override)\n'
                                    '    if override != 0:\n'
                                    '        return DuelAIResult(command, context.comparison, '
                                    'threshold_offset, override)\n'
                                    '    dispatch_offset = u16(threshold_offset << 1)\n'
                                    '    dispatch_address = u32(172820 + s16(dispatch_offset))\n'
                                    '    continuation = state.service_at(dispatch_address, '
                                    'DuelActionContext(actor, opponent, DuelControlContext(command, '
                                    'context.comparison), threshold_offset))\n'
                                    '    if type(continuation) is not DuelActionResult:\n'
                                    "        raise Boundary('real AI vector handler result required')\n"
                                    '    continuation.validate()\n'
                                    '    command = continuation.controls.command\n'
                                    'action = actor.word(36)\n'
                                    'target_address = u32(172844 + s16(u16(action << 2)))\n'
                                    'result = state.service_at(target_address, DuelActionContext(actor, '
                                    'opponent, DuelControlContext(command, context.comparison), '
                                    'threshold_offset))\n'
                                    'if type(result) is not DuelActionResult:\n'
                                    "    raise Boundary('real AI action tail result required')\n"
                                    'result.validate()\n'
                                    'return DuelAIResult(result.controls.command, result.controls.mode, '
                                    'threshold_offset, override)'},
 '_stage_duel_words': {'signature': 'state, source_base, command, rows, row_command',
                       'returns': None,
                       'flow': 'from .business_reuse import stage_sprite_word_packet\n'
                               'return stage_sprite_word_packet(state, '
                               'state.table(source_base).cursor(), command, rows, row_command)'},
 '_configure_duel_action_dialog': {'signature': 'state, position, source',
                                   'returns': None,
                                   'flow': "state.set_scalar('ram_700c_word', position)\n"
                                           "state.set_scalar('ram_700e_long', source)"},
 '_configure_duel_dialog': {'signature': 'state, position, source',
                            'returns': None,
                            'flow': "state.set_scalar('ram_700c_word', position)\n"
                                    "state.set_scalar('ram_700e_long', source)\n"
                                    "state.set_scalar('ram_7014_word', 1)\n"
                                    "state.set_scalar('ram_7016_word', 2)"},
 '_choose_duel_ai_panel': {'signature': 'state, actor, opponent, controls',
                           'returns': None,
                           'flow': 'attribute = actor.word(30)\n'
                                   'threshold_offset = scan_duel_thresholds(state, attribute, '
                                   'state.table(162710).cursor())\n'
                                   'pointer_offset = u16(threshold_offset << 1)\n'
                                   'handler = state.table(162722).long(pointer_offset)\n'
                                   'result = state.service_at(handler, DuelActionContext(actor, '
                                   'opponent, controls, threshold_offset))\n'
                                   'if type(result) is not DuelActionResult:\n'
                                   "    raise Boundary('live duel panel handler must return its typed "
                                   "completion')\n"
                                   'result.validate()\n'
                                   'return result'},
 '_choose_duel_side_loadout': {'signature': 'state, second, controls',
                               'returns': None,
                               'flow': 'actor = state.table(16740512 if second else 16740432)\n'
                                       'opponent = state.table(16740432 if second else 16740512)\n'
                                       "mode_name = 'ram_700b_byte' if second else 'ram_700a_byte'\n"
                                       'choice = state.table(16740524 if second else 16740444)\n'
                                       'equipment_choice = state.table(16740578 if second else '
                                       '16740498)\n'
                                       'if state.scalar(mode_name) != 3:\n'
                                       '    _configure_duel_dialog(state, 50688, 166078)\n'
                                       '    if second:\n'
                                       "        state.set_scalar('ram_70da_word', 1)\n"
                                       '    advance_duel_entry_palette(state)\n'
                                       'while True:\n'
                                       '    _duel_frame(state)\n'
                                       '    advance_duel_entry_palette(state)\n'
                                       '    refresh_duel_actors(state)\n'
                                       '    if not second:\n'
                                       "        state.set_scalar('ram_708a_word', 0)\n"
                                       '    if state.scalar(mode_name) == 3:\n'
                                       '        result = _choose_duel_ai_panel(state, actor, opponent, '
                                       'controls)\n'
                                       '        controls = result.controls\n'
                                       '        if result.completion != 0 or second:\n'
                                       '            break\n'
                                       '        continue\n'
                                       '    controls = _second_controls(state, controls) if second else '
                                       '_first_controls(state, controls)\n'
                                       '    controls = choose_second_duel_equipment(state, choice, '
                                       'controls) if second else choose_first_duel_equipment(state, '
                                       'choice, controls)\n'
                                       "    if state.scalar('ram_700c_word') != 0:\n"
                                       '        continue\n'
                                       '    _stage_duel_words(state, 164354 if second else 164332, '
                                       '1610612740, 1, 60740 if second else 60680)\n'
                                       '    controls = _second_controls(state, controls) if second else '
                                       '_first_controls(state, controls)\n'
                                       '    controls = '
                                       'DuelControlContext(replace_word(controls.command, '
                                       'low16(controls.command) & 240), controls.mode)\n'
                                       '    if low16(controls.command) == 0:\n'
                                       '        continue\n'
                                       '    _sound(state, 172)\n'
                                       '    if state.scalar(mode_name) == 3:\n'
                                       '        break\n'
                                       '    clear_duel_text_plane(state)\n'
                                       '    _configure_duel_dialog(state, 50688, 166154)\n'
                                       '    while True:\n'
                                       '        _duel_frame(state)\n'
                                       '        advance_duel_entry_palette(state)\n'
                                       '        refresh_duel_actors(state)\n'
                                       '        controls = _second_controls(state, controls) if second '
                                       'else _first_controls(state, controls)\n'
                                       '        controls = choose_duel_two_option_menu(state, '
                                       'equipment_choice, controls)\n'
                                       "        if state.scalar('ram_700c_word') != 0:\n"
                                       '            continue\n'
                                       '        controls = _second_controls(state, controls) if second '
                                       'else _first_controls(state, controls)\n'
                                       '        controls = '
                                       'DuelControlContext(replace_word(controls.command, '
                                       'low16(controls.command) & 240), controls.mode)\n'
                                       '        if low16(controls.command) != 0:\n'
                                       '            break\n'
                                       '    _sound(state, 172)\n'
                                       '    if equipment_choice.word() != 0:\n'
                                       '        state.set_scalar(mode_name, 3)\n'
                                       '    break\n'
                                       'state.set_status_word(9984)\n'
                                       'configure_duel_weapon_motion(state, actor)\n'
                                       'clear_duel_text_plane(state)\n'
                                       'return controls'},
 '_wait_duel_status_text': {'signature': 'state, second, controls',
                            'returns': None,
                            'flow': 'if not second:\n'
                                    '    state.table(16740432).set_word(2, 0)\n'
                                    'else:\n'
                                    '    state.table(16740512).set_word(2, 0)\n'
                                    'while True:\n'
                                    '    _duel_frame(state)\n'
                                    '    if not second:\n'
                                    '        advance_duel_entry_palette(state)\n'
                                    '    refresh_duel_actors(state)\n'
                                    "    if state.scalar('ram_700c_word') != 0:\n"
                                    '        continue\n'
                                    '    controls = _second_controls(state, controls) if second else '
                                    '_first_controls(state, controls)\n'
                                    '    controls = DuelControlContext(replace_word(controls.command, '
                                    'low16(controls.command) & 240), controls.mode)\n'
                                    '    if low16(controls.command) != 0:\n'
                                    '        return controls'},
 '_initialize_duel_scene': {'signature': 'state, context',
                            'returns': None,
                            'flow': 'from .business_reuse import clear_video_sprite_plane, '
                                    'expand_glyph_stream\n'
                                    'from .contexts_reuse import GlyphColors\n'
                                    'from .business_scene import flush_scene_transfer_queue\n'
                                    'state.set_status_word(9984)\n'
                                    'command = replace_word(context.controls.command, '
                                    "state.scalar('ram_f606_word'))\n"
                                    'command = replace_byte(command, low8(command) & 191)\n'
                                    'state.mmio_write(12582916, 2, low16(command))\n'
                                    "state.set_scalar('ram_f612_word', 0)\n"
                                    'clear_video_sprite_plane(state)\n'
                                    'for command in (33592, 33336, 33799, 34156, 36151, 37524, 35587):\n'
                                    '    state.mmio_write(12582916, 2, command)\n'
                                    'first, second = (state.table(16740432), state.table(16740512))\n'
                                    'first.set_long(14, 4194304)\n'
                                    'first.set_word(24, 34816)\n'
                                    'first.set_word(2, 1)\n'
                                    'second.set_long(14, 16777216)\n'
                                    'second.set_word(24, 40960)\n'
                                    'second.set_word(2, 1)\n'
                                    "state.set_scalar('ram_70f0_word', 0)\n"
                                    "state.set_scalar('ram_70f6_word', 0)\n"
                                    "state.set_scalar('ram_70f8_word', 0)\n"
                                    'equipment = state.table(4294961800).cursor(u16(first.word(26) * '
                                    '3))\n'
                                    'first.set_byte(43, equipment.next_byte())\n'
                                    'first.set_byte(45, equipment.next_byte())\n'
                                    'first.set_byte(47, equipment.byte())\n'
                                    'equipment = state.table(4294961800).cursor(u16(second.word(26) * '
                                    '3))\n'
                                    'second.set_byte(43, equipment.next_byte())\n'
                                    'second.set_byte(45, equipment.next_byte())\n'
                                    'second.set_byte(47, equipment.byte())\n'
                                    'state.mmio_write(12582916, 4, 1073741824)\n'
                                    '_upload_longs(state, state.table(443316).cursor(), 12287)\n'
                                    'state.mmio_write(12582916, 4, 1073741827)\n'
                                    '_upload_longs(state, state.table(564700).cursor(), 31)\n'
                                    'expand_glyph_stream(state, state.table(566310).cursor(), '
                                    'state.table(4294955776).cursor(), GlyphColors(1, 2), '
                                    'replace_word(context.glyphs.remaining, 9))\n'
                                    '_upload_longs(state, state.table(4294955776).cursor(), 79)\n'
                                    'state.mmio_write(12582916, 4, 1342177283)\n'
                                    '_upload_longs(state, state.table(492468).cursor(), 47)\n'
                                    'state.mmio_write(12582916, 4, 1107296259)\n'
                                    'glyphs = upload_duel_officer_name(state, first.word(26), '
                                    'DuelGlyphContext(1, 2, 9))\n'
                                    'glyphs = upload_duel_officer_name(state, second.word(26), '
                                    'DuelGlyphContext(1, 2, glyphs.remaining))\n'
                                    'upload_duel_glyph_strip(state, state.table(166074).cursor(), '
                                    'DuelGlyphContext(1, 2, 1))\n'
                                    'clear_duel_text_plane(state)\n'
                                    'source, destination = (state.table(163968).cursor(), '
                                    'state.table(4294966016).cursor())\n'
                                    'for _ in range(32):\n'
                                    '    destination.append_long(source.next_long())\n'
                                    "state.set_scalar('ram_f31e_word', 1)\n"
                                    'map_source = state.table(492660).cursor()\n'
                                    "if state.scalar('ram_70f2_word') == 3:\n"
                                    '    map_source = state.table(493142).cursor()\n'
                                    'decode_duel_byte_lanes(state, map_source, '
                                    'state.table(16736256).cursor(), 1280)\n'
                                    'state.mmio_write(12582916, 4, 1610612739)\n'
                                    '_upload_words(state, state.table(16736256).cursor(), 1279)\n'
                                    'decode_duel_byte_lanes(state, state.table(493630).cursor(), '
                                    'state.table(16736256).cursor(), 1280)\n'
                                    'state.mmio_write(12582916, 4, 1879048195)\n'
                                    '_upload_words(state, state.table(16736256).cursor(), 1279)\n'
                                    "state.set_scalar('ram_f694_word', 1539)\n"
                                    "state.set_scalar('ram_f692_word', 1540)\n"
                                    '_stage_duel_words(state, 164128, 1610612776, 3, 59904)\n'
                                    'flush_scene_transfer_queue(state)\n'
                                    '_stage_duel_words(state, 164212, 1610612776, 5, 60288)\n'
                                    'return (first, second)'},
 '_finish_duel_scene': {'signature': 'state, controls, actor_values',
                        'returns': None,
                        'flow': 'from .business_scene import darken_palette\n'
                                'while True:\n'
                                '    _duel_frame(state)\n'
                                '    refresh_duel_actors(state)\n'
                                "    if state.scalar('ram_70f6_word') >= 16:\n"
                                '        return DuelSceneResult(controls, actor_values, 9472)\n'
                                "    darken_palette(state, state.scalar('ram_70f6_word'), 64, "
                                'state.table(163968).cursor())\n'
                                "    state.set_scalar('ram_70f6_word', "
                                "u16(state.scalar('ram_70f6_word') + 1))"},
 '_resolve_duel_pending_action': {'signature': 'state, actor, opponent, controls',
                                  'returns': None,
                                  'flow': "offset = u16(state.scalar('ram_7018_word') << 2)\n"
                                          'vector_address = u32(161142 + s16(offset))\n'
                                          'if vector_address == 161142:\n'
                                          '    handler = 161158\n'
                                          'elif vector_address == 161146:\n'
                                          '    handler = 161810\n'
                                          'elif vector_address == 161150:\n'
                                          '    handler = 161952\n'
                                          'elif vector_address == 161154:\n'
                                          '    handler = 162046\n'
                                          'else:\n'
                                          "    raise Boundary('original signed-WORD action vector "
                                          "leaves known BRA cells')\n"
                                          'result = state.service_at(handler, DuelActionContext(actor, '
                                          'opponent, controls))\n'
                                          'if type(result) is not DuelActionResult:\n'
                                          "    raise Boundary('original four-BRA action vector requires "
                                          "real handler outcome')\n"
                                          'result.validate()\n'
                                          'return result.controls'},
 '_choose_duel_command': {'signature': 'state, controls',
                          'returns': None,
                          'flow': 'state.set_status_word(9984)\n'
                                  "state.set_scalar('ram_d100_word', 0)\n"
                                  "second = negative_word(state.scalar('ram_7018_word'))\n"
                                  'actor = state.table(16740512 if second else 16740432)\n'
                                  'opponent = state.table(16740432 if second else 16740512)\n'
                                  "mode_name = 'ram_700b_byte' if second else 'ram_700a_byte'\n"
                                  'if state.scalar(mode_name) == 3:\n'
                                  '    command = actor.word() & 3\n'
                                  "    state.set_scalar('ram_7019_byte', command)\n"
                                  'else:\n'
                                  '    same_officer = actor.word(26) == actor.word(32)\n'
                                  '    _configure_duel_dialog(state, 52096 if same_officer else 51008, '
                                  '166180 if same_officer else 166122)\n'
                                  '    _sound(state, 173)\n'
                                  '    while True:\n'
                                  '        _duel_frame(state)\n'
                                  '        refresh_duel_actors(state)\n'
                                  '        first = _first_controls(state, controls)\n'
                                  '        controls = _second_controls(state, first) if '
                                  "negative_word(state.scalar('ram_7018_word')) else first\n"
                                  '        saved_input = controls.command\n'
                                  '        controls = choose_duel_action_menu(state, controls)\n'
                                  '        controls = DuelControlContext(replace_word(controls.command, '
                                  'low16(saved_input)), controls.mode)\n'
                                  "        if state.scalar('ram_700c_word') != 0:\n"
                                  '            continue\n'
                                  '        if low16(controls.command) & 32:\n'
                                  '            break\n'
                                  '        if low16(controls.command) & 16:\n'
                                  '            return controls\n'
                                  '_sound(state, 172)\n'
                                  'state.set_status_word(9984)\n'
                                  'clear_duel_text_plane(state)\n'
                                  'actor, opponent = (state.table(16740432), state.table(16740512))\n'
                                  "if negative_word(state.scalar('ram_7018_word')):\n"
                                  '    actor, opponent = (state.table(16740512), '
                                  'state.table(16740432))\n'
                                  'return _resolve_duel_pending_action(state, actor, opponent, '
                                  'controls)'},
 '_show_duel_action_result': {'signature': 'state, controls',
                              'returns': None,
                              'flow': "state.set_scalar('ram_f612_word', 1792)\n"
                                      'while state.read(4294964754, 1) != 0:\n'
                                      "    state.progress('duel_action_result_low_byte_ack')\n"
                                      'show_active_duel_turn_label(state)\n'
                                      "state.set_scalar('ram_f612_word', 1792)\n"
                                      'while state.read(4294964754, 1) != 0:\n'
                                      "    state.progress('duel_action_result_low_byte_ack')\n"
                                      'state.set_status_word(9984)\n'
                                      "selection = 34 if negative_word(state.scalar('ram_7018_word')) "
                                      'else 31\n'
                                      'choose_duel_status_text(state, selection)\n'
                                      'controls = wait_active_duel_action(state, controls)\n'
                                      'clear_duel_text_plane(state)\n'
                                      'selection = 32\n'
                                      "if negative_word(state.scalar('ram_7018_word')):\n"
                                      '    selection = u16(selection + 1)\n'
                                      'choose_duel_status_text(state, selection)\n'
                                      'return wait_either_duel_action(state, controls)'},
 'run_duel_scene': {'signature': 'state: SceneState, context: DuelSceneContext=DuelSceneContext()',
                    'returns': 'DuelSceneResult',
                    'flow': 'context.validate()\n'
                            'first, second = _initialize_duel_scene(state, context)\n'
                            'controls = _choose_duel_side_loadout(state, False, context.controls)\n'
                            'controls = _choose_duel_side_loadout(state, True, controls)\n'
                            'selection = low16(_random(state)) & 3\n'
                            'if selection == 3:\n'
                            '    selection = 0\n'
                            'choose_duel_status_text(state, selection)\n'
                            '_sound(state, 165)\n'
                            'controls = _wait_duel_status_text(state, False, controls)\n'
                            'state.set_status_word(9984)\n'
                            'clear_duel_text_plane(state)\n'
                            'selection = low16(_random(state)) & 3\n'
                            'if selection == 3:\n'
                            '    selection = 0\n'
                            'selection = u16(selection + 3)\n'
                            'choose_duel_status_text(state, selection)\n'
                            '_sound(state, 165)\n'
                            'controls = _wait_duel_status_text(state, True, controls)\n'
                            '_sound(state, 139)\n'
                            'actor_values = context.actor_values\n'
                            'while True:\n'
                            '    state.set_status_word(9984)\n'
                            '    clear_duel_text_plane(state)\n'
                            '    while True:\n'
                            '        _duel_frame(state)\n'
                            '        controls = _first_controls(state, controls)\n'
                            '        first.set_word(0, low16(controls.command))\n'
                            "        if state.scalar('ram_700a_byte') == 3:\n"
                            '            ai = choose_duel_ai_command(state, first, second, '
                            'DuelAIContext(controls.command, controls.mode))\n'
                            '            controls = DuelControlContext(ai.command, ai.comparison)\n'
                            '            first.set_word(0, low16(controls.command))\n'
                            '        first_result = update_duel_actor(state, first, second, '
                            'DuelActorContext(controls.command, controls.mode, actor_values.damage))\n'
                            '        controls = _second_controls(state, '
                            'DuelControlContext(first_result.command, first_result.comparison))\n'
                            '        second.set_word(0, low16(controls.command))\n'
                            "        if state.scalar('ram_700b_byte') == 3:\n"
                            '            ai = choose_duel_ai_command(state, second, first, '
                            'DuelAIContext(controls.command, controls.mode))\n'
                            '            controls = DuelControlContext(ai.command, ai.comparison)\n'
                            '            second.set_word(0, low16(controls.command))\n'
                            '        second_result = update_duel_actor(state, second, first, '
                            'DuelActorContext(controls.command, controls.mode, first_result.damage))\n'
                            '        controls = DuelControlContext(second_result.command, '
                            'second_result.comparison)\n'
                            '        actor_values = DuelActorContext(second_result.command, '
                            'second_result.comparison, second_result.damage)\n'
                            '        show_active_duel_turn_label(state)\n'
                            "        state.set_scalar('ram_7018_word', 0)\n"
                            '        if state.table(16740432).word(28) == 0:\n'
                            '            controls = _show_duel_action_result(state, controls)\n'
                            '            return _finish_duel_scene(state, controls, actor_values)\n'
                            "        state.set_scalar('ram_7018_word', 32768)\n"
                            '        if state.table(16740512).word(28) == 0:\n'
                            '            controls = _show_duel_action_result(state, controls)\n'
                            '            return _finish_duel_scene(state, controls, actor_values)\n'
                            '        active_flags = state.table(16740432).word(2)\n'
                            '        active_flags |= state.table(16740512).word(2)\n'
                            '        if active_flags & 53248:\n'
                            '            continue\n'
                            "        state.set_scalar('ram_7018_word', 0)\n"
                            '        if state.table(16740432).word() & 64:\n'
                            '            break\n'
                            "        state.set_scalar('ram_7018_word', 32768)\n"
                            '        if state.table(16740512).word() & 64:\n'
                            '            break\n'
                            '    controls = _choose_duel_command(state, controls)'}}

def _lower_advance_duel_entry_palette(emitter,rules):
    return _FLOW_LOWERERS['advance_duel_entry_palette'](emitter,rules)

def _lower_run_duel_scene(emitter,rules):
    return _FLOW_LOWERERS['run_duel_scene'](emitter,rules)

def _lower_show_active_duel_turn_label(emitter,rules):
    return _FLOW_LOWERERS['show_active_duel_turn_label'](emitter,rules)

def _lower_wait_active_duel_action(emitter,rules):
    return _FLOW_LOWERERS['wait_active_duel_action'](emitter,rules)

def _lower_configure_duel_weapon_motion(emitter,rules):
    return _FLOW_LOWERERS['configure_duel_weapon_motion'](emitter,rules)

def _lower_refresh_duel_actors(emitter,rules):
    return _FLOW_LOWERERS['refresh_duel_actors'](emitter,rules)

def _lower_upload_duel_officer_name(emitter,rules):
    return _ACTOR_LOWERERS['upload_duel_officer_name'](emitter,rules)

def _lower_clear_duel_text_plane(emitter,rules):
    return _ACTOR_LOWERERS['clear_duel_text_plane'](emitter,rules)

def _lower_choose_duel_two_option_menu(emitter,rules):
    emitter.segment(0x27d9c,0x27dfc)
    emitter.ins('move.w','(%a0),%d1',2)
    emitter.ins('andi.w',f'#0x{rules["direction_mask"]:x},%d0',4)
    emitter.ins('beq.b','scene_pc_027dba',2)
    emitter.ins('move.w',f'#0x{rules["direction_step"]:x},%d2',4)
    emitter.ins('andi.w',f'#0x{rules["positive_mask"]:x},%d0',4)
    emitter.ins('bne.b','scene_pc_027db0',2)
    emitter.ins('neg.w','%d2',2)
    emitter.ins('add.w','%d2,%d1',2)
    emitter.ins('cmpi.w',f'#0x{rules["accept_bound"]:x},%d1',4)
    emitter.ins(rules['accept_branch']+'.b','scene_pc_027dba',2)
    emitter.ins('move.w','%d1,(%a0)',2)
    emitter.ins('bsr.w','scene_pc_0279e6',4)
    emitter.ins('btst.l',f'#0x{rules["confirm_bit"]:x},%d0',4)
    emitter.ins('bne.w','scene_pc_027df4',4)
    emitter.ins('andi.w',f'#0x{rules["cursor_direction_mask"]:x},%d0',4)
    emitter.ins('bne.w','scene_pc_027dda',4)
    emitter.ins('move.w','0xff7008:l,%d0',6)
    emitter.ins('andi.w',f'#0x{rules["cursor_blink_mask"]:x},%d0',4)
    emitter.ins('beq.b','scene_pc_027df4',2)
    emitter.ins('move.w',f'#0x{rules["cursor_coordinate"]:x},%d0',4)
    emitter.ins('move.w','(%a0),%d1',2)
    emitter.ins('mulu.w',f'#0x{rules["cursor_stride"]:x},%d1',4)
    emitter.ins('addi.w',f'#0x{rules["cursor_bias"]:x},%d1',4)
    emitter.ins('move.w',f'#0x{rules["cursor_pattern"]:x},%d2',4)
    emitter.ins('move.w',f'#0x{rules["cursor_attributes"]:x},%d3',4)
    emitter.ins('bsr.w','scene_pc_028f9c',4)
    emitter.ins('subq.w',f'#0x{rules["timer_step"]:x},0xff70fa:l',6)
    emitter.ins('rts','',2)

def _lower_choose_first_duel_equipment(emitter,rules):
    emitter.segment(0x27dfc,0x27ed2)
    emitter.ins('lea.l','0xff707a:l,%a3',6)
    emitter.ins('bra.w','scene_pc_027e0c',4)
    emitter.ins('lea.l','0xff70ca:l,%a3',6)
    emitter.ins('move.w','(%a0),%d1',2)
    emitter.ins('tst.w','%d1',2)
    emitter.ins('bne.b','scene_pc_027e24',2)
    emitter.ins('tst.w','0x2(%a3)',4)
    emitter.ins('bne.b','scene_pc_027e3c',2)
    emitter.ins('addq.w',f'#0x{rules["repair_step"]:x},(%a0)',2)
    emitter.ins('cmpi.w','#0x3,(%a0)',4)
    emitter.ins('bcs.b','scene_pc_027e0c',2)
    emitter.ins('clr.w','(%a0)',2)
    emitter.ins('bra.b','scene_pc_027e0c',2)
    emitter.ins('cmpi.w','#0x1,%d1',4)
    emitter.ins('bne.b','scene_pc_027e34',2)
    emitter.ins('tst.w','(%a3)',2)
    emitter.ins('bne.w','scene_pc_027e3c',4)
    emitter.ins('bra.w','scene_pc_027e18',4)
    emitter.ins('tst.w','0x4(%a3)',4)
    emitter.ins('beq.w','scene_pc_027e18',4)
    emitter.ins('move.w','(%a0),%d1',2)
    emitter.ins('andi.w',f'#0x{rules["direction_mask"]:x},%d0',4)
    emitter.ins('beq.b','scene_pc_027e90',2)
    emitter.ins('move.w',f'#0x{rules["direction_step"]:x},%d2',4)
    emitter.ins('andi.w',f'#0x{rules["positive_mask"]:x},%d0',4)
    emitter.ins('bne.b','scene_pc_027e50',2)
    emitter.ins('neg.w','%d2',2)
    emitter.ins('add.w','%d2,%d1',2)
    emitter.ins('bpl.w','scene_pc_027e5a',4)
    emitter.ins('moveq','#2,%d1',2)
    emitter.ins('bra.b','scene_pc_027e64',2)
    emitter.ins('cmpi.w','#0x3,%d1',4)
    emitter.ins('bcs.w','scene_pc_027e64',4)
    emitter.ins('moveq','#0,%d1',2)
    emitter.ins('tst.w','%d1',2)
    emitter.ins('bne.w','scene_pc_027e72',4)
    emitter.ins('tst.w','0x2(%a3)',4)
    emitter.ins('bne.b','scene_pc_027e88',2)
    emitter.ins('bra.b','scene_pc_027e50',2)
    emitter.ins('cmpi.w','#0x1,%d1',4)
    emitter.ins('bne.w','scene_pc_027e82',4)
    emitter.ins('tst.w','(%a3)',2)
    emitter.ins('bne.w','scene_pc_027e88',4)
    emitter.ins('bra.b','scene_pc_027e50',2)
    emitter.ins('tst.w','0x4(%a3)',4)
    emitter.ins('beq.b','scene_pc_027e50',2)
    emitter.ins('cmpi.w','#0x3,%d1',4)
    emitter.ins('bcc.b','scene_pc_027e90',2)
    emitter.ins('move.w','%d1,(%a0)',2)
    emitter.ins('bsr.w','scene_pc_0279e6',4)
    emitter.ins('btst.l',f'#0x{rules["confirm_bit"]:x},%d0',4)
    emitter.ins('bne.w','scene_pc_027eca',4)
    emitter.ins('andi.w',f'#0x{rules["cursor_direction_mask"]:x},%d0',4)
    emitter.ins('bne.w','scene_pc_027eb0',4)
    emitter.ins('move.w','0xff7008:l,%d0',6)
    emitter.ins('andi.w',f'#0x{rules["cursor_blink_mask"]:x},%d0',4)
    emitter.ins('beq.b','scene_pc_027eca',2)
    emitter.ins('move.w',f'#0x{rules["cursor_coordinate"]:x},%d0',4)
    emitter.ins('move.w','(%a0),%d1',2)
    emitter.ins('mulu.w',f'#0x{rules["cursor_stride"]:x},%d1',4)
    emitter.ins('addi.w',f'#0x{rules["cursor_bias"]:x},%d1',4)
    emitter.ins('move.w',f'#0x{rules["cursor_pattern"]:x},%d2',4)
    emitter.ins('move.w',f'#0x{rules["cursor_attributes"]:x},%d3',4)
    emitter.ins('bsr.w','scene_pc_028f9c',4)
    emitter.ins('subq.w',f'#0x{rules["timer_step"]:x},0xff70fa:l',6)
    emitter.ins('rts','',2)

def _lower_choose_duel_action_menu(emitter,rules):
    _ACTION_LOWERERS['choose_duel_action_menu'](emitter,rules)

def _lower_decode_duel_byte_lanes(emitter,rules):
    return _ACTOR_LOWERERS['decode_duel_byte_lanes'](emitter,rules)

def _lower_choose_duel_status_text(emitter,rules):
    return _FLOW_LOWERERS['choose_duel_status_text'](emitter,rules)

def _lower_update_duel_actor(emitter,rules):
    return _ACTOR_LOWERERS['update_duel_actor'](emitter,rules)

def _lower_scan_duel_thresholds(emitter,rules):
    return _ACTOR_LOWERERS['scan_duel_thresholds'](emitter,rules)

def _lower_append_duel_sprite(emitter,rules):
    return _ACTOR_LOWERERS['append_duel_sprite'](emitter,rules)

def _lower_measure_duel_weapon_contact(emitter,rules):
    return _ACTOR_LOWERERS['measure_duel_weapon_contact'](emitter,rules)

def _lower_choose_duel_ai_command(emitter,rules):
    _AI_LOWERERS['choose_duel_ai_command'](emitter,rules)

def _lower_choose_duel_ai_override(emitter,rules):
    _AI_LOWERERS['choose_duel_ai_override'](emitter,rules)

def _lower_sample_duel_probability(emitter,rules):
    _AI_LOWERERS['sample_duel_probability'](emitter,rules)

def _lower_choose_duel_ai_timeout(emitter,rules):
    _AI_LOWERERS['choose_duel_ai_timeout'](emitter,rules)

LOWERERS={
    'advance_duel_entry_palette':_lower_advance_duel_entry_palette,
    'run_duel_scene':_lower_run_duel_scene,
    'show_active_duel_turn_label':_lower_show_active_duel_turn_label,
    'wait_active_duel_action':_lower_wait_active_duel_action,
    'configure_duel_weapon_motion':_lower_configure_duel_weapon_motion,
    'refresh_duel_actors':_lower_refresh_duel_actors,
    'upload_duel_officer_name':_lower_upload_duel_officer_name,
    'clear_duel_text_plane':_lower_clear_duel_text_plane,
    'choose_duel_two_option_menu':_lower_choose_duel_two_option_menu,
    'choose_first_duel_equipment':_lower_choose_first_duel_equipment,
    'choose_duel_action_menu':_lower_choose_duel_action_menu,
    'decode_duel_byte_lanes':_lower_decode_duel_byte_lanes,
    'choose_duel_status_text':_lower_choose_duel_status_text,
    'update_duel_actor':_lower_update_duel_actor,
    'scan_duel_thresholds':_lower_scan_duel_thresholds,
    'append_duel_sprite':_lower_append_duel_sprite,
    'measure_duel_weapon_contact':_lower_measure_duel_weapon_contact,
    'choose_duel_ai_command':_lower_choose_duel_ai_command,
    'choose_duel_ai_override':_lower_choose_duel_ai_override,
    'sample_duel_probability':_lower_sample_duel_probability,
    'choose_duel_ai_timeout':_lower_choose_duel_ai_timeout,
}

# These finite host ABI projections carry values already live in the original
# instructions and propagate their existing26D46 control tail. They allocate no
# target instruction or machine storage. Unsupported host edits remain rejected;
# this is not a claim that arbitrary Python metadata compiles to new code.
# These finite host ABI projections carry values already live in the original
# instructions and propagate their existing26D46 control tail. They allocate no
# target instruction or machine storage. Unsupported host edits remain rejected;
# this is not a claim that arbitrary Python metadata compiles to new code.
# These finite host ABI projections carry values already live in the original
# instructions and propagate their existing26D46 control tail. They allocate no
# target instruction or machine storage. Unsupported host edits remain rejected;
# this is not a claim that arbitrary Python metadata compiles to new code.
# These finite host ABI projections carry values already live in the original
# instructions and propagate their existing26D46 control tail. They allocate no
# target instruction or machine storage. Unsupported host edits remain rejected;
# this is not a claim that arbitrary Python metadata compiles to new code.
HOST_LINKAGE_DECLARATIONS = {'choose_duel_ai_command': {'signature': 'state: SceneState, actor: Table, opponent: Table, context: '
                                         'DuelAIContext=DuelAIContext()',
                            'returns': 'DuelAIResult',
                            'flow': 'actor = _live_table(state, actor)\n'
                                    'opponent = _live_table(state, opponent)\n'
                                    'if type(context) is not DuelAIContext:\n'
                                    "    raise ValueError('actual typed AI caller context required')\n"
                                    'context.validate()\n'
                                    'command = context.command\n'
                                    'comparison = context.comparison\n'
                                    'threshold_offset = context.threshold_offset\n'
                                    'override = context.override\n'
                                    'retained = context.retained\n'
                                    'if actor.word(34) != 0:\n'
                                    '    actor.set_word(34, u16(actor.word(34) - 1))\n'
                                    'readiness = actor.word(28)\n'
                                    'command = replace_word(command, readiness)\n'
                                    'if readiness == 0:\n'
                                    '    actor.set_word(2, 0)\n'
                                    '    actor.set_word(4, 0)\n'
                                    '    return DuelAIResult(command, comparison, threshold_offset, '
                                    'override, retained)\n'
                                    'opponent_readiness = opponent.word(28)\n'
                                    'command = replace_word(command, opponent_readiness)\n'
                                    'if opponent_readiness == 0:\n'
                                    '    return DuelAIResult(replace_word(command, 256), comparison, '
                                    'threshold_offset, override, retained)\n'
                                    'if actor.word(34) == 0:\n'
                                    '    command = _random(state)\n'
                                    '    command = replace_word(command, u16((low16(command) & 31) + 30))\n'
                                    '    actor.set_word(34, low16(command))\n'
                                    '    attribute = actor.word(30)\n'
                                    '    threshold_offset = scan_duel_thresholds(state, attribute, '
                                    'state.table(172808).cursor())\n'
                                    '    override = choose_duel_ai_override(state, actor, opponent, '
                                    'threshold_offset)\n'
                                    '    timed = choose_duel_ai_timeout(state, actor, opponent, command, '
                                    'override)\n'
                                    '    command, override = (timed.command, timed.override)\n'
                                    '    command = replace_word(command, override)\n'
                                    '    if override != 0:\n'
                                    '        return DuelAIResult(command, comparison, threshold_offset, '
                                    'override, retained)\n'
                                    '    dispatch_offset = u16(threshold_offset << 1)\n'
                                    '    dispatch_address = u32(172820 + s16(dispatch_offset))\n'
                                    '    continuation = state.service_at(dispatch_address, '
                                    'DuelActionContext(actor, opponent, DuelControlContext(command, '
                                    'comparison), threshold_offset, retained))\n'
                                    '    if type(continuation) is not DuelActionResult:\n'
                                    "        raise Boundary('real AI vector handler result required')\n"
                                    '    continuation.validate()\n'
                                    '    command = continuation.controls.command\n'
                                    '    comparison = continuation.controls.mode\n'
                                    '    retained = continuation.retained\n'
                                    'action = actor.word(36)\n'
                                    'target_address = u32(172844 + s16(u16(action << 2)))\n'
                                    'result = state.service_at(target_address, DuelActionContext(actor, '
                                    'opponent, DuelControlContext(command, comparison), threshold_offset, '
                                    'retained))\n'
                                    'if type(result) is not DuelActionResult:\n'
                                    "    raise Boundary('real AI action tail result required')\n"
                                    'result.validate()\n'
                                    'return DuelAIResult(result.controls.command, result.controls.mode, '
                                    'threshold_offset, override, result.retained)'},
 '_choose_duel_side_loadout': {'signature': 'state, second, controls',
                               'returns': None,
                               'flow': 'actor = state.table(16740512 if second else 16740432)\n'
                                       'opponent = state.table(16740432 if second else 16740512)\n'
                                       "mode_name = 'ram_700b_byte' if second else 'ram_700a_byte'\n"
                                       'choice = state.table(16740524 if second else 16740444)\n'
                                       'equipment_choice = state.table(16740578 if second else 16740498)\n'
                                       'if state.scalar(mode_name) != 3:\n'
                                       '    _configure_duel_dialog(state, 50688, 166078)\n'
                                       '    if second:\n'
                                       "        state.set_scalar('ram_70da_word', 1)\n"
                                       '    advance_duel_entry_palette(state)\n'
                                       'while True:\n'
                                       '    _duel_frame(state)\n'
                                       '    advance_duel_entry_palette(state)\n'
                                       '    refresh_duel_actors(state)\n'
                                       '    if not second:\n'
                                       "        state.set_scalar('ram_708a_word', 0)\n"
                                       '    if state.scalar(mode_name) == 3:\n'
                                       '        result = _choose_duel_ai_panel(state, actor, opponent, '
                                       'controls)\n'
                                       '        controls = result.controls\n'
                                       '        if result.completion is None:\n'
                                       "            raise Boundary('panel caller requires actual completion "
                                       "carrier')\n"
                                       '        if result.completion != 0 or second:\n'
                                       '            break\n'
                                       '        continue\n'
                                       '    controls = _second_controls(state, controls) if second else '
                                       '_first_controls(state, controls)\n'
                                       '    controls = choose_second_duel_equipment(state, choice, controls) '
                                       'if second else choose_first_duel_equipment(state, choice, controls)\n'
                                       "    if state.scalar('ram_700c_word') != 0:\n"
                                       '        continue\n'
                                       '    _stage_duel_words(state, 164354 if second else 164332, '
                                       '1610612740, 1, 60740 if second else 60680)\n'
                                       '    controls = _second_controls(state, controls) if second else '
                                       '_first_controls(state, controls)\n'
                                       '    controls = DuelControlContext(replace_word(controls.command, '
                                       'low16(controls.command) & 240), controls.mode)\n'
                                       '    if low16(controls.command) == 0:\n'
                                       '        continue\n'
                                       '    _sound(state, 172)\n'
                                       '    if state.scalar(mode_name) == 3:\n'
                                       '        break\n'
                                       '    clear_duel_text_plane(state)\n'
                                       '    _configure_duel_dialog(state, 50688, 166154)\n'
                                       '    while True:\n'
                                       '        _duel_frame(state)\n'
                                       '        advance_duel_entry_palette(state)\n'
                                       '        refresh_duel_actors(state)\n'
                                       '        controls = _second_controls(state, controls) if second else '
                                       '_first_controls(state, controls)\n'
                                       '        controls = choose_duel_two_option_menu(state, '
                                       'equipment_choice, controls)\n'
                                       "        if state.scalar('ram_700c_word') != 0:\n"
                                       '            continue\n'
                                       '        controls = _second_controls(state, controls) if second else '
                                       '_first_controls(state, controls)\n'
                                       '        controls = DuelControlContext(replace_word(controls.command, '
                                       'low16(controls.command) & 240), controls.mode)\n'
                                       '        if low16(controls.command) != 0:\n'
                                       '            break\n'
                                       '    _sound(state, 172)\n'
                                       '    if equipment_choice.word() != 0:\n'
                                       '        state.set_scalar(mode_name, 3)\n'
                                       '    break\n'
                                       'state.set_status_word(9984)\n'
                                       'configure_duel_weapon_motion(state, actor)\n'
                                       'clear_duel_text_plane(state)\n'
                                       'return controls'},
 '_resolve_duel_pending_action': {'signature': 'state, actor, opponent, controls, retained',
                                  'returns': None,
                                  'flow': "offset = u16(state.scalar('ram_7018_word') << 2)\n"
                                          'controls = DuelControlContext(replace_word(286331153, offset), '
                                          'replace_word(controls.mode, 65535))\n'
                                          'vector_address = u32(161142 + s16(offset))\n'
                                          'if vector_address == 161142:\n'
                                          '    handler = 161158\n'
                                          'elif vector_address == 161146:\n'
                                          '    handler = 161810\n'
                                          'elif vector_address == 161150:\n'
                                          '    handler = 161952\n'
                                          'elif vector_address == 161154:\n'
                                          '    handler = 162046\n'
                                          'else:\n'
                                          "    raise Boundary('original signed-WORD action vector leaves "
                                          "known BRA cells')\n"
                                          'result = state.service_at(handler, DuelActionContext(actor, '
                                          'opponent, controls, 0, retained))\n'
                                          'if type(result) is not DuelActionResult:\n'
                                          "    raise Boundary('original four-BRA action vector requires real "
                                          "handler outcome')\n"
                                          'result.validate()\n'
                                          'return result'},
 '_choose_duel_command': {'signature': 'state, controls, retained',
                          'returns': None,
                          'flow': 'state.set_status_word(9984)\n'
                                  "state.set_scalar('ram_d100_word', 0)\n"
                                  "second = negative_word(state.scalar('ram_7018_word'))\n"
                                  'actor = state.table(16740512 if second else 16740432)\n'
                                  'opponent = state.table(16740432 if second else 16740512)\n'
                                  "mode_name = 'ram_700b_byte' if second else 'ram_700a_byte'\n"
                                  'if state.scalar(mode_name) == 3:\n'
                                  '    command = actor.word() & 3\n'
                                  "    state.set_scalar('ram_7019_byte', command)\n"
                                  'else:\n'
                                  '    same_officer = actor.word(26) == actor.word(32)\n'
                                  '    _configure_duel_dialog(state, 52096 if same_officer else 51008, '
                                  '166180 if same_officer else 166122)\n'
                                  '    _sound(state, 173)\n'
                                  '    while True:\n'
                                  '        _duel_frame(state)\n'
                                  '        refresh_duel_actors(state)\n'
                                  '        first = _first_controls(state, controls)\n'
                                  '        controls = _second_controls(state, first) if '
                                  "negative_word(state.scalar('ram_7018_word')) else first\n"
                                  '        saved_input = controls.command\n'
                                  '        controls = choose_duel_action_menu(state, controls)\n'
                                  '        controls = DuelControlContext(replace_word(controls.command, '
                                  'low16(saved_input)), controls.mode)\n'
                                  "        if state.scalar('ram_700c_word') != 0:\n"
                                  '            continue\n'
                                  '        if low16(controls.command) & 32:\n'
                                  '            break\n'
                                  '        if low16(controls.command) & 16:\n'
                                  '            return DuelActionResult(controls, 0, retained)\n'
                                  '_sound(state, 172)\n'
                                  'state.set_status_word(9984)\n'
                                  'clear_duel_text_plane(state)\n'
                                  'actor, opponent = (state.table(16740432), state.table(16740512))\n'
                                  "if negative_word(state.scalar('ram_7018_word')):\n"
                                  '    actor, opponent = (state.table(16740512), state.table(16740432))\n'
                                  'return _resolve_duel_pending_action(state, actor, opponent, controls, '
                                  'retained)'},
 'run_duel_scene': {'signature': 'state: SceneState, context: DuelSceneContext=DuelSceneContext()',
                    'returns': 'DuelSceneResult',
                    'flow': 'context.validate()\n'
                            'first, second = _initialize_duel_scene(state, context)\n'
                            'controls = _choose_duel_side_loadout(state, False, context.controls)\n'
                            'controls = _choose_duel_side_loadout(state, True, controls)\n'
                            'selection = low16(_random(state)) & 3\n'
                            'if selection == 3:\n'
                            '    selection = 0\n'
                            'choose_duel_status_text(state, selection)\n'
                            '_sound(state, 165)\n'
                            'controls = _wait_duel_status_text(state, False, controls)\n'
                            'state.set_status_word(9984)\n'
                            'clear_duel_text_plane(state)\n'
                            'selection = low16(_random(state)) & 3\n'
                            'if selection == 3:\n'
                            '    selection = 0\n'
                            'selection = u16(selection + 3)\n'
                            'choose_duel_status_text(state, selection)\n'
                            '_sound(state, 165)\n'
                            'controls = _wait_duel_status_text(state, True, controls)\n'
                            '_sound(state, 139)\n'
                            'actor_values = context.actor_values\n'
                            'retained = None\n'
                            'while True:\n'
                            '    state.set_status_word(9984)\n'
                            '    clear_duel_text_plane(state)\n'
                            '    while True:\n'
                            '        _duel_frame(state)\n'
                            '        controls = _first_controls(state, controls)\n'
                            '        first.set_word(0, low16(controls.command))\n'
                            "        if state.scalar('ram_700a_byte') == 3:\n"
                            '            if retained is None:\n'
                            "                raise Boundary('full scene loop lacks current retained values "
                            "after unprojected callees')\n"
                            '            ai = choose_duel_ai_command(state, first, second, '
                            'DuelAIContext(controls.command, controls.mode, 0, 0, retained))\n'
                            '            controls = DuelControlContext(ai.command, ai.comparison)\n'
                            '            retained = ai.retained\n'
                            '            first.set_word(0, low16(controls.command))\n'
                            '        first_result = update_duel_actor(state, first, second, '
                            'DuelActorContext(controls.command, controls.mode, actor_values.damage))\n'
                            '        controls = _second_controls(state, '
                            'DuelControlContext(first_result.command, first_result.comparison))\n'
                            '        second.set_word(0, low16(controls.command))\n'
                            "        if state.scalar('ram_700b_byte') == 3:\n"
                            '            if retained is None:\n'
                            "                raise Boundary('full scene loop lacks current retained values "
                            "after unprojected callees')\n"
                            '            ai = choose_duel_ai_command(state, second, first, '
                            'DuelAIContext(controls.command, controls.mode, 0, 0, retained))\n'
                            '            controls = DuelControlContext(ai.command, ai.comparison)\n'
                            '            retained = ai.retained\n'
                            '            second.set_word(0, low16(controls.command))\n'
                            '        second_result = update_duel_actor(state, second, first, '
                            'DuelActorContext(controls.command, controls.mode, first_result.damage))\n'
                            '        controls = DuelControlContext(second_result.command, '
                            'second_result.comparison)\n'
                            '        actor_values = DuelActorContext(second_result.command, '
                            'second_result.comparison, second_result.damage)\n'
                            '        show_active_duel_turn_label(state)\n'
                            "        state.set_scalar('ram_7018_word', 0)\n"
                            '        if state.table(16740432).word(28) == 0:\n'
                            '            controls = _show_duel_action_result(state, controls)\n'
                            '            return _finish_duel_scene(state, controls, actor_values)\n'
                            "        state.set_scalar('ram_7018_word', 32768)\n"
                            '        if state.table(16740512).word(28) == 0:\n'
                            '            controls = _show_duel_action_result(state, controls)\n'
                            '            return _finish_duel_scene(state, controls, actor_values)\n'
                            '        active_flags = state.table(16740432).word(2)\n'
                            '        active_flags |= state.table(16740512).word(2)\n'
                            '        if active_flags & 53248:\n'
                            '            continue\n'
                            "        state.set_scalar('ram_7018_word', 0)\n"
                            '        if state.table(16740432).word() & 64:\n'
                            '            break\n'
                            "        state.set_scalar('ram_7018_word', 32768)\n"
                            '        if state.table(16740512).word() & 64:\n'
                            '            break\n'
                            '    if retained is None:\n'
                            "        raise Boundary('full scene loop lacks current pending-action values "
                            "after unprojected callees')\n"
                            '    result = _choose_duel_command(state, controls, retained)\n'
                            '    controls, retained = (result.controls, result.retained)\n'
                            '    if result.discarded_continuation is not None:\n'
                            '        if result.discarded_continuation.return_carrier != 161138:\n'
                            "            raise Boundary('unknown discarded duel scene continuation')\n"
                            '        return _finish_duel_scene(state, controls, actor_values)'}}
DECLARATIONS.update(HOST_LINKAGE_DECLARATIONS)
APPROVED['contexts_duel'].add('DuelRetainedValues')




# Finite actual host returns/stack effects of existing actor instructions.
# These bodies are all admitted; unsupported edits fail. No new native
# allocation is implied by this host-ABI projection.
HOST_ACTOR_DECLARATIONS = {'_actor_word': {'signature': 'value, word',
                 'returns': None,
                 'flow': 'return None if value is None else replace_word(value, word)'},
 '_actor_byte': {'signature': 'value, byte',
                 'returns': None,
                 'flow': 'return None if value is None else replace_byte(value, byte)'},
 '_actor_input_frame': {'signature': 'context',
                        'returns': None,
                        'flow': 'if type(context) is not DuelActorContext:\n'
                                "    raise ValueError('actual actor input required')\n"
                                'context.validate()\n'
                                'retained = context.retained\n'
                                'return DuelActorFrame(context.command, context.comparison, context.damage, '
                                'retained.factor if retained is not None else None, '
                                'retained.weapon_difference if retained is not None else None, '
                                'retained.variation if retained is not None else None).validate()'},
 '_actor_stack': {'signature': 'state, frame, stack',
                  'returns': None,
                  'flow': 'if type(frame) is not DuelActorFrame:\n'
                          "    raise ValueError('actual current actor frame required')\n"
                          'frame.validate()\n'
                          'if stack is not None:\n'
                          '    return _live_cursor(state, stack)\n'
                          'if frame.complete:\n'
                          "    raise Boundary('complete actor return needs the actual live stack cursor')\n"
                          'return None'},
 '_push_actor_longs': {'signature': 'stack, values',
                       'returns': None,
                       'flow': 'if stack is None:\n'
                               '    return\n'
                               'for value in values[::-1]:\n'
                               '    if value is None:\n'
                               "        raise Boundary('native saved actor value is unknown')\n"
                               "    uint(value, 32, 'actual saved actor value')\n"
                               'for value in values[::-1]:\n'
                               '    stack.base = u32(stack.base - 4)\n'
                               '    stack.set_long(0, value)'},
 '_pop_actor_longs': {'signature': 'stack, count',
                      'returns': None,
                      'flow': 'return tuple((stack.next_long() for _ in range(count)))'},
 '_push_actor_pair_words': {'signature': 'stack, command, comparison',
                            'returns': None,
                            'flow': 'if stack is None:\n'
                                    '    return\n'
                                    'stack.base = u32(stack.base - 2)\n'
                                    'stack.set_word(0, low16(comparison))\n'
                                    'stack.base = u32(stack.base - 2)\n'
                                    'stack.set_word(0, low16(command))'},
 '_pop_actor_pair_words': {'signature': 'stack, command, comparison',
                           'returns': None,
                           'flow': 'if stack is not None:\n'
                                   '    command, comparison = (stack.next_word(), stack.next_word())\n'
                                   'return (u32(s16(low16(command))), u32(s16(low16(comparison))))'},
 'refresh_duel_actors': {'signature': 'state: SceneState, frame: DuelActorFrame | None=None, stack: Cursor | '
                                      'None=None, caller_actor: Table | None=None, caller_opponent: Table | '
                                      'None=None',
                         'returns': 'DuelRenderResult',
                         'flow': 'current = DuelActorFrame() if frame is None else frame\n'
                                 'stack = _actor_stack(state, current, stack)\n'
                                 'if stack is not None:\n'
                                 '    caller_actor = _live_table(state, caller_actor)\n'
                                 '    caller_opponent = _live_table(state, caller_opponent)\n'
                                 '    _push_actor_longs(stack, (caller_actor.base, caller_opponent.base))\n'
                                 'first, second = (state.table(16740432), state.table(16740512))\n'
                                 'first.set_word(0, 0)\n'
                                 'first_result = render_duel_actor(state, first, second, current, stack)\n'
                                 'second.set_word(0, 0)\n'
                                 'second_result = render_duel_actor(state, second, first, '
                                 'first_result.frame, stack)\n'
                                 'if stack is not None:\n'
                                 '    actor_base, opponent_base = _pop_actor_longs(stack, 2)\n'
                                 '    caller_actor, caller_opponent = (state.table(actor_base), '
                                 'state.table(opponent_base))\n'
                                 'return DuelRenderResult(second_result.frame, caller_actor, '
                                 'caller_opponent, stack).validate(state)'},
 'append_duel_sprite': {'signature': 'state: SceneState, x: Word, y: Word, pattern: Word, attributes: Word, '
                                     'frame: DuelActorFrame | None=None, stack: Cursor | None=None',
                        'returns': 'DuelSpriteResult',
                        'flow': "x = uint(x, 16, 'x')\n"
                                "y = uint(y, 16, 'y')\n"
                                "pattern = uint(pattern, 16, 'pattern')\n"
                                "attributes = uint(attributes, 16, 'attributes')\n"
                                'current = DuelActorFrame() if frame is None else frame\n'
                                'stack = _actor_stack(state, current, stack)\n'
                                'for value, supplied in ((current.command, x), (current.comparison, y), '
                                '(current.distance, pattern), (current.factor, attributes)):\n'
                                '    if value is not None and low16(value) != supplied:\n'
                                "        raise ValueError('sprite arguments must agree with the current "
                                "partial values')\n"
                                '_push_actor_longs(stack, (current.command, current.comparison, '
                                'current.distance, current.factor))\n'
                                "destination = state.table(state.scalar('ram_7002_long')).cursor()\n"
                                'template = state.table(state.table(167992).long(u16(pattern << '
                                '2))).cursor()\n'
                                "next_sprite = state.scalar('ram_7000_word')\n"
                                'if destination.address() != 4294965248:\n'
                                '    destination.set_byte(0, low8(next_sprite), displacement=-5)\n'
                                'next_sprite = u16(next_sprite + 1)\n'
                                'flip = attributes & 6144\n'
                                'flip_value = _actor_word(current.weapon_difference, flip)\n'
                                'animation_value = current.variation\n'
                                'attributes &= 59391\n'
                                'extent = 0\n'
                                'while True:\n'
                                '    vertical_delta = template.byte(2)\n'
                                '    animation_value = _actor_byte(animation_value, vertical_delta)\n'
                                '    animation_value = _actor_word(animation_value, '
                                'u16(s8(vertical_delta)))\n'
                                '    vertical = u16(s8(vertical_delta) + x + 128)\n'
                                '    animation_value = _actor_word(animation_value, vertical)\n'
                                '    destination.append_word(vertical)\n'
                                '    size_byte = template.byte(1)\n'
                                '    animation_value = _actor_byte(animation_value, size_byte)\n'
                                '    animation_value = _actor_word(animation_value, '
                                'u16(low16(animation_value) << 8)) if animation_value is not None else None\n'
                                '    size = u16(size_byte << 8) | next_sprite\n'
                                '    animation_value = _actor_word(animation_value, size)\n'
                                '    next_sprite = u16(next_sprite + 1)\n'
                                '    destination.append_word(size)\n'
                                '    extent = u16((s16(size) >> 7 & 24) + 8)\n'
                                '    animation_value = _actor_word(animation_value, extent)\n'
                                '    tile_word = u16(template.word(4) + attributes) ^ flip\n'
                                '    animation_value = _actor_word(animation_value, tile_word)\n'
                                '    destination.append_word(tile_word)\n'
                                '    position_byte = template.byte(3)\n'
                                '    animation_value = _actor_byte(animation_value, position_byte)\n'
                                '    position = u16(s8(position_byte))\n'
                                '    animation_value = _actor_word(animation_value, position)\n'
                                '    if flip & 2048:\n'
                                '        position = u16(-position)\n'
                                '        animation_value = _actor_word(animation_value, position)\n'
                                '        position = u16(position - extent)\n'
                                '        animation_value = _actor_word(animation_value, position)\n'
                                '    horizontal = u16(position + y + 128)\n'
                                '    animation_value = _actor_word(animation_value, horizontal)\n'
                                '    destination.append_word(horizontal)\n'
                                '    template = template.advance(6)\n'
                                '    if template.byte(0, displacement=-6) & 128:\n'
                                '        break\n'
                                'destination.set_byte(0, 0, displacement=-5)\n'
                                "state.set_scalar('ram_7002_long', destination.address())\n"
                                'next_sprite = u16(next_sprite - 1)\n'
                                "state.set_scalar('ram_7000_word', next_sprite)\n"
                                'saved = (current.command, current.comparison, current.distance, '
                                'current.factor)\n'
                                'if stack is not None:\n'
                                '    saved = _pop_actor_longs(stack, 4)\n'
                                'returned = DuelActorFrame(saved[0], saved[1], saved[2], saved[3], '
                                'flip_value, animation_value).validate()\n'
                                'return DuelSpriteResult(destination, next_sprite, extent, returned, stack, '
                                'template)'},
 'measure_duel_weapon_contact': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: '
                                              'DuelActorFrame | None=None',
                                 'returns': 'DuelContact',
                                 'flow': 'actor = _live_table(state, actor)\n'
                                         'opponent = _live_table(state, opponent)\n'
                                         'current = DuelActorFrame() if frame is None else frame\n'
                                         'if type(current) is not DuelActorFrame:\n'
                                         "    raise ValueError('actual contact frame required')\n"
                                         'current.validate()\n'
                                         'mode_offset = u16(actor.word(12) << 1)\n'
                                         'reach = state.table(172640).word(mode_offset)\n'
                                         'if not actor.byte(24) & 8:\n'
                                         '    reach = u16(-reach)\n'
                                         'relative = u16(reach + actor.word(14) - opponent.word(14))\n'
                                         'magnitude = u16(-relative) if negative_word(relative) else '
                                         'relative\n'
                                         'facing_relative = u16(-relative) if actor.byte(24) & 8 else '
                                         'relative\n'
                                         'limit = state.table(172646).word(mode_offset)\n'
                                         'distance = u16(magnitude - limit)\n'
                                         'returned = DuelActorFrame(current.command, '
                                         '_actor_word(current.comparison, mode_offset), '
                                         '_actor_word(current.distance, distance), '
                                         '_actor_word(current.factor, facing_relative), '
                                         'current.weapon_difference, current.variation).validate()\n'
                                         'return DuelContact(distance, facing_relative, magnitude < limit, '
                                         'returned)'},
 'update_duel_actor': {'signature': 'state: SceneState, actor: Table, opponent: Table, context: '
                                    'DuelActorContext=DuelActorContext()',
                       'returns': 'DuelActorResult',
                       'flow': 'actor = _live_table(state, actor)\n'
                               'opponent = _live_table(state, opponent)\n'
                               'current = _actor_input_frame(context)\n'
                               'stack = _actor_stack(state, current, context.stack)\n'
                               'factor, flip_value, variation = (current.factor, current.weapon_difference, '
                               'current.variation)\n'
                               'for offset in (8, 10, 38, 40):\n'
                               '    if actor.word(offset) != 0:\n'
                               '        actor.set_word(offset, u16(actor.word(offset) - 1))\n'
                               'flash_time = actor.word(40)\n'
                               'comparison = replace_word(context.comparison, flash_time)\n'
                               'if flash_time != 0:\n'
                               '    source = 163968 if actor.address() == 16740432 else 164000\n'
                               '    destination = 4294966016 if actor.address() == 16740432 else 4294966048\n'
                               '    comparison = replace_word(comparison, flash_time & 1)\n'
                               '    if not flash_time & 1:\n'
                               '        source = 164112\n'
                               '    _copy_duel_palette(state, source, destination)\n'
                               '    variation = _actor_word(variation, 65535)\n'
                               'command = replace_word(context.command, actor.word())\n'
                               'damage = context.damage\n'
                               'advance_attack = False\n'
                               'if not negative_word(actor.word(2)):\n'
                               '    direction = 0\n'
                               '    comparison = replace_word(comparison, 0)\n'
                               '    if not low16(command) & 256:\n'
                               '        direction = 1\n'
                               '        if low16(command) & 512:\n'
                               '            direction = 2\n'
                               '    actor.set_byte(3, direction)\n'
                               '    comparison = replace_word(comparison, direction)\n'
                               '    if low16(command) & 16:\n'
                               '        actor.set_byte(2, actor.byte(2) | 128)\n'
                               '        actor.set_byte(2, actor.byte(2) & 191)\n'
                               '        actor.set_word(4, 0)\n'
                               '        actor.set_word(8, actor.word(22))\n'
                               '    else:\n'
                               '        actor.set_word(2, actor.word(2) & 16383)\n'
                               '        if low16(command) & 8192:\n'
                               '            actor.set_byte(2, actor.byte(2) | 64)\n'
                               'else:\n'
                               '    command = replace_word(command, actor.word(4))\n'
                               '    if actor.word(8) == 0:\n'
                               '        if low16(command) == 4:\n'
                               '            contact = measure_duel_weapon_contact(state, actor, opponent, '
                               'DuelActorFrame(command, comparison, damage, factor, flip_value, variation))\n'
                               '            comparison, damage, factor = (contact.frame.comparison, '
                               'contact.frame.distance, contact.frame.factor)\n'
                               '            if contact.borrowed:\n'
                               '                if opponent.byte(2) & 64:\n'
                               '                    comparison = replace_word(comparison, actor.word(2) & '
                               '3)\n'
                               '                    opponent_kind = opponent.word(2) & 3\n'
                               '                    damage = replace_word(damage, opponent_kind)\n'
                               '                    if opponent_kind == low16(comparison):\n'
                               '                        _push_actor_pair_words(stack, command, comparison)\n'
                               '                        _sound(state, 160)\n'
                               '                        command, comparison = _pop_actor_pair_words(stack, '
                               'command, comparison)\n'
                               '                    else:\n'
                               '                        struck = _apply_duel_strike(state, actor, opponent, '
                               'DuelActorFrame(command, comparison, damage, factor, flip_value, variation), '
                               'stack)\n'
                               '                        command, comparison, damage = (struck.command, '
                               'struck.comparison, struck.distance)\n'
                               '                        factor, flip_value, variation = (struck.factor, '
                               'struck.weapon_difference, struck.variation)\n'
                               '                else:\n'
                               '                    struck = _apply_duel_strike(state, actor, opponent, '
                               'DuelActorFrame(command, comparison, damage, factor, flip_value, variation), '
                               'stack)\n'
                               '                    command, comparison, damage = (struck.command, '
                               'struck.comparison, struck.distance)\n'
                               '                    factor, flip_value, variation = (struck.factor, '
                               'struck.weapon_difference, struck.variation)\n'
                               '        advance_attack = True\n'
                               'if advance_attack:\n'
                               '    actor.set_word(8, 4)\n'
                               '    command = replace_word(command, u16(low16(command) + 1))\n'
                               '    if low16(command) >= 5:\n'
                               '        command = replace_word(command, 0)\n'
                               '        actor.set_byte(2, actor.byte(2) & 127)\n'
                               '    actor.set_word(4, low16(command))\n'
                               'flash_time = actor.word(38)\n'
                               'command = replace_word(command, flash_time)\n'
                               'if flash_time != 0:\n'
                               '    source = 163968 if actor.address() == 16740432 else 164000\n'
                               '    destination = 4294966016 if actor.address() == 16740432 else 4294966048\n'
                               '    glow = 1024 if actor.address() == 16740432 else 2048\n'
                               '    comparison = replace_word(comparison, glow)\n'
                               '    command = replace_word(command, flash_time & 1)\n'
                               '    if not flash_time & 1:\n'
                               '        source = 164096\n'
                               '    actor.set_word(0, actor.word() & 62451 | glow)\n'
                               '    _copy_duel_palette(state, source, destination)\n'
                               '    factor = _actor_word(factor, 65535)\n'
                               'if actor.byte(2) & 16:\n'
                               '    if actor.word(10) == 0:\n'
                               '        actor.set_byte(2, actor.byte(2) & 239)\n'
                               'else:\n'
                               '    command = replace_word(command, actor.word())\n'
                               '    comparison = replace_word(comparison, low16(command))\n'
                               '    requested = low16(command) & 12\n'
                               '    command = replace_word(command, requested)\n'
                               '    blocked = False\n'
                               '    if requested:\n'
                               '        facing = 4 if actor.byte(24) & 8 else 8\n'
                               '        factor = _actor_word(factor, facing)\n'
                               '        requested &= facing\n'
                               '        command = replace_word(command, requested)\n'
                               '        if requested:\n'
                               "            current_tick = state.scalar('ram_7008_word') & 15\n"
                               '            command = replace_word(command, current_tick)\n'
                               '            if current_tick == 0:\n'
                               '                actor.set_byte(2, actor.byte(2) | 16)\n'
                               '                actor.set_word(10, 48)\n'
                               '                blocked = True\n'
                               '    if not blocked and low16(comparison) & 3072:\n'
                               '        comparison = replace_word(comparison, low16(comparison) & 3072)\n'
                               '        actor.set_byte(2, actor.byte(2) | 32)\n'
                               '        position = actor.long(18)\n'
                               '        motion_time = actor.word(40)\n'
                               '        motion_time |= actor.word(38)\n'
                               '        factor = _actor_word(factor, motion_time)\n'
                               '        if motion_time != 0:\n'
                               '            position = u32(position + 32768)\n'
                               '        if not low16(comparison) & 2048:\n'
                               '            position = u32(-position)\n'
                               '        comparison = replace_word(comparison, low16(comparison) & 2048)\n'
                               '        position = u32(position + actor.long(14))\n'
                               '        separation = u32(position - opponent.long(14))\n'
                               '        if negative_long(separation):\n'
                               '            separation = u32(-separation)\n'
                               '        comparison = swap_words(separation)\n'
                               '        distance = high16(separation)\n'
                               '        if 16 <= distance < 224:\n'
                               '            actor.set_long(14, position)\n'
                               '        damage = position\n'
                               '    elif not blocked:\n'
                               '        comparison = replace_word(comparison, low16(comparison) & 3072)\n'
                               'rendered = render_duel_actor(state, actor, opponent, DuelActorFrame(command, '
                               'comparison, damage, factor, flip_value, variation), stack)\n'
                               'result = rendered.frame\n'
                               'return DuelActorResult(result.command, result.comparison, result.distance, '
                               'result, rendered.actor, rendered.opponent, rendered.stack).validate()'},
 '_apply_duel_strike': {'signature': 'state, actor, opponent, frame, stack',
                        'returns': None,
                        'flow': '_push_actor_pair_words(stack, frame.command, frame.comparison)\n'
                                '_sound(state, 167)\n'
                                'opponent.set_word(38, 60)\n'
                                'rolled = low16(_random(state)) & 7\n'
                                'if rolled >= 6:\n'
                                '    rolled = u16(rolled - 4)\n'
                                'attribute = actor.word(30)\n'
                                'offset = scan_duel_thresholds(state, attribute, '
                                'state.table(167218).cursor())\n'
                                'damage = u16(rolled + state.table(167230).word(offset))\n'
                                'strength = actor.word(30)\n'
                                'weapon = actor.word(12)\n'
                                'if weapon == 0:\n'
                                '    equipment_index = u16(actor.word(44) << 1)\n'
                                '    strength = u16(strength + state.table(167242).word(equipment_index))\n'
                                'elif weapon <= 1:\n'
                                '    equipment_index = u16(actor.word(42) << 1)\n'
                                '    strength = u16(strength + state.table(167250).word(equipment_index))\n'
                                'else:\n'
                                '    equipment_index = u16(actor.word(46) << 1)\n'
                                '    strength = u16(strength + state.table(167258).word(equipment_index))\n'
                                'product = u32(damage * strength)\n'
                                'kind = u16((actor.word(2) & 3) << 1)\n'
                                'divisor = state.table(167278).word(kind)\n'
                                'damage = divu_retained(product, divisor)\n'
                                'command, comparison = _pop_actor_pair_words(stack, frame.command, '
                                'frame.comparison)\n'
                                'if actor.word(28) != 0:\n'
                                '    remaining = u16(opponent.word(28) - low16(damage))\n'
                                '    opponent.set_word(28, remaining)\n'
                                '    if negative_word(remaining):\n'
                                '        opponent.set_word(28, 0)\n'
                                'return DuelActorFrame(command, comparison, _actor_word(frame.distance, '
                                'kind), frame.factor, frame.weapon_difference, damage).validate()'},
 'render_duel_actor': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: DuelActorFrame '
                                    '| None=None, stack: Cursor | None=None',
                       'returns': 'DuelRenderResult',
                       'flow': 'actor = _live_table(state, actor)\n'
                               'opponent = _live_table(state, opponent)\n'
                               'current = DuelActorFrame() if frame is None else frame\n'
                               'stack = _actor_stack(state, current, stack)\n'
                               'if actor.byte(2) & 8:\n'
                               '    return DuelRenderResult(current, actor, opponent, '
                               'stack).validate(state)\n'
                               'if actor.word(28) == 0:\n'
                               '    _push_actor_longs(stack, (current.command, current.comparison, '
                               'current.distance, current.factor, actor.base, opponent.base))\n'
                               '    mode = actor.word(12)\n'
                               '    pattern = state.table(167820).byte(mode)\n'
                               '    attributes = actor.word(24)\n'
                               "    y = u16(actor.word(14) - state.scalar('ram_7006_word'))\n"
                               '    x = 84 if actor.byte(2) & 16 else 88\n'
                               '    pose = DuelActorFrame(_actor_word(current.command, x), '
                               '_actor_word(current.comparison, y), _actor_word(current.distance, pattern), '
                               '_actor_word(current.factor, attributes), current.weapon_difference, '
                               'current.variation)\n'
                               '    drawn = append_duel_sprite(state, x, y, pattern, attributes, pose, '
                               'stack)\n'
                               '    saved = (current.command, current.comparison, current.distance, '
                               'current.factor, actor.base, opponent.base)\n'
                               '    if stack is not None:\n'
                               '        saved = _pop_actor_longs(stack, 6)\n'
                               '    actor, opponent = (state.table(saved[4]), state.table(saved[5]))\n'
                               '    current = DuelActorFrame(saved[0], saved[1], saved[2], saved[3], '
                               'drawn.frame.weapon_difference, drawn.frame.variation)\n'
                               'else:\n'
                               '    mode_product = u32(actor.word(12) * 18)\n'
                               '    mode_offset = low16(mode_product)\n'
                               '    variation = mode_product\n'
                               '    direction_product = u32(actor.byte(3) * 6)\n'
                               '    pose = u16(direction_product + mode_offset)\n'
                               '    distance_value = replace_word(direction_product, pose)\n'
                               '    animation = actor.word(4)\n'
                               '    if actor.byte(2) & 64:\n'
                               '        animation = 5\n'
                               '    variation = replace_word(variation, animation)\n'
                               '    pose = u16(pose + animation)\n'
                               '    distance_value = replace_word(distance_value, pose)\n'
                               '    x = 84 if actor.byte(2) & 16 else 88\n'
                               "    y = u16(actor.word(14) - state.scalar('ram_7006_word'))\n"
                               '    attributes = actor.word(24)\n'
                               '    pose_frame = DuelActorFrame(_actor_word(current.command, x), '
                               '_actor_word(current.comparison, y), distance_value, '
                               '_actor_word(current.factor, attributes), current.weapon_difference, '
                               'variation)\n'
                               '    _push_actor_longs(stack, (actor.base, opponent.base))\n'
                               '    drawn = append_duel_sprite(state, x, y, pose, attributes, pose_frame, '
                               'stack)\n'
                               '    if stack is not None:\n'
                               '        actor_base, opponent_base = _pop_actor_longs(stack, 2)\n'
                               '        actor, opponent = (state.table(actor_base), '
                               'state.table(opponent_base))\n'
                               '    current = drawn.frame\n'
                               'return _render_duel_movement_overlay(state, actor, opponent, current, '
                               'stack)'},
 '_render_duel_movement_overlay': {'signature': 'state, actor, opponent, frame, stack',
                                   'returns': None,
                                   'flow': 'if not actor.byte(2) & 32:\n'
                                           '    return DuelRenderResult(frame, actor, opponent, '
                                           'stack).validate(state)\n'
                                           'command, comparison = (frame.command, frame.comparison)\n'
                                           'if actor.word(10) == 0:\n'
                                           '    actor.set_word(10, 10)\n'
                                           '    animation = u16(actor.word(6) + 1)\n'
                                           '    if animation >= 5:\n'
                                           '        animation = 1\n'
                                           '        movement_bits = actor.word() & 3072\n'
                                           '        comparison = _actor_word(comparison, movement_bits)\n'
                                           '        if movement_bits == 0:\n'
                                           '            actor.set_byte(2, actor.byte(2) & 223)\n'
                                           '            animation = 0\n'
                                           '    actor.set_word(6, animation)\n'
                                           '    command = _actor_word(command, animation)\n'
                                           "y = u16(actor.word(14) - state.scalar('ram_7006_word'))\n"
                                           'pattern = 62 if actor.word(12) == 0 else 54\n'
                                           'pattern = u16(pattern + actor.word(6))\n'
                                           'if actor.byte(2) & 16:\n'
                                           "    pattern = u16((state.scalar('ram_7008_word') >> 4 & 1) + "
                                           '60)\n'
                                           'attributes = actor.word(24)\n'
                                           'overlay = DuelActorFrame(_actor_word(command, 88), '
                                           '_actor_word(comparison, y), _actor_word(frame.distance, '
                                           'pattern), _actor_word(frame.factor, attributes), '
                                           'frame.weapon_difference, frame.variation)\n'
                                           '_push_actor_longs(stack, (actor.base,))\n'
                                           'drawn = append_duel_sprite(state, 88, y, pattern, attributes, '
                                           'overlay, stack)\n'
                                           'if stack is not None:\n'
                                           '    actor = state.table(_pop_actor_longs(stack, 1)[0])\n'
                                           'return DuelRenderResult(drawn.frame, actor, drawn.source, '
                                           'stack).validate(state)'},
 'run_duel_scene': {'signature': 'state: SceneState, context: DuelSceneContext=DuelSceneContext()',
                    'returns': 'DuelSceneResult',
                    'flow': 'context.validate()\n'
                            'first, second = _initialize_duel_scene(state, context)\n'
                            'controls = _choose_duel_side_loadout(state, False, context.controls)\n'
                            'controls = _choose_duel_side_loadout(state, True, controls)\n'
                            'selection = low16(_random(state)) & 3\n'
                            'if selection == 3:\n'
                            '    selection = 0\n'
                            'choose_duel_status_text(state, selection)\n'
                            '_sound(state, 165)\n'
                            'controls = _wait_duel_status_text(state, False, controls)\n'
                            'state.set_status_word(9984)\n'
                            'clear_duel_text_plane(state)\n'
                            'selection = low16(_random(state)) & 3\n'
                            'if selection == 3:\n'
                            '    selection = 0\n'
                            'selection = u16(selection + 3)\n'
                            'choose_duel_status_text(state, selection)\n'
                            '_sound(state, 165)\n'
                            'controls = _wait_duel_status_text(state, True, controls)\n'
                            '_sound(state, 139)\n'
                            'actor_values = context.actor_values\n'
                            'retained = None\n'
                            'while True:\n'
                            '    state.set_status_word(9984)\n'
                            '    clear_duel_text_plane(state)\n'
                            '    while True:\n'
                            '        _duel_frame(state)\n'
                            '        controls = _first_controls(state, controls)\n'
                            '        first.set_word(0, low16(controls.command))\n'
                            "        if state.scalar('ram_700a_byte') == 3:\n"
                            '            if retained is None:\n'
                            "                raise Boundary('full scene loop lacks current retained values "
                            "after unprojected callees')\n"
                            '            ai = choose_duel_ai_command(state, first, second, '
                            'DuelAIContext(controls.command, controls.mode, 0, 0, retained))\n'
                            '            controls = DuelControlContext(ai.command, ai.comparison)\n'
                            '            retained = ai.retained\n'
                            '            first.set_word(0, low16(controls.command))\n'
                            '        first_result = update_duel_actor(state, first, second, '
                            'DuelActorContext(controls.command, controls.mode, actor_values.damage, '
                            'retained, context.stack))\n'
                            '        retained = first_result.retained\n'
                            '        controls = _second_controls(state, '
                            'DuelControlContext(first_result.command, first_result.comparison))\n'
                            '        second.set_word(0, low16(controls.command))\n'
                            "        if state.scalar('ram_700b_byte') == 3:\n"
                            '            if retained is None:\n'
                            "                raise Boundary('full scene loop lacks current retained values "
                            "after unprojected callees')\n"
                            '            ai = choose_duel_ai_command(state, second, first, '
                            'DuelAIContext(controls.command, controls.mode, 0, 0, retained))\n'
                            '            controls = DuelControlContext(ai.command, ai.comparison)\n'
                            '            retained = ai.retained\n'
                            '            second.set_word(0, low16(controls.command))\n'
                            '        second_result = update_duel_actor(state, second, first, '
                            'DuelActorContext(controls.command, controls.mode, first_result.damage, '
                            'retained, context.stack))\n'
                            '        retained = second_result.retained\n'
                            '        controls = DuelControlContext(second_result.command, '
                            'second_result.comparison)\n'
                            '        actor_values = DuelActorContext(second_result.command, '
                            'second_result.comparison, second_result.damage)\n'
                            '        show_active_duel_turn_label(state)\n'
                            "        state.set_scalar('ram_7018_word', 0)\n"
                            '        if state.table(16740432).word(28) == 0:\n'
                            '            controls = _show_duel_action_result(state, controls)\n'
                            '            return _finish_duel_scene(state, controls, actor_values)\n'
                            "        state.set_scalar('ram_7018_word', 32768)\n"
                            '        if state.table(16740512).word(28) == 0:\n'
                            '            controls = _show_duel_action_result(state, controls)\n'
                            '            return _finish_duel_scene(state, controls, actor_values)\n'
                            '        active_flags = state.table(16740432).word(2)\n'
                            '        active_flags |= state.table(16740512).word(2)\n'
                            '        if active_flags & 53248:\n'
                            '            continue\n'
                            "        state.set_scalar('ram_7018_word', 0)\n"
                            '        if state.table(16740432).word() & 64:\n'
                            '            break\n'
                            "        state.set_scalar('ram_7018_word', 32768)\n"
                            '        if state.table(16740512).word() & 64:\n'
                            '            break\n'
                            '    if retained is None:\n'
                            "        raise Boundary('full scene loop lacks current pending-action values "
                            "after unprojected callees')\n"
                            '    result = _choose_duel_command(state, controls, retained)\n'
                            '    controls, retained = (result.controls, result.retained)\n'
                            '    if result.discarded_continuation is not None:\n'
                            '        if result.discarded_continuation.return_carrier != 161138:\n'
                            "            raise Boundary('unknown discarded duel scene continuation')\n"
                            '        return _finish_duel_scene(state, controls, actor_values)'}}
DECLARATIONS.update(HOST_ACTOR_DECLARATIONS)
APPROVED['contexts_duel'].update({'DuelActorFrame', 'DuelRenderResult'})

# Complete supplied preparation bodies, finite host-ABI expansion only.
# Original instruction allocation is unchanged; no new native credit.
HOST_PREPARATION_DECLARATIONS = {'configure_duel_weapon_motion': {'signature': 'state: SceneState, actor: Table, frame: DuelActorFrame | '
                                               'None=None',
                                  'returns': 'DuelActorFrame | None',
                                  'flow': 'actor = _live_table(state, actor)\n'
                                          'if frame is not None:\n'
                                          '    if type(frame) is not DuelActorFrame:\n'
                                          "        raise ValueError('actual weapon configuration frame "
                                          "required')\n"
                                          '    frame.validate()\n'
                                          'attribute = actor.word(30)\n'
                                          'mode_offset = u16(actor.word(12) << 1)\n'
                                          'penalty = state.table(162430).word(mode_offset)\n'
                                          'difference = u16(attribute - penalty)\n'
                                          'if attribute < penalty:\n'
                                          '    difference = 0\n'
                                          'elif difference >= 80:\n'
                                          '    difference = 80\n'
                                          'delay = u16(80 - difference)\n'
                                          'command = u32(difference * 1792 + 24576)\n'
                                          'actor.set_long(18, command)\n'
                                          'comparison = divu_retained(delay, 2)\n'
                                          'actor.set_word(22, low16(comparison))\n'
                                          'if frame is not None:\n'
                                          '    return DuelActorFrame(command, comparison, frame.distance, '
                                          'frame.factor, frame.weapon_difference, '
                                          'frame.variation).validate()\n'
                                          'return None'},
 'clear_duel_text_plane': {'signature': 'state: SceneState, frame: DuelActorFrame | None=None',
                           'returns': 'DuelActorFrame | None',
                           'flow': 'if frame is not None:\n'
                                   '    if type(frame) is not DuelActorFrame:\n'
                                   "        raise ValueError('actual clear-text frame required')\n"
                                   '    frame.validate()\n'
                                   "state.set_scalar('ram_d100_word', 0)\n"
                                   'state.mmio_write(12582916, 4, 1174405123)\n'
                                   'for _ in range(640):\n'
                                   '    state.mmio_write(12582912, 4, 286331153)\n'
                                   'if frame is not None:\n'
                                   '    return DuelActorFrame(286331153, _actor_word(frame.comparison, '
                                   '65535), frame.distance, frame.factor, frame.weapon_difference, '
                                   'frame.variation).validate()\n'
                                   'return None'},
 '_choose_duel_ai_panel': {'signature': 'state, actor, opponent, controls, preparation=None',
                           'returns': None,
                           'flow': 'if type(preparation) is not DuelPreparationContext:\n'
                                   "    raise Boundary('automatic panel requires actual post-refresh six "
                                   "values, response and live stack')\n"
                                   'preparation.validate(state)\n'
                                   'if actor is not preparation.actor or opponent is not '
                                   'preparation.opponent:\n'
                                   "    raise ValueError('panel must consume the actual caller actor "
                                   "views')\n"
                                   'if type(controls) is not DuelControlContext:\n'
                                   "    raise ValueError('actual current panel controls required')\n"
                                   'controls.validate()\n'
                                   'if (controls.command, controls.mode) != (preparation.frame.command, '
                                   'preparation.frame.comparison):\n'
                                   "    raise ValueError('panel controls must agree with current frame')\n"
                                   'attribute = actor.word(30)\n'
                                   'threshold_offset = scan_duel_thresholds(state, attribute, '
                                   'state.table(162710).cursor())\n'
                                   'pointer_offset = u16(threshold_offset << 1)\n'
                                   'handler = state.table(162722).long(pointer_offset)\n'
                                   'frame = preparation.frame\n'
                                   'current = DuelActorFrame(replace_word(frame.command, attribute), '
                                   'replace_word(frame.comparison, pointer_offset), frame.distance, '
                                   'frame.factor, frame.weapon_difference, frame.variation)\n'
                                   'result = state.service_at(handler, DuelPreparationContext(current, '
                                   'preparation.response, actor, opponent, preparation.stack))\n'
                                   'if type(result) is not DuelPreparationContext:\n'
                                   "    raise Boundary('live duel panel handler must return its typed "
                                   "completion')\n"
                                   'result.validate(state)\n'
                                   'return result'},
 '_choose_duel_side_loadout': {'signature': 'state, second, controls',
                               'returns': None,
                               'flow': 'actor = state.table(16740512 if second else 16740432)\n'
                                       'opponent = state.table(16740432 if second else 16740512)\n'
                                       "mode_name = 'ram_700b_byte' if second else 'ram_700a_byte'\n"
                                       'choice = state.table(16740524 if second else 16740444)\n'
                                       'equipment_choice = state.table(16740578 if second else 16740498)\n'
                                       'if state.scalar(mode_name) != 3:\n'
                                       '    _configure_duel_dialog(state, 50688, 166078)\n'
                                       '    if second:\n'
                                       "        state.set_scalar('ram_70da_word', 1)\n"
                                       '    advance_duel_entry_palette(state)\n'
                                       'while True:\n'
                                       '    _duel_frame(state)\n'
                                       '    advance_duel_entry_palette(state)\n'
                                       '    refresh_duel_actors(state)\n'
                                       '    if not second:\n'
                                       "        state.set_scalar('ram_708a_word', 0)\n"
                                       '    if state.scalar(mode_name) == 3:\n'
                                       "        raise Boundary('effects-only loadout cannot supply current "
                                       "panel values; use complete preparation continuation')\n"
                                       '    controls = _second_controls(state, controls) if second else '
                                       '_first_controls(state, controls)\n'
                                       '    controls = choose_second_duel_equipment(state, choice, controls) '
                                       'if second else choose_first_duel_equipment(state, choice, controls)\n'
                                       "    if state.scalar('ram_700c_word') != 0:\n"
                                       '        continue\n'
                                       '    _stage_duel_words(state, 164354 if second else 164332, '
                                       '1610612740, 1, 60740 if second else 60680)\n'
                                       '    controls = _second_controls(state, controls) if second else '
                                       '_first_controls(state, controls)\n'
                                       '    controls = DuelControlContext(replace_word(controls.command, '
                                       'low16(controls.command) & 240), controls.mode)\n'
                                       '    if low16(controls.command) == 0:\n'
                                       '        continue\n'
                                       '    _sound(state, 172)\n'
                                       '    if state.scalar(mode_name) == 3:\n'
                                       '        break\n'
                                       '    clear_duel_text_plane(state)\n'
                                       '    _configure_duel_dialog(state, 50688, 166154)\n'
                                       '    while True:\n'
                                       '        _duel_frame(state)\n'
                                       '        advance_duel_entry_palette(state)\n'
                                       '        refresh_duel_actors(state)\n'
                                       '        controls = _second_controls(state, controls) if second else '
                                       '_first_controls(state, controls)\n'
                                       '        controls = choose_duel_two_option_menu(state, '
                                       'equipment_choice, controls)\n'
                                       "        if state.scalar('ram_700c_word') != 0:\n"
                                       '            continue\n'
                                       '        controls = _second_controls(state, controls) if second else '
                                       '_first_controls(state, controls)\n'
                                       '        controls = DuelControlContext(replace_word(controls.command, '
                                       'low16(controls.command) & 240), controls.mode)\n'
                                       '        if low16(controls.command) != 0:\n'
                                       '            break\n'
                                       '    _sound(state, 172)\n'
                                       '    if equipment_choice.word() != 0:\n'
                                       '        state.set_scalar(mode_name, 3)\n'
                                       '    break\n'
                                       'state.set_status_word(9984)\n'
                                       'configure_duel_weapon_motion(state, actor)\n'
                                       'clear_duel_text_plane(state)\n'
                                       'return controls'},
 '_wait_duel_status_text': {'signature': 'state, second, controls, preparation=None',
                            'returns': None,
                            'flow': 'if preparation is not None:\n'
                                    '    if not second:\n'
                                    "        raise Boundary('first status palette return is not yet a "
                                    "complete preparation ABI')\n"
                                    '    return _wait_complete_second_status(state, preparation)\n'
                                    'if not second:\n'
                                    '    state.table(16740432).set_word(2, 0)\n'
                                    'else:\n'
                                    '    state.table(16740512).set_word(2, 0)\n'
                                    'while True:\n'
                                    '    _duel_frame(state)\n'
                                    '    if not second:\n'
                                    '        advance_duel_entry_palette(state)\n'
                                    '    refresh_duel_actors(state)\n'
                                    "    if state.scalar('ram_700c_word') != 0:\n"
                                    '        continue\n'
                                    '    controls = _second_controls(state, controls) if second else '
                                    '_first_controls(state, controls)\n'
                                    '    controls = DuelControlContext(replace_word(controls.command, '
                                    'low16(controls.command) & 240), controls.mode)\n'
                                    '    if low16(controls.command) != 0:\n'
                                    '        return controls'},
 '_preparation_with_frame': {'signature': 'state, preparation, frame, actor=None, opponent=None, stack=None',
                             'returns': None,
                             'flow': 'preparation.validate(state)\n'
                                     'return DuelPreparationContext(frame, preparation.response, '
                                     'preparation.actor if actor is None else actor, preparation.opponent if '
                                     'opponent is None else opponent, preparation.stack if stack is None '
                                     'else stack).validate(state)'},
 '_wait_complete_second_status': {'signature': 'state, preparation',
                                  'returns': None,
                                  'flow': 'preparation.validate(state)\n'
                                          'state.table(16740512).set_word(2, 0)\n'
                                          'current = preparation\n'
                                          'while True:\n'
                                          '    _duel_frame(state)\n'
                                          '    rendered = refresh_duel_actors(state, current.frame, '
                                          'current.stack, current.actor, current.opponent)\n'
                                          '    current = _preparation_with_frame(state, current, '
                                          'rendered.frame, rendered.actor, rendered.opponent, '
                                          'rendered.stack)\n'
                                          "    if state.scalar('ram_700c_word') != 0:\n"
                                          '        continue\n'
                                          '    controls = _second_controls(state, '
                                          'DuelControlContext(current.frame.command, '
                                          'current.frame.comparison))\n'
                                          '    command = replace_word(controls.command, '
                                          'low16(controls.command) & 240)\n'
                                          '    frame = DuelActorFrame(command, controls.mode, '
                                          'current.frame.distance, current.frame.factor, '
                                          'current.frame.weapon_difference, current.frame.variation)\n'
                                          '    current = _preparation_with_frame(state, current, frame)\n'
                                          '    if low16(command) != 0:\n'
                                          '        return current'},
 '_commit_complete_duel_loadout': {'signature': 'state, preparation, second',
                                   'returns': None,
                                   'flow': 'preparation.validate(state)\n'
                                           'if type(second) is not bool:\n'
                                           "    raise ValueError('actual selected loadout side required')\n"
                                           'state.set_status_word(9984)\n'
                                           'actor = state.table(16740512 if second else 16740432)\n'
                                           'frame = configure_duel_weapon_motion(state, actor, '
                                           'preparation.frame)\n'
                                           'frame = clear_duel_text_plane(state, frame)\n'
                                           'return _preparation_with_frame(state, preparation, frame, '
                                           'actor=actor)'},
 '_prepare_complete_second_status': {'signature': 'state, preparation',
                                     'returns': None,
                                     'flow': 'from .business_reuse import _reuse_advance_random_pair\n'
                                             'preparation.validate(state)\n'
                                             'random = _reuse_advance_random_pair(state)\n'
                                             'selection = low16(random.sample) & 3\n'
                                             'if selection == 3:\n'
                                             '    selection = 0\n'
                                             'selection = u16(selection + 3)\n'
                                             'command = choose_duel_status_text(state, selection, '
                                             'random.sample)\n'
                                             'frame = preparation.frame\n'
                                             'frame = DuelActorFrame(replace_word(command, 165), '
                                             'random.updated_state, frame.distance, frame.factor, '
                                             'frame.weapon_difference, frame.variation)\n'
                                             '_sound(state, 165)\n'
                                             'current = _preparation_with_frame(state, preparation, frame)\n'
                                             'current = _wait_duel_status_text(state, True, '
                                             'DuelControlContext(frame.command, frame.comparison), current)\n'
                                             'frame = current.frame\n'
                                             'frame = DuelActorFrame(replace_word(frame.command, 139), '
                                             'frame.comparison, frame.distance, frame.factor, '
                                             'frame.weapon_difference, frame.variation)\n'
                                             '_sound(state, 139)\n'
                                             'return _preparation_with_frame(state, current, frame)'},
 '_consume_complete_first_duel_frame': {'signature': 'state, preparation',
                                        'returns': None,
                                        'flow': 'preparation.validate(state)\n'
                                                'state.set_status_word(9984)\n'
                                                'frame = clear_duel_text_plane(state, preparation.frame)\n'
                                                '_duel_frame(state)\n'
                                                'controls = _first_controls(state, '
                                                'DuelControlContext(frame.command, frame.comparison))\n'
                                                'first, second = (state.table(16740432), '
                                                'state.table(16740512))\n'
                                                'first.set_word(0, low16(controls.command))\n'
                                                "if state.scalar('ram_700a_byte') == 3:\n"
                                                "    raise Boundary('first automatic combat frame needs its "
                                                "actual current AI threshold/override ABI')\n"
                                                'actual = DuelActorContext(controls.command, controls.mode, '
                                                'frame.distance, frame.retained, preparation.stack)\n'
                                                'return update_duel_actor(state, first, second, actual)'},
 'continue_automatic_duel_preparation': {'signature': 'state: SceneState, preparation: '
                                                      'DuelPreparationContext',
                                         'returns': 'DuelPreparationResult',
                                         'flow': 'if type(preparation) is not DuelPreparationContext:\n'
                                                 "    raise ValueError('actual complete preparation caller "
                                                 "required')\n"
                                                 'preparation.validate(state)\n'
                                                 'current = _choose_duel_ai_panel(state, preparation.actor, '
                                                 'preparation.opponent, '
                                                 'DuelControlContext(preparation.frame.command, '
                                                 'preparation.frame.comparison), preparation)\n'
                                                 'first_side = current.actor.base == 16740432\n'
                                                 'if low16(current.response) == 0 and first_side:\n'
                                                 "    return DuelPreparationResult('repeat_first', "
                                                 'current).validate(state)\n'
                                                 'current = _commit_complete_duel_loadout(state, current, '
                                                 'not first_side)\n'
                                                 'if first_side:\n'
                                                 "    return DuelPreparationResult('needs_second_loadout', "
                                                 'current).validate(state)\n'
                                                 'current = _prepare_complete_second_status(state, current)\n'
                                                 'actual = _consume_complete_first_duel_frame(state, '
                                                 'current)\n'
                                                 "return DuelPreparationResult('first_frame', None, "
                                                 'actual).validate(state)'}}
DECLARATIONS.update(HOST_PREPARATION_DECLARATIONS)
APPROVED['contexts_duel'].update({'DuelPreparationContext', 'DuelPreparationResult'})
APPROVED['business_reuse'].add('_reuse_advance_random_pair')

# Complete supplied current-AI bodies; finite host ABI admission, not generic Python lowering.
# Four original components864B keep their existing native instruction allocation.
HOST_CURRENT_AI_DECLARATIONS = {'_ai_frame': {'signature': 'frame, command=None, comparison=None, distance=None, factor=None, '
                            'variation=None',
               'returns': None,
               'flow': 'return DuelActorFrame(frame.command if command is None else command, '
                       'frame.comparison if comparison is None else comparison, frame.distance if distance '
                       'is None else distance, frame.factor if factor is None else factor, '
                       'frame.weapon_difference, frame.variation if variation is None else '
                       'variation).validate()'},
 '_ai_random': {'signature': 'state, frame, mask',
                'returns': None,
                'flow': 'from .business_reuse import _reuse_advance_random_pair\n'
                        'random = _reuse_advance_random_pair(state)\n'
                        'return _ai_frame(frame, command=replace_word(random.sample, low16(random.sample) & '
                        'mask), comparison=random.updated_state)'},
 '_ai_override_result': {'signature': 'frame, override',
                         'returns': None,
                         'flow': 'return DuelOverrideResult(_ai_frame(frame, '
                                 'variation=_actor_word(frame.variation, override)), override).validate()'},
 'sample_duel_probability': {'signature': 'state: SceneState, source_word: Word, frame: DuelActorFrame | '
                                          'None=None',
                             'returns': 'DuelProbability',
                             'flow': "source_word = uint(source_word, 16, 'probability word')\n"
                                     'current = DuelActorFrame() if frame is None else frame\n'
                                     'if type(current) is not DuelActorFrame:\n'
                                     "    raise ValueError('actual probability frame required')\n"
                                     'current.validate()\n'
                                     'mask = source_word & 7\n'
                                     'threshold = source_word >> 4\n'
                                     'current = _ai_frame(current, distance=_actor_word(current.distance, '
                                     'mask), factor=_actor_word(current.factor, threshold))\n'
                                     'current = _ai_random(state, current, mask)\n'
                                     'return DuelProbability(current.command, mask, threshold, '
                                     'low16(current.command) < threshold, current)'},
 'choose_duel_ai_timeout': {'signature': 'state: SceneState, actor: Table, opponent: Table, command: Long, '
                                         'override: Word, frame: DuelActorFrame | None=None',
                            'returns': 'DuelAIResult',
                            'flow': 'actor = _live_table(state, actor)\n'
                                    'opponent = _live_table(state, opponent)\n'
                                    "command = uint(command, 32, 'command')\n"
                                    "override = uint(override, 16, 'override')\n"
                                    'current = DuelActorFrame(command) if frame is None else frame\n'
                                    'if type(current) is not DuelActorFrame:\n'
                                    "    raise ValueError('actual timeout frame required')\n"
                                    'current.validate()\n'
                                    'if current.command != command:\n'
                                    "    raise ValueError('timeout command must be the current frame "
                                    "command')\n"
                                    "if state.scalar('ram_70fa_word') > 6144:\n"
                                    "    if state.scalar('ram_700a_word') == 771:\n"
                                    '        readiness = actor.word(28)\n'
                                    '        current = _ai_frame(current, command=replace_word(command, '
                                    'readiness))\n'
                                    '        if readiness <= opponent.word(28):\n'
                                    '            override = 67\n'
                                    '            current = _ai_frame(current, '
                                    'variation=_actor_word(current.variation, override))\n'
                                    '            return DuelAIResult(current.command, current.comparison if '
                                    'current.comparison is not None else 0, 0, override, current.retained, '
                                    'current if frame is not None else None)\n'
                                    'current = _ai_frame(current, command=0)\n'
                                    'return DuelAIResult(0, current.comparison if current.comparison is not '
                                    'None else 0, 0, override, current.retained, current if frame is not '
                                    'None else None)'},
 'choose_duel_ai_override': {'signature': 'state: SceneState, actor: Table, opponent: Table, '
                                          'threshold_offset: Word, frame: DuelActorFrame | None=None',
                             'returns': 'Word | DuelOverrideResult',
                             'flow': 'current = DuelActorFrame() if frame is None else frame\n'
                                     'result = _choose_duel_ai_override_current(state, actor, opponent, '
                                     'threshold_offset, current)\n'
                                     'return result.override if frame is None else result'},
 '_choose_duel_ai_override_current': {'signature': 'state, actor, opponent, threshold_offset, frame',
                                      'returns': None,
                                      'flow': 'actor = _live_table(state, actor)\n'
                                              'opponent = _live_table(state, opponent)\n'
                                              "threshold_offset = uint(threshold_offset, 16, 'threshold "
                                              "offset')\n"
                                              'if type(frame) is not DuelActorFrame:\n'
                                              "    raise ValueError('actual override frame required')\n"
                                              'frame.validate()\n'
                                              "tick = state.scalar('ram_7008_word') & 7\n"
                                              'current = _ai_frame(frame, '
                                              'comparison=_actor_word(frame.comparison, tick), '
                                              'variation=_actor_word(frame.variation, 0))\n'
                                              'if tick:\n'
                                              '    return _ai_override_result(current, 0)\n'
                                              'if actor.base == 16740432:\n'
                                              '    opponent_readiness = opponent.word(28)\n'
                                              '    if opponent_readiness < 51:\n'
                                              '        current = _ai_random(state, current, 1)\n'
                                              '        if low16(current.command) == 0:\n'
                                              '            return _ai_override_result(current, 64)\n'
                                              '    else:\n'
                                              '        current = _ai_random(state, current, 3)\n'
                                              '        return _ai_override_result(current, 64 if '
                                              'low16(current.command) == 0 else 0)\n'
                                              '    opponent_strength = opponent.word(30)\n'
                                              '    current = _ai_frame(current, '
                                              'distance=_actor_word(current.distance, opponent_strength))\n'
                                              '    own_strength = actor.word(30)\n'
                                              '    current = _ai_frame(current, '
                                              'factor=_actor_word(current.factor, own_strength))\n'
                                              '    readiness = actor.word(28)\n'
                                              '    current = _ai_frame(current, '
                                              'comparison=_actor_word(current.comparison, readiness))\n'
                                              '    if readiness < 40:\n'
                                              '        current = _ai_random(state, current, 3)\n'
                                              '        return _ai_override_result(current, 67 if '
                                              'low16(current.command) else 0)\n'
                                              '    if readiness >= 70:\n'
                                              '        if opponent_strength >= own_strength:\n'
                                              '            current = _ai_random(state, current, 1)\n'
                                              '            return _ai_override_result(current, 67 if '
                                              'low16(current.command) else 0)\n'
                                              '        current = _ai_random(state, current, 3)\n'
                                              '        return _ai_override_result(current, 67 if '
                                              'low16(current.command) == 0 else 0)\n'
                                              '    if opponent_strength < own_strength:\n'
                                              '        current = _ai_random(state, current, 1)\n'
                                              '    else:\n'
                                              '        current = _ai_random(state, current, 3)\n'
                                              '    return _ai_override_result(current, 67 if '
                                              'low16(current.command) else 0)\n'
                                              'opponent_readiness = opponent.word(28)\n'
                                              'current = _ai_frame(current, '
                                              'distance=_actor_word(current.distance, opponent_readiness))\n'
                                              'readiness = actor.word(28)\n'
                                              'current = _ai_frame(current, '
                                              'factor=_actor_word(current.factor, readiness))\n'
                                              'if opponent_readiness < readiness:\n'
                                              '    sampled = sample_duel_probability(state, '
                                              'state.table(174562).word(threshold_offset), current)\n'
                                              '    current = sampled.frame\n'
                                              '    if sampled.borrowed:\n'
                                              '        return _ai_override_result(current, 64)\n'
                                              '    sampled = sample_duel_probability(state, '
                                              'state.table(174574).word(threshold_offset), current)\n'
                                              '    return _ai_override_result(sampled.frame, 33 if '
                                              'sampled.borrowed else 0)\n'
                                              'if readiness >= 80:\n'
                                              '    return _ai_override_result(current, 0)\n'
                                              'if readiness >= 50:\n'
                                              '    opponent_strength = opponent.word(30)\n'
                                              '    current = _ai_frame(current, '
                                              'distance=_actor_word(current.distance, opponent_strength))\n'
                                              '    own_strength = actor.word(30)\n'
                                              '    current = _ai_frame(current, '
                                              'factor=_actor_word(current.factor, own_strength))\n'
                                              '    first_source = 173748 if opponent_strength >= '
                                              'own_strength else 173810\n'
                                              '    sampled = sample_duel_probability(state, '
                                              'state.table(first_source).word(threshold_offset), current)\n'
                                              '    current = sampled.frame\n'
                                              '    if sampled.borrowed:\n'
                                              '        return _ai_override_result(current, 67)\n'
                                              '    sampled = sample_duel_probability(state, '
                                              'state.table(173760).word(threshold_offset), current)\n'
                                              '    return _ai_override_result(sampled.frame, 64 if '
                                              'sampled.borrowed else 0)\n'
                                              'opponent_strength = opponent.word(30)\n'
                                              'current = _ai_frame(current, '
                                              'command=_actor_word(current.command, opponent_strength))\n'
                                              'opponent_offset = scan_duel_thresholds(state, '
                                              'opponent_strength, state.table(172808).cursor())\n'
                                              'current = _ai_frame(current, '
                                              'comparison=_actor_word(current.comparison, opponent_offset))\n'
                                              'if opponent_offset < 4:\n'
                                              '    source = 174370\n'
                                              'elif opponent_offset < 8:\n'
                                              '    source = 174204\n'
                                              'elif opponent_offset == 8:\n'
                                              '    source = 174040\n'
                                              'else:\n'
                                              '    source = 173868\n'
                                              'sampled = _sample_duel_live_mode_values(state, source, '
                                              'threshold_offset, False, current)\n'
                                              'current = sampled.frame\n'
                                              'if sampled.borrowed:\n'
                                              '    return _ai_override_result(current, 67)\n'
                                              'sampled = _sample_duel_live_mode_values(state, source, '
                                              'threshold_offset, True, current)\n'
                                              'return _ai_override_result(sampled.frame, 66 if '
                                              'sampled.borrowed else 0)'},
 '_sample_duel_live_mode_pair': {'signature': 'state, source, threshold_offset, second',
                                 'returns': None,
                                 'flow': 'return _sample_duel_live_mode_values(state, source, '
                                         'threshold_offset, second, DuelActorFrame()).borrowed'},
 '_sample_duel_live_mode_values': {'signature': 'state, source, threshold_offset, second, frame',
                                   'returns': None,
                                   'flow': 'if source == 174040:\n'
                                           '    base = 174132\n'
                                           'elif source == 174204:\n'
                                           '    base = 174298\n'
                                           'elif source == 174370:\n'
                                           '    base = 174464\n'
                                           'else:\n'
                                           '    base = 173962\n'
                                           "if state.scalar('ram_efd2_word') == 0:\n"
                                           '    offset = 0\n'
                                           'else:\n'
                                           "    offset = 48 if state.scalar('ram_efd2_word') == 2 else 24\n"
                                           'if second:\n'
                                           '    offset += 12\n'
                                           'source_word = state.table(u32(base + offset)).word(threshold_offset)\n'
                                           'return sample_duel_probability(state, source_word, frame)'},
 '_ai_observed_result': {'signature': 'frame, response, threshold_offset, override',
                         'returns': None,
                         'flow': 'actual_override = low16(frame.variation) if frame.variation is not None '
                                 'else override\n'
                                 'return DuelAIResult(frame.command, frame.comparison, threshold_offset, '
                                 'actual_override, frame.retained, frame, response).validate()'},
 '_ai_rule_frame': {'signature': 'state, actor, opponent, frame, threshold_offset, target_address',
                    'returns': None,
                    'flow': 'if frame.retained is None:\n'
                            "    raise Boundary('actual AI rule needs current six values, not a legacy WORD "
                            "observation')\n"
                            'result = state.service_at(target_address, DuelActionContext(actor, opponent, '
                            'DuelControlContext(frame.command, frame.comparison), threshold_offset, '
                            'frame.retained))\n'
                            'if type(result) is not DuelActionResult:\n'
                            "    raise Boundary('real AI rule must return the actual typed frame')\n"
                            'result.validate()\n'
                            'if result.discarded_continuation is not None:\n'
                            "    raise Boundary('ordinary AI rule returned an unexpected nonlocal "
                            "continuation')\n"
                            'if result.retained is None:\n'
                            "    raise Boundary('AI rule omitted its actual retained return')\n"
                            'return DuelActorFrame(result.controls.command, result.controls.mode, '
                            'result.retained.distance, result.retained.factor, '
                            'result.retained.weapon_difference, result.retained.variation).validate()'},
 'choose_duel_ai_command': {'signature': 'state: SceneState, actor: Table, opponent: Table, context: '
                                         'DuelAIContext=DuelAIContext()',
                            'returns': 'DuelAIResult',
                            'flow': 'actor = _live_table(state, actor)\n'
                                    'opponent = _live_table(state, opponent)\n'
                                    'if type(context) is not DuelAIContext:\n'
                                    "    raise ValueError('actual typed AI caller context required')\n"
                                    'context.validate()\n'
                                    'command = context.command\n'
                                    'comparison = context.comparison\n'
                                    'threshold_offset = context.threshold_offset\n'
                                    'override = context.override\n'
                                    'retained = context.retained\n'
                                    'frame = DuelActorFrame(command, comparison, retained.distance if '
                                    'retained is not None else None, retained.factor if retained is not None '
                                    'else None, retained.weapon_difference if retained is not None else '
                                    'None, retained.variation if retained is not None else None)\n'
                                    'response = context.response\n'
                                    'if actor.word(34) != 0:\n'
                                    '    actor.set_word(34, u16(actor.word(34) - 1))\n'
                                    'readiness = actor.word(28)\n'
                                    'command = replace_word(command, readiness)\n'
                                    'frame = _ai_frame(frame, command=command)\n'
                                    'if readiness == 0:\n'
                                    '    actor.set_word(2, 0)\n'
                                    '    actor.set_word(4, 0)\n'
                                    '    return _ai_observed_result(frame, response, threshold_offset, '
                                    'override)\n'
                                    'opponent_readiness = opponent.word(28)\n'
                                    'command = replace_word(command, opponent_readiness)\n'
                                    'frame = _ai_frame(frame, command=command)\n'
                                    'if opponent_readiness == 0:\n'
                                    '    frame = _ai_frame(frame, command=replace_word(command, 256))\n'
                                    '    return _ai_observed_result(frame, response, threshold_offset, '
                                    'override)\n'
                                    'if actor.word(34) == 0:\n'
                                    '    frame = _ai_random(state, frame, 31)\n'
                                    '    frame = _ai_frame(frame, command=replace_word(frame.command, '
                                    'u16(low16(frame.command) + 30)))\n'
                                    '    actor.set_word(34, low16(frame.command))\n'
                                    '    attribute = actor.word(30)\n'
                                    '    frame = _ai_frame(frame, command=replace_word(frame.command, '
                                    'attribute))\n'
                                    '    threshold_offset = scan_duel_thresholds(state, attribute, '
                                    'state.table(172808).cursor())\n'
                                    '    frame = _ai_frame(frame, comparison=replace_word(frame.comparison, '
                                    'threshold_offset))\n'
                                    '    response = _actor_word(response, threshold_offset)\n'
                                    '    selected = choose_duel_ai_override(state, actor, opponent, '
                                    'threshold_offset, frame)\n'
                                    '    frame, override = (selected.frame, selected.override)\n'
                                    '    timed = choose_duel_ai_timeout(state, actor, opponent, '
                                    'frame.command, override, frame)\n'
                                    '    frame, override = (timed.frame, timed.override)\n'
                                    '    frame = _ai_frame(frame, command=replace_word(frame.command, '
                                    'override))\n'
                                    '    if override != 0:\n'
                                    '        return _ai_observed_result(frame, response, threshold_offset, '
                                    'override)\n'
                                    '    dispatch_offset = u16(threshold_offset << 1)\n'
                                    '    frame = _ai_frame(frame, comparison=replace_word(frame.comparison, '
                                    'dispatch_offset))\n'
                                    '    dispatch_address = u32(172820 + s16(dispatch_offset))\n'
                                    '    frame = _ai_rule_frame(state, actor, opponent, frame, '
                                    'threshold_offset, dispatch_address)\n'
                                    'action = actor.word(36)\n'
                                    'action_offset = u16(action << 2)\n'
                                    'frame = _ai_frame(frame, command=replace_word(frame.command, '
                                    'action_offset))\n'
                                    'target_address = u32(172844 + s16(action_offset))\n'
                                    'frame = _ai_rule_frame(state, actor, opponent, frame, threshold_offset, '
                                    'target_address)\n'
                                    'return _ai_observed_result(frame, response, threshold_offset, '
                                    'override)'},
 '_consume_complete_first_duel_frame': {'signature': 'state, preparation',
                                        'returns': None,
                                        'flow': 'preparation.validate(state)\n'
                                                'state.set_status_word(9984)\n'
                                                'frame = clear_duel_text_plane(state, preparation.frame)\n'
                                                '_duel_frame(state)\n'
                                                'controls = _first_controls(state, '
                                                'DuelControlContext(frame.command, frame.comparison))\n'
                                                'first, second = (state.table(16740432), '
                                                'state.table(16740512))\n'
                                                'first.set_word(0, low16(controls.command))\n'
                                                "if state.scalar('ram_700a_byte') == 3:\n"
                                                '    actual_ai = DuelAIContext(controls.command, '
                                                'controls.mode, low16(preparation.response), '
                                                'low16(frame.variation), frame.retained, '
                                                'preparation.response)\n'
                                                '    ai = choose_duel_ai_command(state, first, second, '
                                                'actual_ai)\n'
                                                '    if ai.frame is None or not ai.frame.complete or '
                                                'ai.response is None:\n'
                                                "        raise Boundary('complete first automatic combat "
                                                "requires its actual AI return')\n"
                                                '    frame = ai.frame\n'
                                                '    controls = DuelControlContext(frame.command, '
                                                'frame.comparison)\n'
                                                '    first.set_word(0, low16(controls.command))\n'
                                                'actual = DuelActorContext(controls.command, controls.mode, '
                                                'frame.distance, frame.retained, preparation.stack)\n'
                                                'return update_duel_actor(state, first, second, actual)'}}
DECLARATIONS.update(HOST_CURRENT_AI_DECLARATIONS)
APPROVED['contexts_duel'].add('DuelOverrideResult')

# Complete supplied initialization contracts; finite host admission, not general Python lowering.
# Original physical emitters and default instruction topology remain unchanged.
DECLARATIONS.pop('_wait_complete_second_status')
HOST_INITIALIZATION_DECLARATIONS = {'advance_duel_entry_palette': {'signature': 'state: SceneState, preparation: DuelPreparationContext | '
                                             'None=None',
                                'returns': 'DuelPreparationContext | None',
                                'flow': 'from .business_scene import darken_palette\n'
                                        'if preparation is not None:\n'
                                        '    preparation.validate(state)\n'
                                        "if state.scalar('ram_70f8_word') >= 16:\n"
                                        '    return preparation\n'
                                        "intensity = u16(15 - state.scalar('ram_70f8_word'))\n"
                                        'if preparation is None:\n'
                                        '    darken_palette(state, intensity, 64, '
                                        'state.table(163968).cursor())\n'
                                        '    current = None\n'
                                        'else:\n'
                                        '    frame = preparation.frame\n'
                                        '    result = darken_palette(state, replace_word(frame.command, '
                                        'intensity), 64, state.table(163968).cursor(), '
                                        'frame.weapon_difference, '
                                        'count_carrier=replace_word(frame.comparison, 64), '
                                        'color=frame.distance, component=frame.factor)\n'
                                        '    current = _preparation_with_frame(state, preparation, '
                                        'DuelActorFrame(result.shade_carrier, result.count_carrier, '
                                        'result.color, result.component, result.accumulated, '
                                        'frame.variation), result.source, result.destination)\n'
                                        "state.set_scalar('ram_70f8_word', u16(state.scalar('ram_70f8_word') "
                                        '+ 1))\n'
                                        'return current'},
 'upload_duel_officer_name': {'signature': 'state: SceneState, officer: Word, colors: DuelGlyphContext, '
                                           'current: DuelInitializationResult | None=None',
                              'returns': 'DuelGlyphContext | DuelInitializationResult',
                              'flow': "officer = uint(officer, 16, 'officer')\n"
                                      'colors.validate()\n'
                                      'if current is not None:\n'
                                      '    current.validate(state)\n'
                                      '    frame = current.preparation.frame\n'
                                      '    if (colors.background, colors.foreground, colors.remaining) != '
                                      '(frame.command, frame.comparison, frame.factor):\n'
                                      "        raise ValueError('name colors must be the actual current "
                                      "values')\n"
                                      '    frame = DuelActorFrame(frame.command, frame.comparison, '
                                      'frame.distance, frame.factor, frame.weapon_difference, u32(officer * '
                                      '6))\n'
                                      '    current = _initialization_values(state, current, frame=frame)\n'
                                      'source = state.table(566532).cursor(u16(officer * 6))\n'
                                      'remaining = replace_word(colors.remaining, 2)\n'
                                      'if source.word(4) == 63:\n'
                                      '    remaining = replace_word(remaining, 1)\n'
                                      '    shade = u8(u16(low16(colors.background) << 4) | '
                                      'low16(colors.background))\n'
                                      '    first, second = (state.table(4294955776).cursor(), '
                                      'state.table(4294956096).cursor())\n'
                                      '    for _ in range(64):\n'
                                      '        first.append_byte(shade)\n'
                                      '        second.append_byte(shade)\n'
                                      '    if current is not None:\n'
                                      '        frame = current.preparation.frame\n'
                                      '        working = replace_word(frame.weapon_difference, '
                                      'u16(low16(frame.command) << 4 | low16(frame.command)))\n'
                                      '        current = _initialization_values(state, current, '
                                      'frame=DuelActorFrame(frame.command, frame.comparison, frame.distance, '
                                      'remaining, working, frame.variation), '
                                      'glyph_work=replace_word(current.glyph_work, 65535), '
                                      'glyph_source=second)\n'
                                      '    return _expand_and_upload_duel_glyphs(state, source, first, '
                                      'DuelGlyphContext(colors.background, colors.foreground, remaining), '
                                      'current)\n'
                                      'return upload_duel_glyph_strip(state, source, '
                                      'DuelGlyphContext(colors.background, colors.foreground, remaining), '
                                      'current)'},
 'upload_duel_glyph_strip': {'signature': 'state: SceneState, source: Cursor, colors: DuelGlyphContext, '
                                          'current: DuelInitializationResult | None=None',
                             'returns': 'DuelGlyphContext | DuelInitializationResult',
                             'flow': 'return _expand_and_upload_duel_glyphs(state, source, '
                                     'state.table(4294955776).cursor(), colors, current)'},
 '_expand_and_upload_duel_glyphs': {'signature': 'state, source, destination, colors, current=None',
                                    'returns': None,
                                    'flow': 'from .business_scene import decode_glyph_rows_to_buffers\n'
                                            'source = _live_cursor(state, source)\n'
                                            'colors.validate()\n'
                                            'saved = None\n'
                                            'if current is not None:\n'
                                            '    from .contexts_reuse import GlyphSavedValues\n'
                                            '    current.validate(state)\n'
                                            '    frame = current.preparation.frame\n'
                                            '    saved = GlyphSavedValues(frame.weapon_difference, '
                                            'current.glyph_work, current.preparation.response, '
                                            'frame.variation, current.glyph_source, '
                                            'current.preparation.stack)\n'
                                            'result = decode_glyph_rows_to_buffers(state, source, '
                                            'destination, colors.background, colors.foreground, '
                                            'colors.remaining, saved)\n'
                                            'source = _upload_longs(state, state.table(4294955776).cursor(), '
                                            '95)\n'
                                            'if current is not None:\n'
                                            '    restored = result.saved\n'
                                            '    frame = DuelActorFrame(replace_word(result.background, '
                                            '65535), result.foreground, frame.distance, result.remaining, '
                                            'restored.working, restored.pixels)\n'
                                            '    return _initialization_values(state, current, frame=frame, '
                                            'response=restored.response, glyph_work=restored.repeat, '
                                            'glyph_source=restored.glyph_source, source=source, '
                                            'destination=result.destination)\n'
                                            'return DuelGlyphContext(result.background, result.foreground, '
                                            'result.remaining)'},
 'decode_duel_byte_lanes': {'signature': 'state: SceneState, source: Cursor, destination: Cursor, length: '
                                         'Word, repeat_value: Long=0, pair_value: Long=0, *, length_carrier: '
                                         'Long | None=None, count_carrier: Long | None=None, stack: Cursor | '
                                         'None=None',
                            'returns': 'DuelLaneResult',
                            'flow': 'source = _live_cursor(state, source)\n'
                                    'destination = _live_cursor(state, destination)\n'
                                    "length = uint(length, 16, 'length')\n"
                                    'saved_address = destination.address()\n'
                                    'if stack is not None:\n'
                                    '    stack = _live_cursor(state, stack)\n'
                                    '    if length_carrier is None or count_carrier is None:\n'
                                    "        raise ValueError('complete lane save requires actual current "
                                    "values')\n"
                                    '    _push_actor_longs(stack, (length_carrier, saved_address))\n'
                                    'result = decode_duel_byte_lane(state, source, destination, length, '
                                    'repeat_value, pair_value, length_carrier=length_carrier, '
                                    'count_carrier=count_carrier)\n'
                                    'if stack is not None:\n'
                                    '    length_carrier, saved_address = _pop_actor_longs(stack, 2)\n'
                                    '    length = low16(length_carrier)\n'
                                    'return decode_duel_byte_lane(state, result.source, '
                                    'state.table(saved_address + 1).cursor(), length, result.repeat_value, '
                                    'result.pair_value, length_carrier=length_carrier, '
                                    'count_carrier=result.count_carrier)'},
 'decode_duel_byte_lane': {'signature': 'state: SceneState, source: Cursor, destination: Cursor, length: '
                                        'Word, repeat_value: Long=0, pair_value: Long=0, *, length_carrier: '
                                        'Long | None=None, count_carrier: Long | None=None',
                           'returns': 'DuelLaneResult',
                           'flow': 'source = _live_cursor(state, source)\n'
                                   'destination = _live_cursor(state, destination)\n'
                                   "remaining = uint(length, 16, 'length')\n"
                                   "repeat_value = uint(repeat_value, 32, 'repeat value')\n"
                                   "pair_value = uint(pair_value, 32, 'pair value')\n"
                                   'if length_carrier is not None:\n'
                                   '    uint(length_carrier, 32)\n'
                                   '    if low16(length_carrier) != length:\n'
                                   "        raise ValueError('lane length must agree with actual caller')\n"
                                   'if count_carrier is not None:\n'
                                   '    uint(count_carrier, 32)\n'
                                   'while remaining != 0:\n'
                                   '    token = source.next_byte()\n'
                                   '    if token < 128:\n'
                                   '        count = token\n'
                                   '        for _ in range(count + 1):\n'
                                   '            destination.set_byte(0, source.next_byte())\n'
                                   '            destination = destination.advance(2)\n'
                                   '            remaining = u16(remaining - 1)\n'
                                   '    elif not token & 64:\n'
                                   '        count = token & 63\n'
                                   '        repeat_value = replace_byte(repeat_value, source.next_byte())\n'
                                   '        for _ in range(count + 1):\n'
                                   '            destination.set_byte(0, low8(repeat_value))\n'
                                   '            destination = destination.advance(2)\n'
                                   '            remaining = u16(remaining - 1)\n'
                                   '    elif not token & 32:\n'
                                   '        count = token & 31\n'
                                   '        repeat_value = replace_byte(repeat_value, source.next_byte())\n'
                                   '        pair_value = replace_byte(pair_value, source.next_byte())\n'
                                   '        for _ in range(count + 1):\n'
                                   '            destination.set_byte(0, low8(repeat_value))\n'
                                   '            destination = destination.advance(2)\n'
                                   '            destination.set_byte(0, low8(pair_value))\n'
                                   '            destination = destination.advance(2)\n'
                                   '            remaining = u16(remaining - 2)\n'
                                   '    else:\n'
                                   '        count = token & 31\n'
                                   '        repeat_value = replace_byte(repeat_value, source.next_byte())\n'
                                   '        for _ in range(count + 1):\n'
                                   '            destination.set_byte(0, low8(repeat_value))\n'
                                   '            destination = destination.advance(2)\n'
                                   '            remaining = u16(remaining - 1)\n'
                                   '            repeat_value = replace_word(repeat_value, '
                                   'u16(low16(repeat_value) + 1))\n'
                                   '    if count_carrier is not None:\n'
                                   '        count_carrier = replace_word(count_carrier, 65535)\n'
                                   'if length_carrier is not None:\n'
                                   '    length_carrier = replace_word(length_carrier, remaining)\n'
                                   'return DuelLaneResult(source, destination, remaining, repeat_value, '
                                   'pair_value, length_carrier, count_carrier)'},
 '_wait_duel_status_text': {'signature': 'state, second, controls, preparation=None',
                            'returns': None,
                            'flow': 'if preparation is not None:\n'
                                    '    return _wait_complete_status(state, second, preparation)\n'
                                    'if not second:\n'
                                    '    state.table(16740432).set_word(2, 0)\n'
                                    'else:\n'
                                    '    state.table(16740512).set_word(2, 0)\n'
                                    'while True:\n'
                                    '    _duel_frame(state)\n'
                                    '    if not second:\n'
                                    '        advance_duel_entry_palette(state)\n'
                                    '    refresh_duel_actors(state)\n'
                                    "    if state.scalar('ram_700c_word') != 0:\n"
                                    '        continue\n'
                                    '    controls = _second_controls(state, controls) if second else '
                                    '_first_controls(state, controls)\n'
                                    '    controls = DuelControlContext(replace_word(controls.command, '
                                    'low16(controls.command) & 240), controls.mode)\n'
                                    '    if low16(controls.command) != 0:\n'
                                    '        return controls'},
 '_wait_complete_status': {'signature': 'state, second, preparation',
                           'returns': None,
                           'flow': 'preparation.validate(state)\n'
                                   'if type(second) is not bool:\n'
                                   "    raise ValueError('actual status side required')\n"
                                   'state.table(16740512 if second else 16740432).set_word(2, 0)\n'
                                   'current = preparation\n'
                                   'while True:\n'
                                   '    _duel_frame(state)\n'
                                   '    if not second:\n'
                                   '        current = advance_duel_entry_palette(state, current)\n'
                                   '    rendered = refresh_duel_actors(state, current.frame, current.stack, '
                                   'current.actor, current.opponent)\n'
                                   '    current = _preparation_with_frame(state, current, rendered.frame, '
                                   'rendered.actor, rendered.opponent, rendered.stack)\n'
                                   "    if state.scalar('ram_700c_word') != 0:\n"
                                   '        continue\n'
                                   '    controls = DuelControlContext(current.frame.command, '
                                   'current.frame.comparison)\n'
                                   '    controls = _second_controls(state, controls) if second else '
                                   '_first_controls(state, controls)\n'
                                   '    command = replace_word(controls.command, low16(controls.command) & '
                                   '240)\n'
                                   '    frame = DuelActorFrame(command, controls.mode, '
                                   'current.frame.distance, current.frame.factor, '
                                   'current.frame.weapon_difference, current.frame.variation)\n'
                                   '    current = _preparation_with_frame(state, current, frame)\n'
                                   '    if low16(command) != 0:\n'
                                   '        return current'},
 '_consume_complete_first_duel_frame': {'signature': 'state, preparation',
                                        'returns': None,
                                        'flow': 'preparation.validate(state)\n'
                                                'state.set_status_word(9984)\n'
                                                'frame = clear_duel_text_plane(state, preparation.frame)\n'
                                                '_duel_frame(state)\n'
                                                'controls = _first_controls(state, '
                                                'DuelControlContext(frame.command, frame.comparison))\n'
                                                'first, second = (state.table(16740432), '
                                                'state.table(16740512))\n'
                                                'first.set_word(0, low16(controls.command))\n'
                                                'response = preparation.response\n'
                                                "if state.scalar('ram_700a_byte') == 3:\n"
                                                '    actual_ai = DuelAIContext(controls.command, '
                                                'controls.mode, low16(preparation.response), '
                                                'low16(frame.variation), frame.retained, '
                                                'preparation.response)\n'
                                                '    ai = choose_duel_ai_command(state, first, second, '
                                                'actual_ai)\n'
                                                '    if ai.frame is None or not ai.frame.complete or '
                                                'ai.response is None:\n'
                                                "        raise Boundary('complete first automatic combat "
                                                "requires its actual AI return')\n"
                                                '    frame = ai.frame\n'
                                                '    response = ai.response\n'
                                                '    controls = DuelControlContext(frame.command, '
                                                'frame.comparison)\n'
                                                '    first.set_word(0, low16(controls.command))\n'
                                                'actual = DuelActorContext(controls.command, controls.mode, '
                                                'frame.distance, frame.retained, preparation.stack)\n'
                                                'returned = update_duel_actor(state, first, second, actual)\n'
                                                'return DuelActorResult(returned.command, '
                                                'returned.comparison, returned.damage, returned.frame, '
                                                'returned.actor, returned.opponent, returned.stack, '
                                                'response).validate()'},
 '_initialization_values': {'signature': 'state, current, *, frame=None, response=None, glyph_work=None, '
                                         'source=None, destination=None, glyph_source=None',
                            'returns': None,
                            'flow': 'current.validate(state)\n'
                                    'preparation = current.preparation\n'
                                    'return '
                                    'DuelInitializationResult(DuelPreparationContext(preparation.frame if '
                                    'frame is None else frame, preparation.response if response is None else '
                                    'response, preparation.actor if source is None else source, '
                                    'preparation.opponent if destination is None else destination, '
                                    'preparation.stack), current.glyph_work if glyph_work is None else '
                                    'glyph_work, current.glyph_source if glyph_source is None else '
                                    'glyph_source).validate(state)'},
 '_stage_complete_duel_packet': {'signature': 'state, current, source_address, command, rows, row_command',
                                 'returns': None,
                                 'flow': 'from .business_reuse import stage_sprite_word_packet\n'
                                         'from .contexts_reuse import SpritePacketContext\n'
                                         'current.validate(state)\n'
                                         'preparation, frame = (current.preparation, '
                                         'current.preparation.frame)\n'
                                         'source = state.table(source_address).cursor()\n'
                                         'packet = SpritePacketContext(command, '
                                         'replace_word(frame.comparison, rows), replace_word(frame.distance, '
                                         'row_command), frame.factor, frame.weapon_difference, '
                                         'current.glyph_work, preparation.response, frame.variation, source, '
                                         'preparation.opponent.cursor(), current.glyph_source, '
                                         'preparation.stack)\n'
                                         'result = stage_sprite_word_packet(state, source, command, rows, '
                                         'row_command, packet)\n'
                                         'frame = DuelActorFrame(result.command, result.rows, '
                                         'result.row_command, result.remaining, result.token, '
                                         'result.rows_remaining)\n'
                                         'return _initialization_values(state, current, frame=frame, '
                                         'response=result.response, glyph_work=result.run_count, '
                                         'source=result.source, destination=result.destination, '
                                         'glyph_source=result.glyph_source)'},
 '_choose_complete_duel_loadout': {'signature': 'state, second, preparation',
                                   'returns': None,
                                   'flow': 'preparation.validate(state)\n'
                                           'if type(second) is not bool:\n'
                                           "    raise ValueError('actual loadout side required')\n"
                                           "mode_name = 'ram_700b_byte' if second else 'ram_700a_byte'\n"
                                           'current = preparation\n'
                                           'if state.scalar(mode_name) != 3:\n'
                                           "    raise Boundary('manual equipment/menu return needs its "
                                           "complete current-value contract')\n"
                                           'if not second:\n'
                                           '    current = advance_duel_entry_palette(state, current)\n'
                                           'while True:\n'
                                           '    _duel_frame(state)\n'
                                           '    current = advance_duel_entry_palette(state, current)\n'
                                           '    rendered = refresh_duel_actors(state, current.frame, '
                                           'current.stack, current.actor, current.opponent)\n'
                                           '    current = _preparation_with_frame(state, current, '
                                           'rendered.frame, rendered.actor, rendered.opponent, '
                                           'rendered.stack)\n'
                                           '    if not second:\n'
                                           "        state.set_scalar('ram_708a_word', 0)\n"
                                           '    if state.scalar(mode_name) != 3:\n'
                                           "        raise Boundary('live loadout switched into unresolved "
                                           "full manual return')\n"
                                           '    current = _preparation_with_frame(state, current, '
                                           'current.frame, actor=state.table(16740512 if second else '
                                           '16740432))\n'
                                           '    current = _choose_duel_ai_panel(state, current.actor, '
                                           'current.opponent, DuelControlContext(current.frame.command, '
                                           'current.frame.comparison), current)\n'
                                           '    selected_second = current.actor.base != 16740432\n'
                                           '    if not selected_second and low16(current.response) == 0:\n'
                                           '        second = False\n'
                                           "        mode_name = 'ram_700a_byte'\n"
                                           '        continue\n'
                                           '    return (_commit_complete_duel_loadout(state, current, '
                                           'selected_second), selected_second)'},
 '_prepare_complete_first_status': {'signature': 'state, preparation',
                                    'returns': None,
                                    'flow': 'from .business_reuse import _reuse_advance_random_pair\n'
                                            'preparation.validate(state)\n'
                                            'random = _reuse_advance_random_pair(state)\n'
                                            'selection = low16(random.sample) & 3\n'
                                            'if selection == 3:\n'
                                            '    selection = 0\n'
                                            'command = choose_duel_status_text(state, selection, '
                                            'random.sample)\n'
                                            'frame = preparation.frame\n'
                                            'frame = DuelActorFrame(replace_word(command, 165), '
                                            'random.updated_state, frame.distance, frame.factor, '
                                            'frame.weapon_difference, frame.variation)\n'
                                            '_sound(state, 165)\n'
                                            'current = _preparation_with_frame(state, preparation, frame)\n'
                                            'current = _wait_duel_status_text(state, False, '
                                            'DuelControlContext(frame.command, frame.comparison), current)\n'
                                            'state.set_status_word(9984)\n'
                                            'return _preparation_with_frame(state, current, '
                                            'clear_duel_text_plane(state, current.frame))'},
 'prepare_duel_scene_first_frame': {'signature': 'state: SceneState, context: DuelInitializationContext',
                                    'returns': 'DuelPreparationResult',
                                    'flow': 'if type(context) is not DuelInitializationContext:\n'
                                            "    raise ValueError('actual complete initialization input "
                                            "required')\n"
                                            'context.validate(state)\n'
                                            'initialized = _initialize_duel_scene(state, context)\n'
                                            'current, selected_second = _choose_complete_duel_loadout(state, '
                                            'False, initialized.preparation)\n'
                                            'while not selected_second:\n'
                                            '    current, selected_second = '
                                            '_choose_complete_duel_loadout(state, True, current)\n'
                                            'current = _prepare_complete_first_status(state, current)\n'
                                            'current = _prepare_complete_second_status(state, current)\n'
                                            'actual = _consume_complete_first_duel_frame(state, current)\n'
                                            "return DuelPreparationResult('first_frame', None, "
                                            'actual).validate(state)'},
 '_initialize_duel_scene': {'signature': 'state, context',
                            'returns': None,
                            'flow': 'from .business_reuse import clear_video_sprite_plane, '
                                    'expand_glyph_stream\n'
                                    'from .contexts_reuse import GlyphColors, GlyphSavedValues\n'
                                    'from .contexts_scene import PacketTransferValues\n'
                                    'from .business_scene import flush_scene_transfer_queue\n'
                                    'if type(context) is not DuelInitializationContext:\n'
                                    "    raise Boundary('natural initialization requires explicit complete "
                                    "live-in and stack')\n"
                                    'context.validate(state)\n'
                                    'frame = context.frame\n'
                                    'state.set_status_word(9984)\n'
                                    "command = replace_word(frame.command, state.scalar('ram_f606_word'))\n"
                                    'command = replace_byte(command, low8(command) & 191)\n'
                                    'state.mmio_write(12582916, 2, low16(command))\n'
                                    "state.set_scalar('ram_f612_word', 0)\n"
                                    'cleared = clear_video_sprite_plane(state, context.response)\n'
                                    'response = cleared.response\n'
                                    'frame = DuelActorFrame(command, frame.comparison, frame.distance, '
                                    'frame.factor, frame.weapon_difference, cleared.variation)\n'
                                    'for command in (33592, 33336, 33799, 34156, 36151, 37524, 35587):\n'
                                    '    state.mmio_write(12582916, 2, command)\n'
                                    'first, second = (state.table(16740432), state.table(16740512))\n'
                                    'first.set_long(14, 4194304)\n'
                                    'first.set_word(24, 34816)\n'
                                    'first.set_word(2, 1)\n'
                                    'second.set_long(14, 16777216)\n'
                                    'second.set_word(24, 40960)\n'
                                    'second.set_word(2, 1)\n'
                                    "state.set_scalar('ram_70f0_word', 0)\n"
                                    "state.set_scalar('ram_70f6_word', 0)\n"
                                    "state.set_scalar('ram_70f8_word', 0)\n"
                                    'equipment = state.table(4294961800).cursor(u16(first.word(26) * 3))\n'
                                    'first.set_byte(43, equipment.next_byte())\n'
                                    'first.set_byte(45, equipment.next_byte())\n'
                                    'first.set_byte(47, equipment.byte())\n'
                                    'equipment_product = u32(second.word(26) * 3)\n'
                                    'equipment = state.table(4294961800).cursor(low16(equipment_product))\n'
                                    'second.set_byte(43, equipment.next_byte())\n'
                                    'second.set_byte(45, equipment.next_byte())\n'
                                    'second.set_byte(47, equipment.byte())\n'
                                    'state.mmio_write(12582916, 4, 1073741824)\n'
                                    '_upload_longs(state, state.table(443316).cursor(), 12287)\n'
                                    'state.mmio_write(12582916, 4, 1073741827)\n'
                                    '_upload_longs(state, state.table(564700).cursor(), 31)\n'
                                    'frame = DuelActorFrame(replace_word(frame.command, 1), '
                                    'replace_word(frame.comparison, 2), frame.distance, '
                                    'replace_word(frame.factor, 9), equipment_product, frame.variation)\n'
                                    'source, destination = (state.table(566310).cursor(), '
                                    'state.table(4294955776).cursor())\n'
                                    'glyph = expand_glyph_stream(state, source, destination, '
                                    'GlyphColors(frame.command, frame.comparison), frame.factor, '
                                    'GlyphSavedValues(frame.weapon_difference, context.glyph_work, response, '
                                    'frame.variation, state.table(562908), context.stack))\n'
                                    'frame = DuelActorFrame(replace_word(frame.command, 65535), '
                                    'frame.comparison, frame.distance, glyph.remaining_carrier, '
                                    'glyph.saved.working, glyph.saved.pixels)\n'
                                    'source = _upload_longs(state, state.table(4294955776).cursor(), 79)\n'
                                    'current = DuelInitializationResult(DuelPreparationContext(frame, '
                                    'glyph.saved.response, source, glyph.destination, context.stack), '
                                    'glyph.saved.repeat, glyph.saved.glyph_source).validate(state)\n'
                                    'state.mmio_write(12582916, 4, 1342177283)\n'
                                    '_upload_longs(state, state.table(492468).cursor(), 47)\n'
                                    'state.mmio_write(12582916, 4, 1107296259)\n'
                                    'for actor in (first, second):\n'
                                    '    frame = current.preparation.frame\n'
                                    '    frame = DuelActorFrame(replace_word(frame.command, 1), '
                                    'replace_word(frame.comparison, 2), frame.distance, frame.factor, '
                                    'frame.weapon_difference, frame.variation)\n'
                                    '    current = _initialization_values(state, current, frame=frame)\n'
                                    '    current = upload_duel_officer_name(state, actor.word(26), '
                                    'DuelGlyphContext(frame.command, frame.comparison, frame.factor), '
                                    'current)\n'
                                    'frame = current.preparation.frame\n'
                                    'frame = DuelActorFrame(replace_word(frame.command, 1), '
                                    'replace_word(frame.comparison, 2), frame.distance, '
                                    'replace_word(frame.factor, 1), frame.weapon_difference, '
                                    'frame.variation)\n'
                                    'current = _initialization_values(state, current, frame=frame)\n'
                                    'current = upload_duel_glyph_strip(state, state.table(166074).cursor(), '
                                    'DuelGlyphContext(frame.command, frame.comparison, frame.factor), '
                                    'current)\n'
                                    'current = _initialization_values(state, current, '
                                    'frame=clear_duel_text_plane(state, current.preparation.frame))\n'
                                    'source, destination = (state.table(163968).cursor(), '
                                    'state.table(4294966016).cursor())\n'
                                    'for _ in range(32):\n'
                                    '    destination.append_long(source.next_long())\n'
                                    'frame = current.preparation.frame\n'
                                    'current = _initialization_values(state, current, '
                                    'frame=DuelActorFrame(replace_word(frame.command, 65535), '
                                    'frame.comparison, frame.distance, frame.factor, '
                                    'frame.weapon_difference, frame.variation), source=source, '
                                    'destination=destination)\n'
                                    "state.set_scalar('ram_f31e_word', 1)\n"
                                    'map_source = state.table(492660).cursor()\n'
                                    "if state.scalar('ram_70f2_word') == 3:\n"
                                    '    map_source = state.table(493142).cursor()\n'
                                    'frame = current.preparation.frame\n'
                                    'lanes = decode_duel_byte_lanes(state, map_source, '
                                    'state.table(16736256).cursor(), 1280, frame.distance, frame.factor, '
                                    'length_carrier=replace_word(frame.command, 1280), '
                                    'count_carrier=frame.comparison, stack=context.stack)\n'
                                    'frame = DuelActorFrame(replace_word(lanes.length_carrier, 65535), '
                                    'lanes.count_carrier, lanes.repeat_value, lanes.pair_value, '
                                    'frame.weapon_difference, frame.variation)\n'
                                    'current = _initialization_values(state, current, frame=frame, '
                                    'source=lanes.source, destination=lanes.destination)\n'
                                    'state.mmio_write(12582916, 4, 1610612739)\n'
                                    '_upload_words(state, state.table(16736256).cursor(), 1279)\n'
                                    'lanes = decode_duel_byte_lanes(state, state.table(493630).cursor(), '
                                    'state.table(16736256).cursor(), 1280, frame.distance, frame.factor, '
                                    'length_carrier=replace_word(frame.command, 1280), '
                                    'count_carrier=frame.comparison, stack=context.stack)\n'
                                    'frame = DuelActorFrame(replace_word(lanes.length_carrier, 65535), '
                                    'lanes.count_carrier, lanes.repeat_value, lanes.pair_value, '
                                    'frame.weapon_difference, frame.variation)\n'
                                    'current = _initialization_values(state, current, frame=frame, '
                                    'source=lanes.source, destination=lanes.destination)\n'
                                    'state.mmio_write(12582916, 4, 1879048195)\n'
                                    '_upload_words(state, state.table(16736256).cursor(), 1279)\n'
                                    "state.set_scalar('ram_f694_word', 1539)\n"
                                    "state.set_scalar('ram_f692_word', 1540)\n"
                                    'current = _stage_complete_duel_packet(state, current, 164128, '
                                    '1610612776, 3, 59904)\n'
                                    'frame = current.preparation.frame\n'
                                    'flushed = flush_scene_transfer_queue(state, '
                                    'PacketTransferValues(frame.command, frame.comparison, frame.distance, '
                                    'frame.factor))\n'
                                    'if flushed is not None:\n'
                                    '    values = flushed.values\n'
                                    '    frame = DuelActorFrame(values.command, values.increment, '
                                    'values.address, values.spill, frame.weapon_difference, '
                                    'frame.variation)\n'
                                    '    current = _initialization_values(state, current, frame=frame, '
                                    'source=flushed.source)\n'
                                    'current = _stage_complete_duel_packet(state, current, 164212, '
                                    '1610612776, 5, 60288)\n'
                                    'return current'},
 'run_duel_scene': {'signature': 'state: SceneState, context: DuelSceneContext=DuelSceneContext()',
                    'returns': 'DuelSceneResult',
                    'flow': 'context.validate()\n'
                            'if context.initialization is None:\n'
                            "    raise Boundary('natural duel scene needs its complete actual initialization "
                            "live-in')\n"
                            'prepare_duel_scene_first_frame(state, context.initialization)\n'
                            "raise Boundary('first actor completed; subsequent natural main continuation is "
                            "not yet projected')"}}
DECLARATIONS.update(HOST_INITIALIZATION_DECLARATIONS)
APPROVED.setdefault('contexts_duel', set()).update({'DuelInitializationContext', 'DuelInitializationResult'})
APPROVED.setdefault('contexts_reuse', set()).update({'GlyphSavedValues', 'SpritePacketContext'})
APPROVED.setdefault('contexts_scene', set()).update({'PacketTransferValues'})

def compile_duel(source, *, selected_names=None):
    if selected_names is not None:
        records, policy = admit_selected_duel_fields(source, DECLARATIONS, APPROVED, selected_names)
        selected_bindings = tuple((binding for binding in DUEL_BINDINGS if binding.name in selected_names))
        if len(selected_bindings) != len(selected_names):
            raise CompileError('all ten complete selected duel owners required')
        result = lower_declared(records, selected_bindings, {name: LOWERERS[name] for name in selected_names})
        result['source_policy'] = policy
        return result
    records, policy = admit_menu_source(source, DECLARATIONS, APPROVED, extra_roles=_ACTION_ROLES + _AI_ROLES + _ACTOR_ROLES + _FLOW_ROLES, extra_rule_builders=(_action_rules, _ai_rules, _actor_rules, _flow_rules))
    sole_strategy_fields = {name: records[name]['effects'] for name in ('_duel_strategy_actor_values', '_duel_strategy_call_fields', '_duel_strategy_live_mode_fields', '_duel_strategy_partial_fields', '_duel_strategy_probability_fields', 'choose_duel_ai_command_fields', 'choose_duel_ai_override_fields', 'choose_duel_ai_timeout_fields', 'measure_duel_weapon_contact_fields', 'sample_duel_probability_fields', 'scan_duel_thresholds_fields')}
    for owner in ('scan_duel_thresholds', 'measure_duel_weapon_contact', 'sample_duel_probability', 'choose_duel_ai_timeout', 'choose_duel_ai_override', 'choose_duel_ai_command'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'], sole_strategy_fields=sole_strategy_fields)
    sole_sprite_fields = {name: records[name]['effects'] for name in ('_duel_sprite_append_word_fields', 'append_duel_sprite_fields')}
    records['append_duel_sprite']['effects'] = dict(previous_fields=records['append_duel_sprite']['effects'], sole_sprite_fields=sole_sprite_fields)
    sole_actor_fields = {name: records[name]['effects'] for name in ('_duel_actor_attack_fields', '_duel_actor_call_fields', '_duel_actor_clear_word_fields', '_duel_actor_flag_fields', '_duel_actor_motion_fields', '_duel_actor_motion_mode_fields', '_duel_actor_overlay_fields', '_duel_actor_palette_fields', '_duel_actor_render_positions_fields', '_duel_actor_restore_words_fields', '_duel_actor_save_words_fields', '_duel_actor_store_fields', '_duel_actor_strike_fields', 'render_duel_actor_fields', 'update_duel_actor_fields')}
    records['update_duel_actor']['effects'] = dict(previous_fields=records['update_duel_actor']['effects'], sole_actor_fields=sole_actor_fields)
    sole_refresh_fields = {name: records[name]['effects'] for name in ('_duel_actor_refresh_call_fields', 'refresh_duel_actors_fields')}
    records['refresh_duel_actors']['effects'] = dict(previous_fields=records['refresh_duel_actors']['effects'], sole_refresh_fields=sole_refresh_fields)
    records['configure_duel_weapon_motion']['effects'] = dict(previous_fields=records['configure_duel_weapon_motion']['effects'], sole_motion_fields=records['configure_duel_weapon_motion_fields']['effects'])
    sole_menu_fields = {name: records[name]['effects'] for name in ('_duel_menu_call_fields', '_duel_menu_button_fields', '_duel_menu_adjust_memory_word_fields', '_duel_menu_equipment_slot', '_duel_menu_equipment_present_fields', '_duel_menu_loadout_highlight_fields', 'choose_duel_two_option_menu_fields', 'choose_duel_equipment_fields', 'choose_first_duel_equipment_fields', 'choose_second_duel_equipment_fields', '_duel_action_direction_fields', '_duel_action_restricted_choice_fields', '_duel_action_menu_highlight_fields', 'choose_duel_action_menu_fields', '_duel_menu_observations_to_fields', '_duel_menu_fields_to_observations')}
    for owner in ('choose_duel_two_option_menu', 'choose_first_duel_equipment', 'choose_duel_action_menu'):
        records[owner]['effects'] = dict(previous_projection=records[owner]['effects'], sole_full_menu_fields=sole_menu_fields)
    sole_scene_fields = {name: records[name]['effects'] for name in ('_duel_scene_status_fields', '_duel_scene_store_fields', '_duel_scene_frame_ack_fields', '_duel_scene_call_fields', '_duel_scene_copy_fields', '_duel_scene_dialog_fields', '_duel_scene_packet_fields', 'initialize_duel_scene_fields', '_duel_scene_auto_loadout_fields', 'prepare_duel_loadout_fields', 'commit_duel_loadout_fields', 'prepare_duel_readiness_fields', 'begin_duel_combat_fields', '_duel_scene_actor_fields', 'continue_after_first_duel_actor_fields', 'choose_duel_turn_action_fields', 'continue_manual_duel_action_fields', '_duel_scene_button_fields', 'perform_selected_duel_action_fields', 'show_terminal_duel_result_fields', 'finish_duel_scene_fields', 'run_duel_scene_fields', '_duel_scene_legacy_context_fields')}
    records['run_duel_scene']['effects'] = dict(previous_projection=records['run_duel_scene']['effects'], sole_logical_scene_fields=sole_scene_fields)
    sole_status_fields = {name: records[name]['effects'] for name in ('show_active_duel_turn_label_fields', 'choose_duel_status_text_fields', '_wait_duel_action_fields', 'wait_active_duel_action_fields', 'wait_either_duel_action_fields', 'continue_duel_action_wait_fields')}
    for owner in ('show_active_duel_turn_label', 'wait_active_duel_action', 'choose_duel_status_text'):
        records[owner]['effects'] = dict(previous_projection=records[owner]['effects'], sole_status_label_wait_fields=sole_status_fields)
    sole_children_fields = {name: records[name]['effects'] for name in ('advance_duel_entry_palette_fields', 'upload_duel_officer_name_fields', 'upload_duel_glyph_strip_fields', '_upload_duel_glyph_buffers_fields', 'clear_duel_text_plane_fields', 'decode_duel_byte_lanes_fields', '_duel_lane_emit_fields', 'decode_duel_byte_lane_fields', '_duel_lane_legacy_fields', '_duel_lane_fields_to_observations', '_duel_scene_call_fields')}
    for owner in ('advance_duel_entry_palette', 'upload_duel_officer_name', 'clear_duel_text_plane', 'decode_duel_byte_lanes'):
        records[owner]['effects'] = dict(previous_projection=records[owner]['effects'], sole_duel_children_fields=sole_children_fields)
    records['run_duel_scene']['effects'] = dict(previous_fields=records['run_duel_scene']['effects'], sole_indexed_action_fields={name: records[name]['effects'] for name in ('_duel_scene_call_fields', 'run_duel_scene_fields', 'perform_selected_duel_action_fields', '_duel_scene_indexed_action_fields', 'perform_selected_duel_action_result_fields')})
    result = lower_declared(records, DUEL_BINDINGS, LOWERERS)
    result['source_policy'] = policy
    return result

# Complete linkage13 source admission; no legacy-body normalization.
HOST_COMPLETE_TURN_DECLARATIONS = {'_live_table': {'signature': 'state, value', 'returns': '', 'flow': "if not isinstance(value, Table) or value.state is not state:\n    raise ValueError('live same-state Table required')\nreturn value"}, '_live_cursor': {'signature': 'state, value', 'returns': '', 'flow': "if not isinstance(value, Cursor) or value.state is not state:\n    raise ValueError('live same-state Cursor required')\nreturn value"}, '_actor_word': {'signature': 'value, word', 'returns': '', 'flow': 'return None if value is None else replace_word(value, word)'}, '_actor_byte': {'signature': 'value, byte', 'returns': '', 'flow': 'return None if value is None else replace_byte(value, byte)'}, '_actor_reframe': {'signature': 'base, command, comparison, distance, factor, weapon_difference, variation, *, working_value=None, response=None, lookup=None', 'returns': '', 'flow': "if type(base) is not DuelActorFrame:\n    raise ValueError('actual actor field source required')\nreturn DuelActorFrame(command, comparison, distance, factor, weapon_difference, variation, base.working_value if working_value is None else working_value, base.response if response is None else response, base.lookup if lookup is None else lookup).validate()"}, '_turn_actor_values': {'signature': 'frame', 'returns': '', 'flow': 'return DuelActorFrame(frame.command, frame.comparison, frame.distance, frame.factor, frame.weapon_difference, frame.variation, frame.working_value, frame.response, frame.lookup).validate()'}, '_turn_from_actor': {'signature': 'state, original, fields, actor, opponent, stack', 'returns': '', 'flow': "checked_duel_turn(original, state)\nfields.validate()\nif not fields.complete or fields.working_value is None or fields.response is None or (fields.lookup is None):\n    raise Boundary('complete duel algorithm omitted current working/response/lookup return')\nreturn DuelTurnFrame(fields.command, fields.comparison, fields.distance, fields.factor, fields.weapon_difference, fields.working_value, fields.response, fields.variation, actor, opponent, fields.lookup, stack, DuelConditionObservation(None, None, None, None)).validate(state)"}, '_actor_input_frame': {'signature': 'context', 'returns': '', 'flow': "if type(context) is not DuelActorContext:\n    raise ValueError('actual actor input required')\ncontext.validate()\nif context.live is not None:\n    current = checked_duel_turn(context.live, context.live.actor.state)\n    if (current.command, current.comparison, current.distance, current.stack) != (context.command, context.comparison, context.damage, context.stack):\n        raise ValueError('actor observations must agree with actual full caller')\n    return _turn_actor_values(current)\nretained = context.retained\nreturn DuelActorFrame(context.command, context.comparison, context.damage, retained.factor if retained is not None else None, retained.weapon_difference if retained is not None else None, retained.variation if retained is not None else None).validate()"}, '_actor_stack': {'signature': 'state, frame, stack', 'returns': '', 'flow': "if type(frame) is not DuelActorFrame:\n    raise ValueError('actual current actor frame required')\nframe.validate()\nif stack is not None:\n    return _live_cursor(state, stack)\nif frame.complete:\n    raise Boundary('complete actor return needs the actual live stack cursor')\nreturn None"}, '_push_actor_longs': {'signature': 'stack, values', 'returns': '', 'flow': "if stack is None:\n    return\nfor value in values[::-1]:\n    if value is None:\n        raise Boundary('native saved actor value is unknown')\n    uint(value, 32, 'actual saved actor value')\nfor value in values[::-1]:\n    stack.base = u32(stack.base - 4)\n    stack.set_long(0, value)"}, '_pop_actor_longs': {'signature': 'stack, count', 'returns': '', 'flow': 'return tuple((stack.next_long() for _ in range(count)))'}, '_push_actor_pair_words': {'signature': 'stack, command, comparison', 'returns': '', 'flow': 'if stack is None:\n    return\nstack.base = u32(stack.base - 2)\nstack.set_word(0, low16(comparison))\nstack.base = u32(stack.base - 2)\nstack.set_word(0, low16(command))'}, '_pop_actor_pair_words': {'signature': 'stack, command, comparison', 'returns': '', 'flow': 'if stack is not None:\n    command, comparison = (stack.next_word(), stack.next_word())\nreturn (u32(s16(low16(command))), u32(s16(low16(comparison))))'}, '_duel_frame': {'signature': 'state', 'returns': '', 'flow': "state.set_status_word(9472)\nstate.set_scalar('ram_f612_word', 1792)\nwhile state.read(4294964754, 1) != 0:\n    state.progress('duel_frame_low_byte_ack')"}, '_sound': {'signature': 'state, command', 'returns': '', 'flow': "from .business_reuse import enqueue_sound_command\nreturn enqueue_sound_command(state, uint(command, 8, 'sound command'))"}, '_random': {'signature': 'state', 'returns': '', 'flow': 'from .business_reuse import step_random\nreturn step_random(state)'}, '_first_controls': {'signature': 'state, controls', 'returns': '', 'flow': 'from .business_reuse import choose_first_duel_control\nresult = choose_first_duel_control(state, controls.command, controls.mode)\nreturn DuelControlContext(result.command, result.mode_carrier)'}, '_second_controls': {'signature': 'state, controls', 'returns': '', 'flow': 'from .business_reuse import choose_second_duel_control\nresult = choose_second_duel_control(state, controls.command, controls.mode)\nreturn DuelControlContext(result.command, result.mode_carrier)'}, '_upload_longs': {'signature': 'state, source, count_latch', 'returns': '', 'flow': "source = _live_cursor(state, source)\ncounter = uint(count_latch, 16, 'count latch')\nwhile True:\n    state.mmio_write(12582912, 4, source.next_long())\n    counter = u16(counter - 1)\n    if counter == 65535:\n        return source"}, '_upload_words': {'signature': 'state, source, count_latch', 'returns': '', 'flow': "source = _live_cursor(state, source)\ncounter = uint(count_latch, 16, 'count latch')\nwhile True:\n    state.mmio_write(12582912, 2, source.next_word())\n    counter = u16(counter - 1)\n    if counter == 65535:\n        return source"}, 'advance_duel_entry_palette': {'signature': 'state: SceneState, preparation: DuelPreparationContext | None=None', 'returns': 'DuelPreparationContext | None', 'flow': "from .business_scene import darken_palette\nif preparation is not None:\n    preparation.validate(state)\nif state.scalar('ram_70f8_word') >= 16:\n    return preparation\nintensity = u16(15 - state.scalar('ram_70f8_word'))\nif preparation is None:\n    darken_palette(state, intensity, 64, state.table(163968).cursor())\n    current = None\nelse:\n    frame = preparation.frame\n    result = darken_palette(state, replace_word(frame.command, intensity), 64, state.table(163968).cursor(), frame.weapon_difference, count_carrier=replace_word(frame.comparison, 64), color=frame.distance, component=frame.factor)\n    current = _preparation_with_frame(state, preparation, _actor_reframe(frame, result.shade_carrier, result.count_carrier, result.color, result.component, result.accumulated, frame.variation), result.source, result.destination)\nstate.set_scalar('ram_70f8_word', u16(state.scalar('ram_70f8_word') + 1))\nreturn current"}, 'show_active_duel_turn_label': {'signature': 'state: SceneState', 'returns': 'Long', 'flow': "raise Boundary('this legacy partial observation lacks the actual current duel frame; use the complete core')"}, 'wait_active_duel_action': {'signature': 'state: SceneState, controls: DuelControlContext=DuelControlContext()', 'returns': 'DuelControlContext', 'flow': "raise Boundary('this legacy partial observation lacks the actual current duel frame; use the complete core')"}, 'wait_either_duel_action': {'signature': 'state: SceneState, controls: DuelControlContext=DuelControlContext()', 'returns': 'DuelControlContext', 'flow': "raise Boundary('this legacy partial observation lacks the actual current duel frame; use the complete core')"}, 'configure_duel_weapon_motion': {'signature': 'state: SceneState, actor: Table, frame: DuelActorFrame | None=None', 'returns': 'DuelActorFrame | None', 'flow': "actor = _live_table(state, actor)\nif frame is not None:\n    if type(frame) is not DuelActorFrame:\n        raise ValueError('actual weapon configuration frame required')\n    frame.validate()\nattribute = actor.word(30)\nmode_offset = u16(actor.word(12) << 1)\npenalty = state.table(162430).word(mode_offset)\ndifference = u16(attribute - penalty)\nif attribute < penalty:\n    difference = 0\nelif difference >= 80:\n    difference = 80\ndelay = u16(80 - difference)\ncommand = u32(difference * 1792 + 24576)\nactor.set_long(18, command)\ncomparison = divu_retained(delay, 2)\nactor.set_word(22, low16(comparison))\nif frame is not None:\n    return _actor_reframe(frame, command, comparison, frame.distance, frame.factor, frame.weapon_difference, frame.variation).validate()\nreturn None"}, 'refresh_duel_actors': {'signature': 'state: SceneState, frame: DuelActorFrame | None=None, stack: Cursor | None=None, caller_actor: Table | None=None, caller_opponent: Table | None=None', 'returns': 'DuelRenderResult', 'flow': 'current = DuelActorFrame() if frame is None else frame\nstack = _actor_stack(state, current, stack)\nif stack is not None:\n    caller_actor = _live_table(state, caller_actor)\n    caller_opponent = _live_table(state, caller_opponent)\n    _push_actor_longs(stack, (caller_actor.base, caller_opponent.base))\nfirst, second = (state.table(16740432), state.table(16740512))\nfirst.set_word(0, 0)\n_duel_enter_actor_call(stack)\nfirst_result = render_duel_actor(state, first, second, current, stack)\n_duel_leave_actor_call(stack)\nsecond.set_word(0, 0)\n_duel_enter_actor_call(stack)\nsecond_result = render_duel_actor(state, second, first, first_result.frame, stack)\n_duel_leave_actor_call(stack)\nif stack is not None:\n    actor_base, opponent_base = _pop_actor_longs(stack, 2)\n    caller_actor, caller_opponent = (state.table(actor_base), state.table(opponent_base))\nreturn DuelRenderResult(second_result.frame, caller_actor, caller_opponent, stack).validate(state)'}, 'upload_duel_officer_name': {'signature': 'state: SceneState, officer: Word, colors: DuelGlyphContext, current: DuelInitializationResult | None=None', 'returns': 'DuelGlyphContext | DuelInitializationResult', 'flow': "officer = uint(officer, 16, 'officer')\ncolors.validate()\nif current is not None:\n    current.validate(state)\n    frame = current.preparation.frame\n    if (colors.background, colors.foreground, colors.remaining) != (frame.command, frame.comparison, frame.factor):\n        raise ValueError('name colors must be the actual current values')\n    frame = _actor_reframe(frame, frame.command, frame.comparison, frame.distance, frame.factor, frame.weapon_difference, u32(officer * 6))\n    current = _initialization_values(state, current, frame=frame)\nsource = state.table(566532).cursor(u16(officer * 6))\nremaining = replace_word(colors.remaining, 2)\nif source.word(4) == 63:\n    remaining = replace_word(remaining, 1)\n    shade = u8(u16(low16(colors.background) << 4) | low16(colors.background))\n    first, second = (state.table(4294955776).cursor(), state.table(4294956096).cursor())\n    for _ in range(64):\n        first.append_byte(shade)\n        second.append_byte(shade)\n    if current is not None:\n        frame = current.preparation.frame\n        working = replace_word(frame.weapon_difference, u16(low16(frame.command) << 4 | low16(frame.command)))\n        current = _initialization_values(state, current, frame=_actor_reframe(frame, frame.command, frame.comparison, frame.distance, remaining, working, frame.variation), glyph_work=replace_word(current.glyph_work, 65535), glyph_source=second)\n    return _expand_and_upload_duel_glyphs(state, source, first, DuelGlyphContext(colors.background, colors.foreground, remaining), current)\nreturn upload_duel_glyph_strip(state, source, DuelGlyphContext(colors.background, colors.foreground, remaining), current)"}, 'upload_duel_glyph_strip': {'signature': 'state: SceneState, source: Cursor, colors: DuelGlyphContext, current: DuelInitializationResult | None=None', 'returns': 'DuelGlyphContext | DuelInitializationResult', 'flow': 'return _expand_and_upload_duel_glyphs(state, source, state.table(4294955776).cursor(), colors, current)'}, '_expand_and_upload_duel_glyphs': {'signature': 'state, source, destination, colors, current=None', 'returns': '', 'flow': 'from .business_scene import decode_glyph_rows_to_buffers\nsource = _live_cursor(state, source)\ncolors.validate()\nsaved = None\nif current is not None:\n    from .contexts_reuse import GlyphSavedValues\n    current.validate(state)\n    frame = current.preparation.frame\n    saved = GlyphSavedValues(frame.weapon_difference, current.glyph_work, current.preparation.response, frame.variation, current.glyph_source, current.preparation.stack)\nresult = decode_glyph_rows_to_buffers(state, source, destination, colors.background, colors.foreground, colors.remaining, saved)\nsource = _upload_longs(state, state.table(4294955776).cursor(), 95)\nif current is not None:\n    restored = result.saved\n    frame = _actor_reframe(frame, replace_word(result.background, 65535), result.foreground, frame.distance, result.remaining, restored.working, restored.pixels)\n    return _initialization_values(state, current, frame=frame, response=restored.response, glyph_work=restored.repeat, glyph_source=restored.glyph_source, source=source, destination=result.destination)\nreturn DuelGlyphContext(result.background, result.foreground, result.remaining)'}, 'clear_duel_text_plane': {'signature': 'state: SceneState, frame: DuelActorFrame | None=None', 'returns': 'DuelActorFrame | None', 'flow': "if frame is not None:\n    if type(frame) is not DuelActorFrame:\n        raise ValueError('actual clear-text frame required')\n    frame.validate()\nstate.set_scalar('ram_d100_word', 0)\nstate.mmio_write(12582916, 4, 1174405123)\nfor _ in range(640):\n    state.mmio_write(12582912, 4, 286331153)\nif frame is not None:\n    return _actor_reframe(frame, 286331153, _actor_word(frame.comparison, 65535), frame.distance, frame.factor, frame.weapon_difference, frame.variation).validate()\nreturn None"}, 'choose_duel_two_option_menu': {'signature': 'state: SceneState, choice: Table, controls: DuelControlContext', 'returns': 'DuelControlContext', 'flow': "choice = _live_table(state, choice)\ncontrols.validate()\nselected = choice.word()\ndirection = low16(controls.command) & 12\nif direction:\n    delta = 1 if direction & 8 else 65535\n    selected = u16(selected + delta)\n    if selected < 2:\n        choice.set_word(0, selected)\ncontrols = _first_controls(state, controls)\nif low16(controls.command) & 32:\n    return controls\ndirection = low16(controls.command) & 12\nif direction or state.scalar('ram_7008_word') & 8:\n    append_duel_sprite(state, 200, u16(choice.word() * 56 + 121), 67, 32768)\nstate.set_scalar('ram_70fa_word', u16(state.scalar('ram_70fa_word') - 1))\nreturn controls"}, '_equipment_available': {'signature': 'equipment, option', 'returns': '', 'flow': 'if option == 0:\n    return equipment.word(2) != 0\nif option == 1:\n    return equipment.word(0) != 0\nreturn equipment.word(4) != 0'}, '_choose_duel_equipment': {'signature': 'state, choice, equipment, controls', 'returns': '', 'flow': "choice = _live_table(state, choice)\nequipment = _live_table(state, equipment)\ncontrols.validate()\nwhile not _equipment_available(equipment, choice.word()):\n    choice.set_word(0, u16(choice.word() + 1))\n    if choice.word() >= 3:\n        choice.set_word(0, 0)\nselected = choice.word()\ndirection = low16(controls.command) & 12\nif direction:\n    delta = 1 if direction & 8 else 65535\n    while True:\n        selected = u16(selected + delta)\n        if negative_word(selected):\n            selected = 2\n        elif selected >= 3:\n            selected = 0\n        if _equipment_available(equipment, selected):\n            break\n    if selected < 3:\n        choice.set_word(0, selected)\ncontrols = _first_controls(state, controls)\nif low16(controls.command) & 32:\n    return controls\nif low16(controls.command) & 12 or state.scalar('ram_7008_word') & 8:\n    append_duel_sprite(state, 200, u16(choice.word() * 56 + 104), 67, 32768)\nstate.set_scalar('ram_70fa_word', u16(state.scalar('ram_70fa_word') - 1))\nreturn controls"}, 'choose_first_duel_equipment': {'signature': 'state: SceneState, choice: Table, controls: DuelControlContext', 'returns': 'DuelControlContext', 'flow': 'return _choose_duel_equipment(state, choice, state.table(16740474), controls)'}, 'choose_second_duel_equipment': {'signature': 'state: SceneState, choice: Table, controls: DuelControlContext', 'returns': 'DuelControlContext', 'flow': 'return _choose_duel_equipment(state, choice, state.table(16740554), controls)'}, 'choose_duel_action_menu': {'signature': 'state: SceneState, controls: DuelControlContext', 'returns': 'DuelControlContext', 'flow': "controls.validate()\nsecond = negative_word(state.scalar('ram_7018_word'))\nactor = state.table(16740512 if second else 16740432)\nrestricted = actor.word(26) == actor.word(32)\nif not restricted:\n    selected = state.scalar('ram_7018_word')\n    direction = low16(controls.command) & 15\n    if direction:\n        if direction & 8:\n            delta = 1\n        elif direction & 4:\n            delta = 65535\n        elif direction & 2:\n            delta = 2\n        else:\n            delta = 65534\n        selected = u16(selected & 65280 | u8(selected + delta))\n        if low8(selected) < 4:\n            state.set_scalar('ram_7018_word', selected)\n    controls = _first_controls(state, controls)\n    if low16(controls.command) & 32:\n        return controls\n    if low16(controls.command) & 15 or state.scalar('ram_7008_word') & 8:\n        x = u16((state.scalar('ram_7018_word') & 2) * 12 + 176)\n        y = u16((state.scalar('ram_7018_word') & 1) * 48 + 136)\n        append_duel_sprite(state, x, y, 67, 32768)\nelse:\n    selected = state.scalar('ram_7019_byte')\n    if low16(controls.command) & 8:\n        selected = u16(selected + 1)\n        if selected == 2:\n            selected = u16(selected + 1)\n        if selected >= 4:\n            selected = 0\n    if low16(controls.command) & 4:\n        if selected == 3:\n            selected = u16(selected - 1)\n        selected = u16(selected - 1)\n        if negative_word(selected):\n            selected = 3\n    state.set_scalar('ram_7019_byte', low8(selected))\n    controls = _first_controls(state, controls)\n    if low16(controls.command) & 32:\n        return controls\n    if low16(controls.command) & 15 or state.scalar('ram_7008_word') & 8:\n        index = state.scalar('ram_7018_word') & 3\n        y = state.table(163854).byte(index)\n        append_duel_sprite(state, 200, y, 67, 32768)\nstate.set_scalar('ram_70fa_word', u16(state.scalar('ram_70fa_word') - 1))\nreturn controls"}, 'decode_duel_byte_lanes': {'signature': 'state: SceneState, source: Cursor, destination: Cursor, length: Word, repeat_value: Long=0, pair_value: Long=0, *, length_carrier: Long | None=None, count_carrier: Long | None=None, stack: Cursor | None=None', 'returns': 'DuelLaneResult', 'flow': "source = _live_cursor(state, source)\ndestination = _live_cursor(state, destination)\nlength = uint(length, 16, 'length')\nsaved_address = destination.address()\nif stack is not None:\n    stack = _live_cursor(state, stack)\n    if length_carrier is None or count_carrier is None:\n        raise ValueError('complete lane save requires actual current values')\n    _push_actor_longs(stack, (length_carrier, saved_address))\nresult = decode_duel_byte_lane(state, source, destination, length, repeat_value, pair_value, length_carrier=length_carrier, count_carrier=count_carrier)\nif stack is not None:\n    length_carrier, saved_address = _pop_actor_longs(stack, 2)\n    length = low16(length_carrier)\nreturn decode_duel_byte_lane(state, result.source, state.table(saved_address + 1).cursor(), length, result.repeat_value, result.pair_value, length_carrier=length_carrier, count_carrier=result.count_carrier)"}, 'decode_duel_byte_lane': {'signature': 'state: SceneState, source: Cursor, destination: Cursor, length: Word, repeat_value: Long=0, pair_value: Long=0, *, length_carrier: Long | None=None, count_carrier: Long | None=None', 'returns': 'DuelLaneResult', 'flow': "source = _live_cursor(state, source)\ndestination = _live_cursor(state, destination)\nremaining = uint(length, 16, 'length')\nrepeat_value = uint(repeat_value, 32, 'repeat value')\npair_value = uint(pair_value, 32, 'pair value')\nif length_carrier is not None:\n    uint(length_carrier, 32)\n    if low16(length_carrier) != length:\n        raise ValueError('lane length must agree with actual caller')\nif count_carrier is not None:\n    uint(count_carrier, 32)\nwhile remaining != 0:\n    token = source.next_byte()\n    if token < 128:\n        count = token\n        for _ in range(count + 1):\n            destination.set_byte(0, source.next_byte())\n            destination = destination.advance(2)\n            remaining = u16(remaining - 1)\n    elif not token & 64:\n        count = token & 63\n        repeat_value = replace_byte(repeat_value, source.next_byte())\n        for _ in range(count + 1):\n            destination.set_byte(0, low8(repeat_value))\n            destination = destination.advance(2)\n            remaining = u16(remaining - 1)\n    elif not token & 32:\n        count = token & 31\n        repeat_value = replace_byte(repeat_value, source.next_byte())\n        pair_value = replace_byte(pair_value, source.next_byte())\n        for _ in range(count + 1):\n            destination.set_byte(0, low8(repeat_value))\n            destination = destination.advance(2)\n            destination.set_byte(0, low8(pair_value))\n            destination = destination.advance(2)\n            remaining = u16(remaining - 2)\n    else:\n        count = token & 31\n        repeat_value = replace_byte(repeat_value, source.next_byte())\n        for _ in range(count + 1):\n            destination.set_byte(0, low8(repeat_value))\n            destination = destination.advance(2)\n            remaining = u16(remaining - 1)\n            repeat_value = replace_word(repeat_value, u16(low16(repeat_value) + 1))\n    if count_carrier is not None:\n        count_carrier = replace_word(count_carrier, 65535)\nif length_carrier is not None:\n    length_carrier = replace_word(length_carrier, remaining)\nreturn DuelLaneResult(source, destination, remaining, repeat_value, pair_value, length_carrier, count_carrier)"}, 'choose_duel_status_text': {'signature': 'state: SceneState, selection: Word, retained: Long=0', 'returns': 'Long', 'flow': "selection = uint(selection, 16, 'selection')\nretained = uint(retained, 32, 'retained text selection')\ndisplacement = u16(selection << 2)\npointer = state.table(164416).long(displacement)\nstate.set_scalar('ram_700e_long', pointer)\nstate.set_scalar('ram_700c_word', 50688)\nreturn replace_word(retained, displacement)"}, 'scan_duel_thresholds': {'signature': 'state: SceneState, value: Word, thresholds: Cursor', 'returns': 'Word', 'flow': "value = uint(value, 16, 'value')\nthresholds = _live_cursor(state, thresholds)\noffset = 65534\nwhile True:\n    offset = u16(offset + 2)\n    threshold = thresholds.next_word()\n    if value < threshold:\n        return offset"}, 'append_duel_sprite': {'signature': 'state: SceneState, x: Word, y: Word, pattern: Word, attributes: Word, frame: DuelActorFrame | None=None, stack: Cursor | None=None', 'returns': 'DuelSpriteResult', 'flow': "x = uint(x, 16, 'x')\ny = uint(y, 16, 'y')\npattern = uint(pattern, 16, 'pattern')\nattributes = uint(attributes, 16, 'attributes')\ncurrent = DuelActorFrame() if frame is None else frame\nstack = _actor_stack(state, current, stack)\nfor value, supplied in ((current.command, x), (current.comparison, y), (current.distance, pattern), (current.factor, attributes)):\n    if value is not None and low16(value) != supplied:\n        raise ValueError('sprite arguments must agree with the current partial values')\n_push_actor_longs(stack, (current.command, current.comparison, current.distance, current.factor))\ndestination = state.table(state.scalar('ram_7002_long')).cursor()\ntemplate = state.table(state.table(167992).long(u16(pattern << 2))).cursor()\nnext_sprite = state.scalar('ram_7000_word')\nif destination.address() != 4294965248:\n    destination.set_byte(0, low8(next_sprite), displacement=-5)\nnext_sprite = u16(next_sprite + 1)\nflip = attributes & 6144\nflip_value = _actor_word(current.weapon_difference, flip)\nanimation_value = current.variation\nattributes &= 59391\nextent = 0\nwhile True:\n    vertical_delta = template.byte(2)\n    animation_value = _actor_byte(animation_value, vertical_delta)\n    animation_value = _actor_word(animation_value, u16(s8(vertical_delta)))\n    vertical = u16(s8(vertical_delta) + x + 128)\n    animation_value = _actor_word(animation_value, vertical)\n    destination.append_word(vertical)\n    size_byte = template.byte(1)\n    animation_value = _actor_byte(animation_value, size_byte)\n    animation_value = _actor_word(animation_value, u16(low16(animation_value) << 8)) if animation_value is not None else None\n    size = u16(size_byte << 8) | next_sprite\n    animation_value = _actor_word(animation_value, size)\n    next_sprite = u16(next_sprite + 1)\n    destination.append_word(size)\n    extent = u16((s16(size) >> 7 & 24) + 8)\n    animation_value = _actor_word(animation_value, extent)\n    tile_word = u16(template.word(4) + attributes) ^ flip\n    animation_value = _actor_word(animation_value, tile_word)\n    destination.append_word(tile_word)\n    position_byte = template.byte(3)\n    animation_value = _actor_byte(animation_value, position_byte)\n    position = u16(s8(position_byte))\n    animation_value = _actor_word(animation_value, position)\n    if flip & 2048:\n        position = u16(-position)\n        animation_value = _actor_word(animation_value, position)\n        position = u16(position - extent)\n        animation_value = _actor_word(animation_value, position)\n    horizontal = u16(position + y + 128)\n    animation_value = _actor_word(animation_value, horizontal)\n    destination.append_word(horizontal)\n    template = template.advance(6)\n    if template.byte(0, displacement=-6) & 128:\n        break\ndestination.set_byte(0, 0, displacement=-5)\nstate.set_scalar('ram_7002_long', destination.address())\nnext_sprite = u16(next_sprite - 1)\nstate.set_scalar('ram_7000_word', next_sprite)\nsaved = (current.command, current.comparison, current.distance, current.factor)\nif stack is not None:\n    saved = _pop_actor_longs(stack, 4)\nreturned = _actor_reframe(current, saved[0], saved[1], saved[2], saved[3], flip_value, animation_value, working_value=_actor_word(current.working_value, extent)).validate()\nreturn DuelSpriteResult(destination, next_sprite, extent, returned, stack, template)"}, 'measure_duel_weapon_contact': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: DuelActorFrame | None=None', 'returns': 'DuelContact', 'flow': "actor = _live_table(state, actor)\nopponent = _live_table(state, opponent)\ncurrent = DuelActorFrame() if frame is None else frame\nif type(current) is not DuelActorFrame:\n    raise ValueError('actual contact frame required')\ncurrent.validate()\nmode_offset = u16(actor.word(12) << 1)\nreach = state.table(172640).word(mode_offset)\nif not actor.byte(24) & 8:\n    reach = u16(-reach)\nrelative = u16(reach + actor.word(14) - opponent.word(14))\nmagnitude = u16(-relative) if negative_word(relative) else relative\nfacing_relative = u16(-relative) if actor.byte(24) & 8 else relative\nlimit = state.table(172646).word(mode_offset)\ndistance = u16(magnitude - limit)\nreturned = _actor_reframe(current, current.command, _actor_word(current.comparison, mode_offset), _actor_word(current.distance, distance), _actor_word(current.factor, facing_relative), current.weapon_difference, current.variation).validate()\nreturn DuelContact(distance, facing_relative, magnitude < limit, returned)"}, '_ai_frame': {'signature': 'frame, command=None, comparison=None, distance=None, factor=None, variation=None', 'returns': '', 'flow': 'return _actor_reframe(frame, frame.command if command is None else command, frame.comparison if comparison is None else comparison, frame.distance if distance is None else distance, frame.factor if factor is None else factor, frame.weapon_difference, frame.variation if variation is None else variation).validate()'}, '_duel_observed_move': {'signature': 'frame, value, width', 'returns': '', 'flow': 'masked = value & (1 << width) - 1\nreturn replace(frame, conditions=DuelConditionObservation(False, masked == 0, bool(masked & 1 << width - 1), False))'}, '_duel_observed_comparison': {'signature': 'frame, left, right, width', 'returns': '', 'flow': 'mask = (1 << width) - 1\nleft, right = (left & mask, right & mask)\ndifference = left - right & mask\nsign = 1 << width - 1\nreturn replace(frame, conditions=DuelConditionObservation(left < right, difference == 0, bool(difference & sign), bool((left ^ right) & (left ^ difference) & sign)))'}, '_duel_call_frame': {'signature': 'state, function, frame, *args', 'returns': '', 'flow': 'checked_duel_turn(frame, state)\ncalled = replace(frame, stack=frame.stack.advance(-4))\nreturned = checked_duel_turn(function(state, *args, called), state)\nreturn replace(returned, stack=returned.stack.advance(4))'}, '_duel_enter_actor_call': {'signature': 'stack', 'returns': '', 'flow': 'if stack is not None:\n    stack.base = u32(stack.base - 4)'}, '_duel_leave_actor_call': {'signature': 'stack', 'returns': '', 'flow': 'if stack is not None:\n    stack.base = u32(stack.base + 4)'}, '_duel_complete_controls': {'signature': 'state, second, frame', 'returns': '', 'flow': "checked_duel_turn(frame, state)\nif type(second) is not bool:\n    raise ValueError('actual input side required')\nreturned = _second_controls(state, DuelControlContext(frame.command, frame.comparison)) if second else _first_controls(state, DuelControlContext(frame.command, frame.comparison))\nreturn replace(frame, command=returned.command, comparison=returned.mode, conditions=DuelConditionObservation(None, None, None, None))"}, 'clear_duel_text_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnFrame', 'flow': 'checked_duel_turn(frame, state)\nfields = clear_duel_text_plane(state, _turn_actor_values(frame))\ncurrent = _turn_from_actor(state, frame, fields, frame.actor, frame.opponent, frame.stack)\nreturn _duel_observed_move(current, 286331153, 32)'}, 'update_duel_actor_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnFrame', 'flow': 'checked_duel_turn(frame, state)\nvalues = _turn_actor_values(frame)\nresult = update_duel_actor(state, frame.actor, frame.opponent, DuelActorContext(frame.command, frame.comparison, frame.distance, values.retained, frame.stack, frame))\nreturn _turn_from_actor(state, frame, result.frame, result.actor, result.opponent, result.stack)'}, 'refresh_duel_actors_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnFrame', 'flow': 'checked_duel_turn(frame, state)\nresult = refresh_duel_actors(state, _turn_actor_values(frame), frame.stack, frame.actor, frame.opponent)\nreturn _turn_from_actor(state, frame, result.frame, result.actor, result.opponent, result.stack)'}, 'choose_duel_ai_command_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnFrame', 'flow': "checked_duel_turn(frame, state)\nvalues = _turn_actor_values(frame)\nresult = choose_duel_ai_command(state, frame.actor, frame.opponent, DuelAIContext(frame.command, frame.comparison, low16(frame.response), low16(frame.variation), values.retained, frame.response, frame))\nif result.live is None:\n    raise Boundary('full AI call omitted its actual live return')\nreturn checked_duel_turn(result.live, state)"}, 'choose_duel_status_text_complete': {'signature': 'state: SceneState, selection: Word, frame: DuelTurnFrame', 'returns': 'DuelTurnFrame', 'flow': "checked_duel_turn(frame, state)\nselection = uint(selection, 16, 'actual status selection')\ncommand = choose_duel_status_text(state, selection, frame.command)\ncurrent = replace(frame, command=command, lookup=state.table(164416))\nreturn _duel_observed_move(current, 50688, 16)"}, 'show_active_duel_turn_label_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnFrame', 'flow': "checked_duel_turn(frame, state)\nsource = state.table(164256).cursor()\ndistance = replace_word(frame.distance, 60424)\nobserved_tick = state.scalar('ram_7008_word')\nif observed_tick & 1:\n    source = state.table(164278).cursor()\n    distance = replace_word(distance, 60484)\ncurrent = _duel_observed_move(replace(frame, command=1610612740, comparison=replace_word(frame.comparison, 1), distance=distance, actor=source), 1, 16)\nreturn checked_duel_turn(state.service_at(158714, current), state)"}, 'wait_active_duel_action_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnFrame', 'flow': "current = checked_duel_turn(frame, state)\nwhile True:\n    _duel_frame(state)\n    state.set_scalar('ram_70fa_word', u16(state.scalar('ram_70fa_word') - 1))\n    current = _duel_call_frame(state, refresh_duel_actors_complete, current)\n    text = state.scalar('ram_700c_word')\n    current = _duel_observed_move(current, text, 16)\n    if text != 0:\n        continue\n    current = _duel_call_frame(state, _duel_complete_controls, current, False)\n    side = state.scalar('ram_7018_word')\n    current = _duel_observed_move(current, side, 16)\n    if negative_word(side):\n        current = _duel_call_frame(state, _duel_complete_controls, current, True)\n    command = replace_word(current.command, low16(current.command) & 112)\n    current = _duel_observed_move(replace(current, command=command), command, 16)\n    if low16(command) != 0:\n        state.set_status_word(9984)\n        return current"}, 'wait_either_duel_action_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnFrame', 'flow': "current = checked_duel_turn(frame, state)\nif state.scalar('ram_700a_byte') == 3:\n    return wait_active_duel_action_complete(state, current)\nif state.scalar('ram_700b_byte') == 3:\n    return wait_active_duel_action_complete(state, current)\nwhile True:\n    _duel_frame(state)\n    state.set_scalar('ram_70fa_word', u16(state.scalar('ram_70fa_word') - 1))\n    current = _duel_call_frame(state, refresh_duel_actors_complete, current)\n    text = state.scalar('ram_700c_word')\n    current = _duel_observed_move(current, text, 16)\n    if text != 0:\n        continue\n    current = _duel_call_frame(state, _duel_complete_controls, current, False)\n    comparison = replace_word(current.comparison, low16(current.command))\n    saved = current.stack.advance(-4)\n    saved.set_long(0, comparison)\n    current = replace(current, comparison=comparison, stack=saved)\n    current = _duel_call_frame(state, _duel_complete_controls, current, True)\n    comparison = current.stack.next_long()\n    command = replace_word(current.command, (low16(current.command) | low16(comparison)) & 112)\n    current = _duel_observed_move(replace(current, comparison=comparison, command=command), command, 16)\n    if low16(command) != 0:\n        state.set_status_word(9984)\n        return current"}, '_ai_random': {'signature': 'state, frame, mask', 'returns': '', 'flow': 'from .business_reuse import _reuse_advance_random_pair\nrandom = _reuse_advance_random_pair(state)\nreturn _ai_frame(frame, command=replace_word(random.sample, low16(random.sample) & mask), comparison=random.updated_state)'}, '_ai_override_result': {'signature': 'frame, override', 'returns': '', 'flow': 'return DuelOverrideResult(_ai_frame(frame, variation=_actor_word(frame.variation, override)), override).validate()'}, 'sample_duel_probability': {'signature': 'state: SceneState, source_word: Word, frame: DuelActorFrame | None=None', 'returns': 'DuelProbability', 'flow': "source_word = uint(source_word, 16, 'probability word')\ncurrent = DuelActorFrame() if frame is None else frame\nif type(current) is not DuelActorFrame:\n    raise ValueError('actual probability frame required')\ncurrent.validate()\nmask = source_word & 7\nthreshold = source_word >> 4\ncurrent = _ai_frame(current, distance=_actor_word(current.distance, mask), factor=_actor_word(current.factor, threshold))\ncurrent = _ai_random(state, current, mask)\nreturn DuelProbability(current.command, mask, threshold, low16(current.command) < threshold, current)"}, 'choose_duel_ai_timeout': {'signature': 'state: SceneState, actor: Table, opponent: Table, command: Long, override: Word, frame: DuelActorFrame | None=None', 'returns': 'DuelAIResult', 'flow': "actor = _live_table(state, actor)\nopponent = _live_table(state, opponent)\ncommand = uint(command, 32, 'command')\noverride = uint(override, 16, 'override')\ncurrent = DuelActorFrame(command) if frame is None else frame\nif type(current) is not DuelActorFrame:\n    raise ValueError('actual timeout frame required')\ncurrent.validate()\nif current.command != command:\n    raise ValueError('timeout command must be the current frame command')\nif state.scalar('ram_70fa_word') > 6144:\n    if state.scalar('ram_700a_word') == 771:\n        readiness = actor.word(28)\n        current = _ai_frame(current, command=replace_word(command, readiness))\n        if readiness <= opponent.word(28):\n            override = 67\n            current = _ai_frame(current, variation=_actor_word(current.variation, override))\n            return DuelAIResult(current.command, current.comparison if current.comparison is not None else 0, 0, override, current.retained, current if frame is not None else None)\ncurrent = _ai_frame(current, command=0)\nreturn DuelAIResult(0, current.comparison if current.comparison is not None else 0, 0, override, current.retained, current if frame is not None else None)"}, '_copy_duel_palette': {'signature': 'state, source_base, destination_base', 'returns': '', 'flow': 'source = state.table(source_base).cursor()\ndestination = state.table(destination_base).cursor()\nfor _ in range(8):\n    destination.append_word(source.next_word())\nreturn source'}, 'update_duel_actor': {'signature': 'state: SceneState, actor: Table, opponent: Table, context: DuelActorContext=DuelActorContext()', 'returns': 'DuelActorResult', 'flow': "actor = _live_table(state, actor)\nopponent = _live_table(state, opponent)\ncurrent = _actor_input_frame(context)\nstack = _actor_stack(state, current, context.stack)\nfactor, flip_value, variation = (current.factor, current.weapon_difference, current.variation)\nfor offset in (8, 10, 38, 40):\n    if actor.word(offset) != 0:\n        actor.set_word(offset, u16(actor.word(offset) - 1))\nflash_time = actor.word(40)\ncomparison = replace_word(context.comparison, flash_time)\nif flash_time != 0:\n    source = 163968 if actor.address() == 16740432 else 164000\n    destination = 4294966016 if actor.address() == 16740432 else 4294966048\n    comparison = replace_word(comparison, flash_time & 1)\n    if not flash_time & 1:\n        source = 164112\n    current = replace(current, lookup=_copy_duel_palette(state, source, destination))\n    variation = _actor_word(variation, 65535)\ncommand = replace_word(context.command, actor.word())\ndamage = context.damage\nadvance_attack = False\nif not negative_word(actor.word(2)):\n    direction = 0\n    comparison = replace_word(comparison, 0)\n    if not low16(command) & 256:\n        direction = 1\n        if low16(command) & 512:\n            direction = 2\n    actor.set_byte(3, direction)\n    comparison = replace_word(comparison, direction)\n    if low16(command) & 16:\n        actor.set_byte(2, actor.byte(2) | 128)\n        actor.set_byte(2, actor.byte(2) & 191)\n        actor.set_word(4, 0)\n        actor.set_word(8, actor.word(22))\n    else:\n        actor.set_word(2, actor.word(2) & 16383)\n        if low16(command) & 8192:\n            actor.set_byte(2, actor.byte(2) | 64)\nelse:\n    command = replace_word(command, actor.word(4))\n    if actor.word(8) == 0:\n        if low16(command) == 4:\n            contact = measure_duel_weapon_contact(state, actor, opponent, _actor_reframe(current, command, comparison, damage, factor, flip_value, variation))\n            comparison, damage, factor = (contact.frame.comparison, contact.frame.distance, contact.frame.factor)\n            if contact.borrowed:\n                if opponent.byte(2) & 64:\n                    comparison = replace_word(comparison, actor.word(2) & 3)\n                    opponent_kind = opponent.word(2) & 3\n                    damage = replace_word(damage, opponent_kind)\n                    if opponent_kind == low16(comparison):\n                        _push_actor_pair_words(stack, command, comparison)\n                        _sound(state, 160)\n                        command, comparison = _pop_actor_pair_words(stack, command, comparison)\n                    else:\n                        struck = _apply_duel_strike(state, actor, opponent, _actor_reframe(current, command, comparison, damage, factor, flip_value, variation), stack)\n                        command, comparison, damage = (struck.command, struck.comparison, struck.distance)\n                        factor, flip_value, variation = (struck.factor, struck.weapon_difference, struck.variation)\n                        current = replace(current, lookup=struck.lookup)\n                else:\n                    struck = _apply_duel_strike(state, actor, opponent, _actor_reframe(current, command, comparison, damage, factor, flip_value, variation), stack)\n                    command, comparison, damage = (struck.command, struck.comparison, struck.distance)\n                    factor, flip_value, variation = (struck.factor, struck.weapon_difference, struck.variation)\n                    current = replace(current, lookup=struck.lookup)\n        advance_attack = True\nif advance_attack:\n    actor.set_word(8, 4)\n    command = replace_word(command, u16(low16(command) + 1))\n    if low16(command) >= 5:\n        command = replace_word(command, 0)\n        actor.set_byte(2, actor.byte(2) & 127)\n    actor.set_word(4, low16(command))\nflash_time = actor.word(38)\ncommand = replace_word(command, flash_time)\nif flash_time != 0:\n    source = 163968 if actor.address() == 16740432 else 164000\n    destination = 4294966016 if actor.address() == 16740432 else 4294966048\n    glow = 1024 if actor.address() == 16740432 else 2048\n    comparison = replace_word(comparison, glow)\n    command = replace_word(command, flash_time & 1)\n    if not flash_time & 1:\n        source = 164096\n    actor.set_word(0, actor.word() & 62451 | glow)\n    current = replace(current, lookup=_copy_duel_palette(state, source, destination))\n    factor = _actor_word(factor, 65535)\nif actor.byte(2) & 16:\n    if actor.word(10) == 0:\n        actor.set_byte(2, actor.byte(2) & 239)\nelse:\n    command = replace_word(command, actor.word())\n    comparison = replace_word(comparison, low16(command))\n    requested = low16(command) & 12\n    command = replace_word(command, requested)\n    blocked = False\n    if requested:\n        facing = 4 if actor.byte(24) & 8 else 8\n        factor = _actor_word(factor, facing)\n        requested &= facing\n        command = replace_word(command, requested)\n        if requested:\n            current_tick = state.scalar('ram_7008_word') & 15\n            command = replace_word(command, current_tick)\n            if current_tick == 0:\n                actor.set_byte(2, actor.byte(2) | 16)\n                actor.set_word(10, 48)\n                blocked = True\n    if not blocked and low16(comparison) & 3072:\n        comparison = replace_word(comparison, low16(comparison) & 3072)\n        actor.set_byte(2, actor.byte(2) | 32)\n        position = actor.long(18)\n        motion_time = actor.word(40)\n        motion_time |= actor.word(38)\n        factor = _actor_word(factor, motion_time)\n        if motion_time != 0:\n            position = u32(position + 32768)\n        if not low16(comparison) & 2048:\n            position = u32(-position)\n        comparison = replace_word(comparison, low16(comparison) & 2048)\n        position = u32(position + actor.long(14))\n        separation = u32(position - opponent.long(14))\n        if negative_long(separation):\n            separation = u32(-separation)\n        comparison = swap_words(separation)\n        distance = high16(separation)\n        if 16 <= distance < 224:\n            actor.set_long(14, position)\n        damage = position\n    elif not blocked:\n        comparison = replace_word(comparison, low16(comparison) & 3072)\n_duel_enter_actor_call(stack)\nrendered = render_duel_actor(state, actor, opponent, _actor_reframe(current, command, comparison, damage, factor, flip_value, variation), stack)\n_duel_leave_actor_call(stack)\nresult = rendered.frame\nreturn DuelActorResult(result.command, result.comparison, result.distance, result, rendered.actor, rendered.opponent, rendered.stack, result.response).validate()"}, '_apply_duel_strike': {'signature': 'state, actor, opponent, frame, stack', 'returns': '', 'flow': '_push_actor_pair_words(stack, frame.command, frame.comparison)\n_sound(state, 167)\nopponent.set_word(38, 60)\nrolled = low16(_random(state)) & 7\nif rolled >= 6:\n    rolled = u16(rolled - 4)\nattribute = actor.word(30)\nthresholds = state.table(167218).cursor()\noffset = scan_duel_thresholds(state, attribute, thresholds)\ndamage = u16(rolled + state.table(167230).word(offset))\nstrength = actor.word(30)\nweapon = actor.word(12)\nif weapon == 0:\n    equipment_index = u16(actor.word(44) << 1)\n    strength = u16(strength + state.table(167242).word(equipment_index))\nelif weapon <= 1:\n    equipment_index = u16(actor.word(42) << 1)\n    strength = u16(strength + state.table(167250).word(equipment_index))\nelse:\n    equipment_index = u16(actor.word(46) << 1)\n    strength = u16(strength + state.table(167258).word(equipment_index))\nproduct = u32(damage * strength)\nkind = u16((actor.word(2) & 3) << 1)\ndivisor = state.table(167278).word(kind)\ndamage = divu_retained(product, divisor)\ncommand, comparison = _pop_actor_pair_words(stack, frame.command, frame.comparison)\nif actor.word(28) != 0:\n    remaining = u16(opponent.word(28) - low16(damage))\n    opponent.set_word(28, remaining)\n    if negative_word(remaining):\n        opponent.set_word(28, 0)\nreturn _actor_reframe(frame, command, comparison, _actor_word(frame.distance, kind), frame.factor, frame.weapon_difference, damage, lookup=thresholds).validate()'}, 'render_duel_actor': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: DuelActorFrame | None=None, stack: Cursor | None=None', 'returns': 'DuelRenderResult', 'flow': "actor = _live_table(state, actor)\nopponent = _live_table(state, opponent)\ncurrent = DuelActorFrame() if frame is None else frame\nstack = _actor_stack(state, current, stack)\nif actor.byte(2) & 8:\n    return DuelRenderResult(current, actor, opponent, stack).validate(state)\nif actor.word(28) == 0:\n    _push_actor_longs(stack, (current.command, current.comparison, current.distance, current.factor, actor.base, opponent.base))\n    mode = actor.word(12)\n    pattern = state.table(167820).byte(mode)\n    attributes = actor.word(24)\n    y = u16(actor.word(14) - state.scalar('ram_7006_word'))\n    x = 84 if actor.byte(2) & 16 else 88\n    pose = _actor_reframe(current, _actor_word(current.command, x), _actor_word(current.comparison, y), _actor_word(current.distance, pattern), _actor_word(current.factor, attributes), current.weapon_difference, current.variation)\n    _duel_enter_actor_call(stack)\n    drawn = append_duel_sprite(state, x, y, pattern, attributes, pose, stack)\n    _duel_leave_actor_call(stack)\n    saved = (current.command, current.comparison, current.distance, current.factor, actor.base, opponent.base)\n    if stack is not None:\n        saved = _pop_actor_longs(stack, 6)\n    actor, opponent = (state.table(saved[4]), state.table(saved[5]))\n    current = _actor_reframe(current, saved[0], saved[1], saved[2], saved[3], drawn.frame.weapon_difference, drawn.frame.variation, working_value=drawn.frame.working_value, lookup=drawn.frame.lookup)\nelse:\n    mode_product = u32(actor.word(12) * 18)\n    mode_offset = low16(mode_product)\n    variation = mode_product\n    direction_product = u32(actor.byte(3) * 6)\n    pose = u16(direction_product + mode_offset)\n    distance_value = replace_word(direction_product, pose)\n    animation = actor.word(4)\n    if actor.byte(2) & 64:\n        animation = 5\n    variation = replace_word(variation, animation)\n    pose = u16(pose + animation)\n    distance_value = replace_word(distance_value, pose)\n    x = 84 if actor.byte(2) & 16 else 88\n    y = u16(actor.word(14) - state.scalar('ram_7006_word'))\n    attributes = actor.word(24)\n    pose_frame = _actor_reframe(current, _actor_word(current.command, x), _actor_word(current.comparison, y), distance_value, _actor_word(current.factor, attributes), current.weapon_difference, variation)\n    _push_actor_longs(stack, (actor.base, opponent.base))\n    _duel_enter_actor_call(stack)\n    drawn = append_duel_sprite(state, x, y, pose, attributes, pose_frame, stack)\n    _duel_leave_actor_call(stack)\n    if stack is not None:\n        actor_base, opponent_base = _pop_actor_longs(stack, 2)\n        actor, opponent = (state.table(actor_base), state.table(opponent_base))\n    current = drawn.frame\nreturn _render_duel_movement_overlay(state, actor, opponent, current, stack)"}, '_render_duel_movement_overlay': {'signature': 'state, actor, opponent, frame, stack', 'returns': '', 'flow': "if not actor.byte(2) & 32:\n    return DuelRenderResult(frame, actor, opponent, stack).validate(state)\ncommand, comparison = (frame.command, frame.comparison)\nif actor.word(10) == 0:\n    actor.set_word(10, 10)\n    animation = u16(actor.word(6) + 1)\n    if animation >= 5:\n        animation = 1\n        movement_bits = actor.word() & 3072\n        comparison = _actor_word(comparison, movement_bits)\n        if movement_bits == 0:\n            actor.set_byte(2, actor.byte(2) & 223)\n            animation = 0\n    actor.set_word(6, animation)\n    command = _actor_word(command, animation)\ny = u16(actor.word(14) - state.scalar('ram_7006_word'))\npattern = 62 if actor.word(12) == 0 else 54\npattern = u16(pattern + actor.word(6))\nif actor.byte(2) & 16:\n    pattern = u16((state.scalar('ram_7008_word') >> 4 & 1) + 60)\nattributes = actor.word(24)\noverlay = _actor_reframe(frame, _actor_word(command, 88), _actor_word(comparison, y), _actor_word(frame.distance, pattern), _actor_word(frame.factor, attributes), frame.weapon_difference, frame.variation)\n_push_actor_longs(stack, (actor.base,))\n_duel_enter_actor_call(stack)\ndrawn = append_duel_sprite(state, 88, y, pattern, attributes, overlay, stack)\n_duel_leave_actor_call(stack)\nif stack is not None:\n    actor = state.table(_pop_actor_longs(stack, 1)[0])\nreturn DuelRenderResult(drawn.frame, actor, drawn.source, stack).validate(state)"}, 'choose_duel_ai_override': {'signature': 'state: SceneState, actor: Table, opponent: Table, threshold_offset: Word, frame: DuelActorFrame | None=None', 'returns': 'Word | DuelOverrideResult', 'flow': 'current = DuelActorFrame() if frame is None else frame\nresult = _choose_duel_ai_override_current(state, actor, opponent, threshold_offset, current)\nreturn result.override if frame is None else result'}, '_choose_duel_ai_override_current': {'signature': 'state, actor, opponent, threshold_offset, frame', 'returns': '', 'flow': "actor = _live_table(state, actor)\nopponent = _live_table(state, opponent)\nthreshold_offset = uint(threshold_offset, 16, 'threshold offset')\nif type(frame) is not DuelActorFrame:\n    raise ValueError('actual override frame required')\nframe.validate()\ntick = state.scalar('ram_7008_word') & 7\ncurrent = _ai_frame(frame, comparison=_actor_word(frame.comparison, tick), variation=_actor_word(frame.variation, 0))\nif tick:\n    return _ai_override_result(current, 0)\nif actor.base == 16740432:\n    opponent_readiness = opponent.word(28)\n    if opponent_readiness < 51:\n        current = _ai_random(state, current, 1)\n        if low16(current.command) == 0:\n            return _ai_override_result(current, 64)\n    else:\n        current = _ai_random(state, current, 3)\n        return _ai_override_result(current, 64 if low16(current.command) == 0 else 0)\n    opponent_strength = opponent.word(30)\n    current = _ai_frame(current, distance=_actor_word(current.distance, opponent_strength))\n    own_strength = actor.word(30)\n    current = _ai_frame(current, factor=_actor_word(current.factor, own_strength))\n    readiness = actor.word(28)\n    current = _ai_frame(current, comparison=_actor_word(current.comparison, readiness))\n    if readiness < 40:\n        current = _ai_random(state, current, 3)\n        return _ai_override_result(current, 67 if low16(current.command) else 0)\n    if readiness >= 70:\n        if opponent_strength >= own_strength:\n            current = _ai_random(state, current, 1)\n            return _ai_override_result(current, 67 if low16(current.command) else 0)\n        current = _ai_random(state, current, 3)\n        return _ai_override_result(current, 67 if low16(current.command) == 0 else 0)\n    if opponent_strength < own_strength:\n        current = _ai_random(state, current, 1)\n    else:\n        current = _ai_random(state, current, 3)\n    return _ai_override_result(current, 67 if low16(current.command) else 0)\nopponent_readiness = opponent.word(28)\ncurrent = _ai_frame(current, distance=_actor_word(current.distance, opponent_readiness))\nreadiness = actor.word(28)\ncurrent = _ai_frame(current, factor=_actor_word(current.factor, readiness))\nif opponent_readiness < readiness:\n    sampled = sample_duel_probability(state, state.table(174562).word(threshold_offset), current)\n    current = sampled.frame\n    if sampled.borrowed:\n        return _ai_override_result(current, 64)\n    sampled = sample_duel_probability(state, state.table(174574).word(threshold_offset), current)\n    return _ai_override_result(sampled.frame, 33 if sampled.borrowed else 0)\nif readiness >= 80:\n    return _ai_override_result(current, 0)\nif readiness >= 50:\n    opponent_strength = opponent.word(30)\n    current = _ai_frame(current, distance=_actor_word(current.distance, opponent_strength))\n    own_strength = actor.word(30)\n    current = _ai_frame(current, factor=_actor_word(current.factor, own_strength))\n    first_source = 173748 if opponent_strength >= own_strength else 173810\n    sampled = sample_duel_probability(state, state.table(first_source).word(threshold_offset), current)\n    current = sampled.frame\n    if sampled.borrowed:\n        return _ai_override_result(current, 67)\n    sampled = sample_duel_probability(state, state.table(173760).word(threshold_offset), current)\n    return _ai_override_result(sampled.frame, 64 if sampled.borrowed else 0)\nopponent_strength = opponent.word(30)\ncurrent = _ai_frame(current, command=_actor_word(current.command, opponent_strength))\nthresholds = state.table(172808).cursor()\nopponent_offset = scan_duel_thresholds(state, opponent_strength, thresholds)\ncurrent = replace(current, lookup=thresholds)\ncurrent = _ai_frame(current, comparison=_actor_word(current.comparison, opponent_offset))\nif opponent_offset < 4:\n    source = 174370\nelif opponent_offset < 8:\n    source = 174204\nelif opponent_offset == 8:\n    source = 174040\nelse:\n    source = 173868\nsampled = _sample_duel_live_mode_values(state, source, threshold_offset, False, current)\ncurrent = sampled.frame\nif sampled.borrowed:\n    return _ai_override_result(current, 67)\nsampled = _sample_duel_live_mode_values(state, source, threshold_offset, True, current)\nreturn _ai_override_result(sampled.frame, 66 if sampled.borrowed else 0)"}, '_sample_duel_live_mode_pair': {'signature': 'state, source, threshold_offset, second', 'returns': '', 'flow': 'return _sample_duel_live_mode_values(state, source, threshold_offset, second, DuelActorFrame()).borrowed'}, '_sample_duel_live_mode_values': {'signature': 'state, source, threshold_offset, second, frame', 'returns': '', 'flow': "if source == 174040:\n    base = 174132\nelif source == 174204:\n    base = 174298\nelif source == 174370:\n    base = 174464\nelse:\n    base = 173962\nif state.scalar('ram_efd2_word') == 0:\n    offset = 0\nelse:\n    offset = 48 if state.scalar('ram_efd2_word') == 2 else 24\nif second:\n    offset += 12\nsource_word = state.table(u32(base + offset)).word(threshold_offset)\nreturn sample_duel_probability(state, source_word, frame)"}, '_ai_observed_result': {'signature': 'frame, response, threshold_offset, override, live=None', 'returns': '', 'flow': 'frame = replace(frame, response=response)\nactual_override = low16(frame.variation) if frame.variation is not None else override\nreturned_live = None\nif live is not None:\n    returned_live = _turn_from_actor(live.actor.state, live, frame, live.actor, live.opponent, live.stack)\nreturn DuelAIResult(frame.command, frame.comparison, threshold_offset, actual_override, frame.retained, frame, response, returned_live).validate()'}, '_ai_rule_frame': {'signature': 'state, actor, opponent, frame, threshold_offset, target_address, live=None, tail=False', 'returns': '', 'flow': "if frame.retained is None:\n    raise Boundary('actual AI rule needs current six values, not a legacy WORD observation')\nsupplied = None\nif live is not None:\n    supplied = _turn_from_actor(state, live, frame, actor, opponent, live.stack)\n    if not tail:\n        supplied = replace(supplied, stack=supplied.stack.advance(-4))\nresult = state.service_at(target_address, DuelActionContext(actor, opponent, DuelControlContext(frame.command, frame.comparison), threshold_offset, frame.retained, live=supplied))\nif type(result) is not DuelActionResult:\n    raise Boundary('real AI rule must return the actual typed frame')\nresult.validate()\nif result.discarded_continuation is not None:\n    raise Boundary('ordinary AI rule returned an unexpected nonlocal continuation')\nif result.retained is None:\n    raise Boundary('AI rule omitted its actual retained return')\nif supplied is not None:\n    if result.live is None:\n        raise Boundary('complete AI rule omitted its current full return')\n    checked_duel_turn(result.live, state)\n    returned_live = result.live if tail else replace(result.live, stack=result.live.stack.advance(4))\n    return (_turn_actor_values(returned_live), returned_live)\nreturn (_actor_reframe(frame, result.controls.command, result.controls.mode, result.retained.distance, result.retained.factor, result.retained.weapon_difference, result.retained.variation).validate(), None)"}, 'choose_duel_ai_command': {'signature': 'state: SceneState, actor: Table, opponent: Table, context: DuelAIContext=DuelAIContext()', 'returns': 'DuelAIResult', 'flow': "actor = _live_table(state, actor)\nopponent = _live_table(state, opponent)\nif type(context) is not DuelAIContext:\n    raise ValueError('actual typed AI caller context required')\ncontext.validate()\ncommand = context.command\ncomparison = context.comparison\nthreshold_offset = context.threshold_offset\noverride = context.override\nretained = context.retained\nframe = DuelActorFrame(command, comparison, retained.distance if retained is not None else None, retained.factor if retained is not None else None, retained.weapon_difference if retained is not None else None, retained.variation if retained is not None else None)\nif context.live is not None:\n    checked_duel_turn(context.live, state)\n    full = _turn_actor_values(context.live)\n    if (full.command, full.comparison, full.retained, full.response) != (command, comparison, retained, context.response):\n        raise ValueError('AI must consume its actual full caller values')\n    frame = full\nresponse = context.response\nlive = context.live\nif actor.word(34) != 0:\n    actor.set_word(34, u16(actor.word(34) - 1))\nreadiness = actor.word(28)\ncommand = replace_word(command, readiness)\nframe = _ai_frame(frame, command=command)\nif readiness == 0:\n    actor.set_word(2, 0)\n    actor.set_word(4, 0)\n    return _ai_observed_result(frame, response, threshold_offset, override, live)\nopponent_readiness = opponent.word(28)\ncommand = replace_word(command, opponent_readiness)\nframe = _ai_frame(frame, command=command)\nif opponent_readiness == 0:\n    frame = _ai_frame(frame, command=replace_word(command, 256))\n    return _ai_observed_result(frame, response, threshold_offset, override, live)\nif actor.word(34) == 0:\n    frame = _ai_random(state, frame, 31)\n    frame = _ai_frame(frame, command=replace_word(frame.command, u16(low16(frame.command) + 30)))\n    actor.set_word(34, low16(frame.command))\n    attribute = actor.word(30)\n    frame = _ai_frame(frame, command=replace_word(frame.command, attribute))\n    thresholds = state.table(172808).cursor()\n    threshold_offset = scan_duel_thresholds(state, attribute, thresholds)\n    frame = replace(frame, lookup=thresholds)\n    frame = _ai_frame(frame, comparison=replace_word(frame.comparison, threshold_offset))\n    response = _actor_word(response, threshold_offset)\n    frame = replace(frame, response=response)\n    selected = choose_duel_ai_override(state, actor, opponent, threshold_offset, frame)\n    frame, override = (selected.frame, selected.override)\n    timed = choose_duel_ai_timeout(state, actor, opponent, frame.command, override, frame)\n    frame, override = (timed.frame, timed.override)\n    frame = _ai_frame(frame, command=replace_word(frame.command, override))\n    if override != 0:\n        return _ai_observed_result(frame, response, threshold_offset, override, live)\n    dispatch_offset = u16(threshold_offset << 1)\n    frame = _ai_frame(frame, comparison=replace_word(frame.comparison, dispatch_offset))\n    dispatch_address = u32(172820 + s16(dispatch_offset))\n    frame, live = _ai_rule_frame(state, actor, opponent, frame, threshold_offset, dispatch_address, live)\n    if live is not None:\n        actor, opponent, response = (live.actor, live.opponent, live.response)\naction = actor.word(36)\naction_offset = u16(action << 2)\nframe = _ai_frame(frame, command=replace_word(frame.command, action_offset))\ntarget_address = u32(172844 + s16(action_offset))\nframe, live = _ai_rule_frame(state, actor, opponent, frame, threshold_offset, target_address, live, True)\nif live is not None:\n    response = live.response\nreturn _ai_observed_result(frame, response, threshold_offset, override, live)"}, '_stage_duel_words': {'signature': 'state, source_base, command, rows, row_command', 'returns': '', 'flow': 'from .business_reuse import stage_sprite_word_packet\nreturn stage_sprite_word_packet(state, state.table(source_base).cursor(), command, rows, row_command)'}, '_configure_duel_dialog': {'signature': 'state, position, source', 'returns': '', 'flow': "state.set_scalar('ram_700c_word', position)\nstate.set_scalar('ram_700e_long', source)\nstate.set_scalar('ram_7014_word', 1)\nstate.set_scalar('ram_7016_word', 2)"}, '_choose_duel_ai_panel': {'signature': 'state, actor, opponent, controls, preparation=None', 'returns': '', 'flow': "if type(preparation) is not DuelPreparationContext:\n    raise Boundary('automatic panel requires actual post-refresh six values, response and live stack')\npreparation.validate(state)\nif actor is not preparation.actor or opponent is not preparation.opponent:\n    raise ValueError('panel must consume the actual caller actor views')\nif type(controls) is not DuelControlContext:\n    raise ValueError('actual current panel controls required')\ncontrols.validate()\nif (controls.command, controls.mode) != (preparation.frame.command, preparation.frame.comparison):\n    raise ValueError('panel controls must agree with current frame')\nattribute = actor.word(30)\nthresholds = state.table(162710).cursor()\nthreshold_offset = scan_duel_thresholds(state, attribute, thresholds)\npointer_offset = u16(threshold_offset << 1)\nhandler = state.table(162722).long(pointer_offset)\nframe = replace(preparation.frame, lookup=thresholds)\ncurrent = _actor_reframe(frame, replace_word(frame.command, attribute), replace_word(frame.comparison, pointer_offset), frame.distance, frame.factor, frame.weapon_difference, frame.variation)\nresult = state.service_at(handler, DuelPreparationContext(current, preparation.response, actor, opponent, preparation.stack))\nif type(result) is not DuelPreparationContext:\n    raise Boundary('live duel panel handler must return its typed completion')\nresult.validate(state)\nreturn result"}, '_choose_duel_side_loadout': {'signature': 'state, second, controls', 'returns': '', 'flow': "actor = state.table(16740512 if second else 16740432)\nopponent = state.table(16740432 if second else 16740512)\nmode_name = 'ram_700b_byte' if second else 'ram_700a_byte'\nchoice = state.table(16740524 if second else 16740444)\nequipment_choice = state.table(16740578 if second else 16740498)\nif state.scalar(mode_name) != 3:\n    _configure_duel_dialog(state, 50688, 166078)\n    if second:\n        state.set_scalar('ram_70da_word', 1)\n    advance_duel_entry_palette(state)\nwhile True:\n    _duel_frame(state)\n    advance_duel_entry_palette(state)\n    refresh_duel_actors(state)\n    if not second:\n        state.set_scalar('ram_708a_word', 0)\n    if state.scalar(mode_name) == 3:\n        raise Boundary('effects-only loadout cannot supply current panel values; use complete preparation continuation')\n    controls = _second_controls(state, controls) if second else _first_controls(state, controls)\n    controls = choose_second_duel_equipment(state, choice, controls) if second else choose_first_duel_equipment(state, choice, controls)\n    if state.scalar('ram_700c_word') != 0:\n        continue\n    _stage_duel_words(state, 164354 if second else 164332, 1610612740, 1, 60740 if second else 60680)\n    controls = _second_controls(state, controls) if second else _first_controls(state, controls)\n    controls = DuelControlContext(replace_word(controls.command, low16(controls.command) & 240), controls.mode)\n    if low16(controls.command) == 0:\n        continue\n    _sound(state, 172)\n    if state.scalar(mode_name) == 3:\n        break\n    clear_duel_text_plane(state)\n    _configure_duel_dialog(state, 50688, 166154)\n    while True:\n        _duel_frame(state)\n        advance_duel_entry_palette(state)\n        refresh_duel_actors(state)\n        controls = _second_controls(state, controls) if second else _first_controls(state, controls)\n        controls = choose_duel_two_option_menu(state, equipment_choice, controls)\n        if state.scalar('ram_700c_word') != 0:\n            continue\n        controls = _second_controls(state, controls) if second else _first_controls(state, controls)\n        controls = DuelControlContext(replace_word(controls.command, low16(controls.command) & 240), controls.mode)\n        if low16(controls.command) != 0:\n            break\n    _sound(state, 172)\n    if equipment_choice.word() != 0:\n        state.set_scalar(mode_name, 3)\n    break\nstate.set_status_word(9984)\nconfigure_duel_weapon_motion(state, actor)\nclear_duel_text_plane(state)\nreturn controls"}, '_wait_duel_status_text': {'signature': 'state, second, controls, preparation=None', 'returns': '', 'flow': "if preparation is not None:\n    return _wait_complete_status(state, second, preparation)\nif not second:\n    state.table(16740432).set_word(2, 0)\nelse:\n    state.table(16740512).set_word(2, 0)\nwhile True:\n    _duel_frame(state)\n    if not second:\n        advance_duel_entry_palette(state)\n    refresh_duel_actors(state)\n    if state.scalar('ram_700c_word') != 0:\n        continue\n    controls = _second_controls(state, controls) if second else _first_controls(state, controls)\n    controls = DuelControlContext(replace_word(controls.command, low16(controls.command) & 240), controls.mode)\n    if low16(controls.command) != 0:\n        return controls"}, '_preparation_with_frame': {'signature': 'state, preparation, frame, actor=None, opponent=None, stack=None', 'returns': '', 'flow': 'preparation.validate(state)\nresponse = preparation.response if frame.response is None else frame.response\nreturn DuelPreparationContext(frame, response, preparation.actor if actor is None else actor, preparation.opponent if opponent is None else opponent, preparation.stack if stack is None else stack).validate(state)'}, '_wait_complete_status': {'signature': 'state, second, preparation', 'returns': '', 'flow': "preparation.validate(state)\nif type(second) is not bool:\n    raise ValueError('actual status side required')\nstate.table(16740512 if second else 16740432).set_word(2, 0)\ncurrent = preparation\nwhile True:\n    _duel_frame(state)\n    if not second:\n        current = advance_duel_entry_palette(state, current)\n    rendered = refresh_duel_actors(state, current.frame, current.stack, current.actor, current.opponent)\n    current = _preparation_with_frame(state, current, rendered.frame, rendered.actor, rendered.opponent, rendered.stack)\n    if state.scalar('ram_700c_word') != 0:\n        continue\n    controls = DuelControlContext(current.frame.command, current.frame.comparison)\n    controls = _second_controls(state, controls) if second else _first_controls(state, controls)\n    command = replace_word(controls.command, low16(controls.command) & 240)\n    frame = _actor_reframe(current.frame, command, controls.mode, current.frame.distance, current.frame.factor, current.frame.weapon_difference, current.frame.variation)\n    current = _preparation_with_frame(state, current, frame)\n    if low16(command) != 0:\n        return current"}, '_commit_complete_duel_loadout': {'signature': 'state, preparation, second', 'returns': '', 'flow': "preparation.validate(state)\nif type(second) is not bool:\n    raise ValueError('actual selected loadout side required')\nstate.set_status_word(9984)\nactor = state.table(16740512 if second else 16740432)\nframe = configure_duel_weapon_motion(state, actor, preparation.frame)\nframe = clear_duel_text_plane(state, frame)\nreturn _preparation_with_frame(state, preparation, frame, actor=actor)"}, '_prepare_complete_second_status': {'signature': 'state, preparation', 'returns': '', 'flow': 'from .business_reuse import _reuse_advance_random_pair\npreparation.validate(state)\nrandom = _reuse_advance_random_pair(state)\nselection = low16(random.sample) & 3\nif selection == 3:\n    selection = 0\nselection = u16(selection + 3)\ncommand = choose_duel_status_text(state, selection, random.sample)\nframe = preparation.frame\nframe = _actor_reframe(frame, replace_word(command, 165), random.updated_state, frame.distance, frame.factor, frame.weapon_difference, frame.variation, lookup=state.table(164416))\n_sound(state, 165)\ncurrent = _preparation_with_frame(state, preparation, frame)\ncurrent = _wait_duel_status_text(state, True, DuelControlContext(frame.command, frame.comparison), current)\nframe = current.frame\nframe = _actor_reframe(frame, replace_word(frame.command, 139), frame.comparison, frame.distance, frame.factor, frame.weapon_difference, frame.variation)\n_sound(state, 139)\nreturn _preparation_with_frame(state, current, frame)'}, '_consume_complete_first_duel_frame': {'signature': 'state, preparation', 'returns': '', 'flow': 'preparation.validate(state)\ncurrent = _duel_from_preparation(state, preparation)\ncurrent = _begin_duel_combat_frame(state, current, True)\nreturn DuelActorResult(current.command, current.comparison, current.distance, _turn_actor_values(current), current.actor, current.opponent, current.stack, current.response).validate()'}, '_duel_from_preparation': {'signature': 'state, preparation', 'returns': '', 'flow': "preparation.validate(state)\nvalues = preparation.frame\nif values.working_value is None or values.response is None or values.lookup is None:\n    raise Boundary('complete preparation must return its current D5/D6/A2, not initialization defaults')\nif values.response != preparation.response:\n    raise ValueError('preparation response must agree with the current actor frame')\nreturn DuelTurnFrame(values.command, values.comparison, values.distance, values.factor, values.weapon_difference, values.working_value, values.response, values.variation, preparation.actor, preparation.opponent, values.lookup, preparation.stack, DuelConditionObservation(None, None, None, None)).validate(state)"}, '_duel_from_first_actor': {'signature': 'state, result', 'returns': '', 'flow': "if type(result) is not DuelActorResult:\n    raise ValueError('the continuation needs the actual first actor return')\nresult.validate()\nvalues = result.frame\nif values is None or not values.complete or values.working_value is None or (values.lookup is None):\n    raise Boundary('first actor did not return its actual current working value/lookup')\nif result.response is None or values.response != result.response:\n    raise Boundary('first actor omitted its current response')\nreturn DuelTurnFrame(values.command, values.comparison, values.distance, values.factor, values.weapon_difference, values.working_value, result.response, values.variation, result.actor, result.opponent, values.lookup, result.stack, DuelConditionObservation(None, None, None, None)).validate(state)"}, '_begin_duel_combat_frame': {'signature': 'state, frame, clear_text', 'returns': '', 'flow': "checked_duel_turn(frame, state)\nif type(clear_text) is not bool:\n    raise ValueError('explicit original loop continuation required')\nif clear_text:\n    state.set_status_word(9984)\n    frame = _duel_call_frame(state, clear_duel_text_complete, frame)\n_duel_frame(state)\nframe = replace(frame, actor=state.table(16740432), opponent=state.table(16740512))\nframe = _duel_call_frame(state, _duel_complete_controls, frame, False)\nframe.actor.set_word(0, low16(frame.command))\nmode = state.scalar('ram_700a_byte')\nframe = _duel_observed_comparison(frame, mode, 3, 8)\nif mode == 3:\n    frame = _duel_call_frame(state, choose_duel_ai_command_complete, frame)\n    frame.actor.set_word(0, low16(frame.command))\nreturn _duel_call_frame(state, update_duel_actor_complete, frame)"}, 'advance_duel_turn': {'signature': 'state: SceneState, frame: DuelTurnFrame, clear_text: bool=True', 'returns': 'DuelTurnOutcome', 'flow': 'current = _begin_duel_combat_frame(state, frame, clear_text)\nreturn continue_after_first_duel_actor(state, current)'}, 'continue_after_first_duel_actor': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnOutcome', 'flow': "checked_duel_turn(frame, state)\nframe = replace(frame, actor=state.table(16740512), opponent=state.table(16740432))\nframe = _duel_call_frame(state, _duel_complete_controls, frame, True)\nframe.actor.set_word(0, low16(frame.command))\nmode = state.scalar('ram_700b_byte')\nframe = _duel_observed_comparison(frame, mode, 3, 8)\nif mode == 3:\n    frame = _duel_call_frame(state, choose_duel_ai_command_complete, frame)\n    frame.actor.set_word(0, low16(frame.command))\nframe = _duel_call_frame(state, update_duel_actor_complete, frame)\nframe = _duel_call_frame(state, show_active_duel_turn_label_complete, frame)\nstate.set_scalar('ram_7018_word', 0)\nfirst_health = state.table(16740432).word(28)\nframe = _duel_observed_move(frame, first_health, 16)\nif first_health == 0:\n    return show_terminal_duel_result_complete(state, frame)\nstate.set_scalar('ram_7018_word', 32768)\nsecond_health = state.table(16740512).word(28)\nframe = _duel_observed_move(frame, second_health, 16)\nif second_health == 0:\n    return show_terminal_duel_result_complete(state, frame)\npending = state.table(16740432).word(2)\nframe = replace(frame, comparison=replace_word(frame.comparison, pending))\npending = u16(low16(frame.comparison) | state.table(16740512).word(2))\nframe = replace(frame, comparison=replace_word(frame.comparison, pending))\npending &= 53248\nframe = replace(frame, comparison=replace_word(frame.comparison, pending))\nframe = _duel_observed_move(frame, pending, 16)\nif pending:\n    return DuelTurnOutcome('next_frame', frame, None).validate(state)\nstate.set_scalar('ram_7018_word', 0)\ncommand = state.table(16740432).word() & 64\nframe = replace(frame, command=replace_word(frame.command, command))\nframe = _duel_observed_move(frame, command, 16)\nif command == 0:\n    state.set_scalar('ram_7018_word', 32768)\n    command = state.table(16740512).word() & 64\n    frame = replace(frame, command=replace_word(frame.command, command))\n    frame = _duel_observed_move(frame, command, 16)\n    if command == 0:\n        return DuelTurnOutcome('next_frame', frame, None).validate(state)\nreturn choose_duel_turn_action_complete(state, frame)"}, 'choose_duel_turn_action_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnOutcome', 'flow': "checked_duel_turn(frame, state)\nstate.set_status_word(9984)\nstate.set_scalar('ram_d100_word', 0)\nside = state.scalar('ram_7018_word')\nframe = _duel_observed_move(frame, side, 16)\nsecond = negative_word(side)\nactor = state.table(16740512 if second else 16740432)\nopponent = state.table(16740432 if second else 16740512)\nmode = state.scalar('ram_700b_byte' if second else 'ram_700a_byte')\nframe = _duel_observed_comparison(frame, mode, 3, 8)\nif mode != 3:\n    officer = actor.word(26)\n    frame = replace(frame, comparison=replace_word(frame.comparison, officer))\n    linked_officer = actor.word(32)\n    frame = _duel_observed_comparison(frame, officer, linked_officer, 16)\n    same = officer == linked_officer\n    _configure_duel_dialog(state, 52096 if same else 51008, 166180 if same else 166122)\n    frame = replace(frame, command=replace_word(frame.command, 173))\n    _sound(state, 173)\n    state.set_status_word(9472)\n    raise DuelContinuationBoundary(160962, frame, 'manual action menu has no proven complete saved-input/glyph return')\ncommand = actor.word() & 3\nframe = replace(frame, command=replace_word(frame.command, command))\nframe = _duel_observed_move(frame, command, 16)\nstate.set_scalar('ram_7019_byte', low8(frame.command))\nreturn perform_selected_duel_action_complete(state, frame)"}, 'perform_selected_duel_action_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnOutcome', 'flow': "checked_duel_turn(frame, state)\nframe = replace(frame, command=replace_word(frame.command, 172))\n_sound(state, 172)\nstate.set_status_word(9984)\nframe = _duel_call_frame(state, clear_duel_text_complete, frame)\nframe = replace(frame, actor=state.table(16740432), opponent=state.table(16740512))\nside = state.scalar('ram_7018_word')\nframe = _duel_observed_move(frame, side, 16)\nif negative_word(side):\n    frame = replace(frame, actor=state.table(16740512), opponent=state.table(16740432))\nshifted = u16(state.scalar('ram_7018_word') << 2)\nframe = replace(frame, command=replace_word(frame.command, shifted))\nvector = u32(161142 + s16(shifted))\ncalled = replace(frame, stack=frame.stack.advance(-4))\ncalled.stack.set_long(0, 161138)\nresult = state.service_at(vector, called)\nresult = checked_duel_action_outcome(result, state)\nif result.discarded_continuation is None:\n    returned = replace(result.frame, stack=result.frame.stack.advance(4))\n    return DuelTurnOutcome('next_frame_clear', returned, None).validate(state)\ntoken = result.discarded_continuation\nif token.return_carrier != 161138:\n    raise DuelContinuationBoundary(token.return_carrier, result.frame, 'actual discarded return token does not denote this indexed call continuation')\nreturn DuelTurnOutcome('fade', result.frame, token).validate(state)"}, 'show_terminal_duel_result_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnOutcome', 'flow': "checked_duel_turn(frame, state)\nstate.set_scalar('ram_f612_word', 1792)\nwhile state.read(4294964754, 1) != 0:\n    state.progress('terminal_duel_label_ack')\nframe = _duel_call_frame(state, show_active_duel_turn_label_complete, frame)\nstate.set_scalar('ram_f612_word', 1792)\nwhile state.read(4294964754, 1) != 0:\n    state.progress('terminal_duel_label_ack')\nstate.set_status_word(9984)\nframe = replace(frame, command=replace_word(frame.command, 31))\nside = state.scalar('ram_7018_word')\nframe = _duel_observed_move(frame, side, 16)\nif negative_word(side):\n    frame = replace(frame, command=replace_word(frame.command, 34))\nframe = _duel_call_frame(state, choose_duel_status_text_complete, frame, low16(frame.command))\nframe = _duel_call_frame(state, wait_active_duel_action_complete, frame)\nframe = _duel_call_frame(state, clear_duel_text_complete, frame)\nframe = replace(frame, command=replace_word(frame.command, 32))\nside = state.scalar('ram_7018_word')\nif negative_word(side):\n    frame = replace(frame, command=replace_word(frame.command, u16(low16(frame.command) + 1)))\nframe = _duel_call_frame(state, choose_duel_status_text_complete, frame, low16(frame.command))\nframe = _duel_call_frame(state, wait_either_duel_action_complete, frame)\nreturn finish_duel_turn_scene(state, frame)"}, 'finish_duel_turn_scene': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnOutcome', 'flow': "from .business_scene import darken_palette\nchecked_duel_turn(frame, state)\nwhile True:\n    _duel_frame(state)\n    frame = _duel_call_frame(state, refresh_duel_actors_complete, frame)\n    shade = state.scalar('ram_70f6_word')\n    frame = _duel_observed_comparison(frame, shade, 16, 16)\n    if shade >= 16:\n        return DuelTurnOutcome('finished', frame, None).validate(state)\n    frame = replace(frame, command=replace_word(frame.command, shade), comparison=replace_word(frame.comparison, 64), actor=state.table(163968).cursor())\n    transformed = darken_palette(state, frame.command, low16(frame.comparison), frame.actor, frame.weapon_difference, count_carrier=frame.comparison, color=frame.distance, component=frame.factor)\n    frame = replace(frame, command=transformed.shade_carrier, comparison=transformed.count_carrier, distance=transformed.color, factor=transformed.component, weapon_difference=transformed.accumulated, actor=transformed.source, opponent=transformed.destination, conditions=DuelConditionObservation(None, None, None, None))\n    state.set_scalar('ram_70f6_word', u16(state.scalar('ram_70f6_word') + 1))"}, '_initialization_values': {'signature': 'state, current, *, frame=None, response=None, glyph_work=None, source=None, destination=None, glyph_source=None', 'returns': '', 'flow': "current.validate(state)\npreparation = current.preparation\nframe = preparation.frame if frame is None else frame\nactual_response = frame.response if response is None else response\nactual_working = frame.working_value if glyph_work is None else glyph_work\nactual_lookup = frame.lookup if glyph_source is None else glyph_source\nif actual_response is None or actual_working is None or actual_lookup is None:\n    raise Boundary('initialization must consume the current actual frame, not an older glyph snapshot')\nframe = replace(frame, working_value=actual_working, response=actual_response, lookup=actual_lookup)\nreturn DuelInitializationResult(DuelPreparationContext(frame, actual_response, preparation.actor if source is None else source, preparation.opponent if destination is None else destination, preparation.stack), actual_working, actual_lookup).validate(state)"}, '_stage_complete_duel_packet': {'signature': 'state, current, source_address, command, rows, row_command', 'returns': '', 'flow': 'from .business_reuse import stage_sprite_word_packet\nfrom .contexts_reuse import SpritePacketContext\ncurrent.validate(state)\npreparation, frame = (current.preparation, current.preparation.frame)\nsource = state.table(source_address).cursor()\npacket = SpritePacketContext(command, replace_word(frame.comparison, rows), replace_word(frame.distance, row_command), frame.factor, frame.weapon_difference, current.glyph_work, preparation.response, frame.variation, source, preparation.opponent.cursor(), current.glyph_source, preparation.stack)\nresult = stage_sprite_word_packet(state, source, command, rows, row_command, packet)\nframe = _actor_reframe(frame, result.command, result.rows, result.row_command, result.remaining, result.token, result.rows_remaining, working_value=result.run_count, response=result.response, lookup=result.glyph_source)\nreturn _initialization_values(state, current, frame=frame, response=result.response, glyph_work=result.run_count, source=result.source, destination=result.destination, glyph_source=result.glyph_source)'}, '_choose_complete_duel_loadout': {'signature': 'state, second, preparation', 'returns': '', 'flow': "preparation.validate(state)\nif type(second) is not bool:\n    raise ValueError('actual loadout side required')\nmode_name = 'ram_700b_byte' if second else 'ram_700a_byte'\ncurrent = preparation\nif state.scalar(mode_name) != 3:\n    raise Boundary('manual equipment/menu return needs its complete current-value contract')\nif not second:\n    current = advance_duel_entry_palette(state, current)\nwhile True:\n    _duel_frame(state)\n    current = advance_duel_entry_palette(state, current)\n    rendered = refresh_duel_actors(state, current.frame, current.stack, current.actor, current.opponent)\n    current = _preparation_with_frame(state, current, rendered.frame, rendered.actor, rendered.opponent, rendered.stack)\n    if not second:\n        state.set_scalar('ram_708a_word', 0)\n    if state.scalar(mode_name) != 3:\n        raise Boundary('live loadout switched into unresolved full manual return')\n    current = _preparation_with_frame(state, current, current.frame, actor=state.table(16740512 if second else 16740432))\n    current = _choose_duel_ai_panel(state, current.actor, current.opponent, DuelControlContext(current.frame.command, current.frame.comparison), current)\n    selected_second = current.actor.base != 16740432\n    if not selected_second and low16(current.response) == 0:\n        second = False\n        mode_name = 'ram_700a_byte'\n        continue\n    return (_commit_complete_duel_loadout(state, current, selected_second), selected_second)"}, '_prepare_complete_first_status': {'signature': 'state, preparation', 'returns': '', 'flow': 'from .business_reuse import _reuse_advance_random_pair\npreparation.validate(state)\nrandom = _reuse_advance_random_pair(state)\nselection = low16(random.sample) & 3\nif selection == 3:\n    selection = 0\ncommand = choose_duel_status_text(state, selection, random.sample)\nframe = preparation.frame\nframe = _actor_reframe(frame, replace_word(command, 165), random.updated_state, frame.distance, frame.factor, frame.weapon_difference, frame.variation, lookup=state.table(164416))\n_sound(state, 165)\ncurrent = _preparation_with_frame(state, preparation, frame)\ncurrent = _wait_duel_status_text(state, False, DuelControlContext(frame.command, frame.comparison), current)\nstate.set_status_word(9984)\nreturn _preparation_with_frame(state, current, clear_duel_text_plane(state, current.frame))'}, 'prepare_duel_scene_first_frame': {'signature': 'state: SceneState, context: DuelInitializationContext', 'returns': 'DuelPreparationResult', 'flow': "if type(context) is not DuelInitializationContext:\n    raise ValueError('actual complete initialization input required')\ncontext.validate(state)\ninitialized = _initialize_duel_scene(state, context)\ncurrent, selected_second = _choose_complete_duel_loadout(state, False, initialized.preparation)\nwhile not selected_second:\n    current, selected_second = _choose_complete_duel_loadout(state, True, current)\ncurrent = _prepare_complete_first_status(state, current)\ncurrent = _prepare_complete_second_status(state, current)\nactual = _consume_complete_first_duel_frame(state, current)\nreturn DuelPreparationResult('first_frame', None, actual).validate(state)"}, 'continue_automatic_duel_preparation': {'signature': 'state: SceneState, preparation: DuelPreparationContext', 'returns': 'DuelPreparationResult', 'flow': "if type(preparation) is not DuelPreparationContext:\n    raise ValueError('actual complete preparation caller required')\npreparation.validate(state)\ncurrent = _choose_duel_ai_panel(state, preparation.actor, preparation.opponent, DuelControlContext(preparation.frame.command, preparation.frame.comparison), preparation)\nfirst_side = current.actor.base == 16740432\nif low16(current.response) == 0 and first_side:\n    return DuelPreparationResult('repeat_first', current).validate(state)\ncurrent = _commit_complete_duel_loadout(state, current, not first_side)\nif first_side:\n    return DuelPreparationResult('needs_second_loadout', current).validate(state)\ncurrent = _prepare_complete_second_status(state, current)\nactual = _consume_complete_first_duel_frame(state, current)\nreturn DuelPreparationResult('first_frame', None, actual).validate(state)"}, '_initialize_duel_scene': {'signature': 'state, context', 'returns': '', 'flow': "from .business_reuse import clear_video_sprite_plane, expand_glyph_stream\nfrom .contexts_reuse import GlyphColors, GlyphSavedValues\nfrom .contexts_scene import PacketTransferValues\nfrom .business_scene import flush_scene_transfer_queue\nif type(context) is not DuelInitializationContext:\n    raise Boundary('natural initialization requires explicit complete live-in and stack')\ncontext.validate(state)\nframe = replace(context.frame, working_value=context.glyph_work, response=context.response)\nstate.set_status_word(9984)\ncommand = replace_word(frame.command, state.scalar('ram_f606_word'))\ncommand = replace_byte(command, low8(command) & 191)\nstate.mmio_write(12582916, 2, low16(command))\nstate.set_scalar('ram_f612_word', 0)\ncleared = clear_video_sprite_plane(state, context.response)\nresponse = cleared.response\nframe = _actor_reframe(frame, command, frame.comparison, frame.distance, frame.factor, frame.weapon_difference, cleared.variation)\nfor command in (33592, 33336, 33799, 34156, 36151, 37524, 35587):\n    state.mmio_write(12582916, 2, command)\nfirst, second = (state.table(16740432), state.table(16740512))\nfirst.set_long(14, 4194304)\nfirst.set_word(24, 34816)\nfirst.set_word(2, 1)\nsecond.set_long(14, 16777216)\nsecond.set_word(24, 40960)\nsecond.set_word(2, 1)\nstate.set_scalar('ram_70f0_word', 0)\nstate.set_scalar('ram_70f6_word', 0)\nstate.set_scalar('ram_70f8_word', 0)\nequipment = state.table(4294961800).cursor(u16(first.word(26) * 3))\nfirst.set_byte(43, equipment.next_byte())\nfirst.set_byte(45, equipment.next_byte())\nfirst.set_byte(47, equipment.byte())\nequipment_product = u32(second.word(26) * 3)\nequipment = state.table(4294961800).cursor(low16(equipment_product))\nsecond.set_byte(43, equipment.next_byte())\nsecond.set_byte(45, equipment.next_byte())\nsecond.set_byte(47, equipment.byte())\nstate.mmio_write(12582916, 4, 1073741824)\n_upload_longs(state, state.table(443316).cursor(), 12287)\nstate.mmio_write(12582916, 4, 1073741827)\n_upload_longs(state, state.table(564700).cursor(), 31)\nframe = _actor_reframe(frame, replace_word(frame.command, 1), replace_word(frame.comparison, 2), frame.distance, replace_word(frame.factor, 9), equipment_product, frame.variation)\nsource, destination = (state.table(566310).cursor(), state.table(4294955776).cursor())\nglyph = expand_glyph_stream(state, source, destination, GlyphColors(frame.command, frame.comparison), frame.factor, GlyphSavedValues(frame.weapon_difference, context.glyph_work, response, frame.variation, state.table(562908), context.stack))\nframe = _actor_reframe(frame, replace_word(frame.command, 65535), frame.comparison, frame.distance, glyph.remaining_carrier, glyph.saved.working, glyph.saved.pixels, working_value=glyph.saved.repeat, response=glyph.saved.response, lookup=glyph.saved.glyph_source)\nsource = _upload_longs(state, state.table(4294955776).cursor(), 79)\ncurrent = DuelInitializationResult(DuelPreparationContext(frame, glyph.saved.response, source, glyph.destination, context.stack), glyph.saved.repeat, glyph.saved.glyph_source).validate(state)\nstate.mmio_write(12582916, 4, 1342177283)\n_upload_longs(state, state.table(492468).cursor(), 47)\nstate.mmio_write(12582916, 4, 1107296259)\nfor actor in (first, second):\n    frame = current.preparation.frame\n    frame = _actor_reframe(frame, replace_word(frame.command, 1), replace_word(frame.comparison, 2), frame.distance, frame.factor, frame.weapon_difference, frame.variation)\n    current = _initialization_values(state, current, frame=frame)\n    current = upload_duel_officer_name(state, actor.word(26), DuelGlyphContext(frame.command, frame.comparison, frame.factor), current)\nframe = current.preparation.frame\nframe = _actor_reframe(frame, replace_word(frame.command, 1), replace_word(frame.comparison, 2), frame.distance, replace_word(frame.factor, 1), frame.weapon_difference, frame.variation)\ncurrent = _initialization_values(state, current, frame=frame)\ncurrent = upload_duel_glyph_strip(state, state.table(166074).cursor(), DuelGlyphContext(frame.command, frame.comparison, frame.factor), current)\ncurrent = _initialization_values(state, current, frame=clear_duel_text_plane(state, current.preparation.frame))\nsource, destination = (state.table(163968).cursor(), state.table(4294966016).cursor())\nfor _ in range(32):\n    destination.append_long(source.next_long())\nframe = current.preparation.frame\ncurrent = _initialization_values(state, current, frame=_actor_reframe(frame, replace_word(frame.command, 65535), frame.comparison, frame.distance, frame.factor, frame.weapon_difference, frame.variation), source=source, destination=destination)\nstate.set_scalar('ram_f31e_word', 1)\nmap_source = state.table(492660).cursor()\nif state.scalar('ram_70f2_word') == 3:\n    map_source = state.table(493142).cursor()\nframe = current.preparation.frame\nlanes = decode_duel_byte_lanes(state, map_source, state.table(16736256).cursor(), 1280, frame.distance, frame.factor, length_carrier=replace_word(frame.command, 1280), count_carrier=frame.comparison, stack=context.stack)\nframe = _actor_reframe(frame, replace_word(lanes.length_carrier, 65535), lanes.count_carrier, lanes.repeat_value, lanes.pair_value, frame.weapon_difference, frame.variation)\ncurrent = _initialization_values(state, current, frame=frame, source=lanes.source, destination=lanes.destination)\nstate.mmio_write(12582916, 4, 1610612739)\n_upload_words(state, state.table(16736256).cursor(), 1279)\nlanes = decode_duel_byte_lanes(state, state.table(493630).cursor(), state.table(16736256).cursor(), 1280, frame.distance, frame.factor, length_carrier=replace_word(frame.command, 1280), count_carrier=frame.comparison, stack=context.stack)\nframe = _actor_reframe(frame, replace_word(lanes.length_carrier, 65535), lanes.count_carrier, lanes.repeat_value, lanes.pair_value, frame.weapon_difference, frame.variation)\ncurrent = _initialization_values(state, current, frame=frame, source=lanes.source, destination=lanes.destination)\nstate.mmio_write(12582916, 4, 1879048195)\n_upload_words(state, state.table(16736256).cursor(), 1279)\nstate.set_scalar('ram_f694_word', 1539)\nstate.set_scalar('ram_f692_word', 1540)\ncurrent = _stage_complete_duel_packet(state, current, 164128, 1610612776, 3, 59904)\nframe = current.preparation.frame\nflushed = flush_scene_transfer_queue(state, PacketTransferValues(frame.command, frame.comparison, frame.distance, frame.factor))\nif flushed is not None:\n    values = flushed.values\n    frame = _actor_reframe(frame, values.command, values.increment, values.address, values.spill, frame.weapon_difference, frame.variation)\n    current = _initialization_values(state, current, frame=frame, source=flushed.source)\ncurrent = _stage_complete_duel_packet(state, current, 164212, 1610612776, 5, 60288)\nreturn current"}, '_finish_duel_scene': {'signature': 'state, controls, actor_values', 'returns': '', 'flow': "raise Boundary('this legacy partial observation lacks the actual current duel frame; use the complete core')"}, '_resolve_duel_pending_action': {'signature': 'state, actor, opponent, controls, retained', 'returns': '', 'flow': "raise Boundary('this legacy partial observation lacks the actual current duel frame; use the complete core')"}, '_choose_duel_command': {'signature': 'state, controls, retained', 'returns': '', 'flow': "raise Boundary('this legacy partial observation lacks the actual current duel frame; use the complete core')"}, '_show_duel_action_result': {'signature': 'state, controls', 'returns': '', 'flow': "raise Boundary('this legacy partial observation lacks the actual current duel frame; use the complete core')"}, 'run_duel_scene': {'signature': 'state: SceneState, context: DuelSceneContext=DuelSceneContext()', 'returns': 'DuelSceneResult', 'flow': "context.validate()\nif context.initialization is None:\n    raise Boundary('natural duel scene needs its complete actual initialization live-in')\nfirst = prepare_duel_scene_first_frame(state, context.initialization)\ncurrent = _duel_from_first_actor(state, first.first_frame)\noutcome = continue_after_first_duel_actor(state, current)\nwhile outcome.phase != 'finished':\n    if outcome.phase == 'fade':\n        outcome = finish_duel_turn_scene(state, outcome.frame)\n    else:\n        outcome = advance_duel_turn(state, outcome.frame, outcome.phase == 'next_frame_clear')\nfinal = outcome.frame\nreturn DuelSceneResult(DuelControlContext(final.command, final.comparison), DuelActorContext(final.command, final.comparison, final.distance, _turn_actor_values(final).retained, final.stack, final), state.read_status_word(), final)"}}
for _name, _shape in HOST_COMPLETE_TURN_DECLARATIONS.items():
    _old = DECLARATIONS.get(_name, {})
    DECLARATIONS[_name] = dict(_old, **_shape)
HOST_COMPLETE_TURN_IMPORTS = {'domain': ['Boundary', 'Cursor', 'Long', 'SceneState', 'Table', 'Word', 'divu_retained', 'high16', 'low16', 'low8', 'negative_long', 'negative_word', 'replace_byte', 'replace_word', 's16', 's8', 'swap_words', 'u16', 'u32', 'u8', 'uint'], 'contexts_duel': ['DuelAIContext', 'DuelAIResult', 'DuelActionContext', 'DuelActionResult', 'DuelActorContext', 'DuelActorFrame', 'DuelActorResult', 'DuelConditionObservation', 'DuelContact', 'DuelContinuationBoundary', 'DuelControlContext', 'DuelGlyphContext', 'DuelInitializationContext', 'DuelInitializationResult', 'DuelLaneResult', 'DuelOverrideResult', 'DuelPreparationContext', 'DuelPreparationResult', 'DuelProbability', 'DuelRenderResult', 'DuelRetainedValues', 'DuelSceneContext', 'DuelSceneResult', 'DuelSpriteResult', 'DuelTurnFrame', 'DuelTurnOutcome', 'checked_duel_action_outcome', 'checked_duel_turn'], 'business_reuse': ['_reuse_advance_random_pair', 'choose_first_duel_control', 'choose_second_duel_control', 'clear_video_sprite_plane', 'enqueue_sound_command', 'expand_glyph_stream', 'stage_sprite_word_packet', 'step_random'], 'business_scene': ['darken_palette', 'decode_glyph_rows_to_buffers', 'flush_scene_transfer_queue'], 'contexts_reuse': ['GlyphColors', 'GlyphSavedValues', 'SpritePacketContext'], 'contexts_scene': ['PacketTransferValues']}
for _module, _names in HOST_COMPLETE_TURN_IMPORTS.items():
    APPROVED.setdefault(_module, set()).update(_names)

# Linkage14 manual menu: complete supplied host bodies, finite AST only.
# Existing ordinary physical emitters and width allocation remain unchanged.
HOST_MANUAL_MENU_DECLARATIONS = {'choose_duel_action_menu': {'signature': 'state: SceneState, controls: DuelControlContext, *, live: '
                                          'DuelTurnFrame | None=None',
                             'returns': 'DuelControlContext',
                             'flow': 'if type(controls) is not DuelControlContext:\n'
                                     "    raise ValueError('actual duel controls required')\n"
                                     'controls.validate()\n'
                                     'if live is None:\n'
                                     "    raise Boundary('action menu requires current eight values, three "
                                     "views and entry stack')\n"
                                     'checked_duel_turn(live, state)\n'
                                     'if (controls.command, controls.mode) != (live.command, '
                                     'live.comparison):\n'
                                     "    raise ValueError('menu observations must agree with the actual "
                                     "full caller')\n"
                                     'returned = choose_duel_action_menu_complete(state, live)\n'
                                     'return DuelControlContext(returned.command, '
                                     'returned.comparison).validate()'},
 'choose_duel_turn_action_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame',
                                      'returns': 'DuelTurnOutcome',
                                      'flow': 'checked_duel_turn(frame, state)\n'
                                              'state.set_status_word(9984)\n'
                                              "state.set_scalar('ram_d100_word', 0)\n"
                                              "side = state.scalar('ram_7018_word')\n"
                                              'frame = _duel_observed_move(frame, side, 16)\n'
                                              'second = negative_word(side)\n'
                                              'actor = state.table(16740512 if second else 16740432)\n'
                                              'opponent = state.table(16740432 if second else 16740512)\n'
                                              "mode = state.scalar('ram_700b_byte' if second else "
                                              "'ram_700a_byte')\n"
                                              'frame = _duel_observed_comparison(frame, mode, 3, 8)\n'
                                              'if mode != 3:\n'
                                              '    officer = actor.word(26)\n'
                                              '    frame = replace(frame, '
                                              'comparison=replace_word(frame.comparison, officer))\n'
                                              '    linked_officer = actor.word(32)\n'
                                              '    frame = _duel_observed_comparison(frame, officer, '
                                              'linked_officer, 16)\n'
                                              '    same = officer == linked_officer\n'
                                              '    _configure_duel_action_dialog(state, 52096 if same else 51008, '
                                              '166180 if same else 166122)\n'
                                              '    frame = replace(frame, '
                                              'command=replace_word(frame.command, 173))\n'
                                              '    _sound(state, 173)\n'
                                              '    return continue_manual_duel_action(state, frame)\n'
                                              'command = actor.word() & 3\n'
                                              'frame = replace(frame, command=replace_word(frame.command, '
                                              'command))\n'
                                              'frame = _duel_observed_move(frame, command, 16)\n'
                                              "state.set_scalar('ram_7019_byte', low8(frame.command))\n"
                                              'return perform_selected_duel_action_complete(state, frame)'},
 '_append_duel_menu_cursor': {'signature': 'state, frame',
                              'returns': None,
                              'flow': 'checked_duel_turn(frame, state)\n'
                                      'called = replace(frame, stack=frame.stack.advance(-4))\n'
                                      'result = append_duel_sprite(state, low16(called.command), '
                                      'low16(called.comparison), low16(called.distance), '
                                      'low16(called.factor), _turn_actor_values(called), called.stack)\n'
                                      'if result.frame is None or result.stack is None or result.source is '
                                      'None:\n'
                                      "    raise Boundary('complete menu sprite omitted its actual current "
                                      "return')\n"
                                      'current = _turn_from_actor(state, called, result.frame, '
                                      'result.destination, result.source, result.stack)\n'
                                      'return replace(current, stack=current.stack.advance(4))'},
 '_duel_menu_highlight': {'signature': 'state, frame, restricted',
                          'returns': None,
                          'flow': 'frame = replace(frame, command=replace_word(frame.command, '
                                  'low16(frame.command) & 15))\n'
                                  'if low16(frame.command) == 0:\n'
                                  "    blink = state.scalar('ram_7008_word')\n"
                                  '    frame = replace(frame, command=replace_word(frame.command, blink & '
                                  '8))\n'
                                  '    if low16(frame.command) == 0:\n'
                                  '        return frame\n'
                                  'if restricted:\n'
                                  "    selected = state.scalar('ram_7018_word') & 3\n"
                                  '    frame = replace(frame, distance=replace_word(frame.distance, '
                                  'selected), command=replace_word(frame.command, 200), comparison=0)\n'
                                  '    vertical = state.table(163854).byte(s16(low16(frame.distance)))\n'
                                  '    frame = replace(frame, comparison=replace_byte(frame.comparison, '
                                  'vertical))\n'
                                  'else:\n'
                                  "    horizontal = (state.scalar('ram_7018_word') & 2) * 12\n"
                                  '    frame = replace(frame, command=replace_word(u32(horizontal), '
                                  'u16(horizontal + 176)))\n'
                                  "    vertical = (state.scalar('ram_7018_word') & 1) * 48\n"
                                  '    frame = replace(frame, comparison=replace_word(u32(vertical), '
                                  'u16(vertical + 136)))\n'
                                  'frame = replace(frame, distance=replace_word(frame.distance, 67), '
                                  'factor=replace_word(frame.factor, 32768))\n'
                                  'return _append_duel_menu_cursor(state, frame)'},
 'choose_duel_action_menu_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame',
                                      'returns': 'DuelTurnFrame',
                                      'flow': 'checked_duel_turn(frame, state)\n'
                                              "second = negative_word(state.scalar('ram_7018_word'))\n"
                                              'actor = state.table(16740512 if second else 16740432)\n'
                                              'officer = actor.word(26)\n'
                                              'frame = replace(frame, '
                                              'comparison=replace_word(frame.comparison, officer))\n'
                                              'restricted = officer == actor.word(32)\n'
                                              'if restricted:\n'
                                              '    frame = replace(frame, '
                                              "comparison=state.scalar('ram_7019_byte'))\n"
                                              '    if frame.command & 8:\n'
                                              '        selected = u16(low16(frame.comparison) + 1)\n'
                                              '        if selected == 2:\n'
                                              '            selected = u16(selected + 1)\n'
                                              '        frame = replace(frame, '
                                              'comparison=replace_word(frame.comparison, selected))\n'
                                              '        if selected >= 4:\n'
                                              '            frame = replace(frame, comparison=0)\n'
                                              '    if frame.command & 4:\n'
                                              '        selected = low16(frame.comparison)\n'
                                              '        if selected == 3:\n'
                                              '            selected = u16(selected - 1)\n'
                                              '        selected = u16(selected - 1)\n'
                                              '        frame = replace(frame, '
                                              'comparison=replace_word(frame.comparison, selected))\n'
                                              '        if negative_word(selected):\n'
                                              '            frame = replace(frame, comparison=3)\n'
                                              "    state.set_scalar('ram_7019_byte', "
                                              'low8(frame.comparison))\n'
                                              'else:\n'
                                              "    selected = state.scalar('ram_7018_word')\n"
                                              '    frame = replace(frame, '
                                              'comparison=replace_word(frame.comparison, selected), '
                                              'command=replace_word(frame.command, low16(frame.command) & '
                                              '15))\n'
                                              '    if low16(frame.command) != 0:\n'
                                              '        delta = 1\n'
                                              '        if not frame.command & 8:\n'
                                              '            delta = 65535\n'
                                              '            if not frame.command & 4:\n'
                                              '                delta = 2 if frame.command & 2 else 65534\n'
                                              '        frame = replace(frame, '
                                              'distance=replace_word(frame.distance, delta))\n'
                                              '        selected_byte = u8(frame.comparison + '
                                              'frame.distance)\n'
                                              '        frame = replace(frame, '
                                              'comparison=replace_byte(frame.comparison, selected_byte))\n'
                                              '        if selected_byte < 4:\n'
                                              "            state.set_scalar('ram_7018_word', "
                                              'low16(frame.comparison))\n'
                                              'frame = _duel_call_frame(state, _duel_complete_controls, '
                                              'frame, False)\n'
                                              'if not frame.command & 32:\n'
                                              '    frame = _duel_menu_highlight(state, frame, restricted)\n'
                                              "timer = state.scalar('ram_70fa_word')\n"
                                              "state.set_scalar('ram_70fa_word', u16(timer - 1))\n"
                                              'return _duel_observed_comparison(frame, timer, 1, '
                                              '16).validate(state)'},
 '_duel_observed_bit': {'signature': 'frame, value, bit',
                        'returns': None,
                        'flow': 'observed = frame.conditions\n'
                                'return replace(frame, conditions=DuelConditionObservation(observed.carry, '
                                'not bool(value & 1 << bit), observed.negative, observed.overflow))'},
 'continue_manual_duel_action': {'signature': 'state: SceneState, frame: DuelTurnFrame',
                                 'returns': 'DuelTurnOutcome',
                                 'flow': 'checked_duel_turn(frame, state)\n'
                                         'state.set_status_word(9472)\n'
                                         'while True:\n'
                                         "    state.set_scalar('ram_f612_word', 1792)\n"
                                         '    while True:\n'
                                         '        acknowledgement = state.read(4294964754, 1)\n'
                                         '        frame = _duel_observed_move(frame, acknowledgement, 8)\n'
                                         '        if acknowledgement == 0:\n'
                                         '            break\n'
                                         "        state.progress('manual_duel_menu_frame_ack')\n"
                                         '    frame = _duel_call_frame(state, refresh_duel_actors_complete, '
                                         'frame)\n'
                                         '    frame = _duel_call_frame(state, _duel_complete_controls, '
                                         'frame, False)\n'
                                         "    side = state.scalar('ram_7018_word')\n"
                                         '    frame = _duel_observed_move(frame, side, 16)\n'
                                         '    if negative_word(side):\n'
                                         '        frame = _duel_call_frame(state, _duel_complete_controls, '
                                         'frame, True)\n'
                                         '    frame = replace(frame, stack=frame.stack.advance(-2))\n'
                                         '    frame.stack.set_word(0, low16(frame.command))\n'
                                         '    frame = _duel_observed_move(frame, low16(frame.command), 16)\n'
                                         '    frame = _duel_call_frame(state, '
                                         'choose_duel_action_menu_complete, frame)\n'
                                         '    saved_command = frame.stack.word()\n'
                                         '    frame = replace(frame, command=replace_word(frame.command, '
                                         'saved_command), stack=frame.stack.advance(2))\n'
                                         '    frame = _duel_observed_move(frame, saved_command, 16)\n'
                                         "    active_dialog = state.scalar('ram_700c_word')\n"
                                         '    frame = _duel_observed_move(frame, active_dialog, 16)\n'
                                         '    if active_dialog != 0:\n'
                                         '        continue\n'
                                         '    frame = _duel_observed_bit(frame, frame.command, 5)\n'
                                         "    if not frame.conditions.require('zero'):\n"
                                         '        return perform_selected_duel_action_complete(state, '
                                         'frame)\n'
                                         '    frame = _duel_observed_bit(frame, frame.command, 4)\n'
                                         "    if not frame.conditions.require('zero'):\n"
                                         "        return DuelTurnOutcome('next_frame_clear', frame, "
                                         'None).validate(state)'}}
DECLARATIONS.update(HOST_MANUAL_MENU_DECLARATIONS)

# Linkage15 manual initialization loadout: complete supplied host bodies, finite AST only.
# Existing ordinary physical emitters and width allocation remain unchanged.
HOST_MANUAL_LOADOUT_DECLARATIONS = {'_expand_and_upload_duel_glyphs': {'signature': 'state, source, destination, colors, current=None',
                                    'returns': None,
                                    'flow': 'from .business_scene import decode_glyph_rows_to_buffers\n'
                                            'source = _live_cursor(state, source)\n'
                                            'colors.validate()\n'
                                            'saved = None\n'
                                            'if current is not None:\n'
                                            '    from .contexts_reuse import GlyphSavedValues\n'
                                            '    current.validate(state)\n'
                                            '    frame = current.preparation.frame\n'
                                            '    saved = GlyphSavedValues(frame.weapon_difference, '
                                            'current.glyph_work, current.preparation.response, '
                                            'frame.variation, current.glyph_source, '
                                            'current.preparation.stack.advance(-4))\n'
                                            'result = decode_glyph_rows_to_buffers(state, source, '
                                            'destination, colors.background, colors.foreground, '
                                            'colors.remaining, saved)\n'
                                            'source = _upload_longs(state, state.table(4294955776).cursor(), '
                                            '95)\n'
                                            'if current is not None:\n'
                                            '    restored = result.saved\n'
                                            '    frame = _actor_reframe(frame, '
                                            'replace_word(result.background, 65535), result.foreground, '
                                            'frame.distance, result.remaining, restored.working, '
                                            'restored.pixels)\n'
                                            '    return _initialization_values(state, current, frame=frame, '
                                            'response=restored.response, glyph_work=restored.repeat, '
                                            'glyph_source=restored.glyph_source, source=source, '
                                            'destination=result.destination, '
                                            'stack=restored.stack.advance(4))\n'
                                            'return DuelGlyphContext(result.background, result.foreground, '
                                            'result.remaining)'},
 'choose_duel_two_option_menu': {'signature': 'state: SceneState, choice: Table, controls: '
                                              'DuelControlContext, *, live: DuelTurnFrame | None=None',
                                 'returns': 'DuelControlContext',
                                 'flow': 'choice = _live_table(state, choice)\n'
                                         'controls.validate()\n'
                                         'current = _duel_legacy_menu_input(state, choice, controls, live)\n'
                                         'returned = choose_duel_two_option_menu_complete(state, current)\n'
                                         'return DuelControlContext(returned.command, '
                                         'returned.comparison).validate()'},
 '_choose_duel_equipment': {'signature': 'state, choice, equipment, controls, live=None',
                            'returns': None,
                            'flow': 'choice = _live_table(state, choice)\n'
                                    'equipment = _live_table(state, equipment)\n'
                                    'controls.validate()\n'
                                    'current = _duel_legacy_menu_input(state, choice, controls, live)\n'
                                    'returned = _choose_duel_equipment_complete(state, equipment, current)\n'
                                    'return DuelControlContext(returned.command, '
                                    'returned.comparison).validate()'},
 'choose_first_duel_equipment': {'signature': 'state: SceneState, choice: Table, controls: '
                                              'DuelControlContext, *, live: DuelTurnFrame | None=None',
                                 'returns': 'DuelControlContext',
                                 'flow': 'return _choose_duel_equipment(state, choice, '
                                         'state.table(16740474), controls, live)'},
 'choose_second_duel_equipment': {'signature': 'state: SceneState, choice: Table, controls: '
                                               'DuelControlContext, *, live: DuelTurnFrame | None=None',
                                  'returns': 'DuelControlContext',
                                  'flow': 'return _choose_duel_equipment(state, choice, '
                                          'state.table(16740554), controls, live)'},
 '_choose_duel_ai_panel': {'signature': 'state, actor, opponent, controls, preparation=None',
                           'returns': None,
                           'flow': 'if type(preparation) is not DuelPreparationContext:\n'
                                   "    raise Boundary('automatic panel requires actual post-refresh six "
                                   "values, response and live stack')\n"
                                   'preparation.validate(state)\n'
                                   'if actor is not preparation.actor or opponent is not '
                                   'preparation.opponent:\n'
                                   "    raise ValueError('panel must consume the actual caller actor "
                                   "views')\n"
                                   'if type(controls) is not DuelControlContext:\n'
                                   "    raise ValueError('actual current panel controls required')\n"
                                   'controls.validate()\n'
                                   'if (controls.command, controls.mode) != (preparation.frame.command, '
                                   'preparation.frame.comparison):\n'
                                   "    raise ValueError('panel controls must agree with current frame')\n"
                                   'attribute = actor.word(30)\n'
                                   'thresholds = state.table(162710).cursor()\n'
                                   'threshold_offset = scan_duel_thresholds(state, attribute, thresholds)\n'
                                   'pointer_offset = u16(threshold_offset << 1)\n'
                                   'handler = state.table(162722).long(pointer_offset)\n'
                                   'frame = replace(preparation.frame, lookup=thresholds)\n'
                                   'current = _actor_reframe(frame, replace_word(frame.command, attribute), '
                                   'replace_word(frame.comparison, pointer_offset), frame.distance, '
                                   'frame.factor, frame.weapon_difference, frame.variation)\n'
                                   'result = state.service_at(handler, DuelPreparationContext(current, '
                                   'preparation.response, actor, opponent, preparation.stack.advance(-4)))\n'
                                   'if type(result) is not DuelPreparationContext:\n'
                                   "    raise Boundary('live duel panel handler must return its typed "
                                   "completion')\n"
                                   'result.validate(state)\n'
                                   'return _preparation_with_frame(state, result, result.frame, '
                                   'stack=result.stack.advance(4))'},
 '_choose_duel_side_loadout': {'signature': 'state, second, controls, preparation=None',
                               'returns': None,
                               'flow': 'if preparation is None:\n'
                                       "    raise Boundary('loadout requires actual current eight values, "
                                       "views and entry SP')\n"
                                       'preparation.validate(state)\n'
                                       'controls.validate()\n'
                                       'if (controls.command, controls.mode) != (preparation.frame.command, '
                                       'preparation.frame.comparison):\n'
                                       "    raise ValueError('loadout controls must agree with the current "
                                       "preparation')\n"
                                       'current, _ = _choose_complete_duel_loadout(state, second, '
                                       'preparation)\n'
                                       'return DuelControlContext(current.frame.command, '
                                       'current.frame.comparison).validate()'},
 '_wait_duel_status_text': {'signature': 'state, second, controls, preparation=None',
                            'returns': None,
                            'flow': 'if preparation is None:\n'
                                    "    raise Boundary('status wait requires current full preparation, not "
                                    "two controls')\n"
                                    'return _wait_complete_status(state, second, preparation)'},
 '_wait_complete_status': {'signature': 'state, second, preparation',
                           'returns': None,
                           'flow': 'preparation.validate(state)\n'
                                   'if type(second) is not bool:\n'
                                   "    raise ValueError('actual status side required')\n"
                                   'state.table(16740512 if second else 16740432).set_word(2, 0)\n'
                                   'current = _duel_from_preparation(state, preparation)\n'
                                   'state.set_status_word(9472)\n'
                                   'while True:\n'
                                   '    current = _duel_loadout_ack(state, current)\n'
                                   '    if not second:\n'
                                   '        current = _duel_call_frame(state, _advance_duel_loadout_palette, '
                                   'current)\n'
                                   '    current = _duel_call_frame(state, refresh_duel_actors_complete, '
                                   'current)\n'
                                   "    if state.scalar('ram_700c_word') != 0:\n"
                                   '        continue\n'
                                   '    current = _duel_call_frame(state, _duel_complete_controls, current, '
                                   'second)\n'
                                   '    current = replace(current, command=replace_word(current.command, '
                                   'low16(current.command) & 240))\n'
                                   '    if low16(current.command) != 0:\n'
                                   '        return _duel_preparation_from_turn(state, '
                                   '_duel_observed_move(current, low16(current.command), 16))'},
 '_commit_complete_duel_loadout': {'signature': 'state, preparation, second',
                                   'returns': None,
                                   'flow': 'preparation.validate(state)\n'
                                           'if type(second) is not bool:\n'
                                           "    raise ValueError('actual selected loadout side required')\n"
                                           'state.set_status_word(9984)\n'
                                           'current = replace(_duel_from_preparation(state, preparation), '
                                           'actor=state.table(16740512 if second else 16740432))\n'
                                           'current = _duel_call_frame(state, '
                                           '_configure_duel_loadout_motion, current)\n'
                                           'current = _duel_call_frame(state, clear_duel_text_complete, '
                                           'current)\n'
                                           'return _duel_preparation_from_turn(state, current)'},
 '_prepare_complete_second_status': {'signature': 'state, preparation',
                                     'returns': None,
                                     'flow': 'from .business_reuse import _reuse_advance_random_pair\n'
                                             'preparation.validate(state)\n'
                                             'random = _reuse_advance_random_pair(state)\n'
                                             'selection = low16(random.sample) & 3\n'
                                             'if selection == 3:\n'
                                             '    selection = 0\n'
                                             'selection = u16(selection + 3)\n'
                                             'current = replace(_duel_from_preparation(state, preparation), '
                                             'command=replace_word(random.sample, selection), '
                                             'comparison=random.updated_state)\n'
                                             'current = _duel_call_frame(state, '
                                             '_choose_complete_status_text, current, selection)\n'
                                             'current = replace(current, '
                                             'command=replace_word(current.command, 165))\n'
                                             '_sound(state, 165)\n'
                                             'current = _wait_complete_status(state, True, '
                                             '_duel_preparation_from_turn(state, current))\n'
                                             'frame = replace(current.frame, '
                                             'command=replace_word(current.frame.command, 139))\n'
                                             '_sound(state, 139)\n'
                                             'return _preparation_with_frame(state, current, frame)'},
 '_initialization_values': {'signature': 'state, current, *, frame=None, response=None, glyph_work=None, '
                                         'source=None, destination=None, glyph_source=None, stack=None',
                            'returns': None,
                            'flow': 'current.validate(state)\n'
                                    'preparation = current.preparation\n'
                                    'frame = preparation.frame if frame is None else frame\n'
                                    'actual_response = frame.response if response is None else response\n'
                                    'actual_working = frame.working_value if glyph_work is None else '
                                    'glyph_work\n'
                                    'actual_lookup = frame.lookup if glyph_source is None else glyph_source\n'
                                    'if actual_response is None or actual_working is None or actual_lookup '
                                    'is None:\n'
                                    "    raise Boundary('initialization must consume the current actual "
                                    "frame, not an older glyph snapshot')\n"
                                    'frame = replace(frame, working_value=actual_working, '
                                    'response=actual_response, lookup=actual_lookup)\n'
                                    'return DuelInitializationResult(DuelPreparationContext(frame, '
                                    'actual_response, preparation.actor if source is None else source, '
                                    'preparation.opponent if destination is None else destination, '
                                    'preparation.stack if stack is None else stack), actual_working, '
                                    'actual_lookup).validate(state)'},
 '_stage_complete_duel_packet': {'signature': 'state, current, source_address, command, rows, row_command',
                                 'returns': None,
                                 'flow': 'from .business_reuse import stage_sprite_word_packet\n'
                                         'from .contexts_reuse import SpritePacketContext\n'
                                         'current.validate(state)\n'
                                         'preparation, frame = (current.preparation, '
                                         'current.preparation.frame)\n'
                                         'source = state.table(source_address).cursor()\n'
                                         'packet = SpritePacketContext(command, '
                                         'replace_word(frame.comparison, rows), replace_word(frame.distance, '
                                         'row_command), frame.factor, frame.weapon_difference, '
                                         'current.glyph_work, preparation.response, frame.variation, source, '
                                         'preparation.opponent.cursor(), current.glyph_source, '
                                         'preparation.stack.advance(-4))\n'
                                         'result = stage_sprite_word_packet(state, source, command, rows, '
                                         'row_command, packet)\n'
                                         'frame = _actor_reframe(frame, result.command, result.rows, '
                                         'result.row_command, result.remaining, result.token, '
                                         'result.rows_remaining, working_value=result.run_count, '
                                         'response=result.response, lookup=result.glyph_source)\n'
                                         'return _initialization_values(state, current, frame=frame, '
                                         'response=result.response, glyph_work=result.run_count, '
                                         'source=result.source, destination=result.destination, '
                                         'glyph_source=result.glyph_source, stack=result.stack.advance(4))'},
 '_choose_complete_duel_loadout': {'signature': 'state, second, preparation',
                                   'returns': None,
                                   'flow': 'outcome = choose_duel_loadout_complete(state, second, '
                                           '_duel_from_preparation(state, preparation))\n'
                                           'return (_duel_preparation_from_turn(state, outcome.frame), '
                                           "outcome.phase == 'second_committed')"},
 '_prepare_complete_first_status': {'signature': 'state, preparation',
                                    'returns': None,
                                    'flow': 'from .business_reuse import _reuse_advance_random_pair\n'
                                            'preparation.validate(state)\n'
                                            'random = _reuse_advance_random_pair(state)\n'
                                            'selection = low16(random.sample) & 3\n'
                                            'if selection == 3:\n'
                                            '    selection = 0\n'
                                            'current = replace(_duel_from_preparation(state, preparation), '
                                            'command=replace_word(random.sample, selection), '
                                            'comparison=random.updated_state)\n'
                                            'current = _duel_call_frame(state, _choose_complete_status_text, '
                                            'current, selection)\n'
                                            'current = replace(current, '
                                            'command=replace_word(current.command, 165))\n'
                                            '_sound(state, 165)\n'
                                            'current = _wait_complete_status(state, False, '
                                            '_duel_preparation_from_turn(state, current))\n'
                                            'state.set_status_word(9984)\n'
                                            'return _duel_preparation_from_turn(state, '
                                            '_duel_call_frame(state, clear_duel_text_complete, '
                                            '_duel_from_preparation(state, current)))'},
 '_initialize_duel_scene': {'signature': 'state, context',
                            'returns': None,
                            'flow': 'from .business_reuse import clear_video_sprite_plane, '
                                    'expand_glyph_stream\n'
                                    'from .contexts_reuse import GlyphColors, GlyphSavedValues\n'
                                    'from .contexts_scene import PacketTransferValues\n'
                                    'from .business_scene import flush_scene_transfer_queue\n'
                                    'if type(context) is not DuelInitializationContext:\n'
                                    "    raise Boundary('natural initialization requires explicit complete "
                                    "live-in and stack')\n"
                                    'context.validate(state)\n'
                                    'frame = replace(context.frame, working_value=context.glyph_work, '
                                    'response=context.response)\n'
                                    'state.set_status_word(9984)\n'
                                    "command = replace_word(frame.command, state.scalar('ram_f606_word'))\n"
                                    'command = replace_byte(command, low8(command) & 191)\n'
                                    'state.mmio_write(12582916, 2, low16(command))\n'
                                    "state.set_scalar('ram_f612_word', 0)\n"
                                    'cleared = clear_video_sprite_plane(state, context.response)\n'
                                    'response = cleared.response\n'
                                    'frame = _actor_reframe(frame, command, frame.comparison, '
                                    'frame.distance, frame.factor, frame.weapon_difference, '
                                    'cleared.variation)\n'
                                    'for command in (33592, 33336, 33799, 34156, 36151, 37524, 35587):\n'
                                    '    state.mmio_write(12582916, 2, command)\n'
                                    'first, second = (state.table(16740432), state.table(16740512))\n'
                                    'first.set_long(14, 4194304)\n'
                                    'first.set_word(24, 34816)\n'
                                    'first.set_word(2, 1)\n'
                                    'second.set_long(14, 16777216)\n'
                                    'second.set_word(24, 40960)\n'
                                    'second.set_word(2, 1)\n'
                                    "state.set_scalar('ram_70f0_word', 0)\n"
                                    "state.set_scalar('ram_70f6_word', 0)\n"
                                    "state.set_scalar('ram_70f8_word', 0)\n"
                                    'equipment = state.table(4294961800).cursor(u16(first.word(26) * 3))\n'
                                    'first.set_byte(43, equipment.next_byte())\n'
                                    'first.set_byte(45, equipment.next_byte())\n'
                                    'first.set_byte(47, equipment.byte())\n'
                                    'equipment_product = u32(second.word(26) * 3)\n'
                                    'equipment = state.table(4294961800).cursor(low16(equipment_product))\n'
                                    'second.set_byte(43, equipment.next_byte())\n'
                                    'second.set_byte(45, equipment.next_byte())\n'
                                    'second.set_byte(47, equipment.byte())\n'
                                    'state.mmio_write(12582916, 4, 1073741824)\n'
                                    '_upload_longs(state, state.table(443316).cursor(), 12287)\n'
                                    'state.mmio_write(12582916, 4, 1073741827)\n'
                                    '_upload_longs(state, state.table(564700).cursor(), 31)\n'
                                    'frame = _actor_reframe(frame, replace_word(frame.command, 1), '
                                    'replace_word(frame.comparison, 2), frame.distance, '
                                    'replace_word(frame.factor, 9), equipment_product, frame.variation)\n'
                                    'source, destination = (state.table(566310).cursor(), '
                                    'state.table(4294955776).cursor())\n'
                                    'glyph = expand_glyph_stream(state, source, destination, '
                                    'GlyphColors(frame.command, frame.comparison), frame.factor, '
                                    'GlyphSavedValues(frame.weapon_difference, context.glyph_work, response, '
                                    'frame.variation, state.table(562908), context.stack.advance(-4)))\n'
                                    'frame = _actor_reframe(frame, replace_word(frame.command, 65535), '
                                    'frame.comparison, frame.distance, glyph.remaining_carrier, '
                                    'glyph.saved.working, glyph.saved.pixels, '
                                    'working_value=glyph.saved.repeat, response=glyph.saved.response, '
                                    'lookup=glyph.saved.glyph_source)\n'
                                    'source = _upload_longs(state, state.table(4294955776).cursor(), 79)\n'
                                    'current = DuelInitializationResult(DuelPreparationContext(frame, '
                                    'glyph.saved.response, source, glyph.destination, '
                                    'glyph.saved.stack.advance(4)), glyph.saved.repeat, '
                                    'glyph.saved.glyph_source).validate(state)\n'
                                    'state.mmio_write(12582916, 4, 1342177283)\n'
                                    '_upload_longs(state, state.table(492468).cursor(), 47)\n'
                                    'state.mmio_write(12582916, 4, 1107296259)\n'
                                    'for actor in (first, second):\n'
                                    '    frame = current.preparation.frame\n'
                                    '    frame = _actor_reframe(frame, replace_word(frame.command, 1), '
                                    'replace_word(frame.comparison, 2), frame.distance, frame.factor, '
                                    'frame.weapon_difference, frame.variation)\n'
                                    '    current = _initialization_values(state, current, frame=frame)\n'
                                    '    current = _duel_call_initialization(state, '
                                    'upload_duel_officer_name, current, actor.word(26), '
                                    'DuelGlyphContext(frame.command, frame.comparison, frame.factor))\n'
                                    'frame = current.preparation.frame\n'
                                    'frame = _actor_reframe(frame, replace_word(frame.command, 1), '
                                    'replace_word(frame.comparison, 2), frame.distance, '
                                    'replace_word(frame.factor, 1), frame.weapon_difference, '
                                    'frame.variation)\n'
                                    'current = _initialization_values(state, current, frame=frame)\n'
                                    'current = _duel_call_initialization(state, upload_duel_glyph_strip, '
                                    'current, state.table(166074).cursor(), DuelGlyphContext(frame.command, '
                                    'frame.comparison, frame.factor))\n'
                                    'cleared_frame = _duel_call_frame(state, clear_duel_text_complete, '
                                    '_duel_from_preparation(state, current.preparation))\n'
                                    'current = _initialization_values(state, current, '
                                    'frame=_turn_actor_values(cleared_frame), source=cleared_frame.actor, '
                                    'destination=cleared_frame.opponent, stack=cleared_frame.stack)\n'
                                    'source, destination = (state.table(163968).cursor(), '
                                    'state.table(4294966016).cursor())\n'
                                    'for _ in range(32):\n'
                                    '    destination.append_long(source.next_long())\n'
                                    'frame = current.preparation.frame\n'
                                    'current = _initialization_values(state, current, '
                                    'frame=_actor_reframe(frame, replace_word(frame.command, 65535), '
                                    'frame.comparison, frame.distance, frame.factor, '
                                    'frame.weapon_difference, frame.variation), source=source, '
                                    'destination=destination)\n'
                                    "state.set_scalar('ram_f31e_word', 1)\n"
                                    'map_source = state.table(492660).cursor()\n'
                                    "if state.scalar('ram_70f2_word') == 3:\n"
                                    '    map_source = state.table(493142).cursor()\n'
                                    'frame = current.preparation.frame\n'
                                    'lane_stack = current.preparation.stack.advance(-4)\n'
                                    'lanes = decode_duel_byte_lanes(state, map_source, '
                                    'state.table(16736256).cursor(), 1280, frame.distance, frame.factor, '
                                    'length_carrier=replace_word(frame.command, 1280), '
                                    'count_carrier=frame.comparison, stack=lane_stack)\n'
                                    'frame = _actor_reframe(frame, replace_word(lanes.length_carrier, '
                                    '65535), lanes.count_carrier, lanes.repeat_value, lanes.pair_value, '
                                    'frame.weapon_difference, frame.variation)\n'
                                    'current = _initialization_values(state, current, frame=frame, '
                                    'source=lanes.source, destination=lanes.destination, '
                                    'stack=lane_stack.advance(4))\n'
                                    'state.mmio_write(12582916, 4, 1610612739)\n'
                                    '_upload_words(state, state.table(16736256).cursor(), 1279)\n'
                                    'lane_stack = current.preparation.stack.advance(-4)\n'
                                    'lanes = decode_duel_byte_lanes(state, state.table(493630).cursor(), '
                                    'state.table(16736256).cursor(), 1280, frame.distance, frame.factor, '
                                    'length_carrier=replace_word(frame.command, 1280), '
                                    'count_carrier=frame.comparison, stack=lane_stack)\n'
                                    'frame = _actor_reframe(frame, replace_word(lanes.length_carrier, '
                                    '65535), lanes.count_carrier, lanes.repeat_value, lanes.pair_value, '
                                    'frame.weapon_difference, frame.variation)\n'
                                    'current = _initialization_values(state, current, frame=frame, '
                                    'source=lanes.source, destination=lanes.destination, '
                                    'stack=lane_stack.advance(4))\n'
                                    'state.mmio_write(12582916, 4, 1879048195)\n'
                                    '_upload_words(state, state.table(16736256).cursor(), 1279)\n'
                                    "state.set_scalar('ram_f694_word', 1539)\n"
                                    "state.set_scalar('ram_f692_word', 1540)\n"
                                    'current = _stage_complete_duel_packet(state, current, 164128, '
                                    '1610612776, 3, 59904)\n'
                                    'frame = current.preparation.frame\n'
                                    'flushed = flush_scene_transfer_queue(state, '
                                    'PacketTransferValues(frame.command, frame.comparison, frame.distance, '
                                    'frame.factor))\n'
                                    'if flushed is not None:\n'
                                    '    values = flushed.values\n'
                                    '    frame = _actor_reframe(frame, values.command, values.increment, '
                                    'values.address, values.spill, frame.weapon_difference, '
                                    'frame.variation)\n'
                                    '    current = _initialization_values(state, current, frame=frame, '
                                    'source=flushed.source)\n'
                                    'current = _stage_complete_duel_packet(state, current, 164212, '
                                    '1610612776, 5, 60288)\n'
                                    'return current'},
 '_duel_legacy_menu_input': {'signature': 'state, choice, controls, live',
                             'returns': None,
                             'flow': 'if live is None:\n'
                                     "    raise Boundary('loadout menu requires the actual current eight "
                                     "values, views and SP')\n"
                                     'checked_duel_turn(live, state)\n'
                                     'if (choice.base, controls.command, controls.mode) != (live.actor.base, '
                                     'live.command, live.comparison):\n'
                                     "    raise ValueError('loadout observations must agree with current "
                                     "choice and values')\n"
                                     'return live'},
 '_finish_duel_loadout_menu': {'signature': 'state, frame',
                               'returns': None,
                               'flow': "timer = state.scalar('ram_70fa_word')\n"
                                       "state.set_scalar('ram_70fa_word', u16(timer - 1))\n"
                                       'return _duel_observed_comparison(frame, timer, 1, '
                                       '16).validate(state)'},
 '_highlight_duel_loadout_choice': {'signature': 'state, frame, vertical_base',
                                    'returns': None,
                                    'flow': 'frame = replace(frame, command=replace_word(frame.command, '
                                            'low16(frame.command) & 12))\n'
                                            'if low16(frame.command) == 0:\n'
                                            "    blink = state.scalar('ram_7008_word')\n"
                                            '    frame = replace(frame, command=replace_word(frame.command, '
                                            'blink & 8))\n'
                                            '    if low16(frame.command) == 0:\n'
                                            '        return frame\n'
                                            'selected = frame.actor.word()\n'
                                            'product = u32(selected * 56)\n'
                                            'frame = replace(frame, command=replace_word(frame.command, '
                                            '200), comparison=replace_word(product, u16(product + '
                                            'vertical_base)), distance=replace_word(frame.distance, 67), '
                                            'factor=replace_word(frame.factor, 32768))\n'
                                            'return _append_duel_menu_cursor(state, frame)'},
 'choose_duel_two_option_menu_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame',
                                          'returns': 'DuelTurnFrame',
                                          'flow': 'checked_duel_turn(frame, state)\n'
                                                  'frame = replace(frame, '
                                                  'comparison=replace_word(frame.comparison, '
                                                  'frame.actor.word()), command=replace_word(frame.command, '
                                                  'low16(frame.command) & 12))\n'
                                                  'if low16(frame.command) != 0:\n'
                                                  '    frame = replace(frame, '
                                                  'distance=replace_word(frame.distance, 1), '
                                                  'command=replace_word(frame.command, low16(frame.command) '
                                                  '& 8))\n'
                                                  '    if low16(frame.command) == 0:\n'
                                                  '        frame = replace(frame, '
                                                  'distance=replace_word(frame.distance, 65535))\n'
                                                  '    selected = u16(frame.comparison + frame.distance)\n'
                                                  '    frame = replace(frame, '
                                                  'comparison=replace_word(frame.comparison, selected))\n'
                                                  '    if selected < 2:\n'
                                                  '        frame.actor.set_word(0, selected)\n'
                                                  'frame = _duel_call_frame(state, _duel_complete_controls, '
                                                  'frame, False)\n'
                                                  'if not frame.command & 32:\n'
                                                  '    frame = _highlight_duel_loadout_choice(state, frame, '
                                                  '121)\n'
                                                  'return _finish_duel_loadout_menu(state, frame)'},
 '_choose_duel_equipment_complete': {'signature': 'state, equipment, frame',
                                     'returns': None,
                                     'flow': 'checked_duel_turn(frame, state)\n'
                                             'equipment = _live_table(state, equipment)\n'
                                             'while True:\n'
                                             '    selected = frame.actor.word()\n'
                                             '    frame = replace(frame, '
                                             'comparison=replace_word(frame.comparison, selected))\n'
                                             '    if _equipment_available(equipment, selected):\n'
                                             '        break\n'
                                             '    frame.actor.set_word(0, u16(frame.actor.word() + 1))\n'
                                             '    if frame.actor.word() >= 3:\n'
                                             '        frame.actor.set_word(0, 0)\n'
                                             'frame = replace(frame, '
                                             'comparison=replace_word(frame.comparison, frame.actor.word()), '
                                             'command=replace_word(frame.command, low16(frame.command) & '
                                             '12))\n'
                                             'if low16(frame.command) != 0:\n'
                                             '    frame = replace(frame, '
                                             'distance=replace_word(frame.distance, 1), '
                                             'command=replace_word(frame.command, low16(frame.command) & '
                                             '8))\n'
                                             '    if low16(frame.command) == 0:\n'
                                             '        frame = replace(frame, '
                                             'distance=replace_word(frame.distance, 65535))\n'
                                             '    while True:\n'
                                             '        selected = u16(frame.comparison + frame.distance)\n'
                                             '        frame = replace(frame, '
                                             'comparison=replace_word(frame.comparison, selected))\n'
                                             '        if negative_word(selected):\n'
                                             '            frame = replace(frame, comparison=2)\n'
                                             '        elif selected >= 3:\n'
                                             '            frame = replace(frame, comparison=0)\n'
                                             '        if _equipment_available(equipment, '
                                             'low16(frame.comparison)):\n'
                                             '            break\n'
                                             '    if low16(frame.comparison) < 3:\n'
                                             '        frame.actor.set_word(0, low16(frame.comparison))\n'
                                             'frame = _duel_call_frame(state, _duel_complete_controls, '
                                             'frame, False)\n'
                                             'if not frame.command & 32:\n'
                                             '    frame = _highlight_duel_loadout_choice(state, frame, 104)\n'
                                             'return _finish_duel_loadout_menu(state, frame)'},
 'choose_first_duel_equipment_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame',
                                          'returns': 'DuelTurnFrame',
                                          'flow': 'return _choose_duel_equipment_complete(state, '
                                                  'state.table(16740474), frame)'},
 'choose_second_duel_equipment_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame',
                                           'returns': 'DuelTurnFrame',
                                           'flow': 'return _choose_duel_equipment_complete(state, '
                                                   'state.table(16740554), frame)'},
 '_duel_call_initialization': {'signature': 'state, function, current, *args',
                               'returns': None,
                               'flow': 'current.validate(state)\n'
                                       'called = _initialization_values(state, current, '
                                       'stack=current.preparation.stack.advance(-4))\n'
                                       'returned = function(state, *args, called).validate(state)\n'
                                       'return _initialization_values(state, returned, '
                                       'stack=returned.preparation.stack.advance(4))'},
 '_duel_preparation_from_turn': {'signature': 'state, frame',
                                 'returns': None,
                                 'flow': 'checked_duel_turn(frame, state)\n'
                                         'return DuelPreparationContext(_turn_actor_values(frame), '
                                         'frame.response, frame.actor, frame.opponent, '
                                         'frame.stack).validate(state)'},
 '_advance_duel_loadout_palette': {'signature': 'state, frame',
                                   'returns': None,
                                   'flow': 'preparation = advance_duel_entry_palette(state, '
                                           '_duel_preparation_from_turn(state, frame))\n'
                                           'return _duel_from_preparation(state, preparation)'},
 '_configure_duel_loadout_motion': {'signature': 'state, frame',
                                    'returns': None,
                                    'flow': 'fields = configure_duel_weapon_motion(state, frame.actor, '
                                            '_turn_actor_values(frame))\n'
                                            'return _turn_from_actor(state, frame, fields, frame.actor, '
                                            'frame.opponent, frame.stack)'},
 '_choose_complete_status_text': {'signature': 'state, selection, frame',
                                  'returns': None,
                                  'flow': 'return choose_duel_status_text_complete(state, selection, frame)'},
 '_duel_loadout_ack': {'signature': 'state, frame',
                       'returns': None,
                       'flow': 'checked_duel_turn(frame, state)\n'
                               "state.set_scalar('ram_f612_word', 1792)\n"
                               'while True:\n'
                               '    pending = state.read(4294964754, 1)\n'
                               '    frame = _duel_observed_move(frame, pending, 8)\n'
                               '    if pending == 0:\n'
                               '        return frame\n'
                               "    state.progress('duel_frame_low_byte_ack')"},
 '_stage_duel_loadout_packet': {'signature': 'state, source_address, row_command, frame',
                                'returns': None,
                                'flow': 'from .linkage_duel_round import stage_duel_turn_packet\n'
                                        'current = replace(frame, command=1610612740, '
                                        'comparison=replace_word(frame.comparison, 1), '
                                        'distance=replace_word(frame.distance, row_command), '
                                        'actor=state.table(source_address).cursor())\n'
                                        'return stage_duel_turn_packet(state, current)'},
 'choose_duel_loadout_complete': {'signature': 'state: SceneState, second: bool, frame: DuelTurnFrame',
                                  'returns': 'DuelLoadoutOutcome',
                                  'flow': 'checked_duel_turn(frame, state)\n'
                                          'if type(second) is not bool:\n'
                                          "    raise ValueError('actual loadout side required')\n"
                                          "mode_name = 'ram_700b_byte' if second else 'ram_700a_byte'\n"
                                          'if state.scalar(mode_name) != 3:\n'
                                          '    _configure_duel_dialog(state, 50688, 166078)\n'
                                          '    if second:\n'
                                          "        state.set_scalar('ram_70da_word', 1)\n"
                                          'if not second:\n'
                                          '    frame = _duel_call_frame(state, '
                                          '_advance_duel_loadout_palette, frame)\n'
                                          'state.set_status_word(9472)\n'
                                          'while True:\n'
                                          '    frame = _duel_loadout_ack(state, frame)\n'
                                          '    frame = _duel_call_frame(state, '
                                          '_advance_duel_loadout_palette, frame)\n'
                                          '    frame = _duel_call_frame(state, refresh_duel_actors_complete, '
                                          'frame)\n'
                                          '    if not second:\n'
                                          "        state.set_scalar('ram_708a_word', 0)\n"
                                          '    if state.scalar(mode_name) == 3:\n'
                                          '        frame = replace(frame, actor=state.table(16740512 if '
                                          'second else 16740432))\n'
                                          '        preparation = _duel_preparation_from_turn(state, frame)\n'
                                          '        preparation = _choose_duel_ai_panel(state, frame.actor, '
                                          'frame.opponent, DuelControlContext(frame.command, '
                                          'frame.comparison), preparation)\n'
                                          '        frame = _duel_from_preparation(state, preparation)\n'
                                          '        selected_second = frame.actor.base != 16740432\n'
                                          '        if not selected_second and low16(frame.response) == 0:\n'
                                          "            second, mode_name = (False, 'ram_700a_byte')\n"
                                          '            continue\n'
                                          '        second = selected_second\n'
                                          '        break\n'
                                          '    frame = replace(frame, actor=state.table(16740524 if second '
                                          'else 16740444))\n'
                                          '    frame = _duel_call_frame(state, _duel_complete_controls, '
                                          'frame, second)\n'
                                          '    frame = _duel_call_frame(state, '
                                          'choose_second_duel_equipment_complete if second else '
                                          'choose_first_duel_equipment_complete, frame)\n'
                                          "    pending = state.scalar('ram_700c_word')\n"
                                          '    frame = _duel_observed_move(frame, pending, 16)\n'
                                          '    if pending != 0:\n'
                                          '        continue\n'
                                          '    frame = _duel_call_frame(state, _stage_duel_loadout_packet, '
                                          'frame, 164354 if second else 164332, 60740 if second else 60680)\n'
                                          '    frame = _duel_call_frame(state, _duel_complete_controls, '
                                          'frame, second)\n'
                                          '    frame = replace(frame, command=replace_word(frame.command, '
                                          'low16(frame.command) & 240))\n'
                                          '    frame = _duel_observed_move(frame, low16(frame.command), 16)\n'
                                          '    if low16(frame.command) == 0:\n'
                                          '        continue\n'
                                          '    frame = replace(frame, command=replace_word(frame.command, '
                                          '172))\n'
                                          '    _sound(state, 172)\n'
                                          '    if state.scalar(mode_name) == 3:\n'
                                          '        break\n'
                                          '    frame = _duel_call_frame(state, clear_duel_text_complete, '
                                          'frame)\n'
                                          '    _configure_duel_dialog(state, 50688, 166154)\n'
                                          '    state.set_status_word(9472)\n'
                                          '    while True:\n'
                                          '        frame = _duel_loadout_ack(state, frame)\n'
                                          '        frame = _duel_call_frame(state, '
                                          '_advance_duel_loadout_palette, frame)\n'
                                          '        frame = _duel_call_frame(state, '
                                          'refresh_duel_actors_complete, frame)\n'
                                          '        frame = replace(frame, actor=state.table(16740578 if '
                                          'second else 16740498))\n'
                                          '        frame = _duel_call_frame(state, _duel_complete_controls, '
                                          'frame, second)\n'
                                          '        frame = _duel_call_frame(state, '
                                          'choose_duel_two_option_menu_complete, frame)\n'
                                          "        pending = state.scalar('ram_700c_word')\n"
                                          '        frame = _duel_observed_move(frame, pending, 16)\n'
                                          '        if pending != 0:\n'
                                          '            continue\n'
                                          '        frame = _duel_call_frame(state, _duel_complete_controls, '
                                          'frame, second)\n'
                                          '        frame = replace(frame, '
                                          'command=replace_word(frame.command, low16(frame.command) & 240))\n'
                                          '        frame = _duel_observed_move(frame, low16(frame.command), '
                                          '16)\n'
                                          '        if low16(frame.command) != 0:\n'
                                          '            break\n'
                                          '    frame = replace(frame, command=replace_word(frame.command, '
                                          '172))\n'
                                          '    _sound(state, 172)\n'
                                          '    frame = replace(frame, actor=state.table(16740578 if second '
                                          'else 16740498))\n'
                                          '    choice = frame.actor.word()\n'
                                          '    frame = _duel_observed_move(frame, choice, 16)\n'
                                          '    if choice != 0:\n'
                                          '        state.set_scalar(mode_name, 3)\n'
                                          '    break\n'
                                          'preparation = _commit_complete_duel_loadout(state, '
                                          '_duel_preparation_from_turn(state, frame), second)\n'
                                          "return DuelLoadoutOutcome('second_committed' if second else "
                                          "'first_committed', _duel_from_preparation(state, "
                                          'preparation)).validate(state)'}}
DECLARATIONS.update(HOST_MANUAL_LOADOUT_DECLARATIONS)
APPROVED.setdefault('contexts_duel', set()).update({'DuelLoadoutOutcome'})
APPROVED.setdefault('linkage_duel_round', set()).update({'stage_duel_turn_packet'})


# Root49 sole full retained-field duel strategy and legacy projections.
DECLARATIONS.update({'scan_duel_thresholds': {'signature': 'state: SceneState, value: Word, thresholds: Cursor', 'returns': 'Word', 'flow': 'uint(value, 16)\nthresholds = _live_cursor(state, thresholds)\nframe = first_replace(FirstDeploymentFrame.unobserved(), target_x=value, controller=thresholds)\nreturned = scan_duel_thresholds_fields(state, frame)\nthresholds.base = returned.controller.base\nreturn low16(returned.target_y)'}, 'measure_duel_weapon_contact': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: DuelActorFrame | None=None', 'returns': 'DuelContact', 'flow': 'entered = _duel_strategy_partial_fields(state, actor, opponent, frame)\nreturned = measure_duel_weapon_contact_fields(state, entered)\ncurrent = _duel_strategy_actor_values(returned)\nreturn DuelContact(low16(returned.unit), low16(returned.count), bool(returned.status & 1), current)'}, 'sample_duel_probability': {'signature': 'state: SceneState, source_word: Word, frame: DuelActorFrame | None=None', 'returns': 'DuelProbability', 'flow': 'uint(source_word, 16)\nentered = _duel_strategy_partial_fields(state, None, None, frame)\nentered = first_replace(entered, unit=source_word if entered.unit is None else replace_word(entered.unit, source_word))\nreturned = sample_duel_probability_fields(state, entered)\nreturn DuelProbability(returned.target_x, low16(returned.unit), low16(returned.count), bool(returned.status & 1), _duel_strategy_actor_values(returned))'}, 'choose_duel_ai_timeout': {'signature': 'state: SceneState, actor: Table, opponent: Table, command: Long, override: Word, frame: DuelActorFrame | None=None', 'returns': 'DuelAIResult', 'flow': 'uint(command, 32)\nuint(override, 16)\nentered = _duel_strategy_partial_fields(state, actor, opponent, frame)\nentered = first_replace(entered, target_x=command, choice=override if entered.choice is None else replace_word(entered.choice, override))\nreturned = choose_duel_ai_timeout_fields(state, entered)\ncurrent = _duel_strategy_actor_values(returned)\nreturn DuelAIResult(current.command, current.comparison, low16(current.response), low16(current.variation), current.retained, current, current.response)'}, '_choose_duel_ai_override_current': {'signature': 'state, actor, opponent, threshold_offset, frame', 'returns': None, 'flow': 'uint(threshold_offset, 16)\nentered = _duel_strategy_partial_fields(state, actor, opponent, frame)\nentered = first_replace(entered, offset_y=threshold_offset if entered.offset_y is None else replace_word(entered.offset_y, threshold_offset))\nreturned = choose_duel_ai_override_fields(state, entered)\nreturn DuelOverrideResult(_duel_strategy_actor_values(returned), low16(returned.choice)).validate()'}, '_sample_duel_live_mode_values': {'signature': 'state, source, threshold_offset, second, frame', 'returns': None, 'flow': 'uint(threshold_offset, 16)\nentered = _duel_strategy_partial_fields(state, None, None, frame)\nentered = first_replace(entered, offset_y=threshold_offset if entered.offset_y is None else replace_word(entered.offset_y, threshold_offset))\nentered = _resource_cost_frame(state, entered, source)\nreturned = _duel_strategy_live_mode_fields(state, entered, source, second)\nreturn DuelProbability(returned.target_x, low16(returned.unit), low16(returned.count), bool(returned.status & 1), _duel_strategy_actor_values(returned))'}, 'choose_duel_ai_command': {'signature': 'state: SceneState, actor: Table, opponent: Table, context: DuelAIContext=DuelAIContext()', 'returns': 'DuelAIResult', 'flow': 'context.validate()\nif context.live is not None:\n    checked_duel_turn(context.live, state)\n    current = _turn_actor_values(context.live)\nelse:\n    retained = context.retained\n    current = DuelActorFrame(context.command, context.comparison, retained.distance if retained is not None else None, retained.factor if retained is not None else None, retained.weapon_difference if retained is not None else None, retained.variation if retained is not None else None, response=context.response)\nentered = _duel_strategy_partial_fields(state, actor, opponent, current)\nreturned = choose_duel_ai_command_fields(state, entered)\ncurrent = _duel_strategy_actor_values(returned)\nreturn DuelAIResult(current.command, current.comparison, low16(current.response), low16(current.variation), current.retained, current, current.response)'}, '_duel_strategy_actor_values': {'signature': 'frame', 'returns': None, 'flow': 'return DuelActorFrame(frame.target_x, frame.target_y, frame.unit, frame.count, frame.distance, frame.choice, frame.offset_x, frame.offset_y, frame.controller).validate()'}, '_duel_strategy_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, target)\nif target == 33748:\n    return sample_battle_action_random_fields(BattlePolicyMemory(state), frame, continuation)\ndef algorithm(memory, entered):\n    if target == 167824:\n        return scan_duel_thresholds_fields(memory.state, entered)\n    if target == 173556:\n        return choose_duel_ai_override_fields(memory.state, entered)\n    if target == 174592:\n        return sample_duel_probability_fields(memory.state, entered)\n    if target == 174688:\n        return choose_duel_ai_timeout_fields(memory.state, entered)\n    raise MovementContinuationBoundary(target, entered, 'actual indexed duel strategy target is not yet restored')\nreturn _presentation_call_fields(BattlePresentationMemory(state), frame, continuation, algorithm)"}, '_duel_strategy_live_mode_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, branch: int, second: bool', 'returns': 'FirstDeploymentFrame', 'flow': "mode_selector = 2\nif branch not in (173868, 174040, 174204, 174370) or type(second) is not bool:\n    raise ValueError('original duel probability family required')\ntable, first_return, second_return = {173868: (173962, 173910, 173956), 174040: (174132, 174082, 174128), 174204: (174298, 174246, 174292), 174370: (174464, 174412, 174458)}[branch]\nmode = state.read(4294963154, 2)\nframe = _movement_test(state, frame, mode, 16)\nif mode != 0:\n    mode = state.read(4294963154, 2)\n    frame = _movement_compare(state, frame, mode, mode_selector, 16)\n    table += 48 if mode == mode_selector else 24\nif second:\n    table += 12\nreturn _duel_strategy_probability_fields(state, frame, table, second_return if second else first_return)"}, '_duel_strategy_partial_fields': {'signature': 'state, actor, opponent, frame', 'returns': None, 'flow': "current = DuelActorFrame() if frame is None else frame\nif type(current) is not DuelActorFrame:\n    raise ValueError('actual duel actor observations required')\ncurrent.validate()\nfor view in (actor, opponent):\n    if view is not None:\n        _live_table(state, view)\nreturn first_replace(FirstDeploymentFrame.unobserved(), target_x=current.command, target_y=current.comparison, unit=current.distance, count=current.factor, distance=current.weapon_difference, offset_x=current.working_value, offset_y=current.response, choice=current.variation, roster=actor.cursor() if actor is not None else None, candidates=opponent.cursor() if opponent is not None else None, controller=current.lookup.cursor() if current.lookup is not None else None)"}, '_duel_strategy_probability_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, table: int, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': "value = state.read(u32(table + s16(low16(frame.offset_y))), 2)\nframe = _movement_move(state, frame, 'unit', value, 16)\nreturn _duel_strategy_call_fields(state, frame, 174592, continuation)"}, 'choose_duel_ai_command_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "cooldown_step = 1\ncooldown_mask = 31\ncooldown_bias = 30\nopponent_zero_command = 256\nprofile_shift = 1\nexecutor_shift = 2\nframe = _resource_cost_frame(state, frame, 172698)\ncooldown = frame.roster.word(34)\nframe = _movement_test(state, frame, cooldown, 16)\nif not frame.status & 4:\n    frame, cooldown = _movement_binary_flags(state, frame, frame.roster.word(34), cooldown_step, 16, True)\n    frame.roster.set_word(34, cooldown)\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(28), 16)\nif frame.status & 4:\n    frame.roster.set_word(2, low16(frame.target_x))\n    frame = _movement_test(state, frame, low16(frame.target_x), 16)\n    frame.roster.set_word(4, low16(frame.target_x))\n    return _movement_test(state, frame, low16(frame.target_x), 16)\nframe = _movement_move(state, frame, 'target_x', frame.candidates.word(28), 16)\nif frame.status & 4:\n    return _movement_move(state, frame, 'target_x', opponent_zero_command, 16)\nframe = _movement_test(state, frame, frame.roster.word(34), 16)\nif frame.status & 4:\n    frame = _duel_strategy_call_fields(state, frame, 33748, 172748)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & cooldown_mask, 16)\n    frame = _movement_add_word(state, frame, 'target_x', cooldown_bias)\n    frame.roster.set_word(34, low16(frame.target_x))\n    frame = _movement_test(state, frame, low16(frame.target_x), 16)\n    frame = _movement_move(state, frame, 'target_x', frame.roster.word(30), 16)\n    frame = first_replace(frame, controller=state.table_at(172808).cursor())\n    frame = _duel_strategy_call_fields(state, frame, 167824, 172774)\n    frame = _movement_move(state, frame, 'offset_y', low16(frame.target_y), 16)\n    frame = _duel_strategy_call_fields(state, frame, 173556, 172780)\n    frame = _duel_strategy_call_fields(state, frame, 174688, 172784)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.choice), 16)\n    frame = _movement_test(state, frame, low16(frame.target_x), 16)\n    if not frame.status & 4:\n        return frame\n    frame = _movement_move(state, frame, 'target_y', low16(frame.offset_y), 16)\n    frame = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_y', low16(frame.target_y), profile_shift)\n    target = u32(172820 + s16(low16(frame.target_y)))\n    frame = _duel_strategy_call_fields(state, frame, target, 172798)\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(36), 16)\nframe = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_x', low16(frame.target_x), executor_shift)\ntarget = u32(172844 + s16(low16(frame.target_x)))\nraise MovementContinuationBoundary(target, frame, 'original indexed duel executor JMP, no extra call slot or fabricated RTS')"}, 'choose_duel_ai_override_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "tick_mask = 7\nfirst_opponent_bound = 51\nfirst_low_bound = 40\nfirst_high_bound = 70\nsecond_mid_bound = 50\nsecond_high_bound = 80\noffset_low_bound = 4\noffset_high_bound = 8\nfirst_low_opponent_mask = 1\nfirst_high_opponent_mask = 3\nfirst_low_or_mid_mask = 3\nfirst_high_or_mid_mask = 1\nfirst_high_weak_mask = 3\ncommand_40 = 64\ncommand_43 = 67\ncommand_42 = 66\ncommand_21 = 33\nframe = _resource_cost_frame(state, frame, 173556)\nframe = _movement_move(state, frame, 'choice', 0, 16)\nframe = _movement_move(state, frame, 'target_y', state.read(16740360, 2), 16)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_y) & tick_mask, 16)\nif not frame.status & 4:\n    return frame\nframe = _movement_compare_address(state, frame, frame.roster.base, 16740432)\nif frame.status & 4:\n    opponent_readiness = frame.candidates.word(28)\n    frame = _movement_compare(state, frame, opponent_readiness, first_opponent_bound, 16)\n    if opponent_readiness < first_opponent_bound:\n        frame = _duel_strategy_call_fields(state, frame, 33748, 173600)\n        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & first_low_opponent_mask, 16)\n        if frame.status & 4:\n            return _movement_move(state, frame, 'choice', command_40, 16)\n    else:\n        frame = _duel_strategy_call_fields(state, frame, 33748, 173620)\n        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & first_high_opponent_mask, 16)\n        if frame.status & 4:\n            return _movement_move(state, frame, 'choice', command_40, 16)\n        return frame\n    frame = _movement_move(state, frame, 'unit', frame.candidates.word(30), 16)\n    frame = _movement_move(state, frame, 'count', frame.roster.word(30), 16)\n    frame = _movement_move(state, frame, 'target_y', frame.roster.word(28), 16)\n    readiness = low16(frame.target_y)\n    opponent_strength, own_strength = (low16(frame.unit), low16(frame.count))\n    frame = _movement_compare(state, frame, readiness, first_low_bound, 16)\n    if readiness < first_low_bound:\n        frame = _duel_strategy_call_fields(state, frame, 33748, 173708)\n        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & first_low_or_mid_mask, 16)\n        if not frame.status & 4:\n            return _movement_move(state, frame, 'choice', command_43, 16)\n        return frame\n    frame = _movement_compare(state, frame, readiness, first_high_bound, 16)\n    if readiness >= first_high_bound:\n        frame = _movement_compare(state, frame, opponent_strength, own_strength, 16)\n        if opponent_strength >= own_strength:\n            frame = _duel_strategy_call_fields(state, frame, 33748, 173668)\n            frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & first_high_or_mid_mask, 16)\n            chosen = not frame.status & 4\n        else:\n            frame = _duel_strategy_call_fields(state, frame, 33748, 173690)\n            frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & first_high_weak_mask, 16)\n            chosen = bool(frame.status & 4)\n    else:\n        frame = _movement_compare(state, frame, opponent_strength, own_strength, 16)\n        if opponent_strength < own_strength:\n            frame = _duel_strategy_call_fields(state, frame, 33748, 173668)\n            frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & first_high_or_mid_mask, 16)\n        else:\n            frame = _duel_strategy_call_fields(state, frame, 33748, 173708)\n            frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & first_low_or_mid_mask, 16)\n        chosen = not frame.status & 4\n    return _movement_move(state, frame, 'choice', command_43, 16) if chosen else frame\nframe = _movement_move(state, frame, 'unit', frame.candidates.word(28), 16)\nframe = _movement_move(state, frame, 'count', frame.roster.word(28), 16)\nopponent_readiness, readiness = (low16(frame.unit), low16(frame.count))\nframe = _movement_compare(state, frame, opponent_readiness, readiness, 16)\nif opponent_readiness < readiness:\n    frame = _duel_strategy_probability_fields(state, frame, 174562, 174544)\n    if frame.status & 1:\n        return _movement_move(state, frame, 'choice', command_40, 16)\n    frame = _duel_strategy_probability_fields(state, frame, 174574, 174556)\n    return _movement_move(state, frame, 'choice', command_21, 16) if frame.status & 1 else frame\nframe = _movement_compare(state, frame, readiness, second_mid_bound, 16)\nif readiness >= second_mid_bound:\n    frame = _movement_compare(state, frame, readiness, second_high_bound, 16)\n    if readiness >= second_high_bound:\n        return frame\n    frame = _movement_move(state, frame, 'unit', frame.candidates.word(30), 16)\n    frame = _movement_move(state, frame, 'count', frame.roster.word(30), 16)\n    opponent_strength, own_strength = (low16(frame.unit), low16(frame.count))\n    frame = _movement_compare(state, frame, opponent_strength, own_strength, 16)\n    if opponent_strength >= own_strength:\n        frame = _duel_strategy_probability_fields(state, frame, 173748, 173794)\n    else:\n        frame = _duel_strategy_probability_fields(state, frame, 173810, 173830)\n    if frame.status & 1:\n        return _movement_move(state, frame, 'choice', command_43, 16)\n    frame = _duel_strategy_probability_fields(state, frame, 173760, 173804)\n    return _movement_move(state, frame, 'choice', command_40, 16) if frame.status & 1 else frame\nframe = _movement_move(state, frame, 'target_x', frame.candidates.word(30), 16)\nframe = first_replace(frame, controller=state.table_at(172808).cursor())\nframe = _duel_strategy_call_fields(state, frame, 167824, 173848)\nopponent_offset = low16(frame.target_y)\nframe = _movement_compare(state, frame, opponent_offset, offset_low_bound, 16)\nif opponent_offset < offset_low_bound:\n    branch = 174370\nelse:\n    frame = _movement_compare(state, frame, opponent_offset, offset_high_bound, 16)\n    if opponent_offset < offset_high_bound:\n        branch = 174204\n    elif opponent_offset == offset_high_bound:\n        branch = 174040\n    else:\n        branch = 173868\nframe = _duel_strategy_live_mode_fields(state, frame, branch, False)\nif frame.status & 1:\n    return _movement_move(state, frame, 'choice', command_43, 16)\nframe = _duel_strategy_live_mode_fields(state, frame, branch, True)\nreturn _movement_move(state, frame, 'choice', command_42, 16) if frame.status & 1 else frame"}, 'choose_duel_ai_timeout_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "timer_bound = 6144\nmode_bound = 771\ntimeout_command = 67\nframe = _resource_cost_frame(state, frame, 174688)\ntimer = state.read(16740602, 2)\nframe = _movement_compare(state, frame, timer, timer_bound, 16)\nif timer > timer_bound:\n    mode = state.read(16740362, 2)\n    frame = _movement_compare(state, frame, mode, mode_bound, 16)\n    if mode == mode_bound:\n        frame = _movement_move(state, frame, 'target_x', frame.roster.word(28), 16)\n        readiness = low16(frame.target_x)\n        opponent_readiness = frame.candidates.word(28)\n        frame = _movement_compare(state, frame, readiness, opponent_readiness, 16)\n        if readiness <= opponent_readiness:\n            return _movement_move(state, frame, 'choice', timeout_command, 16)\nreturn _movement_move_long(state, frame, 'target_x', 0)"}, 'measure_duel_weapon_contact_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "facing_bit = 8\nframe = _resource_cost_frame(state, frame, 172590)\nframe = _movement_move(state, frame, 'target_y', frame.roster.word(12), 16)\nframe = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_y', low16(frame.target_y), 1)\nreach = state.read(u32(172640 + s16(low16(frame.target_y))), 2)\nframe = _movement_move(state, frame, 'unit', reach, 16)\nframe = _postbattle_bit_fields(frame, bool(frame.roster.byte(24) & facing_bit))\nstate.sr = state.sr & 65504 | frame.status\nif frame.status & 4:\n    frame = _duel_commit_sub_word_fields(state, frame, 'unit', 0, True)\nframe = _movement_add_word(state, frame, 'unit', frame.roster.word(14))\nframe = _duel_commit_sub_word_fields(state, frame, 'unit', frame.candidates.word(14))\nframe = _movement_move(state, frame, 'count', low16(frame.unit), 16)\nif frame.status & 8:\n    frame = _duel_commit_sub_word_fields(state, frame, 'unit', 0, True)\nframe = _postbattle_bit_fields(frame, bool(frame.roster.byte(24) & facing_bit))\nstate.sr = state.sr & 65504 | frame.status\nif not frame.status & 4:\n    frame = _duel_commit_sub_word_fields(state, frame, 'count', 0, True)\nlimit = state.read(u32(172646 + s16(low16(frame.target_y))), 2)\nreturn _duel_commit_sub_word_fields(state, frame, 'unit', limit)"}, 'sample_duel_probability_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "probability_mask = 7\nprobability_shift = 4\nframe = _resource_cost_frame(state, frame, 174592)\nframe = _movement_move(state, frame, 'count', low16(frame.unit), 16)\nframe = _movement_move(state, frame, 'unit', low16(frame.unit) & probability_mask, 16)\nframe = _movement_fixed_shift_word(state, frame, 'count', probability_shift, True)\nframe = _duel_strategy_call_fields(state, frame, 33748, 174606)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & low16(frame.unit), 16)\nreturn _movement_compare(state, frame, low16(frame.target_x), low16(frame.count), 16)"}, 'scan_duel_thresholds_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 167824)\nframe = _movement_move(state, frame, 'target_y', 65534, 16)\nwhile True:\n    frame = _movement_add_word(state, frame, 'target_y', 2)\n    threshold = frame.controller.word()\n    frame = first_replace(frame, controller=frame.controller.advance(2))\n    frame = _movement_compare(state, frame, low16(frame.target_x), threshold, 16)\n    if low16(frame.target_x) < threshold:\n        return frame"}})
APPROVED.setdefault('contexts_scene',set()).update({'FirstDeploymentFrame', 'SceneRefreshMemory', 'first_replace'})
APPROVED.setdefault('business_scene',set()).update({'_scene_render_asl_word'})
APPROVED.setdefault('business_movement_support',set()).update({'_movement_binary_flags', '_movement_compare', '_movement_test', '_movement_move_long', '_movement_fixed_shift_word', '_movement_add_word', '_movement_test_long', '_movement_compare_address', '_movement_move'})
APPROVED.setdefault('business_city',set()).update({'_duel_commit_sub_word_fields', '_resource_cost_frame'})
APPROVED.setdefault('contexts_gameplay',set()).update({'MovementContinuationBoundary'})
APPROVED.setdefault('business_actions',set()).update({'sample_battle_action_random_fields'})
APPROVED.setdefault('contexts_policy_memory',set()).update({'BattlePolicyMemory'})
APPROVED.setdefault('business_battle',set()).update({'_presentation_call_fields', '_postbattle_bit_fields'})
APPROVED.setdefault('contexts_battle',set()).update({'BattlePresentationMemory'})


# Root50 real profile-call and executor-JMP parent bridges, no extra owners.
DECLARATIONS.update({'_duel_strategy_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, target)\nif target == 33748:\n    return sample_battle_action_random_fields(BattlePolicyMemory(state), frame, continuation)\ndef algorithm(memory, entered):\n    if target == 167824:\n        return scan_duel_thresholds_fields(memory.state, entered)\n    if target == 173556:\n        return choose_duel_ai_override_fields(memory.state, entered)\n    if target == 174592:\n        return sample_duel_probability_fields(memory.state, entered)\n    if target == 174688:\n        return choose_duel_ai_timeout_fields(memory.state, entered)\n    if target in (172820, 172824, 172828, 172832, 172836, 172840):\n        from ..high_level_dynamic_flows.business_duel import choose_duel_profile_fields\n        return choose_duel_profile_fields(memory.state, entered, target)\n    raise MovementContinuationBoundary(target, entered, 'actual indexed duel strategy target is not yet restored')\nreturn _presentation_call_fields(BattlePresentationMemory(state), frame, continuation, algorithm)"}, 'choose_duel_ai_command_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "cooldown_step = 1\ncooldown_mask = 31\ncooldown_bias = 30\nopponent_zero_command = 256\nprofile_shift = 1\nexecutor_shift = 2\nframe = _resource_cost_frame(state, frame, 172698)\ncooldown = frame.roster.word(34)\nframe = _movement_test(state, frame, cooldown, 16)\nif not frame.status & 4:\n    frame, cooldown = _movement_binary_flags(state, frame, frame.roster.word(34), cooldown_step, 16, True)\n    frame.roster.set_word(34, cooldown)\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(28), 16)\nif frame.status & 4:\n    frame.roster.set_word(2, low16(frame.target_x))\n    frame = _movement_test(state, frame, low16(frame.target_x), 16)\n    frame.roster.set_word(4, low16(frame.target_x))\n    return _movement_test(state, frame, low16(frame.target_x), 16)\nframe = _movement_move(state, frame, 'target_x', frame.candidates.word(28), 16)\nif frame.status & 4:\n    return _movement_move(state, frame, 'target_x', opponent_zero_command, 16)\nframe = _movement_test(state, frame, frame.roster.word(34), 16)\nif frame.status & 4:\n    frame = _duel_strategy_call_fields(state, frame, 33748, 172748)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & cooldown_mask, 16)\n    frame = _movement_add_word(state, frame, 'target_x', cooldown_bias)\n    frame.roster.set_word(34, low16(frame.target_x))\n    frame = _movement_test(state, frame, low16(frame.target_x), 16)\n    frame = _movement_move(state, frame, 'target_x', frame.roster.word(30), 16)\n    frame = first_replace(frame, controller=state.table_at(172808).cursor())\n    frame = _duel_strategy_call_fields(state, frame, 167824, 172774)\n    frame = _movement_move(state, frame, 'offset_y', low16(frame.target_y), 16)\n    frame = _duel_strategy_call_fields(state, frame, 173556, 172780)\n    frame = _duel_strategy_call_fields(state, frame, 174688, 172784)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.choice), 16)\n    frame = _movement_test(state, frame, low16(frame.target_x), 16)\n    if not frame.status & 4:\n        return frame\n    frame = _movement_move(state, frame, 'target_y', low16(frame.offset_y), 16)\n    frame = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_y', low16(frame.target_y), profile_shift)\n    target = u32(172820 + s16(low16(frame.target_y)))\n    frame = _duel_strategy_call_fields(state, frame, target, 172798)\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(36), 16)\nframe = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_x', low16(frame.target_x), executor_shift)\ntarget = u32(172844 + s16(low16(frame.target_x)))\nfrom ..high_level_dynamic_flows.business_duel import execute_duel_rule_fields\nreturn execute_duel_rule_fields(state, frame, target)"}})
APPROVED.setdefault('business_duel',set()).update({'choose_duel_profile_fields','execute_duel_rule_fields'})


# Root51 sole full-field sprite emission and old caller projection.
DECLARATIONS.update({'append_duel_sprite': {'signature': 'state: SceneState, x: Word, y: Word, pattern: Word, attributes: Word, frame: DuelActorFrame | None=None, stack: Cursor | None=None', 'returns': 'DuelSpriteResult', 'flow': "x, y, pattern, attributes = (uint(value, 16) for value in (x, y, pattern, attributes))\nentered = _duel_strategy_partial_fields(state, None, None, frame)\nfor name, value in (('target_x', x), ('target_y', y), ('unit', pattern), ('count', attributes)):\n    actual = entered.carrier(name)\n    if actual is not None and low16(actual) != value:\n        raise ValueError('sprite arguments must agree with observed current fields')\n    entered = first_replace(entered, **{name: value if actual is None else replace_word(actual, value)})\nif stack is not None:\n    entered = first_replace(entered, stack_cursor=_live_cursor(state, stack))\nreturned = append_duel_sprite_fields(state, entered)\nreturn DuelSpriteResult(returned.roster, state.read(16740352, 2), low16(returned.offset_x), _duel_strategy_actor_values(returned), returned.stack_cursor, returned.candidates)"}, '_duel_sprite_append_word_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, value: Word', 'returns': 'FirstDeploymentFrame', 'flow': 'frame.roster.set_word(0, value)\nframe = first_replace(frame, roster=frame.roster.advance(2))\nreturn _movement_test(state, frame, value, 16)'}, 'append_duel_sprite_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "sprite_index_step = 1\nsprite_vertical_origin = 128\nsprite_size_shift = 8\nsprite_extent_shift = 7\nsprite_extent_mask = 24\nsprite_extent_bias = 8\nsprite_horizontal_origin = 128\nframe = _resource_cost_frame(state, frame, 167836)\nframe = _movement_save_longs(state, frame, ('target_x', 'target_y', 'unit', 'count'))\nframe = first_replace(frame, roster=state.table_at(state.read(16740354, 4)).cursor(), candidates=state.table_at(167992).cursor())\nframe = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'unit', low16(frame.unit), 2)\ntemplate = frame.candidates.long(low16(frame.unit))\nframe = first_replace(frame, candidates=state.table_at(template).cursor())\nframe = _movement_move(state, frame, 'unit', state.read(16740352, 2), 16)\nframe = _movement_compare_address(state, frame, frame.roster.base, 4294965248)\nif not frame.status & 4:\n    frame.roster.set_byte(0, low8(frame.unit), -5)\n    frame = _movement_test(state, frame, low8(frame.unit), 8)\nframe = _movement_add_word(state, frame, 'unit', sprite_index_step)\nframe = _movement_move(state, frame, 'distance', low16(frame.count), 16)\nframe = _movement_move(state, frame, 'count', low16(frame.count) & 59391, 16)\nframe = _movement_move(state, frame, 'distance', low16(frame.distance) & 6144, 16)\nwhile True:\n    frame = _movement_move(state, frame, 'choice', frame.candidates.byte(2), 8)\n    frame = _movement_move(state, frame, 'choice', u16(s8(low8(frame.choice))), 16)\n    frame = _movement_add_word(state, frame, 'choice', low16(frame.target_x))\n    frame = _movement_add_word(state, frame, 'choice', sprite_vertical_origin)\n    frame = _duel_sprite_append_word_fields(state, frame, low16(frame.choice))\n    frame = _movement_move(state, frame, 'choice', frame.candidates.byte(1), 8)\n    frame = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'choice', low16(frame.choice), sprite_size_shift)\n    frame = _movement_move(state, frame, 'choice', low16(frame.choice) | low16(frame.unit), 16)\n    frame = _movement_add_word(state, frame, 'unit', sprite_index_step)\n    frame = _duel_sprite_append_word_fields(state, frame, low16(frame.choice))\n    frame = _duel_velocity_asr_fields(state, frame, 'choice', sprite_extent_shift)\n    frame = _movement_move(state, frame, 'choice', low16(frame.choice) & sprite_extent_mask, 16)\n    frame = _movement_add_word(state, frame, 'choice', sprite_extent_bias)\n    frame = _movement_move(state, frame, 'offset_x', low16(frame.choice), 16)\n    frame = _movement_move(state, frame, 'choice', frame.candidates.word(4), 16)\n    frame = _movement_add_word(state, frame, 'choice', low16(frame.count))\n    frame = _movement_move(state, frame, 'choice', low16(frame.choice) ^ low16(frame.distance), 16)\n    frame = _duel_sprite_append_word_fields(state, frame, low16(frame.choice))\n    frame = _movement_move(state, frame, 'choice', frame.candidates.byte(3), 8)\n    frame = _movement_move(state, frame, 'choice', u16(s8(low8(frame.choice))), 16)\n    frame = _postbattle_bit_fields(frame, bool(frame.distance & 1 << 11))\n    state.sr = state.sr & 65504 | frame.status\n    if not frame.status & 4:\n        frame = _duel_commit_sub_word_fields(state, frame, 'choice', 0, True)\n        frame = _duel_commit_sub_word_fields(state, frame, 'choice', low16(frame.offset_x))\n    frame = _movement_add_word(state, frame, 'choice', low16(frame.target_y))\n    frame = _movement_add_word(state, frame, 'choice', sprite_horizontal_origin)\n    frame = _duel_sprite_append_word_fields(state, frame, low16(frame.choice))\n    frame = first_replace(frame, candidates=frame.candidates.advance(6))\n    frame = _postbattle_bit_fields(frame, bool(frame.candidates.byte(0, -6) & 128))\n    state.sr = state.sr & 65504 | frame.status\n    if not frame.status & 4:\n        break\nframe.roster.set_byte(0, 0, -5)\nframe = _movement_test(state, frame, 0, 8)\nstate.write(16740354, 4, frame.roster.base)\nframe = _movement_test_long(state, frame, frame.roster.base)\nframe = _duel_commit_sub_word_fields(state, frame, 'unit', sprite_index_step)\nstate.write(16740352, 2, low16(frame.unit))\nframe = _movement_test(state, frame, low16(frame.unit), 16)\nreturn _movement_restore_longs(state, frame, ('target_x', 'target_y', 'unit', 'count'))"}})
APPROVED.setdefault('business_movement_support',set()).update({'_movement_save_longs', '_movement_compare_address', '_movement_restore_longs'})
APPROVED.setdefault('business_city',set()).update({'_duel_velocity_asr_fields'})
APPROVED.setdefault('domain',set()).update({'s8'})


# Root52 complete actor phases and sole historical projections.
DECLARATIONS.update({'update_duel_actor': {'signature': 'state: SceneState, actor: Table, opponent: Table, context: DuelActorContext=DuelActorContext()', 'returns': 'DuelActorResult', 'flow': 'current = _actor_input_frame(context)\nentered = _duel_strategy_partial_fields(state, actor, opponent, current)\nif context.stack is not None:\n    entered = first_replace(entered, stack_cursor=_live_cursor(state, context.stack))\nreturned = update_duel_actor_fields(state, entered)\nvalues = _duel_strategy_actor_values(returned)\nreturn DuelActorResult(values.command, values.comparison, values.distance, values, returned.roster, returned.candidates, returned.stack_cursor, values.response).validate()'}, '_apply_duel_strike': {'signature': 'state, actor, opponent, frame, stack', 'returns': None, 'flow': 'entered = _duel_strategy_partial_fields(state, actor, opponent, frame)\nif stack is not None:\n    entered = first_replace(entered, stack_cursor=_live_cursor(state, stack))\nentered = _resource_cost_frame(state, entered, 167064)\nreturn _duel_strategy_actor_values(_duel_actor_strike_fields(state, entered))'}, 'render_duel_actor': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: DuelActorFrame | None=None, stack: Cursor | None=None', 'returns': 'DuelRenderResult', 'flow': 'entered = _duel_strategy_partial_fields(state, actor, opponent, frame)\nif stack is not None:\n    entered = first_replace(entered, stack_cursor=_live_cursor(state, stack))\nreturned = render_duel_actor_fields(state, entered)\nreturn DuelRenderResult(_duel_strategy_actor_values(returned), returned.roster, returned.candidates, returned.stack_cursor).validate(state)'}, '_render_duel_movement_overlay': {'signature': 'state, actor, opponent, frame, stack', 'returns': None, 'flow': 'entered = _duel_strategy_partial_fields(state, actor, opponent, frame)\nif stack is not None:\n    entered = first_replace(entered, stack_cursor=_live_cursor(state, stack))\nentered = _resource_cost_frame(state, entered, 167634)\nreturned = _duel_actor_overlay_fields(state, entered)\nreturn DuelRenderResult(_duel_strategy_actor_values(returned), returned.roster, returned.candidates, returned.stack_cursor).validate(state)'}, '_copy_duel_palette': {'signature': 'state, source_base, destination_base', 'returns': None, 'flow': 'entered = first_replace(FirstDeploymentFrame.unobserved(), controller=state.table_at(uint(source_base, 32)), scan=state.table_at(uint(destination_base, 32)).cursor())\nentered = _resource_cost_frame(state, entered, 166880)\nreturn _duel_actor_palette_fields(state, entered, False).controller'}, '_duel_actor_attack_fields': {'signature': 'state, frame', 'returns': None, 'flow': "actor_left_command_bit = 256\nactor_right_command_bit = 512\nactor_attack_command_bit = 16\nactor_special_command_bit = 8192\nactor_attack_phase = 4\nactor_clash_kind_mask = 3\nactor_clash_sound = 160\nactor_attack_delay = 4\nactor_attack_cycle_step = 1\nactor_attack_cycle_bound = 5\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(), 16)\nframe = _movement_test(state, frame, frame.roster.word(2), 16)\nif not frame.status & 8:\n    frame = _movement_move(state, frame, 'target_y', 0, 16)\n    frame = _scene_render_bit(SceneRefreshMemory(state), frame, frame.target_x, actor_left_command_bit)\n    if frame.status & 4:\n        frame = _movement_add_word(state, frame, 'target_y', 1)\n        frame = _scene_render_bit(SceneRefreshMemory(state), frame, frame.target_x, actor_right_command_bit)\n        if not frame.status & 4:\n            frame = _movement_add_word(state, frame, 'target_y', 1)\n    frame = _duel_actor_store_fields(state, frame, frame.roster, 3, low8(frame.target_y), 8)\n    frame = _scene_render_bit(SceneRefreshMemory(state), frame, frame.target_x, actor_attack_command_bit)\n    if frame.status & 4:\n        frame = _duel_actor_store_fields(state, frame, frame.roster, 2, frame.roster.word(2) & 16383)\n        frame = _scene_render_bit(SceneRefreshMemory(state), frame, frame.target_x, actor_special_command_bit)\n        if not frame.status & 4:\n            frame = _duel_actor_flag_fields(state, frame, frame.roster, 64, True)\n        return frame\n    frame = _duel_actor_flag_fields(state, frame, frame.roster, 128, True)\n    frame = _duel_actor_flag_fields(state, frame, frame.roster, 64, False)\n    frame = _duel_actor_clear_word_fields(state, frame, frame.roster, 4)\n    frame = _duel_actor_store_fields(state, frame, frame.roster, 8, frame.roster.word(22))\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(4), 16)\nframe = _movement_test(state, frame, frame.roster.word(8), 16)\nif not frame.status & 4:\n    return frame\nphase = low16(frame.target_x)\nframe = _movement_compare(state, frame, phase, actor_attack_phase, 16)\nif phase == actor_attack_phase:\n    frame = _duel_actor_call_fields(state, frame, 172590, 167008)\n    if frame.status & 1:\n        frame = _scene_render_bit(SceneRefreshMemory(state), frame, frame.candidates.byte(2), 64)\n        clash = False\n        if not frame.status & 4:\n            frame = _movement_move(state, frame, 'target_y', frame.roster.word(2), 16)\n            frame = _movement_move(state, frame, 'unit', frame.candidates.word(2), 16)\n            frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & actor_clash_kind_mask, 16)\n            frame = _movement_move(state, frame, 'unit', low16(frame.unit) & actor_clash_kind_mask, 16)\n            own_kind, opponent_kind = (low16(frame.target_y), low16(frame.unit))\n            frame = _movement_compare(state, frame, opponent_kind, own_kind, 16)\n            if opponent_kind == own_kind:\n                clash = True\n        if clash:\n            frame = _duel_actor_save_words_fields(state, frame)\n            frame = _movement_move(state, frame, 'target_x', actor_clash_sound, 16)\n            frame = _duel_actor_call_fields(state, frame, 32906, 167054)\n            frame = _duel_actor_restore_words_fields(state, frame)\n        else:\n            frame = _duel_actor_strike_fields(state, frame)\nframe = _duel_actor_store_fields(state, frame, frame.roster, 8, actor_attack_delay)\nframe = _movement_add_word(state, frame, 'target_x', actor_attack_cycle_step)\nphase = low16(frame.target_x)\nframe = _movement_compare(state, frame, phase, actor_attack_cycle_bound, 16)\nif phase >= actor_attack_cycle_bound:\n    frame = _movement_move(state, frame, 'target_x', 0, 16)\n    frame = _duel_actor_flag_fields(state, frame, frame.roster, 128, False)\nreturn _duel_actor_store_fields(state, frame, frame.roster, 4, low16(frame.target_x))"}, '_duel_actor_call_fields': {'signature': 'state, frame, target, continuation', 'returns': None, 'flow': "pairs = ((172590, 167008), (32906, 167054), (32906, 167076), (33748, 167088), (167824, 167114), (167836, 167630), (167836, 167756), (167836, 167812))\nif (target, continuation) not in pairs:\n    raise ValueError('actual actor call pair required')\nframe = _resource_cost_frame(state, frame, target)\nif target in (33748, 167824):\n    return _duel_strategy_call_fields(state, frame, target, continuation)\ndef child(memory, entered):\n    if target == 172590:\n        return measure_duel_weapon_contact_fields(memory.state, entered)\n    if target == 167836:\n        return append_duel_sprite_fields(memory.state, entered)\n    return enqueue_sound_command_fields(SceneRefreshMemory(memory.state), entered)\nreturn _presentation_call_fields(BattlePresentationMemory(state), frame, continuation, child)"}, '_duel_actor_clear_word_fields': {'signature': 'state, frame, view, offset', 'returns': None, 'flow': 'view.word(offset)\nreturn _duel_actor_store_fields(state, frame, view, offset, 0)'}, '_duel_actor_flag_fields': {'signature': 'state, frame, view, mask, set_bit', 'returns': None, 'flow': 'old = view.byte(2)\nframe = _scene_render_bit(SceneRefreshMemory(state), frame, old, mask)\nview.set_byte(2, old | mask if set_bit else old & (255 ^ mask))\nreturn frame'}, '_duel_actor_motion_fields': {'signature': 'state, frame', 'returns': None, 'flow': "actor_motion_request_mask = 12\nactor_motion_first_direction = 4\nactor_motion_second_direction = 8\nactor_motion_tick_mask = 15\nactor_motion_delay = 48\nactor_motion_boost = 32768\nactor_motion_reverse_mask = 2048\nactor_motion_minimum = 16\nactor_motion_maximum = 224\nframe = _scene_render_bit(SceneRefreshMemory(state), frame, frame.roster.byte(2), 16)\nif not frame.status & 4:\n    frame = _movement_test(state, frame, frame.roster.word(10), 16)\n    if frame.status & 4:\n        frame = _duel_actor_flag_fields(state, frame, frame.roster, 16, False)\n    return frame\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(), 16)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & actor_motion_request_mask, 16)\nif not frame.status & 4:\n    frame = _movement_move(state, frame, 'count', actor_motion_second_direction, 16)\n    frame = _scene_render_bit(SceneRefreshMemory(state), frame, frame.roster.byte(24), 8)\n    if not frame.status & 4:\n        frame = _movement_move(state, frame, 'count', actor_motion_first_direction, 16)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & low16(frame.count), 16)\n    if not frame.status & 4:\n        frame = _movement_move(state, frame, 'target_x', state.read(16740360, 2), 16)\n        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & actor_motion_tick_mask, 16)\n        if frame.status & 4:\n            frame = _duel_actor_flag_fields(state, frame, frame.roster, 16, True)\n            return _duel_actor_store_fields(state, frame, frame.roster, 10, actor_motion_delay)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_y) & _duel_actor_motion_mode_fields(), 16)\nif frame.status & 4:\n    return frame\nframe = _duel_actor_flag_fields(state, frame, frame.roster, 32, True)\nframe = _movement_move_long(state, frame, 'unit', frame.roster.long(18))\nframe = _movement_move(state, frame, 'count', frame.roster.word(40), 16)\nframe = _movement_move(state, frame, 'count', low16(frame.count) | frame.roster.word(38), 16)\nif not frame.status & 4:\n    frame, value = _movement_binary_flags(state, frame, frame.unit, actor_motion_boost, 32)\n    frame = first_replace(frame, unit=value)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_y) & actor_motion_reverse_mask, 16)\nif frame.status & 4:\n    frame, value = _movement_binary_flags(state, frame, 0, frame.unit, 32, True)\n    frame = first_replace(frame, unit=value)\nframe, value = _movement_binary_flags(state, frame, frame.unit, frame.roster.long(14), 32)\nframe = first_replace(frame, unit=value)\nframe = _movement_move_long(state, frame, 'target_y', frame.unit)\nframe, value = _movement_binary_flags(state, frame, frame.target_y, frame.candidates.long(14), 32, True)\nframe = first_replace(frame, target_y=value)\nif frame.status & 8:\n    frame, value = _movement_binary_flags(state, frame, 0, frame.target_y, 32, True)\n    frame = first_replace(frame, target_y=value)\nframe = _movement_move_long(state, frame, 'target_y', swap_words(frame.target_y))\nseparation = low16(frame.target_y)\nframe = _movement_compare(state, frame, separation, actor_motion_maximum, 16)\nif separation < actor_motion_maximum:\n    frame = _movement_compare(state, frame, separation, actor_motion_minimum, 16)\n    if actor_motion_minimum <= separation:\n        frame = _duel_actor_store_fields(state, frame, frame.roster, 14, frame.unit, 32)\nreturn frame"}, '_duel_actor_motion_mode_fields': {'signature': '', 'returns': None, 'flow': 'actor_motion_mode_mask = 3072\nreturn actor_motion_mode_mask'}, '_duel_actor_overlay_fields': {'signature': 'state, frame', 'returns': None, 'flow': "overlay_frame_delay = 10\noverlay_animation_step = 1\noverlay_animation_bound = 5\noverlay_animation_restart = 1\noverlay_plain_pattern = 62\noverlay_armed_pattern = 54\noverlay_blink_shift = 4\noverlay_blink_mask = 1\noverlay_blink_pattern = 60\nframe = _scene_render_bit(SceneRefreshMemory(state), frame, frame.roster.byte(2), 32)\nif not frame.status & 4:\n    frame = _movement_test(state, frame, frame.roster.word(10), 16)\n    if frame.status & 4:\n        frame = _duel_actor_store_fields(state, frame, frame.roster, 10, overlay_frame_delay)\n        frame = _movement_move(state, frame, 'target_x', frame.roster.word(6), 16)\n        frame = _movement_add_word(state, frame, 'target_x', overlay_animation_step)\n        animation = low16(frame.target_x)\n        frame = _movement_compare(state, frame, animation, overlay_animation_bound, 16)\n        if animation >= overlay_animation_bound:\n            frame = _movement_move(state, frame, 'target_x', overlay_animation_restart, 16)\n            frame = _movement_move(state, frame, 'target_y', frame.roster.word(), 16)\n            frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & _duel_actor_motion_mode_fields(), 16)\n            if frame.status & 4:\n                frame = _duel_actor_flag_fields(state, frame, frame.roster, 32, False)\n                frame = _movement_move(state, frame, 'target_x', 0, 16)\n        frame = _duel_actor_store_fields(state, frame, frame.roster, 6, low16(frame.target_x))\nbaseline, injured = _duel_actor_render_positions_fields()\nframe = _movement_move(state, frame, 'target_x', baseline, 16)\nframe = _movement_move(state, frame, 'target_y', frame.roster.word(14), 16)\nframe = _duel_commit_sub_word_fields(state, frame, 'target_y', state.read(16740358, 2))\nframe = _movement_move(state, frame, 'unit', overlay_armed_pattern, 16)\nframe = _movement_test(state, frame, frame.roster.word(12), 16)\nif frame.status & 4:\n    frame = _movement_move(state, frame, 'unit', overlay_plain_pattern, 16)\nframe = _movement_add_word(state, frame, 'unit', frame.roster.word(6))\nframe = _scene_render_bit(SceneRefreshMemory(state), frame, frame.roster.byte(2), 16)\nif not frame.status & 4:\n    frame = _movement_move(state, frame, 'unit', state.read(16740360, 2), 16)\n    frame = _movement_fixed_shift_word(state, frame, 'unit', overlay_blink_shift, True)\n    frame = _movement_move(state, frame, 'unit', low16(frame.unit) & overlay_blink_mask, 16)\n    frame = _movement_add_word(state, frame, 'unit', overlay_blink_pattern)\nframe = _movement_move(state, frame, 'count', frame.roster.word(24), 16)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, frame.roster.base)\nframe = first_replace(frame, stack_cursor=stack)\nframe = _movement_test_long(state, frame, frame.roster.base)\nframe = _duel_actor_call_fields(state, frame, 167836, 167756)\nactor = frame.stack_cursor.long()\nreturn first_replace(frame, roster=state.table_at(actor).cursor(), stack_cursor=frame.stack_cursor.advance(4))"}, '_duel_actor_palette_fields': {'signature': 'state, frame, glow', 'returns': None, 'flow': "actor_flash_mask = 1\nactor_palette_words = 8\nactor_glow_first = 1024\nactor_glow_second = 2048\nactor_palette_keep_mask = 62451\nif glow:\n    frame = _movement_move(state, frame, 'target_y', actor_glow_first, 16)\nframe = first_replace(frame, controller=state.table_at(163968), scan=state.table_at(4294966016).cursor())\nframe = _movement_compare_address(state, frame, frame.roster.base, 16740432)\nif frame.roster.base != 16740432:\n    if glow:\n        frame = _movement_move(state, frame, 'target_y', actor_glow_second, 16)\n    frame = first_replace(frame, controller=state.table_at(164000), scan=state.table_at(4294966048).cursor())\ncounter = 'count' if glow else 'choice'\ncarrier = 'target_x' if glow else 'target_y'\nif not glow:\n    frame = _movement_move(state, frame, counter, actor_palette_words - 1, 16)\nframe = _movement_move(state, frame, carrier, low16(frame.carrier(carrier)) & actor_flash_mask, 16)\nif frame.status & 4:\n    frame = first_replace(frame, controller=state.table_at(164096 if glow else 164112))\nif glow:\n    frame = _duel_actor_store_fields(state, frame, frame.roster, 0, frame.roster.word() & actor_palette_keep_mask)\n    frame = _duel_actor_store_fields(state, frame, frame.roster, 0, frame.roster.word() | low16(frame.target_y))\n    frame = _movement_move(state, frame, counter, actor_palette_words - 1, 16)\nwhile True:\n    value = frame.controller.word()\n    source = frame.controller.advance(2)\n    frame.scan.set_word(0, value)\n    frame = first_replace(frame, controller=source, scan=frame.scan.advance(2))\n    frame = _movement_test(state, frame, value, 16)\n    remaining = u16(low16(frame.carrier(counter)) - 1)\n    frame = first_replace(frame, **{counter: replace_word(frame.carrier(counter), remaining)})\n    if remaining == 65535:\n        return frame"}, '_duel_actor_render_positions_fields': {'signature': '', 'returns': None, 'flow': 'render_baseline_x = 88\nrender_injured_x = 84\nreturn (render_baseline_x, render_injured_x)'}, '_duel_actor_restore_words_fields': {'signature': 'state, frame', 'returns': None, 'flow': "stack = frame.stack_cursor\nfor name in ('target_x', 'target_y'):\n    value = stack.word()\n    stack = stack.advance(2)\n    frame = first_replace(frame, **{name: u32(s16(value))})\nreturn first_replace(frame, stack_cursor=stack)"}, '_duel_actor_save_words_fields': {'signature': 'state, frame', 'returns': None, 'flow': 'stack = frame.stack_cursor\nfor value in (frame.target_y, frame.target_x):\n    stack = stack.advance(-2)\n    stack.set_word(0, low16(value))\nreturn first_replace(frame, stack_cursor=stack)'}, '_duel_actor_store_fields': {'signature': 'state, frame, view, offset, value, width=16', 'returns': None, 'flow': "value = uint(value, width)\nif width == 8:\n    view.set_byte(offset, value)\nelif width == 16:\n    view.set_word(offset, value)\nelif width == 32:\n    view.set_long(offset, value)\n    return _movement_test_long(state, frame, value)\nelse:\n    raise ValueError('actual actor MOVE width required')\nreturn _movement_test(state, frame, value, width)"}, '_duel_actor_strike_fields': {'signature': 'state, frame', 'returns': None, 'flow': "strike_sound = 167\nstrike_recovery_delay = 60\nstrike_random_mask = 7\nstrike_random_bound = 6\nstrike_random_fold = 4\nstrike_second_weapon_bound = 1\nframe = _duel_actor_save_words_fields(state, frame)\nframe = _movement_move(state, frame, 'target_x', strike_sound, 16)\nframe = _duel_actor_call_fields(state, frame, 32906, 167076)\nframe = _duel_actor_store_fields(state, frame, frame.candidates, 38, strike_recovery_delay)\nframe = _duel_actor_call_fields(state, frame, 33748, 167088)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & strike_random_mask, 16)\nrolled = low16(frame.target_x)\nframe = _movement_compare(state, frame, rolled, strike_random_bound, 16)\nif rolled >= strike_random_bound:\n    frame = _duel_commit_sub_word_fields(state, frame, 'target_x', strike_random_fold)\nframe = _movement_move(state, frame, 'choice', low16(frame.target_x), 16)\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(30), 16)\nframe = first_replace(frame, controller=state.table_at(167218))\nframe = _duel_actor_call_fields(state, frame, 167824, 167114)\nframe = _movement_add_word(state, frame, 'choice', state.read(u32(167230 + s16(low16(frame.target_y))), 2))\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(30), 16)\nframe = _movement_move(state, frame, 'target_y', frame.roster.word(12), 16)\nweapon = low16(frame.target_y)\nframe = _movement_test(state, frame, weapon, 16)\nif weapon == 0:\n    equipment_offset, table = (44, 167242)\nelse:\n    frame = _movement_compare(state, frame, weapon, strike_second_weapon_bound, 16)\n    if weapon <= strike_second_weapon_bound:\n        equipment_offset, table = (42, 167250)\n    else:\n        equipment_offset, table = (46, 167258)\nframe = _movement_move(state, frame, 'unit', frame.roster.word(equipment_offset), 16)\nframe = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'unit', low16(frame.unit), 1)\nframe = _movement_add_word(state, frame, 'target_x', state.read(u32(table + s16(low16(frame.unit))), 2))\nframe = _movement_multiply_word(state, frame, 'choice', low16(frame.target_x))\nframe = _movement_move(state, frame, 'unit', frame.roster.word(2), 16)\nframe = _movement_move(state, frame, 'unit', low16(frame.unit) & 3, 16)\nframe = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'unit', low16(frame.unit), 1)\ndivisor = state.read(u32(167278 + s16(low16(frame.unit))), 2)\nframe = _movement_divu_word(state, frame, 'choice', divisor, 167190)\nframe = _duel_actor_restore_words_fields(state, frame)\nhealth = frame.roster.word(28)\nframe = _movement_test(state, frame, health, 16)\nif health != 0:\n    frame, remaining = _movement_binary_flags(state, frame, frame.candidates.word(28), low16(frame.choice), 16, True)\n    frame.candidates.set_word(28, remaining)\n    if frame.status & 8:\n        frame = _duel_actor_clear_word_fields(state, frame, frame.candidates, 28)\nreturn frame"}, 'render_duel_actor_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "render_skip_bit = 8\nrender_mode_stride = 18\nrender_direction_stride = 6\nrender_special_pattern = 5\nframe = _resource_cost_frame(state, frame, 167532)\nframe = _scene_render_bit(SceneRefreshMemory(state), frame, frame.roster.byte(2), render_skip_bit)\nif not frame.status & 4:\n    return frame\nhealth = frame.roster.word(28)\nframe = _movement_test(state, frame, health, 16)\nbaseline, injured = _duel_actor_render_positions_fields()\nif health == 0:\n    saved = ('target_x', 'target_y', 'unit', 'count', 'roster', 'candidates')\n    frame = _movement_save_longs(state, frame, saved)\n    frame = _movement_move(state, frame, 'target_x', frame.roster.word(12), 16)\n    frame = _movement_move(state, frame, 'unit', state.read(u32(167820 + s16(low16(frame.target_x))), 1), 8)\n    frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 255, 16)\n    frame = _movement_move(state, frame, 'count', frame.roster.word(24), 16)\n    frame = _movement_move(state, frame, 'target_y', frame.roster.word(14), 16)\n    frame = _duel_commit_sub_word_fields(state, frame, 'target_y', state.read(16740358, 2))\n    frame = _movement_move(state, frame, 'target_x', baseline, 16)\n    frame = _scene_render_bit(SceneRefreshMemory(state), frame, frame.roster.byte(2), 16)\n    if not frame.status & 4:\n        frame = _movement_move(state, frame, 'target_x', injured, 16)\n    frame = _duel_actor_call_fields(state, frame, 167836, 167812)\n    frame = _movement_restore_longs(state, frame, saved)\nelse:\n    frame = _movement_move(state, frame, 'choice', frame.roster.word(12), 16)\n    frame = _movement_multiply_word(state, frame, 'choice', render_mode_stride)\n    frame = _movement_move(state, frame, 'unit', 0, 16)\n    frame = _movement_move(state, frame, 'unit', frame.roster.byte(3), 8)\n    frame = _movement_multiply_word(state, frame, 'unit', render_direction_stride)\n    frame = _movement_add_word(state, frame, 'unit', low16(frame.choice))\n    frame = _movement_move(state, frame, 'choice', frame.roster.word(4), 16)\n    frame = _scene_render_bit(SceneRefreshMemory(state), frame, frame.roster.byte(2), 64)\n    if not frame.status & 4:\n        frame = _movement_move(state, frame, 'choice', render_special_pattern, 16)\n    frame = _movement_add_word(state, frame, 'unit', low16(frame.choice))\n    frame = _movement_move(state, frame, 'target_x', baseline, 16)\n    frame = _scene_render_bit(SceneRefreshMemory(state), frame, frame.roster.byte(2), 16)\n    if not frame.status & 4:\n        frame = _movement_move(state, frame, 'target_x', injured, 16)\n    frame = _movement_move(state, frame, 'target_y', frame.roster.word(14), 16)\n    frame = _duel_commit_sub_word_fields(state, frame, 'target_y', state.read(16740358, 2))\n    frame = _movement_move(state, frame, 'count', frame.roster.word(24), 16)\n    frame = _movement_save_longs(state, frame, ('roster', 'candidates'))\n    frame = _duel_actor_call_fields(state, frame, 167836, 167630)\n    frame = _movement_restore_longs(state, frame, ('roster', 'candidates'))\nreturn _duel_actor_overlay_fields(state, frame)"}, 'update_duel_actor_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "actor_timer_step = 1\nframe = _resource_cost_frame(state, frame, 166810)\nfor offset in (8, 10, 38, 40):\n    frame = _movement_test(state, frame, frame.roster.word(offset), 16)\n    if not frame.status & 4:\n        frame, value = _movement_binary_flags(state, frame, frame.roster.word(offset), actor_timer_step, 16, True)\n        frame.roster.set_word(offset, value)\nframe = _movement_move(state, frame, 'target_y', frame.roster.word(40), 16)\nif not frame.status & 4:\n    frame = _duel_actor_palette_fields(state, frame, False)\nframe = _duel_actor_attack_fields(state, frame)\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(38), 16)\nif not frame.status & 4:\n    frame = _duel_actor_palette_fields(state, frame, True)\nframe = _duel_actor_motion_fields(state, frame)\nreturn render_duel_actor_fields(state, frame)"}})
APPROVED.setdefault('business_scene',set()).update({'_scene_render_bit'})
APPROVED.setdefault('business_movement_support',set()).update({'_movement_save_longs', '_movement_divu_word', '_movement_multiply_word', '_movement_restore_longs'})
APPROVED.setdefault('business_services',set()).update({'enqueue_sound_command_fields'})


# Root53 true two-actor refresh parent and its sole projection.
DECLARATIONS.update({'refresh_duel_actors': {'signature': 'state: SceneState, frame: DuelActorFrame | None=None, stack: Cursor | None=None, caller_actor: Table | None=None, caller_opponent: Table | None=None', 'returns': 'DuelRenderResult', 'flow': 'entered = _duel_strategy_partial_fields(state, caller_actor, caller_opponent, frame)\nif stack is not None:\n    entered = first_replace(entered, stack_cursor=_live_cursor(state, stack))\nreturned = refresh_duel_actors_fields(state, entered)\nreturn DuelRenderResult(_duel_strategy_actor_values(returned), returned.roster, returned.candidates, returned.stack_cursor).validate(state)'}, '_duel_actor_refresh_call_fields': {'signature': 'state, frame, continuation', 'returns': None, 'flow': "if continuation not in (162464, 162488):\n    raise ValueError('actual double-actor refresh return required')\ndef child(memory, entered):\n    return render_duel_actor_fields(memory.state, entered)\nreturn _presentation_call_fields(BattlePresentationMemory(state), frame, continuation, child)"}, 'refresh_duel_actors_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 162436)\nsaved = ('roster', 'candidates')\nframe = _movement_save_longs(state, frame, saved)\nfor actor, opponent, continuation in ((16740432, 16740512, 162464), (16740512, 16740432, 162488)):\n    frame = _duel_actor_store_fields(state, frame, state.table_at(actor), 0, 0)\n    frame = first_replace(frame, roster=state.table_at(actor).cursor(), candidates=state.table_at(opponent).cursor())\n    frame = _duel_actor_refresh_call_fields(state, frame, continuation)\nreturn _movement_restore_longs(state, frame, saved)"}})


# Root54 sole complete motion configuration and historical view.
DECLARATIONS.update({'configure_duel_weapon_motion': {'signature': 'state: SceneState, actor: Table, frame: DuelActorFrame | None=None', 'returns': 'DuelActorFrame | None', 'flow': 'entered = _duel_strategy_partial_fields(state, actor, None, frame)\nreturned = configure_duel_weapon_motion_fields(state, entered)\nreturn None if frame is None else _duel_strategy_actor_values(returned)'}, 'configure_duel_weapon_motion_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "maximum_aptitude = 80\nvelocity_scale = 1792\nvelocity_origin = 24576\nframe = _resource_cost_frame(state, frame, 162362)\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(30), 16)\nframe = _movement_move(state, frame, 'target_y', frame.roster.word(12), 16)\nframe = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_y', low16(frame.target_y), 1)\npenalty = state.read(u32(162430 + s16(low16(frame.target_y))), 2)\nframe = _duel_commit_sub_word_fields(state, frame, 'target_x', penalty)\nif frame.status & 1:\n    frame = _movement_move(state, frame, 'target_x', 0, 16)\nelse:\n    frame = _movement_compare(state, frame, low16(frame.target_x), maximum_aptitude, 16)\n    if not frame.status & 1:\n        frame = _movement_move(state, frame, 'target_x', maximum_aptitude, 16)\nframe = _movement_move(state, frame, 'target_y', maximum_aptitude, 16)\nframe = _duel_commit_sub_word_fields(state, frame, 'target_y', low16(frame.target_x))\nframe = _movement_multiply_word(state, frame, 'target_x', velocity_scale)\nframe, value = _movement_binary_flags(state, frame, frame.target_x, velocity_origin, 32)\nframe = first_replace(frame, target_x=value)\nframe = _duel_actor_store_fields(state, frame, frame.roster, 18, frame.target_x, 32)\nframe = _movement_move_long(state, frame, 'target_y', frame.target_y & 65535)\nframe = _movement_divu_word(state, frame, 'target_y', 2, 162420)\nreturn _duel_actor_store_fields(state, frame, frame.roster, 22, low16(frame.target_y))"}})

DECLARATIONS.update({'_equipment_available': {'signature': 'equipment, option', 'returns': None, 'flow': 'return equipment.word(_duel_menu_equipment_slot(option)) != 0'}})

DECLARATIONS.update({'_finish_duel_loadout_menu': {'signature': 'state, frame', 'returns': None, 'flow': 'entered = _duel_menu_observations_to_fields(state, frame, 163316)\nreturn _duel_menu_fields_to_observations(state, _duel_menu_adjust_memory_word_fields(state, entered, True))'}})

DECLARATIONS.update({'_highlight_duel_loadout_choice': {'signature': 'state, frame, vertical_base', 'returns': None, 'flow': 'entered = _duel_menu_observations_to_fields(state, frame, 163290)\ncontinuation = 163316 if vertical_base == 121 else 163530\nreturn _duel_menu_fields_to_observations(state, _duel_menu_loadout_highlight_fields(state, entered, vertical_base, continuation))'}})

DECLARATIONS.update({'choose_duel_two_option_menu_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnFrame', 'flow': 'entered = _duel_menu_observations_to_fields(state, frame, 163228)\nreturn _duel_menu_fields_to_observations(state, choose_duel_two_option_menu_fields(state, entered))'}})

DECLARATIONS.update({'_choose_duel_equipment_complete': {'signature': 'state, equipment, frame', 'returns': None, 'flow': "equipment = _live_table(state, equipment)\nif equipment.base not in (16740474, 16740554):\n    raise ValueError('actual first/second equipment view required')\nentered = _duel_menu_observations_to_fields(state, frame, 163334 if equipment.base == 16740554 else 163324)\nreturn _duel_menu_fields_to_observations(state, choose_duel_equipment_fields(state, entered, equipment.base == 16740554))"}})

DECLARATIONS.update({'choose_first_duel_equipment_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnFrame', 'flow': 'entered = _duel_menu_observations_to_fields(state, frame, 163324)\nreturn _duel_menu_fields_to_observations(state, choose_first_duel_equipment_fields(state, entered))'}})

DECLARATIONS.update({'choose_second_duel_equipment_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnFrame', 'flow': 'entered = _duel_menu_observations_to_fields(state, frame, 163334)\nreturn _duel_menu_fields_to_observations(state, choose_second_duel_equipment_fields(state, entered))'}})

DECLARATIONS.update({'_append_duel_menu_cursor': {'signature': 'state, frame', 'returns': None, 'flow': 'entered = _duel_menu_observations_to_fields(state, frame, 167836)\nreturn _duel_menu_fields_to_observations(state, append_duel_sprite_fields(state, entered))'}})

DECLARATIONS.update({'_duel_menu_highlight': {'signature': 'state, frame, restricted', 'returns': None, 'flow': 'entered = _duel_menu_observations_to_fields(state, frame, 163648)\nreturn _duel_menu_fields_to_observations(state, _duel_action_menu_highlight_fields(state, entered, restricted))'}})

DECLARATIONS.update({'choose_duel_action_menu_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnFrame', 'flow': 'entered = _duel_menu_observations_to_fields(state, frame, 163538)\nreturn _duel_menu_fields_to_observations(state, choose_duel_action_menu_fields(state, entered))'}})

DECLARATIONS.update({'_duel_menu_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': "pairs = ((162278, 163262), (167836, 163316), (162278, 163476), (167836, 163530), (162278, 163640), (167836, 163716), (162278, 163786), (167836, 163846))\nif (target, continuation) not in pairs:\n    raise ValueError('actual menu query/cursor return pair required')\ndef algorithm(memory, entered):\n    if target == 162278:\n        from .business_reuse import choose_first_duel_control_fields\n        return choose_first_duel_control_fields(memory.state, entered)\n    return append_duel_sprite_fields(memory.state, entered)\nreturn _presentation_call_fields(BattlePresentationMemory(state), frame, continuation, algorithm)"}})

DECLARATIONS.update({'_duel_menu_button_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, bit: int', 'returns': 'FirstDeploymentFrame', 'flow': "if bit not in (1, 2, 3, 5):\n    raise ValueError('actual original menu button bit required')\nframe = _postbattle_bit_fields(frame, bool(frame.target_x & 1 << bit))\nstate.sr = state.sr & 65504 | frame.status\nreturn frame"}})

DECLARATIONS.update({'_duel_menu_adjust_memory_word_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, timer: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': "if type(timer) is not bool:\n    raise ValueError('actual choice/timer memory role required')\nview = state.table_at(16740602) if timer else frame.roster\nvalue = view.word(0)\nframe, value = _movement_binary_flags(state, frame, value, 1, 16, timer)\nview.set_word(0, value)\nreturn frame"}})

DECLARATIONS.update({'_duel_menu_equipment_slot': {'signature': 'option: Word', 'returns': 'Word', 'flow': 'uint(option, 16)\nreturn 2 if option == 0 else 0 if option == 1 else 4'}})

DECLARATIONS.update({'_duel_menu_equipment_present_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'option = low16(frame.target_y)\nframe = _movement_test(state, frame, option, 16)\nif option != 0:\n    frame = _movement_compare(state, frame, option, 1, 16)\nreturn _movement_test(state, frame, frame.scan.word(_duel_menu_equipment_slot(option)), 16)'}})

DECLARATIONS.update({'_duel_menu_loadout_highlight_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, vertical_base: Word, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': "if (vertical_base, continuation) not in ((121, 163316), (104, 163530)):\n    raise ValueError('original two-option/equipment cursor plan required')\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 12, 16)\nif frame.status & 4:\n    frame = _movement_move(state, frame, 'target_x', state.read(16740360, 2), 16)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 8, 16)\n    if frame.status & 4:\n        return frame\nframe = _movement_move(state, frame, 'target_x', 200, 16)\nframe = _movement_move(state, frame, 'target_y', frame.roster.word(0), 16)\nframe = _movement_multiply_word(state, frame, 'target_y', 56)\nframe = _movement_add_word(state, frame, 'target_y', vertical_base)\nframe = _movement_move(state, frame, 'unit', 67, 16)\nframe = _movement_move(state, frame, 'count', 32768, 16)\nreturn _duel_menu_call_fields(state, frame, 167836, continuation)"}})

DECLARATIONS.update({'choose_duel_two_option_menu_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 163228)\nframe = _movement_move(state, frame, 'target_y', frame.roster.word(0), 16)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 12, 16)\nif not frame.status & 4:\n    frame = _movement_move(state, frame, 'unit', 1, 16)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 8, 16)\n    if frame.status & 4:\n        frame = _duel_commit_sub_word_fields(state, frame, 'unit', 0, True)\n    frame = _movement_add_word(state, frame, 'target_y', low16(frame.unit))\n    frame = _movement_compare(state, frame, low16(frame.target_y), 2, 16)\n    if frame.status & 1:\n        frame = _duel_actor_store_fields(state, frame, frame.roster, 0, low16(frame.target_y))\nframe = _duel_menu_call_fields(state, frame, 162278, 163262)\nframe = _duel_menu_button_fields(state, frame, 5)\nif frame.status & 4:\n    frame = _duel_menu_loadout_highlight_fields(state, frame, 121, 163316)\nreturn _duel_menu_adjust_memory_word_fields(state, frame, True)"}})

DECLARATIONS.update({'choose_duel_equipment_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, second: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 163334 if second else 163324)\nif type(second) is not bool:\n    raise ValueError('actual first/second equipment entry required')\nframe = first_replace(frame, scan=state.table_at(16740554 if second else 16740474).cursor())\nwhile True:\n    frame = _movement_move(state, frame, 'target_y', frame.roster.word(0), 16)\n    frame = _duel_menu_equipment_present_fields(state, frame)\n    if not frame.status & 4:\n        break\n    frame = _duel_menu_adjust_memory_word_fields(state, frame)\n    selected = frame.roster.word(0)\n    frame = _movement_compare(state, frame, selected, 3, 16)\n    if not frame.status & 1:\n        frame = _duel_actor_clear_word_fields(state, frame, frame.roster, 0)\nframe = _movement_move(state, frame, 'target_y', frame.roster.word(0), 16)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 12, 16)\nif not frame.status & 4:\n    frame = _movement_move(state, frame, 'unit', 1, 16)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 8, 16)\n    if frame.status & 4:\n        frame = _duel_commit_sub_word_fields(state, frame, 'unit', 0, True)\n    while True:\n        frame = _movement_add_word(state, frame, 'target_y', low16(frame.unit))\n        if frame.status & 8:\n            frame = _movement_move_long(state, frame, 'target_y', 2)\n        else:\n            frame = _movement_compare(state, frame, low16(frame.target_y), 3, 16)\n            if not frame.status & 1:\n                frame = _movement_move_long(state, frame, 'target_y', 0)\n        frame = _duel_menu_equipment_present_fields(state, frame)\n        if not frame.status & 4:\n            break\n    frame = _movement_compare(state, frame, low16(frame.target_y), 3, 16)\n    if frame.status & 1:\n        frame = _duel_actor_store_fields(state, frame, frame.roster, 0, low16(frame.target_y))\nframe = _duel_menu_call_fields(state, frame, 162278, 163476)\nframe = _duel_menu_button_fields(state, frame, 5)\nif frame.status & 4:\n    frame = _duel_menu_loadout_highlight_fields(state, frame, 104, 163530)\nreturn _duel_menu_adjust_memory_word_fields(state, frame, True)"}})

DECLARATIONS.update({'choose_first_duel_equipment_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return choose_duel_equipment_fields(state, frame, False)'}})

DECLARATIONS.update({'choose_second_duel_equipment_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return choose_duel_equipment_fields(state, frame, True)'}})

DECLARATIONS.update({'_duel_action_direction_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _movement_move(state, frame, 'unit', 1, 16)\nframe = _duel_menu_button_fields(state, frame, 3)\nif frame.status & 4:\n    frame = _duel_commit_sub_word_fields(state, frame, 'unit', 0, True)\n    frame = _duel_menu_button_fields(state, frame, 2)\n    if frame.status & 4:\n        frame = _movement_move(state, frame, 'unit', 2, 16)\n        frame = _duel_menu_button_fields(state, frame, 1)\n        if frame.status & 4:\n            frame = _duel_commit_sub_word_fields(state, frame, 'unit', 0, True)\nreturn frame"}})

DECLARATIONS.update({'_duel_action_restricted_choice_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _movement_move_long(state, frame, 'target_y', 0)\nframe = _movement_move(state, frame, 'target_y', state.read(16740377, 1), 8)\nframe = _duel_menu_button_fields(state, frame, 3)\nif not frame.status & 4:\n    frame = _movement_add_word(state, frame, 'target_y', 1)\n    frame = _movement_compare(state, frame, low16(frame.target_y), 2, 16)\n    if frame.status & 4:\n        frame = _movement_add_word(state, frame, 'target_y', 1)\n    frame = _movement_compare(state, frame, low16(frame.target_y), 4, 16)\n    if not frame.status & 1:\n        frame = _movement_move_long(state, frame, 'target_y', 0)\nframe = _duel_menu_button_fields(state, frame, 2)\nif not frame.status & 4:\n    frame = _movement_compare(state, frame, low16(frame.target_y), 3, 16)\n    if frame.status & 4:\n        frame = _duel_commit_sub_word_fields(state, frame, 'target_y', 1)\n    frame = _duel_commit_sub_word_fields(state, frame, 'target_y', 1)\n    if frame.status & 8:\n        frame = _movement_move_long(state, frame, 'target_y', 3)\nreturn _duel_actor_store_fields(state, frame, state.table_at(16740377), 0, low8(frame.target_y), 8)"}})

DECLARATIONS.update({'_duel_action_menu_highlight_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, restricted: bool', 'returns': 'FirstDeploymentFrame', 'flow': "if type(restricted) is not bool:\n    raise ValueError('actual action menu row plan required')\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)\nif frame.status & 4:\n    frame = _movement_move(state, frame, 'target_x', state.read(16740360, 2), 16)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 8, 16)\n    if frame.status & 4:\n        return frame\nif restricted:\n    frame = _movement_move(state, frame, 'unit', state.read(16740376, 2), 16)\n    frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 3, 16)\n    frame = _movement_move(state, frame, 'target_x', 200, 16)\n    frame = _movement_move_long(state, frame, 'target_y', 0)\n    vertical = state.table_at(163854).byte(low16(frame.unit))\n    frame = _movement_move(state, frame, 'target_y', vertical, 8)\n    continuation = 163846\nelse:\n    frame = _movement_move(state, frame, 'target_x', state.read(16740376, 2), 16)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 2, 16)\n    frame = _movement_multiply_word(state, frame, 'target_x', 12)\n    frame = _movement_add_word(state, frame, 'target_x', 176)\n    frame = _movement_move(state, frame, 'target_y', state.read(16740376, 2), 16)\n    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 1, 16)\n    frame = _movement_multiply_word(state, frame, 'target_y', 48)\n    frame = _movement_add_word(state, frame, 'target_y', 136)\n    continuation = 163716\nframe = _movement_move(state, frame, 'unit', 67, 16)\nframe = _movement_move(state, frame, 'count', 32768, 16)\nreturn _duel_menu_call_fields(state, frame, 167836, continuation)"}})

DECLARATIONS.update({'choose_duel_action_menu_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 163538)\nside = state.read(16740376, 2)\nframe = _movement_test(state, frame, side, 16)\nsecond = bool(frame.status & 8)\nframe = _movement_move(state, frame, 'target_y', state.read(16740538 if second else 16740458, 2), 16)\nframe = _movement_compare(state, frame, low16(frame.target_y), state.read(16740544 if second else 16740464, 2), 16)\nrestricted = bool(frame.status & 4)\nif restricted:\n    frame = _duel_action_restricted_choice_fields(state, frame)\n    query_return = 163786\nelse:\n    frame = _movement_move(state, frame, 'target_y', state.read(16740376, 2), 16)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)\n    if not frame.status & 4:\n        frame = _duel_action_direction_fields(state, frame)\n        frame = _movement_add_byte(state, frame, 'target_y', low8(frame.unit))\n        frame = _movement_compare(state, frame, low8(frame.target_y), 4, 8)\n        if frame.status & 1:\n            frame = _duel_actor_store_fields(state, frame, state.table_at(16740376), 0, low16(frame.target_y))\n    query_return = 163640\nframe = _duel_menu_call_fields(state, frame, 162278, query_return)\nframe = _duel_menu_button_fields(state, frame, 5)\nif frame.status & 4:\n    frame = _duel_action_menu_highlight_fields(state, frame, restricted)\nreturn _duel_menu_adjust_memory_word_fields(state, frame, True)"}})

DECLARATIONS.update({'_duel_menu_observations_to_fields': {'signature': 'state: SceneState, frame: DuelTurnFrame, target: int', 'returns': 'FirstDeploymentFrame', 'flow': "checked_duel_turn(frame, state)\nentered = first_replace(FirstDeploymentFrame.unobserved(), target_x=frame.command, target_y=frame.comparison, unit=frame.distance, count=frame.factor, distance=frame.weapon_difference, offset_x=frame.working_value, offset_y=frame.response, choice=frame.variation, roster=frame.actor.cursor(), candidates=frame.opponent.cursor(), controller=frame.lookup.cursor(), stack_cursor=frame.stack.advance(0))\nraise MovementContinuationBoundary(target, entered, 'legacy DuelTurnFrame does not observe actual A3-A6 or full CCR/X; supply FirstDeploymentFrame')"}})

DECLARATIONS.update({'_duel_menu_fields_to_observations': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'DuelTurnFrame', 'flow': 'frame = _resource_cost_frame(state, frame, 163228)\nconditions = DuelConditionObservation(bool(frame.status & 1), bool(frame.status & 4), bool(frame.status & 8), bool(frame.status & 2))\nreturn DuelTurnFrame(frame.target_x, frame.target_y, frame.unit, frame.count, frame.distance, frame.offset_x, frame.offset_y, frame.choice, frame.roster, frame.candidates, frame.controller, frame.stack_cursor, conditions).validate(state)'}})

APPROVED.setdefault('high_level_main_flows.business_movement_support',set()).add('_movement_add_byte')
APPROVED.setdefault('business_reuse',set()).add('choose_first_duel_control_fields')

DECLARATIONS.update({'_stage_duel_words': {'signature': 'state, source_base, command, rows, row_command', 'returns': None, 'flow': "return _duel_scene_legacy_context_fields(state, None, 159760, '_duel_scene_packet_fields')"}})

DECLARATIONS.update({'_configure_duel_action_dialog': {'signature': 'state, position, source', 'returns': None, 'flow': "return _duel_scene_legacy_context_fields(state, None, 160914, '_duel_scene_dialog_fields')"}})

DECLARATIONS.update({'_configure_duel_dialog': {'signature': 'state, position, source', 'returns': None, 'flow': "return _duel_scene_legacy_context_fields(state, None, 159796, '_duel_scene_dialog_fields')"}})

DECLARATIONS.update({'_choose_duel_ai_panel': {'signature': 'state, actor, opponent, controls, preparation=None', 'returns': None, 'flow': "return _duel_scene_legacy_context_fields(state, preparation, 162648, '_duel_scene_auto_loadout_fields')"}})

DECLARATIONS.update({'_choose_duel_side_loadout': {'signature': 'state, second, controls, preparation=None', 'returns': None, 'flow': "return _duel_scene_legacy_context_fields(state, preparation, 159786, 'prepare_duel_loadout_fields')"}})

DECLARATIONS.update({'_wait_duel_status_text': {'signature': 'state, second, controls, preparation=None', 'returns': None, 'flow': "return _duel_scene_legacy_context_fields(state, preparation, 160446, 'prepare_duel_readiness_fields')"}})

DECLARATIONS.update({'_wait_complete_status': {'signature': 'state, second, preparation', 'returns': None, 'flow': "return _duel_scene_legacy_context_fields(state, preparation, 160446, 'prepare_duel_readiness_fields')"}})

DECLARATIONS.update({'_commit_complete_duel_loadout': {'signature': 'state, preparation, second', 'returns': None, 'flow': "return _duel_scene_legacy_context_fields(state, preparation, 160082, 'commit_duel_loadout_fields')"}})

DECLARATIONS.update({'_prepare_complete_second_status': {'signature': 'state, preparation', 'returns': None, 'flow': "return _duel_scene_legacy_context_fields(state, preparation, 160496, 'prepare_duel_readiness_fields')"}})

DECLARATIONS.update({'_consume_complete_first_duel_frame': {'signature': 'state, preparation', 'returns': None, 'flow': "return _duel_scene_legacy_context_fields(state, preparation, 160592, 'begin_duel_combat_fields')"}})

DECLARATIONS.update({'_begin_duel_combat_frame': {'signature': 'state, frame, clear_text', 'returns': None, 'flow': "return _duel_scene_legacy_context_fields(state, frame, 160592, 'begin_duel_combat_fields')"}})

DECLARATIONS.update({'advance_duel_turn': {'signature': 'state: SceneState, frame: DuelTurnFrame, clear_text: bool=True', 'returns': 'DuelTurnOutcome', 'flow': "return _duel_scene_legacy_context_fields(state, frame, 160592, 'begin_duel_combat_fields')"}})

DECLARATIONS.update({'continue_after_first_duel_actor': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnOutcome', 'flow': "return _duel_scene_legacy_context_fields(state, frame, 160662, 'continue_after_first_duel_actor_fields')"}})

DECLARATIONS.update({'choose_duel_turn_action_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnOutcome', 'flow': "return _duel_scene_legacy_context_fields(state, frame, 160806, 'choose_duel_turn_action_fields')"}})

DECLARATIONS.update({'continue_manual_duel_action': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnOutcome', 'flow': "return _duel_scene_legacy_context_fields(state, frame, 160962, 'continue_manual_duel_action_fields')"}})

DECLARATIONS.update({'perform_selected_duel_action_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnOutcome', 'flow': "return _duel_scene_legacy_context_fields(state, frame, 161076, 'perform_selected_duel_action_fields')"}})

DECLARATIONS.update({'show_terminal_duel_result_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnOutcome', 'flow': "return _duel_scene_legacy_context_fields(state, frame, 162192, 'show_terminal_duel_result_fields')"}})

DECLARATIONS.update({'finish_duel_turn_scene': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnOutcome', 'flow': "return _duel_scene_legacy_context_fields(state, frame, 159046, 'finish_duel_scene_fields')"}})

DECLARATIONS.update({'_duel_call_initialization': {'signature': 'state, function, current, *args', 'returns': None, 'flow': "return _duel_scene_legacy_context_fields(state, current, 159156, '_duel_scene_call_fields')"}})

DECLARATIONS.update({'_stage_complete_duel_packet': {'signature': 'state, current, source_address, command, rows, row_command', 'returns': None, 'flow': "return _duel_scene_legacy_context_fields(state, current, 159728, '_duel_scene_packet_fields')"}})

DECLARATIONS.update({'_duel_loadout_ack': {'signature': 'state, frame', 'returns': None, 'flow': "return _duel_scene_legacy_context_fields(state, frame, 159840, '_duel_scene_frame_ack_fields')"}})

DECLARATIONS.update({'_stage_duel_loadout_packet': {'signature': 'state, source_address, row_command, frame', 'returns': None, 'flow': "return _duel_scene_legacy_context_fields(state, frame, 159896, '_duel_scene_packet_fields')"}})

DECLARATIONS.update({'choose_duel_loadout_complete': {'signature': 'state: SceneState, second: bool, frame: DuelTurnFrame', 'returns': 'DuelLoadoutOutcome', 'flow': "return _duel_scene_legacy_context_fields(state, frame, 159786, 'prepare_duel_loadout_fields')"}})

DECLARATIONS.update({'_choose_complete_duel_loadout': {'signature': 'state, second, preparation', 'returns': None, 'flow': "return _duel_scene_legacy_context_fields(state, preparation, 159786, 'prepare_duel_loadout_fields')"}})

DECLARATIONS.update({'_prepare_complete_first_status': {'signature': 'state, preparation', 'returns': None, 'flow': "return _duel_scene_legacy_context_fields(state, preparation, 160412, 'prepare_duel_readiness_fields')"}})

DECLARATIONS.update({'prepare_duel_scene_first_frame': {'signature': 'state: SceneState, context: DuelInitializationContext', 'returns': 'DuelPreparationResult', 'flow': "return _duel_scene_legacy_context_fields(state, context, 159156, 'initialize_duel_scene_fields')"}})

DECLARATIONS.update({'continue_automatic_duel_preparation': {'signature': 'state: SceneState, preparation: DuelPreparationContext', 'returns': 'DuelPreparationResult', 'flow': "return _duel_scene_legacy_context_fields(state, preparation, 162648, '_duel_scene_auto_loadout_fields')"}})

DECLARATIONS.update({'_initialize_duel_scene': {'signature': 'state, context', 'returns': None, 'flow': "return _duel_scene_legacy_context_fields(state, context, 159156, 'initialize_duel_scene_fields')"}})

DECLARATIONS.update({'run_duel_scene': {'signature': 'state: SceneState, context: DuelSceneContext=DuelSceneContext()', 'returns': 'DuelSceneResult', 'flow': "return _duel_scene_legacy_context_fields(state, context, 159156, 'run_duel_scene_fields')"}})

DECLARATIONS.update({'_duel_scene_status_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, value: Word', 'returns': 'FirstDeploymentFrame', 'flow': "if value not in (9472, 9984):\n    raise ValueError('actual duel scene status word required')\nstate.set_status_word(value)\nreturn first_replace(frame, status=value & 31)"}})

DECLARATIONS.update({'_duel_scene_store_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, address: Long, value: Long, width: int=16, clear: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': "if type(clear) is not bool:\n    raise ValueError('actual original CLR/MOVE role required')\nview = state.table_at(address)\nif clear:\n    if width != 16 or value != 0:\n        raise ValueError('original scene CLR.W only')\n    return _duel_actor_clear_word_fields(state, frame, view, 0)\nreturn _duel_actor_store_fields(state, frame, view, 0, value, width)"}})

DECLARATIONS.update({'_duel_scene_frame_ack_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, poll: int, arm: bool=True', 'returns': 'FirstDeploymentFrame', 'flow': "if type(arm) is not bool:\n    raise ValueError('actual entry/resume poll role required')\nif arm:\n    frame = _duel_scene_store_fields(state, frame, 4294964754, 1792)\nframe = _movement_test(state, frame, state.read(4294964754, 1), 8)\nif not frame.status & 4:\n    raise MovementContinuationBoundary(poll, frame, 'actual duel frame BYTE ACK requires external IRQ progress')\nreturn frame"}})

DECLARATIONS.update({'_duel_scene_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "if target == 33748:\n    return sample_battle_action_random_fields(BattlePolicyMemory(state), frame, continuation)\ndef child(memory, entered):\n    if target in (162278, 162320):\n        from .business_reuse import choose_first_duel_control_fields, choose_second_duel_control_fields\n        return choose_second_duel_control_fields(state, entered) if target == 162320 else choose_first_duel_control_fields(state, entered)\n    if target == 163228:\n        return choose_duel_two_option_menu_fields(state, entered)\n    if target == 163324:\n        return choose_first_duel_equipment_fields(state, entered)\n    if target == 163334:\n        return choose_second_duel_equipment_fields(state, entered)\n    if target == 163538:\n        return choose_duel_action_menu_fields(state, entered)\n    if target == 162362:\n        return configure_duel_weapon_motion_fields(state, entered)\n    if target == 162436:\n        return refresh_duel_actors_fields(state, entered)\n    if target == 166810:\n        return update_duel_actor_fields(state, entered)\n    if target == 172698:\n        return choose_duel_ai_command_fields(state, entered)\n    if target == 167824:\n        return scan_duel_thresholds_fields(state, entered)\n    if target == 32906:\n        return enqueue_sound_command_fields(SceneRefreshMemory(state), entered, low8(entered.target_x))\n    if target == 158714:\n        from ..high_level_gameplay_flow.business_services import stage_sprite_word_packet_fields\n        return stage_sprite_word_packet_fields(SceneRefreshMemory(state), entered)\n    if target == 44830:\n        from .business_scene import expand_glyph_stream_fields\n        return expand_glyph_stream_fields(SceneRefreshMemory(state), entered)\n    if target == 26830:\n        from ..high_level_gameplay_flow.business_services import clear_video_sprite_plane_fields\n        return clear_video_sprite_plane_fields(SceneRefreshMemory(state), entered)\n    if target == 56998:\n        from .business_scene import darken_palette_fields\n        return darken_palette_fields(SceneRefreshMemory(state), entered)\n    raise MovementContinuationBoundary(target, entered, 'actual duel controller child lacks a complete current-frame ABI')\nreturn _presentation_call_fields(BattlePresentationMemory(state), frame, continuation, child)"}})

DECLARATIONS.update({'_duel_scene_copy_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, source: Long, count: Word, width: int=32, destination: Long | None=None', 'returns': 'FirstDeploymentFrame', 'flow': "if width not in (16, 32):\n    raise ValueError('actual WORD/LONG scene transfer required')\nframe = first_replace(frame, roster=state.table_at(source).cursor())\nif destination is not None:\n    frame = first_replace(frame, candidates=state.table_at(destination).cursor())\nframe = _movement_move(state, frame, 'target_x', count, 16)\nwhile True:\n    value = frame.roster.word(0) if width == 16 else frame.roster.long(0)\n    frame = first_replace(frame, roster=frame.roster.advance(width // 8))\n    view = frame.auxiliary if destination is None else frame.candidates\n    frame = _duel_actor_store_fields(state, frame, view, 0, value, width)\n    if destination is not None:\n        frame = first_replace(frame, candidates=frame.candidates.advance(width // 8))\n    remaining = u16(low16(frame.target_x) - 1)\n    frame = first_replace(frame, target_x=replace_word(frame.target_x, remaining))\n    if remaining == 65535:\n        return frame"}})

DECLARATIONS.update({'_duel_scene_dialog_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, source: Long, position: Word, dimensions: bool=True', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _duel_scene_store_fields(state, frame, 16740364, position)\nframe = _duel_scene_store_fields(state, frame, 16740366, source, 32)\nif dimensions:\n    frame = _duel_scene_store_fields(state, frame, 16740372, 1)\n    frame = _duel_scene_store_fields(state, frame, 16740374, 2)\nreturn frame'}})

DECLARATIONS.update({'_duel_scene_packet_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, source: Long, command: Long, rows: Word, row_command: Word, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "frame = first_replace(frame, roster=state.table_at(source).cursor())\nframe = _movement_move_long(state, frame, 'target_x', command)\nframe = _movement_move(state, frame, 'target_y', rows, 16)\nframe = _movement_move(state, frame, 'unit', row_command, 16)\nreturn _duel_scene_call_fields(state, frame, 158714, continuation)"}})

DECLARATIONS.update({'initialize_duel_scene_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 159156)\nframe = _duel_scene_status_fields(state, frame, 9984)\nframe = _movement_move(state, frame, 'target_x', state.read(4294964742, 2), 16)\nframe = _movement_move(state, frame, 'target_x', low8(frame.target_x) & 191, 8)\nframe = _duel_scene_store_fields(state, frame, 12582916, low16(frame.target_x))\nframe = _duel_scene_store_fields(state, frame, 4294964754, 0, clear=True)\nframe = _duel_scene_call_fields(state, frame, 26830, 159184)\nfor command in (33592, 33336, 33799, 34156, 36151, 37524, 35587):\n    frame = _duel_scene_store_fields(state, frame, 12582916, command)\nfor address, value, width in ((16740446, 4194304, 32), (16740456, 34816, 16), (16740434, 1, 16), (16740526, 16777216, 32), (16740536, 40960, 16), (16740514, 1, 16)):\n    frame = _duel_scene_store_fields(state, frame, address, value, width)\nfor address in (16740592, 16740598, 16740600):\n    frame = _duel_scene_store_fields(state, frame, address, 0, clear=True)\nfor officer_address, destination in ((16740458, 16740475), (16740538, 16740555)):\n    frame = _movement_move_long(state, frame, 'distance', 0)\n    frame = first_replace(frame, scratch=state.table_at(4294961800).cursor())\n    frame = _movement_move(state, frame, 'distance', state.read(officer_address, 2), 16)\n    frame = _movement_multiply_word(state, frame, 'distance', 3)\n    frame = first_replace(frame, scratch=frame.scratch.advance(s16(low16(frame.distance))))\n    for offset in (0, 2):\n        value = frame.scratch.byte(0)\n        frame = first_replace(frame, scratch=frame.scratch.advance(1))\n        frame = _duel_scene_store_fields(state, frame, destination + offset, value, 8)\n    frame = _duel_scene_store_fields(state, frame, destination + 4, frame.scratch.byte(0), 8)\nframe = _duel_scene_store_fields(state, frame, 12582916, 1073741824, 32)\nframe = first_replace(frame, auxiliary=state.table_at(12582912).cursor())\nframe = _duel_scene_copy_fields(state, frame, 443316, 12287)\nframe = _duel_scene_store_fields(state, frame, 12582916, 1073741827, 32)\nframe = _duel_scene_copy_fields(state, frame, 564700, 31)\nframe = first_replace(frame, roster=state.table_at(566310).cursor(), candidates=state.table_at(4294955776).cursor())\nframe = _movement_move(state, frame, 'target_x', 1, 16)\nframe = _movement_move(state, frame, 'target_y', 2, 16)\nframe = _movement_move(state, frame, 'count', 9, 16)\nframe = _duel_scene_call_fields(state, frame, 44830, 159468)\nframe = _duel_scene_copy_fields(state, frame, 4294955776, 79)\nframe = _duel_scene_store_fields(state, frame, 12582916, 1342177283, 32)\nframe = _duel_scene_copy_fields(state, frame, 492468, 47)\nframe = _duel_scene_store_fields(state, frame, 12582916, 1107296259, 32)\nfor officer, continuation in ((16740458, 159536), (16740538, 159554)):\n    frame = _movement_move(state, frame, 'choice', state.read(officer, 2), 16)\n    frame = _movement_move(state, frame, 'target_x', 1, 16)\n    frame = _movement_move(state, frame, 'target_y', 2, 16)\n    frame = _duel_scene_call_fields(state, frame, 163100, continuation)\nframe = first_replace(frame, roster=state.table_at(166074).cursor())\nframe = _movement_move(state, frame, 'target_x', 1, 16)\nframe = _movement_move(state, frame, 'target_y', 2, 16)\nframe = _movement_move(state, frame, 'count', 1, 16)\nframe = _duel_scene_call_fields(state, frame, 163158, 159576)\nframe = _duel_scene_call_fields(state, frame, 163190, 159580)\nframe = _duel_scene_copy_fields(state, frame, 163968, 31, 32, 4294966016)\nframe = _duel_scene_store_fields(state, frame, 4294963998, 1)\nframe = first_replace(frame, roster=state.table_at(492660).cursor())\nframe = _movement_compare(state, frame, state.read(16740594, 2), 3, 16)\nif frame.status & 4:\n    frame = first_replace(frame, roster=state.table_at(493142).cursor())\nfor source_override, continuation, control in ((None, 159644, 1610612739), (493630, 159690, 1879048195)):\n    if source_override is not None:\n        frame = first_replace(frame, roster=state.table_at(source_override).cursor())\n    frame = first_replace(frame, candidates=state.table_at(16736256).cursor())\n    frame = _movement_move(state, frame, 'target_x', 1280, 16)\n    frame = _duel_scene_call_fields(state, frame, 163858, continuation)\n    frame = _duel_scene_store_fields(state, frame, 12582916, control, 32)\n    frame = _duel_scene_copy_fields(state, frame, 16736256, 1279, 16)\nframe = _duel_scene_store_fields(state, frame, 4294964884, 1539)\nframe = _duel_scene_store_fields(state, frame, 4294964882, 1540)\nframe = _duel_scene_packet_fields(state, frame, 164128, 1610612776, 3, 59904, 159754)\nframe = _duel_scene_call_fields(state, frame, 44294, 159760)\nreturn _duel_scene_packet_fields(state, frame, 164212, 1610612776, 5, 60288, 159786)"}})

DECLARATIONS.update({'_duel_scene_auto_loadout_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, second: bool', 'returns': 'tuple[FirstDeploymentFrame, bool]', 'flow': "frame = first_replace(frame, roster=state.table_at(16740512 if second else 16740432).cursor())\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(30), 16)\nframe = first_replace(frame, controller=state.table_at(162710).cursor())\nframe = _duel_scene_call_fields(state, frame, 167824, 162678)\nframe = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_y', low16(frame.target_y), 1)\ntarget = state.read(u32(162722 + s16(low16(frame.target_y))), 4)\nframe = first_replace(frame, scan=state.table_at(target).cursor())\nframe = _duel_scene_call_fields(state, frame, target, 162686)\nframe = _movement_test(state, frame, low16(frame.offset_y), 16)\ncommit = not bool(frame.status & 4)\nframe = _movement_compare_address(state, frame, frame.roster.base, 16740432)\nreturn (frame, commit)"}})

DECLARATIONS.update({'prepare_duel_loadout_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, second: bool=False', 'returns': 'tuple[bool, FirstDeploymentFrame]', 'flow': "if type(second) is not bool:\n    raise ValueError('actual first/second loadout role required')\nframe = _resource_cost_frame(state, frame, 160100 if second else 159786)\nmode = 16740363 if second else 16740362\nactor = 16740512 if second else 16740432\nweapon = 16740524 if second else 16740444\ncontrol_choice = 16740578 if second else 16740498\nquery = 162320 if second else 162278\nframe = _movement_compare(state, frame, state.read(mode, 1), 3, 8)\nif not frame.status & 4:\n    frame = _duel_scene_dialog_fields(state, frame, 166078, 50688)\n    if second:\n        frame = _duel_scene_store_fields(state, frame, 16740570, 1)\nif not second:\n    frame = _duel_scene_call_fields(state, frame, 159110, 159836)\ncontroller = False\nframe = _duel_scene_status_fields(state, frame, 9472)\nwhile True:\n    frame = _duel_scene_frame_ack_fields(state, frame, 160164 if second else 159846)\n    frame = _duel_scene_call_fields(state, frame, 159110, 160174 if second else 159856)\n    frame = _duel_scene_call_fields(state, frame, 162436, 160178 if second else 159860)\n    if not second:\n        frame = _duel_scene_store_fields(state, frame, 16740490, 0, clear=True)\n    frame = _movement_compare(state, frame, state.read(mode, 1), 3, 8)\n    if frame.status & 4:\n        frame, commit = _duel_scene_auto_loadout_fields(state, frame, second)\n        second = not bool(frame.status & 4)\n        actor = 16740512 if second else 16740432\n        mode = 16740363 if second else 16740362\n        weapon = 16740524 if second else 16740444\n        control_choice = 16740578 if second else 16740498\n        query = 162320 if second else 162278\n        if not commit and (not second):\n            continue\n        controller = False\n        break\n    frame = first_replace(frame, roster=state.table_at(weapon).cursor())\n    frame = _duel_scene_call_fields(state, frame, query, 160200 if second else 159888)\n    frame = _duel_scene_call_fields(state, frame, 163334 if second else 163324, 160204 if second else 159892)\n    frame = _movement_test(state, frame, state.read(16740364, 2), 16)\n    if not frame.status & 4:\n        continue\n    frame = _duel_scene_packet_fields(state, frame, 164354 if second else 164332, 1610612740, 1, 60740 if second else 60680, 160238 if second else 159926)\n    frame = _duel_scene_call_fields(state, frame, query, 160242 if second else 159930)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 240, 16)\n    if frame.status & 4:\n        continue\n    frame = _movement_move(state, frame, 'target_x', 172, 16)\n    frame = _duel_scene_call_fields(state, frame, 32906, 160258 if second else 159946)\n    frame = _movement_compare(state, frame, state.read(mode, 1), 3, 8)\n    controller = not bool(frame.status & 4)\n    break\nif controller:\n    frame = _duel_scene_call_fields(state, frame, 163190, 160274 if second else 159962)\n    frame = _duel_scene_dialog_fields(state, frame, 166154, 50688)\n    frame = _duel_scene_status_fields(state, frame, 9472)\n    while True:\n        frame = _duel_scene_frame_ack_fields(state, frame, 160318 if second else 160006)\n        frame = _duel_scene_call_fields(state, frame, 159110, 160328 if second else 160016)\n        frame = _duel_scene_call_fields(state, frame, 162436, 160332 if second else 160020)\n        frame = first_replace(frame, roster=state.table_at(control_choice).cursor())\n        frame = _duel_scene_call_fields(state, frame, 162320 if second else 162278, 160342 if second else 160030)\n        frame = _duel_scene_call_fields(state, frame, 163228, 160346 if second else 160034)\n        frame = _movement_test(state, frame, state.read(16740364, 2), 16)\n        if not frame.status & 4:\n            continue\n        frame = _duel_scene_call_fields(state, frame, 162320 if second else 162278, 160358 if second else 160046)\n        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 240, 16)\n        if frame.status & 4:\n            continue\n        frame = _movement_move(state, frame, 'target_x', 172, 16)\n        frame = _duel_scene_call_fields(state, frame, 32906, 160374 if second else 160062)\n        frame = first_replace(frame, roster=state.table_at(control_choice).cursor())\n        frame = _movement_test(state, frame, frame.roster.word(0), 16)\n        if not frame.status & 4:\n            frame = _duel_scene_store_fields(state, frame, mode, 3, 8)\n        break\nreturn (second, commit_duel_loadout_fields(state, frame, second))"}})

DECLARATIONS.update({'commit_duel_loadout_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, second: bool', 'returns': 'FirstDeploymentFrame', 'flow': "if type(second) is not bool:\n    raise ValueError('actual original selected loadout side required')\nframe = _duel_scene_status_fields(state, frame, 9984)\nframe = first_replace(frame, roster=state.table_at(16740512 if second else 16740432).cursor())\nframe = _duel_scene_call_fields(state, frame, 162362, 160408 if second else 160096)\nreturn _duel_scene_call_fields(state, frame, 163190, 160412 if second else 160100)"}})

DECLARATIONS.update({'prepare_duel_readiness_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "for second in (False, True):\n    if second:\n        frame = _duel_scene_status_fields(state, frame, 9984)\n        frame = _duel_scene_call_fields(state, frame, 163190, 160502)\n    frame = _duel_scene_call_fields(state, frame, 33748, 160508 if second else 160418)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 3, 16)\n    frame = _movement_compare(state, frame, low16(frame.target_x), 3, 16)\n    if frame.status & 4:\n        frame = _movement_move(state, frame, 'target_x', 0, 16)\n    if second:\n        frame = _movement_add_word(state, frame, 'target_x', 3)\n    frame = _duel_scene_call_fields(state, frame, 164392, 160526 if second else 160434)\n    frame = _movement_move(state, frame, 'target_x', 165, 16)\n    frame = _duel_scene_call_fields(state, frame, 32906, 160538 if second else 160446)\n    frame = _duel_scene_store_fields(state, frame, 16740514 if second else 16740434, 0, clear=True)\n    frame = _duel_scene_status_fields(state, frame, 9472)\n    while True:\n        frame = _duel_scene_frame_ack_fields(state, frame, 160554 if second else 160462)\n        if not second:\n            frame = _duel_scene_call_fields(state, frame, 159110, 160472)\n        frame = _duel_scene_call_fields(state, frame, 162436, 160564 if second else 160476)\n        frame = _movement_test(state, frame, state.read(16740364, 2), 16)\n        if not frame.status & 4:\n            continue\n        frame = _duel_scene_call_fields(state, frame, 162320 if second else 162278, 160576 if second else 160488)\n        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 240, 16)\n        if not frame.status & 4:\n            break\nframe = _movement_move(state, frame, 'target_x', 139, 16)\nreturn _duel_scene_call_fields(state, frame, 32906, 160592)"}})

DECLARATIONS.update({'begin_duel_combat_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, clear_text: bool=True', 'returns': 'tuple[str, FirstDeploymentFrame]', 'flow': "frame = _resource_cost_frame(state, frame, 160592 if clear_text else 160604)\nif type(clear_text) is not bool:\n    raise ValueError('actual loop continuation required')\nif clear_text:\n    frame = _duel_scene_status_fields(state, frame, 9984)\n    frame = _duel_scene_call_fields(state, frame, 163190, 160600)\n    frame = _duel_scene_status_fields(state, frame, 9472)\nframe = _duel_scene_frame_ack_fields(state, frame, 160610)\nframe = _duel_scene_actor_fields(state, frame, False)\nreturn continue_after_first_duel_actor_fields(state, frame)"}})

DECLARATIONS.update({'_duel_scene_actor_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, second: bool', 'returns': 'FirstDeploymentFrame', 'flow': "if type(second) is not bool:\n    raise ValueError('actual original actor role required')\nif second:\n    actor, opponent, mode = (16740512, 16740432, 16740363)\n    query, query_return, ai_return, actor_return = (162320, 160678, 160698, 160708)\nelse:\n    actor, opponent, mode = (16740432, 16740512, 16740362)\n    query, query_return, ai_return, actor_return = (162278, 160632, 160652, 160662)\nframe = first_replace(frame, roster=state.table_at(actor).cursor(), candidates=state.table_at(opponent).cursor())\nframe = _duel_scene_call_fields(state, frame, query, query_return)\nframe = _duel_scene_store_fields(state, frame, actor, low16(frame.target_x))\nframe = _movement_compare(state, frame, state.read(mode, 1), 3, 8)\nif frame.status & 4:\n    frame = _duel_scene_call_fields(state, frame, 172698, ai_return)\n    frame = _duel_scene_store_fields(state, frame, actor, low16(frame.target_x))\nreturn _duel_scene_call_fields(state, frame, 166810, actor_return)"}})

DECLARATIONS.update({'continue_after_first_duel_actor_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'tuple[str, FirstDeploymentFrame]', 'flow': "frame = _resource_cost_frame(state, frame, 160662)\nframe = _duel_scene_actor_fields(state, frame, True)\nframe = _duel_scene_call_fields(state, frame, 161030, 160712)\nframe = _duel_scene_store_fields(state, frame, 16740376, 0, clear=True)\nframe = _movement_test(state, frame, state.read(16740460, 2), 16)\nif frame.status & 4:\n    return ('terminal', frame)\nframe = _duel_scene_store_fields(state, frame, 16740376, 32768)\nframe = _movement_test(state, frame, state.read(16740540, 2), 16)\nif frame.status & 4:\n    return ('terminal', frame)\nframe = _movement_move(state, frame, 'target_y', state.read(16740434, 2), 16)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_y) | state.read(16740514, 2), 16)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 53248, 16)\nif not frame.status & 4:\n    return ('next_frame', frame)\nframe = _duel_scene_store_fields(state, frame, 16740376, 0, clear=True)\nframe = _movement_move(state, frame, 'target_x', state.read(16740432, 2), 16)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 64, 16)\nif frame.status & 4:\n    frame = _duel_scene_store_fields(state, frame, 16740376, 32768)\n    frame = _movement_move(state, frame, 'target_x', state.read(16740512, 2), 16)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 64, 16)\n    if frame.status & 4:\n        return ('next_frame', frame)\nreturn ('action', frame)"}})

DECLARATIONS.update({'choose_duel_turn_action_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'tuple[str, FirstDeploymentFrame]', 'flow': "frame = _resource_cost_frame(state, frame, 160806)\nframe = _duel_scene_status_fields(state, frame, 9984)\nframe = _duel_scene_store_fields(state, frame, 4294955264, 0, clear=True)\nframe = _movement_test(state, frame, state.read(16740376, 2), 16)\nsecond = bool(frame.status & 8)\nmode = state.read(16740363 if second else 16740362, 1)\nframe = _movement_compare(state, frame, mode, 3, 8)\nif frame.status & 4:\n    frame = _movement_move(state, frame, 'target_x', state.read(16740512 if second else 16740432, 2), 16)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 3, 16)\n    frame = _duel_scene_store_fields(state, frame, 16740377, low8(frame.target_x), 8)\n    return ('submit', frame)\nframe = _movement_move(state, frame, 'target_y', state.read(16740538 if second else 16740458, 2), 16)\nframe = _movement_compare(state, frame, low16(frame.target_y), state.read(16740544 if second else 16740464, 2), 16)\nlinked = bool(frame.status & 4)\nframe = _duel_scene_dialog_fields(state, frame, 166180 if linked else 166122, 52096 if linked else 51008, False)\nframe = _movement_move(state, frame, 'target_x', 173, 16)\nframe = _duel_scene_call_fields(state, frame, 32906, 160962)\nreturn continue_manual_duel_action_fields(state, frame)"}})

DECLARATIONS.update({'continue_manual_duel_action_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'tuple[str, FirstDeploymentFrame]', 'flow': "frame = _resource_cost_frame(state, frame, 160962)\nframe = _duel_scene_status_fields(state, frame, 9472)\nwhile True:\n    frame = _duel_scene_frame_ack_fields(state, frame, 160972)\n    frame = _duel_scene_call_fields(state, frame, 162436, 160982)\n    frame = _duel_scene_call_fields(state, frame, 162278, 160986)\n    frame = _movement_test(state, frame, state.read(16740376, 2), 16)\n    if frame.status & 8:\n        frame = _duel_scene_call_fields(state, frame, 162320, 160998)\n    stack = frame.stack_cursor.advance(-2)\n    stack.set_word(0, low16(frame.target_x))\n    frame = first_replace(frame, stack_cursor=stack)\n    frame = _movement_test(state, frame, low16(frame.target_x), 16)\n    frame = _duel_scene_call_fields(state, frame, 163538, 161004)\n    saved = frame.stack_cursor.word(0)\n    frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))\n    frame = _movement_move(state, frame, 'target_x', saved, 16)\n    frame = _movement_test(state, frame, state.read(16740364, 2), 16)\n    if not frame.status & 4:\n        continue\n    frame = _duel_scene_button_fields(state, frame, 5)\n    if not frame.status & 4:\n        return ('submit', frame)\n    frame = _duel_scene_button_fields(state, frame, 4)\n    if not frame.status & 4:\n        return ('next_frame_clear', frame)"}})

DECLARATIONS.update({'_duel_scene_button_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, bit: int', 'returns': 'FirstDeploymentFrame', 'flow': "if bit not in (4, 5):\n    raise ValueError('actual manual action button required')\nframe = _postbattle_bit_fields(frame, bool(frame.target_x & 1 << bit))\nstate.sr = state.sr & 65504 | frame.status\nreturn frame"}})

DECLARATIONS.update({'perform_selected_duel_action_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 161076)\nframe = _movement_move(state, frame, 'target_x', 172, 16)\nframe = _duel_scene_call_fields(state, frame, 32906, 161086)\nframe = _duel_scene_status_fields(state, frame, 9984)\nframe = _duel_scene_call_fields(state, frame, 163190, 161094)\nframe = first_replace(frame, roster=state.table_at(16740432).cursor(), candidates=state.table_at(16740512).cursor())\nframe = _movement_test(state, frame, state.read(16740376, 2), 16)\nif frame.status & 8:\n    frame = first_replace(frame, roster=state.table_at(16740512).cursor(), candidates=state.table_at(16740432).cursor())\nframe = _movement_move(state, frame, 'target_x', state.read(16740376, 2), 16)\nframe = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_x', low16(frame.target_x), 2)\ntarget = u32(161142 + s16(low16(frame.target_x)))\nreturn _duel_scene_call_fields(state, frame, target, 161138)"}})

DECLARATIONS.update({'show_terminal_duel_result_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 162192)\nframe = _duel_scene_frame_ack_fields(state, frame, 162198)\nframe = _duel_scene_call_fields(state, frame, 161030, 162208)\nframe = _duel_scene_frame_ack_fields(state, frame, 162214)\nframe = _duel_scene_status_fields(state, frame, 9984)\nframe = _movement_move(state, frame, 'target_x', 31, 16)\nframe = _movement_test(state, frame, state.read(16740376, 2), 16)\nif frame.status & 8:\n    frame = _movement_move(state, frame, 'target_x', 34, 16)\nframe = _duel_scene_call_fields(state, frame, 164392, 162244)\nframe = _duel_scene_call_fields(state, frame, 161658, 162248)\nframe = _duel_scene_call_fields(state, frame, 163190, 162252)\nframe = _movement_move(state, frame, 'target_x', 32, 16)\nframe = _movement_test(state, frame, state.read(16740376, 2), 16)\nif frame.status & 8:\n    frame = _movement_add_word(state, frame, 'target_x', 1)\nframe = _duel_scene_call_fields(state, frame, 164392, 162270)\nreturn _duel_scene_call_fields(state, frame, 161720, 162274)"}})

DECLARATIONS.update({'finish_duel_scene_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 159046)\nframe = _duel_scene_status_fields(state, frame, 9472)\nwhile True:\n    frame = _duel_scene_frame_ack_fields(state, frame, 159056)\n    frame = _duel_scene_call_fields(state, frame, 162436, 159066)\n    step = state.read(16740598, 2)\n    frame = _movement_compare(state, frame, step, 16, 16)\n    if not frame.status & 1:\n        return frame\n    frame = _movement_move(state, frame, 'target_x', state.read(16740598, 2), 16)\n    frame = _movement_move(state, frame, 'target_y', 64, 16)\n    frame = first_replace(frame, roster=state.table_at(163968).cursor())\n    frame = _duel_scene_call_fields(state, frame, 56998, 159100)\n    value = state.read(16740598, 2)\n    frame, value = _movement_binary_flags(state, frame, value, 1, 16)\n    state.write(16740598, 2, value)"}})

DECLARATIONS.update({'run_duel_scene_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 159156)\nframe = initialize_duel_scene_fields(state, frame)\nsecond = False\nwhile True:\n    committed_second, frame = prepare_duel_loadout_fields(state, frame, second)\n    if committed_second:\n        break\n    second = True\nframe = prepare_duel_readiness_fields(state, frame)\nclear_text = True\nwhile True:\n    phase, frame = begin_duel_combat_fields(state, frame, clear_text)\n    if phase == 'terminal':\n        frame = show_terminal_duel_result_fields(state, frame)\n        return finish_duel_scene_fields(state, frame)\n    if phase == 'action':\n        phase, frame = choose_duel_turn_action_fields(state, frame)\n        if phase == 'submit':\n            frame = perform_selected_duel_action_fields(state, frame)\n            phase = 'next_frame_clear'\n    clear_text = phase == 'next_frame_clear'"}})

DECLARATIONS.update({'_duel_scene_legacy_context_fields': {'signature': 'state: SceneState, observation, target: int, sole_core: str', 'returns': 'FirstDeploymentFrame', 'flow': "if type(state) is not SceneState or type(sole_core) is not str:\n    raise ValueError('actual Scene state and named sole duel core required')\nif type(observation) is DuelTurnFrame:\n    return _duel_menu_observations_to_fields(state, observation, target)\nif type(observation) is DuelSceneContext:\n    observation.validate()\n    if observation.initialization is not None:\n        observation = observation.initialization\n    else:\n        raise MovementContinuationBoundary(target, FirstDeploymentFrame.unobserved(), 'legacy scene omits its current complete live-in; use ' + sole_core)\nif type(observation) is DuelInitializationResult:\n    observation.validate(state)\n    observation = observation.preparation\nentered = FirstDeploymentFrame.unobserved()\nif type(observation) is DuelInitializationContext:\n    observation.validate(state)\n    values = observation.frame\n    entered = first_replace(entered, target_x=values.command, target_y=values.comparison, unit=values.distance, count=values.factor, distance=values.weapon_difference, offset_x=observation.glyph_work, offset_y=observation.response, choice=values.variation, controller=values.lookup, stack_cursor=observation.stack.advance(0))\nelif type(observation) is DuelPreparationContext:\n    observation.validate(state)\n    values = observation.frame\n    entered = first_replace(entered, target_x=values.command, target_y=values.comparison, unit=values.distance, count=values.factor, distance=values.weapon_difference, offset_x=values.working_value, offset_y=observation.response, choice=values.variation, roster=observation.actor.cursor(), candidates=observation.opponent.cursor(), controller=values.lookup, stack_cursor=observation.stack.advance(0))\nelif type(observation) is DuelControlContext:\n    observation.validate()\n    entered = first_replace(entered, target_x=observation.command, target_y=observation.mode)\nelif observation is not None:\n    raise ValueError('actual historical duel observation required')\nraise MovementContinuationBoundary(target, entered, 'legacy duel observation omits live A3-A6 and full CCR/X; use ' + sole_core)"}})

APPROVED.setdefault('business_reuse',set()).add('choose_second_duel_control_fields')
APPROVED.setdefault('business_scene',set()).update({'expand_glyph_stream_fields','darken_palette_fields'})
APPROVED.setdefault('business_services',set()).update({'stage_sprite_word_packet_fields','clear_video_sprite_plane_fields'})

DECLARATIONS.update({'show_active_duel_turn_label': {'signature': 'state: SceneState', 'returns': 'Long', 'flow': "return _duel_scene_legacy_context_fields(state, None, 161030, 'show_active_duel_turn_label_fields')"}})

DECLARATIONS.update({'wait_active_duel_action': {'signature': 'state: SceneState, controls: DuelControlContext=DuelControlContext()', 'returns': 'DuelControlContext', 'flow': "return _duel_scene_legacy_context_fields(state, controls, 161658, 'wait_active_duel_action_fields')"}})

DECLARATIONS.update({'wait_either_duel_action': {'signature': 'state: SceneState, controls: DuelControlContext=DuelControlContext()', 'returns': 'DuelControlContext', 'flow': "return _duel_scene_legacy_context_fields(state, controls, 161720, 'wait_either_duel_action_fields')"}})

DECLARATIONS.update({'choose_duel_status_text': {'signature': 'state: SceneState, selection: Word, retained: Long=0', 'returns': 'Long', 'flow': "uint(selection, 16, 'actual selected status WORD')\nuint(retained, 32, 'actual caller retained D0 LONG')\nentered = first_replace(FirstDeploymentFrame.unobserved(), target_x=replace_word(retained, selection))\nreturn choose_duel_status_text_fields(state, entered).target_x"}})

DECLARATIONS.update({'choose_duel_status_text_complete': {'signature': 'state: SceneState, selection: Word, frame: DuelTurnFrame', 'returns': 'DuelTurnFrame', 'flow': "checked_duel_turn(frame, state)\nuint(selection, 16, 'actual selected status WORD')\nentered = first_replace(FirstDeploymentFrame.unobserved(), target_x=replace_word(frame.command, selection))\nreturned = choose_duel_status_text_fields(state, entered)\nreturn replace(frame, command=returned.target_x, lookup=returned.controller, conditions=DuelConditionObservation(bool(returned.status & 1), bool(returned.status & 4), bool(returned.status & 8), bool(returned.status & 2))).validate(state)"}})

DECLARATIONS.update({'show_active_duel_turn_label_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnFrame', 'flow': "entered = _duel_scene_legacy_context_fields(state, frame, 161030, 'show_active_duel_turn_label_fields')\nreturn _duel_menu_fields_to_observations(state, show_active_duel_turn_label_fields(state, entered))"}})

DECLARATIONS.update({'wait_active_duel_action_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnFrame', 'flow': "entered = _duel_scene_legacy_context_fields(state, frame, 161658, 'wait_active_duel_action_fields')\nreturn _duel_menu_fields_to_observations(state, wait_active_duel_action_fields(state, entered))"}})

DECLARATIONS.update({'wait_either_duel_action_complete': {'signature': 'state: SceneState, frame: DuelTurnFrame', 'returns': 'DuelTurnFrame', 'flow': "entered = _duel_scene_legacy_context_fields(state, frame, 161720, 'wait_either_duel_action_fields')\nreturn _duel_menu_fields_to_observations(state, wait_either_duel_action_fields(state, entered))"}})

DECLARATIONS.update({'show_active_duel_turn_label_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 161030)\nframe = first_replace(frame, roster=state.table_at(164256).cursor())\nframe = _movement_move(state, frame, 'unit', 60424, 16)\nframe = _movement_move(state, frame, 'target_x', state.read(16740360, 2), 16)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 1, 16)\nif not frame.status & 4:\n    frame = first_replace(frame, roster=state.table_at(164278).cursor())\n    frame = _movement_move(state, frame, 'unit', 60484, 16)\nframe = _movement_move_long(state, frame, 'target_x', 1610612740)\nframe = _movement_move(state, frame, 'target_y', 1, 16)\nfrom ..high_level_gameplay_flow.business_services import stage_sprite_word_packet_fields\nreturn stage_sprite_word_packet_fields(SceneRefreshMemory(state), frame)"}})

DECLARATIONS.update({'choose_duel_status_text_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "if type(state) is not SceneState or type(frame) is not FirstDeploymentFrame:\n    raise ValueError('actual Scene state and current status frame required')\nframe.validate(state, False)\nif frame.target_x is None:\n    raise MovementContinuationBoundary(164392, frame, 'actual selected D0 LONG required')\nframe = first_replace(frame, controller=state.table_at(164416).cursor())\nframe = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_x', low16(frame.target_x), 2)\npointer = frame.controller.long(low16(frame.target_x))\nframe = _duel_scene_store_fields(state, frame, 16740366, pointer, 32)\nreturn _duel_scene_store_fields(state, frame, 16740364, 50688)"}})

DECLARATIONS.update({'_wait_duel_action_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, either: bool, resume_poll: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': "if type(either) is not bool or type(resume_poll) is not bool:\n    raise ValueError('actual original wait role and poll continuation required')\nframe = _resource_cost_frame(state, frame, 161754 if either and resume_poll else 161668 if resume_poll else 161744 if either else 161658)\nif not resume_poll:\n    frame = _duel_scene_status_fields(state, frame, 9472)\nwhile True:\n    frame = _duel_scene_frame_ack_fields(state, frame, 161754 if either else 161668, arm=not resume_poll)\n    resume_poll = False\n    value = state.read(16740602, 2)\n    frame, value = _movement_binary_flags(state, frame, value, 1, 16, True)\n    state.write(16740602, 2, value)\n    frame = _duel_scene_call_fields(state, frame, 162436, 161770 if either else 161684)\n    frame = _movement_test(state, frame, state.read(16740364, 2), 16)\n    if not frame.status & 4:\n        continue\n    frame = _duel_scene_call_fields(state, frame, 162278, 161782 if either else 161696)\n    if either:\n        frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)\n        frame = _movement_save_longs(state, frame, ('target_y',))\n        frame = _duel_scene_call_fields(state, frame, 162320, 161792)\n        frame = _movement_restore_longs(state, frame, ('target_y',))\n        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) | low16(frame.target_y), 16)\n    else:\n        frame = _movement_test(state, frame, state.read(16740376, 2), 16)\n        if frame.status & 8:\n            frame = _duel_scene_call_fields(state, frame, 162320, 161708)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 112, 16)\n    if not frame.status & 4:\n        return _duel_scene_status_fields(state, frame, 9984)"}})

DECLARATIONS.update({'wait_active_duel_action_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _wait_duel_action_fields(state, frame, False)'}})

DECLARATIONS.update({'wait_either_duel_action_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _resource_cost_frame(state, frame, 161720)\nframe = _movement_compare(state, frame, state.read(16740362, 1), 3, 8)\nif frame.status & 4:\n    return _wait_duel_action_fields(state, frame, False)\nframe = _movement_compare(state, frame, state.read(16740363, 1), 3, 8)\nreturn _wait_duel_action_fields(state, frame, not bool(frame.status & 4))'}})

DECLARATIONS.update({'continue_duel_action_wait_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, either: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': 'return _wait_duel_action_fields(state, frame, either, True)'}})

DECLARATIONS.update({'_duel_scene_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "if target == 33748:\n    return sample_battle_action_random_fields(BattlePolicyMemory(state), frame, continuation)\ndef child(memory, entered):\n    if target in (162278, 162320):\n        from .business_reuse import choose_first_duel_control_fields, choose_second_duel_control_fields\n        return choose_second_duel_control_fields(state, entered) if target == 162320 else choose_first_duel_control_fields(state, entered)\n    if target == 163228:\n        return choose_duel_two_option_menu_fields(state, entered)\n    if target == 163324:\n        return choose_first_duel_equipment_fields(state, entered)\n    if target == 163334:\n        return choose_second_duel_equipment_fields(state, entered)\n    if target == 163538:\n        return choose_duel_action_menu_fields(state, entered)\n    if target == 162362:\n        return configure_duel_weapon_motion_fields(state, entered)\n    if target == 162436:\n        return refresh_duel_actors_fields(state, entered)\n    if target == 166810:\n        return update_duel_actor_fields(state, entered)\n    if target == 172698:\n        return choose_duel_ai_command_fields(state, entered)\n    if target == 167824:\n        return scan_duel_thresholds_fields(state, entered)\n    if target == 161030:\n        return show_active_duel_turn_label_fields(state, entered)\n    if target == 161658:\n        return wait_active_duel_action_fields(state, entered)\n    if target == 161720:\n        return wait_either_duel_action_fields(state, entered)\n    if target == 164392:\n        return choose_duel_status_text_fields(state, entered)\n    if target == 32906:\n        return enqueue_sound_command_fields(SceneRefreshMemory(state), entered, low8(entered.target_x))\n    if target == 158714:\n        from ..high_level_gameplay_flow.business_services import stage_sprite_word_packet_fields\n        return stage_sprite_word_packet_fields(SceneRefreshMemory(state), entered)\n    if target == 44830:\n        from .business_scene import expand_glyph_stream_fields\n        return expand_glyph_stream_fields(SceneRefreshMemory(state), entered)\n    if target == 26830:\n        from ..high_level_gameplay_flow.business_services import clear_video_sprite_plane_fields\n        return clear_video_sprite_plane_fields(SceneRefreshMemory(state), entered)\n    if target == 56998:\n        from .business_scene import darken_palette_fields\n        return darken_palette_fields(SceneRefreshMemory(state), entered)\n    raise MovementContinuationBoundary(target, entered, 'actual duel controller child lacks a complete current-frame ABI')\nreturn _presentation_call_fields(BattlePresentationMemory(state), frame, continuation, child)"}})


# B44 complete duel-child source shapes; ordinary lowerers remain unchanged.
DUEL_CHILDREN_FIELDS_DECLARATIONS = {'advance_duel_entry_palette': {'signature': 'state: SceneState, preparation: DuelPreparationContext | None=None', 'returns': 'DuelPreparationContext | None', 'flow': "entered = _duel_scene_legacy_context_fields(state, preparation, 159110, 'advance_duel_entry_palette_fields')\nadvance_duel_entry_palette_fields(state, entered)\nreturn preparation"}, 'upload_duel_officer_name': {'signature': 'state: SceneState, officer: Word, colors: DuelGlyphContext, current: DuelInitializationResult | None=None', 'returns': 'DuelGlyphContext | DuelInitializationResult', 'flow': "uint(officer, 16, 'officer')\ncolors.validate()\nentered = _duel_scene_legacy_context_fields(state, current, 163100, 'upload_duel_officer_name_fields')\nreturned = upload_duel_officer_name_fields(state, entered)\nreturn DuelGlyphContext(returned.target_x, returned.target_y, returned.count)"}, 'upload_duel_glyph_strip': {'signature': 'state: SceneState, source: Cursor, colors: DuelGlyphContext, current: DuelInitializationResult | None=None', 'returns': 'DuelGlyphContext | DuelInitializationResult', 'flow': "_live_cursor(state, source)\ncolors.validate()\nentered = _duel_scene_legacy_context_fields(state, current, 163158, 'upload_duel_glyph_strip_fields')\nreturned = upload_duel_glyph_strip_fields(state, entered)\nreturn DuelGlyphContext(returned.target_x, returned.target_y, returned.count)"}, '_expand_and_upload_duel_glyphs': {'signature': 'state, source, destination, colors, current=None', 'returns': None, 'flow': "_live_cursor(state, source)\n_live_cursor(state, destination)\ncolors.validate()\nentered = _duel_scene_legacy_context_fields(state, current, 163162, '_upload_duel_glyph_buffers_fields')\nreturned = _upload_duel_glyph_buffers_fields(state, entered)\nreturn DuelGlyphContext(returned.target_x, returned.target_y, returned.count)"}, 'clear_duel_text_plane': {'signature': 'state: SceneState, frame: DuelActorFrame | None=None', 'returns': 'DuelActorFrame | None', 'flow': "entered = FirstDeploymentFrame.unobserved()\nif frame is not None:\n    if type(frame) is not DuelActorFrame:\n        raise ValueError('actual clear-text frame required')\n    frame.validate()\n    entered = first_replace(entered, target_x=frame.command, target_y=frame.comparison, unit=frame.distance, count=frame.factor, distance=frame.weapon_difference, offset_x=frame.working_value, offset_y=frame.response, choice=frame.variation)\nreturned = clear_duel_text_plane_fields(state, entered)\nreturn None if frame is None else _duel_strategy_actor_values(returned)"}, 'decode_duel_byte_lanes': {'signature': 'state: SceneState, source: Cursor, destination: Cursor, length: Word, repeat_value: Long=0, pair_value: Long=0, *, length_carrier: Long | None=None, count_carrier: Long | None=None, stack: Cursor | None=None', 'returns': 'DuelLaneResult', 'flow': 'entered = _duel_lane_legacy_fields(state, source, destination, length, repeat_value, pair_value, length_carrier, count_carrier, stack, 163858)\nreturn _duel_lane_fields_to_observations(decode_duel_byte_lanes_fields(state, entered))'}, 'decode_duel_byte_lane': {'signature': 'state: SceneState, source: Cursor, destination: Cursor, length: Word, repeat_value: Long=0, pair_value: Long=0, *, length_carrier: Long | None=None, count_carrier: Long | None=None', 'returns': 'DuelLaneResult', 'flow': 'entered = _duel_lane_legacy_fields(state, source, destination, length, repeat_value, pair_value, length_carrier, count_carrier, None, 163870)\nreturn _duel_lane_fields_to_observations(decode_duel_byte_lane_fields(state, entered))'}, 'advance_duel_entry_palette_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 159110)\nstep = state.read(16740600, 2)\nframe = _movement_compare(state, frame, step, 16, 16)\nif not frame.status & 1:\n    return frame\nframe = _movement_move(state, frame, 'target_x', 15, 16)\nframe = _duel_commit_sub_word_fields(state, frame, 'target_x', state.read(16740600, 2))\nframe = _movement_move(state, frame, 'target_y', 64, 16)\nframe = first_replace(frame, roster=state.table_at(163968).cursor())\nframe = _duel_scene_call_fields(state, frame, 56998, 159148)\nframe, next_step = _movement_binary_flags(state, frame, state.read(16740600, 2), 1, 16)\nstate.write(16740600, 2, next_step)\nreturn frame"}, 'upload_duel_officer_name_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 163100)\nframe = _movement_multiply_word(state, frame, 'choice', 6)\nframe = first_replace(frame, roster=state.table_at(566532).cursor())\nframe = first_replace(frame, roster=frame.roster.at(low16(frame.choice)))\nframe = _movement_move(state, frame, 'count', 2, 16)\nframe = _movement_compare(state, frame, frame.roster.word(4), 63, 16)\nif not frame.status & 4:\n    return upload_duel_glyph_strip_fields(state, frame)\nframe = _movement_move(state, frame, 'count', 1, 16)\nframe = _movement_move(state, frame, 'distance', low16(frame.target_x), 16)\nframe = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'distance', low16(frame.distance), 4)\nframe = _movement_move(state, frame, 'distance', low16(frame.distance) | low16(frame.target_x), 16)\nframe = _movement_move(state, frame, 'offset_x', 63, 16)\nframe = first_replace(frame, candidates=state.table_at(4294955776).cursor(), controller=state.table_at(4294956096).cursor())\nwhile True:\n    frame = _duel_actor_store_fields(state, frame, frame.candidates, 0, low8(frame.distance), 8)\n    frame = first_replace(frame, candidates=frame.candidates.advance(1))\n    frame = _duel_actor_store_fields(state, frame, frame.controller, 0, low8(frame.distance), 8)\n    frame = first_replace(frame, controller=frame.controller.advance(1))\n    remaining = u16(low16(frame.offset_x) - 1)\n    frame = first_replace(frame, offset_x=replace_word(frame.offset_x, remaining))\n    if remaining == 65535:\n        return _upload_duel_glyph_buffers_fields(state, frame)"}, 'upload_duel_glyph_strip_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _resource_cost_frame(state, frame, 163158)\nframe = first_replace(frame, candidates=state.table_at(4294955776).cursor())\nreturn _upload_duel_glyph_buffers_fields(state, frame)'}, '_upload_duel_glyph_buffers_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _duel_scene_call_fields(state, frame, 44682, 163168)\nframe = first_replace(frame, roster=state.table_at(4294955776).cursor(), auxiliary=state.table_at(12582912))\nframe = _movement_move(state, frame, 'target_x', 95, 16)\nwhile True:\n    value = frame.roster.long(0)\n    frame = first_replace(frame, roster=frame.roster.advance(4))\n    frame = _duel_actor_store_fields(state, frame, frame.auxiliary, 0, value, 32)\n    remaining = u16(low16(frame.target_x) - 1)\n    frame = first_replace(frame, target_x=replace_word(frame.target_x, remaining))\n    if remaining == 65535:\n        return frame"}, 'clear_duel_text_plane_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 163190)\nframe = _duel_scene_store_fields(state, frame, 4294955264, 0, clear=True)\nframe = _duel_scene_store_fields(state, frame, 12582916, 1174405123, 32)\nframe = first_replace(frame, auxiliary=state.table_at(12582912))\nframe = _movement_move_long(state, frame, 'target_x', 286331153)\nframe = _movement_move(state, frame, 'target_y', 639, 16)\nwhile True:\n    frame = _duel_actor_store_fields(state, frame, frame.auxiliary, 0, frame.target_x, 32)\n    remaining = u16(low16(frame.target_y) - 1)\n    frame = first_replace(frame, target_y=replace_word(frame.target_y, remaining))\n    if remaining == 65535:\n        return frame"}, 'decode_duel_byte_lanes_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 163858)\nframe = _movement_save_longs(state, frame, ('target_x', 'candidates'))\nframe = _duel_scene_call_fields(state, frame, 163870, 163864)\nframe = _movement_restore_longs(state, frame, ('target_x', 'candidates'))\nframe = first_replace(frame, candidates=frame.candidates.advance(1))\nreturn decode_duel_byte_lane_fields(state, frame)"}, '_duel_lane_emit_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, value: Word', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _duel_actor_store_fields(state, frame, frame.candidates, 0, value, 8)\nreturn first_replace(frame, candidates=frame.candidates.advance(2))'}, 'decode_duel_byte_lane_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 163870)\nwhile True:\n    frame = _movement_test(state, frame, low16(frame.target_x), 16)\n    if frame.status & 4:\n        return frame\n    frame = _movement_move(state, frame, 'target_y', 0, 16)\n    token = frame.roster.byte(0)\n    frame = first_replace(frame, roster=frame.roster.advance(1))\n    frame = _movement_move(state, frame, 'target_y', token, 8)\n    if not frame.status & 8:\n        kind = 'literal'\n    else:\n        frame = _postbattle_bit_fields(frame, bool(frame.target_y & 64))\n        state.sr = state.sr & 65504 | frame.status\n        if frame.status & 4:\n            kind = 'repeat'\n            frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 63, 16)\n        else:\n            frame = _postbattle_bit_fields(frame, bool(frame.target_y & 32))\n            state.sr = state.sr & 65504 | frame.status\n            kind = 'pair' if frame.status & 4 else 'ascending'\n            frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 31, 16)\n        value = frame.roster.byte(0)\n        frame = first_replace(frame, roster=frame.roster.advance(1))\n        frame = _movement_move(state, frame, 'unit', value, 8)\n        if kind == 'pair':\n            value = frame.roster.byte(0)\n            frame = first_replace(frame, roster=frame.roster.advance(1))\n            frame = _movement_move(state, frame, 'count', value, 8)\n    while True:\n        if kind == 'literal':\n            value = frame.roster.byte(0)\n            frame = first_replace(frame, roster=frame.roster.advance(1))\n            frame = _duel_lane_emit_fields(state, frame, value)\n        else:\n            frame = _duel_lane_emit_fields(state, frame, low8(frame.unit))\n            if kind == 'pair':\n                frame = _duel_lane_emit_fields(state, frame, low8(frame.count))\n        frame, remaining = _movement_binary_flags(state, frame, low16(frame.target_x), 2 if kind == 'pair' else 1, 16, True)\n        frame = first_replace(frame, target_x=replace_word(frame.target_x, remaining))\n        if kind == 'ascending':\n            frame = _movement_add_word(state, frame, 'unit', 1)\n        count = u16(low16(frame.target_y) - 1)\n        frame = first_replace(frame, target_y=replace_word(frame.target_y, count))\n        if count == 65535:\n            break"}, '_duel_lane_legacy_fields': {'signature': 'state: SceneState, source: Cursor, destination: Cursor, length: Word, repeat_value: Long, pair_value: Long, length_carrier: Long | None, count_carrier: Long | None, stack: Cursor | None, target: Long', 'returns': 'FirstDeploymentFrame', 'flow': "source = _live_cursor(state, source)\ndestination = _live_cursor(state, destination)\nlength = uint(length, 16, 'length')\nrepeat_value = uint(repeat_value, 32, 'repeat value')\npair_value = uint(pair_value, 32, 'pair value')\nif length_carrier is not None:\n    uint(length_carrier, 32)\n    if low16(length_carrier) != length:\n        raise ValueError('lane length must agree with actual caller')\nif count_carrier is not None:\n    uint(count_carrier, 32)\nif stack is not None:\n    stack = _live_cursor(state, stack)\nentered = first_replace(FirstDeploymentFrame.unobserved(), target_x=length_carrier, target_y=count_carrier, unit=repeat_value, count=pair_value, roster=source, candidates=destination, stack_cursor=stack)\nentered.validate(state, False)\nraise MovementContinuationBoundary(target, entered, 'legacy lane observations omit live D4-D7/A2-A6 and CCR/X; use the full lane core')"}, '_duel_lane_fields_to_observations': {'signature': 'frame: FirstDeploymentFrame', 'returns': 'DuelLaneResult', 'flow': 'return DuelLaneResult(frame.roster, frame.candidates, low16(frame.target_x), frame.unit, frame.count, frame.target_x, frame.target_y)'}, '_duel_scene_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "if target == 33748:\n    return sample_battle_action_random_fields(BattlePolicyMemory(state), frame, continuation)\n\ndef child(memory, entered):\n    if target in (162278, 162320):\n        from .business_reuse import choose_first_duel_control_fields, choose_second_duel_control_fields\n        return choose_second_duel_control_fields(state, entered) if target == 162320 else choose_first_duel_control_fields(state, entered)\n    if target == 159110:\n        return advance_duel_entry_palette_fields(state, entered)\n    if target == 163100:\n        return upload_duel_officer_name_fields(state, entered)\n    if target == 163158:\n        return upload_duel_glyph_strip_fields(state, entered)\n    if target == 163190:\n        return clear_duel_text_plane_fields(state, entered)\n    if target == 163858:\n        return decode_duel_byte_lanes_fields(state, entered)\n    if target == 163870:\n        return decode_duel_byte_lane_fields(state, entered)\n    if target == 44682:\n        from .business_scene import decode_glyph_rows_to_buffers_fields\n        return decode_glyph_rows_to_buffers_fields(SceneRefreshMemory(state), entered)\n    if target == 163228:\n        return choose_duel_two_option_menu_fields(state, entered)\n    if target == 163324:\n        return choose_first_duel_equipment_fields(state, entered)\n    if target == 163334:\n        return choose_second_duel_equipment_fields(state, entered)\n    if target == 163538:\n        return choose_duel_action_menu_fields(state, entered)\n    if target == 162362:\n        return configure_duel_weapon_motion_fields(state, entered)\n    if target == 162436:\n        return refresh_duel_actors_fields(state, entered)\n    if target == 166810:\n        return update_duel_actor_fields(state, entered)\n    if target == 172698:\n        return choose_duel_ai_command_fields(state, entered)\n    if target == 167824:\n        return scan_duel_thresholds_fields(state, entered)\n    if target == 161030:\n        return show_active_duel_turn_label_fields(state, entered)\n    if target == 161658:\n        return wait_active_duel_action_fields(state, entered)\n    if target == 161720:\n        return wait_either_duel_action_fields(state, entered)\n    if target == 164392:\n        return choose_duel_status_text_fields(state, entered)\n    if target == 32906:\n        return enqueue_sound_command_fields(SceneRefreshMemory(state), entered, low8(entered.target_x))\n    if target == 158714:\n        from ..high_level_gameplay_flow.business_services import stage_sprite_word_packet_fields\n        return stage_sprite_word_packet_fields(SceneRefreshMemory(state), entered)\n    if target == 44830:\n        from .business_scene import expand_glyph_stream_fields\n        return expand_glyph_stream_fields(SceneRefreshMemory(state), entered)\n    if target == 26830:\n        from ..high_level_gameplay_flow.business_services import clear_video_sprite_plane_fields\n        return clear_video_sprite_plane_fields(SceneRefreshMemory(state), entered)\n    if target == 56998:\n        from .business_scene import darken_palette_fields\n        return darken_palette_fields(SceneRefreshMemory(state), entered)\n    raise MovementContinuationBoundary(target, entered, 'actual duel controller child lacks a complete current-frame ABI')\nreturn _presentation_call_fields(BattlePresentationMemory(state), frame, continuation, child)"}}
for _name, _shape in DUEL_CHILDREN_FIELDS_DECLARATIONS.items():
    _old = DECLARATIONS.get(_name, {})
    DECLARATIONS[_name] = dict(_old, **_shape)
APPROVED.setdefault('business_scene', set()).add('decode_glyph_rows_to_buffers_fields')

DECLARATIONS.update({'_duel_scene_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "if target == 33748:\n    return sample_battle_action_random_fields(BattlePolicyMemory(state), frame, continuation)\ndef child(memory, entered):\n    if target in (162278, 162320):\n        from .business_reuse import choose_first_duel_control_fields, choose_second_duel_control_fields\n        return choose_second_duel_control_fields(state, entered) if target == 162320 else choose_first_duel_control_fields(state, entered)\n    if target == 159110:\n        return advance_duel_entry_palette_fields(state, entered)\n    if target == 163100:\n        return upload_duel_officer_name_fields(state, entered)\n    if target == 163158:\n        return upload_duel_glyph_strip_fields(state, entered)\n    if target == 163190:\n        return clear_duel_text_plane_fields(state, entered)\n    if target == 163858:\n        return decode_duel_byte_lanes_fields(state, entered)\n    if target == 163870:\n        return decode_duel_byte_lane_fields(state, entered)\n    if target == 44682:\n        from .business_scene import decode_glyph_rows_to_buffers_fields\n        return decode_glyph_rows_to_buffers_fields(SceneRefreshMemory(state), entered)\n    if target == 163228:\n        return choose_duel_two_option_menu_fields(state, entered)\n    if target == 163324:\n        return choose_first_duel_equipment_fields(state, entered)\n    if target == 163334:\n        return choose_second_duel_equipment_fields(state, entered)\n    if target == 163538:\n        return choose_duel_action_menu_fields(state, entered)\n    if target == 162362:\n        return configure_duel_weapon_motion_fields(state, entered)\n    if target == 162436:\n        return refresh_duel_actors_fields(state, entered)\n    if target == 166810:\n        return update_duel_actor_fields(state, entered)\n    if target == 172698:\n        return choose_duel_ai_command_fields(state, entered)\n    if target == 167824:\n        return scan_duel_thresholds_fields(state, entered)\n    if target == 161030:\n        return show_active_duel_turn_label_fields(state, entered)\n    if target == 161658:\n        return wait_active_duel_action_fields(state, entered)\n    if target == 161720:\n        return wait_either_duel_action_fields(state, entered)\n    if target == 164392:\n        return choose_duel_status_text_fields(state, entered)\n    if target == 32906:\n        return enqueue_sound_command_fields(SceneRefreshMemory(state), entered, low8(entered.target_x))\n    if target == 158714:\n        from ..high_level_gameplay_flow.business_services import stage_sprite_word_packet_fields\n        return stage_sprite_word_packet_fields(SceneRefreshMemory(state), entered)\n    if target == 44830:\n        from .business_scene import expand_glyph_stream_fields\n        return expand_glyph_stream_fields(SceneRefreshMemory(state), entered)\n    if target == 26830:\n        from ..high_level_gameplay_flow.business_services import clear_video_sprite_plane_fields\n        return clear_video_sprite_plane_fields(SceneRefreshMemory(state), entered)\n    if target == 44294:\n        from .business_scene import flush_scene_transfer_queue_fields\n        return flush_scene_transfer_queue_fields(SceneRefreshMemory(state), entered)\n    if target == 56998:\n        from .business_scene import darken_palette_fields\n        return darken_palette_fields(SceneRefreshMemory(state), entered)\n    if target in (162764, 162850, 162954, 162980, 163026, 163068) and continuation == 162686:\n        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_92_fields\n        return highbank_coordinate_live_state_92_fields(state, entered, target)\n    raise MovementContinuationBoundary(target, entered, 'actual duel controller child lacks a complete current-frame ABI')\nreturn _presentation_call_fields(BattlePresentationMemory(state), frame, continuation, child)"}})

DECLARATIONS.update({'run_duel_scene_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 159156)\nframe = initialize_duel_scene_fields(state, frame)\nsecond = False\nwhile True:\n    committed_second, frame = prepare_duel_loadout_fields(state, frame, second)\n    if committed_second:\n        break\n    second = True\nframe = prepare_duel_readiness_fields(state, frame)\nclear_text = True\nwhile True:\n    phase, frame = begin_duel_combat_fields(state, frame, clear_text)\n    if phase == 'terminal':\n        frame = show_terminal_duel_result_fields(state, frame)\n        return finish_duel_scene_fields(state, frame)\n    if phase == 'action':\n        phase, frame = choose_duel_turn_action_fields(state, frame)\n        if phase == 'submit':\n            phase, frame = perform_selected_duel_action_result_fields(state, frame)\n            if phase == 'fade':\n                return finish_duel_scene_fields(state, frame)\n    clear_text = phase == 'next_frame_clear'"}})

DECLARATIONS.update({'perform_selected_duel_action_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "phase, returned = perform_selected_duel_action_result_fields(state, frame)\nif phase != 'next_frame_clear':\n    raise MovementContinuationBoundary(159046, returned, 'nonlocal original action uses perform_selected_duel_action_result_fields')\nreturn returned"}})

DECLARATIONS.update({'_duel_scene_indexed_action_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int', 'returns': 'tuple[str, FirstDeploymentFrame]', 'flow': "stack = frame.stack_cursor.advance(-4)\nstack.set_long(0, 161138)\nentered = first_replace(frame, stack_cursor=stack)\nfrom ..high_level_dynamic_flows.business_duel import execute_indexed_duel_action_fields\nphase, returned = execute_indexed_duel_action_fields(state, entered, target)\nif phase == 'fade':\n    return (phase, returned)\nif phase != 'return':\n    raise ValueError('actual ordinary or fixed-fade action result required')\nactual = returned.stack_cursor.long(0)\nreturned = first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))\nif actual != 161138:\n    raise MovementContinuationBoundary(actual, returned, 'actual action RTS reaches an unowned return address')\nreturn ('next_frame_clear', returned)"}})

DECLARATIONS.update({'perform_selected_duel_action_result_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'tuple[str, FirstDeploymentFrame]', 'flow': "frame = _resource_cost_frame(state, frame, 161076)\nframe = _movement_move(state, frame, 'target_x', 172, 16)\nframe = _duel_scene_call_fields(state, frame, 32906, 161086)\nframe = _duel_scene_status_fields(state, frame, 9984)\nframe = _duel_scene_call_fields(state, frame, 163190, 161094)\nframe = first_replace(frame, roster=state.table_at(16740432).cursor(), candidates=state.table_at(16740512).cursor())\nframe = _movement_test(state, frame, state.read(16740376, 2), 16)\nif frame.status & 8:\n    frame = first_replace(frame, roster=state.table_at(16740512).cursor(), candidates=state.table_at(16740432).cursor())\nframe = _movement_move(state, frame, 'target_x', state.read(16740376, 2), 16)\nframe = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_x', low16(frame.target_x), 2)\ntarget = u32(161142 + s16(low16(frame.target_x)))\nreturn _duel_scene_indexed_action_fields(state, frame, target)"}})

APPROVED.setdefault('business_duel',set()).add('execute_indexed_duel_action_fields')
APPROVED.setdefault('business_scene',set()).add('flush_scene_transfer_queue_fields')

APPROVED.setdefault((2, 'high_level_battle_ai.business_actions'),set()).update(['sample_battle_action_random_fields'])

APPROVED.setdefault((2, 'high_level_battle_ai.contexts_policy_memory'),set()).update(['BattlePolicyMemory'])

APPROVED.setdefault((2, 'high_level_dynamic_flows.business_duel'),set()).update(['choose_duel_profile_fields', 'execute_duel_rule_fields', 'execute_indexed_duel_action_fields'])

APPROVED.setdefault((2, 'high_level_gameplay_flow.business_battle'),set()).update(['_postbattle_bit_fields', '_presentation_call_fields'])

APPROVED.setdefault((2, 'high_level_gameplay_flow.business_services'),set()).update(['clear_video_sprite_plane_fields', 'enqueue_sound_command_fields', 'stage_sprite_word_packet_fields'])

APPROVED.setdefault((2, 'high_level_gameplay_flow.contexts_battle'),set()).update(['BattlePresentationMemory'])

APPROVED.setdefault((2, 'high_level_main_flows.business_movement_support'),set()).update(['_movement_add_byte', '_movement_add_word', '_movement_binary_flags', '_movement_compare', '_movement_compare_address', '_movement_divu_word', '_movement_fixed_shift_word', '_movement_move', '_movement_move_long', '_movement_multiply_word', '_movement_restore_longs', '_movement_save_longs', '_movement_test', '_movement_test_long'])

APPROVED.setdefault((2, 'high_level_main_flows.contexts_gameplay'),set()).update(['MovementContinuationBoundary'])

APPROVED.setdefault((2, 'high_level_remaining_flows.business_city'),set()).update(['_duel_commit_sub_word_fields', '_duel_velocity_asr_fields', '_resource_cost_frame'])

APPROVED.setdefault((2, 'high_level_scene_flows.domain'),set()).update(['s8'])


# Duel3306 real live BYTE polling118; ordinary guards/lowerers and all other phase bodies retained.
DECLARATIONS['_duel_scene_frame_ack_fields'] = {'signature': 'state: SceneState, frame: FirstDeploymentFrame, poll: int, arm: bool=True', 'returns': 'FirstDeploymentFrame', 'flow': "if type(arm) is not bool:\n    raise ValueError('actual entry/resume poll role required')\nif arm:\n    frame = _duel_scene_store_fields(state, frame, 4294964754, 1792)\nwhile True:\n    frame = _movement_test(state, frame, state.read(4294964754, 1), 8)\n    if frame.status & 4:\n        return frame\n    try:\n        state.progress('duel-scene-frame-byte-ack')\n    except Boundary:\n        raise MovementContinuationBoundary(poll, frame, 'actual duel frame BYTE ACK requires external IRQ progress')"}

# B167: exact original six-entry duel CALL dependency; no wider imports.
APPROVED[(2, 'high_level_remaining_flows.business_highbank')] = {'highbank_coordinate_live_state_92_fields'}
