"""Restricted semantic source admission with ordinary mnemonic lowering.

Reads explicit source text only. This is an intermediate structural compiler,
not a general Python compiler or full-console/indirect-handler implementation.
"""
from .compiler_common import CompileError,semantic_functions,lower_declared
from .target import REUSE_BINDINGS

APPROVED={'contexts_reuse': {'ControlChoice',
                    'GlyphColors',
                    'GlyphStreamResult',
                    'SpriteControlContext',
                    'SpriteControlResult'},
 'domain': {'Byte',
            'Cursor',
            'Long',
            'RandomSample',
            'SceneState',
            'Word',
            'checked_cursor',
            'checked_state',
            'descending_inclusive',
            'divu_retained',
            'low16',
            'low8',
            'negative_byte',
            'negative_word',
            'replace_byte',
            'replace_word',
            's16',
            'swap_words',
            'u16',
            'u32',
            'uint'}}

DECLARATIONS={'_control': {'signature': 'state, size, value',
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
 'clear_video_sprite_plane': {'signature': 'state: SceneState',
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
 'enqueue_sound_command': {'signature': 'state: SceneState, command: Byte',
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
 'wait_for_scene_sound_byte': {'signature': 'state: SceneState',
                               'returns': 'None',
                               'flow': 'checked_state(state)\n'
                                       'state.set_status_word(9472)\n'
                                       'while state.read(4294964754, 1) != 0:\n'
                                       "    state.progress('scene-sound-byte')"},
 'expand_glyph_row': {'signature': 'state: SceneState, source: Cursor, background: Byte, foreground: '
                                   'Byte',
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
 'expand_glyph_stream': {'signature': 'state: SceneState, tokens: Cursor, destination: Cursor, colors: '
                                      'GlyphColors, remaining: Long',
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
                                 'return GlyphStreamResult(tokens, destination, replace_word(remaining, '
                                 '65535))'},
 'stage_sprite_word_packet': {'signature': 'state: SceneState, source: Cursor, command: Long, rows: '
                                           'Word, row_command: Word',
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
                                      '            dispatch_offset = u16((token & 32767) >> 7) & 65534\n'
                                      '            relative_target = '
                                      'state.table(158796).word(dispatch_offset)\n'
                                      '            target = u32(158808 + s16(relative_target))\n'
                                      '            result = state.service_at(target, '
                                      'SpriteControlContext(token, command, remaining, source, '
                                      'destination))\n'
                                      '            if type(result) is not SpriteControlResult:\n'
                                      "                raise ValueError('real sprite control result "
                                      "required')\n"
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
 'build_battlefield_outcome_candidates': {'signature': 'state: SceneState',
                                          'returns': 'Word',
                                          'flow': 'checked_state(state)\n'
                                                  'destination = state.action_candidates.cursor()\n'
                                                  "city = state.scalar('battle_scene')\n"
                                                  'count = 0\n'
                                                  'for officer in descending_inclusive(255):\n'
                                                  '    if '
                                                  'state.battlefield_city_assignment.byte(officer) == '
                                                  'low8(city):\n'
                                                  '        if not '
                                                  'negative_byte(state.officer_city_assignment.byte(officer)):\n'
                                                  '            destination.append_word(officer)\n'
                                                  '            count = u16(count + 1)\n'
                                                  'destination.put_word(65535)\n'
                                                  'return count'},
 'step_random': {'signature': 'state: SceneState',
                 'returns': 'Long',
                 'flow': 'return _reuse_advance_random_pair(state).sample'},
 '_reuse_advance_random_pair': {'signature': 'state: SceneState',
                                'returns': 'RandomSample',
                                'flow': 'checked_state(state)\n'
                                        "original = state.scalar('random_seed')\n"
                                        'if original == 0:\n'
                                        '    original = 711800410\n'
                                        'mixed = u32(u32(u32(u32(original << 2) + original) << 3) + '
                                        'original)\n'
                                        'sample = replace_word(original, low16(mixed))\n'
                                        'mixed = swap_words(mixed)\n'
                                        'sample = replace_word(sample, u16(low16(sample) + '
                                        'low16(mixed)))\n'
                                        'mixed = swap_words(replace_word(mixed, low16(sample)))\n'
                                        "state.set_scalar('random_seed', mixed)\n"
                                        'return RandomSample(sample, mixed)'},
 '_choose_duel_control': {'signature': 'state: SceneState, command_carrier: Long, mode_carrier: Long, '
                                       'primary_address: Long, secondary_address: Long',
                          'returns': 'ControlChoice',
                          'flow': 'checked_state(state)\n'
                                  'uint(command_carrier, 32)\n'
                                  'uint(mode_carrier, 32)\n'
                                  'selected = replace_word(command_carrier, state.read(4294964738, 2))\n'
                                  'mode_carrier = replace_byte(mode_carrier, '
                                  'state.read(primary_address, 1))\n'
                                  'if low8(mode_carrier) == 0:\n'
                                  '    return ControlChoice(selected, mode_carrier)\n'
                                  'selected = replace_word(selected, state.read(4294964740, 2))\n'
                                  'if low8(mode_carrier) == 1:\n'
                                  '    return ControlChoice(selected, mode_carrier)\n'
                                  'mode_carrier = replace_byte(mode_carrier, '
                                  'state.read(secondary_address, 1))\n'
                                  'if low8(mode_carrier) == 1:\n'
                                  '    return ControlChoice(selected, mode_carrier)\n'
                                  'selected = replace_word(selected, state.read(4294964738, 2))\n'
                                  'return ControlChoice(selected, mode_carrier)'},
 'choose_first_duel_control': {'signature': 'state: SceneState, command_carrier: Long, mode_carrier: '
                                            'Long',
                               'returns': 'ControlChoice',
                               'flow': 'return _choose_duel_control(state, command_carrier, '
                                       'mode_carrier, 16740362, 16740363)'},
 'choose_second_duel_control': {'signature': 'state: SceneState, command_carrier: Long, mode_carrier: '
                                             'Long',
                                'returns': 'ControlChoice',
                                'flow': 'return _choose_duel_control(state, command_carrier, '
                                        'mode_carrier, 16740363, 16740362)'},
 'distribute_battle_progress_tail': {'signature': 'state: SceneState, count: Word, budget: Word',
                                     'returns': 'None',
                                     'flow': 'checked_state(state)\n'
                                             'uint(count, 16)\n'
                                             'uint(budget, 16)\n'
                                             'if count == 0:\n'
                                             '    return\n'
                                             'award = divu_retained(budget, count)\n'
                                             'roster = state.table(4294955776).cursor()\n'
                                             'ability, progress = (state.table(4294950912), '
                                             'state.table(4294950400))\n'
                                             'while True:\n'
                                             '    member = roster.next_word()\n'
                                             '    if negative_word(member):\n'
                                             '        return\n'
                                             '    offset = u16(member << 1)\n'
                                             '    current = ability.word(offset)\n'
                                             '    if current > progress.word(offset):\n'
                                             '        ability.set_word(offset, min(u16(current + '
                                             'low16(award)), 999))\n'
                                             '    else:\n'
                                             '        current = progress.word(offset)\n'
                                             '        progress.set_word(offset, min(u16(current + '
                                             'low16(award)), 999))',
                                     'slots': {999: ('progress_ceiling', 0, 65535)}}}

def _lower_clear_video_sprite_plane(emitter,rules):
    emitter.segment(0x68ce,0x6950)
    emitter.ins('lea.l','0xc00004:l,%a6',6)
    emitter.ins('move.w','#0x8f01,(%a6)',4)
    emitter.ins('move.w','0xf606:w,%d7',4)
    emitter.ins('ori.b','#0x10,%d7',4)
    emitter.ins('move.w','%d7,(%a6)',2)
    emitter.ins('move.l','#0x93ff9447,(%a6)',6)
    emitter.ins('move.w','#0x9780,(%a6)',4)
    emitter.ins('move.l','#0x78000082,(%a6)',6)
    emitter.ins('move.w','#0xf6,0xc00000:l',8)
    emitter.ins('move.w','(%a6),%d7',2)
    emitter.ins('andi.w','#0x2,%d7',4)
    emitter.ins('bne.b','scene_pc_0068fa',2)
    emitter.ins('tst.b','0xff3f00:l',6)
    emitter.ins('bne.b','scene_pc_006912',2)
    emitter.ins('move.w','#0x0,0xa11100:l',8)
    emitter.ins('move.w','0xf606:w,(%a6)',4)
    emitter.ins('move.w','#0x8f02,(%a6)',4)
    emitter.ins('move.l','#0x40000010,0xc00004:l',10)
    emitter.ins('move.l','#0x0,0xc00000:l',10)
    emitter.ins('move.l','#0x0,0xf312:w',8)
    emitter.ins('move.l','#0x0,0xf316:w',8)
    emitter.ins('lea.l','0xf800:w,%a6',4)
    emitter.ins('moveq','#0,%d7',2)
    emitter.ins('move.w','#0x9f,%d6',4)
    emitter.ins('move.l','%d7,(%a6)+',2)
    emitter.ins('dbra','%d6,scene_pc_006948',4)
    emitter.ins('rts','',2)

def _lower_enqueue_sound_command(emitter,rules):
    emitter.segment(0x808a,0x80d0)
    emitter.ins('st.b','0xff3f00:l',6)
    emitter.ins('move.w','#0x100,0xa11100:l',8)
    emitter.ins('btst.b','#0x0,0xa11100:l',8)
    emitter.ins('bne.b','scene_pc_008098',2)
    emitter.ins('tst.b','0xa01c0a:l',6)
    emitter.ins('beq.b','scene_pc_0080ba',2)
    emitter.ins('tst.b','0xa01c0b:l',6)
    emitter.ins('bne.b','scene_pc_0080c0',2)
    emitter.ins('move.b','%d0,0xa01c0b:l',6)
    emitter.ins('bra.b','scene_pc_0080c0',2)
    emitter.ins('move.b','%d0,0xa01c0a:l',6)
    emitter.ins('sf.b','0xff3f00:l',6)
    emitter.ins('move.w','#0x0,0xa11100:l',8)
    emitter.ins('rts','',2)

def _lower_wait_for_scene_sound_byte(emitter,rules):
    emitter.segment(0x83c8,0x83d4)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('tst.b','0xf612:w',4)
    emitter.ins('bne.b','scene_pc_0083cc',2)
    emitter.ins('rts','',2)

def _lower_step_random(emitter,rules):
    emitter.segment(0x83d4,0x83fa)
    emitter.ins('move.l','0xf61c:w,%d1',4)
    emitter.ins('bne.b','scene_pc_0083e0',2)
    emitter.ins('move.l','#0x2a6d365a,%d1',6)
    emitter.ins('move.l','%d1,%d0',2)
    emitter.ins('asl.l','#0x2,%d1',2)
    emitter.ins('add.l','%d0,%d1',2)
    emitter.ins('asl.l','#0x3,%d1',2)
    emitter.ins('add.l','%d0,%d1',2)
    emitter.ins('move.w','%d1,%d0',2)
    emitter.ins('swap','%d1',2)
    emitter.ins('add.w','%d1,%d0',2)
    emitter.ins('move.w','%d0,%d1',2)
    emitter.ins('swap','%d1',2)
    emitter.ins('move.l','%d1,0xf61c:w',4)
    emitter.ins('rts','',2)

def _lower_expand_glyph_row(emitter,rules):
    emitter.segment(0xaf04,0xaf1e)
    emitter.ins('moveq','#0,%d7',2)
    emitter.ins('move.b','(%a2)+,%d6',2)
    emitter.ins('move.w','#0x7,%d4',4)
    emitter.ins('lsl.l','#0x4,%d7',2)
    emitter.ins('roxl.b','#0x1,%d6',2)
    emitter.ins('bcc.b','scene_pc_00af16',2)
    emitter.ins('or.b','%d1,%d7',2)
    emitter.ins('bra.b','scene_pc_00af18',2)
    emitter.ins('or.b','%d0,%d7',2)
    emitter.ins('dbra','%d4,scene_pc_00af0c',4)
    emitter.ins('rts','',2)

def _lower_expand_glyph_stream(emitter,rules):
    emitter.segment(0xaf1e,0xaf48)
    emitter.ins('movem.l','%d4-%d7,-(%a7)',4)
    emitter.ins('clr.w','%d4',2)
    emitter.ins('move.b','(%a0)+,%d4',2)
    emitter.ins('lsl.w','#0x3,%d4',2)
    emitter.ins('lea.l','0x896dc:l,%a2',6)
    emitter.ins('lea.l','(%a2, %d4.w),%a2',4)
    emitter.ins('move.w','#0x7,%d5',4)
    emitter.ins('bsr.b','scene_pc_00af04',2)
    emitter.ins('move.l','%d7,(%a1)+',2)
    emitter.ins('dbra','%d5,scene_pc_00af36',4)
    emitter.ins('dbra','%d3,scene_pc_00af22',4)
    emitter.ins('movem.l','(%a7)+,%d4-%d7',4)
    emitter.ins('rts','',2)

def _lower_build_battlefield_outcome_candidates(emitter,rules):
    emitter.segment(0x1c2c8,0x1c2fc)
    emitter.ins('lea.l','0xa050:w,%a0',4)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('lea.l','0xcc00:w,%a2',4)
    emitter.ins('move.w','0xf68a:w,%d0',4)
    emitter.ins('move.w','#0xff,%d2',4)
    emitter.ins('clr.w','%d3',2)
    emitter.ins('cmp.b','(%a0, %d2.w),%d0',4)
    emitter.ins('bne.w','scene_pc_01c2f2',4)
    emitter.ins('tst.b','(%a2, %d2.w)',4)
    emitter.ins('bmi.w','scene_pc_01c2f2',4)
    emitter.ins('move.w','%d2,(%a1)+',2)
    emitter.ins('addq.w','#0x1,%d3',2)
    emitter.ins('dbra','%d2,scene_pc_01c2de',4)
    emitter.ins('move.w','#0xffff,(%a1)',4)
    emitter.ins('rts','',2)

def _lower_distribute_battle_progress_tail(emitter,rules):
    emitter.segment(0x1c586,0x1c5e2)
    emitter.ins('tst.w','%d3',2)
    emitter.ins('beq.w','scene_pc_01c5e0',4)
    emitter.ins('andi.l','#0xffff,%d0',6)
    emitter.ins('divu.w','%d3,%d0',2)
    emitter.ins('lea.l','0xd300:w,%a0',4)
    emitter.ins('lea.l','0xc000:w,%a1',4)
    emitter.ins('lea.l','0xbe00:w,%a2',4)
    emitter.ins('move.w','(%a0)+,%d1',2)
    emitter.ins('bmi.w','scene_pc_01c5e0',4)
    emitter.ins('lsl.w','#0x1,%d1',2)
    emitter.ins('move.w','(%a1, %d1.w),%d2',4)
    emitter.ins('cmp.w','(%a2, %d1.w),%d2',4)
    emitter.ins('bls.w','scene_pc_01c5c8',4)
    emitter.ins('add.w','%d0,%d2',2)
    emitter.ins('cmpi.w','#'+hex(rules['progress_ceiling'])+',%d2',4)
    emitter.ins('bls.w','scene_pc_01c5c2',4)
    emitter.ins('move.w','#'+hex(rules['progress_ceiling'])+',%d2',4)
    emitter.ins('move.w','%d2,(%a1, %d1.w)',4)
    emitter.ins('bra.b','scene_pc_01c5a0',2)
    emitter.ins('move.w','(%a2, %d1.w),%d2',4)
    emitter.ins('add.w','%d0,%d2',2)
    emitter.ins('cmpi.w','#'+hex(rules['progress_ceiling'])+',%d2',4)
    emitter.ins('bls.w','scene_pc_01c5da',4)
    emitter.ins('move.w','#'+hex(rules['progress_ceiling'])+',%d2',4)
    emitter.ins('move.w','%d2,(%a2, %d1.w)',4)
    emitter.ins('bra.b','scene_pc_01c5a0',2)
    emitter.ins('rts','',2)

def _lower_stage_sprite_word_packet(emitter,rules):
    emitter.segment(0x26bfa,0x26c4c)
    emitter.ins('lea.l','0xd100:w,%a1',4)
    emitter.ins('adda.w','0xf31a:w,%a1',4)
    emitter.ins('move.w','%d1,%d7',2)
    emitter.ins('subq.w','#0x1,%d7',2)
    emitter.ins('move.w','%d0,(%a1)+',2)
    emitter.ins('move.w','%d2,(%a1)+',2)
    emitter.ins('addi.w','#0x80,%d2',4)
    emitter.ins('move.w','%d0,%d3',2)
    emitter.ins('move.w','(%a0)+,%d4',2)
    emitter.ins('bmi.b','scene_pc_026c22',2)
    emitter.ins('swap','%d0',2)
    emitter.ins('or.w','%d0,%d4',2)
    emitter.ins('move.w','%d4,(%a1)+',2)
    emitter.ins('swap','%d0',2)
    emitter.ins('subq.w','#0x1,%d3',2)
    emitter.ins('bra.w','scene_pc_026c36',4)
    emitter.ins('move.w','%d4,%d5',2)
    emitter.ins('andi.w','#0x7fff,%d4',4)
    emitter.ins('lsr.w','#0x7,%d4',2)
    emitter.ins('bclr.l','#0x0,%d4',4)
    emitter.ins('move.w','28(%pc, %d4.w),%d4',4)
    emitter.ins('jsr','36(%pc, %d4.w)',4)
    emitter.ins('tst.w','%d3',2)
    emitter.ins('bne.b','scene_pc_026c10',2)
    emitter.ins('dbra','%d7,scene_pc_026c06',4)
    emitter.ins('clr.w','(%a1)',2)
    emitter.ins('addq.w','#0x2,%d0',2)
    emitter.ins('mulu.w','%d1,%d0',2)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('add.w','%d0,0xf31a:w',4)
    emitter.ins('rts','',2)

def _lower_choose_first_duel_control(emitter,rules):
    emitter.segment(0x279e6,0x27a10)
    emitter.ins('move.w','0xf602:w,%d0',4)
    emitter.ins('move.b','0xff700a:l,%d1',6)
    emitter.ins('tst.b','%d1',2)
    emitter.ins('beq.b','scene_pc_027a0e',2)
    emitter.ins('move.w','0xf604:w,%d0',4)
    emitter.ins('cmpi.b','#0x1,%d1',4)
    emitter.ins('beq.b','scene_pc_027a0e',2)
    emitter.ins('move.b','0xff700b:l,%d1',6)
    emitter.ins('cmpi.b','#0x1,%d1',4)
    emitter.ins('beq.b','scene_pc_027a0e',2)
    emitter.ins('move.w','0xf602:w,%d0',4)
    emitter.ins('rts','',2)

def _lower_choose_second_duel_control(emitter,rules):
    emitter.segment(0x27a10,0x27a3a)
    emitter.ins('move.w','0xf602:w,%d0',4)
    emitter.ins('move.b','0xff700b:l,%d1',6)
    emitter.ins('tst.b','%d1',2)
    emitter.ins('beq.b','scene_pc_027a38',2)
    emitter.ins('move.w','0xf604:w,%d0',4)
    emitter.ins('cmpi.b','#0x1,%d1',4)
    emitter.ins('beq.b','scene_pc_027a38',2)
    emitter.ins('move.b','0xff700a:l,%d1',6)
    emitter.ins('cmpi.b','#0x1,%d1',4)
    emitter.ins('beq.b','scene_pc_027a38',2)
    emitter.ins('move.w','0xf602:w,%d0',4)
    emitter.ins('rts','',2)

LOWERERS={
    'clear_video_sprite_plane':_lower_clear_video_sprite_plane,
    'enqueue_sound_command':_lower_enqueue_sound_command,
    'wait_for_scene_sound_byte':_lower_wait_for_scene_sound_byte,
    'step_random':_lower_step_random,
    'expand_glyph_row':_lower_expand_glyph_row,
    'expand_glyph_stream':_lower_expand_glyph_stream,
    'build_battlefield_outcome_candidates':_lower_build_battlefield_outcome_candidates,
    'distribute_battle_progress_tail':_lower_distribute_battle_progress_tail,
    'stage_sprite_word_packet':_lower_stage_sprite_word_packet,
    'choose_first_duel_control':_lower_choose_first_duel_control,
    'choose_second_duel_control':_lower_choose_second_duel_control,
}

# Complete supplied initialization contracts; finite host admission, not general Python lowering.
# Original physical emitters and default instruction topology remain unchanged.
HOST_INITIALIZATION_DECLARATIONS = {'_save_glyph_values': {'signature': 'state, saved, include_source',
                        'returns': None,
                        'flow': 'if type(saved) is not GlyphSavedValues:\n'
                                "    raise ValueError('actual glyph MOVEM operands required')\n"
                                'saved.validate(state)\n'
                                'values = (saved.working, saved.repeat, saved.response, saved.pixels)\n'
                                'if include_source:\n'
                                '    values += (saved.glyph_source.base,)\n'
                                'for value in values[::-1]:\n'
                                '    saved.stack.base = u32(saved.stack.base - 4)\n'
                                '    saved.stack.set_long(0, value)'},
 '_restore_glyph_values': {'signature': 'state, saved, glyph_source, include_source',
                           'returns': None,
                           'flow': 'working, repeat, response, pixels = tuple((saved.stack.next_long() for _ '
                                   'in range(4)))\n'
                                   'if include_source:\n'
                                   '    glyph_source = state.table(saved.stack.next_long())\n'
                                   'return GlyphSavedValues(working, repeat, response, pixels, glyph_source, '
                                   'saved.stack).validate(state)'},
 'clear_video_sprite_plane': {'signature': 'state: SceneState, response: Long | None=None',
                              'returns': 'VideoClearResult | None',
                              'flow': 'checked_state(state)\n'
                                      'if response is not None:\n'
                                      '    uint(response, 32)\n'
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
                                      '    destination.append_long(0)\n'
                                      'if response is not None:\n'
                                      '    return VideoClearResult(replace_word(response, 65535), 0, '
                                      'destination).validate(state)\n'
                                      'return None'},
 'expand_glyph_stream': {'signature': 'state: SceneState, tokens: Cursor, destination: Cursor, colors: '
                                      'GlyphColors, remaining: Long, saved: GlyphSavedValues | None=None',
                         'returns': 'GlyphStreamResult',
                         'flow': 'checked_state(state)\n'
                                 'checked_cursor(tokens, state)\n'
                                 'checked_cursor(destination, state)\n'
                                 'if type(colors) is not GlyphColors:\n'
                                 "    raise ValueError('explicit glyph colors required')\n"
                                 'colors.__post_init__()\n'
                                 'uint(remaining, 32)\n'
                                 'if saved is not None:\n'
                                 '    _save_glyph_values(state, saved, False)\n'
                                 'source = None\n'
                                 'for _ in descending_inclusive(low16(remaining)):\n'
                                 '    glyph = u16(tokens.next_byte() << 3)\n'
                                 '    source = state.table(562908).cursor(glyph)\n'
                                 '    for _ in descending_inclusive(7):\n'
                                 '        destination.append_long(expand_glyph_row(state, source, '
                                 'low8(colors.background), low8(colors.foreground)))\n'
                                 'if saved is not None:\n'
                                 '    if source is None:\n'
                                 "        raise ValueError('inclusive glyph loop must define its current "
                                 "source')\n"
                                 '    saved = _restore_glyph_values(state, saved, source, False)\n'
                                 'return GlyphStreamResult(tokens, destination, replace_word(remaining, '
                                 '65535), saved)'},
 'stage_sprite_word_packet': {'signature': 'state: SceneState, source: Cursor, command: Long, rows: Word, '
                                           'row_command: Word, current: SpritePacketContext | None=None',
                              'returns': 'Long | SpritePacketContext',
                              'flow': 'checked_state(state)\n'
                                      'checked_cursor(source, state)\n'
                                      'uint(command, 32)\n'
                                      'uint(rows, 16)\n'
                                      'uint(row_command, 16)\n'
                                      'if current is not None:\n'
                                      '    if type(current) is not SpritePacketContext:\n'
                                      "        raise ValueError('actual complete packet operands required')\n"
                                      '    current.validate(state)\n'
                                      '    if (current.command, low16(current.rows), '
                                      'low16(current.row_command)) != (command, rows, row_command) or '
                                      'current.source is not source:\n'
                                      "        raise ValueError('packet arguments must agree with current "
                                      "caller')\n"
                                      '    rows_carrier, row_carrier = (current.rows, current.row_command)\n'
                                      '    remaining_carrier, token_carrier = (current.remaining, '
                                      'current.token)\n'
                                      '    run_count, response = (current.run_count, current.response)\n'
                                      '    rows_remaining = replace_word(current.rows_remaining, u16(rows - '
                                      '1))\n'
                                      '    glyph_source = current.glyph_source\n'
                                      'destination = state.table(4294955264).cursor(state.read(4294963994, '
                                      '2))\n'
                                      'for _ in descending_inclusive(u16(rows - 1)):\n'
                                      '    destination.append_word(low16(command))\n'
                                      '    destination.append_word(row_command)\n'
                                      '    row_command = u16(row_command + 128)\n'
                                      '    remaining = low16(command)\n'
                                      '    if current is not None:\n'
                                      '        row_carrier = replace_word(row_carrier, row_command)\n'
                                      '        remaining_carrier = replace_word(remaining_carrier, '
                                      'remaining)\n'
                                      '    while True:\n'
                                      '        token = source.next_word()\n'
                                      '        if negative_word(token):\n'
                                      '            dispatch_offset = u16((token & 32767) >> 7) & 65534\n'
                                      '            relative_target = '
                                      'state.table(158796).word(dispatch_offset)\n'
                                      '            target = u32(158808 + s16(relative_target))\n'
                                      '            if current is None:\n'
                                      '                result = state.service_at(target, '
                                      'SpriteControlContext(token, command, remaining, source, '
                                      'destination))\n'
                                      '                if type(result) is not SpriteControlResult:\n'
                                      "                    raise ValueError('real sprite control result "
                                      "required')\n"
                                      '                result.__post_init__()\n'
                                      '                command, remaining = (result.command, '
                                      'result.row_remaining)\n'
                                      '            else:\n'
                                      '                run_count = replace_word(run_count, token)\n'
                                      '                token_carrier = replace_word(token_carrier, '
                                      'dispatch_offset)\n'
                                      '                result = state.service_at(target, '
                                      'SpritePacketContext(command, rows_carrier, row_carrier, '
                                      'remaining_carrier, token_carrier, run_count, response, '
                                      'rows_remaining, source, destination, glyph_source, current.stack))\n'
                                      '                if type(result) is not SpritePacketContext:\n'
                                      "                    raise ValueError('complete sprite handler return "
                                      "required')\n"
                                      '                result.validate(state)\n'
                                      '                command, rows_carrier, row_carrier = (result.command, '
                                      'result.rows, result.row_command)\n'
                                      '                remaining_carrier, token_carrier = (result.remaining, '
                                      'result.token)\n'
                                      '                run_count, response = (result.run_count, '
                                      'result.response)\n'
                                      '                rows_remaining, source, destination = '
                                      '(result.rows_remaining, result.source, result.destination)\n'
                                      '                glyph_source = result.glyph_source\n'
                                      '                rows, row_command, remaining = (low16(rows_carrier), '
                                      'low16(row_carrier), low16(remaining_carrier))\n'
                                      '        else:\n'
                                      '            command = swap_words(command)\n'
                                      '            tile = u16(token | low16(command))\n'
                                      '            destination.append_word(tile)\n'
                                      '            command = swap_words(command)\n'
                                      '            remaining = u16(remaining - 1)\n'
                                      '            if current is not None:\n'
                                      '                token_carrier = replace_word(token_carrier, tile)\n'
                                      '                remaining_carrier = replace_word(remaining_carrier, '
                                      'remaining)\n'
                                      '        if remaining == 0:\n'
                                      '            break\n'
                                      '    if current is not None:\n'
                                      '        rows_remaining = replace_word(rows_remaining, '
                                      'u16(low16(rows_remaining) - 1))\n'
                                      'destination.put_word(0)\n'
                                      'command = replace_word(command, u16(low16(command) + 2))\n'
                                      'allocated = u16(u16(low16(command) * rows) << 1)\n'
                                      'state.write(4294963994, 2, u16(state.read(4294963994, 2) + '
                                      'allocated))\n'
                                      'command = replace_word(low16(command) * rows, allocated)\n'
                                      'if current is not None:\n'
                                      '    return SpritePacketContext(command, rows_carrier, row_carrier, '
                                      'remaining_carrier, token_carrier, run_count, response, '
                                      'rows_remaining, source, destination, glyph_source, '
                                      'current.stack).validate(state)\n'
                                      'return command'}}
DECLARATIONS.update(HOST_INITIALIZATION_DECLARATIONS)
APPROVED.setdefault('contexts_reuse', set()).update({'GlyphSavedValues', 'SpritePacketContext', 'VideoClearResult'})

# Finite full-body contracts: every supplied core/wrapper effect is admitted.
# These are offline declarations, not a runtime source fallback or old body.
HOST_PACKET_RETURN_DECLARATIONS = {"stage_sprite_word_packet": {"signature": "state: SceneState, source: Cursor, command: Long, rows: Word, row_command: Word, current: SpritePacketContext | None=None",
 "returns": "Long | SpritePacketContext",
 "flow": "checked_state(state)\nchecked_cursor(source, state)\nuint(command, 32)\nuint(rows, 16)\nuint(row_command, 16)\nif current is not None:\n    if type(current) is not SpritePacketContext:\n        raise ValueError('actual complete packet operands required')\n    current.validate(state)\n    if (current.command, low16(current.rows), low16(current.row_command)) != (command, rows, row_command) or current.source is not source:\n        raise ValueError('packet arguments must agree with current caller')\n    rows_carrier, row_carrier = (current.rows, current.row_command)\n    remaining_carrier, token_carrier = (current.remaining, current.token)\n    run_count, response = (current.run_count, current.response)\n    rows_remaining = replace_word(current.rows_remaining, u16(rows - 1))\n    glyph_source = current.glyph_source\n    stack = current.stack\ndestination = state.table(4294955264).cursor(state.read(4294963994, 2))\nrow_counter = u16(rows - 1)\nwhile True:\n    destination.append_word(low16(command))\n    destination.append_word(row_command)\n    row_command = u16(row_command + 128)\n    remaining = low16(command)\n    if current is not None:\n        row_carrier = replace_word(row_carrier, row_command)\n        remaining_carrier = replace_word(remaining_carrier, remaining)\n    while True:\n        token = source.next_word()\n        if negative_word(token):\n            dispatch_offset = u16((token & 32767) >> 7) & 65534\n            relative_target = state.table(158796).word(dispatch_offset)\n            target = u32(158808 + s16(relative_target))\n            if current is None:\n                result = state.service_at(target, SpriteControlContext(token, command, remaining, source, destination))\n                if type(result) is not SpriteControlResult:\n                    raise ValueError('real sprite control result required')\n                result.__post_init__()\n                command, remaining = (result.command, result.row_remaining)\n            else:\n                run_count = replace_word(run_count, token)\n                token_carrier = replace_word(token_carrier, relative_target)\n                result = state.service_at(target, SpritePacketContext(command, rows_carrier, row_carrier, remaining_carrier, token_carrier, run_count, response, rows_remaining, source, destination, glyph_source, stack.advance(-4), False, relative_target == 0, bool(relative_target & 32768), False))\n                if type(result) is not SpritePacketContext:\n                    raise ValueError('complete sprite handler return required')\n                result.validate(state)\n                command, rows_carrier, row_carrier = (result.command, result.rows, result.row_command)\n                remaining_carrier, token_carrier = (result.remaining, result.token)\n                run_count, response = (result.run_count, result.response)\n                rows_remaining, source, destination = (result.rows_remaining, result.source, result.destination)\n                glyph_source = result.glyph_source\n                stack = result.stack.advance(4)\n                rows, row_command, remaining = (low16(rows_carrier), low16(row_carrier), low16(remaining_carrier))\n        else:\n            command = swap_words(command)\n            tile = u16(token | low16(command))\n            destination.append_word(tile)\n            command = swap_words(command)\n            remaining = u16(remaining - 1)\n            if current is not None:\n                token_carrier = replace_word(token_carrier, tile)\n                remaining_carrier = replace_word(remaining_carrier, remaining)\n        if remaining == 0:\n            break\n    if current is not None:\n        rows_remaining = replace_word(rows_remaining, u16(low16(rows_remaining) - 1))\n        row_counter = low16(rows_remaining)\n    else:\n        row_counter = u16(row_counter - 1)\n    if row_counter == 65535:\n        break\ndestination.put_word(0)\ncommand = replace_word(command, u16(low16(command) + 2))\nallocated = u16(u16(low16(command) * rows) << 1)\nqueue_offset = state.read(4294963994, 2)\nnext_queue_offset = u16(queue_offset + allocated)\nstate.write(4294963994, 2, next_queue_offset)\ncommand = replace_word(low16(command) * rows, allocated)\nif current is not None:\n    return SpritePacketContext(command, rows_carrier, row_carrier, remaining_carrier, token_carrier, run_count, response, rows_remaining, source, destination, glyph_source, stack, queue_offset + allocated > 65535, next_queue_offset == 0, bool(next_queue_offset & 32768), bool(~(queue_offset ^ allocated) & (queue_offset ^ next_queue_offset) & 32768)).validate(state)\nreturn command"}}
DECLARATIONS.update(HOST_PACKET_RETURN_DECLARATIONS)

def compile_reuse(source, *, selected_names=None):
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    sole_query_fields = {name: records[name]['effects'] for name in ('choose_duel_control_fields', 'choose_first_duel_control_fields', 'choose_second_duel_control_fields', '_choose_duel_control')}
    for owner in ('choose_first_duel_control', 'choose_second_duel_control'):
        records[owner]['effects'] = dict(previous_projection=records[owner]['effects'], sole_live_query_fields=sole_query_fields)
    if selected_names is not None:
        if type(selected_names) is not tuple or selected_names != SELECTED_DEFAULT_NAMES:
            raise CompileError('fixed whole default family required')
        selected_bindings = tuple((binding for binding in REUSE_BINDINGS if binding.name in selected_names))
        if len(selected_bindings) != len(selected_names):
            raise CompileError('all selected whole owners required')
        return lower_declared(records, selected_bindings, {name: LOWERERS[name] for name in selected_names})
    return lower_declared(records, REUSE_BINDINGS, LOWERERS)

# B19 Scene historical projections of sole808A/83C8 algorithm.
APPROVED.setdefault('contexts_reuse',set()).update({'FirstDeploymentFrame', 'wait_for_scene_sound_byte_fields', 'SceneRefreshMemory', 'enqueue_sound_command_fields'})
DECLARATIONS.update({'enqueue_sound_command': {'flow': 'checked_state(state)\n'
                                   'enqueue_sound_command_fields(SceneRefreshMemory(state), '
                                   'FirstDeploymentFrame.unobserved(), command)',
                           'returns': 'None',
                           'signature': 'state: SceneState, command: Byte'},
 'wait_for_scene_sound_byte': {'flow': 'checked_state(state)\n'
                                       'wait_for_scene_sound_byte_fields(SceneRefreshMemory(state), '
                                       'FirstDeploymentFrame.unobserved())',
                               'returns': 'None',
                               'signature': 'state: SceneState'}})

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
APPROVED.setdefault('business_scene',set()).update({'expand_glyph_stream_fields', 'expand_glyph_row_fields'})
APPROVED.setdefault('contexts_scene',set()).update({'first_replace'})
DECLARATIONS.update({'expand_glyph_row': {'signature': 'state: SceneState, source: Cursor, background: Byte, foreground: Byte',
                      'returns': 'Long',
                      'flow': 'from .business_scene import expand_glyph_row_fields\n'
                              'from .contexts_scene import first_replace\n'
                              'checked_state(state)\n'
                              'checked_cursor(source, state)\n'
                              'uint(background, 8)\n'
                              'uint(foreground, 8)\n'
                              'entered = first_replace(FirstDeploymentFrame.unobserved(), '
                              'target_x=background, target_y=foreground, controller=source.advance(0))\n'
                              'actual = expand_glyph_row_fields(SceneRefreshMemory(state), entered)\n'
                              'source.base = actual.controller.base\n'
                              'return actual.choice'},
 'expand_glyph_stream': {'signature': 'state: SceneState, tokens: Cursor, destination: Cursor, colors: '
                                      'GlyphColors, remaining: Long, saved: GlyphSavedValues | None=None',
                         'returns': 'GlyphStreamResult',
                         'flow': 'from .business_scene import expand_glyph_stream_fields\n'
                                 'from .contexts_scene import first_replace\n'
                                 'checked_state(state)\n'
                                 'checked_cursor(tokens, state)\n'
                                 'checked_cursor(destination, state)\n'
                                 'if type(colors) is not GlyphColors:\n'
                                 "    raise ValueError('explicit glyph colors required')\n"
                                 'colors.__post_init__()\n'
                                 'uint(remaining, 32)\n'
                                 'if saved is not None:\n'
                                 '    _save_glyph_values(state, saved, False)\n'
                                 'entered = first_replace(FirstDeploymentFrame.unobserved(), '
                                 'roster=tokens.advance(0), candidates=destination.advance(0), '
                                 'target_x=colors.background, target_y=colors.foreground, count=remaining)\n'
                                 'actual = expand_glyph_stream_fields(SceneRefreshMemory(state), entered)\n'
                                 'tokens.base, destination.base = (actual.roster.base, '
                                 'actual.candidates.base)\n'
                                 'if saved is not None:\n'
                                 '    saved = _restore_glyph_values(state, saved, actual.controller, False)\n'
                                 'return GlyphStreamResult(tokens, destination, actual.count, saved)'}})

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
APPROVED.setdefault('business_services',set()).update({'clear_video_sprite_plane_fields'})
APPROVED.setdefault('contexts_scene',set()).update({'first_replace'})
DECLARATIONS.update({'clear_video_sprite_plane': {'signature': 'state: SceneState, response: Long | None=None',
                              'returns': 'VideoClearResult | None',
                              'flow': 'from ..high_level_gameplay_flow.business_services import '
                                      'clear_video_sprite_plane_fields\n'
                                      'from .contexts_scene import first_replace\n'
                                      'checked_state(state)\n'
                                      'if response is not None:\n'
                                      '    uint(response, 32)\n'
                                      'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                      'offset_y=response)\n'
                                      'actual = clear_video_sprite_plane_fields(SceneRefreshMemory(state), '
                                      'frame)\n'
                                      'if response is not None:\n'
                                      '    return VideoClearResult(actual.offset_y, actual.choice, '
                                      'actual.auxiliary).validate(state)\n'
                                      'return None'}})

DECLARATIONS.update({'_choose_duel_control': {'signature': 'state: SceneState, command_carrier: Long, mode_carrier: Long, primary_address: Long, secondary_address: Long', 'returns': 'ControlChoice', 'flow': "from .contexts_scene import first_replace\nchecked_state(state)\nuint(command_carrier, 32)\nuint(mode_carrier, 32)\nif (primary_address, secondary_address) not in ((16740362, 16740363), (16740363, 16740362)):\n    raise ValueError('one of the actual two control-query roles required')\nentered = first_replace(FirstDeploymentFrame.unobserved(), target_x=command_carrier, target_y=mode_carrier)\nactual = choose_duel_control_fields(state, entered, primary_address == 16740363)\nreturn ControlChoice(actual.target_x, actual.target_y)"}})

DECLARATIONS.update({'choose_duel_control_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, second: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_battle_ai.business_formation import _first_word, _first_byte\nfrom ..high_level_battle_ai.business_geometry import _contact_status\nchecked_state(state)\nif type(frame) is not FirstDeploymentFrame or type(second) is not bool:\n    raise ValueError('actual current control-query fields and original side required')\nframe.validate(state, frame.stack_cursor is not None)\nuint(frame.target_x, 32)\nuint(frame.target_y, 32)\nprimary, secondary = (16740363, 16740362) if second else (16740362, 16740363)\nframe = _first_word(frame, 'target_x', state.read(4294964738, 2))\nframe = _first_byte(frame, 'target_y', state.read(primary, 1))\nmode = low8(frame.target_y)\nframe = _contact_status(frame, mode, 8)\nif mode != 0:\n    frame = _first_word(frame, 'target_x', state.read(4294964740, 2))\n    value = mode - 1 & 255\n    frame = _contact_status(frame, value, 8, mode < 1, bool((mode ^ 1) & (mode ^ value) & 128))\n    if mode != 1:\n        frame = _first_byte(frame, 'target_y', state.read(secondary, 1))\n        mode = low8(frame.target_y)\n        value = mode - 1 & 255\n        frame = _contact_status(frame, value, 8, mode < 1, bool((mode ^ 1) & (mode ^ value) & 128))\n        if mode != 1:\n            frame = _first_word(frame, 'target_x', state.read(4294964738, 2))\nif frame.status is not None:\n    state.sr = state.sr & 65504 | frame.status\nreturn frame.validate(state, frame.stack_cursor is not None)"}})

DECLARATIONS.update({'choose_first_duel_control_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return choose_duel_control_fields(state, frame, False)'}})

DECLARATIONS.update({'choose_second_duel_control_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return choose_duel_control_fields(state, frame, True)'}})

DECLARATIONS.update({'choose_first_duel_control': {'signature': 'state: SceneState, command_carrier: Long, mode_carrier: Long', 'returns': 'ControlChoice', 'flow': 'return _choose_duel_control(state, command_carrier, mode_carrier, 16740362, 16740363)'}})

DECLARATIONS.update({'choose_second_duel_control': {'signature': 'state: SceneState, command_carrier: Long, mode_carrier: Long', 'returns': 'ControlChoice', 'flow': 'return _choose_duel_control(state, command_carrier, mode_carrier, 16740363, 16740362)'}})

APPROVED.setdefault('contexts_scene',set()).add('first_replace')
APPROVED.setdefault('high_level_battle_ai.business_formation',set()).update({'_first_word','_first_byte'})
APPROVED.setdefault('high_level_battle_ai.business_geometry',set()).add('_contact_status')

SELECTED_DEFAULT_NAMES = ('choose_first_duel_control', 'choose_second_duel_control')

APPROVED.setdefault((2, 'high_level_battle_ai.business_formation'),set()).update(['_first_byte', '_first_word'])

APPROVED.setdefault((2, 'high_level_battle_ai.business_geometry'),set()).update(['_contact_status'])

APPROVED.setdefault((2, 'high_level_gameplay_flow.business_services'),set()).update(['clear_video_sprite_plane_fields'])
