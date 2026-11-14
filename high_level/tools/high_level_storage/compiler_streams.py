"""Restricted streams source admission and ordinary storage target emission.

No original ROM/ASM/object or bytecode payload is a generation input.
Supported structural source only, not independent behavior acceptance.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import STREAMS_BINDINGS

APPROVED = {'business_load': {'refresh_loaded_group_attributes'},
 'contexts_streams': {'FixedFieldReadContext', 'checked_buffer', 'BitWriter', 'BitReader'},
 'domain': {'CarryOutcome',
            'Cursor',
            'Long',
            'StorageState',
            'Table',
            'Word',
            'checked_cursor',
            'checked_state',
            'checked_table',
            'descending_inclusive',
            'low16',
            'low8',
            'replace_byte',
            'replace_word',
            's16',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'}}

DECLARATIONS = {'_shift_long_left': {'signature': 'value, count',
                      'returns': None,
                      'flow': 'return u32(value << (count & 63))'},
 '_shift_word_left': {'signature': 'value, count',
                      'returns': None,
                      'flow': 'return u16(value << (count & 63))'},
 '_rotate_byte_right': {'signature': 'value',
                        'returns': None,
                        'flow': 'return u32(value >> 8 | low8(value) << 24)'},
 '_append_save_byte': {'signature': 'destination, value',
                       'returns': None,
                       'flow': 'destination.append_byte(low8(value))\n'
                               'destination.base = u32(destination.base + 1)'},
 '_next_save_byte': {'signature': 'source',
                     'returns': None,
                     'flow': 'value = source.next_byte()\n'
                             'source.base = u32(source.base + 1)\n'
                             'return value'},
 'append_little_endian_bitfield': {'signature': 'state: StorageState, writer: BitWriter, value: '
                                                'Long, width: Word',
                                   'returns': 'Long',
                                   'flow': 'checked_state(state)\n'
                                           'checked_buffer(writer, BitWriter, state)\n'
                                           'uint(value, 32)\n'
                                           'uint(width, 16)\n'
                                           'value = _shift_long_left(value, writer.bit_count)\n'
                                           'value = replace_word(value, low16(value) | '
                                           'low16(writer.residue))\n'
                                           'writer.bit_count = u16(writer.bit_count + width)\n'
                                           'while writer.bit_count >= 8:\n'
                                           '    _append_save_byte(writer.cursor, value)\n'
                                           '    writer.bit_count = u16(writer.bit_count - 8)\n'
                                           '    value >>= 8\n'
                                           'writer.residue = replace_word(writer.residue, '
                                           'low16(value))\n'
                                           'return value'},
 'write_packed_transport_orders': {'signature': 'state: StorageState, destination: Cursor',
                                   'returns': 'Cursor',
                                   'flow': 'checked_state(state)\n'
                                           'checked_cursor(destination, state)\n'
                                           'source = state.transport_orders.cursor()\n'
                                           'writer = BitWriter(destination)\n'
                                           'value = 0\n'
                                           'for _ in descending_inclusive(39):\n'
                                           '    value = source.next_byte() & 3\n'
                                           '    value = u16(value << 7)\n'
                                           '    value |= source.next_byte() & 127\n'
                                           '    value = u16(value << 7)\n'
                                           '    value |= source.next_byte() & 127\n'
                                           '    value = u32(value << 6)\n'
                                           '    value = replace_word(value, low16(value) | '
                                           'source.next_byte() & 63)\n'
                                           '    value = append_little_endian_bitfield(state, '
                                           'writer, value, 22)\n'
                                           'if writer.bit_count != 0:\n'
                                           '    _append_save_byte(destination, value)\n'
                                           'return destination'},
 '_read_group_long_bytes': {'signature': 'source, carrier',
                            'returns': None,
                            'flow': 'carrier = replace_byte(carrier, source.next_byte())\n'
                                    'carrier = replace_word(carrier, u16(low16(carrier) << 8))\n'
                                    'carrier = replace_byte(carrier, source.next_byte())\n'
                                    'carrier = u32(carrier << 8)\n'
                                    'carrier = replace_byte(carrier, source.next_byte())\n'
                                    'carrier = u32(carrier << 8)\n'
                                    'return replace_byte(carrier, source.next_byte())'},
 'write_packed_group_stream': {'signature': 'state: StorageState, destination: Cursor',
                               'returns': 'Cursor',
                               'flow': 'checked_state(state)\n'
                                       'checked_cursor(destination, state)\n'
                                       'source = state.packed_groups.cursor()\n'
                                       'writer = BitWriter(destination)\n'
                                       'carrier = 0\n'
                                       'while True:\n'
                                       '    carrier = replace_byte(carrier, source.next_byte()) & '
                                       '15\n'
                                       '    count = low16(carrier)\n'
                                       '    carrier = append_little_endian_bitfield(state, writer, '
                                       'carrier, 4)\n'
                                       '    if count == 0:\n'
                                       '        break\n'
                                       '    carrier = replace_byte(carrier, source.next_byte()) & '
                                       '127\n'
                                       '    carrier = append_little_endian_bitfield(state, writer, '
                                       'carrier, 7)\n'
                                       '    carrier = replace_byte(carrier, source.next_byte()) & '
                                       '127\n'
                                       '    carrier = append_little_endian_bitfield(state, writer, '
                                       'carrier, 7)\n'
                                       '    source.base = u32(source.base + 1)\n'
                                       '    carrier = replace_byte(carrier, source.next_byte())\n'
                                       '    carrier = append_little_endian_bitfield(state, writer, '
                                       'carrier, 4)\n'
                                       '    carrier = _read_group_long_bytes(source, carrier)\n'
                                       '    carrier = append_little_endian_bitfield(state, writer, '
                                       'carrier, 18)\n'
                                       '    carrier = _read_group_long_bytes(source, carrier)\n'
                                       '    carrier = append_little_endian_bitfield(state, writer, '
                                       'carrier, 20)\n'
                                       '    for _ in descending_inclusive(u16(count - 1)):\n'
                                       '        carrier = replace_byte(carrier, '
                                       'source.next_byte()) & 255\n'
                                       '        carrier = append_little_endian_bitfield(state, '
                                       'writer, carrier, 8)\n'
                                       '_append_save_byte(destination, writer.residue)\n'
                                       'return destination'},
 'checksum_saved_payload': {'signature': 'state: StorageState',
                            'returns': 'Long',
                            'flow': 'checked_state(state)\n'
                                    'source = state.saved_payload.cursor()\n'
                                    'total = 0\n'
                                    'for _ in descending_inclusive(7916):\n'
                                    '    total = u32(total + _next_save_byte(source))\n'
                                    'return total'},
 'write_saved_state_checksum': {'signature': 'state: StorageState',
                                'returns': 'Long',
                                'flow': 'checked_state(state)\n'
                                        'carrier = checksum_saved_payload(state)\n'
                                        'state.saved_checksum.set_byte(0, low8(carrier))\n'
                                        'carrier >>= 8\n'
                                        'state.saved_checksum.set_byte(0, low8(carrier), 2)\n'
                                        'carrier >>= 8\n'
                                        'state.saved_checksum.set_byte(0, low8(carrier), 4)\n'
                                        'carrier = replace_word(carrier, low16(carrier) >> 8)\n'
                                        'state.saved_checksum.set_byte(0, low8(carrier), 6)\n'
                                        'return carrier'},
 'read_buffered_low_word_bitfield': {'signature': 'state: StorageState, reader: BitReader, width: '
                                                  'Word, mask: Word',
                                     'returns': 'Word',
                                     'flow': 'checked_state(state)\n'
                                             'checked_buffer(reader, BitReader, state)\n'
                                             'uint(width, 16)\n'
                                             'uint(mask, 16)\n'
                                             'if reader.bit_count < width:\n'
                                             '    incoming = _next_save_byte(reader.cursor)\n'
                                             '    incoming = _shift_word_left(incoming, '
                                             'reader.bit_count)\n'
                                             '    reader.residue = replace_word(reader.residue, '
                                             'low16(reader.residue) | incoming)\n'
                                             '    reader.bit_count = u16(reader.bit_count + 8)\n'
                                             'value = low16(reader.residue) & mask\n'
                                             'reader.residue = replace_word(reader.residue, '
                                             'low16(reader.residue) >> (width & 63))\n'
                                             'reader.bit_count = u16(reader.bit_count - width)\n'
                                             'return value'},
 'read_packed_transport_orders': {'signature': 'state: StorageState, source: Cursor',
                                  'returns': 'Cursor',
                                  'flow': 'checked_state(state)\n'
                                          'checked_cursor(source, state)\n'
                                          'destination = state.transport_orders.cursor()\n'
                                          'reader = BitReader(source)\n'
                                          'for _ in descending_inclusive(39):\n'
                                          '    destination.set_byte(0, '
                                          'low8(read_buffered_low_word_bitfield(state, reader, 6, '
                                          '63)), 3)\n'
                                          '    destination.set_byte(0, '
                                          'low8(read_buffered_low_word_bitfield(state, reader, 7, '
                                          '127)), 2)\n'
                                          '    destination.set_byte(0, '
                                          'low8(read_buffered_low_word_bitfield(state, reader, 7, '
                                          '127)), 1)\n'
                                          '    destination.set_byte(0, '
                                          'low8(read_buffered_low_word_bitfield(state, reader, 2, '
                                          '3)))\n'
                                          '    destination.base = u32(destination.base + 4)\n'
                                          'return source'},
 'read_buffered_long_bitfield': {'signature': 'state: StorageState, reader: BitReader, width: '
                                              'Word, mask: Long',
                                 'returns': 'Long',
                                 'flow': 'checked_state(state)\n'
                                         'checked_buffer(reader, BitReader, state)\n'
                                         'uint(width, 16)\n'
                                         'uint(mask, 32)\n'
                                         'value = low8(reader.residue)\n'
                                         'while True:\n'
                                         '    value = _rotate_byte_right(value)\n'
                                         '    if reader.bit_count >= width:\n'
                                         '        break\n'
                                         '    value = replace_byte(value, '
                                         '_next_save_byte(reader.cursor))\n'
                                         '    reader.residue = replace_byte(reader.residue, '
                                         'low8(value))\n'
                                         '    reader.bit_count = u16(reader.bit_count + 8)\n'
                                         'shift = u16(32 - reader.bit_count)\n'
                                         'while shift > 8:\n'
                                         '    value >>= 8\n'
                                         '    shift = u16(shift - 8)\n'
                                         'value >>= shift & 63\n'
                                         'value &= mask\n'
                                         'reader.bit_count = u16(reader.bit_count - width)\n'
                                         'return value'},
 '_store_group_long_reverse': {'signature': 'destination, carrier',
                               'returns': None,
                               'flow': 'destination.set_byte(0, low8(carrier), 3)\n'
                                       'carrier >>= 8\n'
                                       'destination.set_byte(0, low8(carrier), 2)\n'
                                       'carrier >>= 8\n'
                                       'destination.set_byte(0, low8(carrier), 1)\n'
                                       'carrier = replace_word(carrier, low16(carrier) >> 8)\n'
                                       'destination.set_byte(0, low8(carrier))\n'
                                       'destination.base = u32(destination.base + 4)'},
 'read_packed_group_stream': {'signature': 'state: StorageState, source: Cursor',
                              'returns': 'Cursor',
                              'flow': 'checked_state(state)\n'
                                      'checked_cursor(source, state)\n'
                                      'destination = state.packed_groups.cursor()\n'
                                      'reader = BitReader(source)\n'
                                      'while True:\n'
                                      '    count = read_buffered_long_bitfield(state, reader, 4, '
                                      '15)\n'
                                      '    destination.append_byte(low8(count))\n'
                                      '    if low8(count) == 0:\n'
                                      '        break\n'
                                      '    '
                                      'destination.append_byte(low8(read_buffered_long_bitfield(state, '
                                      'reader, 7, 127)))\n'
                                      '    '
                                      'destination.append_byte(low8(read_buffered_long_bitfield(state, '
                                      'reader, 7, 127)))\n'
                                      '    destination.base = u32(destination.base + 1)\n'
                                      '    '
                                      'destination.append_byte(low8(read_buffered_long_bitfield(state, '
                                      'reader, 4, 15)))\n'
                                      '    value = read_buffered_long_bitfield(state, reader, 18, '
                                      '262143)\n'
                                      '    _store_group_long_reverse(destination, value)\n'
                                      '    value = read_buffered_long_bitfield(state, reader, 20, '
                                      '1048575)\n'
                                      '    _store_group_long_reverse(destination, value)\n'
                                      '    for _ in descending_inclusive(u16(count - 1)):\n'
                                      '        '
                                      'destination.append_byte(low8(read_buffered_long_bitfield(state, '
                                      'reader, 8, 255)))\n'
                                      'from .business_load import refresh_loaded_group_attributes\n'
                                      'refresh_loaded_group_attributes(state)\n'
                                      'return source'},
 'validate_saved_header_and_checksum': {'signature': 'state: StorageState',
                                        'returns': 'CarryOutcome',
                                        'flow': 'checked_state(state)\n'
                                                'for offset, expected in ((0, 83), (2, 69), (4, '
                                                '71), (6, 65)):\n'
                                                '    if state.saved_header.byte(0, offset) != '
                                                'expected:\n'
                                                '        return state.carry_result(1)\n'
                                                'carrier = checksum_saved_payload(state)\n'
                                                'if low8(carrier) != state.saved_checksum.byte():\n'
                                                '    return state.carry_result(1)\n'
                                                'carrier >>= 8\n'
                                                'if low8(carrier) != state.saved_checksum.byte(0, '
                                                '2):\n'
                                                '    return state.carry_result(1)\n'
                                                'carrier >>= 8\n'
                                                'if low8(carrier) != state.saved_checksum.byte(0, '
                                                '4):\n'
                                                '    return state.carry_result(1)\n'
                                                'carrier = replace_word(carrier, low16(carrier) >> '
                                                '8)\n'
                                                'if low8(carrier) != state.saved_checksum.byte(0, '
                                                '6):\n'
                                                '    return state.carry_result(1)\n'
                                                'return state.carry_result(0)'},
 '_next_fixed_source_value': {'signature': 'source, source_width',
                              'returns': None,
                              'flow': 'remaining = source_width\n'
                                      'value = 0\n'
                                      'while remaining != 0:\n'
                                      '    if remaining == 4:\n'
                                      '        return source.next_long()\n'
                                      '    if remaining >= 2:\n'
                                      '        value = swap_words(value)\n'
                                      '        value = replace_word(value, source.next_word())\n'
                                      '        remaining = u16(remaining - 2)\n'
                                      '        continue\n'
                                      '    value = u32(value << 8)\n'
                                      '    value = replace_byte(value, source.next_byte())\n'
                                      '    break\n'
                                      'return value'},
 'write_masked_fixed_count_fields': {'signature': 'state: StorageState, source: Table, '
                                                  'destination: Cursor, bit_width: Word, '
                                                  'source_width: Word, record_count: Word',
                                     'returns': 'Cursor',
                                     'flow': 'checked_state(state)\n'
                                             'checked_table(source, state)\n'
                                             'checked_cursor(destination, state)\n'
                                             'for value in (bit_width, source_width, '
                                             'record_count):\n'
                                             '    uint(value, 16)\n'
                                             'source = source.cursor()\n'
                                             'mask = state.save_bitwidth_masks.long(u16(bit_width '
                                             '<< 2))\n'
                                             'residue, buffered = (0, 0)\n'
                                             'for _ in descending_inclusive(u16(record_count - '
                                             '1)):\n'
                                             '    value = _next_fixed_source_value(source, '
                                             'source_width) & mask\n'
                                             '    value = _shift_long_left(value, buffered)\n'
                                             '    value = replace_byte(value, low8(value) | '
                                             'low8(residue))\n'
                                             '    buffered = u16(buffered + bit_width)\n'
                                             '    while buffered >= 8:\n'
                                             '        _append_save_byte(destination, value)\n'
                                             '        value >>= 8\n'
                                             '        buffered = u16(buffered - 8)\n'
                                             '    residue = low16(value)\n'
                                             'if residue != 0:\n'
                                             '    source.set_byte(0, low8(residue))\n'
                                             '    source.base = u32(source.base + 2)\n'
                                             'return destination'},
 'read_masked_fixed_count_fields': {'signature': 'state: StorageState, source: Cursor, '
                                                 'destination: Table, bit_width: Word, '
                                                 'destination_width: Word, record_count: Word, *, '
                                                 'retained: FixedFieldReadContext=None',
                                    'returns': 'Cursor',
                                    'flow': 'checked_state(state)\n'
                                            'checked_cursor(source, state)\n'
                                            'checked_table(destination, state)\n'
                                            'for value in (bit_width, destination_width, '
                                            'record_count):\n'
                                            '    uint(value, 16)\n'
                                            'if retained is None:\n'
                                            '    retained = FixedFieldReadContext()\n'
                                            'if type(retained) is not FixedFieldReadContext:\n'
                                            "    raise ValueError('exact fixed-field carrier "
                                            "context required')\n"
                                            'retained.__post_init__()\n'
                                            'destination = destination.cursor()\n'
                                            'mask = state.save_bitwidth_masks.long(u16(bit_width '
                                            '<< 2))\n'
                                            'residue, buffered = (0, 0)\n'
                                            'value = retained.value_carrier\n'
                                            'for _ in descending_inclusive(u16(record_count - '
                                            '1)):\n'
                                            '    value = replace_byte(value, low8(residue))\n'
                                            '    while buffered < bit_width:\n'
                                            '        value = _rotate_byte_right(value)\n'
                                            '        value = replace_byte(value, '
                                            '_next_save_byte(source))\n'
                                            '        buffered = u16(buffered + 8)\n'
                                            '    residue = low16(value)\n'
                                            '    if buffered <= 8:\n'
                                            '        value = replace_word(value, low16(value) >> '
                                            '(u16(8 - buffered) & 63))\n'
                                            '    else:\n'
                                            '        value = _rotate_byte_right(value)\n'
                                            '        shift = u16(32 - buffered)\n'
                                            '        while shift > 8:\n'
                                            '            value >>= 8\n'
                                            '            shift = u16(shift - 8)\n'
                                            '        value >>= shift & 63\n'
                                            '    value &= mask\n'
                                            '    for index in '
                                            'descending_inclusive(u16(destination_width - 1)):\n'
                                            '        destination.set_byte(index, low8(value))\n'
                                            '        value >>= 8\n'
                                            '    destination.base = u32(destination.base + '
                                            's16(destination_width))\n'
                                            '    buffered = u16(buffered - bit_width)\n'
                                            '    retained.value_carrier = value\n'
                                            'return source'}}

def _lower_write_packed_transport_orders(e,rules):
    e.label('storage_pc_0088c6')
    e.ins('lea.l','0xce00:w,%a1',4)
    e.label('storage_pc_0088ca')
    e.ins('clr.w','%d3',2)
    e.label('storage_pc_0088cc')
    e.ins('clr.w','%d4',2)
    e.label('storage_pc_0088ce')
    e.ins('move.w','#0x27,%d0',4)
    e.label('storage_pc_0088d2')
    e.ins('moveq','#0,%d7',2)
    e.label('storage_pc_0088d4')
    e.ins('move.b','(%a1)+,%d7',2)
    e.label('storage_pc_0088d6')
    e.ins('andi.w','#0x3,%d7',4)
    e.label('storage_pc_0088da')
    e.ins('lsl.w','#0x7,%d7',2)
    e.label('storage_pc_0088dc')
    e.ins('move.b','(%a1)+,%d1',2)
    e.label('storage_pc_0088de')
    e.ins('andi.w','#0x7f,%d1',4)
    e.label('storage_pc_0088e2')
    e.ins('or.w','%d1,%d7',2)
    e.label('storage_pc_0088e4')
    e.ins('lsl.w','#0x7,%d7',2)
    e.label('storage_pc_0088e6')
    e.ins('move.b','(%a1)+,%d1',2)
    e.label('storage_pc_0088e8')
    e.ins('andi.w','#0x7f,%d1',4)
    e.label('storage_pc_0088ec')
    e.ins('or.w','%d1,%d7',2)
    e.label('storage_pc_0088ee')
    e.ins('lsl.l','#0x6,%d7',2)
    e.label('storage_pc_0088f0')
    e.ins('move.b','(%a1)+,%d1',2)
    e.label('storage_pc_0088f2')
    e.ins('andi.w','#0x3f,%d1',4)
    e.label('storage_pc_0088f6')
    e.ins('or.w','%d1,%d7',2)
    e.label('storage_pc_0088f8')
    e.ins('lsl.l','%d4,%d7',2)
    e.label('storage_pc_0088fa')
    e.ins('or.w','%d3,%d7',2)
    e.label('storage_pc_0088fc')
    e.ins('addi.w','#0x16,%d4',4)
    e.label('storage_pc_008900')
    e.ins('cmpi.w','#0x8,%d4',4)
    e.label('storage_pc_008904')
    e.ins('bcs.w','storage_pc_008916',4)
    e.label('storage_pc_008908')
    e.ins('move.b','%d7,(%a0)+',2)
    e.label('storage_pc_00890a')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_00890e')
    e.ins('subi.w','#0x8,%d4',4)
    e.label('storage_pc_008912')
    e.ins('lsr.l','#0x8,%d7',2)
    e.label('storage_pc_008914')
    e.ins('bra.b','storage_pc_008900',2)
    e.label('storage_pc_008916')
    e.ins('move.w','%d7,%d3',2)
    e.label('storage_pc_008918')
    e.ins('dbra','%d0,storage_pc_0088d2',4)
    e.label('storage_pc_00891c')
    e.ins('tst.w','%d4',2)
    e.label('storage_pc_00891e')
    e.ins('beq.w','storage_pc_008928',4)
    e.label('storage_pc_008922')
    e.ins('move.b','%d7,(%a0)+',2)
    e.label('storage_pc_008924')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_008928')
    e.ins('rts','',2)

def _lower_write_packed_group_stream(e,rules):
    e.label('storage_pc_008946')
    e.ins('lea.l','0x9000:w,%a1',4)
    e.label('storage_pc_00894a')
    e.ins('moveq','#0,%d3',2)
    e.label('storage_pc_00894c')
    e.ins('clr.w','%d4',2)
    e.label('storage_pc_00894e')
    e.ins('move.b','(%a1)+,%d0',2)
    e.label('storage_pc_008950')
    e.ins('andi.l','#0xf,%d0',6)
    e.label('storage_pc_008956')
    e.ins('move.w','%d0,%d7',2)
    e.label('storage_pc_008958')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_00895c')
    e.ins('bsr.w','storage_pc_0089e0',4)
    e.label('storage_pc_008960')
    e.ins('tst.w','%d7',2)
    e.label('storage_pc_008962')
    e.ins('beq.w','storage_pc_0089d8',4)
    e.label('storage_pc_008966')
    e.ins('move.b','(%a1)+,%d0',2)
    e.label('storage_pc_008968')
    e.ins('andi.l','#0x7f,%d0',6)
    e.label('storage_pc_00896e')
    e.ins('move.w','#0x7,%d1',4)
    e.label('storage_pc_008972')
    e.ins('bsr.w','storage_pc_0089e0',4)
    e.label('storage_pc_008976')
    e.ins('move.b','(%a1)+,%d0',2)
    e.label('storage_pc_008978')
    e.ins('andi.l','#0x7f,%d0',6)
    e.label('storage_pc_00897e')
    e.ins('move.w','#0x7,%d1',4)
    e.label('storage_pc_008982')
    e.ins('bsr.w','storage_pc_0089e0',4)
    e.label('storage_pc_008986')
    e.ins('addq.w','#0x1,%a1',2)
    e.label('storage_pc_008988')
    e.ins('move.b','(%a1)+,%d0',2)
    e.label('storage_pc_00898a')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_00898e')
    e.ins('bsr.w','storage_pc_0089e0',4)
    e.label('storage_pc_008992')
    e.ins('move.b','(%a1)+,%d0',2)
    e.label('storage_pc_008994')
    e.ins('lsl.w','#0x8,%d0',2)
    e.label('storage_pc_008996')
    e.ins('move.b','(%a1)+,%d0',2)
    e.label('storage_pc_008998')
    e.ins('lsl.l','#0x8,%d0',2)
    e.label('storage_pc_00899a')
    e.ins('move.b','(%a1)+,%d0',2)
    e.label('storage_pc_00899c')
    e.ins('lsl.l','#0x8,%d0',2)
    e.label('storage_pc_00899e')
    e.ins('move.b','(%a1)+,%d0',2)
    e.label('storage_pc_0089a0')
    e.ins('move.w','#0x12,%d1',4)
    e.label('storage_pc_0089a4')
    e.ins('bsr.w','storage_pc_0089e0',4)
    e.label('storage_pc_0089a8')
    e.ins('move.b','(%a1)+,%d0',2)
    e.label('storage_pc_0089aa')
    e.ins('lsl.w','#0x8,%d0',2)
    e.label('storage_pc_0089ac')
    e.ins('move.b','(%a1)+,%d0',2)
    e.label('storage_pc_0089ae')
    e.ins('lsl.l','#0x8,%d0',2)
    e.label('storage_pc_0089b0')
    e.ins('move.b','(%a1)+,%d0',2)
    e.label('storage_pc_0089b2')
    e.ins('lsl.l','#0x8,%d0',2)
    e.label('storage_pc_0089b4')
    e.ins('move.b','(%a1)+,%d0',2)
    e.label('storage_pc_0089b6')
    e.ins('move.w','#0x14,%d1',4)
    e.label('storage_pc_0089ba')
    e.ins('bsr.w','storage_pc_0089e0',4)
    e.label('storage_pc_0089be')
    e.ins('subq.w','#0x1,%d7',2)
    e.label('storage_pc_0089c0')
    e.ins('move.b','(%a1)+,%d0',2)
    e.label('storage_pc_0089c2')
    e.ins('andi.l','#0xff,%d0',6)
    e.label('storage_pc_0089c8')
    e.ins('move.w','#0x8,%d1',4)
    e.label('storage_pc_0089cc')
    e.ins('bsr.w','storage_pc_0089e0',4)
    e.label('storage_pc_0089d0')
    e.ins('dbra','%d7,storage_pc_0089c0',4)
    e.label('storage_pc_0089d4')
    e.ins('bra.w','storage_pc_00894e',4)
    e.label('storage_pc_0089d8')
    e.ins('move.b','%d3,(%a0)+',2)
    e.label('storage_pc_0089da')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_0089de')
    e.ins('rts','',2)

def _lower_append_little_endian_bitfield(e,rules):
    e.label('storage_pc_0089e0')
    e.ins('lsl.l','%d4,%d0',2)
    e.label('storage_pc_0089e2')
    e.ins('or.w','%d3,%d0',2)
    e.label('storage_pc_0089e4')
    e.ins('add.w','%d1,%d4',2)
    e.label('storage_pc_0089e6')
    e.ins('cmpi.w','#0x8,%d4',4)
    e.label('storage_pc_0089ea')
    e.ins('bcs.w','storage_pc_0089fa',4)
    e.label('storage_pc_0089ee')
    e.ins('move.b','%d0,(%a0)+',2)
    e.label('storage_pc_0089f0')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_0089f4')
    e.ins('subq.w','#0x8,%d4',2)
    e.label('storage_pc_0089f6')
    e.ins('lsr.l','#0x8,%d0',2)
    e.label('storage_pc_0089f8')
    e.ins('bra.b','storage_pc_0089e6',2)
    e.label('storage_pc_0089fa')
    e.ins('move.w','%d0,%d3',2)
    e.label('storage_pc_0089fc')
    e.ins('rts','',2)

def _lower_write_saved_state_checksum(e,rules):
    e.label('storage_pc_0089fe')
    e.ins('bsr.w','storage_pc_008a22',4)
    e.label('storage_pc_008a02')
    e.ins('move.b','%d1,0x20010d:l',6)
    e.label('storage_pc_008a08')
    e.ins('lsr.l','#0x8,%d1',2)
    e.label('storage_pc_008a0a')
    e.ins('move.b','%d1,0x20010f:l',6)
    e.label('storage_pc_008a10')
    e.ins('lsr.l','#0x8,%d1',2)
    e.label('storage_pc_008a12')
    e.ins('move.b','%d1,0x200111:l',6)
    e.label('storage_pc_008a18')
    e.ins('lsr.w','#0x8,%d1',2)
    e.label('storage_pc_008a1a')
    e.ins('move.b','%d1,0x200113:l',6)
    e.label('storage_pc_008a20')
    e.ins('rts','',2)

def _lower_checksum_saved_payload(e,rules):
    e.label('storage_pc_008a22')
    e.ins('lea.l','0x200115:l,%a0',6)
    e.label('storage_pc_008a28')
    e.ins('move.w','#0x1eec,%d0',4)
    e.label('storage_pc_008a2c')
    e.ins('moveq','#0,%d1',2)
    e.label('storage_pc_008a2e')
    e.ins('moveq','#0,%d2',2)
    e.label('storage_pc_008a30')
    e.ins('move.b','(%a0)+,%d2',2)
    e.label('storage_pc_008a32')
    e.ins('add.l','%d2,%d1',2)
    e.label('storage_pc_008a34')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_008a38')
    e.ins('dbra','%d0,storage_pc_008a30',4)
    e.label('storage_pc_008a3c')
    e.ins('rts','',2)

def _lower_read_packed_transport_orders(e,rules):
    e.label('storage_pc_008fb4')
    e.ins('lea.l','0xce00:w,%a1',4)
    e.label('storage_pc_008fb8')
    e.ins('clr.w','%d3',2)
    e.label('storage_pc_008fba')
    e.ins('clr.w','%d4',2)
    e.label('storage_pc_008fbc')
    e.ins('move.w','#0x27,%d7',4)
    e.label('storage_pc_008fc0')
    e.ins('move.w','#0x6,%d5',4)
    e.label('storage_pc_008fc4')
    e.ins('move.w','#0x3f,%d6',4)
    e.label('storage_pc_008fc8')
    e.ins('bsr.w','storage_pc_008ffe',4)
    e.label('storage_pc_008fcc')
    e.ins('move.b','%d2,0x3(%a1)',4)
    e.label('storage_pc_008fd0')
    e.ins('move.w','#0x7,%d5',4)
    e.label('storage_pc_008fd4')
    e.ins('move.w','#0x7f,%d6',4)
    e.label('storage_pc_008fd8')
    e.ins('bsr.w','storage_pc_008ffe',4)
    e.label('storage_pc_008fdc')
    e.ins('move.b','%d2,0x2(%a1)',4)
    e.label('storage_pc_008fe0')
    e.ins('bsr.w','storage_pc_008ffe',4)
    e.label('storage_pc_008fe4')
    e.ins('move.b','%d2,0x1(%a1)',4)
    e.label('storage_pc_008fe8')
    e.ins('move.w','#0x2,%d5',4)
    e.label('storage_pc_008fec')
    e.ins('move.w','#0x3,%d6',4)
    e.label('storage_pc_008ff0')
    e.ins('bsr.w','storage_pc_008ffe',4)
    e.label('storage_pc_008ff4')
    e.ins('move.b','%d2,(%a1)',2)
    e.label('storage_pc_008ff6')
    e.ins('addq.w','#0x4,%a1',2)
    e.label('storage_pc_008ff8')
    e.ins('dbra','%d7,storage_pc_008fc0',4)
    e.label('storage_pc_008ffc')
    e.ins('rts','',2)

def _lower_read_buffered_low_word_bitfield(e,rules):
    e.label('storage_pc_008ffe')
    e.ins('cmp.w','%d5,%d4',2)
    e.label('storage_pc_009000')
    e.ins('bcc.w','storage_pc_009012',4)
    e.label('storage_pc_009004')
    e.ins('clr.w','%d1',2)
    e.label('storage_pc_009006')
    e.ins('move.b','(%a0)+,%d1',2)
    e.label('storage_pc_009008')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_00900c')
    e.ins('lsl.w','%d4,%d1',2)
    e.label('storage_pc_00900e')
    e.ins('or.w','%d1,%d3',2)
    e.label('storage_pc_009010')
    e.ins('addq.w','#0x8,%d4',2)
    e.label('storage_pc_009012')
    e.ins('move.w','%d3,%d2',2)
    e.label('storage_pc_009014')
    e.ins('and.w','%d6,%d2',2)
    e.label('storage_pc_009016')
    e.ins('lsr.w','%d5,%d3',2)
    e.label('storage_pc_009018')
    e.ins('sub.w','%d5,%d4',2)
    e.label('storage_pc_00901a')
    e.ins('rts','',2)

def _lower_read_packed_group_stream(e,rules):
    e.label('storage_pc_009036')
    e.ins('lea.l','0x9000:w,%a1',4)
    e.label('storage_pc_00903a')
    e.ins('clr.w','%d0',2)
    e.label('storage_pc_00903c')
    e.ins('clr.w','%d1',2)
    e.label('storage_pc_00903e')
    e.ins('move.w','#0x4,%d2',4)
    e.label('storage_pc_009042')
    e.ins('moveq','#15,%d3',2)
    e.label('storage_pc_009044')
    e.ins('bsr.w','storage_pc_0091c4',4)
    e.label('storage_pc_009048')
    e.ins('move.b','%d4,(%a1)+',2)
    e.label('storage_pc_00904a')
    e.ins('beq.w','storage_pc_0090d2',4)
    e.label('storage_pc_00904e')
    e.ins('move.w','%d4,%d7',2)
    e.label('storage_pc_009050')
    e.ins('move.w','#0x7,%d2',4)
    e.label('storage_pc_009054')
    e.ins('moveq','#127,%d3',2)
    e.label('storage_pc_009056')
    e.ins('bsr.w','storage_pc_0091c4',4)
    e.label('storage_pc_00905a')
    e.ins('move.b','%d4,(%a1)+',2)
    e.label('storage_pc_00905c')
    e.ins('bsr.w','storage_pc_0091c4',4)
    e.label('storage_pc_009060')
    e.ins('move.b','%d4,(%a1)+',2)
    e.label('storage_pc_009062')
    e.ins('addq.w','#0x1,%a1',2)
    e.label('storage_pc_009064')
    e.ins('move.w','#0x4,%d2',4)
    e.label('storage_pc_009068')
    e.ins('moveq','#15,%d3',2)
    e.label('storage_pc_00906a')
    e.ins('bsr.w','storage_pc_0091c4',4)
    e.label('storage_pc_00906e')
    e.ins('move.b','%d4,(%a1)+',2)
    e.label('storage_pc_009070')
    e.ins('move.w','#0x12,%d2',4)
    e.label('storage_pc_009074')
    e.ins('move.l','#0x3ffff,%d3',6)
    e.label('storage_pc_00907a')
    e.ins('bsr.w','storage_pc_0091c4',4)
    e.label('storage_pc_00907e')
    e.ins('move.b','%d4,0x3(%a1)',4)
    e.label('storage_pc_009082')
    e.ins('lsr.l','#0x8,%d4',2)
    e.label('storage_pc_009084')
    e.ins('move.b','%d4,0x2(%a1)',4)
    e.label('storage_pc_009088')
    e.ins('lsr.l','#0x8,%d4',2)
    e.label('storage_pc_00908a')
    e.ins('move.b','%d4,0x1(%a1)',4)
    e.label('storage_pc_00908e')
    e.ins('lsr.w','#0x8,%d4',2)
    e.label('storage_pc_009090')
    e.ins('move.b','%d4,(%a1)',2)
    e.label('storage_pc_009092')
    e.ins('addq.w','#0x4,%a1',2)
    e.label('storage_pc_009094')
    e.ins('move.w','#0x14,%d2',4)
    e.label('storage_pc_009098')
    e.ins('move.l','#0xfffff,%d3',6)
    e.label('storage_pc_00909e')
    e.ins('bsr.w','storage_pc_0091c4',4)
    e.label('storage_pc_0090a2')
    e.ins('move.b','%d4,0x3(%a1)',4)
    e.label('storage_pc_0090a6')
    e.ins('lsr.l','#0x8,%d4',2)
    e.label('storage_pc_0090a8')
    e.ins('move.b','%d4,0x2(%a1)',4)
    e.label('storage_pc_0090ac')
    e.ins('lsr.l','#0x8,%d4',2)
    e.label('storage_pc_0090ae')
    e.ins('move.b','%d4,0x1(%a1)',4)
    e.label('storage_pc_0090b2')
    e.ins('lsr.w','#0x8,%d4',2)
    e.label('storage_pc_0090b4')
    e.ins('move.b','%d4,(%a1)',2)
    e.label('storage_pc_0090b6')
    e.ins('addq.w','#0x4,%a1',2)
    e.label('storage_pc_0090b8')
    e.ins('subq.w','#0x1,%d7',2)
    e.label('storage_pc_0090ba')
    e.ins('move.w','#0x8,%d2',4)
    e.label('storage_pc_0090be')
    e.ins('move.l','#0xff,%d3',6)
    e.label('storage_pc_0090c4')
    e.ins('bsr.w','storage_pc_0091c4',4)
    e.label('storage_pc_0090c8')
    e.ins('move.b','%d4,(%a1)+',2)
    e.label('storage_pc_0090ca')
    e.ins('dbra','%d7,storage_pc_0090ba',4)
    e.label('storage_pc_0090ce')
    e.ins('bra.w','storage_pc_00903e',4)
    e.label('storage_pc_0090d2')
    e.ins('bsr.w','storage_pc_0091f8',4)
    e.label('storage_pc_0090d6')
    e.ins('rts','',2)

def _lower_validate_saved_header_and_checksum(e,rules):
    e.label('storage_pc_0090d8')
    e.ins('cmpi.b','#0x53,0x200105:l',8)
    e.label('storage_pc_0090e0')
    e.ins('bne.w','storage_pc_009142',4)
    e.label('storage_pc_0090e4')
    e.ins('cmpi.b','#0x45,0x200107:l',8)
    e.label('storage_pc_0090ec')
    e.ins('bne.w','storage_pc_009142',4)
    e.label('storage_pc_0090f0')
    e.ins('cmpi.b','#0x47,0x200109:l',8)
    e.label('storage_pc_0090f8')
    e.ins('bne.w','storage_pc_009142',4)
    e.label('storage_pc_0090fc')
    e.ins('cmpi.b','#0x41,0x20010b:l',8)
    e.label('storage_pc_009104')
    e.ins('bne.w','storage_pc_009142',4)
    e.label('storage_pc_009108')
    e.ins('bsr.w','storage_pc_008a22',4)
    e.label('storage_pc_00910c')
    e.ins('cmp.b','0x20010d:l,%d1',6)
    e.label('storage_pc_009112')
    e.ins('bne.w','storage_pc_009142',4)
    e.label('storage_pc_009116')
    e.ins('lsr.l','#0x8,%d1',2)
    e.label('storage_pc_009118')
    e.ins('cmp.b','0x20010f:l,%d1',6)
    e.label('storage_pc_00911e')
    e.ins('bne.w','storage_pc_009142',4)
    e.label('storage_pc_009122')
    e.ins('lsr.l','#0x8,%d1',2)
    e.label('storage_pc_009124')
    e.ins('cmp.b','0x200111:l,%d1',6)
    e.label('storage_pc_00912a')
    e.ins('bne.w','storage_pc_009142',4)
    e.label('storage_pc_00912e')
    e.ins('lsr.w','#0x8,%d1',2)
    e.label('storage_pc_009130')
    e.ins('cmp.b','0x200113:l,%d1',6)
    e.label('storage_pc_009136')
    e.ins('bne.w','storage_pc_009142',4)
    e.label('storage_pc_00913a')
    e.ins('andi.w','#0xfffe,%sr',4)
    e.label('storage_pc_00913e')
    e.ins('bra.w','storage_pc_009146',4)
    e.label('storage_pc_009142')
    e.ins('ori.w','#0x1,%sr',4)
    e.label('storage_pc_009146')
    e.ins('rts','',2)

def _lower_read_buffered_long_bitfield(e,rules):
    e.label('storage_pc_0091c4')
    e.ins('moveq','#0,%d4',2)
    e.label('storage_pc_0091c6')
    e.ins('move.b','%d0,%d4',2)
    e.label('storage_pc_0091c8')
    e.ins('ror.l','#0x8,%d4',2)
    e.label('storage_pc_0091ca')
    e.ins('cmp.w','%d2,%d1',2)
    e.label('storage_pc_0091cc')
    e.ins('bcc.w','storage_pc_0091dc',4)
    e.label('storage_pc_0091d0')
    e.ins('move.b','(%a0)+,%d4',2)
    e.label('storage_pc_0091d2')
    e.ins('move.b','%d4,%d0',2)
    e.label('storage_pc_0091d4')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_0091d8')
    e.ins('addq.w','#0x8,%d1',2)
    e.label('storage_pc_0091da')
    e.ins('bra.b','storage_pc_0091c8',2)
    e.label('storage_pc_0091dc')
    e.ins('move.w','#0x20,%d5',4)
    e.label('storage_pc_0091e0')
    e.ins('sub.w','%d1,%d5',2)
    e.label('storage_pc_0091e2')
    e.ins('cmpi.w','#0x8,%d5',4)
    e.label('storage_pc_0091e6')
    e.ins('bls.w','storage_pc_0091f0',4)
    e.label('storage_pc_0091ea')
    e.ins('lsr.l','#0x8,%d4',2)
    e.label('storage_pc_0091ec')
    e.ins('subq.w','#0x8,%d5',2)
    e.label('storage_pc_0091ee')
    e.ins('bra.b','storage_pc_0091e2',2)
    e.label('storage_pc_0091f0')
    e.ins('lsr.l','%d5,%d4',2)
    e.label('storage_pc_0091f2')
    e.ins('and.l','%d3,%d4',2)
    e.label('storage_pc_0091f4')
    e.ins('sub.w','%d2,%d1',2)
    e.label('storage_pc_0091f6')
    e.ins('rts','',2)

def _lower_write_masked_fixed_count_fields(e,rules):
    e.label('storage_pc_00922a')
    e.ins('subq.w','#0x1,%d2',2)
    e.label('storage_pc_00922c')
    e.ins('clr.w','%d3',2)
    e.label('storage_pc_00922e')
    e.ins('clr.w','%d4',2)
    e.label('storage_pc_009230')
    e.ins('lea.l','104(%pc),%a2',4)
    e.label('storage_pc_009234')
    e.ins('move.w','%d0,%d5',2)
    e.label('storage_pc_009236')
    e.ins('lsl.w','#0x2,%d5',2)
    e.label('storage_pc_009238')
    e.ins('move.l','(%a2, %d5.w),%d5',4)
    e.label('storage_pc_00923c')
    e.ins('moveq','#0,%d7',2)
    e.label('storage_pc_00923e')
    e.ins('move.w','%d1,%d6',2)
    e.label('storage_pc_009240')
    e.ins('tst.w','%d6',2)
    e.label('storage_pc_009242')
    e.ins('beq.w','storage_pc_00926a',4)
    e.label('storage_pc_009246')
    e.ins('cmpi.w','#0x4,%d6',4)
    e.label('storage_pc_00924a')
    e.ins('beq.w','storage_pc_009268',4)
    e.label('storage_pc_00924e')
    e.ins('cmpi.w','#0x2,%d6',4)
    e.label('storage_pc_009252')
    e.ins('bcc.w','storage_pc_00925e',4)
    e.label('storage_pc_009256')
    e.ins('lsl.l','#0x8,%d7',2)
    e.label('storage_pc_009258')
    e.ins('move.b','(%a1)+,%d7',2)
    e.label('storage_pc_00925a')
    e.ins('bra.w','storage_pc_00926a',4)
    e.label('storage_pc_00925e')
    e.ins('swap','%d7',2)
    e.label('storage_pc_009260')
    e.ins('move.w','(%a1)+,%d7',2)
    e.label('storage_pc_009262')
    e.ins('subi.w','#0x2,%d6',4)
    e.label('storage_pc_009266')
    e.ins('bra.b','storage_pc_009240',2)
    e.label('storage_pc_009268')
    e.ins('move.l','(%a1)+,%d7',2)
    e.label('storage_pc_00926a')
    e.ins('and.l','%d5,%d7',2)
    e.label('storage_pc_00926c')
    e.ins('lsl.l','%d4,%d7',2)
    e.label('storage_pc_00926e')
    e.ins('or.b','%d3,%d7',2)
    e.label('storage_pc_009270')
    e.ins('add.w','%d0,%d4',2)
    e.label('storage_pc_009272')
    e.ins('cmpi.w','#0x8,%d4',4)
    e.label('storage_pc_009276')
    e.ins('bcs.w','storage_pc_009288',4)
    e.label('storage_pc_00927a')
    e.ins('move.b','%d7,(%a0)+',2)
    e.label('storage_pc_00927c')
    e.ins('lsr.l','#0x8,%d7',2)
    e.label('storage_pc_00927e')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_009282')
    e.ins('subi.w','#0x8,%d4',4)
    e.label('storage_pc_009286')
    e.ins('bra.b','storage_pc_009272',2)
    e.label('storage_pc_009288')
    e.ins('move.w','%d7,%d3',2)
    e.label('storage_pc_00928a')
    e.ins('dbra','%d2,storage_pc_00923c',4)
    e.label('storage_pc_00928e')
    e.ins('tst.w','%d3',2)
    e.label('storage_pc_009290')
    e.ins('beq.w','storage_pc_009298',4)
    e.label('storage_pc_009294')
    e.ins('move.b','%d3,(%a1)',2)
    e.label('storage_pc_009296')
    e.ins('addq.w','#0x2,%a1',2)
    e.label('storage_pc_009298')
    e.ins('rts','',2)

def _lower_read_masked_fixed_count_fields(e,rules):
    e.label('storage_pc_00931e')
    e.ins('subq.w','#0x1,%d2',2)
    e.label('storage_pc_009320')
    e.ins('clr.w','%d3',2)
    e.label('storage_pc_009322')
    e.ins('clr.w','%d4',2)
    e.label('storage_pc_009324')
    e.ins('lea.l','-140(%pc),%a2',4)
    e.label('storage_pc_009328')
    e.ins('move.w','%d0,%d5',2)
    e.label('storage_pc_00932a')
    e.ins('lsl.w','#0x2,%d5',2)
    e.label('storage_pc_00932c')
    e.ins('move.l','(%a2, %d5.w),%d5',4)
    e.label('storage_pc_009330')
    e.ins('move.b','%d3,%d7',2)
    e.label('storage_pc_009332')
    e.ins('cmp.w','%d0,%d4',2)
    e.label('storage_pc_009334')
    e.ins('bcc.w','storage_pc_009346',4)
    e.label('storage_pc_009338')
    e.ins('ror.l','#0x8,%d7',2)
    e.label('storage_pc_00933a')
    e.ins('move.b','(%a0)+,%d7',2)
    e.label('storage_pc_00933c')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_009340')
    e.ins('addi.w','#0x8,%d4',4)
    e.label('storage_pc_009344')
    e.ins('bra.b','storage_pc_009332',2)
    e.label('storage_pc_009346')
    e.ins('move.w','%d7,%d3',2)
    e.label('storage_pc_009348')
    e.ins('cmpi.w','#0x8,%d4',4)
    e.label('storage_pc_00934c')
    e.ins('bhi.w','storage_pc_00935c',4)
    e.label('storage_pc_009350')
    e.ins('move.w','#0x8,%d6',4)
    e.label('storage_pc_009354')
    e.ins('sub.w','%d4,%d6',2)
    e.label('storage_pc_009356')
    e.ins('lsr.w','%d6,%d7',2)
    e.label('storage_pc_009358')
    e.ins('bra.w','storage_pc_009376',4)
    e.label('storage_pc_00935c')
    e.ins('ror.l','#0x8,%d7',2)
    e.label('storage_pc_00935e')
    e.ins('move.w','#0x20,%d6',4)
    e.label('storage_pc_009362')
    e.ins('sub.w','%d4,%d6',2)
    e.label('storage_pc_009364')
    e.ins('cmpi.w','#0x8,%d6',4)
    e.label('storage_pc_009368')
    e.ins('bls.w','storage_pc_009374',4)
    e.label('storage_pc_00936c')
    e.ins('lsr.l','#0x8,%d7',2)
    e.label('storage_pc_00936e')
    e.ins('subi.w','#0x8,%d6',4)
    e.label('storage_pc_009372')
    e.ins('bra.b','storage_pc_009364',2)
    e.label('storage_pc_009374')
    e.ins('lsr.l','%d6,%d7',2)
    e.label('storage_pc_009376')
    e.ins('and.l','%d5,%d7',2)
    e.label('storage_pc_009378')
    e.ins('move.w','%d1,%d6',2)
    e.label('storage_pc_00937a')
    e.ins('subq.w','#0x1,%d6',2)
    e.label('storage_pc_00937c')
    e.ins('move.b','%d7,(%a1, %d6.w)',4)
    e.label('storage_pc_009380')
    e.ins('lsr.l','#0x8,%d7',2)
    e.label('storage_pc_009382')
    e.ins('dbra','%d6,storage_pc_00937c',4)
    e.label('storage_pc_009386')
    e.ins('adda.w','%d1,%a1',2)
    e.label('storage_pc_009388')
    e.ins('sub.w','%d0,%d4',2)
    e.label('storage_pc_00938a')
    e.ins('dbra','%d2,storage_pc_009330',4)
    e.label('storage_pc_00938e')
    e.ins('rts','',2)

LOWERERS = {
    'write_packed_transport_orders':_lower_write_packed_transport_orders,
    'write_packed_group_stream':_lower_write_packed_group_stream,
    'append_little_endian_bitfield':_lower_append_little_endian_bitfield,
    'write_saved_state_checksum':_lower_write_saved_state_checksum,
    'checksum_saved_payload':_lower_checksum_saved_payload,
    'read_packed_transport_orders':_lower_read_packed_transport_orders,
    'read_buffered_low_word_bitfield':_lower_read_buffered_low_word_bitfield,
    'read_packed_group_stream':_lower_read_packed_group_stream,
    'validate_saved_header_and_checksum':_lower_validate_saved_header_and_checksum,
    'read_buffered_long_bitfield':_lower_read_buffered_long_bitfield,
    'write_masked_fixed_count_fields':_lower_write_masked_fixed_count_fields,
    'read_masked_fixed_count_fields':_lower_read_masked_fixed_count_fields,
}

def compile_streams(source):
    """Admit complete current fields and use untouched physical lowerers.

    This bounded frontend is not a generic Python editor or CPU proof.
    The legacy scalar phase inliner is deliberately not used on the
    complete field source; all actual functions share one declaration
    authority, including real child-slot/flag helpers.
    """
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    current_fields = {'append_little_endian_bitfield': 'append_little_endian_bitfield_frame_fields',
     'checksum_saved_payload': 'checksum_saved_payload_frame_fields',
     'read_buffered_long_bitfield': 'read_buffered_long_bitfield_frame_fields',
     'read_buffered_low_word_bitfield': 'read_buffered_low_word_bitfield_frame_fields',
     'read_masked_fixed_count_fields': 'read_masked_fixed_count_frame_fields',
     'read_packed_group_stream': 'read_packed_group_stream_frame_fields',
     'read_packed_transport_orders': 'read_packed_transport_orders_frame_fields',
     'validate_saved_header_and_checksum': 'validate_saved_header_and_checksum_frame_fields',
     'write_masked_fixed_count_fields': 'write_masked_fixed_count_frame_fields',
     'write_packed_group_stream': 'write_packed_group_stream_frame_fields',
     'write_packed_transport_orders': 'write_packed_transport_orders_frame_fields',
     'write_saved_state_checksum': 'write_saved_state_checksum_frame_fields'}
    selected = {}
    for binding in STREAMS_BINDINGS:
        actual = records[current_fields[binding.name]]
        selected[binding.name] = dict(name=binding.name, rules=actual['rules'], effects=actual['effects'])
    return lower_declared(selected, STREAMS_BINDINGS, LOWERERS)

# C54 complete storage-field authority; no ordinary lowerer or common guard change.
DECLARATIONS.pop('_append_save_byte', None)
DECLARATIONS.pop('_next_fixed_source_value', None)
DECLARATIONS.pop('_next_save_byte', None)
DECLARATIONS.pop('_read_group_long_bytes', None)
DECLARATIONS.pop('_rotate_byte_right', None)
DECLARATIONS.pop('_shift_long_left', None)
DECLARATIONS.pop('_shift_word_left', None)
DECLARATIONS.pop('_store_group_long_reverse', None)
DECLARATIONS.update({'_read_saved_group_long_fields': {'flow': "frame, value = storage_read_next(state, frame, 'a1', "
                                           '1)\n'
                                           "frame = storage_move(state, frame, 'd0', value, 8)\n"
                                           "frame = storage_shift(state, frame, 'd0', 8, 16)\n"
                                           "frame, value = storage_read_next(state, frame, 'a1', "
                                           '1)\n'
                                           "frame = storage_move(state, frame, 'd0', value, 8)\n"
                                           'for _ in range(2):\n'
                                           "    frame = storage_shift(state, frame, 'd0', 8, 32)\n"
                                           '    frame, value = storage_read_next(state, frame, '
                                           "'a1', 1)\n"
                                           "    frame = storage_move(state, frame, 'd0', value, "
                                           '8)\n'
                                           'return frame',
                                   'returns': 'StorageFrame',
                                   'signature': 'state: StorageState, frame: StorageFrame'},
 '_restore_saved_group_long_fields': {'flow': 'for displacement, following_bits in ((3, 32), (2, '
                                              '32), (1, 16), (0, 0)):\n'
                                              '    frame = storage_write(state, frame, frame.a1 + '
                                              'displacement, 1, frame.d4)\n'
                                              '    if following_bits:\n'
                                              "        frame = storage_shift(state, frame, 'd4', "
                                              '8, following_bits, True)\n'
                                              "return storage_address_step(frame, 'a1', 4)",
                                      'returns': 'StorageFrame',
                                      'signature': 'state: StorageState, frame: StorageFrame'},
 '_storage_fixed_mask_fields': {'flow': "frame = storage_address(frame, 'a2', 37530)\n"
                                        "frame = storage_move(state, frame, 'd5', frame.d0, 16)\n"
                                        "frame = storage_shift(state, frame, 'd5', 2, 16)\n"
                                        'mask = state.read(frame.a2 + s16(low16(frame.d5)), 4)\n'
                                        "return storage_move(state, frame, 'd5', mask, 32)",
                                'returns': 'StorageFrame',
                                'signature': 'state: StorageState, frame: StorageFrame'},
 '_storage_flush_word_residue_fields': {'flow': "if carrier not in ('d0', 'd7'):\n"
                                                "    raise ValueError('closed storage residue "
                                                "carrier required')\n"
                                                'while True:\n'
                                                '    frame = storage_arithmetic(state, frame, '
                                                "'d4', 8, 16, True, True)\n"
                                                '    if frame.status_word & 1:\n'
                                                '        return frame\n'
                                                "    value = frame.d0 if carrier == 'd0' else "
                                                'frame.d7\n'
                                                '    frame = storage_write_next(state, frame, '
                                                "'a0', 1, value)\n"
                                                "    frame = storage_address_step(frame, 'a0', 1)\n"
                                                '    frame = storage_arithmetic(state, frame, '
                                                "'d4', 8, 16, True)\n"
                                                '    frame = storage_shift(state, frame, carrier, '
                                                '8, 32, True)',
                                        'returns': 'StorageFrame',
                                        'signature': 'state: StorageState, frame: StorageFrame, '
                                                     'carrier: str'},
 'append_little_endian_bitfield': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                           'checked_buffer(writer, BitWriter, state)\n'
                                           'if (writer.cursor.base, writer.residue, '
                                           'writer.bit_count, value, width) != (frame.a0, '
                                           'frame.d3, low16(frame.d4), frame.d0, '
                                           'low16(frame.d1)):\n'
                                           "    raise ValueError('bit-writer arguments differ from "
                                           "complete entry')\n"
                                           'returned = '
                                           'append_little_endian_bitfield_frame_fields(state, '
                                           'frame)\n'
                                           'writer.cursor.base = returned.a0\n'
                                           'writer.residue = returned.d3\n'
                                           'writer.bit_count = low16(returned.d4)\n'
                                           'return returned.d0',
                                   'returns': 'Long',
                                   'signature': 'state: StorageState, writer: BitWriter, value: '
                                                'Long, width: Word, entry_frame: '
                                                'StorageFrame=None'},
 'append_little_endian_bitfield_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                        "frame = storage_shift(state, frame, 'd0', "
                                                        'low16(frame.d4), 32)\n'
                                                        'frame = storage_binary(state, frame, '
                                                        "'d0', frame.d3, 16, 'or')\n"
                                                        'frame = storage_arithmetic(state, frame, '
                                                        "'d4', frame.d1, 16)\n"
                                                        'frame = '
                                                        '_storage_flush_word_residue_fields(state, '
                                                        "frame, 'd0')\n"
                                                        "return storage_move(state, frame, 'd3', "
                                                        'frame.d0, 16)',
                                                'returns': 'StorageFrame',
                                                'signature': 'state: StorageState, frame: '
                                                             'StorageFrame'},
 'checksum_saved_payload': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                    'returned = checksum_saved_payload_frame_fields(state, frame)\n'
                                    'return returned.d1',
                            'returns': 'Long',
                            'signature': 'state: StorageState, entry_frame: StorageFrame=None'},
 'checksum_saved_payload_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                 "frame = storage_address(frame, 'a0', 2097429)\n"
                                                 "frame = storage_move(state, frame, 'd0', 7916, "
                                                 '16)\n'
                                                 "frame = storage_move(state, frame, 'd1', 0, 32)\n"
                                                 "frame = storage_move(state, frame, 'd2', 0, 32)\n"
                                                 'while True:\n'
                                                 '    frame, value = storage_read_next(state, '
                                                 "frame, 'a0', 1)\n"
                                                 "    frame = storage_move(state, frame, 'd2', "
                                                 'value, 8)\n'
                                                 '    frame = storage_arithmetic(state, frame, '
                                                 "'d1', frame.d2, 32)\n"
                                                 "    frame = storage_address_step(frame, 'a0', "
                                                 '1)\n'
                                                 "    frame, again = storage_dbra(frame, 'd0')\n"
                                                 '    if not again:\n'
                                                 '        return frame',
                                         'returns': 'StorageFrame',
                                         'signature': 'state: StorageState, frame: StorageFrame'},
 'read_buffered_long_bitfield': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                         'checked_buffer(reader, BitReader, state)\n'
                                         'if (reader.cursor.base, reader.residue, '
                                         'reader.bit_count, width, mask) != (frame.a0, frame.d0, '
                                         'low16(frame.d1), low16(frame.d2), frame.d3):\n'
                                         "    raise ValueError('LONG reader arguments differ from "
                                         "complete entry')\n"
                                         'returned = '
                                         'read_buffered_long_bitfield_frame_fields(state, frame)\n'
                                         'reader.cursor.base = returned.a0\n'
                                         'reader.residue = returned.d0\n'
                                         'reader.bit_count = low16(returned.d1)\n'
                                         'return returned.d4',
                                 'returns': 'Long',
                                 'signature': 'state: StorageState, reader: BitReader, width: '
                                              'Word, mask: Long, entry_frame: StorageFrame=None'},
 'read_buffered_long_bitfield_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                      "frame = storage_move(state, frame, 'd4', 0, "
                                                      '32)\n'
                                                      "frame = storage_move(state, frame, 'd4', "
                                                      'frame.d0, 8)\n'
                                                      "frame = storage_shift(state, frame, 'd4', "
                                                      '8, 32, True, True)\n'
                                                      'while True:\n'
                                                      '    frame = storage_arithmetic(state, '
                                                      "frame, 'd1', frame.d2, 16, True, True)\n"
                                                      '    if not frame.status_word & 1:\n'
                                                      '        break\n'
                                                      '    frame, value = storage_read_next(state, '
                                                      "frame, 'a0', 1)\n"
                                                      '    frame = storage_move(state, frame, '
                                                      "'d4', value, 8)\n"
                                                      '    frame = storage_move(state, frame, '
                                                      "'d0', frame.d4, 8)\n"
                                                      '    frame = storage_address_step(frame, '
                                                      "'a0', 1)\n"
                                                      '    frame = storage_arithmetic(state, '
                                                      "frame, 'd1', 8, 16)\n"
                                                      '    frame = storage_shift(state, frame, '
                                                      "'d4', 8, 32, True, True)\n"
                                                      "frame = storage_move(state, frame, 'd5', "
                                                      '32, 16)\n'
                                                      'frame = storage_arithmetic(state, frame, '
                                                      "'d5', frame.d1, 16, True)\n"
                                                      'while True:\n'
                                                      '    frame = storage_arithmetic(state, '
                                                      "frame, 'd5', 8, 16, True, True)\n"
                                                      '    if frame.status_word & 5:\n'
                                                      '        break\n'
                                                      '    frame = storage_shift(state, frame, '
                                                      "'d4', 8, 32, True)\n"
                                                      '    frame = storage_arithmetic(state, '
                                                      "frame, 'd5', 8, 16, True)\n"
                                                      "frame = storage_shift(state, frame, 'd4', "
                                                      'low16(frame.d5), 32, True)\n'
                                                      "frame = storage_binary(state, frame, 'd4', "
                                                      "frame.d3, 32, 'and')\n"
                                                      'return storage_arithmetic(state, frame, '
                                                      "'d1', frame.d2, 16, True)",
                                              'returns': 'StorageFrame',
                                              'signature': 'state: StorageState, frame: '
                                                           'StorageFrame'},
 'read_buffered_low_word_bitfield': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                             'checked_buffer(reader, BitReader, state)\n'
                                             'if (reader.cursor.base, reader.residue, '
                                             'reader.bit_count, width, mask) != (frame.a0, '
                                             'frame.d3, low16(frame.d4), low16(frame.d5), '
                                             'low16(frame.d6)):\n'
                                             "    raise ValueError('WORD reader arguments differ "
                                             "from complete entry')\n"
                                             'returned = '
                                             'read_buffered_low_word_bitfield_frame_fields(state, '
                                             'frame)\n'
                                             'reader.cursor.base = returned.a0\n'
                                             'reader.residue = returned.d3\n'
                                             'reader.bit_count = low16(returned.d4)\n'
                                             'return low16(returned.d2)',
                                     'returns': 'Word',
                                     'signature': 'state: StorageState, reader: BitReader, width: '
                                                  'Word, mask: Word, entry_frame: '
                                                  'StorageFrame=None'},
 'read_buffered_low_word_bitfield_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                          'frame = storage_arithmetic(state, '
                                                          "frame, 'd4', frame.d5, 16, True, True)\n"
                                                          'if frame.status_word & 1:\n'
                                                          '    frame = storage_move(state, frame, '
                                                          "'d1', 0, 16)\n"
                                                          '    frame, value = '
                                                          "storage_read_next(state, frame, 'a0', "
                                                          '1)\n'
                                                          '    frame = storage_move(state, frame, '
                                                          "'d1', value, 8)\n"
                                                          '    frame = storage_address_step(frame, '
                                                          "'a0', 1)\n"
                                                          '    frame = storage_shift(state, frame, '
                                                          "'d1', low16(frame.d4), 16)\n"
                                                          '    frame = storage_binary(state, '
                                                          "frame, 'd3', frame.d1, 16, 'or')\n"
                                                          '    frame = storage_arithmetic(state, '
                                                          "frame, 'd4', 8, 16)\n"
                                                          'frame = storage_move(state, frame, '
                                                          "'d2', frame.d3, 16)\n"
                                                          'frame = storage_binary(state, frame, '
                                                          "'d2', frame.d6, 16, 'and')\n"
                                                          'frame = storage_shift(state, frame, '
                                                          "'d3', low16(frame.d5), 16, True)\n"
                                                          'return storage_arithmetic(state, frame, '
                                                          "'d4', frame.d5, 16, True)",
                                                  'returns': 'StorageFrame',
                                                  'signature': 'state: StorageState, frame: '
                                                               'StorageFrame'},
 'read_masked_fixed_count_fields': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                            'checked_cursor(source, state)\n'
                                            'checked_table(destination, state)\n'
                                            'if (source.base, destination.base, bit_width, '
                                            'destination_width, record_count) != (frame.a0, '
                                            'frame.a1, low16(frame.d0), low16(frame.d1), '
                                            'low16(frame.d2)):\n'
                                            "    raise ValueError('fixed reader arguments differ "
                                            "from complete entry')\n"
                                            'if retained is not None:\n'
                                            '    if type(retained) is not FixedFieldReadContext:\n'
                                            "        raise ValueError('exact fixed-field retained "
                                            "context required')\n"
                                            '    retained.__post_init__()\n'
                                            '    if retained.value_carrier != frame.d7:\n'
                                            "        raise ValueError('fixed reader retained LONG "
                                            "differs from entry D7')\n"
                                            'returned = '
                                            'read_masked_fixed_count_frame_fields(state, frame)\n'
                                            'source.base = returned.a0\n'
                                            'if retained is not None:\n'
                                            '    retained.value_carrier = returned.d7\n'
                                            'return source',
                                    'returns': 'Cursor',
                                    'signature': 'state: StorageState, source: Cursor, '
                                                 'destination: Table, bit_width: Word, '
                                                 'destination_width: Word, record_count: Word, '
                                                 'retained: FixedFieldReadContext=None, '
                                                 'entry_frame: StorageFrame=None'},
 'read_masked_fixed_count_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                  "frame = storage_arithmetic(state, frame, 'd2', "
                                                  '1, 16, True)\n'
                                                  "frame = storage_move(state, frame, 'd3', 0, "
                                                  '16)\n'
                                                  "frame = storage_move(state, frame, 'd4', 0, "
                                                  '16)\n'
                                                  'frame = _storage_fixed_mask_fields(state, '
                                                  'frame)\n'
                                                  'while True:\n'
                                                  "    frame = storage_move(state, frame, 'd7', "
                                                  'frame.d3, 8)\n'
                                                  '    while True:\n'
                                                  '        frame = storage_arithmetic(state, '
                                                  "frame, 'd4', frame.d0, 16, True, True)\n"
                                                  '        if not frame.status_word & 1:\n'
                                                  '            break\n'
                                                  '        frame = storage_shift(state, frame, '
                                                  "'d7', 8, 32, True, True)\n"
                                                  '        frame, value = storage_read_next(state, '
                                                  "frame, 'a0', 1)\n"
                                                  '        frame = storage_move(state, frame, '
                                                  "'d7', value, 8)\n"
                                                  '        frame = storage_address_step(frame, '
                                                  "'a0', 1)\n"
                                                  '        frame = storage_arithmetic(state, '
                                                  "frame, 'd4', 8, 16)\n"
                                                  "    frame = storage_move(state, frame, 'd3', "
                                                  'frame.d7, 16)\n'
                                                  '    frame = storage_arithmetic(state, frame, '
                                                  "'d4', 8, 16, True, True)\n"
                                                  '    if frame.status_word & 5:\n'
                                                  '        frame = storage_move(state, frame, '
                                                  "'d6', 8, 16)\n"
                                                  '        frame = storage_arithmetic(state, '
                                                  "frame, 'd6', frame.d4, 16, True)\n"
                                                  '        frame = storage_shift(state, frame, '
                                                  "'d7', low16(frame.d6), 16, True)\n"
                                                  '    else:\n'
                                                  '        frame = storage_shift(state, frame, '
                                                  "'d7', 8, 32, True, True)\n"
                                                  '        frame = storage_move(state, frame, '
                                                  "'d6', 32, 16)\n"
                                                  '        frame = storage_arithmetic(state, '
                                                  "frame, 'd6', frame.d4, 16, True)\n"
                                                  '        while True:\n'
                                                  '            frame = storage_arithmetic(state, '
                                                  "frame, 'd6', 8, 16, True, True)\n"
                                                  '            if frame.status_word & 5:\n'
                                                  '                break\n'
                                                  '            frame = storage_shift(state, frame, '
                                                  "'d7', 8, 32, True)\n"
                                                  '            frame = storage_arithmetic(state, '
                                                  "frame, 'd6', 8, 16, True)\n"
                                                  '        frame = storage_shift(state, frame, '
                                                  "'d7', low16(frame.d6), 32, True)\n"
                                                  "    frame = storage_binary(state, frame, 'd7', "
                                                  "frame.d5, 32, 'and')\n"
                                                  "    frame = storage_move(state, frame, 'd6', "
                                                  'frame.d1, 16)\n'
                                                  '    frame = storage_arithmetic(state, frame, '
                                                  "'d6', 1, 16, True)\n"
                                                  '    while True:\n'
                                                  '        frame = storage_write(state, frame, '
                                                  'frame.a1 + s16(low16(frame.d6)), 1, frame.d7)\n'
                                                  '        frame = storage_shift(state, frame, '
                                                  "'d7', 8, 32, True)\n"
                                                  '        frame, again = storage_dbra(frame, '
                                                  "'d6')\n"
                                                  '        if not again:\n'
                                                  '            break\n'
                                                  "    frame = storage_address_step(frame, 'a1', "
                                                  's16(low16(frame.d1)))\n'
                                                  '    frame = storage_arithmetic(state, frame, '
                                                  "'d4', frame.d0, 16, True)\n"
                                                  "    frame, again = storage_dbra(frame, 'd2')\n"
                                                  '    if not again:\n'
                                                  '        return frame',
                                          'returns': 'StorageFrame',
                                          'signature': 'state: StorageState, frame: StorageFrame'},
 'read_packed_group_stream': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                      'checked_cursor(source, state)\n'
                                      'if source.base != frame.a0:\n'
                                      "    raise ValueError('load stream differs from complete "
                                      "entry A0')\n"
                                      'returned = read_packed_group_stream_frame_fields(state, '
                                      'frame)\n'
                                      'source.base = returned.a0\n'
                                      'return source',
                              'returns': 'Cursor',
                              'signature': 'state: StorageState, source: Cursor, entry_frame: '
                                           'StorageFrame=None'},
 'read_packed_group_stream_frame_fields': {'flow': 'from .business_load import '
                                                   'refresh_loaded_group_attributes_frame_fields\n'
                                                   'frame = storage_entry(state, frame)\n'
                                                   "frame = storage_address(frame, 'a1', "
                                                   '4294938624)\n'
                                                   "frame = storage_move(state, frame, 'd0', 0, "
                                                   '16)\n'
                                                   "frame = storage_move(state, frame, 'd1', 0, "
                                                   '16)\n'
                                                   'while True:\n'
                                                   "    frame = storage_move(state, frame, 'd2', "
                                                   '4, 16)\n'
                                                   "    frame = storage_move(state, frame, 'd3', "
                                                   '15, 32)\n'
                                                   '    frame = storage_call(state, frame, '
                                                   'read_buffered_long_bitfield_frame_fields, '
                                                   '36936)\n'
                                                   '    frame = storage_write_next(state, frame, '
                                                   "'a1', 1, frame.d4)\n"
                                                   '    if frame.status_word & 4:\n'
                                                   '        break\n'
                                                   "    frame = storage_move(state, frame, 'd7', "
                                                   'frame.d4, 16)\n'
                                                   "    frame = storage_move(state, frame, 'd2', "
                                                   '7, 16)\n'
                                                   "    frame = storage_move(state, frame, 'd3', "
                                                   '127, 32)\n'
                                                   '    frame = storage_call(state, frame, '
                                                   'read_buffered_long_bitfield_frame_fields, '
                                                   '36954)\n'
                                                   '    frame = storage_write_next(state, frame, '
                                                   "'a1', 1, frame.d4)\n"
                                                   '    frame = storage_call(state, frame, '
                                                   'read_buffered_long_bitfield_frame_fields, '
                                                   '36960)\n'
                                                   '    frame = storage_write_next(state, frame, '
                                                   "'a1', 1, frame.d4)\n"
                                                   "    frame = storage_address_step(frame, 'a1', "
                                                   '1)\n'
                                                   "    frame = storage_move(state, frame, 'd2', "
                                                   '4, 16)\n'
                                                   "    frame = storage_move(state, frame, 'd3', "
                                                   '15, 32)\n'
                                                   '    frame = storage_call(state, frame, '
                                                   'read_buffered_long_bitfield_frame_fields, '
                                                   '36974)\n'
                                                   '    frame = storage_write_next(state, frame, '
                                                   "'a1', 1, frame.d4)\n"
                                                   '    for width, mask, continuation in ((18, '
                                                   '262143, 36990), (20, 1048575, 37026)):\n'
                                                   '        frame = storage_move(state, frame, '
                                                   "'d2', width, 16)\n"
                                                   '        frame = storage_move(state, frame, '
                                                   "'d3', mask, 32)\n"
                                                   '        frame = storage_call(state, frame, '
                                                   'read_buffered_long_bitfield_frame_fields, '
                                                   'continuation)\n'
                                                   '        frame = '
                                                   '_restore_saved_group_long_fields(state, '
                                                   'frame)\n'
                                                   '    frame = storage_arithmetic(state, frame, '
                                                   "'d7', 1, 16, True)\n"
                                                   '    while True:\n'
                                                   '        frame = storage_move(state, frame, '
                                                   "'d2', 8, 16)\n"
                                                   '        frame = storage_move(state, frame, '
                                                   "'d3', 255, 32)\n"
                                                   '        frame = storage_call(state, frame, '
                                                   'read_buffered_long_bitfield_frame_fields, '
                                                   '37064)\n'
                                                   '        frame = storage_write_next(state, '
                                                   "frame, 'a1', 1, frame.d4)\n"
                                                   '        frame, again = storage_dbra(frame, '
                                                   "'d7')\n"
                                                   '        if not again:\n'
                                                   '            break\n'
                                                   'return storage_call(state, frame, '
                                                   'refresh_loaded_group_attributes_frame_fields, '
                                                   '37078)',
                                           'returns': 'StorageFrame',
                                           'signature': 'state: StorageState, frame: StorageFrame'},
 'read_packed_transport_orders': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                          'checked_cursor(source, state)\n'
                                          'if source.base != frame.a0:\n'
                                          "    raise ValueError('load stream differs from complete "
                                          "entry A0')\n"
                                          'returned = '
                                          'read_packed_transport_orders_frame_fields(state, '
                                          'frame)\n'
                                          'source.base = returned.a0\n'
                                          'return source',
                                  'returns': 'Cursor',
                                  'signature': 'state: StorageState, source: Cursor, entry_frame: '
                                               'StorageFrame=None'},
 'read_packed_transport_orders_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                       "frame = storage_address(frame, 'a1', "
                                                       '4294954496)\n'
                                                       "frame = storage_move(state, frame, 'd3', "
                                                       '0, 16)\n'
                                                       "frame = storage_move(state, frame, 'd4', "
                                                       '0, 16)\n'
                                                       "frame = storage_move(state, frame, 'd7', "
                                                       '39, 16)\n'
                                                       'while True:\n'
                                                       '    for width, mask, displacement, '
                                                       'continuation in ((6, 63, 3, 36812), (7, '
                                                       '127, 2, 36828), (7, 127, 1, 36836), (2, 3, '
                                                       '0, 36852)):\n'
                                                       '        if displacement != 1:\n'
                                                       '            frame = storage_move(state, '
                                                       "frame, 'd5', width, 16)\n"
                                                       '            frame = storage_move(state, '
                                                       "frame, 'd6', mask, 16)\n"
                                                       '        frame = storage_call(state, frame, '
                                                       'read_buffered_low_word_bitfield_frame_fields, '
                                                       'continuation)\n'
                                                       '        frame = storage_write(state, '
                                                       'frame, frame.a1 + displacement, 1, '
                                                       'frame.d2)\n'
                                                       '    frame = storage_address_step(frame, '
                                                       "'a1', 4)\n"
                                                       '    frame, again = storage_dbra(frame, '
                                                       "'d7')\n"
                                                       '    if not again:\n'
                                                       '        return frame',
                                               'returns': 'StorageFrame',
                                               'signature': 'state: StorageState, frame: '
                                                            'StorageFrame'},
 'validate_saved_header_and_checksum': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                                'returned = '
                                                'validate_saved_header_and_checksum_frame_fields(state, '
                                                'frame)\n'
                                                'return CarryOutcome(returned.status_word & 1, '
                                                'returned.status_word)',
                                        'returns': 'CarryOutcome',
                                        'signature': 'state: StorageState, entry_frame: '
                                                     'StorageFrame=None'},
 'validate_saved_header_and_checksum_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                             'valid = True\n'
                                                             'for address, expected in ((2097413, '
                                                             '83), (2097415, 69), (2097417, 71), '
                                                             '(2097419, 65)):\n'
                                                             '    frame = '
                                                             'storage_compare_value(state, frame, '
                                                             'state.read(address, 1), expected, '
                                                             '8)\n'
                                                             '    if not frame.status_word & 4:\n'
                                                             '        valid = False\n'
                                                             '        break\n'
                                                             'if valid:\n'
                                                             '    frame = storage_call(state, '
                                                             'frame, '
                                                             'checksum_saved_payload_frame_fields, '
                                                             '37132)\n'
                                                             '    for address, following_bits in '
                                                             '((2097421, 32), (2097423, 32), '
                                                             '(2097425, 16), (2097427, 0)):\n'
                                                             '        frame = '
                                                             'storage_arithmetic(state, frame, '
                                                             "'d1', state.read(address, 1), 8, "
                                                             'True, True)\n'
                                                             '        if not frame.status_word & '
                                                             '4:\n'
                                                             '            valid = False\n'
                                                             '            break\n'
                                                             '        if following_bits:\n'
                                                             '            frame = '
                                                             "storage_shift(state, frame, 'd1', 8, "
                                                             'following_bits, True)\n'
                                                             'state.sr = frame.status_word\n'
                                                             'state.carry_result(0 if valid else '
                                                             '1)\n'
                                                             'return storage_replace(frame, '
                                                             'status_word=state.sr)',
                                                     'returns': 'StorageFrame',
                                                     'signature': 'state: StorageState, frame: '
                                                                  'StorageFrame'},
 'write_masked_fixed_count_fields': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                             'checked_table(source, state)\n'
                                             'checked_cursor(destination, state)\n'
                                             'if (source.base, destination.base, bit_width, '
                                             'source_width, record_count) != (frame.a1, frame.a0, '
                                             'low16(frame.d0), low16(frame.d1), low16(frame.d2)):\n'
                                             "    raise ValueError('fixed writer arguments differ "
                                             "from complete entry')\n"
                                             'returned = '
                                             'write_masked_fixed_count_frame_fields(state, frame)\n'
                                             'destination.base = returned.a0\n'
                                             'return destination',
                                     'returns': 'Cursor',
                                     'signature': 'state: StorageState, source: Table, '
                                                  'destination: Cursor, bit_width: Word, '
                                                  'source_width: Word, record_count: Word, '
                                                  'entry_frame: StorageFrame=None'},
 'write_masked_fixed_count_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                   "frame = storage_arithmetic(state, frame, 'd2', "
                                                   '1, 16, True)\n'
                                                   "frame = storage_move(state, frame, 'd3', 0, "
                                                   '16)\n'
                                                   "frame = storage_move(state, frame, 'd4', 0, "
                                                   '16)\n'
                                                   'frame = _storage_fixed_mask_fields(state, '
                                                   'frame)\n'
                                                   'while True:\n'
                                                   "    frame = storage_move(state, frame, 'd7', "
                                                   '0, 32)\n'
                                                   "    frame = storage_move(state, frame, 'd6', "
                                                   'frame.d1, 16)\n'
                                                   '    while True:\n'
                                                   '        frame = storage_logic(state, frame, '
                                                   'frame.d6, 16)\n'
                                                   '        if frame.status_word & 4:\n'
                                                   '            break\n'
                                                   '        frame = storage_arithmetic(state, '
                                                   "frame, 'd6', 4, 16, True, True)\n"
                                                   '        if frame.status_word & 4:\n'
                                                   '            frame, value = '
                                                   "storage_read_next(state, frame, 'a1', 4)\n"
                                                   '            frame = storage_move(state, frame, '
                                                   "'d7', value, 32)\n"
                                                   '            break\n'
                                                   '        frame = storage_arithmetic(state, '
                                                   "frame, 'd6', 2, 16, True, True)\n"
                                                   '        if not frame.status_word & 1:\n'
                                                   '            frame = storage_swap(state, frame, '
                                                   "'d7')\n"
                                                   '            frame, value = '
                                                   "storage_read_next(state, frame, 'a1', 2)\n"
                                                   '            frame = storage_move(state, frame, '
                                                   "'d7', value, 16)\n"
                                                   '            frame = storage_arithmetic(state, '
                                                   "frame, 'd6', 2, 16, True)\n"
                                                   '            continue\n'
                                                   '        frame = storage_shift(state, frame, '
                                                   "'d7', 8, 32)\n"
                                                   '        frame, value = '
                                                   "storage_read_next(state, frame, 'a1', 1)\n"
                                                   '        frame = storage_move(state, frame, '
                                                   "'d7', value, 8)\n"
                                                   '        break\n'
                                                   "    frame = storage_binary(state, frame, 'd7', "
                                                   "frame.d5, 32, 'and')\n"
                                                   "    frame = storage_shift(state, frame, 'd7', "
                                                   'low16(frame.d4), 32)\n'
                                                   "    frame = storage_binary(state, frame, 'd7', "
                                                   "frame.d3, 8, 'or')\n"
                                                   '    frame = storage_arithmetic(state, frame, '
                                                   "'d4', frame.d0, 16)\n"
                                                   '    while True:\n'
                                                   '        frame = storage_arithmetic(state, '
                                                   "frame, 'd4', 8, 16, True, True)\n"
                                                   '        if frame.status_word & 1:\n'
                                                   '            break\n'
                                                   '        frame = storage_write_next(state, '
                                                   "frame, 'a0', 1, frame.d7)\n"
                                                   '        frame = storage_shift(state, frame, '
                                                   "'d7', 8, 32, True)\n"
                                                   '        frame = storage_address_step(frame, '
                                                   "'a0', 1)\n"
                                                   '        frame = storage_arithmetic(state, '
                                                   "frame, 'd4', 8, 16, True)\n"
                                                   "    frame = storage_move(state, frame, 'd3', "
                                                   'frame.d7, 16)\n'
                                                   "    frame, again = storage_dbra(frame, 'd2')\n"
                                                   '    if not again:\n'
                                                   '        break\n'
                                                   'frame = storage_logic(state, frame, frame.d3, '
                                                   '16)\n'
                                                   'if not frame.status_word & 4:\n'
                                                   '    frame = storage_write(state, frame, '
                                                   'frame.a1, 1, frame.d3)\n'
                                                   "    frame = storage_address_step(frame, 'a1', "
                                                   '2)\n'
                                                   'return frame',
                                           'returns': 'StorageFrame',
                                           'signature': 'state: StorageState, frame: StorageFrame'},
 'write_packed_group_stream': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                       'checked_cursor(destination, state)\n'
                                       'if destination.base != frame.a0:\n'
                                       "    raise ValueError('save stream differs from complete "
                                       "entry A0')\n"
                                       'returned = write_packed_group_stream_frame_fields(state, '
                                       'frame)\n'
                                       'destination.base = returned.a0\n'
                                       'return destination',
                               'returns': 'Cursor',
                               'signature': 'state: StorageState, destination: Cursor, '
                                            'entry_frame: StorageFrame=None'},
 'write_packed_group_stream_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                    "frame = storage_address(frame, 'a1', "
                                                    '4294938624)\n'
                                                    "frame = storage_move(state, frame, 'd3', 0, "
                                                    '32)\n'
                                                    "frame = storage_move(state, frame, 'd4', 0, "
                                                    '16)\n'
                                                    'while True:\n'
                                                    '    frame, value = storage_read_next(state, '
                                                    "frame, 'a1', 1)\n"
                                                    "    frame = storage_move(state, frame, 'd0', "
                                                    'value, 8)\n'
                                                    '    frame = storage_binary(state, frame, '
                                                    "'d0', 15, 32, 'and')\n"
                                                    "    frame = storage_move(state, frame, 'd7', "
                                                    'frame.d0, 16)\n'
                                                    "    frame = storage_move(state, frame, 'd1', "
                                                    '4, 16)\n'
                                                    '    frame = storage_call(state, frame, '
                                                    'append_little_endian_bitfield_frame_fields, '
                                                    '35168)\n'
                                                    '    frame = storage_logic(state, frame, '
                                                    'frame.d7, 16)\n'
                                                    '    if frame.status_word & 4:\n'
                                                    '        break\n'
                                                    '    for continuation in (35190, 35206):\n'
                                                    '        frame, value = '
                                                    "storage_read_next(state, frame, 'a1', 1)\n"
                                                    '        frame = storage_move(state, frame, '
                                                    "'d0', value, 8)\n"
                                                    '        frame = storage_binary(state, frame, '
                                                    "'d0', 127, 32, 'and')\n"
                                                    '        frame = storage_move(state, frame, '
                                                    "'d1', 7, 16)\n"
                                                    '        frame = storage_call(state, frame, '
                                                    'append_little_endian_bitfield_frame_fields, '
                                                    'continuation)\n'
                                                    "    frame = storage_address_step(frame, 'a1', "
                                                    '1)\n'
                                                    '    frame, value = storage_read_next(state, '
                                                    "frame, 'a1', 1)\n"
                                                    "    frame = storage_move(state, frame, 'd0', "
                                                    'value, 8)\n'
                                                    "    frame = storage_move(state, frame, 'd1', "
                                                    '4, 16)\n'
                                                    '    frame = storage_call(state, frame, '
                                                    'append_little_endian_bitfield_frame_fields, '
                                                    '35218)\n'
                                                    '    for width, continuation in ((18, 35240), '
                                                    '(20, 35262)):\n'
                                                    '        frame = '
                                                    '_read_saved_group_long_fields(state, frame)\n'
                                                    '        frame = storage_move(state, frame, '
                                                    "'d1', width, 16)\n"
                                                    '        frame = storage_call(state, frame, '
                                                    'append_little_endian_bitfield_frame_fields, '
                                                    'continuation)\n'
                                                    '    frame = storage_arithmetic(state, frame, '
                                                    "'d7', 1, 16, True)\n"
                                                    '    while True:\n'
                                                    '        frame, value = '
                                                    "storage_read_next(state, frame, 'a1', 1)\n"
                                                    '        frame = storage_move(state, frame, '
                                                    "'d0', value, 8)\n"
                                                    '        frame = storage_binary(state, frame, '
                                                    "'d0', 255, 32, 'and')\n"
                                                    '        frame = storage_move(state, frame, '
                                                    "'d1', 8, 16)\n"
                                                    '        frame = storage_call(state, frame, '
                                                    'append_little_endian_bitfield_frame_fields, '
                                                    '35280)\n'
                                                    '        frame, again = storage_dbra(frame, '
                                                    "'d7')\n"
                                                    '        if not again:\n'
                                                    '            break\n'
                                                    'frame = storage_write_next(state, frame, '
                                                    "'a0', 1, frame.d3)\n"
                                                    "return storage_address_step(frame, 'a0', 1)",
                                            'returns': 'StorageFrame',
                                            'signature': 'state: StorageState, frame: '
                                                         'StorageFrame'},
 'write_packed_transport_orders': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                           'checked_cursor(destination, state)\n'
                                           'if destination.base != frame.a0:\n'
                                           "    raise ValueError('save stream differs from "
                                           "complete entry A0')\n"
                                           'returned = '
                                           'write_packed_transport_orders_frame_fields(state, '
                                           'frame)\n'
                                           'destination.base = returned.a0\n'
                                           'return destination',
                                   'returns': 'Cursor',
                                   'signature': 'state: StorageState, destination: Cursor, '
                                                'entry_frame: StorageFrame=None'},
 'write_packed_transport_orders_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                        "frame = storage_address(frame, 'a1', "
                                                        '4294954496)\n'
                                                        "frame = storage_move(state, frame, 'd3', "
                                                        '0, 16)\n'
                                                        "frame = storage_move(state, frame, 'd4', "
                                                        '0, 16)\n'
                                                        "frame = storage_move(state, frame, 'd0', "
                                                        '39, 16)\n'
                                                        'while True:\n'
                                                        '    frame = storage_move(state, frame, '
                                                        "'d7', 0, 32)\n"
                                                        '    frame, value = '
                                                        "storage_read_next(state, frame, 'a1', 1)\n"
                                                        '    frame = storage_move(state, frame, '
                                                        "'d7', value, 8)\n"
                                                        '    frame = storage_binary(state, frame, '
                                                        "'d7', 3, 16, 'and')\n"
                                                        '    for width, mask in ((7, 127), (7, '
                                                        '127), (6, 63)):\n'
                                                        '        frame = storage_shift(state, '
                                                        "frame, 'd7', width, 32 if width == 6 else "
                                                        '16)\n'
                                                        '        frame, value = '
                                                        "storage_read_next(state, frame, 'a1', 1)\n"
                                                        '        frame = storage_move(state, '
                                                        "frame, 'd1', value, 8)\n"
                                                        '        frame = storage_binary(state, '
                                                        "frame, 'd1', mask, 16, 'and')\n"
                                                        '        frame = storage_binary(state, '
                                                        "frame, 'd7', frame.d1, 16, 'or')\n"
                                                        '    frame = storage_shift(state, frame, '
                                                        "'d7', low16(frame.d4), 32)\n"
                                                        '    frame = storage_binary(state, frame, '
                                                        "'d7', frame.d3, 16, 'or')\n"
                                                        '    frame = storage_arithmetic(state, '
                                                        "frame, 'd4', 22, 16)\n"
                                                        '    frame = '
                                                        '_storage_flush_word_residue_fields(state, '
                                                        "frame, 'd7')\n"
                                                        '    frame = storage_move(state, frame, '
                                                        "'d3', frame.d7, 16)\n"
                                                        '    frame, again = storage_dbra(frame, '
                                                        "'d0')\n"
                                                        '    if not again:\n'
                                                        '        break\n'
                                                        'frame = storage_logic(state, frame, '
                                                        'frame.d4, 16)\n'
                                                        'if not frame.status_word & 4:\n'
                                                        '    frame = storage_write_next(state, '
                                                        "frame, 'a0', 1, frame.d7)\n"
                                                        '    frame = storage_address_step(frame, '
                                                        "'a0', 1)\n"
                                                        'return frame',
                                                'returns': 'StorageFrame',
                                                'signature': 'state: StorageState, frame: '
                                                             'StorageFrame'},
 'write_saved_state_checksum': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                        'returned = write_saved_state_checksum_frame_fields(state, '
                                        'frame)\n'
                                        'return returned.d1',
                                'returns': 'Long',
                                'signature': 'state: StorageState, entry_frame: StorageFrame=None'},
 'write_saved_state_checksum_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                     'frame = storage_call(state, frame, '
                                                     'checksum_saved_payload_frame_fields, 35330)\n'
                                                     'for address, following_bits in ((2097421, '
                                                     '32), (2097423, 32), (2097425, 16)):\n'
                                                     '    frame = storage_write(state, frame, '
                                                     'address, 1, frame.d1)\n'
                                                     '    frame = storage_shift(state, frame, '
                                                     "'d1', 8, following_bits, True)\n"
                                                     'return storage_write(state, frame, 2097427, '
                                                     '1, frame.d1)',
                                             'returns': 'StorageFrame',
                                             'signature': 'state: StorageState, frame: '
                                                          'StorageFrame'}})
APPROVED.setdefault('business_load', set()).update(('refresh_loaded_group_attributes_frame_fields',))
APPROVED.setdefault('contexts_storage_fields', set()).update(('StorageFrame', 'storage_address', 'storage_address_step', 'storage_arithmetic', 'storage_binary', 'storage_call', 'storage_compare_value', 'storage_dbra', 'storage_entry', 'storage_legacy_entry', 'storage_logic', 'storage_move', 'storage_read_next', 'storage_replace', 'storage_shift', 'storage_swap', 'storage_write', 'storage_write_next'))
APPROVED.setdefault('contexts_streams', set()).update(('BitReader', 'BitWriter', 'FixedFieldReadContext', 'checked_buffer'))
APPROVED.setdefault('domain', set()).update(('Boundary', 'CarryOutcome', 'Cursor', 'Long', 'StorageState', 'Table', 'Word', 'checked_cursor', 'checked_table', 'low16', 's16'))
