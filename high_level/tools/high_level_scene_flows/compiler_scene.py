"""Restricted semantic source admission with ordinary mnemonic lowering.

Reads explicit source text only. This is an intermediate structural compiler,
not a general Python compiler or full-console/indirect-handler implementation.
"""
from .compiler_common import CompileError, lower_declared
from .policy_common import admit_policy_source
from .scene_policy import ROLE_SPECS, owner_rules, LOWERERS as _SOURCE_LOWERERS
from .target import SCENE_BINDINGS

APPROVED = {
    'business_reuse': {'_restore_glyph_values', '_reuse_advance_random_pair', '_save_glyph_values', 'expand_glyph_row', 'step_random'},
    'contexts_objects': {'SceneControllerConditions', 'SceneControllerFrame', 'SceneRenderFrame', 'SpriteBatchResult', 'checked_controller_frame'},
    'contexts_reuse': {'GlyphSavedValues'},
    'contexts_scene': {'DictionaryStreamResult', 'GlyphRowsResult', 'PacketTransferValues', 'PaletteComponentResult', 'PaletteCopyCompleteResult', 'PaletteCopyFields', 'PaletteCopyResult', 'PaletteSnapshotResult', 'PaletteTransformResult', 'PlaneRowContext', 'PlaneRowResult', 'PlaneStreamResult', 'SceneFrameResult', 'ScenePlaybackResult', 'SwappedByteRleObservation', 'SwappedByteRleResult', 'SwappedByteRleRetained', 'VdpPacketResult', 'VdpStreamResult', 'checked_context'},
    'dataclasses': {'replace'},
    'domain': {'Boundary', 'Byte', 'Cursor', 'Long', 'SceneState', 'StackContinuation', 'Table', 'VideoPlaneAddress', 'Word', 'checked_cursor', 'checked_state', 'checked_table', 'descending_inclusive', 'high16', 'low16', 'low8', 'negative_word', 'replace_byte', 'replace_word', 's16', 'swap_words', 'u16', 'u32', 'u8', 'uint'},
    (2, 'high_level_battle_ai.business_formation'): {'first_deployment_random_fields'},
    (2, 'high_level_battle_ai.contexts_policy_memory'): {'BattlePolicyMemory'},
    (2, 'high_level_gameplay_flow.business_battle'): {'_presentation_call_fields'},
    (2, 'high_level_gameplay_flow.contexts_battle'): {'BattlePresentationMemory'},
    (2, 'high_level_main_flows.business_movement_support'): {'_movement_add_word', '_movement_binary_flags', '_movement_frame', '_movement_move', '_movement_test'},
    (2, 'high_level_remaining_flows.business_city'): {'_resource_cost_frame'},
}

DECLARATIONS={'_ram': {'signature': 'state, low',
          'returns': None,
          'flow': "return state.table('ram_' + low)"},
 '_word_shift': {'signature': 'carrier, amount',
                 'returns': None,
                 'flow': 'return replace_word(carrier, u16(low16(carrier) << amount))'},
 '_ror_word': {'signature': 'carrier, amount',
               'returns': None,
               'flow': 'value = low16(carrier)\n'
                       'return replace_word(carrier, u16(value >> amount | value << 16 - '
                       'amount))'},
 '_rol_word': {'signature': 'carrier, amount',
               'returns': None,
               'flow': 'value = low16(carrier)\n'
                       'return replace_word(carrier, u16(value << amount | value >> 16 - '
                       'amount))'},
 '_video_address': {'signature': 'value',
                    'returns': None,
                    'flow': 'if type(value) is not VideoPlaneAddress:\n'
                            "    raise ValueError('explicit video-plane address required')\n"
                            'value.__post_init__()\n'
                            'return value'},
 'flush_scene_transfer_queue': {'signature': 'state: SceneState, values: PacketTransferValues '
                                             '| None=None',
                                'returns': 'VdpPacketResult | None',
                                'flow': 'checked_state(state)\n'
                                        'if values is not None:\n'
                                        '    if type(values) is not PacketTransferValues:\n'
                                        "        raise ValueError('actual packet flush values "
                                        "required')\n"
                                        '    values.validate()\n'
                                        'result = None\n'
                                        "if _ram(state, 'd100').word() != 0:\n"
                                        '    result = write_vdp_packet_stream(state, '
                                        "_ram(state, 'd100').cursor(), values)\n"
                                        "_ram(state, 'f31a').set_word(0, 0)\n"
                                        "_ram(state, 'd100').set_word(0, 0)\n"
                                        'return result'},
 '_write_word_count': {'signature': 'state, source, count',
                       'returns': None,
                       'flow': 'while count >= 8:\n'
                               '    for _ in range(8):\n'
                               '        state.write(12582912, 2, source.next_word())\n'
                               '    count = u16(count - 8)\n'
                               'for _ in descending_inclusive(count):\n'
                               '    state.write(12582912, 2, source.next_word())'},
 'write_vdp_packet_stream': {'signature': 'state: SceneState, source: Cursor, values: '
                                          'PacketTransferValues | None=None',
                             'returns': 'VdpPacketResult',
                             'flow': 'checked_state(state)\n'
                                     'checked_cursor(source, state)\n'
                                     'if values is not None:\n'
                                     '    if type(values) is not PacketTransferValues:\n'
                                     "        raise ValueError('actual packet stream values "
                                     "required')\n"
                                     '    values.validate()\n'
                                     '    count_carrier, increment_carrier = (values.command, '
                                     'values.increment)\n'
                                     '    spill_carrier = values.spill\n'
                                     'command = 0\n'
                                     'while True:\n'
                                     '    increment = 36610\n'
                                     '    count = source.next_word()\n'
                                     '    if count == 0:\n'
                                     '        state.write(12582916, 2, increment)\n'
                                     '        actual = None\n'
                                     '        if values is not None:\n'
                                     '            actual = '
                                     'PacketTransferValues(replace_word(count_carrier, 0), '
                                     'replace_word(increment_carrier, increment), '
                                     'values.address, spill_carrier).validate()\n'
                                     '        return VdpPacketResult(source, command, '
                                     'increment, actual)\n'
                                     '    if negative_word(count):\n'
                                     '        increment = 36736\n'
                                     '        count &= 32767\n'
                                     '        address = source.next_word()\n'
                                     '        total = u16(((address & 8191) >> 7) + count)\n'
                                     '        spill = u16(total - 64) if total >= 64 else 0\n'
                                     '        count = u16(count - spill)\n'
                                     '    else:\n'
                                     '        address = source.next_word()\n'
                                     '        spill = 0\n'
                                     '        if not count & 16384:\n'
                                     '            total = u16(((address & 127) >> 1) + '
                                     'count)\n'
                                     '            spill = u16(total - 64) if total >= 64 else '
                                     '0\n'
                                     '            count = u16(count - spill)\n'
                                     '    count = u16((count & 49151) - 1)\n'
                                     '    state.write(12582916, 2, increment)\n'
                                     '    command = u32(address << 2)\n'
                                     '    command = replace_word(command, low16(command) >> 2 '
                                     '| 16384)\n'
                                     '    command = swap_words(command)\n'
                                     '    state.write(12582916, 4, command)\n'
                                     '    if values is not None:\n'
                                     '        spill_carrier = replace_word(spill_carrier, '
                                     'spill)\n'
                                     '    _write_word_count(state, source, count)\n'
                                     '    if spill != 0:\n'
                                     '        command &= 4286644223 if increment & 2 else '
                                     '3766484991\n'
                                     '        spill = u16(spill - 1)\n'
                                     '        state.write(12582916, 4, command)\n'
                                     '        _write_word_count(state, source, spill)\n'
                                     '        if values is not None:\n'
                                     '            spill_carrier = replace_word(spill_carrier, '
                                     '65535)\n'
                                     '    if values is not None:\n'
                                     '        values = PacketTransferValues(count_carrier, '
                                     'increment_carrier, command, spill_carrier)'},
 'write_vdp_dictionary_repeat_stream': {'signature': 'state: SceneState, source: Cursor, '
                                                     'dictionary: Table, remaining: Word',
                                        'returns': 'DictionaryStreamResult',
                                        'flow': 'checked_state(state)\n'
                                                'checked_cursor(source, state)\n'
                                                'checked_table(dictionary, state)\n'
                                                'uint(remaining, 16)\n'
                                                'alternate, alternate_remaining = (None, 0)\n'
                                                'while True:\n'
                                                '    if alternate_remaining != 0:\n'
                                                '        token = alternate.next_word()\n'
                                                '        alternate_remaining = '
                                                'u8(alternate_remaining - 1)\n'
                                                '    else:\n'
                                                '        token = source.next_word()\n'
                                                '        remaining = u16(remaining - 1)\n'
                                                '    if token < 65024:\n'
                                                '        state.write(12582912, 2, token)\n'
                                                '    elif token < 65280:\n'
                                                '        alternate = '
                                                'dictionary.cursor(u16((token & 255) << 2))\n'
                                                '        if alternate.word() >= 65280:\n'
                                                '            alternate_remaining = 2\n'
                                                '        elif alternate.word() < 65024:\n'
                                                '            alternate_remaining = 2\n'
                                                '        else:\n'
                                                '            state.write(12582912, 2, '
                                                'alternate.word())\n'
                                                '        continue\n'
                                                '    else:\n'
                                                '        repeats = token & 255\n'
                                                '        if alternate_remaining != 0:\n'
                                                '            value = alternate.next_word()\n'
                                                '            alternate_remaining = '
                                                'u8(alternate_remaining - 1)\n'
                                                '        else:\n'
                                                '            value = source.next_word()\n'
                                                '            remaining = u16(remaining - 1)\n'
                                                '        if 65024 <= value < 65280:\n'
                                                '            alternate = '
                                                'dictionary.cursor(u16((value & 255) << 2))\n'
                                                '            value = alternate.next_word()\n'
                                                '            alternate_remaining = 1\n'
                                                '        for _ in '
                                                'descending_inclusive(repeats):\n'
                                                '            state.write(12582912, 2, value)\n'
                                                '    if alternate_remaining == 0 and '
                                                'negative_word(remaining):\n'
                                                '        return '
                                                'DictionaryStreamResult(source, alternate, '
                                                'remaining)'},
 'decode_glyph_rows_to_buffers': {'signature': 'state: SceneState, source: Cursor, '
                                               'destination: Cursor, background: Long, '
                                               'foreground: Long, remaining: Long, saved: '
                                               'GlyphSavedValues | None=None',
                                  'returns': 'GlyphRowsResult',
                                  'flow': 'from .business_reuse import expand_glyph_row, '
                                          '_save_glyph_values, _restore_glyph_values\n'
                                          'checked_state(state)\n'
                                          'checked_cursor(source, state)\n'
                                          'checked_cursor(destination, state)\n'
                                          'uint(background, 32)\n'
                                          'uint(foreground, 32)\n'
                                          'uint(remaining, 32)\n'
                                          'if saved is not None:\n'
                                          '    _save_glyph_values(state, saved, True)\n'
                                          'for _ in descending_inclusive(low16(remaining)):\n'
                                          '    token = source.next_word()\n'
                                          '    if not negative_word(token):\n'
                                          '        offset = u16((token & 65280) << 3) | '
                                          'u16((token & 255) << 5)\n'
                                          '        glyph = '
                                          'state.table(529820).advance(offset).cursor()\n'
                                          '        for _ in range(16):\n'
                                          '            destination.set_long(0, '
                                          'expand_glyph_row(state, glyph, low8(background), '
                                          'low8(foreground)))\n'
                                          '            destination.set_long(0, '
                                          'expand_glyph_row(state, glyph, low8(background), '
                                          'low8(foreground)), 64)\n'
                                          '            destination.base = '
                                          'u32(destination.base + 4)\n'
                                          '    else:\n'
                                          '        background_pixels, foreground_pixels = (0, '
                                          '0)\n'
                                          '        for _ in range(8):\n'
                                          '            background_pixels = '
                                          'u32(background_pixels << 4) | low16(background)\n'
                                          '            foreground_pixels = '
                                          'u32(foreground_pixels << 4) | low16(foreground)\n'
                                          '        for _ in range(16):\n'
                                          '            destination.set_long(0, '
                                          'background_pixels, 64)\n'
                                          '            '
                                          'destination.append_long(background_pixels)\n'
                                          '        destination.set_long(0, foreground_pixels, '
                                          '-36)\n'
                                          '        destination.set_long(0, foreground_pixels, '
                                          '28)\n'
                                          '    destination.base = u32(destination.base + 64)\n'
                                          'if saved is not None:\n'
                                          '    saved = _restore_glyph_values(state, saved, '
                                          'saved.glyph_source, True)\n'
                                          'return GlyphRowsResult(source, destination, '
                                          'replace_word(remaining, 65535), background, '
                                          'foreground, saved)'},
 'darken_palette_component': {'signature': 'state: SceneState, shade: Long, color: Long, '
                                           'accumulated: Long, component: Long=0',
                              'returns': 'PaletteComponentResult',
                              'flow': 'checked_state(state)\n'
                                      'for value in (shade, color, accumulated, component):\n'
                                      '    uint(value, 32)\n'
                                      'accumulated = _word_shift(accumulated, 4)\n'
                                      'color = _rol_word(color, 4)\n'
                                      'component = replace_byte(component, low8(color))\n'
                                      'component = replace_word(component, low16(component) & '
                                      '14)\n'
                                      'borrowed = low8(component) < low8(shade)\n'
                                      'component = replace_byte(component, u8(low8(component) '
                                      '- low8(shade)))\n'
                                      'if borrowed:\n'
                                      '    component = replace_byte(component, 0)\n'
                                      'accumulated = replace_word(accumulated, '
                                      'low16(accumulated) | low16(component))\n'
                                      'return PaletteComponentResult(color, accumulated, '
                                      'component)'},
 'darken_palette': {'signature': 'state: SceneState, shade: Long, count: Word, source: '
                                 'Cursor, accumulator: Long=0, *, count_carrier: Long | '
                                 'None=None, color: Long=0, component: Long=0',
                    'returns': 'PaletteTransformResult',
                    'flow': 'checked_state(state)\n'
                            'checked_cursor(source, state)\n'
                            'uint(shade, 32)\n'
                            'uint(count, 16)\n'
                            'uint(accumulator, 32)\n'
                            'uint(color, 32)\n'
                            'uint(component, 32)\n'
                            'if count_carrier is not None:\n'
                            '    uint(count_carrier, 32)\n'
                            '    if low16(count_carrier) != count:\n'
                            "        raise ValueError('palette count must agree with actual "
                            "caller')\n"
                            'if low16(shade) > 15:\n'
                            "    raise Boundary('original DEAC nonprogressing branch for "
                            "shade WORD >15')\n"
                            "destination = _ram(state, 'fb00').cursor()\n"
                            'if shade & 1:\n'
                            "    if _ram(state, 'f320').byte() & 1:\n"
                            '        shade = replace_word(shade, u16(low16(shade) + 1))\n'
                            'shade &= 4294967294\n'
                            'accumulator = replace_word(accumulator, 0)\n'
                            'for _ in descending_inclusive(count):\n'
                            '    color = replace_word(color, u16(source.next_word() << 4))\n'
                            '    for _ in range(3):\n'
                            '        result = darken_palette_component(state, shade, color, '
                            'accumulator, component)\n'
                            '        color, accumulator, component = (result.color, '
                            'result.accumulated, result.component)\n'
                            '    destination.append_word(low16(accumulator))\n'
                            "_ram(state, 'f31e').set_word(0, u16(_ram(state, 'f31e').word() + "
                            '1))\n'
                            "shade = replace_word(shade, _ram(state, 'fb00').word())\n"
                            "_ram(state, 'fb20').set_word(0, low16(shade))\n"
                            "_ram(state, 'fb40').set_word(0, low16(shade))\n"
                            "_ram(state, 'fb60').set_word(0, low16(shade))\n"
                            'if count_carrier is not None:\n'
                            '    count_carrier = replace_word(count_carrier, 65535)\n'
                            'return PaletteTransformResult(source, destination, shade, '
                            'accumulator, count_carrier, color, component)'},
 'set_vram_write_address': {'signature': 'state: SceneState, address: VideoPlaneAddress',
                            'returns': 'Long',
                            'flow': 'checked_state(state)\n'
                                    'address = _video_address(address).word\n'
                                    'command = swap_words(address & 16383 | 16384) | address '
                                    '>> 14\n'
                                    'state.write(12582916, 4, command)\n'
                                    'return command'},
 '_set_vram_write_address_frame': {'signature': 'state: SceneState, current: '
                                                'SceneControllerFrame, address: '
                                                'VideoPlaneAddress, continuation: Long',
                                   'returns': 'SceneControllerFrame',
                                   'flow': 'current = checked_controller_frame(current, '
                                           'state)\n'
                                           '_video_address(address)\n'
                                           'uint(continuation, 32)\n'
                                           'stack = current.stack.advance(-4)\n'
                                           'stack.set_long(0, continuation)\n'
                                           'stack = stack.advance(-4)\n'
                                           'stack.set_long(0, current.y)\n'
                                           'command = set_vram_write_address(state, address)\n'
                                           'secondary = stack.long()\n'
                                           'stack = _scene_return_to_known_caller(state, '
                                           'stack.advance(4), continuation)\n'
                                           'return replace(current, x=command, y=secondary, '
                                           'stack=stack, '
                                           'conditions=SceneControllerConditions(False, '
                                           'command == 0, bool(command & 2147483648), '
                                           'False))'},
 '_scene_return_to_known_caller': {'signature': 'state: SceneState, stack: Cursor, '
                                                'continuation: Long',
                                   'returns': 'Cursor',
                                   'flow': 'checked_cursor(stack, state)\n'
                                           'uint(continuation, 32)\n'
                                           'target = stack.long()\n'
                                           'if target != continuation:\n'
                                           "    raise Boundary('live stack changed the known "
                                           "ordinary continuation')\n"
                                           'return stack.advance(4)'},
 'write_vdp_word_rle_stream': {'signature': 'state: SceneState, source: Cursor, '
                                            'video_address: VideoPlaneAddress',
                               'returns': 'VdpStreamResult',
                               'flow': 'checked_state(state)\n'
                                       'checked_cursor(source, state)\n'
                                       '_video_address(video_address)\n'
                                       'state.write(12582916, 2, 36610)\n'
                                       'command = set_vram_write_address(state, '
                                       'video_address)\n'
                                       'while True:\n'
                                       '    marker, high = (source.next_byte(), '
                                       'source.next_byte())\n'
                                       '    if marker != high:\n'
                                       '        value = high << 8 | source.next_byte()\n'
                                       '        state.write(12582912, 2, value)\n'
                                       '    else:\n'
                                       '        count = source.next_byte()\n'
                                       '        if count == 0:\n'
                                       '            return VdpStreamResult(source, '
                                       'video_address, command)\n'
                                       '        value = source.next_byte() << 8 | '
                                       'source.next_byte()\n'
                                       '        for _ in descending_inclusive(count):\n'
                                       '            state.write(12582912, 2, value)'},
 '_write_vdp_swapped_byte_rle_core': {'signature': 'state: SceneState, source: Cursor, '
                                                   'video_address: VideoPlaneAddress, '
                                                   'current: SceneControllerFrame | None=None',
                                      'returns': 'SwappedByteRleObservation',
                                      'flow': 'checked_state(state)\n'
                                              'checked_cursor(source, state)\n'
                                              '_video_address(video_address)\n'
                                              'if current is not None:\n'
                                              '    current = '
                                              'checked_controller_frame(current, state)\n'
                                              'state.write(12582916, 2, 36610)\n'
                                              'if current is None:\n'
                                              '    command = set_vram_write_address(state, '
                                              'video_address)\n'
                                              'else:\n'
                                              '    current = '
                                              '_set_vram_write_address_frame(state, current, '
                                              'video_address, 240478)\n'
                                              '    command = current.x\n'
                                              'marker = source.next_byte()\n'
                                              'last_word = None\n'
                                              'while True:\n'
                                              '    low = source.next_byte()\n'
                                              '    if marker != low:\n'
                                              '        last_word = source.next_byte() << 8 | '
                                              'low\n'
                                              '        state.write(12582912, 2, last_word)\n'
                                              '    else:\n'
                                              '        count = source.next_byte()\n'
                                              '        if count == 0:\n'
                                              '            if current is not None:\n'
                                              '                packed_word = current.tile\n'
                                              '                if last_word is not None:\n'
                                              '                    packed_word = '
                                              'replace_word(packed_word, last_word)\n'
                                              '                current = replace(current, '
                                              'source=source, y=replace_byte(current.y, '
                                              'marker), '
                                              'attributes=replace_byte(current.attributes, '
                                              'low), palette=0, tile=packed_word, '
                                              'conditions=SceneControllerConditions(False, '
                                              'True, False, False))\n'
                                              '            return '
                                              'SwappedByteRleObservation(source, '
                                              'video_address, command, marker, low, '
                                              'last_word, current)\n'
                                              '        low = source.next_byte()\n'
                                              '        last_word = source.next_byte() << 8 | '
                                              'low\n'
                                              '        for _ in descending_inclusive(count):\n'
                                              '            state.write(12582912, 2, '
                                              'last_word)'},
 'write_vdp_swapped_byte_rle_stream': {'signature': 'state: SceneState, source: Cursor, '
                                                    'video_address: VideoPlaneAddress',
                                       'returns': 'VdpStreamResult',
                                       'flow': 'actual = '
                                               '_write_vdp_swapped_byte_rle_core(state, '
                                               'source, video_address)\n'
                                               'return VdpStreamResult(actual.source, '
                                               'actual.video_address, '
                                               'actual.command_carrier)'},
 'write_vdp_swapped_byte_rle_stream_complete': {'signature': 'state: SceneState, source: '
                                                             'Cursor, video_address: '
                                                             'VideoPlaneAddress, retained: '
                                                             'SwappedByteRleRetained',
                                                'returns': 'SwappedByteRleResult',
                                                'flow': 'checked_state(state)\n'
                                                        'checked_cursor(source, state)\n'
                                                        '_video_address(video_address)\n'
                                                        'if type(retained) is not '
                                                        'SwappedByteRleRetained:\n'
                                                        "    raise ValueError('actual "
                                                        'D1/D2/D4 partial-write values '
                                                        "required')\n"
                                                        'retained.validate()\n'
                                                        'actual = '
                                                        '_write_vdp_swapped_byte_rle_core(state, '
                                                        'source, video_address)\n'
                                                        'packed_word = retained.packed_word\n'
                                                        'if actual.last_word is not None:\n'
                                                        '    packed_word = '
                                                        'replace_word(packed_word, '
                                                        'actual.last_word)\n'
                                                        'return '
                                                        'SwappedByteRleResult(actual.source, '
                                                        'actual.video_address, '
                                                        'actual.command_carrier, '
                                                        'replace_byte(retained.marker, '
                                                        'actual.marker), '
                                                        'replace_byte(retained.token, '
                                                        'actual.token), 0, packed_word, '
                                                        'actual.last_word, False, True, '
                                                        'False, False)'},
 'write_vdp_swapped_byte_rle_stream_frame': {'signature': 'state: SceneState, frame: '
                                                          'SceneControllerFrame',
                                             'returns': 'SceneControllerFrame',
                                             'flow': 'frame = checked_controller_frame(frame, '
                                                     'state)\n'
                                                     'actual = '
                                                     '_write_vdp_swapped_byte_rle_core(state, '
                                                     'frame.source, '
                                                     'VideoPlaneAddress(frame.x), frame)\n'
                                                     'if actual.live is None:\n'
                                                     "    raise Boundary('complete swapped "
                                                     'stream must return actual current '
                                                     "operands')\n"
                                                     'return actual.live.validate(state)'},
 'advance_plane_row': {'signature': 'state: SceneState, context: PlaneRowContext, current: '
                                    'SceneControllerFrame | None=None',
                       'returns': 'PlaneRowResult',
                       'flow': 'checked_context(context, PlaneRowContext, state)\n'
                               'if current is not None:\n'
                               '    current = checked_controller_frame(current, state)\n'
                               'column_step, column_bound, row_step = (1, 32, 1)\n'
                               'column = u16(context.column + column_step)\n'
                               'rows = context.rows_remaining\n'
                               'address, command = (context.video_address, '
                               'context.command_carrier)\n'
                               'discarded = None\n'
                               'if current is not None:\n'
                               '    difference = u8(low8(column) - column_bound)\n'
                               '    current = replace(current, '
                               'tile=replace_word(current.tile, column), '
                               'conditions=SceneControllerConditions(low8(column) < '
                               'column_bound, difference == 0, bool(difference & 128), '
                               'bool((low8(column) ^ column_bound) & (low8(column) ^ '
                               'difference) & 128)))\n'
                               'if low8(column) >= column_bound:\n'
                               '    rows = u16(rows - row_step)\n'
                               '    if current is not None:\n'
                               '        before = low16(current.row_count)\n'
                               '        current = replace(current, '
                               'row_count=replace_word(current.row_count, rows), '
                               'conditions=SceneControllerConditions(before < row_step, rows '
                               '== 0, bool(rows & 32768), bool((before ^ row_step) & (before '
                               '^ rows) & 32768)))\n'
                               '    if rows == 0:\n'
                               '        discarded = context.continuation\n'
                               '        command = discarded.return_carrier\n'
                               '        if current is not None:\n'
                               '            command = current.stack.long()\n'
                               '            discarded = StackContinuation(command)\n'
                               '            current = replace(current, x=command, '
                               'stack=current.stack.advance(4))\n'
                               '    else:\n'
                               '        address = address.advance_full(context.row_stride)\n'
                               '        if current is None:\n'
                               '            command = set_vram_write_address(state, address)\n'
                               '        else:\n'
                               '            current = _set_vram_write_address_frame(state, '
                               'current, address, 240462)\n'
                               '            command = current.x\n'
                               '        column = 0\n'
                               '        if current is not None:\n'
                               '            current = replace(current, tile=0, '
                               'destination=address, '
                               'conditions=SceneControllerConditions(False, True, False, '
                               'False))\n'
                               'return PlaneRowResult(address, column, rows, command, '
                               'discarded, current)'},
 'read_vdp_plane_rle_rows': {'signature': 'state: SceneState, source: Cursor, video_address: '
                                          'VideoPlaneAddress, row_stride: Long',
                             'returns': 'PlaneStreamResult',
                             'flow': 'return _read_vdp_plane_rle_rows_core(state, source, '
                                     'video_address, row_stride)'},
 '_read_vdp_plane_rle_rows_core': {'signature': 'state: SceneState, source: Cursor, '
                                                'video_address: VideoPlaneAddress, '
                                                'row_stride: Long, current: '
                                                'SceneControllerFrame | None=None',
                                   'returns': 'PlaneStreamResult',
                                   'flow': 'checked_state(state)\n'
                                           'checked_cursor(source, state)\n'
                                           '_video_address(video_address)\n'
                                           'uint(row_stride, 32)\n'
                                           'if current is not None:\n'
                                           '    current = checked_controller_frame(current, '
                                           'state)\n'
                                           '    if current.extent != row_stride:\n'
                                           "        raise ValueError('plane stride must be "
                                           "the actual current extent')\n"
                                           "_ram(state, '8000').set_word(0, 0)\n"
                                           'rows = 32\n'
                                           'if current is not None:\n'
                                           '    current = replace(current, '
                                           'row_count=replace_word(current.row_count, rows))\n'
                                           "_ram(state, '8002').set_word(0, 0)\n"
                                           'state.write(12582916, 2, 36610)\n'
                                           'if current is None:\n'
                                           '    command = set_vram_write_address(state, '
                                           'video_address)\n'
                                           'else:\n'
                                           '    current = replace(current, '
                                           'x=replace_word(current.x, video_address.word))\n'
                                           '    current = '
                                           '_set_vram_write_address_frame(state, current, '
                                           'video_address, 240360)\n'
                                           '    command = current.x\n'
                                           '    current = replace(current, tile=0, '
                                           'conditions=SceneControllerConditions(False, True, '
                                           'False, False))\n'
                                           'column, marker = (0, 0)\n'
                                           "if _ram(state, '8002').word() == 0:\n"
                                           '    marker = source.next_byte()\n'
                                           '    if current is not None:\n'
                                           '        current = replace(current, '
                                           'y=replace_byte(current.y, marker))\n'
                                           'while True:\n'
                                           '    high = source.next_byte()\n'
                                           '    if current is not None:\n'
                                           '        current = replace(current, '
                                           'attributes=replace_byte(current.attributes, '
                                           'high))\n'
                                           '        marker = low8(current.y)\n'
                                           "    literal = _ram(state, '8002').word() != 0 or "
                                           'marker != high\n'
                                           '    if literal:\n'
                                           '        value = high << 8 | source.next_byte()\n'
                                           "        value |= _ram(state, '8000').word()\n"
                                           '        if current is not None:\n'
                                           '            current = replace(current, '
                                           'attributes=replace_word(current.attributes, '
                                           'value))\n'
                                           '        state.write(12582912, 2, value)\n'
                                           '        if current is not None:\n'
                                           '            current = replace(current, '
                                           'stack=current.stack.advance(-4))\n'
                                           '            current.stack.set_long(0, 240400)\n'
                                           '        row = advance_plane_row(state, '
                                           'PlaneRowContext(video_address, row_stride, '
                                           'column, rows, command, '
                                           'StackContinuation(240400)), current)\n'
                                           '    else:\n'
                                           '        count = source.next_byte()\n'
                                           '        if current is not None:\n'
                                           '            current = replace(current, '
                                           'palette=count, '
                                           'conditions=SceneControllerConditions(False, count '
                                           '== 0, bool(count & 128), False))\n'
                                           '        if count == 0:\n'
                                           '            return PlaneStreamResult(source, '
                                           'video_address, command, column, rows, None, '
                                           'current)\n'
                                           '        value = source.next_byte() << 8 | '
                                           'source.next_byte()\n'
                                           '        remaining = count\n'
                                           '        for _ in descending_inclusive(count):\n'
                                           "            value |= _ram(state, '8000').word()\n"
                                           '            if current is not None:\n'
                                           '                current = replace(current, '
                                           'attributes=replace_word(current.attributes, '
                                           'value))\n'
                                           '            state.write(12582912, 2, value)\n'
                                           '            if current is not None:\n'
                                           '                current = replace(current, '
                                           'stack=current.stack.advance(-4))\n'
                                           '                current.stack.set_long(0, '
                                           '240428)\n'
                                           '            row = advance_plane_row(state, '
                                           'PlaneRowContext(video_address, row_stride, '
                                           'column, rows, command, '
                                           'StackContinuation(240428)), current)\n'
                                           '            video_address, column, rows, command '
                                           '= (row.video_address, row.column, '
                                           'row.rows_remaining, row.command_carrier)\n'
                                           '            current = row.live\n'
                                           '            if row.discarded_continuation is not '
                                           'None:\n'
                                           '                return PlaneStreamResult(source, '
                                           'video_address, command, column, rows, '
                                           'row.discarded_continuation, current)\n'
                                           '            if current is not None:\n'
                                           '                current = replace(current, '
                                           'stack=_scene_return_to_known_caller(state, '
                                           'current.stack, 240428))\n'
                                           '                remaining = u16(remaining - 1)\n'
                                           '                current = replace(current, '
                                           'palette=replace_word(current.palette, '
                                           'remaining))\n'
                                           '    video_address, column, rows, command = '
                                           '(row.video_address, row.column, '
                                           'row.rows_remaining, row.command_carrier)\n'
                                           '    if literal:\n'
                                           '        current = row.live\n'
                                           '    if row.discarded_continuation is not None:\n'
                                           '        return PlaneStreamResult(source, '
                                           'video_address, command, column, rows, '
                                           'row.discarded_continuation, current)\n'
                                           '    if literal and current is not None:\n'
                                           '        current = replace(current, '
                                           'stack=_scene_return_to_known_caller(state, '
                                           'current.stack, 240400))'},
 'read_vdp_plane_rle_rows_frame': {'signature': 'state: SceneState, frame: '
                                                'SceneControllerFrame',
                                   'returns': 'SceneControllerFrame',
                                   'flow': 'frame = checked_controller_frame(frame, state)\n'
                                           'if type(frame.destination) is not '
                                           'VideoPlaneAddress:\n'
                                           "    raise Boundary('3AACE requires the actual "
                                           "current A1 video address before DATA')\n"
                                           'actual = _read_vdp_plane_rle_rows_core(state, '
                                           'frame.source, frame.destination, frame.extent, '
                                           'frame)\n'
                                           'if actual.live is None:\n'
                                           "    raise Boundary('complete plane stream must "
                                           "return actual current operands')\n"
                                           'return actual.live.validate(state)'},
 'copy_scene_palette_variant': {'signature': 'state: SceneState, variant: Long',
                                'returns': 'PaletteCopyResult',
                                'flow': 'fields = _copy_scene_palette_variant_fields(state, '
                                        'variant, None)\n'
                                        'return PaletteCopyResult(fields.index_carrier, '
                                        'fields.source, fields.destination, '
                                        'fields.directory).validate(state)'},
 '_copy_scene_palette_variant_fields': {'signature': 'state: SceneState, variant: Long, '
                                                     'count_carrier: Long | None',
                                        'returns': 'PaletteCopyFields',
                                        'flow': 'checked_state(state)\n'
                                                'uint(variant, 32)\n'
                                                'if count_carrier is not None:\n'
                                                '    uint(count_carrier, 32)\n'
                                                'variant = _word_shift(variant, 3)\n'
                                                'directory = '
                                                'state.table(240556).advance(s16(low16(variant))).cursor()\n'
                                                'source = '
                                                'state.table(directory.next_long()).cursor()\n'
                                                'destination = '
                                                'state.table(u32(s16(directory.next_word()))).cursor()\n'
                                                'count = directory.next_word()\n'
                                                'for _ in descending_inclusive(count):\n'
                                                '    last_color_pair = source.next_long()\n'
                                                '    '
                                                'destination.append_long(last_color_pair)\n'
                                                'if count_carrier is not None:\n'
                                                '    count_carrier = '
                                                'replace_word(count_carrier, 65535)\n'
                                                'return PaletteCopyFields(variant, source, '
                                                'destination, directory, count_carrier, '
                                                'last_color_pair).validate(state)'},
 'copy_scene_palette_variant_complete': {'signature': 'state: SceneState, variant: Long, '
                                                      'count_carrier: Long',
                                         'returns': 'PaletteCopyCompleteResult',
                                         'flow': 'uint(count_carrier, 32)\n'
                                                 'fields = '
                                                 '_copy_scene_palette_variant_fields(state, '
                                                 'variant, count_carrier)\n'
                                                 'return '
                                                 'PaletteCopyCompleteResult(fields.index_carrier, '
                                                 'fields.source, fields.destination, '
                                                 'fields.directory, fields.count_carrier, '
                                                 'False, fields.last_color_pair == 0, '
                                                 'bool(fields.last_color_pair & 2147483648), '
                                                 'False).validate(state)'},
 '_begin_scene_palette_darken_core': {'signature': 'state: SceneState, value: Long',
                                      'returns': 'tuple[Long, Word]',
                                      'flow': 'checked_state(state)\n'
                                              'uint(value, 32)\n'
                                              'shade = 15\n'
                                              'value = replace_word(value, low16(value) & '
                                              '255)\n'
                                              "_ram(state, '80c4').set_word(0, low16(value))\n"
                                              "_ram(state, '80c6').set_word(0, 0)\n"
                                              "_ram(state, '80c8').set_word(0, shade)\n"
                                              'return (value, shade)'},
 'begin_scene_palette_darken': {'signature': 'state: SceneState, value: Long',
                                'returns': 'Long',
                                'flow': 'value, shade = '
                                        '_begin_scene_palette_darken_core(state, value)\n'
                                        'return value'},
 'begin_scene_palette_darken_frame': {'signature': 'state: SceneState, frame: '
                                                   'SceneControllerFrame',
                                      'returns': 'SceneControllerFrame',
                                      'flow': 'frame = checked_controller_frame(frame, '
                                              'state)\n'
                                              'value, shade = '
                                              '_begin_scene_palette_darken_core(state, '
                                              'frame.x)\n'
                                              'return replace(frame, x=value, '
                                              'conditions=_scene_logic_conditions(shade, '
                                              '16))'},
 'snapshot_and_clear_scene_palette': {'signature': 'state: SceneState',
                                      'returns': 'PaletteSnapshotResult',
                                      'flow': 'checked_state(state)\n'
                                              'source, destination = (_ram(state, '
                                              "'fb00').cursor(), _ram(state, "
                                              "'fb80').cursor())\n"
                                              'for _ in range(32):\n'
                                              '    destination.append_long(source.long())\n'
                                              '    source.append_long(0)\n'
                                              'return PaletteSnapshotResult(source, '
                                              'destination)'},
 'snapshot_and_clear_scene_palette_frame': {'signature': 'state: SceneState, frame: '
                                                         'SceneControllerFrame',
                                            'returns': 'SceneControllerFrame',
                                            'flow': 'frame = checked_controller_frame(frame, '
                                                    'state)\n'
                                                    'actual = '
                                                    'snapshot_and_clear_scene_palette(state)\n'
                                                    'return replace(frame, y=65535, '
                                                    'source=actual.source, '
                                                    'destination=actual.destination, '
                                                    'conditions=SceneControllerConditions(False, '
                                                    'True, False, False))'},
 'fade_palette_component': {'signature': 'state: SceneState, color: Long, accumulated: Long, '
                                         'component: Long=0',
                            'returns': 'PaletteComponentResult',
                            'flow': 'checked_state(state)\n'
                                    'for value in (color, accumulated, component):\n'
                                    '    uint(value, 32)\n'
                                    'component = replace_byte(component, low8(color))\n'
                                    'component = replace_word(component, low16(component) & '
                                    '14)\n'
                                    "shade = _ram(state, '8001').byte()\n"
                                    'borrowed = low8(component) < shade\n'
                                    'component = replace_byte(component, u8(low8(component) - '
                                    'shade))\n'
                                    'if borrowed:\n'
                                    '    component = 0\n'
                                    'accumulated = replace_word(accumulated, '
                                    'low16(accumulated) | low16(component))\n'
                                    'accumulated = _ror_word(accumulated, 4)\n'
                                    'color = replace_word(color, low16(color) >> 4)\n'
                                    'return PaletteComponentResult(color, accumulated, '
                                    'component)'},
 'advance_scene_palette_fade': {'signature': 'state: SceneState, retained: Long=0',
                                'returns': 'Long',
                                'flow': 'return _advance_scene_palette_fade_core(state, '
                                        'retained)'},
 '_scene_logic_conditions': {'signature': 'value, width',
                             'returns': None,
                             'flow': 'value &= (1 << width) - 1\n'
                                     'return SceneControllerConditions(False, value == 0, '
                                     'bool(value & 1 << width - 1), False)'},
 '_scene_subtract_conditions': {'signature': 'left, right, width',
                                'returns': None,
                                'flow': 'mask, sign = ((1 << width) - 1, 1 << width - 1)\n'
                                        'left, right = (left & mask, right & mask)\n'
                                        'difference = left - right & mask\n'
                                        'return SceneControllerConditions(left < right, '
                                        'difference == 0, bool(difference & sign), bool((left '
                                        '^ right) & (left ^ difference) & sign))'},
 '_advance_scene_palette_fade_core': {'signature': 'state: SceneState, retained: Long, '
                                                   'current: SceneControllerFrame | None=None',
                                      'returns': 'Long | SceneControllerFrame',
                                      'flow': 'checked_state(state)\n'
                                              'uint(retained, 32)\n'
                                              'if current is not None:\n'
                                              '    current = '
                                              'checked_controller_frame(current, state)\n'
                                              'retained = replace_word(retained, _ram(state, '
                                              "'80c4').word())\n"
                                              'if current is not None:\n'
                                              '    current = replace(current, x=retained, '
                                              'conditions=_scene_logic_conditions(retained, '
                                              '16))\n'
                                              'if negative_word(low16(retained)):\n'
                                              '    return retained if current is None else '
                                              'current\n'
                                              'delay_step = 1\n'
                                              "previous_delay = _ram(state, '80c6').word()\n"
                                              'delay = u16(previous_delay - delay_step)\n'
                                              "_ram(state, '80c6').set_word(0, delay)\n"
                                              'if current is not None:\n'
                                              '    current = replace(current, '
                                              'conditions=_scene_subtract_conditions(previous_delay, '
                                              'delay_step, 16))\n'
                                              'if not negative_word(delay):\n'
                                              '    return retained if current is None else '
                                              'current\n'
                                              'retained = replace_word(retained, '
                                              'low16(retained) & 255)\n'
                                              "_ram(state, '80c6').set_word(0, "
                                              'low16(retained))\n'
                                              "if _ram(state, '80c4').byte() == 0:\n"
                                              "    shade = u16(_ram(state, '80c8').word() - "
                                              '1)\n'
                                              "    _ram(state, '80c8').set_word(0, shade)\n"
                                              '    if negative_word(shade):\n'
                                              "        _ram(state, '80c4').set_word(0, "
                                              '65535)\n'
                                              '        if current is not None:\n'
                                              '            current = replace(current, '
                                              'x=retained, '
                                              'conditions=_scene_logic_conditions(65535, '
                                              '16))\n'
                                              '        return retained if current is None '
                                              'else current\n'
                                              'else:\n'
                                              "    shade = u16(_ram(state, '80c8').word() + "
                                              '1)\n'
                                              "    _ram(state, '80c8').set_word(0, shade)\n"
                                              "    if _ram(state, '80c8').word() > 15:\n"
                                              "        _ram(state, '80c4').set_word(0, "
                                              '65535)\n'
                                              '        if current is not None:\n'
                                              '            current = replace(current, '
                                              'x=retained, '
                                              'conditions=_scene_logic_conditions(65535, '
                                              '16))\n'
                                              '        return retained if current is None '
                                              'else current\n'
                                              'retained = replace_word(retained, _ram(state, '
                                              "'80c8').word())\n"
                                              'retained = replace_word(retained, '
                                              'low16(retained) & 14)\n'
                                              "_ram(state, '8000').set_word(0, "
                                              'low16(retained))\n'
                                              'offset = 0\n'
                                              'if current is not None:\n'
                                              '    current = replace(current, x=retained, '
                                              'attributes=0, layer=0, source=_ram(state, '
                                              "'fb00').cursor(), destination=_ram(state, "
                                              "'fb80').cursor(), directory=_ram(state, "
                                              "'80ca'))\n"
                                              'for mask_offset in (0, 4):\n'
                                              '    mask = _ram(state, '
                                              "'80ca').long(mask_offset)\n"
                                              '    if current is not None:\n'
                                              '        current = replace(current, y=31, '
                                              'row_count=mask)\n'
                                              '    remaining = 31\n'
                                              '    for _ in range(32):\n'
                                              '        selected = mask & 1\n'
                                              '        mask >>= 1\n'
                                              '        if current is not None:\n'
                                              '            current = replace(current, '
                                              'row_count=mask)\n'
                                              '        if selected:\n'
                                              '            color_word = _ram(state, '
                                              "'fb80').word(offset)\n"
                                              '            if current is None:\n'
                                              '                color, accumulated, component '
                                              '= (color_word, 0, 0)\n'
                                              '            else:\n'
                                              '                color = '
                                              'replace_word(current.palette, color_word)\n'
                                              '                accumulated = '
                                              'replace_word(current.extent, 0)\n'
                                              '                component = current.tile\n'
                                              '            for continuation in (240108, '
                                              '240112, 240116):\n'
                                              '                if current is not None:\n'
                                              '                    current = replace(current, '
                                              'stack=current.stack.advance(-4))\n'
                                              '                    current.stack.set_long(0, '
                                              'continuation)\n'
                                              '                result = '
                                              'fade_palette_component(state, color, '
                                              'accumulated, component)\n'
                                              '                color, accumulated, component '
                                              '= (result.color, result.accumulated, '
                                              'result.component)\n'
                                              '                if current is not None:\n'
                                              '                    current = replace(current, '
                                              'stack=_scene_return_to_known_caller(state, '
                                              'current.stack, continuation))\n'
                                              '            accumulated = '
                                              '_ror_word(accumulated, 4)\n'
                                              '            _ram(state, '
                                              "'fb00').set_word(offset, low16(accumulated))\n"
                                              '            if current is not None:\n'
                                              '                current = replace(current, '
                                              'palette=color, tile=component, '
                                              'extent=accumulated)\n'
                                              '        offset = u16(offset + 2)\n'
                                              '        remaining = u16(remaining - 1)\n'
                                              '        if current is not None:\n'
                                              '            current = replace(current, '
                                              'attributes=replace_word(current.attributes, '
                                              'offset), y=replace_word(current.y, '
                                              'remaining))\n'
                                              '    if current is not None:\n'
                                              '        current = replace(current, '
                                              'layer=replace_word(current.layer, mask_offset '
                                              '+ 4))\n'
                                              'if current is not None:\n'
                                              '    return replace(current, '
                                              'conditions=_scene_subtract_conditions(low16(current.layer), '
                                              '8, 16))\n'
                                              'return retained'},
 'advance_scene_palette_fade_frame': {'signature': 'state: SceneState, frame: '
                                                   'SceneControllerFrame',
                                      'returns': 'SceneControllerFrame',
                                      'flow': 'frame = checked_controller_frame(frame, '
                                              'state)\n'
                                              'actual = '
                                              '_advance_scene_palette_fade_core(state, '
                                              'frame.x, frame)\n'
                                              'if type(actual) is not SceneControllerFrame:\n'
                                              "    raise Boundary('complete palette fade "
                                              "requires actual current operands')\n"
                                              'return actual.validate(state)'},
 'sample_random_preserving_seed_carrier': {'signature': 'state: SceneState',
                                           'returns': 'Long',
                                           'flow': 'from .business_reuse import step_random\n'
                                                   'checked_state(state)\n'
                                                   'return step_random(state)'},
 'sample_random_preserving_seed_frame': {'signature': 'state: SceneState, frame: '
                                                      'SceneControllerFrame',
                                         'returns': 'SceneControllerFrame',
                                         'flow': 'from .business_reuse import '
                                                 '_reuse_advance_random_pair\n'
                                                 'frame = checked_controller_frame(frame, '
                                                 'state)\n'
                                                 'stack = frame.stack.advance(-4)\n'
                                                 'stack.set_long(0, frame.y)\n'
                                                 'stack = stack.advance(-4)\n'
                                                 'stack.set_long(0, 243500)\n'
                                                 'sample = _reuse_advance_random_pair(state)\n'
                                                 'stack = '
                                                 '_scene_return_to_known_caller(state, stack, '
                                                 '243500)\n'
                                                 'secondary = stack.long()\n'
                                                 'return replace(frame, x=sample.sample, '
                                                 'y=secondary, stack=stack.advance(4), '
                                                 'conditions=SceneControllerConditions(False, '
                                                 'sample.updated_state == 0, '
                                                 'bool(sample.updated_state & 2147483648), '
                                                 'False)).validate(state)'},
 'finish_one_scene_sprite_chain': {'signature': 'state: SceneState, heads: Table, layer: '
                                                'Word, next_link: Long',
                                   'returns': 'Long',
                                   'flow': 'checked_state(state)\n'
                                           'checked_table(heads, state)\n'
                                           'uint(layer, 16)\n'
                                           'uint(next_link, 32)\n'
                                           'if heads.long(layer) != 0:\n'
                                           '    tail = state.table(heads.long(layer, 64))\n'
                                           '    tail.set_byte(0, low8(next_link), 3)\n'
                                           '    next_link = replace_byte(next_link, '
                                           'heads.byte(layer, 32))\n'
                                           'return next_link'},
 'clear_scene_sprite_chain_heads': {'signature': 'state: SceneState',
                                    'returns': 'Long',
                                    'flow': 'checked_state(state)\n'
                                            "heads = _ram(state, '7006')\n"
                                            'for offset in range(0, 32, 4):\n'
                                            '    heads.set_long(offset, 0)\n'
                                            "_ram(state, 'f300').set_byte(0, 0)\n"
                                            'return 0'},
 'finish_scene_sprite_chains': {'signature': 'state: SceneState',
                                'returns': 'Long',
                                'flow': 'checked_state(state)\n'
                                        "heads, next_link = (_ram(state, '7006'), 0)\n"
                                        'for layer in range(28, -1, -4):\n'
                                        '    next_link = finish_one_scene_sprite_chain(state, '
                                        'heads, layer, next_link)\n'
                                        'return clear_scene_sprite_chain_heads(state)'},
 'finish_one_actor_sprite_chain': {'signature': 'state: SceneState, heads: Table, layer: '
                                                'Word, next_link: Long, current: '
                                                'SceneControllerFrame | None=None',
                                   'returns': 'Long | SceneControllerFrame',
                                   'flow': 'checked_state(state)\n'
                                           'checked_table(heads, state)\n'
                                           'uint(layer, 16)\n'
                                           'uint(next_link, 32)\n'
                                           'if current is not None:\n'
                                           '    current = checked_controller_frame(current, '
                                           'state)\n'
                                           'if heads.long(layer) != 0:\n'
                                           '    tail = state.table(heads.long(layer, 64))\n'
                                           '    tail.set_byte(0, low8(next_link), 3)\n'
                                           '    next_link = replace_byte(next_link, '
                                           'heads.byte(layer, 32))\n'
                                           '    if current is not None:\n'
                                           '        current = replace(current, '
                                           'destination=tail.cursor())\n'
                                           'if current is not None:\n'
                                           '    return replace(current, y=next_link)\n'
                                           'return next_link'},
 'finish_actor_sprite_chains': {'signature': 'state: SceneState',
                                'returns': 'Long',
                                'flow': 'return _finish_actor_sprite_chains_core(state)'},
 '_finish_actor_sprite_chains_core': {'signature': 'state: SceneState, current: '
                                                   'SceneControllerFrame | None=None',
                                      'returns': 'Long | SceneControllerFrame',
                                      'flow': 'checked_state(state)\n'
                                              'if current is not None:\n'
                                              '    current = '
                                              'checked_controller_frame(current, state)\n'
                                              "heads, next_link = (_ram(state, '8044'), 0)\n"
                                              'if current is not None:\n'
                                              '    current = replace(current, x=28, y=0, '
                                              'source=heads.cursor())\n'
                                              'for layer in range(28, -1, -4):\n'
                                              '    if current is None:\n'
                                              '        next_link = '
                                              'finish_one_actor_sprite_chain(state, heads, '
                                              'layer, next_link)\n'
                                              '    else:\n'
                                              '        current = replace(current, '
                                              'x=replace_word(current.x, layer), '
                                              'stack=current.stack.advance(-4))\n'
                                              '        current.stack.set_long(0, 242246)\n'
                                              '        current = '
                                              'finish_one_actor_sprite_chain(state, heads, '
                                              'layer, next_link, current)\n'
                                              '        next_link = current.y\n'
                                              '        current = replace(current, '
                                              'stack=_scene_return_to_known_caller(state, '
                                              'current.stack, 242246), '
                                              'x=replace_word(current.x, u16(layer - 4)))\n'
                                              'for offset in range(0, 32, 4):\n'
                                              '    heads.set_long(offset, 0)\n'
                                              "_ram(state, 'f300').set_byte(0, 0)\n"
                                              'if current is not None:\n'
                                              '    return replace(current, x=0, '
                                              'conditions=SceneControllerConditions(False, '
                                              'True, False, False))\n'
                                              'return 0'},
 'finish_actor_sprite_chains_frame': {'signature': 'state: SceneState, frame: '
                                                   'SceneControllerFrame',
                                      'returns': 'SceneControllerFrame',
                                      'flow': 'frame = checked_controller_frame(frame, '
                                              'state)\n'
                                              'actual = '
                                              '_finish_actor_sprite_chains_core(state, '
                                              'frame)\n'
                                              'if type(actual) is not SceneControllerFrame:\n'
                                              "    raise Boundary('complete actor chains "
                                              "require actual current operands')\n"
                                              'return actual.validate(state)'},
 '_apply_sprite_delta': {'signature': 'origin, delta, flipped',
                         'returns': None,
                         'flow': 'if flipped:\n'
                                 '    delta = u8(-delta)\n'
                                 'if delta & 128:\n'
                                 '    return u16(origin - u8(-delta))\n'
                                 'return u16(origin + delta)'},
 '_append_scene_sprites': {'signature': 'state, source, frame, clipped',
                           'returns': None,
                           'flow': 'checked_state(state)\n'
                                   'checked_cursor(source, state)\n'
                                   'if type(frame) is not SceneRenderFrame:\n'
                                   "    raise ValueError('explicit scene render operands "
                                   "required')\n"
                                   'frame.validate(state)\n'
                                   "if _ram(state, 'f300').byte() >= 128:\n"
                                   '    return SpriteBatchResult(source, frame)\n'
                                   'tile = frame.tile & 65535\n'
                                   'layer = u16((low16(frame.attributes) & 7) << 2)\n'
                                   'attributes = replace_word(frame.attributes, '
                                   'low16(frame.attributes) & 65528)\n'
                                   'x = replace_word(frame.x, u16(low16(frame.x) + 128))\n'
                                   'if negative_word(low16(x)):\n'
                                   '    return SpriteBatchResult(source, SceneRenderFrame(x, '
                                   'frame.y, attributes, frame.palette, tile))\n'
                                   'if attributes & 32:\n'
                                   '    x = replace_word(x, u16(low16(x) - 8))\n'
                                   'y = replace_word(frame.y, u16(low16(frame.y) + 128))\n'
                                   'if attributes & 16:\n'
                                   '    y = replace_word(y, u16(low16(y) - 8))\n'
                                   "offset = u16(_ram(state, 'f300').byte() << 3)\n"
                                   "destination = _ram(state, 'f800').cursor(offset)\n"
                                   "heads = _ram(state, '7006')\n"
                                   'while True:\n'
                                   '    if clipped:\n'
                                   "        _ram(state, '7030').set_word(0, 0)\n"
                                   '    horizontal = source.byte()\n'
                                   '    if horizontal == 128:\n'
                                   '        break\n'
                                   '    if clipped:\n'
                                   '        projected = _apply_sprite_delta(_ram(state, '
                                   "'7028').word(), horizontal, False)\n"
                                   '        if projected < 16 or projected > 112:\n'
                                   "            _ram(state, '7030').set_word(0, 1)\n"
                                   "        if _ram(state, '7030').word() != 0:\n"
                                   '            source.base = u32(source.base + 4)\n'
                                   "            if _ram(state, 'f300').byte() >= 128:\n"
                                   '                break\n'
                                   '            continue\n'
                                   '    first_coordinate = _apply_sprite_delta(low16(x), '
                                   'horizontal, bool(attributes & 32))\n'
                                   '    destination.set_word(0, first_coordinate)\n'
                                   '    vertical = source.byte(0, 3)\n'
                                   '    if clipped:\n'
                                   "        _ram(state, '7030').set_word(0, 0)\n"
                                   '        projected = _apply_sprite_delta(_ram(state, '
                                   "'702a').word(), vertical, False)\n"
                                   '        if projected < 16 or projected > 160:\n'
                                   "            _ram(state, '7030').set_word(0, 1)\n"
                                   "        if _ram(state, '7030').word() != 0:\n"
                                   '            source.base = u32(source.base + 4)\n'
                                   "            if _ram(state, 'f300').byte() >= 128:\n"
                                   '                break\n'
                                   '            continue\n'
                                   '    destination.set_word(0, _apply_sprite_delta(low16(y), '
                                   'vertical, bool(attributes & 16)), 6)\n'
                                   '    destination.set_byte(0, source.byte(0, 1), 2)\n'
                                   '    if heads.long(layer) == 0:\n'
                                   '        heads.set_long(layer, destination.base)\n'
                                   "        heads.set_byte(layer, _ram(state, 'f300').byte(), "
                                   '32)\n'
                                   '    else:\n'
                                   '        tail = state.table(heads.long(layer, 64))\n'
                                   "        tail.set_byte(0, _ram(state, 'f300').byte(), 3)\n"
                                   '    heads.set_long(layer, destination.base, 64)\n'
                                   "    _ram(state, 'f300').set_byte(0, u8(_ram(state, "
                                   "'f300').byte() + 1))\n"
                                   '    encoded = source.byte(0, 1) & 240\n'
                                   '    encoded = u16(encoded & 65280 | u8(encoded + '
                                   'low8(frame.palette)))\n'
                                   '    encoded ^= low16(attributes)\n'
                                   '    encoded = u16(encoded << 7)\n'
                                   '    encoded = u16(encoded & 65280 | (low8(encoded) | '
                                   'source.byte(0, 2)))\n'
                                   '    encoded = u16(encoded + low16(tile))\n'
                                   '    destination.set_word(0, encoded, 4)\n'
                                   '    destination.base = u32(destination.base + 8)\n'
                                   '    source.base = u32(source.base + 4)\n'
                                   "    if _ram(state, 'f300').byte() >= 128:\n"
                                   '        break\n'
                                   'return SpriteBatchResult(source, SceneRenderFrame(x, y, '
                                   'attributes, frame.palette, tile))'},
 'append_clipped_scene_sprites': {'signature': 'state: SceneState, source: Cursor, frame: '
                                               'SceneRenderFrame',
                                  'returns': 'SpriteBatchResult',
                                  'flow': 'return _append_scene_sprites(state, source, frame, '
                                          'True)'},
 'append_unclipped_scene_sprites': {'signature': 'state: SceneState, source: Cursor, frame: '
                                                 'SceneRenderFrame',
                                    'returns': 'SpriteBatchResult',
                                    'flow': 'return _append_scene_sprites(state, source, '
                                            'frame, False)'},
 'append_scene_marker_sprite': {'signature': 'state: SceneState, x: Long, y: Long',
                                'returns': 'SpriteBatchResult',
                                'flow': 'checked_state(state)\n'
                                        'uint(x, 32)\n'
                                        'uint(y, 32)\n'
                                        'frame = SceneRenderFrame(replace_word(x, '
                                        'u16(low16(x) - 64)), replace_word(y, u16(low16(y) - '
                                        '64)), 0, 0, 0)\n'
                                        'return append_clipped_scene_sprites(state, '
                                        'state.table(239432).cursor(), frame)'},
 'update_scripted_scene_position': {'signature': 'state: SceneState',
                                    'returns': 'None',
                                    'flow': 'checked_state(state)\n'
                                            "if _ram(state, 'f320').word() & 7:\n"
                                            '    return\n'
                                            "if _ram(state, '702c').byte() == 0:\n"
                                            '    return\n'
                                            "_ram(state, '702e').set_word(0, u16(_ram(state, "
                                            "'702e').word() + 1))\n"
                                            "mode = _ram(state, '7026').word()\n"
                                            'limit = state.table(236162).byte(mode)\n'
                                            "travelled = _ram(state, '702e').word()\n"
                                            'if low8(travelled) > limit:\n'
                                            '    return\n'
                                            "movement = _ram(state, '702c').byte()\n"
                                            'distance = movement & 15\n'
                                            'if movement & 16:\n'
                                            "    _ram(state, '7028').set_word(0, "
                                            "u16(_ram(state, '7028').word() - distance))\n"
                                            'elif movement & 32:\n'
                                            "    _ram(state, '7028').set_word(0, "
                                            "u16(_ram(state, '7028').word() + distance))\n"
                                            'elif movement & 64:\n'
                                            "    _ram(state, '702a').set_word(0, "
                                            "u16(_ram(state, '702a').word() - distance))\n"
                                            'elif movement & 128:\n'
                                            "    _ram(state, '702a').set_word(0, "
                                            "u16(_ram(state, '702a').word() + distance))"},
 'initialize_scripted_secondary_position': {'signature': 'state: SceneState, mode: Word',
                                            'returns': 'None',
                                            'flow': 'checked_state(state)\n'
                                                    'uint(mode, 16)\n'
                                                    "if _ram(state, '7036').word() != 0:\n"
                                                    '    return\n'
                                                    'offset = u16(mode << 1)\n'
                                                    'x = state.table(232328).word(offset)\n'
                                                    'y = state.table(232408).word(offset)\n'
                                                    "_ram(state, '7032').set_word(0, x)\n"
                                                    "_ram(state, '7034').set_word(0, y)\n"
                                                    "_ram(state, '7036').set_word(0, 1)"},
 'select_scene_object_frame': {'signature': 'state: SceneState, frame_offset: Long, '
                                            'tick_carrier: Long=0',
                               'returns': 'SceneFrameResult',
                               'flow': 'checked_state(state)\n'
                                       'uint(frame_offset, 32)\n'
                                       'uint(tick_carrier, 32)\n'
                                       "if _ram(state, '7026').word() <= 27:\n"
                                       '    source = '
                                       'state.table(state.table(237674).long(low16(frame_offset))).cursor()\n'
                                       '    return SceneFrameResult(source, frame_offset)\n'
                                       'if low16(frame_offset) <= 7:\n'
                                       "    sequence_offset = _ram(state, '703c').word()\n"
                                       '    if low16(tick_carrier) & 7 == 0:\n'
                                       "        _ram(state, '703c').set_word(0, "
                                       'u16(sequence_offset + 1))\n'
                                       "        sequence_offset = _ram(state, '703c').word()\n"
                                       '    frame_offset = replace_byte(frame_offset, '
                                       'state.table(237796).byte(sequence_offset))\n'
                                       '    if low8(frame_offset) == 255:\n'
                                       "        _ram(state, '703c').set_word(0, 0)\n"
                                       '        frame_offset = 0\n'
                                       'frame_offset &= 15\n'
                                       'source = '
                                       'state.table(state.table(237690).long(low16(frame_offset))).cursor()\n'
                                       'return SceneFrameResult(source, frame_offset)'},
 '_copy_scene_palette_longs': {'signature': 'state, source',
                               'returns': None,
                               'flow': "destination = _ram(state, 'fb00').cursor()\n"
                                       'for _ in range(8):\n'
                                       '    destination.append_long(source.next_long())'},
 '_copy_scene_palette_words': {'signature': 'state, source',
                               'returns': None,
                               'flow': "destination = _ram(state, 'fb00').cursor()\n"
                                       'for _ in range(16):\n'
                                       '    destination.append_word(source.next_word())'},
 '_scene_pointer': {'signature': 'state, pointer_table, offset=0',
                    'returns': None,
                    'flow': 'return '
                            'state.table(state.table(pointer_table).long(offset)).cursor()'},
 '_draw_fixed_scene_pointer': {'signature': 'state, pointer_table, attributes, offset=0, '
                                            'tile=0',
                               'returns': None,
                               'flow': 'source = _scene_pointer(state, pointer_table, '
                                       'offset)\n'
                                       'return append_unclipped_scene_sprites(state, source, '
                                       'SceneRenderFrame(96, 96, attributes, 0, tile))'},
 '_draw_moving_scene_pointer': {'signature': 'state, pointer_table, attributes, offset=0, '
                                             'tile=0',
                                'returns': None,
                                'flow': 'source = _scene_pointer(state, pointer_table, '
                                        'offset)\n'
                                        "x = _ram(state, '7028').word()\n"
                                        "y = _ram(state, '702a').word()\n"
                                        'return append_clipped_scene_sprites(state, source, '
                                        'SceneRenderFrame(x, y, attributes, 0, tile))'},
 '_draw_scripted_sequence': {'signature': 'state',
                             'returns': None,
                             'flow': "if _ram(state, 'f320').word() & 7 == 0:\n"
                                     "    _ram(state, '7004').set_word(0, u16(_ram(state, "
                                     "'7004').word() + 1))\n"
                                     'while True:\n'
                                     "    mode_offset = u16(_ram(state, '7026').word() << 2)\n"
                                     '    sequence = _scene_pointer(state, 231954, '
                                     'mode_offset)\n'
                                     '    sequence.base = u32(sequence.base + s16(_ram(state, '
                                     "'7004').word()))\n"
                                     '    frame = sequence.byte()\n'
                                     '    if not frame & 128:\n'
                                     '        break\n'
                                     '    sequence.base = u32(sequence.base + 1)\n'
                                     '    frame = sequence.byte()\n'
                                     "    _ram(state, '7004').set_word(0, frame)\n"
                                     "if _ram(state, '7026').word() == 5:\n"
                                     '    if frame >= 3:\n'
                                     '        skip_palette = False\n'
                                     "        if _ram(state, 'f320').word() & 7 == 0:\n"
                                     "            if _ram(state, '703c').word() == 40:\n"
                                     '                skip_palette = True\n'
                                     '            else:\n'
                                     "                _ram(state, '703c').set_word(0, "
                                     "u16(_ram(state, '703c').word() + 4))\n"
                                     '        if not skip_palette:\n'
                                     "            offset = _ram(state, '703c').word()\n"
                                     '            _copy_scene_palette_longs(state, '
                                     '_scene_pointer(state, 235876, offset))\n'
                                     "if _ram(state, '7026').word() == 1:\n"
                                     '    palette_offset = 0 if frame == 1 else 32\n'
                                     '    _copy_scene_palette_longs(state, '
                                     'state.table(233112).cursor(palette_offset))\n'
                                     'update_scripted_scene_position(state)\n'
                                     "mode_offset = u16(_ram(state, '7026').word() << 2)\n"
                                     'objects = '
                                     'state.table(state.table(232488).long(mode_offset))\n'
                                     'source = state.table(objects.long(u16(frame << '
                                     '2))).cursor()\n'
                                     "x, y = (_ram(state, '7028').word(), _ram(state, "
                                     "'702a').word())\n"
                                     'append_clipped_scene_sprites(state, source, '
                                     'SceneRenderFrame(x, y, 4, 0, 0))\n'
                                     "mode = _ram(state, '7026').word()\n"
                                     'if state.table(231834).byte(mode) == 1:\n'
                                     "    mode_offset = u16(_ram(state, '7026').word() << 2)\n"
                                     '    objects = '
                                     'state.table(state.table(232852).long(mode_offset))\n'
                                     '    source = state.table(objects.long(u16(frame << '
                                     '2))).cursor()\n'
                                     "    x, y = (_ram(state, '7028').word(), _ram(state, "
                                     "'702a').word())\n"
                                     '    append_clipped_scene_sprites(state, source, '
                                     'SceneRenderFrame(x, y, 4, 0, 256))\n'
                                     'finish_scene_sprite_chains(state)'},
 '_draw_scripted_arrival': {'signature': 'state',
                            'returns': None,
                            'flow': 'while True:\n'
                                    "    _ram(state, '703c').set_word(0, u16(_ram(state, "
                                    "'703c').word() + 1))\n"
                                    "    if _ram(state, '703c').word() == 144:\n"
                                    "        offset = u16(_ram(state, '7026').word() << 1)\n"
                                    '        x = state.table(236524).word(offset)\n'
                                    '        y = state.table(236572).word(offset)\n'
                                    "        _ram(state, '7028').set_word(0, x)\n"
                                    "        _ram(state, '702a').set_word(0, y)\n"
                                    '        break\n'
                                    "    if _ram(state, '703c').word() > 144:\n"
                                    '        break\n'
                                    '    _draw_fixed_scene_pointer(state, 236468, 5, '
                                    'tile=256)\n'
                                    '    _draw_fixed_scene_pointer(state, 236476, 5)\n'
                                    "    if _ram(state, '7028').word() >= 96:\n"
                                    "        if _ram(state, 'f320').word() & 3 == 0:\n"
                                    "            _ram(state, '7028').set_word(0, "
                                    "u16(_ram(state, '7028').word() - 1))\n"
                                    '    _draw_moving_scene_pointer(state, 236472, 4)\n'
                                    "mode = _ram(state, '7026').word()\n"
                                    'variant = state.table(236760).byte(mode)\n'
                                    'offset = u16(variant << 2)\n'
                                    '_draw_fixed_scene_pointer(state, 236728, 3, offset)\n'
                                    'if mode != 12:\n'
                                    '    update_scripted_scene_position(state)\n'
                                    '    _draw_moving_scene_pointer(state, 236744, 2, '
                                    'offset)'},
 '_draw_scripted_paired_positions': {'signature': 'state',
                                     'returns': None,
                                     'flow': 'update_scripted_scene_position(state)\n'
                                             '_draw_moving_scene_pointer(state, 237328, 5)\n'
                                             "saved_movement = _ram(state, '702c').byte()\n"
                                             "saved_x = _ram(state, '7028').word()\n"
                                             "saved_y = _ram(state, '702a').word()\n"
                                             "_ram(state, '7026').set_word(0, u16(_ram(state, "
                                             "'7026').word() + 1))\n"
                                             "mode = _ram(state, '7026').word()\n"
                                             'movement = state.table(233040).byte(mode)\n'
                                             "_ram(state, '702c').set_byte(0, movement)\n"
                                             'initialize_scripted_secondary_position(state, '
                                             'mode)\n'
                                             "_ram(state, '7028').set_word(0, _ram(state, "
                                             "'7032').word())\n"
                                             "_ram(state, '702a').set_word(0, _ram(state, "
                                             "'7034').word())\n"
                                             'update_scripted_scene_position(state)\n'
                                             '_draw_moving_scene_pointer(state, 237328, 4, '
                                             '4)\n'
                                             "_ram(state, '7032').set_word(0, _ram(state, "
                                             "'7028').word())\n"
                                             "_ram(state, '7034').set_word(0, _ram(state, "
                                             "'702a').word())\n"
                                             "_ram(state, '702c').set_byte(0, "
                                             'saved_movement)\n'
                                             "_ram(state, '7028').set_word(0, saved_x)\n"
                                             "_ram(state, '702a').set_word(0, saved_y)\n"
                                             "_ram(state, '7026').set_word(0, u16(_ram(state, "
                                             "'7026').word() - 1))"},
 '_draw_scripted_staged_pair': {'signature': 'state',
                                'returns': None,
                                'flow': "_ram(state, '7044').set_word(0, u16(_ram(state, "
                                        "'7044').word() + 1))\n"
                                        "tick = _ram(state, 'f320').word()\n"
                                        'frame_offset = 4 if tick & 8 else 0\n'
                                        'selected = select_scene_object_frame(state, '
                                        'frame_offset, tick)\n'
                                        'rendered = append_unclipped_scene_sprites(state, '
                                        'selected.source, SceneRenderFrame(96, 96, 5, 0, 0))\n'
                                        "if _ram(state, '7044').word() < 32:\n"
                                        '    return\n'
                                        'update_scripted_scene_position(state)\n'
                                        'selected = select_scene_object_frame(state, 8, '
                                        'rendered.frame.x)\n'
                                        "x, y = (_ram(state, '7028').word(), _ram(state, "
                                        "'702a').word())\n"
                                        'append_clipped_scene_sprites(state, selected.source, '
                                        'SceneRenderFrame(x, y, 4, 0, 0))\n'
                                        "if _ram(state, '7044').word() < 64:\n"
                                        '    return\n'
                                        "saved_x = _ram(state, '7028').word()\n"
                                        "saved_y = _ram(state, '702a').word()\n"
                                        "saved_movement = _ram(state, '702c').byte()\n"
                                        "_ram(state, '7026').set_word(0, u16(_ram(state, "
                                        "'7026').word() + 1))\n"
                                        "mode = _ram(state, '7026').word()\n"
                                        'movement = state.table(233040).byte(mode)\n'
                                        "_ram(state, '702c').set_byte(0, movement)\n"
                                        "_ram(state, '7028').set_word(0, _ram(state, "
                                        "'7032').word())\n"
                                        "_ram(state, '702a').set_word(0, _ram(state, "
                                        "'7034').word())\n"
                                        'update_scripted_scene_position(state)\n'
                                        'selected = select_scene_object_frame(state, 12)\n'
                                        "x, y = (_ram(state, '7028').word(), _ram(state, "
                                        "'702a').word())\n"
                                        'append_clipped_scene_sprites(state, selected.source, '
                                        'SceneRenderFrame(x, y, 4, 0, 0))\n'
                                        "_ram(state, '7032').set_word(0, _ram(state, "
                                        "'7028').word())\n"
                                        "_ram(state, '7034').set_word(0, _ram(state, "
                                        "'702a').word())\n"
                                        "_ram(state, '7028').set_word(0, saved_x)\n"
                                        "_ram(state, '702a').set_word(0, saved_y)\n"
                                        "_ram(state, '702c').set_byte(0, saved_movement)\n"
                                        "_ram(state, '7026').set_word(0, u16(_ram(state, "
                                        "'7026').word() - 1))"},
 '_draw_scripted_landing': {'signature': 'state',
                            'returns': None,
                            'flow': 'update_scripted_scene_position(state)\n'
                                    '_draw_moving_scene_pointer(state, 237086, 5)\n'
                                    "if _ram(state, '702a').word() != 96:\n"
                                    '    return\n'
                                    "if _ram(state, '703c').word() != 20:\n"
                                    "    if _ram(state, 'f320').word() & 15 == 0:\n"
                                    "        _ram(state, '703c').set_word(0, u16(_ram(state, "
                                    "'703c').word() + 4))\n"
                                    '        _copy_scene_palette_longs(state, '
                                    '_scene_pointer(state, 237094, _ram(state, '
                                    "'703c').word()))\n"
                                    '_draw_fixed_scene_pointer(state, 237086, 4, 4)'},
 '_draw_scripted_wave': {'signature': 'state',
                         'returns': None,
                         'flow': "offset = _ram(state, '703c').word()\n"
                                 "_ram(state, '7028').set_word(0, "
                                 'state.table(238300).word(offset))\n'
                                 "_ram(state, '703c').set_word(0, u16(_ram(state, "
                                 "'703c').word() + 2))\n"
                                 "_ram(state, '703c').word()\n"
                                 "_ram(state, '702a').set_word(0, 96)\n"
                                 "if _ram(state, 'f320').word() & 3:\n"
                                 "    _ram(state, '703c').set_word(0, u16(_ram(state, "
                                 "'703c').word() - 2))\n"
                                 'else:\n'
                                 "    _ram(state, '703c').set_word(0, u16(_ram(state, "
                                 "'703c').word() + 2))\n"
                                 "    if state.table(238300).word(_ram(state, '703c').word()) "
                                 '== 255:\n'
                                 "        _ram(state, '703c').set_word(0, 0)\n"
                                 '_draw_moving_scene_pointer(state, 232836, 3)\n'
                                 "if _ram(state, '703e').word() < 120:\n"
                                 '    return\n'
                                 "if _ram(state, '7004').word() != 24:\n"
                                 "    if _ram(state, 'f320').word() & 7 == 0:\n"
                                 "        _ram(state, '7004').set_word(0, u16(_ram(state, "
                                 "'7004').word() + 4))\n"
                                 '        _copy_scene_palette_longs(state, '
                                 "_scene_pointer(state, 238342, _ram(state, '7004').word()))\n"
                                 '_draw_fixed_scene_pointer(state, 232836, 5, 4)'},
 '_draw_scripted_late_palette': {'signature': 'state',
                                 'returns': None,
                                 'flow': 'update_scripted_scene_position(state)\n'
                                         '_draw_moving_scene_pointer(state, 232844, 4)\n'
                                         "if _ram(state, '703e').word() < 120:\n"
                                         '    return\n'
                                         "if _ram(state, '703c').word() != 24:\n"
                                         "    if _ram(state, 'f320').word() & 15 == 0:\n"
                                         "        _ram(state, '703c').set_word(0, "
                                         "u16(_ram(state, '703c').word() + 4))\n"
                                         '        _copy_scene_palette_longs(state, '
                                         '_scene_pointer(state, 238514, _ram(state, '
                                         "'703c').word()))\n"
                                         '_draw_fixed_scene_pointer(state, 232844, 5, 4)'},
 '_draw_scripted_three_frame_stage': {'signature': 'state',
                                      'returns': None,
                                      'flow': "_ram(state, '7044').set_word(0, "
                                              "u16(_ram(state, '7044').word() + 1))\n"
                                              "if _ram(state, '7044').word() <= 128:\n"
                                              "    if not _ram(state, 'f321').byte() & 4:\n"
                                              "        if _ram(state, '703c').word() >= 2:\n"
                                              "            _ram(state, '703c').set_word(0, "
                                              '0)\n'
                                              '        else:\n'
                                              "            _ram(state, '703c').set_word(0, "
                                              "u16(_ram(state, '703c').word() + 1))\n"
                                              "    offset = u16(_ram(state, '703c').word() << "
                                              '2)\n'
                                              '    _draw_fixed_scene_pointer(state, 238642, '
                                              '5, offset)\n'
                                              'else:\n'
                                              '    _draw_fixed_scene_pointer(state, 238722, '
                                              '5)\n'
                                              '    update_scripted_scene_position(state)\n'
                                              '    _draw_moving_scene_pointer(state, 238722, '
                                              '4, 4)'},
 '_draw_scripted_high_mode': {'signature': 'state',
                              'returns': None,
                              'flow': "if _ram(state, '7026').word() == 28:\n"
                                      '    _draw_scripted_staged_pair(state)\n'
                                      '    return\n'
                                      "_ram(state, '7026').word()\n"
                                      "if _ram(state, '7026').word() == 30:\n"
                                      "    offset = u16((_ram(state, 'f320').word() >> 2 & 3) "
                                      '<< 5)\n'
                                      '    _copy_scene_palette_words(state, '
                                      'state.table(233688).cursor(offset))\n'
                                      "elif _ram(state, '7026').word() == 31:\n"
                                      "    offset = u16((_ram(state, 'f320').word() >> 3 & 1) "
                                      '<< 5)\n'
                                      '    _copy_scene_palette_words(state, '
                                      'state.table(233816).cursor(offset))\n'
                                      "if _ram(state, '7026').word() == 32:\n"
                                      '    _draw_scripted_wave(state)\n'
                                      "elif _ram(state, '7026').word() == 33:\n"
                                      '    _draw_scripted_late_palette(state)\n'
                                      "elif _ram(state, '7026').word() == 34:\n"
                                      '    _draw_scripted_three_frame_stage(state)\n'
                                      "elif _ram(state, '7026').word() == 35:\n"
                                      '    _draw_fixed_scene_pointer(state, 238790, 5)\n'
                                      '    _draw_fixed_scene_pointer(state, 238794, 5, '
                                      'tile=256)\n'
                                      "elif _ram(state, '7026').word() == 37:\n"
                                      '    _draw_fixed_scene_pointer(state, 238858, 5)\n'
                                      '    _draw_fixed_scene_pointer(state, 238862, 5, '
                                      'tile=256)\n'
                                      "elif _ram(state, '7026').word() == 39:\n"
                                      '    _draw_fixed_scene_pointer(state, 238898, 5)\n'
                                      "elif _ram(state, '7026').word() == 31:\n"
                                      '    _draw_fixed_scene_pointer(state, 238040, 4, 4)\n'
                                      'else:\n'
                                      '    _draw_fixed_scene_pointer(state, 238040, 5)'},
 '_draw_scripted_scene_frame': {'signature': 'state',
                                'returns': None,
                                'flow': "if _ram(state, '7026').word() < 10:\n"
                                        '    _draw_scripted_sequence(state)\n'
                                        '    return\n'
                                        "if _ram(state, '7026').word() <= 11:\n"
                                        '    update_scripted_scene_position(state)\n'
                                        "    offset = 4 if _ram(state, '7026').word() == 11 "
                                        'else 0\n'
                                        '    source = _scene_pointer(state, 236296, offset)\n'
                                        "    x, y = (_ram(state, '7028').word(), _ram(state, "
                                        "'702a').word())\n"
                                        "    tile = 0 if _ram(state, '7026').word() == 11 "
                                        'else 256\n'
                                        '    append_clipped_scene_sprites(state, source, '
                                        'SceneRenderFrame(x, y, 4, 0, tile))\n'
                                        "elif _ram(state, '7026').word() <= 19:\n"
                                        '    _draw_scripted_arrival(state)\n'
                                        "elif _ram(state, '7026').word() <= 21:\n"
                                        "    if _ram(state, '7026').word() == 20:\n"
                                        '        _draw_fixed_scene_pointer(state, 236906, 3)\n'
                                        '    else:\n'
                                        '        _draw_fixed_scene_pointer(state, 236914, 3)\n'
                                        '    update_scripted_scene_position(state)\n'
                                        "    if _ram(state, '7026').word() == 20:\n"
                                        '        _draw_moving_scene_pointer(state, 236906, 2, '
                                        '4)\n'
                                        '    else:\n'
                                        '        _draw_moving_scene_pointer(state, 236914, 2, '
                                        '4)\n'
                                        "elif _ram(state, '7026').word() <= 23:\n"
                                        '    _draw_scripted_paired_positions(state)\n'
                                        "elif _ram(state, '7026').word() <= 25:\n"
                                        '    _draw_scripted_staged_pair(state)\n'
                                        'else:\n'
                                        "    if _ram(state, '7026').word() == 27:\n"
                                        '        _draw_scripted_sequence(state)\n'
                                        '        return\n'
                                        "    if _ram(state, '7026').word() > 27:\n"
                                        '        _draw_scripted_high_mode(state)\n'
                                        '    else:\n'
                                        '        _draw_scripted_landing(state)\n'
                                        'finish_scene_sprite_chains(state)'},
 'play_scripted_scene': {'signature': 'state: SceneState',
                         'returns': 'ScenePlaybackResult',
                         'flow': 'checked_state(state)\n'
                                 'state.set_status_word(9984)\n'
                                 "_ram(state, 'f612').set_word(0, 0)\n"
                                 'clear_scene_sprite_chain_heads(state)\n'
                                 "_ram(state, '702e').set_long(0, 0)\n"
                                 "_ram(state, '703a').set_long(0, 0)\n"
                                 "for low in ('7000', '7004', '703e', '7036', '7044', "
                                 "'703c'):\n"
                                 '    _ram(state, low).set_word(0, 0)\n'
                                 "if _ram(state, '7026').word() == 24:\n"
                                 '    secondary_x, secondary_y = (96, 48)\n'
                                 "elif _ram(state, '7026').word() == 28:\n"
                                 '    secondary_x, secondary_y = (96, 48)\n'
                                 'else:\n'
                                 '    secondary_x, secondary_y = (144, 96)\n'
                                 "_ram(state, '7032').set_word(0, secondary_x)\n"
                                 "_ram(state, '7034').set_word(0, secondary_y)\n"
                                 "offset = u16(_ram(state, '7026').word() << 1)\n"
                                 'x = state.table(232328).word(offset)\n'
                                 'y = state.table(232408).word(offset)\n'
                                 "_ram(state, '7028').set_word(0, x)\n"
                                 "_ram(state, '702a').set_word(0, y)\n"
                                 "mode = _ram(state, '7026').word()\n"
                                 'movement = state.table(233040).byte(mode)\n'
                                 "_ram(state, '702c').set_byte(0, movement)\n"
                                 'video = VideoPlaneAddress(0)\n'
                                 "if _ram(state, '7026').word() == 10:\n"
                                 '    video = VideoPlaneAddress(8192)\n'
                                 "offset = u16(_ram(state, '7026').word() << 2)\n"
                                 'write_vdp_word_rle_stream(state, _scene_pointer(state, '
                                 '231354, offset), video)\n'
                                 "mode = _ram(state, '7026').word()\n"
                                 'if state.table(231834).byte(mode) == 1:\n'
                                 "    offset = u16(u16(_ram(state, '7026').word() + 1) << 2)\n"
                                 '    write_vdp_word_rle_stream(state, _scene_pointer(state, '
                                 '231354, offset), VideoPlaneAddress(8192))\n'
                                 "offset = u16(_ram(state, '7026').word() << 2)\n"
                                 '_copy_scene_palette_longs(state, _scene_pointer(state, '
                                 '231674, offset))\n'
                                 'state.set_status_word(9472)\n'
                                 'while True:\n'
                                 "    _ram(state, 'f612').set_word(0, 1536)\n"
                                 "    while _ram(state, 'f612').byte() != 0:\n"
                                 "        state.progress('scripted-scene-sound-byte')\n"
                                 "    _ram(state, '703e').set_word(0, u16(_ram(state, "
                                 "'703e').word() + 1))\n"
                                 "    offset = u16(_ram(state, '7026').word() << 1)\n"
                                 '    duration = state.table(231874).word(offset)\n'
                                 "    if duration == _ram(state, '703e').word():\n"
                                 '        return ScenePlaybackResult(offset, duration)\n'
                                 '    append_scene_marker_sprite(state, offset, duration)\n'
                                 '    _draw_scripted_scene_frame(state)'}}

def _lower_flush_scene_transfer_queue(emitter,rules):
    _SOURCE_LOWERERS['flush_scene_transfer_queue'](emitter,rules)

def _lower_write_vdp_packet_stream(emitter,rules):
    _SOURCE_LOWERERS['write_vdp_packet_stream'](emitter,rules)

def _lower_write_vdp_dictionary_repeat_stream(emitter,rules):
    _SOURCE_LOWERERS['write_vdp_dictionary_repeat_stream'](emitter,rules)

def _lower_decode_glyph_rows_to_buffers(emitter,rules):
    _SOURCE_LOWERERS['decode_glyph_rows_to_buffers'](emitter,rules)

def _lower_darken_palette(emitter,rules):
    _SOURCE_LOWERERS['darken_palette'](emitter,rules)

def _lower_darken_palette_component(emitter,rules):
    _SOURCE_LOWERERS['darken_palette_component'](emitter,rules)

def _lower_write_vdp_word_rle_stream(emitter,rules):
    _SOURCE_LOWERERS['write_vdp_word_rle_stream'](emitter,rules)

def _lower_play_scripted_scene(emitter,rules):
    _SOURCE_LOWERERS['play_scripted_scene'](emitter,rules)

def _lower_update_scripted_scene_position(emitter,rules):
    _SOURCE_LOWERERS['update_scripted_scene_position'](emitter,rules)

def _lower_initialize_scripted_secondary_position(emitter,rules):
    _SOURCE_LOWERERS['initialize_scripted_secondary_position'](emitter,rules)

def _lower_select_scene_object_frame(emitter,rules):
    _SOURCE_LOWERERS['select_scene_object_frame'](emitter,rules)

def _lower_append_clipped_scene_sprites(emitter,rules):
    _SOURCE_LOWERERS['append_clipped_scene_sprites'](emitter,rules)

def _lower_finish_scene_sprite_chains(emitter,rules):
    _SOURCE_LOWERERS['finish_scene_sprite_chains'](emitter,rules)

def _lower_finish_one_scene_sprite_chain(emitter,rules):
    _SOURCE_LOWERERS['finish_one_scene_sprite_chain'](emitter,rules)

def _lower_append_unclipped_scene_sprites(emitter,rules):
    _SOURCE_LOWERERS['append_unclipped_scene_sprites'](emitter,rules)

def _lower_advance_scene_palette_fade(emitter,rules):
    _SOURCE_LOWERERS['advance_scene_palette_fade'](emitter,rules)

def _lower_fade_palette_component(emitter,rules):
    _SOURCE_LOWERERS['fade_palette_component'](emitter,rules)

def _lower_begin_scene_palette_darken(emitter,rules):
    _SOURCE_LOWERERS['begin_scene_palette_darken'](emitter,rules)

def _lower_snapshot_and_clear_scene_palette(emitter,rules):
    _SOURCE_LOWERERS['snapshot_and_clear_scene_palette'](emitter,rules)

def _lower_read_vdp_plane_rle_rows(emitter,rules):
    _SOURCE_LOWERERS['read_vdp_plane_rle_rows'](emitter,rules)

def _lower_write_vdp_swapped_byte_rle_stream(emitter,rules):
    _SOURCE_LOWERERS['write_vdp_swapped_byte_rle_stream'](emitter,rules)

def _lower_copy_scene_palette_variant(emitter,rules):
    _SOURCE_LOWERERS['copy_scene_palette_variant'](emitter,rules)

def _lower_finish_actor_sprite_chains(emitter,rules):
    _SOURCE_LOWERERS['finish_actor_sprite_chains'](emitter,rules)

def _lower_finish_one_actor_sprite_chain(emitter,rules):
    _SOURCE_LOWERERS['finish_one_actor_sprite_chain'](emitter,rules)

def _lower_set_vram_write_address(emitter,rules):
    _SOURCE_LOWERERS['set_vram_write_address'](emitter,rules)

def _lower_sample_random_preserving_seed_carrier(emitter,rules):
    _SOURCE_LOWERERS['sample_random_preserving_seed_carrier'](emitter,rules)

LOWERERS={
    'flush_scene_transfer_queue':_lower_flush_scene_transfer_queue,
    'write_vdp_packet_stream':_lower_write_vdp_packet_stream,
    'write_vdp_dictionary_repeat_stream':_lower_write_vdp_dictionary_repeat_stream,
    'decode_glyph_rows_to_buffers':_lower_decode_glyph_rows_to_buffers,
    'darken_palette':_lower_darken_palette,
    'darken_palette_component':_lower_darken_palette_component,
    'write_vdp_word_rle_stream':_lower_write_vdp_word_rle_stream,
    'play_scripted_scene':_lower_play_scripted_scene,
    'update_scripted_scene_position':_lower_update_scripted_scene_position,
    'initialize_scripted_secondary_position':_lower_initialize_scripted_secondary_position,
    'select_scene_object_frame':_lower_select_scene_object_frame,
    'append_clipped_scene_sprites':_lower_append_clipped_scene_sprites,
    'finish_scene_sprite_chains':_lower_finish_scene_sprite_chains,
    'finish_one_scene_sprite_chain':_lower_finish_one_scene_sprite_chain,
    'append_unclipped_scene_sprites':_lower_append_unclipped_scene_sprites,
    'advance_scene_palette_fade':_lower_advance_scene_palette_fade,
    'fade_palette_component':_lower_fade_palette_component,
    'begin_scene_palette_darken':_lower_begin_scene_palette_darken,
    'snapshot_and_clear_scene_palette':_lower_snapshot_and_clear_scene_palette,
    'read_vdp_plane_rle_rows':_lower_read_vdp_plane_rle_rows,
    'write_vdp_swapped_byte_rle_stream':_lower_write_vdp_swapped_byte_rle_stream,
    'copy_scene_palette_variant':_lower_copy_scene_palette_variant,
    'finish_actor_sprite_chains':_lower_finish_actor_sprite_chains,
    'finish_one_actor_sprite_chain':_lower_finish_one_actor_sprite_chain,
    'set_vram_write_address':_lower_set_vram_write_address,
    'sample_random_preserving_seed_carrier':_lower_sample_random_preserving_seed_carrier,
}

# Complete supplied initialization contracts; finite host admission, not general Python lowering.
# Original physical emitters and default instruction topology remain unchanged.
HOST_INITIALIZATION_DECLARATIONS = {'flush_scene_transfer_queue': {'signature': 'state: SceneState, values: PacketTransferValues | None=None',
                                'returns': 'VdpPacketResult | None',
                                'flow': 'checked_state(state)\n'
                                        'if values is not None:\n'
                                        '    if type(values) is not PacketTransferValues:\n'
                                        "        raise ValueError('actual packet flush values required')\n"
                                        '    values.validate()\n'
                                        'result = None\n'
                                        "if _ram(state, 'd100').word() != 0:\n"
                                        '    result = write_vdp_packet_stream(state, _ram(state, '
                                        "'d100').cursor(), values)\n"
                                        "_ram(state, 'f31a').set_word(0, 0)\n"
                                        "_ram(state, 'd100').set_word(0, 0)\n"
                                        'return result'},
 'write_vdp_packet_stream': {'signature': 'state: SceneState, source: Cursor, values: PacketTransferValues | '
                                          'None=None',
                             'returns': 'VdpPacketResult',
                             'flow': 'checked_state(state)\n'
                                     'checked_cursor(source, state)\n'
                                     'if values is not None:\n'
                                     '    if type(values) is not PacketTransferValues:\n'
                                     "        raise ValueError('actual packet stream values required')\n"
                                     '    values.validate()\n'
                                     '    count_carrier, increment_carrier = (values.command, '
                                     'values.increment)\n'
                                     '    spill_carrier = values.spill\n'
                                     'command = 0\n'
                                     'while True:\n'
                                     '    increment = 36610\n'
                                     '    count = source.next_word()\n'
                                     '    if count == 0:\n'
                                     '        state.write(12582916, 2, increment)\n'
                                     '        actual = None\n'
                                     '        if values is not None:\n'
                                     '            actual = PacketTransferValues(replace_word(count_carrier, '
                                     '0), replace_word(increment_carrier, increment), values.address, '
                                     'spill_carrier).validate()\n'
                                     '        return VdpPacketResult(source, command, increment, actual)\n'
                                     '    if negative_word(count):\n'
                                     '        increment = 36736\n'
                                     '        count &= 32767\n'
                                     '        address = source.next_word()\n'
                                     '        total = u16(((address & 8191) >> 7) + count)\n'
                                     '        spill = u16(total - 64) if total >= 64 else 0\n'
                                     '        count = u16(count - spill)\n'
                                     '    else:\n'
                                     '        address = source.next_word()\n'
                                     '        spill = 0\n'
                                     '        if not count & 16384:\n'
                                     '            total = u16(((address & 127) >> 1) + count)\n'
                                     '            spill = u16(total - 64) if total >= 64 else 0\n'
                                     '            count = u16(count - spill)\n'
                                     '    count = u16((count & 49151) - 1)\n'
                                     '    state.write(12582916, 2, increment)\n'
                                     '    command = u32(address << 2)\n'
                                     '    command = replace_word(command, low16(command) >> 2 | 16384)\n'
                                     '    command = swap_words(command)\n'
                                     '    state.write(12582916, 4, command)\n'
                                     '    if values is not None:\n'
                                     '        spill_carrier = replace_word(spill_carrier, spill)\n'
                                     '    _write_word_count(state, source, count)\n'
                                     '    if spill != 0:\n'
                                     '        command &= 4286644223 if increment & 2 else 3766484991\n'
                                     '        spill = u16(spill - 1)\n'
                                     '        state.write(12582916, 4, command)\n'
                                     '        _write_word_count(state, source, spill)\n'
                                     '        if values is not None:\n'
                                     '            spill_carrier = replace_word(spill_carrier, 65535)\n'
                                     '    if values is not None:\n'
                                     '        values = PacketTransferValues(count_carrier, '
                                     'increment_carrier, command, spill_carrier)'},
 'decode_glyph_rows_to_buffers': {'signature': 'state: SceneState, source: Cursor, destination: Cursor, '
                                               'background: Long, foreground: Long, remaining: Long, saved: '
                                               'GlyphSavedValues | None=None',
                                  'returns': 'GlyphRowsResult',
                                  'flow': 'from .business_reuse import expand_glyph_row, _save_glyph_values, '
                                          '_restore_glyph_values\n'
                                          'checked_state(state)\n'
                                          'checked_cursor(source, state)\n'
                                          'checked_cursor(destination, state)\n'
                                          'uint(background, 32)\n'
                                          'uint(foreground, 32)\n'
                                          'uint(remaining, 32)\n'
                                          'if saved is not None:\n'
                                          '    _save_glyph_values(state, saved, True)\n'
                                          'for _ in descending_inclusive(low16(remaining)):\n'
                                          '    token = source.next_word()\n'
                                          '    if not negative_word(token):\n'
                                          '        offset = u16((token & 65280) << 3) | u16((token & 255) << '
                                          '5)\n'
                                          '        glyph = state.table(529820).advance(offset).cursor()\n'
                                          '        for _ in range(16):\n'
                                          '            destination.set_long(0, expand_glyph_row(state, '
                                          'glyph, low8(background), low8(foreground)))\n'
                                          '            destination.set_long(0, expand_glyph_row(state, '
                                          'glyph, low8(background), low8(foreground)), 64)\n'
                                          '            destination.base = u32(destination.base + 4)\n'
                                          '    else:\n'
                                          '        background_pixels, foreground_pixels = (0, 0)\n'
                                          '        for _ in range(8):\n'
                                          '            background_pixels = u32(background_pixels << 4) | '
                                          'low16(background)\n'
                                          '            foreground_pixels = u32(foreground_pixels << 4) | '
                                          'low16(foreground)\n'
                                          '        for _ in range(16):\n'
                                          '            destination.set_long(0, background_pixels, 64)\n'
                                          '            destination.append_long(background_pixels)\n'
                                          '        destination.set_long(0, foreground_pixels, -36)\n'
                                          '        destination.set_long(0, foreground_pixels, 28)\n'
                                          '    destination.base = u32(destination.base + 64)\n'
                                          'if saved is not None:\n'
                                          '    saved = _restore_glyph_values(state, saved, '
                                          'saved.glyph_source, True)\n'
                                          'return GlyphRowsResult(source, destination, '
                                          'replace_word(remaining, 65535), background, foreground, saved)'},
 'darken_palette': {'signature': 'state: SceneState, shade: Long, count: Word, source: Cursor, accumulator: '
                                 'Long=0, *, count_carrier: Long | None=None, color: Long=0, component: '
                                 'Long=0',
                    'returns': 'PaletteTransformResult',
                    'flow': 'checked_state(state)\n'
                            'checked_cursor(source, state)\n'
                            'uint(shade, 32)\n'
                            'uint(count, 16)\n'
                            'uint(accumulator, 32)\n'
                            'uint(color, 32)\n'
                            'uint(component, 32)\n'
                            'if count_carrier is not None:\n'
                            '    uint(count_carrier, 32)\n'
                            '    if low16(count_carrier) != count:\n'
                            "        raise ValueError('palette count must agree with actual caller')\n"
                            'if low16(shade) > 15:\n'
                            "    raise Boundary('original DEAC nonprogressing branch for shade WORD >15')\n"
                            "destination = _ram(state, 'fb00').cursor()\n"
                            'if shade & 1:\n'
                            "    if _ram(state, 'f320').byte() & 1:\n"
                            '        shade = replace_word(shade, u16(low16(shade) + 1))\n'
                            'shade &= 4294967294\n'
                            'accumulator = replace_word(accumulator, 0)\n'
                            'for _ in descending_inclusive(count):\n'
                            '    color = replace_word(color, u16(source.next_word() << 4))\n'
                            '    for _ in range(3):\n'
                            '        result = darken_palette_component(state, shade, color, accumulator, '
                            'component)\n'
                            '        color, accumulator, component = (result.color, result.accumulated, '
                            'result.component)\n'
                            '    destination.append_word(low16(accumulator))\n'
                            "_ram(state, 'f31e').set_word(0, u16(_ram(state, 'f31e').word() + 1))\n"
                            "shade = replace_word(shade, _ram(state, 'fb00').word())\n"
                            "_ram(state, 'fb20').set_word(0, low16(shade))\n"
                            "_ram(state, 'fb40').set_word(0, low16(shade))\n"
                            "_ram(state, 'fb60').set_word(0, low16(shade))\n"
                            'if count_carrier is not None:\n'
                            '    count_carrier = replace_word(count_carrier, 65535)\n'
                            'return PaletteTransformResult(source, destination, shade, accumulator, '
                            'count_carrier, color, component)'}}
# The earlier host delta is consolidated into DECLARATIONS above.
APPROVED.setdefault('business_reuse', set()).update({'_restore_glyph_values', '_save_glyph_values'})
APPROVED.setdefault('contexts_reuse', set()).update({'GlyphSavedValues'})
APPROVED.setdefault('contexts_scene', set()).update({'PacketTransferValues'})

HOST_SWAPPED_RLE_DECLARATIONS = {
    '_write_vdp_swapped_byte_rle_core': {
        'signature': 'state: SceneState, source: Cursor, video_address: VideoPlaneAddress',
        'returns': 'SwappedByteRleObservation',
        'flow': '''checked_state(state)
checked_cursor(source, state)
_video_address(video_address)
state.write(0xC00004, 2, 0x8F02)
command = set_vram_write_address(state, video_address)
marker = source.next_byte()
last_word = None
while True:
    low = source.next_byte()
    if marker != low:
        last_word = source.next_byte() << 8 | low
        state.write(0xC00000, 2, last_word)
    else:
        count = source.next_byte()
        if count == 0:
            return SwappedByteRleObservation(source, video_address,
                command, marker, low, last_word)
        low = source.next_byte()
        last_word = source.next_byte() << 8 | low
        for _ in descending_inclusive(count):
            state.write(0xC00000, 2, last_word)''',
    },
    'write_vdp_swapped_byte_rle_stream': {
        'signature': 'state: SceneState, source: Cursor, video_address: VideoPlaneAddress',
        'returns': 'VdpStreamResult',
        'flow': '''actual = _write_vdp_swapped_byte_rle_core(state, source, video_address)
return VdpStreamResult(actual.source, actual.video_address, actual.command_carrier)''',
    },
    'write_vdp_swapped_byte_rle_stream_complete': {
        'signature': 'state: SceneState, source: Cursor, video_address: VideoPlaneAddress, retained: SwappedByteRleRetained',
        'returns': 'SwappedByteRleResult',
        'flow': '''checked_state(state)
checked_cursor(source, state)
_video_address(video_address)
if type(retained) is not SwappedByteRleRetained:
    raise ValueError('actual D1/D2/D4 partial-write values required')
retained.validate()
actual = _write_vdp_swapped_byte_rle_core(state, source, video_address)
packed_word = retained.packed_word
if actual.last_word is not None:
    packed_word = replace_word(packed_word, actual.last_word)
return SwappedByteRleResult(actual.source, actual.video_address,
    actual.command_carrier, replace_byte(retained.marker, actual.marker),
    replace_byte(retained.token, actual.token), 0, packed_word,
    actual.last_word, False, True, False, False)''',
    },
}
# All three supplied bodies participate in finite admission. They share the
# original single physical lowerer; this adds no target allocation or general
# Python edit support, and never falls back to an old body at runtime.
# The earlier host delta is consolidated into DECLARATIONS above.
APPROVED.setdefault('contexts_scene', set()).update({
    'SwappedByteRleRetained', 'SwappedByteRleObservation', 'SwappedByteRleResult'})

# Finite full-body contracts: every supplied core/wrapper effect is admitted.
# These are offline declarations, not a runtime source fallback or old body.
HOST_PALETTE_RETURN_DECLARATIONS = {"copy_scene_palette_variant": {"signature": "state: SceneState, variant: Long",
 "returns": "PaletteCopyResult",
 "flow": "fields = _copy_scene_palette_variant_fields(state, variant, None)\nreturn PaletteCopyResult(fields.index_carrier, fields.source, fields.destination, fields.directory).validate(state)"},
 "_copy_scene_palette_variant_fields": {"signature": "state: SceneState, variant: Long, count_carrier: Long | None",
 "returns": "PaletteCopyFields",
 "flow": "checked_state(state)\nuint(variant, 32)\nif count_carrier is not None:\n    uint(count_carrier, 32)\nvariant = _word_shift(variant, 3)\ndirectory = state.table(240556).advance(s16(low16(variant))).cursor()\nsource = state.table(directory.next_long()).cursor()\ndestination = state.table(u32(s16(directory.next_word()))).cursor()\ncount = directory.next_word()\nfor _ in descending_inclusive(count):\n    last_color_pair = source.next_long()\n    destination.append_long(last_color_pair)\nif count_carrier is not None:\n    count_carrier = replace_word(count_carrier, 65535)\nreturn PaletteCopyFields(variant, source, destination, directory, count_carrier, last_color_pair).validate(state)"},
 "copy_scene_palette_variant_complete": {"signature": "state: SceneState, variant: Long, count_carrier: Long",
 "returns": "PaletteCopyCompleteResult",
 "flow": "uint(count_carrier, 32)\nfields = _copy_scene_palette_variant_fields(state, variant, count_carrier)\nreturn PaletteCopyCompleteResult(fields.index_carrier, fields.source, fields.destination, fields.directory, fields.count_carrier, False, fields.last_color_pair == 0, bool(fields.last_color_pair & 2147483648), False).validate(state)"}}
# The earlier host delta is consolidated into DECLARATIONS above.
APPROVED.setdefault('contexts_scene', set()).update({'PaletteCopyFields', 'PaletteCopyCompleteResult'})

def compile_scene(source):
    records, policy = admit_policy_source(source, DECLARATIONS, APPROVED, role_specs=ROLE_SPECS, rule_builders=(owner_rules,), bindings=SCENE_BINDINGS, grammar='scene-policy-path-roles-v1')
    if set(policy['owner_rules']) != {binding.name for binding in SCENE_BINDINGS}:
        raise CompileError('the complete scene family needs one policy authority per owner')
    actual_player_fields = {name: records[name]['effects'] for name in ('_append_scene_sprite_fields', '_copy_scene_palette_longs_fields', '_draw_scripted_scene_frame_fields', '_play_scripted_scene_core', '_scene_render_apply_delta', '_scene_render_arithmetic', '_scene_render_asl_word', '_scene_render_bit', '_scene_render_call_fields', '_scene_render_clip_axis', '_scene_render_compare', '_scene_render_push_longs', '_scene_render_restore_clip', '_scene_render_restore_sprite', '_scene_render_save_clip', 'append_clipped_scene_sprites_fields', 'append_scene_marker_sprite_fields', 'append_unclipped_scene_sprites_fields', 'clear_scene_sprite_chain_heads_fields', 'finish_one_scene_sprite_chain_fields', 'finish_scene_sprite_chains_fields', 'play_scripted_scene_fields', 'set_vram_write_address_fields', 'update_scripted_scene_position_fields', 'write_vdp_word_rle_stream_fields')}
    for owner in ('play_scripted_scene', 'write_vdp_word_rle_stream', 'set_vram_write_address', 'finish_scene_sprite_chains', 'finish_one_scene_sprite_chain', 'append_clipped_scene_sprites', 'append_unclipped_scene_sprites', 'update_scripted_scene_position'):
        records[owner]['effects'] = dict(legacy_projection=records[owner]['effects'], sole_player_fields=actual_player_fields)
    records['play_scripted_scene']['effects'] = dict(previous_fields=records['play_scripted_scene']['effects'], sole_mode_fields={name: records[name]['effects'] for name in ('_copy_scene_palette_words_fields', '_draw_scripted_arrival_fields', '_draw_scripted_high_mode_fields', '_draw_scripted_landing_fields', '_draw_scripted_late_palette_fields', '_draw_scripted_scene_frame_fields', '_draw_scripted_sequence_fields', '_draw_scripted_three_frame_stage_fields', '_draw_scripted_two_layer_fields', '_draw_scripted_wave_fields', '_scene_mode_adjust_word', '_scene_mode_compare', '_scene_mode_lsr_word', '_scene_mode_packet_parameters', '_scene_mode_push_word', '_scene_mode_restore_longs', '_scene_mode_restore_word', '_scene_render_call_fields')})
    actual_pair_fields = {name: records[name]['effects'] for name in ('_draw_scripted_high_mode_fields', '_draw_scripted_paired_positions_fields', '_draw_scripted_scene_frame_fields', '_draw_scripted_staged_pair_fields', '_scene_render_call_fields', 'initialize_scripted_secondary_position_fields', 'select_scene_object_frame_fields')}
    for owner in ('play_scripted_scene', 'initialize_scripted_secondary_position', 'select_scene_object_frame'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'], sole_pair_fields=actual_pair_fields)
    sole_glyph_fields = {name: records[name]['effects'] for name in ('_glyph_restore_fields', '_glyph_row_call_fields', '_glyph_save_fields', '_glyph_shift_long_fields', 'decode_glyph_rows_to_buffers_fields', 'expand_glyph_row_fields', 'expand_glyph_stream_fields')}
    for owner in ('decode_glyph_rows_to_buffers',):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'], sole_glyph_fields=sole_glyph_fields)
    records['write_vdp_dictionary_repeat_stream']['effects'] = dict(legacy_projection=records['write_vdp_dictionary_repeat_stream']['effects'], sole_dictionary_fields={name: records[name]['effects'] for name in ('_dictionary_stream_take_fields', '_dictionary_stream_finished_fields', 'write_vdp_dictionary_repeat_stream_fields')})
    sole_live_packet_fields = {name: records[name]['effects'] for name in ('_vdp_packet_spill_fields', '_write_vdp_packet_run_fields', 'write_vdp_packet_stream_fields')}
    for owner in ('write_vdp_packet_stream',):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'], sole_live_packet_fields=sole_live_packet_fields)
    sole_tile_plane_fields = {name: records[name]['effects'] for name in ('_scene_tile_byte_fields', '_write_vdp_swapped_byte_rle_fields_core', 'write_vdp_swapped_byte_rle_stream_fields', 'advance_plane_row_fields', '_scene_plane_row_call_fields', '_read_vdp_plane_rle_rows_fields_core', 'read_vdp_plane_rle_rows_fields', '_scene_render_call_fields', 'read_vdp_plane_rle_rows_from_control_fields', 'read_vdp_plane_rle_rows_from_literal_fields')}
    for owner in ('read_vdp_plane_rle_rows', 'write_vdp_swapped_byte_rle_stream'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'], sole_tile_plane_fields=sole_tile_plane_fields)
    sole_scene_palette_fields = {name: records[name]['effects'] for name in ('_copy_scene_palette_variant_fields_core', 'copy_scene_palette_variant_fields', '_copy_scene_palette_variant_fields', '_begin_scene_palette_darken_fields_core', 'begin_scene_palette_darken_fields', 'snapshot_and_clear_scene_palette_fields')}
    for owner in ('copy_scene_palette_variant', 'begin_scene_palette_darken', 'snapshot_and_clear_scene_palette'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'], sole_scene_palette_fields=sole_scene_palette_fields)
    sole_darken_fields = {name: records[name]['effects'] for name in ('darken_palette_component_fields', '_darken_palette_component_call_fields', 'darken_palette_fields')}
    for owner in ('darken_palette', 'darken_palette_component'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'], sole_darken_fields=sole_darken_fields)
    sole_scene_preserving_random_fields = {name: records[name]['effects'] for name in ('sample_random_preserving_seed_fields',)}
    for owner in ('sample_random_preserving_seed_carrier',):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'], sole_scene_preserving_random_fields=sole_scene_preserving_random_fields)
    sole_actor_chain_fields = {name: records[name]['effects'] for name in ('finish_actor_sprite_chains_fields', 'finish_one_actor_sprite_chain_fields')}
    for owner in ('finish_actor_sprite_chains', 'finish_one_actor_sprite_chain'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'], sole_actor_chain_fields=sole_actor_chain_fields)
    sole_palette_fade_fields = {name: records[name]['effects'] for name in ('_scene_fade_rotate_word_fields', 'advance_scene_palette_fade_fields', 'fade_palette_component_fields')}
    for owner in ('advance_scene_palette_fade', 'fade_palette_component'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'], sole_palette_fade_fields=sole_palette_fade_fields)
    records['flush_scene_transfer_queue']['effects'] = dict(previous_fields=records['flush_scene_transfer_queue']['effects'], sole_queue_fields=records['flush_scene_transfer_queue_fields']['effects'])
    compiled = lower_declared(records, SCENE_BINDINGS, LOWERERS)
    compiled['source_policy'] = policy
    return compiled

# B20 true same-state player/streams/packet fields; ordinary lowering unchanged.
APPROVED.setdefault('contexts_scene',set()).update({'_first_long', '_scene_refresh_decrement', 'SceneRefreshBoundary', 'SceneRefreshMemory', '_movement_compare', 'FirstDeploymentFrame', '_first_shift_word', '_scene_refresh_emit', '_movement_binary_flags', '_first_word', '_first_byte', '_scene_refresh_flags', 'first_replace'})
DECLARATIONS.pop('_apply_sprite_delta')
DECLARATIONS.update({'_append_scene_sprite_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                              'clipped: bool',
                                 'returns': 'FirstDeploymentFrame',
                                 'flow': 'memory.frame(frame)\n'
                                         'if type(clipped) is not bool:\n'
                                         "    raise ValueError('actual scene clipping entry required')\n"
                                         'if frame.stack_cursor is not None:\n'
                                         '    frame = _scene_render_push_longs(memory, frame, '
                                         '(frame.candidates.base, frame.offset_y, frame.offset_x))\n'
                                         'original = frame\n'
                                         'count = memory.state.read(4294963968, 1)\n'
                                         'frame = _scene_render_compare(memory, frame, count, 128, 8)\n'
                                         'if count >= 128:\n'
                                         '    return memory.sync_status(_scene_render_restore_sprite(memory, '
                                         'frame))\n'
                                         "frame = _first_long(frame, 'distance', frame.distance & 65535)\n"
                                         "frame = _first_word(frame, 'choice', low16(frame.unit))\n"
                                         "frame = _first_word(frame, 'unit', low16(frame.unit) & 65528)\n"
                                         "frame = _first_word(frame, 'choice', low16(frame.choice) & 7 if "
                                         'frame.choice is not None else low16(original.unit) & 7)\n'
                                         'layer = (low16(original.unit) & 7) << 2\n'
                                         "frame = _scene_render_asl_word(memory, frame, 'choice', "
                                         'low16(original.unit) & 7, 2)\n'
                                         "frame = _scene_render_arithmetic(memory, frame, 'target_x', "
                                         'low16(frame.target_x), 128, 16)\n'
                                         'if frame.target_x & 32768:\n'
                                         '    return memory.sync_status(_scene_render_restore_sprite(memory, '
                                         'frame))\n'
                                         'frame = _scene_render_bit(memory, frame, frame.unit, 32)\n'
                                         'if frame.unit & 32:\n'
                                         "    frame = _scene_render_arithmetic(memory, frame, 'target_x', "
                                         'low16(frame.target_x), 8, 16, True)\n'
                                         "frame = _scene_render_arithmetic(memory, frame, 'target_y', "
                                         'low16(frame.target_y), 128, 16)\n'
                                         'frame = _scene_render_bit(memory, frame, frame.unit, 16)\n'
                                         'if frame.unit & 16:\n'
                                         "    frame = _scene_render_arithmetic(memory, frame, 'target_y', "
                                         'low16(frame.target_y), 8, 16, True)\n'
                                         "frame = _first_word(frame, 'offset_x', 0)\n"
                                         'count = memory.state.read(4294963968, 1)\n'
                                         "frame = _first_byte(frame, 'offset_x', count)\n"
                                         "frame = _first_shift_word(frame, 'offset_x', count, 3)\n"
                                         'frame = first_replace(frame, '
                                         'candidates=memory.cursor_at(4294965248, count << 3), '
                                         'controller=memory.cursor_at(16740358))\n'
                                         "frame = _first_word(frame, 'offset_y', low16(frame.target_x))\n"
                                         'extent_word = low16(frame.target_x)\n'
                                         'while True:\n'
                                         '    if clipped:\n'
                                         '        frame = _scene_refresh_emit(memory, frame, 16740400, 2, '
                                         '0)\n'
                                         "    frame = _first_long(frame, 'offset_x', 0)\n"
                                         '    horizontal = frame.roster.byte()\n'
                                         "    frame = _first_byte(frame, 'offset_x', horizontal)\n"
                                         '    frame = _scene_render_compare(memory, frame, horizontal, 128, '
                                         '8)\n'
                                         '    if horizontal == 128:\n'
                                         '        break\n'
                                         '    rejected = False\n'
                                         '    if clipped:\n'
                                         '        frame, rejected = _scene_render_clip_axis(memory, frame, '
                                         '16740392, 112)\n'
                                         '    if not rejected:\n'
                                         '        extent = extent_word if frame.offset_y is None else '
                                         'low16(frame.offset_y)\n'
                                         '        frame, coordinate = _scene_render_apply_delta(memory, '
                                         'frame, 32, extent)\n'
                                         '        extent_word = coordinate\n'
                                         '        frame = _scene_refresh_emit(memory, frame, '
                                         'frame.candidates.base, 2, coordinate)\n'
                                         "        frame = _first_word(frame, 'offset_y', "
                                         'low16(frame.target_y))\n'
                                         '        extent_word = low16(frame.target_y)\n'
                                         "        frame = _first_byte(frame, 'offset_x', "
                                         'frame.roster.byte(0, 3))\n'
                                         '        if clipped:\n'
                                         '            frame = _scene_refresh_emit(memory, frame, 16740400, '
                                         '2, 0)\n'
                                         '            frame, rejected = _scene_render_clip_axis(memory, '
                                         'frame, 16740394, 160)\n'
                                         '        if not rejected:\n'
                                         '            extent = extent_word if frame.offset_y is None else '
                                         'low16(frame.offset_y)\n'
                                         '            frame, coordinate = _scene_render_apply_delta(memory, '
                                         'frame, 16, extent)\n'
                                         '            extent_word = coordinate\n'
                                         '            frame = _scene_refresh_emit(memory, frame, '
                                         'frame.candidates.base + 6, 2, coordinate)\n'
                                         '            frame = _scene_refresh_emit(memory, frame, '
                                         'frame.candidates.base + 2, 1, frame.roster.byte(0, 1))\n'
                                         '            if frame.choice is not None:\n'
                                         '                layer = low16(frame.choice)\n'
                                         '            value = frame.controller.long(layer)\n'
                                         '            frame = _scene_refresh_flags(memory, frame, value, 4)\n'
                                         '            if value == 0:\n'
                                         '                frame = _scene_refresh_emit(memory, frame, '
                                         'frame.controller.base + s16(layer), 4, frame.candidates.base)\n'
                                         '                frame = _scene_refresh_emit(memory, frame, '
                                         'frame.controller.base + s16(layer) + 32, 1, '
                                         'memory.state.read(4294963968, 1))\n'
                                         '            else:\n'
                                         '                frame = first_replace(frame, '
                                         'scan=memory.cursor_at(frame.controller.long(layer, 64)))\n'
                                         '                frame = _scene_refresh_emit(memory, frame, '
                                         'frame.scan.base + 3, 1, memory.state.read(4294963968, 1))\n'
                                         '            frame = _scene_refresh_emit(memory, frame, '
                                         'frame.controller.base + s16(layer) + 64, 4, '
                                         'frame.candidates.base)\n'
                                         '            count = memory.state.read(4294963968, 1)\n'
                                         '            frame, new_count = '
                                         '_movement_binary_flags(memory.state, frame, count, 1, 8)\n'
                                         '            memory.state.write(4294963968, 1, new_count)\n'
                                         "            frame = _first_byte(frame, 'offset_x', "
                                         'frame.roster.byte(0, 1))\n'
                                         '            encoded = low16(frame.offset_x) & 240\n'
                                         "            frame = _first_word(frame, 'offset_x', encoded)\n"
                                         '            frame = _scene_render_arithmetic(memory, frame, '
                                         "'offset_x', low8(frame.offset_x), low8(frame.count), 8)\n"
                                         "            frame = _first_word(frame, 'offset_x', "
                                         'low16(frame.offset_x) ^ low16(frame.unit))\n'
                                         '            frame = _scene_render_asl_word(memory, frame, '
                                         "'offset_x', low16(frame.offset_x), 7)\n"
                                         "            frame = _first_byte(frame, 'offset_x', "
                                         'low8(frame.offset_x) | frame.roster.byte(0, 2))\n'
                                         '            frame = _scene_render_arithmetic(memory, frame, '
                                         "'offset_x', low16(frame.offset_x), low16(frame.distance), 16)\n"
                                         '            frame = _scene_refresh_emit(memory, frame, '
                                         'frame.candidates.base + 4, 2, low16(frame.offset_x))\n'
                                         '            frame = first_replace(frame, '
                                         'candidates=frame.candidates.advance(8))\n'
                                         '    frame = first_replace(frame, roster=frame.roster.advance(4))\n'
                                         '    count = memory.state.read(4294963968, 1)\n'
                                         '    frame = _scene_render_compare(memory, frame, count, 128, 8)\n'
                                         '    if count >= 128:\n'
                                         '        break\n'
                                         'if frame.stack_cursor is not None:\n'
                                         '    frame = _scene_render_restore_sprite(memory, frame)\n'
                                         'else:\n'
                                         '    frame = first_replace(frame, offset_x=original.offset_x, '
                                         'offset_y=original.offset_y, candidates=original.candidates)\n'
                                         'return memory.sync_status(frame)'},
 '_append_scene_sprites': {'signature': 'state, source, frame, clipped',
                           'returns': None,
                           'flow': 'checked_state(state)\n'
                                   'checked_cursor(source, state)\n'
                                   'if type(frame) is not SceneRenderFrame:\n'
                                   "    raise ValueError('explicit scene render operands required')\n"
                                   'frame.validate(state)\n'
                                   'partial = first_replace(FirstDeploymentFrame.unobserved(), '
                                   'target_x=frame.x, target_y=frame.y, unit=frame.attributes, '
                                   'count=frame.palette, distance=frame.tile, roster=source.advance(0))\n'
                                   'actual = _append_scene_sprite_fields(SceneRefreshMemory(state), partial, '
                                   'clipped)\n'
                                   'source.base = actual.roster.base\n'
                                   'return SpriteBatchResult(source, SceneRenderFrame(actual.target_x, '
                                   'actual.target_y, actual.unit, actual.count, actual.distance))'},
 '_copy_scene_palette_longs': {'signature': 'state, source',
                               'returns': None,
                               'flow': 'partial = first_replace(FirstDeploymentFrame.unobserved(), '
                                       'roster=source.advance(0))\n'
                                       'actual = _copy_scene_palette_longs_fields(SceneRefreshMemory(state), '
                                       'partial)\n'
                                       'source.base = actual.roster.base'},
 '_copy_scene_palette_longs_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                      'returns': 'FirstDeploymentFrame',
                                      'flow': 'memory.frame(frame)\n'
                                              'frame = first_replace(frame, '
                                              'candidates=memory.cursor_at(4294966016))\n'
                                              'count = 8\n'
                                              "frame = _first_long(frame, 'target_x', count - 1)\n"
                                              'for index in range(count):\n'
                                              '    value = frame.roster.long()\n'
                                              '    source = frame.roster.advance(4)\n'
                                              '    destination = frame.candidates\n'
                                              '    frame = first_replace(frame, roster=source, '
                                              'candidates=destination.advance(4))\n'
                                              '    frame = _scene_refresh_emit(memory, frame, '
                                              'destination.base, 4, value)\n'
                                              "    frame = _scene_refresh_decrement(frame, 'target_x', count "
                                              '- 1 - index)\n'
                                              'return frame'},
 '_draw_scripted_scene_frame_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': "frame = _first_long(frame, 'target_x', 0)\n"
                                               'mode = memory.state.read(16740390, 2)\n'
                                               'frame = _scene_render_compare(memory, frame, mode, 10, 16)\n'
                                               'if mode < 10:\n'
                                               '    raise SceneRefreshBoundary(235534, frame, None)\n'
                                               'mode = memory.state.read(16740390, 2)\n'
                                               'frame = _scene_render_compare(memory, frame, mode, 11, 16)\n'
                                               'if mode > 11:\n'
                                               '    raise SceneRefreshBoundary(236304, frame, None)\n'
                                               'frame = _scene_render_call_fields(memory, frame, 235992, '
                                               '236214)\n'
                                               'mode = memory.state.read(16740390, 2)\n'
                                               'frame = _scene_render_compare(memory, frame, mode, 11, 16)\n'
                                               'selected = 1 if mode == 11 else 0\n'
                                               "frame = _first_long(frame, 'target_y', selected)\n"
                                               "frame = _scene_render_asl_word(memory, frame, 'target_y', "
                                               'selected, 2)\n'
                                               'frame = first_replace(frame, '
                                               'roster=memory.cursor_at(memory.state.table_at(236296).long(selected '
                                               '<< 2)))\n'
                                               "frame = _first_word(frame, 'target_x', "
                                               'memory.state.read(16740392, 2))\n'
                                               "frame = _first_word(frame, 'target_y', "
                                               'memory.state.read(16740394, 2))\n'
                                               "frame = _first_long(frame, 'unit', 4)\n"
                                               "frame = _first_long(frame, 'count', 0)\n"
                                               'mode = memory.state.read(16740390, 2)\n'
                                               'frame = _scene_render_compare(memory, frame, mode, 11, 16)\n'
                                               "frame = _first_long(frame, 'distance', 0 if mode == 11 else "
                                               '256)\n'
                                               'frame = _scene_render_call_fields(memory, frame, 239008, '
                                               '236284)\n'
                                               'return _scene_render_call_fields(memory, frame, 239438, '
                                               '236290)'},
 '_play_scripted_scene_core': {'signature': 'state: SceneState, frame: FirstDeploymentFrame',
                               'returns': 'FirstDeploymentFrame',
                               'flow': 'memory = SceneRefreshMemory(state)\n'
                                       'memory.frame(frame)\n'
                                       'frame = memory.status_word(frame, 9984)\n'
                                       'frame = _scene_refresh_emit(memory, frame, 4294964754, 2, 0)\n'
                                       'frame = _scene_render_call_fields(memory, frame, 239454, 235174)\n'
                                       'for address, size in ((16740398, 4), (16740410, 4), (16740352, 2), '
                                       '(16740356, 2), (16740414, 2), (16740406, 2), (16740420, 2), '
                                       '(16740412, 2)):\n'
                                       '    frame = _scene_refresh_emit(memory, frame, address, size, 0)\n'
                                       'mode = state.read(16740390, 2)\n'
                                       'frame = _scene_render_compare(memory, frame, mode, 24, 16)\n'
                                       'if mode == 24:\n'
                                       '    secondary_x, secondary_y = (96, 48)\n'
                                       'else:\n'
                                       '    mode = state.read(16740390, 2)\n'
                                       '    frame = _scene_render_compare(memory, frame, mode, 28, 16)\n'
                                       '    if mode == 28:\n'
                                       '        secondary_x, secondary_y = (96, 48)\n'
                                       '    else:\n'
                                       '        secondary_x, secondary_y = (144, 96)\n'
                                       'frame = _scene_refresh_emit(memory, frame, 16740402, 2, '
                                       'secondary_x)\n'
                                       'frame = _scene_refresh_emit(memory, frame, 16740404, 2, '
                                       'secondary_y)\n'
                                       'mode = state.read(16740390, 2)\n'
                                       "frame = _first_word(frame, 'target_x', mode)\n"
                                       "frame = _scene_render_asl_word(memory, frame, 'target_x', mode, 1)\n"
                                       'offset = u16(mode << 1)\n'
                                       'frame = first_replace(frame, roster=memory.cursor_at(232328), '
                                       'candidates=memory.cursor_at(232408))\n'
                                       'x = frame.roster.word(offset)\n'
                                       "frame = _first_word(frame, 'target_y', x)\n"
                                       'y = frame.candidates.word(offset)\n'
                                       "frame = _first_word(frame, 'unit', y)\n"
                                       'frame = _scene_refresh_emit(memory, frame, 16740392, 2, x)\n'
                                       'frame = _scene_refresh_emit(memory, frame, 16740394, 2, y)\n'
                                       'mode = state.read(16740390, 2)\n'
                                       "frame = _first_word(frame, 'target_x', mode)\n"
                                       'frame = first_replace(frame, roster=memory.cursor_at(233040))\n'
                                       'movement = frame.roster.byte(mode)\n'
                                       "frame = _first_byte(frame, 'target_y', movement)\n"
                                       'frame = _scene_refresh_emit(memory, frame, 16740396, 1, movement)\n'
                                       "frame = _first_word(frame, 'target_x', 0)\n"
                                       'mode = state.read(16740390, 2)\n'
                                       'frame = _scene_render_compare(memory, frame, mode, 10, 16)\n'
                                       'video = 0\n'
                                       'if mode == 10:\n'
                                       '    video = 8192\n'
                                       "    frame = _first_word(frame, 'target_x', video)\n"
                                       'mode = state.read(16740390, 2)\n'
                                       "frame = _first_word(frame, 'count', mode)\n"
                                       "frame = _scene_render_asl_word(memory, frame, 'count', mode, 2)\n"
                                       'frame = first_replace(frame, candidates=memory.cursor_at(231354))\n'
                                       'frame = first_replace(frame, '
                                       'roster=memory.cursor_at(frame.candidates.long(u16(mode << 2))))\n'
                                       'frame = _scene_render_call_fields(memory, frame, 235096, 235378, '
                                       'video)\n'
                                       'mode = state.read(16740390, 2)\n'
                                       "frame = _first_word(frame, 'target_x', mode)\n"
                                       'frame = first_replace(frame, auxiliary=memory.cursor_at(231834))\n'
                                       'dual = frame.auxiliary.byte(mode)\n'
                                       "frame = _first_byte(frame, 'target_y', dual)\n"
                                       'frame = _scene_render_compare(memory, frame, dual, 1, 8)\n'
                                       'if dual == 1:\n'
                                       '    mode = state.read(16740390, 2)\n'
                                       "    frame = _first_word(frame, 'count', mode)\n"
                                       "    frame = _scene_render_arithmetic(memory, frame, 'count', mode, "
                                       '1, 16)\n'
                                       "    frame = _scene_render_asl_word(memory, frame, 'count', u16(mode "
                                       '+ 1), 2)\n'
                                       '    frame = first_replace(frame, '
                                       'candidates=memory.cursor_at(231354))\n'
                                       '    frame = first_replace(frame, '
                                       'roster=memory.cursor_at(frame.candidates.long(u16(u16(mode + 1) << '
                                       '2))))\n'
                                       "    frame = _first_word(frame, 'target_x', 8192)\n"
                                       '    frame = _scene_render_call_fields(memory, frame, 235096, 235426, '
                                       '8192)\n'
                                       'mode = state.read(16740390, 2)\n'
                                       "frame = _first_word(frame, 'count', mode)\n"
                                       "frame = _scene_render_asl_word(memory, frame, 'count', mode, 2)\n"
                                       'frame = first_replace(frame, candidates=memory.cursor_at(231674))\n'
                                       'frame = first_replace(frame, '
                                       'roster=memory.cursor_at(frame.candidates.long(u16(mode << 2))))\n'
                                       'frame = _copy_scene_palette_longs_fields(memory, frame)\n'
                                       "frame = _first_long(frame, 'target_x', 0)\n"
                                       'frame = memory.status_word(frame, 9472)\n'
                                       'while True:\n'
                                       '    frame = _scene_refresh_emit(memory, frame, 4294964754, 2, 1536)\n'
                                       '    while True:\n'
                                       '        value = state.read(4294964754, 1)\n'
                                       '        frame = _scene_refresh_flags(memory, frame, value, 1)\n'
                                       '        if value == 0:\n'
                                       '            break\n'
                                       "        state.progress('scripted-scene-sound-byte')\n"
                                       '    previous = state.read(16740414, 2)\n'
                                       '    frame, elapsed = _movement_binary_flags(state, frame, previous, '
                                       '1, 16)\n'
                                       '    state.write(16740414, 2, elapsed)\n'
                                       "    frame = _first_long(frame, 'target_x', 0)\n"
                                       '    mode = state.read(16740390, 2)\n'
                                       "    frame = _first_word(frame, 'target_x', mode)\n"
                                       "    frame = _scene_render_asl_word(memory, frame, 'target_x', mode, "
                                       '1)\n'
                                       "    frame = _first_long(frame, 'target_y', 0)\n"
                                       '    frame = first_replace(frame, roster=memory.cursor_at(231874))\n'
                                       '    duration = frame.roster.word(u16(mode << 1))\n'
                                       "    frame = _first_word(frame, 'target_y', duration)\n"
                                       '    elapsed = state.read(16740414, 2)\n'
                                       '    frame = _scene_render_compare(memory, frame, duration, elapsed, '
                                       '16)\n'
                                       '    if duration == elapsed:\n'
                                       '        return memory.sync_status(frame)\n'
                                       '    if frame.stack_cursor is None:\n'
                                       '        append_scene_marker_sprite(state, frame.target_x, '
                                       'frame.target_y)\n'
                                       '        _draw_scripted_scene_frame(state)\n'
                                       '    else:\n'
                                       '        frame = _scene_render_call_fields(memory, frame, 239406, '
                                       '235520)\n'
                                       '        frame = _draw_scripted_scene_frame_fields(memory, frame)'},
 '_scene_render_apply_delta': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                            'flip_mask: Long, extent: Word',
                               'returns': 'tuple',
                               'flow': 'frame = _scene_render_bit(memory, frame, frame.unit, flip_mask)\n'
                                       'if frame.unit & flip_mask:\n'
                                       "    frame = _scene_render_arithmetic(memory, frame, 'offset_x', 0, "
                                       'low8(frame.offset_x), 8, True)\n'
                                       'frame = _scene_render_bit(memory, frame, frame.offset_x, 128)\n'
                                       'if frame.offset_x & 128:\n'
                                       "    frame = _scene_render_arithmetic(memory, frame, 'offset_x', 0, "
                                       'low8(frame.offset_x), 8, True)\n'
                                       '    delta = low16(frame.offset_x)\n'
                                       "    return (_scene_render_arithmetic(memory, frame, 'offset_y', "
                                       'extent, delta, 16, True), u16(extent - delta))\n'
                                       'delta = low16(frame.offset_x)\n'
                                       "return (_scene_render_arithmetic(memory, frame, 'offset_y', extent, "
                                       'delta, 16), u16(extent + delta))'},
 '_scene_render_arithmetic': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, '
                                           'left, right, width, subtract=False',
                              'returns': 'FirstDeploymentFrame',
                              'flow': 'frame, value = _movement_binary_flags(memory.state, frame, left, '
                                      'right, width, subtract)\n'
                                      'original = frame.carrier(name)\n'
                                      'if width == 8:\n'
                                      '    carrier = None if original is None else replace_byte(original, '
                                      'value)\n'
                                      'elif width == 16:\n'
                                      '    carrier = None if original is None else replace_word(original, '
                                      'value)\n'
                                      'else:\n'
                                      '    carrier = value\n'
                                      'return first_replace(frame, **{name: carrier})'},
 '_scene_render_asl_word': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, '
                                         'original: Word | None, count: Word',
                            'returns': 'FirstDeploymentFrame',
                            'flow': 'if not 1 <= count <= 8:\n'
                                    "    raise ValueError('actual bounded scene ASL.W required')\n"
                                    'if original is None:\n'
                                    '    return first_replace(frame, **{name: None}, status=None)\n'
                                    'uint(original, 16)\n'
                                    'result = original\n'
                                    'overflow = False\n'
                                    'for index in range(count):\n'
                                    '    old_sign = bool(result & 32768)\n'
                                    '    result = u16(result << 1)\n'
                                    '    overflow = overflow or old_sign != bool(result & 32768)\n'
                                    'carry = bool(original & 1 << 16 - count)\n'
                                    'retained = frame.carrier(name)\n'
                                    'frame = first_replace(frame, **{name: None if retained is None else '
                                    'replace_word(retained, result)}, status=(17 if carry else 0) | (2 if '
                                    'overflow else 0) | (8 if result & 32768 else 0) | (4 if result == 0 '
                                    'else 0))\n'
                                    'return memory.sync_status(frame)'},
 '_scene_render_bit': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, value, mask',
                       'returns': 'FirstDeploymentFrame',
                       'flow': 'status = None if frame.status is None else frame.status & 27 | (0 if value & '
                               'mask else 4)\n'
                               'return memory.sync_status(first_replace(frame, status=status))'},
 '_scene_render_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                            'target: Long, continuation: Long, video: Word | None=None',
                               'returns': 'FirstDeploymentFrame',
                               'flow': 'memory.frame(frame)\n'
                                       'if (target, continuation) not in ((239454, 235174), (235096, '
                                       '235378), (235096, 235426), (242352, 235108), (239406, 235520), '
                                       '(235992, 236214), (239008, 236284), (239438, 236290), (239500, '
                                       '239450)):\n'
                                       "    raise ValueError('actual renderer child and return token "
                                       "required')\n"
                                       'memory.sync_status(frame)\n'
                                       'entered = frame\n'
                                       'if frame.stack_cursor is not None:\n'
                                       '    stack = frame.stack_cursor.advance(-4)\n'
                                       '    stack.set_long(0, continuation)\n'
                                       '    entered = first_replace(frame, stack_cursor=stack)\n'
                                       'if target == 239454:\n'
                                       '    result = clear_scene_sprite_chain_heads_fields(memory, entered)\n'
                                       'elif target == 235096:\n'
                                       '    result = write_vdp_word_rle_stream_fields(memory, entered, '
                                       'video)\n'
                                       'elif target == 242352:\n'
                                       '    result = set_vram_write_address_fields(memory, entered, video)\n'
                                       'elif target == 239406:\n'
                                       '    result = append_scene_marker_sprite_fields(memory, entered)\n'
                                       'elif target == 235992:\n'
                                       '    result = update_scripted_scene_position_fields(memory, entered)\n'
                                       'elif target == 239008:\n'
                                       '    result = append_clipped_scene_sprites_fields(memory, entered)\n'
                                       'elif target == 239438:\n'
                                       '    result = finish_scene_sprite_chains_fields(memory, entered)\n'
                                       'else:\n'
                                       '    result = finish_one_scene_sprite_chain_fields(memory, entered)\n'
                                       'memory.frame(result)\n'
                                       'if frame.stack_cursor is not None:\n'
                                       '    actual = result.stack_cursor.long()\n'
                                       '    if actual != continuation:\n'
                                       '        raise SceneRefreshBoundary(target, result, continuation)\n'
                                       '    result = first_replace(result, '
                                       'stack_cursor=result.stack_cursor.advance(4))\n'
                                       'return memory.sync_status(result)'},
 '_scene_render_clip_axis': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, address: '
                                          'Long, maximum: Word',
                             'returns': 'tuple',
                             'flow': 'saved = frame\n'
                                     'frame = _scene_render_save_clip(memory, frame)\n'
                                     'coordinate = memory.state.read(address, 2)\n'
                                     "frame = _first_word(frame, 'target_x', coordinate)\n"
                                     'delta = low8(frame.offset_x)\n'
                                     'frame = _scene_render_bit(memory, frame, frame.offset_x, 128)\n'
                                     'if delta & 128:\n'
                                     "    frame = _scene_render_arithmetic(memory, frame, 'offset_x', 0, "
                                     'delta, 8, True)\n'
                                     "    frame = _scene_render_arithmetic(memory, frame, 'target_x', "
                                     'coordinate, low16(frame.offset_x), 16, True)\n'
                                     'else:\n'
                                     "    frame = _scene_render_arithmetic(memory, frame, 'target_x', "
                                     'coordinate, low16(frame.offset_x), 16)\n'
                                     'projected = low16(frame.target_x)\n'
                                     'frame = _scene_render_compare(memory, frame, projected, 16, 16)\n'
                                     'rejected = projected < 16\n'
                                     'if not rejected:\n'
                                     '    frame = _scene_render_compare(memory, frame, projected, maximum, '
                                     '16)\n'
                                     '    rejected = projected > maximum\n'
                                     'if rejected:\n'
                                     '    frame = _scene_refresh_emit(memory, frame, 16740400, 2, 1)\n'
                                     'if frame.stack_cursor is not None:\n'
                                     '    frame = _scene_render_restore_clip(memory, frame)\n'
                                     'else:\n'
                                     '    frame = first_replace(saved, status=frame.status)\n'
                                     'value = memory.state.read(16740400, 2)\n'
                                     'frame = _scene_refresh_flags(memory, frame, value, 2)\n'
                                     'return (frame, value != 0)'},
 '_scene_render_compare': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, left, right, width',
 'returns': 'FirstDeploymentFrame',
 'flow': 'if frame.status is None:\n'
         '    return frame\n'
         'if width == 32:\n'
         '    retained_x = frame.status & 16\n'
         '    frame, difference = _movement_binary_flags(memory.state, frame, left, right, 32, True)\n'
         '    return memory.sync_status(first_replace(frame, status=frame.status & 15 | retained_x))\n'
         'return _movement_compare(memory.state, frame, left, right, width)'},
 '_scene_render_push_longs': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, values: '
                                           'tuple',
                              'returns': 'FirstDeploymentFrame',
                              'flow': 'if frame.stack_cursor is None:\n'
                                      '    return frame\n'
                                      'stack = frame.stack_cursor\n'
                                      'for value in values:\n'
                                      '    stack = stack.advance(-4)\n'
                                      '    stack.set_long(0, value)\n'
                                      'return first_replace(frame, stack_cursor=stack)'},
 '_scene_render_restore_clip': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                'returns': 'FirstDeploymentFrame',
                                'flow': 'if frame.stack_cursor is None:\n'
                                        '    return frame\n'
                                        'stack = frame.stack_cursor\n'
                                        'values = tuple((stack.long(index * 4) for index in range(12)))\n'
                                        'return first_replace(frame, target_x=values[0], target_y=values[1], '
                                        'unit=values[2], count=values[3], distance=values[4], '
                                        'offset_x=values[5], offset_y=values[6], choice=values[7], '
                                        'roster=memory.cursor_at(values[8]), '
                                        'candidates=memory.cursor_at(values[9]), '
                                        'controller=memory.cursor_at(values[10]), '
                                        'scan=memory.cursor_at(values[11]), stack_cursor=stack.advance(48))'},
 '_scene_render_restore_sprite': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': 'if frame.stack_cursor is None:\n'
                                          '    return frame\n'
                                          'stack = frame.stack_cursor\n'
                                          'extent, row_count, destination = (stack.long(), stack.long(4), '
                                          'stack.long(8))\n'
                                          'return first_replace(frame, offset_x=extent, offset_y=row_count, '
                                          'candidates=memory.cursor_at(destination), '
                                          'stack_cursor=stack.advance(12))'},
 '_scene_render_save_clip': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                             'returns': 'FirstDeploymentFrame',
                             'flow': 'if frame.stack_cursor is None:\n'
                                     '    return frame\n'
                                     'return _scene_render_push_longs(memory, frame, (frame.scan.base, '
                                     'frame.controller.base, frame.candidates.base, frame.roster.base, '
                                     'frame.choice, frame.offset_y, frame.offset_x, frame.distance, '
                                     'frame.count, frame.unit, frame.target_y, frame.target_x))'},
 'append_clipped_scene_sprites_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                      'FirstDeploymentFrame',
                                         'returns': 'FirstDeploymentFrame',
                                         'flow': 'return _append_scene_sprite_fields(memory, frame, True)'},
 'append_scene_marker_sprite': {'signature': 'state: SceneState, x: Long, y: Long',
                                'returns': 'SpriteBatchResult',
                                'flow': 'checked_state(state)\n'
                                        'uint(x, 32)\n'
                                        'uint(y, 32)\n'
                                        'partial = first_replace(FirstDeploymentFrame.unobserved(), '
                                        'target_x=x, target_y=y, distance=0)\n'
                                        'actual = '
                                        'append_scene_marker_sprite_fields(SceneRefreshMemory(state), '
                                        'partial)\n'
                                        'return SpriteBatchResult(actual.roster, '
                                        'SceneRenderFrame(actual.target_x, actual.target_y, actual.unit, '
                                        'actual.count, actual.distance))'},
 'append_scene_marker_sprite_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': "frame = _scene_render_arithmetic(memory, frame, 'target_x', "
                                               'low16(frame.target_x), 64, 16, True)\n'
                                               "frame = _scene_render_arithmetic(memory, frame, 'target_y', "
                                               'low16(frame.target_y), 64, 16, True)\n'
                                               "frame = _first_long(frame, 'unit', 0)\n"
                                               "frame = _first_long(frame, 'count', 0)\n"
                                               "frame = _first_word(frame, 'distance', 0)\n"
                                               'frame = first_replace(frame, '
                                               'roster=memory.cursor_at(239432))\n'
                                               'return append_clipped_scene_sprites_fields(memory, frame)'},
 'append_unclipped_scene_sprites_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                        'FirstDeploymentFrame',
                                           'returns': 'FirstDeploymentFrame',
                                           'flow': 'return _append_scene_sprite_fields(memory, frame, '
                                                   'False)'},
 'clear_scene_sprite_chain_heads': {'signature': 'state: SceneState',
                                    'returns': 'Long',
                                    'flow': 'checked_state(state)\n'
                                            'return '
                                            'clear_scene_sprite_chain_heads_fields(SceneRefreshMemory(state), '
                                            'FirstDeploymentFrame.unobserved()).target_x'},
 'clear_scene_sprite_chain_heads_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                        'FirstDeploymentFrame',
                                           'returns': 'FirstDeploymentFrame',
                                           'flow': 'memory.frame(frame)\n'
                                                   'frame = first_replace(frame, '
                                                   'roster=memory.cursor_at(16740358))\n'
                                                   "frame = _first_long(frame, 'target_x', 0)\n"
                                                   'for offset in range(0, 32, 4):\n'
                                                   '    frame = _scene_refresh_emit(memory, frame, '
                                                   'frame.roster.base + offset, 4, 0)\n'
                                                   'return _scene_refresh_emit(memory, frame, 4294963968, 1, '
                                                   '0)'},
 'finish_one_scene_sprite_chain': {'signature': 'state: SceneState, heads: Table, layer: Word, next_link: '
                                                'Long',
                                   'returns': 'Long',
                                   'flow': 'checked_state(state)\n'
                                           'checked_table(heads, state)\n'
                                           'uint(layer, 16)\n'
                                           'uint(next_link, 32)\n'
                                           'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                           'roster=heads.cursor(), target_x=layer, target_y=next_link)\n'
                                           'return '
                                           'finish_one_scene_sprite_chain_fields(SceneRefreshMemory(state), '
                                           'frame).target_y'},
 'finish_one_scene_sprite_chain_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                       'FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'memory.frame(frame)\n'
                                                  'layer = low16(frame.target_x)\n'
                                                  'value = frame.roster.long(layer)\n'
                                                  'frame = _scene_refresh_flags(memory, frame, value, 4)\n'
                                                  'if value != 0:\n'
                                                  '    frame = first_replace(frame, '
                                                  'candidates=memory.cursor_at(frame.roster.long(layer, '
                                                  '64)))\n'
                                                  '    frame = _scene_refresh_emit(memory, frame, '
                                                  'frame.candidates.base + 3, 1, low8(frame.target_y))\n'
                                                  "    frame = _first_byte(frame, 'target_y', "
                                                  'frame.roster.byte(layer, 32))\n'
                                                  'return memory.sync_status(frame)'},
 'finish_scene_sprite_chains': {'signature': 'state: SceneState',
                                'returns': 'Long',
                                'flow': 'checked_state(state)\n'
                                        'return finish_scene_sprite_chains_fields(SceneRefreshMemory(state), '
                                        'FirstDeploymentFrame.unobserved()).target_x'},
 'finish_scene_sprite_chains_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'memory.frame(frame)\n'
                                               "frame = _first_long(frame, 'target_x', 28)\n"
                                               "frame = _first_long(frame, 'target_y', 0)\n"
                                               'frame = first_replace(frame, '
                                               'roster=memory.cursor_at(16740358))\n'
                                               'while True:\n'
                                               '    frame = _scene_render_call_fields(memory, frame, 239500, '
                                               '239450)\n'
                                               '    previous = low16(frame.target_x)\n'
                                               '    frame = _scene_render_arithmetic(memory, frame, '
                                               "'target_x', previous, 4, 16, True)\n"
                                               '    if frame.status & 8:\n'
                                               '        return clear_scene_sprite_chain_heads_fields(memory, '
                                               'frame)'},
 'play_scripted_scene': {'signature': 'state: SceneState',
                         'returns': 'ScenePlaybackResult',
                         'flow': 'checked_state(state)\n'
                                 'frame = _play_scripted_scene_core(state, '
                                 'FirstDeploymentFrame.unobserved())\n'
                                 'return ScenePlaybackResult(frame.target_x, frame.target_y)'},
 'play_scripted_scene_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame',
                                'returns': 'FirstDeploymentFrame',
                                'flow': 'checked_state(state)\n'
                                        'if type(frame) is not FirstDeploymentFrame or frame.stack_cursor is '
                                        'None:\n'
                                        '    raise SceneRefreshBoundary(235162, frame, None)\n'
                                        'return _play_scripted_scene_core(state, frame)'},
 'set_vram_write_address': {'signature': 'state: SceneState, address: VideoPlaneAddress',
                            'returns': 'Long',
                            'flow': 'checked_state(state)\n'
                                    'address = _video_address(address)\n'
                                    'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                    'target_x=address.carrier)\n'
                                    'return set_vram_write_address_fields(SceneRefreshMemory(state), '
                                    'frame).target_x'},
 'set_vram_write_address_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                                'address: Word | None=None',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'memory.frame(frame)\n'
                                           'if address is None:\n'
                                           '    if frame.target_x is None:\n'
                                           '        raise SceneRefreshBoundary(242352, frame, None)\n'
                                           '    address = low16(frame.target_x)\n'
                                           'uint(address, 16)\n'
                                           'if frame.target_x is not None and low16(frame.target_x) != '
                                           'address:\n'
                                           "    raise ValueError('observed scene video WORD must agree with "
                                           "current D0')\n"
                                           'if frame.stack_cursor is not None:\n'
                                           '    frame = _scene_render_push_longs(memory, frame, '
                                           '(frame.target_y,))\n'
                                           "frame = _first_long(frame, 'target_x', address)\n"
                                           "frame = _first_long(frame, 'target_y', address)\n"
                                           'command = swap_words(address & 16383 | 16384) | address >> 14\n'
                                           'status = (16 if address & 8192 else 0) | (8 if command & '
                                           '2147483648 else 0) | (4 if command == 0 else 0)\n'
                                           'frame = first_replace(frame, target_x=command, status=status)\n'
                                           'frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                           'command)\n'
                                           'if frame.stack_cursor is not None:\n'
                                           '    restored = frame.stack_cursor.long()\n'
                                           '    frame = first_replace(frame, target_y=restored, '
                                           'stack_cursor=frame.stack_cursor.advance(4))\n'
                                           'else:\n'
                                           '    frame = first_replace(frame, target_y=None)\n'
                                           'return memory.sync_status(frame)'},
 'update_scripted_scene_position': {'signature': 'state: SceneState',
                                    'returns': 'None',
                                    'flow': 'checked_state(state)\n'
                                            'update_scripted_scene_position_fields(SceneRefreshMemory(state), '
                                            'FirstDeploymentFrame.unobserved())'},
 'update_scripted_scene_position_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                        'FirstDeploymentFrame',
                                           'returns': 'FirstDeploymentFrame',
                                           'flow': 'memory.frame(frame)\n'
                                                   'if frame.stack_cursor is not None:\n'
                                                   '    stack = frame.stack_cursor.advance(-2)\n'
                                                   '    stack.set_word(0, low16(frame.target_y))\n'
                                                   '    frame = first_replace(frame, stack_cursor=stack)\n'
                                                   'saved = frame.target_y\n'
                                                   'tick = memory.state.read(4294964000, 2)\n'
                                                   "frame = _first_word(frame, 'offset_y', tick)\n"
                                                   "frame = _first_word(frame, 'offset_y', tick & 7)\n"
                                                   'if tick & 7 == 0:\n'
                                                   '    movement = memory.state.read(16740396, 1)\n'
                                                   '    frame = _scene_refresh_flags(memory, frame, '
                                                   'movement, 1)\n'
                                                   '    if movement != 0:\n'
                                                   '        previous = memory.state.read(16740398, 2)\n'
                                                   '        frame, travelled = '
                                                   '_movement_binary_flags(memory.state, frame, previous, 1, '
                                                   '16)\n'
                                                   '        memory.state.write(16740398, 2, travelled)\n'
                                                   '        mode = memory.state.read(16740390, 2)\n'
                                                   "        frame = _first_word(frame, 'target_x', mode)\n"
                                                   '        frame = first_replace(frame, '
                                                   'opponent=memory.cursor_at(236162))\n'
                                                   '        limit = frame.opponent.byte(mode)\n'
                                                   "        frame = _first_byte(frame, 'target_y', limit)\n"
                                                   '        travelled = memory.state.read(16740398, 2)\n'
                                                   "        frame = _first_word(frame, 'choice', travelled)\n"
                                                   '        frame = _scene_render_compare(memory, frame, '
                                                   'low8(travelled), limit, 8)\n'
                                                   '        within_limit = not low8(travelled) > limit\n'
                                                   '        if within_limit:\n'
                                                   "            frame = _first_long(frame, 'target_x', 0)\n"
                                                   '            movement = memory.state.read(16740396, 1)\n'
                                                   "            frame = _first_byte(frame, 'target_x', "
                                                   'movement)\n'
                                                   '            for mask, address, subtract in ((16, '
                                                   '16740392, True), (32, 16740392, False), (64, 16740394, '
                                                   'True), (128, 16740394, False)):\n'
                                                   '                frame = _scene_render_bit(memory, frame, '
                                                   'movement, mask)\n'
                                                   '                if movement & mask:\n'
                                                   '                    frame = _first_word(frame, '
                                                   "'target_y', low16(frame.target_x))\n"
                                                   '                    distance = movement & 15\n'
                                                   '                    frame = _first_long(frame, '
                                                   "'target_y', distance)\n"
                                                   '                    previous = '
                                                   'memory.state.read(address, 2)\n'
                                                   '                    frame, value = '
                                                   '_movement_binary_flags(memory.state, frame, previous, '
                                                   'distance, 16, subtract)\n'
                                                   '                    memory.state.write(address, 2, '
                                                   'value)\n'
                                                   '                    break\n'
                                                   'if frame.stack_cursor is not None:\n'
                                                   '    saved = u32(s16(frame.stack_cursor.word()))\n'
                                                   '    frame = first_replace(frame, '
                                                   'stack_cursor=frame.stack_cursor.advance(2))\n'
                                                   'elif saved is not None:\n'
                                                   '    saved = u32(s16(low16(saved)))\n'
                                                   'return memory.sync_status(first_replace(frame, '
                                                   'target_y=saved))'},
 'write_vdp_word_rle_stream': {'signature': 'state: SceneState, source: Cursor, video_address: '
                                            'VideoPlaneAddress',
                               'returns': 'VdpStreamResult',
                               'flow': 'checked_state(state)\n'
                                       'checked_cursor(source, state)\n'
                                       'video_address = _video_address(video_address)\n'
                                       'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                       'roster=source.advance(0), target_x=video_address.carrier)\n'
                                       'result = write_vdp_word_rle_stream_fields(SceneRefreshMemory(state), '
                                       'frame)\n'
                                       'source.base = result.roster.base\n'
                                       'return VdpStreamResult(source, video_address, result.target_x)'},
 'write_vdp_word_rle_stream_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                                   'video: Word | None=None',
                                      'returns': 'FirstDeploymentFrame',
                                      'flow': 'memory.frame(frame)\n'
                                              'frame = _scene_refresh_emit(memory, frame, 12582916, 2, '
                                              '36610)\n'
                                              'frame = _scene_render_call_fields(memory, frame, 242352, '
                                              '235108, video)\n'
                                              'while True:\n'
                                              '    source = frame.roster\n'
                                              '    marker = source.byte()\n'
                                              '    frame = first_replace(frame, roster=source.advance(1))\n'
                                              "    frame = _first_byte(frame, 'target_y', marker)\n"
                                              '    high = frame.roster.byte()\n'
                                              '    frame = first_replace(frame, '
                                              'roster=frame.roster.advance(1))\n'
                                              "    frame = _first_byte(frame, 'unit', high)\n"
                                              '    frame = _scene_render_compare(memory, frame, marker, '
                                              'high, 8)\n'
                                              '    if marker != high:\n'
                                              '        low = frame.roster.byte()\n'
                                              '        frame = first_replace(frame, '
                                              'roster=frame.roster.advance(1))\n'
                                              "        frame = _first_byte(frame, 'distance', low)\n"
                                              '        original = None if frame.unit is None else '
                                              'low16(frame.unit)\n'
                                              "        frame = _scene_render_asl_word(memory, frame, 'unit', "
                                              'original, 8)\n'
                                              "        frame = _first_byte(frame, 'unit', low)\n"
                                              '        frame = _scene_refresh_emit(memory, frame, 12582912, '
                                              '2, high << 8 | low)\n'
                                              '    else:\n'
                                              "        frame = _first_long(frame, 'count', 0)\n"
                                              '        counter = frame.roster.byte()\n'
                                              '        frame = first_replace(frame, '
                                              'roster=frame.roster.advance(1))\n'
                                              "        frame = _first_byte(frame, 'count', counter)\n"
                                              '        if counter == 0:\n'
                                              '            return memory.sync_status(frame)\n'
                                              '        high = frame.roster.byte()\n'
                                              '        frame = first_replace(frame, '
                                              'roster=frame.roster.advance(1))\n'
                                              "        frame = _first_byte(frame, 'distance', high)\n"
                                              '        low = frame.roster.byte()\n'
                                              '        frame = first_replace(frame, '
                                              'roster=frame.roster.advance(1))\n'
                                              "        frame = _first_byte(frame, 'unit', low)\n"
                                              '        original = None if frame.distance is None else '
                                              'low16(frame.distance)\n'
                                              '        frame = _scene_render_asl_word(memory, frame, '
                                              "'distance', original, 8)\n"
                                              "        frame = _first_byte(frame, 'distance', low)\n"
                                              '        while True:\n'
                                              '            frame = _scene_refresh_emit(memory, frame, '
                                              '12582912, 2, high << 8 | low)\n'
                                              "            frame = _scene_refresh_decrement(frame, 'count', "
                                              'counter)\n'
                                              '            counter = u16(counter - 1)\n'
                                              '            if counter == 65535:\n'
                                              '                break'}})

# B20 repair: actual backedges reload D6; memory CLR keeps prior bus read.
DECLARATIONS.update({'_append_scene_sprite_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                              'clipped: bool',
                                 'returns': 'FirstDeploymentFrame',
                                 'flow': 'memory.frame(frame)\n'
                                         'if type(clipped) is not bool:\n'
                                         "    raise ValueError('actual scene clipping entry required')\n"
                                         'if frame.stack_cursor is not None:\n'
                                         '    frame = _scene_render_push_longs(memory, frame, '
                                         '(frame.candidates.base, frame.offset_y, frame.offset_x))\n'
                                         'original = frame\n'
                                         'count = memory.state.read(4294963968, 1)\n'
                                         'frame = _scene_render_compare(memory, frame, count, 128, 8)\n'
                                         'if count >= 128:\n'
                                         '    return memory.sync_status(_scene_render_restore_sprite(memory, '
                                         'frame))\n'
                                         "frame = _first_long(frame, 'distance', frame.distance & 65535)\n"
                                         "frame = _first_word(frame, 'choice', low16(frame.unit))\n"
                                         "frame = _first_word(frame, 'unit', low16(frame.unit) & 65528)\n"
                                         "frame = _first_word(frame, 'choice', low16(frame.choice) & 7 if "
                                         'frame.choice is not None else low16(original.unit) & 7)\n'
                                         'layer = (low16(original.unit) & 7) << 2\n'
                                         "frame = _scene_render_asl_word(memory, frame, 'choice', "
                                         'low16(original.unit) & 7, 2)\n'
                                         "frame = _scene_render_arithmetic(memory, frame, 'target_x', "
                                         'low16(frame.target_x), 128, 16)\n'
                                         'if frame.target_x & 32768:\n'
                                         '    return memory.sync_status(_scene_render_restore_sprite(memory, '
                                         'frame))\n'
                                         'frame = _scene_render_bit(memory, frame, frame.unit, 32)\n'
                                         'if frame.unit & 32:\n'
                                         "    frame = _scene_render_arithmetic(memory, frame, 'target_x', "
                                         'low16(frame.target_x), 8, 16, True)\n'
                                         "frame = _scene_render_arithmetic(memory, frame, 'target_y', "
                                         'low16(frame.target_y), 128, 16)\n'
                                         'frame = _scene_render_bit(memory, frame, frame.unit, 16)\n'
                                         'if frame.unit & 16:\n'
                                         "    frame = _scene_render_arithmetic(memory, frame, 'target_y', "
                                         'low16(frame.target_y), 8, 16, True)\n'
                                         "frame = _first_word(frame, 'offset_x', 0)\n"
                                         'count = memory.state.read(4294963968, 1)\n'
                                         "frame = _first_byte(frame, 'offset_x', count)\n"
                                         "frame = _first_shift_word(frame, 'offset_x', count, 3)\n"
                                         'frame = first_replace(frame, '
                                         'candidates=memory.cursor_at(4294965248, count << 3), '
                                         'controller=memory.cursor_at(16740358))\n'
                                         'while True:\n'
                                         "    frame = _first_word(frame, 'offset_y', low16(frame.target_x))\n"
                                         '    extent_word = low16(frame.target_x)\n'
                                         '    if clipped:\n'
                                         '        memory.state.read(16740400, 2)\n'
                                         '        frame = _scene_refresh_emit(memory, frame, 16740400, 2, '
                                         '0)\n'
                                         "    frame = _first_long(frame, 'offset_x', 0)\n"
                                         '    horizontal = frame.roster.byte()\n'
                                         "    frame = _first_byte(frame, 'offset_x', horizontal)\n"
                                         '    frame = _scene_render_compare(memory, frame, horizontal, 128, '
                                         '8)\n'
                                         '    if horizontal == 128:\n'
                                         '        break\n'
                                         '    rejected = False\n'
                                         '    if clipped:\n'
                                         '        frame, rejected = _scene_render_clip_axis(memory, frame, '
                                         '16740392, 112)\n'
                                         '    if not rejected:\n'
                                         '        extent = extent_word if frame.offset_y is None else '
                                         'low16(frame.offset_y)\n'
                                         '        frame, coordinate = _scene_render_apply_delta(memory, '
                                         'frame, 32, extent)\n'
                                         '        extent_word = coordinate\n'
                                         '        frame = _scene_refresh_emit(memory, frame, '
                                         'frame.candidates.base, 2, coordinate)\n'
                                         "        frame = _first_word(frame, 'offset_y', "
                                         'low16(frame.target_y))\n'
                                         '        extent_word = low16(frame.target_y)\n'
                                         "        frame = _first_byte(frame, 'offset_x', "
                                         'frame.roster.byte(0, 3))\n'
                                         '        if clipped:\n'
                                         '            memory.state.read(16740400, 2)\n'
                                         '            frame = _scene_refresh_emit(memory, frame, 16740400, '
                                         '2, 0)\n'
                                         '            frame, rejected = _scene_render_clip_axis(memory, '
                                         'frame, 16740394, 160)\n'
                                         '        if not rejected:\n'
                                         '            extent = extent_word if frame.offset_y is None else '
                                         'low16(frame.offset_y)\n'
                                         '            frame, coordinate = _scene_render_apply_delta(memory, '
                                         'frame, 16, extent)\n'
                                         '            extent_word = coordinate\n'
                                         '            frame = _scene_refresh_emit(memory, frame, '
                                         'frame.candidates.base + 6, 2, coordinate)\n'
                                         '            frame = _scene_refresh_emit(memory, frame, '
                                         'frame.candidates.base + 2, 1, frame.roster.byte(0, 1))\n'
                                         '            if frame.choice is not None:\n'
                                         '                layer = low16(frame.choice)\n'
                                         '            value = frame.controller.long(layer)\n'
                                         '            frame = _scene_refresh_flags(memory, frame, value, 4)\n'
                                         '            if value == 0:\n'
                                         '                frame = _scene_refresh_emit(memory, frame, '
                                         'frame.controller.base + s16(layer), 4, frame.candidates.base)\n'
                                         '                frame = _scene_refresh_emit(memory, frame, '
                                         'frame.controller.base + s16(layer) + 32, 1, '
                                         'memory.state.read(4294963968, 1))\n'
                                         '            else:\n'
                                         '                frame = first_replace(frame, '
                                         'scan=memory.cursor_at(frame.controller.long(layer, 64)))\n'
                                         '                frame = _scene_refresh_emit(memory, frame, '
                                         'frame.scan.base + 3, 1, memory.state.read(4294963968, 1))\n'
                                         '            frame = _scene_refresh_emit(memory, frame, '
                                         'frame.controller.base + s16(layer) + 64, 4, '
                                         'frame.candidates.base)\n'
                                         '            count = memory.state.read(4294963968, 1)\n'
                                         '            frame, new_count = '
                                         '_movement_binary_flags(memory.state, frame, count, 1, 8)\n'
                                         '            memory.state.write(4294963968, 1, new_count)\n'
                                         "            frame = _first_byte(frame, 'offset_x', "
                                         'frame.roster.byte(0, 1))\n'
                                         '            encoded = low16(frame.offset_x) & 240\n'
                                         "            frame = _first_word(frame, 'offset_x', encoded)\n"
                                         '            frame = _scene_render_arithmetic(memory, frame, '
                                         "'offset_x', low8(frame.offset_x), low8(frame.count), 8)\n"
                                         "            frame = _first_word(frame, 'offset_x', "
                                         'low16(frame.offset_x) ^ low16(frame.unit))\n'
                                         '            frame = _scene_render_asl_word(memory, frame, '
                                         "'offset_x', low16(frame.offset_x), 7)\n"
                                         "            frame = _first_byte(frame, 'offset_x', "
                                         'low8(frame.offset_x) | frame.roster.byte(0, 2))\n'
                                         '            frame = _scene_render_arithmetic(memory, frame, '
                                         "'offset_x', low16(frame.offset_x), low16(frame.distance), 16)\n"
                                         '            frame = _scene_refresh_emit(memory, frame, '
                                         'frame.candidates.base + 4, 2, low16(frame.offset_x))\n'
                                         '            frame = first_replace(frame, '
                                         'candidates=frame.candidates.advance(8))\n'
                                         '    frame = first_replace(frame, roster=frame.roster.advance(4))\n'
                                         '    count = memory.state.read(4294963968, 1)\n'
                                         '    frame = _scene_render_compare(memory, frame, count, 128, 8)\n'
                                         '    if count >= 128:\n'
                                         '        break\n'
                                         'if frame.stack_cursor is not None:\n'
                                         '    frame = _scene_render_restore_sprite(memory, frame)\n'
                                         'else:\n'
                                         '    frame = first_replace(frame, offset_x=original.offset_x, '
                                         'offset_y=original.offset_y, candidates=original.candidates)\n'
                                         'return memory.sync_status(frame)'}})

# B21 actual remaining mode cores and truthful unobserved projections.
DECLARATIONS.update({'_copy_scene_palette_words': {'signature': 'state, source',
                               'returns': None,
                               'flow': 'partial = first_replace(FirstDeploymentFrame.unobserved(), '
                                       'roster=source.advance(0))\n'
                                       'actual = _copy_scene_palette_words_fields(SceneRefreshMemory(state), '
                                       'partial)\n'
                                       'source.base = actual.roster.base'},
 '_copy_scene_palette_words_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                      'returns': 'FirstDeploymentFrame',
                                      'flow': 'frame = first_replace(frame, '
                                              'candidates=memory.cursor_at(4294966016))\n'
                                              'count = 16\n'
                                              "frame = _first_long(frame, 'target_x', count - 1)\n"
                                              'for index in range(count):\n'
                                              '    source, destination = (frame.roster, frame.candidates)\n'
                                              '    value = source.word()\n'
                                              '    frame = first_replace(frame, roster=source.advance(2), '
                                              'candidates=destination.advance(2))\n'
                                              '    frame = _scene_refresh_emit(memory, frame, '
                                              'destination.base, 2, value)\n'
                                              "    frame = _scene_refresh_decrement(frame, 'target_x', count "
                                              '- 1 - index)\n'
                                              'return frame'},
 '_draw_scripted_arrival': {'signature': 'state',
                            'returns': None,
                            'flow': '_draw_scripted_arrival_fields(SceneRefreshMemory(state), '
                                    'FirstDeploymentFrame.unobserved())'},
 '_draw_scripted_arrival_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "memory.frame(frame)\nif frame.stack_cursor is None:\n    raise SceneRefreshBoundary(236316, frame, None)\nwhile True:\n    frame, _ = _scene_mode_adjust_word(memory, frame, 16740412, 1)\n    counter = memory.state.read(16740412, 2)\n    frame = _scene_render_compare(memory, frame, counter, 144, 16)\n    if counter == 144:\n        mode = memory.state.read(16740390, 2)\n        frame = _first_word(frame, 'target_x', mode)\n        frame = _scene_render_asl_word(memory, frame, 'target_x', mode, 1)\n        frame = first_replace(frame, roster=memory.cursor_at(236524), candidates=memory.cursor_at(236572))\n        x, y = (frame.roster.word(u16(mode << 1)), frame.candidates.word(u16(mode << 1)))\n        frame = _first_word(frame, 'target_y', x)\n        frame = _first_word(frame, 'unit', y)\n        frame = _scene_refresh_emit(memory, frame, 16740392, 2, x)\n        frame = _scene_refresh_emit(memory, frame, 16740394, 2, y)\n        break\n    counter = memory.state.read(16740412, 2)\n    frame = _scene_render_compare(memory, frame, counter, 144, 16)\n    if counter > 144:\n        break\n    frame = first_replace(frame, roster=memory.cursor_at(memory.state.table_at(236468).long()))\n    frame = _scene_mode_packet_parameters(memory, frame, False, 5, 256)\n    frame = _scene_render_call_fields(memory, frame, 239522, 236372)\n    frame = first_replace(frame, roster=memory.cursor_at(memory.state.table_at(236476).long()))\n    frame = _scene_mode_packet_parameters(memory, frame, False, 5, 0)\n    frame = _scene_render_call_fields(memory, frame, 239522, 236400)\n    position = memory.state.read(16740392, 2)\n    frame = _scene_render_compare(memory, frame, position, 96, 16)\n    if position >= 96:\n        tick = memory.state.read(4294964000, 2)\n        frame = _first_word(frame, 'target_x', tick)\n        frame = _first_word(frame, 'target_x', tick & 3)\n        if tick & 3 == 0:\n            frame, _ = _scene_mode_adjust_word(memory, frame, 16740392, 1, True)\n    frame = first_replace(frame, roster=memory.cursor_at(memory.state.table_at(236472).long()))\n    frame = _scene_mode_packet_parameters(memory, frame, True, 4, 0)\n    frame = _scene_render_call_fields(memory, frame, 239008, 236462)\n    return frame\nmode = memory.state.read(16740390, 2)\nframe = _first_word(frame, 'target_x', mode)\nframe = _first_long(frame, 'target_y', 0)\nframe = first_replace(frame, roster=memory.cursor_at(236760))\nvariant = frame.roster.byte(mode)\nframe = _first_byte(frame, 'target_y', variant)\nframe = _scene_render_asl_word(memory, frame, 'target_y', variant, 2)\nframe = _scene_render_push_longs(memory, frame, (frame.target_y, frame.target_x))\nframe = first_replace(frame, roster=memory.cursor_at(memory.state.table_at(236728).long(u16(variant << 2))))\nframe = _scene_mode_packet_parameters(memory, frame, False, 3, 0)\nframe = _scene_render_call_fields(memory, frame, 239522, 236668)\nframe = _scene_mode_restore_longs(memory, frame, ('target_x', 'target_y'))\nframe = _scene_render_compare(memory, frame, low16(frame.target_x), 12, 16)\nif low16(frame.target_x) != 12:\n    frame = _scene_render_push_longs(memory, frame, (frame.target_y,))\n    frame = _scene_render_call_fields(memory, frame, 235992, 236690)\n    frame = _scene_mode_restore_longs(memory, frame, ('target_y',))\n    frame = first_replace(frame, roster=memory.cursor_at(memory.state.table_at(236744).long(low16(frame.target_y))))\n    frame = _scene_mode_packet_parameters(memory, frame, True, 2, 0)\n    frame = _scene_render_call_fields(memory, frame, 239008, 236722)\nreturn frame"},
 '_draw_scripted_high_mode': {'signature': 'state',
                              'returns': None,
                              'flow': '_draw_scripted_high_mode_fields(SceneRefreshMemory(state), '
                                      'FirstDeploymentFrame.unobserved())'},
 '_draw_scripted_high_mode_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'memory.frame(frame)\n'
                                             'if frame.stack_cursor is None:\n'
                                             '    raise SceneRefreshBoundary(237844, frame, None)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 28)\n'
                                             'if mode == 28:\n'
                                             '    raise SceneRefreshBoundary(237398, frame, None)\n'
                                             'frame, _ = _scene_mode_compare(memory, frame, 29)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 30)\n'
                                             'if mode == 30:\n'
                                             '    tick = memory.state.read(4294964000, 2)\n'
                                             "    frame = _first_word(frame, 'target_x', tick)\n"
                                             "    frame = _scene_mode_lsr_word(memory, frame, 'target_x', "
                                             'tick, 2)\n'
                                             '    selected = tick >> 2 & 3\n'
                                             "    frame = _first_word(frame, 'target_x', selected)\n"
                                             "    frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                             'selected, 5)\n'
                                             '    frame = first_replace(frame, '
                                             'roster=memory.cursor_at(233688 + s16(u16(selected << 5))))\n'
                                             '    frame = _copy_scene_palette_words_fields(memory, frame)\n'
                                             'else:\n'
                                             '    frame, mode = _scene_mode_compare(memory, frame, 31)\n'
                                             '    if mode == 31:\n'
                                             '        tick = memory.state.read(4294964000, 2)\n'
                                             "        frame = _first_word(frame, 'target_x', tick)\n"
                                             '        frame = _scene_mode_lsr_word(memory, frame, '
                                             "'target_x', tick, 3)\n"
                                             '        selected = tick >> 3 & 1\n'
                                             "        frame = _first_word(frame, 'target_x', selected)\n"
                                             '        frame = _scene_render_asl_word(memory, frame, '
                                             "'target_x', selected, 5)\n"
                                             '        frame = first_replace(frame, '
                                             'roster=memory.cursor_at(233816 + s16(u16(selected << 5))))\n'
                                             '        frame = _copy_scene_palette_words_fields(memory, '
                                             'frame)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 32)\n'
                                             'if mode == 32:\n'
                                             '    return _draw_scripted_wave_fields(memory, frame)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 33)\n'
                                             'if mode == 33:\n'
                                             '    return _draw_scripted_late_palette_fields(memory, frame)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 34)\n'
                                             'if mode == 34:\n'
                                             '    return _draw_scripted_three_frame_stage_fields(memory, '
                                             'frame)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 35)\n'
                                             'if mode == 35:\n'
                                             '    frame = first_replace(frame, '
                                             'roster=memory.cursor_at(memory.state.table_at(238790).long()))\n'
                                             '    frame = _scene_mode_packet_parameters(memory, frame, '
                                             'False, 5, 0)\n'
                                             '    frame = _scene_render_call_fields(memory, frame, 239522, '
                                             '238756)\n'
                                             '    frame = first_replace(frame, '
                                             'roster=memory.cursor_at(memory.state.table_at(238794).long()))\n'
                                             '    frame = _scene_mode_packet_parameters(memory, frame, '
                                             'False, 5, 256)\n'
                                             '    return _scene_render_call_fields(memory, frame, 239522, '
                                             '238784)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 37)\n'
                                             'if mode == 37:\n'
                                             '    frame = first_replace(frame, '
                                             'roster=memory.cursor_at(memory.state.table_at(238858).long()))\n'
                                             '    frame = _scene_mode_packet_parameters(memory, frame, '
                                             'False, 5, 0)\n'
                                             '    frame = _scene_render_call_fields(memory, frame, 239522, '
                                             '238824)\n'
                                             '    frame = first_replace(frame, '
                                             'roster=memory.cursor_at(memory.state.table_at(238862).long()))\n'
                                             '    frame = _scene_mode_packet_parameters(memory, frame, '
                                             'False, 5, 256)\n'
                                             '    return _scene_render_call_fields(memory, frame, 239522, '
                                             '238852)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 39)\n'
                                             'if mode == 39:\n'
                                             '    frame = first_replace(frame, '
                                             'roster=memory.cursor_at(memory.state.table_at(238898).long()))\n'
                                             '    frame = _scene_mode_packet_parameters(memory, frame, '
                                             'False, 5, 0)\n'
                                             '    return _scene_render_call_fields(memory, frame, 239522, '
                                             '238892)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 31)\n'
                                             'if mode == 31:\n'
                                             "    frame = _first_long(frame, 'target_y', 4)\n"
                                             '    frame = first_replace(frame, '
                                             'roster=memory.cursor_at(memory.state.table_at(238040).long(low16(frame.target_y))))\n'
                                             '    frame = _scene_mode_packet_parameters(memory, frame, '
                                             'False, 4, 0)\n'
                                             '    return _scene_render_call_fields(memory, frame, 239522, '
                                             '238034)\n'
                                             'frame = first_replace(frame, '
                                             'roster=memory.cursor_at(memory.state.table_at(238040).long()))\n'
                                             'frame = _scene_mode_packet_parameters(memory, frame, False, 5, '
                                             '0)\n'
                                             'return _scene_render_call_fields(memory, frame, 239522, '
                                             '238002)'},
 '_draw_scripted_landing': {'signature': 'state',
                            'returns': None,
                            'flow': '_draw_scripted_landing_fields(SceneRefreshMemory(state), '
                                    'FirstDeploymentFrame.unobserved())'},
 '_draw_scripted_landing_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'memory.frame(frame)\n'
                                           'if frame.stack_cursor is None:\n'
                                           '    raise SceneRefreshBoundary(236946, frame, None)\n'
                                           'frame = _scene_render_call_fields(memory, frame, 235992, '
                                           '236950)\n'
                                           'frame = first_replace(frame, '
                                           'roster=memory.cursor_at(memory.state.table_at(237086).long()))\n'
                                           'frame = _scene_mode_packet_parameters(memory, frame, True, 5, '
                                           '0)\n'
                                           'frame = _scene_render_call_fields(memory, frame, 239008, '
                                           '236980)\n'
                                           'y = memory.state.read(16740394, 2)\n'
                                           'frame = _scene_render_compare(memory, frame, y, 96, 16)\n'
                                           'if y != 96:\n'
                                           '    return frame\n'
                                           'counter = memory.state.read(16740412, 2)\n'
                                           'frame = _scene_render_compare(memory, frame, counter, 20, 16)\n'
                                           'if counter != 20:\n'
                                           '    tick = memory.state.read(4294964000, 2)\n'
                                           "    frame = _first_word(frame, 'target_x', tick)\n"
                                           "    frame = _first_word(frame, 'target_x', tick & 15)\n"
                                           '    if tick & 15 == 0:\n'
                                           '        frame, _ = _scene_mode_adjust_word(memory, frame, '
                                           '16740412, 4)\n'
                                           "        frame = _first_long(frame, 'count', 0)\n"
                                           '        offset = memory.state.read(16740412, 2)\n'
                                           "        frame = _first_word(frame, 'count', offset)\n"
                                           '        frame = first_replace(frame, '
                                           'candidates=memory.cursor_at(237094))\n'
                                           '        frame = first_replace(frame, '
                                           'roster=memory.cursor_at(frame.candidates.long(offset)))\n'
                                           '        frame = _copy_scene_palette_longs_fields(memory, frame)\n'
                                           "frame = _first_long(frame, 'target_x', 4)\n"
                                           'frame = first_replace(frame, '
                                           'roster=memory.cursor_at(memory.state.table_at(237086).long(low16(frame.target_x))))\n'
                                           'frame = _scene_mode_packet_parameters(memory, frame, False, 4, '
                                           '0)\n'
                                           'return _scene_render_call_fields(memory, frame, 239522, 237080)'},
 '_draw_scripted_late_palette': {'signature': 'state',
                                 'returns': None,
                                 'flow': '_draw_scripted_late_palette_fields(SceneRefreshMemory(state), '
                                         'FirstDeploymentFrame.unobserved())'},
 '_draw_scripted_late_palette_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                     'FirstDeploymentFrame',
                                        'returns': 'FirstDeploymentFrame',
                                        'flow': 'memory.frame(frame)\n'
                                                'if frame.stack_cursor is None:\n'
                                                '    raise SceneRefreshBoundary(238370, frame, None)\n'
                                                'frame = _scene_render_call_fields(memory, frame, 235992, '
                                                '238374)\n'
                                                'frame = first_replace(frame, '
                                                'candidates=memory.cursor_at(232844))\n'
                                                'frame = first_replace(frame, '
                                                'roster=memory.cursor_at(frame.candidates.long()))\n'
                                                'frame = _scene_mode_packet_parameters(memory, frame, True, '
                                                '4, 0)\n'
                                                'frame = _scene_render_call_fields(memory, frame, 239008, '
                                                '238404)\n'
                                                'elapsed = memory.state.read(16740414, 2)\n'
                                                'frame = _scene_render_compare(memory, frame, elapsed, 120, '
                                                '16)\n'
                                                'if elapsed < 120:\n'
                                                '    return frame\n'
                                                'counter = memory.state.read(16740412, 2)\n'
                                                'frame = _scene_render_compare(memory, frame, counter, 24, '
                                                '16)\n'
                                                'if counter != 24:\n'
                                                '    tick = memory.state.read(4294964000, 2)\n'
                                                "    frame = _first_word(frame, 'target_x', tick)\n"
                                                "    frame = _first_word(frame, 'target_x', tick & 15)\n"
                                                '    if tick & 15 == 0:\n'
                                                '        frame, _ = _scene_mode_adjust_word(memory, frame, '
                                                '16740412, 4)\n'
                                                "        frame = _first_long(frame, 'count', 0)\n"
                                                '        offset = memory.state.read(16740412, 2)\n'
                                                "        frame = _first_word(frame, 'count', offset)\n"
                                                '        frame = first_replace(frame, '
                                                'candidates=memory.cursor_at(238514))\n'
                                                '        frame = first_replace(frame, '
                                                'roster=memory.cursor_at(frame.candidates.long(offset)))\n'
                                                '        frame = _copy_scene_palette_longs_fields(memory, '
                                                'frame)\n'
                                                'frame = first_replace(frame, '
                                                'candidates=memory.cursor_at(232848))\n'
                                                'frame = first_replace(frame, '
                                                'roster=memory.cursor_at(frame.candidates.long()))\n'
                                                'frame = _scene_mode_packet_parameters(memory, frame, False, '
                                                '5, 0)\n'
                                                'return _scene_render_call_fields(memory, frame, 239522, '
                                                '238508)'},
 '_draw_scripted_scene_frame': {'signature': 'state',
                                'returns': None,
                                'flow': '_draw_scripted_scene_frame_fields(SceneRefreshMemory(state), '
                                        'FirstDeploymentFrame.unobserved())'},
 '_draw_scripted_scene_frame_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'if frame.stack_cursor is None:\n'
                                               '    raise SceneRefreshBoundary(235520, frame, None)\n'
                                               "frame = _first_long(frame, 'target_x', 0)\n"
                                               'frame, mode = _scene_mode_compare(memory, frame, 10)\n'
                                               'if mode < 10:\n'
                                               '    return _draw_scripted_sequence_fields(memory, frame)\n'
                                               'frame, mode = _scene_mode_compare(memory, frame, 11)\n'
                                               'if mode <= 11:\n'
                                               '    frame = _scene_render_call_fields(memory, frame, 235992, '
                                               '236214)\n'
                                               '    frame, mode = _scene_mode_compare(memory, frame, 11)\n'
                                               '    selected = 1 if mode == 11 else 0\n'
                                               "    frame = _first_long(frame, 'target_y', selected)\n"
                                               '    frame = _scene_render_asl_word(memory, frame, '
                                               "'target_y', selected, 2)\n"
                                               '    frame = first_replace(frame, '
                                               'roster=memory.cursor_at(memory.state.table_at(236296).long(selected '
                                               '<< 2)))\n'
                                               "    frame = _first_word(frame, 'target_x', "
                                               'memory.state.read(16740392, 2))\n'
                                               "    frame = _first_word(frame, 'target_y', "
                                               'memory.state.read(16740394, 2))\n'
                                               "    frame = _first_long(frame, 'unit', 4)\n"
                                               "    frame = _first_long(frame, 'count', 0)\n"
                                               '    frame, mode = _scene_mode_compare(memory, frame, 11)\n'
                                               "    frame = _first_long(frame, 'distance', 0 if mode == 11 "
                                               'else 256)\n'
                                               '    frame = _scene_render_call_fields(memory, frame, 239008, '
                                               '236284)\n'
                                               'else:\n'
                                               '    frame, mode = _scene_mode_compare(memory, frame, 19)\n'
                                               '    if mode <= 19:\n'
                                               '        frame = _draw_scripted_arrival_fields(memory, '
                                               'frame)\n'
                                               '    else:\n'
                                               '        frame, mode = _scene_mode_compare(memory, frame, '
                                               '21)\n'
                                               '        if mode <= 21:\n'
                                               '            frame = _draw_scripted_two_layer_fields(memory, '
                                               'frame)\n'
                                               '        else:\n'
                                               '            frame, mode = _scene_mode_compare(memory, frame, '
                                               '23)\n'
                                               '            if mode <= 23:\n'
                                               '                raise SceneRefreshBoundary(237130, frame, '
                                               'None)\n'
                                               '            frame, mode = _scene_mode_compare(memory, frame, '
                                               '25)\n'
                                               '            if mode <= 25:\n'
                                               '                raise SceneRefreshBoundary(237398, frame, '
                                               'None)\n'
                                               '            frame, mode = _scene_mode_compare(memory, frame, '
                                               '27)\n'
                                               '            if mode == 27:\n'
                                               '                return '
                                               '_draw_scripted_sequence_fields(memory, frame)\n'
                                               '            frame, mode = _scene_mode_compare(memory, frame, '
                                               '27)\n'
                                               '            if mode > 27:\n'
                                               '                frame = '
                                               '_draw_scripted_high_mode_fields(memory, frame)\n'
                                               '            else:\n'
                                               '                frame = '
                                               '_draw_scripted_landing_fields(memory, frame)\n'
                                               'return _scene_render_call_fields(memory, frame, 239438, '
                                               '236290)'},
 '_draw_scripted_sequence': {'signature': 'state',
                             'returns': None,
                             'flow': '_draw_scripted_sequence_fields(SceneRefreshMemory(state), '
                                     'FirstDeploymentFrame.unobserved())'},
 '_draw_scripted_sequence_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'memory.frame(frame)\n'
                                            'if frame.stack_cursor is None:\n'
                                            '    raise SceneRefreshBoundary(235534, frame, None)\n'
                                            'tick = memory.state.read(4294964000, 2)\n'
                                            "frame = _first_word(frame, 'target_x', tick)\n"
                                            "frame = _first_word(frame, 'target_x', tick & 7)\n"
                                            'if tick & 7 == 0:\n'
                                            '    frame, _ = _scene_mode_adjust_word(memory, frame, 16740356, '
                                            '1)\n'
                                            'while True:\n'
                                            "    frame = _first_long(frame, 'target_y', 0)\n"
                                            '    mode = memory.state.read(16740390, 2)\n'
                                            "    frame = _first_word(frame, 'count', mode)\n"
                                            "    frame = _scene_render_asl_word(memory, frame, 'count', "
                                            'mode, 2)\n'
                                            '    frame = first_replace(frame, '
                                            'candidates=memory.cursor_at(231954))\n'
                                            '    frame = first_replace(frame, '
                                            'roster=memory.cursor_at(frame.candidates.long(u16(mode << '
                                            '2))))\n'
                                            "    frame = _first_long(frame, 'target_x', 0)\n"
                                            '    offset = memory.state.read(16740356, 2)\n'
                                            "    frame = _first_word(frame, 'target_x', offset)\n"
                                            '    frame = first_replace(frame, '
                                            'roster=frame.roster.advance(s16(offset)))\n'
                                            '    packet = frame.roster.byte()\n'
                                            "    frame = _first_byte(frame, 'target_y', packet)\n"
                                            '    if not packet & 128:\n'
                                            '        break\n'
                                            "    frame = _first_long(frame, 'target_x', 0)\n"
                                            '    frame = first_replace(frame, '
                                            'roster=frame.roster.advance(1))\n'
                                            '    redirected = frame.roster.byte()\n'
                                            "    frame = _first_byte(frame, 'target_y', redirected)\n"
                                            '    frame = _scene_refresh_emit(memory, frame, 16740356, 2, '
                                            'low16(frame.target_y))\n'
                                            'frame, mode = _scene_mode_compare(memory, frame, 5)\n'
                                            'if mode == 5:\n'
                                            '    frame = _scene_render_compare(memory, frame, '
                                            'low16(frame.target_y), 3, 16)\n'
                                            '    if low16(frame.target_y) >= 3:\n'
                                            '        tick = memory.state.read(4294964000, 2)\n'
                                            "        frame = _first_word(frame, 'target_x', tick)\n"
                                            "        frame = _first_word(frame, 'target_x', tick & 7)\n"
                                            '        skip_palette = False\n'
                                            '        if tick & 7 == 0:\n'
                                            '            counter = memory.state.read(16740412, 2)\n'
                                            '            frame = _scene_render_compare(memory, frame, '
                                            'counter, 40, 16)\n'
                                            '            if counter == 40:\n'
                                            '                skip_palette = True\n'
                                            '            else:\n'
                                            '                frame, _ = _scene_mode_adjust_word(memory, '
                                            'frame, 16740412, 4)\n'
                                            '        if not skip_palette:\n'
                                            "            frame = _first_long(frame, 'count', 0)\n"
                                            '            offset = memory.state.read(16740412, 2)\n'
                                            "            frame = _first_word(frame, 'count', offset)\n"
                                            '            frame = first_replace(frame, '
                                            'candidates=memory.cursor_at(235876))\n'
                                            '            frame = first_replace(frame, '
                                            'roster=memory.cursor_at(frame.candidates.long(offset)))\n'
                                            '            frame = _copy_scene_palette_longs_fields(memory, '
                                            'frame)\n'
                                            'frame, mode = _scene_mode_compare(memory, frame, 1)\n'
                                            'if mode == 1:\n'
                                            "    frame = _first_long(frame, 'unit', 0)\n"
                                            '    frame = _scene_render_compare(memory, frame, '
                                            'low16(frame.target_y), 1, 16)\n'
                                            '    palette_offset = 0 if low16(frame.target_y) == 1 else 32\n'
                                            '    if palette_offset != 0:\n'
                                            "        frame = _scene_render_arithmetic(memory, frame, 'unit', "
                                            '0, palette_offset, 16)\n'
                                            '    frame = first_replace(frame, '
                                            'candidates=memory.cursor_at(4294966016), '
                                            'roster=memory.cursor_at(233112 + s16(palette_offset)))\n'
                                            '    frame = _copy_scene_palette_longs_fields(memory, frame)\n'
                                            'frame = _scene_mode_push_word(memory, frame, '
                                            'low16(frame.target_y))\n'
                                            'frame = _scene_render_call_fields(memory, frame, 235992, '
                                            '235668)\n'
                                            "frame = _first_long(frame, 'target_x', 0)\n"
                                            'mode = memory.state.read(16740390, 2)\n'
                                            "frame = _first_word(frame, 'count', mode)\n"
                                            "frame = _scene_render_asl_word(memory, frame, 'count', mode, "
                                            '2)\n'
                                            'frame = first_replace(frame, '
                                            'auxiliary=memory.cursor_at(232488))\n'
                                            'frame = first_replace(frame, '
                                            'candidates=memory.cursor_at(frame.auxiliary.long(u16(mode << '
                                            '2))))\n'
                                            'selected = low16(frame.target_y)\n'
                                            "frame = _scene_render_asl_word(memory, frame, 'target_y', "
                                            'selected, 2)\n'
                                            'frame = first_replace(frame, '
                                            'candidates=frame.candidates.advance(s16(u16(selected << 2))))\n'
                                            'frame = first_replace(frame, '
                                            'roster=memory.cursor_at(frame.candidates.long()))\n'
                                            'frame = _scene_mode_packet_parameters(memory, frame, True, 4, '
                                            '0)\n'
                                            "frame = _first_long(frame, 'distance', 0)\n"
                                            'frame = _scene_render_call_fields(memory, frame, 239008, '
                                            '235716)\n'
                                            "frame = _scene_mode_restore_word(memory, frame, 'target_y')\n"
                                            'mode = memory.state.read(16740390, 2)\n'
                                            "frame = _first_word(frame, 'target_x', mode)\n"
                                            'frame = first_replace(frame, '
                                            'auxiliary=memory.cursor_at(231834))\n'
                                            'dual = frame.auxiliary.byte(mode)\n'
                                            "frame = _first_byte(frame, 'unit', dual)\n"
                                            'frame = _scene_render_compare(memory, frame, dual, 1, 8)\n'
                                            'if dual == 1:\n'
                                            "    frame = _first_long(frame, 'target_x', 0)\n"
                                            '    mode = memory.state.read(16740390, 2)\n'
                                            "    frame = _first_word(frame, 'count', mode)\n"
                                            "    frame = _scene_render_asl_word(memory, frame, 'count', "
                                            'mode, 2)\n'
                                            '    frame = first_replace(frame, '
                                            'controller=memory.cursor_at(232852))\n'
                                            '    frame = first_replace(frame, '
                                            'candidates=memory.cursor_at(frame.controller.long(u16(mode << '
                                            '2))))\n'
                                            '    selected = low16(frame.target_y)\n'
                                            "    frame = _scene_render_asl_word(memory, frame, 'target_y', "
                                            'selected, 2)\n'
                                            '    frame = first_replace(frame, '
                                            'candidates=frame.candidates.advance(s16(u16(selected << 2))))\n'
                                            '    frame = first_replace(frame, '
                                            'roster=memory.cursor_at(frame.candidates.long()))\n'
                                            '    frame = _scene_mode_packet_parameters(memory, frame, True, '
                                            '4, 256)\n'
                                            "    frame = _first_long(frame, 'distance', 256)\n"
                                            '    frame = _scene_render_call_fields(memory, frame, 239008, '
                                            '235794)\n'
                                            'return _scene_render_call_fields(memory, frame, 239438, '
                                            '235800)'},
 '_draw_scripted_three_frame_stage': {'signature': 'state',
                                      'returns': None,
                                      'flow': '_draw_scripted_three_frame_stage_fields(SceneRefreshMemory(state), '
                                              'FirstDeploymentFrame.unobserved())'},
 '_draw_scripted_three_frame_stage_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                          'FirstDeploymentFrame',
                                             'returns': 'FirstDeploymentFrame',
                                             'flow': 'memory.frame(frame)\n'
                                                     'if frame.stack_cursor is None:\n'
                                                     '    raise SceneRefreshBoundary(238542, frame, None)\n'
                                                     'frame, _ = _scene_mode_adjust_word(memory, frame, '
                                                     '16740420, 1)\n'
                                                     'counter = memory.state.read(16740420, 2)\n'
                                                     'frame = _scene_render_compare(memory, frame, counter, '
                                                     '128, 16)\n'
                                                     'if counter <= 128:\n'
                                                     '    tick = memory.state.read(4294964001, 1)\n'
                                                     "    frame = _first_byte(frame, 'target_x', tick)\n"
                                                     '    frame = _scene_render_bit(memory, frame, '
                                                     'frame.target_x, 4)\n'
                                                     '    if not tick & 4:\n'
                                                     '        index = memory.state.read(16740412, 2)\n'
                                                     '        frame = _scene_render_compare(memory, frame, '
                                                     'index, 2, 16)\n'
                                                     '        if index >= 2:\n'
                                                     '            frame = _scene_refresh_emit(memory, frame, '
                                                     '16740412, 2, 0)\n'
                                                     '        else:\n'
                                                     '            frame, _ = _scene_mode_adjust_word(memory, '
                                                     'frame, 16740412, 1)\n'
                                                     '    index = memory.state.read(16740412, 2)\n'
                                                     "    frame = _first_word(frame, 'target_y', index)\n"
                                                     '    frame = _scene_render_asl_word(memory, frame, '
                                                     "'target_y', index, 2)\n"
                                                     '    frame = first_replace(frame, '
                                                     'roster=memory.cursor_at(memory.state.table_at(238642).long(u16(index '
                                                     '<< 2))))\n'
                                                     '    frame = _scene_mode_packet_parameters(memory, '
                                                     'frame, False, 5, 0)\n'
                                                     '    return _scene_render_call_fields(memory, frame, '
                                                     '239522, 238636)\n'
                                                     'frame = first_replace(frame, '
                                                     'roster=memory.cursor_at(memory.state.table_at(238722).long()))\n'
                                                     'frame = _scene_mode_packet_parameters(memory, frame, '
                                                     'False, 5, 0)\n'
                                                     'frame = _scene_render_call_fields(memory, frame, '
                                                     '239522, 238680)\n'
                                                     'frame = _scene_render_call_fields(memory, frame, '
                                                     '235992, 238686)\n'
                                                     "frame = _first_long(frame, 'target_y', 4)\n"
                                                     'frame = first_replace(frame, '
                                                     'roster=memory.cursor_at(memory.state.table_at(238722).long(low16(frame.target_y))))\n'
                                                     'frame = _scene_mode_packet_parameters(memory, frame, '
                                                     'True, 4, 0)\n'
                                                     'return _scene_render_call_fields(memory, frame, '
                                                     '239008, 238716)'},
 '_draw_scripted_two_layer_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'memory.frame(frame)\n'
                                             'if frame.stack_cursor is None:\n'
                                             '    raise SceneRefreshBoundary(236796, frame, None)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 20)\n'
                                             'table = 236906 if mode == 20 else 236914\n'
                                             'frame = first_replace(frame, '
                                             'roster=memory.cursor_at(memory.state.table_at(table).long()))\n'
                                             'frame = _scene_mode_packet_parameters(memory, frame, False, 3, '
                                             '0)\n'
                                             'frame = _scene_render_call_fields(memory, frame, 239522, '
                                             '236844)\n'
                                             'frame = _scene_render_call_fields(memory, frame, 235992, '
                                             '236850)\n'
                                             "frame = _first_long(frame, 'target_y', 4)\n"
                                             'frame, mode = _scene_mode_compare(memory, frame, 20)\n'
                                             'table = 236906 if mode == 20 else 236914\n'
                                             'frame = first_replace(frame, '
                                             'roster=memory.cursor_at(memory.state.table_at(table).long(low16(frame.target_y))))\n'
                                             'frame = _scene_mode_packet_parameters(memory, frame, True, 2, '
                                             '0)\n'
                                             'return _scene_render_call_fields(memory, frame, 239008, '
                                             '236900)'},
 '_draw_scripted_wave': {'signature': 'state',
                         'returns': None,
                         'flow': '_draw_scripted_wave_fields(SceneRefreshMemory(state), '
                                 'FirstDeploymentFrame.unobserved())'},
 '_draw_scripted_wave_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                'returns': 'FirstDeploymentFrame',
                                'flow': 'memory.frame(frame)\n'
                                        'if frame.stack_cursor is None:\n'
                                        '    raise SceneRefreshBoundary(238048, frame, None)\n'
                                        "frame = _first_long(frame, 'target_x', 0)\n"
                                        'offset = memory.state.read(16740412, 2)\n'
                                        "frame = _first_word(frame, 'target_x', offset)\n"
                                        'frame = first_replace(frame, candidates=memory.cursor_at(238300 + '
                                        's16(offset)))\n'
                                        'frame = _scene_refresh_emit(memory, frame, 16740392, 2, '
                                        'frame.candidates.word())\n'
                                        'frame, _ = _scene_mode_adjust_word(memory, frame, 16740412, 2)\n'
                                        'offset = memory.state.read(16740412, 2)\n'
                                        "frame = _first_word(frame, 'target_x', offset)\n"
                                        'frame = first_replace(frame, candidates=memory.cursor_at(238300 + '
                                        's16(offset)))\n'
                                        'frame = _scene_refresh_emit(memory, frame, 16740394, 2, 96)\n'
                                        'tick = memory.state.read(4294964000, 2)\n'
                                        "frame = _first_word(frame, 'target_x', tick)\n"
                                        "frame = _first_word(frame, 'target_x', tick & 3)\n"
                                        'if tick & 3:\n'
                                        '    frame, _ = _scene_mode_adjust_word(memory, frame, 16740412, 2, '
                                        'True)\n'
                                        'else:\n'
                                        '    frame, _ = _scene_mode_adjust_word(memory, frame, 16740412, 2)\n'
                                        '    frame = first_replace(frame, '
                                        'candidates=memory.cursor_at(238300))\n'
                                        '    offset = memory.state.read(16740412, 2)\n'
                                        '    frame = first_replace(frame, '
                                        'candidates=frame.candidates.advance(s16(offset)))\n'
                                        '    end = frame.candidates.word()\n'
                                        "    frame = _first_word(frame, 'target_y', end)\n"
                                        '    frame = _scene_render_compare(memory, frame, end, 255, 16)\n'
                                        '    if end == 255:\n'
                                        '        frame = _scene_refresh_emit(memory, frame, 16740412, 2, 0)\n'
                                        'frame = first_replace(frame, candidates=memory.cursor_at(232836))\n'
                                        'frame = first_replace(frame, '
                                        'roster=memory.cursor_at(frame.candidates.long()))\n'
                                        'frame = _scene_mode_packet_parameters(memory, frame, True, 3, 0)\n'
                                        'frame = _scene_render_call_fields(memory, frame, 239008, 238190)\n'
                                        'elapsed = memory.state.read(16740414, 2)\n'
                                        'frame = _scene_render_compare(memory, frame, elapsed, 120, 16)\n'
                                        'if elapsed < 120:\n'
                                        '    return frame\n'
                                        'counter = memory.state.read(16740356, 2)\n'
                                        'frame = _scene_render_compare(memory, frame, counter, 24, 16)\n'
                                        'if counter != 24:\n'
                                        '    tick = memory.state.read(4294964000, 2)\n'
                                        "    frame = _first_word(frame, 'target_x', tick)\n"
                                        "    frame = _first_word(frame, 'target_x', tick & 7)\n"
                                        '    if tick & 7 == 0:\n'
                                        '        frame, _ = _scene_mode_adjust_word(memory, frame, 16740356, '
                                        '4)\n'
                                        "        frame = _first_long(frame, 'count', 0)\n"
                                        '        offset = memory.state.read(16740356, 2)\n'
                                        "        frame = _first_word(frame, 'count', offset)\n"
                                        '        frame = first_replace(frame, '
                                        'candidates=memory.cursor_at(238342))\n'
                                        '        frame = first_replace(frame, '
                                        'roster=memory.cursor_at(frame.candidates.long(offset)))\n'
                                        '        frame = _copy_scene_palette_longs_fields(memory, frame)\n'
                                        'frame = first_replace(frame, candidates=memory.cursor_at(232840))\n'
                                        'frame = first_replace(frame, '
                                        'roster=memory.cursor_at(frame.candidates.long()))\n'
                                        'frame = _scene_mode_packet_parameters(memory, frame, False, 5, 0)\n'
                                        'return _scene_render_call_fields(memory, frame, 239522, 238294)'},
 '_play_scripted_scene_core': {'signature': 'state: SceneState, frame: FirstDeploymentFrame',
                               'returns': 'FirstDeploymentFrame',
                               'flow': "memory = SceneRefreshMemory(state)\nmemory.frame(frame)\nframe = memory.status_word(frame, 9984)\nstate.read(4294964754, 2)\nframe = _scene_refresh_emit(memory, frame, 4294964754, 2, 0)\nframe = _scene_render_call_fields(memory, frame, 239454, 235174)\nfor address, size in ((16740398, 4), (16740410, 4), (16740352, 2), (16740356, 2), (16740414, 2), (16740406, 2), (16740420, 2), (16740412, 2)):\n    state.read(address, size)\n    frame = _scene_refresh_emit(memory, frame, address, size, 0)\nmode = state.read(16740390, 2)\nframe = _scene_render_compare(memory, frame, mode, 24, 16)\nif mode == 24:\n    secondary_x, secondary_y = (96, 48)\nelse:\n    mode = state.read(16740390, 2)\n    frame = _scene_render_compare(memory, frame, mode, 28, 16)\n    if mode == 28:\n        secondary_x, secondary_y = (96, 48)\n    else:\n        secondary_x, secondary_y = (144, 96)\nframe = _scene_refresh_emit(memory, frame, 16740402, 2, secondary_x)\nframe = _scene_refresh_emit(memory, frame, 16740404, 2, secondary_y)\nmode = state.read(16740390, 2)\nframe = _first_word(frame, 'target_x', mode)\nframe = _scene_render_asl_word(memory, frame, 'target_x', mode, 1)\noffset = u16(mode << 1)\nframe = first_replace(frame, roster=memory.cursor_at(232328), candidates=memory.cursor_at(232408))\nx = frame.roster.word(offset)\nframe = _first_word(frame, 'target_y', x)\ny = frame.candidates.word(offset)\nframe = _first_word(frame, 'unit', y)\nframe = _scene_refresh_emit(memory, frame, 16740392, 2, x)\nframe = _scene_refresh_emit(memory, frame, 16740394, 2, y)\nmode = state.read(16740390, 2)\nframe = _first_word(frame, 'target_x', mode)\nframe = first_replace(frame, roster=memory.cursor_at(233040))\nmovement = frame.roster.byte(mode)\nframe = _first_byte(frame, 'target_y', movement)\nframe = _scene_refresh_emit(memory, frame, 16740396, 1, movement)\nframe = _first_word(frame, 'target_x', 0)\nmode = state.read(16740390, 2)\nframe = _scene_render_compare(memory, frame, mode, 10, 16)\nvideo = 0\nif mode == 10:\n    video = 8192\n    frame = _first_word(frame, 'target_x', video)\nmode = state.read(16740390, 2)\nframe = _first_word(frame, 'count', mode)\nframe = _scene_render_asl_word(memory, frame, 'count', mode, 2)\nframe = first_replace(frame, candidates=memory.cursor_at(231354))\nframe = first_replace(frame, roster=memory.cursor_at(frame.candidates.long(u16(mode << 2))))\nframe = _scene_render_call_fields(memory, frame, 235096, 235378, video)\nmode = state.read(16740390, 2)\nframe = _first_word(frame, 'target_x', mode)\nframe = first_replace(frame, auxiliary=memory.cursor_at(231834))\ndual = frame.auxiliary.byte(mode)\nframe = _first_byte(frame, 'target_y', dual)\nframe = _scene_render_compare(memory, frame, dual, 1, 8)\nif dual == 1:\n    mode = state.read(16740390, 2)\n    frame = _first_word(frame, 'count', mode)\n    frame = _scene_render_arithmetic(memory, frame, 'count', mode, 1, 16)\n    frame = _scene_render_asl_word(memory, frame, 'count', u16(mode + 1), 2)\n    frame = first_replace(frame, candidates=memory.cursor_at(231354))\n    frame = first_replace(frame, roster=memory.cursor_at(frame.candidates.long(u16(u16(mode + 1) << 2))))\n    frame = _first_word(frame, 'target_x', 8192)\n    frame = _scene_render_call_fields(memory, frame, 235096, 235426, 8192)\nmode = state.read(16740390, 2)\nframe = _first_word(frame, 'count', mode)\nframe = _scene_render_asl_word(memory, frame, 'count', mode, 2)\nframe = first_replace(frame, candidates=memory.cursor_at(231674))\nframe = first_replace(frame, roster=memory.cursor_at(frame.candidates.long(u16(mode << 2))))\nframe = _copy_scene_palette_longs_fields(memory, frame)\nframe = _first_long(frame, 'target_x', 0)\nframe = memory.status_word(frame, 9472)\nwhile True:\n    frame = _scene_refresh_emit(memory, frame, 4294964754, 2, 1536)\n    while True:\n        value = state.read(4294964754, 1)\n        frame = _scene_refresh_flags(memory, frame, value, 1)\n        if value == 0:\n            break\n        state.progress('scripted-scene-sound-byte')\n    previous = state.read(16740414, 2)\n    frame, elapsed = _movement_binary_flags(state, frame, previous, 1, 16)\n    state.write(16740414, 2, elapsed)\n    frame = _first_long(frame, 'target_x', 0)\n    mode = state.read(16740390, 2)\n    frame = _first_word(frame, 'target_x', mode)\n    frame = _scene_render_asl_word(memory, frame, 'target_x', mode, 1)\n    frame = _first_long(frame, 'target_y', 0)\n    frame = first_replace(frame, roster=memory.cursor_at(231874))\n    duration = frame.roster.word(u16(mode << 1))\n    frame = _first_word(frame, 'target_y', duration)\n    elapsed = state.read(16740414, 2)\n    frame = _scene_render_compare(memory, frame, duration, elapsed, 16)\n    if duration == elapsed:\n        return memory.sync_status(frame)\n    if frame.stack_cursor is None:\n        raise SceneRefreshBoundary(239406, frame, 235520)\n    frame = _scene_render_call_fields(memory, frame, 239406, 235520)\n    frame = _draw_scripted_scene_frame_fields(memory, frame)"},
 '_scene_mode_adjust_word': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, address: '
                                          'Long, amount: Word, subtract: bool=False',
                             'returns': 'tuple',
                             'flow': 'previous = memory.state.read(address, 2)\n'
                                     'frame, value = _movement_binary_flags(memory.state, frame, previous, '
                                     'amount, 16, subtract)\n'
                                     'memory.state.write(address, 2, value)\n'
                                     'return (frame, value)'},
 '_scene_mode_compare': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, value: Word',
                         'returns': 'tuple',
                         'flow': 'mode = memory.state.read(16740390, 2)\n'
                                 'return (_scene_render_compare(memory, frame, mode, value, 16), mode)'},
 '_scene_mode_lsr_word': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, '
                                       'original: Word, count: Word',
                          'returns': 'FirstDeploymentFrame',
                          'flow': 'value = original >> count\n'
                                  'carry = bool(original & 1 << count - 1)\n'
                                  'carrier = None if frame.carrier(name) is None else '
                                  'replace_word(frame.carrier(name), value)\n'
                                  'status = (17 if carry else 0) | (4 if value == 0 else 0)\n'
                                  'return memory.sync_status(first_replace(frame, status=status, **{name: '
                                  'carrier}))'},
 '_scene_mode_packet_parameters': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                                'moving: bool, attributes: Long, tile: Word',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'if moving:\n'
                                           '    x = memory.state.read(16740392, 2)\n'
                                           '    y = memory.state.read(16740394, 2)\n'
                                           'else:\n'
                                           '    x, y = (96, 96)\n'
                                           "frame = _first_word(frame, 'target_x', x)\n"
                                           "frame = _first_word(frame, 'target_y', y)\n"
                                           "frame = _first_long(frame, 'unit', attributes)\n"
                                           "frame = _first_long(frame, 'count', 0)\n"
                                           "return _first_word(frame, 'distance', tile)"},
 '_scene_mode_push_word': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, value: '
                                        'Word',
                           'returns': 'FirstDeploymentFrame',
                           'flow': 'if frame.stack_cursor is None:\n'
                                   '    raise SceneRefreshBoundary(235660, frame, None)\n'
                                   'stack = frame.stack_cursor.advance(-2)\n'
                                   'stack.set_word(0, value)\n'
                                   'return first_replace(frame, stack_cursor=stack)'},
 '_scene_mode_restore_longs': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, names: '
                                            'tuple',
                               'returns': 'FirstDeploymentFrame',
                               'flow': 'if frame.stack_cursor is None:\n'
                                       '    raise SceneRefreshBoundary(235660, frame, None)\n'
                                       'stack = frame.stack_cursor\n'
                                       'values = tuple((stack.long(index * 4) for index in '
                                       'range(len(names))))\n'
                                       'return first_replace(frame, stack_cursor=stack.advance(len(names) * '
                                       '4), **{name: value for name, value in zip(names, values)})'},
 '_scene_mode_restore_word': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name',
                              'returns': 'FirstDeploymentFrame',
                              'flow': 'if frame.stack_cursor is None:\n'
                                      '    raise SceneRefreshBoundary(235718, frame, None)\n'
                                      'stack = frame.stack_cursor\n'
                                      'return first_replace(frame, stack_cursor=stack.advance(2), **{name: '
                                      'u32(s16(stack.word()))})'},
 '_scene_render_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                            'target: Long, continuation: Long, video: Word | None=None',
                               'returns': 'FirstDeploymentFrame',
                               'flow': 'memory.frame(frame)\n'
                                       'if (target, continuation) not in ((239454, 235174), (235096, '
                                       '235378), (235096, 235426), (242352, 235108), (239406, 235520), '
                                       '(235992, 236214), (239008, 236284), (239438, 236290), (239500, '
                                       '239450), (235992, 235668), (239008, 235716), (239008, 235794), '
                                       '(239438, 235800), (239522, 236372), (239522, 236400), (239008, '
                                       '236462), (239522, 236668), (235992, 236690), (239008, 236722), '
                                       '(239522, 236844), (235992, 236850), (239008, 236900), (235992, '
                                       '236950), (239008, 236980), (239522, 237080), (239008, 238190), '
                                       '(239522, 238294), (235992, 238374), (239008, 238404), (239522, '
                                       '238508), (239522, 238636), (239522, 238680), (235992, 238686), '
                                       '(239008, 238716), (239522, 238756), (239522, 238784), (239522, '
                                       '238824), (239522, 238852), (239522, 238892), (239522, 238034), '
                                       '(239522, 238002)):\n'
                                       "    raise ValueError('actual renderer child and return token "
                                       "required')\n"
                                       'memory.sync_status(frame)\n'
                                       'entered = frame\n'
                                       'if frame.stack_cursor is not None:\n'
                                       '    stack = frame.stack_cursor.advance(-4)\n'
                                       '    stack.set_long(0, continuation)\n'
                                       '    entered = first_replace(frame, stack_cursor=stack)\n'
                                       'if target == 239454:\n'
                                       '    result = clear_scene_sprite_chain_heads_fields(memory, entered)\n'
                                       'elif target == 235096:\n'
                                       '    result = write_vdp_word_rle_stream_fields(memory, entered, '
                                       'video)\n'
                                       'elif target == 242352:\n'
                                       '    result = set_vram_write_address_fields(memory, entered, video)\n'
                                       'elif target == 239406:\n'
                                       '    result = append_scene_marker_sprite_fields(memory, entered)\n'
                                       'elif target == 235992:\n'
                                       '    result = update_scripted_scene_position_fields(memory, entered)\n'
                                       'elif target == 239008:\n'
                                       '    result = append_clipped_scene_sprites_fields(memory, entered)\n'
                                       'elif target == 239522:\n'
                                       '    result = append_unclipped_scene_sprites_fields(memory, entered)\n'
                                       'elif target == 239438:\n'
                                       '    result = finish_scene_sprite_chains_fields(memory, entered)\n'
                                       'else:\n'
                                       '    result = finish_one_scene_sprite_chain_fields(memory, entered)\n'
                                       'memory.frame(result)\n'
                                       'if frame.stack_cursor is not None:\n'
                                       '    actual = result.stack_cursor.long()\n'
                                       '    if actual != continuation:\n'
                                       '        raise SceneRefreshBoundary(target, result, continuation)\n'
                                       '    result = first_replace(result, '
                                       'stack_cursor=result.stack_cursor.advance(4))\n'
                                       'return memory.sync_status(result)'}})

# B22 actual last paired/staged slots and scalar projections; ordinary lowering unchanged.
DECLARATIONS.pop('_scene_pointer')
DECLARATIONS.pop('_draw_fixed_scene_pointer')
DECLARATIONS.pop('_draw_moving_scene_pointer')
DECLARATIONS.update({'_draw_scripted_high_mode_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'memory.frame(frame)\n'
                                             'if frame.stack_cursor is None:\n'
                                             '    raise SceneRefreshBoundary(237844, frame, None)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 28)\n'
                                             'if mode == 28:\n'
                                             '    return _draw_scripted_staged_pair_fields(memory, frame)\n'
                                             'frame, _ = _scene_mode_compare(memory, frame, 29)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 30)\n'
                                             'if mode == 30:\n'
                                             '    tick = memory.state.read(4294964000, 2)\n'
                                             "    frame = _first_word(frame, 'target_x', tick)\n"
                                             "    frame = _scene_mode_lsr_word(memory, frame, 'target_x', "
                                             'tick, 2)\n'
                                             '    selected = tick >> 2 & 3\n'
                                             "    frame = _first_word(frame, 'target_x', selected)\n"
                                             "    frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                             'selected, 5)\n'
                                             '    frame = first_replace(frame, '
                                             'roster=memory.cursor_at(233688 + s16(u16(selected << 5))))\n'
                                             '    frame = _copy_scene_palette_words_fields(memory, frame)\n'
                                             'else:\n'
                                             '    frame, mode = _scene_mode_compare(memory, frame, 31)\n'
                                             '    if mode == 31:\n'
                                             '        tick = memory.state.read(4294964000, 2)\n'
                                             "        frame = _first_word(frame, 'target_x', tick)\n"
                                             '        frame = _scene_mode_lsr_word(memory, frame, '
                                             "'target_x', tick, 3)\n"
                                             '        selected = tick >> 3 & 1\n'
                                             "        frame = _first_word(frame, 'target_x', selected)\n"
                                             '        frame = _scene_render_asl_word(memory, frame, '
                                             "'target_x', selected, 5)\n"
                                             '        frame = first_replace(frame, '
                                             'roster=memory.cursor_at(233816 + s16(u16(selected << 5))))\n'
                                             '        frame = _copy_scene_palette_words_fields(memory, '
                                             'frame)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 32)\n'
                                             'if mode == 32:\n'
                                             '    return _draw_scripted_wave_fields(memory, frame)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 33)\n'
                                             'if mode == 33:\n'
                                             '    return _draw_scripted_late_palette_fields(memory, frame)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 34)\n'
                                             'if mode == 34:\n'
                                             '    return _draw_scripted_three_frame_stage_fields(memory, '
                                             'frame)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 35)\n'
                                             'if mode == 35:\n'
                                             '    frame = first_replace(frame, '
                                             'roster=memory.cursor_at(memory.state.table_at(238790).long()))\n'
                                             '    frame = _scene_mode_packet_parameters(memory, frame, '
                                             'False, 5, 0)\n'
                                             '    frame = _scene_render_call_fields(memory, frame, 239522, '
                                             '238756)\n'
                                             '    frame = first_replace(frame, '
                                             'roster=memory.cursor_at(memory.state.table_at(238794).long()))\n'
                                             '    frame = _scene_mode_packet_parameters(memory, frame, '
                                             'False, 5, 256)\n'
                                             '    return _scene_render_call_fields(memory, frame, 239522, '
                                             '238784)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 37)\n'
                                             'if mode == 37:\n'
                                             '    frame = first_replace(frame, '
                                             'roster=memory.cursor_at(memory.state.table_at(238858).long()))\n'
                                             '    frame = _scene_mode_packet_parameters(memory, frame, '
                                             'False, 5, 0)\n'
                                             '    frame = _scene_render_call_fields(memory, frame, 239522, '
                                             '238824)\n'
                                             '    frame = first_replace(frame, '
                                             'roster=memory.cursor_at(memory.state.table_at(238862).long()))\n'
                                             '    frame = _scene_mode_packet_parameters(memory, frame, '
                                             'False, 5, 256)\n'
                                             '    return _scene_render_call_fields(memory, frame, 239522, '
                                             '238852)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 39)\n'
                                             'if mode == 39:\n'
                                             '    frame = first_replace(frame, '
                                             'roster=memory.cursor_at(memory.state.table_at(238898).long()))\n'
                                             '    frame = _scene_mode_packet_parameters(memory, frame, '
                                             'False, 5, 0)\n'
                                             '    return _scene_render_call_fields(memory, frame, 239522, '
                                             '238892)\n'
                                             'frame, mode = _scene_mode_compare(memory, frame, 31)\n'
                                             'if mode == 31:\n'
                                             "    frame = _first_long(frame, 'target_y', 4)\n"
                                             '    frame = first_replace(frame, '
                                             'roster=memory.cursor_at(memory.state.table_at(238040).long(low16(frame.target_y))))\n'
                                             '    frame = _scene_mode_packet_parameters(memory, frame, '
                                             'False, 4, 0)\n'
                                             '    return _scene_render_call_fields(memory, frame, 239522, '
                                             '238034)\n'
                                             'frame = first_replace(frame, '
                                             'roster=memory.cursor_at(memory.state.table_at(238040).long()))\n'
                                             'frame = _scene_mode_packet_parameters(memory, frame, False, 5, '
                                             '0)\n'
                                             'return _scene_render_call_fields(memory, frame, 239522, '
                                             '238002)'},
 '_draw_scripted_paired_positions': {'signature': 'state',
                                     'returns': None,
                                     'flow': '_draw_scripted_paired_positions_fields(SceneRefreshMemory(state), '
                                             'FirstDeploymentFrame.unobserved())'},
 '_draw_scripted_paired_positions_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                         'FirstDeploymentFrame',
                                            'returns': 'FirstDeploymentFrame',
                                            'flow': 'memory.frame(frame)\n'
                                                    'if frame.stack_cursor is None:\n'
                                                    '    raise SceneRefreshBoundary(237130, frame, None)\n'
                                                    'frame = _scene_render_call_fields(memory, frame, '
                                                    '235992, 237134)\n'
                                                    'frame = first_replace(frame, '
                                                    'roster=memory.cursor_at(memory.state.table_at(237328).long()))\n'
                                                    'frame = _scene_mode_packet_parameters(memory, frame, '
                                                    'True, 5, 0)\n'
                                                    'frame = _scene_render_call_fields(memory, frame, '
                                                    '239008, 237164)\n'
                                                    "frame = _first_byte(frame, 'target_y', "
                                                    'memory.state.read(16740396, 1))\n'
                                                    "frame = _first_word(frame, 'unit', "
                                                    'memory.state.read(16740392, 2))\n'
                                                    "frame = _first_word(frame, 'count', "
                                                    'memory.state.read(16740394, 2))\n'
                                                    'frame = _scene_render_push_longs(memory, frame, '
                                                    '(frame.count, frame.unit, frame.target_y))\n'
                                                    'frame, _ = _scene_mode_adjust_word(memory, frame, '
                                                    '16740390, 1)\n'
                                                    'mode = memory.state.read(16740390, 2)\n'
                                                    "frame = _first_word(frame, 'target_x', mode)\n"
                                                    'frame = first_replace(frame, '
                                                    'roster=memory.cursor_at(233040))\n'
                                                    'movement = frame.roster.byte(mode)\n'
                                                    "frame = _first_byte(frame, 'target_y', movement)\n"
                                                    'frame = _scene_refresh_emit(memory, frame, 16740396, 1, '
                                                    'movement)\n'
                                                    'frame = _scene_render_call_fields(memory, frame, '
                                                    '237336, 237218)\n'
                                                    'frame = _scene_refresh_emit(memory, frame, 16740392, 2, '
                                                    'memory.state.read(16740402, 2))\n'
                                                    'frame = _scene_refresh_emit(memory, frame, 16740394, 2, '
                                                    'memory.state.read(16740404, 2))\n'
                                                    'frame = _scene_render_call_fields(memory, frame, '
                                                    '235992, 237244)\n'
                                                    "frame = _first_long(frame, 'target_y', 4)\n"
                                                    'frame = first_replace(frame, '
                                                    'roster=memory.cursor_at(memory.state.table_at(237328).long(low16(frame.target_y))))\n'
                                                    'frame = _scene_mode_packet_parameters(memory, frame, '
                                                    'True, 4, 0)\n'
                                                    'frame = _scene_render_call_fields(memory, frame, '
                                                    '239008, 237274)\n'
                                                    'frame = _scene_refresh_emit(memory, frame, 16740402, 2, '
                                                    'memory.state.read(16740392, 2))\n'
                                                    'frame = _scene_refresh_emit(memory, frame, 16740404, 2, '
                                                    'memory.state.read(16740394, 2))\n'
                                                    'frame = _scene_mode_restore_longs(memory, frame, '
                                                    "('target_y', 'unit', 'count'))\n"
                                                    'frame = _scene_refresh_emit(memory, frame, 16740396, 1, '
                                                    'low8(frame.target_y))\n'
                                                    'frame = _scene_refresh_emit(memory, frame, 16740392, 2, '
                                                    'low16(frame.unit))\n'
                                                    'frame = _scene_refresh_emit(memory, frame, 16740394, 2, '
                                                    'low16(frame.count))\n'
                                                    'frame, _ = _scene_mode_adjust_word(memory, frame, '
                                                    '16740390, 1, True)\n'
                                                    'return frame'},
 '_draw_scripted_scene_frame_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'if frame.stack_cursor is None:\n'
                                               '    raise SceneRefreshBoundary(235520, frame, None)\n'
                                               "frame = _first_long(frame, 'target_x', 0)\n"
                                               'frame, mode = _scene_mode_compare(memory, frame, 10)\n'
                                               'if mode < 10:\n'
                                               '    return _draw_scripted_sequence_fields(memory, frame)\n'
                                               'frame, mode = _scene_mode_compare(memory, frame, 11)\n'
                                               'if mode <= 11:\n'
                                               '    frame = _scene_render_call_fields(memory, frame, 235992, '
                                               '236214)\n'
                                               '    frame, mode = _scene_mode_compare(memory, frame, 11)\n'
                                               '    selected = 1 if mode == 11 else 0\n'
                                               "    frame = _first_long(frame, 'target_y', selected)\n"
                                               '    frame = _scene_render_asl_word(memory, frame, '
                                               "'target_y', selected, 2)\n"
                                               '    frame = first_replace(frame, '
                                               'roster=memory.cursor_at(memory.state.table_at(236296).long(selected '
                                               '<< 2)))\n'
                                               "    frame = _first_word(frame, 'target_x', "
                                               'memory.state.read(16740392, 2))\n'
                                               "    frame = _first_word(frame, 'target_y', "
                                               'memory.state.read(16740394, 2))\n'
                                               "    frame = _first_long(frame, 'unit', 4)\n"
                                               "    frame = _first_long(frame, 'count', 0)\n"
                                               '    frame, mode = _scene_mode_compare(memory, frame, 11)\n'
                                               "    frame = _first_long(frame, 'distance', 0 if mode == 11 "
                                               'else 256)\n'
                                               '    frame = _scene_render_call_fields(memory, frame, 239008, '
                                               '236284)\n'
                                               'else:\n'
                                               '    frame, mode = _scene_mode_compare(memory, frame, 19)\n'
                                               '    if mode <= 19:\n'
                                               '        frame = _draw_scripted_arrival_fields(memory, '
                                               'frame)\n'
                                               '    else:\n'
                                               '        frame, mode = _scene_mode_compare(memory, frame, '
                                               '21)\n'
                                               '        if mode <= 21:\n'
                                               '            frame = _draw_scripted_two_layer_fields(memory, '
                                               'frame)\n'
                                               '        else:\n'
                                               '            frame, mode = _scene_mode_compare(memory, frame, '
                                               '23)\n'
                                               '            if mode <= 23:\n'
                                               '                frame = '
                                               '_draw_scripted_paired_positions_fields(memory, frame)\n'
                                               '            else:\n'
                                               '                frame, mode = _scene_mode_compare(memory, '
                                               'frame, 25)\n'
                                               '                if mode <= 25:\n'
                                               '                    frame = '
                                               '_draw_scripted_staged_pair_fields(memory, frame)\n'
                                               '                else:\n'
                                               '                    frame, mode = '
                                               '_scene_mode_compare(memory, frame, 27)\n'
                                               '                    if mode == 27:\n'
                                               '                        return '
                                               '_draw_scripted_sequence_fields(memory, frame)\n'
                                               '                    frame, mode = '
                                               '_scene_mode_compare(memory, frame, 27)\n'
                                               '                    if mode > 27:\n'
                                               '                        frame = '
                                               '_draw_scripted_high_mode_fields(memory, frame)\n'
                                               '                    else:\n'
                                               '                        frame = '
                                               '_draw_scripted_landing_fields(memory, frame)\n'
                                               'return _scene_render_call_fields(memory, frame, 239438, '
                                               '236290)'},
 '_draw_scripted_staged_pair': {'signature': 'state',
                                'returns': None,
                                'flow': '_draw_scripted_staged_pair_fields(SceneRefreshMemory(state), '
                                        'FirstDeploymentFrame.unobserved())'},
 '_draw_scripted_staged_pair_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'memory.frame(frame)\n'
                                               'if frame.stack_cursor is None:\n'
                                               '    raise SceneRefreshBoundary(237398, frame, None)\n'
                                               'frame, _ = _scene_mode_adjust_word(memory, frame, 16740420, '
                                               '1)\n'
                                               'tick = memory.state.read(4294964000, 2)\n'
                                               "frame = _first_word(frame, 'target_x', tick)\n"
                                               'frame = _scene_render_bit(memory, frame, frame.target_x, 8)\n'
                                               'selected = 4 if tick & 8 else 0\n'
                                               "frame = _first_long(frame, 'target_y', selected)\n"
                                               'frame = _scene_render_call_fields(memory, frame, 237706, '
                                               '237428)\n'
                                               'frame = _scene_mode_packet_parameters(memory, frame, False, '
                                               '5, 0)\n'
                                               'frame = _scene_render_call_fields(memory, frame, 239522, '
                                               '237450)\n'
                                               'counter = memory.state.read(16740420, 2)\n'
                                               'frame = _scene_render_compare(memory, frame, counter, 32, '
                                               '16)\n'
                                               'if counter < 32:\n'
                                               '    return frame\n'
                                               'frame = _scene_render_call_fields(memory, frame, 235992, '
                                               '237468)\n'
                                               "frame = _first_long(frame, 'target_y', 8)\n"
                                               'frame = _scene_render_call_fields(memory, frame, 237706, '
                                               '237474)\n'
                                               'frame = _scene_mode_packet_parameters(memory, frame, True, '
                                               '4, 0)\n'
                                               'frame = _scene_render_call_fields(memory, frame, 239008, '
                                               '237500)\n'
                                               'counter = memory.state.read(16740420, 2)\n'
                                               'frame = _scene_render_compare(memory, frame, counter, 64, '
                                               '16)\n'
                                               'if counter < 64:\n'
                                               '    return frame\n'
                                               "frame = _first_word(frame, 'target_x', "
                                               'memory.state.read(16740392, 2))\n'
                                               "frame = _first_word(frame, 'target_y', "
                                               'memory.state.read(16740394, 2))\n'
                                               "frame = _first_byte(frame, 'unit', "
                                               'memory.state.read(16740396, 1))\n'
                                               'frame = _scene_render_push_longs(memory, frame, (frame.unit, '
                                               'frame.target_y, frame.target_x))\n'
                                               'frame, _ = _scene_mode_adjust_word(memory, frame, 16740390, '
                                               '1)\n'
                                               'mode = memory.state.read(16740390, 2)\n'
                                               "frame = _first_word(frame, 'target_x', mode)\n"
                                               'frame = first_replace(frame, '
                                               'roster=memory.cursor_at(233040))\n'
                                               'movement = frame.roster.byte(mode)\n'
                                               "frame = _first_byte(frame, 'target_y', movement)\n"
                                               'frame = _scene_refresh_emit(memory, frame, 16740396, 1, '
                                               'movement)\n'
                                               'frame = _scene_refresh_emit(memory, frame, 16740392, 2, '
                                               'memory.state.read(16740402, 2))\n'
                                               'frame = _scene_refresh_emit(memory, frame, 16740394, 2, '
                                               'memory.state.read(16740404, 2))\n'
                                               'frame = _scene_render_call_fields(memory, frame, 235992, '
                                               '237586)\n'
                                               "frame = _first_long(frame, 'target_y', 12)\n"
                                               'frame = _scene_render_call_fields(memory, frame, 237706, '
                                               '237592)\n'
                                               'frame = _scene_mode_packet_parameters(memory, frame, True, '
                                               '4, 0)\n'
                                               'frame = _scene_render_call_fields(memory, frame, 239008, '
                                               '237618)\n'
                                               'frame = _scene_refresh_emit(memory, frame, 16740402, 2, '
                                               'memory.state.read(16740392, 2))\n'
                                               'frame = _scene_refresh_emit(memory, frame, 16740404, 2, '
                                               'memory.state.read(16740394, 2))\n'
                                               'frame = _scene_mode_restore_longs(memory, frame, '
                                               "('target_x', 'target_y', 'unit'))\n"
                                               'frame = _scene_refresh_emit(memory, frame, 16740392, 2, '
                                               'low16(frame.target_x))\n'
                                               'frame = _scene_refresh_emit(memory, frame, 16740394, 2, '
                                               'low16(frame.target_y))\n'
                                               'frame = _scene_refresh_emit(memory, frame, 16740396, 1, '
                                               'low8(frame.unit))\n'
                                               'frame, _ = _scene_mode_adjust_word(memory, frame, 16740390, '
                                               '1, True)\n'
                                               'return frame'},
 '_scene_render_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                            'target: Long, continuation: Long, video: Word | None=None',
                               'returns': 'FirstDeploymentFrame',
                               'flow': 'memory.frame(frame)\n'
                                       'if (target, continuation) not in ((239454, 235174), (235096, '
                                       '235378), (235096, 235426), (242352, 235108), (239406, 235520), '
                                       '(235992, 236214), (239008, 236284), (239438, 236290), (239500, '
                                       '239450), (235992, 235668), (239008, 235716), (239008, 235794), '
                                       '(239438, 235800), (239522, 236372), (239522, 236400), (239008, '
                                       '236462), (239522, 236668), (235992, 236690), (239008, 236722), '
                                       '(239522, 236844), (235992, 236850), (239008, 236900), (235992, '
                                       '236950), (239008, 236980), (239522, 237080), (239008, 238190), '
                                       '(239522, 238294), (235992, 238374), (239008, 238404), (239522, '
                                       '238508), (239522, 238636), (239522, 238680), (235992, 238686), '
                                       '(239008, 238716), (239522, 238756), (239522, 238784), (239522, '
                                       '238824), (239522, 238852), (239522, 238892), (239522, 238034), '
                                       '(239522, 238002), (235992, 237134), (239008, 237164), (237336, '
                                       '237218), (235992, 237244), (239008, 237274), (237706, 237428), '
                                       '(239522, 237450), (235992, 237468), (237706, 237474), (239008, '
                                       '237500), (235992, 237586), (237706, 237592), (239008, 237618)):\n'
                                       "    raise ValueError('actual renderer child and return token "
                                       "required')\n"
                                       'memory.sync_status(frame)\n'
                                       'entered = frame\n'
                                       'if frame.stack_cursor is not None:\n'
                                       '    stack = frame.stack_cursor.advance(-4)\n'
                                       '    stack.set_long(0, continuation)\n'
                                       '    entered = first_replace(frame, stack_cursor=stack)\n'
                                       'if target == 239454:\n'
                                       '    result = clear_scene_sprite_chain_heads_fields(memory, entered)\n'
                                       'elif target == 235096:\n'
                                       '    result = write_vdp_word_rle_stream_fields(memory, entered, '
                                       'video)\n'
                                       'elif target == 242352:\n'
                                       '    result = set_vram_write_address_fields(memory, entered, video)\n'
                                       'elif target == 239406:\n'
                                       '    result = append_scene_marker_sprite_fields(memory, entered)\n'
                                       'elif target == 235992:\n'
                                       '    result = update_scripted_scene_position_fields(memory, entered)\n'
                                       'elif target == 239008:\n'
                                       '    result = append_clipped_scene_sprites_fields(memory, entered)\n'
                                       'elif target == 239522:\n'
                                       '    result = append_unclipped_scene_sprites_fields(memory, entered)\n'
                                       'elif target == 237336:\n'
                                       '    result = initialize_scripted_secondary_position_fields(memory, '
                                       'entered)\n'
                                       'elif target == 237706:\n'
                                       '    result = select_scene_object_frame_fields(memory, entered)\n'
                                       'elif target == 239438:\n'
                                       '    result = finish_scene_sprite_chains_fields(memory, entered)\n'
                                       'else:\n'
                                       '    result = finish_one_scene_sprite_chain_fields(memory, entered)\n'
                                       'memory.frame(result)\n'
                                       'if frame.stack_cursor is not None:\n'
                                       '    actual = result.stack_cursor.long()\n'
                                       '    if actual != continuation:\n'
                                       '        raise SceneRefreshBoundary(target, result, continuation)\n'
                                       '    result = first_replace(result, '
                                       'stack_cursor=result.stack_cursor.advance(4))\n'
                                       'return memory.sync_status(result)'},
 'initialize_scripted_secondary_position': {'signature': 'state: SceneState, mode: Word',
                                            'returns': 'None',
                                            'flow': 'checked_state(state)\n'
                                                    'uint(mode, 16)\n'
                                                    'initialize_scripted_secondary_position_fields(SceneRefreshMemory(state), '
                                                    'FirstDeploymentFrame.unobserved(), mode)'},
 'initialize_scripted_secondary_position_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                                'FirstDeploymentFrame, mode: Word | '
                                                                'None=None',
                                                   'returns': 'FirstDeploymentFrame',
                                                   'flow': 'memory.frame(frame)\n'
                                                           'latched = memory.state.read(16740406, 2)\n'
                                                           'frame = _scene_refresh_flags(memory, frame, '
                                                           'latched, 2)\n'
                                                           'if latched != 0:\n'
                                                           '    return frame\n'
                                                           'if mode is None:\n'
                                                           '    if frame.target_x is None:\n'
                                                           '        raise SceneRefreshBoundary(237346, '
                                                           'frame, None)\n'
                                                           '    mode = low16(frame.target_x)\n'
                                                           'uint(mode, 16)\n'
                                                           'if frame.target_x is not None and '
                                                           'low16(frame.target_x) != mode:\n'
                                                           "    raise ValueError('actual secondary mode WORD "
                                                           "disagrees with D0')\n"
                                                           'frame = _scene_render_asl_word(memory, frame, '
                                                           "'target_x', mode, 1)\n"
                                                           'offset = u16(mode << 1)\n'
                                                           'frame = first_replace(frame, '
                                                           'roster=memory.cursor_at(232328), '
                                                           'candidates=memory.cursor_at(232408))\n'
                                                           'x, y = (frame.roster.word(offset), '
                                                           'frame.candidates.word(offset))\n'
                                                           "frame = _first_word(frame, 'target_y', x)\n"
                                                           "frame = _first_word(frame, 'unit', y)\n"
                                                           'frame = _scene_refresh_emit(memory, frame, '
                                                           '16740402, 2, x)\n'
                                                           'frame = _scene_refresh_emit(memory, frame, '
                                                           '16740404, 2, y)\n'
                                                           'return _scene_refresh_emit(memory, frame, '
                                                           '16740406, 2, 1)'},
 'select_scene_object_frame': {'signature': 'state: SceneState, frame_offset: Long, tick_carrier: Long=0',
                               'returns': 'SceneFrameResult',
                               'flow': 'checked_state(state)\n'
                                       'uint(frame_offset, 32)\n'
                                       'uint(tick_carrier, 32)\n'
                                       'partial = first_replace(FirstDeploymentFrame.unobserved(), '
                                       'target_x=tick_carrier, target_y=frame_offset)\n'
                                       'actual = select_scene_object_frame_fields(SceneRefreshMemory(state), '
                                       'partial)\n'
                                       'return SceneFrameResult(actual.roster, actual.target_y)'},
 'select_scene_object_frame_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                      'returns': 'FirstDeploymentFrame',
                                      'flow': 'memory.frame(frame)\n'
                                              'if frame.target_y is None:\n'
                                              '    raise SceneRefreshBoundary(237706, frame, None)\n'
                                              'frame, mode = _scene_mode_compare(memory, frame, 27)\n'
                                              'if mode <= 27:\n'
                                              '    return first_replace(frame, '
                                              'roster=memory.cursor_at(memory.state.table_at(237674).long(low16(frame.target_y))))\n'
                                              'selected = low16(frame.target_y)\n'
                                              'frame = _scene_render_compare(memory, frame, selected, 7, '
                                              '16)\n'
                                              'if selected <= 7:\n'
                                              '    if frame.target_x is None:\n'
                                              '        raise SceneRefreshBoundary(237738, frame, None)\n'
                                              '    sequence = memory.state.read(16740412, 2)\n'
                                              "    frame = _first_word(frame, 'unit', sequence)\n"
                                              '    tick = low16(frame.target_x)\n'
                                              "    frame = _first_word(frame, 'target_x', tick & 7)\n"
                                              '    if tick & 7 == 0:\n'
                                              '        frame, _ = _scene_mode_adjust_word(memory, frame, '
                                              '16740412, 1)\n'
                                              '        sequence = memory.state.read(16740412, 2)\n'
                                              "        frame = _first_word(frame, 'unit', sequence)\n"
                                              '    frame = first_replace(frame, '
                                              'scan=memory.cursor_at(237796))\n'
                                              '    selected = frame.scan.byte(sequence)\n'
                                              "    frame = _first_byte(frame, 'target_y', selected)\n"
                                              '    frame = _scene_render_compare(memory, frame, selected, '
                                              '255, 8)\n'
                                              '    if selected == 255:\n'
                                              '        memory.state.read(16740412, 2)\n'
                                              '        frame = _scene_refresh_emit(memory, frame, 16740412, '
                                              '2, 0)\n'
                                              "        frame = _first_long(frame, 'target_y', 0)\n"
                                              "    frame = _first_long(frame, 'target_y', frame.target_y & "
                                              '15)\n'
                                              'return first_replace(frame, '
                                              'roster=memory.cursor_at(memory.state.table_at(237690).long(low16(frame.target_y))))'}})

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
APPROVED.setdefault('business_reuse',set()).update({'_restore_glyph_values', '_save_glyph_values'})
DECLARATIONS.update({'_glyph_restore_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, original: '
                                        'FirstDeploymentFrame, include_source: bool',
                           'returns': 'FirstDeploymentFrame',
                           'flow': 'if frame.stack_cursor is None:\n'
                                   '    return first_replace(frame, distance=original.distance, '
                                   'offset_x=original.offset_x, offset_y=original.offset_y, '
                                   'choice=original.choice, controller=original.controller if include_source '
                                   'else frame.controller)\n'
                                   'stack = frame.stack_cursor\n'
                                   'values = tuple((stack.long(index * 4) for index in range(4)))\n'
                                   'frame = first_replace(frame, distance=values[0], offset_x=values[1], '
                                   'offset_y=values[2], choice=values[3])\n'
                                   'if include_source:\n'
                                   '    frame = first_replace(frame, '
                                   'controller=memory.cursor_at(stack.long(16)))\n'
                                   'return first_replace(frame, stack_cursor=stack.advance(20 if '
                                   'include_source else 16))'},
 '_glyph_row_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                         'continuation: Long',
                            'returns': 'FirstDeploymentFrame',
                            'flow': 'if continuation not in (44730, 44736, 44856):\n'
                                    "    raise ValueError('real glyph-row return token required')\n"
                                    'entered = frame\n'
                                    'if frame.stack_cursor is not None:\n'
                                    '    stack = frame.stack_cursor.advance(-4)\n'
                                    '    stack.set_long(0, continuation)\n'
                                    '    entered = first_replace(frame, stack_cursor=stack)\n'
                                    'result = expand_glyph_row_fields(memory, entered)\n'
                                    'if frame.stack_cursor is not None:\n'
                                    '    actual = result.stack_cursor.long()\n'
                                    '    if actual != continuation:\n'
                                    '        raise SceneRefreshBoundary(44804, result, continuation)\n'
                                    '    result = first_replace(result, '
                                    'stack_cursor=result.stack_cursor.advance(4))\n'
                                    'return memory.sync_status(result)'},
 '_glyph_save_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                     'include_source: bool',
                        'returns': 'FirstDeploymentFrame',
                        'flow': 'if frame.stack_cursor is None:\n'
                                '    return frame\n'
                                'values = (frame.choice, frame.offset_y, frame.offset_x, frame.distance)\n'
                                'if include_source:\n'
                                '    values = (frame.controller.base,) + values\n'
                                'return _scene_render_push_longs(memory, frame, values)'},
 '_glyph_shift_long_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, '
                                           'amount: Word',
                              'returns': 'FirstDeploymentFrame',
                              'flow': 'original = frame.carrier(name)\n'
                                      'if original is None:\n'
                                      '    raise SceneRefreshBoundary(44812, frame, None)\n'
                                      'value = u32(original << amount)\n'
                                      'carry = bool(original & 1 << 32 - amount)\n'
                                      'status = (17 if carry else 0) | (8 if value & 2147483648 else 0) | (4 '
                                      'if value == 0 else 0)\n'
                                      'return memory.sync_status(first_replace(frame, status=status, '
                                      '**{name: value}))'},
 'decode_glyph_rows_to_buffers': {'signature': 'state: SceneState, source: Cursor, destination: Cursor, '
                                               'background: Long, foreground: Long, remaining: Long, saved: '
                                               'GlyphSavedValues | None=None',
                                  'returns': 'GlyphRowsResult',
                                  'flow': 'from .business_reuse import _save_glyph_values, '
                                          '_restore_glyph_values\n'
                                          'checked_state(state)\n'
                                          'checked_cursor(source, state)\n'
                                          'checked_cursor(destination, state)\n'
                                          'for value in (background, foreground, remaining):\n'
                                          '    uint(value, 32)\n'
                                          'if saved is not None:\n'
                                          '    _save_glyph_values(state, saved, True)\n'
                                          'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                          'target_x=background, target_y=foreground, count=remaining, '
                                          'roster=source.advance(0), candidates=destination.advance(0))\n'
                                          'actual = '
                                          'decode_glyph_rows_to_buffers_fields(SceneRefreshMemory(state), '
                                          'frame)\n'
                                          'source.base, destination.base = (actual.roster.base, '
                                          'actual.candidates.base)\n'
                                          'if saved is not None:\n'
                                          '    saved = _restore_glyph_values(state, saved, '
                                          'saved.glyph_source, True)\n'
                                          'return GlyphRowsResult(source, destination, actual.count, '
                                          'actual.target_x, actual.target_y, saved)'},
 'decode_glyph_rows_to_buffers_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                      'FirstDeploymentFrame',
                                         'returns': 'FirstDeploymentFrame',
                                         'flow': 'memory.frame(frame)\n'
                                                 'if any((value is None for value in (frame.roster, '
                                                 'frame.candidates, frame.target_x, frame.target_y, '
                                                 'frame.count))):\n'
                                                 '    raise SceneRefreshBoundary(44682, frame, None)\n'
                                                 'original = frame\n'
                                                 'frame = _glyph_save_fields(memory, frame, True)\n'
                                                 'remaining = low16(frame.count)\n'
                                                 'row_longs = 16\n'
                                                 'while True:\n'
                                                 '    token = frame.roster.word()\n'
                                                 '    frame = first_replace(frame, '
                                                 'roster=frame.roster.advance(2))\n'
                                                 "    frame = _first_word(frame, 'distance', token)\n"
                                                 '    if not negative_word(token):\n'
                                                 "        frame = _first_word(frame, 'offset_x', token)\n"
                                                 '        high = token & 65280\n'
                                                 "        frame = _first_word(frame, 'offset_x', high)\n"
                                                 "        frame = _first_shift_word(frame, 'offset_x', high, "
                                                 '3)\n'
                                                 '        low = token & 255\n'
                                                 "        frame = _first_word(frame, 'distance', low)\n"
                                                 "        frame = _first_shift_word(frame, 'distance', low, "
                                                 '5)\n'
                                                 '        offset = u16(low << 5) | u16(high << 3)\n'
                                                 "        frame = _first_word(frame, 'distance', offset)\n"
                                                 "        frame = _first_long(frame, 'distance', offset)\n"
                                                 '        frame = first_replace(frame, '
                                                 'controller=memory.cursor_at(529820 + offset))\n'
                                                 "        frame = _first_word(frame, 'offset_x', row_longs - "
                                                 '1)\n'
                                                 '        for index in range(row_longs):\n'
                                                 '            frame = _glyph_row_call_fields(memory, frame, '
                                                 '44730)\n'
                                                 '            frame = _scene_refresh_emit(memory, frame, '
                                                 'frame.candidates.base, 4, frame.choice)\n'
                                                 '            frame = _glyph_row_call_fields(memory, frame, '
                                                 '44736)\n'
                                                 '            frame = _scene_refresh_emit(memory, frame, '
                                                 'frame.candidates.base + 64, 4, frame.choice)\n'
                                                 '            frame = first_replace(frame, '
                                                 'candidates=frame.candidates.advance(4))\n'
                                                 '            frame = _scene_refresh_decrement(frame, '
                                                 "'offset_x', row_longs - 1 - index)\n"
                                                 '    else:\n'
                                                 "        frame = _first_long(frame, 'offset_y', 0)\n"
                                                 "        frame = _first_long(frame, 'choice', 0)\n"
                                                 '        nibbles = 8\n'
                                                 "        frame = _first_word(frame, 'distance', nibbles - "
                                                 '1)\n'
                                                 '        for index in range(nibbles):\n'
                                                 '            frame = _glyph_shift_long_fields(memory, '
                                                 "frame, 'offset_y', 4)\n"
                                                 '            frame = _glyph_shift_long_fields(memory, '
                                                 "frame, 'choice', 4)\n"
                                                 "            frame = _first_word(frame, 'offset_y', "
                                                 'low16(frame.offset_y) | low16(frame.target_x))\n'
                                                 "            frame = _first_word(frame, 'choice', "
                                                 'low16(frame.choice) | low16(frame.target_y))\n'
                                                 '            frame = _scene_refresh_decrement(frame, '
                                                 "'distance', nibbles - 1 - index)\n"
                                                 "        frame = _first_word(frame, 'distance', row_longs - "
                                                 '1)\n'
                                                 '        for index in range(row_longs):\n'
                                                 '            frame = _scene_refresh_emit(memory, frame, '
                                                 'frame.candidates.base + 64, 4, frame.offset_y)\n'
                                                 '            destination = frame.candidates\n'
                                                 '            frame = first_replace(frame, '
                                                 'candidates=destination.advance(4))\n'
                                                 '            frame = _scene_refresh_emit(memory, frame, '
                                                 'destination.base, 4, frame.offset_y)\n'
                                                 '            frame = _scene_refresh_decrement(frame, '
                                                 "'distance', row_longs - 1 - index)\n"
                                                 '        frame = _scene_refresh_emit(memory, frame, '
                                                 'frame.candidates.base - 36, 4, frame.choice)\n'
                                                 '        frame = _scene_refresh_emit(memory, frame, '
                                                 'frame.candidates.base + 28, 4, frame.choice)\n'
                                                 '    frame = first_replace(frame, '
                                                 'candidates=frame.candidates.advance(64))\n'
                                                 "    frame = _scene_refresh_decrement(frame, 'count', "
                                                 'remaining)\n'
                                                 '    remaining = u16(remaining - 1)\n'
                                                 '    if remaining == 65535:\n'
                                                 '        return '
                                                 'memory.sync_status(_glyph_restore_fields(memory, frame, '
                                                 'original, True))'},
 'expand_glyph_row_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                             'returns': 'FirstDeploymentFrame',
                             'flow': 'memory.frame(frame)\n'
                                     'if frame.target_x is None or frame.target_y is None or '
                                     'frame.controller is None:\n'
                                     '    raise SceneRefreshBoundary(44804, frame, None)\n'
                                     "frame = _first_long(frame, 'choice', 0)\n"
                                     'bits = frame.controller.byte()\n'
                                     'frame = first_replace(frame, controller=frame.controller.advance(1))\n'
                                     "frame = _first_byte(frame, 'offset_y', bits)\n"
                                     'row_bits = 8\n'
                                     "frame = _first_word(frame, 'distance', row_bits - 1)\n"
                                     'for index in range(row_bits):\n'
                                     "    frame = _glyph_shift_long_fields(memory, frame, 'choice', 4)\n"
                                     '    carry = bool(bits & 128)\n'
                                     '    bits = u8(bits << 1 | bool(frame.status & 16))\n'
                                     '    carrier = None if frame.offset_y is None else '
                                     'replace_byte(frame.offset_y, bits)\n'
                                     '    status = (17 if carry else 0) | (8 if bits & 128 else 0) | (4 if '
                                     'bits == 0 else 0)\n'
                                     '    frame = first_replace(frame, offset_y=carrier, status=status)\n'
                                     '    color = low8(frame.target_y) if carry else low8(frame.target_x)\n'
                                     "    frame = _first_byte(frame, 'choice', low8(frame.choice) | color)\n"
                                     "    frame = _scene_refresh_decrement(frame, 'distance', row_bits - 1 - "
                                     'index)\n'
                                     'return memory.sync_status(frame)'},
 'expand_glyph_stream_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                'returns': 'FirstDeploymentFrame',
                                'flow': 'memory.frame(frame)\n'
                                        'if any((value is None for value in (frame.roster, frame.candidates, '
                                        'frame.target_x, frame.target_y, frame.count))):\n'
                                        '    raise SceneRefreshBoundary(44830, frame, None)\n'
                                        'original = frame\n'
                                        'frame = _glyph_save_fields(memory, frame, False)\n'
                                        'remaining = low16(frame.count)\n'
                                        'while True:\n'
                                        "    frame = _first_word(frame, 'distance', 0)\n"
                                        '    token = frame.roster.byte()\n'
                                        '    frame = first_replace(frame, roster=frame.roster.advance(1))\n'
                                        "    frame = _first_byte(frame, 'distance', token)\n"
                                        "    frame = _first_shift_word(frame, 'distance', token, 3)\n"
                                        '    frame = first_replace(frame, controller=memory.cursor_at(562908 '
                                        '+ (token << 3)))\n'
                                        '    rows = 8\n'
                                        "    frame = _first_word(frame, 'offset_x', rows - 1)\n"
                                        '    for index in range(rows):\n'
                                        '        frame = _glyph_row_call_fields(memory, frame, 44856)\n'
                                        '        destination = frame.candidates\n'
                                        '        frame = first_replace(frame, '
                                        'candidates=destination.advance(4))\n'
                                        '        frame = _scene_refresh_emit(memory, frame, '
                                        'destination.base, 4, frame.choice)\n'
                                        "        frame = _scene_refresh_decrement(frame, 'offset_x', rows - "
                                        '1 - index)\n'
                                        "    frame = _scene_refresh_decrement(frame, 'count', remaining)\n"
                                        '    remaining = u16(remaining - 1)\n'
                                        '    if remaining == 65535:\n'
                                        '        return memory.sync_status(_glyph_restore_fields(memory, '
                                        'frame, original, False))'}})

DECLARATIONS.update({'write_vdp_dictionary_repeat_stream': {'signature': 'state: SceneState, source: Cursor, dictionary: Table, remaining: Word', 'returns': 'DictionaryStreamResult', 'flow': 'checked_state(state)\nchecked_cursor(source, state)\nchecked_table(dictionary, state)\nuint(remaining, 16)\nframe = first_replace(FirstDeploymentFrame.unobserved(), target_x=remaining, roster=source.advance(0), candidates=dictionary.cursor())\nframe = write_vdp_dictionary_repeat_stream_fields(SceneRefreshMemory(state), frame)\nsource.base = frame.roster.base\nreturn DictionaryStreamResult(source, frame.controller, low16(frame.target_x))'}})

DECLARATIONS.update({'_dictionary_stream_take_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, carrier: str', 'returns': 'tuple[FirstDeploymentFrame, bool]', 'flow': "from ..high_level_main_flows.business_movement_support import _movement_move, _movement_test\nif carrier not in ('target_y', 'count'):\n    raise ValueError('closed dictionary token or repeat-value role required')\nframe = _movement_test(memory.state, frame, low8(frame.unit), 8)\nfrom_dictionary = not bool(frame.status & 4)\nsource = frame.controller if from_dictionary else frame.roster\nvalue = source.word()\nif from_dictionary:\n    frame = first_replace(frame, controller=source.advance(2))\nelse:\n    frame = first_replace(frame, roster=source.advance(2))\nframe = _movement_move(memory.state, frame, carrier, value, 16)\nif from_dictionary:\n    frame, remaining = _movement_binary_flags(memory.state, frame, low8(frame.unit), 1, 8, True)\n    frame = first_replace(frame, unit=replace_byte(frame.unit, remaining))\nelse:\n    frame, remaining = _movement_binary_flags(memory.state, frame, low16(frame.target_x), 1, 16, True)\n    frame = first_replace(frame, target_x=replace_word(frame.target_x, remaining))\nreturn (frame, from_dictionary)"}})

DECLARATIONS.update({'_dictionary_stream_finished_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'tuple[FirstDeploymentFrame, bool]', 'flow': 'from ..high_level_main_flows.business_movement_support import _movement_test\nframe = _movement_test(memory.state, frame, low8(frame.unit), 8)\nif not frame.status & 4:\n    return (frame, False)\nframe = _movement_test(memory.state, frame, low16(frame.target_x), 16)\nreturn (frame, bool(frame.status & 8))'}})

DECLARATIONS.update({'write_vdp_dictionary_repeat_stream_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_movement_support import _movement_frame, _movement_move\nframe = _movement_frame(memory.state, frame)\nmemory.frame(frame)\nframe = _movement_move(memory.state, frame, 'unit', 0, 8)\nframe = first_replace(frame, auxiliary=memory.cursor_at(12582912))\nwhile True:\n    frame, unused_origin = _dictionary_stream_take_fields(memory, frame, 'target_y')\n    frame = _movement_compare(memory.state, frame, low16(frame.target_y), 65024, 16)\n    if frame.status & 1:\n        frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, low16(frame.target_y))\n        frame, finished = _dictionary_stream_finished_fields(memory, frame)\n        if finished:\n            return memory.sync_status(frame)\n        continue\n    frame = _movement_compare(memory.state, frame, low16(frame.target_y), 65280, 16)\n    if frame.status & 1:\n        frame = _movement_move(memory.state, frame, 'target_y', low16(frame.target_y) & 255, 16)\n        frame = memory.sync_status(_first_shift_word(frame, 'target_y', low16(frame.target_y), 2))\n        frame = first_replace(frame, controller=frame.candidates.advance(s16(low16(frame.target_y))))\n        frame = _movement_compare(memory.state, frame, frame.controller.word(), 65280, 16)\n        expand_pair = not bool(frame.status & 1)\n        if not expand_pair:\n            frame = _movement_compare(memory.state, frame, frame.controller.word(), 65024, 16)\n            expand_pair = bool(frame.status & 1)\n        if expand_pair:\n            frame = _movement_move(memory.state, frame, 'unit', 2, 8)\n        else:\n            frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, frame.controller.word())\n        continue\n    frame = _movement_move(memory.state, frame, 'target_y', low16(frame.target_y) & 255, 16)\n    frame, from_dictionary = _dictionary_stream_take_fields(memory, frame, 'count')\n    if not from_dictionary:\n        frame = _movement_compare(memory.state, frame, low16(frame.count), 65280, 16)\n        if frame.status & 1:\n            frame = _movement_compare(memory.state, frame, low16(frame.count), 65024, 16)\n            if not frame.status & 1:\n                frame = _movement_move(memory.state, frame, 'count', low16(frame.count) & 255, 16)\n                frame = memory.sync_status(_first_shift_word(frame, 'count', low16(frame.count), 2))\n                frame = first_replace(frame, controller=frame.candidates.advance(s16(low16(frame.count))))\n                value = frame.controller.word()\n                frame = first_replace(frame, controller=frame.controller.advance(2))\n                frame = _movement_move(memory.state, frame, 'count', value, 16)\n                frame = _movement_move(memory.state, frame, 'unit', 1, 8)\n    while True:\n        frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, low16(frame.count))\n        frame = _scene_refresh_decrement(frame, 'target_y', low16(frame.target_y))\n        if low16(frame.target_y) == 65535:\n            break\n    frame, finished = _dictionary_stream_finished_fields(memory, frame)\n    if finished:\n        return memory.sync_status(frame)"}})

APPROVED.setdefault('business_movement_support',set()).update({'_movement_frame','_movement_move','_movement_test'})

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
DECLARATIONS.update({'_vdp_packet_spill_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                           'vertical: bool',
                              'returns': 'FirstDeploymentFrame',
                              'flow': 'if type(vertical) is not bool:\n'
                                      "    raise ValueError('actual packet direction required')\n"
                                      'mask, shift = (8191, 7) if vertical else (127, 1)\n'
                                      "frame = memory.sync_status(_first_word(frame, 'count', "
                                      'low16(frame.unit)))\n'
                                      "frame = memory.sync_status(_first_word(frame, 'count', "
                                      'low16(frame.count) & mask))\n'
                                      "frame = _scene_mode_lsr_word(memory, frame, 'count', "
                                      'low16(frame.count), shift)\n'
                                      "frame = _scene_render_arithmetic(memory, frame, 'count', "
                                      'low16(frame.count), low16(frame.target_x), 16)\n'
                                      'total = low16(frame.count)\n'
                                      "frame = _scene_render_arithmetic(memory, frame, 'count', total, 64, "
                                      '16, True)\n'
                                      'if total < 64:\n'
                                      "    frame = memory.sync_status(_first_word(frame, 'count', 0))\n"
                                      "return _scene_render_arithmetic(memory, frame, 'target_x', "
                                      'low16(frame.target_x), low16(frame.count), 16, True)'},
 '_write_vdp_packet_run_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                               'carrier: str, recheck_tail: bool',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': "if carrier not in ('target_x', 'count') or type(recheck_tail) is "
                                          'not bool:\n'
                                          "    raise ValueError('closed original packet loop role "
                                          "required')\n"
                                          'while True:\n'
                                          '    remaining = low16(frame.carrier(carrier))\n'
                                          '    frame = _scene_render_compare(memory, frame, remaining, 8, '
                                          '16)\n'
                                          '    if remaining >= 8:\n'
                                          '        for unused in range(8):\n'
                                          '            source = frame.roster\n'
                                          '            value = source.word()\n'
                                          '            frame = first_replace(frame, '
                                          'roster=source.advance(2))\n'
                                          '            frame = _scene_refresh_emit(memory, frame, '
                                          'frame.auxiliary.base, 2, value)\n'
                                          '        frame = _scene_render_arithmetic(memory, frame, carrier, '
                                          'remaining, 8, 16, True)\n'
                                          '        continue\n'
                                          '    while True:\n'
                                          '        source = frame.roster\n'
                                          '        value = source.word()\n'
                                          '        frame = first_replace(frame, roster=source.advance(2))\n'
                                          '        frame = _scene_refresh_emit(memory, frame, '
                                          'frame.auxiliary.base, 2, value)\n'
                                          '        frame = _scene_refresh_decrement(frame, carrier, '
                                          'remaining)\n'
                                          '        remaining = u16(remaining - 1)\n'
                                          '        if remaining == 65535:\n'
                                          '            return frame\n'
                                          '        if recheck_tail:\n'
                                          '            break'},
 'write_vdp_packet_stream': {'signature': 'state: SceneState, source: Cursor, values: PacketTransferValues | '
                                          'None=None',
                             'returns': 'VdpPacketResult',
                             'flow': 'checked_state(state)\n'
                                     'checked_cursor(source, state)\n'
                                     'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                     'roster=source.advance(0))\n'
                                     'if values is None:\n'
                                     '    raise SceneRefreshBoundary(44316, frame, None)\n'
                                     'if type(values) is not PacketTransferValues:\n'
                                     "    raise ValueError('actual packet stream values required')\n"
                                     'values.validate()\n'
                                     'frame = first_replace(frame, target_x=values.command, '
                                     'target_y=values.increment, unit=values.address, count=values.spill)\n'
                                     'frame = write_vdp_packet_stream_fields(SceneRefreshMemory(state), '
                                     'frame)\n'
                                     'source.base = frame.roster.base\n'
                                     'values = PacketTransferValues(frame.target_x, frame.target_y, '
                                     'frame.unit, frame.count).validate()\n'
                                     'return VdpPacketResult(source, frame.unit, low16(frame.target_y), '
                                     'values)'},
 'write_vdp_packet_stream_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'memory.frame(frame)\n'
                                            'if frame.roster is None or frame.target_x is None or '
                                            'frame.target_y is None or (frame.count is None):\n'
                                            '    raise SceneRefreshBoundary(44316, frame, None)\n'
                                            'while True:\n'
                                            '    frame = first_replace(frame, '
                                            'auxiliary=memory.cursor_at(12582912))\n'
                                            "    frame = memory.sync_status(_first_word(frame, 'target_y', "
                                            '36610))\n'
                                            '    source = frame.roster\n'
                                            '    count = source.word()\n'
                                            '    frame = first_replace(frame, roster=source.advance(2))\n'
                                            "    frame = memory.sync_status(_first_word(frame, 'target_x', "
                                            'count))\n'
                                            '    if count == 0:\n'
                                            '        return _scene_refresh_emit(memory, frame, 12582916, 2, '
                                            'low16(frame.target_y))\n'
                                            '    vertical = bool(count & 32768)\n'
                                            '    if vertical:\n'
                                            '        frame = memory.sync_status(_first_word(frame, '
                                            "'target_y', 36736))\n"
                                            '        frame = memory.sync_status(_first_word(frame, '
                                            "'target_x', count & 32767))\n"
                                            "    frame = memory.sync_status(_first_long(frame, 'unit', 0))\n"
                                            '    source = frame.roster\n'
                                            '    address = source.word()\n'
                                            '    frame = first_replace(frame, roster=source.advance(2))\n'
                                            "    frame = memory.sync_status(_first_word(frame, 'unit', "
                                            'address))\n'
                                            '    if vertical:\n'
                                            '        frame = _vdp_packet_spill_fields(memory, frame, True)\n'
                                            '    else:\n'
                                            "        frame = memory.sync_status(_first_word(frame, 'count', "
                                            '0))\n'
                                            '        frame = _scene_render_bit(memory, frame, '
                                            'frame.target_x, 16384)\n'
                                            '        if not count & 16384:\n'
                                            '            frame = _vdp_packet_spill_fields(memory, frame, '
                                            'False)\n'
                                            "    frame = memory.sync_status(_first_word(frame, 'target_x', "
                                            'low16(frame.target_x) & 49151))\n'
                                            "    frame = _scene_render_arithmetic(memory, frame, 'target_x', "
                                            'low16(frame.target_x), 1, 16, True)\n'
                                            '    frame = _scene_refresh_emit(memory, frame, 12582916, 2, '
                                            'low16(frame.target_y))\n'
                                            "    frame = _glyph_shift_long_fields(memory, frame, 'unit', 2)\n"
                                            "    frame = _scene_mode_lsr_word(memory, frame, 'unit', "
                                            'low16(frame.unit), 2)\n'
                                            "    frame = memory.sync_status(_first_word(frame, 'unit', "
                                            'low16(frame.unit) | 16384))\n'
                                            "    frame = memory.sync_status(_first_long(frame, 'unit', "
                                            'swap_words(frame.unit)))\n'
                                            '    frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                            'frame.unit)\n'
                                            '    frame = _write_vdp_packet_run_fields(memory, frame, '
                                            "'target_x', False)\n"
                                            '    spill = low16(frame.count)\n'
                                            '    frame = _scene_refresh_flags(memory, frame, spill, 2)\n'
                                            '    if spill == 0:\n'
                                            '        continue\n'
                                            '    frame = _scene_render_bit(memory, frame, frame.target_y, '
                                            '2)\n'
                                            '    mask = 4286644223 if frame.target_y & 2 else 3766484991\n'
                                            "    frame = memory.sync_status(_first_long(frame, 'unit', "
                                            'frame.unit & mask))\n'
                                            "    frame = _scene_render_arithmetic(memory, frame, 'count', "
                                            'spill, 1, 16, True)\n'
                                            '    frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                            'frame.unit)\n'
                                            '    frame = _write_vdp_packet_run_fields(memory, frame, '
                                            "'count', True)"}})

# B26 obsolete standalone packet loop removed; sole live run owns its logic.
DECLARATIONS.pop('_write_word_count',None)

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
APPROVED.setdefault('business_objects',set()).update({'_scene_controller_legacy_projection', '_scene_controller_legacy_fields'})
DECLARATIONS.update({'_read_vdp_plane_rle_rows_core': {'signature': 'state: SceneState, source: Cursor, video_address: VideoPlaneAddress, row_stride: Long, current: SceneControllerFrame | None=None', 'returns': 'PlaneStreamResult', 'flow': "checked_state(state)\nchecked_cursor(source, state)\n_video_address(video_address)\nuint(row_stride, 32)\nif current is None:\n    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=source.advance(0), candidates=SceneRefreshMemory(state).cursor_at(video_address.carrier), offset_x=row_stride)\nelse:\n    from .business_objects import _scene_controller_legacy_fields\n    frame = _scene_controller_legacy_fields(state, current)\n    if frame.offset_x != row_stride:\n        raise ValueError('actual live plane stride required')\nresult, discarded = _read_vdp_plane_rle_rows_fields_core(SceneRefreshMemory(state), frame)\nsource.base = result.roster.base\nlive = None\nif current is not None:\n    from .business_objects import _scene_controller_legacy_projection\n    live = _scene_controller_legacy_projection(state, result)\nreturn PlaneStreamResult(source, VideoPlaneAddress(result.candidates.base), result.target_x, low16(result.distance), low16(result.offset_y), discarded, live)"}, '_read_vdp_plane_rle_rows_fields_core': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, from_control: bool=False', 'returns': 'tuple', 'flow': "memory.frame(frame)\nif frame.stack_cursor is None:\n    raise SceneRefreshBoundary(240334, frame, None)\nmemory.sync_status(frame)\nif not from_control:\n    memory.state.read(4294934528, 2)\n    frame = _scene_refresh_emit(memory, frame, 4294934528, 2, 0)\n    frame = _first_word(frame, 'offset_y', 32)\nmemory.sync_status(frame)\nmemory.state.read(4294934530, 2)\nframe = _scene_refresh_emit(memory, frame, 4294934530, 2, 0)\nframe = _scene_refresh_emit(memory, frame, 12582916, 2, 36610)\nframe = _first_word(frame, 'target_x', low16(frame.candidates.base))\nframe = _scene_render_call_fields(memory, frame, 242352, 240360)\nframe = _first_long(frame, 'distance', 0)\nmemory.sync_status(frame)\nmode = memory.state.read(4294934530, 2)\nframe = _scene_refresh_flags(memory, frame, mode, 2)\nif mode == 0:\n    frame, marker = _scene_tile_byte_fields(memory, frame, 'target_y')\nwhile True:\n    frame, high = _scene_tile_byte_fields(memory, frame, 'unit')\n    memory.sync_status(frame)\n    mode = memory.state.read(4294934530, 2)\n    frame = _scene_refresh_flags(memory, frame, mode, 2)\n    marker = low8(frame.target_y)\n    if mode == 0:\n        frame = _scene_render_compare(memory, frame, marker, high, 8)\n    literal = mode != 0 or marker != high\n    if literal:\n        frame = _scene_render_asl_word(memory, frame, 'unit', low16(frame.unit), 8)\n        frame, low = _scene_tile_byte_fields(memory, frame, 'unit')\n        memory.sync_status(frame)\n        mask = memory.state.read(4294934528, 2)\n        frame = _first_word(frame, 'unit', low16(frame.unit) | mask)\n        frame = _scene_refresh_emit(memory, frame, 12582912, 2, low16(frame.unit))\n        frame, discarded = _scene_plane_row_call_fields(memory, frame, 240400)\n        if discarded is not None:\n            return (frame, discarded)\n    else:\n        frame = _first_long(frame, 'count', 0)\n        frame, count = _scene_tile_byte_fields(memory, frame, 'count')\n        if count == 0:\n            return (memory.sync_status(frame), None)\n        frame, high = _scene_tile_byte_fields(memory, frame, 'unit')\n        frame = _scene_render_asl_word(memory, frame, 'unit', low16(frame.unit), 8)\n        frame, low = _scene_tile_byte_fields(memory, frame, 'unit')\n        remaining = count\n        while True:\n            memory.sync_status(frame)\n            mask = memory.state.read(4294934528, 2)\n            frame = _first_word(frame, 'unit', low16(frame.unit) | mask)\n            frame = _scene_refresh_emit(memory, frame, 12582912, 2, low16(frame.unit))\n            frame, discarded = _scene_plane_row_call_fields(memory, frame, 240428)\n            if discarded is not None:\n                return (frame, discarded)\n            frame = _scene_refresh_decrement(frame, 'count', remaining)\n            remaining = u16(remaining - 1)\n            if remaining == 65535:\n                break"}, 'read_vdp_plane_rle_rows_from_control_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame, discarded = _read_vdp_plane_rle_rows_fields_core(memory, frame, True)\nreturn frame'}, '_scene_plane_row_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, continuation: Long', 'returns': 'tuple', 'flow': "if continuation not in (240400, 240428):\n    raise ValueError('original plane row continuation required')\nmemory.frame(frame)\nif frame.stack_cursor is None:\n    raise SceneRefreshBoundary(240434, frame, continuation)\nmemory.sync_status(frame)\nframe = _scene_render_push_longs(memory, frame, (continuation,))\nreturned, discarded = advance_plane_row_fields(memory, frame)\nif discarded is not None:\n    return (returned, discarded)\nactual = returned.stack_cursor.long()\nif actual != continuation:\n    raise SceneRefreshBoundary(240434, returned, continuation)\nreturned = first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))\nreturn (memory.sync_status(returned), None)"}, '_scene_render_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long, video: Word | None=None', 'returns': 'FirstDeploymentFrame', 'flow': "memory.frame(frame)\nif (target, continuation) not in ((239454, 235174), (235096, 235378), (235096, 235426), (242352, 235108), (242352, 240360), (242352, 240462), (242352, 240478), (239406, 235520), (235992, 236214), (239008, 236284), (239438, 236290), (239500, 239450), (235992, 235668), (239008, 235716), (239008, 235794), (239438, 235800), (239522, 236372), (239522, 236400), (239008, 236462), (239522, 236668), (235992, 236690), (239008, 236722), (239522, 236844), (235992, 236850), (239008, 236900), (235992, 236950), (239008, 236980), (239522, 237080), (239008, 238190), (239522, 238294), (235992, 238374), (239008, 238404), (239522, 238508), (239522, 238636), (239522, 238680), (235992, 238686), (239008, 238716), (239522, 238756), (239522, 238784), (239522, 238824), (239522, 238852), (239522, 238892), (239522, 238034), (239522, 238002), (235992, 237134), (239008, 237164), (237336, 237218), (235992, 237244), (239008, 237274), (237706, 237428), (239522, 237450), (235992, 237468), (237706, 237474), (239008, 237500), (235992, 237586), (237706, 237592), (239008, 237618)):\n    raise ValueError('actual renderer child and return token required')\nmemory.sync_status(frame)\nentered = frame\nif frame.stack_cursor is not None:\n    stack = frame.stack_cursor.advance(-4)\n    stack.set_long(0, continuation)\n    entered = first_replace(frame, stack_cursor=stack)\nif target == 239454:\n    result = clear_scene_sprite_chain_heads_fields(memory, entered)\nelif target == 235096:\n    result = write_vdp_word_rle_stream_fields(memory, entered, video)\nelif target == 242352:\n    result = set_vram_write_address_fields(memory, entered, video)\nelif target == 239406:\n    result = append_scene_marker_sprite_fields(memory, entered)\nelif target == 235992:\n    result = update_scripted_scene_position_fields(memory, entered)\nelif target == 239008:\n    result = append_clipped_scene_sprites_fields(memory, entered)\nelif target == 239522:\n    result = append_unclipped_scene_sprites_fields(memory, entered)\nelif target == 237336:\n    result = initialize_scripted_secondary_position_fields(memory, entered)\nelif target == 237706:\n    result = select_scene_object_frame_fields(memory, entered)\nelif target == 239438:\n    result = finish_scene_sprite_chains_fields(memory, entered)\nelse:\n    result = finish_one_scene_sprite_chain_fields(memory, entered)\nmemory.frame(result)\nif frame.stack_cursor is not None:\n    actual = result.stack_cursor.long()\n    if actual != continuation:\n        raise SceneRefreshBoundary(target, result, continuation)\n    result = first_replace(result, stack_cursor=result.stack_cursor.advance(4))\nreturn memory.sync_status(result)"}, '_scene_tile_byte_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name', 'returns': 'tuple', 'flow': 'memory.sync_status(frame)\nvalue = frame.roster.byte()\nframe = first_replace(frame, roster=frame.roster.advance(1))\nreturn (_first_byte(frame, name, value), value)'}, '_write_vdp_swapped_byte_rle_core': {'signature': 'state: SceneState, source: Cursor, video_address: VideoPlaneAddress, current: SceneControllerFrame | None=None', 'returns': 'SwappedByteRleObservation', 'flow': 'checked_state(state)\nchecked_cursor(source, state)\n_video_address(video_address)\nif current is None:\n    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=source.advance(0), target_x=video_address.carrier)\nelse:\n    from .business_objects import _scene_controller_legacy_fields\n    frame = _scene_controller_legacy_fields(state, current)\nresult, marker, token, last_word = _write_vdp_swapped_byte_rle_fields_core(SceneRefreshMemory(state), frame)\nsource.base = result.roster.base\nlive = None\nif current is not None:\n    from .business_objects import _scene_controller_legacy_projection\n    live = _scene_controller_legacy_projection(state, result)\nreturn SwappedByteRleObservation(source, video_address, result.target_x, marker, token, last_word, live)'}, '_write_vdp_swapped_byte_rle_fields_core': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': "memory.frame(frame)\nif frame.roster is None or frame.target_x is None:\n    raise SceneRefreshBoundary(240466, frame, None)\nframe = _scene_refresh_emit(memory, frame, 12582916, 2, 36610)\nframe = _scene_render_call_fields(memory, frame, 242352, 240478)\nframe, marker = _scene_tile_byte_fields(memory, frame, 'target_y')\nlast_word = None\nwhile True:\n    frame, low = _scene_tile_byte_fields(memory, frame, 'unit')\n    frame = _scene_render_compare(memory, frame, marker, low, 8)\n    if marker != low:\n        frame, high = _scene_tile_byte_fields(memory, frame, 'distance')\n        previous = None if frame.distance is None else low16(frame.distance)\n        frame = _scene_render_asl_word(memory, frame, 'distance', previous, 8)\n        frame = _first_byte(frame, 'distance', low)\n        last_word = high << 8 | low\n        frame = _scene_refresh_emit(memory, frame, 12582912, 2, last_word)\n    else:\n        frame = _first_long(frame, 'count', 0)\n        frame, count = _scene_tile_byte_fields(memory, frame, 'count')\n        if count == 0:\n            return (memory.sync_status(frame), marker, low, last_word)\n        frame, low = _scene_tile_byte_fields(memory, frame, 'unit')\n        frame, high = _scene_tile_byte_fields(memory, frame, 'distance')\n        previous = None if frame.distance is None else low16(frame.distance)\n        frame = _scene_render_asl_word(memory, frame, 'distance', previous, 8)\n        frame = _first_byte(frame, 'distance', low)\n        last_word = high << 8 | low\n        remaining = count\n        while True:\n            frame = _scene_refresh_emit(memory, frame, 12582912, 2, last_word)\n            frame = _scene_refresh_decrement(frame, 'count', remaining)\n            remaining = u16(remaining - 1)\n            if remaining == 65535:\n                break"}, 'advance_plane_row': {'signature': 'state: SceneState, context: PlaneRowContext, current: SceneControllerFrame | None=None', 'returns': 'PlaneRowResult', 'flow': 'checked_context(context, PlaneRowContext, state)\nif current is None:\n    frame = first_replace(FirstDeploymentFrame.unobserved(), target_x=context.command_carrier, candidates=SceneRefreshMemory(state).cursor_at(context.video_address.carrier), offset_x=context.row_stride)\nelse:\n    from .business_objects import _scene_controller_legacy_fields\n    frame = _scene_controller_legacy_fields(state, current)\nresult, discarded = advance_plane_row_fields(SceneRefreshMemory(state), frame)\nlive = None\nif current is not None:\n    from .business_objects import _scene_controller_legacy_projection\n    live = _scene_controller_legacy_projection(state, result)\nreturn PlaneRowResult(VideoPlaneAddress(result.candidates.base), low16(result.distance), low16(result.offset_y), result.target_x, discarded, live)'}, 'advance_plane_row_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': "memory.frame(frame)\nif frame.stack_cursor is None:\n    raise SceneRefreshBoundary(240434, frame, None)\nframe = _scene_render_arithmetic(memory, frame, 'distance', low16(frame.distance), 1, 16)\ncolumn = low16(frame.distance)\nframe = _scene_render_compare(memory, frame, low8(column), 32, 8)\nif low8(column) >= 32:\n    frame = _scene_render_arithmetic(memory, frame, 'offset_y', low16(frame.offset_y), 1, 16, True)\n    if low16(frame.offset_y) == 0:\n        memory.sync_status(frame)\n        discarded = frame.stack_cursor.long()\n        frame = first_replace(frame, target_x=discarded, stack_cursor=frame.stack_cursor.advance(4))\n        return (memory.sync_status(frame), StackContinuation(discarded))\n    frame = first_replace(frame, candidates=memory.cursor_at(u32(frame.candidates.base + frame.offset_x)))\n    frame = _first_word(frame, 'target_x', low16(frame.candidates.base))\n    frame = _scene_render_call_fields(memory, frame, 242352, 240462)\n    frame = _first_long(frame, 'distance', 0)\nreturn (memory.sync_status(frame), None)"}, 'read_vdp_plane_rle_rows_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame, discarded = _read_vdp_plane_rle_rows_fields_core(memory, frame)\nreturn frame'}, 'write_vdp_swapped_byte_rle_stream_complete': {'signature': 'state: SceneState, source: Cursor, video_address: VideoPlaneAddress, retained: SwappedByteRleRetained', 'returns': 'SwappedByteRleResult', 'flow': "checked_state(state)\nchecked_cursor(source, state)\n_video_address(video_address)\nif type(retained) is not SwappedByteRleRetained:\n    raise ValueError('actual partial-write observations required')\nretained.validate()\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=source.advance(0), target_x=video_address.carrier, unit=retained.token, distance=retained.packed_word)\nresult, marker, token, last_word = _write_vdp_swapped_byte_rle_fields_core(SceneRefreshMemory(state), frame)\nsource.base = result.roster.base\nreturn SwappedByteRleResult(source, video_address, result.target_x, replace_byte(retained.marker, marker), result.unit, result.count, result.distance, last_word, False, True, False, False)"}, 'write_vdp_swapped_byte_rle_stream_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'result, marker, token, last_word = _write_vdp_swapped_byte_rle_fields_core(memory, frame)\nreturn result'}})

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
APPROVED.setdefault('business_objects',set()).update({'_scene_controller_legacy_fields', '_scene_controller_legacy_projection'})
DECLARATIONS.update({'_begin_scene_palette_darken_core': {'signature': 'state: SceneState, value: Long',
                                      'returns': 'tuple[Long, Word]',
                                      'flow': 'checked_state(state)\n'
                                              'uint(value, 32)\n'
                                              'frame, shade = '
                                              '_begin_scene_palette_darken_fields_core(SceneRefreshMemory(state), '
                                              'first_replace(FirstDeploymentFrame.unobserved(), '
                                              'target_x=value))\n'
                                              'return (frame.target_x, shade)'},
 '_begin_scene_palette_darken_fields_core': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                          'FirstDeploymentFrame',
                                             'returns': 'tuple',
                                             'flow': 'memory.frame(frame)\n'
                                                     'if frame.target_x is None:\n'
                                                     '    raise SceneRefreshBoundary(240160, frame, None)\n'
                                                     "frame = _first_word(frame, 'target_x', "
                                                     'low16(frame.target_x) & 255)\n'
                                                     'frame = _scene_refresh_emit(memory, frame, 4294934724, '
                                                     '2, low16(frame.target_x))\n'
                                                     'frame = _scene_refresh_emit(memory, frame, 4294934726, '
                                                     '2, 0)\n'
                                                     'shade = 15\n'
                                                     'return (_scene_refresh_emit(memory, frame, 4294934728, '
                                                     '2, shade), shade)'},
 '_copy_scene_palette_variant_fields': {'signature': 'state: SceneState, variant: Long, count_carrier: Long '
                                                     '| None',
                                        'returns': 'PaletteCopyFields',
                                        'flow': 'checked_state(state)\n'
                                                'uint(variant, 32)\n'
                                                'if count_carrier is not None:\n'
                                                '    uint(count_carrier, 32)\n'
                                                'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                                'target_x=variant, choice=count_carrier)\n'
                                                'frame, pair = '
                                                '_copy_scene_palette_variant_fields_core(SceneRefreshMemory(state), '
                                                'frame)\n'
                                                'return PaletteCopyFields(frame.target_x, frame.controller, '
                                                'frame.scan, frame.candidates, frame.choice, '
                                                'pair).validate(state)'},
 '_copy_scene_palette_variant_fields_core': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                          'FirstDeploymentFrame',
                                             'returns': 'tuple',
                                             'flow': 'memory.frame(frame)\n'
                                                     'if frame.target_x is None:\n'
                                                     '    raise SceneRefreshBoundary(240532, frame, None)\n'
                                                     'frame = first_replace(frame, '
                                                     'candidates=memory.cursor_at(240556))\n'
                                                     "frame = _first_shift_word(frame, 'target_x', "
                                                     'low16(frame.target_x), 3)\n'
                                                     'frame = first_replace(frame, '
                                                     'candidates=frame.candidates.advance(s16(low16(frame.target_x))))\n'
                                                     'memory.sync_status(frame)\n'
                                                     'pointer = frame.candidates.long()\n'
                                                     'frame = first_replace(frame, '
                                                     'controller=memory.cursor_at(pointer), '
                                                     'candidates=frame.candidates.advance(4))\n'
                                                     'pointer = frame.candidates.word()\n'
                                                     'frame = first_replace(frame, '
                                                     'scan=memory.cursor_at(u32(s16(pointer))), '
                                                     'candidates=frame.candidates.advance(2))\n'
                                                     'counter = frame.candidates.word()\n'
                                                     'frame = first_replace(frame, '
                                                     'candidates=frame.candidates.advance(2))\n'
                                                     "frame = _first_word(frame, 'choice', counter)\n"
                                                     'while True:\n'
                                                     '    memory.sync_status(frame)\n'
                                                     '    pair = frame.controller.long()\n'
                                                     '    frame.scan.set_long(0, pair)\n'
                                                     '    frame = _scene_refresh_flags(memory, frame, pair, '
                                                     '4)\n'
                                                     '    frame = first_replace(frame, '
                                                     'controller=frame.controller.advance(4), '
                                                     'scan=frame.scan.advance(4))\n'
                                                     "    frame = _scene_refresh_decrement(frame, 'choice', "
                                                     'counter)\n'
                                                     '    counter = u16(counter - 1)\n'
                                                     '    if counter == 65535:\n'
                                                     '        return (memory.sync_status(frame), pair)'},
 'begin_scene_palette_darken_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'frame, shade = '
                                               '_begin_scene_palette_darken_fields_core(memory, frame)\n'
                                               'return frame'},
 'begin_scene_palette_darken_frame': {'signature': 'state: SceneState, frame: SceneControllerFrame',
                                      'returns': 'SceneControllerFrame',
                                      'flow': 'from .business_objects import '
                                              '_scene_controller_legacy_fields, '
                                              '_scene_controller_legacy_projection\n'
                                              'fields = '
                                              'begin_scene_palette_darken_fields(SceneRefreshMemory(state), '
                                              '_scene_controller_legacy_fields(state, frame))\n'
                                              'return _scene_controller_legacy_projection(state, fields)'},
 'copy_scene_palette_variant_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'frame, pair = '
                                               '_copy_scene_palette_variant_fields_core(memory, frame)\n'
                                               'return frame'},
 'snapshot_and_clear_scene_palette': {'signature': 'state: SceneState',
                                      'returns': 'PaletteSnapshotResult',
                                      'flow': 'checked_state(state)\n'
                                              'frame = '
                                              'snapshot_and_clear_scene_palette_fields(SceneRefreshMemory(state), '
                                              'FirstDeploymentFrame.unobserved())\n'
                                              'return PaletteSnapshotResult(frame.roster, frame.candidates)'},
 'snapshot_and_clear_scene_palette_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                          'FirstDeploymentFrame',
                                             'returns': 'FirstDeploymentFrame',
                                             'flow': 'memory.frame(frame)\n'
                                                     'longs = 32\n'
                                                     "frame = _first_long(frame, 'target_y', longs - 1)\n"
                                                     'frame = first_replace(frame, '
                                                     'roster=memory.cursor_at(4294966016), '
                                                     'candidates=memory.cursor_at(4294966144))\n'
                                                     'counter = longs - 1\n'
                                                     'while True:\n'
                                                     '    memory.sync_status(frame)\n'
                                                     '    pair = frame.roster.long()\n'
                                                     '    frame.candidates.set_long(0, pair)\n'
                                                     '    frame = _scene_refresh_flags(memory, frame, pair, '
                                                     '4)\n'
                                                     '    frame = first_replace(frame, '
                                                     'candidates=frame.candidates.advance(4))\n'
                                                     '    frame.roster.long()\n'
                                                     '    frame.roster.set_long(0, 0)\n'
                                                     '    frame = _scene_refresh_flags(memory, frame, 0, 4)\n'
                                                     '    frame = first_replace(frame, '
                                                     'roster=frame.roster.advance(4))\n'
                                                     '    frame = _scene_refresh_decrement(frame, '
                                                     "'target_y', counter)\n"
                                                     '    counter = u16(counter - 1)\n'
                                                     '    if counter == 65535:\n'
                                                     '        return memory.sync_status(frame)'},
 'snapshot_and_clear_scene_palette_frame': {'signature': 'state: SceneState, frame: SceneControllerFrame',
                                            'returns': 'SceneControllerFrame',
                                            'flow': 'from .business_objects import '
                                                    '_scene_controller_legacy_fields, '
                                                    '_scene_controller_legacy_projection\n'
                                                    'fields = '
                                                    'snapshot_and_clear_scene_palette_fields(SceneRefreshMemory(state), '
                                                    '_scene_controller_legacy_fields(state, frame))\n'
                                                    'return _scene_controller_legacy_projection(state, '
                                                    'fields)'}})


# Root48 complete live palette source; ordinary native lowerers unchanged.
DECLARATIONS.update({'darken_palette_component': {'signature': 'state: SceneState, shade: Long, color: Long, accumulated: Long, component: Long=0', 'returns': 'PaletteComponentResult', 'flow': 'checked_state(state)\nfor value in (shade, color, accumulated, component):\n    uint(value, 32)\nframe = first_replace(FirstDeploymentFrame.unobserved(), target_x=shade, unit=color, count=component, distance=accumulated)\nframe = darken_palette_component_fields(SceneRefreshMemory(state), frame)\nreturn PaletteComponentResult(frame.unit, frame.distance, frame.count).validate(state)'}, 'darken_palette': {'signature': 'state: SceneState, shade: Long, count: Word, source: Cursor, accumulator: Long=0, *, count_carrier: Long | None=None, color: Long=0, component: Long=0', 'returns': 'PaletteTransformResult', 'flow': "checked_state(state)\nchecked_cursor(source, state)\nfor value in (shade, accumulator, color, component):\n    uint(value, 32)\nuint(count, 16)\nif count_carrier is not None:\n    uint(count_carrier, 32)\n    if low16(count_carrier) != count:\n        raise ValueError('palette count must agree with actual caller')\nframe = first_replace(FirstDeploymentFrame.unobserved(), target_x=shade, target_y=count_carrier, unit=color, count=component, distance=accumulator, roster=source.advance(0))\nframe = darken_palette_fields(SceneRefreshMemory(state), frame)\nsource.base = frame.roster.base\nreturn PaletteTransformResult(source, frame.candidates, frame.target_x, frame.distance, frame.target_y, frame.unit, frame.count).validate(state)"}, 'darken_palette_component_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "memory.frame(frame)\nif any((value is None for value in (frame.target_x, frame.unit, frame.count, frame.distance, frame.status))):\n    raise SceneRefreshBoundary(57076, frame, None)\nframe = _first_shift_word(frame, 'distance', low16(frame.distance), 4)\ncolor = _rol_word(frame.unit, 4)\nflags = (8 if low16(color) & 32768 else 0) | (4 if low16(color) == 0 else 0) | low16(color) & 1\nframe = first_replace(frame, unit=color, status=frame.status & 16 | flags)\nmemory.sync_status(frame)\nframe = _first_byte(frame, 'count', low8(frame.unit))\nframe = _first_word(frame, 'count', low16(frame.count) & 14)\nframe, value = _movement_binary_flags(memory.state, frame, low8(frame.count), low8(frame.target_x), 8, True)\nframe = first_replace(frame, count=replace_byte(frame.count, value))\nif frame.status & 1:\n    frame = _first_byte(frame, 'count', 0)\nreturn memory.sync_status(_first_word(frame, 'distance', low16(frame.distance) | low16(frame.count)))"}, '_darken_palette_component_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_gameplay_flow.business_battle import _presentation_call_fields\nfrom ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory\nif continuation not in (57040, 57044, 57048):\n    raise ValueError('original darken component return required')\ndef child(actual, entered):\n    return darken_palette_component_fields(SceneRefreshMemory(actual.state), entered)\nreturn _presentation_call_fields(BattlePresentationMemory(memory.state), frame, continuation, child)"}, 'darken_palette_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "memory.frame(frame)\nif any((value is None for value in (frame.target_x, frame.target_y, frame.unit, frame.count, frame.distance, frame.roster, frame.stack_cursor, frame.status))):\n    raise SceneRefreshBoundary(56998, frame, None)\nshade_ceiling = 15\nframe = _movement_compare(memory.state, frame, low16(frame.target_x), shade_ceiling, 16)\nif low16(frame.target_x) > shade_ceiling:\n    raise SceneRefreshBoundary(57004, frame, 'original shade WORD above15 loops here')\nframe = first_replace(frame, candidates=memory.cursor_at(4294966016))\npresent = bool(frame.target_x & 1)\nframe = first_replace(frame, status=frame.status & 27 | (0 if present else 4))\nif present:\n    present = bool(memory.state.read(4294964000, 1) & 1)\n    frame = first_replace(frame, status=frame.status & 27 | (0 if present else 4))\n    if present:\n        from ..high_level_main_flows.business_movement_support import _movement_add_word\n        frame = _movement_add_word(memory.state, frame, 'target_x', 1)\npresent = bool(frame.target_x & 1)\nframe = first_replace(frame, target_x=frame.target_x & 4294967294, status=frame.status & 27 | (0 if present else 4))\nwhile True:\n    frame = _first_word(frame, 'distance', 0)\n    memory.sync_status(frame)\n    color = frame.roster.word()\n    frame = first_replace(frame, roster=frame.roster.advance(2))\n    frame = _first_word(frame, 'unit', color)\n    frame = _first_shift_word(frame, 'unit', low16(frame.unit), 4)\n    for continuation in (57040, 57044, 57048):\n        frame = _darken_palette_component_call_fields(memory, frame, continuation)\n    value = low16(frame.distance)\n    frame.candidates.set_word(0, value)\n    frame = _scene_refresh_flags(memory, frame, value, 2)\n    frame = first_replace(frame, candidates=frame.candidates.advance(2))\n    counter = u16(low16(frame.target_y) - 1)\n    frame = first_replace(frame, target_y=replace_word(frame.target_y, counter))\n    if counter == 65535:\n        break\nprevious = memory.state.read(4294963998, 2)\nframe, value = _movement_binary_flags(memory.state, frame, previous, 1, 16)\nmemory.state.write(4294963998, 2, value)\nmemory.sync_status(frame)\nframe = _first_word(frame, 'target_x', memory.state.read(4294966016, 2))\nfor destination in (4294966048, 4294966080, 4294966112):\n    frame = _scene_refresh_emit(memory, frame, destination, 2, low16(frame.target_x))\nreturn memory.sync_status(frame)"}})
APPROVED.setdefault('business_battle',set()).add('_presentation_call_fields')
APPROVED.setdefault('contexts_battle',set()).add('BattlePresentationMemory')
APPROVED.setdefault('business_movement_support',set()).add('_movement_add_word')

# B31 sole object roster/label/random fields; ordinary native lowerers unchanged.
APPROVED.setdefault('business_formation',set()).update({'first_deployment_random_fields'})
APPROVED.setdefault('contexts_policy_memory',set()).update({'BattlePolicyMemory'})
APPROVED.setdefault('business_battle',set()).update({'_presentation_call_fields'})
APPROVED.setdefault('contexts_battle',set()).update({'BattlePresentationMemory'})
APPROVED.setdefault('business_objects',set()).update({'_scene_controller_legacy_fields', '_scene_controller_legacy_projection'})
DECLARATIONS.update({'sample_random_preserving_seed_carrier': {'signature': 'state: SceneState',
                                           'returns': 'Long',
                                           'flow': 'checked_state(state)\n'
                                                   'return '
                                                   'sample_random_preserving_seed_fields(SceneRefreshMemory(state), '
                                                   'FirstDeploymentFrame.unobserved()).target_x'},
 'sample_random_preserving_seed_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                       'FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'from ..high_level_battle_ai.business_formation import '
                                                  'first_deployment_random_fields\n'
                                                  'from ..high_level_battle_ai.contexts_policy_memory import '
                                                  'BattlePolicyMemory\n'
                                                  'from ..high_level_gameplay_flow.business_battle import '
                                                  '_presentation_call_fields\n'
                                                  'from ..high_level_gameplay_flow.contexts_battle import '
                                                  'BattlePresentationMemory\n'
                                                  'memory.frame(frame)\n'
                                                  'retained_secondary = frame.target_y\n'
                                                  'frame = _scene_render_push_longs(memory, frame, '
                                                  '(retained_secondary,))\n'
                                                  'def child(actual_memory, entered):\n'
                                                  '    return '
                                                  'first_deployment_random_fields(BattlePolicyMemory(actual_memory.state), '
                                                  'entered)\n'
                                                  'frame = '
                                                  '_presentation_call_fields(BattlePresentationMemory(memory.state), '
                                                  'frame, 243500, child)\n'
                                                  'if frame.stack_cursor is not None:\n'
                                                  '    retained_secondary = frame.stack_cursor.long()\n'
                                                  '    frame = first_replace(frame, '
                                                  'stack_cursor=frame.stack_cursor.advance(4))\n'
                                                  'return memory.sync_status(first_replace(frame, '
                                                  'target_y=retained_secondary))'},
 'sample_random_preserving_seed_frame': {'signature': 'state: SceneState, frame: SceneControllerFrame',
                                         'returns': 'SceneControllerFrame',
                                         'flow': 'from .business_objects import '
                                                 '_scene_controller_legacy_fields, '
                                                 '_scene_controller_legacy_projection\n'
                                                 'fields = '
                                                 'sample_random_preserving_seed_fields(SceneRefreshMemory(state), '
                                                 '_scene_controller_legacy_fields(state, frame))\n'
                                                 'return _scene_controller_legacy_projection(state, fields)'}})

# B32 sole object rendering/integration/actor-chain fields; ordinary native lowerers unchanged.
APPROVED.setdefault('business_objects',set()).update({'_scene_controller_legacy_projection', '_scene_controller_legacy_fields'})
APPROVED.setdefault('business_battle',set()).update({'_presentation_call_fields'})
APPROVED.setdefault('contexts_battle',set()).update({'BattlePresentationMemory'})
DECLARATIONS.update({'_finish_actor_sprite_chains_core': {'signature': 'state: SceneState, current: SceneControllerFrame | '
                                                   'None=None',
                                      'returns': 'Long | SceneControllerFrame',
                                      'flow': 'checked_state(state)\n'
                                              'if current is None:\n'
                                              '    fields = FirstDeploymentFrame.unobserved()\n'
                                              'else:\n'
                                              '    from .business_objects import '
                                              '_scene_controller_legacy_fields\n'
                                              '    fields = _scene_controller_legacy_fields(state, current)\n'
                                              'actual = '
                                              'finish_actor_sprite_chains_fields(SceneRefreshMemory(state), '
                                              'fields)\n'
                                              'if current is None:\n'
                                              '    return actual.target_x\n'
                                              'from .business_objects import '
                                              '_scene_controller_legacy_projection\n'
                                              'return _scene_controller_legacy_projection(state, actual)'},
 'finish_actor_sprite_chains_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'from ..high_level_gameplay_flow.business_battle import '
                                               '_presentation_call_fields\n'
                                               'from ..high_level_gameplay_flow.contexts_battle import '
                                               'BattlePresentationMemory\n'
                                               'memory.frame(frame)\n'
                                               "frame = _first_long(frame, 'target_x', 28)\n"
                                               "frame = _first_long(frame, 'target_y', 0)\n"
                                               'frame = first_replace(frame, '
                                               'roster=memory.cursor_at(4294934596))\n'
                                               'def child(actual_memory, entered):\n'
                                               '    return '
                                               'finish_one_actor_sprite_chain_fields(SceneRefreshMemory(actual_memory.state), '
                                               'entered)\n'
                                               'while True:\n'
                                               '    frame = '
                                               '_presentation_call_fields(BattlePresentationMemory(memory.state), '
                                               'frame, 242246, child)\n'
                                               '    frame = _scene_render_arithmetic(memory, frame, '
                                               "'target_x', low16(frame.target_x), 4, 16, True)\n"
                                               '    if low16(frame.target_x) & 32768:\n'
                                               '        break\n'
                                               "frame = _first_long(frame, 'target_x', 0)\n"
                                               'for displacement in (0, 4, 8, 12, 16, 20, 24, 28):\n'
                                               '    frame = _scene_refresh_emit(memory, frame, '
                                               'u32(frame.roster.base + displacement), 4, frame.target_x)\n'
                                               'return _scene_refresh_emit(memory, frame, 4294963968, 1, 0)'},
 'finish_one_actor_sprite_chain': {'signature': 'state: SceneState, heads: Table, layer: Word, next_link: '
                                                'Long, current: SceneControllerFrame | None=None',
                                   'returns': 'Long | SceneControllerFrame',
                                   'flow': 'checked_state(state)\n'
                                           'checked_table(heads, state)\n'
                                           'uint(layer, 16)\n'
                                           'uint(next_link, 32)\n'
                                           'if current is None:\n'
                                           '    fields = first_replace(FirstDeploymentFrame.unobserved(), '
                                           'roster=heads.cursor(), target_y=next_link)\n'
                                           'else:\n'
                                           '    from .business_objects import '
                                           '_scene_controller_legacy_fields\n'
                                           '    fields = _scene_controller_legacy_fields(state, current)\n'
                                           '    fields = first_replace(fields, roster=heads.cursor(), '
                                           'target_x=replace_word(fields.target_x, layer), '
                                           'target_y=next_link)\n'
                                           'actual = '
                                           'finish_one_actor_sprite_chain_fields(SceneRefreshMemory(state), '
                                           'fields)\n'
                                           'if current is None:\n'
                                           '    return actual.target_y\n'
                                           'from .business_objects import '
                                           '_scene_controller_legacy_projection\n'
                                           'return _scene_controller_legacy_projection(state, actual)'},
 'finish_one_actor_sprite_chain_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                       'FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'if frame.target_x is None:\n'
                                                  '    raise SceneRefreshBoundary(242290, frame, None)\n'
                                                  'return finish_one_scene_sprite_chain_fields(memory, '
                                                  'frame)'}})

# B33 sole palette/action/overlap fields; ordinary native lowerers unchanged.
APPROVED.setdefault('business_objects',set()).update({'_scene_controller_legacy_projection', '_object_shift_word_right_fields', '_scene_controller_legacy_fields', '_object_adjust_word_fields'})
APPROVED.setdefault('business_battle',set()).update({'_presentation_call_fields'})
APPROVED.setdefault('contexts_battle',set()).update({'BattlePresentationMemory'})
APPROVED.setdefault('business_movement_support',set()).update({'_movement_binary_flags'})
DECLARATIONS.update({'_advance_scene_palette_fade_core': {'signature': 'state: SceneState, retained: Long, current: '
                                                   'SceneControllerFrame | None=None',
                                      'returns': 'Long | SceneControllerFrame',
                                      'flow': 'from .business_objects import '
                                              '_scene_controller_legacy_fields, '
                                              '_scene_controller_legacy_projection\n'
                                              'checked_state(state)\n'
                                              'uint(retained, 32)\n'
                                              'fields = first_replace(FirstDeploymentFrame.unobserved(), '
                                              'target_x=retained) if current is None else '
                                              '_scene_controller_legacy_fields(state, current)\n'
                                              'actual = '
                                              'advance_scene_palette_fade_fields(SceneRefreshMemory(state), '
                                              'fields)\n'
                                              'return actual.target_x if current is None else '
                                              '_scene_controller_legacy_projection(state, actual)'},
 '_scene_fade_rotate_word_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                                 'name: str, amount: Word',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'original = frame.carrier(name)\n'
                                            'if original is None:\n'
                                            '    raise SceneRefreshBoundary(240154, frame, None)\n'
                                            'result = _ror_word(original, amount)\n'
                                            'flags = (8 if low16(result) & 32768 else 0) | (4 if '
                                            'low16(result) == 0 else 0)\n'
                                            'if low16(original) & 1 << amount - 1:\n'
                                            '    flags |= 1\n'
                                            'status = None if frame.status is None else frame.status & 16 | '
                                            'flags\n'
                                            'return memory.sync_status(first_replace(frame, **{name: '
                                            'result}, status=status))'},
 'advance_scene_palette_fade_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'from ..high_level_gameplay_flow.business_battle import '
                                               '_presentation_call_fields\n'
                                               'from ..high_level_gameplay_flow.contexts_battle import '
                                               'BattlePresentationMemory\n'
                                               'from .business_objects import _object_adjust_word_fields\n'
                                               'memory.frame(frame)\n'
                                               'memory.sync_status(frame)\n'
                                               'mode = memory.state.read(4294934724, 2)\n'
                                               "frame = _first_word(frame, 'target_x', mode)\n"
                                               'if mode & 32768:\n'
                                               '    return frame\n'
                                               'frame = _object_adjust_word_fields(memory, frame, '
                                               '4294934726, 1, True)\n'
                                               'if not frame.status & 8:\n'
                                               '    return frame\n'
                                               'period = mode & 255\n'
                                               "frame = _first_word(frame, 'target_x', period)\n"
                                               'frame = _scene_refresh_emit(memory, frame, 4294934726, 2, '
                                               'period)\n'
                                               'mode_byte = memory.state.read(4294934724, 1)\n'
                                               'frame = _scene_render_compare(memory, frame, mode_byte, 0, '
                                               '8)\n'
                                               'if mode_byte == 0:\n'
                                               '    frame = _object_adjust_word_fields(memory, frame, '
                                               '4294934728, 1, True)\n'
                                               '    finished = bool(frame.status & 8)\n'
                                               'else:\n'
                                               '    frame = _object_adjust_word_fields(memory, frame, '
                                               '4294934728, 1)\n'
                                               '    shade = memory.state.read(4294934728, 2)\n'
                                               '    frame = _scene_render_compare(memory, frame, shade, 15, '
                                               '16)\n'
                                               '    finished = shade > 15\n'
                                               'if finished:\n'
                                               '    return _scene_refresh_emit(memory, frame, 4294934724, 2, '
                                               '65535)\n'
                                               'shade = memory.state.read(4294934728, 2)\n'
                                               "frame = _first_word(frame, 'target_x', shade)\n"
                                               "frame = _first_word(frame, 'target_x', shade & 14)\n"
                                               'frame = _scene_refresh_emit(memory, frame, 4294934528, 2, '
                                               'low16(frame.target_x))\n'
                                               'frame = first_replace(frame, '
                                               'roster=memory.cursor_at(4294966016), '
                                               'candidates=memory.cursor_at(4294966144), '
                                               'controller=memory.cursor_at(4294934730))\n'
                                               "frame = _first_long(frame, 'unit', 0)\n"
                                               "frame = _first_long(frame, 'choice', 0)\n"
                                               'while True:\n'
                                               "    frame = _first_long(frame, 'target_y', 31)\n"
                                               "    frame = _first_long(frame, 'offset_y', "
                                               'frame.controller.long(low16(frame.choice)))\n'
                                               '    while True:\n'
                                               '        mask = frame.offset_y\n'
                                               '        frame = first_replace(frame, offset_y=mask >> 1, '
                                               'status=(17 if mask & 1 else 0) | (4 if mask >> 1 == 0 else '
                                               '0))\n'
                                               '        memory.sync_status(frame)\n'
                                               '        if mask & 1:\n'
                                               "            frame = _first_word(frame, 'offset_x', 0)\n"
                                               "            frame = _first_word(frame, 'count', "
                                               'frame.candidates.word(low16(frame.unit)))\n'
                                               '            if frame.stack_cursor is None or any((value is '
                                               'None for value in (frame.count, frame.distance, '
                                               'frame.offset_x))):\n'
                                               '                raise SceneRefreshBoundary(240138, frame, '
                                               '240108)\n'
                                               '            for continuation in (240108, 240112, 240116):\n'
                                               '\n'
                                               '                def component(actual_memory, entered):\n'
                                               '                    return '
                                               'fade_palette_component_fields(SceneRefreshMemory(actual_memory.state), '
                                               'entered)\n'
                                               '                frame = '
                                               '_presentation_call_fields(BattlePresentationMemory(memory.state), '
                                               'frame, continuation, component)\n'
                                               '            frame = _scene_fade_rotate_word_fields(memory, '
                                               "frame, 'offset_x', 4)\n"
                                               '            frame = _scene_refresh_emit(memory, frame, '
                                               'u32(frame.roster.base + s16(low16(frame.unit))), 2, '
                                               'low16(frame.offset_x))\n'
                                               '        frame = _scene_render_arithmetic(memory, frame, '
                                               "'unit', low16(frame.unit), 2, 16)\n"
                                               "        frame = _scene_refresh_decrement(frame, 'target_y')\n"
                                               '        if low16(frame.target_y) == 65535:\n'
                                               '            break\n'
                                               '    frame = _scene_render_arithmetic(memory, frame, '
                                               "'choice', low16(frame.choice), 4, 16)\n"
                                               '    frame = _scene_render_compare(memory, frame, '
                                               'low16(frame.choice), 8, 16)\n'
                                               '    if low16(frame.choice) >= 8:\n'
                                               '        return memory.sync_status(frame)'},
 'fade_palette_component': {'signature': 'state: SceneState, color: Long, accumulated: Long, component: '
                                         'Long=0',
                            'returns': 'PaletteComponentResult',
                            'flow': 'actual = fade_palette_component_fields(SceneRefreshMemory(state), '
                                    'first_replace(FirstDeploymentFrame.unobserved(), count=color, '
                                    'distance=component, offset_x=accumulated))\n'
                                    'return PaletteComponentResult(actual.count, actual.offset_x, '
                                    'actual.distance).validate(state)'},
 'fade_palette_component_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': "from .business_objects import _object_shift_word_right_fields\nmemory.frame(frame)\nif any((value is None for value in (frame.count, frame.distance, frame.offset_x))):\n    raise SceneRefreshBoundary(240138, frame, None)\nframe = _first_byte(frame, 'distance', low8(frame.count))\nframe = _first_word(frame, 'distance', low16(frame.distance) & 14)\nmemory.sync_status(frame)\nshade = memory.state.read(4294934529, 1)\nframe, value = _movement_binary_flags(memory.state, frame, low8(frame.distance), shade, 8, True)\nframe = first_replace(frame, distance=replace_byte(frame.distance, value))\nif frame.status & 1:\n    frame = _first_long(frame, 'distance', 0)\nframe = _first_word(frame, 'offset_x', low16(frame.offset_x) | low16(frame.distance))\nframe = _scene_fade_rotate_word_fields(memory, frame, 'offset_x', 4)\nframe, shifted_color = _object_shift_word_right_fields(memory, frame, 'count', low16(frame.count), 4)\nreturn memory.sync_status(frame)"}})

DECLARATIONS.update({'flush_scene_transfer_queue_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_remaining_flows.business_city import _resource_cost_frame\nfrom ..high_level_main_flows.business_movement_support import _movement_test\nfrom ..high_level_gameplay_flow.business_battle import _presentation_call_fields\nfrom ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory\nif type(memory) is not SceneRefreshMemory:\n    raise ValueError('actual same Scene transfer memory required')\nstate = memory.state\nframe = _resource_cost_frame(state, frame, 44294)\nframe = _movement_test(state, frame, state.read(4294955264, 2), 16)\nif not frame.status & 4:\n    frame = first_replace(frame, roster=memory.cursor_at(4294955264))\n\n    def child(actual, entered):\n        return write_vdp_packet_stream_fields(SceneRefreshMemory(actual.state), entered)\n    frame = _presentation_call_fields(BattlePresentationMemory(state), frame, 44306, child)\nfor address in (4294963994, 4294955264):\n    state.read(address, 2)\n    state.write(address, 2, 0)\n    frame = _movement_test(state, frame, 0, 16)\nreturn frame"}})

DECLARATIONS.update({'flush_scene_transfer_queue': {'signature': 'state: SceneState, values: PacketTransferValues | None=None', 'returns': 'VdpPacketResult | None', 'flow': "checked_state(state)\nframe = FirstDeploymentFrame.unobserved()\nif values is not None:\n    if type(values) is not PacketTransferValues:\n        raise ValueError('actual packet flush values required')\n    values.validate()\n    frame = first_replace(frame, target_x=values.command, target_y=values.increment, unit=values.address, count=values.spill)\nflush_scene_transfer_queue_fields(SceneRefreshMemory(state), frame)\nraise SceneRefreshBoundary(44294, frame, None)"}})

APPROVED.setdefault('business_city',set()).add('_resource_cost_frame')
APPROVED.setdefault('business_movement_support',set()).add('_movement_test')
APPROVED.setdefault('business_battle',set()).add('_presentation_call_fields')
APPROVED.setdefault('contexts_battle',set()).add('BattlePresentationMemory')

# Full palette field DECL: explicit actual DBRA WORD counter only.
DECLARATIONS.update({'advance_scene_palette_fade_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_gameplay_flow.business_battle import _presentation_call_fields\nfrom ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory\nfrom .business_objects import _object_adjust_word_fields\nmemory.frame(frame)\nmemory.sync_status(frame)\nmode = memory.state.read(4294934724, 2)\nframe = _first_word(frame, 'target_x', mode)\nif mode & 32768:\n    return frame\nframe = _object_adjust_word_fields(memory, frame, 4294934726, 1, True)\nif not frame.status & 8:\n    return frame\nperiod = mode & 255\nframe = _first_word(frame, 'target_x', period)\nframe = _scene_refresh_emit(memory, frame, 4294934726, 2, period)\nmode_byte = memory.state.read(4294934724, 1)\nframe = _scene_render_compare(memory, frame, mode_byte, 0, 8)\nif mode_byte == 0:\n    frame = _object_adjust_word_fields(memory, frame, 4294934728, 1, True)\n    finished = bool(frame.status & 8)\nelse:\n    frame = _object_adjust_word_fields(memory, frame, 4294934728, 1)\n    shade = memory.state.read(4294934728, 2)\n    frame = _scene_render_compare(memory, frame, shade, 15, 16)\n    finished = shade > 15\nif finished:\n    return _scene_refresh_emit(memory, frame, 4294934724, 2, 65535)\nshade = memory.state.read(4294934728, 2)\nframe = _first_word(frame, 'target_x', shade)\nframe = _first_word(frame, 'target_x', shade & 14)\nframe = _scene_refresh_emit(memory, frame, 4294934528, 2, low16(frame.target_x))\nframe = first_replace(frame, roster=memory.cursor_at(4294966016), candidates=memory.cursor_at(4294966144), controller=memory.cursor_at(4294934730))\nframe = _first_long(frame, 'unit', 0)\nframe = _first_long(frame, 'choice', 0)\nwhile True:\n    frame = _first_long(frame, 'target_y', 31)\n    frame = _first_long(frame, 'offset_y', frame.controller.long(low16(frame.choice)))\n    while True:\n        mask = frame.offset_y\n        frame = first_replace(frame, offset_y=mask >> 1, status=(17 if mask & 1 else 0) | (4 if mask >> 1 == 0 else 0))\n        memory.sync_status(frame)\n        if mask & 1:\n            frame = _first_word(frame, 'offset_x', 0)\n            frame = _first_word(frame, 'count', frame.candidates.word(low16(frame.unit)))\n            if frame.stack_cursor is None or any((value is None for value in (frame.count, frame.distance, frame.offset_x))):\n                raise SceneRefreshBoundary(240138, frame, 240108)\n            for continuation in (240108, 240112, 240116):\n\n                def component(actual_memory, entered):\n                    return fade_palette_component_fields(SceneRefreshMemory(actual_memory.state), entered)\n                frame = _presentation_call_fields(BattlePresentationMemory(memory.state), frame, continuation, component)\n            frame = _scene_fade_rotate_word_fields(memory, frame, 'offset_x', 4)\n            frame = _scene_refresh_emit(memory, frame, u32(frame.roster.base + s16(low16(frame.unit))), 2, low16(frame.offset_x))\n        frame = _scene_render_arithmetic(memory, frame, 'unit', low16(frame.unit), 2, 16)\n        frame = _scene_refresh_decrement(frame, 'target_y', low16(frame.target_y))\n        if low16(frame.target_y) == 65535:\n            break\n    frame = _scene_render_arithmetic(memory, frame, 'choice', low16(frame.choice), 4, 16)\n    frame = _scene_render_compare(memory, frame, low16(frame.choice), 8, 16)\n    if low16(frame.choice) >= 8:\n        return memory.sync_status(frame)"}})

# C53 selected complete source bodies; fixed-default editing NOT_AVAILABLE.
DECLARATIONS.update({'_story_move_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, value: '
                                     'Long, width: Word=16',
                        'returns': 'FirstDeploymentFrame',
                        'flow': 'from ..high_level_dynamic_flows.business_early_phase import '
                                '_allocation_move_fields\n'
                                'return _allocation_move_fields(memory, frame, name, value, width)'},
 '_story_read_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, address: '
                                     'Long, size: Word=2',
                        'returns': '',
                        'flow': 'memory.sync_status(frame)\nreturn memory.state.read(address, size)'},
 '_story_ram_move_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, '
                                         'low: Word, width: Word=16',
                            'returns': 'FirstDeploymentFrame',
                            'flow': 'return _story_move_fields(memory, frame, name, '
                                    '_story_read_fields(memory, frame, 4294901760 | low, width // 8), '
                                    'width)'},
 '_story_store_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, address: '
                                      'Long, value: Long, size: Word=2',
                         'returns': 'FirstDeploymentFrame',
                         'flow': 'return _scene_refresh_emit(memory, frame, address, size, value)'},
 '_story_clear_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, low: Word',
                         'returns': 'FirstDeploymentFrame',
                         'flow': 'from .business_objects import _object_clear_word_fields\n'
                                 'return _object_clear_word_fields(memory, frame, 4294901760 | low)'},
 '_story_add_ram_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, low: Word, '
                                        'amount: Word=1',
                           'returns': 'FirstDeploymentFrame',
                           'flow': 'from .business_objects import _object_adjust_word_fields\n'
                                   'return _object_adjust_word_fields(memory, frame, 4294901760 | low, '
                                   'amount)'},
 '_story_compare_ram_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, low: '
                                            'Word, value: Word',
                               'returns': 'FirstDeploymentFrame',
                               'flow': 'return _scene_render_compare(memory, frame, '
                                       '_story_read_fields(memory, frame, 4294901760 | low), value, 16)'},
 '_story_arithmetic_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, '
                                           'value: Word, subtract: bool=False',
                              'returns': 'FirstDeploymentFrame',
                              'flow': 'return _scene_render_arithmetic(memory, frame, name, '
                                      'low16(frame.carrier(name)), value, 16, subtract)'},
 '_story_status_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, value: Word',
                          'returns': 'FirstDeploymentFrame',
                          'flow': 'memory.state.set_status_word(value)\n'
                                  'return first_replace(frame, status=value & 31)'},
 '_story_mask_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name, mask: '
                                     'Word, width: Word=16',
                        'returns': 'FirstDeploymentFrame',
                        'flow': 'return _story_move_fields(memory, frame, name, frame.carrier(name) & mask & '
                                '(1 << width) - 1, width)'},
 '_story_palette_masks_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                              'masks: tuple',
                                 'returns': 'FirstDeploymentFrame',
                                 'flow': 'if len(masks) != 4:\n'
                                         "    raise ValueError('four original palette masks required')\n"
                                         'for index, value in enumerate(masks):\n'
                                         '    frame = _story_store_fields(memory, frame, 4294934730 + index '
                                         '* 2, value)\n'
                                         'return frame'},
 '_story_clear_plane_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                               'returns': 'FirstDeploymentFrame',
                               'flow': 'from ..high_level_dynamic_flows.business_early_phase import '
                                       '_allocation_fill_fields\n'
                                       'return _allocation_fill_fields(memory, frame, 1610612738, 13107, '
                                       '3455, True)'},
 '_story_script_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, source: '
                                       'Long, dimensions: bool=False',
                          'returns': 'FirstDeploymentFrame',
                          'flow': 'frame = _story_store_fields(memory, frame, 16740364, 40960)\n'
                                  'frame = _story_store_fields(memory, frame, 16740366, source, 4)\n'
                                  'if dimensions:\n'
                                  '    frame = _story_store_fields(memory, frame, 16740372, 3)\n'
                                  '    frame = _story_store_fields(memory, frame, 16740374, 1)\n'
                                  'return frame'},
 '_story_finish_stage_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                             'counters: tuple=(33082,)',
                                'returns': 'FirstDeploymentFrame',
                                'flow': 'for low in counters:\n'
                                        '    frame = _story_clear_fields(memory, frame, low)\n'
                                        'return _story_add_ram_fields(memory, frame, 33002)'},
 '_story_pressed_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                           'returns': 'tuple',
                           'flow': 'value = _story_read_fields(memory, frame, 4294934724, 1)\n'
                                   'return (_scene_render_bit(memory, frame, value, 128), bool(value & '
                                   '128))'},
 '_story_lighten_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                        'continuation: Long',
                           'returns': 'FirstDeploymentFrame',
                           'flow': "frame = _story_move_fields(memory, frame, 'target_x', 1, 32)\n"
                                   'return _story_call_fields(memory, frame, 240184, continuation)'},
 '_story_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, '
                                     'continuation: Long',
                        'returns': 'FirstDeploymentFrame',
                        'flow': 'memory.frame(frame)\n'
                                'memory.sync_status(frame)\n'
                                'entered = _scene_render_push_longs(memory, frame, (continuation,))\n'
                                'result = _story_known_fields(memory, entered, target)\n'
                                'memory.frame(result)\n'
                                'if frame.stack_cursor is not None:\n'
                                '    actual = result.stack_cursor.long()\n'
                                '    if actual != continuation:\n'
                                '        raise SceneRefreshBoundary(target, result, continuation)\n'
                                '    result = first_replace(result, '
                                'stack_cursor=result.stack_cursor.advance(4))\n'
                                'return memory.sync_status(result)'},
 '_story_decode_picture_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                               'source: Long, continuation: Long',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': 'frame = first_replace(frame, roster=memory.cursor_at(source), '
                                          'candidates=memory.cursor_at(57344))\n'
                                          "frame = _story_move_fields(memory, frame, 'offset_x', 128, 32)\n"
                                          "frame = _story_move_fields(memory, frame, 'offset_y', 18)\n"
                                          'return _story_call_fields(memory, frame, 240334, continuation)'},
 '_story_glyph_upload_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, rows: '
                                             'Word',
                                'returns': 'FirstDeploymentFrame',
                                'flow': 'frame = first_replace(frame, auxiliary=memory.cursor_at(12582912))\n'
                                        "frame = _story_move_fields(memory, frame, 'target_x', rows)\n"
                                        'return _story_upload_current_rows_fields(memory, frame)'},
 '_story_initialize_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, scene',
                              'returns': 'FirstDeploymentFrame',
                              'flow': 'memory.frame(frame)\n'
                                      "if scene == 'prologue':\n"
                                      '    masks, palette_return, row_return, source = ((65535, 0, 65535, '
                                      '65535), 243714, None, 242904)\n'
                                      "elif scene == 'departure':\n"
                                      '    masks, palette_return, row_return, source = ((65535,) * 4, '
                                      '246238, 246242, 243080)\n'
                                      "elif scene == 'interlude':\n"
                                      '    masks, palette_return, row_return, source = ((65535,) * 4, '
                                      '248232, 248236, 243428)\n'
                                      "elif scene == 'arrival':\n"
                                      '    masks, palette_return, row_return, source = ((65535,) * 4, '
                                      '248550, None, 243220)\n'
                                      "elif scene == 'finale':\n"
                                      '    masks, palette_return, row_return, source = ((65535,) * 4, '
                                      '250298, None, None)\n'
                                      'else:\n'
                                      "    raise ValueError('closed story initialization role required')\n"
                                      "if scene != 'prologue':\n"
                                      '    frame = _story_status_fields(memory, frame, 9984)\n'
                                      'frame = _story_palette_masks_fields(memory, frame, masks)\n'
                                      "frame = _story_move_fields(memory, frame, 'target_x', 1, 32)\n"
                                      'frame = _story_call_fields(memory, frame, 240160, palette_return)\n'
                                      'if row_return is not None:\n'
                                      '    frame = _story_call_fields(memory, frame, 246330, row_return)\n'
                                      "if scene == 'prologue':\n"
                                      '    frame = _story_status_fields(memory, frame, 9984)\n'
                                      'frame = _story_clear_plane_fields(memory, frame)\n'
                                      'if source is None:\n'
                                      '    frame = _story_store_fields(memory, frame, 16740372, 3)\n'
                                      '    frame = _story_store_fields(memory, frame, 16740374, 1)\n'
                                      'else:\n'
                                      '    frame = _story_script_fields(memory, frame, source, True)\n'
                                      "if scene == 'prologue':\n"
                                      '    frame = _story_status_fields(memory, frame, 9472)\n'
                                      'else:\n'
                                      '    frame = _story_store_fields(memory, frame, 4294934844, 3)\n'
                                      'frame = _story_add_ram_fields(memory, frame, 33002)\n'
                                      "if scene != 'prologue':\n"
                                      '    frame = _story_status_fields(memory, frame, 9472)\n'
                                      'return memory.sync_status(frame)'},
 '_story_timer_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, threshold: '
                                      'Word, masks: tuple | None, fade_return: Long | None, source: Long | '
                                      'None, counters: tuple',
                         'returns': 'FirstDeploymentFrame',
                         'flow': 'frame = _story_add_ram_fields(memory, frame, 33082)\n'
                                 'frame = _story_compare_ram_fields(memory, frame, 33082, threshold)\n'
                                 'if frame.status & 1:\n'
                                 '    return frame\n'
                                 'if masks is not None:\n'
                                 '    frame = _story_palette_masks_fields(memory, frame, masks)\n'
                                 'if fade_return is not None:\n'
                                 '    frame = _story_lighten_fields(memory, frame, fade_return)\n'
                                 'if source is not None:\n'
                                 '    frame = _story_status_fields(memory, frame, 9984)\n'
                                 '    frame = _story_clear_plane_fields(memory, frame)\n'
                                 '    frame = _story_script_fields(memory, frame, source)\n'
                                 '    frame = _story_status_fields(memory, frame, 9472)\n'
                                 'return _story_finish_stage_fields(memory, frame, counters)'},
 '_story_caption_trigger_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                                'threshold: Word, source: Long',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'frame = _story_compare_ram_fields(memory, frame, 33082, '
                                           'threshold)\n'
                                           'if frame.status & 4:\n'
                                           '    frame = _story_status_fields(memory, frame, 9984)\n'
                                           '    frame = _story_clear_plane_fields(memory, frame)\n'
                                           '    frame = _story_script_fields(memory, frame, source)\n'
                                           '    frame = _story_status_fields(memory, frame, 9472)\n'
                                           'return frame'},
 '_story_confirm_page_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                             'picture: Long, picture_return: Long, source: Long',
                                'returns': 'tuple',
                                'flow': 'frame, pressed = _story_pressed_fields(memory, frame)\n'
                                        'if not pressed:\n'
                                        '    return (frame, False)\n'
                                        'frame = _story_status_fields(memory, frame, 9984)\n'
                                        'frame = _story_decode_picture_fields(memory, frame, picture, '
                                        'picture_return)\n'
                                        'frame = _story_clear_plane_fields(memory, frame)\n'
                                        'frame = _story_script_fields(memory, frame, source)\n'
                                        'return (_story_status_fields(memory, frame, 9472), True)'},
 '_story_exit_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                        'returns': 'FirstDeploymentFrame',
                        'flow': 'frame, pressed = _story_pressed_fields(memory, frame)\n'
                                'if pressed:\n'
                                '    return _story_known_fields(memory, frame, 518)\n'
                                'return memory.sync_status(frame)'},
 'initialize_prologue_story_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                      'returns': 'FirstDeploymentFrame',
                                      'flow': 'memory.frame(frame)\n'
                                              "return _story_initialize_fields(memory, frame, 'prologue')"},
 'initialize_departure_story_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'memory.frame(frame)\n'
                                               "return _story_initialize_fields(memory, frame, 'departure')"},
 'initialize_interlude_story_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'memory.frame(frame)\n'
                                               "return _story_initialize_fields(memory, frame, 'interlude')"},
 'initialize_arrival_story_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'memory.frame(frame)\n'
                                             "return _story_initialize_fields(memory, frame, 'arrival')"},
 'initialize_finale_story_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'memory.frame(frame)\n'
                                            "return _story_initialize_fields(memory, frame, 'finale')"},
 'reveal_prologue_caption_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'memory.frame(frame)\nframe = _story_call_fields(memory, frame, 243920, 243804)\nframe = _story_add_ram_fields(memory, frame, 33082)\nframe = _story_compare_ram_fields(memory, frame, 33082, 512)\nif frame.status & 1:\n    return frame\nframe = _story_palette_masks_fields(memory, frame, (0, 65535, 0, 0))\nframe = _story_darken_fields(memory, frame, 243846)\nframe = _story_status_fields(memory, frame, 9984)\nframe = _story_clear_plane_fields(memory, frame)\nframe = _story_script_fields(memory, frame, 242950)\nframe = _story_status_fields(memory, frame, 9472)\nreturn _story_finish_stage_fields(memory, frame, (33082,))'},
 'wait_prologue_portrait_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'memory.frame(frame)\n'
                                           'frame = _story_call_fields(memory, frame, 243920, 243942)\n'
                                           'return _story_timer_fields(memory, frame, 512, None, 243960, '
                                           'None, (33082,))'},
 'wait_prologue_second_page_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                      'returns': 'FirstDeploymentFrame',
                                      'flow': 'memory.frame(frame)\n'
                                              'frame = _story_call_fields(memory, frame, 243920, 244094)\n'
                                              'return _story_timer_fields(memory, frame, 512, None, 244112, '
                                              'None, (33082,))'},
 'reveal_prologue_second_portrait_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                         'FirstDeploymentFrame',
                                            'returns': 'FirstDeploymentFrame',
                                            'flow': 'memory.frame(frame)\n'
                                                    'frame = _story_call_fields(memory, frame, 243920, '
                                                    '244126)\n'
                                                    'return _story_timer_fields(memory, frame, 64, (65535, '
                                                    '65535, 0, 65535), 244168, None, (33082,))'},
 'begin_prologue_closing_caption_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                        'FirstDeploymentFrame',
                                           'returns': 'FirstDeploymentFrame',
                                           'flow': 'memory.frame(frame)\n'
                                                   'frame = _story_call_fields(memory, frame, 244400, '
                                                   '244310)\n'
                                                   'frame = _story_call_fields(memory, frame, 244454, '
                                                   '244314)\n'
                                                   'return _story_timer_fields(memory, frame, 512, None, '
                                                   'None, 244626, (33082,))'},
 'finish_prologue_closing_caption_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                         'FirstDeploymentFrame',
                                            'returns': 'FirstDeploymentFrame',
                                            'flow': 'memory.frame(frame)\n'
                                                    'frame = _story_call_fields(memory, frame, 244400, '
                                                    '244570)\n'
                                                    'frame = _story_call_fields(memory, frame, 244454, '
                                                    '244574)\n'
                                                    'return _story_timer_fields(memory, frame, 6592, '
                                                    '(65535,) * 4, 244616, None, (33082,))'},
 'wait_departure_second_page_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'memory.frame(frame)\n'
                                               'frame = _story_call_fields(memory, frame, 246942, 246914)\n'
                                               'return _story_timer_fields(memory, frame, 512, None, 246932, '
                                               'None, (33082,))'},
 'begin_departure_closing_caption_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                         'FirstDeploymentFrame',
                                            'returns': 'FirstDeploymentFrame',
                                            'flow': 'memory.frame(frame)\n'
                                                    'frame = _story_call_fields(memory, frame, 247238, '
                                                    '247152)\n'
                                                    'return _story_timer_fields(memory, frame, 512, None, '
                                                    'None, 244626, (33082,))'},
 'finish_departure_closing_caption_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                          'FirstDeploymentFrame',
                                             'returns': 'FirstDeploymentFrame',
                                             'flow': 'memory.frame(frame)\n'
                                                     'frame = _story_call_fields(memory, frame, 247238, '
                                                     '247426)\n'
                                                     'return _story_timer_fields(memory, frame, 7040, '
                                                     '(65535,) * 4, 247468, None, (33082,))'},
 'wait_arrival_second_page_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'memory.frame(frame)\n'
                                             'frame = _story_call_fields(memory, frame, 248962, 248930)\n'
                                             'return _story_timer_fields(memory, frame, 512, None, 248948, '
                                             'None, (33082, 33084))'},
 'begin_arrival_closing_caption_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                       'FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'memory.frame(frame)\n'
                                                  'frame = _story_call_fields(memory, frame, 249240, '
                                                  '249154)\n'
                                                  'return _story_timer_fields(memory, frame, 512, None, '
                                                  'None, 244626, (33082,))'},
 'finish_arrival_closing_caption_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                        'FirstDeploymentFrame',
                                           'returns': 'FirstDeploymentFrame',
                                           'flow': 'memory.frame(frame)\n'
                                                   'frame = _story_call_fields(memory, frame, 249240, '
                                                   '249282)\n'
                                                   'return _story_timer_fields(memory, frame, 7040, (65535,) '
                                                   '* 4, 249324, None, (33082,))'},
 'wait_finale_scroll_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                               'returns': 'FirstDeploymentFrame',
                               'flow': 'memory.frame(frame)\n'
                                       'frame = _story_call_fields(memory, frame, 250694, 250668)\n'
                                       'return _story_timer_fields(memory, frame, 256, None, None, None, '
                                       '(33082, 33084))'},
 'finish_finale_closing_caption_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                       'FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'memory.frame(frame)\n'
                                                  'frame = _story_call_fields(memory, frame, 250908, '
                                                  '250856)\n'
                                                  'return _story_timer_fields(memory, frame, 960, (65535,) * '
                                                  '4, 250898, None, (33082,))'},
 'reveal_departure_caption_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'memory.frame(frame)\n'
                                             'frame = _story_call_fields(memory, frame, 246692, 246568)\n'
                                             'frame = _story_caption_trigger_fields(memory, frame, 512, '
                                             '243102)\n'
                                             'return _story_timer_fields(memory, frame, 512, (65535, 65535, '
                                             '0, 65535), 246682, None, (33082,))'},
 'reveal_interlude_caption_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'memory.frame(frame)\n'
                                             'frame = _story_call_fields(memory, frame, 246692, 248328)\n'
                                             'frame = _story_caption_trigger_fields(memory, frame, 256, '
                                             '243450)\n'
                                             'return _story_timer_fields(memory, frame, 960, (65535,) * 4, '
                                             '248442, None, (33082,))'},
 'reveal_arrival_caption_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'memory.frame(frame)\n'
                                           'frame = _story_call_fields(memory, frame, 248766, 248642)\n'
                                           'frame = _story_caption_trigger_fields(memory, frame, 512, '
                                           '243248)\n'
                                           'return _story_timer_fields(memory, frame, 512, (65535, 65535, 0, '
                                           '65535), 248756, None, (33082,))'},
 'reveal_finale_caption_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': 'memory.frame(frame)\n'
                                          'frame = _story_call_fields(memory, frame, 250496, 250372)\n'
                                          'frame = _story_caption_trigger_fields(memory, frame, 192, '
                                          '243368)\n'
                                          'return _story_timer_fields(memory, frame, 320, (65535, 65535, 0, '
                                          '65535), 250486, None, (33082,))'},
 'confirm_prologue_exit_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': 'memory.frame(frame)\n'
                                          'frame = _story_call_fields(memory, frame, 244400, 244656)\n'
                                          'return _story_exit_fields(memory, frame)'},
 'confirm_departure_exit_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'memory.frame(frame)\n'
                                           'frame = _story_call_fields(memory, frame, 247238, 247482)\n'
                                           'return _story_exit_fields(memory, frame)'},
 'confirm_interlude_exit_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'memory.frame(frame)\n'
                                           'frame = _story_call_fields(memory, frame, 246692, 248456)\n'
                                           'return _story_exit_fields(memory, frame)'},
 'confirm_finale_exit_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                'returns': 'FirstDeploymentFrame',
                                'flow': 'memory.frame(frame)\n'
                                        'frame = _story_call_fields(memory, frame, 250908, 250954)\n'
                                        'return _story_exit_fields(memory, frame)'},
 'confirm_arrival_exit_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                 'returns': 'FirstDeploymentFrame',
                                 'flow': 'memory.frame(frame)\nreturn _story_exit_fields(memory, frame)'},
 'confirm_prologue_first_page_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'memory.frame(frame)\nframe = _story_call_fields(memory, frame, 243920, 243974)\nframe, pressed = _story_confirm_page_fields(memory, frame, 287530, 244014, 242994)\nif not pressed:\n    return frame\nframe = _story_darken_fields(memory, frame, 244080)\nframe = _story_finish_stage_fields(memory, frame, (33082,))\nreturn memory.sync_status(frame)'},
 'confirm_departure_first_page_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'memory.frame(frame)\nframe = _story_call_fields(memory, frame, 246692, 246794)\nframe, pressed = _story_confirm_page_fields(memory, frame, 290765, 246834, 243128)\nif not pressed:\n    return frame\nframe = _story_darken_fields(memory, frame, 246900)\nframe = _story_finish_stage_fields(memory, frame, (33082,))\nreturn memory.sync_status(frame)'},
 'confirm_departure_second_page_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'memory.frame(frame)\nframe = _story_call_fields(memory, frame, 246942, 246988)\nframe, pressed = _story_confirm_page_fields(memory, frame, 291400, 247028, 243176)\nif not pressed:\n    return frame\nframe = _story_palette_masks_fields(memory, frame, (65535, 65535, 0, 65535))\nframe = _story_darken_fields(memory, frame, 247118)\nframe = _story_finish_stage_fields(memory, frame, (33082, 33084, 33086, 33088, 33090, 33092))\nreturn memory.sync_status(frame)'},
 'confirm_arrival_first_page_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "memory.frame(frame)\nframe = _story_call_fields(memory, frame, 248766, 248806)\nframe, pressed = _story_pressed_fields(memory, frame)\nif not pressed:\n    return frame\nframe = _story_status_fields(memory, frame, 9984)\nframe = first_replace(frame, roster=memory.cursor_at(285409), candidates=memory.cursor_at(57344))\nframe = _story_move_fields(memory, frame, 'offset_x', 128, 32)\nframe = _story_move_fields(memory, frame, 'offset_y', 18)\nframe = _story_call_fields(memory, frame, 240322, 248846)\nframe = _story_clear_plane_fields(memory, frame)\nframe = _story_script_fields(memory, frame, 243284)\nframe = _story_status_fields(memory, frame, 9472)\nframe = _story_darken_fields(memory, frame, 248912)\nframe = _story_finish_stage_fields(memory, frame, (33082, 33084))\nreturn memory.sync_status(frame)"},
 'confirm_arrival_second_page_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'memory.frame(frame)\nframe = _story_call_fields(memory, frame, 248962, 249010)\nframe, pressed = _story_confirm_page_fields(memory, frame, 286064, 249050, 243332)\nif not pressed:\n    return frame\nframe = _story_palette_masks_fields(memory, frame, (65535, 65535, 0, 65535))\nframe = _story_darken_fields(memory, frame, 249140)\nframe = _story_finish_stage_fields(memory, frame, (33082,))\nreturn memory.sync_status(frame)'},
 'confirm_finale_first_page_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'memory.frame(frame)\nframe = _story_call_fields(memory, frame, 250496, 250532)\nframe, pressed = _story_confirm_page_fields(memory, frame, 289131, 250572, 243390)\nif not pressed:\n    return frame\nframe = _story_darken_fields(memory, frame, 250638)\nframe = _story_finish_stage_fields(memory, frame, (33082, 33084))\nframe = _story_store_fields(memory, frame, 4294934560, 496)\nframe = _story_store_fields(memory, frame, 4294934566, 496)\nreturn memory.sync_status(frame)'},
 'confirm_prologue_second_page_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                      'FirstDeploymentFrame',
                                         'returns': 'FirstDeploymentFrame',
                                         'flow': 'memory.frame(frame)\n'
                                                 'frame = _story_call_fields(memory, frame, 243920, 244182)\n'
                                                 'frame, pressed = _story_pressed_fields(memory, frame)\n'
                                                 'if not pressed:\n'
                                                 '    return frame\n'
                                                 'frame = _story_status_fields(memory, frame, 9984)\n'
                                                 'frame = _story_decode_picture_fields(memory, frame, '
                                                 '288197, 244222)\n'
                                                 'frame = _story_store_fields(memory, frame, 4294934566, 0)\n'
                                                 'frame = _story_status_fields(memory, frame, 9472)\n'
                                                 'frame = _story_finish_stage_fields(memory, frame)\n'
                                                 'frame = _story_status_fields(memory, frame, 9984)\n'
                                                 'frame = _story_clear_plane_fields(memory, frame)\n'
                                                 'frame = _story_script_fields(memory, frame, 243034)\n'
                                                 'return _story_status_fields(memory, frame, 9472)'},
 'advance_finale_scroll_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': 'memory.frame(frame)\n'
                                          'frame = _story_call_fields(memory, frame, 250908, 250742)\n'
                                          'for low in (32800, 32806):\n'
                                          '    frame = _story_add_ram_fields(memory, frame, low)\n'
                                          'for low in (32800, 32806):\n'
                                          '    value = _story_read_fields(memory, frame, 4294901760 | low) & '
                                          '511\n'
                                          '    frame = _story_store_fields(memory, frame, 4294901760 | low, '
                                          'value)\n'
                                          'frame = _story_compare_ram_fields(memory, frame, 32806, 256)\n'
                                          'if not frame.status & 5:\n'
                                          '    return frame\n'
                                          'frame = _story_compare_ram_fields(memory, frame, 32806, 112)\n'
                                          'if frame.status & 1:\n'
                                          '    return frame\n'
                                          'frame = _story_finish_stage_fields(memory, frame)\n'
                                          'frame = _story_status_fields(memory, frame, 9984)\n'
                                          'frame = _story_clear_plane_fields(memory, frame)\n'
                                          'frame = _story_script_fields(memory, frame, 243406)\n'
                                          'return _story_status_fields(memory, frame, 9472)'},
 '_story_select_sprite_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                              'directory: Long, attributes: Word | None',
                                 'returns': 'FirstDeploymentFrame',
                                 'flow': 'from .business_objects import _append_object_sprite_fields\n'
                                         "frame = _scene_render_asl_word(memory, frame, 'unit', "
                                         'low16(frame.unit), 2)\n'
                                         'address = directory + s16(low16(frame.unit))\n'
                                         'frame = first_replace(frame, '
                                         'roster=memory.cursor_at(_story_read_fields(memory, frame, address, '
                                         '4)))\n'
                                         "frame = _story_move_fields(memory, frame, 'unit', 5)\n"
                                         "frame = _story_move_fields(memory, frame, 'count', 0, 32)\n"
                                         'if attributes is not None:\n'
                                         "    frame = _story_move_fields(memory, frame, 'distance', "
                                         'attributes)\n'
                                         'return _append_object_sprite_fields(memory, frame)'},
 'select_prologue_sprite_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'memory.frame(frame)\n'
                                           'return _story_select_sprite_fields(memory, frame, 244694, 256)'},
 'select_departure_sprite_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'memory.frame(frame)\n'
                                            'return _story_select_sprite_fields(memory, frame, 247516, '
                                            'None)'},
 'select_arrival_sprite_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': 'memory.frame(frame)\n'
                                          'return _story_select_sprite_fields(memory, frame, 249372, 512)'},
 'select_finale_sprite_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                 'returns': 'FirstDeploymentFrame',
                                 'flow': 'memory.frame(frame)\n'
                                         "frame = _story_move_fields(memory, frame, 'distance', 256)\n"
                                         'return select_finale_sprite_with_attributes_fields(memory, frame)'},
 'select_finale_sprite_with_attributes_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                              'FirstDeploymentFrame',
                                                 'returns': 'FirstDeploymentFrame',
                                                 'flow': 'memory.frame(frame)\n'
                                                         'return _story_select_sprite_fields(memory, frame, '
                                                         '250992, None)'},
 'draw_prologue_portrait_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'memory.frame(frame)\n'
                                           "frame = _story_move_fields(memory, frame, 'unit', 12)\n"
                                           "frame = _story_move_fields(memory, frame, 'target_x', 128)\n"
                                           "frame = _story_move_fields(memory, frame, 'target_y', 192)\n"
                                           'return _story_call_fields(memory, frame, 244674, 243936)'},
 '_story_animation_index_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                                'counter: Word, shift: Word, maximum: Word, reset_counter: '
                                                'bool, hold_last: bool=False',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'frame = _story_add_ram_fields(memory, frame, counter)\n'
                                           "frame = _story_ram_move_fields(memory, frame, 'unit', counter)\n"
                                           "frame = _scene_mode_lsr_word(memory, frame, 'unit', "
                                           'low16(frame.unit), shift)\n'
                                           'frame = _scene_render_compare(memory, frame, low16(frame.unit), '
                                           'maximum, 16)\n'
                                           'if not frame.status & 5:\n'
                                           '    if reset_counter:\n'
                                           '        frame = _story_clear_fields(memory, frame, counter)\n'
                                           "    frame = _story_move_fields(memory, frame, 'unit', maximum if "
                                           'hold_last else 0, 32)\n'
                                           'return frame'},
 '_story_draw_pose_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, x: Word, '
                                          'y: Word, target: Long, continuation: Long, attributes: Word | '
                                          'None=None',
                             'returns': 'FirstDeploymentFrame',
                             'flow': "frame = _story_move_fields(memory, frame, 'target_x', x)\n"
                                     "frame = _story_move_fields(memory, frame, 'target_y', y)\n"
                                     'if attributes is not None:\n'
                                     "    frame = _story_move_fields(memory, frame, 'distance', attributes)\n"
                                     'return _story_call_fields(memory, frame, target, continuation)'},
 'animate_prologue_portrait_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                      'returns': 'FirstDeploymentFrame',
                                      'flow': 'memory.frame(frame)\n'
                                              'frame = _story_animation_index_fields(memory, frame, 33084, '
                                              '5, 2, True)\n'
                                              "frame = _story_arithmetic_fields(memory, frame, 'unit', 9)\n"
                                              'frame = _story_draw_pose_fields(memory, frame, 128, 192, '
                                              '244674, 244438)\n'
                                              "frame = _story_move_fields(memory, frame, 'target_x', 128)\n"
                                              "frame = _story_move_fields(memory, frame, 'target_y', 192)\n"
                                              "frame = _story_move_fields(memory, frame, 'unit', 0, 32)\n"
                                              'return _story_call_fields(memory, frame, 244674, 244452)'},
 'cycle_prologue_colors_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': 'memory.frame(frame)\n'
                                          "frame = _story_ram_move_fields(memory, frame, 'target_x', 33086)\n"
                                          "frame = _scene_mode_lsr_word(memory, frame, 'target_x', "
                                          'low16(frame.target_x), 4)\n'
                                          'frame = _scene_render_compare(memory, frame, '
                                          'low16(frame.target_x), 6, 16)\n'
                                          'if frame.status & 1:\n'
                                          "    frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                          'low16(frame.target_x), 1)\n'
                                          '    value = _story_read_fields(memory, frame, 244484 + '
                                          's16(low16(frame.target_x)))\n'
                                          '    frame = _story_store_fields(memory, frame, 4294966044, '
                                          'value)\n'
                                          '    return _story_add_ram_fields(memory, frame, 33086)\n'
                                          'frame = _scene_render_compare(memory, frame, '
                                          'low16(frame.target_x), 14, 16)\n'
                                          'if frame.status & 1:\n'
                                          "    frame = _story_arithmetic_fields(memory, frame, 'target_x', "
                                          '6, True)\n'
                                          "    frame = _story_arithmetic_fields(memory, frame, 'target_x', "
                                          '9)\n'
                                          '    frame = _story_call_fields(memory, frame, 240532, 244516)\n'
                                          '    return _story_add_ram_fields(memory, frame, 33086)\n'
                                          'frame = _story_compare_ram_fields(memory, frame, 32806, 80)\n'
                                          'if not frame.status & 1:\n'
                                          '    return frame\n'
                                          'for low, value in ((64258, 3822), (64262, 3784), (64286, 3718)):\n'
                                          '    frame = _story_store_fields(memory, frame, 4294901760 | low, '
                                          'value)\n'
                                          "frame = _story_ram_move_fields(memory, frame, 'target_x', 62240)\n"
                                          "frame = _story_mask_fields(memory, frame, 'target_x', 3)\n"
                                          'if frame.status & 4:\n'
                                          '    frame = _story_add_ram_fields(memory, frame, 32806)\n'
                                          'return frame'},
 'load_departure_tile_rows_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'memory.frame(frame)\n'
                                             'frame = first_replace(frame, '
                                             'controller=memory.cursor_at(246436))\n'
                                             'rows = ((59424, 246344), (59552, 246352), (59680, 246360), '
                                             '(59808, 246368), (59936, 246376), (60064, 246384), (60192, '
                                             '246392), (60320, 246400))\n'
                                             'for address, continuation in rows:\n'
                                             "    frame = _story_move_fields(memory, frame, 'target_x', "
                                             'address)\n'
                                             '    frame = _story_call_fields(memory, frame, 246402, '
                                             'continuation)\n'
                                             'return frame'},
 'write_departure_tile_row_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'memory.frame(frame)\n'
                                             'frame = _scene_render_push_longs(memory, frame, '
                                             '(frame.controller.base,))\n'
                                             'frame = _story_store_fields(memory, frame, 12582916, 36610)\n'
                                             'frame = _story_call_fields(memory, frame, 242352, 246418)\n'
                                             'stack = frame.stack_cursor\n'
                                             'frame = first_replace(frame, '
                                             'controller=memory.cursor_at(stack.long()), '
                                             'stack_cursor=stack.advance(4))\n'
                                             "frame = _story_move_fields(memory, frame, 'target_x', 7, 32)\n"
                                             'while True:\n'
                                             '    value = _story_read_fields(memory, frame, '
                                             'frame.controller.base)\n'
                                             '    frame = first_replace(frame, '
                                             'controller=frame.controller.advance(2))\n'
                                             '    frame = _story_store_fields(memory, frame, 12582912, '
                                             'value)\n'
                                             '    remaining = u16(low16(frame.target_x) - 1)\n'
                                             '    frame = first_replace(frame, '
                                             'target_x=replace_word(frame.target_x, remaining))\n'
                                             '    if remaining == 65535:\n'
                                             '        return frame'},
 '_story_rising_layer_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                             'counter: Word, sampled_counter: Word, shift: Word, baseline: '
                                             'Word, tile: Word, attributes: Word, continuation: Long',
                                'returns': 'FirstDeploymentFrame',
                                'flow': 'frame = _story_add_ram_fields(memory, frame, counter)\n'
                                        "frame = _story_ram_move_fields(memory, frame, 'unit', "
                                        'sampled_counter)\n'
                                        "frame = _scene_mode_lsr_word(memory, frame, 'unit', "
                                        'low16(frame.unit), shift)\n'
                                        "frame = _story_move_fields(memory, frame, 'target_y', baseline)\n"
                                        "frame = _story_arithmetic_fields(memory, frame, 'target_y', "
                                        'low16(frame.unit), True)\n'
                                        "frame = _story_move_fields(memory, frame, 'target_x', 128)\n"
                                        "frame = _story_move_fields(memory, frame, 'unit', tile)\n"
                                        "frame = _story_move_fields(memory, frame, 'distance', attributes)\n"
                                        'return _story_call_fields(memory, frame, 247500, continuation)'},
 'animate_departure_three_layers_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                        'FirstDeploymentFrame',
                                           'returns': 'FirstDeploymentFrame',
                                           'flow': 'memory.frame(frame)\n'
                                                   'frame = _story_rising_layer_fields(memory, frame, 33084, '
                                                   '33084, 6, 176, 0, 512, 246724)\n'
                                                   'frame = _story_rising_layer_fields(memory, frame, 33086, '
                                                   '33084, 5, 176, 1, 512, 246756)\n'
                                                   'return _story_rising_layer_fields(memory, frame, 33088, '
                                                   '33084, 4, 176, 2, 512, 246788)'},
 'animate_departure_transition_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                      'FirstDeploymentFrame',
                                         'returns': 'FirstDeploymentFrame',
                                         'flow': 'memory.frame(frame)\n'
                                                 'frame = _story_animation_index_fields(memory, frame, '
                                                 '33084, 5, 5, True)\n'
                                                 "frame = _story_arithmetic_fields(memory, frame, 'unit', "
                                                 '3)\n'
                                                 'return _story_draw_pose_fields(memory, frame, 128, 192, '
                                                 '247500, 246982, 256)'},
 'animate_departure_closing_layers_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                          'FirstDeploymentFrame',
                                             'returns': 'FirstDeploymentFrame',
                                             'flow': 'memory.frame(frame)\n'
                                                     "frame = _story_ram_move_fields(memory, frame, 'unit', "
                                                     '33092)\n'
                                                     "frame = _scene_mode_lsr_word(memory, frame, 'unit', "
                                                     'low16(frame.unit), 3)\n'
                                                     "frame = _story_move_fields(memory, frame, 'target_y', "
                                                     '224)\n'
                                                     'frame = _story_arithmetic_fields(memory, frame, '
                                                     "'target_y', low16(frame.unit), True)\n"
                                                     'frame = _scene_render_compare(memory, frame, '
                                                     'low16(frame.target_y), 192, 16)\n'
                                                     'if frame.status & 5:\n'
                                                     '    frame = _story_move_fields(memory, frame, '
                                                     "'target_y', 192)\n"
                                                     'else:\n'
                                                     '    frame = _story_add_ram_fields(memory, frame, '
                                                     '33092)\n'
                                                     "frame = _story_move_fields(memory, frame, 'target_x', "
                                                     '128)\n'
                                                     "frame = _story_move_fields(memory, frame, 'unit', 13)\n"
                                                     "frame = _story_move_fields(memory, frame, 'distance', "
                                                     '256)\n'
                                                     'frame = _story_call_fields(memory, frame, 247500, '
                                                     '247282)\n'
                                                     'frame = _story_ram_move_fields(memory, frame, '
                                                     "'target_y', 33090)\n"
                                                     'frame = _scene_mode_lsr_word(memory, frame, '
                                                     "'target_y', low16(frame.target_y), 3)\n"
                                                     'frame = _story_arithmetic_fields(memory, frame, '
                                                     "'target_y', 160)\n"
                                                     'frame = _scene_render_compare(memory, frame, '
                                                     'low16(frame.target_y), 192, 16)\n'
                                                     'if not frame.status & 1:\n'
                                                     '    frame = _story_move_fields(memory, frame, '
                                                     "'target_y', 192)\n"
                                                     'else:\n'
                                                     '    frame = _story_add_ram_fields(memory, frame, '
                                                     '33090)\n'
                                                     "frame = _story_move_fields(memory, frame, 'target_x', "
                                                     '128)\n'
                                                     "frame = _story_move_fields(memory, frame, 'unit', 12)\n"
                                                     "frame = _story_move_fields(memory, frame, 'distance', "
                                                     '512)\n'
                                                     'frame = _story_call_fields(memory, frame, 247500, '
                                                     '247324)\n'
                                                     'frame = _story_rising_layer_fields(memory, frame, '
                                                     '33084, 33084, 6, 192, 9, 512, 247356)\n'
                                                     'frame = _story_rising_layer_fields(memory, frame, '
                                                     '33086, 33086, 5, 192, 10, 512, 247388)\n'
                                                     'return _story_rising_layer_fields(memory, frame, '
                                                     '33088, 33088, 4, 192, 11, 512, 247420)'},
 'animate_arrival_portrait_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'memory.frame(frame)\n'
                                             'frame = _story_animation_index_fields(memory, frame, 33084, 5, '
                                             '3, True)\n'
                                             'return _story_draw_pose_fields(memory, frame, 128, 192, '
                                             '249352, 248800)'},
 'animate_arrival_zoom_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                 'returns': 'FirstDeploymentFrame',
                                 'flow': 'memory.frame(frame)\n'
                                         'frame = _story_add_ram_fields(memory, frame, 33084)\n'
                                         "frame = _story_ram_move_fields(memory, frame, 'unit', 33084)\n"
                                         "frame = _scene_mode_lsr_word(memory, frame, 'unit', "
                                         'low16(frame.unit), 5)\n'
                                         "frame = _story_move_fields(memory, frame, 'target_x', 128)\n"
                                         "frame = _story_move_fields(memory, frame, 'target_y', 192)\n"
                                         "frame = _story_arithmetic_fields(memory, frame, 'target_x', "
                                         'low16(frame.unit), True)\n'
                                         "frame = _story_arithmetic_fields(memory, frame, 'target_y', "
                                         'low16(frame.unit), True)\n'
                                         "frame = _story_move_fields(memory, frame, 'unit', 4, 32)\n"
                                         'frame = _story_call_fields(memory, frame, 249352, 248990)\n'
                                         "frame = _story_move_fields(memory, frame, 'target_x', 128)\n"
                                         "frame = _story_move_fields(memory, frame, 'target_y', 192)\n"
                                         "frame = _story_move_fields(memory, frame, 'unit', 8, 32)\n"
                                         'return _story_call_fields(memory, frame, 249352, 249004)'},
 'animate_arrival_closing_portrait_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                          'FirstDeploymentFrame',
                                             'returns': 'FirstDeploymentFrame',
                                             'flow': 'memory.frame(frame)\n'
                                                     'frame = _story_animation_index_fields(memory, frame, '
                                                     '33084, 5, 2, True)\n'
                                                     'frame = _story_arithmetic_fields(memory, frame, '
                                                     "'unit', 5)\n"
                                                     'return _story_draw_pose_fields(memory, frame, 128, '
                                                     '196, 249352, 249276)'},
 'animate_finale_portrait_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'memory.frame(frame)\n'
                                            'frame = _story_animation_index_fields(memory, frame, 33084, 5, '
                                            '3, False, True)\n'
                                            'return _story_draw_pose_fields(memory, frame, 128, 192, 250972, '
                                            '250526)'},
 'move_finale_actor_diagonally_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                      'FirstDeploymentFrame',
                                         'returns': 'FirstDeploymentFrame',
                                         'flow': 'memory.frame(frame)\n'
                                                 'frame = _story_compare_ram_fields(memory, frame, 33084, '
                                                 '160)\n'
                                                 'if not frame.status & 5:\n'
                                                 '    return frame\n'
                                                 'frame = _story_add_ram_fields(memory, frame, 33084, 2)\n'
                                                 "frame = _story_move_fields(memory, frame, 'target_x', 48)\n"
                                                 "frame = _story_move_fields(memory, frame, 'target_y', "
                                                 '224)\n'
                                                 'frame = _story_arithmetic_fields(memory, frame, '
                                                 "'target_x', _story_read_fields(memory, frame, "
                                                 '4294934844))\n'
                                                 'frame = _story_arithmetic_fields(memory, frame, '
                                                 "'target_y', _story_read_fields(memory, frame, 4294934844), "
                                                 'True)\n'
                                                 'frame = _story_arithmetic_fields(memory, frame, '
                                                 "'target_x', _story_read_fields(memory, frame, "
                                                 '4294934560))\n'
                                                 "frame = _story_move_fields(memory, frame, 'unit', 7)\n"
                                                 'return _story_call_fields(memory, frame, 250972, 250736)'},
 'animate_finale_closing_portrait_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                         'FirstDeploymentFrame',
                                            'returns': 'FirstDeploymentFrame',
                                            'flow': 'memory.frame(frame)\n'
                                                    'frame = _story_add_ram_fields(memory, frame, 33084)\n'
                                                    "frame = _story_ram_move_fields(memory, frame, 'unit', "
                                                    '33084)\n'
                                                    "frame = _scene_mode_lsr_word(memory, frame, 'unit', "
                                                    'low16(frame.unit), 4)\n'
                                                    'frame = _scene_render_compare(memory, frame, '
                                                    'low16(frame.unit), 1, 16)\n'
                                                    'if not frame.status & 5:\n'
                                                    "    frame = _story_move_fields(memory, frame, 'unit', "
                                                    '0, 32)\n'
                                                    '    frame = _story_clear_fields(memory, frame, 33084)\n'
                                                    "frame = _story_arithmetic_fields(memory, frame, 'unit', "
                                                    '5)\n'
                                                    "frame = _story_move_fields(memory, frame, 'target_x', "
                                                    '192)\n'
                                                    "frame = _story_move_fields(memory, frame, 'target_y', "
                                                    '192)\n'
                                                    "frame = _story_move_fields(memory, frame, 'distance', "
                                                    '512)\n'
                                                    'return _story_call_fields(memory, frame, 250976, '
                                                    '250948)'},
 '_story_text_dimensions_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                                'characters: Word, continuation: Long',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': "frame = _story_move_fields(memory, frame, 'target_x', "
                                           '_story_read_fields(memory, frame, 16740372))\n'
                                           "frame = _story_move_fields(memory, frame, 'target_y', "
                                           '_story_read_fields(memory, frame, 16740374))\n'
                                           "frame = _story_move_fields(memory, frame, 'count', characters)\n"
                                           'return _story_call_fields(memory, frame, 44682, continuation)'},
 '_story_upload_current_rows_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'while True:\n'
                                               '    value = _story_read_fields(memory, frame, '
                                               'frame.roster.base, 4)\n'
                                               '    frame = first_replace(frame, '
                                               'roster=frame.roster.advance(4))\n'
                                               '    frame = _story_store_fields(memory, frame, '
                                               'frame.auxiliary.base, value, 4)\n'
                                               '    counter = u16(low16(frame.target_x) - 1)\n'
                                               '    frame = first_replace(frame, '
                                               'target_x=replace_word(frame.target_x, counter))\n'
                                               '    if counter == 65535:\n'
                                               '        return frame'},
 '_story_text_tile_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, advance: '
                                          'Word',
                             'returns': 'FirstDeploymentFrame',
                             'flow': "frame = _story_move_fields(memory, frame, 'unit', "
                                     '_story_read_fields(memory, frame, 16740364))\n'
                                     "return _story_arithmetic_fields(memory, frame, 'unit', advance)"},
 '_story_decimal_strip_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, role',
                                 'returns': 'FirstDeploymentFrame',
                                 'flow': "if role == 'officer':\n"
                                         '    counter, decimal_return, glyph_return, digits = (32996, '
                                         '262420, 262486, 3)\n'
                                         "elif role == 'pair':\n"
                                         '    counter, decimal_return, glyph_return, digits = (32998, '
                                         '262548, 262602, 2)\n'
                                         "elif role == 'triple':\n"
                                         '    counter, decimal_return, glyph_return, digits = (33000, '
                                         '262692, 262758, 3)\n'
                                         'else:\n'
                                         "    raise ValueError('closed text number role required')\n"
                                         "if role == 'triple':\n"
                                         '    frame = _story_store_fields(memory, frame, 16740364, '
                                         'low16(frame.unit))\n'
                                         '    frame = _story_store_fields(memory, frame, 16740366, '
                                         'frame.roster.base, 4)\n'
                                         'else:\n'
                                         '    frame = _story_store_fields(memory, frame, 16740366, '
                                         'frame.roster.base, 4)\n'
                                         '    frame = _story_store_fields(memory, frame, 16740364, '
                                         'low16(frame.unit))\n'
                                         "frame = _story_move_fields(memory, frame, 'target_x', 0, 32)\n"
                                         "frame = _story_ram_move_fields(memory, frame, 'target_x', "
                                         'counter)\n'
                                         'frame = _story_call_fields(memory, frame, 242392, decimal_return)\n'
                                         "carriers = ('target_x', 'target_y', 'unit') if digits == 3 else "
                                         "('target_x', 'target_y')\n"
                                         'for name in carriers:\n'
                                         '    frame = _story_move_fields(memory, frame, name, 256)\n'
                                         'for index, name in enumerate(carriers):\n'
                                         '    frame = _story_ram_move_fields(memory, frame, name, 32774 - '
                                         'digits + index, 8)\n'
                                         'for index, name in enumerate(carriers):\n'
                                         '    frame = _story_store_fields(memory, frame, 4294934528 + index '
                                         '* 2, low16(frame.carrier(name)))\n'
                                         'frame = first_replace(frame, roster=memory.cursor_at(4294934528), '
                                         'candidates=memory.cursor_at(4294955776))\n'
                                         'frame = _story_text_dimensions_fields(memory, frame, digits - 1, '
                                         'glyph_return)\n'
                                         'frame = first_replace(frame, roster=memory.cursor_at(4294955776), '
                                         'auxiliary=memory.cursor_at(12582912))\n'
                                         "frame = _story_move_fields(memory, frame, 'target_x', digits * 32 "
                                         '- 1)\n'
                                         "if role == 'pair':\n"
                                         '    frame = _story_compare_ram_fields(memory, frame, 32768, 256)\n'
                                         '    if frame.status & 4:\n'
                                         '        frame = first_replace(frame, '
                                         'roster=frame.roster.advance(128))\n'
                                         "        frame = _story_move_fields(memory, frame, 'target_x', "
                                         '_story_read_fields(memory, frame, 16740364))\n'
                                         '        frame = _story_arithmetic_fields(memory, frame, '
                                         "'target_x', 128)\n"
                                         '        frame = _story_call_fields(memory, frame, 242352, 262642)\n'
                                         "        frame = _story_move_fields(memory, frame, 'target_x', 31)\n"
                                         "elif role == 'triple':\n"
                                         '    frame = _story_text_tile_fields(memory, frame, 384)\n'
                                         '    frame = _story_compare_ram_fields(memory, frame, 32768, 256)\n'
                                         '    if frame.status & 4:\n'
                                         '        frame = first_replace(frame, '
                                         'roster=frame.roster.advance(128))\n'
                                         '        frame = _story_text_tile_fields(memory, frame, 256)\n'
                                         "        frame = _story_move_fields(memory, frame, 'target_x', 63)\n"
                                         '        frame = _story_compare_ram_fields(memory, frame, 32770, '
                                         '256)\n'
                                         '        if frame.status & 4:\n'
                                         '            frame = first_replace(frame, '
                                         'roster=frame.roster.advance(128))\n'
                                         '            frame = _story_text_tile_fields(memory, frame, 128)\n'
                                         "            frame = _story_move_fields(memory, frame, 'target_x', "
                                         '31)\n'
                                         'frame = _story_upload_current_rows_fields(memory, frame)\n'
                                         "if role != 'triple':\n"
                                         '    frame = _story_text_tile_fields(memory, frame, digits * 128)\n'
                                         'frame = first_replace(frame, '
                                         'roster=memory.cursor_at(_story_read_fields(memory, frame, '
                                         '16740366, 4)))\n'
                                         "if role != 'pair':\n"
                                         '    frame = first_replace(frame, roster=frame.roster.advance(2))\n'
                                         'return memory.sync_status(frame)'},
 'append_story_officer_number_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                     'FirstDeploymentFrame',
                                        'returns': 'FirstDeploymentFrame',
                                        'flow': 'memory.frame(frame)\n'
                                                'return _story_decimal_strip_fields(memory, frame, '
                                                "'officer')"},
 'append_story_counter_pair_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                      'returns': 'FirstDeploymentFrame',
                                      'flow': 'memory.frame(frame)\n'
                                              "return _story_decimal_strip_fields(memory, frame, 'pair')"},
 'append_story_counter_triple_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                     'FirstDeploymentFrame',
                                        'returns': 'FirstDeploymentFrame',
                                        'flow': 'memory.frame(frame)\n'
                                                'return _story_decimal_strip_fields(memory, frame, '
                                                "'triple')"},
 'advance_story_text_stream_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                      'returns': 'FirstDeploymentFrame',
                                      'flow': 'memory.frame(frame)\n'
                                              "frame = _story_ram_move_fields(memory, frame, 'target_y', "
                                              '61400)\n'
                                              "frame = _story_ram_move_fields(memory, frame, 'target_x', "
                                              '62240)\n'
                                              'mask = _story_read_fields(memory, frame, 262054 + '
                                              's16(low16(frame.target_y)), 1)\n'
                                              "frame = _story_mask_fields(memory, frame, 'target_x', mask, "
                                              '8)\n'
                                              'if not frame.status & 4:\n'
                                              '    return frame\n'
                                              'value = _story_read_fields(memory, frame, 16740364)\n'
                                              'frame = _scene_refresh_flags(memory, frame, value, 2)\n'
                                              'if frame.status & 4:\n'
                                              '    return frame\n'
                                              "frame = _story_move_fields(memory, frame, 'target_x', "
                                              '_story_read_fields(memory, frame, 16740364))\n'
                                              'frame = _story_call_fields(memory, frame, 242352, 262094)\n'
                                              'frame = first_replace(frame, '
                                              'roster=memory.cursor_at(_story_read_fields(memory, frame, '
                                              '16740366, 4)))\n'
                                              "frame = _story_move_fields(memory, frame, 'target_x', "
                                              '_story_read_fields(memory, frame, frame.roster.base))\n'
                                              "frame = _story_mask_fields(memory, frame, 'target_x', 49151)\n"
                                              'special = False\n'
                                              'for token, selected, alternate in ((32776, 32992, 32994), '
                                              '(32782, 32988, 32990), (32778, 32994, 32992), (65283, 32990, '
                                              '32988)):\n'
                                              "    frame = _story_ram_move_fields(memory, frame, 'choice', "
                                              'selected)\n'
                                              "    frame = _story_ram_move_fields(memory, frame, 'offset_y', "
                                              'alternate)\n'
                                              '    frame = _scene_render_compare(memory, frame, '
                                              'low16(frame.target_x), token, 16)\n'
                                              '    if frame.status & 4:\n'
                                              '        special = True\n'
                                              '        break\n'
                                              'scan_following = True\n'
                                              'if special:\n'
                                              '    value = _story_read_fields(memory, frame, 4294934806)\n'
                                              '    frame = _scene_refresh_flags(memory, frame, value, 2)\n'
                                              '    if not frame.status & 4:\n'
                                              "        frame = _story_move_fields(memory, frame, 'choice', "
                                              'low16(frame.offset_y))\n'
                                              "    frame = _story_move_fields(memory, frame, 'target_x', "
                                              '_story_read_fields(memory, frame, 16740372))\n'
                                              "    frame = _story_move_fields(memory, frame, 'target_y', "
                                              '_story_read_fields(memory, frame, 16740374))\n'
                                              '    frame = _story_call_fields(memory, frame, 262850, '
                                              '262188)\n'
                                              '    frame = _story_text_tile_fields(memory, frame, 384)\n'
                                              'else:\n'
                                              "    frame = _story_move_fields(memory, frame, 'unit', "
                                              '_story_read_fields(memory, frame, 16740364))\n'
                                              '    frame = _scene_render_bit(memory, frame, frame.target_x, '
                                              '32768)\n'
                                              '    if not frame.status & 4:\n'
                                              '        scan_following = False\n'
                                              '    else:\n'
                                              '        frame = first_replace(frame, '
                                              'candidates=memory.cursor_at(4294955776))\n'
                                              '        frame = _story_text_dimensions_fields(memory, frame, '
                                              '0, 262240)\n'
                                              '        frame = first_replace(frame, '
                                              'roster=memory.cursor_at(4294955776))\n'
                                              '        frame = _story_glyph_upload_fields(memory, frame, '
                                              '31)\n'
                                              '        frame = _story_text_tile_fields(memory, frame, 128)\n'
                                              'if scan_following:\n'
                                              '    frame = first_replace(frame, '
                                              'roster=memory.cursor_at(_story_read_fields(memory, frame, '
                                              '16740366, 4)).advance(2))\n'
                                              "    frame = _story_move_fields(memory, frame, 'target_x', "
                                              '_story_read_fields(memory, frame, frame.roster.base))\n'
                                              'if not scan_following or frame.status & 8:\n'
                                              '    frame = _scene_render_compare(memory, frame, '
                                              'low16(frame.target_x), 65312, 16)\n'
                                              '    if frame.status & 4:\n'
                                              '        frame = _story_arithmetic_fields(memory, frame, '
                                              "'unit', 64)\n"
                                              '        frame = first_replace(frame, '
                                              'roster=frame.roster.advance(2))\n'
                                              '    else:\n'
                                              '        frame = _scene_render_compare(memory, frame, '
                                              'low16(frame.target_x), 32770, 16)\n'
                                              '        if frame.status & 4:\n'
                                              '            frame = first_replace(frame, '
                                              'roster=frame.roster.advance(2))\n'
                                              '            frame = _story_move_fields(memory, frame, '
                                              "'target_x', low16(frame.unit))\n"
                                              "            frame = _story_move_fields(memory, frame, 'unit', "
                                              '43264)\n'
                                              '            frame = _scene_render_compare(memory, frame, '
                                              'low16(frame.target_x), 43264, 16)\n'
                                              '            if not frame.status & 1:\n'
                                              '                frame = _story_move_fields(memory, frame, '
                                              "'unit', 45568)\n"
                                              '        else:\n'
                                              '            frame = _scene_render_compare(memory, frame, '
                                              'low16(frame.target_x), 32784, 16)\n'
                                              '            if frame.status & 4:\n'
                                              '                frame = _story_call_fields(memory, frame, '
                                              '262398, 262340)\n'
                                              '            else:\n'
                                              '                frame = _scene_render_compare(memory, frame, '
                                              'low16(frame.target_x), 32785, 16)\n'
                                              '                if frame.status & 4:\n'
                                              '                    frame = first_replace(frame, '
                                              'roster=frame.roster.advance(2))\n'
                                              '                    frame = _story_call_fields(memory, frame, '
                                              '262526, 262356)\n'
                                              '                else:\n'
                                              '                    frame = _scene_render_compare(memory, '
                                              'frame, low16(frame.target_x), 32786, 16)\n'
                                              '                    if frame.status & 4:\n'
                                              '                        frame = first_replace(frame, '
                                              'roster=frame.roster.advance(2))\n'
                                              '                        frame = _story_call_fields(memory, '
                                              'frame, 262670, 262372)\n'
                                              '                    else:\n'
                                              '                        frame = _scene_render_compare(memory, '
                                              'frame, low16(frame.target_x), 32768, 16)\n'
                                              '                        if frame.status & 4:\n'
                                              '                            frame = '
                                              "_story_move_fields(memory, frame, 'unit', 0)\n"
                                              'return _story_finish_text_stream_fields(memory, frame)'},
 '_story_finish_text_stream_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                      'returns': 'FirstDeploymentFrame',
                                      'flow': 'frame = _story_store_fields(memory, frame, 16740364, '
                                              'low16(frame.unit))\n'
                                              'return _story_store_fields(memory, frame, 16740366, '
                                              'frame.roster.base, 4)'},
 '_story_dma_setup_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, words: '
                                          'tuple, latch: Word, retain_port: bool',
                             'returns': 'FirstDeploymentFrame',
                             'flow': 'if retain_port:\n'
                                     '    frame = first_replace(frame, '
                                     'auxiliary=memory.cursor_at(12582916))\n'
                                     "frame = _story_ram_move_fields(memory, frame, 'choice', 62982)\n"
                                     "frame = _story_move_fields(memory, frame, 'choice', low8(frame.choice) "
                                     '| 16, 8)\n'
                                     'frame = _story_store_fields(memory, frame, frame.auxiliary.base, '
                                     'low16(frame.choice))\n'
                                     'frame = _story_store_fields(memory, frame, 10555648, 256)\n'
                                     'frame = _story_store_fields(memory, frame, frame.auxiliary.base, '
                                     'words[0], 4)\n'
                                     'frame = _story_store_fields(memory, frame, frame.auxiliary.base, '
                                     'words[1], 4)\n'
                                     'frame = _story_store_fields(memory, frame, frame.auxiliary.base, '
                                     '38783)\n'
                                     'frame = _story_store_fields(memory, frame, frame.auxiliary.base, '
                                     'words[2])\n'
                                     'frame = _story_store_fields(memory, frame, 4294964768, latch)\n'
                                     'frame = _story_store_fields(memory, frame, frame.auxiliary.base, '
                                     '_story_read_fields(memory, frame, 4294964768))\n'
                                     'value = _story_read_fields(memory, frame, 4294917888, 1)\n'
                                     'frame = _scene_refresh_flags(memory, frame, value, 1)\n'
                                     'if frame.status & 4:\n'
                                     '    frame = _story_store_fields(memory, frame, 10555648, 0)\n'
                                     'return frame'},
 '_story_dma_finish_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                              'returns': 'FirstDeploymentFrame',
                              'flow': "frame = _story_ram_move_fields(memory, frame, 'target_x', 62982)\n"
                                      "frame = _story_move_fields(memory, frame, 'target_x', "
                                      'low8(frame.target_x) | 64, 8)\n'
                                      'return _story_store_fields(memory, frame, 12582916, '
                                      'low16(frame.target_x))'},
 'transfer_story_plane_dma_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'memory.frame(frame)\n'
                                             'frame = _story_call_fields(memory, frame, 26570, 238908)\n'
                                             'frame = _story_call_fields(memory, frame, 18754, 238914)\n'
                                             'frame = _story_dma_setup_fields(memory, frame, (2483065664, '
                                             '2533201280, 49152), 128, True)\n'
                                             'frame = _story_store_fields(memory, frame, '
                                             'frame.auxiliary.base, _story_read_fields(memory, frame, '
                                             '4294964742))\n'
                                             'frame = _story_clear_fields(memory, frame, 62994)\n'
                                             'return _story_dma_finish_fields(memory, frame)'},
 'transfer_story_overlay_dma_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'memory.frame(frame)\n'
                                               'frame = _story_call_fields(memory, frame, 26570, 239778)\n'
                                               'frame = _story_dma_setup_fields(memory, frame, (2483131200, '
                                               '2533135616, 20480), 131, True)\n'
                                               'frame = _story_store_fields(memory, frame, '
                                               'frame.auxiliary.base, _story_read_fields(memory, frame, '
                                               '4294964742))\n'
                                               'frame = _story_store_fields(memory, frame, 12582916, '
                                               '1073741840, 4)\n'
                                               'frame = _story_store_fields(memory, frame, 12582912, '
                                               '_story_read_fields(memory, frame, 4294934564, 4), 4)\n'
                                               'frame = _story_store_fields(memory, frame, 12582916, '
                                               '1409286147, 4)\n'
                                               'frame = _story_store_fields(memory, frame, 12582912, '
                                               '_story_read_fields(memory, frame, 4294934568, 4), 4)\n'
                                               "frame = _story_move_fields(memory, frame, 'target_x', 96)\n"
                                               'while True:\n'
                                               '    remaining = u16(low16(frame.target_x) - 1)\n'
                                               '    frame = first_replace(frame, '
                                               'target_x=replace_word(frame.target_x, remaining))\n'
                                               '    if remaining == 65535:\n'
                                               '        break\n'
                                               'frame = _story_dma_setup_fields(memory, frame, (2483065664, '
                                               '2533201280, 49152), 128, True)\n'
                                               'frame = _story_store_fields(memory, frame, '
                                               'frame.auxiliary.base, _story_read_fields(memory, frame, '
                                               '4294964742))\n'
                                               'frame = _story_dma_finish_fields(memory, frame)\n'
                                               'return _story_call_fields(memory, frame, 262058, 239988)'},
 '_story_dispatch_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, table: '
                                         'Long',
                            'returns': 'FirstDeploymentFrame',
                            'flow': 'memory.frame(frame)\n'
                                    "frame = _story_ram_move_fields(memory, frame, 'target_x', 33002)\n"
                                    "frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                    'low16(frame.target_x), 2)\n'
                                    'return _story_known_fields(memory, frame, table + '
                                    's16(low16(frame.target_x)))'},
 'dispatch_prologue_story_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'return _story_dispatch_fields(memory, frame, 243644)'},
 'dispatch_departure_story_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'return _story_dispatch_fields(memory, frame, 246172)'},
 'dispatch_arrival_story_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'return _story_dispatch_fields(memory, frame, 248484)'},
 'dispatch_finale_story_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': 'return _story_dispatch_fields(memory, frame, 250236)'},
 'dispatch_interlude_story_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'return _story_dispatch_fields(memory, frame, 248186)'},
 '_story_known_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long',
                         'returns': 'FirstDeploymentFrame',
                         'flow': 'memory.frame(frame)\n'
                                 'if target == 238902:\n'
                                 '    return transfer_story_plane_dma_fields(memory, frame)\n'
                                 'elif target == 239772:\n'
                                 '    return transfer_story_overlay_dma_fields(memory, frame)\n'
                                 'elif target == 243614:\n'
                                 '    return dispatch_prologue_story_fields(memory, frame)\n'
                                 'elif target == 243618:\n'
                                 '    return dispatch_departure_story_fields(memory, frame)\n'
                                 'elif target == 243622:\n'
                                 '    return dispatch_arrival_story_fields(memory, frame)\n'
                                 'elif target == 243626:\n'
                                 '    return dispatch_finale_story_fields(memory, frame)\n'
                                 'elif target == 243630:\n'
                                 '    return dispatch_interlude_story_fields(memory, frame)\n'
                                 'elif target == 243644:\n'
                                 '    return initialize_prologue_story_fields(memory, frame)\n'
                                 'elif target == 243648:\n'
                                 '    return reveal_prologue_caption_fields(memory, frame)\n'
                                 'elif target == 243652:\n'
                                 '    return wait_prologue_portrait_fields(memory, frame)\n'
                                 'elif target == 243656:\n'
                                 '    return confirm_prologue_first_page_fields(memory, frame)\n'
                                 'elif target == 243660:\n'
                                 '    return wait_prologue_second_page_fields(memory, frame)\n'
                                 'elif target == 243664:\n'
                                 '    return reveal_prologue_second_portrait_fields(memory, frame)\n'
                                 'elif target == 243668:\n'
                                 '    return confirm_prologue_second_page_fields(memory, frame)\n'
                                 'elif target == 243672:\n'
                                 '    return begin_prologue_closing_caption_fields(memory, frame)\n'
                                 'elif target == 243676:\n'
                                 '    return finish_prologue_closing_caption_fields(memory, frame)\n'
                                 'elif target == 243680:\n'
                                 '    return confirm_prologue_exit_fields(memory, frame)\n'
                                 'elif target == 243920:\n'
                                 '    return draw_prologue_portrait_fields(memory, frame)\n'
                                 'elif target == 244400:\n'
                                 '    return animate_prologue_portrait_fields(memory, frame)\n'
                                 'elif target == 244454:\n'
                                 '    return cycle_prologue_colors_fields(memory, frame)\n'
                                 'elif target == 244674:\n'
                                 '    return select_prologue_sprite_fields(memory, frame)\n'
                                 'elif target == 246172:\n'
                                 '    return initialize_departure_story_fields(memory, frame)\n'
                                 'elif target == 246176:\n'
                                 '    return reveal_departure_caption_fields(memory, frame)\n'
                                 'elif target == 246180:\n'
                                 '    return confirm_departure_first_page_fields(memory, frame)\n'
                                 'elif target == 246184:\n'
                                 '    return wait_departure_second_page_fields(memory, frame)\n'
                                 'elif target == 246188:\n'
                                 '    return confirm_departure_second_page_fields(memory, frame)\n'
                                 'elif target == 246192:\n'
                                 '    return begin_departure_closing_caption_fields(memory, frame)\n'
                                 'elif target == 246196:\n'
                                 '    return finish_departure_closing_caption_fields(memory, frame)\n'
                                 'elif target == 246200:\n'
                                 '    return confirm_departure_exit_fields(memory, frame)\n'
                                 'elif target == 246330:\n'
                                 '    return load_departure_tile_rows_fields(memory, frame)\n'
                                 'elif target == 246402:\n'
                                 '    return write_departure_tile_row_fields(memory, frame)\n'
                                 'elif target == 246692:\n'
                                 '    return animate_departure_three_layers_fields(memory, frame)\n'
                                 'elif target == 246942:\n'
                                 '    return animate_departure_transition_fields(memory, frame)\n'
                                 'elif target == 247238:\n'
                                 '    return animate_departure_closing_layers_fields(memory, frame)\n'
                                 'elif target == 247500:\n'
                                 '    return select_departure_sprite_fields(memory, frame)\n'
                                 'elif target == 248186:\n'
                                 '    return initialize_interlude_story_fields(memory, frame)\n'
                                 'elif target == 248190:\n'
                                 '    return reveal_interlude_caption_fields(memory, frame)\n'
                                 'elif target == 248194:\n'
                                 '    return confirm_interlude_exit_fields(memory, frame)\n'
                                 'elif target == 248484:\n'
                                 '    return initialize_arrival_story_fields(memory, frame)\n'
                                 'elif target == 248488:\n'
                                 '    return reveal_arrival_caption_fields(memory, frame)\n'
                                 'elif target == 248492:\n'
                                 '    return confirm_arrival_first_page_fields(memory, frame)\n'
                                 'elif target == 248496:\n'
                                 '    return wait_arrival_second_page_fields(memory, frame)\n'
                                 'elif target == 248500:\n'
                                 '    return confirm_arrival_second_page_fields(memory, frame)\n'
                                 'elif target == 248504:\n'
                                 '    return begin_arrival_closing_caption_fields(memory, frame)\n'
                                 'elif target == 248508:\n'
                                 '    return finish_arrival_closing_caption_fields(memory, frame)\n'
                                 'elif target == 248512:\n'
                                 '    return confirm_arrival_exit_fields(memory, frame)\n'
                                 'elif target == 248766:\n'
                                 '    return animate_arrival_portrait_fields(memory, frame)\n'
                                 'elif target == 248962:\n'
                                 '    return animate_arrival_zoom_fields(memory, frame)\n'
                                 'elif target == 249240:\n'
                                 '    return animate_arrival_closing_portrait_fields(memory, frame)\n'
                                 'elif target == 249352:\n'
                                 '    return select_arrival_sprite_fields(memory, frame)\n'
                                 'elif target == 250236:\n'
                                 '    return initialize_finale_story_fields(memory, frame)\n'
                                 'elif target == 250240:\n'
                                 '    return reveal_finale_caption_fields(memory, frame)\n'
                                 'elif target == 250244:\n'
                                 '    return confirm_finale_first_page_fields(memory, frame)\n'
                                 'elif target == 250248:\n'
                                 '    return wait_finale_scroll_fields(memory, frame)\n'
                                 'elif target == 250252:\n'
                                 '    return advance_finale_scroll_fields(memory, frame)\n'
                                 'elif target == 250256:\n'
                                 '    return finish_finale_closing_caption_fields(memory, frame)\n'
                                 'elif target == 250260:\n'
                                 '    return confirm_finale_exit_fields(memory, frame)\n'
                                 'elif target == 250496:\n'
                                 '    return animate_finale_portrait_fields(memory, frame)\n'
                                 'elif target == 250694:\n'
                                 '    return move_finale_actor_diagonally_fields(memory, frame)\n'
                                 'elif target == 250908:\n'
                                 '    return animate_finale_closing_portrait_fields(memory, frame)\n'
                                 'elif target == 250972:\n'
                                 '    return select_finale_sprite_fields(memory, frame)\n'
                                 'elif target == 250976:\n'
                                 '    return select_finale_sprite_with_attributes_fields(memory, frame)\n'
                                 'elif target == 262058:\n'
                                 '    return advance_story_text_stream_fields(memory, frame)\n'
                                 'elif target == 262398:\n'
                                 '    return append_story_officer_number_fields(memory, frame)\n'
                                 'elif target == 262526:\n'
                                 '    return append_story_counter_pair_fields(memory, frame)\n'
                                 'elif target == 262670:\n'
                                 '    return append_story_counter_triple_fields(memory, frame)\n'
                                 'elif target == 240160:\n'
                                 '    return begin_scene_palette_darken_fields(memory, frame)\n'
                                 'elif target == 240184:\n'
                                 '    from ..high_level_dynamic_flows.business_early_phase import '
                                 'begin_scene_palette_lighten_fields\n'
                                 '    return begin_scene_palette_lighten_fields(memory, frame)\n'
                                 'elif target == 240334:\n'
                                 '    return read_vdp_plane_rle_rows_fields(memory, frame)\n'
                                 'elif target == 242352:\n'
                                 '    return set_vram_write_address_fields(memory, frame)\n'
                                 'elif target == 240532:\n'
                                 '    return copy_scene_palette_variant_fields(memory, frame)\n'
                                 'elif target == 44682:\n'
                                 '    return decode_glyph_rows_to_buffers_fields(memory, frame)\n'
                                 'elif target == 242392:\n'
                                 '    from ..high_level_dynamic_flows.business_early_phase import '
                                 'encode_six_decimal_digits_fields\n'
                                 '    return encode_six_decimal_digits_fields(memory, frame)\n'
                                 'raise SceneRefreshBoundary(target, frame, None)'}})
APPROVED.setdefault('business_objects',set()).update({'_append_object_sprite_fields', '_object_adjust_word_fields', '_object_clear_word_fields'})
APPROVED.setdefault((2, 'high_level_dynamic_flows.business_early_phase'),set()).update({'_allocation_fill_fields', '_allocation_move_fields', 'begin_scene_palette_lighten_fields', 'encode_six_decimal_digits_fields'})


# Narrative10164: genuine story platform calls and nonreturning reset tail.
DECLARATIONS.update({'_story_known_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long', 'returns': 'FirstDeploymentFrame', 'flow': 'memory.frame(frame)\nif target == 26570:\n    from ..high_level_main_flows.business_lowbank import poll_controller_with_z80_bus_fields\n    return poll_controller_with_z80_bus_fields(memory.state, frame)\nif target == 18754:\n    from ..high_level_remaining_flows.business_lowbank import lowbank_process_device_control_9_fields\n    return lowbank_process_device_control_9_fields(memory.state, frame)\nif target == 518:\n    from ..high_level_main_flows.business_boot import reset_console_frame_fields\n    return reset_console_frame_fields(memory.state, frame)\nif target == 238902:\n    return transfer_story_plane_dma_fields(memory, frame)\nelif target == 239772:\n    return transfer_story_overlay_dma_fields(memory, frame)\nelif target == 243614:\n    return dispatch_prologue_story_fields(memory, frame)\nelif target == 243618:\n    return dispatch_departure_story_fields(memory, frame)\nelif target == 243622:\n    return dispatch_arrival_story_fields(memory, frame)\nelif target == 243626:\n    return dispatch_finale_story_fields(memory, frame)\nelif target == 243630:\n    return dispatch_interlude_story_fields(memory, frame)\nelif target == 243644:\n    return initialize_prologue_story_fields(memory, frame)\nelif target == 243648:\n    return reveal_prologue_caption_fields(memory, frame)\nelif target == 243652:\n    return wait_prologue_portrait_fields(memory, frame)\nelif target == 243656:\n    return confirm_prologue_first_page_fields(memory, frame)\nelif target == 243660:\n    return wait_prologue_second_page_fields(memory, frame)\nelif target == 243664:\n    return reveal_prologue_second_portrait_fields(memory, frame)\nelif target == 243668:\n    return confirm_prologue_second_page_fields(memory, frame)\nelif target == 243672:\n    return begin_prologue_closing_caption_fields(memory, frame)\nelif target == 243676:\n    return finish_prologue_closing_caption_fields(memory, frame)\nelif target == 243680:\n    return confirm_prologue_exit_fields(memory, frame)\nelif target == 243920:\n    return draw_prologue_portrait_fields(memory, frame)\nelif target == 244400:\n    return animate_prologue_portrait_fields(memory, frame)\nelif target == 244454:\n    return cycle_prologue_colors_fields(memory, frame)\nelif target == 244674:\n    return select_prologue_sprite_fields(memory, frame)\nelif target == 246172:\n    return initialize_departure_story_fields(memory, frame)\nelif target == 246176:\n    return reveal_departure_caption_fields(memory, frame)\nelif target == 246180:\n    return confirm_departure_first_page_fields(memory, frame)\nelif target == 246184:\n    return wait_departure_second_page_fields(memory, frame)\nelif target == 246188:\n    return confirm_departure_second_page_fields(memory, frame)\nelif target == 246192:\n    return begin_departure_closing_caption_fields(memory, frame)\nelif target == 246196:\n    return finish_departure_closing_caption_fields(memory, frame)\nelif target == 246200:\n    return confirm_departure_exit_fields(memory, frame)\nelif target == 246330:\n    return load_departure_tile_rows_fields(memory, frame)\nelif target == 246402:\n    return write_departure_tile_row_fields(memory, frame)\nelif target == 246692:\n    return animate_departure_three_layers_fields(memory, frame)\nelif target == 246942:\n    return animate_departure_transition_fields(memory, frame)\nelif target == 247238:\n    return animate_departure_closing_layers_fields(memory, frame)\nelif target == 247500:\n    return select_departure_sprite_fields(memory, frame)\nelif target == 248186:\n    return initialize_interlude_story_fields(memory, frame)\nelif target == 248190:\n    return reveal_interlude_caption_fields(memory, frame)\nelif target == 248194:\n    return confirm_interlude_exit_fields(memory, frame)\nelif target == 248484:\n    return initialize_arrival_story_fields(memory, frame)\nelif target == 248488:\n    return reveal_arrival_caption_fields(memory, frame)\nelif target == 248492:\n    return confirm_arrival_first_page_fields(memory, frame)\nelif target == 248496:\n    return wait_arrival_second_page_fields(memory, frame)\nelif target == 248500:\n    return confirm_arrival_second_page_fields(memory, frame)\nelif target == 248504:\n    return begin_arrival_closing_caption_fields(memory, frame)\nelif target == 248508:\n    return finish_arrival_closing_caption_fields(memory, frame)\nelif target == 248512:\n    return confirm_arrival_exit_fields(memory, frame)\nelif target == 248766:\n    return animate_arrival_portrait_fields(memory, frame)\nelif target == 248962:\n    return animate_arrival_zoom_fields(memory, frame)\nelif target == 249240:\n    return animate_arrival_closing_portrait_fields(memory, frame)\nelif target == 249352:\n    return select_arrival_sprite_fields(memory, frame)\nelif target == 250236:\n    return initialize_finale_story_fields(memory, frame)\nelif target == 250240:\n    return reveal_finale_caption_fields(memory, frame)\nelif target == 250244:\n    return confirm_finale_first_page_fields(memory, frame)\nelif target == 250248:\n    return wait_finale_scroll_fields(memory, frame)\nelif target == 250252:\n    return advance_finale_scroll_fields(memory, frame)\nelif target == 250256:\n    return finish_finale_closing_caption_fields(memory, frame)\nelif target == 250260:\n    return confirm_finale_exit_fields(memory, frame)\nelif target == 250496:\n    return animate_finale_portrait_fields(memory, frame)\nelif target == 250694:\n    return move_finale_actor_diagonally_fields(memory, frame)\nelif target == 250908:\n    return animate_finale_closing_portrait_fields(memory, frame)\nelif target == 250972:\n    return select_finale_sprite_fields(memory, frame)\nelif target == 250976:\n    return select_finale_sprite_with_attributes_fields(memory, frame)\nelif target == 262058:\n    return advance_story_text_stream_fields(memory, frame)\nelif target == 262398:\n    return append_story_officer_number_fields(memory, frame)\nelif target == 262526:\n    return append_story_counter_pair_fields(memory, frame)\nelif target == 262670:\n    return append_story_counter_triple_fields(memory, frame)\nelif target == 240160:\n    return begin_scene_palette_darken_fields(memory, frame)\nelif target == 240184:\n    from ..high_level_dynamic_flows.business_early_phase import begin_scene_palette_lighten_fields\n    return begin_scene_palette_lighten_fields(memory, frame)\nelif target == 240334:\n    return read_vdp_plane_rle_rows_fields(memory, frame)\nelif target == 242352:\n    return set_vram_write_address_fields(memory, frame)\nelif target == 240532:\n    return copy_scene_palette_variant_fields(memory, frame)\nelif target == 44682:\n    return decode_glyph_rows_to_buffers_fields(memory, frame)\nelif target == 242392:\n    from ..high_level_dynamic_flows.business_early_phase import encode_six_decimal_digits_fields\n    return encode_six_decimal_digits_fields(memory, frame)\nraise SceneRefreshBoundary(target, frame, None)'}})
APPROVED.setdefault((2, 'high_level_main_flows.business_lowbank'), set()).update({'poll_controller_with_z80_bus_fields'})
APPROVED.setdefault((2, 'high_level_remaining_flows.business_lowbank'), set()).update({'lowbank_process_device_control_9_fields'})
APPROVED.setdefault((2, 'high_level_main_flows.business_boot'), set()).update({'reset_console_frame_fields'})

# B125 complete current Scene policy uses; no grammar/default fallback.
DECLARATIONS.update({'flush_scene_transfer_queue_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_remaining_flows.business_city import _resource_cost_frame\nfrom ..high_level_main_flows.business_movement_support import _movement_test\nfrom ..high_level_gameplay_flow.business_battle import _presentation_call_fields\nfrom ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory\nif type(memory) is not SceneRefreshMemory:\n    raise ValueError('actual same Scene transfer memory required')\nstate = memory.state\nframe = _resource_cost_frame(state, frame, 44294)\nqueued_words = state.read(4294955264, 2)\nframe = _movement_test(state, frame, queued_words, 16)\nif queued_words != 0:\n    frame = first_replace(frame, roster=memory.cursor_at(4294955264))\n\n    def child(actual, entered):\n        return write_vdp_packet_stream_fields(SceneRefreshMemory(actual.state), entered)\n    frame = _presentation_call_fields(BattlePresentationMemory(state), frame, 44306, child)\nfor address in (4294963994, 4294955264):\n    state.read(address, 2)\n    state.write(address, 2, 0)\n    frame = _movement_test(state, frame, 0, 16)\nreturn frame"}})


# Source140: one literal-plane internal entry, original physical owners unchanged.
DECLARATIONS.update({'_read_vdp_plane_rle_rows_fields_core': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, from_control: bool=False, from_literal: bool=False', 'returns': 'tuple', 'flow': "memory.frame(frame)\nif frame.stack_cursor is None:\n    raise SceneRefreshBoundary(240334, frame, None)\nmemory.sync_status(frame)\nif not from_control and (not from_literal):\n    memory.state.read(4294934528, 2)\n    frame = _scene_refresh_emit(memory, frame, 4294934528, 2, 0)\n    frame = _first_word(frame, 'offset_y', 32)\nmemory.sync_status(frame)\nif not from_literal:\n    memory.state.read(4294934530, 2)\n    frame = _scene_refresh_emit(memory, frame, 4294934530, 2, 0)\nframe = _scene_refresh_emit(memory, frame, 12582916, 2, 36610)\nframe = _first_word(frame, 'target_x', low16(frame.candidates.base))\nframe = _scene_render_call_fields(memory, frame, 242352, 240360)\nframe = _first_long(frame, 'distance', 0)\nmemory.sync_status(frame)\nmode = memory.state.read(4294934530, 2)\nframe = _scene_refresh_flags(memory, frame, mode, 2)\nif mode == 0:\n    frame, marker = _scene_tile_byte_fields(memory, frame, 'target_y')\nwhile True:\n    frame, high = _scene_tile_byte_fields(memory, frame, 'unit')\n    memory.sync_status(frame)\n    mode = memory.state.read(4294934530, 2)\n    frame = _scene_refresh_flags(memory, frame, mode, 2)\n    marker = low8(frame.target_y)\n    if mode == 0:\n        frame = _scene_render_compare(memory, frame, marker, high, 8)\n    literal = mode != 0 or marker != high\n    if literal:\n        frame = _scene_render_asl_word(memory, frame, 'unit', low16(frame.unit), 8)\n        frame, low = _scene_tile_byte_fields(memory, frame, 'unit')\n        memory.sync_status(frame)\n        mask = memory.state.read(4294934528, 2)\n        frame = _first_word(frame, 'unit', low16(frame.unit) | mask)\n        frame = _scene_refresh_emit(memory, frame, 12582912, 2, low16(frame.unit))\n        frame, discarded = _scene_plane_row_call_fields(memory, frame, 240400)\n        if discarded is not None:\n            return (frame, discarded)\n    else:\n        frame = _first_long(frame, 'count', 0)\n        frame, count = _scene_tile_byte_fields(memory, frame, 'count')\n        if count == 0:\n            return (memory.sync_status(frame), None)\n        frame, high = _scene_tile_byte_fields(memory, frame, 'unit')\n        frame = _scene_render_asl_word(memory, frame, 'unit', low16(frame.unit), 8)\n        frame, low = _scene_tile_byte_fields(memory, frame, 'unit')\n        remaining = count\n        while True:\n            memory.sync_status(frame)\n            mask = memory.state.read(4294934528, 2)\n            frame = _first_word(frame, 'unit', low16(frame.unit) | mask)\n            frame = _scene_refresh_emit(memory, frame, 12582912, 2, low16(frame.unit))\n            frame, discarded = _scene_plane_row_call_fields(memory, frame, 240428)\n            if discarded is not None:\n                return (frame, discarded)\n            frame = _scene_refresh_decrement(frame, 'count', remaining)\n            remaining = u16(remaining - 1)\n            if remaining == 65535:\n                break"}, 'read_vdp_plane_rle_rows_from_literal_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame, discarded = _read_vdp_plane_rle_rows_fields_core(memory, frame, False, True)\nreturn frame'}})


# Source145: actual phase BRA cells and live name CALL; original owners/lowerers unchanged.
DECLARATIONS.update({'_story_known_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long', 'returns': 'FirstDeploymentFrame', 'flow': 'memory.frame(frame)\nif target == 26570:\n    from ..high_level_main_flows.business_lowbank import poll_controller_with_z80_bus_fields\n    return poll_controller_with_z80_bus_fields(memory.state, frame)\nif target == 18754:\n    from ..high_level_remaining_flows.business_lowbank import lowbank_process_device_control_9_fields\n    return lowbank_process_device_control_9_fields(memory.state, frame)\nif target == 518:\n    from ..high_level_main_flows.business_boot import reset_console_frame_fields\n    return reset_console_frame_fields(memory.state, frame)\nif target == 238902:\n    return transfer_story_plane_dma_fields(memory, frame)\nelif target == 239772:\n    return transfer_story_overlay_dma_fields(memory, frame)\nelif target == 243614:\n    return dispatch_prologue_story_fields(memory, frame)\nelif target == 243618:\n    return dispatch_departure_story_fields(memory, frame)\nelif target == 243622:\n    return dispatch_arrival_story_fields(memory, frame)\nelif target == 243626:\n    return dispatch_finale_story_fields(memory, frame)\nelif target == 243630:\n    return dispatch_interlude_story_fields(memory, frame)\nelif target == 243644:\n    return initialize_prologue_story_fields(memory, frame)\nelif target == 243648:\n    return reveal_prologue_caption_fields(memory, frame)\nelif target == 243652:\n    return wait_prologue_portrait_fields(memory, frame)\nelif target == 243656:\n    return confirm_prologue_first_page_fields(memory, frame)\nelif target == 243660:\n    return wait_prologue_second_page_fields(memory, frame)\nelif target == 243664:\n    return reveal_prologue_second_portrait_fields(memory, frame)\nelif target == 243668:\n    return confirm_prologue_second_page_fields(memory, frame)\nelif target == 243672:\n    return begin_prologue_closing_caption_fields(memory, frame)\nelif target == 243676:\n    return finish_prologue_closing_caption_fields(memory, frame)\nelif target == 243680:\n    return confirm_prologue_exit_fields(memory, frame)\nelif target == 243920:\n    return draw_prologue_portrait_fields(memory, frame)\nelif target == 244400:\n    return animate_prologue_portrait_fields(memory, frame)\nelif target == 244454:\n    return cycle_prologue_colors_fields(memory, frame)\nelif target == 244674:\n    return select_prologue_sprite_fields(memory, frame)\nelif target == 246172:\n    return initialize_departure_story_fields(memory, frame)\nelif target == 246176:\n    return reveal_departure_caption_fields(memory, frame)\nelif target == 246180:\n    return confirm_departure_first_page_fields(memory, frame)\nelif target == 246184:\n    return wait_departure_second_page_fields(memory, frame)\nelif target == 246188:\n    return confirm_departure_second_page_fields(memory, frame)\nelif target == 246192:\n    return begin_departure_closing_caption_fields(memory, frame)\nelif target == 246196:\n    return finish_departure_closing_caption_fields(memory, frame)\nelif target == 246200:\n    return confirm_departure_exit_fields(memory, frame)\nelif target == 246330:\n    return load_departure_tile_rows_fields(memory, frame)\nelif target == 246402:\n    return write_departure_tile_row_fields(memory, frame)\nelif target == 246692:\n    return animate_departure_three_layers_fields(memory, frame)\nelif target == 246942:\n    return animate_departure_transition_fields(memory, frame)\nelif target == 247238:\n    return animate_departure_closing_layers_fields(memory, frame)\nelif target == 247500:\n    return select_departure_sprite_fields(memory, frame)\nelif target == 248186:\n    return initialize_interlude_story_fields(memory, frame)\nelif target == 248190:\n    return reveal_interlude_caption_fields(memory, frame)\nelif target == 248194:\n    return confirm_interlude_exit_fields(memory, frame)\nelif target == 248484:\n    return initialize_arrival_story_fields(memory, frame)\nelif target == 248488:\n    return reveal_arrival_caption_fields(memory, frame)\nelif target == 248492:\n    return confirm_arrival_first_page_fields(memory, frame)\nelif target == 248496:\n    return wait_arrival_second_page_fields(memory, frame)\nelif target == 248500:\n    return confirm_arrival_second_page_fields(memory, frame)\nelif target == 248504:\n    return begin_arrival_closing_caption_fields(memory, frame)\nelif target == 248508:\n    return finish_arrival_closing_caption_fields(memory, frame)\nelif target == 248512:\n    return confirm_arrival_exit_fields(memory, frame)\nelif target == 248766:\n    return animate_arrival_portrait_fields(memory, frame)\nelif target == 248962:\n    return animate_arrival_zoom_fields(memory, frame)\nelif target == 249240:\n    return animate_arrival_closing_portrait_fields(memory, frame)\nelif target == 249352:\n    return select_arrival_sprite_fields(memory, frame)\nelif target == 250236:\n    return initialize_finale_story_fields(memory, frame)\nelif target == 250240:\n    return reveal_finale_caption_fields(memory, frame)\nelif target == 250244:\n    return confirm_finale_first_page_fields(memory, frame)\nelif target == 250248:\n    return wait_finale_scroll_fields(memory, frame)\nelif target == 250252:\n    return advance_finale_scroll_fields(memory, frame)\nelif target == 250256:\n    return finish_finale_closing_caption_fields(memory, frame)\nelif target == 250260:\n    return confirm_finale_exit_fields(memory, frame)\nelif target == 250496:\n    return animate_finale_portrait_fields(memory, frame)\nelif target == 250694:\n    return move_finale_actor_diagonally_fields(memory, frame)\nelif target == 250908:\n    return animate_finale_closing_portrait_fields(memory, frame)\nelif target == 250972:\n    return select_finale_sprite_fields(memory, frame)\nelif target == 250976:\n    return select_finale_sprite_with_attributes_fields(memory, frame)\nelif target == 262058:\n    return advance_story_text_stream_fields(memory, frame)\nelif target == 262398:\n    return append_story_officer_number_fields(memory, frame)\nelif target == 262526:\n    return append_story_counter_pair_fields(memory, frame)\nelif target == 262670:\n    return append_story_counter_triple_fields(memory, frame)\nelif target == 240160:\n    return begin_scene_palette_darken_fields(memory, frame)\nelif target == 240184:\n    from ..high_level_dynamic_flows.business_early_phase import begin_scene_palette_lighten_fields\n    return begin_scene_palette_lighten_fields(memory, frame)\nelif target == 240334:\n    return read_vdp_plane_rle_rows_fields(memory, frame)\nelif target == 242352:\n    return set_vram_write_address_fields(memory, frame)\nelif target == 240532:\n    return copy_scene_palette_variant_fields(memory, frame)\nelif target == 44682:\n    return decode_glyph_rows_to_buffers_fields(memory, frame)\nelif target == 242392:\n    from ..high_level_dynamic_flows.business_early_phase import encode_six_decimal_digits_fields\n    return encode_six_decimal_digits_fields(memory, frame)\nif target == 262850:\n    from ..high_level_dynamic_flows.business_actions import upload_object_officer_name_frame_fields\n    return upload_object_officer_name_frame_fields(memory.state, frame)\nif target == 240322:\n    from ..high_level_main_flows.business_scene_support import decode_high_plane_rows_fields\n    return decode_high_plane_rows_fields(memory.state, frame)\nraise SceneRefreshBoundary(target, frame, None)'}})
APPROVED.setdefault((2, 'high_level_dynamic_flows.business_actions'), set()).update(('upload_object_officer_name_frame_fields',))

# B113 original39664 marker read is outside the39666 payload loop.
DECLARATIONS.update({'write_vdp_word_rle_stream_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, video: Word | None=None', 'returns': 'FirstDeploymentFrame', 'flow': "memory.frame(frame)\nframe = _scene_refresh_emit(memory, frame, 12582916, 2, 36610)\nframe = _scene_render_call_fields(memory, frame, 242352, 235108, video)\nsource = frame.roster\nmarker = source.byte()\nframe = first_replace(frame, roster=source.advance(1))\nframe = _first_byte(frame, 'target_y', marker)\nwhile True:\n    high = frame.roster.byte()\n    frame = first_replace(frame, roster=frame.roster.advance(1))\n    frame = _first_byte(frame, 'unit', high)\n    frame = _scene_render_compare(memory, frame, marker, high, 8)\n    if marker != high:\n        low = frame.roster.byte()\n        frame = first_replace(frame, roster=frame.roster.advance(1))\n        frame = _first_byte(frame, 'distance', low)\n        original = None if frame.unit is None else low16(frame.unit)\n        frame = _scene_render_asl_word(memory, frame, 'unit', original, 8)\n        frame = _first_byte(frame, 'unit', low)\n        frame = _scene_refresh_emit(memory, frame, 12582912, 2, high << 8 | low)\n    else:\n        frame = _first_long(frame, 'count', 0)\n        counter = frame.roster.byte()\n        frame = first_replace(frame, roster=frame.roster.advance(1))\n        frame = _first_byte(frame, 'count', counter)\n        if counter == 0:\n            return memory.sync_status(frame)\n        high = frame.roster.byte()\n        frame = first_replace(frame, roster=frame.roster.advance(1))\n        frame = _first_byte(frame, 'distance', high)\n        low = frame.roster.byte()\n        frame = first_replace(frame, roster=frame.roster.advance(1))\n        frame = _first_byte(frame, 'unit', low)\n        original = None if frame.distance is None else low16(frame.distance)\n        frame = _scene_render_asl_word(memory, frame, 'distance', original, 8)\n        frame = _first_byte(frame, 'distance', low)\n        while True:\n            frame = _scene_refresh_emit(memory, frame, 12582912, 2, high << 8 | low)\n            frame = _scene_refresh_decrement(frame, 'count', counter)\n            counter = u16(counter - 1)\n            if counter == 65535:\n                break"}})

# B168: seven original story darken CALLs; one exact shared helper.
DECLARATIONS.update({'_story_darken_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _story_move_fields(memory, frame, 'target_x', 1, 32)\nreturn _story_call_fields(memory, frame, 240160, continuation)"}})

# B169: exact arrival3AAC2 prefix dependency; no wider imports.
APPROVED[(2, 'high_level_main_flows.business_scene_support')] = {'decode_high_plane_rows_fields'}
