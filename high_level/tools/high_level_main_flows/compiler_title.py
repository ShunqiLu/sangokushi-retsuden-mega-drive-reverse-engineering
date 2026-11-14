"""Restricted business-text admission and ordinary mnemonic lowering.
An intermediate fixed-structure compiler, not arbitrary Python or CPU proof.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import BUSINESS_TITLE_BINDINGS

APPROVED={'contexts_main': {'BitmapTileResult', 'SceneTick', 'SoundWord', 'BitmapRow'},
 'domain': {'Cursor',
            'Long',
            'SceneState',
            'Table',
            'VideoPlaneAddress',
            'Word',
            'checked_cursor',
            'checked_state',
            'checked_table',
            'data_view',
            'descending_inclusive',
            'divu_retained',
            'high16',
            'low16',
            'ram_view',
            'replace_word',
            's16',
            'swap_words',
            'u16',
            'u32',
            'uint'},
 'services': {'begin_scene_palette_darken',
              'call_target',
              'clear_video_sprite_plane',
              'copy_scene_palette_variant',
              'enqueue_sound_command',
              'initialize_video_registers_and_planes',
              'read_vdp_plane_literal_rows',
              'read_vdp_plane_rle_rows',
              'snapshot_and_clear_scene_palette',
              'write_vdp_swapped_byte_rle_stream'}}

DECLARATIONS={'_ram': {'signature': 'state, address',
          'returns': None,
          'flow': "return ram_view(state, 'ram_%04x' % address)"},
 '_begin_title_transfer': {'signature': 'state, reset_scroll',
                           'returns': None,
                           'flow': 'state.set_status_word(9984)\n'
                                   'state.write(12582916, 2, _ram(state, 62982).word() & 65471)\n'
                                   'if reset_scroll:\n'
                                   '    _ram(state, 62226).set_word(0, 0)\n'
                                   '    _ram(state, 62228).set_word(0, 0)\n'
                                   '    _ram(state, 62230).set_word(0, 0)\n'
                                   '    _ram(state, 62232).set_word(0, 0)\n'
                                   'clear_video_sprite_plane(state)'},
 'initialize_title_scene': {'signature': 'state: SceneState, literal_marker: Long',
                            'returns': None,
                            'flow': 'checked_state(state)\n'
                                    '_ram(state, 62254).set_word(0, 0)\n'
                                    'return initialize_title_scene_preserving_mode(state, '
                                    'literal_marker)'},
 'initialize_title_scene_preserving_mode': {'signature': 'state: SceneState, literal_marker: Long',
                                            'returns': None,
                                            'flow': 'checked_state(state)\n'
                                                    'uint(literal_marker, 32)\n'
                                                    '_begin_title_transfer(state, True)\n'
                                                    'initialize_video_registers_and_planes(state)\n'
                                                    'state.write(12582916, 4, 1610612738)\n'
                                                    'for _ in range(8192):\n'
                                                    '    state.write(12582912, 2, 0)\n'
                                                    'state.write(12582916, 2, 36610)\n'
                                                    'state.write(12582916, 2, 33328)\n'
                                                    'state.write(12582916, 2, 33584)\n'
                                                    'state.write(12582916, 2, 33799)\n'
                                                    'state.write(12582916, 2, 34140)\n'
                                                    'state.write(12582916, 2, 34560)\n'
                                                    'state.write(12582916, 2, 35584)\n'
                                                    'state.write(12582916, 2, 35969)\n'
                                                    'state.write(12582916, 2, 36143)\n'
                                                    'state.write(12582916, 2, 36610)\n'
                                                    'state.write(12582916, 2, 36881)\n'
                                                    'state.write(12582916, 2, 37248)\n'
                                                    'state.write(12582916, 2, 37376)\n'
                                                    'write_vdp_swapped_byte_rle_stream(state, '
                                                    "data_view(state, 'data_05d5e4').cursor(), "
                                                    'VideoPlaneAddress(0))\n'
                                                    'write_vdp_swapped_byte_rle_stream(state, '
                                                    "data_view(state, 'data_05f137').cursor(), "
                                                    'VideoPlaneAddress(8192))\n'
                                                    'write_vdp_swapped_byte_rle_stream(state, '
                                                    "data_view(state, 'data_060e6c').cursor(), "
                                                    'VideoPlaneAddress(16384))\n'
                                                    'write_vdp_swapped_byte_rle_stream(state, '
                                                    "data_view(state, 'data_06254f').cursor(), "
                                                    'VideoPlaneAddress(32768))\n'
                                                    'write_vdp_swapped_byte_rle_stream(state, '
                                                    "data_view(state, 'data_064340').cursor(), "
                                                    'VideoPlaneAddress(40960))\n'
                                                    'state.write(12582916, 2, 36610)\n'
                                                    'state.write(12582916, 4, 1845493761)\n'
                                                    "source = data_view(state, 'data_0d374a').cursor()\n"
                                                    'for _ in range(1024):\n'
                                                    '    state.write(12582912, 4, source.next_long())\n'
                                                    'read_vdp_plane_literal_rows(state, '
                                                    "data_view(state, 'data_0655f1').cursor(), "
                                                    'VideoPlaneAddress(57344), 128, 32, '
                                                    'literal_marker)\n'
                                                    'read_vdp_plane_rle_rows(state, data_view(state, '
                                                    "'data_065df3').cursor(), VideoPlaneAddress(57408), "
                                                    '128)\n'
                                                    'copy_scene_palette_variant(state, 17)\n'
                                                    'snapshot_and_clear_scene_palette(state)\n'
                                                    '_ram(state, 32970).set_word(0, 65535)\n'
                                                    '_ram(state, 32972).set_word(0, 65535)\n'
                                                    '_ram(state, 32974).set_word(0, 65535)\n'
                                                    '_ram(state, 32976).set_word(0, 65535)\n'
                                                    'begin_scene_palette_darken(state, 1)\n'
                                                    '_ram(state, 62251).set_byte(0, 0)\n'
                                                    '_ram(state, 62994).set_word(0, 768)\n'
                                                    'if _ram(state, 62976).word() != 16:\n'
                                                    '    enqueue_sound_command(state, 129)\n'
                                                    '    _ram(state, 62252).set_word(0, 3)\n'
                                                    'upload_title_emblem_set(state, _ram(state, '
                                                    '62252).word())\n'
                                                    '_ram(state, 62984).set_word(0, 4)\n'
                                                    'state.set_status_word(9472)'},
 'return_title_idle_slot': {'signature': 'state: SceneState',
                            'returns': None,
                            'flow': 'checked_state(state)'},
 'initialize_secondary_title_scene': {'signature': 'state: SceneState',
                                      'returns': None,
                                      'flow': 'checked_state(state)\n'
                                              '_begin_title_transfer(state, True)\n'
                                              'state.write(12582916, 2, 33328)\n'
                                              'state.write(12582916, 2, 33592)\n'
                                              'state.write(12582916, 2, 33798)\n'
                                              'state.write(12582916, 2, 34140)\n'
                                              'call_target(state, 33042, SoundWord(4))\n'
                                              'call_target(state, 218108, SceneTick())\n'
                                              '_ram(state, 62270).set_word(0, 49532)\n'
                                              '_ram(state, 62272).set_word(0, 49532)\n'
                                              '_ram(state, 62268).set_word(0, 1)\n'
                                              '_ram(state, 62274).set_word(0, 0)\n'
                                              '_ram(state, 62276).set_word(0, 0)\n'
                                              '_ram(state, 62278).set_word(0, 65040)\n'
                                              '_ram(state, 62254).set_word(0, 0)\n'
                                              '_ram(state, 62251).set_byte(0, 0)\n'
                                              '_ram(state, 62984).set_word(0, 4)\n'
                                              '_ram(state, 62994).set_word(0, 771)\n'
                                              'state.set_status_word(9472)'},
 'initialize_title_transition_scene': {'signature': 'state: SceneState',
                                       'returns': None,
                                       'flow': 'checked_state(state)\n'
                                               '_begin_title_transfer(state, False)\n'
                                               'state.write(12582916, 2, 33328)\n'
                                               'state.write(12582916, 2, 33592)\n'
                                               'state.write(12582916, 2, 33798)\n'
                                               'state.write(12582916, 2, 34140)\n'
                                               'call_target(state, 218586, SceneTick())\n'
                                               '_ram(state, 62280).set_word(0, u16(_ram(state, '
                                               '62280).word() + 1))\n'
                                               '_ram(state, 62230).set_word(0, 0)\n'
                                               'palette = _ram(state, 64256).cursor()\n'
                                               'for _ in range(16):\n'
                                               '    palette.append_long(0)\n'
                                               '_ram(state, 62238).set_word(0, u16(_ram(state, '
                                               '62238).word() + 1))\n'
                                               '_ram(state, 62284).set_word(0, u16(_ram(state, '
                                               '62284).word() + 1))\n'
                                               '_ram(state, 62254).set_word(0, 0)\n'
                                               '_ram(state, 62251).set_byte(0, 0)\n'
                                               '_ram(state, 62984).set_word(0, 4)\n'
                                               'state.set_status_word(9472)'},
 'upload_title_emblem_set': {'signature': 'state: SceneState, scale: Word',
                             'returns': None,
                             'flow': 'checked_state(state)\n'
                                     'uint(scale, 16)\n'
                                     "pointers = data_view(state, 'data_003a3e').cursor()\n"
                                     'tile = 768\n'
                                     'for _ in range(7):\n'
                                     '    source = state.table_at(pointers.next_long())\n'
                                     '    destination = _ram(state, 53504).cursor()\n'
                                     '    scale_title_bitmap_to_tiles(state, source, destination, 32, '
                                     '32, scale)\n'
                                     '    upload_title_bitmap_tile_rows(state, _ram(state, '
                                     '53504).cursor(), tile)\n'
                                     '    tile = u16(tile + 16)'},
 'scale_title_bitmap_to_tiles': {'signature': 'state: SceneState, source: Table, destination: Cursor, '
                                              'source_height: Word, source_width: Word, output_height: '
                                              'Word',
                                 'returns': None,
                                 'flow': 'checked_state(state)\n'
                                         'checked_table(source, state)\n'
                                         'checked_cursor(destination, state)\n'
                                         'uint(source_height, 16)\n'
                                         'uint(source_width, 16)\n'
                                         'uint(output_height, 16)\n'
                                         'step = u32((divu_retained(u16(source_width << 8), '
                                         'output_height) & 65535) << 8)\n'
                                         'vertical, rows_remaining = (0, source_height)\n'
                                         'while True:\n'
                                         '    scanline = select_title_bitmap_scanline(state, source, '
                                         'source_height, source_width, vertical)\n'
                                         '    row = BitmapRow(scanline, source_width, source_height, '
                                         'step, vertical, 0, 0, source_width)\n'
                                         '    column_buffer, remaining_width = (destination, '
                                         'source_width)\n'
                                         '    while True:\n'
                                         '        pixels = pack_title_bitmap_tile_row(state, row, '
                                         'column_buffer)\n'
                                         '        row = BitmapRow(scanline, source_width, '
                                         'source_height, step, vertical, pixels.horizontal, '
                                         'pixels.pending_pixels, remaining_width)\n'
                                         '        previous_width = remaining_width\n'
                                         '        remaining_width = u16(remaining_width - 8)\n'
                                         '        if previous_width <= 8:\n'
                                         '            break\n'
                                         '        column_buffer = column_buffer.advance(128)\n'
                                         '    vertical = u32(vertical + step)\n'
                                         '    rows_remaining = u16(rows_remaining - 1)\n'
                                         '    if rows_remaining == 0:\n'
                                         '        return\n'
                                         '    destination = destination.advance(4)'},
 'select_title_bitmap_scanline': {'signature': 'state: SceneState, source: Table, source_height: Word, '
                                               'source_width: Word, vertical: Long',
                                  'returns': 'Table | None',
                                  'flow': 'checked_state(state)\n'
                                          'checked_table(source, state)\n'
                                          'uint(source_height, 16)\n'
                                          'uint(source_width, 16)\n'
                                          'uint(vertical, 32)\n'
                                          'row_index = high16(vertical)\n'
                                          'if row_index >= source_height:\n'
                                          '    return None\n'
                                          'row_offset = u16((source_width >> 3) * row_index)\n'
                                          'return source.at(row_offset)'},
 'pack_title_bitmap_tile_row': {'signature': 'state: SceneState, row: BitmapRow, destination: Cursor',
                                'returns': 'BitmapTileResult',
                                'flow': 'if type(row) is not BitmapRow:\n'
                                        "    raise ValueError('explicit BitmapRow required')\n"
                                        'row.validate(state)\n'
                                        'checked_cursor(destination, state)\n'
                                        'pixels, horizontal = (row.pending_pixels, row.horizontal)\n'
                                        'if row.source is None or row.source.base & 2147483648:\n'
                                        '    pixels = 0\n'
                                        'else:\n'
                                        '    for _ in range(8):\n'
                                        '        pixels = u32(pixels << 4)\n'
                                        '        column = high16(horizontal)\n'
                                        '        if column < row.source_width:\n'
                                        '            packed = row.source.byte(u16(column >> 3))\n'
                                        '            if packed & 1 << (column & 7):\n'
                                        '                pixels = replace_word(pixels, low16(pixels) | '
                                        '15)\n'
                                        '        horizontal = u32(horizontal + row.step)\n'
                                        'destination.set_long(0, pixels)\n'
                                        'return BitmapTileResult(horizontal, pixels)'},
 'upload_title_bitmap_tile_rows': {'signature': 'state: SceneState, source: Cursor, tile: Long',
                                   'returns': None,
                                   'flow': 'checked_state(state)\n'
                                           'checked_cursor(source, state)\n'
                                           'uint(tile, 32)\n'
                                           'command = u32(tile << 7) & 262016\n'
                                           'command = replace_word(command, low16(command) >> 2 | '
                                           '16384)\n'
                                           'state.write(12582916, 4, swap_words(command))\n'
                                           'for _ in range(256):\n'
                                           '    state.write(12582912, 2, source.next_word())\n'
                                           '_ram(state, 53504).set_word(0, 0)'}}

def _lower_initialize_title_scene(emitter,rules):
    emitter.segment(0x3e0,0x3e8)
    emitter.ins('bra.w','main_pc_00378e',4)
    emitter.ins('bra.w','main_pc_003792',4)
    emitter.segment(0x378e,0x3958)
    emitter.ins('clr.w','0xf32e:w',4)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.w','0xf606:w,%d0',4)
    emitter.ins('andi.b','#0xbf,%d0',4)
    emitter.ins('move.w','%d0,0xc00004:l',6)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('move.w','%d0,0xf312:w',4)
    emitter.ins('move.w','%d0,0xf314:w',4)
    emitter.ins('move.w','%d0,0xf316:w',4)
    emitter.ins('move.w','%d0,0xf318:w',4)
    emitter.ins('jsr','main_pc_0068ce:l',6)
    emitter.ins('jsr','main_pc_006826:l',6)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x0,%d6',4)
    emitter.ins('move.w','#0x1fff,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,main_pc_0037da',4)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.w','#0x8230,0xc00004:l',8)
    emitter.ins('move.w','#0x8330,0xc00004:l',8)
    emitter.ins('move.w','#0x8407,0xc00004:l',8)
    emitter.ins('move.w','#0x855c,0xc00004:l',8)
    emitter.ins('move.w','#0x8700,0xc00004:l',8)
    emitter.ins('move.w','#0x8b00,0xc00004:l',8)
    emitter.ins('move.w','#0x8c81,0xc00004:l',8)
    emitter.ins('move.w','#0x8d2f,0xc00004:l',8)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.w','#0x9011,0xc00004:l',8)
    emitter.ins('move.w','#0x9180,0xc00004:l',8)
    emitter.ins('move.w','#0x9200,0xc00004:l',8)
    emitter.ins('lea.l','0x5d5e4:l,%a0',6)
    emitter.ins('move.w','#0x0,%d0',4)
    emitter.ins('jsr','main_pc_03ab52:l',6)
    emitter.ins('lea.l','0x5f137:l,%a0',6)
    emitter.ins('move.w','#0x2000,%d0',4)
    emitter.ins('jsr','main_pc_03ab52:l',6)
    emitter.ins('lea.l','0x60e6c:l,%a0',6)
    emitter.ins('move.w','#0x4000,%d0',4)
    emitter.ins('jsr','main_pc_03ab52:l',6)
    emitter.ins('lea.l','0x6254f:l,%a0',6)
    emitter.ins('move.w','#0x8000,%d0',4)
    emitter.ins('jsr','main_pc_03ab52:l',6)
    emitter.ins('lea.l','0x64340:l,%a0',6)
    emitter.ins('move.w','#0xa000,%d0',4)
    emitter.ins('jsr','main_pc_03ab52:l',6)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x6e000001,0xc00004:l',10)
    emitter.ins('lea.l','0xd374a:l,%a0',6)
    emitter.ins('move.w','#0x3ff,%d0',4)
    emitter.ins('move.l','(%a0)+,0xc00000:l',6)
    emitter.ins('dbra','%d0,main_pc_0038b4',4)
    emitter.ins('lea.l','0x655f1:l,%a0',6)
    emitter.ins('lea.l','0xe000:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('move.w','#0x20,%d6',4)
    emitter.ins('jsr','main_pc_03aab6:l',6)
    emitter.ins('lea.l','0x65df3:l,%a0',6)
    emitter.ins('lea.l','0xe040:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('jsr','main_pc_03aace:l',6)
    emitter.ins('moveq','#17,%d0',2)
    emitter.ins('jsr','main_pc_03ab94:l',6)
    emitter.ins('jsr','main_pc_03aa8a:l',6)
    emitter.ins('move.w','#0xffff,0x80ca:w',6)
    emitter.ins('move.w','#0xffff,0x80cc:w',6)
    emitter.ins('move.w','#0xffff,0x80ce:w',6)
    emitter.ins('move.w','#0xffff,0x80d0:w',6)
    emitter.ins('moveq','#1,%d0',2)
    emitter.ins('jsr','main_pc_03aa20:l',6)
    emitter.ins('clr.b','0xf32b:w',4)
    emitter.ins('move.w','#0x300,0xf612:w',6)
    emitter.ins('cmpi.w','#0x10,0xf600:w',6)
    emitter.ins('beq.w','main_pc_003944',4)
    emitter.ins('move.b','#0x81,%d0',4)
    emitter.ins('jsr','main_pc_00808a:l',6)
    emitter.ins('move.w','#0x3,0xf32c:w',6)
    emitter.ins('move.w','0xf32c:w,%d2',4)
    emitter.ins('bsr.w','main_pc_003a00',4)
    emitter.ins('move.w','#0x4,0xf608:w',6)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('rts','',2)

def _lower_return_title_idle_slot(emitter,rules):
    emitter.segment(0x3e8,0x3ec)
    emitter.ins('bra.w','main_pc_003958',4)
    emitter.segment(0x3958,0x395a)
    emitter.ins('rts','',2)

def _lower_initialize_secondary_title_scene(emitter,rules):
    emitter.segment(0x3ec,0x3f0)
    emitter.ins('bra.w','main_pc_003b64',4)
    emitter.segment(0x3b64,0x3bf6)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.w','0xf606:w,%d0',4)
    emitter.ins('andi.b','#0xbf,%d0',4)
    emitter.ins('move.w','%d0,0xc00004:l',6)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('move.w','%d0,0xf312:w',4)
    emitter.ins('move.w','%d0,0xf314:w',4)
    emitter.ins('move.w','%d0,0xf316:w',4)
    emitter.ins('move.w','%d0,0xf318:w',4)
    emitter.ins('jsr','main_pc_0068ce:l',6)
    emitter.ins('move.w','#0x8230,0xc00004:l',8)
    emitter.ins('move.w','#0x8338,0xc00004:l',8)
    emitter.ins('move.w','#0x8406,0xc00004:l',8)
    emitter.ins('move.w','#0x855c,0xc00004:l',8)
    emitter.ins('moveq','#4,%d0',2)
    emitter.ins('jsr','main_pc_008112:l',6)
    emitter.ins('jsr','main_pc_0353fc:l',6)
    emitter.ins('move.w','#0xc17c,0xf33e:w',6)
    emitter.ins('move.w','#0xc17c,0xf340:w',6)
    emitter.ins('move.w','#0x1,0xf33c:w',6)
    emitter.ins('clr.w','0xf342:w',4)
    emitter.ins('clr.w','0xf344:w',4)
    emitter.ins('move.w','#0xfe10,0xf346:w',6)
    emitter.ins('clr.w','0xf32e:w',4)
    emitter.ins('clr.b','0xf32b:w',4)
    emitter.ins('move.w','#0x4,0xf608:w',6)
    emitter.ins('move.w','#0x303,0xf612:w',6)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('rts','',2)

def _lower_initialize_title_transition_scene(emitter,rules):
    emitter.segment(0x3f0,0x3f4)
    emitter.ins('bra.w','main_pc_003bf6',4)
    emitter.segment(0x3bf6,0x3c66)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.w','0xf606:w,%d0',4)
    emitter.ins('andi.b','#0xbf,%d0',4)
    emitter.ins('move.w','%d0,0xc00004:l',6)
    emitter.ins('jsr','main_pc_0068ce:l',6)
    emitter.ins('move.w','#0x8230,0xc00004:l',8)
    emitter.ins('move.w','#0x8338,0xc00004:l',8)
    emitter.ins('move.w','#0x8406,0xc00004:l',8)
    emitter.ins('move.w','#0x855c,0xc00004:l',8)
    emitter.ins('jsr','main_pc_0355da:l',6)
    emitter.ins('addq.w','#0x1,0xf348:w',4)
    emitter.ins('clr.w','0xf316:w',4)
    emitter.ins('move.w','#0xf,%d0',4)
    emitter.ins('lea.l','0xfb00:w,%a0',4)
    emitter.ins('clr.l','(%a0)+',2)
    emitter.ins('dbra','%d0,main_pc_003c44',4)
    emitter.ins('addq.w','#0x1,0xf31e:w',4)
    emitter.ins('addq.w','#0x1,0xf34c:w',4)
    emitter.ins('clr.w','0xf32e:w',4)
    emitter.ins('clr.b','0xf32b:w',4)
    emitter.ins('move.w','#0x4,0xf608:w',6)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('rts','',2)

def _lower_upload_title_emblem_set(emitter,rules):
    emitter.segment(0x3a00,0x3a3e)
    emitter.ins('movem.l','%d0-%d3/%d5/%a0-%a2,-(%a7)',4)
    emitter.ins('lea.l','56(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','#0x300,%d3',4)
    emitter.ins('move.w','#0x6,%d5',4)
    emitter.ins('movea.l','(%a0)+,%a1',2)
    emitter.ins('lea.l','0xd100:w,%a2',4)
    emitter.ins('move.w','#0x20,%d0',4)
    emitter.ins('move.w','#0x20,%d1',4)
    emitter.ins('jsr','56(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('lea.l','0xd100:w,%a2',4)
    emitter.ins('jsr','214(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('addi.w','#0x10,%d3',4)
    emitter.ins('dbra','%d5,main_pc_003a12',4)
    emitter.ins('movem.l','(%a7)+,%d0-%d3/%d5/%a0-%a2',4)
    emitter.ins('rts','',2)

def _lower_scale_title_bitmap_to_tiles(emitter,rules):
    emitter.segment(0x3a5a,0x3aa2)
    emitter.ins('movem.l','%d0-%d7/%a0-%a6,-(%a7)',4)
    emitter.ins('moveq','#0,%d3',2)
    emitter.ins('move.w','%d1,%d3',2)
    emitter.ins('lsl.w','#0x8,%d3',2)
    emitter.ins('divu.w','%d2,%d3',2)
    emitter.ins('andi.l','#0xffff,%d3',6)
    emitter.ins('lsl.l','#0x8,%d3',2)
    emitter.ins('move.w','%d0,%d2',2)
    emitter.ins('moveq','#0,%d4',2)
    emitter.ins('move.w','%d1,%d5',2)
    emitter.ins('moveq','#0,%d6',2)
    emitter.ins('movea.l','%a2,%a3',2)
    emitter.ins('bsr.w','main_pc_003aa2',4)
    emitter.ins('movem.l','%d0/%d2,-(%a7)',4)
    emitter.ins('bsr.w','main_pc_003ac0',4)
    emitter.ins('subq.w','#0x8,%d5',2)
    emitter.ins('bls.b','main_pc_003a8e',2)
    emitter.ins('lea.l','0x80(%a3),%a3',4)
    emitter.ins('bra.b','main_pc_003a80',2)
    emitter.ins('movem.l','(%a7)+,%d0/%d2',4)
    emitter.ins('add.l','%d3,%d4',2)
    emitter.ins('subq.w','#0x1,%d2',2)
    emitter.ins('beq.b','main_pc_003a9c',2)
    emitter.ins('addq.w','#0x4,%a2',2)
    emitter.ins('bra.b','main_pc_003a72',2)
    emitter.ins('movem.l','(%a7)+,%d0-%d7/%a0-%a6',4)
    emitter.ins('rts','',2)

def _lower_select_title_bitmap_scanline(emitter,rules):
    emitter.segment(0x3aa2,0x3ac0)
    emitter.ins('move.w','%d1,%d7',2)
    emitter.ins('lsr.w','#0x3,%d7',2)
    emitter.ins('swap','%d4',2)
    emitter.ins('cmp.w','%d0,%d4',2)
    emitter.ins('bcc.b','main_pc_003ab6',2)
    emitter.ins('mulu.w','%d4,%d7',2)
    emitter.ins('swap','%d4',2)
    emitter.ins('lea.l','(%a1, %d7.w),%a4',4)
    emitter.ins('rts','',2)
    emitter.ins('movea.l','#0xffffffff,%a4',6)
    emitter.ins('swap','%d4',2)
    emitter.ins('rts','',2)

def _lower_pack_title_bitmap_tile_row(emitter,rules):
    emitter.segment(0x3ac0,0x3b02)
    emitter.ins('move.l','%a4,%d0',2)
    emitter.ins('bpl.b','main_pc_003ac8',2)
    emitter.ins('moveq','#0,%d7',2)
    emitter.ins('bra.b','main_pc_003afe',2)
    emitter.ins('move.l','%d5,-(%a7)',2)
    emitter.ins('move.w','#0x7,%d0',4)
    emitter.ins('lsl.l','#0x4,%d7',2)
    emitter.ins('swap','%d6',2)
    emitter.ins('cmp.w','%d1,%d6',2)
    emitter.ins('bcs.b','main_pc_003ada',2)
    emitter.ins('clr.b','%d5',2)
    emitter.ins('bra.b','main_pc_003af4',2)
    emitter.ins('move.w','%d0,-(%a7)',2)
    emitter.ins('move.w','%d6,%d5',2)
    emitter.ins('lsr.w','#0x3,%d5',2)
    emitter.ins('move.b','(%a4, %d5.w),%d5',4)
    emitter.ins('move.w','%d6,%d0',2)
    emitter.ins('andi.w','#0x7,%d0',4)
    emitter.ins('btst.l','%d0,%d5',2)
    emitter.ins('beq.b','main_pc_003af2',2)
    emitter.ins('ori.w','#0xf,%d7',4)
    emitter.ins('move.w','(%a7)+,%d0',2)
    emitter.ins('swap','%d6',2)
    emitter.ins('add.l','%d3,%d6',2)
    emitter.ins('dbra','%d0,main_pc_003ace',4)
    emitter.ins('move.l','(%a7)+,%d5',2)
    emitter.ins('move.l','%d7,(%a3)',2)
    emitter.ins('rts','',2)

def _lower_upload_title_bitmap_tile_rows(emitter,rules):
    emitter.segment(0x3b02,0x3b34)
    emitter.ins('movem.l','%d3/%d7/%a2,-(%a7)',4)
    emitter.ins('lsl.l','#0x7,%d3',2)
    emitter.ins('andi.l','#0x3ff80,%d3',6)
    emitter.ins('lsr.w','#0x2,%d3',2)
    emitter.ins('ori.w','#0x4000,%d3',4)
    emitter.ins('swap','%d3',2)
    emitter.ins('move.l','%d3,0xc00004:l',6)
    emitter.ins('move.w','#0xff,%d7',4)
    emitter.ins('move.w','(%a2)+,0xc00000:l',6)
    emitter.ins('dbra','%d7,main_pc_003b20',4)
    emitter.ins('clr.w','0xd100:w',4)
    emitter.ins('movem.l','(%a7)+,%d3/%d7/%a2',4)
    emitter.ins('rts','',2)

LOWERERS={
    'initialize_title_scene':_lower_initialize_title_scene,
    'return_title_idle_slot':_lower_return_title_idle_slot,
    'initialize_secondary_title_scene':_lower_initialize_secondary_title_scene,
    'initialize_title_transition_scene':_lower_initialize_title_transition_scene,
    'upload_title_emblem_set':_lower_upload_title_emblem_set,
    'scale_title_bitmap_to_tiles':_lower_scale_title_bitmap_to_tiles,
    'select_title_bitmap_scanline':_lower_select_title_bitmap_scanline,
    'pack_title_bitmap_tile_row':_lower_pack_title_bitmap_tile_row,
    'upload_title_bitmap_tile_rows':_lower_upload_title_bitmap_tile_rows,
}

def compile_source(source):
    records=semantic_functions(source,DECLARATIONS,APPROVED)
    sole_title_fields={name:records[name]['effects'] for name in ('_title_frame_fields', '_title_write_fields', '_title_shift_word_fields', '_title_dbra_fields', '_title_child_fields', '_begin_title_transfer_fields', 'initialize_title_scene_fields', 'initialize_title_scene_preserving_mode_fields', 'return_title_idle_slot_fields', 'initialize_secondary_title_scene_fields', '_title_increment_word_fields', 'initialize_title_transition_scene_fields', 'upload_title_emblem_set_fields', 'scale_title_bitmap_to_tiles_fields', 'select_title_bitmap_scanline_fields', 'pack_title_bitmap_tile_row_fields', 'upload_title_bitmap_tile_rows_fields')}
    for owner in ('initialize_title_scene', 'return_title_idle_slot', 'initialize_secondary_title_scene', 'initialize_title_transition_scene', 'upload_title_emblem_set', 'scale_title_bitmap_to_tiles', 'select_title_bitmap_scanline', 'pack_title_bitmap_tile_row', 'upload_title_bitmap_tile_rows'):
        records[owner]['effects']=dict(historical_projection=records[owner]['effects'],actual_complete_fields=sole_title_fields)
    return lower_declared(records,BUSINESS_TITLE_BINDINGS,LOWERERS)

# B51: full actual bodies, not old scalar shape fallback.
DECLARATIONS.update({'_begin_title_transfer': {'signature': 'state, reset_scroll', 'returns': '', 'flow': 'entered = _title_frame_fields(state, FirstDeploymentFrame.unobserved(), 14226)\nreturn _begin_title_transfer_fields(state, entered, reset_scroll, 14268)'}, '_begin_title_transfer_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, reset_scroll: bool, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': "if type(reset_scroll) is not bool:\n    raise ValueError('actual title scroll-reset branch required')\nstate.set_status_word(9984)\nframe = first_replace(frame, status=0)\nframe = _movement_move(state, frame, 'target_x', state.read(4294964742, 2), 16)\nframe = _movement_move(state, frame, 'target_x', low8(frame.target_x) & 191, 8)\nframe = _title_write_fields(state, frame, 12582916, low16(frame.target_x))\nif reset_scroll:\n    frame = _movement_move(state, frame, 'target_x', 0, 16)\n    for address in (4294963986, 4294963988, 4294963990, 4294963992):\n        frame = _title_write_fields(state, frame, address, low16(frame.target_x))\nreturn _title_child_fields(state, frame, 26830, continuation)"}, '_title_child_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = first_replace(frame, stack_cursor=stack)\nif target == 14938:\n    result = scale_title_bitmap_to_tiles_fields(state, entered)\nelif target == 15010:\n    result = select_title_bitmap_scanline_fields(state, entered)\nelif target == 15040:\n    result = pack_title_bitmap_tile_row_fields(state, entered)\nelif target == 15106:\n    result = upload_title_bitmap_tile_rows_fields(state, entered)\nelif target == 14848:\n    result = upload_title_emblem_set_fields(state, entered)\nelif target == 26830:\n    from ..high_level_gameplay_flow.business_services import clear_video_sprite_plane_fields\n    result = clear_video_sprite_plane_fields(SceneRefreshMemory(state), entered)\nelif target == 26662:\n    from ..high_level_gameplay_flow.business_services import initialize_video_registers_and_planes_fields\n    result = initialize_video_registers_and_planes_fields(SceneRefreshMemory(state), entered)\nelif target == 240466:\n    from ..high_level_scene_flows.business_scene import write_vdp_swapped_byte_rle_stream_fields\n    result = write_vdp_swapped_byte_rle_stream_fields(SceneRefreshMemory(state), entered)\nelif target == 240334:\n    from ..high_level_scene_flows.business_scene import read_vdp_plane_rle_rows_fields\n    result = read_vdp_plane_rle_rows_fields(SceneRefreshMemory(state), entered)\nelif target == 240532:\n    from ..high_level_scene_flows.business_scene import copy_scene_palette_variant_fields\n    result = copy_scene_palette_variant_fields(SceneRefreshMemory(state), entered)\nelif target == 240266:\n    from ..high_level_scene_flows.business_scene import snapshot_and_clear_scene_palette_fields\n    result = snapshot_and_clear_scene_palette_fields(SceneRefreshMemory(state), entered)\nelif target == 240160:\n    from ..high_level_scene_flows.business_scene import begin_scene_palette_darken_fields\n    result = begin_scene_palette_darken_fields(SceneRefreshMemory(state), entered)\nelif target == 32906:\n    from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields\n    result = enqueue_sound_command_fields(SceneRefreshMemory(state), entered)\nelif target == 33042:\n    from ..high_level_gameplay_flow.business_services import copy_video_transfer_descriptor_fields\n    result = copy_video_transfer_descriptor_fields(SceneRefreshMemory(state), entered)\nelif target == 218108:\n    from .business_scene_support import upload_glyph_tile_sequence_fields\n    result = upload_glyph_tile_sequence_fields(state, entered)\nelif target == 218586:\n    from .business_scene_support import initialize_auxiliary_text_panel_fields\n    result = initialize_auxiliary_text_panel_fields(state, entered)\nelse:\n    raise MovementContinuationBoundary(target, entered, 'actual title child/internal entry lacks a complete ABI')\nactual = result.stack_cursor.long()\nif actual != continuation:\n    raise FirstDeploymentReturnBoundary(actual, result, continuation)\nreturn first_replace(result, stack_cursor=result.stack_cursor.advance(4))"}, '_title_dbra_fields': {'signature': 'frame: FirstDeploymentFrame, name: str', 'returns': 'FirstDeploymentFrame', 'flow': 'return first_replace(frame, **{name: replace_word(frame.carrier(name), u16(low16(frame.carrier(name)) - 1))})'}, '_title_frame_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, entry: int', 'returns': 'FirstDeploymentFrame', 'flow': 'from ..high_level_remaining_flows.business_city import _resource_cost_frame\nreturn _resource_cost_frame(state, frame, entry)'}, '_title_increment_word_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, address: int', 'returns': 'FirstDeploymentFrame', 'flow': 'previous = state.read(address, 2)\nframe, value = _movement_binary_flags(state, frame, previous, 1, 16)\nstate.write(address, 2, value)\nreturn frame'}, '_title_shift_word_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, name: str, count: int, right: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': 'from ..high_level_remaining_flows.business_highbank import _position_order_shift\nframe = _position_order_shift(frame, name, count, right)\nstate.sr = state.sr & 65504 | frame.status\nreturn frame'}, '_title_write_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, address: int, value, size: int=2, clear: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory\nfrom ..high_level_gameplay_flow.business_services import _scene_refresh_emit\nif size not in (1, 2, 4) or type(clear) is not bool:\n    raise ValueError('actual title store width required')\nif clear:\n    state.read(address, size)\nreturn _scene_refresh_emit(SceneRefreshMemory(state), frame, address, size, value)"}, 'initialize_secondary_title_scene': {'signature': 'state: SceneState', 'returns': '', 'flow': 'checked_state(state)\nentered = first_replace(FirstDeploymentFrame.unobserved())\nreturned = initialize_secondary_title_scene_fields(state, entered)\nreturn None'}, 'initialize_secondary_title_scene_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _title_frame_fields(state, frame, 1004)\nframe = _begin_title_transfer_fields(state, frame, True, 15246)\nfor command in (33328, 33592, 33798, 34140):\n    frame = _title_write_fields(state, frame, 12582916, command)\nframe = _movement_move_long(state, frame, 'target_x', 4)\nframe = _title_child_fields(state, frame, 33042, 15286)\nframe = _title_child_fields(state, frame, 218108, 15292)\nfor address, value, clear in ((4294964030, 49532, False), (4294964032, 49532, False), (4294964028, 1, False), (4294964034, 0, True), (4294964036, 0, True), (4294964038, 65040, False), (4294964014, 0, True)):\n    frame = _title_write_fields(state, frame, address, value, 2, clear)\nframe = _title_write_fields(state, frame, 4294964011, 0, 1, True)\nframe = _title_write_fields(state, frame, 4294964744, 4)\nframe = _title_write_fields(state, frame, 4294964754, 771)\nstate.set_status_word(9472)\nreturn first_replace(frame, status=0)"}, 'initialize_title_scene': {'signature': 'state: SceneState, literal_marker: Long', 'returns': '', 'flow': 'checked_state(state)\nentered = first_replace(FirstDeploymentFrame.unobserved())\nreturned = initialize_title_scene_fields(state, entered)\nreturn None'}, 'initialize_title_scene_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _title_frame_fields(state, frame, 992)\nframe = _title_write_fields(state, frame, 4294964014, 0, clear=True)\nreturn initialize_title_scene_preserving_mode_fields(state, frame)'}, 'initialize_title_scene_preserving_mode': {'signature': 'state: SceneState, literal_marker: Long', 'returns': '', 'flow': 'checked_state(state)\nentered = first_replace(FirstDeploymentFrame.unobserved())\nreturned = initialize_title_scene_preserving_mode_fields(state, entered)\nreturn None'}, 'initialize_title_scene_preserving_mode_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _title_frame_fields(state, frame, 996)\nframe = _begin_title_transfer_fields(state, frame, True, 14268)\nframe = _title_child_fields(state, frame, 26662, 14274)\nframe = _title_write_fields(state, frame, 12582916, 1610612738, 4)\nframe = first_replace(frame, scratch=state.table_at(12582912))\nframe = _movement_move(state, frame, 'offset_y', 0, 16)\nframe = _movement_move(state, frame, 'choice', 8191, 16)\nwhile True:\n    frame = _title_write_fields(state, frame, frame.scratch.base, low16(frame.offset_y))\n    frame = _title_dbra_fields(frame, 'choice')\n    if low16(frame.choice) == 65535:\n        break\nfor command in (36610, 33328, 33584, 33799, 34140, 34560, 35584, 35969, 36143, 36610, 36881, 37248, 37376):\n    frame = _title_write_fields(state, frame, 12582916, command)\nfor source_address, video_word, continuation in ((382436, 0, 14424), (389431, 8192, 14440), (396908, 16384, 14456), (402767, 32768, 14472), (410432, 40960, 14488)):\n    frame = first_replace(frame, roster=state.table_at(source_address).cursor())\n    frame = _movement_move(state, frame, 'target_x', video_word, 16)\n    frame = _title_child_fields(state, frame, 240466, continuation)\nframe = _title_write_fields(state, frame, 12582916, 36610)\nframe = _title_write_fields(state, frame, 12582916, 1845493761, 4)\nframe = first_replace(frame, roster=state.table_at(866122).cursor())\nframe = _movement_move(state, frame, 'target_x', 1023, 16)\nwhile True:\n    value = frame.roster.long()\n    frame = first_replace(frame, roster=frame.roster.advance(4))\n    frame = _title_write_fields(state, frame, 12582912, value, 4)\n    frame = _title_dbra_fields(frame, 'target_x')\n    if low16(frame.target_x) == 65535:\n        break\nframe = first_replace(frame, roster=state.table_at(415217).cursor(), candidates=state.table_at(57344).cursor())\nframe = _movement_move_long(state, frame, 'offset_x', 128)\nframe = _movement_move(state, frame, 'offset_y', 32, 16)\nframe = _title_child_fields(state, frame, 240310, 14554)\nframe = first_replace(frame, roster=state.table_at(417267).cursor(), candidates=state.table_at(57408).cursor())\nframe = _movement_move_long(state, frame, 'offset_x', 128)\nframe = _title_child_fields(state, frame, 240334, 14578)\nframe = _movement_move_long(state, frame, 'target_x', 17)\nframe = _title_child_fields(state, frame, 240532, 14586)\nframe = _title_child_fields(state, frame, 240266, 14592)\nfor address in (4294934730, 4294934732, 4294934734, 4294934736):\n    frame = _title_write_fields(state, frame, address, 65535)\nframe = _movement_move_long(state, frame, 'target_x', 1)\nframe = _title_child_fields(state, frame, 240160, 14624)\nframe = _title_write_fields(state, frame, 4294964011, 0, 1, True)\nframe = _title_write_fields(state, frame, 4294964754, 768)\nframe = _movement_compare(state, frame, state.read(4294964736, 2), 16, 16)\nif not frame.status & 4:\n    frame = _movement_move(state, frame, 'target_x', 129, 8)\n    frame = _title_child_fields(state, frame, 32906, 14654)\n    frame = _title_write_fields(state, frame, 4294964012, 3)\nframe = _movement_move(state, frame, 'unit', state.read(4294964012, 2), 16)\nframe = _title_child_fields(state, frame, 14848, 14668)\nframe = _title_write_fields(state, frame, 4294964744, 4)\nstate.set_status_word(9472)\nreturn first_replace(frame, status=0)"}, 'initialize_title_transition_scene': {'signature': 'state: SceneState', 'returns': '', 'flow': 'checked_state(state)\nentered = first_replace(FirstDeploymentFrame.unobserved())\nreturned = initialize_title_transition_scene_fields(state, entered)\nreturn None'}, 'initialize_title_transition_scene_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _title_frame_fields(state, frame, 1008)\nframe = _begin_title_transfer_fields(state, frame, False, 15374)\nfor command in (33328, 33592, 33798, 34140):\n    frame = _title_write_fields(state, frame, 12582916, command)\nframe = _title_child_fields(state, frame, 218586, 15412)\nframe = _title_increment_word_fields(state, frame, 4294964040)\nframe = _title_write_fields(state, frame, 4294963990, 0, clear=True)\nframe = _movement_move(state, frame, 'target_x', 15, 16)\nframe = first_replace(frame, roster=state.table_at(4294966016).cursor())\nwhile True:\n    frame = _title_write_fields(state, frame, frame.roster.base, 0, 4, True)\n    frame = first_replace(frame, roster=frame.roster.advance(4))\n    frame = _title_dbra_fields(frame, 'target_x')\n    if low16(frame.target_x) == 65535:\n        break\nframe = _title_increment_word_fields(state, frame, 4294963998)\nframe = _title_increment_word_fields(state, frame, 4294964044)\nframe = _title_write_fields(state, frame, 4294964014, 0, clear=True)\nframe = _title_write_fields(state, frame, 4294964011, 0, 1, True)\nframe = _title_write_fields(state, frame, 4294964744, 4)\nstate.set_status_word(9472)\nreturn first_replace(frame, status=0)"}, 'pack_title_bitmap_tile_row': {'signature': 'state: SceneState, row: BitmapRow, destination: Cursor', 'returns': 'BitmapTileResult', 'flow': 'checked_state(state)\nrow.validate(state)\nchecked_cursor(destination, state)\nentered = first_replace(FirstDeploymentFrame.unobserved(), opponent=row.source, scan=destination, target_y=row.source_width, count=row.step, distance=row.vertical, offset_y=row.horizontal, choice=row.pending, offset_x=row.remaining)\nreturned = pack_title_bitmap_tile_row_fields(state, entered)\nreturn BitmapTileResult(returned.offset_y, returned.choice)'}, 'pack_title_bitmap_tile_row_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_remaining_flows.business_city import _special_action_shift_long\nframe = _title_frame_fields(state, frame, 15040)\nframe = _movement_move_long(state, frame, 'target_x', frame.opponent.base)\nif frame.status & 8:\n    frame = _movement_move_long(state, frame, 'choice', 0)\n    return _title_write_fields(state, frame, frame.scan.base, frame.choice, 4)\nstack = frame.stack_cursor.advance(-4)\nframe = _title_write_fields(state, frame, stack.base, frame.offset_x, 4)\nframe = first_replace(frame, stack_cursor=stack)\nframe = _movement_move(state, frame, 'target_x', 7, 16)\nwhile True:\n    frame = _special_action_shift_long(state, frame, 'choice', 4)\n    frame = _movement_move_long(state, frame, 'offset_y', swap_words(frame.offset_y))\n    frame = _movement_compare(state, frame, low16(frame.offset_y), low16(frame.target_y), 16)\n    if not frame.status & 1:\n        frame = _movement_move(state, frame, 'offset_x', 0, 8)\n    else:\n        stack = frame.stack_cursor.advance(-2)\n        frame = _title_write_fields(state, frame, stack.base, low16(frame.target_x))\n        frame = first_replace(frame, stack_cursor=stack)\n        frame = _movement_move(state, frame, 'offset_x', low16(frame.offset_y), 16)\n        frame = _title_shift_word_fields(state, frame, 'offset_x', 3, True)\n        frame = _movement_move(state, frame, 'offset_x', frame.opponent.byte(low16(frame.offset_x)), 8)\n        frame = _movement_move(state, frame, 'target_x', low16(frame.offset_y), 16)\n        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 7, 16)\n        bit = frame.target_x & 31\n        status = frame.status & 27 | (0 if frame.offset_x & 1 << bit else 4)\n        state.sr = state.sr & 65504 | status\n        frame = first_replace(frame, status=status)\n        if not frame.status & 4:\n            frame = _movement_move(state, frame, 'choice', low16(frame.choice) | 15, 16)\n        restored = frame.stack_cursor.word()\n        frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))\n        frame = _movement_move(state, frame, 'target_x', restored, 16)\n    frame = _movement_move_long(state, frame, 'offset_y', swap_words(frame.offset_y))\n    frame = _movement_arithmetic_long(state, frame, 'offset_y', frame.count)\n    frame = _title_dbra_fields(frame, 'target_x')\n    if low16(frame.target_x) == 65535:\n        break\nrestored = frame.stack_cursor.long()\nframe = first_replace(frame, stack_cursor=frame.stack_cursor.advance(4))\nframe = _movement_move_long(state, frame, 'offset_x', restored)\nreturn _title_write_fields(state, frame, frame.scan.base, frame.choice, 4)"}, 'return_title_idle_slot': {'signature': 'state: SceneState', 'returns': '', 'flow': 'checked_state(state)\nentered = first_replace(FirstDeploymentFrame.unobserved())\nreturned = return_title_idle_slot_fields(state, entered)\nreturn None'}, 'return_title_idle_slot_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "checked_state(state)\nif type(frame) is not FirstDeploymentFrame:\n    raise ValueError('actual title fields required')\nreturn frame.validate(state, False)"}, 'scale_title_bitmap_to_tiles': {'signature': 'state: SceneState, source: Table, destination: Cursor, source_height: Word, source_width: Word, output_height: Word', 'returns': '', 'flow': 'checked_state(state)\nchecked_table(source, state)\nchecked_cursor(destination, state)\nentered = first_replace(FirstDeploymentFrame.unobserved(), candidates=source.cursor(), controller=state.table_at(destination.base), target_x=source_height, target_y=source_width, unit=output_height)\nreturned = scale_title_bitmap_to_tiles_fields(state, entered)\nreturn None'}, 'scale_title_bitmap_to_tiles_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _title_frame_fields(state, frame, 14938)\nsaved = ('target_x', 'target_y', 'unit', 'count', 'distance', 'offset_x', 'offset_y', 'choice', 'roster', 'candidates', 'controller', 'scan', 'opponent', 'scratch', 'auxiliary')\nframe = _movement_save_longs(state, frame, saved)\nframe = _movement_move_long(state, frame, 'count', 0)\nframe = _movement_move(state, frame, 'count', low16(frame.target_y), 16)\nframe = _title_shift_word_fields(state, frame, 'count', 8)\nframe = _movement_divu_word(state, frame, 'count', low16(frame.unit), 14948)\nframe = _movement_move_long(state, frame, 'count', frame.count & 65535)\nframe = _movement_shift_long(state, frame, 'count')\nframe = _movement_move(state, frame, 'unit', low16(frame.target_x), 16)\nframe = _movement_move_long(state, frame, 'distance', 0)\nwhile True:\n    frame = _movement_move(state, frame, 'offset_x', low16(frame.target_y), 16)\n    frame = _movement_move_long(state, frame, 'offset_y', 0)\n    frame = first_replace(frame, scan=state.table_at(frame.controller.base).cursor())\n    frame = _title_child_fields(state, frame, 15010, 14972)\n    frame = _movement_save_longs(state, frame, ('target_x', 'unit'))\n    while True:\n        frame = _title_child_fields(state, frame, 15040, 14980)\n        frame, value = _movement_binary_flags(state, frame, low16(frame.offset_x), 8, 16, True)\n        frame = first_replace(frame, offset_x=replace_word(frame.offset_x, value))\n        if frame.status & 5:\n            break\n        frame = first_replace(frame, scan=frame.scan.advance(128))\n    frame = _movement_restore_longs(state, frame, ('target_x', 'unit'))\n    frame = _movement_arithmetic_long(state, frame, 'distance', frame.count)\n    frame, value = _movement_binary_flags(state, frame, low16(frame.unit), 1, 16, True)\n    frame = first_replace(frame, unit=replace_word(frame.unit, value))\n    if frame.status & 4:\n        return _movement_restore_longs(state, frame, saved)\n    frame = first_replace(frame, controller=frame.controller.advance(4))"}, 'select_title_bitmap_scanline': {'signature': 'state: SceneState, source: Table, source_height: Word, source_width: Word, vertical: Long', 'returns': 'Table | None', 'flow': 'checked_state(state)\nchecked_table(source, state)\nentered = first_replace(FirstDeploymentFrame.unobserved(), candidates=source.cursor(), target_x=source_height, target_y=source_width, distance=vertical)\nreturned = select_title_bitmap_scanline_fields(state, entered)\nreturn None if returned.opponent.base & 2147483648 else returned.opponent'}, 'select_title_bitmap_scanline_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _title_frame_fields(state, frame, 15010)\nframe = _movement_move(state, frame, 'choice', low16(frame.target_y), 16)\nframe = _title_shift_word_fields(state, frame, 'choice', 3, True)\nframe = _movement_move_long(state, frame, 'distance', swap_words(frame.distance))\nframe = _movement_compare(state, frame, low16(frame.distance), low16(frame.target_x), 16)\nif not frame.status & 1:\n    frame = first_replace(frame, opponent=state.table_at(4294967295))\n    return _movement_move_long(state, frame, 'distance', swap_words(frame.distance))\nframe = _movement_multiply_word(state, frame, 'choice', low16(frame.distance))\nframe = _movement_move_long(state, frame, 'distance', swap_words(frame.distance))\nreturn first_replace(frame, opponent=state.table_at(u32(frame.candidates.base + s16(low16(frame.choice)))))"}, 'upload_title_bitmap_tile_rows': {'signature': 'state: SceneState, source: Cursor, tile: Long', 'returns': '', 'flow': 'checked_state(state)\nchecked_cursor(source, state)\nentered = first_replace(FirstDeploymentFrame.unobserved(), controller=source, count=tile)\nreturned = upload_title_bitmap_tile_rows_fields(state, entered)\nreturn None'}, 'upload_title_bitmap_tile_rows_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory\nfrom ..high_level_scene_flows.business_scene import _glyph_shift_long_fields\nframe = _title_frame_fields(state, frame, 15106)\nsaved = ('count', 'choice', 'controller')\nframe = _movement_save_longs(state, frame, saved)\nframe = _glyph_shift_long_fields(SceneRefreshMemory(state), frame, 'count', 7)\nframe = _movement_move_long(state, frame, 'count', frame.count & 262016)\nframe = _title_shift_word_fields(state, frame, 'count', 2, True)\nframe = _movement_move(state, frame, 'count', low16(frame.count) | 16384, 16)\nframe = _movement_move_long(state, frame, 'count', swap_words(frame.count))\nframe = _title_write_fields(state, frame, 12582916, frame.count, 4)\nframe = _movement_move(state, frame, 'choice', 255, 16)\nwhile True:\n    value = frame.controller.word()\n    frame = first_replace(frame, controller=frame.controller.advance(2))\n    frame = _title_write_fields(state, frame, 12582912, value)\n    frame = _title_dbra_fields(frame, 'choice')\n    if low16(frame.choice) == 65535:\n        break\nframe = _title_write_fields(state, frame, 4294955264, 0, clear=True)\nreturn _movement_restore_longs(state, frame, saved)"}, 'upload_title_emblem_set': {'signature': 'state: SceneState, scale: Word', 'returns': '', 'flow': 'checked_state(state)\nentered = first_replace(FirstDeploymentFrame.unobserved(), unit=scale)\nreturned = upload_title_emblem_set_fields(state, entered)\nreturn None'}, 'upload_title_emblem_set_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _title_frame_fields(state, frame, 14848)\nsaved = ('target_x', 'target_y', 'unit', 'count', 'offset_x', 'roster', 'candidates', 'controller')\nframe = _movement_save_longs(state, frame, saved)\nframe = first_replace(frame, roster=state.table_at(14910).cursor())\nframe = _movement_move(state, frame, 'count', 768, 16)\nframe = _movement_move(state, frame, 'offset_x', 6, 16)\nwhile True:\n    pointer = frame.roster.long()\n    frame = first_replace(frame, candidates=state.table_at(pointer).cursor(), roster=frame.roster.advance(4), controller=state.table_at(4294955264))\n    frame = _movement_move(state, frame, 'target_x', 32, 16)\n    frame = _movement_move(state, frame, 'target_y', 32, 16)\n    frame = _title_child_fields(state, frame, 14938, 14884)\n    frame = first_replace(frame, controller=state.table_at(4294955264))\n    frame = _title_child_fields(state, frame, 15106, 14894)\n    frame = _movement_add_word(state, frame, 'count', 16)\n    frame = _title_dbra_fields(frame, 'offset_x')\n    if low16(frame.offset_x) == 65535:\n        return _movement_restore_longs(state, frame, saved)"}})

APPROVED.setdefault('business_movement_support',set()).update(('_movement_add_word', '_movement_arithmetic_long', '_movement_binary_flags', '_movement_compare', '_movement_divu_word', '_movement_move', '_movement_move_long', '_movement_multiply_word', '_movement_restore_longs', '_movement_save_longs', '_movement_shift_long', '_movement_test', '_movement_test_long'))

APPROVED.setdefault('business_scene_support',set()).update(('initialize_auxiliary_text_panel_fields', 'upload_glyph_tile_sequence_fields'))

APPROVED.setdefault('contexts_gameplay',set()).update(('FirstDeploymentFrame', 'FirstDeploymentReturnBoundary', 'MovementContinuationBoundary', 'first_replace'))

APPROVED.setdefault('domain',set()).update(('low8',))

APPROVED.setdefault((2, 'high_level_gameplay_flow.business_services'),set()).update(('_scene_refresh_emit', 'clear_video_sprite_plane_fields', 'copy_video_transfer_descriptor_fields', 'enqueue_sound_command_fields', 'initialize_video_registers_and_planes_fields'))

APPROVED.setdefault((2, 'high_level_gameplay_flow.contexts_services'),set()).update(('SceneRefreshMemory',))

APPROVED.setdefault((2, 'high_level_remaining_flows.business_city'),set()).update(('_resource_cost_frame', '_special_action_shift_long'))

APPROVED.setdefault((2, 'high_level_remaining_flows.business_highbank'),set()).update(('_position_order_shift',))

APPROVED.setdefault((2, 'high_level_scene_flows.business_scene'),set()).update(('_glyph_shift_long_fields', 'begin_scene_palette_darken_fields', 'copy_scene_palette_variant_fields', 'read_vdp_plane_rle_rows_fields', 'snapshot_and_clear_scene_palette_fields', 'write_vdp_swapped_byte_rle_stream_fields'))


# Source140: one literal-plane internal entry, original physical owners unchanged.
DECLARATIONS.update({'_title_child_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = first_replace(frame, stack_cursor=stack)\nif target == 14938:\n    result = scale_title_bitmap_to_tiles_fields(state, entered)\nelif target == 15010:\n    result = select_title_bitmap_scanline_fields(state, entered)\nelif target == 15040:\n    result = pack_title_bitmap_tile_row_fields(state, entered)\nelif target == 15106:\n    result = upload_title_bitmap_tile_rows_fields(state, entered)\nelif target == 14848:\n    result = upload_title_emblem_set_fields(state, entered)\nelif target == 26830:\n    from ..high_level_gameplay_flow.business_services import clear_video_sprite_plane_fields\n    result = clear_video_sprite_plane_fields(SceneRefreshMemory(state), entered)\nelif target == 26662:\n    from ..high_level_gameplay_flow.business_services import initialize_video_registers_and_planes_fields\n    result = initialize_video_registers_and_planes_fields(SceneRefreshMemory(state), entered)\nelif target == 240466:\n    from ..high_level_scene_flows.business_scene import write_vdp_swapped_byte_rle_stream_fields\n    result = write_vdp_swapped_byte_rle_stream_fields(SceneRefreshMemory(state), entered)\nelif target == 240310:\n    from .business_scene_support import decode_unmasked_literal_plane_fields\n    result = decode_unmasked_literal_plane_fields(state, entered)\nelif target == 240334:\n    from ..high_level_scene_flows.business_scene import read_vdp_plane_rle_rows_fields\n    result = read_vdp_plane_rle_rows_fields(SceneRefreshMemory(state), entered)\nelif target == 240532:\n    from ..high_level_scene_flows.business_scene import copy_scene_palette_variant_fields\n    result = copy_scene_palette_variant_fields(SceneRefreshMemory(state), entered)\nelif target == 240266:\n    from ..high_level_scene_flows.business_scene import snapshot_and_clear_scene_palette_fields\n    result = snapshot_and_clear_scene_palette_fields(SceneRefreshMemory(state), entered)\nelif target == 240160:\n    from ..high_level_scene_flows.business_scene import begin_scene_palette_darken_fields\n    result = begin_scene_palette_darken_fields(SceneRefreshMemory(state), entered)\nelif target == 32906:\n    from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields\n    result = enqueue_sound_command_fields(SceneRefreshMemory(state), entered)\nelif target == 33042:\n    from ..high_level_gameplay_flow.business_services import copy_video_transfer_descriptor_fields\n    result = copy_video_transfer_descriptor_fields(SceneRefreshMemory(state), entered)\nelif target == 218108:\n    from .business_scene_support import upload_glyph_tile_sequence_fields\n    result = upload_glyph_tile_sequence_fields(state, entered)\nelif target == 218586:\n    from .business_scene_support import initialize_auxiliary_text_panel_fields\n    result = initialize_auxiliary_text_panel_fields(state, entered)\nelse:\n    raise MovementContinuationBoundary(target, entered, 'actual title child/internal entry lacks a complete ABI')\nactual = result.stack_cursor.long()\nif actual != continuation:\n    raise FirstDeploymentReturnBoundary(actual, result, continuation)\nreturn first_replace(result, stack_cursor=result.stack_cursor.advance(4))"}})
APPROVED.setdefault('business_scene_support', set()).update(('decode_unmasked_literal_plane_fields',))
