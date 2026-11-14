"""Restricted save source admission and ordinary storage target emission.

No original ROM/ASM/object or bytecode payload is a generation input.
Supported structural source only, not independent behavior acceptance.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import SAVE_BINDINGS

APPROVED = {'business_streams': {'write_masked_fixed_count_fields',
                      'write_packed_group_stream',
                      'write_packed_transport_orders',
                      'write_saved_state_checksum'},
 'contexts_save': {'SavedForceColumnContext'},
 'domain': {'StorageState', 'u32', 'low16', 'Cursor', 'divu_retained', 'checked_state', 'Long'}}

DECLARATIONS = {'write_saved_game_state': {'signature': 'state: StorageState',
                            'returns': 'Long',
                            'flow': 'checked_state(state)\n'
                                    'state.write(2097413, 1, 83)\n'
                                    'state.write(2097415, 1, 69)\n'
                                    'state.write(2097417, 1, 71)\n'
                                    'state.write(2097419, 1, 65)\n'
                                    "state.write(2097429, 1, state.scalar('metadata_f67b'))\n"
                                    "state.write(2097431, 1, state.scalar('metadata_f67d'))\n"
                                    "state.write(2097433, 1, state.scalar('metadata_f67f'))\n"
                                    "state.write(2097435, 1, state.scalar('metadata_f374'))\n"
                                    "state.write(2097437, 1, state.scalar('metadata_f375'))\n"
                                    "state.write(2097439, 1, state.scalar('metadata_efd3'))\n"
                                    "state.write(2097441, 1, state.scalar('metadata_efe5'))\n"
                                    "state.write(2097443, 1, state.scalar('metadata_efd7'))\n"
                                    "state.write(2097445, 1, state.scalar('metadata_efd9'))\n"
                                    'destination = state.table(2097447).cursor()\n'
                                    'write_masked_fixed_count_fields(state, state.ram_a000, '
                                    'destination, 5, 1, 40)\n'
                                    'source = state.ram_efaa.cursor()\n'
                                    'for _ in range(5):\n'
                                    '    destination.append_byte(source.next_byte())\n'
                                    '    destination.base = u32(destination.base + 1)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_a028, '
                                    'destination, 8, 1, 40)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_a050, '
                                    'destination, 8, 1, 256)\n'
                                    'stage_saved_officer_positions(state)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_d300, '
                                    'destination, 8, 2, 256)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_d500, '
                                    'destination, 9, 2, 256)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_b200, '
                                    'destination, 8, 2, 256)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_b400, '
                                    'destination, 8, 2, 256)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_b600, '
                                    'destination, 8, 2, 256)\n'
                                    'stage_scaled_officer_parameter_words(state)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_d300, '
                                    'destination, 5, 2, 256)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_c000, '
                                    'destination, 10, 2, 256)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_be00, '
                                    'destination, 10, 2, 256)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_c200, '
                                    'destination, 7, 1, 256)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_c300, '
                                    'destination, 7, 1, 256)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_c400, '
                                    'destination, 5, 1, 256)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_c500, '
                                    'destination, 7, 1, 256)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_c700, '
                                    'destination, 5, 1, 256)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_c800, '
                                    'destination, 14, 4, 256)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_cc00, '
                                    'destination, 8, 1, 256)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_e000, '
                                    'destination, 20, 4, 40)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_e0a0, '
                                    'destination, 20, 4, 40)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_e140, '
                                    'destination, 10, 4, 40)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_e1e0, '
                                    'destination, 10, 4, 40)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_e280, '
                                    'destination, 7, 4, 40)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_e320, '
                                    'destination, 7, 4, 40)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_e3c0, '
                                    'destination, 7, 4, 40)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_e5a0, '
                                    'destination, 7, 4, 40)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_f428, '
                                    'destination, 4, 1, 40)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_e640, '
                                    'destination, 9, 2, 16)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_f460, '
                                    'destination, 9, 2, 40)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_e660, '
                                    'destination, 20, 4, 40)\n'
                                    'source = state.ram_e700.cursor()\n'
                                    'for _ in range(2):\n'
                                    '    destination.append_byte(source.next_byte())\n'
                                    '    destination.base = u32(destination.base + 1)\n'
                                    'source = state.ram_e710.cursor()\n'
                                    'for _ in range(32):\n'
                                    '    destination.append_byte(source.next_byte())\n'
                                    '    destination.base = u32(destination.base + 1)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_e778, '
                                    'destination, 17, 4, 40)\n'
                                    'stage_saved_city_orders(state)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_d300, '
                                    'destination, 9, 2, 40)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_d300.at(80), '
                                    'destination, 14, 2, 40)\n'
                                    'write_masked_fixed_count_fields(state, '
                                    'state.ram_d300.at(160), destination, 9, 2, 40)\n'
                                    'write_masked_fixed_count_fields(state, '
                                    'state.ram_d300.at(240), destination, 7, 2, 40)\n'
                                    'write_masked_fixed_count_fields(state, '
                                    'state.ram_d300.at(320), destination, 9, 2, 40)\n'
                                    'write_masked_fixed_count_fields(state, '
                                    'state.ram_d300.at(400), destination, 10, 2, 40)\n'
                                    'stage_saved_force_record_columns(state, '
                                    'SavedForceColumnContext(state.ram_e9f8.cursor()))\n'
                                    'write_masked_fixed_count_fields(state, state.ram_d300, '
                                    'destination, 6, 1, 16)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_d300.at(16), '
                                    'destination, 6, 1, 16)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_d300.at(32), '
                                    'destination, 8, 1, 16)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_d300.at(48), '
                                    'destination, 4, 1, 16)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_ea38, '
                                    'destination, 1, 1, 40)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_ea88, '
                                    'destination, 2, 1, 768)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_ed88, '
                                    'destination, 18, 4, 40)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_ee28, '
                                    'destination, 20, 4, 40)\n'
                                    'write_masked_fixed_count_fields(state, state.ram_f590, '
                                    'destination, 2, 1, 16)\n'
                                    'write_packed_transport_orders(state, destination)\n'
                                    'write_packed_group_stream(state, destination)\n'
                                    'return write_saved_state_checksum(state)'},
 'stage_saved_officer_positions': {'signature': 'state: StorageState',
                                   'returns': 'None',
                                   'flow': 'checked_state(state)\n'
                                           'source = state.ram_a150.cursor()\n'
                                           'first_column = state.ram_d300.cursor()\n'
                                           'second_column = state.ram_d500.cursor()\n'
                                           'for _ in range(256):\n'
                                           '    first_column.append_word(source.next_word() >> 7)\n'
                                           '    second_column.append_word(source.next_word() >> 7)',
                                   'slots': {7: ('position_shift', 1, 8)}},
 'stage_saved_city_orders': {'signature': 'state: StorageState',
                             'returns': 'None',
                             'flow': 'checked_state(state)\n'
                                     'source = state.ram_e818.cursor()\n'
                                     'destination = state.ram_d300.cursor()\n'
                                     'for _ in range(40):\n'
                                     '    destination.set_word(0, source.next_word())\n'
                                     '    destination.set_word(0, source.next_word(), 80)\n'
                                     '    destination.set_word(0, source.next_word(), 160)\n'
                                     '    field = source.next_word()\n'
                                     '    if field != 65535:\n'
                                     '        field = low16(divu_retained(field, 100))\n'
                                     '    destination.set_word(0, field, 240)\n'
                                     '    destination.set_word(0, source.next_word(), 320)\n'
                                     '    destination.set_word(0, source.next_word(), 400)\n'
                                     '    destination.base = u32(destination.base + 2)'},
 'stage_scaled_officer_parameter_words': {'signature': 'state: StorageState',
                                          'returns': 'None',
                                          'flow': 'checked_state(state)\n'
                                                  'source = state.ram_b800.cursor()\n'
                                                  'destination = state.ram_d300.cursor()\n'
                                                  'for _ in range(256):\n'
                                                  '    '
                                                  'destination.append_word(low16(divu_retained(source.next_word(), '
                                                  '5)))'},
 'stage_saved_force_record_columns': {'signature': 'state: StorageState, context: '
                                                   'SavedForceColumnContext',
                                      'returns': 'Cursor',
                                      'flow': 'checked_state(state)\n'
                                              'if type(context) is not SavedForceColumnContext:\n'
                                              "    raise ValueError('typed saved-force column "
                                              "context required')\n"
                                              'context.checked_for(state)\n'
                                              'source = context.source\n'
                                              'first_column = state.ram_d300.cursor()\n'
                                              'second_column = state.ram_d300.cursor(16)\n'
                                              'third_column = state.ram_d300.cursor(32)\n'
                                              'fourth_column = state.ram_d300.cursor(48)\n'
                                              'for _ in range(16):\n'
                                              '    first_column.append_byte(source.next_byte())\n'
                                              '    second_column.append_byte(source.next_byte())\n'
                                              '    third_column.append_byte(source.next_byte())\n'
                                              '    fourth_column.append_byte(source.next_byte())\n'
                                              'return source'}}

def _lower_write_saved_game_state(e,rules):
    e.label('storage_pc_0083fa')
    e.ins('move.b','#0x53,0x200105:l',8)
    e.label('storage_pc_008402')
    e.ins('move.b','#0x45,0x200107:l',8)
    e.label('storage_pc_00840a')
    e.ins('move.b','#0x47,0x200109:l',8)
    e.label('storage_pc_008412')
    e.ins('move.b','#0x41,0x20010b:l',8)
    e.label('storage_pc_00841a')
    e.ins('move.b','0xf67b:w,0x200115:l',8)
    e.label('storage_pc_008422')
    e.ins('move.b','0xf67d:w,0x200117:l',8)
    e.label('storage_pc_00842a')
    e.ins('move.b','0xf67f:w,0x200119:l',8)
    e.label('storage_pc_008432')
    e.ins('move.b','0xf374:w,0x20011b:l',8)
    e.label('storage_pc_00843a')
    e.ins('move.b','0xf375:w,0x20011d:l',8)
    e.label('storage_pc_008442')
    e.ins('move.b','0xefd3:w,0x20011f:l',8)
    e.label('storage_pc_00844a')
    e.ins('move.b','0xefe5:w,0x200121:l',8)
    e.label('storage_pc_008452')
    e.ins('move.b','0xefd7:w,0x200123:l',8)
    e.label('storage_pc_00845a')
    e.ins('move.b','0xefd9:w,0x200125:l',8)
    e.label('storage_pc_008462')
    e.ins('movea.l','#0x200127,%a0',6)
    e.label('storage_pc_008468')
    e.ins('lea.l','0xa000:w,%a1',4)
    e.label('storage_pc_00846c')
    e.ins('move.w','#0x5,%d0',4)
    e.label('storage_pc_008470')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008474')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008478')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_00847c')
    e.ins('lea.l','0xefaa:w,%a1',4)
    e.label('storage_pc_008480')
    e.ins('move.b','(%a1)+,(%a0)+',2)
    e.label('storage_pc_008482')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_008486')
    e.ins('move.b','(%a1)+,(%a0)+',2)
    e.label('storage_pc_008488')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_00848c')
    e.ins('move.b','(%a1)+,(%a0)+',2)
    e.label('storage_pc_00848e')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_008492')
    e.ins('move.b','(%a1)+,(%a0)+',2)
    e.label('storage_pc_008494')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_008498')
    e.ins('move.b','(%a1)+,(%a0)+',2)
    e.label('storage_pc_00849a')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_00849e')
    e.ins('lea.l','0xa028:w,%a1',4)
    e.label('storage_pc_0084a2')
    e.ins('move.w','#0x8,%d0',4)
    e.label('storage_pc_0084a6')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_0084aa')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_0084ae')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_0084b2')
    e.ins('lea.l','0xa050:w,%a1',4)
    e.label('storage_pc_0084b6')
    e.ins('move.w','#0x8,%d0',4)
    e.label('storage_pc_0084ba')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_0084be')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_0084c2')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_0084c6')
    e.ins('bsr.w','storage_pc_008866',4)
    e.label('storage_pc_0084ca')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('storage_pc_0084ce')
    e.ins('move.w','#0x8,%d0',4)
    e.label('storage_pc_0084d2')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_0084d6')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_0084da')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_0084de')
    e.ins('lea.l','0xd500:w,%a1',4)
    e.label('storage_pc_0084e2')
    e.ins('move.w','#0x9,%d0',4)
    e.label('storage_pc_0084e6')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_0084ea')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_0084ee')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_0084f2')
    e.ins('lea.l','0xb200:w,%a1',4)
    e.label('storage_pc_0084f6')
    e.ins('move.w','#0x8,%d0',4)
    e.label('storage_pc_0084fa')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_0084fe')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008502')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_008506')
    e.ins('lea.l','0xb400:w,%a1',4)
    e.label('storage_pc_00850a')
    e.ins('move.w','#0x8,%d0',4)
    e.label('storage_pc_00850e')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008512')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008516')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_00851a')
    e.ins('lea.l','0xb600:w,%a1',4)
    e.label('storage_pc_00851e')
    e.ins('move.w','#0x8,%d0',4)
    e.label('storage_pc_008522')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008526')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_00852a')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_00852e')
    e.ins('bsr.w','storage_pc_00892a',4)
    e.label('storage_pc_008532')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('storage_pc_008536')
    e.ins('move.w','#0x5,%d0',4)
    e.label('storage_pc_00853a')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_00853e')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008542')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_008546')
    e.ins('lea.l','0xc000:w,%a1',4)
    e.label('storage_pc_00854a')
    e.ins('move.w','#0xa,%d0',4)
    e.label('storage_pc_00854e')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008552')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008556')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_00855a')
    e.ins('lea.l','0xbe00:w,%a1',4)
    e.label('storage_pc_00855e')
    e.ins('move.w','#0xa,%d0',4)
    e.label('storage_pc_008562')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008566')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_00856a')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_00856e')
    e.ins('lea.l','0xc200:w,%a1',4)
    e.label('storage_pc_008572')
    e.ins('move.w','#0x7,%d0',4)
    e.label('storage_pc_008576')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_00857a')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_00857e')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_008582')
    e.ins('lea.l','0xc300:w,%a1',4)
    e.label('storage_pc_008586')
    e.ins('move.w','#0x7,%d0',4)
    e.label('storage_pc_00858a')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_00858e')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008592')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_008596')
    e.ins('lea.l','0xc400:w,%a1',4)
    e.label('storage_pc_00859a')
    e.ins('move.w','#0x5,%d0',4)
    e.label('storage_pc_00859e')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_0085a2')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_0085a6')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_0085aa')
    e.ins('lea.l','0xc500:w,%a1',4)
    e.label('storage_pc_0085ae')
    e.ins('move.w','#0x7,%d0',4)
    e.label('storage_pc_0085b2')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_0085b6')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_0085ba')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_0085be')
    e.ins('lea.l','0xc700:w,%a1',4)
    e.label('storage_pc_0085c2')
    e.ins('move.w','#0x5,%d0',4)
    e.label('storage_pc_0085c6')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_0085ca')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_0085ce')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_0085d2')
    e.ins('lea.l','0xc800:w,%a1',4)
    e.label('storage_pc_0085d6')
    e.ins('move.w','#0xe,%d0',4)
    e.label('storage_pc_0085da')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_0085de')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_0085e2')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_0085e6')
    e.ins('lea.l','0xcc00:w,%a1',4)
    e.label('storage_pc_0085ea')
    e.ins('move.w','#0x8,%d0',4)
    e.label('storage_pc_0085ee')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_0085f2')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_0085f6')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_0085fa')
    e.ins('lea.l','0xe000:w,%a1',4)
    e.label('storage_pc_0085fe')
    e.ins('move.w','#0x14,%d0',4)
    e.label('storage_pc_008602')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008606')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_00860a')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_00860e')
    e.ins('lea.l','0xe0a0:w,%a1',4)
    e.label('storage_pc_008612')
    e.ins('move.w','#0x14,%d0',4)
    e.label('storage_pc_008616')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_00861a')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_00861e')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_008622')
    e.ins('lea.l','0xe140:w,%a1',4)
    e.label('storage_pc_008626')
    e.ins('move.w','#0xa,%d0',4)
    e.label('storage_pc_00862a')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_00862e')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008632')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_008636')
    e.ins('lea.l','0xe1e0:w,%a1',4)
    e.label('storage_pc_00863a')
    e.ins('move.w','#0xa,%d0',4)
    e.label('storage_pc_00863e')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008642')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008646')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_00864a')
    e.ins('lea.l','0xe280:w,%a1',4)
    e.label('storage_pc_00864e')
    e.ins('move.w','#0x7,%d0',4)
    e.label('storage_pc_008652')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008656')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_00865a')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_00865e')
    e.ins('lea.l','0xe320:w,%a1',4)
    e.label('storage_pc_008662')
    e.ins('move.w','#0x7,%d0',4)
    e.label('storage_pc_008666')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_00866a')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_00866e')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_008672')
    e.ins('lea.l','0xe3c0:w,%a1',4)
    e.label('storage_pc_008676')
    e.ins('move.w','#0x7,%d0',4)
    e.label('storage_pc_00867a')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_00867e')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008682')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_008686')
    e.ins('lea.l','0xe5a0:w,%a1',4)
    e.label('storage_pc_00868a')
    e.ins('move.w','#0x7,%d0',4)
    e.label('storage_pc_00868e')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008692')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008696')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_00869a')
    e.ins('lea.l','0xf428:w,%a1',4)
    e.label('storage_pc_00869e')
    e.ins('move.w','#0x4,%d0',4)
    e.label('storage_pc_0086a2')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_0086a6')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_0086aa')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_0086ae')
    e.ins('lea.l','0xe640:w,%a1',4)
    e.label('storage_pc_0086b2')
    e.ins('move.w','#0x9,%d0',4)
    e.label('storage_pc_0086b6')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_0086ba')
    e.ins('move.w','#0x10,%d2',4)
    e.label('storage_pc_0086be')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_0086c2')
    e.ins('lea.l','0xf460:w,%a1',4)
    e.label('storage_pc_0086c6')
    e.ins('move.w','#0x9,%d0',4)
    e.label('storage_pc_0086ca')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_0086ce')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_0086d2')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_0086d6')
    e.ins('lea.l','0xe660:w,%a1',4)
    e.label('storage_pc_0086da')
    e.ins('move.w','#0x14,%d0',4)
    e.label('storage_pc_0086de')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_0086e2')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_0086e6')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_0086ea')
    e.ins('move.b','0xe700:w,(%a0)+',4)
    e.label('storage_pc_0086ee')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_0086f2')
    e.ins('move.b','0xe701:w,(%a0)+',4)
    e.label('storage_pc_0086f6')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_0086fa')
    e.ins('lea.l','0xe710:w,%a1',4)
    e.label('storage_pc_0086fe')
    e.ins('move.w','#0x1f,%d2',4)
    e.label('storage_pc_008702')
    e.ins('move.b','(%a1)+,(%a0)+',2)
    e.label('storage_pc_008704')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_008708')
    e.ins('dbra','%d2,storage_pc_008702',4)
    e.label('storage_pc_00870c')
    e.ins('lea.l','0xe778:w,%a1',4)
    e.label('storage_pc_008710')
    e.ins('move.w','#0x11,%d0',4)
    e.label('storage_pc_008714')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008718')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_00871c')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_008720')
    e.ins('bsr.w','storage_pc_008888',4)
    e.label('storage_pc_008724')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('storage_pc_008728')
    e.ins('move.w','#0x9,%d0',4)
    e.label('storage_pc_00872c')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008730')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008734')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_008738')
    e.ins('lea.l','0xd350:w,%a1',4)
    e.label('storage_pc_00873c')
    e.ins('move.w','#0xe,%d0',4)
    e.label('storage_pc_008740')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008744')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008748')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_00874c')
    e.ins('lea.l','0xd3a0:w,%a1',4)
    e.label('storage_pc_008750')
    e.ins('move.w','#0x9,%d0',4)
    e.label('storage_pc_008754')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008758')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_00875c')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_008760')
    e.ins('lea.l','0xd3f0:w,%a1',4)
    e.label('storage_pc_008764')
    e.ins('move.w','#0x7,%d0',4)
    e.label('storage_pc_008768')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_00876c')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008770')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_008774')
    e.ins('lea.l','0xd440:w,%a1',4)
    e.label('storage_pc_008778')
    e.ins('move.w','#0x9,%d0',4)
    e.label('storage_pc_00877c')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008780')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008784')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_008788')
    e.ins('lea.l','0xd490:w,%a1',4)
    e.label('storage_pc_00878c')
    e.ins('move.w','#0xa,%d0',4)
    e.label('storage_pc_008790')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008794')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008798')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_00879c')
    e.ins('lea.l','0xe9f8:w,%a1',4)
    e.label('storage_pc_0087a0')
    e.ins('bsr.w','storage_pc_008a3e',4)
    e.label('storage_pc_0087a4')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('storage_pc_0087a8')
    e.ins('move.w','#0x6,%d0',4)
    e.label('storage_pc_0087ac')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_0087b0')
    e.ins('move.w','#0x10,%d2',4)
    e.label('storage_pc_0087b4')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_0087b8')
    e.ins('lea.l','0xd310:w,%a1',4)
    e.label('storage_pc_0087bc')
    e.ins('move.w','#0x6,%d0',4)
    e.label('storage_pc_0087c0')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_0087c4')
    e.ins('move.w','#0x10,%d2',4)
    e.label('storage_pc_0087c8')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_0087cc')
    e.ins('lea.l','0xd320:w,%a1',4)
    e.label('storage_pc_0087d0')
    e.ins('move.w','#0x8,%d0',4)
    e.label('storage_pc_0087d4')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_0087d8')
    e.ins('move.w','#0x10,%d2',4)
    e.label('storage_pc_0087dc')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_0087e0')
    e.ins('lea.l','0xd330:w,%a1',4)
    e.label('storage_pc_0087e4')
    e.ins('move.w','#0x4,%d0',4)
    e.label('storage_pc_0087e8')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_0087ec')
    e.ins('move.w','#0x10,%d2',4)
    e.label('storage_pc_0087f0')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_0087f4')
    e.ins('lea.l','0xea38:w,%a1',4)
    e.label('storage_pc_0087f8')
    e.ins('move.w','#0x1,%d0',4)
    e.label('storage_pc_0087fc')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008800')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008804')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_008808')
    e.ins('lea.l','0xea88:w,%a1',4)
    e.label('storage_pc_00880c')
    e.ins('move.w','#0x2,%d0',4)
    e.label('storage_pc_008810')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008814')
    e.ins('move.w','#0x300,%d2',4)
    e.label('storage_pc_008818')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_00881c')
    e.ins('lea.l','0xed88:w,%a1',4)
    e.label('storage_pc_008820')
    e.ins('move.w','#0x12,%d0',4)
    e.label('storage_pc_008824')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008828')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_00882c')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_008830')
    e.ins('lea.l','0xee28:w,%a1',4)
    e.label('storage_pc_008834')
    e.ins('move.w','#0x14,%d0',4)
    e.label('storage_pc_008838')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_00883c')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008840')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_008844')
    e.ins('lea.l','0xf590:w,%a1',4)
    e.label('storage_pc_008848')
    e.ins('move.w','#0x2,%d0',4)
    e.label('storage_pc_00884c')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008850')
    e.ins('move.w','#0x10,%d2',4)
    e.label('storage_pc_008854')
    e.ins('bsr.w','storage_pc_00922a',4)
    e.label('storage_pc_008858')
    e.ins('bsr.w','storage_pc_0088c6',4)
    e.label('storage_pc_00885c')
    e.ins('bsr.w','storage_pc_008946',4)
    e.label('storage_pc_008860')
    e.ins('bsr.w','storage_pc_0089fe',4)
    e.label('storage_pc_008864')
    e.ins('rts','',2)

def _lower_stage_saved_officer_positions(e,rules):
    e.label('storage_pc_008866')
    e.ins('lea.l','0xa150:w,%a2',4)
    e.label('storage_pc_00886a')
    e.ins('lea.l','0xd300:w,%a3',4)
    e.label('storage_pc_00886e')
    e.ins('lea.l','0xd500:w,%a4',4)
    e.label('storage_pc_008872')
    e.ins('move.w','#0xff,%d0',4)
    e.label('storage_pc_008876')
    e.ins('move.w','(%a2)+,%d1',2)
    e.label('storage_pc_008878')
    e.ins('lsr.w','#'+hex(rules['position_shift'])+',%d1',2)
    e.label('storage_pc_00887a')
    e.ins('move.w','%d1,(%a3)+',2)
    e.label('storage_pc_00887c')
    e.ins('move.w','(%a2)+,%d1',2)
    e.label('storage_pc_00887e')
    e.ins('lsr.w','#'+hex(rules['position_shift'])+',%d1',2)
    e.label('storage_pc_008880')
    e.ins('move.w','%d1,(%a4)+',2)
    e.label('storage_pc_008882')
    e.ins('dbra','%d0,storage_pc_008876',4)
    e.label('storage_pc_008886')
    e.ins('rts','',2)

def _lower_stage_saved_city_orders(e,rules):
    e.label('storage_pc_008888')
    e.ins('lea.l','0xe818:w,%a1',4)
    e.label('storage_pc_00888c')
    e.ins('lea.l','0xd300:w,%a2',4)
    e.label('storage_pc_008890')
    e.ins('move.w','#0x27,%d0',4)
    e.label('storage_pc_008894')
    e.ins('move.w','(%a1)+,(%a2)',2)
    e.label('storage_pc_008896')
    e.ins('move.w','(%a1)+,0x50(%a2)',4)
    e.label('storage_pc_00889a')
    e.ins('move.w','(%a1)+,0xa0(%a2)',4)
    e.label('storage_pc_00889e')
    e.ins('move.w','(%a1)+,%d1',2)
    e.label('storage_pc_0088a0')
    e.ins('cmpi.w','#0xffff,%d1',4)
    e.label('storage_pc_0088a4')
    e.ins('beq.w','storage_pc_0088b2',4)
    e.label('storage_pc_0088a8')
    e.ins('andi.l','#0xffff,%d1',6)
    e.label('storage_pc_0088ae')
    e.ins('divu.w','#0x64,%d1',4)
    e.label('storage_pc_0088b2')
    e.ins('move.w','%d1,0xf0(%a2)',4)
    e.label('storage_pc_0088b6')
    e.ins('move.w','(%a1)+,0x140(%a2)',4)
    e.label('storage_pc_0088ba')
    e.ins('move.w','(%a1)+,0x190(%a2)',4)
    e.label('storage_pc_0088be')
    e.ins('addq.w','#0x2,%a2',2)
    e.label('storage_pc_0088c0')
    e.ins('dbra','%d0,storage_pc_008894',4)
    e.label('storage_pc_0088c4')
    e.ins('rts','',2)

def _lower_stage_scaled_officer_parameter_words(e,rules):
    e.label('storage_pc_00892a')
    e.ins('lea.l','0xb800:w,%a1',4)
    e.label('storage_pc_00892e')
    e.ins('lea.l','0xd300:w,%a2',4)
    e.label('storage_pc_008932')
    e.ins('move.w','#0xff,%d0',4)
    e.label('storage_pc_008936')
    e.ins('moveq','#0,%d1',2)
    e.label('storage_pc_008938')
    e.ins('move.w','(%a1)+,%d1',2)
    e.label('storage_pc_00893a')
    e.ins('divu.w','#0x5,%d1',4)
    e.label('storage_pc_00893e')
    e.ins('move.w','%d1,(%a2)+',2)
    e.label('storage_pc_008940')
    e.ins('dbra','%d0,storage_pc_008936',4)
    e.label('storage_pc_008944')
    e.ins('rts','',2)

def _lower_stage_saved_force_record_columns(e,rules):
    e.label('storage_pc_008a3e')
    e.ins('lea.l','0xd300:w,%a2',4)
    e.label('storage_pc_008a42')
    e.ins('lea.l','0xd310:w,%a3',4)
    e.label('storage_pc_008a46')
    e.ins('lea.l','0xd320:w,%a4',4)
    e.label('storage_pc_008a4a')
    e.ins('lea.l','0xd330:w,%a5',4)
    e.label('storage_pc_008a4e')
    e.ins('move.w','#0xf,%d0',4)
    e.label('storage_pc_008a52')
    e.ins('move.b','(%a1)+,(%a2)+',2)
    e.label('storage_pc_008a54')
    e.ins('move.b','(%a1)+,(%a3)+',2)
    e.label('storage_pc_008a56')
    e.ins('move.b','(%a1)+,(%a4)+',2)
    e.label('storage_pc_008a58')
    e.ins('move.b','(%a1)+,(%a5)+',2)
    e.label('storage_pc_008a5a')
    e.ins('dbra','%d0,storage_pc_008a52',4)
    e.label('storage_pc_008a5e')
    e.ins('rts','',2)

LOWERERS = {
    'write_saved_game_state':_lower_write_saved_game_state,
    'stage_saved_officer_positions':_lower_stage_saved_officer_positions,
    'stage_saved_city_orders':_lower_stage_saved_city_orders,
    'stage_scaled_officer_parameter_words':_lower_stage_scaled_officer_parameter_words,
    'stage_saved_force_record_columns':_lower_stage_saved_force_record_columns,
}

def compile_save(source):
    """Admit complete current fields and use untouched physical lowerers.

    This bounded frontend is not a generic Python editor or CPU proof.
    The legacy scalar phase inliner is deliberately not used on the
    complete field source; all actual functions share one declaration
    authority, including real child-slot/flag helpers.
    """
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    current_fields = {'stage_saved_city_orders': 'stage_saved_city_orders_frame_fields',
     'stage_saved_force_record_columns': 'stage_saved_force_record_columns_frame_fields',
     'stage_saved_officer_positions': 'stage_saved_officer_positions_frame_fields',
     'stage_scaled_officer_parameter_words': 'stage_scaled_officer_parameter_words_frame_fields',
     'write_saved_game_state': 'write_saved_game_state_frame_fields'}
    selected = {}
    for binding in SAVE_BINDINGS:
        actual = records[current_fields[binding.name]]
        selected[binding.name] = dict(name=binding.name, rules=actual['rules'], effects=actual['effects'])
    return lower_declared(selected, SAVE_BINDINGS, LOWERERS)

# C54 complete storage-field authority; no ordinary lowerer or common guard change.
DECLARATIONS.update({'_write_saved_column_fields': {'flow': 'source, field_bits, stride, count, continuation = column\n'
                                        "frame = storage_address(frame, 'a1', source)\n"
                                        "frame = storage_move(state, frame, 'd0', field_bits, 16)\n"
                                        "frame = storage_move(state, frame, 'd1', stride, 16)\n"
                                        "frame = storage_move(state, frame, 'd2', count, 16)\n"
                                        'return storage_call(state, frame, '
                                        'write_masked_fixed_count_frame_fields, continuation)',
                                'returns': 'StorageFrame',
                                'signature': 'state: StorageState, frame: StorageFrame, column: '
                                             'tuple'},
 '_write_saved_columns_fields': {'flow': 'for column in columns:\n'
                                         '    frame = _write_saved_column_fields(state, frame, '
                                         'column)\n'
                                         'return frame',
                                 'returns': 'StorageFrame',
                                 'signature': 'state: StorageState, frame: StorageFrame, columns: '
                                              'tuple'},
 'begin_saved_payload': {'flow': "raise Boundary('legacy partial storage phase has no whole entry; "
                                 "use the full save or restore core')",
                         'returns': 'Cursor',
                         'signature': 'state: StorageState, entry_frame: StorageFrame=None'},
 'stage_saved_city_orders': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                     'returned = stage_saved_city_orders_frame_fields(state, '
                                     'frame)\n'
                                     'return None',
                             'returns': 'None',
                             'signature': 'state: StorageState, entry_frame: StorageFrame=None'},
 'stage_saved_city_orders_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                  "frame = storage_address(frame, 'a1', "
                                                  '4294961176)\n'
                                                  "frame = storage_address(frame, 'a2', "
                                                  '4294955776)\n'
                                                  "frame = storage_move(state, frame, 'd0', 39, "
                                                  '16)\n'
                                                  'while True:\n'
                                                  '    for displacement in (0, 80, 160):\n'
                                                  '        frame, value = storage_read_next(state, '
                                                  "frame, 'a1', 2)\n"
                                                  '        frame = storage_write(state, frame, '
                                                  'frame.a2 + displacement, 2, value)\n'
                                                  '    frame, value = storage_read_next(state, '
                                                  "frame, 'a1', 2)\n"
                                                  "    frame = storage_move(state, frame, 'd1', "
                                                  'value, 16)\n'
                                                  '    frame = storage_arithmetic(state, frame, '
                                                  "'d1', 65535, 16, True, True)\n"
                                                  '    if low16(frame.d1) != 65535:\n'
                                                  '        frame = storage_binary(state, frame, '
                                                  "'d1', 65535, 32, 'and')\n"
                                                  '        frame = storage_divide(state, frame, '
                                                  "'d1', 100)\n"
                                                  '    frame = storage_write(state, frame, '
                                                  'frame.a2 + 240, 2, frame.d1)\n'
                                                  '    for displacement in (320, 400):\n'
                                                  '        frame, value = storage_read_next(state, '
                                                  "frame, 'a1', 2)\n"
                                                  '        frame = storage_write(state, frame, '
                                                  'frame.a2 + displacement, 2, value)\n'
                                                  "    frame = storage_address_step(frame, 'a2', "
                                                  '2)\n'
                                                  "    frame, again = storage_dbra(frame, 'd0')\n"
                                                  '    if not again:\n'
                                                  '        return frame',
                                          'returns': 'StorageFrame',
                                          'signature': 'state: StorageState, frame: StorageFrame'},
 'stage_saved_force_record_columns': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                              'context.checked_for(state)\n'
                                              'if context.source.base != frame.a1:\n'
                                              "    raise ValueError('save force source differs "
                                              "from complete entry A1')\n"
                                              'returned = '
                                              'stage_saved_force_record_columns_frame_fields(state, '
                                              'frame)\n'
                                              'context.source.base = returned.a1\n'
                                              'return context.source',
                                      'returns': 'Cursor',
                                      'signature': 'state: StorageState, context: '
                                                   'SavedForceColumnContext, entry_frame: '
                                                   'StorageFrame=None'},
 'stage_saved_force_record_columns_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                           "for role, address in (('a2', "
                                                           "4294955776), ('a3', 4294955792), "
                                                           "('a4', 4294955808), ('a5', "
                                                           '4294955824)):\n'
                                                           '    frame = storage_address(frame, '
                                                           'role, address)\n'
                                                           'frame = storage_move(state, frame, '
                                                           "'d0', 15, 16)\n"
                                                           'while True:\n'
                                                           "    for destination in ('a2', 'a3', "
                                                           "'a4', 'a5'):\n"
                                                           '        frame, value = '
                                                           "storage_read_next(state, frame, 'a1', "
                                                           '1)\n'
                                                           '        frame = '
                                                           'storage_write_next(state, frame, '
                                                           'destination, 1, value)\n'
                                                           '    frame, again = storage_dbra(frame, '
                                                           "'d0')\n"
                                                           '    if not again:\n'
                                                           '        return frame',
                                                   'returns': 'StorageFrame',
                                                   'signature': 'state: StorageState, frame: '
                                                                'StorageFrame'},
 'stage_saved_officer_positions': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                           'returned = '
                                           'stage_saved_officer_positions_frame_fields(state, '
                                           'frame)\n'
                                           'return None',
                                   'returns': 'None',
                                   'signature': 'state: StorageState, entry_frame: '
                                                'StorageFrame=None'},
 'stage_saved_officer_positions_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                        "frame = storage_address(frame, 'a2', "
                                                        '4294943056)\n'
                                                        "frame = storage_address(frame, 'a3', "
                                                        '4294955776)\n'
                                                        "frame = storage_address(frame, 'a4', "
                                                        '4294956288)\n'
                                                        "frame = storage_move(state, frame, 'd0', "
                                                        '255, 16)\n'
                                                        'while True:\n'
                                                        "    for destination in ('a3', 'a4'):\n"
                                                        '        frame, coordinate = '
                                                        "storage_read_next(state, frame, 'a2', 2)\n"
                                                        '        frame = storage_move(state, '
                                                        "frame, 'd1', coordinate, 16)\n"
                                                        '        frame = storage_shift(state, '
                                                        "frame, 'd1', 7, 16, True)\n"
                                                        '        frame = storage_write_next(state, '
                                                        'frame, destination, 2, frame.d1)\n'
                                                        '    frame, again = storage_dbra(frame, '
                                                        "'d0')\n"
                                                        '    if not again:\n'
                                                        '        return frame',
                                                'returns': 'StorageFrame',
                                                'signature': 'state: StorageState, frame: '
                                                             'StorageFrame',
                                                'slots': {7: ('position_shift', 1, 8)}},
 'stage_scaled_officer_parameter_words': {'flow': 'frame = storage_legacy_entry(state, '
                                                  'entry_frame)\n'
                                                  'returned = '
                                                  'stage_scaled_officer_parameter_words_frame_fields(state, '
                                                  'frame)\n'
                                                  'return None',
                                          'returns': 'None',
                                          'signature': 'state: StorageState, entry_frame: '
                                                       'StorageFrame=None'},
 'stage_scaled_officer_parameter_words_frame_fields': {'flow': 'frame = storage_entry(state, '
                                                               'frame)\n'
                                                               'frame = storage_address(frame, '
                                                               "'a1', 4294948864)\n"
                                                               'frame = storage_address(frame, '
                                                               "'a2', 4294955776)\n"
                                                               'frame = storage_move(state, frame, '
                                                               "'d0', 255, 16)\n"
                                                               'while True:\n'
                                                               '    frame = storage_move(state, '
                                                               "frame, 'd1', 0, 32)\n"
                                                               '    frame, value = '
                                                               'storage_read_next(state, frame, '
                                                               "'a1', 2)\n"
                                                               '    frame = storage_move(state, '
                                                               "frame, 'd1', value, 16)\n"
                                                               '    frame = storage_divide(state, '
                                                               "frame, 'd1', 5)\n"
                                                               '    frame = '
                                                               'storage_write_next(state, frame, '
                                                               "'a2', 2, frame.d1)\n"
                                                               '    frame, again = '
                                                               "storage_dbra(frame, 'd0')\n"
                                                               '    if not again:\n'
                                                               '        return frame',
                                                       'returns': 'StorageFrame',
                                                       'signature': 'state: StorageState, frame: '
                                                                    'StorageFrame'},
 'write_saved_city_fields': {'flow': "raise Boundary('legacy partial storage phase has no whole "
                                     "entry; use the full save or restore core')",
                             'returns': 'None',
                             'signature': 'state: StorageState, destination: Cursor, entry_frame: '
                                          'StorageFrame=None'},
 'write_saved_force_and_battle_fields': {'flow': "raise Boundary('legacy partial storage phase has "
                                                 'no whole entry; use the full save or restore '
                                                 "core')",
                                         'returns': 'None',
                                         'signature': 'state: StorageState, destination: Cursor, '
                                                      'entry_frame: StorageFrame=None'},
 'write_saved_game_state': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                    'returned = write_saved_game_state_frame_fields(state, frame)\n'
                                    'return returned.d1',
                            'returns': 'Long',
                            'signature': 'state: StorageState, entry_frame: StorageFrame=None'},
 'write_saved_game_state_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                 'for address, value in ((2097413, 83), (2097415, '
                                                 '69), (2097417, 71), (2097419, 65)):\n'
                                                 '    frame = storage_write(state, frame, address, '
                                                 '1, value)\n'
                                                 'for source, destination in ((4294964859, '
                                                 '2097429), (4294964861, 2097431), (4294964863, '
                                                 '2097433), (4294964084, 2097435), (4294964085, '
                                                 '2097437), (4294963155, 2097439), (4294963173, '
                                                 '2097441), (4294963159, 2097443), (4294963161, '
                                                 '2097445)):\n'
                                                 '    frame = storage_write(state, frame, '
                                                 'destination, 1, state.read(source, 1))\n'
                                                 "frame = storage_address(frame, 'a0', 2097447)\n"
                                                 'frame = _write_saved_column_fields(state, frame, '
                                                 '(4294942720, 5, 1, 40, 33916))\n'
                                                 "frame = storage_address(frame, 'a1', "
                                                 '4294963114)\n'
                                                 'for _ in range(5):\n'
                                                 '    frame, value = storage_read_next(state, '
                                                 "frame, 'a1', 1)\n"
                                                 '    frame = storage_write_next(state, frame, '
                                                 "'a0', 1, value)\n"
                                                 "    frame = storage_address_step(frame, 'a0', "
                                                 '1)\n'
                                                 'frame = _write_saved_columns_fields(state, '
                                                 'frame, ((4294942760, 8, 1, 40, 33970), '
                                                 '(4294942800, 8, 1, 256, 33990)))\n'
                                                 'frame = storage_call(state, frame, '
                                                 'stage_saved_officer_positions_frame_fields, '
                                                 '33994)\n'
                                                 'frame = _write_saved_columns_fields(state, '
                                                 'frame, ((4294955776, 8, 2, 256, 34014), '
                                                 '(4294956288, 9, 2, 256, 34034), (4294947328, 8, '
                                                 '2, 256, 34054), (4294947840, 8, 2, 256, 34074), '
                                                 '(4294948352, 8, 2, 256, 34094)))\n'
                                                 'frame = storage_call(state, frame, '
                                                 'stage_scaled_officer_parameter_words_frame_fields, '
                                                 '34098)\n'
                                                 'frame = _write_saved_columns_fields(state, '
                                                 'frame, ((4294955776, 5, 2, 256, 34118), '
                                                 '(4294950912, 10, 2, 256, 34138), (4294950400, '
                                                 '10, 2, 256, 34158), (4294951424, 7, 1, 256, '
                                                 '34178), (4294951680, 7, 1, 256, 34198), '
                                                 '(4294951936, 5, 1, 256, 34218), (4294952192, 7, '
                                                 '1, 256, 34238), (4294952704, 5, 1, 256, 34258), '
                                                 '(4294952960, 14, 4, 256, 34278), (4294953984, 8, '
                                                 '1, 256, 34298)))\n'
                                                 'frame = _write_saved_columns_fields(state, '
                                                 'frame, ((4294959104, 20, 4, 40, 34318), '
                                                 '(4294959264, 20, 4, 40, 34338), (4294959424, 10, '
                                                 '4, 40, 34358), (4294959584, 10, 4, 40, 34378), '
                                                 '(4294959744, 7, 4, 40, 34398), (4294959904, 7, '
                                                 '4, 40, 34418), (4294960064, 7, 4, 40, 34438), '
                                                 '(4294960544, 7, 4, 40, 34458), (4294964264, 4, '
                                                 '1, 40, 34478), (4294960704, 9, 2, 16, 34498), '
                                                 '(4294964320, 9, 2, 40, 34518), (4294960736, 20, '
                                                 '4, 40, 34538)))\n'
                                                 'for source in (4294960896, 4294960897):\n'
                                                 '    frame = storage_write_next(state, frame, '
                                                 "'a0', 1, state.read(source, 1))\n"
                                                 "    frame = storage_address_step(frame, 'a0', "
                                                 '1)\n'
                                                 "frame = storage_address(frame, 'a1', "
                                                 '4294960912)\n'
                                                 "frame = storage_move(state, frame, 'd2', 31, "
                                                 '16)\n'
                                                 'while True:\n'
                                                 '    frame, value = storage_read_next(state, '
                                                 "frame, 'a1', 1)\n"
                                                 '    frame = storage_write_next(state, frame, '
                                                 "'a0', 1, value)\n"
                                                 "    frame = storage_address_step(frame, 'a0', "
                                                 '1)\n'
                                                 "    frame, again = storage_dbra(frame, 'd2')\n"
                                                 '    if not again:\n'
                                                 '        break\n'
                                                 'frame = _write_saved_column_fields(state, frame, '
                                                 '(4294961016, 17, 4, 40, 34592))\n'
                                                 'frame = storage_call(state, frame, '
                                                 'stage_saved_city_orders_frame_fields, 34596)\n'
                                                 'frame = _write_saved_columns_fields(state, '
                                                 'frame, ((4294955776, 9, 2, 40, 34616), '
                                                 '(4294955856, 14, 2, 40, 34636), (4294955936, 9, '
                                                 '2, 40, 34656), (4294956016, 7, 2, 40, 34676), '
                                                 '(4294956096, 9, 2, 40, 34696), (4294956176, 10, '
                                                 '2, 40, 34716)))\n'
                                                 "frame = storage_address(frame, 'a1', "
                                                 '4294961656)\n'
                                                 'frame = storage_call(state, frame, '
                                                 'stage_saved_force_record_columns_frame_fields, '
                                                 '34724)\n'
                                                 'frame = _write_saved_columns_fields(state, '
                                                 'frame, ((4294955776, 6, 1, 16, 34744), '
                                                 '(4294955792, 6, 1, 16, 34764), (4294955808, 8, '
                                                 '1, 16, 34784), (4294955824, 4, 1, 16, 34804), '
                                                 '(4294961720, 1, 1, 40, 34824), (4294961800, 2, '
                                                 '1, 768, 34844), (4294962568, 18, 4, 40, 34864), '
                                                 '(4294962728, 20, 4, 40, 34884), (4294964624, 2, '
                                                 '1, 16, 34904)))\n'
                                                 'frame = storage_call(state, frame, '
                                                 'write_packed_transport_orders_frame_fields, '
                                                 '34908)\n'
                                                 'frame = storage_call(state, frame, '
                                                 'write_packed_group_stream_frame_fields, 34912)\n'
                                                 'return storage_call(state, frame, '
                                                 'write_saved_state_checksum_frame_fields, 34916)',
                                         'returns': 'StorageFrame',
                                         'signature': 'state: StorageState, frame: StorageFrame'},
 'write_saved_membership_fields': {'flow': "raise Boundary('legacy partial storage phase has no "
                                           "whole entry; use the full save or restore core')",
                                   'returns': 'None',
                                   'signature': 'state: StorageState, destination: Cursor, '
                                                'entry_frame: StorageFrame=None'},
 'write_saved_officer_fields': {'flow': "raise Boundary('legacy partial storage phase has no whole "
                                        "entry; use the full save or restore core')",
                                'returns': 'None',
                                'signature': 'state: StorageState, destination: Cursor, '
                                             'entry_frame: StorageFrame=None'},
 'write_saved_order_columns': {'flow': "raise Boundary('legacy partial storage phase has no whole "
                                       "entry; use the full save or restore core')",
                               'returns': 'None',
                               'signature': 'state: StorageState, destination: Cursor, '
                                            'entry_frame: StorageFrame=None'}})
APPROVED.setdefault('business_streams', set()).update(('write_masked_fixed_count_frame_fields', 'write_packed_group_stream_frame_fields', 'write_packed_transport_orders_frame_fields', 'write_saved_state_checksum_frame_fields'))
APPROVED.setdefault('contexts_save', set()).update(('SavedForceColumnContext',))
APPROVED.setdefault('contexts_storage_fields', set()).update(('StorageFrame', 'storage_address', 'storage_address_step', 'storage_arithmetic', 'storage_binary', 'storage_call', 'storage_dbra', 'storage_divide', 'storage_entry', 'storage_legacy_entry', 'storage_move', 'storage_read_next', 'storage_shift', 'storage_write', 'storage_write_next'))
APPROVED.setdefault('domain', set()).update(('Boundary', 'Cursor', 'Long', 'StorageState', 'low16'))
