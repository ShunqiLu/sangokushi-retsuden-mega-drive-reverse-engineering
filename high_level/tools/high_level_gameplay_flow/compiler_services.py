"""Restricted services structural source admission and ordinary mnemonic lowering.

Explicit semantic input only; no original ROM/ASM/IR/object input or opaque
opcode payload. Fixed original layout; unsupported source changes are rejected.
Actual service/IRQ and CPU behavior are not supplied by this finite compiler.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import SERVICES_BINDINGS

APPROVED = {'business_battle': {'upload_battle_scene_labels'},
 'contexts_battle': {'BattleSceneContext'},
 'contexts_services': {'GlyphColors',
                       'GlyphStreamResult',
                       'SceneDisplayContext',
                       'SceneDisplayResult',
                       'SpriteControlContext',
                       'SpriteControlResult',
                       'TransferResult'},
 'domain': {'Boundary',
            'Byte',
            'Cursor',
            'GameplayState',
            'Long',
            'Table',
            'Word',
            'checked_cursor',
            'checked_state',
            'descending_inclusive',
            'low16',
            'low8',
            'negative_word',
            'replace_word',
            's16',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'}}

# Exact cross-domain imports used by the full-field service implementations.
# Keep the compiler's relative-level and no-alias admission rules unchanged.
APPROVED.setdefault((2,'high_level_scene_flows.business_scene'),set()).update({
    'expand_glyph_row_fields','expand_glyph_stream_fields','play_scripted_scene_fields'})
APPROVED.setdefault((2,'high_level_scene_flows.domain'),set()).update({'SceneState'})
APPROVED.setdefault((2,'high_level_main_flows.business_movement_support'),set()).update({
    '_movement_binary_flags','_movement_save_longs','_movement_restore_longs'})
APPROVED.setdefault((2,'high_level_battle_ai.business_formation'),set()).update({
    '_first_sub_word','_first_add_word','_first_memory_word','_first_right_word'})
APPROVED.setdefault((2,'high_level_player_commands.business_budget'),set()).update({'_six_place_decimal_fields'})
APPROVED.setdefault((2,'high_level_player_commands.contexts_numeric'),set()).update({'DecimalMemory'})

DECLARATIONS = {'_control': {'signature': 'state, size, value',
              'returns': None,
              'flow': 'state.write(12582916, size, value)'},
 '_pixels': {'signature': 'state, size, value',
             'returns': None,
             'flow': 'state.write(12582912, size, value)'},
 '_wait_dma': {'signature': 'state',
               'returns': None,
               'flow': "while state.read(12582916, 2) & 2:\n    state.progress('vdp-dma')"},
 '_release_sound_bus_if_allowed': {'signature': 'state',
                                   'returns': None,
                                   'flow': 'if state.read(16727808, 1) == 0:\n'
                                           '    state.write(10555648, 2, 0)'},
 'clear_scene_video_and_state': {'signature': 'state: GameplayState',
                                 'returns': 'None',
                                 'flow': 'checked_state(state)\n'
                                         'state.set_status_word(9984)\n'
                                         'pattern = select_scene_fill_pattern(state)\n'
                                         'state.write(4294964094, 2, 0)\n'
                                         '_control(state, 4, 1621098498)\n'
                                         'for _ in descending_inclusive(1439):\n'
                                         '    _pixels(state, 4, pattern)\n'
                                         'if state.read(4294964932, 2) == 0:\n'
                                         '    _control(state, 4, 1879048193)\n'
                                         '    source = state.table(564700).cursor()\n'
                                         '    for _ in descending_inclusive(23):\n'
                                         '        _pixels(state, 4, source.next_long())\n'
                                         '    source = state.table(565372).cursor()\n'
                                         '    for _ in descending_inclusive(15):\n'
                                         '        _pixels(state, 4, source.next_long())\n'
                                         'pattern = select_scene_fill_pattern(state)\n'
                                         'destination = state.table(4294964502).cursor()\n'
                                         'for _ in descending_inclusive(23):\n'
                                         '    destination.append_long(pattern)\n'
                                         'state.write(4294964090, 2, 0)\n'
                                         'state.write(4294964092, 2, 0)\n'
                                         'refresh_gameplay_scene(state)'},
 'select_scene_fill_pattern': {'signature': 'state: GameplayState',
                               'returns': 'Long',
                               'flow': 'checked_state(state)\n'
                                       'index = u16(state.read(4294964932, 2) << 2)\n'
                                       'return state.table(1686).long(index)'},
 'reset_scene_input_markers': {'signature': 'state: GameplayState',
                               'returns': 'None',
                               'flow': 'checked_state(state)\n'
                                       'for address in (4294963968, 4294965248, 4294965250, '
                                       '4294965254):\n'
                                       '    state.write(address, 2, 0)'},
 'initialize_video_registers_and_planes': {'signature': 'state: GameplayState',
                                           'returns': 'None',
                                           'flow': 'checked_state(state)\n'
                                                   'registers = state.table(26792).cursor()\n'
                                                   'for _ in descending_inclusive(18):\n'
                                                   '    _control(state, 2, registers.next_word())\n'
                                                   'state.write(4294964742, 2, state.read(26794, '
                                                   '2))\n'
                                                   '_control(state, 4, 3221225472)\n'
                                                   'for _ in descending_inclusive(63):\n'
                                                   '    _pixels(state, 2, 0)\n'
                                                   '_control(state, 2, 36609)\n'
                                                   '_control(state, 2, state.read(4294964742, 2) | '
                                                   '16)\n'
                                                   '_control(state, 4, 2483000575)\n'
                                                   '_control(state, 2, 38784)\n'
                                                   '_control(state, 4, 1073741952)\n'
                                                   '_pixels(state, 2, 0)\n'
                                                   '_wait_dma(state)\n'
                                                   '_release_sound_bus_if_allowed(state)\n'
                                                   '_control(state, 2, state.read(4294964742, 2))\n'
                                                   '_control(state, 2, 36610)'},
 'clear_video_sprite_plane': {'signature': 'state: GameplayState',
                              'returns': 'None',
                              'flow': 'checked_state(state)\n'
                                      '_control(state, 2, 36609)\n'
                                      '_control(state, 2, state.read(4294964742, 2) | 16)\n'
                                      '_control(state, 4, 2483000391)\n'
                                      '_control(state, 2, 38784)\n'
                                      '_control(state, 4, 2013266050)\n'
                                      '_pixels(state, 2, 246)\n'
                                      '_wait_dma(state)\n'
                                      '_release_sound_bus_if_allowed(state)\n'
                                      '_control(state, 2, state.read(4294964742, 2))\n'
                                      '_control(state, 2, 36610)\n'
                                      '_control(state, 4, 1073741840)\n'
                                      '_pixels(state, 4, 0)\n'
                                      'state.write(4294963986, 4, 0)\n'
                                      'state.write(4294963990, 4, 0)\n'
                                      'destination = state.table(4294965248).cursor()\n'
                                      'for _ in descending_inclusive(159):\n'
                                      '    destination.append_long(0)'},
 'enqueue_sound_command': {'signature': 'state: GameplayState, command: Byte',
                           'returns': 'None',
                           'flow': 'checked_state(state)\n'
                                   'uint(command, 8)\n'
                                   'state.write(16727808, 1, 255)\n'
                                   'state.write(10555648, 2, 256)\n'
                                   'while state.read(10555648, 1) & 1:\n'
                                   "    state.progress('sound-bus-acquire')\n"
                                   'if state.read(10492938, 1) == 0:\n'
                                   '    state.write(10492938, 1, command)\n'
                                   'elif state.read(10492939, 1) == 0:\n'
                                   '    state.write(10492939, 1, command)\n'
                                   'state.write(16727808, 1, 0)\n'
                                   'state.write(10555648, 2, 0)'},
 'copy_video_transfer_descriptor': {'signature': 'state: GameplayState, index: Word',
                                    'returns': 'TransferResult',
                                    'flow': 'checked_state(state)\n'
                                            'uint(index, 16)\n'
                                            'descriptor = state.table(33068).cursor(u16(index << '
                                            '3))\n'
                                            'source = '
                                            'state.table(descriptor.next_long()).cursor()\n'
                                            'destination = '
                                            'state.table(u32(s16(descriptor.next_word()))).cursor()\n'
                                            'remaining = descriptor.next_word()\n'
                                            'for _ in descending_inclusive(remaining):\n'
                                            '    destination.append_long(source.next_long())\n'
                                            'state.write(4294963998, 2, u16(state.read(4294963998, '
                                            '2) + 1))\n'
                                            'return TransferResult(source, destination)'},
 'wait_for_scene_sound_byte': {'signature': 'state: GameplayState',
                               'returns': 'None',
                               'flow': 'checked_state(state)\n'
                                       'state.set_status_word(9472)\n'
                                       'while state.read(4294964754, 1) != 0:\n'
                                       "    state.progress('scene-sound-byte')"},
 'expand_glyph_row': {'signature': 'state: GameplayState, source: Cursor, background: Byte, '
                                   'foreground: Byte',
                      'returns': 'Long',
                      'flow': 'checked_state(state)\n'
                              'checked_cursor(source, state)\n'
                              'uint(background, 8)\n'
                              'uint(foreground, 8)\n'
                              'bits = source.next_byte()\n'
                              'pixels = 0\n'
                              'for bit in range(7, -1, -1):\n'
                              '    pixels = u32(pixels << 4)\n'
                              '    pixels |= foreground if bits & 1 << bit else background\n'
                              'return pixels'},
 'expand_glyph_stream': {'signature': 'state: GameplayState, tokens: Cursor, destination: Cursor, '
                                      'colors: GlyphColors, remaining: Long',
                         'returns': 'GlyphStreamResult',
                         'flow': 'checked_state(state)\n'
                                 'checked_cursor(tokens, state)\n'
                                 'checked_cursor(destination, state)\n'
                                 'if type(colors) is not GlyphColors:\n'
                                 "    raise ValueError('explicit glyph colors required')\n"
                                 'colors.__post_init__()\n'
                                 'uint(remaining, 32)\n'
                                 'for _ in descending_inclusive(low16(remaining)):\n'
                                 '    glyph = u16(tokens.next_byte() << 3)\n'
                                 '    source = state.table(562908).cursor(glyph)\n'
                                 '    for _ in descending_inclusive(7):\n'
                                 '        destination.append_long(expand_glyph_row(state, source, '
                                 'low8(colors.background), low8(colors.foreground)))\n'
                                 'return GlyphStreamResult(tokens, destination, '
                                 'replace_word(remaining, 65535))'},
 'refresh_gameplay_scene': {'signature': 'state: GameplayState, retained: Long=0',
                            'returns': 'Long',
                            'flow': 'checked_state(state)\n'
                                    'uint(retained, 32)\n'
                                    'while True:\n'
                                    '    retained = replace_word(retained, state.read(12582916, '
                                    '2))\n'
                                    '    if not retained & 8:\n'
                                    '        break\n'
                                    "    state.progress('vblank-end')\n"
                                    'while True:\n'
                                    '    retained = replace_word(retained, state.read(12582916, '
                                    '2))\n'
                                    '    if retained & 8:\n'
                                    '        return retained\n'
                                    "    state.progress('vblank-start')"},
 'load_gameplay_scene': {'signature': 'state: GameplayState',
                         'returns': 'None',
                         'flow': 'checked_state(state)\n'
                                 'if state.read(4294963158, 2) == 0:\n'
                                 '    saved_sound = state.read(4294964754, 2)\n'
                                 '    state.write(4294964133, 1, state.read(4294964133, 1) & 251)\n'
                                 '    reset_scene_input_markers(state)\n'
                                 '    state.write(4294964754, 2, 2304)\n'
                                 '    refresh_gameplay_scene(state)\n'
                                 '    wait_for_scene_sound_byte(state)\n'
                                 '    state.set_status_word(9984)\n'
                                 '    select_sound_command_from_scene(state)\n'
                                 '    _control(state, 4, 1082392579)\n'
                                 '    for _ in descending_inclusive(5):\n'
                                 '        _pixels(state, 4, 0)\n'
                                 '    draw_overlay_frame(state)\n'
                                 '    scene = state.service_at(235162, SceneDisplayContext())\n'
                                 '    if type(scene) is not SceneDisplayResult:\n'
                                 "        raise Boundary('real scene service must supply its "
                                 "retained output carriers')\n"
                                 '    scene.__post_init__()\n'
                                 '    state.set_status_word(9984)\n'
                                 '    background = clear_overlay_frame(state)\n'
                                 '    state.write(16740390, 2, 65535)\n'
                                 '    _control(state, 4, 1075838976)\n'
                                 '    for _ in descending_inclusive(7):\n'
                                 '        _pixels(state, 4, 286331153)\n'
                                 '    state.write(4294964094, 2, 0)\n'
                                 '    state.write(4294964754, 2, saved_sound)\n'
                                 '    state.write(4294964132, 1, state.read(4294964132, 1) & 247)\n'
                                 '    state.write(4294963144, 4, 0)\n'
                                 '    state.write(4294963148, 4, 0)\n'
                                 '    _control(state, 4, 2013265922)\n'
                                 '    _pixels(state, 4, 0)\n'
                                 '    _pixels(state, 4, 0)\n'
                                 '    background = resume_pending_sound(state, background)\n'
                                 '    if state.read(4294964932, 2) == 1:\n'
                                 '        from .business_battle import upload_battle_scene_labels\n'
                                 '        from .contexts_battle import BattleSceneContext\n'
                                 '        upload_battle_scene_labels(state, '
                                 'BattleSceneContext(background, replace_word(scene.foreground, '
                                 '65535), scene.glyph_count, replace_word(scene.training_carrier, '
                                 '65535)))\n'
                                 '    return\n'
                                 'state.write(16740390, 2, 65535)'},
 'select_sound_command_from_scene': {'signature': 'state: GameplayState',
                                     'returns': 'Word',
                                     'flow': 'checked_state(state)\n'
                                             'offset = u16(state.read(16740390, 2) << 1)\n'
                                             'command = state.table(67632).word(offset)\n'
                                             'state.write(4294963152, 2, command)\n'
                                             'if not negative_word(command):\n'
                                             '    enqueue_sound_command(state, low8(command))\n'
                                             'return command'},
 'resume_pending_sound': {'signature': 'state: GameplayState, retained: Long=0',
                          'returns': 'Long',
                          'flow': 'checked_state(state)\n'
                                  'uint(retained, 32)\n'
                                  'if not negative_word(state.read(4294963152, 2)):\n'
                                  '    retained = replace_word(retained, state.read(4294965092, '
                                  '1))\n'
                                  '    enqueue_sound_command(state, low8(retained))\n'
                                  'return retained'},
 'draw_overlay_frame': {'signature': 'state: GameplayState',
                        'returns': 'None',
                        'flow': 'checked_state(state)\n'
                                '_control(state, 4, 1912602625)\n'
                                'for _ in descending_inclusive(7):\n'
                                '    _pixels(state, 4, 858993459)\n'
                                'source = state.table(565436).cursor()\n'
                                'for _ in descending_inclusive(63):\n'
                                '    _pixels(state, 4, source.next_long())\n'
                                'command = draw_overlay_frame_header(state, 1090781187)\n'
                                'for _ in descending_inclusive(9):\n'
                                '    command = draw_overlay_frame_middle(state, command)\n'
                                'draw_overlay_frame_footer(state, command)'},
 'draw_overlay_frame_header': {'signature': 'state: GameplayState, command: Long',
                               'returns': 'Long',
                               'flow': 'checked_state(state)\n'
                                       'uint(command, 32)\n'
                                       '_control(state, 4, command)\n'
                                       '_pixels(state, 2, 50065)\n'
                                       'for _ in descending_inclusive(8):\n'
                                       '    _pixels(state, 4, 3281175442)\n'
                                       '_pixels(state, 2, 52119)\n'
                                       'command = u32(command + 8388608)\n'
                                       '_control(state, 4, command)\n'
                                       '_pixels(state, 4, 3281240980)\n'
                                       'for _ in descending_inclusive(7):\n'
                                       '    _pixels(state, 4, 3281372053)\n'
                                       '_pixels(state, 4, 3415792531)\n'
                                       'return command'},
 'draw_overlay_frame_middle': {'signature': 'state: GameplayState, command: Long',
                               'returns': 'Long',
                               'flow': 'checked_state(state)\n'
                                       'uint(command, 32)\n'
                                       'command = u32(command + 8388608)\n'
                                       '_control(state, 4, command)\n'
                                       '_pixels(state, 4, 3281240982)\n'
                                       'for _ in descending_inclusive(7):\n'
                                       '    _pixels(state, 4, 1133527952)\n'
                                       '_pixels(state, 4, 3684096915)\n'
                                       'return command'},
 'draw_overlay_frame_footer': {'signature': 'state: GameplayState, command: Long',
                               'returns': 'Long',
                               'flow': 'checked_state(state)\n'
                                       'uint(command, 32)\n'
                                       'command = u32(command + 8388608)\n'
                                       '_control(state, 4, command)\n'
                                       '_pixels(state, 4, 3281245080)\n'
                                       'for _ in descending_inclusive(7):\n'
                                       '    _pixels(state, 4, 3684031381)\n'
                                       '_pixels(state, 4, 3683965843)\n'
                                       'command = u32(command + 8388608)\n'
                                       '_control(state, 4, command)\n'
                                       '_pixels(state, 4, 3549944722)\n'
                                       'for _ in descending_inclusive(7):\n'
                                       '    _pixels(state, 4, 3683834770)\n'
                                       '_pixels(state, 4, 3683834769)\n'
                                       'return command'},
 'clear_overlay_frame': {'signature': 'state: GameplayState',
                         'returns': 'Long',
                         'flow': 'checked_state(state)\n'
                                 'command = 1090781187\n'
                                 'for _ in descending_inclusive(13):\n'
                                 '    _control(state, 4, command)\n'
                                 '    for _ in descending_inclusive(9):\n'
                                 '        _pixels(state, 4, 0)\n'
                                 '    command = u32(command + 8388608)\n'
                                 'return command'},
 'stage_sprite_word_packet': {'signature': 'state: GameplayState, source: Cursor, command: Long, '
                                           'rows: Word, row_command: Word',
                              'returns': 'Long',
                              'flow': 'checked_state(state)\n'
                                      'checked_cursor(source, state)\n'
                                      'uint(command, 32)\n'
                                      'uint(rows, 16)\n'
                                      'uint(row_command, 16)\n'
                                      'destination = '
                                      'state.table(4294955264).cursor(state.read(4294963994, 2))\n'
                                      'for _ in descending_inclusive(u16(rows - 1)):\n'
                                      '    destination.append_word(low16(command))\n'
                                      '    destination.append_word(row_command)\n'
                                      '    row_command = u16(row_command + 128)\n'
                                      '    remaining = low16(command)\n'
                                      '    while True:\n'
                                      '        token = source.next_word()\n'
                                      '        if negative_word(token):\n'
                                      '            dispatch_offset = u16((token & 32767) >> 7) & '
                                      '65534\n'
                                      '            relative_target = '
                                      'state.table(158796).word(dispatch_offset)\n'
                                      '            target = u32(158808 + s16(relative_target))\n'
                                      '            result = state.service_at(target, '
                                      'SpriteControlContext(token, command, remaining, source, '
                                      'destination))\n'
                                      '            if type(result) is not SpriteControlResult:\n'
                                      "                raise ValueError('real sprite control "
                                      "result required')\n"
                                      '            result.__post_init__()\n'
                                      '            command, remaining = (result.command, '
                                      'result.row_remaining)\n'
                                      '        else:\n'
                                      '            command = swap_words(command)\n'
                                      '            destination.append_word(u16(token | '
                                      'low16(command)))\n'
                                      '            command = swap_words(command)\n'
                                      '            remaining = u16(remaining - 1)\n'
                                      '        if remaining == 0:\n'
                                      '            break\n'
                                      'destination.put_word(0)\n'
                                      'command = replace_word(command, u16(low16(command) + 2))\n'
                                      'allocated = u16(u16(low16(command) * rows) << 1)\n'
                                      'state.write(4294963994, 2, u16(state.read(4294963994, 2) + '
                                      'allocated))\n'
                                      'return replace_word(low16(command) * rows, allocated)'},
 'present_gameplay_message': {'signature': 'state: GameplayState',
                              'returns': 'None',
                              'flow': 'checked_state(state)\n'
                                      'saved_sound = state.read(4294964754, 2)\n'
                                      'saved_ui = state.read(4294964066, 2)\n'
                                      'state.write(4294964754, 2, 523)\n'
                                      'state.write(4294964736, 2, 0)\n'
                                      'refresh_gameplay_scene(state)\n'
                                      'state.set_status_word(9472)\n'
                                      'while True:\n'
                                      '    while state.read(4294964736, 2) == 0:\n'
                                      "        state.progress('message-scene')\n"
                                      '    if state.read(4294964736, 2) != 40:\n'
                                      '        break\n'
                                      '    clear_scene_video_and_state(state)\n'
                                      '    state.write(4294964736, 2, 0)\n'
                                      '    state.set_status_word(9472)\n'
                                      'state.set_status_word(9984)\n'
                                      'state.write(4294964066, 2, saved_ui)\n'
                                      'state.write(4294964754, 2, saved_sound)'}}

def _lower_clear_scene_video_and_state(e,rules):
    e.label('gameplay_pc_00060c')
    e.ins('move.w','#0x2700,%sr',4)
    e.label('gameplay_pc_000610')
    e.ins('bsr.w','gameplay_pc_00068a',4)
    e.label('gameplay_pc_000614')
    e.ins('clr.w','0xf37e:w',4)
    e.label('gameplay_pc_000618')
    e.ins('move.l','#0x60a00002,0xc00004:l',10)
    e.label('gameplay_pc_000622')
    e.ins('move.w','#0x59f,%d0',4)
    e.label('gameplay_pc_000626')
    e.ins('move.l','%d1,0xc00000:l',6)
    e.label('gameplay_pc_00062c')
    e.ins('dbra','%d0,gameplay_pc_000626',4)
    e.label('gameplay_pc_000630')
    e.ins('tst.w','0xf6c4:w',4)
    e.label('gameplay_pc_000634')
    e.ins('bne.b','gameplay_pc_000668',2)
    e.label('gameplay_pc_000636')
    e.ins('move.l','#0x70000001,0xc00004:l',10)
    e.label('gameplay_pc_000640')
    e.ins('lea.l','0x89ddc:l,%a0',6)
    e.label('gameplay_pc_000646')
    e.ins('move.w','#0x17,%d0',4)
    e.label('gameplay_pc_00064a')
    e.ins('move.l','(%a0)+,0xc00000:l',6)
    e.label('gameplay_pc_000650')
    e.ins('dbra','%d0,gameplay_pc_00064a',4)
    e.label('gameplay_pc_000654')
    e.ins('lea.l','0x8a07c:l,%a0',6)
    e.label('gameplay_pc_00065a')
    e.ins('move.w','#0xf,%d0',4)
    e.label('gameplay_pc_00065e')
    e.ins('move.l','(%a0)+,0xc00000:l',6)
    e.label('gameplay_pc_000664')
    e.ins('dbra','%d0,gameplay_pc_00065e',4)
    e.label('gameplay_pc_000668')
    e.ins('bsr.w','gameplay_pc_00068a',4)
    e.label('gameplay_pc_00066c')
    e.ins('lea.l','0xf516:w,%a0',4)
    e.label('gameplay_pc_000670')
    e.ins('move.w','#0x17,%d0',4)
    e.label('gameplay_pc_000674')
    e.ins('move.l','%d1,(%a0)+',2)
    e.label('gameplay_pc_000676')
    e.ins('dbra','%d0,gameplay_pc_000674',4)
    e.label('gameplay_pc_00067a')
    e.ins('clr.w','0xf37a:w',4)
    e.label('gameplay_pc_00067e')
    e.ins('clr.w','0xf37c:w',4)
    e.label('gameplay_pc_000682')
    e.ins('jsr','gameplay_pc_00af48:l',6)
    e.label('gameplay_pc_000688')
    e.ins('rts','',2)

def _lower_select_scene_fill_pattern(e,rules):
    e.label('gameplay_pc_00068a')
    e.ins('move.w','0xf6c4:w,%d0',4)
    e.label('gameplay_pc_00068e')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_000690')
    e.ins('move.l','4(%pc, %d0.w),%d1',4)
    e.label('gameplay_pc_000694')
    e.ins('rts','',2)

def _lower_reset_scene_input_markers(e,rules):
    e.label('gameplay_pc_004a16')
    e.ins('clr.w','0xf300:w',4)
    e.label('gameplay_pc_004a1a')
    e.ins('clr.w','0xf800:w',4)
    e.label('gameplay_pc_004a1e')
    e.ins('clr.w','0xf802:w',4)
    e.label('gameplay_pc_004a22')
    e.ins('clr.w','0xf806:w',4)
    e.label('gameplay_pc_004a26')
    e.ins('nop','',2)
    e.label('gameplay_pc_004a28')
    e.ins('nop','',2)
    e.label('gameplay_pc_004a2a')
    e.ins('rts','',2)

def _lower_initialize_video_registers_and_planes(e,rules):
    e.label('gameplay_pc_006826')
    e.ins('lea.l','0xc00004:l,%a0',6)
    e.label('gameplay_pc_00682c')
    e.ins('lea.l','0xc00000:l,%a1',6)
    e.label('gameplay_pc_006832')
    e.ins('lea.l','116(%pc),%a2',4)
    e.label('gameplay_pc_006836')
    e.ins('moveq','#18,%d7',2)
    e.label('gameplay_pc_006838')
    e.ins('move.w','(%a2)+,(%a0)',2)
    e.label('gameplay_pc_00683a')
    e.ins('dbra','%d7,gameplay_pc_006838',4)
    e.label('gameplay_pc_00683e')
    e.ins('move.w','106(%pc),0xf606:w',6)
    e.label('gameplay_pc_006844')
    e.ins('moveq','#0,%d0',2)
    e.label('gameplay_pc_006846')
    e.ins('move.l','#0xc0000000,0xc00004:l',10)
    e.label('gameplay_pc_006850')
    e.ins('move.w','#0x3f,%d7',4)
    e.label('gameplay_pc_006854')
    e.ins('move.w','%d0,(%a1)',2)
    e.label('gameplay_pc_006856')
    e.ins('dbra','%d7,gameplay_pc_006854',4)
    e.label('gameplay_pc_00685a')
    e.ins('lea.l','0xc00004:l,%a6',6)
    e.label('gameplay_pc_006860')
    e.ins('move.w','#0x8f01,(%a6)',4)
    e.label('gameplay_pc_006864')
    e.ins('move.w','0xf606:w,%d7',4)
    e.label('gameplay_pc_006868')
    e.ins('ori.b','#0x10,%d7',4)
    e.label('gameplay_pc_00686c')
    e.ins('move.w','%d7,(%a6)',2)
    e.label('gameplay_pc_00686e')
    e.ins('move.l','#0x93ff94ff,(%a6)',6)
    e.label('gameplay_pc_006874')
    e.ins('move.w','#0x9780,(%a6)',4)
    e.label('gameplay_pc_006878')
    e.ins('move.l','#0x40000080,(%a6)',6)
    e.label('gameplay_pc_00687e')
    e.ins('move.w','#0x0,0xc00000:l',8)
    e.label('gameplay_pc_006886')
    e.ins('move.w','(%a6),%d7',2)
    e.label('gameplay_pc_006888')
    e.ins('andi.w','#0x2,%d7',4)
    e.label('gameplay_pc_00688c')
    e.ins('bne.b','gameplay_pc_006886',2)
    e.label('gameplay_pc_00688e')
    e.ins('tst.b','0xff3f00:l',6)
    e.label('gameplay_pc_006894')
    e.ins('bne.b','gameplay_pc_00689e',2)
    e.label('gameplay_pc_006896')
    e.ins('move.w','#0x0,0xa11100:l',8)
    e.label('gameplay_pc_00689e')
    e.ins('move.w','0xf606:w,(%a6)',4)
    e.label('gameplay_pc_0068a2')
    e.ins('move.w','#0x8f02,(%a6)',4)
    e.label('gameplay_pc_0068a6')
    e.ins('rts','',2)

def _lower_clear_video_sprite_plane(e,rules):
    e.label('gameplay_pc_0068ce')
    e.ins('lea.l','0xc00004:l,%a6',6)
    e.label('gameplay_pc_0068d4')
    e.ins('move.w','#0x8f01,(%a6)',4)
    e.label('gameplay_pc_0068d8')
    e.ins('move.w','0xf606:w,%d7',4)
    e.label('gameplay_pc_0068dc')
    e.ins('ori.b','#0x10,%d7',4)
    e.label('gameplay_pc_0068e0')
    e.ins('move.w','%d7,(%a6)',2)
    e.label('gameplay_pc_0068e2')
    e.ins('move.l','#0x93ff9447,(%a6)',6)
    e.label('gameplay_pc_0068e8')
    e.ins('move.w','#0x9780,(%a6)',4)
    e.label('gameplay_pc_0068ec')
    e.ins('move.l','#0x78000082,(%a6)',6)
    e.label('gameplay_pc_0068f2')
    e.ins('move.w','#0xf6,0xc00000:l',8)
    e.label('gameplay_pc_0068fa')
    e.ins('move.w','(%a6),%d7',2)
    e.label('gameplay_pc_0068fc')
    e.ins('andi.w','#0x2,%d7',4)
    e.label('gameplay_pc_006900')
    e.ins('bne.b','gameplay_pc_0068fa',2)
    e.label('gameplay_pc_006902')
    e.ins('tst.b','0xff3f00:l',6)
    e.label('gameplay_pc_006908')
    e.ins('bne.b','gameplay_pc_006912',2)
    e.label('gameplay_pc_00690a')
    e.ins('move.w','#0x0,0xa11100:l',8)
    e.label('gameplay_pc_006912')
    e.ins('move.w','0xf606:w,(%a6)',4)
    e.label('gameplay_pc_006916')
    e.ins('move.w','#0x8f02,(%a6)',4)
    e.label('gameplay_pc_00691a')
    e.ins('move.l','#0x40000010,0xc00004:l',10)
    e.label('gameplay_pc_006924')
    e.ins('move.l','#0x0,0xc00000:l',10)
    e.label('gameplay_pc_00692e')
    e.ins('move.l','#0x0,0xf312:w',8)
    e.label('gameplay_pc_006936')
    e.ins('move.l','#0x0,0xf316:w',8)
    e.label('gameplay_pc_00693e')
    e.ins('lea.l','0xf800:w,%a6',4)
    e.label('gameplay_pc_006942')
    e.ins('moveq','#0,%d7',2)
    e.label('gameplay_pc_006944')
    e.ins('move.w','#0x9f,%d6',4)
    e.label('gameplay_pc_006948')
    e.ins('move.l','%d7,(%a6)+',2)
    e.label('gameplay_pc_00694a')
    e.ins('dbra','%d6,gameplay_pc_006948',4)
    e.label('gameplay_pc_00694e')
    e.ins('rts','',2)

def _lower_enqueue_sound_command(e,rules):
    e.label('gameplay_pc_00808a')
    e.ins('st.b','0xff3f00:l',6)
    e.label('gameplay_pc_008090')
    e.ins('move.w','#0x100,0xa11100:l',8)
    e.label('gameplay_pc_008098')
    e.ins('btst.b','#0x0,0xa11100:l',8)
    e.label('gameplay_pc_0080a0')
    e.ins('bne.b','gameplay_pc_008098',2)
    e.label('gameplay_pc_0080a2')
    e.ins('tst.b','0xa01c0a:l',6)
    e.label('gameplay_pc_0080a8')
    e.ins('beq.b','gameplay_pc_0080ba',2)
    e.label('gameplay_pc_0080aa')
    e.ins('tst.b','0xa01c0b:l',6)
    e.label('gameplay_pc_0080b0')
    e.ins('bne.b','gameplay_pc_0080c0',2)
    e.label('gameplay_pc_0080b2')
    e.ins('move.b','%d0,0xa01c0b:l',6)
    e.label('gameplay_pc_0080b8')
    e.ins('bra.b','gameplay_pc_0080c0',2)
    e.label('gameplay_pc_0080ba')
    e.ins('move.b','%d0,0xa01c0a:l',6)
    e.label('gameplay_pc_0080c0')
    e.ins('sf.b','0xff3f00:l',6)
    e.label('gameplay_pc_0080c6')
    e.ins('move.w','#0x0,0xa11100:l',8)
    e.label('gameplay_pc_0080ce')
    e.ins('rts','',2)

def _lower_copy_video_transfer_descriptor(e,rules):
    e.label('gameplay_pc_008112')
    e.ins('lea.l','24(%pc),%a1',4)
    e.label('gameplay_pc_008116')
    e.ins('lsl.w','#0x3,%d0',2)
    e.label('gameplay_pc_008118')
    e.ins('adda.w','%d0,%a1',2)
    e.label('gameplay_pc_00811a')
    e.ins('movea.l','(%a1)+,%a2',2)
    e.label('gameplay_pc_00811c')
    e.ins('movea.w','(%a1)+,%a3',2)
    e.label('gameplay_pc_00811e')
    e.ins('move.w','(%a1)+,%d7',2)
    e.label('gameplay_pc_008120')
    e.ins('move.l','(%a2)+,(%a3)+',2)
    e.label('gameplay_pc_008122')
    e.ins('dbra','%d7,gameplay_pc_008120',4)
    e.label('gameplay_pc_008126')
    e.ins('addq.w','#0x1,0xf31e:w',4)
    e.label('gameplay_pc_00812a')
    e.ins('rts','',2)

def _lower_wait_for_scene_sound_byte(e,rules):
    e.label('gameplay_pc_0083c8')
    e.ins('move.w','#0x2500,%sr',4)
    e.label('gameplay_pc_0083cc')
    e.ins('tst.b','0xf612:w',4)
    e.label('gameplay_pc_0083d0')
    e.ins('bne.b','gameplay_pc_0083cc',2)
    e.label('gameplay_pc_0083d2')
    e.ins('rts','',2)

def _lower_expand_glyph_row(e,rules):
    e.label('gameplay_pc_00af04')
    e.ins('moveq','#0,%d7',2)
    e.label('gameplay_pc_00af06')
    e.ins('move.b','(%a2)+,%d6',2)
    e.label('gameplay_pc_00af08')
    e.ins('move.w','#0x7,%d4',4)
    e.label('gameplay_pc_00af0c')
    e.ins('lsl.l','#0x4,%d7',2)
    e.label('gameplay_pc_00af0e')
    e.ins('roxl.b','#0x1,%d6',2)
    e.label('gameplay_pc_00af10')
    e.ins('bcc.b','gameplay_pc_00af16',2)
    e.label('gameplay_pc_00af12')
    e.ins('or.b','%d1,%d7',2)
    e.label('gameplay_pc_00af14')
    e.ins('bra.b','gameplay_pc_00af18',2)
    e.label('gameplay_pc_00af16')
    e.ins('or.b','%d0,%d7',2)
    e.label('gameplay_pc_00af18')
    e.ins('dbra','%d4,gameplay_pc_00af0c',4)
    e.label('gameplay_pc_00af1c')
    e.ins('rts','',2)

def _lower_expand_glyph_stream(e,rules):
    e.label('gameplay_pc_00af1e')
    e.ins('movem.l','%d4-%d7,-(%a7)',4)
    e.label('gameplay_pc_00af22')
    e.ins('clr.w','%d4',2)
    e.label('gameplay_pc_00af24')
    e.ins('move.b','(%a0)+,%d4',2)
    e.label('gameplay_pc_00af26')
    e.ins('lsl.w','#0x3,%d4',2)
    e.label('gameplay_pc_00af28')
    e.ins('lea.l','0x896dc:l,%a2',6)
    e.label('gameplay_pc_00af2e')
    e.ins('lea.l','(%a2, %d4.w),%a2',4)
    e.label('gameplay_pc_00af32')
    e.ins('move.w','#0x7,%d5',4)
    e.label('gameplay_pc_00af36')
    e.ins('bsr.b','gameplay_pc_00af04',2)
    e.label('gameplay_pc_00af38')
    e.ins('move.l','%d7,(%a1)+',2)
    e.label('gameplay_pc_00af3a')
    e.ins('dbra','%d5,gameplay_pc_00af36',4)
    e.label('gameplay_pc_00af3e')
    e.ins('dbra','%d3,gameplay_pc_00af22',4)
    e.label('gameplay_pc_00af42')
    e.ins('movem.l','(%a7)+,%d4-%d7',4)
    e.label('gameplay_pc_00af46')
    e.ins('rts','',2)

def _lower_refresh_gameplay_scene(e,rules):
    e.label('gameplay_pc_00af48')
    e.ins('nop','',2)
    e.label('gameplay_pc_00af4a')
    e.ins('nop','',2)
    e.label('gameplay_pc_00af4c')
    e.ins('move.w','0xc00004:l,%d0',6)
    e.label('gameplay_pc_00af52')
    e.ins('btst.l','#0x3,%d0',4)
    e.label('gameplay_pc_00af56')
    e.ins('bne.b','gameplay_pc_00af4c',2)
    e.label('gameplay_pc_00af58')
    e.ins('nop','',2)
    e.label('gameplay_pc_00af5a')
    e.ins('nop','',2)
    e.label('gameplay_pc_00af5c')
    e.ins('move.w','0xc00004:l,%d0',6)
    e.label('gameplay_pc_00af62')
    e.ins('btst.l','#0x3,%d0',4)
    e.label('gameplay_pc_00af66')
    e.ins('beq.b','gameplay_pc_00af5c',2)
    e.label('gameplay_pc_00af68')
    e.ins('rts','',2)

def _lower_load_gameplay_scene(e,rules):
    e.label('gameplay_pc_01072c')
    e.ins('tst.w','0xefd6:w',4)
    e.label('gameplay_pc_010730')
    e.ins('bne.w','gameplay_pc_0107fc',4)
    e.label('gameplay_pc_010734')
    e.ins('move.w','0xf612:w,-(%a7)',4)
    e.label('gameplay_pc_010738')
    e.ins('bclr.b','#0x2,0xf3a5:w',6)
    e.label('gameplay_pc_01073e')
    e.ins('jsr','gameplay_pc_004a16:l',6)
    e.label('gameplay_pc_010744')
    e.ins('move.w','#0x900,0xf612:w',6)
    e.label('gameplay_pc_01074a')
    e.ins('jsr','gameplay_pc_00af48:l',6)
    e.label('gameplay_pc_010750')
    e.ins('jsr','gameplay_pc_0083c8:l',6)
    e.label('gameplay_pc_010756')
    e.ins('move.w','#0x2700,%sr',4)
    e.label('gameplay_pc_01075a')
    e.ins('bsr.w','gameplay_pc_010814',4)
    e.label('gameplay_pc_01075e')
    e.ins('move.l','#0x40840003,0xc00004:l',10)
    e.label('gameplay_pc_010768')
    e.ins('move.w','#0x5,%d0',4)
    e.label('gameplay_pc_01076c')
    e.ins('move.l','#0x0,0xc00000:l',10)
    e.label('gameplay_pc_010776')
    e.ins('dbra','%d0,gameplay_pc_01076c',4)
    e.label('gameplay_pc_01077a')
    e.ins('bsr.w','gameplay_pc_010896',4)
    e.label('gameplay_pc_01077e')
    e.ins('jsr','gameplay_pc_03969a:l',6)
    e.label('gameplay_pc_010784')
    e.ins('move.w','#0x2700,%sr',4)
    e.label('gameplay_pc_010788')
    e.ins('bsr.w','gameplay_pc_0109d8',4)
    e.label('gameplay_pc_01078c')
    e.ins('move.w','#0xffff,0xff7026:l',8)
    e.label('gameplay_pc_010794')
    e.ins('move.l','#0x40200000,0xc00004:l',10)
    e.label('gameplay_pc_01079e')
    e.ins('move.w','#0x7,%d0',4)
    e.label('gameplay_pc_0107a2')
    e.ins('move.l','#0x11111111,0xc00000:l',10)
    e.label('gameplay_pc_0107ac')
    e.ins('dbra','%d0,gameplay_pc_0107a2',4)
    e.label('gameplay_pc_0107b0')
    e.ins('clr.w','0xf37e:w',4)
    e.label('gameplay_pc_0107b4')
    e.ins('move.w','(%a7)+,0xf612:w',4)
    e.label('gameplay_pc_0107b8')
    e.ins('bclr.b','#0x3,0xf3a4:w',6)
    e.label('gameplay_pc_0107be')
    e.ins('clr.l','0xefc8:w',4)
    e.label('gameplay_pc_0107c2')
    e.ins('clr.l','0xefcc:w',4)
    e.label('gameplay_pc_0107c6')
    e.ins('move.l','#0x78000002,0xc00004:l',10)
    e.label('gameplay_pc_0107d0')
    e.ins('move.l','#0x0,0xc00000:l',10)
    e.label('gameplay_pc_0107da')
    e.ins('move.l','#0x0,0xc00000:l',10)
    e.label('gameplay_pc_0107e4')
    e.ins('bsr.w','gameplay_pc_010880',4)
    e.label('gameplay_pc_0107e8')
    e.ins('cmpi.w','#0x1,0xf6c4:w',6)
    e.label('gameplay_pc_0107ee')
    e.ins('bne.w','gameplay_pc_010812',4)
    e.label('gameplay_pc_0107f2')
    e.ins('jsr','gameplay_pc_0177be:l',6)
    e.label('gameplay_pc_0107f8')
    e.ins('bra.w','gameplay_pc_010812',4)
    e.label('gameplay_pc_0107fc')
    e.ins('move.l','#0x100000,%d0',6)
    e.label('gameplay_pc_010802')
    e.ins('nop','',2)
    e.label('gameplay_pc_010804')
    e.ins('nop','',2)
    e.label('gameplay_pc_010806')
    e.ins('dbra','%d0,gameplay_pc_010802',4)
    e.label('gameplay_pc_01080a')
    e.ins('move.w','#0xffff,0xff7026:l',8)
    e.label('gameplay_pc_010812')
    e.ins('rts','',2)

def _lower_select_sound_command_from_scene(e,rules):
    e.label('gameplay_pc_010814')
    e.ins('move.w','0xff7026:l,%d0',6)
    e.label('gameplay_pc_01081a')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01081c')
    e.ins('move.w','18(%pc, %d0.w),%d0',4)
    e.label('gameplay_pc_010820')
    e.ins('move.w','%d0,0xefd0:w',4)
    e.label('gameplay_pc_010824')
    e.ins('bmi.w','gameplay_pc_01082e',4)
    e.label('gameplay_pc_010828')
    e.ins('jsr','gameplay_pc_00808a:l',6)
    e.label('gameplay_pc_01082e')
    e.ins('rts','',2)

def _lower_resume_pending_sound(e,rules):
    e.label('gameplay_pc_010880')
    e.ins('tst.w','0xefd0:w',4)
    e.label('gameplay_pc_010884')
    e.ins('bmi.w','gameplay_pc_010894',4)
    e.label('gameplay_pc_010888')
    e.ins('clr.w','%d0',2)
    e.label('gameplay_pc_01088a')
    e.ins('move.b','0xf764:w,%d0',4)
    e.label('gameplay_pc_01088e')
    e.ins('jsr','gameplay_pc_00808a:l',6)
    e.label('gameplay_pc_010894')
    e.ins('rts','',2)

def _lower_draw_overlay_frame(e,rules):
    e.label('gameplay_pc_010896')
    e.ins('move.l','#0x72000001,0xc00004:l',10)
    e.label('gameplay_pc_0108a0')
    e.ins('move.w','#0x7,%d0',4)
    e.label('gameplay_pc_0108a4')
    e.ins('move.l','#0x33333333,0xc00000:l',10)
    e.label('gameplay_pc_0108ae')
    e.ins('dbra','%d0,gameplay_pc_0108a4',4)
    e.label('gameplay_pc_0108b2')
    e.ins('lea.l','0x8a0bc:l,%a0',6)
    e.label('gameplay_pc_0108b8')
    e.ins('move.w','#0x3f,%d0',4)
    e.label('gameplay_pc_0108bc')
    e.ins('move.l','(%a0)+,0xc00000:l',6)
    e.label('gameplay_pc_0108c2')
    e.ins('dbra','%d0,gameplay_pc_0108bc',4)
    e.label('gameplay_pc_0108c6')
    e.ins('move.l','#0x41040003,%d0',6)
    e.label('gameplay_pc_0108cc')
    e.ins('bsr.w','gameplay_pc_0108e2',4)
    e.label('gameplay_pc_0108d0')
    e.ins('move.w','#0x9,%d2',4)
    e.label('gameplay_pc_0108d4')
    e.ins('bsr.w','gameplay_pc_01093e',4)
    e.label('gameplay_pc_0108d8')
    e.ins('dbra','%d2,gameplay_pc_0108d4',4)
    e.label('gameplay_pc_0108dc')
    e.ins('bsr.w','gameplay_pc_010972',4)
    e.label('gameplay_pc_0108e0')
    e.ins('rts','',2)

def _lower_draw_overlay_frame_header(e,rules):
    e.label('gameplay_pc_0108e2')
    e.ins('move.l','%d0,0xc00004:l',6)
    e.label('gameplay_pc_0108e8')
    e.ins('move.w','#0xc391,0xc00000:l',8)
    e.label('gameplay_pc_0108f0')
    e.ins('move.w','#0x8,%d1',4)
    e.label('gameplay_pc_0108f4')
    e.ins('move.l','#0xc392c392,0xc00000:l',10)
    e.label('gameplay_pc_0108fe')
    e.ins('dbra','%d1,gameplay_pc_0108f4',4)
    e.label('gameplay_pc_010902')
    e.ins('move.w','#0xcb97,0xc00000:l',8)
    e.label('gameplay_pc_01090a')
    e.ins('addi.l','#0x800000,%d0',6)
    e.label('gameplay_pc_010910')
    e.ins('move.l','%d0,0xc00004:l',6)
    e.label('gameplay_pc_010916')
    e.ins('move.l','#0xc393c394,0xc00000:l',10)
    e.label('gameplay_pc_010920')
    e.ins('move.w','#0x7,%d1',4)
    e.label('gameplay_pc_010924')
    e.ins('move.l','#0xc395c395,0xc00000:l',10)
    e.label('gameplay_pc_01092e')
    e.ins('dbra','%d1,gameplay_pc_010924',4)
    e.label('gameplay_pc_010932')
    e.ins('move.l','#0xcb98db93,0xc00000:l',10)
    e.label('gameplay_pc_01093c')
    e.ins('rts','',2)

def _lower_draw_overlay_frame_middle(e,rules):
    e.label('gameplay_pc_01093e')
    e.ins('addi.l','#0x800000,%d0',6)
    e.label('gameplay_pc_010944')
    e.ins('move.l','%d0,0xc00004:l',6)
    e.label('gameplay_pc_01094a')
    e.ins('move.l','#0xc393c396,0xc00000:l',10)
    e.label('gameplay_pc_010954')
    e.ins('move.w','#0x7,%d1',4)
    e.label('gameplay_pc_010958')
    e.ins('move.l','#0x43904390,0xc00000:l',10)
    e.label('gameplay_pc_010962')
    e.ins('dbra','%d1,gameplay_pc_010958',4)
    e.label('gameplay_pc_010966')
    e.ins('move.l','#0xdb96db93,0xc00000:l',10)
    e.label('gameplay_pc_010970')
    e.ins('rts','',2)

def _lower_draw_overlay_frame_footer(e,rules):
    e.label('gameplay_pc_010972')
    e.ins('addi.l','#0x800000,%d0',6)
    e.label('gameplay_pc_010978')
    e.ins('move.l','%d0,0xc00004:l',6)
    e.label('gameplay_pc_01097e')
    e.ins('move.l','#0xc393d398,0xc00000:l',10)
    e.label('gameplay_pc_010988')
    e.ins('move.w','#0x7,%d1',4)
    e.label('gameplay_pc_01098c')
    e.ins('move.l','#0xdb95db95,0xc00000:l',10)
    e.label('gameplay_pc_010996')
    e.ins('dbra','%d1,gameplay_pc_01098c',4)
    e.label('gameplay_pc_01099a')
    e.ins('move.l','#0xdb94db93,0xc00000:l',10)
    e.label('gameplay_pc_0109a4')
    e.ins('addi.l','#0x800000,%d0',6)
    e.label('gameplay_pc_0109aa')
    e.ins('move.l','%d0,0xc00004:l',6)
    e.label('gameplay_pc_0109b0')
    e.ins('move.l','#0xd397db92,0xc00000:l',10)
    e.label('gameplay_pc_0109ba')
    e.ins('move.w','#0x7,%d1',4)
    e.label('gameplay_pc_0109be')
    e.ins('move.l','#0xdb92db92,0xc00000:l',10)
    e.label('gameplay_pc_0109c8')
    e.ins('dbra','%d1,gameplay_pc_0109be',4)
    e.label('gameplay_pc_0109cc')
    e.ins('move.l','#0xdb92db91,0xc00000:l',10)
    e.label('gameplay_pc_0109d6')
    e.ins('rts','',2)

def _lower_clear_overlay_frame(e,rules):
    e.label('gameplay_pc_0109d8')
    e.ins('move.l','#0x41040003,%d0',6)
    e.label('gameplay_pc_0109de')
    e.ins('move.w','#0xd,%d1',4)
    e.label('gameplay_pc_0109e2')
    e.ins('move.l','%d0,0xc00004:l',6)
    e.label('gameplay_pc_0109e8')
    e.ins('move.w','#0x9,%d2',4)
    e.label('gameplay_pc_0109ec')
    e.ins('move.l','#0x0,0xc00000:l',10)
    e.label('gameplay_pc_0109f6')
    e.ins('dbra','%d2,gameplay_pc_0109ec',4)
    e.label('gameplay_pc_0109fa')
    e.ins('addi.l','#0x800000,%d0',6)
    e.label('gameplay_pc_010a00')
    e.ins('dbra','%d1,gameplay_pc_0109e2',4)
    e.label('gameplay_pc_010a04')
    e.ins('rts','',2)

def _lower_stage_sprite_word_packet(e,rules):
    e.label('gameplay_pc_026bfa')
    e.ins('lea.l','0xd100:w,%a1',4)
    e.label('gameplay_pc_026bfe')
    e.ins('adda.w','0xf31a:w,%a1',4)
    e.label('gameplay_pc_026c02')
    e.ins('move.w','%d1,%d7',2)
    e.label('gameplay_pc_026c04')
    e.ins('subq.w','#0x1,%d7',2)
    e.label('gameplay_pc_026c06')
    e.ins('move.w','%d0,(%a1)+',2)
    e.label('gameplay_pc_026c08')
    e.ins('move.w','%d2,(%a1)+',2)
    e.label('gameplay_pc_026c0a')
    e.ins('addi.w','#0x80,%d2',4)
    e.label('gameplay_pc_026c0e')
    e.ins('move.w','%d0,%d3',2)
    e.label('gameplay_pc_026c10')
    e.ins('move.w','(%a0)+,%d4',2)
    e.label('gameplay_pc_026c12')
    e.ins('bmi.b','gameplay_pc_026c22',2)
    e.label('gameplay_pc_026c14')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_026c16')
    e.ins('or.w','%d0,%d4',2)
    e.label('gameplay_pc_026c18')
    e.ins('move.w','%d4,(%a1)+',2)
    e.label('gameplay_pc_026c1a')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_026c1c')
    e.ins('subq.w','#0x1,%d3',2)
    e.label('gameplay_pc_026c1e')
    e.ins('bra.w','gameplay_pc_026c36',4)
    e.label('gameplay_pc_026c22')
    e.ins('move.w','%d4,%d5',2)
    e.label('gameplay_pc_026c24')
    e.ins('andi.w','#0x7fff,%d4',4)
    e.label('gameplay_pc_026c28')
    e.ins('lsr.w','#0x7,%d4',2)
    e.label('gameplay_pc_026c2a')
    e.ins('bclr.l','#0x0,%d4',4)
    e.label('gameplay_pc_026c2e')
    e.ins('move.w','28(%pc, %d4.w),%d4',4)
    e.label('gameplay_pc_026c32')
    e.ins('jsr','36(%pc, %d4.w)',4)
    e.label('gameplay_pc_026c36')
    e.ins('tst.w','%d3',2)
    e.label('gameplay_pc_026c38')
    e.ins('bne.b','gameplay_pc_026c10',2)
    e.label('gameplay_pc_026c3a')
    e.ins('dbra','%d7,gameplay_pc_026c06',4)
    e.label('gameplay_pc_026c3e')
    e.ins('clr.w','(%a1)',2)
    e.label('gameplay_pc_026c40')
    e.ins('addq.w','#0x2,%d0',2)
    e.label('gameplay_pc_026c42')
    e.ins('mulu.w','%d1,%d0',2)
    e.label('gameplay_pc_026c44')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_026c46')
    e.ins('add.w','%d0,0xf31a:w',4)
    e.label('gameplay_pc_026c4a')
    e.ins('rts','',2)

def _lower_present_gameplay_message(e,rules):
    e.label('gameplay_pc_030a74')
    e.ins('move.w','0xf612:w,-(%a7)',4)
    e.label('gameplay_pc_030a78')
    e.ins('move.w','0xf362:w,-(%a7)',4)
    e.label('gameplay_pc_030a7c')
    e.ins('move.w','#0x20b,0xf612:w',6)
    e.label('gameplay_pc_030a82')
    e.ins('clr.w','0xf600:w',4)
    e.label('gameplay_pc_030a86')
    e.ins('jsr','gameplay_pc_00af48:l',6)
    e.label('gameplay_pc_030a8c')
    e.ins('move.w','#0x2500,%sr',4)
    e.label('gameplay_pc_030a90')
    e.ins('tst.w','0xf600:w',4)
    e.label('gameplay_pc_030a94')
    e.ins('beq.b','gameplay_pc_030a90',2)
    e.label('gameplay_pc_030a96')
    e.ins('cmpi.w','#0x28,0xf600:w',6)
    e.label('gameplay_pc_030a9c')
    e.ins('bne.w','gameplay_pc_030ab0',4)
    e.label('gameplay_pc_030aa0')
    e.ins('jsr','gameplay_pc_00060c:l',6)
    e.label('gameplay_pc_030aa6')
    e.ins('clr.w','0xf600:w',4)
    e.label('gameplay_pc_030aaa')
    e.ins('move.w','#0x2500,%sr',4)
    e.label('gameplay_pc_030aae')
    e.ins('bra.b','gameplay_pc_030a90',2)
    e.label('gameplay_pc_030ab0')
    e.ins('move.w','#0x2700,%sr',4)
    e.label('gameplay_pc_030ab4')
    e.ins('move.w','(%a7)+,0xf362:w',4)
    e.label('gameplay_pc_030ab8')
    e.ins('move.w','(%a7)+,0xf612:w',4)
    e.label('gameplay_pc_030abc')
    e.ins('rts','',2)

LOWERERS = {
    'clear_scene_video_and_state':_lower_clear_scene_video_and_state,
    'select_scene_fill_pattern':_lower_select_scene_fill_pattern,
    'reset_scene_input_markers':_lower_reset_scene_input_markers,
    'initialize_video_registers_and_planes':_lower_initialize_video_registers_and_planes,
    'clear_video_sprite_plane':_lower_clear_video_sprite_plane,
    'enqueue_sound_command':_lower_enqueue_sound_command,
    'copy_video_transfer_descriptor':_lower_copy_video_transfer_descriptor,
    'wait_for_scene_sound_byte':_lower_wait_for_scene_sound_byte,
    'expand_glyph_row':_lower_expand_glyph_row,
    'expand_glyph_stream':_lower_expand_glyph_stream,
    'refresh_gameplay_scene':_lower_refresh_gameplay_scene,
    'load_gameplay_scene':_lower_load_gameplay_scene,
    'select_sound_command_from_scene':_lower_select_sound_command_from_scene,
    'resume_pending_sound':_lower_resume_pending_sound,
    'draw_overlay_frame':_lower_draw_overlay_frame,
    'draw_overlay_frame_header':_lower_draw_overlay_frame_header,
    'draw_overlay_frame_middle':_lower_draw_overlay_frame_middle,
    'draw_overlay_frame_footer':_lower_draw_overlay_frame_footer,
    'clear_overlay_frame':_lower_clear_overlay_frame,
    'stage_sprite_word_packet':_lower_stage_sprite_word_packet,
    'present_gameplay_message':_lower_present_gameplay_message,
}

# One shared four-marker field algorithm; the original 22-byte owner remains.
# This is finite host admission, not general Python semantic compilation.
APPROVED['contexts_services'].add('MarkerResetMemory')
DECLARATIONS.update({
    'reset_scene_input_markers': {
        'signature': 'state: GameplayState',
        'returns': 'None',
        'flow': 'checked_state(state)\n_reset_scene_input_marker_fields(MarkerResetMemory(state))',
    },
    '_reset_scene_input_marker_fields': {
        'signature': 'memory: MarkerResetMemory',
        'returns': 'None',
        'flow': "if type(memory) is not MarkerResetMemory:\n    raise ValueError('sealed live marker memory required')\nmemory.validate()\nfor address in (4294963968, 4294965248, 4294965250, 4294965254):\n    memory.state.read(address, 2)\n    memory.write_word(address, 0)",
    },
})


def compile_services(source):
    records=semantic_functions(source,DECLARATIONS,APPROVED)
    sole_scene_clear_fields = {name:records[name]['effects'] for name in ('clear_scene_video_and_state_fields', 'select_scene_fill_pattern_fields', '_scene_refresh_call_fields')}
    for owner in ('clear_scene_video_and_state', 'select_scene_fill_pattern'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'], sole_scene_clear_fields=sole_scene_clear_fields)
    sole_refresh_fields = {name:records[name]['effects'] for name in ('_scene_refresh_advance_command', '_scene_refresh_bit_clear', '_scene_refresh_call_fields', '_scene_refresh_decrement', '_scene_refresh_emit', '_scene_refresh_flags', '_scene_refresh_frame', '_scene_refresh_repeat_pixels', 'clear_overlay_frame_fields', 'draw_overlay_frame_fields', 'draw_overlay_frame_footer_fields', 'draw_overlay_frame_header_fields', 'draw_overlay_frame_middle_fields', 'enqueue_sound_command_fields', 'load_gameplay_scene_fields', 'refresh_gameplay_scene_fields', 'resume_pending_sound_fields', 'select_sound_command_from_scene_fields', 'wait_for_scene_sound_byte_fields')}
    for owner in ('reset_scene_input_markers', 'enqueue_sound_command', 'wait_for_scene_sound_byte', 'refresh_gameplay_scene', 'load_gameplay_scene', 'select_sound_command_from_scene', 'resume_pending_sound', 'draw_overlay_frame', 'draw_overlay_frame_header', 'draw_overlay_frame_middle', 'draw_overlay_frame_footer', 'clear_overlay_frame'):
        records[owner]['effects'] = dict(legacy_projection=records[owner]['effects'],sole_refresh_fields=sole_refresh_fields)
    records['present_gameplay_message']['effects'] += '\nsole modal field core: ' + '\n'.join(records[name]['effects'] for name in ('_gameplay_message_call_fields', 'present_gameplay_message_fields'))
    for owner in ('stage_sprite_word_packet',):
        records[owner]['effects'] += '\nsole consolidation/arrival/packet fields: ' + '\n'.join(records[name]['effects'] for name in ('stage_sprite_word_packet_fields', '_word_packet_copy_run_fields', 'increment_word_packet_control_fields', 'repeat_word_packet_control_fields'))
    sole_remaining_word_controls = {name:records[name]['effects'] for name in ('_word_packet_numeric_control_fields', '_word_packet_tile_pair_control_fields', 'append_even_tile_pair_control_fields', 'append_long_decimal_packet_control_fields', 'append_odd_tile_pair_control_fields', 'append_word_decimal_packet_control_fields', 'stage_sprite_word_packet_fields')}
    for owner in ('stage_sprite_word_packet',):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'],sole_remaining_word_controls=sole_remaining_word_controls)
    sole_video_initialization_fields = {name:records[name]['effects'] for name in ('_video_plane_dma_fields', 'clear_video_sprite_plane_fields', 'initialize_video_registers_and_planes_fields')}
    for owner in ('initialize_video_registers_and_planes', 'clear_video_sprite_plane'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'],sole_video_initialization_fields=sole_video_initialization_fields)
    sole_transfer_descriptor_fields = {name:records[name]['effects'] for name in ('copy_video_transfer_descriptor_fields',)}
    for owner in ('copy_video_transfer_descriptor',):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'],sole_transfer_descriptor_fields=sole_transfer_descriptor_fields)
    return lower_declared({b.name:records[b.name] for b in SERVICES_BINDINGS},SERVICES_BINDINGS,LOWERERS)

# B19 sole refresh/display full fields; native lowerers unchanged.
APPROVED.setdefault('contexts_services',set()).update({'FirstDeploymentFrame', 'SceneRefreshBoundary', '_first_shift_word', 'SceneSoundSelectionFields', '_first_byte', '_first_long', '_first_word', 'SceneRefreshMemory', '_first_compare_word', 'first_replace'})
DECLARATIONS.update({'_scene_refresh_advance_command': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'left = frame.target_x\n'
                                            'if left is None:\n'
                                            '    raise SceneRefreshBoundary(67850, frame, None)\n'
                                            'value = u32(left + 8388608)\n'
                                            'overflow = bool(~(left ^ 8388608) & (left ^ value) & '
                                            '2147483648)\n'
                                            'status = (17 if left + 8388608 > 4294967295 else 0) | (2 if '
                                            'overflow else 0) | (8 if value & 2147483648 else 0) | (4 if '
                                            'value == 0 else 0)\n'
                                            'return memory.sync_status(first_replace(frame, target_x=value, '
                                            'status=status))'},
 '_scene_refresh_bit_clear': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                           'address, bit',
                              'returns': 'FirstDeploymentFrame',
                              'flow': 'memory.sync_status(frame)\n'
                                      'previous = memory.state.read(address, 1)\n'
                                      'memory.state.write(address, 1, previous & (255 ^ 1 << bit))\n'
                                      'status = None if frame.status is None else frame.status & 27 | (0 if '
                                      'previous & 1 << bit else 4)\n'
                                      'return memory.sync_status(first_replace(frame, status=status))'},
 '_scene_refresh_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                             'target: Long, continuation: Long, command: Byte | None=None',
                                'returns': 'FirstDeploymentFrame',
                                'flow': '_scene_refresh_frame(memory, frame)\n'
                                        'if (target, continuation) not in ((18966, 67396), (44872, 67408), '
                                        '(33736, 67414), (67604, 67422), (67734, 67454), (235162, 67460), '
                                        '(68056, 67468), (67712, 67560), (96190, 67576), (32906, 67630), '
                                        '(32906, 67732), (67810, 67792), (67902, 67800), (67954, 67808)):\n'
                                        "    raise ValueError('actual closed scene refresh child and token "
                                        "required')\n"
                                        'if command is not None and target != 32906:\n'
                                        "    raise ValueError('only sound mailbox has an observed BYTE "
                                        "argument')\n"
                                        'entered = memory.sync_status(frame)\n'
                                        'if frame.stack_cursor is not None:\n'
                                        '    stack = frame.stack_cursor.advance(-4)\n'
                                        '    stack.set_long(0, continuation)\n'
                                        '    entered = first_replace(frame, stack_cursor=stack)\n'
                                        'if target == 18966:\n'
                                        '    '
                                        '_reset_scene_input_marker_fields(MarkerResetMemory(memory.state))\n'
                                        '    result = _scene_refresh_flags(memory, entered, 0, 2)\n'
                                        'elif target == 44872:\n'
                                        '    result = refresh_gameplay_scene_fields(memory, entered)\n'
                                        'elif target == 33736:\n'
                                        '    result = wait_for_scene_sound_byte_fields(memory, entered)\n'
                                        'elif target == 67604:\n'
                                        '    result = select_sound_command_from_scene_fields(memory, '
                                        'entered).frame\n'
                                        'elif target == 67734:\n'
                                        '    result = draw_overlay_frame_fields(memory, entered)\n'
                                        'elif target == 68056:\n'
                                        '    result = clear_overlay_frame_fields(memory, entered)\n'
                                        'elif target == 67712:\n'
                                        '    result = resume_pending_sound_fields(memory, entered)\n'
                                        'elif target == 32906:\n'
                                        '    result = enqueue_sound_command_fields(memory, entered, '
                                        'command)\n'
                                        'elif target == 67810:\n'
                                        '    result = draw_overlay_frame_header_fields(memory, entered)\n'
                                        'elif target == 67902:\n'
                                        '    result = draw_overlay_frame_middle_fields(memory, entered)\n'
                                        'elif target == 67954:\n'
                                        '    result = draw_overlay_frame_footer_fields(memory, entered)\n'
                                        'elif target == 235162 and entered.stack_cursor is None:\n'
                                        '    observed = memory.state.service_at(target, '
                                        'SceneDisplayContext())\n'
                                        '    if type(observed) is not SceneDisplayResult:\n'
                                        "        raise Boundary('legacy renderer requires its real retained "
                                        "output observations')\n"
                                        '    observed.__post_init__()\n'
                                        '    result = first_replace(entered, target_y=observed.foreground, '
                                        'unit=observed.glyph_count, count=observed.training_carrier, '
                                        'status=None)\n'
                                        'elif target == 96190 and entered.stack_cursor is None:\n'
                                        '    from .business_battle import upload_battle_scene_labels\n'
                                        '    from .contexts_battle import BattleSceneContext\n'
                                        '    upload_battle_scene_labels(memory.state, '
                                        'BattleSceneContext(entered.target_x, entered.target_y, '
                                        'entered.unit, replace_word(entered.count, 65535)))\n'
                                        '    result = FirstDeploymentFrame.unobserved()\n'
                                        'else:\n'
                                        '    result = memory.state.service_at(target, entered)\n'
                                        '    if type(result) is not FirstDeploymentFrame:\n'
                                        '        raise SceneRefreshBoundary(target, entered, continuation)\n'
                                        '_scene_refresh_frame(memory, result)\n'
                                        'if frame.stack_cursor is not None:\n'
                                        '    if result.stack_cursor is None:\n'
                                        '        raise SceneRefreshBoundary(target, result, continuation)\n'
                                        '    memory.sync_status(result)\n'
                                        '    actual = result.stack_cursor.long()\n'
                                        '    if actual != continuation:\n'
                                        '        raise SceneRefreshBoundary(target, result, continuation)\n'
                                        '    result = first_replace(result, '
                                        'stack_cursor=result.stack_cursor.advance(4))\n'
                                        'return memory.sync_status(result)'},
 '_scene_refresh_decrement': {'signature': 'frame: FirstDeploymentFrame, name, counter: Word',
                              'returns': 'FirstDeploymentFrame',
                              'flow': 'uint(counter, 16)\n'
                                      'retained = frame.carrier(name)\n'
                                      'return first_replace(frame, **{name: None if retained is None else '
                                      'replace_word(retained, u16(counter - 1))})'},
 '_scene_refresh_emit': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, address, '
                                      'size, value',
                         'returns': 'FirstDeploymentFrame',
                         'flow': 'memory.sync_status(frame)\n'
                                 'memory.state.write(address, size, value)\n'
                                 'return _scene_refresh_flags(memory, frame, value, size)'},
 '_scene_refresh_flags': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, value, size',
                          'returns': 'FirstDeploymentFrame',
                          'flow': 'if size not in (1, 2, 4):\n'
                                  "    raise ValueError('original scene DATA width required')\n"
                                  'uint(value, size * 8)\n'
                                  'sign = 1 << size * 8 - 1\n'
                                  'status = None if frame.status is None else frame.status & 16 | (8 if '
                                  'value & sign else 0) | (4 if value == 0 else 0)\n'
                                  'return memory.sync_status(first_replace(frame, status=status))'},
 '_scene_refresh_frame': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                          'returns': 'FirstDeploymentFrame',
                          'flow': 'if type(memory) is not SceneRefreshMemory:\n'
                                  "    raise ValueError('sealed same-state scene refresh memory required')\n"
                                  'return memory.frame(frame)'},
 '_scene_refresh_repeat_pixels': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                               'name, counter: Word, value: Long',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': 'frame = _first_word(frame, name, counter)\n'
                                          'while True:\n'
                                          '    frame = _scene_refresh_emit(memory, frame, 12582912, 4, '
                                          'value)\n'
                                          '    frame = _scene_refresh_decrement(frame, name, counter)\n'
                                          '    counter = u16(counter - 1)\n'
                                          '    if counter == 65535:\n'
                                          '        return frame'},
 'clear_overlay_frame': {'signature': 'state: GameplayState',
                         'returns': 'Long',
                         'flow': 'checked_state(state)\n'
                                 'return clear_overlay_frame_fields(SceneRefreshMemory(state), '
                                 'FirstDeploymentFrame.unobserved()).target_x'},
 'clear_overlay_frame_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                'returns': 'FirstDeploymentFrame',
                                'flow': '_scene_refresh_frame(memory, frame)\n'
                                        "frame = _first_long(frame, 'target_x', 1090781187)\n"
                                        "frame = _first_word(frame, 'target_y', 13)\n"
                                        'counter = 13\n'
                                        'while True:\n'
                                        '    frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                        'frame.target_x)\n'
                                        "    frame = _scene_refresh_repeat_pixels(memory, frame, 'unit', 9, "
                                        '0)\n'
                                        '    frame = _scene_refresh_advance_command(memory, frame)\n'
                                        "    frame = _scene_refresh_decrement(frame, 'target_y', counter)\n"
                                        '    counter = u16(counter - 1)\n'
                                        '    if counter == 65535:\n'
                                        '        return frame'},
 'draw_overlay_frame': {'signature': 'state: GameplayState',
                        'returns': 'None',
                        'flow': 'checked_state(state)\n'
                                'draw_overlay_frame_fields(SceneRefreshMemory(state), '
                                'FirstDeploymentFrame.unobserved())'},
 'draw_overlay_frame_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                               'returns': 'FirstDeploymentFrame',
                               'flow': '_scene_refresh_frame(memory, frame)\n'
                                       'frame = _scene_refresh_emit(memory, frame, 12582916, 4, 1912602625)\n'
                                       "frame = _scene_refresh_repeat_pixels(memory, frame, 'target_x', 7, "
                                       '858993459)\n'
                                       'frame = first_replace(frame, roster=memory.cursor_at(565436))\n'
                                       "frame = _first_word(frame, 'target_x', 63)\n"
                                       'counter = 63\n'
                                       'while True:\n'
                                       '    memory.sync_status(frame)\n'
                                       '    source = frame.roster\n'
                                       '    value = source.long()\n'
                                       '    frame = first_replace(frame, roster=source.advance(4))\n'
                                       '    frame = _scene_refresh_emit(memory, frame, 12582912, 4, value)\n'
                                       "    frame = _scene_refresh_decrement(frame, 'target_x', counter)\n"
                                       '    counter = u16(counter - 1)\n'
                                       '    if counter == 65535:\n'
                                       '        break\n'
                                       "frame = _first_long(frame, 'target_x', 1090781187)\n"
                                       'frame = _scene_refresh_call_fields(memory, frame, 67810, 67792)\n'
                                       "frame = _first_word(frame, 'unit', 9)\n"
                                       'counter = 9\n'
                                       'while True:\n'
                                       '    frame = _scene_refresh_call_fields(memory, frame, 67902, 67800)\n'
                                       "    frame = _scene_refresh_decrement(frame, 'unit', counter)\n"
                                       '    counter = u16(counter - 1)\n'
                                       '    if counter == 65535:\n'
                                       '        break\n'
                                       'return _scene_refresh_call_fields(memory, frame, 67954, 67808)'},
 'draw_overlay_frame_footer': {'signature': 'state: GameplayState, command: Long',
                               'returns': 'Long',
                               'flow': 'checked_state(state)\n'
                                       'uint(command, 32)\n'
                                       'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                       'target_x=command)\n'
                                       'return draw_overlay_frame_footer_fields(SceneRefreshMemory(state), '
                                       'frame).target_x'},
 'draw_overlay_frame_footer_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                      'returns': 'FirstDeploymentFrame',
                                      'flow': '_scene_refresh_frame(memory, frame)\n'
                                              'frame = _scene_refresh_advance_command(memory, frame)\n'
                                              'frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                              'frame.target_x)\n'
                                              'frame = _scene_refresh_emit(memory, frame, 12582912, 4, '
                                              '3281245080)\n'
                                              'frame = _scene_refresh_repeat_pixels(memory, frame, '
                                              "'target_y', 7, 3684031381)\n"
                                              'frame = _scene_refresh_emit(memory, frame, 12582912, 4, '
                                              '3683965843)\n'
                                              'frame = _scene_refresh_advance_command(memory, frame)\n'
                                              'frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                              'frame.target_x)\n'
                                              'frame = _scene_refresh_emit(memory, frame, 12582912, 4, '
                                              '3549944722)\n'
                                              'frame = _scene_refresh_repeat_pixels(memory, frame, '
                                              "'target_y', 7, 3683834770)\n"
                                              'return _scene_refresh_emit(memory, frame, 12582912, 4, '
                                              '3683834769)'},
 'draw_overlay_frame_header': {'signature': 'state: GameplayState, command: Long',
                               'returns': 'Long',
                               'flow': 'checked_state(state)\n'
                                       'uint(command, 32)\n'
                                       'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                       'target_x=command)\n'
                                       'return draw_overlay_frame_header_fields(SceneRefreshMemory(state), '
                                       'frame).target_x'},
 'draw_overlay_frame_header_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                      'returns': 'FirstDeploymentFrame',
                                      'flow': '_scene_refresh_frame(memory, frame)\n'
                                              'frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                              'frame.target_x)\n'
                                              'frame = _scene_refresh_emit(memory, frame, 12582912, 2, '
                                              '50065)\n'
                                              'frame = _scene_refresh_repeat_pixels(memory, frame, '
                                              "'target_y', 8, 3281175442)\n"
                                              'frame = _scene_refresh_emit(memory, frame, 12582912, 2, '
                                              '52119)\n'
                                              'frame = _scene_refresh_advance_command(memory, frame)\n'
                                              'frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                              'frame.target_x)\n'
                                              'frame = _scene_refresh_emit(memory, frame, 12582912, 4, '
                                              '3281240980)\n'
                                              'frame = _scene_refresh_repeat_pixels(memory, frame, '
                                              "'target_y', 7, 3281372053)\n"
                                              'return _scene_refresh_emit(memory, frame, 12582912, 4, '
                                              '3415792531)'},
 'draw_overlay_frame_middle': {'signature': 'state: GameplayState, command: Long',
                               'returns': 'Long',
                               'flow': 'checked_state(state)\n'
                                       'uint(command, 32)\n'
                                       'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                       'target_x=command)\n'
                                       'return draw_overlay_frame_middle_fields(SceneRefreshMemory(state), '
                                       'frame).target_x'},
 'draw_overlay_frame_middle_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                      'returns': 'FirstDeploymentFrame',
                                      'flow': '_scene_refresh_frame(memory, frame)\n'
                                              'frame = _scene_refresh_advance_command(memory, frame)\n'
                                              'frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                              'frame.target_x)\n'
                                              'frame = _scene_refresh_emit(memory, frame, 12582912, 4, '
                                              '3281240982)\n'
                                              'frame = _scene_refresh_repeat_pixels(memory, frame, '
                                              "'target_y', 7, 1133527952)\n"
                                              'return _scene_refresh_emit(memory, frame, 12582912, 4, '
                                              '3684096915)'},
 'enqueue_sound_command': {'signature': 'state: GameplayState, command: Byte',
                           'returns': 'None',
                           'flow': 'checked_state(state)\n'
                                   'enqueue_sound_command_fields(SceneRefreshMemory(state), '
                                   'FirstDeploymentFrame.unobserved(), command)'},
 'enqueue_sound_command_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                               'command: Byte | None=None',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': "_scene_refresh_frame(memory, frame)\nif command is None:\n    if frame.target_x is None:\n        raise SceneRefreshBoundary(32906, frame, None)\n    command = low8(frame.target_x)\nuint(command, 8)\nmemory.sync_status(frame)\nmemory.state.read(16727808, 1)\nmemory.state.write(16727808, 1, 255)\nframe = _scene_refresh_emit(memory, frame, 10555648, 2, 256)\nwhile True:\n    value = memory.state.read(10555648, 1)\n    status = None if frame.status is None else frame.status & 27 | (0 if value & 1 else 4)\n    frame = memory.sync_status(first_replace(frame, status=status))\n    if not value & 1:\n        break\n    memory.state.progress('sound-bus-acquire')\nvalue = memory.state.read(10492938, 1)\nframe = _scene_refresh_flags(memory, frame, value, 1)\nif value == 0:\n    frame = _scene_refresh_emit(memory, frame, 10492938, 1, command)\nelse:\n    value = memory.state.read(10492939, 1)\n    frame = _scene_refresh_flags(memory, frame, value, 1)\n    if value == 0:\n        frame = _scene_refresh_emit(memory, frame, 10492939, 1, command)\nmemory.state.read(16727808, 1)\nmemory.state.write(16727808, 1, 0)\nreturn _scene_refresh_emit(memory, frame, 10555648, 2, 0)"},
 'load_gameplay_scene': {'signature': 'state: GameplayState',
                         'returns': 'None',
                         'flow': 'checked_state(state)\n'
                                 'load_gameplay_scene_fields(SceneRefreshMemory(state), '
                                 'FirstDeploymentFrame.unobserved())'},
 'load_gameplay_scene_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                'returns': 'FirstDeploymentFrame',
                                'flow': '_scene_refresh_frame(memory, frame)\n'
                                        'memory.sync_status(frame)\n'
                                        'value = memory.state.read(4294963158, 2)\n'
                                        'frame = _scene_refresh_flags(memory, frame, value, 2)\n'
                                        'if value != 0:\n'
                                        "    frame = _first_long(frame, 'target_x', 1048576)\n"
                                        "    frame = _scene_refresh_decrement(frame, 'target_x', 0)\n"
                                        '    return _scene_refresh_emit(memory, frame, 16740390, 2, 65535)\n'
                                        'saved_sound = memory.state.read(4294964754, 2)\n'
                                        'if frame.stack_cursor is not None:\n'
                                        '    stack = frame.stack_cursor.advance(-2)\n'
                                        '    stack.set_word(0, saved_sound)\n'
                                        '    frame = first_replace(frame, stack_cursor=stack)\n'
                                        'frame = _scene_refresh_flags(memory, frame, saved_sound, 2)\n'
                                        'frame = _scene_refresh_bit_clear(memory, frame, 4294964133, 2)\n'
                                        'frame = _scene_refresh_call_fields(memory, frame, 18966, 67396)\n'
                                        'frame = _scene_refresh_emit(memory, frame, 4294964754, 2, 2304)\n'
                                        'frame = _scene_refresh_call_fields(memory, frame, 44872, 67408)\n'
                                        'frame = _scene_refresh_call_fields(memory, frame, 33736, 67414)\n'
                                        'frame = memory.status_word(frame, 9984)\n'
                                        'frame = _scene_refresh_call_fields(memory, frame, 67604, 67422)\n'
                                        'frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                        '1082392579)\n'
                                        "frame = _scene_refresh_repeat_pixels(memory, frame, 'target_x', 5, "
                                        '0)\n'
                                        'frame = _scene_refresh_call_fields(memory, frame, 67734, 67454)\n'
                                        'frame = _scene_refresh_call_fields(memory, frame, 235162, 67460)\n'
                                        'frame = memory.status_word(frame, 9984)\n'
                                        'frame = _scene_refresh_call_fields(memory, frame, 68056, 67468)\n'
                                        'frame = _scene_refresh_emit(memory, frame, 16740390, 2, 65535)\n'
                                        'frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                        '1075838976)\n'
                                        "frame = _scene_refresh_repeat_pixels(memory, frame, 'target_x', 7, "
                                        '286331153)\n'
                                        'frame = _scene_refresh_emit(memory, frame, 4294964094, 2, 0)\n'
                                        'if frame.stack_cursor is not None:\n'
                                        '    memory.sync_status(frame)\n'
                                        '    saved_sound = frame.stack_cursor.word()\n'
                                        '    frame = first_replace(frame, '
                                        'stack_cursor=frame.stack_cursor.advance(2))\n'
                                        'frame = _scene_refresh_emit(memory, frame, 4294964754, 2, '
                                        'saved_sound)\n'
                                        'frame = _scene_refresh_bit_clear(memory, frame, 4294964132, 3)\n'
                                        'frame = _scene_refresh_emit(memory, frame, 4294963144, 4, 0)\n'
                                        'frame = _scene_refresh_emit(memory, frame, 4294963148, 4, 0)\n'
                                        'frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                        '2013265922)\n'
                                        'frame = _scene_refresh_emit(memory, frame, 12582912, 4, 0)\n'
                                        'frame = _scene_refresh_emit(memory, frame, 12582912, 4, 0)\n'
                                        'frame = _scene_refresh_call_fields(memory, frame, 67712, 67560)\n'
                                        'value = memory.state.read(4294964932, 2)\n'
                                        'frame = _first_compare_word(frame, value, 1)\n'
                                        'if value == 1:\n'
                                        '    frame = _scene_refresh_call_fields(memory, frame, 96190, '
                                        '67576)\n'
                                        'return memory.sync_status(frame)'},
 'refresh_gameplay_scene': {'signature': 'state: GameplayState, retained: Long=0',
                            'returns': 'Long',
                            'flow': 'checked_state(state)\n'
                                    'uint(retained, 32)\n'
                                    'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                    'target_x=retained)\n'
                                    'return refresh_gameplay_scene_fields(SceneRefreshMemory(state), '
                                    'frame).target_x'},
 'refresh_gameplay_scene_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': '_scene_refresh_frame(memory, frame)\n'
                                           "for edge in ('vblank-end', 'vblank-start'):\n"
                                           '    while True:\n'
                                           '        memory.sync_status(frame)\n'
                                           '        value = memory.state.read(12582916, 2)\n'
                                           "        frame = _first_word(frame, 'target_x', value)\n"
                                           '        status = None if frame.status is None else frame.status '
                                           '& 27 | (0 if value & 8 else 4)\n'
                                           '        frame = memory.sync_status(first_replace(frame, '
                                           'status=status))\n'
                                           "        if edge == 'vblank-end' and (not value & 8) or (edge == "
                                           "'vblank-start' and value & 8):\n"
                                           '            break\n'
                                           '        memory.state.progress(edge)\n'
                                           'return frame'},
 'resume_pending_sound': {'signature': 'state: GameplayState, retained: Long=0',
                          'returns': 'Long',
                          'flow': 'checked_state(state)\n'
                                  'uint(retained, 32)\n'
                                  'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                  'target_x=retained)\n'
                                  'return resume_pending_sound_fields(SceneRefreshMemory(state), '
                                  'frame).target_x'},
 'resume_pending_sound_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                 'returns': 'FirstDeploymentFrame',
                                 'flow': '_scene_refresh_frame(memory, frame)\n'
                                         'value = memory.state.read(4294963152, 2)\n'
                                         'frame = _scene_refresh_flags(memory, frame, value, 2)\n'
                                         'if not negative_word(value):\n'
                                         "    frame = _first_word(frame, 'target_x', 0)\n"
                                         '    memory.sync_status(frame)\n'
                                         '    command = memory.state.read(4294965092, 1)\n'
                                         "    frame = _first_byte(frame, 'target_x', command)\n"
                                         '    frame = _scene_refresh_call_fields(memory, frame, 32906, '
                                         '67732, command)\n'
                                         'return memory.sync_status(frame)'},
 'select_sound_command_from_scene': {'signature': 'state: GameplayState',
                                     'returns': 'Word',
                                     'flow': 'checked_state(state)\n'
                                             'return '
                                             'select_sound_command_from_scene_fields(SceneRefreshMemory(state), '
                                             'FirstDeploymentFrame.unobserved()).command'},
 'select_sound_command_from_scene_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                         'FirstDeploymentFrame',
                                            'returns': 'SceneSoundSelectionFields',
                                            'flow': '_scene_refresh_frame(memory, frame)\n'
                                                    'value = memory.state.read(16740390, 2)\n'
                                                    "frame = _first_word(frame, 'target_x', value)\n"
                                                    "frame = _first_shift_word(frame, 'target_x', value, 1)\n"
                                                    'memory.sync_status(frame)\n'
                                                    'command = memory.cursor_at(67632, u16(value << '
                                                    '1)).word()\n'
                                                    "frame = _first_word(frame, 'target_x', command)\n"
                                                    'frame = _scene_refresh_emit(memory, frame, 4294963152, '
                                                    '2, command)\n'
                                                    'if not negative_word(command):\n'
                                                    '    frame = _scene_refresh_call_fields(memory, frame, '
                                                    '32906, 67630, low8(command))\n'
                                                    'return SceneSoundSelectionFields(frame, command)'},
 'wait_for_scene_sound_byte': {'signature': 'state: GameplayState',
                               'returns': 'None',
                               'flow': 'checked_state(state)\n'
                                       'wait_for_scene_sound_byte_fields(SceneRefreshMemory(state), '
                                       'FirstDeploymentFrame.unobserved())'},
 'wait_for_scene_sound_byte_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                      'returns': 'FirstDeploymentFrame',
                                      'flow': '_scene_refresh_frame(memory, frame)\n'
                                              'frame = memory.status_word(frame, 9472)\n'
                                              'while True:\n'
                                              '    value = memory.state.read(4294964754, 1)\n'
                                              '    frame = _scene_refresh_flags(memory, frame, value, 1)\n'
                                              '    if value == 0:\n'
                                              '        return frame\n'
                                              "    memory.state.progress('scene-sound-byte')"}})


# Entire sole _gameplay_message_call_fields current body.
DECLARATIONS.update({'_gameplay_message_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_refresh_frame(memory, frame)\nif (target, continuation) not in ((44872, 199308), (1548, 199334)):\n    raise ValueError('original gameplay message child and token required')\nentered = memory.sync_status(frame)\nif frame.stack_cursor is not None:\n    stack = frame.stack_cursor.advance(-4)\n    stack.set_long(0, continuation)\n    entered = first_replace(frame, stack_cursor=stack)\nif target == 44872:\n    returned = refresh_gameplay_scene_fields(memory, entered)\nelif entered.stack_cursor is None:\n    clear_scene_video_and_state(memory.state)\n    returned = first_replace(entered, status=None)\nelse:\n    raise SceneRefreshBoundary(target, entered, continuation)\nreturned = _scene_refresh_frame(memory, returned)\nmemory.sync_status(returned)\nif frame.stack_cursor is not None:\n    actual = returned.stack_cursor.long()\n    if actual != continuation:\n        raise SceneRefreshBoundary(actual, returned, continuation)\n    returned = first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))\nreturn returned"}})


# Entire sole present_gameplay_message current body.
DECLARATIONS.update({'present_gameplay_message': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\npresent_gameplay_message_fields(SceneRefreshMemory(state), FirstDeploymentFrame.unobserved())'}})


# Entire sole present_gameplay_message_fields current body.
DECLARATIONS.update({'present_gameplay_message_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_refresh_frame(memory, frame)\nsaved = []\nfor address in (4294964754, 4294964066):\n    memory.sync_status(frame)\n    value = memory.state.read(address, 2)\n    saved.append(value)\n    if frame.stack_cursor is not None:\n        stack = frame.stack_cursor.advance(-2)\n        stack.set_word(0, value)\n        frame = first_replace(frame, stack_cursor=stack)\n    frame = _scene_refresh_flags(memory, frame, value, 2)\nframe = _scene_refresh_emit(memory, frame, 4294964754, 2, 523)\nmemory.state.read(4294964736, 2)\nframe = _scene_refresh_emit(memory, frame, 4294964736, 2, 0)\nframe = _gameplay_message_call_fields(memory, frame, 44872, 199308)\nframe = memory.status_word(frame, 9472)\nwhile True:\n    while True:\n        memory.sync_status(frame)\n        command = memory.state.read(4294964736, 2)\n        frame = _scene_refresh_flags(memory, frame, command, 2)\n        if command:\n            break\n        if frame.stack_cursor is not None:\n            raise SceneRefreshBoundary(199312, frame, None)\n        memory.state.progress('message-scene')\n    command = memory.state.read(4294964736, 2)\n    frame = _first_compare_word(frame, command, 40)\n    memory.sync_status(frame)\n    if command != 40:\n        break\n    frame = _gameplay_message_call_fields(memory, frame, 1548, 199334)\n    memory.state.read(4294964736, 2)\n    frame = _scene_refresh_emit(memory, frame, 4294964736, 2, 0)\n    frame = memory.status_word(frame, 9472)\nframe = memory.status_word(frame, 9984)\nfor address, legacy_value in ((4294964066, saved[1]), (4294964754, saved[0])):\n    if frame.stack_cursor is None:\n        value = legacy_value\n    else:\n        value = frame.stack_cursor.word()\n        frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))\n    frame = _scene_refresh_emit(memory, frame, address, 2, value)\nreturn memory.sync_status(frame)"}})


# Entire sole B19 child bridge; actual 10784 slot belongs to its parent.
DECLARATIONS.update({'_scene_refresh_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long, command: Byte | None=None', 'returns': 'FirstDeploymentFrame', 'flow': "_scene_refresh_frame(memory, frame)\nif (target, continuation) not in ((18966, 67396), (44872, 67408), (33736, 67414), (67604, 67422), (67734, 67454), (235162, 67460), (68056, 67468), (67712, 67560), (96190, 67576), (32906, 67630), (32906, 67732), (67810, 67792), (67902, 67800), (67954, 67808)):\n    raise ValueError('actual closed scene refresh child and token required')\nif command is not None and target != 32906:\n    raise ValueError('only sound mailbox has an observed BYTE argument')\nentered = memory.sync_status(frame)\nif frame.stack_cursor is not None:\n    stack = frame.stack_cursor.advance(-4)\n    stack.set_long(0, continuation)\n    entered = first_replace(frame, stack_cursor=stack)\nif target == 18966:\n    _reset_scene_input_marker_fields(MarkerResetMemory(memory.state))\n    result = _scene_refresh_flags(memory, entered, 0, 2)\nelif target == 44872:\n    result = refresh_gameplay_scene_fields(memory, entered)\nelif target == 33736:\n    result = wait_for_scene_sound_byte_fields(memory, entered)\nelif target == 67604:\n    result = select_sound_command_from_scene_fields(memory, entered).frame\nelif target == 67734:\n    result = draw_overlay_frame_fields(memory, entered)\nelif target == 68056:\n    result = clear_overlay_frame_fields(memory, entered)\nelif target == 67712:\n    result = resume_pending_sound_fields(memory, entered)\nelif target == 32906:\n    result = enqueue_sound_command_fields(memory, entered, command)\nelif target == 67810:\n    result = draw_overlay_frame_header_fields(memory, entered)\nelif target == 67902:\n    result = draw_overlay_frame_middle_fields(memory, entered)\nelif target == 67954:\n    result = draw_overlay_frame_footer_fields(memory, entered)\nelif target == 235162 and entered.stack_cursor is not None:\n    from ..high_level_scene_flows.business_scene import play_scripted_scene_fields\n    result = play_scripted_scene_fields(memory.state, entered)\nelif target == 235162 and entered.stack_cursor is None:\n    observed = memory.state.service_at(target, SceneDisplayContext())\n    if type(observed) is not SceneDisplayResult:\n        raise Boundary('legacy renderer requires its real retained output observations')\n    observed.__post_init__()\n    result = first_replace(entered, target_y=observed.foreground, unit=observed.glyph_count, count=observed.training_carrier, status=None)\nelif target == 96190 and entered.stack_cursor is None:\n    from .business_battle import upload_battle_scene_labels\n    from .contexts_battle import BattleSceneContext\n    upload_battle_scene_labels(memory.state, BattleSceneContext(entered.target_x, entered.target_y, entered.unit, replace_word(entered.count, 65535)))\n    result = FirstDeploymentFrame.unobserved()\nelse:\n    result = memory.state.service_at(target, entered)\n    if type(result) is not FirstDeploymentFrame:\n        raise SceneRefreshBoundary(target, entered, continuation)\n_scene_refresh_frame(memory, result)\nif frame.stack_cursor is not None:\n    if result.stack_cursor is None:\n        raise SceneRefreshBoundary(target, result, continuation)\n    memory.sync_status(result)\n    actual = result.stack_cursor.long()\n    if actual != continuation:\n        raise SceneRefreshBoundary(target, result, continuation)\n    result = first_replace(result, stack_cursor=result.stack_cursor.advance(4))\nreturn memory.sync_status(result)"}})
APPROVED.setdefault('business_scene',set()).update({'play_scripted_scene_fields'})


# Entire current sole stage_sprite_word_packet body.
DECLARATIONS.update({'stage_sprite_word_packet': {'signature': 'state: GameplayState, source: Cursor, command: Long, rows: Word, row_command: Word', 'returns': 'Long', 'flow': 'checked_state(state)\nchecked_cursor(source, state)\nuint(command, 32)\nuint(rows, 16)\nuint(row_command, 16)\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=source, target_x=command)\nreturn stage_sprite_word_packet_fields(SceneRefreshMemory(state), frame).target_x'}})


# Entire current sole stage_sprite_word_packet_fields body.
DECLARATIONS.update({'stage_sprite_word_packet_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_scene_flows.domain import SceneState\nfrom ..high_level_main_flows.business_movement_support import _movement_binary_flags\nfrom ..high_level_battle_ai.business_formation import _first_sub_word, _first_memory_word, _first_right_word\nframe = _scene_refresh_frame(memory, frame)\nif type(memory.state) is not SceneState or any((value is None for value in (frame.target_x, frame.target_y, frame.unit, frame.count, frame.distance, frame.offset_x, frame.offset_y, frame.choice, frame.roster, frame.candidates, frame.controller, frame.scan, frame.opponent, frame.scratch, frame.auxiliary, frame.stack_cursor, frame.status))):\n    raise SceneRefreshBoundary(158714, frame, None)\nframe.validate(memory.state, True)\ndestination = memory.cursor_at(4294955264)\nframe = first_replace(frame, candidates=destination)\nqueued = memory.state.read(4294963994, 2)\ndestination = destination.advance(s16(queued))\nframe = first_replace(frame, candidates=destination)\nrows = low16(frame.target_y)\nframe = _first_word(frame, 'choice', rows)\nframe = _first_sub_word(frame, 'choice', rows, 1)\nfor counter in descending_inclusive(u16(rows - 1)):\n    destination.set_word(0, low16(frame.target_x))\n    destination = destination.advance(2)\n    frame = first_replace(frame, candidates=destination)\n    frame = _first_memory_word(frame, low16(frame.target_x))\n    destination.set_word(0, low16(frame.unit))\n    destination = destination.advance(2)\n    frame = first_replace(frame, candidates=destination)\n    frame = _first_memory_word(frame, low16(frame.unit))\n    from ..high_level_battle_ai.business_formation import _first_add_word\n    frame = _first_add_word(frame, 'unit', low16(frame.unit), 128)\n    frame = _first_word(frame, 'count', low16(frame.target_x))\n    while True:\n        token = frame.roster.word()\n        frame = first_replace(frame, roster=frame.roster.advance(2))\n        frame = _first_word(frame, 'distance', token)\n        if negative_word(token):\n            frame = _first_word(frame, 'offset_x', low16(frame.distance))\n            frame = _first_word(frame, 'distance', low16(frame.distance) & 32767)\n            frame = _first_right_word(frame, 'distance', low16(frame.distance), 7)\n            before = frame.distance\n            frame = first_replace(frame, distance=before & 4294967294, status=frame.status & 27 | (0 if before & 1 else 4))\n            relative = memory.state.table(158796).word(low16(frame.distance))\n            frame = _first_word(frame, 'distance', relative)\n            target = u32(158808 + s16(relative))\n            stack = frame.stack_cursor.advance(-4)\n            stack.set_long(0, 158774)\n            entered = first_replace(frame, stack_cursor=stack)\n            memory.sync_status(entered)\n            raise SceneRefreshBoundary(target, entered, 158774)\n        frame = _first_long(frame, 'target_x', swap_words(frame.target_x))\n        frame = _first_word(frame, 'distance', low16(frame.distance) | low16(frame.target_x))\n        destination.set_word(0, low16(frame.distance))\n        destination = destination.advance(2)\n        frame = first_replace(frame, candidates=destination)\n        frame = _first_memory_word(frame, low16(frame.distance))\n        frame = _first_long(frame, 'target_x', swap_words(frame.target_x))\n        frame = _first_sub_word(frame, 'count', low16(frame.count), 1)\n        frame = _first_memory_word(frame, low16(frame.count))\n        if low16(frame.count) == 0:\n            break\n    frame = first_replace(frame, choice=replace_word(frame.choice, u16(counter - 1)))\ndestination.word()\ndestination.set_word(0, 0)\nframe = _first_memory_word(frame, 0)\nframe = _first_add_word(frame, 'target_x', low16(frame.target_x), 2)\nframe = _first_long(frame, 'target_x', low16(frame.target_x) * low16(frame.target_y))\nframe = _first_shift_word(frame, 'target_x', low16(frame.target_x), 1)\nprevious = memory.state.read(4294963994, 2)\nframe, value = _movement_binary_flags(memory.state, frame, previous, low16(frame.target_x), 16)\nmemory.state.write(4294963994, 2, value)\nmemory.sync_status(frame)\nreturn memory.frame(frame)"}})

APPROVED.setdefault('domain',set()).update({'SceneState'})

APPROVED.setdefault('business_movement_support',set()).update({'_movement_binary_flags'})

APPROVED.setdefault('business_formation',set()).update({'_first_right_word', '_first_memory_word', '_first_sub_word', '_first_add_word'})

DECLARATIONS.update({'_word_packet_copy_run_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, increasing: bool', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_scene_flows.domain import SceneState\nfrom ..high_level_battle_ai.business_formation import _first_sub_word, _first_add_word, _first_memory_word\nif type(increasing) is not bool:\n    raise ValueError('actual repeated or ascending word control required')\nframe = _scene_refresh_frame(memory, frame)\nentry = 158834 if increasing else 158808\nif type(memory.state) is not SceneState or any((value is None for value in (frame.target_x, frame.target_y, frame.unit, frame.count, frame.distance, frame.offset_x, frame.offset_y, frame.choice, frame.roster, frame.candidates, frame.controller, frame.scan, frame.opponent, frame.scratch, frame.auxiliary, frame.stack_cursor, frame.status))):\n    raise SceneRefreshBoundary(entry, frame, None)\nframe.validate(memory.state, True)\nframe = _first_word(frame, 'offset_x', low16(frame.offset_x) & 255)\nframe = _first_long(frame, 'target_x', swap_words(frame.target_x))\ntoken = frame.roster.word()\nframe = first_replace(frame, roster=frame.roster.advance(2))\nframe = _first_word(frame, 'distance', token)\nframe = _first_word(frame, 'distance', low16(frame.distance) | low16(frame.target_x))\ncount = low16(frame.offset_x)\nframe = _first_word(frame, 'offset_y', count)\nframe = _first_sub_word(frame, 'offset_y', count, 1)\nfor counter in descending_inclusive(u16(count - 1)):\n    frame.candidates.set_word(0, low16(frame.distance))\n    frame = first_replace(frame, candidates=frame.candidates.advance(2))\n    frame = _first_memory_word(frame, low16(frame.distance))\n    if increasing:\n        frame = _first_add_word(frame, 'distance', low16(frame.distance), 2)\n    frame = first_replace(frame, offset_y=replace_word(frame.offset_y, u16(counter - 1)))\nframe = _first_sub_word(frame, 'count', low16(frame.count), low16(frame.offset_x))\nframe = _first_long(frame, 'target_x', swap_words(frame.target_x))\nreturn memory.sync_status(frame)"}})

DECLARATIONS.update({'increment_word_packet_control_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _word_packet_copy_run_fields(memory, frame, True)'}})

DECLARATIONS.update({'repeat_word_packet_control_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _word_packet_copy_run_fields(memory, frame, False)'}})

DECLARATIONS.update({'stage_sprite_word_packet_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_scene_flows.domain import SceneState\nfrom ..high_level_main_flows.business_movement_support import _movement_binary_flags\nfrom ..high_level_battle_ai.business_formation import _first_sub_word, _first_memory_word, _first_right_word\nframe = _scene_refresh_frame(memory, frame)\nif type(memory.state) is not SceneState or any((value is None for value in (frame.target_x, frame.target_y, frame.unit, frame.count, frame.distance, frame.offset_x, frame.offset_y, frame.choice, frame.roster, frame.candidates, frame.controller, frame.scan, frame.opponent, frame.scratch, frame.auxiliary, frame.stack_cursor, frame.status))):\n    raise SceneRefreshBoundary(158714, frame, None)\nframe.validate(memory.state, True)\ndestination = memory.cursor_at(4294955264)\nframe = first_replace(frame, candidates=destination)\nqueued = memory.state.read(4294963994, 2)\ndestination = destination.advance(s16(queued))\nframe = first_replace(frame, candidates=destination)\nrows = low16(frame.target_y)\nframe = _first_word(frame, 'choice', rows)\nframe = _first_sub_word(frame, 'choice', rows, 1)\nfor counter in descending_inclusive(u16(rows - 1)):\n    destination.set_word(0, low16(frame.target_x))\n    destination = destination.advance(2)\n    frame = first_replace(frame, candidates=destination)\n    frame = _first_memory_word(frame, low16(frame.target_x))\n    destination.set_word(0, low16(frame.unit))\n    destination = destination.advance(2)\n    frame = first_replace(frame, candidates=destination)\n    frame = _first_memory_word(frame, low16(frame.unit))\n    from ..high_level_battle_ai.business_formation import _first_add_word\n    frame = _first_add_word(frame, 'unit', low16(frame.unit), 128)\n    frame = _first_word(frame, 'count', low16(frame.target_x))\n    while True:\n        token = frame.roster.word()\n        frame = first_replace(frame, roster=frame.roster.advance(2))\n        frame = _first_word(frame, 'distance', token)\n        if negative_word(token):\n            frame = _first_word(frame, 'offset_x', low16(frame.distance))\n            frame = _first_word(frame, 'distance', low16(frame.distance) & 32767)\n            frame = _first_right_word(frame, 'distance', low16(frame.distance), 7)\n            before = frame.distance\n            frame = first_replace(frame, distance=before & 4294967294, status=frame.status & 27 | (0 if before & 1 else 4))\n            relative = memory.state.table(158796).word(low16(frame.distance))\n            frame = _first_word(frame, 'distance', relative)\n            target = u32(158808 + s16(relative))\n            stack = frame.stack_cursor.advance(-4)\n            stack.set_long(0, 158774)\n            entered = first_replace(frame, stack_cursor=stack)\n            memory.sync_status(entered)\n            if target == 158808:\n                frame = repeat_word_packet_control_fields(memory, entered)\n            elif target == 158834:\n                frame = increment_word_packet_control_fields(memory, entered)\n            else:\n                raise SceneRefreshBoundary(target, entered, 158774)\n            actual = frame.stack_cursor.long()\n            if actual != 158774:\n                raise SceneRefreshBoundary(actual, frame, 158774)\n            frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(4))\n            frame = _first_memory_word(frame, low16(frame.count))\n            if low16(frame.count) == 0:\n                break\n            continue\n        frame = _first_long(frame, 'target_x', swap_words(frame.target_x))\n        frame = _first_word(frame, 'distance', low16(frame.distance) | low16(frame.target_x))\n        destination.set_word(0, low16(frame.distance))\n        destination = destination.advance(2)\n        frame = first_replace(frame, candidates=destination)\n        frame = _first_memory_word(frame, low16(frame.distance))\n        frame = _first_long(frame, 'target_x', swap_words(frame.target_x))\n        frame = _first_sub_word(frame, 'count', low16(frame.count), 1)\n        frame = _first_memory_word(frame, low16(frame.count))\n        if low16(frame.count) == 0:\n            break\n    frame = first_replace(frame, choice=replace_word(frame.choice, u16(counter - 1)))\ndestination.word()\ndestination.set_word(0, 0)\nframe = _first_memory_word(frame, 0)\nframe = _first_add_word(frame, 'target_x', low16(frame.target_x), 2)\nframe = _first_long(frame, 'target_x', low16(frame.target_x) * low16(frame.target_y))\nframe = _first_shift_word(frame, 'target_x', low16(frame.target_x), 1)\nprevious = memory.state.read(4294963994, 2)\nframe, value = _movement_binary_flags(memory.state, frame, previous, low16(frame.target_x), 16)\nmemory.state.write(4294963994, 2, value)\nmemory.sync_status(frame)\nreturn memory.frame(frame)"}})

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
APPROVED.setdefault('business_scene',set()).update({'play_scripted_scene_fields', 'expand_glyph_stream_fields', 'expand_glyph_row_fields'})
APPROVED.setdefault('business_battle',set()).update({'upload_battle_scene_labels_fields'})
DECLARATIONS.update({'_scene_refresh_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                             'target: Long, continuation: Long, command: Byte | None=None',
                                'returns': 'FirstDeploymentFrame',
                                'flow': '_scene_refresh_frame(memory, frame)\n'
                                        'if (target, continuation) not in ((18966, 67396), (44872, 67408), '
                                        '(33736, 67414), (67604, 67422), (67734, 67454), (235162, 67460), '
                                        '(68056, 67468), (67712, 67560), (96190, 67576), (32906, 67630), '
                                        '(32906, 67732), (67810, 67792), (67902, 67800), (67954, 67808)):\n'
                                        "    raise ValueError('actual closed scene refresh child and token "
                                        "required')\n"
                                        'if command is not None and target != 32906:\n'
                                        "    raise ValueError('only sound mailbox has an observed BYTE "
                                        "argument')\n"
                                        'entered = memory.sync_status(frame)\n'
                                        'if frame.stack_cursor is not None:\n'
                                        '    stack = frame.stack_cursor.advance(-4)\n'
                                        '    stack.set_long(0, continuation)\n'
                                        '    entered = first_replace(frame, stack_cursor=stack)\n'
                                        'if target == 18966:\n'
                                        '    '
                                        '_reset_scene_input_marker_fields(MarkerResetMemory(memory.state))\n'
                                        '    result = _scene_refresh_flags(memory, entered, 0, 2)\n'
                                        'elif target == 44872:\n'
                                        '    result = refresh_gameplay_scene_fields(memory, entered)\n'
                                        'elif target == 33736:\n'
                                        '    result = wait_for_scene_sound_byte_fields(memory, entered)\n'
                                        'elif target == 67604:\n'
                                        '    result = select_sound_command_from_scene_fields(memory, '
                                        'entered).frame\n'
                                        'elif target == 67734:\n'
                                        '    result = draw_overlay_frame_fields(memory, entered)\n'
                                        'elif target == 68056:\n'
                                        '    result = clear_overlay_frame_fields(memory, entered)\n'
                                        'elif target == 67712:\n'
                                        '    result = resume_pending_sound_fields(memory, entered)\n'
                                        'elif target == 32906:\n'
                                        '    result = enqueue_sound_command_fields(memory, entered, '
                                        'command)\n'
                                        'elif target == 67810:\n'
                                        '    result = draw_overlay_frame_header_fields(memory, entered)\n'
                                        'elif target == 67902:\n'
                                        '    result = draw_overlay_frame_middle_fields(memory, entered)\n'
                                        'elif target == 67954:\n'
                                        '    result = draw_overlay_frame_footer_fields(memory, entered)\n'
                                        'elif target == 235162 and entered.stack_cursor is not None:\n'
                                        '    from ..high_level_scene_flows.business_scene import '
                                        'play_scripted_scene_fields\n'
                                        '    result = play_scripted_scene_fields(memory.state, entered)\n'
                                        'elif target == 235162 and entered.stack_cursor is None:\n'
                                        '    observed = memory.state.service_at(target, '
                                        'SceneDisplayContext())\n'
                                        '    if type(observed) is not SceneDisplayResult:\n'
                                        "        raise Boundary('legacy renderer requires its real retained "
                                        "output observations')\n"
                                        '    observed.__post_init__()\n'
                                        '    result = first_replace(entered, target_y=observed.foreground, '
                                        'unit=observed.glyph_count, count=observed.training_carrier, '
                                        'status=None)\n'
                                        'elif target == 96190:\n'
                                        '    from .business_battle import upload_battle_scene_labels_fields\n'
                                        '    result = upload_battle_scene_labels_fields(memory, entered)\n'
                                        'else:\n'
                                        '    result = memory.state.service_at(target, entered)\n'
                                        '    if type(result) is not FirstDeploymentFrame:\n'
                                        '        raise SceneRefreshBoundary(target, entered, continuation)\n'
                                        '_scene_refresh_frame(memory, result)\n'
                                        'if frame.stack_cursor is not None:\n'
                                        '    if result.stack_cursor is None:\n'
                                        '        raise SceneRefreshBoundary(target, result, continuation)\n'
                                        '    memory.sync_status(result)\n'
                                        '    actual = result.stack_cursor.long()\n'
                                        '    if actual != continuation:\n'
                                        '        raise SceneRefreshBoundary(target, result, continuation)\n'
                                        '    result = first_replace(result, '
                                        'stack_cursor=result.stack_cursor.advance(4))\n'
                                        'return memory.sync_status(result)'},
 'expand_glyph_row': {'signature': 'state: GameplayState, source: Cursor, background: Byte, foreground: Byte',
                      'returns': 'Long',
                      'flow': 'from ..high_level_scene_flows.business_scene import expand_glyph_row_fields\n'
                              'checked_state(state)\n'
                              'checked_cursor(source, state)\n'
                              'uint(background, 8)\n'
                              'uint(foreground, 8)\n'
                              'entered = first_replace(FirstDeploymentFrame.unobserved(), '
                              'target_x=background, target_y=foreground, controller=source.advance(0))\n'
                              'actual = expand_glyph_row_fields(SceneRefreshMemory(state), entered)\n'
                              'source.base = actual.controller.base\n'
                              'return actual.choice'},
 'expand_glyph_stream': {'signature': 'state: GameplayState, tokens: Cursor, destination: Cursor, colors: '
                                      'GlyphColors, remaining: Long',
                         'returns': 'GlyphStreamResult',
                         'flow': 'from ..high_level_scene_flows.business_scene import '
                                 'expand_glyph_stream_fields\n'
                                 'checked_state(state)\n'
                                 'checked_cursor(tokens, state)\n'
                                 'checked_cursor(destination, state)\n'
                                 'if type(colors) is not GlyphColors:\n'
                                 "    raise ValueError('explicit glyph colors required')\n"
                                 'colors.__post_init__()\n'
                                 'uint(remaining, 32)\n'
                                 'entered = first_replace(FirstDeploymentFrame.unobserved(), '
                                 'roster=tokens.advance(0), candidates=destination.advance(0), '
                                 'target_x=colors.background, target_y=colors.foreground, count=remaining)\n'
                                 'actual = expand_glyph_stream_fields(SceneRefreshMemory(state), entered)\n'
                                 'tokens.base, destination.base = (actual.roster.base, '
                                 'actual.candidates.base)\n'
                                 'return GlyphStreamResult(tokens, destination, actual.count)'}})

# Parent observes the actual A1 advanced by its control child.
DECLARATIONS.update({'stage_sprite_word_packet_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_scene_flows.domain import SceneState\nfrom ..high_level_main_flows.business_movement_support import _movement_binary_flags\nfrom ..high_level_battle_ai.business_formation import _first_sub_word, _first_memory_word, _first_right_word\nframe = _scene_refresh_frame(memory, frame)\nif type(memory.state) is not SceneState or any((value is None for value in (frame.target_x, frame.target_y, frame.unit, frame.count, frame.distance, frame.offset_x, frame.offset_y, frame.choice, frame.roster, frame.candidates, frame.controller, frame.scan, frame.opponent, frame.scratch, frame.auxiliary, frame.stack_cursor, frame.status))):\n    raise SceneRefreshBoundary(158714, frame, None)\nframe.validate(memory.state, True)\ndestination = memory.cursor_at(4294955264)\nframe = first_replace(frame, candidates=destination)\nqueued = memory.state.read(4294963994, 2)\ndestination = destination.advance(s16(queued))\nframe = first_replace(frame, candidates=destination)\nrows = low16(frame.target_y)\nframe = _first_word(frame, 'choice', rows)\nframe = _first_sub_word(frame, 'choice', rows, 1)\nfor counter in descending_inclusive(u16(rows - 1)):\n    destination.set_word(0, low16(frame.target_x))\n    destination = destination.advance(2)\n    frame = first_replace(frame, candidates=destination)\n    frame = _first_memory_word(frame, low16(frame.target_x))\n    destination.set_word(0, low16(frame.unit))\n    destination = destination.advance(2)\n    frame = first_replace(frame, candidates=destination)\n    frame = _first_memory_word(frame, low16(frame.unit))\n    from ..high_level_battle_ai.business_formation import _first_add_word\n    frame = _first_add_word(frame, 'unit', low16(frame.unit), 128)\n    frame = _first_word(frame, 'count', low16(frame.target_x))\n    while True:\n        token = frame.roster.word()\n        frame = first_replace(frame, roster=frame.roster.advance(2))\n        frame = _first_word(frame, 'distance', token)\n        if negative_word(token):\n            frame = _first_word(frame, 'offset_x', low16(frame.distance))\n            frame = _first_word(frame, 'distance', low16(frame.distance) & 32767)\n            frame = _first_right_word(frame, 'distance', low16(frame.distance), 7)\n            before = frame.distance\n            frame = first_replace(frame, distance=before & 4294967294, status=frame.status & 27 | (0 if before & 1 else 4))\n            relative = memory.state.table(158796).word(low16(frame.distance))\n            frame = _first_word(frame, 'distance', relative)\n            target = u32(158808 + s16(relative))\n            stack = frame.stack_cursor.advance(-4)\n            stack.set_long(0, 158774)\n            entered = first_replace(frame, stack_cursor=stack)\n            memory.sync_status(entered)\n            if target == 158808:\n                frame = repeat_word_packet_control_fields(memory, entered)\n            elif target == 158834:\n                frame = increment_word_packet_control_fields(memory, entered)\n            else:\n                raise SceneRefreshBoundary(target, entered, 158774)\n            actual = frame.stack_cursor.long()\n            if actual != 158774:\n                raise SceneRefreshBoundary(actual, frame, 158774)\n            frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(4))\n            destination = frame.candidates\n            frame = _first_memory_word(frame, low16(frame.count))\n            if low16(frame.count) == 0:\n                break\n            continue\n        frame = _first_long(frame, 'target_x', swap_words(frame.target_x))\n        frame = _first_word(frame, 'distance', low16(frame.distance) | low16(frame.target_x))\n        destination.set_word(0, low16(frame.distance))\n        destination = destination.advance(2)\n        frame = first_replace(frame, candidates=destination)\n        frame = _first_memory_word(frame, low16(frame.distance))\n        frame = _first_long(frame, 'target_x', swap_words(frame.target_x))\n        frame = _first_sub_word(frame, 'count', low16(frame.count), 1)\n        frame = _first_memory_word(frame, low16(frame.count))\n        if low16(frame.count) == 0:\n            break\n    frame = first_replace(frame, choice=replace_word(frame.choice, u16(counter - 1)))\ndestination.word()\ndestination.set_word(0, 0)\nframe = _first_memory_word(frame, 0)\nframe = _first_add_word(frame, 'target_x', low16(frame.target_x), 2)\nframe = _first_long(frame, 'target_x', low16(frame.target_x) * low16(frame.target_y))\nframe = _first_shift_word(frame, 'target_x', low16(frame.target_x), 1)\nprevious = memory.state.read(4294963994, 2)\nframe, value = _movement_binary_flags(memory.state, frame, previous, low16(frame.target_x), 16)\nmemory.state.write(4294963994, 2, value)\nmemory.sync_status(frame)\nreturn memory.frame(frame)"}})

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
APPROVED.setdefault('domain',set()).update({'SceneState'})
APPROVED.setdefault('business_budget',set()).update({'_six_place_decimal_fields'})
APPROVED.setdefault('contexts_numeric',set()).update({'DecimalMemory'})
APPROVED.setdefault('business_movement_support',set()).update({'_movement_save_longs', '_movement_binary_flags', '_movement_restore_longs'})
APPROVED.setdefault('business_formation',set()).update({'_first_sub_word', '_first_add_word', '_first_memory_word', '_first_right_word'})
DECLARATIONS.update({'_word_packet_numeric_control_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                      'FirstDeploymentFrame, wide: bool',
                                         'returns': 'FirstDeploymentFrame',
                                         'flow': 'from ..high_level_scene_flows.domain import SceneState\n'
                                                 'from ..high_level_player_commands.business_budget import '
                                                 '_six_place_decimal_fields\n'
                                                 'from ..high_level_player_commands.contexts_numeric import '
                                                 'DecimalMemory\n'
                                                 'from ..high_level_main_flows.business_movement_support '
                                                 'import _movement_save_longs, _movement_restore_longs\n'
                                                 'from ..high_level_battle_ai.business_formation import '
                                                 '_first_sub_word, _first_memory_word\n'
                                                 'if type(wide) is not bool:\n'
                                                 "    raise ValueError('actual WORD or LONG numeric control "
                                                 "required')\n"
                                                 'entry, continuation = (158934, 158964) if wide else '
                                                 '(158862, 158894)\n'
                                                 'frame = _scene_refresh_frame(memory, frame)\n'
                                                 'if type(memory.state) is not SceneState or '
                                                 'frame.stack_cursor is None:\n'
                                                 '    raise SceneRefreshBoundary(entry, frame, None)\n'
                                                 'frame.validate(memory.state, True)\n'
                                                 "frame = _first_word(frame, 'offset_x', "
                                                 'low16(frame.offset_x) & 255)\n'
                                                 'pointer = frame.roster.long()\n'
                                                 'frame = first_replace(frame, '
                                                 'roster=frame.roster.advance(4), '
                                                 'controller=memory.cursor_at(pointer))\n'
                                                 "saved_names = ('target_x', 'target_y', 'unit', 'count', "
                                                 "'distance', 'offset_x')\n"
                                                 'frame = _movement_save_longs(memory.state, frame, '
                                                 'saved_names)\n'
                                                 'if wide:\n'
                                                 '    value = frame.controller.long()\n'
                                                 "    frame = _first_long(frame, 'target_x', value)\n"
                                                 'else:\n'
                                                 "    frame = _first_long(frame, 'target_x', 0)\n"
                                                 '    value = frame.controller.word()\n'
                                                 "    frame = _first_word(frame, 'target_x', value)\n"
                                                 'digit_tile = memory.cursor_at(4294964882).word()\n'
                                                 "frame = _first_word(frame, 'target_y', digit_tile)\n"
                                                 'blank_tile = memory.cursor_at(4294964884).word()\n'
                                                 "frame = _first_word(frame, 'unit', blank_tile)\n"
                                                 'frame = first_replace(frame, '
                                                 'auxiliary=memory.cursor_at(4294955776))\n'
                                                 'memory.sync_status(frame)\n'
                                                 'numeric = DecimalMemory(memory.state, frame.stack_cursor)\n'
                                                 'numeric.enter_call(continuation)\n'
                                                 'formatted = _six_place_decimal_fields(numeric, '
                                                 'frame.target_x, low16(frame.target_y), low16(frame.unit), '
                                                 'frame.auxiliary)\n'
                                                 'numeric.leave_call(continuation)\n'
                                                 'frame = first_replace(frame, target_x=formatted.remainder, '
                                                 'stack_cursor=numeric.stack_cursor, '
                                                 'auxiliary=formatted.destination)\n'
                                                 "frame = _first_word(frame, 'count', formatted.divisor)\n"
                                                 "frame = _first_word(frame, 'distance', formatted.started)\n"
                                                 "frame = _first_word(frame, 'offset_x', formatted.glyph)\n"
                                                 'status = (16 if formatted.glyph < digit_tile else 0) | (8 '
                                                 'if formatted.glyph & 32768 else 0) | (4 if formatted.glyph '
                                                 '== 0 else 0)\n'
                                                 'frame = memory.sync_status(first_replace(frame, '
                                                 'status=status))\n'
                                                 'frame = _movement_restore_longs(memory.state, frame, '
                                                 'saved_names)\n'
                                                 "frame = _first_word(frame, 'distance', 6)\n"
                                                 "frame = _first_sub_word(frame, 'distance', 6, "
                                                 'low16(frame.offset_x))\n'
                                                 "frame = _first_shift_word(frame, 'distance', "
                                                 'low16(frame.distance), 1)\n'
                                                 'frame = first_replace(frame, '
                                                 'controller=memory.cursor_at(4294955776).advance(s16(low16(frame.distance))))\n'
                                                 'count = low16(frame.offset_x)\n'
                                                 "frame = _first_word(frame, 'distance', count)\n"
                                                 "frame = _first_sub_word(frame, 'distance', count, 1)\n"
                                                 "frame = _first_long(frame, 'target_x', "
                                                 'swap_words(frame.target_x))\n'
                                                 'for counter in descending_inclusive(u16(count - 1)):\n'
                                                 '    tile = frame.controller.word()\n'
                                                 '    frame = first_replace(frame, '
                                                 'controller=frame.controller.advance(2))\n'
                                                 "    frame = _first_word(frame, 'offset_y', tile)\n"
                                                 "    frame = _first_word(frame, 'offset_y', "
                                                 'low16(frame.offset_y) | low16(frame.target_x))\n'
                                                 '    frame.candidates.set_word(0, low16(frame.offset_y))\n'
                                                 '    frame = first_replace(frame, '
                                                 'candidates=frame.candidates.advance(2))\n'
                                                 '    frame = _first_memory_word(frame, '
                                                 'low16(frame.offset_y))\n'
                                                 '    frame = first_replace(frame, '
                                                 'distance=replace_word(frame.distance, u16(counter - 1)))\n'
                                                 "frame = _first_long(frame, 'target_x', "
                                                 'swap_words(frame.target_x))\n'
                                                 "frame = _first_sub_word(frame, 'count', "
                                                 'low16(frame.count), low16(frame.offset_x))\n'
                                                 'return memory.sync_status(frame)'},
 '_word_packet_tile_pair_control_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                        'FirstDeploymentFrame, odd: bool',
                                           'returns': 'FirstDeploymentFrame',
                                           'flow': 'from ..high_level_scene_flows.domain import SceneState\n'
                                                   'from ..high_level_battle_ai.business_formation import '
                                                   '_first_add_word, _first_sub_word, _first_memory_word\n'
                                                   'if type(odd) is not bool:\n'
                                                   "    raise ValueError('actual even or odd tile-pair "
                                                   "control required')\n"
                                                   'frame = _scene_refresh_frame(memory, frame)\n'
                                                   'entry = 159024 if odd else 159004\n'
                                                   'if type(memory.state) is not SceneState or frame.roster '
                                                   'is None or frame.candidates is None or (frame.count is '
                                                   'None) or (frame.offset_x is None):\n'
                                                   '    raise SceneRefreshBoundary(entry, frame, None)\n'
                                                   'pointer = frame.roster.long()\n'
                                                   'frame = first_replace(frame, '
                                                   'roster=frame.roster.advance(4), '
                                                   'controller=memory.cursor_at(pointer))\n'
                                                   'tile = frame.controller.word()\n'
                                                   "frame = _first_word(frame, 'offset_x', tile)\n"
                                                   "frame = _first_shift_word(frame, 'offset_x', tile, 2)\n"
                                                   'base = memory.cursor_at(4294963062).word()\n'
                                                   "frame = _first_add_word(frame, 'offset_x', "
                                                   'low16(frame.offset_x), base)\n'
                                                   'if odd:\n'
                                                   "    frame = _first_add_word(frame, 'offset_x', "
                                                   'low16(frame.offset_x), 1)\n'
                                                   'frame.candidates.set_word(0, low16(frame.offset_x))\n'
                                                   'frame = first_replace(frame, '
                                                   'candidates=frame.candidates.advance(2))\n'
                                                   'frame = _first_memory_word(frame, '
                                                   'low16(frame.offset_x))\n'
                                                   "frame = _first_add_word(frame, 'offset_x', "
                                                   'low16(frame.offset_x), 2)\n'
                                                   'frame.candidates.set_word(0, low16(frame.offset_x))\n'
                                                   'frame = first_replace(frame, '
                                                   'candidates=frame.candidates.advance(2))\n'
                                                   'frame = _first_memory_word(frame, '
                                                   'low16(frame.offset_x))\n'
                                                   "frame = _first_sub_word(frame, 'count', "
                                                   'low16(frame.count), 2)\n'
                                                   'return memory.sync_status(frame)'},
 'append_even_tile_pair_control_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                       'FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'return _word_packet_tile_pair_control_fields(memory, '
                                                  'frame, False)'},
 'append_long_decimal_packet_control_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                            'FirstDeploymentFrame',
                                               'returns': 'FirstDeploymentFrame',
                                               'flow': 'return _word_packet_numeric_control_fields(memory, '
                                                       'frame, True)'},
 'append_odd_tile_pair_control_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                      'FirstDeploymentFrame',
                                         'returns': 'FirstDeploymentFrame',
                                         'flow': 'return _word_packet_tile_pair_control_fields(memory, '
                                                 'frame, True)'},
 'append_word_decimal_packet_control_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                            'FirstDeploymentFrame',
                                               'returns': 'FirstDeploymentFrame',
                                               'flow': 'return _word_packet_numeric_control_fields(memory, '
                                                       'frame, False)'},
 'stage_sprite_word_packet_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'from ..high_level_scene_flows.domain import SceneState\n'
                                             'from ..high_level_main_flows.business_movement_support import '
                                             '_movement_binary_flags\n'
                                             'from ..high_level_battle_ai.business_formation import '
                                             '_first_sub_word, _first_memory_word, _first_right_word\n'
                                             'frame = _scene_refresh_frame(memory, frame)\n'
                                             'if type(memory.state) is not SceneState or any((value is None '
                                             'for value in (frame.target_x, frame.target_y, frame.unit, '
                                             'frame.count, frame.distance, frame.offset_x, frame.offset_y, '
                                             'frame.choice, frame.roster, frame.candidates, '
                                             'frame.controller, frame.scan, frame.opponent, frame.scratch, '
                                             'frame.auxiliary, frame.stack_cursor, frame.status))):\n'
                                             '    raise SceneRefreshBoundary(158714, frame, None)\n'
                                             'frame.validate(memory.state, True)\n'
                                             'destination = memory.cursor_at(4294955264)\n'
                                             'frame = first_replace(frame, candidates=destination)\n'
                                             'queued = memory.state.read(4294963994, 2)\n'
                                             'destination = destination.advance(s16(queued))\n'
                                             'frame = first_replace(frame, candidates=destination)\n'
                                             'rows = low16(frame.target_y)\n'
                                             "frame = _first_word(frame, 'choice', rows)\n"
                                             "frame = _first_sub_word(frame, 'choice', rows, 1)\n"
                                             'for counter in descending_inclusive(u16(rows - 1)):\n'
                                             '    destination.set_word(0, low16(frame.target_x))\n'
                                             '    destination = destination.advance(2)\n'
                                             '    frame = first_replace(frame, candidates=destination)\n'
                                             '    frame = _first_memory_word(frame, low16(frame.target_x))\n'
                                             '    destination.set_word(0, low16(frame.unit))\n'
                                             '    destination = destination.advance(2)\n'
                                             '    frame = first_replace(frame, candidates=destination)\n'
                                             '    frame = _first_memory_word(frame, low16(frame.unit))\n'
                                             '    from ..high_level_battle_ai.business_formation import '
                                             '_first_add_word\n'
                                             "    frame = _first_add_word(frame, 'unit', low16(frame.unit), "
                                             '128)\n'
                                             "    frame = _first_word(frame, 'count', "
                                             'low16(frame.target_x))\n'
                                             '    while True:\n'
                                             '        token = frame.roster.word()\n'
                                             '        frame = first_replace(frame, '
                                             'roster=frame.roster.advance(2))\n'
                                             "        frame = _first_word(frame, 'distance', token)\n"
                                             '        if negative_word(token):\n'
                                             "            frame = _first_word(frame, 'offset_x', "
                                             'low16(frame.distance))\n'
                                             "            frame = _first_word(frame, 'distance', "
                                             'low16(frame.distance) & 32767)\n'
                                             "            frame = _first_right_word(frame, 'distance', "
                                             'low16(frame.distance), 7)\n'
                                             '            before = frame.distance\n'
                                             '            frame = first_replace(frame, distance=before & '
                                             '4294967294, status=frame.status & 27 | (0 if before & 1 else '
                                             '4))\n'
                                             '            relative = '
                                             'memory.state.table(158796).word(low16(frame.distance))\n'
                                             "            frame = _first_word(frame, 'distance', relative)\n"
                                             '            target = u32(158808 + s16(relative))\n'
                                             '            stack = frame.stack_cursor.advance(-4)\n'
                                             '            stack.set_long(0, 158774)\n'
                                             '            entered = first_replace(frame, '
                                             'stack_cursor=stack)\n'
                                             '            memory.sync_status(entered)\n'
                                             '            if target == 158808:\n'
                                             '                frame = '
                                             'repeat_word_packet_control_fields(memory, entered)\n'
                                             '            elif target == 158834:\n'
                                             '                frame = '
                                             'increment_word_packet_control_fields(memory, entered)\n'
                                             '            elif target == 158862:\n'
                                             '                frame = '
                                             'append_word_decimal_packet_control_fields(memory, entered)\n'
                                             '            elif target == 158934:\n'
                                             '                frame = '
                                             'append_long_decimal_packet_control_fields(memory, entered)\n'
                                             '            elif target == 159004:\n'
                                             '                frame = '
                                             'append_even_tile_pair_control_fields(memory, entered)\n'
                                             '            elif target == 159024:\n'
                                             '                frame = '
                                             'append_odd_tile_pair_control_fields(memory, entered)\n'
                                             '            else:\n'
                                             '                raise SceneRefreshBoundary(target, entered, '
                                             '158774)\n'
                                             '            actual = frame.stack_cursor.long()\n'
                                             '            if actual != 158774:\n'
                                             '                raise SceneRefreshBoundary(actual, frame, '
                                             '158774)\n'
                                             '            frame = first_replace(frame, '
                                             'stack_cursor=frame.stack_cursor.advance(4))\n'
                                             '            destination = frame.candidates\n'
                                             '            frame = _first_memory_word(frame, '
                                             'low16(frame.count))\n'
                                             '            if low16(frame.count) == 0:\n'
                                             '                break\n'
                                             '            continue\n'
                                             "        frame = _first_long(frame, 'target_x', "
                                             'swap_words(frame.target_x))\n'
                                             "        frame = _first_word(frame, 'distance', "
                                             'low16(frame.distance) | low16(frame.target_x))\n'
                                             '        destination.set_word(0, low16(frame.distance))\n'
                                             '        destination = destination.advance(2)\n'
                                             '        frame = first_replace(frame, candidates=destination)\n'
                                             '        frame = _first_memory_word(frame, '
                                             'low16(frame.distance))\n'
                                             "        frame = _first_long(frame, 'target_x', "
                                             'swap_words(frame.target_x))\n'
                                             "        frame = _first_sub_word(frame, 'count', "
                                             'low16(frame.count), 1)\n'
                                             '        frame = _first_memory_word(frame, low16(frame.count))\n'
                                             '        if low16(frame.count) == 0:\n'
                                             '            break\n'
                                             '    frame = first_replace(frame, '
                                             'choice=replace_word(frame.choice, u16(counter - 1)))\n'
                                             'destination.word()\n'
                                             'destination.set_word(0, 0)\n'
                                             'frame = _first_memory_word(frame, 0)\n'
                                             "frame = _first_add_word(frame, 'target_x', "
                                             'low16(frame.target_x), 2)\n'
                                             "frame = _first_long(frame, 'target_x', low16(frame.target_x) * "
                                             'low16(frame.target_y))\n'
                                             "frame = _first_shift_word(frame, 'target_x', "
                                             'low16(frame.target_x), 1)\n'
                                             'previous = memory.state.read(4294963994, 2)\n'
                                             'frame, value = _movement_binary_flags(memory.state, frame, '
                                             'previous, low16(frame.target_x), 16)\n'
                                             'memory.state.write(4294963994, 2, value)\n'
                                             'memory.sync_status(frame)\n'
                                             'return memory.frame(frame)'}})

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
DECLARATIONS.update({'_video_plane_dma_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, sprite: '
                                          'bool',
                             'returns': 'FirstDeploymentFrame',
                             'flow': 'if type(sprite) is not bool:\n'
                                     "    raise ValueError('actual video initialization or sprite-plane "
                                     "entry required')\n"
                                     'frame = _scene_refresh_frame(memory, frame)\n'
                                     'frame = first_replace(frame, auxiliary=memory.cursor_at(12582916))\n'
                                     'frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, '
                                     '36609)\n'
                                     'register = memory.cursor_at(4294964742).word()\n'
                                     "frame = _first_word(frame, 'choice', register)\n"
                                     "frame = _first_byte(frame, 'choice', low8(register) | 16)\n"
                                     'frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, '
                                     'register | 16)\n'
                                     'frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 4, '
                                     '2483000391 if sprite else 2483000575)\n'
                                     'frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, '
                                     '38784)\n'
                                     'frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 4, '
                                     '2013266050 if sprite else 1073741952)\n'
                                     'frame = _scene_refresh_emit(memory, frame, 12582912, 2, 246 if sprite '
                                     'else 0)\n'
                                     'while True:\n'
                                     '    response = frame.auxiliary.word()\n'
                                     "    frame = _first_word(frame, 'choice', response)\n"
                                     "    frame = _first_word(frame, 'choice', response & 2)\n"
                                     '    if response & 2 == 0:\n'
                                     '        break\n'
                                     '    if frame.stack_cursor is not None:\n'
                                     '        raise SceneRefreshBoundary(26874 if sprite else 26758, '
                                     'memory.sync_status(frame), None)\n'
                                     "    memory.state.progress('vdp-dma')\n"
                                     '    frame = first_replace(frame, status=memory.state.sr & 31)\n'
                                     'released = memory.cursor_at(16727808).byte()\n'
                                     'frame = _scene_refresh_flags(memory, frame, released, 1)\n'
                                     'if released == 0:\n'
                                     '    frame = _scene_refresh_emit(memory, frame, 10555648, 2, 0)\n'
                                     'restored = memory.cursor_at(4294964742).word()\n'
                                     'frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, '
                                     'restored)\n'
                                     'return _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, '
                                     '36610)'},
 'clear_video_sprite_plane': {'signature': 'state: GameplayState',
                              'returns': 'None',
                              'flow': 'checked_state(state)\n'
                                      'clear_video_sprite_plane_fields(SceneRefreshMemory(state), '
                                      'FirstDeploymentFrame.unobserved())'},
 'clear_video_sprite_plane_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'frame = _video_plane_dma_fields(memory, frame, True)\n'
                                             'frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                             '1073741840)\n'
                                             'frame = _scene_refresh_emit(memory, frame, 12582912, 4, 0)\n'
                                             'frame = _scene_refresh_emit(memory, frame, 4294963986, 4, 0)\n'
                                             'frame = _scene_refresh_emit(memory, frame, 4294963990, 4, 0)\n'
                                             'frame = first_replace(frame, '
                                             'auxiliary=memory.cursor_at(4294965248))\n'
                                             "frame = _first_long(frame, 'choice', 0)\n"
                                             "frame = _first_word(frame, 'offset_y', 159)\n"
                                             'for counter in descending_inclusive(159):\n'
                                             '    destination = frame.auxiliary\n'
                                             '    frame = first_replace(frame, '
                                             'auxiliary=destination.advance(4))\n'
                                             '    frame = _scene_refresh_emit(memory, frame, '
                                             'destination.base, 4, frame.choice)\n'
                                             "    frame = _scene_refresh_decrement(frame, 'offset_y', "
                                             'counter)\n'
                                             'return memory.sync_status(frame)'},
 'initialize_video_registers_and_planes': {'signature': 'state: GameplayState',
                                           'returns': 'None',
                                           'flow': 'checked_state(state)\n'
                                                   'initialize_video_registers_and_planes_fields(SceneRefreshMemory(state), '
                                                   'FirstDeploymentFrame.unobserved())'},
 'initialize_video_registers_and_planes_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                               'FirstDeploymentFrame',
                                                  'returns': 'FirstDeploymentFrame',
                                                  'flow': 'frame = _scene_refresh_frame(memory, frame)\n'
                                                          'frame = first_replace(frame, '
                                                          'roster=memory.cursor_at(12582916), '
                                                          'candidates=memory.cursor_at(12582912), '
                                                          'controller=memory.cursor_at(26792))\n'
                                                          "frame = _first_long(frame, 'choice', 18)\n"
                                                          'for counter in descending_inclusive(18):\n'
                                                          '    register = frame.controller.word()\n'
                                                          '    frame = first_replace(frame, '
                                                          'controller=frame.controller.advance(2))\n'
                                                          '    frame = _scene_refresh_emit(memory, frame, '
                                                          'frame.roster.base, 2, register)\n'
                                                          '    frame = _scene_refresh_decrement(frame, '
                                                          "'choice', counter)\n"
                                                          'initial = memory.cursor_at(26794).word()\n'
                                                          'frame = _scene_refresh_emit(memory, frame, '
                                                          '4294964742, 2, initial)\n'
                                                          "frame = _first_long(frame, 'target_x', 0)\n"
                                                          'frame = _scene_refresh_emit(memory, frame, '
                                                          '12582916, 4, 3221225472)\n'
                                                          "frame = _first_word(frame, 'choice', 63)\n"
                                                          'for counter in descending_inclusive(63):\n'
                                                          '    frame = _scene_refresh_emit(memory, frame, '
                                                          'frame.candidates.base, 2, low16(frame.target_x))\n'
                                                          '    frame = _scene_refresh_decrement(frame, '
                                                          "'choice', counter)\n"
                                                          'return '
                                                          'memory.sync_status(_video_plane_dma_fields(memory, '
                                                          'frame, False))'}})

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
APPROVED.setdefault('business_movement_support',set()).update({'_movement_binary_flags'})
DECLARATIONS.update({'copy_video_transfer_descriptor': {'signature': 'state: GameplayState, index: Word',
                                    'returns': 'TransferResult',
                                    'flow': 'checked_state(state)\n'
                                            'uint(index, 16)\n'
                                            'frame = '
                                            'copy_video_transfer_descriptor_fields(SceneRefreshMemory(state), '
                                            'FirstDeploymentFrame.unobserved(), index)\n'
                                            'return TransferResult(frame.controller, frame.scan)'},
 'copy_video_transfer_descriptor_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                        'FirstDeploymentFrame, observed_index: Word | '
                                                        'None=None',
                                           'returns': 'FirstDeploymentFrame',
                                           'flow': 'from ..high_level_main_flows.business_movement_support '
                                                   'import _movement_binary_flags\n'
                                                   'memory.frame(frame)\n'
                                                   'if observed_index is None:\n'
                                                   '    if frame.target_x is None:\n'
                                                   '        raise SceneRefreshBoundary(33042, frame, None)\n'
                                                   '    index = low16(frame.target_x)\n'
                                                   'else:\n'
                                                   '    index = uint(observed_index, 16)\n'
                                                   '    if frame.target_x is not None and '
                                                   'low16(frame.target_x) != index:\n'
                                                   "        raise ValueError('actual descriptor WORD index "
                                                   "differs from retained D0')\n"
                                                   'frame = first_replace(frame, '
                                                   'candidates=memory.cursor_at(33068))\n'
                                                   'frame = memory.sync_status(_first_shift_word(frame, '
                                                   "'target_x', index, 3))\n"
                                                   'frame = first_replace(frame, '
                                                   'candidates=frame.candidates.advance(s16(u16(index << '
                                                   '3))))\n'
                                                   'descriptor = frame.candidates\n'
                                                   'address = descriptor.long()\n'
                                                   'frame = first_replace(frame, '
                                                   'candidates=descriptor.advance(4), '
                                                   'controller=memory.cursor_at(address))\n'
                                                   'descriptor = frame.candidates\n'
                                                   'address = u32(s16(descriptor.word()))\n'
                                                   'frame = first_replace(frame, '
                                                   'candidates=descriptor.advance(2), '
                                                   'scan=memory.cursor_at(address))\n'
                                                   'descriptor = frame.candidates\n'
                                                   'remaining = descriptor.word()\n'
                                                   'frame = first_replace(frame, '
                                                   'candidates=descriptor.advance(2))\n'
                                                   "frame = memory.sync_status(_first_word(frame, 'choice', "
                                                   'remaining))\n'
                                                   'while True:\n'
                                                   '    source, destination = (frame.controller, '
                                                   'frame.scan)\n'
                                                   '    value = source.long()\n'
                                                   '    frame = first_replace(frame, '
                                                   'controller=source.advance(4))\n'
                                                   '    frame = _scene_refresh_emit(memory, frame, '
                                                   'destination.base, 4, value)\n'
                                                   '    frame = first_replace(frame, '
                                                   'scan=destination.advance(4))\n'
                                                   "    frame = _scene_refresh_decrement(frame, 'choice', "
                                                   'remaining)\n'
                                                   '    remaining = u16(remaining - 1)\n'
                                                   '    if remaining == 65535:\n'
                                                   '        break\n'
                                                   'memory.sync_status(frame)\n'
                                                   'previous = memory.state.read(4294963998, 2)\n'
                                                   'frame, value = _movement_binary_flags(memory.state, '
                                                   'frame, previous, 1, 16)\n'
                                                   'memory.state.write(4294963998, 2, value)\n'
                                                   'return memory.sync_status(frame)'}})


# Complete scene clear126 and fill-selector12 original Frame cores99; ordinary opcode lowerers and historical APIs unchanged.
DECLARATIONS.update({'_scene_refresh_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long, command: Byte | None=None', 'returns': 'FirstDeploymentFrame', 'flow': "_scene_refresh_frame(memory, frame)\nif (target, continuation) not in ((1674, 1556), (1674, 1644), (44872, 1672), (18966, 67396), (44872, 67408), (33736, 67414), (67604, 67422), (67734, 67454), (235162, 67460), (68056, 67468), (67712, 67560), (96190, 67576), (32906, 67630), (32906, 67732), (67810, 67792), (67902, 67800), (67954, 67808)):\n    raise ValueError('actual closed scene refresh child and token required')\nif command is not None and target != 32906:\n    raise ValueError('only sound mailbox has an observed BYTE argument')\nentered = memory.sync_status(frame)\nif frame.stack_cursor is not None:\n    stack = frame.stack_cursor.advance(-4)\n    stack.set_long(0, continuation)\n    entered = first_replace(frame, stack_cursor=stack)\nif target == 1674:\n    result = select_scene_fill_pattern_fields(memory, entered)\nelif target == 18966:\n    _reset_scene_input_marker_fields(MarkerResetMemory(memory.state))\n    result = _scene_refresh_flags(memory, entered, 0, 2)\nelif target == 44872:\n    result = refresh_gameplay_scene_fields(memory, entered)\nelif target == 33736:\n    result = wait_for_scene_sound_byte_fields(memory, entered)\nelif target == 67604:\n    result = select_sound_command_from_scene_fields(memory, entered).frame\nelif target == 67734:\n    result = draw_overlay_frame_fields(memory, entered)\nelif target == 68056:\n    result = clear_overlay_frame_fields(memory, entered)\nelif target == 67712:\n    result = resume_pending_sound_fields(memory, entered)\nelif target == 32906:\n    result = enqueue_sound_command_fields(memory, entered, command)\nelif target == 67810:\n    result = draw_overlay_frame_header_fields(memory, entered)\nelif target == 67902:\n    result = draw_overlay_frame_middle_fields(memory, entered)\nelif target == 67954:\n    result = draw_overlay_frame_footer_fields(memory, entered)\nelif target == 235162 and entered.stack_cursor is not None:\n    from ..high_level_scene_flows.business_scene import play_scripted_scene_fields\n    result = play_scripted_scene_fields(memory.state, entered)\nelif target == 235162 and entered.stack_cursor is None:\n    observed = memory.state.service_at(target, SceneDisplayContext())\n    if type(observed) is not SceneDisplayResult:\n        raise Boundary('legacy renderer requires its real retained output observations')\n    observed.__post_init__()\n    result = first_replace(entered, target_y=observed.foreground, unit=observed.glyph_count, count=observed.training_carrier, status=None)\nelif target == 96190:\n    from .business_battle import upload_battle_scene_labels_fields\n    result = upload_battle_scene_labels_fields(memory, entered)\nelse:\n    result = memory.state.service_at(target, entered)\n    if type(result) is not FirstDeploymentFrame:\n        raise SceneRefreshBoundary(target, entered, continuation)\n_scene_refresh_frame(memory, result)\nif frame.stack_cursor is not None:\n    if result.stack_cursor is None:\n        raise SceneRefreshBoundary(target, result, continuation)\n    memory.sync_status(result)\n    actual = result.stack_cursor.long()\n    if actual != continuation:\n        raise SceneRefreshBoundary(target, result, continuation)\n    result = first_replace(result, stack_cursor=result.stack_cursor.advance(4))\nreturn memory.sync_status(result)"}, 'select_scene_fill_pattern_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_refresh_frame(memory, frame)\nif frame.stack_cursor is None:\n    raise SceneRefreshBoundary(1674, frame, None)\nmemory.sync_status(frame)\nframe = _first_word(frame, 'target_x', memory.state.read(4294964932, 2))\nframe = _first_shift_word(frame, 'target_x', low16(frame.target_x), 2)\nmemory.sync_status(frame)\npattern = memory.cursor_at(1686).long(s16(low16(frame.target_x)))\nreturn memory.sync_status(_first_long(frame, 'target_y', pattern))"}, 'clear_scene_video_and_state_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_refresh_frame(memory, frame)\nif frame.stack_cursor is None:\n    raise SceneRefreshBoundary(1548, frame, None)\nframe = memory.status_word(frame, 9984)\nframe = _scene_refresh_call_fields(memory, frame, 1674, 1556)\nmemory.sync_status(frame)\nmemory.state.read(4294964094, 2)\nframe = _scene_refresh_emit(memory, frame, 4294964094, 2, 0)\nframe = _scene_refresh_emit(memory, frame, 12582916, 4, 1621098498)\nframe = _scene_refresh_repeat_pixels(memory, frame, 'target_x', 1439, frame.target_y)\nmemory.sync_status(frame)\nactive = memory.state.read(4294964932, 2)\nframe = _scene_refresh_flags(memory, frame, active, 2)\nif active == 0:\n    frame = _scene_refresh_emit(memory, frame, 12582916, 4, 1879048193)\n    for address, count in ((564700, 23), (565372, 15)):\n        frame = first_replace(frame, roster=memory.cursor_at(address))\n        frame = _first_word(frame, 'target_x', count)\n        for counter in descending_inclusive(count):\n            memory.sync_status(frame)\n            source = frame.roster\n            value = source.long()\n            frame = first_replace(frame, roster=source.advance(4))\n            frame = _scene_refresh_emit(memory, frame, 12582912, 4, value)\n            frame = _scene_refresh_decrement(frame, 'target_x', counter)\nframe = _scene_refresh_call_fields(memory, frame, 1674, 1644)\nframe = first_replace(frame, roster=memory.cursor_at(4294964502))\nframe = _first_word(frame, 'target_x', 23)\nfor counter in descending_inclusive(23):\n    destination = frame.roster\n    frame = first_replace(frame, roster=destination.advance(4))\n    frame = _scene_refresh_emit(memory, frame, destination.base, 4, frame.target_y)\n    frame = _scene_refresh_decrement(frame, 'target_x', counter)\nfor address in (4294964090, 4294964092):\n    memory.sync_status(frame)\n    memory.state.read(address, 2)\n    frame = _scene_refresh_emit(memory, frame, address, 2, 0)\nreturn _scene_refresh_call_fields(memory, frame, 44872, 1672)"}})

DECLARATIONS.update({'_gameplay_message_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _scene_refresh_frame(memory, frame)\nif (target, continuation) not in ((44872, 199308), (1548, 199334)):\n    raise ValueError('original gameplay message child and token required')\nentered = memory.sync_status(frame)\nif frame.stack_cursor is not None:\n    stack = frame.stack_cursor.advance(-4)\n    stack.set_long(0, continuation)\n    entered = first_replace(frame, stack_cursor=stack)\nif target == 44872:\n    returned = refresh_gameplay_scene_fields(memory, entered)\nelif entered.stack_cursor is None:\n    clear_scene_video_and_state(memory.state)\n    returned = first_replace(entered, status=None)\nelse:\n    returned = clear_scene_video_and_state_fields(memory, entered)\nreturned = _scene_refresh_frame(memory, returned)\nmemory.sync_status(returned)\nif frame.stack_cursor is not None:\n    actual = returned.stack_cursor.long()\n    if actual != continuation:\n        raise SceneRefreshBoundary(actual, returned, continuation)\n    returned = first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))\nreturn returned"}})

# Live device integration; ordinary target lowering unchanged.
DECLARATIONS.update({'_video_plane_dma_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, sprite: bool', 'returns': 'FirstDeploymentFrame', 'flow': "if type(sprite) is not bool:\n    raise ValueError('actual video initialization or sprite-plane entry required')\nframe = _scene_refresh_frame(memory, frame)\nframe = first_replace(frame, auxiliary=memory.cursor_at(12582916))\nframe = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, 36609)\nregister = memory.cursor_at(4294964742).word()\nframe = _first_word(frame, 'choice', register)\nframe = _first_byte(frame, 'choice', low8(register) | 16)\nframe = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, register | 16)\nframe = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 4, 2483000391 if sprite else 2483000575)\nframe = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, 38784)\nframe = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 4, 2013266050 if sprite else 1073741952)\nframe = _scene_refresh_emit(memory, frame, 12582912, 2, 246 if sprite else 0)\nwhile True:\n    response = frame.auxiliary.word()\n    frame = _first_word(frame, 'choice', response)\n    frame = _first_word(frame, 'choice', response & 2)\n    if response & 2 == 0:\n        break\n    memory.state.progress('vdp-dma')\n    frame = first_replace(frame, status=memory.state.sr & 31)\nreleased = memory.cursor_at(16727808).byte()\nframe = _scene_refresh_flags(memory, frame, released, 1)\nif released == 0:\n    frame = _scene_refresh_emit(memory, frame, 10555648, 2, 0)\nrestored = memory.cursor_at(4294964742).word()\nframe = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, restored)\nreturn _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, 36610)"}})
