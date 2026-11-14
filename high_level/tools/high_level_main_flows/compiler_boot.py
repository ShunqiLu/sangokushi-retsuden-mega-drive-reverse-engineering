"""Restricted business-text admission and ordinary mnemonic lowering.
An intermediate fixed-structure compiler, not arbitrary Python or CPU proof.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import BUSINESS_BOOT_BINDINGS

APPROVED={'business_main': {'dispatch_main_scene_slot'},
 'contexts_boot': {'ResetProfile', 'BootstrapOutcome'},
 'contexts_main': {'SceneTick'},
 'domain': {'Cursor',
            'Long',
            'SceneState',
            'checked_state',
            'data_view',
            'descending_inclusive',
            'low16',
            'negative_long',
            'ram_view',
            'replace_byte',
            'replace_word',
            's16',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'},
 'services': {'call_target', 'initialize_video_registers_and_planes'}}

DECLARATIONS={'_ram': {'signature': 'state, address',
          'returns': None,
          'flow': "return ram_view(state, 'ram_%04x' % address)"},
 '_checksum_failed': {'signature': 'state',
                      'returns': None,
                      'flow': 'initialize_video_registers_and_planes(state)\n'
                              'state.write(12582916, 4, 3221225472)\n'
                              'for _ in range(64):\n'
                              '    state.write(12582912, 2, 14)\n'
                              'while True:\n'
                              "    state.progress('fatal cartridge checksum loop')"},
 'reset_console': {'signature': 'state: SceneState, profile: ResetProfile',
                   'returns': None,
                   'flow': 'checked_state(state)\n'
                           'if type(profile) is not ResetProfile:\n'
                           "    raise ValueError('explicit ResetProfile required')\n"
                           'profile.validate(state)\n'
                           'if state.read(10551304, 4) == 0 and state.read(10551308, 2) == 0:\n'
                           '    configuration = profile.configuration\n'
                           '    register_word = u32(s16(configuration.next_word()))\n'
                           '    clear_counter = configuration.next_word()\n'
                           '    register_increment = u32(s16(configuration.next_word()))\n'
                           '    sound_memory = configuration.next_long()\n'
                           '    sound_bus = configuration.next_long()\n'
                           '    sound_reset = configuration.next_long()\n'
                           '    video_data = configuration.next_long()\n'
                           '    video_control = configuration.next_long()\n'
                           '    version = state.read(u32(sound_bus - 4351), 1) & 15\n'
                           '    if version:\n'
                           '        state.write(u32(sound_bus + 12032), 4, 1397049153)\n'
                           '    state.read(video_control, 2)\n'
                           '    profile.processor.set_user_stack(state, 0)\n'
                           '    for _ in range(24):\n'
                           '        register_word = replace_byte(register_word, '
                           'configuration.next_byte())\n'
                           '        state.write(video_control, 2, low16(register_word))\n'
                           '        register_word = replace_word(register_word, '
                           'u16(low16(register_word) + low16(register_increment)))\n'
                           '    state.write(video_control, 4, configuration.next_long())\n'
                           '    state.write(video_data, 2, 0)\n'
                           '    state.write(sound_bus, 2, low16(register_increment))\n'
                           '    state.write(sound_reset, 2, low16(register_increment))\n'
                           '    while state.read(sound_bus, 1) & 1:\n'
                           "        state.progress('reset sound bus request')\n"
                           '    for _ in range(38):\n'
                           '        state.write(sound_memory, 1, configuration.next_byte())\n'
                           '        sound_memory = u32(sound_memory + 1)\n'
                           '    state.write(sound_reset, 2, 0)\n'
                           '    state.write(sound_bus, 2, 0)\n'
                           '    state.write(sound_reset, 2, low16(register_increment))\n'
                           '    clear_address = 0\n'
                           '    for _ in descending_inclusive(clear_counter):\n'
                           '        clear_address = u32(clear_address - 4)\n'
                           '        state.write(clear_address, 4, 0)\n'
                           '    state.write(video_control, 4, configuration.next_long())\n'
                           '    state.write(video_control, 4, configuration.next_long())\n'
                           '    for _ in range(32):\n'
                           '        state.write(video_data, 4, 0)\n'
                           '    state.write(video_control, 4, configuration.next_long())\n'
                           '    for _ in range(20):\n'
                           '        state.write(video_data, 4, 0)\n'
                           '    for _ in range(4):\n'
                           '        state.write(u32(video_data + 17), 1, configuration.next_byte())\n'
                           '    state.write(sound_reset, 2, 0)\n'
                           '    outcome = profile.processor.restore_zeroed_bootstrap_context(state, '
                           'state.table_at(clear_address).cursor())\n'
                           '    if type(outcome) is not BootstrapOutcome:\n'
                           "        raise ValueError('real bootstrap status carrier required')\n"
                           '    outcome.validate(state)\n'
                           '    state.set_status_word(9984)\n'
                           '    profile = ResetProfile(profile.processor, configuration, '
                           'outcome.status_carrier)\n'
                           'return start_game_main_loop(state, profile)'},
 'start_game_main_loop': {'signature': 'state: SceneState, profile: ResetProfile',
                          'returns': None,
                          'flow': 'checked_state(state)\n'
                                  'if type(profile) is not ResetProfile:\n'
                                  "    raise ValueError('explicit ResetProfile required')\n"
                                  'profile.validate(state)\n'
                                  'state.read(12582916, 2)\n'
                                  'status = profile.retained_status_carrier\n'
                                  'while True:\n'
                                  '    status = replace_word(status, state.read(12582916, 2) & 2)\n'
                                  '    if low16(status) == 0:\n'
                                  '        break\n'
                                  "    state.progress('bootstrap VDP DMA wait')\n"
                                  'initialization_retained = bool(state.read(10551309, 1) & 64)\n'
                                  'if not initialization_retained or _ram(state, 65532).long() != '
                                  '1768843636:\n'
                                  "    end_address = data_view(state, 'data_0001a4').long()\n"
                                  '    length = u32(u32(end_address + 1) - 512)\n'
                                  '    length = length >> 1 | length & 2147483648\n'
                                  '    first_count, outer_count = (u16(low16(length) - 1), length >> 16 '
                                  '& 65535)\n'
                                  "    source, checksum = (data_view(state, 'data_000200').cursor(), "
                                  '0)\n'
                                  '    for block in descending_inclusive(outer_count):\n'
                                  '        count = first_count if block == outer_count else 65535\n'
                                  '        for _ in descending_inclusive(count):\n'
                                  '            checksum = u16(checksum + source.next_word())\n'
                                  "    if checksum != data_view(state, 'data_00018e').word():\n"
                                  '        return _checksum_failed(state)\n'
                                  '    destination = _ram(state, 65024).cursor()\n'
                                  '    for _ in range(128):\n'
                                  '        destination.append_long(0)\n'
                                  '    _ram(state, 65532).set_long(0, 1768843636)\n'
                                  'destination = state.table_at(16711680).cursor()\n'
                                  'for _ in range(16256):\n'
                                  '    destination.append_long(0)\n'
                                  'profile.processor.set_supervisor_stack(state, 16776704)\n'
                                  'initialize_video_registers_and_planes(state)\n'
                                  'call_target(state, 26960, SceneTick())\n'
                                  'call_target(state, 26548, SceneTick())\n'
                                  '_ram(state, 62218).set_word(0, 80)\n'
                                  '_ram(state, 62220).set_word(0, 160)\n'
                                  '_ram(state, 62222).set_word(0, 6144)\n'
                                  '_ram(state, 61400).set_word(0, 2)\n'
                                  '_ram(state, 45054).set_word(0, 1)\n'
                                  '_ram(state, 62976).set_word(0, 4)\n'
                                  'from .business_main import dispatch_main_scene_slot\n'
                                  'while True:\n'
                                  '    while _ram(state, 62976).word() == 0:\n'
                                  "        state.progress('main scene request wait')\n"
                                  '    selector = _ram(state, 62976).word() & 65532\n'
                                  '    dispatch_main_scene_slot(state, selector)\n'
                                  '    _ram(state, 62976).set_word(0, 0)\n'
                                  '    state.set_status_word(9472)'}}

def _lower_reset_console(emitter,rules):
    emitter.segment(0x206,0x294)
    emitter.ins('tst.l','0xa10008:l',6)
    emitter.ins('bne.b','main_pc_000214',2)
    emitter.ins('tst.w','0xa1000c:l',6)
    emitter.ins('bne.b','main_pc_000292',2)
    emitter.ins('lea.l','124(%pc),%a5',4)
    emitter.ins('movem.w','(%a5)+,%d5-%d7',4)
    emitter.ins('movem.l','(%a5)+,%a0-%a4',4)
    emitter.ins('move.b','-0x10ff(%a1),%d0',4)
    emitter.ins('andi.b','#0xf,%d0',4)
    emitter.ins('beq.b','main_pc_000234',2)
    emitter.ins('move.l','#0x53454741,0x2f00(%a1)',8)
    emitter.ins('move.w','(%a4),%d0',2)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('movea.l','%d0,%a6',2)
    emitter.ins('move','%a6,%usp',2)
    emitter.ins('moveq','#23,%d1',2)
    emitter.ins('move.b','(%a5)+,%d5',2)
    emitter.ins('move.w','%d5,(%a4)',2)
    emitter.ins('add.w','%d7,%d5',2)
    emitter.ins('dbra','%d1,main_pc_00023e',4)
    emitter.ins('move.l','(%a5)+,(%a4)',2)
    emitter.ins('move.w','%d0,(%a3)',2)
    emitter.ins('move.w','%d7,(%a1)',2)
    emitter.ins('move.w','%d7,(%a2)',2)
    emitter.ins('btst.l','%d0,(%a1)',2)
    emitter.ins('bne.b','main_pc_000250',2)
    emitter.ins('moveq','#37,%d2',2)
    emitter.ins('move.b','(%a5)+,(%a0)+',2)
    emitter.ins('dbra','%d2,main_pc_000256',4)
    emitter.ins('move.w','%d0,(%a2)',2)
    emitter.ins('move.w','%d0,(%a1)',2)
    emitter.ins('move.w','%d7,(%a2)',2)
    emitter.ins('move.l','%d0,-(%a6)',2)
    emitter.ins('dbra','%d6,main_pc_000262',4)
    emitter.ins('move.l','(%a5)+,(%a4)',2)
    emitter.ins('move.l','(%a5)+,(%a4)',2)
    emitter.ins('moveq','#31,%d3',2)
    emitter.ins('move.l','%d0,(%a3)',2)
    emitter.ins('dbra','%d3,main_pc_00026e',4)
    emitter.ins('move.l','(%a5)+,(%a4)',2)
    emitter.ins('moveq','#19,%d4',2)
    emitter.ins('move.l','%d0,(%a3)',2)
    emitter.ins('dbra','%d4,main_pc_000278',4)
    emitter.ins('moveq','#3,%d5',2)
    emitter.ins('move.b','(%a5)+,0x11(%a3)',4)
    emitter.ins('dbra','%d5,main_pc_000280',4)
    emitter.ins('move.w','%d0,(%a2)',2)
    emitter.ins('movem.l','(%a6),%d0-%d7/%a0-%a6',4)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('bra.b','main_pc_000300',2)
    emitter.segment(0x300,0x3d8)
    emitter.ins('tst.w','0xc00004:l',6)
    emitter.ins('lea.l','0xc00004:l,%a6',6)
    emitter.ins('move.w','(%a6),%d0',2)
    emitter.ins('andi.w','#0x2,%d0',4)
    emitter.ins('bne.b','main_pc_00030c',2)
    emitter.ins('btst.b','#0x6,0xa1000d:l',8)
    emitter.ins('beq.b','main_pc_00032a',2)
    emitter.ins('cmpi.l','#0x696e6974,0xfffc:w',8)
    emitter.ins('beq.w','main_pc_00036e',4)
    emitter.ins('lea.l','0x1a4:w,%a0',4)
    emitter.ins('move.l','(%a0),%d0',2)
    emitter.ins('addq.l','#0x1,%d0',2)
    emitter.ins('lea.l','0x200:w,%a0',4)
    emitter.ins('sub.l','%a0,%d0',2)
    emitter.ins('asr.l','#0x1,%d0',2)
    emitter.ins('move.w','%d0,%d2',2)
    emitter.ins('subq.w','#0x1,%d2',2)
    emitter.ins('swap','%d0',2)
    emitter.ins('moveq','#0,%d1',2)
    emitter.ins('add.w','(%a0)+,%d1',2)
    emitter.ins('dbra','%d2,main_pc_000342',4)
    emitter.ins('dbra','%d0,main_pc_000342',4)
    emitter.ins('lea.l','0x18e:w,%a0',4)
    emitter.ins('cmp.w','(%a0),%d1',2)
    emitter.ins('bne.w','main_pc_0004c8',4)
    emitter.ins('lea.l','0xfe00:w,%a6',4)
    emitter.ins('moveq','#0,%d7',2)
    emitter.ins('move.w','#0x7f,%d6',4)
    emitter.ins('move.l','%d7,(%a6)+',2)
    emitter.ins('dbra','%d6,main_pc_000360',4)
    emitter.ins('move.l','#0x696e6974,0xfffc:w',8)
    emitter.ins('lea.l','0xff0000:l,%a6',6)
    emitter.ins('moveq','#0,%d7',2)
    emitter.ins('move.w','#0x3f7f,%d6',4)
    emitter.ins('move.l','%d7,(%a6)+',2)
    emitter.ins('dbra','%d6,main_pc_00037a',4)
    emitter.ins('lea.l','0xfffe00:l,%a7',6)
    emitter.ins('jsr','main_pc_006826:l',6)
    emitter.ins('jsr','main_pc_006950:l',6)
    emitter.ins('jsr','main_pc_0067b4:l',6)
    emitter.ins('move.w','#0x50,0xf30a:w',6)
    emitter.ins('move.w','#0xa0,0xf30c:w',6)
    emitter.ins('move.w','#0x1800,0xf30e:w',6)
    emitter.ins('move.w','#0x2,0xefd8:w',6)
    emitter.ins('move.w','#0x1,0xaffe:w',6)
    emitter.ins('move.w','#0x4,0xf600:w',6)
    emitter.ins('tst.w','0xf600:w',4)
    emitter.ins('beq.b','main_pc_0003bc',2)
    emitter.ins('move.w','0xf600:w,%d0',4)
    emitter.ins('andi.w','#0xfffc,%d0',4)
    emitter.ins('jsr','8(%pc, %d0.w)',4)
    emitter.ins('clr.w','0xf600:w',4)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('bra.b','main_pc_0003bc',2)
    emitter.segment(0x4c8,0x4e8)
    emitter.ins('jsr','main_pc_006826:l',6)
    emitter.ins('move.l','#0xc0000000,0xc00004:l',10)
    emitter.ins('moveq','#63,%d7',2)
    emitter.ins('move.w','#0xe,0xc00000:l',8)
    emitter.ins('dbra','%d7,main_pc_0004da',4)
    emitter.ins('bra.b','main_pc_0004e6',2)

LOWERERS={
    'reset_console':_lower_reset_console,
}

def compile_source(source):
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    for owner, field in (('reset_console', 'reset_console_frame_fields'), ('start_game_main_loop', 'start_game_main_loop_frame_fields')):
        records[owner]['effects'] = dict(historical_projection=records[owner]['effects'], sole_complete_fields=records[field]['effects'], parameter_edit_status='NOT_AVAILABLE')
    return lower_declared(records, BUSINESS_BOOT_BINDINGS, LOWERERS)


# C59 exact complete fields, compatibility projections and current closed dispatch.
DECLARATIONS.update({'_bootstrap_checksum_extent_frame_fields': {'flow': 'from ..high_level_remaining_flows.business_city '
                                                     'import _recruitment_right_long\n'
                                                     'original = frame.target_x\n'
                                                     'frame = _recruitment_right_long(state, frame, '
                                                     "'target_x', 1)\n"
                                                     'value = frame.target_x | original & 2147483648\n'
                                                     'status = frame.status & 17 | (8 if value & '
                                                     '2147483648 else 0) | (4 if value == 0 else 0)\n'
                                                     'state.sr = state.sr & 65504 | status\n'
                                                     'return first_replace(frame, target_x=value, '
                                                     'status=status)',
                                             'returns': 'FirstDeploymentFrame',
                                             'signature': 'state: SceneState, frame: '
                                                          'FirstDeploymentFrame'},
 '_bootstrap_checksum_failed_frame_fields': {'flow': 'frame = display_call_fields(state, frame, 26662, '
                                                     '1230)\n'
                                                     'frame = display_store_fields(state, frame, 1230, '
                                                     '12582916, 3221225472, 4)\n'
                                                     'frame = display_move_fields(state, frame, '
                                                     "'choice', 63, 32)\n"
                                                     'while True:\n'
                                                     '    frame = display_store_fields(state, frame, '
                                                     '1242, 12582912, 14)\n'
                                                     '    frame, more = display_loop_fields(frame, '
                                                     "'choice')\n"
                                                     '    if not more:\n'
                                                     '        break\n'
                                                     'while True:\n'
                                                     "    state.progress('original4E6 fatal cartridge "
                                                     "checksum loop')",
                                             'returns': 'FirstDeploymentFrame',
                                             'signature': 'state: SceneState, frame: '
                                                          'FirstDeploymentFrame'},
 '_checksum_failed': {'flow': 'from .contexts_display_fields import display_legacy_frame_fields\n'
                              'return display_legacy_frame_fields(state, None, 1224)',
                      'returns': '',
                      'signature': 'state'},
 'reset_console': {'flow': 'from .contexts_display_fields import display_legacy_frame_fields\n'
                           'entered = display_legacy_frame_fields(state, profile, 518)\n'
                           'return reset_console_frame_fields(state, entered)',
                   'returns': '',
                   'signature': 'state: SceneState, profile: ResetProfile'},
 'reset_console_frame_fields': {'flow': 'from .business_movement_support import _movement_test_long, '
                                        '_movement_test, _movement_add_word\n'
                                        'from .business_map import _world_map_bit_fields\n'
                                        'frame = display_frame_fields(state, frame)\n'
                                        'frame = _movement_test_long(state, frame, state.read(10551304, '
                                        '4))\n'
                                        'if frame.status & 4:\n'
                                        '    frame = _movement_test(state, frame, state.read(10551308, '
                                        '2), 16)\n'
                                        'if not frame.status & 4:\n'
                                        '    return start_game_main_loop_frame_fields(state, frame)\n'
                                        "frame = display_address_fields(state, frame, 'scratch', 660)\n"
                                        "for name in ('offset_x', 'offset_y', 'choice'):\n"
                                        '    value = u32(s16(frame.scratch.word()))\n'
                                        '    frame = first_replace(frame, **{name: value}, '
                                        'scratch=frame.scratch.advance(2))\n'
                                        "for name in ('roster', 'candidates', 'controller', 'scan', "
                                        "'opponent'):\n"
                                        '    value = frame.scratch.long()\n'
                                        '    frame = first_replace(frame, '
                                        'scratch=frame.scratch.advance(4))\n'
                                        '    frame = display_address_fields(state, frame, name, value)\n'
                                        "frame = display_move_fields(state, frame, 'target_x', "
                                        'state.read(u32(frame.candidates.base - 4351), 1), 8)\n'
                                        "frame = display_move_fields(state, frame, 'target_x', "
                                        'low8(frame.target_x) & 15, 8)\n'
                                        'if not frame.status & 4:\n'
                                        '    frame = display_store_fields(state, frame, 556, '
                                        'u32(frame.candidates.base + 12032), 1397049153, 4)\n'
                                        "frame = display_move_fields(state, frame, 'target_x', "
                                        'frame.opponent.word())\n'
                                        "frame = display_move_fields(state, frame, 'target_x', 0, 32)\n"
                                        "frame = display_address_fields(state, frame, 'auxiliary', "
                                        'frame.target_x)\n'
                                        'if type(profile) is not ResetProfile:\n'
                                        "    raise MovementContinuationBoundary(570, frame, 'original "
                                        "MOVE A6,USP requires the existing explicit BootstrapControl')\n"
                                        'profile.validate(state)\n'
                                        'profile.processor.set_user_stack(state, frame.auxiliary.base)\n'
                                        "frame = display_move_fields(state, frame, 'target_y', 23, 32)\n"
                                        'while True:\n'
                                        '    value = frame.scratch.byte()\n'
                                        '    frame = first_replace(frame, '
                                        'scratch=frame.scratch.advance(1))\n'
                                        "    frame = display_move_fields(state, frame, 'offset_x', "
                                        'value, 8)\n'
                                        '    frame = display_store_fields(state, frame, 576, '
                                        'frame.opponent.base, low16(frame.offset_x))\n'
                                        "    frame = _movement_add_word(state, frame, 'offset_x', "
                                        'low16(frame.choice))\n'
                                        "    frame, more = display_loop_fields(frame, 'target_y')\n"
                                        '    if not more:\n'
                                        '        break\n'
                                        'value = frame.scratch.long()\n'
                                        'frame = first_replace(frame, '
                                        'scratch=frame.scratch.advance(4))\n'
                                        'frame = display_store_fields(state, frame, 584, '
                                        'frame.opponent.base, value, 4)\n'
                                        'frame = display_store_fields(state, frame, 586, '
                                        'frame.scan.base, low16(frame.target_x))\n'
                                        'frame = display_store_fields(state, frame, 588, '
                                        'frame.candidates.base, low16(frame.choice))\n'
                                        'frame = display_store_fields(state, frame, 590, '
                                        'frame.controller.base, low16(frame.choice))\n'
                                        'while True:\n'
                                        '    frame = _world_map_bit_fields(state, frame, '
                                        'frame.candidates.byte(), frame.target_x & 7)\n'
                                        '    if frame.status & 4:\n'
                                        '        break\n'
                                        "    state.progress('original250 sound bus request bit0')\n"
                                        "frame = display_move_fields(state, frame, 'unit', 37, 32)\n"
                                        'while True:\n'
                                        '    value = frame.scratch.byte()\n'
                                        '    frame = first_replace(frame, '
                                        'scratch=frame.scratch.advance(1))\n'
                                        '    frame = display_store_fields(state, frame, 598, '
                                        'frame.roster.base, value, 1)\n'
                                        '    frame = first_replace(frame, '
                                        'roster=frame.roster.advance(1))\n'
                                        "    frame, more = display_loop_fields(frame, 'unit')\n"
                                        '    if not more:\n'
                                        '        break\n'
                                        'frame = display_store_fields(state, frame, 604, '
                                        'frame.controller.base, low16(frame.target_x))\n'
                                        'frame = display_store_fields(state, frame, 606, '
                                        'frame.candidates.base, low16(frame.target_x))\n'
                                        'frame = display_store_fields(state, frame, 608, '
                                        'frame.controller.base, low16(frame.choice))\n'
                                        'while True:\n'
                                        '    frame = first_replace(frame, '
                                        'auxiliary=frame.auxiliary.advance(-4))\n'
                                        '    frame = display_store_fields(state, frame, 610, '
                                        'frame.auxiliary.base, frame.target_x, 4)\n'
                                        "    frame, more = display_loop_fields(frame, 'offset_y')\n"
                                        '    if not more:\n'
                                        '        break\n'
                                        'for pc in (616, 618):\n'
                                        '    value = frame.scratch.long()\n'
                                        '    frame = first_replace(frame, '
                                        'scratch=frame.scratch.advance(4))\n'
                                        '    frame = display_store_fields(state, frame, pc, '
                                        'frame.opponent.base, value, 4)\n'
                                        "frame = display_move_fields(state, frame, 'count', 31, 32)\n"
                                        'while True:\n'
                                        '    frame = display_store_fields(state, frame, 622, '
                                        'frame.scan.base, frame.target_x, 4)\n'
                                        "    frame, more = display_loop_fields(frame, 'count')\n"
                                        '    if not more:\n'
                                        '        break\n'
                                        'value = frame.scratch.long()\n'
                                        'frame = first_replace(frame, '
                                        'scratch=frame.scratch.advance(4))\n'
                                        'frame = display_store_fields(state, frame, 628, '
                                        'frame.opponent.base, value, 4)\n'
                                        "frame = display_move_fields(state, frame, 'distance', 19, 32)\n"
                                        'while True:\n'
                                        '    frame = display_store_fields(state, frame, 632, '
                                        'frame.scan.base, frame.target_x, 4)\n'
                                        "    frame, more = display_loop_fields(frame, 'distance')\n"
                                        '    if not more:\n'
                                        '        break\n'
                                        "frame = display_move_fields(state, frame, 'offset_x', 3, 32)\n"
                                        'while True:\n'
                                        '    value = frame.scratch.byte()\n'
                                        '    frame = first_replace(frame, '
                                        'scratch=frame.scratch.advance(1))\n'
                                        '    frame = display_store_fields(state, frame, 640, '
                                        'u32(frame.scan.base + 17), value, 1)\n'
                                        "    frame, more = display_loop_fields(frame, 'offset_x')\n"
                                        '    if not more:\n'
                                        '        break\n'
                                        'frame = display_store_fields(state, frame, 648, '
                                        'frame.controller.base, low16(frame.target_x))\n'
                                        'source = frame.auxiliary\n'
                                        "for name in ('target_x', 'target_y', 'unit', 'count', "
                                        "'distance', 'offset_x', 'offset_y', 'choice', 'roster', "
                                        "'candidates', 'controller', 'scan', 'opponent', 'scratch', "
                                        "'auxiliary'):\n"
                                        '    value = source.long()\n'
                                        '    source = source.advance(4)\n'
                                        "    if name in ('roster', 'candidates', 'controller', 'scan', "
                                        "'opponent', 'scratch', 'auxiliary'):\n"
                                        '        frame = display_address_fields(state, frame, name, '
                                        'value)\n'
                                        '    else:\n'
                                        '        frame = first_replace(frame, **{name: value})\n'
                                        'frame = display_status_fields(state, frame, 9984)\n'
                                        'return start_game_main_loop_frame_fields(state, frame)',
                                'returns': 'FirstDeploymentFrame',
                                'signature': 'state: SceneState, frame: FirstDeploymentFrame, profile: '
                                             'ResetProfile | None=None'},
 'start_game_main_loop': {'flow': 'from .contexts_display_fields import display_legacy_frame_fields\n'
                                  'entered = display_legacy_frame_fields(state, profile, 768)\n'
                                  'return start_game_main_loop_frame_fields(state, entered)',
                          'returns': '',
                          'signature': 'state: SceneState, profile: ResetProfile'},
 'start_game_main_loop_frame_fields': {'flow': 'from .business_movement_support import _movement_test, '
                                               '_movement_compare, _movement_binary_flags, '
                                               '_movement_add_word\n'
                                               'from ..high_level_scene_flows.business_scene import '
                                               '_scene_render_compare\n'
                                               'from ..high_level_gameplay_flow.contexts_services '
                                               'import SceneRefreshMemory\n'
                                               'from ..high_level_remaining_flows.business_city import '
                                               '_special_action_swap\n'
                                               'from .business_map import _world_map_bit_fields\n'
                                               'frame = display_frame_fields(state, frame)\n'
                                               'frame = _movement_test(state, frame, '
                                               'state.read(12582916, 2), 16)\n'
                                               'frame = display_address_fields(state, frame, '
                                               "'auxiliary', 12582916)\n"
                                               'while True:\n'
                                               '    frame = display_move_fields(state, frame, '
                                               "'target_x', frame.auxiliary.word())\n"
                                               '    frame = display_move_fields(state, frame, '
                                               "'target_x', low16(frame.target_x) & 2)\n"
                                               '    if frame.status & 4:\n'
                                               '        break\n'
                                               "    state.progress('original30C bootstrap VDP DMA "
                                               "wait')\n"
                                               'frame = _world_map_bit_fields(state, frame, '
                                               'state.read(10551309, 1), 6)\n'
                                               'retained = not frame.status & 4\n'
                                               'if retained:\n'
                                               '    frame = '
                                               '_scene_render_compare(SceneRefreshMemory(state), frame, '
                                               'state.read(4294967292, 4), 1768843636, 32)\n'
                                               '    retained = bool(frame.status & 4)\n'
                                               'if not retained:\n'
                                               '    frame = display_address_fields(state, frame, '
                                               "'roster', 420)\n"
                                               '    frame = display_move_fields(state, frame, '
                                               "'target_x', frame.roster.long(), 32)\n"
                                               '    frame, value = _movement_binary_flags(state, frame, '
                                               'frame.target_x, 1, 32)\n'
                                               '    frame = first_replace(frame, target_x=value)\n'
                                               '    frame = display_address_fields(state, frame, '
                                               "'roster', 512)\n"
                                               '    frame, value = _movement_binary_flags(state, frame, '
                                               'frame.target_x, frame.roster.base, 32, True)\n'
                                               '    frame = first_replace(frame, target_x=value)\n'
                                               '    frame = '
                                               '_bootstrap_checksum_extent_frame_fields(state, frame)\n'
                                               "    frame = display_move_fields(state, frame, 'unit', "
                                               'low16(frame.target_x))\n'
                                               '    frame, value = _movement_binary_flags(state, frame, '
                                               'low16(frame.unit), 1, 16, True)\n'
                                               '    frame = first_replace(frame, '
                                               'unit=replace_word(frame.unit, value))\n'
                                               '    frame = _special_action_swap(state, frame, '
                                               "'target_x')\n"
                                               '    frame = display_move_fields(state, frame, '
                                               "'target_y', 0, 32)\n"
                                               '    while True:\n'
                                               '        while True:\n'
                                               '            value = frame.roster.word()\n'
                                               '            frame = first_replace(frame, '
                                               'roster=frame.roster.advance(2))\n'
                                               '            frame = _movement_add_word(state, frame, '
                                               "'target_y', value)\n"
                                               '            frame, more = display_loop_fields(frame, '
                                               "'unit')\n"
                                               '            if not more:\n'
                                               '                break\n'
                                               '        frame, more = display_loop_fields(frame, '
                                               "'target_x')\n"
                                               '        if not more:\n'
                                               '            break\n'
                                               '    frame = display_address_fields(state, frame, '
                                               "'roster', 398)\n"
                                               '    frame = _movement_compare(state, frame, '
                                               'low16(frame.target_y), frame.roster.word(), 16)\n'
                                               '    if not frame.status & 4:\n'
                                               '        return '
                                               '_bootstrap_checksum_failed_frame_fields(state, frame)\n'
                                               '    frame = display_address_fields(state, frame, '
                                               "'auxiliary', 4294966784)\n"
                                               "    frame = display_move_fields(state, frame, 'choice', "
                                               '0, 32)\n'
                                               '    frame = display_move_fields(state, frame, '
                                               "'offset_y', 127)\n"
                                               '    while True:\n'
                                               '        frame = display_store_fields(state, frame, 864, '
                                               'frame.auxiliary.base, frame.choice, 4)\n'
                                               '        frame = first_replace(frame, '
                                               'auxiliary=frame.auxiliary.advance(4))\n'
                                               '        frame, more = display_loop_fields(frame, '
                                               "'offset_y')\n"
                                               '        if not more:\n'
                                               '            break\n'
                                               '    frame = display_store_fields(state, frame, 870, '
                                               '4294967292, 1768843636, 4)\n'
                                               'frame = display_address_fields(state, frame, '
                                               "'auxiliary', 16711680)\n"
                                               "frame = display_move_fields(state, frame, 'choice', 0, "
                                               '32)\n'
                                               "frame = display_move_fields(state, frame, 'offset_y', "
                                               '16255)\n'
                                               'while True:\n'
                                               '    frame = display_store_fields(state, frame, 890, '
                                               'frame.auxiliary.base, frame.choice, 4)\n'
                                               '    frame = first_replace(frame, '
                                               'auxiliary=frame.auxiliary.advance(4))\n'
                                               '    frame, more = display_loop_fields(frame, '
                                               "'offset_y')\n"
                                               '    if not more:\n'
                                               '        break\n'
                                               'frame = display_address_fields(state, frame, '
                                               "'stack_cursor', 16776704)\n"
                                               'frame = display_call_fields(state, frame, 26662, 908)\n'
                                               'frame = display_call_fields(state, frame, 26960, 914)\n'
                                               'frame = display_call_fields(state, frame, 26548, 920)\n'
                                               'for pc, address, value in ((920, 4294963978, 80), (926, '
                                               '4294963980, 160), (932, 4294963982, 6144), (938, '
                                               '4294963160, 2), (944, 4294946814, 1), (950, 4294964736, '
                                               '4)):\n'
                                               '    frame = display_store_fields(state, frame, pc, '
                                               'address, value)\n'
                                               'while True:\n'
                                               '    while True:\n'
                                               '        frame = _movement_test(state, frame, '
                                               'state.read(4294964736, 2), 16)\n'
                                               '        if not frame.status & 4:\n'
                                               '            break\n'
                                               "        state.progress('original3BC main scene request "
                                               "wait')\n"
                                               '    frame = display_move_fields(state, frame, '
                                               "'target_x', state.read(4294964736, 2))\n"
                                               '    frame = display_move_fields(state, frame, '
                                               "'target_x', low16(frame.target_x) & 65532)\n"
                                               '    frame = display_call_fields(state, frame, u32(980 + '
                                               's16(low16(frame.target_x))), 974)\n'
                                               '    frame = display_store_fields(state, frame, 974, '
                                               '4294964736, 0, clear=True)\n'
                                               '    frame = display_status_fields(state, frame, 9472)',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame'}})
APPROVED.setdefault('business_map', set()).update(('_world_map_bit_fields',))
APPROVED.setdefault('business_movement_support', set()).update(('_movement_add_word', '_movement_binary_flags', '_movement_compare', '_movement_test', '_movement_test_long'))
APPROVED.setdefault('contexts_display_fields', set()).update(('display_address_fields', 'display_call_fields', 'display_frame_fields', 'display_legacy_frame_fields', 'display_loop_fields', 'display_move_fields', 'display_status_fields', 'display_store_fields'))
APPROVED.setdefault('contexts_gameplay', set()).update(('FirstDeploymentFrame', 'MovementContinuationBoundary', 'first_replace'))
APPROVED.setdefault('domain', set()).update(('low8',))
APPROVED.setdefault((2, 'high_level_gameplay_flow.contexts_services'), set()).update(('SceneRefreshMemory',))
APPROVED.setdefault((2, 'high_level_remaining_flows.business_city'), set()).update(('_recruitment_right_long', '_special_action_swap'))
APPROVED.setdefault((2, 'high_level_scene_flows.business_scene'), set()).update(('_scene_render_compare',))


# B108 exact full bootstrap owner; ordinary original native lowerer is untouched.
_bootstrap_legacy_declaration183 = dict(DECLARATIONS['start_game_main_loop_frame_fields'])
APPROVED.setdefault('bootstrap_steps', set()).update(('run_bootstrap_main_blocking_fields',))
DECLARATIONS.update({'start_game_main_loop_frame_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'from .bootstrap_steps import run_bootstrap_main_blocking_fields\nreturn run_bootstrap_main_blocking_fields(state, frame)'}})
_compile_source_before_bootstrap183 = compile_source


def compile_source(source):
    from pathlib import Path
    from .compiler_bootstrap_steps import admit_bootstrap_main_program
    current = Path(__file__).with_name('bootstrap_steps.py').read_text(encoding='utf-8')
    admit_bootstrap_main_program(current, _bootstrap_legacy_declaration183)
    return _compile_source_before_bootstrap183(source)
