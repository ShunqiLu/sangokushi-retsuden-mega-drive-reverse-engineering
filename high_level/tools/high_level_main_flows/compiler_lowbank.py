"""Restricted business-text admission and ordinary mnemonic lowering.
An intermediate fixed-structure compiler, not arbitrary Python or CPU proof.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import BUSINESS_LOWBANK_BINDINGS

APPROVED={'business_lowbank': {'poll_controller_with_z80_bus', 'upload_selected_tile_row', 'poll_two_controller_ports_alternate_1', 'release_z80_reset', 'poll_two_controller_ports'}, 'contexts_lowbank': {'DrawSceneFooterGlyphsInput', 'PollTwoControllerPortsResult', 'RefreshScenePalettesResult', 'DrawSceneHeaderGlyphsResult', 'ReleaseZ80ResetResult', 'DrawCurrentResourceGlyphsInput', 'UploadSelectedTileRowResult', 'ConfigureControllerOutputsInput', 'UploadSelectedTileRowInput', 'PollWorldMapInputResult', 'InitializeZ80SoundImageResult', 'UploadWorldMapPaletteResult', 'UploadSelectedModeTileRowsResult', 'PacketTransferValues', 'QueueSoundWordListInput', 'UploadWorldMapPaletteInput', 'ReleaseZ80ResetInput', 'InitializeSceneGrowthAndTilesResult', 'UploadSelectedModeTileRowsInput', 'PollTwoControllerPortsInput', 'DrawSceneHeaderGlyphsInput', 'DrawSceneFooterGlyphsResult', 'InitializeSceneGrowthAndTilesInput', 'InitializeZ80SoundImageInput', 'PollControllerWithZ80BusInput', 'PollTwoControllerPortsAlternate1Input', 'InitializeSceneGrowthAndTilesService1', 'PollTwoControllerPortsAlternate1Result', 'QueueSoundWordListResult', 'RefreshScenePalettesInput', 'UploadSelectionLayoutInput', 'UploadSelectionLayoutResult', 'PollWorldMapInputInput', 'ConfigureControllerOutputsResult', 'PollControllerWithZ80BusResult', 'DrawCurrentResourceGlyphsResult', 'PollWorldMapInputService1'}, 'domain': {'replace_word', 'u16', 'replace_byte', 's16', 's8', 'swap_words', 'u8', 'low8', 'low16', 'checked_state', 'u32', 'SceneState', 'Boundary'}, 'services': {'flush_scene_transfer_queue', 'clear_video_sprite_plane', 'expand_glyph_stream', 'call_target', 'GlyphColors', 'decode_glyph_rows_to_buffers'}, 'contexts_tick': {'MapTickFrame', 'checked_tick_frame'}, 'dataclasses': {'replace'}}

DECLARATIONS={'poll_world_map_input': {'signature': 'state: SceneState, inputs: PollWorldMapInputInput', 'returns': 'PollWorldMapInputResult', 'flow': "checked_state(state)\nif type(inputs) is not PollWorldMapInputInput:\n    raise ValueError('function-specific typed input required')\ninputs.validate(state)\nraise Boundary('4890 requires the complete current MapTickFrame including spill')"},
 'upload_world_map_palette': {'signature': 'state: SceneState, inputs: UploadWorldMapPaletteInput',
                              'returns': 'UploadWorldMapPaletteResult',
                              'flow': 'checked_state(state)\n'
                                      'if type(inputs) is not UploadWorldMapPaletteInput:\n'
                                      "    raise ValueError('function-specific typed input required')\n"
                                      'inputs.validate(state)\n'
                                      'value = inputs.value\n'
                                      'arithmetic_carry = False\n'
                                      'arithmetic_overflow = False\n'
                                      'value_is_zero = False\n'
                                      'value_is_negative = False\n'
                                      'state.write(12582916, 4, u32(2080374786))\n'
                                      'read_value_1 = state.read(4294963990, 2)\n'
                                      'value = replace_word(value, u16(read_value_1))\n'
                                      'retained_value_2 = low16(value)\n'
                                      'value = replace_word(value, u16(-retained_value_2))\n'
                                      'state.write(12582912, 2, u16(low16(value)))\n'
                                      'read_value_3 = state.read(4294963992, 2)\n'
                                      'value = replace_word(value, u16(read_value_3))\n'
                                      'retained_value_4 = low16(value)\n'
                                      'value = replace_word(value, u16(-retained_value_4))\n'
                                      'state.write(12582912, 2, u16(low16(value)))\n'
                                      'state.write(12582916, 4, u32(1073741840))\n'
                                      'read_value_5 = state.read(4294963986, 2)\n'
                                      'state.write(12582912, 2, u16(read_value_5))\n'
                                      'read_value_6 = state.read(4294963988, 2)\n'
                                      'state.write(12582912, 2, u16(read_value_6))\n'
                                      'tested_value = u16(read_value_6)\n'
                                      'value_is_zero = tested_value == 0\n'
                                      'value_is_negative = bool(tested_value & 32768)\n'
                                      'arithmetic_carry = False\n'
                                      'arithmetic_overflow = False\n'
                                      'return UploadWorldMapPaletteResult(value=value, '
                                      'carry=arithmetic_carry, zero=value_is_zero, '
                                      'negative=value_is_negative, overflow=arithmetic_overflow)'},
 'draw_scene_header_glyphs': {'signature': 'state: SceneState, inputs: DrawSceneHeaderGlyphsInput',
                              'returns': 'DrawSceneHeaderGlyphsResult',
                              'flow': 'checked_state(state)\n'
                                      'if type(inputs) is not DrawSceneHeaderGlyphsInput:\n'
                                      "    raise ValueError('function-specific typed input required')\n"
                                      'inputs.validate(state)\n'
                                      'destination = None\n'
                                      'source = None\n'
                                      'port = inputs.port\n'
                                      'value = inputs.value\n'
                                      'field = inputs.field\n'
                                      'row = inputs.row\n'
                                      'offset = inputs.offset\n'
                                      'arithmetic_carry = False\n'
                                      'arithmetic_overflow = False\n'
                                      'value_is_zero = False\n'
                                      'value_is_negative = False\n'
                                      'destination = state.table_at(u32(565756))\n'
                                      'source = state.table_at(u32(4294955776))\n'
                                      'row = replace_word(row, u16(1))\n'
                                      'from .services import decode_glyph_rows_to_buffers\n'
                                      'logical_result_1 = decode_glyph_rows_to_buffers(state, '
                                      'destination.cursor(), source.cursor(), value, field, row)\n'
                                      'destination, source = (logical_result_1.source, '
                                      'logical_result_1.destination)\n'
                                      'value, field, row = (logical_result_1.background, '
                                      'logical_result_1.foreground, logical_result_1.remaining)\n'
                                      'destination = state.table_at(u32(565760))\n'
                                      'row = replace_word(row, u16(9))\n'
                                      'from .services import decode_glyph_rows_to_buffers\n'
                                      'logical_result_2 = decode_glyph_rows_to_buffers(state, '
                                      'destination.cursor(), source.cursor(), value, field, row)\n'
                                      'destination, source = (logical_result_2.source, '
                                      'logical_result_2.destination)\n'
                                      'value, field, row = (logical_result_2.background, '
                                      'logical_result_2.foreground, logical_result_2.remaining)\n'
                                      'state.write(12582916, 4, u32(1509949440))\n'
                                      'source = state.table_at(u32(4294955776))\n'
                                      'offset = replace_word(offset, u16(383))\n'
                                      'while True:\n'
                                      '    read_value_3 = state.read(u32(source.base + 0), 4)\n'
                                      '    source = source.advance(4)\n'
                                      '    state.write(u32(port.base + 0), 4, u32(read_value_3))\n'
                                      '    tested_value = u32(read_value_3)\n'
                                      '    value_is_zero = tested_value == 0\n'
                                      '    value_is_negative = bool(tested_value & 2147483648)\n'
                                      '    arithmetic_carry = False\n'
                                      '    arithmetic_overflow = False\n'
                                      '    offset = replace_word(offset, u16(low16(offset) - 1))\n'
                                      '    if low16(offset) != 65535:\n'
                                      '        continue\n'
                                      '    break\n'
                                      'return DrawSceneHeaderGlyphsResult(destination=destination, '
                                      'source=source, value=value, field=field, row=row, offset=offset, '
                                      'carry=arithmetic_carry, zero=value_is_zero, '
                                      'negative=value_is_negative, overflow=arithmetic_overflow)'},
 'upload_selection_layout': {'signature': 'state: SceneState, inputs: UploadSelectionLayoutInput',
                             'returns': 'UploadSelectionLayoutResult',
                             'flow': 'checked_state(state)\n'
                                     'if type(inputs) is not UploadSelectionLayoutInput:\n'
                                     "    raise ValueError('function-specific typed input required')\n"
                                     'inputs.validate(state)\n'
                                     'destination = None\n'
                                     'offset = inputs.offset\n'
                                     'arithmetic_carry = False\n'
                                     'arithmetic_overflow = False\n'
                                     'value_is_zero = False\n'
                                     'value_is_negative = False\n'
                                     'state.write(12582916, 4, u32(1879048193))\n'
                                     'destination = state.table_at(u32(564700))\n'
                                     'offset = replace_word(offset, u16(23))\n'
                                     'while True:\n'
                                     '    read_value_1 = state.read(u32(destination.base + 0), 4)\n'
                                     '    destination = destination.advance(4)\n'
                                     '    state.write(12582912, 4, u32(read_value_1))\n'
                                     '    offset = replace_word(offset, u16(low16(offset) - 1))\n'
                                     '    if low16(offset) != 65535:\n'
                                     '        continue\n'
                                     '    break\n'
                                     'state.write(12582916, 4, u32(1889533953))\n'
                                     'destination = state.table_at(u32(565084))\n'
                                     'offset = replace_word(offset, u16(7))\n'
                                     'while True:\n'
                                     '    read_value_2 = state.read(u32(destination.base + 0), 4)\n'
                                     '    destination = destination.advance(4)\n'
                                     '    state.write(12582912, 4, u32(read_value_2))\n'
                                     '    offset = replace_word(offset, u16(low16(offset) - 1))\n'
                                     '    if low16(offset) != 65535:\n'
                                     '        continue\n'
                                     '    break\n'
                                     'state.write(12582916, 4, u32(1912602625))\n'
                                     'offset = replace_word(offset, u16(7))\n'
                                     'while True:\n'
                                     '    state.write(12582912, 4, u32(858993459))\n'
                                     '    offset = replace_word(offset, u16(low16(offset) - 1))\n'
                                     '    if low16(offset) != 65535:\n'
                                     '        continue\n'
                                     '    break\n'
                                     'destination = state.table_at(u32(565436))\n'
                                     'offset = replace_word(offset, u16(7))\n'
                                     'while True:\n'
                                     '    read_value_3 = state.read(u32(destination.base + 0), 4)\n'
                                     '    destination = destination.advance(4)\n'
                                     '    state.write(12582912, 4, u32(read_value_3))\n'
                                     '    tested_value = u32(read_value_3)\n'
                                     '    value_is_zero = tested_value == 0\n'
                                     '    value_is_negative = bool(tested_value & 2147483648)\n'
                                     '    arithmetic_carry = False\n'
                                     '    arithmetic_overflow = False\n'
                                     '    offset = replace_word(offset, u16(low16(offset) - 1))\n'
                                     '    if low16(offset) != 65535:\n'
                                     '        continue\n'
                                     '    break\n'
                                     'return UploadSelectionLayoutResult(destination=destination, '
                                     'offset=offset, carry=arithmetic_carry, zero=value_is_zero, '
                                     'negative=value_is_negative, overflow=arithmetic_overflow)'},
 'draw_scene_footer_glyphs': {'signature': 'state: SceneState, inputs: DrawSceneFooterGlyphsInput',
                              'returns': 'DrawSceneFooterGlyphsResult',
                              'flow': 'checked_state(state)\n'
                                      'if type(inputs) is not DrawSceneFooterGlyphsInput:\n'
                                      "    raise ValueError('function-specific typed input required')\n"
                                      'inputs.validate(state)\n'
                                      'destination = None\n'
                                      'source = None\n'
                                      'port = inputs.port\n'
                                      'value = inputs.value\n'
                                      'field = inputs.field\n'
                                      'tile = inputs.tile\n'
                                      'row = inputs.row\n'
                                      'arithmetic_carry = False\n'
                                      'arithmetic_overflow = False\n'
                                      'value_is_zero = False\n'
                                      'value_is_negative = False\n'
                                      'destination = state.table_at(u32(566310))\n'
                                      'source = state.table_at(u32(4294955776))\n'
                                      'row = replace_word(row, u16(9))\n'
                                      'from .services import expand_glyph_stream, GlyphColors\n'
                                      'logical_result_1 = expand_glyph_stream(state, '
                                      'destination.cursor(), source.cursor(), GlyphColors(value, '
                                      'field), row)\n'
                                      'destination, source, row = (logical_result_1.tokens, '
                                      'logical_result_1.destination, '
                                      'logical_result_1.remaining_carrier)\n'
                                      'state.write(12582916, 4, u32(1891631105))\n'
                                      'source = state.table_at(u32(4294955776))\n'
                                      'tile = replace_word(tile, u16(79))\n'
                                      'while True:\n'
                                      '    read_value_2 = state.read(u32(source.base + 0), 4)\n'
                                      '    source = source.advance(4)\n'
                                      '    state.write(u32(port.base + 0), 4, u32(read_value_2))\n'
                                      '    tested_value = u32(read_value_2)\n'
                                      '    value_is_zero = tested_value == 0\n'
                                      '    value_is_negative = bool(tested_value & 2147483648)\n'
                                      '    arithmetic_carry = False\n'
                                      '    arithmetic_overflow = False\n'
                                      '    tile = replace_word(tile, u16(low16(tile) - 1))\n'
                                      '    if low16(tile) != 65535:\n'
                                      '        continue\n'
                                      '    break\n'
                                      'return DrawSceneFooterGlyphsResult(destination=destination, '
                                      'source=source, tile=tile, row=row, carry=arithmetic_carry, '
                                      'zero=value_is_zero, negative=value_is_negative, '
                                      'overflow=arithmetic_overflow)'},
 'draw_current_resource_glyphs': {'signature': 'state: SceneState, inputs: '
                                               'DrawCurrentResourceGlyphsInput',
                                  'returns': 'DrawCurrentResourceGlyphsResult',
                                  'flow': 'checked_state(state)\n'
                                          'if type(inputs) is not DrawCurrentResourceGlyphsInput:\n'
                                          "    raise ValueError('function-specific typed input "
                                          "required')\n"
                                          'inputs.validate(state)\n'
                                          'destination = None\n'
                                          'value = inputs.value\n'
                                          'arithmetic_carry = False\n'
                                          'arithmetic_overflow = False\n'
                                          'value_is_zero = False\n'
                                          'value_is_negative = False\n'
                                          'destination = state.table_at(u32(564988))\n'
                                          'state.write(12582916, 4, u32(1738539009))\n'
                                          'value = replace_word(value, u16(23))\n'
                                          'while True:\n'
                                          '    read_value_1 = state.read(u32(destination.base + 0), 4)\n'
                                          '    destination = destination.advance(4)\n'
                                          '    state.write(12582912, 4, u32(read_value_1))\n'
                                          '    tested_value = u32(read_value_1)\n'
                                          '    value_is_zero = tested_value == 0\n'
                                          '    value_is_negative = bool(tested_value & 2147483648)\n'
                                          '    arithmetic_carry = False\n'
                                          '    arithmetic_overflow = False\n'
                                          '    value = replace_word(value, u16(low16(value) - 1))\n'
                                          '    if low16(value) != 65535:\n'
                                          '        continue\n'
                                          '    break\n'
                                          'return '
                                          'DrawCurrentResourceGlyphsResult(destination=destination, '
                                          'value=value, carry=arithmetic_carry, zero=value_is_zero, '
                                          'negative=value_is_negative, overflow=arithmetic_overflow)'},
 'configure_controller_outputs': {'signature': 'state: SceneState, inputs: '
                                               'ConfigureControllerOutputsInput',
                                  'returns': 'ConfigureControllerOutputsResult',
                                  'flow': 'checked_state(state)\n'
                                          'if type(inputs) is not ConfigureControllerOutputsInput:\n'
                                          "    raise ValueError('function-specific typed input "
                                          "required')\n"
                                          'inputs.validate(state)\n'
                                          'value = 0\n'
                                          'arithmetic_carry = False\n'
                                          'arithmetic_overflow = False\n'
                                          'value_is_zero = False\n'
                                          'value_is_negative = False\n'
                                          'value = u32(u32(64))\n'
                                          'state.write(10551305, 1, u8(low8(value)))\n'
                                          'state.write(10551307, 1, u8(low8(value)))\n'
                                          'state.write(10551309, 1, u8(low8(value)))\n'
                                          'tested_value = u8(low8(value))\n'
                                          'value_is_zero = tested_value == 0\n'
                                          'value_is_negative = bool(tested_value & 128)\n'
                                          'arithmetic_carry = False\n'
                                          'arithmetic_overflow = False\n'
                                          'return ConfigureControllerOutputsResult(value=value, '
                                          'carry=arithmetic_carry, zero=value_is_zero, '
                                          'negative=value_is_negative, overflow=arithmetic_overflow)'},
 'poll_controller_with_z80_bus': {'signature': 'state: SceneState, inputs: '
                                               'PollControllerWithZ80BusInput',
                                  'returns': 'PollControllerWithZ80BusResult',
                                  'flow': 'checked_state(state)\n'
                                          'if type(inputs) is not PollControllerWithZ80BusInput:\n'
                                          "    raise ValueError('function-specific typed input "
                                          "required')\n"
                                          'inputs.validate(state)\n'
                                          'destination = None\n'
                                          'source = None\n'
                                          'value = inputs.value\n'
                                          'field = inputs.field\n'
                                          'tile = inputs.tile\n'
                                          'arithmetic_carry = False\n'
                                          'arithmetic_overflow = False\n'
                                          'value_is_zero = False\n'
                                          'value_is_negative = False\n'
                                          'state.write(10555648, 2, u16(256))\n'
                                          'while True:\n'
                                          '    read_value_1 = state.read(10555648, 1)\n'
                                          '    value_is_zero = not bool(read_value_1 & 1 << 0 % 8)\n'
                                          '    if not value_is_zero:\n'
                                          '        continue\n'
                                          '    break\n'
                                          'from .business_lowbank import poll_two_controller_ports\n'
                                          'from .contexts_lowbank import PollTwoControllerPortsInput\n'
                                          'call_result_2 = poll_two_controller_ports(state, '
                                          'PollTwoControllerPortsInput(value=value, field=field, '
                                          'tile=tile))\n'
                                          'destination = call_result_2.destination\n'
                                          'source = call_result_2.source\n'
                                          'value = call_result_2.value\n'
                                          'field = call_result_2.field\n'
                                          'tile = call_result_2.tile\n'
                                          'arithmetic_carry = call_result_2.carry\n'
                                          'value_is_zero = call_result_2.zero\n'
                                          'value_is_negative = call_result_2.negative\n'
                                          'arithmetic_overflow = call_result_2.overflow\n'
                                          'state.write(10555648, 2, u16(0))\n'
                                          'tested_value = u16(0)\n'
                                          'value_is_zero = tested_value == 0\n'
                                          'value_is_negative = bool(tested_value & 32768)\n'
                                          'arithmetic_carry = False\n'
                                          'arithmetic_overflow = False\n'
                                          'return '
                                          'PollControllerWithZ80BusResult(destination=destination, '
                                          'source=source, value=value, field=field, tile=tile, '
                                          'carry=arithmetic_carry, zero=value_is_zero, '
                                          'negative=value_is_negative, overflow=arithmetic_overflow)'},
 'poll_two_controller_ports': {'signature': 'state: SceneState, inputs: PollTwoControllerPortsInput',
                               'returns': 'PollTwoControllerPortsResult',
                               'flow': 'checked_state(state)\n'
                                       'if type(inputs) is not PollTwoControllerPortsInput:\n'
                                       "    raise ValueError('function-specific typed input required')\n"
                                       'inputs.validate(state)\n'
                                       'destination = None\n'
                                       'source = None\n'
                                       'value = inputs.value\n'
                                       'field = inputs.field\n'
                                       'tile = inputs.tile\n'
                                       'arithmetic_carry = False\n'
                                       'arithmetic_overflow = False\n'
                                       'value_is_zero = False\n'
                                       'value_is_negative = False\n'
                                       'destination = state.table_at(u32(4294964738))\n'
                                       'source = state.table_at(u32(10551299))\n'
                                       'from .business_lowbank import '
                                       'poll_two_controller_ports_alternate_1\n'
                                       'from .contexts_lowbank import '
                                       'PollTwoControllerPortsAlternate1Input\n'
                                       'call_result_1 = poll_two_controller_ports_alternate_1(state, '
                                       'PollTwoControllerPortsAlternate1Input(destination=destination, '
                                       'source=source, value=value, field=field, tile=tile))\n'
                                       'destination = call_result_1.destination\n'
                                       'source = call_result_1.source\n'
                                       'value = call_result_1.value\n'
                                       'field = call_result_1.field\n'
                                       'tile = call_result_1.tile\n'
                                       'arithmetic_carry = call_result_1.carry\n'
                                       'value_is_zero = call_result_1.zero\n'
                                       'value_is_negative = call_result_1.negative\n'
                                       'arithmetic_overflow = call_result_1.overflow\n'
                                       'source = state.table_at(u32(u32(source.base + 2)))\n'
                                       'state.write(u32(source.base + 0), 1, u8(0))\n'
                                       'read_value_2 = state.read(u32(source.base + 0), 1)\n'
                                       'value = replace_byte(value, u8(read_value_2))\n'
                                       'shift_value_3 = low8(value)\n'
                                       'shift_count_4 = 2 & 63\n'
                                       'value = replace_byte(value, u8(shift_value_3 << '
                                       'shift_count_4))\n'
                                       'old_value_5 = u8(low8(value))\n'
                                       'amount_6 = u8(192)\n'
                                       'value = replace_byte(value, u8(old_value_5 & amount_6))\n'
                                       'state.write(u32(source.base + 0), 1, u8(64))\n'
                                       'read_value_7 = state.read(u32(source.base + 0), 1)\n'
                                       'field = replace_byte(field, u8(read_value_7))\n'
                                       'old_value_8 = u8(low8(field))\n'
                                       'amount_9 = u8(63)\n'
                                       'field = replace_byte(field, u8(old_value_8 & amount_9))\n'
                                       'old_value_10 = u8(low8(value))\n'
                                       'amount_11 = u8(low8(field))\n'
                                       'value = replace_byte(value, u8(old_value_10 | amount_11))\n'
                                       'retained_value_12 = low8(value)\n'
                                       'value = replace_byte(value, u8(~retained_value_12))\n'
                                       'field = replace_byte(field, u8(low8(value)))\n'
                                       'read_value_13 = state.read(u32(destination.base + 0), 1)\n'
                                       'tile = replace_byte(tile, u8(read_value_13))\n'
                                       'old_value_14 = u8(low8(value))\n'
                                       'amount_15 = u8(low8(tile))\n'
                                       'value = replace_byte(value, u8(old_value_14 ^ amount_15))\n'
                                       'state.write(u32(destination.base + 0), 1, u8(low8(field)))\n'
                                       'destination = destination.advance(1)\n'
                                       'old_value_16 = u8(low8(value))\n'
                                       'amount_17 = u8(low8(field))\n'
                                       'value = replace_byte(value, u8(old_value_16 & amount_17))\n'
                                       'state.write(u32(destination.base + 0), 1, u8(low8(value)))\n'
                                       'destination = destination.advance(1)\n'
                                       'tested_value = u8(low8(value))\n'
                                       'value_is_zero = tested_value == 0\n'
                                       'value_is_negative = bool(tested_value & 128)\n'
                                       'arithmetic_carry = False\n'
                                       'arithmetic_overflow = False\n'
                                       'return PollTwoControllerPortsResult(destination=destination, '
                                       'source=source, value=value, field=field, tile=tile, '
                                       'carry=arithmetic_carry, zero=value_is_zero, '
                                       'negative=value_is_negative, overflow=arithmetic_overflow)'},
 'poll_two_controller_ports_alternate_1': {'signature': 'state: SceneState, inputs: '
                                                        'PollTwoControllerPortsAlternate1Input',
                                           'returns': 'PollTwoControllerPortsAlternate1Result',
                                           'flow': 'checked_state(state)\n'
                                                   'if type(inputs) is not '
                                                   'PollTwoControllerPortsAlternate1Input:\n'
                                                   "    raise ValueError('function-specific typed input "
                                                   "required')\n"
                                                   'inputs.validate(state)\n'
                                                   'destination = inputs.destination\n'
                                                   'source = inputs.source\n'
                                                   'value = inputs.value\n'
                                                   'field = inputs.field\n'
                                                   'tile = inputs.tile\n'
                                                   'arithmetic_carry = False\n'
                                                   'arithmetic_overflow = False\n'
                                                   'value_is_zero = False\n'
                                                   'value_is_negative = False\n'
                                                   'state.write(u32(source.base + 0), 1, u8(0))\n'
                                                   'read_value_1 = state.read(u32(source.base + 0), 1)\n'
                                                   'value = replace_byte(value, u8(read_value_1))\n'
                                                   'shift_value_2 = low8(value)\n'
                                                   'shift_count_3 = 2 & 63\n'
                                                   'value = replace_byte(value, u8(shift_value_2 << '
                                                   'shift_count_3))\n'
                                                   'old_value_4 = u8(low8(value))\n'
                                                   'amount_5 = u8(192)\n'
                                                   'value = replace_byte(value, u8(old_value_4 & '
                                                   'amount_5))\n'
                                                   'state.write(u32(source.base + 0), 1, u8(64))\n'
                                                   'read_value_6 = state.read(u32(source.base + 0), 1)\n'
                                                   'field = replace_byte(field, u8(read_value_6))\n'
                                                   'old_value_7 = u8(low8(field))\n'
                                                   'amount_8 = u8(63)\n'
                                                   'field = replace_byte(field, u8(old_value_7 & '
                                                   'amount_8))\n'
                                                   'old_value_9 = u8(low8(value))\n'
                                                   'amount_10 = u8(low8(field))\n'
                                                   'value = replace_byte(value, u8(old_value_9 | '
                                                   'amount_10))\n'
                                                   'retained_value_11 = low8(value)\n'
                                                   'value = replace_byte(value, '
                                                   'u8(~retained_value_11))\n'
                                                   'field = replace_byte(field, u8(low8(value)))\n'
                                                   'read_value_12 = state.read(u32(destination.base + '
                                                   '0), 1)\n'
                                                   'tile = replace_byte(tile, u8(read_value_12))\n'
                                                   'old_value_13 = u8(low8(value))\n'
                                                   'amount_14 = u8(low8(tile))\n'
                                                   'value = replace_byte(value, u8(old_value_13 ^ '
                                                   'amount_14))\n'
                                                   'state.write(u32(destination.base + 0), 1, '
                                                   'u8(low8(field)))\n'
                                                   'destination = destination.advance(1)\n'
                                                   'old_value_15 = u8(low8(value))\n'
                                                   'amount_16 = u8(low8(field))\n'
                                                   'value = replace_byte(value, u8(old_value_15 & '
                                                   'amount_16))\n'
                                                   'state.write(u32(destination.base + 0), 1, '
                                                   'u8(low8(value)))\n'
                                                   'destination = destination.advance(1)\n'
                                                   'tested_value = u8(low8(value))\n'
                                                   'value_is_zero = tested_value == 0\n'
                                                   'value_is_negative = bool(tested_value & 128)\n'
                                                   'arithmetic_carry = False\n'
                                                   'arithmetic_overflow = False\n'
                                                   'return '
                                                   'PollTwoControllerPortsAlternate1Result(destination=destination, '
                                                   'source=source, value=value, field=field, tile=tile, '
                                                   'carry=arithmetic_carry, zero=value_is_zero, '
                                                   'negative=value_is_negative, '
                                                   'overflow=arithmetic_overflow)'},
 'initialize_z80_sound_image': {'signature': 'state: SceneState, inputs: InitializeZ80SoundImageInput',
                                'returns': 'InitializeZ80SoundImageResult',
                                'flow': 'checked_state(state)\n'
                                        'if type(inputs) is not InitializeZ80SoundImageInput:\n'
                                        "    raise ValueError('function-specific typed input "
                                        "required')\n"
                                        'inputs.validate(state)\n'
                                        'destination = None\n'
                                        'source = None\n'
                                        'value = inputs.value\n'
                                        'arithmetic_carry = False\n'
                                        'arithmetic_overflow = False\n'
                                        'value_is_zero = False\n'
                                        'value_is_negative = False\n'
                                        'state.write(10555648, 2, u16(256))\n'
                                        'from .business_lowbank import release_z80_reset\n'
                                        'from .contexts_lowbank import ReleaseZ80ResetInput\n'
                                        'call_result_1 = release_z80_reset(state, '
                                        'ReleaseZ80ResetInput())\n'
                                        'arithmetic_carry = call_result_1.carry\n'
                                        'value_is_zero = call_result_1.zero\n'
                                        'value_is_negative = call_result_1.negative\n'
                                        'arithmetic_overflow = call_result_1.overflow\n'
                                        'while True:\n'
                                        '    read_value_2 = state.read(10555648, 1)\n'
                                        '    value_is_zero = not bool(read_value_2 & 1 << 0 % 8)\n'
                                        '    if not value_is_zero:\n'
                                        '        continue\n'
                                        '    break\n'
                                        'destination = state.table_at(u32(27090))\n'
                                        'source = state.table_at(u32(10485760))\n'
                                        'value = replace_word(value, u16(4095))\n'
                                        'while True:\n'
                                        '    read_value_3 = state.read(u32(destination.base + 0), 1)\n'
                                        '    destination = destination.advance(1)\n'
                                        '    state.write(u32(source.base + 0), 1, u8(read_value_3))\n'
                                        '    source = source.advance(1)\n'
                                        '    value = replace_word(value, u16(low16(value) - 1))\n'
                                        '    if low16(value) != 65535:\n'
                                        '        continue\n'
                                        '    break\n'
                                        'destination = state.table_at(u32(31132))\n'
                                        'value = replace_word(value, u16(3583))\n'
                                        'while True:\n'
                                        '    read_value_4 = state.read(u32(destination.base + 0), 1)\n'
                                        '    destination = destination.advance(1)\n'
                                        '    state.write(u32(source.base + 0), 1, u8(read_value_4))\n'
                                        '    source = source.advance(1)\n'
                                        '    value = replace_word(value, u16(low16(value) - 1))\n'
                                        '    if low16(value) != 65535:\n'
                                        '        continue\n'
                                        '    break\n'
                                        'destination = state.table_at(u32(27050))\n'
                                        'source = state.table_at(u32(10492928))\n'
                                        'value = u32(u32(12))\n'
                                        'while True:\n'
                                        '    read_value_5 = state.read(u32(destination.base + 0), 1)\n'
                                        '    destination = destination.advance(1)\n'
                                        '    state.write(u32(source.base + 0), 1, u8(read_value_5))\n'
                                        '    source = source.advance(1)\n'
                                        '    value = replace_word(value, u16(low16(value) - 1))\n'
                                        '    if low16(value) != 65535:\n'
                                        '        continue\n'
                                        '    break\n'
                                        'from .business_lowbank import release_z80_reset\n'
                                        'from .contexts_lowbank import ReleaseZ80ResetInput\n'
                                        'call_result_6 = release_z80_reset(state, '
                                        'ReleaseZ80ResetInput())\n'
                                        'arithmetic_carry = call_result_6.carry\n'
                                        'value_is_zero = call_result_6.zero\n'
                                        'value_is_negative = call_result_6.negative\n'
                                        'arithmetic_overflow = call_result_6.overflow\n'
                                        'state.write(10555648, 2, u16(0))\n'
                                        'tested_value = u16(0)\n'
                                        'value_is_zero = tested_value == 0\n'
                                        'value_is_negative = bool(tested_value & 32768)\n'
                                        'arithmetic_carry = False\n'
                                        'arithmetic_overflow = False\n'
                                        'return InitializeZ80SoundImageResult(destination=destination, '
                                        'source=source, value=value, carry=arithmetic_carry, '
                                        'zero=value_is_zero, negative=value_is_negative, '
                                        'overflow=arithmetic_overflow)'},
 'release_z80_reset': {'signature': 'state: SceneState, inputs: ReleaseZ80ResetInput',
                       'returns': 'ReleaseZ80ResetResult',
                       'flow': 'checked_state(state)\n'
                               'if type(inputs) is not ReleaseZ80ResetInput:\n'
                               "    raise ValueError('function-specific typed input required')\n"
                               'inputs.validate(state)\n'
                               'arithmetic_carry = False\n'
                               'arithmetic_overflow = False\n'
                               'value_is_zero = False\n'
                               'value_is_negative = False\n'
                               'state.write(10555904, 2, u16(0))\n'
                               'state.write(10555904, 2, u16(256))\n'
                               'tested_value = u16(256)\n'
                               'value_is_zero = tested_value == 0\n'
                               'value_is_negative = bool(tested_value & 32768)\n'
                               'arithmetic_carry = False\n'
                               'arithmetic_overflow = False\n'
                               'return ReleaseZ80ResetResult(carry=arithmetic_carry, '
                               'zero=value_is_zero, negative=value_is_negative, '
                               'overflow=arithmetic_overflow)'},
 'queue_sound_word_list': {'signature': 'state: SceneState, inputs: QueueSoundWordListInput',
                           'returns': 'QueueSoundWordListResult',
                           'flow': 'checked_state(state)\n'
                                   'if type(inputs) is not QueueSoundWordListInput:\n'
                                   "    raise ValueError('function-specific typed input required')\n"
                                   'inputs.validate(state)\n'
                                   'source = None\n'
                                   'descriptor = None\n'
                                   'records = None\n'
                                   'value = inputs.value\n'
                                   'remaining = inputs.remaining\n'
                                   'arithmetic_carry = False\n'
                                   'arithmetic_overflow = False\n'
                                   'value_is_zero = False\n'
                                   'value_is_negative = False\n'
                                   'source = state.table_at(u32(33068))\n'
                                   'shift_value_1 = low16(value)\n'
                                   'shift_count_2 = 3 & 63\n'
                                   'value = replace_word(value, u16(shift_value_1 << shift_count_2))\n'
                                   'source = state.table_at(u32(u32(source.base + '
                                   's16(u16(low16(value))))))\n'
                                   'read_value_3 = state.read(u32(source.base + 0), 4)\n'
                                   'source = source.advance(4)\n'
                                   'descriptor = state.table_at(u32(read_value_3))\n'
                                   'read_value_4 = state.read(u32(source.base + 0), 2)\n'
                                   'source = source.advance(2)\n'
                                   'records = state.table_at(u32(u32(s16(u16(read_value_4)))))\n'
                                   'records = state.table_at(u32(u32(records.base + s16(u16(128)))))\n'
                                   'read_value_5 = state.read(u32(source.base + 0), 2)\n'
                                   'source = source.advance(2)\n'
                                   'remaining = replace_word(remaining, u16(read_value_5))\n'
                                   'while True:\n'
                                   '    read_value_6 = state.read(u32(descriptor.base + 0), 4)\n'
                                   '    descriptor = descriptor.advance(4)\n'
                                   '    state.write(u32(records.base + 0), 4, u32(read_value_6))\n'
                                   '    records = records.advance(4)\n'
                                   '    remaining = replace_word(remaining, u16(low16(remaining) - 1))\n'
                                   '    if low16(remaining) != 65535:\n'
                                   '        continue\n'
                                   '    break\n'
                                   'read_value_7 = state.read(4294963998, 2)\n'
                                   'old_value_8 = u16(read_value_7)\n'
                                   'amount_9 = u16(1)\n'
                                   'state.write(4294963998, 2, u16(old_value_8 + amount_9))\n'
                                   'tested_value = u16(old_value_8 + amount_9)\n'
                                   'value_is_zero = tested_value == 0\n'
                                   'value_is_negative = bool(tested_value & 32768)\n'
                                   'arithmetic_carry = old_value_8 + amount_9 > 65535\n'
                                   'arithmetic_overflow = bool(~(old_value_8 ^ amount_9) & (old_value_8 '
                                   '^ u16(old_value_8 + amount_9)) & 32768)\n'
                                   'return QueueSoundWordListResult(source=source, '
                                   'descriptor=descriptor, records=records, value=value, '
                                   'remaining=remaining, carry=arithmetic_carry, zero=value_is_zero, '
                                   'negative=value_is_negative, overflow=arithmetic_overflow)'},
 'initialize_scene_growth_and_tiles': {'signature': 'state: SceneState, inputs: '
                                                    'InitializeSceneGrowthAndTilesInput',
                                       'returns': 'InitializeSceneGrowthAndTilesResult',
                                       'flow': 'checked_state(state)\n'
                                               'if type(inputs) is not '
                                               'InitializeSceneGrowthAndTilesInput:\n'
                                               "    raise ValueError('function-specific typed input "
                                               "required')\n"
                                               'inputs.validate(state)\n'
                                               'destination = None\n'
                                               'value = inputs.value\n'
                                               'offset = inputs.offset\n'
                                               'limit = 0\n'
                                               'member = 0\n'
                                               'remaining = inputs.remaining\n'
                                               'arithmetic_carry = False\n'
                                               'arithmetic_overflow = False\n'
                                               'value_is_zero = False\n'
                                               'value_is_negative = False\n'
                                               'state.set_status_word(u16(9984))\n'
                                               'read_value_1 = state.read(4294964742, 2)\n'
                                               'value = replace_word(value, u16(read_value_1))\n'
                                               'old_value_2 = u8(low8(value))\n'
                                               'amount_3 = u8(191)\n'
                                               'value = replace_byte(value, u8(old_value_2 & '
                                               'amount_3))\n'
                                               'state.write(12582916, 2, u16(low16(value)))\n'
                                               'from .services import clear_video_sprite_plane\n'
                                               'clear_video_sprite_plane(state)\n'
                                               'state.write(12582916, 4, u32(1073741824))\n'
                                               'destination = state.table_at(u32(38230))\n'
                                               'value = replace_word(value, u16(439))\n'
                                               'while True:\n'
                                               '    read_value_5 = state.read(u32(destination.base + '
                                               '0), 4)\n'
                                               '    destination = destination.advance(4)\n'
                                               '    state.write(12582912, 4, u32(read_value_5))\n'
                                               '    value = replace_word(value, u16(low16(value) - 1))\n'
                                               '    if low16(value) != 65535:\n'
                                               '        continue\n'
                                               '    break\n'
                                               'limit = u32(u32(11))\n'
                                               'member = u32(u32(3))\n'
                                               'offset = replace_word(offset, u16(32769))\n'
                                               'value = u32(1176240131)\n'
                                               'while True:\n'
                                               '    remaining = replace_word(remaining, '
                                               'u16(low16(limit)))\n'
                                               '    state.write(12582916, 4, u32(value))\n'
                                               '    while True:\n'
                                               '        state.write(12582912, 2, u16(low16(offset)))\n'
                                               '        old_value_6 = u16(low16(offset))\n'
                                               '        amount_7 = u16(1)\n'
                                               '        offset = replace_word(offset, u16(old_value_6 + '
                                               'amount_7))\n'
                                               '        remaining = replace_word(remaining, '
                                               'u16(low16(remaining) - 1))\n'
                                               '        if low16(remaining) != 65535:\n'
                                               '            continue\n'
                                               '        break\n'
                                               '    old_value_8 = u32(value)\n'
                                               '    amount_9 = u32(8388608)\n'
                                               '    value = u32(old_value_8 + amount_9)\n'
                                               '    member = replace_word(member, u16(low16(member) - '
                                               '1))\n'
                                               '    if low16(member) != 65535:\n'
                                               '        continue\n'
                                               '    break\n'
                                               'read_value_10 = state.read(10551297, 1)\n'
                                               'value_is_zero = not bool(read_value_10 & 1 << 7 % 8)\n'
                                               'if not value_is_zero:\n'
                                               '    state.write(12582916, 2, u16(36610))\n'
                                               '    state.write(12582916, 4, u32(1714421763))\n'
                                               '    state.write(12582912, 2, u16(32821))\n'
                                               '    state.write(12582912, 2, u16(32822))\n'
                                               'value = u32(u32(0))\n'
                                               'service_result_11 = call_target(state, 33042, '
                                               'InitializeSceneGrowthAndTilesService1(destination=destination, '
                                               'value=value, offset=offset, limit=limit, member=member, '
                                               'remaining=remaining))\n'
                                               "raise Boundary('return ABI for "
                                               'InitializeSceneGrowthAndTilesService1 is not bound by '
                                               "this draft')\n"
                                               'state.write(4294964760, 2, u16(40))\n'
                                               'state.write(4294964744, 2, u16(300))\n'
                                               'state.set_status_word(u16(9472))\n'
                                               'state.write(4294964754, 2, u16(256))\n'
                                               'tested_value = u16(256)\n'
                                               'value_is_zero = tested_value == 0\n'
                                               'value_is_negative = bool(tested_value & 32768)\n'
                                               'arithmetic_carry = False\n'
                                               'arithmetic_overflow = False\n'
                                               'return '
                                               'InitializeSceneGrowthAndTilesResult(destination=destination, '
                                               'value=value, offset=offset, limit=limit, member=member, '
                                               'remaining=remaining, carry=arithmetic_carry, '
                                               'zero=value_is_zero, negative=value_is_negative, '
                                               'overflow=arithmetic_overflow)'},
 'refresh_scene_palettes': {'signature': 'state: SceneState, inputs: RefreshScenePalettesInput',
 'returns': 'RefreshScenePalettesResult',
 'flow': 'checked_state(state)\n'
         'if type(inputs) is not RefreshScenePalettesInput:\n'
         "    raise ValueError('function-specific typed input required')\n"
         'inputs.validate(state)\n'
         'fields = refresh_scene_palettes_fields(state)\n'
         'source = inputs.source if fields.source_if_written is None else '
         'fields.source_if_written\n'
         'return RefreshScenePalettesResult(destination=fields.destination, source=source, '
         'value=replace_word(inputs.value, fields.value_word), field=replace_word(inputs.field, '
         'fields.field_word), carry=fields.carry, zero=fields.zero, negative=fields.negative, '
         'overflow=fields.overflow)'},
 'upload_selected_mode_tile_rows': {'signature': 'state: SceneState, inputs: '
                                                 'UploadSelectedModeTileRowsInput',
                                    'returns': 'UploadSelectedModeTileRowsResult',
                                    'flow': 'checked_state(state)\n'
                                            'if type(inputs) is not UploadSelectedModeTileRowsInput:\n'
                                            "    raise ValueError('function-specific typed input "
                                            "required')\n"
                                            'inputs.validate(state)\n'
                                            'destination = inputs.destination\n'
                                            'port = None\n'
                                            'field = inputs.field\n'
                                            'tile = inputs.tile\n'
                                            'stack_cursor = inputs.stack_cursor\n'
                                            'arithmetic_carry = False\n'
                                            'arithmetic_overflow = False\n'
                                            'value_is_zero = False\n'
                                            'value_is_negative = False\n'
                                            'stack_cursor = stack_cursor.advance(-4)\n'
                                            'state.write(stack_cursor.base, 4, u32(destination.base))\n'
                                            'port = state.table_at(u32(12582912))\n'
                                            'destination = state.table_at(u32(42910))\n'
                                            'read_value_1 = state.read(4294964048, 2)\n'
                                            'tile = replace_word(tile, u16(read_value_1))\n'
                                            'shift_value_2 = low16(tile)\n'
                                            'shift_count_3 = 5 & 63\n'
                                            'tile = replace_word(tile, u16(shift_value_2 << '
                                            'shift_count_3))\n'
                                            'state.write(12582916, 4, u32(1092616195))\n'
                                            'from .business_lowbank import upload_selected_tile_row\n'
                                            'from .contexts_lowbank import UploadSelectedTileRowInput\n'
                                            'call_result_4 = upload_selected_tile_row(state, '
                                            'UploadSelectedTileRowInput(destination=destination, '
                                            'port=port, field=field, tile=tile))\n'
                                            'field = call_result_4.field\n'
                                            'tile = call_result_4.tile\n'
                                            'arithmetic_carry = call_result_4.carry\n'
                                            'value_is_zero = call_result_4.zero\n'
                                            'value_is_negative = call_result_4.negative\n'
                                            'arithmetic_overflow = call_result_4.overflow\n'
                                            'state.write(12582916, 4, u32(1101004803))\n'
                                            'tested_value = u32(1101004803)\n'
                                            'value_is_zero = tested_value == 0\n'
                                            'value_is_negative = bool(tested_value & 2147483648)\n'
                                            'arithmetic_carry = False\n'
                                            'arithmetic_overflow = False\n'
                                            'from .business_lowbank import upload_selected_tile_row\n'
                                            'from .contexts_lowbank import UploadSelectedTileRowInput\n'
                                            'call_result_5 = upload_selected_tile_row(state, '
                                            'UploadSelectedTileRowInput(destination=destination, '
                                            'port=port, field=field, tile=tile))\n'
                                            'field = call_result_5.field\n'
                                            'tile = call_result_5.tile\n'
                                            'arithmetic_carry = call_result_5.carry\n'
                                            'value_is_zero = call_result_5.zero\n'
                                            'value_is_negative = call_result_5.negative\n'
                                            'arithmetic_overflow = call_result_5.overflow\n'
                                            'read_value_6 = state.read(stack_cursor.base, 4)\n'
                                            'stack_cursor = stack_cursor.advance(4)\n'
                                            'destination = state.table_at(u32(read_value_6))\n'
                                            'return '
                                            'UploadSelectedModeTileRowsResult(destination=destination, '
                                            'port=port, field=field, tile=tile, carry=arithmetic_carry, '
                                            'zero=value_is_zero, negative=value_is_negative, '
                                            'overflow=arithmetic_overflow)'},
 'upload_selected_tile_row': {'signature': 'state: SceneState, inputs: UploadSelectedTileRowInput',
                              'returns': 'UploadSelectedTileRowResult',
                              'flow': 'checked_state(state)\n'
                                      'if type(inputs) is not UploadSelectedTileRowInput:\n'
                                      "    raise ValueError('function-specific typed input required')\n"
                                      'inputs.validate(state)\n'
                                      'destination = inputs.destination\n'
                                      'port = inputs.port\n'
                                      'field = inputs.field\n'
                                      'tile = inputs.tile\n'
                                      'arithmetic_carry = False\n'
                                      'arithmetic_overflow = False\n'
                                      'value_is_zero = False\n'
                                      'value_is_negative = False\n'
                                      'field = replace_word(field, u16(7))\n'
                                      'while True:\n'
                                      '    read_value_1 = state.read(u32(destination.base + '
                                      's16(low16(tile)) + 0), 2)\n'
                                      '    state.write(u32(port.base + 0), 2, u16(read_value_1))\n'
                                      '    old_value_2 = u16(low16(tile))\n'
                                      '    amount_3 = u16(2)\n'
                                      '    tile = replace_word(tile, u16(old_value_2 + amount_3))\n'
                                      '    tested_value = u16(old_value_2 + amount_3)\n'
                                      '    value_is_zero = tested_value == 0\n'
                                      '    value_is_negative = bool(tested_value & 32768)\n'
                                      '    arithmetic_carry = old_value_2 + amount_3 > 65535\n'
                                      '    arithmetic_overflow = bool(~(old_value_2 ^ amount_3) & '
                                      '(old_value_2 ^ u16(old_value_2 + amount_3)) & 32768)\n'
                                      '    field = replace_word(field, u16(low16(field) - 1))\n'
                                      '    if low16(field) != 65535:\n'
                                      '        continue\n'
                                      '    break\n'
                                      'return UploadSelectedTileRowResult(field=field, tile=tile, '
                                      'carry=arithmetic_carry, zero=value_is_zero, '
                                      'negative=value_is_negative, overflow=arithmetic_overflow)'}}


DECLARATIONS.update({'poll_world_map_input_frame': {'signature': 'state: SceneState, frame: MapTickFrame', 'returns': 'MapTickFrame', 'flow': "checked_tick_frame(frame, state)\nvalue = frame.motion_x\nfield = frame.motion_y\ntile = frame.attributes\nremaining = frame.control_latch\nfrom .business_lowbank import poll_controller_with_z80_bus\nfrom .contexts_lowbank import PollControllerWithZ80BusInput\ncall_result_1 = poll_controller_with_z80_bus(state, PollControllerWithZ80BusInput(value=value, field=field, tile=tile))\ndestination = call_result_1.destination\nsource = call_result_1.source\nvalue = call_result_1.value\nfield = call_result_1.field\ntile = call_result_1.tile\narithmetic_carry = call_result_1.carry\nvalue_is_zero = call_result_1.zero\nvalue_is_negative = call_result_1.negative\narithmetic_overflow = call_result_1.overflow\nport = state.table_at(u32(12582916))\nread_value_2 = state.read(4294964742, 2)\nremaining = replace_word(remaining, u16(read_value_2))\nold_value_3 = u8(low8(remaining))\namount_4 = u8(16)\nremaining = replace_byte(remaining, u8(old_value_3 | amount_4))\nstate.write(u32(port.base + 0), 2, u16(low16(remaining)))\nstate.write(10555648, 2, u16(256))\nstate.write(u32(port.base + 0), 4, u32(2483131200))\nstate.write(u32(port.base + 0), 4, u32(2533135616))\nstate.write(u32(port.base + 0), 2, u16(38783))\nstate.write(u32(port.base + 0), 2, u16(30720))\nstate.write(4294964768, 2, u16(130))\nread_value_5 = state.read(4294964768, 2)\nstate.write(u32(port.base + 0), 2, u16(read_value_5))\nread_value_6 = state.read(16727808, 1)\ncomparison_left = u8(read_value_6)\ncomparison_right = u8(0)\ntested_value = u8(comparison_left - comparison_right)\nvalue_is_zero = tested_value == 0\nvalue_is_negative = bool(tested_value & 128)\narithmetic_carry = comparison_left < comparison_right\narithmetic_overflow = bool((comparison_left ^ comparison_right) & (comparison_left ^ u8(comparison_left - comparison_right)) & 128)\nif not not value_is_zero:\n    state.write(10555648, 2, u16(0))\nread_value_7 = state.read(4294964742, 2)\nstate.write(u32(port.base + 0), 2, u16(read_value_7))\nread_value_8 = state.read(4294963998, 2)\ncomparison_left = u16(read_value_8)\ncomparison_right = u16(0)\ntested_value = u16(comparison_left - comparison_right)\nvalue_is_zero = tested_value == 0\nvalue_is_negative = bool(tested_value & 32768)\narithmetic_carry = comparison_left < comparison_right\narithmetic_overflow = bool((comparison_left ^ comparison_right) & (comparison_left ^ u16(comparison_left - comparison_right)) & 32768)\nif not value_is_zero:\n    port = state.table_at(u32(12582916))\n    read_value_9 = state.read(4294964742, 2)\n    remaining = replace_word(remaining, u16(read_value_9))\n    old_value_10 = u8(low8(remaining))\n    amount_11 = u8(16)\n    remaining = replace_byte(remaining, u8(old_value_10 | amount_11))\n    state.write(u32(port.base + 0), 2, u16(low16(remaining)))\n    state.write(10555648, 2, u16(256))\n    state.write(u32(port.base + 0), 4, u32(2483065664))\n    state.write(u32(port.base + 0), 4, u32(2533201280))\n    state.write(u32(port.base + 0), 2, u16(38783))\n    state.write(u32(port.base + 0), 2, u16(49152))\n    state.write(4294964768, 2, u16(128))\n    read_value_12 = state.read(4294964768, 2)\n    state.write(u32(port.base + 0), 2, u16(read_value_12))\n    read_value_13 = state.read(16727808, 1)\n    comparison_left = u8(read_value_13)\n    comparison_right = u8(0)\n    tested_value = u8(comparison_left - comparison_right)\n    value_is_zero = tested_value == 0\n    value_is_negative = bool(tested_value & 128)\n    arithmetic_carry = comparison_left < comparison_right\n    arithmetic_overflow = bool((comparison_left ^ comparison_right) & (comparison_left ^ u8(comparison_left - comparison_right)) & 128)\n    if not not value_is_zero:\n        state.write(10555648, 2, u16(0))\n    read_value_14 = state.read(4294964742, 2)\n    state.write(u32(port.base + 0), 2, u16(read_value_14))\n    read_value_15 = state.read(4294963998, 2)\n    state.write(4294963998, 2, u16(0))\n    tested_value = u16(0)\n    value_is_zero = tested_value == 0\n    value_is_negative = bool(tested_value & 32768)\n    arithmetic_carry = False\n    arithmetic_overflow = False\nframe = replace(frame, source=destination, destination=source, vdp_port=port, motion_x=value, motion_y=field, attributes=tile, control_latch=remaining, carry=arithmetic_carry, zero=value_is_zero, negative=value_is_negative, overflow=arithmetic_overflow)\ncalled = replace(frame, stack_cursor=frame.stack_cursor.advance(-4))\nreturned = checked_tick_frame(call_target(state, 18966, called), state)\nframe = replace(returned, stack_cursor=returned.stack_cursor.advance(4))\nfrom .services import flush_scene_transfer_queue\npacket_values = PacketTransferValues(frame.motion_x, frame.motion_y, frame.attributes, frame.tile_count)\npacket_result = flush_scene_transfer_queue(state, packet_values)\nif packet_result is not None:\n    packet_result.validate(state)\n    if type(packet_result.values) is not PacketTransferValues:\n        raise Boundary('AD06 must return actual packet carriers')\n    frame = replace(frame, source=packet_result.source, vdp_port=state.table_at(12582912), motion_x=packet_result.values.command, motion_y=packet_result.values.increment, attributes=packet_result.values.address, tile_count=packet_result.values.spill)\nreturn replace(frame, carry=False, zero=True, negative=False, overflow=False)"}})

def _lower_poll_world_map_input(emitter,rules):
    emitter.segment(0x4890,0x4942)
    emitter.ins('jsr','main_pc_0067ca:l',6)
    emitter.ins('lea.l','0xc00004:l,%a6',6)
    emitter.ins('move.w','0xf606:w,%d7',4)
    emitter.ins('ori.b','#0x10,%d7',4)
    emitter.ins('move.w','%d7,(%a6)',2)
    emitter.ins('move.w','#0x100,0xa11100:l',8)
    emitter.ins('move.l','#0x94019340,(%a6)',6)
    emitter.ins('move.l','#0x96fc9500,(%a6)',6)
    emitter.ins('move.w','#0x977f,(%a6)',4)
    emitter.ins('move.w','#0x7800,(%a6)',4)
    emitter.ins('move.w','#0x82,0xf620:w',6)
    emitter.ins('move.w','0xf620:w,(%a6)',4)
    emitter.ins('tst.b','0xff3f00:l',6)
    emitter.ins('bne.b','main_pc_0048dc',2)
    emitter.ins('move.w','#0x0,0xa11100:l',8)
    emitter.ins('move.w','0xf606:w,(%a6)',4)
    emitter.ins('tst.w','0xf31e:w',4)
    emitter.ins('beq.w','main_pc_004936',4)
    emitter.ins('lea.l','0xc00004:l,%a6',6)
    emitter.ins('move.w','0xf606:w,%d7',4)
    emitter.ins('ori.b','#0x10,%d7',4)
    emitter.ins('move.w','%d7,(%a6)',2)
    emitter.ins('move.w','#0x100,0xa11100:l',8)
    emitter.ins('move.l','#0x94009340,(%a6)',6)
    emitter.ins('move.l','#0x96fd9580,(%a6)',6)
    emitter.ins('move.w','#0x977f,(%a6)',4)
    emitter.ins('move.w','#0xc000,(%a6)',4)
    emitter.ins('move.w','#0x80,0xf620:w',6)
    emitter.ins('move.w','0xf620:w,(%a6)',4)
    emitter.ins('tst.b','0xff3f00:l',6)
    emitter.ins('bne.b','main_pc_00492e',2)
    emitter.ins('move.w','#0x0,0xa11100:l',8)
    emitter.ins('move.w','0xf606:w,(%a6)',4)
    emitter.ins('clr.w','0xf31e:w',4)
    emitter.ins('bsr.w','main_pc_004a16',4)
    emitter.ins('jsr','main_pc_00ad06:l',6)
    emitter.ins('rts','',2)

def _lower_upload_world_map_palette(emitter,rules):
    emitter.segment(0x4998,0x49d6)
    emitter.ins('move.l','#0x7c000002,0xc00004:l',10)
    emitter.ins('move.w','0xf316:w,%d0',4)
    emitter.ins('neg.w','%d0',2)
    emitter.ins('move.w','%d0,0xc00000:l',6)
    emitter.ins('move.w','0xf318:w,%d0',4)
    emitter.ins('neg.w','%d0',2)
    emitter.ins('move.w','%d0,0xc00000:l',6)
    emitter.ins('move.l','#0x40000010,0xc00004:l',10)
    emitter.ins('move.w','0xf312:w,0xc00000:l',8)
    emitter.ins('move.w','0xf314:w,0xc00000:l',8)
    emitter.ins('rts','',2)

def _lower_draw_scene_header_glyphs(emitter,rules):
    emitter.segment(0x5204,0x5242)
    emitter.ins('lea.l','0x8a1fc:l,%a0',6)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0x1,%d3',4)
    emitter.ins('jsr','main_pc_00ae8a:l',6)
    emitter.ins('lea.l','0x8a200:l,%a0',6)
    emitter.ins('move.w','#0x9,%d3',4)
    emitter.ins('jsr','main_pc_00ae8a:l',6)
    emitter.ins('move.l','#0x5a000000,0xc00004:l',10)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0x17f,%d4',4)
    emitter.ins('move.l','(%a1)+,(%a6)',2)
    emitter.ins('dbra','%d4,main_pc_00523a',4)
    emitter.ins('rts','',2)

def _lower_upload_selection_layout(emitter,rules):
    emitter.segment(0x52c2,0x5330)
    emitter.ins('move.l','#0x70000001,0xc00004:l',10)
    emitter.ins('lea.l','0x89ddc:l,%a0',6)
    emitter.ins('move.w','#0x17,%d4',4)
    emitter.ins('move.l','(%a0)+,0xc00000:l',6)
    emitter.ins('dbra','%d4,main_pc_0052d6',4)
    emitter.ins('move.l','#0x70a00001,0xc00004:l',10)
    emitter.ins('lea.l','0x89f5c:l,%a0',6)
    emitter.ins('move.w','#0x7,%d4',4)
    emitter.ins('move.l','(%a0)+,0xc00000:l',6)
    emitter.ins('dbra','%d4,main_pc_0052f4',4)
    emitter.ins('move.l','#0x72000001,0xc00004:l',10)
    emitter.ins('move.w','#0x7,%d4',4)
    emitter.ins('move.l','#0x33333333,0xc00000:l',10)
    emitter.ins('dbra','%d4,main_pc_00530c',4)
    emitter.ins('lea.l','0x8a0bc:l,%a0',6)
    emitter.ins('move.w','#0x7,%d4',4)
    emitter.ins('move.l','(%a0)+,0xc00000:l',6)
    emitter.ins('dbra','%d4,main_pc_005324',4)
    emitter.ins('rts','',2)

def _lower_draw_scene_footer_glyphs(emitter,rules):
    emitter.segment(0x5370,0x539e)
    emitter.ins('lea.l','0x8a426:l,%a0',6)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0x9,%d3',4)
    emitter.ins('jsr','main_pc_00af1e:l',6)
    emitter.ins('move.l','#0x70c00001,0xc00004:l',10)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0x4f,%d2',4)
    emitter.ins('move.l','(%a1)+,(%a6)',2)
    emitter.ins('dbra','%d2,main_pc_005396',4)
    emitter.ins('rts','',2)

def _lower_draw_current_resource_glyphs(emitter,rules):
    emitter.segment(0x55b0,0x55d0)
    emitter.ins('lea.l','0x89efc:l,%a0',6)
    emitter.ins('move.l','#0x67a00001,0xc00004:l',10)
    emitter.ins('move.w','#0x17,%d0',4)
    emitter.ins('move.l','(%a0)+,0xc00000:l',6)
    emitter.ins('dbra','%d0,main_pc_0055c4',4)
    emitter.ins('rts','',2)

def _lower_configure_controller_outputs(emitter,rules):
    emitter.segment(0x67b4,0x67ca)
    emitter.ins('moveq','#64,%d0',2)
    emitter.ins('move.b','%d0,0xa10009:l',6)
    emitter.ins('move.b','%d0,0xa1000b:l',6)
    emitter.ins('move.b','%d0,0xa1000d:l',6)
    emitter.ins('rts','',2)

def _lower_poll_controller_with_z80_bus(emitter,rules):
    emitter.segment(0x67ca,0x67e8)
    emitter.ins('move.w','#0x100,0xa11100:l',8)
    emitter.ins('btst.b','#0x0,0xa11100:l',8)
    emitter.ins('bne.b','main_pc_0067d2',2)
    emitter.ins('bsr.b','main_pc_0067e8',2)
    emitter.ins('move.w','#0x0,0xa11100:l',8)
    emitter.ins('rts','',2)

def _lower_poll_two_controller_ports(emitter,rules):
    emitter.segment(0x67e8,0x6826)
    emitter.ins('lea.l','0xf602:w,%a0',4)
    emitter.ins('lea.l','0xa10003:l,%a1',6)
    emitter.ins('bsr.b','main_pc_0067f6',2)
    emitter.ins('addq.w','#0x2,%a1',2)
    emitter.ins('move.b','#0x0,(%a1)',4)
    emitter.ins('nop','',2)
    emitter.ins('nop','',2)
    emitter.ins('move.b','(%a1),%d0',2)
    emitter.ins('lsl.b','#0x2,%d0',2)
    emitter.ins('andi.b','#0xc0,%d0',4)
    emitter.ins('move.b','#0x40,(%a1)',4)
    emitter.ins('nop','',2)
    emitter.ins('nop','',2)
    emitter.ins('move.b','(%a1),%d1',2)
    emitter.ins('andi.b','#0x3f,%d1',4)
    emitter.ins('or.b','%d1,%d0',2)
    emitter.ins('not.b','%d0',2)
    emitter.ins('move.b','%d0,%d1',2)
    emitter.ins('move.b','(%a0),%d2',2)
    emitter.ins('eor.b','%d2,%d0',2)
    emitter.ins('move.b','%d1,(%a0)+',2)
    emitter.ins('and.b','%d1,%d0',2)
    emitter.ins('move.b','%d0,(%a0)+',2)
    emitter.ins('rts','',2)

def _lower_initialize_z80_sound_image(emitter,rules):
    emitter.segment(0x6950,0x69aa)
    emitter.ins('move.w','#0x100,0xa11100:l',8)
    emitter.ins('bsr.w','main_pc_0069b8',4)
    emitter.ins('btst.b','#0x0,0xa11100:l',8)
    emitter.ins('bne.b','main_pc_00695c',2)
    emitter.ins('lea.l','106(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('lea.l','0xa00000:l,%a1',6)
    emitter.ins('move.w','#0xfff,%d0',4)
    emitter.ins('move.b','(%a0)+,(%a1)+',2)
    emitter.ins('dbra','%d0,main_pc_006976',4)
    emitter.ins('lea.l','4126(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','#0xdff,%d0',4)
    emitter.ins('move.b','(%a0)+,(%a1)+',2)
    emitter.ins('dbra','%d0,main_pc_006986',4)
    emitter.ins('lea.l','28(%pc),%a0',4)
    emitter.ins('lea.l','0xa01c00:l,%a1',6)
    emitter.ins('moveq','#12,%d0',2)
    emitter.ins('move.b','(%a0)+,(%a1)+',2)
    emitter.ins('dbra','%d0,main_pc_006998',4)
    emitter.ins('bsr.b','main_pc_0069b8',2)
    emitter.ins('move.w','#0x0,0xa11100:l',8)
    emitter.ins('rts','',2)

def _lower_release_z80_reset(emitter,rules):
    emitter.segment(0x69b8,0x69d2)
    emitter.ins('move.w','#0x0,0xa11200:l',8)
    emitter.ins('nop','',2)
    emitter.ins('nop','',2)
    emitter.ins('nop','',2)
    emitter.ins('nop','',2)
    emitter.ins('move.w','#0x100,0xa11200:l',8)
    emitter.ins('rts','',2)

def _lower_queue_sound_word_list(emitter,rules):
    emitter.segment(0x80f4,0x8112)
    emitter.ins('lea.l','54(%pc),%a1',4)
    emitter.ins('lsl.w','#0x3,%d0',2)
    emitter.ins('adda.w','%d0,%a1',2)
    emitter.ins('movea.l','(%a1)+,%a2',2)
    emitter.ins('movea.w','(%a1)+,%a3',2)
    emitter.ins('adda.w','#0x80,%a3',4)
    emitter.ins('move.w','(%a1)+,%d7',2)
    emitter.ins('move.l','(%a2)+,(%a3)+',2)
    emitter.ins('dbra','%d7,main_pc_008106',4)
    emitter.ins('addq.w','#0x1,0xf31e:w',4)
    emitter.ins('rts','',2)

def _lower_initialize_scene_growth_and_tiles(emitter,rules):
    emitter.segment(0x93f0,0x949e)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.w','0xf606:w,%d0',4)
    emitter.ins('andi.b','#0xbf,%d0',4)
    emitter.ins('move.w','%d0,0xc00004:l',6)
    emitter.ins('jsr','main_pc_0068ce:l',6)
    emitter.ins('move.l','#0x40000000,0xc00004:l',10)
    emitter.ins('lea.l','322(%pc),%a0',4)
    emitter.ins('move.w','#0x1b7,%d0',4)
    emitter.ins('move.l','(%a0)+,0xc00000:l',6)
    emitter.ins('dbra','%d0,main_pc_00941a',4)
    emitter.ins('moveq','#11,%d5',2)
    emitter.ins('moveq','#3,%d6',2)
    emitter.ins('move.w','#0x8001,%d4',4)
    emitter.ins('move.l','#0x461c0003,%d0',6)
    emitter.ins('move.w','%d5,%d7',2)
    emitter.ins('move.l','%d0,0xc00004:l',6)
    emitter.ins('move.w','%d4,0xc00000:l',6)
    emitter.ins('addq.w','#0x1,%d4',2)
    emitter.ins('dbra','%d7,main_pc_00943a',4)
    emitter.ins('addi.l','#0x800000,%d0',6)
    emitter.ins('dbra','%d6,main_pc_009432',4)
    emitter.ins('btst.b','#0x7,0xa10001:l',8)
    emitter.ins('beq.w','main_pc_00947e',4)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x66300003,0xc00004:l',10)
    emitter.ins('move.w','#0x8035,0xc00000:l',8)
    emitter.ins('move.w','#0x8036,0xc00000:l',8)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('jsr','main_pc_008112:l',6)
    emitter.ins('move.w','#0x28,0xf618:w',6)
    emitter.ins('move.w','#0x12c,0xf608:w',6)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('move.w','#0x100,0xf612:w',6)
    emitter.ins('rts','',2)

def _lower_refresh_scene_palettes(emitter,rules):
    emitter.segment(0xa3da,0xa42e)
    emitter.ins('lea.l','0xfb00:w,%a0',4)
    emitter.ins('cmpi.w','#0x20,0xf352:w',6)
    emitter.ins('bcc.w','main_pc_00a3ec',4)
    emitter.ins('lea.l','0xfb80:w,%a0',4)
    emitter.ins('move.w','0xef7a:w,%d0',4)
    emitter.ins('move.w','0xef7c:w,%d1',4)
    emitter.ins('addq.w','#0x1,%d1',2)
    emitter.ins('cmpi.w','#0x6,%d1',4)
    emitter.ins('bcs.w','main_pc_00a428',4)
    emitter.ins('clr.w','%d1',2)
    emitter.ins('addq.w','#0x1,%d0',2)
    emitter.ins('cmpi.w','#0xa,%d0',4)
    emitter.ins('bcs.w','main_pc_00a40c',4)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('move.w','%d0,0xef7a:w',4)
    emitter.ins('lsl.w','#0x2,%d0',2)
    emitter.ins('lea.l','26(%pc),%a1',4)
    emitter.ins('move.w','(%a1, %d0.w),0x32(%a0)',6)
    emitter.ins('move.w','0x2(%a1, %d0.w),0x38(%a0)',6)
    emitter.ins('move.w','#0x1,0xf31e:w',6)
    emitter.ins('move.w','%d1,0xef7c:w',4)
    emitter.ins('rts','',2)

def _lower_upload_selected_mode_tile_rows(emitter,rules):
    emitter.segment(0xa760,0xa78e)
    emitter.ins('move.l','%a0,-(%a7)',2)
    emitter.ins('lea.l','0xc00000:l,%a6',6)
    emitter.ins('lea.l','52(%pc),%a0',4)
    emitter.ins('move.w','0xf350:w,%d2',4)
    emitter.ins('lsl.w','#0x5,%d2',2)
    emitter.ins('move.l','#0x41200003,0xc00004:l',10)
    emitter.ins('bsr.b','main_pc_00a78e',2)
    emitter.ins('move.l','#0x41a00003,0xc00004:l',10)
    emitter.ins('bsr.b','main_pc_00a78e',2)
    emitter.ins('movea.l','(%a7)+,%a0',2)
    emitter.ins('rts','',2)

def _lower_upload_selected_tile_row(emitter,rules):
    emitter.segment(0xa78e,0xa79e)
    emitter.ins('move.w','#0x7,%d1',4)
    emitter.ins('move.w','(%a0, %d2.w),(%a6)',4)
    emitter.ins('addq.w','#0x2,%d2',2)
    emitter.ins('dbra','%d1,main_pc_00a792',4)
    emitter.ins('rts','',2)

LOWERERS={
    'poll_world_map_input':_lower_poll_world_map_input,
    'upload_world_map_palette':_lower_upload_world_map_palette,
    'draw_scene_header_glyphs':_lower_draw_scene_header_glyphs,
    'upload_selection_layout':_lower_upload_selection_layout,
    'draw_scene_footer_glyphs':_lower_draw_scene_footer_glyphs,
    'draw_current_resource_glyphs':_lower_draw_current_resource_glyphs,
    'configure_controller_outputs':_lower_configure_controller_outputs,
    'poll_controller_with_z80_bus':_lower_poll_controller_with_z80_bus,
    'poll_two_controller_ports':_lower_poll_two_controller_ports,
    'initialize_z80_sound_image':_lower_initialize_z80_sound_image,
    'release_z80_reset':_lower_release_z80_reset,
    'queue_sound_word_list':_lower_queue_sound_word_list,
    'initialize_scene_growth_and_tiles':_lower_initialize_scene_growth_and_tiles,
    'refresh_scene_palettes':_lower_refresh_scene_palettes,
    'upload_selected_mode_tile_rows':_lower_upload_selected_mode_tile_rows,
    'upload_selected_tile_row':_lower_upload_selected_tile_row,
}

# Complete actual field-core contracts; ordinary lowerers unchanged.
APPROVED['contexts_lowbank'].add('PaletteRefreshFields')
DECLARATIONS.update({'refresh_scene_palettes_fields': {'signature': 'state: SceneState',
                                   'returns': 'PaletteRefreshFields',
                                   'flow': 'checked_state(state)\n'
                                           'destination = state.table_at(4294966016)\n'
                                           'if state.read(4294964050, 2) < 32:\n'
                                           '    destination = state.table_at(4294966144)\n'
                                           'value_word = state.read(4294963066, 2)\n'
                                           'field_word = u16(state.read(4294963068, 2) + 1)\n'
                                           'source_if_written = None\n'
                                           'if field_word >= 6:\n'
                                           '    field_word = 0\n'
                                           '    value_word = u16(value_word + 1)\n'
                                           '    if value_word >= 10:\n'
                                           '        value_word = 0\n'
                                           '    state.write(4294963066, 2, value_word)\n'
                                           '    value_word = u16(value_word << 2)\n'
                                           '    source_if_written = state.table_at(42030)\n'
                                           '    first_color = '
                                           'state.read(u32(source_if_written.base + '
                                           's16(value_word)), 2)\n'
                                           '    state.write(u32(destination.base + 50), 2, '
                                           'first_color)\n'
                                           '    second_color = '
                                           'state.read(u32(source_if_written.base + '
                                           's16(value_word) + 2), 2)\n'
                                           '    state.write(u32(destination.base + 56), 2, '
                                           'second_color)\n'
                                           '    state.write(4294963998, 2, 1)\n'
                                           'state.write(4294963068, 2, field_word)\n'
                                           'return PaletteRefreshFields(destination, '
                                           'source_if_written, value_word, field_word, False, '
                                           'field_word == 0, bool(field_word & 32768), False)'}})

def compile_source(source):
    records=semantic_functions(source,DECLARATIONS,APPROVED)
    records['poll_world_map_input']['effects'] = dict(
        projection=records['poll_world_map_input']['effects'],
        supplied_current_input_and_queue=records['poll_world_map_input_frame']['effects'])
    records['refresh_scene_palettes']['effects'] += '\nsole actual palette CCR/frame core: ' + '\n'.join(records[name]['effects'] for name in ('refresh_scene_palettes_fields', 'refresh_scene_palettes_frame_fields'))
    for owner, field in (('poll_world_map_input', 'poll_world_map_input_fields'), ('upload_world_map_palette', 'upload_world_map_palette_fields'), ('draw_scene_header_glyphs', 'draw_scene_header_glyphs_fields'), ('upload_selection_layout', 'upload_selection_layout_fields'), ('draw_scene_footer_glyphs', 'draw_scene_footer_glyphs_fields'), ('draw_current_resource_glyphs', 'draw_current_resource_glyphs_fields'), ('configure_controller_outputs', 'configure_controller_outputs_fields'), ('poll_controller_with_z80_bus', 'poll_controller_with_z80_bus_fields'), ('poll_two_controller_ports', 'poll_two_controller_ports_fields'), ('poll_two_controller_ports_alternate_1', 'poll_two_controller_ports_alternate_1_fields'), ('initialize_z80_sound_image', 'initialize_z80_sound_image_fields'), ('release_z80_reset', 'release_z80_reset_fields'), ('queue_sound_word_list', 'queue_sound_word_list_fields'), ('initialize_scene_growth_and_tiles', 'initialize_scene_growth_and_tiles_fields'), ('upload_selected_mode_tile_rows', 'upload_selected_mode_tile_rows_fields'), ('upload_selected_tile_row', 'upload_selected_tile_row_fields')):
        records[owner]['effects']=dict(historical_projection=records[owner]['effects'],sole_current_fields=records[field]['effects'])
    return lower_declared(records,BUSINESS_LOWBANK_BINDINGS,LOWERERS)

DECLARATIONS.update({'refresh_scene_palettes_fields': {'signature': 'state: SceneState', 'returns': 'PaletteRefreshFields', 'flow': 'checked_state(state)\ndestination = state.table_at(4294966016)\nif state.read(4294964050, 2) < 32:\n    destination = state.table_at(4294966144)\nvalue_word = state.read(4294963066, 2)\nfield_total = state.read(4294963068, 2) + 1\nextend = field_total > 65535\nfield_word = u16(field_total)\nsource_if_written = None\nif field_word >= 6:\n    field_word = 0\n    value_total = value_word + 1\n    extend = value_total > 65535\n    value_word = u16(value_total)\n    if value_word >= 10:\n        value_word = 0\n    state.write(4294963066, 2, value_word)\n    extend = bool(value_word & 16384)\n    value_word = u16(value_word << 2)\n    source_if_written = state.table_at(42030)\n    first_color = state.read(u32(source_if_written.base + s16(value_word)), 2)\n    state.write(u32(destination.base + 50), 2, first_color)\n    second_color = state.read(u32(source_if_written.base + s16(value_word) + 2), 2)\n    state.write(u32(destination.base + 56), 2, second_color)\n    state.write(4294963998, 2, 1)\nstate.write(4294963068, 2, field_word)\nreturn PaletteRefreshFields(destination, source_if_written, value_word, field_word, False, field_word == 0, bool(field_word & 32768), False, extend)'}})

DECLARATIONS.update({'refresh_scene_palettes_frame_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'from ..high_level_remaining_flows.business_city import _resource_cost_frame\nframe = _resource_cost_frame(state, frame, 41946)\nfields = refresh_scene_palettes_fields(state).validate(state)\nsource = frame.candidates if fields.source_if_written is None else fields.source_if_written.cursor()\nstatus = (16 if fields.extend else 0) | (1 if fields.carry else 0) | (4 if fields.zero else 0)\nstatus |= (8 if fields.negative else 0) | (2 if fields.overflow else 0)\nstate.sr = state.sr & 65504 | status\nreturn first_replace(frame, roster=fields.destination.cursor(), candidates=source, target_x=replace_word(frame.target_x, fields.value_word), target_y=replace_word(frame.target_y, fields.field_word), status=status)'}})

APPROVED.setdefault('contexts_gameplay',set()).update(('FirstDeploymentFrame', 'first_replace'))

APPROVED.setdefault('business_city',set()).update(('_resource_cost_frame',))

# Exact existing palette facade import; this does not loosen the shared guard.
APPROVED.setdefault((2, 'high_level_remaining_flows.business_city'), set()).add('_resource_cost_frame')

DECLARATIONS.update({'_campaign_ui_arithmetic_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, carrier: str, value: int, subtract: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': 'from .business_commands import _city_ui_arithmetic_fields\nreturn _city_ui_arithmetic_fields(state, frame, carrier, value, subtract)'}})

DECLARATIONS.update({'_campaign_ui_bit_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, value: int, bit: int', 'returns': 'FirstDeploymentFrame', 'flow': 'from .business_map import _world_map_bit_fields\nreturn _world_map_bit_fields(state, frame, value, bit)'}})

DECLARATIONS.update({'_campaign_ui_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int, token: int', 'returns': 'FirstDeploymentFrame', 'flow': 'from .business_main import _campaign_call_fields\nreturn _campaign_call_fields(state, frame, target, token)'}})

DECLARATIONS.update({'_campaign_ui_controller_shift_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'from .business_movement_support import _movement_binary_flags\nfor step in range(2):\n    value = low8(frame.target_x)\n    frame, value = _movement_binary_flags(state, frame, value, value, 8)\n    frame = first_replace(frame, target_x=replace_byte(frame.target_x, value))\nstatus = frame.status & 29\nstate.sr = state.sr & 65504 | status\nreturn first_replace(frame, status=status)'}})

DECLARATIONS.update({'_campaign_ui_copy_panel_longs_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, source_carrier: str, count_carrier: str, instruction: int, destination: int', 'returns': 'FirstDeploymentFrame', 'flow': 'while True:\n    source = frame.carrier(source_carrier)\n    value = source.long()\n    frame = first_replace(frame, **{source_carrier: source.advance(4)})\n    frame = _campaign_ui_write_fields(state, frame, instruction, destination, value, 4)\n    frame, more = _campaign_ui_loop_fields(frame, count_carrier)\n    if not more:\n        return frame'}})

DECLARATIONS.update({'_campaign_ui_frame_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, entry: int', 'returns': 'FirstDeploymentFrame', 'flow': 'from .business_commands import _city_ui_frame_fields\nreturn _city_ui_frame_fields(state, frame, entry)'}})

DECLARATIONS.update({'_campaign_ui_loop_fields': {'signature': 'frame: FirstDeploymentFrame, carrier: str', 'returns': 'tuple[FirstDeploymentFrame, bool]', 'flow': 'remaining = u16(low16(frame.carrier(carrier)) - 1)\nreturn (first_replace(frame, **{carrier: replace_word(frame.carrier(carrier), remaining)}), remaining != 65535)'}})

DECLARATIONS.update({'_campaign_ui_move_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, carrier: str, value: int, width: int=16', 'returns': 'FirstDeploymentFrame', 'flow': 'from .business_movement_support import _movement_move, _movement_move_long\nif width == 32:\n    return _movement_move_long(state, frame, carrier, value)\nreturn _movement_move(state, frame, carrier, value, width)'}})

DECLARATIONS.update({'_campaign_ui_negate_word_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, carrier: str', 'returns': 'FirstDeploymentFrame', 'flow': 'from .business_movement_support import _movement_binary_flags\nframe, value = _movement_binary_flags(state, frame, 0, low16(frame.carrier(carrier)), 16, True)\nreturn first_replace(frame, **{carrier: replace_word(frame.carrier(carrier), value)})'}})

DECLARATIONS.update({'_campaign_ui_port_read_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _campaign_ui_write_fields(state, frame, 26614, frame.candidates.address, 0, 1)\nframe = _campaign_ui_move_fields(state, frame, 'target_x', frame.candidates.byte(), 8)\nframe = _campaign_ui_controller_shift_fields(state, frame)\nframe = _campaign_ui_move_fields(state, frame, 'target_x', low8(frame.target_x) & 192, 8)\nframe = _campaign_ui_write_fields(state, frame, 26630, frame.candidates.address, 64, 1)\nframe = _campaign_ui_move_fields(state, frame, 'target_y', frame.candidates.byte(), 8)\nframe = _campaign_ui_move_fields(state, frame, 'target_y', low8(frame.target_y) & 63, 8)\nframe = _campaign_ui_move_fields(state, frame, 'target_x', low8(frame.target_x) | low8(frame.target_y), 8)\nframe = _campaign_ui_move_fields(state, frame, 'target_x', low8(frame.target_x) ^ 255, 8)\nframe = _campaign_ui_move_fields(state, frame, 'target_y', low8(frame.target_x), 8)\nframe = _campaign_ui_move_fields(state, frame, 'unit', frame.roster.byte(), 8)\nframe = _campaign_ui_move_fields(state, frame, 'target_x', low8(frame.target_x) ^ low8(frame.unit), 8)\nframe = _campaign_ui_write_fields(state, frame, 26654, frame.roster.address, low8(frame.target_y), 1)\nframe = first_replace(frame, roster=frame.roster.advance(1))\nframe = _campaign_ui_move_fields(state, frame, 'target_x', low8(frame.target_x) & low8(frame.target_y), 8)\nframe = _campaign_ui_write_fields(state, frame, 26658, frame.roster.address, low8(frame.target_x), 1)\nreturn first_replace(frame, roster=frame.roster.advance(1))"}})

DECLARATIONS.update({'_campaign_ui_shift_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, carrier: str, amount: int', 'returns': 'FirstDeploymentFrame', 'flow': 'from .business_scene_support import _aux_text_shift_word_fields\nreturn _aux_text_shift_word_fields(state, frame, carrier, amount)'}})

DECLARATIONS.update({'_campaign_ui_write_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, pc: int, address: int, value: int, width: int=2, clear: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': 'from .business_main import _campaign_emit_fields\nreturn _campaign_emit_fields(state, frame, pc, address, value, width, clear)'}})

DECLARATIONS.update({'configure_controller_outputs': {'signature': 'state: SceneState, inputs: ConfigureControllerOutputsInput', 'returns': 'ConfigureControllerOutputsResult', 'flow': "checked_state(state)\nif type(inputs) is not ConfigureControllerOutputsInput:\n    raise ValueError('function-specific typed input required')\ninputs.validate(state)\nincoming = FirstDeploymentFrame.unobserved()\nobserved = configure_controller_outputs_fields(state, incoming)\nreturn ConfigureControllerOutputsResult(value=observed.target_x, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))"}})

DECLARATIONS.update({'configure_controller_outputs_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _campaign_ui_frame_fields(state, frame, 26548)\nframe = _campaign_ui_move_fields(state, frame, 'target_x', 64, 32)\nframe = _campaign_ui_write_fields(state, frame, 26550, 10551305, low8(frame.target_x), 1)\nframe = _campaign_ui_write_fields(state, frame, 26556, 10551307, low8(frame.target_x), 1)\nreturn _campaign_ui_write_fields(state, frame, 26562, 10551309, low8(frame.target_x), 1)"}})

DECLARATIONS.update({'draw_current_resource_glyphs': {'signature': 'state: SceneState, inputs: DrawCurrentResourceGlyphsInput', 'returns': 'DrawCurrentResourceGlyphsResult', 'flow': "checked_state(state)\nif type(inputs) is not DrawCurrentResourceGlyphsInput:\n    raise ValueError('function-specific typed input required')\ninputs.validate(state)\nincoming = FirstDeploymentFrame.unobserved()\nincoming = first_replace(incoming, target_x=inputs.value)\nobserved = draw_current_resource_glyphs_fields(state, incoming)\nreturn DrawCurrentResourceGlyphsResult(destination=state.table_at(observed.roster.address), value=observed.target_x, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))"}})

DECLARATIONS.update({'draw_current_resource_glyphs_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _campaign_ui_frame_fields(state, frame, 21936)\nframe = first_replace(frame, roster=state.table_at(564988).cursor())\nframe = _campaign_ui_write_fields(state, frame, 21942, 12582916, 1738539009, 4)\nframe = _campaign_ui_move_fields(state, frame, 'target_x', 23)\nreturn _campaign_ui_copy_panel_longs_fields(state, frame, 'roster', 'target_x', 21956, 12582912)"}})

DECLARATIONS.update({'draw_scene_footer_glyphs': {'signature': 'state: SceneState, inputs: DrawSceneFooterGlyphsInput', 'returns': 'DrawSceneFooterGlyphsResult', 'flow': "checked_state(state)\nif type(inputs) is not DrawSceneFooterGlyphsInput:\n    raise ValueError('function-specific typed input required')\ninputs.validate(state)\nincoming = FirstDeploymentFrame.unobserved()\nincoming = first_replace(incoming, auxiliary=inputs.port.cursor(), target_x=inputs.value, target_y=inputs.field, unit=inputs.tile, count=inputs.row)\nobserved = draw_scene_footer_glyphs_fields(state, incoming)\nreturn DrawSceneFooterGlyphsResult(destination=state.table_at(observed.roster.address), source=state.table_at(observed.candidates.address), tile=observed.unit, row=observed.count, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))"}})

DECLARATIONS.update({'draw_scene_footer_glyphs_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _campaign_ui_frame_fields(state, frame, 21360)\nframe = first_replace(frame, roster=state.table_at(566310).cursor(), candidates=state.table_at(4294955776).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'count', 9)\nframe = _campaign_ui_call_fields(state, frame, 44830, 21380)\nframe = _campaign_ui_write_fields(state, frame, 21380, 12582916, 1891631105, 4)\nframe = first_replace(frame, candidates=state.table_at(4294955776).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'unit', 79)\nreturn _campaign_ui_copy_panel_longs_fields(state, frame, 'candidates', 'unit', 21398, frame.auxiliary.address)"}})

DECLARATIONS.update({'draw_scene_header_glyphs': {'signature': 'state: SceneState, inputs: DrawSceneHeaderGlyphsInput', 'returns': 'DrawSceneHeaderGlyphsResult', 'flow': "checked_state(state)\nif type(inputs) is not DrawSceneHeaderGlyphsInput:\n    raise ValueError('function-specific typed input required')\ninputs.validate(state)\nincoming = FirstDeploymentFrame.unobserved()\nincoming = first_replace(incoming, auxiliary=inputs.port.cursor(), target_x=inputs.value, target_y=inputs.field, count=inputs.row, distance=inputs.offset)\nobserved = draw_scene_header_glyphs_fields(state, incoming)\nreturn DrawSceneHeaderGlyphsResult(destination=state.table_at(observed.roster.address), source=state.table_at(observed.candidates.address), value=observed.target_x, field=observed.target_y, row=observed.count, offset=observed.distance, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))"}})

DECLARATIONS.update({'draw_scene_header_glyphs_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _campaign_ui_frame_fields(state, frame, 20996)\nframe = first_replace(frame, roster=state.table_at(565756).cursor(), candidates=state.table_at(4294955776).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'count', 1)\nframe = _campaign_ui_call_fields(state, frame, 44682, 21016)\nframe = first_replace(frame, roster=state.table_at(565760).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'count', 9)\nframe = _campaign_ui_call_fields(state, frame, 44682, 21032)\nframe = _campaign_ui_write_fields(state, frame, 21032, 12582916, 1509949440, 4)\nframe = first_replace(frame, candidates=state.table_at(4294955776).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'distance', 383)\nreturn _campaign_ui_copy_panel_longs_fields(state, frame, 'candidates', 'distance', 21050, frame.auxiliary.address)"}})

DECLARATIONS.update({'initialize_scene_growth_and_tiles': {'signature': 'state: SceneState, inputs: InitializeSceneGrowthAndTilesInput', 'returns': 'InitializeSceneGrowthAndTilesResult', 'flow': "checked_state(state)\nif type(inputs) is not InitializeSceneGrowthAndTilesInput:\n    raise ValueError('function-specific typed input required')\ninputs.validate(state)\nincoming = FirstDeploymentFrame.unobserved()\nincoming = first_replace(incoming, target_x=inputs.value, distance=inputs.offset, choice=inputs.remaining)\nobserved = initialize_scene_growth_and_tiles_fields(state, incoming)\nreturn InitializeSceneGrowthAndTilesResult(destination=state.table_at(observed.roster.address), value=observed.target_x, offset=observed.distance, limit=observed.offset_x, member=observed.offset_y, remaining=observed.choice, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))"}})

DECLARATIONS.update({'initialize_scene_growth_and_tiles_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from .business_movement_support import _movement_arithmetic_long\nframe = _campaign_ui_frame_fields(state, frame, 37872)\nstate.sr = 9984\nframe = first_replace(frame, status=0)\nframe = _campaign_ui_move_fields(state, frame, 'target_x', state.read(4294964742, 2))\nframe = _campaign_ui_move_fields(state, frame, 'target_x', low8(frame.target_x) & 191, 8)\nframe = _campaign_ui_write_fields(state, frame, 37884, 12582916, low16(frame.target_x))\nframe = _campaign_ui_call_fields(state, frame, 26830, 37896)\nframe = _campaign_ui_write_fields(state, frame, 37896, 12582916, 1073741824, 4)\nframe = first_replace(frame, roster=state.table_at(38230).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'target_x', 439)\nframe = _campaign_ui_copy_panel_longs_fields(state, frame, 'roster', 'target_x', 37914, 12582912)\nframe = _campaign_ui_move_fields(state, frame, 'offset_x', 11, 32)\nframe = _campaign_ui_move_fields(state, frame, 'offset_y', 3, 32)\nframe = _campaign_ui_move_fields(state, frame, 'distance', 32769)\nframe = _campaign_ui_move_fields(state, frame, 'target_x', 1176240131, 32)\nwhile True:\n    frame = _campaign_ui_move_fields(state, frame, 'choice', low16(frame.offset_x))\n    frame = _campaign_ui_write_fields(state, frame, 37940, 12582916, frame.target_x, 4)\n    while True:\n        frame = _campaign_ui_write_fields(state, frame, 37946, 12582912, low16(frame.distance))\n        frame = _campaign_ui_arithmetic_fields(state, frame, 'distance', 1)\n        frame, more = _campaign_ui_loop_fields(frame, 'choice')\n        if not more:\n            break\n    frame = _movement_arithmetic_long(state, frame, 'target_x', 8388608)\n    frame, more = _campaign_ui_loop_fields(frame, 'offset_y')\n    if not more:\n        break\nframe = _campaign_ui_bit_fields(state, frame, state.read(10551297, 1), 7)\nif not frame.status & 4:\n    frame = _campaign_ui_write_fields(state, frame, 37980, 12582916, 36610)\n    frame = _campaign_ui_write_fields(state, frame, 37988, 12582916, 1714421763, 4)\n    frame = _campaign_ui_write_fields(state, frame, 37998, 12582912, 32821)\n    frame = _campaign_ui_write_fields(state, frame, 38006, 12582912, 32822)\nframe = _campaign_ui_move_fields(state, frame, 'target_x', 0, 32)\nframe = _campaign_ui_call_fields(state, frame, 33042, 38022)\nframe = _campaign_ui_write_fields(state, frame, 38022, 4294964760, 40)\nframe = _campaign_ui_write_fields(state, frame, 38028, 4294964744, 300)\nstate.sr = 9472\nframe = first_replace(frame, status=0)\nreturn _campaign_ui_write_fields(state, frame, 38038, 4294964754, 256)"}})

DECLARATIONS.update({'initialize_z80_sound_image': {'signature': 'state: SceneState, inputs: InitializeZ80SoundImageInput', 'returns': 'InitializeZ80SoundImageResult', 'flow': "checked_state(state)\nif type(inputs) is not InitializeZ80SoundImageInput:\n    raise ValueError('function-specific typed input required')\ninputs.validate(state)\nincoming = FirstDeploymentFrame.unobserved()\nincoming = first_replace(incoming, target_x=inputs.value)\nobserved = initialize_z80_sound_image_fields(state, incoming)\nreturn InitializeZ80SoundImageResult(destination=state.table_at(observed.roster.address), source=state.table_at(observed.candidates.address), value=observed.target_x, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))"}})

DECLARATIONS.update({'initialize_z80_sound_image_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _campaign_ui_frame_fields(state, frame, 26960)\nframe = _campaign_ui_write_fields(state, frame, 26960, 10555648, 256)\nframe = _campaign_ui_call_fields(state, frame, 27064, 26972)\nwhile True:\n    frame = _campaign_ui_bit_fields(state, frame, state.read(10555648, 1), 0)\n    if frame.status & 4:\n        break\nframe = first_replace(frame, roster=state.table_at(27090).cursor(), candidates=state.table_at(10485760).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'target_x', 4095)\nwhile True:\n    value = frame.roster.byte()\n    frame = first_replace(frame, roster=frame.roster.advance(1))\n    frame = _campaign_ui_write_fields(state, frame, 26998, frame.candidates.address, value, 1)\n    frame = first_replace(frame, candidates=frame.candidates.advance(1))\n    frame, more = _campaign_ui_loop_fields(frame, 'target_x')\n    if not more:\n        break\nframe = first_replace(frame, roster=state.table_at(31132).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'target_x', 3583)\nwhile True:\n    value = frame.roster.byte()\n    frame = first_replace(frame, roster=frame.roster.advance(1))\n    frame = _campaign_ui_write_fields(state, frame, 27014, frame.candidates.address, value, 1)\n    frame = first_replace(frame, candidates=frame.candidates.advance(1))\n    frame, more = _campaign_ui_loop_fields(frame, 'target_x')\n    if not more:\n        break\nframe = first_replace(frame, roster=state.table_at(27050).cursor(), candidates=state.table_at(10492928).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'target_x', 12, 32)\nwhile True:\n    value = frame.roster.byte()\n    frame = first_replace(frame, roster=frame.roster.advance(1))\n    frame = _campaign_ui_write_fields(state, frame, 27032, frame.candidates.address, value, 1)\n    frame = first_replace(frame, candidates=frame.candidates.advance(1))\n    frame, more = _campaign_ui_loop_fields(frame, 'target_x')\n    if not more:\n        break\nframe = _campaign_ui_call_fields(state, frame, 27064, 27040)\nreturn _campaign_ui_write_fields(state, frame, 27040, 10555648, 0)"}})

DECLARATIONS.update({'poll_controller_with_z80_bus': {'signature': 'state: SceneState, inputs: PollControllerWithZ80BusInput', 'returns': 'PollControllerWithZ80BusResult', 'flow': "checked_state(state)\nif type(inputs) is not PollControllerWithZ80BusInput:\n    raise ValueError('function-specific typed input required')\ninputs.validate(state)\nincoming = FirstDeploymentFrame.unobserved()\nincoming = first_replace(incoming, target_x=inputs.value, target_y=inputs.field, unit=inputs.tile)\nobserved = poll_controller_with_z80_bus_fields(state, incoming)\nreturn PollControllerWithZ80BusResult(destination=state.table_at(observed.roster.address), source=state.table_at(observed.candidates.address), value=observed.target_x, field=observed.target_y, tile=observed.unit, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))"}})

DECLARATIONS.update({'poll_controller_with_z80_bus_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _campaign_ui_frame_fields(state, frame, 26570)\nframe = _campaign_ui_write_fields(state, frame, 26570, 10555648, 256)\nwhile True:\n    frame = _campaign_ui_bit_fields(state, frame, state.read(10555648, 1), 0)\n    if frame.status & 4:\n        break\nframe = _campaign_ui_call_fields(state, frame, 26600, 26590)\nreturn _campaign_ui_write_fields(state, frame, 26590, 10555648, 0)'}})

DECLARATIONS.update({'poll_two_controller_ports': {'signature': 'state: SceneState, inputs: PollTwoControllerPortsInput', 'returns': 'PollTwoControllerPortsResult', 'flow': "checked_state(state)\nif type(inputs) is not PollTwoControllerPortsInput:\n    raise ValueError('function-specific typed input required')\ninputs.validate(state)\nincoming = FirstDeploymentFrame.unobserved()\nincoming = first_replace(incoming, target_x=inputs.value, target_y=inputs.field, unit=inputs.tile)\nobserved = poll_two_controller_ports_fields(state, incoming)\nreturn PollTwoControllerPortsResult(destination=state.table_at(observed.roster.address), source=state.table_at(observed.candidates.address), value=observed.target_x, field=observed.target_y, tile=observed.unit, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))"}})

DECLARATIONS.update({'poll_two_controller_ports_alternate_1': {'signature': 'state: SceneState, inputs: PollTwoControllerPortsAlternate1Input', 'returns': 'PollTwoControllerPortsAlternate1Result', 'flow': "checked_state(state)\nif type(inputs) is not PollTwoControllerPortsAlternate1Input:\n    raise ValueError('function-specific typed input required')\ninputs.validate(state)\nincoming = FirstDeploymentFrame.unobserved()\nincoming = first_replace(incoming, roster=inputs.destination.cursor(), candidates=inputs.source.cursor(), target_x=inputs.value, target_y=inputs.field, unit=inputs.tile)\nobserved = poll_two_controller_ports_alternate_1_fields(state, incoming)\nreturn PollTwoControllerPortsAlternate1Result(destination=state.table_at(observed.roster.address), source=state.table_at(observed.candidates.address), value=observed.target_x, field=observed.target_y, tile=observed.unit, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))"}})

DECLARATIONS.update({'poll_two_controller_ports_alternate_1_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _campaign_ui_frame_fields(state, frame, 26614)\nreturn _campaign_ui_port_read_fields(state, frame)'}})

DECLARATIONS.update({'poll_two_controller_ports_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _campaign_ui_frame_fields(state, frame, 26600)\nframe = first_replace(frame, roster=state.table_at(4294964738).cursor(), candidates=state.table_at(10551299).cursor())\nframe = _campaign_ui_call_fields(state, frame, 26614, 26612)\nframe = first_replace(frame, candidates=frame.candidates.advance(2))\nreturn _campaign_ui_port_read_fields(state, frame)'}})

DECLARATIONS.update({'poll_world_map_input': {'signature': 'state: SceneState, inputs: PollWorldMapInputInput', 'returns': 'PollWorldMapInputResult', 'flow': "checked_state(state)\nif type(inputs) is not PollWorldMapInputInput:\n    raise ValueError('function-specific typed input required')\ninputs.validate(state)\nincoming = FirstDeploymentFrame.unobserved()\nincoming = first_replace(incoming, target_x=inputs.value, target_y=inputs.field, unit=inputs.tile, choice=inputs.remaining)\nobserved = poll_world_map_input_fields(state, incoming)\nreturn PollWorldMapInputResult(destination=state.table_at(observed.roster.address), source=state.table_at(observed.candidates.address), port=state.table_at(observed.auxiliary.address), value=observed.target_x, field=observed.target_y, tile=observed.unit, remaining=observed.choice, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))"}})

DECLARATIONS.update({'poll_world_map_input_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from .business_movement_support import _movement_test\nframe = _campaign_ui_frame_fields(state, frame, 18576)\nframe = _campaign_ui_call_fields(state, frame, 26570, 18582)\nframe = first_replace(frame, auxiliary=state.table_at(12582916).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'choice', state.read(4294964742, 2))\nframe = _campaign_ui_move_fields(state, frame, 'choice', low8(frame.choice) | 16, 8)\nframe = _campaign_ui_write_fields(state, frame, 18596, frame.auxiliary.address, low16(frame.choice))\nframe = _campaign_ui_write_fields(state, frame, 18598, 10555648, 256)\nframe = _campaign_ui_write_fields(state, frame, 18606, frame.auxiliary.address, 2483131200, 4)\nframe = _campaign_ui_write_fields(state, frame, 18612, frame.auxiliary.address, 2533135616, 4)\nframe = _campaign_ui_write_fields(state, frame, 18618, frame.auxiliary.address, 38783)\nframe = _campaign_ui_write_fields(state, frame, 18622, frame.auxiliary.address, 30720)\nframe = _campaign_ui_write_fields(state, frame, 18626, 4294964768, 130)\nframe = _campaign_ui_write_fields(state, frame, 18632, frame.auxiliary.address, state.read(4294964768, 2))\nframe = _movement_test(state, frame, state.read(16727808, 1), 8)\nif frame.status & 4:\n    frame = _campaign_ui_write_fields(state, frame, 18644, 10555648, 0)\nframe = _campaign_ui_write_fields(state, frame, 18652, frame.auxiliary.address, state.read(4294964742, 2))\nframe = _movement_test(state, frame, state.read(4294963998, 2), 16)\nif not frame.status & 4:\n    frame = first_replace(frame, auxiliary=state.table_at(12582916).cursor())\n    frame = _campaign_ui_move_fields(state, frame, 'choice', state.read(4294964742, 2))\n    frame = _campaign_ui_move_fields(state, frame, 'choice', low8(frame.choice) | 16, 8)\n    frame = _campaign_ui_write_fields(state, frame, 18678, frame.auxiliary.address, low16(frame.choice))\n    frame = _campaign_ui_write_fields(state, frame, 18680, 10555648, 256)\n    frame = _campaign_ui_write_fields(state, frame, 18688, frame.auxiliary.address, 2483065664, 4)\n    frame = _campaign_ui_write_fields(state, frame, 18694, frame.auxiliary.address, 2533201280, 4)\n    frame = _campaign_ui_write_fields(state, frame, 18700, frame.auxiliary.address, 38783)\n    frame = _campaign_ui_write_fields(state, frame, 18704, frame.auxiliary.address, 49152)\n    frame = _campaign_ui_write_fields(state, frame, 18708, 4294964768, 128)\n    frame = _campaign_ui_write_fields(state, frame, 18714, frame.auxiliary.address, state.read(4294964768, 2))\n    frame = _movement_test(state, frame, state.read(16727808, 1), 8)\n    if frame.status & 4:\n        frame = _campaign_ui_write_fields(state, frame, 18726, 10555648, 0)\n    frame = _campaign_ui_write_fields(state, frame, 18734, frame.auxiliary.address, state.read(4294964742, 2))\n    frame = _campaign_ui_write_fields(state, frame, 18738, 4294963998, 0, clear=True)\nframe = _campaign_ui_call_fields(state, frame, 18966, 18746)\nreturn _campaign_ui_call_fields(state, frame, 44294, 18752)"}})

DECLARATIONS.update({'poll_world_map_input_frame': {'signature': 'state: SceneState, frame: MapTickFrame', 'returns': 'MapTickFrame', 'flow': "from .business_main import _campaign_legacy_observations_fields\nincoming = _campaign_legacy_observations_fields(state, frame, 'world')\nobserved = poll_world_map_input_fields(state, incoming)\nreturn replace(frame, motion_x=observed.target_x, motion_y=observed.target_y, attributes=observed.unit, tile_count=observed.count, officer=observed.distance, count=observed.offset_x, index=observed.offset_y, control_latch=observed.choice, source=state.table_at(observed.roster.address), destination=state.table_at(observed.candidates.address), packet=state.table_at(observed.controller.address), vdp_port=state.table_at(observed.auxiliary.address), stack_cursor=observed.stack_cursor)"}})

DECLARATIONS.update({'queue_sound_word_list': {'signature': 'state: SceneState, inputs: QueueSoundWordListInput', 'returns': 'QueueSoundWordListResult', 'flow': "checked_state(state)\nif type(inputs) is not QueueSoundWordListInput:\n    raise ValueError('function-specific typed input required')\ninputs.validate(state)\nincoming = FirstDeploymentFrame.unobserved()\nincoming = first_replace(incoming, target_x=inputs.value, choice=inputs.remaining)\nobserved = queue_sound_word_list_fields(state, incoming)\nreturn QueueSoundWordListResult(source=state.table_at(observed.scan.address), descriptor=state.table_at(observed.roster.address), records=state.table_at(observed.controller.address), value=observed.target_x, remaining=observed.choice, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))"}})

DECLARATIONS.update({'queue_sound_word_list_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _campaign_ui_frame_fields(state, frame, 33012)\nframe = first_replace(frame, candidates=state.table_at(33068).cursor())\nframe = _campaign_ui_shift_fields(state, frame, 'target_x', 3)\nframe = first_replace(frame, candidates=frame.candidates.advance(s16(low16(frame.target_x))))\nsource = frame.candidates.long()\nframe = first_replace(frame, controller=state.table_at(source).cursor(), candidates=frame.candidates.advance(4))\ntarget = s16(frame.candidates.word()) & 4294967295\nframe = first_replace(frame, scan=state.table_at(target).cursor(), candidates=frame.candidates.advance(2))\nframe = first_replace(frame, scan=state.table_at(u32(frame.scan.base + 128)).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'choice', frame.candidates.word())\nframe = first_replace(frame, candidates=frame.candidates.advance(2))\nwhile True:\n    value = frame.controller.long()\n    frame = first_replace(frame, controller=frame.controller.advance(4))\n    frame = _campaign_ui_write_fields(state, frame, 33030, frame.scan.address(), value, 4)\n    frame = first_replace(frame, scan=frame.scan.advance(4))\n    frame, more = _campaign_ui_loop_fields(frame, 'choice')\n    if not more:\n        break\nfrom .business_commands import _city_ui_memory_arithmetic_fields\nreturn _city_ui_memory_arithmetic_fields(state, frame, 4294963998, 1)"}})

DECLARATIONS.update({'release_z80_reset': {'signature': 'state: SceneState, inputs: ReleaseZ80ResetInput', 'returns': 'ReleaseZ80ResetResult', 'flow': "checked_state(state)\nif type(inputs) is not ReleaseZ80ResetInput:\n    raise ValueError('function-specific typed input required')\ninputs.validate(state)\nincoming = FirstDeploymentFrame.unobserved()\nobserved = release_z80_reset_fields(state, incoming)\nreturn ReleaseZ80ResetResult(carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))"}})

DECLARATIONS.update({'release_z80_reset_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _campaign_ui_frame_fields(state, frame, 27064)\nframe = _campaign_ui_write_fields(state, frame, 27064, 10555904, 0)\nreturn _campaign_ui_write_fields(state, frame, 27080, 10555904, 256)'}})

DECLARATIONS.update({'upload_selected_mode_tile_rows': {'signature': 'state: SceneState, inputs: UploadSelectedModeTileRowsInput', 'returns': 'UploadSelectedModeTileRowsResult', 'flow': "checked_state(state)\nif type(inputs) is not UploadSelectedModeTileRowsInput:\n    raise ValueError('function-specific typed input required')\ninputs.validate(state)\nincoming = FirstDeploymentFrame.unobserved()\nincoming = first_replace(incoming, roster=inputs.destination.cursor(), target_y=inputs.field, unit=inputs.tile, stack_cursor=inputs.stack_cursor)\nobserved = upload_selected_mode_tile_rows_fields(state, incoming)\nreturn UploadSelectedModeTileRowsResult(destination=state.table_at(observed.roster.address), port=state.table_at(observed.auxiliary.address), field=observed.target_y, tile=observed.unit, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))"}})

DECLARATIONS.update({'upload_selected_mode_tile_rows_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _campaign_ui_frame_fields(state, frame, 42848)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, frame.roster.address)\nframe = first_replace(frame, stack_cursor=stack)\nfrom .business_movement_support import _movement_test_long\nframe = _movement_test_long(state, frame, frame.roster.address)\nframe = first_replace(frame, auxiliary=state.table_at(12582912).cursor(), roster=state.table_at(42910).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'unit', state.read(4294964048, 2))\nframe = _campaign_ui_shift_fields(state, frame, 'unit', 5)\nframe = _campaign_ui_write_fields(state, frame, 42866, 12582916, 1092616195, 4)\nframe = _campaign_ui_call_fields(state, frame, 42894, 42878)\nframe = _campaign_ui_write_fields(state, frame, 42878, 12582916, 1101004803, 4)\nframe = _campaign_ui_call_fields(state, frame, 42894, 42890)\nrestored = frame.stack_cursor.long()\nreturn first_replace(frame, roster=state.table_at(restored).cursor(), stack_cursor=frame.stack_cursor.advance(4))"}})

DECLARATIONS.update({'upload_selected_tile_row': {'signature': 'state: SceneState, inputs: UploadSelectedTileRowInput', 'returns': 'UploadSelectedTileRowResult', 'flow': "checked_state(state)\nif type(inputs) is not UploadSelectedTileRowInput:\n    raise ValueError('function-specific typed input required')\ninputs.validate(state)\nincoming = FirstDeploymentFrame.unobserved()\nincoming = first_replace(incoming, roster=inputs.destination.cursor(), auxiliary=inputs.port.cursor(), target_y=inputs.field, unit=inputs.tile)\nobserved = upload_selected_tile_row_fields(state, incoming)\nreturn UploadSelectedTileRowResult(field=observed.target_y, tile=observed.unit, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))"}})

DECLARATIONS.update({'upload_selected_tile_row_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _campaign_ui_frame_fields(state, frame, 42894)\nframe = _campaign_ui_move_fields(state, frame, 'target_y', 7)\nwhile True:\n    value = frame.roster.word(low16(frame.unit))\n    frame = _campaign_ui_write_fields(state, frame, 42898, frame.auxiliary.address, value)\n    frame = _campaign_ui_arithmetic_fields(state, frame, 'unit', 2)\n    frame, more = _campaign_ui_loop_fields(frame, 'target_y')\n    if not more:\n        return frame"}})

DECLARATIONS.update({'upload_selection_layout': {'signature': 'state: SceneState, inputs: UploadSelectionLayoutInput', 'returns': 'UploadSelectionLayoutResult', 'flow': "checked_state(state)\nif type(inputs) is not UploadSelectionLayoutInput:\n    raise ValueError('function-specific typed input required')\ninputs.validate(state)\nincoming = FirstDeploymentFrame.unobserved()\nincoming = first_replace(incoming, distance=inputs.offset)\nobserved = upload_selection_layout_fields(state, incoming)\nreturn UploadSelectionLayoutResult(destination=state.table_at(observed.roster.address), offset=observed.distance, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))"}})

DECLARATIONS.update({'upload_selection_layout_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _campaign_ui_frame_fields(state, frame, 21186)\nframe = _campaign_ui_write_fields(state, frame, 21186, 12582916, 1879048193, 4)\nframe = first_replace(frame, roster=state.table_at(564700).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'distance', 23)\nframe = _campaign_ui_copy_panel_longs_fields(state, frame, 'roster', 'distance', 21206, 12582912)\nframe = _campaign_ui_write_fields(state, frame, 21216, 12582916, 1889533953, 4)\nframe = first_replace(frame, roster=state.table_at(565084).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'distance', 7)\nframe = _campaign_ui_copy_panel_longs_fields(state, frame, 'roster', 'distance', 21236, 12582912)\nframe = _campaign_ui_write_fields(state, frame, 21246, 12582916, 1912602625, 4)\nframe = _campaign_ui_move_fields(state, frame, 'distance', 7)\nwhile True:\n    frame = _campaign_ui_write_fields(state, frame, 21260, 12582912, 858993459, 4)\n    frame, more = _campaign_ui_loop_fields(frame, 'distance')\n    if not more:\n        break\nframe = first_replace(frame, roster=state.table_at(565436).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'distance', 7)\nreturn _campaign_ui_copy_panel_longs_fields(state, frame, 'roster', 'distance', 21284, 12582912)"}})

DECLARATIONS.update({'upload_world_map_palette': {'signature': 'state: SceneState, inputs: UploadWorldMapPaletteInput', 'returns': 'UploadWorldMapPaletteResult', 'flow': "checked_state(state)\nif type(inputs) is not UploadWorldMapPaletteInput:\n    raise ValueError('function-specific typed input required')\ninputs.validate(state)\nincoming = FirstDeploymentFrame.unobserved()\nincoming = first_replace(incoming, target_x=inputs.value)\nobserved = upload_world_map_palette_fields(state, incoming)\nreturn UploadWorldMapPaletteResult(value=observed.target_x, carry=bool(observed.status & 1), zero=bool(observed.status & 4), negative=bool(observed.status & 8), overflow=bool(observed.status & 2))"}})

DECLARATIONS.update({'upload_world_map_palette_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _campaign_ui_frame_fields(state, frame, 18840)\nframe = _campaign_ui_write_fields(state, frame, 18840, 12582916, 2080374786, 4)\nframe = _campaign_ui_move_fields(state, frame, 'target_x', state.read(4294963990, 2))\nframe = _campaign_ui_negate_word_fields(state, frame, 'target_x')\nframe = _campaign_ui_write_fields(state, frame, 18856, 12582912, low16(frame.target_x))\nframe = _campaign_ui_move_fields(state, frame, 'target_x', state.read(4294963992, 2))\nframe = _campaign_ui_negate_word_fields(state, frame, 'target_x')\nframe = _campaign_ui_write_fields(state, frame, 18868, 12582912, low16(frame.target_x))\nframe = _campaign_ui_write_fields(state, frame, 18874, 12582916, 1073741840, 4)\nframe = _campaign_ui_write_fields(state, frame, 18884, 12582912, state.read(4294963986, 2))\nreturn _campaign_ui_write_fields(state, frame, 18892, 12582912, state.read(4294963988, 2))"}})

APPROVED.setdefault('contexts_lowbank',set()).update(('PaletteRefreshFields',))

APPROVED.setdefault('business_main',set()).update(('_campaign_legacy_observations_fields',))

APPROVED.setdefault('business_commands',set()).update(('_city_ui_frame_fields',))

APPROVED.setdefault('business_movement_support',set()).update(('_movement_move', '_movement_move_long'))

APPROVED.setdefault('business_main',set()).update(('_campaign_emit_fields',))

APPROVED.setdefault('business_main',set()).update(('_campaign_call_fields',))

APPROVED.setdefault('business_map',set()).update(('_world_map_bit_fields',))

APPROVED.setdefault('business_scene_support',set()).update(('_aux_text_shift_word_fields',))

APPROVED.setdefault('business_commands',set()).update(('_city_ui_arithmetic_fields',))

APPROVED.setdefault('business_movement_support',set()).update(('_movement_binary_flags',))

APPROVED.setdefault('business_commands',set()).update(('_city_ui_memory_arithmetic_fields',))

APPROVED.setdefault('business_movement_support',set()).update(('_movement_test_long',))

APPROVED.setdefault('business_movement_support',set()).update(('_movement_test',))

APPROVED.setdefault('business_movement_support',set()).update(('_movement_arithmetic_long',))

# Live Scene Cursor address correction; ordinary lowering unchanged.
DECLARATIONS.update({'_campaign_ui_port_read_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _campaign_ui_write_fields(state, frame, 26614, frame.candidates.base, 0, 1)\nframe = _campaign_ui_move_fields(state, frame, 'target_x', frame.candidates.byte(), 8)\nframe = _campaign_ui_controller_shift_fields(state, frame)\nframe = _campaign_ui_move_fields(state, frame, 'target_x', low8(frame.target_x) & 192, 8)\nframe = _campaign_ui_write_fields(state, frame, 26630, frame.candidates.base, 64, 1)\nframe = _campaign_ui_move_fields(state, frame, 'target_y', frame.candidates.byte(), 8)\nframe = _campaign_ui_move_fields(state, frame, 'target_y', low8(frame.target_y) & 63, 8)\nframe = _campaign_ui_move_fields(state, frame, 'target_x', low8(frame.target_x) | low8(frame.target_y), 8)\nframe = _campaign_ui_move_fields(state, frame, 'target_x', low8(frame.target_x) ^ 255, 8)\nframe = _campaign_ui_move_fields(state, frame, 'target_y', low8(frame.target_x), 8)\nframe = _campaign_ui_move_fields(state, frame, 'unit', frame.roster.byte(), 8)\nframe = _campaign_ui_move_fields(state, frame, 'target_x', low8(frame.target_x) ^ low8(frame.unit), 8)\nframe = _campaign_ui_write_fields(state, frame, 26654, frame.roster.base, low8(frame.target_y), 1)\nframe = first_replace(frame, roster=frame.roster.advance(1))\nframe = _campaign_ui_move_fields(state, frame, 'target_x', low8(frame.target_x) & low8(frame.target_y), 8)\nframe = _campaign_ui_write_fields(state, frame, 26658, frame.roster.base, low8(frame.target_x), 1)\nreturn first_replace(frame, roster=frame.roster.advance(1))"}})

# Live device integration; ordinary target lowering unchanged.
DECLARATIONS.update({'initialize_z80_sound_image_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _campaign_ui_frame_fields(state, frame, 26960)\nframe = _campaign_ui_write_fields(state, frame, 26960, 10555648, 256)\nframe = _campaign_ui_call_fields(state, frame, 27064, 26972)\nwhile True:\n    frame = _campaign_ui_bit_fields(state, frame, state.read(10555648, 1), 0)\n    if frame.status & 4:\n        break\nframe = first_replace(frame, roster=state.table_at(27090).cursor(), candidates=state.table_at(10485760).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'target_x', 4095)\nwhile True:\n    value = frame.roster.byte()\n    frame = first_replace(frame, roster=frame.roster.advance(1))\n    frame = _campaign_ui_write_fields(state, frame, 26998, frame.candidates.base, value, 1)\n    frame = first_replace(frame, candidates=frame.candidates.advance(1))\n    frame, more = _campaign_ui_loop_fields(frame, 'target_x')\n    if not more:\n        break\nframe = first_replace(frame, roster=state.table_at(31132).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'target_x', 3583)\nwhile True:\n    value = frame.roster.byte()\n    frame = first_replace(frame, roster=frame.roster.advance(1))\n    frame = _campaign_ui_write_fields(state, frame, 27014, frame.candidates.base, value, 1)\n    frame = first_replace(frame, candidates=frame.candidates.advance(1))\n    frame, more = _campaign_ui_loop_fields(frame, 'target_x')\n    if not more:\n        break\nframe = first_replace(frame, roster=state.table_at(27050).cursor(), candidates=state.table_at(10492928).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'target_x', 12, 32)\nwhile True:\n    value = frame.roster.byte()\n    frame = first_replace(frame, roster=frame.roster.advance(1))\n    frame = _campaign_ui_write_fields(state, frame, 27032, frame.candidates.base, value, 1)\n    frame = first_replace(frame, candidates=frame.candidates.advance(1))\n    frame, more = _campaign_ui_loop_fields(frame, 'target_x')\n    if not more:\n        break\nframe = _campaign_ui_call_fields(state, frame, 27064, 27040)\nreturn _campaign_ui_write_fields(state, frame, 27040, 10555648, 0)"}})

# Original4890 live VDP Cursor correction; ordinary lowering unchanged.
DECLARATIONS.update({'poll_world_map_input_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from .business_movement_support import _movement_test\nframe = _campaign_ui_frame_fields(state, frame, 18576)\nframe = _campaign_ui_call_fields(state, frame, 26570, 18582)\nframe = first_replace(frame, auxiliary=state.table_at(12582916).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'choice', state.read(4294964742, 2))\nframe = _campaign_ui_move_fields(state, frame, 'choice', low8(frame.choice) | 16, 8)\nframe = _campaign_ui_write_fields(state, frame, 18596, frame.auxiliary.base, low16(frame.choice))\nframe = _campaign_ui_write_fields(state, frame, 18598, 10555648, 256)\nframe = _campaign_ui_write_fields(state, frame, 18606, frame.auxiliary.base, 2483131200, 4)\nframe = _campaign_ui_write_fields(state, frame, 18612, frame.auxiliary.base, 2533135616, 4)\nframe = _campaign_ui_write_fields(state, frame, 18618, frame.auxiliary.base, 38783)\nframe = _campaign_ui_write_fields(state, frame, 18622, frame.auxiliary.base, 30720)\nframe = _campaign_ui_write_fields(state, frame, 18626, 4294964768, 130)\nframe = _campaign_ui_write_fields(state, frame, 18632, frame.auxiliary.base, state.read(4294964768, 2))\nframe = _movement_test(state, frame, state.read(16727808, 1), 8)\nif frame.status & 4:\n    frame = _campaign_ui_write_fields(state, frame, 18644, 10555648, 0)\nframe = _campaign_ui_write_fields(state, frame, 18652, frame.auxiliary.base, state.read(4294964742, 2))\nframe = _movement_test(state, frame, state.read(4294963998, 2), 16)\nif not frame.status & 4:\n    frame = first_replace(frame, auxiliary=state.table_at(12582916).cursor())\n    frame = _campaign_ui_move_fields(state, frame, 'choice', state.read(4294964742, 2))\n    frame = _campaign_ui_move_fields(state, frame, 'choice', low8(frame.choice) | 16, 8)\n    frame = _campaign_ui_write_fields(state, frame, 18678, frame.auxiliary.base, low16(frame.choice))\n    frame = _campaign_ui_write_fields(state, frame, 18680, 10555648, 256)\n    frame = _campaign_ui_write_fields(state, frame, 18688, frame.auxiliary.base, 2483065664, 4)\n    frame = _campaign_ui_write_fields(state, frame, 18694, frame.auxiliary.base, 2533201280, 4)\n    frame = _campaign_ui_write_fields(state, frame, 18700, frame.auxiliary.base, 38783)\n    frame = _campaign_ui_write_fields(state, frame, 18704, frame.auxiliary.base, 49152)\n    frame = _campaign_ui_write_fields(state, frame, 18708, 4294964768, 128)\n    frame = _campaign_ui_write_fields(state, frame, 18714, frame.auxiliary.base, state.read(4294964768, 2))\n    frame = _movement_test(state, frame, state.read(16727808, 1), 8)\n    if frame.status & 4:\n        frame = _campaign_ui_write_fields(state, frame, 18726, 10555648, 0)\n    frame = _campaign_ui_write_fields(state, frame, 18734, frame.auxiliary.base, state.read(4294964742, 2))\n    frame = _campaign_ui_write_fields(state, frame, 18738, 4294963998, 0, clear=True)\nframe = _campaign_ui_call_fields(state, frame, 18966, 18746)\nreturn _campaign_ui_call_fields(state, frame, 44294, 18752)"}})

# Finite campaign Scene view access repair; ordinary lowering/APPROVED unchanged.
DECLARATIONS.update({'draw_scene_header_glyphs_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _campaign_ui_frame_fields(state, frame, 20996)\nframe = first_replace(frame, roster=state.table_at(565756).cursor(), candidates=state.table_at(4294955776).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'count', 1)\nframe = _campaign_ui_call_fields(state, frame, 44682, 21016)\nframe = first_replace(frame, roster=state.table_at(565760).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'count', 9)\nframe = _campaign_ui_call_fields(state, frame, 44682, 21032)\nframe = _campaign_ui_write_fields(state, frame, 21032, 12582916, 1509949440, 4)\nframe = first_replace(frame, candidates=state.table_at(4294955776).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'distance', 383)\nreturn _campaign_ui_copy_panel_longs_fields(state, frame, 'candidates', 'distance', 21050, frame.auxiliary.base)"}, 'draw_scene_footer_glyphs_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _campaign_ui_frame_fields(state, frame, 21360)\nframe = first_replace(frame, roster=state.table_at(566310).cursor(), candidates=state.table_at(4294955776).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'count', 9)\nframe = _campaign_ui_call_fields(state, frame, 44830, 21380)\nframe = _campaign_ui_write_fields(state, frame, 21380, 12582916, 1891631105, 4)\nframe = first_replace(frame, candidates=state.table_at(4294955776).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'unit', 79)\nreturn _campaign_ui_copy_panel_longs_fields(state, frame, 'candidates', 'unit', 21398, frame.auxiliary.base)"}, 'upload_selected_tile_row_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _campaign_ui_frame_fields(state, frame, 42894)\nframe = _campaign_ui_move_fields(state, frame, 'target_y', 7)\nwhile True:\n    value = frame.roster.word(low16(frame.unit))\n    frame = _campaign_ui_write_fields(state, frame, 42898, frame.auxiliary.base, value)\n    frame = _campaign_ui_arithmetic_fields(state, frame, 'unit', 2)\n    frame, more = _campaign_ui_loop_fields(frame, 'target_y')\n    if not more:\n        return frame"}, 'upload_selected_mode_tile_rows_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _campaign_ui_frame_fields(state, frame, 42848)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, frame.roster.base)\nframe = first_replace(frame, stack_cursor=stack)\nfrom .business_movement_support import _movement_test_long\nframe = _movement_test_long(state, frame, frame.roster.base)\nframe = first_replace(frame, auxiliary=state.table_at(12582912).cursor(), roster=state.table_at(42910).cursor())\nframe = _campaign_ui_move_fields(state, frame, 'unit', state.read(4294964048, 2))\nframe = _campaign_ui_shift_fields(state, frame, 'unit', 5)\nframe = _campaign_ui_write_fields(state, frame, 42866, 12582916, 1092616195, 4)\nframe = _campaign_ui_call_fields(state, frame, 42894, 42878)\nframe = _campaign_ui_write_fields(state, frame, 42878, 12582916, 1101004803, 4)\nframe = _campaign_ui_call_fields(state, frame, 42894, 42890)\nrestored = frame.stack_cursor.long()\nreturn first_replace(frame, roster=state.table_at(restored).cursor(), stack_cursor=frame.stack_cursor.advance(4))"}, '_campaign_ui_copy_panel_longs_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, source_carrier: str, count_carrier: str, instruction: int, destination: int', 'returns': 'FirstDeploymentFrame', 'flow': "if source_carrier not in ('roster', 'candidates'):\n    raise ValueError('only original roster/candidates panel source views are admitted')\nwhile True:\n    source = state.checked_table(getattr(frame, source_carrier))\n    value = source.long()\n    frame = first_replace(frame, **{source_carrier: source.advance(4)})\n    frame = _campaign_ui_write_fields(state, frame, instruction, destination, value, 4)\n    frame, more = _campaign_ui_loop_fields(frame, count_carrier)\n    if not more:\n        return frame"}})
