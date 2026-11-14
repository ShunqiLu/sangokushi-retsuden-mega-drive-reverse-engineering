"""Restricted load source admission and ordinary storage target emission.

No original ROM/ASM/object or bytecode payload is a generation input.
Supported structural source only, not independent behavior acceptance.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import LOAD_BINDINGS

APPROVED = {'business_streams': {'read_masked_fixed_count_fields',
                      'read_packed_group_stream',
                      'read_packed_transport_orders',
                      'validate_saved_header_and_checksum'},
 'contexts_load': {'RestoreOutcome'},
 'domain': {'Byte',
            'Cursor',
            'StorageState',
            'checked_cursor',
            'checked_state',
            'descending_inclusive',
            'divu_retained',
            'low16',
            'low8',
            'u16',
            'uint'}}

DECLARATIONS = {'restore_saved_game_state': {'signature': 'state: StorageState',
                              'returns': 'RestoreOutcome',
                              'flow': 'checked_state(state)\n'
                                      'validated = validate_saved_header_and_checksum(state)\n'
                                      'if validated.carry != 0:\n'
                                      '    return RestoreOutcome(False, None)\n'
                                      'header = state.saved_metadata\n'
                                      "state.set_scalar('visible_force_first', 0)\n"
                                      "state.set_scalar('visible_force_first_low', "
                                      'header.byte(0))\n'
                                      "state.set_scalar('visible_force_second', 0)\n"
                                      "state.set_scalar('visible_force_second_low', "
                                      'header.byte(2))\n'
                                      "state.set_scalar('visible_force_third', 0)\n"
                                      "state.set_scalar('visible_force_third_low', "
                                      'header.byte(4))\n'
                                      "state.set_scalar('year_high_byte', header.byte(6))\n"
                                      "state.set_scalar('year_low_byte', header.byte(8))\n"
                                      "state.set_scalar('scenario_selector', 0)\n"
                                      "state.set_scalar('scenario_selector_low', header.byte(10))\n"
                                      "state.set_scalar('loaded_field_efe4', 0)\n"
                                      "state.set_scalar('loaded_field_efe4_low', header.byte(12))\n"
                                      "state.set_scalar('calendar_field_efd6', 0)\n"
                                      "state.set_scalar('calendar_field_efd6_low', "
                                      'header.byte(14))\n'
                                      "state.set_scalar('calendar_field_efd8', 0)\n"
                                      "state.set_scalar('calendar_field_efd8_low', "
                                      'header.byte(16))\n'
                                      'source = state.saved_game_fields.cursor()\n'
                                      'source = read_masked_fixed_count_fields(state, source, '
                                      'state.city_owner_tokens, 5, 1, 40)\n'
                                      'destination = state.loaded_state_bytes.cursor()\n'
                                      'for _ in range(5):\n'
                                      '    destination.append_byte(source.next_byte())\n'
                                      '    source.base = source.advance(1).base\n'
                                      'source = read_masked_fixed_count_fields(state, source, '
                                      'state.city_state_a028, 8, 1, 40)\n'
                                      'source = read_masked_fixed_count_fields(state, source, '
                                      'state.officer_city_tokens, 8, 1, 256)\n'
                                      'source = read_masked_fixed_count_fields(state, source, '
                                      'state.position_x_stage, 8, 2, 256)\n'
                                      'source = read_masked_fixed_count_fields(state, source, '
                                      'state.position_y_stage, 9, 2, 256)\n'
                                      'restore_saved_officer_positions(state)\n'
                                      'for destination, bit_width in ((state.officer_readiness, '
                                      '8), (state.officer_resolve, 8), (state.officer_strength, '
                                      '8), (state.position_x_stage, 5)):\n'
                                      '    source = read_masked_fixed_count_fields(state, source, '
                                      'destination, bit_width, 2, 256)\n'
                                      'restore_scaled_officer_parameter_words(state)\n'
                                      'for destination, bit_width, element_bytes in '
                                      '((state.officer_ability, 10, 2), (state.officer_progress, '
                                      '10, 2), (state.officer_disposition, 7, 1), '
                                      '(state.officer_loyalty, 7, 1), '
                                      '(state.officer_group_attribute, 5, 1), '
                                      '(state.officer_training, 7, 1), (state.officer_status, 5, '
                                      '1), (state.officer_troops, 14, 4), '
                                      '(state.officer_city_assignment, 8, 1)):\n'
                                      '    source = read_masked_fixed_count_fields(state, source, '
                                      'destination, bit_width, element_bytes, 256)\n'
                                      'for destination, bit_width in ((state.city_gold, 20), '
                                      '(state.city_food, 20), (state.city_parameter_e140, 10), '
                                      '(state.city_parameter_e1e0, 10), '
                                      '(state.city_parameter_e280, 7), (state.city_parameter_e320, '
                                      '7), (state.city_parameter_e3c0, 7), '
                                      '(state.city_parameter_e5a0, 7)):\n'
                                      '    source = read_masked_fixed_count_fields(state, source, '
                                      'destination, bit_width, 4, 40)\n'
                                      'source = read_masked_fixed_count_fields(state, source, '
                                      'state.city_owner_bytes, 4, 1, 40)\n'
                                      'normalize_saved_city_owner_sentinels(state)\n'
                                      'source = read_masked_fixed_count_fields(state, source, '
                                      'state.force_heads, 9, 2, 16)\n'
                                      'normalize_saved_force_head_sentinels(state)\n'
                                      'source = read_masked_fixed_count_fields(state, source, '
                                      'state.city_heads, 9, 2, 40)\n'
                                      'normalize_saved_city_head_sentinels(state)\n'
                                      'source = read_masked_fixed_count_fields(state, source, '
                                      'state.force_relationships, 20, 4, 40)\n'
                                      'state.force_link_bytes.set_byte(0, source.next_byte())\n'
                                      'source.base = source.advance(1).base\n'
                                      'state.force_link_bytes.set_byte(1, source.next_byte())\n'
                                      'source.base = source.advance(1).base\n'
                                      'destination = state.force_state_bytes.cursor()\n'
                                      'for _ in descending_inclusive(31):\n'
                                      '    destination.append_byte(source.next_byte())\n'
                                      '    source.base = source.advance(1).base\n'
                                      'source = read_masked_fixed_count_fields(state, source, '
                                      'state.city_parameter_e778, 17, 4, 40)\n'
                                      'for destination, bit_width in '
                                      '((state.city_order_actor_stage, 9), '
                                      '(state.city_order_quantity_stage, 14), '
                                      '(state.city_order_welfare_actor_stage, 9), '
                                      '(state.city_order_welfare_quantity_stage, 7), '
                                      '(state.city_order_transport_actor_stage, 9), '
                                      '(state.city_order_transport_quantity_stage, 10)):\n'
                                      '    source = read_masked_fixed_count_fields(state, source, '
                                      'destination, bit_width, 2, 40)\n'
                                      'restore_city_orders_and_action_flags(state)\n'
                                      'for destination, bit_width in ((state.force_column_first, '
                                      '6), (state.force_column_second, 6), '
                                      '(state.force_column_third, 8), (state.force_column_fourth, '
                                      '4)):\n'
                                      '    source = read_masked_fixed_count_fields(state, source, '
                                      'destination, bit_width, 1, 16)\n'
                                      'restore_saved_force_record_columns(state, '
                                      'state.force_records.cursor())\n'
                                      'source = read_masked_fixed_count_fields(state, source, '
                                      'state.city_parameter_ea38, 1, 1, 40)\n'
                                      'source = read_masked_fixed_count_fields(state, source, '
                                      'state.officer_equipment, 2, 1, 768)\n'
                                      'source = read_masked_fixed_count_fields(state, source, '
                                      'state.city_battle_gold, 18, 4, 40)\n'
                                      'source = read_masked_fixed_count_fields(state, source, '
                                      'state.city_battle_food, 20, 4, 40)\n'
                                      'source = read_masked_fixed_count_fields(state, source, '
                                      'state.force_parameter_f590, 2, 1, 16)\n'
                                      'source = read_packed_transport_orders(state, source)\n'
                                      'source = read_packed_group_stream(state, source)\n'
                                      "state.set_scalar('loaded_queue_head', 65535)\n"
                                      "state.set_scalar('loaded_flag_f776', 0)\n"
                                      "state.set_scalar('loaded_generation', "
                                      "u16(state.scalar('loaded_generation') + 1))\n"
                                      'return RestoreOutcome(True, source)'},
 'restore_saved_officer_positions': {'signature': 'state: StorageState',
                                     'returns': 'None',
                                     'flow': 'checked_state(state)\n'
                                             'destination = state.officer_positions.cursor()\n'
                                             'x_values = state.position_x_stage.cursor()\n'
                                             'y_values = state.position_y_stage.cursor()\n'
                                             'for _ in descending_inclusive(255):\n'
                                             '    destination.append_word(u16(x_values.next_word() '
                                             '<< 7))\n'
                                             '    destination.append_word(u16(y_values.next_word() '
                                             '<< 7))\n'
                                             'return None',
                                     'slots': {7: ('position_shift', 1, 8)}},
 'restore_city_orders_and_action_flags': {'signature': 'state: StorageState',
                                          'returns': 'None',
                                          'flow': 'checked_state(state)\n'
                                                  'source = state.city_order_actor_stage.cursor()\n'
                                                  'destination = state.city_orders.cursor()\n'
                                                  'for _ in descending_inclusive(39):\n'
                                                  '    officer = source.word()\n'
                                                  '    if officer == 511:\n'
                                                  '        officer = 65535\n'
                                                  '    else:\n'
                                                  '        state.officer_actions.set_byte(officer, '
                                                  '2)\n'
                                                  '    destination.append_word(officer)\n'
                                                  '    amount = source.word(80)\n'
                                                  '    if amount == 16383:\n'
                                                  '        amount = 65535\n'
                                                  '    destination.append_word(amount)\n'
                                                  '    officer = source.word(160)\n'
                                                  '    if officer == 511:\n'
                                                  '        officer = 65535\n'
                                                  '    else:\n'
                                                  '        state.officer_actions.set_byte(officer, '
                                                  '3)\n'
                                                  '    destination.append_word(officer)\n'
                                                  '    amount = source.word(240)\n'
                                                  '    if amount != 127:\n'
                                                  '        amount = u16(amount * 100)\n'
                                                  '    else:\n'
                                                  '        amount = 65535\n'
                                                  '    destination.append_word(amount)\n'
                                                  '    officer = source.word(320)\n'
                                                  '    if officer == 511:\n'
                                                  '        officer = 65535\n'
                                                  '    else:\n'
                                                  '        state.officer_actions.set_byte(officer, '
                                                  '4)\n'
                                                  '    destination.append_word(officer)\n'
                                                  '    amount = source.word(400)\n'
                                                  '    if amount == 1023:\n'
                                                  '        amount = 65535\n'
                                                  '    destination.append_word(amount)\n'
                                                  '    source.base = source.advance(2).base\n'
                                                  'return None'},
 'restore_scaled_officer_parameter_words': {'signature': 'state: StorageState',
                                            'returns': 'None',
                                            'flow': 'checked_state(state)\n'
                                                    'source = state.position_x_stage.cursor()\n'
                                                    'destination = '
                                                    'state.officer_parameter_b800.cursor()\n'
                                                    'for _ in descending_inclusive(255):\n'
                                                    '    '
                                                    'destination.append_word(u16(source.next_word() '
                                                    '* 5))\n'
                                                    'return None'},
 'normalize_saved_force_head_sentinels': {'signature': 'state: StorageState',
                                          'returns': 'None',
                                          'flow': 'checked_state(state)\n'
                                                  'destination = state.force_heads.cursor()\n'
                                                  'for _ in descending_inclusive(15):\n'
                                                  '    head = destination.word()\n'
                                                  '    if head == 511:\n'
                                                  '        head = 65535\n'
                                                  '    destination.append_word(head)\n'
                                                  'return None'},
 'normalize_saved_city_head_sentinels': {'signature': 'state: StorageState',
                                         'returns': 'None',
                                         'flow': 'checked_state(state)\n'
                                                 'destination = state.city_heads.cursor()\n'
                                                 'for _ in descending_inclusive(39):\n'
                                                 '    head = destination.word()\n'
                                                 '    if head == 511:\n'
                                                 '        head = 65535\n'
                                                 '    destination.append_word(head)\n'
                                                 'return None'},
 'normalize_saved_city_owner_sentinels': {'signature': 'state: StorageState',
                                          'returns': 'None',
                                          'flow': 'checked_state(state)\n'
                                                  'destination = state.city_owner_bytes.cursor()\n'
                                                  'for _ in descending_inclusive(39):\n'
                                                  '    owner = destination.byte()\n'
                                                  '    if owner == 15:\n'
                                                  '        owner = 255\n'
                                                  '    destination.append_byte(owner)\n'
                                                  'return None'},
 'restore_saved_force_record_columns': {'signature': 'state: StorageState, destination: Cursor',
                                        'returns': 'None',
                                        'flow': 'checked_state(state)\n'
                                                'checked_cursor(destination, state)\n'
                                                'first = state.force_column_first.cursor()\n'
                                                'second = state.force_column_second.cursor()\n'
                                                'third = state.force_column_third.cursor()\n'
                                                'fourth = state.force_column_fourth.cursor()\n'
                                                'for _ in descending_inclusive(15):\n'
                                                '    destination.append_byte(first.next_byte())\n'
                                                '    destination.append_byte(second.next_byte())\n'
                                                '    destination.append_byte(third.next_byte())\n'
                                                '    destination.append_byte(fourth.next_byte())\n'
                                                'return None'},
 'refresh_loaded_group_attributes': {'signature': 'state: StorageState, retained_header_high_byte: '
                                                  'Byte=0',
                                     'returns': 'None',
                                     'flow': 'checked_state(state)\n'
                                             'uint(retained_header_high_byte, 8)\n'
                                             'group = state.group_records\n'
                                             'while True:\n'
                                             '    header = group.byte()\n'
                                             '    if header == 0:\n'
                                             '        return None\n'
                                             '    count = u16(retained_header_high_byte << 8 | '
                                             'header)\n'
                                             '    total = 0\n'
                                             '    for member_position in '
                                             'descending_inclusive(u16(count - 1)):\n'
                                             '        member = group.byte(member_position, 13)\n'
                                             '        total = u16(total + '
                                             'state.officer_group_attribute.byte(member))\n'
                                             '    average = divu_retained(total, count)\n'
                                             '    group.set_byte(3, low8(low16(average)))\n'
                                             '    group = group.at(count, 13)'}}

def _lower_restore_saved_game_state(e,rules):
    e.label('storage_pc_008a60')
    e.ins('bsr.w','storage_pc_0090d8',4)
    e.label('storage_pc_008a64')
    e.ins('bcs.w','storage_pc_008ee8',4)
    e.label('storage_pc_008a68')
    e.ins('clr.w','0xf67a:w',4)
    e.label('storage_pc_008a6c')
    e.ins('move.b','0x200115:l,0xf67b:w',8)
    e.label('storage_pc_008a74')
    e.ins('clr.w','0xf67c:w',4)
    e.label('storage_pc_008a78')
    e.ins('move.b','0x200117:l,0xf67d:w',8)
    e.label('storage_pc_008a80')
    e.ins('clr.w','0xf67e:w',4)
    e.label('storage_pc_008a84')
    e.ins('move.b','0x200119:l,0xf67f:w',8)
    e.label('storage_pc_008a8c')
    e.ins('move.b','0x20011b:l,0xf374:w',8)
    e.label('storage_pc_008a94')
    e.ins('move.b','0x20011d:l,0xf375:w',8)
    e.label('storage_pc_008a9c')
    e.ins('clr.w','0xefd2:w',4)
    e.label('storage_pc_008aa0')
    e.ins('move.b','0x20011f:l,0xefd3:w',8)
    e.label('storage_pc_008aa8')
    e.ins('clr.w','0xefe4:w',4)
    e.label('storage_pc_008aac')
    e.ins('move.b','0x200121:l,0xefe5:w',8)
    e.label('storage_pc_008ab4')
    e.ins('clr.w','0xefd6:w',4)
    e.label('storage_pc_008ab8')
    e.ins('move.b','0x200123:l,0xefd7:w',8)
    e.label('storage_pc_008ac0')
    e.ins('clr.w','0xefd8:w',4)
    e.label('storage_pc_008ac4')
    e.ins('move.b','0x200125:l,0xefd9:w',8)
    e.label('storage_pc_008acc')
    e.ins('movea.l','#0x200127,%a0',6)
    e.label('storage_pc_008ad2')
    e.ins('lea.l','0xa000:w,%a1',4)
    e.label('storage_pc_008ad6')
    e.ins('move.w','#0x5,%d0',4)
    e.label('storage_pc_008ada')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008ade')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008ae2')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008ae6')
    e.ins('lea.l','0xefaa:w,%a1',4)
    e.label('storage_pc_008aea')
    e.ins('move.b','(%a0)+,(%a1)+',2)
    e.label('storage_pc_008aec')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_008af0')
    e.ins('move.b','(%a0)+,(%a1)+',2)
    e.label('storage_pc_008af2')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_008af6')
    e.ins('move.b','(%a0)+,(%a1)+',2)
    e.label('storage_pc_008af8')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_008afc')
    e.ins('move.b','(%a0)+,(%a1)+',2)
    e.label('storage_pc_008afe')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_008b02')
    e.ins('move.b','(%a0)+,(%a1)+',2)
    e.label('storage_pc_008b04')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_008b08')
    e.ins('lea.l','0xa028:w,%a1',4)
    e.label('storage_pc_008b0c')
    e.ins('move.w','#0x8,%d0',4)
    e.label('storage_pc_008b10')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008b14')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008b18')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008b1c')
    e.ins('lea.l','0xa050:w,%a1',4)
    e.label('storage_pc_008b20')
    e.ins('move.w','#0x8,%d0',4)
    e.label('storage_pc_008b24')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008b28')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008b2c')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008b30')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('storage_pc_008b34')
    e.ins('move.w','#0x8,%d0',4)
    e.label('storage_pc_008b38')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008b3c')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008b40')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008b44')
    e.ins('lea.l','0xd500:w,%a1',4)
    e.label('storage_pc_008b48')
    e.ins('move.w','#0x9,%d0',4)
    e.label('storage_pc_008b4c')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008b50')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008b54')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008b58')
    e.ins('bsr.w','storage_pc_008eea',4)
    e.label('storage_pc_008b5c')
    e.ins('lea.l','0xb200:w,%a1',4)
    e.label('storage_pc_008b60')
    e.ins('move.w','#0x8,%d0',4)
    e.label('storage_pc_008b64')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008b68')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008b6c')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008b70')
    e.ins('lea.l','0xb400:w,%a1',4)
    e.label('storage_pc_008b74')
    e.ins('move.w','#0x8,%d0',4)
    e.label('storage_pc_008b78')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008b7c')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008b80')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008b84')
    e.ins('lea.l','0xb600:w,%a1',4)
    e.label('storage_pc_008b88')
    e.ins('move.w','#0x8,%d0',4)
    e.label('storage_pc_008b8c')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008b90')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008b94')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008b98')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('storage_pc_008b9c')
    e.ins('move.w','#0x5,%d0',4)
    e.label('storage_pc_008ba0')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008ba4')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008ba8')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008bac')
    e.ins('bsr.w','storage_pc_00901c',4)
    e.label('storage_pc_008bb0')
    e.ins('lea.l','0xc000:w,%a1',4)
    e.label('storage_pc_008bb4')
    e.ins('move.w','#0xa,%d0',4)
    e.label('storage_pc_008bb8')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008bbc')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008bc0')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008bc4')
    e.ins('lea.l','0xbe00:w,%a1',4)
    e.label('storage_pc_008bc8')
    e.ins('move.w','#0xa,%d0',4)
    e.label('storage_pc_008bcc')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008bd0')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008bd4')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008bd8')
    e.ins('lea.l','0xc200:w,%a1',4)
    e.label('storage_pc_008bdc')
    e.ins('move.w','#0x7,%d0',4)
    e.label('storage_pc_008be0')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008be4')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008be8')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008bec')
    e.ins('lea.l','0xc300:w,%a1',4)
    e.label('storage_pc_008bf0')
    e.ins('move.w','#0x7,%d0',4)
    e.label('storage_pc_008bf4')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008bf8')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008bfc')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008c00')
    e.ins('lea.l','0xc400:w,%a1',4)
    e.label('storage_pc_008c04')
    e.ins('move.w','#0x5,%d0',4)
    e.label('storage_pc_008c08')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008c0c')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008c10')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008c14')
    e.ins('lea.l','0xc500:w,%a1',4)
    e.label('storage_pc_008c18')
    e.ins('move.w','#0x7,%d0',4)
    e.label('storage_pc_008c1c')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008c20')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008c24')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008c28')
    e.ins('lea.l','0xc700:w,%a1',4)
    e.label('storage_pc_008c2c')
    e.ins('move.w','#0x5,%d0',4)
    e.label('storage_pc_008c30')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008c34')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008c38')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008c3c')
    e.ins('lea.l','0xc800:w,%a1',4)
    e.label('storage_pc_008c40')
    e.ins('move.w','#0xe,%d0',4)
    e.label('storage_pc_008c44')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008c48')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008c4c')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008c50')
    e.ins('lea.l','0xcc00:w,%a1',4)
    e.label('storage_pc_008c54')
    e.ins('move.w','#0x8,%d0',4)
    e.label('storage_pc_008c58')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008c5c')
    e.ins('move.w','#0x100,%d2',4)
    e.label('storage_pc_008c60')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008c64')
    e.ins('lea.l','0xe000:w,%a1',4)
    e.label('storage_pc_008c68')
    e.ins('move.w','#0x14,%d0',4)
    e.label('storage_pc_008c6c')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008c70')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008c74')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008c78')
    e.ins('lea.l','0xe0a0:w,%a1',4)
    e.label('storage_pc_008c7c')
    e.ins('move.w','#0x14,%d0',4)
    e.label('storage_pc_008c80')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008c84')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008c88')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008c8c')
    e.ins('lea.l','0xe140:w,%a1',4)
    e.label('storage_pc_008c90')
    e.ins('move.w','#0xa,%d0',4)
    e.label('storage_pc_008c94')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008c98')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008c9c')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008ca0')
    e.ins('lea.l','0xe1e0:w,%a1',4)
    e.label('storage_pc_008ca4')
    e.ins('move.w','#0xa,%d0',4)
    e.label('storage_pc_008ca8')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008cac')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008cb0')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008cb4')
    e.ins('lea.l','0xe280:w,%a1',4)
    e.label('storage_pc_008cb8')
    e.ins('move.w','#0x7,%d0',4)
    e.label('storage_pc_008cbc')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008cc0')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008cc4')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008cc8')
    e.ins('lea.l','0xe320:w,%a1',4)
    e.label('storage_pc_008ccc')
    e.ins('move.w','#0x7,%d0',4)
    e.label('storage_pc_008cd0')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008cd4')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008cd8')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008cdc')
    e.ins('lea.l','0xe3c0:w,%a1',4)
    e.label('storage_pc_008ce0')
    e.ins('move.w','#0x7,%d0',4)
    e.label('storage_pc_008ce4')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008ce8')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008cec')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008cf0')
    e.ins('lea.l','0xe5a0:w,%a1',4)
    e.label('storage_pc_008cf4')
    e.ins('move.w','#0x7,%d0',4)
    e.label('storage_pc_008cf8')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008cfc')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008d00')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008d04')
    e.ins('lea.l','0xf428:w,%a1',4)
    e.label('storage_pc_008d08')
    e.ins('move.w','#0x4,%d0',4)
    e.label('storage_pc_008d0c')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008d10')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008d14')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008d18')
    e.ins('bsr.w','storage_pc_009184',4)
    e.label('storage_pc_008d1c')
    e.ins('lea.l','0xe640:w,%a1',4)
    e.label('storage_pc_008d20')
    e.ins('move.w','#0x9,%d0',4)
    e.label('storage_pc_008d24')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008d28')
    e.ins('move.w','#0x10,%d2',4)
    e.label('storage_pc_008d2c')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008d30')
    e.ins('bsr.w','storage_pc_009148',4)
    e.label('storage_pc_008d34')
    e.ins('lea.l','0xf460:w,%a1',4)
    e.label('storage_pc_008d38')
    e.ins('move.w','#0x9,%d0',4)
    e.label('storage_pc_008d3c')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008d40')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008d44')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008d48')
    e.ins('bsr.w','storage_pc_009166',4)
    e.label('storage_pc_008d4c')
    e.ins('lea.l','0xe660:w,%a1',4)
    e.label('storage_pc_008d50')
    e.ins('move.w','#0x14,%d0',4)
    e.label('storage_pc_008d54')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008d58')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008d5c')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008d60')
    e.ins('move.b','(%a0)+,0xe700:w',4)
    e.label('storage_pc_008d64')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_008d68')
    e.ins('move.b','(%a0)+,0xe701:w',4)
    e.label('storage_pc_008d6c')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_008d70')
    e.ins('lea.l','0xe710:w,%a1',4)
    e.label('storage_pc_008d74')
    e.ins('move.w','#0x1f,%d2',4)
    e.label('storage_pc_008d78')
    e.ins('move.b','(%a0)+,(%a1)+',2)
    e.label('storage_pc_008d7a')
    e.ins('lea.l','0x1(%a0),%a0',4)
    e.label('storage_pc_008d7e')
    e.ins('dbra','%d2,storage_pc_008d78',4)
    e.label('storage_pc_008d82')
    e.ins('lea.l','0xe778:w,%a1',4)
    e.label('storage_pc_008d86')
    e.ins('move.w','#0x11,%d0',4)
    e.label('storage_pc_008d8a')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008d8e')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008d92')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008d96')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('storage_pc_008d9a')
    e.ins('move.w','#0x9,%d0',4)
    e.label('storage_pc_008d9e')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008da2')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008da6')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008daa')
    e.ins('lea.l','0xd350:w,%a1',4)
    e.label('storage_pc_008dae')
    e.ins('move.w','#0xe,%d0',4)
    e.label('storage_pc_008db2')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008db6')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008dba')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008dbe')
    e.ins('lea.l','0xd3a0:w,%a1',4)
    e.label('storage_pc_008dc2')
    e.ins('move.w','#0x9,%d0',4)
    e.label('storage_pc_008dc6')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008dca')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008dce')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008dd2')
    e.ins('lea.l','0xd3f0:w,%a1',4)
    e.label('storage_pc_008dd6')
    e.ins('move.w','#0x7,%d0',4)
    e.label('storage_pc_008dda')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008dde')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008de2')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008de6')
    e.ins('lea.l','0xd440:w,%a1',4)
    e.label('storage_pc_008dea')
    e.ins('move.w','#0x9,%d0',4)
    e.label('storage_pc_008dee')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008df2')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008df6')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008dfa')
    e.ins('lea.l','0xd490:w,%a1',4)
    e.label('storage_pc_008dfe')
    e.ins('move.w','#0xa,%d0',4)
    e.label('storage_pc_008e02')
    e.ins('move.w','#0x2,%d1',4)
    e.label('storage_pc_008e06')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008e0a')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008e0e')
    e.ins('bsr.w','storage_pc_008f0c',4)
    e.label('storage_pc_008e12')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('storage_pc_008e16')
    e.ins('move.w','#0x6,%d0',4)
    e.label('storage_pc_008e1a')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008e1e')
    e.ins('move.w','#0x10,%d2',4)
    e.label('storage_pc_008e22')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008e26')
    e.ins('lea.l','0xd310:w,%a1',4)
    e.label('storage_pc_008e2a')
    e.ins('move.w','#0x6,%d0',4)
    e.label('storage_pc_008e2e')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008e32')
    e.ins('move.w','#0x10,%d2',4)
    e.label('storage_pc_008e36')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008e3a')
    e.ins('lea.l','0xd320:w,%a1',4)
    e.label('storage_pc_008e3e')
    e.ins('move.w','#0x8,%d0',4)
    e.label('storage_pc_008e42')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008e46')
    e.ins('move.w','#0x10,%d2',4)
    e.label('storage_pc_008e4a')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008e4e')
    e.ins('lea.l','0xd330:w,%a1',4)
    e.label('storage_pc_008e52')
    e.ins('move.w','#0x4,%d0',4)
    e.label('storage_pc_008e56')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008e5a')
    e.ins('move.w','#0x10,%d2',4)
    e.label('storage_pc_008e5e')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008e62')
    e.ins('lea.l','0xe9f8:w,%a1',4)
    e.label('storage_pc_008e66')
    e.ins('bsr.w','storage_pc_0091a2',4)
    e.label('storage_pc_008e6a')
    e.ins('lea.l','0xea38:w,%a1',4)
    e.label('storage_pc_008e6e')
    e.ins('move.w','#0x1,%d0',4)
    e.label('storage_pc_008e72')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008e76')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008e7a')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008e7e')
    e.ins('lea.l','0xea88:w,%a1',4)
    e.label('storage_pc_008e82')
    e.ins('move.w','#0x2,%d0',4)
    e.label('storage_pc_008e86')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008e8a')
    e.ins('move.w','#0x300,%d2',4)
    e.label('storage_pc_008e8e')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008e92')
    e.ins('lea.l','0xed88:w,%a1',4)
    e.label('storage_pc_008e96')
    e.ins('move.w','#0x12,%d0',4)
    e.label('storage_pc_008e9a')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008e9e')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008ea2')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008ea6')
    e.ins('lea.l','0xee28:w,%a1',4)
    e.label('storage_pc_008eaa')
    e.ins('move.w','#0x14,%d0',4)
    e.label('storage_pc_008eae')
    e.ins('move.w','#0x4,%d1',4)
    e.label('storage_pc_008eb2')
    e.ins('move.w','#0x28,%d2',4)
    e.label('storage_pc_008eb6')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008eba')
    e.ins('lea.l','0xf590:w,%a1',4)
    e.label('storage_pc_008ebe')
    e.ins('move.w','#0x2,%d0',4)
    e.label('storage_pc_008ec2')
    e.ins('move.w','#0x1,%d1',4)
    e.label('storage_pc_008ec6')
    e.ins('move.w','#0x10,%d2',4)
    e.label('storage_pc_008eca')
    e.ins('bsr.w','storage_pc_00931e',4)
    e.label('storage_pc_008ece')
    e.ins('bsr.w','storage_pc_008fb4',4)
    e.label('storage_pc_008ed2')
    e.ins('bsr.w','storage_pc_009036',4)
    e.label('storage_pc_008ed6')
    e.ins('move.w','#0xffff,0xff3000:l',8)
    e.label('storage_pc_008ede')
    e.ins('clr.w','0xf776:w',4)
    e.label('storage_pc_008ee2')
    e.ins('addq.w','#0x1,0xaffe:w',4)
    e.label('storage_pc_008ee6')
    e.ins('rts','',2)
    e.label('storage_pc_008ee8')
    e.ins('rts','',2)

def _lower_restore_saved_officer_positions(e,rules):
    e.label('storage_pc_008eea')
    e.ins('lea.l','0xa150:w,%a2',4)
    e.label('storage_pc_008eee')
    e.ins('lea.l','0xd300:w,%a3',4)
    e.label('storage_pc_008ef2')
    e.ins('lea.l','0xd500:w,%a4',4)
    e.label('storage_pc_008ef6')
    e.ins('move.w','#0xff,%d0',4)
    e.label('storage_pc_008efa')
    e.ins('move.w','(%a3)+,%d1',2)
    e.label('storage_pc_008efc')
    e.ins('lsl.w','#'+hex(rules['position_shift'])+',%d1',2)
    e.label('storage_pc_008efe')
    e.ins('move.w','%d1,(%a2)+',2)
    e.label('storage_pc_008f00')
    e.ins('move.w','(%a4)+,%d1',2)
    e.label('storage_pc_008f02')
    e.ins('lsl.w','#'+hex(rules['position_shift'])+',%d1',2)
    e.label('storage_pc_008f04')
    e.ins('move.w','%d1,(%a2)+',2)
    e.label('storage_pc_008f06')
    e.ins('dbra','%d0,storage_pc_008efa',4)
    e.label('storage_pc_008f0a')
    e.ins('rts','',2)

def _lower_restore_city_orders_and_action_flags(e,rules):
    e.label('storage_pc_008f0c')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('storage_pc_008f10')
    e.ins('lea.l','0xe818:w,%a2',4)
    e.label('storage_pc_008f14')
    e.ins('lea.l','0xcd00:w,%a3',4)
    e.label('storage_pc_008f18')
    e.ins('move.w','#0x27,%d0',4)
    e.label('storage_pc_008f1c')
    e.ins('move.w','(%a1),%d1',2)
    e.label('storage_pc_008f1e')
    e.ins('cmpi.w','#0x1ff,%d1',4)
    e.label('storage_pc_008f22')
    e.ins('bne.w','storage_pc_008f2e',4)
    e.label('storage_pc_008f26')
    e.ins('move.w','#0xffff,%d1',4)
    e.label('storage_pc_008f2a')
    e.ins('bra.w','storage_pc_008f34',4)
    e.label('storage_pc_008f2e')
    e.ins('move.b','#0x2,(%a3, %d1.w)',6)
    e.label('storage_pc_008f34')
    e.ins('move.w','%d1,(%a2)+',2)
    e.label('storage_pc_008f36')
    e.ins('move.w','0x50(%a1),%d1',4)
    e.label('storage_pc_008f3a')
    e.ins('cmpi.w','#0x3fff,%d1',4)
    e.label('storage_pc_008f3e')
    e.ins('bne.w','storage_pc_008f46',4)
    e.label('storage_pc_008f42')
    e.ins('move.w','#0xffff,%d1',4)
    e.label('storage_pc_008f46')
    e.ins('move.w','%d1,(%a2)+',2)
    e.label('storage_pc_008f48')
    e.ins('move.w','0xa0(%a1),%d1',4)
    e.label('storage_pc_008f4c')
    e.ins('cmpi.w','#0x1ff,%d1',4)
    e.label('storage_pc_008f50')
    e.ins('bne.w','storage_pc_008f5c',4)
    e.label('storage_pc_008f54')
    e.ins('move.w','#0xffff,%d1',4)
    e.label('storage_pc_008f58')
    e.ins('bra.w','storage_pc_008f62',4)
    e.label('storage_pc_008f5c')
    e.ins('move.b','#0x3,(%a3, %d1.w)',6)
    e.label('storage_pc_008f62')
    e.ins('move.w','%d1,(%a2)+',2)
    e.label('storage_pc_008f64')
    e.ins('move.w','0xf0(%a1),%d1',4)
    e.label('storage_pc_008f68')
    e.ins('cmpi.w','#0x7f,%d1',4)
    e.label('storage_pc_008f6c')
    e.ins('beq.w','storage_pc_008f78',4)
    e.label('storage_pc_008f70')
    e.ins('mulu.w','#0x64,%d1',4)
    e.label('storage_pc_008f74')
    e.ins('bra.w','storage_pc_008f7c',4)
    e.label('storage_pc_008f78')
    e.ins('move.w','#0xffff,%d1',4)
    e.label('storage_pc_008f7c')
    e.ins('move.w','%d1,(%a2)+',2)
    e.label('storage_pc_008f7e')
    e.ins('move.w','0x140(%a1),%d1',4)
    e.label('storage_pc_008f82')
    e.ins('cmpi.w','#0x1ff,%d1',4)
    e.label('storage_pc_008f86')
    e.ins('bne.w','storage_pc_008f92',4)
    e.label('storage_pc_008f8a')
    e.ins('move.w','#0xffff,%d1',4)
    e.label('storage_pc_008f8e')
    e.ins('bra.w','storage_pc_008f98',4)
    e.label('storage_pc_008f92')
    e.ins('move.b','#0x4,(%a3, %d1.w)',6)
    e.label('storage_pc_008f98')
    e.ins('move.w','%d1,(%a2)+',2)
    e.label('storage_pc_008f9a')
    e.ins('move.w','0x190(%a1),%d1',4)
    e.label('storage_pc_008f9e')
    e.ins('cmpi.w','#0x3ff,%d1',4)
    e.label('storage_pc_008fa2')
    e.ins('bne.w','storage_pc_008faa',4)
    e.label('storage_pc_008fa6')
    e.ins('move.w','#0xffff,%d1',4)
    e.label('storage_pc_008faa')
    e.ins('move.w','%d1,(%a2)+',2)
    e.label('storage_pc_008fac')
    e.ins('addq.w','#0x2,%a1',2)
    e.label('storage_pc_008fae')
    e.ins('dbra','%d0,storage_pc_008f1c',4)
    e.label('storage_pc_008fb2')
    e.ins('rts','',2)

def _lower_restore_scaled_officer_parameter_words(e,rules):
    e.label('storage_pc_00901c')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('storage_pc_009020')
    e.ins('lea.l','0xb800:w,%a2',4)
    e.label('storage_pc_009024')
    e.ins('move.w','#0xff,%d0',4)
    e.label('storage_pc_009028')
    e.ins('move.w','(%a1)+,%d1',2)
    e.label('storage_pc_00902a')
    e.ins('mulu.w','#0x5,%d1',4)
    e.label('storage_pc_00902e')
    e.ins('move.w','%d1,(%a2)+',2)
    e.label('storage_pc_009030')
    e.ins('dbra','%d0,storage_pc_009028',4)
    e.label('storage_pc_009034')
    e.ins('rts','',2)

def _lower_normalize_saved_force_head_sentinels(e,rules):
    e.label('storage_pc_009148')
    e.ins('lea.l','0xe640:w,%a1',4)
    e.label('storage_pc_00914c')
    e.ins('move.w','#0xf,%d0',4)
    e.label('storage_pc_009150')
    e.ins('move.w','(%a1),%d1',2)
    e.label('storage_pc_009152')
    e.ins('cmpi.w','#0x1ff,%d1',4)
    e.label('storage_pc_009156')
    e.ins('bne.w','storage_pc_00915e',4)
    e.label('storage_pc_00915a')
    e.ins('move.w','#0xffff,%d1',4)
    e.label('storage_pc_00915e')
    e.ins('move.w','%d1,(%a1)+',2)
    e.label('storage_pc_009160')
    e.ins('dbra','%d0,storage_pc_009150',4)
    e.label('storage_pc_009164')
    e.ins('rts','',2)

def _lower_normalize_saved_city_head_sentinels(e,rules):
    e.label('storage_pc_009166')
    e.ins('lea.l','0xf460:w,%a1',4)
    e.label('storage_pc_00916a')
    e.ins('move.w','#0x27,%d0',4)
    e.label('storage_pc_00916e')
    e.ins('move.w','(%a1),%d1',2)
    e.label('storage_pc_009170')
    e.ins('cmpi.w','#0x1ff,%d1',4)
    e.label('storage_pc_009174')
    e.ins('bne.w','storage_pc_00917c',4)
    e.label('storage_pc_009178')
    e.ins('move.w','#0xffff,%d1',4)
    e.label('storage_pc_00917c')
    e.ins('move.w','%d1,(%a1)+',2)
    e.label('storage_pc_00917e')
    e.ins('dbra','%d0,storage_pc_00916e',4)
    e.label('storage_pc_009182')
    e.ins('rts','',2)

def _lower_normalize_saved_city_owner_sentinels(e,rules):
    e.label('storage_pc_009184')
    e.ins('lea.l','0xf428:w,%a1',4)
    e.label('storage_pc_009188')
    e.ins('move.w','#0x27,%d0',4)
    e.label('storage_pc_00918c')
    e.ins('move.b','(%a1),%d1',2)
    e.label('storage_pc_00918e')
    e.ins('cmpi.b','#0xf,%d1',4)
    e.label('storage_pc_009192')
    e.ins('bne.w','storage_pc_00919a',4)
    e.label('storage_pc_009196')
    e.ins('move.b','#0xff,%d1',4)
    e.label('storage_pc_00919a')
    e.ins('move.b','%d1,(%a1)+',2)
    e.label('storage_pc_00919c')
    e.ins('dbra','%d0,storage_pc_00918c',4)
    e.label('storage_pc_0091a0')
    e.ins('rts','',2)

def _lower_restore_saved_force_record_columns(e,rules):
    e.label('storage_pc_0091a2')
    e.ins('lea.l','0xd300:w,%a2',4)
    e.label('storage_pc_0091a6')
    e.ins('lea.l','0xd310:w,%a3',4)
    e.label('storage_pc_0091aa')
    e.ins('lea.l','0xd320:w,%a4',4)
    e.label('storage_pc_0091ae')
    e.ins('lea.l','0xd330:w,%a5',4)
    e.label('storage_pc_0091b2')
    e.ins('move.w','#0xf,%d0',4)
    e.label('storage_pc_0091b6')
    e.ins('move.b','(%a2)+,(%a1)+',2)
    e.label('storage_pc_0091b8')
    e.ins('move.b','(%a3)+,(%a1)+',2)
    e.label('storage_pc_0091ba')
    e.ins('move.b','(%a4)+,(%a1)+',2)
    e.label('storage_pc_0091bc')
    e.ins('move.b','(%a5)+,(%a1)+',2)
    e.label('storage_pc_0091be')
    e.ins('dbra','%d0,storage_pc_0091b6',4)
    e.label('storage_pc_0091c2')
    e.ins('rts','',2)

def _lower_refresh_loaded_group_attributes(e,rules):
    e.label('storage_pc_0091f8')
    e.ins('lea.l','0x9000:w,%a1',4)
    e.label('storage_pc_0091fc')
    e.ins('lea.l','0xc400:w,%a2',4)
    e.label('storage_pc_009200')
    e.ins('move.b','(%a1),%d0',2)
    e.label('storage_pc_009202')
    e.ins('beq.w','storage_pc_009228',4)
    e.label('storage_pc_009206')
    e.ins('move.w','%d0,%d1',2)
    e.label('storage_pc_009208')
    e.ins('subq.w','#0x1,%d1',2)
    e.label('storage_pc_00920a')
    e.ins('moveq','#0,%d2',2)
    e.label('storage_pc_00920c')
    e.ins('clr.w','%d3',2)
    e.label('storage_pc_00920e')
    e.ins('move.b','0xd(%a1, %d1.w),%d3',4)
    e.label('storage_pc_009212')
    e.ins('move.b','(%a2, %d3.w),%d3',4)
    e.label('storage_pc_009216')
    e.ins('add.w','%d3,%d2',2)
    e.label('storage_pc_009218')
    e.ins('dbra','%d1,storage_pc_00920c',4)
    e.label('storage_pc_00921c')
    e.ins('divu.w','%d0,%d2',2)
    e.label('storage_pc_00921e')
    e.ins('move.b','%d2,0x3(%a1)',4)
    e.label('storage_pc_009222')
    e.ins('lea.l','0xd(%a1, %d0.w),%a1',4)
    e.label('storage_pc_009226')
    e.ins('bra.b','storage_pc_009200',2)
    e.label('storage_pc_009228')
    e.ins('rts','',2)

LOWERERS = {
    'restore_saved_game_state':_lower_restore_saved_game_state,
    'restore_saved_officer_positions':_lower_restore_saved_officer_positions,
    'restore_city_orders_and_action_flags':_lower_restore_city_orders_and_action_flags,
    'restore_scaled_officer_parameter_words':_lower_restore_scaled_officer_parameter_words,
    'normalize_saved_force_head_sentinels':_lower_normalize_saved_force_head_sentinels,
    'normalize_saved_city_head_sentinels':_lower_normalize_saved_city_head_sentinels,
    'normalize_saved_city_owner_sentinels':_lower_normalize_saved_city_owner_sentinels,
    'restore_saved_force_record_columns':_lower_restore_saved_force_record_columns,
    'refresh_loaded_group_attributes':_lower_refresh_loaded_group_attributes,
}

def compile_load(source):
    """Admit complete current fields and use untouched physical lowerers.

    This bounded frontend is not a generic Python editor or CPU proof.
    The legacy scalar phase inliner is deliberately not used on the
    complete field source; all actual functions share one declaration
    authority, including real child-slot/flag helpers.
    """
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    current_fields = {'normalize_saved_city_head_sentinels': 'normalize_saved_city_head_sentinels_frame_fields',
     'normalize_saved_city_owner_sentinels': 'normalize_saved_city_owner_sentinels_frame_fields',
     'normalize_saved_force_head_sentinels': 'normalize_saved_force_head_sentinels_frame_fields',
     'refresh_loaded_group_attributes': 'refresh_loaded_group_attributes_frame_fields',
     'restore_city_orders_and_action_flags': 'restore_city_orders_and_action_flags_frame_fields',
     'restore_saved_force_record_columns': 'restore_saved_force_record_columns_frame_fields',
     'restore_saved_game_state': 'restore_saved_game_state_frame_fields',
     'restore_saved_officer_positions': 'restore_saved_officer_positions_frame_fields',
     'restore_scaled_officer_parameter_words': 'restore_scaled_officer_parameter_words_frame_fields'}
    selected = {}
    for binding in LOAD_BINDINGS:
        actual = records[current_fields[binding.name]]
        selected[binding.name] = dict(name=binding.name, rules=actual['rules'], effects=actual['effects'])
    return lower_declared(selected, LOAD_BINDINGS, LOWERERS)

# C54 complete storage-field authority; no ordinary lowerer or common guard change.
DECLARATIONS.update({'_normalize_saved_sentinels_fields': {'flow': "frame = storage_address(frame, 'a1', address)\n"
                                               "frame = storage_move(state, frame, 'd0', counter, "
                                               '16)\n'
                                               'while True:\n'
                                               "    frame = storage_move(state, frame, 'd1', "
                                               'state.read(frame.a1, bits // 8), bits)\n'
                                               "    frame = storage_arithmetic(state, frame, 'd1', "
                                               'sentinel, bits, True, True)\n'
                                               '    if frame.status_word & 4:\n'
                                               "        frame = storage_move(state, frame, 'd1', "
                                               '(1 << bits) - 1, bits)\n'
                                               "    frame = storage_write_next(state, frame, 'a1', "
                                               'bits // 8, frame.d1)\n'
                                               "    frame, again = storage_dbra(frame, 'd0')\n"
                                               '    if not again:\n'
                                               '        return frame',
                                       'returns': 'StorageFrame',
                                       'signature': 'state: StorageState, frame: StorageFrame, '
                                                    'address: Long, counter: int, bits: int, '
                                                    'sentinel: int'},
 '_read_saved_column_fields': {'flow': 'destination, field_bits, stride, count, continuation = '
                                       'column\n'
                                       "frame = storage_address(frame, 'a1', destination)\n"
                                       "frame = storage_move(state, frame, 'd0', field_bits, 16)\n"
                                       "frame = storage_move(state, frame, 'd1', stride, 16)\n"
                                       "frame = storage_move(state, frame, 'd2', count, 16)\n"
                                       'return storage_call(state, frame, '
                                       'read_masked_fixed_count_frame_fields, continuation)',
                               'returns': 'StorageFrame',
                               'signature': 'state: StorageState, frame: StorageFrame, column: '
                                            'tuple'},
 '_read_saved_columns_fields': {'flow': 'for column in columns:\n'
                                        '    frame = _read_saved_column_fields(state, frame, '
                                        'column)\n'
                                        'return frame',
                                'returns': 'StorageFrame',
                                'signature': 'state: StorageState, frame: StorageFrame, columns: '
                                             'tuple'},
 '_restore_city_order_word_fields': {'flow': 'value = state.read(frame.a1 + displacement, 2)\n'
                                             "frame = storage_move(state, frame, 'd1', value, 16)\n"
                                             "frame = storage_arithmetic(state, frame, 'd1', "
                                             'sentinel, 16, True, True)\n'
                                             'if frame.status_word & 4:\n'
                                             "    frame = storage_move(state, frame, 'd1', 65535, "
                                             '16)\n'
                                             'elif assignment:\n'
                                             '    frame = storage_write(state, frame, frame.a3 + '
                                             's16(low16(frame.d1)), 1, assignment)\n'
                                             "return storage_write_next(state, frame, 'a2', 2, "
                                             'frame.d1)',
                                     'returns': 'StorageFrame',
                                     'signature': 'state: StorageState, frame: StorageFrame, '
                                                  'displacement: int, sentinel: int, assignment: '
                                                  'int'},
 'begin_loaded_membership_fields': {'flow': "raise Boundary('legacy partial storage phase has no "
                                            "whole entry; use the full save or restore core')",
                                    'returns': 'Cursor',
                                    'signature': 'state: StorageState, entry_frame: '
                                                 'StorageFrame=None'},
 'normalize_saved_city_head_sentinels': {'flow': 'frame = storage_legacy_entry(state, '
                                                 'entry_frame)\n'
                                                 'returned = '
                                                 'normalize_saved_city_head_sentinels_frame_fields(state, '
                                                 'frame)\n'
                                                 'return None',
                                         'returns': 'None',
                                         'signature': 'state: StorageState, entry_frame: '
                                                      'StorageFrame=None'},
 'normalize_saved_city_head_sentinels_frame_fields': {'flow': 'return '
                                                              '_normalize_saved_sentinels_fields(state, '
                                                              'storage_entry(state, frame), '
                                                              '4294964320, 39, 16, 511)',
                                                      'returns': 'StorageFrame',
                                                      'signature': 'state: StorageState, frame: '
                                                                   'StorageFrame'},
 'normalize_saved_city_owner_sentinels': {'flow': 'frame = storage_legacy_entry(state, '
                                                  'entry_frame)\n'
                                                  'returned = '
                                                  'normalize_saved_city_owner_sentinels_frame_fields(state, '
                                                  'frame)\n'
                                                  'return None',
                                          'returns': 'None',
                                          'signature': 'state: StorageState, entry_frame: '
                                                       'StorageFrame=None'},
 'normalize_saved_city_owner_sentinels_frame_fields': {'flow': 'return '
                                                               '_normalize_saved_sentinels_fields(state, '
                                                               'storage_entry(state, frame), '
                                                               '4294964264, 39, 8, 15)',
                                                       'returns': 'StorageFrame',
                                                       'signature': 'state: StorageState, frame: '
                                                                    'StorageFrame'},
 'normalize_saved_force_head_sentinels': {'flow': 'frame = storage_legacy_entry(state, '
                                                  'entry_frame)\n'
                                                  'returned = '
                                                  'normalize_saved_force_head_sentinels_frame_fields(state, '
                                                  'frame)\n'
                                                  'return None',
                                          'returns': 'None',
                                          'signature': 'state: StorageState, entry_frame: '
                                                       'StorageFrame=None'},
 'normalize_saved_force_head_sentinels_frame_fields': {'flow': 'return '
                                                               '_normalize_saved_sentinels_fields(state, '
                                                               'storage_entry(state, frame), '
                                                               '4294960704, 15, 16, 511)',
                                                       'returns': 'StorageFrame',
                                                       'signature': 'state: StorageState, frame: '
                                                                    'StorageFrame'},
 'refresh_loaded_group_attributes': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                             'if retained_header_high_byte != frame.d0 >> 8 & '
                                             '255:\n'
                                             "    raise ValueError('retained group count WORD "
                                             "differs from complete entry')\n"
                                             'returned = '
                                             'refresh_loaded_group_attributes_frame_fields(state, '
                                             'frame)\n'
                                             'return None',
                                     'returns': 'None',
                                     'signature': 'state: StorageState, retained_header_high_byte: '
                                                  'Byte=0, entry_frame: StorageFrame=None'},
 'refresh_loaded_group_attributes_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                          "frame = storage_address(frame, 'a1', "
                                                          '4294938624)\n'
                                                          "frame = storage_address(frame, 'a2', "
                                                          '4294951936)\n'
                                                          'while True:\n'
                                                          '    frame = storage_move(state, frame, '
                                                          "'d0', state.read(frame.a1, 1), 8)\n"
                                                          '    if frame.status_word & 4:\n'
                                                          '        return frame\n'
                                                          '    frame = storage_move(state, frame, '
                                                          "'d1', frame.d0, 16)\n"
                                                          '    frame = storage_arithmetic(state, '
                                                          "frame, 'd1', 1, 16, True)\n"
                                                          '    frame = storage_move(state, frame, '
                                                          "'d2', 0, 32)\n"
                                                          '    while True:\n'
                                                          '        frame = storage_move(state, '
                                                          "frame, 'd3', 0, 16)\n"
                                                          '        frame = storage_move(state, '
                                                          "frame, 'd3', state.read(frame.a1 + "
                                                          's16(low16(frame.d1)) + 13, 1), 8)\n'
                                                          '        frame = storage_move(state, '
                                                          "frame, 'd3', state.read(frame.a2 + "
                                                          's16(low16(frame.d3)), 1), 8)\n'
                                                          '        frame = '
                                                          "storage_arithmetic(state, frame, 'd2', "
                                                          'frame.d3, 16)\n'
                                                          '        frame, again = '
                                                          "storage_dbra(frame, 'd1')\n"
                                                          '        if not again:\n'
                                                          '            break\n'
                                                          '    frame = storage_divide(state, '
                                                          "frame, 'd2', frame.d0)\n"
                                                          '    frame = storage_write(state, frame, '
                                                          'frame.a1 + 3, 1, frame.d2)\n'
                                                          '    frame = storage_address_step(frame, '
                                                          "'a1', s16(low16(frame.d0)) + 13)",
                                                  'returns': 'StorageFrame',
                                                  'signature': 'state: StorageState, frame: '
                                                               'StorageFrame'},
 'restore_city_orders_and_action_flags': {'flow': 'frame = storage_legacy_entry(state, '
                                                  'entry_frame)\n'
                                                  'returned = '
                                                  'restore_city_orders_and_action_flags_frame_fields(state, '
                                                  'frame)\n'
                                                  'return None',
                                          'returns': 'None',
                                          'signature': 'state: StorageState, entry_frame: '
                                                       'StorageFrame=None'},
 'restore_city_orders_and_action_flags_frame_fields': {'flow': 'frame = storage_entry(state, '
                                                               'frame)\n'
                                                               'frame = storage_address(frame, '
                                                               "'a1', 4294955776)\n"
                                                               'frame = storage_address(frame, '
                                                               "'a2', 4294961176)\n"
                                                               'frame = storage_address(frame, '
                                                               "'a3', 4294954240)\n"
                                                               'frame = storage_move(state, frame, '
                                                               "'d0', 39, 16)\n"
                                                               'while True:\n'
                                                               '    for displacement, sentinel, '
                                                               'assignment in ((0, 511, 2), (80, '
                                                               '16383, 0), (160, 511, 3)):\n'
                                                               '        frame = '
                                                               '_restore_city_order_word_fields(state, '
                                                               'frame, displacement, sentinel, '
                                                               'assignment)\n'
                                                               '    frame = storage_move(state, '
                                                               "frame, 'd1', state.read(frame.a1 + "
                                                               '240, 2), 16)\n'
                                                               '    frame = '
                                                               'storage_arithmetic(state, frame, '
                                                               "'d1', 127, 16, True, True)\n"
                                                               '    if frame.status_word & 4:\n'
                                                               '        frame = '
                                                               "storage_move(state, frame, 'd1', "
                                                               '65535, 16)\n'
                                                               '    else:\n'
                                                               '        frame = '
                                                               'storage_multiply(state, frame, '
                                                               "'d1', 100)\n"
                                                               '    frame = '
                                                               'storage_write_next(state, frame, '
                                                               "'a2', 2, frame.d1)\n"
                                                               '    for displacement, sentinel, '
                                                               'assignment in ((320, 511, 4), '
                                                               '(400, 1023, 0)):\n'
                                                               '        frame = '
                                                               '_restore_city_order_word_fields(state, '
                                                               'frame, displacement, sentinel, '
                                                               'assignment)\n'
                                                               '    frame = '
                                                               "storage_address_step(frame, 'a1', "
                                                               '2)\n'
                                                               '    frame, again = '
                                                               "storage_dbra(frame, 'd0')\n"
                                                               '    if not again:\n'
                                                               '        return frame',
                                                       'returns': 'StorageFrame',
                                                       'signature': 'state: StorageState, frame: '
                                                                    'StorageFrame'},
 'restore_loaded_city_fields': {'flow': "raise Boundary('legacy partial storage phase has no whole "
                                        "entry; use the full save or restore core')",
                                'returns': 'Cursor',
                                'signature': 'state: StorageState, source: Cursor, entry_frame: '
                                             'StorageFrame=None'},
 'restore_loaded_officer_fields': {'flow': "raise Boundary('legacy partial storage phase has no "
                                           "whole entry; use the full save or restore core')",
                                   'returns': 'Cursor',
                                   'signature': 'state: StorageState, source: Cursor, entry_frame: '
                                                'StorageFrame=None'},
 'restore_saved_force_and_battle_fields': {'flow': "raise Boundary('legacy partial storage phase "
                                                   'has no whole entry; use the full save or '
                                                   "restore core')",
                                           'returns': 'Cursor',
                                           'signature': 'state: StorageState, source: Cursor, '
                                                        'entry_frame: StorageFrame=None'},
 'restore_saved_force_record_columns': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                                'checked_cursor(destination, state)\n'
                                                'if destination.base != frame.a1:\n'
                                                "    raise ValueError('restore force destination "
                                                "differs from entry A1')\n"
                                                'returned = '
                                                'restore_saved_force_record_columns_frame_fields(state, '
                                                'frame)\n'
                                                'destination.base = returned.a1\n'
                                                'return None',
                                        'returns': 'None',
                                        'signature': 'state: StorageState, destination: Cursor, '
                                                     'entry_frame: StorageFrame=None'},
 'restore_saved_force_record_columns_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                             "for role, address in (('a2', "
                                                             "4294955776), ('a3', 4294955792), "
                                                             "('a4', 4294955808), ('a5', "
                                                             '4294955824)):\n'
                                                             '    frame = storage_address(frame, '
                                                             'role, address)\n'
                                                             'frame = storage_move(state, frame, '
                                                             "'d0', 15, 16)\n"
                                                             'while True:\n'
                                                             "    for source in ('a2', 'a3', 'a4', "
                                                             "'a5'):\n"
                                                             '        frame, value = '
                                                             'storage_read_next(state, frame, '
                                                             'source, 1)\n'
                                                             '        frame = '
                                                             'storage_write_next(state, frame, '
                                                             "'a1', 1, value)\n"
                                                             '    frame, again = '
                                                             "storage_dbra(frame, 'd0')\n"
                                                             '    if not again:\n'
                                                             '        return frame',
                                                     'returns': 'StorageFrame',
                                                     'signature': 'state: StorageState, frame: '
                                                                  'StorageFrame'},
 'restore_saved_game_state': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                      'returned = restore_saved_game_state_frame_fields(state, '
                                      'frame)\n'
                                      'if returned.status_word & 1:\n'
                                      '    return RestoreOutcome(False, None)\n'
                                      'return RestoreOutcome(True, '
                                      'state.table(returned.a0).cursor())',
                              'returns': 'RestoreOutcome',
                              'signature': 'state: StorageState, entry_frame: StorageFrame=None'},
 'restore_saved_game_state_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                   'frame = storage_call(state, frame, '
                                                   'validate_saved_header_and_checksum_frame_fields, '
                                                   '35428)\n'
                                                   'if frame.status_word & 1:\n'
                                                   '    return frame\n'
                                                   'for source, clear_address, destination in '
                                                   '((2097429, 4294964858, 4294964859), (2097431, '
                                                   '4294964860, 4294964861), (2097433, 4294964862, '
                                                   '4294964863), (2097435, None, 4294964084), '
                                                   '(2097437, None, 4294964085), (2097439, '
                                                   '4294963154, 4294963155), (2097441, 4294963172, '
                                                   '4294963173), (2097443, 4294963158, '
                                                   '4294963159), (2097445, 4294963160, '
                                                   '4294963161)):\n'
                                                   '    if clear_address is not None:\n'
                                                   '        frame = storage_clear_memory(state, '
                                                   'frame, clear_address, 2)\n'
                                                   '    frame = storage_write(state, frame, '
                                                   'destination, 1, state.read(source, 1))\n'
                                                   "frame = storage_address(frame, 'a0', 2097447)\n"
                                                   'frame = _read_saved_column_fields(state, '
                                                   'frame, (4294942720, 5, 1, 40, 35558))\n'
                                                   "frame = storage_address(frame, 'a1', "
                                                   '4294963114)\n'
                                                   'for _ in range(5):\n'
                                                   '    frame, value = storage_read_next(state, '
                                                   "frame, 'a0', 1)\n"
                                                   '    frame = storage_write_next(state, frame, '
                                                   "'a1', 1, value)\n"
                                                   "    frame = storage_address_step(frame, 'a0', "
                                                   '1)\n'
                                                   'frame = _read_saved_columns_fields(state, '
                                                   'frame, ((4294942760, 8, 1, 40, 35612), '
                                                   '(4294942800, 8, 1, 256, 35632), (4294955776, '
                                                   '8, 2, 256, 35652), (4294956288, 9, 2, 256, '
                                                   '35672)))\n'
                                                   'frame = storage_call(state, frame, '
                                                   'restore_saved_officer_positions_frame_fields, '
                                                   '35676)\n'
                                                   'frame = _read_saved_columns_fields(state, '
                                                   'frame, ((4294947328, 8, 2, 256, 35696), '
                                                   '(4294947840, 8, 2, 256, 35716), (4294948352, '
                                                   '8, 2, 256, 35736), (4294955776, 5, 2, 256, '
                                                   '35756)))\n'
                                                   'frame = storage_call(state, frame, '
                                                   'restore_scaled_officer_parameter_words_frame_fields, '
                                                   '35760)\n'
                                                   'frame = _read_saved_columns_fields(state, '
                                                   'frame, ((4294950912, 10, 2, 256, 35780), '
                                                   '(4294950400, 10, 2, 256, 35800), (4294951424, '
                                                   '7, 1, 256, 35820), (4294951680, 7, 1, 256, '
                                                   '35840), (4294951936, 5, 1, 256, 35860), '
                                                   '(4294952192, 7, 1, 256, 35880), (4294952704, '
                                                   '5, 1, 256, 35900), (4294952960, 14, 4, 256, '
                                                   '35920), (4294953984, 8, 1, 256, 35940)))\n'
                                                   'frame = _read_saved_columns_fields(state, '
                                                   'frame, ((4294959104, 20, 4, 40, 35960), '
                                                   '(4294959264, 20, 4, 40, 35980), (4294959424, '
                                                   '10, 4, 40, 36000), (4294959584, 10, 4, 40, '
                                                   '36020), (4294959744, 7, 4, 40, 36040), '
                                                   '(4294959904, 7, 4, 40, 36060), (4294960064, 7, '
                                                   '4, 40, 36080), (4294960544, 7, 4, 40, 36100), '
                                                   '(4294964264, 4, 1, 40, 36120)))\n'
                                                   'frame = storage_call(state, frame, '
                                                   'normalize_saved_city_owner_sentinels_frame_fields, '
                                                   '36124)\n'
                                                   'frame = _read_saved_column_fields(state, '
                                                   'frame, (4294960704, 9, 2, 16, 36144))\n'
                                                   'frame = storage_call(state, frame, '
                                                   'normalize_saved_force_head_sentinels_frame_fields, '
                                                   '36148)\n'
                                                   'frame = _read_saved_column_fields(state, '
                                                   'frame, (4294964320, 9, 2, 40, 36168))\n'
                                                   'frame = storage_call(state, frame, '
                                                   'normalize_saved_city_head_sentinels_frame_fields, '
                                                   '36172)\n'
                                                   'frame = _read_saved_column_fields(state, '
                                                   'frame, (4294960736, 20, 4, 40, 36192))\n'
                                                   'for destination in (4294960896, 4294960897):\n'
                                                   '    frame, value = storage_read_next(state, '
                                                   "frame, 'a0', 1)\n"
                                                   '    frame = storage_write(state, frame, '
                                                   'destination, 1, value)\n'
                                                   "    frame = storage_address_step(frame, 'a0', "
                                                   '1)\n'
                                                   "frame = storage_address(frame, 'a1', "
                                                   '4294960912)\n'
                                                   "frame = storage_move(state, frame, 'd2', 31, "
                                                   '16)\n'
                                                   'while True:\n'
                                                   '    frame, value = storage_read_next(state, '
                                                   "frame, 'a0', 1)\n"
                                                   '    frame = storage_write_next(state, frame, '
                                                   "'a1', 1, value)\n"
                                                   "    frame = storage_address_step(frame, 'a0', "
                                                   '1)\n'
                                                   "    frame, again = storage_dbra(frame, 'd2')\n"
                                                   '    if not again:\n'
                                                   '        break\n'
                                                   'frame = _read_saved_columns_fields(state, '
                                                   'frame, ((4294961016, 17, 4, 40, 36246), '
                                                   '(4294955776, 9, 2, 40, 36266), (4294955856, '
                                                   '14, 2, 40, 36286), (4294955936, 9, 2, 40, '
                                                   '36306), (4294956016, 7, 2, 40, 36326), '
                                                   '(4294956096, 9, 2, 40, 36346), (4294956176, '
                                                   '10, 2, 40, 36366)))\n'
                                                   'frame = storage_call(state, frame, '
                                                   'restore_city_orders_and_action_flags_frame_fields, '
                                                   '36370)\n'
                                                   'frame = _read_saved_columns_fields(state, '
                                                   'frame, ((4294955776, 6, 1, 16, 36390), '
                                                   '(4294955792, 6, 1, 16, 36410), (4294955808, 8, '
                                                   '1, 16, 36430), (4294955824, 4, 1, 16, '
                                                   '36450)))\n'
                                                   "frame = storage_address(frame, 'a1', "
                                                   '4294961656)\n'
                                                   'frame = storage_call(state, frame, '
                                                   'restore_saved_force_record_columns_frame_fields, '
                                                   '36458)\n'
                                                   'frame = _read_saved_columns_fields(state, '
                                                   'frame, ((4294961720, 1, 1, 40, 36478), '
                                                   '(4294961800, 2, 1, 768, 36498), (4294962568, '
                                                   '18, 4, 40, 36518), (4294962728, 20, 4, 40, '
                                                   '36538), (4294964624, 2, 1, 16, 36558)))\n'
                                                   'frame = storage_call(state, frame, '
                                                   'read_packed_transport_orders_frame_fields, '
                                                   '36562)\n'
                                                   'frame = storage_call(state, frame, '
                                                   'read_packed_group_stream_frame_fields, 36566)\n'
                                                   'frame = storage_write(state, frame, 16723968, '
                                                   '2, 65535)\n'
                                                   'frame = storage_clear_memory(state, frame, '
                                                   '4294965110, 2)\n'
                                                   'value = state.read(4294946814, 2)\n'
                                                   'original_d0 = frame.d0\n'
                                                   'frame = storage_replace(frame, d0=frame.d0 & '
                                                   '4294901760 | value)\n'
                                                   "frame = storage_arithmetic(state, frame, 'd0', "
                                                   '1, 16)\n'
                                                   'state.write(4294946814, 2, low16(frame.d0))\n'
                                                   'return storage_replace(frame, d0=original_d0)',
                                           'returns': 'StorageFrame',
                                           'signature': 'state: StorageState, frame: StorageFrame'},
 'restore_saved_links_and_orders': {'flow': "raise Boundary('legacy partial storage phase has no "
                                            "whole entry; use the full save or restore core')",
                                    'returns': 'Cursor',
                                    'signature': 'state: StorageState, source: Cursor, '
                                                 'entry_frame: StorageFrame=None'},
 'restore_saved_metadata': {'flow': "raise Boundary('legacy partial storage phase has no whole "
                                    "entry; use the full save or restore core')",
                            'returns': 'None',
                            'signature': 'state: StorageState, entry_frame: StorageFrame=None'},
 'restore_saved_officer_positions': {'flow': 'frame = storage_legacy_entry(state, entry_frame)\n'
                                             'returned = '
                                             'restore_saved_officer_positions_frame_fields(state, '
                                             'frame)\n'
                                             'return None',
                                     'returns': 'None',
                                     'signature': 'state: StorageState, entry_frame: '
                                                  'StorageFrame=None'},
 'restore_saved_officer_positions_frame_fields': {'flow': 'frame = storage_entry(state, frame)\n'
                                                          "frame = storage_address(frame, 'a2', "
                                                          '4294943056)\n'
                                                          "frame = storage_address(frame, 'a3', "
                                                          '4294955776)\n'
                                                          "frame = storage_address(frame, 'a4', "
                                                          '4294956288)\n'
                                                          'frame = storage_move(state, frame, '
                                                          "'d0', 255, 16)\n"
                                                          'while True:\n'
                                                          "    for source in ('a3', 'a4'):\n"
                                                          '        frame, value = '
                                                          'storage_read_next(state, frame, source, '
                                                          '2)\n'
                                                          '        frame = storage_move(state, '
                                                          "frame, 'd1', value, 16)\n"
                                                          '        frame = storage_shift(state, '
                                                          "frame, 'd1', 7, 16)\n"
                                                          '        frame = '
                                                          "storage_write_next(state, frame, 'a2', "
                                                          '2, frame.d1)\n'
                                                          '    frame, again = storage_dbra(frame, '
                                                          "'d0')\n"
                                                          '    if not again:\n'
                                                          '        return frame',
                                                  'returns': 'StorageFrame',
                                                  'signature': 'state: StorageState, frame: '
                                                               'StorageFrame',
                                                  'slots': {7: ('position_shift', 1, 8)}},
 'restore_scaled_officer_parameter_words': {'flow': 'frame = storage_legacy_entry(state, '
                                                    'entry_frame)\n'
                                                    'returned = '
                                                    'restore_scaled_officer_parameter_words_frame_fields(state, '
                                                    'frame)\n'
                                                    'return None',
                                            'returns': 'None',
                                            'signature': 'state: StorageState, entry_frame: '
                                                         'StorageFrame=None'},
 'restore_scaled_officer_parameter_words_frame_fields': {'flow': 'frame = storage_entry(state, '
                                                                 'frame)\n'
                                                                 'frame = storage_address(frame, '
                                                                 "'a1', 4294955776)\n"
                                                                 'frame = storage_address(frame, '
                                                                 "'a2', 4294948864)\n"
                                                                 'frame = storage_move(state, '
                                                                 "frame, 'd0', 255, 16)\n"
                                                                 'while True:\n'
                                                                 '    frame, value = '
                                                                 'storage_read_next(state, frame, '
                                                                 "'a1', 2)\n"
                                                                 '    frame = storage_move(state, '
                                                                 "frame, 'd1', value, 16)\n"
                                                                 '    frame = '
                                                                 'storage_multiply(state, frame, '
                                                                 "'d1', 5)\n"
                                                                 '    frame = '
                                                                 'storage_write_next(state, frame, '
                                                                 "'a2', 2, frame.d1)\n"
                                                                 '    frame, again = '
                                                                 "storage_dbra(frame, 'd0')\n"
                                                                 '    if not again:\n'
                                                                 '        return frame',
                                                         'returns': 'StorageFrame',
                                                         'signature': 'state: StorageState, frame: '
                                                                      'StorageFrame'}})
APPROVED.setdefault('business_streams', set()).update(('read_masked_fixed_count_frame_fields', 'read_packed_group_stream_frame_fields', 'read_packed_transport_orders_frame_fields', 'validate_saved_header_and_checksum_frame_fields'))
APPROVED.setdefault('contexts_load', set()).update(('RestoreOutcome',))
APPROVED.setdefault('contexts_storage_fields', set()).update(('StorageFrame', 'storage_address', 'storage_address_step', 'storage_arithmetic', 'storage_call', 'storage_clear_memory', 'storage_dbra', 'storage_divide', 'storage_entry', 'storage_legacy_entry', 'storage_logic', 'storage_move', 'storage_multiply', 'storage_read_next', 'storage_replace', 'storage_shift', 'storage_write', 'storage_write_next'))
APPROVED.setdefault('domain', set()).update(('Boundary', 'Byte', 'Cursor', 'Long', 'StorageState', 'checked_cursor', 'low16', 's16'))
