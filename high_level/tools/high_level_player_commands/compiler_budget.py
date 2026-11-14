"""Draft restricted semantic frontend and ordinary GNU target lowering.

Generated development draft; Python rules remain in business_budget.
Only these explicit structural forms and declared literal rules are admitted.
Not a general Python compiler or a complete CPU equivalence proof.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import BUDGET_BINDINGS

APPROVED = {'contexts_budget': {'DecimalPlaceResult', 'CommandColumns',
 'ResourceRowInput', 'CommittedResourceRowInput', 'ResourceRowsInput', 'ResourceRowsResult'},
 'contexts_numeric': {'DecimalMemory','DecimalPlaceFields','DecimalTransactionFields'},
 'domain': {'Boundary',
            'Cursor',
            'GameState',
            'Long',
            'Table',
            'Word',
            'checked_cursor',
            'checked_state',
            'checked_table',
            'descending_inclusive',
            'divu_retained',
            'low16',
            'negative_word',
            'replace_byte',
            'replace_word',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'}}

DECLARATIONS = {'prepare_budget_summary_panel': {'signature': 'state: GameState',
                                  'returns': 'Cursor',
                                  'flow': 'checked_state(state)\n'
                                          'out = '
                                          "state.command_queue.cursor(state.scalar('command_queue_offset'))\n"
                                          'pair = CommandColumns(out, 16)\n'
                                          'pair.append_pair(6, 6)\n'
                                          'pair.append_pair(49954, 50082)\n'
                                          'pair.append_run(32768, 32768, 6)\n'
                                          'pair.next_row()\n'
                                          'for word in (6, 50210, 50048):\n'
                                          '    out.append_word(word)\n'
                                          'for _ in range(4):\n'
                                          '    out.append_word(50049)\n'
                                          'out.append_word(52096)\n'
                                          'pair.append_pair(6, 6)\n'
                                          'pair.append_pair(50338, 50466)\n'
                                          'pair.append_pair(50050, 50050)\n'
                                          'append_numbered_budget_columns(state, out, 49269, 3)\n'
                                          'pair.append_pair(52098, 52098)\n'
                                          'pair.next_row()\n'
                                          'for word in (6, 50594, 50050):\n'
                                          '    out.append_word(word)\n'
                                          'for _ in range(4):\n'
                                          '    out.append_word(49153)\n'
                                          'out.append_word(52098)\n'
                                          'pair.append_pair(6, 6)\n'
                                          'pair.append_pair(50722, 50850)\n'
                                          'pair.append_pair(50050, 50050)\n'
                                          'append_numbered_budget_columns(state, out, 49277, 3)\n'
                                          'pair.append_pair(52098, 52098)\n'
                                          'pair.next_row()\n'
                                          'for word in (6, 50978, 54144):\n'
                                          '    out.append_word(word)\n'
                                          'for _ in range(4):\n'
                                          '    out.append_word(54145)\n'
                                          'out.append_word(56192)\n'
                                          'out.set_word(32, 6)\n'
                                          'out.set_word(16, 6)\n'
                                          'out.append_word(6)\n'
                                          'out.set_word(32, 51362)\n'
                                          'out.set_word(16, 51234)\n'
                                          'out.append_word(51106)\n'
                                          'for _ in range(6):\n'
                                          '    out.set_word(32, 32768)\n'
                                          '    out.set_word(16, 32768)\n'
                                          '    out.append_word(32768)\n'
                                          'out.put_word(0)\n'
                                          "state.set_scalar('command_queue_offset', "
                                          "u16(state.scalar('command_queue_offset') + 192))\n"
                                          'return out'},
 'append_numbered_budget_columns': {'signature': 'state: GameState, out: Cursor, tile: Word, latch: '
                                                 'Word',
                                    'returns': 'Word',
                                    'flow': 'checked_state(state)\n'
                                            'checked_cursor(out, state)\n'
                                            'uint(tile, 16)\n'
                                            'uint(latch, 16)\n'
                                            'return CommandColumns(out, 16).append_numbered_pair(tile, '
                                            'latch + 1)'},
 'prepare_compact_budget_summary_panel': {'signature': 'state: GameState',
                                          'returns': 'Cursor',
                                          'flow': 'checked_state(state)\n'
                                                  'out = '
                                                  "state.command_queue.cursor(state.scalar('command_queue_offset'))\n"
                                                  'pair = CommandColumns(out, 16)\n'
                                                  'for word in (6, 50210, 50048):\n'
                                                  '    out.append_word(word)\n'
                                                  'for _ in range(4):\n'
                                                  '    out.append_word(50049)\n'
                                                  'out.append_word(52096)\n'
                                                  'pair.append_pair(6, 6)\n'
                                                  'pair.append_pair(50338, 50466)\n'
                                                  'pair.append_pair(50050, 50050)\n'
                                                  'append_numbered_budget_columns(state, out, 49285, '
                                                  '3)\n'
                                                  'pair.append_pair(52098, 52098)\n'
                                                  'pair.next_row()\n'
                                                  'for word in (6, 50594, 50050):\n'
                                                  '    out.append_word(word)\n'
                                                  'for _ in range(4):\n'
                                                  '    out.append_word(49153)\n'
                                                  'out.append_word(52098)\n'
                                                  'pair.append_pair(6, 6)\n'
                                                  'pair.append_pair(50722, 50850)\n'
                                                  'pair.append_pair(50050, 50050)\n'
                                                  'append_numbered_budget_columns(state, out, 49293, '
                                                  '1)\n'
                                                  'append_numbered_budget_columns(state, out, 49153, '
                                                  '1)\n'
                                                  'pair.append_pair(52098, 52098)\n'
                                                  'pair.next_row()\n'
                                                  'for word in (6, 50978, 54144):\n'
                                                  '    out.append_word(word)\n'
                                                  'for _ in range(4):\n'
                                                  '    out.append_word(54145)\n'
                                                  'out.append_word(56192)\n'
                                                  'out.put_word(0)\n'
                                                  "state.set_scalar('command_queue_offset', "
                                                  "u16(state.scalar('command_queue_offset') + 112))\n"
                                                  'return out'},
 'select_descriptor_portrait_parts': {'signature': 'state: GameState, retained_mask_high: Word=0',
                                      'returns': 'None',
                                      'flow': 'checked_state(state)\n'
                                              'uint(retained_mask_high, 16)\n'
                                              'descriptor = '
                                              "state.table(state.scalar('active_descriptor'))\n"
                                              'first = descriptor.byte(1)\n'
                                              'second = descriptor.byte(2)\n'
                                              'source = state.portrait_pair_catalog.cursor()\n'
                                              'index = u16(0)\n'
                                              'while True:\n'
                                              '    if source.byte() == first:\n'
                                              '        if source.byte(1) == second:\n'
                                              '            break\n'
                                              '    source.base = source.advance(2).base\n'
                                              '    index = u16(index + 1)\n'
                                              'offset = u16((index << 1) + index)\n'
                                              'state.portrait_masks.set_byte(1, '
                                              'state.portrait_part_masks.byte(offset))\n'
                                              'state.portrait_masks.set_byte(3, '
                                              'state.portrait_part_masks.byte(offset, 1))\n'
                                              'state.portrait_masks.set_byte(5, '
                                              'state.portrait_part_masks.byte(offset, 2))\n'
                                              "if not state.scalar('portrait_flags_BYTE') & 1:\n"
                                              '    for offset in (0, 2, 4):\n'
                                              '        selected = find_first_set_mask_bit(state, '
                                              'u32(retained_mask_high << 16 | '
                                              'state.portrait_masks.word(offset)))\n'
                                              '        state.portrait_first_bits.set_word(offset, '
                                              'selected)'},
 'find_first_set_mask_bit': {'signature': 'state: GameState, mask: Long',
                             'returns': 'Word',
                             'flow': 'checked_state(state)\n'
                                     'uint(mask, 32)\n'
                                     'if mask == 0:\n'
                                     "    raise Boundary('original modulo32 bit search never finds a "
                                     "set bit')\n"
                                     'bit = u16(0)\n'
                                     'while not mask & 1 << (bit & 31):\n'
                                     '    bit = u16(bit + 1)\n'
                                     'return bit'},
 'prepare_command_amount_modal': {'signature': 'state: GameState',
                                  'returns': 'Cursor',
                                  'flow': 'checked_state(state)\n'
                                          'out = '
                                          "state.command_queue.cursor(state.scalar('command_queue_offset'))\n"
                                          'append_amount_modal_frame(state, out)\n'
                                          'append_amount_modal_descriptor_limit(state, out)\n'
                                          "state.set_scalar('command_queue_offset', "
                                          "u16(state.scalar('command_queue_offset') + 120))\n"
                                          'return out'},
 'append_amount_modal_frame': {'signature': 'state: GameState, out: Cursor',
                               'returns': 'None',
                               'flow': 'checked_state(state)\n'
                                       'checked_cursor(out, state)\n'
                                       'pair = CommandColumns(out, 30)\n'
                                       'pair.append_pair(13, 13)\n'
                                       'pair.append_pair(49332, 49716)\n'
                                       'pair.append_pair(50048, 54144)\n'
                                       'pair.append_run(50049, 54145, 11)\n'
                                       'pair.append_pair(52096, 56192)\n'
                                       'pair.next_row()'},
 'append_amount_modal_descriptor_limit': {'signature': 'state: GameState, out: Cursor',
                                          'returns': 'None',
                                          'flow': 'checked_state(state)\n'
                                                  'checked_cursor(out, state)\n'
                                                  'pair = CommandColumns(out, 30)\n'
                                                  'pair.append_pair(13, 13)\n'
                                                  'pair.append_pair(49460, 49588)\n'
                                                  'pair.append_pair(50050, 50050)\n'
                                                  'out.put_word(49233)\n'
                                                  'out.set_word(30, 49234)\n'
                                                  'out.set_word(2, 49235)\n'
                                                  'out.set_word(32, 49236)\n'
                                                  'out.base = out.advance(4).base\n'
                                                  'pair.append_run(49153, 49153, 3)\n'
                                                  'descriptor = '
                                                  "state.table(state.scalar('active_descriptor'))\n"
                                                  'value = descriptor.byte(5)\n'
                                                  'value = u16(value << 8) | descriptor.byte(6)\n'
                                                  'value = u32(value << 8) | descriptor.byte(7)\n'
                                                  'value = u32(value << 8) | descriptor.byte(8)\n'
                                                  "state.set_scalar('amount_limit', value)\n"
                                                  'append_six_place_decimal_value(state, value, 50054, '
                                                  '49153, state.decimal_scratch.cursor())\n'
                                                  'digits = state.decimal_scratch.cursor()\n'
                                                  'for _ in range(6):\n'
                                                  '    pair.append_pair(49153, digits.next_word())\n'
                                                  'pair.append_pair(52098, 52098)\n'
                                                  'out.set_word(30, 0)'},
 'append_selected_command_row_label': {'signature': 'state: GameState',
                                       'returns': 'None',
                                       'flow': 'checked_state(state)\n'
                                               "if not state.scalar('display_flags_BYTE') & 8:\n"
                                               "    row = state.scalar('command_row')\n"
                                               '    x = u16(u16(u16(row << 1) + '
                                               "state.scalar('command_row')) << 3)\n"
                                               '    state.append_command_label(state.command_row_label, '
                                               'u16(x + 56), 200, 0)'},
 'clear_command_amount_page': {'signature': 'state: GameState',
                               'returns': 'Cursor',
                               'flow': 'checked_state(state)\n'
                                       'out = '
                                       "state.command_queue.cursor(state.scalar('command_queue_offset'))\n"
                                       'for offset in (90, 60, 30):\n'
                                       '    out.set_word(offset, 13)\n'
                                       'out.append_word(13)\n'
                                       'for offset, value in ((90, 49716), (60, 49588), (30, 49460)):\n'
                                       '    out.set_word(offset, value)\n'
                                       'out.append_word(49332)\n'
                                       'for _ in range(13):\n'
                                       '    for offset in (90, 60, 30):\n'
                                       '        out.set_word(offset, 32768)\n'
                                       '    out.append_word(32768)\n'
                                       'out.base = out.advance(90).base\n'
                                       'position = u16(50098)\n'
                                       'for _ in range(10):\n'
                                       '    out.append_word(14)\n'
                                       '    out.append_word(position)\n'
                                       '    position = u16(position + 128)\n'
                                       '    for _ in range(14):\n'
                                       '        out.append_word(32768)\n'
                                       'out.put_word(0)\n'
                                       "state.set_scalar('command_queue_offset', "
                                       "u16(state.scalar('command_queue_offset') + 440))\n"
                                       'return out'},
 'prepare_budget_amount_page': {'signature': "state: GameState",
  'returns': "Cursor",
  'flow':
          "checked_state(state)\n"
          "out = state.command_queue.cursor(state.scalar('command_queue_offset'))\n"
          "for word in (11, 0xC5B2, 0xC380): out.append_word(word)\n"
          "for _ in range(9): out.append_word(0xC381)\n"
          "out.append_word(0xCB80)\n"
          "pair = CommandColumns(out, 26)\n"
          "pair.append_pair(11, 11); pair.append_pair(0xC632, 0xC6B2); pair.append_pair(0xC382, 0xC382)\n"
          "pair.append_run(0xC001, 0xC001, 9); pair.append_pair(0xCB82, 0xCB82); pair.next_row()\n"
          "pair.append_pair(11, 11); pair.append_pair(0xC732, 0xC7B2); pair.append_pair(0xC382, 0xC382)\n"
          "out.put_word(0xC051); out.set_word(26, 0xC052); out.set_word(2, 0xC053); out.set_word(28, 0xC054)\n"
          "out.base = out.advance(4).base\n"
          "pair.append_pair(0xC001, 0xC001)\n"
          "append_six_place_decimal_value(state, state.scalar('selected_amount'), 0xC386, 0xC001, state.decimal_scratch.cursor())\n"
          "digits = state.decimal_scratch.cursor()\n"
          "for _ in range(6): pair.append_pair(0xC001, digits.next_word())\n"
          "pair.append_pair(0xCB82, 0xCB82); pair.next_row()\n"
          "for word in (11, 0xC832, 0xD380): out.append_word(word)\n"
          "for _ in range(9): out.append_word(0xD381)\n"
          "out.append_word(0xDB80); out.put_word(0)\n"
          "state.set_scalar('command_queue_offset', u16(state.scalar('command_queue_offset') + 156))\n"
          "return prepare_command_amount_modal(state)\n"},
 'step_budget_amount_controls': {'signature': "state: GameState",
  'returns': "None",
  'flow':
          "checked_state(state)\n"
          "held = state.scalar('held_controls_BYTE') & 12\n"
          "if held:\n"
          "    timer = u16(state.scalar('repeat_timer') - 1); state.set_scalar('repeat_timer', timer)\n"
          "    if timer != 0: return\n"
          "    state.set_scalar('repeat_timer', 12)\n"
          "    if not held & 8:\n"
          "        place = state.scalar('amount_place')\n"
          "        offset = u16(u16(5 - place) << 2)\n"
          "        threshold = state.amount_place_thresholds.long(offset)\n"
          "        if threshold > state.scalar('amount_limit'): return\n"
          "        state.set_scalar('amount_place', u16(state.scalar('amount_place') - 1))\n"
          "    else:\n"
          "        place = u16(state.scalar('amount_place') + 1)\n"
          "        if place > 5: return\n"
          "        state.set_scalar('amount_place', place)\n"
          "else:\n"
          "    held = state.scalar('held_controls_BYTE') & 3\n"
          "    if held:\n"
          "        timer = u16(state.scalar('repeat_timer') - 1); state.set_scalar('repeat_timer', timer)\n"
          "        if timer != 0: return\n"
          "        state.set_scalar('repeat_timer', 12)\n"
          "        offset = u16(u16(5 - state.scalar('amount_place')) << 2)\n"
          "        if not held & 2:\n"
          "            step = state.amount_value_steps.long(offset)\n"
          "            amount = u32(step + state.scalar('selected_amount'))\n"
          "            if amount > state.scalar('amount_limit'): return\n"
          "            state.set_scalar('selected_amount', amount)\n"
          "            cost = state.amount_cost_steps.long(offset)\n"
          "            state.set_scalar('cost_amount', u32(state.scalar('cost_amount') + cost))\n"
          "        else:\n"
          "            step = state.amount_value_steps.long(offset)\n"
          "            amount = state.scalar('selected_amount')\n"
          "            difference = u32(amount - step)\n"
          "            if amount < step: return\n"
          "            state.set_scalar('selected_amount', difference)\n"
          "            cost = state.amount_cost_steps.long(offset)\n"
          "            state.set_scalar('cost_amount', u32(state.scalar('cost_amount') - cost))\n"
          "    else: state.set_scalar('repeat_timer', 1)\n"
          "append_budget_cost_and_amount_values(state)\n"},
 'append_budget_cost_and_amount_values': {'signature': 'state: GameState',
                                          'returns': 'Cursor',
                                          'flow': 'checked_state(state)\n'
                                                  'out = '
                                                  "state.command_queue.cursor(state.scalar('command_queue_offset'))\n"
                                                  'append_six_place_decimal_value(state, '
                                                  "state.scalar('cost_amount'), 50054, 49153, "
                                                  'state.amount_digits.cursor())\n'
                                                  'out.append_word(6)\n'
                                                  'out.append_word(50874)\n'
                                                  'digits = state.amount_digits.cursor()\n'
                                                  'position = u16(0)\n'
                                                  'for _ in range(6):\n'
                                                  '    word = digits.next_word()\n'
                                                  '    if word == 49153:\n'
                                                  '        if position >= '
                                                  "state.scalar('amount_place'):\n"
                                                  '            word = u16(50054)\n'
                                                  '    out.append_word(word)\n'
                                                  '    position = u16(position + 1)\n'
                                                  'append_six_place_decimal_value(state, '
                                                  "state.scalar('selected_amount'), 50054, 49153, "
                                                  'state.amount_digits.cursor())\n'
                                                  'out.append_word(6)\n'
                                                  'out.append_word(51130)\n'
                                                  'digits = state.amount_digits.cursor()\n'
                                                  'for _ in range(6):\n'
                                                  '    out.append_word(digits.next_word())\n'
                                                  'out.put_word(0)\n'
                                                  "state.set_scalar('command_queue_offset', "
                                                  "u16(state.scalar('command_queue_offset') + 32))\n"
                                                  'return out'},
 'append_budget_place_highlight': {'signature': 'state: GameState',
                                   'returns': 'None',
                                   'flow': 'checked_state(state)\n'
                                           "if not state.scalar('display_flags_BYTE') & 16:\n"
                                           "    y = u16(u16(state.scalar('amount_place') << 3) + 232)\n"
                                           '    state.append_command_label(state.budget_place_label, '
                                           '104, y, 0)'},
 'append_budget_header_row': {'signature': 'state: GameState, out: Cursor',
                              'returns': 'None',
                              'flow': 'checked_state(state)\n'
                                      'checked_cursor(out, state)\n'
                                      'for word in (8, 50210, 50048):\n'
                                      '    out.append_word(word)\n'
                                      'for _ in range(6):\n'
                                      '    out.append_word(50049)\n'
                                      'out.append_word(52096)'},
 'append_budget_first_detail_rows': {'signature': 'state: GameState, out: Cursor',
                                     'returns': 'None',
                                     'flow': 'checked_state(state)\n'
                                             'checked_cursor(out, state)\n'
                                             'pair = CommandColumns(out, 20)\n'
                                             'pair.append_pair(8, 8)\n'
                                             'pair.append_pair(50338, 50466)\n'
                                             'pair.append_pair(50050, 50050)\n'
                                             'tile = append_four_budget_numbered_tiles(state, out, '
                                             '49297)\n'
                                             'append_four_budget_numbered_tiles(state, out, u16(tile + '
                                             '4))\n'
                                             'pair.append_run(49153, 49153, 2)\n'
                                             'pair.append_pair(52098, 52098)\n'
                                             'pair.next_row()\n'
                                             'for word in (8, 50594, 50050):\n'
                                             '    out.append_word(word)\n'
                                             'for _ in range(6):\n'
                                             '    out.append_word(49153)\n'
                                             'out.append_word(52098)'},
 'append_budget_second_detail_row': {'signature': 'state: GameState, out: Cursor',
                                     'returns': 'None',
                                     'flow': 'checked_state(state)\n'
                                             'checked_cursor(out, state)\n'
                                             'pair = CommandColumns(out, 20)\n'
                                             'pair.append_pair(8, 8)\n'
                                             'pair.append_pair(50722, 50850)\n'
                                             'pair.append_pair(50050, 50050)\n'
                                             'for tile in (49297, 49305, 49297):\n'
                                             '    append_four_budget_numbered_tiles(state, out, tile)\n'
                                             'pair.append_pair(52098, 52098)\n'
                                             'pair.next_row()'},
 'append_budget_footer_row': {'signature': 'state: GameState, out: Cursor',
                              'returns': 'None',
                              'flow': 'checked_state(state)\n'
                                      'checked_cursor(out, state)\n'
                                      'for word in (8, 50978, 54144):\n'
                                      '    out.append_word(word)\n'
                                      'for _ in range(6):\n'
                                      '    out.append_word(54145)\n'
                                      'out.append_word(56192)'},
 'append_four_budget_numbered_tiles': {'signature': 'state: GameState, out: Cursor, tile: Word',
                                       'returns': 'Word',
                                       'flow': 'checked_state(state)\n'
                                               'checked_cursor(out, state)\n'
                                               'uint(tile, 16)\n'
                                               'pair = CommandColumns(out, 20)\n'
                                               'out.put_word(tile)\n'
                                               'tile = u16(tile + 1)\n'
                                               'out.set_word(20, tile)\n'
                                               'tile = u16(tile + 1)\n'
                                               'out.base = out.advance(2).base\n'
                                               'out.put_word(tile)\n'
                                               'tile = u16(tile + 1)\n'
                                               'out.set_word(20, tile)\n'
                                               'out.base = out.advance(2).base\n'
                                               'return u16(tile - 3)'},
 'append_six_place_decimal_value': {'signature': 'state: GameState, value: Long, digit_tile: Word, '
                                                 'blank_tile: Word, destination: Cursor',
                                    'returns': 'Cursor',
                                    'flow': 'checked_state(state)\n'
                                            'uint(value, 32)\n'
                                            'uint(digit_tile, 16)\n'
                                            'uint(blank_tile, 16)\n'
                                            'checked_cursor(destination, state)\n'
                                            'return _six_place_decimal_fields(DecimalMemory(state), '
                                            'value, digit_tile, blank_tile, destination).destination'},
 'append_decimal_value_place': {'signature': 'state: GameState, value: Long, divisor: Word, tile_base: '
                                             'Word, blank: Word, started: Word, out: Cursor',
                                'returns': 'DecimalPlaceResult',
                                'flow': 'checked_state(state)\n'
                                        'uint(value, 32)\n'
                                        'uint(divisor, 16)\n'
                                        'uint(tile_base, 16)\n'
                                        'uint(blank, 16)\n'
                                        'uint(started, 16)\n'
                                        'checked_cursor(out, state)\n'
                                        'result = _decimal_value_place_fields(DecimalMemory(state), '
                                        'value, divisor, tile_base, blank, started, out)\n'
                                        'return DecimalPlaceResult(result.remainder, result.started)'},
 'prepare_command_amount_limit': {'signature': "state: GameState",
  'returns': "Cursor",
  'flow':
          "checked_state(state)\n"
          "out = state.command_queue.cursor(state.scalar('command_queue_offset'))\n"
          "out.set_word(44, 9); out.set_word(22, 9); out.append_word(9)\n"
          "out.set_word(44, 0xC4BC); out.set_word(22, 0xC43C); out.append_word(0xC3BC)\n"
          "out.set_word(44, 0xD380); out.set_word(22, 0xC382); out.append_word(0xC380)\n"
          "for _ in range(7):\n"
          "    out.set_word(44, 0xD381); out.set_word(22, 0xC001); out.append_word(0xC381)\n"
          "out.set_word(20, 0xC386)\n"
          "out.set_word(44, 0xDB80); out.set_word(22, 0xCB82); out.append_word(0xCB80); out.set_word(44, 0)\n"
          "state.set_scalar('command_queue_offset', u16(state.scalar('command_queue_offset') + 66))\n"
          "offset = u16(state.scalar('current_city') << 2)\n"
          "state.set_scalar('amount_limit', state.city_gold.long(offset))\n"
          "records = state.command_price_records.cursor()\n"
          "limit_live_command_amount_by_price_record(state, records)\n"
          "append_six_place_decimal_value(state, state.scalar('amount_limit'), 0xC386, 0, state.amount_digits.cursor())\n"
          "state.set_scalar('repeat_timer', 1)\n"
          "state.set_scalar('display_flags_WORD', state.scalar('display_flags_WORD') | 0x8040)\n"
          "state.set_scalar('display_flags_WORD', state.scalar('display_flags_WORD') & 0xF9FF)\n"
          "return records\n"},
 'limit_live_command_amount_by_price_record': {'signature': 'state: GameState, records: Cursor',
                                               'returns': 'None',
                                               'flow': 'checked_state(state)\n'
                                                       'checked_cursor(records, state)\n'
                                                       "message = state.scalar('command_message')\n"
                                                       'if message != 147:\n'
                                                       '    while records.word() != message:\n'
                                                       '        records.base = records.advance(8).base\n'
                                                       '    limit = records.long(2)\n'
                                                       "    if limit < state.scalar('amount_limit'):\n"
                                                       "        state.set_scalar('amount_limit', "
                                                       'limit)\n'
                                                       '    places = records.word(6)\n'
                                                       "    state.set_scalar('amount_place', places)\n"
                                                       "    state.set_scalar('amount_maximum_place', "
                                                       'places)\n'
                                                       'else:\n'
                                                       '    roster = state.candidate_roster.cursor()\n'
                                                       '    count = u16(0)\n'
                                                       '    while True:\n'
                                                       '        member = roster.next_word()\n'
                                                       '        if negative_word(member):\n'
                                                       '            break\n'
                                                       '        if member & 16384:\n'
                                                       '            count = u16(count + 1)\n'
                                                       '    limit = u32(count * 25000)\n'
                                                       "    if limit < state.scalar('amount_limit'):\n"
                                                       "        state.set_scalar('amount_limit', "
                                                       'limit)\n'
                                                       "    state.set_scalar('amount_place', 5)\n"
                                                       "    state.set_scalar('amount_maximum_place', "
                                                       '5)'},
 'update_player_command_amount': {'signature': "state: GameState",
  'returns': "None",
  'flow':
          "checked_state(state)\n"
          "append_selected_command_amount(state)\n"
          "step_live_command_amount_controls(state)\n"
          "append_blinking_amount_place(state)\n"
          "if state.scalar('pressed_controls_BYTE') & 32:\n"
          "    amount = state.scalar('selected_amount'); state.set_scalar('committed_amount', amount)\n"
          "    if state.scalar('selected_amount') != 0:\n"
          "        state.set_scalar('command_sound', 520); state.set_scalar('ui_state', 4)\n"
          "elif state.scalar('pressed_controls_BYTE') & 16:\n"
          "    state.set_scalar('command_sound', 520); state.set_scalar('ui_state', 2); state.set_scalar('return_ui_state', 18)\n"},
 'append_selected_command_amount': {'signature': 'state: GameState',
                                    'returns': 'Cursor',
                                    'flow': 'checked_state(state)\n'
                                            'out = '
                                            "state.command_queue.cursor(state.scalar('command_queue_offset'))\n"
                                            'out.append_word(6)\n'
                                            'out.append_word(50240)\n'
                                            'append_six_place_decimal_value(state, '
                                            "state.scalar('selected_amount'), 50054, 0, "
                                            'state.selected_amount_digits.cursor())\n'
                                            'digits = state.selected_amount_digits.cursor()\n'
                                            'position = u16(0)\n'
                                            'for _ in range(6):\n'
                                            '    tile = digits.next_word()\n'
                                            '    if tile == 0:\n'
                                            '        tile = u16(50054 if position >= '
                                            "state.scalar('amount_place') else 49153)\n"
                                            '    out.append_word(tile)\n'
                                            '    position = u16(position + 1)\n'
                                            'out.put_word(0)\n'
                                            "state.set_scalar('command_queue_offset', "
                                            "u16(state.scalar('command_queue_offset') + 16))\n"
                                            'return out'},
 'step_live_command_amount_controls': {'signature': 'state: GameState',
                                       'returns': 'None',
                                       'flow': 'checked_state(state)\n'
                                               "held = state.scalar('held_controls_BYTE') & 12\n"
                                               'if held:\n'
                                               "    timer = u16(state.scalar('repeat_timer') - 1)\n"
                                               "    state.set_scalar('repeat_timer', timer)\n"
                                               '    if timer != 0:\n'
                                               '        return\n'
                                               "    state.set_scalar('repeat_timer', 12)\n"
                                               '    if not held & 8:\n'
                                               '        select_previous_amount_place(state)\n'
                                               '    else:\n'
                                               '        select_next_amount_place(state)\n'
                                               'else:\n'
                                               "    held = state.scalar('held_controls_BYTE') & 3\n"
                                               '    if held:\n'
                                               "        timer = u16(state.scalar('repeat_timer') - 1)\n"
                                               "        state.set_scalar('repeat_timer', timer)\n"
                                               '        if timer != 0:\n'
                                               '            return\n'
                                               "        state.set_scalar('repeat_timer', 12)\n"
                                               '        if not held & 2:\n'
                                               '            state.add_selected_cost()\n'
                                               '        else:\n'
                                               '            decrement_live_command_amount_small(state)\n'
                                               '    else:\n'
                                               "        state.set_scalar('repeat_timer', 1)"},
 'select_previous_amount_place': {'signature': 'state: GameState',
                                  'returns': 'None',
                                  'flow': 'checked_state(state)\n'
                                          "place = state.scalar('amount_place')\n"
                                          'lower = u16(place - 1)\n'
                                          'if place != 0:\n'
                                          '    if state.amount_digits.word(u16(lower << 1)) != 0:\n'
                                          "        state.set_scalar('amount_place', "
                                          "u16(state.scalar('amount_place') - 1))"},
 'select_next_amount_place': {'signature': 'state: GameState',
                              'returns': 'None',
                              'flow': 'checked_state(state)\n'
                                      "place = u16(state.scalar('amount_place') + 1)\n"
                                      "if place <= state.scalar('amount_maximum_place'):\n"
                                      "    state.set_scalar('amount_place', "
                                      "u16(state.scalar('amount_place') + 1))"},
 'decrement_live_command_amount_small': {'signature': 'state: GameState',
                                         'returns': 'None',
                                         'flow': 'checked_state(state)\n'
                                                 "offset = u16(state.scalar('amount_place') << 2)\n"
                                                 'step = state.command_value_steps.long(offset)\n'
                                                 "amount = state.scalar('selected_amount')\n"
                                                 'if amount >= step:\n'
                                                 "    state.set_scalar('selected_amount', u32(amount - "
                                                 'step))'},
 'append_blinking_amount_place': {'signature': "state: GameState",
  'returns': "None",
  'flow':
          "checked_state(state)\n"
          "if state.scalar('amount_blink_timer') >= 24: state.set_scalar('amount_blink_timer', 24)\n"
          "if not state.scalar('held_controls_WORD') & 48:\n"
          "    value = u16(state.scalar('amount_blink_timer') - 1); state.set_scalar('amount_blink_timer', value)\n"
          "    if state.scalar('amount_blink_timer') >= 12:\n"
          "        y = u16(u16(state.scalar('amount_place') << 3) + 256)\n"
          "        state.append_command_label(state.amount_place_highlight, 64, y, 0)\n"},
 'prepare_percentage_panel': {'signature': 'state: GameState',
                              'returns': 'Cursor',
                              'flow': 'checked_state(state)\n'
                                      'out = '
                                      "state.command_queue.cursor(state.scalar('command_queue_offset'))\n"
                                      'append_percentage_header_row(state, out)\n'
                                      'append_percentage_value_rows(state, out)\n'
                                      'append_percentage_footer_row(state, out)\n'
                                      'out.put_word(0)\n'
                                      "state.set_scalar('command_queue_offset', "
                                      "u16(state.scalar('command_queue_offset') + 88))\n"
                                      'return out'},
 'append_percentage_header_row': {'signature': 'state: GameState, out: Cursor',
                                  'returns': 'None',
                                  'flow': 'checked_state(state)\n'
                                          'checked_cursor(out, state)\n'
                                          'for word in (9, 50332, 50048):\n'
                                          '    out.append_word(word)\n'
                                          'for _ in range(7):\n'
                                          '    out.append_word(50049)\n'
                                          'out.append_word(52096)'},
 'append_percentage_value_rows': {'signature': 'state: GameState, out: Cursor',
                                  'returns': 'None',
                                  'flow': 'checked_state(state)\n'
                                          'checked_cursor(out, state)\n'
                                          'pair = CommandColumns(out, 22)\n'
                                          'pair.append_pair(9, 9)\n'
                                          'pair.append_pair(50460, 50588)\n'
                                          'pair.append_pair(50050, 50050)\n'
                                          'pair.append_numbered_pair(49193, 2)\n'
                                          'pair.append_numbered_pair(49201, 2)\n'
                                          'pair.append_run(49153, 49153, 3)\n'
                                          'pair.append_pair(52098, 52098)\n'
                                          'pair.next_row()'},
 'append_percentage_footer_row': {'signature': 'state: GameState, out: Cursor',
                                  'returns': 'None',
                                  'flow': 'checked_state(state)\n'
                                          'checked_cursor(out, state)\n'
                                          'for word in (9, 50716, 54144):\n'
                                          '    out.append_word(word)\n'
                                          'for _ in range(7):\n'
                                          '    out.append_word(54145)\n'
                                          'out.append_word(56192)'},
 'clear_percentage_panel': {'signature': 'state: GameState',
                            'returns': 'Cursor',
                            'flow': 'checked_state(state)\n'
                                    'out = '
                                    "state.command_queue.cursor(state.scalar('command_queue_offset'))\n"
                                    'for offset in (66, 44, 22):\n'
                                    '    out.set_word(offset, 9)\n'
                                    'out.append_word(9)\n'
                                    'for offset, word in ((66, 50716), (44, 50588), (22, 50460)):\n'
                                    '    out.set_word(offset, word)\n'
                                    'out.append_word(50332)\n'
                                    'for _ in range(9):\n'
                                    '    for offset in (66, 44, 22):\n'
                                    '        out.set_word(offset, 0)\n'
                                    '    out.append_word(0)\n'
                                    'out.set_word(66, 0)\n'
                                    "state.set_scalar('command_queue_offset', "
                                    "u16(state.scalar('command_queue_offset') + 88))\n"
                                    'return out'},
 'append_percentage_value': {'signature': 'state: GameState',
                             'returns': 'Cursor',
                             'flow': 'checked_state(state)\n'
                                     'append_six_place_decimal_value(state, '
                                     "state.scalar('percentage_value'), 50054, 49153, "
                                     'state.amount_digits.cursor())\n'
                                     'out = '
                                     "state.command_queue.cursor(state.scalar('command_queue_offset'))\n"
                                     'out.append_word(2)\n'
                                     'out.append_word(50600)\n'
                                     'tile = state.amount_digits.word(8)\n'
                                     'if tile == 49153:\n'
                                     "    if state.scalar('percentage_place') == 0:\n"
                                     '        tile = u16(50054)\n'
                                     'out.append_word(tile)\n'
                                     'out.append_word(state.amount_digits.word(10))\n'
                                     'out.put_word(0)\n'
                                     "state.set_scalar('command_queue_offset', "
                                     "u16(state.scalar('command_queue_offset') + 8))\n"
                                     'return out'},
 'step_percentage_controls': {'signature': 'state: GameState',
                              'returns': 'None',
                              'flow': 'checked_state(state)\n'
                                      "held = state.scalar('held_controls_BYTE') & 12\n"
                                      'if held:\n'
                                      "    timer = u16(state.scalar('repeat_timer') - 1)\n"
                                      "    state.set_scalar('repeat_timer', timer)\n"
                                      '    if timer != 0:\n'
                                      '        return\n'
                                      "    state.set_scalar('percentage_place', 1 if held & 8 else 0)\n"
                                      'else:\n'
                                      "    held = state.scalar('held_controls_BYTE') & 3\n"
                                      '    if held:\n'
                                      "        timer = u16(state.scalar('repeat_timer') - 1)\n"
                                      "        state.set_scalar('repeat_timer', timer)\n"
                                      '        if timer != 0:\n'
                                      '            return\n'
                                      "        state.set_scalar('repeat_timer', 12)\n"
                                      '        step = u16(1)\n'
                                      "        if state.scalar('percentage_place') == 0:\n"
                                      '            step = u16(10)\n'
                                      "        if not state.scalar('held_controls_BYTE') & 2:\n"
                                      "            changed = u16(state.scalar('percentage_value') + "
                                      'step)\n'
                                      "            state.set_scalar('percentage_value', changed)\n"
                                      "            if state.scalar('percentage_value') > 99:\n"
                                      "                state.set_scalar('percentage_value', "
                                      "u16(state.scalar('percentage_value') - step))\n"
                                      '        else:\n'
                                      "            changed = u16(state.scalar('percentage_value') - "
                                      'step)\n'
                                      "            state.set_scalar('percentage_value', changed)\n"
                                      '            if negative_word(changed):\n'
                                      "                state.set_scalar('percentage_value', "
                                      "u16(state.scalar('percentage_value') + step))\n"
                                      '    else:\n'
                                      "        state.set_scalar('repeat_timer', 1)"},
 'append_percentage_place_highlight': {'signature': 'state: GameState',
                                       'returns': 'None',
                                       'flow': 'checked_state(state)\n'
                                               "if not state.scalar('pressed_controls_BYTE') & 32:\n"
                                               "    if not state.scalar('display_flags_BYTE') & 8:\n"
                                               '        y = u16(160)\n'
                                               "        if state.scalar('percentage_place') != 0:\n"
                                               '            y = u16(y + 8)\n'
                                               '        '
                                               'state.append_command_label(state.percentage_place_highlight, '
                                               '88, y, 0)'},
 'prepare_resource_amount_panel': {'signature': "state: GameState",
  'returns': "Cursor",
  'flow':
          "checked_state(state)\n"
          "out = state.command_queue.cursor(state.scalar('command_queue_offset'))\n"
          "city = append_city_resource_amount_rows(state, out)\n"
          "committed = append_committed_resource_amount_rows(state, ResourceRowsInput(city.destination, city.numeric_carrier))\n"
          "out = committed.destination\n"
          "state.set_scalar('command_queue_offset', u16(state.scalar('command_queue_offset') + 364))\n"
          "state.set_scalar('amount_place', 5)\n"
          "state.set_scalar('repeat_timer', 1); state.set_scalar('repeat_timer', 1)\n"
          "state.set_scalar('display_flags_WORD', state.scalar('display_flags_WORD') | 0x8040)\n"
          "state.set_scalar('display_flags_WORD', state.scalar('display_flags_WORD') & 0xF9FF)\n"
          "return out\n"},
 'append_city_resource_amount_rows': {'signature': "state: GameState, out: Cursor",
  'returns': "ResourceRowsResult",
  'flow':
          "checked_state(state); checked_cursor(out, state)\n"
          "for word in (12, 0xC0B4, 0xC380): out.append_word(word)\n"
          "for _ in range(10): out.append_word(0xC381)\n"
          "out.append_word(0xCB80)\n"
          "value = state.city_gold.long(u16(state.scalar('current_city') << 2))\n"
          "formatted = _six_place_decimal_fields(DecimalMemory(state), value, 1, 0, state.resource_digits.cursor())\n"
          "first = append_live_resource_value_row(state, ResourceRowInput(out, replace_word(formatted.remainder, 0xC04D), 0xC1B4))\n"
          "out = first.destination\n"
          "value = state.city_food.long(u16(state.scalar('current_city') << 2))\n"
          "formatted = _six_place_decimal_fields(DecimalMemory(state), value, 1, 0, state.resource_digits.cursor())\n"
          "second = append_live_resource_value_row(state, ResourceRowInput(out, replace_word(formatted.remainder, 0xC051), 0xC2B4))\n"
          "out = second.destination\n"
          "for word in (12, 0xC334, 0xD380): out.append_word(word)\n"
          "for counter in descending_inclusive(9): out.append_word(0xD381)\n"
          "out.append_word(0xDB80)\n"
          "return ResourceRowsResult(out, replace_word(second.numeric_carrier, u16(counter - 1)))\n"},
 'append_live_resource_value_row': {'signature': "state: GameState, context: ResourceRowInput",
  'returns': "ResourceRowsResult",
  'flow':
          "checked_state(state)\n"
          "if type(context) is not ResourceRowInput: raise ValueError('complete live resource row input required')\n"
          "context.validate(state)\n"
          "out = context.destination; tile = low16(context.tile_carrier); row = context.row\n"
          "pair = CommandColumns(out, 28)\n"
          "pair.append_pair(12, 12); pair.append_pair(u16(row - 128), row); pair.append_pair(0xC382, 0xC382)\n"
          "out.put_word(tile); tile = u16(tile + 1); out.set_word(28, tile); tile = u16(tile + 1); out.base = out.advance(2).base\n"
          "out.put_word(tile); tile = u16(tile + 1); out.set_word(28, tile); out.base = out.advance(2).base\n"
          "pair.append_run(0xC001, 0xC001, 2)\n"
          "digits = state.resource_digits.cursor()\n"
          "for counter in descending_inclusive(5):\n"
          "    value = digits.next_word()\n"
          "    tile = u16(value + 0xC385) if value else u16(0xC001)\n"
          "    pair.append_pair(0xC001, tile)\n"
          "pair.append_pair(0xCB82, 0xCB82); pair.next_row()\n"
          "return ResourceRowsResult(out, replace_word(context.tile_carrier, u16(counter - 1)))\n"},
 'append_committed_resource_amount_rows': {'signature': "state: GameState, context: ResourceRowsInput",
  'returns': "ResourceRowsResult",
  'flow':
          "checked_state(state)\n"
          "if type(context) is not ResourceRowsInput: raise ValueError('full incoming numeric carrier required')\n"
          "context.validate(state)\n"
          "out = context.destination\n"
          "for word in (12, 0xC434, 0xC380): out.append_word(word)\n"
          "for _ in range(10): out.append_word(0xC381)\n"
          "out.append_word(0xCB80)\n"
          "first = append_committed_resource_value_row(state, CommittedResourceRowInput(out, replace_word(context.numeric_carrier, 0xC04D), 0xC534, state.scalar('committed_amount')))\n"
          "out = first.destination\n"
          "for word in (12, 0xC5B4, 0xC382): out.append_word(word)\n"
          "for _ in range(10): out.append_word(0xC001)\n"
          "out.append_word(0xCB82)\n"
          "second = append_committed_resource_value_row(state, CommittedResourceRowInput(out, replace_word(first.numeric_carrier, 0xC051), 0xC6B4, state.scalar('cost_amount')))\n"
          "out = second.destination\n"
          "for word in (12, 0xC734, 0xD380): out.append_word(word)\n"
          "for counter in descending_inclusive(9): out.append_word(0xD381)\n"
          "out.append_word(0xDB80); out.put_word(0)\n"
          "return ResourceRowsResult(out, replace_word(second.numeric_carrier, u16(counter - 1)))\n"},
 'append_committed_resource_value_row': {'signature': "state: GameState, context: CommittedResourceRowInput",
  'returns': "ResourceRowsResult",
  'flow':
          "checked_state(state)\n"
          "if type(context) is not CommittedResourceRowInput: raise ValueError('complete committed resource row input required')\n"
          "context.validate(state)\n"
          "out = context.destination; tile = low16(context.tile_carrier); row = context.row\n"
          "pair = CommandColumns(out, 28)\n"
          "pair.append_pair(12, 12); pair.append_pair(u16(row - 128), row); pair.append_pair(0xC382, 0xC382)\n"
          "out.put_word(tile); tile = u16(tile + 1); out.set_word(28, tile); tile = u16(tile + 1); out.base = out.advance(2).base\n"
          "out.put_word(tile); tile = u16(tile + 1); out.set_word(28, tile); out.base = out.advance(2).base\n"
          "amount = replace_word(context.tile_carrier, low16(context.loaded_amount))\n"
          "formatted = _six_place_decimal_fields(DecimalMemory(state), amount, 1, 0, state.resource_digits.cursor())\n"
          "digits = state.resource_digits.cursor()\n"
          "# The first two cells are explicit blanks; only the remaining six cells\n"
          "# consume the freshly formatted WORDs (12EC6 branches to 12ED2).\n"
          "for latch in descending_inclusive(7):\n"
          "    retained_fill = u16(0xC001)\n"
          "    if latch <= 5:\n"
          "        value = digits.next_word()\n"
          "        retained_fill = u16(value + 0xC385) if value else u16(0xC001)\n"
          "    pair.append_pair(0xC001, retained_fill)\n"
          "pair.append_pair(0xCB82, 0xCB82); pair.next_row()\n"
          "return ResourceRowsResult(out, replace_word(formatted.remainder, u16(latch - 1)))\n"},
 '_six_place_decimal_fields': {'signature': 'memory: DecimalMemory, value: Long, digit_tile: Word, blank_tile: Word, '
              'destination: Cursor',
 'returns': 'DecimalTransactionFields',
 'flow': 'if type(memory) is not DecimalMemory:\n'
         "    raise ValueError('sealed decimal memory required')\n"
         'memory.check_cursor(destination)\n'
         'uint(value, 32)\n'
         'uint(digit_tile, 16)\n'
         'uint(blank_tile, 16)\n'
         'leading = u16(0)\n'
         'started = u16(0)\n'
         'while True:\n'
         '    previous = value\n'
         '    value = u32(value - 100000)\n'
         '    if previous < 100000:\n'
         '        break\n'
         '    leading = u16(leading + 1)\n'
         'value = u32(value + 100000)\n'
         'if leading == 0:\n'
         '    destination.append_word(blank_tile)\n'
         'else:\n'
         '    glyph = memory.glyph(leading)\n'
         '    destination.append_word(u16(digit_tile + glyph))\n'
         '    started = u16(started + 1)\n'
         'for divisor, continuation in ((10000, 75580), (1000, 75588), (100, 75596), (10, '
         '75604)):\n'
         '    memory.enter_call(continuation)\n'
         '    result = _decimal_value_place_fields(memory, value, divisor, digit_tile, blank_tile, '
         'started, destination)\n'
         '    memory.leave_call(continuation)\n'
         '    value, started = (result.remainder, result.started)\n'
         'glyph = u16(digit_tile + memory.glyph(low16(value)))\n'
         'destination.append_word(glyph)\n'
         'return DecimalTransactionFields(destination, value, divisor, started, glyph)'},
 '_decimal_value_place_fields': {'signature': 'memory: DecimalMemory, value: Long, divisor: Word, '
                                              'tile_base: Word, blank: Word, started: Word, out: Cursor',
                                 'returns': 'DecimalPlaceFields',
                                 'flow': 'if type(memory) is not DecimalMemory:\n'
                                         "    raise ValueError('sealed decimal memory required')\n"
                                         'memory.check_cursor(out)\n'
                                         'uint(value, 32)\n'
                                         'uint(divisor, 16)\n'
                                         'uint(tile_base, 16)\n'
                                         'uint(blank, 16)\n'
                                         'uint(started, 16)\n'
                                         'packed = divu_retained(value, divisor)\n'
                                         'quotient = low16(packed)\n'
                                         'glyph = u16(0)\n'
                                         'if started != 0 or quotient != 0:\n'
                                         '    glyph = u16(tile_base + memory.glyph(quotient))\n'
                                         '    out.append_word(glyph)\n'
                                         '    started = u16(1)\n'
                                         'else:\n'
                                         '    out.append_word(blank)\n'
                                         'return DecimalPlaceFields(packed >> 16, started, glyph)'}}

def _lower_prepare_budget_summary_panel(e, rules):
    e.label('player_pc_011cf2')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_011cf6')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_011cfa')
    e.ins('move.w', '#0x6,0x10(%a0)', 6)
    e.label('player_pc_011d00')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_011d04')
    e.ins('move.w', '#0xc3a2,0x10(%a0)', 6)
    e.label('player_pc_011d0a')
    e.ins('move.w', '#0xc322,(%a0)+', 4)
    e.label('player_pc_011d0e')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_011d12')
    e.ins('move.w', '#0x8000,0x10(%a0)', 6)
    e.label('player_pc_011d18')
    e.ins('move.w', '#0x8000,(%a0)+', 4)
    e.label('player_pc_011d1c')
    e.ins('dbra', '%d0,player_pc_011d12', 4)
    e.label('player_pc_011d20')
    e.ins('adda.w', '#0x10,%a0', 4)
    e.label('player_pc_011d24')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_011d28')
    e.ins('move.w', '#0xc422,(%a0)+', 4)
    e.label('player_pc_011d2c')
    e.ins('move.w', '#0xc380,(%a0)+', 4)
    e.label('player_pc_011d30')
    e.ins('move.w', '#0x3,%d0', 4)
    e.label('player_pc_011d34')
    e.ins('move.w', '#0xc381,(%a0)+', 4)
    e.label('player_pc_011d38')
    e.ins('dbra', '%d0,player_pc_011d34', 4)
    e.label('player_pc_011d3c')
    e.ins('move.w', '#0xcb80,(%a0)+', 4)
    e.label('player_pc_011d40')
    e.ins('move.w', '#0x6,0x10(%a0)', 6)
    e.label('player_pc_011d46')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_011d4a')
    e.ins('move.w', '#0xc522,0x10(%a0)', 6)
    e.label('player_pc_011d50')
    e.ins('move.w', '#0xc4a2,(%a0)+', 4)
    e.label('player_pc_011d54')
    e.ins('move.w', '#0xc382,0x10(%a0)', 6)
    e.label('player_pc_011d5a')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_011d5e')
    e.ins('move.w', '#0xc075,%d1', 4)
    e.label('player_pc_011d62')
    e.ins('move.w', '#0x3,%d2', 4)
    e.label('player_pc_011d66')
    e.ins('bsr.w', 'player_pc_011e2a', 4)
    e.label('player_pc_011d6a')
    e.ins('move.w', '#0xcb82,0x10(%a0)', 6)
    e.label('player_pc_011d70')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_011d74')
    e.ins('adda.w', '#0x10,%a0', 4)
    e.label('player_pc_011d78')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_011d7c')
    e.ins('move.w', '#0xc5a2,(%a0)+', 4)
    e.label('player_pc_011d80')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_011d84')
    e.ins('move.w', '#0x3,%d0', 4)
    e.label('player_pc_011d88')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_011d8c')
    e.ins('dbra', '%d0,player_pc_011d88', 4)
    e.label('player_pc_011d90')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_011d94')
    e.ins('move.w', '#0x6,0x10(%a0)', 6)
    e.label('player_pc_011d9a')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_011d9e')
    e.ins('move.w', '#0xc6a2,0x10(%a0)', 6)
    e.label('player_pc_011da4')
    e.ins('move.w', '#0xc622,(%a0)+', 4)
    e.label('player_pc_011da8')
    e.ins('move.w', '#0xc382,0x10(%a0)', 6)
    e.label('player_pc_011dae')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_011db2')
    e.ins('move.w', '#0xc07d,%d1', 4)
    e.label('player_pc_011db6')
    e.ins('move.w', '#0x3,%d2', 4)
    e.label('player_pc_011dba')
    e.ins('bsr.w', 'player_pc_011e2a', 4)
    e.label('player_pc_011dbe')
    e.ins('move.w', '#0xcb82,0x10(%a0)', 6)
    e.label('player_pc_011dc4')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_011dc8')
    e.ins('adda.w', '#0x10,%a0', 4)
    e.label('player_pc_011dcc')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_011dd0')
    e.ins('move.w', '#0xc722,(%a0)+', 4)
    e.label('player_pc_011dd4')
    e.ins('move.w', '#0xd380,(%a0)+', 4)
    e.label('player_pc_011dd8')
    e.ins('move.w', '#0x3,%d0', 4)
    e.label('player_pc_011ddc')
    e.ins('move.w', '#0xd381,(%a0)+', 4)
    e.label('player_pc_011de0')
    e.ins('dbra', '%d0,player_pc_011ddc', 4)
    e.label('player_pc_011de4')
    e.ins('move.w', '#0xdb80,(%a0)+', 4)
    e.label('player_pc_011de8')
    e.ins('move.w', '#0x6,0x20(%a0)', 6)
    e.label('player_pc_011dee')
    e.ins('move.w', '#0x6,0x10(%a0)', 6)
    e.label('player_pc_011df4')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_011df8')
    e.ins('move.w', '#0xc8a2,0x20(%a0)', 6)
    e.label('player_pc_011dfe')
    e.ins('move.w', '#0xc822,0x10(%a0)', 6)
    e.label('player_pc_011e04')
    e.ins('move.w', '#0xc7a2,(%a0)+', 4)
    e.label('player_pc_011e08')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_011e0c')
    e.ins('move.w', '#0x8000,0x20(%a0)', 6)
    e.label('player_pc_011e12')
    e.ins('move.w', '#0x8000,0x10(%a0)', 6)
    e.label('player_pc_011e18')
    e.ins('move.w', '#0x8000,(%a0)+', 4)
    e.label('player_pc_011e1c')
    e.ins('dbra', '%d0,player_pc_011e0c', 4)
    e.label('player_pc_011e20')
    e.ins('clr.w', '(%a0)', 2)
    e.label('player_pc_011e22')
    e.ins('addi.w', '#0xc0,0xf31a:w', 6)
    e.label('player_pc_011e28')
    e.ins('rts', '', 2)

def _lower_append_numbered_budget_columns(e, rules):
    e.label('player_pc_011e2a')
    e.ins('move.w', '%d1,(%a0)', 2)
    e.label('player_pc_011e2c')
    e.ins('addq.w', '#0x1,%d1', 2)
    e.label('player_pc_011e2e')
    e.ins('move.w', '%d1,0x10(%a0)', 4)
    e.label('player_pc_011e32')
    e.ins('addq.w', '#0x1,%d1', 2)
    e.label('player_pc_011e34')
    e.ins('addq.w', '#0x2,%a0', 2)
    e.label('player_pc_011e36')
    e.ins('dbra', '%d2,player_pc_011e2a', 4)
    e.label('player_pc_011e3a')
    e.ins('rts', '', 2)

def _lower_prepare_compact_budget_summary_panel(e, rules):
    e.label('player_pc_011e3c')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_011e40')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_011e44')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_011e48')
    e.ins('move.w', '#0xc422,(%a0)+', 4)
    e.label('player_pc_011e4c')
    e.ins('move.w', '#0xc380,(%a0)+', 4)
    e.label('player_pc_011e50')
    e.ins('move.w', '#0x3,%d0', 4)
    e.label('player_pc_011e54')
    e.ins('move.w', '#0xc381,(%a0)+', 4)
    e.label('player_pc_011e58')
    e.ins('dbra', '%d0,player_pc_011e54', 4)
    e.label('player_pc_011e5c')
    e.ins('move.w', '#0xcb80,(%a0)+', 4)
    e.label('player_pc_011e60')
    e.ins('move.w', '#0x6,0x10(%a0)', 6)
    e.label('player_pc_011e66')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_011e6a')
    e.ins('move.w', '#0xc522,0x10(%a0)', 6)
    e.label('player_pc_011e70')
    e.ins('move.w', '#0xc4a2,(%a0)+', 4)
    e.label('player_pc_011e74')
    e.ins('move.w', '#0xc382,0x10(%a0)', 6)
    e.label('player_pc_011e7a')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_011e7e')
    e.ins('move.w', '#0x3,%d2', 4)
    e.label('player_pc_011e82')
    e.ins('move.w', '#0xc085,%d1', 4)
    e.label('player_pc_011e86')
    e.ins('bsr.b', 'player_pc_011e2a', 2)
    e.label('player_pc_011e88')
    e.ins('move.w', '#0xcb82,0x10(%a0)', 6)
    e.label('player_pc_011e8e')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_011e92')
    e.ins('adda.w', '#0x10,%a0', 4)
    e.label('player_pc_011e96')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_011e9a')
    e.ins('move.w', '#0xc5a2,(%a0)+', 4)
    e.label('player_pc_011e9e')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_011ea2')
    e.ins('move.w', '#0x3,%d0', 4)
    e.label('player_pc_011ea6')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_011eaa')
    e.ins('dbra', '%d0,player_pc_011ea6', 4)
    e.label('player_pc_011eae')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_011eb2')
    e.ins('move.w', '#0x6,0x10(%a0)', 6)
    e.label('player_pc_011eb8')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_011ebc')
    e.ins('move.w', '#0xc6a2,0x10(%a0)', 6)
    e.label('player_pc_011ec2')
    e.ins('move.w', '#0xc622,(%a0)+', 4)
    e.label('player_pc_011ec6')
    e.ins('move.w', '#0xc382,0x10(%a0)', 6)
    e.label('player_pc_011ecc')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_011ed0')
    e.ins('move.w', '#0x1,%d2', 4)
    e.label('player_pc_011ed4')
    e.ins('move.w', '#0xc08d,%d1', 4)
    e.label('player_pc_011ed8')
    e.ins('bsr.w', 'player_pc_011e2a', 4)
    e.label('player_pc_011edc')
    e.ins('move.w', '#0x1,%d2', 4)
    e.label('player_pc_011ee0')
    e.ins('move.w', '#0xc001,%d1', 4)
    e.label('player_pc_011ee4')
    e.ins('bsr.w', 'player_pc_011e2a', 4)
    e.label('player_pc_011ee8')
    e.ins('move.w', '#0xcb82,0x10(%a0)', 6)
    e.label('player_pc_011eee')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_011ef2')
    e.ins('adda.w', '#0x10,%a0', 4)
    e.label('player_pc_011ef6')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_011efa')
    e.ins('move.w', '#0xc722,(%a0)+', 4)
    e.label('player_pc_011efe')
    e.ins('move.w', '#0xd380,(%a0)+', 4)
    e.label('player_pc_011f02')
    e.ins('move.w', '#0x3,%d0', 4)
    e.label('player_pc_011f06')
    e.ins('move.w', '#0xd381,(%a0)+', 4)
    e.label('player_pc_011f0a')
    e.ins('dbra', '%d0,player_pc_011f06', 4)
    e.label('player_pc_011f0e')
    e.ins('move.w', '#0xdb80,(%a0)+', 4)
    e.label('player_pc_011f12')
    e.ins('clr.w', '(%a0)', 2)
    e.label('player_pc_011f14')
    e.ins('addi.w', '#0x70,0xf31a:w', 6)
    e.label('player_pc_011f1a')
    e.ins('rts', '', 2)

def _lower_select_descriptor_portrait_parts(e, rules):
    e.label('player_pc_011f82')
    e.ins('movea.l', '0xff382c:l,%a0', 6)
    e.label('player_pc_011f88')
    e.ins('move.b', '0x1(%a0),%d0', 4)
    e.label('player_pc_011f8c')
    e.ins('move.b', '0x2(%a0),%d1', 4)
    e.label('player_pc_011f90')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_011f92')
    e.ins('lea.l', '0xd4d22:l,%a1', 6)
    e.label('player_pc_011f98')
    e.ins('cmp.b', '(%a1),%d0', 2)
    e.label('player_pc_011f9a')
    e.ins('bne.w', 'player_pc_011fa6', 4)
    e.label('player_pc_011f9e')
    e.ins('cmp.b', '0x1(%a1),%d1', 4)
    e.label('player_pc_011fa2')
    e.ins('beq.w', 'player_pc_011fac', 4)
    e.label('player_pc_011fa6')
    e.ins('addq.w', '#0x2,%a1', 2)
    e.label('player_pc_011fa8')
    e.ins('addq.w', '#0x1,%d2', 2)
    e.label('player_pc_011faa')
    e.ins('bra.b', 'player_pc_011f98', 2)
    e.label('player_pc_011fac')
    e.ins('move.w', '%d2,%d0', 2)
    e.label('player_pc_011fae')
    e.ins('lsl.w', '#0x1,%d0', 2)
    e.label('player_pc_011fb0')
    e.ins('add.w', '%d2,%d0', 2)
    e.label('player_pc_011fb2')
    e.ins('lea.l', '0xd4d2f:l,%a0', 6)
    e.label('player_pc_011fb8')
    e.ins('move.b', '(%a0, %d0.w),0xefb3:w', 6)
    e.label('player_pc_011fbe')
    e.ins('move.b', '0x1(%a0, %d0.w),0xefb5:w', 6)
    e.label('player_pc_011fc4')
    e.ins('move.b', '0x2(%a0, %d0.w),0xefb7:w', 6)
    e.label('player_pc_011fca')
    e.ins('btst.b', '#0x0,0xf3a4:w', 6)
    e.label('player_pc_011fd0')
    e.ins('bne.w', 'player_pc_011ff8', 4)
    e.label('player_pc_011fd4')
    e.ins('move.w', '0xefb2:w,%d0', 4)
    e.label('player_pc_011fd8')
    e.ins('bsr.w', 'player_pc_011ffa', 4)
    e.label('player_pc_011fdc')
    e.ins('move.w', '%d1,0xef64:w', 4)
    e.label('player_pc_011fe0')
    e.ins('move.w', '0xefb4:w,%d0', 4)
    e.label('player_pc_011fe4')
    e.ins('bsr.w', 'player_pc_011ffa', 4)
    e.label('player_pc_011fe8')
    e.ins('move.w', '%d1,0xef66:w', 4)
    e.label('player_pc_011fec')
    e.ins('move.w', '0xefb6:w,%d0', 4)
    e.label('player_pc_011ff0')
    e.ins('bsr.w', 'player_pc_011ffa', 4)
    e.label('player_pc_011ff4')
    e.ins('move.w', '%d1,0xef68:w', 4)
    e.label('player_pc_011ff8')
    e.ins('rts', '', 2)

def _lower_find_first_set_mask_bit(e, rules):
    e.label('player_pc_011ffa')
    e.ins('clr.w', '%d1', 2)
    e.label('player_pc_011ffc')
    e.ins('btst.l', '%d1,%d0', 2)
    e.label('player_pc_011ffe')
    e.ins('bne.w', 'player_pc_012006', 4)
    e.label('player_pc_012002')
    e.ins('addq.w', '#0x1,%d1', 2)
    e.label('player_pc_012004')
    e.ins('bra.b', 'player_pc_011ffc', 2)
    e.label('player_pc_012006')
    e.ins('rts', '', 2)

def _lower_prepare_command_amount_modal(e, rules):
    e.label('player_pc_012008')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_01200c')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_012010')
    e.ins('jsr', '18(%pc)', 4)
    e.label('player_pc_012014')
    e.ins('nop', '', 2)
    e.label('player_pc_012016')
    e.ins('jsr', '76(%pc)', 4)
    e.label('player_pc_01201a')
    e.ins('nop', '', 2)
    e.label('player_pc_01201c')
    e.ins('addi.w', '#0x78,0xf31a:w', 6)
    e.label('player_pc_012022')
    e.ins('rts', '', 2)

def _lower_append_amount_modal_frame(e, rules):
    e.label('player_pc_012024')
    e.ins('move.w', '#0xd,0x1e(%a0)', 6)
    e.label('player_pc_01202a')
    e.ins('move.w', '#0xd,(%a0)+', 4)
    e.label('player_pc_01202e')
    e.ins('move.w', '#0xc234,0x1e(%a0)', 6)
    e.label('player_pc_012034')
    e.ins('move.w', '#0xc0b4,(%a0)+', 4)
    e.label('player_pc_012038')
    e.ins('move.w', '#0xd380,0x1e(%a0)', 6)
    e.label('player_pc_01203e')
    e.ins('move.w', '#0xc380,(%a0)+', 4)
    e.label('player_pc_012042')
    e.ins('move.w', '#0xa,%d0', 4)
    e.label('player_pc_012046')
    e.ins('move.w', '#0xd381,0x1e(%a0)', 6)
    e.label('player_pc_01204c')
    e.ins('move.w', '#0xc381,(%a0)+', 4)
    e.label('player_pc_012050')
    e.ins('dbra', '%d0,player_pc_012046', 4)
    e.label('player_pc_012054')
    e.ins('move.w', '#0xdb80,0x1e(%a0)', 6)
    e.label('player_pc_01205a')
    e.ins('move.w', '#0xcb80,(%a0)+', 4)
    e.label('player_pc_01205e')
    e.ins('adda.w', '#0x1e,%a0', 4)
    e.label('player_pc_012062')
    e.ins('rts', '', 2)

def _lower_append_amount_modal_descriptor_limit(e, rules):
    e.label('player_pc_012064')
    e.ins('move.w', '#0xd,0x1e(%a0)', 6)
    e.label('player_pc_01206a')
    e.ins('move.w', '#0xd,(%a0)+', 4)
    e.label('player_pc_01206e')
    e.ins('move.w', '#0xc1b4,0x1e(%a0)', 6)
    e.label('player_pc_012074')
    e.ins('move.w', '#0xc134,(%a0)+', 4)
    e.label('player_pc_012078')
    e.ins('move.w', '#0xc382,0x1e(%a0)', 6)
    e.label('player_pc_01207e')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_012082')
    e.ins('move.w', '#0xc051,(%a0)', 4)
    e.label('player_pc_012086')
    e.ins('move.w', '#0xc052,0x1e(%a0)', 6)
    e.label('player_pc_01208c')
    e.ins('move.w', '#0xc053,0x2(%a0)', 6)
    e.label('player_pc_012092')
    e.ins('move.w', '#0xc054,0x20(%a0)', 6)
    e.label('player_pc_012098')
    e.ins('addq.w', '#0x4,%a0', 2)
    e.label('player_pc_01209a')
    e.ins('move.w', '#0x2,%d0', 4)
    e.label('player_pc_01209e')
    e.ins('move.w', '#0xc001,0x1e(%a0)', 6)
    e.label('player_pc_0120a4')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_0120a8')
    e.ins('dbra', '%d0,player_pc_01209e', 4)
    e.label('player_pc_0120ac')
    e.ins('movea.l', '0xff382c:l,%a1', 6)
    e.label('player_pc_0120b2')
    e.ins('move.b', '0x5(%a1),%d0', 4)
    e.label('player_pc_0120b6')
    e.ins('lsl.w', '#0x8,%d0', 2)
    e.label('player_pc_0120b8')
    e.ins('move.b', '0x6(%a1),%d0', 4)
    e.label('player_pc_0120bc')
    e.ins('lsl.l', '#0x8,%d0', 2)
    e.label('player_pc_0120be')
    e.ins('move.b', '0x7(%a1),%d0', 4)
    e.label('player_pc_0120c2')
    e.ins('lsl.l', '#0x8,%d0', 2)
    e.label('player_pc_0120c4')
    e.ins('move.b', '0x8(%a1),%d0', 4)
    e.label('player_pc_0120c8')
    e.ins('move.l', '%d0,0xf3f8:w', 4)
    e.label('player_pc_0120cc')
    e.ins('move.w', '#0xc386,%d1', 4)
    e.label('player_pc_0120d0')
    e.ins('move.w', '#0xc001,%d2', 4)
    e.label('player_pc_0120d4')
    e.ins('lea.l', '0xd300:w,%a6', 4)
    e.label('player_pc_0120d8')
    e.ins('jsr', 'player_pc_01270a:l', 6)
    e.label('player_pc_0120de')
    e.ins('lea.l', '0xd300:w,%a1', 4)
    e.label('player_pc_0120e2')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_0120e6')
    e.ins('move.w', '(%a1)+,0x1e(%a0)', 4)
    e.label('player_pc_0120ea')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_0120ee')
    e.ins('dbra', '%d0,player_pc_0120e6', 4)
    e.label('player_pc_0120f2')
    e.ins('move.w', '#0xcb82,0x1e(%a0)', 6)
    e.label('player_pc_0120f8')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_0120fc')
    e.ins('clr.w', '0x1e(%a0)', 4)
    e.label('player_pc_012100')
    e.ins('rts', '', 2)

def _lower_append_selected_command_row_label(e, rules):
    e.label('player_pc_01221c')
    e.ins('btst.b', '#0x3,0xf321:w', 6)
    e.label('player_pc_012222')
    e.ins('bne.b', 'player_pc_012246', 2)
    e.label('player_pc_012224')
    e.ins('lea.l', '34(%pc),%a0', 4)
    e.label('player_pc_012228')
    e.ins('nop', '', 2)
    e.label('player_pc_01222a')
    e.ins('move.w', '0xf3f0:w,%d0', 4)
    e.label('player_pc_01222e')
    e.ins('lsl.w', '#0x1,%d0', 2)
    e.label('player_pc_012230')
    e.ins('add.w', '0xf3f0:w,%d0', 4)
    e.label('player_pc_012234')
    e.ins('lsl.w', '#0x3,%d0', 2)
    e.label('player_pc_012236')
    e.ins('addi.w', '#0x38,%d0', 4)
    e.label('player_pc_01223a')
    e.ins('move.w', '#0xc8,%d1', 4)
    e.label('player_pc_01223e')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_012240')
    e.ins('jsr', 'player_pc_00ac08:l', 6)
    e.label('player_pc_012246')
    e.ins('rts', '', 2)

def _lower_clear_command_amount_page(e, rules):
    e.label('player_pc_012292')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_012296')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_01229a')
    e.ins('move.w', '#0xd,0x5a(%a0)', 6)
    e.label('player_pc_0122a0')
    e.ins('move.w', '#0xd,0x3c(%a0)', 6)
    e.label('player_pc_0122a6')
    e.ins('move.w', '#0xd,0x1e(%a0)', 6)
    e.label('player_pc_0122ac')
    e.ins('move.w', '#0xd,(%a0)+', 4)
    e.label('player_pc_0122b0')
    e.ins('move.w', '#0xc234,0x5a(%a0)', 6)
    e.label('player_pc_0122b6')
    e.ins('move.w', '#0xc1b4,0x3c(%a0)', 6)
    e.label('player_pc_0122bc')
    e.ins('move.w', '#0xc134,0x1e(%a0)', 6)
    e.label('player_pc_0122c2')
    e.ins('move.w', '#0xc0b4,(%a0)+', 4)
    e.label('player_pc_0122c6')
    e.ins('move.w', '#0xc,%d0', 4)
    e.label('player_pc_0122ca')
    e.ins('move.w', '#0x8000,0x5a(%a0)', 6)
    e.label('player_pc_0122d0')
    e.ins('move.w', '#0x8000,0x3c(%a0)', 6)
    e.label('player_pc_0122d6')
    e.ins('move.w', '#0x8000,0x1e(%a0)', 6)
    e.label('player_pc_0122dc')
    e.ins('move.w', '#0x8000,(%a0)+', 4)
    e.label('player_pc_0122e0')
    e.ins('dbra', '%d0,player_pc_0122ca', 4)
    e.label('player_pc_0122e4')
    e.ins('adda.w', '#0x5a,%a0', 4)
    e.label('player_pc_0122e8')
    e.ins('move.w', '#0x9,%d0', 4)
    e.label('player_pc_0122ec')
    e.ins('move.w', '#0xc3b2,%d1', 4)
    e.label('player_pc_0122f0')
    e.ins('move.w', '#0xe,(%a0)+', 4)
    e.label('player_pc_0122f4')
    e.ins('move.w', '%d1,(%a0)+', 2)
    e.label('player_pc_0122f6')
    e.ins('addi.w', '#0x80,%d1', 4)
    e.label('player_pc_0122fa')
    e.ins('move.w', '#0xd,%d2', 4)
    e.label('player_pc_0122fe')
    e.ins('move.w', '#0x8000,(%a0)+', 4)
    e.label('player_pc_012302')
    e.ins('dbra', '%d2,player_pc_0122fe', 4)
    e.label('player_pc_012306')
    e.ins('dbra', '%d0,player_pc_0122f0', 4)
    e.label('player_pc_01230a')
    e.ins('clr.w', '(%a0)', 2)
    e.label('player_pc_01230c')
    e.ins('addi.w', '#0x1b8,0xf31a:w', 6)
    e.label('player_pc_012312')
    e.ins('rts', '', 2)

def _lower_prepare_budget_amount_page(e, rules):
    e.label('player_pc_012314')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_012318')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_01231c')
    e.ins('move.w', '#0xb,(%a0)+', 4)
    e.label('player_pc_012320')
    e.ins('move.w', '#0xc5b2,(%a0)+', 4)
    e.label('player_pc_012324')
    e.ins('move.w', '#0xc380,(%a0)+', 4)
    e.label('player_pc_012328')
    e.ins('move.w', '#0x8,%d0', 4)
    e.label('player_pc_01232c')
    e.ins('move.w', '#0xc381,(%a0)+', 4)
    e.label('player_pc_012330')
    e.ins('dbra', '%d0,player_pc_01232c', 4)
    e.label('player_pc_012334')
    e.ins('move.w', '#0xcb80,(%a0)+', 4)
    e.label('player_pc_012338')
    e.ins('move.w', '#0xb,0x1a(%a0)', 6)
    e.label('player_pc_01233e')
    e.ins('move.w', '#0xb,(%a0)+', 4)
    e.label('player_pc_012342')
    e.ins('move.w', '#0xc6b2,0x1a(%a0)', 6)
    e.label('player_pc_012348')
    e.ins('move.w', '#0xc632,(%a0)+', 4)
    e.label('player_pc_01234c')
    e.ins('move.w', '#0xc382,0x1a(%a0)', 6)
    e.label('player_pc_012352')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_012356')
    e.ins('move.w', '#0x8,%d0', 4)
    e.label('player_pc_01235a')
    e.ins('move.w', '#0xc001,0x1a(%a0)', 6)
    e.label('player_pc_012360')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_012364')
    e.ins('dbra', '%d0,player_pc_01235a', 4)
    e.label('player_pc_012368')
    e.ins('move.w', '#0xcb82,0x1a(%a0)', 6)
    e.label('player_pc_01236e')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_012372')
    e.ins('adda.w', '#0x1a,%a0', 4)
    e.label('player_pc_012376')
    e.ins('move.w', '#0xb,0x1a(%a0)', 6)
    e.label('player_pc_01237c')
    e.ins('move.w', '#0xb,(%a0)+', 4)
    e.label('player_pc_012380')
    e.ins('move.w', '#0xc7b2,0x1a(%a0)', 6)
    e.label('player_pc_012386')
    e.ins('move.w', '#0xc732,(%a0)+', 4)
    e.label('player_pc_01238a')
    e.ins('move.w', '#0xc382,0x1a(%a0)', 6)
    e.label('player_pc_012390')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_012394')
    e.ins('move.w', '#0xc051,(%a0)', 4)
    e.label('player_pc_012398')
    e.ins('move.w', '#0xc052,0x1a(%a0)', 6)
    e.label('player_pc_01239e')
    e.ins('move.w', '#0xc053,0x2(%a0)', 6)
    e.label('player_pc_0123a4')
    e.ins('move.w', '#0xc054,0x1c(%a0)', 6)
    e.label('player_pc_0123aa')
    e.ins('addq.w', '#0x4,%a0', 2)
    e.label('player_pc_0123ac')
    e.ins('move.w', '#0xc001,0x1a(%a0)', 6)
    e.label('player_pc_0123b2')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_0123b6')
    e.ins('move.l', '0xf3f4:w,%d0', 4)
    e.label('player_pc_0123ba')
    e.ins('move.w', '#0xc386,%d1', 4)
    e.label('player_pc_0123be')
    e.ins('move.w', '#0xc001,%d2', 4)
    e.label('player_pc_0123c2')
    e.ins('lea.l', '0xd300:w,%a6', 4)
    e.label('player_pc_0123c6')
    e.ins('jsr', 'player_pc_01270a:l', 6)
    e.label('player_pc_0123cc')
    e.ins('lea.l', '0xd300:w,%a1', 4)
    e.label('player_pc_0123d0')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_0123d4')
    e.ins('move.w', '(%a1)+,0x1a(%a0)', 4)
    e.label('player_pc_0123d8')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_0123dc')
    e.ins('dbra', '%d0,player_pc_0123d4', 4)
    e.label('player_pc_0123e0')
    e.ins('move.w', '#0xcb82,0x1a(%a0)', 6)
    e.label('player_pc_0123e6')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_0123ea')
    e.ins('adda.w', '#0x1a,%a0', 4)
    e.label('player_pc_0123ee')
    e.ins('move.w', '#0xb,(%a0)+', 4)
    e.label('player_pc_0123f2')
    e.ins('move.w', '#0xc832,(%a0)+', 4)
    e.label('player_pc_0123f6')
    e.ins('move.w', '#0xd380,(%a0)+', 4)
    e.label('player_pc_0123fa')
    e.ins('move.w', '#0x8,%d0', 4)
    e.label('player_pc_0123fe')
    e.ins('move.w', '#0xd381,(%a0)+', 4)
    e.label('player_pc_012402')
    e.ins('dbra', '%d0,player_pc_0123fe', 4)
    e.label('player_pc_012406')
    e.ins('move.w', '#0xdb80,(%a0)+', 4)
    e.label('player_pc_01240a')
    e.ins('clr.w', '(%a0)', 2)
    e.label('player_pc_01240c')
    e.ins('addi.w', '#0x9c,0xf31a:w', 6)
    e.label('player_pc_012412')
    e.ins('bsr.w', 'player_pc_012008', 4)
    e.label('player_pc_012416')
    e.ins('rts', '', 2)

def _lower_step_budget_amount_controls(e, rules):
    e.label('player_pc_012418')
    e.ins('move.b', '0xf602:w,%d0', 4)
    e.label('player_pc_01241c')
    e.ins('andi.w', '#0xc,%d0', 4)
    e.label('player_pc_012420')
    e.ins('beq.b', 'player_pc_012470', 2)
    e.label('player_pc_012422')
    e.ins('subq.w', '#0x1,0xf608:w', 4)
    e.label('player_pc_012426')
    e.ins('bne.w', 'player_pc_0124fa', 4)
    e.label('player_pc_01242a')
    e.ins('move.w', '#0xc,0xf608:w', 6)
    e.label('player_pc_012430')
    e.ins('btst.l', '#0x3,%d0', 4)
    e.label('player_pc_012434')
    e.ins('bne.b', 'player_pc_01245a', 2)
    e.label('player_pc_012436')
    e.ins('move.w', '#0x5,%d1', 4)
    e.label('player_pc_01243a')
    e.ins('sub.w', '0xf39a:w,%d1', 4)
    e.label('player_pc_01243e')
    e.ins('lsl.w', '#0x2,%d1', 2)
    e.label('player_pc_012440')
    e.ins('lea.l', '190(%pc),%a0', 4)
    e.label('player_pc_012444')
    e.ins('nop', '', 2)
    e.label('player_pc_012446')
    e.ins('move.l', '(%a0, %d1.w),%d2', 4)
    e.label('player_pc_01244a')
    e.ins('cmp.l', '0xf3f8:w,%d2', 4)
    e.label('player_pc_01244e')
    e.ins('bhi.w', 'player_pc_0124fa', 4)
    e.label('player_pc_012452')
    e.ins('subq.w', '#0x1,0xf39a:w', 4)
    e.label('player_pc_012456')
    e.ins('bra.w', 'player_pc_0124f6', 4)
    e.label('player_pc_01245a')
    e.ins('move.w', '0xf39a:w,%d1', 4)
    e.label('player_pc_01245e')
    e.ins('addq.w', '#0x1,%d1', 2)
    e.label('player_pc_012460')
    e.ins('cmpi.w', '#0x5,%d1', 4)
    e.label('player_pc_012464')
    e.ins('bhi.w', 'player_pc_0124fa', 4)
    e.label('player_pc_012468')
    e.ins('move.w', '%d1,0xf39a:w', 4)
    e.label('player_pc_01246c')
    e.ins('bra.w', 'player_pc_0124f6', 4)
    e.label('player_pc_012470')
    e.ins('move.b', '0xf602:w,%d0', 4)
    e.label('player_pc_012474')
    e.ins('andi.w', '#0x3,%d0', 4)
    e.label('player_pc_012478')
    e.ins('beq.b', 'player_pc_0124f0', 2)
    e.label('player_pc_01247a')
    e.ins('subq.w', '#0x1,0xf608:w', 4)
    e.label('player_pc_01247e')
    e.ins('bne.w', 'player_pc_0124fa', 4)
    e.label('player_pc_012482')
    e.ins('move.w', '#0xc,0xf608:w', 6)
    e.label('player_pc_012488')
    e.ins('btst.l', '#0x1,%d0', 4)
    e.label('player_pc_01248c')
    e.ins('bne.b', 'player_pc_0124be', 2)
    e.label('player_pc_01248e')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_012492')
    e.ins('sub.w', '0xf39a:w,%d0', 4)
    e.label('player_pc_012496')
    e.ins('lsl.w', '#0x2,%d0', 2)
    e.label('player_pc_012498')
    e.ins('lea.l', '98(%pc),%a0', 4)
    e.label('player_pc_01249c')
    e.ins('move.l', '(%a0, %d0.w),%d1', 4)
    e.label('player_pc_0124a0')
    e.ins('add.l', '0xf3f4:w,%d1', 4)
    e.label('player_pc_0124a4')
    e.ins('cmp.l', '0xf3f8:w,%d1', 4)
    e.label('player_pc_0124a8')
    e.ins('bhi.w', 'player_pc_0124fa', 4)
    e.label('player_pc_0124ac')
    e.ins('move.l', '%d1,0xf3f4:w', 4)
    e.label('player_pc_0124b0')
    e.ins('lea.l', '98(%pc),%a0', 4)
    e.label('player_pc_0124b4')
    e.ins('move.l', '(%a0, %d0.w),%d1', 4)
    e.label('player_pc_0124b8')
    e.ins('add.l', '%d1,0xf3ba:w', 4)
    e.label('player_pc_0124bc')
    e.ins('bra.b', 'player_pc_0124f6', 2)
    e.label('player_pc_0124be')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_0124c2')
    e.ins('sub.w', '0xf39a:w,%d0', 4)
    e.label('player_pc_0124c6')
    e.ins('lsl.w', '#0x2,%d0', 2)
    e.label('player_pc_0124c8')
    e.ins('lea.l', '50(%pc),%a0', 4)
    e.label('player_pc_0124cc')
    e.ins('move.l', '(%a0, %d0.w),%d1', 4)
    e.label('player_pc_0124d0')
    e.ins('move.l', '0xf3f4:w,%d2', 4)
    e.label('player_pc_0124d4')
    e.ins('sub.l', '%d1,%d2', 2)
    e.label('player_pc_0124d6')
    e.ins('bcs.w', 'player_pc_0124fa', 4)
    e.label('player_pc_0124da')
    e.ins('move.l', '%d2,0xf3f4:w', 4)
    e.label('player_pc_0124de')
    e.ins('lea.l', '52(%pc),%a0', 4)
    e.label('player_pc_0124e2')
    e.ins('nop', '', 2)
    e.label('player_pc_0124e4')
    e.ins('move.l', '(%a0, %d0.w),%d1', 4)
    e.label('player_pc_0124e8')
    e.ins('sub.l', '%d1,0xf3ba:w', 4)
    e.label('player_pc_0124ec')
    e.ins('bra.w', 'player_pc_0124f6', 4)
    e.label('player_pc_0124f0')
    e.ins('move.w', '#0x1,0xf608:w', 6)
    e.label('player_pc_0124f6')
    e.ins('bsr.w', 'player_pc_01252c', 4)
    e.label('player_pc_0124fa')
    e.ins('rts', '', 2)

def _lower_append_budget_cost_and_amount_values(e, rules):
    e.label('player_pc_01252c')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_012530')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_012534')
    e.ins('move.l', '0xf3ba:w,%d0', 4)
    e.label('player_pc_012538')
    e.ins('move.w', '#0xc386,%d1', 4)
    e.label('player_pc_01253c')
    e.ins('move.w', '#0xc001,%d2', 4)
    e.label('player_pc_012540')
    e.ins('lea.l', '0xef00:w,%a6', 4)
    e.label('player_pc_012544')
    e.ins('jsr', 'player_pc_01270a:l', 6)
    e.label('player_pc_01254a')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_01254e')
    e.ins('move.w', '#0xc6ba,(%a0)+', 4)
    e.label('player_pc_012552')
    e.ins('lea.l', '0xef00:w,%a1', 4)
    e.label('player_pc_012556')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_01255a')
    e.ins('clr.w', '%d1', 2)
    e.label('player_pc_01255c')
    e.ins('move.w', '(%a1)+,%d2', 2)
    e.label('player_pc_01255e')
    e.ins('cmpi.w', '#0xc001,%d2', 4)
    e.label('player_pc_012562')
    e.ins('bne.b', 'player_pc_01256e', 2)
    e.label('player_pc_012564')
    e.ins('cmp.w', '0xf39a:w,%d1', 4)
    e.label('player_pc_012568')
    e.ins('bcs.b', 'player_pc_01256e', 2)
    e.label('player_pc_01256a')
    e.ins('move.w', '#0xc386,%d2', 4)
    e.label('player_pc_01256e')
    e.ins('move.w', '%d2,(%a0)+', 2)
    e.label('player_pc_012570')
    e.ins('addq.w', '#0x1,%d1', 2)
    e.label('player_pc_012572')
    e.ins('dbra', '%d0,player_pc_01255c', 4)
    e.label('player_pc_012576')
    e.ins('move.l', '0xf3f4:w,%d0', 4)
    e.label('player_pc_01257a')
    e.ins('move.w', '#0xc386,%d1', 4)
    e.label('player_pc_01257e')
    e.ins('move.w', '#0xc001,%d2', 4)
    e.label('player_pc_012582')
    e.ins('lea.l', '0xef00:w,%a6', 4)
    e.label('player_pc_012586')
    e.ins('jsr', 'player_pc_01270a:l', 6)
    e.label('player_pc_01258c')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_012590')
    e.ins('move.w', '#0xc7ba,(%a0)+', 4)
    e.label('player_pc_012594')
    e.ins('lea.l', '0xef00:w,%a1', 4)
    e.label('player_pc_012598')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_01259c')
    e.ins('move.w', '(%a1)+,(%a0)+', 2)
    e.label('player_pc_01259e')
    e.ins('dbra', '%d0,player_pc_01259c', 4)
    e.label('player_pc_0125a2')
    e.ins('clr.w', '(%a0)', 2)
    e.label('player_pc_0125a4')
    e.ins('addi.w', '#0x20,0xf31a:w', 6)
    e.label('player_pc_0125aa')
    e.ins('rts', '', 2)

def _lower_append_budget_place_highlight(e, rules):
    e.label('player_pc_0125ac')
    e.ins('btst.b', '#0x4,0xf321:w', 6)
    e.label('player_pc_0125b2')
    e.ins('bne.b', 'player_pc_0125ce', 2)
    e.label('player_pc_0125b4')
    e.ins('lea.l', '26(%pc),%a0', 4)
    e.label('player_pc_0125b8')
    e.ins('move.w', '#0x68,%d0', 4)
    e.label('player_pc_0125bc')
    e.ins('move.w', '0xf39a:w,%d1', 4)
    e.label('player_pc_0125c0')
    e.ins('lsl.w', '#0x3,%d1', 2)
    e.label('player_pc_0125c2')
    e.ins('addi.w', '#0xe8,%d1', 4)
    e.label('player_pc_0125c6')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_0125c8')
    e.ins('jsr', 'player_pc_00ac08:l', 6)
    e.label('player_pc_0125ce')
    e.ins('rts', '', 2)

def _lower_append_budget_header_row(e, rules):
    e.label('player_pc_012602')
    e.ins('move.w', '#0x8,(%a0)+', 4)
    e.label('player_pc_012606')
    e.ins('move.w', '#0xc422,(%a0)+', 4)
    e.label('player_pc_01260a')
    e.ins('move.w', '#0xc380,(%a0)+', 4)
    e.label('player_pc_01260e')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_012612')
    e.ins('move.w', '#0xc381,(%a0)+', 4)
    e.label('player_pc_012616')
    e.ins('dbra', '%d0,player_pc_012612', 4)
    e.label('player_pc_01261a')
    e.ins('move.w', '#0xcb80,(%a0)+', 4)
    e.label('player_pc_01261e')
    e.ins('rts', '', 2)

def _lower_append_budget_first_detail_rows(e, rules):
    e.label('player_pc_012620')
    e.ins('move.w', '#0x8,0x14(%a0)', 6)
    e.label('player_pc_012626')
    e.ins('move.w', '#0x8,(%a0)+', 4)
    e.label('player_pc_01262a')
    e.ins('move.w', '#0xc522,0x14(%a0)', 6)
    e.label('player_pc_012630')
    e.ins('move.w', '#0xc4a2,(%a0)+', 4)
    e.label('player_pc_012634')
    e.ins('move.w', '#0xc382,0x14(%a0)', 6)
    e.label('player_pc_01263a')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_01263e')
    e.ins('move.w', '#0xc091,%d0', 4)
    e.label('player_pc_012642')
    e.ins('bsr.w', 'player_pc_0126f0', 4)
    e.label('player_pc_012646')
    e.ins('addq.w', '#0x4,%d0', 2)
    e.label('player_pc_012648')
    e.ins('bsr.w', 'player_pc_0126f0', 4)
    e.label('player_pc_01264c')
    e.ins('move.w', '#0xc001,0x14(%a0)', 6)
    e.label('player_pc_012652')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_012656')
    e.ins('move.w', '#0xc001,0x14(%a0)', 6)
    e.label('player_pc_01265c')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_012660')
    e.ins('move.w', '#0xcb82,0x14(%a0)', 6)
    e.label('player_pc_012666')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_01266a')
    e.ins('adda.w', '#0x14,%a0', 4)
    e.label('player_pc_01266e')
    e.ins('move.w', '#0x8,(%a0)+', 4)
    e.label('player_pc_012672')
    e.ins('move.w', '#0xc5a2,(%a0)+', 4)
    e.label('player_pc_012676')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_01267a')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_01267e')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_012682')
    e.ins('dbra', '%d0,player_pc_01267e', 4)
    e.label('player_pc_012686')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_01268a')
    e.ins('rts', '', 2)

def _lower_append_budget_second_detail_row(e, rules):
    e.label('player_pc_01268c')
    e.ins('move.w', '#0x8,0x14(%a0)', 6)
    e.label('player_pc_012692')
    e.ins('move.w', '#0x8,(%a0)+', 4)
    e.label('player_pc_012696')
    e.ins('move.w', '#0xc6a2,0x14(%a0)', 6)
    e.label('player_pc_01269c')
    e.ins('move.w', '#0xc622,(%a0)+', 4)
    e.label('player_pc_0126a0')
    e.ins('move.w', '#0xc382,0x14(%a0)', 6)
    e.label('player_pc_0126a6')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_0126aa')
    e.ins('move.w', '#0xc091,%d0', 4)
    e.label('player_pc_0126ae')
    e.ins('bsr.w', 'player_pc_0126f0', 4)
    e.label('player_pc_0126b2')
    e.ins('move.w', '#0xc099,%d0', 4)
    e.label('player_pc_0126b6')
    e.ins('bsr.w', 'player_pc_0126f0', 4)
    e.label('player_pc_0126ba')
    e.ins('move.w', '#0xc091,%d0', 4)
    e.label('player_pc_0126be')
    e.ins('bsr.w', 'player_pc_0126f0', 4)
    e.label('player_pc_0126c2')
    e.ins('move.w', '#0xcb82,0x14(%a0)', 6)
    e.label('player_pc_0126c8')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_0126cc')
    e.ins('adda.w', '#0x14,%a0', 4)
    e.label('player_pc_0126d0')
    e.ins('rts', '', 2)

def _lower_append_budget_footer_row(e, rules):
    e.label('player_pc_0126d2')
    e.ins('move.w', '#0x8,(%a0)+', 4)
    e.label('player_pc_0126d6')
    e.ins('move.w', '#0xc722,(%a0)+', 4)
    e.label('player_pc_0126da')
    e.ins('move.w', '#0xd380,(%a0)+', 4)
    e.label('player_pc_0126de')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_0126e2')
    e.ins('move.w', '#0xd381,(%a0)+', 4)
    e.label('player_pc_0126e6')
    e.ins('dbra', '%d0,player_pc_0126e2', 4)
    e.label('player_pc_0126ea')
    e.ins('move.w', '#0xdb80,(%a0)+', 4)
    e.label('player_pc_0126ee')
    e.ins('rts', '', 2)

def _lower_append_four_budget_numbered_tiles(e, rules):
    e.label('player_pc_0126f0')
    e.ins('move.w', '%d0,%d1', 2)
    e.label('player_pc_0126f2')
    e.ins('move.w', '%d1,(%a0)', 2)
    e.label('player_pc_0126f4')
    e.ins('addq.w', '#0x1,%d1', 2)
    e.label('player_pc_0126f6')
    e.ins('move.w', '%d1,0x14(%a0)', 4)
    e.label('player_pc_0126fa')
    e.ins('addq.w', '#0x1,%d1', 2)
    e.label('player_pc_0126fc')
    e.ins('addq.w', '#0x2,%a0', 2)
    e.label('player_pc_0126fe')
    e.ins('move.w', '%d1,(%a0)', 2)
    e.label('player_pc_012700')
    e.ins('addq.w', '#0x1,%d1', 2)
    e.label('player_pc_012702')
    e.ins('move.w', '%d1,0x14(%a0)', 4)
    e.label('player_pc_012706')
    e.ins('addq.w', '#0x2,%a0', 2)
    e.label('player_pc_012708')
    e.ins('rts', '', 2)

def _lower_append_six_place_decimal_value(e, rules):
    e.label('player_pc_01270a')
    e.ins('clr.w', '%d3', 2)
    e.label('player_pc_01270c')
    e.ins('clr.w', '%d4', 2)
    e.label('player_pc_01270e')
    e.ins('subi.l', '#0x186a0,%d0', 6)
    e.label('player_pc_012714')
    e.ins('bcs.b', 'player_pc_01271a', 2)
    e.label('player_pc_012716')
    e.ins('addq.w', '#0x1,%d3', 2)
    e.label('player_pc_012718')
    e.ins('bra.b', 'player_pc_01270e', 2)
    e.label('player_pc_01271a')
    e.ins('addi.l', '#0x186a0,%d0', 6)
    e.label('player_pc_012720')
    e.ins('tst.w', '%d3', 2)
    e.label('player_pc_012722')
    e.ins('bne.b', 'player_pc_012728', 2)
    e.label('player_pc_012724')
    e.ins('move.w', '%d2,(%a6)+', 2)
    e.label('player_pc_012726')
    e.ins('bra.b', 'player_pc_012734', 2)
    e.label('player_pc_012728')
    e.ins('clr.w', '%d5', 2)
    e.label('player_pc_01272a')
    e.ins('move.b', '86(%pc, %d3.w),%d5', 4)
    e.label('player_pc_01272e')
    e.ins('add.w', '%d1,%d5', 2)
    e.label('player_pc_012730')
    e.ins('move.w', '%d5,(%a6)+', 2)
    e.label('player_pc_012732')
    e.ins('addq.w', '#0x1,%d4', 2)
    e.label('player_pc_012734')
    e.ins('move.w', '#0x2710,%d3', 4)
    e.label('player_pc_012738')
    e.ins('bsr.w', 'player_pc_012760', 4)
    e.label('player_pc_01273c')
    e.ins('move.w', '#0x3e8,%d3', 4)
    e.label('player_pc_012740')
    e.ins('bsr.w', 'player_pc_012760', 4)
    e.label('player_pc_012744')
    e.ins('move.w', '#0x64,%d3', 4)
    e.label('player_pc_012748')
    e.ins('bsr.w', 'player_pc_012760', 4)
    e.label('player_pc_01274c')
    e.ins('move.w', '#0xa,%d3', 4)
    e.label('player_pc_012750')
    e.ins('bsr.w', 'player_pc_012760', 4)
    e.label('player_pc_012754')
    e.ins('clr.w', '%d5', 2)
    e.label('player_pc_012756')
    e.ins('move.b', '42(%pc, %d0.w),%d5', 4)
    e.label('player_pc_01275a')
    e.ins('add.w', '%d1,%d5', 2)
    e.label('player_pc_01275c')
    e.ins('move.w', '%d5,(%a6)+', 2)
    e.label('player_pc_01275e')
    e.ins('rts', '', 2)

def _lower_append_decimal_value_place(e, rules):
    e.label('player_pc_012760')
    e.ins('clr.w', '%d5', 2)
    e.label('player_pc_012762')
    e.ins('divu.w', '%d3,%d0', 2)
    e.label('player_pc_012764')
    e.ins('tst.w', '%d4', 2)
    e.label('player_pc_012766')
    e.ins('bne.b', 'player_pc_01276c', 2)
    e.label('player_pc_012768')
    e.ins('tst.w', '%d0', 2)
    e.label('player_pc_01276a')
    e.ins('beq.b', 'player_pc_01277a', 2)
    e.label('player_pc_01276c')
    e.ins('move.b', '20(%pc, %d0.w),%d5', 4)
    e.label('player_pc_012770')
    e.ins('add.w', '%d1,%d5', 2)
    e.label('player_pc_012772')
    e.ins('move.w', '%d5,(%a6)+', 2)
    e.label('player_pc_012774')
    e.ins('move.w', '#0x1,%d4', 4)
    e.label('player_pc_012778')
    e.ins('bra.b', 'player_pc_01277c', 2)
    e.label('player_pc_01277a')
    e.ins('move.w', '%d2,(%a6)+', 2)
    e.label('player_pc_01277c')
    e.ins('clr.w', '%d0', 2)
    e.label('player_pc_01277e')
    e.ins('swap', '%d0', 2)
    e.label('player_pc_012780')
    e.ins('rts', '', 2)

def _lower_prepare_command_amount_limit(e, rules):
    e.label('player_pc_01278c')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_012790')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_012794')
    e.ins('move.w', '#0x9,0x2c(%a0)', 6)
    e.label('player_pc_01279a')
    e.ins('move.w', '#0x9,0x16(%a0)', 6)
    e.label('player_pc_0127a0')
    e.ins('move.w', '#0x9,(%a0)+', 4)
    e.label('player_pc_0127a4')
    e.ins('move.w', '#0xc4bc,0x2c(%a0)', 6)
    e.label('player_pc_0127aa')
    e.ins('move.w', '#0xc43c,0x16(%a0)', 6)
    e.label('player_pc_0127b0')
    e.ins('move.w', '#0xc3bc,(%a0)+', 4)
    e.label('player_pc_0127b4')
    e.ins('move.w', '#0xd380,0x2c(%a0)', 6)
    e.label('player_pc_0127ba')
    e.ins('move.w', '#0xc382,0x16(%a0)', 6)
    e.label('player_pc_0127c0')
    e.ins('move.w', '#0xc380,(%a0)+', 4)
    e.label('player_pc_0127c4')
    e.ins('move.w', '#0x6,%d0', 4)
    e.label('player_pc_0127c8')
    e.ins('move.w', '#0xd381,0x2c(%a0)', 6)
    e.label('player_pc_0127ce')
    e.ins('move.w', '#0xc001,0x16(%a0)', 6)
    e.label('player_pc_0127d4')
    e.ins('move.w', '#0xc381,(%a0)+', 4)
    e.label('player_pc_0127d8')
    e.ins('dbra', '%d0,player_pc_0127c8', 4)
    e.label('player_pc_0127dc')
    e.ins('move.w', '#0xc386,0x14(%a0)', 6)
    e.label('player_pc_0127e2')
    e.ins('move.w', '#0xdb80,0x2c(%a0)', 6)
    e.label('player_pc_0127e8')
    e.ins('move.w', '#0xcb82,0x16(%a0)', 6)
    e.label('player_pc_0127ee')
    e.ins('move.w', '#0xcb80,(%a0)+', 4)
    e.label('player_pc_0127f2')
    e.ins('clr.w', '0x2c(%a0)', 4)
    e.label('player_pc_0127f6')
    e.ins('addi.w', '#0x42,0xf31a:w', 6)
    e.label('player_pc_0127fc')
    e.ins('move.w', '0xf364:w,%d0', 4)
    e.label('player_pc_012800')
    e.ins('lsl.w', '#0x2,%d0', 2)
    e.label('player_pc_012802')
    e.ins('lea.l', '0xdffc:w,%a1', 4)
    e.label('player_pc_012806')
    e.ins('move.l', '(%a1, %d0.w),%d0', 4)
    e.label('player_pc_01280a')
    e.ins('move.l', '%d0,0xf3f8:w', 4)
    e.label('player_pc_01280e')
    e.ins('lea.l', '48(%pc),%a0', 4)
    e.label('player_pc_012812')
    e.ins('nop', '', 2)
    e.label('player_pc_012814')
    e.ins('bsr.w', 'player_pc_012878', 4)
    e.label('player_pc_012818')
    e.ins('move.l', '0xf3f8:w,%d0', 4)
    e.label('player_pc_01281c')
    e.ins('move.w', '#0xc386,%d1', 4)
    e.label('player_pc_012820')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_012822')
    e.ins('lea.l', '0xef00:w,%a6', 4)
    e.label('player_pc_012826')
    e.ins('jsr', 'player_pc_01270a:l', 6)
    e.label('player_pc_01282c')
    e.ins('move.w', '#0x1,0xf608:w', 6)
    e.label('player_pc_012832')
    e.ins('ori.w', '#0x8040,0xf3a4:w', 6)
    e.label('player_pc_012838')
    e.ins('andi.w', '#0xf9ff,0xf3a4:w', 6)
    e.label('player_pc_01283e')
    e.ins('rts', '', 2)

def _lower_limit_live_command_amount_by_price_record(e, rules):
    e.label('player_pc_012878')
    e.ins('move.w', '0xf38c:w,%d7', 4)
    e.label('player_pc_01287c')
    e.ins('cmpi.w', '#0x93,%d7', 4)
    e.label('player_pc_012880')
    e.ins('beq.w', 'player_pc_0128aa', 4)
    e.label('player_pc_012884')
    e.ins('cmp.w', '(%a0),%d7', 2)
    e.label('player_pc_012886')
    e.ins('beq.b', 'player_pc_01288c', 2)
    e.label('player_pc_012888')
    e.ins('addq.w', '#0x8,%a0', 2)
    e.label('player_pc_01288a')
    e.ins('bra.b', 'player_pc_012884', 2)
    e.label('player_pc_01288c')
    e.ins('move.l', '0x2(%a0),%d7', 4)
    e.label('player_pc_012890')
    e.ins('cmp.l', '0xf3f8:w,%d7', 4)
    e.label('player_pc_012894')
    e.ins('bcc.b', 'player_pc_01289a', 2)
    e.label('player_pc_012896')
    e.ins('move.l', '%d7,0xf3f8:w', 4)
    e.label('player_pc_01289a')
    e.ins('move.w', '0x6(%a0),%d7', 4)
    e.label('player_pc_01289e')
    e.ins('move.w', '%d7,0xf39a:w', 4)
    e.label('player_pc_0128a2')
    e.ins('move.w', '%d7,0xf3fc:w', 4)
    e.label('player_pc_0128a6')
    e.ins('bra.w', 'player_pc_0128e0', 4)
    e.label('player_pc_0128aa')
    e.ins('move.l', '%d6,-(%a7)', 2)
    e.label('player_pc_0128ac')
    e.ins('lea.l', '0xf500:w,%a1', 4)
    e.label('player_pc_0128b0')
    e.ins('clr.w', '%d7', 2)
    e.label('player_pc_0128b2')
    e.ins('move.w', '(%a1)+,%d6', 2)
    e.label('player_pc_0128b4')
    e.ins('bmi.w', 'player_pc_0128c2', 4)
    e.label('player_pc_0128b8')
    e.ins('btst.l', '#0xe,%d6', 4)
    e.label('player_pc_0128bc')
    e.ins('beq.b', 'player_pc_0128b2', 2)
    e.label('player_pc_0128be')
    e.ins('addq.w', '#0x1,%d7', 2)
    e.label('player_pc_0128c0')
    e.ins('bra.b', 'player_pc_0128b2', 2)
    e.label('player_pc_0128c2')
    e.ins('mulu.w', '#0x61a8,%d7', 4)
    e.label('player_pc_0128c6')
    e.ins('cmp.l', '0xf3f8:w,%d7', 4)
    e.label('player_pc_0128ca')
    e.ins('bcc.w', 'player_pc_0128d2', 4)
    e.label('player_pc_0128ce')
    e.ins('move.l', '%d7,0xf3f8:w', 4)
    e.label('player_pc_0128d2')
    e.ins('move.w', '#0x5,0xf39a:w', 6)
    e.label('player_pc_0128d8')
    e.ins('move.w', '#0x5,0xf3fc:w', 6)
    e.label('player_pc_0128de')
    e.ins('move.l', '(%a7)+,%d6', 2)
    e.label('player_pc_0128e0')
    e.ins('rts', '', 2)

def _lower_update_player_command_amount(e, rules):
    e.label('player_pc_0128e2')
    e.ins('bsr.w', 'player_pc_01292c', 4)
    e.label('player_pc_0128e6')
    e.ins('bsr.w', 'player_pc_012980', 4)
    e.label('player_pc_0128ea')
    e.ins('bsr.w', 'player_pc_012a4e', 4)
    e.label('player_pc_0128ee')
    e.ins('btst.b', '#0x5,0xf603:w', 6)
    e.label('player_pc_0128f4')
    e.ins('beq.b', 'player_pc_012910', 2)
    e.label('player_pc_0128f6')
    e.ins('move.l', '0xf3f4:w,0xf39e:w', 6)
    e.label('player_pc_0128fc')
    e.ins('tst.l', '0xf3f4:w', 4)
    e.label('player_pc_012900')
    e.ins('beq.b', 'player_pc_01292a', 2)
    e.label('player_pc_012902')
    e.ins('move.w', '#0x208,0xf612:w', 6)
    e.label('player_pc_012908')
    e.ins('move.w', '#0x4,0xf362:w', 6)
    e.label('player_pc_01290e')
    e.ins('bra.b', 'player_pc_01292a', 2)
    e.label('player_pc_012910')
    e.ins('btst.b', '#0x4,0xf603:w', 6)
    e.label('player_pc_012916')
    e.ins('beq.b', 'player_pc_01292a', 2)
    e.label('player_pc_012918')
    e.ins('move.w', '#0x208,0xf612:w', 6)
    e.label('player_pc_01291e')
    e.ins('move.w', '#0x2,0xf362:w', 6)
    e.label('player_pc_012924')
    e.ins('move.w', '#0x12,0xf36a:w', 6)
    e.label('player_pc_01292a')
    e.ins('rts', '', 2)

def _lower_append_selected_command_amount(e, rules):
    e.label('player_pc_01292c')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_012930')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_012934')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_012938')
    e.ins('move.w', '#0xc440,(%a0)+', 4)
    e.label('player_pc_01293c')
    e.ins('move.l', '0xf3f4:w,%d0', 4)
    e.label('player_pc_012940')
    e.ins('move.w', '#0xc386,%d1', 4)
    e.label('player_pc_012944')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_012946')
    e.ins('lea.l', '0xef0c:w,%a6', 4)
    e.label('player_pc_01294a')
    e.ins('jsr', 'player_pc_01270a:l', 6)
    e.label('player_pc_012950')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_012954')
    e.ins('lea.l', '0xef0c:w,%a1', 4)
    e.label('player_pc_012958')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_01295a')
    e.ins('move.w', '(%a1)+,%d1', 2)
    e.label('player_pc_01295c')
    e.ins('bne.b', 'player_pc_01296e', 2)
    e.label('player_pc_01295e')
    e.ins('cmp.w', '0xf39a:w,%d2', 4)
    e.label('player_pc_012962')
    e.ins('bcs.b', 'player_pc_01296a', 2)
    e.label('player_pc_012964')
    e.ins('move.w', '#0xc386,%d1', 4)
    e.label('player_pc_012968')
    e.ins('bra.b', 'player_pc_01296e', 2)
    e.label('player_pc_01296a')
    e.ins('move.w', '#0xc001,%d1', 4)
    e.label('player_pc_01296e')
    e.ins('move.w', '%d1,(%a0)+', 2)
    e.label('player_pc_012970')
    e.ins('addq.w', '#0x1,%d2', 2)
    e.label('player_pc_012972')
    e.ins('dbra', '%d0,player_pc_01295a', 4)
    e.label('player_pc_012976')
    e.ins('clr.w', '(%a0)', 2)
    e.label('player_pc_012978')
    e.ins('addi.w', '#0x10,0xf31a:w', 6)
    e.label('player_pc_01297e')
    e.ins('rts', '', 2)

def _lower_step_live_command_amount_controls(e, rules):
    e.label('player_pc_012980')
    e.ins('move.b', '0xf602:w,%d0', 4)
    e.label('player_pc_012984')
    e.ins('andi.w', '#0xc,%d0', 4)
    e.label('player_pc_012988')
    e.ins('beq.w', 'player_pc_0129ac', 4)
    e.label('player_pc_01298c')
    e.ins('subq.w', '#0x1,0xf608:w', 4)
    e.label('player_pc_012990')
    e.ins('bne.w', 'player_pc_0129dc', 4)
    e.label('player_pc_012994')
    e.ins('move.w', '#0xc,0xf608:w', 6)
    e.label('player_pc_01299a')
    e.ins('btst.l', '#0x3,%d0', 4)
    e.label('player_pc_01299e')
    e.ins('bne.b', 'player_pc_0129a6', 2)
    e.label('player_pc_0129a0')
    e.ins('bsr.w', 'player_pc_0129de', 4)
    e.label('player_pc_0129a4')
    e.ins('bra.b', 'player_pc_0129dc', 2)
    e.label('player_pc_0129a6')
    e.ins('bsr.w', 'player_pc_0129f8', 4)
    e.label('player_pc_0129aa')
    e.ins('bra.b', 'player_pc_0129dc', 2)
    e.label('player_pc_0129ac')
    e.ins('move.b', '0xf602:w,%d0', 4)
    e.label('player_pc_0129b0')
    e.ins('andi.w', '#0x3,%d0', 4)
    e.label('player_pc_0129b4')
    e.ins('beq.b', 'player_pc_0129d6', 2)
    e.label('player_pc_0129b6')
    e.ins('subq.w', '#0x1,0xf608:w', 4)
    e.label('player_pc_0129ba')
    e.ins('bne.w', 'player_pc_0129dc', 4)
    e.label('player_pc_0129be')
    e.ins('move.w', '#0xc,0xf608:w', 6)
    e.label('player_pc_0129c4')
    e.ins('btst.l', '#0x1,%d0', 4)
    e.label('player_pc_0129c8')
    e.ins('bne.b', 'player_pc_0129d0', 2)
    e.label('player_pc_0129ca')
    e.ins('bsr.w', 'player_pc_012a0c', 4)
    e.label('player_pc_0129ce')
    e.ins('bra.b', 'player_pc_0129dc', 2)
    e.label('player_pc_0129d0')
    e.ins('bsr.w', 'player_pc_012a2e', 4)
    e.label('player_pc_0129d4')
    e.ins('bra.b', 'player_pc_0129dc', 2)
    e.label('player_pc_0129d6')
    e.ins('move.w', '#0x1,0xf608:w', 6)
    e.label('player_pc_0129dc')
    e.ins('rts', '', 2)

def _lower_select_previous_amount_place(e, rules):
    e.label('player_pc_0129de')
    e.ins('move.w', '0xf39a:w,%d0', 4)
    e.label('player_pc_0129e2')
    e.ins('subq.w', '#0x1,%d0', 2)
    e.label('player_pc_0129e4')
    e.ins('bcs.b', 'player_pc_0129f6', 2)
    e.label('player_pc_0129e6')
    e.ins('lsl.w', '#0x1,%d0', 2)
    e.label('player_pc_0129e8')
    e.ins('lea.l', '0xef00:w,%a0', 4)
    e.label('player_pc_0129ec')
    e.ins('tst.w', '(%a0, %d0.w)', 4)
    e.label('player_pc_0129f0')
    e.ins('beq.b', 'player_pc_0129f6', 2)
    e.label('player_pc_0129f2')
    e.ins('subq.w', '#0x1,0xf39a:w', 4)
    e.label('player_pc_0129f6')
    e.ins('rts', '', 2)

def _lower_select_next_amount_place(e, rules):
    e.label('player_pc_0129f8')
    e.ins('move.w', '0xf39a:w,%d0', 4)
    e.label('player_pc_0129fc')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_0129fe')
    e.ins('cmp.w', '0xf3fc:w,%d0', 4)
    e.label('player_pc_012a02')
    e.ins('bhi.w', 'player_pc_012a0a', 4)
    e.label('player_pc_012a06')
    e.ins('addq.w', '#0x1,0xf39a:w', 4)
    e.label('player_pc_012a0a')
    e.ins('rts', '', 2)

def _lower_decrement_live_command_amount_small(e, rules):
    e.label('player_pc_012a2e')
    e.ins('move.w', '0xf39a:w,%d1', 4)
    e.label('player_pc_012a32')
    e.ins('lsl.w', '#0x2,%d1', 2)
    e.label('player_pc_012a34')
    e.ins('lea.l', '2582(%pc),%a0', 4)
    e.label('player_pc_012a38')
    e.ins('nop', '', 2)
    e.label('player_pc_012a3a')
    e.ins('move.l', '(%a0, %d1.w),%d1', 4)
    e.label('player_pc_012a3e')
    e.ins('move.l', '0xf3f4:w,%d2', 4)
    e.label('player_pc_012a42')
    e.ins('sub.l', '%d1,%d2', 2)
    e.label('player_pc_012a44')
    e.ins('bcs.w', 'player_pc_012a4c', 4)
    e.label('player_pc_012a48')
    e.ins('move.l', '%d2,0xf3f4:w', 4)
    e.label('player_pc_012a4c')
    e.ins('rts', '', 2)

def _lower_append_blinking_amount_place(e, rules):
    e.label('player_pc_012a4e')
    e.ins('cmpi.w', '#0x18,0xf39c:w', 6)
    e.label('player_pc_012a54')
    e.ins('bcs.b', 'player_pc_012a5c', 2)
    e.label('player_pc_012a56')
    e.ins('move.w', '#0x18,0xf39c:w', 6)
    e.label('player_pc_012a5c')
    e.ins('move.w', '0xf602:w,%d0', 4)
    e.label('player_pc_012a60')
    e.ins('andi.w', '#0x30,%d0', 4)
    e.label('player_pc_012a64')
    e.ins('bne.w', 'player_pc_012a8e', 4)
    e.label('player_pc_012a68')
    e.ins('subq.w', '#0x1,0xf39c:w', 4)
    e.label('player_pc_012a6c')
    e.ins('cmpi.w', '#0xc,0xf39c:w', 6)
    e.label('player_pc_012a72')
    e.ins('bcs.b', 'player_pc_012a8e', 2)
    e.label('player_pc_012a74')
    e.ins('lea.l', '26(%pc),%a0', 4)
    e.label('player_pc_012a78')
    e.ins('move.w', '#0x40,%d0', 4)
    e.label('player_pc_012a7c')
    e.ins('move.w', '0xf39a:w,%d1', 4)
    e.label('player_pc_012a80')
    e.ins('lsl.w', '#0x3,%d1', 2)
    e.label('player_pc_012a82')
    e.ins('addi.w', '#0x100,%d1', 4)
    e.label('player_pc_012a86')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_012a88')
    e.ins('jsr', 'player_pc_00ac08:l', 6)
    e.label('player_pc_012a8e')
    e.ins('rts', '', 2)

def _lower_prepare_percentage_panel(e, rules):
    e.label('player_pc_012a98')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_012a9c')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_012aa0')
    e.ins('bsr.w', 'player_pc_012ab6', 4)
    e.label('player_pc_012aa4')
    e.ins('bsr.w', 'player_pc_012ad4', 4)
    e.label('player_pc_012aa8')
    e.ins('bsr.w', 'player_pc_012b4c', 4)
    e.label('player_pc_012aac')
    e.ins('clr.w', '(%a0)', 2)
    e.label('player_pc_012aae')
    e.ins('addi.w', '#0x58,0xf31a:w', 6)
    e.label('player_pc_012ab4')
    e.ins('rts', '', 2)

def _lower_append_percentage_header_row(e, rules):
    e.label('player_pc_012ab6')
    e.ins('move.w', '#0x9,(%a0)+', 4)
    e.label('player_pc_012aba')
    e.ins('move.w', '#0xc49c,(%a0)+', 4)
    e.label('player_pc_012abe')
    e.ins('move.w', '#0xc380,(%a0)+', 4)
    e.label('player_pc_012ac2')
    e.ins('move.w', '#0x6,%d0', 4)
    e.label('player_pc_012ac6')
    e.ins('move.w', '#0xc381,(%a0)+', 4)
    e.label('player_pc_012aca')
    e.ins('dbra', '%d0,player_pc_012ac6', 4)
    e.label('player_pc_012ace')
    e.ins('move.w', '#0xcb80,(%a0)+', 4)
    e.label('player_pc_012ad2')
    e.ins('rts', '', 2)

def _lower_append_percentage_value_rows(e, rules):
    e.label('player_pc_012ad4')
    e.ins('move.w', '#0x9,0x16(%a0)', 6)
    e.label('player_pc_012ada')
    e.ins('move.w', '#0x9,(%a0)+', 4)
    e.label('player_pc_012ade')
    e.ins('move.w', '#0xc59c,0x16(%a0)', 6)
    e.label('player_pc_012ae4')
    e.ins('move.w', '#0xc51c,(%a0)+', 4)
    e.label('player_pc_012ae8')
    e.ins('move.w', '#0xc382,0x16(%a0)', 6)
    e.label('player_pc_012aee')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_012af2')
    e.ins('move.w', '#0xc029,%d0', 4)
    e.label('player_pc_012af6')
    e.ins('move.w', '%d0,(%a0)', 2)
    e.label('player_pc_012af8')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_012afa')
    e.ins('move.w', '%d0,0x16(%a0)', 4)
    e.label('player_pc_012afe')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_012b00')
    e.ins('addq.w', '#0x2,%a0', 2)
    e.label('player_pc_012b02')
    e.ins('move.w', '%d0,(%a0)', 2)
    e.label('player_pc_012b04')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_012b06')
    e.ins('move.w', '%d0,0x16(%a0)', 4)
    e.label('player_pc_012b0a')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_012b0c')
    e.ins('addq.w', '#0x2,%a0', 2)
    e.label('player_pc_012b0e')
    e.ins('move.w', '#0xc031,%d0', 4)
    e.label('player_pc_012b12')
    e.ins('move.w', '%d0,(%a0)', 2)
    e.label('player_pc_012b14')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_012b16')
    e.ins('move.w', '%d0,0x16(%a0)', 4)
    e.label('player_pc_012b1a')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_012b1c')
    e.ins('addq.w', '#0x2,%a0', 2)
    e.label('player_pc_012b1e')
    e.ins('move.w', '%d0,(%a0)', 2)
    e.label('player_pc_012b20')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_012b22')
    e.ins('move.w', '%d0,0x16(%a0)', 4)
    e.label('player_pc_012b26')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_012b28')
    e.ins('addq.w', '#0x2,%a0', 2)
    e.label('player_pc_012b2a')
    e.ins('move.w', '#0x2,%d0', 4)
    e.label('player_pc_012b2e')
    e.ins('move.w', '#0xc001,0x16(%a0)', 6)
    e.label('player_pc_012b34')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_012b38')
    e.ins('dbra', '%d0,player_pc_012b2e', 4)
    e.label('player_pc_012b3c')
    e.ins('move.w', '#0xcb82,0x16(%a0)', 6)
    e.label('player_pc_012b42')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_012b46')
    e.ins('adda.w', '#0x16,%a0', 4)
    e.label('player_pc_012b4a')
    e.ins('rts', '', 2)

def _lower_append_percentage_footer_row(e, rules):
    e.label('player_pc_012b4c')
    e.ins('move.w', '#0x9,(%a0)+', 4)
    e.label('player_pc_012b50')
    e.ins('move.w', '#0xc61c,(%a0)+', 4)
    e.label('player_pc_012b54')
    e.ins('move.w', '#0xd380,(%a0)+', 4)
    e.label('player_pc_012b58')
    e.ins('move.w', '#0x6,%d0', 4)
    e.label('player_pc_012b5c')
    e.ins('move.w', '#0xd381,(%a0)+', 4)
    e.label('player_pc_012b60')
    e.ins('dbra', '%d0,player_pc_012b5c', 4)
    e.label('player_pc_012b64')
    e.ins('move.w', '#0xdb80,(%a0)+', 4)
    e.label('player_pc_012b68')
    e.ins('rts', '', 2)

def _lower_clear_percentage_panel(e, rules):
    e.label('player_pc_012b6a')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_012b6e')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_012b72')
    e.ins('move.w', '#0x9,0x42(%a0)', 6)
    e.label('player_pc_012b78')
    e.ins('move.w', '#0x9,0x2c(%a0)', 6)
    e.label('player_pc_012b7e')
    e.ins('move.w', '#0x9,0x16(%a0)', 6)
    e.label('player_pc_012b84')
    e.ins('move.w', '#0x9,(%a0)+', 4)
    e.label('player_pc_012b88')
    e.ins('move.w', '#0xc61c,0x42(%a0)', 6)
    e.label('player_pc_012b8e')
    e.ins('move.w', '#0xc59c,0x2c(%a0)', 6)
    e.label('player_pc_012b94')
    e.ins('move.w', '#0xc51c,0x16(%a0)', 6)
    e.label('player_pc_012b9a')
    e.ins('move.w', '#0xc49c,(%a0)+', 4)
    e.label('player_pc_012b9e')
    e.ins('move.w', '#0x8,%d0', 4)
    e.label('player_pc_012ba2')
    e.ins('clr.w', '0x42(%a0)', 4)
    e.label('player_pc_012ba6')
    e.ins('clr.w', '0x2c(%a0)', 4)
    e.label('player_pc_012baa')
    e.ins('clr.w', '0x16(%a0)', 4)
    e.label('player_pc_012bae')
    e.ins('clr.w', '(%a0)+', 2)
    e.label('player_pc_012bb0')
    e.ins('dbra', '%d0,player_pc_012ba2', 4)
    e.label('player_pc_012bb4')
    e.ins('clr.w', '0x42(%a0)', 4)
    e.label('player_pc_012bb8')
    e.ins('addi.w', '#0x58,0xf31a:w', 6)
    e.label('player_pc_012bbe')
    e.ins('rts', '', 2)

def _lower_append_percentage_value(e, rules):
    e.label('player_pc_012bc0')
    e.ins('lea.l', '0xef00:w,%a6', 4)
    e.label('player_pc_012bc4')
    e.ins('moveq', '#0,%d0', 2)
    e.label('player_pc_012bc6')
    e.ins('move.w', '0xf3b6:w,%d0', 4)
    e.label('player_pc_012bca')
    e.ins('move.w', '#0xc386,%d1', 4)
    e.label('player_pc_012bce')
    e.ins('move.w', '#0xc001,%d2', 4)
    e.label('player_pc_012bd2')
    e.ins('jsr', 'player_pc_01270a:l', 6)
    e.label('player_pc_012bd8')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_012bdc')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_012be0')
    e.ins('move.w', '#0x2,(%a0)+', 4)
    e.label('player_pc_012be4')
    e.ins('move.w', '#0xc5a8,(%a0)+', 4)
    e.label('player_pc_012be8')
    e.ins('move.w', '0xef08:w,%d0', 4)
    e.label('player_pc_012bec')
    e.ins('cmpi.w', '#0xc001,%d0', 4)
    e.label('player_pc_012bf0')
    e.ins('bne.b', 'player_pc_012bfc', 2)
    e.label('player_pc_012bf2')
    e.ins('tst.w', '0xf3b8:w', 4)
    e.label('player_pc_012bf6')
    e.ins('bne.b', 'player_pc_012bfc', 2)
    e.label('player_pc_012bf8')
    e.ins('move.w', '#0xc386,%d0', 4)
    e.label('player_pc_012bfc')
    e.ins('move.w', '%d0,(%a0)+', 2)
    e.label('player_pc_012bfe')
    e.ins('move.w', '0xef0a:w,(%a0)+', 4)
    e.label('player_pc_012c02')
    e.ins('clr.w', '(%a0)', 2)
    e.label('player_pc_012c04')
    e.ins('addi.w', '#0x8,0xf31a:w', 6)
    e.label('player_pc_012c0a')
    e.ins('rts', '', 2)

def _lower_step_percentage_controls(e, rules):
    e.label('player_pc_012c0c')
    e.ins('move.b', '0xf602:w,%d0', 4)
    e.label('player_pc_012c10')
    e.ins('andi.b', '#0xc,%d0', 4)
    e.label('player_pc_012c14')
    e.ins('beq.b', 'player_pc_012c30', 2)
    e.label('player_pc_012c16')
    e.ins('subq.w', '#0x1,0xf608:w', 4)
    e.label('player_pc_012c1a')
    e.ins('bne.b', 'player_pc_012c82', 2)
    e.label('player_pc_012c1c')
    e.ins('btst.l', '#0x3,%d0', 4)
    e.label('player_pc_012c20')
    e.ins('bne.b', 'player_pc_012c28', 2)
    e.label('player_pc_012c22')
    e.ins('clr.w', '0xf3b8:w', 4)
    e.label('player_pc_012c26')
    e.ins('bra.b', 'player_pc_012c82', 2)
    e.label('player_pc_012c28')
    e.ins('move.w', '#0x1,0xf3b8:w', 6)
    e.label('player_pc_012c2e')
    e.ins('bra.b', 'player_pc_012c82', 2)
    e.label('player_pc_012c30')
    e.ins('move.b', '0xf602:w,%d0', 4)
    e.label('player_pc_012c34')
    e.ins('andi.b', '#0x3,%d0', 4)
    e.label('player_pc_012c38')
    e.ins('beq.b', 'player_pc_012c7c', 2)
    e.label('player_pc_012c3a')
    e.ins('subq.w', '#0x1,0xf608:w', 4)
    e.label('player_pc_012c3e')
    e.ins('bne.w', 'player_pc_012c82', 4)
    e.label('player_pc_012c42')
    e.ins('move.w', '#0xc,0xf608:w', 6)
    e.label('player_pc_012c48')
    e.ins('move.w', '#0x1,%d1', 4)
    e.label('player_pc_012c4c')
    e.ins('tst.w', '0xf3b8:w', 4)
    e.label('player_pc_012c50')
    e.ins('bne.b', 'player_pc_012c56', 2)
    e.label('player_pc_012c52')
    e.ins('move.w', '#0xa,%d1', 4)
    e.label('player_pc_012c56')
    e.ins('btst.b', '#0x1,0xf602:w', 6)
    e.label('player_pc_012c5c')
    e.ins('bne.b', 'player_pc_012c70', 2)
    e.label('player_pc_012c5e')
    e.ins('add.w', '%d1,0xf3b6:w', 4)
    e.label('player_pc_012c62')
    e.ins('cmpi.w', '#0x63,0xf3b6:w', 6)
    e.label('player_pc_012c68')
    e.ins('bls.b', 'player_pc_012c82', 2)
    e.label('player_pc_012c6a')
    e.ins('sub.w', '%d1,0xf3b6:w', 4)
    e.label('player_pc_012c6e')
    e.ins('bra.b', 'player_pc_012c82', 2)
    e.label('player_pc_012c70')
    e.ins('sub.w', '%d1,0xf3b6:w', 4)
    e.label('player_pc_012c74')
    e.ins('bpl.b', 'player_pc_012c82', 2)
    e.label('player_pc_012c76')
    e.ins('add.w', '%d1,0xf3b6:w', 4)
    e.label('player_pc_012c7a')
    e.ins('bra.b', 'player_pc_012c82', 2)
    e.label('player_pc_012c7c')
    e.ins('move.w', '#0x1,0xf608:w', 6)
    e.label('player_pc_012c82')
    e.ins('rts', '', 2)

def _lower_append_percentage_place_highlight(e, rules):
    e.label('player_pc_012c84')
    e.ins('btst.b', '#0x5,0xf603:w', 6)
    e.label('player_pc_012c8a')
    e.ins('bne.w', 'player_pc_012cb4', 4)
    e.label('player_pc_012c8e')
    e.ins('btst.b', '#0x3,0xf321:w', 6)
    e.label('player_pc_012c94')
    e.ins('bne.b', 'player_pc_012cb4', 2)
    e.label('player_pc_012c96')
    e.ins('lea.l', '30(%pc),%a0', 4)
    e.label('player_pc_012c9a')
    e.ins('nop', '', 2)
    e.label('player_pc_012c9c')
    e.ins('move.w', '#0x58,%d0', 4)
    e.label('player_pc_012ca0')
    e.ins('move.w', '#0xa0,%d1', 4)
    e.label('player_pc_012ca4')
    e.ins('tst.w', '0xf3b8:w', 4)
    e.label('player_pc_012ca8')
    e.ins('beq.b', 'player_pc_012cac', 2)
    e.label('player_pc_012caa')
    e.ins('addq.w', '#0x8,%d1', 2)
    e.label('player_pc_012cac')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_012cae')
    e.ins('jsr', 'player_pc_00ac08:l', 6)
    e.label('player_pc_012cb4')
    e.ins('rts', '', 2)

def _lower_prepare_resource_amount_panel(e, rules):
    e.label('player_pc_012cbe')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_012cc2')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_012cc6')
    e.ins('bsr.w', 'player_pc_012cf4', 4)
    e.label('player_pc_012cca')
    e.ins('bsr.w', 'player_pc_012dfc', 4)
    e.label('player_pc_012cce')
    e.ins('addi.w', '#0x16c,0xf31a:w', 6)
    e.label('player_pc_012cd4')
    e.ins('move.w', '#0x5,0xf39a:w', 6)
    e.label('player_pc_012cda')
    e.ins('move.w', '#0x1,0xf608:w', 6)
    e.label('player_pc_012ce0')
    e.ins('move.w', '#0x1,0xf608:w', 6)
    e.label('player_pc_012ce6')
    e.ins('ori.w', '#0x8040,0xf3a4:w', 6)
    e.label('player_pc_012cec')
    e.ins('andi.w', '#0xf9ff,0xf3a4:w', 6)
    e.label('player_pc_012cf2')
    e.ins('rts', '', 2)

def _lower_append_city_resource_amount_rows(e, rules):
    e.label('player_pc_012cf4')
    e.ins('move.w', '#0xc,(%a0)+', 4)
    e.label('player_pc_012cf8')
    e.ins('move.w', '#0xc0b4,(%a0)+', 4)
    e.label('player_pc_012cfc')
    e.ins('move.w', '#0xc380,(%a0)+', 4)
    e.label('player_pc_012d00')
    e.ins('move.w', '#0x9,%d0', 4)
    e.label('player_pc_012d04')
    e.ins('move.w', '#0xc381,(%a0)+', 4)
    e.label('player_pc_012d08')
    e.ins('dbra', '%d0,player_pc_012d04', 4)
    e.label('player_pc_012d0c')
    e.ins('move.w', '#0xcb80,(%a0)+', 4)
    e.label('player_pc_012d10')
    e.ins('move.w', '0xf364:w,%d0', 4)
    e.label('player_pc_012d14')
    e.ins('lsl.w', '#0x2,%d0', 2)
    e.label('player_pc_012d16')
    e.ins('lea.l', '0xdffc:w,%a1', 4)
    e.label('player_pc_012d1a')
    e.ins('move.l', '(%a1, %d0.w),%d0', 4)
    e.label('player_pc_012d1e')
    e.ins('move.w', '#0x1,%d1', 4)
    e.label('player_pc_012d22')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_012d24')
    e.ins('lea.l', '0xef18:w,%a6', 4)
    e.label('player_pc_012d28')
    e.ins('jsr', 'player_pc_01270a:l', 6)
    e.label('player_pc_012d2e')
    e.ins('move.w', '#0xc04d,%d0', 4)
    e.label('player_pc_012d32')
    e.ins('move.w', '#0xc1b4,%d1', 4)
    e.label('player_pc_012d36')
    e.ins('bsr.w', 'player_pc_012d82', 4)
    e.label('player_pc_012d3a')
    e.ins('move.w', '0xf364:w,%d0', 4)
    e.label('player_pc_012d3e')
    e.ins('lsl.w', '#0x2,%d0', 2)
    e.label('player_pc_012d40')
    e.ins('lea.l', '0xe09c:w,%a1', 4)
    e.label('player_pc_012d44')
    e.ins('move.l', '(%a1, %d0.w),%d0', 4)
    e.label('player_pc_012d48')
    e.ins('move.w', '#0x1,%d1', 4)
    e.label('player_pc_012d4c')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_012d4e')
    e.ins('lea.l', '0xef18:w,%a6', 4)
    e.label('player_pc_012d52')
    e.ins('jsr', 'player_pc_01270a:l', 6)
    e.label('player_pc_012d58')
    e.ins('move.w', '#0xc051,%d0', 4)
    e.label('player_pc_012d5c')
    e.ins('move.w', '#0xc2b4,%d1', 4)
    e.label('player_pc_012d60')
    e.ins('bsr.w', 'player_pc_012d82', 4)
    e.label('player_pc_012d64')
    e.ins('move.w', '#0xc,(%a0)+', 4)
    e.label('player_pc_012d68')
    e.ins('move.w', '#0xc334,(%a0)+', 4)
    e.label('player_pc_012d6c')
    e.ins('move.w', '#0xd380,(%a0)+', 4)
    e.label('player_pc_012d70')
    e.ins('move.w', '#0x9,%d0', 4)
    e.label('player_pc_012d74')
    e.ins('move.w', '#0xd381,(%a0)+', 4)
    e.label('player_pc_012d78')
    e.ins('dbra', '%d0,player_pc_012d74', 4)
    e.label('player_pc_012d7c')
    e.ins('move.w', '#0xdb80,(%a0)+', 4)
    e.label('player_pc_012d80')
    e.ins('rts', '', 2)

def _lower_append_live_resource_value_row(e, rules):
    e.label('player_pc_012d82')
    e.ins('move.w', '#0xc,0x1c(%a0)', 6)
    e.label('player_pc_012d88')
    e.ins('move.w', '#0xc,(%a0)+', 4)
    e.label('player_pc_012d8c')
    e.ins('move.w', '%d1,0x1c(%a0)', 4)
    e.label('player_pc_012d90')
    e.ins('subi.w', '#0x80,%d1', 4)
    e.label('player_pc_012d94')
    e.ins('move.w', '%d1,(%a0)+', 2)
    e.label('player_pc_012d96')
    e.ins('move.w', '#0xc382,0x1c(%a0)', 6)
    e.label('player_pc_012d9c')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_012da0')
    e.ins('move.w', '%d0,(%a0)', 2)
    e.label('player_pc_012da2')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_012da4')
    e.ins('move.w', '%d0,0x1c(%a0)', 4)
    e.label('player_pc_012da8')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_012daa')
    e.ins('addq.w', '#0x2,%a0', 2)
    e.label('player_pc_012dac')
    e.ins('move.w', '%d0,(%a0)', 2)
    e.label('player_pc_012dae')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_012db0')
    e.ins('move.w', '%d0,0x1c(%a0)', 4)
    e.label('player_pc_012db4')
    e.ins('addq.w', '#0x2,%a0', 2)
    e.label('player_pc_012db6')
    e.ins('move.w', '#0xc001,0x1c(%a0)', 6)
    e.label('player_pc_012dbc')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_012dc0')
    e.ins('move.w', '#0xc001,0x1c(%a0)', 6)
    e.label('player_pc_012dc6')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_012dca')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_012dce')
    e.ins('lea.l', '0xef18:w,%a1', 4)
    e.label('player_pc_012dd2')
    e.ins('move.w', '(%a1)+,%d1', 2)
    e.label('player_pc_012dd4')
    e.ins('beq.b', 'player_pc_012ddc', 2)
    e.label('player_pc_012dd6')
    e.ins('addi.w', '#0xc385,%d1', 4)
    e.label('player_pc_012dda')
    e.ins('bra.b', 'player_pc_012de0', 2)
    e.label('player_pc_012ddc')
    e.ins('move.w', '#0xc001,%d1', 4)
    e.label('player_pc_012de0')
    e.ins('move.w', '%d1,0x1c(%a0)', 4)
    e.label('player_pc_012de4')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_012de8')
    e.ins('dbra', '%d0,player_pc_012dd2', 4)
    e.label('player_pc_012dec')
    e.ins('move.w', '#0xcb82,0x1c(%a0)', 6)
    e.label('player_pc_012df2')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_012df6')
    e.ins('adda.w', '#0x1c,%a0', 4)
    e.label('player_pc_012dfa')
    e.ins('rts', '', 2)

def _lower_append_committed_resource_amount_rows(e, rules):
    e.label('player_pc_012dfc')
    e.ins('move.w', '#0xc,(%a0)+', 4)
    e.label('player_pc_012e00')
    e.ins('move.w', '#0xc434,(%a0)+', 4)
    e.label('player_pc_012e04')
    e.ins('move.w', '#0xc380,(%a0)+', 4)
    e.label('player_pc_012e08')
    e.ins('move.w', '#0x9,%d0', 4)
    e.label('player_pc_012e0c')
    e.ins('move.w', '#0xc381,(%a0)+', 4)
    e.label('player_pc_012e10')
    e.ins('dbra', '%d0,player_pc_012e0c', 4)
    e.label('player_pc_012e14')
    e.ins('move.w', '#0xcb80,(%a0)+', 4)
    e.label('player_pc_012e18')
    e.ins('move.w', '#0xc04d,%d0', 4)
    e.label('player_pc_012e1c')
    e.ins('move.w', '#0xc534,%d1', 4)
    e.label('player_pc_012e20')
    e.ins('move.l', '0xf39e:w,%d2', 4)
    e.label('player_pc_012e24')
    e.ins('bsr.w', 'player_pc_012e74', 4)
    e.label('player_pc_012e28')
    e.ins('move.w', '#0xc,(%a0)+', 4)
    e.label('player_pc_012e2c')
    e.ins('move.w', '#0xc5b4,(%a0)+', 4)
    e.label('player_pc_012e30')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_012e34')
    e.ins('move.w', '#0x9,%d0', 4)
    e.label('player_pc_012e38')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_012e3c')
    e.ins('dbra', '%d0,player_pc_012e38', 4)
    e.label('player_pc_012e40')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_012e44')
    e.ins('move.w', '#0xc051,%d0', 4)
    e.label('player_pc_012e48')
    e.ins('move.w', '#0xc6b4,%d1', 4)
    e.label('player_pc_012e4c')
    e.ins('move.l', '0xf3ba:w,%d2', 4)
    e.label('player_pc_012e50')
    e.ins('bsr.w', 'player_pc_012e74', 4)
    e.label('player_pc_012e54')
    e.ins('move.w', '#0xc,(%a0)+', 4)
    e.label('player_pc_012e58')
    e.ins('move.w', '#0xc734,(%a0)+', 4)
    e.label('player_pc_012e5c')
    e.ins('move.w', '#0xd380,(%a0)+', 4)
    e.label('player_pc_012e60')
    e.ins('move.w', '#0x9,%d0', 4)
    e.label('player_pc_012e64')
    e.ins('move.w', '#0xd381,(%a0)+', 4)
    e.label('player_pc_012e68')
    e.ins('dbra', '%d0,player_pc_012e64', 4)
    e.label('player_pc_012e6c')
    e.ins('move.w', '#0xdb80,(%a0)+', 4)
    e.label('player_pc_012e70')
    e.ins('clr.w', '(%a0)', 2)
    e.label('player_pc_012e72')
    e.ins('rts', '', 2)

def _lower_append_committed_resource_value_row(e, rules):
    e.label('player_pc_012e74')
    e.ins('move.w', '#0xc,0x1c(%a0)', 6)
    e.label('player_pc_012e7a')
    e.ins('move.w', '#0xc,(%a0)+', 4)
    e.label('player_pc_012e7e')
    e.ins('move.w', '%d1,0x1c(%a0)', 4)
    e.label('player_pc_012e82')
    e.ins('subi.w', '#0x80,%d1', 4)
    e.label('player_pc_012e86')
    e.ins('move.w', '%d1,(%a0)+', 2)
    e.label('player_pc_012e88')
    e.ins('move.w', '#0xc382,0x1c(%a0)', 6)
    e.label('player_pc_012e8e')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_012e92')
    e.ins('move.w', '%d0,(%a0)', 2)
    e.label('player_pc_012e94')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_012e96')
    e.ins('move.w', '%d0,0x1c(%a0)', 4)
    e.label('player_pc_012e9a')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_012e9c')
    e.ins('addq.w', '#0x2,%a0', 2)
    e.label('player_pc_012e9e')
    e.ins('move.w', '%d0,(%a0)', 2)
    e.label('player_pc_012ea0')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_012ea2')
    e.ins('move.w', '%d0,0x1c(%a0)', 4)
    e.label('player_pc_012ea6')
    e.ins('addq.w', '#0x2,%a0', 2)
    e.label('player_pc_012ea8')
    e.ins('move.w', '%d2,%d0', 2)
    e.label('player_pc_012eaa')
    e.ins('move.w', '#0x1,%d1', 4)
    e.label('player_pc_012eae')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_012eb0')
    e.ins('lea.l', '0xef18:w,%a6', 4)
    e.label('player_pc_012eb4')
    e.ins('jsr', 'player_pc_01270a:l', 6)
    e.label('player_pc_012eba')
    e.ins('lea.l', '0xef18:w,%a6', 4)
    e.label('player_pc_012ebe')
    e.ins('move.w', '#0x7,%d0', 4)
    e.label('player_pc_012ec2')
    e.ins('cmpi.w', '#0x5,%d0', 4)
    e.label('player_pc_012ec6')
    e.ins('bhi.b', 'player_pc_012ed2', 2)
    e.label('player_pc_012ec8')
    e.ins('move.w', '(%a6)+,%d3', 2)
    e.label('player_pc_012eca')
    e.ins('beq.b', 'player_pc_012ed2', 2)
    e.label('player_pc_012ecc')
    e.ins('addi.w', '#0xc385,%d3', 4)
    e.label('player_pc_012ed0')
    e.ins('bra.b', 'player_pc_012ed6', 2)
    e.label('player_pc_012ed2')
    e.ins('move.w', '#0xc001,%d3', 4)
    e.label('player_pc_012ed6')
    e.ins('move.w', '%d3,0x1c(%a0)', 4)
    e.label('player_pc_012eda')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_012ede')
    e.ins('dbra', '%d0,player_pc_012ec2', 4)
    e.label('player_pc_012ee2')
    e.ins('move.w', '#0xcb82,0x1c(%a0)', 6)
    e.label('player_pc_012ee8')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_012eec')
    e.ins('adda.w', '#0x1c,%a0', 4)
    e.label('player_pc_012ef0')
    e.ins('rts', '', 2)

LOWERERS = {
    'prepare_budget_summary_panel':_lower_prepare_budget_summary_panel,
    'append_numbered_budget_columns':_lower_append_numbered_budget_columns,
    'prepare_compact_budget_summary_panel':_lower_prepare_compact_budget_summary_panel,
    'select_descriptor_portrait_parts':_lower_select_descriptor_portrait_parts,
    'find_first_set_mask_bit':_lower_find_first_set_mask_bit,
    'prepare_command_amount_modal':_lower_prepare_command_amount_modal,
    'append_amount_modal_frame':_lower_append_amount_modal_frame,
    'append_amount_modal_descriptor_limit':_lower_append_amount_modal_descriptor_limit,
    'append_selected_command_row_label':_lower_append_selected_command_row_label,
    'clear_command_amount_page':_lower_clear_command_amount_page,
    'prepare_budget_amount_page':_lower_prepare_budget_amount_page,
    'step_budget_amount_controls':_lower_step_budget_amount_controls,
    'append_budget_cost_and_amount_values':_lower_append_budget_cost_and_amount_values,
    'append_budget_place_highlight':_lower_append_budget_place_highlight,
    'append_budget_header_row':_lower_append_budget_header_row,
    'append_budget_first_detail_rows':_lower_append_budget_first_detail_rows,
    'append_budget_second_detail_row':_lower_append_budget_second_detail_row,
    'append_budget_footer_row':_lower_append_budget_footer_row,
    'append_four_budget_numbered_tiles':_lower_append_four_budget_numbered_tiles,
    'append_six_place_decimal_value':_lower_append_six_place_decimal_value,
    'append_decimal_value_place':_lower_append_decimal_value_place,
    'prepare_command_amount_limit':_lower_prepare_command_amount_limit,
    'limit_live_command_amount_by_price_record':_lower_limit_live_command_amount_by_price_record,
    'update_player_command_amount':_lower_update_player_command_amount,
    'append_selected_command_amount':_lower_append_selected_command_amount,
    'step_live_command_amount_controls':_lower_step_live_command_amount_controls,
    'select_previous_amount_place':_lower_select_previous_amount_place,
    'select_next_amount_place':_lower_select_next_amount_place,
    'decrement_live_command_amount_small':_lower_decrement_live_command_amount_small,
    'append_blinking_amount_place':_lower_append_blinking_amount_place,
    'prepare_percentage_panel':_lower_prepare_percentage_panel,
    'append_percentage_header_row':_lower_append_percentage_header_row,
    'append_percentage_value_rows':_lower_append_percentage_value_rows,
    'append_percentage_footer_row':_lower_append_percentage_footer_row,
    'clear_percentage_panel':_lower_clear_percentage_panel,
    'append_percentage_value':_lower_append_percentage_value,
    'step_percentage_controls':_lower_step_percentage_controls,
    'append_percentage_place_highlight':_lower_append_percentage_place_highlight,
    'prepare_resource_amount_panel':_lower_prepare_resource_amount_panel,
    'append_city_resource_amount_rows':_lower_append_city_resource_amount_rows,
    'append_live_resource_value_row':_lower_append_live_resource_value_row,
    'append_committed_resource_amount_rows':_lower_append_committed_resource_amount_rows,
    'append_committed_resource_value_row':_lower_append_committed_resource_value_row,
}

def compile_budget(source):
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    for name, phases in {
        'append_six_place_decimal_value':('_six_place_decimal_fields','_decimal_value_place_fields'),
        'append_decimal_value_place':('_decimal_value_place_fields',),
    }.items():
        records[name]['effects']=dict(actual_projection=records[name]['effects'],
            actual_field_algorithms={phase:records[phase]['effects'] for phase in phases})
    return lower_declared({b.name:records[b.name] for b in BUDGET_BINDINGS}, BUDGET_BINDINGS, LOWERERS)

# C56 complete menu ABI and honest same-core compatibility declarations.
DECLARATIONS.update({'_budget_known_fields': {'signature': 'memory, frame, target', 'returns': None, 'flow': 'if target == 72946:\n    return prepare_budget_summary_panel_frame_fields(memory, frame)\nif target == 73258:\n    return append_numbered_budget_columns_frame_fields(memory, frame)\nif target == 73276:\n    return prepare_compact_budget_summary_panel_frame_fields(memory, frame)\nif target == 73602:\n    return select_descriptor_portrait_parts_frame_fields(memory, frame)\nif target == 73722:\n    return find_first_set_mask_bit_frame_fields(memory, frame)\nif target == 73736:\n    return prepare_command_amount_modal_frame_fields(memory, frame)\nif target == 73764:\n    return append_amount_modal_frame_frame_fields(memory, frame)\nif target == 73828:\n    return append_amount_modal_descriptor_limit_frame_fields(memory, frame)\nif target == 74268:\n    return append_selected_command_row_label_frame_fields(memory, frame)\nif target == 74386:\n    return clear_command_amount_page_frame_fields(memory, frame)\nif target == 74516:\n    return prepare_budget_amount_page_frame_fields(memory, frame)\nif target == 74776:\n    return step_budget_amount_controls_frame_fields(memory, frame)\nif target == 75052:\n    return append_budget_cost_and_amount_values_frame_fields(memory, frame)\nif target == 75180:\n    return append_budget_place_highlight_frame_fields(memory, frame)\nif target == 75266:\n    return append_budget_header_row_frame_fields(memory, frame)\nif target == 75296:\n    return append_budget_first_detail_rows_frame_fields(memory, frame)\nif target == 75404:\n    return append_budget_second_detail_row_frame_fields(memory, frame)\nif target == 75474:\n    return append_budget_footer_row_frame_fields(memory, frame)\nif target == 75504:\n    return append_four_budget_numbered_tiles_frame_fields(memory, frame)\nif target == 75530:\n    return append_six_place_decimal_value_frame_fields(memory, frame)\nif target == 75616:\n    return append_decimal_value_place_frame_fields(memory, frame)\nif target == 75660:\n    return prepare_command_amount_limit_frame_fields(memory, frame)\nif target == 75896:\n    return limit_live_command_amount_by_price_record_frame_fields(memory, frame)\nif target == 76002:\n    return update_player_command_amount_frame_fields(memory, frame)\nif target == 76076:\n    return append_selected_command_amount_frame_fields(memory, frame)\nif target == 76160:\n    return step_live_command_amount_controls_frame_fields(memory, frame)\nif target == 76254:\n    return select_previous_amount_place_frame_fields(memory, frame)\nif target == 76280:\n    return select_next_amount_place_frame_fields(memory, frame)\nif target == 76334:\n    return decrement_live_command_amount_small_frame_fields(memory, frame)\nif target == 76366:\n    return append_blinking_amount_place_frame_fields(memory, frame)\nif target == 76440:\n    return prepare_percentage_panel_frame_fields(memory, frame)\nif target == 76470:\n    return append_percentage_header_row_frame_fields(memory, frame)\nif target == 76500:\n    return append_percentage_value_rows_frame_fields(memory, frame)\nif target == 76620:\n    return append_percentage_footer_row_frame_fields(memory, frame)\nif target == 76650:\n    return clear_percentage_panel_frame_fields(memory, frame)\nif target == 76736:\n    return append_percentage_value_frame_fields(memory, frame)\nif target == 76812:\n    return step_percentage_controls_frame_fields(memory, frame)\nif target == 76932:\n    return append_percentage_place_highlight_frame_fields(memory, frame)\nif target == 76990:\n    return prepare_resource_amount_panel_frame_fields(memory, frame)\nif target == 77044:\n    return append_city_resource_amount_rows_frame_fields(memory, frame)\nif target == 77186:\n    return append_live_resource_value_row_frame_fields(memory, frame)\nif target == 77308:\n    return append_committed_resource_amount_rows_frame_fields(memory, frame)\nif target == 77428:\n    return append_committed_resource_value_row_frame_fields(memory, frame)\nreturn None'}, '_command_legacy_entry': {'signature': 'state, entry_frame, original_entry', 'returns': None, 'flow': "checked_state(state)\nif entry_frame is None:\n    raise Boundary('historical scalar menu API lacks actual complete entry carriers; use its named frame core')\nif type(entry_frame) is not CommandFrame:\n    raise ValueError('actual complete CommandFrame required')\nuint(original_entry, 32)\nmemory = CommandMenuMemory(state)\nreturn (memory, memory.enter(entry_frame))"}, 'append_amount_modal_descriptor_limit': {'signature': 'state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': "memory, entered = _command_legacy_entry(state, entry_frame, 73828)\nchecked_cursor(out, state)\nif out.base != entered.addresses[0]:\n    raise ValueError('legacy output must be the actual A0 entry')\nactual = append_amount_modal_descriptor_limit_frame_fields(memory, entered)\nout.base = actual.addresses[0]\nreturn None"}, 'append_amount_modal_descriptor_limit_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 13, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 13, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 49588, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49460, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49233, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 49234, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 2), 49235, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 32), 49236, 16)\nframe = frame.with_address(0, frame.addresses[0] + 4)\nframe = _command_load_fields(memory, frame, 0, 2, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 49153, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nvalue = memory.state.read(16726060, 4)\nframe = frame.with_address(1, value)\nvalue = memory.state.read(u32(frame.addresses[1] + 5), 1)\nframe = _command_load_fields(memory, frame, 0, value, 8)\nframe = _command_shift_fields(memory, frame, 0, 8, 16, False)\nvalue = memory.state.read(u32(frame.addresses[1] + 6), 1)\nframe = _command_load_fields(memory, frame, 0, value, 8)\nframe = _command_shift_fields(memory, frame, 0, 8, 32, False)\nvalue = memory.state.read(u32(frame.addresses[1] + 7), 1)\nframe = _command_load_fields(memory, frame, 0, value, 8)\nframe = _command_shift_fields(memory, frame, 0, 8, 32, False)\nvalue = memory.state.read(u32(frame.addresses[1] + 8), 1)\nframe = _command_load_fields(memory, frame, 0, value, 8)\nframe = _command_store_fields(memory, frame, 4294964216, frame.data[0], 32)\nframe = _command_load_fields(memory, frame, 1, 50054, 16)\nframe = _command_load_fields(memory, frame, 2, 49153, 16)\nframe = frame.with_address(6, 4294955776)\nframe = _command_call_fields(memory, frame, 75530, 73950)\nframe = frame.with_address(1, 4294955776)\nframe = _command_load_fields(memory, frame, 0, 5, 16)\nwhile True:\n    value = memory.state.read(u32(frame.addresses[1]), 2)\n    frame = frame.with_address(1, frame.addresses[1] + 2)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), value, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 0, 16, True)\nreturn frame'}, 'append_amount_modal_frame': {'signature': 'state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': "memory, entered = _command_legacy_entry(state, entry_frame, 73764)\nchecked_cursor(out, state)\nif out.base != entered.addresses[0]:\n    raise ValueError('legacy output must be the actual A0 entry')\nactual = append_amount_modal_frame_frame_fields(memory, entered)\nout.base = actual.addresses[0]\nreturn None"}, 'append_amount_modal_frame_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 13, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 13, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 49716, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49332, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 54144, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 10, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 54145, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 56192, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(30))\nreturn frame'}, 'append_blinking_amount_place': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 76366)\nactual = append_blinking_amount_place_frame_fields(memory, entered)\nreturn None'}, 'append_blinking_amount_place_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\ndestination = memory.state.read(4294964124, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 24, 16, True, True)\nif not bool(frame.status_word & 1):\n    frame = _command_store_fields(memory, frame, 4294964124, 24, 16)\nvalue = memory.state.read(4294964738, 2)\nframe = _command_load_fields(memory, frame, 0, value, 16)\nresult = frame.data[0] & 65535 & 48\nframe = _command_load_fields(memory, frame, 0, result, 16)\nif not not frame.status_word & 4:\n    destination = memory.state.read(4294964124, 2)\n    frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)\n    memory.state.write(4294964124, 2, result)\n    destination = memory.state.read(4294964124, 2)\n    frame, result = _command_binary_fields(memory, frame, destination, 12, 16, True, True)\n    if not bool(frame.status_word & 1):\n        frame = frame.with_address(0, u32(76406 + 26))\n        frame = _command_load_fields(memory, frame, 0, 64, 16)\n        value = memory.state.read(4294964122, 2)\n        frame = _command_load_fields(memory, frame, 1, value, 16)\n        frame = _command_shift_fields(memory, frame, 1, 3, 16, False)\n        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 256, 16, False, False)\n        frame = frame.with_data(1, result, 16)\n        frame = _command_load_fields(memory, frame, 2, 0, 16)\n        frame = _command_call_fields(memory, frame, 44040, 76430)\nreturn frame'}, 'append_budget_cost_and_amount_values': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'Cursor', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 75052)\nactual = append_budget_cost_and_amount_values_frame_fields(memory, entered)\nreturn memory.cursor_at(actual.addresses[0])'}, 'append_budget_cost_and_amount_values_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nvalue = memory.state.read(4294964154, 4)\nframe = _command_load_fields(memory, frame, 0, value, 32)\nframe = _command_load_fields(memory, frame, 1, 50054, 16)\nframe = _command_load_fields(memory, frame, 2, 49153, 16)\nframe = frame.with_address(6, 4294962944)\nframe = _command_call_fields(memory, frame, 75530, 75082)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50874, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(1, 4294962944)\nframe = _command_load_fields(memory, frame, 0, 5, 16)\nframe = _command_load_fields(memory, frame, 1, 0, 16)\nwhile True:\n    value = memory.state.read(u32(frame.addresses[1]), 2)\n    frame = frame.with_address(1, frame.addresses[1] + 2)\n    frame = _command_load_fields(memory, frame, 2, value, 16)\n    frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 49153, 16, True, True)\n    if not not frame.status_word & 4:\n        source = memory.state.read(4294964122, 2)\n        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, source, 16, True, True)\n        if not bool(frame.status_word & 1):\n            frame = _command_load_fields(memory, frame, 2, 50054, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[2] & 65535, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, False, False)\n    frame = frame.with_data(1, result, 16)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nvalue = memory.state.read(4294964212, 4)\nframe = _command_load_fields(memory, frame, 0, value, 32)\nframe = _command_load_fields(memory, frame, 1, 50054, 16)\nframe = _command_load_fields(memory, frame, 2, 49153, 16)\nframe = frame.with_address(6, 4294962944)\nframe = _command_call_fields(memory, frame, 75530, 75148)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 51130, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(1, 4294962944)\nframe = _command_load_fields(memory, frame, 0, 5, 16)\nwhile True:\n    value = memory.state.read(u32(frame.addresses[1]), 2)\n    frame = frame.with_address(1, frame.addresses[1] + 2)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), value, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 32, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame'}, 'append_budget_first_detail_rows': {'signature': 'state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': "memory, entered = _command_legacy_entry(state, entry_frame, 75296)\nchecked_cursor(out, state)\nif out.base != entered.addresses[0]:\n    raise ValueError('legacy output must be the actual A0 entry')\nactual = append_budget_first_detail_rows_frame_fields(memory, entered)\nout.base = actual.addresses[0]\nreturn None"}, 'append_budget_first_detail_rows_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 8, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 50466, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50338, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 49297, 16)\nframe = _command_call_fields(memory, frame, 75504, 75334)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 4, 16, False, False)\nframe = frame.with_data(0, result, 16)\nframe = _command_call_fields(memory, frame, 75504, 75340)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 49153, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 49153, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(20))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50594, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 5, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nreturn frame'}, 'append_budget_footer_row': {'signature': 'state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': "memory, entered = _command_legacy_entry(state, entry_frame, 75474)\nchecked_cursor(out, state)\nif out.base != entered.addresses[0]:\n    raise ValueError('legacy output must be the actual A0 entry')\nactual = append_budget_footer_row_frame_fields(memory, entered)\nout.base = actual.addresses[0]\nreturn None"}, 'append_budget_footer_row_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50978, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 5, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54145, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 56192, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nreturn frame'}, 'append_budget_header_row': {'signature': 'state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': "memory, entered = _command_legacy_entry(state, entry_frame, 75266)\nchecked_cursor(out, state)\nif out.base != entered.addresses[0]:\n    raise ValueError('legacy output must be the actual A0 entry')\nactual = append_budget_header_row_frame_fields(memory, entered)\nout.base = actual.addresses[0]\nreturn None"}, 'append_budget_header_row_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50210, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 5, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nreturn frame'}, 'append_budget_place_highlight': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 75180)\nactual = append_budget_place_highlight_frame_fields(memory, entered)\nreturn None'}, 'append_budget_place_highlight_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\ntested = memory.state.read(4294964001, 1)\nframe = _command_bit_fields(memory, frame, tested, 4 % 8)\nif not not frame.status_word & 4:\n    frame = frame.with_address(0, u32(75190 + 26))\n    frame = _command_load_fields(memory, frame, 0, 104, 16)\n    value = memory.state.read(4294964122, 2)\n    frame = _command_load_fields(memory, frame, 1, value, 16)\n    frame = _command_shift_fields(memory, frame, 1, 3, 16, False)\n    frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 232, 16, False, False)\n    frame = frame.with_data(1, result, 16)\n    frame = _command_load_fields(memory, frame, 2, 0, 16)\n    frame = _command_call_fields(memory, frame, 44040, 75214)\nreturn frame'}, 'append_budget_second_detail_row': {'signature': 'state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': "memory, entered = _command_legacy_entry(state, entry_frame, 75404)\nchecked_cursor(out, state)\nif out.base != entered.addresses[0]:\n    raise ValueError('legacy output must be the actual A0 entry')\nactual = append_budget_second_detail_row_frame_fields(memory, entered)\nout.base = actual.addresses[0]\nreturn None"}, 'append_budget_second_detail_row_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 8, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 50850, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50722, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 49297, 16)\nframe = _command_call_fields(memory, frame, 75504, 75442)\nframe = _command_load_fields(memory, frame, 0, 49305, 16)\nframe = _command_call_fields(memory, frame, 75504, 75450)\nframe = _command_load_fields(memory, frame, 0, 49297, 16)\nframe = _command_call_fields(memory, frame, 75504, 75458)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(20))\nreturn frame'}, 'append_city_resource_amount_rows': {'signature': 'state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None', 'returns': 'ResourceRowsResult', 'flow': "memory, entered = _command_legacy_entry(state, entry_frame, 77044)\nchecked_cursor(out, state)\nif out.base != entered.addresses[0]:\n    raise ValueError('legacy output must be the actual A0 entry')\nactual = append_city_resource_amount_rows_frame_fields(memory, entered)\nout.base = actual.addresses[0]\nreturn ResourceRowsResult(memory.cursor_at(actual.addresses[0]), actual.data[0])"}, 'append_city_resource_amount_rows_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 12, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49332, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 9, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nvalue = memory.state.read(4294964068, 2)\nframe = _command_load_fields(memory, frame, 0, value, 16)\nframe = _command_shift_fields(memory, frame, 0, 2, 16, False)\nframe = frame.with_address(1, 4294959100)\nvalue = memory.state.read(u32(frame.addresses[1] + s16(frame.data[0] & 65535)), 4)\nframe = _command_load_fields(memory, frame, 0, value, 32)\nframe = _command_load_fields(memory, frame, 1, 1, 16)\nframe = _command_load_fields(memory, frame, 2, 0, 16)\nframe = frame.with_address(6, 4294962968)\nframe = _command_call_fields(memory, frame, 75530, 77102)\nframe = _command_load_fields(memory, frame, 0, 49229, 16)\nframe = _command_load_fields(memory, frame, 1, 49588, 16)\nframe = _command_call_fields(memory, frame, 77186, 77114)\nvalue = memory.state.read(4294964068, 2)\nframe = _command_load_fields(memory, frame, 0, value, 16)\nframe = _command_shift_fields(memory, frame, 0, 2, 16, False)\nframe = frame.with_address(1, 4294959260)\nvalue = memory.state.read(u32(frame.addresses[1] + s16(frame.data[0] & 65535)), 4)\nframe = _command_load_fields(memory, frame, 0, value, 32)\nframe = _command_load_fields(memory, frame, 1, 1, 16)\nframe = _command_load_fields(memory, frame, 2, 0, 16)\nframe = frame.with_address(6, 4294962968)\nframe = _command_call_fields(memory, frame, 75530, 77144)\nframe = _command_load_fields(memory, frame, 0, 49233, 16)\nframe = _command_load_fields(memory, frame, 1, 49844, 16)\nframe = _command_call_fields(memory, frame, 77186, 77156)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 12, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49972, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 9, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54145, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 56192, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nreturn frame'}, 'append_committed_resource_amount_rows': {'signature': 'state: GameState, context: ResourceRowsInput, *, entry_frame: CommandFrame | None=None', 'returns': 'ResourceRowsResult', 'flow': "memory, entered = _command_legacy_entry(state, entry_frame, 77308)\ncontext.validate(state)\nif context.destination.base != entered.addresses[0]:\n    raise ValueError('resource context must match real A0 entry')\nif context.numeric_carrier != entered.data[0]:\n    raise ValueError('actual resource LONG required')\nactual = append_committed_resource_amount_rows_frame_fields(memory, entered)\nreturn ResourceRowsResult(memory.cursor_at(actual.addresses[0]), actual.data[0])"}, 'append_committed_resource_amount_rows_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 12, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50228, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 9, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 49229, 16)\nframe = _command_load_fields(memory, frame, 1, 50484, 16)\nvalue = memory.state.read(4294964126, 4)\nframe = _command_load_fields(memory, frame, 2, value, 32)\nframe = _command_call_fields(memory, frame, 77428, 77352)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 12, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50612, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 9, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 49233, 16)\nframe = _command_load_fields(memory, frame, 1, 50868, 16)\nvalue = memory.state.read(4294964154, 4)\nframe = _command_load_fields(memory, frame, 2, value, 32)\nframe = _command_call_fields(memory, frame, 77428, 77396)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 12, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50996, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 9, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54145, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 56192, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\nreturn frame'}, 'append_committed_resource_value_row': {'signature': 'state: GameState, context: CommittedResourceRowInput, *, entry_frame: CommandFrame | None=None', 'returns': 'ResourceRowsResult', 'flow': "memory, entered = _command_legacy_entry(state, entry_frame, 77428)\ncontext.validate(state)\nif context.destination.base != entered.addresses[0]:\n    raise ValueError('resource context must match real A0 entry')\nif context.tile_carrier != entered.data[0]:\n    raise ValueError('actual resource LONG required')\nactual = append_committed_resource_value_row_frame_fields(memory, entered)\nreturn ResourceRowsResult(memory.cursor_at(actual.addresses[0]), actual.data[0])"}, 'append_committed_resource_value_row_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), 12, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 12, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), frame.data[1] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 128, 16, True, False)\nframe = frame.with_data(1, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[1] & 65535, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[0] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)\nframe = frame.with_data(0, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), frame.data[0] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)\nframe = frame.with_data(0, result, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[0] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)\nframe = frame.with_data(0, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), frame.data[0] & 65535, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, frame.data[2] & 65535, 16)\nframe = _command_load_fields(memory, frame, 1, 1, 16)\nframe = _command_load_fields(memory, frame, 2, 0, 16)\nframe = frame.with_address(6, 4294962968)\nframe = _command_call_fields(memory, frame, 75530, 77498)\nframe = frame.with_address(6, 4294962968)\nframe = _command_load_fields(memory, frame, 0, 7, 16)\nwhile True:\n    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 5, 16, True, True)\n    if not frame.status_word & 5:\n        frame = _command_load_fields(memory, frame, 3, 49153, 16)\n    else:\n        value = memory.state.read(u32(frame.addresses[6]), 2)\n        frame = frame.with_address(6, frame.addresses[6] + 2)\n        frame = _command_load_fields(memory, frame, 3, value, 16)\n        if bool(frame.status_word & 4):\n            frame = _command_load_fields(memory, frame, 3, 49153, 16)\n        else:\n            frame, result = _command_binary_fields(memory, frame, frame.data[3] & 65535, 50053, 16, False, False)\n            frame = frame.with_data(3, result, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), frame.data[3] & 65535, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(28))\nreturn frame'}, 'append_decimal_value_place_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nreturn _command_decimal_place_fields(memory, frame)'}, 'append_four_budget_numbered_tiles': {'signature': 'state: GameState, out: Cursor, tile: Word, *, entry_frame: CommandFrame | None=None', 'returns': 'Word', 'flow': "memory, entered = _command_legacy_entry(state, entry_frame, 75504)\nchecked_cursor(out, state)\nif out.base != entered.addresses[0]:\n    raise ValueError('legacy output must be the actual A0 entry')\nuint(tile, 16)\nif tile != entered.data[0] & 65535:\n    raise ValueError('actual numbered tile WORD required')\nactual = append_four_budget_numbered_tiles_frame_fields(memory, entered)\nout.base = actual.addresses[0]\nreturn actual.data[0] & 65535"}, 'append_four_budget_numbered_tiles_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _command_load_fields(memory, frame, 1, frame.data[0] & 65535, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[1] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, False, False)\nframe = frame.with_data(1, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), frame.data[1] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, False, False)\nframe = frame.with_data(1, result, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[1] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, False, False)\nframe = frame.with_data(1, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), frame.data[1] & 65535, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nreturn frame'}, 'append_live_resource_value_row': {'signature': 'state: GameState, context: ResourceRowInput, *, entry_frame: CommandFrame | None=None', 'returns': 'ResourceRowsResult', 'flow': "memory, entered = _command_legacy_entry(state, entry_frame, 77186)\ncontext.validate(state)\nif context.destination.base != entered.addresses[0]:\n    raise ValueError('resource context must match real A0 entry')\nif context.tile_carrier != entered.data[0]:\n    raise ValueError('actual resource LONG required')\nactual = append_live_resource_value_row_frame_fields(memory, entered)\nreturn ResourceRowsResult(memory.cursor_at(actual.addresses[0]), actual.data[0])"}, 'append_live_resource_value_row_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), 12, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 12, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), frame.data[1] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 128, 16, True, False)\nframe = frame.with_data(1, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[1] & 65535, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[0] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)\nframe = frame.with_data(0, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), frame.data[0] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)\nframe = frame.with_data(0, result, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[0] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)\nframe = frame.with_data(0, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), frame.data[0] & 65535, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), 49153, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), 49153, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 5, 16)\nframe = frame.with_address(1, 4294962968)\nwhile True:\n    value = memory.state.read(u32(frame.addresses[1]), 2)\n    frame = frame.with_address(1, frame.addresses[1] + 2)\n    frame = _command_load_fields(memory, frame, 1, value, 16)\n    if bool(frame.status_word & 4):\n        frame = _command_load_fields(memory, frame, 1, 49153, 16)\n    else:\n        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 50053, 16, False, False)\n        frame = frame.with_data(1, result, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), frame.data[1] & 65535, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(28))\nreturn frame'}, 'append_numbered_budget_columns': {'signature': 'state: GameState, out: Cursor, tile: Word, latch: Word, *, entry_frame: CommandFrame | None=None', 'returns': 'Word', 'flow': "memory, entered = _command_legacy_entry(state, entry_frame, 73258)\nchecked_cursor(out, state)\nif out.base != entered.addresses[0]:\n    raise ValueError('legacy output must be the actual A0 entry')\nuint(tile, 16)\nif tile != entered.data[1] & 65535:\n    raise ValueError('actual numbered tile WORD required')\nuint(latch, 16)\nif latch != entered.data[2] & 65535:\n    raise ValueError('actual loop counter WORD required')\nactual = append_numbered_budget_columns_frame_fields(memory, entered)\nout.base = actual.addresses[0]\nreturn actual.data[1] & 65535"}, 'append_numbered_budget_columns_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': "frame = memory.enter(frame)\nreturn _command_numbered_pair_fields(memory, frame, 'budget')"}, 'append_percentage_footer_row': {'signature': 'state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': "memory, entered = _command_legacy_entry(state, entry_frame, 76620)\nchecked_cursor(out, state)\nif out.base != entered.addresses[0]:\n    raise ValueError('legacy output must be the actual A0 entry')\nactual = append_percentage_footer_row_frame_fields(memory, entered)\nout.base = actual.addresses[0]\nreturn None"}, 'append_percentage_footer_row_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 9, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50716, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 6, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54145, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 56192, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nreturn frame'}, 'append_percentage_header_row': {'signature': 'state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': "memory, entered = _command_legacy_entry(state, entry_frame, 76470)\nchecked_cursor(out, state)\nif out.base != entered.addresses[0]:\n    raise ValueError('legacy output must be the actual A0 entry')\nactual = append_percentage_header_row_frame_fields(memory, entered)\nout.base = actual.addresses[0]\nreturn None"}, 'append_percentage_header_row_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 9, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50332, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 6, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nreturn frame'}, 'append_percentage_place_highlight': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 76932)\nactual = append_percentage_place_highlight_frame_fields(memory, entered)\nreturn None'}, 'append_percentage_place_highlight_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\ntested = memory.state.read(4294964739, 1)\nframe = _command_bit_fields(memory, frame, tested, 5 % 8)\nif not not frame.status_word & 4:\n    tested = memory.state.read(4294964001, 1)\n    frame = _command_bit_fields(memory, frame, tested, 3 % 8)\n    if not not frame.status_word & 4:\n        frame = frame.with_address(0, u32(76952 + 30))\n        frame = _command_load_fields(memory, frame, 0, 88, 16)\n        frame = _command_load_fields(memory, frame, 1, 160, 16)\n        value = memory.state.read(4294964152, 2)\n        frame = _command_test_fields(memory, frame, value, 16)\n        if not bool(frame.status_word & 4):\n            frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 8, 16, False, False)\n            frame = frame.with_data(1, result, 16)\n        frame = _command_load_fields(memory, frame, 2, 0, 16)\n        frame = _command_call_fields(memory, frame, 44040, 76980)\nreturn frame'}, 'append_percentage_value': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'Cursor', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 76736)\nactual = append_percentage_value_frame_fields(memory, entered)\nreturn memory.cursor_at(actual.addresses[0])'}, 'append_percentage_value_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(6, 4294962944)\nframe = _command_load_fields(memory, frame, 0, 0, 32)\nvalue = memory.state.read(4294964150, 2)\nframe = _command_load_fields(memory, frame, 0, value, 16)\nframe = _command_load_fields(memory, frame, 1, 50054, 16)\nframe = _command_load_fields(memory, frame, 2, 49153, 16)\nframe = _command_call_fields(memory, frame, 75530, 76760)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 2, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50600, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nvalue = memory.state.read(4294962952, 2)\nframe = _command_load_fields(memory, frame, 0, value, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 49153, 16, True, True)\nif not not frame.status_word & 4:\n    value = memory.state.read(4294964152, 2)\n    frame = _command_test_fields(memory, frame, value, 16)\n    if not not frame.status_word & 4:\n        frame = _command_load_fields(memory, frame, 0, 50054, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[0] & 65535, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nvalue = memory.state.read(4294962954, 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), value, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 8, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame'}, 'append_percentage_value_rows': {'signature': 'state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': "memory, entered = _command_legacy_entry(state, entry_frame, 76500)\nchecked_cursor(out, state)\nif out.base != entered.addresses[0]:\n    raise ValueError('legacy output must be the actual A0 entry')\nactual = append_percentage_value_rows_frame_fields(memory, entered)\nout.base = actual.addresses[0]\nreturn None"}, 'append_percentage_value_rows_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 9, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 9, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 50588, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50460, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 49193, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[0] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)\nframe = frame.with_data(0, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), frame.data[0] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)\nframe = frame.with_data(0, result, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[0] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)\nframe = frame.with_data(0, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), frame.data[0] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)\nframe = frame.with_data(0, result, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 49201, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[0] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)\nframe = frame.with_data(0, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), frame.data[0] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)\nframe = frame.with_data(0, result, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[0] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)\nframe = frame.with_data(0, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), frame.data[0] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)\nframe = frame.with_data(0, result, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 2, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 49153, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(22))\nreturn frame'}, 'append_selected_command_amount': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'Cursor', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 76076)\nactual = append_selected_command_amount_frame_fields(memory, entered)\nreturn memory.cursor_at(actual.addresses[0])'}, 'append_selected_command_amount_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50240, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nvalue = memory.state.read(4294964212, 4)\nframe = _command_load_fields(memory, frame, 0, value, 32)\nframe = _command_load_fields(memory, frame, 1, 50054, 16)\nframe = _command_load_fields(memory, frame, 2, 0, 16)\nframe = frame.with_address(6, 4294962956)\nframe = _command_call_fields(memory, frame, 75530, 76112)\nframe = _command_load_fields(memory, frame, 0, 5, 16)\nframe = frame.with_address(1, 4294962956)\nframe = _command_load_fields(memory, frame, 2, 0, 16)\nwhile True:\n    value = memory.state.read(u32(frame.addresses[1]), 2)\n    frame = frame.with_address(1, frame.addresses[1] + 2)\n    frame = _command_load_fields(memory, frame, 1, value, 16)\n    if not not frame.status_word & 4:\n        source = memory.state.read(4294964122, 2)\n        frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, source, 16, True, True)\n        if bool(frame.status_word & 1):\n            frame = _command_load_fields(memory, frame, 1, 49153, 16)\n        else:\n            frame = _command_load_fields(memory, frame, 1, 50054, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[1] & 65535, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 1, 16, False, False)\n    frame = frame.with_data(2, result, 16)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 16, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame'}, 'append_selected_command_row_label': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 74268)\nactual = append_selected_command_row_label_frame_fields(memory, entered)\nreturn None'}, 'append_selected_command_row_label_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\ntested = memory.state.read(4294964001, 1)\nframe = _command_bit_fields(memory, frame, tested, 3 % 8)\nif not not frame.status_word & 4:\n    frame = frame.with_address(0, u32(74278 + 34))\n    value = memory.state.read(4294964208, 2)\n    frame = _command_load_fields(memory, frame, 0, value, 16)\n    frame = _command_shift_fields(memory, frame, 0, 1, 16, False)\n    source = memory.state.read(4294964208, 2)\n    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, source, 16, False, False)\n    frame = frame.with_data(0, result, 16)\n    frame = _command_shift_fields(memory, frame, 0, 3, 16, False)\n    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 56, 16, False, False)\n    frame = frame.with_data(0, result, 16)\n    frame = _command_load_fields(memory, frame, 1, 200, 16)\n    frame = _command_load_fields(memory, frame, 2, 0, 16)\n    frame = _command_call_fields(memory, frame, 44040, 74310)\nreturn frame'}, 'append_six_place_decimal_value_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nreturn _command_decimal_transaction_fields(memory, frame)'}, 'clear_command_amount_page': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'Cursor', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 74386)\nactual = clear_command_amount_page_frame_fields(memory, entered)\nreturn memory.cursor_at(actual.addresses[0])'}, 'clear_command_amount_page_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 90), 13, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 60), 13, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 13, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 13, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 90), 49716, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 60), 49588, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 49460, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49332, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 12, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 90), 32768, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 60), 32768, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 32768, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 32768, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = frame.with_address(0, frame.addresses[0] + s16(90))\nframe = _command_load_fields(memory, frame, 0, 9, 16)\nframe = _command_load_fields(memory, frame, 1, 50098, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 14, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[1] & 65535, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 128, 16, False, False)\n    frame = frame.with_data(1, result, 16)\n    frame = _command_load_fields(memory, frame, 2, 13, 16)\n    while True:\n        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 32768, 16)\n        frame = frame.with_address(0, frame.addresses[0] + 2)\n        frame, repeat = _command_dbra_fields(frame, 2)\n        if repeat:\n            continue\n        break\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 440, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame'}, 'clear_percentage_panel': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'Cursor', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 76650)\nactual = clear_percentage_panel_frame_fields(memory, entered)\nreturn memory.cursor_at(actual.addresses[0])'}, 'clear_percentage_panel_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 66), 9, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 44), 9, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 9, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 9, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 66), 50716, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 44), 50588, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 50460, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50332, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 8, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 66), 0, 16, True)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 44), 0, 16, True)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 0, 16, True)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 66), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 88, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame'}, 'decrement_live_command_amount_small': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 76334)\nactual = decrement_live_command_amount_small_frame_fields(memory, entered)\nreturn None'}, 'decrement_live_command_amount_small_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nvalue = memory.state.read(4294964122, 2)\nframe = _command_load_fields(memory, frame, 1, value, 16)\nframe = _command_shift_fields(memory, frame, 1, 2, 16, False)\nframe = frame.with_address(0, u32(76342 + 2582))\nvalue = memory.state.read(u32(frame.addresses[0] + s16(frame.data[1] & 65535)), 4)\nframe = _command_load_fields(memory, frame, 1, value, 32)\nvalue = memory.state.read(4294964212, 4)\nframe = _command_load_fields(memory, frame, 2, value, 32)\nframe, result = _command_binary_fields(memory, frame, frame.data[2], frame.data[1], 32, True, False)\nframe = frame.with_data(2, result, 32)\nif not bool(frame.status_word & 1):\n    frame = _command_store_fields(memory, frame, 4294964212, frame.data[2], 32)\nreturn frame'}, 'find_first_set_mask_bit': {'signature': 'state: GameState, mask: Long, *, entry_frame: CommandFrame | None=None', 'returns': 'Word', 'flow': "memory, entered = _command_legacy_entry(state, entry_frame, 73722)\nuint(mask, 32)\nif mask != entered.data[0]:\n    raise ValueError('actual original mask LONG required')\nactual = find_first_set_mask_bit_frame_fields(memory, entered)\nreturn actual.data[1] & 65535"}, 'find_first_set_mask_bit_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _command_load_fields(memory, frame, 1, 0, 16)\nwhile True:\n    frame = _command_bit_fields(memory, frame, frame.data[0], frame.data[1] % 32)\n    if not frame.status_word & 4:\n        break\n    frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, False, False)\n    frame = frame.with_data(1, result, 16)\n    continue\nreturn frame'}, 'limit_live_command_amount_by_price_record': {'signature': 'state: GameState, records: Cursor, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': "memory, entered = _command_legacy_entry(state, entry_frame, 75896)\nchecked_cursor(records, state)\nif records.base != entered.addresses[0]:\n    raise ValueError('legacy records must be the actual A0 entry')\nactual = limit_live_command_amount_by_price_record_frame_fields(memory, entered)\nreturn None"}, 'limit_live_command_amount_by_price_record_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nvalue = memory.state.read(4294964108, 2)\nframe = _command_load_fields(memory, frame, 7, value, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[7] & 65535, 147, 16, True, True)\nif bool(frame.status_word & 4):\n    frame = frame.with_address(7, frame.addresses[7] - 4)\n    frame = _command_store_fields(memory, frame, frame.addresses[7], frame.data[6], 32)\n    frame = frame.with_address(1, 4294964480)\n    frame = _command_load_fields(memory, frame, 7, 0, 16)\n    while True:\n        value = memory.state.read(u32(frame.addresses[1]), 2)\n        frame = frame.with_address(1, frame.addresses[1] + 2)\n        frame = _command_load_fields(memory, frame, 6, value, 16)\n        if bool(frame.status_word & 8):\n            break\n        frame = _command_bit_fields(memory, frame, frame.data[6], 14 % 32)\n        if bool(frame.status_word & 4):\n            continue\n        frame, result = _command_binary_fields(memory, frame, frame.data[7] & 65535, 1, 16, False, False)\n        frame = frame.with_data(7, result, 16)\n        continue\n    frame = _command_product_fields(memory, frame, 7, 25000)\n    source = memory.state.read(4294964216, 4)\n    frame, result = _command_binary_fields(memory, frame, frame.data[7], source, 32, True, True)\n    if not not frame.status_word & 1:\n        frame = _command_store_fields(memory, frame, 4294964216, frame.data[7], 32)\n    frame = _command_store_fields(memory, frame, 4294964122, 5, 16)\n    frame = _command_store_fields(memory, frame, 4294964220, 5, 16)\n    value = memory.state.read(u32(frame.addresses[7]), 4)\n    frame = frame.with_address(7, frame.addresses[7] + 4)\n    frame = _command_load_fields(memory, frame, 6, value, 32)\nelse:\n    while True:\n        source = memory.state.read(u32(frame.addresses[0]), 2)\n        frame, result = _command_binary_fields(memory, frame, frame.data[7] & 65535, source, 16, True, True)\n        if bool(frame.status_word & 4):\n            break\n        frame = frame.with_address(0, frame.addresses[0] + 8)\n        continue\n    value = memory.state.read(u32(frame.addresses[0] + 2), 4)\n    frame = _command_load_fields(memory, frame, 7, value, 32)\n    source = memory.state.read(4294964216, 4)\n    frame, result = _command_binary_fields(memory, frame, frame.data[7], source, 32, True, True)\n    if not not frame.status_word & 1:\n        frame = _command_store_fields(memory, frame, 4294964216, frame.data[7], 32)\n    value = memory.state.read(u32(frame.addresses[0] + 6), 2)\n    frame = _command_load_fields(memory, frame, 7, value, 16)\n    frame = _command_store_fields(memory, frame, 4294964122, frame.data[7] & 65535, 16)\n    frame = _command_store_fields(memory, frame, 4294964220, frame.data[7] & 65535, 16)\nreturn frame'}, 'prepare_budget_amount_page': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'Cursor', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 74516)\nactual = prepare_budget_amount_page_frame_fields(memory, entered)\nreturn memory.cursor_at(actual.addresses[0])'}, 'prepare_budget_amount_page_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 11, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50610, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 8, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 11, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 11, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 50866, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50738, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 8, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 49153, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(26))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 11, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 11, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 51122, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50994, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49233, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 49234, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 2), 49235, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), 49236, 16)\nframe = frame.with_address(0, frame.addresses[0] + 4)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 49153, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nvalue = memory.state.read(4294964212, 4)\nframe = _command_load_fields(memory, frame, 0, value, 32)\nframe = _command_load_fields(memory, frame, 1, 50054, 16)\nframe = _command_load_fields(memory, frame, 2, 49153, 16)\nframe = frame.with_address(6, 4294955776)\nframe = _command_call_fields(memory, frame, 75530, 74700)\nframe = frame.with_address(1, 4294955776)\nframe = _command_load_fields(memory, frame, 0, 5, 16)\nwhile True:\n    value = memory.state.read(u32(frame.addresses[1]), 2)\n    frame = frame.with_address(1, frame.addresses[1] + 2)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), value, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(26))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 11, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 51250, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 8, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54145, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 56192, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 156, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nframe = _command_call_fields(memory, frame, 73736, 74774)\nreturn frame'}, 'prepare_budget_summary_panel': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'Cursor', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 72946)\nactual = prepare_budget_summary_panel_frame_fields(memory, entered)\nreturn memory.cursor_at(actual.addresses[0])'}, 'prepare_budget_summary_panel_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 6, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 50082, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49954, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 5, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 32768, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 32768, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = frame.with_address(0, frame.addresses[0] + s16(16))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50210, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 3, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 6, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 50466, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50338, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 1, 49269, 16)\nframe = _command_load_fields(memory, frame, 2, 3, 16)\nframe = _command_call_fields(memory, frame, 73258, 73066)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(16))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50594, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 3, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 6, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 50850, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50722, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 1, 49277, 16)\nframe = _command_load_fields(memory, frame, 2, 3, 16)\nframe = _command_call_fields(memory, frame, 73258, 73150)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(16))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50978, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 3, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54145, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 56192, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 32), 6, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 6, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 32), 51362, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 51234, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 51106, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 5, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 32), 32768, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 32768, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 32768, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 192, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame'}, 'prepare_command_amount_limit': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'Cursor', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 75660)\nactual = prepare_command_amount_limit_frame_fields(memory, entered)\nreturn memory.cursor_at(actual.addresses[0])'}, 'prepare_command_amount_limit_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 44), 9, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 9, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 9, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 44), 50364, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 50236, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50108, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 44), 54144, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 6, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 44), 54145, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 49153, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 50054, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 44), 56192, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 44), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 66, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nvalue = memory.state.read(4294964068, 2)\nframe = _command_load_fields(memory, frame, 0, value, 16)\nframe = _command_shift_fields(memory, frame, 0, 2, 16, False)\nframe = frame.with_address(1, 4294959100)\nvalue = memory.state.read(u32(frame.addresses[1] + s16(frame.data[0] & 65535)), 4)\nframe = _command_load_fields(memory, frame, 0, value, 32)\nframe = _command_store_fields(memory, frame, 4294964216, frame.data[0], 32)\nframe = frame.with_address(0, u32(75792 + 48))\nframe = _command_call_fields(memory, frame, 75896, 75800)\nvalue = memory.state.read(4294964216, 4)\nframe = _command_load_fields(memory, frame, 0, value, 32)\nframe = _command_load_fields(memory, frame, 1, 50054, 16)\nframe = _command_load_fields(memory, frame, 2, 0, 16)\nframe = frame.with_address(6, 4294962944)\nframe = _command_call_fields(memory, frame, 75530, 75820)\nframe = _command_store_fields(memory, frame, 4294964744, 1, 16)\ndestination = memory.state.read(4294964132, 2)\nresult = destination | 32832\nframe = _command_store_fields(memory, frame, 4294964132, result, 16)\ndestination = memory.state.read(4294964132, 2)\nresult = destination & 63999\nframe = _command_store_fields(memory, frame, 4294964132, result, 16)\nreturn frame'}, 'prepare_command_amount_modal': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'Cursor', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 73736)\nactual = prepare_command_amount_modal_frame_fields(memory, entered)\nreturn memory.cursor_at(actual.addresses[0])'}, 'prepare_command_amount_modal_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_call_fields(memory, frame, 73764, 73748)\nframe = _command_call_fields(memory, frame, 73828, 73754)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 120, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame'}, 'prepare_compact_budget_summary_panel': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'Cursor', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 73276)\nactual = prepare_compact_budget_summary_panel_frame_fields(memory, entered)\nreturn memory.cursor_at(actual.addresses[0])'}, 'prepare_compact_budget_summary_panel_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50210, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 3, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 6, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 50466, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50338, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 2, 3, 16)\nframe = _command_load_fields(memory, frame, 1, 49285, 16)\nframe = _command_call_fields(memory, frame, 73258, 73352)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(16))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50594, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 3, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 6, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 50850, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50722, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 2, 1, 16)\nframe = _command_load_fields(memory, frame, 1, 49293, 16)\nframe = _command_call_fields(memory, frame, 73258, 73436)\nframe = _command_load_fields(memory, frame, 2, 1, 16)\nframe = _command_load_fields(memory, frame, 1, 49153, 16)\nframe = _command_call_fields(memory, frame, 73258, 73448)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(16))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50978, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 3, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54145, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 56192, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 112, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame'}, 'prepare_percentage_panel': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'Cursor', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 76440)\nactual = prepare_percentage_panel_frame_fields(memory, entered)\nreturn memory.cursor_at(actual.addresses[0])'}, 'prepare_percentage_panel_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_call_fields(memory, frame, 76470, 76452)\nframe = _command_call_fields(memory, frame, 76500, 76456)\nframe = _command_call_fields(memory, frame, 76620, 76460)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 88, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame'}, 'prepare_resource_amount_panel': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'Cursor', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 76990)\nactual = prepare_resource_amount_panel_frame_fields(memory, entered)\nreturn memory.cursor_at(actual.addresses[0])'}, 'prepare_resource_amount_panel_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_call_fields(memory, frame, 77044, 77002)\nframe = _command_call_fields(memory, frame, 77308, 77006)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 364, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nframe = _command_store_fields(memory, frame, 4294964122, 5, 16)\nframe = _command_store_fields(memory, frame, 4294964744, 1, 16)\nframe = _command_store_fields(memory, frame, 4294964744, 1, 16)\ndestination = memory.state.read(4294964132, 2)\nresult = destination | 32832\nframe = _command_store_fields(memory, frame, 4294964132, result, 16)\ndestination = memory.state.read(4294964132, 2)\nresult = destination & 63999\nframe = _command_store_fields(memory, frame, 4294964132, result, 16)\nreturn frame'}, 'select_descriptor_portrait_parts': {'signature': 'state: GameState, retained_mask_high: Word=0, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 73602)\nactual = select_descriptor_portrait_parts_frame_fields(memory, entered)\nreturn None'}, 'select_descriptor_portrait_parts_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nvalue = memory.state.read(16726060, 4)\nframe = frame.with_address(0, value)\nvalue = memory.state.read(u32(frame.addresses[0] + 1), 1)\nframe = _command_load_fields(memory, frame, 0, value, 8)\nvalue = memory.state.read(u32(frame.addresses[0] + 2), 1)\nframe = _command_load_fields(memory, frame, 1, value, 8)\nframe = _command_load_fields(memory, frame, 2, 0, 16)\nframe = frame.with_address(1, 871714)\nwhile True:\n    source = memory.state.read(u32(frame.addresses[1]), 1)\n    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 255, source, 8, True, True)\n    if not frame.status_word & 4:\n        frame = frame.with_address(1, frame.addresses[1] + 2)\n        frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 1, 16, False, False)\n        frame = frame.with_data(2, result, 16)\n        continue\n    source = memory.state.read(u32(frame.addresses[1] + 1), 1)\n    frame, result = _command_binary_fields(memory, frame, frame.data[1] & 255, source, 8, True, True)\n    if bool(frame.status_word & 4):\n        break\n    frame = frame.with_address(1, frame.addresses[1] + 2)\n    frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 1, 16, False, False)\n    frame = frame.with_data(2, result, 16)\n    continue\nframe = _command_load_fields(memory, frame, 0, frame.data[2] & 65535, 16)\nframe = _command_shift_fields(memory, frame, 0, 1, 16, False)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, frame.data[2] & 65535, 16, False, False)\nframe = frame.with_data(0, result, 16)\nframe = frame.with_address(0, 871727)\nvalue = memory.state.read(u32(frame.addresses[0] + s16(frame.data[0] & 65535)), 1)\nframe = _command_store_fields(memory, frame, 4294963123, value, 8)\nvalue = memory.state.read(u32(frame.addresses[0] + 1 + s16(frame.data[0] & 65535)), 1)\nframe = _command_store_fields(memory, frame, 4294963125, value, 8)\nvalue = memory.state.read(u32(frame.addresses[0] + 2 + s16(frame.data[0] & 65535)), 1)\nframe = _command_store_fields(memory, frame, 4294963127, value, 8)\ntested = memory.state.read(4294964132, 1)\nframe = _command_bit_fields(memory, frame, tested, 0 % 8)\nif not not frame.status_word & 4:\n    value = memory.state.read(4294963122, 2)\n    frame = _command_load_fields(memory, frame, 0, value, 16)\n    frame = _command_call_fields(memory, frame, 73722, 73692)\n    frame = _command_store_fields(memory, frame, 4294963044, frame.data[1] & 65535, 16)\n    value = memory.state.read(4294963124, 2)\n    frame = _command_load_fields(memory, frame, 0, value, 16)\n    frame = _command_call_fields(memory, frame, 73722, 73704)\n    frame = _command_store_fields(memory, frame, 4294963046, frame.data[1] & 65535, 16)\n    value = memory.state.read(4294963126, 2)\n    frame = _command_load_fields(memory, frame, 0, value, 16)\n    frame = _command_call_fields(memory, frame, 73722, 73716)\n    frame = _command_store_fields(memory, frame, 4294963048, frame.data[1] & 65535, 16)\nreturn frame'}, 'select_next_amount_place': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 76280)\nactual = select_next_amount_place_frame_fields(memory, entered)\nreturn None'}, 'select_next_amount_place_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nvalue = memory.state.read(4294964122, 2)\nframe = _command_load_fields(memory, frame, 0, value, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)\nframe = frame.with_data(0, result, 16)\nsource = memory.state.read(4294964220, 2)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, source, 16, True, True)\nif not not frame.status_word & 5:\n    destination = memory.state.read(4294964122, 2)\n    frame, result = _command_binary_fields(memory, frame, destination, 1, 16, False, False)\n    memory.state.write(4294964122, 2, result)\nreturn frame'}, 'select_previous_amount_place': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 76254)\nactual = select_previous_amount_place_frame_fields(memory, entered)\nreturn None'}, 'select_previous_amount_place_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nvalue = memory.state.read(4294964122, 2)\nframe = _command_load_fields(memory, frame, 0, value, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, True, False)\nframe = frame.with_data(0, result, 16)\nif not bool(frame.status_word & 1):\n    frame = _command_shift_fields(memory, frame, 0, 1, 16, False)\n    frame = frame.with_address(0, 4294962944)\n    value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[0] & 65535)), 2)\n    frame = _command_test_fields(memory, frame, value, 16)\n    if not bool(frame.status_word & 4):\n        destination = memory.state.read(4294964122, 2)\n        frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)\n        memory.state.write(4294964122, 2, result)\nreturn frame'}, 'step_budget_amount_controls': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 74776)\nactual = step_budget_amount_controls_frame_fields(memory, entered)\nreturn None'}, 'step_budget_amount_controls_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nvalue = memory.state.read(4294964738, 1)\nframe = _command_load_fields(memory, frame, 0, value, 8)\nresult = frame.data[0] & 65535 & 12\nframe = _command_load_fields(memory, frame, 0, result, 16)\nif bool(frame.status_word & 4):\n    value = memory.state.read(4294964738, 1)\n    frame = _command_load_fields(memory, frame, 0, value, 8)\n    result = frame.data[0] & 65535 & 3\n    frame = _command_load_fields(memory, frame, 0, result, 16)\n    if bool(frame.status_word & 4):\n        frame = _command_store_fields(memory, frame, 4294964744, 1, 16)\n        frame = _command_call_fields(memory, frame, 75052, 75002)\n    else:\n        destination = memory.state.read(4294964744, 2)\n        frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)\n        memory.state.write(4294964744, 2, result)\n        if not not frame.status_word & 4:\n            frame = _command_store_fields(memory, frame, 4294964744, 12, 16)\n            frame = _command_bit_fields(memory, frame, frame.data[0], 1 % 32)\n            if not frame.status_word & 4:\n                frame = _command_load_fields(memory, frame, 0, 5, 16)\n                source = memory.state.read(4294964122, 2)\n                frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, source, 16, True, False)\n                frame = frame.with_data(0, result, 16)\n                frame = _command_shift_fields(memory, frame, 0, 2, 16, False)\n                frame = frame.with_address(0, u32(74954 + 50))\n                value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[0] & 65535)), 4)\n                frame = _command_load_fields(memory, frame, 1, value, 32)\n                value = memory.state.read(4294964212, 4)\n                frame = _command_load_fields(memory, frame, 2, value, 32)\n                frame, result = _command_binary_fields(memory, frame, frame.data[2], frame.data[1], 32, True, False)\n                frame = frame.with_data(2, result, 32)\n                if not bool(frame.status_word & 1):\n                    frame = _command_store_fields(memory, frame, 4294964212, frame.data[2], 32)\n                    frame = frame.with_address(0, u32(74976 + 52))\n                    value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[0] & 65535)), 4)\n                    frame = _command_load_fields(memory, frame, 1, value, 32)\n                    destination = memory.state.read(4294964154, 4)\n                    frame, result = _command_binary_fields(memory, frame, destination, frame.data[1], 32, True, False)\n                    memory.state.write(4294964154, 4, result)\n                    frame = _command_call_fields(memory, frame, 75052, 75002)\n            else:\n                frame = _command_load_fields(memory, frame, 0, 5, 16)\n                source = memory.state.read(4294964122, 2)\n                frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, source, 16, True, False)\n                frame = frame.with_data(0, result, 16)\n                frame = _command_shift_fields(memory, frame, 0, 2, 16, False)\n                frame = frame.with_address(0, u32(74906 + 98))\n                value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[0] & 65535)), 4)\n                frame = _command_load_fields(memory, frame, 1, value, 32)\n                source = memory.state.read(4294964212, 4)\n                frame, result = _command_binary_fields(memory, frame, frame.data[1], source, 32, False, False)\n                frame = frame.with_data(1, result, 32)\n                source = memory.state.read(4294964216, 4)\n                frame, result = _command_binary_fields(memory, frame, frame.data[1], source, 32, True, True)\n                if not not frame.status_word & 5:\n                    frame = _command_store_fields(memory, frame, 4294964212, frame.data[1], 32)\n                    frame = frame.with_address(0, u32(74930 + 98))\n                    value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[0] & 65535)), 4)\n                    frame = _command_load_fields(memory, frame, 1, value, 32)\n                    destination = memory.state.read(4294964154, 4)\n                    frame, result = _command_binary_fields(memory, frame, destination, frame.data[1], 32, False, False)\n                    memory.state.write(4294964154, 4, result)\n                    frame = _command_call_fields(memory, frame, 75052, 75002)\nelse:\n    destination = memory.state.read(4294964744, 2)\n    frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)\n    memory.state.write(4294964744, 2, result)\n    if not not frame.status_word & 4:\n        frame = _command_store_fields(memory, frame, 4294964744, 12, 16)\n        frame = _command_bit_fields(memory, frame, frame.data[0], 3 % 32)\n        if not frame.status_word & 4:\n            value = memory.state.read(4294964122, 2)\n            frame = _command_load_fields(memory, frame, 1, value, 16)\n            frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, False, False)\n            frame = frame.with_data(1, result, 16)\n            frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 5, 16, True, True)\n            if not not frame.status_word & 5:\n                frame = _command_store_fields(memory, frame, 4294964122, frame.data[1] & 65535, 16)\n                frame = _command_call_fields(memory, frame, 75052, 75002)\n        else:\n            frame = _command_load_fields(memory, frame, 1, 5, 16)\n            source = memory.state.read(4294964122, 2)\n            frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, source, 16, True, False)\n            frame = frame.with_data(1, result, 16)\n            frame = _command_shift_fields(memory, frame, 1, 2, 16, False)\n            frame = frame.with_address(0, u32(74818 + 190))\n            value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[1] & 65535)), 4)\n            frame = _command_load_fields(memory, frame, 2, value, 32)\n            source = memory.state.read(4294964216, 4)\n            frame, result = _command_binary_fields(memory, frame, frame.data[2], source, 32, True, True)\n            if not not frame.status_word & 5:\n                destination = memory.state.read(4294964122, 2)\n                frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)\n                memory.state.write(4294964122, 2, result)\n                frame = _command_call_fields(memory, frame, 75052, 75002)\nreturn frame'}, 'step_live_command_amount_controls': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 76160)\nactual = step_live_command_amount_controls_frame_fields(memory, entered)\nreturn None'}, 'step_live_command_amount_controls_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nvalue = memory.state.read(4294964738, 1)\nframe = _command_load_fields(memory, frame, 0, value, 8)\nresult = frame.data[0] & 65535 & 12\nframe = _command_load_fields(memory, frame, 0, result, 16)\nif bool(frame.status_word & 4):\n    value = memory.state.read(4294964738, 1)\n    frame = _command_load_fields(memory, frame, 0, value, 8)\n    result = frame.data[0] & 65535 & 3\n    frame = _command_load_fields(memory, frame, 0, result, 16)\n    if bool(frame.status_word & 4):\n        frame = _command_store_fields(memory, frame, 4294964744, 1, 16)\n    else:\n        destination = memory.state.read(4294964744, 2)\n        frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)\n        memory.state.write(4294964744, 2, result)\n        if not not frame.status_word & 4:\n            frame = _command_store_fields(memory, frame, 4294964744, 12, 16)\n            frame = _command_bit_fields(memory, frame, frame.data[0], 1 % 32)\n            if not frame.status_word & 4:\n                frame = _command_call_fields(memory, frame, 76334, 76244)\n            else:\n                frame = _command_call_fields(memory, frame, 76300, 76238)\nelse:\n    destination = memory.state.read(4294964744, 2)\n    frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)\n    memory.state.write(4294964744, 2, result)\n    if not not frame.status_word & 4:\n        frame = _command_store_fields(memory, frame, 4294964744, 12, 16)\n        frame = _command_bit_fields(memory, frame, frame.data[0], 3 % 32)\n        if not frame.status_word & 4:\n            frame = _command_call_fields(memory, frame, 76280, 76202)\n        else:\n            frame = _command_call_fields(memory, frame, 76254, 76196)\nreturn frame'}, 'step_percentage_controls': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 76812)\nactual = step_percentage_controls_frame_fields(memory, entered)\nreturn None'}, 'step_percentage_controls_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nvalue = memory.state.read(4294964738, 1)\nframe = _command_load_fields(memory, frame, 0, value, 8)\nresult = frame.data[0] & 255 & 12\nframe = _command_load_fields(memory, frame, 0, result, 8)\nif bool(frame.status_word & 4):\n    value = memory.state.read(4294964738, 1)\n    frame = _command_load_fields(memory, frame, 0, value, 8)\n    result = frame.data[0] & 255 & 3\n    frame = _command_load_fields(memory, frame, 0, result, 8)\n    if bool(frame.status_word & 4):\n        frame = _command_store_fields(memory, frame, 4294964744, 1, 16)\n    else:\n        destination = memory.state.read(4294964744, 2)\n        frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)\n        memory.state.write(4294964744, 2, result)\n        if not not frame.status_word & 4:\n            frame = _command_store_fields(memory, frame, 4294964744, 12, 16)\n            frame = _command_load_fields(memory, frame, 1, 1, 16)\n            value = memory.state.read(4294964152, 2)\n            frame = _command_test_fields(memory, frame, value, 16)\n            if not not frame.status_word & 4:\n                frame = _command_load_fields(memory, frame, 1, 10, 16)\n            tested = memory.state.read(4294964738, 1)\n            frame = _command_bit_fields(memory, frame, tested, 1 % 8)\n            if not frame.status_word & 4:\n                destination = memory.state.read(4294964150, 2)\n                frame, result = _command_binary_fields(memory, frame, destination, frame.data[1] & 65535, 16, True, False)\n                memory.state.write(4294964150, 2, result)\n                if not not frame.status_word & 8:\n                    destination = memory.state.read(4294964150, 2)\n                    frame, result = _command_binary_fields(memory, frame, destination, frame.data[1] & 65535, 16, False, False)\n                    memory.state.write(4294964150, 2, result)\n            else:\n                destination = memory.state.read(4294964150, 2)\n                frame, result = _command_binary_fields(memory, frame, destination, frame.data[1] & 65535, 16, False, False)\n                memory.state.write(4294964150, 2, result)\n                destination = memory.state.read(4294964150, 2)\n                frame, result = _command_binary_fields(memory, frame, destination, 99, 16, True, True)\n                if not bool(frame.status_word & 5):\n                    destination = memory.state.read(4294964150, 2)\n                    frame, result = _command_binary_fields(memory, frame, destination, frame.data[1] & 65535, 16, True, False)\n                    memory.state.write(4294964150, 2, result)\nelse:\n    destination = memory.state.read(4294964744, 2)\n    frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)\n    memory.state.write(4294964744, 2, result)\n    if not not frame.status_word & 4:\n        frame = _command_bit_fields(memory, frame, frame.data[0], 3 % 32)\n        if not frame.status_word & 4:\n            frame = _command_store_fields(memory, frame, 4294964152, 1, 16)\n        else:\n            frame = _command_store_fields(memory, frame, 4294964152, 0, 16, True)\nreturn frame'}, 'update_player_command_amount': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 76002)\nactual = update_player_command_amount_frame_fields(memory, entered)\nreturn None'}, 'update_player_command_amount_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _command_call_fields(memory, frame, 76076, 76006)\nframe = _command_call_fields(memory, frame, 76160, 76010)\nframe = _command_call_fields(memory, frame, 76366, 76014)\ntested = memory.state.read(4294964739, 1)\nframe = _command_bit_fields(memory, frame, tested, 5 % 8)\nif bool(frame.status_word & 4):\n    tested = memory.state.read(4294964739, 1)\n    frame = _command_bit_fields(memory, frame, tested, 4 % 8)\n    if not bool(frame.status_word & 4):\n        frame = _command_store_fields(memory, frame, 4294964754, 520, 16)\n        frame = _command_store_fields(memory, frame, 4294964066, 2, 16)\n        frame = _command_store_fields(memory, frame, 4294964074, 18, 16)\nelse:\n    value = memory.state.read(4294964212, 4)\n    frame = _command_store_fields(memory, frame, 4294964126, value, 32)\n    value = memory.state.read(4294964212, 4)\n    frame = _command_test_fields(memory, frame, value, 32)\n    if not bool(frame.status_word & 4):\n        frame = _command_store_fields(memory, frame, 4294964754, 520, 16)\n        frame = _command_store_fields(memory, frame, 4294964066, 4, 16)\nreturn frame'}})
APPROVED.setdefault('contexts_command_fields',set()).update(['CommandFrame', 'CommandMenuMemory', '_command_binary_fields', '_command_bit_fields', '_command_call_fields', '_command_dbra_fields', '_command_decimal_place_fields', '_command_decimal_transaction_fields', '_command_load_fields', '_command_numbered_pair_fields', '_command_product_fields', '_command_quotient_fields', '_command_shift_fields', '_command_store_fields', '_command_tail_fields', '_command_test_fields'])
APPROVED.setdefault('domain',set()).update({'s16'})

# C57 actual 1293C shared entry; entire same-core declarations.
DECLARATIONS.update({'_budget_known_fields': {'signature': 'memory, frame, target', 'returns': None, 'flow': 'if target == 72946:\n    return prepare_budget_summary_panel_frame_fields(memory, frame)\nif target == 73258:\n    return append_numbered_budget_columns_frame_fields(memory, frame)\nif target == 73276:\n    return prepare_compact_budget_summary_panel_frame_fields(memory, frame)\nif target == 73602:\n    return select_descriptor_portrait_parts_frame_fields(memory, frame)\nif target == 73722:\n    return find_first_set_mask_bit_frame_fields(memory, frame)\nif target == 73736:\n    return prepare_command_amount_modal_frame_fields(memory, frame)\nif target == 73764:\n    return append_amount_modal_frame_frame_fields(memory, frame)\nif target == 73828:\n    return append_amount_modal_descriptor_limit_frame_fields(memory, frame)\nif target == 74268:\n    return append_selected_command_row_label_frame_fields(memory, frame)\nif target == 74386:\n    return clear_command_amount_page_frame_fields(memory, frame)\nif target == 74516:\n    return prepare_budget_amount_page_frame_fields(memory, frame)\nif target == 74776:\n    return step_budget_amount_controls_frame_fields(memory, frame)\nif target == 75052:\n    return append_budget_cost_and_amount_values_frame_fields(memory, frame)\nif target == 75180:\n    return append_budget_place_highlight_frame_fields(memory, frame)\nif target == 75266:\n    return append_budget_header_row_frame_fields(memory, frame)\nif target == 75296:\n    return append_budget_first_detail_rows_frame_fields(memory, frame)\nif target == 75404:\n    return append_budget_second_detail_row_frame_fields(memory, frame)\nif target == 75474:\n    return append_budget_footer_row_frame_fields(memory, frame)\nif target == 75504:\n    return append_four_budget_numbered_tiles_frame_fields(memory, frame)\nif target == 75530:\n    return append_six_place_decimal_value_frame_fields(memory, frame)\nif target == 75616:\n    return append_decimal_value_place_frame_fields(memory, frame)\nif target == 75660:\n    return prepare_command_amount_limit_frame_fields(memory, frame)\nif target == 75896:\n    return limit_live_command_amount_by_price_record_frame_fields(memory, frame)\nif target == 76002:\n    return update_player_command_amount_frame_fields(memory, frame)\nif target == 76076:\n    return append_selected_command_amount_frame_fields(memory, frame)\nif target == 76092:\n    return append_selected_command_amount_frame_fields(memory, frame, 76092)\nif target == 76160:\n    return step_live_command_amount_controls_frame_fields(memory, frame)\nif target == 76254:\n    return select_previous_amount_place_frame_fields(memory, frame)\nif target == 76280:\n    return select_next_amount_place_frame_fields(memory, frame)\nif target == 76300:\n    return add_selected_cost_frame_fields(memory, frame)\nif target == 76334:\n    return decrement_live_command_amount_small_frame_fields(memory, frame)\nif target == 76366:\n    return append_blinking_amount_place_frame_fields(memory, frame)\nif target == 76440:\n    return prepare_percentage_panel_frame_fields(memory, frame)\nif target == 76470:\n    return append_percentage_header_row_frame_fields(memory, frame)\nif target == 76500:\n    return append_percentage_value_rows_frame_fields(memory, frame)\nif target == 76620:\n    return append_percentage_footer_row_frame_fields(memory, frame)\nif target == 76650:\n    return clear_percentage_panel_frame_fields(memory, frame)\nif target == 76736:\n    return append_percentage_value_frame_fields(memory, frame)\nif target == 76812:\n    return step_percentage_controls_frame_fields(memory, frame)\nif target == 76932:\n    return append_percentage_place_highlight_frame_fields(memory, frame)\nif target == 76990:\n    return prepare_resource_amount_panel_frame_fields(memory, frame)\nif target == 77044:\n    return append_city_resource_amount_rows_frame_fields(memory, frame)\nif target == 77186:\n    return append_live_resource_value_row_frame_fields(memory, frame)\nif target == 77308:\n    return append_committed_resource_amount_rows_frame_fields(memory, frame)\nif target == 77428:\n    return append_committed_resource_value_row_frame_fields(memory, frame)\nreturn None'}, 'append_selected_command_amount_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame, entry: int=76076', 'returns': 'CommandFrame', 'flow': "if type(entry) is not int or entry not in (76076, 76092):\n    raise ValueError('only actual selected-amount entry or middle entry required')\nframe = memory.enter(frame)\nif entry == 76076:\n    frame = frame.with_address(0, 4294955264)\n    value = memory.state.read(4294963994, 2)\n    frame = frame.with_address(0, frame.addresses[0] + s16(value))\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50240, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\nvalue = memory.state.read(4294964212, 4)\nframe = _command_load_fields(memory, frame, 0, value, 32)\nframe = _command_load_fields(memory, frame, 1, 50054, 16)\nframe = _command_load_fields(memory, frame, 2, 0, 16)\nframe = frame.with_address(6, 4294962956)\nframe = _command_call_fields(memory, frame, 75530, 76112)\nframe = _command_load_fields(memory, frame, 0, 5, 16)\nframe = frame.with_address(1, 4294962956)\nframe = _command_load_fields(memory, frame, 2, 0, 16)\nwhile True:\n    value = memory.state.read(u32(frame.addresses[1]), 2)\n    frame = frame.with_address(1, frame.addresses[1] + 2)\n    frame = _command_load_fields(memory, frame, 1, value, 16)\n    if not not frame.status_word & 4:\n        source = memory.state.read(4294964122, 2)\n        frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, source, 16, True, True)\n        if bool(frame.status_word & 1):\n            frame = _command_load_fields(memory, frame, 1, 49153, 16)\n        else:\n            frame = _command_load_fields(memory, frame, 1, 50054, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[1] & 65535, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 1, 16, False, False)\n    frame = frame.with_data(2, result, 16)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 16, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame"}})

# B151: exact existing12A0C full-Frame ABI; no new CODE ownership.
DECLARATIONS.update({'add_selected_cost_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nvalue = memory.state.read(4294964122, 2)\nframe = _command_load_fields(memory, frame, 1, value, 16)\nframe = _command_shift_fields(memory, frame, 1, 2, 16)\nframe = frame.with_address(0, 78924)\nvalue = memory.state.read(u32(frame.addresses[0] + s16(frame.data[1] & 65535)), 4)\nframe = _command_load_fields(memory, frame, 1, value, 32)\nsource = memory.state.read(4294964212, 4)\nframe, result = _command_binary_fields(memory, frame, frame.data[1], source, 32)\nframe = frame.with_data(1, result, 32)\nsource = memory.state.read(4294964216, 4)\nframe, ignored = _command_binary_fields(memory, frame, frame.data[1], source, 32, True, True)\nif not frame.status_word & 5:\n    return frame\nreturn _command_store_fields(memory, frame, 4294964212, frame.data[1], 32)'}})
